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

# Default narrator: Kokoro am_fenrir again. The owner's cloned voice (Chatterbox, NARRATOR_ENGINE=clone, prompt in
# assets/voice/owner_prompt.wav) was the default from Oct 2026 until the owner saw more viewers swiping away on the
# cloned-voice videos (35% stayed to watch) and switched back (5 Oct 2026).
CLONE_PROMPT = os.path.join(ROOT, "assets", "voice", "owner_prompt.wav")
CLONE_PYTHON = os.environ.get("CLONE_PYTHON", "/home/user/.venv-clone/bin/python")
ORPHEUS_PYTHON = os.environ.get("ORPHEUS_PYTHON", "/home/user/.venv-orpheus/bin/python")
ORPHEUS_REPOS = {"q8": "PkmX/orpheus-3b-0.1-ft-Q8_0-GGUF", "q6": "TheVisitorX/orpheus-3b-0.1-ft-Q6_K-GGUF"}
# Orpheus is breathy: a presence lift and gentle compression make it clearer on a phone (owner approved "O+")
ORPHEUS_TONE = ("highpass=f=80,equalizer=f=220:t=q:w=1:g=-2,equalizer=f=3000:t=q:w=1:g=4,equalizer=f=6000:t=q:w=1:g=2,"
                "acompressor=threshold=-20dB:ratio=3:attack=5:release=60:makeup=2,alimiter=limit=0.95")
ENGINE = os.environ.get("NARRATOR_ENGINE", "kokoro")
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
elif ENGINE == "elevenlabs":
    VOICE = os.environ.get("NARRATOR_VOICE", "iP95p4xoKVk53GoZ742B")   # see ELEVEN below
    SPEED = float(os.environ.get("NARRATOR_SPEED", "1.0"))
else:
    VOICE = os.environ.get("NARRATOR_VOICE", "en_US-ryan-high")
    # Piper length scale: <1 speaks faster. 0.8 lands the ryan voice at ~230 wpm.
    SPEED = 1 / float(os.environ.get("NARRATOR_PACE", "0.8"))
VOICE_BASE = "https://huggingface.co/rhasspy/piper-voices/resolve/main"
SR = 44100
TRIM_PAD = 0.02  # seconds of room kept around each trimmed line
MAX_PAUSE = 0.3  # pauses inside a line are shortened to this (the reference narrator's breaths are ~0.32 s)


def configure(voice=None, speed=None, max_pause=None, engine=None, turbo=False, turbo_ref=None, rate=None,
              tempo_min=None, tempo_max=None, orpheus=None, orpheus_quant="q4"):
    """Per-video narrator settings (environment variables still win, so you can audition voices).
    `engine="elevenlabs"` switches this video's narrator to ElevenLabs (default voice: Chris).
    `turbo=True` voices the video with Chatterbox Turbo (and its tags); `turbo_ref="am_puck+1.5"` gives the narrator
    the timbre of that Kokoro voice (pitch-shifted by the semitones after +/-) instead of Turbo's stock voice.
    `rate` (syllables per second) and `tempo_min` set a calmer pace for clone/Turbo takes (the doctor channel's
    explainers are read slower than the story videos)."""
    global VOICE, SPEED, MAX_PAUSE, ENGINE, CLONE_MODEL, NARRATOR_REF, CLONE_RATE, TEMPO_MIN, TEMPO_MAX
    if rate and "CLONE_RATE" not in os.environ:
        CLONE_RATE = rate
    if tempo_min:
        TEMPO_MIN = tempo_min
    if tempo_max:
        TEMPO_MAX = tempo_max
    if orpheus and "NARRATOR_ENGINE" not in os.environ:   # `orpheus="leo"`: Orpheus TTS stock voice (tools/orpheus_tts.py)
        engine = "clone"                                 # `orpheus_quant="q8"`: the bigger, clearer model (owner: "O+")
        CLONE_MODEL = f"orpheus-{orpheus}" + ("" if orpheus_quant == "q4" else f"-{orpheus_quant}")
    if turbo and "NARRATOR_ENGINE" not in os.environ:
        engine = "clone"
        if "CLONE_MODEL" not in os.environ:
            CLONE_MODEL = "turbo"
    NARRATOR_REF = turbo_ref
    if engine and "NARRATOR_ENGINE" not in os.environ and engine != ENGINE:
        ENGINE = engine
        if engine == "elevenlabs":
            VOICE = os.environ.get("NARRATOR_VOICE", ELEVEN["chris"])
            SPEED = float(os.environ.get("NARRATOR_SPEED", "1.0"))
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


