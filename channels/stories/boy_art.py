"""THE BOY WHO INHERITED ANOTHER BODY: the cast and sets (cel-shaded 2D, the same toon style as the horror channel).

Story bible: channels/stories/boy_who_inherited_bible.md; the approved reconstructed Chapter 1:
channels/stories/boy_who_inherited_ch1.md. Looks are production design (the bible gives none). Laid out from W and H
so the same drawings serve the 9:16 Shorts and the 16:9 long video.
"""
import math

from motion.engine import W, H, cairo, clamp01
from motion.polish import rad, text_width

from channels.horror import hud2d
from channels.horror import toon2d as tk
from channels.horror.toon2d import INK, curve, glow, grade, hexa, mix, noise, poly, toon

V = H > W
U = H / 1280 if not V else 1.0

NEIL = dict(skin=hexa("#d9a582"), hair=hexa("#2a1f1a"), iris=hexa("#5d6a72"), style="neil")
MAYA = dict(skin=hexa("#b9805c"), hair=hexa("#1c1412"), iris=hexa("#5a3a24"), style="maya")
ARTHUR = dict(skin=hexa("#e3c9b8"), hair=hexa("#e9e6e1"), iris=hexa("#6d7f8c"), style="arthur")
NURSE = dict(skin=hexa("#e8bfa0"), hair=hexa("#5a3a22"), iris=hexa("#4a3a2a"), style="bun")
HOODIE = (hexa("#4b5058"), hexa("#30343a"), hexa("#636a74"))
COAT_M = (hexa("#2b3550"), hexa("#1a2135"), hexa("#3c4a6e"))
SCARF = (hexa("#d79b2b"), hexa("#9c6b14"))
GOWN = (hexa("#b9cfe0"), hexa("#8ea8bd"), hexa("#d2e2ee"))
SCRUBS = (hexa("#3a8f9a"), hexa("#246870"), hexa("#55aab4"))
JACKET = (hexa("#2c2c30"), hexa("#18181b"), hexa("#3c3c42"))

FX = {   # eye opening, brow raise, worry (+ inner ends up), mouth, mouth open
    "calm": (1.0, 0.0, 0.0, "line", 0.0), "smile": (0.9, 0.1, 0.15, "smile", 0.0), "grin": (0.8, 0.15, 0.0, "grin", 0.4),
    "focus": (0.75, -0.05, -0.3, "line", 0.0), "worry": (1.05, 0.25, 0.7, "line", 0.1),
    "fear": (1.25, 0.5, 1.0, "o", 0.55), "shock": (1.35, 0.75, 0.4, "o", 0.9), "grief": (0.6, 0.1, 1.0, "frown", 0.0),
    "laugh": (0.55, 0.2, 0.2, "grin", 0.7),
}


def _eye(cr, x, sx, rx, ry, k, look, iris, fear=0.0, old=False):
    cr.save()
    cr.translate(x, 0)
    h = ry * k

    def shape(c):
        c.save()
        c.scale(sx, 1)
        c.new_path()
        c.move_to(-rx, 2)
        c.curve_to(-rx * 0.5, -h, rx * 0.5, -h, rx, -h * 0.1)
        c.curve_to(rx * 0.6, h * 0.8, -rx * 0.5, h * 0.8, -rx, 2)
        c.close_path()
        c.restore()
    shape(cr)
    cr.set_source_rgba(0.97, 0.96, 0.94, 1)
    cr.fill_preserve()
    cr.save()
    cr.clip()
    px, py = look[0] * rx * 0.4, look[1] * ry * 0.3
    ir = rx * 0.6 * (1 - 0.3 * fear)
    cr.set_source_rgba(*iris)
    cr.arc(px, py, ir, 0, 2 * math.pi)
    cr.fill()
    cr.set_source_rgba(0.04, 0.03, 0.03, 1)
    cr.arc(px, py, ir * 0.48, 0, 2 * math.pi)
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.9)
    cr.arc(px + ir * 0.35, py - ir * 0.35, ir * 0.25, 0, 2 * math.pi)
    cr.fill()
    cr.restore()
    shape(cr)
    cr.set_source_rgba(*INK)
    cr.set_line_width(2.6)
    cr.stroke()
    cr.save()                                                  # the upper lid line
    cr.scale(sx, 1)
    cr.new_path()
    cr.move_to(-rx * 1.02, 2)
    cr.curve_to(-rx * 0.5, -h - 2, rx * 0.5, -h - 2, rx * 1.04, -h * 0.1 - 2)
    cr.restore()
    cr.set_line_width(4.5)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.stroke()
    if old:                                                    # heavy lids and bags
        cr.set_source_rgba(*INK[:3], 0.45)
        cr.set_line_width(2)
        cr.save()
        cr.scale(sx, 1)
        cr.new_path()
        cr.move_to(-rx, h * 0.9)
        cr.curve_to(-rx * 0.4, h * 1.5, rx * 0.4, h * 1.5, rx, h * 0.8)
        cr.move_to(-rx * 0.9, -h - 9)
        cr.curve_to(-rx * 0.3, -h - 16, rx * 0.4, -h - 14, rx * 1.05, -h * 0.2 - 8)
        cr.restore()
        cr.stroke()
    cr.restore()


