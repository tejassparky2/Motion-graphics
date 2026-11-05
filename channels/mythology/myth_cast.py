"""The mythology channel's code-drawn cast (6 Nov 2026), built on the chibi kit in motion/toons.py (its head, limbs and
hands) with Indian royal and divine costume: crowns (kirita, mukut, tiara), kundala earrings, layered gold necklaces,
armlets and bangles, the sacred thread, dhoti with a gold border, an angavastram that sways, saree with pallu,
tilak and bindi, a halo (prabhamandala) for deities, and props (plough, veena, lotus, Vedas, kamandalu, rosary,
hourglass). Everything is a pure function of t.

  figure(cr, t, x, y, s, who, ...)   a standing character, feet at (x, y)
  brahma(cr, t, x, y, s, ...)        Brahma seated on a lotus: three visible heads, four arms, white beard
Units match toons' adult build: about 560 units tall at s=1.
"""
import math

from motion.engine import hexc
from motion.polish import OUTLINE, WHITE, alpha, ellipse, ground_shadow, lin, paint, rad, shade, smooth, soft_disc, \
    stroke_line
from motion.toons import ARMS, BUILDS, _hand, _limb, head

GOLD = hexc("#e8b23a")
GOLD_D = hexc("#a8741c")
RUBY = hexc("#c8203a")
EMERALD = hexc("#1f8a5a")
PEARL = hexc("#fbf3e4")

LOOKS = {
    "kakudmi": dict(skin=hexc("#d39a6e"), hair="short", hair_col=hexc("#1e130d"), stache=hexc("#1e130d"),
                    crown="mukut", dhoti=hexc("#f4e2bc"), border=GOLD, cloth=hexc("#9c2a2a"), torso="bare",
                    tilak="king", build="adult"),
    "revati": dict(skin=hexc("#e2a87e"), hair="bun", hair_col=hexc("#1e130d"), crown="tiara", saree=hexc("#1f7a6e"),
                   blouse=hexc("#e8a33a"), cloth=hexc("#d9577a"), border=GOLD, tilak="bindi", build="adult",
                   female=True),
    "balarama": dict(skin=hexc("#f6dcc0"), hair="short", hair_col=hexc("#1e130d"), crown="kirita",
                     dhoti=hexc("#2f5fb3"), border=GOLD, cloth=hexc("#1f3f86"), torso="bare", tilak="vaishnava",
                     build="adult", halo=True),
    "gandharva1": dict(skin=hexc("#efc3a0"), hair="short", hair_col=hexc("#2b1a12"), crown="mukut",
                       dhoti=hexc("#3f9b6e"), border=GOLD, cloth=hexc("#8a4fc9"), torso="bare", tilak="dot",
                       build="adult"),
    "gandharva2": dict(skin=hexc("#d8a07a"), hair="short", hair_col=hexc("#2b1a12"), crown="mukut",
                       dhoti=hexc("#c9542e"), border=GOLD, cloth=hexc("#2fa59a"), torso="bare", tilak="dot",
                       build="adult"),
    "suitor": dict(skin=hexc("#c98d62"), hair="short", hair_col=hexc("#1e130d"), stache=hexc("#1e130d"),
                   crown="turban", turban=hexc("#d8763a"), dhoti=hexc("#f1e6d0"), border=hexc("#c94a3a"),
                   cloth=hexc("#4f7fc9"), torso="bare", build="adult"),
    "villager": dict(skin=hexc("#b97c52"), hair="short", hair_col=hexc("#1e130d"), dhoti=hexc("#efe3c8"),
                     border=hexc("#8a5a2b"), cloth=hexc("#c9a46a"), torso="bare", build="kid"),
}


# ---------------------------------------------------------------- small helpers
def _jewel(cr, x, y, r, col=RUBY):
    cr.arc(x, y, r, 0, 2 * math.pi)
    paint(cr, rad(x - r * 0.3, y - r * 0.3, r * 1.4, [(0, shade(col, 0.5)), (1, shade(col, -0.2))]), OUTLINE, 2.5)
    cr.arc(x - r * 0.3, y - r * 0.35, r * 0.28, 0, 2 * math.pi)
    paint(cr, alpha(WHITE, 0.8), None, 0)


def _gold(cr, path, lw=3.5):
    """Fill the current path in gold with a top-left highlight."""
    paint(cr, lin(0, -40, 0, 40, [(0, shade(GOLD, 0.35)), (0.5, GOLD), (1, GOLD_D)]), OUTLINE, lw)


