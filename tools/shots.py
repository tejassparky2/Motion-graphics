"""Film-like still shots for the creepy stories, made locally and free: DreamShaper 8 (CreativeML OpenRAIL-M) with the
LCM LoRA (OpenRAIL++) so a shot needs only ~6 steps on the CPU. No paid service, nothing leaves the machine.

  python tools/shots.py shots.json OUT_DIR
  shots.json: [{"name": "a01", "prompt": "...", "seed": 1, "w": 512, "h": 896}, ...]

The main character (the channel's recurring MC) is described by MC below, so every shot draws the same boy.
"""
import json
import os
import sys

import torch
from diffusers import LCMScheduler, StableDiffusionPipeline

MC = ("Milo, a 15 year old boy with messy black hair, pale freckled face, dark tired eyes, wearing a faded red hoodie")
STYLE = ("cinematic horror film still, photorealistic 3d render, unreal engine 5, dramatic low-key lighting, volumetric "
         "light, deep shadows, moody blue night tones, shallow depth of field, 35mm film grain, highly detailed")
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
    for s in shots:
        prompt = s["prompt"].replace("MC", MC) + ", " + STYLE
        img = pipe(prompt, negative_prompt=NEGATIVE, num_inference_steps=s.get("steps", 6),
                   guidance_scale=s.get("cfg", 1.5), width=s.get("w", 512), height=s.get("h", 896),
                   generator=torch.Generator().manual_seed(s.get("seed", 1))).images[0]
        img.save(os.path.join(out, f"{s['name']}.png"))
        print("shot", s["name"], flush=True)


if __name__ == "__main__":
    main()
