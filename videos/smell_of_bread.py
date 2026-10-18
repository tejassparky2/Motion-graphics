"""Sued for Smelling Bread -- the old folk tale of the judge who paid for a smell with a sound, in the polished look.

Script: out/scripts_batch_oct26-31.md, row 63 (owner approved 18 Oct 2026). A folk tale told in many countries
(versions name Nasreddin, Birbal, or a nameless judge); the video says "an old folk tale" and names no one. Closing
debate: if using something costs the owner nothing, is it still taking? Everyday example: café music, a neighbour's
Wi-Fi. Turbo stock female narrator with tags; the baker and the judge through Turbo with Kokoro reference voices.
"""
import math
import random

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, lin, paint,
                           rad, rrect, shade, sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person, portrait
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, mouth_of, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 1.0
voice.SPEAKERS.update({"baker": dict(voice="am_santa", speed=1.0, turbo_ref="am_santa"),
                       "judge": dict(voice="bm_george", speed=0.95, turbo_ref="bm_george")})
POOR = dict(skin="tan", hair="short", hair_col=hexc("#5a3418"), beard=hexc("#5a3418"), shirt=hexc("#b8a088"),
            pants=hexc("#7a6a5a"), tunic=True, belt=hexc("#5a3a20"), build="adult")
BAKER = dict(skin="light", hair="short", hair_col=hexc("#8a5a3a"), stache=hexc("#8a5a3a"), shirt=WHITE,
             pants=hexc("#5a5a6a"), apron=WHITE, build="adult")

SCRIPT = [
    dict(id="s1", scene="court", text="A poor man is dragged into court. His crime? He smelled bread."),
    dict(id="s2", scene="bakery", text="Every morning, he eats his dry bread outside a bakery, and breathes in the "
                                       "smell of fresh loaves."),
    dict(id="s3", scene="baker", text="He enjoys my smell every single day. He should pay for it!", speaker="baker"),
    dict(id="s4", scene="court2", text="The whole town is watching. The judge thinks. Then he asks the poor man for "
                                       "his coins."),
    dict(id="s5", scene="coins", text="His last few coins. [gasp]"),
    dict(id="s6", scene="coins", text="The judge shakes them, right next to the baker's ear."),
    dict(id="s7", scene="paid", text="There. You've been paid.", speaker="judge"),
    dict(id="s8", scene="paid", text="Paid? With what?", speaker="baker"),
    dict(id="s9", scene="verdict", text="He enjoyed the smell of your bread. You enjoyed the sound of his money.",
         speaker="judge", gap=0.3),
    dict(id="s10", scene="home", text="And the poor man walked home, with every coin still in his pocket. [laugh]"),
    dict(id="s11", scene="today", text="It's an old folk tale, told in many countries. But it's still a real question. "
                                       "Like music from a café, or your neighbour's Wi-Fi."),
    dict(id="s12", scene="end", text="If it costs the owner nothing, is it still taking? Baker, or poor man?", gap=0.3),
]

