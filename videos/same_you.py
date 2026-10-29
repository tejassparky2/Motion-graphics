"""Row 79: "Grandpa Says the Boy in This Photo Is Gone" -- how much of you is replaced over a life, and the part that
isn't, told by a grandpa and his granddaughter in the polished look, built on the Meanwhile Mayank frame-0 rules
(one subject on a plain ground, two-tier hook with a red mark).

Script: out/scripts_slots_75-81.md (owner, 29 Oct 2026: "Make it from research currently did"). Source: Spalding,
Bhardwaj, Buchholz, Druid & Frisén, "Retrospective birth dating of cells in humans", Cell (2005): carbon-14 from the
1950s-60s bomb tests showed cortical neurons are as old as the person. Red blood cells live about 120 days; the
skin's outer layer renews in weeks; bone is remodelled continuously. The "every cell in 7 years" claim is a myth and
is left out. Turbo stock female narrator with tags; Grandpa and the girl through Turbo with Kokoro reference voices.
"""
import math

from motion import voice
from motion.engine import W, H, cue, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, check, sparkles, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, lin, paint,
                           rad, rrect, sign, smooth, soft_disc, stroke_line, vignette)
from motion.toons import person
from videos.bq_kit import hook2, plain, ring, talker

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "p7"          # music drops out under the brain-cell answer (research 18 Oct 2026, A5)
SERIES = "Big Questions"
voice.SPEAKERS.update({"grandpa": dict(voice="bm_george", speed=0.95, turbo_ref="bm_george-1.5"),
                       "girl": dict(voice="af_heart", speed=1.05, turbo_ref="af_heart+3")})
GIRL = dict(skin="olive", hair="bun", hair_col=hexc("#2b1a12"), shirt=hexc("#f4c430"), tie=None,
            pants=hexc("#2f6a7a"))
SEPIA = dict(skin=hexc("#e2c8a0"), hair="spiky", hair_col=hexc("#5a4030"), shirt=hexc("#efe0c4"),
             pants=hexc("#8a7050"), tie=hexc("#a08060"), shoes=hexc("#5a4030"))
WARM = ("#ddd4c8", "#c4b8a8")
OLD_SKIN = hexc("#d8a07a")

SCRIPT = [
    dict(id="p1", scene="photo", text="This little boy is me. But most of his body isn't in me anymore.",
         speaker="grandpa"),
    dict(id="p2", scene="room", text="How? You're right here.", speaker="girl"),
    dict(id="p3", scene="blood", text="Your red blood cells only live about four months."),
    dict(id="p4", scene="skin", text="The outer layer of your skin is replaced every few weeks."),
    dict(id="p5", scene="bone", text="Even your bones are slowly taken apart and rebuilt."),
    dict(id="p6", scene="same", text="So is anything still the same?", speaker="girl"),
    dict(id="p7", scene="brain", text="Yes. Most of the brain cells you think with are as old as you. Scientists "
                                      "proved it with carbon left over from old atom bomb tests. [gasp]", gap=0.4),
    dict(id="p8", scene="tap", text="So the boy's brain stayed. The rest of him moved out.", speaker="grandpa"),
    dict(id="p9", scene="end", text="So, are you still the person you were at five? Or someone new with the same "
                                    "name?", gap=0.3),
]

METADATA = dict(
    title="Grandpa Says the Boy in This Photo Is Gone 📷",
    alt_titles=["Is This Still You? Your Body Says No 📷", "Most of You Is New. Except This. 📷"],
    description="""Grandpa holds up a photo of himself at five: "This little boy is me. But most of his body isn't in me anymore." 📷

Your red blood cells live about four months. The outer layer of your skin is replaced every few weeks. Even your bones are slowly taken apart and rebuilt.

So is anything still the same? Yes: most of the brain cells you think with are as old as you. Scientists proved it in 2005 using carbon-14 left in the air by the atom bomb tests of the 1950s and 60s.

(The famous "every cell is replaced every 7 years" line is a myth, so it's not in this video.)

Source: Spalding, Bhardwaj, Buchholz, Druid & Frisén, "Retrospective birth dating of cells in humans", Cell (2005).

💬 Are you still the person you were at five? Or someone new with the same name? 👇

🔔 Interestingly Strange: mind-bending questions, clever twists and strange true facts, animated in under a minute.""",
    hashtags=["#ShipOfTheseus", "#HumanBody", "#Shorts"],
    tags=["ship of theseus", "are you the same person", "body cells replaced", "brain cells age", "carbon 14 dating",
          "human body facts", "philosophy shorts", "identity", "big questions", "interestingly strange"],
    pinned_comment="Are you still the kid in your old photos? SAME ME or SOMEONE NEW? Tell me why 👇",
)


