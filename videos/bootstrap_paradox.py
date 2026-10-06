"""Episode 10: "The Song Nobody Wrote" — the bootstrap paradox (script B1, out/scripts/weird_history_time_batch2.md).

The standard bootstrap / ontological paradox thought experiment, told with an original band (not the usual Beethoven
example, to avoid echoing a well-known TV episode). "Loops like this might be the only kind of history time travel
allows" is the Novikov self-consistency idea, framed as "some say".
"""
import math

from motion.captions import captions
from motion.characters import person, phone
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, confetti, enter_world, hl, sepia, set_camera, stamp, whip

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="b1", scene="hook", text="This song has no songwriter. Nobody ever wrote it."),
    dict(id="b2", scene="room", text="You love an old song. So you build a time machine,"),
    dict(id="b3", scene="garage",
         text="go back [fifty years,|50 years,] and play it for the band, before they ever wrote it.", gap=0.12),
    dict(id="b4", scene="garage", text="They love it. They record it. It becomes a hit."),
    dict(id="b5", scene="room2", text="[Fifty years|50 years] later, you hear it, and fall in love with it."),
    dict(id="b6", scene="loop",
         text="So, who wrote the song? The band didn't. They copied you. You didn't. You copied them."),
    dict(id="b7", scene="loop2", text="The song just exists. It loops through time, and nobody ever created it."),
    dict(id="b8", scene="prof",
         text="Physicists call this a causal loop. And some say, if time travel to the past is possible, loops like "
              "this might be the only kind of history it allows."),
    dict(id="b9", scene="end", text="So next time you hear a song you love, ask yourself: who wrote it?", pace=0.97),
]

