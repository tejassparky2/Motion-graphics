"""THE BOY WHO INHERITED ANOTHER BODY in the anime look: the same drawing API as boy_art, with Neil, Maya, Arthur
and the nurse as painted puppets (assets/anime/boy, made by tools/anime_assets.py from channels/stories/boy_cast.py)
and painted sets. Screens, the receipt, the phone, the wristband, the hand and the cards stay drawn in code
(boy_art); story details the plot depends on (the walk light, the car's headlights, the blue lights, the crowd, the
kneeling figure) are drawn over the paintings. Anything without an asset falls back to boy_art.
"""
import math
import os

from motion.engine import W, H
from channels.stories import anime2d as AN
from channels.stories import boy_art as _v
from channels.stories.boy_art import *  # noqa: F401,F403  (screens, props, cards: unchanged)
from channels.stories.boy_art import (V, U, glow, hexa, toon, tk, poly, hud2d, chart, order_book, SCARF)

ROOT = AN.ROOT
BG = "assets/anime/boy/bg/{}.png"
# neck base (x, y) and head size, in base.png pixels (1024x1536), measured on the chosen paintings
RIG = {"neil": dict(neck=(520, 690), head=581), "maya": dict(neck=(580, 750), head=724),
       "arthur": dict(neck=(510, 800), head=798), "nurse": dict(neck=(610, 790), head=730)}
EXPR = {"calm": "neutral", "focus": "neutral", "neutral": "neutral", "smile": "smile", "grin": "smile",
        "laugh": "laugh", "worry": "fear", "fear": "fear", "shock": "fear", "grief": "grief"}
FALLBACK = {"laugh": ("smile",), "smile": (), "grief": ("fear",)}
_P = {}


def _bg(name):
    return BG.format(name) if os.path.exists(os.path.join(ROOT, BG.format(name))) else None


def ready(who):
    return who in RIG and os.path.exists(os.path.join(ROOT, "assets/anime/boy", who, "base.png"))


def puppet(who):
    if who not in _P:
        r = RIG[who]
        _P[who] = AN.Puppet("boy", who, r["neck"], r["head"], phase=sum(map(ord, who)) * 0.37)
    return _P[who]


def bust(cr, x, y, s, t, who, fx="calm", look=(0.0, 0.0), light=(-14, -10), rim=None, rim_from=(9, 0), talk=0.0,
         tears=0.0, sweat=0.0, tremble=0.0, outfit=None, cannula=False, eyes_closed=False):
    """A character from the chest up; (x, y) = the base of the neck (as in boy_art). One look per character."""
    if not ready(who):
        return _v.bust(cr, x, y, s, t, who, fx, look, light, rim, rim_from, talk, tears, sweat, tremble, outfit,
                       cannula)
    p = puppet(who)
    e = EXPR.get(fx, "neutral")
    if e != "neutral" and not p.has(e):
        e = next((f for f in FALLBACK.get(e, ()) if p.has(f)), "neutral")
    if tremble:
        x += tremble * 2.4 * math.sin(AN.held(t) * 39)
    p.draw(cr, x, y, s, t, e, talk=talk, eyes_closed=eyes_closed)
    if rim:
        glow(cr, x + rim_from[0] * 12 * s, y - 200 * s, 260 * s, rim[:3], 0.12 * (rim[3] if len(rim) > 3 else 1))


def trading_room(cr, t, flash_walls=0.0, balance=None, crash=0.0):
    """Neil's room at night (painted), with the three screens drawn over it: the chart, the order book, the account."""
    if not _bg("room_night"):
        return _v.trading_room(cr, t, flash_walls, balance, crash)
    AN.paint_bg(cr, _bg("room_night"), blur=6)
    cr.set_source_rgba(0.02, 0.03, 0.06, 0.45)
    cr.paint()
    glow(cr, W * 0.5, H * 0.45, max(W, H) * 0.7, (0.35, 0.55, 0.9), 0.25)
    sw = W * (0.3 if not V else 0.42)
    sh = sw * 0.62
    cy = H * (0.36 if V else 0.42)
    xs = [W * 0.5 - sw * 1.05, W * 0.5, W * 0.5 + sw * 1.05] if not V else [W * 0.5 - sw * 0.6, W * 0.5 + sw * 0.6,
                                                                              W * 0.5]
    ys = [cy, cy, cy] if not V else [cy - sh * 0.62, cy - sh * 0.62, cy + sh * 0.6]
    for j, (x, y) in enumerate(zip(xs, ys)):
        toon(cr, lambda c, x=x, y=y: tk.tk_rrect(c, x - sw / 2 - 10, y - sh / 2 - 10, sw + 20, sh + 20, 10),
             hexa("#1c1d22"), None, (0, 0), None, lw=2.5)
        cr.save()
        cr.rectangle(x - sw / 2, y - sh / 2, sw, sh)
        cr.clip()
        cr.set_source_rgba(0.03, 0.05, 0.08, 1)
        cr.paint()
        if j == 0:
            chart(cr, t, x - sw / 2, y - sh / 2, sw, sh, crash)
        elif j == 1:
            order_book(cr, t, x - sw / 2, y - sh / 2, sw, sh, flash_walls)
        else:
            hud2d._text(cr, "ACCOUNT", x - sw / 2 + 16, y - sh / 2 + 34, 20 * max(U, 0.8) * (sw / 300),
                        (0.6, 0.8, 1, 0.7), "Liberation Mono")
            if balance:
                sz = min(40, sw * 0.11)
                glow(cr, x, y, sw * 0.4, (0.3, 1, 0.6), 0.2)
                hud2d._text(cr, balance, x, y + sz * 0.4, sz, (0.45, 1, 0.65, 1), "Liberation Mono", "center")
        cr.restore()
        glow(cr, x, y, sw * 0.7, (0.4, 0.7, 1), 0.12)


