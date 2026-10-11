"""Meme M6: "Me: I'll sleep early tonight." / "Me at 3 AM:" -- the kid is watching this exact meme for the 47th time.
~6 s loop.

Original meme in our own characters (owner picked M1, M3, M6 on 11 Oct 2026). No voice at all: the top caption bar
and our own sound hits. The phone shows this same video, and the replay tap cuts back to frame 0, so it loops.
"""
import math

from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.meme import bedroom, blanket, bed, clock, meme_bar, phone
from motion.pkit import GOLD, sparkles
from motion.polish import OUTLINE, WHITE, appear, bold_text, captions, paint, rrect, soft_disc, stroke_line, vignette
from motion.toons import head, person

NARRATOR = dict(speed=0.92)
TAIL = 0.1

SCRIPT = [
    dict(id="n1", scene="bed", text="", hold=1.6),
    dict(id="n2", scene="spin", text="", hold=0.7),
    dict(id="n3", scene="night", text="", hold=2.6),
    dict(id="n4", scene="replay", text="", hold=0.6),
]

METADATA = dict(
    title="Me at 3 AM: Watched It 47 Times 😭",
    alt_titles=["\"I'll Sleep Early Tonight\" 😭 (3 AM Me)", "Me: Sleeps Early. Also Me at 3 AM: 💀"],
    description="""Me: I'll sleep early tonight. 😴
Me at 3 AM: 📱👀

How many times did YOU watch this? Be honest 😭👇

🔔 Interestingly Strange: strange stories, school memes, mind-bending paradoxes and weird history, animated.""",
    hashtags=["#Memes", "#Relatable", "#Shorts"],
    tags=["3am memes", "relatable memes", "sleep memes", "me at 3am", "phone addiction", "funny shorts",
          "student memes", "animated memes", "interestingly strange"],
    pinned_comment="Be honest: how many times did you watch this? 😭👇",
)

KX, KY, KS = 330, 1000, 0.95     # the kid sitting up in bed (feet hidden under the blanket)


def _kid(cr, t, eyes, mouth, night=False):
    bed(cr, KX, KY)
    person(cr, t, KX, KY + 120, KS, "kid", eyes=eyes, mouth=mouth, arms=("hold", "hold") if night else ("down", "down"),
           shadow=False, shirt=hexc("#8fd0a0"))
    blanket(cr, KX + 40, KY + 40, hexc("#4aa3f0") if not night else hexc("#2a5a8a"))


def scene_bed(cr, t, tl):
    bedroom(cr, dark=False)
    soft_disc(cr, 610, 760, 160, (1, 0.9, 0.6, 0.35))       # bedside lamp
    rrect(cr, 560, 760, 100, 120, 10)
    paint(cr, hexc("#8a5a2b"), OUTLINE, 5)
    clock(cr, t, 150, 420, 75, 10, 0)
    closed = t >= 0.9
    _kid(cr, t, "closed" if closed else "happy", "smile")
    # the phone goes face down on the bedside table
    u = ease_out(seg(t, 0.0, 0.5))
    phone(cr, lerp(420, 610, u), lerp(800, 745, u), 0.5, rot=lerp(0.3, 1.57, u), glow=not closed)
    if closed:
        for k in range(3):
            ph = (t * 0.8 + k / 3) % 1
            bold_text(cr, "z", 470 + ph * 80, 560 - ph * 140, 30 + 20 * ph, WHITE)
    meme_bar(cr, t, 0.0, ["Me: I'll sleep", "early tonight."])
    vignette(cr, 0.3)


def scene_spin(cr, t, tl):
    A = tl.at
    s0 = A("n2")
    u = seg(t, s0, s0 + 0.7)
    cr.rectangle(0, 0, W, H)
    cr.set_source_rgba(*(lerp(0.6, 0.06, u) for _ in range(3)), 1)
    cr.fill()
    mins = 10 * 60 + u * 5 * 60          # 10:00 PM -> 3:00 AM
    clock(cr, t, 360, 620, 230, int(mins // 60), mins % 60, dark=u > 0.5)
    cue("whoosh", t, s0, 0.6)


def scene_night(cr, t, tl):
    A = tl.at
    s0 = A("n3")
    bedroom(cr, dark=True)
    clock(cr, t, 110, 420, 65, 3, 0, dark=True)
    _kid(cr, t, "wide", "grin", night=True)
    hx, hy = KX, KY + 120 - 392 * KS          # head centre
    r = 94 * KS
    soft_disc(cr, hx + 40, hy, 230, (0.5, 0.75, 1.0, 0.28))   # phone light on his face

    def screen(c, w, h):                       # the phone shows this same meme
        c.rectangle(0, 0, w, h)
        c.set_source_rgba(*hexc("#141830"))
        c.fill()
        rrect(c, 8, 10, w - 16, 34, 6)
        paint(c, WHITE, None, 0)
        bold_text(c, "Me at 3 AM:", w / 2, 33, 15, hexc("#1b1b1f"), font="Fredoka", outline=None, shadow=0)
        head(c, t, w / 2, 130, 34, "kid", eyes="wide", mouth="grin")
        rrect(c, w / 2 - 14, 168, 28, 44, 5)
        paint(c, hexc("#1b1b1f"), WHITE, 2)

    phone(cr, hx + 175, hy + 130, 1.35, rot=-0.12, screen=screen)
    counts = [45, 46, 47]
    k = min(2, int((t - s0) / 0.7))
    for j in range(k + 1):
        cue("pop", t, s0 + 0.15 + 0.7 * j)
    if t >= s0 + 0.15:
        sc = 1 + 0.25 * max(0.0, 1 - (t - s0 - 0.15 - 0.7 * k) / 0.2)
        cr.save()
        cr.translate(360, 265)
        cr.scale(sc, sc)
        bold_text(cr, f"WATCHED: {counts[k]} TIMES", 0, 0, 54, GOLD)
        cr.restore()
    meme_bar(cr, t, s0, ["Me at 3 AM:"])
    vignette(cr, 0.5)


def scene_replay(cr, t, tl):
    A = tl.at
    s0 = A("n4")
    bedroom(cr, dark=True)
    _kid(cr, t, "happy", "grin", night=True)
    k = max(appear(t, s0, 0.2), 0.02)
    cr.save()
    cr.translate(360, 600)
    cr.scale(k, k)
    cr.arc(0, 0, 130, 0, 2 * math.pi)
    paint(cr, (1, 1, 1, 0.92), OUTLINE, 8)
    cr.arc(0, 0, 70, -0.3, 4.6)
    cr.set_line_width(22)
    cr.set_source_rgba(0.1, 0.1, 0.12, 1)
    cr.stroke()
    cr.move_to(66, -60)
    cr.line_to(110, -2)
    cr.line_to(40, 6)
    cr.close_path()
    cr.fill()
    cr.restore()
    cue("pop", t, s0)
    meme_bar(cr, t, s0 - 0.24, ["Me at 3 AM:"])
    vignette(cr, 0.5)


SCENES = {"bed": scene_bed, "spin": scene_spin, "night": scene_night, "replay": scene_replay}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    if name not in ("replay",):
        whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
