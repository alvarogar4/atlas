#!/bin/sh
# PostToolUse hook (Write|Edit). When an agent writes a Markdown note inside the brain, re-read
# changed notes into QMD's index in the background, so the note is searchable at once.
#
# Off unless the Atlas config has ATLAS_QMD_REFRESH=1 and ATLAS_QMD_CMD is the absolute path of
# an executable. It only ever runs `<qmd> update`, from the brain folder. It is an
# optimisation: searches stay correct without it (grep sees every file).
# It prints nothing, never waits for QMD and always exits 0.

cfg="${ATLAS_CONFIG:-$HOME/.config/atlas/.env}"
value() {  # value NAME: last NAME=... line of the config, quotes stripped, leading ~/ expanded
  v=$(sed -n "s/^[[:space:]]*$1=//p" "$cfg" 2>/dev/null | tail -n 1)
  v=${v%\"}; v=${v#\"}; v=${v%\'}; v=${v#\'}
  # shellcheck disable=SC2088  # a literal ~/ from the config file, expanded here by hand
  case "$v" in "~/"*) v="$HOME/${v#\~/}" ;; esac
  printf '%s' "$v"
}
enabled=0
if [ -r "$cfg" ] && [ "$(value ATLAS_QMD_REFRESH)" = 1 ]; then
  qmd=$(value ATLAS_QMD_CMD); brain=$(value ATLAS_BRAIN_PATH)
  # One executable by absolute path: never a command line, a bare name or a path relative to
  # whatever project the agent happens to be working in.
  case "$qmd" in
    /*) if [ -f "$qmd" ] && [ -x "$qmd" ] && [ -d "$brain" ] && command -v python3 >/dev/null 2>&1; then enabled=1; fi ;;
  esac
fi
if [ "$enabled" != 1 ]; then cat >/dev/null 2>&1; exit 0; fi   # drain the event, do nothing

# The rest needs a JSON parser and a lock that the system releases if the process dies.
# -I: Python must not import anything from the current folder or the user's environment.
exec python3 -I "$(dirname "$0")/qmd-refresh.py" "$qmd" "$brain" 2>/dev/null
