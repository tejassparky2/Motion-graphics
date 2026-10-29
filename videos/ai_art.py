"""Row 81: "She Won the Art Prize. A Computer Drew It." -- who owns AI art, told through a girl and her art teacher, with
the real 2022 Colorado State Fair case, in the polished look, built on the Meanwhile Mayank frame-0 rules (one subject
on a plain ground, two-tier hook with a red mark).

Script: out/scripts_slots_75-81.md (owner, 29 Oct 2026: "Make it from research currently did"). Facts: Jason Allen's
"Théâtre D'opéra Spatial", made with Midjourney, won the digital-arts category at the 2022 Colorado State Fair; the US
Copyright Office refused registration (December 2022) and its Review Board upheld that on 5 September 2023 (not
enough human authorship); Allen then sued in federal court. The painting shown is our own drawing, not his picture.
The girl and teacher are invented. Turbo stock female narrator with tags; the girl and the teacher through Turbo with
Kokoro reference voices.
"""
import math
import random

from motion import voice
from motion.engine import W, H, cue, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, red_x, sparkles, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, lin, paint,
                           rad, rrect, sign, smooth, soft_disc, stamp, stroke_line, text_width, vignette)
from motion.toons import person
from videos.bq_kit import hook2, plain, ring, talker
from videos.last_bencher_4 import room

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "a7"          # music drops out under the Copyright Office's answer (research 18 Oct 2026, A5)
SERIES = "Big Questions"
END_TAG = "Subscribe · a new question tomorrow"      # alternate videos test the silent subscribe wording (research E4/E5)
voice.SPEAKERS.update({"girl": dict(voice="af_bella", speed=1.05, turbo_ref="af_bella+3"),
                       "teacher": dict(voice="bf_emma", speed=1.0, turbo_ref="bf_emma")})
GIRL = dict(skin="light", hair="curly", hair_col=hexc("#b0502a"), shirt=hexc("#5ab0f0"), tie=None,
            pants=hexc("#3a3a5a"))
TEACHER = dict(shirt=hexc("#2fa59a"), collar=hexc("#ffffff"))
WALL = ("#cfe6dc", "#e6f2ea")
PROMPT = "castle under a giant moon"

SCRIPT = [
    dict(id="a1", scene="prize", text="Ma'am, I won the art contest. But a computer drew it. Is the prize still mine?",
         speaker="girl"),
    dict(id="a2", scene="laptop", text="She typed what she wanted. The AI painted it in seconds."),
    dict(id="a3", scene="class", text="Then the computer is the artist.", speaker="teacher"),
    dict(id="a4", scene="director", text="A film director never holds the camera. Is the film not theirs?",
         speaker="girl"),
    dict(id="a5", scene="fair", text="This really happened. In [twenty twenty two,|2022,] an AI-made picture won "
                                     "first prize at a US state fair."),
    dict(id="a6", scene="owns", text="So who owns it?", speaker="teacher"),
    dict(id="a7", scene="office", text="The US Copyright Office said: not him. Not enough human work. He took it to "
                                       "court.", gap=0.4),
    dict(id="a8", scene="split", text="Some say the idea is the art. Others say the skill is. [chuckle]"),
    dict(id="a9", scene="end", text="So, if you only had the idea, is it your painting? Or the machine's?", gap=0.3),
]

