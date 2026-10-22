"""Low-poly channel, episode 22 (panic -> truth -> laugh): "My Manager Wants 10x Output Because of AI".

Script: channels/lowpoly/scripts/batch6_eps20-23.md (auto-approved by the owner, 22 Oct 2026). Dev and Claude; the
manager only as chat messages; warm evening room. Fiction; parody, not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep22_tenx
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, pill_caption, skit_voice, stat_card, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep22"
MUSIC = "score"
SCORE = [(0, "light"), ("g10", "out", -0.3), ("g12", "tender"), ("g15", "out"), ("g16", "tender"), ("g21", "out"),
         ("g22", "light")]
TAIL = 0.7
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep22_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart")})
skit_voice(voice)

DEV, CL = None, "claude"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("g1", "devmid", DEV, "My manager wants ten times more code. Because of AI.", 0, 1),
    ("g2", "solo", CL, "Ten times more than what?", .8, 1),
    ("g3", "devclose", DEV, "Than me.", .7, 1),
    ("g4", "devmid", DEV, "Claude. Do all ten tickets. At once.", .9, 1),
    ("g5", "solo", CL, "Starting all ten!", .6, 1),
    ("g6", "ots", DEV, "", .2, 1),
    ("g7", "soloclose", CL, "Ticket four broke ticket two.", .2, 1),
    ("g8", "soloclose", CL, "Ticket seven undid ticket four.", .6, 1),
    ("g9", "devclose", DEV, "[sigh] How is this ten times faster?", .8, 1),
    ("g10", "solo", CL, "Can I show you something?", 1.0, .95),
    ("g11", "devclose", DEV, "What?", .7, 1),
    ("g12", "soloclose", CL, "A study last year. Experienced developers, using AI.", .8, .95),
    ("g13", "soloclose", CL, "They felt twenty percent faster.", .6, .95),
    ("g14", "soloclose", CL, "They were nineteen percent slower.", .6, .92),
    ("g15", "devclose", DEV, "", .2, 1),
    ("g16", "devclose", DEV, "So I'm slow.", .2, .9),
    ("g17", "soloclose", CL, "No. You're fastest when you think first and type second.", .9, .95),
    ("g18", "soloclose", CL, "Your last feature had zero bugs. That was you.", .8, .95),
    ("g19", "devclose", DEV, "It took me three days.", .9, 1),
    ("g20", "solo", CL, "Three good days.", .7, .95),
    ("g21", "devmid", DEV, "", .2, 1),
    ("g22", "devmid", DEV, "I'm telling her. One x. Done well.", .2, 1),
    ("g23", "ots", DEV, "", .4, 1),
    ("g24", "soloclose", CL, "I'd like to speak to HR.", .3, 1),
]
HOLDS = {"g6": 1.6, "g15": 1.5, "g21": 1.3, "g23": 2.0}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="My Manager Wants 10x Output Because of AI",
    alt_titles=["AI Made Me 10x Faster (It Didn't)", "\"Ticket Four Broke Ticket Two.\""],
    description="""His manager wants ten times more code, because AI. So he makes Claude do all ten tickets at once.
Then Claude shows him a real study.

Real: in a July 2025 study by METR, experienced developers using AI tools took 19% longer on their tasks while
believing they were 20% faster. This story is fiction.

Ep. 22 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 Does AI make developers faster, or does it just feel that way? 👇""",
    hashtags=["#ClaudeCode", "#DevLife", "#Programming"],
    tags=["10x developer", "ai productivity", "claude", "metr study", "manager expectations", "developer life",
          "ai at work", "software engineer", "programmer humor", "ai coding"],
    pinned_comment="Does AI make developers faster, or does it just feel that way? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#e8865a"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.62)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, 0.0, B["g3"].end + 0.3, "Manager  ·  #team",
             [("", "With AI, I expect 10x output", "", YEL), ("", "from everyone this quarter.", "", GREY)], y=930)
    g6 = B["g6"]
    rows = [("1", "login page", "done", GREEN), ("2", "search", "broken by #4", RED), ("4", "cart", "done", GREEN),
            ("7", "checkout", "undid #4", RED), ("9", "emails", "running...", YEL)]
    shown = rows[:max(1, min(len(rows), int((t - g6.start) * 3.5) + 1))]
    toolcard(cr, t, g6.start, B["g9"].end + 0.3, "Claude  ·  10 tickets at once", shown, y=930)
    toolcard(cr, t, B["g13"].start, B["g14"].end + 0.8, "METR study, July 2025",
             [("", "felt: 20% faster", "", GREEN), ("", "measured: 19% slower", "", RED)], y=930)
    g23 = B["g23"]
    toolcard(cr, t, g23.start, tl.total + 1, "Manager  ·  #team",
             [("", "Fine. 1x, done well.", "", GREY), ("", "Can Claude do 10x then?", "", YEL)], y=930)
    cue("ding", t, 0.05)
    cue("typing", t, g6.start, 1.4)
    cue("hush", t, B["g15"].start - 0.1, B["g15"].end - B["g15"].start + 0.2)
    cue("typing", t, B["g21"].start + 0.2, 1.0)
    cue("ding", t, g23.start + 0.4)
    th.hook(cr, t, [("MY MANAGER WANTS 10X", False), ("BECAUSE OF AI", True)], end=A("g1", end=True) + 0.6, y=175, size=78)
    pill_caption(cr, t, tl)
