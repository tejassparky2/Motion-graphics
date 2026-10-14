import sys, torch, soundfile as sf
from chatterbox.mtl_tts import ChatterboxMultilingualTTS
out = sys.argv[1]
m = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
text = ("सर, क्या भगवान इतना भारी पत्थर बना सकते हैं, कि वो खुद भी उसे उठा न सकें? "
        "पूरी क्लास एकदम चुप। और टीचर? वो बस मुस्कुराए।")
prompt = "/home/user/Motion-graphics/assets/voice/owner_prompt_fast.wav"
for name, p, ex, cfg in (("default_calm", None, 0.5, 0.5), ("default_emotional", None, 0.85, 0.35),
                         ("owner_voice_emotional", prompt, 0.85, 0.35)):
    torch.manual_seed(7)
    w = m.generate(text, language_id="hi", audio_prompt_path=p, exaggeration=ex, cfg_weight=cfg)
    sf.write(f"{out}/{name}.wav", w.squeeze(0).numpy(), m.sr)
    print(name, round(w.shape[-1] / m.sr, 1), "s", flush=True)
