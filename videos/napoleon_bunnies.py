"""Funny history F1: "Napoleon Lost a Battle. To Bunnies." -- in the owner's reference narration style (Abhay Create:
talks to the viewer, "bro", modern comparisons, big set-up / flat landing).

Script: out/scripts_funny_history.md, F1 narration-style version (owner approved 15 Oct 2026). The story comes from
General Paul Thiébault's memoirs, published decades later; numbers vary (hundreds to 3,000), so "about a thousand"
and "the story comes from one of his own generals". Turbo voice with tags (narrator only, stock voice).
"""
import math
import random

from motion import thriller as th
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, appear, bold_text, camera, captions, ellipse, enter, lin, paint, rad,
                           rrect, sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 0.9
FUR = [hexc(c) for c in ("#f4f1ec", "#c9b8a6", "#9a8676", "#e8dcc8", "#7a6a5c")]

SCRIPT = [
    dict(id="b1", scene="hook", text="Napoleon conquered half of Europe. Bro was unstoppable. And then he lost a "
                                     "battle. To bunnies."),
    dict(id="b2", scene="party", text="[Eighteen oh seven.|1807.] He's just signed a peace deal, so his right-hand "
                                      "man says: let's party. A rabbit hunt."),
    dict(id="b3", scene="cages", text="And look at this guy's planning. A thousand rabbits. Ordered. Delivered. Cages "
                                      "ready. [chuckle]"),
    dict(id="b4", scene="tame", text="Just one tiny problem. He bought tame rabbits. Pet rabbits. From farmers."),
    dict(id="b5", scene="charge", text="Now think about it. The cage doors open. And the rabbits look at Napoleon like he's "
                                       "the Zomato delivery guy."),
    dict(id="b6", scene="charge", text="A thousand bunnies. Sprinting. At the most feared man in Europe."),
    dict(id="b7", scene="run", text="Up his boots. Into his coat. Bro is running to his carriage, swatting rabbits "
                                    "with his hat. [laugh]"),
    dict(id="b8", scene="carriage", text="Even the carriage got invaded. Ears sticking out of the windows."),
    dict(id="b9", scene="loo", text="Everyone talks about Waterloo. Nobody talks about [Bunny-loo.|Bunnyloo.]"),
    dict(id="b10", scene="end", text="So who wins. Napoleon, or a thousand bunnies?", gap=0.3),
]

