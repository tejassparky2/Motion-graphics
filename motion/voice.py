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
import glob
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

# Default narrator: the channel owner's own cloned voice (Chatterbox, prompt in assets/voice/owner_prompt.wav).
CLONE_PROMPT = os.path.join(ROOT, "assets", "voice", "owner_prompt.wav")
CLONE_PYTHON = os.environ.get("CLONE_PYTHON", "/home/user/.venv-clone/bin/python")
ENGINE = os.environ.get("NARRATOR_ENGINE", "clone" if os.path.exists(CLONE_PROMPT) else "kokoro")
if ENGINE == "clone":
    # Owner approved the sample and asked for "slightly faster". The clone reads short sentences slowly, so takes
    # play at x1.15 (riddle lines, pace 0.9, at x1.035). Last Bencher Part 2 lands at ~180 wpm with pauses, vs 176
    # for the approved sample. Tempo change keeps the pitch.
    VOICE = "owner-clone"
    SPEED = float(os.environ.get("NARRATOR_SPEED", "1.15"))
elif ENGINE == "kokoro":
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


# Character voices for multi-voice videos: speaker -> dict(voice=<kokoro voice>, speed=1.0, pitch=<semitones>,
# formant="shifted" (cartoon, the default) or "preserved" (a higher but natural-sounding voice)).
# Anyone not listed (and the narrator) uses the main narrator voice: the owner's clone by default.
CAST_VOICES = {}


def configure(voice=None, speed=None, max_pause=None, cast=None, clone_rate=None):
    """Per-video narrator settings (environment variables still win, so you can audition voices).
    `clone_rate`: target syllables/s for the cloned voice in this video (default CLONE_RATE)."""
    global VOICE, SPEED, MAX_PAUSE, CLONE_RATE
    if "CLONE_RATE" not in os.environ:   # reset per video, so one video's pace never leaks into the next
        CLONE_RATE = clone_rate or CLONE_RATE_DEFAULT
    CAST_VOICES.clear()
    CAST_VOICES.update(cast or {})
    if voice and "NARRATOR_VOICE" not in os.environ:
        VOICE = voice
    if speed and "NARRATOR_SPEED" not in os.environ and ENGINE != "clone":   # per-video speeds were tuned for Kokoro
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
PRONOUNCE = {"lakh": "[lakh](/lˈɑːk/)", "emus": "[emus](/ˈimjuz/)", "emu": "[emu](/ˈimju/)",
             "bencher": "[bencher](/bˈɛnʧəɹ/)", "benchers": "[benchers](/bˈɛnʧəɹz/)"}


def _pronounce(text):
    if ENGINE != "kokoro":
        return text
    for word, markup in PRONOUNCE.items():
        text = re.sub(rf"\b{word}\b", markup, text, flags=re.I)
    return text


CLONE_VERSION = "v3"   # bump when the clone generation, pace or tone changes


def _cast_synth(text, pace, who):
    """A character line in a stock Kokoro voice, optionally pitched up/down for a cartoon voice."""
    v = CAST_VOICES[who]
    out = os.path.join(ROOT, "build", "tts", f"{_key(text, pace, who)}.wav")
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        _kokoro_wav(_pronounce(text), v.get("speed", 1.0) * pace, out, voice=v["voice"])
        if v.get("pitch"):
            import imageio_ffmpeg
            tmp = out + ".pitch.wav"
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", out, "-filter:a",
                            f"rubberband=pitch={2 ** (v['pitch'] / 12):.4f}:formant={v.get('formant', 'shifted')}:"
                            f"transients=crisp:pitchq=quality",
                            tmp], check=True)
            os.replace(tmp, out)
    return _squeeze(_trim(_read_wav(out)))


def _key(text, pace=1.0, who=None):
    if who in CAST_VOICES:
        v = CAST_VOICES[who]
        fmt = "" if v.get("formant", "shifted") == "shifted" else f"{v['formant']}|"   # keeps older takes cached
        return hashlib.sha1(f"cast|{v['voice']}|{v.get('speed', 1.0)}|{v.get('pitch', 0)}|{fmt}{pace:.3f}|"
                            f"{_pronounce(text)}".encode()).hexdigest()[:16]
    if text in _EXTERNAL:   # lines cut from an uploaded narration are keyed by that file
        return hashlib.sha1(f"ext|{EXTERNAL_TAG}|{text}".encode()).hexdigest()[:16]
    if ENGINE == "clone":
        return hashlib.sha1(f"clone|{CLONE_VERSION}|{CLONE_RATE}|{pace:.3f}|{text}".encode()).hexdigest()[:16]
    return hashlib.sha1(f"{ENGINE}|{VOICE}|{SPEED * pace:.3f}|{_pronounce(text)}".encode()).hexdigest()[:16]


