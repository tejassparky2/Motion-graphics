"""Anime art for the story channels, generated on this CPU (report: reports/CPU anime animation pipeline.md).

Characters are painted ONCE (a bust on a white background), cut out, and reused in every shot; expressions, blinks and
mouth shapes are small img2img edits of the face, pasted back with a soft mask, so the character never drifts.
Backgrounds are painted without people. Everything is SD 1.5 Counterfeit-V3.0 (CreativeML OpenRAIL-M, selling images
allowed), bf16 on the Xeon's AMX; upscaled with Real-ESRGAN x4plus_anime_6B (BSD-3); cut out with skytnt/anime-seg
(Apache-2.0). Original characters only: prompts describe them, never name an existing one.

Runs in its own venv (torch CPU, diffusers, transformers, peft, onnxruntime, opencv-python-headless):
    PY tools/anime_assets.py cand  SPEC_MODULE NAME SEED[,SEED...]    candidates -> build/anime/cand/NAME_SEED.png
    PY tools/anime_assets.py char  SPEC_MODULE NAME                   chosen seed -> assets/anime/SET/NAME/base.png ...
    PY tools/anime_assets.py parts SPEC_MODULE NAME [PART...]         expression / blink / mouth patches
    PY tools/anime_assets.py bg    SPEC_MODULE NAME [SEED[,SEED...]]  painted background(s)
SPEC_MODULE is e.g. channels.stories.dma_cast (prompts, seeds and face boxes live there).
"""
import functools
import importlib
import json
import os
import sys
import time

import cv2
import numpy as np
import torch
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
torch.set_num_threads(int(os.environ.get("THREADS", "4")))
CKPT = ("gsdf/Counterfeit-V3.0", "Counterfeit-V3.0_fix_fp16.safetensors")
NEG = ("(worst quality, low quality:1.4), lowres, bad anatomy, bad hands, missing fingers, extra digits, text, "
       "watermark, signature, logo, blurry, jpeg artifacts, nsfw, 3d, realistic")


def log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)


# ------------------------------------------------------------------ models
@functools.lru_cache(maxsize=None)
def sd(kind="txt"):
    """txt2img / img2img pipelines sharing one bf16 Counterfeit model (DPM++ 2M Karras)."""
    from diffusers import (StableDiffusionPipeline, StableDiffusionImg2ImgPipeline, DPMSolverMultistepScheduler)
    from huggingface_hub import hf_hub_download
    if kind == "txt":
        p = StableDiffusionPipeline.from_single_file(hf_hub_download(*CKPT), torch_dtype=torch.bfloat16,
                                                     safety_checker=None)
        p.scheduler = DPMSolverMultistepScheduler.from_config(p.scheduler.config, use_karras_sigmas=True,
                                                              algorithm_type="dpmsolver++")
        p.unet.to(memory_format=torch.channels_last)
        p.vae.to(memory_format=torch.channels_last)
        p.set_progress_bar_config(disable=True)
        return p
    if kind == "lcm":                                                 # fast edits: LCM-LoRA, 6 steps, no CFG
        from diffusers import LCMScheduler
        from huggingface_hub import hf_hub_download
        p = StableDiffusionImg2ImgPipeline(**sd("txt").components)
        p.scheduler = LCMScheduler.from_config(p.scheduler.config)
        p.load_lora_weights(hf_hub_download("latent-consistency/lcm-lora-sdv1-5", "pytorch_lora_weights.safetensors"))
        p.fuse_lora()
        p.set_progress_bar_config(disable=True)
        return p
    p = StableDiffusionImg2ImgPipeline(**sd("txt").components)
    p.set_progress_bar_config(disable=True)
    return p


def txt2img(prompt, w, h, seed, steps=18, cfg=6.5, neg=""):
    g = torch.Generator().manual_seed(seed)
    with torch.inference_mode():
        return sd("txt")(prompt, negative_prompt=NEG + ", " + neg if neg else NEG, width=w, height=h,
                         num_inference_steps=steps, guidance_scale=cfg, generator=g).images[0]


def img2img(img, prompt, strength, seed, steps=20, cfg=6.5, neg="", fast=False):
    g = torch.Generator().manual_seed(seed)
    with torch.inference_mode():
        if fast:
            return sd("lcm")(prompt, image=img, strength=strength, num_inference_steps=8, guidance_scale=1.0,
                             generator=g).images[0]
        return sd("img")(prompt, image=img, strength=strength, negative_prompt=NEG + ", " + neg if neg else NEG,
                         num_inference_steps=steps, guidance_scale=cfg, generator=g).images[0]


