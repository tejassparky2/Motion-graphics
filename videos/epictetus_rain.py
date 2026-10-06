"""Clever words from history: Epictetus, "It's not things that upset us, it's what we think about them."

Epictetus (c. AD 50-135) was born a slave in Hierapolis, was later freed, and taught philosophy (Stoicism). His pupil
Arrian wrote down his teaching; Enchiridion 5: "Men are disturbed not by things, but by the opinions about things"
(also translated "It is not things that disturb us, but our judgements about things"). Marcus Aurelius, Meditations
1.7, thanks his teacher Rusticus for making him acquainted with the discourses of Epictetus, lent from Rusticus's own
collection. The rain example (a wedding vs a dry farm) is ours, to show the idea.
"""
import math

from motion.captions import captions
from motion.characters import CAST, bubble, person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import hl, stamp, whip
from motion.story import BLUE, CLOSE, GREEN, bg, buttons, card, head_c, scroll, tag, talk

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="e1", scene="hook", text="A man born a slave had one idea. And an emperor of Rome learned from it."),
    dict(id="e2", scene="intro", text="His name was Epictetus. He was born a slave, almost two thousand years ago. "
                                      "Later he was freed, and became a teacher."),
    dict(id="e3", scene="idea", text="He taught this: It's not things that upset us. It's what we think about them.",
         speaker="epictetus", speaker_from="it's"),
    dict(id="e4", scene="rain", text="Sounds strange? Here's an example. It starts to rain."),
    dict(id="e5", scene="rain", text="A bride on her wedding day thinks: My day is ruined. She cries."),
    dict(id="e6", scene="rain", text="A farmer with dry fields thinks: Finally! He dances."),
    dict(id="e7", scene="rain", text="Same rain. The rain didn't decide how they feel. Their thoughts did."),
    dict(id="e8", scene="choose", text="So you can't always choose what happens. But you can choose how you see it."),
    dict(id="e9", scene="emperor", text="The emperor Marcus Aurelius thanked a teacher, for giving him the lessons of "
                                        "Epictetus to read."),
    dict(id="e10", scene="end", text="So what do you think? Do you control your feelings? Or do they control you?",
         pace=0.95),
]

