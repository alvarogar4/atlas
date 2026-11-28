"""Report on how agents find notes in real sessions, from the retrieval-log hook's log.

    python3 -I scripts/retrieval-report.py [--days 7] [--agent codex] [--check-newer]

Per day (local time) and agent: sessions that searched or read the brain, searches per session,
the first search tool, searches and seconds until the first note read, and the re-search rate
(a search that follows another search with no note read in between).

--check-newer reruns logged queries through QMD (read-only `query` and `search`, top 10, at most
--max-queries of them, --delay seconds apart) and flags a "missed newer note": the session read
a note from those results, and a newer note on the same topic (ranked above a note the session
read, or in the same folder as one; dated by frontmatter updated, modified or created, else the
file's modification time) was never read in that session.
"""
import argparse
import collections
import datetime as dt
import json
import os
import re
import statistics
import subprocess
import sys
import time

SEARCH = ("qmd_query", "qmd_search", "grep", "obsidian")


def config() -> dict:
    path = os.environ.get("ATLAS_CONFIG") or os.path.expanduser("~/.config/atlas/.env")
    values = {}
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = re.match(r"\s*(ATLAS_\w+)=(.*)", line)
                if m:
                    v = m.group(2).strip().strip("\"'")
                    values[m.group(1)] = os.path.expanduser(v) if v.startswith("~/") else v
    except OSError:
        pass
    return values


def load(path: str, since: dt.date, agent: str):
    events = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            try:
                e = json.loads(line)
                when = dt.datetime.strptime(e["ts"][:23], "%Y-%m-%dT%H:%M:%S.%f").replace(tzinfo=dt.timezone.utc)
            except (ValueError, KeyError):
                continue
            e["when"] = when.astimezone()
            if e["when"].date() >= since and (not agent or e.get("agent") == agent):
                events.append(e)
    events.sort(key=lambda e: (e["when"], e.get("seq", 0)))
    return events


def sessions_of(events):
    by = collections.OrderedDict()
    for e in events:
        by.setdefault((e.get("agent"), e.get("session")), []).append(e)
    return by


def session_stats(evs):
    searches = [e for e in evs if e["kind"] in SEARCH]
    reads = [e for e in evs if e["kind"] == "read"]
    first_read = reads[0] if reads else None
    before = [e for e in searches if first_read is None or e["when"] <= first_read["when"]]
    research = 0
    last = None
    for e in evs:
        if e["kind"] in SEARCH and last in SEARCH:
            research += 1
        last = e["kind"]
    return {
        "day": evs[0]["when"].date().isoformat(),
        "searches": len(searches),
        "first": searches[0]["kind"] if searches else "(read only)",
        "to_read_searches": len(before) if first_read else None,
        "to_read_secs": (first_read["when"] - evs[0]["when"]).total_seconds() if first_read else None,
        "research": research,
    }


def med(xs):
    xs = [x for x in xs if x is not None]
    return f"{statistics.median(xs):.1f}" if xs else "-"


def table(rows):
    groups = collections.OrderedDict()
    for s in rows:
        groups.setdefault((s["day"], s["agent"]), []).append(s)
    out = ["| Day | Agent | Sessions | Searches/session | First tool | Searches to first read | Secs to first read | Re-search rate | No read |",
           "| --- | --- | --- | --- | --- | --- | --- | --- | --- |"]
    for (day, agent), ss in sorted(groups.items()):
        firsts = collections.Counter(s["first"] for s in ss)
        first = ", ".join(f"{k} {100 * v // len(ss)}%" for k, v in firsts.most_common())
        searches = sum(s["searches"] for s in ss)
        rate = f"{100 * sum(s['research'] for s in ss) / searches:.0f}%" if searches else "-"
        no_read = sum(s["to_read_secs"] is None for s in ss)
        out.append(f"| {day} | {agent} | {len(ss)} | {med([s['searches'] for s in ss])} | {first} | "
                   f"{med([s['to_read_searches'] for s in ss])} | {med([s['to_read_secs'] for s in ss])} | {rate} | {no_read} |")
    return "\n".join(out)


class Qmd:
    """Read-only QMD calls, run from the brain folder like Atlas does."""

    def __init__(self, cmd: str, brain: str, delay: float):
        self.cmd, self.brain, self.delay = cmd, os.path.realpath(brain), delay
        self.roots = {}

    def run(self, args):
        time.sleep(self.delay)
        p = subprocess.run([self.cmd] + args, cwd=self.brain, stdin=subprocess.DEVNULL,
                           capture_output=True, text=True, timeout=120, check=False)
        return p.stdout if p.returncode == 0 else ""

    def to_rel(self, uri: str):
        """qmd://<collection>/<path> -> brain-relative path, or None outside the brain."""
        m = re.match(r"qmd://([^/]+)/(.+)", uri)
        if not m:
            return uri
        name, rest = m.groups()
        if name not in self.roots:
            out = subprocess.run([self.cmd, "collection", "show", name], cwd=self.brain, capture_output=True,
                                 text=True, timeout=60, check=False, stdin=subprocess.DEVNULL).stdout
            found = re.search(r"^\s*Path:\s*(.+)$", out, re.M)
            self.roots[name] = os.path.realpath(found.group(1).strip()) if found else None
        root = self.roots[name]
        if not root:
            return None
        full = os.path.join(root, rest)
        return os.path.relpath(full, self.brain) if full.startswith(self.brain + os.sep) else None

    def top(self, kind: str, query: str):
        sub = "query" if kind == "qmd_query" else "search"
        args = [sub, query, "-n", "10", "--format", "files"] + (["--no-rerank"] if sub == "query" else [])
        paths = []
        for line in self.run(args).splitlines():
            m = re.search(r"(qmd://[^,\s]+)", line)
            rel = self.to_rel(m.group(1)) if m else None
            if rel:
                paths.append(rel)
        return paths


