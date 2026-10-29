"""Row 77: "Her Rat Walked Straight Up to the Cat" -- Toxoplasma and the rats that stop fearing cats, told through a
girl and a vet, in the polished look, built on the Meanwhile Mayank frame-0 rules (one subject on a plain ground,
two-tier hook with a red mark).

Script: out/scripts_slots_75-81.md (owner, 29 Oct 2026: "Make it from research currently did"). Source: Berdoy,
Webster & Macdonald, "Fatal attraction in rats infected with Toxoplasma gondii", Proc. R. Soc. B (2000): infected rats
lost their avoidance of cat odour and some were drawn to it. About a third of people carry the parasite (estimates
vary); effects on human behaviour are disputed, so the video claims none. Turbo stock female narrator with tags; the
girl and the vet through Turbo with Kokoro reference voices.
"""
import math

from motion import voice
from motion.engine import W, H, cue, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, bubble, buttons, red_x, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, lin, paint,
                           rad, rrect, sign, smooth, soft_disc, stroke_line, vignette)
from motion.toons import person
from videos.bq_kit import hook2, plain, ring, talker
from videos.cat_mayor import cat

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "r7"          # music drops out under "one in three people" (research 18 Oct 2026, A5)
SERIES = "Interestingly Strange"
END_TAG = "Subscribe · a new question tomorrow"      # alternate videos test the silent subscribe wording (research E4/E5)
voice.SPEAKERS.update({"girl": dict(voice="af_sky", speed=1.05, turbo_ref="af_sky+3"),
                       "vet": dict(voice="am_adam", speed=1.0, turbo_ref="am_adam")})
GIRL = dict(skin="tan", hair="pony", hair_col=hexc("#2b1a12"), shirt=hexc("#f29ab0"), tie=None,
            pants=hexc("#3b4a7a"))
PINK = hexc("#ffa8b8")
GERM = hexc("#7ae86a")
CREAM = ("#f6ecd8", "#e6d8bc")

SCRIPT = [
    dict(id="r1", scene="rat", text="Doctor, why does my rat walk straight up to our cat?", speaker="girl"),
    dict(id="r2", scene="rat", text="Your rat isn't brave. Something inside it wants the cat to eat it.",
         speaker="vet"),
    dict(id="r3", scene="cycle", text="It's a parasite called Toxoplasma. It can only breed inside a cat."),
    dict(id="r4", scene="smell", text="So it changes the rat. The smell of a cat stops meaning danger."),
    dict(id="r5", scene="study", text="In [two thousand,|2000,] Oxford scientists tested it. Healthy rats avoided cat "
                                      "smell. Infected rats stopped avoiding it. Some even went looking for it."),
    dict(id="r6", scene="people", text="Wait. Can people catch it too?", speaker="girl"),
    dict(id="r7", scene="carry", text="About one in three people carry it. Mostly from undercooked meat, or cat "
                                      "litter.", speaker="vet", gap=0.4),
    dict(id="r8", scene="argue", text="Scientists still argue whether it changes people at all. [gasp]"),
    dict(id="r9", scene="end", text="So, if a germ can change what you want, is it still your choice? Or the germ's?",
         gap=0.3),
]

METADATA = dict(
    title="Her Rat Walked Straight Up to the Cat 🐀",
    alt_titles=["This Germ Makes Rats Love Cats 🐀", "Something Inside It Wants to Be Eaten 🐀"],
    description="""A girl asks the vet why her rat walks straight up to the cat. The answer: something inside it wants the cat to eat it. 🐀

It's a parasite called Toxoplasma gondii, and it can only breed inside a cat. In infected rats, the smell of a cat stops meaning danger. In 2000, Oxford scientists tested it: healthy rats avoided cat smell, infected rats stopped avoiding it, and some even went looking for it.

About one in three people carry it too (estimates vary), mostly from undercooked meat or cat litter. Whether it changes people at all is still argued about, and this video claims nothing either way.

Source: Berdoy, Webster & Macdonald, "Fatal attraction in rats infected with Toxoplasma gondii", Proceedings of the Royal Society B (2000).

💬 If a germ can change what you want, is it still your choice? Or the germ's? 👇

🔔 Interestingly Strange: weird animals, clever twists and mind-bending questions, animated in under a minute.""",
    hashtags=["#Toxoplasma", "#WeirdScience", "#Shorts"],
    tags=["toxoplasma", "toxoplasma gondii", "rat and cat parasite", "mind control parasite", "weird animals",
          "parasite facts", "free will", "biology facts", "science shorts", "interestingly strange"],
    pinned_comment="If a germ changes what you want... is it still YOUR choice? MY CHOICE or THE GERM'S? 👇",
)


