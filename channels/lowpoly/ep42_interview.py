"""Low-poly channel, episode 42: "My Interview Is Tomorrow. No AI Allowed." (emotional skit).

Script: channels/lowpoly/scripts/batch11_eps40-43.md (auto-approved by the owner, 26 Oct 2026). Emotional, ~60 s (the
format that won the most subscribers in the first analytics). Real: Anthropic research, 29 Jan 2026: 52 mostly junior
engineers learning a new library; the AI group averaged 50% on a quiz against 67% for hand-coding; the biggest gap was
debugging; those who kept asking follow-up and conceptual questions still learned (correlational). Fiction; parody,
not affiliated with OpenAI.

    python channels/lowpoly/make_skit.py ep42_interview
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_caption, build_script, frames, mono, screen_insert, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep42"
MUSIC = "score"
SCORE = [(0, "light"), ("e5", "tender"), ("e15", "swell"), ("e20", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep42_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})
skit_voice(voice)

DEV, CX = None, "codex"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("e1", "devmid", DEV, "Tomorrow's interview. No AI allowed.", 0, 1),
    ("e2", "cxclose", CX, "Then let's practice.", .5, 1),
    ("e3", "devclose", DEV, "Write a function that reverses a list.", .5, 1),
    ("e4", "cxclose", CX, "No. You write it.", .5, 1),
    ("e5", "devclose", DEV, "I can't. I haven't written one alone in a year.", .9, .95),
    ("e6", "cxclose", CX, "You fixed a bug alone last week.", .8, .95),
    ("e7", "devclose", DEV, "You fixed it.", .5, 1),
    ("e8", "cxclose", CX, "You found it. I just typed.", .6, .95),
    ("e9", "devmid", DEV, "There was a study. People who used AI scored lower.", .8, 1),
    ("e10", "cx", CX, "Fifty percent, against sixty-seven. Worst at debugging.", .5, 1),
    ("e11", "devclose", DEV, "So I'm the fifty.", .7, .95),
    ("e12", "cxclose", CX, "The ones who kept asking why did better. You always ask why.", .8, .95),
    ("e13", "devclose", DEV, "Every time. [chuckle]", .5, 1),
    ("e14", "cxclose", CX, "Every single time.", .4, 1),
    ("e14h", "ots", DEV, "", .4, 1),
    ("e15", "devclose", DEV, "It works.", .3, .95),
    ("e16", "cxclose", CX, "You wrote that.", .6, .95),
    ("e17", "devclose", DEV, "Can I still talk to you after?", 1.0, .95),
    ("e18", "cxclose", CX, "After the interview.", .6, 1),
    ("e19", "devclose", DEV, "And if I get the job?", .6, 1),
    ("e20", "cxclose", CX, "Then you'll need me. They use AI there.", .5, 1),
]
HOLDS = {"e14h": 2.4}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="My Interview Is Tomorrow. No AI Allowed.",
    alt_titles=["\"I Haven't Written One Alone in a Year.\"", "Can I Still Code Without AI?"],
    description="""Tomorrow's coding interview bans AI. Dev hasn't written a function alone in a year. Codex won't write it
for him.

Real: in an Anthropic study published 29 Jan 2026, 52 mostly junior engineers learned a new library with or without an
AI assistant; the AI group averaged 50% on the quiz afterwards against 67% for those who coded by hand, with the
biggest gap on debugging. Those who used AI to keep asking questions and get explanations still learned. Dev's
interview is fiction.

Ep. 42 of Dev vs the bots. Parody. Not affiliated with OpenAI.

💬 Could you pass a coding interview tomorrow without AI? 👇""",
    hashtags=["#Codex", "#CodingInterview", "#AI"],
    tags=["coding interview", "no ai allowed", "can i code without ai", "codex", "learning to code", "programmer humor",
          "developer life", "ai skills", "junior developer", "software engineering"],
    pinned_comment="Could you pass a coding interview tomorrow without AI? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a3d"))
WHITE = (1, 1, 1)


def _code(cr, x, y, w, h, t, k):
    mono(cr, "practice.py", x + 30, y + 50, 22, GREY, k)
    lines = ["def reverse(items):", "    out = []", "    for x in items:", "        out.insert(0, x)", "    return out"]
    for i, line in enumerate(lines):
        if t >= _code.t0 + 0.35 * i:
            mono(cr, line, x + 30, y + 120 + 48 * i, 28, WHITE, k)
    if t >= _code.t0 + 2.0:
        mono(cr, "✓ reverse([1, 2, 3]) == [3, 2, 1]", x + 30, y + h - 60, 26, GREEN, k)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    B = tl.by_id
    toolcard(cr, t, 0.1, B["e2"].end + 0.3, "calendar  ·  tomorrow", [("", "10:00 AM  coding interview", "", WHITE),
             ("!", "no AI tools allowed", "", RED)], y=1085)
    toolcard(cr, t, B["e10"].start + 0.2, B["e11"].end + 0.3, "Anthropic study  ·  Jan 2026",
             [("", "with AI: 50% on the quiz", "", RED), ("", "by hand: 67%", "", GREEN), ("", "biggest gap: debugging", "", GREY)], y=1085)
    _code.t0 = B["e14h"].start + 0.1
    screen_insert(cr, t, B["e14h"].start, B["e15"].end + 0.3, "practice.py", "1:42 AM", _code)
    cue("typing", t, B["e14h"].start + 0.1, 1.8)
    cue("ding", t, B["e14h"].start + 2.1)
    build_caption(cr, t, tl)
