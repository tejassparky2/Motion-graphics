"""Researchers found: the marshmallow test, revisited.

- Walter Mischel's delay-of-gratification studies at Stanford's Bing Nursery School (late 1960s-early 1970s): one treat
  now, or two if the child waits alone. Follow-ups (e.g. Shoda, Mischel & Peake 1990) linked longer waiting to higher
  teenage test scores (SAT).
- Watts, Duncan & Quan (2018, Psychological Science): a larger, more diverse sample (children of mothers without a
  college degree, from a national study). The link was about half the original size, and shrank by about two thirds
  once family background, early ability and home environment were counted.
- Kidd, Palmeri & Aslin (2013, Cognition), "Rational snacking": children who had seen the adult break a promise waited
  a median of about 3 minutes; after a reliable adult, about 12 minutes (about four times longer).
Structure follows the owner's Napoleon reference.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    write
from motion.kit import hl, stamp, whip
from motion.story import BLUE, CLOSE, GREEN, bg, buttons, card, tag

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="k1", scene="hook", text="One treat right now. Or two, if you can wait. This simple test was supposed to "
                                     "predict your whole future."),
    dict(id="k2", scene="lab", text="In the late [nineteen sixties,|1960s,] psychologist Walter Mischel tried it on "
                                    "preschool kids at Stanford University."),
    dict(id="k3", scene="deal", text="Each child got a marshmallow, and a deal. Eat it now. Or wait alone, and get "
                                     "two."),
    dict(id="k4", scene="later", text="Years later, the kids who waited longer had higher test scores as teenagers."),
    dict(id="k5", scene="later", text="So the lesson seemed clear. Willpower is the secret to success."),
    dict(id="k6", scene="redo", text="But the first kids all came from one university nursery school. In "
                                     "[twenty eighteen,|2018,] researchers tried again, with hundreds of kids from "
                                     "different families."),
    dict(id="k7", scene="redo", text="Waiting still mattered a little. But once they counted family money and home "
                                     "life, the effect shrank by about two thirds."),
    dict(id="k8", scene="trust", text="And in another study, kids waited about four times longer, when the adult had "
                                      "kept an earlier promise."),
    dict(id="k9", scene="end", text="So what do you think? Is waiting about willpower? Or about trust?", pace=0.95),
]

METADATA = dict(
    title="The Marshmallow Test Was WRONG? What Scientists Found Later 🍬",
    alt_titles=["The Famous Willpower Test… Was It Really About Money? 🍬",
                "Wait for 2 Marshmallows? The Twist Nobody Told You 😳"],
    description="""One treat now, or two if you can wait. This simple test was supposed to predict your whole future. 🍬

In the late 1960s, psychologist Walter Mischel tried it on preschool kids at Stanford. Years later, the kids who waited longer had higher test scores as teenagers, and "willpower is the secret to success" became famous.

But the first kids all came from one university nursery school. In 2018, researchers tried again with hundreds of kids from different families: waiting still mattered a little, but once they counted family money and home life, the effect shrank by about two thirds. And in another study, kids waited about four times longer when the adult had kept an earlier promise. 😳

Studies: Mischel (Stanford, 1960s-70s); Watts, Duncan & Quan (2018), Psychological Science; Kidd, Palmeri & Aslin (2013), Cognition.

💬 So what do you think? Is waiting about willpower, or about trust? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#MarshmallowTest", "#Psychology", "#Willpower"],
    tags=["marshmallow test", "marshmallow experiment", "delayed gratification", "willpower", "psychology experiment",
          "stanford", "self control", "researchers found", "psychology facts", "interestingly strange"],
    pinned_comment="Would YOU have waited for the second marshmallow? Be honest 🍬👇",
)

SKY, GROUND = hexc("#eaf1f8"), hexc("#cfd8e3")
TABLE, TABLE_D = hexc("#c99a6b"), hexc("#9c6b43")
PINK = hexc("#ff7aa8")
KID = "kid_b"


def marshmallow(cr, x, y, s=1.0, seed=0):
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-26, -40, 52, 40, 14, 10), WHITE, seed=seed, amp=0.3, lw=3.5)
        blob(cr, 0, -40, 26, 8, hexc("#f4f4f4"), seed=seed + 1, amp=0.2, lw=3)


def plate(cr, x, y, n, s=1.0):
    with at(cr, x, y, s):
        blob(cr, 0, 0, 80, 16, WHITE, seed=10, amp=0.3, lw=3.5)
        for k in range(n):
            marshmallow(cr, (k - (n - 1) / 2) * 56, 4, 0.9, seed=20 + k)


def table(cr, x, y, w=420):
    shape(cr, rrect_pts(x - w / 2, y, w, 30, 6, 10), TABLE, seed=30, amp=0.3, lw=4)
    for sx in (-1, 1):
        line(cr, [(x + sx * (w / 2 - 30), y + 30), (x + sx * (w / 2 - 30), y + 140)], 10, TABLE_D, seed=31 + sx, amp=0.2)