CLONE_VERSION = "v4"   # bump when the clone generation, pace or tone changes (v4: Turbo takes made with the right model)

# Chatterbox Turbo voice tags (the tokens in its tokenizer, added_tokens.json). Tested 14 Oct 2026 on this channel's
# lines (out/turbo_tags_research.md): the sound tags really make the sound, but only on some takes, so clone_check
# keeps a take only once the sound is there; the mood tags only shade the delivery a little (slower, more emphatic).
# Kokoro and the owner clone can't voice them, so they're dropped there.
TURBO_SOUNDS = {"[laugh]", "[chuckle]", "[sigh]", "[gasp]", "[sniff]", "[groan]", "[cough]", "[clear throat]",
                "[shush]"}
TURBO_MOODS = {"[angry]", "[fear]", "[surprised]", "[whispering]", "[dramatic]", "[narration]", "[crying]",
               "[happy]", "[sarcastic]", "[advertisement]"}
TURBO_TAGS = TURBO_SOUNDS | TURBO_MOODS
_TAG = re.compile(r"\[(?:" + "|".join(t[1:-1] for t in sorted(TURBO_TAGS)) + r")\]")


def strip_tags(text):
    return " ".join(_TAG.sub(" ", text).split())


def _voice_tags(text):
    return text if (ENGINE == "clone" and CLONE_MODEL == "turbo") else strip_tags(text)
# CLONE_MODEL=turbo: Chatterbox Turbo's own stock voice (not a clone of anyone), tested by the owner on 14 Oct 2026
# ("en turbo is not bad, make only 1 video with it to test"). Same pipeline as the owner clone; separate caches.
CLONE_MODEL = os.environ.get("CLONE_MODEL", "owner")


# Character voices: a video sets voice.SPEAKERS = {"croc": dict(voice="am_onyx", speed=0.95, pitch=-2.5), ...}.
# Lines (or the part of a line from `speaker_from` on) spoken by that character use its own Kokoro voice, speed and
# pitch shift (semitones), so dialogue sounds like a cast and not like the narrator reading quotes. The narrator
# itself is unchanged. Kokoro only; the clone engine ignores it.
SPEAKERS = {}
# With CLONE_MODEL=turbo a character can speak through Turbo too, with its tags: give it `turbo_ref` (a Kokoro voice
# name). Turbo copies the timbre of a short Kokoro clip in that voice (synthetic, nobody real is cloned).


def _char(who):
    spec = SPEAKERS.get(who) if (who and (ENGINE in ("kokoro", "elevenlabs") or CLONE_MODEL == "turbo")) else None
    return None if (spec and _turbo_char(who)) else spec


NARRATOR_REF = None


def _decode_tag():
    """Orpheus takes made before 25 Oct 2026 lost their first ~0.17 s (orpheus-cpp's streaming decoder); new cache keys."""
    return "|whole" if CLONE_MODEL.startswith("orpheus-") else ""


def _turbo_char(who):
    """The character's (or, for who=None, the narrator's) Turbo reference voice, if it speaks through Turbo."""
    if not (ENGINE == "clone" and CLONE_MODEL == "turbo"):
        return None
    if not who:
        return NARRATOR_REF
    spec = SPEAKERS.get(who)
    return spec.get("turbo_ref") if spec else None


TURBO_REF_TEXT = ("Well, well. Look what we have here! Don't worry, I always keep my promises. Mostly. "
                  "Please, I'm begging you. Just this once. You'll see, it's going to be fine.")


def _turbo_ref_wav(ref):
    """A ~9 s clip of a Kokoro voice for Turbo to take the timbre from (made once, cached).
    `ref`: "af_heart", or "am_puck+1.5" / "af_heart-2" for a pitch-shifted (younger / deeper) version."""
    out = os.path.join(ROOT, "build", "turbo_refs", f"{ref}.wav")
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        m = re.fullmatch(r"([a-z]{2}_[a-z]+)([+-][0-9.]+)?", ref)
        kvoice, st = m.group(1), float(m.group(2) or 0)
        raw = out + ".raw.wav"
        _kokoro_wav(TURBO_REF_TEXT, 1.0, raw, kvoice)
        if abs(st) > 0.01:
            import imageio_ffmpeg
            subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", raw, "-filter:a",
                            f"rubberband=pitch={2 ** (st / 12):.5f}:pitchq=quality:formant=shifted", out], check=True)
            os.remove(raw)
        else:
            os.replace(raw, out)
    return out


