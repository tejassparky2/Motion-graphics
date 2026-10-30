"""Demo stills and layout check for channels/monsters/fx2d.py (the 2D anime effects and game HUD).

    FPS=24 python channels/monsters/test_fx2d.py                 # stills -> out/monsters/tests/fx2d_*.png
    FPS=24 python channels/monsters/test_fx2d.py --sheets DIR    # also contact sheets of each animation

Every still is drawn over out/monsters/tests/puffshrimp_anime_wide.png scaled to 720x1280. The layout check draws
each HUD element alone at many moments and fails if any pixel lands in the caption band or the bottom 25%.
"""
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.environ.setdefault("FPS", "24")

import numpy as np  # noqa: E402

from channels.monsters import fx2d as fx  # noqa: E402
from motion.engine import FPS, H, W, cairo  # noqa: E402

OUT = os.path.join(ROOT, "out", "monsters", "tests")
BASE = os.path.join(OUT, "puffshrimp_anime_wide.png")
_base = None


def base():
    global _base
    if _base is None:
        src = cairo.ImageSurface.create_from_png(BASE)
        _base = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        c = cairo.Context(_base)
        c.scale(W / src.get_width(), H / src.get_height())
        c.set_source_surface(src, 0, 0)
        c.get_source().set_filter(cairo.FILTER_GOOD)
        c.paint()
    return _base


def frame(draw, t, bg=True):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    if bg:
        cr.set_source_surface(base(), 0, 0)
        cr.paint()
    draw(cr, t)
    return surf


def caption(cr, text="It's just a shrimp."):
    """A stand-in for hud2d.captions (same font, size, outline and baseline) to show the HUD clears it."""
    fx._text(cr, text, W / 2, 905, 52, fx.WHITE, fx.ROUND, "center", outline=(0.05, 0.03, 0.06, 1), ow=52 * 0.16,
             shadow=0.45)


# ---------------------------------------------------------------- the demo shots
SX, SY = 360, 700                     # the puff-shrimp's middle in the base frame (its feet are at ~790)


def d_impact_a(cr, t):
    fx.impact_frame(cr, t, 0.0, SX, SY)


def d_impact_b(cr, t):
    fx.impact_frame(cr, t + 1 / FPS, 0.0, SX, SY)


def d_speed_radial(cr, t):
    fx.speed_lines(cr, t, 0.0, mode="radial", cx=SX, cy=SY, bg=False)
    caption(cr, "It moved.")


def d_speed_horizontal(cr, t):
    fx.speed_lines(cr, t, 0.0, mode="horizontal", cols=("#7fd3ff", "#3a4bd8"))
    fx.hook_text(cr, t, 0.0, ("ZOOM!",), red=(), y=640, size=120)


def d_effects(cr, t):
    fx.shockwave(cr, t, 0.10, SX, 795, r=330, squash=0.28, sound=False)
    fx.dust_puffs(cr, t, 0.05, SX, 790)
    fx.glow_burst(cr, t, 0.15, 560, 470, 200, fx.MINT)
    fx.sparkles(cr, t, 0.05, 170, 520, n=6, radius=100)
    fx.surprise(cr, t, 0.2, SX, 600)
    caption(cr, "Wait. What?")


def d_hud(cr, t):
    fx.status_bar(cr, t, 0.0, hp=0.8, hits=[(t - 0.3, 0.35)])
    fx.creature_tag(cr, t, 0.0, threat=2, changes=[(t - 0.12, 4)])
    fx.rule_chip(cr, t, t - 0.6)
    caption(cr)


def d_choice(cr, t):
    fx.status_bar(cr, t, 0.0, hp=0.35)
    fx.creature_tag(cr, t, 0.0, threat=4)
    fx.choice_menu(cr, t, t - 0.9, "RUN", "STAY STILL", pick=1, pick_at=t - 0.3, prompt="WHAT DOES KAI DO?")
    caption(cr, "Don't move.")


def d_bond(cr, t):
    fx.status_bar(cr, t, 0.0, hp=1.0)
    fx.bond_popup(cr, t, t - 0.45)
    caption(cr, "It chose him.")


def d_fact(cr, t):
    fx.creature_tag(cr, t, 0.0, "PUFF-SHRIMP", 3)
    fx.fact_card(cr, t, t - 1.0)
    caption(cr, "Hotter than lava.")


def d_boot(cr, t):
    fx.hud_boot(cr, t, t - 1.3)


def d_hook(cr, t):
    fx.hook_text(cr, t, 0.0, ("THE CUTEST ONE", "KILLS FIRST"), red=("KILLS",))


STILLS = [("impact_a", d_impact_a, 0.0), ("impact_b", d_impact_b, 0.0), ("speed_radial", d_speed_radial, 0.4),
          ("speed_horizontal", d_speed_horizontal, 0.4), ("effects", d_effects, 0.42), ("hud", d_hud, 5.0),
          ("choice", d_choice, 5.0), ("bond", d_bond, 5.0), ("fact", d_fact, 5.0), ("boot", d_boot, 5.0),
          ("hook", d_hook, 0.0)]


