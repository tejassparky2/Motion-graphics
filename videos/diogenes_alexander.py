"""Clever words from history: Diogenes and Alexander the Great (Plutarch, Life of Alexander, ch. 14).

At Corinth (c. 336 BC), after the Greeks chose the young Alexander as their leader, statesmen and philosophers came
to congratulate him; Diogenes of Sinope did not. Alexander went to him and found him lying in the sun; asked whether he
wanted anything, Diogenes said "Yes, stand a little out of my sun." Alexander's followers laughed and jeered, but he
said: "But verily, if I were not Alexander, I would be Diogenes." (Perrin translation.) Diogenes was famous for living
in a large clay jar (a pithos), often called a "barrel" in retellings. The cup: Diogenes Laertius, Lives 6.37 ("One
day, observing a child drinking out of his hands, he cast away the cup from his wallet with the words, 'A child has
beaten me in plain living.'"). Structure follows the owner's Napoleon
reference.
"""
import math

from motion.captions import captions
from motion.characters import CAST, person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import hl, stamp, whip
from motion.story import CLOSE, GREEN, bg, buttons, scroll, tag

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="d1", scene="hook", text="The most powerful man in the world offered a poor man anything he wanted. The "
                                     "poor man asked him to move."),
    dict(id="d2", scene="leader", text="The powerful man was Alexander the Great. Greece had just made him its "
                                       "leader."),
    dict(id="d3", scene="corinth", text="In Corinth, important people came to praise him."),
    dict(id="d4", scene="jar", text="But one man didn't come. Diogenes, a philosopher who lived in a big clay jar."),
    dict(id="d5", scene="jar", text="So Alexander went to find him. Diogenes was lying in the sun."),
    dict(id="d6", scene="meet", text="Alexander asked if he wanted anything at all."),
    dict(id="d7", scene="meet", text="Diogenes said: Yes. Stand a little out of my sun.", speaker="oldman",
         speaker_from="yes.", pace=0.9),
    dict(id="d8", scene="offer", text="Why was that so clever? Alexander could give him gold. Land. Even power."),
    dict(id="d9", scene="offer", text="But Diogenes didn't want any of it."),
    dict(id="d10", scene="cup", text="He once saw a boy drinking water from his hands. So he threw away his only cup."),
    dict(id="d11", scene="nothing", text="So the king had nothing to offer him. The only thing he could do, was step "
                                         "out of the sunlight."),
    dict(id="d12", scene="nothing", text="If someone needs nothing from you, you can't buy him. And you can't control "
                                         "him."),
    dict(id="d13", scene="laugh", text="His men laughed. But Alexander understood. He said: if I were not Alexander, "
                                       "I would be Diogenes.", speaker="alexander", speaker_from="if",
         gap=0.5),
    dict(id="d14", scene="end", text="So what do you think? Who was really richer? The man who had everything, or the "
                                     "man who needed nothing?", pace=0.95),
]

