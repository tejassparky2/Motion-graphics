"""Clever words from history: Archimedes, "Give me a place to stand, and I will move the Earth."

The saying is quoted by Pappus of Alexandria (Collection, book 8) and later writers. Plutarch (Life of Marcellus 14)
tells the story behind it: Archimedes wrote to King Hiero of Syracuse that with a given force any given weight could
be moved, and that if there were another world and he could go to it, he could move this one. Hiero asked him to
show it, so Archimedes took a three-masted merchant ship of the royal fleet, which had been hauled ashore with great
labour by many men, put many people and the usual cargo on board, sat some way off and, without great effort,
pulling with his hand a set of compound pulleys, drew it toward him smoothly, as if it were gliding through the
water. The seesaw is the law of the lever (weight x distance balances): 60 kg at 1 unit balances 30 kg at 2 units.
"""
import math

from motion.captions import captions
from motion.characters import CAST, person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import hl, stamp, whip
from motion.story import BLUE, CLOSE, GREEN, bg, buttons, card, head_c, tag, talk

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="a1", scene="hook", text="Over two thousand years ago, one man said he could move the whole Earth. By "
                                     "himself."),
    dict(id="a2", scene="intro", text="His name was Archimedes. He lived in Syracuse, on the island of Sicily."),
    dict(id="a3", scene="quote", text="He said: Give me a place to stand, and I will move the Earth.",
         speaker="archimedes", speaker_from="give"),
    dict(id="a4", scene="crazy", text="Was he crazy? No. He knew the secret of the lever."),
    dict(id="a5", scene="seesaw", text="Look at a seesaw. A dad weighs [sixty kilos.|60 kg.] His son weighs "
                                       "[thirty.|30 kg.]"),
    dict(id="a6", scene="seesaw", text="If they sit at the same distance from the middle, the dad goes down. The son "
                                       "goes up."),
    dict(id="a7", scene="seesaw", text="But if the son sits twice as far from the middle, they balance."),
    dict(id="a8", scene="seesaw", text="Half the weight, twice the distance. So with a long enough lever, a small "
                                       "push can lift something huge."),
    dict(id="a9", scene="ship", text="The king asked him to prove it. So Archimedes chose a big ship, pulled up on "
                                     "land, full of people and cargo."),
    dict(id="a10", scene="ship", text="He sat far away, and pulled a rope through a set of pulleys. And the ship slid "
                                      "toward him. Alone."),
    dict(id="a11", scene="end", text="So what do you think? With a place to stand, could he really move the Earth?",
         pace=0.95),
]

