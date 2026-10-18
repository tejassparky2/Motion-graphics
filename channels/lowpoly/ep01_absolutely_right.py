"""Low-poly channel, episode 1 (comedy): "I Tried to Make Claude Disagree With Me".

Script: channels/lowpoly/scripts/ep01_absolutely_right.md (owner approved 18 Oct 2026: "Approved, render it i want
detailed emotional real dev feel"). Dev and Claude only (owner, 18 Oct: never Claude and Codex together). Original
story; parody, not affiliated with Anthropic. 3D picture: scene_skit.html?dir=ep01ar (directions/ep01ar.js); this
module adds the hook, the "absolutely right" counter, the Thinking chip, code panels, captions and sound.

    python channels/lowpoly/make_skit.py ep01_absolutely_right
"""
import math
import os

from motion import thriller as th, voice
from motion.engine import FPS, W, cairo, cue, hexc, seg
from motion.polish import WHITE, appear, bold_text, rrect, vignette

from importlib import util as _u
_spec = _u.spec_from_file_location("lp_ep01", os.path.join(os.path.dirname(os.path.abspath(__file__)), "ep01_code_review.py"))
_ep1 = _u.module_from_spec(_spec)
_spec.loader.exec_module(_ep1)
panel, mono, clean_caption = _ep1.panel, _ep1.mono, _ep1.clean_caption      # same panels and captions as before

NARRATOR = dict(turbo=True, turbo_ref="am_michael")      # Dev: male voice (owner, 17 Oct)
DIRECTION = "ep01ar"
MUSIC = "pad"
TAIL = 1.8                                               # room for the head hitting the desk
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build",
                      "lowpoly", "ep01ar_frames")

voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart")})

AR = "You're absolutely right!"
SCRIPT = [
    dict(id="a1", scene="dev", text="Claude. This line is wrong."),
    dict(id="a2", scene="claude", speaker="claude", text=f"{AR} Fixing it.", gap=0.4),
    dict(id="a3", scene="devclose", text="Wait. It was fine before.", gap=0.5),
    dict(id="a4", scene="claude", speaker="claude", text=f"{AR} Putting it back.", gap=0.35),
    dict(id="a5", scene="dev", text="Okay. The bug is in the [C S S.|CSS.]", gap=0.6),
    dict(id="a6", scene="claude", speaker="claude", text=f"{AR} Rewriting the [C S S.|CSS.]", gap=0.35),
    dict(id="a7", scene="devclose", text="There is no [C S S.|CSS.]", gap=0.6),
    dict(id="a8", scene="claudeclose", speaker="claude", text=f"{AR} Creating the [C S S.|CSS.]", gap=0.35),
    dict(id="a9", scene="devlean", text="Just once. Tell me I'm wrong.", gap=0.7),
    dict(id="a10", scene="claudecu", speaker="claude", text="", hold=2.2, gap=0.2),
    dict(id="a11", scene="claude", speaker="claude", text="You're absolutely right. You're wrong.", gap=0.2),
    dict(id="a12", scene="devclose", text="Okay. Last one. Am I a good programmer?", gap=0.9),
    dict(id="a13", scene="claudecu", speaker="claude", text="", hold=3.2, gap=0.2),
    dict(id="a14", scene="claudeclose", speaker="claude", text="Let's look at that loop again.", gap=0.2),
    dict(id="a15", scene="devclose", text="You hesitated.", gap=0.8),
    dict(id="a16", scene="claude", speaker="claude", text=AR, gap=0.35),
]

METADATA = dict(
    title="I Tried to Make Claude Disagree With Me 😭",
    alt_titles=["Claude Agrees With EVERYTHING", "You're Absolutely Right! (6 Times)"],
    description="""2:47 AM. One bug. I just wanted Claude to tell me I was wrong. Once. 😭

"This line is wrong." You're absolutely right!
"It was fine before." You're absolutely right!
"There is no CSS." You're absolutely right!

Then I asked if I'm a good programmer.

Parody. Not affiliated with Anthropic or OpenAI.

💬 How many times has your AI said "You're absolutely right" today? 👇""",
    hashtags=["#ClaudeCode", "#ProgrammerHumor", "#DevLife"],
    tags=["claude", "claude code", "you're absolutely right", "ai coding", "programmer humor", "coding memes",
          "developer life", "software engineer", "ai agrees with everything", "vibe coding"],
    pinned_comment="How many times has your AI said \"You're absolutely right\" today? 👇",
)

ORANGE, GREEN, RED, GREY, YEL, PINK, BLUE = (hexc(c) for c in ("#ff9a5c", "#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f",
                                                               "#ff79c6", "#7fb4ff"))
_n_frames = []


def _frame(t):
    if not _n_frames:
        _n_frames.append(len(os.listdir(FRAMES)))
    i = min(int(round(t * FPS)), _n_frames[0] - 1)
    return cairo.ImageSurface.create_from_png(os.path.join(FRAMES, f"f{i:05d}.png"))


