"""Episode 6: "The Monty Hall Problem" — script approved by the channel (out/scripts/paradoxes_batch1.md #1).

Facts: under the standard rules (the host knows where the car is, always opens a goat door, always offers the switch)
switching wins with probability 2/3 and staying wins 1/3. In 1990 Marilyn vos Savant's Parade column explained this and
drew thousands of letters insisting she was wrong, many from readers with PhDs.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.critters import car, goat
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, confetti, enter_world, fly, hl, set_camera, stamp, whip

NARRATOR = dict()
TAIL = 1.3   # hold the car reveal + confetti after the last line

SCRIPT = [
    dict(id="m1", scene="stage",
         text="Three doors. Behind one, a car. Behind the other two, goats. You pick door number one."),
    dict(id="m2", scene="stage", text="Now the host, who knows where the car is, opens door three. Goat."),
    dict(id="m3", scene="stage", text="He asks: do you want to switch to door two?", speaker="host", speaker_from="do"),
    dict(id="m4", scene="stage", text="Most people say it doesn't matter. [Fifty-fifty,|50/50,] right?"),
    dict(id="m5", scene="stage", text="Wrong. If you switch, you win [two out of three|2 out of 3] times.", gap=0.25),
    dict(id="m6", scene="stage",
         text="Here's why. When you first picked, you had a [one in three|1 in 3] chance. That doesn't change."),
    dict(id="m7", scene="stage",
         text="So the other [two thirds|2/3] don't disappear. They all pile onto the one door the host left closed."),
    dict(id="m8", scene="mail",
         text="When a columnist explained this in [nineteen ninety,|1990,] thousands of readers wrote in to say she was wrong. "
              "Many of them had PhDs.", gap=0.25),
    dict(id="m9", scene="finale", text="She wasn't. So, next time you get a second chance, switch.", gap=0.2),
]

METADATA = dict(
    title="Why You Should ALWAYS Switch Doors 🚪🐐🚗",
    alt_titles=["The Math Puzzle That Fooled Thousands of PhDs 🚪", "Pick a Door… Then Switch? (Monty Hall Problem) 🐐"],
    description="""Three doors. One car. Two goats. You pick a door, the host opens a different one with a goat… Should you switch? 🚪

Most people say it doesn't matter. The math says switching wins 2 out of 3 times. When this was published in a magazine column in 1990, thousands of readers wrote in to say it was wrong — many of them with PhDs. It wasn't. 🐐🚗

It's called the Monty Hall problem.

💬 Before watching, would you have switched? Be honest 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#MontyHall", "#Paradox", "#Math"],
    tags=["monty hall problem", "monty hall", "probability", "paradox", "math puzzle", "brain teaser",
          "switch or stay", "game show puzzle", "math shorts", "interestingly strange"],
    pinned_comment="Still not convinced? Try it with 100 doors: you pick 1, the host opens 98 goats. Would you switch now? 🤔",
)

GOLD = hexc("#f2b632")
GREEN = hexc("#3d8f45")
BLUE = hexc("#3f6fb5")
PURPLE = hexc("#6a45b5")
DOOR_X = (150, 360, 570)
DOOR_COLS = (hexc("#e0487a"), hexc("#3f6fb5"), hexc("#3d8f45"))
DW, DH, DY = 170, 330, 860    # door width, height, bottom


def stage_set(cr, t):
    cr.set_source_rgba(*hexc("#2a1f45"))
    cr.paint()
    for i in range(-6, 16):   # curtain folds
        x = i * 70
        shape(cr, [(x, 300), (x + 60, 300), (x + 50, 880), (x + 10, 880)], hexc("#8e2f5a" if i % 2 else "#a8386a"),
              seed=4000 + i, amp=1.2, lw=0, stroke=None)
    for i, x in enumerate((60, 360, 660)):   # spotlights
        cr.move_to(x - 20, 300)
        cr.line_to(x + 20, 300)
        cr.line_to(x + 150, 900)
        cr.line_to(x - 150, 900)
        cr.close_path()
        cr.set_source_rgba(1, 0.95, 0.7, 0.10 + 0.04 * math.sin(t * 2 + i))
        cr.fill()
    sharp_shape(cr, [(-800, 880), (1500, 870), (1500, 1800), (-800, 1800)], hexc("#3b2f5c"), seed=4050, amp=1, lw=4)
    for k in range(-6, 16):   # glossy floor stripes
        line(cr, [(k * 90, 880), (k * 140 - 300, 1400)], 3, hexc("#4a3d70"), seed=4060 + k, amp=0.6)
    # light bulbs along the top
    for k in range(-2, 13):
        on = (int(t * 6) + k) % 3 == 0
        dot(cr, k * 60, 320, 9, GOLD if on else hexc("#8a7a3a"))


