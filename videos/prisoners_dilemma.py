"""Two Friends, One Broken Window -- the prisoner's dilemma as a school story, in the polished look.

Script: out/scripts_batch_oct26-31.md, row 62 (owner approved 18 Oct 2026). Original story on the classic
prisoner's dilemma payoffs (quiet/quiet 1 day each, blame/quiet 0 and 10, blame/blame 5 each): blaming is better
whatever the friend does, so both blame and both get 5 instead of 1. Everyday example: two shops in a price war.
Closing debate: trust your friend, or save yourself? Turbo stock female narrator with tags; the coach through Turbo
with a Kokoro reference voice.
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, enter, lin, paint, rad, rrect,
                           shade, sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person, portrait
from videos.last_bencher_4 import BLUE, GOLD, GREEN, PURPLE, RED, mouth_of, red_x, room, sparkles, studio

NARRATOR = dict(turbo=True)
TAIL = 1.0
voice.SPEAKERS.update({"coach": dict(voice="am_eric", speed=1.0, turbo_ref="am_eric")})
COACH = dict(skin="brown", hair="short", hair_col=hexc("#1e130d"), shirt=hexc("#e8473f"), suit=hexc("#e8473f"),
             pants=hexc("#2b2b33"), build="adult")
FRIEND_A = "kid"
FRIEND_B = "student2"

SCRIPT = [
    dict(id="p1", scene="window", text="A window is smashed. Two best friends are caught nearby. And the coach puts "
                                       "them in separate rooms."),
    dict(id="p2", scene="deal", text="If you both stay quiet, one day of detention each.", speaker="coach"),
    dict(id="p3", scene="deal", text="If you blame your friend, and he stays quiet, you walk free. He gets ten days.",
         speaker="coach"),
    dict(id="p4", scene="deal", text="If you both blame each other, five days each.", speaker="coach"),
    dict(id="p5", scene="think", text="Now think like the first friend."),
    dict(id="p6", scene="think", text="If my friend stays quiet, blaming him sets me free. Better than one day."),
    dict(id="p7", scene="think", text="If my friend blames me, blaming him gets me five days. Better than ten."),
    dict(id="p8", scene="think", text="So whatever he does, blaming is smarter."),
    dict(id="p9", scene="split", text="And in the other room, his friend thinks the exact same thing. [gasp]"),
    dict(id="p10", scene="both", text="Both blame. Five days each. When staying quiet would have cost one. [sigh]"),
    dict(id="p11", scene="shops", text="Being smart alone made them both lose. It's called the prisoner's dilemma. "
                                       "It's why two shops cut prices until neither makes money."),
    dict(id="p12", scene="end", text="So, you're in that room. Trust your friend, or save yourself?", gap=0.3),
]

METADATA = dict(
    title="2 Best Friends. 1 Broken Window. 2 Rooms. 🪟",
    alt_titles=["Blame Your Friend or Stay Quiet? (Prisoner's Dilemma) 🪟", "Why Being Smart Made Both Friends Lose 🧠"],
    description="""A window is smashed. Two best friends are caught nearby, and the coach puts them in separate rooms. 🪟

Both stay quiet: 1 day of detention each.
You blame him and he stays quiet: you walk free, he gets 10 days.
Both blame: 5 days each.

Whatever your friend does, blaming is "smarter"... so both blame, and both get 5 days instead of 1. That's the prisoner's dilemma, and it's why two shops can cut prices until neither makes money. 🤯

💬 You're in that room. Trust your friend, or save yourself? 👇

🔔 Interestingly Strange: clever twists, The Last Bencher and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#PrisonersDilemma", "#GameTheory", "#Shorts"],
    tags=["prisoner's dilemma", "game theory", "trust or betray", "best friends", "psychology", "school story",
          "would you rather", "decision making", "brain teaser", "interestingly strange"],
    pinned_comment="Trust your friend 🤝 or save yourself 🏃? Be honest 👇",
)


def coach(cr, t, x, y, s, tl=None, **kw):
    kw.setdefault("mouth", "talk" if tl is not None and tl.speaking("coach", t) else "flat")
    person(cr, t, x, y, s, "sir", **dict(COACH, **kw))
    cr.save()                                                       # whistle on a cord
    cr.translate(x, y)
    cr.scale(s, s)
    stroke_line(cr, [(-30, -372), (0, -300), (30, -372)], 3, WHITE, curve=True)
    rrect(cr, -12, -306, 24, 16, 5)
    paint(cr, hexc("#c8c8d0"), OUTLINE, 3)
    cr.restore()


