"""Operating-table kit for Body Facts surgery scenes, styled on the owner's reference Short (a knee on blue drapes,
cut open, with clamp characters holding the wound): drapes, a numbing syringe, the incision (cut line, opening
wound with red tissue and blood), clamp characters, forceps and stitches. World units; call inside a camera."""
import math

from motion.engine import INK, WHITE, at, blob, dot, hexc, lerp, line, rrect_pts, seg, shape, sharp_shape

DRAPE, DRAPE_D = hexc("#86cfdc"), hexc("#5fb3c4")
SKIN, SKIN_D = hexc("#f9e2c4"), hexc("#e8bfa0")
LIP = hexc("#efb8a0")
MUSCLE, MUSCLE_D = hexc("#c4544b"), hexc("#8e2f2c")
BLOOD, BLOOD_D = hexc("#c8202c"), hexc("#7d1018")
METAL, METAL_D = hexc("#c9ced6"), hexc("#7d8591")


def drapes(cr):
    cr.set_source_rgba(*DRAPE)
    cr.paint()                       # whole frame: scenes can sit anywhere in the world
    for k in range(12):   # cloth folds, repeated across the world
        y = -200 + k * 150
        for x0 in (0, 1600):
            line(cr, [(x0 - 300, y), (x0 - 60, y + 30), (x0 + 140, y - 10)], 4, DRAPE_D, seed=700 + k, amp=1.0)
            line(cr, [(x0 + 600, y + 60), (x0 + 800, y + 90), (x0 + 1020, y + 50)], 4, DRAPE_D, seed=720 + k, amp=1.0)


def ellipse(cx, cy, rx, ry, n=64):
    return [(cx + rx * math.cos(2 * math.pi * k / n), cy + ry * math.sin(2 * math.pi * k / n)) for k in range(n)]


def slit(cx, cy, rx, bend, n=40):
    """The cut line: left to right across (cx, cy), bowed by `bend`."""
    return [(cx - rx + 2 * rx * k / (n - 1), cy + bend * math.sin(math.pi * k / (n - 1))) for k in range(n)]


def cut_line(cr, pts, cut):
    """A fresh cut drawn up to `cut` (0..1) along pts: a red line with a dark edge."""
    if cut <= 0:
        return None
    n = max(2, int(len(pts) * min(1.0, cut)))
    p = pts[:n]
    line(cr, p, 9, BLOOD_D, seed=740, amp=0.4)
    line(cr, p, 5, BLOOD, seed=741, amp=0.4)
    for k in range(0, n, 6):     # beads of blood along it
        dot(cr, p[k][0], p[k][1] + 5, 4, BLOOD)
    return p[-1]


def wound(cr, t, cx, cy, rx, ry, open_u, inside=None, bone=False, seed=0):
    """An open incision, `open_u` 0 (a closed slit) .. 1 (fully open). `inside(cr)` draws what's visible through it,
    clipped to the opening. `bone=True` adds a cream ring of skull edge (for the head)."""
    if open_u <= 0:
        return
    h = max(4.0, ry * open_u)
    shape(cr, ellipse(cx, cy + 4, rx + 22, h + 20), LIP, seed=750 + seed, amp=0.8, lw=3.5)          # raised skin lip
    shape(cr, ellipse(cx, cy, rx + 6, h + 6), MUSCLE, seed=751 + seed, amp=0.6, lw=4)              # red tissue
    for k in range(16):                                                                         # muscle fibres
        a = 2 * math.pi * k / 16
        x0, y0 = cx + (rx - 4) * math.cos(a), cy + (h - 4) * math.sin(a)
        x1, y1 = cx + (rx + 2) * math.cos(a + 0.06), cy + (h + 2) * math.sin(a + 0.06)
        line(cr, [(x0, y0), (x1, y1)], 2.5, MUSCLE_D, seed=760 + k, amp=0.3)
    inner_rx, inner_ry = rx - 16, max(2.0, h - 16)
    if bone:
        shape(cr, ellipse(cx, cy, rx - 8, max(3.0, h - 8)), hexc("#f2e6cf"), seed=752 + seed, amp=0.4, lw=3)
        inner_rx, inner_ry = rx - 26, max(2.0, h - 26)
    cr.save()
    cr.new_path()
    pts = ellipse(cx, cy, inner_rx, inner_ry)
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.close_path()
    cr.clip()
    cr.set_source_rgba(*hexc("#6e2730"))
    cr.paint()
    if inside:
        inside(cr)
    cr.restore()
    shape(cr, ellipse(cx, cy, inner_rx, inner_ry), None, seed=753 + seed, amp=0.4, lw=3.5)
    # blood: drips from the lower edge, running down the skin, longer as time goes on
    for k, (fx, base) in enumerate(((-0.5, 18), (0.08, 34), (0.55, 12))):
        x = cx + rx * fx
        y = cy + h * math.sqrt(max(0.0, 1 - fx * fx)) + 10
        grow = min(1.0, open_u * 1.5) * (0.6 + 0.4 * math.sin(t * 0.9 + k * 2.1) ** 2)
        ln = base * grow
        shape(cr, [(x - 4, y - 8), (x + 4, y - 8), (x + 3, y + ln - 4), (x + 7, y + ln + 4), (x, y + ln + 12),
                   (x - 7, y + ln + 4), (x - 3, y + ln - 4)], BLOOD, seed=770 + k, amp=0.3, lw=2.5, stroke=BLOOD_D)
        u = (t * 0.7 + k * 0.33) % 1.0          # a drop falling off now and then
        if open_u >= 1 and u < 0.5:
            blob(cr, x, y + ln + 16 + 160 * u * u, 5, 7, BLOOD, seed=775 + k, amp=0.2, lw=2, stroke=BLOOD_D)


