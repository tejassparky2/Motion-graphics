"""Simple drawn props for news panels. Each draws around (0, 0) at scale `s`; all generic, no real logos."""
import math

from .engine import INK, RED, WHITE, at, blob, dot, ease_out, hexc, line, rrect_pts, shape, write

GREY = hexc("#a9adb5")
STEEL = hexc("#c9ccd2")
SKYB = hexc("#7fc8e8")
GREEN = hexc("#2e9e52")
GOLD = hexc("#f2b632")
NAVY = hexc("#2b2d3a")


def truck(c, x, y, s=1.0, seed=10000):
    with at(c, x, y, s):
        shape(c, rrect_pts(-130, -70, 170, 100, 8, 14), WHITE, seed=seed, amp=0.4, lw=4)
        shape(c, [(40, -40), (95, -40), (125, -5), (125, 30), (40, 30)], hexc("#e0483d"), seed=seed + 1, amp=0.4, lw=4)
        shape(c, [(58, -32), (92, -32), (112, -8), (58, -8)], SKYB, seed=seed + 2, amp=0.3, lw=3)
        for wx in (-95, -40, 90):
            blob(c, wx, 34, 18, 18, INK, seed + 3 + wx, amp=0.2, lw=0, stroke=None)
            dot(c, wx, 34, 7, GREY)
        for k, col in enumerate((GREEN, GOLD, hexc("#e0487a"))):   # groceries inside
            blob(c, -100 + k * 40, -30, 16, 20, col, seed + 10 + k, amp=0.4, lw=3)


def barrel(c, x, y, s=1.0, col=None, label=None, seed=10100):
    with at(c, x, y, s):
        shape(c, rrect_pts(-30, -42, 60, 84, 10, 12), col or hexc("#3a6ea5"), seed=seed, amp=0.4, lw=4)
        for yy in (-16, 16):
            line(c, [(-30, yy), (30, yy)], 3, INK, seed + 1 + yy, amp=0.2)
        if label:
            write(c, [(label, WHITE)], 0, 8, 18, align="center", bold=True)


def price_sign(c, x, y, text, sub="DIESEL", s=1.0, col=RED, seed=10200):
    with at(c, x, y, s):
        shape(c, rrect_pts(-120, -70, 240, 140, 14, 14), NAVY, seed=seed, amp=0.4, lw=4)
        write(c, [(sub, hexc("#fbf3e1"))], 0, -30, 26, align="center", bold=True)
        shape(c, rrect_pts(-100, -14, 200, 70, 8, 12), hexc("#111318"), seed=seed + 1, amp=0.2, lw=0, stroke=None)
        write(c, [(text, col)], 0, 40, 52, align="center", bold=True)


def strait(c, x, y, t, s=1.0, blocked=1.0, seed=10300):
    """A narrow sea passage between two coasts, tankers queued outside."""
    with at(c, x, y, s):
        shape(c, rrect_pts(-240, -90, 480, 180, 18, 16), hexc("#7fb3e8"), seed=seed, amp=0.5, lw=4)
        shape(c, [(-240, -90), (240, -90), (240, -30), (40, -14), (-30, -40), (-240, -20)], hexc("#e8d9a8"),
              seed=seed + 1, amp=0.6, lw=4)
        shape(c, [(-240, 90), (240, 90), (240, 40), (60, 20), (-20, 40), (-240, 30)], hexc("#e8d9a8"),
              seed=seed + 2, amp=0.6, lw=4)
        for k in range(3):
            tx = -200 + k * 50 + 4 * math.sin(t * 2 + k)
            shape(c, [(tx - 20, -4), (tx + 20, -4), (tx + 14, 10), (tx - 14, 10)], hexc("#555a66"),
                  seed=seed + 3 + k, amp=0.3, lw=3)
        if blocked:
            line(c, [(10, -40), (40, 40)], 10 * blocked, RED, seed + 9, amp=0.3)
            line(c, [(40, -40), (10, 40)], 10 * blocked, RED, seed + 10, amp=0.3)
        write(c, [("Strait of Hormuz", INK)], 0, 78, 24, align="center", bold=True)


def calendar(c, x, y, top, big, s=1.0, seed=10400):
    with at(c, x, y, s):
        shape(c, rrect_pts(-90, -80, 180, 170, 14, 14), WHITE, seed=seed, amp=0.4, lw=4)
        shape(c, rrect_pts(-90, -80, 180, 44, 14, 14), RED, seed=seed + 1, amp=0.3, lw=4)
        write(c, [(top, WHITE)], 0, -48, 24, align="center", bold=True)
        write(c, [(big, INK)], 0, 50, 64, align="center", bold=True)