def cafe(cr, t, cups=0.0, dusk=0.0):
    """The café by the station (painted); dusk warms the light."""
    if not _bg("cafe"):
        return _v.cafe(cr, t, cups, dusk)
    AN.paint_bg(cr, _bg("cafe"))
    if dusk > 0:
        cr.set_source_rgba(1.0, 0.55, 0.3, 0.18 * dusk)
        cr.paint()


def _street_overlays(cr, t, light, car, blue, crowd):
    px, py = W * (0.85 if not V else 0.8), H * 0.3             # the walk light (the plot turns on it)
    toon(cr, lambda c: c.rectangle(px - 5, py, 10, H * 0.3), hexa("#2c2e33"), None, (0, 0), None, lw=2)
    toon(cr, lambda c: tk.tk_rrect(c, px - 30, py - 84, 60, 110, 9), hexa("#1c1d21"), None, (0, 0), None, lw=2.5)
    on_col = (0.3, 1, 0.5) if light == "green" else (1, 0.25, 0.2)
    glow(cr, px, py - 28 if light == "green" else py - 58, 90, on_col, 0.7)
    cr.set_source_rgba(*on_col, 1)
    cr.arc(px, py - 28 if light == "green" else py - 58, 16, 0, 2 * math.pi)
    cr.fill()
    if car > 0:                                                # headlights coming, growing
        cx, cy = W * (0.12 + 0.3 * car), H * (0.56 + 0.12 * car)
        r = 20 + 220 * car ** 2
        glow(cr, cx, cy, r * 3, (1, 0.95, 0.8), 0.75 * car)
        for sx in (-1, 1):
            glow(cr, cx + sx * r * 0.6, cy, r * 0.9, (1, 0.97, 0.85), 0.9)
            cr.set_source_rgba(1, 0.98, 0.92, 1)
            cr.arc(cx + sx * r * 0.6, cy, r * 0.2, 0, 2 * math.pi)
            cr.fill()
    if blue > 0:                                               # the ambulance's lights
        for j in range(2):
            on = 1.0 if (t * 3 + j) % 2 < 1 else 0.2
            glow(cr, W * (0.42 + 0.08 * j), H * 0.6, 300, (0.3, 0.5, 1), 0.65 * blue * on)
    if crowd > 0:
        for k in range(9):
            x = W * (0.3 + 0.05 * k)
            cr.set_source_rgba(0.04, 0.05, 0.08, 0.9 * crowd)
            cr.arc(x, H * 0.6, 10, 0, 2 * math.pi)
            cr.fill()
            cr.rectangle(x - 10, H * 0.6, 20, 40)
            cr.fill()


def street(cr, t, light="green", car=0.0, dusk=0.6, blue=0.0, crowd=0.0):
    """The crossing near the station at dusk (painted), with the walk light, the car, the blue lights and the crowd."""
    if not _bg("street"):
        return _v.street(cr, t, light, car, dusk, blue, crowd)
    AN.paint_bg(cr, _bg("street"))
    cr.set_source_rgba(0.12, 0.1, 0.25, 0.35 * max(0.0, dusk - 0.5) * 2)   # later: bluer, darker
    cr.paint()
    _street_overlays(cr, t, light, car, blue, crowd)


def hospital(cr, t, window_view=0.0, monitor=1.0):
    """The private room (painted). window_view 0..1 opens the window: the crossing far below, blue lights, a crowd,
    someone kneeling."""
    if not _bg("hospital"):
        return _v.hospital(cr, t, window_view, monitor)
    AN.paint_bg(cr, _bg("hospital"))
    if window_view > 0:
        wx0, wy0 = W * (0.52 if not V else 0.1), H * 0.08
        ww, wh = W * (0.44 if not V else 0.8), H * (0.5 if not V else 0.34)
        cr.save()
        cr.push_group()
        toon(cr, lambda c: c.rectangle(wx0 - 8, wy0 - 8, ww + 16, wh + 16), hexa("#dfe5e8"), hexa("#b9c1c6"), (0, -3),
             None, lw=2.5)
        cr.rectangle(wx0, wy0, ww, wh)
        cr.clip()
        cr.translate(wx0, wy0)
        cr.scale(ww / W, wh / H)
        if _bg("street"):
            AN.paint_bg(cr, _bg("street"))
            cr.set_source_rgba(0.05, 0.06, 0.16, 0.55)
            cr.paint()
        _street_overlays(cr, t, "red", 0.0, 1.0, 1.0)
        cr.set_source_rgba(0.05, 0.06, 0.09, 1)                # a small figure kneeling at the crossing
        cr.arc(W * 0.46, H * 0.66, 14, 0, 2 * math.pi)
        cr.fill()
        poly(cr, [(W * 0.44, H * 0.68), (W * 0.49, H * 0.68), (W * 0.5, H * 0.74), (W * 0.42, H * 0.74)])
        cr.fill()
        cr.set_source_rgba(*SCARF[0][:3], 1)
        cr.rectangle(W * 0.44, H * 0.675, W * 0.045, 6)
        cr.fill()
        cr.pop_group_to_source()
        cr.paint_with_alpha(window_view)
        cr.restore()
