"""Demo stills and layout check for channels/monsters/fx2d_ab.py (the A/B vote cards of the S24 split).

    FPS=24 python channels/monsters/test_fx2d_ab.py     # -> out/monsters/tests/fx2d_ab_*.png

Draws the cards over a stand-in split (two colour bands) at the key moments: A popping, A settled + B popping, both
pulsing. The layout check draws each card alone at many moments and fails if a pixel lands right of x 560, in the
caption band (845-930) or under the Shorts UI (y >= 960), or above the top bar (y < 96).
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.environ.setdefault("FPS", "24")

import numpy as np  # noqa: E402

from channels.monsters import fx2d_ab as ab  # noqa: E402
from motion.engine import FPS, H, W, cairo  # noqa: E402

OUT = os.path.join(ROOT, "out", "monsters", "tests")
A_AT, B_AT, BOTH_AT = 0.4, 2.9, 4.6


def frame(t, cards=("A", "B")):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    cr.set_source_rgb(0.36, 0.62, 0.38)
    cr.rectangle(0, 0, W, H / 2)
    cr.fill()
    cr.set_source_rgb(0.30, 0.48, 0.70)
    cr.rectangle(0, H / 2, W, H / 2)
    cr.fill()
    if "A" in cards:
        ab.ab_card(cr, t, A_AT, "A", "SAVE", pulse_at=BOTH_AT)
    if "B" in cards:
        ab.ab_card(cr, t, B_AT, "B", "RUN", pulse_at=BOTH_AT)
    return surf


def alone(t, letter):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    ab.ab_card(cr, t, A_AT if letter == "A" else B_AT, letter, "SAVE" if letter == "A" else "RUN", pulse_at=BOTH_AT)
    a = np.frombuffer(surf.get_data(), np.uint8).reshape(H, surf.get_stride() // 4, 4)[:, :W, 3]
    return a > 8


def layout_check():
    bad = []
    for letter in "AB":
        for f in range(0, int(6 * FPS)):
            m = alone(f / FPS, letter)
            if not m.any():
                continue
            ys, xs = np.nonzero(m)
            if xs.max() >= 560 or ys.min() < 96 or ys.max() >= 960 or (m[845:931].any()):
                bad.append((letter, f, xs.max(), ys.min(), ys.max()))
    return bad


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, t in (("a_pop", A_AT + 0.12), ("a_settled_b_pop", B_AT + 0.12), ("both_pulse", BOTH_AT + 0.05)):
        frame(t).write_to_png(os.path.join(OUT, f"fx2d_ab_{name}.png"))
    bad = layout_check()
    print("layout:", "OK" if not bad else f"{len(bad)} frames out of bounds, first {bad[:3]}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
