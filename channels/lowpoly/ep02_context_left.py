"""Low-poly channel, episode 2 (comedy): "When Your AI Forgets the Whole Project".

Script: channels/lowpoly/scripts/ep02_context_left.md, option B (owner approved 18 Oct 2026: "B approved, render it"):
Dev and Codex, then Claude pops up for the last beat. Original story; parody, not affiliated with OpenAI or Anthropic.
3D picture: scene_skit.html?dir=ep02ctx (directions/ep02ctx.js); this module adds the hook, the "Context left" card,
the compacting and usage-limit banners, tool cards, captions and sound.

    python channels/lowpoly/make_skit.py ep02_context_left
"""
import math
import os

from importlib import util as _u
from motion import thriller as th, voice
from motion.engine import FPS, W, cairo, cue, hexc, seg
from motion.polish import WHITE, appear, bold_text, rrect, vignette

_spec = _u.spec_from_file_location("lp_ep01ar", os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep01_absolutely_right.py"))
_ep = _u.module_from_spec(_spec)
_spec.loader.exec_module(_ep)
toolcard, caption, mono = _ep.toolcard, _ep.caption, _ep.mono      # same tool-log cards and captions as episode 1

NARRATOR = dict(turbo=True, turbo_ref="am_michael")      # Dev: male voice (owner, 17 Oct)
DIRECTION = "ep02ctx"
MUSIC = "pad"
TAIL = 1.2
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build",
                      "lowpoly", "ep02ctx_frames")

voice.SPEAKERS.update({
    "claude": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart"),
    "codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2"),
})

SCRIPT = [
    dict(id="c1", scene="dev", text="Codex. Last bug. Then we ship."),
    dict(id="c2", scene="codex", speaker="codex", text="Sure! Remind me what we're building?", gap=0.4),
    dict(id="c3", scene="devclose", text="The app. We've been on it for three hours.", gap=0.5),
    dict(id="c4", scene="codex", speaker="codex", text="Right! The to-do app!", gap=0.35),
    dict(id="c5", scene="devclose", text="It's a food delivery app.", gap=0.6),
    dict(id="c6", scene="codexclose", speaker="codex", text="Got it! A food delivery to-do app.", gap=0.35),
    dict(id="c7", scene="dev", text="Just fix the login button.", gap=0.6),
    dict(id="c8", scene="codex", speaker="codex", text="Which login? I see three.", gap=0.35),
    dict(id="c9", scene="devclose", text="The one you made an hour ago.", gap=0.4),
    dict(id="c10", scene="codexclose", speaker="codex", text="I don't remember an hour ago.", gap=0.4),
    dict(id="c11", scene="codexcu", speaker="codex", text="", hold=2.4, gap=0.2),
    dict(id="c12", scene="codex", speaker="codex", text="Hi! I'm Codex. What are we building today?", gap=0.2),
    dict(id="c13", scene="devclose", text="You were there. You were there!", gap=0.5),
    dict(id="c14", scene="dev", text="Okay. One message. Fix the login button.", gap=0.8),
    dict(id="c15", scene="codex", speaker="codex", text="On it!", gap=0.35),
    dict(id="c16", scene="ots", speaker="codex", text="", hold=2.0, gap=0.5),
    dict(id="c17", scene="devclose", text="No. No, no, no.", gap=0.2),
    dict(id="c18", scene="codex", speaker="codex", text="See you in five hours!", gap=0.35),
    dict(id="c19", scene="dev", text="Fine. Claude. Help me.", gap=1.1),
    dict(id="c20", scene="claudepop", speaker="claude", text="Hi! I'm Claude. What are we building today?", gap=0.6),
    dict(id="c21", scene="endside", text="", hold=2.6, gap=0.4),
]

METADATA = dict(
    title="When Your AI Forgets the Whole Project 😭",
    alt_titles=["Context Left: 0%", "My AI Hit the Usage Limit at the Worst Time"],
    description="""3 hours. Same chat. One last bug. 😭

"Remind me what we're building?"
"A food delivery to-do app."
"Compacting conversation…"
"Usage limit reached."

So I asked the other AI.

Parody. Not affiliated with OpenAI or Anthropic.

💬 What's worse: your AI forgetting everything, or the usage limit? 👇""",
    hashtags=["#Codex", "#ClaudeCode", "#ProgrammerHumor"],
    tags=["codex", "claude", "claude code", "context window", "usage limit", "ai coding", "vibe coding",
          "programmer humor", "coding memes", "developer life"],
    pinned_comment="What's worse: your AI forgetting everything, or the usage limit? 👇",
)

ORANGE, GREEN, RED, GREY, YEL, CYAN = (hexc(c) for c in ("#ff9a5c", "#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#7fe3ff"))
_n_frames = []


def _frame(t):
    if not _n_frames:
        _n_frames.append(len(os.listdir(FRAMES)))
    i = min(int(round(t * FPS)), _n_frames[0] - 1)
    return cairo.ImageSurface.create_from_png(os.path.join(FRAMES, f"f{i:05d}.png"))