def clock(cr, t, x, y, s=1.0, speed=1.0, seed=40):
    with at(cr, x, y, s):
        blob(cr, 0, 0, 46, 46, WHITE, seed=seed, amp=0.3, lw=4)
        a = t * speed
        line(cr, [(0, 0), (28 * math.sin(a), -28 * math.cos(a))], 5, INK, seed=seed + 1, amp=0.1)
        line(cr, [(0, 0), (16 * math.sin(a / 12), -16 * math.cos(a / 12))], 6, INK, seed=seed + 2, amp=0.1)


def bar(cr, x, base, h, col, label, seed, w=120):
    if h > 1:
        shape(cr, rrect_pts(x - w / 2, base - h, w, h, 8, 10), col, seed=seed, amp=0.3, lw=4)
    write(cr, [(label, INK)], x, base + 44, 32, align="center", bold=True)


def kid_at_table(cr, t, x=360, mood="dot", mouth="smile", sweat=False, arms=("hold", "hold")):
    person(cr, KID, x, 960, t, facing=1, arms=arms, eyes=mood, mouth=mouth, scale=1.1, sweat=sweat)
    table(cr, x, 860)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, (1.7, 360, 820)), (A("k1", "two,"), (1.5, 360, 810)), (A("k1", "predict"), (1.5, 360, 800))]
    bg(cr, t, keys, SKY, GROUND)
    kid_at_table(cr, t, mood="wide", mouth="o")
    plate(cr, 270, 858, 1, 0.9)
    if t >= A("k1", "two,"):
        plate(cr, 450, 858, 2, 0.9)
    tag(cr, t, A("k1", "now."), 270, 640, "NOW: 1", hexc("#ff8a80"), s=0.8)
    tag(cr, t, A("k1", "two,"), 450, 640, "WAIT: 2", hexc("#7ee08a"), s=0.8, seed=61)
    hl(cr, t, [("1 now", RED), (" or ", INK), ("2 later", GREEN), ("?", INK)], 215, 66, 0.0, bold=True, sound=False)
    if t >= A("k1", "future."):
        stamp(cr, t, A("k1", "future."), "YOUR FUTURE?", dur=0.8, y=330)


def scene_lab(cr, t, tl):
    A = tl.at
    keys = [(A("k2") - 0.2, (1.4, 360, 780))]
    bg(cr, t, keys, SKY, GROUND)
    card(cr, t, A("k2", "1960s,"), 360, 560, 0.75, "STANFORD", "1960s", seed=50)
    tag(cr, t, A("k2", "mischel"), 360, 700, "WALTER MISCHEL", hexc("#9fd0ff"), s=0.7)
    for k, (who, x) in enumerate((("kid_a", 230), ("kid_b", 360), ("kid_d", 490))):
        if t >= A("k2", "preschool"):
            person(cr, who, x, 960, t, facing=1 if x < 360 else -1, eyes="happy", mouth="grin", scale=1.0)
    hl(cr, t, [("the ", INK), ("marshmallow", PINK), (" test", INK)], 215, 66, A("k2"), bold=True)


def scene_deal(cr, t, tl):
    A = tl.at
    keys = [(A("k3") - 0.2, (1.6, 360, 820)), (A("k3", "now."), (1.7, 300, 820)), (A("k3", "two."), (1.6, 400, 820))]
    bg(cr, t, keys, SKY, GROUND)
    waiting = t >= A("k3", "wait")
    kid_at_table(cr, t, mood="wide" if waiting else "happy", mouth="flat" if waiting else "grin", sweat=waiting,
                 arms=("face", "down") if waiting else ("hold", "hold"))
    plate(cr, 290, 858, 1, 0.9)
    if waiting:
        clock(cr, t, 480, 640, 0.9, speed=3.0)
    tag(cr, t, A("k3", "eat"), 290, 650, "EAT NOW: 1", hexc("#ff8a80"), s=0.7)
    if t >= A("k3", "two."):
        plate(cr, 470, 858, 2, 0.8)
    hl(cr, t, [("eat it ", INK), ("now", RED), ("...", INK)], 215, 66, A("k3", "eat"), end=A("k3", "wait") - 0.05,
       bold=True)
    hl(cr, t, [("...or ", INK), ("WAIT", GREEN), (" for two", INK)], 215, 66, A("k3", "wait"), bold=True)


def scene_later(cr, t, tl):
    A = tl.at
    keys = [(A("k4") - 0.2, (1.35, 360, 700)), (A("k5"), (1.35, 360, 700)), (A("k5", "willpower"), (1.4, 360, 690))]
    bg(cr, t, keys, SKY, GROUND)
    g = ease_out(seg(t, A("k4", "higher"), A("k4", "teenagers.", end=True)))
    bar(cr, 270, 820, 120 + 200 * g, GREEN, "WAITED", seed=60)
    bar(cr, 450, 820, 120 + 50 * g, BLUE, "ATE IT", seed=61)
    line(cr, [(170, 820), (550, 820)], 5, INK, seed=62, amp=0.2)
    tag(cr, t, A("k4", "years"), 360, 450, "YEARS LATER", hexc("#9fd0ff"), s=0.7)
    hl(cr, t, [("higher ", INK), ("test scores", GREEN)], 215, 66, A("k4", "higher"), end=A("k5") - 0.05, bold=True)
    if t >= A("k5", "willpower"):
        stamp(cr, t, A("k5", "willpower"), "WILLPOWER = SUCCESS?", dur=1.2, y=330)


