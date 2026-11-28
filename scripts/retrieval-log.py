"""Second half of the retrieval-log hook (started by retrieval-log.sh only when the user opted in).

Reads one PostToolUse event on stdin (Claude Code, Codex or Grok), and when the tool searched or
read the brain, appends one JSON line per search or read to the log. What goes in a line:
time, agent, session, tool, kind (qmd_query, qmd_search, grep, obsidian, read), the query or
pattern, brain-relative paths, exit status, hit count and duration when the agent gives them.
What never goes in: the command line (a heredoc can carry a whole note) or the tool's output.
"""
import json
import os
import re
import shlex
import stat
import sys
import time

QUERY_MAX = 300
SEARCHERS = {"grep", "egrep", "fgrep", "rg", "ag", "ack", "find", "fd"}
READERS = {"cat", "sed", "head", "tail", "less", "more", "bat", "nl", "awk", "wc"}
SEPARATORS = {"&&", "||", ";", "|", "&", "(", ")", "\n"}


def config(path: str) -> dict:
    values = {}
    with open(path, encoding="utf-8", errors="replace") as f:
        for line in f:
            m = re.match(r"\s*(ATLAS_\w+)=(.*)", line)
            if m:
                v = m.group(2).strip().strip("\"'")
                values[m.group(1)] = os.path.expanduser(v) if v.startswith("~/") else v
    return values


def agent_of(event: dict) -> str:
    if "hookEventName" in event or os.environ.get("GROK_HOOK_EVENT"):
        return "grok"
    if "turn_id" in event:
        return "codex"
    return "claude"


class Brain:
    def __init__(self, path: str, qmd: str, obsidian: str):
        self.root = os.path.realpath(path)
        self.spellings = sorted({path.rstrip("/"), self.root}, key=len, reverse=True)
        self.qmd = qmd
        self.obsidian = obsidian
        self.vaults = {os.path.basename(self.root), os.path.basename(path.rstrip("/"))}

    def rel(self, path: str, cwd: str):
        """Brain-relative path, or None when the path is outside the brain."""
        if path.startswith("qmd://"):
            return path  # mapped to a file by the report, which can ask QMD for the collection path
        full = os.path.realpath(os.path.join(cwd, os.path.expanduser(path)))
        if full == self.root or full.startswith(self.root + os.sep):
            return os.path.relpath(full, self.root)
        # Claude Code reports the session's folder, not the shell's after a `cd` into the brain:
        # a relative path that exists in the brain is taken as the brain's.
        if (path and not os.path.isabs(path) and not path.startswith(("~", ".."))
                and not os.path.exists(os.path.join(cwd, path))):
            inside = os.path.realpath(os.path.join(self.root, path))
            if inside.startswith(self.root + os.sep) and os.path.exists(inside):
                return os.path.relpath(inside, self.root)
        return None

    def mentioned(self, text: str) -> bool:
        return any(s and s in text for s in self.spellings)


def clip(text: str) -> str:
    return text if len(text) <= QUERY_MAX else text[:QUERY_MAX] + "..."


def words(command: str):
    """Shell words of a command, split into simple commands; nothing for a command with a heredoc.
    $'..' quoting becomes '..'."""
    if re.search(r"(?<!<)<<(?!<)", command):
        return  # a heredoc carries text (often a note being written): log nothing from it
    command = command.replace("$'", "'")
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()\n")
    lexer.whitespace = " \t\r"
    lexer.whitespace_split = True
    lexer.commenters = ""
    current = []
    for token in lexer:
        if token in SEPARATORS or set(token) <= set(";&|()\n"):
            if current:
                yield current
            current = []
        else:
            current.append(token)
    if current:
        yield current


def first_operand(args, takes_value=("-e", "-f", "-g", "-m", "-A", "-B", "-C", "-t", "--glob", "--type")):
    skip = False
    for i, a in enumerate(args):
        if skip:
            skip = False
            continue
        if a in ("-e", "--regexp") and i + 1 < len(args):
            return args[i + 1], args[i + 2:]
        if a.startswith("-"):
            skip = a in takes_value
            continue
        return a, args[i + 1:]
    return None, []