# ---------------------------------------------------------------- props
def old_photo(cr, t, x, y, s=1.0, fade_body=0.0, rot=-0.04):
    """A sepia photo of a little boy (Grandpa at five), white border, centre (x, y). Returns the face position."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    rrect(cr, -200, -250, 400, 500, 8)
    paint(cr, hexc("#f6f0e2"), OUTLINE, 6)
    cr.save()
    cr.rectangle(-175, -225, 350, 400)
    cr.clip()
    cr.set_source(lin(0, -225, 0, 175, [(0, hexc("#c8b08a")), (1, hexc("#a88a64"))]))
    cr.paint()
    person(cr, t, 0, 260, 0.95, "kid", bob=False, shadow=False, mouth="grin", **SEPIA)
    if fade_body > 0:                                              # his body fades out of the picture, the head stays
        cr.rectangle(-175, -20, 350, 200)
        cr.set_source_rgba(0.78, 0.69, 0.54, 0.75 * fade_body)
        cr.fill()
    cr.set_source_rgba(0.55, 0.4, 0.2, 0.18)
    cr.paint()
    cr.restore()
    cr.restore()


def old_hand(cr, x, y, s=1.0, rot=0.0):
    """A wrinkled hand from the bottom right, thumb pressing on the photo corner."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    rrect(cr, 40, 10, 320, 120, 50)                                # cardigan sleeve
    paint(cr, hexc("#8a6a4a"), OUTLINE, 6)
    ellipse(cr, 0, 40, 90, 66)                                     # back of the hand
    paint(cr, rad(-20, 20, 110, [(0, shade_skin(0.1)), (1, OLD_SKIN)]), OUTLINE, 6)
    ellipse(cr, -70, -10, 30, 52, -0.6)                            # thumb on the photo
    paint(cr, OLD_SKIN, OUTLINE, 5)
    for k in range(3):                                             # wrinkles and a spot
        stroke_line(cr, [(-30 + k * 22, 20), (-20 + k * 22, 36), (-30 + k * 22, 52)], 3, alpha(OUTLINE, 0.45))
    ellipse(cr, 30, 60, 8, 6)
    paint(cr, hexc("#b87a5a"), None, 0)
    cr.restore()


def shade_skin(k):
    return tuple(min(1.0, c + k) for c in OLD_SKIN[:3]) + (1.0,)


def blood_cell(cr, t, x, y, r, k=1.0):
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y + 8 * math.sin(t * 2))
    cr.scale(k, k * 0.92)
    ellipse(cr, 0, 0, r, r)
    paint(cr, rad(-r * 0.3, -r * 0.3, r * 1.2, [(0, hexc("#ff6a6a")), (1, hexc("#c8202a"))]), OUTLINE, 7)
    ellipse(cr, 0, 0, r * 0.45, r * 0.45)
    paint(cr, alpha(hexc("#8a1018"), 0.45), None, 0)
    cr.restore()


