"""Body Facts organ cast, shared by the doctor-channel videos: the brain, the nose's two working sides, the liver's
two lobes, plus the head bandage and fact card used in the hospital scenes. Faces, the heart, the scalpel and the
hospital set come from the first episode (videos/kidney_donor.py) so every episode looks like the same world."""
import math

from motion.engine import INK, WHITE, at, blob, dot, hexc, line, pop, rrect_pts, shape, write
from videos.kidney_donor import eyes, grad_fill, mouth

PINK_A, PINK_B = hexc("#ffc2cf"), hexc("#e07a95")       # brain gradient: light -> dark
LIV_A, LIV_B = hexc("#b5524a"), hexc("#6e2320")         # liver gradient
TURB_A, TURB_B = hexc("#ffb3a8"), hexc("#e0786c")       # nasal tissue gradient


def _ellipse(cx, cy, rx, ry, n=90, wob=0.0, seed=0):
    return [(cx + rx * (1 + wob * math.sin(k * 7 + seed)) * math.cos(2 * math.pi * k / n),
             cy + ry * (1 + wob * math.sin(k * 5 + seed)) * math.sin(2 * math.pi * k / n)) for k in range(n)]


def brain(cr, t, x, y, s, mood="calm", talking=False, look=0.0, shake=0.0, squish=0.0):
    """Cute pink brain seen from the front: two halves, wiggly folds, a face on the front."""
    x += math.sin(t * 50) * shake
    y += math.sin(t * 2.1) * 3
    with at(cr, x, y, s):
        cr.scale(1 + 0.05 * squish, 1 - 0.08 * squish)
        pts = []
        for k in range(120):            # bumpy outline: folds poke out round the edge
            a = 2 * math.pi * k / 120
            r = 1 + 0.035 * math.sin(a * 14)
            pts.append((165 * r * math.cos(a), 122 * r * math.sin(a) - 10 * max(0, -math.sin(a)) ** 3))
        grad_fill(cr, pts, PINK_A, PINK_B, 0, 0, 170, lw=4.5)
        line(cr, [(0, -128), (6, -96), (-4, -70), (2, -48)], 4, hexc("#b94f6c"), seed=301, amp=0.3)   # middle split
        for k, (fx, fy, w) in enumerate([(-110, -60, 40), (-70, -90, 46), (70, -90, 46), (110, -60, 40),
                                         (-130, 10, 30), (130, 10, 30), (-100, 70, 44), (100, 70, 44),
                                         (-40, 95, 34), (40, 95, 34)]):
            line(cr, [(fx - w / 2, fy), (fx - w / 6, fy - 12), (fx + w / 6, fy + 8), (fx + w / 2, fy - 4)], 3.5,
                 hexc("#c75f7b"), seed=310 + k, amp=0.4)
        blob(cr, -70, -70, 26, 14, hexc("#ffffff", 0.35), seed=330, amp=0.3, lw=0, stroke=None)
        eyes(cr, 0, -6, 1.15, mood, look, blink=(int(t * 10) % 41 == 0))
        mouth(cr, 0, 46, 1.1, mood, talking, t)


def skull(cr, cx, cy, lid_open):
    """Cream skull ring round the brain; the top cap swings up on a hinge at the right (0 = shut, 1 = open)."""
    bone, bone_d = hexc("#f2e6cf"), hexc("#d9c7a3")
    ro, ri = (300, 250), (262, 214)

    def band(a0, a1):
        n = 40
        outer = [(cx + ro[0] * math.cos(a0 + (a1 - a0) * k / n), cy + ro[1] * math.sin(a0 + (a1 - a0) * k / n))
                 for k in range(n + 1)]
        inner = [(cx + ri[0] * math.cos(a1 - (a1 - a0) * k / n), cy + ri[1] * math.sin(a1 - (a1 - a0) * k / n))
                 for k in range(n + 1)]
        return outer + inner

    shape(cr, band(-0.62, math.pi + 0.62), bone, seed=340, amp=0.3, lw=4)        # sides and bottom
    hx, hy = cx + ro[0] * math.cos(-0.62), cy + ro[1] * math.sin(-0.62)
    with at(cr, hx, hy, 1.0, rot=-1.9 * lid_open):
        cr.translate(-hx, -hy)
        shape(cr, band(math.pi + 0.62, 2 * math.pi - 0.62), bone, seed=341, amp=0.3, lw=4)
        line(cr, [(cx - 120, cy - 238), (cx - 60, cy - 246)], 3, bone_d, seed=342, amp=0.3)