def _key(text, pace=1.0, who=None, tone=None):
    spec = _char(who)
    if ENGINE == "elevenlabs" and (not spec or "el" in spec):
        return _el_spec(text, pace, who, tone)[0]
    if spec:
        tag = f"{spec.get('voice')}|{spec.get('speed', 1.0)}|{spec.get('pitch', 0.0)}"
        return hashlib.sha1(f"char|{tag}|{SPEED * pace:.3f}|{_pronounce(text)}".encode()).hexdigest()[:16]
    if text in _EXTERNAL:   # lines cut from an uploaded narration are keyed by that file
        return hashlib.sha1(f"ext|{EXTERNAL_TAG}|{text}".encode()).hexdigest()[:16]
    if ENGINE == "clone":
        ref = f"{_turbo_char(who)}|" if _turbo_char(who) else ""
        return hashlib.sha1(f"clone|{CLONE_MODEL}|{CLONE_VERSION}{_decode_tag()}|{CLONE_RATE}|{pace:.3f}|{ref}{text}".encode()).hexdigest()[:16]
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


def synth(text, pace=1.0, who=None, tone=None):
    """Speech for one line as float samples at 44.1 kHz, silence-trimmed (cached).

    `pace` scales the speed for this line only (e.g. 0.9 to land a punchline a touch slower).
    `who` picks a character voice from SPEAKERS (narrator if unset).
    `tone` is an ElevenLabs v3 audio tag for this take ("excited", "whispers", ...); other engines ignore it."""
    spec = _char(who)
    if ENGINE == "elevenlabs" and (not spec or "el" in spec):
        # the gentler trim: ElevenLabs ends sentences softly, and _trim cut "homework" to "home" (14 Oct 2026)
        return _squeeze(_clone_trim(_read_wav(_el_finished(text, pace, who, tone))))
    if spec:
        out = os.path.join(ROOT, "build", "tts", f"{_key(text, pace, who)}.wav")
        if not os.path.exists(out):
            os.makedirs(os.path.dirname(out), exist_ok=True)
            raw = out + ".raw.wav"
            _kokoro_wav(_pronounce(strip_tags(text)), SPEED * pace * spec.get("speed", 1.0), raw, spec.get("voice"))
            st = spec.get("pitch", 0.0)
            if abs(st) > 0.01:   # pitch only (tempo kept), for a character's colour
                import imageio_ffmpeg
                subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", raw, "-filter:a",
                                f"rubberband=pitch={2 ** (st / 12):.5f}:pitchq=quality:transients=crisp", "-ar",
                                str(SR), "-ac", "1", out], check=True)
                os.remove(raw)
            else:
                os.replace(raw, out)
        return _squeeze(_trim(_read_wav(out)))
    if text in _EXTERNAL:
        return _squeeze(_trim(_read_wav(_EXTERNAL[text])))
    out = os.path.join(ROOT, "build", "tts", f"{_key(text, pace)}.wav")
    if ENGINE == "clone":
        if not os.path.exists(_clone_raw(text, who)):
            clone_prefetch([(text, who)])
        return _squeeze(_clone_trim(_read_wav(_clone_process(text, pace, who)[0])))
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if ENGINE == "kokoro":
            _kokoro_wav(_pronounce(strip_tags(text)), SPEED * pace, out)
        else:
            model = _voice_path()
            subprocess.run([sys.executable, "-m", "piper", "-m", model, "-f", out,
                            "--length-scale", str(1 / (SPEED * pace))],
                           input=strip_tags(text).encode(), check=True, stderr=subprocess.DEVNULL)
    return _squeeze(_trim(_read_wav(out)))


# Pace target: The Teacher Bluffed (owner: "speed similar as the teacher Bluffed video") reads at a median
# 5.2 syllables per second of speech, with lines within ~0.5 of each other.
CLONE_RATE = float(os.environ.get("CLONE_RATE", "5.5"))   # owner: "fast up voice slightly more" (was 5.2)
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
    for w in re.findall(r"[a-z']+", strip_tags(text).lower()):
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


