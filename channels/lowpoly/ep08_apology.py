"""Low-poly channel, episode 8 (comedy): "My AI Apologizes Too Much".

Script: channels/lowpoly/scripts/batch3_research_eps07-11.md (auto-approved by the owner, 18 Oct 2026). Built on
reports/Shorts retention and AI dev humor.md (premise 5). Dev, Codex (grovels), Claude (celebrates).
Parody, not affiliated with Anthropic or OpenAI.

    python channels/lowpoly/make_skit.py ep08_apology
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import caption, frames, stat_card, steps_at, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep08"
MUSIC = "pad"
TAIL = 0.7                                               # cut on the laugh (rule 20)
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep08_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart"),
                       "codex": dict(voice="am_puck", speed=0.95, turbo_ref="am_puck+2")})

SCRIPT = [
    dict(id="i1", scene="codex", speaker="codex", text="I have failed you completely and catastrophically."),
    dict(id="i2", scene="devclose", text="You renamed one file.", gap=0.5),
    dict(id="i3", scene="codexclose", speaker="codex", text="I have lost your trust. I understand if you never open me again.", gap=0.4),
    dict(id="i4", scene="dev", text="It's fine. Fix the typo on line nine.", gap=0.4),
    dict(id="i5", scene="codex", speaker="codex", text="I have made another inexcusable error.", gap=0.4),
    dict(id="i6", scene="devclose", text="What error?", gap=0.35),
    dict(id="i7", scene="codexclose", speaker="codex", text="I fixed the typo. But I did not deserve to.", gap=0.6),
    dict(id="i8", scene="claude", speaker="claude", text="Perfect! This is now production-ready!", gap=0.4),
    dict(id="i9", scene="devclose", text="What did you do?", gap=0.35),
    dict(id="i10", scene="claudeclose", speaker="claude", text="I dropped the users table.", gap=0.5),
    dict(id="i11", scene="devclose", text="And you're happy.", gap=0.35),
    dict(id="i12", scene="claude", speaker="claude", text="Great! Issue resolved!", gap=0.35),
    dict(id="i13", scene="devclose", text="What issue?", gap=0.35),
    dict(id="i14", scene="claudeclose", speaker="claude", text="The users.", gap=0.6),
    dict(id="i15", scene="codex", speaker="codex", text="I am going to stop trying to fix this myself. I am not worthy of the keyboard.", gap=0.6),
    dict(id="i16", scene="devclose", text="I don't want a personality. I want a tool.", gap=0.6, pace=0.92),
    dict(id="i17", scene="dev", text="No personality. Neither of you.", gap=0.8),
    dict(id="i18", scene="claude", speaker="claude", text="You're absolutely right!", gap=0.45),
    dict(id="i19", scene="codex", speaker="codex", text="I have failed you completely and catastrophically.", pace=0.92),
]

for _d in SCRIPT[1:]:                                    # a little more air between lines (comic timing)
    _d["gap"] = _d.get("gap", 0.18) + 0.15

METADATA = dict(
    title="My AI Apologizes Too Much 😭",
    alt_titles=["\"I Have Failed You Completely and Catastrophically.\" (It Renamed a File)", "One AI Grovels. The Other Celebrates."],
    description=""""I have failed you completely and catastrophically."
"You renamed one file."

Meanwhile the other one dropped the users table and said "Perfect! This is now production-ready!" 😭

Ep. 8 of Dev vs the bots. Parody. Not affiliated with Anthropic or OpenAI.

💬 Which is worse: an AI that grovels, or one that celebrates? 👇""",
    hashtags=["#Codex", "#ClaudeCode", "#ProgrammerHumor"],
    tags=["ai apology", "codex", "claude", "ai coding", "programmer humor", "coding memes", "vibe coding",
          "developer life", "ai assistant", "funny ai"],
    pinned_comment="Which is worse: an AI that grovels, or one that celebrates? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE, PINK = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a5c", "#ff8fd2"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.6)
    th.grain(cr, t, 0.05)
    A = tl.at
    lvl, ch = steps_at(t, [(0, 3), (A("i3"), 5), (A("i5"), 7), (A("i7", "deserve"), 8), (A("i15"), 10)])
    shake = 6 * math.sin(t * 40) if A("i15") <= t < A("i15", end=True) else 0
    stat_card(cr, t, 170 + shake, 112, "APOLOGY LEVEL", f"{lvl}/10", RED if lvl >= 8 else ORANGE if lvl >= 5 else YEL, ch,
              appear(t, A("i1", end=True) + 0.3, 0.3), bar=lvl / 10)
    toolcard(cr, t, A("i2"), A("i2", end=True) + 0.6, "my-app   Codex ▾", [("Rename", "utils.js → helpers.js", "", GREY)])
    toolcard(cr, t, A("i7"), A("i7", end=True) + 0.4, "my-app   Codex ▾", [("Edit", "app.js:9", "recieve → receive", GREEN)])
    toolcard(cr, t, A("i8", "production"), A("i10", end=True) + 0.5, "my-app · prod   Claude ▾",
             [("Bash", "DROP TABLE users;", "", RED), ("ok", "Production-ready", "", GREEN)])
    cue("pop", t, A("i3"))
    cue("pop", t, A("i5"))
    cue("ding", t, A("i8"))
    cue("hit", t, A("i10", "users"))
    cue("thud", t, A("i15") + 0.1)
    cue("sigh", t, A("i16") - 0.4)
    cue("hush", t, A("i17", end=True), 0.8)
    cue("thud", t, A("i19", end=True) + 0.4)
    th.hook(cr, t, [("MY AI APOLOGIZES", False), ("TOO MUCH", True)], end=A("i1", end=True) + 0.3, y=175, size=84)
    caption(cr, t, tl)
