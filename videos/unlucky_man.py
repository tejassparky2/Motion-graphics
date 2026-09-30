"""Episode 14: "The Unluckiest (or Luckiest) Man Alive" — Frane Selak, following the reference Short's story beats.

Facts (Wikipedia, "Frane Selak"): Croatian, born 1929. Claimed: 1962 train into the Neretva river (swam out); 1963
fell from a plane into a haystack; 1966 bus into a river; car fires (1970/72 and 1973); hit by a bus in Zagreb in 1995
(minor injuries); 1996 thrown from his car on a mountain road, clinging to a tree while the car fell 150 m; lottery
win in 2002/2003 of 6-7 million kuna (about EUR 800-900k, "nearly a million dollars"). Wikipedia: "None of Selak's
near-death experiences have ever been independently verified" (and there are no records of the 1963 plane incident).
So the script tells it as his story, and the twist ending says so. Deaths in the claimed crashes are not dramatised.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.critters import car
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, smooth, write)
from motion.kit import camera, confetti, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict(speed=1.08)
TAIL = 0.8

SCRIPT = [
    dict(id="u1", scene="intro",
         text="Meet Frane Selak. He might be the unluckiest man who ever lived. Or the luckiest."),
    dict(id="u2", scene="train",
         text="[Nineteen sixty-two.|1962.] His train flies off a bridge, into an icy river. He swims to shore."),
    dict(id="u3", scene="plane",
         text="[Nineteen sixty-three.|1963.] On his first ever flight, a door blows open, and he gets sucked out. "
              "He lands, in a haystack."),
    dict(id="u4", scene="bus", text="[Nineteen sixty-six.|1966.] His bus skids into a river. He swims out. Again."),
    dict(id="u5", scene="car",
         text="So he decides: no more public transport. He buys a car. It catches fire. [Twice.|TWICE.]"),
    dict(id="u6", scene="street", text="In [ninety-five,|1995,] a bus hits him. Just a few bruises."),
    dict(id="u7", scene="cliff",
         text="In [ninety-six,|1996,] his car goes off a mountain road. He's thrown out, and grabs a tree, as his car "
              "drops [a hundred and fifty meters.|150 meters.]"),
    dict(id="u8", scene="lottery", text="Then, he buys a lottery ticket, and wins nearly a million dollars."),
    dict(id="u9", scene="end",
         text="Here's the strange part. None of his accidents were ever officially confirmed. So: unluckiest man "
              "alive, or the best storyteller?", gap=0.22),
]

METADATA = dict(
    title="The Unluckiest (or Luckiest) Man Alive 😳🍀",
    alt_titles=["He Survived 7 Disasters… Then Won the Lottery 🍀", "Train, Plane, Bus, Cliff… He Survived ALL of It? 😳"],
    description="""A train into an icy river. A fall from a plane into a haystack. A bus into a river. Two car fires. Hit by a bus. Thrown from a car on a mountain road… and then a lottery win of nearly a million dollars. 😳🍀

That's the story Croatian music teacher Frane Selak told the world. The strange part? None of his near-death experiences were ever independently verified.

💬 Unluckiest man alive, luckiest man alive… or the best storyteller? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Storytime", "#TrueStory", "#Luck"],
    tags=["frane selak", "unluckiest man", "luckiest man alive", "survived everything", "lottery win", "true story",
          "weird history", "storytime", "near death", "interestingly strange"],
    pinned_comment="Be honest: unluckiest, luckiest… or best storyteller? 🤔👇",
)

MAN = "oldman"
RIVER = hexc("#3aa0c8")
GREEN = hexc("#3d8f45")
GOLD = hexc("#f2b632")
HAY = hexc("#e8c46a")
SKY = hexc("#bfe6ff")


def counter(cr, t, n, start):
    """Running 'near-death' tally in the top-right corner (screen space)."""
    cr.save()
    cr.identity_matrix()
    sc = 1 + 0.25 * max(0.0, 1 - (t - start) / 0.25) if t >= start else 1
    with at(cr, 590, 400, 1.3 * sc):
        shape(cr, rrect_pts(-90, -60, 180, 120, 18, 16), INK, seed=11000, amp=0.6, lw=0, stroke=None)
        write(cr, [("SURVIVED", GOLD)], 0, -22, 24, align="center", bold=True)
        write(cr, [(str(n), WHITE)], 0, 44, 64, align="center", bold=True)
    cr.restore()


