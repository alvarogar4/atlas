"""Checks for the retrieval-log hook: run `python3 -I scripts/retrieval-log-test.py`.

Feeds PostToolUse events from Claude Code, Codex and Grok to the real hook with a throwaway config
and log folder, and checks what lands in the log: the lookups, and never note text or foreign vaults.
"""
import json
import os
import stat
import subprocess
import tempfile
from pathlib import Path

HOOK = Path(__file__).resolve().parent / "retrieval-log.sh"


def run(tmp, events, enabled=True, read=True):
    brain = tmp / "brain"
    cfg = tmp / "atlas.env"
    cfg.write_text(f"ATLAS_BRAIN_PATH={brain}\nATLAS_QMD_CMD=/opt/q/qmd\n" + ("ATLAS_RETRIEVAL_LOG=1\n" if enabled else ""))
    env = dict(os.environ, ATLAS_CONFIG=str(cfg), XDG_STATE_HOME=str(tmp / "state"))
    for event in events:
        p = subprocess.run(["sh", str(HOOK)], input=json.dumps(event), env=env, capture_output=True, text=True, timeout=10)
        assert p.returncode == 0 and p.stdout == "" and p.stderr == "", p
    log = tmp / "state/atlas/retrieval-events.jsonl"
    if not read:
        return None
    return [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []


def bash(command, cwd="/tmp", **extra):
    return dict(session_id="s1", cwd=cwd, tool_name="Bash", tool_input=dict(command=command), **extra)


def main():
    with tempfile.TemporaryDirectory() as folder:
        tmp = Path(folder).resolve()
        b = tmp / "brain"
        (b / "inbox").mkdir(parents=True)
        (b / "inbox/a.md").write_text("note\n")
        assert run(tmp, [bash(f"grep -rn acme {b}")], enabled=False) == [], "off unless opted in"
        events = run(tmp, [
            bash(f"cd {b} && /opt/q/qmd query $'lex: acme price\\nvec: what acme pays' -n 5; sed -n 1,9p inbox/a.md"),
            bash(f"grep -rn 'ACME-4821' {b}", tool_response=dict(stdout="x\ny\n", returnCodeInterpretation="No matches found")),
            bash(f"cat > {b}/inbox/new.md <<'NOTE-END'\nsecret text\ncd {b} && qmd query 'secret phrase'\nNOTE-END"),
            bash("obsidian vault=other search query='other vault'"),
            bash("cd /tmp && qmd search 'other index'"),
            bash("ls; grep foo /etc/hosts; cat README.md"),
            bash("sed -n 1,5p inbox/a.md; rg -n acme areas/missing"),  # after a `cd` into the brain
            dict(session_id="s1", cwd=str(b), tool_name="Read", tool_input=dict(file_path=str(b / "inbox/a.md")),
                 agent_id="x", agent_type="general-purpose", duration_ms=4),
            dict(hookEventName="post_tool_use", sessionId="g1", cwd="/tmp", toolName="read_file",
                 toolInput=dict(target_file=str(b / "inbox/a.md"))),
            dict(session_id="c1", turn_id="t1", cwd=str(b), tool_name="Bash", tool_input=dict(command="rg -il acme ."),
                 tool_response=""),
        ])
        got = [(e["agent"], e["kind"], e.get("query"), e.get("paths")) for e in events]
        want = [
            ("claude", "qmd_query", "lex: acme price\nvec: what acme pays", None),
            ("claude", "read", None, ["inbox/a.md"]),
            ("claude", "grep", "ACME-4821", None),
            ("claude", "read", None, ["inbox/a.md"]),
            ("claude", "read", None, ["inbox/a.md"]),
            ("grok", "read", None, ["inbox/a.md"]),
            ("codex", "grep", "acme", None),
        ]
        assert got == want, got
        assert events[2]["exit"] == 1 and events[2]["hits"] == 2, events[2]
        assert events[4]["subagent"] == "general-purpose" and events[4]["duration_ms"] == 4, events[4]
        text = (tmp / "state/atlas/retrieval-events.jsonl").read_text()
        assert "secret" not in text and "other" not in text, "note text or a foreign vault was logged"
        mode = stat.S_IMODE((tmp / "state/atlas/retrieval-events.jsonl").stat().st_mode)
        assert mode == 0o600, oct(mode)
        log = tmp / "state/atlas/retrieval-events.jsonl"
        log.unlink()
        os.mkfifo(log)  # a FIFO with no reader must not stall the hook
        run(tmp, [bash(f"grep -rn acme {b}")], read=False)  # the 10 s timeout fails a stall
    print("retrieval-log ok")


if __name__ == "__main__":
    main()
