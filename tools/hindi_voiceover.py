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


# Whisper writes some words in Latin or digits; aspiration and a few vowel/voicing spellings vary in its Hindi output
LATIN = {"whatsapp": "व्हाट्सऐप", "dm": "डी एम", "3d": "थ्री डी", "3599": "तीन हज़ार पाँच सौ निन्यानवे",
         "35": "थर्टी फ़ाइव", "99": "नाइंटी नाइन", "1": "वन"}
SAME = str.maketrans({"भ": "ब", "छ": "च", "ध": "त", "थ": "त", "ठ": "ट", "ख": "क", "घ": "ग", "झ": "ज", "ढ": "त",
                      "ष": "स", "श": "स", "ी": "ि", "ू": "ु", "ं": "", "ँ": "", "ृ": "र", "ऐ": "ै",
                      "ड": "त", "ट": "त", "द": "त"})


def _words(s):
    s = re.sub(r"[।.,?!'\"“”‘’\-–—:;]", " ", s.lower())
    s = " " + " ".join(LATIN.get(w, w) for w in s.split()) + " "
    s = re.sub(r"ये(?=\s|$)", "ए", s.replace("\u093c", "").replace(" यह ", " ये "))   # चाहिये = चाहिए; यह = ये
    return [re.sub(r"य$", "ए", w).translate(SAME) for w in s.split()]


def misheard(text, heard, need=0.78):
    """Script words with no close match in what Whisper heard, in order (empty = clear)."""
    a, b = _words(text), _words(heard)
    bad, j = [], 0
    for w in a:
        best, at = 0.0, j
        for k in range(max(0, j - 2), min(len(b), j + 4)):
            r = difflib.SequenceMatcher(None, w, b[k]).ratio()
            if r > best:
                best, at = r, k
        if best < need:
            bad.append(w)
        else:
            j = at + 1
    return bad


def heard_ok(text, heard, need=0.82):
    a, b = "".join(_words(text)), "".join(_words(heard))
    return difflib.SequenceMatcher(None, a, b).ratio() >= need and not misheard(text, heard)


def speech_only(w, sr, rel=0.12, keep=0.12):
    """Cut the faint murmur Chatterbox Multilingual often leaves after (or before) the words: keep from the first to
    the last 20 ms window louder than `rel` of the take's peak, plus `keep` seconds, with a short fade."""
    hop = int(0.02 * sr)
    env = np.array([np.sqrt(np.mean(w[i:i + hop] ** 2)) for i in range(0, len(w) - hop, hop)])
    loud = np.flatnonzero(env > rel * env.max())
    a, b = max(0, (loud[0] * hop) - int(keep * sr)), min(len(w), (loud[-1] + 1) * hop + int(keep * sr))
    w = w[a:b].copy()
    f = int(0.03 * sr)
    w[-f:] *= np.linspace(1, 0, f)
    return w


def takes(texts, lang="hi", tries=3, prompt=None, voice="owner"):
    """Takes in `voice` (cache tag) cloned from `prompt` (default: the owner's prompt), Whisper-checked."""
    from faster_whisper import WhisperModel
    d = os.path.join(ROOT, "build", "mtl")
    os.makedirs(d, exist_ok=True)
    clone_py = os.environ.get("CLONE_PYTHON", os.path.expanduser("~/.venv-clone/bin/python"))
    checker, chosen, score, todo = None, {}, {}, list(dict.fromkeys(texts))
    for n in range(tries):
        tag = "" if voice == "owner" else f".{voice}"
        jobs = [[t, os.path.join(d, f"{vo.voice._key(t)}{tag}.{lang}.try{n}.wav")] for t in todo]
        if any(not os.path.exists(o) for _, o in jobs):
            json.dump(jobs, open(os.path.join(d, "jobs.json"), "w"), ensure_ascii=False)
            subprocess.run([clone_py, os.path.join(ROOT, "tools", "mtl_clone_tts.py"), os.path.join(d, "jobs.json"),
                            "--lang", lang] + (["--prompt", prompt] if prompt else []), check=True)
        checker = checker or WhisperModel("medium", device="cpu", compute_type="int8")
        bad = []
        for t, o in jobs:
            heard = " ".join(x.text for x in checker.transcribe(o, language=lang, beam_size=5)[0])
            ok = heard_ok(t, heard)
            miss = 0 if ok else 1 + len(misheard(t, heard))
            if t not in chosen or miss < score[t]:      # a clear take wins, else the one with fewest misheard words
                chosen[t], score[t] = o, miss
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
    ap.add_argument("--picks", help='JSON {"line number": take number}: takes chosen by ear/transcript (Whisper often '
                                    "writes Hinglish in Latin letters, which the automatic check can't compare)")
    a = ap.parse_args()
    lines = vo.paragraphs(open(a.script, encoding="utf-8").read(), a.gap)
    picks = {int(k): v for k, v in json.load(open(a.picks)).items()} if a.picks else {}
    got = {s: os.path.join(ROOT, "build", "mtl", f"{vo.voice._key(s)}.{a.lang}.try{picks[i + 1]}.wav")
           for i, (s, _) in enumerate(lines) if i + 1 in picks}
    got.update(takes([s for i, (s, _) in enumerate(lines) if i + 1 not in picks], a.lang))
    track, cues, t = [np.zeros(int(vo.LEAD * SR))], [], vo.LEAD
    for s, pause in lines:
        w, wsr = soundfile.read(got[s])
        w = speech_only(w if w.ndim == 1 else w.mean(axis=1), wsr)
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