METADATA = dict(
    title="A Slave Said ONE Sentence… and a Roman Emperor Studied It 🌧️",
    alt_titles=["It's Not Things That Upset You (Epictetus) 🧠", "Same Rain, Two Feelings: The Idea That Changes Everything 🌧️"],
    description="""A man born a slave had one idea. And an emperor of Rome learned from it. 🧠

Epictetus was born a slave almost 2,000 years ago. Later he was freed and became a teacher. He taught: "It's not things that upset us. It's what we think about them."

Example: it starts to rain. A bride on her wedding day thinks "My day is ruined" and cries. A farmer with dry fields thinks "Finally!" and dances. Same rain. The rain didn't decide how they feel; their thoughts did. So you can't always choose what happens, but you can choose how you see it.

The emperor Marcus Aurelius thanked a teacher for giving him the lessons of Epictetus to read.

Sources: Epictetus, Enchiridion 5; Marcus Aurelius, Meditations 1.7.

💬 So what do you think? Do you control your feelings, or do they control you? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Stoicism", "#Epictetus", "#Philosophy"],
    tags=["epictetus", "stoicism", "stoic philosophy", "marcus aurelius", "mindset", "philosophy explained",
          "enchiridion", "ancient wisdom", "history facts", "interestingly strange"],
    pinned_comment="Do YOU control your feelings, or do they control you? Be honest 👇🌧️",
)

SKY, GROUND = hexc("#f4e6cc"), hexc("#d4bc90")
GOLD, GOLD_D = hexc("#f2c14e"), hexc("#b9862a")
EPI, MARCUS = "epictetus", "marcus"
CAST.setdefault(EPI, dict(skin=hexc("#d9a173"), shirt=hexc("#9a7a52"), pants=hexc("#6b5a45"), bw=94, bh=104,
                          head=40, kind="robe", hair="scruffy", hair_col=hexc("#4a3a2a"), beard=hexc("#4a3a2a"),
                          seed=281))
CAST.setdefault(MARCUS, dict(skin=hexc("#f0c29c"), shirt=hexc("#6b2d7a"), pants=hexc("#6b2d7a"), bw=98, bh=112,
                             head=40, kind="robe", hair="messy", hair_col=hexc("#8a6a3a"), beard=hexc("#8a6a3a"),
                             seed=283))
CAST.setdefault("bride", dict(skin=hexc("#f0c29c"), shirt=hexc("#fbfbf7"), pants=hexc("#f0c29c"), bw=82, bh=112,
                              head=38, kind="dress", hair="long", hair_col=hexc("#5a2e1c"), lashes=True, blush=True,
                              seed=285))


def laurel(cr, who, x, y, s):
    hx, hy = head_c(who, x, y, s)
    with at(cr, hx, hy - 30 * s, s):
        for side in (-1, 1):
            for k in range(4):
                blob(cr, side * (12 + k * 9), 4 + k * 7, 9, 5, hexc("#5f9a3c"), seed=10 + k + side * 5, amp=0.2, lw=2)


def chains(cr, x, y, broken=0.0):
    for side in (-1, 1):
        for k in range(4):
            dx = side * (20 + k * 22) + (side * broken * 40 * k)
            blob(cr, x + dx, y + broken * k * 10, 12, 8, hexc("#8d939c"), seed=20 + k, amp=0.2, lw=3)


def epictetus(cr, t, tl, x, y=960, s=1.1, **kw):
    kw.setdefault("arms", ("hip", "hip"))
    kw.setdefault("eyes", "dot")
    person(cr, EPI, x, y, t, facing=kw.pop("facing", 1), scale=s, mouth=talk(tl, EPI, t, kw.pop("mouth", "smile")),
           **kw)


def marcus(cr, t, x, y=960, s=1.1, **kw):
    kw.setdefault("arms", ("hold", "hip"))
    person(cr, MARCUS, x, y, t, facing=kw.pop("facing", -1), scale=s, **kw)
    laurel(cr, MARCUS, x, y, s)


def book(cr, x, y, s=1.0):
    with at(cr, x, y, s, rot=-0.1):
        shape(cr, rrect_pts(-46, -34, 92, 68, 6, 10), hexc("#f4e4bc"), seed=30, amp=0.4, lw=4)
        for k in range(3):
            line(cr, [(-32, -14 + k * 14), (32, -14 + k * 14)], 3, hexc("#8a7a5a"), seed=31 + k, amp=0.3)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, CLOSE), (A("e1", "emperor"), (1.5, 400, 800))]
    bg(cr, t, keys, SKY, GROUND)
    epictetus(cr, t, tl, 250, arms=("down", "down"), eyes="sly", mouth="smile")
    chains(cr, 250, 905)
    if t >= A("e1", "emperor"):
        marcus(cr, t, 520, arms=("hold", "hip"), eyes="wide", mouth="o")
        book(cr, 470, 820, 0.8)
    hl(cr, t, [("born a ", INK), ("SLAVE", RED)], 215, 70, 0.0, end=A("e1", "emperor") - 0.05, bold=True, sound=False)
    hl(cr, t, [("an ", INK), ("EMPEROR", hexc("#6b2d7a")), (" learned from him", INK)], 215, 52, A("e1", "emperor"),
       bold=True)
    cue("hit", t, A("e1", "emperor"))


def scene_intro(cr, t, tl):
    A = tl.at
    keys = [(A("e2") - 0.2, CLOSE), (A("e2", "freed,"), (1.4, 360, 790))]
    bg(cr, t, keys, SKY, GROUND)
    freed = ease_out(seg(t, A("e2", "freed,"), A("e2", "freed,") + 0.5))
    teach = t >= A("e2", "teacher.")
    if teach:
        for k, (who, x) in enumerate((("kid_b", 520), ("kid_c", 610))):
            person(cr, who, x, 960, t, facing=-1, arms=("down", "down"), eyes="happy", mouth="smile", scale=0.8)
    epictetus(cr, t, tl, 300 if not teach else 260, arms=("cheer", "cheer") if 0 < freed < 1 or (freed >= 1 and not
              teach) else (("point", "hip") if teach else ("down", "down")), eyes="happy" if freed > 0 else "sad",
              mouth="grin" if freed > 0 else "flat")
    if freed < 1:
        chains(cr, 300, 905, broken=freed)
    tag(cr, t, A("e2", "epictetus."), 330, 560, "EPICTETUS", GOLD, s=0.7)
    if A("e2", "slave,") <= t < A("e2", "freed,"):
        tag(cr, t, A("e2", "slave,"), 330, 650, "BORN A SLAVE", hexc("#ffb3a8"), s=0.6, seed=61)
    if t >= A("e2", "freed,"):
        tag(cr, t, A("e2", "freed,"), 330, 650, "FREED" if not teach else "TEACHER", GREEN, s=0.6, seed=62)
    hl(cr, t, [("almost ", INK), ("2,000", RED), (" years ago", INK)], 215, 62, A("e2", "almost"), bold=True)


def scene_idea(cr, t, tl):
    A = tl.at
    keys = [(A("e3") - 0.2, (1.0, 360, 640))]
    bg(cr, t, keys, SKY)
    lines = [([("It's not ", INK), ("THINGS", RED)], A("e3", "it's")),
             ([("that upset us.", INK)], A("e3", "upset")),
             ([("It's what we ", INK), ("THINK", GREEN)], A("e3", "it's", nth=2)),
             ([("about them.", INK)], A("e3", "about"))]
    scroll(cr, t, lines, 360, 450, 1.0, size=54, gap=76, w=620)
    epictetus(cr, t, tl, 360, y=860, s=1.0, arms=("point", "hip"), eyes="dot")
    hl(cr, t, [("his big ", INK), ("IDEA", GREEN)], 215, 70, A("e3"), bold=True)
    cue("hit", t, A("e3", "think"))


def cloud(cr, t, x, y, s=1.0):
    with at(cr, x, y, s):
        for k, (dx, dy, r) in enumerate(((-90, 10, 60), (-20, -20, 80), (70, 0, 65), (130, 20, 45), (-150, 25, 40))):
            blob(cr, dx, dy, r, r * 0.8, hexc("#8f9aa8"), seed=40 + k, amp=0.6, lw=4)
        for k in range(12):
            dx = -170 + k * 30
            ph = (t * 1.6 + k * 0.37) % 1.0
            line(cr, [(dx, 60 + ph * 520), (dx - 6, 84 + ph * 520)], 4, hexc("#5aa9d6"), seed=50 + k, amp=0.1)


def scene_rain(cr, t, tl):
    A = tl.at
    keys = [(A("e4") - 0.2, (1.0, 360, 640))]
    bg(cr, t, keys, hexc("#dfe6ec"))
    rain = t >= A("e4", "rain.")
    # left: wedding (an arch with flowers); right: a dry field
    shape(cr, rrect_pts(-20, 860, 380, 420, 0, 14), hexc("#cfe3c4"), seed=60, amp=0.3, lw=0, stroke=None)
    shape(cr, rrect_pts(360, 860, 380, 420, 0, 14), hexc("#d9b77a") if t < A("e6", "dances.") else hexc("#a7c46a"),
          seed=61, amp=0.3, lw=0, stroke=None)
    line(cr, [(360, 300), (360, 1280)], 5, INK, seed=62, amp=0.3)
    for k in range(4):
        line(cr, [(420 + k * 80, 900), (440 + k * 80, 880)], 4, hexc("#8a6a2a"), seed=63 + k, amp=0.4)
    if rain:
        with at(cr, 0, 0, 1.0):
            cloud(cr, t, 180, 300, 0.85)
            cloud(cr, t, 540, 300, 0.85)
    sad = t >= A("e5", "ruined.")
    person(cr, "bride", 180, 880, t, facing=1, arms=("face", "face") if sad else ("down", "down"),
           eyes="sad" if sad else "happy", mouth="sad" if sad else "smile", tears=sad, scale=1.2)
    happy = t >= A("e6", "finally!")
    person(cr, "farmer", 540, 880, t, facing=-1, arms=("cheer", "cheer") if happy else ("hip", "hip"),
           eyes="happy" if happy else "sad", mouth="grin" if happy else "flat", scale=1.2,
           jump=abs(math.sin(t * 8)) * 26 if t >= A("e6", "dances.") else 0)
    if t >= A("e5", "thinks:"):
        bubble(cr, 180, 480, 320, 120, (180, 580), [("My day is ", INK), ("RUINED", RED)], s=1.0, size=34,
               thought=True, lines=[[("My day is", INK)], [("RUINED", RED)]])
    if t >= A("e6", "thinks:"):
        bubble(cr, 540, 480, 280, 120, (540, 580), [("FINALLY!", GREEN)], s=1.0, size=48, thought=True)
    hl(cr, t, [("it starts to ", INK), ("RAIN", BLUE)], 215, 66, A("e4", "here's"), end=A("e5") - 0.05, bold=True)
    hl(cr, t, [("a ", INK), ("BRIDE", RED), ("...", INK)], 215, 70, A("e5"), end=A("e6") - 0.05, bold=True)
    hl(cr, t, [("a ", INK), ("FARMER", GREEN), ("...", INK)], 215, 70, A("e6"), end=A("e7") - 0.05, bold=True)
    hl(cr, t, [("SAME", BLUE), (" rain", INK)], 215, 74, A("e7"), end=A("e7", "rain", nth=2) - 0.05, bold=True)
    hl(cr, t, [("their ", INK), ("THOUGHTS", GREEN), (" decided", INK)], 215, 60, A("e7", "rain", nth=2), bold=True)
    hl(cr, t, [("sounds ", INK), ("STRANGE", RED), ("?", INK)], 215, 70, A("e4"), end=A("e4", "here's") - 0.05,
       bold=True)
    cue("hit", t, A("e7"))


def scene_choose(cr, t, tl):
    A = tl.at
    keys = [(A("e8") - 0.2, (1.0, 360, 640))]
    bg(cr, t, keys, SKY)
    card(cr, t, A("e8"), 360, 430, 0.95, "what happens:", "NOT YOUR CHOICE", top_col=INK, bottom_col=RED,
         seed=70, w=560)
    card(cr, t, A("e8", "but"), 360, 680, 0.95, "how you see it:", "YOUR CHOICE", top_col=INK, bottom_col=GREEN,
         seed=71, w=560)
    hl(cr, t, [("you ", INK), ("CHOOSE", GREEN)], 215, 70, A("e8", "but"), bold=True)
    cue("hit", t, A("e8", "but"))


def scene_emperor(cr, t, tl):
    A = tl.at
    keys = [(A("e9") - 0.2, CLOSE), (A("e9", "lessons"), (1.5, 380, 800))]
    bg(cr, t, keys, SKY, GROUND)
    person(cr, "hilbert", 230, 960, t, facing=1, arms=("give", "hip"), eyes="happy", mouth="smile", scale=1.0)
    marcus(cr, t, 470, arms=("hold", "hip"), eyes="happy" if t >= A("e9", "lessons") else "dot", mouth="smile")
    book(cr, 400 if t >= A("e9", "giving") else 300, 820, 0.8)
    tag(cr, t, A("e9", "marcus"), 380, 570, "MARCUS AURELIUS", GOLD, s=0.55)
    tag(cr, t, A("e9", "emperor"), 380, 640, "ROMAN EMPEROR", hexc("#d9b3ff"), s=0.48, seed=63)
    hl(cr, t, [("an emperor's ", INK), ("THANKS", GREEN)], 215, 62, A("e9"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("e10") - 0.2, CLOSE)]
    bg(cr, t, keys, SKY, GROUND)
    epictetus(cr, t, tl, 360, arms=("chin", "hip"), eyes="sly", mouth="smirk")
    buttons(cr, t, A("e10", "feelings?"), (("I DO", GREEN), ("THEY DO", RED)), y=1060, s=0.75)
    hl(cr, t, [("who's in ", INK), ("CONTROL", RED), ("?", INK)], 215, 66, A("e10", "do"), bold=True, underline=True)
    stamp(cr, t, A("e10", "you?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "intro": scene_intro, "idea": scene_idea, "rain": scene_rain, "choose": scene_choose,
     "emperor": scene_emperor, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
