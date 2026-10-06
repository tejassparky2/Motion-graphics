"""Episode 8: "The Shortest War in History" — approved script A2 (out/scripts/weird_history_time_batch2.md).

Facts (Wikipedia, "Anglo-Zanzibar War"): 27 August 1896, UK vs the Sultanate of Zanzibar. Sultan Hamad bin Thuwaini died
on 25 August; his nephew Khalid bin Barghash took the palace without the British approval the 1890 treaty required.
Ultimatum to leave by 9:00; bombardment began at 9:00 and the war lasted 38-45 minutes (38 most often cited). Khalid
escaped (to the German consulate, then German East Africa); Britain installed Hamoud bin Muhammed. About 500
Zanzibaris were killed or wounded, so the tone stays on the timing, never on the casualties.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict(speed=1.02)
TAIL = 0.8

SCRIPT = [
    dict(id="w1", scene="tv", text="The shortest war in history lasted about as long as a TV episode."),
    dict(id="w2", scene="throne",
         text="August, [eighteen ninety-six.|1896.] The Sultan of Zanzibar dies, and his nephew grabs the palace, "
              "without Britain's approval."),
    dict(id="w3", scene="letter", text="Britain says: leave by [nine a.m.|9 a.m.]"),
    dict(id="w4", scene="throne2", text="He doesn't."),
    dict(id="w5", scene="sea", text="At [nine o'clock,|9:00,] British warships open fire."),
    dict(id="w6", scene="sea",
         text="By about [nine forty,|9:40,] the palace is wrecked, the flag is down, and the new sultan has escaped "
              "out the back."),
    dict(id="w7", scene="clock", text="The war is over in around [thirty-eight minutes.|38 minutes.]", gap=0.2),
    dict(id="w8", scene="throne3", text="Britain puts its own choice on the throne."),
    dict(id="w9", scene="tv2",
         text="So next time a show feels long, remember: an entire war was shorter than your average TV episode."),
]

METADATA = dict(
    title="The Shortest War in History Lasted 38 Minutes ⏱️",
    alt_titles=["This War Was Shorter Than a TV Episode 😳", "The 38-Minute War Nobody Talks About ⏱️"],
    description="""The shortest war in history lasted about as long as a TV episode. ⏱️

August 27, 1896: the Sultan of Zanzibar dies, and his nephew takes the palace without Britain's approval. Britain gives him until 9 a.m. to leave. He doesn't. At 9:00 the warships open fire, and roughly 38 minutes later it's over. (Historians put it at 38–45 minutes.) It's known as the Anglo-Zanzibar War.

💬 What's the weirdest history fact you know? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#History", "#WeirdHistory", "#DidYouKnow"],
    tags=["shortest war in history", "anglo zanzibar war", "38 minute war", "weird history", "history facts",
          "zanzibar", "1896", "did you know", "history shorts", "interestingly strange"],
    pinned_comment="Shorter than an episode of your favorite show 😳 What would YOU do in 38 minutes? 👇",
)

SKY = hexc("#bfe6ff")
SEA = hexc("#3aa0c8")
SAND = hexc("#ecd28e")
PALACE = hexc("#f4efe1")
GOLD = hexc("#f2b632")
NAVY = hexc("#23346b")
GREEN = hexc("#3d8f45")
ZRED = hexc("#c8312c")    # the sultanate's plain red flag


def union_flag(cr, x, y, w=90, h=54, seed=0):
    cr.save()
    cr.translate(x, y)
    cr.rectangle(0, 0, w, h)
    cr.clip()
    cr.set_source_rgba(*NAVY)
    cr.paint()
    for lw, col in ((h * 0.22, WHITE), (h * 0.08, RED)):
        cr.set_line_width(lw)
        cr.set_source_rgba(*col)
        cr.move_to(0, 0), cr.line_to(w, h), cr.move_to(w, 0), cr.line_to(0, h)
        cr.stroke()
    for lw, col in ((h * 0.34, WHITE), (h * 0.2, RED)):
        cr.set_line_width(lw)
        cr.set_source_rgba(*col)
        cr.move_to(w / 2, 0), cr.line_to(w / 2, h), cr.move_to(0, h / 2), cr.line_to(w, h / 2)
        cr.stroke()
    cr.restore()
    shape(cr, rrect_pts(x, y, w, h, 2, 14), None, seed=seed, amp=0.5, lw=3)


