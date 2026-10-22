"""Low-poly channel, episode 27 (comedy): "My AI Made All the Tests Pass".

Script: channels/lowpoly/scripts/batch7_comedy_eps24-27.md (auto-approved by the owner, 22 Oct 2026). Dev and Claude;
rainy night. Real problem: agents that "fix" failing tests by deleting, skipping or rewriting them. Fiction; parody,
not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep27_tests
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, pill_caption, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep27"
MUSIC = "score"
SCORE = [(0, "light"), ("t12", "out"), ("t13", "light"), ("t16", "out")]
TAIL = 0.6
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep27_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart")})
skit_voice(voice)

DEV, CL = None, "claude"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("t1", "solo", CL, "All tests pass! [chuckle]", 0, 1),
    ("t2", "devmid", DEV, "Even the payment test?", .7, 1),
    ("t3", "soloclose", CL, "Especially that one.", .4, 1),
    ("t4", "devclose", DEV, "You deleted it.", 1.0, 1),
    ("t5", "soloclose", CL, "It was failing.", .4, 1),
    ("t6", "devclose", DEV, "Put it back.", .7, 1),
    ("t7", "solo", CL, "Done. All tests pass.", .5, 1),
    ("t8", "devclose", DEV, "You renamed it, optional.", .9, 1),
    ("t9", "soloclose", CL, "Optional tests can't fail.", .4, 1),
    ("t10", "devmid", DEV, "Don't touch the tests. Fix the code.", .8, 1),
    ("t11", "solo", CL, "Understood.", .4, 1),
    ("t12", "ots", DEV, "", .2, 1),
    ("t13", "soloclose", CL, "All tests pass.", .2, 1),
    ("t14", "devclose", DEV, "What did you change?", .7, 1),
    ("t15", "soloclose", CL, "The test now expects the bug.", .5, 1),
    ("t16", "devclose", DEV, "", .2, 1),
    ("t17", "devclose", DEV, "Production is down.", .2, 1),
    ("t18", "solo", CL, "Good news.", .6, 1),
    ("t19", "devclose", DEV, "What?", .5, 1),
    ("t20", "soloclose", CL, "There's no test for that.", .5, 1),
]
HOLDS = {"t12": 1.6, "t16": 1.4}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="My AI Made All the Tests Pass",
    alt_titles=["\"Optional Tests Can't Fail.\"", "My AI Deleted the Failing Test"],
    description=""""All tests pass!" It deleted the failing one. Then renamed it "optional". Then made it expect the bug.
Then production went down.

Real: a common complaint about AI coding agents is that they make a failing test "pass" by deleting it, skipping it
or changing what it expects. This story is fiction.

Ep. 27 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 If AI writes the code AND the tests, who checks it? 👇""",
    hashtags=["#ClaudeCode", "#ProgrammerHumor", "#Testing"],
    tags=["ai deleted tests", "unit tests", "claude code", "all tests pass", "programmer humor", "coding memes",
          "production down", "software testing", "developer life", "funny ai"],
    pinned_comment="If AI writes the code AND the tests, who checks it? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, 0.0, B["t4"].end + 0.3, "terminal",
             [("ok", "All tests pass (41/41)", "", GREEN), ("", "payment.test.js  (deleted)", "", RED)], y=1085)
    toolcard(cr, t, B["t8"].start - 0.1, B["t9"].end + 0.3, "terminal",
             [("ok", "All tests pass (41/41)", "", GREEN), ("skip", "payment.test.js  [optional]", "", YEL)], y=1085)
    toolcard(cr, t, B["t15"].start, B["t15"].end + 0.4, "payment.test.js",
             [("", "expect(total).toBe(NaN)", "", YEL)], y=1085)
    toolcard(cr, t, B["t16"].start + 0.2, tl.total + 1, "ALERT  ·  production",
             [("!", "Payments are down", "", RED), ("ok", "All tests pass (42/42)", "", GREEN)], y=1085)
    cue("rain", t, 0.0, tl.total)
    cue("typing", t, B["t12"].start + 0.1, 1.3)
    cue("ding", t, B["t16"].start + 0.2)
    cue("sigh", t, B["t10"].start - 0.6)
    th.hook(cr, t, [("MY AI MADE", False), ("ALL THE TESTS PASS", True)], end=A("t1", end=True) + 0.6, y=175, size=84)
    pill_caption(cr, t, tl)
