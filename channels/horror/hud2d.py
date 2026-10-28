"""Overlays for the 2D episodes, after the owner's 2D reference (25 Oct 2026): a tidy stats bar (label over value),
sentence-case rounded captions with the key word coloured, a tilted RULE tag, speech bubbles for other characters,
a big in-world phone held in two hands, a background blur helper (depth of field), and the A/B ending card.
"""
import math

import numpy as np
from scipy.ndimage import gaussian_filter

from motion.engine import W, H, cairo, clamp01, cue
from motion.polish import rrect, text_path, text_width
from channels.horror import toon2d as tk
from channels.horror.toon2d import INK, glow, hexa

ROUND = "Fredoka"
MONO = "Liberation Mono"
UI = "Liberation Sans"
RED = hexa("#ff3b30")
GREEN = hexa("#34d17a")
YELLOW = hexa("#ffd23f")


def _text(cr, s, x, y, size, col, font=ROUND, align="left", outline=None, ow=0.0, shadow=0.0):
    if shadow:
        text_path(cr, s, x + size * 0.04, y + size * 0.07, size, font, align)
        cr.set_source_rgba(0, 0, 0, shadow)
        cr.fill()
    if outline:
        text_path(cr, s, x, y, size, font, align)
        cr.set_source_rgba(*outline)
        cr.set_line_width(ow)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
    text_path(cr, s, x, y, size, font, align)
    cr.set_source_rgba(*col)
    cr.fill()


def meta_2d(meta):
    """The 3D episode's upload sheet, reworded for the 2D cut (it must not say "3D animation")."""
    out = dict(meta)
    out["description"] = meta["description"].replace("3D animation", "2D animation")
    out["tags"] = [("2d animation" if tg == "3d animation" else tg) for tg in meta["tags"]]
    return out


