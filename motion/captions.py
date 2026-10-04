"""Word-by-word kinetic captions timed from the narration's word timestamps.

1-3 words per chunk on one line, breaking at punctuation; the word being spoken is highlighted.
Placed ~71% down the frame: below the characters' faces, above the bottom ~25% that the YouTube Shorts UI covers.
"""
import math

from . import engine
from .engine import INK, W, cairo, clamp01, hexc

Y = 915            # baseline: over bodies, clear of faces and of the bottom ~25% YouTube UI
MAX_W = 560        # keep clear of the right-side UI
SIZE = 62
FILL = hexc("#ffffff")
HIGHLIGHT = hexc("#ffd23f")
PUNCT = ".,!?:;"
# Clean style (Body Facts references): one word at a time, uppercase, white with a dark outline, a little lower.
CLEAN_Y, CLEAN_SIZE = 950, 64
EMPHASIS = set()     # words shown bigger (medical terms); a video can add its own


def _chunks(tl):
    out = []
    if engine.STYLE["clean"]:
        return [[u] for b in tl.beats for u in b.units]
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
            (_draw_clean if engine.STYLE["clean"] else _draw)(cr, t, ch, start)
            return


def _draw(cr, t, chunk, start):
    words = [u.shown.rstrip(",.;:") or u.shown for u in chunk]
    cr.save()
    cr.identity_matrix()
    cr.select_font_face(engine.FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
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


def _draw_clean(cr, t, chunk, start):
    word = chunk[0].shown.strip(",.;:!?\"'“”").upper() or chunk[0].shown.upper()
    key = word.lower()
    size = CLEAN_SIZE * (1.3 if key in EMPHASIS else 1.0)
    cr.save()
    cr.identity_matrix()
    cr.select_font_face(engine.FONT, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    wdt = cr.text_extents(word).x_advance
    if wdt > MAX_W:
        size *= MAX_W / wdt
        cr.set_font_size(size)
        wdt = MAX_W
    u = clamp01((t - start) / 0.08)
    sc = 0.9 + 0.1 * (1 - (1 - u) ** 3)
    cr.translate(W / 2, CLEAN_Y - size * 0.35)
    cr.scale(sc, sc)
    cr.translate(-W / 2, -(CLEAN_Y - size * 0.35))
    x = W / 2 - wdt / 2
    cr.move_to(x + 3, CLEAN_Y + 4)            # soft drop shadow
    cr.text_path(word)
    cr.set_source_rgba(0, 0, 0, 0.35)
    cr.fill()
    cr.move_to(x, CLEAN_Y)
    cr.text_path(word)
    cr.set_source_rgba(*INK)
    cr.set_line_width(size * 0.16)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke_preserve()
    cr.set_source_rgba(*FILL)
    cr.fill()
    cr.restore()
