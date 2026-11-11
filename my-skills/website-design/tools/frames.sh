#!/usr/bin/env bash
# frames.sh: turn a film into the frame sequences a scroll film or walkthrough plays.
#
#   ./frames.sh <video> <out-dir> [frames-per-second=24] [width=1920]
#
# Writes <out-dir>/landscape/0001.webp ..., <out-dir>/portrait/0001.webp ... (a 4:5 centre crop for
# phones), and poster.jpg (the first frame, for the no-script view and link previews). Prints the
# SequencePlayer settings to paste. Needs ffmpeg with libwebp.
#
# Budget: 150 to 300 frames is plenty for a full-page journey. At quality 70, 1920 px frames run
# 60 to 140 KB each; the player loads every 16th frame first, so scrubbing works while the rest arrive.
set -euo pipefail
in="${1:?video file}"; out="${2:?output folder}"; fps="${3:-24}"; width="${4:-1920}"
command -v ffmpeg >/dev/null || { echo "ffmpeg is not installed" >&2; exit 2; }
mkdir -p "$out/landscape" "$out/portrait"
ffmpeg -hide_banner -loglevel error -y -i "$in" -vf "fps=$fps,scale=$width:-2" -c:v libwebp -quality 70 "$out/landscape/%04d.webp"
ffmpeg -hide_banner -loglevel error -y -i "$in" -vf "fps=$fps,crop=ih*4/5:ih,scale=1080:-2" -c:v libwebp -quality 70 "$out/portrait/%04d.webp"
ffmpeg -hide_banner -loglevel error -y -i "$in" -vf "scale=$width:-2" -frames:v 1 -q:v 3 "$out/poster.jpg"
n=$(ls "$out/landscape" | wc -l | tr -d ' ')
kb=$(du -sk "$out/landscape" | cut -f1)
echo "Frames: $n landscape, $(ls "$out/portrait" | wc -l | tr -d ' ') portrait. Landscape set: ${kb} KB in total."
cat <<EOF
new SequencePlayer({
  canvas,
  frameCount: $n,
  src: (i) => \`/$(basename "$out")/landscape/\${String(i + 1).padStart(4, '0')}.webp\`,
  portraitSrc: (i) => \`/$(basename "$out")/portrait/\${String(i + 1).padStart(4, '0')}.webp\`,
});
EOF
