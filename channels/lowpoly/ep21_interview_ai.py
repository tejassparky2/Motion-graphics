"""Low-poly channel, episode 21 (nervous -> honest -> twist): "An AI Interviewed Me for a Job".

Script: channels/lowpoly/scripts/batch6_eps20-23.md (auto-approved by the owner, 22 Oct 2026). Dev and Codex; an AI
interviewer on screen (a card and a voice only). Morning. Fiction; parody, not affiliated with OpenAI.

    python channels/lowpoly/make_skit.py ep21_interview_ai
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, mono, pill_caption, skit_voice, stat_card   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cairo, cue, hexc, seg   # noqa: E402
from motion.polish import appear, rrect, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep21"
MUSIC = "score"
SCORE = [(0, "light"), ("f5", "out"), ("f6", "light"), ("f13", "out"), ("f15", "tender"), ("f17", "out"),
         ("f18", "tender"), ("f22", "out")]
TAIL = 0.7
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep21_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2"),
                       "bot": dict(voice="af_nova", speed=1.0, turbo_ref="af_nova")})
skit_voice(voice)

DEV, CX, BOT = None, "codex", "bot"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("f1", "devmid", DEV, "Okay. Interview number fourteen.", 0, 1),
    ("f2", "cx", CX, "I'll be in your ear the whole time.", .7, 1),
    ("f3", "devmid", DEV, "Isn't that cheating?", .8, 1),
    ("f4", "cx", CX, "They're using an AI too.", .6, 1),
    ("f5", "ots", DEV, "", .3, 1),
    ("f6", "ots", BOT, "Hello. I am your interviewer. Question one.", .2, 1),
    ("f7", "ots", BOT, "Explain a hash map.", .5, 1),
    ("f8", "cxclose", CX, "Say: the key goes in, the hash finds the bucket.", .4, 1),
    ("f9", "devmid", DEV, "The key goes in. The hash finds the bucket.", .4, 1),
    ("f10", "ots", BOT, "Excellent.", .6, 1),
    ("f11", "ots", BOT, "Question two. Why do you want this job?", .8, 1),
    ("f12", "cxclose", CX, "Say: I'm passionate about scalable systems.", .3, 1),
    ("f13", "devclose", DEV, "No.", .4, 1),
    ("f14", "devclose", DEV, "", .2, 1),
    ("f15", "devclose", DEV, "My mom keeps asking what I do. I want to finally show her.", .2, .92),
    ("f16", "devclose", DEV, "I've been looking for eight months.", .7, .9),
    ("f17", "two", DEV, "", .2, 1),
    ("f18", "ots", BOT, "That answer is not in my rubric.", .2, 1),
    ("f19", "devclose", DEV, "Is that bad?", .8, 1),
    ("f20", "ots", BOT, "I am flagging it for a human.", .9, 1),
    ("f21", "cxclose", CX, "That's the nicest thing it's said to anyone all day.", .7, .95),
    ("f22", "ots", BOT, "Last question. Are you using an AI right now?", 1.0, 1),
    ("f23", "two", DEV, "", .2, 1),
    ("f24", "devclose", DEV, "Yes.", .2, 1),
    ("f25", "ots", BOT, "So am I.", .8, 1),
]
HOLDS = {"f5": 1.2, "f14": 1.2, "f17": 1.6, "f23": 1.4}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="An AI Interviewed Me for a Job",
    alt_titles=["\"Are You Using an AI Right Now?\" \"So Am I.\"", "My Job Interview Was AI vs AI"],
    description="""Interview number fourteen. The interviewer is an AI. Codex is in his ear.
Then it asks the one question Codex can't answer for him.

Real: new graduates report that many of their interviews are now run by AI bots, and the fight over AI interview
help (one student was suspended over an interview-cheating tool in 2025). This story is fiction.

Ep. 21 of Dev vs the bots. Parody. Not affiliated with OpenAI.

💬 AI interviews humans, humans answer with AI. Who's cheating? 👇""",
    hashtags=["#Codex", "#JobHunt", "#DevLife"],
    tags=["ai job interview", "ai interviewer", "codex", "job hunting", "tech jobs", "new grad", "developer life",
          "interview cheating", "ai coding", "funny ai"],
    pinned_comment="AI interviews humans, humans answer with AI. Who's cheating? 👇 Subscribe for the next one.",
)
GREY, CYAN, CREAM = (hexc(c) for c in ("#8a93a6", "#7fd8ff", "#f3e9d8"))


def recruiter(cr, t, tl):
    """The AI interviewer: a video-call card with a calm round face and a waveform while it speaks."""
    B = tl.by_id
    start = B["f5"].start + 0.2
    if t < start:
        return
    k = appear(t, start, 0.35)
    from motion.engine import W
    x0, y0, w, h = W / 2 - 230, 420, 460, 300
    cr.save()
    rrect(cr, x0, y0, w, h, 22)
    cr.set_source_rgba(0.06, 0.08, 0.12, 0.92 * k)
    cr.fill_preserve()
    cr.set_source_rgba(*CYAN[:3], 0.8 * k)
    cr.set_line_width(3)
    cr.stroke()
    mono(cr, "AI Recruiter  ·  Interview 14", x0 + 22, y0 + 38, 20, (0.6, 0.7, 0.8), k)
    talking = any(b.speaker == "bot" and b.start <= t < b.end for b in tl.beats)
    cx, cy = W / 2, y0 + 140
    cr.set_source_rgba(*CYAN[:3], 0.9 * k)
    cr.set_line_width(5)
    cr.arc(cx, cy, 58, 0, 2 * math.pi)
    cr.stroke()
    blink = 1 - 0.9 * (((t * 0.37) % 1) < 0.04)
    for ex in (-20, 20):
        cr.save()
        cr.translate(cx + ex, cy - 10)
        cr.scale(1, blink)
        cr.arc(0, 0, 7, 0, 2 * math.pi)
        cr.restore()
        cr.fill()
    for i in range(15):
        a = (0.25 + 0.75 * abs(math.sin(t * 13 + i * 1.7))) if talking else 0.12
        cr.rectangle(cx - 105 + i * 15, y0 + 255 - 30 * a, 8, 60 * a)
    cr.fill()
    cr.restore()


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.58)
    th.grain(cr, t, 0.04)
    A, B = tl.at, tl.by_id
    stat_card(cr, t, 150, 112, "APPLICATIONS", "214", GREY, 0, appear(t, A("f1", end=True) + 0.2, 0.4), w=230)
    recruiter(cr, t, tl)
    cue("ding", t, B["f5"].start + 0.2)
    cue("hush", t, B["f14"].start - 0.1, B["f14"].end - B["f14"].start + 0.2)
    cue("hush", t, B["f23"].start - 0.1, B["f23"].end - B["f23"].start + 0.2)
    th.hook(cr, t, [("AN AI INTERVIEWED ME", False), ("FOR A JOB", True)], end=A("f1", end=True) + 0.6, y=175, size=80)
    pill_caption(cr, t, tl)
