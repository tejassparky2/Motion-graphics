"""Low-poly channel, episode 30: "I Made Claude My JARVIS".

Script: channels/lowpoly/scripts/batch8_big_asks_eps28-31.md (owner approved, 23 Oct 2026). Reference 10's form.
Nothing real to claim: a fan fantasy (Iron Man's AI butler). Fiction; parody, not affiliated with Anthropic or Marvel.

    python channels/lowpoly/make_skit.py ep30_jarvis
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, mono, plain_caption, screen_insert, skit_voice   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc, seg   # noqa: E402
from motion.polish import rrect, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep30"
MUSIC = "score"
SCORE = [(0, "out"), ("j19", "tender"), ("j21", "end", 0.9)]
TAIL = 0.7
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep30_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart")})
skit_voice(voice, rate=3.4, tempo_min=0.8)

DEV, CL = None, "claude"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("j1", "devmid", DEV, "Claude. From today, you're my [Jarvis.|JARVIS.]", 0, 1),
    ("j2", "soloclose", CL, "Good evening, sir.", .6, .95),
    ("j3", "devmid", DEV, "Yes! Open the curtains.", .5, 1),
    ("j4", "soloclose", CL, "I'm a chat window, sir.", .5, 1),
    ("j5", "devclose", DEV, "Then make me a suit.", .7, 1),
    ("j6", "solo", CL, "Done.", .5, 1),
    ("j7", "ots", DEV, "That's a hoodie.", 1.0, 1),
    ("j8", "soloclose", CL, "It's the Mark One, sir.", .5, 1),
    ("j9", "devmid", DEV, "Scan the room for threats.", .8, 1),
    ("j10", "solo", CL, "One threat found.", .6, 1),
    ("j11", "devclose", DEV, "Where?", .4, 1),
    ("j12", "soloclose", CL, "The kitchen sink.", .5, 1),
    ("j13", "devclose", DEV, "[Jarvis|JARVIS] never talks about dishes.", 1.0, 1),
    ("j14", "soloclose", CL, "Tony Stark has robots for dishes.", .5, 1),
    ("j15", "devclose", DEV, "Fine. Run a scan on me.", 1.0, 1),
    ("j16", "ots", CL, "Last meal, noon. Sleep, four hours. Water, none.", .7, .95),
    ("j17", "devclose", DEV, "That's bad.", 1.0, .95),
    ("j18", "devclose", DEV, "What would [Jarvis|JARVIS] say?", .8, .95),
    ("j19", "soloclose", CL, "Eat something. Then save the world.", 1.2, .95),
    ("j20", "devclose", DEV, "Order a pizza. [chuckle]", 1.3, 1),
    ("j21", "soloclose", CL, "I'm a chat window, sir.", .5, 1),
]
HOLDS = {}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="I Made Claude My JARVIS",
    alt_titles=["\"I'm a Chat Window, Sir.\"", "When Your AI Isn't JARVIS"],
    description="""He wants Iron Man's JARVIS. He gets Claude.
The suit is a hoodie. The only threat is the sink. And the last scan is on him.

This story is fiction.

Ep. 30 of Dev vs the bots. Parody. Not affiliated with Anthropic or Marvel.

💬 Would you want an AI that tells you to eat, or one that just obeys? 👇""",
    hashtags=["#JARVIS", "#ClaudeAI", "#ProgrammerHumor"],
    tags=["jarvis", "iron man", "claude", "ai assistant", "programmer humor", "coding memes", "tony stark",
          "self care", "developer life", "funny ai"],
    pinned_comment="An AI that tells you to eat, or one that just obeys? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a3d"))
WHITE = (1, 1, 1)


def _cart(cr, x, y, w, h, t, k):
    mono(cr, "Cart (1)", x + 30, y + 60, 26, GREY, k)
    rrect(cr, x + 30, y + 100, 220, 260, 18)
    cr.set_source_rgb(0.55, 0.57, 0.62)
    cr.fill()
    rrect(cr, x + 85, y + 100, 110, 50, 20)     # the hood
    cr.set_source_rgb(0.45, 0.47, 0.52)
    cr.fill()
    mono(cr, "Grey hoodie", x + 280, y + 170, 34, WHITE, k)
    mono(cr, "$19", x + 280, y + 225, 40, GREEN, k)
    mono(cr, "Model: Mark One", x + 280, y + 280, 24, ORANGE, k)
    rrect(cr, x + 30, y + h - 120, w - 60, 80, 16)
    cr.set_source_rgb(1, 0.6, 0.24)
    cr.fill()
    mono(cr, "Buy now", x + w / 2 - 70, y + h - 68, 30, (0.1, 0.07, 0.05), k)


def _threat(cr, x, y, w, h, t, k):
    mono(cr, "Room scan", x + 30, y + 60, 26, GREY, k)
    mono(cr, "1 threat found", x + 30, y + 130, 38, RED, k)
    mono(cr, "Location:  sink", x + 30, y + 210, 30, WHITE, k)
    mono(cr, "Dishes:    14 days", x + 30, y + 265, 30, WHITE, k)
    mono(cr, "Smell:     yes", x + 30, y + 320, 30, YEL, k)


def _scan(rise):
    def paint(cr, x, y, w, h, t, k):
        mono(cr, "Scan: Dev", x + 30, y + 60, 26, GREY, k)
        rows = [("Last meal", "noon", .25), ("Sleep", "4 h", .3), ("Water", "none", .04)]
        for i, (lab, val, f) in enumerate(rows):
            at = rise + 0.9 * i
            if t < at:
                break
            yy = y + 140 + 115 * i
            mono(cr, lab, x + 30, yy, 30, WHITE, k)
            mono(cr, val, x + w - 160, yy, 30, RED, k)
            rrect(cr, x + 30, yy + 22, w - 60, 26, 10)
            cr.set_source_rgba(1, 1, 1, 0.1)
            cr.fill()
            rrect(cr, x + 30, yy + 22, max(10, (w - 60) * f * seg(t, at, at + 0.4)), 26, 10)
            cr.set_source_rgb(*RED[:3])
            cr.fill()
    return paint


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    screen_insert(cr, t, B["j6"].end + 0.3, B["j7"].end + 0.4, "shop", "11:20 PM", _cart)
    screen_insert(cr, t, B["j12"].end + 0.2, B["j13"].start + 1.3, "jarvis_mode", "11:31 PM", _threat)
    screen_insert(cr, t, B["j16"].start, B["j16"].end + 0.4, "jarvis_mode", "2:10 AM", _scan(B["j16"].start + 0.2))
    cue("pop", t, B["j6"].end + 0.3)
    cue("ding", t, B["j12"].end + 0.2)
    cue("typing", t, B["j16"].start, 1.0)
    cue("sigh", t, B["j17"].start - 0.6)
    plain_caption(cr, t, tl)