def note_date(brain: str, rel: str):
    path = os.path.join(brain, rel)
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            head = [next(f, "") for _ in "x" * 40]
    except OSError:
        return None
    if head and head[0].strip() == "---":
        for key in ("updated", "modified", "created"):
            for line in head[1:]:
                if line.strip() == "---":
                    break
                m = re.match(rf"{key}:\s*['\"]?(\d{{4}}-\d{{2}}-\d{{2}}(?:[ T]\d{{2}}:\d{{2}})?)", line)
                if m:
                    return m.group(1).replace("T", " ")
    return dt.datetime.fromtimestamp(os.path.getmtime(path)).strftime("%Y-%m-%d %H:%M")


def plain_words(pattern: str) -> bool:
    """A grep pattern QMD's keyword search can stand in for: words, no regex syntax."""
    return bool(re.fullmatch(r"[\w\s.'\-]+", pattern)) and not re.search(r"\\|\.\*", pattern)


def missed_newer(sessions, qmd: Qmd, brain: str, max_queries: int):
    flags, checked = [], 0
    for (agent, session), evs in sessions.items():
        for i, e in enumerate(evs):
            if checked >= max_queries:
                return flags, checked
            query = e.get("query") or ""
            if e["kind"] not in SEARCH or not query or (e["kind"] != "qmd_query" and not plain_words(query)):
                continue
            read_after = {qmd.to_rel(p) or p for later in evs[i + 1:] if later["kind"] == "read" for p in later.get("paths", [])}
            read_after = {p if p.endswith(".md") else p + ".md" for p in read_after if p}
            checked += 1
            top = qmd.top(e["kind"] if e["kind"] == "qmd_query" else "qmd_search", query)
            hit = [p for p in top if p in read_after]
            if not hit:
                continue
            dates = {p: note_date(brain, p) for p in top}
            newest_read = max(dates[p] or "" for p in hit)
            last_hit = max(top.index(p) for p in hit)
            folders = {os.path.dirname(p) for p in hit}
            for rank, p in enumerate(top):
                # Same topic: QMD ranked it above a note the session read, or it sits next to one.
                near = rank < last_hit or os.path.dirname(p) in folders
                if near and p not in read_after and (dates[p] or "") > newest_read:
                    flags.append((e["when"].strftime("%Y-%m-%d %H:%M"), agent, query.replace("\n", " / ")[:80],
                                  ", ".join(hit), newest_read, p, dates[p]))
    return flags, checked


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    state = os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state")
    ap.add_argument("--log", default=os.path.join(state, "atlas", "retrieval-events.jsonl"))
    ap.add_argument("--days", type=int, default=7, help="days back, today included (default 7)")
    ap.add_argument("--agent", help="claude, codex or grok")
    ap.add_argument("--check-newer", action="store_true", help="rerun queries through QMD (read-only)")
    ap.add_argument("--max-queries", type=int, default=20)
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between QMD calls")
    a = ap.parse_args()
    if not os.path.exists(a.log):
        sys.exit(f"no log at {a.log}: set ATLAS_RETRIEVAL_LOG=1 in the Atlas config to start one")
    since = dt.date.today() - dt.timedelta(days=a.days - 1)
    sessions = sessions_of(load(a.log, since, a.agent))
    rows = []
    for (agent, _), evs in sessions.items():
        rows.append(dict(session_stats(evs), agent=agent))
    print(f"# Brain retrieval, {since} to {dt.date.today()} ({len(rows)} sessions)\n")
    print(table(rows) if rows else "No brain lookups logged in this period.")
    if a.check_newer:
        cfg = config()
        qmd, brain = cfg.get("ATLAS_QMD_CMD", ""), cfg.get("ATLAS_BRAIN_PATH", "")
        if not (qmd.startswith("/") and os.access(qmd, os.X_OK) and os.path.isdir(brain)):
            sys.exit("--check-newer needs ATLAS_QMD_CMD (absolute path) and ATLAS_BRAIN_PATH in the Atlas config")
        flags, checked = missed_newer(sessions, Qmd(qmd, brain, a.delay), os.path.realpath(brain), a.max_queries)
        print(f"\n## Missed newer notes ({len(flags)} in {checked} queries rechecked)\n")
        if flags:
            print("| When | Agent | Query | Read | Read date | Newer note not read | Its date |\n| --- | --- | --- | --- | --- | --- | --- |")
            for f in flags:
                print("| " + " | ".join(str(x).replace("|", "/") for x in f) + " |")


if __name__ == "__main__":
    main()