METADATA = dict(
    title="Alexander the Great Offered Him Anything… His Answer Was Genius ☀️",
    alt_titles=["The Man Who Told Alexander the Great to Move 😳", "Who Was Richer: Alexander or Diogenes? ☀️"],
    description="""The most powerful man in the world offered a poor man anything he wanted. The poor man asked him to move. ☀️

Greece had just made Alexander the Great its leader. In Corinth, important people came to praise him, but the philosopher Diogenes, who lived in a big clay jar, didn't come. So Alexander went to find him, lying in the sun, and asked if he wanted anything at all.

Diogenes said: "Yes. Stand a little out of my sun."

Why was that so clever? Alexander could give him gold, land, even power, but Diogenes didn't want any of it. He once saw a boy drinking water from his hands, so he threw away his only cup. So the king had nothing to offer him: the only thing he could do was step out of the sunlight. If someone needs nothing from you, you can't buy him, and you can't control him.

Alexander's men laughed, but Alexander understood: "If I were not Alexander, I would be Diogenes."

Sources: Plutarch, Life of Alexander, chapter 14; Diogenes Laertius, Lives of the Philosophers, book 6 (the cup).

💬 So what do you think? Who was really richer: the man who had everything, or the man who needed nothing? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#AlexanderTheGreat", "#Diogenes", "#Philosophy"],
    tags=["diogenes", "alexander the great", "diogenes and alexander", "stand out of my sun", "stoic", "philosophy",
          "history stories", "ancient greece", "plutarch", "interestingly strange"],
    pinned_comment="Who was richer: Alexander or Diogenes? Defend your answer 👇☀️",
)

SKY, GROUND = hexc("#f7e7c4"), hexc("#d9bf8f")
GOLD, GOLD_D = hexc("#f2c14e"), hexc("#b9862a")
CLAY, CLAY_D = hexc("#c46a3c"), hexc("#8e4a26")
SUN = hexc("#ffd23f")
ALEX, DIO = "alexander", "oldman"
# Alexander: young, curly hair, royal purple robe (our own design)
CAST.setdefault("alexander", dict(skin=hexc("#f0c29c"), shirt=hexc("#6b2d7a"), pants=hexc("#6b2d7a"), bw=92, bh=112,
                                  head=40, kind="robe", hair="messy", hair_col=hexc("#b8892f"), seed=233))
DX, AX = 490, 240          # Diogenes by his jar on the right, Alexander arrives on the left


def head_top(who, y, s):
    c = CAST[who]
    return y - (26 + c["bh"] + 2 * c["head"] - 12) * s


def laurel(cr, who, x, y, s):
    with at(cr, x, head_top(who, y, s) + 14 * s, s):
        for side in (-1, 1):
            for k in range(4):
                blob(cr, side * (12 + k * 9), 4 + k * 7, 9, 5, hexc("#5f9a3c"), seed=10 + k + side * 5, amp=0.2,
                     lw=2)
        line(cr, [(-40, 30), (-30, 6), (0, -2), (30, 6), (40, 30)], 3, GOLD_D, seed=20, amp=0.2)


def jar(cr, x, y, s=1.0):
    with at(cr, x, y, s):
        blob(cr, 0, -90, 90, 100, CLAY, seed=30, amp=0.6, lw=5)
        blob(cr, 0, -180, 50, 18, CLAY_D, seed=31, amp=0.4, lw=4)
        for k in range(3):
            line(cr, [(-70, -120 + k * 30), (70, -120 + k * 30)], 3, CLAY_D, seed=32 + k, amp=0.5)


def columns(cr):
    for k, x in enumerate((-40, 140, 580, 760)):
        shape(cr, rrect_pts(x - 34, 420, 68, 540, 4, 12), hexc("#efe4cf"), seed=40 + k, amp=0.4, lw=4)
        shape(cr, rrect_pts(x - 50, 400, 100, 30, 4, 10), hexc("#e3d6bd"), seed=45 + k, amp=0.3, lw=4)
        for f in (-14, 0, 14):
            line(cr, [(x + f, 440), (x + f, 940)], 2, hexc("#cbbd9f"), seed=50 + k * 3 + f, amp=0.2)


def sunbeam(cr, t, x, y, blocked=0.0):
    a = (0.35 + 0.08 * math.sin(t * 4)) * (1 - 0.85 * blocked)
    cr.move_to(x + 260, 200)
    cr.line_to(x - 130, y)
    cr.line_to(x + 130, y)
    cr.close_path()
    cr.set_source_rgba(*hexc("#fff3a0", a))
    cr.fill()


def alexander(cr, t, x, y=960, s=1.1, **kw):
    kw.setdefault("arms", ("hip", "hip"))
    kw.setdefault("eyes", "dot")
    kw.setdefault("mouth", "smile")
    person(cr, ALEX, x, y, t, facing=kw.pop("facing", 1), scale=s, **kw)
    laurel(cr, ALEX, x, y, s)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, (1.6, 360, 820)), (A("d1", "wanted."), (1.5, 360, 820)), (A("d1", "move."), (1.7, 420, 830))]
    bg(cr, t, keys, SKY, GROUND)
    sunbeam(cr, t, DX, 960)
    jar(cr, DX + 110, 960, 0.8)
    alexander(cr, t, AX, arms=("hip", "hip"), eyes="sly", mouth="smirk")
    person(cr, DIO, DX, 960, t, facing=-1, arms=("down", "down"), eyes="happy", mouth="grin", scale=1.05)
    hl(cr, t, [("\"ANYTHING", hexc("#b9862a")), (" you want\"", INK)], 215, 62, 0.0, end=A("d1", "poor", nth=2) - 0.05,
       bold=True, sound=False)
    hl(cr, t, [("\"Just ", INK), ("MOVE", RED), (".\"", INK)], 215, 70, A("d1", "poor", nth=2), bold=True)
    cue("hit", t, A("d1", "move."))


def scene_leader(cr, t, tl):
    A = tl.at
    keys = [(A("d2") - 0.2, (1.6, 300, 820)), (A("d2", "greece"), (1.55, 320, 810)), (A("d2", "leader."), (1.5, 360, 810))]
    bg(cr, t, keys, SKY, GROUND)
    columns(cr)
    alexander(cr, t, 300, arms=("cheer", "hip") if t >= A("d2", "leader.") else ("hip", "hip"), eyes="happy",
              mouth="grin")
    tag(cr, t, A("d2", "alexander"), 300, 600, "ALEXANDER THE GREAT", GOLD, s=0.62)
    hl(cr, t, [("the most ", INK), ("POWERFUL", hexc("#b9862a")), (" man", INK)], 215, 52, A("d2"), bold=True)


def scene_corinth(cr, t, tl):
    A = tl.at
    keys = [(A("d3") - 0.2, (1.35, 360, 800)), (A("d3", "praise"), (1.4, 360, 810))]
    bg(cr, t, keys, SKY, GROUND)
    columns(cr)
    alexander(cr, t, 250, arms=("hip", "hip"), eyes="happy", mouth="grin", s=1.05)
    for k, (who, x) in enumerate((("hilbert", 400), ("pujol", 490), ("claimant", 580))):
        bow = t >= A("d3", "praise")
        person(cr, who, x, 960, t, facing=-1, arms=("down", "down"), eyes="happy", mouth="smile", scale=0.95,
               lean=0.35 if bow else 0.0)
    tag(cr, t, A("d3", "corinth,"), 360, 600, "CORINTH", GOLD, s=0.7)
    hl(cr, t, [("everyone came to ", INK), ("PRAISE", GREEN)], 215, 58, A("d3", "important"), bold=True)


def scene_jar(cr, t, tl):
    A = tl.at
    keys = [(A("d4") - 0.2, (1.5, 360, 810)), (A("d4", "diogenes,"), (1.6, 460, 820)), (A("d5"), (1.5, 400, 810)),
            (A("d5", "sun."), (1.7, 470, 830))]
    bg(cr, t, keys, SKY, GROUND)
    sunbeam(cr, t, DX, 960)
    jar(cr, DX + 110, 960, 0.85)
    person(cr, DIO, DX, 960, t, facing=-1, arms=("hold", "down"), eyes="happy", mouth="smile", scale=1.05)
    if t >= A("d5"):
        x = lerp(-60, 170, ease_out(seg(t, A("d5"), A("d5", "find") + 0.6)))
        alexander(cr, t, x, walk=t * 1.4 if t < A("d5", "find") + 0.6 else None)
    tag(cr, t, A("d4", "diogenes,"), DX, 600, "DIOGENES", hexc("#ff8a80"), s=0.7)
    hl(cr, t, [("lived in a ", INK), ("CLAY JAR", hexc("#c46a3c"))], 215, 62, A("d4", "lived"), end=A("d5") - 0.05,
       bold=True)
    hl(cr, t, [("lying in the ", INK), ("SUN", hexc("#d8a20a"))], 215, 66, A("d5", "lying"), bold=True)


def scene_meet(cr, t, tl):
    A = tl.at
    keys = [(A("d6") - 0.2, (1.55, 370, 820)), (A("d7", "yes."), (1.8, 440, 830)), (A("d7", "sun."), (1.5, 370, 820))]
    bg(cr, t, keys, SKY, GROUND)
    blocked = ease_out(seg(t, A("d6") - 0.3, A("d6")))
    sunbeam(cr, t, DX, 960, blocked=blocked)
    if blocked > 0.2:   # Alexander's shadow falls on Diogenes
        blob(cr, DX - 10, 950, 90, 18, hexc("#000000", 0.25 * blocked), seed=70, amp=0.3, lw=0, stroke=None)
    jar(cr, DX + 110, 960, 0.85)
    alexander(cr, t, 320, arms=("give", "hip") if t < A("d7") else ("chin", "hip"),
              eyes="wide" if t >= A("d7", "stand") else "dot", mouth="smile")
    dt = tl.speaking("oldman", t)
    person(cr, DIO, DX, 960, t, facing=-1, arms=("point", "down") if t >= A("d7", "stand") else ("hold", "down"),
           eyes="sly", mouth=("o" if int(t * 12) % 2 else "smirk") if dt else "smirk", scale=1.05)
    if t >= A("d7", "stand"):
        stamp(cr, t, A("d7", "stand"), "MOVE!", dur=0.7, y=330)
    hl(cr, t, [("\"Want ", INK), ("anything", hexc("#b9862a")), ("?\"", INK)], 215, 64, A("d6"), end=A("d7") - 0.05,
       bold=True)
    hl(cr, t, [("\"Stand out of my ", INK), ("SUN", hexc("#d8a20a")), (".\"", INK)], 215, 60, A("d7", "stand"),
       bold=True)


def gold_bag(cr, x, y, s=1.0):
    with at(cr, x, y, s):
        blob(cr, 0, 0, 52, 46, GOLD, seed=80, amp=0.4, lw=4, stroke=GOLD_D)
        blob(cr, 0, -48, 22, 10, GOLD_D, seed=81, amp=0.3, lw=3)
        write(cr, [("$", GOLD_D)], 0, 18, 52, align="center", bold=True)


def land(cr, x, y, s=1.0):
    with at(cr, x, y, s):
        blob(cr, 0, 0, 64, 40, hexc("#7cc06a"), seed=82, amp=0.7, lw=4)
        line(cr, [(0, 0), (0, -80)], 5, INK, seed=83, amp=0.1)
        sharp_shape(cr, [(0, -80), (44, -66), (0, -52)], RED, seed=84, amp=0.2, lw=3)


def crown_icon(cr, x, y, s=1.0):
    with at(cr, x, y, s):
        sharp_shape(cr, [(-50, 30), (-50, -24), (-24, 4), (0, -36), (24, 4), (50, -24), (50, 30)], GOLD, seed=85,
                    amp=0.3, lw=4)


def cross(cr, t, start, x, y, r=70):
    if t < start:
        return
    u = ease_out(seg(t, start, start + 0.25))
    line(cr, [(x - r, y - r), (x - r + 2 * r * u, y - r + 2 * r * u)], 12, RED, seed=86, amp=0.3)
    if u > 0.5:
        v = (u - 0.5) * 2
        line(cr, [(x + r, y - r), (x + r - 2 * r * v, y - r + 2 * r * v)], 12, RED, seed=87, amp=0.3)


OFFERS = ((gold_bag, 190, "gold."), (land, 360, "land."), (crown_icon, 530, "power."))


def scene_offer(cr, t, tl):
    A = tl.at
    keys = [(A("d8") - 0.2, (1.5, 360, 800)), (A("d9"), (1.5, 360, 805))]
    bg(cr, t, keys, SKY, GROUND)
    alexander(cr, t, 190, s=1.0, arms=("give", "hip"), eyes="happy", mouth="grin")
    person(cr, DIO, 530, 960, t, facing=-1, arms=("hip", "hip") if t >= A("d9") else ("down", "down"), eyes="sly",
           mouth="flat" if t >= A("d9") else "smile", scale=0.9)
    for k, (icon, x, key) in enumerate(OFFERS):
        st = A("d8", key)
        if t >= st:
            icon(cr, x, 610, max(0.6, pop(t, st, 0.3)) * 0.95)
            cross(cr, t, A("d9", "want") + k * 0.15, x, 610, r=60)
    hl(cr, t, [("why so ", INK), ("CLEVER", GREEN), ("?", INK)], 215, 70, A("d8"), end=A("d8", "gold.") - 0.05,
       bold=True)
    hl(cr, t, [("gold, land, ", hexc("#b9862a")), ("power", RED)], 215, 66, A("d8", "gold."), end=A("d9") - 0.05,
       bold=True)
    hl(cr, t, [("he wanted ", INK), ("NONE", RED), (" of it", INK)], 215, 66, A("d9"), bold=True)
    cue("hit", t, A("d9", "want"))


def cup(cr, x, y, s=1.0, rot=0.0):
    with at(cr, x, y, s, rot=rot):
        shape(cr, [(-26, -30), (26, -30), (18, 24), (-18, 24)], CLAY, seed=88, amp=0.3, lw=4)
        blob(cr, 32, -6, 12, 16, CLAY_D, seed=89, amp=0.2, lw=4)


def scene_cup(cr, t, tl):
    A = tl.at
    keys = [(A("d10") - 0.2, (1.3, 400, 790)), (A("d10", "threw"), (1.3, 420, 790))]
    bg(cr, t, keys, SKY, GROUND)
    # a fountain on the left, a boy drinking from his cupped hands
    shape(cr, rrect_pts(150, 860, 150, 100, 14, 12), hexc("#cfd6dc"), seed=90, amp=0.4, lw=4)
    blob(cr, 225, 862, 64, 12, hexc("#7fc4ef"), seed=91, amp=0.3, lw=3)
    line(cr, [(225, 780), (225, 860)], 6, hexc("#7fc4ef"), seed=92, amp=0.6)
    if t >= A("d10", "boy"):
        person(cr, "kid_b", 340, 960, t, facing=-1, arms=("face", "face"), eyes="happy", mouth="smile", scale=0.95)
    throw = A("d10", "threw")
    dio_arms = ("hold", "down") if t < throw else ("cheer", "down")
    person(cr, DIO, 570, 960, t, facing=-1, arms=dio_arms, eyes="wide" if A("d10", "hands.") <= t < throw else "happy",
           mouth="o" if A("d10", "hands.") <= t < throw else "grin", scale=1.05)
    if t < throw:
        cup(cr, 532, 862, 0.8)
    else:
        u = ease_out(seg(t, throw, throw + 0.8))
        cup(cr, lerp(540, 820, u), 760 - 260 * math.sin(u * math.pi * 0.8), 0.8, rot=u * 6)
    tag(cr, t, A("d10", "only"), 520, 640, "HIS ONLY CUP", hexc("#ff8a80"), s=0.6)
    hl(cr, t, [("drinking from his ", INK), ("HANDS", GREEN)], 215, 58, A("d10", "boy"), end=throw - 0.05, bold=True)
    hl(cr, t, [("so he threw away his ", INK), ("CUP", RED)], 215, 58, throw, bold=True)
    cue("whoosh", t, throw)


def meter(cr, t, x, y, level, label):
    with at(cr, x, y, 1.0):
        shape(cr, rrect_pts(-220, -34, 440, 68, 30, 12), WHITE, seed=93, amp=0.3, lw=4)
        if level > 0.01:
            shape(cr, rrect_pts(-210, -24, 420 * level, 48, 22, 10), RED, seed=94, amp=0.2, lw=0, stroke=None)
        write(cr, [(label, INK)], 0, -54, 34, align="center", bold=True)


def scene_nothing(cr, t, tl):
    A = tl.at
    keys = [(A("d11") - 0.2, (1.35, 360, 790)), (A("d12"), (1.35, 360, 790))]
    bg(cr, t, keys, SKY, GROUND)
    moved = t >= A("d11", "step")
    ax = 330 if not moved else lerp(330, 210, ease_out(seg(t, A("d11", "step"), A("d11", "step") + 0.6)))
    sunbeam(cr, t, DX, 960, blocked=0.0 if moved else 1.0)
    jar(cr, DX + 110, 960, 0.85)
    alexander(cr, t, ax, arms=("hold", "hip") if not moved else ("hip", "hip"), eyes="sad" if not moved else "dot",
              mouth="flat")
    if not moved:
        gold_bag(cr, ax + 70, 860, 0.55)
    person(cr, DIO, DX, 960, t, facing=-1, arms=("down", "down"), eyes="happy", mouth="grin", scale=1.05)
    level = 1.0 - ease_out(seg(t, A("d12", "buy"), A("d12", "control")))
    if t >= A("d12"):
        meter(cr, t, 360, 570, level, "POWER OVER HIM")
    if t >= A("d12", "buy"):
        tag(cr, t, A("d12", "buy"), 230, 660, "CAN'T BUY", GREEN, s=0.6)
    if t >= A("d12", "control"):
        tag(cr, t, A("d12", "control"), 485, 660, "CAN'T CONTROL", GREEN, s=0.6, seed=61)
    hl(cr, t, [("nothing to ", INK), ("OFFER", RED)], 215, 66, A("d11"), end=A("d12") - 0.05, bold=True)
    hl(cr, t, [("needs ", INK), ("NOTHING", GREEN), (" from you?", INK)], 215, 58, A("d12", "if"), bold=True)
    cue("hit", t, A("d12", "control"))


def scene_laugh(cr, t, tl):
    A = tl.at
    keys = [(A("d13") - 0.2, (1.45, 330, 820)), (A("d13", "if"), (1.6, 300, 830))]
    bg(cr, t, keys, SKY, GROUND)
    sunbeam(cr, t, DX, 960)
    jar(cr, DX + 110, 960, 0.85)
    for who, x in (("rocker_a", 40), ("rocker_b", 120)):
        person(cr, who, x, 960, t, facing=1, arms=("hip", "hip"), eyes="happy", mouth="grin", scale=0.95,
               shake=1.0 if t < A("d13", "but") else 0)
    talk = tl.speaking("alexander", t)
    alexander(cr, t, 250, arms=("chin", "hip") if t < A("d13", "if") else ("point", "hip"), eyes="dot",
              mouth=("o" if int(t * 12) % 2 else "smile") if talk else "smile")
    person(cr, DIO, DX, 960, t, facing=-1, arms=("down", "down"), eyes="happy", mouth="grin", scale=1.05)
    tag(cr, t, A("d13", "if"), 330, 600, "PLUTARCH, LIFE OF ALEXANDER", hexc("#ffe6a0"), s=0.4, seed=62)
    hl(cr, t, [("Alexander ", INK), ("understood", GREEN)], 215, 62, A("d13", "but"), end=A("d13", "if") - 0.05,
       bold=True)
    hl(cr, t, [("\"I would be ", INK), ("DIOGENES", RED), (".\"", INK)], 215, 58, A("d13", "if"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("d14") - 0.2, (1.5, 360, 820)), (A("d14", "everything,"), (1.75, 260, 830)),
            (A("d14", "needed"), (1.75, 470, 830)), (A("d14", "nothing?", end=True), (1.45, 365, 820))]
    bg(cr, t, keys, SKY, GROUND)
    sunbeam(cr, t, DX, 960)
    jar(cr, DX + 110, 960, 0.85)
    alexander(cr, t, AX, arms=("hip", "hip"), eyes="sly", mouth="smirk")
    person(cr, DIO, DX, 960, t, facing=-1, arms=("down", "down"), eyes="happy", mouth="grin", scale=1.05)
    buttons(cr, t, A("d14", "nothing?"), (("ALEXANDER", hexc("#b9862a")), ("DIOGENES", RED)), y=1060, s=0.62)
    hl(cr, t, [("who was ", INK), ("RICHER", GREEN), ("?", INK)], 215, 70, A("d14", "who"), bold=True, underline=True)
    stamp(cr, t, A("d14", "nothing?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "leader": scene_leader, "corinth": scene_corinth, "jar": scene_jar, "meet": scene_meet,
     "offer": scene_offer, "cup": scene_cup, "nothing": scene_nothing, "laugh": scene_laugh, "end": scene_end}[name](
        cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
