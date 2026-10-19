"""Hindi voice-over in the owner's cloned voice (Chatterbox Multilingual), for the Hindi page's reels.

  python tools/hindi_voiceover.py script.txt OUT_NAME [--gap 0.9]

script.txt: Devanagari, one paragraph per line group (blank line between); each paragraph is one flowing take, like the
English reels' --flow --polish style. Every take is heard back with Whisper medium (Hindi) and re-made up to 3 times
if it doesn't match the script. Writes out/voiceover/OUT_NAME.wav / .mp3 / .srt (no metadata tags).
"""
import argparse
import difflib
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import voiceover as vo          # noqa: E402  (shared helpers: paragraphs, POLISH, CLEAN, stamp, LEAD/TAIL)

import numpy as np              # noqa: E402
import soundfile                # noqa: E402
import imageio_ffmpeg           # noqa: E402

ROOT = vo.ROOT
SR = vo.voice.SR


def norm(s):
    """Compare spoken Hindi loosely: drop punctuation, nukta and chandrabindu/anusvara differences, spaces."""
    s = re.sub(r"[।.,?!'\"“”‘’\-–—:;]", " ", s.lower())
    s = s.replace("़", "").replace("ँ", "ं")
    return "".join(s.split())


def heard_ok(text, heard, need=0.82):
    return difflib.SequenceMatcher(None, norm(text), norm(heard)).ratio() >= need


def takes(texts, lang="hi", tries=3):
    from faster_whisper import WhisperModel
    d = os.path.join(ROOT, "build", "mtl")
    os.makedirs(d, exist_ok=True)
    clone_py = os.environ.get("CLONE_PYTHON", os.path.expanduser("~/.venv-clone/bin/python"))
    checker, chosen, todo = None, {}, list(dict.fromkeys(texts))
    for n in range(tries):
        jobs = [[t, os.path.join(d, f"{vo.voice._key(t)}.{lang}.try{n}.wav")] for t in todo]
        if any(not os.path.exists(o) for _, o in jobs):
            json.dump(jobs, open(os.path.join(d, "jobs.json"), "w"), ensure_ascii=False)
            subprocess.run([clone_py, os.path.join(ROOT, "tools", "mtl_clone_tts.py"), os.path.join(d, "jobs.json"),
                            "--lang", lang], check=True)
        checker = checker or WhisperModel("medium", device="cpu", compute_type="int8")
        bad = []
        for t, o in jobs:
            heard = " ".join(x.text for x in checker.transcribe(o, language=lang, beam_size=5)[0])
            ok = heard_ok(t, heard)
            if t not in chosen or ok:
                chosen[t] = o
            if not ok:
                bad.append(t)
            print(f"try {n + 1} {'ok ' if ok else 'BAD'} {t!r} heard as {heard.strip()!r}", file=sys.stderr)
        todo = bad
        if not todo:
            break
    return chosen


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("name")
    ap.add_argument("--gap", type=float, default=0.9)
    ap.add_argument("--lang", default="hi")
    a = ap.parse_args()
    lines = vo.paragraphs(open(a.script, encoding="utf-8").read(), a.gap)
    got = takes([s for s, _ in lines], a.lang)
    track, cues, t = [np.zeros(int(vo.LEAD * SR))], [], vo.LEAD
    for s, pause in lines:
        w, wsr = soundfile.read(got[s])
        w = w if w.ndim == 1 else w.mean(axis=1)
        if wsr != SR:
            from math import gcd
            from scipy.signal import resample_poly
            g = gcd(SR, wsr)
            w = resample_poly(w, SR // g, wsr // g)
        w = vo.voice._clone_trim(w)
        cues.append((t, t + len(w) / SR, s))
        track += [w, np.zeros(int(pause * SR))]
        t += len(w) / SR + pause
    track[-1] = np.zeros(int(vo.TAIL * SR))
    audio = np.concatenate(track)
    audio *= 0.89 / max(1e-6, np.abs(audio).max())
    base = os.path.join(ROOT, "out", "voiceover", a.name)
    os.makedirs(os.path.dirname(base), exist_ok=True)
    soundfile.write(base + ".wav", audio, SR, subtype="PCM_16")
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", base + ".wav", "-af", vo.POLISH + ",alimiter=limit=0.89",
                    *vo.CLEAN, base + ".polish.wav"], check=True)
    os.replace(base + ".polish.wav", base + ".wav")
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", base + ".wav", "-c:a", "libmp3lame", "-b:a", "192k",
                    "-write_xing", "0", "-id3v2_version", "0", *vo.CLEAN, base + ".mp3"], check=True)
    with open(base + ".srt", "w", encoding="utf-8") as f:
        for k, (s0, s1, s) in enumerate(cues, 1):
            f.write(f"{k}\n{vo.stamp(s0)} --> {vo.stamp(s1)}\n{s}\n\n")
    print(f"hindi voice-over: {len(lines)} lines, {len(audio) / SR:.1f} s -> {base}.wav / .mp3 / .srt")


if __name__ == "__main__":
    main()
