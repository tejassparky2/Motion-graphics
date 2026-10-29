"""Test premium Hindi voices against Meanwhile Mayank's narrator.

Voices the same Hinglish passage with Sarvam (bulbul:v4-flash documentary/story personas + male bulbul:v3 speakers)
and ElevenLabs eleven_v3 (premade male voices), then ranks every sample by speaker similarity to the reference clips
(Resemblyzer), Whisper-medium word error rate (Hindi) and median pitch.

Keys come from the environment or the Windows user environment, never from chat or files:
  SARVAM_API_KEY, ELEVENLABS_API_KEY   (a provider without a key is skipped)
Usage: python -I -X utf8 channels/hinglish/voice_premium.py "<shorts research>\\mayank\\voice"
"""
import base64, glob, json, os, re, sys, urllib.request
import numpy as np, librosa, soundfile as sf
from resemblyzer import VoiceEncoder, preprocess_wav
from faster_whisper import WhisperModel

TEXT = ("सोचो, एक ऐसा पौधा जो कीड़ों को खा जाता है। और ये कोई फ़िल्म का सीन नहीं है, ये बिल्कुल सच है। "
        "इसका नाम है वीनस फ्लाईट्रैप। इसकी पत्तियों पर छोटे-छोटे बाल होते हैं। "
        "अगर कोई कीड़ा बीस सेकंड के अंदर दो बार इन्हें छू ले, तो पत्ती आधे सेकंड में बंद हो जाती है। "
        "पर सबसे अजीब बात ये है कि ये पौधा गिनती कर सकता है।")
SARVAM = [("bulbul:v4-flash", v) for v in ("anand_hi_documentary", "mahesh_hi_documentary", "ratan_hi_documentary",
                                             "shubh_hi_stories_mixed", "shubh_hi_stories_dramatic", "anand_hi_news")]
SARVAM += [("bulbul:v3", v) for v in ("shubh", "aditya", "rahul", "rohan", "amit", "kabir", "advait", "dev", "tarun",
                                      "mohit", "varun")]
ELEVEN_MAX_VOICES = 6
ELEVEN_MIN_CHARS_LEFT = 3000  # leave room for the cloud chat's videos on the shared free plan


def key(name):
    if os.environ.get(name):
        return os.environ[name]
    try:  # set with [Environment]::SetEnvironmentVariable(name, value, 'User') after this app started
        import winreg
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment") as k:
            return winreg.QueryValueEx(k, name)[0]
    except OSError:
        return None


def http(url, headers, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None,
                                 headers={**headers, "Content-Type": "application/json"},
                                 method="POST" if body is not None else "GET")
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def sarvam(k, out_dir):
    made = []
    for model, speaker in SARVAM:
        out = os.path.join(out_dir, f"sarvam_{speaker}.wav")
        if not os.path.exists(out):
            try:
                r = json.loads(http("https://api.sarvam.ai/text-to-speech", {"api-subscription-key": k},
                                    {"text": TEXT, "language_code": "hi-IN", "speaker": speaker, "model": model,
                                     "speech_sample_rate": 24000}))
                open(out, "wb").write(base64.b64decode(r["audios"][0]))
            except Exception as e:
                print(f"  sarvam {speaker}: failed ({e})")
                continue
        made.append(out)
    return made


def eleven(k, out_dir):
    h = {"xi-api-key": k}
    sub = json.loads(http("https://api.elevenlabs.io/v1/user/subscription", h))
    left = sub["character_limit"] - sub["character_count"]
    print(f"  ElevenLabs characters left this month: {left}")
    voices = [v for v in json.loads(http("https://api.elevenlabs.io/v1/voices", h))["voices"]
              if v.get("category") == "premade" and (v.get("labels") or {}).get("gender") == "male"]
    made = []
    for v in voices[:ELEVEN_MAX_VOICES]:
        out = os.path.join(out_dir, f"eleven_{v['name'].split()[0]}.mp3")
        if not os.path.exists(out):
            if left - len(TEXT) < ELEVEN_MIN_CHARS_LEFT:
                print("  ElevenLabs: stopping to keep quota for the cloud chat")
                break
            try:
                audio = http(f"https://api.elevenlabs.io/v1/text-to-speech/{v['voice_id']}?output_format=mp3_44100_128",
                             h, {"text": TEXT, "model_id": "eleven_v3"})
                open(out, "wb").write(audio)
                left -= len(TEXT)
            except Exception as e:
                print(f"  eleven {v['name']}: failed ({e})")
                continue
        made.append(out)
    return made


def words(s):
    return re.findall(r"[\wऀ-ॿ]+", s.replace("़", ""))


def wer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r != h))
    return d[-1] / len(ref)


def main():
    vdir = sys.argv[1]
    out_dir = os.path.join(vdir, "premium")
    os.makedirs(out_dir, exist_ok=True)
    files = []
    for name, fn in (("SARVAM_API_KEY", sarvam), ("ELEVENLABS_API_KEY", eleven)):
        k = key(name)
        print(f"{name}: {'found' if k else 'not set, skipped'}")
        if k:
            files += fn(k, out_dir)
    if not files:
        return
    enc = VoiceEncoder(verbose=False)
    refs = [enc.embed_utterance(preprocess_wav(r)) for r in sorted(glob.glob(os.path.join(vdir, "ref_*.wav")))]
    centroid = np.mean(refs, axis=0)
    centroid /= np.linalg.norm(centroid)
    model = WhisperModel("medium", device="cpu", compute_type="int8")
    rows = []
    for f in files:
        y, sr = librosa.load(f, sr=16000)
        sim = float(np.dot(enc.embed_utterance(preprocess_wav(y, source_sr=16000)), centroid))
        f0, voiced, _ = librosa.pyin(y, fmin=60, fmax=400, sr=16000)
        hyp = " ".join(s.text for s in model.transcribe(y, language="hi", beam_size=5)[0])
        rows.append((sim, os.path.basename(f), float(np.nanmedian(f0[voiced])), len(y) / 16000, wer(words(TEXT), words(hyp))))
    print("\nmost similar to his narrator first (best free voice scored 0.728; his own clips 0.97):")
    for sim, name, f0, dur, w in sorted(rows, reverse=True):
        print(f"  {sim:.3f}  {name:38s} pitch {f0:6.1f} Hz  {dur:5.1f} s  Whisper WER {w:.0%}")


main()
