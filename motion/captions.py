"""Word-by-word kinetic captions timed from the narration's word timestamps.

1-3 words per chunk on one line, breaking at punctuation; the word being spoken is highlighted.
Placed ~71% down the frame: below the characters' faces, above the bottom ~25% that the YouTube Shorts UI covers.
"""
import math

from .engine import FONT, INK, W, cairo, clamp01, hexc

Y = 915            # baseline: over bodies, clear of faces and of the bottom ~25% YouTube UI
MAX_W = 560        # keep clear of the right-side UI
SIZE = 62
FILL = hexc("#ffffff")
HIGHLIGHT = hexc("#ffd23f")
PUNCT = ".,!?:;"


def _chunks(tl):
    out = []
    for b in tl.beats:
        cur = []
        for u in b.units:
            cur.append(u)
            text = " ".join(x.shown for x in cur)
            if u.shown[-1] in PUNCT or len(cur) == 3 or len(text) > 16:
                out.append(cur)
                cur = []
        if cur:
            out.append(cur)
    return out


_cache = {}


def captions(cr, t, tl):
    chunks = _cache.get(id(tl))
    if chunks is None:
        chunks = _cache[id(tl)] = _chunks(tl)
    for i, ch in enumerate(chunks):
        start = ch[0].start
        nxt = chunks[i + 1][0].start if i + 1 < len(chunks) else tl.total
        stop = nxt if nxt - ch[-1].end < 0.5 else ch[-1].end + 0.2
        if start - 0.02 <= t < stop:
            _draw(cr, t, ch, start)
            return


def _draw(cr, t, chunk, start):
    words = [u.shown.rstrip(",.;:") or u.shown for u in chunk]
    cr.save()
    cr.identity_matrix()
    cr.select_font_face(FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    size = SIZE
    cr.set_font_size(size)
    space = cr.text_extents(" ").x_advance
    widths = [cr.text_extents(w).x_advance for w in words]
    total = sum(widths) + space * (len(words) - 1)
    if total > MAX_W:
        size *= MAX_W / total
        cr.set_font_size(size)
        space *= MAX_W / total
        widths = [w * MAX_W / total for w in widths]
        total = MAX_W
    # quick pop-in
    u = clamp01((t - start) / 0.1)
    sc = 0.86 + 0.14 * (1 - (1 - u) ** 3)
    cr.translate(W / 2, Y - size * 0.35)
    cr.scale(sc, sc)
    cr.translate(-W / 2, -(Y - size * 0.35))
    x = W / 2 - total / 2
    for word, wdt, unit in zip(words, widths, chunk):
        active = unit.start - 0.03 <= t < unit.end + 0.05 or (t >= unit.end and unit is chunk[-1])
        lift = -4 * math.sin(math.pi * clamp01((t - unit.start) / 0.12)) if active else 0
        cr.move_to(x, Y + lift)
        cr.text_path(word)
        cr.set_source_rgba(*INK)
        cr.set_line_width(size * 0.17)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke_preserve()
        cr.set_source_rgba(*(HIGHLIGHT if active else FILL))
        cr.fill()
        x += wdt + space
    cr.restore()
