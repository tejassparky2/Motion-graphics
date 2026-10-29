"""Narration for the Hinglish channel: one TTS take per script line, cached, trimmed, laid end to end with short
pauses, plus word times so on-screen words can land on the spoken word.

Engines (pick per video with NARRATOR = dict(engine=..., ...)):
- edge:   Microsoft neural voices via edge-tts (placeholder while the owner picks a voice; for a monetized channel
          the same voices go through Azure Speech). Word times come from the service's word boundaries.
- sarvam: Sarvam Bulbul (needs SARVAM_API_KEY). Word times are spread by character position.
- eleven: ElevenLabs (needs ELEVENLABS_API_KEY). Word times are spread by character position.
Never a clone of a real person.
"""
import asyncio
import base64
import hashlib
import io
import json
import os
import subprocess
import urllib.request
import wave

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
CACHE = os.path.join(ROOT, "build", "hinglish", "tts")
SR = 44100
LEAD = 0.10        # first word lands this early (his reels speak from ~0.08 s)
# Pauses between lines, from Whisper word timings of the reference reels (pace_measure.py, 29 Oct 2026): sentence
# pauses 0.50-0.61 s median. Our takes keep ~0.07 s of trimmed edge, so the added gap is a little shorter.
GAP = 0.43         # silence between two lines
QGAP = 0.53        # after a question
TAIL = 0.8         # after the last line


ENV_FILES = [os.path.join(os.path.dirname(ROOT), ".env"),   # <shorts research>\.env, outside the public repo
             os.path.join(ROOT, ".env")]                    # git-ignored fallback


def _key(name):
    """A secret from the environment, the Windows user environment, or a KEY=value line in a .env file.
    Never printed or logged."""
    if os.environ.get(name):
        return os.environ[name]
    try:
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, name)[0]
    except OSError:
        pass
    for f in ENV_FILES:
        if os.path.exists(f):
            for line in open(f, encoding="utf-8-sig"):
                k, sep, v = line.strip().partition("=")
                if sep and k.strip().removeprefix("export ").strip() == name:
                    return v.strip().strip("'\"") or None
    return None


def _decode(data):
    """Any audio bytes -> float mono at SR via ffmpeg."""
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-i", "pipe:0", "-ac", "1", "-ar", str(SR),
                        "-f", "f32le", "pipe:1"], input=data, capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32).astype(np.float64)


def _edge(text, cfg):
    import edge_tts

    async def run():
        com = edge_tts.Communicate(text, cfg.get("voice", "hi-IN-MadhurNeural"), rate=cfg.get("rate", "+35%"),
                                   boundary="WordBoundary")
        audio, words = bytearray(), []
        async for ch in com.stream():
            if ch["type"] == "audio":
                audio += ch["data"]
            elif ch["type"] == "WordBoundary":
                words.append((ch["text"], ch["offset"] / 1e7, ch["duration"] / 1e7))
        return bytes(audio), words
    return asyncio.run(run())