def counter(cr, t, tl, hits):
    """The running gag: a small card top-left, "Absolutely right: N", ticking up with a bump on each one."""
    if t < hits[0]:
        return
    n = sum(t >= h for h in hits)
    last = max(h for h in hits if t >= h)
    k = appear(t, hits[0], 0.25)
    bump = 1 + 0.25 * math.exp(-(t - last) * 9)
    flick = 1.0
    a13 = tl.by_id["a13"]
    if a13.start <= t < a13.end:                    # it flickers while Claude can't answer
        flick = 0.35 if math.sin(t * 31) * math.sin(t * 7.3) > 0.3 else 1.0
    cr.save()
    cr.translate(150, 112)
    rrect(cr, -118, -52, 236, 104, 18)
    cr.set_source_rgba(0.06, 0.06, 0.09, 0.88 * k * flick)
    cr.fill_preserve()
    cr.set_source_rgba(*ORANGE[:3], 0.9 * k * flick)
    cr.set_line_width(3)
    cr.stroke()
    cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(19)
    cr.move_to(-100, -20)
    cr.set_source_rgba(0.75, 0.77, 0.82, k * flick)
    cr.show_text("ABSOLUTELY RIGHT")
    cr.restore()
    cr.save()
    cr.translate(150, 140)
    cr.scale(bump, bump)
    bold_text(cr, str(n), 0, 0, 54, ORANGE, outline=None, shadow=0)
    cr.restore()


def thinking(cr, t, beat):
    """Claude's "Thinking…" chip while it can't bring itself to answer (dots cycling, a timer counting)."""
    if not (beat.start <= t < beat.end + 0.1):
        return
    k = appear(t, beat.start, 0.2)
    cr.save()
    cr.translate(W / 2, 300)
    rrect(cr, -150, -36, 300, 72, 36)
    cr.set_source_rgba(0.08, 0.08, 0.11, 0.9 * k)
    cr.fill_preserve()
    cr.set_source_rgba(*ORANGE[:3], 0.7 * k)
    cr.set_line_width(2.5)
    cr.stroke()
    for i in range(3):                               # three dots bouncing in turn
        y = -6 * max(0, math.sin(t * 7 - i * 0.9))
        cr.arc(-108 + i * 18, 4 + y, 5, 0, 2 * math.pi)
        cr.set_source_rgba(*ORANGE[:3], k)
        cr.fill()
    cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(28)
    cr.move_to(-58, 12)
    cr.set_source_rgba(0.93, 0.93, 0.95, k)
    cr.show_text("Thinking")
    cr.set_font_size(20)
    cr.move_to(72, 11)
    cr.set_source_rgba(0.6, 0.62, 0.68, k)
    cr.show_text(f"{t - beat.start:0.0f}s")
    cr.restore()


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.6)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id

    def diff(old_first):
        def body(cr, k, top):
            rows = [("- ", "for (i = 0; i <= 10; i++)", RED), ("+ ", "for (i = 0; i < 10; i++)", GREEN)]
            if not old_first:
                rows = [("- ", "for (i = 0; i < 10; i++)", RED), ("+ ", "for (i = 0; i <= 10; i++)", GREEN)]
            mono(cr, "app.js  line 42", -280, top + 60, 24, GREY, k)
            for j, (sign, code, col) in enumerate(rows):
                x = -280 + mono(cr, sign, -280, top + 115 + j * 50, 30, col, k)
                mono(cr, code, x, top + 115 + j * 50, 28, col, k)
        return body
    panel(cr, t, A("a2", "Fixing"), A("a2", end=True) + 0.5, diff(True), h=210)
    panel(cr, t, A("a4", "Putting"), A("a4", end=True) + 0.5, diff(False), h=210)

    def css(cr, k, top):
        mono(cr, "styles.css", -280, top + 80, 34, BLUE, k)
        n = int(2000 * min(1, seg(t, A("a6", "Rewriting"), A("a6", end=True))))
        mono(cr, f"{n:,} lines changed", -280, top + 140, 32, YEL, k)
    panel(cr, t, A("a6", "Rewriting"), A("a6", end=True) + 0.5, css, h=190)

    def newfile(cr, k, top):
        mono(cr, "+ new file:", -280, top + 80, 30, GREEN, k)
        mono(cr, "styles.css", -280, top + 135, 38, BLUE, k)
    panel(cr, t, A("a8", "Creating"), A("a8", end=True) + 0.5, newfile, h=190, accent=GREEN)
    panel(cr, t, A("a14", "loop"), A("a14", end=True) + 0.7, diff(True), h=210)

    hits = [A(i) for i in ("a2", "a4", "a6", "a8", "a11", "a16")]
    for h in hits:
        cue("ding", t, h + 0.05)
    counter(cr, t, tl, hits)
    thinking(cr, t, B["a10"])
    thinking(cr, t, B["a13"])

    cue("typing", t, 0.0, 1.6)                          # Dev was already hammering the keys
    cue("sigh", t, A("a3") - 0.55)                        # Dev's breath reactions (voice tags aren't reliable)
    cue("hush", t, B["a10"].start, B["a10"].end - B["a10"].start + 0.2)
    cue("gasp_in", t, A("a11", "wrong") + 0.35)
    cue("hush", t, B["a13"].start, B["a13"].end - B["a13"].start + 0.2)
    cue("sigh", t, A("a15") - 0.7)
    cue("thud", t, B["a16"].end + 0.55)
    th.hook(cr, t, [("I TRIED TO MAKE", False), ("CLAUDE DISAGREE", True)], end=A("a1", end=True) + 0.3, y=250, size=80)
    clean_caption(cr, t, tl)
