"""DEAD MAN'S ALGORITHM in the anime look: the same drawing API as dma_art, with the eight named students as painted
puppets (assets/anime/dma, made by tools/anime_assets.py from channels/stories/dma_cast.py) and painted backgrounds.
Momo, screens, cameras, cards and text stay drawn in code (dma_art). Anything without an asset falls back to dma_art.
"""
import math
import os

from motion.engine import W, H, clamp01
from channels.stories import anime2d as AN
from channels.stories import dma_art as _v
from channels.stories.dma_art import *  # noqa: F401,F403  (UI pieces, Momo, cards: unchanged)
from channels.stories.dma_art import V, glow, noise, hexa, toon, tk, camera_unit, meteor_streak

ROOT = AN.ROOT
BG = "assets/anime/dma/bg/{}.png"
# neck base (x, y) and head height, in base.png pixels (1024x1536), measured on the chosen paintings
RIG = {"ren": dict(neck=(580, 662), head=560), "haruto": dict(neck=(480, 680), head=445),
       "yui": dict(neck=(530, 640), head=570), "aoi": dict(neck=(700, 690), head=638),
       "mio": dict(neck=(530, 860), head=770)}
EXPR = {"calm": "neutral", "focus": "neutral", "neutral": "neutral", "shock": "fear", "fear": "fear", "worry": "fear",
        "sad": "fear", "smile": "smile", "grin": "grin", "smirk": "smirk", "angry": "angry"}
FALLBACK = {"smile": ("grin", "smirk"), "grin": ("smile", "smirk"), "smirk": ("grin", "smile"), "angry": ("fear",)}
_P = {}


def _bg(name):
    return BG.format(name) if os.path.exists(os.path.join(ROOT, BG.format(name))) else None


def puppet(who):
    if who not in _P:
        r = RIG[who]
        _P[who] = AN.Puppet("dma", who, r["neck"], r["head"], phase=sum(map(ord, who)) * 0.37)
    return _P[who]


def ready(who):
    return isinstance(who, str) and who in RIG and os.path.exists(os.path.join(ROOT, "assets/anime/dma", who,
                                                                                    "base.png"))


def student_bust(cr, x, y, s, t, who, expr="calm", look=(0.0, 0.0), light=(-14, -10), rim=None, rim_from=(9, 0),
                 talk=0.0, tilt=0.0, sweat=0.0, tears=0.0, tremble=0.0, eyes_closed=False, alpha=1.0):
    """A student from the chest up; (x, y) = the base of the neck (as in dma_art)."""
    if not ready(who):
        return _v.student_bust(cr, x, y, s, t, who, expr, look, light, rim, rim_from, talk, tilt, sweat, tears,
                               tremble)
    p = puppet(who)
    e = EXPR.get(expr, "neutral")
    if e != "neutral" and not p.has(e):
        e = next((f for f in FALLBACK.get(e, ()) if p.has(f)), "neutral")
    if tremble:
        x += tremble * 2.4 * math.sin(AN.held(t) * 39)
    p.draw(cr, x, y, s, t, e, talk=talk, tilt=tilt, eyes_closed=eyes_closed, alpha=alpha)
    if rim:                                                    # a coloured light from one side (meteor, screen)
        glow(cr, x + rim_from[0] * 12 * s, y - 200 * s, 260 * s, rim[:3], 0.12 * (rim[3] if len(rim) > 3 else 1))


def classroom(cr, t, meteor=0.0, clock=(12, 16, 0)):
    """Class 3-B: the painted classroom; the meteor grows in the windows on the left and turns the light orange."""
    if not _bg("classroom"):
        return _v.classroom(cr, t, meteor, clock)
    AN.paint_bg(cr, _bg("classroom"), ax=0.4)
    if meteor > 0:
        cr.save()
        cr.rectangle(0, 0, W * 0.42, H * 0.55)
        cr.clip()
        meteor_streak(cr, t, W * 0.2, H * 0.22, meteor)
        cr.restore()
        cr.set_source_rgba(1.0, 0.55, 0.2, 0.28 * meteor)
        cr.paint()
        glow(cr, W * 0.2, H * 0.22, 900, (1, 0.6, 0.2), 0.45 * meteor)


