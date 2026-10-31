"""WW2 style frame (script lines 46-48): Dunkirk as an animated 1940s poster, 8 s, 1920x1080.

    A low horizon under a smoky khaki sky: black oil smoke billows from Dunkirk's skyline across a slow sunburst.
    On the sand, a long line of soldiers in one-tone poster silhouette waits, receding into the haze; a queue wades
    out to a fishing boat. Small boats of every kind cross the hatched Channel toward them in silhouette, and a
    destroyer offshore flashes its signal lamp.
    0.0-3.4  three RAF fighters cross overhead (left to right); 4.6-7.6 a second pair crosses back, higher
    1.0-6.8  the counter climbs to 338,226 "soldiers rescued"
    the JUNE 1940 date tag sits in the corner throughout; a slow push-in toward the waterline; print_finish last
    Sound: surf and gulls under distant engines; aircraft pass at 0.4 and 4.8; a lamp click on each flash.

    /home/user/.venv-main/bin/python channels/ww2/style/dunkirk.py [--still T OUT.png]
Writes out/ww2/style/dunkirk.mp4 (and dunkirk_mid.png at 4.0 s).
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from channels.ww2.kit.core import (H, ROOT, STENCIL, TITLE, W, date_stamp, ease_out, lerp, paper,  # noqa: E402
                                   print_finish, push_in, rays, render_clip, seg, smooth, text)
from channels.ww2.kit import props as P  # noqa: E402

DUR = 8.0
HORIZON = 640
FOCUS = (1000, 760)                        # the push-in closes in on the waterline where the boats meet the beach
SAND, SAND_DK = "#d7c08b", "#b59d68"


def shore_x(y):
    """x of the waterline at height y (beach to the left, sea to the right)."""
    u = (y - HORIZON) / (H - HORIZON)
    return 640 + 520 * u ** 1.1


def depth(y):
    """0 at the horizon, 1 at the bottom edge."""
    return max(0.0, (y - HORIZON) / (H - HORIZON))


def tone(y):
    """Silhouette ink by distance: hazy khaki-grey far away, solid ink close up (poster depth layers)."""
    return P.mix("#7d7766", "ink", min(1.0, depth(y) ** 0.6 * 1.15))


# ---------------------------------------------------------------- poster soldier silhouettes
def soldier(cr, x, y, h, t, seed, color, pose="idle", rim=False):
    """A one-tone poster soldier, h px tall, standing on (x, y): dish helmet, greatcoat, pack, maybe a rifle."""
    r = random.Random(seed)
    sway = math.sin(t * (0.9 + r.random() * 0.5) + seed) * h * 0.012
    breathe = 1 + 0.012 * math.sin(t * 2.2 + seed)
    k = h / 100.0
    cr.save()
    cr.translate(x + sway, y)
    cr.scale(k, k * breathe)
    lean = r.uniform(-0.04, 0.06) + (0.12 if pose == "tired" else 0)
    stance = r.uniform(5, 9)
    for sx in (-1, 1):                                                          # legs, puttees and boots
        P.poly(cr, [(sx * stance - 6, 0), (sx * stance + 7, 0), (sx * stance + 5, -5), (sx * 2 + 5, -50),
                    (sx * 2 - 5, -50), (sx * stance - 5, -5)])
    cr.rotate(lean)
    P.poly(cr, [(-16, -34), (16, -34), (11, -80), (-11, -80)])                  # greatcoat to the knee
    P.rrect(cr, -17 if seed % 2 else 6, -78, 11, 22, 3)                          # pack
    if seed % 3 == 0:                                                           # rifle slung on the shoulder
        P.poly(cr, [(4, -94), (7, -95), (-4, -30), (-7, -30)])
    cr.new_sub_path()
    cr.arc(0, -87, 8, 0, math.tau)                                              # head
    tilt = -0.25 if pose == "tired" else r.uniform(-0.08, 0.08)
    cr.save()
    cr.translate(0, -92)
    cr.rotate(tilt)
    P.ellipse(cr, 0, 0, 14, 3.4)                                                # dish helmet brim
    cr.new_sub_path()
    cr.arc(0, -1, 9, math.pi, math.tau)
    cr.restore()
    if pose == "wave":                                          # a bent-arm wave (never a straight raised arm)
        hx = 20 + 7 * math.sin(t * 7 + seed)
        P.poly(cr, [(7, -78), (24, -90), (27, -84), (11, -72)])                  # upper arm out to the elbow
        P.poly(cr, [(22, -88), (hx - 3, -110), (hx + 4, -110), (28, -86)])       # forearm up, hand waving
        cr.new_sub_path()
        cr.arc(hx, -112, 4.5, 0, math.tau)
        P.poly(cr, [(-12, -76), (-15, -50), (-11, -50), (-8, -76)])
    else:
        P.poly(cr, [(-14, -78), (-19, -46), (-12, -46), (-7, -76)])
        P.poly(cr, [(14, -78), (19, -46), (12, -46), (7, -76)])
    P.fill(cr, color)
    if rim:                                                                     # a cream catch-light on the helmet
        cr.save()
        cr.translate(0, -92)
        cr.rotate(tilt)
        cr.new_path()
        cr.arc(0, -1, 7.5, math.pi * 1.15, math.pi * 1.4)
        P.ink(cr, 1.6, "cream", 0.85)
        cr.restore()
    cr.restore()


def _people():
    r = random.Random(46)
    out = []
    for i in range(300):                                         # the long line, 3-4 ranks deep, into the haze
        u = (i / 300) ** 0.75
        y = lerp(HORIZON + 6, 1060, u ** 1.25)
        rank = r.randrange(4)
        x = shore_x(y) - lerp(26, 240, u) - rank * lerp(5, 44, u) + r.uniform(-3, 3)
        y += rank * lerp(1, 9, u)
        out.append(dict(x=x, y=y, pose="tired" if r.random() < 0.2 else "idle", seed=i, wade=0.0))
    for i in range(14):                                          # the queue wading out to the fishing boat
        u = i / 13
        y = lerp(808, 822, u) + r.uniform(-2, 2)
        out.append(dict(x=shore_x(y) + 16 + u * 230, y=y, pose="idle", seed=400 + i, wade=0.15 + 0.5 * smooth(u)))
    for i in range(120):                                         # loose groups further up the beach
        u = r.random() ** 0.8
        y = lerp(HORIZON + 10, 1000, u)
        out.append(dict(x=shore_x(y) - lerp(160, 900, u) * r.uniform(0.45, 1.0), y=y,
                        pose=r.choice(["idle", "tired", "idle"]), seed=600 + i, wade=0.0))
    for i in range(8):                                           # the front few wave at the boats
        y = r.uniform(1010, 1085)
        out.append(dict(x=shore_x(y) - r.uniform(30, 170), y=y, pose=r.choice(["wave", "idle"]), seed=800 + i,
                        wade=0.0))
    out.sort(key=lambda p: p["y"])
    return out


PEOPLE = _people()


def draw_person(cr, t, p):
    h = lerp(16, 150, depth(p["y"]) ** 1.05)
    c = tone(p["y"])
    soldier(cr, p["x"], p["y"], h, t, p["seed"], c, p["pose"], rim=h > 115)
    if p["wade"] > 0:                                            # flat water over the legs + a cream foam bar
        top = p["y"] - h * p["wade"]
        cr.rectangle(p["x"] - h * 0.22, top, h * 0.44, p["y"] + 4 - top)
        P.fill(cr, "sea")
        P.line(cr, p["x"] - h * 0.18, top, p["x"] + h * 0.18, top, max(1.5, h * 0.03), "cream")


# ---------------------------------------------------------------- the boats (silhouettes)
def _boats():
    B = []

    def add(cls, y, x0, x1, facing=-1, **kw):
        s = lerp(0.1, 0.62, depth(y) ** 1.05)
        B.append(dict(p=cls(scale=s, facing=facing, seed=len(B), side="britain"), y=y, x0=x0, x1=x1, kw=kw))

    add(P.Destroyer, 650, 1640, 1560, speed=40)
    add(P.Yacht, 654, 1000, 920, sail=True, speed=40)
    add(P.FishingBoat, 660, 1250, 1150, speed=50)
    add(P.PaddleFerry, 670, 1860, 1660, speed=60)
    add(P.Yacht, 676, 900, 1010, facing=1, speed=60, crowd=4)
    add(P.FishingBoat, 696, 1520, 1340, speed=60)
    add(P.Yacht, 720, 2000, 1740, speed=70)
    add(P.FishingBoat, 735, 1120, 1240, facing=1, speed=60, crowd=6)
    add(P.Yacht, 760, 1460, 1220, sail=True, speed=70)
    add(P.FishingBoat, 790, 1960, 1650, speed=70)
    add(P.FishingBoat, 826, 1160, 1140, speed=8, crowd=3)       # the boat at the end of the wading queue
    add(P.Yacht, 845, 1640, 1420, speed=60)
    add(P.PaddleFerry, 880, 2240, 1760, speed=80)
    add(P.Yacht, 950, 1560, 1360, facing=1, speed=60, crowd=5)
    add(P.FishingBoat, 1040, 2000, 1560, speed=90)
    B.sort(key=lambda b: b["y"])
    return B


BOATS = _boats()


def draw_boat(cr, t, b):
    x = lerp(b["x0"], b["x1"], seg(t, 0, DUR))
    b["p"].draw(cr, t, x=x, y=b["y"], silhouette=tone(b["y"]), water="sea", **b["kw"])
    if isinstance(b["p"], P.Destroyer):                          # the bridge lamp signals (cream on the silhouette)
        sc = b["p"].o["scale"]
        P.signal_flash(cr, x - 86 * sc, b["y"] - 128 * sc, t, start=1.4, pattern=".-. . ... -.-. ..- .",
                       unit=0.11, size=8, color="cream")


# ---------------------------------------------------------------- the world
def sky(cr, t):
    paper(cr)
    cr.rectangle(0, 0, W, HORIZON)
    P.fill(cr, "sky", 0.55)
    rays(cr, t, 1180, HORIZON, n=30, color="khaki", alpha=0.28, spin=0.02)
    P.smoke(cr, 560, HORIZON + 30, t + 1, height=440, width=48, color="#9a917a", alpha=1.0, wind=1.4, rate=6,
            life=4.5, seed=31)
    for i, (sx, h, wdt) in enumerate(((120, 760, 72), (330, 840, 84), (520, 700, 64))):   # oil smoke (sources
        P.smoke(cr, sx, HORIZON + 40, t + 3, height=h, width=wdt, dark=True, alpha=1.0, wind=0.9, rate=8,   # hide
                life=6.0, seed=20 + i)                                                                   # behind town)


def town(cr, t):
    """Dunkirk's skyline on the left horizon (roofs, the belfry, dockside cranes) in one hazy tone."""
    r = random.Random(12)
    c = "#5c564b"
    x = -10
    while x < 600:
        w = r.uniform(26, 60)
        h = r.uniform(18, 44)
        P.poly(cr, [(x, HORIZON), (x, HORIZON - h), (x + w / 2, HORIZON - h - r.uniform(6, 16)), (x + w, HORIZON - h),
                    (x + w, HORIZON)])
        P.fill(cr, c)
        x += w - 2
    P.poly(cr, [(300, HORIZON), (304, HORIZON - 120), (312, HORIZON - 144), (320, HORIZON - 120), (324, HORIZON)])
    P.fill(cr, c)
    for cx in (480, 540):
        P.line(cr, cx, HORIZON, cx, HORIZON - 80, 4, c)
        P.line(cr, cx - 10, HORIZON - 78, cx + 44, HORIZON - 88, 4, c)
    text(cr, "DUNKIRK", 300, HORIZON - 170, 30, font=STENCIL, color="cream", outline="ink", outline_w=5, spacing=4)