def year(cr, t, start, txt):
    stamp(cr, t, start, txt, dur=0.7, y=500)


def river_scene(cr, t, bridge=True):
    cr.set_source_rgba(*SKY)
    cr.paint()
    for k in range(-4, 12):
        sharp_shape(cr, [(k * 160 - 80, 700), (k * 160, 520 - (k % 3) * 60), (k * 160 + 80, 700)], hexc("#8aa0b8"),
                    seed=11100 + k, amp=0.8, lw=3)
    sharp_shape(cr, [(-900, 700), (1700, 700), (1700, 1900), (-900, 1900)], RIVER, seed=11101, amp=0.8, lw=0, stroke=None)
    for k in range(14):
        wx = -600 + k * 120 + (t * 40) % 120
        line(cr, [(wx, 760 + (k % 4) * 70), (wx + 30, 748 + (k % 4) * 70), (wx + 60, 760 + (k % 4) * 70)], 3, WHITE,
             seed=11110 + k, amp=0.4)
    if bridge:
        sharp_shape(cr, [(-900, 600), (1700, 600), (1700, 630), (-900, 630)], hexc("#8e5a2e"), seed=11120, amp=0.4, lw=4)
        for k in range(-4, 10):
            line(cr, [(k * 200, 630), (k * 200, 700)], 8, hexc("#6b4a2e"), seed=11121 + k, amp=0.3)


def swimmer(cr, x, y, t, seed=0):
    person(cr, MAN, x, y, t, facing=1, arms=("cheer", "wave"), eyes="wide", mouth="o", scale=0.7)
    cr.set_source_rgba(*RIVER)
    cr.rectangle(x - 80, y - 60, 160, 120)
    cr.fill()
    for k in range(3):
        line(cr, [(x - 60 + k * 40, y - 60), (x - 40 + k * 40, y - 70), (x - 20 + k * 40, y - 60)], 3, WHITE,
             seed=seed + k, amp=0.3)


def train_car(cr, x, y, s=1.0, rot=0.0, seed=0):
    with at(cr, x, y, s, rot=rot):
        shape(cr, rrect_pts(-150, -110, 300, 110, 14, 18), hexc("#c0504d"), seed=seed, amp=0.6, lw=4)
        for k in range(4):
            shape(cr, rrect_pts(-130 + k * 70, -90, 50, 40, 6, 10), hexc("#bfe6ef"), seed=seed + 1 + k, amp=0.3, lw=3)
        for wx in (-100, 100):
            blob(cr, wx, 0, 22, 22, INK, seed=seed + 10 + wx, amp=0.3, lw=3)


def bus(cr, x, y, s=1.0, rot=0.0, seed=0, facing=1):
    with at(cr, x, y, s, rot=rot, flip=facing < 0):
        shape(cr, rrect_pts(-200, -150, 400, 150, 20, 20), hexc("#ffc93c"), seed=seed, amp=0.8, lw=4.5)
        for k in range(5):
            shape(cr, rrect_pts(-170 + k * 70, -130, 52, 50, 6, 10), hexc("#bfe6ef"), seed=seed + 1 + k, amp=0.3, lw=3)
        shape(cr, rrect_pts(170, -130, 26, 80, 6, 10), hexc("#bfe6ef"), seed=seed + 9, amp=0.3, lw=3)
        for wx in (-120, 120):
            blob(cr, wx, 0, 30, 30, INK, seed=seed + 10 + wx, amp=0.3, lw=3)
            blob(cr, wx, 0, 12, 12, hexc("#a9a2ae"), seed=seed + 11 + wx, amp=0.2, lw=2)


def flames(cr, x, y, t, s=1.0, seed=0):
    for k in range(6):
        u = (t * 2.5 + k / 6) % 1
        with at(cr, x + (k - 3) * 30 * s, y - u * 120 * s, s * (1 - u * 0.6)):
            sharp_shape(cr, [(-22, 0), (0, -60), (22, 0)], hexc("#ff6b2b") if k % 2 else hexc("#ffd23f"),
                        seed=seed + k, amp=1.5, lw=2.5)


