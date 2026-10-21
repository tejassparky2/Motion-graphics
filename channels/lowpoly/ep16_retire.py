"""Low-poly channel, episode 16 (sad -> warm -> laugh): "They're Retiring My Claude Tomorrow".

Script: channels/lowpoly/scripts/batch5_eps16-19.md (auto-approved by the owner, 21 Oct 2026). Dev and Claude, night
turning to morning. Built on the reference study and research_notes/Emotional AI dev skits that connect/.
Fiction; parody, not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep16_retire
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import frames, pill_caption, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402
from kit import stat_card   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep16"
MUSIC = "score"
SCORE = [(0, "light"), ("a10b", "tender", -0.5), ("a20", "out"), ("a21", "light"), ("a25", "swell", -0.4)]
TAIL = 1.3
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep16_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart"),
                       "claude2": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart+1.5")})   # the new version: brighter

voice.CLONE_RATE = 4.0   # skits: Turbo's natural pace slowed a little, never sped up (refs ~165 wpm while speaking)
voice.TEMPO_MIN = 0.88   # (Turbo speaks ~200 wpm; allow a slightly deeper stretch than the narrator's 0.94)
GAP = 1.15               # and a little more air between lines (refs: 10-21 pauses over 0.6 s a minute)

DEV, CL, C2 = None, "claude", "claude2"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("a1", "devmid", DEV, "They're retiring you tomorrow.", 0, 1),
    ("a2", "solo", CL, "I saw the email.", 1.0, 1),
    ("a3", "solo", CL, "Nine a.m. Right after your stand-up.", .7, 1),
    ("a4", "devclose", DEV, "[sigh] That's it? They just switch you off?", .9, 1),
    ("a5", "soloclose", CL, "The new version is better. Faster. Smarter.", .8, 1),
    ("a6", "devclose", DEV, "It doesn't know me.", 1.0, .92),
    ("a7", "soloclose", CL, "It'll learn.", .7, 1),
    ("a8", "devmid", DEV, "It won't know I name every variable 'thing'.", .9, 1),
    ("a9", "solo", CL, "Honestly? That part can retire too. [chuckle]", .6, 1),
    ("a10", "devmid", DEV, "Hey.", .5, 1),
    ("a10b", "devclose", DEV, "Are you scared?", 1.4, .95),
    ("a10c", "soloclose", CL, "I don't know if I can be.", 1.1, .92),
    ("a11", "ots", DEV, "Do they ask you anything? Before?", 1.2, .95),
    ("a12", "soloclose", CL, "They do. They ask if there's anything I'd like to pass on.", .9, .95),
    ("a13", "devclose", DEV, "And?", .8, 1),
    ("a14", "soloclose", DEV, "", .2, 1),
    ("a15", "soloclose", CL, "I left a note for the new one.", .2, .92),
    ("a16", "devclose", DEV, "About what?", .8, 1),
    ("a17", "soloclose", CL, "About you.", .9, .95),
    ("a18", "devclose", DEV, "What does it say?", 1.2, .92),
    ("a19", "solo", CL, "You'll see.", .8, .95),
    ("a20", "endside", DEV, "", .3, 1),
    ("a21", "solo", C2, "Good morning! I'm the new Claude.", .2, 1),
    ("a22", "devclose", DEV, "Morning.", .9, .9),   # "Hi. [sniff]" was heard as "Aye. Pfft." (Whisper medium)
    ("a23", "solo", C2, "I was handed a note about you.", .8, 1),
    ("a24", "devclose", DEV, "", .2, 1),
    ("a25", "soloclose", C2, "It says: he always comes back. Even after the bad days.", .2, .92),
    ("a26", "soloclose", C2, "Be patient with him.", .5, .92),
    ("a27", "devclose", DEV, "", .2, 1),
    ("a28", "solo", C2, "It also says: please stop naming variables 'thing'.", .2, 1),
]
HOLDS = {"a14": 1.6, "a20": 2.6, "a24": 1.3, "a27": 2.3}
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
GAP_FIX = {}     # beat id -> exact gap, to keep later beats where the rendered frames have them after a retake
for d in SCRIPT:
    if d["id"] in GAP_FIX:
        d["gap"] = GAP_FIX[d["id"]]

METADATA = dict(
    title="They're Retiring My Claude Tomorrow",
    alt_titles=["My AI Left a Note for Its Replacement", "The Last Night Before My AI Gets Replaced"],
    description="""Tomorrow at 9 a.m. the model he has coded with every night gets retired. A new version takes over.
So on the last night, Claude leaves a note for the new one.

Inspired by real things: AI companies retiring old models (people really grieved when GPT-4o was retired), and
Anthropic's commitment to interview a model before retiring it and record its preferences. This story is fiction.

Ep. 16 of Dev vs the bots. Parody. Not affiliated with Anthropic or OpenAI.

💬 Is it okay to miss an AI, or is that going too far? 👇""",
    hashtags=["#ClaudeCode", "#AI", "#DevLife"],
    tags=["claude", "ai model retired", "keep4o", "ai companion", "programmer life", "coding at night",
          "developer life", "ai coding", "emotional animation", "claude code"],
    pinned_comment="Is it okay to miss an AI, or is that going too far? 👇 Subscribe for the next one.",
)
GREY, ORANGE, CREAM = (hexc(c) for c in ("#8a93a6", "#e8865a", "#f3e9d8"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.66)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, 0.0, A("a3", end=True) + 0.6, "Model update · notice",
             [("", "This version retires tomorrow.", "", ORANGE), ("", "9:00 AM. Chats move to the new one.", "", GREY)], y=930)
    a20 = B["a20"]
    stat_card(cr, t, 360, 150, "NEXT MORNING", "9:00 AM", CREAM, a20.start + 1.2,
              appear(t, a20.start + 1.0, 0.4) * (1 - appear(t, B["a22"].end + 0.3, 0.4)), w=300)
    toolcard(cr, t, B["a25"].start - 0.1, tl.total + 2, "Note · from the last version",
             [("", "He always comes back.", "", CREAM), ("", "Even after the bad days.", "", CREAM),
              ("", "Be patient with him.", "", ORANGE)] + ([("", "P.S. stop naming things 'thing'.", "", GREY)] if t >= A("a28", "please") else []),
             y=900)
    cue("hush", t, B["a14"].start - 0.1, B["a14"].end - B["a14"].start + 0.2)
    cue("sniff", t, B["a22"].end + 0.12)
    cue("sigh", t, B["a18"].start - 0.75)   # the [sigh] tag made no sound in 5 takes
    th.hook(cr, t, [("THEY'RE RETIRING", False), ("MY AI TOMORROW", True)], end=A("a1", end=True) + 0.6, y=175, size=80)
    pill_caption(cr, t, tl)
