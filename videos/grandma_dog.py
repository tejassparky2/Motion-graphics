"""Big question: "Would You Lie to Your Sick Grandma?" -- Grandma asks about her dog, who ran away three days ago,
in the polished look. Original story (not true history).

Owner, 20 Oct 2026: "Make more 2 auto approved be creative be controversy ... watcher should feel relatable or happy or
sad or mind blowing or should argue". Kant, "On a Supposed Right to Lie from Philanthropy" (1797): never lie, not even
to a murderer at the door asking where your friend is hiding. J. S. Mill, Utilitarianism (1861), ch. 2: the chief
exception to truthfulness is "when the withholding of some fact (as of information from a male-factor, or of bad news
from a person dangerously ill) would preserve some one ... from great and unmerited evil". Twist: the dog never ran
away; Grandma hid him under her blanket (a bump that moves from frame 0, for rewatches). Turbo stock female narrator
with tags; Grandma and the boy through Turbo with Kokoro reference voices (no tags on them). The dog was first
called Moti, but Whisper medium heard it as "mote", "Motti" and "Mahdi" (20 Oct 2026), so he is Bruno.
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, lin, paint,
                           rad, rrect, shade, sign, smooth, soft_disc, stamp, stroke_line, vignette)
from motion.toons import head, person

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "a9"          # music drops out under Grandma's reveal (research 18 Oct 2026, A5)
SERIES = "Big Questions"
voice.SPEAKERS.update({"grandma": dict(voice="bf_emma", speed=0.95, turbo_ref="bf_emma"),
                       "boy": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+3")})
DADI = dict(skin="brown", hair="bun", hair_col=hexc("#dcd8d4"), glasses=True, brows_col=hexc("#bdb8b4"))
BOY = dict(skin="brown", shirt=hexc("#ffcf5a"), tie=None, pants=hexc("#3b5b9a"))
SAREE = hexc("#a8324a")
FUR, FUR_D = hexc("#e2a866"), hexc("#b87a3c")

SCRIPT = [
    dict(id="a2", scene="ask", text="Beta, is Bruno eating properly?", speaker="grandma"),
    dict(id="a1", scene="ask", text="Grandma is sick in bed."),                   # re-cut 26 Oct: question first
    dict(id="a3", scene="gone", text="Bruno ran away three days ago. Nobody told her. [sigh]"),
    dict(id="a4", scene="scale", text="The truth could break her heart. A lie would let her rest."),
    dict(id="a5", scene="kant", text="Immanuel Kant said: never lie. Not even to a murderer at your door."),
    dict(id="a6", scene="mill", text="John Stuart Mill disagreed. Keeping bad news from someone dangerously ill can "
                                     "be right."),
    dict(id="a7", scene="lie", text="So the boy takes a breath, and lies."),
    dict(id="a8", scene="lie", text="He's fine, Grandma. He ate two rotis today.", speaker="boy"),
    dict(id="a9", scene="reveal", text="Really? Then who is this?", speaker="grandma", gap=0.35),
    dict(id="a10", scene="reveal", text="Bruno never ran away. He sneaked into her room, and she hid him, so nobody "
                                        "would make him sleep outside. [laugh]"),
    dict(id="a11", scene="both", text="Two lies. Both out of love."),
    dict(id="a12", scene="end", text="So, was the boy's lie kind, or was it still wrong?", gap=0.3),
]

METADATA = dict(
    title="Grandma Asked About Her Dog. He Ran Away 3 Days Ago 🐶",
    alt_titles=["Would You Lie to Your Sick Grandma? 🐶", "The Kindest Lie... or Still a Lie? 🐶"],
    description="""Grandma is sick in bed. She asks one question: "Beta, is Bruno eating properly?" But Bruno ran away three days ago, and nobody told her. 🐶

The truth could break her heart. A lie would let her rest.

Immanuel Kant said: never lie, not even to a murderer at your door (1797). John Stuart Mill disagreed: keeping bad news from someone dangerously ill can be right (Utilitarianism, 1861).

