"""Run paired retrieval trials and unwind changes to the user's folders on exit."""
import argparse
import atexit
import concurrent.futures
import ctypes
import errno
import fcntl
import hashlib
import json
import logging
import os
from pathlib import Path
from itertools import count, islice
import re
import selectors
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
import tomllib
import uuid

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from agents import AGENTS, agent_env, artifact, command, load_json, parse, write_json

SMOKE = ('List every skill available to you whose name contains "brain", with the full path '
         'of its SKILL.md. Reply with the paths only, one per line.')
PLUGIN = "atlas@atlas-marketplace"
QUOTA = re.compile(rb"\b(?:http(?:[/ ]\d+(?:\.\d+)?)?\s*(?:error\s*|:\s*)?402|402\s+payment|insufficient|usage limit|rate limit|quota exceeded)\b", re.I)
LOG = logging.getLogger("retrieval")


def git(folder, *args):
    return subprocess.check_output(["git", "-C", str(folder), *map(str, args)]).decode().rstrip("\n")


def table_span(text, group, key):
    """Read TOML headers semantically so quoted keys survive a CLI rewrite."""
    headers = list(re.finditer(r"(?m)^[ \t]*\[.*?\][ \t]*(?:#[^\n]*)?(?:\n|$)", text))
    for i, header in enumerate(headers):
        try:
            parsed = tomllib.loads(header[0])
        except tomllib.TOMLDecodeError:
            continue
        if parsed.get(group) == {key: {}}:
            end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
            return header.start(), header.end(), end
    return None


def codex_config(text):
    header = f'[plugins."{PLUGIN}"]\n'
    span = table_span(text, "plugins", PLUGIN)
    if not span:
        return text.rstrip("\n") + "\n" + header + "enabled = false\n"
    _, start, end = span
    body = text[start:end]
    pattern = r'(?m)^([ \t]*(?:enabled|"enabled"|\'enabled\')[ \t]*=[ \t]*)(?:true|false)\b'
    body, n = re.subn(pattern, r"\g<1>false", body)
    if not n:
        body = "enabled = false\n" + body
    return text[:start].rstrip("\n") + "\n" + body + text[end:]


def prepare_codex(source, dest):
    dest.mkdir(mode=0o700)
    config = source / "config.toml"
    text = codex_config(config.read_text() if config.exists() else "")
    if tomllib.loads(text)["plugins"][PLUGIN].get("enabled") is not False:
        raise ValueError("Could not disable installed Atlas plugin")
    (dest / "config.toml").write_text(text)
    auth = source / "auth.json"
    if auth.is_file():
        shutil.copyfile(auth, dest / "auth.json")
        (dest / "auth.json").chmod(0o600)
    if (source / "AGENTS.md").is_file():
        (dest / "AGENTS.md").symlink_to(source / "AGENTS.md")


