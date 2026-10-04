"""Clever words from history: Machiavelli, "Is it better to be loved or feared?" (The Prince, ch. 17; written 1513,
published 1532).

Real wording (English translation, W. K. Marriott): it is "much safer to be feared than loved, when, of the two, either
must be dispensed with"; love "is broken at every opportunity" for advantage, but fear "preserves you by a dread of
punishment which never fails"; a prince must be feared "in such a way that, if he does not win love, he avoids hatred",
by keeping away from his subjects' property, because "men more quickly forget the death of their father than the
loss of their patrimony". Structure follows the owner's Napoleon reference.
"""
import math

from motion.captions import captions
from motion.characters import CAST, person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import hl, stamp, whip
from motion.story import BLUE, CLOSE, GREEN, bg, buttons, card, scroll, tag

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="m1", scene="hook", text="Is it better to be loved, or feared? Five hundred years ago, one man gave an "
                                     "answer people still argue about."),
    dict(id="m2", scene="book", text="His name was Niccolò Machiavelli. In [fifteen thirteen,|1513,] he wrote a short "
                                     "book of advice for rulers. It's called The Prince."),
    dict(id="m3", scene="choice", text="In it, he asks the big question. Should a leader be loved, or feared?"),
    dict(id="m4", scene="choice", text="Best is both, he says. But if you have to pick one, it's much safer to be "
                                       "feared."),
    dict(id="m5", scene="ropes", text="Why? Because people break love whenever it helps them. But the fear of "
                                      "punishment never lets go."),
    dict(id="m6", scene="catch", text="But there's a catch. Feared is fine. Hated is not. And the fastest way to be "
                                      "hated? Take people's money."),
    dict(id="m7", scene="quote", text="In his words, people forget the death of their father faster than the loss of "
                                      "their inheritance."),
    dict(id="m8", scene="end", text="So what do you think? Would you rather be loved, or feared?", pace=0.95),
]

