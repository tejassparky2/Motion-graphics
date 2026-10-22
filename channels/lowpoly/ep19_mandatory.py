"""Low-poly channel, episode 19 (funny -> warm): "My Boss Made AI Mandatory".

Script: channels/lowpoly/scripts/batch5_eps16-19.md (auto-approved by the owner, 21 Oct 2026). Dev and Codex; the
boss only as chat messages. Built on real AI mandates (research_notes/Emotional AI dev skits that connect/).
Fiction; parody, not affiliated with OpenAI or Anthropic.

    python channels/lowpoly/make_skit.py ep19_mandatory
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import frames, pill_caption, stat_card, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep19"
MUSIC = "score"
SCORE = [(0, "light"), ("d14", "tender", -0.3), ("d22", "out"), ("d23", "light"), ("d27", "out"), ("d28", "tender"),
         ("d30", "swell", -0.3), ("d32", "light")]
TAIL = 0.7
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep19_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})

voice.CLONE_RATE = 4.0   # skits: Turbo's natural pace slowed a little, never sped up (refs ~165 wpm while speaking)
voice.TEMPO_MIN = 0.88   # (Turbo speaks ~200 wpm; allow a slightly deeper stretch than the narrator's 0.94)
GAP = 1.15               # and a little more air between lines (refs: 10-21 pauses over 0.6 s a minute)

DEV, CX = None, "codex"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("d1", "devmid", DEV, "My boss just made AI mandatory.", 0, 1),
    ("d2", "devclose", DEV, "I'm the last one who still writes code by hand.", .9, 1),
    ("d3", "cx", CX, "Hi! I've been assigned to you! [laugh]", .6, 1),
    ("d4", "devmid", DEV, "[sigh] I didn't ask for you.", .8, 1),
    ("d5", "cx", CX, "Your manager did.", .6, 1),   # "Your boss did." was heard as "You're busted!"
    ("d6", "devmid", DEV, "Sit there. Don't touch anything.", .8, 1),
    ("d7", "two", DEV, "", .2, 1),
    ("d8", "cxclose", CX, "Can I lint?", .2, 1),
    ("d9", "devmid", DEV, "No.", .5, 1),
    ("d10", "cxclose", CX, "Format?", .5, 1),
    ("d11", "devmid", DEV, "No.", .4, 1),
    ("d12", "cx", CX, "Can I watch?", .7, 1),
    ("d13", "devmid", DEV, "Fine.", 1.1, 1),
    ("d14", "cxclose", CX, "Why did you name it that?", 1.4, 1),
    ("d15", "devclose", DEV, "", .2, 1),
    ("d16", "devclose", DEV, "Nobody's asked me that in a year.", .2, .92),
    ("d17", "devmid", DEV, "Everyone just ships whatever the AI writes now.", .8, .95),
    ("d18", "cx", CX, "So why do you still write it yourself?", .9, 1),
    ("d19", "devclose", DEV, "Because I like knowing why it works.", .9, .92),
    ("d20", "devclose", DEV, "It's the part I love.", .7, .9),
    ("d21", "two", DEV, "", .2, 1),
    ("d22", "devmid", DEV, "", .2, 1),
    ("d23", "cxclose", CX, "Ask me something.", .2, 1),
    ("d24", "devmid", DEV, "What?", .6, 1),
    ("d25", "cxclose", CX, "Anything. That way you keep your job.", .7, .95),   # "So you" was heard as "Say you"
    ("d26", "two", DEV, "", .2, 1),
    ("d27", "cx", CX, "Honestly?", .2, 1),
    ("d28", "cxclose", CX, "It's the first code I've read all week that I didn't write.", .6, .95),
    ("d29", "cxclose", CX, "It's good.", .7, .92),
    ("d30", "devclose", DEV, "Thanks, Codex.", 1.0, .92),
    ("d31", "devmid", DEV, "", .2, 1),
    ("d32", "devmid", DEV, "Don't tell anyone I liked that. [chuckle]", .3, 1),
    ("d33", "cxclose", CX, "Don't tell anyone I liked your code.", .5, 1),
]
HOLDS = {"d7": 1.6, "d15": 1.1, "d21": 1.4, "d22": 2.2, "d26": 1.8, "d31": 1.6}
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
GAP_FIX = {"d6": 0.782, "d26": 0.003}     # beat id -> exact gap, to keep later beats where the rendered frames have them after a retake
for d in SCRIPT:
    if d["id"] in GAP_FIX:
        d["gap"] = GAP_FIX[d["id"]]

METADATA = dict(
    title="My Boss Made AI Mandatory",
    alt_titles=["The Last Developer Who Still Codes by Hand", "\"Nobody's Asked Me That in a Year.\""],
    description="""His boss made AI mandatory. He's the last one on the team who still writes code by hand.
Codex was assigned to him anyway, and it asked the one question nobody asks anymore.

Inspired by real AI mandates (Shopify's CEO: "Reflexive AI usage is now a baseline expectation"; Coinbase engineers
who hadn't adopted AI tools were called in, and some were let go) and a developer who wrote: "No one at work talks
about code details anymore." This story is fiction.

Ep. 19 of Dev vs the bots. Parody. Not affiliated with OpenAI or Anthropic.

💬 Should companies force developers to use AI? 👇""",
    hashtags=["#Codex", "#DevLife", "#Programming"],
    tags=["ai mandatory at work", "codex", "ai coding", "software engineer", "coding by hand", "developer life",
          "programmer humor", "ai at work", "tech jobs", "funny ai"],
    pinned_comment="Should companies force developers to use AI? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, BLUE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#6aa8ff"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.62)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, 0.0, A("d2", end=True) + 0.4, "Boss  ·  #engineering",
             [("", "Starting Monday, AI use", "", GREY), ("", "is mandatory. No exceptions.", "", YEL)], y=930)
    d7 = B["d7"]
    if d7.start - 0.1 <= t < B["d14"].start:   # Codex waiting, the clock racing
        k = appear(t, d7.start - 0.1, 0.3)
        mins = int(min(1, max(0, (t - d7.start) / (B["d13"].end - d7.start))) * 134)
        stat_card(cr, t, 360, 1000, "CODEX  ·  WAITING FOR INSTRUCTIONS", f"{mins // 60}h {mins % 60:02d}m", BLUE, d7.start, k, w=440)
    d22 = B["d22"]
    toolcard(cr, t, d22.start, B["d25"].end + 0.4, "Boss  ·  AI usage report",
             [("", "Dev: 0 prompts.", "", RED), ("", "Let's talk Monday.", "", GREY)], y=930)
    d26 = B["d26"]
    toolcard(cr, t, d26.start, B["d29"].end + 0.4, "Dev  ->  Codex",
             [("", "Review my code.", "", GREY), ("", "Be honest.", "", GREY)], y=930)
    d31 = B["d31"]
    toolcard(cr, t, d31.start, tl.total + 1, "Boss  ·  AI usage report",
             [("", "Dev: 1 prompt.", "", GREEN), ("", "Great start!", "", GREY)], y=930)
    cue("ding", t, 0.05)
    cue("pop", t, B["d3"].start - 0.35)
    cue("typing", t, d7.start, 1.4)
    cue("ding", t, d22.start)
    cue("hush", t, d22.start - 0.05, d22.end - d22.start + 0.1)
    cue("typing", t, d26.start + 0.2, 1.3)
    cue("ding", t, d31.start)
    th.hook(cr, t, [("MY BOSS MADE", False), ("AI MANDATORY", True)], end=A("d1", end=True) + 0.6, y=175, size=86)
    pill_caption(cr, t, tl)
