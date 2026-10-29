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
    gen = {k: v for k, v in cfg.items() if k not in ("studio", "pace_wps")}
    return os.path.join(CACHE, f"raw_{_hash(text, gen)}.wav")


def pace(a, text, target_wps, max_pause=0.3, keep_pause=0.24):
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
    words = len([w for w in text.replace("...", " ").split() if any(ch.isalnum() for ch in w)])
    rate = words / max(0.3, len(a) / SR)
    tempo = float(np.clip(target_wps / rate, 0.85, 1.35)) if rate > 0 else 1.0
    if abs(tempo - 1) < 0.02:
        return a
    p = subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1",
                        "-i", "pipe:0", "-af", f"rubberband=tempo={tempo:.4f}:transients=crisp:formant=preserved",
                        "-f", "f32le", "pipe:1"], input=a.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32).astype(np.float64)


VOICE_EQ = os.path.join(HERE, "voice_eq.json")


def studio(a, version):
    """Studio narration chain (owner, 29 Oct 2026: "give voice a studio effect like mayank"): light denoise,
    75 Hz high-pass, the EQ measured to move our voice toward his narration's tonal balance (voice_match.py),
    narrator compression, de-essing and a peak limiter. `version` only names the chain for the cache key."""
    eq = json.load(open(VOICE_EQ))
    entries = ";".join(f"entry({f},{g})" for f, g in zip(eq["bands_hz"], eq["gain_db"]))
    chain = ",".join([
        "afftdn=nf=-38",                                   # gentle: a stronger setting dulled the 5-9 kHz range
        "highpass=f=75",
        f"firequalizer=gain_entry='{entries}'",
        "acompressor=threshold=-22dB:ratio=3:attack=5:release=70:makeup=3dB",
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


ENGINES = {"edge": _edge, "sarvam": _sarvam, "eleven": _eleven, "parler": _parler}


def _hash(text, cfg):
    return hashlib.sha1(json.dumps([cfg, text], ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]


def prefetch(script, cfg):
    """Engines that load a big model (parler) voice every uncached line in one batch."""
    if cfg["engine"] != "parler":
        return
    os.makedirs(CACHE, exist_ok=True)
    jobs = [(l["text"], _raw_path(l["text"], cfg)) for l in script
            if not os.path.exists(os.path.join(CACHE, f"{_hash(l['text'], cfg)}.wav"))
            and not os.path.exists(_raw_path(l["text"], cfg))]
    if jobs:
        _parler_batch(jobs, cfg)


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
        if cfg.get("pace_wps"):
            a = pace(a, text, cfg["pace_wps"])
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
