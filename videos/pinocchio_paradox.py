"""Paradox: "The Pinocchio Paradox" — "My nose is about to grow." True or a lie?

Proposed in 2001 (Veronique Eldridge-Smith) as a version of the liar paradox ("This sentence is false"), one of the
oldest puzzles in logic. The puppet is our own design (Collodi's 1883 character is public domain; nothing taken from
any film version).
Structure copies what worked on The Infinite Hotel: impossible premise, a character line, step-by-step logic, the
twist, who came up with it, then an open question for the comments.
"""
import math

from motion.captions import captions
from motion.characters import bubble
from motion.engine import INK, RED, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="p1", scene="shop", text="Pinocchio has one rule. When he lies, his nose grows. When he tells the truth, "
                                     "it stays the same."),
    dict(id="p2", scene="shop", text="One day, he says this.", gap=0.3),
    dict(id="p3", scene="shop", text="My nose is about to grow.", speaker="pino", pace=0.88),
    dict(id="p4", scene="logic", text="Let's test it. What if he's telling the truth? Then his nose must grow. But "
                                      "noses only grow for lies. So it can't be the truth.", pace=0.95),
    dict(id="p5", scene="logic", text="What if he's lying? Then the opposite is true. His nose won't grow. But a lie "
                                      "always makes it grow. So it can't be a lie, either.", pace=0.95),
    dict(id="p6", scene="spin", text="True breaks the rule. A lie breaks the rule. No answer works."),
    dict(id="p7", scene="sign", text="It's called the Pinocchio paradox. A philosopher came up with it in "
                                     "[two thousand one.|2001.] It's a new version of a puzzle that's over "
                                     "[two thousand years|2,000 years] old: this sentence is false."),
    dict(id="p8", scene="end", text="So... does his nose grow?", pace=0.95),
]

