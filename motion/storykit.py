"""Shared pieces for the story-style news videos (characters acting in drawn places, camera cuts on key words).

World units: characters stand at y=905 (GROUND 900). Camera helper: to put world point Y at screen height S with
zoom z, use focus y = Y + (780 - S) / z (kit.enter_world anchors the focus at (360, 780)).
A character's head centre is at y~725 (feet at 905): close-up keys look like (1.8, x, 825)."""
import math

from .engine import INK, RED, WHITE, at, blob, dot, hexc, line, pop, rrect_pts, shape, sharp_shape, write
from .newsfolk import folk

GROUND = 900
SKY = hexc("#a9dcf5")
GRASS = hexc("#9ccf7a")
ROAD = hexc("#c9b48a")
GREEN = hexc("#2e9e52")
GOLD = hexc("#f2b632")
NAVY = hexc("#23346b")
ORANGE = hexc("#e0a03a")
PURPLE = hexc("#8a63d2")


def news_pacing():
    """Pacing for the news channel. Call once at the top of each news video module.
    Research (research_notes/news_pacing.md): pauses of 300-400 ms between phrases already give the full
    intelligibility gain (Tanaka et al. 2011), human Shorts narrators pause ~0.1-0.2 s, and every extra second of
    silence is a swipe risk. So a clear but short stop at each full stop (each sentence is still its own take, so the
    voice drops at the end), a slightly longer one after a question, and a slow camera push-in on every held shot."""
    from . import kit, timeline
    timeline.STOP_PAUSE = 0.32
    timeline.QUESTION_PAUSE = 0.40
    timeline.BEAT_GAP = 0.34
    kit.DRIFT[0] = 0.006


def reveal_gaps(script, music, gap=0.55):
    """Keep a real beat of silence before each reveal line (the music drops out there)."""
    for spec in script:
        if spec["id"] in music.get("drops", ()):
            spec["gap"] = max(spec.get("gap", 0.18), gap)


def actor(cr, who, x, t, y=905, **kw):
    """A character from our own cast (motion/newsfolk.py)."""
    if kw.get("eyes") == "dot":
        kw["eyes"] = "open"
    folk(cr, who, x, y, t, **kw)


def focus(x, z=1.8, y=725, screen=600):
    """Camera key that puts world point (x, y) at screen height `screen`."""
    return (z, x, y + (780 - screen) / z)


def sky_ground(cr, ground=ROAD, snow=False):
    cr.set_source_rgba(*(hexc("#dfe9f2") if snow else SKY))
    cr.paint()
    for k, (cx, cy) in enumerate([(120, 330), (620, 290), (1100, 340), (1600, 300), (-300, 310)]):
        blob(cr, cx, cy, 70, 26, WHITE, 17100 + k, amp=0.8, lw=0, stroke=None)
    sharp_shape(cr, [(-1200, GROUND), (2600, GROUND), (2600, 2200), (-1200, 2200)], WHITE if snow else ground,
                seed=17110, amp=0.8, lw=4)
    if not snow:
        for k in range(-8, 22):
            line(cr, [(k * 120, 960), (k * 120 + 60, 960)], 8, GOLD, 17120 + k, amp=0.2)


def snowfall(cr, t, x0=-600, x1=2000):
    for k in range(70):
        x = x0 + (k * 97) % (x1 - x0)
        y = 250 + ((k * 53 + t * 60) % 700)
        dot(cr, x + 10 * math.sin(t + k), y, 4, WHITE)


def building(cr, x, w, h, col, sign, sign_col=WHITE, sign_bg=None, windows=True, seed=17200):
    top = GROUND - h
    shape(cr, rrect_pts(x - w / 2, top, w, h, 6, 18), col, seed=seed, amp=0.6, lw=5)
    if sign:
        shape(cr, rrect_pts(x - w / 2 - 14, top - 30, w + 28, 64, 8, 16), sign_bg or NAVY, seed=seed + 1, amp=0.4,
              lw=5)
        write(cr, [(sign, sign_col)], x, top + 14, 36 if len(sign) < 14 else 28, align="center", bold=True)
    if windows:
        for r in range(max(1, int((h - 160) / 110))):
            for c in range(max(1, int((w - 40) / 90))):
                wx = x - w / 2 + 30 + c * 90
                wy = top + 60 + r * 110
                shape(cr, rrect_pts(wx, wy, 56, 64, 4, 10), hexc("#cdeaf7"), seed=seed + 10 + r * 9 + c, amp=0.3,
                      lw=3)
    shape(cr, rrect_pts(x - 40, GROUND - 130, 80, 130, 6, 12), hexc("#8e5a2e"), seed=seed + 5, amp=0.4, lw=4)