def stopwatch(cr, x, y, r, minutes, label=True, wedge=True):
    shape(cr, rrect_pts(x - 14, y - r - 22, 28, 18, 4, 8), GOLD, seed=5001, amp=0.4, lw=3)
    blob(cr, x, y, r, r, WHITE, seed=5000, amp=0.6, lw=5)
    for k in range(12):
        a = k * math.pi / 6
        line(cr, [(x + math.sin(a) * r * 0.8, y - math.cos(a) * r * 0.8), (x + math.sin(a) * r * 0.92,
                   y - math.cos(a) * r * 0.92)], 3, INK, seed=5002 + k, amp=0.1)
    if wedge and minutes > 0:   # red wedge fills as the minutes run
        cr.move_to(x, y)
        cr.arc(x, y, r * 0.78, -math.pi / 2, -math.pi / 2 + 2 * math.pi * minutes / 60)
        cr.close_path()
        cr.set_source_rgba(*hexc("#e53935", 0.35))
        cr.fill()
    a = 2 * math.pi * minutes / 60
    line(cr, [(x, y), (x + math.sin(a) * r * 0.75, y - math.cos(a) * r * 0.75)], 5, RED, seed=5020, amp=0.1)
    dot(cr, x, y, 6, INK)
    if label:
        write(cr, [(f"{int(minutes)} min", RED)], x, y + r + 50, r * 0.5, align="center", bold=True, halo=WHITE)


# ------------------------------------------------------------------ TV (hook + loop ending)
def tv(cr, x, y, s, t, screen):
    with at(cr, x, y, s):
        line(cr, [(-40, -230), (-110, -330)], 5, INK, seed=5100, amp=0.3)   # antenna
        line(cr, [(40, -230), (110, -320)], 5, INK, seed=5101, amp=0.3)
        shape(cr, rrect_pts(-270, -230, 540, 400, 40, 22), hexc("#8e5a2e"), seed=5102, amp=0.8, lw=5)
        shape(cr, rrect_pts(-240, -200, 400, 340, 30, 22), hexc("#20303a"), seed=5103, amp=0.6, lw=4)
        for k in range(2):
            blob(cr, 205, -120 + k * 80, 18, 18, GOLD, seed=5104 + k, amp=0.4, lw=3)
        cr.save()
        cr.rectangle(-236, -196, 392, 332)
        cr.clip()
        screen(cr)
        cr.restore()
        for dx in (-200, 200):
            line(cr, [(dx, 170), (dx + (20 if dx > 0 else -20), 230)], 7, INK, seed=5110 + dx, amp=0.3)


def mini_battle(cr, t):
    """What's on the TV: a tiny palace and a tiny ship trading puffs."""
    cr.set_source_rgba(*SKY)
    cr.paint()
    sharp_shape(cr, [(-240, 60), (160, 60), (160, 140), (-240, 140)], SEA, seed=5120, amp=0.6, lw=0, stroke=None)
    shape(cr, rrect_pts(10, -90, 140, 150, 6, 14), PALACE, seed=5121, amp=0.6, lw=3.5)
    line(cr, [(80, -90), (80, -160)], 3, INK, seed=5124, amp=0.2)
    sharp_shape(cr, [(80, -160), (120, -156), (120, -134), (80, -138)], ZRED, seed=5125, amp=0.4, lw=2.5)
    sharp_shape(cr, [(-220, 40), (-60, 40), (-80, 76), (-210, 76)], hexc("#6b7280"), seed=5122, amp=0.6, lw=3.5)
    sharp_shape(cr, [(-170, 40), (-110, 40), (-110, 10), (-170, 10)], hexc("#9aa3a8"), seed=5126, amp=0.4, lw=3)
    k = (t * 1.5) % 1
    blob(cr, lerp(-60, 60, k), 20 - math.sin(k * math.pi) * 90, 8, 8, INK, seed=5123, amp=0.2)
    if k > 0.85:
        blob(cr, 70, 0, 40, 30, hexc("#ffd23f"), seed=5127, amp=2.0, lw=3)


