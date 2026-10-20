"""Low-poly channel, episode 15 (quiet, then warm): "My Junior Asked Me, Not the AI."

Script: channels/lowpoly/scripts/batch4_eps14-15.md (auto-approved by the owner, 20 Oct 2026). Dev at his desk, a
new junior developer (guest) beside him, Claude. Reference-10 form: short lines, reaction cuts, caption pill, rain, Turbo sound tags
(owner, 20 Oct 2026: "Use tags for emotions so it feels human").
Parody, not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep15_junior
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import frames, pill_caption, stat_card, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep15"
MUSIC = "pad"
TAIL = 0.6
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep15_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart"),
                       "junior": dict(voice="af_sarah", speed=1.0, turbo_ref="af_sarah")})

DEV, CL, JR = None, "claude", "junior"
_lines = [   # (id, shot, speaker, text, gap before)
    ("r1", "jr", JR, "Can you show me how you'd fix this?", 0),
    ("r2", "dev", DEV, "Just ask Claude.", .4),
    ("r3", "jr", JR, "I did. It fixed it.", .4),
    ("r4", "devjr", DEV, "So?", .35),
    ("r5", "jrclose", JR, "I still don't know why it broke.", .5),
    ("r6", "devjr", DEV, "", .2),
    ("r7", "devclose", DEV, "Claude. Explain it to her.", .2),
    ("r8", "solo", CL, "I could.", .45),
    ("r9", "soloclose", CL, "But she asked you.", .5),
    ("r10", "devclose", DEV, "I'm busy.", .5),
    ("r11", "jrclose", JR, "It's okay. I'll figure it out. [sniff]", .4),
    ("r12", "two", DEV, "", .2),
    ("r13", "devclose", DEV, "[sigh] Wait.", .2),
    ("r14", "devjr", DEV, "Pull your chair over.", .45),
    ("r15", "jrclose", JR, "[gasp] Really?", .35),
    ("r16", "devclose", DEV, "Someone did this for me once.", .5),
    ("r17", "screen", DEV, "See line twelve? That's where it breaks.", .6),
    ("r18", "jr", JR, "Why?", .35),
    ("r19", "devjr", DEV, "I don't know yet. Let's find out. [chuckle]", .4),
    ("r20", "soloclose", CL, "Should I just fix it?", .7),
    ("r21", "devclose", DEV, "No.", .3),
    ("r22", "jrclose", JR, "No.", .2),
]
SCRIPT = []
for i, (bid, shot, who, text, gap) in enumerate(_lines):
    d = dict(id=bid, scene=shot, text=text)
    if who:
        d["speaker"] = who
    if i:
        d["gap"] = gap
    if not text:
        d["hold"] = {"r6": 1.3, "r12": 1.8}[bid]
    if bid in ("r5", "r11", "r16"):
        d["pace"] = 0.92
    SCRIPT.append(d)

METADATA = dict(
    title="My Junior Asked Me, Not the AI",
    alt_titles=["\"Just Ask Claude.\" \"I Did.\"", "The New Junior Didn't Want the AI. She Wanted Me."],
    description="""The new junior could have asked the AI. She asked Dev.
"Just ask Claude." "I did. It fixed it. I still don't know why it broke."

Ep. 15 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 Do juniors still need a human, or is AI enough? 👇""",
    hashtags=["#ClaudeCode", "#DevLife", "#JuniorDeveloper"],
    tags=["junior developer", "mentorship", "claude", "ai coding", "learning to code", "developer life",
          "software engineer", "senior developer", "ai replacing juniors", "coding motivation"],
    pinned_comment="Do juniors still need a human, or is AI enough? 👇 Subscribe for the next one.",
)
GREEN, GREY, YEL, RED = (hexc(c) for c in ("#7ee08a", "#8a93a6", "#ffd23f", "#ff5c5c"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.66)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    stat_card(cr, t, 150, 112, "NEW JUNIOR", "Day 3", GREY, 0, appear(t, A("r1", end=True) + 0.3, 0.4), w=220)
    toolcard(cr, t, A("r3", "fixed") - 0.1, B["r4"].end + 0.4, "Claude · cart.js",
             [("ok", "Fixed 1 issue", "", GREEN), ("", "(no explanation asked)", "", GREY)], y=900)
    toolcard(cr, t, A("r17", "twelve") - 0.1, A("r19", end=True) + 0.4, "cart.js",
             [("11", "for (let i = 0;", "", GREY), ("12", "  i <= items.length; i++)", "← here", YEL)], y=900)
    cue("rain", t, 0.0, tl.total)
    cue("hush", t, B["r6"].start - 0.1, B["r6"].end - B["r6"].start + 0.2)
    cue("hush", t, B["r12"].start - 0.1, B["r12"].end - B["r12"].start + 0.2)
    cue("pop", t, A("r22", "No"))
    th.hook(cr, t, [("MY JUNIOR ASKED ME.", False), ("NOT THE AI.", True)], end=A("r1", end=True) + 0.5, y=175, size=80)
    pill_caption(cr, t, tl)
