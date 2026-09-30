"""Episode 19: "The Man Who Lied to Hitler" — Juan Pujol García ("Garbo").

Facts (Wikipedia, "Juan Pujol García"): approached the British embassy in Madrid three times from January 1941 and was
turned down; became a German (Abwehr) agent instead; stayed in Lisbon and invented reports from a tourist guide to
Britain, library reference books/magazines and cinema newsreels; the Germans eventually funded a network of 27
agents, all fictitious, paying him US$340,000 over the war; MI5 later ran him as "Garbo"; in Operation Fortitude he
told the Germans Normandy was a diversion, and they held back reinforcements; Iron Cross Second Class (29 July 1944)
and MBE (25 November 1944); faked his death from malaria in Angola in 1949, moved to Venezuela; found by Nigel West
(Rupert Allason) and met him in 1984 (35 years later). The Iron Cross is drawn as a plain cross with no symbols.
"""
import math

from motion.captions import captions
from motion.characters import cash, money_pile, person
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, confetti, enter_world, hl, sepia, set_camera, stamp, whip
from videos.shortest_war import union_flag

NARRATOR = dict(speed=1.04)
TAIL = 0.8

SCRIPT = [
    dict(id="d1", scene="hook", text="During World War Two, one man lied to the Nazis so well, they gave him a medal."),
    dict(id="d2", scene="office",
         text="His name was Juan Pujol. He hated the Nazis, so he offered to spy for Britain. They said no. "
              "[Three times.|3 times.]"),
    dict(id="d3", scene="office", text="So he tried the other side. The Germans hired him, and sent him to spy on London."),
    dict(id="d4", scene="lisbon",
         text="He never went. He stayed in Lisbon, and made everything up, from a tourist guidebook, library "
              "magazines, and movie newsreels."),
    dict(id="d5", scene="network",
         text="Then he invented spies. By the end, the Germans were paying for [twenty-seven|27] agents. None of "
              "them existed."),
    dict(id="d6", scene="network", text="They paid him about [three hundred forty thousand dollars.|$340,000.]"),
    dict(id="d7", scene="dday",
         text="Britain finally hired him for real. And on D-Day, he told the Germans Normandy was just a trick. "
              "They held back their troops."),
    dict(id="d8", scene="medals",
         text="Here's the twist. Germany gave him the Iron Cross. And Britain gave him a royal medal too. From both "
              "sides, in the same war."),
    dict(id="d9", scene="end",
         text="Then he faked his own death, vanished to Venezuela, and was found [thirty-five years later.|35 years "
              "later.]", gap=0.2),
]

