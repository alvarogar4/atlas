"""Exercise the full scorer and recovery paths using invented streams and local Git objects."""
import errno
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import threading
import time
import tomllib
from unittest.mock import patch

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import agents
import run
import score

FIX = HERE / "fixtures"
BRAIN = Path("/fixture/brain")
checks = 0


def check(actual, expected, label):
    global checks
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")
    checks += 1


def scoring(tmp):
    out = tmp / "scoring"
    shutil.copytree(FIX / "recorded", out)
    cases = {c["id"]: c for c in agents.load_json(FIX / "cases.json")["cases"]}
    rows, failed = score.read_runs(out, cases, BRAIN)
    check([(m["agent"], m["version"], m["case"], m["status"]) for m in failed],
          [("codex", "pr", "c03", "quota")], "failed trial")
    # In order: citations, surfaced, current, stale, superseded, calls, first hit index/time,
    # first open index/time, wasted note count, first search tool.
    stale = (0, 0, 0, True, True, 1, None, None, None, None, 0, None)
    direct = (1, 1, 1, False, False, 1, 1, 2.5, 1, 2.5, 0, None)
    felt = (1, 1, None, False, False, 1, 1, 2.5, 1, 2.5, 0, None)
    exact = (1, 1, None, False, False, 1, 1, 1.4, None, None, 0, "grep")
    one = (1/3, 1/3, None, False, False, 1, 1, 2.5, 1, 2.5, 0, None)
    only = (1, 1, 1, False, False, 1, 1, 1.4, None, None, 0, "grep")
    expected = {
        "opus": [
            (stale, (1, 1, 1, False, False, 2, 1, 1.4, 2, 2.5, 0, "qmd_query")),
            ((1, 1, 0, True, False, 1, 1, 1.4, None, None, 0, "grep"), only),
            (felt, felt), (one, exact)],
        "codex": [
            (stale, (1, 1, 1, False, False, 3, 2, 1.4, 3, 2.5, 0, "grep")),
            (direct, (1, 1, 1, False, False, 2, 2, 1.4, None, None, 1, "grep")),
            (exact, None), (exact, one)],
        "grok": [
            (stale, (1, 1, 1, False, False, 2, 1, 1.4, 2, 2.5, 0, "grep")),
            (direct, direct),
            (felt, (1, 1, None, False, False, 1, 1, .9, None, None, 0, "grep")), (exact, exact)]}
    fields = ("found", "surfaced", "latest", "stale_only", "superseded_only", "calls",
              "calls_to_relevant", "secs_to_relevant", "opened_calls", "opened_secs", "waste", "first_search")
    by_id = {(r["agent"], r["case"], r["version"]): r for r in rows}
    check(len(rows), 23, "successful trials")
    for agent, trials in expected.items():
        for i, pair in enumerate(trials, 1):
            for v, exp in zip(("main", "pr"), pair):
                key = agent, f"c{i:02}", v
                if exp is None:
                    check(key in by_id, False, "quota excluded")
                    continue
                m = by_id[key]["metrics"]
                for field, value in zip(fields, exp, strict=True):
                    check(m[field], value, f"{key} {field}")
                check(m["usage"]["input_tokens"], {"opus":110, "codex":100, "grok":103}[agent], "input tokens")
                check(m["usage"]["output_tokens"], {"opus":21, "codex":22, "grok":24}[agent], "output tokens")
                check(m["cost_usd"], .31 if agent == "opus" else None, "cost")
    def trial(agent, case):
        return by_id[agent, case, "pr"]
    check(trial("codex", "c01")["metrics"]["research"], 1, "repeat search")
    check(trial("opus", "c01")["metrics"]["counts"], {"skill":1, "qmd_query":1, "qmd_get":1}, "tool mix")
    check(trial("codex", "c02")["metrics"]["wasted_notes"], ["resources/ink-mix.md"], "wasted path")
    call = trial("codex", "c01")["record"]["calls"][0]
    check((call["exit_code"], call["error"], call["input"], call["t"]),
          (1, False, "rg -l missing-brass /fixture/brain", .5), "deduplicated start and no-match")
    rec = trial("grok", "c01")["record"]
    check(rec["calls"][0]["output"], "/fixture/brain/areas/log/2030-03-11.md", "decoded byte list")
    check(rec["answer"], "Both screens run v2.1.4. areas/log/2030-03-11.md", "final chunks only")
    check(all(r["record"]["session_ok"] for r in rows), True, "session completion")
    matched = list(score.pairs(rows, "main", "pr"))
    for agent, totals in [("opus", (0,3,1,.25)), ("codex", (1,2,0,1)), ("grok", (0,2,2,.5))]:
        check(score.tally(p for p in matched if p[0]["agent"] == agent), totals, agent + " pairs")
    check(score.tally(matched), (1, 7, 3, .0703125), "overall pairs")
    check(score.sign_test(13, 7), .26317596435546875, "small sample")
    cmd = [sys.executable, "-I", HERE / "score.py", "--out", out, "--cases", FIX / "cases.json",
           "--brain", BRAIN, "--report", tmp / "copy.md"]
    report = subprocess.check_output(cmd, text=True)
    check(report, (out / "report.md").read_text(), "report stdout")
    check(report, (tmp / "copy.md").read_text(), "second report")
    check("| codex | pr | c03 | 1 | quota |" in report, True, "quota row visible")
    check("| main | pr | Overall | 1 | 7 | 3 | 0.0703125 |" in report, True, "paired report")
    check(all(s in report for s in ("2030-03-14", "1 FAILED", "## Cases", "## Flags", "superseded_only")), True, "sections")
    check(subprocess.check_output(cmd + ["--reparse"], text=True), report, "cache and reparse agree")


