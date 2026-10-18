"""Low-poly channel, episode 6 (comedy): "Explain It Like I'm Five".

Script: channels/lowpoly/scripts/ep06_simpler.md (auto-approved by the owner, 18 Oct 2026). Dev and Claude; Codex
pops up for the answer. Parody, not affiliated with Anthropic or OpenAI.

    python channels/lowpoly/make_skit.py ep06_simpler
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import caption, frames, mono, stat_card, steps_at, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep06"
MUSIC = "pad"
TAIL = 1.4
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep06_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart"),
                       "codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})

SCRIPT = [
    dict(id="g1", scene="dev", text="Claude. What does this error mean?"),
    dict(id="g2", scene="claude", speaker="claude", text="The parser hit an unexpected token while reading the payload.", gap=0.4),
    dict(id="g3", scene="devclose", text="Simpler.", gap=0.5),
    dict(id="g4", scene="claude", speaker="claude", text="The computer read your data and got confused.", gap=0.3),
    dict(id="g5", scene="devclose", text="Simpler.", gap=0.5),
    dict(id="g6", scene="claudeclose", speaker="claude", text="Computer read. Computer confused.", gap=0.3),
    dict(id="g7", scene="devclose", text="Simpler!", gap=0.5),
    dict(id="g8", scene="claudeclose", speaker="claude", text="Computer. Sad.", gap=0.5),
    dict(id="g9", scene="dev", text="Okay. Why is computer sad?", gap=0.8),
    dict(id="g10", scene="codex", speaker="codex", text="You forgot a comma. Line four.", gap=0.6),
    dict(id="g11", scene="devclose", text="That's it?", gap=0.4),
    dict(id="g12", scene="codexclose", speaker="codex", text="That's it.", gap=0.3),
    dict(id="g13", scene="dev", text="Claude. Why didn't you just say that?", gap=0.6),
    dict(id="g14", scene="claudeclose", speaker="claude", text="You said simpler.", gap=0.4),
    dict(id="g15", scene="devclose", text="", hold=1.6, gap=0.2),
    dict(id="g16", scene="claude", speaker="claude", text="Computer. Happy now.", gap=0.2),
]

METADATA = dict(
    title="Explain It Like I'm Five 😭",
    alt_titles=["Computer. Sad.", "I Asked Claude to Explain My Error Simpler"],
    description=""""Unexpected token in JSON at position 4021." Okay but what does it MEAN? 😭

Simpler. Simpler. SIMPLER.

"Computer. Sad."

Parody. Not affiliated with Anthropic or OpenAI.

💬 Do you want AI to explain like a senior dev, or like you're five? 👇""",
    hashtags=["#ClaudeCode", "#Codex", "#ProgrammerHumor"],
    tags=["claude", "codex", "explain like im five", "json error", "ai coding", "programmer humor",
          "coding memes", "learning to code", "vibe coding", "developer life"],
    pinned_comment="Do you want AI to explain like a senior dev, or like you're five? 👇",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a5c"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.65)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    simp, ch = steps_at(t, [(0, 0), (A("g2"), 10), (A("g4"), 45), (A("g6"), 80), (A("g8"), 100)])
    stat_card(cr, t, 170, 112, "SIMPLICITY", f"{simp}%", ORANGE, ch, appear(t, A("g2"), 0.3), bar=simp / 100)
    toolcard(cr, t, A("g1", "error") - 0.1, A("g2", end=True) + 0.5, "terminal",
             [("✗", "Unexpected token }", "", RED), ("", "in JSON at position 4021", "", RED)])
    toolcard(cr, t, A("g10", "comma"), A("g12", end=True) + 0.8, "data.json  line 4",
             [("3", '"name": "Dev"', "", GREY), ("4", '"age": 22', "← ,", YEL), ("5", '"job": "developer"', "", GREY)])
    for key in ("g3", "g5", "g7"):
        cue("pop", t, A(key) + 0.05)
    cue("hush", t, A("g8"), 1.0)
    cue("ding", t, A("g10", "comma"))
    cue("hush", t, B["g15"].start - 0.1, B["g15"].end - B["g15"].start + 0.3)
    th.hook(cr, t, [("EXPLAIN IT", False), ("LIKE I'M FIVE", True)], end=A("g1", end=True) + 0.3, y=175, size=84)
    caption(cr, t, tl)
