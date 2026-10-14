"""Indic Parler-TTS (AI4Bharat, Apache-2.0; gated on Hugging Face: needs HF_TOKEN). Hinglish samples with the delivery described in words.
   Setup: python3 -m venv --system-site-packages ~/.venv-indic; pip install parler-tts; pip install torch==2.11.0 torchaudio==2.11.0+cpu (CPU index).
   Run:   ~/.venv-indic/bin/python tools/hindi_parler_test.py OUT_DIR"""
import sys, torch, soundfile as sf
from parler_tts import ParlerTTSForConditionalGeneration
from transformers import AutoTokenizer
out = sys.argv[1]
name = "ai4bharat/indic-parler-tts"
model = ParlerTTSForConditionalGeneration.from_pretrained(name)
tok = AutoTokenizer.from_pretrained(name)
dtok = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
text = ("सर, क्या भगवान इतना heavy पत्थर बना सकते हैं, कि वो खुद भी उसे lift ना कर पाएं? "
        "पूरी class एकदम silent. और teacher? वो बस smile करते रहे।")
styles = {
    "rohit_storyteller": "Rohit speaks in a very expressive and animated tone, like an excited storyteller, at a "
                         "moderately fast pace with dramatic pauses. The recording is very clear, close-sounding, "
                         "with no background noise.",
    "aman_dramatic": "Aman delivers a dramatic, suspenseful narration with high expressivity and varied pitch, at a "
                     "moderate pace. The recording is very clear and close-sounding, with no background noise.",
    "divya_storyteller": "Divya speaks in a lively, expressive and animated tone, like a storyteller, at a "
                         "moderately fast pace. The recording is very clear, with no background noise.",
}
for k, desc in styles.items():
    torch.manual_seed(3)
    g = model.generate(input_ids=dtok(desc, return_tensors="pt").input_ids,
                       prompt_input_ids=tok(text, return_tensors="pt").input_ids)
    a = g.cpu().numpy().squeeze()
    sf.write(f"{out}/{k}.wav", a, model.config.sampling_rate)
    print(k, round(len(a) / model.config.sampling_rate, 1), "s", flush=True)
