"""WW2 Episode 1 thumbnail (helper 8): a 1942 world map in the side colours, THE WHOLE WAR in slab, and a small
Churchill / Stalin / Hitler trio of poster portraits. Sides are colours only: no symbols, no flags.

    python channels/ww2/ep01/thumbnail.py        # -> out/ww2/ep01/thumbnail.png (1280x720) + thumbnail_check.png

thumbnail_check.png puts the thumbnail at the sizes YouTube shows it (search 360 px, phone feed 246 px, sidebar 168 px)
for the readability check: the words and the faces must still read at 168 px.
"""
import os
import sys

import cairo

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, ROOT)
from channels.ww2.kit import heads  # noqa: E402
from channels.ww2.kit.core import H, SLAB, STENCIL, W, col, paper, print_finish, text  # noqa: E402
from channels.ww2.kit.maps import Map  # noqa: E402

OUT = os.path.join(ROOT, "out", "ww2", "ep01")
TW, TH = 1280, 720
T = 2.0                                     # a still moment: blinks off, idle mid-breath


def world_1942():
    """The world at the Axis high tide (late 1942), coloured by side; occupied land in halftone."""
    m = Map("world", compass=False)
    for r in ("deu", "aut"):
        m.side(r, -1, "germany", occupied=False)
    m.side("ita", -1, "italy", occupied=False)
    m.side("jpn", -1, "japan", occupied=False)
    for r in m.regions("axis_1942_occupied"):
        if r in m.bbox:
            x0, _, x1, _ = m.bbox[r]
            east = (x0 + x1) / 2 > m.xy((60.0, 0.0))[0]          # east of the Urals' longitude: Japan's empire
            m.side(r, -1, "japan" if east else "germany", occupied=True)
    m.side("axis_minors", -1, "axis", occupied=False)
    m.side("ussr", -1, "soviet", occupied=False)
    m.side("chn", -1, "china", occupied=False)
    for g in ("allies_1942", "commonwealth"):
        m.side(g, -1, "allies", occupied=False)
    for r in ("fra",):                                            # Free France fights on, but France itself is occupied
        m.side(r, -1, "germany", occupied=True)
    return m


def draw(cr, t=T):
    paper(cr)
    cr.save()                                                     # the map, pushed in on Eurasia and the Pacific
    cr.translate(W * 0.5, H * 0.5)
    cr.scale(1.32, 1.32)
    cr.translate(-W * 0.43, -H * 0.42)
    world_1942().draw(cr, 0.0)
    cr.restore()
    # the left third darkened under the words, as a printed ink block with a ragged poster edge
    cr.new_path()
    cr.move_to(0, 0)
    for x, y in ((1010, 0), (930, 280), (980, 560), (900, 820), (950, 1080), (0, 1080)):
        cr.line_to(x, y)
    cr.close_path()
    cr.set_source_rgba(*col("ink", 0.80))
    cr.fill()
    # the trio, shoulder to shoulder at the bottom right (no sunburst: rays over the red USSR would read as the
    # Rising Sun pattern STYLE.md forbids)
    for who, cx, h, turn in (("stalin", 1210, 640, 0.30), ("hitler", 1755, 640, 0.60), ("churchill", 1480, 720, 0.45)):
        heads.portrait(cr, t, who, cx, H + 40, height=h, expr="determined", turn=turn, idle=False)
    # the words: slab, cream on the ink block, hard ink drop shadow, and the years in stencil
    for s, y, size in (("THE", 268, 190), ("WHOLE", 520, 250), ("WAR", 790, 290)):
        text(cr, s, 70 + 10, y + 10, size, font=SLAB, color="ink", align="left")
        text(cr, s, 70, y, size, font=SLAB, color="cream" if s != "WAR" else "gold", align="left",
             outline="ink", outline_w=10)
    text(cr, "1939 - 1945", 76, 950, 120, font=STENCIL, color="alert", align="left", outline="ink", outline_w=6)
    print_finish(cr, t, strength=0.6)


def main():
    os.makedirs(OUT, exist_ok=True)
    big = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    draw(cairo.Context(big))
    thumb = cairo.ImageSurface(cairo.FORMAT_RGB24, TW, TH)
    c = cairo.Context(thumb)
    c.scale(TW / W, TH / H)
    c.set_source_surface(big, 0, 0)
    c.get_source().set_filter(cairo.FILTER_BEST)
    c.paint()
    path = os.path.join(OUT, "thumbnail.png")
    thumb.write_to_png(path)
    # the readability check: the thumbnail at YouTube's display widths, side by side
    sizes = (360, 246, 168)
    chk = cairo.ImageSurface(cairo.FORMAT_RGB24, sum(sizes) + 40 * len(sizes), 240)
    c = cairo.Context(chk)
    c.set_source_rgb(1, 1, 1)
    c.paint()
    x = 20
    for w in sizes:
        c.save()
        c.translate(x, 20)
        c.scale(w / TW, w / TW)
        c.set_source_surface(thumb, 0, 0)
        c.get_source().set_filter(cairo.FILTER_BEST)
        c.paint()
        c.restore()
        x += w + 40
    chk.write_to_png(os.path.join(OUT, "thumbnail_check.png"))
    print(path, f"{os.path.getsize(path) / 1e6:.2f} MB")


if __name__ == "__main__":
    main()