# ---- narration recorded elsewhere (e.g. the channel owner's own voice clone), uploaded as one file per video
_EXTERNAL = {}     # spoken line text -> wav path cut from the uploaded narration
EXTERNAL_TAG = ""


def use_external(media, lines):
    """Use an uploaded narration (audio or video file) instead of TTS.

    The file is transcribed with word timestamps, aligned to the script, and cut into one clip per line, so the
    rest of the pipeline (trimming, pause squeezing, word timings, captions) works exactly as with TTS.
    Raises if a line can't be found in the recording (e.g. the reader skipped it)."""
    global EXTERNAL_TAG, _whisper
    import imageio_ffmpeg
    tag = hashlib.sha1(open(media, "rb").read()).hexdigest()[:12]
    d = os.path.join(ROOT, "build", "ext", tag)
    os.makedirs(d, exist_ok=True)
    full = os.path.join(d, "full.wav")
    if not os.path.exists(full):
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", media, "-vn", "-ac", "1",
                        "-ar", str(SR), "-c:a", "pcm_s16le", full], check=True)
    a = _read_wav(full)
    words_cache = os.path.join(d, "words.json")
    if os.path.exists(words_cache):
        heard = json.load(open(words_cache))
    else:
        if _whisper is None:
            from faster_whisper import WhisperModel
            _whisper = WhisperModel(os.environ.get("ALIGN_MODEL", "small.en"), device="cpu", compute_type="int8")
        a16 = np.interp(np.arange(int(len(a) * 16000 / SR)) * SR / 16000, np.arange(len(a)), a)
        segs, _ = _whisper.transcribe(a16.astype(np.float32), language="en", word_timestamps=True)
        heard = [(w.word, w.start, w.end) for sg in segs for w in sg.words]
        json.dump(heard, open(words_cache, "w"))
    script, owner = [], []
    for i, line in enumerate(lines):
        for w in line.split():
            script.append(_norm(w))
            owner.append(i)
    got = [_norm(w) for w, _, _ in heard]
    first, last = [None] * len(lines), [None] * len(lines)
    for blk in difflib.SequenceMatcher(None, script, got, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            i = owner[blk.a + k]
            t0, t1 = heard[blk.b + k][1], heard[blk.b + k][2]
            first[i] = t0 if first[i] is None else min(first[i], t0)
            last[i] = t1 if last[i] is None else max(last[i], t1)
    dur = len(a) / SR
    for i in range(len(lines)):   # a line heard differently (e.g. "1925" for "nineteen twenty-five") sits between its neighbours
        if first[i] is None:
            first[i] = last[i - 1] if i and last[i - 1] is not None else 0.0
            nxt = next((first[j] for j in range(i + 1, len(lines)) if first[j] is not None), dur)
            last[i] = max(first[i] + 0.3, nxt - 0.05)
            print(f"narration: no words matched for line {i} ({lines[i]!r}); using the gap", file=sys.stderr)
    prev_end = 0.0
    for i, line in enumerate(lines):
        start = max(prev_end, first[i] - 0.08)
        nxt = first[i + 1] if i + 1 < len(lines) else dur
        end = min(nxt - 0.02, last[i] + 0.25)
        prev_end = end
        _EXTERNAL[line] = os.path.join(d, f"line{i:02d}.wav")
        import soundfile
        soundfile.write(_EXTERNAL[line], a[int(start * SR): int(end * SR)], SR, subtype="PCM_16")
    EXTERNAL_TAG = tag
    return tag


_kokoro = {}


def _kokoro_wav(text, speed, out, voice=None):
    import soundfile
    from scipy.signal import resample_poly
    voice = voice or VOICE
    if voice[0] not in _kokoro:
        from kokoro import KPipeline
        _kokoro[voice[0]] = KPipeline(lang_code=voice[0], repo_id="hexgrad/Kokoro-82M")
    audio = np.concatenate([r.audio.numpy() for r in _kokoro[voice[0]](text, voice=voice, speed=speed)])
    soundfile.write(out, resample_poly(audio, 147, 80), SR, subtype="PCM_16")  # 24 kHz -> 44.1 kHz


def synth(text, pace=1.0, who=None):
    """Speech for one line as float samples at 44.1 kHz, silence-trimmed (cached).

    `pace` scales the speed for this line only (e.g. 0.9 to land a punchline a touch slower).
    `who` picks a character voice from CAST_VOICES; anyone else is the narrator voice."""
    if text in _EXTERNAL:
        return _squeeze(_trim(_read_wav(_EXTERNAL[text])))
    if who in CAST_VOICES:
        return _cast_synth(text, pace, who)
    out = os.path.join(ROOT, "build", "tts", f"{_key(text, pace)}.wav")
    if ENGINE == "clone":
        if not os.path.exists(_clone_raw(text)):
            clone_prefetch([text])
        return _squeeze(_clone_trim(_read_wav(_clone_process(text, pace)[0])))
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


# Pace target: The Teacher Bluffed (owner: "speed similar as the teacher Bluffed video") reads at a median
# 5.2 syllables per second of speech, with lines within ~0.5 of each other.
CLONE_RATE = float(os.environ.get("CLONE_RATE", "5.5"))   # owner: "fast up voice slightly more" (was 5.2)
CLONE_RATE_DEFAULT = CLONE_RATE
# Tone, matched to the narrators in the owner's reference videos (voice separated from music, long-term spectrum):
# the clone was 5-8 dB duller above 2.5 kHz and boomy at 125-160 Hz. So: cut the boom, keep firm bass body at
# ~220 Hz, lift presence and air, then light compression for a punchy, even level.
CLONE_TONE = ("highpass=f=70,"
              "equalizer=f=140:t=q:w=1.2:g=-4,"
              "equalizer=f=230:t=q:w=1.0:g=2,"
              "equalizer=f=3200:t=q:w=1.0:g=4,"
              "equalizer=f=6000:t=q:w=1.0:g=4,"
              "highshelf=f=8500:g=4,"
              "acompressor=threshold=-20dB:ratio=3:attack=5:release=60:makeup=2,"
              "alimiter=limit=0.95")


def syllables(text):
    n = 0
    for w in re.findall(r"[a-z']+", text.lower()):
        g = len(re.findall(r"[aeiouy]+", w))
        if w.endswith("e") and not w.endswith(("le", "ee")) and g > 1:
            g -= 1
        n += max(1, g)
    return n


def speech_secs(a, sr):
    """Seconds of actual speech: silences longer than 120 ms don't count."""
    w = int(0.01 * sr)
    n = len(a) // w
    if n == 0:
        return len(a) / sr
    env = np.abs(a[:n * w]).reshape(n, w).max(1)
    on = env > 0.03 * env.max()
    tot, i = 0, 0
    while i < n:
        j = i
        while j < n and on[j] == on[i]:
            j += 1
        if on[i] or (j - i) < 12:
            tot += j - i
        i = j
    return tot / 100


TEMPO_MIN, TEMPO_MAX = 0.94, 1.15     # bigger stretches smear short words ("blood" -> "black"), even with rubberband


def _clone_process(text, pace):
    """The finished take: nudged toward the target pace (rubberband, crisp mode) and toned. -> (path, final rate)."""
    import imageio_ffmpeg
    import soundfile
    out = os.path.join(ROOT, "build", "tts", f"{_key(text, pace)}.wav")
    r, rsr = soundfile.read(_clone_raw(text))
    rate = syllables(text) / max(0.2, speech_secs(r, rsr))
    tempo = min(TEMPO_MAX, max(TEMPO_MIN, CLONE_RATE * pace / rate))
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        stretch = (f"rubberband=tempo={tempo:.4f}:transients=crisp:detector=compound:phase=laminar:window=short:"
                   f"formant=preserved:pitchq=quality,") if abs(tempo - 1) > 0.005 else ""
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", _clone_raw(text),
                        "-filter:a", stretch + CLONE_TONE, "-ar", str(SR), "-ac", "1", out], check=True)
    return out, rate * tempo


