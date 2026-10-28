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
from channels.stories import dma_kit as K   # noqa: E402

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


def dma_s3(cr):
    """Ren lit by his bidding terminal, BID 1 on it: MY NUMBER: ONE."""
    t = 40.0
    A.chamber(cr, t, flicker=False)
    cr.set_source_rgba(0.0, 0.02, 0.05, 0.35)
    cr.paint()
    A.student_bust(cr, W * 0.5, H * 0.86, 1.6, t, "ren", "focus")
    A.terminal(cr, t, W * 0.76, H * 0.86, 0.75, tokens=100, bid=1)
    glow(cr, W * 0.76, H * 0.8, 380, (0.4, 1, 0.9), 0.25)
    satsuei.apply(cr, t, glow=0.3, light=((0.8, 0.7), (0.5, 1.0, 0.9), 0.22), ca=1.5, grain=0.03)
    _top_shade(cr)
    big_text(cr, [("MY NUMBER:", (1, 1, 1, 1)), ("ONE.", hud2d.RED)], 250, 118)
    chip(cr, "DEAD MAN'S ALGORITHM · PART 3")


def dma_s4(cr):
    """Saki, quiet, in the white room, Momo small behind her: THE POOREST DIES."""
    t = 40.0
    K.white_room(cr, t, K.players(20), side=True)
    A.student_bust(cr, W * 0.5, H * 0.92, 1.7, t, "saki", "calm")
    satsuei.apply(cr, t, glow=0.25, light=((0.5, 0.0), (0.92, 0.96, 1.0), 0.15), ca=1.5, grain=0.03)
    _top_shade(cr)
    big_text(cr, [("THE POOREST", (1, 1, 1, 1)), ("DIES.", hud2d.RED)], 250, 118)
    chip(cr, "DEAD MAN'S ALGORITHM · PART 4")


def dma_s5(cr):
    """Momo on its heap of gold tokens, Ren in front: 0 PLAYERS. 0 DEATHS?"""
    t = 40.0
    K.white_room(cr, t, K.players(1), momo=False, pile=1.0)
    A.momo(cr, W * 0.62, H * 0.66, 2.0, t, mood="sly")
    A.student_bust(cr, W * 0.3, H * 0.95, 1.4, t, "ren", "focus")
    satsuei.apply(cr, t, glow=0.28, light=((0.6, 0.4), (1.0, 0.9, 0.6), 0.2), ca=1.5, grain=0.03)
    _top_shade(cr)
    big_text(cr, [("0 PLAYERS.", (1, 1, 1, 1)), ("0 DEATHS?", hud2d.RED)], 250, 118)
    chip(cr, "DEAD MAN'S ALGORITHM · PART 5")


def dma_s6(cr):
    """Saki frightened, one gold token glinting in front of her: ONE TOKEN. PLAYERS: 2."""
    t = 40.0
    K.white_room(cr, t, K.players(2), red=True, pile=1.0, side=True)
    cr.set_source_rgba(0.05, 0.0, 0.02, 0.25)
    cr.paint()
    A.student_bust(cr, W * 0.5, H * 0.95, 1.75, t, "saki", "fear")
    K.token(cr, W * 0.78, H * 0.78, 90, glint=1.0)
    satsuei.apply(cr, t, glow=0.3, light=((0.78, 0.75), (1.0, 0.85, 0.5), 0.25), ca=1.5, grain=0.03)
    _top_shade(cr)
    big_text(cr, [("ONE TOKEN.", (1, 1, 1, 1)), ("PLAYERS: 2", hud2d.RED)], 250, 118)
    chip(cr, "DEAD MAN'S ALGORITHM · PART 6")


def _manga_panel(cr, page, panel, folder="assets/manga/dma/ch01", ax=0.5, ay=0.5, fit=None, yc=0.5, xc=0.5):
    """A manga panel (from the manga chat's page and manifest) filling the cover, or, with fit = a share of the
    width, shown whole across the cover with its centre at yc."""
    import json
    from channels.stories import anime2d as AN
    box = json.load(open(os.path.join(ROOT, folder, "manifest.json")))["pages"][str(page)]["panels"][panel - 1]["box"]
    surf = AN.image(f"{folder}/page_{page:02d}.jpg")
    x0, y0, x1, y1 = box
    k = W * fit / (x1 - x0) if fit else max(W / (x1 - x0), H / (y1 - y0))
    cr.save()
    cr.translate(W * xc, H * yc)
    cr.scale(k, k)
    cr.translate(-(x0 + (x1 - x0) * ax), -(y0 + (y1 - y0) * ay))
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)                    # this panel only
    cr.clip()
    cr.set_source_surface(surf, 0, 0)
    cr.get_source().set_filter(cairo.FILTER_GOOD)
    cr.paint()
    cr.restore()


