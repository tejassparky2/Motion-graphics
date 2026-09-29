"""Voice-over narration (offline neural text-to-speech) + word timings.

Engines:
- kokoro (default): Kokoro-82M (Apache-2.0), noticeably more natural and expressive. Default voice `am_michael`,
  chosen by measurement: 100% Whisper intelligibility at ~225 wpm, and pitch variation (3.7 st SD, 8.8 st range)
  close to the reference creator's narrator (3.1 st, 8.0 st). No watermarking in its code.
- piper: the earlier Piper voice (`NARRATOR_ENGINE=piper`).

- Models download on first use (Kokoro from Hugging Face; Piper into build/voices/).
- Every line is cached in build/tts/ so re-renders only synthesize lines that changed.
- Leading/trailing silence is trimmed so lines can be butted together with tight, controlled gaps.
- Word timestamps come from running faster-whisper over the synthesized audio (also cached), so on-screen
  numbers and captions land on the spoken word.
"""
import difflib
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request
import wave

import numpy as np

from .engine import ROOT

ENGINE = os.environ.get("NARRATOR_ENGINE", "kokoro")
if ENGINE == "kokoro":
    # Channel default narrator: am_fenrir, the stock voice measured closest to the reference narrator the user chose
    # (speaker similarity 0.72, the best of 12; median pitch 142 vs 154 Hz; pitch SD 5.0 vs 6.4 semitones).
    # Speed 0.95 lands at ~200 wpm overall in a finished video (the reference narrator: 167 overall, 190 while
    # speaking), a little brisker than the reference to keep the retention-friendly pace.
    # Videos can override via NARRATOR in their module.
    VOICE = os.environ.get("NARRATOR_VOICE", "am_fenrir")
    SPEED = float(os.environ.get("NARRATOR_SPEED", "0.95"))
else:
    VOICE = os.environ.get("NARRATOR_VOICE", "en_US-ryan-high")
    # Piper length scale: <1 speaks faster. 0.8 lands the ryan voice at ~230 wpm.
    SPEED = 1 / float(os.environ.get("NARRATOR_PACE", "0.8"))
VOICE_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main"
SR = 44100
TRIM_PAD = 0.02  # seconds of room kept around each trimmed line
MAX_PAUSE = 0.3  # pauses inside a line are shortened to this (the reference narrator's breaths are ~0.32 s)


def configure(voice=None, speed=None, max_pause=None):
    """Per-video narrator settings (environment variables still win, so you can audition voices)."""
    global VOICE, SPEED, MAX_PAUSE
    if voice and "NARRATOR_VOICE" not in os.environ:
        VOICE = voice
    if speed and "NARRATOR_SPEED" not in os.environ:
        SPEED = speed
    if max_pause is not None:
        MAX_PAUSE = max_pause


def _voice_path():
    d = os.path.join(ROOT, "build", "voices")
    os.makedirs(d, exist_ok=True)
    model = os.path.join(d, f"{VOICE}.onnx")
    lang, name, quality = VOICE.split("-")  # piper voice names look like en_US-ryan-high
    url = f"{VOICE_BASE}/{lang.split('_')[0]}/{lang}/{name}/{quality}/{VOICE}.onnx"
    for path, src in ((model, url), (model + ".json", url + ".json")):
        if not os.path.exists(path):
            print(f"downloading {os.path.basename(path)}", file=sys.stderr)
            urllib.request.urlretrieve(src, path + ".part")
            os.replace(path + ".part", path)
    return model


def _read_wav(path):
    with wave.open(path) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float64) / 32767
        if w.getnchannels() == 2:
            a = a[::2]
    if sr != SR:
        a = np.interp(np.arange(int(len(a) * SR / sr)) * sr / SR, np.arange(len(a)), a)
    return a


def _trim(a):
    env = np.convolve(np.abs(a), np.ones(441) / 441, mode="same")
    loud = np.nonzero(env > 0.012)[0]
    if not len(loud):
        return a
    pad = int(TRIM_PAD * SR)
    return a[max(0, loud[0] - pad): loud[-1] + pad]


