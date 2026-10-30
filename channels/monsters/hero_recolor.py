"""Restyle the Seed-san textures into the hero: sage-green tunic with cream trim, navy trousers, dark-brown hair."""
import sys

import numpy as np
from PIL import Image

V = sys.argv[1]


def hexrgb(h):
    return np.array([int(h[i:i + 2], 16) for i in (1, 3, 5)], np.float32) / 255


def recolor(px, mask, dark, light, lo=0.55, hi=1.0):
    """Map luminance inside `mask` onto a dark->light ramp of the new colour (keeps the baked folds and shading)."""
    L = px[..., :3].mean(-1)
    t = np.clip((L - lo) / (hi - lo), 0, 1)[..., None]
    new = dark * (1 - t) + light * t
    px[..., :3] = np.where(mask[..., None], new, px[..., :3])


wear = np.asarray(Image.open(f"{V}/tex/wear.png").convert("RGBA")).astype(np.float32) / 255
H, W = wear.shape[:2]
rgb = wear[..., :3]
mx, mn = rgb.max(-1), rgb.min(-1)
sat = (mx - mn) / np.maximum(mx, 1e-4)
L = rgb.mean(-1)
yy, xx = np.mgrid[0:H, 0:W]
blue = (sat > 0.35) & (rgb[..., 2] > rgb[..., 0] + 0.15)
white = (sat < 0.16) & (L > 0.5)
tunic = (xx < 0.49 * W) & (yy < 0.46 * H)
white = white | (tunic & (sat < 0.3) & (L > 0.45) & ~blue)          # the sleeves carry a blue-grey tint
# regions found by painting each texture piece by the body part it wraps (arms / chest / hips / legs)
sleeves = (xx >= 490) & (xx < 594) & (yy >= 105) & (yy < 466)
wrap = (xx >= 676) & (xx < 886) & (yy < 286)                         # the left forearm wrap
light = (sat < 0.3) & (L > 0.45) & ~blue
recolor(wear, light & sleeves, hexrgb("#4f7d5e"), hexrgb("#9cc7a3"))
recolor(wear, light & wrap, hexrgb("#1a1a20"), hexrgb("#3c3c48"))
pants = (xx < 0.65 * W) & (yy >= 0.46 * H) & (yy < 0.865 * H)
recolor(wear, white & tunic, hexrgb("#4f7d5e"), hexrgb("#9cc7a3"))
recolor(wear, white & pants, hexrgb("#1c2236"), hexrgb("#3b4670"))
recolor(wear, blue, hexrgb("#c99a5b"), hexrgb("#f3e3c0"), lo=0.3, hi=0.9)   # trim and accents: warm cream
Image.fromarray((np.clip(wear, 0, 1) * 255).astype(np.uint8)).save(f"{V}/tex/wear_hero.png")

hair = np.asarray(Image.open(f"{V}/tex/hair.png").convert("RGBA")).astype(np.float32) / 255
recolor(hair, np.ones(hair.shape[:2], bool), hexrgb("#24160f"), hexrgb("#7a5640"), lo=0.02, hi=0.3)
Image.fromarray((np.clip(hair, 0, 1) * 255).astype(np.uint8)).save(f"{V}/tex/hair_hero.png")
# the sample's right glove has blue gadget fingertips: give it the same bare fingers as the left glove
body = np.asarray(Image.open(f"{V}/tex/body.png").convert("RGBA")).astype(np.float32) / 255
b = body[..., :3]
bsat = (b.max(-1) - b.min(-1)) / np.maximum(b.max(-1), 1e-4)
bblue = (bsat > 0.35) & (b[..., 2] > b[..., 0] + 0.15)
src = body[0:140, 612:812].copy()
dst = body[0:140, 812:1012]
m = bblue[0:140, 812:1012]
dst[m] = src[m]
body[0:140, 812:1012] = dst

Image.fromarray((np.clip(body, 0, 1) * 255).astype(np.uint8)).save(f"{V}/tex/body_hero.png")
print("ok")
