"""Clever words from history: Diogenes and Alexander the Great (Plutarch, Life of Alexander, ch. 14).

At Corinth (c. 336 BC), after the Greeks chose the young Alexander as their leader, statesmen and philosophers came
to congratulate him; Diogenes of Sinope did not. Alexander went to him and found him lying in the sun; asked whether he
wanted anything, Diogenes said "Yes, stand a little out of my sun." Alexander's followers laughed and jeered, but he
said: "But verily, if I were not Alexander, I would be Diogenes." (Perrin translation.) Diogenes was famous for living
in a large clay jar (a pithos), often called a "barrel" in retellings. Structure follows the owner's Napoleon
reference.
"""
import math

from motion.captions import captions
from motion.characters import CAST, person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    write
from motion.kit import hl, stamp, whip
from motion.story import CLOSE, GREEN, bg, buttons, scroll, tag

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="d1", scene="hook", text="The most powerful man in the world met a man who owned almost nothing. And the "
                                     "poor man won."),
    dict(id="d2", scene="leader", text="The powerful man was Alexander the Great. He was about twenty, and Greece had "
                                       "just made him its leader."),
    dict(id="d3", scene="corinth", text="In the city of Corinth, crowds of important people came to praise him."),
    dict(id="d4", scene="jar", text="But one man didn't come. Diogenes, a philosopher who lived in a big clay jar."),
    dict(id="d5", scene="jar", text="So Alexander went to find him. Diogenes was lying in the sun."),
    dict(id="d6", scene="meet", text="Alexander asked if he wanted anything at all."),
    dict(id="d7", scene="meet", text="Diogenes said: Yes. Stand a little out of my sun.", speaker="oldman",
         speaker_from="yes.", pace=0.9),
    dict(id="d8", scene="meet", text="Alexander's men laughed at him. But Alexander said: if I were not Alexander, I "
                                     "would be Diogenes.", speaker="alexander", speaker_from="if", gap=0.3),
    dict(id="d9", scene="plutarch", text="That story comes from the Greek writer, Plutarch."),
    dict(id="d10", scene="end", text="So what do you think? Who was really richer? The man who had everything, or the "
                                     "man who wanted nothing?", pace=0.95),
]

