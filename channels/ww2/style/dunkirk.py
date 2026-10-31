"""WW2 style frame (script lines 46-48): Dunkirk, 8 s, 1920x1080.

    A side view down the beach: Dunkirk's skyline and three columns of oil smoke on the left horizon, a long packed
    line of British and French soldiers waiting on the sand (it recedes into the distance), a queue wading out to a
    fishing boat, and small boats of every kind crossing the bobbing Channel toward them, a destroyer offshore
    flashing a signal lamp.
    0.0-3.6  three RAF fighters cross overhead (left to right)
    1.0-6.8  the counter climbs to 338,226 "soldiers rescued"
    4.6-7.6  a second pair crosses back, higher
    the JUNE 1940 date tag sits in the corner throughout; a slow push-in toward the waterline over the shot

    /home/user/.venv-main/bin/python channels/ww2/style/dunkirk.py [--still T OUT.png]
Writes out/ww2/style/dunkirk.mp4 (and dunkirk_mid.png at 4.0 s).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from channels.ww2.kit.core import (H, ROOT, W, counter, date_stamp, lerp, paper, push_in,  # noqa: E402
                                   render_clip, seg, smooth)
from channels.ww2.kit import props as P  # noqa: E402
from channels.ww2.kit.stick import Figure  # noqa: E402

DUR = 8.0
HORIZON = 470
SAND, SAND_DK, DUNE = "#d8c48f", "#c6ae76", "#bfa772"
FOCUS = (1020, 640)                       # the push-in closes in on the waterline where the boats meet the beach


def shore_x(y):
    """x of the waterline at height y (the beach is left of it, the sea right); a gentle curve into the distance."""
    u = (y - HORIZON) / (H - HORIZON)
    return 600 + 560 * u ** 1.15


def depth_scale(y, near=0.36, far=0.06):
    """Size of a 300 px figure / a prop standing at height y (perspective from the horizon to the bottom edge)."""
    return lerp(far, near, ((y - HORIZON) / (H - HORIZON)) ** 1.1)


# ---------------------------------------------------------------- the people
def _soldiers():
    r = random.Random(46)
    people = []
    for i in range(330):                                         # the long line along the beach, 3-4 ranks deep
        u = (i / 330) ** 0.7
        y = lerp(HORIZON + 14, 1050, u ** 1.3)
        rank = r.randrange(4)
        x = shore_x(y) - lerp(30, 230, u) - rank * lerp(6, 46, u) + r.uniform(-4, 4)
        y += rank * lerp(1, 10, u)
        nation = "france" if r.random() < 0.22 else "britain"
        pose = r.choice(["idle", "idle", "idle", "stand", "head_down", "arms_crossed"])
        people.append(dict(x=x, y=y, nation=nation, pose=pose, off=r.uniform(0, 4), facing=1, wade=0.0, seed=i))
    for i in range(16):                                          # a queue wading out to the fishing boat
        u = i / 15
        y = lerp(738, 752, u) + r.uniform(-3, 3)
        x = shore_x(y) + 14 + u * 236
        people.append(dict(x=x, y=y, nation="britain", pose="idle", off=r.uniform(0, 4), facing=1,
                           wade=0.12 + smooth(u) * 0.5, seed=500 + i))
    for i in range(170):                                         # more men further up the beach, in loose groups
        u = r.random() ** 0.8
        y = lerp(HORIZON + 20, 1000, u)
        x = shore_x(y) - lerp(120, 900, u) * r.uniform(0.45, 1.0)
        people.append(dict(x=x, y=y, nation="france" if r.random() < 0.3 else "britain",
                           pose=r.choice(["idle", "stand", "head_down", "sit", "arms_crossed"]), off=r.uniform(0, 4),
                           facing=r.choice((1, -1)), wade=0.0, seed=900 + i))
    for i in range(10):                                          # front: a few wave at the boats
        y = r.uniform(990, 1075)
        x = shore_x(y) - r.uniform(40, 180)
        people.append(dict(x=x, y=y, nation="britain", pose=r.choice(["wave", "point", "idle"]),
                           off=r.uniform(0, 4), facing=1, wade=0.0, seed=700 + i))
    people.sort(key=lambda p: p["y"])
    for p in people:
        p["fig"] = Figure(nation=p["nation"], x=p["x"], y=p["y"], scale=depth_scale(p["y"]), facing=p["facing"],
                          prop="rifle" if p["seed"] % 5 == 0 else None, seed=p["seed"])
    return people


PEOPLE = _soldiers()


def draw_person(cr, t, p):
    p["fig"].draw(cr, t + p["off"], [(0.0, p["pose"])])
    if p["wade"] > 0:                                            # water over the legs, with a foam ring
        s = depth_scale(p["y"]) * 300
        top = p["y"] - s * p["wade"]
        cr.rectangle(p["x"] - s * 0.3, top, s * 0.6, p["y"] + 6 - top)
        P.fill(cr, "sea")
        P.ellipse(cr, p["x"], top, s * 0.2, s * 0.035)
        P.ink(cr, max(1.2, s * 0.012), "white", 0.9)


# ---------------------------------------------------------------- the boats
def _boats():
    B = []

    def add(cls, y, x0, x1, facing=-1, t0=0.0, **kw):
        B.append(dict(p=cls(scale=depth_scale(y, near=0.62, far=0.12), facing=facing, seed=len(B), side="britain"),
                      y=y, x0=x0, x1=x1, t0=t0, kw=kw))

    add(P.Destroyer, 486, 1560, 1470, speed=40, smoke=True)
    add(P.Yacht, 492, 1090, 980, sail=True, speed=40)
    add(P.FishingBoat, 498, 1280, 1150, speed=50)
    add(P.PaddleFerry, 512, 1790, 1560, speed=60)
    add(P.Yacht, 520, 980, 1110, facing=1, speed=60, crowd=4)          # a loaded one heading home
    add(P.FishingBoat, 548, 1500, 1310, speed=60)
    add(P.Yacht, 580, 1980, 1700, speed=70)
    add(P.FishingBoat, 600, 1120, 1260, facing=1, speed=60, crowd=6)
    add(P.Yacht, 640, 1430, 1180, sail=True, speed=70)
    add(P.FishingBoat, 690, 1900, 1580, speed=70)
    add(P.Yacht, 720, 1600, 1380, speed=60)
    add(P.Yacht, 860, 1500, 1320, facing=1, speed=60, crowd=5, sail=False)
    add(P.FishingBoat, 760, 1140, 1116, speed=8, crowd=3)              # the boat at the end of the wading queue
    add(P.PaddleFerry, 790, 2200, 1700, speed=80)
    add(P.Yacht, 905, 2100, 1640, speed=90)
    add(P.FishingBoat, 1010, 1950, 1490, speed=90)
    B.sort(key=lambda b: b["y"])
    return B


BOATS = _boats()


def draw_boat(cr, t, b):
    u = seg(t, 0, DUR)
    b["p"].draw(cr, t, x=lerp(b["x0"], b["x1"], u), y=b["y"], **b["kw"])


# ---------------------------------------------------------------- the world
def sky(cr, t):
    paper(cr)
    g = P.cairo.LinearGradient(0, 200, 0, HORIZON)
    g.add_color_stop_rgba(0, 0.55, 0.53, 0.49, 0.0)
    g.add_color_stop_rgba(1, 0.55, 0.53, 0.49, 0.16)
    cr.rectangle(0, 200, W, HORIZON - 196)
    cr.set_source(g)
    cr.fill()


def sea(cr, t):
    cr.rectangle(0, HORIZON, W, H - HORIZON)
    P.fill(cr, "sea")
    r = random.Random(5)
    for i in range(260):                                         # wave hatching, denser and finer toward the horizon
        v = r.random() ** 1.6
        y = HORIZON + 6 + v * (H - HORIZON)
        k = depth_scale(y, 1.0, 0.12)
        x = (r.uniform(-100, W + 100) - 18 * k * t) % (W + 200) - 100
        if x < shore_x(y) + 30:
            continue
        bob = math.sin(t * 2.2 + i) * 3 * k
        P.line(cr, x, y + bob, x + 60 * k, y + bob, max(1.2, 4 * k), "sea_dk", 0.9)
    P.line(cr, 0, HORIZON, W, HORIZON, 2.5, "ink_soft", 0.7)


def town(cr, t):
    """Dunkirk's skyline on the left horizon (roofs, the belfry, dockside cranes), hazy with distance."""
    r = random.Random(12)
    x = -10
    while x < 560:
        w = r.uniform(26, 60)
        h = r.uniform(18, 46)
        P.poly(cr, [(x, HORIZON), (x, HORIZON - h), (x + w / 2, HORIZON - h - r.uniform(6, 16)), (x + w, HORIZON - h),
                    (x + w, HORIZON)])
        P.fill(cr, "#8b8478", 0.85)
        x += w - 2
    P.poly(cr, [(300, HORIZON), (304, HORIZON - 110), (312, HORIZON - 132), (320, HORIZON - 110), (324, HORIZON)])
    P.fill(cr, "#7a7368")
    for cx in (470, 520):
        P.line(cr, cx, HORIZON, cx, HORIZON - 70, 3, "#7a7368")
        P.line(cr, cx - 10, HORIZON - 68, cx + 40, HORIZON - 78, 3, "#7a7368")