# ---------------------------------------------------------------- the rat, the germ, the cat's eyes
def rat(cr, t, x, y, s=1.0, facing=1, walk=None, eyes="open", glow=0.0):
    """A grey pet rat in side view, feet at (x, y), nose toward +x (facing=1). `glow` lights the germ in its head."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s * facing, s)
    sw = math.sin(t * 3) * 10
    tail = [(-80, -30), (-160, -10 + sw), (-232, -40 - sw)]
    stroke_line(cr, tail, 17, OUTLINE)
    stroke_line(cr, tail, 9, PINK)
    for k, lx in enumerate((-50, 52)):
        dx = 14 * math.sin(walk + k * math.pi) if walk is not None else 0
        ellipse(cr, lx + dx, -8, 26, 13)
        paint(cr, PINK, OUTLINE, 4)
    ellipse(cr, -5, -55, 100, 56)
    paint(cr, rad(-20, -95, 140, [(0, hexc("#c8c4cc")), (1, hexc("#8a8690"))]), OUTLINE, 6)
    smooth(cr, [(50, -96), (112, -92), (160, -64), (180, -47), (160, -33), (110, -26), (58, -30)])
    paint(cr, rad(100, -80, 90, [(0, hexc("#d4d0d8")), (1, hexc("#9a96a0"))]), OUTLINE, 6)
    ellipse(cr, 80, -102, 28, 32)
    paint(cr, hexc("#b0acb6"), OUTLINE, 5)
    ellipse(cr, 82, -99, 16, 20)
    paint(cr, PINK, None, 0)
    if glow > 0:
        pulse = 1 + 0.15 * math.sin(t * 7)
        soft_disc(cr, 100, -64, 60 * glow * pulse, (0.5, 1, 0.4, 0.55 * glow))
        ellipse(cr, 100, -64, 13 * glow * pulse, 8 * glow * pulse, 0.5)
        paint(cr, GERM, OUTLINE, 3)
    if eyes == "happy":
        stroke_line(cr, [(118, -66), (128, -76), (138, -66)], 5, OUTLINE)
    else:
        ellipse(cr, 128, -68, 9, 10)
        paint(cr, hexc("#1b1b1f"), None, 0)
        cr.arc(131, -72, 3, 0, 2 * math.pi)
        paint(cr, WHITE, None, 0)
    ellipse(cr, 180, -47, 9, 8)
    paint(cr, PINK, OUTLINE, 3)
    for k in (-1, 0, 1):
        stroke_line(cr, [(166, -44), (220, -48 + k * 13)], 2.5, OUTLINE, curve=False)
    cr.restore()


def germ(cr, t, x, y, s=1.0, face=True):
    """Toxoplasma drawn as its real crescent shape, with a cheeky face."""
    cr.save()
    cr.translate(x, y + 6 * math.sin(t * 3))
    cr.rotate(0.25 * math.sin(t * 2))
    cr.scale(s, s)
    soft_disc(cr, 0, 0, 150, (0.5, 1, 0.4, 0.25))
    cr.move_to(-110, 20)
    cr.curve_to(-80, -90, 80, -90, 110, 20)
    cr.curve_to(60, -30, -60, -30, -110, 20)
    cr.close_path()
    paint(cr, lin(0, -70, 0, 20, [(0, hexc("#b4ff9a")), (1, GERM)]), OUTLINE, 6)
    ellipse(cr, 10, -32, 18, 14)
    paint(cr, hexc("#3a9a4a"), None, 0)
    if face:
        for ex in (-30, 30):
            ellipse(cr, ex, -48, 7, 8)
            paint(cr, OUTLINE, None, 0)
        stroke_line(cr, [(-14, -30), (0, -24), (14, -30)], 4, OUTLINE)
    cr.restore()


def cat_eyes(cr, t, x, y, s=1.0, open_=1.0):
    """Two yellow cat eyes in a dark patch at the edge of frame."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ellipse(cr, 0, 0, 230, 170)
    cr.set_source(rad(0, 0, 230, [(0, (0.08, 0.06, 0.1, 0.9)), (0.6, (0.08, 0.06, 0.1, 0.6)),
                                  (1, (0.08, 0.06, 0.1, 0.0))]))
    cr.fill()
    blink = 0.12 if (t * 0.6) % 3.4 < 0.1 else 1.0
    h = 38 * open_ * blink
    for ex in (-60, 60):
        cr.save()
        cr.translate(ex, 0)
        cr.move_to(-46, 0)
        cr.curve_to(-20, -h, 20, -h, 46, 0)
        cr.curve_to(20, h, -20, h, -46, 0)
        cr.close_path()
        paint(cr, hexc("#ffd23a"), OUTLINE, 4)
        if h > 8:
            ellipse(cr, 0, 0, 7, h * 0.8)
            paint(cr, OUTLINE, None, 0)
        cr.restore()
    cr.restore()