def head(cr, t, spec, fx="calm", look=(0.0, 0.0), light=(-14, -10), rim=None, rim_from=(9, 0), talk=0.0, seed=0.0,
         tears=0.0, sweat=0.0, cannula=False):
    """A head centred at (0, 0), ~190 px wide. spec: NEIL / MAYA / ARTHUR / NURSE."""
    ok, brow, worry, mouth, mo = FX[fx]
    st = spec["style"]
    old = st == "arthur"
    sk = spec["skin"]
    sk_d = mix(sk, hexa("#7a4e3c"), 0.35)
    hair, hair_d = spec["hair"], mix(spec["hair"], (0, 0, 0, 1), 0.4 if not old else 0.2)
    if st == "maya":                                           # big curls behind, to the shoulders, a bumpy outline
        pts = []
        for j in range(25):
            ang = math.pi * (0.95 + 1.1 * j / 24)
            r = 150 + 18 * math.sin(j * 2.3)
            pts.append((r * math.cos(ang) * 0.95, -40 + r * math.sin(ang) * 1.05))
        pts = [(-118, 210), (-150, 120)] + pts + [(150, 120), (118, 210), (60, 236), (-60, 236)]
        toon(cr, lambda c: curve(c, pts), hair, hair_d, light, rim, rim_from)
        cr.set_source_rgba(1, 1, 1, 0.12)
        cr.set_line_width(3)
        for j in range(10):
            cr.new_path()
            cr.arc(-120 + (j % 5) * 60, 40 + (j // 5) * 90, 18, math.pi * 0.9, math.pi * 1.9)
            cr.stroke()
    if st == "bun":
        toon(cr, lambda c: c.arc(0, -150, 34, 0, 2 * math.pi), hair, hair_d, light, rim, rim_from)
    for sx in (-1, 1):
        toon(cr, lambda c, sx=sx: curve(c, [(sx * 86, -22), (sx * 104, -30), (sx * 108, 8), (sx * 88, 26)]), sk, sk_d,
             light, rim, rim_from, lw=3.5)
    face = (lambda c: curve(c, [(-84, -40), (-82, -100), (-48, -136), (0, -146), (48, -136), (82, -100), (84, -40),
                                (78, 30), (58, 74), (0, 102), (-58, 74), (-78, 30)])) if not old else \
        (lambda c: curve(c, [(-82, -40), (-84, -104), (-50, -140), (0, -148), (50, -140), (84, -104), (82, -40),
                             (70, 34), (50, 82), (0, 108), (-50, 82), (-70, 34)]))
    toon(cr, face, sk, sk_d, light, rim, rim_from)
    cr.save()
    cr.new_path()
    face(cr)
    cr.clip()
    if old:                                                    # hollow cheeks, wrinkles, spots
        for sx in (-1, 1):
            cr.set_source(rad(sx * 52, 40, 40, [(0, (0.45, 0.32, 0.3, 0.3)), (1, (0.45, 0.32, 0.3, 0))]))
            cr.paint()
        cr.set_source_rgba(*INK[:3], 0.35)
        cr.set_line_width(2)
        for k in range(3):
            cr.move_to(-40, -96 + k * 10)
            cr.curve_to(-14, -100 + k * 10, 14, -100 + k * 10, 40, -96 + k * 10)
        for sx in (-1, 1):
            cr.move_to(sx * 24, 34)
            cr.curve_to(sx * 40, 54, sx * 44, 70, sx * 38, 86)
        cr.stroke()
        cr.set_source_rgba(0.55, 0.38, 0.28, 0.35)
        for k in range(6):
            cr.arc(-56 + (k * 23) % 110, -60 + (k * 37) % 50, 4 + k % 3, 0, 2 * math.pi)
            cr.fill()
    else:
        for sx in (-1, 1):
            cr.set_source(rad(sx * 48, 30, 26, [(0, (0.95, 0.5, 0.48, 0.18)), (1, (0.95, 0.5, 0.48, 0))]))
            cr.paint()
    cr.restore()
    k = (1 - 0.95 * (math.sin(((t + seed) % 3.9) / 0.13 * math.pi) if (t + seed) % 3.9 < 0.13 else 0)) * ok
    for sx in (-1, 1):
        cr.save()
        cr.translate(0, -4)
        _eye(cr, sx * 36, sx, 21 if not old else 18, 17 if not old else 13, k, look, spec["iris"],
             fear=max(0.0, worry) * (ok > 1.1), old=old)
        cr.restore()
        cr.save()
        cr.translate(sx * 38, -44 - 12 * brow)
        cr.scale(sx, 1)
        cr.rotate(0.3 * worry)
        cr.set_source_rgba(*mix(hair if not old else hexa("#c8c4be"), (0, 0, 0, 1), 0.3))
        cr.set_line_width(6 if not old else 7)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.new_path()
        cr.move_to(-20, 2)
        cr.curve_to(-6, -6, 10, -7, 24, 0)
        cr.stroke()
        cr.restore()
    cr.set_source_rgba(*sk_d[:3], 0.95)                        # nose
    cr.set_line_width(2.6)
    cr.new_path()
    cr.move_to(4, 4)
    cr.curve_to(8, 18, 10, 28, 0, 32)
    cr.stroke()
    if cannula:                                                # the oxygen line under the nose
        cr.set_source_rgba(0.85, 0.92, 0.95, 0.9)
        cr.set_line_width(5)
        cr.move_to(-90, 30)
        cr.curve_to(-40, 44, 40, 44, 90, 30)
        cr.stroke()
    mo = max(mo, 0.45 * talk * (0.5 + 0.5 * math.sin(t * 22)))
    cr.save()
    cr.translate(0, 60 if not old else 66)
    if mouth == "o" or mo > 0.2 and mouth not in ("grin",):
        cr.save()
        cr.scale(1, 0.35 + mo)
        cr.new_path()
        cr.arc(0, 0, 12, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(0.42, 0.13, 0.14, 1)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(2.6)
        cr.stroke()
    elif mouth == "grin":
        cr.new_path()
        cr.move_to(-26, -4)
        cr.curve_to(-12, 14 + 8 * mo, 12, 14 + 8 * mo, 26, -4)
        cr.close_path()
        cr.set_source_rgba(0.97, 0.96, 0.94, 1)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(2.6)
        cr.stroke()
    else:
        cr.set_source_rgba(*INK)
        cr.set_line_width(3)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.new_path()
        if mouth == "smile":
            cr.move_to(-18, -2)
            cr.curve_to(-6, 8, 6, 8, 18, -2)
        elif mouth == "frown":
            cr.move_to(-16, 5)
            cr.curve_to(-5, -4, 5, -4, 16, 5)
        else:
            cr.move_to(-14, 0)
            cr.line_to(14, 0)
        cr.stroke()
    cr.restore()
    if st == "neil":                                           # messy dark hair, a fringe falling right
        toon(cr, lambda c: curve(c, [(-92, -10), (-98, -84), (-60, -140), (0, -156), (62, -142), (98, -92), (94, -6),
                                     (84, -50), (70, -36), (56, -74), (30, -50), (10, -84), (-16, -54), (-38, -80),
                                     (-60, -48), (-80, -66)]), hair, hair_d, light, rim, rim_from)
    elif st == "maya":                                         # curls on top, a side part; the face and ears open
        toon(cr, lambda c: curve(c, [(-90, -40), (-100, -96), (-62, -146), (6, -160), (70, -142), (102, -96),
                                     (94, -44), (84, -70), (60, -96), (24, -104), (-10, -92), (-46, -74),
                                     (-72, -56)]), hair, hair_d, light, rim, rim_from)
        cr.set_source_rgba(1, 1, 1, 0.1)
        cr.set_line_width(3)
        for k in range(6):
            cr.new_path()
            cr.arc(-80 + k * 32, -110 + 8 * (k % 2), 14, math.pi, 2 * math.pi)
            cr.stroke()
    elif st == "arthur":                                       # thin white hair at the sides, the crown bare
        for sx in (-1, 1):
            toon(cr, lambda c, sx=sx: curve(c, [(sx * 84, -20), (sx * 92, -80), (sx * 60, -118), (sx * 74, -86),
                                                (sx * 80, -40)]), hair, hair_d, light, rim, rim_from, lw=3)
        cr.set_source_rgba(1, 1, 1, 0.5)
        cr.set_line_width(2)
        for k in range(5):
            cr.move_to(-30 + k * 14, -140)
            cr.curve_to(-26 + k * 14, -150, -20 + k * 14, -152, -14 + k * 14, -146)
        cr.stroke()
    elif st == "bun":
        toon(cr, lambda c: curve(c, [(-90, -20), (-96, -90), (-56, -140), (0, -150), (56, -140), (96, -90), (90, -20),
                                     (70, -80), (0, -100), (-70, -80)]), hair, hair_d, light, rim, rim_from)
    if tears > 0:
        cr.set_source_rgba(0.75, 0.9, 1, 0.8 * tears)
        for sx in (-1, 1):
            ty = 20 + 44 * ((t * 0.5 + (sx > 0) * 0.5) % 1)
            cr.arc(sx * 36, ty, 5, 0, 2 * math.pi)
            cr.fill()
    if sweat > 0:
        cr.set_source_rgba(0.75, 0.9, 1, 0.85 * sweat)
        cr.save()
        cr.translate(80, -50 + 30 * ((t * 0.4) % 1))
        cr.move_to(0, -12)
        cr.curve_to(8, 0, 8, 9, 0, 10)
        cr.curve_to(-8, 9, -8, 0, 0, -12)
        cr.restore()
        cr.fill()


def bust(cr, x, y, s, t, who, fx="calm", look=(0.0, 0.0), light=(-14, -10), rim=None, rim_from=(9, 0), talk=0.0,
         tears=0.0, sweat=0.0, tremble=0.0, outfit=None, cannula=False):
    """A character from the chest up. who: neil / maya / arthur / nurse. (x, y) = the base of the neck.
    outfit: neil = hoodie (night) or jacket (street); maya = coat and scarf; arthur = hospital gown; nurse = scrubs."""
    spec = {"neil": NEIL, "maya": MAYA, "arthur": ARTHUR, "nurse": NURSE}[who]
    cr.save()
    cr.translate(x + tremble * 2.4 * math.sin(t * 39), y)
    cr.scale(s, s)
    up = -3 * (0.5 + 0.5 * math.sin(t * 2 * math.pi * 0.28))
    sk = spec["skin"]
    sk_d = mix(sk, hexa("#7a4e3c"), 0.35)
    body = lambda c: curve(c, [(-56, -6 + up), (-160, 28 + up), (-196, 130), (-206, 430), (206, 430), (196, 130),
                               (160, 28 + up), (56, -6 + up)])
    if who == "neil":
        top = HOODIE if outfit != "jacket" else JACKET
        toon(cr, body, top[0], top[1], light, rim, rim_from)
        toon(cr, lambda c: poly(c, [(-32, -84), (32, -84), (34, 0), (-34, 0)]), sk, sk_d, (0, 8), None, lw=3.5)
        if outfit == "jacket":
            toon(cr, lambda c: poly(c, [(-44, 0), (44, 0), (20, 160), (-20, 160)]), hexa("#ececec"), hexa("#bdbdbd"),
                 (0, -3), None, lw=3)                          # a white tee under the jacket
        else:
            toon(cr, lambda c: curve(c, [(-110, -2 + up), (-74, -40 + up), (0, -50 + up), (74, -40 + up),
                                         (110, -2 + up), (80, 34 + up), (0, 18 + up), (-80, 34 + up)]), top[2],
                 top[1], light, rim, rim_from)                 # the hood around the neck
    elif who == "maya":
        toon(cr, body, COAT_M[0], COAT_M[1], light, rim, rim_from)
        toon(cr, lambda c: poly(c, [(-30, -84), (30, -84), (32, 0), (-32, 0)]), sk, sk_d, (0, 8), None, lw=3.5)
        toon(cr, lambda c: curve(c, [(-104, 4 + up), (-70, -36 + up), (0, -46 + up), (70, -36 + up), (104, 4 + up),
                                     (60, 60 + up), (40, 200), (6, 200), (10, 60 + up), (-70, 44 + up)]), *SCARF,
             light, rim, rim_from)                             # the mustard scarf
    elif who == "arthur":
        toon(cr, body, GOWN[0], GOWN[1], light, rim, rim_from)
        cr.set_source_rgba(0.35, 0.5, 0.7, 0.35)               # the gown's print
        for k in range(30):
            cr.arc(-180 + (k * 53) % 360, 60 + (k * 37) % 360, 6, 0, 2 * math.pi)
            cr.fill()
        toon(cr, lambda c: poly(c, [(-28, -86), (28, -86), (30, 0), (-30, 0)]), sk, sk_d, (0, 8), None, lw=3.5)
        cr.set_source_rgba(*INK[:3], 0.4)                      # the old neck's cords
        cr.set_line_width(2)
        for sx in (-1, 1):
            cr.move_to(sx * 10, -70)
            cr.line_to(sx * 18, -4)
        cr.stroke()
        toon(cr, lambda c: poly(c, [(-50, -4), (0, 40), (50, -4), (40, 10), (0, 26), (-40, 10)]), GOWN[2], GOWN[1],
             (0, -3), None, lw=3)
    else:   # nurse
        toon(cr, body, SCRUBS[0], SCRUBS[1], light, rim, rim_from)
        toon(cr, lambda c: poly(c, [(-30, -84), (30, -84), (32, 0), (-32, 0)]), sk, sk_d, (0, 8), None, lw=3.5)
        toon(cr, lambda c: poly(c, [(-44, -2), (0, 70), (44, -2)]), sk, sk_d, (0, 6), None, lw=3)
    cr.translate(0, -186)
    cr.rotate(0.01 * noise(t * 0.5, hash(who) % 7))
    head(cr, t, spec, fx, look, light, rim, rim_from, talk, seed=len(who) * 0.7, tears=tears, sweat=sweat,
         cannula=cannula)
    cr.restore()


# ------------------------------------------------------------------ sets
def trading_room(cr, t, flash_walls=0.0, balance=None, crash=0.0):
    """Neil's room at night: three screens (a chart, the order book with buy walls that blink out, the account), a
    desk lamp, a cold mug. balance: the account figure (string) on the right screen."""
    cr.set_source_rgba(*hexa("#14161d"))
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
             hexa("#1c1d22"), None, (0, 0), None, lw=4)
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
    toon(cr, lambda c: c.rectangle(-20, H * (0.72 if V else 0.78), W + 40, H), hexa("#2a2420"), hexa("#1a1612"),
         (0, -4), None)
    lx = W * (0.88 if not V else 0.85)
    glow(cr, lx, H * 0.7, 260, (1, 0.8, 0.5), 0.3)
    toon(cr, lambda c: c.arc(W * 0.14, H * (0.74 if V else 0.8), 28, 0, 2 * math.pi), hexa("#c9c3b8"), None, (0, 0),
         None, lw=3)                                           # the cold mug


def chart(cr, t, x0, y0, w, h, crash=0.0):
    """A price line that spikes, then (crash 0..1) falls through where it was."""
    pts = []
    for k in range(60):
        u = k / 59
        v = 0.6 - 0.15 * u + 0.04 * math.sin(k * 1.3)
        if u > 0.7:
            v -= 0.3 * min(1.0, (u - 0.7) / 0.08)              # the spike
        if u > 0.86 and crash > 0:
            v += 0.5 * crash * min(1.0, (u - 0.86) / 0.1)      # ...and the fall
        pts.append((x0 + 10 + u * (w - 20), y0 + v * h))
    cr.set_source_rgba(0.4, 1, 0.6, 0.9)
    cr.set_line_width(3)
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.stroke()
    if crash > 0:
        cr.set_source_rgba(1, 0.35, 0.3, 0.9)
        cr.set_line_width(3.5)
        cr.move_to(*pts[51])
        for p in pts[52:]:
            cr.line_to(*p)
        cr.stroke()


def order_book(cr, t, x0, y0, w, h, flash=0.0):
    """Bids and asks; two big buy walls just under the price blink in and out (orders that are never filled)."""
    rows = 12
    rh = h / rows
    for r in range(rows):
        ask = r < rows / 2
        size = 0.2 + 0.25 * ((r * 7) % 5) / 5
        wall = (not ask) and r in (7, 9)
        if wall:
            on = 1.0 if (flash > 0 and math.sin(t * 9 + r) > -0.2) or flash == 0 else 0.0
            size = 0.92 * on + 0.05
        col = (1, 0.35, 0.35, 0.5) if ask else (0.35, 1, 0.55, 0.5 + 0.4 * wall)
        cr.set_source_rgba(*col)
        cr.rectangle(x0 + w - size * w, y0 + r * rh + 2, size * w, rh - 4)
        cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.6)
    cr.rectangle(x0, y0 + h / 2 - 1, w, 2)
    cr.fill()


def phone_chat(cr, t, x, y, s, msgs, typing=None):
    """A phone held up: the chat with Maya. msgs = [(text, mine?, k 0..1)]."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    toon(cr, lambda c: tk.tk_rrect(c, -150, -290, 300, 580, 34), hexa("#16171b"), None, (0, 0), None, lw=5)
    cr.set_source_rgba(0.08, 0.09, 0.12, 1)
    tk.tk_rrect(cr, -136, -276, 272, 552, 26)
    cr.fill()
    hud2d._text(cr, "Maya", 0, -236, 30, (1, 1, 1, 0.95), hud2d.ROUND, "center")
    yy = -170
    for txt, mine, k in msgs:
        if k <= 0:
            continue
        n = max(1, int(len(txt) * clamp01(k)))
        w = min(220, text_width(cr, txt, 24, "Liberation Sans") + 30)
        bx = 120 - w if mine else -120
        tk.tk_rrect(cr, bx, yy - 30, w, 46, 18)
        cr.set_source_rgba(*((0.2, 0.5, 1, 1) if mine else (0.25, 0.26, 0.3, 1)))
        cr.fill()
        hud2d._text(cr, txt[:n], bx + 15, yy + 2, 24, (1, 1, 1, 1), "Liberation Sans")
        yy += 66
    if typing:
        tk.tk_rrect(cr, -120, yy - 30, 80, 42, 18)
        cr.set_source_rgba(0.25, 0.26, 0.3, 1)
        cr.fill()
        for j in range(3):
            cr.set_source_rgba(1, 1, 1, 0.4 + 0.6 * (int(t * 4) % 3 == j))
            cr.arc(-96 + j * 16, yy - 9, 4, 0, 2 * math.pi)
            cr.fill()
    cr.restore()


def cafe(cr, t, cups=0.0, dusk=0.0):
    """The café by the station on a cold afternoon: window, menu board, the counter; two hot chocolates."""
    sky = mix(hexa("#c7d3de"), hexa("#e7a77a"), dusk)
    cr.set_source_rgba(*mix(hexa("#e9dcc8"), hexa("#d9a97e"), 0.4 * dusk))
    cr.paint()
    wx0, wx1 = W * 0.05, W * (0.5 if not V else 0.95)
    toon(cr, lambda c: c.rectangle(wx0, H * 0.08, wx1 - wx0, H * 0.32), sky, None, (0, 0), None, lw=5)
    cr.set_source_rgba(0.5, 0.52, 0.56, 0.6)                   # the station roof across the road
    cr.rectangle(wx0, H * 0.26, wx1 - wx0, H * 0.06)
    cr.fill()
    if not V:
        toon(cr, lambda c: tk.tk_rrect(c, W * 0.58, H * 0.1, W * 0.34, H * 0.3, 8), hexa("#2b2a28"), None, (0, 0),
             None, lw=4)
        for k, ln in enumerate(("HOT CHOCOLATE", "COFFEE", "TEA")):
            hud2d._text(cr, ln, W * 0.6, H * 0.17 + k * 40 * U * 1.6, 26, (0.95, 0.92, 0.85, 0.9), "Kalam")
    toon(cr, lambda c: c.rectangle(-20, H * 0.66, W + 40, H), hexa("#7a5034"), hexa("#53351f"), (0, -5), None)
    if cups > 0:
        for j, x in enumerate((W * 0.4, W * 0.6)):
            cr.save()
            cr.translate(x, H * 0.72)
            sc = 1.0 * max(U, 0.8)
            cr.scale(sc, sc)
            toon(cr, lambda c: poly(c, [(-40, -90), (40, -90), (32, 30), (-32, 30)]), hexa("#f4efe6"),
                 hexa("#cfc7b8"), (-3, -3), None, lw=3.5)
            toon(cr, lambda c: tk.tk_rrect(c, -46, -110, 92, 24, 8), hexa("#5a3a24"), None, (0, 0), None, lw=3)
            for k in range(3):                                 # steam
                cr.set_source_rgba(1, 1, 1, 0.35)
                cr.set_line_width(4)
                ph = t * 1.5 + k + j
                cr.move_to(-16 + k * 16, -120)
                cr.curve_to(-30 + k * 16 + 10 * math.sin(ph), -160, k * 16 - 10 * math.sin(ph), -190, -10 + k * 16,
                            -220)
                cr.stroke()
            cr.restore()


def receipt(cr, t, x, y, s):
    """The receipt: TWO HOT CHOCOLATE 9.20, and the time it was printed."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate(-0.05)
    toon(cr, lambda c: poly(c, [(-110, -200), (110, -200), (110, 180), (90, 196), (70, 180), (50, 196), (30, 180),
                                (10, 196), (-10, 180), (-30, 196), (-50, 180), (-70, 196), (-90, 180), (-110, 196)]),
         hexa("#f7f5ef"), hexa("#d9d5ca"), (-3, -3), None)
    ink = (0.2, 0.2, 0.22, 1)
    hud2d._text(cr, "STATION CAFÉ", 0, -150, 26, ink, "Liberation Mono", "center")
    hud2d._text(cr, "2 x HOT CHOCOLATE", -94, -60, 20, ink, "Liberation Mono")
    hud2d._text(cr, "TOTAL       9.20", -94, -10, 22, ink, "Liberation Mono")
    hud2d._text(cr, "DEBIT CARD", -94, 40, 20, ink, "Liberation Mono")
    hud2d._text(cr, "THANK YOU", 0, 120, 22, ink, "Liberation Mono", "center")
    cr.restore()


def street(cr, t, light="green", car=0.0, dusk=0.6, blue=0.0, crowd=0.0):
    """The crossing near the station at dusk: zebra stripes, the pedestrian light, a car coming (car 0..1 = how close)."""
    g = cairo.LinearGradient(0, 0, 0, H * 0.5)
    g.add_color_stop_rgb(0, *mix(hexa("#8fa9c8"), hexa("#2b3550"), dusk)[:3])
    g.add_color_stop_rgb(1, *mix(hexa("#e6c7a6"), hexa("#a0627a"), dusk)[:3])
    cr.set_source(g)
    cr.paint()
    for k in range(7):                                         # buildings
        bx = k * W / 6.5
        bh = H * (0.18 + 0.1 * ((k * 37) % 5) / 5)
        cr.set_source_rgba(*mix(hexa("#3a4256"), hexa("#1c2030"), dusk)[:3], 1)
        cr.rectangle(bx, H * 0.5 - bh, W / 7, bh)
        cr.fill()
        for j in range(6):                                     # lit windows
            if (k * 3 + j) % 3 == 0:
                cr.set_source_rgba(1, 0.85, 0.55, 0.6 * dusk)
                cr.rectangle(bx + 14 + (j % 3) * 26, H * 0.5 - bh + 20 + (j // 3) * 34, 14, 18)
                cr.fill()
    cr.set_source_rgba(0.24, 0.24, 0.27, 1)                    # the road
    cr.rectangle(0, H * 0.5, W, H * 0.5)
    cr.fill()
    for k in range(9):                                         # zebra stripes in perspective
        x = W * 0.5 + (k - 4) * W * 0.11
        cr.set_source_rgba(0.92, 0.92, 0.9, 0.9)
        poly(cr, [(x - W * 0.03, H * 0.62), (x + W * 0.03, H * 0.62), (x * 1.0 + W * 0.05 + (x - W / 2) * 0.6, H),
                  (x - W * 0.05 + (x - W / 2) * 0.6, H)])
        cr.fill()
    px, py = W * (0.85 if not V else 0.8), H * 0.3             # the pedestrian light
    toon(cr, lambda c: c.rectangle(px - 6, py, 12, H * 0.32), hexa("#2c2e33"), None, (0, 0), None, lw=3)
    toon(cr, lambda c: tk.tk_rrect(c, px - 34, py - 90, 68, 120, 10), hexa("#1c1d21"), None, (0, 0), None, lw=4)
    on_col = (0.3, 1, 0.5) if light == "green" else (1, 0.25, 0.2)
    glow(cr, px, py - 30 if light == "green" else py - 62, 70, on_col, 0.6)
    cr.set_source_rgba(*on_col, 1)
    cr.arc(px, py - 30 if light == "green" else py - 62, 18, 0, 2 * math.pi)
    cr.fill()
    if car > 0:                                                # headlights coming, growing
        cx, cy = W * (0.12 + 0.3 * car), H * (0.56 + 0.12 * car)
        r = 20 + 220 * car ** 2
        glow(cr, cx, cy, r * 3, (1, 0.95, 0.8), 0.7 * car)
        for sx in (-1, 1):
            cr.set_source_rgba(1, 0.98, 0.9, 1)
            cr.arc(cx + sx * r * 0.6, cy, r * 0.22, 0, 2 * math.pi)
            cr.fill()
        cr.set_source_rgba(0.08, 0.08, 0.1, 0.9)
        tk.tk_rrect(cr, cx - r, cy - r * 0.55, 2 * r, r * 0.4, r * 0.15)
        cr.fill()
    if blue > 0:                                               # the ambulance's lights
        for j in range(2):
            on = 1.0 if (t * 3 + j) % 2 < 1 else 0.2
            glow(cr, W * (0.42 + 0.08 * j), H * 0.6, 260, (0.3, 0.5, 1), 0.6 * blue * on)
    if crowd > 0:
        for k in range(9):
            x = W * (0.3 + 0.05 * k)
            cr.set_source_rgba(0.05, 0.06, 0.09, crowd)
            cr.arc(x, H * 0.6, 10, 0, 2 * math.pi)
            cr.fill()
            cr.rectangle(x - 10, H * 0.6, 20, 40)
            cr.fill()
    grade(cr, (1.0, 0.92, 0.9), (0.62, 0.55, 0.62))


def hospital(cr, t, window_view=0.0, monitor=1.0):
    """The private room: a pale wall, the heart monitor, the drip stand, the big dark window. window_view 0..1 shows
    the street far below through it: the crossing, blue lights, a crowd, someone kneeling."""
    cr.set_source_rgba(*hexa("#d9dfe2"))
    cr.paint()
    wx0, wy0 = W * (0.52 if not V else 0.1), H * 0.08
    ww, wh = W * (0.44 if not V else 0.8), H * (0.5 if not V else 0.34)
    toon(cr, lambda c: c.rectangle(wx0 - 10, wy0 - 10, ww + 20, wh + 20), hexa("#eef2f4"), hexa("#c7ced2"), (0, -3),
         None, lw=4)
    cr.save()
    cr.rectangle(wx0, wy0, ww, wh)
    cr.clip()
    cr.set_source_rgba(0.05, 0.07, 0.12, 1)
    cr.paint()
    if window_view > 0:                                        # far below: the crossing, 100 m away
        cr.translate(wx0, wy0)
        cr.scale(ww / W, wh / H)
        cr.push_group()
        street(cr, t, light="red", car=0.0, dusk=0.9, blue=1.0, crowd=1.0)
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
    cr.set_source_rgba(1, 1, 1, 0.08)                          # glass sheen
    cr.rectangle(wx0, wy0, ww, wh)
    cr.fill()
    mx, my = W * (0.16 if not V else 0.78), H * (0.3 if not V else 0.5)
    toon(cr, lambda c: tk.tk_rrect(c, mx - 90, my - 70, 180, 130, 12), hexa("#2b2f33"), None, (0, 0), None, lw=4)
    cr.set_source_rgba(0.04, 0.08, 0.06, 1)
    tk.tk_rrect(cr, mx - 78, my - 58, 156, 106, 8)
    cr.fill()
    cr.set_source_rgba(0.35, 1, 0.5, monitor)                  # the trace, slow and tired
    cr.set_line_width(2.5)
    for k in range(40):
        u = k / 39
        ph = (u * 2 + t * 0.6) % 1
        v = -30 if 0.45 < ph < 0.48 else (14 if 0.48 < ph < 0.5 else 0)
        if k == 0:
            cr.move_to(mx - 74 + u * 148, my + v)
        else:
            cr.line_to(mx - 74 + u * 148, my + v)
    cr.stroke()
    hud2d._text(cr, "58", mx + 60, my + 40, 22, (0.35, 1, 0.5, monitor), "Liberation Mono", "right")


def old_hand(cr, t, x, y, s, ring=True, tremble=1.0):
    """An old man's hand, raised: thin spotted skin, swollen knuckles, a heavy gold ring. It trembles."""
    cr.save()
    cr.translate(x + 2.2 * tremble * math.sin(t * 31), y + 1.6 * tremble * math.sin(t * 27))
    cr.scale(s, s)
    sk = ARTHUR["skin"]
    toon(cr, lambda c: curve(c, [(-60, 300), (-50, 110), (50, 104), (70, 300)]), GOWN[0], GOWN[1], (-8, -6), None)
    toon(cr, lambda c: curve(c, [(-60, 120), (-66, 40), (-58, -40), (-40, -110), (-24, -112), (-20, -30), (-6, -130),
                                 (12, -132), (14, -34), (30, -120), (46, -116), (40, -26), (58, -90), (72, -84), (60, 0),
                                 (66, 60), (54, 120)]), sk, mix(sk, hexa("#7a4e3c"), 0.35), (-6, -5), None, lw=4)
    cr.set_source_rgba(0.55, 0.38, 0.28, 0.4)                  # spots
    for k in range(8):
        cr.arc(-40 + (k * 17) % 90, 20 + (k * 29) % 80, 4 + k % 3, 0, 2 * math.pi)
        cr.fill()
    cr.set_source_rgba(*INK[:3], 0.4)
    cr.set_line_width(2)
    for k in range(4):                                         # the knuckle creases, tendons
        cr.move_to(-30 + k * 22, 10)
        cr.line_to(-26 + k * 22, 90)
    cr.stroke()
    if ring:
        toon(cr, lambda c: tk.tk_rrect(c, 2, -60, 24, 16, 6), hexa("#e2b64a"), hexa("#9c7a20"), (-2, -2),
             (1, 1, 0.8, 0.6), (-3, -3), lw=2.5)
    cr.restore()


def wristband(cr, t, x, y, s):
    """The hospital wristband: VANCE, ARTHUR. AGE 82."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate(-0.06)
    toon(cr, lambda c: tk.tk_rrect(c, -250, -50, 500, 100, 20), hexa("#f5f7f8"), hexa("#cfd6da"), (-3, -3), None)
    cr.set_source_rgba(0.85, 0.2, 0.25, 1)
    cr.rectangle(-250, -50, 40, 100)
    cr.fill()
    hud2d._text(cr, "VANCE, ARTHUR", -190, -6, 40, (0.1, 0.1, 0.12, 1), "Liberation Mono")
    hud2d._text(cr, "AGE 82", -190, 34, 30, (0.1, 0.1, 0.12, 1), "Liberation Mono")
    cr.restore()


def law_card(cr, t, k, distance=0.0):
    """The cosmic law, written on the dark: THE NEAREST. THE WEAKEST. with a line measuring out ~100 metres."""
    if k <= 0:
        return
    cr.save()
    cr.push_group()
    cr.set_source_rgba(0.01, 0.01, 0.03, 0.92)
    cr.paint()
    for j in range(80):                                        # stars
        sx, sy = (j * 137.5) % W, (j * 71.3) % H
        cr.set_source_rgba(1, 1, 1, 0.2 + 0.4 * (0.5 + 0.5 * math.sin(t * 1.2 + j)))
        cr.arc(sx, sy, 1.2 + (j % 3) * 0.6, 0, 2 * math.pi)
        cr.fill()
    y = H * 0.62
    x0, x1 = W * 0.12, W * 0.88
    cr.set_source_rgba(0.75, 0.85, 1, 0.9)
    cr.set_line_width(3)
    cr.move_to(x0, y)
    cr.line_to(x0 + (x1 - x0) * distance, y)
    cr.stroke()
    for x, lab, al in ((x0, "NEIL, 17", "left"), (x1, "ARTHUR VANCE, 82", "right")):
        cr.arc(x, y, 8, 0, 2 * math.pi)
        cr.fill()
        hud2d._text(cr, lab, x + (-10 if al == "left" else 10), y + 44, 22 * max(U, 0.85), (0.8, 0.88, 1, 0.9),
                    "Liberation Mono", al)
    hud2d._text(cr, "~100 METRES", W / 2, y - 22, 26 * max(U, 0.85), (0.8, 0.88, 1, distance), "Liberation Mono",
                "center")
    sz = 74 if V else 64
    hud2d._text(cr, "THE NEAREST.", W / 2, H * 0.3, sz, (1, 1, 1, 1), hud2d.ROUND, "center")
    hud2d._text(cr, "THE WEAKEST.", W / 2, H * 0.3 + sz * 1.15, sz, hud2d.RED, hud2d.ROUND, "center")
    cr.pop_group_to_source()
    cr.paint_with_alpha(k)
    cr.restore()


def chapter_card(cr, t, k, roman, title):
    """I. THE MARKET WAS LYING — a quiet title on black."""
    if k <= 0:
        return
    cr.save()
    cr.push_group()
    cr.set_source_rgba(0.02, 0.02, 0.03, 1)
    cr.paint()
    hud2d._text(cr, roman, W / 2, H * 0.44, 40, (0.85, 0.75, 0.5, 1), "Liberation Serif", "center")
    sz = min(64.0, 64 * (W - 80) / text_width(cr, title, 64, "Liberation Serif"))
    hud2d._text(cr, title, W / 2, H * 0.54, sz, (1, 1, 1, 1), "Liberation Serif", "center")
    cr.pop_group_to_source()
    cr.paint_with_alpha(k)
    cr.restore()
