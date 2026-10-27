"""Thumbnails / covers for the horror Shorts, drawn with the episodes' own sets (1080 x 1920, vertical: the Shorts
cover and the Instagram Reels cover).

    /home/user/.venv-main/bin/python channels/horror/thumbs.py tower9_n2   -> out/horror/thumbs/tower9_n2.png
"""
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.environ.setdefault("FONTCONFIG_FILE", os.path.join(ROOT, "build", "fonts.conf"))
from motion.engine import W, H, cairo   # noqa: E402
from motion.polish import text_width   # noqa: E402

from channels.horror import hud2d   # noqa: E402
from channels.horror import toon2d as tk   # noqa: E402
from channels.horror.toon2d import INK, glow   # noqa: E402

OUT = os.path.join(ROOT, "out", "horror", "thumbs")


def big_text(cr, lines, y, size=118):
    """Fat outlined words, each line fitted to the frame: [(text, colour)]."""
    for k, (txt, col) in enumerate(lines):
        sz = min(size, size * (W - 60) / text_width(cr, txt, size, hud2d.ROUND))
        hud2d._text(cr, txt, W / 2, y + k * size * 1.02, sz, col, hud2d.ROUND, "center", outline=INK, ow=sz * 0.16,
                    shadow=0.6)


def badge(cr, x, y, letter, col, r=46):
    glow(cr, x, y, r * 2.4, col, 0.35)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*col)
    cr.fill_preserve()
    cr.set_source_rgba(*INK)
    cr.set_line_width(6)
    cr.stroke()
    hud2d._text(cr, letter, x, y + r * 0.42, r * 1.2, (0.05, 0.05, 0.07, 1), hud2d.ROUND, "center")


def tower9_n2(cr):
    """Your face at the window, finger to its lips, above the frosted hatch: WHO DO YOU LET IN?"""
    from channels.horror import tower9_n2_2d as ep
    t = 26.2
    cr.save()                                                # top: the copy at the window
    cr.rectangle(0, 0, W, 700)
    cr.clip()
    cr.translate(0, -300)
    ep.window_scene(cr, t, ep.copy_close(t, tk.FACES["smile"], 1.0), flash=0.35, dark=0.3)
    cr.restore()
    cr.save()                                                # bottom: the hatch, frost, light leaking from below
    cr.rectangle(0, 700, W, H - 700)
    cr.clip()
    cr.translate(0, 420)
    ep.n1.hatch(cr, t, light=0.9, frost=1.0)
    tk.grade(cr, (0.6, 0.66, 0.85), (0.35, 0.36, 0.45))
    glow(cr, 360, 990, 260, ep.n1.TORCH, 0.35)
    cr.restore()
    cr.set_source_rgba(0.85, 0.9, 1, 0.9)
    cr.rectangle(0, 697, W, 6)
    cr.fill()
    g = cairo.LinearGradient(0, 600, 0, 940)                 # a dark band behind the words
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(0.35, 0, 0, 0, 0.7)
    g.add_color_stop_rgba(0.65, 0, 0, 0, 0.7)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.paint()
    big_text(cr, [("WHO DO YOU", (1, 1, 1, 1)), ("LET IN?", hud2d.RED)], 760, 120)
    badge(cr, 620, 200, "A", hud2d.RED)                     # on the dark glass, clear of the face
    badge(cr, 620, 1010, "B", hud2d.GREEN)                  # above the bottom, where feeds put the title
    hud2d._text(cr, "WINDOW", 552, 216, 40, (1, 1, 1, 1), hud2d.ROUND, "right", outline=INK, ow=7, shadow=0.5)
    hud2d._text(cr, "HATCH", 552, 1026, 40, (1, 1, 1, 1), hud2d.ROUND, "right", outline=INK, ow=7, shadow=0.5)
    cr.save()                                                # the series chip
    tk.tk_rrect(cr, 30, 40, 330, 64, 32)
    cr.set_source_rgba(0.04, 0.04, 0.06, 0.85)
    cr.fill_preserve()
    cr.set_source_rgba(*hud2d.YELLOW)
    cr.set_line_width(3)
    cr.stroke()
    hud2d._text(cr, "TOWER 9 · NIGHT 2", 195, 84, 30, hud2d.YELLOW, hud2d.ROUND, "center")
    cr.restore()


def chip(cr, text):
    w = text_width(cr, text, 30, hud2d.ROUND) + 50
    tk.tk_rrect(cr, 30, 40, w, 64, 32)
    cr.set_source_rgba(0.04, 0.04, 0.06, 0.85)
    cr.fill_preserve()
    cr.set_source_rgba(*hud2d.YELLOW)
    cr.set_line_width(3)
    cr.stroke()
    hud2d._text(cr, text, 30 + w / 2, 84, 30, hud2d.YELLOW, hud2d.ROUND, "center")


def timelock(cr):
    """The masked face at your teller glass, big; the alarm's red glow below: HE KNOWS YOUR NAME."""
    from channels.horror import timelock_2d as ep
    t = 3.0
    cr.save()
    cr.translate(360, 640)
    cr.scale(1.18, 1.18)
    cr.translate(-360, -700)
    ep.lobby(cr, t)                                          # (blurred() assumes a 720 x 1280 device; dim it instead)
    cr.set_source_rgba(0.02, 0.03, 0.04, 0.55)
    cr.paint()
    ep.danny(cr, 360, 980, 1.5, t, mask=1.0, look=(0, 0.1))
    ep.teller_glass(cr, t, fog=0.7)
    cr.restore()
    tk.grade(cr, (0.85, 0.98, 0.98), (0.45, 0.5, 0.55))
    glow(cr, 360, 1300, 520, ep.ALARM_RED, 0.5)
    g = cairo.LinearGradient(0, 120, 0, 460)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.75)
    g.add_color_stop_rgba(1, 0, 0, 0, 0)
    cr.set_source(g)
    cr.paint()
    big_text(cr, [("HE KNOWS", (1, 1, 1, 1)), ("YOUR NAME", hud2d.RED)], 250, 124)
    chip(cr, "TIME LOCK · PART 1")
    badge_text = "BOX 41"
    cr.save()
    cr.translate(560, 1000)
    cr.rotate(-0.12)
    hud2d.stamp(cr, 1.0, 0.0, 9.0, [badge_text], x=0, y=0, rot=0.0)
    cr.restore()


THUMBS = {"tower9_n2": tower9_n2, "timelock": timelock}

if __name__ == "__main__":
    name = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    scale = 1.5                                              # draw at 720 x 1280, save at 1080 x 1920
    s = cairo.ImageSurface(cairo.FORMAT_RGB24, int(W * scale), int(H * scale))
    cr = cairo.Context(s)
    cr.scale(scale, scale)
    THUMBS[name](cr)
    path = os.path.join(OUT, f"{name}.png")
    s.write_to_png(path)
    print("wrote", path)
