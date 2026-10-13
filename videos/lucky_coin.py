"""The lucky coin -- an original twist story (told as a story, not as true), polished look.

For sixty years a man lets a coin make every big choice. On his eightieth birthday his grandson sees that it has heads
on both sides. Script approved by the owner on 13 Oct 2026 (out/scripts_batch_47-50.md doc, with the "Hook fix" first
line); the description opens with "A short story" so nobody reads it as true.
"""
import math

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.meme import living_room
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, check, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, enter, lin, paint, rad, rrect,
                           shade, sign, smooth, soft_disc, soft_rrect, stamp, stroke_line, vignette)
from motion.timeline import clear_dialogue
from motion.toons import person

NARRATOR = dict(speed=0.92)
TAIL = 0.9
voice.SPEAKERS.update({"kid": dict(voice="am_puck", speed=1.04, pitch=2.5),
                       "grandpa": dict(voice="bm_george", speed=0.92, pitch=-1.5)})

SCRIPT = [
    dict(id="c1", scene="birthday", text="On his eightieth birthday, Grandpa finally let his grandson hold the lucky "
                                         "coin."),
    dict(id="c2", scene="flash", text="For sixty years, that coin made every big choice in his life.", gap=0.3),
    dict(id="c3", scene="flash", text="Heads, yes. Tails, no."),
    dict(id="c4", scene="job", text="Take the job? He flipped it. Heads. Best job he ever had."),
    dict(id="c5", scene="city", text="Move to a new city? Heads."),
    dict(id="c6", scene="love", text="Ask her out? Heads. They were married for fifty years."),
    dict(id="c7", scene="friends", text="His friends called it the lucky coin."),
    dict(id="c8", scene="flip", text="Now the grandson flipped it over. And froze.", gap=0.35),
    dict(id="c9", scene="flip", text="Heads. And heads.", gap=0.35, pace=0.9),
    dict(id="c10", scene="talk", text="Grandpa, it never decided anything!", speaker="kid"),
    dict(id="c11", scene="talk", text="I know. I always knew what I wanted. I just needed a reason to be brave.",
         speaker="grandpa"),
    dict(id="c12", scene="end", text="So, was he brave, or was he cheating?", gap=0.3, pace=0.95),
]
clear_dialogue(SCRIPT, ids=["c10", "c11"], pace=0.95)

METADATA = dict(
    title="Heads, Yes. Tails, No. For 60 Years 🪙",
    alt_titles=["He Let a Coin Run His Life for 60 Years 🪙", "Grandpa's Lucky Coin Wasn't Lucky 🪙",
                "The Coin That Made Every Choice 🪙"],
    description="""A short story: for 60 years, one coin made every big choice in his life. Then his grandson looked at it. 🪙

On his 80th birthday, Grandpa finally let his grandson hold the lucky coin. Heads, yes. Tails, no.
Take the job? Heads. Move to a new city? Heads. Ask her out? Heads, and they were married for fifty years.
Then the grandson flipped it over… and froze. Heads. And heads.
"Grandpa, it never decided anything!"
"I know. I always knew what I wanted. I just needed a reason to be brave."

(An original short story.)

💬 So, was he brave, or was he cheating? 👇

🔔 Interestingly Strange: strange stories with a twist, The Last Bencher, paradoxes and weird history, animated.""",
    hashtags=["#ShortStory", "#PlotTwist", "#Shorts"],
    tags=["twist story", "short story", "coin flip", "lucky coin", "story with a twist", "life lesson", "plot twist",
          "animated story", "grandpa story", "interestingly strange"],
    pinned_comment="Brave, or cheating? 🪙 What's the biggest choice YOU would leave to a coin? 👇",
)

SEPIA = (0.55, 0.38, 0.15)


# ---------------------------------------------------------------- props
def coin(cr, t, x, y, r, face="H", spin=None, glow=True):
    """A gold coin; `spin` (a phase) flips it edge-on and back, showing `face` on both sides."""
    k = 1.0 if spin is None else abs(math.cos(spin))
    if glow:
        soft_disc(cr, x, y, r * 2.2, (1, 0.85, 0.3, 0.3))
    cr.save()
    cr.translate(x, y)
    cr.scale(max(k, 0.06), 1)
    cr.arc(0, 0, r, 0, 2 * math.pi)
    paint(cr, rad(-r * 0.3, -r * 0.4, r * 1.4, [(0, hexc("#fff0a0")), (0.6, hexc("#f0c040")), (1, hexc("#b8861a"))]),
          OUTLINE, max(3, r * 0.08))
    cr.arc(0, 0, r * 0.8, 0, 2 * math.pi)
    cr.set_line_width(r * 0.05)
    cr.set_source_rgba(0.6, 0.42, 0.08, 0.6)
    cr.stroke()
    if k > 0.3:
        bold_text(cr, face, 0, r * 0.34, r * 0.95, hexc("#a87410"), font="Fredoka", outline=None, shadow=0)
    cr.restore()