METADATA = dict(
    title="Alexander the Great Offered Him Anything… His Answer Was Genius ☀️",
    alt_titles=["The Man Who Told Alexander the Great to Move 😳", "Who Was Richer: Alexander or Diogenes? ☀️"],
    description="""The most powerful man in the world met a man who owned almost nothing. And the poor man won. ☀️

Alexander the Great was about 20, and Greece had just made him its leader. In Corinth, crowds of important people came to praise him, but the philosopher Diogenes, who lived in a big clay jar, didn't come. So Alexander went to find him, lying in the sun, and asked if he wanted anything at all.

Diogenes said: "Yes. Stand a little out of my sun."

Alexander's men laughed, but Alexander said: "If I were not Alexander, I would be Diogenes."

Source: Plutarch, Life of Alexander, chapter 14.

💬 So what do you think? Who was really richer: the man who had everything, or the man who wanted nothing? 👇

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
    keys = [(0, (1.6, 360, 820)), (A("d1", "nothing."), (1.5, 360, 820)), (A("d1", "won."), (1.7, 420, 830))]
    bg(cr, t, keys, SKY, GROUND)
    sunbeam(cr, t, DX, 960)
    jar(cr, DX + 110, 960, 0.8)
    alexander(cr, t, AX, arms=("hip", "hip"), eyes="sly", mouth="smirk")
    person(cr, DIO, DX, 960, t, facing=-1, arms=("down", "down"), eyes="happy", mouth="grin", scale=1.05)
    hl(cr, t, [("EVERYTHING", hexc("#b9862a")), (" vs ", INK), ("NOTHING", RED)], 215, 62, 0.0, bold=True,
       sound=False)
    cue("hit", t, A("d1", "won."))


def scene_leader(cr, t, tl):
    A = tl.at
    keys = [(A("d2") - 0.2, (1.6, 300, 820)), (A("d2", "twenty,"), (1.55, 320, 810)), (A("d2", "leader."), (1.5, 360, 810))]
    bg(cr, t, keys, SKY, GROUND)
    columns(cr)
    alexander(cr, t, 300, arms=("cheer", "hip") if t >= A("d2", "leader.") else ("hip", "hip"), eyes="happy",
              mouth="grin")
    tag(cr, t, A("d2", "alexander"), 300, 600, "ALEXANDER THE GREAT", GOLD, s=0.62)
    tag(cr, t, A("d2", "twenty,"), 470, 720, "AGE ~20", hexc("#7ee08a"), s=0.6, seed=61)
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
    hl(cr, t, [("everyone came to ", INK), ("PRAISE", GREEN)], 215, 58, A("d3", "crowds"), bold=True)


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
    keys = [(A("d6") - 0.2, (1.55, 370, 820)), (A("d7", "yes."), (1.8, 440, 830)), (A("d7", "sun."), (1.5, 370, 820)),
            (A("d8", "laughed"), (1.45, 330, 820)), (A("d8", "if"), (1.8, 300, 830))]
    bg(cr, t, keys, SKY, GROUND)
    moved = t >= A("d8")
    ax = 320 if not moved else lerp(320, 230, ease_out(seg(t, A("d8"), A("d8") + 0.5)))
    blocked = 0.0 if moved else ease_out(seg(t, A("d6") - 0.3, A("d6")))
    sunbeam(cr, t, DX, 960, blocked=blocked)
    if blocked > 0.2:   # Alexander's shadow falls on Diogenes
        blob(cr, DX - 10, 950, 90, 18, hexc("#000000", 0.25 * blocked), seed=70, amp=0.3, lw=0, stroke=None)
    jar(cr, DX + 110, 960, 0.85)
    if moved:   # his men, laughing
        for k, (who, x) in enumerate((("rocker_a", 40), ("rocker_b", 120))):
            person(cr, who, x, 960, t, facing=1, arms=("hip", "hip"), eyes="happy", mouth="grin", scale=0.95,
                   shake=1.0 if t < A("d8", "but") else 0)
    talk = tl.speaking("alexander", t)
    alexander(cr, t, ax, arms=("point", "hip") if t < A("d7") else ("chin", "hip"),
              eyes="wide" if A("d7", "stand") <= t < A("d8") else "dot",
              mouth=("o" if int(t * 12) % 2 else "smile") if talk else "smile")
    dt = tl.speaking("oldman", t)
    person(cr, DIO, DX, 960, t, facing=-1, arms=("point", "down") if t >= A("d7", "stand") else ("hold", "down"),
           eyes="sly", mouth=("o" if int(t * 12) % 2 else "smirk") if dt else "smirk", scale=1.05)
    if A("d7", "stand") <= t < A("d8"):
        stamp(cr, t, A("d7", "stand"), "MOVE!", dur=0.7, y=330)
    hl(cr, t, [("\"Want ", INK), ("anything", hexc("#b9862a")), ("?\"", INK)], 215, 64, A("d6"), end=A("d7") - 0.05,
       bold=True)
    hl(cr, t, [("\"Stand out of my ", INK), ("SUN", hexc("#d8a20a")), (".\"", INK)], 215, 60, A("d7", "stand"),
       end=A("d8", "if") - 0.05, bold=True)
    hl(cr, t, [("\"I would be ", INK), ("DIOGENES", RED), (".\"", INK)], 215, 58, A("d8", "if"), bold=True)


def scene_plutarch(cr, t, tl):
    A = tl.at
    keys = [(A("d9") - 0.2, (1.0, 360, 640))]
    bg(cr, t, keys, SKY, GROUND)
    lines = [([("PLUTARCH", RED)], A("d9")), ([("Life of Alexander", INK)], A("d9", "plutarch")),
             ([("chapter 14", INK)], A("d9", "plutarch") + 0.3)]
    scroll(cr, t, lines, 360, 560, 1.0, size=48, gap=70)
    hl(cr, t, [("the ", INK), ("source", GREEN)], 215, 66, A("d9"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("d10") - 0.2, (1.5, 360, 820)), (A("d10", "everything,"), (1.75, 260, 830)),
            (A("d10", "wanted"), (1.75, 470, 830)), (A("d10", "nothing?", end=True), (1.45, 365, 820))]
    bg(cr, t, keys, SKY, GROUND)
    sunbeam(cr, t, DX, 960)
    jar(cr, DX + 110, 960, 0.85)
    alexander(cr, t, AX, arms=("hip", "hip"), eyes="sly", mouth="smirk")
    person(cr, DIO, DX, 960, t, facing=-1, arms=("down", "down"), eyes="happy", mouth="grin", scale=1.05)
    buttons(cr, t, A("d10", "nothing?"), (("ALEXANDER", hexc("#b9862a")), ("DIOGENES", RED)), y=1060, s=0.62)
    hl(cr, t, [("who was ", INK), ("RICHER", GREEN), ("?", INK)], 215, 70, A("d10", "who"), bold=True, underline=True)
    stamp(cr, t, A("d10", "nothing?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "leader": scene_leader, "corinth": scene_corinth, "jar": scene_jar, "meet": scene_meet,
     "plutarch": scene_plutarch, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
