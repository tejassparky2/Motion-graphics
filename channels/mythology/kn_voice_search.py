"""Kannada narrator search (owner, 6 Nov 2026: "for hindi the voice you already have and we try to make kannada").
Same recipe as the Hindi voice "Aman": an Indic Parler-TTS named Kannada speaker reads a short original passage, and
that synthetic clip becomes IndicF5's voice prompt. Nobody is cloned.

Speakers are the Kannada ones listed on the Indic Parler-TTS model card (Suresh and Anu are its recommended pair).
Every candidate reads REF_TEXT (two sentences, ~8 s), so the clip and its transcript can be used as the IndicF5
prompt as they are, with no cutting.

Usage: <shorts research>/.venv-parler/Scripts/python -I -X utf8 channels/mythology/kn_voice_search.py <out_dir>
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF_TEXT = ("ಯೋಚಿಸಿ, ಸಾವಿರಾರು ವರ್ಷಗಳಿಂದ ಜನ ಹೇಳುತ್ತಾ ಬಂದಿರುವ ಒಂದು ಕಥೆ. "
            "ಆದರೆ ಅದರ ಒಂದು ಭಾಗ, ಹೆಚ್ಚಿನವರಿಗೆ ಗೊತ್ತೇ ಇಲ್ಲ.")
SPEAKERS = {"suresh": "Suresh", "chetan": "Chetan", "anu": "Anu", "vidya": "Vidya"}
SEEDS = [3, 11, 42, 77]


def describe(name):
    # the Hindi narrator's wording (named_aman), only the speaker changed, so the two channels sound alike
    return (f"{name} speaks with a slightly high-pitch in an expressive and animated tone at a fast pace. The "
            f"recording is very clean and close-sounding, with no background noise.")


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    meta = {f"{k}_s{s}": dict(description=describe(n), seed=s, text=REF_TEXT) for k, n in SPEAKERS.items()
            for s in SEEDS}
    json.dump(meta, open(os.path.join(out, "candidates.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    jobs = [{"text": REF_TEXT, "description": m["description"], "seed": m["seed"], "out": os.path.join(out, f"{k}.wav")}
            for k, m in meta.items() if not os.path.exists(os.path.join(out, f"{k}.wav"))]
    spec = {"description": "", "seed": 0, "jobs": jobs}
    subprocess.run([sys.executable, "-I", "-X", "utf8", "-W", "ignore", os.path.join(HERE, "parler_say.py")],
                   input=json.dumps(spec, ensure_ascii=False).encode("utf-8"), check=True)


main()
