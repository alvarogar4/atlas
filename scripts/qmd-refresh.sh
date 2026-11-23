#!/bin/sh
# PostToolUse hook (Write|Edit). When an agent writes a Markdown note inside the brain, re-read
# changed notes into QMD's index in the background, so the note is searchable at once.
#
# Off unless the Atlas config has ATLAS_QMD_REFRESH=1 and ATLAS_QMD_CMD is the absolute path of
# an executable. It only ever runs `<qmd> update`, from the brain folder. It is an
# optimisation: searches stay correct without it (grep sees every file).
# It prints nothing, never waits for QMD and always exits 0.

# The hook runs in whatever folder the agent is working in. Nothing here may depend on that
# folder: this script's own tools come from the system folders, and the config is read only
# by absolute path. QMD itself is started with the PATH the hook was given (it may need the
# user's own Node).
USER_PATH=$PATH
PATH="/usr/bin:/bin:/usr/sbin:/sbin:$PATH"
cfg="${ATLAS_CONFIG:-$HOME/.config/atlas/.env}"
case "$cfg" in /*) ;; *) exit 0 ;; esac
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
    /*) py=$(command -v python3 2>/dev/null); if [ -f "$qmd" ] && [ -x "$qmd" ] && [ -d "$brain" ] && [ -n "$py" ]; then enabled=1; fi ;;
  esac
fi
[ "$enabled" = 1 ] || exit 0

# The rest needs a JSON parser and a lock that the system releases if the process dies.
# -I: Python must not import anything from the current folder or the user's environment.
PATH=$USER_PATH exec "$py" -I "$(dirname "$0")/qmd-refresh.py" "$qmd" "$brain" 2>/dev/null
