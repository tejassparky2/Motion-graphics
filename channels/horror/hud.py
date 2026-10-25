"""The game-style HUD drawn over the 3D frames: episode tag, a draining resource meter, a counter, the clock, the
rule strip, phone messages, the hook, captions and the two-way choice. Crisp vector text (pycairo), red accent.
"""
import math
import os

from motion import thriller as th
from motion.engine import FPS, W, H, cairo, clamp01, cue, hexc, seg
from motion.polish import rrect, text_path, text_width

RED = hexc("#ff2b2b")
AMBER = hexc("#ffb02e")
GREEN = hexc("#5ef08a")
HOOK, UI = th.HOOK, th.UI
MONO = "Liberation Mono"
YELLOW = hexc("#ffd23f")
_n_frames = {}


def frame(cr, t, frames):
    """Paint the 3D frame for time t."""
    if frames not in _n_frames:
        _n_frames[frames] = len(os.listdir(frames))
    i = min(int(round(t * FPS)), _n_frames[frames] - 1)
    cr.set_source_surface(cairo.ImageSurface.create_from_png(os.path.join(frames, f"f{i:05d}.png")), 0, 0)
    cr.paint()


def _plain(cr, s, x, y, size, font=UI, align="left", col=(1, 1, 1, 1)):
    text_path(cr, s, x, y, size, font, align)
    cr.set_source_rgba(*col)
    cr.fill()


def _panel(cr, x, y, w, h, a=0.62, border=None):
    rrect(cr, x, y, w, h, 14)
    cr.set_source_rgba(0.02, 0.02, 0.03, a)
    cr.fill_preserve()
    cr.set_source_rgba(*(border or (1, 1, 1, 0.18)))
    cr.set_line_width(2.5)
    cr.stroke()


def tag(cr, t, series, part):
    """Top-left: SERIES / PART n, with a blinking red REC-style dot (fixed size, the same in every episode)."""
    _panel(cr, 26, 30, 250, 74)
    on = (t % 1.2) < 0.8
    cr.arc(52, 67, 9, 0, 2 * math.pi)
    cr.set_source_rgba(*RED[:3], 1 if on else 0.25)
    cr.fill()
    _plain(cr, series, 72, 62, 26, HOOK)
    _plain(cr, part, 72, 92, 20, UI, col=(1, 1, 1, 0.7))


def meter(cr, t, label, value, x=W - 26 - 250, y=30, warn=0.25, icon="battery", shake_below=0.1):
    """Top-right: a draining meter (value 0..1) with its label and percentage; red and shaking when low."""
    low = value <= warn
    jx = 2.0 * math.sin(t * 50) if value <= shake_below else 0
    _panel(cr, x + jx, y, 250, 74, border=(*RED[:3], 0.8) if low else None)
    col = RED if low else (GREEN if value > 0.5 else AMBER)
    if low and (t % 0.6) > 0.42:
        col = (*col[:3], 0.35)
    _plain(cr, label, x + 18 + jx, y + 30, 19, UI, col=(1, 1, 1, 0.75))
    bx, by, bw, bh = x + 18 + jx, y + 40, 128, 22
    if icon == "battery":
        rrect(cr, bx, by, bw, bh, 5)
        cr.set_source_rgba(1, 1, 1, 0.8)
        cr.set_line_width(2.5)
        cr.stroke()
        cr.rectangle(bx + bw + 2, by + 6, 6, bh - 12)
        cr.fill()
    else:
        rrect(cr, bx, by, bw, bh, 5)
        cr.set_source_rgba(1, 1, 1, 0.15)
        cr.fill()
    rrect(cr, bx + 4, by + 4, max(2, (bw - 8) * clamp01(value)), bh - 8, 3)
    cr.set_source_rgba(*col)
    cr.fill()
    _plain(cr, f"{round(value * 100)}%", x + 232 + jx, y + 60, 30, HOOK, "right", col)


