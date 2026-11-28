#!/bin/sh
# PostToolUse hook (Bash, Read, Grep, Glob and Grok's names for them). When an agent searches or
# reads the brain, append one line about it to a local log, so `retrieval-report.py` can measure
# how agents find notes in real sessions.
#
# Off unless the Atlas config has ATLAS_RETRIEVAL_LOG=1. It logs the search query or pattern, the
# brain-relative paths read, the tool and timings: never a command line or a tool's output, so no
# note text. The log is ${XDG_STATE_HOME:-~/.local/state}/atlas/retrieval-events.jsonl (mode 600).
# It prints nothing (Grok shows a PostToolUse hook's output to the model) and always exits 0.

# Nothing here may depend on the folder the agent works in: tools come from the system folders
# and the config is read only by absolute path.
PATH="/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
cfg="${ATLAS_CONFIG:-$HOME/.config/atlas/.env}"
case "$cfg" in /*) ;; *) exit 0 ;; esac
[ -r "$cfg" ] || exit 0
on=$(sed -n 's/^[[:space:]]*ATLAS_RETRIEVAL_LOG=//p' "$cfg" 2>/dev/null | tail -n 1)
on=${on%\"}; on=${on#\"}; on=${on%\'}; on=${on#\'}
[ "$on" = 1 ] || exit 0
brain=$(sed -n 's/^[[:space:]]*ATLAS_BRAIN_PATH=//p' "$cfg" 2>/dev/null | tail -n 1)
brain=${brain%\"}; brain=${brain#\"}; brain=${brain%\'}; brain=${brain#\'}
# shellcheck disable=SC2088  # a literal ~/ from the config file, expanded here by hand
case "$brain" in "~/"*) brain="$HOME/${brain#\~/}" ;; esac
brain=${brain%/}
[ -n "$brain" ] && [ -d "$brain" ] || exit 0
real=$(cd "$brain" 2>/dev/null && pwd -P) || exit 0
# Most tool calls never touch the brain: skip them without starting Python (Grok runs this hook
# in the foreground). Anything that names the brain, QMD, Obsidian or a note goes on to the parser.
payload=$(cat)
case "$payload" in
  *"$brain"* | *"$real"* | *qmd* | *bsidian* | *.md*) ;;
  *) exit 0 ;;
esac
py=$(command -v python3 2>/dev/null) || exit 0
# -I: Python must not import anything from the current folder or the user's environment.
printf '%s\n' "$payload" | "$py" -I "$(dirname "$0")/retrieval-log.py" "$cfg" >/dev/null 2>&1
exit 0