def _clone_process(text, pace, who=None):
    """The finished take: nudged toward the target pace (rubberband, crisp mode) and toned. -> (path, final rate)."""
    import imageio_ffmpeg
    import soundfile
    out = os.path.join(ROOT, "build", "tts", f"{_key(text, pace, who)}.wav")
    r, rsr = soundfile.read(_clone_raw(text, who))
    rate = syllables(text) / max(0.2, speech_secs(r, rsr))
    tempo = min(TEMPO_MAX, max(TEMPO_MIN, CLONE_RATE * pace / rate))
    if _has_sound(text):   # a laugh or a sigh counts as "speech" above, so don't rush the words to make up for it
        tempo = min(tempo, 1.05)
    if not os.path.exists(out):
        os.makedirs(os.path.dirname(out), exist_ok=True)
        stretch = (f"rubberband=tempo={tempo:.4f}:transients=crisp:detector=compound:phase=laminar:window=short:"
                   f"formant=preserved:pitchq=quality,") if abs(tempo - 1) > 0.005 else ""
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", _clone_raw(text, who),
                        "-filter:a", stretch + (CLONE_TONE if CLONE_MODEL == "owner" else ORPHEUS_TONE if CLONE_MODEL.startswith("orpheus-")
                                                 else "highpass=f=60,alimiter=limit=0.95"), "-ar", str(SR), "-ac", "1", out], check=True)
    return out, rate * tempo


def _clone_trim(a, thresh=0.006, pre=0.035, post=0.05):
    """Tight trim for clone takes: drop the breath/silence the model leaves around a sentence, but keep soft
    first consonants (a looser threshold than _trim, so "Put" doesn't turn into "could")."""
    env = np.convolve(np.abs(a), np.ones(441) / 441, mode="same")
    loud = np.nonzero(env > thresh)[0]
    if not len(loud):
        return a
    return a[max(0, loud[0] - int(pre * SR)): loud[-1] + int(post * SR)]


def _clone_raw(text, who=None):
    ref = _turbo_char(who)
    key = f"{CLONE_MODEL}|{CLONE_VERSION}{_decode_tag()}|{text}" + (f"|{ref}" if ref else "")
    return os.path.join(ROOT, "build", "clone_tts", hashlib.sha1(key.encode()).hexdigest()[:16] + ".wav")


def _has_sound(text):
    return any(t in text for t in TURBO_SOUNDS) and CLONE_MODEL == "turbo"


# Spellings the clone pronounces more clearly (only what it's told to say; captions keep the real word).
CLONE_SAY = {"bencher": "benchur", "benchers": "benchurs", "Frane": "Frahneh", "Selak": "Sehlahk", "Gabriel's": "Gaybreeul's", "Plutarch": "Ploo-tark", "Pyrrhus": "Peer-us", "Pyrrhic": "Pirrick"}


def _clone_say(text):
    for word, say in CLONE_SAY.items():
        text = re.sub(rf"\b{word}\b", say, text, flags=re.I)
    return text


def clone_prefetch(texts):
    """Generate every missing sentence in one go (the clone model takes ~20 s to load).
    `texts`: sentences, or (sentence, character) pairs for characters that speak through Turbo."""
    if ENGINE != "clone":
        return
    pairs = [t if isinstance(t, tuple) else (t, None) for t in texts]
    jobs = [[_voice_tags(_clone_say(t)), _clone_raw(t, w)] + ([_turbo_ref_wav(_turbo_char(w))] if _turbo_char(w) else [])
            for t, w in dict.fromkeys(pairs) if t not in _EXTERNAL and not os.path.exists(_clone_raw(t, w))]
    if not jobs:
        return
    path = os.path.join(ROOT, "build", "clone_tts", f"jobs_{os.getpid()}.json")   # one per render, so parallel renders never collide
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(jobs, open(path, "w"))
    print(f"clone voice: generating {len(jobs)} sentences", file=sys.stderr, flush=True)
    # the model choice must reach the subprocess: a video that picks Turbo in its NARRATOR settings (not the shell
    # environment) was otherwise voiced by the owner-clone model, tags read out as words (found 15 Oct 2026)
    if CLONE_MODEL.startswith("orpheus-"):
        _, voice, *quant = CLONE_MODEL.split("-")
        env = dict(os.environ, ORPHEUS_VOICE=voice)
        if quant:
            env["ORPHEUS_REPO"] = ORPHEUS_REPOS[quant[0]]
        subprocess.run([ORPHEUS_PYTHON, os.path.join(ROOT, "tools", "orpheus_tts.py"), path], check=True, env=env)
        return
    subprocess.run([CLONE_PYTHON, os.path.join(ROOT, "tools", "clone_tts.py"), path], check=True,
                   env=dict(os.environ, CLONE_MODEL=CLONE_MODEL))