METADATA = dict(
    title="Pinocchio Said ONE Sentence… and Broke Logic 🤥🤯",
    alt_titles=["The Sentence That Breaks Pinocchio's Nose 🤥", "Does His Nose Grow? (Nobody Can Answer) 🤯"],
    description="""Pinocchio's nose grows every time he lies. So he says: "My nose is about to grow." 🤥

If it's true, his nose grows… but it only grows when he lies. If it's a lie, his nose has to grow… which makes it true. Every answer flips into the other one.

It's called the Pinocchio paradox, proposed in 2001 as a twist on the liar paradox ("this sentence is false"), one of the oldest puzzles in logic.

💬 So… does his nose grow? Yes or no 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Paradox", "#Pinocchio", "#MindBlown"],
    tags=["pinocchio paradox", "liar paradox", "paradox", "logic puzzle", "this sentence is false", "brain teaser",
          "mind blowing", "philosophy", "paradox explained", "interestingly strange"],
    pinned_comment="YES or NO: does his nose grow? 🤥 Explain your answer… if you can 😂👇",
)

WOOD, WOOD_D, WOOD_L = hexc("#e2b27a"), hexc("#b07a45"), hexc("#f3cf9c")
SHIRT, CAP = hexc("#3f8f8a"), hexc("#c0504d")
TRUE_C, LIE_C = hexc("#2e9e52"), hexc("#e0483d")
BLUE = hexc("#3f6fb5")
WALL = hexc("#f2dcb3")


def pino(cr, t, x, y, s, nose=1.0, mood="calm", talking=False, look=0.0, dizzy=False):
    """Our wooden puppet. `nose` = nose length multiplier (1 = normal)."""
    bob = math.sin(t * 2.4) * 3
    with at(cr, x, y + bob, s):
        # body
        shape(cr, rrect_pts(-62, 40, 124, 150, 26, 16), SHIRT, seed=501, amp=0.4, lw=4)
        for k in range(3):
            dot(cr, 0, 70 + k * 30, 6, hexc("#f2b632"))
        line(cr, [(-62, 70), (-100, 150)], 14, WOOD_D, seed=502, amp=0.3)
        line(cr, [(62, 70), (100, 150)], 14, WOOD_D, seed=503, amp=0.3)
        for jx in (-100, 100):
            blob(cr, jx, 152, 13, 13, WOOD, seed=504 + jx, amp=0.2, lw=3)
        # head
        blob(cr, 0, -30, 70, 72, WOOD, seed=510, amp=0.4, lw=4.5)
        for k in range(4):   # wood grain
            line(cr, [(-50 + k * 8, -80 + k * 30), (-20 + k * 10, -70 + k * 30)], 2.5, hexc("#c9925a", 0.6),
                 seed=511 + k, amp=0.5)
        blob(cr, -40, 0, 14, 9, hexc("#f08a8a", 0.7), seed=515, amp=0.2, lw=0, stroke=None)
        blob(cr, 40, 0, 14, 9, hexc("#f08a8a", 0.7), seed=516, amp=0.2, lw=0, stroke=None)
        # cap with a feather
        shape(cr, [(-74, -66), (-40, -112), (40, -116), (78, -66)], CAP, seed=520, amp=0.4, lw=4)
        line(cr, [(30, -112), (70, -150), (64, -120)], 5, hexc("#f2b632"), seed=521, amp=0.4)
        # eyes
        for side in (-1, 1):
            ex = side * 26
            if dizzy:
                for k in range(3):
                    a = t * 8 + k * 2
                    dot(cr, ex + math.cos(a) * (4 + k * 4), -38 + math.sin(a) * (4 + k * 4), 2.5, INK)
                continue
            if mood == "happy":
                line(cr, [(ex - 12, -36), (ex, -46), (ex + 12, -36)], 4, INK, seed=530 + side, amp=0.1)
                continue
            big = 1.3 if mood == "shock" else 1.0
            blob(cr, ex, -38, 15 * big, 18 * big, WHITE, seed=532 + side, amp=0.2, lw=3.5)
            dot(cr, ex + look * 6, -35, 7, INK)
            dot(cr, ex + look * 6 + 2.5, -39, 2, WHITE)
            if mood == "worried":
                line(cr, [(ex - 12 * side, -60), (ex + 10 * side, -66)], 4, INK, seed=534 + side, amp=0.1)
        # mouth
        if talking:
            blob(cr, 0, 26, 14, 6 + 9 * abs(math.sin(t * 22)), hexc("#7a2a24"), seed=540, amp=0.2, lw=3)
        elif mood in ("shock", "worried"):
            blob(cr, 0, 28, 10, 12, hexc("#7a2a24"), seed=541, amp=0.2, lw=3)
        else:
            line(cr, [(-18, 20), (0, 32), (18, 20)], 4, INK, seed=542, amp=0.1)
        # the nose: a wooden cone that grows to the right
        L = 46 * nose
        shape(cr, [(4, -24), (12 + L, -14), (4, -6)], WOOD_L, seed=550, amp=0.15, lw=4)
        dot(cr, 12 + L, -14, 5, WOOD_D)
        if nose > 2.2:   # a little leaf on a long nose
            blob(cr, 12 + L * 0.7, -28, 12, 6, hexc("#79b061"), seed=551, amp=0.3, lw=2.5)


def workshop(cr):
    cr.set_source_rgba(*WALL)
    cr.rectangle(-900, -900, 2600, 3200)
    cr.fill()
    for k in range(-6, 20):
        line(cr, [(-200 + k * 70, 300), (-200 + k * 70, 1000)], 2.5, hexc("#e2c897"), seed=600 + k, amp=0.5)
    sharp_shape(cr, [(-900, 1000), (1700, 990), (1700, 2200), (-900, 2200)], hexc("#a8774a"), seed=610, amp=0.6, lw=4)
    shape(cr, rrect_pts(470, 380, 200, 160, 10, 12), hexc("#bfe6ff"), seed=611, amp=0.5, lw=4)    # window
    line(cr, [(570, 380), (570, 540)], 4, INK, seed=612, amp=0.2)
    for k in range(3):    # tools on the wall
        line(cr, [(80 + k * 60, 400), (80 + k * 60, 520)], 6, hexc("#6d4524"), seed=620 + k, amp=0.3)
        blob(cr, 80 + k * 60, 392, 16, 10, hexc("#9aa3ad"), seed=625 + k, amp=0.3, lw=3)


def meter(cr, t, x, y, state, s=1.0):
    """A TRUE / LIE switch. state: 0 = TRUE, 1 = LIE, between = flipping."""
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-150, -46, 300, 92, 46, 16), hexc("#2b2d3a"), seed=700, amp=0.2, lw=4)
        kx = lerp(-80, 80, state)
        col = LIE_C if state > 0.5 else TRUE_C
        blob(cr, kx, 0, 66, 36, col, seed=701, amp=0.2, lw=3.5)
        write(cr, [("LIE" if state > 0.5 else "TRUE", WHITE)], kx, 14, 38, align="center", bold=True)


def scene_shop(cr, t, tl):
    A = tl.at
    keys = [(0, (1.6, 360, 700)), (A("p1", "nose"), (2.0, 420, 690)), (A("p1", "truth,"), (1.3, 380, 720)),
            (A("p2"), (1.0, 360, 760)), (A("p2", "says"), (1.6, 360, 700)),
            (A("p3"), (1.3, 400, 700)), (A("p3", "grow"), (1.9, 360, 690))]
    set_camera(camera(t, keys))
    enter_world(cr)
    workshop(cr)
    # the nose grows on "lies", then snaps back on "truth"
    lie_t = A("p1", "lies,")
    nose = 1.0 + 1.8 * ease_out(seg(t, lie_t, lie_t + 0.35)) * (1 - seg(t, A("p1", "truth,"), A("p1", "truth,") + 0.3))
    mood = "shock" if lie_t <= t < A("p1", "truth,") else ("worried" if t >= A("p3") else "calm")
    if A("p1", "truth,") <= t < A("p2"):
        mood = "happy"
    pino(cr, t, 330, 640, 1.6, nose, mood, talking=tl.speaking("pino", t), look=1 if t >= A("p3") else 0)
    if t >= A("p3"):
        with at(cr, 520, 360, max(0.85, pop(t, A("p3"), 0.25))):
            shape(cr, rrect_pts(-170, -70, 340, 140, 30, 14), WHITE, seed=710, amp=0.4, lw=4)
            shape(cr, [(-80, 66), (-120, 120), (-40, 66)], WHITE, seed=711, amp=0.3, lw=4)
            write(cr, [("\"My nose is", INK)], 0, -10, 40, align="center", bold=True)
            write(cr, [("about to ", INK), ("GROW", RED), (".\"", INK)], 0, 40, 40, align="center", bold=True)
    hl(cr, t, [("a ", INK), ("LIE", RED), (" = nose grows", INK)], 215, 64, 0.0, end=A("p1", "truth,") - 0.05,
       bold=True, sound=False)
    hl(cr, t, [("the ", INK), ("TRUTH", TRUE_C), (" = nose stays", INK)], 215, 60, A("p1", "truth,"),
       end=A("p2") - 0.05, bold=True)
    hl(cr, t, [("so he says ", INK), ("THIS", RED), (":", INK)], 215, 70, A("p2"), end=A("p3") - 0.05, bold=True)
    cue("pop", t, lie_t)
    cue("hit", t, A("p3", "grow"))


def card(cr, t, x, y, s, title, col, rows, cross_t):
    """A test card: a title, reasoning lines that appear one by one, and a big X when the test fails."""
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-200, -130, 400, 260, 20, 14), hexc("#fdf6e3"), seed=720, amp=0.4, lw=5)
        write(cr, [(title, col)], 0, -72, 48, align="center", bold=True)
        for k, (text, rcol, st) in enumerate(rows):
            if t >= st:
                write(cr, [(text, rcol)], 0, -6 + k * 56, 38, align="center", bold=True,
                      progress=ease_out(seg(t, st, st + 0.3)))
        if t >= cross_t:
            u = ease_out(seg(t, cross_t, cross_t + 0.2))
            line(cr, [(-170, -110), (lerp(-170, 170, u), lerp(-110, 110, u))], 16, hexc("#e0483d", 0.9), seed=730,
                 amp=0.3)
            if u > 0.5:
                line(cr, [(170, -110), (lerp(170, -170, u), lerp(-110, 110, u))], 16, hexc("#e0483d", 0.9),
                     seed=731, amp=0.3)


def scene_logic(cr, t, tl):
    A = tl.at
    keys = [(A("p4") - 0.2, (1.0, 360, 780)), (A("p4", "must"), (1.05, 360, 760)), (A("p4", "can't"), (1.0, 360, 780)),
            (A("p5", "won't"), (1.05, 360, 760)), (A("p5", "either."), (1.0, 360, 780))]
    set_camera(camera(t, keys))
    enter_world(cr)
    workshop(cr)
    truth = [("nose must grow", INK, A("p4", "must")), ("but that's a LIE", LIE_C, A("p4", "only"))]
    if t < A("p5"):
        card(cr, t, 360, 450, max(0.85, pop(t, A("p4", "what"), 0.3)) * 1.25, "TRUTH?", TRUE_C, truth, A("p4", "can't"))
    else:
        u = ease_out(seg(t, A("p5"), A("p5") + 0.35))   # test 1 shrinks to a reminder on the left
        card(cr, t, lerp(360, 120, u), lerp(450, 700, u), lerp(1.25, 0.42, u), "TRUTH?", TRUE_C, truth,
             A("p4", "can't"))
        if u >= 1:
            card(cr, t, 360, 450, max(0.85, pop(t, A("p5") + 0.3, 0.3)) * 1.25, "LIE?", LIE_C,
                 [("nose won't grow", INK, A("p5", "won't")), ("but lies GROW it", LIE_C, A("p5", "always"))],
                 A("p5", "either."))
    # the nose acts out each step
    nose = 1.0
    if A("p4", "must") <= t < A("p4", "can't"):
        nose = 1.0 + 1.4 * ease_out(seg(t, A("p4", "must"), A("p4", "must") + 0.3))
    elif A("p5", "always") <= t < A("p5", "either."):
        nose = 1.0 + 1.4 * ease_out(seg(t, A("p5", "always"), A("p5", "always") + 0.3))
    pino(cr, t, 360, 760, 1.0, nose, "worried" if t < A("p5") else "shock", look=-0.5)
    cue("hit", t, A("p4", "can't"))
    cue("hit", t, A("p5", "either."))
    hl(cr, t, [("test 1: is it ", INK), ("TRUE", TRUE_C), ("?", INK)], 215, 62, A("p4", "what"),
       end=A("p5") - 0.05, bold=True)
    hl(cr, t, [("test 2: is it a ", INK), ("LIE", LIE_C), ("?", INK)], 215, 62, A("p5"), bold=True)


def scene_spin(cr, t, tl):
    A = tl.at
    keys = [(A("p6") - 0.2, (1.0, 360, 690)), (A("p6", "true"), (1.1, 360, 690)), (A("p6", "lie"), (1.0, 360, 690)),
            (A("p6", "answer"), (1.1, 360, 690))]
    set_camera(camera(t, keys))
    enter_world(cr)
    workshop(cr)
    f = (t - A("p6")) * 5.0          # faster and faster
    state = (math.sin(f * (1 + 0.5 * (t - A("p6")))) + 1) / 2
    meter(cr, t, 360, 330, 1.0 if state > 0.5 else 0.0)
    nose = 1.0 + 1.6 * (1 if state > 0.5 else 0)
    pino(cr, t, 330, 680, 1.35, nose, "shock", dizzy=t >= A("p6", "answer"))
    for k in range(2):   # the loop arrows
        a0 = t * 4 + k * math.pi
        cr.save()
        cr.translate(360, 330)
        cr.arc(0, 0, 180, a0, a0 + 2.2)
        cr.restore()
        cr.set_source_rgba(*(TRUE_C if k else LIE_C))
        cr.set_line_width(8)
        cr.stroke()
    if int(f) != int(f - 5.0 / 30):
        cue("pop", t, t)
    hl(cr, t, [("TRUE", TRUE_C), (": breaks the rule", INK)], 215, 60, A("p6"), end=A("p6", "lie") - 0.05, bold=True)
    hl(cr, t, [("LIE", LIE_C), (": breaks the rule", INK)], 215, 60, A("p6", "lie"), end=A("p6", "answer") - 0.05,
       bold=True)
    hl(cr, t, [("NO", RED), (" answer works", INK)], 215, 70, A("p6", "answer"), bold=True, underline=True)


def scene_sign(cr, t, tl):
    A = tl.at
    keys = [(A("p7") - 0.2, (1.1, 360, 700)), (A("p7", "pinocchio"), (1.5, 360, 520)), (A("p7", "2001."), (1.3, 360, 600)),
            (A("p7", "puzzle"), (1.0, 360, 720)), (A("p7", "sentence"), (1.3, 360, 760))]
    set_camera(camera(t, keys))
    enter_world(cr)
    workshop(cr)
    with at(cr, 360, 520, max(0.85, pop(t, A("p7", "pinocchio"), 0.3)), rot=-0.03):
        shape(cr, rrect_pts(-260, -90, 520, 180, 18, 14), hexc("#fdf6e3"), seed=800, amp=0.5, lw=5)
        write(cr, [("THE PINOCCHIO", INK)], 0, -14, 52, align="center", bold=True)
        write(cr, [("PARADOX", RED)], 0, 52, 62, align="center", bold=True)
    if t >= A("p7", "2001."):
        with at(cr, 590, 380, max(0.85, pop(t, A("p7", "2001."), 0.25)), rot=0.1):
            blob(cr, 0, 0, 72, 46, hexc("#f2b632"), seed=801, amp=0.5, lw=4)
            write(cr, [("2001", INK)], 0, 14, 40, align="center", bold=True)
    if t >= A("p7", "sentence"):   # the original liar sentence
        with at(cr, 360, 700, max(0.85, pop(t, A("p7", "sentence"), 0.25)), rot=0.02):
            shape(cr, rrect_pts(-280, -60, 560, 120, 14, 14), hexc("#2b2d3a"), seed=802, amp=0.4, lw=4)
            write(cr, [("\"This sentence is ", WHITE), ("FALSE", hexc("#ff6b6b")), (".\"", WHITE)], 0, 14, 42,
                  align="center", bold=True)
        cue("hit", t, A("p7", "sentence"))
    pino(cr, t, 120, 1180, 0.9, 1.0, "calm")
    hl(cr, t, [("a puzzle over ", INK), ("2,000 YEARS", RED), (" old", INK)], 215, 52, A("p7", "puzzle"),
       end=A("p7", "sentence") - 0.05, bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("p8") - 0.2, (1.3, 360, 640)), (A("p8", "nose"), (2.0, 380, 600)), (A("p8", "grow?"), (1.5, 360, 660))]
    set_camera(camera(t, keys))
    enter_world(cr)
    workshop(cr)
    wob = 1.0 + 0.8 * (math.sin(t * 6) + 1) / 2        # the nose can't decide
    pino(cr, t, 330, 640, 1.5, wob, "worried", look=0.8)
    for k, (lab, col, x) in enumerate((("YES", TRUE_C, 200), ("NO", LIE_C, 520))):
        if t >= A("p8", "grow?"):
            with at(cr, x, 1110, max(0.85, pop(t, A("p8", "grow?") + k * 0.12, 0.25))):
                shape(cr, rrect_pts(-110, -46, 220, 92, 46, 14), col, seed=900 + k, amp=0.3, lw=4)
                write(cr, [(lab, WHITE)], 0, 16, 48, align="center", bold=True)
    hl(cr, t, [("does his nose ", INK), ("GROW", RED), ("?", INK)], 215, 70, A("p8"), bold=True, underline=True)
    stamp(cr, t, A("p8", "grow?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"shop": scene_shop, "logic": scene_logic, "spin": scene_spin, "sign": scene_sign, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
