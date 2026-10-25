"""Big question: "If God Already Knows, Why Pray?" -- exam morning, a girl prays and her little brother asks one
question; Aquinas answers, in the polished look. Original story.

Script: out/scripts_big_questions_batch2.md, video 3 (owner approved 25 Oct 2026). Thomas Aquinas, Summa Theologiae
II-II, q. 83, a. 2: "we pray not that we may change the Divine disposition, but that we may impetrate that which God
has disposed to be fulfilled by our prayers"; line p9 is a plain-English paraphrase. Respectful: the girl's prayer is
never mocked. Turbo stock female narrator with tags; the girl and her brother through Turbo with Kokoro reference
voices (no tags on them).
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, check, shake, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, bold_text, camera, captions, ellipse, enter, lin, paint, rad,
                           rrect, shade, sign, smooth, soft_disc, stamp, stroke_line, vignette)
from motion.timeline import clear_dialogue
from videos.bq_kit import talker, two_doors

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "p6"          # music drops out on the brother's question (research 18 Oct 2026, A5)
SERIES = "Big Questions"
END_TAG = "Subscribe · a new question tomorrow"      # alternate videos test the silent subscribe wording (research E4/E5)
voice.SPEAKERS.update({"sis": dict(voice="af_nicole", speed=1.0, turbo_ref="af_nicole"),
                       "bro": dict(voice="am_puck", speed=1.06, pitch=4.0, turbo_ref="am_puck+5")})
SIS = dict(skin="brown", hair="bun", hair_col=hexc("#1e130d"), shirt=hexc("#3fae8a"), tie=None,
           pants=hexc("#2f3550"), build="kid")
BRO = dict(skin="brown", shirt=hexc("#ff9a3c"), tie=None, pants=hexc("#3b5b9a"))
PRAY = ((-58, -64), (-58, -64))                                   # both hands together under the chin

SCRIPT = [
    dict(id="p1", scene="pray", text="Exam morning. A girl folds her hands and prays to pass."),
    dict(id="p2", scene="talk", text="Wait. Doesn't God already know if you'll pass?", speaker="bro"),
    dict(id="p3", scene="talk", text="Of course. He knows everything.", speaker="sis"),
    dict(id="p4", scene="talk", text="And his plan is perfect?", speaker="bro"),
    dict(id="p5", scene="talk", text="Yes.", speaker="sis"),
    dict(id="p6", scene="talk", text="Then why pray? You can't change a perfect plan.", speaker="bro", gap=0.4),
    dict(id="p7", scene="doors", text="If prayer changes God's plan, the plan wasn't perfect. If it can't, why pray?"),
    dict(id="p8", scene="aquinas", text="Thomas Aquinas answered this seven hundred years ago."),
    dict(id="p9", scene="aquinas", text="We don't pray to change God's plan. Our prayers are part of the plan."),
    dict(id="p10", scene="callback", text="So God's plan includes you studying too?", speaker="bro"),
    dict(id="p11", scene="callback", text="She groans. [laugh]"),
    dict(id="p12", scene="end", text="So, does prayer change what happens, or does it change the one who prays?",
         gap=0.3),
]
clear_dialogue(SCRIPT, ids={"p2", "p3", "p4", "p5", "p6"}, pace=0.96, turn_gap=0.34)

METADATA = dict(
    title="She Prayed Before Her Exam. Her Brother Asked 1 Question 🙏",
    alt_titles=["If God Already Knows, Why Pray? 🙏", "Does Prayer Change God's Plan? 🙏"],
    description="""Exam morning. A girl folds her hands and prays to pass. Her little brother: "Doesn't God already know if you'll pass? And his plan is perfect? Then why pray? You can't change a perfect plan." 🙏

If prayer changes God's plan, the plan wasn't perfect. If it can't, why pray?

Thomas Aquinas answered this about 750 years ago: we don't pray to change God's plan; our prayers are part of the plan. (Paraphrased from Summa Theologiae II-II, q. 83, a. 2: "we pray not that we may change the Divine disposition, but that we may impetrate that which God has disposed to be fulfilled by our prayers.")