def tank(c, x, y, level=1.0, s=1.0, label=None, seed=10500):
    with at(c, x, y, s):
        shape(c, rrect_pts(-70, -90, 140, 180, 20, 14), WHITE, seed=seed, amp=0.4, lw=4)
        h = 170 * max(0.0, min(1.0, level))
        if h > 2:
            shape(c, rrect_pts(-64, 84 - h, 128, h, 14, 12), hexc("#3a6ea5"), seed=seed + 1, amp=0.3, lw=0, stroke=None)
        if label:
            write(c, [(label, RED)], 0, 0, 24, align="center", bold=True)


def hospital(c, x, y, s=1.0, seed=10600):
    with at(c, x, y, s):
        shape(c, rrect_pts(-110, -80, 220, 160, 8, 14), WHITE, seed=seed, amp=0.4, lw=4)
        shape(c, rrect_pts(-16, -66, 32, 60, 4, 10), RED, seed=seed + 1, amp=0.2, lw=0, stroke=None)
        shape(c, rrect_pts(-30, -52, 60, 32, 4, 10), RED, seed=seed + 2, amp=0.2, lw=0, stroke=None)
        for k in range(4):
            shape(c, rrect_pts(-90 + k * 48, 4, 32, 30, 4, 10), SKYB, seed=seed + 3 + k, amp=0.2, lw=3)
        shape(c, rrect_pts(-20, 44, 40, 36, 4, 10), hexc("#8e5a2e"), seed=seed + 8, amp=0.2, lw=3)


def biohazard_door(c, x, y, s=1.0, seed=10700):
    with at(c, x, y, s):
        shape(c, rrect_pts(-80, -100, 160, 200, 8, 14), STEEL, seed=seed, amp=0.4, lw=4)
        blob(c, 0, -20, 46, 46, GOLD, seed + 1, amp=0.3, lw=4)
        for k in range(3):
            a = -math.pi / 2 + k * 2 * math.pi / 3
            blob(c, 22 * math.cos(a), -20 + 22 * math.sin(a), 13, 13, INK, seed + 2 + k, amp=0.2, lw=0, stroke=None)
        dot(c, 0, -20, 8, GOLD)
        write(c, [("LAB", INK)], 0, 70, 30, align="center", bold=True)


def old_scroll(c, x, y, top, bottom, s=1.0, seed=10800):
    with at(c, x, y, s):
        shape(c, rrect_pts(-200, -70, 400, 140, 12, 14), hexc("#f4e4bc"), seed=seed, amp=0.6, lw=4)
        for sx in (-1, 1):
            blob(c, sx * 200, 0, 18, 76, hexc("#d9c08a"), seed + 1 + sx, amp=0.5, lw=4)
        write(c, [(top, INK)], 0, -8, 38, align="center", bold=True)
        write(c, [(bottom, hexc("#8a5a2a"))], 0, 40, 28, align="center")


def map_pin(c, x, y, label, s=1.0, seed=10900):
    with at(c, x, y, s):
        shape(c, rrect_pts(-220, -80, 440, 160, 18, 14), hexc("#e8efe2"), seed=seed, amp=0.5, lw=4)
        shape(c, [(-190, -40), (-60, -66), (80, -50), (190, -60), (200, 30), (60, 50), (-80, 40), (-200, 50)],
              hexc("#cfe3b8"), seed=seed + 1, amp=0.8, lw=3)
        shape(c, [(40, -20), (60, -50), (80, -20), (60, 10)], RED, seed=seed + 2, amp=0.2, lw=3)
        dot(c, 60, -30, 7, WHITE)
        write(c, [(label, INK)], 0, 64, 28, align="center", bold=True)


def binoculars(c, x, y, s=1.0, seed=11000):
    with at(c, x, y, s):
        for sx in (-1, 1):
            blob(c, sx * 34, 0, 30, 34, NAVY, seed + sx, amp=0.3, lw=4)
            blob(c, sx * 34, 6, 18, 20, SKYB, seed + 3 + sx, amp=0.2, lw=3)
        shape(c, rrect_pts(-14, -20, 28, 30, 4, 10), NAVY, seed=seed + 6, amp=0.2, lw=3)