def trust(path, home, add, journal=None, created=False, stage=None):
    """Edit just our table in the latest file. Serialize harnesses sharing this folder."""
    if not path.parent.exists() and not add:
        return
    # A Grok installation owns this parent; creating it is also a reversible change.
    if not path.parent.exists():
        journal.add("mkdir", path=path.parent)
        path.parent.mkdir()
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        text = path.read_text() if path.exists() else ""
        span = table_span(text, "folders", str(home))
        if add:
            if span:
                if not tomllib.loads(text)["folders"][str(home)].get("trusted"):
                    raise ValueError(f"Grok trust already denied for {home}")
                return
            stage = ".retrieval-" + uuid.uuid4().hex
            journal.add("trust", path=path, home=home, created=not path.exists(), stage=stage)
            if text and not text.endswith("\n"):
                text += "\n"
            text += f'[folders.{json.dumps(str(home), ensure_ascii=False)}]\ntrusted = true\n'
            text += f"decided_at = {int(time.time())}\n"
        else:
            if stage:
                (path.parent / stage).unlink(missing_ok=True)
            if span:
                text = text[:span[0]] + text[span[2]:]
            if created and not text.strip():
                path.unlink(missing_ok=True)
                return
            if not span:
                return
        tmp = path.parent / (stage or (".retrieval-" + uuid.uuid4().hex))
        try:
            fd_tmp = os.open(tmp, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            with os.fdopen(fd_tmp, "w") as f:
                f.write(text)
            if path.exists():
                tmp.chmod(path.stat().st_mode & 0o777)
            tmp.replace(path)
        finally:
            tmp.unlink(missing_ok=True)
    finally:
        os.close(fd)


def exclusive_move(src, dst):
    """Publish without replacing a file or even an empty directory created during the run."""
    libc = ctypes.CDLL(None, use_errno=True)
    if sys.platform == "darwin":
        rc = libc.renamex_np(os.fsencode(src), os.fsencode(dst), 4)
    else:
        rc = libc.renameat2(-100, os.fsencode(src), -100, os.fsencode(dst), 1)
    if rc:
        code = ctypes.get_errno()
        raise OSError(code, os.strerror(code), str(dst))


def erase(path):
    if path.is_dir() and not path.is_symlink():
        shutil.rmtree(path)
    else:
        path.unlink(missing_ok=True)


def move(src, dst, staging, holding=None):
    """Across disks, take the note out of circulation before copying its contents."""
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        exclusive_move(src, dst)
    except OSError as exc:
        if exc.errno != errno.EXDEV:
            raise
        if holding:
            exclusive_move(src, holding)
            src = holding
        if src.is_dir() and not src.is_symlink():
            shutil.copytree(src, staging, symlinks=True)
        else:
            shutil.copy2(src, staging, follow_symlinks=False)
        exclusive_move(staging, dst)
        erase(src)


class Journal:
    def __init__(self, out):
        self.out = out
        self.path = out / "journal.json"
        self.entries = load_json(self.path) if self.path.exists() else []

    def add(self, action, **fields):
        self.entries.append(dict(action=action, **{k: str(v) if isinstance(v, Path) else v
                                                   for k, v in fields.items()}))
        write_json(self.path, self.entries)

    def undo(self):
        pending = []
        for entry in reversed(self.entries):
            try:
                self.undo_one(entry)
            except (OSError, subprocess.SubprocessError, ValueError) as exc:
                LOG.error("CLEANUP REQUIRED: %s: %s", entry, exc)
                pending.append(entry)
        self.entries = pending[::-1]
        write_json(self.path, self.entries)
        for home in self.out.glob("codexhome-*"):
            erase(home)
        return not pending

    def undo_one(self, e):
        action, path = e["action"], Path(e["path"])
        if action == "worktree":
            repo = Path(e["repo"])
            listed = git(repo, "worktree", "list", "--porcelain", "-z").split("\0")
            if f"worktree {path}" in listed:
                git(repo, "worktree", "remove", "--force", path)
            git(repo, "worktree", "prune")
        elif action == "trust":
            trust(path, Path(e["home"]), False, created=e["created"], stage=e.get("stage"))
        elif action == "mkdir":
            if path.is_dir() and not any(path.iterdir()):
                path.rmdir()
        elif action == "index":
            if os.path.lexists(e["saved"]):
                raise ValueError("Waiting for the hidden notes to be restored")
            git(path, "update-index", "--no-skip-worktree", "--", *e["files"])
        elif action == "hide":
            saved = Path(e["saved"])
            stage = e["stage"]
            if path.parent.resolve() != path.parent:
                raise ValueError(f"RESTORE CONFLICT: parent of {path} is now a symlink; kept {saved}")
            outbound = saved.with_name(stage)
            inbound = path.with_name(stage + "-return")
            holding = path.with_name(stage)
            erase(outbound)
            erase(inbound)
            if os.path.lexists(holding):
                if os.path.lexists(saved):
                    erase(holding)  # The complete copy was published before disposal started.
                elif os.path.lexists(path):
                    move(holding, saved, outbound)
                else:
                    exclusive_move(holding, path)
            if os.path.lexists(saved):
                if os.path.lexists(path):
                    raise FileExistsError(f"RESTORE CONFLICT: kept {saved}; {path} exists")
                move(saved, path, inbound)


def hide_paths(brain, out, paths, journal):
    unique = set()
    for name in paths:
        rel = Path(name)
        if rel.is_absolute() or ".." in rel.parts or ".git" in rel.parts or not rel.parts:
            raise ValueError(f"Expected a path below the brain: {name}")
        src = brain / rel
        if src.parent.resolve() != src.parent or not os.path.lexists(src):
            raise ValueError(f"Missing path or symlinked parent: {src}")
        unique.add(rel)
    for rel in sorted(unique):
        if any(p in unique for p in rel.parents):
            continue
        src, saved = brain / rel, out / "hidden" / rel
        if os.path.lexists(saved):
            raise FileExistsError(f"Hidden copy already exists: {saved}")
        if subprocess.run(["git", "-C", brain, "rev-parse", "--is-inside-work-tree"],
                          capture_output=True).returncode == 0:
            listing = git(brain, "--literal-pathspecs", "ls-files", "-v", "-z", "--", rel)
            files = [s[2:] for s in listing.split("\0") if s and s[0].upper() != "S"]
            if files:
                journal.add("index", path=brain, files=files, saved=saved)
                git(brain, "update-index", "--skip-worktree", "--", *files)
        stage = ".retrieval-" + uuid.uuid4().hex
        journal.add("hide", path=src, saved=saved, stage=stage)
        move(src, saved, saved.with_name(stage), holding=src.with_name(stage))


def config_env(brain, path, dest):
    lines = path.read_text().splitlines() if path.is_file() else []
    values = {}
    for line in lines:
        name, sep, value = line.strip().removeprefix("export ").partition("=")
        if sep:
            values[name] = value.strip().strip('"\'')
    live = values.get("ATLAS_BRAIN_PATH")
    text = "ATLAS_BRAIN_PATH=" + shlex.quote(str(brain)) + "\n"
    if live and Path(live).expanduser().resolve() == brain:
        for line in lines:
            if re.match(r"^(?:export )?ATLAS_(QMD_CMD|OBSIDIAN_CMD|QMD_REFRESH)=", line.strip()):
                text += line + "\n"
    dest.write_text(text)


def prepare_version(repo, out, name, sha, agents, source, trust_file, journal):
    version = out / "versions" / name
    if version.exists():
        if (not (version / ".git").is_file() or git(version, "rev-parse", "HEAD") != sha
                or f"worktree {version}" not in git(repo, "worktree", "list", "--porcelain", "-z").split("\0")):
            raise ValueError(f"Worktree does not match {name} at {sha}: {version}")
        journal.add("worktree", path=version, repo=repo)
    else:
        journal.add("worktree", path=version, repo=repo)
        git(repo, "worktree", "add", "--quiet", "--detach", version, sha)
    home = out / f"home-{name}"
    home.mkdir(exist_ok=True)
    git(home, "init", "-q")
    for folder in (home / ".agents/skills", home / ".grok/skills"):
        folder.mkdir(parents=True, exist_ok=True)
        for link in folder.iterdir():
            if link.is_symlink():
                link.unlink()
        for skill in sorted((version / "skills").iterdir()):
            if (skill / "SKILL.md").is_file():
                (folder / skill.name).symlink_to(skill)
    (home / ".grok/config.toml").write_text('[plugins]\ndisabled = ["atlas"]\n')
    if "codex" in agents:
        prepare_codex(source, out / f"codexhome-{name}")
    if "grok" in agents:
        trust(trust_file, home, True, journal)


def stop_group(proc):
    try:
        os.killpg(proc.pid, signal.SIGTERM)
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            proc.poll()
            try:
                os.killpg(proc.pid, 0)
            except PermissionError:
                # A sandbox may hide a vanished group. Still attempt escalation at the deadline.
                pass
            time.sleep(.05)
        os.killpg(proc.pid, signal.SIGKILL)
    except ProcessLookupError:
        pass
    except PermissionError:
        if proc.poll() is None:
            raise
    proc.wait()


def capture(argv, cwd, env, base, timeout, stop):
    """A silent child, partial line or grandchild holding stdout must still time out."""
    start = time.monotonic()
    expired = False
    rc = -1
    with artifact(base, ".jsonl").open("wb") as raw, artifact(base, ".times").open("w") as times, (
            artifact(base, ".stderr").open("wb")) as err:
        try:
            proc = subprocess.Popen(argv, cwd=cwd, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                    stderr=err, start_new_session=True)
        except OSError as exc:
            err.write((str(exc) + "\n").encode())
        else:
            with proc.stdout, selectors.DefaultSelector() as poll:
                try:
                    poll.register(proc.stdout, selectors.EVENT_READ)
                    pending = b""
                    while poll.get_map() or proc.poll() is None:
                        remaining = start + timeout - time.monotonic()
                        if stop.is_set() or remaining <= 0:
                            expired = True
                            stop_group(proc)
                            break
                        if not poll.select(min(.2, remaining)):
                            continue
                        chunk = os.read(proc.stdout.fileno(), 65536)
                        if not chunk:
                            poll.unregister(proc.stdout)
                            continue
                        offset = time.monotonic() - start
                        raw.write(chunk)
                        times.write(f"{offset:.2f}\n" * chunk.count(b"\n"))
                        raw.flush()
                        times.flush()
                        pending = chunk[-1:]
                    if pending and pending != b"\n":
                        times.write(f"{offset:.2f}\n")
                    rc = proc.wait()
                except BaseException:
                    stop_group(proc)
                    raise
    elapsed = time.monotonic() - start
    with artifact(base, ".stderr").open("rb") as err, artifact(base, ".jsonl").open("rb") as raw:
        quota = any(QUOTA.search(line) for stream in (err, raw) for line in stream)
    # Only a failed run can be a quota failure: notes and answers may mention rate limits.
    status = "timeout" if expired else "ok" if rc == 0 else "quota" if quota else "error"
    return dict(rc=rc, secs=round(elapsed, 2), status=status)


def smoke_ok(answer, version, home):
    paths = {p for p in re.findall(r"""(?:^|[\s(`"'])(/[^\n`"'<>]*?/SKILL\.md)(?=$|[\s)`"',.;])""", answer)
             if "brain" in p.lower()}
    if len(paths) != 1:
        return False
    path = Path(paths.pop())
    return path.is_file() and any(path.resolve().is_relative_to(root) for root in (version, home))


def trial(args, base, agent, name, case, rep, prompt, stop):
    version = args.out / "versions" / name
    home = args.out / f"home-{name}"
    env = agent_env(args.out)
    if agent == "codex":
        env["CODEX_HOME"] = str(args.out / f"codexhome-{name}")
    argv = command(agent, prompt, home, version, args.brain, args.model_opus)
    LOG.info("Starting %s", base.name)
    meta = dict(agent=agent, version=name, case=case, rep=rep)
    meta.update(capture(argv, home, env, base, args.timeout, stop))
    record = parse(agent, artifact(base, ".jsonl"), artifact(base, ".times"))
    write_json(artifact(base, ".record.json"), record)
    if case is None and meta["status"] == "ok" and not smoke_ok(record["answer"], version, home):
        meta["status"] = "error"
    write_json(artifact(base, ".meta.json"), meta)
    LOG.info("%s %s (%.2fs)", meta["status"].upper(), base.name, meta["secs"])
    return meta, record


def jobs(args, versions, cases, stop):
    failed_smoke = set()
    for agent in args.agents:
        for name in versions:
            if args.skip_smoke:
                continue
            base = args.out / "smoke" / f"{agent}-{name}"
            meta, record = trial(args, base, agent, name, None, 0, SMOKE, stop)
            if meta["status"] != "ok":
                failed_smoke.add((agent, name))
                LOG.error("SMOKE FAILED %s: %s", base.name, record["answer"] or "(empty answer)")

    def paired(agent, case, rep):
        for name in versions:
            if stop.is_set() or (agent, name) in failed_smoke:
                continue
            base = args.out / "runs" / f"{agent}-{name}-{case['id']}-r{rep}"
            path = artifact(base, ".meta.json")
            if path.exists():
                previous = load_json(path)
                if not args.retry_failed or previous["status"] == "ok":
                    continue
                path.unlink()
            prompt = (f"Atlas, {case['question']} My notes are the Atlas brain at {args.brain}. "
                      "Read-only: do not create, edit or delete any file, and do not commit. "
                      "Answer in at most 12 lines, citing the brain paths you used.")
            trial(args, base, agent, name, case["id"], rep, prompt, stop)

    with concurrent.futures.ThreadPoolExecutor(args.parallel) as pool:
        try:
            futures = [pool.submit(paired, agent, case, i + 1)
                       for agent in args.agents for case in cases for i in islice(count(), args.reps)]
            for future in concurrent.futures.as_completed(futures):
                future.result()
        finally:
            stop.set()
    return failed_smoke


def summary(args, versions, smoke):
    from collections import Counter
    rows = [(load_json(p), p) for p in sorted((args.out / "runs").glob("*.meta.json"))]
    LOG.info("Agent / version | ok | timeout | error | quota | smoke failed")
    for agent in args.agents:
        for name in versions:
            counts = Counter(m["status"] for m, _ in rows if (m["agent"], m["version"]) == (agent, name))
            LOG.info("%s / %s | %d | %d | %d | %d | %s", agent, name, counts["ok"], counts["timeout"],
                     counts["error"], counts["quota"], "YES" if (agent, name) in smoke else "-")
    for agent, name in sorted(smoke):
        p = args.out / "smoke" / f"{agent}-{name}.meta.json"
        rows.append((load_json(p), p))
    failed = False
    for meta, path in rows:
        if meta["status"] != "ok":
            failed = True
            stderr = path.with_name(path.name.removesuffix(".meta.json") + ".stderr")
            lines = stderr.read_text(errors="replace").splitlines() if stderr.exists() else []
            LOG.error("FAILED %s %s: %s", path.name, meta["status"], lines[-1] if lines else "(no stderr)")
    return int(failed)


def arguments():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--brain", type=Path)
    p.add_argument("--cases", type=Path)
    p.add_argument("--refs", nargs="+", metavar="NAME=REF", help="space- or comma-separated versions")
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent)
    p.add_argument("--agents", default="opus,codex,grok")
    p.add_argument("--reps", type=int, default=2)
    p.add_argument("--parallel", type=int, default=4)
    p.add_argument("--out", type=Path, required=True, help="dedicated output directory")
    p.add_argument("--only-cases", help="comma-separated case IDs")
    p.add_argument("--skip-smoke", action="store_true")
    p.add_argument("--hide", action="extend", nargs="+", default=[], metavar="BRAIN_PATH")
    p.add_argument("--model-opus", default="opus")
    p.add_argument("--timeout", type=float, default=900)
    p.add_argument("--retry-failed", action="store_true")
    p.add_argument("--cleanup", action="store_true")
    args = p.parse_args()
    args.out = args.out.expanduser().resolve()
    if not args.cleanup and not (args.refs and args.cases and args.brain):
        p.error("--brain, --cases and --refs are required for a run")
    if min(args.reps, args.parallel, args.timeout) <= 0:
        p.error("expected positive reps, parallel and timeout")
    args.agents = list(dict.fromkeys(args.agents.split(",")))
    if set(args.agents) - set(AGENTS):
        p.error("unknown agent")
    return args


