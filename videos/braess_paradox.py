"""Paradox: "Braess's Paradox" — adding a road can make everyone's trip slower (Dietrich Braess, 1968).

Numbers are the standard textbook example: 4,000 drivers; each route = one narrow road (cars/100 minutes) + one
highway (always 45 minutes). Split evenly: 20 + 45 = 65 minutes. Add a free shortcut joining the two narrow roads:
everyone takes narrow-shortcut-narrow = 40 + 0 + 40 = 80 minutes, and either old route would now take 40 + 45 = 85,
so nobody switches back. Real-city examples are left out (they are disputed). Same structure as The Infinite Hotel.
"""
import math

from motion.captions import captions
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, text_width, write
from motion.kit import camera, hl, stamp, whip

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="b1", scene="city", text="A city builds a brand new road. And traffic gets worse. For everyone."),
    dict(id="b2", scene="map", text="Here's how. [Four thousand|4,000] drivers go from home to work. There are two "
                                    "routes: top and bottom."),
    dict(id="b3", scene="map", text="Each route has a narrow road, and a highway. The narrow road takes one minute for "
                                    "every hundred cars. The highway always takes [forty-five minutes.|45 minutes.]"),
    dict(id="b4", scene="map", text="So the drivers split in half. [Two thousand|2,000] cars per route. That's "
                                    "[twenty|20] minutes, plus [forty-five.|45.] Everyone arrives in "
                                    "[sixty-five minutes.|65 minutes.]"),
    dict(id="b5", scene="shortcut", text="Now the city adds a free shortcut, joining the two narrow roads."),
    dict(id="b6", scene="shortcut", text="Every driver switches to it, because it skips both highways."),
    dict(id="b7", scene="shortcut", text="But now all [four thousand|4,000] cars use both narrow roads. Each one takes "
                                         "[forty minutes.|40 minutes.] The whole trip takes "
                                         "[eighty minutes.|80 minutes.]"),
    dict(id="b8", scene="shortcut", text="And nobody can switch back. The old routes would now take [forty|40] plus "
                                         "[forty-five.|45.] That's [eighty-five.|85.]"),
    dict(id="b9", scene="name", text="It's called [Bress's|Braess's] paradox. Mathematician Dietrich "
                                     "[Bress|Braess] described it in [nineteen sixty-eight.|1968.]"),
    dict(id="b10", scene="end", text="So... would you take the shortcut?", pace=0.95),
]

