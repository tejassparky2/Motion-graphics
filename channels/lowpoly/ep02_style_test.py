"""Low-poly channel: camera/caption style test for episode 2 (owner, 18 Oct 2026: "yes make the test shot").

The first six lines of channels/lowpoly/scripts/ep02_wrong_file.md (script not yet approved; this is only a look test)
shot in the "That's Not My Dad" reference's style: wide lens, close low and tilted angles, handheld shake, a cut
inside most lines, one-word bold captions. 3D picture: scene_skit.html?dir=ep02test (directions/ep02test.js).

    python channels/lowpoly/make_skit.py ep02_style_test
"""
import os

from motion import thriller as th, voice
from motion.engine import FPS, W, cairo, cue, hexc, seg
from motion.polish import WHITE, appear, rrect, vignette

NARRATOR = dict(turbo=True, turbo_ref="am_michael")      # Dev, a boy: male voice (owner, 17 Oct)
DIRECTION = "ep02test"
MUSIC = "pad"
TAIL = 1.0
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build",
                      "lowpoly", "ep02_test_frames")

voice.SPEAKERS.update({
    "claude": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart"),
    "codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2"),
})

SCRIPT = [
    dict(id="t1", scene="dev", text="Nothing I change does anything."),
    dict(id="t2", scene="claude", speaker="claude", text="Let's add a print. Just to check.", gap=0.4),
    dict(id="t3", scene="dev", text="Done. Nothing printed.", gap=0.4),
    dict(id="t4", scene="codex", speaker="codex", text="Okay. Delete the whole function.", gap=0.4),
    dict(id="t5", scene="dev", text="Deleted. The app still works.", gap=0.4),
    dict(id="t6", scene="claude", speaker="claude", text="That's not possible.", gap=0.5),
]

METADATA = dict(title="Style test (not for upload)", alt_titles=[], description="Style test. Parody. Not affiliated "
                "with Anthropic or OpenAI.", hashtags=[], tags=[], pinned_comment="")

COLORS = {None: WHITE, "claude": hexc("#ffb27a"), "codex": hexc("#9fb4ff")}
MONO = "DejaVu Sans Mono"
_n_frames = []


def _frame(t):
    if not _n_frames:
        _n_frames.append(len(os.listdir(FRAMES)))
    i = min(int(round(t * FPS)), _n_frames[0] - 1)
    return cairo.ImageSurface.create_from_png(os.path.join(FRAMES, f"f{i:05d}.png"))


def panel(cr, t, start, end, draw_body, h=200, y=330, accent=hexc("#7f9bff")):
    if not (start <= t < end):
        return
    k = appear(t, start, 0.18) * (1 - seg(t, end - 0.12, end))
    cr.save()
    cr.translate(W / 2, y)
    cr.rotate(-0.03)                      # a little tilt, like the handheld camera
    s = 0.88 + 0.12 * k
    cr.scale(s, s)
    rrect(cr, -310, -h / 2, 620, h, 22)
    cr.set_source_rgba(0.06, 0.07, 0.1, 0.94 * k)
    cr.fill_preserve()
    cr.set_source_rgba(*accent[:3], k)
    cr.set_line_width(4)
    cr.stroke()
    draw_body(cr, k, -h / 2)
    cr.restore()


def mono(cr, text, x, y, size, col, k):
    cr.select_font_face(MONO, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(size)
    cr.move_to(x, y)
    cr.set_source_rgba(*col[:3], k)
    cr.show_text(text)
    return cr.text_extents(text).x_advance


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.55)
    th.grain(cr, t, 0.05)
    A = tl.at
    cue("hush", t, A("t6") - 0.25, 1.4)
    PINK, YEL, GREY, GREEN, RED = (hexc(c) for c in ("#ff79c6", "#ffd23f", "#8a93a6", "#7ee08a", "#ff5c5c"))

    def prn(cr, k, top):
        x = -280 + mono(cr, "print", -280, top + 115, 44, PINK, k)
        mono(cr, '("HERE")', x, top + 115, 44, YEL, k)
    panel(cr, t, A("t2", "print."), A("t2", end=True) + 0.3, prn)

    def term(cr, k, top):
        mono(cr, "$ python app.py", -280, top + 85, 34, GREEN, k)
        if int(t * 2.5) % 2:
            mono(cr, "▌", -280, top + 145, 34, GREY, k)
    panel(cr, t, A("t3"), A("t3", end=True) + 0.3, term, accent=GREY)

    def gone(cr, k, top):
        w = mono(cr, "def handle_click():", -280, top + 80, 32, PINK, k)
        cut = seg(t, A("t5"), A("t5") + 0.4)
        cr.move_to(-285, top + 70)
        cr.line_to(-285 + (w + 10) * cut, top + 70)
        cr.set_source_rgba(*RED[:3], k)
        cr.set_line_width(5)
        cr.stroke()
        if t >= A("t5", "still"):
            mono(cr, "app: running ✓", -280, top + 150, 36, GREEN, k)
    panel(cr, t, A("t5"), A("t5", end=True) + 0.4, gone, accent=GREEN)

    cue("hit", t, A("t6"))
    th.hook(cr, t, [("NOTHING I CHANGE", False), ("WORKS", True)], end=A("t1", end=True), y=170, size=86)
    word_caption(cr, t, tl)


def word_caption(cr, t, tl, y=930, size=66):
    """The reference's captions: one word at a time, big bold type with a hard shadow, popping in.
    Dev white, Claude orange, Codex blue."""
    for b in tl.beats:
        if not (b.start - 0.05 <= t < b.end + 0.25) or not b.units:
            continue
        cur = None
        for u in b.units:
            if t >= u.start - 0.03:
                cur = u
        if cur is None:
            return
        word = cur.shown
        k = appear(t, cur.start - 0.03, 0.07)
        cr.save()
        cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(size)
        ext = cr.text_extents(word)
        cr.translate(W / 2, y)
        s = 1.18 - 0.18 * k
        cr.scale(s, s)
        x = -ext.x_advance / 2
        cr.move_to(x, 0)
        cr.text_path(word)
        cr.set_source_rgba(0, 0, 0, 0.85)
        cr.set_line_width(7)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
        cr.move_to(x + 2, 5)
        cr.set_source_rgba(0, 0, 0, 0.6)
        cr.show_text(word)
        cr.move_to(x, 0)
        cr.set_source_rgba(*COLORS.get(b.speaker, WHITE)[:3], 1)
        cr.show_text(word)
        cr.restore()
        return
