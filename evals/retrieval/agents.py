"""Translate each CLI's stream into calls in start order, keeping result text for scoring."""
import json
import os
import re
import shlex
import tempfile
from itertools import zip_longest
from pathlib import Path

AGENTS = ("opus", "codex", "grok")
SETTINGS = '{"enabledPlugins":{"atlas@atlas-marketplace":false}}'


def agent_env(out):
    env = {k: v for k, v in os.environ.items() if k not in (
        "ATLAS_BRAIN_PATH", "ATLAS_QMD_CMD", "ATLAS_OBSIDIAN_CMD", "ATLAS_QMD_REFRESH", "ATLAS_RETRIEVAL_LOG")}
    env["ATLAS_CONFIG"] = str(out / "atlas.env")
    return env


def command(agent, prompt, home, version, brain, model="opus"):
    if agent == "opus":
        return ["claude", "-p", prompt, "--model", model, "--plugin-dir", str(version),
                "--settings", SETTINGS, "--add-dir", str(brain), "--output-format", "stream-json",
                "--verbose", "--permission-mode", "bypassPermissions"]
    if agent == "codex":
        return ["codex", "exec", "--json", "-s", "danger-full-access", "--skip-git-repo-check", prompt]
    if agent == "grok":
        return ["grok", "-p", prompt, "--output-format", "streaming-json", "--always-approve",
                "--cwd", str(home)]
    raise ValueError(f"Unknown agent {agent}")


def unwrap(cmd):
    try:
        parts = shlex.split(cmd)
    except ValueError:
        return cmd
    if len(parts) == 3 and Path(parts[0]).name in ("bash", "zsh", "sh") and parts[1] == "-lc":
        return parts[2]
    return cmd


def content(value):
    if isinstance(value, list):
        return "\n".join(content(part) for part in value)
    if isinstance(value, dict):
        return content(value.get("text", value.get("content", "")))
    return value if isinstance(value, str) else ""


def parse(agent, jsonl_path, times_path):
    record = dict(agent=agent, answer="", calls=[], usage={}, cost_usd=None, session_ok=False)
    by_id = {}
    results = {}

    def start(key, tool, args, t):
        if key in by_id:
            return
        value = unwrap(args["command"]) if isinstance(args, dict) and "command" in args else (
            json.dumps(args, ensure_ascii=False, separators=(",", ":")))
        call = dict(i=len(by_id) + 1, t=t, tool=tool, input=value, output="", error=False)
        by_id[key] = call
        record["calls"].append(call)

    times = Path(times_path)
    offsets = times.read_text().splitlines() if times.exists() else []
    with Path(jsonl_path).open(errors="replace") as stream:
        for line, stamp in zip_longest(stream, offsets):
            try:
                event = json.loads(line or "")
            except ValueError:
                continue
            if not isinstance(event, dict):
                continue
            t = float(stamp) if stamp else None
            kind = event.get("type")
            if agent == "opus":
                message = event.get("message")
                for block in message.get("content", []) if isinstance(message, dict) else []:
                    if not isinstance(block, dict):
                        continue
                    if block.get("type") == "tool_use":
                        start(block["id"], block["name"], block.get("input", {}), t)
                    if block.get("type") == "tool_result":
                        results[block["tool_use_id"]] = dict(output=content(block.get("content"))[:20000],
                                                             error=bool(block.get("is_error")))
                if kind == "result":
                    record.update(answer=event.get("result", ""), cost_usd=event.get("total_cost_usd"),
                                  usage=event.get("usage", {}), session_ok=not event.get("is_error"))
            elif agent == "codex":
                item = event.get("item", {})
                if item.get("type") == "command_execution" and kind in ("item.started", "item.completed"):
                    key = item["id"]
                    start(key, "command_execution", {"command": item.get("command", "")}, t)
                    if kind == "item.completed":
                        code = item.get("exit_code")
                        results[key] = dict(output=(item.get("aggregated_output") or "")[:20000],
                                            exit_code=code, error=code not in (0, 1))
                if kind == "item.completed" and item.get("type") == "agent_message":
                    record["answer"] = item["text"]
                if kind == "turn.completed":
                    record.update(usage=event.get("usage", {}), session_ok=True)
            elif agent == "grok":
                if kind in ("tool_call", "tool_call_update"):
                    record["answer"] = ""
                    key = event["toolCallId"]
                    if kind == "tool_call":
                        start(key, event.get("toolName") or event.get("title", ""), event.get("rawInput", {}), t)
                    else:
                        result = event.get("rawOutput")
                        raw = result.get("stdout") if isinstance(result, dict) else result
                        if isinstance(raw, list):
                            raw = bytes(raw).decode(errors="replace")
                        output = content(raw) or content(event.get("content"))
                        if output or event.get("status") in ("completed", "failed"):
                            previous = results.get(key, {})
                            results[key] = dict(output=(output or previous.get("output", ""))[:20000],
                                                error=event.get("status") == "failed")
                if kind == "text":
                    record["answer"] += event.get("data", "")
                if kind == "usage":
                    for name, value in event.get("usage", {}).items():
                        if isinstance(value, (int, float)):
                            record["usage"][name] = record["usage"].get(name, 0) + value
            else:
                raise ValueError(f"Unknown agent {agent}")
    for key, result in results.items():
        if key in by_id:
            by_id[key].update(result)
    if agent == "grok":
        record["session_ok"] = bool(record["answer"].strip())
    return record


