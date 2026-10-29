"""Design the channel's own narrator from a written brief (owner, 29 Oct 2026: "youthful energy and strong command of
language", "friendly, upbeat", "clear delivery"). Generates the voice-test passage for every description x seed in one
Parler run. Descriptions use the Data-Speech training vocabulary (pitch, speed, expressivity, clean/close-sounding).
Description-only voices come first: no named dataset speaker, so nobody's identity is borrowed.

Usage: <parler venv python> -I -X utf8 channels/hinglish/voice_search.py <out_dir>
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from design_voice_text import TEXT  # noqa: E402

DESCRIPTIONS = {
    "young_hi_expr": "A young male speaker with a slightly high-pitch voice delivers his words in an expressive and "
                     "animated way at a fast pace. The recording is very clean and very close-sounding, with no "
                     "background noise.",
    "young_conf": "A young man with a clear, confident voice speaks with a moderate pitch in a very expressive and "
                  "animated tone at a fast pace. The recording is very clean and close-sounding.",
    "energetic": "A male speaker delivers an energetic, expressive and animated speech with a slightly high-pitch at a "
                 "fast pace. Very clear audio, close-sounding, with no background noise.",
    "upbeat_friendly": "An upbeat young male narrator with a friendly, warm voice speaks fast in an expressive and "
                       "animated tone. The recording is of very high quality, very clean and close-sounding.",
    "young_vfast": "A young male speaker with a high-pitch voice speaks very fast in a very expressive and animated "
                   "tone. The audio is very clear and close-sounding.",
    "command": "A male speaker with a confident, slightly low-pitch voice and strong, crisp articulation speaks fast in "
               "an expressive and animated tone. Very clean, close-sounding recording.",
    "named_aman": "Aman speaks with a slightly high-pitch in an expressive and animated tone at a fast pace. The "
                  "recording is very clean and close-sounding, with no background noise.",
    "named_rohit": "Rohit speaks with a slightly high-pitch in an expressive and animated tone at a fast pace. The "
                   "recording is very clean and close-sounding, with no background noise.",
}
SEEDS = [3, 11, 42, 77, 123]


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    json.dump(DESCRIPTIONS, open(os.path.join(out, "descriptions.json"), "w", encoding="utf-8"), indent=1)
    jobs = [{"text": TEXT, "description": d, "seed": s, "out": os.path.join(out, f"{n}_s{s}.wav")}
            for n, d in DESCRIPTIONS.items() for s in SEEDS if not os.path.exists(os.path.join(out, f"{n}_s{s}.wav"))]
    spec = {"description": "", "seed": 0, "jobs": jobs}
    subprocess.run([sys.executable, "-I", "-X", "utf8", "-W", "ignore", os.path.join(HERE, "parler_say.py")],
                   input=json.dumps(spec, ensure_ascii=False).encode("utf-8"), check=True)


main()