def beach(cr, t):
    pts = [(-20, HORIZON - 2)]
    for i in range(41):
        y = lerp(HORIZON, H + 10, i / 40)
        pts.append((shore_x(y), y))
    pts.append((-20, H + 10))
    P.poly(cr, pts)
    P.fill(cr, SAND)
    P.poly(cr, [(-20, HORIZON - 2), (600, HORIZON - 2), (560, HORIZON + 10), (-20, HORIZON + 30)])
    P.fill(cr, DUNE)
    r = random.Random(9)
    for i in range(70):                                          # sand ripples
        y = HORIZON + 30 + r.random() ** 1.3 * (H - HORIZON)
        x = r.uniform(0, shore_x(y) - 60)
        k = depth_scale(y, 1.0, 0.15)
        P.line(cr, x, y, x + 50 * k, y - 2 * k, max(1.0, 3 * k), SAND_DK, 0.8)
    for j in range(2):                                           # wet sand and the moving foam line
        pts = []
        for i in range(41):
            y = lerp(HORIZON + 2, H + 10, i / 40)
            k = depth_scale(y, 1.0, 0.1)
            pts.append((shore_x(y) + (8 + j * 22 + 10 * math.sin(t * 1.4 + i * 0.5 + j)) * k, y))
        P.poly(cr, pts, close=False)
        P.ink(cr, 3 + j * 2, "white" if j else "#b9a77c", 0.85 if j else 0.6)