def scene_tv(cr, t, tl, end=False):
    A = tl.at
    cr.set_source_rgba(*hexc("#f3d9a4"))
    cr.paint()
    if not end:
        keys = [(0, (1.25, 360, 700)), (A("w1", "war"), (1.0, 360, 700)), (A("w1", "lasted"), (1.4, 480, 520)),
                (A("w1", "TV"), (0.95, 360, 720))]
    else:
        keys = [(A("w9") - 0.2, (1.0, 360, 700)), (A("w9", "long"), (1.4, 300, 640)), (A("w9", "remember"), (0.95, 360, 720)),
                (A("w9", "war"), (1.0, 360, 740)), (A("w9", "shorter"), (1.08, 360, 760)), (A("w9", "TV"), (0.95, 360, 720))]
    z, fx, fy = camera(t, keys)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    for k in range(-6, 14):   # wallpaper
        line(cr, [(k * 90, -400), (k * 90, 1800)], 3, hexc("#e8c98a"), seed=5200 + k, amp=0.6)
    sharp_shape(cr, [(-600, 930), (1400, 930), (1400, 1900), (-600, 1900)], hexc("#b98a5a"), seed=5201, amp=1, lw=4)
    tv(cr, 360, 720, 1.15, t, lambda c: mini_battle(c, t))
    stopwatch(cr, 560, 390, 70, (t * 12) % 60 if not end else 38, label=False)
    if not end:
        hl(cr, t, [("SHORTEST", RED), (" war ever", INK)], 215, 76, 0.0, end=A("w1", "TV") - 0.05, bold=True, sound=False)
        hl(cr, t, [("= 1 ", INK), ("TV episode", hexc("#3f6fb5"))], 215, 76, A("w1", "TV"), bold=True)
    else:
        # the bars: one TV episode vs the whole war
        grow = seg(t, A("w9", "war"), A("w9", "shorter", end=True))
        for i, (lab, frac, col, key) in enumerate((("TV episode", 1.0, hexc("#3f6fb5"), "remember"),
                                                    ("WAR: 38 min", 0.82, RED, "war"))):
            u = seg(t, A("w9", key), A("w9", key) + 0.4)
            if u <= 0:
                continue
            y = 1020 + i * 106
            shape(cr, rrect_pts(40, y, max(10, 640 * frac * ease_out(u)), 86, 18, 18), col, seed=5300 + i, amp=0.6,
                  lw=4)
            write(cr, [(lab, WHITE)], 64, y + 60, 48, bold=True)
        hl(cr, t, [("a show feels ", INK), ("long", RED), ("?", INK)], 215, 70, A("w9", "long"), end=A("w9", "war") - 0.05,
           bold=True)
        hl(cr, t, [("the war was ", INK), ("SHORTER", RED)], 215, 72, A("w9", "shorter"), bold=True, underline=True)
        if grow >= 1:
            cue("hit", t, A("w9", "shorter", end=True))


