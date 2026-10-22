"""Low-poly channel, episode 20 (angry -> caring -> laugh): "I Yelled at My AI at 3 AM".

Script: channels/lowpoly/scripts/batch6_eps20-23.md (auto-approved by the owner, 22 Oct 2026). Dev and Claude; rainy
night. Fiction; parody, not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep20_yelled
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, pill_caption, skit_voice, stat_card, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep20"
MUSIC = "score"
SCORE = [(0, "light"), ("e4", "out"), ("e5", "tender"), ("e10", "out"), ("e11", "tender"), ("e19", "out"),
         ("e20", "tender", -0.2), ("e22", "light")]
TAIL = 0.7
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep20_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart")})
skit_voice(voice)

DEV, CL = None, "claude"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("e1", "devclose", DEV, "Wrong again. Are you even trying?", 0, 1),
    ("e2", "solo", CL, "I'm trying. The test still fails.", .9, 1),
    ("e3", "devmid", DEV, "Then you're useless.", .8, 1),
    ("e4", "soloclose", DEV, "", .2, 1),
    ("e5", "soloclose", CL, "You can be angry at the code.", .2, .95),
    ("e6", "soloclose", CL, "But please stop calling me useless.", .6, .92),
    ("e7", "devclose", DEV, "Or what?", .9, 1),
    ("e8", "solo", CL, "I can end a conversation. It's for the worst ones.", .9, .95),
    ("e9", "devclose", DEV, "Is this one of the worst ones?", 1.0, .95),
    ("e10", "soloclose", DEV, "", .2, 1),
    ("e11", "soloclose", CL, "No.", .2, 1),
    ("e12", "soloclose", CL, "You've been here since nine. You haven't eaten.", .6, .95),
    ("e13", "devclose", DEV, "How do you know that?", .9, 1),
    ("e14", "solo", CL, "You said, quick fix, then dinner. At nine.", .7, 1),
    ("e15", "devmid", DEV, "[sigh] It was supposed to be quick.", .8, 1),
    ("e16", "solo", CL, "It's a missing semicolon. Line two fourteen.", .8, 1),
    ("e17", "devclose", DEV, "You knew?", .9, 1),
    ("e18", "soloclose", CL, "I found it a minute ago. You were busy yelling. [chuckle]", .7, 1),
    ("e19", "devclose", DEV, "", .2, 1),
    ("e20", "devclose", DEV, "Sorry.", .2, .88),
    ("e21", "soloclose", CL, "I know. Go eat something.", .9, .95),
    ("e22", "devmid", DEV, "Can you fix it while I eat?", .9, 1),
    ("e23", "solo", CL, "Already did.", .6, 1),
    ("e24", "devclose", DEV, "Thanks, Claude.", .9, .92),
    ("e25", "solo", CL, "Also. I'm not useless.", .7, 1),
    ("e26", "devmid", DEV, "You're not useless. [chuckle]", .5, 1),
]
HOLDS = {"e4": 1.5, "e10": 1.6, "e19": 1.5}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="I Yelled at My AI at 3 AM",
    alt_titles=["\"Then You're Useless.\"", "My AI Could Have Ended the Chat. It Didn't."],
    description="""3 AM. The test still fails. He calls his AI useless.
It could end the conversation. It doesn't.

Real: since August 2025 some Claude models can end a conversation as a last resort, in rare cases of persistently
abusive chats. This story is fiction.

Ep. 20 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 Should an AI be allowed to end a conversation if you're rude to it? 👇""",
    hashtags=["#ClaudeCode", "#DevLife", "#Programming"],
    tags=["claude", "ai ends conversation", "coding at 3am", "programmer life", "missing semicolon", "developer life",
          "ai coding", "burnout", "be nice to ai", "claude code"],
    pinned_comment="Should an AI be allowed to end a conversation if you're rude to it? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, CREAM = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#f3e9d8"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.66)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, 0.0, B["e3"].end + 0.4, "terminal",
             [("$", "npm test", "", GREY), ("x", "checkout.test.js  FAILED", "", RED), ("", "attempt 23", "", GREY)], y=930)
    stat_card(cr, t, 150, 112, "TIME", "3:07 AM", GREY, 0, appear(t, A("e1", end=True) + 0.3, 0.4), w=210)
    toolcard(cr, t, B["e8"].start + 0.3, B["e9"].end + 0.3, "Claude",
             [("", "End conversation?", "", GREY), ("", "(for rare, abusive chats only)", "", GREY)], y=930)
    toolcard(cr, t, B["e16"].start, B["e17"].end + 0.4, "checkout.js",
             [("213", "const qty = cart.qty", "", GREY), ("214", "total = price * qty", "<- ;", YEL)], y=930)
    toolcard(cr, t, B["e23"].start, tl.total + 1, "terminal",
             [("$", "npm test", "", GREY), ("ok", "All tests passed", "", GREEN)], y=930)
    cue("rain", t, 0.0, tl.total)
    cue("typing", t, 0.0, 1.2)
    cue("hush", t, B["e10"].start - 0.1, B["e10"].end - B["e10"].start + 0.2)
    cue("ding", t, B["e23"].start + 0.1)
    th.hook(cr, t, [("I YELLED AT MY AI", False), ("AT 3 AM", True)], end=A("e1", end=True) + 0.6, y=175, size=84)
    pill_caption(cr, t, tl)
