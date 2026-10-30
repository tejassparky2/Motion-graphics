"""Hero outfit textures, painted over the Seed-san sample's (owner, 30 Oct 2026: "change his dress, take inspiration
from Pokémon and modern anime"). A modern anime protagonist look: a colour-blocked teal short jacket with a white
zip line and white trim over a long white tee, charcoal joggers, bare forearms with black fingerless gloves, a teal
sweatband. Regions were found by painting each texture piece by the body part it wraps (see NOTES.md).

    python3 channels/monsters/hero_recolor.py SRC_DIR      (SRC_DIR/tex holds the sample's wear.png, hair.png, body.png)
writes SRC_DIR/tex/{wear_hero,wear_earth,hair_hero,body_hero}.png."""
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


def load(name):
    return np.asarray(Image.open(f"{V}/tex/{name}.png").convert("RGBA")).astype(np.float32) / 255


def save(px, name):
    Image.fromarray((np.clip(px, 0, 1) * 255).astype(np.uint8)).save(f"{V}/tex/{name}.png")


def outfit(pal):
    wear = load("wear")
    H, W = wear.shape[:2]
    rgb = wear[..., :3]
    sat = (rgb.max(-1) - rgb.min(-1)) / np.maximum(rgb.max(-1), 1e-4)
    L = rgb.mean(-1)
    yy, xx = np.mgrid[0:H, 0:W]
    blue = (sat > 0.35) & (rgb[..., 2] > rgb[..., 0] + 0.15)
    light = (sat < 0.3) & (L > 0.45) & ~blue
    tunic = (xx < 0.49 * W) & (yy < 0.46 * H)
    jacket = tunic & (yy < 300)                                 # above the belt seam: the short jacket
    tee = tunic & (yy >= 300)                                   # below it: the long tee hanging out
    sleeves = (xx >= 490) & (xx < 594) & (yy >= 105) & (yy < 466)
    wrap = (xx >= 676) & (xx < 886) & (yy < 286)                # the left forearm wrap -> a sweatband
    pants = (xx < 0.65 * W) & (yy >= 0.46 * H) & (yy < 0.865 * H)
    recolor(wear, light & (jacket | sleeves), *pal["jacket"])
    recolor(wear, light & tee, *pal["tee"])
    recolor(wear, light & wrap, *pal["band"])
    recolor(wear, light & pants, *pal["pants"])
    recolor(wear, blue & ~tee, *pal["trim"], lo=0.3, hi=0.9)    # collar, cuffs and the jacket hem
    recolor(wear, blue & tee, *pal["tee"], lo=0.3, hi=0.9)      # the lower flap's hem matches the flap
    # a zip line down the jacket front (the front piece's centre, from the collar slit to the belt seam)
    z = (xx >= 366) & (xx < 373) & (yy >= 186) & (yy < 300)
    wear[..., :3] = np.where(z[..., None], pal["zip"], wear[..., :3])
    pull = (xx >= 362) & (xx < 377) & (yy >= 186) & (yy < 200)
    wear[..., :3] = np.where(pull[..., None], pal["zip"] * 0.8, wear[..., :3])
    return wear


WORLD = dict(jacket=(hexrgb("#11635e"), hexrgb("#2fbcb0")), tee=(hexrgb("#23262f"), hexrgb("#555b6b")),
             band=(hexrgb("#11635e"), hexrgb("#2fbcb0")), pants=(hexrgb("#1c1f27"), hexrgb("#4a4f5e")),
             trim=(hexrgb("#c9ced6"), hexrgb("#ffffff")), zip=hexrgb("#ffffff"))
EARTH = dict(jacket=(hexrgb("#2e323a"), hexrgb("#7a818e")), tee=(hexrgb("#8d939e"), hexrgb("#d8dce3")),
             band=(hexrgb("#2e323a"), hexrgb("#7a818e")), pants=(hexrgb("#1f2a3d"), hexrgb("#4a5f80")),
             trim=(hexrgb("#8d939e"), hexrgb("#d8dce3")), zip=hexrgb("#d8dce3"))
save(outfit(WORLD), "wear_hero")
save(outfit(EARTH), "wear_earth")

hair = load("hair")
recolor(hair, np.ones(hair.shape[:2], bool), hexrgb("#24160f"), hexrgb("#7a5640"), lo=0.02, hi=0.3)
save(hair, "hair_hero")

# skin texture: bare forearms (the sample's black arm-warmers painted skin) and the right glove's blue gadget
# fingertips replaced by the left glove's bare fingers
body = load("body")
b = body[..., :3]
bsat = (b.max(-1) - b.min(-1)) / np.maximum(b.max(-1), 1e-4)
bblue = (bsat > 0.35) & (b[..., 2] > b[..., 0] + 0.15)
src = body[0:140, 612:812].copy()
dst = body[0:140, 812:1012]
m = bblue[0:140, 812:1012]
dst[m] = src[m]
body[0:140, 812:1012] = dst
H, W = body.shape[:2]
yy, xx = np.mgrid[0:H, 0:W]
arms = (xx >= 776) & (xx < 1016) & (yy >= 448) & (yy < 660)
dark = b.max(-1) < 0.42
skin_lit, skin_shade = hexrgb("#fbe3d2"), hexrgb("#efc6b0")
t = np.clip((yy - 448) / 212.0, 0, 1)[..., None]               # a soft top-to-bottom shade along the arm piece
skin = skin_lit * (1 - t * 0.6) + skin_shade * (t * 0.6)
body[..., :3] = np.where((arms & dark)[..., None], skin, body[..., :3])
save(body, "body_hero")
print("ok")