def classification():
    examples = {
        "qmd_query": ["pier-qmd query wool", '"/opt/pier-qmd" vsearch lamp', '"$QMD" query bell'],
        "qmd_search": ["$Q search 'blue card'"], "qmd_get": ["qmd get resources/pin.md"],
        "grep": ["grep -rl fee .", "rg -F ACME-4821", "ag bell", "git grep felt", "find . -name '*.md'"],
        "obsidian": ['Obsidian vault="Pier loft" backlinks path=pin.md', "obsidian search blue",
                     "obsidian links", "obsidian tags", "obsidian tag", "obsidian read", "obsidian files"],
        "read": ["cat areas/a.md", "sed -n '2p' x.md", "head a.md", "tail b.md", "less a.md", "bat b.md",
                 "nl a.md", """ /bin/bash -lc "cat a.md" """],
        "list": ["ls -al", "tree areas"],
        "skill": ["cat /tmp/skills/recall/SKILL.md", "head skills/lookup/reference/notes.md"],
        "other": ["pwd", "echo 'cat'"]}
    for kind, cmds in examples.items():
        for cmd in cmds:
            check(agents.classify(dict(tool="Bash", input=cmd)), kind, cmd)
    for tool, kind in [("Skill","skill"), ("Read","read"), ("Glob","grep"), ("Grep","grep"),
                       ("read_file","read"), ("list_dir","list"), ("grep","grep"), ("Task","other")]:
        check(agents.classify(dict(tool=tool, input="{}")), kind, tool)
    check(agents.unwrap('/bin/bash -lc "cat a.md"'), "cat a.md", "double quote wrapper")
    check(score.normalize("[ink](/fixture/brain/resources/ink.md)", BRAIN), "[ink](resources/ink)", "normalization")
    check(score.matches("areas/log/", "areas/log/a"), True, "folder with note")
    check(score.matches("areas/log/", "areas/log/"), False, "bare folder")
    check(list(score.opened_notes(dict(tool="Bash", input="cat '/fixture/brain/a b.md' /tmp/no.md"), BRAIN)),
          ["a b.md"], "quoted brain note")


def config_checks(tmp):
    source, dest = tmp / "source", tmp / "sandbox"
    source.mkdir()
    for text in ('[plugins."other"]\nenabled = true\n', "",
                 '[plugins."atlas@atlas-marketplace"]\nenabled = true # on\n[plugins.other]\nenabled = true\n'):
        parsed = tomllib.loads(run.codex_config(text))
        check(parsed["plugins"][run.PLUGIN]["enabled"], False, "disabled installed plugin")
        if "other" in text:
            check(parsed["plugins"]["other"]["enabled"], True, "neighbor plugin")
    (source / "auth.json").write_text('{"sample":true}')
    (source / "AGENTS.md").write_text("Fixture instructions.")
    run.prepare_codex(source, dest)
    check((dest / "auth.json").stat().st_mode & 0o777, 0o600, "credential mode")
    check((dest / "AGENTS.md").resolve(), source / "AGENTS.md", "instructions link")
    live = tmp / "live"
    cfg = tmp / "atlas.env"
    live.write_text(f'ATLAS_BRAIN_PATH="{tmp}"\nATLAS_QMD_CMD=/bin/pier-qmd\nATLAS_OBSIDIAN_CMD=obsidian\n'
                    'ATLAS_QMD_REFRESH=1\nATLAS_RETRIEVAL_LOG=/tmp/private\n')
    run.config_env(tmp, live, cfg)
    check(cfg.read_text().splitlines()[1:], ["ATLAS_QMD_CMD=/bin/pier-qmd", "ATLAS_OBSIDIAN_CMD=obsidian",
                                             "ATLAS_QMD_REFRESH=1"], "live brain config")
    run.config_env(BRAIN, live, cfg)
    check(cfg.read_text(), "ATLAS_BRAIN_PATH=/fixture/brain\n", "fixture config")