So the boy lies... and then Grandma lifts her blanket. 😄

An original story. Kant: "On a Supposed Right to Lie from Philanthropy" (1797). Mill: Utilitarianism, chapter 2 (1861).

💬 Was the boy's lie kind, or was it still wrong? 👇

🔔 Interestingly Strange: mind-bending questions, clever twists and The Last Bencher, animated in under a minute.""",
    hashtags=["#Grandma", "#Philosophy", "#Shorts"],
    tags=["would you lie to grandma", "white lie", "is lying ever right", "kant lying", "murderer at the door",
          "john stuart mill", "moral dilemma", "grandma and dog", "philosophy", "interestingly strange"],
    pinned_comment="Kind lie or still wrong? Pick a side and give your reason: would YOU have told Grandma the "
                   "truth? 👇",
)


# ---------------------------------------------------------------- props
def dog(cr, t, x, y, s=1.0, facing=1, tongue=True, wag=1.0, eyes="happy"):
    """Bruno: a round, sandy Indian street dog, sitting; (x, y) = where the body meets the floor."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s * facing, s)
    tail = math.sin(t * 16) * 0.5 * wag
    smooth(cr, [(-70, -40), (-100 + 10 * tail, -90 - 20 * tail), (-110 + 20 * tail, -120 - 10 * tail),
                (-92, -86), (-64, -50)])
    paint(cr, FUR, OUTLINE, 5)
    ellipse(cr, 0, -60, 82, 64)                                    # body
    paint(cr, rad(-20, -80, 110, [(0, shade(FUR, 0.25)), (1, FUR)]), OUTLINE, 5)
    ellipse(cr, 26, -40, 34, 30)                                   # white chest
    paint(cr, hexc("#fff4e2"), None, 0)
    for lx in (-30, 38):                                           # front paws
        ellipse(cr, lx, -6, 24, 14)
        paint(cr, shade(FUR, 0.1), OUTLINE, 4.5)
    dog_head(cr, t, 44, -138, 1.0, tongue=tongue, eyes=eyes)
    cr.restore()


def dog_head(cr, t, x, y, s=1.0, tongue=True, eyes="happy", ear=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for side in (-1, 1):                                           # floppy ears
        cr.save()
        cr.translate(side * 50, -38)
        cr.rotate(side * (0.5 + 0.15 * math.sin(t * 5 + side) + ear))
        ellipse(cr, 0, 26, 20, 38)
        paint(cr, FUR_D, OUTLINE, 4.5)
        cr.restore()
    ellipse(cr, 0, 0, 62, 56)
    paint(cr, rad(-14, -20, 80, [(0, shade(FUR, 0.3)), (1, FUR)]), OUTLINE, 5)
    ellipse(cr, 0, 24, 34, 24)                                     # muzzle
    paint(cr, hexc("#fff4e2"), OUTLINE, 4)
    ellipse(cr, 0, 12, 12, 9)                                      # nose
    paint(cr, OUTLINE, None, 0)
    for side in (-1, 1):
        if eyes == "happy":
            cr.arc(side * 24, -10, 9, math.pi, 2 * math.pi)
            cr.set_source_rgba(*OUTLINE)
            cr.set_line_width(5)
            cr.stroke()
        else:
            ellipse(cr, side * 24, -10, 8, 10)
            paint(cr, OUTLINE, None, 0)
            ellipse(cr, side * 24 - 2, -13, 3, 3)
            paint(cr, WHITE, None, 0)
    if tongue:
        rrect(cr, -9, 32, 18, 22 + 4 * math.sin(t * 10), 9)
        paint(cr, hexc("#ff7a8a"), OUTLINE, 3.5)
    cr.restore()


def bowl(cr, x, y, s=1.0, food=False):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.move_to(-60, -30)
    cr.line_to(60, -30)
    cr.line_to(46, 0)
    cr.line_to(-46, 0)
    cr.close_path()
    paint(cr, lin(0, -30, 0, 0, [(0, hexc("#e8473f")), (1, hexc("#a82a24"))]), OUTLINE, 5)
    bold_text(cr, "BRUNO", 0, -6, 20, WHITE, outline=None, shadow=0)
    if food:
        ellipse(cr, 0, -32, 50, 10)
        paint(cr, hexc("#d8a060"), OUTLINE, 3)
    cr.restore()


def room(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#f3d9c2")), (0.64, hexc("#ecc8a8")), (0.64, hexc("#9a6a44")),
                                   (1, hexc("#7a4e30"))]))
    cr.fill()
    rrect(cr, 470, 330, 190, 230, 12)                              # window, late afternoon
    paint(cr, lin(0, 330, 0, 560, [(0, hexc("#ffb878")), (1, hexc("#ffe2b8"))]), OUTLINE, 6)
    stroke_line(cr, [(565, 330), (565, 560)], 5, OUTLINE, curve=False)
    stroke_line(cr, [(470, 445), (660, 445)], 5, OUTLINE, curve=False)
    rrect(cr, 210, 300, 120, 150, 8)                               # framed photo: Grandma and Bruno
    paint(cr, hexc("#c8954a"), OUTLINE, 5)
    rrect(cr, 224, 314, 92, 122, 4)
    paint(cr, hexc("#fff0d8"), None, 0)
    soft_disc(cr, 270, 375, 30, alpha(FUR, 0.9), blur=0.1)


