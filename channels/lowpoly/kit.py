"""Shared overlay pieces for low-poly episodes: tool-log cards, captions, banners, stat cards, the frame loader.

Episodes 1-2 define these in their own modules; later episodes import them from here.
"""
import math
import os
from importlib import util as _u

from motion.engine import FPS, cairo, seg
from motion.polish import appear, bold_text, rrect

HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, file):
    spec = _u.spec_from_file_location(name, os.path.join(HERE, file))
    m = _u.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_e2 = _load("lp_kit_ep02", "ep02_context_left.py")
toolcard, caption, mono, banner = _e2.toolcard, _e2.caption, _e2.mono, _e2.banner


def frames(path):
    """A loader for one episode's rendered 3D frames: frame(t) -> cairo surface."""
    n = []

    def frame(t):
        if not n:
            n.append(len(os.listdir(path)))
        return cairo.ImageSurface.create_from_png(os.path.join(path, f"f{min(int(round(t * FPS)), n[0] - 1):05d}.png"))
    return frame


def steps_at(t, steps):
    """steps = [(time, value), ...] in time order -> (current value, time it changed)."""
    val, last = steps[0][1], steps[0][0]
    for at, v in steps:
        if t >= at:
            val, last = v, at
    return val, last


def stat_card(cr, t, x, y, label, value, col, changed, k=1.0, w=276, bar=None):
    """A small dark card (label + big number) that bumps when the value changes; optional meter bar 0..1."""
    if k <= 0:
        return
    cr.save()
    cr.translate(x, y)
    rrect(cr, -w / 2, -52, w, 104 + (18 if bar is not None else 0), 18)
    cr.set_source_rgba(0.06, 0.06, 0.09, 0.9 * k)
    cr.fill_preserve()
    cr.set_source_rgba(*col[:3], 0.9 * k)
    cr.set_line_width(3)
    cr.stroke()
    cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(19)
    cr.move_to(-w / 2 + 20, -20)
    cr.set_source_rgba(0.75, 0.77, 0.82, k)
    cr.show_text(label)
    cr.restore()
    cr.save()
    cr.translate(x, y + 30)
    b = 1 + 0.25 * math.exp(-max(0, t - changed) * 9)
    cr.scale(b, b)
    bold_text(cr, value, 0, 0, 50, col, outline=None, shadow=0)
    cr.restore()
    if bar is not None:
        cr.save()
        cr.set_source_rgba(1, 1, 1, 0.12 * k)
        rrect(cr, x - w / 2 + 20, y + 58, w - 40, 8, 4)
        cr.fill()
        cr.set_source_rgba(*col[:3], 0.9 * k)
        rrect(cr, x - w / 2 + 20, y + 58, max(6, (w - 40) * min(1, bar)), 8, 4)
        cr.fill()
        cr.restore()


def pill_caption(cr, t, tl, y=318, size=27):
    """Reference 10's captions: the whole line in small white type on a dark rounded pill near the top."""
    from motion.engine import W
    for i, b in enumerate(tl.beats):
        nxt = tl.beats[i + 1].start if i + 1 < len(tl.beats) else tl.total
        end = min(b.end + 0.45, nxt - 0.05)
        if not (b.start - 0.05 <= t < end) or not b.units:
            continue
        k = min(appear(t, b.start - 0.05, 0.1), 1 - seg(t, end - 0.1, end))
        words, lines, cur = " ".join(u.shown for u in b.units).split(), [], ""
        for w in words:
            if cur and len(cur) + 1 + len(w) > 26:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        vo = getattr(b, "speaker", None) == "vo"      # Dev's inner voice: italic, no pill, like a thought
        cr.save()
        cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_ITALIC if vo else cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(size)
        wmax = max(cr.text_extents(l).x_advance for l in lines)
        h = size * 1.35 * len(lines) + size * 0.7
        rrect(cr, W / 2 - wmax / 2 - 22, y - size * 1.1, wmax + 44, h, 16)
        cr.set_source_rgba(0.05, 0.05, 0.07, (0.35 if vo else 0.72) * k)
        cr.fill()
        for j, line in enumerate(lines):
            ext = cr.text_extents(line)
            cr.move_to(W / 2 - ext.x_advance / 2, y + j * size * 1.35)
            cr.set_source_rgba(1, 1, 1, k)
            cr.show_text(line)
        cr.restore()
        return
