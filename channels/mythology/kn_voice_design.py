"""Design a new Kannada narrator from a written description, the way the Hindi voice "Aman" was made (owner, 7 Nov
2026: "Try created new voice with description like we did in our shorts chat for hindi voice i want clear good voice
similar to our hindi one").

kn_voice_search.py already tried Aman's exact wording with the Kannada speakers (Suresh, Vidya; rejected). This grid
tries what is left, each reading the same two-sentence passage (REF_TEXT) so the clip can be the IndicF5 prompt as is:
- aman_*: the Hindi narrator's own Indic Parler speaker, Aman, reading Kannada (the closest to the Hindi voice);
- *_calm: calmer, clearer wording at a moderate pace (owner, 6 Nov: "clear calm and well understandable");
- narrator_*: no named speaker, only the description of a deep, warm, clear male storyteller.
Nobody is cloned: every voice comes from text.

Usage: <shorts research>/.venv-parler/Scripts/python -I -X utf8 channels/mythology/kn_voice_design.py <out_dir>
Then kn_voice_design_score.py ranks the clips."""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REF_TEXT = ("ಯೋಚಿಸಿ, ಸಾವಿರಾರು ವರ್ಷಗಳಿಂದ ಜನ ಹೇಳುತ್ತಾ ಬಂದಿರುವ ಒಂದು ಕಥೆ. "      # same passage as kn_voice_search.py
            "ಆದರೆ ಅದರ ಒಂದು ಭಾಗ, ಹೆಚ್ಚಿನವರಿಗೆ ಗೊತ್ತೇ ಇಲ್ಲ.")

QUALITY = "The recording is very clear and close-sounding, with no background noise."
DESCRIPTIONS = {
    # the Hindi narrator's exact description (channels/hinglish/voice_search.py, "named_aman")
    "aman_orig": ("Aman speaks with a slightly high-pitch in an expressive and animated tone at a fast pace. The "
                  "recording is very clean and close-sounding, with no background noise."),
    "aman_calm": ("Aman speaks with a moderate pitch in a calm, clear and warm tone at a moderate pace, like a "
                  "storyteller narrating an old legend. " + QUALITY),
    "narrator_calm": ("A male narrator with a deep, warm and clear voice speaks in a calm, confident storytelling tone "
                      "at a moderate pace. " + QUALITY),
    "narrator_lively": ("A male narrator with a clear, slightly deep voice speaks in an engaging and expressive "
                        "storytelling tone at a moderate pace. " + QUALITY),
    "suresh_calm": ("Suresh speaks with a moderate pitch in a calm, clear and warm tone at a moderate pace, like a "
                    "storyteller narrating an old legend. " + QUALITY),
    "chetan_calm": ("Chetan speaks with a moderate pitch in a calm, clear and warm tone at a moderate pace, like a "
                    "storyteller narrating an old legend. " + QUALITY),
}
SEEDS = {"aman_orig": [3, 11, 42, 77], "aman_calm": [3, 11, 42, 77], "narrator_calm": [3, 11, 42, 77],
         "narrator_lively": [3, 42], "suresh_calm": [3, 42], "chetan_calm": [3, 42]}


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    meta = {f"{k}_s{s}": dict(description=DESCRIPTIONS[k], seed=s, text=REF_TEXT) for k in DESCRIPTIONS
            for s in SEEDS[k]}
    json.dump(meta, open(os.path.join(out, "candidates.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    jobs = [{"text": REF_TEXT, "description": m["description"], "seed": m["seed"], "out": os.path.join(out, f"{k}.wav")}
            for k, m in meta.items() if not os.path.exists(os.path.join(out, f"{k}.wav"))]
    spec = {"description": "", "seed": 0, "jobs": jobs}
    subprocess.run([sys.executable, "-I", "-X", "utf8", "-W", "ignore", os.path.join(HERE, "parler_say.py")],
                   input=json.dumps(spec, ensure_ascii=False).encode("utf-8"), check=True)


if __name__ == "__main__":
    main()
