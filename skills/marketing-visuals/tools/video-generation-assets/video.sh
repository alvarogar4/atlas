#!/usr/bin/env bash
# Remotion video helper for marketing-visuals. Run through package.json from this folder:
# bun scaffold | bun stills | bun render | bun save (same arguments as below).
#
#   video.sh new    <workdir> [fonts_dir]      scaffold the template, copy fonts, install deps
#   video.sh stills <workdir> <frame>...       render stills at those frames into out/stills.png (2 columns)
#   video.sh render <workdir> <name>           render out/<name>.mp4 + out/<name>.gif, check loop, frame sheet
#                                              (GIF_NTH=3 keeps every 3rd frame for a smaller GIF; default 2)
#   video.sh save   <workdir> <resources_dir> <name>   copy outputs and source into the content folder
#
# Keep <workdir> outside the brain (scratchpad): node_modules must never land in resources/.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
cmd="${1:-}"; shift || true

need() { command -v "$1" >/dev/null || { echo "missing: $1 ($2)" >&2; exit 1; }; }

case "$cmd" in
  new)
    W="${1:?workdir}"; FONTS="${2:-}"
    need bun "brew install oven-sh/bun/bun"; need ffmpeg "brew install ffmpeg"
    [ -e "$W/src" ] && { echo "$W already has a project" >&2; exit 1; }
    mkdir -p "$W"
    cp -R "$HERE/template/." "$W/"
    if [ -n "$FONTS" ]; then cp "$FONTS"/*.woff2 "$W/public/fonts/"; fi
    (cd "$W" && bun install >/dev/null)
    echo "ready: $W (edit src/kit.tsx tokens + FONTS, then src/Scene.tsx)"
    ls "$W/public/fonts" | grep -q woff2 || echo "warning: no fonts in public/fonts, text will use system fallbacks"
    ;;

  stills)
    W="${1:?workdir}"; shift
    [ $# -gt 0 ] || { echo "give at least one frame" >&2; exit 1; }
    cd "$W"; mkdir -p out; rm -f out/still-*.png
    i=0
    for f in "$@"; do
      i=$((i + 1))
      npx remotion still src/index.ts Video "out/still-$(printf %03d $i).png" --frame="$f" >/dev/null
    done
    rows=$(( (i + 1) / 2 ))
    ffmpeg -loglevel error -y -i out/still-%03d.png -vf "scale=600:-1,tile=2x${rows}:padding=4:color=white" -frames:v 1 out/stills.png
    echo "out/stills.png  frames: $*"
    ;;

  render)
    W="${1:?workdir}"; NAME="${2:?name}"
    cd "$W"; mkdir -p out
    npx remotion render src/index.ts Video "out/$NAME.mp4" --codec=h264 --crf=18 >/dev/null
    npx remotion render src/index.ts Video "out/$NAME.gif" --codec=gif --every-nth-frame="${GIF_NTH:-2}" >/dev/null
    # Loop check: first and last GIF frames should be black (luma max near 16).
    ffmpeg -loglevel error -i "out/$NAME.gif" -vf "signalstats,metadata=print:key=lavfi.signalstats.YMAX:file=out/ymax.txt" -f null -
    first=$(grep -o 'YMAX=[0-9]*' out/ymax.txt | head -1 | cut -d= -f2)
    last=$(grep -o 'YMAX=[0-9]*' out/ymax.txt | tail -1 | cut -d= -f2)
    frames=$(grep -c YMAX out/ymax.txt)
    # Frame sheet: 6 evenly spaced GIF frames, to check the encoded result.
    step=$(( frames / 6 > 0 ? frames / 6 : 1 ))
    ffmpeg -loglevel error -y -i "out/$NAME.gif" -vf "select='not(mod(n\,$step))',scale=600:-1,tile=2x3:padding=4:color=white" -frames:v 1 out/gif-sheet.png
    ls -la "out/$NAME.mp4" "out/$NAME.gif" | awk '{print $5, $9}'
    echo "gif frames: $frames  first-frame YMAX: $first  last-frame YMAX: $last"
    if [ "$first" -gt 24 ] || [ "$last" -gt 24 ]; then echo "warning: GIF does not start and end on black, the loop will show a seam"; fi
    echo "check: out/gif-sheet.png"
    ;;

  save)
    W="${1:?workdir}"; R="${2:?resources_dir}"; NAME="${3:?name}"
    mkdir -p "$R/$NAME-src/src"
    cp "$W/out/$NAME.mp4" "$W/out/$NAME.gif" "$R/"
    cp "$W"/src/*.ts* "$R/$NAME-src/src/"
    cp "$W/package.json" "$R/$NAME-src/"
    cat > "$R/$NAME-src/README.md" <<EOF
Remotion source for \`../$NAME.gif\` and \`../$NAME.mp4\`.

To re-render, from the marketing-visuals \`tools/video-generation-assets\` folder:

    bun scaffold <scratch-dir> <fonts-dir>
    cp -R <path-to-this-folder>/src <scratch-dir>/
    bun render <scratch-dir> $NAME
EOF
    echo "saved: $R/$NAME.mp4, $R/$NAME.gif, $R/$NAME-src/"
    ;;

  *)
    sed -n '2,12p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
    ;;
esac
