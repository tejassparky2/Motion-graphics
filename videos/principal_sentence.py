"""The Last Bencher's One Sentence -- genie-style story #2 (out/scripts_genie_style_batch1.md, approved by the owner on
14 Oct 2026). The principal catches the last bencher asleep: "Say one sentence. True gets detention, false gets extra
homework." The kid says "I will get extra homework." Original story; narrated by ElevenLabs Chris.

Staging: the kid is caught in class, then the principal deals with him in his office while the whole class watches
through the glass in the door (so "the whole class goes quiet" and "get out of my office" both fit).
"""
import math

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, INKC, PURPLE, RED, buttons, card, shake, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter,
                           ground_shadow, light_rays, lin, paint, put, rad, rrect, shade, sign, smooth, soft_disc,
                           soft_rrect, sprite, stamp, stroke_line, vignette)
from motion.rulekit import either_way, mouth, note, stone, zzz
from motion.toons import head, person
from videos.last_bencher_4 import classroom, room

NARRATOR = dict(engine="elevenlabs")
TAIL = 0.9
voice.SPEAKERS.update({
    "principal": dict(el=voice.ELEVEN["adam"], tone="stern"),
    "kid": dict(el=voice.ELEVEN["liam"], pitch=2.5, tone="confidently"),
})

SCRIPT = [
    dict(id="p1", scene="class", text="The principal catches the last bencher sleeping in class, and gives him one "
                                      "chance.", tone="dramatic"),
    dict(id="p2", scene="deal", text="Say one sentence. If it's true, you get detention. If it's false, you get "
                                     "extra homework.", speaker="principal", gap=0.3),
    dict(id="p3", scene="quiet", text="The whole class goes quiet.", tone="whispers"),
    dict(id="p4", scene="line", text="I will get extra homework.", speaker="kid", gap=0.45, pace=0.9, tone="smugly"),
    dict(id="p5", scene="freeze", text="The principal freezes.", gap=0.45, pace=0.92, tone="dramatic"),
    dict(id="p6", scene="logic", text="If the sentence is true, he gets extra homework. But true sentences get "
                                      "detention."),
    dict(id="p7", scene="logic", text="If it's false, he doesn't get homework. But false sentences get homework."),
    dict(id="p8", scene="logic", text="Either way, the principal breaks his own rule.", pace=0.95),
    dict(id="p9", scene="out", text="Get out of my office.", speaker="principal", gap=0.3, tone="frustrated"),
    dict(id="p10", scene="walk", text="So he walked out. No detention. No homework.", tone="amused"),
    dict(id="p11", scene="end", text="Was that genius, or just lucky?", gap=0.6, pace=0.95, tone="curious"),
]

METADATA = dict(
    title="Principal: Say 1 Sentence. Kid: …😏",
    alt_titles=["The Last Bencher Beat the Principal With 1 Sentence 😏", "True = Detention. False = Homework. Kid: 😏",
                "The Sentence That Broke the Principal's Rule 🤯"],
    description="""The principal catches the last bencher sleeping in class, and gives him one chance. 😴

"Say one sentence. If it's true, you get detention. If it's false, you get extra homework."

The whole class goes quiet. And the last bencher says: "I will get extra homework."

The principal freezes. If the sentence is true, he gets extra homework, but true sentences get detention. If it's false, he doesn't get homework, but false sentences get homework. Either way, the principal breaks his own rule.

"Get out of my office." So he walked out. No detention. No homework. 😎

An original Last Bencher story built on a classic self-reference trap.

💬 Was that genius, or just lucky? 👇

🔔 Interestingly Strange: mind-bending paradoxes, clever stories, weird animals and bizarre history, animated in under a minute.""",
    hashtags=["#LastBencher", "#Paradox", "#Shorts"],
    tags=["last bencher", "principal", "one sentence", "detention or homework", "paradox", "self reference paradox",
          "brain teaser", "funny school story", "backbenchers", "interestingly strange"],
    pinned_comment="What sentence would YOU have said? Best one gets pinned 😏👇",
)

