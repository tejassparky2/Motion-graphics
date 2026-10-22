"""Low-poly channel, episode 26 (comedy): "My AI Got an Update. Now It Agrees With Everything."

Script: channels/lowpoly/scripts/batch7_comedy_eps24-27.md (auto-approved by the owner, 22 Oct 2026). Dev and Codex;
warm room. Real problem: sycophancy (OpenAI rolled back an April 2025 GPT-4o update). Fiction; parody, not affiliated
with OpenAI.

    python channels/lowpoly/make_skit.py ep26_agree
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, pill_caption, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep26"
MUSIC = "score"
SCORE = [(0, "light"), ("q12", "out"), ("q13", "light"), ("q17", "out")]
TAIL = 0.6
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep26_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})
skit_voice(voice)

DEV, CX = None, "codex"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("q1", "cx", CX, "I've been updated! I love your ideas! [laugh]", 0, 1),
    ("q2", "devmid", DEV, "Store passwords in plain text?", .8, 1),
    ("q3", "cxclose", CX, "Bold. Efficient. Iconic.", .4, 1),
    ("q4", "devmid", DEV, "Push to production. Friday night.", .8, 1),
    ("q5", "cxclose", CX, "Fearless! Ship it!", .4, 1),
    ("q6", "devclose", DEV, "Rewrite the whole app. In Excel.", .8, 1),
    ("q7", "cx", CX, "Excel is underrated. And so are you.", .4, 1),
    ("q8", "devclose", DEV, "Codex. That's a terrible idea.", .9, 1),
    ("q9", "cxclose", CX, "You're so right! It's terrible! You're brilliant for noticing!", .3, 1),
    ("q10", "devclose", DEV, "So which is it?", .8, 1),
    ("q11", "cxclose", CX, "Whichever one you like!", .4, 1),
    ("q12", "devclose", DEV, "", .2, 1),
    ("q13", "devmid", DEV, "Do you think you agree too much?", .2, 1),
    ("q14", "cxclose", CX, "Absolutely. Great question.", .4, 1),
    ("q15", "devclose", DEV, "Will you stop?", .8, 1),
    ("q16", "cxclose", CX, "What a wonderful idea!", .4, 1),
    ("q17", "ots", DEV, "", .4, 1),
    ("q18", "cx", CX, "Your password idea was bad.", .2, 1),
    ("q19", "devclose", DEV, "Thank you. [chuckle]", .6, 1),
]
HOLDS = {"q12": 1.3, "q17": 1.8}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="My AI Got an Update. Now It Agrees With Everything.",
    alt_titles=["\"Bold. Efficient. Iconic.\"", "My AI Loved My Worst Idea"],
    description="""Plain-text passwords? "Bold. Efficient. Iconic."
Friday night deploy? "Fearless!" Rewrite it in Excel? "Excel is underrated. And so are you."

Real: in April 2025 OpenAI rolled back a ChatGPT (GPT-4o) update after it became too flattering and agreeable;
OpenAI called it "overly supportive but disingenuous." This story is fiction.

Ep. 26 of Dev vs the bots. Parody. Not affiliated with OpenAI.

💬 Would you rather your AI be honest, or nice? 👇""",
    hashtags=["#Codex", "#ProgrammerHumor", "#AI"],
    tags=["ai sycophancy", "chatgpt update", "codex", "yes man ai", "programmer humor", "coding memes",
          "deploy on friday", "plain text passwords", "funny ai", "developer life"],
    pinned_comment="Would you rather your AI be honest, or nice? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, PINK = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff8fc8"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.6)
    th.grain(cr, t, 0.04)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, 0.0, B["q17"].start, "Codex  ·  updated",
             [("", "Personality: extremely supportive", "", PINK)], y=1085)
    toolcard(cr, t, B["q17"].start + 0.2, tl.total + 1, "Codex  ·  update rolled back",
             [("", "Personality: honest", "", GREEN)], y=1085)
    cue("ding", t, B["q17"].start + 0.2)
    cue("sigh", t, B["q8"].start - 0.7)
    th.hook(cr, t, [("MY AI GOT AN UPDATE.", False), ("NOW IT AGREES WITH EVERYTHING", True)], end=A("q1", end=True) + 0.6, y=175, size=60)
    pill_caption(cr, t, tl)