def _clone_trim(a, thresh=0.006, pre=0.035, post=0.05):
    """Tight trim for clone takes: drop the breath/silence the model leaves around a sentence, but keep soft
    first consonants (a looser threshold than _trim, so "Put" doesn't turn into "could")."""
    env = np.convolve(np.abs(a), np.ones(441) / 441, mode="same")
    loud = np.nonzero(env > thresh)[0]
    if not len(loud):
        return a
    return a[max(0, loud[0] - int(pre * SR)): loud[-1] + int(post * SR)]


def _clone_raw(text):
    return os.path.join(ROOT, "build", "clone_tts",
                        hashlib.sha1(f"owner|{CLONE_VERSION}|{text}".encode()).hexdigest()[:16] + ".wav")


# Spellings the clone pronounces more clearly (only what it's told to say; captions keep the real word).
CLONE_SAY = {"bencher": "benchur", "benchers": "benchurs", "Frane": "Frahneh", "Selak": "Sehlahk", "Gabriel's": "Gaybreeul's"}


def _clone_say(text):
    for word, say in CLONE_SAY.items():
        text = re.sub(rf"\b{word}\b", say, text, flags=re.I)
    return text


def clone_prefetch(texts):
    """Generate every missing sentence in one go (the clone model takes ~20 s to load)."""
    if ENGINE != "clone":
        return
    jobs = [[_clone_say(t), _clone_raw(t)] for t in dict.fromkeys(texts)
            if t not in _EXTERNAL and not os.path.exists(_clone_raw(t))]
    if not jobs:
        return
    path = os.path.join(ROOT, "build", "clone_tts", f"jobs_{os.getpid()}.json")   # one per render, so parallel renders never collide
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(jobs, open(path, "w"))
    print(f"clone voice: generating {len(jobs)} sentences", file=sys.stderr, flush=True)
    subprocess.run([CLONE_PYTHON, os.path.join(ROOT, "tools", "clone_tts.py"), path], check=True)