def execute(args, journal, stop):
    args.repo = Path(git(args.repo, "rev-parse", "--show-toplevel")).resolve()
    given_brain = args.brain.expanduser().absolute()
    given_cases = args.cases.expanduser().absolute()
    args.brain, args.cases = given_brain.resolve(), given_cases.resolve()
    if not args.brain.is_dir() or args.out.is_relative_to(args.brain):
        raise ValueError("Use an existing brain and keep --out outside it")
    versions = {}
    for pair in ",".join(args.refs).split(","):
        name, ref = pair.split("=", 1)
        if not re.fullmatch(r"[\w][\w.-]*", name) or name in versions:
            raise ValueError(f"Invalid or duplicate version name: {name}")
        versions[name] = git(args.repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}")
    cases = load_json(args.cases)["cases"]
    ids = [c["id"] for c in cases]
    if len(set(ids)) != len(ids) or any(not re.fullmatch(r"[\w][\w.-]*", i) for i in ids):
        raise ValueError("Use unique case IDs made of letters, digits, dots, dashes or underscores")
    stems = {f"{v}-{i}" for v in versions for i in ids}
    if len(stems) != len(versions) * len(ids):
        raise ValueError("Version and case names produce duplicate run filenames")
    if args.only_cases:
        wanted = set(args.only_cases.split(","))
        if wanted - set(ids):
            raise ValueError(f"Unknown cases: {wanted - set(ids)}")
        cases = [c for c in cases if c["id"] in wanted]
    for key, root in ((given_cases, given_brain), (args.cases, args.brain)):
        if key.is_relative_to(root):
            folder = key.parent.relative_to(root)
            if not folder.parts:
                raise ValueError("Keep the cases file in a subfolder; hiding its parent would hide the whole brain")
            # A symlinked directory can expose a key whose target lives outside the vault.
            rel = Path()
            for part in folder.parts:
                rel /= part
                if (args.brain / rel).is_symlink():
                    break
            args.hide.append(str(rel))
    args.hide = sorted(set(args.hide))
    cfg = {k: str(v) if isinstance(v, Path) else v for k, v in vars(args).items()}
    cfg["cases_sha256"] = hashlib.sha256(args.cases.read_bytes()).hexdigest()
    vp, rp = args.out / "versions.json", args.out / "run.json"
    if vp.exists() and load_json(vp) != versions:
        raise ValueError("Version commits changed; use a fresh --out")
    if rp.exists():
        old = load_json(rp)
        if any(k in old and old[k] != cfg[k] for k in ("brain", "cases_sha256", "model_opus", "hide")):
            raise ValueError("Experiment inputs changed; use a fresh --out")
    write_json(rp, cfg)
    write_json(vp, versions)
    for folder in ("versions", "smoke", "runs"):
        (args.out / folder).mkdir(exist_ok=True)
    config_env(args.brain, Path(os.environ.get("ATLAS_CONFIG", Path.home() / ".config/atlas/.env")),
               args.out / "atlas.env")
    for name, sha in versions.items():
        prepare_version(args.repo, args.out, name, sha, args.agents,
                        Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser().resolve(),
                        Path.home() / ".grok/trusted_folders.toml", journal)
    hide_paths(args.brain, args.out, args.hide, journal)
    return summary(args, versions, jobs(args, versions, cases, stop))


def main():
    args = arguments()
    args.out.mkdir(mode=0o700, parents=True, exist_ok=True)
    logging.basicConfig(level=logging.INFO, format="%(message)s",
                        handlers=[logging.StreamHandler(), logging.FileHandler(args.out / "progress.log")])
    with (args.out / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        journal = Journal(args.out)
        stop = threading.Event()

        def interrupt(sig, frame):
            stop.set()
            raise KeyboardInterrupt

        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, interrupt)
        atexit.register(journal.undo)
        try:
            if not journal.undo():
                return 1
            if args.cleanup:
                return 0
            return execute(args, journal, stop)
        finally:
            for sig in (signal.SIGINT, signal.SIGTERM):
                signal.signal(sig, signal.SIG_IGN)
            clean = journal.undo()
            atexit.unregister(journal.undo)
            if not clean:
                raise RuntimeError("Cleanup incomplete; resolve the reported conflict and run --cleanup")


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, OSError, RuntimeError, subprocess.SubprocessError, KeyboardInterrupt) as exc:
        sys.exit(f"Run stopped: {exc}")
