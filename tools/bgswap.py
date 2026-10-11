"""Put a figurine clip on a new background (after tools/bgswap_masks.py).

  python tools/bgswap.py MASK_DIR OUT.mp4 [--bg studio|brand|blur] [--compare COMPARE.mp4]

In-between masks are filled by optical flow from the neighbouring cut-outs, edges are feathered, the background
follows the camera's sway a little (so the figurine doesn't float), and a soft contact shadow is drawn under the
base. The figurine gets a light lift (exposure, warmth, colour). Output: 1080x1920 H.264, no audio, no metadata.
"""
import argparse
import glob
import os
import subprocess

import cv2
import numpy as np

W, H, FPS = 1080, 1920, 30
CLEAN = ["-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact", "-flags:v", "+bitexact",
         "-bsf:v", "filter_units=remove_types=6", "-metadata:s:v", "handler_name="]


def load(d):
    frames = sorted(glob.glob(os.path.join(d, "frame_*.png")))
    imgs = [cv2.cvtColor(cv2.imread(f), cv2.COLOR_BGR2RGB) for f in frames]
    keys = {int(os.path.basename(m)[5:10]): cv2.imread(m, cv2.IMREAD_GRAYSCALE).astype(np.float32) / 255
            for m in glob.glob(os.path.join(d, "mask_*.png"))}
    return imgs, keys