def pill_bottle(c, x, y, s=1.0, seed=11100):
    with at(c, x, y, s):
        shape(c, rrect_pts(-46, -50, 92, 120, 12, 14), hexc("#f2a33a"), seed=seed, amp=0.4, lw=4)
        shape(c, rrect_pts(-54, -78, 108, 32, 8, 12), WHITE, seed=seed + 1, amp=0.3, lw=4)
        shape(c, rrect_pts(-36, -20, 72, 56, 4, 10), WHITE, seed=seed + 2, amp=0.3, lw=3)
        write(c, [("Rx", INK)], 0, 18, 30, align="center", bold=True)


def robotaxi(c, x, y, s=1.0, t=0.0, doors=0.0, seed=11200):
    """A generic two-seat driverless taxi (not a copy of any real car)."""
    with at(c, x, y, s):
        shape(c, [(-150, 30), (-140, -10), (-70, -60), (60, -64), (130, -16), (150, 30)], hexc("#c9ccd2"),
              seed=seed, amp=0.5, lw=4)
        shape(c, [(-60, -50), (50, -54), (100, -18), (-110, -14)], hexc("#3b3f4a"), seed=seed + 1, amp=0.3, lw=3)
        for wx in (-90, 90):
            blob(c, wx, 34, 26, 26, INK, seed + 2 + wx, amp=0.2, lw=0, stroke=None)
            dot(c, wx, 34, 10, GREY)
        if doors > 0:   # butterfly door swinging up
            u = ease_out(doors)
            with at(c, -10, -50, 1.0, rot=-1.1 * u):
                shape(c, [(0, 0), (90, 0), (80, 50), (0, 50)], hexc("#c9ccd2"), seed=seed + 5, amp=0.3, lw=4)


def no_wheel(c, x, y, s=1.0, seed=11300):
    """An empty driver's seat: the place where a steering wheel would be is crossed out."""
    with at(c, x, y, s):
        shape(c, rrect_pts(-60, -40, 90, 130, 18, 12), hexc("#3b3f4a"), seed=seed, amp=0.4, lw=4)
        blob(c, 100, -20, 46, 46, None, seed + 1, amp=0.3, lw=8, stroke=GREY)
        line(c, [(60, -60), (140, 20)], 9, RED, seed + 2, amp=0.2)
        line(c, [(140, -60), (60, 20)], 9, RED, seed + 3, amp=0.2)


def clock(c, x, y, s=1.0, t=0.0, seed=11400):
    with at(c, x, y, s):
        blob(c, 0, 0, 40, 40, WHITE, seed, amp=0.3, lw=4)
        line(c, [(0, 0), (0, -26)], 4, INK, seed + 1, amp=0.1)
        a = t * 3
        line(c, [(0, 0), (22 * math.sin(a), -22 * math.cos(a))], 4, RED, seed + 2, amp=0.1)


def wrong_pin(c, x, y, s=1.0, seed=11500):
    with at(c, x, y, s):
        shape(c, [(-20, -10), (0, -50), (20, -10), (0, 30)], RED, seed=seed, amp=0.2, lw=3)
        dot(c, 0, -20, 7, WHITE)
        write(c, [("?", INK)], 34, -14, 40, bold=True)


def open_trunk(c, x, y, s=1.0, seed=11600):
    with at(c, x, y, s):
        shape(c, rrect_pts(-50, -10, 100, 50, 8, 12), hexc("#c9ccd2"), seed=seed, amp=0.3, lw=4)
        with at(c, -50, -10, 1.0, rot=-0.7):
            shape(c, rrect_pts(0, -6, 100, 12, 4, 10), hexc("#c9ccd2"), seed=seed + 1, amp=0.2, lw=4)
        blob(c, 10, 6, 22, 16, hexc("#8e5a2e"), seed + 2, amp=0.3, lw=3)


def clipboard(c, x, y, title, s=1.0, seed=11700):
    with at(c, x, y, s):
        shape(c, rrect_pts(-110, -90, 220, 190, 10, 14), hexc("#b07a45"), seed=seed, amp=0.4, lw=4)
        shape(c, rrect_pts(-94, -70, 188, 160, 6, 12), WHITE, seed=seed + 1, amp=0.3, lw=3)
        shape(c, rrect_pts(-34, -100, 68, 26, 6, 10), GREY, seed=seed + 2, amp=0.2, lw=3)
        write(c, [(title, RED)], 0, -30, 26, align="center", bold=True)
        for k in range(3):
            line(c, [(-74, 4 + k * 26), (74, 4 + k * 26)], 3, GREY, seed + 3 + k, amp=0.4)


