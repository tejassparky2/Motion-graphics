"""Researchers found / clever words from history: the Ben Franklin effect.

- Franklin's Autobiography: a wealthy, well-educated new member of the Pennsylvania Assembly spoke against him (late
  1730s). Franklin asked to borrow a scarce, curious book from the man's library; it was sent at once, and Franklin
  returned it about a week later with a note of thanks. Next time they met, the man spoke to him with great civility;
  "we became great friends, and our friendship continued to his death." Franklin's maxim: "He that has once done you a
  kindness will be more ready to do you another, than he whom you yourself have obliged."
- Jecker & Landy (1969, Human Relations): participants asked by the researcher himself to give back their winnings
  (as a personal favour) liked him more than those who weren't asked.
Structure follows the owner's Napoleon reference.
"""
import math

from motion.captions import captions
from motion.characters import CAST, bubble, person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    write
from motion.kit import hl, stamp, whip
from motion.story import BLUE, CLOSE, GREEN, bg, buttons, card, scroll, tag

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="b1", scene="hook", text="Want an enemy to like you? Don't do them a favor. Ask them for one."),
    dict(id="b2", scene="assembly", text="In the [seventeen thirties,|1730s,] a rich new lawmaker in Pennsylvania "
                                         "spoke out against Benjamin Franklin."),
    dict(id="b3", scene="book", text="Franklin didn't flatter him. He did something stranger. He asked to borrow a "
                                     "rare book from the man's library."),
    dict(id="b4", scene="book", text="The man sent it right away. Franklin returned it about a week later, with a "
                                     "note of thanks."),
    dict(id="b5", scene="friends", text="The next time they met, the man spoke to him kindly. And they stayed "
                                        "friends for life."),
    dict(id="b6", scene="quote", text="Franklin wrote: He that has once done you a kindness, will be more ready to do "
                                      "you another, than he whom you yourself have obliged."),
    dict(id="b7", scene="study", text="In [nineteen sixty-nine,|1969,] psychologists tested it. When the researcher "
                                      "asked people for a favor, they ended up liking him more."),
    dict(id="b8", scene="name", text="It's called the Ben Franklin effect. When we help someone, our brain decides we "
                                     "must like them."),
    dict(id="b9", scene="end", text="So what do you think? Would you try it on someone who doesn't like you?",
         pace=0.95),
]

