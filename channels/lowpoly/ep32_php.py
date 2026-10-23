"""Low-poly channel, episode 32: "Codex, PHP Has Two Critical Bugs".

Script: channels/lowpoly/scripts/batch9_morphy_eps32-35.md (auto-approved by the owner, 23 Oct 2026). @agentmorphy's
form: line 1 is "Codex, <today's news>", the AI states embarrassing facts flatly, three exposures, a twist; snappy
gaps, a music bed all the way, captions that build up word by word. Real: php.net 21 Oct 2026 (PHP 8.5.12, 8.4.27,
8.3.36, 8.2.35 fix two critical RCE bugs) and 23 Oct (turn off session upload progress); Node.js security release the
same day (10 CVEs); PHP 7.2 support ended 30 Nov 2020. Fiction; parody, not affiliated with OpenAI.

    python channels/lowpoly/make_skit.py ep32_php
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_caption, build_script, frames, mono, screen_insert, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import rrect, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep32"
MUSIC = "score"
SCORE = [(0, "light"), ("x16", "tender"), ("x19", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep32_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})
skit_voice(voice)

DEV, CX = None, "codex"
PHP = "[P H P|PHP]"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("x1", "devmid", DEV, f"Codex. {PHP} has two critical bugs.", 0, 1),
    ("x2", "cxclose", CX, "It's patched. Update to [eight point four point twenty-seven|8.4.27].", .35, 1),
    ("x3", "devclose", DEV, "And Node has ten. Same day.", .4, 1),
    ("x4", "cxclose", CX, "Update Node too.", .35, 1),
    ("x5", "devmid", DEV, f"Okay. Which {PHP} am I on?", .45, 1),
    ("x6", "cxclose", CX, "[Seven point two|7.2].", .35, 1),
    ("x7", "devclose", DEV, "Is there a patch for [seven point two|7.2]?", .45, 1),
    ("x8", "cxclose", CX, "Support ended in [twenty twenty|2020].", .35, 1),
    ("x9", "devclose", DEV, "Then the bug can't find it. It's too old.", .5, 1),
    ("x10", "cx", CX, "Bots found it. Four thousand times today.", .35, 1),
    ("x11", "devclose", DEV, "Nobody even uses that site.", .5, 1),
    ("x12", "cxclose", CX, "It's your login page.", .35, 1),
    ("x13", "devmid", DEV, "Update everything.", .6, 1),
    ("x14", "cx", CX, "Done. [Eight point four point twenty-seven|8.4.27].", .4, 1),
    ("x15", "devclose", DEV, "We're safe. [chuckle]", .5, 1),
    ("x16", "cxclose", CX, "One more thing. Turn off upload progress.", .4, 1),
    ("x17", "devclose", DEV, "My site has an upload progress bar!", .4, 1),
    ("x18", "cxclose", CX, "It's been stuck at ninety-nine percent since [twenty nineteen|2019].", .4, 1),
    ("x19", "devclose", DEV, "That's the design.", .7, .95),
]
HOLDS = {}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="Codex, PHP Has Two Critical Bugs",
    alt_titles=["Which PHP Am I On?", "\"It's Been Stuck at 99% Since 2019.\""],
    description="""PHP shipped emergency fixes for two critical bugs. Node shipped ten fixes the same day.
Dev asks Codex which PHP he's on.

Real: on 21 Oct 2026 PHP 8.5.12, 8.4.27, 8.3.36 and 8.2.35 fixed two critical bugs (CVE-2026-109618,
CVE-2026-109619) that "can allow unauthenticated remote code execution" (php.net). On 23 Oct php.net advised setting
session.upload_progress.enabled=0 until the next release. Node.js fixed 10 CVEs the same day. PHP 7.2 stopped getting
security fixes in November 2020. Dev, his site and his progress bar are fiction.

Ep. 32 of Dev vs the bots. Parody. Not affiliated with OpenAI.

💬 Be honest: what's the oldest thing still running in production for you? 👇""",
    hashtags=["#PHP", "#Codex", "#ProgrammerHumor"],
    tags=["php vulnerability", "php 8.4.27", "cve-2026-109618", "php update", "codex", "programmer humor",
          "coding memes", "web security", "developer life", "funny ai"],
    pinned_comment="What's the oldest thing still running in production for you? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a3d"))
WHITE = (1, 1, 1)


def _log(cr, x, y, w, h, t, k):
    mono(cr, "access.log  (today)", x + 30, y + 50, 22, GREY, k)
    rows = ["GET /login.php   bot", "POST /login.php  bot", "GET /login.php   bot", "GET /upload.php  bot",
            "POST /login.php  bot", "GET /login.php   bot", "GET /login.php   bot"]
    for i, r in enumerate(rows):
        mono(cr, r, x + 30, y + 110 + 46 * i, 26, WHITE if i % 3 else YEL, k)
    mono(cr, "4,000 requests today", x + 30, y + h - 40, 30, RED, k)


def _done(cr, x, y, w, h, t, k):
    mono(cr, "$ update php", x + 30, y + 60, 26, GREY, k)
    mono(cr, "PHP 7.2.34  ->  8.4.27", x + 30, y + 140, 32, WHITE, k)
    mono(cr, "✓ 2 critical bugs fixed", x + 30, y + 210, 30, GREEN, k)


def _bar(cr, x, y, w, h, t, k):
    mono(cr, "Uploading photo.jpg", x + 30, y + 90, 30, WHITE, k)
    rrect(cr, x + 30, y + 140, w - 60, 40, 14)
    cr.set_source_rgba(1, 1, 1, 0.12)
    cr.fill()
    rrect(cr, x + 30, y + 140, (w - 60) * 0.99, 40, 14)
    cr.set_source_rgb(*ORANGE[:3])
    cr.fill()
    mono(cr, "99%", x + 30, y + 240, 40, ORANGE, k)
    mono(cr, "since 2019", x + 30, y + 300, 26, GREY, k)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, 0.0, B["x3"].end + 0.3, "php.net  ·  21 Oct",
             [("!", "2 critical bugs (remote code execution)", "", RED), ("ok", "Fixed: 8.5.12 · 8.4.27 · 8.3.36", "", GREEN)], y=1085)
    toolcard(cr, t, B["x6"].start, B["x8"].end + 0.3, "your server", [("", "PHP 7.2.34", "", YEL),
             ("", "security support ended 2020", "", RED)], y=1085)
    screen_insert(cr, t, B["x10"].start + 0.3, B["x11"].end + 0.3, "access.log", "11:40 PM", _log)
    screen_insert(cr, t, B["x14"].start + 0.2, B["x15"].end + 0.3, "terminal", "11:52 PM", _done)
    toolcard(cr, t, B["x16"].start, B["x17"].end + 0.3, "php.net  ·  23 Oct",
             [("", "session.upload_progress.enabled=0", "", YEL)], y=1085)
    screen_insert(cr, t, B["x18"].start + 0.2, B["x18"].end + 0.3, "yoursite.com/upload", "11:58 PM", _bar)
    cue("ding", t, 0.15)
    cue("typing", t, B["x14"].start, 0.8)
    build_caption(cr, t, tl)