_NUMWORDS = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen "
                "seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand "
                "million percent point and a".split())
_checker = None


SAME_SOUND = {"principle": "principal", "principles": "principals"}   # Whisper's spelling, not a mishearing
_TAG_WORDS = {"chuckle", "laugh", "sigh", "gasp", "sniff", "groan", "cough", "shush", "jekyll", "chuckl"}
_SOUNDS_HEARD = set("heh hehe hehehe ha hah haha hahaha hm hmm mm mhm uh um ugh huh ahem shh sh ah aah oh ooh phew sniff".split())


def _heard_ok(text, heard):
    """Same words, allowing numbers heard as digits ("twenty-eight" -> "28") and a tag's laugh heard as "heh",
    and same-sounding spellings ("principle" for "principal")."""
    t = re.sub(r"[^a-z0-9' ]", " ", strip_tags(text).lower().replace("-", " ")).split()
    h = [SAME_SOUND.get(w, w) for w in re.sub(r"[^a-z0-9' ]", " ", heard.lower().replace("-", " ")).split()]
    if _has_sound(text):
        h = [w for w in h if w not in _SOUNDS_HEARD or w in t]
        # Turbo sometimes SAYS the tag ("Come down for dinner, sweetie. Chuckle."; Lily's "chuckle" heard as "Jekyll")
        if any(w.rstrip("s") in _TAG_WORDS and w not in t for w in h):
            return False
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, t, h).get_opcodes():
        if op == "equal":
            continue
        if all(w in _NUMWORDS for w in t[i1:i2]) and all(re.fullmatch(r"[0-9%.,]+|and|a", w) for w in h[j1:j2]):
            continue
        return False
    return True


def _sound_ok(text, a, sr, words):
    """Did a sound tag actually make its sound? Turbo voices it on some takes only. It shows up as a laugh-like word
    Whisper adds ("heh"), or as >= 0.3 s of sound before the first word / after the last / between two words."""
    if not _has_sound(text):
        return True
    said = set(re.sub(r"[^a-z' ]", " ", strip_tags(text).lower()).split())
    if any(re.sub(r"[^a-z]", "", w.word.lower()) in _SOUNDS_HEARD - said for w in words):
        return True
    if not words:
        return False
    env = np.convolve(np.abs(a), np.ones(int(sr * 0.02)) / (sr * 0.02), mode="same")
    loud = np.nonzero(env > 0.01)[0]
    if not len(loud):
        return False
    on, off = loud[0] / sr, loud[-1] / sr
    gaps = [b.start - x.end for x, b in zip(words, words[1:])]
    first = text.lstrip().startswith("[")
    last = text.rstrip().endswith("]")
    return ((first and words[0].start - on >= 0.3) or (last and off - words[-1].end >= 0.3)
            or (not first and not last and max(gaps, default=0) >= 0.3))