def halo(cr, t, x, y, r, alpha_=1.0, rays=True):
    """Prabhamandala: a soft glow, a gold ring with petals and slowly turning rays."""
    if alpha_ <= 0:
        return
    soft_disc(cr, x, y, r * 1.5, alpha(hexc("#ffe6a0"), 0.35 * alpha_))
    if rays:
        cr.save()
        cr.translate(x, y)
        cr.rotate(t * 0.08)
        for k in range(24):
            a = k * math.pi / 12
            cr.move_to(math.cos(a - 0.04) * r * 0.7, math.sin(a - 0.04) * r * 0.7)
            cr.line_to(math.cos(a) * r * 1.35, math.sin(a) * r * 1.35)
            cr.line_to(math.cos(a + 0.04) * r * 0.7, math.sin(a + 0.04) * r * 0.7)
            cr.close_path()
        cr.set_source_rgba(1, 0.86, 0.45, 0.22 * alpha_)
        cr.fill()
        cr.restore()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(1, 0.93, 0.7, 0.35 * alpha_)
    cr.fill()
    for k in range(16):                                  # petal rim
        a = k * math.pi / 8 + t * 0.05
        ellipse(cr, x + math.cos(a) * r, y + math.sin(a) * r, r * 0.13, r * 0.07, a)
        paint(cr, alpha(GOLD, alpha_), alpha(OUTLINE, 0.6 * alpha_), 2)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*GOLD_D[:3], 0.9 * alpha_)
    cr.set_line_width(6)
    cr.stroke()


# ---------------------------------------------------------------- headwear (head centre at 0,0, radius r)
def crown(cr, r, kind, look=None, t=0.0):
    if kind == "kirita":                                  # tall tiered crown of Vishnu forms and gods
        base = -0.55 * r
        pts = [(-0.78 * r, base + 0.12 * r), (-0.62 * r, -1.05 * r), (-0.32 * r, -1.55 * r), (0, -1.95 * r),
               (0.32 * r, -1.55 * r), (0.62 * r, -1.05 * r), (0.78 * r, base + 0.12 * r)]
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
        cr.close_path()
        _gold(cr, None, 4.5)
        for k, yy in enumerate((-0.75, -1.1, -1.42)):      # tiers
            w = 0.7 - 0.17 * k
            stroke_line(cr, [(-w * r, yy * r), (w * r, yy * r)], 4, GOLD_D, curve=False)
            for j in range(-2 + k, 3 - k):
                _jewel(cr, j * 0.22 * r, yy * r - 0.1 * r, 0.06 * r, RUBY if j % 2 else EMERALD)
        _jewel(cr, 0, -1.8 * r, 0.1 * r, RUBY)            # finial
        ellipse(cr, 0, base + 0.05 * r, 0.86 * r, 0.16 * r)  # band
        _gold(cr, None, 4)
        for j in range(-3, 4):
            _jewel(cr, j * 0.24 * r, base + 0.05 * r, 0.055 * r, PEARL)
    elif kind == "mukut":                                 # a king's crown: band with five points, the middle tall
        base = -0.6 * r
        cr.move_to(-0.8 * r, base + 0.1 * r)
        for k, (px, py) in enumerate(((-0.72, -1.0), (-0.48, -0.86), (-0.3, -1.12), (-0.14, -0.9), (0, -1.45),
                                     (0.14, -0.9), (0.3, -1.12), (0.48, -0.86), (0.72, -1.0))):
            cr.line_to(px * r, py * r)
        cr.line_to(0.8 * r, base + 0.1 * r)
        cr.close_path()
        _gold(cr, None, 4.5)
        _jewel(cr, 0, -1.08 * r, 0.11 * r, RUBY)
        for px, py in ((-0.72, -0.98), (-0.3, -1.08), (0.3, -1.08), (0.72, -0.98)):
            cr.arc(px * r, py * r, 0.05 * r, 0, 2 * math.pi)
            paint(cr, PEARL, OUTLINE, 2)
        ellipse(cr, 0, base + 0.04 * r, 0.86 * r, 0.15 * r)
        _gold(cr, None, 4)
        for j in range(-3, 4):
            _jewel(cr, j * 0.24 * r, base + 0.04 * r, 0.05 * r, EMERALD if j % 2 else RUBY)
    elif kind == "tiara":                                 # a princess's head ornament with a maang tikka
        cr.arc(0, 0.1 * r, 0.95 * r, math.pi * 1.18, math.pi * 1.82)
        cr.set_source_rgba(*GOLD)
        cr.set_line_width(0.07 * r)
        cr.stroke()
        stroke_line(cr, [(0, -0.86 * r), (0, -0.55 * r)], 3, GOLD, curve=False)
        _jewel(cr, 0, -0.5 * r, 0.075 * r, RUBY)
        for k in range(5):
            a = math.pi * (1.25 + 0.125 * k)
            _jewel(cr, math.cos(a) * 0.95 * r, 0.1 * r + math.sin(a) * 0.95 * r, 0.05 * r, PEARL)
    elif kind == "turban":
        col = (look or {}).get("turban", hexc("#d8763a"))
        smooth(cr, [(-0.95 * r, -0.2 * r), (-0.9 * r, -0.85 * r), (-0.3 * r, -1.25 * r), (0.4 * r, -1.2 * r),
                    (0.95 * r, -0.8 * r), (0.95 * r, -0.2 * r), (0, -0.45 * r)])
        paint(cr, lin(0, -1.2 * r, 0, -0.2 * r, [(0, shade(col, 0.3)), (1, shade(col, -0.2))]), OUTLINE, 4.5)
        for k in range(3):
            stroke_line(cr, [(-0.85 * r, (-0.4 - 0.25 * k) * r), (0.1 * r, (-0.75 - 0.2 * k) * r),
                             (0.9 * r, (-0.45 - 0.2 * k) * r)], 3, alpha(OUTLINE, 0.35))
        _jewel(cr, 0.05 * r, -0.62 * r, 0.08 * r, EMERALD)


