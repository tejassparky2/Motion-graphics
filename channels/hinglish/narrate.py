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
GAP = 0.26         # silence between two lines
QGAP = 0.34        # after a question
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


ENGINES = {"edge": _edge, "sarvam": _sarvam, "eleven": _eleven}


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
    h = hashlib.sha1(json.dumps([cfg, text], ensure_ascii=False, sort_keys=True).encode()).hexdigest()[:16]
    wav, meta = os.path.join(CACHE, f"{h}.wav"), os.path.join(CACHE, f"{h}.json")
    if not os.path.exists(wav):
        data, words = ENGINES[cfg["engine"]](text, cfg)
        a, off = _trim(_decode(data))
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
