#!/bin/sh
# PostToolUse hook (Write|Edit). When an agent writes a Markdown note inside the brain, re-read
# changed notes into QMD's keyword index in the background, so the note is searchable at once.
#
# Off unless the Atlas config says ATLAS_QMD_REFRESH=1 and names QMD in ATLAS_QMD_CMD. It only
# ever runs `<qmd> update`: it never embeds, never downloads a model and never sends note text
# anywhere. It is an optimisation: searches stay correct without it (grep sees every file).
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
  # ATLAS_QMD_CMD is one executable (a name on the PATH or a path), never a command line.
  if [ -n "$qmd" ] && [ -n "$brain" ] && command -v "$qmd" >/dev/null 2>&1; then enabled=1; fi
fi
if [ "$enabled" != 1 ]; then cat >/dev/null 2>&1; exit 0; fi   # drain the event, do nothing

# The file path, read with a real JSON parser so quotes and escapes in names are handled.
if command -v jq >/dev/null 2>&1; then
  file=$(jq -r '.tool_input.file_path // empty' 2>/dev/null)
elif command -v python3 >/dev/null 2>&1; then
  file=$(python3 -c 'import json,sys; print((json.load(sys.stdin).get("tool_input") or {}).get("file_path") or "")' 2>/dev/null)
else
  cat >/dev/null 2>&1; exit 0
fi
case "$file" in
  "${brain%/}"/*.md) ;;
  *) exit 0 ;;
esac

# One refresh per write. QMD serialises overlapping refreshes itself, and each one reads the
# files as they are when it starts, so the last write of a burst is always picked up.
( "$qmd" update ) </dev/null >/dev/null 2>&1 &
exit 0