# ---------------------------------------------------------------- layout check
HUD = {
    "status_bar": lambda cr, t: fx.status_bar(cr, t, 0.0, hp=0.9, hits=[(0.5, 0.15)]),
    "creature_tag": lambda cr, t: fx.creature_tag(cr, t, 0.0, threat=2, changes=[(0.5, 5)]),
    "choice_menu": lambda cr, t: fx.choice_menu(cr, t, 0.0, pick=0, prompt="WHAT DOES KAI DO?"),
    "bond_popup": lambda cr, t: fx.bond_popup(cr, t, 0.0),
    "rule_chip": lambda cr, t: fx.rule_chip(cr, t, 0.0),
    "fact_card": lambda cr, t: fx.fact_card(cr, t, 0.0),
    "hud_boot": lambda cr, t: fx.hud_boot(cr, t, 0.0),
    "hook_text": lambda cr, t: fx.hook_text(cr, t, 0.0, ("THE CUTEST ONE", "KILLS FIRST"), red=("KILLS",)),
}


def layout_check():
    bad = []
    for name, draw in HUD.items():
        lo = hi = None
        for t in np.arange(0, 2.6, 0.1):
            a = np.ndarray((H, W * 4), np.uint8, frame(draw, float(t), bg=False).get_data())[:, 3::4]
            rows = np.nonzero(a.max(axis=1) > 8)[0]
            if len(rows):
                lo = rows[0] if lo is None else min(lo, rows[0])
                hi = rows[-1] if hi is None else max(hi, rows[-1])
        ok = hi is not None and hi < fx.CAPTION_BAND[0] and lo >= 60
        print(f"  {name:13s} y {lo}-{hi}  {'ok' if ok else 'OVERLAP'}")
        if not ok:
            bad.append(name)
    return bad


def sheets(folder, n=8):
    """One contact sheet per demo: n frames across its animation, at a third of full size."""
    os.makedirs(folder, exist_ok=True)
    clips = [("impact", lambda cr, t: fx.impact_frame(cr, t, 0.0, SX, SY), 0.0, 4 / FPS),
             ("effects", d_effects, 0.0, 1.3),
             ("status_hit", lambda cr, t: fx.status_bar(cr, t, 0.0, hp=0.8, hits=[(0.4, 0.15)]), 0.0, 1.6),
             ("threat", lambda cr, t: fx.creature_tag(cr, t, 0.0, threat=2, changes=[(0.4, 5)]), 0.0, 1.4),
             ("choice", lambda cr, t: fx.choice_menu(cr, t, 0.0, pick=1, pick_at=0.6), 0.0, 1.45),
             ("bond", lambda cr, t: fx.bond_popup(cr, t, 0.0), 0.0, 1.9),
             ("rule", lambda cr, t: fx.rule_chip(cr, t, 0.0), 0.0, 0.8),
             ("fact", lambda cr, t: fx.fact_card(cr, t, 0.0), 0.0, 1.0),
             ("boot", lambda cr, t: fx.hud_boot(cr, t, 0.0), 0.0, 2.9),
             ("hook", lambda cr, t: fx.hook_text(cr, t, 0.0, ("THE CUTEST ONE", "KILLS FIRST"), red=("KILLS",)),
              0.0, 0.5)]
    sc = 1 / 3
    for name, draw, t0, t1 in clips:
        sheet = cairo.ImageSurface(cairo.FORMAT_ARGB32, int(W * sc) * n, int(H * sc))
        c = cairo.Context(sheet)
        for i in range(n):
            t = t0 + (t1 - t0) * i / (n - 1)
            c.save()
            c.translate(i * int(W * sc), 0)
            c.scale(sc, sc)
            c.set_source_surface(frame(draw, t), 0, 0)
            c.paint()
            fx._text(c, f"{t:.2f}s", 12, 60, 44, fx.YELLOW, fx.ROUND, outline=fx.INK, ow=8)
            c.restore()
        sheet.write_to_png(os.path.join(folder, f"sheet_{name}.png"))


if __name__ == "__main__":
    for name, draw, t in STILLS:
        t0 = time.time()
        surf = frame(draw, t)
        ms = (time.time() - t0) * 1000
        path = os.path.join(OUT, f"fx2d_{name}.png")
        surf.write_to_png(path)
        print(f"{path}  {ms:.0f} ms  {os.path.getsize(path) / 1e6:.2f} MB")
    print("layout check (HUD above the caption band and the Shorts UI):")
    bad = layout_check()
    if "--sheets" in sys.argv:
        sheets(sys.argv[sys.argv.index("--sheets") + 1])
    sys.exit(1 if bad else 0)