def face_marks(cr, r, look, turn=0.0):
    fx = turn * 0.22 * r
    kind = look.get("tilak")
    if kind == "vaishnava":                               # the U-shaped namam with a red centre line
        stroke_line(cr, [(fx - 0.1 * r, -0.5 * r), (fx - 0.08 * r, -0.3 * r), (fx, -0.24 * r),
                         (fx + 0.08 * r, -0.3 * r), (fx + 0.1 * r, -0.5 * r)], 0.045 * r, WHITE)
        stroke_line(cr, [(fx, -0.52 * r), (fx, -0.3 * r)], 0.04 * r, RUBY, curve=False)
    elif kind == "king":
        stroke_line(cr, [(fx, -0.52 * r), (fx, -0.3 * r)], 0.05 * r, RUBY, curve=False)
    elif kind in ("bindi", "dot"):
        cr.arc(fx, -0.33 * r, 0.05 * r, 0, 2 * math.pi)
        paint(cr, RUBY, None, 0)
    for side in (-1, 1):                                  # kundala earrings
        ex, ey = side * 0.98 * r, 0.32 * r
        stroke_line(cr, [(ex, 0.12 * r), (ex, ey - 0.08 * r)], 2.5, GOLD_D, curve=False)
        cr.arc(ex, ey, 0.11 * r, 0, 2 * math.pi)
        paint(cr, rad(ex - 0.03 * r, ey - 0.04 * r, 0.14 * r, [(0, shade(GOLD, 0.4)), (1, GOLD_D)]), OUTLINE, 2.5)
        _jewel(cr, ex, ey, 0.04 * r, RUBY)


def fancy_head(cr, t, x, y, r, look, eyes="open", mouth="smile", lookdir=(0.0, 0.0), brows=None, turn=0.0,
               beard=None, blink=0.0):
    """A toons head with the costume's crown, tilak and earrings."""
    kw = dict(skin=look["skin"], hair=look.get("hair", "short"), hair_col=look.get("hair_col", OUTLINE))
    if look.get("stache") is not None:
        kw["stache"] = look["stache"]
    if beard is not None or look.get("beard") is not None:
        kw["beard"] = beard if beard is not None else look["beard"]
    if look.get("brows_col") is not None:
        kw["brows_col"] = look["brows_col"]
    e = "closed" if blink > 0.5 and eyes == "open" else eyes
    cr.save()
    cr.translate(x, y)
    if look.get("crown") in ("kirita", "mukut") and look.get("hair") != "bald":   # long hair behind the shoulders
        for side in (-1, 1):
            smooth(cr, [(side * 0.55 * r, -0.5 * r), (side * 1.08 * r, -0.1 * r), (side * 1.12 * r, 0.9 * r),
                        (side * 0.8 * r, 1.05 * r), (side * 0.7 * r, 0.2 * r)])
            paint(cr, look.get("hair_col", OUTLINE), OUTLINE, 3)
    cr.restore()
    head(cr, t, x, y, r, "kid", e, mouth, lookdir, brows, turn, 0.0, True, False, **kw)
    cr.save()
    cr.translate(x, y)
    face_marks(cr, r, look, turn)
    if look.get("crown"):
        crown(cr, r, look["crown"], look, t)
    cr.restore()