# ------------------------------------------------------------------ throne room
def throne_room(cr, t):
    cr.set_source_rgba(*hexc("#f1d7a1"))
    cr.paint()
    for k in range(-3, 5):   # arches
        x = k * 260
        shape(cr, [(x + 40, 900), (x + 40, 470), (x + 130, 390), (x + 220, 470), (x + 220, 900)], hexc("#e2bd7c"),
              seed=5400 + k, amp=0.8, lw=3.5)
        for j in range(6):
            dot(cr, x + 60 + j * 32, 450 + (j % 2) * 14, 4, hexc("#3aa0c8"))
    sharp_shape(cr, [(-800, 900), (1600, 890), (1600, 1900), (-800, 1900)], hexc("#b0624a"), seed=5401, amp=1, lw=4)
    sharp_shape(cr, [(260, 900), (460, 900), (560, 1400), (160, 1400)], hexc("#c8312c"), seed=5402, amp=0.8, lw=3.5)
    # throne
    shape(cr, [(310, 900), (310, 640), (360, 600), (410, 640), (410, 900)], GOLD, seed=5410, amp=0.8, lw=4.5)
    shape(cr, rrect_pts(326, 660, 68, 130, 16, 16), hexc("#b8325e"), seed=5411, amp=0.6, lw=3.5)
    shape(cr, rrect_pts(290, 800, 140, 34, 10, 16), GOLD, seed=5412, amp=0.6, lw=4)
    dot(cr, 360, 626, 8, hexc("#3aa0c8"))


def crown(cr, x, y, s=1.0, rot=0.0):
    with at(cr, x, y, s, rot=rot):
        sharp_shape(cr, [(-34, 0), (-38, -40), (-18, -18), (0, -46), (18, -18), (38, -40), (34, 0)], GOLD, seed=5420,
                    amp=0.6, lw=3.5)
        for k in (-20, 0, 20):
            dot(cr, k, -10, 4, RED)