def payoff(cr, t, start, x, y, a, b, label_a, label_b, col_a, col_b, s=1.0, hot=False):
    """A deal card: what each friend does, and the days each one gets."""
    if t < start:
        return
    k = max(0.01, appear(t, start, 0.35))
    cr.save()
    cr.translate(x, y)
    cr.scale(k * s, k * s)
    rrect(cr, -330, -85, 660, 170, 30)
    paint(cr, (1, 1, 1, 0.94) if not hot else hexc("#fff3c4"), OUTLINE, 7)
    bold_text(cr, label_a, -240, -18, 38, col_a)
    bold_text(cr, "+", -155, -18, 40, OUTLINE, outline=None, shadow=0)
    bold_text(cr, label_b, -70, -18, 38, col_b)
    bold_text(cr, a, 120, 6, 70, col_a)
    bold_text(cr, "/", 185, 6, 56, OUTLINE, outline=None, shadow=0)
    bold_text(cr, b, 250, 6, 70, col_b)
    bold_text(cr, "DAYS", 185, 62, 30, OUTLINE, outline=None, shadow=0)
    bold_text(cr, "YOU", -240, 40, 26, alpha(OUTLINE, 0.6), outline=None, shadow=0)
    bold_text(cr, "FRIEND", -70, 40, 26, alpha(OUTLINE, 0.6), outline=None, shadow=0)
    cr.restore()


def small_room(cr, t, x, y, w, h, who, eyes="open", mouth="flat", arms=("front", "front"), sweat=False, bubble=None):
    rrect(cr, x, y, w, h, 18)
    paint(cr, lin(0, y, 0, y + h, [(0, hexc("#d8e4ee")), (1, hexc("#a8b8c8"))]), OUTLINE, 6)
    rrect(cr, x + w * 0.2, y + h - 70, w * 0.6, 22, 6)               # little table
    paint(cr, hexc("#8a5a2e"), OUTLINE, 4)
    person(cr, t, x + w / 2, y + h - 20, min(0.62, 0.62 * h / 460), who, eyes=eyes, mouth=mouth, arms=arms,
           sweat=sweat, shadow=False)
    if bubble:
        rrect(cr, x + w / 2 - 110, y - 110, 220, 90, 30)
        paint(cr, WHITE, OUTLINE, 5)
        bold_text(cr, bubble, x + w / 2, y - 48, 46, RED)