def smell_waves(cr, t, start, x0, x1, y):
    if t < start:
        return
    for k in range(3):
        u = ((t - start) * 0.6 + k / 3) % 1.0
        x = lerp(x0, x1, u)
        a = math.sin(u * math.pi)
        pts = [(x + 18 * math.sin(j * 1.4 + t * 3), y - 50 + j * 25) for j in range(5)]
        stroke_line(cr, pts, 9, alpha(hexc("#c890e8"), a))


def rat_box(cr, t, x, y, label, col):
    """A test box seen from above, with a cat-smell corner (top right)."""
    rrect(cr, x - 160, y - 210, 320, 420, 16)
    paint(cr, hexc("#f4efe4"), OUTLINE, 6)
    ellipse(cr, x + 110, y - 160, 90, 90)
    cr.set_source(rad(x + 110, y - 160, 90, [(0, (0.78, 0.56, 0.9, 0.6)), (1, (0.78, 0.56, 0.9, 0.0))]))
    cr.fill()
    for dx, dy in ((0, 0), (-18, -20), (0, -28), (18, -20)):       # a paw print = cat smell
        ellipse(cr, x + 110 + dx, y - 150 + dy * 1.2, 11 if dy else 16, 11 if dy else 13)
        paint(cr, hexc("#8a5aa8"), None, 0)
    bold_text(cr, "CAT SMELL", x + 80, y - 95, 22, hexc("#8a5aa8"), outline=None, shadow=0)
    bold_text(cr, label, x, y - 235, 40, col)


def plate(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ellipse(cr, 0, 0, 90, 40)
    paint(cr, WHITE, OUTLINE, 5)
    ellipse(cr, 0, -6, 52, 24)
    paint(cr, hexc("#d8606a"), OUTLINE, 4)
    stroke_line(cr, [(-20, -10), (10, -2)], 5, hexc("#f4c8c8"), curve=False)
    cr.restore()


def litter_box(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.move_to(-90, -30)
    cr.line_to(90, -30)
    cr.line_to(70, 40)
    cr.line_to(-70, 40)
    cr.close_path()
    paint(cr, hexc("#5ab0d8"), OUTLINE, 5)
    ellipse(cr, 0, -30, 88, 14)
    paint(cr, hexc("#e8dcc0"), OUTLINE, 4)
    cr.restore()


def girl(cr, t, tl, x, y, s=1.0, **kw):
    talker(cr, t, tl, "girl", "student1", x, y, s, **dict(GIRL, **kw))


def vet(cr, t, tl, x, y, s=1.0, **kw):
    talker(cr, t, tl, "vet", "doctor", x, y, s, **kw)


# ---------------------------------------------------------------- scenes
def scene_rat(cr, t, tl):
    A = tl.at
    plain(cr, *CREAM)
    zoom = A("r2", "Something")
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (zoom, (1.9, 330, 690))], dur=0.6))
    cat_eyes(cr, t, 590, 560, 1.0, open_=1.0 if t < A("r2", "eat") else 0.55)
    x = lerp(130, 250, seg(t, 0, A("r1", end=True)))
    rat(cr, t, x, 800, 1.45, walk=t * 7 if t < A("r1", end=True) else None,
        glow=appear(t, zoom + 0.3, 0.5) if t >= zoom + 0.3 else 0.0)
    cr.restore()
    if t >= A("r2", "eat"):
        tag(cr, t, A("r2", "eat"), 360, 470, "IT WANTS THIS", col=RED, size=44)
    vignette(cr, 0.3)


