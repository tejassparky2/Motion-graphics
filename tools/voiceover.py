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


def paragraphs(text, gap):
    """Presenter style (--flow): each paragraph is one flowing take, with a short gap after it."""
    return [(" ".join(p.split()), gap) for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


# Presenter polish (--polish): clean low end, a little warmth and presence, gentle de-essing and even level --
# the close-mic sound of a creator talking to camera.
POLISH = ("highpass=f=75,equalizer=f=180:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.2:g=3,"
          "equalizer=f=9000:t=q:w=1:g=1.5,deesser=i=0.35,"
          "acompressor=threshold=0.1:ratio=3:attack=8:release=120:makeup=1.6")


def phrases(text, gap, comma=0.2, stop=0.4):
    """Even presenter style (--phrases): every phrase (split at commas and full stops) is its own take, all set to the
    same pace, joined with short natural pauses; `gap` after each line. -> [(phrase, pause after, line index)]"""
    out = []
    for li, para in enumerate(p for p in re.split(r"\n\s*\n", text.strip()) if p.strip()):
        parts = [x.strip() for x in re.split(r"(?<=[,.?!])\s+", " ".join(para.split())) if x.strip()]
        for k, x in enumerate(parts):
            last = k == len(parts) - 1
            out.append((x, gap if last else comma if x.endswith(",") else stop, li))
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
    ap.add_argument("--flow", action="store_true", help="presenter style: one take per paragraph, short gaps")
    ap.add_argument("--gap", type=float, default=0.3, help="pause after each paragraph with --flow (s)")
    ap.add_argument("--polish", action="store_true", help="presenter EQ, de-ess and compression")
    ap.add_argument("--phrases", action="store_true", help="one take per phrase, same pace (short phrases can drawl)")
    ap.add_argument("--even", type=float, default=0, metavar="SYL_PER_S",
                    help="even out the speed inside each take: stretch every phrase to this rate (e.g. 5.4)")
    a = ap.parse_args()

    text = open(a.script, encoding="utf-8").read()
    if a.phrases:
        trip = phrases(text, a.gap)
        lines, line_of = [(x, p) for x, p, _ in trip], [li for _, _, li in trip]
    else:
        lines = paragraphs(text, a.gap) if a.flow else sentences(text)
        line_of = list(range(len(lines)))
    texts = [s for s, _ in lines]
    voice.clone_prefetch(texts)
    voice.clone_check([(s, a.pace) for s in texts], slack=0.07 if a.phrases else 0.15)

    sr = voice.SR
    track, cues, t = [np.zeros(int(LEAD * sr))], [], LEAD
    for s, pause in lines:
        path, _ = voice._clone_process(s, a.pace)
        if a.even:
            from even_pace import even
            evened = path[:-4] + f".even{a.even}.wav"
            if not os.path.exists(evened):
                for p, r0, r1 in even(path, s, evened, a.even):
                    print(f"  even: {r0:4.1f} -> {r1:4.1f} syl/s  {p}", file=sys.stderr)
            path = evened
        w, wsr = soundfile.read(path)
        w = voice._clone_trim(w if w.ndim == 1 else w.mean(axis=1))
        cues.append((t, t + len(w) / wsr, s))
        track += [w, np.zeros(int(pause * sr))]
        t += len(w) / wsr + pause
    track[-1] = np.zeros(int(TAIL * sr))
    if a.phrases:   # one caption cue per line, not per phrase
        merged = {}
        for (c0, c1, txt), li in zip(cues, line_of):
            m = merged.setdefault(li, [c0, c1, []])
            m[1] = c1
            m[2].append(txt)
        cues = [(c0, c1, " ".join(t)) for c0, c1, t in merged.values()]
    audio = np.concatenate(track)
    audio *= 0.89 / max(1e-6, np.abs(audio).max())          # peak at -1 dB

    out_dir = os.path.join(ROOT, "out", "voiceover")
    os.makedirs(out_dir, exist_ok=True)
    base = os.path.join(out_dir, a.name)
    soundfile.write(base + ".wav", audio, sr, subtype="PCM_16")
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    if a.polish:
        subprocess.run([ff, "-y", "-loglevel", "error", "-i", base + ".wav", "-af", POLISH + ",alimiter=limit=0.89",
                        *CLEAN, base + ".polish.wav"], check=True)
        os.replace(base + ".polish.wav", base + ".wav")
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
