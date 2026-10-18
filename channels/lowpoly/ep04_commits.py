"""Low-poly channel, episode 4 (warm): "I Told Claude I'm Not a Real Developer".

Script: channels/lowpoly/scripts/ep04_commits.md (auto-approved by the owner, 18 Oct 2026). Dev and Claude only.
Parody, not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep04_commits
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import caption, frames, mono, stat_card, steps_at, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import W, cairo, cue, hexc, seg   # noqa: E402
from motion.polish import appear, rrect, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep04"
MUSIC = "pad"
TAIL = 1.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep04_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.95, turbo_ref="af_heart")})

SCRIPT = [
    dict(id="e1", scene="devclose", text="Claude. I'm not a real developer."),
    dict(id="e2", scene="soloclose", speaker="claude", text="What happened?", gap=0.6),
    dict(id="e3", scene="dev", text="It crashed. Again. Everyone else knows what they're doing.", gap=0.5),
    dict(id="e4", scene="solo", speaker="claude", text="Can I show you something?", gap=0.7),
    dict(id="e5", scene="ots", speaker="claude", text="Your commits this year.", gap=0.4),
    dict(id="e6", scene="devclose", text="Most of them just say fix.", gap=0.8),
    dict(id="e7", scene="soloclose", speaker="claude", text="Fixes are still commits.", gap=0.5),
    dict(id="e8", scene="solo", speaker="claude", text="And this one. March. Your first.", gap=0.7),
    dict(id="e9", scene="devclose", text="I was so scared to push that.", gap=0.8),
    dict(id="e10", scene="soloclose", speaker="claude", text="You pushed it anyway.", gap=0.6),
    dict(id="e11", scene="devclose", text="", hold=1.8, gap=0.3),
    dict(id="e12", scene="dev", text="Okay. What's the crash?", gap=0.3),
    dict(id="e13", scene="solo", speaker="claude", text="A missing semicolon.", gap=0.4),
    dict(id="e14", scene="devclose", text="Of course it is.", gap=0.4),
    dict(id="e15", scene="dev", text="Push it.", gap=0.5),
    dict(id="e16", scene="soloclose", speaker="claude", text="Commits this year. One thousand two hundred fifteen.", gap=0.9),
]

METADATA = dict(
    title="I Told Claude I'm Not a Real Developer",
    alt_titles=["1,214 Commits That Say 'fix'", "3 AM. Another Crash."],
    description="""3 AM. Another crash. "I'm not a real developer."

Then Claude showed me my commits. 1,214 of them. Most just say "fix".

"Fixes are still commits."

Parody. Not affiliated with Anthropic.

💬 Be honest: how many of your commits just say "fix"? 👇""",
    hashtags=["#ClaudeCode", "#ImposterSyndrome", "#DevLife"],
    tags=["claude", "claude code", "imposter syndrome", "developer", "learning to code", "git commit",
          "vibe coding", "programmer", "self taught developer", "coding motivation"],
    pinned_comment="Be honest: how many of your commits just say \"fix\"? 👇",
)
GREEN, RED, GREY, YEL, DIM = (hexc(c) for c in ("#5fd17a", "#ff5c5c", "#8a93a6", "#ffd23f", "#1e3a26"))


def graph(cr, t, start, end, extra_at):
    """A year of commit squares (most green), with the count; one more lights up at extra_at."""
    if not (start <= t < end):
        return
    k = appear(t, start, 0.25) * (1 - seg(t, end - 0.2, end))
    cr.save()
    cr.translate(W / 2, 860)
    rrect(cr, -320, -110, 640, 220, 20)
    cr.set_source_rgba(0.08, 0.09, 0.11, 0.95 * k)
    cr.fill()
    mono(cr, "commits · 2026", -296, -72, 22, GREY, k)
    import random
    rnd = random.Random(4)
    grow = seg(t, start, start + 1.2)
    for c in range(26):
        for r in range(7):
            on = rnd.random() < 0.82 and c / 26 <= grow
            last = c == 25 and r == 3
            col = (GREEN if t >= extra_at else DIM) if last else (GREEN if on else DIM)
            a = 0.35 + 0.65 * rnd.random() if on else 1
            rrect(cr, -296 + c * 22.5, -52 + r * 18, 18, 14, 3)
            cr.set_source_rgba(*col[:3], a * k)
            cr.fill()
    cr.restore()


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.65)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    push = A("e15", end=True) + 0.2
    n, ch = steps_at(t, [(0, 1214), (push, 1215)])
    stat_card(cr, t, 170, 112, "COMMITS THIS YEAR", f"{n:,}", GREEN, ch, appear(t, A("e5"), 0.3))
    graph(cr, t, A("e5"), A("e6", "fix"), 1e9)
    toolcard(cr, t, A("e6", "fix"), A("e7", end=True) + 0.4, "git log --oneline",
             [("a91f2c", "fix", "", GREY), ("3be07d", "fix again", "", GREY), ("77c1e9", "fix fix", "", GREY),
              ("0d4a18", "final fix", "", GREY), ("e52b6f", "fix (real)", "", GREY)], y=880)
    toolcard(cr, t, A("e8", "March"), A("e10", end=True) + 0.6, "first commit · Mar 2026",
             [("1a2b3c", "hello world (please work)", "", YEL)])
    toolcard(cr, t, A("e13"), A("e14", end=True) + 0.4, "app.js  line 42",
             [("−", "const total = price * qty", "", RED), ("+", "const total = price * qty;", "", GREEN)])
    toolcard(cr, t, A("e15"), A("e16") - 0.3, "terminal",
             [("$", 'git commit -m "fix"', "", GREY), ("$", "git push", "", GREY), ("ok", "pushed", "", GREEN)])
    graph(cr, t, A("e16") - 0.3, tl.total + 1, push + 0.4)
    cue("hush", t, B["e11"].start - 0.2, B["e11"].end - B["e11"].start + 0.4)
    cue("sigh", t, A("e1") - 0.1)
    cue("typing", t, A("e15", end=True) - 0.1, 0.8)
    cue("ding", t, push)
    th.hook(cr, t, [("3 AM.", False), ("ANOTHER CRASH.", True)], end=A("e1", end=True) + 0.3, y=175, size=84)
    caption(cr, t, tl)