def scene_cycle(cr, t, tl):
    A = tl.at
    plain(cr, "#eaf4ec", "#d4e8d8")
    s0 = tl.scene_at(t)[1]
    cr.save()
    k = appear(t, s0, 0.4)
    cr.translate(190, 600)
    cr.scale(k, k)
    germ(cr, t, 0, 0, 1.25)
    cr.restore()
    cat(cr, t, 530, 830, 0.95, tie=False, eyes="half" if t < A("r3", "breed") else "open")
    if t >= A("r3", "Toxoplasma"):
        sign(cr, t, A("r3", "Toxoplasma"), 360, 230, "TOXOPLASMA", col=GREEN, size=60)
    if t >= A("r3", "breed"):
        u = seg(t, A("r3", "breed"), A("r3", "breed") + 0.4)
        stroke_line(cr, [(290, 640), (lerp(290, 450, u), lerp(640, 740, u))], 12, RED)
    if t >= A("r3", "inside"):
        ring(cr, t, A("r3", "inside"), 530, 760, 90, 80)
        tag(cr, t, A("r3", "inside"), 400, 420, "BREEDS ONLY IN CATS", col=RED, size=40)
    vignette(cr, 0.3)


def scene_smell(cr, t, tl):
    A = tl.at
    plain(cr, *CREAM)
    s0 = tl.scene_at(t)[1]
    stopped = t >= A("r4", "stops")
    rat(cr, t, 150, 800, 0.9, eyes="happy" if stopped else "open",
        glow=1.0 if t >= A("r4", "changes") else 0.4)
    cat(cr, t, 560, 820, 0.85, tie=False, eyes="half")
    smell_waves(cr, t, A("r4", "smell"), 470, 260, 640)
    sign(cr, t, s0, 190, 470, "DANGER", col=RED, size=52)
    if stopped:
        red_x(cr, t, A("r4", "stops"), 190, 455, 70)
    if t >= A("r4", "changes"):
        tag(cr, t, A("r4", "changes"), 360, 220, "THE GERM REWIRES IT", col=GREEN, size=40)
    vignette(cr, 0.3)


def scene_study(cr, t, tl):
    A = tl.at
    plain(cr, "#e8ecf4", "#d4dae8")
    s0 = tl.scene_at(t)[1]
    tag(cr, t, s0, 360, 200, "2000 · OXFORD", col=BLUE, size=46)
    rat_box(cr, t, 185, 600, "HEALTHY", GREEN)
    rat_box(cr, t, 535, 600, "INFECTED", RED)
    # healthy rat runs to the far corner when its line comes
    u = seg(t, A("r5", "avoided"), A("r5", "avoided") + 0.5)
    rat(cr, t, lerp(190, 150, u), lerp(660, 730, u), 0.55, facing=1 if u < 0.05 else -1,
        walk=t * 12 if 0 < u < 1 else None)
    # the infected one stays put, then walks into the cat smell
    v = seg(t, A("r5", "looking"), A("r5", "looking") + 0.6)
    rat(cr, t, lerp(500, 540, v), lerp(700, 500, v), 0.55, walk=t * 9 if 0 < v < 1 else None, glow=0.8,
        eyes="happy" if v > 0.9 else "open")
    if t >= A("r5", "avoided"):
        bold_text(cr, "RUNS AWAY", 185, 790, 34, GREEN)
    if t >= A("r5", "stopped"):
        bold_text(cr, "STAYS", 535, 790, 34, RED)
    if t >= A("r5", "looking"):
        ring(cr, t, A("r5", "looking"), 645, 440, 80, 70)
    vignette(cr, 0.25)


