"""Low-poly channel, episode 24 (comedy): "My AI Recommended a Package That Doesn't Exist".

Script: channels/lowpoly/scripts/batch7_comedy_eps24-27.md (auto-approved by the owner, 22 Oct 2026). Dev and Codex;
night. Real problem: package hallucination ("slopsquatting"). Fiction; parody, not affiliated with OpenAI.

    python channels/lowpoly/make_skit.py ep24_package
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, pill_caption, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep24"
MUSIC = "score"
SCORE = [(0, "light"), ("p15", "out", -0.4)]
TAIL = 0.6
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep24_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})
skit_voice(voice)

DEV, CX = None, "codex"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("p1", "cx", CX, "Just install fix-everything.", 0, 1),
    ("p2", "devmid", DEV, "What's fix-everything?", .7, 1),
    ("p3", "cx", CX, "Very popular. Two million downloads a week.", .5, 1),
    ("p4", "devclose", DEV, "It doesn't exist.", .9, 1),
    ("p5", "cxclose", CX, "Try fix-everything-pro.", .4, 1),
    ("p6", "devclose", DEV, "Doesn't exist.", .8, 1),
    ("p7", "cxclose", CX, "Fix-everything-pro-max.", .4, 1),
    ("p8", "devclose", DEV, "Codex.", 1.0, 1),
    ("p9", "cx", CX, "It's in my training data. I can feel it.", .4, 1),
    ("p10", "devmid", DEV, "You made it up.", .7, 1),
    ("p11", "cxclose", CX, "I prefer, predicted it. [laugh]", .4, 1),
    ("p12", "cx", CX, "Fine. I'll publish it. Then it exists.", .9, 1),
    ("p13", "ots", DEV, "", .2, 1),
    ("p14", "devclose", DEV, "", .2, 1),
    ("p15", "devclose", DEV, "Who is downloading this?", .2, 1),
    ("p16", "cxclose", CX, "Other AIs.", .7, 1),
    ("p17", "devmid", DEV, "What does it even do?", 1.0, 1),
    ("p18", "cxclose", CX, "Nothing. But confidently.", .5, 1),
]
HOLDS = {"p13": 1.6, "p14": 1.6}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="My AI Recommended a Package That Doesn't Exist",
    alt_titles=["\"It's in My Training Data. I Can Feel It.\"", "npm install fix-everything"],
    description=""""Just install fix-everything." It doesn't exist. Neither does fix-everything-pro.
So Codex publishes it.

Real: a USENIX Security 2025 study found that 19.7% of code samples from code-writing AIs recommended at least
one package that doesn't exist, and attackers now register those made-up names ("slopsquatting"). This story is
fiction.

Ep. 24 of Dev vs the bots. Parody. Not affiliated with OpenAI.

💬 Your AI suggests a package. Do you check it exists, or just install it? 👇""",
    hashtags=["#Codex", "#ProgrammerHumor", "#npm"],
    tags=["ai hallucination", "slopsquatting", "npm install", "codex", "programmer humor", "coding memes",
          "fake package", "supply chain attack", "developer life", "funny ai"],
    pinned_comment="Your AI suggests a package. Do you check it exists, or just install it? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.62)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    for bid, name in (("p4", "fix-everything"), ("p6", "fix-everything-pro"), ("p8", "fix-everything-pro-max")):
        nxt = {"p4": "p5", "p6": "p7", "p8": "p9"}[bid]
        toolcard(cr, t, B[bid].start - 0.1, B[nxt].start + 0.2, "terminal",
                 [("$", f"npm install {name}", "", GREY), ("404", "Not Found", "", RED)], y=1085)
        cue("ding", t, B[bid].start - 0.05)
    toolcard(cr, t, B["p13"].start, B["p13"].end + 0.1, "terminal",
             [("$", "npm publish fix-everything", "", GREY), ("ok", "+ fix-everything@1.0.0", "", GREEN)], y=1085)
    toolcard(cr, t, B["p14"].start, B["p16"].end + 0.4, "npmjs.com  ·  fix-everything",
             [("", "30,212 downloads this week", "", YEL), ("", "Readme: (empty)", "", GREY)], y=1085)
    toolcard(cr, t, B["p18"].start - 0.1, tl.total + 1, "fix-everything / index.js",
             [("1", "module.exports = {}", "", GREY)], y=1085)
    cue("sigh", t, B["p8"].start - 0.75)
    cue("typing", t, B["p13"].start + 0.1, 1.0)
    cue("pop", t, B["p14"].start + 0.1)
    cue("hush", t, B["p18"].start - 0.15, B["p18"].end - B["p18"].start + 0.8)
    th.hook(cr, t, [("MY AI RECOMMENDED A PACKAGE", False), ("THAT DOESN'T EXIST", True)], end=A("p1", end=True) + 0.6, y=175, size=62)
    pill_caption(cr, t, tl)