def _post(url, headers, body):
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={**headers, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def _sarvam(text, cfg):
    k = _key("SARVAM_API_KEY")
    if not k:
        raise RuntimeError("SARVAM_API_KEY is not set")
    r = json.loads(_post("https://api.sarvam.ai/text-to-speech", {"api-subscription-key": k},
                         {"text": text, "language_code": "hi-IN", "speaker": cfg["speaker"],
                          "model": cfg.get("model", "bulbul:v3"), "pace": cfg.get("pace", 1.0),
                          "speech_sample_rate": 44100}))
    return base64.b64decode(r["audios"][0]), None


def _eleven(text, cfg):
    k = _key("ELEVENLABS_API_KEY")
    if not k:
        raise RuntimeError("ELEVENLABS_API_KEY is not set")
    audio = _post(f"https://api.elevenlabs.io/v1/text-to-speech/{cfg['voice_id']}?output_format=mp3_44100_128",
                  {"xi-api-key": k}, {"text": text, "model_id": cfg.get("model", "eleven_v3")})
    return audio, None


PARLER_PY = os.path.join(os.path.dirname(ROOT), ".venv-parler", "Scripts", "python.exe")


def _parler_batch(jobs, cfg):
    """Voice [(text, wav_path), ...] in one run of parler_say.py (the model loads once)."""
    spec = {"description": cfg["description"], "seed": cfg["seed"], "jobs": [{"text": t, "out": o} for t, o in jobs]}
    subprocess.run([PARLER_PY, "-I", "-X", "utf8", "-W", "ignore", os.path.join(HERE, "parler_say.py")],
                   input=json.dumps(spec, ensure_ascii=False).encode("utf-8"), check=True)


def _raw_path(text, cfg):
    """Raw engine output, keyed only by what changes the generated voice (not by pace or the studio chain)."""
    gen = {k: v for k, v in cfg.items() if k not in ("studio", "pace_wps", "pitch_expand", "tempo")}
    return os.path.join(CACHE, f"raw_{_hash(text, gen)}.wav")


def pace(a, text, target_wps, max_pause=0.3, keep_pause=0.24, fixed_tempo=None):
    """Match the reference delivery (owner, 29 Oct 2026: "match voice speech pace all to mayank"): shorten pauses
    inside a line longer than `max_pause` to `keep_pause`, then time-stretch (rubberband, pitch kept) so the words per
    second of the whole line equal `target_wps`. The stretch is limited to 0.85-1.35x so it never sounds processed."""
    hop = int(0.02 * SR)
    env = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, mode="same"))
    quiet = env < max(1e-4, env.max() * 0.02)
    out, i, n = [], 0, len(a)
    while i < n:                                   # squeeze long internal silences
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            seg = a[i:j]
            if (j - i) / SR > max_pause and 0 < i and j < n:
                k = int(keep_pause * SR / 2)
                seg = np.concatenate([seg[:k], seg[-k:]])
            out.append(seg)
            i = j
        else:
            j = i
            while j < n and not quiet[j]:
                j += 1
            out.append(a[i:j])
            i = j
    a = np.concatenate(out)
    # whole-line rate (words / take length), the same way the reference's 198-200 wpm (3.3 w/s) was measured; an
    # energy-gated "speaking time" undercounts quiet consonants and made lines slower instead of faster
    if fixed_tempo:
        # one factor for the whole video (owner, 29 Oct 2026: "somewhere too fast and some too slow", robotic): per-line
        # word-rate targets pushed lines with long English/science words to 1.35x and slowed short-word lines to 0.88x
        tempo = float(fixed_tempo)
    else:
        words = len([w for w in text.replace("...", " ").split() if any(ch.isalnum() for ch in w)])
        rate = words / max(0.3, len(a) / SR)
        tempo = float(np.clip(target_wps / rate, 0.85, 1.35)) if rate > 0 else 1.0
    if abs(tempo - 1) < 0.02:
        return a
    # small changes: WSOLA atempo is the most natural on speech; bigger ones need rubberband
    filt = (f"atempo={tempo:.4f}" if abs(tempo - 1) <= 0.15
            else f"rubberband=tempo={tempo:.4f}:transients=mixed:formant=preserved")
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1",
                        "-i", "pipe:0", "-af", filt, "-f", "f32le", "pipe:1"],
                       input=a.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32).astype(np.float64)


def expand_pitch(a, up=1.5, down=1.3):
    """Widen the intonation of a take (research, 29 Oct 2026: description wording leaves our narrator at ~13-16 st of
    pitch range; lively documentary narration runs ~20-25 st). Praat PSOLA: every pitch point moves away from the
    take's median in the log domain, by `up` above it and the gentler `down` below it (deep lows turn creaky).
    Duration, timing and the voice's spectral character are kept."""
    import parselmouth
    from parselmouth.praat import call
    snd = parselmouth.Sound(a.astype(np.float64), sampling_frequency=SR)
    f0 = snd.to_pitch(time_step=0.01, pitch_floor=70, pitch_ceiling=450).selected_array["frequency"]
    f0 = f0[f0 > 0]
    if len(f0) < 10:
        return a
    m = float(np.median(f0))
    manip = call(snd, "To Manipulation", 0.01, 70, 450)
    tier = call(manip, "Extract pitch tier")
    call(tier, "Formula", f"if self > {m} then {m} * (self / {m}) ^ {up} else {m} * (self / {m}) ^ {down} fi")
    call([tier, manip], "Replace pitch tier")
    out = call(manip, "Get resynthesis (overlap-add)").values[0]
    return out.astype(np.float64)