def door(cr, i, t, open_u=0.0, content=None, tag=None, tag_col=INK, glow=0.0):
    x, col = DOOR_X[i], DOOR_COLS[i]
    x0, y0 = x - DW / 2, DY - DH
    if glow > 0:
        blob(cr, x, DY - DH / 2, DW * 0.75, DH * 0.62, hexc("#ffd23f", 0.35 * glow), seed=4100 + i, amp=2, lw=0,
             stroke=None)
    shape(cr, rrect_pts(x0 - 14, y0 - 14, DW + 28, DH + 14, 12, 18), GOLD, seed=4110 + i, amp=0.6, lw=4)
    shape(cr, rrect_pts(x0, y0, DW, DH, 6, 18), hexc("#1a1428"), seed=4120 + i, amp=0.4, lw=3)   # opening
    if content and open_u > 0.2:
        content(x, DY - 8)
    if open_u < 1:   # door leaf swinging open (drawn narrower as it opens)
        w = DW * (1 - open_u)
        shape(cr, rrect_pts(x0, y0, max(8, w), DH, 6, 18), col, seed=4130 + i, amp=0.6, lw=4)
        if w > 60:
            write(cr, [(str(i + 1), WHITE)], x0 + w / 2, y0 + 120, 90, align="center", bold=True)
            dot(cr, x0 + w - 22, y0 + DH / 2 + 20, 7, GOLD)
    if tag:
        with at(cr, x, y0 - 60, 1.0):
            shape(cr, rrect_pts(-58, -34, 116, 60, 14, 14), WHITE, seed=4140 + i, amp=0.6, lw=3.5)
            write(cr, [(tag, tag_col)], 0, 12, 40, align="center", bold=True)


