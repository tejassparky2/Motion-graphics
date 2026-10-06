"""Episode 3: "The Zombie Ant" — the Ophiocordyceps fungus that hijacks carpenter ants.

Facts (checked against Wikipedia's article on Ophiocordyceps unilateralis, which cites the primary research):
- infected ants leave their canopy nest after convulsions knock them down to the forest floor
- the ant clamps its jaws onto a major vein on the underside of a leaf, generally ~26 cm above the forest floor
- the biting is synchronised around solar noon
- infection to death takes 4-10 days
- the fruiting stalk grows from the back of the neck (dorsal pronotum); spores fall onto ants below
"""
import math

from motion.captions import captions
from motion.critters import ant, spores, stalk
from motion.engine import INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict()   # channel default narrator

SCRIPT = [
    dict(id="z1", scene="canopy", text="This ant is about to become a zombie. And it has no idea."),
    dict(id="z2", scene="canopy", text="It's a carpenter ant in the rainforest, and a tiny fungus spore just landed on it."),
    dict(id="z3", scene="canopy",
         text="Over the next [four to ten days,|4-10 days,] the fungus spreads through its body, and starts taking control."),
    dict(id="z4", scene="fall", text="The ant starts shaking, and falls out of its nest in the treetops."),
    dict(id="z5", scene="plant",
         text="Then it climbs a plant, to about [twenty-six centimeters|26 cm] above the ground. Almost always around that height."),
    dict(id="z6", scene="leaf", text="Around noon, it bites the big vein under a leaf, and locks its jaws. For good.", gap=0.25),
    dict(id="z7", scene="leaf", text="Scientists call it the death grip.", pace=0.92),
    dict(id="z8", scene="stalk",
         text="Days later, a stalk grows out of the back of its neck, and rains spores onto the ants walking below.", gap=0.25),
    dict(id="z9", scene="stalk", text="And the whole thing starts again."),
]