VOICE_EQ = os.path.join(HERE, "voice_eq.json")


def studio(a, version):
    """Studio narration chain (owner, 29 Oct 2026: "give voice a studio effect like mayank"): light denoise,
    75 Hz high-pass, the EQ measured to move our voice toward his narration's tonal balance (voice_match.py),
    narrator compression, de-essing and a peak limiter. `version` only names the chain for the cache key."""
    eq = json.load(open(VOICE_EQ))
    entries = ";".join(f"entry({f},{g})" for f, g in zip(eq["bands_hz"], eq["gain_db"]))
    if version in ("v1", "v2"):
        comp = "acompressor=threshold=-22dB:ratio=3:attack=5:release=70:makeup=3dB"
    else:
        # v3 (research, 29 Oct 2026): the fast 3:1 squashed syllables (speech spread 7.2 dB vs ~9.5 in the reference);
        # speech engineering guidance is ~2:1, 15-30 ms attack, 150-250 ms release, RMS detection, 2-4 dB reduction
        peak = np.abs(a).max()
        a = a * (10 ** (-3 / 20) / peak) if peak > 0 else a      # same input level for every take
        comp = "acompressor=threshold=-20dB:ratio=2:attack=20:release=200:detection=rms:knee=4:makeup=2dB"
    chain = ",".join([
        "afftdn=nf=-38",                                   # gentle: a stronger setting dulled the 5-9 kHz range
        "highpass=f=75",
        f"firequalizer=gain_entry='{entries}'",
        comp,
        "deesser=i=0.25:m=0.5:f=0.5",                      # light: v1's 0.5 cut the presence the EQ adds
        "alimiter=limit=0.89:level=false",
    ])
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1",
                        "-i", "pipe:0", "-af", chain, "-f", "f32le", "pipe:1"],
                       input=a.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32).astype(np.float64)


def _parler(text, cfg):
    raw = _raw_path(text, cfg)
    if not os.path.exists(raw):
        _parler_batch([(text, raw)], cfg)
    return open(raw, "rb").read(), None


F5_PY = os.path.join(os.path.dirname(ROOT), "tools", ".venv-f5", "Scripts", "python.exe")


def _f5_batch(jobs, cfg):
    """Voice [(text, wav_path), ...] with IndicF5 in one run of f5_say.py, from the channel voice's reference prompt
    (cfg ref_audio / ref_text). IndicF5 samples noise each run, so a different `take` gives a different reading."""
    spec = {"ref_audio": cfg["ref_audio"], "ref_text": cfg["ref_text"], "jobs": [{"text": t, "out": o} for t, o in jobs]}
    subprocess.run([F5_PY, "-I", "-X", "utf8", "-W", "ignore", os.path.join(HERE, "f5_say.py")],
                   input=json.dumps(spec, ensure_ascii=False).encode("utf-8"), check=True)


def _f5(text, cfg):
    raw = _raw_path(text, cfg)
    if not os.path.exists(raw):
        _f5_batch([(text, raw)], cfg)
    return open(raw, "rb").read(), None


BATCH = {"parler": _parler_batch, "f5": _f5_batch}
ENGINES = {"edge": _edge, "sarvam": _sarvam, "eleven": _eleven, "parler": _parler, "f5": _f5}


