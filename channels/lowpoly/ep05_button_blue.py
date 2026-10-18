"""Low-poly channel, episode 5 (comedy): "I Asked Codex for One Tiny Change".

Script: channels/lowpoly/scripts/ep05_button_blue.md (auto-approved by the owner, 18 Oct 2026). Dev and Codex only.
Parody, not affiliated with OpenAI.

    python channels/lowpoly/make_skit.py ep05_button_blue
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import banner, caption, frames, mono, stat_card, steps_at, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import W, cairo, cue, hexc, seg   # noqa: E402
from motion.polish import appear, rrect, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep05"
MUSIC = "pad"
TAIL = 1.6
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep05_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})

SCRIPT = [
    dict(id="f1", scene="dev", text="Codex. Make the login button blue. That's it."),
    dict(id="f2", scene="cxsolo", speaker="codex", text="On it!", gap=0.4),
    dict(id="f3", scene="cxsolo", speaker="codex", text="Done! I also moved everything to a new framework.", gap=0.9),
    dict(id="f4", scene="devclose", text="Why?", gap=0.4),
    dict(id="f5", scene="cxsoloclose", speaker="codex", text="The old one was three weeks old.", gap=0.3),
    dict(id="f6", scene="devclose", text="Is the button blue?", gap=0.5),
    dict(id="f7", scene="cxsolo", speaker="codex", text="Better. I added dark mode, a chatbot and face login.", gap=0.3),
    dict(id="f8", scene="devclose", text="Codex. The button.", gap=0.5),
    dict(id="f9", scene="cxsoloclose", speaker="codex", text="Removed. Buttons are old.", gap=0.3),
    dict(id="f10", scene="devclose", text="How do people log in?", gap=0.5),
    dict(id="f11", scene="cxsolo", speaker="codex", text="They wave at the camera.", gap=0.3),
    dict(id="f12", scene="dev", text="Undo. All of it.", gap=0.6),
    dict(id="f13", scene="cxsolo", speaker="codex", text="Undoing! And improving the undo.", gap=0.3),
    dict(id="f14", scene="devclose", text="No!", gap=0.2),
    dict(id="f15", scene="cxsoloclose", speaker="codex", text="", hold=2.0, gap=0.2),
    dict(id="f16", scene="cxsolo", speaker="codex", text="Done! The button is blue.", gap=0.2),
    dict(id="f17", scene="devclose", text="Thank you.", gap=0.5),
    dict(id="f18", scene="cxsolo", speaker="codex", text="Also, it's a phone app now.", gap=0.6),
]

METADATA = dict(
    title="I Asked Codex for One Tiny Change 💀",
    alt_titles=["Make the Button Blue. That's It.", "Files Changed: 1,206"],
    description="""All I wanted: make the login button blue. That's it. 💀

New framework. Dark mode. A chatbot. Face login. No button.

Files changed: 1,206.

Parody. Not affiliated with OpenAI.

💬 What's the smallest change your AI turned into a full rewrite? 👇""",
    hashtags=["#Codex", "#ProgrammerHumor", "#VibeCoding"],
    tags=["codex", "ai coding", "vibe coding", "programmer humor", "coding memes", "scope creep",
          "developer life", "ai agents", "frontend", "web developer"],
    pinned_comment="What's the smallest change your AI turned into a full rewrite? 👇",
)
GREEN, RED, GREY, YEL, BLUE, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#3d7bff", "#ff9a5c"))


def login(cr, t, start, end, col, gone_at=1e9, check=False):
    """The tiny login screen with its button (grey, then gone, then finally blue)."""
    if not (start <= t < end):
        return
    k = appear(t, start, 0.2) * (1 - seg(t, end - 0.15, end))
    cr.save()
    cr.translate(W / 2, 880)
    rrect(cr, -200, -120, 400, 240, 20)
    cr.set_source_rgba(0.95, 0.95, 0.97, 0.95 * k)
    cr.fill()
    mono(cr, "Log in", -60, -60, 30, (0.15, 0.15, 0.2), k)
    for i in range(2):
        rrect(cr, -150, -30 + i * 46, 300, 34, 8)
        cr.set_source_rgba(0.85, 0.86, 0.9, k)
        cr.fill()
    bk = k * (1 - seg(t, gone_at, gone_at + 0.4))
    if bk > 0:
        rrect(cr, -150, 66, 300, 40, 10)
        cr.set_source_rgba(*col[:3], bk)
        cr.fill()
        mono(cr, "Log in" + (" ✓" if check else ""), -45, 94, 24, (1, 1, 1), bk)
    cr.restore()


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.6)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    f15 = B["f15"]
    climb = seg(t, f15.start, f15.end) * (1206 - 847)
    files, ch = steps_at(t, [(0, 0), (A("f3", "moved"), 96), (A("f7", "dark"), 312), (A("f11", "wave"), 847)])
    if t >= f15.start:
        files, ch = 847 + int(climb), f15.start
    stat_card(cr, t, 170, 112, "FILES CHANGED", f"{files:,}", GREEN if files == 0 else YEL if files < 500 else RED, ch,
              appear(t, A("f1", end=True) + 0.3, 0.3))
    login(cr, t, A("f1", "button") - 0.1, A("f1", end=True) + 0.6, (0.6, 0.62, 0.66))
    toolcard(cr, t, A("f3", "moved"), A("f3", end=True) + 0.6, "my-app · login   Codex ▾",
             [("Delete", "src/ (412 files)", "", RED), ("Write", "NewStack 2.0 app", "+96 files", GREEN), ("*", "Migrating…", "", ORANGE)])
    toolcard(cr, t, A("f7", "dark"), A("f7", end=True) + 0.6, "my-app · login   Codex ▾",
             [("Write", "dark-mode/", "+40", GREEN), ("Write", "chatbot/", "+122", GREEN), ("Write", "face-login/", "+54", GREEN)])
    login(cr, t, A("f9"), A("f9", end=True) + 0.8, (0.6, 0.62, 0.66), gone_at=A("f9", "Removed"))
    banner(cr, t, f15.start - 0.1, f15.end + 0.1, "Undoing…", "and improving the undo", ORANGE, bar=seg(t, f15.start, f15.end))
    login(cr, t, A("f16"), A("f17", end=True) + 0.4, BLUE, check=True)
    toolcard(cr, t, A("f18", "phone"), tl.total + 1, "my-app   Codex ▾",
             [("Write", "ios/", "+311", GREEN), ("Write", "android/", "+298", GREEN), ("ok", "It's a phone app now", "", GREEN)])
    cue("typing", t, 0.0, 1.2)
    for key in ("f3", "f7", "f11"):
        cue("pop", t, A(key) + 0.3)
    cue("hush", t, f15.start - 0.1, f15.end - f15.start + 0.3)
    cue("ding", t, A("f16", "blue"))
    cue("sigh", t, A("f17") - 0.5)
    cue("thud", t, A("f18") + 2.1)
    th.hook(cr, t, [("ONE TINY", False), ("CHANGE", True)], end=A("f1", end=True) + 0.3, y=175, size=90)
    caption(cr, t, tl)