def head_bandage(cr, x, y, t):
    """Post-surgery bandage wrapped round the top of a person() head standing at (x, y), scale 1."""
    hy = y - 26 - 104 - 40 + 12 + math.sin(t * 2.6) * 1.6
    shape(cr, [(x - 44, hy - 8), (x - 40, hy - 34), (x - 20, hy - 50), (x + 20, hy - 50), (x + 40, hy - 34),
               (x + 44, hy - 8), (x, hy - 16)], WHITE, seed=350, amp=0.5, lw=3.5)
    line(cr, [(x - 40, hy - 22), (x + 40, hy - 24)], 2.5, hexc("#d6dce3"), seed=351, amp=0.3)
    line(cr, [(x - 28, hy - 40), (x + 30, hy - 38)], 2.5, hexc("#d6dce3"), seed=352, amp=0.3)


def card(cr, t, start, x, y, runs, size=38, w=440):
    """White fact card that pops in at `start`."""
    with at(cr, x, y, max(0.85, pop(t, start, 0.25))):
        shape(cr, rrect_pts(-w / 2, -42, w, 84, 18, 12), WHITE, seed=360, amp=0.3, lw=3.5)
        write(cr, runs, 0, 14, size, align="center", bold=True)


# ------------------------------------------------------------------ the nose's two sides
def turbinate(cr, t, x, y, side, swell, mood="calm", talking=False, look=0.0, hat=None):
    """The puffy tissue on the outer wall of one nasal passage, as a character. `side` = -1 (screen left wall) or
    +1 (screen right wall); `swell` 0 = shrunk (that side breathes) .. 1 = swollen shut (that side rests)."""
    w = 92 + 84 * swell              # width out from the wall; the passage is ~190 wide
    h = 170 + 30 * swell
    cx = x - side * (w / 2 - 6)      # grows out from its wall into the passage
    b = 1 + 0.02 * math.sin(t * 2.4 + side)
    pts = _ellipse(cx, y, w / 2 * b, h, wob=0.03, seed=side)
    grad_fill(cr, pts, TURB_A, TURB_B, cx, y, h, lw=4)
    fx = cx
    s = 0.85 + 0.2 * swell
    eyes(cr, fx, y - 30, s, mood, look, blink=(int(t * 10 + side * 7) % 43 == 0))
    mouth(cr, fx, y + 22 * s + 6, s, mood, talking, t)
    if hat == "hard":                # on shift: a yellow hard hat
        with at(cr, fx, y - h + 24, 0.9):
            shape(cr, [(-46, 10), (-40, -22), (-16, -40), (16, -40), (40, -22), (46, 10)], hexc("#ffd23f"), seed=370,
                  amp=0.4, lw=3.5)
            line(cr, [(-60, 12), (60, 12)], 6, INK, seed=371, amp=0.3)
    elif hat == "sleep":             # on break: a nightcap
        with at(cr, fx, y - h + 30, 1.0):
            shape(cr, [(-52, 14), (-30, -30), (20, -50), (70, -30), (52, 14)], hexc("#5b7fd6"), seed=372, amp=0.5,
                  lw=3.5)
            blob(cr, 76, -26, 13, 13, WHITE, seed=373, amp=0.4, lw=3)
    return fx, y - 30


