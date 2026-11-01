#!/bin/bash
# WW2 Ep1 send copy: the 32 picture chunks (out/ww2/ep01/parts, frame order P1..P8) + the lossless mix -> one clean mp4.
# One encode generation: x264 crf 20, preset slow, tune animation, VBV cap 4 Mbps (<= ~376 MiB, under the 400 MiB send limit);
# AAC 320k 48 kHz; no metadata, no encoder tags (SEI dropped, then a stream-copy remux clears the encoder name).
#   bash channels/ww2/ep01/deliver.sh [OUT_DIR]       (default OUT_DIR: build/ww2)
set -e
cd "$(dirname "$0")/../../.."
OUT=${1:-build/ww2}; mkdir -p "$OUT"
FF=$(/home/user/.venv-main/bin/python -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
L=$OUT/concat.txt; : > "$L"
for p in P1 P2 P3 P4 P5 P6 P7 P8; do
  for f in $(ls out/ww2/ep01/parts/${p}_f*.mp4 | sort); do echo "file '$PWD/$f'" >> "$L"; done
done
echo "chunks: $(wc -l < "$L") (expect 32)"
"$FF" -y -v error -stats -f concat -safe 0 -i "$L" -i out/ww2/ep01/mix.flac -map 0:v:0 -map 1:a:0 \
  -c:v libx264 -preset slow -tune animation -crf 20 -maxrate 4000k -bufsize 8000k -pix_fmt yuv420p \
  -c:a aac -b:a 320k -ar 48000 -map_metadata -1 -map_chapters -1 -fflags +bitexact -flags:v +bitexact -flags:a +bitexact \
  -bsf:v filter_units=remove_types=6 -movflags +faststart "$OUT/enc_tmp.mp4"
"$FF" -y -v error -i "$OUT/enc_tmp.mp4" -map 0 -c copy -map_metadata -1 -fflags +bitexact -flags:v +bitexact -flags:a +bitexact \
  -metadata:s:v handler_name= -metadata:s:a handler_name= -movflags +faststart "$OUT/WW2_Explained_Episode1.mp4"
rm -f "$OUT/enc_tmp.mp4" "$L"
/home/user/.venv-main/bin/python -c "import cv2;c=cv2.VideoCapture('$OUT/WW2_Explained_Episode1.mp4');print('frames',int(c.get(7)),'(expect 17623)')"
echo "tags: $(strings "$OUT/WW2_Explained_Episode1.mp4" | grep -cE 'Lavf[0-9]|Lavc[0-9]|x264 - core|libx264') (expect 0)"
ls -la "$OUT/WW2_Explained_Episode1.mp4"