def brain(cr, t, x, y, s=1.0, glow=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    if glow > 0:
        soft_disc(cr, 0, 0, 260 * (1 + 0.05 * math.sin(t * 5)), (1, 0.85, 0.4, 0.5 * glow))
    smooth(cr, [(-150, 20), (-160, -50), (-110, -110), (-30, -130), (50, -125), (130, -90), (160, -20), (140, 50),
                (80, 80), (0, 70), (-80, 80)])
    paint(cr, rad(-30, -60, 200, [(0, hexc("#ffc4d0")), (1, hexc("#f08aa4"))]), OUTLINE, 7)
    for pts in ([(-110, -60), (-70, -90), (-40, -50), (-80, -20)], [(-20, -100), (10, -60), (40, -95)],
                [(60, -70), (100, -40), (70, 0), (110, 30)], [(-100, 30), (-50, 10), (-20, 50)],
                [(0, -20), (30, 20), (0, 40)]):
        stroke_line(cr, pts, 5, alpha(OUTLINE, 0.55))
    stroke_line(cr, [(0, -125), (0, 70)], 5, alpha(OUTLINE, 0.45), curve=False)
    stroke_line(cr, [(40, 70), (60, 140)], 34, OUTLINE, curve=False)       # brain stem
    stroke_line(cr, [(40, 70), (60, 140)], 24, hexc("#f08aa4"), curve=False)
    cr.restore()


def bomb_cloud(cr, x, y, k):
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    rrect(cr, -18, -60, 36, 70, 10)
    paint(cr, hexc("#c8b8a8"), OUTLINE, 4)
    for dx, dy, r in ((-40, -80, 34), (0, -96, 42), (40, -80, 34), (0, -70, 30)):
        ellipse(cr, dx, dy, r, r * 0.8)
        paint(cr, hexc("#ffb05a"), OUTLINE, 4)
    ellipse(cr, 0, 12, 70, 14)
    paint(cr, hexc("#a89888"), OUTLINE, 4)
    cr.restore()


def grandpa(cr, t, tl, x, y, s=1.0, **kw):
    talker(cr, t, tl, "grandpa", "grandpa", x, y, s, **kw)


def girl(cr, t, tl, x, y, s=1.0, **kw):
    talker(cr, t, tl, "girl", "student1", x, y, s, **dict(GIRL, **kw))


def living_room(cr):
    plain(cr, "#efe2cc", "#d8c4a4")
    cr.rectangle(0, 1010, W, H - 1010)
    cr.set_source_rgb(*hexc("#a8805a")[:3])
    cr.fill()
    rrect(cr, 470, 300, 150, 120, 6)                               # a frame on the wall
    paint(cr, hexc("#c8b08a"), hexc("#7a5a3a"), 10)


# ---------------------------------------------------------------- scenes
def scene_photo(cr, t, tl):
    A = tl.at
    plain(cr, *WARM)
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("p1", "most"), (1.08, 360, 660))], dur=1.2))
    old_photo(cr, t, 360, 640, 1.0, fade_body=seg(t, A("p1", "body"), A("p1", "anymore", end=True)))
    old_hand(cr, 560, 880, 1.0, rot=-0.2)
    ring(cr, t, A("p1", "me"), 364, 528, 115, 120)
    cr.restore()
    if t >= A("p1", "body"):
        tag(cr, t, A("p1", "body"), 360, 740, "GONE?", col=RED, size=44)
    vignette(cr, 0.3)


def scene_room(cr, t, tl):
    A = tl.at
    living_room(cr)
    grandpa(cr, t, tl, 470, 1080, 1.0, facing=-1, eyes="happy", arms=("hold", "down"))
    girl(cr, t, tl, 200, 1060, 0.95, eyes="wide", brows="up",
         arms=("point" if t >= A("p2", "right") else "hips", "down"))
    if t >= A("p2", "right"):
        tag(cr, t, A("p2", "right"), 470, 330, "RIGHT HERE!", col=PURPLE, size=44)
    vignette(cr, 0.3)