def chamber(cr, t, flicker=True, screen=None, dark=0.0):
    """The underground hall (painted), the wall screen and the cameras drawn over it."""
    if not _bg("chamber"):
        return _v.chamber(cr, t, flicker, screen, dark)
    AN.paint_bg(cr, _bg("chamber"))
    if flicker and noise(t * 9, 4) > 0.55:
        cr.set_source_rgba(0, 0, 0.02, 0.3)
        cr.paint()
    if screen is not None:                                     # the wall screen
        sw, sh = (W * 0.8, H * 0.24) if V else (W * 0.56, H * 0.36)
        sx0, sy0 = (W - sw) / 2, H * (0.16 if V else 0.13)
        toon(cr, lambda c: tk.tk_rrect(c, sx0 - 14, sy0 - 14, sw + 28, sh + 28, 10), hexa("#1d1f22"), None, (0, 0),
             None, lw=3)
        cr.save()
        cr.rectangle(sx0, sy0, sw, sh)
        cr.clip()
        cr.set_source_rgba(0.02, 0.04, 0.05, 1)
        cr.paint()
        screen(cr, sx0, sy0, sw, sh)
        for yy in range(int(sy0), int(sy0 + sh), 4):           # scan lines
            cr.set_source_rgba(0, 0, 0, 0.18)
            cr.rectangle(sx0, yy, sw, 1.5)
            cr.fill()
        cr.restore()
        glow(cr, W / 2, sy0 + sh / 2, sw * 0.8, (0.4, 0.9, 1), 0.22)
    for cx, cy, sx in ((W * 0.06, H * 0.12, 1), (W * 0.94, H * 0.12, -1)):
        camera_unit(cr, t, cx, cy, sx, 0.8)
    if dark > 0:
        cr.set_source_rgba(0, 0, 0, dark)
        cr.paint()


LYING = (("ren", 0.5, 0.52, 1.55, 0.0), ("yui", 0.2, 0.3, -1.4, 0.0), ("haruto", 0.8, 0.28, 1.3, 0.3),
         ("kota", 0.18, 0.75, 1.8, 0.0), ("go", 0.82, 0.74, -1.7, 0.6), ("aoi", 0.5, 0.12, 1.1, 0.0),
         ("mio", 0.45, 0.9, -1.2, 0.0), ("riku", 0.9, 0.5, -1.9, 0.0))


def lying_students(cr, t, stir=0.0):
    """From above: the class on the concrete floor, eyes shut; a few start to move (stir)."""
    if not (_bg("floor") and all(ready(w) for w, *_ in LYING)):
        return _v.lying_students(cr, t, stir)
    AN.paint_bg(cr, _bg("floor"))
    for who, u, v, ang, wake in LYING:
        cr.save()
        cr.translate(W * u, H * v)
        cr.rotate(ang + 0.05 * stir * wake * math.sin(AN.held(t) * 3))
        student_bust(cr, 0, 120, 0.62, t, who, "calm", eyes_closed=not (stir and wake))
        cr.restore()
    cr.set_source_rgba(0.05, 0.07, 0.12, 0.35)                # the cold light from above
    cr.paint()


def eye_closeup(cr, t, k, who="ren"):
    """Extreme close-up of a painted eye (the eyes box of the cast spec), slowly pushing in."""
    from channels.stories import dma_cast
    ex0, ey0, ex1, ey1 = dma_cast.CHARS[who]["eyes"]
    cx, cy = (ex0 + ex1 * 1.0) / 2 - (ex1 - ex0) * 0.22, (ey0 + ey1) / 2   # the eye on the viewer's left
    base = AN.image(os.path.join("assets/anime/dma", who, "base.png"))
    z = W / ((ex1 - ex0) * 2 * 0.62) * (1 + 0.12 * k)
    cr.save()
    cr.set_source_rgba(0, 0, 0, 1)
    cr.paint()
    cr.translate(W / 2, H / 2)
    cr.scale(z, z)
    cr.translate(-cx * 2, -cy * 2)
    cr.set_source_surface(base, 0, 0)
    cr.get_source().set_filter(AN.cairo.FILTER_GOOD)
    cr.paint()
    cr.restore()