def bed(cr, t, x=60, y=820, bump=True, lift=0.0):
    """Side view of the bed, headboard at the left. `lift` 0..1 pulls the blanket back off the dog."""
    rrect(cr, x, y - 300, 46, 330, 14)                             # headboard
    paint(cr, lin(0, y - 300, 0, y, [(0, hexc("#9a5a30")), (1, hexc("#6a3a1e"))]), OUTLINE, 6)
    rrect(cr, x + 20, y - 90, 430, 90, 16)                         # mattress
    paint(cr, hexc("#f4efe4"), OUTLINE, 5)
    ellipse(cr, x + 100, y - 150, 70, 34)                          # pillow
    paint(cr, WHITE, OUTLINE, 5)


def blanket(cr, t, x=60, y=820, bump=True, lift=0.0, wiggle=1.0):
    b = 0.0
    if bump:                                                       # the "empty" blanket breathes: it's Bruno
        b = 6 * math.sin(t * 2.6) * wiggle + 4 * max(0.0, math.sin(t * 9)) * wiggle * (math.sin(t * 0.7) > 0.6)
    top = y - 120
    bx = x + 330 + 30 * lift
    pts = [(x + 70, y - 10), (x + 70, top + 10), (x + 180, top - 4), (bx - 80, top - 2), (bx - 30, top - 52 - b),
           (bx + 40, top - 46 - b), (bx + 90, top), (x + 470, top + 16), (x + 470, y - 10)]
    if lift > 0:
        pts = [(px, py + (40 * lift if px > bx - 120 else 0)) for px, py in pts]
    smooth(cr, pts)
    paint(cr, lin(0, top - 40, 0, y, [(0, hexc("#5aa0d8")), (1, hexc("#3a70b0"))]), OUTLINE, 6)
    for k in range(4):                                             # quilt stitching
        xx = x + 140 + k * 80
        stroke_line(cr, [(xx, top + 30), (xx + 10, y - 20)], 3, alpha(WHITE, 0.35), curve=False)


def grandma(cr, t, tl, x, y, r=74, **kw):
    """Grandma sitting up against the pillow: saree shoulders, head, bindi."""
    if kw.get("mouth") is None:
        kw["mouth"] = "talk" if tl is not None and tl.speaking("grandma", t) else "smile"
    kw.setdefault("eyes", "open")
    smooth(cr, [(x - 110, y + 230), (x - 100, y + 90), (x - 40, y + 62), (x + 40, y + 62), (x + 100, y + 90),
                (x + 110, y + 230)])
    paint(cr, lin(0, y + 60, 0, y + 230, [(0, shade(SAREE, 0.15)), (1, SAREE)]), OUTLINE, 5)
    stroke_line(cr, [(x + 60, y + 70), (x - 40, y + 230)], 14, GOLD, curve=False)       # pallu border
    head(cr, t, x, y, r, "teacher", **dict(DADI, **kw))
    soft_disc(cr, x, y - 0.42 * r, 0.075 * r, hexc("#d8202a"), blur=0.05)                # bindi


