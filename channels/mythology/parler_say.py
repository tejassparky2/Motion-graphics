"""Batch voicing with the channel's designed Indic Parler-TTS voice. Runs in the separate Parler venv; narrate.py
calls it with a JSON job on stdin: {"description": str, "seed": int, "jobs": [{"text": str, "out": wav_path}, ...]}.
The model loads once per batch; every line uses the same description and seed so it stays one voice."""
import json, os, sys
import soundfile as sf
import torch
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from narrate import _key  # noqa: E402

MODEL = "ai4bharat/indic-parler-tts"

spec = json.loads(sys.stdin.read())
tok_hf = _key("HF_TOKEN")
dev = "cuda" if torch.cuda.is_available() else "cpu"
model = ParlerTTSForConditionalGeneration.from_pretrained(
    MODEL, token=tok_hf, torch_dtype=torch.float16 if dev == "cuda" else torch.float32).to(dev)
tok = AutoTokenizer.from_pretrained(MODEL, token=tok_hf)
dtok = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path, token=tok_hf)
for job in spec["jobs"]:                       # a job may override the batch's description and seed (voice search)
    desc_ids = dtok(job.get("description", spec["description"]), return_tensors="pt").input_ids.to(dev)
    torch.manual_seed(job.get("seed", spec["seed"]))
    g = model.generate(input_ids=desc_ids, prompt_input_ids=tok(job["text"], return_tensors="pt").input_ids.to(dev))
    sf.write(job["out"], g.to(torch.float32).cpu().numpy().squeeze(), model.config.sampling_rate)
    print("voiced", os.path.basename(job["out"]), flush=True)