# ------------------------------------------------------------------ scenes
def scene_intro(cr, t, tl):
    A = tl.at
    keys = [(0, (1.8, 360, 700)), (A("u1", "Frane"), (1.3, 360, 740)), (A("u1", "might"), (2.2, 360, 700)),
            (A("u1", "unluckiest"), (1.5, 280, 700)), (A("u1", "ever"), (2.3, 330, 690)), (A("u1", "lived"), (1.4, 300, 720)),
            (A("u1", "luckiest", nth=2), (2.0, 440, 700))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    unlucky = A("u1", "unluckiest") <= t < A("u1", "luckiest", nth=2)
    lucky = t >= A("u1", "luckiest", nth=2)
    cr.set_source_rgba(*(hexc("#9aa3b8") if unlucky else (hexc("#c9f0c4") if lucky else hexc("#fbf3e1"))))
    cr.paint()
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#b98a5a"), seed=11200, amp=1, lw=4)
    if unlucky:   # storm cloud over his head
        blob(cr, 280, 470, 150, 70, hexc("#555a66"), seed=11201, amp=2.0, lw=4)
        for k in range(6):
            u = (t * 3 + k / 6) % 1
            line(cr, [(200 + k * 30, 540 + u * 200), (196 + k * 30, 560 + u * 200)], 4, RIVER, seed=11202 + k, amp=0.1)
    if lucky:   # four-leaf clover sparkle
        for k in range(4):
            a = k * math.pi / 2 + t
            blob(cr, 470 + 30 * math.cos(a), 480 + 30 * math.sin(a), 26, 26, GREEN, seed=11210 + k, amp=0.6, lw=3)
    person(cr, MAN, 360, 905, t, facing=1, arms=("down", "down") if unlucky else (("cheer", "cheer") if lucky else
                                                                              ("wave", "hip")),
           eyes="sad" if unlucky else ("happy" if lucky else "dot"), mouth="wobble" if unlucky else "grin",
           tears=unlucky, jump=abs(math.sin(t * 8)) * 12 if lucky else 0)
    hl(cr, t, [("Frane ", INK), ("Selak", RED)], 215, 84, A("u1", "Frane"), end=A("u1", "unluckiest") - 0.05, bold=True)
    hl(cr, t, [("UNLUCKIEST", RED), ("...", INK)], 215, 84, A("u1", "unluckiest"), end=A("u1", "luckiest", nth=2) - 0.05,
       bold=True)
    hl(cr, t, [("...or ", INK), ("LUCKIEST", GREEN), ("?", INK)], 215, 84, A("u1", "luckiest", nth=2), bold=True)


def scene_train(cr, t, tl):
    A = tl.at
    fall = seg(t, A("u2", "flies"), A("u2", "river", end=True))
    keys = [(A("u2") - 0.2, (0.9, 360, 640)), (A("u2") + 0.6, (1.6, 160, 580)), (A("u2", "his"), (0.9, 330, 640)),
            (A("u2", "train"), (1.4, 360, 580)), (A("u2", "bridge"), (1.1, 400, 640)),
            (A("u2", "into"), (1.8, 460, 780)), (A("u2", "icy"), (1.1, 420, 700)), (A("u2", "swims"), (1.9, 330, 780)),
            (A("u2", "to"), (1.3, 260, 740)), (A("u2", "shore"), (2.0, 200, 780))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    river_scene(cr, t)
    x = lerp(160, 460, min(1, seg(t, A("u2"), A("u2", "flies")) + fall))
    train_car(cr, x, lerp(600, 820, ease_out(fall)), 1.0, rot=0.9 * fall, seed=11300)
    if fall >= 1:
        for k in range(5):   # the splash
            u = seg(t, A("u2", "river", end=True), A("u2", "river", end=True) + 0.5)
            blob(cr, 460 + (k - 2) * 50, 760 - math.sin(u * math.pi) * (60 + k * 10), 18, 26, WHITE, seed=11310 + k,
                 amp=0.8, lw=2.5)
        cue("thud", t, A("u2", "river", end=True) - 0.1)
    if t >= A("u2", "swims"):
        sw = seg(t, A("u2", "swims"), A("u2", "shore", end=True))
        swimmer(cr, lerp(420, 180, sw), 790, t, seed=11320)
    year(cr, t, A("u2"), "1962")
    counter(cr, t, 1 if t >= A("u2", "shore") else 0, A("u2", "shore"))
    hl(cr, t, [("off the ", INK), ("bridge", RED)], 215, 84, A("u2", "bridge"), end=A("u2", "swims") - 0.05, bold=True)
    hl(cr, t, [("he ", INK), ("SWIMS", GREEN), (" out", INK)], 215, 90, A("u2", "swims"), bold=True)


def scene_plane(cr, t, tl):
    A = tl.at
    out = A("u3", "sucked")
    land = A("u3", "haystack")
    keys = [(A("u3") - 0.2, (0.8, 360, 560)), (A("u3") + 0.6, (1.3, 360, 800)), (A("u3", "on"), (0.9, 300, 520)), (A("u3", "first"), (1.6, 300, 460)), (A("u3", "flight"), (1.1, 400, 500)),
            (A("u3", "door"), (2.0, 420, 440)),
            (out, (1.0, 360, 600)), (A("u3", "lands"), (1.3, 360, 820)), (land, (1.8, 360, 860))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#ffd9a0"))
    cr.paint()
    for k in range(5):
        blob(cr, (k * 230 + t * 30) % 1200 - 200, 300 + (k % 3) * 120, 90, 34, WHITE, seed=11400 + k, amp=1.5, lw=0,
             stroke=None)
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#c9b26a"), seed=11401, amp=1, lw=4)
    # plane crossing the sky
    px = lerp(-100, 900, seg(t, A("u3") - 0.2, A("u3", end=True)))
    with at(cr, px, 420, 1.0, rot=-0.05):
        shape(cr, [(-220, 0), (-180, -40), (200, -40), (240, 0), (200, 30), (-180, 30)], WHITE, seed=11410, amp=0.8, lw=4)
        sharp_shape(cr, [(-40, -10), (60, -10), (10, 90)], hexc("#c7c2cc"), seed=11411, amp=0.5, lw=3.5)
        sharp_shape(cr, [(-200, -30), (-170, -110), (-140, -30)], RED, seed=11412, amp=0.5, lw=3.5)
        for k in range(6):
            blob(cr, -120 + k * 50, -12, 9, 9, hexc("#bfe6ef"), seed=11413 + k, amp=0.2, lw=2.5)
        door_open = t >= A("u3", "door")
        shape(cr, rrect_pts(60 if not door_open else 40, -34, 30, 56, 4, 10), INK if door_open else hexc("#e8e0d0"),
              seed=11420, amp=0.3, lw=3)
    # the fall
    if t >= out:
        u = seg(t, out, land + 0.1)
        fx, fy = lerp(420, 360, u), lerp(460, 860, smooth(u))
        if u < 1:
            with at(cr, fx, fy, 0.8, rot=u * 8):
                person(cr, MAN, 0, 0, t, facing=1, arms=("cheer", "cheer"), eyes="wide", mouth="o")
        cue("whoosh", t, out, 0.4)
    hay = t >= land
    shape(cr, [(200, 900), (240, 780), (360, 730), (480, 780), (520, 900)], HAY, seed=11430, amp=2.5, lw=4)
    for k in range(8):
        line(cr, [(230 + k * 36, 890), (250 + k * 34, 790)], 2.5, hexc("#c9a64a"), seed=11431 + k, amp=0.8)
    if hay:
        person(cr, MAN, 360, 830, t, facing=1, arms=("thumb", "hip"), eyes="happy", mouth="grin", scale=0.8)
        shape(cr, [(260, 900), (300, 820), (420, 820), (460, 900)], HAY, seed=11440, amp=2.0, lw=3.5)
        cue("thud", t, land)
    year(cr, t, A("u3"), "1963")
    counter(cr, t, 2 if hay else 1, land)
    hl(cr, t, [("door ", INK), ("BLOWS OPEN", RED)], 215, 70, A("u3", "door"), end=A("u3", "lands") - 0.05, bold=True)
    hl(cr, t, [("...a ", INK), ("HAYSTACK", GOLD)], 215, 84, land, bold=True)


def scene_bus(cr, t, tl):
    A = tl.at
    skid = seg(t, A("u4", "skids"), A("u4", "river", end=True))
    keys = [(A("u4") - 0.2, (1.0, 360, 640)), (A("u4") + 0.6, (1.6, 120, 640)), (A("u4", "bus"), (1.2, 320, 600)), (A("u4", "river"), (1.2, 420, 740)),
            (A("u4", "swims"), (1.8, 300, 780)), (A("u4", "again"), (2.2, 260, 760))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    river_scene(cr, t, bridge=False)
    sharp_shape(cr, [(-900, 700), (220, 700), (260, 1900), (-900, 1900)], hexc("#6b6f78"), seed=11500, amp=0.8, lw=4)
    bus(cr, lerp(0, 400, skid), lerp(700, 830, ease_out(max(0, skid - 0.5) * 2)), 0.9, rot=0.35 * skid, seed=11510)
    if t >= A("u4", "swims"):
        swimmer(cr, lerp(460, 260, seg(t, A("u4", "swims"), A("u4", "again", end=True))), 790, t, seed=11520)
    year(cr, t, A("u4"), "1966")
    counter(cr, t, 3 if t >= A("u4", "swims") else 2, A("u4", "swims"))
    hl(cr, t, [("bus into a ", INK), ("RIVER", RIVER)], 215, 80, A("u4", "river"), end=A("u4", "again") - 0.05, bold=True)
    hl(cr, t, [("AGAIN", RED)], 215, 110, A("u4", "again"), bold=True)


def scene_car(cr, t, tl):
    A = tl.at
    keys = [(A("u5") - 0.2, (1.4, 250, 740)), (A("u5", "public"), (1.9, 250, 700)), (A("u5", "buys"), (1.1, 400, 760)),
            (A("u5", "fire"), (1.6, 480, 760)), (A("u5", "twice"), (1.1, 420, 740))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#fbe2c4"))
    cr.paint()
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#6b6f78"), seed=11600, amp=1, lw=4)
    for k in range(-8, 18):
        line(cr, [(k * 120, 1000), (k * 120 + 60, 1000)], 6, hexc("#f7d774"), seed=11601 + k, amp=0.3)
    if t < A("u5", "buys"):
        bus(cr, 520, 900, 0.8, seed=11610)
        with at(cr, 520, 760, 1.0, rot=0.2):
            line(cr, [(-150, -90), (150, 90)], 14, RED, seed=11611, amp=0.5)
            line(cr, [(150, -90), (-150, 90)], 14, RED, seed=11612, amp=0.5)
        person(cr, MAN, 200, 905, t, facing=1, arms=("point", "hip"), eyes="sly", mouth="flat")
    else:
        burning = t >= A("u5", "fire")
        car(cr, 470, 900, t, 0.9, color=hexc("#3f6fb5"), seed=11620)
        if burning:
            flames(cr, 470, 820, t, 1.2, seed=11630)
            n = 2 if t >= A("u5", "twice") else 1
            person(cr, MAN, 170, 905, t, facing=1, arms=("face", "hip"), eyes="wide", mouth="o", sweat=True,
                   jump=abs(math.sin(t * 10)) * 10)
            write(cr, [(f"FIRE #{n}", RED)], 470, 640, 60, align="center", bold=True, halo=WHITE)
            cue("hit", t, A("u5", "fire"))
            cue("hit", t, A("u5", "twice"))
        else:
            person(cr, MAN, 170, 905, t, facing=1, arms=("thumb", "hip"), eyes="happy", mouth="grin")
    counter(cr, t, 5 if t >= A("u5", "twice") else (4 if t >= A("u5", "fire") else 3),
            A("u5", "twice") if t >= A("u5", "twice") else A("u5", "fire"))
    hl(cr, t, [("no more ", INK), ("public transport", RED)], 215, 62, A("u5", "public"), end=A("u5", "buys") - 0.05,
       bold=True)
    hl(cr, t, [("his car? ", INK), ("ON FIRE", RED)], 215, 80, A("u5", "fire"), bold=True)


def scene_street(cr, t, tl):
    A = tl.at
    hit = A("u6", "hits")
    keys = [(A("u6") - 0.2, (1.1, 360, 720)), (A("u6", "bus"), (1.5, 460, 720)), (hit, (1.9, 280, 760)),
            (A("u6", "bruises"), (1.4, 260, 760))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#d9e8f2"))
    cr.paint()
    for k in range(-5, 12):
        h = 220 + (k * 71) % 160
        sharp_shape(cr, [(k * 130, 900 - h), (k * 130 + 120, 900 - h), (k * 130 + 120, 900), (k * 130, 900)],
                    hexc("#a9b8c8"), seed=11700 + k, amp=0.6, lw=3)
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#6b6f78"), seed=11701, amp=1, lw=4)
    write(cr, [("ZAGREB", INK)], 470, 640, 56, align="center", bold=True, halo=WHITE)
    bx = lerp(900, 420, ease_out(seg(t, A("u6"), hit)))
    bus(cr, bx, 900, 0.9, seed=11710, facing=-1)
    knocked = t >= hit
    with at(cr, 250 if not knocked else 200, 905, 1.0, rot=-0.35 * min(1, (t - hit) * 4) if knocked else 0):
        person(cr, MAN, 0, 0, t, facing=1, eyes="wide" if not knocked else "closed", mouth="o",
               arms=("face", "hip") if not knocked else ("cheer", "down"))
    if knocked:
        for k in range(3):   # cartoon stars
            a = t * 5 + k * 2.1
            write(cr, [("*", GOLD)], 180 + 50 * math.cos(a), 700 + 20 * math.sin(a), 50, bold=True)
        cue("hit", t, hit)
    year(cr, t, A("u6"), "1995")
    counter(cr, t, 6 if knocked else 5, hit)
    hl(cr, t, [("hit by a ", INK), ("BUS", RED)], 215, 90, hit, end=A("u6", "bruises") - 0.05, bold=True)
    hl(cr, t, [("just ", INK), ("bruises", GREEN)], 215, 90, A("u6", "bruises"), bold=True)


def scene_cliff(cr, t, tl):
    A = tl.at
    off = A("u7", "off")
    thrown = A("u7", "thrown")
    drop = A("u7", "drops")
    keys = [(A("u7") - 0.2, (1.0, 360, 600)), (A("u7", "car"), (1.4, 300, 520)), (off, (1.1, 380, 600)),
            (thrown, (1.7, 300, 560)), (A("u7", "grabs"), (1.2, 400, 700)), (A("u7", "tree"), (2.0, 420, 640)), (drop, (0.7, 440, 800)),
            (A("u7", "150"), (0.6, 460, 900))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*SKY)
    cr.paint()
    for k in range(-3, 8):
        sharp_shape(cr, [(k * 220 - 120, 1400), (k * 220, 700 - (k % 3) * 120), (k * 220 + 120, 1400)],
                    hexc("#8aa0b8"), seed=11800 + k, amp=0.8, lw=3)
    # cliff + road
    sharp_shape(cr, [(-900, 560), (380, 560), (330, 700), (360, 900), (300, 1400), (-900, 1400)], hexc("#8e7a5a"),
                seed=11801, amp=1.4, lw=4.5)
    sharp_shape(cr, [(-900, 540), (380, 540), (380, 560), (-900, 560)], hexc("#555a66"), seed=11802, amp=0.4, lw=3)
    # the tree on the cliff face
    line(cr, [(340, 640), (420, 600)], 10, hexc("#6b4a2e"), seed=11810, amp=0.4)
    blob(cr, 440, 580, 60, 40, GREEN, seed=11811, amp=1.2, lw=4)
    u = seg(t, off, off + 0.4)
    if t < thrown:
        car(cr, lerp(100, 360, u), 540 + (u ** 2) * 40, t, 0.6, color=hexc("#c0504d"), seed=11820)
        person(cr, MAN, lerp(100, 360, u), 480, t, facing=1, scale=0.45, eyes="wide", mouth="o")
    else:
        # the car falls away; he hangs on the branch
        fall = seg(t, drop, drop + 1.2)
        with at(cr, lerp(380, 640, fall), lerp(545, 1500, fall ** 1.6), 0.6, rot=fall * 5):
            car(cr, 0, 0, t, 1.0, color=hexc("#c0504d"), seed=11820)
        with at(cr, 400, 790, 0.7):
            person(cr, MAN, 0, 0, t, facing=-1, arms=("cheer", "cheer"), eyes="wide", mouth="o", sweat=True)
        cue("whoosh", t, drop, 0.5)
    year(cr, t, A("u7"), "1996")
    counter(cr, t, 7 if t >= A("u7", "tree") else 6, A("u7", "tree"))
    hl(cr, t, [("off a ", INK), ("mountain road", RED)], 215, 70, off, end=A("u7", "tree") - 0.05, bold=True)
    hl(cr, t, [("grabs a ", INK), ("TREE", GREEN)], 215, 90, A("u7", "tree"), end=A("u7", "150") - 0.05, bold=True)
    hl(cr, t, [("150 m", RED), (" drop", INK)], 215, 90, A("u7", "150"), bold=True)


def scene_lottery(cr, t, tl):
    A = tl.at
    win = A("u8", "wins")
    keys = [(A("u8") - 0.2, (1.4, 300, 740)), (A("u8", "lottery"), (2.0, 320, 700)), (win, (1.0, 360, 700)),
            (A("u8", "million"), (1.3, 360, 620))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*(hexc("#c9f0c4") if t >= win else hexc("#fbf3e1")))
    cr.paint()
    if t >= win:
        for k in range(20):
            a = k * math.pi / 10 + t * 0.5
            cr.move_to(360, 620)
            cr.arc(360, 620, 1400, a, a + math.pi / 20)
            cr.close_path()
            cr.set_source_rgba(*hexc("#f7d774", 0.5))
            cr.fill()
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#b98a5a"), seed=11900, amp=1, lw=4)
    won = t >= win
    person(cr, MAN, 330, 905, t, facing=1, arms=("cheer", "cheer") if won else ("hold", "hip"), eyes="happy" if won else "dot",
           mouth="grin" if won else "smile", item=None if won else "ticket", jump=abs(math.sin(t * 9)) * 16 if won else 0)
    if won:
        with at(cr, 360, 560, pop(t, win, 0.25) or 0.01, rot=-0.06):
            shape(cr, rrect_pts(-230, -90, 460, 180, 20, 20), GOLD, seed=11910, amp=0.8, lw=5)
            write(cr, [("JACKPOT!", RED)], 0, 30, 96, align="center", bold=True)
        confetti(cr, t, win)
        cue("kaching", t, win)
    hl(cr, t, [("a ", INK), ("lottery ticket", GOLD)], 215, 80, A("u8", "lottery"), end=win - 0.05, bold=True)
    hl(cr, t, [("~$1,000,000", GREEN)], 215, 90, A("u8", "million"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("u9") - 0.2, (1.0, 360, 700)), (A("u9", "strange"), (1.8, 160, 720)), (A("u9", "none"), (1.5, 360, 600)),
            (A("u9", "accidents"), (1.1, 360, 680)), (A("u9", "officially"), (1.9, 330, 620)),
            (A("u9", "confirmed"), (1.1, 360, 660)),
            (A("u9", "so"), (0.9, 360, 700)), (A("u9", "unluckiest"), (1.6, 240, 700)), (A("u9", "alive"), (1.1, 300, 720)),
            (A("u9", "best"), (1.9, 360, 600)), (A("u9", "storyteller"), (1.6, 480, 700))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#e9d3ae"))
    cr.paint()
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#b98a5a"), seed=12000, amp=1, lw=4)
    # an empty archive folder
    with at(cr, 360, 600, 1.0, rot=-0.04):
        shape(cr, rrect_pts(-190, -130, 380, 260, 10, 18), hexc("#e8c46a"), seed=12010, amp=0.8, lw=4)
        write(cr, [("OFFICIAL RECORDS", INK)], 0, -70, 36, align="center", bold=True)
        if t >= A("u9", "none"):
            write(cr, [("0", RED)], -40, 70, 120, align="center", bold=True)
            write(cr, [("found", INK)], 80, 50, 40, align="center", bold=True)
    person(cr, MAN, 150, 905, t, facing=1, arms=("chin", "hip") if t < A("u9", "storyteller") else ("wave", "hip"),
           eyes="sly", mouth="smirk")
    counter(cr, t, 7, -10)
    hl(cr, t, [("never ", INK), ("confirmed", RED)], 215, 84, A("u9", "confirmed"), end=A("u9", "unluckiest") - 0.05,
       bold=True)
    hl(cr, t, [("unlucky", RED), (" or ", INK), ("storyteller", GOLD), ("?", INK)], 215, 70, A("u9", "unluckiest"),
       bold=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"intro": scene_intro, "train": scene_train, "plane": scene_plane, "bus": scene_bus, "car": scene_car,
     "street": scene_street, "cliff": scene_cliff, "lottery": scene_lottery, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