def boy(cr, t, tl, x, y, s=0.85, **kw):
    if kw.get("mouth") is None:
        kw["mouth"] = "talk" if tl is not None and tl.speaking("boy", t) else "flat"
    person(cr, t, x, y, s, "kid", **dict(BOY, **kw))


def bedroom(cr, t, tl, gx=170, gy=590, g=None, b=None, lift=0.0, dog_up=0.0, wiggle=1.0):
    room(cr, t)
    bed(cr, t)
    grandma(cr, t, tl, gx, gy, **(g or {}))
    if dog_up > 0:                                                 # Bruno pops out from under the blanket
        dog_head(cr, t, 400, lerp(760, 640, dog_up), 1.0, eyes="happy")
    blanket(cr, t, lift=lift, wiggle=wiggle)
    if b is not False:
        boy(cr, t, tl, 560, 1010, **(b or {}))


# ---------------------------------------------------------------- scenes
def scene_ask(cr, t, tl):
    A = tl.at
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("a2"), (1.25, 300, 640))], dur=0.6))
    bedroom(cr, t, tl, g=dict(eyes="half" if t < A("a2") else "open", look=(0.5, 0.1)),
            b=dict(eyes="open", arms=("hold", "down"), look=(-0.6, 0.0),
                   hold=lambda c, hx, hy: bowl(c, hx + 10, hy + 20, 0.7)))
    cr.restore()
    if t >= A("a2"):
        tag(cr, t, A("a2", "Bruno"), 220, 330, "BRUNO = HER DOG", col=GOLD, size=36)
    vignette(cr, 0.35)


