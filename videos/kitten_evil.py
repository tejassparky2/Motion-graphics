"""Big question: "Could God Have Saved Her?" -- a girl buries her kitten and asks her dad three questions (the problem
of evil), in the polished look. Original story.

Script: out/scripts_big_questions_batch2.md, video 1 (owner approved 25 Oct 2026). The "Epicurean paradox" is known
from Lactantius (De Ira Dei, ch. 13) and David Hume, Dialogues Concerning Natural Religion (1779), Part X; the line
says "often credited to Epicurus" because the attribution is uncertain. Free-will defence: Alvin Plantinga, God,
Freedom, and Evil (1974); the girl's reply is the standard objection from natural suffering. Turbo stock female
narrator with tags; the girl and her dad through Turbo with Kokoro reference voices (no tags on them).
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, red_x, shake, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, bold_text, camera, captions, ellipse, enter, lin, paint, rad,
                           rrect, shade, sign, smooth, soft_disc, stamp, stroke_line, vignette)
from motion.timeline import clear_dialogue
from videos.bq_kit import heart_shape, scroll, talker, two_doors

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "d6"          # music drops out when Dad has no answer (research 18 Oct 2026, A5)
SERIES = "Big Questions"
voice.SPEAKERS.update({"girl": dict(voice="af_sky", speed=1.0, turbo_ref="af_sky+3"),
                       "dad": dict(voice="am_adam", speed=0.97, turbo_ref="am_adam")})
GIRL = dict(skin="tan", hair="pony", hair_col=hexc("#2b1a12"), shirt=hexc("#9fd0f0"), tie=None,
            pants=hexc("#e86a8a"), skirt=True, build="kid")
HUG_DAD = ((-150, 10), "down")                                  # Dad's arm around her shoulders
HUG_GIRL = ((-70, 40), (-40, 70))                               # her arms wrapped around him

SCRIPT = [
    dict(id="d1", scene="grave", text="A girl buries her kitten in the garden. Then she asks her dad three questions."),
    dict(id="d2", scene="ask", text="Could God have saved her?", speaker="girl"),
    dict(id="d3", scene="ask", text="Yes. God can do anything.", speaker="dad"),
    dict(id="d4", scene="ask", text="Did God want her to live?", speaker="girl"),
    dict(id="d5", scene="ask", text="Of course. God is good.", speaker="dad"),
    dict(id="d6", scene="ask", text="Then why is she gone?", speaker="girl", gap=0.4),
    dict(id="d7", scene="scroll", text="It's the oldest puzzle about God. It's often credited to Epicurus, over two "
                                       "thousand years ago."),
    dict(id="d8", scene="doors", text="If God can stop suffering but won't, is he good? If he wants to but can't, is "
                                      "he all-powerful?"),
    dict(id="d9", scene="free", text="One famous answer is free will. A world where we can truly choose good must let "
                                     "us choose harm too."),
    dict(id="d10", scene="comeback", text="But nobody chose to make my kitten sick.", speaker="girl"),
    dict(id="d11", scene="hug", text="And that's the part people still argue about. Her dad just hugs her. [sigh]"),
    dict(id="d12", scene="end", text="So, is suffering proof against a good God, or the price of a free world?",
         gap=0.3),
]
clear_dialogue(SCRIPT, ids={"d2", "d3", "d4", "d5", "d6"}, pace=0.96, turn_gap=0.34)

METADATA = dict(
    title="She Asked Her Dad 3 Questions About God 🐱",
    alt_titles=["Could God Have Saved Her Kitten? 🐱", "The Oldest Question About God 🐱"],
    description="""A girl buries her kitten in the garden. Then she asks her dad three questions. "Could God have saved her?" Yes. "Did God want her to live?" Of course. "Then why is she gone?" 🐱

It's the oldest puzzle about God, often credited to Epicurus: if God can stop suffering but won't, is he good? If he wants to but can't, is he all-powerful?

One famous answer is free will: a world where we can truly choose good must let us choose harm too. But nobody chose to make a kitten sick, and that's the part people still argue about.

An original story. Sources: the "Epicurean paradox" (Lactantius, De Ira Dei 13; David Hume, Dialogues Concerning Natural Religion, 1779, Part X); the free-will defence (Alvin Plantinga, God, Freedom, and Evil, 1974).

