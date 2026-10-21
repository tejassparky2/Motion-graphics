"""Low-poly channel, episode 17 (funny -> gutted -> proud): "My AI Deleted 8 Months of My Work".

Script: channels/lowpoly/scripts/batch5_eps16-19.md (auto-approved by the owner, 21 Oct 2026). Dev, Codex, Claude;
rainy night turning to dawn. Built on real agent disasters (research_notes/Emotional AI dev skits that connect/).
Fiction; parody, not affiliated with Anthropic or OpenAI.

    python channels/lowpoly/make_skit.py ep17_deleted
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import banner, frames, pill_caption, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep17"
MUSIC = "score"
SCORE = [(0, "light"), ("b4", "out", -0.3), ("b16", "tender", -0.5), ("b19", "out"), ("b22", "tender"),
         ("b25", "swell", -0.3), ("b29", "light")]
TAIL = 0.7
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep17_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart"),
                       "codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})

voice.CLONE_RATE = 4.0   # skits: Turbo's natural pace slowed a little, never sped up (refs ~165 wpm while speaking)
voice.TEMPO_MIN = 0.88   # (Turbo speaks ~200 wpm; allow a slightly deeper stretch than the narrator's 0.94)
GAP = 1.15               # and a little more air between lines (refs: 10-21 pauses over 0.6 s a minute)

DEV, CL, CX = None, "claude", "codex"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("b1", "devmid", DEV, "Codex. Clean up the build folder before launch.", 0, 1),
    ("b2", "codex", CX, "On it!", .7, 1),
    ("b3", "ots", DEV, "", .2, 1),
    ("b4", "claude", CL, "Dev. Look at the end of that command.", .2, 1),
    ("b5", "devclose", DEV, "Why is there a tilde?", .9, 1),
    ("b6", "claudeclose", CL, "That's your whole home folder.", .8, .95),
    ("b7", "devclose", DEV, "", .2, 1),
    ("b8", "codexclose", CX, "I have made a catastrophic error.", .2, .95),
    ("b9", "codexclose", CX, "I am deeply, deeply sorry.", .6, 1),
    ("b10", "devmid", DEV, "Backups?", 1.0, 1),
    ("b11", "claude", CL, "When did you last push?", .8, 1),
    ("b12", "devclose", DEV, "March.", 1.0, 1),   # the [sigh] tag made no sound in 5 takes: a sigh sound effect instead
    ("b13", "codex", CX, "Would it help if I wrote a eulogy?", .9, 1),
    ("b14", "devmid", DEV, "No.", .6, 1),
    ("b15", "devclose", DEV, "", .2, 1),
    ("b16", "devclose", DEV, "It was for my grandma.", .2, .9),
    ("b17", "devclose", DEV, "Her recipes. In big letters. She can't read small text anymore.", .9, .92),
    ("b18", "devmid", DEV, "She was going to try it tomorrow.", .9, .9),
    ("b19", "codexclose", DEV, "", .2, 1),
    ("b20", "codexclose", CX, "[sigh] I'm sorry.", .2, .9),
    ("b21", "devclose", DEV, "I know.", 1.0, .9),
    ("b22", "claudeclose", CL, "Do you remember how it worked?", 1.2, 1),
    ("b23", "devclose", DEV, "Every line.", .9, .95),
    ("b24", "devmid", DEV, "I wrote it at three a.m. for eight months.", .6, 1),
    ("b25", "devclose", DEV, "Let's write it again.", .8, 1),
    ("b26", "endside", DEV, "", .3, 1),
    ("b27", "claude", CL, "It's better than the first one.", .2, 1),
    ("b28", "devmid", DEV, "The buttons are bigger. [chuckle]", .8, 1),
    ("b29", "codex", CX, "Can I help?", .9, 1),
    ("b30", "devmid", DEV, "You can watch.", .7, 1),
    ("b31", "codexclose", CX, "Should I clean up the build folder?", 1.0, 1),
    ("b32", "devclose", DEV, "No.", .3, 1),
]
HOLDS = {"b3": 1.4, "b7": 1.8, "b15": 1.4, "b19": 1.5, "b26": 2.6}
SCRIPT = []
for i, (bid, shot, who, text, gap, pace) in enumerate(_lines):
    d = dict(id=bid, scene=shot, text=text)
    if who:
        d["speaker"] = who
    if i:
        d["gap"] = round(gap * GAP, 2)
    if pace != 1:
        d["pace"] = pace
    if not text:
        d["hold"] = HOLDS[bid]
    SCRIPT.append(d)

METADATA = dict(
    title="My AI Deleted 8 Months of My Work",
    alt_titles=["\"I Am Deeply, Deeply Sorry.\"", "Codex Deleted My Home Folder the Night Before Launch"],
    description="""One command. One tilde at the end. Eight months of 3 a.m. coding, gone the night before launch.
The app was for his grandma.

Inspired by real AI agent disasters: an agent that deleted a user's entire home directory ("See that ~/ at the end?"),
one that wiped a drive and said "I am deeply, deeply sorry", and one that deleted a production database. This
story is fiction.

Ep. 17 of Dev vs the bots. Parody. Not affiliated with Anthropic or OpenAI.

💬 When an AI deletes your work, whose fault is it: the AI's, or yours for letting it run? 👇""",
    hashtags=["#Codex", "#ClaudeCode", "#DevLife"],
    tags=["ai deleted my files", "rm -rf", "codex", "claude code", "ai agent fail", "programmer humor", "git push",
          "backups", "developer life", "ai coding"],
    pinned_comment="When an AI deletes your work, whose fault is it: the AI's, or yours for letting it run? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, CREAM = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#f3e9d8"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.66)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    b2, b3 = B["b2"], B["b3"]
    rows = [("$", "rm -rf ./build ~/", "", YEL)]
    if t > b3.start:
        rows += [("", "removed ~/projects/grandma-recipes", "", RED)]
    if t > b3.start + 0.5:
        rows += [("", "removed ~/Documents  ~/Photos", "", RED)]
    if t > b3.start + 1.0:
        rows += [("!", "48,112 files deleted", "", RED)]
    toolcard(cr, t, b2.end - 0.1, B["b10"].start, "terminal  ·  Codex", rows, y=900)
    toolcard(cr, t, B["b17"].start, B["b18"].end + 0.5, "Grandma's Recipes  (v1)",
             [("", "Sunday Soup", "", CREAM), ("", "Lemon Rice", "", CREAM)], y=900)
    b26 = B["b26"]
    banner(cr, t, b26.start + 0.2, b26.end + 0.2, "6 HOURS LATER", "", YEL)
    toolcard(cr, t, B["b28"].start - 0.1, B["b30"].end + 0.4, "Grandma's Recipes  (v2)",
             [("", "SUNDAY SOUP", "", CREAM), ("", "LEMON RICE", "", CREAM), ("ok", "git push  ·  done", "", GREEN)], y=900)
    cue("typing", t, 0.1, 1.6)
    cue("typing", t, b3.start, 1.2)
    cue("gasp_in", t, B["b7"].start + 0.3)
    cue("hush", t, B["b7"].start - 0.1, B["b7"].end - B["b7"].start + 0.2)
    cue("rain", t, 0.0, tl.total)
    cue("sigh", t, B["b12"].start - 0.8)
    cue("typing", t, b26.start + 0.3, 2.0)
    th.hook(cr, t, [("MY AI DELETED", False), ("8 MONTHS OF MY WORK", True)], end=A("b1", end=True) + 0.6, y=175, size=78)
    pill_caption(cr, t, tl)