def blink_at(t, seed=0, period=3.7):
    ph = (t + seed * 0.913) % period
    return 1.0 if ph < 0.12 else 0.0


# ---------------------------------------------------------------- props: hold(cr, hx, hy) in local units
def plough(cr, hx, hy):
    """Balarama's hala resting on the shoulder: a long wooden shaft and a curved iron share at the top."""
    a, b = (hx - 70, hy + 90), (hx + 150, hy - 330)
    stroke_line(cr, [a, b], 22, OUTLINE, curve=False)
    stroke_line(cr, [a, b], 15, hexc("#9a6a3a"), curve=False)
    bx, by = b
    smooth(cr, [(bx - 10, by + 10), (bx + 40, by - 40), (bx + 95, by - 20), (bx + 110, by + 30), (bx + 70, by + 10),
                (bx + 30, by + 30)])
    paint(cr, lin(bx, by - 40, bx, by + 30, [(0, hexc("#d9dde6")), (1, hexc("#7c8494"))]), OUTLINE, 4)
    for k in range(3):
        stroke_line(cr, [(a[0] + (b[0] - a[0]) * (0.3 + 0.12 * k) - 12, a[1] + (b[1] - a[1]) * (0.3 + 0.12 * k)),
                         (a[0] + (b[0] - a[0]) * (0.3 + 0.12 * k) + 12, a[1] + (b[1] - a[1]) * (0.3 + 0.12 * k))], 5,
                    GOLD, curve=False)


def veena(cr, hx, hy):
    a, b = (hx - 170, hy + 40), (hx + 150, hy - 90)
    for (gx, gy), gr in ((a, 46), (b, 34)):
        cr.arc(gx, gy, gr, 0, 2 * math.pi)
        paint(cr, rad(gx - gr * 0.3, gy - gr * 0.3, gr * 1.3, [(0, hexc("#e8a85a")), (1, hexc("#8a4a1e"))]),
              OUTLINE, 4)
    stroke_line(cr, [a, b], 18, OUTLINE, curve=False)
    stroke_line(cr, [a, b], 12, hexc("#7a3e1c"), curve=False)
    for k in range(4):
        stroke_line(cr, [(a[0], a[1] - 4 + k * 3), (b[0], b[1] - 4 + k * 3)], 1.2, alpha(PEARL, 0.8), curve=False)


def lotus_flower(cr, hx, hy, r=40):
    for k in range(7):
        a = -math.pi / 2 + (k - 3) * 0.38
        ellipse(cr, hx + math.cos(a) * r * 0.55, hy + math.sin(a) * r * 0.55, r * 0.55, r * 0.22, a)
        paint(cr, rad(hx, hy, r, [(0, hexc("#fff0f4")), (1, hexc("#e9729a"))]), OUTLINE, 2.5)
    cr.arc(hx, hy, r * 0.18, 0, 2 * math.pi)
    paint(cr, GOLD, OUTLINE, 2)


def vedas(cr, hx, hy):
    for k in range(3):
        ellipse(cr, hx, hy - 10 - k * 14, 70, 14)
        paint(cr, lin(0, hy - 30, 0, hy, [(0, hexc("#f5e2b0")), (1, hexc("#c9a46a"))]), OUTLINE, 3)
    stroke_line(cr, [(hx - 10, hy - 50), (hx - 10, hy + 6)], 4, RUBY, curve=False)


def kamandalu(cr, hx, hy):
    ellipse(cr, hx, hy + 30, 42, 38)
    paint(cr, rad(hx - 12, hy + 18, 50, [(0, hexc("#f0c070")), (1, hexc("#9a6420"))]), OUTLINE, 4)
    stroke_line(cr, [(hx + 34, hy + 22), (hx + 70, hy - 4)], 9, OUTLINE, curve=False)
    stroke_line(cr, [(hx + 34, hy + 22), (hx + 70, hy - 4)], 5, hexc("#c08a3a"), curve=False)
    cr.arc(hx, hy - 6, 22, math.pi, 2 * math.pi)
    cr.set_source_rgba(*OUTLINE)
    cr.set_line_width(5)
    cr.stroke()


def rosary(cr, hx, hy):
    for k in range(13):
        a = math.pi * (0.1 + 0.8 * k / 12)
        cr.arc(hx + math.cos(a) * 34, hy + 10 + math.sin(a) * 46, 6, 0, 2 * math.pi)
        paint(cr, hexc("#8a3a22"), OUTLINE, 1.5)


