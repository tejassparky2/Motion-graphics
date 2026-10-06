"""Researchers found: "The Spotlight Effect" (Gilovich, Medvec & Savitsky, Cornell, J. Pers. Soc. Psych. 2000).

Students wore a Barry Manilow T-shirt (chosen because it embarrassed college students) into a room of other students,
then guessed how many had noticed it. They guessed about half; only about a quarter (about 23%) actually had.
Structure follows the owner's "Napoleon was once asked" reference: a question hook, a simple model, the answer step by
step, an everyday takeaway, and "So what do you think?" at the end. The singer is shown only as his name on the shirt.
"""
import math

from motion.captions import captions
from motion.characters import CAST, bubble, person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    write
from motion.kit import camera, hl, stamp, whip

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="s1", scene="hook", text="You walk into a room of strangers, wearing the most embarrassing T-shirt in the "
                                     "world. How many people notice?"),
    dict(id="s2", scene="lab", text="In the year [two thousand,|2000,] researchers at Cornell University tested exactly "
                                    "that."),
    dict(id="s3", scene="lab", text="They made students wear a T-shirt with a giant picture of the singer Barry Manilow. "
                                    "For college students back then, that was very uncool."),
    dict(id="s4", scene="room", text="Each student walked into a room full of other students. Then walked straight back "
                                     "out."),
    dict(id="s5", scene="guess", text="Then they guessed how many people had noticed the shirt. Their guess? About half "
                                      "the room."),
    dict(id="s6", scene="guess", text="The real answer? Only about one in four.", gap=0.3),
    dict(id="s7", scene="guess", text="Half the people they were worried about never even saw it."),
    dict(id="s8", scene="name", text="Scientists call it the spotlight effect. You feel like everyone is watching you. "
                                     "But everyone else is busy worrying about themselves."),
    dict(id="s9", scene="end", text="So what do you think? What's one thing you were embarrassed about, that nobody "
                                    "even noticed?", pace=0.95),
]