METADATA = dict(
    title="A New Road Made Traffic WORSE… For Everyone 🚗🤯",
    alt_titles=["Why Adding a Road Can Slow Everyone Down (Braess's Paradox) 🚗",
                "More Roads = More Traffic?! The Braess Paradox 🤯"],
    description="""A city builds a brand new road… and traffic gets worse for everyone. 🚗

4,000 drivers, two routes. Each route has one narrow road (the more cars, the slower it gets) and one highway that always takes 45 minutes. Split in half, everyone arrives in 65 minutes.

Add a free shortcut between the two narrow roads and every driver takes it. Both narrow roads jam: now the trip takes 80 minutes, and nobody can switch back, because the old routes now take 85. 🤯

It's called Braess's paradox, described by mathematician Dietrich Braess in 1968.

💬 So… would you take the shortcut? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Paradox", "#Traffic", "#Math"],
    tags=["braess paradox", "braess's paradox", "traffic paradox", "game theory", "nash equilibrium", "math paradox",
          "paradox", "traffic", "mind blowing math", "interestingly strange"],
    pinned_comment="Be honest… would you take the shortcut? 🚗 (Everyone says no. Everyone takes it.) 👇",
)

GRASS, GRASS_D = hexc("#9fd28a"), hexc("#8cc278")
ROAD, ROAD_D = hexc("#5d6470"), hexc("#3f444d")
LANE = hexc("#f4efe1")
YEL = hexc("#ffd23f")
GREEN = hexc("#2e9e52")
CREAM = hexc("#fdf6e3")
CAR_COLS = [hexc(c) for c in ("#e0483d", "#3f6fb5", "#f2a93b", "#6f4fb0", "#2e9e8f", "#ff7aa8", "#f4efe1")]

HOME, WORK = (70, 600), (650, 600)
NA, NB = (360, 390), (360, 810)          # top junction / bottom junction
# road: (from, to, kind)   narrow roads jam; highways always take 45
ROADS = {"n1": (HOME, NA, "narrow"), "h1": (NA, WORK, "highway"),
         "h2": (HOME, NB, "highway"), "n2": (NB, WORK, "narrow"),
         "sc": (NA, NB, "shortcut")}
SEED = {"n1": 11, "h1": 23, "h2": 37, "n2": 41, "sc": 53}
LABEL_AT = {"n1": (165, 455), "h1": (560, 455), "h2": (165, 760), "n2": (560, 760), "sc": (470, 600)}


def bg(cr, t, keys, dur=0.3):
    cr.set_source_rgba(*GRASS)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=dur)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    for k in range(40):   # grass tufts
        x, y = (k * 137) % 900 - 90, (k * 263) % 1500 - 100
        line(cr, [(x - 8, y), (x - 4, y - 12)], 3, GRASS_D, seed=k, amp=0.2)
        line(cr, [(x + 2, y), (x + 4, y - 14)], 3, GRASS_D, seed=k + 50, amp=0.2)


def road(cr, key, grow=1.0, glow=None):
    (x0, y0), (x1, y1), kind = ROADS[key]
    x1, y1 = lerp(x0, x1, grow), lerp(y0, y1, grow)
    w = {"narrow": 30, "highway": 58, "shortcut": 30}[kind]
    if glow:
        line(cr, [(x0, y0), (x1, y1)], w + 30, glow, seed=SEED[key], amp=0.2)
    line(cr, [(x0, y0), (x1, y1)], w + 8, INK, seed=SEED[key], amp=0.2)
    line(cr, [(x0, y0), (x1, y1)], w, ROAD if kind != "shortcut" else hexc("#6d7480"), seed=SEED[key], amp=0.2)
    n = int(math.hypot(x1 - x0, y1 - y0) / 40)
    for k in range(n):   # lane dashes
        a, b = (k + 0.2) / max(n, 1), (k + 0.6) / max(n, 1)
        cr.move_to(lerp(x0, x1, a), lerp(y0, y1, a))
        cr.line_to(lerp(x0, x1, b), lerp(y0, y1, b))
    cr.set_source_rgba(*(LANE if kind == "highway" else YEL))
    cr.set_line_width(4 if kind == "highway" else 3)
    cr.stroke()


def car(cr, x, y, ang, col, s=1.0):
    with at(cr, x, y, s, rot=ang):
        shape(cr, rrect_pts(-15, -9, 30, 18, 6, 8), col, seed=7, amp=0.2, lw=2.5)
        shape(cr, rrect_pts(-6, -7, 12, 14, 3, 6), hexc("#cfe8f5"), seed=8, amp=0.1, lw=1.5)


def traffic(cr, t, key, n, speed, jam=False):
    """`n` cars flowing along road `key` at `speed` (fraction of the road per second)."""
    (x0, y0), (x1, y1), kind = ROADS[key]
    ang = math.atan2(y1 - y0, x1 - x0)
    nx, ny = -math.sin(ang), math.cos(ang)
    for k in range(n):
        u = (k / n + t * speed) % 1.0
        lane = ((k % 2) * 2 - 1) * (11 if kind == "highway" else 0)
        wob = math.sin(t * 9 + k) * 1.5 if jam else 0
        car(cr, lerp(x0, x1, u) + nx * lane + wob, lerp(y0, y1, u) + ny * lane, ang, CAR_COLS[(k * 3 + len(key)) % 7],
            0.85 if jam else 0.95)


def place(cr, x, y, kind, s=1.0):
    with at(cr, x, y, s):
        if kind == "home":
            shape(cr, rrect_pts(-46, -30, 92, 70, 6, 10), hexc("#f2a93b"), seed=9100, amp=0.4, lw=4)
            sharp_shape(cr, [(-58, -26), (0, -78), (58, -26)], hexc("#c0504d"), seed=9101, amp=0.4, lw=4)
            shape(cr, rrect_pts(-12, 6, 24, 34, 4, 6), hexc("#6d4524"), seed=9102, amp=0.2, lw=3)
            write(cr, [("HOME", INK)], 0, 78, 30, align="center", bold=True, halo=WHITE)
        else:
            shape(cr, rrect_pts(-42, -90, 84, 130, 6, 10), hexc("#7fa6c9"), seed=9200, amp=0.4, lw=4)
            for r in range(4):
                for c in range(2):
                    shape(cr, rrect_pts(-30 + c * 34, -78 + r * 28, 26, 18, 3, 6), hexc("#e8f4fb"), seed=9201 + r * 2 + c,
                          amp=0.1, lw=2)
            write(cr, [("WORK", INK)], 0, 78, 30, align="center", bold=True, halo=WHITE)


def badge(cr, x, y, text, col, s=1.0):
    with at(cr, x, y, s):
        w = text_width(cr, [(text, col)], 42, bold=True) + 44
        shape(cr, rrect_pts(-w / 2, -36, w, 72, 30, 12), INK, seed=9300, amp=0.3, lw=0, stroke=None)
        write(cr, [(text, col)], 0, 14, 42, align="center", bold=True)


def tag(cr, x, y, text, col, rot=0.0, size=30):
    with at(cr, x, y, 1.0, rot=rot):
        write(cr, [(text, col)], 0, 0, size, align="center", bold=True, halo=WHITE)


def world(cr, t, state, shortcut=0.0, glow=None):
    """state: 'split' (2,000 each way), 'jam' (all 4,000 on narrow-shortcut-narrow)."""
    glow = glow or {}
    for k in ("n1", "h1", "h2", "n2"):
        road(cr, k, glow=glow.get(k))
    if shortcut > 0:
        road(cr, "sc", grow=shortcut, glow=glow.get("sc"))
    if state == "split":
        for k in ("n1", "n2"):
            traffic(cr, t, k, 5, 0.30)
        for k in ("h1", "h2"):
            traffic(cr, t, k, 6, 0.14)
    elif state == "jam":
        for k in ("n1", "n2"):
            traffic(cr, t, k, 12, 0.07, jam=True)
        traffic(cr, t, "sc", 6, 0.5)
    place(cr, *HOME, "home")
    place(cr, *WORK, "work")
    for p in (NA, NB):
        blob(cr, p[0], p[1], 22, 22, ROAD_D, seed=9400 + p[1], amp=0.3, lw=4)


def scene_city(cr, t, tl):
    A = tl.at
    keys = [(0, (1.05, 360, 600)), (A("b1", "new"), (1.3, 360, 600)), (A("b1", "worse."), (1.0, 360, 620)),
            (A("b1", "everyone."), (1.2, 360, 600))]
    bg(cr, t, keys)
    built = ease_out(seg(t, A("b1", "new"), A("b1", "road.", end=True)))
    state = "jam" if t >= A("b1", "worse.") else "split"
    world(cr, t, state, shortcut=built, glow={"sc": hexc("#ffd23f", 0.6)} if t < A("b1", "worse.") else
          {"n1": hexc("#e0483d", 0.45), "n2": hexc("#e0483d", 0.45)})
    if A("b1", "new") <= t < A("b1", "worse."):
        tag(cr, 470, 560, "NEW", hexc("#e0483d"), rot=-0.1, size=40)
        tag(cr, 470, 610, "ROAD!", hexc("#e0483d"), rot=-0.1, size=40)
    if t >= A("b1", "worse."):
        with at(cr, 360, 1010, max(0.85, pop(t, A("b1", "worse."), 0.25))):
            badge(cr, 0, 0, "TRAFFIC: WORSE", hexc("#ff6b5e"))
    hl(cr, t, [("NEW", GREEN), (" road = ", INK), ("MORE", RED), (" traffic?!", INK)], 200, 50, 0.0, bold=True,
       sound=False)
    cue("hit", t, A("b1", "worse."))
    stamp(cr, t, A("b1", "everyone."), "EVERYONE!", dur=0.6, y=330)


def scene_map(cr, t, tl):
    A = tl.at
    keys = [(A("b2") - 0.2, (1.25, 120, 600)), (A("b2", "work."), (1.0, 360, 600)), (A("b2", "two"), (1.05, 360, 600)),
            (A("b3", "narrow"), (1.15, 320, 560)), (A("b3", "always"), (1.15, 400, 560)),
            (A("b4"), (1.0, 360, 600)), (A("b4", "65"), (1.05, 360, 620))]
    bg(cr, t, keys)
    glow = {}
    if A("b2", "two") <= t < A("b3"):
        glow = {"n1": hexc("#ffd23f", 0.55), "h1": hexc("#ffd23f", 0.55), "h2": hexc("#7fd1ff", 0.55),
                "n2": hexc("#7fd1ff", 0.55)}
    elif A("b3", "narrow") <= t < A("b3", "always"):
        glow = {"n1": hexc("#e0483d", 0.45), "n2": hexc("#e0483d", 0.45)}
    elif A("b3", "always") <= t < A("b4"):
        glow = {"h1": hexc("#2e9e52", 0.45), "h2": hexc("#2e9e52", 0.45)}
    world(cr, t, "split" if t >= A("b2", "four") else "none", glow=glow)
    if A("b2", "four") <= t < A("b3"):
        with at(cr, 360, 1010, max(0.85, pop(t, A("b2", "four"), 0.25))):
            badge(cr, 0, 0, "4,000 DRIVERS", YEL)
    if A("b2", "two") <= t < A("b3"):
        tag(cr, 300, 300, "TOP", hexc("#b9862a"), size=44)
        tag(cr, 300, 900, "BOTTOM", hexc("#2f7fb5"), size=44)
    if A("b3", "narrow") <= t < A("b4", "20"):
        tag(cr, *LABEL_AT["n1"], "NARROW", RED, rot=-0.6)
        tag(cr, *LABEL_AT["n2"], "NARROW", RED, rot=-0.6)
    if A("b3", "always") <= t:
        tag(cr, *LABEL_AT["h1"], "45 min", GREEN, rot=0.6, size=36)
        tag(cr, *LABEL_AT["h2"], "45 min", GREEN, rot=0.6, size=36)
    if A("b3", "minute") <= t < A("b3", "always"):
        with at(cr, 360, 600, max(0.85, pop(t, A("b3", "minute"), 0.25))):
            badge(cr, 0, 0, "1 min per 100 cars", hexc("#ff6b5e"))
    if t >= A("b4", "split"):
        tag(cr, 230, 330, "2,000", hexc("#b9862a"), size=40)
        tag(cr, 230, 880, "2,000", hexc("#2f7fb5"), size=40)
    if t >= A("b4", "20"):
        tag(cr, *LABEL_AT["n1"], "20 min", RED, rot=-0.6, size=36)
        tag(cr, *LABEL_AT["n2"], "20 min", RED, rot=-0.6, size=36)
    if t >= A("b4", "65"):
        with at(cr, 360, 1010, max(0.85, pop(t, A("b4", "65"), 0.25))):
            badge(cr, 0, 0, "20 + 45 = 65 min", hexc("#7ee08a"))
    hl(cr, t, [("4,000", RED), (" drivers", INK)], 200, 64, A("b2", "four"), end=A("b2", "two") - 0.05, bold=True)
    hl(cr, t, [("TWO", RED), (" routes", INK)], 200, 64, A("b2", "two"), end=A("b3", "narrow") - 0.05, bold=True)
    hl(cr, t, [("narrow: ", INK), ("1 min per 100 cars", RED)], 200, 48, A("b3", "narrow"), end=A("b3", "always") - 0.05,
       bold=True)
    hl(cr, t, [("highway: always ", INK), ("45", GREEN)], 200, 60, A("b3", "always"), end=A("b4") - 0.05, bold=True)
    hl(cr, t, [("2,000", RED), (" cars per route", INK)], 200, 58, A("b4", "split"), end=A("b4", "65") - 0.05, bold=True)
    hl(cr, t, [("everyone: ", INK), ("65 min", GREEN)], 200, 64, A("b4", "65"), bold=True, underline=True)


def scene_shortcut(cr, t, tl):
    A = tl.at
    keys = [(A("b5") - 0.2, (1.0, 360, 600)), (A("b5", "shortcut,"), (1.4, 360, 600)), (A("b6"), (1.05, 360, 600)),
            (A("b7"), (1.0, 360, 600)), (A("b7", "both"), (1.1, 360, 580)), (A("b7", "80"), (1.0, 360, 620)),
            (A("b8"), (1.0, 360, 620)), (A("b8", "85."), (1.05, 360, 620))]
    bg(cr, t, keys)
    built = ease_out(seg(t, A("b5", "adds"), A("b5", "shortcut,", end=True) + 0.2))
    jam = t >= A("b7")
    glow = {"sc": hexc("#ffd23f", 0.6)} if not jam else {"n1": hexc("#e0483d", 0.45), "n2": hexc("#e0483d", 0.45),
                                                         "sc": hexc("#e0483d", 0.3)}
    if A("b6") <= t < A("b7"):     # the tempting new path: narrow, shortcut, narrow
        glow = {k: hexc("#ffd23f", 0.75) for k in ("n1", "sc", "n2")}
    if t >= A("b8", "old"):
        glow.update({"h1": hexc("#9aa0a8", 0.5), "h2": hexc("#9aa0a8", 0.5)})
    world(cr, t, "jam" if jam else "split", shortcut=built, glow=glow)
    if A("b5", "free") <= t:
        tag(cr, *LABEL_AT["sc"], "0 min", hexc("#b9862a"), size=40)
    if t >= A("b7", "40"):
        tag(cr, *LABEL_AT["n1"], "40 min", RED, rot=-0.6, size=36)
        tag(cr, *LABEL_AT["n2"], "40 min", RED, rot=-0.6, size=36)
    if A("b7", "80") <= t < A("b8", "old"):
        with at(cr, 360, 1010, max(0.85, pop(t, A("b7", "80"), 0.25))):
            badge(cr, 0, 0, "40 + 0 + 40 = 80 min", hexc("#ff6b5e"))
    if t >= A("b8", "old"):
        with at(cr, 360, 1010, max(0.85, pop(t, A("b8", "old"), 0.25))):
            badge(cr, 0, 0, "old route: 40 + 45 = 85", hexc("#ff6b5e"))
        for k in ("h1", "h2"):
            x, y = LABEL_AT[k]
            line(cr, [(x - 30, y - 30), (x + 30, y + 30)], 9, RED, seed=9500, amp=0.3)
            line(cr, [(x + 30, y - 30), (x - 30, y + 30)], 9, RED, seed=9501, amp=0.3)
    hl(cr, t, [("a ", INK), ("FREE", GREEN), (" shortcut", INK)], 200, 64, A("b5", "free"), end=A("b6") - 0.05, bold=True)
    hl(cr, t, [("skips both ", INK), ("HIGHWAYS", GREEN)], 200, 60, A("b6"), end=A("b7") - 0.05, bold=True)
    hl(cr, t, [("4,000", RED), (" on narrow roads", INK)], 200, 54, A("b7"), end=A("b7", "80") - 0.05, bold=True)
    hl(cr, t, [("was ", INK), ("65", GREEN), (", now ", INK), ("80", RED)], 200, 64, A("b7", "80"),
       end=A("b8") - 0.05, bold=True)
    hl(cr, t, [("NOBODY", RED), (" can switch back", INK)], 200, 56, A("b8"), bold=True)
    cue("hit", t, A("b7", "80"))


def scene_name(cr, t, tl):
    A = tl.at
    keys = [(A("b9") - 0.2, (1.0, 360, 620)), (A("b9", "paradox."), (1.15, 360, 560)), (A("b9", "dietrich"), (1.0, 360, 620))]
    bg(cr, t, keys)
    world(cr, t, "jam", shortcut=1.0)
    with at(cr, 360, 420, max(0.85, pop(t, A("b9"), 0.3)), rot=-0.03):
        shape(cr, rrect_pts(-260, -90, 520, 180, 18, 14), CREAM, seed=9600, amp=0.5, lw=5)
        write(cr, [("BRAESS'S", INK)], 0, -14, 58, align="center", bold=True)
        write(cr, [("PARADOX", RED)], 0, 56, 66, align="center", bold=True)
    if t >= A("b9", "dietrich"):
        with at(cr, 360, 1010, max(0.85, pop(t, A("b9", "dietrich"), 0.25))):
            badge(cr, 0, 0, "Dietrich Braess, 1968", YEL)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("b10") - 0.2, (1.05, 360, 600)), (A("b10", "shortcut?"), (1.3, 360, 600))]
    bg(cr, t, keys)
    world(cr, t, "jam", shortcut=1.0, glow={"sc": hexc("#ffd23f", 0.5 + 0.3 * math.sin(t * 6))})
    for k, (lab, col, x) in enumerate((("YES", GREEN, 200), ("NO", hexc("#e0483d"), 520))):
        if t >= A("b10", "shortcut?"):
            with at(cr, x, 1030, max(0.85, pop(t, A("b10", "shortcut?") + k * 0.12, 0.25))):
                shape(cr, rrect_pts(-110, -46, 220, 92, 46, 14), col, seed=9700 + k, amp=0.3, lw=4)
                write(cr, [(lab, WHITE)], 0, 16, 48, align="center", bold=True)
    hl(cr, t, [("would you take the ", INK), ("SHORTCUT", RED), ("?", INK)], 200, 44, A("b10"), bold=True, underline=True)
    stamp(cr, t, A("b10", "shortcut?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"city": scene_city, "map": scene_map, "shortcut": scene_shortcut, "name": scene_name,
     "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
