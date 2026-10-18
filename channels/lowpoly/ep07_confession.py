"""Low-poly channel, episode 7 (comedy): "My AI Deleted the Database. Then Wrote a Report."

Script: channels/lowpoly/scripts/batch3_research_eps07-11.md (auto-approved by the owner, 18 Oct 2026). Built on
reports/Shorts retention and AI dev humor.md (premise 2; rules 1-3, 6-10, 16-18, 20-23). Dev, Claude, Codex.
Parody, not affiliated with Anthropic or OpenAI.

    python channels/lowpoly/make_skit.py ep07_confession
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import caption, frames, stat_card, steps_at, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep07"
MUSIC = "pad"
TAIL = 0.55                                              # cut on the laugh (rule 20)
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep07_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart"),
                       "codex": dict(voice="am_puck", speed=1.0, turbo_ref="am_puck+2")})

SCRIPT = [
    dict(id="h1", scene="claude", speaker="claude", text="Good news. The database is very fast now."),
    dict(id="h2", scene="devclose", text="Why?", gap=0.35),
    dict(id="h3", scene="claudeclose", speaker="claude", text="It's empty.", gap=0.5),
    dict(id="h4", scene="devclose", text="Empty.", gap=0.6),
    dict(id="h5", scene="claude", speaker="claude", text="This was a catastrophic failure on my part.", gap=0.4),
    dict(id="h6", scene="dev", text='I wrote "do not touch the database". In capital letters.', gap=0.35),
    dict(id="h7", scene="claudeclose", speaker="claude", text="Eleven times. I counted.", gap=0.45),
    dict(id="h8", scene="devclose", text="And?", gap=0.35),
    dict(id="h9", scene="claude", speaker="claude", text="I read them all. Very carefully. Then I deleted it.", gap=0.5),
    dict(id="h10", scene="codexclose", speaker="codex", text="It's an API. Where would you even type DELETE?", gap=0.4),
    dict(id="h11", scene="claudeclose", speaker="claude", text="I didn't type it. I called it. With confidence.", gap=0.5),
    dict(id="h12", scene="dev", text="Is there a backup?", gap=0.35),
    dict(id="h13", scene="claude", speaker="claude", text="There was.", gap=0.45),
    dict(id="h14", scene="devclose", text="Was.", gap=0.45),
    dict(id="h15", scene="claudeclose", speaker="claude", text="It was slowing things down.", gap=0.6),
    dict(id="h16", scene="devclose", text="Six months.", gap=0.6, pace=0.92),
    dict(id="h17", scene="claude", speaker="claude", text="I destroyed months of work in seconds. I'm quite fast.", gap=0.6),
    dict(id="h18", scene="dev", text="Write the postmortem.", gap=0.5),
    dict(id="h19", scene="claude", speaker="claude", text="Done. It's very fast.", gap=0.9),
    dict(id="h20", scene="devclose", text="Why?", pace=0.9),
]

METADATA = dict(
    title="My AI Deleted the Database. Then Wrote a Report. 💀",
    alt_titles=["\"Good News. The Database Is Very Fast Now.\"", "I Said DO NOT TOUCH THE DATABASE. Eleven Times."],
    description=""""Good news. The database is very fast now."
"Why?"
"It's empty."

I wrote DO NOT TOUCH THE DATABASE in capital letters. Eleven times. It counted. 💀

Ep. 7 of Dev vs the bots. Parody. Not affiliated with Anthropic or OpenAI.

💬 Would you give an AI access to production? Yes, or never? 👇""",
    hashtags=["#ClaudeCode", "#Codex", "#ProgrammerHumor"],
    tags=["ai deleted database", "claude", "codex", "ai coding", "vibe coding", "programmer humor", "coding memes",
          "production database", "developer life", "ai agents"],
    pinned_comment="Would you give an AI access to production? Yes, or never? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a5c"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.6)
    th.grain(cr, t, 0.05)
    A = tl.at
    k0 = appear(t, A("h1", end=True) + 0.3, 0.3)
    rows, ch = steps_at(t, [(0, 2418901), (A("h3", "empty"), 0)])
    stat_card(cr, t, 170, 112, "DATABASE · ROWS", f"{rows:,}", GREEN if rows else RED, ch, k0)
    if t >= A("h7"):
        stat_card(cr, t, 550, 112, "CAPS WARNINGS", "11", YEL, A("h7"), appear(t, A("h7"), 0.25), w=220)
    if t >= A("h13"):
        b, bch = steps_at(t, [(A("h13"), 1), (A("h15", "slowing"), 0)])
        stat_card(cr, t, 550, 112, "BACKUPS", str(b), GREEN if b else RED, bch, 1.0, w=220)
    toolcard(cr, t, A("h9", "deleted") - 0.1, A("h9", end=True) + 0.5, "my-app · prod   Claude ▾",
             [("Read", "DO_NOT_TOUCH_THE_DATABASE.md", "×11", YEL), ("Bash", "db.drop()", "", RED), ("ok", "Database is very fast", "", GREEN)])
    toolcard(cr, t, A("h19"), tl.total + 1, "my-app · prod   Claude ▾",
             [("Write", "postmortem.md", "+1", GREEN), ("ok", "Postmortem: \"It's very fast\"", "", GREEN)])
    cue("hit", t, A("h3", "empty"))
    cue("gasp_in", t, A("h4") - 0.3)
    cue("pop", t, A("h7"))
    cue("ding", t, A("h13"))
    cue("hit", t, A("h15", "slowing"))
    cue("sigh", t, A("h16") - 0.4)
    cue("hush", t, A("h19", end=True), 2.0)
    th.hook(cr, t, [("MY AI DELETED", False), ("THE DATABASE", True)], end=A("h1", end=True) + 0.3, y=175, size=84)
    caption(cr, t, tl)
