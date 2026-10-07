"""Voice-over in the owner's own cloned voice for any video (made for the owner's 3D business videos).

  NARRATOR_ENGINE=clone python tools/voiceover.py script.txt OUT_NAME [--pace 0.85] [--video clip.mp4]

script.txt: plain text. Every sentence ends with . ? or ! and is spoken as its own take, with a real full-stop pause
after it (the same pauses as the channel videos). A blank line between paragraphs gives a longer pause.
Each take is heard back with Whisper medium and re-made (up to 3 tries) if words are misheard.

Writes out/voiceover/OUT_NAME.wav, OUT_NAME.mp3 and OUT_NAME.srt (subtitles, one sentence per cue). With --video,
also OUT_NAME.mp4: that video with the voice-over as its soundtrack (picture copied untouched, no metadata tags).
Only the owner's voice is cloned (assets/voice/owner_prompt*.wav); Chatterbox's Perth watermark is left in place.
"""
import argparse
import os
import re
import subprocess
import sys

os.environ["NARRATOR_ENGINE"] = "clone"
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np            # noqa: E402
import soundfile              # noqa: E402
import imageio_ffmpeg         # noqa: E402

from motion import voice      # noqa: E402
from motion.engine import ROOT  # noqa: E402
from motion.timeline import STOP_PAUSE, QUESTION_PAUSE  # noqa: E402

# Owner (7 Oct 2026): "slow little my cloned voice". Voice-overs default to pace 0.85 (~4.7 syllables/s instead of the
# Shorts' 5.5) with 30% longer pauses; slowing a take down to x0.85 stays clean with rubberband.
PACE = 0.85
PAUSE_SCALE = 1.3
PARAGRAPH_PAUSE = 0.6 * PAUSE_SCALE
LEAD, TAIL = 0.15, 0.4
voice.TEMPO_MIN = 0.8
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact"]


def sentences(text):
    """[(sentence, pause after)] -- paragraphs split on blank lines, sentences on . ? ! followed by a space."""
    out = []
    for para in re.split(r"\n\s*\n", text.strip()):
        parts = [s.strip() for s in re.split(r"(?<=[.?!])\s+", " ".join(para.split())) if s.strip()]
        for k, s in enumerate(parts):
            if not re.search(r"[.?!]$", s):
                s += "."
            last = k == len(parts) - 1
            out.append((s, PARAGRAPH_PAUSE if last else (QUESTION_PAUSE if s.endswith("?") else STOP_PAUSE) * PAUSE_SCALE))
    return out


def stamp(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("name")
    ap.add_argument("--pace", type=float, default=PACE, help="1.0 = the Shorts pace; lower is slower (default %(default)s)")
    ap.add_argument("--video", help="a video to put the voice-over on")
    a = ap.parse_args()

    lines = sentences(open(a.script, encoding="utf-8").read())
    texts = [s for s, _ in lines]
    voice.clone_prefetch(texts)
    voice.clone_check([(s, a.pace) for s in texts])

    sr = voice.SR
    track, cues, t = [np.zeros(int(LEAD * sr))], [], LEAD
    for s, pause in lines:
        path, _ = voice._clone_process(s, a.pace)
        w, wsr = soundfile.read(path)
        w = voice._clone_trim(w if w.ndim == 1 else w.mean(axis=1))
        cues.append((t, t + len(w) / wsr, s))
        track += [w, np.zeros(int(pause * sr))]
        t += len(w) / wsr + pause
    track[-1] = np.zeros(int(TAIL * sr))
    audio = np.concatenate(track)
    audio *= 0.89 / max(1e-6, np.abs(audio).max())          # peak at -1 dB

    out_dir = os.path.join(ROOT, "out", "voiceover")
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.join(out_dir, a.name)
    soundfile.write(base + ".wav", audio, sr, subtype="PCM_16")
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", base + ".wav", "-c:a", "libmp3lame", "-b:a", "192k",
                    "-write_xing", "0", "-id3v2_version", "0", *CLEAN, base + ".mp3"], check=True)
    with open(base + ".srt", "w", encoding="utf-8") as f:
        for k, (s0, s1, s) in enumerate(cues, 1):
            f.write(f"{k}\n{stamp(s0)} --> {stamp(s1)}\n{s}\n\n")
    if a.video:
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", a.video, "-i", base + ".wav", "-map", "0:v:0",
                        "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", *CLEAN, base + ".mp4"],
                       check=True)
    print(f"voice-over: {len(lines)} sentences, {len(audio) / sr:.1f} s -> {base}.wav / .mp3 / .srt"
          + (" / .mp4" if a.video else ""))


if __name__ == "__main__":
    main()
