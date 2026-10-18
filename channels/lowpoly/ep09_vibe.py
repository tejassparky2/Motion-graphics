"""Low-poly channel, episode 9 (comedy, warm turn): "I Built an App in an Hour. Nobody Knows How It Works."

Script: channels/lowpoly/scripts/batch3_research_eps07-11.md (auto-approved by the owner, 18 Oct 2026). Built on
reports/Shorts retention and AI dev humor.md (premise 8). Dev and Claude only. Parody, not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep09_vibe
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import caption, frames, mono, stat_card, steps_at, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import W, cue, hexc, seg   # noqa: E402
from motion.polish import appear, rrect, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep09"
MUSIC = "pad"
TAIL = 0.55
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep09_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart")})

SCRIPT = [
    dict(id="j1", scene="dev", text="I built this in an hour. Watch."),
    dict(id="j2", scene="devclose", text="Why does the button do that?", gap=0.45),
    dict(id="j3", scene="soloclose", speaker="claude", text="I don't know either.", gap=0.5),
    dict(id="j4", scene="devclose", text="You wrote it.", gap=0.35),
    dict(id="j5", scene="solo", speaker="claude", text="I wrote it very fast.", gap=0.5),
    dict(id="j6", scene="dev", text="Fix it.", gap=0.4),
    dict(id="j7", scene="solo", speaker="claude", text="Fixed. Two new buttons do that now.", gap=0.6),
    dict(id="j8", scene="devclose", text="What does line forty-two do?", gap=0.4),
    dict(id="j9", scene="soloclose", speaker="claude", text="Nobody knows. Including line forty-two.", gap=0.6),
    dict(id="j10", scene="devclose", text="Did it work yesterday?", gap=0.35),
    dict(id="j11", scene="solo", speaker="claude", text="Yesterday it had different bugs.", gap=0.6),
    dict(id="j12", scene="dev", text="Start over. Same app. Clean.", gap=0.5),
    dict(id="j13", scene="solo", speaker="claude", text="Done. It's in a different language now.", gap=0.5),
    dict(id="j14", scene="devclose", text="Why?", gap=0.35),
    dict(id="j15", scene="soloclose", speaker="claude", text="The old one had bugs.", gap=0.7),
    dict(id="j16", scene="devclose", text="I used to understand my own code.", gap=0.7, pace=0.92),
    dict(id="j17", scene="soloclose", speaker="claude", text="You could write one line. By hand.", gap=0.5),
    dict(id="j18", scene="ots", text="", hold=1.6, gap=0.3),
    dict(id="j19", scene="solo", speaker="claude", text="There's a bug in it.", gap=0.5),
    dict(id="j20", scene="devclose", text="I know. It's mine.", gap=0.6, pace=0.92),
    dict(id="j21", scene="solo", speaker="claude", text="Shall I fix it?", gap=0.7),
    dict(id="j22", scene="devclose", text="No.", pace=0.9),
]

METADATA = dict(
    title="I Built an App in an Hour. Nobody Knows How It Works.",
    alt_titles=["Vibe Coding Is Easy. Vibe Debugging Isn't.", "\"What Does Line 42 Do?\" \"Nobody Knows.\""],
    description="""I built an app in an hour. Then I asked what line 42 does.

"Nobody knows. Including line 42."

Ep. 9 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 Vibe coding: freedom, or a trap? 👇""",
    hashtags=["#VibeCoding", "#ClaudeCode", "#ProgrammerHumor"],
    tags=["vibe coding", "vibe debugging", "claude", "ai coding", "programmer humor", "coding memes",
          "learning to code", "developer life", "software bugs", "funny ai"],
    pinned_comment="Vibe coding: freedom, or a trap? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE, BLUE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a5c", "#7fb4ff"))


def app_window(cr, t, start, end, buttons, run_from=None):
    """A little app mock-up; its button slides away from the cursor (that's the bug)."""
    if not (start <= t < end):
        return
    k = appear(t, start, 0.2) * (1 - seg(t, end - 0.15, end))
    cr.save()
    cr.translate(W / 2, 880)
    rrect(cr, -220, -120, 440, 240, 18)
    cr.set_source_rgba(0.96, 0.96, 0.98, 0.95 * k)
    cr.fill()
    mono(cr, "My App", -200, -80, 26, (0.15, 0.15, 0.2), k)
    for i in range(buttons):
        slide = 0
        if run_from is not None and t >= run_from:
            slide = 150 * min(1, (t - run_from) * 2.5) * (1 if i % 2 == 0 else -1)
        rrect(cr, -140 + slide + (i * 20), -20 + i * 50, 280, 38, 10)
        cr.set_source_rgba(*BLUE[:3], k)
        cr.fill()
        mono(cr, "Save", -30 + slide + i * 20, 6 + i * 50, 22, (1, 1, 1), k)
    cr.restore()


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.65)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    bugs, ch = steps_at(t, [(0, 1), (A("j7", "Two"), 3), (A("j11", "different"), 7), (A("j13", "different"), 12), (B["j18"].start + 1.0, 1)])
    stat_card(cr, t, 170, 112, "BUGS", str(bugs), GREEN if bugs <= 1 else YEL if bugs < 6 else RED, ch,
              appear(t, A("j2"), 0.3))
    lang, lch = steps_at(t, [(0, "JavaScript"), (A("j13", "language"), "Go")])
    if t >= A("j13", "different"):
        stat_card(cr, t, 550, 112, "LANGUAGE", lang, ORANGE, lch, appear(t, A("j13", "different"), 0.25), w=220)
    app_window(cr, t, A("j1", "Watch"), A("j3", end=True) + 0.3, 1, run_from=A("j1", end=True) + 0.1)
    app_window(cr, t, A("j7", "Two"), A("j7", end=True) + 0.6, 3, run_from=A("j7", "Two") + 0.3)
    toolcard(cr, t, A("j8", "forty"), A("j9", end=True) + 0.5, "app.js",
             [("41", "const x = y ?? z ?? w;", "", GREY), ("42", "x && (x = !x || x);", "← ?", YEL), ("43", "// TODO: understand 42", "", GREY)])
    toolcard(cr, t, A("j13", "Done"), A("j15", end=True) + 0.4, "my-app   Claude ▾",
             [("Delete", "app.js", "", RED), ("Write", "main.go", "+3,402", GREEN), ("ok", "Same app. Different bugs.", "", GREEN)])
    toolcard(cr, t, B["j18"].start + 0.2, tl.total + 1, "main.go  (by Dev)",
             [("1", 'fmt.Println("hello")', "", GREEN), ("", "▌", "", GREY)])
    cue("typing", t, 0.0, 1.0)
    cue("pop", t, A("j1", end=True) + 0.1)
    cue("pop", t, A("j7", "Two") + 0.3)
    cue("hit", t, A("j13", "different"))
    cue("sigh", t, A("j16") - 0.4)
    cue("hush", t, A("j16") - 0.2, B["j18"].end - A("j16") + 0.6)
    cue("typing", t, B["j18"].start + 0.2, 1.1)
    cue("ding", t, B["j18"].start + 1.0)
    cue("hush", t, A("j21", end=True), 1.2)
    th.hook(cr, t, [("I BUILT AN APP", False), ("IN ONE HOUR", True)], end=A("j1", end=True) + 0.3, y=175, size=84)
    caption(cr, t, tl)