def hourglass(cr, hx, hy, sand=0.5, t=0.0):
    w, h = 46, 70
    cr.save()
    cr.translate(hx, hy - 20)
    for yy in (-h, h):
        ellipse(cr, 0, yy, w + 10, 9)
        paint(cr, hexc("#8a5a2b"), OUTLINE, 3)
    for side in (-1, 1):
        stroke_line(cr, [(side * (w + 4), -h), (side * (w + 4), h)], 6, hexc("#8a5a2b"), curve=False)
    def bulb(c):
        c.move_to(-w, -h + 8)
        c.curve_to(-w, -10, -6, -6, -6, 0)
        c.curve_to(-6, 6, -w, 10, -w, h - 8)
        c.line_to(w, h - 8)
        c.curve_to(w, 10, 6, 6, 6, 0)
        c.curve_to(6, -6, w, -10, w, -h + 8)
        c.close_path()
    bulb(cr)
    paint(cr, alpha(hexc("#dff3ff"), 0.45), OUTLINE, 3.5)
    cr.save()
    bulb(cr)
    cr.clip()
    top = -8 - (h - 16) * (1 - sand)
    cr.rectangle(-w, top, 2 * w, -8 - top + 1)
    cr.set_source_rgba(*hexc("#f0c060")[:3], 1)
    cr.fill()
    cr.rectangle(-w, h - 8 - (h - 16) * sand, 2 * w, (h - 16) * sand)
    cr.fill()
    if 0 < sand < 1:
        cr.rectangle(-2, -2, 4, h)
        cr.fill()
    cr.restore()
    cr.restore()


# ---------------------------------------------------------------- the standing figure
def _arm(cr, side, pose, shoulder_y, sw, aw, skin, hold=None, bare=True, sleeve=None):
    hxy = ARMS.get(pose, ARMS["down"]) if isinstance(pose, str) else pose
    sx = side * (sw - 8)
    ex, ey = sx + side * hxy[0], shoulder_y + hxy[1]
    mx, my = (sx + ex) / 2 + side * 16, (shoulder_y + ey) / 2 + 12
    _limb(cr, [(sx, shoulder_y), (mx, my), (ex, ey)], aw, skin if bare else sleeve)
    if bare:                                               # armlet on the upper arm, bangles at the wrist
        ax, ay = sx + (mx - sx) * 0.45, shoulder_y + (my - shoulder_y) * 0.45
        ellipse(cr, ax, ay, aw * 0.62, aw * 0.3, math.atan2(my - shoulder_y, mx - sx) + math.pi / 2)
        _gold(cr, None, 3)
        _jewel(cr, ax, ay, aw * 0.16, RUBY)
    wx, wy = ex + (mx - ex) * 0.18, ey + (my - ey) * 0.18
    ellipse(cr, wx, wy, aw * 0.55, aw * 0.26, math.atan2(ey - my, ex - mx) + math.pi / 2)
    _gold(cr, None, 3)
    _hand(cr, ex, ey, 19, skin)
    if hold:
        hold(cr, ex, ey)
    return ex, ey