def flow_warp(src_img, dst_img, mask):
    """Move `mask` (aligned to src_img) onto dst_img using dense optical flow at half resolution."""
    a = cv2.cvtColor(cv2.resize(dst_img, (W // 2, H // 2)), cv2.COLOR_RGB2GRAY)
    b = cv2.cvtColor(cv2.resize(src_img, (W // 2, H // 2)), cv2.COLOR_RGB2GRAY)
    flow = cv2.calcOpticalFlowFarneback(a, b, None, 0.5, 4, 25, 3, 7, 1.5, 0) * 2
    flow = cv2.resize(flow, (W, H))
    gx, gy = np.meshgrid(np.arange(W, dtype=np.float32), np.arange(H, dtype=np.float32))
    return cv2.remap(mask, gx + flow[..., 0], gy + flow[..., 1], cv2.INTER_LINEAR)


def all_masks(imgs, keys):
    ks = sorted(keys)
    out = []
    for i in range(len(imgs)):
        if i in keys:
            out.append(keys[i])
            continue
        k0 = max(k for k in ks if k < i)
        k1 = min(k for k in ks if k > i)
        w = (i - k0) / (k1 - k0)
        out.append((1 - w) * flow_warp(imgs[k0], imgs[i], keys[k0]) + w * flow_warp(imgs[k1], imgs[i], keys[k1]))
    # light temporal smoothing against edge flicker
    sm = [out[0]]
    for m in out[1:]:
        sm.append(0.7 * m + 0.3 * sm[-1])
    return sm


def refine(m):
    m = np.clip((m - 0.15) / 0.7, 0, 1)                        # firm up the semi-transparent fringe
    m = cv2.erode(m, np.ones((3, 3), np.uint8), iterations=1)   # drop the 1-px halo of old background
    return cv2.GaussianBlur(m, (0, 0), 1.2)


def background(kind, first, mask=None, size=(int(W * 1.12), int(H * 1.12))):
    w, h = size
    y = np.linspace(0, 1, h)[:, None, None]
    x = np.linspace(-1, 1, w)[None, :, None]
    if kind == "blur":
        # fill the figurine's spot from its surroundings first, so it doesn't bleed into the blur as a halo
        hole = cv2.dilate((mask > 0.2).astype(np.uint8), np.ones((41, 41), np.uint8))
        small = cv2.inpaint(cv2.resize(first, (W // 4, H // 4)), cv2.resize(hole, (W // 4, H // 4)), 15,
                            cv2.INPAINT_TELEA)
        bg = cv2.GaussianBlur(cv2.resize(small, (w, h), interpolation=cv2.INTER_CUBIC), (0, 0), 28).astype(np.float32)
        return np.clip(bg * 0.8 + 20, 0, 255)
    if kind == "brand":
        top, bottom, glow = np.array([255, 196, 110]), np.array([214, 112, 30]), np.array([255, 236, 200])
    else:  # studio: warm cream sweep
        top, bottom, glow = np.array([244, 236, 226]), np.array([205, 188, 170]), np.array([255, 250, 242])
    bg = top * (1 - y) + bottom * y
    r = np.sqrt((x * 0.9) ** 2 + ((y - 0.42) * 1.6) ** 2)
    bg = bg + (glow - bg) * np.clip(1 - r, 0, 1) ** 1.6 * 0.85   # soft key light behind the figurine
    floor = np.clip((y - 0.66) / 0.04, 0, 1)                       # gentle tabletop horizon
    bg = bg * (1 - 0.10 * floor)
    return np.clip(bg, 0, 255).astype(np.float32)


def lift(img):
    """Gentle lighting fix on the figurine: a bit brighter, warmer and richer."""
    a = img.astype(np.float32)
    a = 255 * (a / 255) ** 0.88                     # lift mid-tones / shadows
    a *= np.array([1.03, 1.0, 0.96])                # warm
    g = a.mean(axis=2, keepdims=True)
    a = g + (a - g) * 1.12
    return np.clip(a, 0, 255)


def shadow(m):
    """Soft contact shadow under the base plus a faint ambient shadow from the silhouette."""
    ys, xs = np.nonzero(m > 0.5)
    sh = np.zeros_like(m)
    if len(ys):
        bottom = np.percentile(ys, 99.5)
        row = xs[ys > bottom - 40]
        x0, x1 = (np.percentile(row, 2), np.percentile(row, 98)) if len(row) else (xs.min(), xs.max())
        cv2.ellipse(sh, (int((x0 + x1) / 2), int(bottom) + 6), (int((x1 - x0) * 0.56), 26), 0, 0, 360, 1.0, -1)
        sh = cv2.GaussianBlur(sh, (0, 0), 18) * 0.55
        amb = cv2.GaussianBlur(np.roll(m, 18, axis=0), (0, 0), 30) * 0.18
        sh = np.maximum(sh, amb)
    return sh, (xs.mean() if len(xs) else W / 2, ys.mean() if len(ys) else H / 2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("masks")
    ap.add_argument("out")
    ap.add_argument("--bg", default="studio")
    ap.add_argument("--compare")
    a = ap.parse_args()
    imgs, keys = load(a.masks)
    masks = [refine(m) for m in all_masks(imgs, keys)]
    bg = background(a.bg, imgs[0], masks[0])
    enc = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                            "-pix_fmt", "yuv420p", *CLEAN, a.out], stdin=subprocess.PIPE)
    cmp = None
    if a.compare:
        cmp = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s",
                                f"{W}x{H // 2}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-crf", "20",
                                "-pix_fmt", "yuv420p", *CLEAN, a.compare], stdin=subprocess.PIPE)
    c0 = None
    for img, m in zip(imgs, masks):
        sh, c = shadow(m)
        c0 = c0 or c
        # background follows 35% of the figurine's sway, as if both were filmed together
        dx, dy = (c[0] - c0[0]) * 0.35, (c[1] - c0[1]) * 0.35
        ox = int(np.clip((bg.shape[1] - W) / 2 - dx, 0, bg.shape[1] - W))
        oy = int(np.clip((bg.shape[0] - H) / 2 - dy, 0, bg.shape[0] - H))
        b = bg[oy:oy + H, ox:ox + W] * (1 - sh[..., None] * 0.9)
        fg = lift(img)
        # light wrap: let a little background colour into the very edge
        edge = np.clip(m - cv2.erode(m, np.ones((7, 7), np.uint8)), 0, 1)[..., None]
        fg = fg * (1 - 0.25 * edge) + b * 0.25 * edge
        out = np.clip(fg * m[..., None] + b * (1 - m[..., None]), 0, 255).astype(np.uint8)
        enc.stdin.write(out.tobytes())
        if cmp:
            pair = np.concatenate([cv2.resize(img, (W // 2, H // 2)), cv2.resize(out, (W // 2, H // 2))], axis=1)
            cmp.stdin.write(pair.tobytes())
    enc.stdin.close()
    enc.wait()
    if cmp:
        cmp.stdin.close()
        cmp.wait()
    print(a.out)


if __name__ == "__main__":
    main()