def scene_gone(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#3a3550"), hexc("#5a4a6a"), seed=11)
    rrect(cr, 170, 300, 380, 470, 10)                              # MISSING poster
    paint(cr, hexc("#fff8e8"), OUTLINE, 6)
    bold_text(cr, "MISSING", 360, 375, 66, RED, outline=None, shadow=0)
    soft_disc(cr, 360, 590, 120, alpha(hexc("#f0d8b8"), 1), blur=0.05)
    dog(cr, t, 340, 690, 0.95, eyes="open", wag=0.0, tongue=False)
    bold_text(cr, "BRUNO", 360, 755, 44, OUTLINE, outline=None, shadow=0)
    for xx in (190, 530):
        rrect(cr, xx - 30, 285, 60, 30, 4)
        paint(cr, alpha(hexc("#e8e0c8"), 0.8), None, 0)
    if t >= A("a3", "three"):
        tag(cr, t, A("a3", "three"), 360, 230, "3 DAYS AGO", col=PURPLE, size=44)
    stamp(cr, t, A("a3", "Nobody"), 360, 830, "NOBODY TOLD HER", col=RED, size=52)
    vignette(cr, 0.45)


def heart(cr, x, y, s, col, crack=0.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.move_to(0, 40)
    cr.curve_to(-70, -10, -50, -70, 0, -36)
    cr.curve_to(50, -70, 70, -10, 0, 40)
    paint(cr, col, OUTLINE, 5)
    if crack > 0:
        stroke_line(cr, [(0, -34), (-10, -10), (8, 6), (-4, 30)][:max(2, int(4 * crack))], 6, OUTLINE, curve=False)
    cr.restore()


def scene_scale(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b3a4a"), hexc("#4a5a6a"), seed=12)
    card(cr, t, A("a4", "truth"), 190, 520, 300, 300, "TRUTH", ["", "", "BREAKS", "HER HEART"], col=RED,
         title_size=40, line_size=40)
    if t >= A("a4", "truth") + 0.3:
        heart(cr, 190, 520, 0.9, hexc("#ff5a6a"), crack=seg(t, A("a4", "break"), A("a4", "heart", end=True)))
    card(cr, t, A("a4", "lie"), 530, 520, 300, 300, "LIE", ["", "", "LETS HER", "REST"], col=GREEN, title_size=40,
         line_size=40)
    if t >= A("a4", "lie") + 0.3:
        bold_text(cr, "z Z z", 530 + 6 * math.sin(t * 2), 520, 54, hexc("#6aa8e8"), outline=OUTLINE, shadow=0)
    sign(cr, t, tl.scene_at(t)[1], 360, 220, "WHAT DO YOU SAY?", col=GOLD, size=56)
    vignette(cr, 0.4)


def door(cr, t, x, y, open_=0.0):
    rrect(cr, x - 110, y - 330, 220, 330, 8)
    paint(cr, hexc("#1a1a24"), OUTLINE, 6)                         # dark doorway
    if open_ > 0.05:                                               # the murderer's silhouette
        soft_disc(cr, x, y - 250, 40, (0, 0, 0, 0.95), blur=0.05)
        smooth(cr, [(x - 70, y), (x - 60, y - 170), (x, y - 205), (x + 60, y - 170), (x + 70, y)])
        paint(cr, (0.02, 0.02, 0.04, 0.95), None, 0)
        for side in (-1, 1):
            soft_disc(cr, x + side * 14, y - 256, 6, hexc("#ff3a3a"), blur=0.2)
    cr.save()
    cr.translate(x - 110, y - 330)
    cr.scale(1 - 0.75 * open_, 1)
    rrect(cr, 0, 0, 220, 330, 8)
    paint(cr, lin(0, 0, 220, 0, [(0, hexc("#9a5a30")), (1, hexc("#7a4220"))]), OUTLINE, 6)
    cr.arc(190, 170, 12, 0, 2 * math.pi)
    paint(cr, GOLD, OUTLINE, 3)
    cr.restore()


def scene_kant(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f2230"), hexc("#3a3048"), seed=13)
    card(cr, t, tl.scene_at(t)[1], 360, 330, 420, 230, "IMMANUEL KANT · 1797", ["NEVER LIE.", "NOT EVEN ONCE."], col=BLUE,
         title_size=34, line_size=46)
    if t >= A("a5", "murderer") - 0.3:
        door(cr, t, 360, 860, seg(t, A("a5", "murderer"), A("a5", "door", end=True)))
        cue("knock", t, A("a5", "murderer") - 0.3, 0.8)
    if t >= A("a5", "door"):
        tag(cr, t, A("a5", "door"), 360, 560, "EVEN TO A MURDERER", col=RED, size=40)
    vignette(cr, 0.5)


def scene_mill(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e6c8"), hexc("#fff6e8"), seed=14)
    card(cr, t, tl.scene_at(t)[1], 360, 330, 440, 260, "JOHN STUART MILL · 1861", ["HIDE BAD NEWS", "FROM SOMEONE",
         "DANGEROUSLY ILL"], col=GREEN, title_size=32, line_size=42)
    stamp(cr, t, A("a6", "disagreed"), 560, 150, "DISAGREED", col=PURPLE, size=44)
    k = appear(t, A("a6", "Keeping"))
    if k > 0.02:                                                   # Grandma in a little window: she is the one
        cr.save()
        cr.translate(360, 680)
        cr.scale(0.55 * k, 0.55 * k)
        cr.translate(-360, -640)
        rrect(cr, 0, 280, 720, 760, 40)
        cr.save()
        cr.clip()
        room(cr, t)
        bed(cr, t)
        grandma(cr, t, None, 170, 590, eyes="half", mouth="flat")
        blanket(cr, t)
        cr.restore()
        rrect(cr, 0, 280, 720, 760, 40)
        paint(cr, None, WHITE, 14)
        cr.restore()
    vignette(cr, 0.35)


def scene_lie(cr, t, tl):
    A = tl.at
    cr.save()
    enter(cr, camera(t, [(A("a7"), (1.0, 360, 640)), (A("a7", "breath"), (1.45, 560, 700)),
                         (A("a8"), (1.15, 420, 660))], dur=0.5))
    lying = t >= A("a8")
    bedroom(cr, t, tl, g=dict(eyes="open", look=(0.6, 0.0)),
            b=dict(eyes="half" if not lying else "happy", mouth=None if lying else "flat",
                   sweat=lying, arms=("hold", "down") if not lying else ("hold", "hips"),
                   hold=lambda c, hx, hy: bowl(c, hx + 10, hy + 20, 0.7)))
    cr.restore()
    if t >= A("a7", "breath") and t < A("a8"):
        cue("sigh", t, A("a7", "breath"), 0.5)
    if lying:
        tag(cr, t, A("a8", "rotis"), 470, 300, "2 ROTIS (LIE)", col=RED, size=40)
    vignette(cr, 0.35)


def scene_reveal(cr, t, tl):
    A = tl.at
    pop = seg(t, A("a9", "this"), A("a9", "this") + 0.35)
    cr.save()
    enter(cr, camera(t, [(A("a9"), (1.2, 300, 640)), (A("a9", "this"), (1.05, 330, 640)),
                         (A("a10", "outside"), (1.2, 330, 600))], dur=0.4))
    face = "happy" if t >= A("a9", "this") else "half"
    bedroom(cr, t, tl, g=dict(eyes=face, mouth="grin" if t >= A("a10") else None, brows="raise"),
            b=dict(eyes="wide" if t >= A("a9", "this") else "happy", mouth="o" if t >= A("a9", "this") else "flat",
                   arms=("down", "down")), lift=pop, dog_up=pop)
    cr.restore()
    if t >= A("a9", "this"):
        cue("pop", t, A("a9", "this"), 0.2)
        sparkles(cr, t, A("a9", "this"), 400, 620, n=7, seed=21, col=GOLD)
        sign(cr, t, A("a9", "this"), 360, 230, "BRUNO WAS HERE ALL ALONG", col=GREEN, size=42)
    if t >= A("a10", "hid"):
        tag(cr, t, A("a10", "hid"), 360, 360, "SHE HID HIM", col=PURPLE, size=44)
    vignette(cr, 0.3)


def scene_both(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd8e0"), hexc("#fff0d8"), seed=15)
    card(cr, t, tl.scene_at(t)[1], 190, 470, 300, 220, "HIS LIE", ["BRUNO ATE", "2 ROTIS"], col=BLUE, title_size=36,
         line_size=40)
    card(cr, t, tl.scene_at(t)[1] + 0.15, 530, 470, 300, 220, "HER LIE", ["BRUNO IS", "NOT HERE"], col=PURPLE, title_size=36,
         line_size=40)
    if t >= A("a11", "love"):
        heart(cr, 360, 720, 1.1 + 0.05 * math.sin(t * 8), hexc("#ff5a7a"))
        sign(cr, t, A("a11", "love"), 360, 220, "BOTH OUT OF LOVE", col=RED, size=54)
    vignette(cr, 0.3)


def scene_end(cr, t, tl):
    A = tl.at
    cr.save()
    enter(cr, camera(t, [(A("a12"), (1.0, 360, 640))]))
    bedroom(cr, t, tl, g=dict(eyes="happy", mouth="grin"), b=dict(eyes="happy", mouth="smile",
            arms=("shrug", "shrug")), lift=1.0, dog_up=1.0)
    cr.restore()
    sign(cr, t, A("a12", "kind"), 360, 210, "KIND LIE, OR STILL WRONG?", col=GOLD, size=46)
    buttons(cr, t, A("a12", "kind"), [("KIND", GREEN), ("WRONG", RED)], y=360, size=48)
    vignette(cr, 0.3)


SCENES = {"ask": scene_ask, "gone": scene_gone, "scale": scene_scale, "kant": scene_kant, "mill": scene_mill,
          "lie": scene_lie, "reveal": scene_reveal, "both": scene_both, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("HER DOG RAN AWAY.", False), ("NOBODY TOLD HER.", True)], end=tl.at("a3"), y=150, size=74)
    captions(cr, t, tl)
