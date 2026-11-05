"""Rank the Kannada narrator candidates from kn_voice_search.py, then voice a short sample through the real pipeline.

  score:  Whisper medium (language "kn") word error against the passage, pitch movement (SD in semitones; the
          Hindi narrator's lively lines sit at ~5 st), length and median pitch -> <dir>/ranking.json
  sample: copies each chosen candidate to myth_assets/voice/kn_refs/<stem>.wav and voices SAMPLE with IndicF5 from
          it, line by line, with the channel's tempo, studio chain and pauses -> myth_out/voice_samples/<stem>.wav/.m4a

Whisper is weak in Kannada, so the score only shortlists; the owner's ear picks.
Usage: python -I -X utf8 channels/mythology/kn_voice_pick.py score <dir>
       python -I -X utf8 channels/mythology/kn_voice_pick.py sample <dir> stem [stem ...]
"""
import json, os, shutil, subprocess, sys
import numpy as np, librosa, soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import narrate  # noqa: E402
from channel import KN_REF_TEXT, NARRATORS, OUT_ROOT, _KN_VOICES  # noqa: E402

# Original Kannada lines (a teaser of the Kakudmi story, Bhagavata Purana 9.3): about 15-20 s spoken.
SAMPLE = ["ಯೋಚಿಸಿ, ಒಬ್ಬ ರಾಜ ಬ್ರಹ್ಮದೇವರ ಮುಂದೆ ಕೆಲವೇ ಕ್ಷಣ ಕಾದು ನಿಂತ.",
          "ಆದರೆ ಅವನು ಭೂಮಿಗೆ ಹಿಂತಿರುಗಿದಾಗ... ಕೋಟ್ಯಂತರ ವರ್ಷಗಳು ಕಳೆದಿದ್ದವು.",
          "ಇದು ಯಾವುದೋ ಸಿನಿಮಾ ಕಥೆ ಅಲ್ಲ. ಭಾಗವತ ಪುರಾಣದಲ್ಲೇ ಈ ಕಥೆ ಇದೆ.",
          "ಅವನ ಮಂತ್ರಿಗಳು, ಅವನ ಬಂಧುಗಳು, ಅವನ ವಂಶ... ಯಾರೂ ಉಳಿದಿರಲಿಲ್ಲ."]


def pitch(y):
    f0, v, _ = librosa.pyin(y, fmin=65, fmax=450, sr=16000)
    f0 = f0[v]
    return float(np.median(f0)), float((12 * np.log2(f0 / np.median(f0))).std())


def score(d):
    from asr import whisper
    from render_myth import wer, words
    model = whisper()
    rows = {}
    for f in sorted(os.listdir(d)):
        if not f.endswith(".wav"):
            continue
        y, _ = librosa.load(os.path.join(d, f), sr=16000)
        y, _ = librosa.effects.trim(y, top_db=35)
        heard = " ".join(s.text for s in model.transcribe(y, language="kn", beam_size=5)[0]).strip()
        med, sd = pitch(y)
        rows[f[:-4]] = dict(wer=round(wer(words(KN_REF_TEXT), words(heard)), 3), sd=round(sd, 2),
                            f0=round(med), secs=round(len(y) / 16000, 2), heard=heard)
        r = rows[f[:-4]]
        print(f"{f[:-4]:>12}  WER {r['wer']:4.0%}  SD {r['sd']:.1f} st  f0 {r['f0']} Hz  {r['secs']:.1f} s  {heard[:60]}",
              flush=True)
    json.dump(rows, open(os.path.join(d, "ranking.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def sample(d, stems):
    from asr import whisper
    from render_myth import wer, words
    out_dir = os.path.join(OUT_ROOT, "voice_samples")
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(_KN_VOICES, exist_ok=True)
    model = whisper()
    for stem in stems:
        ref = os.path.join(_KN_VOICES, f"{stem}.wav")
        shutil.copyfile(os.path.join(d, f"{stem}.wav"), ref)
        cfg = {**NARRATORS["kn"], "ref_audio": ref}
        narrate.prefetch([dict(text=t) for t in SAMPLE], cfg)
        parts = []
        for i, text in enumerate(SAMPLE):
            a, _, wav = narrate.take(text, cfg)
            y, _ = librosa.load(wav, sr=16000)
            heard = " ".join(s.text for s in model.transcribe(y, language="kn", beam_size=5)[0]).strip()
            print(f"{stem} line {i + 1}: WER {wer(words(text), words(heard)):4.0%}  {heard}", flush=True)
            parts += [np.zeros(int(0.1 * narrate.SR)) if i == 0 else np.zeros(int(narrate.GAP * narrate.SR)), a]
        parts.append(np.zeros(int(0.6 * narrate.SR)))
        a = np.concatenate(parts)
        path = os.path.join(out_dir, f"kannada_{stem}.wav")
        sf.write(path, a.astype(np.float32), narrate.SR)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-c:a", "aac", "-b:a", "192k",
                        "-map_metadata", "-1", path[:-4] + ".m4a"], check=True)
        print(f"{stem}: {len(a) / narrate.SR:.1f} s -> {path[:-4]}.m4a", flush=True)


if __name__ == "__main__":
    if sys.argv[1] == "score":
        score(sys.argv[2])
    else:
        sample(sys.argv[2], sys.argv[3:])
