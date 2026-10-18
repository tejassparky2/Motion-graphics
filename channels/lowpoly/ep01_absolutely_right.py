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
mono = _ep1.mono

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
    dict(id="a9", scene="dev", text="Just once. Tell me I'm wrong.", gap=0.7),
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
    cr.translate(W / 2, 880)
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


def toolcard(cr, t, start, end, title, rows, y=880):
    """A coding agent's tool log (reference 7): title bar, then one step per row, revealed one by one.
    rows: (verb, target, note, colour of note); verb "*" = a working line in orange, "ok" = a green tick line."""
    if not (start <= t < end):
        return
    k = appear(t, start, 0.2) * (1 - seg(t, end - 0.15, end))
    h = 78 + 46 * len(rows)
    cr.save()
    cr.translate(W / 2, y)
    s = 0.92 + 0.08 * k
    cr.scale(s, s)
    rrect(cr, -320, -h / 2, 640, h, 18)
    cr.set_source_rgba(0.09, 0.09, 0.12, 0.95 * k)
    cr.fill_preserve()
    cr.set_source_rgba(1, 1, 1, 0.12 * k)
    cr.set_line_width(2)
    cr.stroke()
    top = -h / 2
    mono(cr, title, -296, top + 38, 20, GREY, k)
    cr.move_to(-320, top + 56)
    cr.line_to(320, top + 56)
    cr.set_source_rgba(1, 1, 1, 0.08 * k)
    cr.stroke()
    for i, (verb, target, note, col) in enumerate(rows):
        at = start + 0.25 + 0.32 * i
        if t < at:
            break
        kk = k * appear(t, at, 0.12)
        yy = top + 96 + 46 * i
        if verb == "*":
            pulse = 0.6 + 0.4 * math.sin(t * 6)
            mono(cr, "✻ " + target, -296, yy, 24, ORANGE, kk * pulse)
            continue
        if verb == "ok":
            mono(cr, "✓ " + target, -296, yy, 24, GREEN, kk)
            continue
        xx = -296 + mono(cr, verb, -296, yy, 24, WHITE, kk) + 16
        xx += mono(cr, target, xx, yy, 24, (0.68, 0.71, 0.78), kk) + 16
        if note:
            mono(cr, note, xx, yy, 24, col, kk)
    cr.restore()


def caption(cr, t, tl, y=470, size=30):
    """Reference 7's captions: small clean white type with a soft shadow, above the characters, whole line at once."""
    for i, b in enumerate(tl.beats):
        nxt = tl.beats[i + 1].start if i + 1 < len(tl.beats) else tl.total
        end = min(b.end + 0.5, nxt - 0.05)
        if not (b.start - 0.05 <= t < end) or not b.units:
            continue
        k = min(appear(t, b.start - 0.05, 0.12), 1 - seg(t, end - 0.12, end))
        words, lines, cur = " ".join(u.shown for u in b.units).split(), [], ""
        for w in words:
            if cur and len(cur) + 1 + len(w) > 28:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        cr.save()
        cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(size)
        for j, line in enumerate(lines):
            ext = cr.text_extents(line)
            x, yy = W / 2 - ext.x_advance / 2, y + j * size * 1.3
            for dy, a in ((3, 0.6), (1, 0.8)):
                cr.move_to(x, yy + dy)
                cr.set_source_rgba(0, 0, 0, a * k)
                cr.show_text(line)
            cr.move_to(x, yy)
            cr.set_source_rgba(1, 1, 1, k)
            cr.show_text(line)
        cr.restore()
        return


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.6)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id

    T = "my-app · fix loop   Claude ▾"
    toolcard(cr, t, A("a2", "Fixing"), A("a2", end=True) + 0.6, T,
             [("Read", "app.js", "", GREY), ("Edit", "app.js", "+1 −1", GREEN), ("ok", "Fixed line 42", "", GREEN)])
    toolcard(cr, t, A("a4", "Putting"), A("a4", end=True) + 0.6, T,
             [("Edit", "app.js", "+1 −1", GREEN), ("ok", "Reverted line 42", "", GREEN)])
    toolcard(cr, t, A("a6", "Rewriting"), A("a6", end=True) + 0.6, T,
             [("Read", "styles.css", "", GREY), ("Edit", "styles.css", "+2,000 −1,987", YEL), ("*", "Rewriting CSS…", "", ORANGE)])
    toolcard(cr, t, A("a8", "Creating"), A("a8", end=True) + 0.6, T,
             [("Write", "styles.css", "+1", GREEN), ("ok", "Created styles.css", "", GREEN)])
    toolcard(cr, t, A("a14", "look"), A("a14", end=True) + 0.9, T,
             [("Read", "app.js", "", GREY), ("Read", "app.js", "(again)", GREY), ("*", "Looking at that loop…", "", ORANGE)])

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
    caption(cr, t, tl)
