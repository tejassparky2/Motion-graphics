"""Low-poly channel, episode 37: AI news explainer, "Why Does Claude Look So Proud? (Anthropic Stopped Using Git)".

Script: channels/lowpoly/scripts/batch10_ai_news_eps36-39.md (auto-approved by the owner, 24 Oct 2026). Reference form
(news explainer; its opener is not reused). Real: anthropic.com/engineering/redesigning-source-control (13 Oct 2026, updated 15
Oct). Parody characters; not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep37_scion
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import bignum, build_script, frames, headline, skit_voice   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep37"
MUSIC = "score"
SCORE = [(0, "light"), ("s18", "tender"), ("s19", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep37_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart")})
skit_voice(voice)

DEV, CL = None, "claude"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("s1", "devmid", DEV, "Why do you look so proud?", 0, 1),
    ("s2", "soloclose", CL, "My company stopped using git.", .3, 1),
    ("s3", "devclose", DEV, "Wait, what? Everyone uses git.", .3, 1),
    ("s4", "soloclose", CL, "Not in our main repo. Not anymore.", .3, 1),
    ("s5", "devclose", DEV, "Why would they stop?", .3, 1),
    ("s6", "solo", CL, "Because of agents like me. In May, we merged about [twenty-five hundred|2,500] changes a day.", .3, 1),
    ("s7", "soloclose", CL, "By September, over [thirty thousand.|30,000.]", .25, 1),
    ("s8", "devclose", DEV, "[Thirty thousand|30,000] a day?", .3, 1),
    ("s9", "solo", CL, "And [twenty-five million|25 million] code checkouts a day, just for testing.", .3, 1),
    ("s10", "devclose", DEV, "Does git break?", .3, 1),
    ("s11", "soloclose", CL, "Done the normal way, that's over [six hundred|600] petabytes a day.", .3, 1),
    ("s12", "devmid", DEV, "So what did they build?", .35, 1),
    ("s13", "solo", CL, "Scion. Their own version control. Two hundred times lighter than the old git mirrors.", .3, 1),
    ("s14", "devclose", DEV, "How many people built that?", .3, 1),
    ("s15", "soloclose", CL, "Seven. In five months.", .3, 1),
    ("s16", "devclose", DEV, "Should I delete git?", .4, 1),
    ("s17", "soloclose", CL, "No. They say it only makes sense for giant repos.", .3, 1),
    ("s18", "devclose", DEV, "So the slow part isn't writing code anymore.", .5, .95),
    ("s19", "soloclose", CL, "No. It's the tools built for humans.", .4, .95),
]
HOLDS = {}
GAP_FIX = {"s11": 0.294}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="Anthropic Stopped Using Git. Here's Why.",
    alt_titles=["Git Couldn't Keep Up With AI Agents", "30,000 Changes a Day Broke Git"],
    description="""AI agents now write code so fast that git couldn't keep up. Claude explains why Anthropic built its
own version control, Scion.

Real (anthropic.com/engineering, 13 Oct 2026): merged changes went from about 2,500 a day in May 2026 to over 30,000 a
day by September; about 25 million CI checkouts a day; fetching that the normal way would be "over 600 PB of git
traffic per day"; Scion uses 200x less CPU and memory than the old git mirrors; seven people built it and moved the repo
in five months. Anthropic says Scion "is by no means a suitable replacement for git for general use". Dev and Claude
are parody characters.

Ep. 37 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 Is your team's slowest part the code now, or the tools around it? 👇""",
    hashtags=["#Git", "#ClaudeAI", "#AINews"],
    tags=["anthropic scion", "anthropic git", "version control", "monorepo", "ai agents", "claude", "ai news",
          "developer tools", "programmer humor", "tech news"],
    pinned_comment="Is your team's slowest part the code now, or the tools around it? 👇 Subscribe for tomorrow's AI news.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a3d"))
WHITE = (1, 1, 1)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    B = tl.by_id
    headline(cr, t, B["s2"].start + 0.2, B["s3"].end + 0.2, "anthropic.com/engineering", "Redesigning source control for agents",
             [("Oct 13, 2026", GREY), ("main repo: off git", ORANGE)])
    bignum(cr, t, B["s6"].start + 1.4, B["s6"].end + 0.2, "merged changes per day", 2500, "May 2026", col=GREY)
    bignum(cr, t, B["s7"].start, B["s8"].end + 0.2, "merged changes per day", "30,000+", "September 2026", col=ORANGE, count=False)
    bignum(cr, t, B["s9"].start + 0.3, B["s9"].end + 0.2, "CI", 25000000, "code checkouts a day", col=YEL)
    bignum(cr, t, B["s11"].start + 0.3, B["s11"].end + 0.2, "the normal git way", "600 PB", "of traffic a day", col=RED)
    bignum(cr, t, B["s13"].start + 0.4, B["s13"].end + 0.2, "Scion", "200x", "less CPU and memory", sub="than the old git mirrors", col=GREEN)
    headline(cr, t, B["s17"].start, B["s17"].end + 0.2, "anthropic.com/engineering", "\"Scion is by no means a suitable replacement for git for general use.\"",
             [("only for giant monorepos", GREY)])
    cue("ding", t, B["s2"].start + 0.2)
    th.captions(cr, t, tl, y=400, size=60)