def sea(cr, t):
    cr.rectangle(0, HORIZON, W, H - HORIZON)
    P.fill(cr, "sea")
    y = HORIZON + 4.0
    i = 0
    while y < H:                                                 # printed hatching, tighter toward the horizon
        k = depth(y)
        off = (t * (8 + 30 * k) + i * 37) % 80
        cr.set_dash([40 + 160 * k, 14 + 40 * k], -off)
        P.line(cr, shore_x(y) + 20, y, W + 20, y, max(1.2, 3.2 * k + 0.8), "sea_dk", 0.9)
        cr.set_dash([])
        y += 5 + 26 * k
        i += 1
    P.line(cr, 0, HORIZON, W, HORIZON, 3, "ink")


def beach(cr, t):
    pts = [(-20, HORIZON)]
    for i in range(41):
        y = lerp(HORIZON, H + 10, i / 40)
        pts.append((shore_x(y), y))
    pts.append((-20, H + 10))
    P.poly(cr, pts)
    P.fill(cr, SAND)
    P.poly(cr, pts)
    P.dots(cr, SAND_DK, 1, 0.7, below=HORIZON + 140)
    cr.new_path()
    for j in range(2):                                           # wet sand and the moving cream foam line
        pts = []
        for i in range(41):
            y = lerp(HORIZON + 2, H + 10, i / 40)
            k = depth(y) + 0.1
            pts.append((shore_x(y) + (6 + j * 20 + 9 * math.sin(t * 1.4 + i * 0.5 + j)) * k, y))
        P.poly(cr, pts, close=False)
        P.ink(cr, 3 + j * 3, "cream" if j else SAND_DK, 1.0)


