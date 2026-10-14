"""ElevenLabs voice samples (owner, 14 Oct 2026: "test elevenlabs English voice; if emotions are good we can switch",
and an emotional Hinglish voice for the Hindi channel). Premade and public-library voices only, never a clone of a
real person. Each sample is one request for the whole passage, so the model keeps the emotional arc; audio tags
([whispers], [excited], ...) steer eleven_v3. Cached in build/elevenlabs/, so re-runs cost no characters.

  python tools/elevenlabs_samples.py            # all samples
  python tools/elevenlabs_samples.py en         # English only ("hi" for Hinglish)
  python tools/elevenlabs_samples.py library    # native Hindi library voices (needs a paid plan or credits)
"""
import hashlib
import json
import os
import subprocess
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CACHE = REPO / "build/elevenlabs"

EN = ("[curious] A teacher finds a pack of cigarettes in the classroom trash can.\n"
      "[whispers] The school's cameras have been broken for years.\n"
      "But the kids don't know that.\n"
      "[mischievously] So he makes a plan.\n"
      "Four minutes of silence. [excited] Then Tyler stands up.\n"
      "Everyone leans in. And it's... [laughs] candy cigarettes!")
HI = ("[curious] सर, क्या भगवान इतना heavy पत्थर बना सकते हैं, कि वो खुद भी उसे lift ना कर पाएं?\n"
      "[whispers] पूरी class एकदम silent.\n"
      "और teacher? [softly] वो बस smile करते रहे।")

# (file, voice_id, voice name, model, text)
SAMPLES = [
    ("out/voice_samples/en_eleven_brian", "nPczCjzI2devNBz1zQrb", "Brian (deep, resonant)", "eleven_v3", EN),
    ("out/voice_samples/en_eleven_chris", "iP95p4xoKVk53GoZ742B", "Chris (charming, down-to-earth)", "eleven_v3", EN),
    ("out/voice_samples/en_eleven_liam", "TX3LPaxmHKxFdv7VOQHJ", "Liam (energetic Shorts creator)", "eleven_v3", EN),
    # Hindi on the free plan: premade voices only (US accents). Free users can't use library voices or Voice Design
    # through the API (402/403), so the native Hindi storytellers below need the Creator plan or $5 of credits.
    ("out/hindi_samples/hi_eleven_brian_male", "nPczCjzI2devNBz1zQrb", "Brian (premade)", "eleven_v3", HI),
    ("out/hindi_samples/hi_eleven_liam_male", "TX3LPaxmHKxFdv7VOQHJ", "Liam (premade)", "eleven_v3", HI),
    ("out/hindi_samples/hi_eleven_jessica_female", "cgSgspJ2msm6clMCkdW9", "Jessica (premade)", "eleven_v3", HI),
]
HI_LIBRARY = [  # native Hindi narrators from the public voice library (paid API access): (file, voice_id, name)
    ("out/hindi_samples/hi_eleven_viraj_male", "3AMU7jXQuQa3oRvRqUmb", "Viraj - Rich, Confident and Expressive"),
    ("out/hindi_samples/hi_eleven_rahul_male", "K0JkRcnnqtJOP749opMo", "Rahul - Hinglish"),
    ("out/hindi_samples/hi_eleven_monika_female", "1qEiC6qsybMkmnNdVMbK", "Monika Sogam - Calm and Natural"),
]
if "library" in sys.argv[1:]:
    SAMPLES = [(f, v, n, "eleven_v3", HI) for f, v, n in HI_LIBRARY]


def tts(voice_id, model, text, stability=0.5):
    """MP3 bytes for text, from the cache when this exact request was made before."""
    body = {"text": text, "model_id": model, "voice_settings": {"stability": stability, "similarity_boost": 0.75}}
    key = hashlib.sha1(json.dumps([voice_id, body], ensure_ascii=False).encode()).hexdigest()[:16]
    path = CACHE / f"{key}.mp3"
    if not path.exists():
        req = urllib.request.Request(
            f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}?output_format=mp3_44100_128",
            data=json.dumps(body).encode(), method="POST",
            headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
        CACHE.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(req, timeout=180) as r:
            path.write_bytes(r.read())
    return path


if __name__ == "__main__":
    want = [a for a in sys.argv[1:] if a != "library"] or ["en", "hi"]
    for out, vid, name, model, text in SAMPLES:
        if not any(Path(out).name.startswith(w + "_") for w in want):
            continue
        mp3 = tts(vid, model, text)
        dst = REPO / f"{out}.m4a"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(mp3), "-map_metadata", "-1", "-c:a", "aac",
                        "-b:a", "160k", "-fflags", "+bitexact", str(dst)], check=True)
        print(f"{dst.relative_to(REPO)}  <- {name}, {model}", flush=True)