METADATA = dict(
    title="He Lied to the Nazis So Well, They Gave Him a Medal 🎖️",
    alt_titles=["The Spy Who Invented 27 Fake Spies 🕵️", "He Got Medals From BOTH Sides of WW2 😳"],
    description="""During World War Two, Juan Pujol lied to the Nazis so well that they gave him the Iron Cross. 🎖️

Britain turned him down 3 times, so he got hired by the Germans instead… then never went to London. He made everything up from a tourist guidebook and newsreels, and invented 27 spies who never existed. On D-Day, he helped convince the Germans that Normandy was just a trick.

His reward? A medal from Germany AND one from Britain. Then he faked his own death. 🕵️

💬 Greatest liar in history? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#History", "#WW2", "#Spy"],
    tags=["juan pujol garcia", "garbo spy", "double agent", "ww2 history", "d-day", "spy story", "history facts",
          "weird history", "history shorts", "interestingly strange"],
    pinned_comment="Imagine getting a medal from BOTH sides of a war 😳 Greatest liar ever? 👇",
)

GOLD = hexc("#f2b632")
NAVY = hexc("#23346b")
GREEN = hexc("#3d8f45")
GREY = hexc("#6b6f78")
SEA = hexc("#3aa0c8")
MAN = "pujol"


def iron_cross(cr, x, y, s=1.0, seed=0):
    with at(cr, x, y, s):
        pts = [(-12, -60), (12, -60), (22, -24), (60, -12), (60, 12), (22, 24), (12, 60), (-12, 60), (-22, 24),
               (-60, 12), (-60, -12), (-22, -24)]
        sharp_shape(cr, pts, INK, seed=seed, amp=0.4, lw=5, stroke=hexc("#c7c2cc"))
        line(cr, [(0, -60), (0, -100)], 10, hexc("#c0504d"), seed=seed + 1, amp=0.2)


def royal_medal(cr, x, y, s=1.0, seed=0):
    with at(cr, x, y, s):
        sharp_shape(cr, [(-26, -110), (26, -110), (20, -40), (-20, -40)], hexc("#e0487a"), seed=seed, amp=0.3, lw=3)
        blob(cr, 0, 0, 46, 46, GOLD, seed=seed + 1, amp=0.4, lw=4)
        write(cr, [("MBE", INK)], 0, 12, 28, align="center", bold=True)


def typewriter(cr, x, y, t, seed=0):
    shape(cr, rrect_pts(x - 90, y - 50, 180, 70, 12, 14), hexc("#555a66"), seed=seed, amp=0.5, lw=4)
    shape(cr, rrect_pts(x - 60, y - 130, 120, 90, 4, 14), WHITE, seed=seed + 1, amp=0.4, lw=3)
    for k in range(3):
        line(cr, [(x - 48, y - 110 + k * 18), (x - 48 + 90 * min(1, (t * 1.5 + k * 0.3) % 1.3), y - 110 + k * 18)], 2.5,
             INK, seed=seed + 2 + k, amp=0.2)
    for k in range(6):
        dot(cr, x - 60 + k * 24, y - 10, 6, WHITE)


def scene_hook(cr, t, tl):
    A = tl.at
    cr.set_source_rgba(*hexc("#f7d774"))
    cr.paint()
    keys = [(0, (1.9, 360, 720)), (A("d1", "World"), (1.3, 360, 700)), (A("d1", "Two"), (2.3, 330, 700)),
            (A("d1", "man"), (1.5, 400, 660)), (A("d1", "lied"), (1.1, 400, 680)), (A("d1", "Nazis"), (1.8, 520, 560)),
            (A("d1", "well"), (1.3, 420, 620)), (A("d1", "gave"), (2.0, 330, 700)), (A("d1", "medal"), (1.5, 400, 640))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    for k in range(20):   # sunburst inside the camera, so every zoom reads
        a = k * math.pi / 10 + t * 0.4
        cr.move_to(360, 700)
        cr.arc(360, 700, 1600, a, a + math.pi / 20)
        cr.close_path()
        cr.set_source_rgba(*hexc("#f2a93b", 0.55))
        cr.fill()
    person(cr, MAN, 330, 905, t, facing=1, arms=("thumb", "hip"), eyes="sly", mouth="smirk")
    # a Pinocchio-style nose meter: the lie gauge
    if t >= A("d1", "lied"):
        with at(cr, 580, 520, pop(t, A("d1", "lied"), 0.2) or 0.01):
            shape(cr, rrect_pts(-80, -150, 160, 300, 14, 16), WHITE, seed=16000, amp=0.5, lw=4)
            write(cr, [("LIE-O-METER", INK)], 0, -110, 22, align="center", bold=True)
            lvl = min(1.0, 0.3 + (t - A("d1", "lied")) * 0.8)
            shape(cr, rrect_pts(-40, 120 - 200 * lvl, 80, 200 * lvl, 8, 12), RED, seed=16001, amp=0.4, lw=3)
    if t >= A("d1", "medal"):
        iron_cross(cr, 420, 760, 0.9 * (pop(t, A("d1", "medal"), 0.25) or 0.01), seed=16010)
        cue("kaching", t, A("d1", "medal"))
    hl(cr, t, [("WW2", RED)], 215, 96, 0.0, end=A("d1", "man") - 0.05, bold=True, sound=False)
    hl(cr, t, [("lied so well...", INK)], 215, 80, A("d1", "lied"), end=A("d1", "medal") - 0.05, bold=True)
    hl(cr, t, [("they gave him a ", INK), ("MEDAL", GOLD)], 215, 70, A("d1", "medal"), bold=True)


def scene_office(cr, t, tl):
    A = tl.at
    keys = [(A("d2") - 0.2, (1.1, 360, 740)), (A("d2", "name"), (1.6, 260, 720)), (A("d2", "Juan"), (2.2, 240, 690)),
            (A("d2", "Pujol"), (1.5, 280, 720)), (A("d2", "hated"), (1.2, 330, 700)), (A("d2", "Nazis"), (1.8, 420, 560)),
            (A("d2", "offered"), (1.3, 380, 720)), (A("d2", "spy"), (1.8, 260, 700)), (A("d2", "Britain"), (1.4, 520, 640)), (A("d2", "no"), (1.9, 560, 700)), (A("d2", "3"), (1.2, 400, 700)),
            (A("d3", "other"), (1.4, 400, 740)), (A("d3", "Germans"), (1.8, 560, 640)), (A("d3", "hired"), (1.2, 480, 680)),
            (A("d3", "sent"), (2.0, 560, 600)), (A("d3", "spy"), (1.3, 420, 700)), (A("d3", "London"), (2.1, 560, 720))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#e9d3ae"))
    cr.paint()
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#b98a5a"), seed=16100, amp=1, lw=4)
    rejected = A("d2", "no") <= t < A("d3")
    if t < A("d3"):
        # the British embassy door, with a NO sign
        shape(cr, rrect_pts(470, 480, 200, 420, 8, 18), hexc("#6b4a2e"), seed=16110, amp=0.6, lw=4)
        union_flag(cr, 500, 400, 140, 84, seed=16111)
        if rejected:
            n = 3 if t >= A("d2", "3") else 1 + int(2 * seg(t, A("d2", "no"), A("d2", "3")))
            for k in range(n):
                with at(cr, 570, 620 + k * 90, pop(t, A("d2", "no") + k * 0.25, 0.2) or 0.01, rot=-0.1 + k * 0.1):
                    shape(cr, rrect_pts(-80, -34, 160, 68, 10, 14), RED, seed=16120 + k, amp=0.5, lw=3.5)
                    write(cr, [("NO", WHITE)], 0, 16, 48, align="center", bold=True)
                cue("hit", t, A("d2", "no") + k * 0.25)
    else:
        # the other side: a letter of acceptance, 'from Berlin'
        with at(cr, 560, 640, pop(t, A("d3", "Germans"), 0.2) or 0.01, rot=0.06):
            shape(cr, rrect_pts(-120, -150, 240, 300, 6, 16), WHITE, seed=16130, amp=0.5, lw=4)
            write(cr, [("FROM: BERLIN", INK)], 0, -100, 26, align="center", bold=True)
            write(cr, [("You're hired.", INK)], 0, -40, 28, align="center")
            write(cr, [("Target:", INK)], 0, 20, 26, align="center")
            write(cr, [("LONDON", RED)], 0, 70, 44, align="center", bold=True)
    if A("d2", "hated") <= t < A("d2", "offered"):   # no to the Nazis: a prohibition sign, no symbols
        with at(cr, 420, 560, pop(t, A("d2", "hated"), 0.2) or 0.01):
            blob(cr, 0, 0, 110, 110, WHITE, seed=16140, amp=0.5, lw=0, stroke=None)
            write(cr, [("NAZIS", INK)], 0, 16, 48, align="center", bold=True)
            cr.set_source_rgba(*RED)
            cr.set_line_width(22)
            cr.arc(0, 0, 110, 0, 2 * math.pi)
            cr.stroke()
            line(cr, [(-78, -78), (78, 78)], 22, RED, seed=16141, amp=0.1)
    person(cr, MAN, 240, 905, t, facing=1, arms=("wave", "hip") if t < A("d2", "no") else
           (("face", "hip") if rejected else ("thumb", "hip")), eyes="happy" if not rejected else "sad",
           mouth="grin" if not rejected else "wobble")
    sepia(cr, 0.3)
    hl(cr, t, [("Juan ", INK), ("Pujol", RED)], 215, 90, A("d2", "Juan"), end=A("d2", "Britain") - 0.05, bold=True)
    hl(cr, t, [("Britain: ", INK), ("NO", RED), (" x3", INK)], 215, 84, A("d2", "no"), end=A("d3") - 0.05, bold=True)
    hl(cr, t, [("hired by ", INK), ("the Germans", GREY)], 215, 70, A("d3", "Germans"), bold=True)


def scene_lisbon(cr, t, tl):
    A = tl.at
    keys = [(A("d4") - 0.2, (1.6, 360, 700)), (A("d4", "never"), (2.2, 330, 690)), (A("d4", "Lisbon"), (0.9, 380, 640)),
            (A("d4", "made"), (1.6, 300, 720)), (A("d4", "guidebook"), (1.9, 520, 620)), (A("d4", "library"), (1.6, 160, 560)),
            (A("d4", "newsreels"), (1.8, 560, 440))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#f3d9a4"))
    cr.paint()
    for k in range(-4, 12):   # Lisbon tiles
        for j in range(8):
            if (k + j) % 2:
                shape(cr, rrect_pts(k * 90, 300 + j * 80, 80, 70, 6, 10), hexc("#bfd7ef"), seed=16200 + k * 10 + j,
                      amp=0.3, lw=2)
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#b0773f"), seed=16201, amp=1, lw=4)
    write(cr, [("LISBON", NAVY)], 360, 370, 60, align="center", bold=True, halo=WHITE)
    # desk + typewriter
    person(cr, MAN, 420, 905, t, facing=-1, arms=("give", "give"), eyes="sly", mouth="smirk")
    shape(cr, rrect_pts(150, 820, 330, 90, 8, 16), hexc("#6d4524"), seed=16210, amp=0.6, lw=4)
    typewriter(cr, 270, 820, t, seed=16220)
    if t >= A("d4", "guidebook"):   # the tourist guide
        with at(cr, 520, 640, pop(t, A("d4", "guidebook"), 0.2) or 0.01, rot=0.12):
            shape(cr, rrect_pts(-80, -100, 160, 200, 8, 14), hexc("#3d8f45"), seed=16230, amp=0.5, lw=4)
            write(cr, [("GUIDE TO", WHITE)], 0, -40, 26, align="center", bold=True)
            write(cr, [("BRITAIN", GOLD)], 0, 0, 32, align="center", bold=True)
            write(cr, [("for tourists", WHITE)], 0, 50, 20, align="center")
    if t >= A("d4", "library"):   # magazines
        with at(cr, 160, 560, pop(t, A("d4", "library"), 0.2) or 0.01, rot=-0.1):
            for k in range(3):
                shape(cr, rrect_pts(-70 + k * 12, -90 + k * 10, 140, 180, 4, 12), [hexc("#e0487a"), hexc("#3f6fb5"),
                                                                                   WHITE][k], seed=16240 + k, amp=0.4, lw=3)
            write(cr, [("MAGAZINE", INK)], 24, -30, 22, align="center", bold=True)
    if t >= A("d4", "newsreels"):   # film reel
        with at(cr, 560, 440, pop(t, A("d4", "newsreels"), 0.2) or 0.01, rot=t * 2):
            blob(cr, 0, 0, 60, 60, INK, seed=16250, amp=0.3, lw=3)
            for k in range(5):
                a = k * 2 * math.pi / 5
                blob(cr, 32 * math.cos(a), 32 * math.sin(a), 12, 12, hexc("#c7c2cc"), seed=16251 + k, amp=0.2, lw=0,
                     stroke=None)
    if A("d4", "never") <= t < A("d4", "Lisbon"):
        stamp(cr, t, A("d4", "never"), "NEVER WENT", dur=0.8, y=470)
    sepia(cr, 0.3)
    hl(cr, t, [("made it ", INK), ("ALL UP", RED)], 215, 90, A("d4", "made"), bold=True)


def scene_network(cr, t, tl):
    A = tl.at
    keys = [(A("d5") - 0.2, (1.0, 360, 640)), (A("d5", "invented"), (1.6, 360, 520)), (A("d5", "spies"), (2.4, 360, 640)),
            (A("d5", "end"), (1.2, 360, 600)), (A("d5", "Germans"), (1.8, 560, 700)), (A("d5", "paying"), (1.3, 300, 640)),
            (A("d5", "27"), (0.9, 360, 640)),
            (A("d5", "none"), (1.5, 360, 700)), (A("d5", "existed"), (1.1, 360, 640)), (A("d6", "paid"), (1.4, 360, 800)),
            (A("d6", "$340,000"), (1.1, 360, 700)),
            (A("d6", "$340,000") + 0.8, (1.8, 360, 900)), (A("d6", "$340,000") + 1.5, (1.0, 360, 640))]
    z, fx, fy = camera(t, keys, dur=0.15)
    cr.set_source_rgba(*hexc("#e9e2d0"))
    cr.paint()
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    shape(cr, rrect_pts(20, 330, 680, 660, 10, 20), hexc("#b98a5a"), seed=16300, amp=0.8, lw=5)   # cork board
    # the spider: Pujol's photo in the middle, 27 fake agents pinned around with red string
    n = int(27 * seg(t, A("d5", "invented"), A("d5", "27", end=True) + 0.3))
    cx, cy = 360, 640
    for k in range(n):
        a = k * 2 * math.pi / 27
        r = 230 + (k % 3) * 40
        x, y = cx + r * math.cos(a) * 1.15, cy + r * math.sin(a)
        line(cr, [(cx, cy), (x, y)], 2, RED, seed=16310 + k, amp=0.3)
        shape(cr, rrect_pts(x - 26, y - 30, 52, 60, 3, 8), WHITE, seed=16340 + k, amp=0.3, lw=2)
        blob(cr, x, y - 6, 12, 12, hexc("#c7c2cc"), seed=16370 + k, amp=0.3, lw=2)
        write(cr, [("?", INK)], x, y + 2, 20, align="center", bold=True)
        if t >= A("d5", "none"):
            line(cr, [(x - 24, y - 26), (x + 24, y + 26)], 4, RED, seed=16400 + k, amp=0.2)
    shape(cr, rrect_pts(cx - 60, cy - 70, 120, 140, 4, 12), WHITE, seed=16430, amp=0.4, lw=3)
    person(cr, MAN, cx, cy + 90, t, facing=1, scale=0.45, eyes="sly", mouth="smirk")
    write(cr, [(str(n), RED)], 600, 400, 56, align="center", bold=True, halo=WHITE)
    if t >= A("d6", "paid"):
        money_pile(cr, 360, 940, 0.9, seed=16440)
    sepia(cr, 0.25)
    hl(cr, t, [("27", RED), (" fake spies", INK)], 215, 90, A("d5", "27"), end=A("d6") - 0.05, bold=True)
    hl(cr, t, [("~$340,000", GREEN), (" paid", INK)], 215, 80, A("d6", "$340,000"), bold=True)
    if t >= A("d5", "none"):
        stamp(cr, t, A("d5", "none"), "NONE EXISTED", dur=0.9, y=470)


def scene_dday(cr, t, tl):
    A = tl.at
    keys = [(A("d7") - 0.2, (1.4, 260, 420)), (A("d7", "real"), (1.9, 260, 380)), (A("d7", "D-Day"), (1.0, 380, 620)),
            (A("d7", "Normandy"), (1.6, 300, 660)), (A("d7", "just"), (1.1, 360, 700)), (A("d7", "trick"), (1.5, 470, 560)), (A("d7", "held"), (1.1, 400, 620))]
    z, fx, fy = camera(t, keys, dur=0.15)
    cr.set_source_rgba(*SEA)
    cr.paint()
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    # simple map: English coast at top, French coast at bottom
    blob(cr, 360, 330, 520, 150, hexc("#b9d99a"), seed=16500, amp=6, lw=4)
    write(cr, [("BRITAIN", INK)], 360, 330, 44, align="center", bold=True)
    blob(cr, 360, 980, 640, 220, hexc("#e9d9a8"), seed=16501, amp=6, lw=4)
    write(cr, [("FRANCE", INK)], 360, 1050, 44, align="center", bold=True)
    dot(cr, 250, 820, 12, RED)
    write(cr, [("Normandy", RED)], 250, 800, 30, align="center", bold=True)
    dot(cr, 520, 760, 12, NAVY)
    write(cr, [("Calais", NAVY)], 520, 740, 30, align="center", bold=True)
    u = seg(t, A("d7", "D-Day"), A("d7", "D-Day") + 0.6)
    if u > 0:   # the real landing
        line(cr, [(300, 430), (lerp(300, 250, u), lerp(430, 800, u))], 8, RED, seed=16510, amp=0.4)
    if t >= A("d7", "trick"):   # the fake threat he sold
        for k in range(3):
            line(cr, [(420 + k * 30, 430), (500 + k * 10, 730)], 5, hexc("#23346b", 0.6), seed=16520 + k, amp=0.4)
        write(cr, [("the REAL attack?", NAVY)], 560, 600, 30, align="center", bold=True, halo=WHITE)
        with at(cr, 250, 880, 1.0):
            write(cr, [("\"just a trick\"", INK)], 0, 0, 30, align="center", bold=True, halo=WHITE)
    if t >= A("d7", "held"):   # tanks waiting at Calais
        for k in range(3):
            shape(cr, rrect_pts(470 + k * 50, 830, 40, 24, 4, 8), GREY, seed=16530 + k, amp=0.3, lw=2.5)
        write(cr, [("waiting...", GREY)], 540, 900, 26, align="center", bold=True)
    if t < A("d7", "D-Day"):
        with at(cr, 250, 420, 1.0):
            person(cr, MAN, 0, 0, t, facing=1, scale=0.6, arms=("thumb", "hip"), eyes="happy", mouth="grin")
            union_flag(cr, 50, -190, 80, 48, seed=16540)
    sepia(cr, 0.2)
    hl(cr, t, [("D-DAY", RED)], 215, 96, A("d7", "D-Day"), end=A("d7", "trick") - 0.05, bold=True)
    hl(cr, t, [("Normandy = ", INK), ("\"a trick\"", RED)], 215, 72, A("d7", "trick"), end=A("d7", "held") - 0.05, bold=True)
    hl(cr, t, [("troops ", INK), ("held back", NAVY)], 215, 80, A("d7", "held"), bold=True)


def scene_medals(cr, t, tl):
    A = tl.at
    keys = [(A("d8") - 0.2, (1.2, 360, 700)), (A("d8", "twist"), (1.6, 360, 640)), (A("d8", "Germany"), (1.8, 220, 600)),
            (A("d8", "gave"), (1.2, 300, 680)), (A("d8", "Iron"), (2.3, 200, 580)), (A("d8", "Cross"), (1.5, 220, 640)),
            (A("d8", "Britain"), (1.8, 500, 600)), (A("d8", "royal"), (2.3, 520, 580)), (A("d8", "too"), (1.3, 400, 660)),
            (A("d8", "from"), (2.1, 360, 720)), (A("d8", "sides"), (1.0, 360, 660)), (A("d8", "same"), (1.8, 360, 640)), (A("d8", "both"), (1.1, 360, 680)), (A("d8", "same"), (1.4, 360, 700))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#fbf3e1"))
    cr.paint()
    cr.save()
    cr.rectangle(-600, -600, 960, 2600)
    cr.clip()
    cr.set_source_rgba(*hexc("#d9d4c7"))
    cr.paint()
    cr.restore()
    cr.set_source_rgba(*hexc("#d6e2f5"))
    cr.rectangle(360, -600, 1200, 2600)
    cr.fill()
    person(cr, MAN, 360, 905, t, facing=1, arms=("cheer", "cheer") if t >= A("d8", "both") else ("hip", "hip"),
           eyes="happy", mouth="grin", jump=abs(math.sin(t * 8)) * 10 if t >= A("d8", "both") else 0)
    if t >= A("d8", "Germany"):
        iron_cross(cr, 200, 560, 1.3 * (pop(t, A("d8", "Germany"), 0.25) or 0.01), seed=16600)
        write(cr, [("IRON CROSS", INK)], 200, 690, 30, align="center", bold=True)
        write(cr, [("Germany, 1944", GREY)], 200, 726, 24, align="center")
    if t >= A("d8", "Britain"):
        royal_medal(cr, 520, 580, 1.3 * (pop(t, A("d8", "Britain"), 0.25) or 0.01), seed=16610)
        write(cr, [("MBE", NAVY)], 520, 690, 30, align="center", bold=True)
        write(cr, [("Britain, 1944", GREY)], 520, 726, 24, align="center")
    if t >= A("d8", "both"):
        confetti(cr, t, A("d8", "both"))
        cue("kaching", t, A("d8", "both"))
    hl(cr, t, [("the ", INK), ("TWIST", RED)], 215, 96, A("d8", "twist"), end=A("d8", "both") - 0.05, bold=True)
    hl(cr, t, [("medals from ", INK), ("BOTH SIDES", RED)], 215, 66, A("d8", "both"), bold=True, underline=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("d9") - 0.2, (1.4, 250, 700)), (A("d9", "faked"), (1.0, 300, 720)), (A("d9", "own"), (2.2, 220, 760)),
            (A("d9", "death"), (1.6, 220, 700)), (A("d9", "vanished"), (1.0, 380, 700)), (A("d9", "Venezuela"), (1.5, 500, 640)),
            (A("d9", "found"), (1.9, 470, 600)), (A("d9", "35"), (1.1, 400, 700)), (A("d9", "35") + 0.8, (1.6, 470, 620))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#bfe6ff"))
    cr.paint()
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#e9d9a8"), seed=16700, amp=1, lw=4)
    # the fake grave
    shape(cr, [(140, 900), (140, 700), (220, 640), (300, 700), (300, 900)], hexc("#a9a2ae"), seed=16710, amp=0.6, lw=4)
    write(cr, [("R.I.P.", INK)], 220, 750, 36, align="center", bold=True)
    write(cr, [("1949", INK)], 220, 800, 30, align="center")
    if t >= A("d9", "faked"):
        write(cr, [("(not really)", RED)], 220, 850, 24, align="center", bold=True)
    # Venezuela palm + Pujol in a sun hat
    if t >= A("d9", "Venezuela"):
        line(cr, [(560, 900), (590, 620)], 12, hexc("#8e5a2e"), seed=16720, amp=0.5)
        for k in range(5):
            a = -math.pi / 2 + (k - 2) * 0.55
            line(cr, [(590, 620), (590 + 110 * math.cos(a), 620 + 110 * math.sin(a) + 50)], 16, GREEN, seed=16721 + k,
                 amp=0.8)
        write(cr, [("VENEZUELA", GREEN)], 480, 460, 44, align="center", bold=True, halo=WHITE)
        person(cr, MAN, 470, 905, t, facing=-1, arms=("hip", "hip"), eyes="sly", mouth="smirk")
    if t >= A("d9", "found"):
        with at(cr, 470, 560, pop(t, A("d9", "found"), 0.2) or 0.01):
            shape(cr, rrect_pts(-110, -40, 220, 80, 12, 14), INK, seed=16730, amp=0.4, lw=0, stroke=None)
            write(cr, [("FOUND: 1984", GOLD)], 0, 14, 34, align="center", bold=True)
    hl(cr, t, [("faked his ", INK), ("DEATH", RED)], 215, 84, A("d9", "death"), end=A("d9", "found") - 0.05, bold=True)
    hl(cr, t, [("found ", INK), ("35 years", RED), (" later", INK)], 215, 70, A("d9", "found"), bold=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "office": scene_office, "lisbon": scene_lisbon, "network": scene_network, "dday": scene_dday,
     "medals": scene_medals, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
