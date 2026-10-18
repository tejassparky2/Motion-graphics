"""This Circle Is a Square -- taxicab geometry, in the polished look.

Script: out/scripts_batch_oct26-31.md, row 64 (owner approved 18 Oct 2026); the idea came from the God-rock comment
thread (_mr._fool_ asked whether a circle can be a square). In taxicab (Manhattan) geometry distance is |dx| + |dy|
along a street grid, so the "circle" of all points 3 blocks from a centre is a square standing on its corner (a
diamond). Closing debate: did we cheat by changing what distance means, or is it really a circle? Turbo stock female
narrator with tags.
"""
import math

from motion import thriller as th
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, enter, lin, paint, rad, rrect,
                           shade, sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 1.0

SCRIPT = [
    dict(id="c1", scene="hook", text="A taxi driver draws a perfect circle. And it comes out as a square."),
    dict(id="c2", scene="rule", text="A circle is every point at the same distance from the middle. That's the rule."),
    dict(id="c3", scene="streets", text="But a taxi can't fly over buildings. It can only drive along the streets. "
                                        "Up, down, left and right."),
    dict(id="c4", scene="streets", text="So for a taxi, distance means blocks driven."),
    dict(id="c5", scene="grid", text="Now mark every corner exactly three blocks from the taxi stand."),
    dict(id="c6", scene="grid", text="Three blocks up. Three blocks right. Two right and one up. One right and two "
                                     "up."),
    dict(id="c7", scene="grid", text="Go all the way round, and join the dots."),
    dict(id="c8", scene="grid", text="It's a square. Standing on its corner. [gasp]"),
    dict(id="c9", scene="grid", text="And for the taxi, it's a perfect circle. Every point is three blocks from the "
                                     "middle."),
    dict(id="c10", scene="named", text="It's real maths. It's called taxicab geometry."),
    dict(id="c11", scene="comment", text="One of you asked in the comments if a circle can be a square. Here's your "
                                         "answer. [chuckle]"),
    dict(id="c12", scene="end", text="So did we cheat by changing what distance means? Or is it really a circle?",
         gap=0.3),
]

METADATA = dict(
    title="This Circle Is a Square. Really. ⬜",
    alt_titles=["A Taxi Driver Drew a Circle. It Came Out Square ⬜🚕", "The Circle That's Actually a Square 🤯"],
    description="""A taxi driver draws a perfect circle... and it comes out as a square. ⬜🚕

A circle is every point at the same distance from the middle. But a taxi can't fly over buildings: it can only drive along the streets, so for a taxi, distance means blocks driven. Mark every corner exactly 3 blocks from the taxi stand, join the dots... and you get a square standing on its corner. For the taxi, it's a perfect circle.

It's real maths: taxicab geometry.

One of you asked in the comments if a circle can be a square. Here's your answer. 😏

💬 Did we cheat by changing what "distance" means, or is it really a circle? 👇

🔔 Interestingly Strange: mind-bending paradoxes, clever twists and The Last Bencher, animated in under a minute.""",
    hashtags=["#Math", "#Paradox", "#Shorts"],
    tags=["taxicab geometry", "circle that is a square", "manhattan distance", "math paradox", "mind blowing math",
          "geometry", "square circle", "math facts", "paradox", "interestingly strange"],
    pinned_comment="Cheat 🚫 or real circle ⭕? Defend your answer 👇",
)

TAXI = hexc("#ffcf3f")
CX, CY, B = 360, 560, 62           # grid centre (the taxi stand) and one block in pixels
RING = [(x, y) for x in range(-3, 4) for y in range(-3, 4) if abs(x) + abs(y) == 3]
RING.sort(key=lambda p: math.atan2(-p[1], p[0]) % (2 * math.pi))


