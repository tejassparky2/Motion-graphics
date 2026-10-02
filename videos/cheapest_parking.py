"""Episode 11: "The Cheapest Parking in New York" — a clever-twist story, retold in our own words.

A rich man borrows $5,000 from a bank and puts up his $300,000 sports car as collateral. Two weeks later he repays
$5,000 plus $23 interest. Why? Two weeks of guarded parking in New York... for $23.

Math (checked): $5,000 at 12% a year for 14 days = 5000 x 0.12 x 14 / 365 = $23.01. The story is a well-known
banking joke (folklore), told here with our own characters, dialogue and numbers.
"""
import math

from motion.captions import captions
from motion.characters import bubble, cash, money_pile, person
from motion.critters import car
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, confetti, enter_world, fly, hl, set_camera, stamp, whip

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="k1", scene="street",
         text="A man in a fancy suit walks into a New York bank, and asks to borrow [five thousand dollars.|$5,000.]"),
    dict(id="k2", scene="bank", text="The banker says: sure, but we need something as collateral.", speaker="teacher",
         speaker_from="sure"),
    dict(id="k3", scene="bank",
         text="So the man hands over the keys to his [three hundred thousand dollar|$300,000] sports car."),
    dict(id="k4", scene="bank",
         text="The bankers can't stop laughing. A supercar, for five grand? They park it in the bank's secure garage."),
    dict(id="k5", scene="garage",
         text="Two weeks later, he comes back, and pays the five thousand, plus [twenty-three dollars|$23] in interest."),
    dict(id="k6", scene="bank2", text="Then the banker looks him up, and he's a multi-millionaire."),
    dict(id="k7", scene="bank2", text="Sir, why would you need to borrow five thousand dollars?", speaker="teacher"),
    dict(id="k8", scene="bank2",
         text="The man smiles. Where else in New York can I park for two weeks? For only "
              "[twenty-three dollars.|$23.]",
         speaker="host", speaker_from="where", gap=0.22),
    dict(id="k9", scene="end", text="Genius, or cheapskate?", pace=0.95, gap=0.25),
]

