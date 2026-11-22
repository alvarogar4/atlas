#!/bin/sh
# PostToolUse hook (Write|Edit). When an agent writes a Markdown note inside the brain and QMD
# is configured (ATLAS_QMD_CMD in the Atlas config), refresh QMD's index in the background so
# the note is searchable right away: `update` for keywords, `embed` for meaning.
#
# It is an optimisation, never a requirement: the skill still runs `qmd update` before the
# first search of a session. So this script does nothing when anything is missing, never
# prints, never waits for QMD and always exits 0.

input=$(cat 2>/dev/null) || exit 0
cfg="${ATLAS_CONFIG:-$HOME/.config/atlas/.env}"
[ -f "$cfg" ] || exit 0

value() {  # value NAME: last NAME=... line of the config, quotes stripped, leading ~ expanded
  v=$(sed -n "s/^[[:space:]]*$1=//p" "$cfg" | tail -n 1)
  v=${v%\"}; v=${v#\"}; v=${v%\'}; v=${v#\'}
  # shellcheck disable=SC2088  # a literal ~/ from the config file, expanded here by hand
  case "$v" in "~/"*) v="$HOME/${v#\~/}" ;; esac
  printf '%s' "$v"
}
qmd=$(value ATLAS_QMD_CMD)
brain=$(value ATLAS_BRAIN_PATH)
[ -n "$qmd" ] && [ -n "$brain" ] || exit 0

file=$(printf '%s' "$input" | sed -n 's/.*"file_path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -n 1)
case "$file" in
  "${brain%/}"/*.md) ;;
  *) exit 0 ;;
esac

# One refresh at a time. A write that lands while one is running sets the "dirty" flag and the
# running refresh goes round once more, so the last write of a burst is never left out.
lock="${TMPDIR:-/tmp}/atlas-qmd-refresh.$(id -u)"
: > "$lock.dirty" 2>/dev/null || exit 0
find "$lock" -maxdepth 0 -mmin +15 -exec rmdir {} \; 2>/dev/null   # a lock left by a crash
mkdir "$lock" 2>/dev/null || exit 0
(
  trap 'rmdir "$lock" 2>/dev/null' EXIT
  while [ -e "$lock.dirty" ]; do
    rm -f "$lock.dirty"
    # $qmd is split on purpose: the command may carry arguments (for example an ssh prefix)
    $qmd update && $qmd embed
  done
) </dev/null >/dev/null 2>&1 &
exit 0