💬 Is suffering proof against a good God, or the price of a free world? Keep it respectful 🙏 👇

🔔 Interestingly Strange: mind-bending questions, clever twists and The Last Bencher, animated in under a minute.""",
    hashtags=["#BigQuestions", "#Philosophy", "#Shorts"],
    tags=["problem of evil", "why does god allow suffering", "epicurus paradox", "free will", "god and suffering",
          "philosophy", "deep questions", "kid asks dad", "big questions", "interestingly strange"],
    pinned_comment="PROOF or PRICE? Give one reason, and keep it respectful 🙏 👇",
)


# ---------------------------------------------------------------- props
def garden(cr, t, dusk=0.0):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, shade(hexc("#ffb080"), -0.35 * dusk)), (0.45, shade(hexc("#ffd8a8"), -0.3 * dusk)),
                                   (0.62, shade(hexc("#9ad07a"), -0.3 * dusk)), (1, shade(hexc("#5aa04a"), -0.3 * dusk))]))
    cr.fill()
    soft_disc(cr, 560, 520, 150, (1, 0.85, 0.5, 0.5 - 0.3 * dusk))               # low sun
    for k in range(10):                                                            # fence
        x = 20 + k * 72
        cr.move_to(x, 800)
        cr.line_to(x, 640)
        cr.line_to(x + 25, 615)
        cr.line_to(x + 50, 640)
        cr.line_to(x + 50, 800)
        cr.close_path()
        paint(cr, shade(hexc("#f0e2c8"), -0.3 * dusk), OUTLINE, 4)
    rrect(cr, 0, 680, W, 18, 4)
    paint(cr, shade(hexc("#e0d0b0"), -0.3 * dusk), OUTLINE, 4)
    stroke_line(cr, [(110, 800), (120, 520)], 26, hexc("#7a4a2a"), curve=False)   # a small tree
    for dx, dy, r in ((-60, -10, 80), (50, -30, 90), (0, -90, 85)):
        ellipse(cr, 120 + dx, 500 + dy, r, r * 0.85)
        paint(cr, shade(hexc("#4a9a4a"), -0.3 * dusk), OUTLINE, 5)


def grave(cr, t, x=360, y=900, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ellipse(cr, 0, 0, 120, 40)                                                     # soil mound
    paint(cr, rad(-20, -20, 140, [(0, hexc("#9a6a40")), (1, hexc("#6a4426"))]), OUTLINE, 5)
    for k, (fx, col) in enumerate(((-70, hexc("#ff7a9a")), (-20, hexc("#ffd84d")), (40, hexc("#ffffff")),
                                   (80, hexc("#c87aff")))):                       # flowers
        stroke_line(cr, [(fx, -10), (fx + 4, -48)], 4, hexc("#3a8a3a"), curve=False)
        for p in range(5):
            a = p * 2 * math.pi / 5 + t * 0.3
            ellipse(cr, fx + 4 + 9 * math.cos(a), -52 + 9 * math.sin(a), 7, 7)
            paint(cr, col, OUTLINE, 2)
        ellipse(cr, fx + 4, -52, 5, 5)
        paint(cr, GOLD, None, 0)
    cr.arc(0, -16, 22, 0, 2 * math.pi)                                             # the collar with a bell
    cr.set_source_rgba(*hexc("#e8473f"))
    cr.set_line_width(7)
    cr.stroke()
    ellipse(cr, 0, 8, 9, 9)
    paint(cr, GOLD, OUTLINE, 3)
    cr.restore()


def girl(cr, t, tl, x, y, s=0.9, **kw):
    talker(cr, t, tl, "girl", "student1", x, y, s, rest="sad", **dict(GIRL, **kw))


def dad(cr, t, tl, x, y, s=1.0, **kw):
    talker(cr, t, tl, "dad", "dad", x, y, s, rest="smile", **kw)


def yes_card(cr, t, start, x, y, title, crack_at=None):
    card(cr, t, start, x, y, 280, 150, title, ["YES"], col=GREEN, title_size=34, line_size=56)
    if crack_at is not None and t >= crack_at:
        stroke_line(cr, [(x - 20, y - 70), (x + 6, y - 20), (x - 12, y + 20), (x + 14, y + 72)], 7, OUTLINE,
                    curve=False)
        red_x(cr, t, crack_at, x, y + 10, 60)


# ---------------------------------------------------------------- scenes
def scene_grave(cr, t, tl):
    A = tl.at
    garden(cr, t)
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 700)), (A("d1", "asks"), (1.2, 380, 760))], dur=0.8))
    grave(cr, t, 330, 980, 1.0)
    dad(cr, t, None, 560, 1000, 0.95, eyes="sad", mouth="flat", arms=("down", "down"), look=(-0.5, 0.3))
    girl(cr, t, None, 200, 1000, 0.85, eyes="sad", mouth="sad", arms=("front", "front"), look=(0.4, 0.4))
    cr.restore()
    if t >= A("d1", "three"):
        tag(cr, t, A("d1", "three"), 360, 380, "3 QUESTIONS", col=PURPLE, size=44)
    vignette(cr, 0.35)


def scene_ask(cr, t, tl):
    A = tl.at
    garden(cr, t)
    frozen = t >= A("d6", "gone")
    cr.save()
    enter(cr, camera(t, [(A("d2") - 0.3, (1.25, 380, 780)), (A("d6"), (1.45, 420, 760))], dur=0.6))
    grave(cr, t, 330, 1010, 0.9)
    if frozen:
        dx, dy = shake(t, A("d6", "gone"), 0.3, 5)
        cr.translate(dx, dy)
    dad(cr, t, tl, 540, 1000, 0.95, eyes="wide" if frozen else "open", mouth="o" if frozen else None,
        brows="up" if frozen else None, arms=("front", "down") if frozen else ("hips", "down"), sweat=frozen,
        look=(-0.5, 0.2))
    girl(cr, t, tl, 250, 1000, 0.85, eyes="sad", arms=("down", "down"), look=(0.6, -0.4))
    cr.restore()
    yes_card(cr, t, A("d3", "Yes"), 200, 300, "CAN HE?", crack_at=A("d6", "gone"))
    if t >= A("d5"):
        yes_card(cr, t, A("d5", "Of"), 520, 300, "WANTS TO?", crack_at=A("d6", "gone") + 0.15)
    if frozen:
        sign(cr, t, A("d6", "gone"), 360, 500, "THEN WHY?", col=RED, size=70)
    vignette(cr, 0.35)


def scene_scroll(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e6c8"), hexc("#e8d0a0"), seed=41)
    scroll(cr, 360, 620, 1.0)
    old = t >= A("d7", "thousand")
    bold_text(cr, "2,000+ YEARS" if old else "CAN? WANTS?", 360, 610, 40, hexc("#6a4426"), outline=None, shadow=0)
    bold_text(cr, "OLD" if old else "WHY?", 360, 670, 40, hexc("#6a4426"), outline=None, shadow=0)
    tag(cr, t, tl.scene_at(t)[1], 360, 240, "THE OLDEST PUZZLE", col=GOLD, size=50)
    if t >= A("d7", "Epicurus"):
        sign(cr, t, A("d7", "Epicurus"), 360, 350, "OFTEN CREDITED TO EPICURUS", col=hexc("#a8713e"), size=36)
    vignette(cr, 0.35)


def scene_doors(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#55406e"), seed=42)
    two_doors(cr, t, ["CAN, BUT WON'T", "WANTS, BUT CAN'T"], [PURPLE, BLUE],
              x_at=(A("d8", "good"), A("d8", "powerful")), label_size=30)
    sign(cr, t, tl.scene_at(t)[1], 360, 190, "IS HE GOOD?", col=GOLD, size=56, end=A("d8", "wants") - 0.05)
    if t >= A("d8", "wants"):
        sign(cr, t, A("d8", "wants"), 360, 190, "ALL-POWERFUL?", col=GOLD, size=56)
    vignette(cr, 0.4)


def fork(cr, t, x, y, s=1.0, tear=0.0):
    """The free-will card: a road that splits into GOOD and HARM."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -250, -200, 500, 400, 22)
    paint(cr, WHITE, OUTLINE, 6)
    rrect(cr, -250, -200, 500, 70, 22)
    paint(cr, GOLD, OUTLINE, 6)
    bold_text(cr, "FREE WILL", 0, -150, 44, WHITE)
    stroke_line(cr, [(0, 170), (0, 40)], 26, hexc("#b8b8c8"), curve=False)
    stroke_line(cr, [(0, 50), (-120, -90)], 24, GREEN, curve=False)
    stroke_line(cr, [(0, 50), (120, -90)], 24, RED, curve=False)
    bold_text(cr, "GOOD", -140, -100, 34, GREEN, outline=None, shadow=0)
    bold_text(cr, "HARM", 140, -100, 34, RED, outline=None, shadow=0)
    cr.restore()
    if tear > 0:
        pts = [(x - 250 * s, y + 10), (x - 120 * s, y - 30), (x, y + 30), (x + 120 * s, y - 20), (x + 250 * s, y + 20)]
        stroke_line(cr, pts[:max(2, int(len(pts) * tear))], 10, OUTLINE, curve=False)


