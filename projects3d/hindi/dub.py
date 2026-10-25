"""Hindi dub of a testimonial in the speaker's own cloned voice (only with her consent), one clip per line.

  python projects3d/hindi/dub.py projects3d/hindi/reel05/dub.txt reel05 --voice sowmya --prompt PROMPT.wav [--picks P]

dub.txt: one paragraph per segment of the English reel, in the same order (Devanagari, so English words come out the
Indian way). Each line is made up to 3 times and heard back with Whisper medium (Hindi); the clearest take is kept
(--picks {"line": take} overrides by ear). Writes out/3d/hindi/dub/NAME_NN.wav (48 kHz mono, trimmed, polished).
Chatterbox's Perth watermark is left in place. The prompt and the dub stay out of git (out/3d/ is ignored).
"""
import argparse
import difflib
import json
import os
import subprocess
import sys

import soundfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import hindi_voiceover as hv     # noqa: E402


def best_prefix(script, heard):
    """How many heard words make up the script line: the prefix most like the script (ties: the shorter one)."""
    target = "".join(hv._words(script))
    n = len(hv._words(script))
    best, k_best = -1.0, len(heard)
    for k in range(max(1, n - 3), min(len(heard), n + 3) + 1):
        r = difflib.SequenceMatcher(None, target, "".join(hv._words(" ".join(heard[:k])))).ratio()
        if r > best + 1e-6:
            best, k_best = r, k
    # Whisper wrote the line mostly in Latin letters (Hinglish): no reliable match, keep every heard word
    return k_best if best >= 0.45 else len(heard)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("script")
    ap.add_argument("name")
    ap.add_argument("--voice", required=True)
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--picks")
    a = ap.parse_args()
    lines = [s for s, _ in hv.vo.paragraphs(open(a.script, encoding="utf-8").read(), 0.0)]
    picks = {int(k): v for k, v in json.load(open(a.picks)).items()} if a.picks else {}
    got = {s: os.path.join(ROOT, "build", "mtl", f"{hv.vo.voice._key(s)}.{a.voice}.hi.try{picks[i + 1]}.wav")
           for i, s in enumerate(lines) if i + 1 in picks}
    got.update(hv.takes([s for i, s in enumerate(lines) if i + 1 not in picks], prompt=a.prompt, voice=a.voice))
    out = os.path.join(ROOT, "out", "3d", "hindi", "dub")
    os.makedirs(out, exist_ok=True)
    from faster_whisper import WhisperModel
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    for i, s in enumerate(lines):
        w, sr = soundfile.read(got[s])
        w = w if w.ndim == 1 else w.mean(axis=1)
        # the multilingual model sometimes keeps babbling (loudly, even word-like) after the sentence: keep only the
        # heard words that best match the script line and cut 0.2 s after them, then trim quiet edges
        words = [x for seg in model.transcribe(got[s], language="hi", word_timestamps=True)[0] for x in seg.words]
        if words:
            k = best_prefix(s, [x.word for x in words])
            w = w[: int(min(len(w) / sr, words[k - 1].end + 0.2) * sr)]
        w = hv.speech_only(w, sr)
        raw = os.path.join(out, f"{a.name}_{i + 1:02d}.raw.wav")
        soundfile.write(raw, w, sr)
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-af", hv.vo.POLISH + ",alimiter=limit=0.89",
                        "-ar", "48000", "-ac", "1", *hv.vo.CLEAN, os.path.join(out, f"{a.name}_{i + 1:02d}.wav")],
                       check=True)
        os.remove(raw)
        print(f"{a.name}_{i + 1:02d}: {len(w) / sr:.2f} s  {s}")


if __name__ == "__main__":
    main()