def taxi(cr, t, x, y, s=1.0, rot=0.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    soft_disc(cr, 0, 30, 90, (0, 0, 0, 0.3))
    rrect(cr, -80, -30, 160, 50, 16)
    paint(cr, lin(0, -30, 0, 20, [(0, shade(TAXI, 0.2)), (1, shade(TAXI, -0.15))]), OUTLINE, 5)
    rrect(cr, -45, -62, 90, 40, 12)
    paint(cr, hexc("#bfe6ff"), OUTLINE, 5)
    rrect(cr, -22, -78, 44, 18, 5)
    paint(cr, WHITE, OUTLINE, 3)
    bold_text(cr, "TAXI", 0, -64, 14, OUTLINE, outline=None, shadow=0)
    for wx in (-48, 48):
        cr.arc(wx, 22, 15, 0, 2 * math.pi)
        paint(cr, hexc("#2b2b33"), OUTLINE, 4)
    for k in range(4):
        rrect(cr, -70 + k * 36, -4, 18, 12, 2)
        paint(cr, OUTLINE, None)
    cr.restore()


def city_grid(cr, t, alpha_=1.0, buildings=True):
    """Streets every block around the taxi stand, with little buildings in each block."""
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#2b2f4a")), (1, hexc("#3f4a6e"))]))
    cr.fill()
    if buildings:
        for i in range(-5, 5):
            for j in range(-5, 6):
                x0, y0 = CX + i * B + 8, CY + j * B + 8
                h = 0.35 + 0.65 * ((i * 7 + j * 13) % 5) / 4
                rrect(cr, x0, y0, B - 16, B - 16, 6)
                paint(cr, shade(hexc("#6a7aa8"), -0.3 + 0.3 * h), alpha(OUTLINE, 0.6), 2)
    for k in range(-6, 7):                                            # streets
        stroke_line(cr, [(CX + k * B, 0), (CX + k * B, H)], 6, (1, 1, 1, 0.22 * alpha_), curve=False)
        stroke_line(cr, [(0, CY + k * B), (W, CY + k * B)], 6, (1, 1, 1, 0.22 * alpha_), curve=False)


def dot(cr, t, start, x, y, col=GOLD, r=14):
    if t < start:
        return
    k = appear(t, start, 0.25)
    cr.arc(x, y, r * k * (1 + 0.15 * math.sin(t * 6 + x)), 0, 2 * math.pi)
    paint(cr, col, OUTLINE, 4)


def path(cr, t, start, pts, col, dur=0.5):
    """Draw a street route block by block."""
    if t < start:
        return
    u = seg(t, start, start + dur) * (len(pts) - 1)
    n = int(u)
    seg_pts = pts[:n + 1]
    if n < len(pts) - 1:
        f = u - n
        a, b = pts[n], pts[n + 1]
        seg_pts = seg_pts + [(lerp(a[0], b[0], f), lerp(a[1], b[1], f))]
    if len(seg_pts) > 1:
        stroke_line(cr, seg_pts, 12, OUTLINE, curve=False)
        stroke_line(cr, seg_pts, 7, col, curve=False)


def P(gx, gy):
    return CX + gx * B, CY - gy * B


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    city_grid(cr, t)
    k = ease_out(seg(t, 0.0, 0.8))
    pts = [P(3, 0), P(0, 3), P(-3, 0), P(0, -3), P(3, 0)]             # the square glows from frame 0
    stroke_line(cr, pts, 16, OUTLINE, curve=False)
    stroke_line(cr, pts, 10, alpha(GOLD, k), curve=False)
    soft_disc(cr, CX, CY, 260, (1, 0.85, 0.3, 0.12 * k))
    taxi(cr, t, CX, CY + 12, 0.7)
    if t >= A("c1", "square."):
        stamp(cr, t, A("c1", "square."), 360, 900 - 120, "IT'S A CIRCLE?!", col=RED, size=58)
        cue("hit", t, A("c1", "square."))
    vignette(cr, 0.45)


def scene_rule(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e6c8"), hexc("#fff6e8"), seed=2)
    u = ease_out(seg(t, A("c2"), A("c2", "middle.", end=True)))
    cr.arc(360, 560, 220, -math.pi / 2, -math.pi / 2 + 2 * math.pi * u)
    paint(cr, None, BLUE, 12)
    cr.arc(360, 560, 12, 0, 2 * math.pi)
    paint(cr, RED, OUTLINE, 4)
    for k in range(8):                                                # equal radius lines
        if t < A("c2", "same") + 0.06 * k:
            continue
        a = k * math.pi / 4
        stroke_line(cr, [(360, 560), (360 + 220 * math.cos(a), 560 + 220 * math.sin(a))], 5, alpha(OUTLINE, 0.6),
                    curve=False)
    sign(cr, t, A("c2", "same"), 360, 170, "SAME DISTANCE", col=BLUE, size=60, end=A("c2", "rule.") - 0.05)
    sign(cr, t, A("c2", "rule."), 360, 170, "THE RULE", col=PURPLE, size=70)
    vignette(cr, 0.3)


def scene_streets(cr, t, tl):
    A = tl.at
    city_grid(cr, t)
    route = [P(0, 0), P(0, 1), P(1, 1), P(1, 2), P(2, 2)]
    if t < A("c3", "streets."):                                      # a crow-flies line, crossed out
        stroke_line(cr, [P(0, 0), P(2, 2)], 8, alpha(WHITE, 0.6), curve=False)
        if t >= A("c3", "fly"):
            mx, my = P(1, 1)
            stroke_line(cr, [(mx - 40, my - 40), (mx + 40, my + 40)], 12, RED, curve=False)
            stroke_line(cr, [(mx + 40, my - 40), (mx - 40, my + 40)], 12, RED, curve=False)
    else:
        path(cr, t, A("c3", "streets."), route, GOLD, dur=1.2)
    u = seg(t, A("c3", "streets."), A("c3", "streets.") + 1.2) * (len(route) - 1)
    n = min(int(u), len(route) - 2)
    f = u - n
    (ax, ay), (bx, by) = route[n], route[n + 1]
    taxi(cr, t, lerp(ax, bx, f), lerp(ay, by, f) + 10, 0.55, rot=0.0 if ay == by else -math.pi / 2 * 0)
    for k, word in enumerate(("Up,", "down,", "left", "right.")):
        if t >= A("c3", word):
            bold_text(cr, ("UP", "DOWN", "LEFT", "RIGHT")[k], 140 + k * 150, 1000 - 80, 34, GOLD)
    if t >= A("c4"):
        n_blocks = 1 + min(3, int(3 * seg(t, A("c4", "distance"), A("c4", "driven.", end=True))))
        sign(cr, t, A("c4", "blocks"), 360, 170, f"DISTANCE = BLOCKS: {min(n_blocks, 4)}", col=GOLD, size=50)
    else:
        sign(cr, t, A("c3", "fly"), 360, 170, "NO FLYING", col=RED, size=70)
    vignette(cr, 0.4)


def scene_grid(cr, t, tl):
    A = tl.at
    city_grid(cr, t, buildings=t < A("c7"))
    cr.save()
    zoom = camera(t, [(A("c5") - 0.3, (1.0, 360, 640)), (A("c8"), (1.08, 360, 600))])
    enter(cr, zoom)
    taxi(cr, t, CX, CY + 10, 0.5)
    bold_text(cr, "STAND", CX, CY + 70, 26, WHITE)
    routes = [("Three", [P(0, 0), P(0, 1), P(0, 2), P(0, 3)], 3, (0, 3)),
              ("right.", [P(0, 0), P(1, 0), P(2, 0), P(3, 0)], 4, (3, 0)),
              ("Two", [P(0, 0), P(1, 0), P(2, 0), P(2, 1)], 5, (2, 1)),
              ("One", [P(0, 0), P(1, 0), P(1, 1), P(1, 2)], 6, (1, 2))]
    cols = (BLUE, GREEN, PURPLE, RED)
    shown = set()
    for k, (word, pts, _, end) in enumerate(routes):
        st = A("c6", word, nth=1)
        if t < A("c7"):
            path(cr, t, st, pts, cols[k], dur=0.45)
        dot(cr, t, st + 0.45, *P(*end))
        shown.add(end)
    if t >= A("c7"):                                                 # all the way round
        for j, p in enumerate(RING):
            dot(cr, t, A("c7") + 0.08 * j, *P(*p))
    if t >= A("c7", "join"):
        u = seg(t, A("c7", "join"), A("c7", "dots.", end=True) + 0.3)
        corners = [P(3, 0), P(0, 3), P(-3, 0), P(0, -3), P(3, 0)]
        n = int(u * 4)
        pts = corners[:n + 1]
        if n < 4:
            f = u * 4 - n
            pts = pts + [(lerp(corners[n][0], corners[n + 1][0], f), lerp(corners[n][1], corners[n + 1][1], f))]
        stroke_line(cr, pts, 16, OUTLINE, curve=False)
        stroke_line(cr, pts, 10, GOLD, curve=False)
    if t >= A("c9", "perfect"):                                       # "3" on every side
        for (gx, gy) in ((1.5, 1.5), (-1.5, 1.5), (-1.5, -1.5), (1.5, -1.5)):
            x, y = P(gx, gy)
            bold_text(cr, "3", x + (24 if gx > 0 else -24), y + (-6 if gy > 0 else 40), 46, GOLD)
    cr.restore()
    sign(cr, t, A("c5", "three"), 360, 170, "3 BLOCKS AWAY", col=GOLD, size=60, end=A("c7") - 0.05)
    if t >= A("c8"):
        sign(cr, t, A("c8", "square."), 360, 170, "A SQUARE!", col=RED, size=76, end=A("c9") - 0.05)
        if t >= A("c8", "square."):
            cue("hit", t, A("c8", "square."))
    if t >= A("c9"):
        sign(cr, t, A("c9", "circle."), 360, 170, "= A TAXI CIRCLE", col=GREEN, size=60)
    vignette(cr, 0.4)


def scene_named(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e6c8"), hexc("#fff6e8"), seed=4)
    cr.arc(220, 600, 130, 0, 2 * math.pi)                             # normal circle vs taxicab circle
    paint(cr, None, BLUE, 10)
    pts = [(500 + 130, 600), (500, 470), (500 - 130, 600), (500, 730), (500 + 130, 600)]
    stroke_line(cr, pts, 10, GOLD, curve=False)
    bold_text(cr, "NORMAL", 220, 800, 36, BLUE)
    bold_text(cr, "TAXI", 500, 800, 36, hexc("#c8961e"))
    sign(cr, t, A("c10", "real"), 360, 170, "REAL MATHS", col=GREEN, size=66, end=A("c10", "called") - 0.05)
    sign(cr, t, A("c10", "taxicab"), 360, 170, "TAXICAB GEOMETRY", col=GOLD, size=56)
    vignette(cr, 0.3)


def scene_comment(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1a1a2e"), hexc("#3a2a5a"), seed=5)
    k = appear(t, A("c11"), 0.4)
    cr.save()
    cr.translate(360, 520)
    cr.scale(k, k)
    rrect(cr, -290, -120, 580, 240, 30)                               # a comment bubble (no username)
    paint(cr, WHITE, OUTLINE, 6)
    cr.arc(-220, -50, 34, 0, 2 * math.pi)
    paint(cr, hexc("#cdb8ff"), OUTLINE, 4)
    bold_text(cr, "CAN A CIRCLE", 40, -40, 42, OUTLINE, outline=None, shadow=0)
    bold_text(cr, "BE A SQUARE?", 40, 20, 42, OUTLINE, outline=None, shadow=0)
    stroke_line(cr, [(-160, 80), (120, 80)], 6, alpha(OUTLINE, 0.3), curve=False)
    cr.restore()
    if t >= A("c11", "answer."):
        stamp(cr, t, A("c11", "answer."), 360, 780 - 20, "YES. KIND OF.", col=GREEN, size=60)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    pts = [(360 + 120, 640), (360, 520), (360 - 120, 640), (360, 760), (360 + 120, 640)]
    stroke_line(cr, pts, 12, GOLD, curve=False)
    taxi(cr, t, 360, 650, 0.4)
    sign(cr, t, A("c12", "cheat"), 190, 400, "WE CHEATED", col=RED, size=46, rot=-0.06)
    sign(cr, t, A("c12", "circle?"), 530, 400, "REAL CIRCLE", col=GREEN, size=46, rot=0.05)
    sign(cr, t, A("c12"), 360, 190, "YOU DECIDE", col=GOLD, size=64)
    vignette(cr, 0.3)


SCENES = {"hook": scene_hook, "rule": scene_rule, "streets": scene_streets, "grid": scene_grid, "named": scene_named,
          "comment": scene_comment, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("THIS CIRCLE", False), ("IS A SQUARE", True)], end=tl.at("c2"), y=170, size=104)
    captions(cr, t, tl)
