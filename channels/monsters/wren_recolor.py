"""Wren's outfit and hair textures (Episode 2), painted over the hero's (Seed-san) textures so she shares Kai's toon
look but reads as her own person: a cream tunic with ochre trim, an olive under-flap, dark-brown leggings, leather
wrist cuffs, and plum-black hair. The hood, capelet, braids, satchel and bell are separate meshes (mk/wren.py).

    python3 channels/monsters/wren_recolor.py        -> assets/monsters/wren/{wear_wren,hair_wren}.png
"""
import os

import numpy as np
from PIL import Image

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SRC = os.path.join(ROOT, "assets", "monsters", "hero")
DST = os.path.join(ROOT, "assets", "monsters", "wren")


def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255


def load(path):
    return np.asarray(Image.open(path).convert("RGBA")).astype(np.float32) / 255


def ramp(px, mask, dark, light, lo, hi):
    """Map luminance inside `mask` onto dark->light (keeps the baked folds and shading)."""
    L = px[..., :3].mean(-1)
    t = np.clip((L - lo) / max(hi - lo, 1e-4), 0, 1)[..., None]
    px[..., :3] = np.where(mask[..., None], dark * (1 - t) + light * t, px[..., :3])


def main():
    os.makedirs(DST, exist_ok=True)
    wear = load(os.path.join(SRC, "wear_hero.png"))
    H, W = wear.shape[:2]
    rgb = wear[..., :3]
    yy, xx = np.mgrid[0:H, 0:W]
    sat = (rgb.max(-1) - rgb.min(-1)) / np.maximum(rgb.max(-1), 1e-4)
    L = rgb.mean(-1)
    teal = (sat > 0.3) & (rgb[..., 1] > rgb[..., 0] + 0.08) & (rgb[..., 2] > rgb[..., 0] + 0.05)
    white = (sat < 0.12) & (L > 0.72)
    tunic = (xx < 0.49 * W) & (yy < 0.46 * H)
    tee = tunic & (yy >= 300)
    sleeves = (xx >= 490) & (xx < 594) & (yy >= 105) & (yy < 466)
    wrap = (xx >= 676) & (xx < 886) & (yy < 286)
    pants = (xx < 0.65 * W) & (yy >= 0.46 * H) & (yy < 0.865 * H)
    dark = (sat < 0.3) & (L < 0.45)
    ramp(wear, teal & ~wrap, hexrgb("#a8916a"), hexrgb("#efe3c6"), 0.12, 0.62)        # cream tunic (was teal)
    ramp(wear, teal & wrap, hexrgb("#5a3a24"), hexrgb("#9a6a40"), 0.12, 0.62)          # leather wrist cuffs
    ramp(wear, dark & tee, hexrgb("#3f4a25"), hexrgb("#7e8c4c"), 0.08, 0.4)            # olive under-flap
    ramp(wear, dark & pants, hexrgb("#2c1f18"), hexrgb("#6a4b38"), 0.06, 0.38)         # dark-brown leggings
    ramp(wear, white & (tunic | sleeves | wrap), hexrgb("#a8711f"), hexrgb("#e4ad4c"), 0.7, 1.0)   # ochre trim
    z = (xx >= 360) & (xx < 380) & (yy >= 180) & (yy < 302)                            # no zip: plain tunic front
    wear[..., :3] = np.where(z[..., None], hexrgb("#e6d8b8"), wear[..., :3])
    Image.fromarray((np.clip(wear, 0, 1) * 255).astype(np.uint8)).save(os.path.join(DST, "wear_wren.png"))
    hair = load(os.path.join(SRC, "hair_hero.png"))
    ramp(hair, np.ones(hair.shape[:2], bool), hexrgb("#1a1424"), hexrgb("#5a477a"), 0.02, 0.3)   # plum-black
    Image.fromarray((np.clip(hair, 0, 1) * 255).astype(np.uint8)).save(os.path.join(DST, "hair_wren.png"))
    print("wrote", DST)


if __name__ == "__main__":
    main()