def context_card(cr, t, tl):
    """The running gag: "CONTEXT LEFT n%" top-left, draining on Codex's lines; at the end it's about Dev."""
    A, B = tl.at, tl.by_id
    steps = [(0, 9), (A("c2"), 7), (A("c4"), 5), (A("c6"), 4), (A("c8"), 3), (A("c10"), 1), (A("c12"), 100),
             (A("c15"), 97), (B["c21"].start + 0.4, 0)]
    val, last = 9, 0.0
    for at, v in steps:
        if t >= at:
            val, last = v, at
    dev = t >= B["c21"].start + 0.4
    gone = A("c19") <= t < B["c21"].start + 0.4          # Codex is off: card slides away
    k = 1 - seg(t, A("c19"), A("c19") + 0.3) if gone else appear(t, B["c21"].start + 0.4, 0.3) if dev else 1
    k *= appear(t, A("c1", end=True) + 0.3, 0.3)          # comes in once the hook text has gone
    if k <= 0:
        return
    col = RED if val <= 3 else YEL if val < 50 else GREEN
    blink = 0.35 if val == 1 and math.sin(t * 16) > 0 else 1.0
    if A("c11") - 0.2 <= t < B["c11"].end:                # compacting: the number scrambles
        val = int(abs(math.sin(t * 23)) * 99)
    cr.save()
    cr.translate(170, 112)
    rrect(cr, -138, -52, 276, 104, 18)
    cr.set_source_rgba(0.06, 0.06, 0.09, 0.9 * k)
    cr.fill_preserve()
    cr.set_source_rgba(*col[:3], 0.9 * k)
    cr.set_line_width(3)
    cr.stroke()
    cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(19)
    cr.move_to(-118, -20)
    cr.set_source_rgba(0.75, 0.77, 0.82, k)
    cr.show_text("DEV'S CONTEXT LEFT" if dev else "CONTEXT LEFT")
    cr.restore()
    cr.save()
    cr.translate(170, 142)
    bump = 1 + 0.25 * math.exp(-(t - last) * 9)
    cr.scale(bump, bump)
    bold_text(cr, f"{val}%", 0, 0, 52, col, outline=None, shadow=0)
    cr.restore()
    cr.save()                                             # the meter bar
    cr.set_source_rgba(1, 1, 1, 0.12 * k)
    rrect(cr, 50, 166, 240, 8, 4)
    cr.fill()
    cr.set_source_rgba(*col[:3], 0.9 * k * blink)
    rrect(cr, 50, 166, max(6, 240 * val / 100), 8, 4)
    cr.fill()
    cr.restore()


def banner(cr, t, start, end, title, sub, col, bar=None, y=860):
    """A big system banner (compacting, usage limit)."""
    if not (start <= t < end):
        return
    k = appear(t, start, 0.15) * (1 - seg(t, end - 0.15, end))
    cr.save()
    cr.translate(W / 2, y)
    s = 0.9 + 0.1 * k
    cr.scale(s, s)
    rrect(cr, -310, -78, 620, 156, 22)
    cr.set_source_rgba(0.08, 0.07, 0.1, 0.95 * k)
    cr.fill_preserve()
    cr.set_source_rgba(*col[:3], k)
    cr.set_line_width(4)
    cr.stroke()
    cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(34)
    ext = cr.text_extents(title)
    cr.move_to(-ext.x_advance / 2, -14)
    cr.set_source_rgba(*col[:3], k)
    cr.show_text(title)
    cr.set_font_size(24)
    ext = cr.text_extents(sub)
    cr.move_to(-ext.x_advance / 2, 28)
    cr.set_source_rgba(0.8, 0.82, 0.86, k)
    cr.show_text(sub)
    if bar is not None:
        cr.set_source_rgba(1, 1, 1, 0.12 * k)
        rrect(cr, -250, 46, 500, 10, 5)
        cr.fill()
        cr.set_source_rgba(*col[:3], k)
        rrect(cr, -250, 46, max(8, 500 * bar), 10, 5)
        cr.fill()
    cr.restore()


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.6)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    T = "food-app · login   Codex ▾"
    toolcard(cr, t, A("c8", "Which"), A("c8", end=True) + 0.8, T,
             [("Read", "login.js", "", GREY), ("Read", "login_new.js", "", GREY), ("Read", "login_FINAL.js", "", YEL)])
    c11 = B["c11"]
    banner(cr, t, c11.start - 0.1, c11.end + 0.15, "Compacting conversation…", "summarising 3 hours of chat",
           CYAN, bar=seg(t, c11.start, c11.end - 0.2))
    toolcard(cr, t, A("c15"), B["c16"].start + 0.1, T, [("Read", "login_FINAL.js", "", GREY), ("*", "Fixing login…", "", ORANGE)])
    c16 = B["c16"]
    banner(cr, t, c16.start, A("c18", end=True) + 0.2, "Usage limit reached", "Resets in 4h 59m", RED)
    context_card(cr, t, tl)

    cue("typing", t, 0.0, 1.8)
    cue("typing", t, A("c14", "Fix"), 1.4)
    for key in ("c2", "c4", "c6", "c8", "c10"):
        cue("pop", t, A(key) + 0.05)
    cue("hush", t, c11.start - 0.1, c11.end - c11.start + 0.3)
    cue("ding", t, A("c12") + 0.05)
    cue("sigh", t, A("c14") - 0.7)
    cue("hush", t, c16.start, c16.end - c16.start + 0.2)
    cue("hit", t, c16.start + 0.05)
    cue("gasp_in", t, A("c17") - 0.35)
    cue("hush", t, B["c21"].start + 0.3, 2.0)
    cue("thud", t, B["c21"].start + 1.55)
    th.hook(cr, t, [("3 HOURS.", False), ("SAME CHAT.", True)], end=A("c1", end=True) + 0.3, y=175, size=84)
    caption(cr, t, tl)