METADATA = dict(
    title="Want an Enemy to Like You? Ask THEM for a Favor (Ben Franklin's Trick) 🤝",
    alt_titles=["The Ben Franklin Effect: Make Enemies Like You 😳", "Why Asking for a Favor Makes People Like You 🤝"],
    description="""Want an enemy to like you? Don't do them a favor. Ask them for one. 🤝

In the 1730s, a rich new lawmaker in Pennsylvania spoke out against Benjamin Franklin. Franklin didn't flatter him: he asked to borrow a rare book from the man's library. The rival sent it right away, Franklin returned it a week later with a note of thanks, and they stayed friends for life.

Franklin wrote: "He that has once done you a kindness will be more ready to do you another, than he whom you yourself have obliged."

In 1969, psychologists tested it (Jecker & Landy): when the researcher asked people for a favor, they ended up liking him more. It's called the Ben Franklin effect.

Sources: The Autobiography of Benjamin Franklin; Jecker & Landy (1969), Human Relations.

💬 So what do you think? Would you try it on someone who doesn't like you? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#BenFranklin", "#Psychology", "#LifeHacks"],
    tags=["ben franklin effect", "benjamin franklin", "psychology trick", "how to make someone like you",
          "dark psychology", "psychology facts", "history quotes", "researchers found", "social skills",
          "interestingly strange"],
    pinned_comment="Would you try this on someone who doesn't like you? Report back 😂🤝👇",
)

SKY, GROUND = hexc("#efe6d6"), hexc("#c9a77c")
HALL = hexc("#e9dcc0")
GOLD, GOLD_D = hexc("#f2c14e"), hexc("#b9862a")
PINK = hexc("#ff7aa8")
FRANK, RIVAL = "franklin", "seth"
# our Franklin: grey hair long at the sides, brown coat (own design)
CAST.setdefault("franklin", dict(CAST["oldman"], shirt=hexc("#7a5230"), pants=hexc("#5a3a20"), seed=251))
FX, RX = 230, 500


def book(cr, x, y, s=1.0, rot=0.0):
    with at(cr, x, y, s, rot=rot):
        shape(cr, rrect_pts(-46, -60, 92, 120, 6, 10), hexc("#7a2b35"), seed=10, amp=0.3, lw=4)
        line(cr, [(-32, -60), (-32, 60)], 3, GOLD, seed=11, amp=0.1)
        write(cr, [("RARE", GOLD)], 6, 6, 22, align="center", bold=True)


def note(cr, x, y, s=1.0):
    with at(cr, x, y, s, rot=0.1):
        shape(cr, rrect_pts(-50, -34, 100, 68, 6, 10), WHITE, seed=20, amp=0.3, lw=3)
        write(cr, [("thanks!", INK)], 0, 8, 22, align="center", bold=True)


def heart(cr, x, y, s=1.0, seed=30):
    with at(cr, x, y, s):
        blob(cr, -14, -10, 22, 22, PINK, seed=seed, amp=0.3, lw=3)
        blob(cr, 14, -10, 22, 22, PINK, seed=seed + 1, amp=0.3, lw=3)
        shape(cr, [(-32, -2), (32, -2), (0, 36)], PINK, seed=seed + 2, amp=0.3, lw=3)


def pair(cr, t, fmood=("dot", "smile"), rmood=("dot", "flat"), farms=("hip", "hip"), rarms=("hip", "hip"), rshake=0.0):
    person(cr, FRANK, FX, 960, t, facing=1, arms=farms, eyes=fmood[0], mouth=fmood[1], scale=1.1)
    person(cr, RIVAL, RX, 960, t, facing=-1, arms=rarms, eyes=rmood[0], mouth=rmood[1], scale=1.1, shake=rshake)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, CLOSE), (A("b1", "ask"), (1.6, 380, 810))]
    bg(cr, t, keys, SKY, GROUND)
    asked = t >= A("b1", "ask")
    pair(cr, t, fmood=("sly", "smirk"), rmood=("wide", "o") if asked else ("dot", "flat"),
         farms=("point", "hip") if asked else ("hip", "hip"), rarms=("hip", "hip"))
    if not asked:
        write(cr, [("#!@%", RED)], RX, 620, 40, align="center", bold=True)
    else:
        heart(cr, RX + 40, 620, max(0.6, pop(t, A("b1", "ask"), 0.3)) * 1.1)
    hl(cr, t, [("make an ", INK), ("ENEMY", RED), (" like you", INK)], 215, 60, 0.0, end=A("b1", "ask") - 0.05,
       bold=True, sound=False)
    hl(cr, t, [("ask ", INK), ("THEM", RED), (" for a favor", INK)], 215, 60, A("b1", "ask"), bold=True)


def scene_assembly(cr, t, tl):
    A = tl.at
    keys = [(A("b2") - 0.2, (1.4, 360, 790)), (A("b2", "against"), (1.55, 400, 810))]
    bg(cr, t, keys, HALL, GROUND)
    for k, x in enumerate((60, 660)):
        shape(cr, rrect_pts(x - 30, 380, 60, 580, 4, 12), WHITE, seed=40 + k, amp=0.4, lw=4)
    angry = t >= A("b2", "spoke")
    pair(cr, t, fmood=("wide", "o") if angry else ("dot", "smile"), rmood=("sly", "flat"),
         rarms=("point", "hip") if angry else ("hip", "hip"), rshake=1.0 if angry else 0)
    card(cr, t, A("b2", "1730s,"), 360, 610, 0.6, "PENNSYLVANIA", "1730s", seed=41)
    tag(cr, t, A("b2", "franklin."), FX, 700, "BEN FRANKLIN", GOLD, s=0.55)
    hl(cr, t, [("a rich ", INK), ("RIVAL", RED)], 215, 70, A("b2", "rich"), bold=True)


def scene_book(cr, t, tl):
    A = tl.at
    keys = [(A("b3") - 0.2, CLOSE), (A("b3", "borrow"), (1.6, 360, 810)), (A("b4"), CLOSE),
            (A("b4", "thanks."), (1.6, 380, 810))]
    bg(cr, t, keys, SKY, GROUND)
    pair(cr, t, fmood=("sly", "smirk") if t < A("b4") else ("happy", "grin"),
         rmood=("wide", "o") if A("b3", "borrow") <= t < A("b4") else ("dot", "smile"),
         farms=("point", "hip") if A("b3", "asked") <= t < A("b4") else ("hold", "hip"))
    if t >= A("b4", "sent"):   # the book flies over, then goes back with a note
        u = ease_out(seg(t, A("b4", "sent"), A("b4", "sent") + 0.6))
        back = ease_out(seg(t, A("b4", "returned"), A("b4", "returned") + 0.6))
        x = lerp(lerp(RX, FX + 50, u), RX - 40, back)
        book(cr, x, 760 - 60 * math.sin(math.pi * (u if back == 0 else back)), 0.9, rot=0.1)
        if t >= A("b4", "note"):
            note(cr, x + 40, 690, 0.9)
    elif t >= A("b3", "book"):
        book(cr, RX + 70, 760, max(0.6, pop(t, A("b3", "book"), 0.25)) * 0.9)
    hl(cr, t, [("no flattery...", INK)], 215, 64, A("b3"), end=A("b3", "asked") - 0.05, bold=True)
    hl(cr, t, [("\"Can I ", INK), ("BORROW", GREEN), (" a book?\"", INK)], 215, 58, A("b3", "asked"),
       end=A("b4") - 0.05, bold=True)
    hl(cr, t, [("returned, with ", INK), ("THANKS", GREEN)], 215, 60, A("b4", "returned"), bold=True)


def scene_friends(cr, t, tl):
    A = tl.at
    keys = [(A("b5") - 0.2, CLOSE), (A("b5", "friends"), (1.6, 370, 810))]
    bg(cr, t, keys, SKY, GROUND)
    pair(cr, t, fmood=("happy", "grin"), rmood=("happy", "grin"), farms=("point", "hip"), rarms=("point", "hip"))
    if t >= A("b5", "kindly."):
        heart(cr, 365, 640, max(0.6, pop(t, A("b5", "kindly."), 0.3)) * 1.1)
    hl(cr, t, [("friends ", GREEN), ("for life", INK)], 215, 70, A("b5", "friends"), bold=True)


def scene_quote(cr, t, tl):
    A = tl.at
    keys = [(A("b6") - 0.2, (1.0, 360, 640)), (A("b6", "obliged."), (1.04, 360, 640))]
    bg(cr, t, keys, SKY)
    lines = [([("He that has once done", INK)], A("b6", "he")),
             ([("you a ", INK), ("KINDNESS", GREEN)], A("b6", "kindness,")),
             ([("will be more ready", INK)], A("b6", "ready")),
             ([("to do you ", INK), ("ANOTHER", RED)], A("b6", "another,")),
             ([("than he whom you", INK)], A("b6", "than")),
             ([("yourself have obliged.", INK)], A("b6", "obliged."))]
    scroll(cr, t, lines, 360, 590, 1.0, size=40, gap=62, w=620)
    hl(cr, t, [("Benjamin ", INK), ("Franklin", GOLD_D)], 215, 62, A("b6"), bold=True)


def scene_study(cr, t, tl):
    A = tl.at
    keys = [(A("b7") - 0.2, (1.45, 360, 800)), (A("b7", "liking"), (1.55, 380, 810))]
    bg(cr, t, keys, hexc("#e6edf5"), hexc("#cfd8e3"))
    card(cr, t, A("b7", "1969,"), 360, 540, 0.6, "EXPERIMENT", "1969", seed=50)
    asked = t >= A("b7", "asked")
    person(cr, "teacher", 230, 960, t, facing=1, arms=("point", "hip") if asked else ("hip", "hip"), eyes="dot",
           mouth="o" if asked else "smile", scale=1.05)
    person(cr, "sam", 490, 960, t, facing=-1, arms=("hold", "down"), eyes="happy" if t >= A("b7", "liking") else "dot",
           mouth="grin" if t >= A("b7", "liking") else "smile", scale=1.05)
    if asked and t < A("b7", "liking"):
        bubble(cr, 300, 700, 210, 70, (250, 760), [("a favor?", INK)], s=0.9, size=30)
    if t >= A("b7", "liking"):   # a liking meter that fills
        u = ease_out(seg(t, A("b7", "liking"), A("b7", "more.", end=True)))
        with at(cr, 490, 690, 0.8):
            shape(cr, rrect_pts(-110, -24, 220, 48, 22, 10), WHITE, seed=51, amp=0.3, lw=3.5)
            shape(cr, rrect_pts(-104, -18, 208 * (0.35 + 0.6 * u), 36, 18, 10), PINK, seed=52, amp=0.2, lw=0,
                  stroke=None)
            write(cr, [("LIKE", INK)], 0, 11, 26, align="center", bold=True)
    hl(cr, t, [("they liked him ", INK), ("MORE", PINK)], 215, 64, A("b7", "liking"), bold=True)


def scene_name(cr, t, tl):
    A = tl.at
    keys = [(A("b8") - 0.2, (1.4, 360, 790)), (A("b8", "brain"), (1.5, 400, 800))]
    bg(cr, t, keys, SKY, GROUND)
    person(cr, RIVAL, 470, 960, t, facing=-1, arms=("chin", "hip"), eyes="happy", mouth="smile", scale=1.1)
    if t < A("b8", "when"):
        card(cr, t, A("b8", "franklin"), 360, 560, 0.62, "THE BEN FRANKLIN", "EFFECT", seed=60, w=520)
    else:
        bubble(cr, 360, 600, 440, 110, (450, 720), [("I helped him...", INK)], s=0.9, size=36, thought=True,
               lines=[[("I helped him...", INK)], [("so I must ", INK), ("LIKE", PINK), (" him!", INK)]])
    hl(cr, t, [("help ", INK), ("= ", INK), ("like", PINK)], 215, 70, A("b8", "help"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("b9") - 0.2, CLOSE), (A("b9", "try"), (1.55, 370, 810)), (A("b9", "you?"), (1.45, 360, 810))]
    bg(cr, t, keys, SKY, GROUND)
    pair(cr, t, fmood=("sly", "smirk"), rmood=("dot", "flat"), farms=("point", "hip"))
    book(cr, FX + 60, 780, 0.8)
    buttons(cr, t, A("b9", "you?"), (("I'D TRY IT", GREEN), ("NO WAY", RED)), y=1060, s=0.62)
    hl(cr, t, [("would you ", INK), ("TRY IT", GREEN), ("?", INK)], 215, 70, A("b9", "try"), bold=True, underline=True)
    stamp(cr, t, A("b9", "you?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "assembly": scene_assembly, "book": scene_book, "friends": scene_friends,
     "quote": scene_quote, "study": scene_study, "name": scene_name, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