class _RDB(torch.nn.Module):
    def __init__(self, nf=64, gc=32):
        super().__init__()
        self.conv1 = torch.nn.Conv2d(nf, gc, 3, 1, 1)
        self.conv2 = torch.nn.Conv2d(nf + gc, gc, 3, 1, 1)
        self.conv3 = torch.nn.Conv2d(nf + 2 * gc, gc, 3, 1, 1)
        self.conv4 = torch.nn.Conv2d(nf + 3 * gc, gc, 3, 1, 1)
        self.conv5 = torch.nn.Conv2d(nf + 4 * gc, nf, 3, 1, 1)
        self.lrelu = torch.nn.LeakyReLU(0.2, True)

    def forward(self, x):
        x1 = self.lrelu(self.conv1(x))
        x2 = self.lrelu(self.conv2(torch.cat((x, x1), 1)))
        x3 = self.lrelu(self.conv3(torch.cat((x, x1, x2), 1)))
        x4 = self.lrelu(self.conv4(torch.cat((x, x1, x2, x3), 1)))
        return self.conv5(torch.cat((x, x1, x2, x3, x4), 1)) * 0.2 + x


class _RRDB(torch.nn.Module):
    def __init__(self, nf, gc):
        super().__init__()
        self.rdb1, self.rdb2, self.rdb3 = _RDB(nf, gc), _RDB(nf, gc), _RDB(nf, gc)

    def forward(self, x):
        return self.rdb3(self.rdb2(self.rdb1(x))) * 0.2 + x


class _RRDBNet(torch.nn.Module):
    """Real-ESRGAN's RRDBNet (BSD-3), x4; the anime_6B weights use 6 blocks."""
    def __init__(self, nb=6, nf=64, gc=32):
        super().__init__()
        self.conv_first = torch.nn.Conv2d(3, nf, 3, 1, 1)
        self.body = torch.nn.Sequential(*[_RRDB(nf, gc) for _ in range(nb)])
        self.conv_body = torch.nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_up1 = torch.nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_up2 = torch.nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_hr = torch.nn.Conv2d(nf, nf, 3, 1, 1)
        self.conv_last = torch.nn.Conv2d(nf, 3, 3, 1, 1)
        self.lrelu = torch.nn.LeakyReLU(0.2, True)

    def forward(self, x):
        f = self.conv_first(x)
        f = f + self.conv_body(self.body(f))
        f = self.lrelu(self.conv_up1(torch.nn.functional.interpolate(f, scale_factor=2, mode="nearest")))
        f = self.lrelu(self.conv_up2(torch.nn.functional.interpolate(f, scale_factor=2, mode="nearest")))
        return self.conv_last(self.lrelu(self.conv_hr(f)))


@functools.lru_cache(maxsize=None)
def esrgan():
    m = _RRDBNet()
    path = os.environ.get("ESRGAN_6B", os.path.join(ROOT, "build", "anime", "RealESRGAN_x4plus_anime_6B.pth"))
    m.load_state_dict(torch.load(path, map_location="cpu")["params_ema"])
    return m.eval().to(memory_format=torch.channels_last)


def upscale(img, factor=2, tile=256):
    """Real-ESRGAN anime x4 in bf16 tiles, then resized to `factor`x."""
    a = torch.from_numpy(np.asarray(img.convert("RGB"), np.float32) / 255).permute(2, 0, 1)[None]
    _, _, h, w = a.shape
    out = torch.zeros(1, 3, h * 4, w * 4)
    pad = 12
    with torch.inference_mode(), torch.autocast("cpu", dtype=torch.bfloat16):
        for y in range(0, h, tile):
            for x in range(0, w, tile):
                y0, x0, y1, x1 = max(0, y - pad), max(0, x - pad), min(h, y + tile + pad), min(w, x + tile + pad)
                o = esrgan()(a[:, :, y0:y1, x0:x1].contiguous(memory_format=torch.channels_last)).float()
                oy, ox = (y - y0) * 4, (x - x0) * 4
                th, tw = min(tile, h - y) * 4, min(tile, w - x) * 4
                out[:, :, y * 4:y * 4 + th, x * 4:x * 4 + tw] = o[:, :, oy:oy + th, ox:ox + tw]
    big = (out[0].permute(1, 2, 0).clamp(0, 1).numpy() * 255 + 0.5).astype(np.uint8)
    if factor != 4:
        big = cv2.resize(big, (w * factor, h * factor), interpolation=cv2.INTER_AREA)
    return Image.fromarray(big)


@functools.lru_cache(maxsize=None)
def seg_model():
    import onnxruntime as ort
    from huggingface_hub import hf_hub_download
    return ort.InferenceSession(hf_hub_download("skytnt/anime-seg", "isnetis.onnx"), providers=["CPUExecutionProvider"])