def toss(cr, t, start, x, y, r=40, height=260):
    """A coin flipped up from (x, y) at `start`, landing heads after 0.8 s."""
    u = seg(t, start, start + 0.8)
    if t < start:
        return False
    yy = y - height * math.sin(u * math.pi)
    coin(cr, t, x, yy, r, "H", spin=None if u >= 1 else t * 20)
    if u >= 1:
        cue("kaching", t, start + 0.8)
        return True
    if u < 0.1:
        cue("whoosh", t, start, 0.4)
    return False


def sepia(cr, a=0.28):
    cr.rectangle(0, 0, W, H)
    cr.set_source_rgba(*SEPIA, a)
    cr.fill()


def young(cr, t, x, y, s, **kw):
    """Grandpa sixty years ago: dark hair, no glasses."""
    person(cr, t, x, y, s, "grandpa", hair="short", hair_col=hexc("#2b1a12"), stache=hexc("#2b1a12"), glasses=False,
           suit=hexc("#3a5a8a"), shirt=WHITE, **kw)


def cake(cr, t, x, y, label="80"):
    rrect(cr, x - 120, y - 100, 240, 100, 16)
    paint(cr, lin(0, y - 100, 0, y, [(0, hexc("#fff0d8")), (1, hexc("#e8c89a"))]), OUTLINE, 5)
    rrect(cr, x - 130, y - 112, 260, 24, 12)
    paint(cr, hexc("#ff8fb5"), OUTLINE, 4)
    bold_text(cr, label, x, y - 28, 58, RED)
    for k in range(4):
        cx = x - 75 + k * 50
        rrect(cr, cx - 6, y - 165, 12, 54, 4)
        paint(cr, hexc("#9fd0ff"), OUTLINE, 3)
        smooth(cr, [(cx, y - 168), (cx - 8, y - 182), (cx, y - 200 + 3 * math.sin(t * 12 + k)), (cx + 8, y - 182)])
        paint(cr, GOLD, hexc("#ff8a3c"), 2)


def table(cr, y=860):
    rrect(cr, 30, y, W - 60, 36, 10)
    paint(cr, lin(0, y, 0, y + 36, [(0, hexc("#b9824a")), (1, hexc("#8a5a2e"))]), OUTLINE, 5)


# ---------------------------------------------------------------- scenes
def scene_birthday(cr, t, tl):
    A = tl.at
    living_room(cr)
    table(cr)
    cake(cr, t, 360, 860)
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("c1", "coin."), (1.25, 360, 560))], dur=0.8))
    person(cr, t, 150, 1080, 0.85, "grandpa", eyes="happy", mouth="smile", arms=("out", "down"))
    hold = A("c1", "hold")
    person(cr, t, 580, 1080, 0.75, "kid", eyes="wide" if t >= hold else "open", mouth="o" if t >= hold else "smile",
           arms=("out", "down"), facing=-1)
    u = ease_out(seg(t, hold, hold + 0.7))
    coin(cr, t, lerp(250, 470, u), lerp(620, 600, u) - 60 * math.sin(u * math.pi), 34)
    cr.restore()
    sign(cr, t, -0.5, 360, 120, "THE LUCKY COIN", col=GOLD, size=64)
    tag(cr, t, A("c1", "eightieth"), 360, 300, "80TH BIRTHDAY", col=PURPLE, size=40)
    vignette(cr, 0.35)