PRIN = dict(hair="bald", hair_col=hexc("#3a3a40"), stache=hexc("#3a3a40"), suit=hexc("#2f3b5a"),
            pants=hexc("#2a3048"), shirt=WHITE, tie=hexc("#b33a2e"), glasses=True, brows_col=hexc("#3a3a40"))
WALL = hexc("#e9d8b8")
WOOD = hexc("#8e5a2e")


# ---------------------------------------------------------------- the office
def _office(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, 760, [(0, hexc("#f2e4c8")), (1, WALL)]))
    c.fill()
    c.rectangle(0, 600, W, 200)
    c.set_source(lin(0, 600, 0, 800, [(0, hexc("#c9a77a")), (1, hexc("#a8865a"))]))
    c.fill()
    c.rectangle(0, 596, W, 10)
    c.set_source_rgba(*hexc("#8a6a42"))
    c.fill()
    c.rectangle(0, 800, W, H - 800)
    c.set_source(lin(0, 800, 0, H, [(0, hexc("#9a4e48")), (1, hexc("#6e3430"))]))
    c.fill()
    soft_rrect(c, 30, 170, 210, 430, 10, (0, 0, 0, 0.25), sigma=10)       # bookshelf
    rrect(c, 30, 160, 210, 440, 10)
    paint(c, lin(0, 160, 0, 600, [(0, shade(WOOD, 0.2)), (1, WOOD)]), OUTLINE, 5)
    cols = [RED, BLUE, GREEN, GOLD, PURPLE, hexc("#3a8f8f")]
    for r in range(3):
        y = 190 + r * 135
        rrect(c, 46, y, 178, 112, 4)
        paint(c, shade(WOOD, -0.35), None, 0)
        for b in range(6):
            hgt = 76 + (b * 13 + r * 7) % 30
            rrect(c, 54 + b * 28, y + 112 - hgt, 24, hgt, 3)
            paint(c, cols[(b + r * 2) % 6], OUTLINE, 2.5)
    rrect(c, 300, 200, 150, 110, 6)            # framed certificate
    paint(c, GOLD, OUTLINE, 4)
    rrect(c, 314, 214, 122, 82, 3)
    paint(c, WHITE, None, 0)
    bold_text(c, "PRINCIPAL", 375, 250, 20, INKC, outline=None, shadow=0)
    stroke_line(c, [(330, 272), (420, 272)], 3, alpha(INKC, 0.5), curve=False)
    c.arc(410, 288, 10, 0, 2 * math.pi)
    paint(c, RED, None, 0)
    c.arc(375, 120, 44, 0, 2 * math.pi)        # clock
    paint(c, WHITE, OUTLINE, 5)
    stroke_line(c, [(375, 120), (375, 92)], 5, OUTLINE, curve=False)
    stroke_line(c, [(375, 120), (395, 128)], 5, OUTLINE, curve=False)


def office(cr, t):
    put(cr, sprite("principal_office", W, H, _office), 0, 0)


DOOR = (500, 180, 190, 620)    # x, y, w, h


def door(cr, t, open_=0.0, faces=0.0, gasp=False):
    """The office door with a glass panel; `faces` 0..1 brings the class's heads up to the glass."""
    x, y, w, h = DOOR
    rrect(cr, x - 12, y - 12, w + 24, h + 12, 6)
    paint(cr, shade(WOOD, -0.3), OUTLINE, 5)
    cr.rectangle(x, y, w, h)
    cr.set_source_rgba(0.15, 0.12, 0.1, 1)
    cr.fill()
    if open_ > 0:
        light_rays(cr, t, x + w / 2, y + 40, n=3, a=0.12 * open_)
    dw = w * (1 - 0.82 * open_)
    rrect(cr, x, y, dw, h, 4)
    paint(cr, lin(x, 0, x + dw, 0, [(0, shade(WOOD, 0.25)), (1, WOOD)]), OUTLINE, 5)
    gx, gy, gw, gh = x + 26 * (dw / w), y + 40, (w - 52) * (dw / w), 200
    if dw > 30:
        cr.save()
        rrect(cr, gx, gy, gw, gh, 8)
        cr.clip_preserve()
        cr.set_source(lin(0, gy, 0, gy + gh, [(0, hexc("#cfe9ff")), (1, hexc("#9fc8e8"))]))
        cr.fill()
        if faces > 0:
            for k, (who, fx) in enumerate((("student1", 0.22), ("student2", 0.5), ("student3", 0.78))):
                rise = ease_out(seg(faces, k * 0.15, k * 0.15 + 0.6))
                head(cr, t, gx + gw * fx, gy + gh + 40 - 120 * rise, 40, who, eyes="wide" if gasp else "open",
                     mouth="o" if gasp else "flat")
        cr.restore()
        rrect(cr, gx, gy, gw, gh, 8)
        paint(cr, alpha(WHITE, 0.12), OUTLINE, 4)
        stroke_line(cr, [(gx + 16, gy + 30), (gx + 50, gy + 10)], 5, alpha(WHITE, 0.6), curve=False)
    cr.arc(x + dw - 24, y + 360, 10, 0, 2 * math.pi)
    paint(cr, GOLD, OUTLINE, 3)


