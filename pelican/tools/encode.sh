#!/usr/bin/env bash
# Encode rendered frames + soundtrack into the final film.
#   encode.sh FRAMES_DIR SOUNDTRACK.wav OUT.mp4 [FIRST_FRAME] [NUM_FRAMES]
# Adds a soft lens vignette, fine film grain and fades in/out.
set -euo pipefail
FRAMES=$1
AUDIO=$2
OUT=$3
FIRST=${4:-1}
COUNT=${5:-$(ls "$FRAMES"/f_*.png | wc -l)}
FPS=24
DUR=$(python3 -c "print(${COUNT}/${FPS})")
FADE_OUT_START=$(python3 -c "print(max(0.0, ${COUNT}/${FPS} - 1.6))")

ffmpeg -y -loglevel error -stats \
  -framerate $FPS -start_number "$FIRST" -i "$FRAMES/f_%04d.png" \
  -i "$AUDIO" \
  -filter_complex "[0:v]format=rgb24,vignette=angle=0.55:mode=forward,noise=alls=2:allf=t,\
fade=t=in:st=0:d=0.6,fade=t=out:st=${FADE_OUT_START}:d=1.6,format=yuv420p[v]" \
  -map "[v]" -map 1:a -t "$DUR" \
  -c:v libx264 -preset slow -crf 18 -tune film -profile:v high -pix_fmt yuv420p \
  -movflags +faststart \
  -c:a aac -b:a 256k \
  "$OUT"
echo "wrote $OUT"