def clone_check(takes, tries=3, slack=0.15):
    """Hear every finished take with Whisper medium. Re-make takes that are misheard, whose pace is more than
    `slack` off the target, or whose sound tag made no sound, and keep the best of `tries`.
    `takes`: [(text, pace)] or [(text, pace, character)]."""
    if ENGINE != "clone":
        return
    global _checker
    import shutil
    import soundfile
    takes = list(dict.fromkeys(tuple(x) + (None,) * (3 - len(x)) for x in takes))
    if CLONE_MODEL == "turbo":   # Turbo's pace varies with emotion; clarity and tag sounds stay strict, pace less so
        slack = max(slack, 0.3)
    if CLONE_MODEL.startswith("orpheus-"):   # Orpheus keeps its own natural pace (no stretching): check clarity only,
        slack = 9.0                          # and it sometimes changes words, so it gets more tries to say them exactly
        tries = max(tries, 6)
    tries = tries + 2 if any(_has_sound(t) for t, _, _ in takes) else tries
    todo = [(t, p, w) for t, p, w in takes if t not in _EXTERNAL and not os.path.exists(_clone_raw(t, w) + ".ok")]
    if not todo:
        return
    if _checker is None:
        from faster_whisper import WhisperModel
        _checker = WhisperModel("medium.en", device="cpu", compute_type="int8")
    best = {}
    for attempt in range(tries):
        bad = []
        for t, p, w in todo:
            out, rate = _clone_process(t, p, w)
            a, sr = soundfile.read(out)
            a = np.concatenate([np.zeros(sr // 2), a, np.zeros(sr // 2)])
            a16 = np.interp(np.arange(int(len(a) * 16000 / sr)) * sr / 16000, np.arange(len(a)), a).astype(np.float32)
            segs = list(_checker.transcribe(a16, language="en", beam_size=5, word_timestamps=True)[0])
            heard = " ".join(x.text.strip() for x in segs)
            words = [x for s in segs for x in s.words]
            probs = [x.probability for x in words]
            off = abs(rate / (CLONE_RATE * p) - 1)
            score = (_heard_ok(t, heard), _sound_ok(t, a16, 16000, words), off <= slack, -off,
                     float(np.mean(probs)) if probs else 0.0)
            keep = f"{_clone_raw(t, w)}.try{attempt}.wav"
            shutil.copy(_clone_raw(t, w), keep)
            if (t, w) not in best or score > best[(t, w)][0]:
                best[(t, w)] = (score, keep, heard, p)
            if not (score[0] and score[1] and score[2]):
                bad.append((t, p, w))
        print(f"clone check {attempt + 1}/{tries}: {len(todo) - len(bad)}/{len(todo)} takes clear and on pace",
              file=sys.stderr, flush=True)
        if not bad or attempt == tries - 1:
            break
        for t, p, w in bad:
            if os.path.exists(_clone_raw(t, w)):   # the same sentence can come twice, at two paces
                os.remove(_clone_raw(t, w))
            for pc in (p, 1.0, 0.9):
                f = os.path.join(ROOT, "build", "tts", f"{_key(t, pc, w)}.wav")
                if os.path.exists(f):
                    os.remove(f)
        clone_prefetch([(t, w) for t, _, w in bad])
        todo = bad
    for (t, w), (score, keep, heard, p) in best.items():
        shutil.copy(keep, _clone_raw(t, w))
        for pc in (p, 1.0, 0.9):   # rebuild the finished take from the chosen raw one
            for f in glob.glob(os.path.join(ROOT, "build", "tts", f"{_key(t, pc, w)}*")):
                os.remove(f)
        open(_clone_raw(t, w) + ".ok", "w").write(heard)
        if not score[0]:
            print(f"clone check: still unclear after {tries} tries: {t!r} heard as {heard!r}", file=sys.stderr)
        elif not score[1]:
            print(f"clone check: the sound tag made no sound after {tries} tries: {t!r}", file=sys.stderr)


# ---- ElevenLabs (owner, 14 Oct 2026: "Chris is good, make the genie scripts with him for emotions")
# Premade / library voices only, never a clone of a real person. One API call per sentence take (the pipeline's
# full-stop pauses stay), eleven_v3 with an optional audio tag per take for emotion. Raw MP3s are cached in
# build/el_tts/ by request, so re-renders cost no characters. A video's SPEAKERS entry can name an ElevenLabs voice:
#   "kid": dict(el=ELEVEN["liam"], pitch=2.5, tone="mischievously", fx="aecho=...")   (fx: an ffmpeg audio filter)
ELEVEN = {"chris": "iP95p4xoKVk53GoZ742B", "brian": "nPczCjzI2devNBz1zQrb", "liam": "TX3LPaxmHKxFdv7VOQHJ",
          "callum": "N2lVS1w4EtoT3dr4eOWO", "adam": "pNInz6obpgDQGcFmaJgB", "bill": "pqHfZKP75CvOlQylNhV4",
          "daniel": "onwK4e9ZLuTAKqWW03F9", "lily": "pFZP5JQG7iQjIQuC4Bku", "harry": "SOYHLrjzK2X1ezoPC6cr",
          "george": "JBFqnCBsd6RMkjVDRZzb", "jessica": "cgSgspJ2msm6clMCkdW9", "laura": "FGY2WhTYpPnrIDTdsKH5"}
EL_MODEL = os.environ.get("EL_MODEL", "eleven_v3")
EL_SAY = {"bencher": "benchur"}      # "last bencher" came out as "last bench" (Whisper medium, 14 Oct 2026)
EL_STABILITY = 0.5      # eleven_v3: 0 creative, 0.5 natural, 1 robust
EL_VERSION = "v2"       # bump when the processing below changes
# Narrator pace: ElevenLabs reads some takes much faster than others (a ghost video's logic lines came out at 270 wpm
# next to 170 elsewhere). Each narrator take is nudged toward CLONE_RATE syllables per second (the Teacher Bluffed
# pace the owner chose) if it runs faster, by at most 12%; characters keep the pace they were acted at.
EL_TEMPO = (0.88, 1.0)     # slow rushed takes down; never speed a take up (clarity first)


def _el_spec(text, pace, who, tone):
    """(finished-take key, raw-request key, request body, voice id, tempo, pitch, fx) for one take."""
    spec = _char(who) or {}
    text = strip_tags(text)                # Turbo sound tags ([chuckle], ...) are not ElevenLabs tags
    vid = spec.get("el", VOICE)
    tone = tone or spec.get("tone")
    for word, sub in EL_SAY.items():       # spellings it says more clearly; captions keep the real word
        text = re.sub(rf"\b{word}", sub, text, flags=re.I)
    say = f"[{tone}] {text}" if tone else text
    body = {"text": say, "model_id": EL_MODEL,
            "voice_settings": {"stability": spec.get("stability", EL_STABILITY), "similarity_boost": 0.75}}
    tempo = (SPEED if not spec else 1.0) * spec.get("speed", 1.0) * pace
    pitch, fx = spec.get("pitch", 0.0), spec.get("fx", "")
    raw = hashlib.sha1(json.dumps([vid, body], ensure_ascii=False).encode()).hexdigest()[:16]
    paced = "" if spec else f"|rate{CLONE_RATE}|{EL_TEMPO}"
    key = hashlib.sha1(f"el|{EL_VERSION}|{raw}|{tempo:.3f}|{pitch}|{fx}{paced}".encode()).hexdigest()[:16]
    return key, raw, body, vid, tempo, pitch, fx


def _el_raw(raw, body, vid):
    path = os.path.join(ROOT, "build", "el_tts", f"{raw}.mp3")
    if not os.path.exists(path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{vid}?output_format=mp3_44100_128",
            data=json.dumps(body).encode(), method="POST",
            headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
        for attempt in range(4):
            try:
                with urllib.request.urlopen(req, timeout=180) as r:
                    data = r.read()
                break
            except urllib.error.HTTPError as e:
                if e.code < 500 and e.code != 429 or attempt == 3:
                    raise RuntimeError(f"ElevenLabs {e.code}: {e.read()[:300]!r}") from None
                import time
                time.sleep(2 ** (attempt + 1))
        open(path + ".part", "wb").write(data)
        os.replace(path + ".part", path)
        print(f"elevenlabs: {len(body['text'])} chars: {body['text']!r}", file=sys.stderr, flush=True)
    return path


def _el_finished(text, pace=1.0, who=None, tone=None):
    """The finished take as a 44.1 kHz mono wav: decoded, tempo (rubberband, pitch kept), pitch shift, effects."""
    import imageio_ffmpeg
    key, raw, body, vid, tempo, pitch, fx = _el_spec(text, pace, who, tone)
    out = os.path.join(ROOT, "build", "tts", f"{key}.wav")
    if not os.path.exists(out):
        src = _el_raw(raw, body, vid)
        os.makedirs(os.path.dirname(out), exist_ok=True)
        if not _char(who):         # narrator: toward the channel pace (see EL_TEMPO)
            dec = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", src, "-f", "f32le", "-ac", "1",
                                  "-ar", "16000", "-"], capture_output=True, check=True).stdout
            rate = syllables(text) / max(0.2, speech_secs(np.frombuffer(dec, np.float32), 16000))
            tempo *= min(EL_TEMPO[1], max(EL_TEMPO[0], CLONE_RATE * pace / rate))
        chain = []
        if abs(tempo - 1) > 0.005 or abs(pitch) > 0.01:
            # a pitch shift moves the formants too (smaller, younger voice, e.g. a kid); tempo alone keeps them
            chain.append(f"rubberband=tempo={tempo:.4f}:pitch={2 ** (pitch / 12):.5f}:transients=crisp:"
                         f"pitchq=quality" + (":formant=preserved" if abs(pitch) <= 0.01 else ""))
        if fx:
            chain.append(fx)
        chain.append("highpass=f=60,alimiter=limit=0.95")
        subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-i", src, "-filter:a",
                        ",".join(chain), "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", out], check=True)
    return out


