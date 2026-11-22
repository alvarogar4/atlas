"""Second half of the qmd-refresh hook (started by qmd-refresh.sh only when the user opted in).

Hook mode (event JSON on stdin): if the written file is a Markdown note inside the brain,
start a detached worker and leave at once.

Worker mode: run `<qmd> update` from the brain folder, one refresh at a time.
- QMD's update lists the files, then drops from the index what is not on its list. Two
  overlapping updates can therefore drop a note written between their two listings, so
  refreshes are serialised with a lock the system releases when the process ends.
- Writes that arrive while a refresh is waiting for its turn are covered by it: it lists the
  files after they were written. So at most one refresh waits, and a burst of writes costs two.
"""
import fcntl
import json
import os
import subprocess
import sys


def worker(qmd: str, brain: str) -> None:
    state = os.path.join(os.environ.get("XDG_CACHE_HOME") or os.path.expanduser("~/.cache"), "atlas")
    os.makedirs(state, mode=0o700, exist_ok=True)
    waiting = open(os.path.join(state, "qmd-refresh.waiting"), "w")
    try:
        fcntl.flock(waiting, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        return  # a refresh is already waiting; it starts after this write and will see it
    running = open(os.path.join(state, "qmd-refresh.running"), "w")
    fcntl.flock(running, fcntl.LOCK_EX)  # let the refresh in progress finish
    fcntl.flock(waiting, fcntl.LOCK_UN)  # from here on, a new write queues its own refresh
    subprocess.run([qmd, "update"], cwd=brain, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, timeout=900, check=False)


def hook(qmd: str, brain: str) -> None:
    try:
        path = (json.load(sys.stdin).get("tool_input") or {}).get("file_path") or ""
    except (ValueError, AttributeError):
        return
    root = os.path.realpath(brain)
    if not path.endswith(".md") or os.path.commonpath([root, os.path.realpath(path)]) != root:
        return
    subprocess.Popen([sys.executable, "-I", os.path.abspath(__file__), "--worker", qmd, brain],
                     stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                     start_new_session=True, cwd="/")


if __name__ == "__main__":
    try:
        if len(sys.argv) == 4 and sys.argv[1] == "--worker":
            worker(sys.argv[2], sys.argv[3])
        elif len(sys.argv) == 3:
            hook(sys.argv[1], sys.argv[2])
    except Exception:  # a hook must never fail a tool call
        pass