METADATA = dict(
    title="This Song Has No Songwriter 🎸 (The Bootstrap Paradox)",
    alt_titles=["Nobody Wrote This Song… and It Still Exists 🤯", "The Time Travel Paradox That Breaks Your Brain ⏳"],
    description="""You love an old song. So you build a time machine, go back 50 years, and play it for the band before they ever wrote it. They record it. It becomes a hit. 50 years later, you hear it and fall in love with it… 🎸

So who wrote the song? 🤯

It's called the bootstrap paradox (or a causal loop): information that exists without ever being created. Some physicists think that if time travel to the past is possible, only self-consistent loops like this could happen.

💬 So… who wrote it? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Paradox", "#TimeTravel", "#MindBlown"],
    tags=["bootstrap paradox", "time travel paradox", "causal loop", "paradox", "time travel", "mind blowing",
          "physics", "thought experiment", "paradox explained", "interestingly strange"],
    pinned_comment="Plot hole or genius? Who REALLY wrote the song? 🤔👇",
)

PURPLE = hexc("#6a45b5")
GOLD = hexc("#f2b632")
TEAL = hexc("#2f7f86")
GREEN = hexc("#3d8f45")
BLUE = hexc("#3f6fb5")
PINK = hexc("#e0487a")
KID = "sam"


# ------------------------------------------------------------------ props
def note(cr, x, y, s=1.0, col=INK, double=False, seed=0):
    with at(cr, x, y, s):
        blob(cr, 0, 0, 13, 10, col, seed=seed, amp=0.3, lw=2.5)
        line(cr, [(11, -2), (11, -52)], 4, col, seed=seed + 1, amp=0.2)
        if double:
            blob(cr, 40, -8, 13, 10, col, seed=seed + 2, amp=0.3, lw=2.5)
            line(cr, [(51, -10), (51, -60)], 4, col, seed=seed + 3, amp=0.2)
            line(cr, [(11, -52), (51, -60)], 7, col, seed=seed + 4, amp=0.2)
        else:
            line(cr, [(11, -52), (28, -36)], 5, col, seed=seed + 5, amp=0.2)


def heart(cr, x, y, s, col, seed=0):
    with at(cr, x, y, s):
        blob(cr, -12, -8, 14, 14, col, seed=seed, amp=0.3, lw=0, stroke=None)
        blob(cr, 12, -8, 14, 14, col, seed=seed + 1, amp=0.3, lw=0, stroke=None)
        sharp_shape(cr, [(-25, -2), (25, -2), (0, 26)], col, seed=seed + 2, amp=0.2, lw=0, stroke=None)


def notes_float(cr, t, x, y, n=4, spread=120, seed=0):
    for k in range(n):
        u = (t * 0.7 + k / n) % 1
        col = [PINK, BLUE, GREEN, PURPLE][k % 4]
        note(cr, x + math.sin(u * 6 + k) * spread * 0.4 + (k - n / 2) * 20, y - u * 160, 0.7 + 0.2 * (k % 2),
             hexc("#2a2230", 1 - u) if k % 2 else col, double=k % 2 == 0, seed=seed + k * 10)


def record(cr, x, y, r, t, label="???", spin=1.0, seed=0):
    with at(cr, x, y, 1.0, rot=t * 3 * spin):
        blob(cr, 0, 0, r, r, hexc("#1c1a22"), seed=seed, amp=0.4, lw=4)
        for k in range(3):
            cr.set_source_rgba(1, 1, 1, 0.12)
            cr.set_line_width(2)
            cr.arc(0, 0, r * (0.55 + k * 0.13), 0.3 + k, 1.4 + k)
            cr.stroke()
        blob(cr, 0, 0, r * 0.46, r * 0.46, hexc("#e0487a"), seed=seed + 1, amp=0.3, lw=3)
        dot(cr, 0, 0, r * 0.05, INK)
    write(cr, [(label, WHITE)], x, y + r * 0.1, r * 0.16, align="center", bold=True)


def time_machine(cr, x, y, t, s=1.0, shake=0.0, glow=0.0):
    """A washing machine with a kitchen clock duct-taped on top."""
    with at(cr, x + math.sin(t * 50) * shake, y, s):
        if glow > 0:
            blob(cr, 0, -150, 200 * glow + 10, 200 * glow + 10, hexc("#9fd3f0", 0.5 * glow), seed=7000, amp=1.5, lw=0,
                 stroke=None)
        shape(cr, rrect_pts(-110, -260, 220, 260, 18, 20), WHITE, seed=7001, amp=0.8, lw=4.5)
        line(cr, [(-110, -210), (110, -210)], 3.5, INK, seed=7002, amp=0.4)
        for k in range(3):
            dot(cr, -70 + k * 30, -234, 7, [RED, GOLD, GREEN][k])
        blob(cr, 0, -110, 70, 70, hexc("#bfe6ef"), seed=7003, amp=0.6, lw=5)
        blob(cr, 0, -110, 50, 50, hexc("#9fd3f0"), seed=7004, amp=0.8, lw=3)
        # the clock, taped on
        blob(cr, 20, -300, 46, 46, GOLD, seed=7005, amp=0.5, lw=4)
        blob(cr, 20, -300, 36, 36, WHITE, seed=7006, amp=0.4, lw=2.5)
        a = t * 8 * (1 + 6 * glow)
        line(cr, [(20, -300), (20 + 26 * math.sin(a), -300 - 26 * math.cos(a))], 3.5, RED, seed=7007, amp=0.1)
        line(cr, [(20, -300), (20 + 16 * math.sin(a / 12), -300 - 16 * math.cos(a / 12))], 4.5, INK, seed=7008, amp=0.1)
        for sx in (-1, 1):   # duct tape
            sharp_shape(cr, [(20 + sx * 20, -270), (20 + sx * 50, -250), (20 + sx * 44, -238), (20 + sx * 14, -258)],
                        hexc("#a9a2ae"), seed=7009 + sx, amp=0.4, lw=2.5)


def bedroom(cr, t):
    cr.set_source_rgba(*hexc("#9fb8e0"))
    cr.paint()
    for k in range(-4, 14):   # wallpaper stripes
        sharp_shape(cr, [(k * 90, 250), (k * 90 + 40, 250), (k * 90 + 40, 900), (k * 90, 900)], hexc("#8eabd6"),
                    seed=7100 + k, amp=0.5, lw=0, stroke=None)
    sharp_shape(cr, [(-800, 900), (1600, 890), (1600, 1900), (-800, 1900)], hexc("#c99a62"), seed=7101, amp=1, lw=4)
    # band poster on the wall: the song's own record sleeve
    shape(cr, rrect_pts(470, 380, 200, 240, 6, 18), hexc("#f7d774"), seed=7102, amp=0.6, lw=4)
    record(cr, 570, 480, 64, 0.0, label="", spin=0)
    write(cr, [("1976", PINK)], 570, 600, 40, align="center", bold=True)
    # bed
    shape(cr, rrect_pts(-220, 760, 330, 140, 20, 18), hexc("#e0487a"), seed=7103, amp=0.8, lw=4)
    shape(cr, rrect_pts(-200, 730, 110, 50, 20, 14), WHITE, seed=7104, amp=0.6, lw=3.5)


def garage(cr, t):
    cr.set_source_rgba(*hexc("#c9a56a"))
    cr.paint()
    for k in range(-5, 16):   # wooden planks
        line(cr, [(k * 70, 250), (k * 70, 900)], 3, hexc("#a8844f"), seed=7200 + k, amp=0.8)
    sharp_shape(cr, [(-800, 900), (1600, 890), (1600, 1900), (-800, 1900)], hexc("#8a8a8a"), seed=7201, amp=1, lw=4)
    shape(cr, rrect_pts(40, 380, 260, 70, 10, 18), PURPLE, seed=7202, amp=0.8, lw=4)
    write(cr, [("THE LOOPS", hexc("#f7d774"))], 170, 430, 42, align="center", bold=True)
    write(cr, [("1976", INK)], 560, 450, 60, align="center", bold=True)
    # amp + drum
    shape(cr, rrect_pts(560, 740, 130, 160, 10, 16), hexc("#2b2d3a"), seed=7203, amp=0.6, lw=4)
    blob(cr, 625, 820, 44, 44, hexc("#555a66"), seed=7204, amp=0.5, lw=3)
    shape(cr, rrect_pts(-120, 790, 170, 110, 40, 18), hexc("#c0504d"), seed=7205, amp=0.6, lw=4)
    blob(cr, -35, 790, 85, 18, hexc("#f4efe1"), seed=7206, amp=0.4, lw=3.5)


def guitar(cr, x, y, t, s=1.0, rot=-0.5, col=None, seed=0):
    with at(cr, x, y, s, rot=rot + 0.05 * math.sin(t * 12)):
        blob(cr, 0, 0, 40, 32, col or hexc("#e0487a"), seed=seed, amp=0.6, lw=3.5)
        blob(cr, 0, 0, 10, 10, INK, seed=seed + 1, amp=0.2)
        sharp_shape(cr, [(30, -6), (120, -6), (120, 6), (30, 6)], hexc("#8e5a2e"), seed=seed + 2, amp=0.3, lw=3)


# ------------------------------------------------------------------ scenes
def scene_hook(cr, t, tl, end=False):
    A = tl.at
    cr.set_source_rgba(*hexc("#f7d774"))
    cr.paint()
    for k in range(20):   # rotating sunburst: every punch-in reads on screen
        a = k * math.pi / 10 + t * 0.5
        cr.move_to(360, 620)
        cr.arc(360, 620, 1400, a, a + math.pi / 20)
        cr.close_path()
        cr.set_source_rgba(*hexc("#f2a93b", 0.55))
        cr.fill()
    b = "b9" if end else "b1"
    if not end:
        keys = [(A(b) - 0.2, (0.8,)), (A(b, "song"), (1.15,)), (A(b, "songwriter"), (0.9,)), (A(b, "nobody"), (1.35,)),
                (A(b, "wrote"), (1.0,))]
    else:
        keys = [(A(b) - 0.2, (0.85,)), (A(b, "hear"), (1.2,)), (A(b, "love"), (0.95,)), (A(b, "ask"), (1.35,)),
                (A(b, "who"), (1.05,)), (A(b, "wrote"), (1.4,))]
    z = camera(t, keys, dur=0.12)[0]
    with at(cr, 360, 620, z):
        record(cr, 0, 0, 230, t, label="")
        write(cr, [("written by:", WHITE)], 0, -18, 30, align="center", bold=True)
        write(cr, [("???", WHITE)], 0, 60, 86, align="center", bold=True, halo=INK)
    notes_float(cr, t, 360, 380, n=6, spread=520, seed=7300)
    if not end:
        hl(cr, t, [("NO", RED), (" songwriter", INK)], 215, 84, A("b1", "no"), end=A("b1", "nobody") - 0.05, bold=True)
        hl(cr, t, [("nobody ", INK), ("wrote", RED), (" it", INK)], 215, 84, A("b1", "nobody"), bold=True)
    else:
        hl(cr, t, [("who ", INK), ("wrote", RED), (" it?", INK)], 215, 96, A("b9", "who"), bold=True, underline=True)


def scene_room(cr, t, tl, later=False):
    A = tl.at
    if not later:
        keys = [(A("b2") - 0.2, (1.6, 120, 760)), (A("b2", "song"), (2.0, 140, 700)), (A("b2", "build"), (1.2, 330, 760)),
                (A("b2", "machine"), (1.6, 420, 700))]
    else:
        keys = [(A("b5") - 0.2, (1.0, 330, 760)), (A("b5", "later"), (1.6, 570, 540)), (A("b5", "hear"), (1.9, 140, 700)),
                (A("b5", "fall"), (1.3, 200, 760))]
    set_camera(camera(t, keys, dur=0.18))
    enter_world(cr)
    bedroom(cr, t)
    bop = abs(math.sin(t * 7)) * 6
    loving = later and t >= A("b5", "fall")
    person(cr, KID, 140, 900, t, facing=1, arms=("hold", "hip") if not loving else ("cheer", "cheer"),
           eyes="closed" if not loving else "happy", mouth="grin", jump=bop)
    # headphones
    with at(cr, 140 + 7, 900 - 26 - 102 - 40 + 12 - bop, 1.0):
        line(cr, [(-44, -6), (-30, -44), (30, -44), (44, -6)], 6, INK, seed=7400, amp=0.3)
        for sx in (-1, 1):
            blob(cr, sx * 44, 0, 12, 18, RED, seed=7401 + sx, amp=0.3, lw=3)
    notes_float(cr, t, 170, 640, n=3, spread=80, seed=7410)
    if loving:
        for k in range(3):   # hearts
            u = (t * 0.9 + k / 3) % 1
            heart(cr, 200 + k * 34, 600 - u * 100, 0.6 + 0.3 * u, hexc("#e0487a", 1 - u), seed=7420 + k)
    if not later:
        u = seg(t, A("b2", "build"), A("b2", "machine") + 0.2)
        if u > 0:
            time_machine(cr, 420, 900, t, s=0.9 * ease_out(min(1, u * 1.4)) + 0.01, glow=seg(t, A("b2", "machine"),
                                                                                       A("b2", end=True)))
            cue("pop", t, A("b2", "build"))
        hl(cr, t, [("an ", INK), ("OLD", PINK), (" song", INK)], 215, 80, A("b2", "old"), end=A("b2", "build") - 0.05,
           bold=True)
        hl(cr, t, [("time machine", BLUE), ("*", INK)], 215, 74, A("b2", "machine"), bold=True)
        if t >= A("b2", "machine"):
            write(cr, [("*washing machine + clock", INK)], 360, 1180, 30, align="center", halo=hexc("#fbf3e1", 0.9))
    else:
        hl(cr, t, [("50 years ", INK), ("later", PINK)], 215, 80, A("b5", "50"), end=A("b5", "fall") - 0.05, bold=True)
        hl(cr, t, [("you ", INK), ("LOVE", PINK), (" it", INK)], 215, 90, A("b5", "fall"), bold=True)


def scene_garage(cr, t, tl):
    A = tl.at
    arrive = A("b3")
    keys = [(arrive - 0.2, (1.3, 330, 760)), (A("b3", "50"), (0.9, 330, 700)), (A("b3", "play"), (1.7, 150, 720)),
            (A("b3", "band"), (1.2, 400, 760)), (A("b3", "before"), (1.8, 470, 700)),
            (A("b4", "love"), (1.2, 400, 760)), (A("b4", "record"), (1.7, 520, 700)), (A("b4", "hit"), (1.0, 360, 700))]
    set_camera(camera(t, keys, dur=0.18))
    enter_world(cr)
    garage(cr, t)
    flash = 1 - seg(t, arrive, arrive + 0.35)
    time_machine(cr, 40, 900, t, s=0.7, glow=flash)
    cue("whoosh", t, arrive, 0.3)
    playing = A("b3", "play") <= t
    person(cr, KID, 160, 900, t, facing=1, arms=("give", "hip") if playing else ("hip", "hip"), eyes="happy",
           mouth="grin", item="phone" if playing and t < A("b4") else None)
    if playing and t < A("b4", "record"):
        notes_float(cr, t, 260, 660, n=3, spread=100, seed=7500)
    wow = t >= A("b4")
    for i, (who, x) in enumerate((("rocker_a", 400), ("rocker_b", 540))):
        person(cr, who, x, 900, t, facing=-1, arms=("cheer", "hip") if wow else ("hip", "hip"),
               eyes="wide" if playing and not wow else ("happy" if wow else "dot"),
               mouth="o" if playing and not wow else "grin", jump=abs(math.sin(t * 8 + i)) * 10 if wow else 0)
        guitar(cr, x - 10, 800, t, 0.9, col=[PINK, BLUE][i], seed=7510 + i * 10)
    sepia(cr, 0.55)
    # recording light + a hit record
    if t >= A("b4", "record"):
        on = int(t * 4) % 2
        cr.save()
        cr.identity_matrix()
        shape(cr, rrect_pts(470, 330, 200, 64, 12, 16), hexc("#e53935" if on else "#7a1f1f"), seed=7520, amp=0.6, lw=4)
        write(cr, [("REC", WHITE)], 570, 376, 40, align="center", bold=True)
        cr.restore()
    if t >= A("b4", "hit"):
        cr.save()
        cr.identity_matrix()
        sc = pop(t, A("b4", "hit"), 0.25)
        if sc > 0:
            with at(cr, 360, 560, sc, rot=-0.08):
                shape(cr, rrect_pts(-180, -90, 360, 180, 18, 20), GOLD, seed=7530, amp=0.8, lw=5)
                write(cr, [("#1 HIT", RED)], 0, 30, 90, align="center", bold=True)
        confetti(cr, t, A("b4", "hit"))
        cr.restore()
        cue("kaching", t, A("b4", "hit"))
    hl(cr, t, [("50 years ", INK), ("BACK", BLUE)], 215, 80, A("b3", "50"), end=A("b3", "before") - 0.05, bold=True)
    hl(cr, t, [("before they ", INK), ("wrote it", RED)], 215, 70, A("b3", "before"), end=A("b4") - 0.05, bold=True)
    hl(cr, t, [("they ", INK), ("LOVE", PINK), (" it", INK)], 215, 80, A("b4", "love"), end=A("b4", "record") - 0.05,
       bold=True)


def loop_diagram(cr, t, tl, part):
    """YOU → BAND → HIT → YOU, and the song riding the loop forever."""
    A = tl.at
    cr.set_source_rgba(*hexc("#fbf3e1"))
    cr.paint()
    cx, cy, R = 360, 640, 250
    if part == 1:
        z = camera(t, [(A("b6") - 0.2, (0.9, 360, 640)), (A("b6", "who"), (1.0, 360, 640)),
                       (A("b6", "band"), (1.4, 560, 760)), (A("b6", "copied"), (1.25, 480, 560)),
                       (A("b6", "you", nth=2), (1.5, 360, 420)),
                       (A("b6", "copied", nth=2), (1.2, 250, 560))], dur=0.18)
    else:
        z = camera(t, [(A("b7") - 0.2, (1.25, 360, 640)), (A("b7", "exists"), (0.95, 360, 640)),
                       (A("b7", "loops"), (1.1, 360, 640)), (A("b7", "time"), (0.85, 360, 640)),
                       (A("b7", "nobody"), (1.35, 360, 640)), (A("b7", "created"), (1.7, 360, 660))], dur=0.18)
    cr.translate(360, 640)
    cr.scale(z[0], z[0])
    cr.translate(-z[1], -z[2])
    spin = t * (0.9 if part == 2 else 0.4)
    cr.set_line_width(10)
    cr.set_source_rgba(*hexc("#f7d774"))
    cr.arc(cx, cy, R, 0, 2 * math.pi)
    cr.stroke()
    for k in range(3):   # arrowheads chasing round the circle
        a = spin + k * 2 * math.pi / 3
        px, py = cx + R * math.cos(a), cy + R * math.sin(a)
        with at(cr, px, py, 1.0, rot=a + math.pi / 2):
            sharp_shape(cr, [(-22, -18), (22, 0), (-22, 18)], hexc("#e8a93b"), seed=7600 + k, amp=0.3, lw=3)
    nodes = [(-90, "YOU", BLUE, KID), (30, "THE BAND", PURPLE, "rocker_a"), (150, "#1 HIT", RED, None)]
    for k, (deg, lab, col, who) in enumerate(nodes):
        a = math.radians(deg)
        x, y = cx + R * math.cos(a), cy + R * math.sin(a)
        sc = pop(t, A("b6") if part == 1 else 0, 0.25) if part == 1 else 1.0
        if sc <= 0:
            continue
        with at(cr, x, y, sc):
            blob(cr, 0, 0, 92, 92, WHITE, seed=7610 + k, amp=0.8, lw=5, stroke=col)
            if who:
                person(cr, who, 0, 70, t, facing=1, scale=0.55, eyes="dot", mouth="smile")
            else:
                record(cr, 0, -6, 60, t, label="")
            write(cr, [(lab, col)], 0, 130, 38, align="center", bold=True, halo=WHITE)
    # the song itself travelling the loop
    a = spin * 2.2 + 1.0
    note(cr, cx + R * math.cos(a), cy + R * math.sin(a), 1.2, PINK, double=True, seed=7650)
    if part == 1:
        for key, n0, n1, nth in (("copied", 0, 1, 1), ("copied", 2, 0, 2)):
            tt = A("b6", key, nth=nth)
            if t >= tt:
                a0, a1 = math.radians(nodes[n0][0]), math.radians(nodes[n1][0])
                x0, y0 = cx + R * 0.55 * math.cos(a0), cy + R * 0.55 * math.sin(a0)
                x1, y1 = cx + R * 0.55 * math.cos(a1), cy + R * 0.55 * math.sin(a1)
                u = seg(t, tt, tt + 0.3)
                line(cr, [(x0, y0), (lerp(x0, x1, u), lerp(y0, y1, u))], 8, RED, seed=7660 + nth, amp=0.5)
                write(cr, [("copied", RED)], (x0 + x1) / 2, (y0 + y1) / 2 - 12, 40, align="center", bold=True,
                      halo=WHITE)
        hl(cr, t, [("who ", INK), ("wrote", RED), (" it?", INK)], 215, 90, A("b6", "who"), end=A("b6", "band") - 0.05,
           bold=True)
        hl(cr, t, [("band: ", INK), ("copied YOU", PURPLE)], 215, 76, A("b6", "band"), end=A("b6", "you", nth=2) - 0.05,
           bold=True)
        hl(cr, t, [("you: ", INK), ("copied THEM", BLUE)], 215, 76, A("b6", "you", nth=2), bold=True)
    else:
        write(cr, [("∞", PINK)], cx, cy + 50, 190, align="center", bold=True)
        hl(cr, t, [("it just ", INK), ("EXISTS", PINK)], 215, 84, A("b7", "exists"), end=A("b7", "nobody") - 0.05,
           bold=True)
        hl(cr, t, [("created by: ", INK), ("NOBODY", RED)], 215, 72, A("b7", "nobody"), bold=True, underline=True)


def scene_prof(cr, t, tl):
    A = tl.at
    keys = [(A("b8") - 0.2, (1.1, 360, 720)), (A("b8", "causal"), (1.5, 470, 560)), (A("b8", "some"), (1.8, 170, 720)),
            (A("b8", "time"), (1.1, 400, 700)), (A("b8", "possible"), (1.7, 480, 560)), (A("b8", "only"), (1.1, 400, 700)),
            (A("b8", "history"), (1.9, 485, 650)), (A("b8", "allows"), (1.2, 360, 720))]
    set_camera(camera(t, keys, dur=0.18))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#e9d3ae"))
    cr.paint()
    sharp_shape(cr, [(-800, 900), (1600, 890), (1600, 1900), (-800, 1900)], hexc("#b98a5a"), seed=7700, amp=1, lw=4)
    shape(cr, rrect_pts(250, 380, 470, 330, 8, 20), hexc("#8e5a2e"), seed=7701, amp=0.8, lw=4)
    shape(cr, rrect_pts(266, 396, 438, 298, 6, 20), hexc("#2f5b46"), seed=7702, amp=0.6, lw=3)
    chalk = hexc("#f4f1e6")
    u = seg(t, A("b8", "causal"), A("b8", "loop", end=True))
    if u > 0:   # a loop drawn in chalk
        cr.set_source_rgba(*chalk)
        cr.set_line_width(6)
        cr.arc(485, 560, 100, -math.pi / 2, -math.pi / 2 + 2 * math.pi * u)
        cr.stroke()
        write(cr, [("CAUSAL", chalk)], 485, 550, 40, align="center", bold=True)
        write(cr, [("LOOP", hexc("#f7d774"))], 485, 600, 44, align="center", bold=True)
    if t >= A("b8", "only"):
        write(cr, [("only loops allowed?", hexc("#f7d774"))], 485, 680, 32, align="center", bold=True)
    person(cr, "hilbert", 160, 900, t, facing=1, arms=("point", "hip") if t >= A("b8", "causal") else ("chin", "hip"),
           eyes="sly" if t >= A("b8", "some") else "dot", mouth="o" if int(t * 10) % 2 else "smile")
    hl(cr, t, [("a ", INK), ("causal loop", PURPLE)], 215, 80, A("b8", "causal"), end=A("b8", "some") - 0.05, bold=True)
    hl(cr, t, [("time travel", BLUE), (" = loops only?", INK)], 215, 60, A("b8", "time"), bold=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "hook":
        scene_hook(cr, t, tl)
    elif name == "room":
        scene_room(cr, t, tl)
    elif name == "garage":
        scene_garage(cr, t, tl)
    elif name == "room2":
        scene_room(cr, t, tl, later=True)
    elif name == "loop":
        loop_diagram(cr, t, tl, 1)
    elif name == "loop2":
        loop_diagram(cr, t, tl, 2)
    elif name == "prof":
        scene_prof(cr, t, tl)
    else:
        scene_hook(cr, t, tl, end=True)
    cr.restore()
    captions(cr, t, tl)