METADATA = dict(
    title="He Said He Could Move the EARTH… and Then Proved It With a Ship 🌍",
    alt_titles=["\"Give Me a Place to Stand and I Will Move the Earth\" 🌍", "How One Man Pulled a Full Ship Alone ⚓"],
    description="""Over 2,000 years ago, one man said he could move the whole Earth. By himself. 🌍

Archimedes of Syracuse said: "Give me a place to stand, and I will move the Earth." Was he crazy? No. He knew the secret of the lever.

Look at a seesaw: a dad weighs 60 kg and his son 30 kg. At the same distance from the middle, the dad goes down. But if the son sits twice as far from the middle, they balance. Half the weight, twice the distance. So with a long enough lever, a small push can lift something huge.

The king asked him to prove it. So Archimedes chose a big ship, pulled up on land and full of people and cargo, sat far away, pulled a rope through a set of pulleys, and the ship slid toward him. Alone.

Sources: Plutarch, Life of Marcellus 14; the saying is quoted by Pappus of Alexandria.

💬 So what do you think? With a place to stand, could he really move the Earth? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Archimedes", "#Physics", "#History"],
    tags=["archimedes", "give me a place to stand", "lever", "law of the lever", "physics explained", "seesaw physics",
          "ancient greece", "history facts", "science history", "interestingly strange"],
    pinned_comment="Could he really move the Earth with a long enough lever? YES or NO 👇🌍",
)

SKY, GROUND = hexc("#f6e6c6"), hexc("#d9bf8f")
SPACE = hexc("#1d2340")
GOLD, GOLD_D = hexc("#f2c14e"), hexc("#b9862a")
WOOD, WOOD_D = hexc("#b9824a"), hexc("#8e5a2e")
SEA = hexc("#5aa9d6")
ARCH = "archimedes"
CAST.setdefault(ARCH, dict(skin=hexc("#e8b48a"), shirt=hexc("#3f6fb5"), pants=hexc("#3f6fb5"), bw=96, bh=110,
                           head=40, kind="robe", hair="gray", hair_col=hexc("#e2ddd2"), beard=hexc("#e2ddd2"),
                           seed=261))
CAST.setdefault("hiero", dict(skin=hexc("#f0c29c"), shirt=hexc("#7a2b35"), pants=hexc("#7a2b35"), bw=100, bh=112,
                              head=40, kind="robe", hair="messy", hair_col=hexc("#3a2a22"), beard=hexc("#3a2a22"),
                              seed=263))


def stars(cr, t):
    for k in range(40):
        x = (k * 97) % 760 - 20
        y = (k * 53) % 900 + 120
        a = 0.5 + 0.5 * math.sin(t * 3 + k)
        blob(cr, x, y, 3, 3, hexc("#ffffff", a), seed=k, amp=0.1, lw=0, stroke=None)


def earth(cr, x, y, r, rot=0.0):
    with at(cr, x, y, 1.0, rot=rot):
        blob(cr, 0, 0, r, r, hexc("#4f8fd6"), seed=30, amp=0.4, lw=5)
        for k, (dx, dy, rx, ry) in enumerate(((-r * 0.3, -r * 0.3, r * 0.35, r * 0.25), (r * 0.35, r * 0.1, r * 0.3,
                                                                                         r * 0.4),
                                             (-r * 0.2, r * 0.45, r * 0.25, r * 0.15))):
            blob(cr, dx, dy, rx, ry, hexc("#6cbf5a"), seed=31 + k, amp=0.6, lw=3)


def space_lever(cr, t, tl, push=0.0, talking=False):
    """Archimedes on a rock in space, pushing down the long end of a lever with the Earth on the other end."""
    stars(cr, t)
    px, py = 300, 720
    ang = 0.30 - 0.10 * push
    cx, sx_ = math.cos(ang), math.sin(ang)
    lx, ly = px - 160 * cx, py + 160 * sx_
    rx, ry = px + 290 * cx, py - 290 * sx_
    earth(cr, rx - 10, ry - 102, 100, rot=t * 0.2)
    blob(cr, 210, 860, 210, 44, hexc("#8a7a6a"), seed=42, amp=0.6, lw=4)
    sharp_shape(cr, [(px - 46, 830), (px + 46, 830), (px, py + 6)], hexc("#9a9a9a"), seed=40, amp=0.3, lw=4)
    line(cr, [(lx, ly), (rx, ry)], 14, WOOD, seed=41, amp=0.2)
    person(cr, ARCH, 105, 850, t, facing=1, arms=("give", "give"), eyes="sly" if not talking else "dot",
           mouth=talk(tl, ARCH, t, "smirk"), scale=0.9, lean=0.12 * push)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, (1.0, 360, 640)), (A("a1", "earth."), (1.06, 360, 640))]
    bg(cr, t, keys, SPACE)
    push = ease_out(seg(t, A("a1", "himself."), A("a1", "himself.") + 0.6))
    space_lever(cr, t, tl, push)
    hl(cr, t, [("move the ", INK), ("WHOLE EARTH", BLUE), ("?", INK)], 215, 54, 0.0, bold=True, sound=False,
       halo=hexc("#fbf3e1", 0.95))
    if t >= A("a1", "himself."):
        stamp(cr, t, A("a1", "himself."), "ALONE!", dur=0.7, y=330)
    cue("hit", t, A("a1", "himself."))


def scene_intro(cr, t, tl):
    A = tl.at
    keys = [(A("a2") - 0.2, CLOSE), (A("a2", "syracuse,"), (1.4, 380, 790))]
    bg(cr, t, keys, hexc("#cfe8f5"), GROUND)
    shape(cr, [(-200, 930), (900, 930), (900, 960), (-200, 960)], SEA, seed=50, amp=0.5, lw=3)
    for k, x in enumerate((120, 600)):
        shape(cr, rrect_pts(x - 30, 600, 60, 340, 4, 12), hexc("#efe4cf"), seed=51 + k, amp=0.4, lw=4)
        shape(cr, rrect_pts(x - 44, 584, 88, 26, 4, 10), hexc("#e3d6bd"), seed=53 + k, amp=0.3, lw=4)
    person(cr, ARCH, 360, 960, t, facing=1, arms=("chin", "hip"), eyes="sly", mouth="smile", scale=1.1)
    tag(cr, t, A("a2", "archimedes."), 360, 560, "ARCHIMEDES", GOLD, s=0.7)
    tag(cr, t, A("a2", "syracuse,"), 360, 650, "SYRACUSE, SICILY", hexc("#9fd4ff"), s=0.55, seed=61)
    hl(cr, t, [("over ", INK), ("2,000", RED), (" years ago", INK)], 215, 62, A("a2"), bold=True)


def scene_quote(cr, t, tl):
    A = tl.at
    keys = [(A("a3") - 0.2, (1.0, 360, 640)), (A("a3", "earth."), (1.06, 360, 640))]
    bg(cr, t, keys, SPACE)
    push = ease_out(seg(t, A("a3", "move"), A("a3", "earth.") + 0.3))
    space_lever(cr, t, tl, push, talking=True)
    hl(cr, t, [("\"Give me a place to ", INK), ("STAND", RED)], 215, 54, A("a3", "give"),
       end=A("a3", "move") - 0.05, bold=True, halo=hexc("#fbf3e1", 0.95))
    hl(cr, t, [("...and I will move the ", INK), ("EARTH", BLUE), (".\"", INK)], 215, 52, A("a3", "move"), bold=True,
       halo=hexc("#fbf3e1", 0.95))


def scene_crazy(cr, t, tl):
    A = tl.at
    keys = [(A("a4") - 0.2, CLOSE), (A("a4", "secret"), (1.4, 360, 780))]
    bg(cr, t, keys, SKY, GROUND)
    no = t >= A("a4", "no.")
    person(cr, ARCH, 360, 960, t, facing=1, arms=("point", "hip") if no else ("hip", "hip"),
           eyes="sly" if no else "wide", mouth="smirk" if no else "o", scale=1.15)
    if t < A("a4", "no."):
        for k in range(3):
            write(cr, [("?", RED)], 250 + k * 110, 600 - 30 * (k % 2), 70, bold=True)
    if t >= A("a4", "lever."):
        with at(cr, 360, 560, max(0.6, pop(t, A("a4", "lever."), 0.3))):
            shape(cr, rrect_pts(-200, -70, 400, 140, 18, 12), WHITE, seed=60, amp=0.4, lw=4)
            sharp_shape(cr, [(-20, 40), (20, 40), (0, 10)], hexc("#9a9a9a"), seed=61, amp=0.2, lw=3)
            line(cr, [(-170, 20), (170, 0)], 9, WOOD, seed=62, amp=0.2)
            blob(cr, -140, -6, 26, 20, RED, seed=63, amp=0.3, lw=3)
            write(cr, [("THE LEVER", INK)], 70, -22, 34, align="center", bold=True)
    hl(cr, t, [("was he ", INK), ("CRAZY", RED), ("?", INK)], 215, 70, A("a4"), end=A("a4", "no.") - 0.05, bold=True)
    hl(cr, t, [("the secret of the ", INK), ("LEVER", GREEN)], 215, 62, A("a4", "no."), bold=True)
    cue("hit", t, A("a4", "lever."))


PX, PY = 360, 790          # seesaw pivot (top)
HALF = 260                 # half the plank


def plank_y(d, a):
    return PY - d * math.sin(a)


def scene_seesaw(cr, t, tl):
    A = tl.at
    keys = [(A("a5") - 0.2, (1.15, 360, 700))]
    bg(cr, t, keys, hexc("#cfe8f5"), hexc("#9ccc7a"), ground_y=870)
    # tilt: level -> dad side down (same distance) -> balanced (son twice as far)
    down = ease_out(seg(t, A("a6", "dad"), A("a6", "dad") + 0.6))
    level = ease_out(seg(t, A("a7", "balance."), A("a7", "balance.") + 0.6))
    a = 0.22 * down * (1 - level)
    son_d = lerp(120, 240, ease_out(seg(t, A("a7", "twice"), A("a7", "twice") + 0.8)))
    sharp_shape(cr, [(PX - 60, 870), (PX + 60, 870), (PX, PY + 6)], hexc("#9a9a9a"), seed=70, amp=0.3, lw=4)
    line(cr, [(PX - HALF * math.cos(a), plank_y(-HALF, a)), (PX + HALF * math.cos(a), plank_y(HALF, a))], 16, WOOD,
         seed=71, amp=0.2)
    dad_x, dad_y = PX - 120 * math.cos(a), plank_y(-120, a)
    son_x, son_y = PX + son_d * math.cos(a), plank_y(son_d, a)
    person(cr, "seth", dad_x, dad_y - 4, t, facing=1, arms=("hip", "hip"), eyes="happy" if down < 0.5 or level else
           "sly", mouth="grin", scale=0.95, bob=False)
    person(cr, "chotu", son_x, son_y - 4, t, facing=-1, arms=("cheer", "down") if 0.5 < down and level < 0.5 else
           ("hip", "hip"), eyes="wide" if 0.5 < down and level < 0.5 else "happy", mouth="o" if 0.5 < down and
           level < 0.5 else "grin", scale=1.05, bob=False)
    if A("a5", "60") <= t < A("a8"):
        tag(cr, t, A("a5", "60"), dad_x, dad_y - 320, "60 kg", GOLD, s=0.7)
    if A("a5", "30") <= t < A("a8"):
        tag(cr, t, A("a5", "30"), son_x, son_y - 300, "30 kg", hexc("#9fd4ff"), s=0.7, seed=61)
    if t >= A("a6"):   # distance markers under the plank
        for d, lab, col in ((-120, "1x", GOLD_D), (son_d, "2x" if t >= A("a7", "twice") else "1x", BLUE)):
            x = PX + d * math.cos(a)
            d0 = 45 if d > 0 else -45   # from just outside the pivot to the person, under the plank
            line(cr, [(PX + d0 * math.cos(a), plank_y(d0, a) + 30), (x, plank_y(d, a) + 30)], 6, col,
                 seed=72 + (d > 0), amp=0.2)
            write(cr, [(lab, col)], x, plank_y(d, a) + 66, 46, align="center", bold=True)
    if t >= A("a8"):
        card(cr, t, A("a8"), 360, 455, 0.85, "HALF the weight", "TWICE the distance", top_col=INK, bottom_col=RED,
             seed=73, w=560)
    hl(cr, t, [("a ", INK), ("SEESAW", GREEN)], 215, 70, A("a5"), end=A("a6") - 0.05, bold=True)
    hl(cr, t, [("same distance: ", INK), ("dad wins", RED)], 215, 60, A("a6"), end=A("a7") - 0.05, bold=True)
    hl(cr, t, [("twice as far: ", INK), ("BALANCE", GREEN)], 215, 60, A("a7"), end=A("a8") - 0.05, bold=True)
    cue("hit", t, A("a7", "balance."))


def ship(cr, x, y, s=1.0):
    with at(cr, x, y, s):
        line(cr, [(0, -40), (0, -300)], 8, WOOD_D, seed=80, amp=0.2)
        shape(cr, [(6, -290), (130, -170), (6, -110)], hexc("#f4efe1"), seed=81, amp=0.6, lw=4)
        for k in range(5):
            blob(cr, -150 + k * 70, -62, 20, 20, (hexc("#f0c29c"), hexc("#e8b48a"), hexc("#c99a72"))[k % 3],
                 seed=82 + k, amp=0.3, lw=3)
        shape(cr, [(-230, -40), (230, -40), (170, 50), (-170, 50)], WOOD, seed=88, amp=0.5, lw=5)
        for k in range(3):
            line(cr, [(-200 + k * 12, -10 + k * 18), (200 - k * 12, -10 + k * 18)], 3, WOOD_D, seed=89 + k, amp=0.4)


def scene_ship(cr, t, tl):
    A = tl.at
    keys = [(A("a9") - 0.2, (1.1, 380, 760))]
    bg(cr, t, keys, hexc("#cfe8f5"), hexc("#e6cf9a"), ground_y=900)
    slide = ease_out(seg(t, A("a10", "slid"), A("a10", "slid") + 1.4))
    sx = lerp(200, 320, slide)
    if t >= A("a9", "ship,"):
        ship(cr, sx, 850, max(0.6, pop(t, A("a9", "ship,"), 0.3)) * 0.6)
    if t < A("a10"):
        person(cr, "hiero", 560, 900, t, facing=-1, arms=("point", "hip"), eyes="sly", mouth="smirk", scale=0.85)
        hx, hy = head_c("hiero", 560, 900, 0.85)
        sharp_shape(cr, [(hx - 28, hy - 30), (hx - 28, hy - 56), (hx - 14, hy - 42), (hx, hy - 62), (hx + 14, hy - 42),
                         (hx + 28, hy - 56), (hx + 28, hy - 30)], GOLD, seed=90, amp=0.3, lw=3)
        tag(cr, t, A("a9"), 560, 560, "KING HIERO", GOLD, s=0.55)
    else:   # pulleys and a rope from the ship to Archimedes, sitting far away
        for k, (x, y) in enumerate(((560, 800), (600, 760))):
            blob(cr, x, y, 22, 22, hexc("#9a9a9a"), seed=91 + k, amp=0.2, lw=4)
        line(cr, [(sx + 130, 830), (560, 778), (600, 782), (630, 860)], 4, INK, seed=93, amp=0.3)
        pull = math.sin(t * 6) * 8 if 0 < slide < 1 else 0
        person(cr, ARCH, 650, 900, t, facing=-1, arms=("hold", "hold"), eyes="happy" if slide >= 1 else "sly",
               mouth="grin" if slide >= 1 else "smirk", scale=0.85, lean=-0.1 + pull * 0.005)
        tag(cr, t, A("a10", "pulleys."), 580, 640, "PULLEYS", hexc("#9fd4ff"), s=0.5, seed=62)
    if t >= A("a9", "people"):
        tag(cr, t, A("a9", "people"), 230, 560, "PEOPLE + CARGO", hexc("#ffe6a0"), s=0.5, seed=63)
    hl(cr, t, [("\"", INK), ("PROVE", RED), (" it.\"", INK)], 215, 70, A("a9"), end=A("a9", "so") - 0.05, bold=True)
    hl(cr, t, [("a ship ", INK), ("ON LAND", RED)], 215, 66, A("a9", "so"), end=A("a10") - 0.05, bold=True)
    hl(cr, t, [("pulled ", INK), ("ALONE", GREEN)], 215, 70, A("a10"), bold=True)
    if t >= A("a10", "alone."):
        stamp(cr, t, A("a10", "alone."), "BY HIMSELF!", dur=0.8, y=330)
    cue("hit", t, A("a10", "slid"))


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("a11") - 0.2, (1.0, 360, 640))]
    bg(cr, t, keys, SPACE)
    space_lever(cr, t, tl, 0.5 + 0.5 * math.sin(t * 2))
    buttons(cr, t, A("a11", "earth?"), (("YES", GREEN), ("NO", RED)), y=1060, s=0.75)
    hl(cr, t, [("could he ", INK), ("REALLY", RED), ("?", INK)], 215, 70, A("a11", "with"), bold=True,
       underline=True, halo=hexc("#fbf3e1", 0.95))
    stamp(cr, t, A("a11", "earth?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "intro": scene_intro, "quote": scene_quote, "crazy": scene_crazy, "seesaw": scene_seesaw,
     "ship": scene_ship, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
