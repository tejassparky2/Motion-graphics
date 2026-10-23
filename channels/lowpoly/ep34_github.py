"""Low-poly channel, episode 34: "Codex, GitHub Is Down Again".

Script: channels/lowpoly/scripts/batch9_morphy_eps32-35.md (auto-approved by the owner, 23 Oct 2026). @agentmorphy's
form. Real: githubstatus.com lists 17 incidents from 1 to 23 Oct 2026. Inspired by a real report (anthropics/claude-code
#40710) where a dev blamed the AI for a `git reset --hard` every 10 minutes that was "a separate tool I built"; not
claimed in the video. Fiction; parody, not affiliated with OpenAI or GitHub.

    python channels/lowpoly/make_skit.py ep34_github
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_caption, build_script, frames, mono, screen_insert, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep34"
MUSIC = "score"
SCORE = [(0, "light"), ("z17", "tender"), ("z19", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep34_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})
skit_voice(voice)

DEV, CX = None, "codex"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("z1", "devmid", DEV, "Codex. GitHub is down. Again.", 0, 1),
    ("z2", "cxclose", CX, "Seventeen incidents in October.", .35, 1),
    ("z3", "devclose", DEV, "That's why my deploys keep failing.", .45, 1),
    ("z4", "cxclose", CX, "No. Your code failed first.", .35, 1),
    ("z5", "devclose", DEV, "Then why does my branch reset every ten minutes?", .5, 1),
    ("z6", "cxclose", CX, "Your cron job.", .35, 1),
    ("z7", "devclose", DEV, "I don't have a cron job.", .4, 1),
    ("z8", "cx", CX, "You wrote it in March. At [three A M|3 AM].", .35, 1),
    ("z9", "devclose", DEV, "What does it do?", .5, 1),
    ("z10", "cxclose", CX, "Resets your branch. Every ten minutes.", .35, 1),
    ("z11", "devmid", DEV, "I'm reporting this to GitHub.", .6, 1),
    ("z12", "cxclose", CX, "You did. Forty paragraphs.", .35, 1),
    ("z13", "devclose", DEV, "Did they reply?", .45, 1),
    ("z14", "cxclose", CX, "Not yet. They're down.", .35, 1),
    ("z15", "devclose", DEV, "Okay. Delete the cron job.", .6, 1),
    ("z16", "cx", CX, "Deleted.", .35, 1),
    ("z17", "devmid", DEV, "So I can go home? [chuckle]", .5, 1),
    ("z18", "cxclose", CX, "GitHub is back.", .45, 1),
    ("z19", "devclose", DEV, "I didn't see that.", .6, .95),
]
HOLDS = {}
GAP_FIX = {"z5": 0.151}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="Codex, GitHub Is Down Again",
    alt_titles=["My Branch Resets Every 10 Minutes", "\"No. Your Code Failed First.\""],
    description="""GitHub is down. Again. So that's why the deploys keep failing... right?
Codex has a different theory. It's in the crontab. Written at 3 AM.

Real: GitHub's status page lists 17 incidents from 1 to 23 October 2026. Dev, his cron job and his forty-paragraph
bug report are fiction (though developers really have filed detailed bug reports against tools for things their own
scripts did).

Ep. 34 of Dev vs the bots. Parody. Not affiliated with OpenAI or GitHub.

💬 Last time you blamed a tool, whose fault was it really? 👇""",
    hashtags=["#GitHub", "#Codex", "#ProgrammerHumor"],
    tags=["github down", "github outage", "cron job", "git reset", "codex", "programmer humor", "coding memes",
          "devops", "developer life", "funny ai"],
    pinned_comment="Last time you blamed a tool, whose fault was it really? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a3d"))
WHITE = (1, 1, 1)


def _cron(cr, x, y, w, h, t, k):
    mono(cr, "$ crontab -l", x + 30, y + 60, 26, GREY, k)
    mono(cr, "# added Mar 14, 3:07 AM", x + 30, y + 130, 26, GREY, k)
    mono(cr, "*/10 * * * *  cd ~/app &&", x + 30, y + 190, 28, WHITE, k)
    mono(cr, "  git reset --hard origin/old", x + 30, y + 240, 28, RED, k)
    mono(cr, "# temporary", x + 30, y + 310, 26, YEL, k)


def _issue(cr, x, y, w, h, t, k):
    mono(cr, "New issue  ·  draft", x + 30, y + 60, 22, GREY, k)
    mono(cr, "GitHub keeps resetting", x + 30, y + 130, 32, WHITE, k)
    mono(cr, "my branch!!!", x + 30, y + 175, 32, WHITE, k)
    for i in range(6):
        cr.rectangle(x + 30, y + 230 + 36 * i, (w - 60) * (0.95 - 0.07 * (i % 3)), 14)
    cr.set_source_rgba(1, 1, 1, 0.18)
    cr.fill()
    mono(cr, "40 paragraphs", x + 30, y + h - 40, 28, YEL, k)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, 0.0, B["z2"].end + 0.4, "githubstatus.com", [("!", "Incident with Actions", "", RED),
             ("", "October: 17 incidents", "", GREY)], y=1085)
    screen_insert(cr, t, B["z8"].start + 0.4, B["z9"].end + 0.3, "crontab", "11:46 PM", _cron)
    screen_insert(cr, t, B["z12"].start + 0.4, B["z13"].end + 0.3, "github.com", "11:49 PM", _issue)
    toolcard(cr, t, B["z16"].start, B["z16"].end + 0.5, "terminal", [("ok", "crontab -r", "", GREEN)], y=1085)
    toolcard(cr, t, B["z18"].start, tl.total + 1, "githubstatus.com", [("ok", "All systems operational", "", GREEN)], y=1085)
    cue("buzz", t, 0.1, 0.5)
    cue("ding", t, B["z18"].start)
    build_caption(cr, t, tl)