def airflow(cr, t, x0, x1, y0, y1, strength, seed=0):
    """Wisps of air rising through a passage; `strength` 0..1 sets how many get through."""
    n = int(round(7 * strength))
    for i in range(n):
        u = ((t * (0.9 + 0.1 * i) + i / max(1, n) + seed * 0.13) % 1.0)
        yy = y1 - (y1 - y0) * u
        xx = (x0 + x1) / 2 + math.sin(u * 9 + i * 2) * (x1 - x0) * 0.22
        a = math.sin(math.pi * u)
        line(cr, [(xx - 12, yy + 22), (xx, yy), (xx + 10, yy - 20)], 5, hexc("#ffffff", 0.85 * a), seed=380 + i,
             amp=0.4)


# ------------------------------------------------------------------ the liver's two lobes
def big_lobe_pts(x, y, s):
    """The liver's big lobe (the patient's right, so screen left in a front view): a rounded wedge."""
    base = [(-200, -60), (-150, -110), (-40, -120), (60, -100), (110, -60), (100, 10), (40, 60), (-80, 90),
            (-170, 70), (-215, 10)]
    return [(x + px * s, y + py * s) for px, py in base]


def small_lobe_pts(x, y, s, grown=0.0):
    """The small lobe: a tapering tongue; as it regrows it fills out into a rounder (different) shape."""
    base = [(-70, -80), (0, -92), (90, -78), (170, -40), (200, -10), (150, 20), (60, 46), (-40, 60), (-80, 30)]
    full = [(-190, -100), (-60, -140), (80, -130), (190, -80), (230, -10), (190, 60), (60, 110), (-90, 120),
            (-200, 60)]
    return [(x + (bx + (fx - bx) * grown) * s, y + (by + (fy - by) * grown) * s) for (bx, by), (fx, fy)
            in zip(base, full)]


def lobe(cr, t, pts, fx, fy, s, mood="calm", talking=False, look=0.0, shake=0.0):
    dx = math.sin(t * 50) * shake
    pts = [(px + dx, py) for px, py in pts]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    cx, cy, r = sum(xs) / len(xs), sum(ys) / len(ys), max(max(xs) - min(xs), max(ys) - min(ys)) / 2
    shape(cr, pts, LIV_B, seed=390, amp=0.5, lw=0, stroke=None)
    grad_fill(cr, _smooth(pts), LIV_A, LIV_B, cx, cy, r, lw=4.5)
    blob(cr, cx - r * 0.35, cy - r * 0.3, 22 * s, 12 * s, hexc("#ffffff", 0.22), seed=391, amp=0.3, lw=0, stroke=None)
    eyes(cr, fx + dx, fy, s, mood, look, blink=(int(t * 10 + fx) % 39 == 0))
    mouth(cr, fx + dx, fy + 46 * s, s, mood, talking, t)


def _smooth(pts, k=6):
    """Rounded closed outline through the given corners (Chaikin-style subdivision)."""
    for _ in range(3):
        out = []
        for i, p in enumerate(pts):
            q = pts[(i + 1) % len(pts)]
            out += [(0.75 * p[0] + 0.25 * q[0], 0.75 * p[1] + 0.25 * q[1]),
                    (0.25 * p[0] + 0.75 * q[0], 0.25 * p[1] + 0.75 * q[1])]
        pts = out
    return pts


def calendar(cr, t, x, y, label, start):
    """Little tear-off calendar page."""
    with at(cr, x, y, max(0.85, pop(t, start, 0.2)), rot=0.06):
        shape(cr, rrect_pts(-90, -70, 180, 140, 14, 12), WHITE, seed=395, amp=0.4, lw=3.5)
        shape(cr, rrect_pts(-90, -70, 180, 40, 10, 12), hexc("#d8363a"), seed=396, amp=0.3, lw=3.5)
        for k in (-40, 40):
            dot(cr, x * 0 + k, -70, 7, INK)
        write(cr, [(label, INK)], 0, 44, 46, align="center", bold=True)