METADATA = dict(
    title="He Got Sued for Smelling Bread 🍞",
    alt_titles=["Sued for Smelling Bread. The Judge's Answer Is Genius 🍞", "The Baker Wanted Money for the Smell 🍞"],
    description="""A poor man is dragged into court. His crime? He smelled bread. 🍞

Every morning he eats his dry bread outside a bakery and breathes in the smell of fresh loaves, so the baker wants him to pay for it. The judge asks for the poor man's last coins... and shakes them next to the baker's ear. "He enjoyed the smell of your bread. You enjoyed the sound of his money." 😂

An old folk tale, told in many countries.

💬 If it costs the owner nothing, is it still taking? Team Baker or Team Poor Man? 👇

🔔 Interestingly Strange: clever twists, The Last Bencher and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#FolkTale", "#PlotTwist", "#Shorts"],
    tags=["smell of bread story", "folk tale", "clever judge", "wise judge story", "moral story", "plot twist",
          "short story", "clever verdict", "would you rather", "interestingly strange"],
    pinned_comment="Team Baker 🍞 or Team Poor Man 🪙? Is using a smell 'taking'? 👇",
)


def baker(cr, t, x, y, s, tl=None, **kw):
    kw.setdefault("mouth", "talk" if tl is not None and tl.speaking("baker", t) else "flat")
    person(cr, t, x, y, s, "barber", **dict(BAKER, **kw))
    cr.save()                                                       # chef's hat
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -60, -600, 120, 70, 10)
    paint(cr, WHITE, OUTLINE, 5)
    for dx in (-40, 0, 40):
        cr.arc(dx, -610, 36, 0, 2 * math.pi)
        paint(cr, WHITE, OUTLINE, 5)
    cr.restore()


def poor(cr, t, x, y, s, **kw):
    person(cr, t, x, y, s, "villager", **dict(POOR, **kw))


def judge(cr, t, x, y, s, tl=None, **kw):
    kw.setdefault("mouth", "talk" if tl is not None and tl.speaking("judge", t) else "smile")
    person(cr, t, x, y, s, "judge", **kw)


def loaf(cr, x, y, s=1.0, rot=0.0):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    ellipse(cr, 0, 0, 70, 34)
    paint(cr, rad(-20, -14, 80, [(0, hexc("#f0b860")), (1, hexc("#b8702e"))]), OUTLINE, 5)
    for k in range(3):
        stroke_line(cr, [(-36 + k * 30, -20), (-20 + k * 30, 14)], 4, alpha(OUTLINE, 0.5), curve=False)
    cr.restore()


def steam(cr, t, x, y, n=3, h=220, col=(1, 1, 1, 0.55)):
    for k in range(n):
        ph = (t * 0.6 + k / n) % 1
        pts = [(x + k * 30 + 18 * math.sin(ph * 6 + j + k), y - j * h / 6 - ph * 40) for j in range(7)]
        stroke_line(cr, pts, 8 * (1 - ph) + 2, (col[0], col[1], col[2], col[3] * (1 - ph)))


def coins(cr, t, x, y, n=3, shake=0.0):
    for k in range(n):
        dx = 22 * math.sin(t * 40 + k) * shake
        cr.arc(x + k * 26 - 26 + dx, y - k * 6, 18, 0, 2 * math.pi)
        paint(cr, rad(x - 6, y - 6, 24, [(0, hexc("#ffe680")), (1, hexc("#c8961e"))]), OUTLINE, 4)


def _court_bg(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#5a3a2a")), (0.62, hexc("#8a5a3a")), (0.62, hexc("#a87a4a")),
                                   (1, hexc("#6a4a2a"))]))
    cr.fill()
    for k in range(5):                                              # columns
        rrect(cr, 30 + k * 150, 100, 60, 690, 8)
        paint(cr, lin(0, 0, 60, 0, [(0, hexc("#e8dcc0")), (1, hexc("#b8a888"))]), OUTLINE, 4)
    rrect(cr, 180, 560, 360, 230, 12)                               # the judge's bench
    paint(cr, hexc("#6a3a1a"), OUTLINE, 6)


def crowd(cr, t, n=6, y=1060, s=0.38):
    for k in range(n):
        person(cr, t, 70 + k * 118, y - (k % 2) * 20, s, ("reporter", "kid", "teacher", "dad", "student1", "cousin")[k
               % 6], eyes="wide", mouth="o", arms=("front", "front"), seed=k + 9, look=(0, -0.6))


def scene_court(cr, t, tl):
    A = tl.at
    _court_bg(cr, t)
    cr.save()
    enter(cr, camera(t, [(0.0, (1.0, 360, 640)), (A("s1", "crime?"), (1.2, 330, 640))], dur=0.6))
    judge(cr, t, 360, 600, 0.6, None, eyes="half", arms=("front", "front"))
    pull = 1 - ease_out(seg(t, 0.0, A("s1", "court.")))
    poor(cr, t, lerp(240, -60, pull), 1000, 0.8, eyes="wide", mouth="o", arms=("out", "front"), hold=lambda c, hx, hy:
         loaf(c, hx, hy, 0.5))
    baker(cr, t, 540, 1000, 0.8, None, eyes="angry", brows="angry", arms=("point", "hips"))
    cr.restore()
    if t >= A("s1", "smelled"):
        stamp(cr, t, A("s1", "smelled"), 360, 420, "SMELLING BREAD", col=RED, size=58)
        cue("hit", t, A("s1", "smelled"))
    vignette(cr, 0.45)


def scene_bakery(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd8a0"), hexc("#fff1d6"), seed=2)
    cr.rectangle(0, 900, W, H - 900)
    cr.set_source(lin(0, 900, 0, H, [(0, hexc("#c8b8a0")), (1, hexc("#9a8a72"))]))
    cr.fill()
    rrect(cr, 300, 260, 400, 640, 10)                                # bakery front
    paint(cr, hexc("#f4e6c8"), OUTLINE, 6)
    for k in range(5):
        rrect(cr, 290 + k * 84, 220, 84, 70, 6)
        paint(cr, RED if k % 2 == 0 else WHITE, OUTLINE, 4)
    rrect(cr, 340, 380, 320, 240, 10)                                # window full of loaves
    paint(cr, hexc("#ffe7b8"), OUTLINE, 5)
    for k in range(6):
        loaf(cr, 400 + (k % 3) * 100, 470 + (k // 3) * 90, 0.6, 0.1 * (k - 2))
    bold_text(cr, "BAKERY", 500, 330, 50, hexc("#7a3a1a"), outline=None, shadow=0)
    steam(cr, t, 430, 380, n=4, h=200)
    sniff = t >= A("s2", "breathes")
    poor(cr, t, 170, 1000, 0.85, eyes="closed" if sniff else "open", mouth="smile", arms=("hold", "down"),
         hold=lambda c, hx, hy: loaf(c, hx, hy, 0.35), look=(0.5, -0.2))
    if sniff:                                                        # the smell drifting to his nose
        pts = [(lerp(420, 210, u), 400 + 80 * math.sin(u * 6 + t * 2)) for u in [j / 8 for j in range(9)]]
        stroke_line(cr, pts, 10, (1, 0.85, 0.5, 0.55))
        cue("sniff", t, A("s2", "breathes"))
    sign(cr, t, A("s2", "dry"), 360, 170, "DRY BREAD", col=hexc("#a8713e"), size=60, end=A("s2", "breathes") - 0.05)
    sign(cr, t, A("s2", "smell"), 360, 170, "+ FREE SMELL", col=GREEN, size=60)
    vignette(cr, 0.3)


def scene_baker(cr, t, tl):
    A = tl.at
    _court_bg(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("s3") - 0.3, (1.45, 400, 560))]))
    baker(cr, t, 400, 980, 1.0, tl, eyes="angry", brows="angry", arms=("fist", "hips"))
    cr.restore()
    sign(cr, t, A("s3", "pay"), 360, 170, "PAY FOR THE SMELL!", col=RED, size=58)
    vignette(cr, 0.45)


def scene_court2(cr, t, tl):
    A = tl.at
    _court_bg(cr, t)
    crowd(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("s4") - 0.3, (1.0, 360, 640)), (A("s4", "thinks."), (1.35, 360, 470))], dur=0.6))
    asks = t >= A("s4", "asks")
    judge(cr, t, 360, 600, 0.6, None, eyes="half", arms=("out", "front") if asks else ("chin", "front"))
    cr.restore()
    if t >= A("s4", "coins."):
        sign(cr, t, A("s4", "coins."), 360, 170, "YOUR COINS, PLEASE", col=GOLD, size=54)
    vignette(cr, 0.45)


def scene_coins(cr, t, tl):
    A = tl.at
    _court_bg(cr, t)
    if t < A("s6"):
        cr.save()                                                   # close-up: the last coins in a shaking hand
        enter(cr, camera(t, [(A("s5") - 0.3, (1.8, 260, 640))]))
        poor(cr, t, 260, 1000, 0.85, eyes="sad", mouth="sad", arms=("hold", "down"), sweat=True)
        cr.restore()
        coins(cr, t, 360, 720, 3, shake=0.2)
        sign(cr, t, A("s5", "last"), 360, 170, "HIS LAST COINS", col=PURPLE, size=60)
    else:
        cr.save()
        enter(cr, camera(t, [(A("s6") - 0.1, (1.3, 400, 560))]))
        baker(cr, t, 480, 980, 0.95, None, eyes="wide", brows="raise", arms=("hips", "hips"))
        judge(cr, t, 240, 980, 0.95, None, eyes="happy", mouth="smug", arms=("up", "down"))
        cr.restore()
        shake = 1.0 if t >= A("s6", "shakes") else 0.0
        coins(cr, t, 420, 380, 3, shake=shake)
        if shake:
            for k in range(3):                                      # jingle lines toward the baker's ear
                ph = (t * 2 + k / 3) % 1
                cr.arc(460, 400, 30 + 60 * ph, -0.5, 0.5)
                paint(cr, None, (1, 0.85, 0.3, 1 - ph), 5)
            cue("kaching", t, A("s6", "shakes"))
            sign(cr, t, A("s6", "ear."), 360, 170, "JINGLE JINGLE", col=GOLD, size=60)
    vignette(cr, 0.45)


def scene_paid(cr, t, tl):
    A = tl.at
    _court_bg(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("s7") - 0.3, (1.3, 360, 560))]))
    judge(cr, t, 240, 980, 0.95, tl, eyes="happy", arms=("out", "down"),
          hold=lambda c, hx, hy: coins(c, t, hx, hy, 3) if t < A("s8") else None)
    baker(cr, t, 480, 980, 0.95, tl, eyes="wide" if t >= A("s8") else "open", brows="raise",
          arms=("shrug", "shrug") if t >= A("s8") else ("hips", "hips"))
    cr.restore()
    sign(cr, t, A("s7", "paid."), 360, 170, "PAID.", col=GREEN, size=80, end=A("s8") - 0.05)
    if t >= A("s8"):
        sign(cr, t, A("s8", "what?"), 360, 170, "WITH WHAT?", col=RED, size=70)
    vignette(cr, 0.45)


def scene_verdict(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#55406e"), seed=4)
    loaf(cr, 190, 500, 1.4)
    steam(cr, t, 150, 440, n=3, h=160)
    coins(cr, t, 530, 510, 3, shake=1.0 if t >= A("s9", "sound") else 0.0)
    if t >= A("s9", "smell"):
        sign(cr, t, A("s9", "smell"), 190, 740, "THE SMELL", col=hexc("#a8713e"), size=46)
    if t >= A("s9", "sound"):
        sign(cr, t, A("s9", "sound"), 530, 740, "THE SOUND", col=GOLD, size=46)
        stroke_line(cr, [(300, 480), (420, 480)], 10, WHITE, curve=False)
        stroke_line(cr, [(420, 540), (300, 540)], 10, WHITE, curve=False)
    portrait(cr, t, A("s9"), 360, 270, 76, "judge", mouth=mouth_of(tl, "judge", t, "smug"), eyes="happy",
             bg=hexc("#ffd84d"))
    vignette(cr, 0.4)


def scene_home(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffb86a"), hexc("#ffe7a8"), seed=5)
    cr.rectangle(0, 900, W, H - 900)
    cr.set_source(lin(0, 900, 0, H, [(0, hexc("#c8b8a0")), (1, hexc("#9a8a72"))]))
    cr.fill()
    x = lerp(120, 560, seg(t, A("s10"), A("s10", end=True) + 0.8))
    poor(cr, t, x, 1000, 0.85, eyes="happy", mouth="grin", arms=("wave", "pocket"), walk=t * 10, run=True)
    coins(cr, t, x + 40, 760 + 10 * math.sin(t * 10), 2)
    sign(cr, t, A("s10", "every"), 360, 170, "EVERY COIN KEPT", col=GREEN, size=60)
    vignette(cr, 0.3)


def scene_today(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f3a4a"), hexc("#3f5a6e"), seed=6)
    sign(cr, t, A("s11", "folk"), 360, 170, "AN OLD FOLK TALE", col=hexc("#a8713e"), size=56, end=A("s11", "real") - 0.05)
    sign(cr, t, A("s11", "real"), 360, 170, "STILL A REAL QUESTION", col=PURPLE, size=52)
    if t >= A("s11", "music"):                                       # a café with music notes floating out
        rrect(cr, 60, 470, 280, 320, 14)
        paint(cr, hexc("#f4e6c8"), OUTLINE, 6)
        bold_text(cr, "CAFE", 200, 540, 46, hexc("#7a3a1a"), outline=None, shadow=0)
        for k in range(4):
            ph = (t * 0.7 + k / 4) % 1
            nx, ny = 200 + 120 * ph + 20 * math.sin(t * 3 + k), 640 - 200 * ph
            ellipse(cr, nx, ny, 14, 10)                             # a drawn music note
            paint(cr, (1, 0.85, 0.3, 1 - ph), alpha(OUTLINE, 1 - ph), 3)
            stroke_line(cr, [(nx + 12, ny), (nx + 12, ny - 44)], 5, alpha(OUTLINE, 1 - ph), curve=False)
    if t >= A("s11", "Wi-Fi."):                                      # Wi-Fi bars leaking over a fence
        cx, cy = 520, 740
        for k in range(3):
            cr.arc(cx, cy, 50 + k * 50, -math.pi * 0.75, -math.pi * 0.25)
            paint(cr, None, alpha(GREEN, 1 - 0.25 * k), 14)
        cr.arc(cx, cy, 14, 0, 2 * math.pi)
        paint(cr, GREEN, OUTLINE, 4)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    baker(cr, t, 200, 960, 0.6, None, eyes="angry", brows="angry", arms=("hips", "hips"))
    poor(cr, t, 520, 960, 0.6, eyes="happy", mouth="smile", arms=("down", "down"))
    sign(cr, t, A("s12", "taking?"), 360, 190, "IS IT STILL TAKING?", col=GOLD, size=52)
    sign(cr, t, A("s12", "Baker,"), 200, 380, "BAKER", col=RED, size=60, rot=-0.06)
    sign(cr, t, A("s12", "poor"), 520, 380, "POOR MAN", col=GREEN, size=52, rot=0.05)
    vignette(cr, 0.3)


SCENES = {"court": scene_court, "bakery": scene_bakery, "baker": scene_baker, "court2": scene_court2,
          "coins": scene_coins, "paid": scene_paid, "verdict": scene_verdict, "home": scene_home,
          "today": scene_today, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("HIS CRIME?", False), ("SMELLING BREAD", True)], end=tl.at("s2"), y=170, size=100)
    captions(cr, t, tl)