def chips(cr, t, items, x=26, y=114):
    """A row of small status chips under the series tag (after the third reference: WATER 3 / PHONE 41% / SIGNAL x).
    items = [(text, changed_at or None, red)]: a chip flashes and pops when its value changes."""
    for text, at, red in items:
        sz = 21
        w = text_width(cr, text, sz, MONO) + 26
        k = clamp01((t - at) / 0.6) if at is not None else 1
        s = 1 + 0.25 * (1 - k)
        cr.save()
        cr.translate(x + w / 2, y + 19)
        cr.scale(s, s)
        flash = (1 - k) * (0.5 + 0.5 * math.sin(t * 30))
        _panel(cr, -w / 2, -19, w, 38, a=0.66, border=(*RED[:3], 0.95) if red or k < 1 else (1, 1, 1, 0.22))
        if flash > 0:
            rrect(cr, -w / 2, -19, w, 38, 14)
            cr.set_source_rgba(*RED[:3], 0.35 * flash)
            cr.fill()
        _plain(cr, text, 0, 8, sz, MONO, "center", RED if red else (1, 1, 1, 0.9))
        cr.restore()
        x += w + 10


def tag_line(cr, t, text, x=26, y=124):
    """The small line under the series tag: DAY/NIGHT and the live clock."""
    _plain(cr, text, x + 4, y, 22, MONO, "left", (1, 1, 1, 0.85))


def rule(cr, t, start, text, y=192):
    """The rule: stamped big when it's read, then kept as a thin strip under the HUD."""
    if t < start:
        return
    k = clamp01((t - start) / 0.25)
    sz = 26
    w = text_width(cr, text, sz, HOOK) + 60
    x = (W - w) / 2
    _panel(cr, x, y, w, 46, a=0.7 * k, border=(*RED[:3], 0.9 * k))
    _plain(cr, text, W / 2, y + 34, sz, HOOK, "center", (*RED[:3], k))


def big(cr, t, start, end, lines, y=330, size=92):
    """Big shaking words mid-screen (a reveal: '13?', 'OUT OF SERVICE')."""
    if t < start or t > end + 0.2:
        return
    a = clamp01((t - start) / 0.12) * (1 - clamp01((t - end) / 0.2))
    s = 1.25 - 0.25 * clamp01((t - start) / 0.18)
    cr.save()
    cr.translate(W / 2, y)
    cr.scale(s, s)
    cr.push_group()
    for k, (txt, red) in enumerate(lines):
        sz = min(size, size * (W - 80) / max(1, text_width(cr, txt, size, HOOK)))
        th._text(cr, txt, 1.5 * math.sin(t * 43 + k), k * size * 1.05, sz, RED if red else (1, 1, 1, 1), HOOK)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def sign(cr, t, start, end, lines, y=300, w=560, paper=(0.86, 0.84, 0.76), ink=(0.12, 0.06, 0.05), size=40,
         font="Permanent Marker", rot=-0.02):
    """A printed/handwritten notice shown up close (the elevator sign, the logbook page)."""
    if t < start or t > end + 0.25:
        return
    a = clamp01((t - start) / 0.25) * (1 - clamp01((t - end) / 0.25))
    h = 70 + len(lines) * size * 1.25
    cr.save()
    cr.translate(W / 2, y + 30 * (1 - a))
    cr.rotate(rot)
    cr.push_group()
    rrect(cr, -w / 2, 0, w, h, 6)
    cr.set_source_rgba(*paper, 0.96)
    cr.fill()
    for k, (txt, red) in enumerate(lines):
        _plain(cr, txt, 0, 50 + k * size * 1.25 + size * 0.4, size, font, "center",
               (*RED[:3], 1) if red else (*ink, 1))
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def phone(cr, t, start, sender, msg, end, y=300, typing=0.6, app="MESSAGES"):
    """A phone message card (sender + bubble); buzz on arrival."""
    th.phone(cr, t, start, sender, msg, y=y, typing=typing, end=end)