def _hash(text, cfg):
    return hashlib.sha1(json.dumps([cfg, text], ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]


def prefetch(script, cfg):
    """Engines that load a big model (parler, f5) voice every uncached line in one batch."""
    if cfg["engine"] not in BATCH:
        return
    os.makedirs(CACHE, exist_ok=True)
    jobs = [(l["text"], _raw_path(l["text"], cfg)) for l in script
            if not os.path.exists(os.path.join(CACHE, f"{_hash(l['text'], cfg)}.wav"))
            and not os.path.exists(_raw_path(l["text"], cfg))]
    if jobs:
        BATCH[cfg["engine"]](jobs, cfg)


def _trim(a, thresh=0.012):
    loud = np.flatnonzero(np.abs(a) > thresh)
    if not len(loud):
        return a, 0.0
    i0 = max(0, loud[0] - int(0.02 * SR))
    i1 = min(len(a), loud[-1] + int(0.05 * SR))
    return a[i0:i1], i0 / SR


def take(text, cfg):
    """(samples, [(word, start, dur)] or None) for one line, cached by engine settings + text."""
    os.makedirs(CACHE, exist_ok=True)
    h = _hash(text, cfg)
    wav, meta = os.path.join(CACHE, f"{h}.wav"), os.path.join(CACHE, f"{h}.json")
    if not os.path.exists(wav):
        data, words = ENGINES[cfg["engine"]](text, cfg)
        a, off = _trim(_decode(data))
        if cfg.get("pitch_expand"):
            a = expand_pitch(a, *cfg["pitch_expand"])
        if cfg.get("pace_wps") or cfg.get("tempo"):
            a = pace(a, text, cfg.get("pace_wps"), fixed_tempo=cfg.get("tempo"))
            words = None                                   # boundaries no longer line up after the stretch
        if cfg.get("studio"):
            a = studio(a, cfg["studio"])
        if words:
            words = [(w, max(0.0, s - off), d) for w, s, d in words]
        with wave.open(wav, "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(SR)
            f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())
        json.dump({"text": text, "words": words}, open(meta, "w", encoding="utf-8"), ensure_ascii=False)
    with wave.open(wav) as f:
        a = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float64) / 32767
    return a, json.load(open(meta, encoding="utf-8"))["words"], wav


class Beat:
    def __init__(self, id, text, start, dur, words, wav):
        self.id, self.text, self.start, self.dur, self.words, self.wav = id, text, start, dur, words, wav
        self.end = start + dur

    def at(self, word=None, frac=None):
        """Time a word starts (first word containing `word`), or a fraction of the way through the line."""
        if word is not None:
            if self.words:
                for w, s, _ in self.words:
                    if word in w:
                        return self.start + s
            i = self.text.find(word)
            if i >= 0:
                return self.start + self.dur * i / max(1, len(self.text))
            raise KeyError(f"{word!r} not in line {self.id}")
        return self.start + self.dur * (frac or 0.0)


class Timeline:
    def __init__(self, script, cfg, tail=TAIL):
        self.beats, self.by_id, self._clips = [], {}, []
        prefetch(script, cfg)
        t = LEAD
        for i, line in enumerate(script):
            a, words, wav = take(line["text"], cfg)
            b = Beat(line["id"], line["text"], t, len(a) / SR, words, wav)
            self.beats.append(b)
            self.by_id[b.id] = b
            self._clips.append((t, a))
            last = i == len(script) - 1
            t = b.end + (tail if last else line.get("gap", QGAP if line["text"].rstrip().endswith("?") else GAP))
        self.total = t

    def __getitem__(self, k):
        return self.by_id[k]

    def clips(self):
        return self._clips

    def to_json(self):
        return {"total": self.total, "beats": [dict(id=b.id, text=b.text, start=b.start, dur=b.dur, words=b.words,
                                                     wav=b.wav) for b in self.beats]}

    @classmethod
    def from_json(cls, d):
        tl = cls.__new__(cls)
        tl.beats = [Beat(x["id"], x["text"], x["start"], x["dur"], x["words"], x["wav"]) for x in d["beats"]]
        tl.by_id = {b.id: b for b in tl.beats}
        tl.total, tl._clips = d["total"], None
        return tl
