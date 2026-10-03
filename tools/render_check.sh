#!/bin/bash
# Render each video, then check it: verify.py (Whisper small: words, pace, no encoder tags) and audit.py
# (Whisper medium on every line, the standing rule). Run from the repo root:  tools/render_check.sh kidney_donor
cd "$(dirname "$0")/.."
for v in "$@"; do
  if ! python render.py --video "$v" > "build/$v.log" 2>&1; then echo "== $v FAILED"; grep -a -A4 Traceback "build/$v.log" | tail -5; continue; fi
  PYTHONPATH=. python tools/verify.py "$v" > "build/verify_$v.log" 2>&1
  echo "== $v | $(grep -a -o 'narration: .*wpm while speaking' "build/$v.log" | sed 's/narration: //') | $(grep -o 'ASR match [0-9.]*%' "build/verify_$v.log")"
  python tools/audit.py "$v" 2>&1 | grep -E "^  |flagged"
done