def figure(cr, t, x, y, s=1.0, who="kakudmi", facing=1, eyes="open", mouth="smile", lookdir=(0.0, 0.0), brows=None,
           arms=("down", "down"), hold=None, hold_back=None, turn=0.0, bob=True, shadow=True, halo_a=None, seed=0,
           tilt=0.0, alpha_=1.0, **over):
    """A standing royal or divine character, feet at (x, y)."""
    look = dict(LOOKS[who])
    look.update(over)
    b = BUILDS[look.get("build", "adult")]
    hr, hy, sy, py, sw, pw, lw, aw = (b[k] for k in ("hr", "hy", "sy", "py", "sw", "pw", "lw", "aw"))
    skin = look["skin"]
    breathe = math.sin(t * 2.0 + seed * 1.3) if bob else 0.0
    sway = math.sin(t * 1.7 + seed) * 0.6 + math.sin(t * 2.9 + seed * 2) * 0.4
    if alpha_ < 1:
        cr.push_group()
    if shadow:
        ground_shadow(cr, x, y + 4 * s, (sw + 40) * s, 0.28)
    ha = look.get("halo") if halo_a is None else halo_a
    if ha:
        halo(cr, t, x, y + (hy - 10) * s, hr * 1.55 * s, float(ha))
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    cr.scale(s * facing, s)
    shoulder_y = sy + 26 + breathe * 1.5
    female = look.get("female")
    if female and look.get("hair") == "bun":                # a long braid hanging down the back, behind everything
        bx0, by0 = hr * 0.35, hy + hr * 0.4
        pts = [(bx0, by0), (bx0 + 14, by0 + hr * 1.4), (bx0 + 6 + sway * 8, by0 + hr * 2.8)]
        stroke_line(cr, pts, 30, OUTLINE)
        stroke_line(cr, pts, 22, look["hair_col"])
        for k in range(5):
            yy = by0 + hr * (0.5 + 0.45 * k)
            stroke_line(cr, [(bx0 - 4, yy), (bx0 + 18, yy + 12)], 3, alpha(WHITE, 0.25), curve=False)
    # ---- legs and lower garment
    for side in (-1, 1):
        fx = side * pw * 0.42
        _limb(cr, [(fx, -150), (fx, -60), (fx, -18)], lw * 0.9, skin)
        ellipse(cr, fx + 8, -8, 28, 13)                    # bare feet
        paint(cr, shade(skin, -0.05), OUTLINE, 4)
        stroke_line(cr, [(fx - 18, -28), (fx + 20, -28)], 5, GOLD, curve=False)      # anklet
    if female:
        col = look["saree"]
        smooth(cr, [(-pw - 4, py - 40), (pw + 4, py - 40), (pw + 40, -60), (pw + 46, -22), (-pw - 46, -22),
                    (-pw - 40, -60)])
        paint(cr, lin(0, py - 40, 0, -22, [(0, shade(col, 0.25)), (1, shade(col, -0.2))]), OUTLINE, 5)
        for k in range(-2, 3):                             # pleats
            stroke_line(cr, [(k * 18, py - 10), (k * 24, -30)], 3, alpha(OUTLINE, 0.3), curve=False)
        cr.save()
        smooth(cr, [(-pw - 4, py - 40), (pw + 4, py - 40), (pw + 40, -60), (pw + 46, -22), (-pw - 46, -22),
                    (-pw - 40, -60)])
        cr.clip()
        cr.rectangle(-pw - 60, -54, 2 * pw + 120, 30)
        _gold(cr, None, 0)
        cr.restore()
    else:
        col = look["dhoti"]
        pts = [(-pw - 8, py - 26), (pw + 8, py - 26), (pw + 22, -110), (pw * 0.5, -96), (0, -104), (-pw * 0.5, -96),
               (-pw - 22, -110)]
        smooth(cr, pts)
        paint(cr, lin(0, py - 26, 0, -100, [(0, shade(col, 0.25)), (1, shade(col, -0.15))]), OUTLINE, 5)
        for k in range(-1, 2):                             # front pleats
            stroke_line(cr, [(k * 12, py - 6), (k * 16, -100)], 3, alpha(OUTLINE, 0.3), curve=False)
        stroke_line(cr, [(-pw - 20, -112), (-pw * 0.5, -98), (0, -106), (pw * 0.5, -98), (pw + 20, -112)], 8,
                    look.get("border", GOLD))
    # ---- angavastram / pallu behind the body (swaying end)
    cloth = look["cloth"]
    tail_x = -sw - 30 + sway * 10
    smooth(cr, [(-sw + 4, shoulder_y - 10), (-sw - 20, shoulder_y + 60), (tail_x, py + 40), (tail_x + 30, py + 60),
                (-sw + 30, shoulder_y + 70)])
    paint(cr, lin(-sw, shoulder_y, -sw, py, [(0, shade(cloth, 0.2)), (1, shade(cloth, -0.25))]), OUTLINE, 4.5)
    # ---- back arm
    _arm(cr, -1, arms[1], shoulder_y, sw, aw, skin, hold_back)
    # ---- torso
    top, bot = sy + breathe, py + 14
    body = [(-sw, top + 30), (-sw + 18, top + 4), (0, top - 4), (sw - 18, top + 4), (sw, top + 30),
            (pw + 6, bot - 20), (pw - 4, bot), (-pw + 4, bot), (-pw - 6, bot - 20)]
    if female:
        smooth(cr, body)
        paint(cr, lin(-sw, top, sw, bot, [(0, shade(skin, 0.2)), (1, shade(skin, -0.1))]), OUTLINE, 5)
        smooth(cr, [(-sw, top + 30), (-sw + 18, top + 4), (0, top + 4), (sw - 18, top + 4), (sw, top + 30),
                    (sw - 10, top + 110), (-sw + 10, top + 110)])
        paint(cr, lin(0, top, 0, top + 110, [(0, shade(look["blouse"], 0.25)), (1, shade(look["blouse"], -0.2))]),
              OUTLINE, 4.5)
        smooth(cr, [(-sw + 10, top + 10), (sw - 4, top + 6), (pw + 20, bot - 10), (pw - 6, bot + 10),
                    (-sw + 30, top + 90)])                 # the pallu across the chest
        paint(cr, lin(-sw, top, sw, bot, [(0, shade(cloth, 0.25)), (1, shade(cloth, -0.15))]), OUTLINE, 4.5)
        stroke_line(cr, [(-sw + 12, top + 14), (sw - 2, top + 10)], 6, GOLD)
    else:
        smooth(cr, body)
        paint(cr, lin(-sw, top, sw, bot, [(0, shade(skin, 0.25)), (0.5, skin), (1, shade(skin, -0.12))]),
              OUTLINE, 5)
        stroke_line(cr, [(-sw + 20, top + 10), (-10, top + 80), (pw - 4, bot - 10)], 3.5, PEARL)   # sacred thread
        smooth(cr, [(sw - 8, top + 6), (sw + 6, top + 30), (sw - 20, top + 70), (-pw, bot - 40), (-pw - 10, bot - 70),
                    (sw - 40, top + 30)])                  # angavastram across the chest
        paint(cr, lin(-sw, top, sw, bot, [(0, shade(cloth, 0.25)), (1, shade(cloth, -0.15))]), OUTLINE, 4.5)
        rrect_y = bot - 30                                 # waist sash
        smooth(cr, [(-pw - 6, rrect_y), (pw + 6, rrect_y), (pw + 8, rrect_y + 24), (-pw - 8, rrect_y + 24)])
        _gold(cr, None, 3.5)
        _jewel(cr, 0, rrect_y + 12, 9, EMERALD)
    # necklaces
    for k, (dy, w, col) in enumerate(((22, 40, GOLD), (40, 56, GOLD), (58, 66, PEARL))):
        stroke_line(cr, [(-w, top + 6), (0, top + dy + 18), (w, top + 6)], 6 if col is not PEARL else 5,
                    OUTLINE)
        stroke_line(cr, [(-w, top + 6), (0, top + dy + 18), (w, top + 6)], 4 if col is not PEARL else 3, col)
    _jewel(cr, 0, top + 62, 11, RUBY)
    # ---- head
    cr.save()
    cr.translate(0, hy + breathe * 2)
    cr.rotate(math.sin(t * 1.5 + seed) * 0.02 if bob else 0.0)
    fancy_head(cr, t, 0, 0, hr, look, eyes, mouth, (lookdir[0] * facing, lookdir[1]), brows, turn,
               blink=blink_at(t, seed) if eyes == "open" else 0.0)
    cr.restore()
    # ---- front arm
    _arm(cr, 1, arms[0], shoulder_y, sw, aw, skin, hold)
    cr.restore()
    if alpha_ < 1:
        cr.pop_group_to_source()
        cr.paint_with_alpha(max(0.0, alpha_))