def shell_events(command: str, cwd: str, brain: Brain):
    events = []
    here = cwd
    try:
        commands = list(words(command))
    except ValueError:
        return events
    for argv in commands:
        while argv and re.match(r"^\w+=", argv[0]):
            argv = argv[1:]  # VAR=value prefixes
        if not argv:
            continue
        name = os.path.basename(argv[0])
        args = argv[1:]
        if name == "cd" and args:
            here = os.path.join(here, os.path.expanduser(args[0]))
            continue
        in_brain = brain.rel(here, "/") is not None
        # QMD and Obsidian can serve other vaults: count them only when they are the brain's.
        is_qmd = (brain.qmd and argv[0] == brain.qmd) or (in_brain and (
            name == "qmd" or re.match(r"^\$\{?\w+\}?$", argv[0])))
        if is_qmd and args and args[0] in ("query", "search", "vsearch", "get"):
            sub, rest = args[0], args[1:]
            operand, _ = first_operand(rest, ("-n", "-c", "--format", "--collection", "--min-score"))
            if sub == "get":
                if operand:
                    events.append({"kind": "read", "tool": "qmd", "paths": [operand]})
                continue
            kind = "qmd_search" if sub == "search" else "qmd_query"
            events.append({"kind": kind, "tool": "qmd", "query": clip((operand or "").replace("\\n", "\n"))})
            continue
        if (brain.obsidian and argv[0] == brain.obsidian) or name.lower() == "obsidian":
            sub = next((a for a in args if "=" not in a and not a.startswith("-")), "")
            opts = dict(a.split("=", 1) for a in args if "=" in a)
            if opts.get("vault") not in brain.vaults:
                continue
            if sub in ("search", "search:context", "backlinks", "links", "tags", "tag", "read", "files", "outline"):
                event = {"kind": "read" if sub == "read" else "obsidian", "tool": f"obsidian {sub}"}
                if opts.get("query") or opts.get("name"):
                    event["query"] = clip(opts.get("query") or opts.get("name"))
                if opts.get("path") or opts.get("file"):
                    event["paths"] = [p for p in [brain.rel(opts["path"], here) if opts.get("path") else opts["file"]] if p]
                events.append(event)
            continue
        if name == "git" and args[:1] == ["grep"]:
            name, args = "grep", args[1:]
        if name in SEARCHERS:
            pattern, rest = first_operand(args)
            if name in ("find", "fd"):
                names = [args[i + 1] for i, a in enumerate(args[:-1]) if a in ("-name", "-iname", "-path")]
                targets = [a for a in args if not a.startswith("-")][:1] if name == "find" else rest
                pattern = names[0] if names else (pattern if name == "fd" else None)
            else:
                targets = rest
            touched = in_brain if not targets else any(brain.rel(t, here) is not None for t in targets)
            if touched and pattern:
                events.append({"kind": "grep", "tool": name, "query": clip(pattern)})
            continue
        if name in READERS:
            if any(a.startswith(">") or a in ("-i", "--in-place") for a in args):
                continue  # writes a file (`cat > note.md`, `sed -i`): not a lookup
            paths = [brain.rel(a, here) for a in args if a.endswith(".md") and not a.startswith("-")]
            paths = [p for p in paths if p]
            if paths:
                events.append({"kind": "read", "tool": name, "paths": paths})
    return events


def tool_events(event: dict, brain: Brain):
    name = event.get("tool_name") or event.get("toolName") or ""
    data = event.get("tool_input") or event.get("toolInput") or {}
    cwd = event.get("cwd") or os.getcwd()
    if not isinstance(data, dict):
        return []
    if name in ("Bash", "run_terminal_command", "exec_command", "shell"):
        command = data.get("command") or data.get("cmd") or ""
        if isinstance(command, list):
            command = shlex.join(str(c) for c in command)
        cwd = data.get("cwd") or data.get("workdir") or cwd
        return shell_events(command, cwd, brain)
    if name in ("Read", "read_file"):
        path = brain.rel(data.get("file_path") or data.get("target_file") or "", cwd)
        return [{"kind": "read", "tool": name, "paths": [path]}] if path and path.endswith(".md") else []
    if name in ("Grep", "Glob", "grep"):
        where = data.get("path") or cwd
        if brain.rel(where, cwd) is None:
            return []
        return [{"kind": "grep", "tool": name, "query": clip(str(data.get("pattern") or ""))}]
    return []


def outcome(event: dict):
    """Exit code and number of output lines, when the agent reports them. Never the output itself."""
    response = event.get("tool_response")
    if response is None:
        response = event.get("toolResult")
    code, lines = None, None
    if isinstance(response, dict):
        code = response.get("exit_code", response.get("exitCode"))
        if response.get("returnCodeInterpretation") == "No matches found":
            code = 1
        out = response.get("stdout", response.get("output"))
        if isinstance(out, str):
            lines = len(out.splitlines())
    elif isinstance(response, str):
        m = re.search(r"(?:Exit code|exit_code|Process exited with code)[:\s]+(\d+)", response)
        code = int(m.group(1)) if m else None
    return code, lines


def append(record_lines) -> None:
    state = os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state")
    folder = os.path.join(state, "atlas")
    os.makedirs(folder, mode=0o700, exist_ok=True)
    path = os.path.join(folder, "retrieval-events.jsonl")
    # Non-blocking, and only a regular file: a FIFO or device there must not stall the agent.
    fd = os.open(path, os.O_WRONLY | os.O_APPEND | os.O_CREAT | os.O_NOFOLLOW | os.O_NONBLOCK, 0o600)
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode):
            return
        if os.fstat(fd).st_mode & 0o077:
            os.fchmod(fd, 0o600)
        os.write(fd, "".join(record_lines).encode())
    finally:
        os.close(fd)


def main(cfg_path: str) -> None:
    cfg = config(cfg_path)
    if not cfg.get("ATLAS_BRAIN_PATH") or not os.path.isdir(cfg["ATLAS_BRAIN_PATH"]):
        return
    event = json.load(sys.stdin)
    brain = Brain(cfg["ATLAS_BRAIN_PATH"], cfg.get("ATLAS_QMD_CMD", ""), cfg.get("ATLAS_OBSIDIAN_CMD", ""))
    found = tool_events(event, brain)
    if not found:
        return
    code, lines = outcome(event)
    base = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) + f".{int(time.time() * 1000) % 1000:03d}Z",
        "agent": agent_of(event),
        "session": event.get("session_id") or event.get("sessionId") or os.environ.get("GROK_SESSION_ID"),
        "tool_use_id": event.get("tool_use_id") or event.get("toolUseId"),
    }
    if event.get("agent_id"):
        base["subagent"] = event.get("agent_type") or True
    duration = event.get("duration_ms") or event.get("durationMs")
    out = []
    for i, e in enumerate(found):
        record = dict(base, seq=i, **e)
        if len(found) == 1:  # the agent reports one exit code and output for the whole command
            if code is not None:
                record["exit"] = code
            if lines is not None and e["kind"] != "read":
                record["hits"] = lines
        if duration is not None:
            record["duration_ms"] = duration
        out.append(json.dumps(record, ensure_ascii=False) + "\n")
    append(out)


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except Exception:  # a hook must never fail a tool call
        pass
