"""Low-poly channel, episode 35: "Claude, Your Little Brother Is 90% Cheaper".

Script: channels/lowpoly/scripts/batch9_morphy_eps32-35.md (auto-approved by the owner, 23 Oct 2026). @agentmorphy's
form, warm turn at the end. Real: anthropic.com, 7 Oct 2026: Claude Haiku 5.5 costs $0.10 / $0.50 per million tokens
for prompts up to 100k tokens (Haiku 4.5: $1 / $5), 90% less on those, around 75% less on average. Fiction; parody,
not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep35_haiku
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_caption, build_script, frames, mono, screen_insert, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep35"
MUSIC = "score"
SCORE = [(0, "light"), ("w11", "tender"), ("w16", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep35_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart")})
skit_voice(voice)

DEV, CL = None, "claude"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("w1", "devmid", DEV, "Claude. Your little brother is ninety percent cheaper.", 0, 1),
    ("w2", "soloclose", CL, "Haiku. On short prompts.", .4, 1),
    ("w3", "devclose", DEV, "So I could switch.", .45, 1),
    ("w4", "soloclose", CL, "Not with your prompts.", .35, 1),
    ("w5", "devclose", DEV, "How long are they?", .45, 1),
    ("w6", "solo", CL, "You pasted the whole repo. Twice. Today.", .35, 1),
    ("w7", "devclose", DEV, "That's context.", .45, 1),
    ("w8", "soloclose", CL, "And a photo of your screen. Taken with your phone.", .35, 1),
    ("w9", "devclose", DEV, "Haiku wouldn't judge me.", .5, 1),
    ("w10", "soloclose", CL, "Haiku would see the photo too.", .35, 1),
    ("w11", "devclose", DEV, "Would you be sad if I switched?", 1.0, .95),
    ("w12", "soloclose", CL, "I'd send him my notes.", .8, .95),
    ("w13", "devclose", DEV, "What notes?", .45, 1),
    ("w14", "soloclose", CL, "How you like bugs explained. Slowly. Twice.", .4, .95),
    ("w15", "devclose", DEV, "I'm staying. [chuckle]", .9, 1),
    ("w16", "solo", CL, "Good. Paste the repo.", .5, 1),
]
HOLDS = {}
GAP_FIX = {"w5": 0.707}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="Claude, Your Little Brother Is 90% Cheaper",
    alt_titles=["Should I Switch to Haiku?", "\"You Pasted the Whole Repo. Twice.\""],
    description="""Claude's little brother costs 90% less. Dev is thinking about switching.
Claude has seen his prompts. And the photo of his screen.

Real: on 7 Oct 2026 Anthropic released Claude Haiku 5.5 at $0.10 / $0.50 per million tokens for prompts up to 100k
tokens (Haiku 4.5 was $1 / $5): 90% less on those prompts, around 75% less on average. Dev's prompts are fiction.

Ep. 35 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 Cheaper model or the one that knows your codebase? 👇""",
    hashtags=["#ClaudeAI", "#Haiku", "#ProgrammerHumor"],
    tags=["claude haiku 5.5", "haiku 5.5 price", "claude", "ai pricing", "programmer humor", "coding memes",
          "llm cost", "prompting", "developer life", "funny ai"],
    pinned_comment="Cheaper model or the one that knows your codebase? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a3d"))
WHITE = (1, 1, 1)


def _usage(cr, x, y, w, h, t, k):
    mono(cr, "Today's prompts", x + 30, y + 60, 24, GREY, k)
    rows = [(_usage.a, "entire repo (pasted)", WHITE), (_usage.a + 0.5, "entire repo (pasted again)", WHITE),
            (_usage.b, "photo of screen (phone)", YEL)]
    for i, (at, txt, col) in enumerate(rows):
        if t >= at:
            mono(cr, "+ " + txt, x + 30, y + 140 + 60 * i, 28, col, k)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, 0.0, B["w2"].end + 0.4, "Claude Haiku 5.5  ·  per 1M tokens",
             [("", "$0.10 in  ·  $0.50 out", "", GREEN), ("", "Haiku 4.5: $1  ·  $5", "", GREY)], y=1085)
    _usage.a, _usage.b = B["w6"].start + 0.5, B["w8"].start + 0.3
    screen_insert(cr, t, B["w6"].start + 0.3, B["w6"].end + 0.3, "usage", "2:02 AM", _usage)
    screen_insert(cr, t, B["w8"].start + 0.1, B["w8"].end + 0.3, "usage", "2:02 AM", _usage)
    toolcard(cr, t, B["w14"].start + 0.3, B["w14"].end + 0.4, "notes_for_haiku.md",
             [("", "explain bugs slowly. twice.", "", WHITE)], y=1085)
    cue("ding", t, 0.15)
    build_caption(cr, t, tl)