def el_check(takes, tries=3):
    """Hear every ElevenLabs take with Whisper medium; re-make (up to `tries` in all) any take that's misheard, and
    keep the first clear one. `takes`: [(text, pace, who, tone)]. Clear takes get a .ok marker, so this runs once."""
    if ENGINE != "elevenlabs":
        return
    global _checker
    import shutil
    import soundfile
    todo = []
    for t in dict.fromkeys(takes):
        spec = _char(t[2])
        if spec and "el" not in spec:
            continue
        _, raw, body, vid, *_ = _el_spec(*t)
        if not os.path.exists(os.path.join(ROOT, "build", "el_tts", f"{raw}.ok")):
            todo.append(t)
    if not todo:
        return
    if _checker is None:
        from faster_whisper import WhisperModel
        _checker = WhisperModel("medium.en", device="cpu", compute_type="int8")
    for t in todo:
        key, raw, body, vid, *_ = _el_spec(*t)
        rawp = os.path.join(ROOT, "build", "el_tts", f"{raw}.mp3")
        heard = ""
        for attempt in range(tries):
            a, sr = soundfile.read(_el_finished(*t))
            a = np.concatenate([np.zeros(sr // 2), a, np.zeros(sr // 2)])
            a16 = np.interp(np.arange(int(len(a) * 16000 / sr)) * sr / 16000, np.arange(len(a)), a).astype(np.float32)
            heard = " ".join(x.text.strip() for x in _checker.transcribe(a16, language="en", beam_size=5)[0])
            shutil.copy(rawp, f"{rawp}.try{attempt}")
            if _heard_ok(t[0], heard):
                break
            print(f"elevenlabs check: {t[0]!r} heard as {heard!r} (try {attempt + 1}/{tries})", file=sys.stderr)
            if attempt < tries - 1:     # make it again
                for f in glob.glob(os.path.join(ROOT, "build", "tts", f"{key}*")) + [rawp]:
                    os.remove(f)
        else:
            shutil.copy(f"{rawp}.try0", rawp)      # nothing clear: keep the first take and say so
            for f in glob.glob(os.path.join(ROOT, "build", "tts", f"{key}*")):
                os.remove(f)
            print(f"elevenlabs check: still unclear after {tries} tries: {t[0]!r}", file=sys.stderr)
        open(os.path.join(ROOT, "build", "el_tts", f"{raw}.ok"), "w").write(heard)


_whisper = None


def _norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def word_times(text, audio, pace=1.0, who=None, tone=None):
    """[(start, end)] for each whitespace-separated word of `text`, relative to the start of `audio`.

    Whisper's timestamps are matched to the script by sequence alignment; words Whisper heard differently
    (e.g. "seventy" -> "70") get times interpolated from their neighbours by character length.
    """
    cache = os.path.join(ROOT, "build", "tts", f"{_key(text, pace, who, tone)}.p{MAX_PAUSE}.words.json")
    if os.path.exists(cache):
        return [tuple(x) for x in json.load(open(cache))]
    global _whisper
    if _whisper is None:
        from faster_whisper import WhisperModel
        _whisper = WhisperModel(os.environ.get("ALIGN_MODEL", "small.en"), device="cpu", compute_type="int8")
    a16 = np.interp(np.arange(int(len(audio) * 16000 / SR)) * SR / 16000, np.arange(len(audio)), audio)
    text = strip_tags(text)   # times are for the spoken words only
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
    gate = (np.abs(track) > 0.01).astype(np.float64)
    # sidechain-style envelope: ~20 ms attack (the bed drops the moment a word starts), ~300 ms release (no pumping
    # between words); a hop of 1 ms keeps it cheap (research 18 Oct 2026, A4)
    hop = SR // 1000
    g = gate[: len(gate) // hop * hop].reshape(-1, hop).max(axis=1)
    a_up, a_dn = 1 - np.exp(-1 / 20), 1 - np.exp(-1 / 300)
    env = np.empty_like(g)
    v = 0.0
    for i, x in enumerate(g):
        v += (a_up if x > v else a_dn) * (x - v)
        env[i] = v
    env = np.repeat(env, hop)
    env = np.concatenate([env, np.full(len(gate) - len(env), env[-1] if len(env) else 0.0)])
    return track, np.clip(env, 0, 1)