def alpha_mask(img, s=1024):
    """skytnt/anime-seg (ISNet): a 0..1 foreground mask for an anime character image."""
    a = np.asarray(img.convert("RGB"), np.float32) / 255
    h, w = a.shape[:2]
    k = s / max(h, w)
    nh, nw = int(h * k), int(w * k)
    inp = np.zeros((s, s, 3), np.float32)
    py, px = (s - nh) // 2, (s - nw) // 2
    inp[py:py + nh, px:px + nw] = cv2.resize(a, (nw, nh))
    m = seg_model().run(None, {seg_model().get_inputs()[0].name: inp.transpose(2, 0, 1)[None]})[0][0, 0]
    return cv2.resize(m[py:py + nh, px:px + nw], (w, h))


def cutout(img):
    m = alpha_mask(img)
    m = np.clip((m - 0.08) / 0.84, 0, 1)                       # firm edges, keep soft hair tips
    rgba = np.dstack([np.asarray(img.convert("RGB")), (m * 255 + 0.5).astype(np.uint8)])
    return Image.fromarray(rgba, "RGBA")


def soft_ellipse(w, h, box, feather):
    """A 0..1 elliptical mask over box (x0, y0, x1, y1), feathered by `feather` px."""
    m = np.zeros((h, w), np.float32)
    x0, y0, x1, y1 = box
    cv2.ellipse(m, (int((x0 + x1) / 2), int((y0 + y1) / 2)), (int((x1 - x0) / 2), int((y1 - y0) / 2)), 0, 0, 360, 1.0,
                -1)
    return cv2.GaussianBlur(m, (0, 0), feather) if feather else m


# ------------------------------------------------------------------ jobs
def spec_of(mod, name):
    s = importlib.import_module(mod)
    return s, (s.CHARS.get(name) or s.BGS.get(name))


def char_neg(s, c):
    return ", ".join(filter(None, (getattr(s, "CHAR_NEG", ""), c.get("neg", ""))))


def char_img(s, c, seed):
    if hasattr(s, "CHAR_NEG_FULL"):                                   # the spec gives the whole negative prompt
        g = torch.Generator().manual_seed(seed)
        with torch.inference_mode():
            return sd("txt")(s.CHAR_PROMPT.format(**c), negative_prompt=", ".join(filter(None, (c.get("neg"),
                             s.CHAR_NEG_FULL))), width=512, height=768, num_inference_steps=18, guidance_scale=6.5,
                             generator=g).images[0]
    return txt2img(s.CHAR_PROMPT.format(**c), 512, 768, seed, neg=char_neg(s, c))


def out_dir(s, *parts):
    d = os.path.join(ROOT, "assets", "anime", s.SET, *parts)
    os.makedirs(d, exist_ok=True)
    return d


def cand(mod, name, seeds):
    s, c = spec_of(mod, name)
    d = os.path.join(ROOT, "build", "anime", "cand")
    os.makedirs(d, exist_ok=True)
    for seed in seeds:
        t = time.time()
        img = char_img(s, c, seed)
        img.save(os.path.join(d, f"{s.SET}_{name}_{seed}.png"))
        log(f"cand {name} {seed}: {time.time() - t:.0f}s")


def char(mod, name):
    """The chosen candidate -> 2x upscale (1024x1536) -> cutout base.png (+ the 512 original kept for edits)."""
    s, c = spec_of(mod, name)
    d = out_dir(s, name)
    t = time.time()
    cpath = os.path.join(ROOT, "build", "anime", "cand", f"{s.SET}_{name}_{c['seed']}.png")
    img = Image.open(cpath).convert("RGB") if os.path.exists(cpath) else \
        char_img(s, c, c["seed"])
    img.save(os.path.join(d, "src512.png"))
    big = upscale(img)
    cut = cutout(big)
    a = np.array(cut)
    if c.get("clean_light_below"):                    # drop pale stray shapes (smoke, clouds) below a line
        y0 = c["clean_light_below"] * 2
        lum = a[y0:, :, :3].mean(axis=2)
        a[y0:, :, 3][lum > 175] = 0
    for x0, y0, x1, y1 in c.get("clear", ()):         # stray props the model painted (512x768 coordinates)
        a[y0 * 2:y1 * 2, x0 * 2:x1 * 2, 3] = 0
    for x0, y0, x1, y1 in c.get("clear_light", ()):   # ... only their pale parts, where they touch the body
        reg = a[y0 * 2:y1 * 2, x0 * 2:x1 * 2]
        reg[..., 3][reg[..., :3].mean(axis=2) > 110] = 0
    cut = Image.fromarray(a, "RGBA")
    cut.save(os.path.join(d, "base.png"))
    log(f"char {name}: {time.time() - t:.0f}s")