METADATA = dict(
    title="She Won the Art Prize. A Computer Drew It. 🖼️",
    alt_titles=["Is AI Art Really Yours? 🖼️", "She Typed It. It Won. Whose Is It? 🖼️"],
    description="""A girl wins the school art contest, then tells her teacher the truth: a computer drew it. Is the prize still hers? 🖼️

She typed what she wanted; the AI painted it in seconds. Her teacher says the computer is the artist. She says a film director never holds the camera, and the film is still theirs.

This really happened. In 2022, Jason Allen's AI-made picture "Théâtre D'opéra Spatial" (made with Midjourney) won first prize in the digital-arts category at the Colorado State Fair. The US Copyright Office refused to register it: not enough human work. Its Review Board upheld that on 5 September 2023, and he took it to court.

The girl and teacher are invented; the painting in the video is our own drawing, not his picture.

💬 If you only had the idea, is it your painting? Or the machine's? 👇

🔔 Interestingly Strange: mind-bending questions, clever twists and strange true stories, animated in under a minute.""",
    hashtags=["#AIArt", "#BigQuestions", "#Shorts"],
    tags=["ai art", "who owns ai art", "ai art copyright", "colorado state fair ai art", "jason allen",
          "theatre d'opera spatial", "midjourney", "is ai art real art", "big questions", "interestingly strange"],
    pinned_comment="Idea or skill: which one makes it YOUR painting? MINE or THE MACHINE'S? 👇",
)