def syringe(cr, t, x, y, s, rot, push):
    """Numbing injection. (x, y) is the needle tip; `push` 0..1 empties it."""
    with at(cr, x, y, s, rot=rot):
        line(cr, [(0, 0), (0, -46)], 3, METAL_D, seed=780, amp=0.1)
        shape(cr, rrect_pts(-16, -170, 32, 124, 6, 12), hexc("#eaf6ff"), seed=781, amp=0.3, lw=3.5)
        fill = 1 - push
        if fill > 0.02:
            shape(cr, rrect_pts(-13, -50 - 116 * fill, 26, 116 * fill, 4, 12), hexc("#5fb6ff"), seed=782, amp=0.2, lw=0,
                  stroke=None)
        for k in range(5):
            line(cr, [(-16, -70 - k * 20), (-6, -70 - k * 20)], 2, INK, seed=783 + k, amp=0.1)
        top = -50 - 116 * fill                     # plunger seal sits on the liquid
        handle = top - 140
        shape(cr, rrect_pts(-12, top - 6, 24, 8, 3, 8), hexc("#3a3d45"), seed=787, amp=0.1, lw=0, stroke=None)
        line(cr, [(0, top), (0, handle)], 6, METAL_D, seed=788, amp=0.1)
        shape(cr, rrect_pts(-26, handle - 10, 52, 12, 4, 10), METAL, seed=789, amp=0.2, lw=3)


def clamp(cr, t, x, y, side, s=1.0, mood="happy", look=0.0):
    """Clamp character holding a wound edge open, like the reference's retractors: a metal arm from off-screen,
    a curved claw at (x, y) gripping the edge, and googly eyes on the hinge. side=-1 comes from the left."""
    from videos.kidney_donor import eyes
    with at(cr, x, y, s, flip=side > 0):
        # arm in from the left (flipped for the right)
        sharp_shape(cr, [(-430, 70), (-120, 18), (-110, 42), (-430, 100)], METAL, seed=790, amp=0.6, lw=3.5)
        sharp_shape(cr, [(-430, 130), (-120, 52), (-112, 74), (-430, 160)], METAL, seed=791, amp=0.6, lw=3.5)
        blob(cr, -112, 46, 30, 30, METAL, seed=792, amp=0.4, lw=3.5)                       # hinge
        # claws hooking over the wound edge
        for dy in (-26, 22):
            shape(cr, [(-100, 40 + dy * 0.4), (-40, 30 + dy), (-6, 10 + dy), (4, 30 + dy), (-36, 52 + dy),
                       (-96, 60 + dy * 0.4)], METAL, seed=793 + dy, amp=0.4, lw=3.5)
        line(cr, [(-80, 34), (-30, 26)], 3, WHITE, seed=796, amp=0.2)
        with at(cr, -112, 40, 1.0, flip=side > 0):
            eyes(cr, 0, 0, 0.5, mood, look * (-1 if side > 0 else 1))


def forceps(cr, x, y, s=1.0, grip=1.0):
    """Long forceps reaching down to (x, y) from above."""
    with at(cr, x, y, s):
        gap = 22 * (1 - grip) + 6
        for sx in (-1, 1):
            sharp_shape(cr, [(sx * gap, 0), (sx * (gap + 6), 0), (sx * 40, -420), (sx * 26, -420)], METAL, seed=800 + sx,
                        amp=0.4, lw=3)


def stitches(cr, pts, progress):
    """Sutures closing a cut, appearing left to right."""
    n = int(len(pts) * progress)
    line(cr, pts[:max(2, n)], 4, MUSCLE_D, seed=810, amp=0.3) if n > 1 else None
    for k in range(2, n, 4):
        x, y = pts[k]
        line(cr, [(x - 9, y - 12), (x + 9, y + 12)], 3.5, hexc("#2b3a66"), seed=811 + k, amp=0.2)
        line(cr, [(x + 9, y - 12), (x - 9, y + 12)], 3.5, hexc("#2b3a66"), seed=812 + k, amp=0.2)


def scalpel_tip(px, py, rot, s):
    """Where to put videos.kidney_donor.scalpel() so its blade tip lands on (px, py) at rotation `rot`."""
    return px - 80 * s * math.sin(rot), py + 80 * s * math.cos(rot)


def along(pts, u):
    """Point at fraction u of a polyline."""
    u = min(1.0, max(0.0, u))
    i = min(len(pts) - 1, int(u * (len(pts) - 1)))
    return pts[i]


def progress(t, a, b):
    return seg(t, a, b)


def lerp2(p, q, u):
    return lerp(p[0], q[0], u), lerp(p[1], q[1], u)
