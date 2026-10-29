"""Design the channel's own narrator with Indic Parler-TTS (AI4Bharat, Apache-2.0): the voice comes from a written
description, not from anyone's recording.

Generates the voice-test passage for a grid of descriptions (named Indic Parler speakers x pitch x expressivity x
seed), so the candidates can be scored on pitch (target ~145 Hz), pace (~190 wpm) and Whisper clarity.
With --lines, re-voices three different script lines with one chosen description + seed to check it stays the
same voice.

Needs HF_TOKEN (the model is gated: accept its terms on huggingface.co first). Runs in the separate Parler venv:
  .venv-parler\\Scripts\\python -I -X utf8 channels/hinglish/design_voice.py <out_dir>
  .venv-parler\\Scripts\\python -I -X utf8 channels/hinglish/design_voice.py <out_dir> --lines "<name>"
"""
import itertools, json, os, sys
import soundfile as sf
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from design_voice_text import TEXT  # noqa: E402
from narrate import _key  # noqa: E402

MODEL = "ai4bharat/indic-parler-tts"
LINES = ["सोचो, एक ऐसा चूहा जो बिल्ली की स्मेल से भागता नहीं... बल्कि ख़ुद चल के उसकी तरफ़ जाता है।",
         "फिर ये पैरासाइट चूहे के दिमाग़ तक पहुँचता है, और वहाँ छोटे-छोटे सिस्ट्स बना के छुप जाता है।",
         "आपके घर में बिल्ली है? और क्या आपको ये पता था? कमेंट में बताइए।"]
SPEAKERS = ["Rohit", "Aman"]
PITCH = {"mid": "a moderate pitch", "midhigh": "a slightly high pitch"}
EXPR = {"calm": "a calm, clear and slightly expressive tone", "lively": "a clear, engaging and expressive tone"}
SEEDS = [3, 11]


def describe(spk, pitch, expr):
    return (f"{spk} speaks with {PITCH[pitch]} in {EXPR[expr]}, at a fast pace, like a documentary narrator "
            f"explaining a surprising fact. The recording is very clear and close-sounding, with no background noise.")


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    tok_hf = _key("HF_TOKEN")
    if not tok_hf:
        sys.exit("HF_TOKEN is not set (and accept the model's terms on huggingface.co/ai4bharat/indic-parler-tts)")
    dev = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if dev == "cuda" else torch.float32
    model = ParlerTTSForConditionalGeneration.from_pretrained(MODEL, token=tok_hf, torch_dtype=dtype).to(dev)
    tok = AutoTokenizer.from_pretrained(MODEL, token=tok_hf)
    dtok = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path, token=tok_hf)
    sr = model.config.sampling_rate

    def say(text, desc, seed, path):
        torch.manual_seed(seed)
        g = model.generate(input_ids=dtok(desc, return_tensors="pt").input_ids.to(dev),
                           prompt_input_ids=tok(text, return_tensors="pt").input_ids.to(dev))
        a = g.to(torch.float32).cpu().numpy().squeeze()
        sf.write(path, a, sr)
        return len(a) / sr

    if "--lines" in sys.argv:                       # consistency check for one chosen candidate
        name = sys.argv[sys.argv.index("--lines") + 1]
        spk, pitch, expr, seed = name.split("_")
        desc = describe(spk, pitch, expr)
        for i, line in enumerate(LINES):
            d = say(line, desc, int(seed[1:]), os.path.join(out, f"{name}_line{i + 1}.wav"))
            print(f"{name} line {i + 1}: {d:.1f} s", flush=True)
        return
    meta = {}
    for spk, pitch, expr, seed in itertools.product(SPEAKERS, PITCH, EXPR, SEEDS):
        name = f"{spk}_{pitch}_{expr}_s{seed}"
        desc = describe(spk, pitch, expr)
        d = say(TEXT, desc, seed, os.path.join(out, f"{name}.wav"))
        meta[name] = desc
        print(f"{name}: {d:.1f} s", flush=True)
    json.dump(meta, open(os.path.join(out, "descriptions.json"), "w", encoding="utf-8"), indent=1)


main()
