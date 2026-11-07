"""Voice the Kakudmi teaser (kn_voice_pick.SAMPLE) with IndicF5 from chosen described voices, through the channel's
real chain (tempo, studio, pauses), so the owner hears each one as it would sound in a reel.

  stem from kn_voice_design.py's folder -> its clip becomes myth_assets/voice/kn_refs/design_<stem>.wav (+ .txt)
  stem "aman_hindi"                     -> IndicF5 prompted straight from the Hindi narrator's own clip (Hindi
                                           words), speaking Kannada: the Hindi channel's voice itself
Writes myth_out/voice_samples/kannada_<stem>.wav/.m4a, and each line's raw take to <design_dir>/samples/ with
texts.json so kn_voice_design_score.py can check them.
Usage: <shorts research>/.venv-research/Scripts/python -I -X utf8 channels/mythology/kn_design_sample.py <design_dir> stem [stem ...]"""
import json, os, shutil, subprocess, sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import narrate  # noqa: E402
from channel import NARRATORS, OUT_ROOT, _KN_VOICES  # noqa: E402
from kn_voice_design import REF_TEXT  # noqa: E402
from kn_voice_pick import SAMPLE  # noqa: E402


def main():
    d, stems = sys.argv[1], sys.argv[2:]
    out_dir = os.path.join(OUT_ROOT, "voice_samples")
    lines_dir = os.path.join(d, "samples")
    os.makedirs(lines_dir, exist_ok=True)
    texts_path = os.path.join(lines_dir, "texts.json")
    texts = json.load(open(texts_path, encoding="utf-8")) if os.path.exists(texts_path) else {}
    for stem in stems:
        if stem == "aman_hindi":
            cfg = {**NARRATORS["kn"], "ref_audio": NARRATORS["hi"]["ref_audio"], "ref_text": NARRATORS["hi"]["ref_text"]}
        else:
            ref = os.path.join(_KN_VOICES, f"design_{stem}.wav")
            shutil.copyfile(os.path.join(d, f"{stem}.wav"), ref)
            with open(ref[:-4] + ".txt", "w", encoding="utf-8") as f:
                f.write(REF_TEXT)
            cfg = {**NARRATORS["kn"], "ref_audio": ref, "ref_text": REF_TEXT}
        narrate.prefetch([dict(text=t) for t in SAMPLE], cfg)
        parts = []
        for i, text in enumerate(SAMPLE):
            a, _, wav = narrate.take(text, cfg)
            k = f"{stem}_l{i + 1}"
            shutil.copyfile(wav, os.path.join(lines_dir, k + ".wav"))
            texts[k] = text
            parts += [np.zeros(int((0.1 if i == 0 else narrate.GAP) * narrate.SR)), a]
        parts.append(np.zeros(int(0.6 * narrate.SR)))
        a = np.concatenate(parts)
        path = os.path.join(out_dir, f"kannada_{stem}.wav")
        sf.write(path, a.astype(np.float32), narrate.SR)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", path, "-c:a", "aac", "-b:a", "192k",
                        "-map_metadata", "-1", path[:-4] + ".m4a"], check=True)
        print(f"{stem}: {len(a) / narrate.SR:.1f} s -> {path[:-4]}.m4a", flush=True)
    json.dump(texts, open(texts_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
