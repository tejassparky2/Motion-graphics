#!/usr/bin/env python3
"""Asset prep for the Brahma-and-the-calves reel (scenes_brahma_calves.py): cuts figures out of the Cleveland Museum
of Art paintings (CC0) and fills the holes they leave in the painting, so the layers can move as a multiplane camera
without a ghost double.

  python -I -X utf8 channels/mythology/bc_prep.py            # every cut-out and plate that is missing
  python -I -X utf8 channels/mythology/bc_prep.py --force boys_lunch plate_146117

Cut-outs: rembg with an explicit model (BiRefNet general lite or IS-Net general use; never rembg's default model).
Hole fill: LaMa (Carve/LaMa-ONNX, Apache-2.0) on CPU, run per hole on a square crop around it at 512 x 512, then
scaled back and blended in with a feathered mask and a little grain so the fill matches the painting's surface.
Outputs: <myth_assets>/brahma_calves/layers/<name>.png and layers/index.json (where each cut-out sat in its painting).
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from channel import ASSETS_ROOT  # noqa: E402

SRC = os.path.join(ASSETS_ROOT, "brahma_calves")
OUT = os.path.join(SRC, "layers")
LAMA = os.path.join(ASSETS_ROOT, "models", "lama_fp32.onnx")

# name: (painting file, crop box as fractions x0, y0, x1, y1, rembg model, keep-only boxes in crop fractions or None)
# ADD: soft ellipses (source px: cx, cy, rx, ry) forced into a cut-out where the model missed a thin detail
ADD = {"boys_lunch": [(632, 1040, 80, 34)]}  # Krishna's peacock-feather crest (left behind on the plate otherwise)
CUTS = {
    "brahma_k": ("cma_162498_brahma_kalighat.jpg", (0.0, 0.03, 1.0, 1.0), "birefnet-general-lite", None),
    "boys_lunch": ("cma_146117_krishna_returns_braj.jpg", (0.0, 0.42, 0.40, 0.90), "birefnet-general-lite", None),
    "swan_146": ("cma_146117_krishna_returns_braj.jpg", (0.13, 0.0, 0.33, 0.22), "birefnet-general-lite",
                 [(0.0, 0.0, 1.0, 0.84)]),
    "swan_141": ("cma_141755_brahma_hides.jpg", (0.17, 0.11, 0.47, 0.50), "birefnet-general-lite", None),
    "krishna_flute": ("cma_314462_krishna_fluting.jpg", (0.38, 0.20, 0.70, 0.67), "birefnet-general-lite", None),
    "two_boys": ("cma_145241_friends_of_krishna.jpg", (0.53, 0.45, 0.77, 0.93), "birefnet-general-lite", None),
    "boy_red": ("cma_145241_friends_of_krishna.jpg", (0.535, 0.45, 0.668, 0.93), "birefnet-general-lite", None),
    "boy_grey": ("cma_145241_friends_of_krishna.jpg", (0.655, 0.45, 0.77, 0.93), "birefnet-general-lite", None),
    "cows_145": ("cma_145241_friends_of_krishna.jpg", (0.04, 0.55, 0.36, 0.93), "birefnet-general-lite", None),
    "krishna_145": ("cma_145241_friends_of_krishna.jpg", (0.34, 0.55, 0.47, 0.93), "birefnet-general-lite", None),
    "yasoda_hug": ("cma_162465_yasoda_holding.jpg", (0.12, 0.04, 0.88, 0.97), "birefnet-general-lite", None),
    "vishnu_garuda": ("cma_155590_vishnu_garuda.jpg", (0.02, 0.04, 0.98, 0.97), "birefnet-general-lite", None),
    "calf_row": ("cma_153198_flute_episodes_malwa.jpg", (0.01, 0.52, 0.36, 0.74), "birefnet-general-lite", None),
    "krishna_forest": ("cma_154759_krishna_summons_cows.jpg", (0.42, 0.18, 0.60, 0.80), "birefnet-general-lite", None),
    "mothers": ("cma_154758_cattle_to_graze.jpg", (0.82, 0.17, 0.995, 0.93), "birefnet-general-lite", None),
}

# plate name: (painting file, cut-outs to remove, extra dilation in source px)
PLATES = {
    "plate_146117": ("cma_146117_krishna_returns_braj.jpg", ["boys_lunch", "swan_146"], 20),
    "plate_141755": ("cma_141755_brahma_hides.jpg", ["swan_141"], 14),
    "plate_154759": ("cma_154759_krishna_summons_cows.jpg", ["krishna_forest"], 14),
    "plate_154758": ("cma_154758_cattle_to_graze.jpg", ["mothers"], 16),
}
# extra boxes (source px) filled on a plate: the swan's feet, left below the cut that drops the bush they stand on
PLATE_EXTRA = {"plate_146117": [(745, 418, 890, 490)]}

_sessions = {}


def session(model):
    from rembg import new_session
    if model not in _sessions:
        _sessions[model] = new_session(model)
    return _sessions[model]


def load_index():
    p = os.path.join(OUT, "index.json")
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else {}


def save_index(idx):
    json.dump(idx, open(os.path.join(OUT, "index.json"), "w", encoding="utf-8"), indent=1)


def cut(name, idx):
    from rembg import remove
    fn, (x0, y0, x1, y1), model, keep = CUTS[name]
    img = Image.open(os.path.join(SRC, fn)).convert("RGB")
    W0, H0 = img.size
    box = (int(x0 * W0), int(y0 * H0), int(x1 * W0), int(y1 * H0))
    crop = img.crop(box)
    rgba = remove(crop, session=session(model), post_process_mask=True)
    a = np.asarray(rgba.getchannel("A"), np.float32)
    if keep:
        m = np.zeros_like(a)
        for kx0, ky0, kx1, ky1 in keep:
            m[int(ky0 * a.shape[0]):int(ky1 * a.shape[0]), int(kx0 * a.shape[1]):int(kx1 * a.shape[1])] = 1
        a *= m
    for cx, cy, rx, ry in ADD.get(name, []):
        yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]].astype(np.float32)
        d = ((xx + box[0] - cx) / rx) ** 2 + ((yy + box[1] - cy) / ry) ** 2
        a = np.maximum(a, np.clip((1.25 - d) / 0.5, 0, 1) * 255)
    a[a < 12] = 0
    out = crop.convert("RGBA")
    out.putalpha(Image.fromarray(a.astype(np.uint8)))
    bb = out.getchannel("A").getbbox()
    out = out.crop(bb)
    out.save(os.path.join(OUT, f"{name}.png"))
    idx[name] = dict(src=fn, x=box[0] + bb[0], y=box[1] + bb[1], w=out.width, h=out.height, src_w=W0, src_h=H0)
    print(f"cut {name}: {out.size} at {idx[name]['x']},{idx[name]['y']}")


_lama = None


def lama(img512, mask512):
    """img512: HxWx3 float 0..1, mask512: HxW 0/1 -> filled HxWx3 float 0..1."""
    global _lama
    import onnxruntime as ort
    if _lama is None:
        _lama = ort.InferenceSession(LAMA, providers=["CPUExecutionProvider"])
    im = img512.transpose(2, 0, 1)[None].astype(np.float32)
    mk = (mask512 > 0.5).astype(np.float32)[None, None]
    out = _lama.run(None, {"image": im, "mask": mk})[0][0].transpose(1, 2, 0)
    if out.max() > 2:
        out = out / 255.0
    return np.clip(out, 0, 1)


def plate(name, idx):
    from scipy import ndimage
    fn, cuts, dil = PLATES[name]
    img = Image.open(os.path.join(SRC, fn)).convert("RGB")
    W0, H0 = img.size
    arr = np.asarray(img, np.float32) / 255.0
    mask = np.zeros((H0, W0), bool)
    for c in cuts:
        e = idx[c]
        a = np.asarray(Image.open(os.path.join(OUT, f"{c}.png")).getchannel("A")) > 4
        mask[e["y"]:e["y"] + e["h"], e["x"]:e["x"] + e["w"]] |= a
    for bx0, by0, bx1, by1 in PLATE_EXTRA.get(name, []):
        mask[by0:by1, bx0:bx1] = True
    mask = ndimage.binary_dilation(mask, iterations=dil)
    lab, n = ndimage.label(ndimage.binary_dilation(mask, iterations=40))
    res = arr.copy()
    rng = np.random.default_rng(7)
    for k, sl in enumerate(ndimage.find_objects(lab)):
        ys, xs = sl
        h, w = ys.stop - ys.start, xs.stop - xs.start
        side = int(max(h, w) * 1.5) + 64
        cy, cx = (ys.start + ys.stop) // 2, (xs.start + xs.stop) // 2
        sy0 = int(np.clip(cy - side // 2, 0, max(0, H0 - side)))
        sx0 = int(np.clip(cx - side // 2, 0, max(0, W0 - side)))
        sh, sw = min(side, H0), min(side, W0)
        sub = res[sy0:sy0 + sh, sx0:sx0 + sw]
        sm = mask[sy0:sy0 + sh, sx0:sx0 + sw] & (lab[sy0:sy0 + sh, sx0:sx0 + sw] == k + 1)
        im512 = np.asarray(Image.fromarray((sub * 255).astype(np.uint8)).resize((512, 512), Image.LANCZOS),
                           np.float32) / 255.0
        m512 = np.asarray(Image.fromarray(sm.astype(np.uint8) * 255).resize((512, 512), Image.BILINEAR)) > 40
        m512 = ndimage.binary_dilation(m512, iterations=2)
        f512 = lama(im512, m512)
        fill = np.asarray(Image.fromarray((f512 * 255).astype(np.uint8)).resize((sw, sh), Image.LANCZOS),
                          np.float32) / 255.0
        fill += rng.normal(0, 0.012, fill.shape).astype(np.float32)       # the painting's grain over the soft fill
        feather = np.asarray(Image.fromarray(sm.astype(np.uint8) * 255).filter(ImageFilter.GaussianBlur(4)),
                             np.float32)[..., None] / 255.0
        feather = np.maximum(feather, sm[..., None].astype(np.float32))
        res[sy0:sy0 + sh, sx0:sx0 + sw] = sub * (1 - feather) + fill * feather
        print(f"  {name}: hole {k + 1}/{n} {w}x{h} filled from a {sw}x{sh} crop")
    Image.fromarray((np.clip(res, 0, 1) * 255).astype(np.uint8)).save(os.path.join(OUT, f"{name}.png"))
    idx[name] = dict(src=fn, x=0, y=0, w=W0, h=H0, src_w=W0, src_h=H0)
    print(f"plate {name}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", nargs="*", default=[])
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    idx = load_index()
    for n in CUTS:
        if n in a.force or not os.path.exists(os.path.join(OUT, f"{n}.png")) or n not in idx:
            cut(n, idx)
            save_index(idx)
    for n, (_, cuts, _) in PLATES.items():
        if n in a.force or any(c in a.force for c in cuts) or not os.path.exists(os.path.join(OUT, f"{n}.png")):
            plate(n, idx)
            save_index(idx)