def scene_stage(cr, t, tl):
    A = tl.at
    keys = [(0, (1.2, 360, 700)), (A("m1", "car"), (1.8, 360, 690)), (A("m1", "goats"), (1.3, 360, 700)),
            (A("m1", "pick"), (1.5, 230, 760)), (A("m2"), (1.4, 520, 760)), (A("m2", "opens"), (1.9, 570, 700)),
            (A("m2", "Goat"), (2.3, 570, 720)), (A("m3"), (1.5, 560, 800)), (A("m3", "two"), (1.9, 360, 700)),
            (A("m4"), (1.2, 360, 700)), (A("m4", "50/50"), (1.6, 360, 690)), (A("m5"), (1.4, 360, 700)),
            (A("m5", "switch"), (1.8, 360, 700)), (A("m6"), (1.2, 360, 660)), (A("m6", "picked"), (1.8, 150, 680)),
            (A("m6", "1"), (2.1, 150, 640)), (A("m6", "change"), (1.5, 260, 700)), (A("m7"), (1.3, 450, 660)),
            (A("m7", "disappear"), (1.8, 570, 640)), (A("m7", "pile"), (1.7, 470, 660)),
            (A("m7", "closed"), (2.0, 360, 660))]
    z, fx, fy = camera(t, keys)
    if t < A("m1", "car"):
        z += 0.06 * seg(t, 0, A("m1", "car"))
    set_camera((z, fx, fy))
    enter_world(cr)
    stage_set(cr, t)

    picked = t >= A("m1", "pick")
    open3 = ease_out(seg(t, A("m2", "opens"), A("m2", "opens") + 0.5))
    # probability tags
    tags = [None, None, None]
    glows = [0.0, 0.0, 0.0]
    if t >= A("m6", "1"):
        tags[0] = "1/3"
    if t >= A("m7", "2/3"):
        tags[1] = "1/3" if t < A("m7", "pile") else "2/3"
        tags[2] = "1/3" if t < A("m7", "pile") else None
    if t >= A("m7", "pile"):
        glows[1] = 0.6 + 0.4 * math.sin(t * 6)
    if picked:
        glows[0] = max(glows[0], 0.5)
    door(cr, 0, t, tag=tags[0], tag_col=RED, glow=glows[0])
    door(cr, 1, t, tag=tags[1], tag_col=GREEN if tags[1] == "2/3" else INK, glow=glows[1])
    door(cr, 2, t, open_u=open3, tag=tags[2],
         content=lambda x, y: goat(cr, x - 10, y, t, s=0.7, facing=-1, bleat=A("m2", "Goat") <= t < A("m2", "Goat") + 0.8))
    if t >= A("m2", "Goat"):
        cue("pop", t, A("m2", "Goat"))
    # the 1/3 from door three sliding over onto door two
    fly(cr, t, A("m7", "pile") - 0.1, 0.6, (DOOR_X[2], DY - DH - 60), (DOOR_X[1], DY - DH - 60),
        lambda x, y: (shape(cr, rrect_pts(x - 58, y - 34, 116, 60, 14, 14), hexc("#fff3c4"), seed=4150, amp=0.6, lw=3.5),
                      write(cr, [("1/3", INK)], x, y + 12, 40, align="center", bold=True)), height=80)
    # bracket over doors 2+3
    if A("m7", "2/3") <= t < A("m7", "pile"):
        line(cr, [(DOOR_X[1] - 80, DY - DH - 120), (DOOR_X[1] - 80, DY - DH - 140), (DOOR_X[2] + 80, DY - DH - 140),
                  (DOOR_X[2] + 80, DY - DH - 120)], 5, GREEN, seed=4160, amp=0.4)
        write(cr, [("2/3", GREEN)], (DOOR_X[1] + DOOR_X[2]) / 2, DY - DH - 156, 44, align="center", bold=True)

    # contestant + host in front of the doors
    s = dict(facing=1, arms=("point", "hip") if A("m1", "pick") <= t < A("m2") else ("hip", "hip"), eyes="dot",
             mouth="smile")
    if t >= A("m3"):
        s.update(arms=("chin", "hip"), eyes="wide", mouth="o")
    if t >= A("m4", "50/50"):
        s.update(arms=("hip", "hip"), eyes="sly", mouth="smirk")
    if t >= A("m5"):
        s.update(eyes="wide", mouth="o", shake=1.0 if t < A("m5", "switch") else 0)
    person(cr, "sam", 130, 1010, t, scale=0.85, **s)
    host_arms = ("hold", "point") if A("m2", "opens") - 0.3 <= t < A("m3") else ("hold", "wave") if t < A("m1", "car") \
        else ("hold", "hip")
    talking = tl.speaking("host", t)
    person(cr, "host", 590, 1010, t, facing=-1, scale=0.85, arms=host_arms, item="mic",
           mouth=("o" if int(t * 12) % 2 else "grin") if talking else "grin")

    # headlines
    hl(cr, t, [("1 ", GOLD), ("car", RED), (" · 2 ", GOLD), ("goats", WHITE)], 200, 62, A("m1", "goats"),
       end=A("m2") - 0.05, bold=True, halo=hexc("#2a1f45", 0.9))
    hl(cr, t, [("SWITCH", GOLD), (" to door 2?", WHITE)], 200, 62, A("m3", "switch"), end=A("m4") - 0.05, bold=True,
       halo=hexc("#2a1f45", 0.9))
    hl(cr, t, [("50/50?", WHITE)], 200, 96, A("m4", "50/50"), end=A("m5") - 0.05, bold=True, halo=hexc("#2a1f45", 0.9))
    stamp(cr, t, A("m5", "Wrong"), "WRONG", dur=0.9, y=430, color="#ff5a5f")
    hl(cr, t, [("STAY", WHITE), (" = 1/3", RED)], 190, 60, A("m5", "2 out of 3"), end=A("m6") - 0.05, bold=True,
       halo=hexc("#2a1f45", 0.9))
    hl(cr, t, [("SWITCH", GOLD), (" = 2/3", GREEN)], 265, 60, A("m5", "2 out of 3"), end=A("m6") - 0.05, bold=True,
       halo=hexc("#2a1f45", 0.9))
    hl(cr, t, [("first pick: ", WHITE), ("1/3", RED)], 200, 62, A("m6", "1"), end=A("m7") - 0.05, bold=True,
       halo=hexc("#2a1f45", 0.9))
    hl(cr, t, [("the other ", WHITE), ("2/3", GREEN), (" moves", WHITE)], 200, 60, A("m7", "pile"), bold=True,
       halo=hexc("#2a1f45", 0.9))


