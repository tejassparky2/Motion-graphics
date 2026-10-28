"""Anime puppets and painted backgrounds for the story channels (reports/CPU anime animation pipeline.md).

Each character is ONE painted bust (assets/anime/SET/NAME/base.png, made by tools/anime_assets.py) plus face patches
(expressions, blink, mouth shapes) pasted over it, so the character looks the same in every shot. Motion follows anime
limited animation: the character changes on 2s (12 drawings a second at 24 fps) while the camera moves every frame;
blinks are sparse and irregular; talking cycles three mouths (closed, half, open) with uneven holds.
"""
import functools
import json
import math
import os

import cairo
import cv2
import numpy as np

from motion.engine import W, H

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STEP = 1 / 12                                                    # drawings change on 2s at 24 fps


def held(t, step=STEP):
    """Time quantized to the drawing rate (anime holds each drawing for 2 frames)."""
    return math.floor(t / step + 1e-6) * step


def _surface_from_rgba(a):
    """numpy RGBA (straight alpha) -> premultiplied cairo ARGB32 surface."""
    h, w = a.shape[:2]
    al = a[..., 3:4].astype(np.float32) / 255
    bgra = np.dstack([a[..., 2::-1].astype(np.float32) * al, al * 255]).astype(np.uint8)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    buf = np.ndarray((h, s.get_stride() // 4, 4), np.uint8, s.get_data())
    buf[:, :w] = bgra
    s.mark_dirty()
    return s


@functools.lru_cache(maxsize=None)
def image(path, blur=0, scale=1.0, pad_bottom=0):
    """A PNG as a cairo surface (optionally pre-blurred / pre-scaled; cached per process). pad_bottom repeats the last
    row downward, so a bust's cut-off chest never ends inside the frame."""
    a = cv2.imread(os.path.join(ROOT, path), cv2.IMREAD_UNCHANGED)
    if a is None:
        raise FileNotFoundError(path)
    a = cv2.cvtColor(a, cv2.COLOR_BGRA2RGBA if a.shape[2] == 4 else cv2.COLOR_BGR2RGB)
    if a.shape[2] == 3:
        a = np.dstack([a, np.full(a.shape[:2], 255, np.uint8)])
    if pad_bottom:
        a = cv2.copyMakeBorder(a, 0, pad_bottom, 0, 0, cv2.BORDER_REPLICATE)
    if scale != 1.0:
        a = cv2.resize(a, (int(a.shape[1] * scale), int(a.shape[0] * scale)), interpolation=cv2.INTER_AREA)
    if blur:
        a = cv2.GaussianBlur(a, (0, 0), blur)
    return _surface_from_rgba(a)


def paint_bg(cr, path, blur=0, ax=0.5, ay=0.5, zoom=1.0, alpha=1.0):
    """Cover the canvas with a background plate (centre of interest at (ax, ay) of the image)."""
    s = image(path, blur=blur, scale=0.5 if blur else 1.0)
    iw, ih = s.get_width(), s.get_height()
    k = max(W / iw, H / ih) * zoom
    cr.save()
    cr.translate(W / 2, H / 2)
    cr.scale(k, k)
    cr.translate(-iw * ax, -ih * ay)
    cr.set_source_surface(s, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint_with_alpha(alpha)
    cr.restore()


class Puppet:
    """A painted bust with face patches. meta: neck (x, y) and head height in base.png pixels."""

    def __init__(self, set_, name, neck, head_h, phase=0.0):
        self.dir = os.path.join("assets", "anime", set_, name)
        self.neck, self.head_h, self.phase = neck, head_h, phase
        mp = os.path.join(ROOT, self.dir, "parts.json")
        self.parts = json.load(open(mp)) if os.path.exists(mp) else {}

    def has(self, part):
        return part in self.parts

    def _paste(self, cr, part):
        p = self.parts[part]
        cr.set_source_surface(image(os.path.join(self.dir, part + ".png")), p["x"], p["y"])
        cr.get_source().set_filter(cairo.FILTER_GOOD)
        cr.paint()

    def blinking(self, t):
        """Irregular blinks: one every 2.4-5.2 s, eyes shut for one drawing (1/12 s)."""
        n = 0
        at = 0.6 + 2.0 * ((math.sin(self.phase * 12.9898) * 43758.5453) % 1)
        while at < t - STEP:
            n += 1
            at += 2.4 + 2.8 * ((math.sin((n + self.phase) * 78.233) * 43758.5453) % 1)
        return at - 1e-6 <= t < at + STEP

    @staticmethod
    def mouth(t, talk):
        """Closed / half / open with uneven holds (random switching reads as chattering)."""
        if talk <= 0:
            return None
        pattern = ("open", "open", "half", None, "open", "half", "half", None, "open", "open", None, "half")
        return pattern[int(t / STEP) % len(pattern)]

    def draw(self, cr, x, y, s, t, expr="neutral", talk=0.0, tilt=0.0, blink=True, alpha=1.0, flip=False,
             eyes_closed=False, fade=False):
        """(x, y) = the base of the neck on the canvas; s = 1 gives a 250 px tall head."""
        tq = held(t)
        k = s * 250 / self.head_h
        breathe = 1 + 0.007 * math.sin(2 * math.pi * 0.23 * tq + self.phase)
        sway = 0.006 * math.sin(2 * math.pi * 0.11 * tq + self.phase * 3) + tilt
        base = image(os.path.join(self.dir, "base.png"), pad_bottom=0 if fade else 1200)
        cr.save()
        cr.translate(x, y)
        cr.rotate(sway)
        cr.scale(k * (-1 if flip else 1), k * breathe)
        cr.translate(-self.neck[0], -self.neck[1])
        if alpha < 1 or fade:
            cr.push_group()
        cr.set_source_surface(base, 0, 0)
        cr.get_source().set_filter(cairo.FILTER_GOOD)
        cr.paint()
        face = expr if expr != "neutral" and self.has(expr) else None
        if face:
            self._paste(cr, face)
        pre = face + "+" if face else ""
        m = self.mouth(t, talk)
        if m == "open" and not self.has(pre + "open") and self.has(pre + "half"):
            m = "half"                                         # a smeared open mouth was dropped: use half-open
        if m and self.has(pre + m):
            self._paste(cr, pre + m)
        elif m and self.has(pre + "open"):                     # expression faces have closed / open only
            if m == "open":
                self._paste(cr, pre + "open")
        if (eyes_closed or blink and self.blinking(t)) and self.has(pre + "blink"):
            self._paste(cr, pre + "blink")
        if fade:                                               # the torso fades out instead of ending in an edge
            bh = base.get_height()
            g = cairo.LinearGradient(0, self.neck[1] + 0.12 * bh, 0, self.neck[1] + 0.42 * bh)
            g.add_color_stop_rgba(0, 0, 0, 0, alpha)
            g.add_color_stop_rgba(1, 0, 0, 0, 0)
            cr.pop_group_to_source()
            cr.mask(g)
        elif alpha < 1:
            cr.pop_group_to_source()
            cr.paint_with_alpha(alpha)
        cr.restore()
