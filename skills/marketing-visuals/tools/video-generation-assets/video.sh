#!/usr/bin/env bash
# Remotion video helper for marketing-visuals. Run through package.json from this folder:
# bun scaffold | bun stills | bun render | bun save | bun sheet (same arguments as below).
#
#   video.sh new    <workdir> [fonts_dir]      scaffold the template, copy fonts, install deps
#   video.sh stills <workdir> <frame>...       render stills at those frames into out/stills.png (2 columns)
#   video.sh render <workdir> <name>           render out/<name>.mp4 + out/<name>.gif, check loop, frame sheet,
#                                              report audio loudness if the scene has sound
#                                              (GIF_NTH=3 keeps every 3rd frame for a smaller GIF; default 2;
#                                              GIF=0 renders the MP4 only, for films)
#   video.sh save   <workdir> <resources_dir> <name>   copy outputs of every format, source and audio
#   video.sh sheet  <video> [px]               contact sheet of any video, one frame a second (<video>-sheet.png),
#                                              plus frozen stretches of 3 s or more and the first frame's luma;
#                                              for a reference film or a finished render (px 360 = phone width)
#
# COMP=<id> picks the composition (a key of FORMATS in Scene.tsx) for stills and render; default Video.
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
      npx remotion still src/index.ts "${COMP:-Video}" "out/still-$(printf %03d $i).png" --frame="$f" >/dev/null
    done
    rows=$(( (i + 1) / 2 ))
    ffmpeg -loglevel error -y -i out/still-%03d.png -vf "scale=600:-1,tile=2x${rows}:padding=4:color=white" -frames:v 1 out/stills.png
    echo "out/stills.png  frames: $*"
    ;;

  render)
    W="${1:?workdir}"; NAME="${2:?name}"
    cd "$W"; mkdir -p out
    npx remotion render src/index.ts "${COMP:-Video}" "out/$NAME.mp4" --codec=h264 --crf=18 >/dev/null
    if [ "${GIF:-1}" = 0 ]; then
      ls -la "out/$NAME.mp4" | awk '{print $5, $9}'
    else
      npx remotion render src/index.ts "${COMP:-Video}" "out/$NAME.gif" --codec=gif --every-nth-frame="${GIF_NTH:-2}" >/dev/null
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
    fi
    # Sound is optional. When the MP4 has it, report loudness; the GIF never carries sound.
    if [ -n "$(ffprobe -v error -select_streams a -show_entries stream=index -of csv=p=0 "out/$NAME.mp4")" ]; then
      lufs=$(ffmpeg -nostats -i "out/$NAME.mp4" -af ebur128 -f null - 2>&1 | awk '/Integrated loudness/{f=1} f&&/I:/{print $2; exit}')
      peak=$(ffmpeg -nostats -i "out/$NAME.mp4" -af volumedetect -f null - 2>&1 | awk '/max_volume/{print $5}')
      echo "audio: yes, ${lufs} LUFS integrated, peak ${peak} dB (the GIF is silent)"
      echo "  music bed: aim for -16 to -14 LUFS; cues only: LUFS reads low, keep the peak between -10 and -1 dB"
    else
      echo "audio: none"
    fi
    if [ "${GIF:-1}" = 0 ]; then echo "check: bun sheet $W/out/$NAME.mp4"; else echo "check: out/gif-sheet.png"; fi
    ;;

  sheet)
    V="${1:?video}"; PX="${2:-480}"
    need ffmpeg "brew install ffmpeg"
    OUT="${V%.*}-sheet.png"
    dur=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$V")
    # One frame a second; past 72 s, 72 frames spread over the whole video.
    fps=$(awk -v d="$dur" 'BEGIN { printf "%.4f", (d > 72 ? 72 / d : 1) }')
    n=$(awk -v d="$dur" -v f="$fps" 'BEGIN { print int(d * f) + 1 }')
    ffmpeg -loglevel error -y -i "$V" -vf "fps=$fps,scale=$PX:-1,tile=6x$(( (n + 5) / 6 )):padding=4:color=white" -frames:v 1 "$OUT"
    # Dead stretches: 3 s or more where the picture does not change (-70dB: small moving dots still count as motion).
    frozen=$(ffmpeg -nostats -i "$V" -map 0:v -vf "freezedetect=n=-70dB:d=3" -f null - 2>&1 \
      | awk '/freeze_start/{s=$NF} /freeze_duration/{printf "%s%.1f s at %.1f s", sep, $NF, s; sep=", "}')
    ymax=$(ffmpeg -loglevel error -i "$V" -vf "signalstats,metadata=print:key=lavfi.signalstats.YMAX:file=-" -frames:v 1 -f null - \
      | grep -o 'YMAX=[0-9]*' | head -1 | cut -d= -f2)
    printf "%s  %.1f s, %s frames at %s fps, left to right, top to bottom\n" "$OUT" "$dur" "$n" "$fps"
    echo "frozen 3 s+: ${frozen:-none}"
    echo "first-frame YMAX: $ymax"
    if [ "$ymax" -le 24 ]; then echo "warning: frame 0 is black; it is the thumbnail on X and LinkedIn (fine for a looping GIF)"; fi
    ;;

  save)
    W="${1:?workdir}"; R="${2:?resources_dir}"; NAME="${3:?name}"
    mkdir -p "$R/$NAME-src/src"
    # Every format rendered under this name: <name>.mp4 and <name>-<format>.mp4, plus their GIFs.
    shopt -s nullglob
    outs=("$W/out/$NAME".mp4 "$W/out/$NAME".gif "$W/out/$NAME"-*.mp4 "$W/out/$NAME"-*.gif)
    [ ${#outs[@]} -gt 0 ] || { echo "no outputs named $NAME in $W/out" >&2; exit 1; }
    cp "${outs[@]}" "$R/"
    cp "$W"/src/*.ts* "$R/$NAME-src/src/"
    cp "$W/package.json" "$R/$NAME-src/"
    audio=("$W"/public/audio/*)
    if [ ${#audio[@]} -gt 0 ]; then mkdir -p "$R/$NAME-src/audio"; cp "${audio[@]}" "$R/$NAME-src/audio/"; fi
    cat > "$R/$NAME-src/README.md" <<EOF
Remotion source for \`../$NAME.gif\` and \`../$NAME.mp4\`.

To re-render, from the marketing-visuals \`tools/video-generation-assets\` folder:

    bun scaffold <scratch-dir> <fonts-dir>
    cp -R <path-to-this-folder>/src <scratch-dir>/
    mkdir -p <scratch-dir>/public/audio && cp <path-to-this-folder>/audio/* <scratch-dir>/public/audio/  # only if audio/ exists
    COMP=<format> bun render <scratch-dir> $NAME[-<format>]
EOF
    echo "saved: ${outs[*]##*/} and $R/$NAME-src/"
    ;;

  *)
    sed -n '2,16p' "$0" | sed 's/^# \{0,1\}//'
    exit 1
    ;;
esac