def seed_repo(folder):
    """Make a disposable revision without reading Git identity, hooks or network config."""
    folder.mkdir()
    run.git(folder, "init", "-q")
    path = folder / "skills/second-brain/SKILL.md"
    path.parent.mkdir(parents=True)
    path.write_text("# Fixture skill\n")
    run.git(folder, "add", "--", "skills")
    tree = run.git(folder, "write-tree")
    author = "Fixture <fixture@example.invalid> 1000000000 +0000"
    obj = f"tree {tree}\nauthor {author}\ncommitter {author}\n\nFixture\n"
    sha = subprocess.check_output(["git", "-C", folder, "hash-object", "-t", "commit", "-w", "--stdin"],
                                  input=obj, text=True).strip()
    run.git(folder, "update-ref", "HEAD", sha)
    return sha


def recovery(tmp):
    out = tmp / "output"
    out.mkdir()
    journal = run.Journal(out)
    home = tmp / "test folder"
    path = tmp / "trust.toml"
    first = '[folders."/tmp/other"]\ntrusted = true\n'
    later = '[folders."/tmp/later"]\ntrusted = true\n'
    for rewritten in (False, True):
        path.write_text(first)
        run.trust(path, home, True, journal)
        check(tomllib.loads(path.read_text())["folders"][str(home)]["trusted"], True, "added trust")
        if rewritten:
            path.write_text(f"[folders.'{home}']\ntrusted=true\ndecided_at=3\n" + later + first)
        else:
            with path.open("a") as f:
                f.write(later)
        run.Journal(out).undo()
        journal = run.Journal(out)
        check(tomllib.loads(path.read_text()), tomllib.loads(first + later), "preserve other trust decisions")
        check(journal.undo(), True, "repeat trust removal")
    repo = tmp / "repo"
    sha = seed_repo(repo)
    (out / "versions").mkdir()
    run.prepare_version(repo, out, "pr", sha, ["opus"], tmp / "unused", path, journal)
    version = out / "versions/pr"
    linked = out / "home-pr/.agents/skills/second-brain/SKILL.md"
    check(run.smoke_ok(str(linked), version, out / "home-pr"), True, "isolated skill")
    check(run.smoke_ok(str(repo / "skills/second-brain/SKILL.md"), version, out / "home-pr"), False, "leaked skill")
    check(run.smoke_ok(str(linked) + "\n" + str(repo / "skills/second-brain/SKILL.md"), version, home), False, "two skills")
    brain = tmp / "brain"
    brain.mkdir()
    run.git(brain, "init", "-q")
    private = brain / "keys"
    private.mkdir()
    (private / "gold.md").write_text("original")
    (private / "skip.md").write_text("keep index bit")
    run.git(brain, "add", "keys")
    run.git(brain, "update-index", "--skip-worktree", "--", "keys/skip.md")
    run.hide_paths(brain, out, ["keys", "keys/gold.md"], journal)
    check(os.path.lexists(private), False, "hidden subtree")
    check(run.git(brain, "ls-files", "-v").splitlines(), ["S keys/gold.md", "S keys/skip.md"], "hidden index")
    (out / "codexhome-main").mkdir()
    for _ in (1, 2):
        check(run.Journal(out).undo(), True, "replay journal")
        check((private / "gold.md").read_text(), "original", "restored subtree")
        check(run.git(brain, "ls-files", "-v").splitlines(), ["H keys/gold.md", "S keys/skip.md"], "restore index bits")
        check((out / "codexhome-main").exists() or version.exists(), False, "transient state removed")
        check(str(version) in run.git(repo, "worktree", "list", "--porcelain"), False, "Git registration removed")
    journal = run.Journal(out)
    journal.add("worktree", path=version, repo=repo)
    journal.add("trust", path=path, home=home, created=False)
    journal.add("hide", path=private, saved=out / "hidden/keys", stage=".test-stage")
    check(journal.undo(), True, "crash before mutation")
    run.hide_paths(brain, out, ["keys/gold.md"], journal)
    gold = private / "gold.md"
    gold.write_text("new")
    with patch.object(run.LOG, "error") as warn:
        check(journal.undo(), False, "conflict retained")
        check(warn.called, True, "conflict warning")
    check(gold.read_text(), "new", "preserve replacement")
    check((out / "hidden/keys/gold.md").read_text(), "original", "preserve hidden copy")
    gold.unlink()
    check(journal.undo(), True, "resolve conflict")
    check(gold.read_text(), "original", "recovered after conflict")
    # Simulate two devices and a crash after taking ownership, before publishing the copy.
    rename = run.exclusive_move
    def two_disks(src, dst):
        if src.is_relative_to(brain) != dst.is_relative_to(brain):
            raise OSError(errno.EXDEV, "cross-device move")
        rename(src, dst)
    with patch.object(run, "exclusive_move", two_disks):
        with patch.object(shutil, "copy2", side_effect=InterruptedError("interrupted copy")):
            try:
                run.hide_paths(brain, out, ["keys/gold.md"], journal)
            except InterruptedError:
                pass
        check(gold.exists(), False, "original held during copy")
        gold.write_text("replacement")
        with patch.object(run.LOG, "error"):
            check(run.Journal(out).undo(), False, "conflict during cross-device copy")
        check((out / "hidden/keys/gold.md").read_text(), "original", "complete cross-device backup")
        check(gold.read_text(), "replacement", "preserve concurrent replacement")
        gold.unlink()
        check(run.Journal(out).undo(), True, "cross-device replay")
        check(gold.read_text(), "original", "cross-device restore")