_NUMWORDS = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
                "seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand "
                "million percent point and a".split())
_checker = None


def _heard_ok(text, heard):
    """Same words, allowing numbers heard as digits ("twenty-eight" -> "28")."""
    t = re.sub(r"[^a-z0-9' ]", " ", text.lower().replace("-", " ")).split()
    h = re.sub(r"[^a-z0-9' ]", " ", heard.lower().replace("-", " ")).split()
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, t, h).get_opcodes():
        if op == "equal":
            continue
        if all(w in _NUMWORDS for w in t[i1:i2]) and all(re.fullmatch(r"[0-9%.,]+|and|a", w) for w in h[j1:j2]):
            continue
        return False
    return True


def clone_check(takes, tries=3, slack=0.15):
    """Hear every finished take with Whisper medium. Re-make takes that are misheard or whose pace is more than
    `slack` off the target, and keep the best of `tries`. `takes`: [(text, pace)]."""
    if ENGINE != "clone":
        return
    global _checker
    import shutil
    import soundfile
    takes = list(dict.fromkeys(takes))
    todo = [(t, p) for t, p in takes if t not in _EXTERNAL and not os.path.exists(_clone_raw(t) + ".ok")]
    if not todo:
        return
    if _checker is None:
        from faster_whisper import WhisperModel
        _checker = WhisperModel("medium.en", device="cpu", compute_type="int8")
    best = {}
    for attempt in range(tries):
        bad = []
        for t, p in todo:
            out, rate = _clone_process(t, p)
            a, sr = soundfile.read(out)
            a = np.concatenate([np.zeros(sr // 2), a, np.zeros(sr // 2)])
            a16 = np.interp(np.arange(int(len(a) * 16000 / sr)) * sr / 16000, np.arange(len(a)), a).astype(np.float32)
            segs = list(_checker.transcribe(a16, language="en", beam_size=5, word_timestamps=True)[0])
            heard = " ".join(x.text.strip() for x in segs)
            probs = [w.probability for x in segs for w in x.words]
            off = abs(rate / (CLONE_RATE * p) - 1)
            score = (_heard_ok(t, heard), off <= slack, -off, float(np.mean(probs)) if probs else 0.0)
            keep = f"{_clone_raw(t)}.try{attempt}.wav"
            shutil.copy(_clone_raw(t), keep)
            if t not in best or score > best[t][0]:
                best[t] = (score, keep, heard, p)
            if not (score[0] and score[1]):
                bad.append((t, p))
        print(f"clone check {attempt + 1}/{tries}: {len(todo) - len(bad)}/{len(todo)} takes clear and on pace",
              file=sys.stderr, flush=True)
        if not bad or attempt == tries - 1:
            break
        for t, p in bad:
            os.remove(_clone_raw(t))
            for pc in (p, 1.0, 0.9):
                f = os.path.join(ROOT, "build", "tts", f"{_key(t, pc)}.wav")
                if os.path.exists(f):
                    os.remove(f)
        clone_prefetch([t for t, _ in bad])
        todo = bad
    for t, (score, keep, heard, p) in best.items():
        shutil.copy(keep, _clone_raw(t))
        for pc in (p, 1.0, 0.9):   # rebuild the finished take from the chosen raw one
            for f in glob.glob(os.path.join(ROOT, "build", "tts", f"{_key(t, pc)}*")):
                os.remove(f)
        open(_clone_raw(t) + ".ok", "w").write(heard)
        if not score[0]:
            print(f"clone check: still unclear after {tries} tries: {t!r} heard as {heard!r}", file=sys.stderr)


_whisper = None


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def word_times(text, audio, pace=1.0, who=None):
    """[(start, end)] for each whitespace-separated word of `text`, relative to the start of `audio`.

    Whisper's timestamps are matched to the script by sequence alignment; words Whisper heard differently
    (e.g. "seventy" -> "70") get times interpolated from their neighbours by character length.
    """
    cache = os.path.join(ROOT, "build", "tts", f"{_key(text, pace, who)}.p{MAX_PAUSE}.words.json")
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