def hospital(cr, x, seed=17300):
    building(cr, x, 420, 470, WHITE, "HOSPITAL", WHITE, hexc("#e0302f"), seed=seed)
    shape(cr, rrect_pts(x - 14, GROUND - 440, 28, 80, 3, 10), RED, seed=seed + 50, amp=0.2, lw=0, stroke=None)
    shape(cr, rrect_pts(x - 40, GROUND - 414, 80, 28, 3, 10), RED, seed=seed + 51, amp=0.2, lw=0, stroke=None)


def quarantine_tape(cr, x0, x1, y, seed=17350):
    line(cr, [(x0, y), (x1, y + 10)], 26, GOLD, seed, amp=0.4)
    n = int((x1 - x0) / 170)
    for k in range(n):
        write(cr, [("QUARANTINE", INK)], x0 + 85 + k * 170, y + 14 + 10 * k / max(1, n), 22, align="center",
              bold=True)


def billboard(cr, x, y, w, h, draw_fn, seed=17400):
    """A roadside billboard on two posts; draw_fn(cr) draws inside around (0, 0)."""
    for px in (x - w * 0.3, x + w * 0.3):
        line(cr, [(px, GROUND), (px, y + h / 2)], 12, hexc("#8f939b"), seed + int(px), amp=0.2)
    shape(cr, rrect_pts(x - w / 2, y - h / 2, w, h, 10, 16), WHITE, seed=seed, amp=0.5, lw=6)
    with at(cr, x, y):
        draw_fn(cr)


def podium(cr, x, label, col=NAVY, seed=17450, h=110):
    """A speaker's podium, drawn after the speaker so it hides their legs (keep h low so the face shows)."""
    shape(cr, [(x - 80, GROUND), (x + 80, GROUND), (x + 66, GROUND - h), (x - 66, GROUND - h)], col, seed=seed,
          amp=0.4, lw=5)
    write(cr, [(label, WHITE)], x, GROUND - h / 2 + 8, 22, align="center", bold=True)
    for k in (-1, 1):
        line(cr, [(x + k * 20, GROUND - h), (x + k * 34, GROUND - h - 40)], 4, INK, seed + k, amp=0.1)


def office(cr, t):
    cr.set_source_rgba(*hexc("#f3ead6"))
    cr.paint()
    for k in range(-6, 18):
        line(cr, [(k * 110, 250), (k * 110, GROUND)], 4, hexc("#e8dcc0"), 17500 + k, amp=0.4)
    sharp_shape(cr, [(-1200, GROUND), (2600, GROUND), (2600, 2200), (-1200, 2200)], hexc("#b07a45"), seed=17520,
                amp=0.8, lw=4)
    shape(cr, rrect_pts(80, 420, 240, 200, 10, 14), hexc("#7fc8e8"), seed=17530, amp=0.4, lw=5)   # window
    line(cr, [(200, 420), (200, 620)], 5, INK, 17531, amp=0.2)


def desk(cr, x, seed=17550):
    shape(cr, rrect_pts(x - 160, GROUND - 150, 320, 24, 6, 12), hexc("#8e5a2e"), seed=seed, amp=0.3, lw=4)
    for dx in (-140, 120):
        shape(cr, rrect_pts(x + dx, GROUND - 126, 20, 126, 4, 10), hexc("#6b4a2e"), seed=seed + dx, amp=0.2, lw=3)


def laptop(cr, x, y, s=1.0, screen=hexc("#7fc8e8"), seed=17600):
    """A generic laptop (no brand logo)."""
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-80, -110, 160, 104, 8, 12), hexc("#c9ccd2"), seed=seed, amp=0.3, lw=4)
        shape(cr, rrect_pts(-70, -100, 140, 84, 4, 10), screen, seed=seed + 1, amp=0.2, lw=0, stroke=None)
        shape(cr, [(-100, -6), (100, -6), (86, 10), (-86, 10)], hexc("#a9adb5"), seed=seed + 2, amp=0.3, lw=4)


def robot(cr, x, y, t, s=1.0, reach=0.0, seed=17650):
    """A friendly AI-helper robot."""
    with at(cr, x, y + 4 * math.sin(t * 3), s):
        line(cr, [(0, -150), (0, -176)], 4, INK, seed, amp=0.1)
        dot(cr, 0, -180, 8, RED)
        shape(cr, rrect_pts(-44, -150, 88, 66, 18, 12), hexc("#dfe3ea"), seed=seed + 1, amp=0.4, lw=4.5)
        for sx in (-1, 1):
            blob(cr, sx * 18, -118, 10, 12, hexc("#5fd1f5"), seed + 2 + sx, amp=0.2, lw=3)
        shape(cr, rrect_pts(-36, -80, 72, 70, 14, 12), hexc("#c9ccd2"), seed=seed + 5, amp=0.4, lw=4.5)
        line(cr, [(36, -60), (70 + 40 * reach, -70 - 10 * reach)], 8, INK, seed + 6, amp=0.2)
        blob(cr, 74 + 40 * reach, -72 - 10 * reach, 10, 10, hexc("#dfe3ea"), seed + 7, amp=0.2, lw=3)
        for sx in (-1, 1):
            line(cr, [(sx * 16, -10), (sx * 18, 0)], 7, INK, seed + 8 + sx, amp=0.1)