METADATA = dict(
    title="Is It Better to Be Loved or Feared? Machiavelli's Answer 😈",
    alt_titles=["The 500-Year-Old Answer to 'Loved or Feared?' 👑", "Machiavelli Said People Forgive Murder Before Money 😳"],
    description="""Is it better to be loved, or feared? 500 years ago, Niccolò Machiavelli gave an answer people still argue about. 👑

In The Prince (written in 1513), he says the best is both. But if you have to pick one, it's much safer to be feared: people break love whenever it helps them, but the fear of punishment never lets go.

The catch: feared is fine, hated is not. And the fastest way to be hated is to take people's money, because, in his words, men forget the death of their father faster than the loss of their inheritance. 😳

Source: Machiavelli, The Prince, chapter 17.

💬 So what do you think? Would you rather be loved, or feared? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Machiavelli", "#History", "#Philosophy"],
    tags=["machiavelli", "the prince", "better to be feared than loved", "loved or feared", "philosophy",
          "history quotes", "leadership", "power", "dark psychology", "interestingly strange"],
    pinned_comment="Loved or feared? Pick one and defend it 👇😈",
)

SKY, FLOOR = hexc("#3b2a2a"), hexc("#6b4a3a")
GOLD, GOLD_D = hexc("#f2c14e"), hexc("#b9862a")
PINK = hexc("#ff7aa8")
KING = "host"
FOLK = (("kid_a", 430), ("mia", 520), ("rocker_a", 610))


def crown(cr, who, x, y, s=1.0):
    c = CAST[who]
    top = y - (26 + c["bh"] + 2 * c["head"] - 12) * s
    with at(cr, x, top + 6 * s, s):
        sharp_shape(cr, [(-34, 0), (-34, -34), (-18, -14), (0, -40), (18, -14), (34, -34), (34, 0)], GOLD, seed=10,
                    amp=0.3, lw=3.5)


def machiavelli(cr, t, x, y, s=1.0, talking=False):
    """Our Machiavelli: a thin face, short dark hair, black Florentine robe with a red collar."""
    with at(cr, x, y, s):
        shape(cr, [(-160, 120), (160, 120), (200, 430), (-200, 430)], hexc("#1f1f24"), seed=20, amp=0.5, lw=5)
        shape(cr, [(-70, 112), (70, 112), (50, 150), (-50, 150)], hexc("#a0303a"), seed=21, amp=0.3, lw=4)
        blob(cr, 0, 0, 78, 100, hexc("#f0c29c"), seed=22, amp=0.5, lw=5)
        shape(cr, [(-80, -20), (-70, -90), (0, -112), (70, -90), (80, -20), (50, -60), (-50, -60)], hexc("#2a2018"),
              seed=23, amp=0.5, lw=4)
        for sx in (-1, 1):
            blob(cr, sx * 30, 0, 10, 8, WHITE, seed=24 + sx, amp=0.1, lw=3)
            blob(cr, sx * 30 + 3, 1, 5, 5, INK, seed=26 + sx, amp=0.1, lw=0, stroke=None)
        line(cr, [(-22, 50), (0, 46), (24, 40)], 5, INK, seed=28, amp=0.2) if not talking else \
            blob(cr, 0, 48, 18, 5 + 9 * abs(math.sin(t * 20)), hexc("#7a2b35"), seed=29, amp=0.2, lw=3)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, (1.8, 360, 830)), (A("m1", "feared?"), (1.8, 380, 830)), (A("m1", "five"), (1.6, 360, 820))]
    bg(cr, t, keys, SKY, FLOOR)
    person(cr, KING, 360, 960, t, facing=1, arms=("hip", "hip"), eyes="sly", mouth="smirk", scale=1.15)
    crown(cr, KING, 360, 960, 1.15)
    # a heart on one side, a sword on the other
    with at(cr, 250, 700, 1.0 + 0.06 * math.sin(t * 5)):
        blob(cr, -14, -10, 26, 26, PINK, seed=30, amp=0.3, lw=3)
        blob(cr, 14, -10, 26, 26, PINK, seed=31, amp=0.3, lw=3)
        sharp_shape(cr, [(-38, -2), (38, -2), (0, 42)], PINK, seed=32, amp=0.3, lw=3)
    if t >= A("m1", "feared?"):
        with at(cr, 480, 700, max(0.6, pop(t, A("m1", "feared?"), 0.25)), rot=0.5):
            line(cr, [(0, -70), (0, 50)], 12, hexc("#c9cdd4"), seed=33, amp=0.2)
            line(cr, [(-30, 30), (30, 30)], 10, GOLD_D, seed=34, amp=0.2)
    hl(cr, t, [("LOVED", PINK), (" or ", INK), ("FEARED", RED), ("?", INK)], 215, 70, 0.0, bold=True, sound=False,
       halo=hexc("#fbf3e1", 0.95))
    cue("hit", t, A("m1", "feared?"))


def scene_book(cr, t, tl):
    A = tl.at
    keys = [(A("m2") - 0.2, (1.0, 360, 640)), (A("m2", "1513,"), (1.0, 360, 640)), (A("m2", "prince."), (1.1, 360, 620))]
    bg(cr, t, keys, SKY)
    machiavelli(cr, t, 360, 560, 1.0, talking=False)
    tag(cr, t, A("m2", "machiavelli."), 360, 300, "MACHIAVELLI", GOLD, s=0.85)
    if t >= A("m2", "prince."):
        with at(cr, 520, 930, max(0.6, pop(t, A("m2", "prince."), 0.3)) * 0.9, rot=-0.08):
            shape(cr, rrect_pts(-110, -140, 220, 280, 8, 12), hexc("#7a2b35"), seed=40, amp=0.4, lw=5)
            write(cr, [("THE", GOLD)], 0, -40, 40, align="center", bold=True)
            write(cr, [("PRINCE", GOLD)], 0, 20, 46, align="center", bold=True)
            write(cr, [("1513", WHITE)], 0, 90, 34, align="center", bold=True)
    hl(cr, t, [("advice for ", INK), ("rulers", RED)], 215, 66, A("m2", "advice"), bold=True, halo=hexc("#fbf3e1", 0.95))


def door(cr, x, y, label, col, open_=0.0, seed=0):
    shape(cr, rrect_pts(x - 90, y - 260, 180, 260, 70, 14), hexc("#5a3a2a"), seed=seed, amp=0.4, lw=5)
    shape(cr, rrect_pts(x - 78, y - 248, 156 * (1 - 0.7 * open_), 248, 64, 12), col, seed=seed + 1, amp=0.3, lw=4)
    write(cr, [(label, WHITE)], x, y - 120, 40, align="center", bold=True)


def scene_choice(cr, t, tl):
    A = tl.at
    keys = [(A("m3") - 0.2, (1.5, 360, 820)), (A("m4"), (1.5, 360, 820)), (A("m4", "feared."), (1.7, 440, 830))]
    bg(cr, t, keys, SKY, FLOOR)
    pick = ease_out(seg(t, A("m4", "feared."), A("m4", "feared.") + 0.5))
    door(cr, 230, 960, "LOVED", PINK, seed=50)
    door(cr, 490, 960, "FEARED", RED, open_=pick, seed=60)
    kx = lerp(360, 440, pick)
    person(cr, KING, kx, 980, t, facing=1 if pick > 0.1 else -1, arms=("chin", "hip") if t < A("m4") else ("point", "hip"),
           eyes="sly", mouth="flat", scale=1.0)
    crown(cr, KING, kx, 980, 1.0)
    if A("m4", "both,") <= t < A("m4", "but"):
        tag(cr, t, A("m4", "both,"), 360, 630, "BEST: BOTH", GREEN, s=0.8)
    hl(cr, t, [("loved ", PINK), ("or ", INK), ("feared", RED), ("?", INK)], 215, 66, A("m3", "should"),
       end=A("m4", "but") - 0.05, bold=True, halo=hexc("#fbf3e1", 0.95))
    hl(cr, t, [("pick one? ", INK), ("FEARED", RED)], 215, 70, A("m4", "pick"), bold=True, halo=hexc("#fbf3e1", 0.95))
    cue("hit", t, A("m4", "feared."))


def scene_ropes(cr, t, tl):
    A = tl.at
    keys = [(A("m5") - 0.2, (1.0, 360, 640)), (A("m5", "love"), (1.08, 300, 640)), (A("m5", "fear"), (1.08, 420, 640))]
    bg(cr, t, keys, hexc("#efe6d6"), hexc("#d9c7a8"))
    # love: a thin pink thread that snaps; fear: a thick iron chain that holds
    snap = t >= A("m5", "helps")
    if not snap:
        line(cr, [(230, 420), (230, 820)], 12, PINK, seed=70, amp=0.6)
    else:
        line(cr, [(230, 420), (240, 590)], 12, PINK, seed=71, amp=0.6)
        line(cr, [(225, 670), (230, 820)], 12, PINK, seed=72, amp=0.6)
    for k in range(9):
        if t >= A("m5", "fear"):
            blob(cr, 490, 430 + k * 48, 28, 34, hexc("#7d838e"), seed=80 + k, amp=0.3, lw=5)
    tag(cr, t, A("m5", "love"), 230, 340, "LOVE", PINK, s=0.8)
    tag(cr, t, A("m5", "fear"), 490, 340, "FEAR", RED, s=0.8, seed=61)
    if snap:
        stamp(cr, t, A("m5", "helps"), "SNAP!", dur=0.6, y=330)
    hl(cr, t, [("love ", PINK), ("breaks", INK)], 215, 70, A("m5", "love"), end=A("m5", "fear") - 0.05, bold=True)
    hl(cr, t, [("fear ", RED), ("holds", INK)], 215, 70, A("m5", "fear"), bold=True)


def scene_catch(cr, t, tl):
    A = tl.at
    keys = [(A("m6") - 0.2, CLOSE), (A("m6", "hated?"), (1.5, 400, 810)), (A("m6", "money."), (1.5, 400, 810))]
    bg(cr, t, keys, SKY, FLOOR)
    grab = t >= A("m6", "take")
    person(cr, KING, 260, 960, t, facing=1, arms=("hold", "hip") if grab else ("hip", "hip"),
           eyes="sly" if grab else "dot", mouth="grin" if grab else "flat", scale=1.1)
    crown(cr, KING, 260, 960, 1.1)
    angry = t >= A("m6", "money.")
    for k, (who, x) in enumerate(FOLK):
        person(cr, who, x, 960, t, facing=-1, arms=("point", "down") if angry else ("hold", "down"),
               eyes="wide" if angry else "dot", mouth="o" if angry else "smile", scale=1.0, shake=1.5 if angry else 0)
    if grab:   # the bag moves from the people to the king
        u = ease_out(seg(t, A("m6", "take"), A("m6", "take") + 0.6))
        with at(cr, lerp(520, 330, u), 800, 0.9):
            blob(cr, 0, 0, 40, 34, GOLD, seed=90, amp=0.4, lw=4, stroke=GOLD_D)
            write(cr, [("$", GOLD_D)], 0, 14, 40, align="center", bold=True)
    hl(cr, t, [("feared: ", INK), ("OK", GREEN), ("  hated: ", INK), ("NO", RED)], 215, 60, A("m6", "feared"),
       end=A("m6", "fastest") - 0.05, bold=True, halo=hexc("#fbf3e1", 0.95))
    hl(cr, t, [("take their ", INK), ("MONEY", RED), ("?", INK)], 215, 66, A("m6", "take"), bold=True,
       halo=hexc("#fbf3e1", 0.95))
    if angry:
        stamp(cr, t, A("m6", "money."), "HATED", dur=0.7, y=330)


def scene_quote(cr, t, tl):
    A = tl.at
    keys = [(A("m7") - 0.2, (1.0, 360, 620)), (A("m7", "inheritance."), (1.06, 360, 620))]
    bg(cr, t, keys, SKY)
    lines = [([("People forget", INK)], A("m7", "forget")),
             ([("their ", INK), ("FATHER'S DEATH", RED)], A("m7", "death")),
             ([("faster than", INK)], A("m7", "faster")),
             ([("their ", INK), ("LOST MONEY", GOLD_D)], A("m7", "inheritance."))]
    scroll(cr, t, lines, 360, 540, 1.05, size=44, gap=68)
    machiavelli(cr, t, 560, 940, 0.4, talking=True)
    hl(cr, t, [("Machiavelli, ", INK), ("The Prince", RED)], 215, 60, A("m7"), bold=True, halo=hexc("#fbf3e1", 0.95))
    cue("hit", t, A("m7", "inheritance."))


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("m8") - 0.2, (1.0, 360, 640)), (A("m8", "loved,"), (1.05, 360, 640))]
    bg(cr, t, keys, SKY)
    machiavelli(cr, t, 360, 560, 1.0)
    buttons(cr, t, A("m8", "loved,"), (("LOVED", PINK), ("FEARED", RED)), y=1040, s=0.8)
    hl(cr, t, [("LOVED", PINK), (" or ", INK), ("FEARED", RED), ("?", INK)], 215, 70, A("m8", "would"), bold=True,
       underline=True, halo=hexc("#fbf3e1", 0.95))
    stamp(cr, t, A("m8", "feared?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "book": scene_book, "choice": scene_choice, "ropes": scene_ropes, "catch": scene_catch,
     "quote": scene_quote, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