def classify(call):
    tool, cmd = call["tool"].lower(), call["input"]
    if tool == "skill" or re.search(r'(?:\bSKILL\.md\b|(?:^|\b)skills/[^"\s]+\.md\b)', cmd):
        return "skill"
    native = {"grep": "grep", "glob": "grep", "read": "read", "read_file": "read", "list_dir": "list"}
    if tool in native:
        return native[tool]
    if tool not in ("bash", "command_execution", "run_terminal_command"):
        return "other"
    cmd = unwrap(cmd).strip()
    if re.search(r"""\bobsidian\b["']?(?:\s+vault=(?:"[^"]*"|'[^']*'|\S+))?\s+(?:search|backlinks|links|tags?|read|files)\b""", cmd, re.I):
        return "obsidian"
    match = re.search(r"""(?:[\w./-]*qmd|\$\{?[\w]+\}?)["']?\s+(query|vsearch|search|get)\b""", cmd, re.I)
    if match:
        return {"search": "qmd_search", "get": "qmd_get"}.get(match[1].lower(), "qmd_query")
    # Match executables at command boundaries so a search term like "cat" stays a search.
    boundary = r"(?:^|[;&|(]\s*|\n\s*)(?:(?:command|env)\s+)?(?:/[\w./-]*/)?"
    if re.search(boundary + r"(?:grep|rg|ag|git\s+grep)\b|\bfind\b[^;&|]*\s-i?name\b", cmd):
        return "grep"
    if re.search(boundary + r"(?:cat|head|tail|less|bat|nl|sed\s+-n)\b", cmd):
        return "read"
    if re.search(boundary + r"(?:ls|tree)\b", cmd):
        return "list"
    return "other"


def write_json(path, data):
    """Publish complete JSON so resume never mistakes half a write for completion."""
    path = Path(path)
    with tempfile.NamedTemporaryFile(mode="w", dir=path.parent, delete=False) as tmp:
        try:
            json.dump(data, tmp, indent=2, ensure_ascii=False)
            tmp.write("\n")
            tmp.flush()
            os.replace(tmp.name, path)
        finally:
            Path(tmp.name).unlink(missing_ok=True)


def load_json(path):
    return json.loads(Path(path).read_text())


def artifact(base, suffix):
    return base.parent / (base.name + suffix)