# ------------------------------------------------------------------ depth of field
def blurred(cr, draw_bg, sigma=7.0, scale=0.5):
    """Draw a background layer (with the current transform) blurred, at reduced resolution for speed."""
    w, h = int(W * scale), int(H * scale)
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    c = cairo.Context(surf)
    c.scale(scale, scale)
    c.transform(cr.get_matrix())
    draw_bg(c)
    surf.flush()
    a = np.ndarray((h, surf.get_stride() // 4, 4), np.uint8, surf.get_data())[:, :w].astype(np.float32)
    for ch in range(4):
        a[..., ch] = gaussian_filter(a[..., ch], sigma * scale)
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, w, h)
    o = np.ndarray((h, out.get_stride() // 4, 4), np.uint8, out.get_data())
    o[:, :w] = np.clip(a + 0.5, 0, 255).astype(np.uint8)
    out.mark_dirty()
    cr.save()
    cr.identity_matrix()
    cr.scale(1 / scale, 1 / scale)
    cr.set_source_surface(out, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint()
    cr.restore()


# ------------------------------------------------------------------ the stats bar
def stats(cr, t, items, y=28):
    """Three (or so) boxes across the top: [(label, value, state)], state in None / "warn" / "bad", optionally with
    a changed-at time (label, value, state, at) that pops the box."""
    n = len(items)
    gap, x0 = 10, 22
    w = (W - 2 * x0 - gap * (n - 1)) / n
    for k, it in enumerate(items):
        label, value, state = it[:3]
        at = it[3] if len(it) > 3 else None
        pop = clamp01((t - at) / 0.45) if at is not None else 1.0
        x = x0 + k * (w + gap)
        col = RED if state == "bad" else YELLOW if state == "warn" else (1, 1, 1, 1)
        cr.save()
        cr.translate(x + w / 2, y + 38)
        s = 1 + 0.12 * (1 - pop)
        cr.scale(s, s)
        rrect(cr, -w / 2, -38, w, 76, 12)
        cr.set_source_rgba(0.04, 0.04, 0.06, 0.78)
        cr.fill_preserve()
        cr.set_source_rgba(*(col[:3] if state else (1, 1, 1)), 0.9 if state else 0.14)
        cr.set_line_width(2.5)
        cr.stroke()
        _text(cr, label, -w / 2 + 14, -12, 15, (1, 1, 1, 0.55), MONO)
        blink = state == "bad" and (t % 0.8) > 0.55
        _text(cr, value, -w / 2 + 14, 24, 30, (*col[:3], 0.45 if blink else 1), ROUND)
        cr.restore()


# ------------------------------------------------------------------ captions (sentence case, key word coloured)
def _chunks(tl):
    from motion.captions import _chunks as base
    return base(tl)


_caps = {}


def captions(cr, t, tl, key=(), y=905, size=52, max_w=600, key_col=RED, skip=()):
    """`skip`: beat ids whose words are shown in a speech bubble instead."""
    chunks = _caps.get(id(tl))
    if chunks is None:
        chunks = _caps[id(tl)] = _chunks(tl)
    for b in tl.beats:
        if b.id in skip and b.start - 0.05 <= t <= b.end + 0.3:
            return
    keys = {k.lower() for k in key}
    for i, ch in enumerate(chunks):
        start = ch[0].start
        nxt = chunks[i + 1][0].start if i + 1 < len(chunks) else tl.total
        stop = nxt if nxt - ch[-1].end < 0.5 else ch[-1].end + 0.25
        if not (start - 0.02 <= t < stop):
            continue
        words = [u.shown for u in ch]
        if words:
            words[0] = words[0][:1].upper() + words[0][1:]
        space = text_width(cr, " ", size, ROUND) * 1.1
        widths = [text_width(cr, w, size, ROUND) for w in words]
        total = sum(widths) + space * (len(words) - 1)
        sz = size * min(1, max_w / total)
        k = 0.92 + 0.08 * clamp01((t - start) / 0.1)
        cr.save()
        cr.translate(W / 2, y)
        cr.scale(k, k)
        x = -total * sz / size / 2
        for wd, w, u in zip(widths, words, ch):
            bare = w.strip(".,!?\"'").lower()
            hot = bare in keys or any(c.isdigit() for c in bare)
            col = key_col if hot else (1, 1, 1, 1)
            _text(cr, w, x, 0, sz, col, ROUND, outline=(0.05, 0.03, 0.06, 1), ow=sz * 0.16, shadow=0.45)
            x += (wd + space) * sz / size
        cr.restore()
        return


def hook(cr, t, lines, end, y=230, size=78):
    """The hook in big rounded type from frame 0: [(text, red?)]."""
    if t >= end + 0.25:
        return
    a = 1.0 if t < end else 1 - (t - end) / 0.25
    cr.save()
    cr.push_group()
    for k, (txt, red) in enumerate(lines):
        sz = min(size, size * (W - 70) / max(1, text_width(cr, txt, size, ROUND)))
        _text(cr, txt, W / 2, y + k * size * 1.05, sz, RED if red else (1, 1, 1, 1), ROUND, "center",
              outline=(0.05, 0.03, 0.06, 1), ow=sz * 0.14, shadow=0.5)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


# ------------------------------------------------------------------ the rule tag, stamps, title cards
def rule_tag(cr, t, start, end, text, x=W / 2, y=250, rot=-0.06):
    if t < start or t > end + 0.2:
        return
    a = clamp01((t - start) / 0.12) * (1 - clamp01((t - end) / 0.2))
    s = 1.35 - 0.35 * clamp01((t - start) / 0.18)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    size = min(40.0, 40 * (W - 110) / text_width(cr, text, 40, ROUND))      # long rules shrink to fit the frame
    w = text_width(cr, text, size, ROUND) + 50
    cr.push_group()
    rrect(cr, -w / 2, -38, w, 76, 8)
    cr.set_source_rgba(*YELLOW)
    cr.fill_preserve()
    cr.set_source_rgba(*INK)
    cr.set_line_width(5)
    cr.stroke()
    _text(cr, text, 0, size * 0.35, size, INK, ROUND, "center")
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def stamp(cr, t, start, end, lines, x=W / 2, y=360, rot=-0.12, col=RED):
    """A rubber stamp slammed on screen (WHO PRESSED 13? / OUT OF SERVICE)."""
    if t < start or t > end + 0.2:
        return
    a = clamp01((t - start) / 0.06) * (1 - clamp01((t - end) / 0.2))
    s = 1.6 - 0.6 * clamp01((t - start) / 0.12)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.push_group()
    sizes = [70 if k == 0 else 34 for k in range(len(lines))]
    w = max(text_width(cr, l, sz, ROUND) for l, sz in zip(lines, sizes)) + 60
    h = sum(sz * 1.2 for sz in sizes) + 30
    rrect(cr, -w / 2, -h / 2, w, h, 14)
    cr.set_source_rgba(*col[:3], 0.95)
    cr.set_line_width(8)
    cr.stroke()
    yy = -h / 2 + 15
    for l, sz in zip(lines, sizes):
        yy += sz
        _text(cr, l, 0, yy, sz, (*col[:3], 0.95), ROUND, "center")
        yy += sz * 0.2
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def title_card(cr, t, start, end, kicker, big, sub, big_col=RED):
    """A full-screen chapter card on black (PART 1 · THE ELEVATOR / FLOOR 13 / line)."""
    if t < start or t > end + 0.2:
        return
    a = clamp01((t - start) / 0.15) * (1 - clamp01((t - end) / 0.2))
    cr.save()
    cr.push_group()
    cr.set_source_rgba(0.02, 0.02, 0.04, 1)
    cr.paint()
    _text(cr, kicker, W / 2, 520, 22, (1, 1, 1, 0.55), MONO, "center")
    glow(cr, W / 2, 640, 260, big_col, 0.18)
    _text(cr, big, W / 2, 680, 150, big_col, ROUND, "center")
    _text(cr, sub, W / 2, 770, 30, (1, 1, 1, 0.85), ROUND, "center")
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


# ------------------------------------------------------------------ speech bubbles
def bubble(cr, t, start, end, text, x, y, tail, w=430, size=34, creepy=False):
    """A speech bubble at (x, y) (its centre) with a tail pointing at `tail`; the text types on over the line."""
    if t < start - 0.1 or t > end + 0.35:
        return
    a = clamp01((t - start + 0.1) / 0.15) * (1 - clamp01((t - end - 0.15) / 0.2))
    shown = text[:max(1, int(len(text) * clamp01((t - start) / max(0.3, (end - start) * 0.85))))]
    lines, cur = [], ""
    for word in text.split():
        nxt = (cur + " " + word).strip()
        if cur and text_width(cr, nxt, size, ROUND) > w - 50:
            lines.append(cur)
            cur = word
        else:
            cur = nxt
    lines.append(cur)
    h = 34 + len(lines) * size * 1.2
    jx = 2.0 * math.sin(t * 31) if creepy else 0.0
    cr.save()
    cr.translate(x + jx, y)
    cr.push_group()
    fill = (0.93, 0.9, 0.86, 1) if creepy else (1, 1, 1, 1)
    cr.new_path()
    rrect(cr, -w / 2, -h / 2, w, h, 26)
    tx, ty = tail[0] - x, tail[1] - y
    bx = max(-w / 2 + 40, min(w / 2 - 40, tx * 0.3))
    by = h / 2 if ty > 0 else -h / 2
    cr.move_to(bx - 22, by)
    cr.line_to(tx, ty)
    cr.line_to(bx + 22, by)
    cr.close_path()
    cr.set_source_rgba(*fill)
    cr.fill_preserve()
    cr.set_source_rgba(*INK)
    cr.set_line_width(5)
    cr.stroke()
    rrect(cr, -w / 2 + 3, -h / 2 + 3, w - 6, h - 6, 24)
    cr.set_source_rgba(*fill)
    cr.fill()
    # typed text: draw the full lines but only up to the shown length
    left = len(shown)
    yy = -h / 2 + 17 + size
    for ln in lines:
        part = ln[:max(0, left)]
        left -= len(ln) + 1
        if part:
            _text(cr, part, -w / 2 + 25, yy, size, INK, ROUND)
        yy += size * 1.2
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


# ------------------------------------------------------------------ the phone, held in two hands
def phone_pov(cr, t, start, clock, date, notes, glow_a=1.0, skin=None, sleeve=None):
    """The phone filling the frame, held in both hands (point of view), lock screen with notifications.
    notes = [(time, app, title, text)]; each slides in with a buzz (add a 5th item, False, for a silent one: a
    buzz under a spoken word can be misheard)."""
    sk = skin or tk.SKIN
    sl = sleeve or tk.HOOD
    lift = (1 - clamp01((t - start) / 0.35)) ** 2 * 500
    cr.save()
    cr.translate(0, lift)
    glow(cr, W / 2, 620, 520, (0.55, 0.7, 1), 0.3 * glow_a)
    x0, y0, w, h = 150, 210, 420, 860
    for sx in (-1, 1):                                       # sleeves coming up from the bottom corners
        tk.toon(cr, lambda c, sx=sx: tk.curve(c, [(W / 2 + sx * 120, 1400), (W / 2 + sx * 300, 1300),
                                                  (W / 2 + sx * 250, 900), (W / 2 + sx * 170, 860),
                                                  (W / 2 + sx * 120, 1000)]), sl, tk.HOOD_D, (-14, -10), None)
    tk.toon(cr, lambda c: tk.tk_rrect(c, x0, y0, w, h, 54), hexa("#16171b"), None, (0, 0), None, lw=6)
    g = cairo.LinearGradient(0, y0, 0, y0 + h)
    g.add_color_stop_rgba(0, *hexa("#3a3f8f"))
    g.add_color_stop_rgba(1, *hexa("#7a3f78"))
    tk.tk_rrect(cr, x0 + 14, y0 + 14, w - 28, h - 28, 42)
    cr.set_source(g)
    cr.fill()
    cr.set_source_rgba(0, 0, 0, 1)
    tk.tk_rrect(cr, W / 2 - 55, y0 + 28, 110, 26, 13)
    cr.fill()
    _text(cr, clock, W / 2, y0 + 190, 104, (1, 1, 1, 0.95), ROUND, "center")
    _text(cr, date, W / 2, y0 + 236, 26, (1, 1, 1, 0.8), ROUND, "center")
    yy = y0 + 290
    for at, app, title, text, *buzz in notes:
        if t < at:
            break
        k = clamp01((t - at) / 0.25)
        if not buzz or buzz[0]:
            cue("buzz", t, at)
        cr.save()
        cr.translate((1 - k) * 60, 0)
        lines, cur = [], ""
        for word in text.split():
            nxt = (cur + " " + word).strip()
            if cur and text_width(cr, nxt, 27, UI) > w - 90:
                lines.append(cur)
                cur = word
            else:
                cur = nxt
        lines.append(cur)
        bh = 86 + 34 * len(lines)
        tk.tk_rrect(cr, x0 + 28, yy, w - 56, bh, 22)
        cr.set_source_rgba(0.97, 0.97, 0.98, 0.96 * k)
        cr.fill()
        tk.tk_rrect(cr, x0 + 44, yy + 16, 28, 28, 7)
        cr.set_source_rgba(*(GREEN[:3]), k)
        cr.fill()
        _text(cr, app, x0 + 84, yy + 37, 18, (0.4, 0.4, 0.45, k), UI)
        _text(cr, "now", x0 + w - 48, yy + 37, 18, (0.4, 0.4, 0.45, k), UI, "right")
        _text(cr, title, x0 + 44, yy + 72, 26, (0.08, 0.08, 0.1, k), UI)
        for j, ln in enumerate(lines):
            _text(cr, ln, x0 + 44, yy + 106 + 34 * j, 27, (0.15, 0.15, 0.18, k), UI)
        cr.restore()
        yy += bh + 14
    for sx in (-1, 1):                                       # thumbs and fingers over the phone's edges
        tk.toon(cr, lambda c, sx=sx: tk.curve(c, [(W / 2 + sx * 230, 1010), (W / 2 + sx * 262, 940),
                                                  (W / 2 + sx * 250, 880), (W / 2 + sx * 214, 870),
                                                  (W / 2 + sx * 196, 930), (W / 2 + sx * 180, 1000)]),
                sk, tk.SKIN_D, (-10, -8), None, lw=4)
    cr.restore()


# ------------------------------------------------------------------ the ending
def ab_card(cr, t, start, a_text, b_text, a_col=RED, b_col=GREEN, kicker="YOUR CHOICE", decides="Part 2",
            title="WHAT DO YOU DO?", ask="COMMENT A OR B", letters=("A", "B")):
    """WHAT DO YOU DO? with option cards A and B, then COMMENT A OR B / Top answer decides Part 2."""
    if t < start:
        return
    k = clamp01((t - start) / 0.25)
    cr.set_source_rgba(0.02, 0.02, 0.04, 0.82 * k)
    cr.paint()
    _text(cr, kicker, W / 2, 250, 20, (1, 1, 1, 0.55 * k), MONO, "center")
    tsz = min(60.0, 60 * (W - 60) / text_width(cr, title, 60, ROUND))
    _text(cr, title, W / 2, 320, tsz, (1, 1, 1, k), ROUND, "center", shadow=0.4)
    for n, (letter, label, col) in enumerate(((letters[0], a_text, a_col), (letters[1], b_text, b_col))):
        p = clamp01((t - start - 0.2 - 0.15 * n) / 0.25)
        if p <= 0:
            continue
        cx = W / 2 + (-150 if n == 0 else 150)
        cr.save()
        cr.translate(cx, 510)
        cr.scale(0.8 + 0.2 * p, 0.8 + 0.2 * p)
        rrect(cr, -125, -125, 250, 250, 26)
        cr.set_source_rgba(0.06, 0.06, 0.08, p)
        cr.fill_preserve()
        glow(cr, 0, 0, 200, col, 0.18 * p)
        rrect(cr, -125, -125, 250, 250, 26)
        cr.set_source_rgba(*col[:3], p)
        cr.set_line_width(7)
        cr.stroke()
        cr.arc(0, -50, 40, 0, 2 * math.pi)
        cr.set_source_rgba(*col[:3], p)
        cr.fill()
        _text(cr, letter, 0, -32, 50, (0.05, 0.05, 0.07, p), ROUND, "center")
        words = label.split()
        if len(words) == 3:                                   # three short words, three lines (PUT / IT / BACK)
            for j, wd in enumerate(words):
                _text(cr, wd, 0, 28 + j * 34, 30, (1, 1, 1, p), ROUND, "center")
        for j, wd in enumerate(words[:2] if len(words) != 3 else []):
            _text(cr, wd, 0, 40 + j * 40, 36 if len(words) > 1 else 40, (1, 1, 1, p), ROUND, "center")
        cr.restore()
    p = clamp01((t - start - 0.6) / 0.25)
    if p > 0:
        cr.save()
        cr.translate(W / 2, 715)
        asz = min(40.0, 40 * 380 / text_width(cr, ask, 40, ROUND))
        aw = max(420, text_width(cr, ask, asz, ROUND) + 60)
        rrect(cr, -aw / 2, -42, aw, 84, 42)
        cr.set_source_rgba(*YELLOW[:3], p)
        cr.fill()
        _text(cr, ask, 0, 14, asz, (0.08, 0.06, 0.04, p), ROUND, "center")
        cr.restore()
        _text(cr, f"Top answer decides {decides}", W / 2, 795, 26, (1, 1, 1, 0.85 * p), ROUND, "center")