def dma_manga01(cr):
    """Aoi's glasses with the streak of light in them (page 7): THE LAST NORMAL MINUTE."""
    cr.set_source_rgba(0.05, 0.05, 0.06, 1)
    cr.paint()
    _manga_panel(cr, 7, 4, fit=1.0, yc=0.5)                   # Aoi's glasses with the streak in them...
    _manga_panel(cr, 6, 1, fit=1.0, yc=0.82)                  # ...while Riku slams the desk
    _top_shade(cr, 520)
    big_text(cr, [("THE LAST", (1, 1, 1, 1)), ("NORMAL MINUTE.", hud2d.RED)], 250, 112)
    chip(cr, "DEAD MAN'S ALGORITHM · THE MANGA · EP 1")


def dma_manga02(cr):
    """The meteor filling the sky over the school (page 10), Ren frozen in its glare (page 11): 12:17:05."""
    cr.set_source_rgba(0.05, 0.05, 0.06, 1)
    cr.paint()
    _manga_panel(cr, 10, 1, fit=1.0, yc=0.52)
    _manga_panel(cr, 11, 1, fit=1.0, yc=0.84)
    _top_shade(cr, 520)
    big_text(cr, [("12:17:05.", (1, 1, 1, 1)), ("THE SKY FELL.", hud2d.RED)], 250, 112)
    chip(cr, "DEAD MAN'S ALGORITHM · THE MANGA · EP 2")


def dma_manga03(cr):
    """Momo waving in its spotlight (page 20) over Ren's cold stare (page 19): 20 SURVIVORS. OF WHAT?"""
    cr.set_source_rgba(0.05, 0.05, 0.06, 1)
    cr.paint()
    _manga_panel(cr, 20, 3, fit=1.0, yc=0.52)
    _manga_panel(cr, 19, 4, fit=1.0, yc=0.84)
    _top_shade(cr, 520)
    big_text(cr, [("20 SURVIVORS.", (1, 1, 1, 1)), ("OF WHAT?", hud2d.RED)], 250, 112)
    chip(cr, "DEAD MAN'S ALGORITHM · THE MANGA · EP 3")


def dma_manga04(cr):
    """Momo starting the clock (page 25) over Ren's eyes reading the rules: 10 MINUTES. ONE KEY."""
    cr.set_source_rgba(0.05, 0.05, 0.06, 1)
    cr.paint()
    _manga_panel(cr, 25, 4, fit=1.0, yc=0.53)
    _manga_panel(cr, 25, 3, fit=1.0, yc=0.88)
    _top_shade(cr, 520)
    big_text(cr, [("10 MINUTES.", (1, 1, 1, 1)), ("ONE KEY.", hud2d.RED)], 250, 112)
    chip(cr, "DEAD MAN'S ALGORITHM · THE MANGA · EP 4")


def dma_manga05(cr):
    """Ren's resolve (Chapter 2 page 5), filling the cover: MY NUMBER WAS ONE."""
    folder = "assets/manga/dma/ch02"
    cr.set_source_rgba(0.05, 0.05, 0.06, 1)
    cr.paint()
    _manga_panel(cr, 5, 1, folder, ax=0.5, ay=0.42, yc=0.6)
    _top_shade(cr, 520)
    big_text(cr, [("MY NUMBER", (1, 1, 1, 1)), ("WAS ONE.", hud2d.RED)], 250, 112)
    chip(cr, "DEAD MAN'S ALGORITHM · THE MANGA · EP 5")


def dma_manga06(cr):
    """Riku's grin (Chapter 2 page 9) over Momo announcing the result (page 8): HE BID THIRTY."""
    folder = "assets/manga/dma/ch02"
    cr.set_source_rgba(0.05, 0.05, 0.06, 1)
    cr.paint()
    _manga_panel(cr, 9, 1, folder, fit=1.0, yc=0.52)
    _manga_panel(cr, 9, 2, folder, fit=0.62, yc=0.86, xc=0.69)
    _manga_panel(cr, 9, 3, folder, fit=0.62, yc=0.86, xc=0.31)
    _top_shade(cr, 520)
    big_text(cr, [("HE LIED.", (1, 1, 1, 1)), ("THE PLAN HELD.", hud2d.RED)], 250, 112)
    chip(cr, "DEAD MAN'S ALGORITHM · THE MANGA · EP 6")