METADATA = dict(
    title="The Cheapest Parking Spot in New York 😂🚗",
    alt_titles=["Why a Millionaire Borrowed $5,000 From a Bank 🤔", "He Used a Bank as a $23 Parking Garage 😂"],
    description="""A man in a fancy suit walks into a New York bank and borrows $5,000, using his $300,000 sports car as collateral. The bankers laugh… until two weeks later he pays it back with $23 of interest. 😂🚗

Why would a multi-millionaire need $5,000? He didn't. He needed parking. 😏

(The math: $5,000 at 12% a year for 14 days ≈ $23.)

💬 Genius or cheapskate? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#PlotTwist", "#Storytime", "#Funny"],
    tags=["plot twist", "funny story", "clever trick", "rich man trick", "new york parking", "bank loan story",
          "twist ending", "storytime", "animated story", "interestingly strange"],
    pinned_comment="Genius or cheapskate? 😂 Be honest 👇",
)

GOLD = hexc("#f2b632")
GREEN = hexc("#3d8f45")
MARBLE = hexc("#efe8dc")
NAVY = hexc("#23346b")
CAR = hexc("#e0483f")
RICH, BANKER = "host", "teacher"
RX, BX = 250, 540          # rich man and banker positions inside the bank


def skyline(cr, t):
    cr.set_source_rgba(*hexc("#9fd6f2"))
    cr.paint()
    for k in range(-6, 16):   # skyscrapers
        h = 260 + ((k * 137) % 5) * 90
        x = k * 110
        col = [hexc("#8fa3c0"), hexc("#7b8fb0"), hexc("#a3b4cc")][k % 3]
        sharp_shape(cr, [(x, 900 - h), (x + 100, 900 - h), (x + 100, 900), (x, 900)], col, seed=8000 + k, amp=0.6, lw=3)
        for r in range(int(h / 60)):
            for c in range(3):
                if (k + r + c) % 4:
                    dot(cr, x + 22 + c * 28, 900 - h + 30 + r * 60, 6, hexc("#fff3c4"))
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#6b6f78"), seed=8001, amp=1, lw=4)
    for k in range(-8, 20):
        line(cr, [(k * 120, 1000), (k * 120 + 60, 1000)], 6, hexc("#f7d774"), seed=8002 + k, amp=0.3)
    # the bank's front
    shape(cr, rrect_pts(380, 470, 420, 430, 6, 20), MARBLE, seed=8050, amp=0.8, lw=4.5)
    sharp_shape(cr, [(360, 480), (590, 370), (820, 480)], MARBLE, seed=8051, amp=0.6, lw=4.5)
    write(cr, [("BANK", NAVY)], 590, 460, 50, align="center", bold=True)
    for k in range(4):
        shape(cr, rrect_pts(410 + k * 100, 500, 34, 400, 8, 16), WHITE, seed=8052 + k, amp=0.5, lw=3)
    shape(cr, rrect_pts(540, 740, 100, 160, 8, 14), hexc("#8e5a2e"), seed=8060, amp=0.5, lw=4)


def bank_inside(cr, t):
    cr.set_source_rgba(*hexc("#e6dcc8"))
    cr.paint()
    for k in range(-3, 6):   # marble columns
        x = k * 240
        shape(cr, rrect_pts(x, 330, 60, 570, 10, 18), MARBLE, seed=8100 + k, amp=0.6, lw=3.5)
        line(cr, [(x + 20, 360), (x + 34, 520), (x + 24, 700)], 2, hexc("#cfc5b3"), seed=8110 + k, amp=0.8)
    sharp_shape(cr, [(-900, 900), (1600, 890), (1600, 1900), (-900, 1900)], hexc("#b0624a"), seed=8101, amp=1, lw=4)
    for k in range(-8, 16):   # checker floor
        sharp_shape(cr, [(k * 100, 900), (k * 100 + 50, 900), (k * 100 + 20, 1000), (k * 100 - 30, 1000)],
                    hexc("#9a5540"), seed=8120 + k, amp=0.3, lw=0, stroke=None)
    # vault door
    blob(cr, 860, 620, 150, 150, hexc("#a9a2ae"), seed=8130, amp=0.6, lw=5)
    blob(cr, 860, 620, 110, 110, hexc("#c7c2cc"), seed=8131, amp=0.5, lw=3.5)
    for k in range(6):
        a = k * math.pi / 3 + t * 0.2
        line(cr, [(860, 620), (860 + 80 * math.cos(a), 620 + 80 * math.sin(a))], 6, INK, seed=8132 + k, amp=0.2)
    shape(cr, rrect_pts(250, 380, 300, 80, 10, 18), NAVY, seed=8140, amp=0.6, lw=4)
    write(cr, [("FIRST BANK", GOLD)], 400, 434, 44, align="center", bold=True)


def counter(cr):
    shape(cr, rrect_pts(400, 836, 380, 70, 8, 18), hexc("#6d4524"), seed=8150, amp=0.8, lw=4.5)
    line(cr, [(400, 858), (780, 858)], 4, GOLD, seed=8151, amp=0.5)


def keys_prop(cr, x, y, s=1.0, rot=0.0):
    with at(cr, x, y, s, rot=rot):
        blob(cr, 0, 0, 18, 18, None, seed=8200, amp=0.3, lw=5, stroke=hexc("#a9a2ae"))
        shape(cr, rrect_pts(10, -14, 60, 28, 10, 12), CAR, seed=8201, amp=0.3, lw=3)
        write(cr, [("SC", WHITE)], 40, 8, 20, align="center", bold=True)
        sharp_shape(cr, [(-12, 14), (-4, 14), (-4, 60), (-12, 60)], hexc("#c7c2cc"), seed=8202, amp=0.2, lw=2.5)


def scene_street(cr, t, tl):
    A = tl.at
    keys = [(0, (1.1, 360, 760)), (A("k1", "fancy"), (1.9, 170, 700)), (A("k1", "walks"), (1.0, 400, 700)),
            (A("k1", "New"), (0.8, 470, 560)), (A("k1", "asks"), (1.5, 450, 740)), (A("k1", "$5,000"), (1.9, 330, 700))]
    set_camera(camera(t, keys, dur=0.16))
    enter_world(cr)
    skyline(cr, t)
    walk = seg(t, A("k1", "walks"), A("k1", "bank", end=True) + 0.2)
    person(cr, RICH, lerp(160, 520, walk), 905, t, facing=1, walk=t * 2.2 if 0 < walk < 1 else None,
           arms=("hip", "hip") if walk < 1 else ("give", "hip"), eyes="sly", mouth="smirk")
    if t >= A("k1", "$5,000"):
        bubble(cr, 360, 560, 260, 110, (500, 700), [("$5,000?", GREEN)], s=pop(t, A("k1", "$5,000"), 0.2), size=56)
    hl(cr, t, [("a ", INK), ("FANCY", GOLD), (" suit", INK)], 215, 84, A("k1", "fancy"), end=A("k1", "New") - 0.05, bold=True)
    hl(cr, t, [("New York", NAVY), (" bank", INK)], 215, 84, A("k1", "New"), end=A("k1", "$5,000") - 0.05, bold=True)
    hl(cr, t, [("borrow ", INK), ("$5,000", GREEN)], 215, 84, A("k1", "$5,000"), bold=True)


def scene_bank(cr, t, tl, part):
    A = tl.at
    if part == 1:
        keys = [(A("k2") - 0.2, (1.1, 380, 740)), (A("k2", "sure"), (1.9, BX, 700)), (A("k2", "collateral"), (1.5, 420, 720)),
                (A("k3", "keys"), (2.0, 300, 700)), (A("k3", "$300,000"), (1.0, 380, 700)),
                (A("k3", "sports"), (1.4, 330, 640)), (A("k4", "laughing"), (1.0, 400, 740)),
                (A("k4", "supercar"), (1.8, BX, 700)), (A("k4", "park"), (1.2, 400, 740))]
    else:
        keys = [(A("k6") - 0.2, (1.2, 420, 740)), (A("k6", "looks"), (1.9, 640, 650)), (A("k6", "multi"), (1.3, 640, 640)),
                (A("k7", "why"), (1.9, BX, 700)), (A("k7", "borrow"), (1.3, 420, 740)), (A("k8", "smiles"), (2.0, RX, 690)),
                (A("k8", "where"), (1.5, 300, 720)), (A("k8", "park"), (1.2, 400, 740)), (A("k8", "$23."), (1.9, RX, 700))]
    set_camera(camera(t, keys, dur=0.16))
    enter_world(cr)
    bank_inside(cr, t)
    lol = part == 1 and A("k4") <= t < A("k4", "park")
    # banker behind the counter (+ a teller who laughs along)
    bs = dict(facing=-1, arms=("hip", "hip"), eyes="dot", mouth="smile")
    if part == 1 and t >= A("k3", "$300,000"):
        bs.update(eyes="wide", mouth="o")
    if lol:
        bs.update(eyes="closed", mouth="laugh", jump=abs(math.sin(t * 9)) * 8)
    if part == 2:
        bs.update(eyes="wide" if t < A("k7") else "dot", mouth="o", sweat=A("k6", "multi") <= t < A("k8"),
                  arms=("chin", "hip") if A("k7") <= t < A("k8") else ("hip", "hip"))
        if t >= A("k8", "$23."):
            bs.update(eyes="wide", mouth="o", shake=1.5)
    if tl.speaking("teacher", t):
        bs["mouth"] = "o" if int(t * 12) % 2 else "smile"
    person(cr, "mia", 680, 900, t, facing=-1, eyes="closed" if lol else "dot", mouth="laugh" if lol else "smile",
           jump=abs(math.sin(t * 9 + 1)) * 8 if lol else 0)
    person(cr, BANKER, BX, 900, t, **bs)
    counter(cr)
    # rich man in front
    rs = dict(facing=1, arms=("hip", "hip"), eyes="sly", mouth="smirk")
    if part == 1 and A("k3", "hands") <= t < A("k4"):
        rs.update(arms=("give", "hip"))
    if part == 2 and t >= A("k8", "smiles"):
        rs.update(eyes="happy", mouth="grin")
    if tl.speaking("host", t):
        rs["mouth"] = "o" if int(t * 12) % 2 else "smirk"
    person(cr, RICH, RX, 905, t, **rs)
    if part == 1:
        if A("k3", "hands") <= t < A("k4", "park"):
            keys_prop(cr, lerp(320, 450, seg(t, A("k3", "hands"), A("k3", "keys", end=True))), 822, 1.1,
                      rot=math.sin(t * 6) * 0.2)
        # the car shows up in a thought cloud
        if A("k3", "sports") <= t < A("k4", "laughing"):
            cr.save()
            with at(cr, 360, 560, pop(t, A("k3", "sports"), 0.25) or 0.01):
                blob(cr, 0, 0, 260, 140, WHITE, seed=8300, amp=2.0, lw=4)
                car(cr, 0, 70, t, 0.6, color=CAR, seed=8301)
            cr.restore()
        if lol and int(t * 3) % 2:
            write(cr, [("HA HA HA", RED)], 620, 640, 48, align="center", bold=True, halo=WHITE)
        hl(cr, t, [("collateral", GOLD), ("?", INK)], 215, 84, A("k2", "collateral"), end=A("k3") - 0.05, bold=True)
        hl(cr, t, [("$300,000", GREEN), (" sports car", INK)], 215, 70, A("k3", "$300,000"), end=A("k4") - 0.05, bold=True)
        hl(cr, t, [("a supercar... for ", INK), ("$5K", GREEN), ("?", INK)], 215, 66, A("k4", "supercar"),
           end=A("k4", "park") - 0.05, bold=True)
        hl(cr, t, [("into the ", INK), ("secure garage", NAVY)], 215, 66, A("k4", "park"), bold=True)
    else:
        # the banker's screen
        if A("k6", "looks") <= t < A("k7"):
            with at(cr, 640, 640, pop(t, A("k6", "looks"), 0.2) or 0.01):
                shape(cr, rrect_pts(-150, -100, 300, 190, 10, 16), INK, seed=8400, amp=0.5, lw=4)
                shape(cr, rrect_pts(-136, -86, 272, 162, 6, 16), hexc("#dff5e3"), seed=8401, amp=0.4, lw=0, stroke=None)
                write(cr, [("BALANCE", INK)], 0, -40, 28, align="center", bold=True)
                if t >= A("k6", "multi"):
                    write(cr, [("$$$$$$$$", GREEN)], 0, 30, 56, align="center", bold=True)
            if t >= A("k6", "multi"):
                cue("kaching", t, A("k6", "multi"))
        hl(cr, t, [("MULTI-MILLIONAIRE", GREEN)], 215, 70, A("k6", "multi"), end=A("k7") - 0.05, bold=True)
        hl(cr, t, [("\"why borrow ", INK), ("$5,000", GREEN), ("?\"", INK)], 215, 66, A("k7", "why"), end=A("k8") - 0.05,
           bold=True)
        hl(cr, t, [("parking", NAVY), (" for 2 weeks = ", INK), ("$23", RED)], 215, 60, A("k8", "park"), bold=True,
           underline=True)
        if t >= A("k8", "$23."):
            stamp(cr, t, A("k8", "$23."), "GENIUS", dur=0.8, y=470)


def scene_garage(cr, t, tl):
    A = tl.at
    keys = [(A("k5") - 0.2, (1.0, 360, 720)), (A("k5", "weeks"), (1.3, 560, 520)), (A("k5", "comes"), (1.6, 380, 760)),
            (A("k5", "pays"), (1.2, 360, 700)), (A("k5", "five"), (1.8, 200, 700)), (A("k5", "$23"), (1.9, 520, 700))]
    set_camera(camera(t, keys, dur=0.16))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#5c6270"))
    cr.paint()
    for k in range(-4, 10):   # concrete pillars
        shape(cr, rrect_pts(k * 260, 300, 60, 600, 4, 18), hexc("#7b808c"), seed=8500 + k, amp=0.6, lw=3.5)
        write(cr, [("B" + str(k % 3 + 1), GOLD)], k * 260 + 30, 400, 34, align="center", bold=True)
    sharp_shape(cr, [(-900, 900), (1600, 890), (1600, 1900), (-900, 1900)], hexc("#4a4f5c"), seed=8501, amp=1, lw=4)
    for k in range(-6, 14):
        line(cr, [(k * 140, 900), (k * 140 - 60, 1100)], 5, hexc("#f7d774"), seed=8502 + k, amp=0.3)
    # spotlight on the car, plus a security camera
    cr.move_to(360, 260)
    cr.line_to(120, 900)
    cr.line_to(620, 900)
    cr.close_path()
    cr.set_source_rgba(1, 0.97, 0.8, 0.22)
    cr.fill()
    car(cr, 370, 900, t, 1.0, color=CAR, seed=8510)
    with at(cr, 640, 330, 1.0, rot=0.3 * math.sin(t * 1.5)):
        shape(cr, rrect_pts(-40, -20, 80, 40, 8, 12), WHITE, seed=8520, amp=0.4, lw=3.5)
        dot(cr, -44, 0, 8, RED if int(t * 2) % 2 else hexc("#7a1f1f"))
    shape(cr, rrect_pts(40, 330, 250, 70, 8, 16), hexc("#2b2d3a"), seed=8530, amp=0.5, lw=3.5)
    write(cr, [("24/7 SECURITY", GOLD)], 165, 378, 32, align="center", bold=True)
    # calendar flipping 14 days
    day = 1 + int(13 * seg(t, A("k5"), A("k5", "later", end=True)))
    shape(cr, rrect_pts(470, 420, 180, 150, 8, 16), WHITE, seed=8540, amp=0.6, lw=4)
    shape(cr, rrect_pts(470, 420, 180, 40, 8, 16), RED, seed=8541, amp=0.5, lw=3)
    write(cr, [("DAY", INK)], 560, 494, 28, align="center", bold=True)
    write(cr, [(str(day), RED)], 560, 552, 56, align="center", bold=True)
    if t >= A("k5", "comes"):
        person(cr, RICH, 150, 905, t, facing=1, arms=("give", "hip") if t >= A("k5", "pays") else ("hip", "hip"),
               eyes="happy", mouth="grin")
    if t >= A("k5", "five"):
        money_pile(cr, 250, 900, 0.5, seed=8550)
    if t >= A("k5", "$23"):
        with at(cr, 520, 700, pop(t, A("k5", "$23"), 0.25) or 0.01, rot=-0.08):
            shape(cr, rrect_pts(-130, -60, 260, 120, 10, 16), WHITE, seed=8560, amp=0.6, lw=4)
            write(cr, [("interest:", INK)], 0, -14, 30, align="center")
            write(cr, [("$23", RED)], 0, 44, 60, align="center", bold=True)
    hl(cr, t, [("2 weeks ", INK), ("later", RED)], 215, 84, A("k5", "weeks"), end=A("k5", "pays") - 0.05, bold=True)
    hl(cr, t, [("$5,000", GREEN), (" + ", INK), ("$23", RED)], 215, 90, A("k5", "pays"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("k9") - 0.2, (1.0, 360, 720)), (A("k9", "genius"), (1.3, 250, 700)), (A("k9", "cheapskate"), (1.3, 470, 700))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#fbf3e1"))
    cr.paint()
    cr.save()
    cr.rectangle(-600, -600, 960, 2600)
    cr.clip()
    cr.set_source_rgba(*hexc("#c9f0c4"))
    cr.paint()
    cr.restore()
    cr.set_source_rgba(*hexc("#ffd0d0"))
    cr.rectangle(360, -600, 1200, 2600)
    cr.fill()
    person(cr, RICH, 360, 905, t, facing=1, arms=("thumb", "hip"), eyes="sly", mouth="smirk", scale=1.2)
    car(cr, 360, 1080, t, 0.5, color=CAR, seed=8600)
    write(cr, [("GENIUS", GREEN)], 180, 520, 64, align="center", bold=True, halo=WHITE)
    write(cr, [("CHEAPSKATE", RED)], 540, 520, 56, align="center", bold=True, halo=WHITE)
    hl(cr, t, [("genius", GREEN), (" or ", INK), ("cheapskate", RED), ("?", INK)], 215, 70, A("k9"), bold=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "street":
        scene_street(cr, t, tl)
    elif name == "bank":
        scene_bank(cr, t, tl, 1)
    elif name == "garage":
        scene_garage(cr, t, tl)
    elif name == "bank2":
        scene_bank(cr, t, tl, 2)
    else:
        scene_end(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