def scene_blood(cr, t, tl):
    A = tl.at
    plain(cr, "#fbe8e4", "#f0cccc")
    s0 = tl.scene_at(t)[1]
    pop = A("p3", "months", end=True) + 0.15
    k = appear(t, s0, 0.4) * (1 - seg(t, pop, pop + 0.15))
    blood_cell(cr, t, 360, 560, 170, k)
    if t >= pop + 0.15:
        blood_cell(cr, t, 360, 560, 170, appear(t, pop + 0.35, 0.4) if t >= pop + 0.35 else 0)
        sparkles(cr, t, pop, 360, 560, n=10, col=hexc("#ff6a6a"), spread=200)
        tag(cr, t, pop + 0.35, 360, 790, "A NEW ONE", col=GREEN, size=36)
    if t >= A("p3", "four"):
        card(cr, t, A("p3", "four"), 360, 230, 360, 150, "LIFESPAN", ["~4 MONTHS"], col=RED, title_size=30,
             line_size=46)
    vignette(cr, 0.25)


def scene_skin(cr, t, tl):
    A = tl.at
    plain(cr, "#f6eadc", "#e8d4bc")
    s0 = tl.scene_at(t)[1]
    cols = ("#f8d8b8", "#f0c09a", "#e0a07a", "#c87a5a")             # outer layer first
    for k in (3, 2, 1, 0):
        rrect(cr, 60, 510 + 70 * k, 600, 80, 14)
        paint(cr, hexc(cols[k]), OUTLINE, 5)
    tag(cr, t, s0, 360, 440, "OUTER LAYER", col=GOLD, size=36, end=A("p4", "replaced"))
    flake = seg(t, A("p4", "replaced"), A("p4", "replaced") + 1.2)
    for j in range(6):                                             # the top layer flakes off ...
        fx = 110 + j * 100 + 20 * math.sin(j * 2.1)
        fy = 510 - 260 * flake - 30 * (j % 2) * flake
        cr.save()
        cr.translate(fx, fy)
        cr.rotate(flake * (1.5 if j % 2 else -1.2))
        rrect(cr, -44, -16, 88, 32, 8)
        paint(cr, alpha(hexc(cols[0]), 1 - 0.6 * flake), alpha(OUTLINE, 1 - 0.6 * flake), 4)
        cr.restore()
    if t >= A("p4", "weeks"):                                       # ... and a new one rises underneath
        u = seg(t, A("p4", "weeks"), A("p4", "weeks") + 0.5)
        rrect(cr, 60, lerp(580, 500, u), 600, 40, 10)
        paint(cr, hexc("#fff0dc"), OUTLINE, 4)
        tag(cr, t, A("p4", "weeks"), 360, 230, "EVERY FEW WEEKS", col=BLUE, size=46)
    vignette(cr, 0.25)


def scene_bone(cr, t, tl):
    A = tl.at
    plain(cr, "#e8eef4", "#d0dae4")
    for lw in (14, 0):                                             # a thick outline under the fill = one shape
        cr.save()
        cr.translate(360, 600)
        cr.rotate(-0.35)
        cr.new_path()
        rrect(cr, -220, -40, 440, 80, 30)
        for sx in (-1, 1):
            ellipse(cr, sx * 230, -40, 52, 52)
            ellipse(cr, sx * 230, 40, 52, 52)
        if lw:
            cr.set_source_rgba(*OUTLINE)
            cr.set_line_width(lw)
            cr.stroke()
        else:
            cr.set_source_rgb(*hexc("#f6f0e0")[:3])
            cr.fill()
        cr.restore()
    apart = seg(t, A("p5", "apart"), A("p5", "apart") + 0.6)
    back = seg(t, A("p5", "rebuilt"), A("p5", "rebuilt") + 0.6)
    lift = apart * (1 - back)
    for j in range(4):                                             # little builders carrying bone pieces
        bx = 200 + j * 110
        by = 600 - (bx - 360) * math.tan(0.35) * 1.0
        py = by - 30 - 140 * lift
        rrect(cr, bx - 30, py - 14, 60, 28, 6)
        paint(cr, hexc("#fff8e8"), OUTLINE, 4)
        hx, hy = bx + 10, py - 40 + 4 * math.sin(t * 6 + j)
        ellipse(cr, hx, hy, 20, 20)
        paint(cr, hexc("#7ac8f0"), OUTLINE, 4)
        cr.arc(hx, hy - 8, 20, math.pi, 2 * math.pi)                # hard hat
        paint(cr, GOLD, OUTLINE, 4)
    if t >= A("p5", "apart"):
        tag(cr, t, A("p5", "apart"), 360, 260, "TAKEN APART", col=RED, size=44, end=A("p5", "rebuilt") - 0.05)
    if t >= A("p5", "rebuilt"):
        tag(cr, t, A("p5", "rebuilt"), 360, 260, "...AND REBUILT", col=GREEN, size=44)
    vignette(cr, 0.25)