def scene_redo(cr, t, tl):
    A = tl.at
    keys = [(A("k6") - 0.2, (1.35, 360, 760)), (A("k6", "2018,"), (1.3, 360, 740)), (A("k7"), (1.3, 360, 700)),
            (A("k7", "shrank"), (1.35, 360, 700))]
    bg(cr, t, keys, SKY, GROUND)
    if t < A("k6", "2018,"):
        card(cr, t, A("k6", "nursery"), 360, 600, 0.75, "ONE NURSERY", "SCHOOL", seed=70)
        for k in range(4):
            person(cr, "kid_b", 210 + k * 100, 960, t, facing=1, eyes="dot", mouth="smile", scale=0.9)
    elif t < A("k7"):
        card(cr, t, A("k6", "2018,"), 360, 520, 0.7, "TRIED AGAIN", "2018", seed=71)
        for k, who in enumerate(("kid_a", "mia", "kid_c", "rocker_a", "kid_d", "chotu", "kid_b", "rocker_b")):
            if t >= A("k6", "hundreds") + k * 0.08:
                person(cr, who, 150 + (k % 4) * 140, 800 + (k // 4) * 160, t, facing=1 if k % 2 else -1,
                       eyes="happy", mouth="grin", scale=0.75)
    else:
        shrink = ease_out(seg(t, A("k7", "shrank"), A("k7", "thirds.", end=True)))
        h = 330 * (1 - 0.66 * shrink)
        bar(cr, 360, 790, h, GREEN, "WAITING'S EFFECT", seed=72, w=180)
        if t >= A("k7", "money"):
            tag(cr, t, A("k7", "money"), 230, 460, "FAMILY MONEY", hexc("#ffd23f"), s=0.6)
        if t >= A("k7", "home"):
            tag(cr, t, A("k7", "home"), 500, 460, "HOME LIFE", hexc("#ffd23f"), s=0.6, seed=62)
        if t >= A("k7", "thirds."):
            tag(cr, t, A("k7", "thirds."), 360, 580, "-2/3", hexc("#ff8a80"), s=0.85, seed=63)
    hl(cr, t, [("tried ", INK), ("AGAIN", RED)], 215, 70, A("k6", "2018,"), end=A("k7") - 0.05, bold=True)
    hl(cr, t, [("the effect ", INK), ("SHRANK", RED)], 215, 66, A("k7", "shrank"), bold=True)


def scene_trust(cr, t, tl):
    A = tl.at
    keys = [(A("k8") - 0.2, (1.5, 360, 800)), (A("k8", "promise."), (1.5, 360, 800))]
    bg(cr, t, keys, SKY, GROUND)
    for x, label, col, mins, seed in ((230, "BROKEN PROMISE", hexc("#ff8a80"), "3 min", 80),
                                      (490, "KEPT PROMISE", hexc("#7ee08a"), "12 min", 81)):
        person(cr, "kid_a" if x < 360 else "kid_d", x, 960, t, facing=1 if x < 360 else -1,
               eyes="dot" if x < 360 else "happy", mouth="flat" if x < 360 else "smile", scale=1.0)
        tag(cr, t, A("k8", "four"), x, 630, mins, col, s=0.7, seed=seed)
        tag(cr, t, A("k8", "kept"), x, 700, label, col, s=0.4, seed=seed + 10)
        clock(cr, t, x, 560, 0.75, speed=1.0 if x < 360 else 4.0, seed=seed + 20)
    hl(cr, t, [("waited ", INK), ("4x longer", GREEN)], 215, 70, A("k8", "four"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("k9") - 0.2, (1.5, 360, 820)), (A("k9", "willpower?"), (1.6, 360, 820)), (A("k9", "trust?"), (1.45, 360, 820))]
    bg(cr, t, keys, SKY, GROUND)
    kid_at_table(cr, t, mood="sly", mouth="smirk", arms=("chin", "hold"))
    plate(cr, 360, 858, 1, 0.9)
    buttons(cr, t, A("k9", "trust?"), (("WILLPOWER", BLUE), ("TRUST", GREEN)), y=1060, s=0.62)
    hl(cr, t, [("willpower", BLUE), (" or ", INK), ("trust", GREEN), ("?", INK)], 215, 70, A("k9", "willpower?"),
       bold=True, underline=True)
    stamp(cr, t, A("k9", "trust?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "lab": scene_lab, "deal": scene_deal, "later": scene_later, "redo": scene_redo,
     "trust": scene_trust, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
