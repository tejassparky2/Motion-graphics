"""Clever words from history: Socrates, "I know that I don't know" (often summed up as "I know that I know nothing").

Plato, Apology 21a-22e: Socrates' friend Chaerephon asked the oracle at Delphi whether anyone was wiser than Socrates,
and the priestess answered that no one was. Socrates, aware he was not wise, set out to test it: he questioned a
politician with a name for wisdom, then poets, then craftsmen. Each thought he knew more than he did. About the
politician he concluded (Grube translation): "I am wiser than this man; it is likely that neither of us knows
anything worthwhile, but he thinks he knows something when he does not, whereas when I do not know, neither do I
think I know." The craftsmen did know their crafts, but thought that made them wise in other big matters too. The two
students before a test are our own example of the idea.
"""
import math

from motion.captions import captions
from motion.characters import CAST, bubble, person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import hl, stamp, whip
from motion.story import BLUE, CLOSE, GREEN, bg, buttons, card, scroll, tag, talk

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="s1", scene="hook", text="The wisest man in Athens said he knew nothing. And that's exactly why he was "
                                     "the wisest."),
    dict(id="s2", scene="oracle", text="About two thousand four hundred years ago, a friend of Socrates asked the "
                                       "famous oracle of Delphi: Is anyone wiser than Socrates?"),
    dict(id="s3", scene="oracle", text="The answer was: No one."),
    dict(id="s4", scene="test", text="Socrates was confused. He knew he wasn't wise. So he went to test it."),
    dict(id="s5", scene="test", text="He questioned a famous politician. Then poets. Then craftsmen. People everyone "
                                     "called wise."),
    dict(id="s6", scene="test", text="Each one thought he knew more than he really did. When Socrates asked simple "
                                     "questions, they couldn't explain."),
    dict(id="s7", scene="realize", text="Then Socrates understood. He said: This man thinks he knows, when he "
                                        "doesn't. I don't know, and I don't think I do.", speaker="socrates",
         speaker_from="this"),
    dict(id="s8", scene="students", text="Here's an example. Two students have a test tomorrow."),
    dict(id="s9", scene="students", text="The first one thinks he knows everything. So he doesn't study."),
    dict(id="s10", scene="students", text="The second one knows what he doesn't know. So he studies exactly that."),
    dict(id="s11", scene="students", text="Who passes? The one who knew what he didn't know."),
    dict(id="s12", scene="end", text="So what do you think? Is it smart to say: I don't know?", pace=0.95),
]