METADATA = dict(
    title="This Fungus Turns Ants Into Zombies 🧟🐜",
    alt_titles=["The Ant That Doesn't Know It's a Zombie 🐜", "Nature's Scariest Mind Control Is Real 🍄"],
    description="""This ant is about to become a zombie… and it has no idea. 🧟

A fungus called Ophiocordyceps takes over carpenter ants in the rainforest. It makes them climb to almost the exact same height, bite a leaf at around noon, and lock their jaws forever — then it sprouts out of the ant's neck to infect the next one. 🍄

Real science: the "death grip" was studied by researchers in tropical forests, and the fungus was first described by naturalist Alfred Russel Wallace in 1859.

💬 Would you rather be the ant or the fungus?

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#ZombieAnt", "#WeirdAnimals", "#Nature"],
    tags=["zombie ant", "zombie ant fungus", "ophiocordyceps", "cordyceps", "mind control fungus", "weird animals",
          "insect facts", "nature facts", "science shorts", "interestingly strange"],
    pinned_comment="Cordyceps is real — but only for ants 😅 What weird animal should we do next? 👇",
)

JUNGLE = hexc("#2f6b45")
JUNGLE_L = hexc("#4f9a58")
JUNGLE_D = hexc("#234f35")
BARK = hexc("#7a5234")
GREEN = hexc("#3d8f45")
PURPLE = hexc("#8a63d2")


def leaf(cr, x, y, w, h, rot=0.0, color=JUNGLE_L, seed=0, vein=True):
    with at(cr, x, y, 1.0, rot=rot):
        pts = []
        for i in range(24):
            a = 2 * math.pi * i / 24
            r = 1 - 0.35 * abs(math.sin(a)) ** 3
            pts.append((w / 2 * math.cos(a) * r, h / 2 * math.sin(a) * (1.1 if math.cos(a) > 0 else 0.9)))
        shape(cr, pts, color, seed=seed, amp=1.0, lw=4)
        if vein:
            line(cr, [(-w / 2 + 8, 0), (0, -3), (w / 2 - 10, 0)], 4, JUNGLE_D, seed=seed + 1, amp=0.6)
            for k in range(-3, 4):
                if k:
                    line(cr, [(k * w / 9, -1), (k * w / 9 + w / 12, -h / 3 if k % 2 else h / 3)], 2.5, JUNGLE_D,
                         seed=seed + 2 + k, amp=0.5)


def jungle_bg(cr, t, light=0.0):
    cr.set_source_rgba(*JUNGLE)
    cr.paint()
    for i, (x, y, r) in enumerate([(-200, 380, 220), (500, 300, 260), (200, 1150, 300), (900, 900, 260),
                                    (-150, 900, 240), (820, 420, 200)]):
        blob(cr, x, y, r, r * 0.8, JUNGLE_D, seed=1000 + i, amp=6, lw=0, stroke=None)
    for i, (x, y) in enumerate([(120, 330), (640, 520), (60, 760), (700, 1000), (300, 1180)]):
        blob(cr, x, y, 60, 40, hexc("#bfe3c9", 0.25 + light), seed=1010 + i, amp=4, lw=0, stroke=None)
    for i, x in enumerate((-60, 780)):   # vines
        line(cr, [(x, 200), (x + 40, 500), (x - 20, 800), (x + 30, 1300)], 7, JUNGLE_D, seed=1020 + i, amp=2)


# ---------------------------------------------------------------- scenes
def scene_canopy(cr, t, tl):
    A = tl.at
    keys = [(0, (1.5, 380, 700)), (A("z1", "zombie"), (2.0, 420, 690)), (A("z1", "no"), (2.4, 470, 680)),
            (A("z1", "idea"), (1.5, 380, 700)), (A("z2", "carpenter"), (2.1, 360, 700)),
            (A("z2", "rainforest"), (1.2, 380, 640)), (A("z2", "fungus"), (1.8, 440, 600)),
            (A("z2", "spore"), (2.1, 420, 690)), (A("z3"), (1.6, 400, 700)), (A("z3", "fungus"), (2.3, 340, 700)),
            (A("z3", "body"), (1.7, 420, 700)), (A("z3", "control"), (2.4, 470, 680))]
    z, fx, fy = camera(t, keys)
    if t < A("z1", "zombie"):
        z += 0.05 * seg(t, 0, A("z1", "zombie"))
    set_camera((z, fx, fy))
    enter_world(cr)
    jungle_bg(cr, t)
    # the branch the colony walks on
    shape(cr, [(-800, 730), (1500, 700), (1500, 770), (-800, 800)], BARK, seed=1100, amp=2.0, lw=5)
    for i in range(6):
        leaf(cr, -200 + i * 230, 690 - (i % 2) * 30, 150, 60, rot=-0.3 + 0.2 * (i % 3), seed=1110 + i * 5)
    # a trail of healthy ants in the background, and our ant
    for i in range(4):
        ax = (-300 + i * 260 + t * 60) % 1300 - 300
        ant(cr, ax, 735, t, s=0.55, walk=ax / 90, seed=40 + i)
    infect = A("z2", "spore")
    zombie = 0.0 if t < A("z3") else min(1.0, 0.2 + seg(t, A("z3"), A("z3", "control")) * 0.8)
    walking = t < A("z3", "control")
    ant(cr, 400, 745, t, s=1.1, walk=(t * 1.2) if walking else None, zombie=zombie,
        eye="wide" if infect <= t < A("z3") else "normal", seed=7)
    # the spore floating down and landing
    if A("z2") <= t < infect + 0.2:
        u = seg(t, A("z2"), infect)
        dot(cr, lerp(470, 350, u) + math.sin(t * 6) * 8, lerp(420, 650, u), 7, hexc("#f3ead0"))
    if t >= infect:
        cue("pop", t, infect)
    hl(cr, t, [("ZOMBIE", PURPLE), (" ant?", INK)], 215, 70, A("z1", "zombie"), end=A("z2") - 0.05, bold=True)
    hl(cr, t, [("1 tiny ", INK), ("spore", GREEN)], 215, 66, A("z2", "spore"), end=A("z3") - 0.05, bold=True)
    hl(cr, t, [("4-10 days", RED)], 215, 72, A("z3", "4-10"), bold=True, underline=True)


def scene_fall(cr, t, tl):
    A = tl.at
    fall = A("z4", "falls")
    z, fx, fy = camera(t, [(A("z4") - 0.2, (1.8, 400, 690)), (fall, (1.2, 400, 900))], dur=0.5)
    set_camera((z, fx, fy))
    enter_world(cr)
    jungle_bg(cr, t)
    shape(cr, [(-800, 730), (1500, 700), (1500, 770), (-800, 800)], BARK, seed=1100, amp=2.0, lw=5)
    sharp_line = hexc("#3a2a1e")
    shape(cr, [(-800, 1260), (1500, 1240), (1500, 1800), (-800, 1800)], hexc("#4a3526"), seed=1150, amp=2, lw=5)
    for i in range(10):
        leaf(cr, -300 + i * 150, 1255, 90, 34, rot=0.2 * (i % 3), color=hexc("#8a6a3a"), seed=1160 + i, vein=False)
    u = ease_out(seg(t, fall, fall + 0.8))
    y = lerp(745, 1250, u * u)
    ant(cr, 400 + u * 40, y, t, s=1.1, zombie=1.0, tilt=u * 3.0, seed=7)
    cue("whoosh", t, fall, 0.5)
    cue("thud", t, fall + 0.8)
    hl(cr, t, [("*shake shake*", PURPLE)], 215, 62, A("z4", "shaking"), end=fall, bold=True)
    hl(cr, t, [("down it goes...", INK)], 215, 62, fall, bold=True)


def scene_plant(cr, t, tl):
    A = tl.at
    top = A("z5", "26")
    z, fx, fy = camera(t, [(A("z5") - 0.2, (1.3, 380, 820)), (A("z5", "climbs"), (1.5, 380, 760)),
                           (A("z5", "plant"), (1.9, 410, 820)), (A("z5", "about"), (1.4, 340, 700)),
                           (top, (1.7, 360, 640)), (A("z5", "Almost"), (1.4, 380, 720))])
    set_camera((z, fx, fy))
    enter_world(cr)
    jungle_bg(cr, t)
    shape(cr, [(-800, 1000), (1500, 990), (1500, 1800), (-800, 1800)], hexc("#4a3526"), seed=1200, amp=2, lw=5)
    # plant stem with leaves
    line(cr, [(400, 1000), (396, 800), (404, 600), (400, 380)], 16, INK, seed=1201, amp=0.8)
    line(cr, [(400, 1000), (396, 800), (404, 600), (400, 380)], 10, hexc("#6aa84f"), seed=1201, amp=0.8)
    leaf(cr, 520, 470, 220, 90, rot=-0.25, seed=1205)
    leaf(cr, 290, 640, 200, 80, rot=0.3, seed=1210)
    # ruler
    shape(cr, rrect_pts(170, 450, 50, 550, 6, 20), hexc("#ffd23f"), seed=1215, amp=0.6, lw=3.5)
    for k in range(0, 27, 2):
        yy = 1000 - k * 20
        line(cr, [(170, yy), (190 if k % 10 else 205, yy)], 3, INK, seed=1216 + k, amp=0.2)
    write(cr, [("26", INK)], 195, 470, 24, align="center", bold=True)
    # the ant climbing the stem
    u = ease_out(seg(t, A("z5", "climbs"), top))
    ant(cr, 412, lerp(1000, 480, u), t, s=0.8, walk=t * 1.5 if u < 1 else None, zombie=1.0, tilt=-math.pi / 2,
        seed=7)
    hl(cr, t, [("26 cm", RED)], 215, 90, top, bold=True, underline=True)
    hl(cr, t, [("almost ", INK), ("every time", RED)], 305, 56, A("z5", "Almost"), bold=True)


def scene_leaf(cr, t, tl):
    A = tl.at
    bite = A("z6", "bites")
    lock = A("z6", "locks")
    z, fx, fy = camera(t, [(A("z6") - 0.2, (1.2, 380, 700)), (A("z6", "noon"), (1.1, 380, 620)),
                           (bite, (1.6, 400, 720)), (lock, (2.2, 470, 700)), (A("z7"), (1.5, 400, 720)),
                           (A("z7", "death"), (1.9, 430, 720))])
    set_camera((z, fx, fy))
    enter_world(cr)
    jungle_bg(cr, t, light=0.2)
    # sun + clock at noon
    s_ = pop(t, A("z6", "noon"), 0.3)
    if s_:
        with at(cr, 560, 330, s_):
            blob(cr, 0, 0, 70, 70, hexc("#ffd23f"), seed=1300, amp=1, lw=4)
            write(cr, [("12:00", INK)], 0, 12, 36, align="center", bold=True)
    # a big leaf seen from below, the vein running across
    leaf(cr, 380, 620, 640, 240, rot=-0.08, seed=1310)
    # the ant hanging under the vein
    gripping = t >= bite
    ant(cr, 330, 860, t, s=1.3, zombie=1.0, grip=gripping, tilt=-0.35 if gripping else 0.0, seed=7)
    if t >= lock:
        cue("hit", t, lock)
        for k in range(3):   # 'locked' marks
            sc = pop(t, lock + k * 0.08, 0.2)
            if sc <= 0:
                continue
            with at(cr, 480 + k * 22, 640 - k * 14, sc):
                line(cr, [(-8, 0), (8, 0)], 5, RED, seed=1320 + k, amp=0.2)
    hl(cr, t, [("12:00 ", INK), ("NOON", RED)], 215, 66, A("z6", "noon"), end=A("z7") - 0.05, bold=True)
    hl(cr, t, [("jaws: ", INK), ("LOCKED", RED)], 295, 62, lock, end=A("z7") - 0.05, bold=True)
    stamp(cr, t, A("z7", "death"), "DEATH GRIP", dur=1.3, y=420, color="#ff5a5f")


def scene_stalk(cr, t, tl):
    A = tl.at
    grow = A("z8", "stalk")
    rain = A("z8", "rains")
    z, fx, fy = camera(t, [(A("z8") - 0.2, (1.6, 400, 720)), (A("z8", "later"), (1.3, 380, 760)),
                           (grow, (2.0, 420, 640)), (A("z8", "back"), (2.5, 390, 700)), (rain, (1.2, 400, 820)),
                           (A("z8", "walking"), (1.8, 420, 1100)),
                           (A("z9"), (1.4, 380, 900)), (A("z9", "again"), (1.9, 300, 1000))])
    set_camera((z, fx, fy))
    enter_world(cr)
    jungle_bg(cr, t, light=0.1)
    shape(cr, [(-800, 1180), (1500, 1170), (1500, 1800), (-800, 1800)], hexc("#4a3526"), seed=1400, amp=2, lw=5)
    leaf(cr, 380, 620, 640, 240, rot=-0.08, seed=1310)
    ant(cr, 330, 860, t, s=1.3, zombie=1.0, grip=True, tilt=-0.35, seed=7)
    h = 170 * ease_out(seg(t, grow, grow + 1.2))
    stalk(cr, 385, 770, h, t, seed=1410)   # from the back of the neck
    spores(cr, 390, 620, t, rain, spread=320)
    # ants walking on the forest floor below
    for i in range(3):
        ax = (-200 + i * 300 + t * 70) % 1100 - 200
        ant(cr, ax, 1190, t, s=0.55, walk=ax / 80, seed=60 + i,
            eye="spiral" if (i == 1 and t >= A("z9", "again")) else "normal")
    stamp(cr, t, A("z7", "death"), "DEATH GRIP", dur=1.3, y=420, color="#ff5a5f")   # carries over the cut
    hl(cr, t, [("out of its ", INK), ("neck", RED)], 215, 64, A("z8", "neck"), end=rain - 0.3, bold=True)
    hl(cr, t, [("spores ", GREEN), ("rain down", INK)], 215, 64, rain, end=A("z9") - 0.05, bold=True)
    hl(cr, t, [("...and again.", PURPLE)], 215, 70, A("z9", "again"), bold=True, underline=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"canopy": scene_canopy, "fall": scene_fall, "plant": scene_plant, "leaf": scene_leaf,
     "stalk": scene_stalk}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
