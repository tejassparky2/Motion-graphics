"""Low-poly channel, episode 1 (comedy): "I Asked AI to Review My Coworker's Code".

Script: channels/lowpoly/scripts/ep01_code_review.md (owner approved 17 Oct 2026). Original story; parody, not
affiliated with Anthropic or OpenAI. Cast and voices as in the skit test the owner signed off: Dev (male voice),
Claude (the Claude Code mascot), Codex (blue robot). 3D picture: scene_skit.html?dir=ep01 (directions/ep01.js);
this module adds the hook text, code panels, captions and sound.

    python channels/lowpoly/make_skit.py ep01_code_review
"""
import math
import os

from motion import thriller as th, voice
from motion.engine import FPS, W, cairo, cue, hexc, seg
from motion.polish import WHITE, appear, bold_text, captions, rrect, vignette

NARRATOR = dict(turbo=True, turbo_ref="am_michael")      # Dev, a boy: male voice (owner, 17 Oct)
DIRECTION = "ep01"
MUSIC = "pad"                      # soft ambient bed like the reference skits (silent drops on punchlines)
TAIL = 1.4
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build",
                      "lowpoly", "ep01_frames")

voice.SPEAKERS.update({
    "claude": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart"),
    "codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2"),
})

SCRIPT = [
    dict(id="e1", scene="dev", text="Guys. Review my coworker's code. Be honest."),
    dict(id="e2", scene="claude", speaker="claude", text="Of course! Let's take a look."),
    dict(id="e3", scene="claude", speaker="claude", text="Oh.", gap=0.6),
    dict(id="e4", scene="codex", speaker="codex", text="Oh no.", gap=0.35),
    dict(id="e5", scene="duo", speaker="claude", text="There's a function called [do stuff two.|doStuff2.]", gap=0.5),
    dict(id="e6", scene="codex", speaker="codex", text="And a comment that just says. Don't touch this.", gap=0.35),
    dict(id="e7", scene="dev", text="Okay. But is it bad?", gap=0.4),
    dict(id="e8", scene="claude", speaker="claude", text="It has [forty-seven|47] if statements. Inside each other.", gap=0.5),
    dict(id="e9", scene="codex", speaker="codex", text="And the password is [password one two three.|password123.]", gap=0.45),
    dict(id="e10", scene="devclose", text="Maybe my coworker was just tired.", gap=0.5),
    dict(id="e11", scene="claude", speaker="claude", text="Should I message your coworker?", gap=0.5),
    dict(id="e12", scene="devclose", text="No!", gap=0.2),
    dict(id="e13", scene="codex", speaker="codex", text="Too late. I checked who wrote it.", gap=0.45),
    dict(id="e14", scene="claudeclose", speaker="claude", text="It was you.", gap=0.7),
    dict(id="e15", scene="dev", text="That was past me. I don't know him.", gap=0.5),
    dict(id="e16", scene="claude", speaker="claude", text="Want me to fix it?", gap=0.6),
    dict(id="e17", scene="wide", text="Please.", gap=0.4),
    dict(id="e18", scene="codex", speaker="codex", text="I'll start with the password.", gap=0.5),
]

METADATA = dict(
    title="I Asked AI to Review My Coworker's Code 😬",
    alt_titles=["The AI Ran Git Blame on Me 😬", "Claude Found Out Who Wrote It"],
    description="""I asked Claude and Codex to review my coworker's code. Be honest, I said. 😬

doStuff2(). "// don't touch this". 47 if statements inside each other. password123.

Then Codex checked who wrote it.

Parody. Not affiliated with Anthropic or OpenAI.

💬 Be honest: what's the worst thing past-you left in your code? 👇""",
    hashtags=["#ClaudeCode", "#Codex", "#ProgrammerHumor"],
    tags=["claude", "claude code", "codex", "ai coding", "programmer humor", "code review", "git blame",
          "developer life", "coding memes", "software engineer"],
    pinned_comment="Be honest: what's the worst thing past-you left in your code? 👇",
)

COLORS = {None: (WHITE, hexc("#ffffff")), "claude": (hexc("#f5a05f"), hexc("#ff8a3d")),
          "codex": (hexc("#a9b8ff"), hexc("#7f9bff"))}
MONO = "DejaVu Sans Mono"
_n_frames = []


def _frame(t):
    if not _n_frames:
        _n_frames.append(len(os.listdir(FRAMES)))
    i = min(int(round(t * FPS)), _n_frames[0] - 1)
    return cairo.ImageSurface.create_from_png(os.path.join(FRAMES, f"f{i:05d}.png"))


def panel(cr, t, start, end, draw_body, h=230, y=330, accent=hexc("#7f9bff")):
    """A dark code-editor panel that pops in over the picture (above the captions)."""
    if not (start <= t < end):
        return
    k = appear(t, start, 0.22) * (1 - seg(t, end - 0.15, end))
    cr.save()
    cr.translate(W / 2, y)
    s = 0.9 + 0.1 * k
    cr.scale(s, s)
    rrect(cr, -310, -h / 2, 620, h, 22)
    cr.set_source_rgba(0.06, 0.07, 0.1, 0.94 * k)
    cr.fill_preserve()
    cr.set_source_rgba(*accent[:3], k)
    cr.set_line_width(4)
    cr.stroke()
    for i, c in enumerate(("#ff5f57", "#febc2e", "#28c840")):
        cr.arc(-280 + i * 26, -h / 2 + 22, 7, 0, 2 * math.pi)
        cr.set_source_rgba(*hexc(c)[:3], k)
        cr.fill()
    draw_body(cr, k, -h / 2)
    cr.restore()


