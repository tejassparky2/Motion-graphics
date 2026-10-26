"""Low-poly channel, episode 40: "With AI, I'm Twice as Fast" (short comedy).

Script: channels/lowpoly/scripts/batch11_eps40-43.md (auto-approved by the owner, 26 Oct 2026). Short format (the
highest % viewed in the first analytics). Real: METR, 10 Jul 2025: experienced developers took 19% longer with AI and
still believed it had sped them up by 20%. Fiction; parody, not affiliated with OpenAI.

    python channels/lowpoly/make_skit.py ep40_faster
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_caption, build_script, frames, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep40"
MUSIC = "score"
SCORE = [(0, "light"), ("v12", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep40_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})
skit_voice(voice)

DEV, CX = None, "codex"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("v1", "devmid", DEV, "Done. With you, I'm twice as fast. [chuckle]", 0, 1),
    ("v2", "cxclose", CX, "A study timed experienced developers.", .35, 1),
    ("v3", "devclose", DEV, "And?", .3, 1),
    ("v4", "cxclose", CX, "With AI, they took nineteen percent longer.", .3, 1),
    ("v5", "devclose", DEV, "Longer?", .35, 1),
    ("v6", "cx", CX, "They still believed they were twenty percent faster.", .3, 1),
    ("v7", "devclose", DEV, "So I'm fast. In my heart.", .45, 1),
    ("v8", "cxclose", CX, "You started this at nine.", .35, 1),
    ("v9", "devclose", DEV, "And?", .3, 1),
    ("v10", "cxclose", CX, "It's four forty.", .35, 1),
    ("v11", "devclose", DEV, "Twice as fast, though.", .6, .95),
    ("v12", "cxclose", CX, "In your heart.", .45, 1),
]
HOLDS = {}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="With AI, I'm Twice as Fast",
    alt_titles=["\"So I'm Fast. In My Heart.\"", "Does AI Really Make You Faster?"],
    description="""Dev is sure AI makes him twice as fast. Codex has the study. And the clock.

Real: in a 2025 study by METR, 16 experienced open-source developers took 19% longer on real issues when they were
allowed to use AI tools, and afterwards still believed AI had sped them up by 20% (METR says newer data from 2026
exists). Dev's day is fiction.

Ep. 40 of Dev vs the bots. Parody. Not affiliated with OpenAI.

💬 Be honest: does AI make you faster, or does it just feel that way? 👇""",
    hashtags=["#Codex", "#ProgrammerHumor", "#AI"],
    tags=["ai productivity", "metr study", "ai makes developers slower", "codex", "programmer humor", "coding memes",
          "developer life", "ai coding", "funny ai", "software engineering"],
    pinned_comment="Does AI make you faster, or does it just feel that way? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f"))
WHITE = (1, 1, 1)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    B = tl.by_id
    toolcard(cr, t, B["v4"].start + 0.2, B["v6"].end + 0.3, "METR study  ·  2025",
             [("", "with AI: 19% longer", "", RED), ("", "felt: 20% faster", "", GREEN)], y=1085)
    toolcard(cr, t, B["v8"].start, B["v10"].end + 0.3, "task: \"quick fix\"",
             [("", "started   9:00 AM", "", WHITE), ("", "now       4:40 PM", "", YEL)], y=1085)
    cue("ding", t, B["v4"].start + 0.2)
    build_caption(cr, t, tl)