def your_call(cr, t, start, a_text, b_text, vote, y=360):
    """The ending card: YOUR CALL. and the two options as pills (A red, B white), then the vote line."""
    if t < start:
        return
    k = clamp01((t - start) / 0.25)
    cr.set_source_rgba(0, 0, 0, 0.45 * k)
    cr.paint()
    s = 1.3 - 0.3 * k
    cr.save()
    cr.translate(W / 2, y)
    cr.scale(s, s)
    th._text(cr, "YOUR CALL.", 0, 0, 104, (1, 1, 1, k), HOOK)
    cr.restore()
    for n, (txt, col) in enumerate(((a_text, RED), (b_text, (1, 1, 1, 1)))):
        p = clamp01((t - start - 0.25 - 0.18 * n) / 0.25)
        if p <= 0:
            continue
        w = text_width(cr, txt, 66, HOOK) + 90
        cy = y + 120 + n * 150
        cr.save()
        cr.translate(W / 2, cy)
        cr.scale(0.8 + 0.2 * p, 0.8 + 0.2 * p)
        rrect(cr, -w / 2, -60, w, 120, 60)
        cr.set_source_rgba(*(col[:3] if n == 0 else (1, 1, 1)), p)
        cr.fill()
        _plain(cr, txt, 0, 24, 66, HOOK, "center", (1, 1, 1, p) if n == 0 else (0.05, 0.05, 0.06, p))
        cr.restore()
    if t >= start + 0.7:
        _plain(cr, vote, W / 2, y + 430, 30, HOOK, "center", (1, 1, 1, clamp01((t - start - 0.7) / 0.3)))


def time_card(cr, t, start, end, big_text, small_text, y=360):
    """A time jump: big clock time and a line under it (3:14 AM / THE GENERATOR HAS 1 HOUR)."""
    if t < start or t > end + 0.2:
        return
    a = clamp01((t - start) / 0.15) * (1 - clamp01((t - end) / 0.2))
    w = 560
    _panel(cr, (W - w) / 2, y - 100, w, 170, a=0.8 * a, border=(1, 1, 1, 0.25 * a))
    th._text(cr, big_text, W / 2, y + 5, 96, (1, 1, 1, a), HOOK)
    _plain(cr, small_text, W / 2, y + 50, 24, MONO, "center", (1, 1, 1, 0.75 * a))


def phone_thread(cr, t, start, end, contact, sub, msgs, y=190, h=680):
    """A full-screen phone chat. msgs = [(time, "in"/"out", text, note)]; an incoming message shows typing dots for
    0.6 s first; `note` under an outgoing one is red (Not Delivered). Buzz on every incoming message."""
    if t < start or t > end + 0.25:
        return
    a = clamp01((t - start) / 0.2) * (1 - clamp01((t - end) / 0.25))
    up = (1 - clamp01((t - start) / 0.3)) ** 2 * 200
    x0, w = 105, W - 210
    cr.save()
    cr.translate(0, up)
    cr.push_group()
    th.glow(cr, W / 2, y + h / 2, 470, (0.45, 0.6, 1.0), 0.16)
    rrect(cr, x0, y, w, h, 60)
    cr.set_source_rgba(0.06, 0.06, 0.08, 0.97)
    cr.fill_preserve()
    cr.set_source_rgba(0.3, 0.31, 0.36, 1)
    cr.set_line_width(7)
    cr.stroke()
    rrect(cr, W / 2 - 60, y + 18, 120, 30, 15)
    cr.set_source_rgba(0, 0, 0, 1)
    cr.fill()
    _plain(cr, contact, W / 2, y + 92, 30, UI, "center", (1, 1, 1, 0.95))
    _plain(cr, sub, W / 2, y + 120, 18, UI, "center", (*RED[:3], 0.9) if "No" in sub else (1, 1, 1, 0.5))
    cr.set_source_rgba(1, 1, 1, 0.12)
    cr.rectangle(x0 + 24, y + 140, w - 48, 2)
    cr.fill()
    by = y + 170
    for at, side, text, note in msgs:
        if t < at:
            break
        lines = _wrap_ui(cr, text, 28, w - 170)
        bh = 22 + 36 * len(lines)
        bw = max(text_width(cr, ln, 28, UI) for ln in lines) + 44
        typing = side == "in" and t < at + 0.6
        if typing:
            bw, bh = 110, 58
        bx = x0 + 30 if side == "in" else x0 + w - 30 - bw
        pop = 0.85 + 0.15 * clamp01((t - at) / 0.12)
        cr.save()
        cr.translate(bx + (0 if side == "in" else bw), by)
        cr.scale(pop, pop)
        cr.translate(-(0 if side == "in" else bw), 0)
        rrect(cr, 0, 0, bw, bh, 26)
        cr.set_source_rgba(*((0.2, 0.21, 0.24) if side == "in" else (0.13, 0.45, 0.98)), 1)
        cr.fill()
        if typing:
            for k in range(3):
                on = 0.35 + 0.65 * clamp01(math.sin((t - at) * 9 - k * 0.9))
                cr.arc(28 + k * 27, 29, 8, 0, 2 * math.pi)
                cr.set_source_rgba(1, 1, 1, on)
                cr.fill()
        else:
            for k, ln in enumerate(lines):
                _plain(cr, ln, 22, 40 + 36 * k, 28, UI, "left", (1, 1, 1, 1))
        cr.restore()
        if side == "in":
            cue("buzz", t, at + 0.6)
        by += bh + 14
        if note and not typing:
            _plain(cr, note, x0 + w - 34, by + 6, 18, UI, "right", (*RED[:3], 1))
            by += 26
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def _wrap_ui(cr, s, size, max_w):
    lines, cur = [], ""
    for w in s.split():
        nxt = (cur + " " + w).strip()
        if cur and text_width(cr, nxt, size, UI) > max_w:
            lines.append(cur)
            cur = w
        else:
            cur = nxt
    return lines + [cur] if cur else lines