def mono(cr, text, x, y, size, col, k, bold=True):
    cr.select_font_face(MONO, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD if bold else cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    cr.move_to(x, y)
    cr.set_source_rgba(*col[:3], k)
    cr.show_text(text)
    return cr.text_extents(text).x_advance


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.6)                                   # the references' dark, filmic edges
    th.grain(cr, t, 0.05)
    A = tl.at
    for key, dur in (("e3", 1.0), ("e12", 0.8), ("e14", 1.3)):   # music drops out for the punchlines
        cue("hush", t, A(key) - 0.25, dur)
    BLUE, PINK, GREEN, RED, GREY, YEL = (hexc(c) for c in ("#7fb4ff", "#ff79c6", "#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f"))

    def pr(cr, k, top):
        mono(cr, "Pull request #42", -280, top + 80, 34, WHITE, k)
        x = -280 + mono(cr, "author: ", -280, top + 140, 30, GREY, k, False)
        mono(cr, '"coworker"', x, top + 140, 30, YEL, k)
    panel(cr, t, A("e2", "look."), A("e3", end=True) + 0.4, pr, h=190)

    def fn(cr, k, top):
        x = -280 + mono(cr, "function ", -280, top + 110, 36, PINK, k)
        x += mono(cr, "doStuff2", x, top + 110, 36, BLUE, k)
        mono(cr, "() {", x, top + 110, 36, WHITE, k)
        mono(cr, "  // TODO: rename", -280, top + 165, 28, GREY, k, False)
    panel(cr, t, A("e5", "called"), A("e5", end=True) + 0.5, fn, h=210)

    def comment(cr, k, top):
        mono(cr, "// DON'T TOUCH THIS", -280, top + 120, 40, RED, k)
    panel(cr, t, A("e6", "touch"), A("e6", end=True) + 0.5, comment, h=190, accent=RED)

    def ifs(cr, k, top):
        n = int(47 * min(1, seg(t, A("e8", "47"), A("e8", "other.", end=True))))
        for i in range(6):
            mono(cr, " " * (i * 2) + "if (", -280, top + 70 + i * 34, 28, PINK, k)
        bold_text(cr, f"{n} nested ifs", 150, top + 215, 40, RED, outline=None, shadow=0)
    panel(cr, t, A("e8", "47"), A("e8", end=True) + 0.5, ifs, h=270, accent=RED)

    def pw(cr, k, top):
        x = -280 + mono(cr, "password = ", -280, top + 120, 36, WHITE, k)
        mono(cr, '"password123"', x, top + 120, 36, YEL, k)
    panel(cr, t, A("e9", "password", nth=2), A("e9", end=True) + 0.6, pw, h=190, accent=RED)

    def blame(cr, k, top):
        mono(cr, "$ git blame", -280, top + 85, 32, GREEN, k)
        x = -280 + mono(cr, "author: ", -280, top + 150, 38, GREY, k, False)
        if t >= A("e13", "wrote"):
            mono(cr, "YOU", x, top + 150, 44, RED, k)
    panel(cr, t, A("e13", "checked"), A("e14", end=True) + 0.3, blame, h=200, accent=GREEN)

    def gone(cr, k, top):
        w = mono(cr, '"password123"', -280, top + 110, 38, YEL, k)
        cut = seg(t, A("e18", "password."), A("e18", "password.", end=True) + 0.3)
        if cut > 0:
            cr.move_to(-285, top + 98)
            cr.line_to(-285 + (w + 10) * cut, top + 98)
            cr.set_source_rgba(*RED[:3], k)
            cr.set_line_width(6)
            cr.stroke()
        if cut >= 1:
            mono(cr, "deleted ✓", -280, top + 165, 30, GREEN, k)
    panel(cr, t, A("e18", "start"), tl.total + 1, gone, h=210, accent=GREEN)

    cue("hit", t, A("e3"))
    cue("hit", t, A("e13", "wrote"))
    cue("gasp_in", t, A("e14") - 0.35)
    th.hook(cr, t, [("MY “COWORKER'S”", False), ("CODE", True)], end=A("e1", end=True), y=170, size=96)
    clean_caption(cr, t, tl)


def clean_caption(cr, t, tl, y=1010, size=34):
    """The references' captions: the whole line in small clean type with a soft shadow, fading in and out,
    coloured by speaker (Dev white, Claude orange, Codex blue)."""
    for i, b in enumerate(tl.beats):
        nxt = tl.beats[i + 1].start if i + 1 < len(tl.beats) else tl.total
        end = min(b.end + 0.6, nxt - 0.05)
        if not (b.start - 0.05 <= t < end) or not b.units:
            continue
        k = min(appear(t, b.start - 0.05, 0.15), 1 - seg(t, end - 0.15, end))
        text = " ".join(u.shown for u in b.units)
        words, lines, cur = text.split(), [], ""
        for w in words:                                  # wrap to lines of about 30 characters
            if cur and len(cur) + 1 + len(w) > 30:
                lines.append(cur)
                cur = w
            else:
                cur = (cur + " " + w).strip()
        lines.append(cur)
        col = COLORS.get(b.speaker, COLORS[None])[0]
        cr.save()
        cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(size)
        for j, line in enumerate(lines):
            ext = cr.text_extents(line)
            x, yy = W / 2 - ext.x_advance / 2, y + j * size * 1.3
            for dx, dy, a in ((0, 3, 0.55), (0, 1, 0.75)):   # soft drop shadow
                cr.move_to(x + dx, yy + dy)
                cr.set_source_rgba(0, 0, 0, a * k)
                cr.show_text(line)
            cr.move_to(x, yy)
            cr.set_source_rgba(*col[:3], k)
            cr.show_text(line)
        cr.restore()
        return
