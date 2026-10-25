"""Low-poly channel, episode 39: AI news explainer, "Hey Claude, What's New? (An AI That Works While You Sleep)".

Script: channels/lowpoly/scripts/batch10_ai_news_eps36-39.md (auto-approved by the owner, 24 Oct 2026). Reference form.
Real: claude.com/resources/articles/claude-duet (21 Oct 2026, research preview). Parody characters; not affiliated with
Anthropic.

    python channels/lowpoly/make_skit.py ep39_duet
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import bignum, build_script, frames, headline, skit_voice   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep39"
MUSIC = "score"
SCORE = [(0, "light"), ("d17", "tender"), ("d18", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep39_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart")})
skit_voice(voice)

DEV, CL = None, "claude"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("d1", "devmid", DEV, "Hey Claude. What's new with you?", 0, 1),
    ("d2", "soloclose", CL, "I have a new app. It works while you sleep.", .3, 1),
    ("d3", "devclose", DEV, "Wait, what?", .3, 1),
    ("d4", "solo", CL, "It's called Claude Duet. A research preview, from [October twenty-first.|Oct 21.]", .3, 1),
    ("d5", "devclose", DEV, "What does it do?", .3, 1),
    ("d6", "soloclose", CL, "Every morning, it sends you a short brief. Then it checks your connected apps every few hours.", .3, 1),
    ("d7", "devclose", DEV, "Even when my laptop is off?", .3, 1),
    ("d8", "solo", CL, "Yes. It runs on its own computer, with its own browser.", .3, 1),
    ("d9", "devclose", DEV, "Can it pay my bills?", .35, 1),
    ("d10", "soloclose", CL, "Only if you say yes. It asks before it sends, pays, signs, or deletes anything.", .3, 1),
    ("d11", "devclose", DEV, "Can it trade stocks for me?", .3, 1),
    ("d12", "soloclose", CL, "Never. Not even if you say yes.", .3, 1),
    ("d13", "devmid", DEV, "Who can use it?", .35, 1),
    ("d14", "solo", CL, "There's a waitlist. Pro and Max users in the U S go first.", .3, 1),
    ("d15", "devclose", DEV, "Does it cost extra?", .3, 1),
    ("d16", "soloclose", CL, "It's in the plan. But its background checks use your limits.", .3, 1),
    ("d17", "devclose", DEV, "An AI that works while I sleep.", .5, .95),
    ("d18", "soloclose", CL, "And only wakes you when something needs you.", .4, .95),
]
HOLDS = {}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="Claude Duet: An AI That Works While You Sleep",
    alt_titles=["Hey Claude, What's New? (Claude Duet Explained)", "This AI Checks Your Accounts Every Few Hours"],
    description="""Anthropic's new Claude Duet checks your apps every few hours and works on its own computer, even
when your laptop is off. Claude explains what it can and can't do.

Real (claude.com, 21 Oct 2026): Claude Duet is a research preview with a waitlist, starting with US Pro and Max
subscribers, on iOS, Android and claude.ai. It sends a morning brief, checks connected accounts every few hours, runs
on its own virtual machine and browser, asks before it sends a message, makes a payment, signs a document or deletes
anything, and never trades securities or moves money between accounts, even with approval. Its background checks count
toward plan limits. Dev and Claude are parody characters.

Ep. 39 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 Would you let an AI check your accounts every few hours? Yes or never? 👇""",
    hashtags=["#ClaudeAI", "#AIAgents", "#AINews"],
    tags=["claude duet", "anthropic", "ai agent", "proactive ai", "claude", "ai news", "ai assistant",
          "automation", "programmer humor", "tech news"],
    pinned_comment="Would you let an AI check your accounts every few hours? 👇 Subscribe for tomorrow's AI news.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a3d"))
WHITE = (1, 1, 1)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    B = tl.by_id
    headline(cr, t, B["d4"].start + 0.3, B["d4"].end + 0.2, "claude.com  ·  Oct 21", "Claude Duet: a proactive agent app",
             [("research preview", YEL), ("iOS · Android · claude.ai", WHITE)])
    headline(cr, t, B["d6"].start + 0.3, B["d6"].end + 0.2, "Claude Duet", "What it does",
             [("morning brief", WHITE), ("checks your apps every few hours", WHITE), ("messages you only when needed", GREEN)])
    headline(cr, t, B["d10"].start + 0.3, B["d12"].end + 0.2, "Claude Duet  ·  rules", "Asks you first before it:",
             [("sends · pays · signs · deletes", YEL), ("never: trades stocks or moves money", RED)])
    bignum(cr, t, B["d14"].start + 0.3, B["d14"].end + 0.2, "access", "Waitlist", "US Pro and Max first", col=ORANGE, count=False)
    headline(cr, t, B["d16"].start + 0.3, B["d16"].end + 0.2, "cost", "Included in Pro and Max",
             [("background checks use your limits", YEL)])
    cue("ding", t, B["d2"].start + 0.2)
    th.captions(cr, t, tl, y=400, size=60)
