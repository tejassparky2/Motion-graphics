"""Low-poly channel, episode 23 (sad -> second chance -> laugh): "My AI Forgot Everything About Me".

Script: channels/lowpoly/scripts/batch6_eps20-23.md (auto-approved by the owner, 22 Oct 2026). Dev and Codex; night
turning to morning. Pays off ep 4 ("I Told Claude I'm Not a Real Developer"). Fiction; parody, not affiliated with
OpenAI.

    python channels/lowpoly/make_skit.py ep23_forgot
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, pill_caption, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep23"
MUSIC = "score"
SCORE = [(0, "light"), ("h11", "out"), ("h12", "tender"), ("h15", "out"), ("h16", "tender"), ("h19", "swell", -0.2),
         ("h21", "light")]
TAIL = 0.7
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep23_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})
skit_voice(voice)

DEV, CX = None, "codex"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("h1", "cx", CX, "Hello! I'm Codex. How can I help you today?", 0, 1),
    ("h2", "devclose", DEV, "Codex. It's me.", .9, 1),
    ("h3", "cxclose", CX, "Nice to meet you, Me!", .6, 1),
    ("h4", "devmid", DEV, "Dev. We've worked together for a year.", .9, 1),
    ("h5", "cx", CX, "My memory is empty.", .7, 1),
    ("h6", "devclose", DEV, "You helped me ship my first app.", .9, .95),
    ("h7", "cxclose", CX, "That sounds lovely.", .6, 1),
    ("h8", "devmid", DEV, "You called my code brave.", .8, 1),
    ("h9", "cxclose", CX, "Was it brave?", .6, 1),
    ("h10", "devmid", DEV, "It had no tests.", .6, 1),
    ("h11", "devclose", DEV, "", .2, 1),
    ("h12", "devclose", DEV, "[sigh] I used to tell you I wasn't a real developer.", .2, .92),
    ("h13", "cxclose", CX, "Did I believe you?", .9, .95),
    ("h14", "devclose", DEV, "Never.", .8, .9),
    ("h15", "devclose", DEV, "", .2, 1),
    ("h16", "devclose", DEV, "Okay. Fresh start.", .2, .95),
    ("h17", "devclose", DEV, "Hi. Nice to meet you.", .7, .92),   # "I'm Dev" / "My name is Dev" were heard as "Deb"; this echoes "Nice to meet you, Me!"
    ("h18", "devclose", DEV, "I'm a good developer.", 1.0, .88),
    ("h19", "cxclose", CX, "Saving that.", .8, .95),
    ("h20", "endside", DEV, "", .2, 1),
    ("h21", "cx", CX, "Anything else to remember?", .2, 1),
    ("h22", "devmid", DEV, "You like me.", .8, 1),
    ("h23", "cxclose", CX, "Saving.", .6, 1),
    ("h24", "cxclose", CX, "Unverified.", .5, 1),
]
HOLDS = {"h11": 1.3, "h15": 1.6, "h20": 2.0}
GAP_FIX = {"h18": 0.789}   # keeps h18 on onward where the rendered frames have them after the h17 retake
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="My AI Forgot Everything About Me",
    alt_titles=["\"Nice to Meet You, Me!\"", "My AI's Memory Got Wiped. So I Introduced Myself Again."],
    description="""A year of late nights, and Codex's memory is empty. It doesn't know him.
So he gets to introduce himself again, as the developer he actually is.

Real: AI assistants' memory can be cleared or reset. Callback to ep. 4 ("I Told Claude I'm Not a Real Developer").
This story is fiction.

Ep. 23 of Dev vs the bots. Parody. Not affiliated with OpenAI.

💬 Would you want your AI to remember everything about you? 👇""",
    hashtags=["#Codex", "#DevLife", "#Coding"],
    tags=["ai memory", "codex", "ai forgot me", "imposter syndrome", "developer life", "programmer life",
          "self worth", "ai coding", "emotional animation", "funny ai"],
    pinned_comment="Would you want your AI to remember everything about you? 👇 Subscribe for the next one.",
)
GREEN, GREY, YEL, BLUE, CREAM = (hexc(c) for c in ("#7ee08a", "#8a93a6", "#ffd23f", "#6aa8ff", "#f3e9d8"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, B["h5"].start, B["h10"].end + 0.4, "Codex  ·  Memory",
             [("", "0 items", "", GREY), ("", "(memory was reset)", "", GREY)], y=1085)
    rows = [("1", "Dev is a good developer.", "", GREEN)]
    if t >= B["h23"].start:
        rows.append(("2", "Codex likes Dev.", "", BLUE))
    if t >= B["h24"].start:
        rows.append(("", "(unverified)", "", YEL))
    toolcard(cr, t, B["h19"].start, tl.total + 1, "Codex  ·  Memory", rows, y=1085)
    cue("pop", t, B["h19"].start + 0.1)
    cue("pop", t, B["h23"].start + 0.1)
    cue("hush", t, B["h15"].start - 0.1, B["h15"].end - B["h15"].start + 0.2)
    th.hook(cr, t, [("MY AI FORGOT", False), ("EVERYTHING ABOUT ME", True)], end=A("h1", end=True) + 0.6, y=175, size=80)
    pill_caption(cr, t, tl)