def parts(mod, name, which=None):
    """Face patches: each is an img2img edit of the face crop, pasted back over the base with a feathered ellipse.
    Saved as RGBA PNGs at full (2x) size, cropped to their box, with offsets in parts.json."""
    s, c = spec_of(mod, name)
    d = out_dir(s, name)
    src = Image.open(os.path.join(d, "src512.png")).convert("RGB")
    fx0, fy0, fx1, fy1 = c["face"]                                   # face box in 512x768 coords (square-ish)
    side = max(fx1 - fx0, fy1 - fy0)
    cx, cy = (fx0 + fx1) / 2, (fy0 + fy1) / 2
    box = [int(cx - side / 2), int(cy - side / 2), int(cx + side / 2), int(cy + side / 2)]
    S = int(os.environ.get("PART_SIZE", "384"))                     # edit size (the face is ~200 px in the source)
    crop = src.crop(box).resize((S, S), Image.LANCZOS)
    k = S / side
    meta_path = os.path.join(d, "parts.json")
    meta = json.load(open(meta_path)) if os.path.exists(meta_path) else {}
    jobs = s.PARTS(c)
    for pname, (prompt, strength, region) in jobs.items():
        if which and pname not in which:
            continue
        t = time.time()
        base_face = crop
        if "+" in pname:                                              # e.g. "fear+blink": edit the fear face
            parent = pname.split("+")[0]
            base_face = Image.open(os.path.join(d, f"_face_{parent}.png")).convert("RGB")
        fast = region != "face" and os.environ.get("PART_LCM", "1") == "1"   # eyes / mouth: LCM (the full sampler
        #                                                                       did no better on blinks, 5x slower)
        out = img2img(base_face, s.FACE_PROMPT.format(**c) + ", " + prompt, strength, c["seed"] + 7, fast=fast)
        if region == "face":                                          # expression faces are edited further
            out.save(os.path.join(d, f"_face_{pname}.png"))
        rx0, ry0, rx1, ry1 = [(v - box[i % 2]) * k for i, v in enumerate(c[region])] if region != "face" else \
            (S * 0.08, S * 0.08, S * 0.92, S * 0.92)
        m = soft_ellipse(S, S, (rx0, ry0, rx1, ry1), S * 0.02 if region != "face" else S * 0.045)
        ring = (m > 0.05) & (m < 0.6)                                 # match the patch's colour to its surroundings
        if ring.any():
            o = np.asarray(out, np.float32)
            shift = np.asarray(base_face, np.float32)[ring].mean(0) - o[ring].mean(0)
            out = Image.fromarray(np.clip(o + shift, 0, 255).astype(np.uint8))
        size = int(round(side * 2))                                   # the crop is shown at 2x: S -> 2*side
        up = out.resize((size, size), Image.LANCZOS)
        mk = cv2.resize(m, (size, size))
        ys, xs = np.nonzero(mk > 0.01)
        y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        rgba = np.dstack([np.asarray(up)[y0:y1, x0:x1], (mk[y0:y1, x0:x1] * 255 + 0.5).astype(np.uint8)])
        Image.fromarray(rgba, "RGBA").save(os.path.join(d, f"{pname}.png"))
        meta[pname] = dict(x=int(box[0] * 2 + x0), y=int(box[1] * 2 + y0))
        json.dump(meta, open(meta_path, "w"), indent=1)
        log(f"part {name}/{pname}: {time.time() - t:.0f}s")


def bg(mod, name, seeds=None):
    s, b = spec_of(mod, name)
    w, h = b.get("size", (512, 768))
    for seed in (seeds or [b["seed"]]):
        t = time.time()
        cpath = os.path.join(ROOT, "build", "anime", "cand", f"{s.SET}_bg_{name}_{seed}.png")
        if not seeds and os.path.exists(cpath):                       # the chosen candidate: no need to paint again
            img = Image.open(cpath).convert("RGB")
        else:
            img = txt2img(s.BG_PROMPT.format(**b), w, h, seed, steps=b.get("steps", 18), neg=b.get("neg", ""))
        if not seeds and b.get("flip"):
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        if seeds:
            dd = os.path.join(ROOT, "build", "anime", "cand")
            os.makedirs(dd, exist_ok=True)
            img.save(os.path.join(dd, f"{s.SET}_bg_{name}_{seed}.png"))
        else:
            upscale(img).save(os.path.join(out_dir(s, "bg"), f"{name}.png"))
        log(f"bg {name} {seed}: {time.time() - t:.0f}s")


if __name__ == "__main__":
    cmd, mod, name = sys.argv[1:4]
    rest = sys.argv[4:]
    if cmd == "cand":
        cand(mod, name, [int(x) for x in rest[0].split(",")])
    elif cmd == "char":
        char(mod, name)
    elif cmd == "parts":
        parts(mod, name, rest or None)
    elif cmd == "bg":
        bg(mod, name, [int(x) for x in rest[0].split(",")] if rest else None)