def scene_throne(cr, t, tl, part):
    A = tl.at
    if part == 1:
        keys = [(A("w2") - 0.2, (1.1, 360, 700)), (A("w2", "August"), (1.6, 250, 640)), (A("w2", "1896"), (1.3, 400, 700)), (A("w2", "Sultan"), (1.3, 360, 720)),
                (A("w2", "dies"), (1.9, 200, 640)), (A("w2", "nephew"), (1.4, 560, 760)), (A("w2", "grabs"), (1.7, 380, 720)),
                (A("w2", "without"), (1.2, 360, 700))]
    elif part == 2:
        keys = [(A("w4") - 0.2, (1.6, 360, 700)), (A("w4", "doesn't"), (2.0, 370, 640))]
    else:
        keys = [(A("w8") - 0.2, (1.1, 360, 700)), (A("w8", "own"), (1.5, 360, 640)), (A("w8", "throne"), (1.7, 360, 680))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    throne_room(cr, t)
    if part == 1:
        # the old sultan's portrait gets a black ribbon; the crown waits on the cushion
        with at(cr, 180, 560, 0.9):
            shape(cr, rrect_pts(-60, -80, 120, 150, 8, 16), GOLD, seed=5430, amp=0.6, lw=4)
            shape(cr, rrect_pts(-46, -66, 92, 122, 6, 16), hexc("#fff3c4"), seed=5431, amp=0.5, lw=2.5)
            blob(cr, 0, -20, 22, 24, hexc("#b9794a"), seed=5432, amp=0.5, lw=3)
            shape(cr, rrect_pts(-22, -50, 44, 14, 5, 10), hexc("#2f6f5e"), seed=5433, amp=0.4, lw=2.5)
            if t >= A("w2", "dies"):
                line(cr, [(-60, -80), (-20, -80), (-60, -40)], 9, INK, seed=5434, amp=0.3)
        run = seg(t, A("w2", "nephew"), A("w2", "grabs", end=True))
        on = t >= A("w2", "grabs", end=True)
        if not on:
            crown(cr, 360, 796, 0.9)
        if t >= A("w2", "nephew"):
            x = lerp(760, 360, ease_out(run))
            person(cr, "claimant", x, 900 if not on else 900, t, facing=-1 if not on else 1,
                   walk=None if on else t * 2.4, arms=("cheer", "hip") if on else ("down", "down"),
                   eyes="sly" if not on else "happy", mouth="grin")
            if on:
                crown(cr, 364, 684, 0.8, rot=0.08)
        if t >= A("w2", "without"):
            union_flag(cr, 520, 520, 110, 66, seed=5440)
            sc = pop(t, A("w2", "approval"), 0.25)
            if sc > 0:
                with at(cr, 575, 553, sc, rot=-0.2):
                    line(cr, [(-70, -50), (70, 50)], 10, RED, seed=5441, amp=0.4)
                    line(cr, [(70, -50), (-70, 50)], 10, RED, seed=5442, amp=0.4)
        hl(cr, t, [("1896", RED)], 215, 90, A("w2", "1896"), end=A("w2", "Sultan") - 0.05, bold=True)
        hl(cr, t, [("the Sultan ", INK), ("dies", RED)], 215, 70, A("w2", "dies"), end=A("w2", "nephew") - 0.05, bold=True)
        hl(cr, t, [("nephew ", INK), ("grabs", RED), (" the palace", INK)], 215, 60, A("w2", "grabs"),
           end=A("w2", "without") - 0.05, bold=True)
        hl(cr, t, [("Britain: ", INK), ("NOT approved", RED)], 215, 64, A("w2", "without"), bold=True)
        # little map inset when Zanzibar is named
        sc = pop(t, A("w2", "Zanzibar"), 0.25) * (1 - seg(t, A("w2", "dies") - 0.1, A("w2", "dies") + 0.1))
        if sc > 0:
            cr.save()
            cr.identity_matrix()
            with at(cr, 540, 470, sc):
                blob(cr, 0, 0, 120, 120, SEA, seed=5450, amp=0.8, lw=4.5)
                blob(cr, -150, -20, 120, 150, hexc("#a8c77a"), seed=5451, amp=1.2, lw=4)   # the mainland coast
                blob(cr, 30, 10, 16, 34, hexc("#a8c77a"), seed=5452, amp=0.6, lw=3.5)
                write(cr, [("ZANZIBAR", WHITE)], 20, 90, 30, align="center", bold=True, halo=INK)
            cr.restore()
    elif part == 2:
        person(cr, "claimant", 360, 900, t, facing=1, arms=("hip", "hip"), eyes="sly", mouth="smirk")
        crown(cr, 364, 684, 0.8, rot=0.08)
        shake = math.sin(t * 16) * 12 if t >= A("w4", "doesn't") else 0
        with at(cr, 240 + shake, 640, 1.0, rot=-0.15):   # the ultimatum, tossed aside
            shape(cr, rrect_pts(-60, -40, 120, 80, 4, 14), WHITE, seed=5460, amp=0.6, lw=3)
            write(cr, [("9:00", RED)], 0, 14, 36, align="center", bold=True)
        hl(cr, t, [("\"NOPE.\"", RED)], 215, 96, A("w4", "doesn't"), bold=True)
    else:
        # the new sultan, lowered in by a giant British hand
        drop = ease_out(seg(t, A("w8", "puts"), A("w8", "choice", end=True)))
        y = lerp(300, 900, drop)
        person(cr, "successor", 360, y, t, facing=1, arms=("down", "down"), eyes="wide" if drop < 1 else "happy",
               mouth="o" if drop < 1 else "smile")
        if drop < 1:
            with at(cr, 360, y - 220, 1.0):
                shape(cr, rrect_pts(-40, -60, 80, 70, 24, 16), hexc("#f0c29c"), seed=5470, amp=0.7, lw=4)
                shape(cr, rrect_pts(-44, -400, 88, 340, 10, 16), NAVY, seed=5471, amp=0.6, lw=4)   # sleeve
        union_flag(cr, 500, 470, 120, 72, seed=5472)
        hl(cr, t, [("Britain's ", INK), ("own choice", hexc("#3f6fb5"))], 215, 70, A("w8", "own"), bold=True)
        cue("thud", t, A("w8", "choice", end=True))


def scene_letter(cr, t, tl):
    A = tl.at
    cr.set_source_rgba(*hexc("#e9d3ae"))
    cr.paint()
    z = camera(t, [(A("w3") - 0.2, (1.0,)), (A("w3", "leave"), (1.15,)), (A("w3", "9"), (1.35,))])[0]
    with at(cr, 360, 640, z, rot=-0.04):
        shape(cr, rrect_pts(-270, -330, 540, 600, 10, 24), hexc("#fbf6e6"), seed=5500, amp=0.8, lw=4)
        union_flag(cr, -230, -300, 110, 66, seed=5501)
        write(cr, [("ULTIMATUM", NAVY)], 50, -250, 52, align="center", bold=True)
        write(cr, [("Leave the palace", INK)], 0, -120, 44, align="center")
        write(cr, [("by", INK)], 0, -50, 44, align="center")
        if t >= A("w3", "9"):
            write(cr, [("9:00 a.m.", RED)], 0, 80, 110, align="center", bold=True)
            cue("hit", t, A("w3", "9"))
        line(cr, [(-200, 200), (60, 200)], 2.5, INK, seed=5502, amp=0.3)
        line(cr, [(-180, 190), (-140, 160), (-100, 196), (-60, 164), (-20, 190)], 3, NAVY, seed=5503, amp=0.6)
    stopwatch(cr, 590, 1040, 70, 59 + 0.9 * seg(t, A("w3"), A("w3", end=True)), label=False, wedge=False)
    write(cr, [("8:59", INK)], 590, 1175, 36, align="center", bold=True, halo=WHITE)
    hl(cr, t, [("\"Leave by ", INK), ("9 a.m.", RED), ("\"", INK)], 215, 66, A("w3", "leave"), bold=True)


# ------------------------------------------------------------------ the bombardment
def warship(cr, x, y, t, s=1.0, seed=0):
    with at(cr, x, y + math.sin(t * 2 + seed) * 4, s):
        sharp_shape(cr, [(-150, -30), (150, -30), (120, 20), (-130, 20)], hexc("#6b7280"), seed=seed, amp=0.8, lw=4)
        sharp_shape(cr, [(-80, -30), (60, -30), (60, -70), (-80, -70)], hexc("#9aa3a8"), seed=seed + 1, amp=0.6, lw=3.5)
        for k, fx in enumerate((-50, 10)):
            sharp_shape(cr, [(fx, -70), (fx + 26, -70), (fx + 26, -120), (fx, -120)], hexc("#c9a64a"), seed=seed + 2 + k,
                        amp=0.5, lw=3.5)
            u = (t * 0.9 + k * 0.5 + seed * 0.13) % 1
            blob(cr, fx + 13 - u * 40, -140 - u * 60, 14 + u * 16, 12 + u * 12, hexc("#8a8a8a", 0.7 * (1 - u)),
                 seed=seed + 5 + k, amp=0.8, lw=0, stroke=None)
        line(cr, [(100, -30), (100, -150)], 3.5, INK, seed=seed + 8, amp=0.2)
        union_flag(cr, 100, -150, 44, 26, seed=seed + 9)
        line(cr, [(-150, -40), (-190, -52)], 7, INK, seed=seed + 10, amp=0.2)   # gun


def palace(cr, x, y, t, wreck, flag):
    with at(cr, x, y, 1.0, rot=0.05 * wreck):
        shape(cr, rrect_pts(-190, -260, 380, 260, 6, 20), PALACE, seed=5600, amp=0.8, lw=4.5)
        for r in range(3):
            for c in range(5):
                if wreck > 0.5 and (r * 5 + c) % 4 == 1:
                    continue
                shape(cr, [(-160 + c * 70, -30 - r * 80), (-160 + c * 70, -70 - r * 80), (-136 + c * 70, -86 - r * 80),
                           (-112 + c * 70, -70 - r * 80), (-112 + c * 70, -30 - r * 80)], hexc("#3aa0c8"),
                      seed=5610 + r * 5 + c, amp=0.5, lw=3)
        # tower + flagpole
        shape(cr, rrect_pts(-40, -380, 80, 130, 4, 16), PALACE, seed=5620, amp=0.6, lw=4)
        line(cr, [(0, -380), (0, -520)], 4, INK, seed=5621, amp=0.2)
        fy = lerp(-520, -400, flag)
        if flag < 1:
            sharp_shape(cr, [(0, fy), (70, fy + 6), (70, fy + 46), (0, fy + 40)], ZRED, seed=5622, amp=0.6, lw=3)
        if wreck > 0:
            for k in range(6):   # cracks
                x0 = -150 + k * 60
                line(cr, [(x0, -250), (x0 + 16, -200), (x0 - 6, -150), (x0 + 12, -100)], 3.5, INK, seed=5630 + k,
                     amp=0.8)
            for k in range(3):   # smoke
                u = (t * 0.7 + k / 3) % 1
                blob(cr, -120 + k * 110, -300 - u * 160, 30 + u * 30, 24 + u * 20, hexc("#6b6b6b", 0.6 * (1 - u) * wreck),
                     seed=5640 + k, amp=0.9, lw=0, stroke=None)


def scene_sea(cr, t, tl):
    A = tl.at
    fire = A("w5", "fire")
    keys = [(A("w5") - 0.2, (1.1, 360, 700)), (A("w5", "9:00"), (1.6, 600, 420)), (A("w5", "British"), (1.0, 200, 760)),
            (A("w5", "warships"), (1.5, -160, 860)), (A("w5", "open"), (1.2, 60, 780)),
            (fire, (0.8, 300, 700)), (A("w6", "9:40"), (1.3, 470, 560)), (A("w6", "wrecked"), (1.1, 560, 640)),
            (A("w6", "flag"), (1.6, 620, 360)), (A("w6", "new"), (1.3, 820, 800)), (A("w6", "escaped"), (1.6, 900, 820))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*SKY)
    cr.paint()
    blob(cr, 900, 250, 60, 60, hexc("#ffe28a"), seed=5700, amp=0.5, lw=3)
    sharp_shape(cr, [(-900, 820), (380, 820), (380, 1900), (-900, 1900)], SEA, seed=5701, amp=0.8, lw=0, stroke=None)
    for k in range(10):   # waves
        wx = -800 + k * 120 + (t * 30) % 120
        line(cr, [(wx, 860 + (k % 3) * 60), (wx + 30, 848 + (k % 3) * 60), (wx + 60, 860 + (k % 3) * 60)], 3, WHITE,
             seed=5710 + k, amp=0.4)
    sharp_shape(cr, [(360, 830), (1600, 800), (1600, 1900), (320, 1900)], SAND, seed=5702, amp=1.0, lw=4)
    wreck = seg(t, A("w6", "wrecked") - 0.1, A("w6", "wrecked") + 0.4)
    flag = seg(t, A("w6", "flag"), A("w6", "down", end=True))
    palace(cr, 640, 820, t, wreck, flag)
    ships = ((-420, 900), (-160, 960), (100, 900))
    for i, (sx, sy) in enumerate(ships):
        warship(cr, sx, sy, t, 0.9, seed=5750 + i * 20)
    # the barrage: puffs, arcing shells and a BOOM now and then
    if t >= fire:
        for i, (sx, sy) in enumerate(ships):
            u = ((t - fire) * 1.6 + i * 0.33) % 1
            gx, gy = sx - 170 * 0.9 + 40, sy - 36
            blob(cr, gx - 30, gy, 26 * (1 - u) + 4, 20 * (1 - u) + 4, hexc("#d8d3c4", 1 - u), seed=5800 + i, amp=0.9,
                 lw=2.5)
            px, py = lerp(sx, 560 + i * 60, u), lerp(sy - 60, 700, u) - math.sin(u * math.pi) * 220
            dot(cr, px, py, 7, INK)
        for k in range(8):
            tb = fire + k * 0.45
            sc = pop(t, tb, 0.15) * (1 - seg(t, tb + 0.25, tb + 0.4))
            if sc > 0:
                with at(cr, 520 + (k * 97) % 240, 560 + (k * 53) % 200, sc, rot=((k % 3) - 1) * 0.2):
                    blob(cr, 0, 0, 70, 50, hexc("#ffd23f"), seed=5820 + k, amp=2.0, lw=4)
                    write(cr, [("BOOM", RED)], 0, 14, 40, align="center", bold=True)
                cue("hit", t, tb)
    # the new sultan slips out the back
    if t >= A("w6", "new"):
        run = seg(t, A("w6", "escaped"), A("w6", "back", end=True) + 0.3)
        person(cr, "claimant", lerp(830, 1060, run), 900, t, facing=1, walk=t * 3.2 if run > 0 else None,
               arms=("down", "down"), eyes="wide", mouth="o", sweat=True, scale=0.8)
    # clocks: 9:00 on the dot, and the minutes running in the corner
    mins = 38 * seg(t, fire, A("w6", end=True)) if t >= A("w5", "9:00") else 0
    cr.save()
    cr.identity_matrix()
    stopwatch(cr, 610, 420, 62, mins)
    cr.restore()
    hl(cr, t, [("9:00", RED)], 215, 90, A("w5", "9:00"), end=A("w5", "warships") - 0.05, bold=True)
    hl(cr, t, [("OPEN FIRE", RED)], 215, 84, fire, end=A("w6") - 0.05, bold=True)
    hl(cr, t, [("9:40", RED)], 215, 90, A("w6", "9:40"), end=A("w6", "wrecked") - 0.05, bold=True)
    hl(cr, t, [("palace: ", INK), ("wrecked", RED)], 215, 70, A("w6", "wrecked"), end=A("w6", "flag") - 0.05, bold=True)
    hl(cr, t, [("flag: ", INK), ("down", RED)], 215, 76, A("w6", "flag"), end=A("w6", "new") - 0.05, bold=True)
    hl(cr, t, [("...out the ", INK), ("back", RED)], 215, 76, A("w6", "escaped"), bold=True)


def scene_clock(cr, t, tl):
    A = tl.at
    cr.set_source_rgba(*hexc("#fbf3e1"))
    cr.paint()
    for k in range(24):   # sunburst so the reveal hits hard
        a = k * math.pi / 12 + t * 0.4
        cr.move_to(360, 640)
        cr.arc(360, 640, 1200, a, a + math.pi / 24)
        cr.close_path()
        cr.set_source_rgba(*hexc("#f7d774", 0.5))
        cr.fill()
    z = camera(t, [(A("w7") - 0.2, (0.85,)), (A("w7", "war"), (1.1,)), (A("w7", "over"), (0.95,)), (A("w7", "around"), (1.2,)),
                   (A("w7", "38"), (1.35,))], dur=0.15)[0]
    run = seg(t, A("w7"), A("w7", "38"))
    with at(cr, 360, 560, z):
        stopwatch(cr, 0, 0, 200, 38 * ease_out(run), label=False)
    if t >= A("w7", "38"):
        with at(cr, 360, 560, max(0.01, pop(t, A("w7", "38"), 0.25)) * z, rot=-0.06):
            write(cr, [("38", RED)], 0, 50, 190, align="center", bold=True, halo=WHITE)
        write(cr, [("MINUTES", INK)], 360, 1110, 70, align="center", bold=True, halo=WHITE)
        cue("hit", t, A("w7", "38"))
    hl(cr, t, [("WAR OVER", INK)], 215, 90, A("w7", "over"), bold=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "tv":
        scene_tv(cr, t, tl)
    elif name == "throne":
        scene_throne(cr, t, tl, 1)
    elif name == "letter":
        scene_letter(cr, t, tl)
    elif name == "throne2":
        scene_throne(cr, t, tl, 2)
    elif name == "sea":
        scene_sea(cr, t, tl)
    elif name == "clock":
        scene_clock(cr, t, tl)
    elif name == "throne3":
        scene_throne(cr, t, tl, 3)
    else:
        scene_tv(cr, t, tl, end=True)
    cr.restore()
    captions(cr, t, tl)
