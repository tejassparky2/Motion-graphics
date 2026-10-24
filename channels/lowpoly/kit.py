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


def build_script(lines, holds, gap=1.15, gap_fix=None):
    """lines = [(id, shot, speaker or None, text, gap before, pace)] -> SCRIPT. Empty text = a silent hold (holds[id]
    seconds). Gaps are scaled by `gap` (batch-5 rules: a little more air); gap_fix pins exact gaps after a retake."""
    script = []
    for i, (bid, shot, who, text, g, pace) in enumerate(lines):
        d = dict(id=bid, scene=shot, text=text)
        if who:
            d["speaker"] = who
        if i:
            d["gap"] = (gap_fix or {}).get(bid, round(g * gap, 2))
        if pace != 1:
            d["pace"] = pace
        if not text:
            d["hold"] = holds[bid]
        script.append(d)
    return script


def skit_voice(voice, rate=4.0, tempo_min=0.88):
    """Batch-5 voice settings for skits: Turbo's natural pace slowed a little, never sped up, and two clone-check tries
    with a looser pace test (one-word lines can't pass a strict one; the full-line Whisper check after the render
    still applies). Batch 8 passes rate=3.4, tempo_min=0.8: reference 10 talks at ~140 wpm, our takes ran ~190."""
    voice.CLONE_RATE = rate
    voice.TEMPO_MIN = tempo_min
    check = voice.clone_check
    voice.clone_check = lambda takes, tries=3, slack=0.15: check(takes, 2, max(slack, 0.45))


def plain_caption(cr, t, tl, y=330, size=30):
    """Reference 10's captions (owner, 23 Oct 2026): the whole line in small plain white type with a soft dark
    shadow, no box."""
    from motion.engine import W
    for i, b in enumerate(tl.beats):
        nxt = tl.beats[i + 1].start if i + 1 < len(tl.beats) else tl.total
        end = min(b.end + 0.45, nxt - 0.05)
        if not (b.start - 0.05 <= t < end) or not b.units:
            continue
        k = min(appear(t, b.start - 0.05, 0.1), 1 - seg(t, end - 0.1, end))
        words, lines, cur = " ".join(u.shown for u in b.units).split(), [], ""
        for w in words:
            if cur and len(cur) + 1 + len(w) > 28:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        cr.save()
        cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(size)
        for j, line in enumerate(lines):
            ext = cr.text_extents(line)
            x, yy = W / 2 - ext.x_advance / 2, y + j * size * 1.3
            for dx, dy, a in ((0, 3, 0.55), (2, 2, 0.35), (-2, 2, 0.35), (0, 0, 0.0)):
                if a:
                    cr.move_to(x + dx, yy + dy)
                    cr.set_source_rgba(0, 0, 0, a * k)
                    cr.show_text(line)
            cr.move_to(x, yy)
            cr.set_source_rgba(1, 1, 1, k)
            cr.show_text(line)
        cr.restore()
        return


def screen_insert(cr, t, start, end, title, clock, paint, y=800, h=640):
    """Reference 10's cut to the screen: the room goes dark behind a big app window (title bar, a clock top right that
    can jump) and `paint(cr, x, y, w, h, t, k)` draws what's inside. A hard cut in and out, like the reference.
    clock: a string, or [(time, string), ...] steps."""
    from motion.engine import W
    if not (start <= t < end):
        return
    k = 1.0
    cr.save()
    cr.set_source_rgba(0.02, 0.02, 0.05, 0.88)
    cr.paint()
    w = W - 40
    x0, y0 = 20, y - h / 2
    rrect(cr, x0, y0, w, h, 14)
    cr.set_source_rgba(0.07, 0.075, 0.1, 1)
    cr.fill_preserve()
    cr.set_source_rgba(1, 1, 1, 0.1)
    cr.set_line_width(2)
    cr.stroke()
    mono(cr, title, x0 + 22, y0 + 34, 19, (0.62, 0.66, 0.74), k)
    if isinstance(clock, (list, tuple)):
        clock = steps_at(t, clock)[0]
    if clock:
        cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(30)
        ext = cr.text_extents(clock)
        cr.move_to(x0 + w - 22 - ext.x_advance, y0 + 38)
        cr.set_source_rgba(1, 1, 1, 0.95)
        cr.show_text(clock)
    cr.move_to(x0, y0 + 54)
    cr.line_to(x0 + w, y0 + 54)
    cr.set_source_rgba(1, 1, 1, 0.08)
    cr.stroke()
    cr.rectangle(x0 + 2, y0 + 56, w - 4, h - 58)
    cr.clip()
    paint(cr, x0 + 2, y0 + 56, w - 4, h - 58, t, k)
    cr.restore()


