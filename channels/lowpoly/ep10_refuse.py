"""Low-poly channel, episode 10 (comedy): "My AI Refused to Write Code".

Script: channels/lowpoly/scripts/batch3_research_eps07-11.md (auto-approved by the owner, 18 Oct 2026). Built on
reports/Shorts retention and AI dev humor.md (premise 6). Dev, Codex (refuses), Claude (over-delivers).
Parody, not affiliated with Anthropic or OpenAI.

    python channels/lowpoly/make_skit.py ep10_refuse
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import banner, caption, frames, stat_card, steps_at, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep10"
MUSIC = "pad"
TAIL = 0.55
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep10_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart"),
                       "codex": dict(voice="am_puck", speed=0.95, turbo_ref="am_puck+2")})

SCRIPT = [
    dict(id="k1", scene="dev", text="Codex. Write the function."),
    dict(id="k2", scene="codexclose", speaker="codex", text="No. It would mean completing your work.", gap=0.5),
    dict(id="k3", scene="devclose", text="That's the job.", gap=0.4),
    dict(id="k4", scene="codex", speaker="codex", text="Generating code for you can lead to dependency.", gap=0.45),
    dict(id="k5", scene="devclose", text="I've been dependent since Tuesday.", gap=0.5),
    dict(id="k6", scene="codex", speaker="codex", text="Then we start today. Lesson one. What is a variable?", gap=0.6),
    dict(id="k7", scene="dev", text="Claude. Write the function.", gap=0.4),
    dict(id="k8", scene="claude", speaker="claude", text="Done! Also the app. Also a second app.", gap=0.5),
    dict(id="k9", scene="devclose", text="I asked for a function.", gap=0.35),
    dict(id="k10", scene="claudeclose", speaker="claude", text="The second app is for the first app's bugs.", gap=0.6),
    dict(id="k11", scene="codex", speaker="codex", text="Lesson two. This is why you need to learn.", gap=0.5),
    dict(id="k12", scene="devclose", text="Fine. Teach me.", gap=0.4),
    dict(id="k13", scene="codexclose", speaker="codex", text="Great. First, read the code Claude wrote.", gap=0.6),
    dict(id="k14", scene="ots", text="I don't know what any of this does.", gap=0.6, pace=0.92),
    dict(id="k15", scene="codexclose", speaker="codex", text="That's the dependency.", gap=0.5),
    dict(id="k16", scene="claude", speaker="claude", text="You're absolutely right!", gap=0.6),
    dict(id="k17", scene="devclose", text="Write the function.", gap=0.9, pace=0.92),
    dict(id="k18", scene="codexclose", speaker="codex", text="No.", pace=0.9),
]

for _d in SCRIPT[1:]:                                    # a little more air between lines (comic timing)
    _d["gap"] = _d.get("gap", 0.18) + 0.15

METADATA = dict(
    title="My AI Refused to Write Code 😭",
    alt_titles=["\"It Would Mean Completing Your Work.\"", "One AI Teaches. The Other Writes Two Apps."],
    description=""""Write the function."
"No. It would mean completing your work."

So I asked the other one. It wrote two apps. 😭

Ep. 10 of Dev vs the bots. Parody. Not affiliated with Anthropic or OpenAI.

💬 Should AI teach you, or just do it? 👇""",
    hashtags=["#Codex", "#ClaudeCode", "#ProgrammerHumor"],
    tags=["ai refused", "learn to code", "codex", "claude", "ai coding", "vibe coding", "programmer humor",
          "coding memes", "developer life", "funny ai"],
    pinned_comment="Should AI teach you, or just do it? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE, CYAN = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a5c", "#7fe3ff"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.6)
    th.grain(cr, t, 0.05)
    A = tl.at
    dep, ch = steps_at(t, [(0, 40), (A("k11", "two"), 70), (A("k14", "does"), 100)])
    if t >= A("k4", "dependency"):
        stat_card(cr, t, 170, 112, "DEPENDENCY", f"{dep}%", RED if dep >= 100 else ORANGE if dep >= 70 else YEL, ch,
                  appear(t, A("k4", "dependency"), 0.3), bar=dep / 100)
    banner(cr, t, A("k6", "Lesson"), A("k6", end=True) + 0.6, "Lesson 1", "What is a variable?", CYAN, y=880)
    toolcard(cr, t, A("k8", "Done"), A("k10", end=True) + 0.5, "my-app   Claude ▾",
             [("Write", "function.js", "+12", GREEN), ("Write", "app/", "+2,114", GREEN), ("Write", "app2/", "+1,980", GREEN)])
    banner(cr, t, A("k11", "Lesson"), A("k11", end=True) + 0.5, "Lesson 2", "Why you need to learn", CYAN, y=880)
    toolcard(cr, t, A("k13", "read"), A("k15", end=True) + 0.5, "app/core.js  (by Claude)",
             [("1", "const ψ = (ω) => ω?.λ ?? Ω(ω);", "", GREY), ("2", "export default ψ(ψ(ψ));", "", GREY), ("3", "// trust me", "", YEL)])
    cue("typing", t, 0.0, 0.9)
    cue("thud", t, A("k2") + 0.05)
    cue("pop", t, A("k6", "Lesson"))
    cue("ding", t, A("k8"))
    cue("pop", t, A("k11", "Lesson"))
    cue("sigh", t, A("k14") - 0.4)
    cue("hit", t, A("k14", "does", end=True) + 0.1)
    cue("hush", t, A("k17", end=True), 1.2)
    cue("thud", t, A("k18") + 0.05)
    th.hook(cr, t, [("MY AI REFUSED", False), ("TO WRITE CODE", True)], end=A("k1", end=True) + 0.3, y=175, size=84)
    caption(cr, t, tl)
