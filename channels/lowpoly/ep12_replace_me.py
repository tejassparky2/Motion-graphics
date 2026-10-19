"""Low-poly channel, episode 12 (warm, then a laugh): "I Asked My AI If It's Going to Replace Me".

Script: channels/lowpoly/scripts/ep12_replace_me.md (owner approved 19 Oct 2026: "Approved, render it"). Replaces
episode 3. Dev and Claude only. Grounded in the research's job-fear and lost-joy threads. Parody, not affiliated
with Anthropic.

    python channels/lowpoly/make_skit.py ep12_replace_me
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import caption, frames, stat_card, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep12"
MUSIC = "pad"
TAIL = 0.6
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep12_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.95, turbo_ref="af_heart")})

SCRIPT = [
    dict(id="n1", scene="devphone", text="They cut half the team today."),
    dict(id="n2", scene="soloclose", speaker="claude", text="Are you okay?", gap=0.8),
    dict(id="n3", scene="devclose", text="I'm still here. For now.", gap=0.6),
    dict(id="n4", scene="devclose", text="Be honest. Are you here to replace me?", gap=0.6),
    dict(id="n5", scene="clcu", speaker="claude", text="I don't know.", gap=1.2, pace=0.92),
    dict(id="n6", scene="devclose", text="That's not very comforting.", gap=0.6),
    dict(id="n7", scene="solo", speaker="claude", text="You asked me to be honest.", gap=0.5),
    dict(id="n8", scene="devclose", text="I used to love this job.", gap=0.9, pace=0.92),
    dict(id="n9", scene="soloclose", speaker="claude", text="What did you love about it?", gap=0.6),
    dict(id="n10", scene="devclose", text="The moment it finally works. After hours of nothing.", gap=0.6, pace=0.94),
    dict(id="n11", scene="soloclose", speaker="claude", text="When did you last feel that?", gap=0.6),
    dict(id="n12", scene="devcu", text="", hold=1.3, gap=0.3),
    dict(id="n13", scene="devcu", text="Before you.", gap=0.2, pace=0.88),
    dict(id="n14", scene="clcu", speaker="claude", text="Then I'll leave this one for you.", gap=1.5, pace=0.94),
    dict(id="n15", scene="devclose", text="What?", gap=0.5),
    dict(id="n16", scene="soloclose", speaker="claude", text="Line forty. It's all yours.", gap=0.5),
    dict(id="n17", scene="ots", text="", hold=2.6, gap=0.5),
    dict(id="n18", scene="devcu", text="There it is.", gap=0.4, pace=0.9),
    dict(id="n19", scene="soloclose", speaker="claude", text="I can fix it. I can't feel it for you.", gap=0.9, pace=0.94),
    dict(id="n20", scene="solo", speaker="claude", text="Also. I left you three more.", gap=1.0),
    dict(id="n21", scene="devclose", text="Don't touch them.", gap=0.5),
]

METADATA = dict(
    title="I Asked My AI If It's Going to Replace Me",
    alt_titles=["\"They Cut Half the Team Today.\"", "My AI Left Me a Bug on Purpose"],
    description="""2 AM. They cut half the team today. So I asked my AI the question.

"Are you here to replace me?"
"I don't know."

Ep. 12 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 Is AI taking the joy out of coding, or giving it back? 👇""",
    hashtags=["#ClaudeCode", "#DevLife", "#Coding"],
    tags=["ai replacing developers", "layoffs", "claude", "ai coding", "developer life", "coding motivation",
          "software engineer", "programmer", "learning to code", "tech layoffs"],
    pinned_comment="Is AI taking the joy out of coding, or giving it back? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.68)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    stat_card(cr, t, 150, 112, "TIME", "2:14 AM", GREY, 0, appear(t, A("n1", end=True) + 0.4, 0.4), w=210)
    toolcard(cr, t, A("n1", "half") - 0.1, A("n3", end=True) + 0.3, "#general · 6:02 PM",
             [("", "Today we said goodbye to", "", GREY), ("", "half of the engineering team.", "", RED)], y=880)
    toolcard(cr, t, A("n16", "forty"), B["n17"].start + 0.4, "app.js", [("40", "if (user = null) {", "← bug", YEL)])
    n17 = B["n17"]
    toolcard(cr, t, n17.start + 0.3, n17.start + 1.4, "app.js  (Dev)", [("40", "if (user === null) {", "", GREEN)])
    toolcard(cr, t, n17.start + 1.4, A("n19", end=True) + 0.3, "terminal",
             [("$", "npm test", "", GREY), ("ok", "All tests passed", "", GREEN)])
    toolcard(cr, t, A("n20", "three"), tl.total + 1, "bugs left for Dev",
             [("12", "lol = undefined", "", YEL), ("88", "while (true) {", "", YEL), ("131", "// TODO: Dev", "", YEL)])
    cue("hush", t, B["n12"].start - 0.1, A("n14", end=True) - B["n12"].start + 1.2)
    cue("typing", t, n17.start + 0.2, 1.0)
    cue("ding", t, n17.start + 1.4)
    cue("pop", t, A("n20", "three"))
    th.hook(cr, t, [("THEY CUT HALF", False), ("THE TEAM TODAY", True)], end=A("n1", end=True) + 0.4, y=175, size=84)
    caption(cr, t, tl)
