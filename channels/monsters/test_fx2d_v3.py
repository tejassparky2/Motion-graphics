"""Demo stills for helper 7's v3 additions to channels/monsters/fx2d.py: impact_frame_v3 and speed_lines_v3.

    FPS=24 python channels/monsters/test_fx2d_v3.py      # -> out/monsters/tests/fx2d_v3_*.png and fx2d_v3_sheet.png

Drawn over out/monsters/tests/puffshrimp_anime_wide.png (as test_fx2d.py). The sheet shows the four impact frames
in a row, then the three speed-line modes, at half size.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.environ.setdefault("FPS", "24")

from channels.monsters import fx2d as fx  # noqa: E402
from channels.monsters.test_fx2d import SX, SY, frame  # noqa: E402
from motion.engine import FPS, H, W, cairo  # noqa: E402

OUT = os.path.join(ROOT, "out", "monsters", "tests")

DEMOS = [(f"impact_{k}", (lambda k: lambda cr, t: fx.impact_frame_v3(cr, t + k / FPS, 0.0, SX, SY))(k), 0.0)
         for k in range(4)]
DEMOS += [
    ("speed_radial", lambda cr, t: fx.speed_lines_v3(cr, t, 0.0, mode="radial", cx=SX, cy=SY), 0.2),
    ("speed_horizontal", lambda cr, t: fx.speed_lines_v3(cr, t, 0.0, mode="horizontal",
                                                         bg=("#7fd3ff", "#3a4bd8")), 0.2),
    ("speed_vertical", lambda cr, t: fx.speed_lines_v3(cr, t, 0.0, mode="vertical", col=fx.hexa("#fff6c8"),
                                                       bg=("#ffd9f0", "#8a6cff")), 0.2),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    sheet = cairo.ImageSurface(cairo.FORMAT_ARGB32, W // 2 * 4, H // 2 * 2)
    sc = cairo.Context(sheet)
    for i, (name, draw, t) in enumerate(DEMOS):
        surf = frame(draw, t)
        surf.write_to_png(os.path.join(OUT, f"fx2d_v3_{name}.png"))
        sc.save()
        sc.translate((i % 4) * W // 2, (i // 4) * H // 2)
        sc.scale(0.5, 0.5)
        sc.set_source_surface(surf, 0, 0)
        sc.paint()
        sc.restore()
    sheet.write_to_png(os.path.join(OUT, "fx2d_v3_sheet.png"))
    print("wrote", len(DEMOS), "stills + fx2d_v3_sheet.png")


if __name__ == "__main__":
    main()