def capture_checks(tmp):
    stop = threading.Event()
    def capture(name, script, timeout=3):
        return run.capture([sys.executable, "-I", "-c", script], tmp, os.environ, tmp / name, timeout, stop)
    result = capture("timed", 'import time; print("one", flush=True); time.sleep(.12); print("two", end="")')
    check(result["status"], "ok", "process completion")
    check((tmp / "timed.jsonl").read_text(), "one\ntwo", "preserve raw lines")
    offsets = (tmp / "timed.times").read_text().splitlines()
    check(len(offsets), 2, "offset count")
    check(float(offsets[1]) - float(offsets[0]) >= .08, True, "arrival offsets")
    result = capture("silent", "import time; time.sleep(30)", .2)
    check(result["status"], "timeout", "silent child")
    check(result["rc"], -signal.SIGTERM, "terminate process group")
    check(capture("quota", 'import sys; sys.exit("HTTP 402: insufficient funds")')["status"], "quota", "quota status")
    check(capture("bad", 'raise SystemExit(7)')["status"], "error", "nonzero exit")


def runner_cli(tmp):
    """Drive real CLI setup, smoke, jobs and finally with a local stream emitter."""
    repo, brain = tmp / "repo", tmp / "brain"
    private, out = brain / "private", tmp / "live-out"
    private.mkdir()
    cases = private / "cases.json"
    shutil.copyfile(FIX / "cases.json", cases)
    gate = tmp / "simulate-failure"
    gate.touch()
    emitter = tmp / "emit.py"
    emitter.write_text("""import json, os, sys
from pathlib import Path
prompt, version, brain, gate, config = sys.argv[1:]
assert not (Path(brain) / "private").exists()
assert os.environ["ATLAS_CONFIG"] == config and "ATLAS_RETRIEVAL_LOG" not in os.environ
assert sys.stdin.read() == ""
answer = "Both screens run v2.1.4. areas/log/2030-03-11.md"
if prompt.startswith("Load each skill"):
    answer = str(Path.cwd() / ".agents/skills/second-brain/SKILL.md")
    if Path(gate).exists() and version == "pr":
        answer = "/tmp/foreign/second-brain/SKILL.md"
elif Path(gate).exists() and "weekly skiff" in prompt:
    sys.exit("usage limit")
print(json.dumps(dict(type="result", result=answer, usage={}, total_cost_usd=0)))
""")
    shim = """import sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, sys.argv.pop(1))
import run
emitter, gate = sys.argv[1:3]
del sys.argv[1:3]
def local(agent, prompt, home, version, brain, model):
    return [sys.executable, "-I", emitter, prompt, version.name, str(brain), gate, str(home.parent / "atlas.env")]
run.command = local
sys.exit(run.main())
"""
    cmd = [sys.executable, "-I", "-c", shim, HERE, emitter, gate, "--repo", repo, "--brain", brain,
           "--cases", cases, "--refs", "main=HEAD", "pr=HEAD", "--agents", "opus", "--only-cases",
           "c01,c02", "--reps", "1", "--parallel", "2", "--out", out.relative_to(tmp)]
    env = dict(os.environ, ATLAS_CONFIG=str(tmp / "unused-config"), ATLAS_RETRIEVAL_LOG="unused")
    for attempt, (extra, rc, total, starts) in enumerate([
            ([], 1, 2, 4), ([], 1, 4, 4), (["--retry-failed"], 0, 4, 3)]):
        result = subprocess.run(cmd + extra, cwd=tmp, env=env, capture_output=True, text=True)
        check(result.returncode, rc, result.stderr)
        check(result.stderr.count("Starting "), starts, "smoke, resume and retry")
        check(len(list((out / "runs").glob("*.meta.json"))), total, "case metadata count")
        check(cases.is_file(), True, "answer key restored")
        check(agents.load_json(out / "journal.json"), [], "normal CLI cleanup")
        if attempt == 0:
            check("SMOKE FAILED opus-pr" in result.stderr and "FAILED opus-main-c02-r1" in result.stderr,
                  True, "failure summary")
            gate.unlink()
    check(subprocess.run([sys.executable, "-I", HERE / "run.py", "--out", out, "--cleanup"],
                         cwd=tmp, env=env, capture_output=True).returncode, 0, "cleanup CLI")
    emitter.write_text("from pathlib import Path\nimport time\nPath('ready').touch()\ntime.sleep(60)\n")
    interrupted = tmp / "interrupted"
    with subprocess.Popen(cmd + ["--out", interrupted, "--skip-smoke", "--only-cases", "c01"],
                          cwd=tmp, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE) as proc:
        try:
            until = time.monotonic() + 10
            while not (interrupted / "home-main/ready").exists():
                if proc.poll() is not None or time.monotonic() > until:
                    raise AssertionError("Trial did not reach the interruption point")
                time.sleep(.02)
            check(cases.exists(), False, "private cases hidden before signal")
            proc.terminate()
            _, err = proc.communicate(timeout=15)
            check(proc.returncode != 0, True, err.decode())
        finally:
            if proc.poll() is None:
                proc.kill()
    check(cases.is_file(), True, "SIGTERM restores cases")
    check(agents.load_json(interrupted / "journal.json"), [], "SIGTERM replays journal")
    check(str(interrupted) in run.git(repo, "worktree", "list", "--porcelain"), False, "SIGTERM removes worktrees")