def file_icon(cr, kind, x, y, s=1.0, seed=17700):
    with at(cr, x, y, s):
        if kind == "files":
            shape(cr, [(-40, -22), (-12, -22), (-4, -30), (40, -30), (40, 30), (-40, 30)], hexc("#7fb3e8"),
                  seed=seed, amp=0.4, lw=4)
        elif kind == "email":
            shape(cr, rrect_pts(-42, -28, 84, 56, 6, 12), WHITE, seed=seed, amp=0.4, lw=4)
            line(cr, [(-40, -24), (0, 6), (40, -24)], 4, INK, seed + 1, amp=0.3)
        elif kind == "messages":
            blob(cr, 0, -4, 42, 30, GREEN, seed, amp=0.5, lw=4)
        elif kind == "history":
            blob(cr, 0, 0, 34, 34, hexc("#7fc8e8"), seed, amp=0.4, lw=4)
            line(cr, [(-34, 0), (34, 0)], 3, INK, seed + 1, amp=0.3)
            blob(cr, 0, 0, 14, 34, None, seed + 2, amp=0.3, lw=3)


def sign(cr, x, y, text, col=RED, bg=WHITE, s=1.0, rot=-0.04, seed=17750, start=None, t=None):
    sc = s * ((pop(t, start, 0.25) or 0.01) if start is not None else 1.0)
    with at(cr, x, y, sc, rot=rot):
        cr.select_font_face("Kalam", 0, 1)
        cr.set_font_size(40)
        half = cr.text_extents(text).x_advance / 2 + 26
        shape(cr, rrect_pts(-half, -38, 2 * half, 76, 10, 12), bg, seed=seed, amp=0.4, lw=4.5)
        write(cr, [(text, col)], 0, 14, 40, align="center", bold=True)


def comment_prompt(cr, t, start, y=430):
    """'Tell me in the comments' as on-screen text under the YES/NO buttons (the voice ends on the question)."""
    if t < start:
        return
    cr.identity_matrix()
    with at(cr, 360, y, max(0.6, pop(t, start, 0.25)) * 0.9):
        shape(cr, rrect_pts(-250, -38, 500, 76, 38, 14), NAVY, seed=17800, amp=0.3, lw=4)
        write(cr, [("Tell me in the comments", WHITE)], -16, 13, 34, align="center", bold=True)
        line(cr, [(212, -14), (212, 16)], 5, GOLD, 17801, amp=0.1)
        line(cr, [(200, 4), (212, 18), (224, 4)], 5, GOLD, 17802, amp=0.1)


def squirrel(cr, x, y, t, s=1.0, facing=1, seed=17850):
    """A generic wild rodent (squirrel / prairie dog) standing on its back legs."""
    brown = hexc("#a8743f")
    with at(cr, x, y, s):
        cr.scale(facing, 1)
        blob(cr, -46, -70, 30, 62, hexc("#8a5a2b"), seed, amp=0.8, lw=4)          # bushy tail
        blob(cr, 0, -60, 34, 52, brown, seed + 1, amp=0.4, lw=4)                    # body
        blob(cr, 6, -50, 16, 26, hexc("#e9cfa3"), seed + 2, amp=0.3, lw=0, stroke=None)   # belly
        blob(cr, 10, -124, 26, 24, brown, seed + 3, amp=0.4, lw=4)                  # head
        blob(cr, -4, -146, 7, 9, brown, seed + 4, amp=0.2, lw=3)                    # ear
        dot(cr, 20, -128, 4.5, INK)                                                 # eye
        dot(cr, 36, -118, 3.5, INK)                                                 # nose
        for sx in (-10, 14):
            line(cr, [(sx, -12), (sx, 0)], 6, INK, seed + 5 + sx, amp=0.1)


def flea(cr, x, y, t, s=1.0, seed=17870):
    """A tiny flea that hops in place."""
    hop = abs(math.sin(t * 6)) * 10
    with at(cr, x, y - hop, s):
        blob(cr, 0, 0, 9, 7, hexc("#4a2a1a"), seed, amp=0.2, lw=2)
        for k in (-1, 1):
            line(cr, [(k * 4, 4), (k * 9, 10)], 2, INK, seed + k, amp=0.1)