def fighters(cr, t):
    for i, (dy, dx) in enumerate(((0, 0), (46, -120), (-40, -150))):
        u = seg(t, 0.0, 3.6)
        if 0 < u < 1:
            x = lerp(-260, W + 300, u) + dx
            P.Fighter(side="britain", seed=i).draw(cr, t, x=x, y=200 + dy + 6 * math.sin(t * 2 + i), scale=0.34,
                                                   bank=8 + 4 * math.sin(t * 1.5 + i), pitch=2)
    for i, (dy, dx) in enumerate(((0, 0), (30, 110))):
        u = seg(t, 4.6, 7.6)
        if 0 < u < 1:
            x = lerp(W + 220, -260, u) + dx
            P.Fighter(side="britain", seed=5 + i).draw(cr, t, x=x, y=130 + dy, scale=0.22, facing=-1, bank=12)


def scene(cr, t):
    sky(cr, t)
    for i, (sx, h) in enumerate(((150, 520), (340, 600), (520, 470))):   # oil-tank smoke behind the town
        P.smoke(cr, sx, HORIZON - 10, t + 3, height=h, width=110, dark=True, alpha=0.6, wind=0.42, rate=7,
                life=5.0, seed=20 + i)
    town(cr, t)
    sea(cr, t)
    beach(cr, t)
    people = iter(PEOPLE)
    pend = next(people, None)
    for b in BOATS:                                              # boats and people in depth order
        while pend is not None and pend["y"] <= b["y"]:
            draw_person(cr, t, pend)
            pend = next(people, None)
        draw_boat(cr, t, b)
        if isinstance(b["p"], P.Destroyer):                      # the destroyer's bridge lamp signals
            sc = b["p"].o["scale"]
            bx = lerp(b["x0"], b["x1"], seg(t, 0, DUR)) - 86 * sc
            P.signal_flash(cr, bx, b["y"] - 128 * sc, t, start=1.4, pattern=".-. . ... -.-. ..- .", unit=0.11,
                           size=9)
    while pend is not None:
        draw_person(cr, t, pend)
        pend = next(people, None)
    fighters(cr, t)


def draw(cr, t):
    z = push_in(t, 0, DUR, 1.0, 1.07)
    cr.save()
    fx, fy = FOCUS
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    scene(cr, t)
    cr.restore()
    counter(cr, t, 1.0, 6.8, 338226, W - 330, 200, size=118, label="soldiers rescued")
    date_stamp(cr, t, "JUNE 1940", start=-1.0)


if __name__ == "__main__":
    out = os.path.join(ROOT, "out", "ww2", "style")
    if "--still" in sys.argv:
        i = sys.argv.index("--still")
        render_clip(draw, DUR, sys.argv[i + 2], still=float(sys.argv[i + 1]))
    else:
        render_clip(draw, DUR, os.path.join(out, "dunkirk.mp4"))
        render_clip(draw, DUR, os.path.join(out, "dunkirk_mid.png"), still=4.0)