def scene_same(cr, t, tl):
    A = tl.at
    living_room(cr)
    cr.save()
    enter(cr, camera(t, [(tl.scene_at(t)[1], (1.6, 420, 640))], dur=0.6))
    grandpa(cr, t, tl, 520, 1100, 1.0, facing=-1, eyes="open", arms=("down", "down"))
    old_photo(cr, t, 330, 600, 0.42, rot=0.06)
    cr.restore()
    if t >= A("p6", "same"):
        sign(cr, t, A("p6", "same"), 360, 230, "STILL THE SAME?", col=PURPLE, size=56)
    vignette(cr, 0.3)


def scene_brain(cr, t, tl):
    A = tl.at
    plain(cr, "#1e2440", "#141a30")
    s0 = tl.scene_at(t)[1]
    glow = appear(t, A("p7", "brain"), 0.5) if t >= A("p7", "brain") else 0.0
    brain(cr, t, 360, 600, 1.15 * appear(t, s0, 0.4), glow=glow)
    if t >= A("p7", "Yes"):
        check(cr, t, A("p7", "Yes"), 560, 420, 50)
    if t >= A("p7", "old") and t < A("p7", "carbon"):
        tag(cr, t, A("p7", "old"), 360, 230, "AS OLD AS YOU", col=GOLD, size=52)
    if t >= A("p7", "carbon"):
        card(cr, t, A("p7", "carbon"), 230, 250, 300, 140, "2005 STUDY", ["CARBON-14"], col=BLUE, title_size=30,
             line_size=40)
        bomb_cloud(cr, 540, 310, appear(t, A("p7", "bomb"), 0.4) if t >= A("p7", "bomb") else 0)
    vignette(cr, 0.4)


def scene_tap(cr, t, tl):
    A = tl.at
    living_room(cr)
    tap = t >= A("p8", "brain")
    grandpa(cr, t, tl, 450, 1080, 1.0, facing=-1, eyes="happy", arms=("face" if tap else "down", "down"))
    girl(cr, t, tl, 190, 1060, 0.95, eyes="happy" if t >= A("p8", "rest") else "open", arms=("down", "down"))
    if tap:
        tag(cr, t, A("p8", "stayed"), 450, 360, "BRAIN: STAYED", col=GREEN, size=40)
    if t >= A("p8", "rest"):
        sign(cr, t, A("p8", "rest"), 360, 220, "THE REST: MOVED OUT", col=RED, size=44)
    vignette(cr, 0.3)


def scene_end(cr, t, tl):
    A = tl.at
    plain(cr, *WARM)
    old_photo(cr, t, 210, 690, 0.55, rot=-0.06)
    grandpa(cr, t, tl, 520, 1080, 0.9, facing=-1, eyes="happy", arms=("down", "down"))
    sign(cr, t, A("p9", "five"), 360, 210, "STILL YOU?", col=GOLD, size=60)
    buttons(cr, t, A("p9", "new"), [("SAME ME", GREEN), ("SOMEONE NEW", PURPLE)], y=370, size=44, w=320)
    vignette(cr, 0.3)


SCENES = {"photo": scene_photo, "room": scene_room, "blood": scene_blood, "skin": scene_skin, "bone": scene_bone,
          "same": scene_same, "brain": scene_brain, "tap": scene_tap, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    hook2(cr, t, "IS THIS BOY", "GRANDPA?", end=tl.at("p1", end=True), y=190, big_at=tl.at("p1", "boy"),
          mark="circle", mark_at=tl.at("p1", "me"))
    captions(cr, t, tl)
