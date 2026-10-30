"""Demo stills for channels/monsters/fx2d_anime.py (comic faces, emotion backgrounds, split screen, observer shake).

    FPS=24 python channels/monsters/test_fx2d_anime.py      # -> out/monsters/tests/fx2d_anime_*.png

The faces are drawn over the hero close-up from out/monsters/tests/hero_restyle_sheet.png (its right-hand panel).
"""
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.environ.setdefault("FPS", "24")

from channels.monsters import fx2d, fx2d_anime as fa  # noqa: E402
from motion.engine import FPS, H, W, cairo  # noqa: E402

TESTS = os.path.join(ROOT, "out", "monsters", "tests")
CW, CH = W // 2, H // 2                         # a grid cell (the hero close-up panel is exactly this size)
FACE = dict(x=156, y=241, size=190, tilt=-0.02)  # between the eyes of that panel
_cache = {}


def png(name):
    if name not in _cache:
        _cache[name] = cairo.ImageSurface.create_from_png(os.path.join(TESTS, name))
    return _cache[name]


def hero_close():
    """The hero close-up panel (360x640) cut from the restyle sheet."""
    if "hero" not in _cache:
        s = cairo.ImageSurface(cairo.FORMAT_ARGB32, CW, CH)
        c = cairo.Context(s)
        c.set_source_surface(png("hero_restyle_sheet.png"), -1080, 0)
        c.paint()
        _cache["hero"] = s
    return _cache["hero"]


def full(surf):
    """A surface scaled to fill the 720x1280 frame."""
    out = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(out)
    c.scale(W / surf.get_width(), H / surf.get_height())
    c.set_source_surface(surf, 0, 0)
    c.get_source().set_filter(cairo.FILTER_GOOD)
    c.paint()
    return out


def label(cr, text, x, y, size=26):
    fx2d._text(cr, text, x, y, size, fx2d.WHITE, fx2d.ROUND, outline=fx2d.INK, ow=6)


def face_grid(items):
    """Four faces in a 2x2 grid of hero close-ups: items = [(name, fn, t, kwargs)]."""
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    for k, (name, fn, t, kw) in enumerate(items):
        cr.save()
        cr.translate((k % 2) * CW, (k // 2) * CH)
        cr.rectangle(0, 0, CW, CH)
        cr.clip()
        cr.set_source_surface(hero_close(), 0, 0)
        cr.paint()
        fn(cr, t, 0.0, **{**FACE, **kw})
        label(cr, name, 14, CH - 18)
        cr.restore()
    return surf


def bg(mood, t=0.5):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    fa.emotion_bg(cairo.Context(surf), t, 0.0, 2.0, mood=mood, sound=False)
    return surf


def split_ab():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    fa.split(cr, 0.6, 0.0, 2.0, [full(hero_close()), full(png("puffshrimp_anime_wide.png"))],
             focus=[(312, 520), (360, 690)], sound=False)
    return surf


def split_5():
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    pics = [full(hero_close()), full(png("jellysnail_shock.png")), full(png("puffshrimp_anime_wide.png")),
            full(png("fluffmoth_hover.png")), full(png("pistolshrimp_close.png"))]
    fa.split(cr, 0.6, 0.0, 2.0, pics, focus=[(312, 500), None, (360, 690), None, None], tilt=0.04, sound=False)
    return surf


def shake_sheet():
    """Every frame of one shake (16 frames at 24 fps) as quarter-size thumbnails, with each frame's offset."""
    base = full(hero_close())
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    cr = cairo.Context(surf)
    tw, th = W // 4, H // 4
    for i in range(16):
        t = i / FPS
        fr = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
        c = cairo.Context(fr)
        c.set_source_surface(base, 0, 0)
        c.paint()
        fa.shake(c, t, 0.0)
        dx, dy = fa.shake_offset(t, 0.0)
        cr.save()
        cr.translate((i % 4) * tw, (i // 4) * th)
        cr.scale(0.25, 0.25)
        cr.set_source_surface(fr, 0, 0)
        cr.paint()
        cr.restore()
        label(cr, f"f{i} {dx:+.0f},{dy:+.0f}", (i % 4) * tw + 8, (i // 4) * th + 30, 20)
    return surf


STILLS = {
    "faces_a": lambda: face_grid([("sweat drop", fa.sweat_drop, 0.3, {}), ("dot eyes", fa.dot_eyes, 0.3, {}),
                                  ("tear streams", fa.tear_streams, 0.6, {}),
                                  ("swirl eyes", fa.swirl_eyes, 0.3, {})]),
    "faces_b": lambda: face_grid([("terror eyes", fa.terror_eyes, 0.3, {}),
                                  ("anger mark", fa.anger_mark, 0.3, dict(side=-1)),
                                  ("blush lines", fa.blush_lines, 0.3, {}),
                                  ("sweat bead", fa.sweat_drop, 1.2, dict(bead=True, side=-1))]),
    **{f"bg_{m}": (lambda m=m: bg(m)) for m in fa.MOODS},
    "split_ab": split_ab,
    "split_5": split_5,
    "shake": shake_sheet,
}

if __name__ == "__main__":
    for name, make in STILLS.items():
        t0 = time.time()
        surf = make()
        path = os.path.join(TESTS, f"fx2d_anime_{name}.png")
        surf.write_to_png(path)
        print(f"{path}  {(time.time() - t0) * 1000:.0f} ms  {os.path.getsize(path) / 1e6:.2f} MB")