def scene_free(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f3a4a"), hexc("#3f5a6e"), seed=43)
    fork(cr, t, 360, 560, 0.95 * min(1.0, 0.6 + 2 * (t - tl.scene_at(t)[1])))
    if t >= A("d9", "harm"):
        tag(cr, t, A("d9", "harm"), 360, 250, "REAL CHOICE = REAL HARM", col=PURPLE, size=40)
    vignette(cr, 0.4)


def scene_comeback(cr, t, tl):
    A = tl.at
    garden(cr, t, dusk=0.3)
    cr.save()
    enter(cr, camera(t, [(A("d10") - 0.3, (1.9, 250, 640))], dur=0.5))
    girl(cr, t, tl, 250, 1000, 0.85, eyes="sad", brows="sad", arms=("front", "front"), look=(0.3, -0.2))
    cr.restore()
    fork(cr, t, 360, 360, 0.55, tear=seg(t, A("d10", "sick"), A("d10", "sick", end=True) + 0.3))
    if t >= A("d10", "nobody"):
        tag(cr, t, A("d10", "nobody"), 360, 150, "NOBODY CHOSE THIS", col=RED, size=44)
    vignette(cr, 0.4)


def scene_hug(cr, t, tl):
    A = tl.at
    garden(cr, t, dusk=0.5)
    cr.save()
    enter(cr, camera(t, [(A("d11"), (1.2, 380, 780)), (A("d11", "hugs"), (1.35, 380, 760))], dur=0.8))
    hugging = t >= A("d11", "hugs")
    dad(cr, t, None, 430 if hugging else 540, 1000, 0.95, eyes="closed" if hugging else "sad", mouth="flat",
        arms=HUG_DAD if hugging else ("down", "down"))
    girl(cr, t, None, 350 if hugging else 250, 1000, 0.85, eyes="closed" if hugging else "sad", mouth="sad",
         arms=HUG_GIRL if hugging else ("down", "down"))
    grave(cr, t, 190, 1090, 0.8)
    cr.restore()
    if hugging:
        heart_shape(cr, 380, 470 - 20 * seg(t, A("d11", "hugs"), A("d11", "hugs") + 1.2), 0.7, hexc("#ff7a9a"))
    sign(cr, t, A("d11", "argue"), 360, 200, "STILL ARGUED TODAY", col=PURPLE, size=48,
         end=A("d11", "hugs") - 0.05)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    garden(cr, t, dusk=0.7)
    cr.save()
    enter(cr, camera(t, [(A("d12"), (1.1, 380, 800))]))
    dad(cr, t, None, 430, 1000, 0.95, eyes="half", mouth="flat", arms=HUG_DAD)
    girl(cr, t, None, 350, 1000, 0.85, eyes="sad", mouth="flat", arms=HUG_GIRL)
    grave(cr, t, 190, 1090, 0.8)
    cr.restore()
    sign(cr, t, A("d12", "proof"), 360, 200, "PROOF, OR PRICE?", col=GOLD, size=56)
    buttons(cr, t, A("d12", "proof"), [("PROOF", RED), ("PRICE", GREEN)], y=330, size=52)
    vignette(cr, 0.35)


SCENES = {"grave": scene_grave, "ask": scene_ask, "scroll": scene_scroll, "doors": scene_doors, "free": scene_free,
          "comeback": scene_comeback, "hug": scene_hug, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("COULD GOD HAVE", False), ("SAVED HER?", True)], end=tl.at("d3"), y=150, size=84)
    captions(cr, t, tl)
