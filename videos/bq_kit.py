"""Shared bits for the Big Questions batch 2 videos (kitten_evil, who_made_evil, prayer_plan, pascal_bet,
heaven_forever): talking characters, the two-doors dilemma, a scroll, a night sky."""
import math
import random

from motion.engine import W, H, hexc
from motion.pkit import GOLD, red_x
from motion.polish import OUTLINE, WHITE, alpha, bold_text, ellipse, lin, paint, rrect, soft_disc, stroke_line
from motion.toons import person


def mouth_of(tl, who, t, rest="smile"):
    return "talk" if tl is not None and tl.speaking(who, t) else rest


def talker(cr, t, tl, speaker, cast, x, y, s=1.0, rest="smile", **kw):
    """A character whose mouth flaps while `speaker` is talking (unless a mouth is given)."""
    if kw.get("mouth") is None:
        kw["mouth"] = mouth_of(tl, speaker, t, rest)
    person(cr, t, x, y, s, cast, **kw)


def door(cr, x, y, s, label, col, label_size=32):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -110, -300, 220, 300, 12)
    paint(cr, lin(0, -300, 0, 0, [(0, col), (1, col)]), OUTLINE, 6)
    rrect(cr, -84, -272, 168, 110, 8)
    paint(cr, alpha(WHITE, 0.15), alpha(OUTLINE, 0.5), 3)
    cr.arc(70, -150, 12, 0, 2 * math.pi)
    paint(cr, GOLD, OUTLINE, 4)
    cr.restore()
    bold_text(cr, label, x, y - 330 * s, label_size, WHITE)


def two_doors(cr, t, labels, cols, x_at=None, y=900, s=0.9, label_size=32):
    """The dilemma: two doors side by side; `x_at` = (time of the left X, time of the right X)."""
    for k, (lab, col) in enumerate(zip(labels, cols)):
        x = 190 + 340 * k
        door(cr, x, y, s, lab, col, label_size)
        if x_at is not None and x_at[k] is not None and t >= x_at[k]:
            red_x(cr, t, x_at[k], x, y - 150 * s, 70)


def scroll(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -220, -170, 440, 340, 10)
    paint(cr, hexc("#f2e2b8"), OUTLINE, 6)
    for side in (-1, 1):
        rrect(cr, -240, side * 170 - 22, 480, 44, 22)
        paint(cr, hexc("#c8a868"), OUTLINE, 5)
    for k in range(6):
        stroke_line(cr, [(-170, -110 + k * 40), (170 - 40 * (k % 2), -110 + k * 40)], 4, alpha(OUTLINE, 0.35),
                    curve=False)
    cr.restore()


def night_sky(cr, t, top="#0b1030", bottom="#2a2a5e", seed=7, n=90):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc(top)), (1, hexc(bottom))]))
    cr.fill()
    rng = random.Random(seed)
    for _ in range(n):
        x, y, r = rng.uniform(0, W), rng.uniform(0, H * 0.7), rng.uniform(1.2, 3.4)
        tw = 0.55 + 0.45 * math.sin(t * rng.uniform(1.5, 4.0) + rng.uniform(0, 6))
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 0.92, 0.35 + 0.6 * tw)
        cr.fill()


def moon(cr, x, y, r=60):
    soft_disc(cr, x, y, r * 2.4, (1, 0.96, 0.8, 0.18))
    ellipse(cr, x, y, r, r)
    paint(cr, hexc("#fff6d8"), None, 0)
    for dx, dy, rr in ((-18, -10, 12), (14, 18, 9), (20, -22, 7)):
        ellipse(cr, x + dx, y + dy, rr, rr)
        paint(cr, hexc("#efe2b8"), None, 0)


def heart_shape(cr, x, y, s, col, crack=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.move_to(0, 40)
    cr.curve_to(-70, -10, -50, -70, 0, -36)
    cr.curve_to(50, -70, 70, -10, 0, 40)
    paint(cr, col, OUTLINE, 5)
    if crack > 0:
        stroke_line(cr, [(0, -34), (-10, -10), (8, 6), (-4, 30)][:max(2, int(4 * crack))], 6, OUTLINE, curve=False)
    cr.restore()