def killed_run(tmp):
    """A run killed with SIGKILL is undone by the next run, whatever --out that one uses."""
    dead = tmp / "killed-out"
    dead.mkdir()
    trust_file = tmp / "killed-trust.toml"
    trust_file.write_text('[folders."/tmp/other"]\ntrusted = true\n')
    home = tmp / "killed-home"
    run.trust(trust_file, home, True, run.Journal(dead))
    (dead / "codexhome-main").mkdir()
    (dead / "codexhome-main/auth.json").write_text("{}")
    agents.write_json(run.registry() / "dead.json", dict(out=str(dead)))
    result = subprocess.run([sys.executable, "-I", HERE / "run.py", "--out", tmp / "fresh-out", "--cleanup"],
                            cwd=tmp, env=dict(os.environ), capture_output=True, text=True)
    check(result.returncode, 0, result.stderr)
    check(str(home) in trust_file.read_text(), False, "killed run: Grok trust removed")
    check((dead / "codexhome-main").exists(), False, "killed run: credentials deleted")
    check(list(run.registry().glob("*.json")), [], "killed run: registry emptied")


def main():
    classification()
    with tempfile.TemporaryDirectory() as folder, patch.dict(os.environ, {
            "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1"}):
        tmp = Path(folder).resolve()
        os.environ["XDG_STATE_HOME"] = str(tmp / "state")
        scoring(tmp)
        config_checks(tmp)
        recovery(tmp)
        capture_checks(tmp)
        runner_cli(tmp)
        killed_run(tmp)
    print(f"selftest ok ({checks} checks)")


if __name__ == "__main__":
    main()