def scene_window(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#8fd0f0"), hexc("#e8f6ff"), seed=1)
    cr.rectangle(0, 860, W, H - 860)
    cr.set_source(lin(0, 860, 0, H, [(0, hexc("#6ab86a")), (1, hexc("#3f8a4a"))]))
    cr.fill()
    rrect(cr, 60, 160, 600, 700, 10)                                 # school wall
    paint(cr, hexc("#e8c89a"), OUTLINE, 6)
    rrect(cr, 220, 260, 280, 260, 10)                                # the broken window
    paint(cr, hexc("#9fd6ff"), OUTLINE, 7)
    if t >= 0.15:
        for k in range(7):
            a = k * 0.9 + 0.3
            stroke_line(cr, [(360, 390), (360 + 140 * math.cos(a), 390 + 120 * math.sin(a))], 4, OUTLINE,
                        curve=False)
        cue("hit", t, 0.15)
    cr.arc(360, 390, 22, 0, 2 * math.pi)                             # the ball stuck in it
    paint(cr, hexc("#ff8a3c"), OUTLINE, 4)
    caught = t >= A("p1", "caught")
    person(cr, t, 200, 1000, 0.7, FRIEND_A, eyes="wide" if caught else "happy", mouth="o" if caught else "grin",
           arms=("up", "up") if caught else ("down", "down"), seed=1)
    person(cr, t, 330, 1000, 0.7, FRIEND_B, eyes="wide" if caught else "happy", mouth="o" if caught else "grin",
           arms=("face", "face") if caught else ("down", "down"), seed=2)
    if caught:
        coach(cr, t, 560, 1000, 0.85, None, eyes="angry", brows="angry", arms=("point", "hips"))
    if t >= A("p1", "separate"):
        sign(cr, t, A("p1", "separate"), 360, 600, "SEPARATE ROOMS", col=RED, size=56)
    vignette(cr, 0.4)


def scene_deal(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2b2f4a"), hexc("#4a4f6e"), seed=3)
    payoff(cr, t, A("p2", "quiet,"), 360, 330, "1", "1", "QUIET", "QUIET", GREEN, GREEN)
    payoff(cr, t, A("p3", "blame"), 360, 535, "0", "10", "BLAME", "QUIET", RED, GREEN)
    payoff(cr, t, A("p4", "both"), 360, 740, "5", "5", "BLAME", "BLAME", RED, RED)
    portrait(cr, t, A("p2"), 600, 140, 70, "sir", mouth=mouth_of(tl, "coach", t, "flat"), eyes="angry",
             bg=hexc("#ffb3a8"), end=A("p4", end=True), **{k: v for k, v in COACH.items() if k != "build"})
    vignette(cr, 0.45)


def scene_think(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f3a4a"), hexc("#3f5a6e"), seed=5)
    small_room(cr, t, 200, 640, 320, 260, FRIEND_A, eyes="half", mouth="flat", arms=("think", "front"))
    sign(cr, t, A("p5", "first"), 360, 170, "FRIEND #1 THINKS", col=BLUE, size=56, end=A("p8") - 0.05)
    for row, (beat, title, a_, b_, y) in enumerate((("p6", "IF HE STAYS QUIET", "0", "1", 290),
                                                    ("p7", "IF HE BLAMES ME", "5", "10", 470))):
        if t < A(beat):
            continue
        bold_text(cr, title, 360, y, 44, WHITE)
        bold_text(cr, f"BLAME: {a_}", 200, y + 80, 56, RED)
        bold_text(cr, f"QUIET: {b_}", 520, y + 80, 56, GREEN)
        if t >= A(beat, "Better"):
            rrect(cr, 60, y + 22, 280, 80, 24)
            paint(cr, None, GOLD, 8)
    if t >= A("p8", "blaming"):
        sign(cr, t, A("p8", "blaming"), 360, 170, "BLAME WINS... RIGHT?", col=RED, size=56)
        cue("hit", t, A("p8", "blaming"))
    vignette(cr, 0.4)


def scene_split(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f2a3a"), hexc("#3a4a5e"), seed=6)
    same = t >= A("p9", "same")
    small_room(cr, t, 30, 420, 320, 460, FRIEND_A, eyes="half", mouth="smug", bubble="BLAME")
    small_room(cr, t, 370, 420, 320, 460, FRIEND_B, eyes="half", mouth="smug" if same else "flat",
               bubble="BLAME" if same else "...")
    if same:
        sign(cr, t, A("p9", "same"), 360, 170, "THE EXACT SAME THING", col=RED, size=52)
    vignette(cr, 0.45)


def scene_both(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    cr.save()
    enter(cr, camera(t, [(A("p10") - 0.3, (1.1, 360, 640))]))
    person(cr, t, 230, 960, 0.8, FRIEND_A, eyes="sad", mouth="sad", arms=("down", "down"), seed=1)
    person(cr, t, 490, 960, 0.8, FRIEND_B, eyes="sad", mouth="sad", arms=("down", "down"), seed=2)
    cr.restore()
    stamp(cr, t, A("p10", "Five"), 360, 330, "5 DAYS EACH", col=RED, size=70)
    if t >= A("p10", "one."):
        sign(cr, t, A("p10", "one."), 360, 520, "COULD HAVE BEEN 1", col=GREEN, size=50)
    vignette(cr, 0.45)


def shop(cr, t, x, y, price, col, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    rrect(cr, -130, -280, 260, 280, 10)
    paint(cr, hexc("#f4efe6"), OUTLINE, 6)
    for k in range(5):                                              # striped awning
        rrect(cr, -140 + k * 56, -320, 56, 60, 6)
        paint(cr, col if k % 2 == 0 else WHITE, OUTLINE, 4)
    rrect(cr, -90, -200, 180, 90, 10)
    paint(cr, WHITE, OUTLINE, 5)
    bold_text(cr, f"${price}", 0, -140, 56, RED)
    cr.restore()


def scene_shops(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffe7a8"), hexc("#fff6e8"), seed=7)
    if t < A("p11", "shops"):
        person(cr, t, 250, 880, 0.75, FRIEND_A, eyes="sad", mouth="sad", arms=("down", "down"), seed=1)
        person(cr, t, 470, 880, 0.75, FRIEND_B, eyes="sad", mouth="sad", arms=("down", "down"), seed=2)
        sign(cr, t, A("p11"), 360, 300, "SMART ALONE = BOTH LOSE", col=PURPLE, size=46, end=A("p11", "called") - 0.05)
        sign(cr, t, A("p11", "prisoner's"), 360, 300, "THE PRISONER'S DILEMMA", col=GOLD, size=50)
    else:
        u = seg(t, A("p11", "cut"), A("p11", "money.", end=True))
        price = max(1, int(round(10 - 9 * u)))
        shop(cr, t, 190, 860, price, RED, 1.2)
        shop(cr, t, 530, 860, max(1, price - (1 if u < 0.95 else 0)), BLUE, 1.2)
        if t >= A("p11", "neither"):
            stamp(cr, t, A("p11", "money."), 360, 300, "NOBODY WINS", col=RED, size=62)
    vignette(cr, 0.3)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    small_room(cr, t, 180, 560, 360, 320, FRIEND_A, eyes="half", mouth="flat", arms=("think", "front"))
    sign(cr, t, A("p12", "room."), 360, 190, "YOU'RE IN THAT ROOM", col=GOLD, size=52)
    sign(cr, t, A("p12", "Trust"), 190, 400, "TRUST", col=GREEN, size=60, rot=-0.06)
    sign(cr, t, A("p12", "save"), 530, 400, "SAVE MYSELF", col=RED, size=44, rot=0.05)
    vignette(cr, 0.3)


SCENES = {"window": scene_window, "deal": scene_deal, "think": scene_think, "split": scene_split,
          "both": scene_both, "shops": scene_shops, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("2 FRIENDS.", False), ("1 BROKEN WINDOW", True)], end=tl.at("p2"), y=170, size=96)
    captions(cr, t, tl)