def desk(cr, x, y, s=1.0):
    """The principal's desk from the front; (x, y) is the middle of its top edge."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -210, 0, 420, 34, 8)
    paint(cr, lin(0, 0, 0, 34, [(0, shade(WOOD, 0.4)), (1, shade(WOOD, 0.1))]), OUTLINE, 5)
    rrect(cr, -196, 30, 392, 200, 8)
    paint(cr, lin(0, 30, 0, 230, [(0, WOOD), (1, shade(WOOD, -0.3))]), OUTLINE, 5)
    rrect(cr, -80, 80, 160, 46, 6)
    paint(cr, lin(0, 80, 0, 126, [(0, hexc("#ffe28a")), (1, GOLD)]), OUTLINE, 3.5)
    bold_text(cr, "PRINCIPAL", 0, 112, 26, INKC, outline=None, shadow=0)
    rrect(cr, 110, -40, 40, 44, 8)           # mug
    paint(cr, RED, OUTLINE, 3.5)
    for k in range(3):                       # a pile of papers
        rrect(cr, -170 + k * 3, -10 - k * 8, 110, 12, 3)
        paint(cr, WHITE, OUTLINE, 2.5)
    cr.restore()


def principal(cr, t, tl, x, y, s=1.0, eyes="angry", rest="flat", arms=("hips", "hips"), brows="angry", g=0.0,
              sweat=False, facing=1):
    stone(cr, lambda c: person(c, t, x, y, s, "sir", eyes=eyes, mouth=mouth(tl, "principal", t, rest), brows=brows,
                               arms=arms, sweat=sweat, facing=facing, **PRIN), g)


def kid(cr, t, tl, x, y, s=1.0, **kw):
    kw.setdefault("mouth", mouth(tl, "kid", t, kw.pop("rest", "smug")))
    person(cr, t, x, y, s, "kid", **kw)


# ---------------------------------------------------------------- scenes
def scene_class(cr, t, tl):
    A = tl.at
    room(cr, t)
    caught = A("p1", "sleeping")
    cam = camera(t, [(0, (1.9, 560, 430)), (A("p1", "sleeping"), (1.9, 560, 430)), (A("p1", "class,"), (1.0, 360, 640)),
                     (A("p1", "chance."), (1.2, 470, 620))], dur=0.7)
    cr.save()
    enter(cr, cam)
    awake = t >= A("p1", "gives")
    classroom(cr, t, tl, kid_pose=dict(eyes="wide" if awake else "closed", mouth="o" if awake else "flat",
                                       arms=("front", "front"), tilt=0.0 if awake else -0.18),
              look_at=(560, 0) if t >= caught else None)
    if not awake:
        zzz(cr, t, 600, 330, 0.9)
    px = lerp(900, 600, ease_out(seg(t, A("p1", "class,") - 0.3, A("p1", "class,") + 0.5)))
    principal(cr, t, tl, px, 1090, 0.95, arms=("hips", "point") if awake else ("hips", "hips"), facing=-1)
    cr.restore()
    sign(cr, t, -0.5, 360, 150, "1 SENTENCE", col=GOLD, size=84, end=A("p1", "chance.") - 0.1)
    sign(cr, t, A("p1", "chance."), 360, 150, "ONE CHANCE", col=RED, size=78)
    vignette(cr, 0.45)


def scene_deal(cr, t, tl):
    A = tl.at
    office(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("p2") - 0.3, (1.3, 300, 640)), (A("p2", "If"), (1.0, 360, 640))], dur=0.6))
    door(cr, t)
    principal(cr, t, tl, 260, 870, 0.95, arms=("point", "hips"))
    desk(cr, 260, 780, 0.95)
    kid(cr, t, tl, 560, 1060, 0.8, eyes="half", arms=("pocket", "pocket"), look=(-0.6, -0.3), rest="flat")
    cr.restore()
    card(cr, t, A("p2", "true,"), 185, 230, 320, 200, "TRUE", ["= DETENTION"], col=GREEN, line_size=40)
    card(cr, t, A("p2", "false,"), 535, 230, 320, 200, "FALSE", ["= HOMEWORK"], col=RED, line_size=40)
    vignette(cr, 0.4)


def scene_quiet(cr, t, tl):
    A = tl.at
    office(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("p3") - 0.3, (1.0, 360, 640)), (A("p3", "class"), (1.7, 595, 360))], dur=0.7))
    door(cr, t, faces=seg(t, A("p3"), A("p3") + 0.9), gasp=t >= A("p3", "quiet."))
    principal(cr, t, tl, 260, 870, 0.95, arms=("cross", "cross"), rest="smug")
    desk(cr, 260, 780, 0.95)
    cr.restore()
    tag(cr, t, A("p3", "quiet."), 360, 160, "SHHH...", col=PURPLE, size=64)
    vignette(cr, 0.5)


def scene_line(cr, t, tl):
    A = tl.at
    office(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("p4") - 0.3, (1.3, 420, 700))]))
    door(cr, t, faces=1.0)
    kid(cr, t, tl, 470, 1050, 1.0, eyes="half", arms=("point", "pocket"), brows="raise", look=(-0.6, -0.2),
        facing=-1)
    cr.restore()
    note(cr, t, A("p4") + 0.05, 280, 360, ["\"I WILL GET", "EXTRA", "HOMEWORK.\""], hot=1, w=440, size=56, rot=-0.04)
    vignette(cr, 0.5)


def scene_freeze(cr, t, tl):
    A = tl.at
    office(cr, t)
    fr = A("p5", "freezes.")
    dx, dy = shake(t, fr, 0.3, 8)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, camera(t, [(A("p5") - 0.3, (1.45, 280, 560))]))
    door(cr, t, faces=1.0, gasp=True)
    principal(cr, t, tl, 260, 870, 0.95, eyes="wide", rest="o", brows="up", arms=("down", "down"),
              g=ease_out(seg(t, fr, fr + 0.4)))
    desk(cr, 260, 780, 0.95)
    cr.restore()
    if t >= fr:
        cue("hit", t, fr)
    stamp(cr, t, fr, 360, 180, "FROZEN", col=hexc("#5a6478"), size=100)
    vignette(cr, 0.5)


def _stuck(cr, t, spin):
    person(cr, t, 360, 1000, 0.55, "sir", eyes="x" if spin and t % 1 > 0.5 else "wide", mouth="o", brows="up",
           arms=("up", "up") if spin else ("chin", "down"), sweat=True, **PRIN)


def scene_logic(cr, t, tl):
    studio(cr, t, hexc("#3a2a5a"), hexc("#b08ad8"), seed=6)
    either_way(cr, t, tl, "p6", "p7", "p8",
               ("TRUE?", ["Gets HOMEWORK...", "but TRUE =", "DETENTION!"], GREEN),
               ("FALSE?", ["No HOMEWORK...", "but FALSE =", "HOMEWORK!"], RED),
               "RULE BROKEN", PURPLE, ("p6", "detention."), ("p7", "homework.", False, 2), figure=_stuck)
    vignette(cr, 0.4)


def scene_out(cr, t, tl):
    A = tl.at
    office(cr, t)
    dx, dy = shake(t, A("p9", "out"), 0.3, 6)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, camera(t, [(A("p9") - 0.3, (1.3, 380, 620))]))
    door(cr, t, open_=ease_out(seg(t, A("p9", "office.") - 0.2, A("p9", "office.") + 0.3)), faces=1.0, gasp=True)
    principal(cr, t, tl, 260, 870, 0.95, eyes="angry", arms=("point", "hips"), brows="angry", sweat=True)
    desk(cr, 260, 780, 0.95)
    kid(cr, t, tl, 470, 1050, 0.85, eyes="happy", arms=("pocket", "pocket"), rest="grin", look=(-0.5, -0.2))
    cr.restore()
    stamp(cr, t, A("p9", "Get"), 360, 170, "GET OUT!", col=RED, size=96)
    vignette(cr, 0.45)


def _corridor(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, 800, [(0, hexc("#d8ecf2")), (1, hexc("#b8d8e2"))]))
    cr.fill()
    for k in range(4):           # lockers
        x = 40 + k * 170
        rrect(cr, x, 300, 150, 500, 8)
        paint(cr, lin(x, 0, x + 150, 0, [(0, hexc("#5a9ad8")), (1, hexc("#3a7ab8"))]), OUTLINE, 5)
        for j in range(3):
            stroke_line(cr, [(x + 40, 340 + j * 18), (x + 110, 340 + j * 18)], 4, alpha(OUTLINE, 0.5), curve=False)
        cr.arc(x + 120, 560, 9, 0, 2 * math.pi)
        paint(cr, hexc("#d8d8e0"), OUTLINE, 3)
    cr.rectangle(0, 800, W, H - 800)
    cr.set_source(lin(0, 800, 0, H, [(0, hexc("#e8e0d0")), (1, hexc("#c8bca8"))]))
    cr.fill()
    for k in range(6):
        stroke_line(cr, [(-200 + k * 220, H), (360 + (k - 2.5) * 60, 800)], 3, alpha(OUTLINE, 0.15), curve=False)


def scene_walk(cr, t, tl):
    A = tl.at
    _corridor(cr, t)
    w0 = A("p10")
    x = lerp(-80, 420, seg(t, w0 - 0.2, A("p10", "No", nth=1)))
    cr.save()
    enter(cr, (1.0, 360, 640))
    kid(cr, t, tl, x, 1060, 0.95, eyes="happy", arms=("pocket", "pocket"), rest="grin", walk=t * 7 if x < 420 else None,
        look=(0.4, 0))
    cr.restore()
    stamp(cr, t, A("p10", "detention."), 360, 200, "NO DETENTION", col=GREEN, size=72, rot=-0.1)
    stamp(cr, t, A("p10", "homework."), 360, 330, "NO HOMEWORK", col=BLUE, size=72, rot=0.06)
    sparkles(cr, t, A("p10", "homework."), 420, 620, n=8, seed=2, col=GOLD)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    _corridor(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    kid(cr, t, tl, 380, 1060, 0.95, eyes="half", arms=("pocket", "pocket"), rest="smug", brows="raise",
        look=(0.0, 0.2))
    cr.restore()
    stamp(cr, t, A("p10", "detention."), 360, 200, "NO DETENTION", col=GREEN, size=72, rot=-0.1, end=A("p11"))
    stamp(cr, t, A("p10", "homework."), 360, 330, "NO HOMEWORK", col=BLUE, size=72, rot=0.06, end=A("p11"))
    sign(cr, t, A("p11"), 360, 140, "GENIUS OR LUCKY?", col=PURPLE, size=58)
    buttons(cr, t, A("p11", "genius,"), [("GENIUS", GOLD), ("LUCKY", GREEN)], y=290)
    vignette(cr, 0.45)


SCENES = {"class": scene_class, "deal": scene_deal, "quiet": scene_quiet, "line": scene_line,
          "freeze": scene_freeze, "logic": scene_logic, "out": scene_out, "walk": scene_walk, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