METADATA = dict(
    title="The Wisest Man Said \"I Know Nothing\"… and That's WHY He Was Wise 🧠",
    alt_titles=["\"I Know That I Know Nothing\" Explained in 50 Seconds 🧠", "The Oracle Said He Was the Wisest. He Tried to Prove It Wrong 😳"],
    description="""The wisest man in Athens said he knew nothing. And that's exactly why he was the wisest. 🧠

About 2,400 years ago, a friend of Socrates asked the oracle of Delphi: "Is anyone wiser than Socrates?" The answer: no one. Socrates was confused, because he knew he wasn't wise. So he tested it: he questioned a famous politician, then poets, then craftsmen. Each one thought he knew more than he really did, and when Socrates asked simple questions, they couldn't explain.

Then he understood: "This man thinks he knows, when he doesn't. I don't know, and I don't think I do."

Example: two students have a test tomorrow. The first thinks he knows everything, so he doesn't study. The second knows what he doesn't know, so he studies exactly that. Who passes? The one who knew what he didn't know.

Source: Plato, Apology 21-22. Often summed up as "I know that I know nothing."

💬 So what do you think? Is it smart to say "I don't know"? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Socrates", "#Philosophy", "#Wisdom"],
    tags=["socrates", "i know that i know nothing", "socratic paradox", "oracle of delphi", "plato apology",
          "philosophy explained", "ancient greece", "wisdom", "history facts", "interestingly strange"],
    pinned_comment="Is saying \"I don't know\" smart or weak? Defend your answer 👇🧠",
)

SKY, GROUND = hexc("#f5e7cb"), hexc("#d6bd92")
GOLD, GOLD_D = hexc("#f2c14e"), hexc("#b9862a")
SOC = "socrates"
CAST.setdefault(SOC, dict(skin=hexc("#e8b48a"), shirt=hexc("#f1ead8"), pants=hexc("#f1ead8"), bw=104, bh=104,
                          head=42, kind="robe", hair="gray", hair_col=hexc("#e2ddd2"), beard=hexc("#e2ddd2"),
                          seed=291))
CAST.setdefault("pythia", dict(skin=hexc("#f0c29c"), shirt=hexc("#7a4fa0"), pants=hexc("#7a4fa0"), bw=82, bh=112,
                               head=38, kind="dress", hair="long", hair_col=hexc("#2b1c14"), lashes=True, seed=293))


def socrates(cr, t, tl, x, y=960, s=1.1, **kw):
    kw.setdefault("arms", ("hip", "hip"))
    kw.setdefault("eyes", "dot")
    person(cr, SOC, x, y, t, facing=kw.pop("facing", 1), scale=s, mouth=talk(tl, SOC, t, kw.pop("mouth", "smile")),
           **kw)


def temple(cr, x0, x1, y):
    shape(cr, [(x0 - 30, y - 330), ((x0 + x1) / 2, y - 430), (x1 + 30, y - 330)], hexc("#efe4cf"), seed=10, amp=0.4,
          lw=4)
    shape(cr, rrect_pts(x0 - 30, y - 340, x1 - x0 + 60, 26, 3, 10), hexc("#e3d6bd"), seed=11, amp=0.3, lw=4)
    n = 4
    for k in range(n):
        x = x0 + k * (x1 - x0) / (n - 1)
        shape(cr, rrect_pts(x - 24, y - 314, 48, 314, 3, 12), hexc("#efe4cf"), seed=12 + k, amp=0.4, lw=4)


def smoke(cr, t, x, y):
    for k in range(4):
        ph = (t * 0.5 + k * 0.25) % 1.0
        blob(cr, x + 20 * math.sin(t * 2 + k), y - ph * 160, 16 + ph * 22, 12 + ph * 16, hexc("#c9c4d6", 0.8 - 0.7 * ph),
             seed=20 + k, amp=0.6, lw=0, stroke=None)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, (1.6, 360, 820)), (A("s1", "and"), (1.75, 360, 830))]
    bg(cr, t, keys, SKY, GROUND)
    socrates(cr, t, tl, 360, arms=("hip", "hip") if t < A("s1", "and") else ("point", "hip"),
             eyes="sly", mouth="smirk")
    if t < A("s1", "and"):
        for k in range(3):
            write(cr, [("?", RED)], 250 + k * 110, 640 - 30 * (k % 2), 64, bold=True)
    hl(cr, t, [("\"I know ", INK), ("NOTHING", RED), (".\"", INK)], 215, 70, 0.0, end=A("s1", "and") - 0.05, bold=True,
       sound=False)
    hl(cr, t, [("...so he was the ", INK), ("WISEST", GREEN)], 215, 58, A("s1", "and"), bold=True)
    cue("hit", t, A("s1", "wisest."))


def scene_oracle(cr, t, tl):
    A = tl.at
    keys = [(A("s2") - 0.2, (1.2, 360, 760)), (A("s3"), (1.35, 420, 780))]
    bg(cr, t, keys, SKY, GROUND)
    temple(cr, 380, 640, 960)
    smoke(cr, t, 540, 830)
    shape(cr, [(500, 960), (540, 860), (580, 960)], hexc("#b9862a"), seed=30, amp=0.3, lw=4)
    person(cr, "pythia", 540, 880, t, facing=-1, arms=("wave", "down") if t >= A("s3", "no") else ("down", "down"),
           eyes="sly" if t >= A("s3", "no") else "dot", mouth="o" if t >= A("s3", "no") else "smile", scale=0.85)
    person(cr, "claimant", 210, 960, t, facing=1, arms=("point", "hip") if t >= A("s2", "is") else ("down", "down"),
           eyes="wide", mouth="o" if A("s2", "is") <= t < A("s3") else "smile", scale=1.0)
    tag(cr, t, A("s2", "oracle"), 520, 470, "ORACLE OF DELPHI", GOLD, s=0.55)
    if A("s2", "is") <= t < A("s3"):
        bubble(cr, 250, 560, 330, 120, (220, 680), [], s=max(0.6, pop(t, A("s2", "is"), 0.25)), size=34,
               lines=[[("Anyone wiser", INK)], [("than ", INK), ("Socrates", BLUE), ("?", INK)]])
    if t >= A("s3", "no"):
        stamp(cr, t, A("s3", "no"), "NO ONE!", dur=0.8, y=330)
    hl(cr, t, [("about ", INK), ("2,400", RED), (" years ago", INK)], 215, 62, A("s2"), end=A("s2", "is") - 0.05,
       bold=True)
    hl(cr, t, [("\"anyone ", INK), ("WISER", GREEN), ("?\"", INK)], 215, 66, A("s2", "is"), end=A("s3", "no") - 0.05,
       bold=True)
    cue("hit", t, A("s3", "no"))


PEOPLE = (("lustig", 165, "politician.", "POLITICIAN"), ("rocker_a", 360, "poets.", "POET"),
          ("owner", 555, "craftsmen.", "CRAFTSMAN"))


def scene_test(cr, t, tl):
    A = tl.at
    keys = [(A("s4") - 0.2, CLOSE), (A("s5"), (1.35, 360, 790))]
    bg(cr, t, keys, SKY, GROUND)
    if t < A("s5"):
        socrates(cr, t, tl, 360, arms=("chin", "hip") if t < A("s4", "test") else ("point", "hip"),
                 eyes="wide" if t < A("s4", "knew") else "sly", mouth="o" if t < A("s4", "knew") else "smirk")
        if t < A("s4", "knew"):
            for k in range(3):
                write(cr, [("?", RED)], 250 + k * 110, 630 - 30 * (k % 2), 64, bold=True)
        hl(cr, t, [("he knew he ", INK), ("WASN'T", RED), (" wise", INK)], 215, 60, A("s4", "knew"), bold=True)
        hl(cr, t, [("Socrates was ", INK), ("CONFUSED", RED)], 215, 60, A("s4"), end=A("s4", "knew") - 0.05,
           bold=True)
        return
    stuck = t >= A("s6", "explain.")
    for k, (who, x, key, lab) in enumerate(PEOPLE):
        st = A("s5", key)
        if t >= st:
            proud = t < A("s6", "when")
            person(cr, who, x, 900, t, facing=1 if x < 360 else -1, arms=("hip", "hip") if proud else ("rub", "face"),
                   eyes="sly" if proud else "wide", mouth="smirk" if proud else "o", sweat=stuck,
                   scale=max(0.6, pop(t, st, 0.25)) * 0.9)
            tag(cr, t, st, x, 590, lab, GOLD, s=0.42, seed=60 + k)
            if t >= A("s6", "when"):
                write(cr, [("?", RED)], x + 8, 698, 60, align="center", bold=True)
    hl(cr, t, [("people called ", INK), ("WISE", GREEN)], 215, 62, A("s5"), end=A("s6") - 0.05, bold=True)
    hl(cr, t, [("thought they ", INK), ("KNEW", RED)], 215, 66, A("s6"), end=A("s6", "when") - 0.05, bold=True)
    hl(cr, t, [("couldn't ", RED), ("explain", INK)], 215, 70, A("s6", "when"), bold=True)


def box(cr, t, start, x, y, who, top, bottom, col, mark):
    if t < start:
        return
    with at(cr, x, y, max(0.6, pop(t, start, 0.3))):
        shape(cr, rrect_pts(-165, -170, 330, 340, 20, 12), WHITE, seed=70 + int(x) % 7, amp=0.4, lw=4)
        write(cr, [(who, INK)], 0, -110, 46, align="center", bold=True)
        write(cr, [(top, INK)], 0, -36, 38, align="center", bold=True)
        write(cr, [(bottom, col)], 0, 24, 36, align="center", bold=True)
        write(cr, [(mark, col)], 0, 120, 60, align="center", bold=True)


def scene_realize(cr, t, tl):
    A = tl.at
    keys = [(A("s7") - 0.2, (1.0, 360, 640))]
    bg(cr, t, keys, SKY)
    box(cr, t, A("s7", "this"), 185, 470, "HIM", "doesn't know", "THINKS HE DOES", RED, "NOT WISE")
    box(cr, t, A("s7", "don't"), 535, 470, "SOCRATES", "doesn't know", "KNOWS IT", GREEN, "WISE")
    socrates(cr, t, tl, 360, y=870, s=1.0, arms=("point", "hip"), eyes="happy" if t < A("s7", "doesn't.") else "dot")
    hl(cr, t, [("then he ", INK), ("UNDERSTOOD", GREEN)], 215, 62, A("s7"), bold=True)
    cue("hit", t, A("s7", "don't"))


def desk(cr, x, y):
    shape(cr, rrect_pts(x - 90, y - 10, 180, 22, 4, 10), hexc("#b9824a"), seed=80 + int(x) % 5, amp=0.3, lw=4)
    for dx in (-76, 76):
        line(cr, [(x + dx, y + 12), (x + dx, y + 90)], 6, hexc("#8e5a2e"), seed=82, amp=0.2)


def paper(cr, x, y, grade, col, s=1.0):
    with at(cr, x, y, s, rot=-0.08):
        shape(cr, rrect_pts(-50, -64, 100, 128, 6, 10), WHITE, seed=84, amp=0.4, lw=4)
        write(cr, [(grade, col)], 0, 28, 80, align="center", bold=True)


def scene_students(cr, t, tl):
    A = tl.at
    keys = [(A("s8") - 0.2, (1.2, 360, 760))]
    bg(cr, t, keys, hexc("#e9eef2"), hexc("#c9b493"), ground_y=900)
    tag(cr, t, A("s8", "test"), 360, 470, "TEST TOMORROW", hexc("#ffb3a8"), s=0.6)
    line(cr, [(360, 520), (360, 900)], 4, hexc("#b0b8c0"), seed=90, amp=0.3)
    done = t >= A("s11")
    # student 1: relaxed, not studying
    desk(cr, 190, 820)
    person(cr, "kid_b", 190, 900, t, facing=1,
           arms=("hip", "hip") if not done else ("face", "face"),
           eyes=("happy" if t < A("s11") else "sad") if t >= A("s9") else "dot",
           mouth="grin" if not done else "sad", scale=1.0)
    if A("s9", "thinks") <= t < A("s11"):
        bubble(cr, 185, 560, 260, 96, (190, 650), [("I know it all!", INK)], s=1.0, size=34)
    # student 2: studying
    desk(cr, 530, 820)
    person(cr, "kid_a", 530, 900, t, facing=-1, arms=("hold", "hold") if t >= A("s10", "studies") else
           ("chin", "hip"), eyes="dot" if not done else "happy", mouth="flat" if not done else "grin", scale=1.0)
    if t >= A("s10", "studies"):
        with at(cr, 490, 790, 0.8, rot=0.1):
            shape(cr, rrect_pts(-40, -30, 80, 60, 6, 10), hexc("#3f6fb5"), seed=86, amp=0.3, lw=4)
    if A("s10", "knows") <= t < A("s11"):
        bubble(cr, 530, 560, 300, 96, (530, 650), [("What don't I know?", INK)], s=1.0, size=32)
    if done:
        paper(cr, 120, 650, "F", RED, max(0.6, pop(t, A("s11", "one"), 0.3)))
        paper(cr, 600, 650, "A", GREEN, max(0.6, pop(t, A("s11", "one"), 0.3)))
    hl(cr, t, [("an ", INK), ("EXAMPLE", GREEN)], 215, 70, A("s8"), end=A("s9") - 0.05, bold=True)
    hl(cr, t, [("\"I know ", INK), ("EVERYTHING", RED), ("\"", INK)], 215, 60, A("s9"), end=A("s10") - 0.05, bold=True)
    hl(cr, t, [("studies what he ", INK), ("DOESN'T", GREEN), (" know", INK)], 215, 44, A("s10"), end=A("s11") - 0.05,
       bold=True)
    hl(cr, t, [("who ", INK), ("PASSES", GREEN), ("?", INK)], 215, 70, A("s11"), bold=True)
    cue("hit", t, A("s11", "one"))


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("s12") - 0.2, CLOSE)]
    bg(cr, t, keys, SKY, GROUND)
    socrates(cr, t, tl, 360, arms=("chin", "hip"), eyes="sly", mouth="smirk")
    buttons(cr, t, A("s12", "smart"), (("SMART", GREEN), ("WEAK", RED)), y=1060, s=0.75)
    hl(cr, t, [("\"I don't know\": ", INK), ("SMART", GREEN), ("?", INK)], 215, 58, A("s12", "is"), bold=True,
       underline=True)
    stamp(cr, t, A("s12", "know?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "oracle": scene_oracle, "test": scene_test, "realize": scene_realize,
     "students": scene_students, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
