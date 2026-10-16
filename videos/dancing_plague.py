"""Funny history F3: "The Dancing Plague of 1518" -- reference narration style (talks to the viewer, "bro", modern
comparisons on old history).

Script: out/scripts_funny_history.md, F3 narration-style version (owner approved 15 Oct 2026). Strasbourg, July 1518:
one woman (Frau Troffea in later accounts) danced for days, others joined (dozens, later accounts say hundreds); the
council hired musicians and set up a stage; it got worse. Causes are still debated (stress and famine, mass
psychogenic illness, ergot), deaths disputed and left out. Turbo voice with tags (narrator only).
"""
import math

from motion import thriller as th
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, appear, bold_text, camera, captions, enter, lin, paint, rrect, sign,
                           soft_disc, stamp, stroke_line, vignette)
from motion.toons import person
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 0.9
SHIRTS = [hexc(c) for c in ("#d8453c", "#3b7dd8", "#2f9a5a", "#e8a23a", "#8a5bd0", "#d85a9a", "#3aa8a8")]

SCRIPT = [
    dict(id="b1", scene="hook", text="[Fifteen eighteen.|1518.] A woman walks into the street in Strasbourg. Starts "
                                     "dancing. And just doesn't stop."),
    dict(id="b2", scene="days", text="One day. Two days. Bro, her legs had more stamina than my phone battery. "
                                     "[chuckle]"),
    dict(id="b3", scene="crowd", text="Then people start joining. Within weeks, dozens of people dancing. Nonstop."),
    dict(id="b4", scene="council", text="So the city leaders sit down. Serious faces. Big meeting. And they come up "
                                        "with a plan."),
    dict(id="b5", scene="council", text="More music.", gap=0.45),
    dict(id="b6", scene="stage", gap=0.5, text="They hire musicians. They build a stage. Because obviously, the cure for too "
                                      "much dancing is a dance floor. [laugh]"),
    dict(id="b7", scene="worse", text="And you know what happened next? It got worse. Way worse."),
    dict(id="b8", scene="why", text="To this day, nobody knows exactly why. Stress, hunger, fear. Or something else."),
    dict(id="b9", scene="end", text="If one song could make you dance for days, which song would it be?", gap=0.3),
]

