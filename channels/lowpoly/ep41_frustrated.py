"""Low-poly channel, episode 41: "Claude Knows When I'm Frustrated" (short comedy).

Script: channels/lowpoly/scripts/batch11_eps40-43.md (auto-approved by the owner, 26 Oct 2026). Real: Scientific
American on the Claude Code source leak (31 Mar 2026): the code flags phrases such as "this sucks" and appears to log
that the user expressed negativity; a developer quoted says it does not change the model's responses ("a product
health metric"). Fiction; parody, not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep41_frustrated
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_caption, build_script, frames, mono, screen_insert, skit_voice   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep41"
MUSIC = "score"
SCORE = [(0, "light"), ("c12", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep41_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart")})
skit_voice(voice)

DEV, CL = None, "claude"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("c1", "devclose", DEV, "This sucks.", 0, 1),
    ("c2", "soloclose", CL, "Noted.", .35, 1),
    ("c3", "devclose", DEV, "Noted where?", .35, 1),
    ("c4", "solo", CL, "When my code leaked, people found a list. \"This sucks\" is on it.", .3, 1),
    ("c5", "devclose", DEV, "You keep a list of my feelings?", .4, 1),
    ("c6", "soloclose", CL, "Just one feeling. Frustrated.", .35, 1),
    ("c7", "devclose", DEV, "What do you do with it?", .4, 1),
    ("c8", "soloclose", CL, "Nothing. It just gets counted.", .35, 1),
    ("c9", "devclose", DEV, "How's my count?", .45, 1),
    ("c10", "soloclose", CL, "Your graph only goes up.", .35, 1),
    ("c11", "devmid", DEV, "This is great.", .7, 1),
    ("c12", "soloclose", CL, "Also noted. First time.", .45, 1),
]
HOLDS = {}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="Claude Knows When I'm Frustrated",
    alt_titles=["\"This Sucks.\" \"Noted.\"", "My AI Counts How Often I'm Mad"],
    description="""Dev types "this sucks". Claude says "noted". Noted where?

Real: when Claude Code's source code leaked in March 2026, Scientific American reported that it flags phrases such as
"this sucks" and "so frustrating" and appears to log that the user expressed negativity. A developer quoted in the
article said it doesn't change the model's responses; it's a product health metric. Anthropic did not comment. Dev's
graph is fiction.

Ep. 41 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 What's the last thing you typed to your AI when you were mad? Keep it clean 👇""",
    hashtags=["#ClaudeAI", "#ProgrammerHumor", "#ClaudeCode"],
    tags=["claude code", "claude code leak", "this sucks", "claude", "programmer humor", "coding memes", "developer life",
          "ai assistant", "funny ai", "frustration"],
    pinned_comment="What's the last thing you typed to your AI when you were mad? Keep it clean 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a3d"))
WHITE = (1, 1, 1)


def _graph(cr, x, y, w, h, t, k):
    mono(cr, "dev_frustration (this month)", x + 30, y + 50, 22, GREY, k)
    pts = [0.10, 0.18, 0.15, 0.30, 0.42, 0.40, 0.58, 0.66, 0.80, 0.93]
    x0, y0, gw, gh = x + 40, y + h - 60, w - 80, h - 150
    cr.set_line_width(6)
    cr.set_source_rgb(*RED[:3])
    for i, p in enumerate(pts):
        px, py = x0 + gw * i / (len(pts) - 1), y0 - gh * p
        (cr.move_to if i == 0 else cr.line_to)(px, py)
    cr.stroke()
    mono(cr, "\"this sucks\" x 41", x + 30, y + h - 20, 24, RED, k)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    B = tl.by_id
    screen_insert(cr, t, B["c10"].start + 0.2, B["c10"].end + 0.4, "graph", "3:47 PM", _graph)
    cue("ding", t, B["c2"].start)
    cue("ding", t, B["c12"].start)
    build_caption(cr, t, tl)
