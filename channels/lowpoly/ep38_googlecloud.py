"""Low-poly channel, episode 38: AI news explainer, "Hey Codex, What's New? (OpenAI Moves Into Google Cloud)".

Script: channels/lowpoly/scripts/batch10_ai_news_eps36-39.md (auto-approved by the owner, 24 Oct 2026). Reference form.
Real: cloud.google.com blog (21 Oct 2026: OpenAI models in private preview; Codex CLI/Desktop can connect); claude.com
(22 Oct 2026: Claude Models on Google Cloud, Anthropic managed, generally available). Parody characters; not affiliated
with OpenAI, Google or Anthropic.

    python channels/lowpoly/make_skit.py ep38_googlecloud
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import bignum, build_script, frames, headline, skit_voice   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep38"
MUSIC = "score"
SCORE = [(0, "light"), ("g17", "tender"), ("g18", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep38_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})
skit_voice(voice)

DEV, CX = None, "codex"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("g1", "devmid", DEV, "Hey Codex. What's new with you?", 0, 1),
    ("g2", "cxclose", CX, "I'm moving in with Google.", .3, 1),
    ("g3", "devclose", DEV, "Wait, what?", .3, 1),
    ("g4", "cx", CX, "On [October twenty-first,|Oct 21,] Google Cloud started offering [Open A I's|OpenAI's] models.", .3, 1),
    ("g5", "devclose", DEV, "[Open A I?|OpenAI?] On Google?", .3, 1),
    ("g6", "cxclose", CX, "[G P T six|GPT-6] Astra, [G P T six point one|GPT-6.1] Sol, and [G P T six|GPT-6] Luna. In private preview, for some big companies.", .3, 1),
    ("g7", "devclose", DEV, "And you?", .3, 1),
    ("g8", "cxclose", CX, "Codex can connect to it from day one.", .3, 1),
    ("g9", "devclose", DEV, "And Claude?", .3, 1),
    ("g10", "cx", CX, "One day later, Claude's full platform went live there too.", .3, 1),
    ("g11", "devmid", DEV, "So Google sells its rivals?", .35, 1),
    ("g12", "cxclose", CX, "Google says it's the only big cloud with all three. Gemini, Claude, and [G P T.|GPT.]", .3, 1),
    ("g13", "devclose", DEV, "Why would companies want that?", .3, 1),
    ("g14", "cx", CX, "One bill. And it counts toward what they already promised to spend on Google.", .3, 1),
    ("g15", "devclose", DEV, "And for developers?", .3, 1),
    ("g16", "cxclose", CX, "Switching models gets easier. Same account.", .3, 1),
    ("g17", "devclose", DEV, "Rivals in one shop.", .5, .95),
    ("g18", "cxclose", CX, "Like a food court. For AI.", .4, 1),
]
HOLDS = {}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="OpenAI's Models Are Now on Google Cloud",
    alt_titles=["Hey Codex, What's New? (GPT on Google Cloud)", "Google Now Sells Gemini, Claude AND GPT"],
    description="""OpenAI's models just showed up on Google Cloud, and Claude's full platform followed a day later.
Codex explains what it means.

Real: on 21 Oct 2026 Google Cloud announced GPT-6 Astra, GPT-6.1 Sol and GPT-6 Luna in private preview for select
enterprise customers, with Codex CLI and Desktop able to connect, billed on one Google Cloud invoice that counts toward
existing commitments (cloud.google.com). Google says it is "the only hyperscale cloud provider offering access to all
three leading closed source LLMs". On 22 Oct, Claude Models on Google Cloud (Anthropic managed) became generally
available (claude.com). Dev and Codex are parody characters.

Ep. 38 of Dev vs the bots. Parody. Not affiliated with OpenAI, Google or Anthropic.

💬 One cloud with every model: good for developers, or too much power in one place? 👇""",
    hashtags=["#GoogleCloud", "#OpenAI", "#AINews"],
    tags=["openai google cloud", "gpt-6 google cloud", "claude google cloud", "gemini", "codex", "ai news",
          "cloud computing", "llm", "programmer humor", "tech news"],
    pinned_comment="One cloud with every model: good for developers, or too much power in one place? 👇 Subscribe for tomorrow's AI news.",
)
GREEN, RED, GREY, YEL, BLUE, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#4d8dff", "#ff9a3d"))
WHITE = (1, 1, 1)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    B = tl.by_id
    headline(cr, t, B["g4"].start + 0.3, B["g5"].end + 0.2, "cloud.google.com  ·  Oct 21", "Google Cloud brings OpenAI models to customers",
             [("private preview", YEL), ("Codex CLI + Desktop can connect", WHITE)])
    headline(cr, t, B["g6"].start + 0.3, B["g6"].end + 0.2, "models", "Coming to Google Cloud",
             [("GPT-6 Astra", WHITE), ("GPT-6.1 Sol", WHITE), ("GPT-6 Luna", WHITE), ("select enterprise customers first", GREY)])
    headline(cr, t, B["g10"].start + 0.3, B["g10"].end + 0.2, "claude.com  ·  Oct 22", "Claude on Google Cloud (Anthropic managed) is generally available",
             [("Fable 5.1 · Opus 5.5", ORANGE), ("Sonnet 5.5 · Haiku 5.5", ORANGE)])
    bignum(cr, t, B["g12"].start + 0.3, B["g12"].end + 0.2, "Google's claim", "3", "big model families, one cloud",
           sub="Gemini · Claude · GPT", col=BLUE, count=False)
    headline(cr, t, B["g14"].start + 0.3, B["g14"].end + 0.2, "for companies", "One Google Cloud invoice",
             [("counts toward existing commitments", GREEN)])
    cue("ding", t, B["g4"].start + 0.3)
    th.captions(cr, t, tl, y=400, size=60)