def fighters(cr, t):
    for i, (dy, dx) in enumerate(((0, 0), (52, -130), (-44, -160))):
        u = seg(t, 0.0, 3.4)
        if 0 < u < 1:
            P.Fighter(side="britain", seed=i).draw(cr, t, x=lerp(-260, W + 320, u) + dx,
                                                   y=250 + dy + 6 * math.sin(t * 2 + i), scale=0.4,
                                                   bank=10 + 4 * math.sin(t * 1.5 + i), pitch=2)
    for i, (dy, dx) in enumerate(((0, 0), (34, 120))):
        u = seg(t, 4.6, 7.6)
        if 0 < u < 1:
            P.Fighter(side="britain", seed=5 + i).draw(cr, t, x=lerp(W + 240, -280, u) + dx, y=150 + dy, scale=0.26,
                                                       facing=-1, bank=14)


def scene(cr, t):
    sky(cr, t)
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
    while pend is not None:
        draw_person(cr, t, pend)
        pend = next(people, None)
    fighters(cr, t)


def tally(cr, t):
    """The rescue counter as a poster panel: a big cream number with an ink key line on a red band."""
    if t < 1.0:
        return
    pop = P.back_out(seg(t, 1.0, 1.3))
    if pop < 0.01:
        return
    v = 338226 * ease_out(seg(t, 1.0, 6.8))
    cr.save()
    cr.translate(W - 330, 190)
    cr.scale(pop, pop)
    cr.rotate(-0.03)
    P.poly(cr, [(-250, 40), (250, 34), (244, 92), (-244, 96)])
    P.fill_ink(cr, "alert", 5, tone=False)
    text(cr, f"{v:,.0f}", 0, 22, 140, font=TITLE, color="cream", bold=False, outline="ink", outline_w=12)
    text(cr, "SOLDIERS RESCUED", 0, 80, 38, font=STENCIL, color="cream", spacing=4)
    cr.restore()


def draw(cr, t):
    z = push_in(t, 0, DUR, 1.0, 1.07)
    cr.save()
    fx, fy = FOCUS
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    scene(cr, t)
    cr.restore()
    tally(cr, t)
    date_stamp(cr, t, "JUNE 1940", start=-1.0)
    print_finish(cr, t)


if __name__ == "__main__":
    out = os.path.join(ROOT, "out", "ww2", "style")
    if "--still" in sys.argv:
        i = sys.argv.index("--still")
        render_clip(draw, DUR, sys.argv[i + 2], still=float(sys.argv[i + 1]))
    else:
        render_clip(draw, DUR, os.path.join(out, "dunkirk.mp4"))
        render_clip(draw, DUR, os.path.join(out, "dunkirk_mid.png"), still=4.0)