# ---------------------------------------------------------------- props
def painting(cr, t, x, y, s=1.0, reveal=1.0, glitch=0.0):
    """Our own dreamy castle-under-a-moon picture in a gold frame, centre (x, y); `reveal` paints it in."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -230, -180, 460, 360, 10)
    paint(cr, lin(0, -180, 0, 180, [(0, hexc("#e8c060")), (1, hexc("#b08030"))]), OUTLINE, 6)
    rrect(cr, -200, -150, 400, 300, 4)
    paint(cr, hexc("#f6f0e4"), OUTLINE, 4)
    cr.save()
    cr.rectangle(-200, -150, 400 * max(0.0, min(1.0, reveal)), 300)
    cr.clip()
    cr.rectangle(-200, -150, 400, 300)
    cr.set_source(lin(0, -150, 0, 150, [(0, hexc("#3a2a7a")), (0.55, hexc("#c86aa8")), (1, hexc("#ffb06a"))]))
    cr.fill()
    soft_disc(cr, 70, -50, 150, (1, 0.95, 0.8, 0.45))
    ellipse(cr, 70, -50, 70, 70)
    paint(cr, hexc("#fff4d8"), None, 0)
    smooth(cr, [(-200, 150), (-200, 40), (-120, -10), (-50, 50), (30, 0), (120, 60), (200, 20), (200, 150)])
    paint(cr, hexc("#5a3a7a"), None, 0)
    for cx, h in ((-40, 120), (0, 160), (40, 120)):                # castle towers
        rrect(cr, cx - 18, 110 - h, 36, h, 3)
        paint(cr, hexc("#2a1a4a"), None, 0)
        cr.move_to(cx - 24, 110 - h)
        cr.line_to(cx, 110 - h - 40)
        cr.line_to(cx + 24, 110 - h)
        cr.close_path()
        paint(cr, hexc("#2a1a4a"), None, 0)
    rrect(cr, -70, 30, 140, 80, 3)
    paint(cr, hexc("#2a1a4a"), None, 0)
    for wx in (-40, 0, 40):
        rrect(cr, wx - 5, 50 - (40 if wx == 0 else 0), 10, 16, 3)
        paint(cr, hexc("#ffd86a"), None, 0)
    cr.restore()
    if glitch > 0:                                                 # pixel squares flicker: a machine made this
        rng = random.Random(int(t * 12))
        for _ in range(10):
            gx, gy = rng.uniform(-190, 170), rng.uniform(-140, 120)
            cr.rectangle(gx, gy, 26, 26)
            cr.set_source_rgba(rng.random(), rng.random(), 1, 0.65 * glitch)
            cr.fill()
    cr.restore()


def ribbon(cr, t, x, y, s=1.0, text="1ST", col=None):
    col = col or GOLD
    cr.save()
    cr.translate(x, y)
    cr.rotate(0.08 * math.sin(t * 2))
    cr.scale(s, s)
    for side in (-1, 1):                                           # tails
        cr.move_to(side * 14, 20)
        cr.line_to(side * 46, 130)
        cr.line_to(side * 26, 116)
        cr.line_to(side * 10, 134)
        cr.line_to(side * -6, 30)
        cr.close_path()
        paint(cr, RED if col == GOLD else col, OUTLINE, 4)
    n = 16
    cr.new_path()
    for k in range(2 * n):
        r = 72 if k % 2 == 0 else 58
        a = math.pi * k / n
        (cr.move_to if k == 0 else cr.line_to)(r * math.cos(a), r * math.sin(a))
    cr.close_path()
    paint(cr, col, OUTLINE, 4)
    ellipse(cr, 0, 0, 46, 46)
    paint(cr, lin(0, -46, 0, 46, [(0, (1, 1, 1, 0.9)), (1, col)]), OUTLINE, 4)
    bold_text(cr, text, 0, 12, 30, RED if col == GOLD else WHITE, shadow=0)
    cr.restore()


def laptop(cr, t, x, y, s=1.0, typed=""):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -200, -260, 400, 250, 14)
    paint(cr, hexc("#3a3a44"), OUTLINE, 6)
    rrect(cr, -180, -240, 360, 210, 6)
    paint(cr, hexc("#f4f6fb"), None, 0)
    rrect(cr, -160, -170, 320, 60, 10)
    paint(cr, WHITE, hexc("#8a96a8"), 4)
    sz = 26 * min(1.0, 290 / max(1, text_width(cr, PROMPT, 26, "Fredoka")))
    bold_text(cr, typed + ("|" if int(t * 3) % 2 else ""), -148, -131, sz, hexc("#2b2b33"), font="Fredoka",
              outline=None, shadow=0, align="left")
    rrect(cr, -60, -90, 120, 40, 20)
    paint(cr, PURPLE, OUTLINE, 3)
    bold_text(cr, "MAKE", 0, -60, 24, WHITE, outline=None, shadow=0)
    cr.move_to(-240, -10)
    cr.line_to(240, -10)
    cr.line_to(270, 20)
    cr.line_to(-270, 20)
    cr.close_path()
    paint(cr, hexc("#8a8a96"), OUTLINE, 5)
    cr.restore()


def director_chair(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for a, b in (((-90, 0), (70, -150)), ((90, 0), (-70, -150))):
        stroke_line(cr, [a, b], 14, hexc("#8a5a2b"), curve=False)
    rrect(cr, -100, -170, 200, 26, 6)
    paint(cr, hexc("#8a5a2b"), OUTLINE, 4)
    rrect(cr, -90, -290, 180, 70, 6)
    paint(cr, hexc("#2b2b33"), OUTLINE, 4)
    bold_text(cr, "DIRECTOR", 0, -244, 30, WHITE, outline=None, shadow=0)
    for sx in (-1, 1):
        stroke_line(cr, [(sx * 90, -150), (sx * 90, -300)], 12, hexc("#8a5a2b"), curve=False)
    cr.restore()


def clapper(cr, t, x, y, s=1.0, snap=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -110, -40, 220, 140, 8)
    paint(cr, hexc("#2b2b33"), OUTLINE, 5)
    bold_text(cr, "SCENE 1", 0, 50, 30, WHITE, outline=None, shadow=0)
    cr.save()
    cr.translate(-110, -40)
    cr.rotate(-0.5 * (1 - snap))
    rrect(cr, 0, -40, 220, 40, 6)
    paint(cr, WHITE, OUTLINE, 5)
    for k in range(4):
        cr.move_to(20 + k * 52, -40)
        cr.line_to(46 + k * 52, -40)
        cr.line_to(26 + k * 52, 0)
        cr.line_to(0 + k * 52, 0)
        cr.close_path()
        paint(cr, hexc("#2b2b33"), None, 0)
    cr.restore()
    cr.restore()


def movie_camera(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for a in (-0.35, 0.0, 0.35):
        stroke_line(cr, [(0, 0), (math.sin(a) * 160, 160)], 10, hexc("#5a5a66"), curve=False)
    rrect(cr, -90, -70, 150, 90, 12)
    paint(cr, hexc("#3a3a44"), OUTLINE, 5)
    for cx in (-50, 20):
        ellipse(cr, cx, -110, 38, 38)
        paint(cr, hexc("#5a5a66"), OUTLINE, 5)
    cr.move_to(60, -50)
    cr.line_to(120, -80)
    cr.line_to(120, 10)
    cr.line_to(60, -10)
    cr.close_path()
    paint(cr, hexc("#5a5a66"), OUTLINE, 5)
    cr.restore()


def gavel(cr, t, x, y, s=1.0, swing=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -100, 40, 200, 30, 8)                                # the block
    paint(cr, hexc("#8a5a2b"), OUTLINE, 5)
    cr.translate(80, -60)
    cr.rotate(-0.9 * (1 - swing))
    stroke_line(cr, [(0, 0), (-150, 60)], 16, hexc("#a8703a"), curve=False)
    cr.save()
    cr.translate(-150, 60)
    cr.rotate(0.38)
    rrect(cr, -30, -60, 60, 120, 12)
    paint(cr, hexc("#8a5a2b"), OUTLINE, 5)
    cr.restore()
    cr.restore()


def bulb(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    soft_disc(cr, 0, -10, 110, (1, 0.95, 0.5, 0.5))
    ellipse(cr, 0, -20, 55, 60)
    paint(cr, hexc("#ffe46a"), OUTLINE, 5)
    rrect(cr, -26, 34, 52, 36, 8)
    paint(cr, hexc("#a8acb8"), OUTLINE, 4)
    cr.restore()


def brush(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.rotate(0.7)
    rrect(cr, -12, -90, 24, 120, 10)
    paint(cr, hexc("#c8703a"), OUTLINE, 4)
    rrect(cr, -16, 30, 32, 24, 4)
    paint(cr, hexc("#a8acb8"), OUTLINE, 4)
    cr.move_to(-16, 54)
    cr.curve_to(-18, 90, 0, 110, 0, 110)
    cr.curve_to(0, 110, 18, 90, 16, 54)
    cr.close_path()
    paint(cr, hexc("#e8473f"), OUTLINE, 4)
    cr.restore()


def girl(cr, t, tl, x, y, s=1.0, **kw):
    talker(cr, t, tl, "girl", "student2", x, y, s, **dict(GIRL, **kw))


def teacher(cr, t, tl, x, y, s=1.0, **kw):
    talker(cr, t, tl, "teacher", "teacher", x, y, s, **dict(TEACHER, **kw))


# ---------------------------------------------------------------- scenes
def scene_prize(cr, t, tl):
    A = tl.at
    plain(cr, *WALL)
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("a1", "computer"), (1.08, 360, 660))], dur=1.0))
    glitch = 0.0
    if A("a1", "computer") <= t < A("a1", "computer") + 1.2:
        glitch = 1 - seg(t, A("a1", "computer") + 0.6, A("a1", "computer") + 1.2)
    painting(cr, t, 360, 640, 1.0, glitch=glitch)
    ribbon(cr, t, 560, 790, 1.0)
    ring(cr, t, A("a1", "won"), 560, 800, 100, 100)
    cr.restore()
    sparkles(cr, t, A("a1", "contest"), 560, 790, n=8, col=GOLD, spread=120)
    vignette(cr, 0.3)


def scene_laptop(cr, t, tl):
    A = tl.at
    plain(cr, "#e8ecf4", "#d0d8e6")
    s0 = tl.scene_at(t)[1]
    n = int(len(PROMPT) * seg(t, A("a2", "typed"), A("a2", "wanted", end=True)))
    laptop(cr, t, 360, 830, 1.0, PROMPT[:n])
    paint_t = A("a2", "painted")
    painting(cr, t, 360, 400, 0.8, reveal=seg(t, paint_t, paint_t + 0.8))
    if t >= paint_t:
        for k in range(5):                                         # letters fly up into the canvas
            u = ((t - paint_t) * 1.6 + k / 5) % 1.0
            if t > paint_t + 1.0:
                break
            bold_text(cr, PROMPT[k * 5:k * 5 + 4], lerp(260 + k * 40, 360, u), lerp(680, 420, u), 28 * (1 - u * 0.5),
                      PURPLE, shadow=0)
    if t >= A("a2", "seconds"):
        tag(cr, t, A("a2", "seconds"), 360, 160, "IN SECONDS", col=GOLD, size=46)
    elif t >= s0:
        tag(cr, t, s0, 360, 160, "SHE TYPES...", col=BLUE, size=42)
    vignette(cr, 0.25)


def scene_class(cr, t, tl):
    A = tl.at
    room(cr, t)
    painting(cr, t, 360, 560, 0.45)
    teacher(cr, t, tl, 540, 1080, 1.0, facing=-1, arms=("point", "down"), brows="raise", eyes="half")
    girl(cr, t, tl, 170, 1050, 0.95, eyes="wide" if t >= A("a3", "artist") else "open", brows="up")
    if t >= A("a3", "artist"):
        card(cr, t, A("a3", "artist"), 360, 260, 420, 150, "ARTIST", ["COMPUTER?"], col=PURPLE, title_size=32,
             line_size=46)
    vignette(cr, 0.3)


def scene_director(cr, t, tl):
    A = tl.at
    plain(cr, "#2a2a3a", "#1a1a26")
    soft_disc(cr, 470, 560, 380, (1, 0.95, 0.8, 0.22))             # a spotlight
    if t >= A("a4", "director"):
        k = appear(t, A("a4", "director"), 0.4)
        director_chair(cr, 470, 820, 1.0 * k)
    if t >= A("a4", "camera"):
        k = appear(t, A("a4", "camera"), 0.4)
        movie_camera(cr, 560, 480, 0.9 * k)
        red_x(cr, t, A("a4", "holds"), 560, 420, 60)
    girl(cr, t, tl, 160, 1050, 0.95, arms=("out", "down"), brows="up")
    if t >= A("a4", "film", nth=2):
        clapper(cr, t, 330, 330, 0.9, snap=seg(t, A("a4", "film", nth=2), A("a4", "film", nth=2) + 0.2))
        cue("hit", t, A("a4", "film", nth=2) + 0.2)
    vignette(cr, 0.35)


def scene_fair(cr, t, tl):
    A = tl.at
    plain(cr, "#fdf2dc", "#f0d8b0")
    s0 = tl.scene_at(t)[1]
    for k in range(9):                                             # fair tent stripes
        cr.rectangle(k * 80, 0, 40, 110)
        cr.set_source_rgba(*RED[:3], 0.85)
        cr.fill()
    sign(cr, t, s0, 360, 200, "REAL STORY", col=RED, size=56, end=A("a5", "twenty") - 0.05)
    if t >= A("a5", "twenty"):
        stamp(cr, t, A("a5", "twenty"), 360, 220, "2022", col=BLUE, size=80)
    painting(cr, t, 360, 600, 0.85)
    if t >= A("a5", "first"):
        ribbon(cr, t, 540, 720, 1.1 * appear(t, A("a5", "first"), 0.4), text="1ST", col=BLUE)
    if t >= A("a5", "fair"):
        tag(cr, t, A("a5", "fair"), 330, 840, "JASON ALLEN · COLORADO STATE FAIR", col=GOLD, size=28)
    vignette(cr, 0.25)


def scene_owns(cr, t, tl):
    A = tl.at
    room(cr, t)
    teacher(cr, t, tl, 360, 1000, 0.9, arms=("shrug", "shrug"), brows="up", eyes="wide")
    for k, (x, who) in enumerate(((120, "student1"), (360, "student3"), (600, "student2"))):
        turn = seg(t, A("a6", "who"), A("a6", "who") + 0.3)
        person(cr, t, x, 1260, 0.85, who, facing=-1 if x > 360 else 1, eyes="wide", mouth="o", seed=k,
               look=(0.0, -0.6 * turn), arms=("down", "down"))
    if t >= A("a6", "owns"):
        sign(cr, t, A("a6", "owns"), 360, 220, "WHO OWNS IT?", col=PURPLE, size=64)
    vignette(cr, 0.35)


def scene_office(cr, t, tl):
    A = tl.at
    plain(cr, "#e8e4dc", "#d0c8b8")
    s0 = tl.scene_at(t)[1]
    card(cr, t, s0, 360, 520, 460, 400, "US COPYRIGHT", ["Application:", "AI-made picture", "Owner: ?"], col=BLUE,
         title_size=34, line_size=36)
    if t >= A("a7", "not"):
        stamp(cr, t, A("a7", "not"), 360, 600, "REFUSED", col=RED, size=80)
    if t >= A("a7", "human"):
        tag(cr, t, A("a7", "human"), 360, 230, "NOT ENOUGH HUMAN WORK", col=RED, size=40)
    if t >= A("a7", "court"):
        k = appear(t, A("a7", "court"), 0.3)
        g0 = A("a7", "court") + 0.15
        gavel(cr, t, 520, 820, 0.8 * k, swing=seg(t, g0, g0 + 0.15))
        cue("thud", t, g0 + 0.15)
    vignette(cr, 0.3)


def scene_split(cr, t, tl):
    A = tl.at
    plain(cr, "#f4ecf8", "#e2d4ec")
    sign(cr, t, tl.scene_at(t)[1], 360, 220, "WHAT MAKES IT ART?", col=PURPLE, size=50)
    for x in (190, 530):                                           # two empty cards wait for their word
        rrect(cr, x - 150, 360, 300, 400, 24)
        paint(cr, alpha(WHITE, 0.45), alpha(OUTLINE, 0.35), 5)
        bold_text(cr, "?", x, 600, 120, alpha(OUTLINE, 0.25), outline=None, shadow=0)
    if t >= A("a8", "idea"):
        k = appear(t, A("a8", "idea"), 0.4)
        cr.save()
        cr.translate(190, 560)
        cr.scale(k, k)
        rrect(cr, -150, -200, 300, 400, 24)
        paint(cr, WHITE, OUTLINE, 6)
        bulb(cr, 0, -40, 1.1)
        bold_text(cr, "IDEA", 0, 150, 60, GOLD)
        cr.restore()
    if t >= A("a8", "skill"):
        k = appear(t, A("a8", "skill"), 0.4)
        cr.save()
        cr.translate(530, 560)
        cr.scale(k, k)
        rrect(cr, -150, -200, 300, 400, 24)
        paint(cr, WHITE, OUTLINE, 6)
        brush(cr, 0, -50, 1.1)
        bold_text(cr, "SKILL", 0, 150, 60, BLUE)
        cr.restore()
        bold_text(cr, "VS", 360, 580, 70, RED)
    vignette(cr, 0.25)


def scene_end(cr, t, tl):
    A = tl.at
    plain(cr, *WALL)
    painting(cr, t, 400, 640, 0.75)
    ribbon(cr, t, 540, 740, 0.8)
    girl(cr, t, tl, 140, 1060, 0.85, arms=("hips", "down"), eyes="half", mouth="smug")
    sign(cr, t, A("a9", "painting"), 360, 210, "WHOSE PAINTING?", col=GOLD, size=56)
    buttons(cr, t, A("a9", "machine"), [("MINE", GREEN), ("THE MACHINE'S", RED)], y=370, size=40, w=300)
    vignette(cr, 0.3)


SCENES = {"prize": scene_prize, "laptop": scene_laptop, "class": scene_class, "director": scene_director,
          "fair": scene_fair, "owns": scene_owns, "office": scene_office, "split": scene_split, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    hook2(cr, t, "1ST PRIZE. PAINTED BY", "AI", end=tl.at("a1", end=True), y=190, big_at=tl.at("a1", "won"),
          mark="circle", mark_at=tl.at("a1", "computer"))
    captions(cr, t, tl)