METADATA = dict(
    title="She Couldn't Stop Dancing. For Days. 💃",
    alt_titles=["The Dancing Plague of 1518 💃", "The Cure for Too Much Dancing? More Music. 🎻"],
    description="""1518, Strasbourg. A woman walks into the street, starts dancing... and just doesn't stop. 💃

Days later, others join her. Within weeks, dozens of people are dancing nonstop. The city leaders' genius plan? More music. They hired musicians and built a stage. It got worse. 😂

To this day, nobody knows exactly why it happened: stress, hunger, fear, or something else.

(The Dancing Plague of 1518, recorded in Strasbourg's city records. Numbers vary between accounts.)

💬 If one song could make you dance for days, which song would it be? 👇

🔔 Interestingly Strange: funny history, clever twists and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#FunnyHistory", "#History", "#Shorts"],
    tags=["dancing plague", "dancing plague of 1518", "strasbourg 1518", "funny history", "weird history",
          "history facts", "medieval history", "dancing mania", "strange history", "interestingly strange"],
    pinned_comment="Mine would be the song that's been stuck in my head all week 🎵 Yours? 👇",
)


def dancer(cr, t, x, y, s, k=0, tired=0.0, who="villager", **kw):
    kw.setdefault("shirt", SHIRTS[k % len(SHIRTS)])
    """Someone dancing: arms swap up and out, body sways. `tired` 0..1 slows it and adds sweat."""
    sp = lerp(6.0, 3.5, tired)
    ph = t * sp + k * 1.7
    up = math.sin(ph) > 0
    arms = ("up", "wave") if up else ("wave", "out")
    cr.save()
    cr.translate(x, y - abs(math.sin(ph)) * 18 * s)
    person(cr, t, 0, 0, s, who, facing=1 if (k % 2) else -1, eyes="half" if tired > 0.5 else "happy",
           mouth="o" if tired > 0.5 else "grin", arms=arms, tilt=0.18 * math.sin(ph * 0.5), walk=ph,
           sweat=tired > 0.3, seed=k, **kw)
    cr.restore()


def woman(cr, t, x, y, s, tired=0.0):
    dancer(cr, t, x, y, s, k=3, tired=tired, who="mother", shirt=hexc("#d8453c"), hair_col=hexc("#a8582a"))


def street(cr, t, dark=0.0):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#ffd9a8")), (0.55, hexc("#fff0d8")), (0.56, hexc("#b8a088")),
                                   (1, hexc("#8a7a66"))]))
    cr.fill()
    for k, (x, w, h, col) in enumerate([(-20, 200, 520, "#f0e0c0"), (180, 180, 600, "#e8cfa8"),
                                        (360, 200, 560, "#f4e4c8"), (560, 200, 500, "#e0c8a0")]):
        top = 700 - h
        rrect(cr, x, top, w, h, 0)                                 # half-timbered houses
        paint(cr, hexc(col), OUTLINE, 6)
        cr.move_to(x - 10, top)
        cr.line_to(x + w / 2, top - 120)
        cr.line_to(x + w + 10, top)
        cr.close_path()
        paint(cr, hexc("#a8452a"), OUTLINE, 6)
        for yy in range(int(top) + 90, 690, 130):
            stroke_line(cr, [(x, yy), (x + w, yy)], 9, hexc("#5a3a22"), curve=False)
        stroke_line(cr, [(x, top), (x + w, top + 120)], 8, hexc("#5a3a22"), curve=False)
        rrect(cr, x + w / 2 - 30, top + 150, 60, 70, 8)
        paint(cr, hexc("#7ab0d8"), OUTLINE, 4)
    if dark:
        cr.rectangle(0, 0, W, H)
        cr.set_source_rgba(0.05, 0.05, 0.15, 0.55 * dark)
        cr.fill()


def battery(cr, x, y, level, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -70, -36, 140, 72, 12)
    paint(cr, WHITE, OUTLINE, 6)
    rrect(cr, 70, -14, 12, 28, 4)
    paint(cr, OUTLINE, None)
    col = GREEN if level > 0.5 else (GOLD if level > 0.2 else RED)
    rrect(cr, -62, -28, max(4, 124 * level), 56, 8)
    paint(cr, col, None)
    cr.restore()


def scene_hook(cr, t, tl):
    A = tl.at
    street(cr, t)
    cr.save()
    enter(cr, camera(t, [(0.0, (1.15, 360, 760)), (A("b1", "stop."), (1.4, 360, 820))], dur=0.6))
    for k, x in enumerate((150, 570)):                               # onlookers staring
        person(cr, t, x, 1000, 0.6, "villager" if k else "barber", facing=1 if k == 0 else -1, eyes="wide",
               mouth="o", arms=("chin", "down"), seed=k, shirt=SHIRTS[k + 4])
    woman(cr, t, 360, 1060, 0.95)
    cr.restore()
    sign(cr, t, A("b1", "Strasbourg."), 360, 360, "STRASBOURG, 1518", col=PURPLE, size=54,
         end=A("b1", "doesn't") - 0.05)
    if t >= A("b1", "stop."):
        stamp(cr, t, A("b1", "stop."), 360, 420, "NONSTOP", col=RED, size=80)
    vignette(cr, 0.3)


def scene_days(cr, t, tl):
    A = tl.at
    night = 0.5 + 0.5 * math.sin(t * 2.4)
    street(cr, t, dark=night * 0.8)
    day = 2 if t >= A("b2", "Two") else 1
    sign(cr, t, A("b2"), 360, 200, f"DAY {day}", col=BLUE, size=72)
    woman(cr, t, 250, 1040, 0.85, tired=0.2 if day == 1 else 0.45)
    if t >= A("b2", "phone"):
        k = appear(t, A("b2", "phone"), 0.3)
        rrect(cr, 450, 480, 200, 360, 30)                         # the phone, battery draining
        paint(cr, hexc("#2b2b33"), OUTLINE, 6)
        level = lerp(0.6, 0.03, seg(t, A("b2", "phone"), A("b2", "battery.", end=True) + 0.4))
        battery(cr, 550, 640, level, 0.9 * k)
        bold_text(cr, f"{int(level * 100)}%", 550, 760, 44, WHITE, ow=5)
        sign(cr, t, A("b2", "stamina"), 250, 420, "LEGS: 100%", col=GREEN, size=48)
    vignette(cr, 0.35)


def scene_crowd(cr, t, tl):
    A = tl.at
    street(cr, t)
    n = 1 + int(14 * ease_out(seg(t, A("b3", "joining."), A("b3", "dancing.", end=True))))
    spots = [(360, 1060), (170, 1000), (550, 1000), (260, 920), (460, 920), (90, 1090), (630, 1090), (360, 860),
             (160, 840), (560, 840), (250, 1120), (470, 1120), (60, 900), (660, 900), (360, 980)]
    for k, (x, y) in sorted(list(enumerate(spots[:n])), key=lambda e: e[1][1]):
        if k == 0:
            woman(cr, t, x, y, 0.62, tired=0.5)
        else:
            dancer(cr, t, x, y, 0.5 + 0.0003 * y, k=k, who="villager" if k % 3 else "barber")
    count = {True: "DOZENS", False: f"{n}"}[t >= A("b3", "dozens")]
    sign(cr, t, A("b3", "joining."), 360, 220, count, col=GOLD, size=78)
    if t >= A("b3", "Nonstop."):
        stamp(cr, t, A("b3", "Nonstop."), 360, 400, "NONSTOP", col=RED, size=70)
    vignette(cr, 0.3)


def council_table(cr, t, tl, facepalm=False):
    rrect(cr, 0, 0, W, H, 0)
    paint(cr, lin(0, 0, 0, H, [(0, hexc("#6a4a32")), (1, hexc("#3a2818"))]), None)
    for k, x in enumerate((150, 360, 570)):
        person(cr, t, x, 980, 0.72, ("judge", "aquinas", "villager")[k], eyes="half", mouth="flat", brows="angry",
               arms=("face", "down") if facepalm else ("cross", "down"), seed=k + 2,
               shirt=hexc(("#2a2a3a", "#4a2a2a", "#2a3a4a")[k]))
    rrect(cr, 40, 860, 640, 60, 10)                                # the long table
    paint(cr, hexc("#8a5a32"), OUTLINE, 7)
    rrect(cr, 60, 920, 600, 240, 0)
    paint(cr, hexc("#6a4224"), OUTLINE, 7)


def scene_council(cr, t, tl):
    A = tl.at
    council_table(cr, t, tl)
    sign(cr, t, A("b4", "Serious"), 360, 200, "SERIOUS FACES", col=BLUE, size=54, end=A("b4", "Big") - 0.05)
    sign(cr, t, A("b4", "Big"), 360, 200, "BIG MEETING", col=PURPLE, size=60, end=A("b4", "plan.") - 0.05)
    sign(cr, t, A("b4", "plan."), 360, 200, "THE PLAN:", col=GOLD, size=66, end=A("b5") - 0.05)
    if t >= A("b5"):
        k = appear(t, A("b5"), 0.25)
        cr.save()
        cr.translate(360, 420)
        cr.scale(k, k)
        rrect(cr, -290, -110, 580, 220, 30)
        paint(cr, WHITE, OUTLINE, 8)
        bold_text(cr, "MORE MUSIC.", 0, 30, 92, RED)
        cr.restore()
        cue("hit", t, A("b5"))
    vignette(cr, 0.4)


def musician(cr, t, x, y, s, k, inst):
    def drum(c, hx, hy):
        c.arc(hx, hy + 30, 44, 0, 2 * math.pi)
        paint(c, hexc("#d8453c"), OUTLINE, 5)

    def fiddle(c, hx, hy):
        c.save()
        c.translate(hx, hy - 10)
        c.rotate(-0.6)
        c.scale(1, 1.6)
        c.arc(0, 0, 24, 0, 2 * math.pi)
        paint(c, hexc("#b0702a"), OUTLINE, 5)
        c.restore()
    person(cr, t, x, y, s, "seller" if k % 2 else "villager", eyes="happy", mouth="grin", arms=("hold", "down"),
           hold=drum if inst == "drum" else fiddle, seed=k + 5, shirt=SHIRTS[(k + 2) % len(SHIRTS)])


def scene_stage(cr, t, tl):
    A = tl.at
    street(cr, t)
    built = seg(t, A("b6", "stage."), A("b6", "stage.", end=True) + 0.3)
    if built > 0:                                                  # the stage rises
        h = 160 * ease_out(built)
        rrect(cr, 60, 820 - h + 160, 600, h, 6)
        paint(cr, hexc("#a8713e"), OUTLINE, 7)
        for k in range(5):
            soft_disc(cr, 120 + k * 120, 640, 70, (1, 0.9, 0.4, 0.35 * built * (0.6 + 0.4 * math.sin(t * 6 + k))))
    if t >= A("b6", "musicians."):
        for k, (x, inst) in enumerate(((150, "drum"), (360, "fiddle"), (570, "drum"))):
            if t >= A("b6", "musicians.") + 0.15 * k:
                musician(cr, t, x, 820, 0.55, k, inst)
    if t >= A("b6", "obviously,"):
        for k, x in enumerate((140, 300, 450, 600)):
            dancer(cr, t, x, 1150, 0.55, k=k + 1)
        sign(cr, t, A("b6", "obviously,"), 360, 230, "CURE FOR DANCING:", col=BLUE, size=50)
    if t >= A("b6", "floor."):
        stamp(cr, t, A("b6", "floor."), 360, 400, "A DANCE FLOOR", col=PURPLE, size=64)
        sparkles(cr, t, A("b6", "floor."), 360, 500, n=10, seed=6, col=GOLD, spread=260)
    vignette(cr, 0.3)


def scene_worse(cr, t, tl):
    A = tl.at
    if t < A("b7", "worse."):
        street(cr, t)
        for k in range(8):
            dancer(cr, t, 70 + k * 85, 1000 + (k % 2) * 80, 0.48, k=k)
        sign(cr, t, A("b7"), 360, 230, "WHAT HAPPENED NEXT?", col=BLUE, size=50)
    else:
        council_table(cr, t, tl, facepalm=True)
        rows = 1 if t < A("b7", "Way") else 2
        for r in range(rows):
            for k in range(6):
                dancer(cr, t, 70 + k * 116, 420 + r * 190, 0.36, k=k + r * 6)
        stamp(cr, t, A("b7", "worse."), 360, 200, "WORSE", col=RED, size=72)
        if rows == 2:
            stamp(cr, t, A("b7", "Way"), 360, 300, "WAY WORSE", col=RED, size=64, rot=0.08)
    vignette(cr, 0.35)


def scene_why(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cfe4ff"), hexc("#fff6e8"), seed=5)
    sign(cr, t, A("b8"), 360, 200, "WHY? NOBODY KNOWS", col=PURPLE, size=56)
    for k, (key, word, col) in enumerate((("Stress,", "STRESS", BLUE), ("hunger,", "HUNGER", GOLD),
                                          ("fear.", "FEAR", RED))):
        if t >= A("b8", key):
            sign(cr, t, A("b8", key), 360, 420 + k * 150, word, col=col, size=60)
    if t >= A("b8", "something"):
        bold_text(cr, "???", 360, 950, 120, hexc("#2b1d16"), outline=None, shadow=0)
    vignette(cr, 0.3)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd0e8"), hexc("#fff1d6"), seed=9)
    sign(cr, t, A("b9"), 360, 200, "YOUR SONG?", col=GOLD, size=70)
    woman(cr, t, 360, 1000, 0.9)
    for k in range(3):                                             # music notes floating up
        y = 700 - ((t * 120 + k * 140) % 400)
        bold_text(cr, "♪", 170 + k * 190, y, 80, PURPLE, ow=5)
    vignette(cr, 0.3)


SCENES = {"hook": scene_hook, "days": scene_days, "crowd": scene_crowd, "council": scene_council,
          "stage": scene_stage, "worse": scene_worse, "why": scene_why, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("SHE COULDN'T", False), ("STOP DANCING", True)], end=tl.at("b1", "Starts"), y=170, size=96)
    captions(cr, t, tl)