So God's plan includes her studying too. 😄

An original story.

💬 Does prayer change what happens, or does it change the one who prays? Keep it respectful 🙏 👇

🔔 Interestingly Strange: mind-bending questions, clever twists and The Last Bencher, animated in under a minute.""",
    hashtags=["#BigQuestions", "#Philosophy", "#Shorts"],
    tags=["why pray if god knows", "does prayer change god's plan", "thomas aquinas prayer", "prayer and free will",
          "exam prayer", "philosophy", "deep questions", "siblings", "big questions", "interestingly strange"],
    pinned_comment="Does prayer change WHAT HAPPENS, or change YOU? One reason, keep it respectful 🙏 👇",
)


# ---------------------------------------------------------------- props
def room(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#fbe8c8")), (0.66, hexc("#f2d8b0")), (0.66, hexc("#c8925a")),
                                   (1, hexc("#9a6a3a"))]))
    cr.fill()
    rrect(cr, 60, 200, 230, 280, 12)                               # window, morning
    paint(cr, lin(0, 200, 0, 480, [(0, hexc("#9fd6ff")), (1, hexc("#fff4d8"))]), OUTLINE, 6)
    stroke_line(cr, [(175, 200), (175, 480)], 6, OUTLINE, curve=False)
    soft_disc(cr, 120, 260, 50, (1, 1, 0.85, 0.7))
    cr.save()                                                      # wall clock at 7:45
    cr.translate(430, 300)
    ellipse(cr, 0, 0, 62, 62)
    paint(cr, WHITE, OUTLINE, 6)
    for a, ln, w in ((math.radians(7.75 * 30 - 90), 30, 7), (math.radians(45 * 6 - 90), 46, 5)):
        stroke_line(cr, [(0, 0), (ln * math.cos(a), ln * math.sin(a))], w, OUTLINE, curve=False)
    cr.restore()
    rrect(cr, 600, 200, 140, 700, 6)                               # the doorway at the right
    paint(cr, hexc("#d8b88a"), OUTLINE, 6)
    rrect(cr, 618, 220, 122, 680, 4)
    paint(cr, hexc("#5a4030"), None, 0)


def desk(cr, x=300, y=900):
    rrect(cr, x - 230, y - 20, 460, 30, 8)
    paint(cr, hexc("#a8713e"), OUTLINE, 5)
    for lx in (x - 210, x + 190):
        rrect(cr, lx, y + 10, 22, 160, 4)
        paint(cr, hexc("#8a5a30"), OUTLINE, 4)
    for k, col in enumerate((hexc("#e8473f"), hexc("#4aa3f0"), hexc("#3fbf6a"))):    # books
        rrect(cr, x + 80, y - 50 - 26 * k, 130, 26, 4)
        paint(cr, col, OUTLINE, 4)
    rrect(cr, x - 200, y - 34, 120, 16, 4)                         # admit card + pens
    paint(cr, WHITE, OUTLINE, 3)
    bold_text(cr, "ADMIT CARD", x - 140, y - 22, 12, OUTLINE, outline=None, shadow=0)


def sis(cr, t, tl, x, y, s=0.95, **kw):
    talker(cr, t, tl, "sis", "student1", x, y, s, rest="smile", **dict(SIS, **kw))


def bro(cr, t, tl, x, y, s=0.75, **kw):
    talker(cr, t, tl, "bro", "kid", x, y, s, rest="smug", **dict(BRO, **kw))


def bowl(cr, hx, hy):
    cr.move_to(hx - 40, hy - 12)
    cr.line_to(hx + 40, hy - 12)
    cr.line_to(hx + 28, hy + 18)
    cr.line_to(hx - 28, hy + 18)
    cr.close_path()
    paint(cr, hexc("#4aa3f0"), OUTLINE, 4)
    for k in range(5):
        ellipse(cr, hx - 24 + k * 12, hy - 16, 7, 5)
        paint(cr, hexc("#f0c060"), OUTLINE, 2)


def textbook(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -90, -60, 180, 120, 8)
    paint(cr, hexc("#e8473f"), OUTLINE, 5)
    rrect(cr, -70, -40, 140, 40, 6)
    paint(cr, WHITE, None, 0)
    bold_text(cr, "MATHS", 0, -10, 30, hexc("#e8473f"), outline=None, shadow=0)
    cr.restore()


# ---------------------------------------------------------------- scenes
def scene_pray(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("p1", "folds"), (1.15, 320, 680))], dur=0.8))
    sis(cr, t, None, 280, 1010, 0.95, eyes="closed", mouth="flat", arms=PRAY)
    desk(cr, 300, 960)
    bro(cr, t, None, 680, 1000, 0.75, eyes="open", mouth="smug", arms=("hold", "down"), hold=bowl,
        look=(-0.7, 0.0))
    cr.restore()
    if t >= A("p1", "Exam"):
        tag(cr, t, A("p1", "Exam"), 470, 440, "EXAM DAY", col=RED, size=44)
    vignette(cr, 0.35)


def scene_talk(cr, t, tl):
    A = tl.at
    room(cr, t)
    peek = t >= A("p6", "Then")
    cr.save()
    enter(cr, camera(t, [(A("p2") - 0.3, (1.2, 420, 700)), (A("p6"), (1.3, 420, 680))], dur=0.6))
    sis(cr, t, tl, 280, 1010, 0.95, eyes="half" if peek else ("closed" if t < A("p3") else "open"), arms=PRAY,
        brows="raise" if peek else None, look=(0.6, 0.0))
    desk(cr, 300, 960)
    bro(cr, t, tl, 600, 1000, 0.75, eyes="open", arms=("hold", "down"), hold=bowl, look=(-0.7, 0.0))
    cr.restore()
    card(cr, t, A("p3", "knows"), 200, 300, 300, 140, "KNOWS ALL", [], col=BLUE, title_size=40, mark="ok",
         mark_at=A("p3", "everything"))
    if t >= A("p5"):
        card(cr, t, A("p5"), 520, 300, 300, 140, "PERFECT PLAN", [], col=GREEN, title_size=36, mark="ok",
             mark_at=A("p5") + 0.2)
    if peek:
        sign(cr, t, A("p6", "Then"), 360, 480, "THEN WHY PRAY?", col=RED, size=62)
    vignette(cr, 0.35)


def scene_doors(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#55406e"), seed=61)
    two_doors(cr, t, ["IT CHANGES", "IT CAN'T"], [PURPLE, BLUE], x_at=(A("p7", "perfect"), A("p7", "why")),
              label_size=36)
    card(cr, t, tl.scene_at(t)[1], 190, 380, 300, 120, "NOT PERFECT?", [], col=PURPLE, title_size=34)
    if t >= A("p7", "can't"):
        card(cr, t, A("p7", "can't"), 530, 380, 300, 120, "WHY PRAY?", [], col=BLUE, title_size=34)
    vignette(cr, 0.4)


def path(cr, t, start, x, y, glow_at=None):
    """The plan as a winding path of stepping stones to a PASS flag; one stone is the prayer."""
    stones = [(x - 200, y + 230, "SLEEP"), (x - 60, y + 160, "PRAYER"), (x + 110, y + 100, "STUDY"),
              (x - 30, y + 20, "EXAM"), (x + 150, y - 50, "")]
    for k, (sx, sy, lab) in enumerate(stones[:-1]):
        a = min(1.0, max(0.0, (t - start - 0.15 * k) / 0.3))
        if a <= 0:
            continue
        if lab == "PRAYER" and glow_at is not None and t >= glow_at:
            soft_disc(cr, sx, sy, 110, (1, 0.9, 0.4, 0.55))
        ellipse(cr, sx, sy, 78 * a, 34 * a)
        paint(cr, hexc("#c8c0b0") if lab != "PRAYER" else hexc("#ffd84d"), OUTLINE, 5)
        if a >= 1:
            bold_text(cr, lab, sx, sy + 10, 26, OUTLINE, outline=None, shadow=0)
    fx, fy = stones[-1][:2]
    if t >= start + 0.7:
        stroke_line(cr, [(fx, fy + 30), (fx, fy - 120)], 8, OUTLINE, curve=False)
        cr.move_to(fx, fy - 120)
        cr.line_to(fx + 100, fy - 95)
        cr.line_to(fx, fy - 70)
        cr.close_path()
        paint(cr, GREEN, OUTLINE, 4)
        bold_text(cr, "PASS", fx + 40, fy - 87, 22, WHITE, outline=None, shadow=0)


def scene_aquinas(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e6c8"), hexc("#fff6e8"), seed=62)
    s0 = tl.scene_at(t)[1]
    if t < A("p9"):
        card(cr, t, s0, 360, 360, 460, 200, "THOMAS AQUINAS", ["1270s"], col=hexc("#a8713e"), title_size=40,
             line_size=54)
        if t >= A("p8", "seven"):
            tag(cr, t, A("p8", "seven"), 360, 560, "700+ YEARS AGO", col=PURPLE, size=44)
    else:
        sign(cr, t, A("p9"), 360, 200, "NOT TO CHANGE THE PLAN", col=RED, size=44, end=A("p9", "Our") - 0.05)
        if t >= A("p9", "Our"):
            sign(cr, t, A("p9", "Our"), 360, 200, "PRAYER IS PART OF IT", col=GREEN, size=48)
        path(cr, t, A("p9"), 360, 520, glow_at=A("p9", "part"))
    vignette(cr, 0.3)


def scene_callback(cr, t, tl):
    A = tl.at
    room(cr, t)
    slide = seg(t, A("p10", "studying"), A("p10", "studying") + 0.6)
    groan = t >= A("p11")
    cr.save()
    enter(cr, camera(t, [(A("p10") - 0.3, (1.25, 400, 700)), (A("p11"), (1.45, 300, 700))], dur=0.5))
    sis(cr, t, tl, 280, 1010, 0.95, eyes="half" if groan else "open", mouth="flat" if groan else None,
        brows="angry" if groan else None, arms=("face", "down") if groan else PRAY)
    desk(cr, 300, 960)
    bro(cr, t, tl, 600, 1000, 0.75, eyes="happy", arms=("point", "down"), look=(-0.7, 0.0))
    textbook(cr, lerp(560, 330, slide), 900, 0.8)
    cr.restore()
    if t >= A("p10", "studying"):
        tag(cr, t, A("p10", "studying"), 360, 330, "THE PLAN: STUDY TOO", col=GOLD, size=44)
    vignette(cr, 0.35)


def scene_end(cr, t, tl):
    A = tl.at
    room(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("p12"), (1.1, 380, 720))]))
    sis(cr, t, None, 280, 1010, 0.95, eyes="half", mouth="smile", arms=PRAY)
    desk(cr, 300, 960)
    textbook(cr, 330, 900, 0.8)
    bro(cr, t, None, 600, 1000, 0.75, eyes="happy", mouth="grin", arms=("shrug", "shrug"))
    cr.restore()
    sign(cr, t, A("p12", "change"), 360, 200, "WHAT DOES PRAYER CHANGE?", col=GOLD, size=42)
    buttons(cr, t, A("p12", "happens"), [("WHAT HAPPENS", BLUE), ("THE ONE WHO PRAYS", GREEN)], y=330, size=36,
            w=320)
    vignette(cr, 0.35)


SCENES = {"pray": scene_pray, "talk": scene_talk, "doors": scene_doors, "aquinas": scene_aquinas,
          "callback": scene_callback, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("WHY PRAY IF GOD", False), ("ALREADY KNOWS?", True)], end=tl.at("p3"), y=140, size=72)
    captions(cr, t, tl)