METADATA = dict(
    title="Nobody Is Watching You as Much as You Think (Science Proved It) 👀",
    alt_titles=["The Embarrassing T-Shirt Experiment 😳", "Why You Feel Like Everyone Is Staring (The Spotlight Effect)"],
    description="""You walk into a room wearing the most embarrassing T-shirt in the world. How many people notice? 😳

In 2000, researchers at Cornell University tested it. Students wore a T-shirt with a giant picture of singer Barry Manilow, walked into a room of other students, and walked out. They guessed about half the room had noticed the shirt. The real answer: only about one in four. 👀

Psychologists call it the spotlight effect: we feel like everyone is watching us, but everyone else is busy worrying about themselves.

Study: Gilovich, Medvec & Savitsky (2000), "The Spotlight Effect in Social Judgment", Journal of Personality and Social Psychology.

💬 So what do you think? What's one thing you were embarrassed about that nobody even noticed? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Psychology", "#SpotlightEffect", "#Science"],
    tags=["spotlight effect", "psychology experiment", "social anxiety", "embarrassing", "cornell study",
          "psychology facts", "researchers found", "brain facts", "self confidence", "interestingly strange"],
    pinned_comment="Be honest: what's the most embarrassing thing you thought EVERYONE saw? 😂👇",
)

WALL, FLOOR = hexc("#f3e6cf"), hexc("#c99a6b")
GOLD = hexc("#ffd23f")
GREEN = hexc("#2e9e52")
BLUE = hexc("#3f6fb5")
SHIRT_BG = hexc("#f4efe1")
WALKER = "sam"
# the room: 8 students in two rows (back row smaller, higher)
CROWD = [("kid_a", 340, 810, 0.9), ("mia", 445, 810, 0.9), ("kid_b", 550, 810, 0.9), ("rocker_a", 655, 810, 0.9),
         ("kid_c", 300, 930, 1.05), ("rocker_b", 410, 930, 1.05), ("kid_d", 520, 930, 1.05), ("seth", 630, 930, 1.05)]
BASE = (1.25, 390, 700)    # the whole room, framed close enough to read faces on a phone
WX, WY = 170, 930          # where the walker stands, apart from the crowd, by the door


def bg(cr, t, keys, color=WALL, dur=0.3):
    cr.set_source_rgba(*color)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=dur)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)


def room(cr, board=True):
    cr.set_source_rgba(*WALL)
    cr.rectangle(-600, -400, 2000, 1500)
    cr.fill()
    shape(cr, [(-600, 1050), (1400, 1050), (1400, 2200), (-600, 2200)], FLOOR, seed=10, amp=0.5, lw=4)
    shape(cr, rrect_pts(20, 600, 110, 330, 8, 12), hexc("#9c6b43"), seed=11, amp=0.4, lw=4)    # door
    if board:
        shape(cr, rrect_pts(380, 420, 230, 110, 8, 12), hexc("#2f5d4a"), seed=12, amp=0.4, lw=4)
        write(cr, [("PSYCH 101", WHITE)], 495, 488, 32, align="center", bold=True)


def tshirt_print(cr, x, y, s, who=WALKER):
    """The embarrassing print on the walker's chest: a cartoon portrait and the singer's name."""
    bh = CAST[who]["bh"]
    with at(cr, x, y + (-26 - bh * 0.52) * s, s):
        shape(cr, rrect_pts(-30, -30, 60, 56, 6, 8), SHIRT_BG, seed=20, amp=0.2, lw=2)
        blob(cr, 0, -8, 13, 15, hexc("#e8b48a"), seed=21, amp=0.3, lw=1.5)
        blob(cr, 0, -20, 16, 8, hexc("#c9a227"), seed=22, amp=0.4, lw=1.5)        # big hair
        write(cr, [("BARRY", RED)], 0, 20, 12, align="center", bold=True)


def big_shirt(cr, x, y, s):
    """The T-shirt on its own, held up for the reveal."""
    with at(cr, x, y, s):
        shape(cr, [(-150, -150), (-60, -170), (60, -170), (150, -150), (210, -70), (150, -30), (150, 170),
                   (-150, 170), (-150, -30), (-210, -70)], WHITE, seed=30, amp=0.6, lw=5)
        blob(cr, 0, -40, 60, 70, hexc("#e8b48a"), seed=31, amp=0.6, lw=4)
        blob(cr, 0, -100, 78, 36, hexc("#c9a227"), seed=32, amp=0.8, lw=4)
        for ex in (-22, 22):
            blob(cr, ex, -48, 6, 7, INK, seed=33 + ex, amp=0.1, lw=0, stroke=None)
        line(cr, [(-22, -8), (0, 4), (22, -8)], 4, INK, seed=35, amp=0.2)
        write(cr, [("BARRY MANILOW", RED)], 0, 120, 34, align="center", bold=True)


def crowd(cr, t, look=None, glow=None, think=None):
    """look: index set facing/looking at the walker (others look at each other). glow: {index: colour}."""
    look, glow = look or set(), glow or {}
    for k, (who, x, y, s) in enumerate(CROWD):
        if k in glow:
            blob(cr, x, y - 120 * s, 70 * s, 110 * s, glow[k], seed=40 + k, amp=0.5, lw=0, stroke=None)
        facing = -1 if k in look else (1 if k % 2 else -1)
        person(cr, who, x, y, t, facing=facing, eyes="wide" if k in look else "dot",
               mouth="o" if k in look else "smile", scale=s)
        if think and k in think:
            bubble(cr, min(max(x, 250), 560), y - 250 * s, 170, 60, (x, y - 200 * s), [(think[k], INK)], s=0.9,
                   size=26, thought=True)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, BASE), (A("s1", "embarrassing"), (1.8, 200, 760)), (A("s1", "how"), BASE)]
    bg(cr, t, keys)
    room(cr)
    # in his head: every single person stares, and a spotlight burns on him
    a = 0.35 + 0.1 * math.sin(t * 6)
    cr.move_to(WX + 20, 420)
    cr.line_to(WX - 90, 960)
    cr.line_to(WX + 90, 960)
    cr.close_path()
    cr.set_source_rgba(*hexc("#fff3a0", a))
    cr.fill()
    crowd(cr, t, look=set(range(8)))
    person(cr, WALKER, WX, WY, t, facing=1, arms=("face", "down"), eyes="wide", mouth="o", sweat=True, scale=1.1,
           shake=1.0)
    tshirt_print(cr, WX, WY, 1.1)
    hl(cr, t, [("EVERYONE", RED), (" is staring?", INK)], 215, 66, 0.0, bold=True, sound=False)


def scene_lab(cr, t, tl):
    A = tl.at
    keys = [(A("s2") - 0.2, (1.0, 360, 640)), (A("s3", "giant"), (1.2, 360, 600)), (A("s3", "uncool."), (1.0, 360, 640))]
    bg(cr, t, keys, color=hexc("#dfe9f2"))
    if t < A("s3"):
        with at(cr, 360, 560, max(0.85, pop(t, A("s2"), 0.3)), rot=-0.03):
            shape(cr, rrect_pts(-250, -100, 500, 200, 18, 14), hexc("#fdf6e3"), seed=50, amp=0.5, lw=5)
            write(cr, [("CORNELL UNIVERSITY", hexc("#b31b1b"))], 0, -16, 44, align="center", bold=True)
            write(cr, [("2000", INK)], 0, 56, 60, align="center", bold=True)
        hl(cr, t, [("researchers ", INK), ("tested it", BLUE)], 215, 66, A("s2", "researchers"), bold=True)
    else:
        big_shirt(cr, 360, 600, max(0.6, pop(t, A("s3"), 0.3)))
        if t >= A("s3", "uncool."):
            stamp(cr, t, A("s3", "uncool."), "VERY UNCOOL", dur=0.9, y=330)
        hl(cr, t, [("the ", INK), ("EMBARRASSING", RED), (" shirt", INK)], 215, 60, A("s3"),
           end=A("s3", "uncool.") - 0.05, bold=True)


def scene_room(cr, t, tl):
    A = tl.at
    keys = [(A("s4") - 0.2, BASE)]
    bg(cr, t, keys)
    room(cr)
    crowd(cr, t, look={1, 6})
    # walks in from the door, turns round, walks back out
    t0, t1 = A("s4", "walked"), A("s4", "out.", end=True)
    u = seg(t, t0, t1)
    x = 75 + 140 * math.sin(math.pi * u)
    facing = 1 if u < 0.5 else -1
    person(cr, WALKER, x, WY, t, facing=facing, walk=(t - t0) * 1.6, eyes="dot", mouth="flat", scale=1.1)
    tshirt_print(cr, x, WY, 1.1)
    hl(cr, t, [("walk in... ", INK), ("walk out", BLUE)], 215, 66, A("s4"), bold=True)


def scene_guess(cr, t, tl):
    A = tl.at
    keys = [(A("s5") - 0.2, BASE), (A("s6"), BASE), (A("s7"), (1.3, 420, 700))]
    bg(cr, t, keys)
    room(cr, board=False)
    person(cr, WALKER, WX, WY, t, facing=1, arms=("chin", "down"), eyes="dot", mouth="flat", scale=1.1)
    tshirt_print(cr, WX, WY, 1.1)
    guess, real = {0, 2, 5, 7}, {2, 7}
    glow = {}
    if A("s5", "half") <= t < A("s6", "only"):
        glow = {k: hexc("#ffd23f", 0.6) for k in guess}
    elif t >= A("s6", "only"):
        glow = {k: hexc("#2e9e52", 0.55) for k in real}
        if t >= A("s7"):
            glow.update({k: hexc("#e0483d", 0.35) for k in guess - real})
    crowd(cr, t, look=real if t >= A("s6", "only") else set(), glow=glow)
    # the scoreboard
    if t >= A("s5", "half"):
        with at(cr, 280, 520, max(0.85, pop(t, A("s5", "half"), 0.25)) * 0.85):
            shape(cr, rrect_pts(-150, -55, 300, 110, 18, 12), hexc("#2b2d3a"), seed=60, amp=0.3, lw=0, stroke=None)
            write(cr, [("THEY GUESSED", WHITE)], 0, -12, 26, align="center", bold=True)
            write(cr, [("HALF", GOLD)], 0, 36, 46, align="center", bold=True)
    if t >= A("s6", "only"):
        with at(cr, 530, 520, max(0.85, pop(t, A("s6", "only"), 0.25)) * 0.85):
            shape(cr, rrect_pts(-150, -55, 300, 110, 18, 12), hexc("#2b2d3a"), seed=61, amp=0.3, lw=0, stroke=None)
            write(cr, [("REALITY", WHITE)], 0, -12, 26, align="center", bold=True)
            write(cr, [("1 IN 4", hexc("#7ee08a"))], 0, 36, 46, align="center", bold=True)
        cue("hit", t, A("s6", "only"))
    hl(cr, t, [("how many ", INK), ("noticed", RED), ("?", INK)], 215, 66, A("s5"), end=A("s6") - 0.05, bold=True)
    hl(cr, t, [("only ", INK), ("1 IN 4", GREEN)], 215, 72, A("s6"), end=A("s7") - 0.05, bold=True)
    hl(cr, t, [("half ", INK), ("NEVER", RED), (" saw it", INK)], 215, 70, A("s7"), bold=True, underline=True)


def scene_name(cr, t, tl):
    A = tl.at
    keys = [(A("s8") - 0.2, BASE), (A("s8", "busy"), (1.2, 420, 690))]
    bg(cr, t, keys)
    room(cr, board=False)
    worries = {0: "my hair...", 3: "am I late?", 6: "did I say that?"}
    person(cr, WALKER, WX, WY, t, facing=1, arms=("hip", "hip"), eyes="happy", mouth="grin", scale=1.1)
    crowd(cr, t, think=worries if t >= A("s8", "busy") else None)
    if t < A("s8", "busy"):
        with at(cr, 400, 520, max(0.85, pop(t, A("s8", "spotlight"), 0.3)) * 0.85, rot=-0.03):
            shape(cr, rrect_pts(-250, -90, 500, 180, 18, 14), hexc("#fdf6e3"), seed=70, amp=0.5, lw=5)
            write(cr, [("THE SPOTLIGHT", INK)], 0, -14, 52, align="center", bold=True)
            write(cr, [("EFFECT", RED)], 0, 56, 66, align="center", bold=True)
    hl(cr, t, [("everyone is ", INK), ("busy", BLUE), (" with themselves", INK)], 215, 42, A("s8", "busy"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("s9") - 0.2, BASE), (A("s9", "embarrassed"), (1.7, 230, 760))]
    bg(cr, t, keys)
    room(cr)
    crowd(cr, t)
    person(cr, WALKER, WX, WY, t, facing=1, arms=("thumb", "hip"), eyes="happy", mouth="grin", scale=1.1)
    tshirt_print(cr, WX, WY, 1.1)
    hl(cr, t, [("what did ", INK), ("NOBODY", RED), (" notice?", INK)], 215, 60, A("s9"), bold=True, underline=True)
    stamp(cr, t, A("s9", "noticed?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "lab": scene_lab, "room": scene_room, "guess": scene_guess, "name": scene_name,
     "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