# ---------------------------------------------------------------- Brahma, seated on a lotus
BRAHMA = dict(skin=hexc("#e9a877"), hair="bald", hair_col=hexc("#f2efe8"), beard=hexc("#f4f1ea"),
              stache=hexc("#f4f1ea"), brows_col=hexc("#e8e4dc"), crown="kirita", cloth=hexc("#c8402e"),
              dhoti=hexc("#e8892b"), tilak="dot")


def lotus_seat(cr, cx, cy, w, t=0.0):
    for row, (rw, rh, col) in enumerate(((1.0, 0.42, hexc("#e9729a")), (0.82, 0.36, hexc("#f39ab8")),
                                         (0.6, 0.3, hexc("#fbc6d6")))):
        n = 11 - row * 2
        for k in range(n):
            a = math.pi * (0.05 + 0.9 * k / (n - 1))
            px = cx - math.cos(a) * w * rw * 0.5
            py = cy - math.sin(a) * w * rh * 0.25 + row * -8
            ellipse(cr, px, py, w * 0.11, w * 0.2, -(math.pi / 2 - a) * 0.9)
            paint(cr, rad(px, py - w * 0.1, w * 0.25, [(0, hexc("#fff4f7")), (1, col)]), OUTLINE, 3)
    ellipse(cr, cx, cy + w * 0.06, w * 0.55, w * 0.1)
    paint(cr, lin(0, cy, 0, cy + w * 0.12, [(0, hexc("#7fb36a")), (1, hexc("#3f7a3a"))]), OUTLINE, 3)


