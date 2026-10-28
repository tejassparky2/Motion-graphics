"""Covers for the story Shorts (anime look), 1080 x 1920: the Shorts cover and the Reels cover.

    /home/user/.venv-main/bin/python channels/stories/thumbs.py dma_s1   -> out/stories/thumbs/dma_s1.png
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.environ.setdefault("FONTCONFIG_FILE", os.path.join(ROOT, "build", "fonts.conf"))
from motion.engine import W, H, cairo   # noqa: E402
from motion import satsuei   # noqa: E402

from channels.horror import hud2d   # noqa: E402
from channels.horror.thumbs import big_text, chip   # noqa: E402
from channels.horror.toon2d import glow   # noqa: E402
from channels.stories import dma_anime as A   # noqa: E402

OUT = os.path.join(ROOT, "out", "stories", "thumbs")


def dma_s1(cr):
    """Ren's frightened face, big, the meteor burning in the classroom window behind him: 20 SURVIVORS."""
    t = 30.0
    A.classroom(cr, t, meteor=0.85)
    cr.set_source_rgba(0.1, 0.03, 0.0, 0.25)
    cr.paint()
    A.student_bust(cr, W * 0.5, H * 0.9, 1.75, t, "ren", "fear")
    glow(cr, W * 0.15, H * 0.2, 700, (1, 0.55, 0.2), 0.35)
    satsuei.apply(cr, t, glow=0.3, light=((0.15, 0.2), (1.0, 0.75, 0.5), 0.25), ca=1.5, grain=0.03)
    g = cairo.LinearGradient(0, 100, 0, 470)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.75)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.paint()
    big_text(cr, [("12:17.", (1, 1, 1, 1)), ("20 SURVIVORS.", hud2d.RED)], 250, 118)
    chip(cr, "DEAD MAN'S ALGORITHM · PART 1")


def dma_s2(cr):
    """Riku's smirk in the cold room, the exit key in its glass case beside him: 100 TOKENS. TIE = ELIMINATED."""
    t = 40.0
    A.chamber(cr, t, flicker=False)
    cr.set_source_rgba(0.0, 0.02, 0.05, 0.35)
    cr.paint()
    A.glass_case(cr, t, W * 0.72, H * 0.6, 1.1)
    glow(cr, W * 0.72, H * 0.55, 420, (1, 0.85, 0.4), 0.3)
    A.student_bust(cr, W * 0.38, H * 0.92, 1.6, t, "riku", "smirk")
    satsuei.apply(cr, t, glow=0.3, light=((0.7, 0.4), (1.0, 0.85, 0.55), 0.22), ca=1.5, grain=0.03)
    g = cairo.LinearGradient(0, 100, 0, 470)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.75)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.paint()
    big_text(cr, [("100 TOKENS.", (1, 1, 1, 1)), ("TIE = ELIMINATED.", hud2d.RED)], 250, 112)
    chip(cr, "DEAD MAN'S ALGORITHM · PART 2")


THUMBS = {"dma_s1": dma_s1, "dma_s2": dma_s2}

if __name__ == "__main__":
    name = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    scale = 1.5                                              # draw at 720 x 1280, save at 1080 x 1920
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W * scale), int(H * scale))
    cr = cairo.Context(s)
    cr.scale(scale, scale)
    THUMBS[name](cr)
    path = os.path.join(OUT, f"{name}.png")
    s.write_to_png(path)
    print("wrote", path)
