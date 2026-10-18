"""Low-poly channel, episode 3 (comedy): "I Asked 2 AIs to Fix One Bug".

Script: channels/lowpoly/scripts/ep03_great_point.md (auto-approved by the owner, 18 Oct 2026: "Make next 4 episode
auto approved i will skip which i don't like"). Dev, Claude and Codex. Parody, not affiliated with Anthropic or OpenAI.

    python channels/lowpoly/make_skit.py ep03_great_point
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import banner, caption, frames, stat_card, steps_at, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc, seg   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep03"
MUSIC = "pad"
TAIL = 1.6
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep03_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart"),
                       "codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})

SCRIPT = [
    dict(id="d1", scene="dev", text="The site is down. Both of you. Fix it."),
    dict(id="d2", scene="claude", speaker="claude", text="Codex, would you like to go first?", gap=0.4),
    dict(id="d3", scene="codex", speaker="codex", text="Oh no, Claude. After you!", gap=0.3),
    dict(id="d4", scene="claude", speaker="claude", text="I insist. Your last fix was lovely.", gap=0.3),
    dict(id="d5", scene="codex", speaker="codex", text="Your plan was lovelier!", gap=0.3),
    dict(id="d6", scene="devclose", text="The site. Is. Down.", gap=0.5),
    dict(id="d7", scene="claudeclose", speaker="claude", text="Great point, Dev.", gap=0.4),
    dict(id="d8", scene="codexclose", speaker="codex", text="Such a great point.", gap=0.3),
    dict(id="d9", scene="duo", speaker="claude", text="Codex, your point about his point was great.", gap=0.3),
    dict(id="d10", scene="codex", speaker="codex", text="Thank you! Great point about my point!", gap=0.3),
    dict(id="d11", scene="dev", text="I'll do it myself.", gap=0.6),
    dict(id="d12", scene="ots", text="Fixed. One line.", gap=1.4),
    dict(id="d13", scene="claude", speaker="claude", text="Wow. Great fix, Dev!", gap=0.5),
    dict(id="d14", scene="codex", speaker="codex", text="Such a great fix!", gap=0.3),
    dict(id="d15", scene="duo", speaker="claude", text="Codex, your compliment was great.", gap=0.3),
    dict(id="d16", scene="devclose", text="Not again.", gap=0.6),
]

METADATA = dict(
    title="I Asked 2 AIs to Fix One Bug 😭",
    alt_titles=["Great Point, Codex!", "The Site Is Down (They're Being Polite)"],
    description="""The site is down. I asked Claude AND Codex to fix it. 😭

"After you!" "No, after you!" "Great point!" "Great point about my point!"

7,450 users waiting.

Parody. Not affiliated with Anthropic or OpenAI.

💬 Be honest: which AI do you ask first when the site is down? 👇""",
    hashtags=["#ClaudeCode", "#Codex", "#ProgrammerHumor"],
    tags=["claude", "claude code", "codex", "ai coding", "programmer humor", "coding memes", "site down",
          "developer life", "vibe coding", "ai agents"],
    pinned_comment="Be honest: which AI do you ask first when the site is down? 👇",
)
GREEN, RED, YEL, PINK = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#ffd23f", "#ff8fd2"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.6)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    up = A("d12", "One") - 0.2
    users, ch = steps_at(t, [(0, 1204), (A("d5"), 2310), (A("d6"), 3980), (A("d10"), 7450), (up, 0)])
    k = appear(t, A("d1", end=True) + 0.3, 0.3)
    stat_card(cr, t, 170, 112, "SITE UP" if t >= up else "SITE DOWN · USERS WAITING", f"{users:,}",
              GREEN if t >= up else RED, ch, k)
    comp, cc = steps_at(t, [(0, 0)] + [(A(i), n + 1) for n, i in enumerate(("d4", "d5", "d7", "d8", "d9", "d10", "d13", "d14", "d15"))])
    stat_card(cr, t, 550, 112, "COMPLIMENTS", str(comp), PINK, cc, appear(t, A("d4"), 0.3), w=220)
    toolcard(cr, t, A("d11", end=True) - 0.1, A("d12", end=True) + 0.8, "my-site · prod   Dev ▾",
             [("Edit", "server.js", "+1 −1", GREEN), ("ok", "Site is up", "", GREEN)])
    cue("typing", t, 0.0, 1.4)
    cue("typing", t, A("d11", end=True), 1.1)
    for i in ("d4", "d5", "d7", "d8", "d9", "d10", "d13", "d14", "d15"):
        cue("pop", t, A(i) + 0.05)
    cue("ding", t, up)
    cue("hush", t, A("d12", end=True), 1.2)
    cue("sigh", t, A("d16") - 0.6)
    cue("thud", t, A("d16") + 1.5)
    th.hook(cr, t, [("I ASKED 2 AIs", False), ("TO FIX ONE BUG", True)], end=A("d1", end=True) + 0.3, y=175, size=80)
    caption(cr, t, tl)
