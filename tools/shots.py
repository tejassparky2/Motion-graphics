"""Film-like still shots for the creepy stories, made locally and free: DreamShaper 8 (CreativeML OpenRAIL-M) with the
LCM LoRA (OpenRAIL++) so a shot needs only ~6 steps on the CPU. No paid service, nothing leaves the machine.

  python tools/shots.py shots.json OUT_DIR
  shots.json: [{"name": "a01", "prompt": "...", "seed": 1, "w": 512, "h": 896}, ...]
  Add "layout": "sketch.png" (+ "strength", default 0.7) to paint over a rough sketch, so the scary detail (a
  silhouette, eyes, a glow) lands exactly where the shot needs it. Add "seeds": [1, 2, 3] for several takes.

The main character (the channel's recurring MC) is described by MC below, so every shot draws the same boy.
"""
import json
import os
import sys

import torch
from diffusers import LCMScheduler, StableDiffusionImg2ImgPipeline, StableDiffusionPipeline
from PIL import Image

MC = "15 year old boy Milo, messy black hair, pale freckled face, plain red hoodie"
# Kept short: CLIP reads only 77 tokens, and the shot's own content comes first.
STYLE = "cinematic thriller film still, photorealistic, unreal engine 5 render, low-key lighting, volumetric light, film grain"
NEGATIVE = ("cartoon, anime, illustration, painting, flat colors, lowres, blurry, deformed, extra fingers, bad hands, "
            "bad anatomy, text, watermark, logo, signature, bright daylight, gore, blood")


def main():
    shots, out = json.load(open(sys.argv[1])), sys.argv[2]
    os.makedirs(out, exist_ok=True)
    torch.set_num_threads(os.cpu_count())
    pipe = StableDiffusionPipeline.from_pretrained("Lykon/dreamshaper-8", variant="fp16", torch_dtype=torch.float32,
                                                   safety_checker=None, requires_safety_checker=False)
    pipe.load_lora_weights("latent-consistency/lcm-lora-sdv1-5")
    pipe.fuse_lora()
    pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
    paint = StableDiffusionImg2ImgPipeline(**pipe.components)
    for s in shots:
        prompt = s["prompt"].replace("MC", MC) + ", " + STYLE
        for seed in s.get("seeds", [s.get("seed", 1)]):
            name = s["name"] + (f"_s{seed}" if "seeds" in s else "")
            if os.path.exists(os.path.join(out, f"{name}.png")):   # already made (re-runs only add what's missing)
                continue
            common = dict(negative_prompt=NEGATIVE, guidance_scale=s.get("cfg", 1.5),
                          generator=torch.Generator().manual_seed(seed))
            if s.get("layout"):
                sketch = Image.open(s["layout"]).convert("RGB").resize((s.get("w", 512), s.get("h", 896)))
                strength = s.get("strength", 0.7)
                img = paint(prompt, image=sketch, strength=strength,
                            num_inference_steps=max(s.get("steps", 8), round(6 / strength)), **common).images[0]
            else:
                img = pipe(prompt, num_inference_steps=s.get("steps", 8), width=s.get("w", 512),
                           height=s.get("h", 896), **common).images[0]
            img.save(os.path.join(out, f"{name}.png"))
            print("shot", name, flush=True)


if __name__ == "__main__":
    main()
