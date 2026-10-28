"""Covers for the story Shorts (anime look), 1080 x 1920: the Shorts cover and the Reels cover.

    /home/user/.venv-main/bin/python channels/stories/thumbs.py dma_s1   -> out/stories/thumbs/dma_s1.png
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
if len(sys.argv) > 1 and sys.argv[1].endswith("_long"):     # long videos: a 16:9 cover (set before the engine loads)
    os.environ["CANVAS"] = "landscape"
os.environ.setdefault("FONTCONFIG_FILE", os.path.join(ROOT, "build", "fonts.conf"))
from motion.engine import W, H, cairo   # noqa: E402
from motion import satsuei   # noqa: E402

from channels.horror import hud2d   # noqa: E402
from channels.horror.thumbs import big_text, chip   # noqa: E402
from channels.horror.toon2d import glow   # noqa: E402
from channels.stories import dma_anime as A   # noqa: E402
from channels.stories import boy_anime as B   # noqa: E402

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


def _top_shade(cr, h=470):
    g = cairo.LinearGradient(0, 100, 0, h)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.75)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.paint()


def boy_s1(cr):
    """Neil lit by his screens at night, the account figure huge: $5,014,382.61 · ONE DAY LEFT."""
    t = 20.0
    B.trading_room(cr, t, balance=None)
    B.bust(cr, W * 0.5, H * 0.95, 1.7, t, "neil", "focus")
    glow(cr, W * 0.5, H * 0.55, 600, (0.3, 1, 0.6), 0.18)
    satsuei.apply(cr, t, glow=0.3, light=((0.5, 0.35), (0.5, 0.8, 1.0), 0.2), ca=1.5, grain=0.03)
    _top_shade(cr)
    big_text(cr, [("$5,014,382.61", (0.45, 1, 0.65, 1)), ("ONE DAY LEFT.", hud2d.RED)], 250, 112)
    chip(cr, "THE BOY WHO INHERITED ANOTHER BODY · 1")


def boy_s2(cr):
    """The old face in the hospital bed, grief in his eyes, the city below: HE WOKE UP 82."""
    t = 20.0
    B.hospital(cr, t)
    cr.set_source_rgba(0.0, 0.02, 0.06, 0.3)
    cr.paint()
    B.bust(cr, W * 0.5, H * 0.97, 2.1, t, "arthur", "grief")
    satsuei.apply(cr, t, glow=0.28, light=((0.5, 0.1), (0.6, 0.75, 1.0), 0.2), ca=1.5, grain=0.03)
    _top_shade(cr)
    big_text(cr, [("HE DIED AT 17.", (1, 1, 1, 1)), ("HE WOKE UP 82.", hud2d.RED)], 250, 112)
    chip(cr, "THE BOY WHO INHERITED ANOTHER BODY · 2")


def dma_long(cr):
    """16:9: the classroom burning orange, Ren frightened on the right, the meteor in the windows: 12:17."""
    t = 30.0
    A.classroom(cr, t, meteor=0.85)
    A.student_bust(cr, W * 0.72, H * 1.02, 1.05, t, "ren", "fear")
    satsuei.apply(cr, t, glow=0.3, light=((0.2, 0.2), (1.0, 0.75, 0.5), 0.25), ca=1.2, grain=0.03)
    g = cairo.LinearGradient(0, 0, W * 0.6, 0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.7)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.paint()
    for k, (txt, col, sz) in enumerate((("12:17.", (1, 1, 1, 1), 120), ("THE SKY FELL", hud2d.RED, 74),
                                        ("ON US.", hud2d.RED, 74))):
        hud2d._text(cr, txt, 60, 250 + k * 92 + (30 if k else 0), sz, col, hud2d.ROUND, "left", outline=(0, 0, 0, 1),
                    ow=sz * 0.14, shadow=0.6)
    hud2d._text(cr, "DEAD MAN'S ALGORITHM · CHAPTER 1", 60, 120, 30, (1, 0.85, 0.4, 1), hud2d.ROUND, "left",
                shadow=0.6)


def boy_long(cr):
    """16:9: Neil on the left, Arthur on the right, the same eyes: 17 -> 82."""
    t = 20.0
    cr.save()
    cr.rectangle(0, 0, W / 2, H)
    cr.clip()
    B.trading_room(cr, t)
    B.bust(cr, W * 0.25, H * 0.98, 1.15, t, "neil", "fear")
    cr.restore()
    cr.save()
    cr.rectangle(W / 2, 0, W / 2, H)
    cr.clip()
    B.hospital(cr, t)
    B.bust(cr, W * 0.75, H * 0.98, 1.15, t, "arthur", "grief")
    cr.restore()
    satsuei.apply(cr, t, glow=0.28, ca=1.2, grain=0.03)
    cr.set_source_rgba(1, 1, 1, 0.9)
    cr.rectangle(W / 2 - 3, 0, 6, H)
    cr.fill()
    for x, txt in ((W * 0.25, "17"), (W * 0.75, "82")):
        hud2d._text(cr, txt, x, 170, 150, (1, 1, 1, 1), hud2d.ROUND, "center", outline=(0, 0, 0, 1), ow=20,
                    shadow=0.6)
    hud2d._text(cr, "SAME MIND.", W / 2, H * 0.47, 64, hud2d.RED, hud2d.ROUND, "center", outline=(0, 0, 0, 1), ow=10,
                shadow=0.6)


THUMBS = {"dma_s1": dma_s1, "dma_s2": dma_s2, "dma_long": dma_long, "boy_s1": boy_s1, "boy_s2": boy_s2,
          "boy_long": boy_long}

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