def fire_helmet(c, x, y, s=1.0, seed=11800):
    with at(c, x, y, s):
        shape(c, [(-80, 20), (-60, -30), (-20, -56), (30, -56), (66, -26), (86, 20)], RED, seed=seed, amp=0.4, lw=4)
        shape(c, rrect_pts(-96, 14, 200, 22, 10, 12), RED, seed=seed + 1, amp=0.3, lw=4)
        blob(c, 6, -18, 22, 20, GOLD, seed + 2, amp=0.3, lw=3)


def counter(c, x, y, a, b, u, s=1.0, col=GREEN, seed=11900):
    """A number that counts up from a to b as u goes 0 to 1."""
    with at(c, x, y, s):
        v = int(round(a + (b - a) * ease_out(u)))
        write(c, [(f"{v:,}", col)], 0, 30, 96, align="center", bold=True)


def bars(c, x, y, items, u=1.0, s=1.0, top=150, seed=12000):
    """Bar chart: items = [(label, value, colour, text)], tallest bar `top` px."""
    vmax = max(v for _, v, _, _ in items)
    n = len(items)
    with at(c, x, y, s):
        line(c, [(-60 * n - 20, 60), (60 * n + 20, 60)], 4, INK, seed, amp=0.3)
        for k, (label, v, col, text) in enumerate(items):
            bx = (k - (n - 1) / 2) * 130
            h = max(4, top * v / vmax * ease_out(u))
            shape(c, rrect_pts(bx - 40, 60 - h, 80, h, 6, 12), col, seed=seed + 1 + k, amp=0.3, lw=4)
            write(c, [(text, col)], bx, 50 - h - 10, 34, align="center", bold=True)
            write(c, [(label, INK)], bx, 92, 24, align="center", bold=True)


def gauge(c, x, y, text, u=1.0, s=1.0, seed=12100):
    with at(c, x, y, s):
        c.save()
        c.new_path()
        c.arc(0, 40, 110, math.pi, 2 * math.pi)
        c.set_line_width(26)
        c.set_source_rgba(*hexc("#e8e2d4"))
        c.stroke()
        c.restore()
        a = math.pi + math.pi * 0.42 * ease_out(u)
        line(c, [(0, 40), (90 * math.cos(a), 40 + 90 * math.sin(a))], 6, RED, seed, amp=0.1)
        dot(c, 0, 40, 10, INK)
        write(c, [(text, RED)], 0, 100, 48, align="center", bold=True)


def wallet(c, x, y, s=1.0, seed=12200):
    with at(c, x, y, s):
        shape(c, rrect_pts(-80, -50, 160, 100, 14, 14), hexc("#8e5a2e"), seed=seed, amp=0.4, lw=4)
        shape(c, rrect_pts(30, -20, 60, 40, 10, 10), hexc("#b07a45"), seed=seed + 1, amp=0.3, lw=3)
        shape(c, rrect_pts(-70, -72, 110, 40, 4, 10), hexc("#8fd18f"), seed=seed + 2, amp=0.3, lw=3)


def job_icon(c, kind, x, y, s=1.0, seed=12300):
    with at(c, x, y, s):
        if kind == "health":
            blob(c, 0, 0, 44, 44, WHITE, seed, amp=0.3, lw=4)
            shape(c, rrect_pts(-10, -30, 20, 60, 3, 10), RED, seed=seed + 1, amp=0.2, lw=0, stroke=None)
            shape(c, rrect_pts(-30, -10, 60, 20, 3, 10), RED, seed=seed + 2, amp=0.2, lw=0, stroke=None)
        elif kind == "build":
            shape(c, [(-46, 16), (-34, -22), (0, -38), (34, -22), (46, 16)], GOLD, seed=seed, amp=0.3, lw=4)
            shape(c, rrect_pts(-56, 10, 112, 16, 8, 10), GOLD, seed=seed + 1, amp=0.2, lw=4)
        elif kind == "factory":
            shape(c, [(-50, 40), (-50, -10), (-20, -30), (-20, -10), (10, -30), (10, -10), (50, -30), (50, 40)],
                  GREY, seed=seed, amp=0.3, lw=4)
            shape(c, rrect_pts(28, -60, 16, 40, 3, 10), GREY, seed=seed + 1, amp=0.2, lw=3)


def door(c, x, y, open_=0.3, s=1.0, seed=12400):
    with at(c, x, y, s):
        shape(c, rrect_pts(-60, -100, 120, 200, 6, 14), hexc("#3b3f4a"), seed=seed, amp=0.3, lw=4)
        w = 120 * (1 - 0.6 * open_)
        shape(c, rrect_pts(-60, -100, w, 200, 6, 14), hexc("#b07a45"), seed=seed + 1, amp=0.3, lw=4)
        dot(c, -60 + w - 14, 0, 6, GOLD)