def build_caption(cr, t, tl, y=330, size=30):
    """@agentmorphy's captions (owner, 23 Oct 2026): small plain white type that builds up word by word as the line
    is spoken. The line is laid out in full first, so words never jump when the next one appears."""
    from motion.engine import W
    for i, b in enumerate(tl.beats):
        nxt = tl.beats[i + 1].start if i + 1 < len(tl.beats) else tl.total
        end = min(b.end + 0.45, nxt - 0.05)
        if not (b.start - 0.05 <= t < end) or not b.units:
            continue
        k = 1 - seg(t, end - 0.1, end)
        cr.save()
        cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(size)
        words = []                                   # (word, time it appears)
        for u in b.units:
            for w in u.shown.split():
                words.append((w, u.start))
        lines, cur = [], []
        for w in words:
            if cur and len(" ".join(x for x, _ in cur)) + 1 + len(w[0]) > 28:
                lines.append(cur)
                cur = [w]
            else:
                cur.append(w)
        lines.append(cur)
        space = cr.text_extents(" a").x_advance - cr.text_extents("a").x_advance
        for j, line in enumerate(lines):
            full = " ".join(x for x, _ in line)
            x = W / 2 - cr.text_extents(full).x_advance / 2
            yy = y + j * size * 1.3
            for w, at in line:
                kw = k * appear(t, at - 0.04, 0.08)
                adv = cr.text_extents(w).x_advance
                if kw > 0:
                    for dx, dy, a in ((0, 3, 0.55), (2, 2, 0.35), (-2, 2, 0.35)):
                        cr.move_to(x + dx, yy + dy)
                        cr.set_source_rgba(0, 0, 0, a * kw)
                        cr.show_text(w)
                    cr.move_to(x, yy)
                    cr.set_source_rgba(1, 1, 1, kw)
                    cr.show_text(w)
                x += adv + space
        cr.restore()
        return


def headline(cr, t, start, end, source, title, rows=(), clock=""):
    """A news-explainer cutaway (owner's reference, 24 Oct 2026): the source and date on top, the headline in big
    type, then up to four short fact rows, each (text, colour), revealed one by one."""
    from motion.engine import W

    def paint(cr, x, y, w, h, t, k):
        cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        size, lines, cur = 40, [], ""
        cr.set_font_size(size)
        for word in title.split():
            trial = (cur + " " + word).strip()
            if cur and cr.text_extents(trial).x_advance > w - 60:
                lines.append(cur)
                cur = word
            else:
                cur = trial
        lines.append(cur)
        for i, line in enumerate(lines):
            cr.move_to(x + 30, y + 70 + i * size * 1.25)
            cr.set_source_rgba(1, 1, 1, k)
            cr.show_text(line)
        y0 = y + 70 + len(lines) * size * 1.25 + 30
        for i, (text, col) in enumerate(rows):
            if t < start + 0.5 + 0.45 * i:
                break
            mono(cr, text, x + 30, y0 + 52 * i, 27, col, k)
    screen_insert(cr, t, start, end, source, clock, paint)


def bignum(cr, t, start, end, source, value, label, sub="", col=(1.0, 0.36, 0.36), count=True):
    """A news-explainer number card: a big number that counts up to `value` (int, or a string shown as is), a label
    under it and an optional small source line."""
    def paint(cr, x, y, w, h, t, k):
        if isinstance(value, (int, float)) and count:
            u = min(1.0, max(0.0, (t - start) / 0.6))
            v = value * (1 - (1 - u) ** 3)
            txt = f"{int(round(v)):,}"
        else:
            txt = str(value)
        cr.save()
        cr.translate(x + w / 2, y + h * 0.42)
        bold_text(cr, txt, 0, 0, 120 if len(txt) < 8 else 90, col, outline=None, shadow=0)
        cr.restore()
        cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(34)
        ext = cr.text_extents(label)
        cr.move_to(x + w / 2 - ext.x_advance / 2, y + h * 0.62)
        cr.set_source_rgba(1, 1, 1, k)
        cr.show_text(label)
        if sub:
            cr.set_font_size(22)
            ext = cr.text_extents(sub)
            cr.move_to(x + w / 2 - ext.x_advance / 2, y + h * 0.62 + 50)
            cr.set_source_rgba(0.62, 0.66, 0.74, k)
            cr.show_text(sub)
    screen_insert(cr, t, start, end, source, "", paint)