def brahma(cr, t, x, y, s=1.0, eyes="open", mouth="smile", brows=None, lookdir=(0.0, 0.0), halo_a=1.0, laugh=0.0,
           seed=0, abhaya=1.0):
    """Brahma seated on a lotus with (x, y) at the centre of the lotus base: three visible heads (the fourth is
    behind), four arms holding the Vedas, a water pot, a rosary and a lotus, white beard, red and saffron cloth."""
    look = BRAHMA
    hr = 86
    shake = math.sin(t * 22) * 4 * laugh
    breathe = math.sin(t * 1.8 + seed)
    if halo_a:
        halo(cr, t, x, y - 520 * s, 170 * s, halo_a)
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    lotus_seat(cr, 0, 0, 520, t)
    # crossed legs under the dhoti
    smooth(cr, [(-200, -40), (-150, -120), (0, -140), (150, -120), (200, -40), (120, -10), (-120, -10)])
    paint(cr, lin(0, -140, 0, -10, [(0, shade(look["dhoti"], 0.25)), (1, shade(look["dhoti"], -0.2))]), OUTLINE, 5)
    stroke_line(cr, [(-190, -40), (0, -20), (190, -40)], 7, GOLD)
    sy = -330 + breathe * 2
    sw, pw = 88, 74
    # back arms: Vedas and kamandalu raised
    _arm(cr, -1, (120, -150), sy + 20, sw, 30, look["skin"], vedas)
    _arm(cr, 1, (120, -150), sy + 20, sw, 30, look["skin"], kamandalu)
    # torso
    top, bot = sy, -120
    smooth(cr, [(-sw, top + 30), (-sw + 18, top + 4), (0, top - 4), (sw - 18, top + 4), (sw, top + 30),
                (pw + 10, bot - 20), (pw, bot), (-pw, bot), (-pw - 10, bot - 20)])
    paint(cr, lin(-sw, top, sw, bot, [(0, shade(look["skin"], 0.25)), (1, shade(look["skin"], -0.12))]), OUTLINE, 5)
    stroke_line(cr, [(-sw + 20, top + 10), (-10, top + 90), (pw - 4, bot - 10)], 3.5, PEARL)
    smooth(cr, [(sw - 8, top + 6), (sw + 6, top + 30), (sw - 20, top + 70), (-pw, bot - 30), (-pw - 10, bot - 60),
                (sw - 40, top + 30)])
    paint(cr, lin(-sw, top, sw, bot, [(0, shade(look["cloth"], 0.25)), (1, shade(look["cloth"], -0.15))]), OUTLINE,
          4.5)
    for dy, w, col in ((22, 44, GOLD), (44, 60, GOLD), (64, 70, PEARL)):
        stroke_line(cr, [(-w, top + 6), (0, top + dy + 18), (w, top + 6)], 6, OUTLINE)
        stroke_line(cr, [(-w, top + 6), (0, top + dy + 18), (w, top + 6)], 4, col)
    # heads: the two side heads first, then the front one
    hy = top - 120
    for side in (-1, 1):
        cr.save()
        cr.translate(side * 118 + shake * 0.5, hy + 22)
        cr.scale(0.78, 0.78)
        fancy_head(cr, t, 0, 0, hr, look, "open" if eyes != "closed" else "closed", "smile", (side * 0.6, 0),
                   None, side * 1.0, blink=blink_at(t, seed + side * 3))
        cr.restore()
    cr.save()
    cr.translate(shake, hy)
    fancy_head(cr, t, 0, 0, hr, look, eyes, mouth, lookdir, brows, 0.0,
               blink=blink_at(t, seed) if eyes == "open" else 0.0)
    cr.restore()
    # front arms: right hand raised in blessing (abhaya), left holding a lotus and the rosary on the lap
    _arm(cr, 1, (150 - 60 * (1 - abhaya), -40 * abhaya + 140 * (1 - abhaya)), sy + 30, sw, 30, look["skin"], None)
    if abhaya > 0.5:                                       # the open palm of the blessing, facing the viewer
        hx, hy_ = sw - 8 + 150, sy + 30 - 40
        ellipse(cr, hx, hy_ - 26, 22, 30)
        paint(cr, shade(look["skin"], 0.08), OUTLINE, 4)
        for k in range(4):
            stroke_line(cr, [(hx - 15 + k * 10, hy_ - 44), (hx - 16 + k * 10.5, hy_ - 66)], 9, OUTLINE)
            stroke_line(cr, [(hx - 15 + k * 10, hy_ - 44), (hx - 16 + k * 10.5, hy_ - 66)], 5.5,
                        shade(look["skin"], 0.08))
        cr.arc(hx, hy_ - 26, 5, 0, 2 * math.pi)
        paint(cr, RUBY, None, 0)
    _arm(cr, -1, (40, 150), sy + 30, sw, 30, look["skin"], lambda c, hx, hy_: (lotus_flower(c, hx, hy_ - 30, 34),
                                                                             rosary(c, hx + 10, hy_)))
    cr.restore()