def scene_flash(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e4c0"), hexc("#d8b878"), seed=2)
    coin(cr, t, 360, 450, 130, "H", spin=t * 2.2)
    sepia(cr, 0.22)
    tag(cr, t, A("c2", "sixty"), 360, 180, "60 YEARS", col=PURPLE, size=56)
    if t >= A("c3"):
        card(cr, t, A("c3"), 360, 750, 520, 180, "THE RULE", ["HEADS = YES", "TAILS = NO"], col=BLUE,
             title_size=40, line_size=46)
    vignette(cr, 0.45)


def scene_job(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#d8e8f4"), hexc("#f4f0e6"), seed=4)
    for k in range(3):                                     # office windows
        rrect(cr, 60 + k * 210, 160, 180, 260, 8)
        paint(cr, lin(0, 160, 0, 420, [(0, hexc("#9fd6ff")), (1, hexc("#e8f7ff"))]), OUTLINE, 4)
    landed = toss(cr, t, A("c4", "flipped"), 470, 640, 44)
    young(cr, t, 250, 1000, 0.9, eyes="happy" if landed else "open", mouth="grin" if landed else "smile",
          arms=("hold", "out"), hold=lambda c, hx, hy: (rrect(c, hx - 30, hy, 60, 46, 6),
                                                         paint(c, hexc("#5a3a24"), OUTLINE, 4)))
    if landed:
        check(cr, t, A("c4", "Heads.") + 0.1, 560, 560, 40)
        sign(cr, t, A("c4", "Best"), 360, 820, "BEST JOB EVER", col=GREEN, size=52)
    sign(cr, t, A("c4"), 360, 110, "TAKE THE JOB?", col=BLUE, size=58)
    sepia(cr, 0.18)
    vignette(cr, 0.4)


def scene_city(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffc8a0"), hexc("#ffe8c8"), seed=5)
    for k, (bx, bh) in enumerate(((60, 300), (160, 420), (270, 340), (380, 480), (500, 360), (600, 420))):
        rrect(cr, bx, 760 - bh, 90, bh, 6)
        paint(cr, hexc("#6a5a8a"), OUTLINE, 4)
        for j in range(int(bh / 70)):
            cr.rectangle(bx + 20, 760 - bh + 20 + j * 60, 18, 24)
            cr.rectangle(bx + 52, 760 - bh + 20 + j * 60, 18, 24)
            cr.set_source_rgba(1, 0.9, 0.5, 0.8)
            cr.fill()
    landed = toss(cr, t, A("c5"), 520, 640, 44)
    young(cr, t, 240, 1000, 0.9, eyes="happy", mouth="grin" if landed else "smile", arms=("hold", "wave"),
          hold=lambda c, hx, hy: (rrect(c, hx - 40, hy, 80, 60, 8), paint(c, hexc("#c8402e"), OUTLINE, 4)))
    if landed:
        check(cr, t, A("c5", "Heads."), 610, 560, 40)
    sign(cr, t, A("c5"), 360, 110, "NEW CITY?", col=PURPLE, size=60)
    sepia(cr, 0.16)
    vignette(cr, 0.4)


def scene_love(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd8e8"), hexc("#fff1e6"), seed=6)
    wed = A("c6", "married")
    if t < wed:
        landed = toss(cr, t, A("c6", "Ask"), 360, 560, 40)
        young(cr, t, 200, 1000, 0.88, eyes="happy" if landed else "open", mouth="grin" if landed else "o",
              arms=("chin", "down"), facing=1)
        person(cr, t, 530, 1000, 0.85, "mother", eyes="happy", mouth="smile", arms=("down", "down"), facing=-1)
        if landed:
            sparkles(cr, t, A("c6", "Heads."), 360, 520, n=6, seed=2, col=RED, spread=140)
        sign(cr, t, A("c6"), 360, 110, "ASK HER OUT?", col=RED, size=58)
    else:
        k = appear(t, wed, 0.4)
        cr.save()
        cr.translate(360, 560)
        cr.scale(k, k)
        rrect(cr, -230, -260, 460, 460, 16)
        paint(cr, hexc("#c8a040"), OUTLINE, 8)
        rrect(cr, -200, -230, 400, 400, 8)
        paint(cr, hexc("#f4ecd8"), OUTLINE, 4)
        young(cr, t, -80, 160, 0.62, eyes="happy", mouth="grin", arms=("down", "out"), shadow=False)
        person(cr, t, 80, 160, 0.6, "mother", eyes="happy", mouth="grin", arms=("out", "down"), shadow=False,
               shirt=WHITE)
        cr.restore()
        for j in range(5):
            ph = (t * 0.6 + j / 5) % 1
            bold_text(cr, "♥", 120 + j * 120, 900 - ph * 300, 40, alpha(RED, 1 - ph), font="DejaVu Sans",
                      outline=None, shadow=0)
        tag(cr, t, A("c6", "fifty"), 360, 180, "50 YEARS", col=RED, size=56)
    sepia(cr, 0.14)
    vignette(cr, 0.4)


def scene_friends(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e4c0"), hexc("#fff1d6"), seed=8)
    coin(cr, t, 360, 420, 90, "H", spin=t * 1.5)
    sparkles(cr, t, A("c7"), 360, 420, n=8, seed=4, col=GOLD, spread=160)
    for k, (x, who) in enumerate(((110, "fermi"), (300, "villager"), (480, "lewis"), (640, "mother"))):
        person(cr, t, x, 1020, 0.7, who, eyes="happy", mouth="grin", arms=("point", "down"),
               facing=1 if x < 360 else -1, seed=k)
    sign(cr, t, A("c7", "lucky"), 360, 130, "THE LUCKY COIN", col=GOLD, size=60)
    sepia(cr, 0.12)
    vignette(cr, 0.4)


def scene_flip(cr, t, tl):
    A = tl.at
    living_room(cr)
    froze = A("c8", "froze.")
    both = A("c9")
    if t < both:
        cr.save()
        enter(cr, camera(t, [(A("c8") - 0.3, (1.0, 360, 640)), (froze, (1.3, 400, 560))], dur=0.5))
        person(cr, t, 470, 1080, 0.85, "kid", eyes="wide" if t >= froze else "open",
               mouth="o" if t >= froze else "smile", brows="up" if t >= froze else None, arms=("out", "down"),
               facing=-1, sweat=t >= froze)
        spin = None if t >= froze else (t * 9 if t >= A("c8", "flipped") else None)
        coin(cr, t, 330, 640, 60, "H", spin=spin)
        cr.restore()
    else:
        studio(cr, t, hexc("#2a2a3a"), hexc("#4a3a5a"), seed=3)
    stamp(cr, t, froze, 360, 160, "FROZE", col=BLUE, size=80, end=both - 0.05)
    if t >= both:
        coin(cr, t, 210, 520, 120, "H")
        if t >= A("c9", "heads.", nth=2):
            coin(cr, t, 510, 520, 120 * appear(t, A("c9", "heads.", nth=2), 0.25) + 1, "H")
            cue("hit", t, A("c9", "heads.", nth=2))
        bold_text(cr, "SIDE 1", 210, 720, 40, WHITE)
        if t >= A("c9", "heads.", nth=2):
            bold_text(cr, "SIDE 2", 510, 720, 40, WHITE)
            stamp(cr, t, A("c9", "heads.", nth=2) + 0.2, 360, 220, "2x HEADS", col=RED, size=84)
    vignette(cr, 0.4)


def scene_talk(cr, t, tl):
    A = tl.at
    living_room(cr)
    table(cr)
    cake(cr, t, 360, 860)
    g_talk = tl.speaking("grandpa", t)
    k_talk = tl.speaking("kid", t)
    wink = t >= A("c11", "brave.")
    person(cr, t, 170, 1080, 0.9, "grandpa", eyes="closed" if wink else "happy",
           mouth="talk" if g_talk else ("smug" if wink else "smile"),
           arms=("pocket", "down") if wink else ("hips", "down"))
    person(cr, t, 560, 1080, 0.78, "kid", eyes="wide", mouth="talk" if k_talk else "o", arms=("point", "down"),
           facing=-1, brows="up")
    if t < A("c11", "brave."):
        coin(cr, t, 430, 770, 28, "H")
    if t >= A("c11", "brave."):
        sparkles(cr, t, A("c11", "brave."), 170, 560, n=5, seed=6, col=GOLD, spread=80)
        sign(cr, t, A("c11", "brave."), 360, 160, "A REASON TO BE BRAVE", col=GOLD, size=46)
    vignette(cr, 0.35)


def scene_end(cr, t, tl):
    A = tl.at
    living_room(cr)
    table(cr)
    cake(cr, t, 360, 860)
    person(cr, t, 170, 1080, 0.9, "grandpa", eyes="happy", mouth="smug", arms=("pocket", "down"))
    person(cr, t, 560, 1080, 0.78, "kid", eyes="half", mouth="flat", arms=("hips", "hips"), facing=-1)
    buttons(cr, t, A("c12", "brave,"), [("BRAVE", GREEN), ("CHEATING", RED)], y=330, size=48, w=300)
    sign(cr, t, A("c12"), 360, 150, "YOUR VERDICT?", col=GOLD, size=60)
    vignette(cr, 0.35)


SCENES = {"birthday": scene_birthday, "flash": scene_flash, "job": scene_job, "city": scene_city,
          "love": scene_love, "friends": scene_friends, "flip": scene_flip, "talk": scene_talk, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
