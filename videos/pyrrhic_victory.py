"""Clever words from history: Pyrrhus, "One more such victory and we are ruined" (the Pyrrhic victory).

Plutarch, Life of Pyrrhus 21: Pyrrhus, king of Epirus (a Greek kingdom), crossed to Italy to fight Rome (280 BC) and
beat the Romans at Heraclea and again at Asculum (279 BC). After Asculum, to someone congratulating him, he said: "If
we are victorious in one more battle with the Romans, we shall be utterly ruined." Plutarch explains: he had lost a
great part of the army he came with and almost all his friends and generals, he had no others to summon from home,
while the Romans filled up their legions quickly and easily, "as from a fountain gushing forth indoors". Hence a
"Pyrrhic victory": a win that costs the winner too much. The soldier counters on screen are a picture of the idea,
not real numbers (none are spoken).
"""
import math

from motion.captions import captions
from motion.characters import CAST, bubble, person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import hl, stamp, whip
from motion.story import BLUE, CLOSE, GREEN, bg, buttons, card, helmet, scroll, tag, talk

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="p1", scene="hook", text="A king won a big battle. Then he said: One more win like this, and we're "
                                     "finished."),
    dict(id="p2", scene="king", text="His name was Pyrrhus. He was a Greek king. About two thousand three hundred "
                                     "years ago, he took his army to fight Rome."),
    dict(id="p3", scene="count", text="He won. Then he fought Rome again. And he won again."),
    dict(id="p4", scene="count", text="But each win cost him many of his best soldiers. And most of his generals."),
    dict(id="p5", scene="count", text="He was far from home. He couldn't replace them."),
    dict(id="p6", scene="count", text="Rome could. After every loss, Rome quickly filled its army back up."),
    dict(id="p7", scene="quote", text="So when someone praised him for the win, Pyrrhus said: If we win one more "
                                      "battle against the Romans, we will be completely ruined.", speaker="pyrrhus",
         speaker_from="if"),
    dict(id="p8", scene="term", text="That's why a win that costs too much is called a Pyrrhic victory."),
    dict(id="p9", scene="friend", text="It's like winning an argument with your best friend. You win the argument. "
                                       "But you lose the friend."),
    dict(id="p10", scene="end", text="So what do you think? Have you ever won something, but lost more?", pace=0.95),
]

