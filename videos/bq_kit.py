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


# ---------------------------------------------------------------- the two-tier hook (Mayank frame-0 rules, 29 Oct 2026)
def hook2(cr, t, small, big, end, y=210, small_size=46, big_size=150, big_at=0.0, mark=None, mark_at=None,
          small_col=(1, 1, 1, 1), big_col=None):
    """Small setup words on top, ONE big red key word under them (popping in at `big_at`), and a red mark drawn on
    the key word as it is spoken: mark = "strike" | "circle" | "tick" at `mark_at`. Gone 0.25 s after `end`."""
    from motion import thriller as th
    from motion.polish import text_width
    if t >= end + 0.25:
        return
    a = 1.0 if t < end else 1 - (t - end) / 0.25
    big_col = big_col or th.RED
    cr.save()
    cr.push_group()
    sz = small_size
    w = text_width(cr, small, sz, th.HOOK)
    if w > W - 80:
        sz *= (W - 80) / w
    th._text(cr, small, W / 2, y, sz, small_col, th.HOOK)
    if t >= big_at:
        bz = big_size
        bw = text_width(cr, big, bz, th.HOOK)
        if bw > W - 70:
            bz *= (W - 70) / bw
            bw = W - 70
        k = min(1.0, (t - big_at) / 0.18)
        pop = 1.35 - 0.35 * k + 0.06 * math.sin(min(1.0, (t - big_at) / 0.35) * math.pi)
        by = y + sz * 0.35 + bz * 0.95
        cr.save()
        cr.translate(W / 2, by - bz * 0.35)
        cr.scale(pop, pop)
        cr.translate(-W / 2, -(by - bz * 0.35))
        th._text(cr, big, W / 2, by, bz, big_col, th.HOOK)
        cr.restore()
        if mark and mark_at is not None and t >= mark_at:
            u = min(1.0, (t - mark_at) / 0.25)
            x0, x1 = W / 2 - bw / 2 - 14, W / 2 + bw / 2 + 14
            cy = by - bz * 0.38
            cr.set_source_rgba(*th.RED)
            cr.set_line_cap(1)
            if mark == "strike":
                cr.set_line_width(bz * 0.11)
                cr.move_to(x0, cy + bz * 0.08)
                cr.line_to(x0 + (x1 - x0) * u, cy - bz * 0.08 * (2 * u - 1))
                cr.stroke()
            elif mark == "circle":
                cr.set_line_width(9)
                cr.save()
                cr.translate(W / 2, cy)
                cr.scale((x1 - x0) / 2 + 10, bz * 0.62)
                cr.arc(0, 0, 1, -2.2, -2.2 + 2 * math.pi * u * 1.05)
                cr.restore()
                cr.stroke()
            elif mark == "tick":
                cr.set_line_width(14)
                tx = x1 + 30
                pts = [(tx, cy), (tx + 22, cy + 26), (tx + 64, cy - 36)]
                cr.move_to(*pts[0])
                if u < 0.4:
                    q = u / 0.4
                    cr.line_to(pts[0][0] + (pts[1][0] - pts[0][0]) * q, pts[0][1] + (pts[1][1] - pts[0][1]) * q)
                else:
                    q = (u - 0.4) / 0.6
                    cr.line_to(*pts[1])
                    cr.line_to(pts[1][0] + (pts[2][0] - pts[1][0]) * q, pts[1][1] + (pts[2][1] - pts[1][1]) * q)
                cr.stroke()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def ring(cr, t, start, x, y, rx, ry, col=None, lw=9, dur=0.3):
    """A red marker circle drawn round something from `start`."""
    from motion import thriller as th
    if t < start:
        return
    u = min(1.0, (t - start) / dur)
    cr.save()
    cr.set_source_rgba(*(col or th.RED))
    cr.set_line_width(lw)
    cr.set_line_cap(1)
    cr.save()
    cr.translate(x, y)
    cr.scale(rx, ry)
    cr.arc(0, 0, 1, -2.0, -2.0 + 2 * math.pi * u * 1.05)
    cr.restore()
    cr.stroke()
    cr.restore()


def plain(cr, top, bottom=None):
    """A plain background (frame-0 rule: one subject on an empty ground) with a soft centre glow."""
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc(top)), (1, hexc(bottom or top))]))
    cr.fill()
    soft_disc(cr, W / 2, H * 0.48, 420, (1, 1, 1, 0.08))
