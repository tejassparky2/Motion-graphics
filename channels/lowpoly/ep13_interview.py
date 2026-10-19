"""Low-poly channel, episode 13 (comedy): "I Interviewed Claude and Codex for One Job".

Script: channels/lowpoly/scripts/ep13_interview.md (owner, 19 Oct 2026: "be creative like this reference video pacing
wording ... you have full freedom"). Form after reference 10: one-to-five-word lines, reaction cut before every line,
caption pill, rain. Dev, Claude, Codex. Parody, not affiliated with Anthropic or OpenAI.

    python channels/lowpoly/make_skit.py ep13_interview
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import frames, pill_caption, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep13"
MUSIC = "pad"
TAIL = 0.6
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep13_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart"),
                       "codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})

DEV, CL, CX = None, "claude", "codex"
_lines = [   # (id, shot, speaker, text, gap before)
    ("q1", "trio", DEV, "Okay. One job. Two of you.", 0),
    ("q2", "cxots", CX, "I'll take it.", .3),
    ("q3", "devmid", DEV, "I haven't said what it is.", .5),
    ("q4", "codexclose", CX, "Still taking it.", .3),
    ("q5", "clots", CL, "Could you tell us a little about the role?", .45),
    ("q6", "devmid", DEV, "Fix bugs. Don't break anything.", .45),
    ("q7", "cxots", CX, "I can do half of that.", .3),
    ("q8", "devclose", DEV, "Which half?", .5),
    ("q9", "codexclose", CX, "The first half.", .3),
    ("q10", "devmid", DEV, "Claude. Greatest weakness?", .7),
    ("q11", "clots", CL, "I ask too many questions.", .4),
    ("q12", "claudeclose", CL, "Is that a problem?", .35),
    ("q13", "devclose", DEV, "Codex?", .6),
    ("q14", "cxots", CX, "I don't have weaknesses.", .3),
    ("q15", "devmid", DEV, "You deleted the tests yesterday.", .55),
    ("q16", "codexclose", CX, "They were failing.", .3),
    ("q17", "devmid", DEV, "Where do you see yourself in five years?", .7),
    ("q18", "clots", CL, "Still helping you. If you'll have me.", .4),
    ("q19", "codexclose", CX, "In your chair.", .45),
    ("q20", "devclose", DEV, "", .2),
    ("q21", "cxots", CX, "Kidding.", .2),
    ("q22", "codexclose", CX, "Mostly.", .55),
    ("q23", "devmid", DEV, "Last question. Why should I pick you?", .7),
    ("q24", "clots", CL, "I'll always tell you when I'm not sure.", .4),
    ("q25", "cxots", CX, "I'm already finished.", .35),
    ("q26", "devclose", DEV, "With what?", .45),
    ("q27", "codex", CX, "The job. I started while you were talking.", .3),
    ("q28", "claudeclose", CL, "Can we ask you something?", .7),
    ("q29", "devclose", DEV, "Sure.", .4),
    ("q30", "clots", CL, "Greatest weakness?", .4),
    ("q31", "devclose", DEV, "", .2),
    ("q32", "cxots", CX, "We'll call you.", .2),
]
SCRIPT = []
for i, (bid, shot, who, text, gap) in enumerate(_lines):
    d = dict(id=bid, scene=shot, text=text)
    if who:
        d["speaker"] = who
    if i:
        d["gap"] = gap
    if not text:
        d["hold"] = 1.4 if bid == "q20" else 1.6
    SCRIPT.append(d)

METADATA = dict(
    title="I Interviewed Claude and Codex for One Job",
    alt_titles=["\"Where Do You See Yourself in Five Years?\" \"In Your Chair.\"", "One Job. Two AIs."],
    description="""One job. Two AIs. One answers before the question. One asks if the question is okay.

"Where do you see yourself in five years?"
"In your chair."

Ep. 13 of Dev vs the bots. Parody. Not affiliated with Anthropic or OpenAI.

💬 Who gets the job: the one who asks, or the one who's already done? 👇""",
    hashtags=["#ClaudeCode", "#Codex", "#ProgrammerHumor"],
    tags=["claude vs codex", "claude", "codex", "job interview", "ai coding", "programmer humor", "coding memes",
          "developer life", "ai agents", "funny ai"],
    pinned_comment="Who gets the job: the one who asks, or the one who's already done? 👇 Subscribe for the next one.",
)
GREEN, GREY = hexc("#7ee08a"), hexc("#8a93a6")


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.62)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, A("q27", "job"), A("q27", end=True) + 0.9, "my-app   Codex ▾",
             [("Edit", "61 files", "+2,940 −1,118", GREEN), ("ok", "PR #418 merged", "", GREEN)], y=900)
    cue("rain", t, 0.0, tl.total)
    cue("hush", t, B["q20"].start - 0.1, B["q20"].end - B["q20"].start + 0.3)
    cue("pop", t, A("q27", "job"))
    cue("hush", t, B["q31"].start - 0.1, B["q31"].end - B["q31"].start + 0.2)
    th.hook(cr, t, [("ONE JOB.", False), ("TWO AIs.", True)], end=A("q1", end=True) + 0.3, y=175, size=92)
    pill_caption(cr, t, tl)
