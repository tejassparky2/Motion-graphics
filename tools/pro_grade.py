"""Consistent 'professional' lighting for phone clips shot under different room lights.

Each clip is measured once (a few frames, so the correction doesn't flicker) and matched to one look:
neutral-warm white balance, a common brightness, lifted shadows with protected highlights, a gentle S-curve,
a soft highlight glow and a light vignette.

  g = ClipGrade(path)          # measures the clip
  frame = g(frame)             # PIL RGB -> PIL RGB
"""
import subprocess

import numpy as np
from PIL import Image, ImageFilter

TARGET_LUMA = 118.0                       # 0..255 mean, brighter than the raw clips (74-99)
WARM = np.array([1.03, 1.0, 0.95])        # neutral-warm white
_vig = {}


def _sample(path, n=5, size=(270, 480)):
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
                                         "csv=p=0", path]))
    out = []
    for k in range(n):
        raw = subprocess.check_output(["ffmpeg", "-v", "error", "-ss", f"{dur * (k + 0.5) / n:.2f}", "-i", path,
                                       "-frames:v", "1", "-vf", f"scale={size[0]}:{size[1]}", "-f", "rawvideo",
                                       "-pix_fmt", "rgb24", "-"])
        if raw:
            out.append(np.frombuffer(raw, np.uint8).reshape(size[1], size[0], 3))
    return np.stack(out).astype(np.float32)


class ClipGrade:
    def __init__(self, path, strength=0.75):
        a = _sample(path)
        px = a.reshape(-1, 3)
        mean = px.mean(0)
        # white-patch: the brightest 5% (white printer head, screen, base text) should be neutral-warm white
        lum = px @ np.array([0.299, 0.587, 0.114])
        bright = px[lum >= np.percentile(lum, 95)].mean(0)
        g_world = mean.mean() * WARM / mean
        g_white = bright.mean() * WARM / bright
        # pull the colour cast 75% of the way to neutral-warm, half grey-world and half white-patch
        self.gain = 1 + strength * ((g_world + g_white) / 2 - 1)
        luma = float(((a * self.gain).clip(0, 255) @ np.array([0.299, 0.587, 0.114])).mean())
        # exposure as a gamma so highlights stay put while mid-tones and shadows come up
        self.gamma = float(np.clip(np.log(TARGET_LUMA / 255) / np.log(max(1.0, luma) / 255), 0.55, 1.05))

    def __call__(self, frame):
        a = np.asarray(frame).astype(np.float32) * self.gain / 255
        a = np.clip(a, 0, 1) ** self.gamma
        a = a + 0.22 * (a * a * (3 - 2 * a) - a)                 # gentle S-curve
        g = a.mean(axis=2, keepdims=True)
        a = g + (a - g) * 1.08                                   # a touch more colour
        h, w = a.shape[:2]
        # soft glow: blurred highlights added back
        hi = np.clip((a.max(axis=2) - 0.72) / 0.28, 0, 1)
        small = Image.fromarray((hi * 255).astype(np.uint8)).resize((w // 4, h // 4)).filter(
            ImageFilter.GaussianBlur(10)).resize((w, h), Image.BILINEAR)
        a = a + 0.10 * (np.asarray(small, np.float32) / 255)[..., None]
        if (w, h) not in _vig:
            y, x = np.mgrid[0:h, 0:w]
            r = np.sqrt(((x - w / 2) / (w * 0.75)) ** 2 + ((y - h / 2) / (h * 0.7)) ** 2)
            _vig[(w, h)] = (1 - 0.28 * np.clip(r - 0.4, 0, 1) ** 1.5)[..., None].astype(np.float32)
        a = a * _vig[(w, h)]
        return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