def scene_mail(cr, t, tl):
    """The columnist buried in angry letters."""
    A = tl.at
    keys = [(A("m8") - 0.3, (1.4, 360, 760)), (A("m8", "columnist"), (2.0, 360, 740)), (A("m8", "1990"), (1.8, 420, 700)),
            (A("m8", "thousands"), (1.1, 360, 760)), (A("m8", "wrote"), (1.4, 460, 780)), (A("m8", "wrong"), (1.6, 300, 760)),
            (A("m8", "Many"), (1.9, 360, 820)), (A("m8", "PhDs"), (1.3, 420, 740))]
    z, fx, fy = camera(t, keys)
    set_camera((z, fx, fy))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#f1dfbd"))
    cr.paint()
    sharp_shape(cr, [(-800, 900), (1500, 890), (1500, 1800), (-800, 1800)], hexc("#c8976a"), seed=4200, amp=1, lw=4)
    # desk + columnist
    person(cr, "mia", 360, 960, t, facing=1, arms=("hold", "hip"), eyes="happy" if t < A("m8", "wrong") else "sly",
           mouth="smile" if t < A("m8", "wrong") else "smirk")
    sharp_shape(cr, [(170, 860), (560, 860), (560, 960), (170, 960)], hexc("#8e4a1e"), seed=4201, amp=0.8, lw=4)
    # a magazine page on the desk
    shape(cr, rrect_pts(390, 800, 110, 60, 4, 12), WHITE, seed=4202, amp=0.4, lw=3)
    write(cr, [("1990", RED)], 445, 840, 30, align="center", bold=True)
    # letters pouring in
    import random
    r = random.Random(4)
    start = A("m8", "thousands")
    for k in range(40):
        t0 = start + k * 0.05
        u = seg(t, t0, t0 + 0.7)
        if u <= 0:
            continue
        sx, ex = r.uniform(-150, 870), r.uniform(120, 620)
        x = lerp(sx, ex, u)
        y = lerp(300, 830 - (k % 12) * 12, u) - math.sin(u * math.pi) * 80
        with at(cr, x, y, 0.8, rot=r.uniform(-0.6, 0.6)):
            shape(cr, rrect_pts(-40, -26, 80, 52, 4, 10), WHITE, seed=4210 + k, amp=0.4, lw=3)
            line(cr, [(-40, -26), (0, 4), (40, -26)], 2.5, INK, seed=4260 + k, amp=0.2)
            if k % 4 == 0 and t >= A("m8", "PhDs"):
                shape(cr, [(-22, -44), (22, -44), (22, -36), (-22, -36)], INK, seed=4300 + k, amp=0.2, lw=0,
                      stroke=None)   # graduation cap on some letters
                shape(cr, [(-30, -48), (0, -58), (30, -48), (0, -38)], INK, seed=4320 + k, amp=0.2, lw=0, stroke=None)
    cue("whoosh", t, start, 0.8)
    hl(cr, t, [("1990", RED)], 210, 96, A("m8", "1990"), end=A("m8", "thousands") - 0.05, bold=True)
    hl(cr, t, [("\"You're ", INK), ("WRONG", RED), ("!\"", INK)], 210, 80, A("m8", "wrong"), end=A("m8", "PhDs") - 0.05,
       bold=True)
    hl(cr, t, [("...from ", INK), ("PhDs", PURPLE)], 210, 80, A("m8", "PhDs"), bold=True, underline=True)


def scene_finale(cr, t, tl):
    A = tl.at
    reveal = A("m9", "second")       # the door swings open on "second chance"
    keys = [(A("m9") - 0.2, (1.5, 360, 700)), (A("m9", "next"), (1.9, 360, 690)), (reveal, (1.6, 360, 700)),
            (A("m9", "switch"), (1.25, 360, 740))]
    z, fx, fy = camera(t, keys)
    set_camera((z, fx, fy))
    enter_world(cr)
    stage_set(cr, t)
    door(cr, 0, t)
    door(cr, 1, t, open_u=ease_out(seg(t, reveal - 0.2, reveal + 0.3)), glow=1.0 if t >= reveal else 0.4,
         content=lambda x, y: car(cr, x, y, t, s=0.42))
    door(cr, 2, t, open_u=1.0, content=lambda x, y: goat(cr, x - 10, y, t, s=0.7, facing=-1))
    person(cr, "sam", 130, 1010, t, scale=0.85, arms=("cheer", "cheer") if t >= reveal else ("point", "hip"),
           eyes="happy" if t >= reveal else "dot", mouth="laugh" if t >= reveal else "smile",
           jump=abs(math.sin((t - reveal) * 9)) * 20 if t >= reveal else 0)
    person(cr, "host", 590, 1010, t, facing=-1, scale=0.85, arms=("hold", "cheer"), item="mic", mouth="grin")
    confetti(cr, t, reveal)
    cue("kaching", t, reveal)
    stamp(cr, t, A("m9", "wasn't"), "SHE WAS RIGHT", dur=1.1, y=430, color="#79b061")
    hl(cr, t, [("SWITCH.", GOLD)], 220, 110, A("m9", "switch"), bold=True, underline=True, halo=hexc("#2a1f45", 0.9))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"stage": scene_stage, "mail": scene_mail, "finale": scene_finale}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