def clinic(cr):
    plain(cr, "#e6f0f4", "#cfdee6")
    rrect(cr, 200, 760, 320, 40, 10)                               # exam table
    paint(cr, hexc("#b8c4cc"), OUTLINE, 5)
    for lx in (230, 490):
        rrect(cr, lx - 8, 800, 16, 200, 6)
        paint(cr, hexc("#8a96a0"), OUTLINE, 4)


def scene_people(cr, t, tl):
    A = tl.at
    clinic(cr)
    rat(cr, t, 360, 760, 0.55, glow=0.6)
    wide = t >= A("r6", "Wait")
    girl(cr, t, tl, 150, 1060, 0.95, eyes="wide" if wide else "open", brows="up", arms=("front", "front"),
         look=(0.0, 0.4))
    vet(cr, t, tl, 580, 1080, 0.95, facing=-1, eyes="open", arms=("hips", "down"))
    if t >= A("r6", "people"):
        sign(cr, t, A("r6", "people"), 360, 230, "PEOPLE TOO?", col=PURPLE, size=60)
    vignette(cr, 0.3)


def scene_carry(cr, t, tl):
    A = tl.at
    plain(cr, "#f2ece0", "#e2d8c4")
    s0 = tl.scene_at(t)[1]
    for k, x in enumerate((160, 360, 560)):
        hit = k == 1 and t >= A("r7", "three")
        if hit:
            soft_disc(cr, x, 680, 200, (0.5, 1, 0.4, 0.5))
        person(cr, t, x, 900, 0.5, ("fermi", "student1", "grandpa")[k], seed=k, eyes="wide" if hit else "open")
    if t >= A("r7", "one"):
        k = appear(t, A("r7", "one"), 0.35)
        cr.save()
        cr.translate(360, 260)
        cr.scale(k, k)
        bold_text(cr, "1 IN 3", 0, 0, 120, GOLD)
        bold_text(cr, "PEOPLE", 0, 70, 50, WHITE)
        cr.restore()
        cue("hit", t, A("r7", "one"))
    if t >= A("r7", "meat"):
        k = appear(t, A("r7", "meat"), 0.35)
        plate(cr, 190, 440, k)
    if t >= A("r7", "litter"):
        k = appear(t, A("r7", "litter"), 0.35)
        litter_box(cr, 530, 440, k)
    vignette(cr, 0.25)


def scene_argue(cr, t, tl):
    A = tl.at
    plain(cr, "#e8ecf4", "#d4dae8")
    s0 = tl.scene_at(t)[1]
    person(cr, t, 170, 1060, 0.9, "doctor2", arms=("point", "down"), mouth="open", brows="angry")
    person(cr, t, 550, 1060, 0.9, "doctor", facing=-1, arms=("shrug", "shrug"), mouth="flat", brows="raise")
    bold_text(cr, "?", 360, 640 + 10 * math.sin(t * 3), 160, GOLD)
    sign(cr, t, s0, 360, 220, "DOES IT CHANGE PEOPLE?", col=PURPLE, size=44)
    bubble(cr, t, A("r8", "argue"), 200, 390, "MAYBE A LITTLE!", col=WHITE, size=34, tail=1)
    bubble(cr, t, A("r8", "changes"), 520, 470, "NO PROOF!", col=WHITE, size=34, tail=-1)
    vignette(cr, 0.3)


def scene_end(cr, t, tl):
    A = tl.at
    plain(cr, *CREAM)
    cat_eyes(cr, t, 590, 600, 0.9)
    rat(cr, t, 250, 820, 1.3, glow=1.0)
    sign(cr, t, A("r9", "change"), 360, 210, "WHOSE CHOICE?", col=GOLD, size=60)
    buttons(cr, t, A("r9", "germ", nth=2), [("MY CHOICE", GREEN), ("THE GERM'S", RED)], y=380, size=44, w=300)
    vignette(cr, 0.3)


SCENES = {"rat": scene_rat, "cycle": scene_cycle, "smell": scene_smell, "study": scene_study,
          "people": scene_people, "carry": scene_carry, "argue": scene_argue, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    hook2(cr, t, "THIS RAT IS NOT", "AFRAID", end=tl.at("r2", "brave", end=True) + 0.3, y=200,
          big_at=tl.at("r1", "straight"), mark="strike", mark_at=tl.at("r2", "brave"))
    captions(cr, t, tl)