METADATA = dict(
    title="Napoleon Lost a Battle. To Bunnies. 🐰",
    alt_titles=["Napoleon vs 1,000 Bunnies 🐰 (He Lost)", "The Rabbit Hunt That Went Horribly Wrong 🐰"],
    description="""Napoleon conquered half of Europe. And then he lost a battle... to bunnies. 🐰

1807: after a peace treaty, his chief of staff threw a celebration rabbit hunt and ordered about a thousand rabbits. One tiny problem: they were tame rabbits from farmers. So when the cages opened, the rabbits didn't run away. They ran straight at Napoleon, thinking he had food. 😂

The story comes from the memoirs of one of his own generals (published decades later, so take the details with a pinch of salt).

💬 Who wins: Napoleon, or a thousand bunnies? 👇

🔔 Interestingly Strange: funny history, clever twists and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#FunnyHistory", "#Napoleon", "#Shorts"],
    tags=["napoleon rabbits", "napoleon bunnies", "funny history", "napoleon", "history facts", "weird history",
          "bunnyloo", "history memes", "rabbit hunt", "interestingly strange"],
    pinned_comment="Team Napoleon 🎩 or Team Bunnies 🐰? 👇",
)


# ---------------------------------------------------------------- props
def rabbit(cr, t, x, y, s=1.0, facing=1, hop=0.0, col=None, bowtie=False, eyes="open", seed=0):
    """A small round bunny, feet at (x, y). `hop` 0..1 lifts it."""
    col = col or FUR[seed % len(FUR)]
    cr.save()
    cr.translate(x, y - 40 * s * math.sin(math.pi * hop))
    cr.scale(s * facing, s)
    ellipse(cr, -30, -40, 14, 14)                                  # tail puff
    paint(cr, WHITE, OUTLINE, 4)
    ellipse(cr, 0, -40, 44, 36)                                    # body
    paint(cr, col, OUTLINE, 5)
    for k, dx in enumerate((14, 30)):                              # ears
        cr.save()
        cr.translate(dx, -86)
        cr.rotate(-0.25 + 0.3 * k + 0.08 * math.sin(t * 5 + seed))
        ellipse(cr, 0, -34, 10, 32)
        paint(cr, col, OUTLINE, 4)
        ellipse(cr, 0, -32, 5, 22)
        paint(cr, hexc("#ffb3c1"), None)
        cr.restore()
    ellipse(cr, 26, -70, 28, 25)                                   # head
    paint(cr, col, OUTLINE, 5)
    if eyes == "happy":
        stroke_line(cr, [(30, -74), (36, -80), (42, -74)], 4, OUTLINE)
    else:
        cr.arc(36, -76, 5, 0, 2 * math.pi)
        paint(cr, hexc("#2b1d16"), None)
        cr.arc(37.5, -78, 1.8, 0, 2 * math.pi)
        paint(cr, WHITE, None)
    cr.arc(52, -66, 4, 0, 2 * math.pi)
    paint(cr, hexc("#ff8fa3"), None)
    if bowtie:
        cr.move_to(20, -46)
        cr.line_to(6, -54)
        cr.line_to(6, -38)
        cr.close_path()
        cr.move_to(20, -46)
        cr.line_to(34, -54)
        cr.line_to(34, -38)
        cr.close_path()
        paint(cr, RED, OUTLINE, 3)
    cr.restore()


def cage(cr, x, y, s=1.0, open_=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -70, -110, 140, 110, 6)
    paint(cr, hexc("#c99460"), OUTLINE, 6)
    for k in range(5):
        stroke_line(cr, [(-50 + k * 25, -100), (-50 + k * 25, -10)], 5, hexc("#6a4a2a"), curve=False)
    if open_:
        cr.save()
        cr.translate(-70, -110)
        cr.rotate(-1.4 * open_)
        rrect(cr, 0, 0, 140, 16, 4)
        paint(cr, hexc("#a87444"), OUTLINE, 5)
        cr.restore()
    cr.restore()


def carriage(cr, t, x, y, s=1.0, ears=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -170, -230, 340, 190, 30)                            # cabin
    paint(cr, lin(0, -230, 0, -40, [(0, hexc("#2a3a7a")), (1, hexc("#1a2450"))]), OUTLINE, 8)
    rrect(cr, -150, -210, 300, 20, 6)
    paint(cr, GOLD, OUTLINE, 4)
    for k, wx in enumerate((-90, 50)):                             # windows
        rrect(cr, wx, -180, 80, 80, 10)
        paint(cr, hexc("#cfe6ff"), OUTLINE, 5)
        if ears:                                                   # bunny ears poking out of the windows
            for j in range(2):
                e = ease_out(min(1, ears * 1.5 - 0.3 * (k + j)))
                if e > 0:
                    ellipse(cr, wx + 25 + j * 30, -170 - 30 * e, 9, 26 * e)
                    paint(cr, FUR[(k + j) % 4], OUTLINE, 4)
    for wx in (-110, 110):                                         # wheels
        cr.arc(wx, -20, 55, 0, 2 * math.pi)
        paint(cr, hexc("#3a2418"), OUTLINE, 6)
        for k in range(6):
            a = k * math.pi / 3 + t
            stroke_line(cr, [(wx, -20), (wx + 50 * math.cos(a), -20 + 50 * math.sin(a))], 4, GOLD, curve=False)
    cr.restore()


def field(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#9fd6ff")), (0.5, hexc("#dff2ff")), (0.51, hexc("#9bd87a")),
                                   (1, hexc("#5aa043"))]))
    cr.fill()
    for k, (x, y, r) in enumerate(((120, 640, 120), (560, 620, 160))):    # bushes
        cr.arc(x, y, r, math.pi, 2 * math.pi)
        paint(cr, hexc("#4a9a3a"), OUTLINE, 6)


def herd(cr, t, start, n, x0, x1, y0, y1, target=None, speed=1.0, seed=1):
    """`n` bunnies hopping from the left side toward `target` (x) since `start`."""
    rng = random.Random(seed)
    for k in range(n):
        st = start + rng.random() * 0.8
        if t < st:
            continue
        u = (t - st) * speed
        x = lerp(x0, x1, rng.random())
        y = lerp(y0, y1, rng.random())
        if target is not None:                                     # hop toward the target, then mill around it
            x = lerp(x, target + rng.uniform(-120, 120), min(1, u * 0.5))
        rabbit(cr, t, x, y, 0.55 + 0.25 * (y - y0) / max(1, y1 - y0), facing=1 if target is None or target > x else -1,
               hop=abs(math.sin((t + k) * 7)) * 0.5, seed=k)


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    field(cr, t)
    lost = t >= A("b1", "bunnies.")
    cr.save()
    enter(cr, camera(t, [(0.0, (1.0, 360, 640)), (A("b1", "lost"), (1.15, 360, 640))], dur=0.8))
    person(cr, t, 360, 900, 1.0, "napoleon", eyes="wide" if lost else "half", mouth="o" if lost else "smug",
           arms=("up", "up") if lost else ("chin", "hips"), brows="up" if lost else "raise")
    if lost:                                                       # the bunny pile-on
        for k in range(14):
            st = A("b1", "bunnies.") + 0.05 * k
            if t >= st:
                u = ease_out(seg(t, st, st + 0.35))
                ang = k * 0.9
                rabbit(cr, t, 360 + math.cos(ang) * 160 * (1 - 0.5 * u), lerp(1300, 760 + (k % 4) * 40, u), 0.8,
                       facing=1 if math.cos(ang) < 0 else -1, seed=k)
        cue("pop", t, A("b1", "bunnies."))
    cr.restore()
    vignette(cr, 0.3)


def scene_party(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffe7a8"), hexc("#fff6e8"), seed=3)
    sign(cr, t, A("b2"), 360, 170, "1807", col=PURPLE, size=90, end=A("b2", "peace") - 0.05)
    if t >= A("b2", "peace"):                                      # the treaty
        k = appear(t, A("b2", "peace"), 0.4)
        cr.save()
        cr.translate(360, 520)
        cr.scale(k, k)
        rrect(cr, -170, -200, 340, 400, 10)
        paint(cr, hexc("#fff3d6"), OUTLINE, 6)
        for j in range(7):
            stroke_line(cr, [(-130, -150 + j * 40), (110, -150 + j * 40)], 4, (0.3, 0.2, 0.1, 0.5), curve=False)
        bold_text(cr, "PEACE", 0, -160, 50, hexc("#8a5a2e"))
        stroke_line(cr, [(-90, 150), (-40, 120), (10, 160), (70, 125)], 5, BLUE)
        cr.restore()
    if t >= A("b2", "party."):
        person(cr, t, 560, 1000, 0.65, "napoleon", bicorne=None, suit=hexc("#3a5a2a"), eyes="happy", mouth="grin",
               arms=("wave", "hips"))
        sign(cr, t, A("b2", "party."), 360, 170, "LET'S PARTY!", col=GOLD, size=76, end=A("b2", "rabbit") - 0.05)
        sign(cr, t, A("b2", "rabbit"), 360, 170, "VICTORY RABBIT HUNT", col=GREEN, size=54)
    vignette(cr, 0.3)


def scene_cages(cr, t, tl):
    A = tl.at
    field(cr, t)
    keys = ("Ordered.", "Delivered.", "Cages")
    for k in range(9):                                             # cages stacking up
        st = A("b3", "thousand") + 0.12 * k
        if t >= st:
            u = ease_out(seg(t, st, st + 0.3))
            cage(cr, 140 + (k % 3) * 220, lerp(-200, 760 - (k // 3) * 120, u), 0.9)
    for j, key in enumerate(keys):
        if t >= A("b3", key):
            stamp(cr, t, A("b3", key), 360, 260 + j * 90, key.rstrip(".").upper(), col=GREEN, size=50, rot=-0.05)
    sign(cr, t, A("b3", "planning."), 360, 140, "1,000 RABBITS", col=PURPLE, size=72)
    vignette(cr, 0.3)


def scene_tame(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd6e0"), hexc("#fff6e8"), seed=5)
    rabbit(cr, t, 360, 760, 2.6, bowtie=t >= A("b4", "Pet"), eyes="happy" if t >= A("b4", "Pet") else "open", seed=0)
    if t >= A("b4", "farmers."):
        person(cr, t, 600, 1020, 0.55, "villager", eyes="happy", mouth="grin", arms=("wave", "down"))
    stamp(cr, t, A("b4", "tame"), 360, 300, "TAME", col=RED, size=96, end=A("b4", "Pet") - 0.05)
    sign(cr, t, A("b4", "Pet"), 360, 300, "PET RABBITS", col=PURPLE, size=72)
    sign(cr, t, A("b4", "problem."), 360, 140, "ONE TINY PROBLEM", col=RED, size=56, end=A("b4", "tame") - 0.05)
    cue("hit", t, A("b4", "tame"))
    vignette(cr, 0.3)


def scene_charge(cr, t, tl):
    A = tl.at
    field(cr, t)
    opened = A("b5", "open.")
    cage(cr, 110, 720, 0.8, open_=seg(t, opened, opened + 0.3))
    cr.save()
    enter(cr, camera(t, [(A("b5") - 0.3, (1.0, 360, 640)), (A("b6"), (1.1, 420, 660))], dur=0.6))
    scared = t >= A("b6")
    person(cr, t, 560, 940, 0.8, "napoleon", facing=-1, eyes="wide" if scared else "open",
           mouth="o" if scared else "smile", arms=("up", "up") if scared else ("hips", "hips"))
    if t >= opened:
        herd(cr, t, opened, 18 if t < A("b6") else 30, 0, 300, 860, 1000, target=520, speed=0.8, seed=2)
    if t >= A("b5", "Zomato"):                                     # what the bunnies see
        rrect(cr, 380, 500, 300, 110, 30)
        paint(cr, WHITE, OUTLINE, 6)
        bold_text(cr, "FOOD GUY?", 530, 572, 44, RED)
    cr.restore()
    sign(cr, t, A("b6", "thousand"), 360, 150, "1,000 BUNNIES", col=PURPLE, size=70, end=A("b6", "feared") - 0.05)
    sign(cr, t, A("b6", "feared"), 360, 150, "MOST FEARED MAN", col=RED, size=60)
    vignette(cr, 0.3)


def scene_run(cr, t, tl):
    A = tl.at
    field(cr, t)
    run_x = lerp(560, 200, seg(t, A("b7", "running"), A("b7", "hat.", end=True)))
    cr.save()
    enter(cr, camera(t, [(A("b7") - 0.3, (1.15, 400, 640))]))

    def hat(c, hx, hy):
        c.save()
        c.translate(hx, hy - 20)
        c.rotate(math.sin(t * 12) * 0.8)
        c.move_to(-60, 0)
        c.curve_to(-40, -50, 40, -50, 60, 0)
        c.close_path()
        paint(c, hexc("#1a1a2a"), OUTLINE, 5)
        c.restore()

    person(cr, t, run_x, 960, 0.85, "napoleon", bicorne=None, facing=-1, eyes="wide", mouth="o",
           arms=("hold", "up"), hold=hat if t >= A("b7", "swatting") else None, walk=t * 14, run=True)
    for k in range(3):                                             # bunnies clinging on
        if t >= A("b7", ("boots.", "coat.", "running")[k]):
            rabbit(cr, t, run_x - 20 + k * 25, 960 - 120 - 130 * k, 0.5, seed=k + 3)
    herd(cr, t, A("b7") - 0.5, 16, 600, 760, 900, 1020, target=run_x, speed=1.0, seed=4)
    cr.restore()
    sign(cr, t, A("b7", "running"), 360, 150, "RETREAT!", col=RED, size=80)
    vignette(cr, 0.3)


def scene_carriage(cr, t, tl):
    A = tl.at
    field(cr, t)
    carriage(cr, t * 0.2, 360, 900, 1.2, ears=seg(t, A("b8", "Ears"), A("b8", "windows.", end=True)))
    herd(cr, t, A("b8"), 8, 60, 660, 960, 1040, seed=6)
    stamp(cr, t, A("b8", "invaded."), 360, 260, "INVADED", col=RED, size=86)
    cue("hit", t, A("b8", "invaded."))
    vignette(cr, 0.3)


def scene_loo(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cfe6ff"), hexc("#fff6e8"), seed=7)
    sign(cr, t, A("b9", "Waterloo."), 360, 380, "WATERLOO 1815", col=BLUE, size=64)
    if t >= A("b9", "Nobody"):
        k = seg(t, A("b9", "Nobody"), A("b9", "Nobody") + 0.3)
        stroke_line(cr, [(120, 360), (lerp(120, 600, k), 360 - 30 * k)], 14, RED, curve=False)
    if t >= A("b9", "Bunny-loo."):
        sign(cr, t, A("b9", "Bunny-loo."), 360, 600, "BUNNYLOO 1807", col=RED, size=76)
        sparkles(cr, t, A("b9", "Bunny-loo."), 360, 600, n=10, seed=8, col=GOLD, spread=200)
        rabbit(cr, t, 360, 900, 1.2, bowtie=True, eyes="happy", seed=1)
    vignette(cr, 0.3)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    sign(cr, t, A("b10"), 360, 180, "WHO WINS?", col=GOLD, size=80)
    sign(cr, t, A("b10", "Napoleon,"), 360, 420, "NAPOLEON", col=BLUE, size=72)
    sign(cr, t, A("b10", "bunnies?"), 360, 600, "1,000 BUNNIES", col=RED, size=72)
    vignette(cr, 0.3)


SCENES = {"hook": scene_hook, "party": scene_party, "cages": scene_cages, "tame": scene_tame, "charge": scene_charge,
          "run": scene_run, "carriage": scene_carriage, "loo": scene_loo, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("NAPOLEON VS", False), ("1,000 BUNNIES", True)], end=tl.at("b2"), y=170, size=96)
    captions(cr, t, tl)