def _squeeze(a):
    """Shorten any internal silence longer than MAX_PAUSE (like a jump-cut editor removing dead air)."""
    win = int(0.01 * SR)
    n = len(a) // win
    if n < 3:
        return a
    env = np.abs(a[: n * win]).reshape(n, win).max(axis=1)
    quiet = env < 0.02
    keep = np.ones(len(a), bool)
    limit = int(MAX_PAUSE / 0.01)
    i = 0
    while i < n:
        if not quiet[i]:
            i += 1
            continue
        j = i
        while j < n and quiet[j]:
            j += 1
        if j - i > limit:
            cut0 = i + limit // 2
            cut1 = j - (limit - limit // 2)
            keep[cut0 * win: cut1 * win] = False
        i = j
    return a[keep]


# Pronunciation fixes for words the English voices don't know (Kokoro/misaki phoneme markup).
# "lakh" defaults to a short "lock"; Indian English says "laakh" with a long vowel.
PRONOUNCE = {"lakh": "[lakh](/lˈɑːk/)"}


def _pronounce(text):
    if ENGINE != "kokoro":
        return text
    for word, markup in PRONOUNCE.items():
        text = re.sub(rf"\b{word}\b", markup, text, flags=re.I)
    return text


def _key(text, pace=1.0):
    return hashlib.sha1(f"{ENGINE}|{VOICE}|{SPEED * pace:.3f}|{_pronounce(text)}".encode()).hexdigest()[:16]


_kokoro = {}


def _kokoro_wav(text, speed, out):
    import soundfile
    from scipy.signal import resample_poly
    if VOICE[0] not in _kokoro:
        from kokoro import KPipeline
        _kokoro[VOICE[0]] = KPipeline(lang_code=VOICE[0], repo_id="hexgrad/Kokoro-82M")
    audio = np.concatenate([r.audio.numpy() for r in _kokoro[VOICE[0]](text, voice=VOICE, speed=speed)])
    soundfile.write(out, resample_poly(audio, 147, 80), SR, subtype="PCM_16")  # 24 kHz -> 44.1 kHz


def synth(text, pace=1.0):
    """Speech for one line as float samples at 44.1 kHz, silence-trimmed (cached).

    `pace` scales the speed for this line only (e.g. 0.9 to land a punchline a touch slower)."""
    out = os.path.join(ROOT, "build", "tts", f"{_key(text, pace)}.wav")
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if ENGINE == "kokoro":
            _kokoro_wav(_pronounce(text), SPEED * pace, out)
        else:
            model = _voice_path()
            subprocess.run([sys.executable, "-m", "piper", "-m", model, "-f", out,
                            "--length-scale", str(1 / (SPEED * pace))],
                           input=text.encode(), check=True, stderr=subprocess.DEVNULL)
    return _squeeze(_trim(_read_wav(out)))


_whisper = None


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def word_times(text, audio, pace=1.0):
    """[(start, end)] for each whitespace-separated word of `text`, relative to the start of `audio`.

    Whisper's timestamps are matched to the script by sequence alignment; words Whisper heard differently
    (e.g. "seventy" -> "70") get times interpolated from their neighbours by character length.
    """
    cache = os.path.join(ROOT, "build", "tts", f"{_key(text, pace)}.p{MAX_PAUSE}.words.json")
    if os.path.exists(cache):
        return [tuple(x) for x in json.load(open(cache))]
    global _whisper
    if _whisper is None:
        from faster_whisper import WhisperModel
        _whisper = WhisperModel(os.environ.get("ALIGN_MODEL", "small.en"), device="cpu", compute_type="int8")
    a16 = np.interp(np.arange(int(len(audio) * 16000 / SR)) * SR / 16000, np.arange(len(audio)), audio)
    segs, _ = _whisper.transcribe(a16.astype(np.float32), language="en", word_timestamps=True,
                                  initial_prompt=text)
    heard = [(w.word, w.start, w.end) for s in segs for w in s.words]
    script = text.split()
    a = [_norm(w) for w in script]
    b = [_norm(w) for w, _, _ in heard]
    times = [None] * len(script)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = (heard[blk.b + k][1], heard[blk.b + k][2])
    dur = len(audio) / SR
    i = 0
    while i < len(script):
        if times[i] is not None:
            i += 1
            continue
        j = i
        while j < len(script) and times[j] is None:
            j += 1
        t0 = times[i - 1][1] if i > 0 else 0.0
        t1 = times[j][0] if j < len(script) else dur
        weights = [max(1, len(a[k])) for k in range(i, j)]
        tot = sum(weights)
        acc = t0
        for k, wgt in zip(range(i, j), weights):
            span = (t1 - t0) * wgt / tot
            times[k] = (acc, acc + span)
            acc += span
        i = j
    json.dump(times, open(cache, "w"))
    return times


def narration_track(clips, total):
    """Mix [(start, samples)] into one track. Returns (track, speaking) — speaking is a 0..1 ducking envelope."""
    track = np.zeros(int(total * SR))
    for at, clip in clips:
        i = int(at * SR)
        clip = clip[: max(0, len(track) - i)]
        track[i:i + len(clip)] += clip
    env = (np.abs(track) > 0.01).astype(np.float64)
    k = int(0.3 * SR)  # ~300 ms release so the music doesn't pump between words
    env = np.convolve(env, np.ones(k) / k, mode="same")
    return track, np.clip(env * 4, 0, 1)