METADATA = dict(
    title="He WON the Battle… Then Said \"One More Win and We're Finished\" ⚔️",
    alt_titles=["Where \"Pyrrhic Victory\" Comes From ⚔️", "The King Who Won Himself Into Ruin 😳"],
    description="""A king won a big battle. Then he said: "One more win like this, and we're finished." ⚔️

About 2,300 years ago, Pyrrhus, a Greek king, took his army to fight Rome. He won. Then he won again. But each win cost him many of his best soldiers and most of his generals. He was far from home and couldn't replace them. Rome could: after every loss, it quickly filled its army back up.

So when someone praised him for the win, Pyrrhus said: "If we win one more battle against the Romans, we will be completely ruined."

That's why a win that costs too much is called a Pyrrhic victory. Like winning an argument with your best friend: you win the argument, but you lose the friend.

Source: Plutarch, Life of Pyrrhus, chapter 21.

💬 So what do you think? Have you ever won something, but lost more? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#History", "#Rome", "#PyrrhicVictory"],
    tags=["pyrrhic victory", "pyrrhus", "pyrrhus of epirus", "ancient rome", "history facts", "plutarch",
          "famous quotes", "clever words", "history stories", "interestingly strange"],
    pinned_comment="Have you ever won something but lost more? Tell us 👇⚔️",
)

SKY, GROUND = hexc("#f2e2c4"), hexc("#c9b083")
GOLD, GOLD_D = hexc("#f2c14e"), hexc("#b9862a")
P_BLUE = hexc("#2f5fa8")
R_RED = hexc("#b8322c")
GRAY = hexc("#a6a6a6")
PYR = "pyrrhus"
CAST.setdefault(PYR, dict(skin=hexc("#e8b48a"), shirt=hexc("#3c5f8f"), pants=hexc("#2b4466"), bw=100, bh=110, head=40,
                          kind="robe", hair="messy", hair_col=hexc("#3a2a22"), beard=hexc("#3a2a22"), seed=271))
CAST.setdefault("soldier_p", dict(skin=hexc("#f0c29c"), shirt=P_BLUE, pants=hexc("#24487f"), bw=88, bh=98, head=36,
                                  kind="robe", hair="messy", hair_col=hexc("#3a2a22"), seed=273))


def pyrrhus(cr, t, tl, x, y=960, s=1.1, facing=1, **kw):
    kw.setdefault("arms", ("hip", "hip"))
    kw.setdefault("eyes", "dot")
    person(cr, PYR, x, y, t, facing=facing, scale=s, mouth=talk(tl, PYR, t, kw.pop("mouth", "smile")), **kw)
    helmet(cr, PYR, x, y, s, crest=P_BLUE, facing=facing)


def banner(cr, x, y, col, s=1.0):
    with at(cr, x, y, s):
        line(cr, [(0, 0), (0, -220)], 7, hexc("#6b4a2a"), seed=10, amp=0.2)
        shape(cr, rrect_pts(0, -220, 110, 80, 6, 10), col, seed=11, amp=0.5, lw=4)
        blob(cr, 55, -180, 16, 16, GOLD, seed=12, amp=0.3, lw=3)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, CLOSE), (A("p1", "one"), (1.6, 330, 810)), (A("p1", "finished."), (1.7, 300, 820))]
    bg(cr, t, keys, SKY, GROUND)
    worried = t >= A("p1", "then")
    for k, x in enumerate((470, 560)):
        person(cr, "soldier_p", x, 960, t, facing=-1, arms=("down", "rub"), eyes="sad", mouth="flat", scale=0.85,
               lean=0.12)
        helmet(cr, "soldier_p", x, 960, 0.85, crest=P_BLUE, facing=-1)
    banner(cr, 140, 960, P_BLUE, 0.9)
    pyrrhus(cr, t, tl, 280, arms=("cheer", "hip") if not worried else ("face", "hip"),
            eyes="happy" if not worried else "sad", mouth="grin" if not worried else "flat")
    hl(cr, t, [("he ", INK), ("WON", GREEN), ("...", INK)], 215, 70, 0.0, end=A("p1", "one") - 0.05, bold=True,
       sound=False)
    hl(cr, t, [("\"one more win = ", INK), ("FINISHED", RED), ("\"", INK)], 215, 54, A("p1", "one"),
       bold=True)
    cue("hit", t, A("p1", "finished."))


def scene_king(cr, t, tl):
    A = tl.at
    keys = [(A("p2") - 0.2, CLOSE), (A("p2", "army"), (1.3, 380, 780))]
    bg(cr, t, keys, SKY, GROUND)
    march = ease_out(seg(t, A("p2", "army"), A("p2", "army") + 1.2))
    if t >= A("p2", "army"):
        for k in range(3):
            x = lerp(-80, 120, march) - k * 85
            person(cr, "soldier_p", x, 960, t, facing=1, walk=t * 1.4 if march < 1 else None, arms=("hold", "down"),
                   eyes="dot", mouth="flat", scale=0.8)
            helmet(cr, "soldier_p", x, 960, 0.8, crest=P_BLUE)
        banner(cr, 640, 960, R_RED, 0.85)
        tag(cr, t, A("p2", "rome."), 600, 640, "ROME", hexc("#ff9a8a"), s=0.6, seed=62)
    px = 330 if t < A("p2", "army") else lerp(330, 380, march)
    pyrrhus(cr, t, tl, px, arms=("point", "hip") if t >= A("p2", "fight") else ("hip", "hip"), eyes="sly")
    tag(cr, t, A("p2", "pyrrhus."), 330, 560, "KING PYRRHUS", GOLD, s=0.65)
    if A("p2", "greek") <= t < A("p2", "army"):
        tag(cr, t, A("p2", "greek"), 330, 640, "A GREEK KING", hexc("#9fd4ff"), s=0.55, seed=61)
    hl(cr, t, [("about ", INK), ("2,300", RED), (" years ago", INK)], 215, 62, A("p2", "about"), bold=True)


N = 10


def soldier_icon(cr, x, y, col, state, k=0):
    """state: 1 alive, 0 lost (grey, crossed)."""
    c = col if state > 0.5 else GRAY
    with at(cr, x, y, 1.2):
        blob(cr, 0, 20, 18, 22, c, seed=k, amp=0.3, lw=3)
        blob(cr, 0, -16, 15, 15, hexc("#f0c29c") if state > 0.5 else hexc("#d0d0d0"), seed=k + 20, amp=0.3, lw=3)
        shape(cr, [(-16, -18), (-12, -32), (0, -36), (12, -32), (16, -18)], c, seed=7, amp=0.2, lw=3)
        if state <= 0.5:
            line(cr, [(-16, -30), (16, 34)], 5, RED, seed=8, amp=0.2)


def army(cr, t, x0, y, col, alive_at):
    """A row of N soldiers; alive_at(k) -> 1/0 for soldier k at time t."""
    for k in range(N):
        soldier_icon(cr, x0 + (k % 5) * 112, y + (k // 5) * 112, col, alive_at(k), k)


def scene_count(cr, t, tl):
    A = tl.at
    keys = [(A("p3") - 0.2, (1.0, 360, 640))]
    bg(cr, t, keys, SKY)
    win1, win2 = A("p3", "won."), A("p3", "again.", nth=2)
    refill = A("p6", "filled")

    def pyr_alive(k):
        if t >= win2 and k >= 4:
            return 0
        if t >= win1 and k >= 7:
            return 0
        return 1

    def rome_alive(k):
        if t >= refill + k * 0.06:
            return 1
        if t >= win2 and k >= 2:
            return 0
        if t >= win1 and k >= 6:
            return 0
        return 1

    shape(cr, rrect_pts(30, 260, 660, 285, 24, 14), hexc("#e3ecf7"), seed=20, amp=0.4, lw=4)
    write(cr, [("PYRRHUS", P_BLUE)], 360, 305, 44, align="center", bold=True)
    army(cr, t, 136, 368, P_BLUE, pyr_alive)
    shape(cr, rrect_pts(30, 562, 660, 285, 24, 14), hexc("#f7e3e1"), seed=21, amp=0.4, lw=4)
    write(cr, [("ROME", R_RED)], 360, 607, 44, align="center", bold=True)
    army(cr, t, 136, 670, R_RED, rome_alive)
    if t >= win1:
        tag(cr, t, win1, 590, 285, "WIN 1" if t < win2 else "WIN 2", GREEN, s=0.6, seed=63)
    if A("p5") <= t < A("p6"):
        tag(cr, t, A("p5", "replace"), 360, 553, "NO NEW SOLDIERS", hexc("#ffb3a8"), s=0.65, seed=65)
    if t >= refill:
        tag(cr, t, refill, 580, 582, "REFILLED!", GREEN, s=0.6, seed=66)
    hl(cr, t, [("he ", INK), ("WON", GREEN), (". twice.", INK)], 215, 70, A("p3"), end=A("p4") - 0.05, bold=True)
    hl(cr, t, [("but the ", INK), ("COST", RED)], 215, 70, A("p4"), end=A("p5") - 0.05, bold=True)
    hl(cr, t, [("far from ", INK), ("HOME", RED)], 215, 70, A("p5"), end=A("p6") - 0.05, bold=True)
    hl(cr, t, [("Rome ", R_RED), ("REFILLS", GREEN)], 215, 70, A("p6"), bold=True)
    for st in (win1, win2):
        cue("hit", t, st)
    cue("pop", t, refill)


def scene_quote(cr, t, tl):
    A = tl.at
    keys = [(A("p7") - 0.2, (1.5, 380, 810)), (A("p7", "if"), (1.15, 360, 700))]
    bg(cr, t, keys, SKY, GROUND)
    person(cr, "soldier_p", 520, 960, t, facing=-1, arms=("thumb", "down") if t < A("p7", "if") else ("down", "down"),
           eyes="happy" if t < A("p7", "if") else "wide", mouth="grin" if t < A("p7", "if") else "o", scale=0.95)
    helmet(cr, "soldier_p", 520, 960, 0.95, crest=P_BLUE, facing=-1)
    pyrrhus(cr, t, tl, 270, arms=("chin", "hip") if t < A("p7", "if") else ("point", "hip"),
            eyes="sad" if t >= A("p7", "if") else "dot", mouth="flat")
    if t >= A("p7", "if"):
        lines = [([("\"One more win", INK)], A("p7", "if")),
                 ([("against Rome...", INK)], A("p7", "against")),
                 ([("and we're ", INK), ("RUINED", RED), (".\"", INK)], A("p7", "ruined."))]
        scroll(cr, t, lines, 360, 470, 0.8, size=50, gap=70, w=600)
    hl(cr, t, [("\"Great ", INK), ("WIN", GREEN), ("!\"", INK)], 215, 70, A("p7"), end=A("p7", "if") - 0.05, bold=True)
    hl(cr, t, [("Pyrrhus ", INK), ("said", RED)], 215, 66, A("p7", "if"), bold=True)
    cue("hit", t, A("p7", "ruined."))


def scene_term(cr, t, tl):
    A = tl.at
    keys = [(A("p8") - 0.2, (1.0, 360, 640))]
    bg(cr, t, keys, SKY)
    if t >= A("p8", "win"):
        lines = [([("a win that", INK)], A("p8", "win")), ([("COSTS TOO MUCH", RED)], A("p8", "costs"))]
        scroll(cr, t, lines, 360, 450, 0.95, size=52, gap=72, w=580)
    card(cr, t, A("p8", "called"), 360, 720, 1.0, "it's called a", "PYRRHIC VICTORY", seed=70, w=600)
    hl(cr, t, [("a win that ", INK), ("HURTS", RED)], 215, 66, A("p8"), bold=True)
    cue("hit", t, A("p8", "victory."))


def trophy(cr, x, y, s=1.0):
    with at(cr, x, y, s):
        shape(cr, [(-40, -60), (40, -60), (26, 0), (-26, 0)], GOLD, seed=80, amp=0.3, lw=4)
        shape(cr, rrect_pts(-10, 0, 20, 30, 4, 8), GOLD_D, seed=81, amp=0.2, lw=3)
        shape(cr, rrect_pts(-30, 30, 60, 16, 4, 8), GOLD_D, seed=82, amp=0.2, lw=3)


def scene_friend(cr, t, tl):
    A = tl.at
    keys = [(A("p9") - 0.2, CLOSE), (A("p9", "lose"), (1.4, 330, 790))]
    bg(cr, t, keys, hexc("#cfe8f5"), hexc("#9ccc7a"))
    won = t >= A("p9", "win", nth=2)
    leave = ease_out(seg(t, A("p9", "lose"), A("p9", "lose") + 1.0))
    person(cr, "kid_c", 240, 960, t, facing=1, arms=("cheer", "hip") if won and leave < 0.3 else
           ("point", "hip"), eyes="happy" if won and leave < 0.3 else ("sad" if leave >= 0.3 else "sly"),
           mouth="grin" if won and leave < 0.3 else ("flat" if leave >= 0.3 else "o"), scale=1.1)
    if won:
        trophy(cr, 160, 740, max(0.6, pop(t, A("p9", "win", nth=2), 0.3)) * 0.9)
    fx = lerp(500, 800, leave)
    person(cr, "kid_b", fx, 960, t, facing=-1 if leave < 0.05 else 1, walk=t * 1.4 if 0 < leave < 1 else None,
           arms=("point", "hip") if not won else ("down", "down"), eyes="sly" if not won else "sad",
           mouth="o" if not won else "sad", scale=1.1)
    if not won and t >= A("p9"):
        bubble(cr, 370, 600, 200, 100, (380, 700), [("Blah blah!", INK)], s=0.9, size=36)
    hl(cr, t, [("won the ", INK), ("ARGUMENT", GREEN)], 215, 62, A("p9", "win", nth=2), end=A("p9", "lose") - 0.05,
       bold=True)
    hl(cr, t, [("lost the ", INK), ("FRIEND", RED)], 215, 70, A("p9", "lose"), bold=True)
    hl(cr, t, [("like an ", INK), ("ARGUMENT", RED)], 215, 66, A("p9"), end=A("p9", "win", nth=2) - 0.05, bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("p10") - 0.2, CLOSE)]
    bg(cr, t, keys, SKY, GROUND)
    banner(cr, 140, 960, P_BLUE, 0.9)
    pyrrhus(cr, t, tl, 300, arms=("face", "hip"), eyes="sad", mouth="flat")
    for k, x in enumerate((480, 570)):
        person(cr, "soldier_p", x, 960, t, facing=-1, arms=("down", "rub"), eyes="sad", mouth="flat", scale=0.85,
               lean=0.12)
        helmet(cr, "soldier_p", x, 960, 0.85, crest=P_BLUE, facing=-1)
    buttons(cr, t, A("p10", "won"), (("YES", RED), ("NOT YET", GREEN)), y=1060, s=0.7)
    hl(cr, t, [("won, but ", INK), ("LOST MORE", RED), ("?", INK)], 215, 62, A("p10", "have"), bold=True,
       underline=True)
    stamp(cr, t, A("p10", "more?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "king": scene_king, "count": scene_count, "quote": scene_quote, "term": scene_term,
     "friend": scene_friend, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
