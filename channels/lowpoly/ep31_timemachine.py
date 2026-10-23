"""Low-poly channel, episode 31: "I Asked Codex for a Time Machine".

Script: channels/lowpoly/scripts/batch8_big_asks_eps28-31.md (owner approved, 23 Oct 2026). Reference 10's form.
Real: "don't deploy on Fridays" is a long-running developer rule; `git revert` undoes a pushed commit with a new
commit (git docs). Fiction; parody, not affiliated with OpenAI.

    python channels/lowpoly/make_skit.py ep31_timemachine
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, mono, plain_caption, screen_insert, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc, seg   # noqa: E402
from motion.polish import rrect, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep31"
MUSIC = "score"
SCORE = [(0, "out"), ("m16", "tender"), ("m21", "end", 0.9)]
TAIL = 0.7
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep31_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})
skit_voice(voice)

DEV, CX = None, "codex"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("m1", "devmid", DEV, "Codex. Build me a time machine.", 0, 1),
    ("m2", "cxclose", CX, "Why?", .5, 1),
    ("m3", "devclose", DEV, "I pushed to main. On a Friday.", .6, 1),
    ("m4", "cxclose", CX, "That's called git revert.", .5, 1),
    ("m5", "devclose", DEV, "Further back.", .6, 1),
    ("m6", "cxclose", CX, "How far?", .4, 1),
    ("m7", "devmid", DEV, "[Twenty nineteen.|2019.] Before I learned JavaScript.", .6, 1),
    ("m8", "cx", CX, "Building.", .6, 1),
    ("m9", "cxclose", CX, "Problem.", 1.6, 1),
    ("m10", "devclose", DEV, "What?", .4, 1),
    ("m11", "cxclose", CX, "It needs a lot of power.", .4, 1),
    ("m12", "devclose", DEV, "How much?", .5, 1),
    ("m13", "cxclose", CX, "Your laptop is at eleven percent.", .4, 1),
    ("m14", "cx", CX, "Why [twenty nineteen?|2019?]", 1.2, .95),
    ("m15", "devclose", DEV, "I used to sleep in [twenty nineteen.|2019.]", 1.0, .95),
    ("m16", "cxclose", CX, "If you go back, you never learn to code.", 1.2, .95),
    ("m17", "cxclose", CX, "Then we never meet.", .9, .95),
    ("m17h", "devclose", DEV, "", .3, 1),
    ("m18", "devclose", DEV, "Revert to Thursday.", .2, 1),
    ("m19", "cx", CX, "Reverting.", .5, 1),
    ("m20", "devclose", DEV, "Now revert JavaScript.", 1.0, 1),
    ("m21", "endside", CX, "Nobody can do that.", .6, 1),
]
HOLDS = {"m17h": 1.4}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="I Asked Codex for a Time Machine",
    alt_titles=["I Pushed to Main on a Friday", "\"That's Called Git Revert.\""],
    description="""He pushed to main. On a Friday. Now he wants a time machine.
Not to yesterday. To 2019. Before he learned JavaScript.

Real: "don't deploy on Fridays" is an old developer rule, and `git revert` undoes a pushed commit by adding a new
one. This story is fiction.

Ep. 31 of Dev vs the bots. Parody. Not affiliated with OpenAI.

💬 One trip back in time: what would you undo? 👇""",
    hashtags=["#Codex", "#ProgrammerHumor", "#Git"],
    tags=["time machine", "git revert", "push to main", "friday deploy", "codex", "programmer humor", "coding memes",
          "javascript", "developer life", "funny ai"],
    pinned_comment="One trip back in time: what would you undo? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a3d"))
WHITE = (1, 1, 1)


def _build(start):
    def paint(cr, x, y, w, h, t, k):
        mono(cr, "$ codex build time_machine", x + 30, y + 60, 24, GREY, k)
        mono(cr, "Target:  2019", x + 30, y + 140, 32, WHITE, k)
        mono(cr, "Reason:  JavaScript", x + 30, y + 195, 32, YEL, k)
        u = min(0.97, seg(t, start, start + 1.6) ** 0.6)
        rrect(cr, x + 30, y + 260, w - 60, 34, 12)
        cr.set_source_rgba(1, 1, 1, 0.1)
        cr.fill()
        rrect(cr, x + 30, y + 260, max(12, (w - 60) * u), 34, 12)
        cr.set_source_rgb(*ORANGE)
        cr.fill()
        mono(cr, f"{int(u * 100)}%", x + 30, y + 345, 30, WHITE, k)
        if u >= 0.97:
            mono(cr, "Power needed: 1.21 GW", x + 30, y + 410, 28, RED, k)
    return paint


def _revert(cr, x, y, w, h, t, k):
    mono(cr, "$ git revert a3f9c1", x + 30, y + 60, 26, GREY, k)
    mono(cr, "✓ Reverted \"friday fix\"", x + 30, y + 140, 32, GREEN, k)
    mono(cr, "✓ Production is back up", x + 30, y + 200, 32, GREEN, k)
    mono(cr, "Time travel: not needed", x + 30, y + 280, 28, GREY, k)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, B["m3"].start + 0.3, B["m4"].end + 0.3, "ALERT  ·  Friday 5:02 PM",
             [("!", "Checkout is down", "", RED), ("", "last push: you", "", GREY)], y=1085)
    screen_insert(cr, t, B["m8"].end + 0.2, B["m9"].start - 0.05, "time_machine", "5:09 PM", _build(B["m8"].end + 0.3))
    toolcard(cr, t, B["m13"].start + 0.3, B["m13"].end + 0.6, "battery", [("", "11%", "", RED)], y=1085)
    screen_insert(cr, t, B["m19"].end + 0.2, B["m20"].start - 0.05, "terminal", "5:31 PM", _revert)
    cue("buzz", t, B["m3"].start + 0.3, 0.6)
    cue("typing", t, B["m8"].end + 0.2, 1.2)
    cue("ding", t, B["m19"].end + 0.3)
    plain_caption(cr, t, tl)