def captions(cr, t, tl, key=(), y=915, size=66, max_w=620):
    """Big 1-3 word captions (Anton, white); danger words in red and numbers/times in yellow, like the references;
    the word being spoken pops a little."""
    from motion.captions import _chunks
    chunks = _caps.get(id(tl))
    if chunks is None:
        chunks = _caps[id(tl)] = _chunks(tl)
    keys = {k.lower() for k in key}
    for i, ch in enumerate(chunks):
        start = ch[0].start
        nxt = chunks[i + 1][0].start if i + 1 < len(chunks) else tl.total
        stop = nxt if nxt - ch[-1].end < 0.5 else ch[-1].end + 0.25
        if not (start - 0.02 <= t < stop):
            continue
        words = [u.shown.rstrip(",;:").upper() for u in ch]
        space = text_width(cr, " ", size, HOOK)
        widths = [text_width(cr, w, size, HOOK) for w in words]
        total = sum(widths) + space * (len(words) - 1)
        sz = size * min(1, max_w / total)
        k = 0.9 + 0.1 * clamp01((t - start) / 0.1)
        cr.save()
        cr.translate(W / 2, y)
        cr.scale(k, k)
        x = -total * sz / size / 2
        for wd, w, u in zip(widths, words, ch):
            bare = w.strip(".,!?\"'").lower()
            col = RED if bare in keys else YELLOW if any(c.isdigit() for c in bare) else (1, 1, 1, 1)
            on = u.start - 0.03 <= t < u.end + 0.05
            cr.save()
            cr.translate(x + wd * sz / size / 2, 0)
            if on:
                cr.scale(1.08, 1.08)
            th._text(cr, w, -wd * sz / size / 2, 0, sz, col, HOOK, align="left", ow=sz * 0.14)
            cr.restore()
            x += (wd + space) * sz / size
        cr.restore()
        return


_caps = {}


def finish(cr, t, flash_at=(), vig=0.5, grain=0.06):
    """Grain, vignette and white lightning/shock flashes."""
    g = cairo.RadialGradient(W / 2, H * 0.45, H * 0.2, W / 2, H * 0.48, H * 0.8)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, vig)
    cr.set_source(g)
    cr.paint()
    th.grain(cr, t, grain)
    for at in flash_at:
        th.flash(cr, t, at, dur=0.15, a=0.5)


def blackout(cr, t, start, end, fade=0.08):
    """A cut to black (with a short fade back in)."""
    if start <= t < end + fade:
        cr.set_source_rgba(0, 0, 0, 1 if t < end else 1 - (t - end) / fade)
        cr.paint()


hook = th.hook