def dma_manga_ch02_long(cr):
    """16:9: Riku's grin (Chapter 2 page 9) on the right, Ren's resolve (page 5) below it, the title on the left:
    CHAPTER 2 / THE BIDS."""
    folder = "assets/manga/dma/ch02"
    cr.set_source_rgba(0.05, 0.05, 0.06, 1)
    cr.paint()
    _manga_panel(cr, 9, 1, folder, fit=0.62, yc=0.36, xc=0.68)
    _manga_panel(cr, 5, 1, folder, fit=0.44, yc=0.8, xc=0.76)
    g = cairo.LinearGradient(0, 0, W * 0.55, 0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.paint()
    for k, (txt, col, sz) in enumerate((("CHAPTER 2", (1, 1, 1, 1), 96), ("THE BIDS.", hud2d.RED, 110),
                                        ("FULL CHAPTER", (1, 0.85, 0.4, 1), 40))):
        hud2d._text(cr, txt, 50, 230 + k * 120, sz, col, hud2d.ROUND, "left", outline=(0, 0, 0, 1), ow=sz * 0.12,
                    shadow=0.6)
    hud2d._text(cr, "DEAD MAN'S ALGORITHM · THE MANGA", 50, 100, 30, (1, 0.85, 0.4, 1), hud2d.ROUND, "left",
                outline=(0, 0, 0, 1), ow=4)


def dma_manga_ch03_long(cr):
    """16:9: Saki with the single token in her palm (Chapter 3 page 14) on the right, Riku's smile (page 11) below it,
    the title on the left: CHAPTER 3 / THE CHARITY."""
    folder = "assets/manga/dma/ch03"
    cr.set_source_rgba(0.05, 0.05, 0.06, 1)
    cr.paint()
    _manga_panel(cr, 14, 1, folder, fit=0.62, yc=0.36, xc=0.68)
    _manga_panel(cr, 11, 3, folder, fit=0.44, yc=0.8, xc=0.76)
    g = cairo.LinearGradient(0, 0, W * 0.55, 0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.paint()
    for k, (txt, col, sz) in enumerate((("CHAPTER 3", (1, 1, 1, 1), 96), ("THE CHARITY.", hud2d.RED, 96),
                                        ("FULL CHAPTER", (1, 0.85, 0.4, 1), 40))):
        hud2d._text(cr, txt, 50, 230 + k * 120, sz, col, hud2d.ROUND, "left", outline=(0, 0, 0, 1), ow=sz * 0.12,
                    shadow=0.6)
    hud2d._text(cr, "DEAD MAN'S ALGORITHM · THE MANGA", 50, 100, 30, (1, 0.85, 0.4, 1), hud2d.ROUND, "left",
                outline=(0, 0, 0, 1), ow=4)


def dma_manga_ch01_long(cr):
    """16:9: the meteor filling the sky (page 10) on the right, Momo waving in its spotlight (page 20) below it, the
    chapter title on the left: CHAPTER 1 / 12:17."""
    cr.set_source_rgba(0.05, 0.05, 0.06, 1)
    cr.paint()
    _manga_panel(cr, 10, 1, fit=0.62, yc=0.36, xc=0.68)
    _manga_panel(cr, 20, 3, fit=0.4, yc=0.8, xc=0.78)
    g = cairo.LinearGradient(0, 0, W * 0.55, 0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.92)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.paint()
    for k, (txt, col, sz) in enumerate((("CHAPTER 1", (1, 1, 1, 1), 96), ("12:17.", hud2d.RED, 120),
                                        ("FULL CHAPTER", (1, 0.85, 0.4, 1), 40))):
        hud2d._text(cr, txt, 50, 230 + k * 120, sz, col, hud2d.ROUND, "left", outline=(0, 0, 0, 1), ow=sz * 0.12,
                    shadow=0.6)
    hud2d._text(cr, "DEAD MAN'S ALGORITHM · THE MANGA", 50, 100, 30, (1, 0.85, 0.4, 1), hud2d.ROUND, "left",
                outline=(0, 0, 0, 1), ow=4)


THUMBS = {"dma_s1": dma_s1, "dma_s2": dma_s2, "dma_long": dma_long, "boy_s1": boy_s1, "boy_s2": boy_s2,
          "boy_long": boy_long, "dma_s3": dma_s3, "dma_s4": dma_s4, "dma_s5": dma_s5, "dma_s6": dma_s6,
          "dma_manga01": dma_manga01, "dma_manga02": dma_manga02,
          "dma_manga03": dma_manga03, "dma_manga04": dma_manga04, "dma_manga_ch01_long": dma_manga_ch01_long,
          "dma_manga05": dma_manga05, "dma_manga06": dma_manga06, "dma_manga_ch02_long": dma_manga_ch02_long,
          "dma_manga_ch03_long": dma_manga_ch03_long}

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
