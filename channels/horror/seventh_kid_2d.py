"""The Seventh Kid, Part 1: the Halloween special. Owner, 27 Oct 2026: "Ok go for Halloween ... auto approved
Halloween use studies research reference make strong suspense tension video". Script and why:
out/horror/scripts_seventh_kid_part1.md (written against reports/Horror reference study 27 Oct.md).

YOU are Riley, walking six kids trick-or-treating; at the last house you count seven. Two of them are ghosts in the
bed sheet you cut for your little brother Sam this morning, crooked eye hole and all. A note on the door gives three
rules (the rules are the clues). Both ghosts grab your hands; you test them ("What's my name?"); the narrator gives the
answer, then one fact takes it away (Sam can't say R). The porch lights are the clock. The vote: which hand do you let
go, left or right? Clues on screen, never spoken: the left ghost's eyes catch the light like a cat's; the right ghost's
breath never fogs in the cold; the note's R's are written backwards.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py seventh_kid_2d   -> out/horror/seventh_kid_2d.mp4
"""
import math

from motion import audio, voice
from motion.engine import W, H, cairo, cue, seg
from motion.polish import text_width

from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the horror effects)
from channels.horror import toon2d as tk
from channels.horror.toon2d import INK, curve, glow, grade, hexa, mix, noise, poly, toon

NARRATOR = dict(turbo=True)
TAIL = 2.0                     # the reference study: the vote card stays up ~2 s with the comment ask on it
MUSIC = "horror"
TWIST = "k15"                  # the bed drops out under "But Sam is five."
audio.GAINS.update(sting=0.5)                 # the 7th-kid sting peaked at 0 dBFS in the first render
voice.SPEAKERS["sam"] = dict(voice="am_puck", speed=1.04, pitch=3.5, turbo_ref="am_puck+4.5")

SCRIPT = [
    dict(id="k1", scene="count", text="You're walking six kids trick-or-treating. At the last house, you count "
                                      "seven."),
    dict(id="k2", scene="ghosts", text="Two of them are ghosts. You only brought one."),
    dict(id="k3", scene="kitchen", text="Your little brother, Sam. You cut the holes for his eyes yourself."),
    dict(id="k4", scene="holes", text="One came out crooked. Both ghosts have it."),
    dict(id="k5", scene="door", text="There's a note on the door. In a child's handwriting."),
    dict(id="k6", scene="note", text="One. It always comes as the one you love most."),
    dict(id="k7", scene="note", text="Two. It can't say your name."),
    dict(id="k8", scene="note", text="Three. When the porch lights go out, it goes home with the hand it's holding."),
    dict(id="k9", scene="street", text="Trick-or-treat ends at nine. Every porch light goes out. Four minutes."),
    dict(id="k10", scene="hands", text="Both ghosts grab your hands."),
    dict(id="k11", scene="you", text="So you ask them. What's my name?"),
    dict(id="k12", scene="left", text="You're Riley!", speaker="sam", gap=0.3),
    dict(id="k13", scene="right", text="You're silly. I want to go home.", speaker="sam", gap=0.35),
    dict(id="k14", scene="hands", text="It can't say your name. So the left one is Sam.", gap=0.3),
    dict(id="k15", scene="you", text="But Sam is five. He can't say the letter R.", gap=0.7),
    dict(id="k16", scene="kitchen", text="Wiley! Look! I'm a ghost!", speaker="sam", gap=0.3),
    dict(id="k17", scene="left", text="He's never said Riley. Not once.", gap=0.3),
    dict(id="k18", scene="street", text="Two lights left.", gap=0.9),
    dict(id="k19", scene="hands", text="Whoever you let go of stays out here in the dark."),
    dict(id="k20", scene="hands", text="Let go of the left, and you trust what you know about Sam."),
    dict(id="k21", scene="hands", text="Let go of the right, and you trust the note on the door."),
    dict(id="k22", scene="hands", text="So which hand do you let go? Left, or right?", gap=0.3),
]

METADATA = dict(
    title="You Took 6 Kids Trick-or-Treating. You Count 7. 🎃",
    alt_titles=["Two Ghosts. You Only Brought One. 🎃", "Which Ghost Is Your Little Brother? 🎃"],
    description="""Halloween night. You're walking six kids trick-or-treating... and at the last house, you count seven. 🎃

Two of them are ghosts. You only brought one: your little brother, in the sheet you cut this morning. Both ghosts have his crooked eye hole. And the note on the door has three rules.

The Seventh Kid, Part 1. An interactive Halloween story: YOU decide what happens next.
💬 Which hand do you let go? Comment LEFT or RIGHT. Most comments decide Part 2. 👇

(Fiction. 2D animation. Suspense, no gore.)""",
    hashtags=["#Halloween", "#HorrorStory", "#Shorts"],
    tags=["halloween", "halloween story", "trick or treat", "scary story", "horror story", "interactive story",
          "you decide", "choose your ending", "ghost story", "2d animation", "plot twist", "part 1"],
    pinned_comment="Let go of the RIGHT. The note was right about the costume, and \"You're silly\" is exactly what "
                   "you'd say if you couldn't say the name. Left or right? 👇 (Look at the R's on the note 👀)",
)

KEY = {"seven", "ghosts", "one", "sam", "crooked", "both", "note", "child's", "love", "name", "hand", "holding",
       "nine", "four", "hands", "riley", "silly", "home", "five", "r", "wiley", "never", "lights", "dark", "left",
       "right"}
HZ = 600                                                     # the street's horizon
PORCH = (1.0, 0.76, 0.42)
NIGHT = ((0.72, 0.78, 1.0), (0.34, 0.33, 0.5))
SLEEVE = (tk.RY_JACKET[0], tk.RY_JACKET[1])
GOLD = hexa("#f2c14e")


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0):
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1), cy + 3 * shake * noise(t * 0.6, 4))
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


# ------------------------------------------------------------------ the street: houses, porch lights (the clock)
def _houses():
    out = []
    for i in range(6):
        for side in (-1, 1):
            z = 1 + 0.85 * i
            sc = 1 / z
            out.append((z, side, 360 + side * 470 * sc, HZ + (1240 - HZ) * sc, sc, i))
    return sorted(out, key=lambda h: -h[0])                  # farthest first: draw order, and the order they go dark


HOUSES = _houses()


def tree(cr, x, gy, sc, seed=0):
    """A bare tree, black against the sky."""
    cr.save()
    cr.translate(x, gy)
    cr.scale(sc, sc)
    cr.set_source_rgba(0.04, 0.04, 0.07, 1)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)

    def branch(x0, y0, ang, ln, w, d):
        x1, y1 = x0 + ln * math.sin(ang), y0 - ln * math.cos(ang)
        cr.set_line_width(w)
        cr.move_to(x0, y0)
        cr.line_to(x1, y1)
        cr.stroke()
        if d > 0:
            for k, da in enumerate((-0.45, 0.38)):
                branch(x1, y1, ang + da + 0.12 * math.sin(seed * 3 + d * 2 + k), ln * 0.72, w * 0.62, d - 1)
    branch(0, 0, 0.05 * math.sin(seed), 260, 34, 5)
    cr.restore()


def street(cr, t, lights=12.0, kids_away=False):
    """Looking down the street: sky and moon, two rows of houses toward the horizon, each with a porch light. `lights`
    = how many are still on (float); the farthest go dark first, so the dark walks toward you."""
    g = cairo.LinearGradient(0, 0, 0, HZ + 40)
    g.add_color_stop_rgb(0, 0.05, 0.06, 0.16)
    g.add_color_stop_rgb(1, 0.22, 0.16, 0.32)
    cr.set_source(g)
    cr.paint()
    for k in range(70):                                      # stars
        sx, sy = (k * 137.5) % W, (k * 71.3) % (HZ - 80)
        cr.set_source_rgba(1, 1, 1, 0.25 + 0.35 * (0.5 + 0.5 * math.sin(t * 1.3 + k)))
        cr.arc(sx, sy, 1.2 + (k % 3) * 0.6, 0, 2 * math.pi)
        cr.fill()
    glow(cr, 540, 250, 260, (0.85, 0.85, 1.0), 0.35)
    toon(cr, lambda c: c.arc(540, 250, 70, 0, 2 * math.pi), hexa("#f3efd9"), hexa("#cfc8a8"), (-14, -10), None, lw=3)
    cr.set_source_rgba(0.75, 0.72, 0.6, 0.5)
    for cx, cy, r in ((520, 230, 12), (562, 270, 9), (548, 222, 6)):
        cr.arc(cx, cy, r, 0, 2 * math.pi)
        cr.fill()
    cr.set_source_rgba(0.12, 0.1, 0.2, 0.75)                 # a cloud across the moon
    cr.save()
    cr.translate(470 + 20 * math.sin(t * 0.05), 300)
    cr.scale(1, 0.22)
    cr.arc(0, 0, 150, 0, 2 * math.pi)
    cr.restore()
    cr.fill()
    cr.set_source_rgba(0.07, 0.07, 0.12, 1)                  # far treeline
    cr.move_to(0, HZ + 10)
    for k in range(25):
        cr.line_to(k * 30, HZ - 20 - 18 * abs(math.sin(k * 1.7)))
    cr.line_to(W, HZ + 10)
    cr.close_path()
    cr.fill()
    cr.set_source_rgba(*hexa("#1c1c27")[:3], 1)              # the road and its pavements
    cr.move_to(-260, H)
    cr.line_to(W + 260, H)
    cr.line_to(372, HZ)
    cr.line_to(348, HZ)
    cr.close_path()
    cr.fill()
    for side in (-1, 1):
        cr.set_source_rgba(0.3, 0.3, 0.38, 1)
        cr.move_to(360 + side * 470, H)
        cr.line_to(360 + side * 620, H)
        cr.line_to(360 + side * 16, HZ)
        cr.line_to(360 + side * 12, HZ)
        cr.close_path()
        cr.fill()
    cr.set_source_rgba(0.85, 0.8, 0.5, 0.5)                  # dashed centre line
    for k in range(9):
        a, b = k / 9, (k + 0.45) / 9
        ya, yb = HZ + (H - HZ) * a ** 2, HZ + (H - HZ) * b ** 2
        wa, wb = 2 + 10 * a ** 2, 2 + 10 * b ** 2
        cr.move_to(360 - wa, ya)
        cr.line_to(360 + wa, ya)
        cr.line_to(360 + wb, yb)
        cr.line_to(360 - wb, yb)
        cr.close_path()
        cr.fill()
    walls = [hexa("#2b3046"), hexa("#3a2f3f"), hexa("#2c3b3c"), hexa("#3b3530")]
    n = len(HOUSES)
    for rank, (z, side, x, gy, sc, i) in enumerate(HOUSES):
        b = max(0.0, min(1.0, rank - (n - lights) + 1))
        wcol = walls[(i * 2 + (side > 0)) % 4]
        hw, hh = 300 * sc, 230 * sc
        cr.save()
        cr.translate(x, gy)
        toon(cr, lambda c: c.rectangle(-hw / 2, -hh, hw, hh), wcol, mix(wcol, (0, 0, 0, 1), 0.4), (side * -10, -6),
             None, lw=max(1.5, 4 * sc))
        toon(cr, lambda c: poly(c, [(-hw / 2 - 18 * sc, -hh), (0, -hh - 140 * sc), (hw / 2 + 18 * sc, -hh)]),
             hexa("#17151f"), None, (0, -6), None, lw=max(1.5, 4 * sc))
        dx = -side * 70 * sc                                 # the door faces the road
        cr.set_source_rgba(0.12, 0.07, 0.07, 1)
        cr.rectangle(dx - 26 * sc, -120 * sc, 52 * sc, 120 * sc)
        cr.fill()
        for wx in (side * 70 * sc,):                         # a window, some lit
            lit = 0.55 if (i + (side > 0)) % 3 == 0 else 0.0
            cr.set_source_rgba(*mix((0.08, 0.08, 0.12, 1), (1, 0.7, 0.35, 1), lit * b)[:3], 1)
            cr.rectangle(wx - 34 * sc, -170 * sc, 68 * sc, 60 * sc)
            cr.fill()
        lx, ly = dx + side * -44 * sc, -132 * sc             # the porch light beside the door
        if b > 0:
            glow(cr, lx, ly, 150 * sc, PORCH, 0.9 * b)
            glow(cr, dx, -10 * sc, 120 * sc, PORCH, 0.35 * b)
        cr.set_source_rgba(*mix((0.15, 0.13, 0.12, 1), (1, 0.9, 0.6, 1), b)[:3], 1)
        cr.arc(lx, ly, max(2.0, 9 * sc), 0, 2 * math.pi)
        cr.fill()
        if i % 2 == 0:                                       # a jack-o'-lantern on the step
            cr.set_source_rgba(0.95, 0.5, 0.1, 1)
            cr.arc(dx + 40 * sc * side, -12 * sc, 16 * sc, 0, 2 * math.pi)
            cr.fill()
            glow(cr, dx + 40 * sc * side, -12 * sc, 50 * sc, (1, 0.55, 0.15), 0.5 + 0.2 * math.sin(t * 9 + i))
        cr.restore()
        if i in (1, 3) and side < 0:
            tree(cr, x + 190 * sc, gy + 6 * sc, sc * 1.3, seed=i)
    if kids_away:                                            # the other kids, far off, walking to their parents' car
        for k, cost in enumerate(("witch", "skeleton", "pumpkin", "vampire", "astronaut")):
            tk.kid_full(cr, 300 + k * 28, HZ + 92 + (k % 2) * 6, 0.11, t, cost, seed=k)
    g = cairo.LinearGradient(0, HZ - 60, 0, H)               # ground mist
    g.add_color_stop_rgba(0, 0.6, 0.6, 0.8, 0)
    g.add_color_stop_rgba(0.25, 0.6, 0.6, 0.8, 0.14)
    g.add_color_stop_rgba(1, 0.6, 0.6, 0.8, 0.04)
    cr.set_source(g)
    cr.paint()


# ------------------------------------------------------------------ the last house: its door, the note, the porch light
def note_paper(cr, x, y, s, rot=0.05):
    """The note taped to the door, small (its words are read later, big)."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    toon(cr, lambda c: c.rectangle(-85, -105, 170, 210), hexa("#f1ead6"), hexa("#cbbf9f"), (-4, -4), None, lw=3)
    cr.set_source_rgba(0.55, 0.65, 0.85, 0.5)
    cr.set_line_width(1.5)
    for k in range(9):
        cr.move_to(-80, -70 + k * 20)
        cr.line_to(80, -70 + k * 20)
        cr.stroke()
    cr.set_source_rgba(0.45, 0.2, 0.55, 0.85)                 # crayon scribble lines
    cr.set_line_width(4)
    for k in range(7):
        y0 = -76 + k * 24
        cr.move_to(-66, y0)
        for j in range(10):
            cr.line_to(-66 + j * 13 + (k * 7) % 11, y0 + 4 * math.sin(j * 1.9 + k))
        cr.stroke()
    cr.set_source_rgba(0.95, 0.95, 0.85, 0.7)                 # tape
    for sx in (-1, 1):
        cr.save()
        cr.translate(sx * 70, -102)
        cr.rotate(sx * 0.6)
        cr.rectangle(-26, -9, 52, 18)
        cr.restore()
        cr.fill()
    cr.restore()


def porch(cr, t, light=1.0):
    """The last house, straight on: the red door with the note, the porch lamp, the steps, the candy bowl."""
    cr.set_source_rgba(*hexa("#24323b"))
    cr.paint()
    cr.set_source_rgba(0, 0, 0, 0.35)
    cr.set_line_width(3)
    for y in range(20, H, 44):
        cr.move_to(0, y)
        cr.line_to(W, y)
        cr.stroke()
    toon(cr, lambda c: c.rectangle(182, 290, 356, 680), hexa("#d9d2c0"), hexa("#9e9681"), (-8, -6), None)
    toon(cr, lambda c: c.rectangle(212, 320, 296, 650), hexa("#7c2024"), hexa("#4b1013"), (-10, -8), None)
    cr.set_source_rgba(0, 0, 0, 0.3)
    cr.set_line_width(4)
    for px, py, pw, ph in ((240, 470, 100, 200), (380, 470, 100, 200), (240, 710, 100, 220), (380, 710, 100, 220)):
        cr.rectangle(px, py, pw, ph)
        cr.stroke()
    cr.set_source_rgba(0.05, 0.05, 0.08, 1)                   # the dark window in the door
    cr.arc(360, 395, 52, math.pi, 0)
    cr.line_to(412, 420)
    cr.line_to(308, 420)
    cr.close_path()
    cr.fill()
    toon(cr, lambda c: c.arc(470, 690, 13, 0, 2 * math.pi), hexa("#d9b24a"), hexa("#8f7020"), (-3, -3), None, lw=3)
    note_paper(cr, 360, 590, 0.95)
    lx, ly = 600, 470                                         # the porch lamp
    toon(cr, lambda c: poly(c, [(lx - 30, ly - 70), (lx + 30, ly - 70), (lx + 24, ly + 40), (lx - 24, ly + 40)]),
         hexa("#1b1b20"), None, (0, 0), None, lw=4)
    cr.set_source_rgba(*mix((0.2, 0.18, 0.16, 1), (1, 0.85, 0.55, 1), light)[:3], 1)
    cr.rectangle(lx - 18, ly - 56, 36, 84)
    cr.fill()
    if light > 0:
        glow(cr, lx, ly - 10, 320, PORCH, 0.75 * light)
        glow(cr, 360, 620, 520, PORCH, 0.22 * light)
    for k, (y0, inset) in enumerate(((970, 0), (1080, -40), (1190, -80))):   # the steps
        toon(cr, lambda c, y0=y0, inset=inset: c.rectangle(80 + inset, y0, 560 - 2 * inset, 110), hexa("#5a4130"),
             hexa("#3a2a1e"), (0, -8), None)
    cr.save()                                                 # the candy bowl, still full (nobody's home)
    cr.translate(170, 960)
    toon(cr, lambda c: curve(c, [(-70, -20), (-60, 20), (-30, 40), (30, 40), (60, 20), (70, -20)]), hexa("#e07a18"),
         hexa("#a14f08"), (-6, -6), None)
    for k in range(9):
        cr.set_source_rgba(*((0.9, 0.2, 0.3, 1), (0.95, 0.85, 0.2, 1), (0.3, 0.6, 0.95, 1))[k % 3])
        cr.save()
        cr.translate(-52 + k * 13, -26 - 10 * math.sin(k * 1.3))
        cr.rotate(k)
        cr.rectangle(-9, -5, 18, 10)
        cr.restore()
        cr.fill()
    cr.restore()
    cr.save()                                                 # a jack-o'-lantern
    cr.translate(560, 1000)
    toon(cr, lambda c: c.arc(0, 0, 60, 0, 2 * math.pi), hexa("#f0821a"), hexa("#b45608"), (-8, -8), None)
    fl = 0.75 + 0.25 * math.sin(t * 11) * math.sin(t * 7.3)
    cr.set_source_rgba(1, 0.85, 0.3, fl)
    for sx in (-1, 1):
        cr.move_to(sx * 22 - 12, -6)
        cr.line_to(sx * 22 + 12, -6)
        cr.line_to(sx * 22, -26)
        cr.close_path()
        cr.fill()
    cr.move_to(-30, 16)
    cr.curve_to(-10, 34, 10, 34, 30, 16)
    cr.line_to(0, 22)
    cr.close_path()
    cr.fill()
    glow(cr, 0, 0, 140, (1, 0.6, 0.2), 0.4 * fl)
    cr.restore()


def crayon(cr, s, x, y, size, col, backwards_r=True):
    """A child's crayon capitals, R written backwards."""
    for ch in s:
        w = text_width(cr, ch, size, "Kalam")
        if ch == "R" and backwards_r:
            cr.save()
            cr.translate(x + w / 2, 0)
            cr.scale(-1, 1)
            hud2d._text(cr, ch, 0, y, size, col, "Kalam", "center")
            cr.restore()
        else:
            hud2d._text(cr, ch, x, y, size, col, "Kalam")
        x += w


NOTE = [("IF YOU COUNT", 0, True), ("ONE EXTRA:", 0, True), ("1. IT ALWAYS COMES AS", 1, False),
        ("THE ONE YOU LOVE MOST", 1, False), ("2. IT CAN'T SAY", 2, False), ("YOUR NAME", 2, False),
        ("3. WHEN THE PORCH LITES", 3, False), ("GO OUT, IT GOES HOME", 3, False), ("WITH THE HAND IT'S HOLDING", 3, False)]


def note_big(cr, t, hi=0, hk=1.0):
    """The note, filling the frame: lined paper, purple crayon; rule `hi` gets a yellow marker swipe (hk 0..1)."""
    cr.set_source_rgba(*hexa("#3d1416"))
    cr.paint()
    glow(cr, 620, 200, 600, PORCH, 0.3)
    cr.save()
    cr.translate(360, 650)
    cr.rotate(-0.025)
    toon(cr, lambda c: c.rectangle(-310, -470, 620, 900), hexa("#f2ebd7"), hexa("#d2c6a6"), (-8, -8), None)
    cr.set_source_rgba(0.55, 0.65, 0.85, 0.5)
    cr.set_line_width(2)
    for k in range(13):
        cr.move_to(-300, -360 + k * 66)
        cr.line_to(300, -360 + k * 66)
        cr.stroke()
    cr.set_source_rgba(0.85, 0.35, 0.35, 0.5)
    cr.move_to(-240, -470)
    cr.line_to(-240, 430)
    cr.stroke()
    for k, (line, rule, head) in enumerate(NOTE):
        y = -380 + k * 88 + (20 if rule >= 1 else 0)
        size = 46 if head else 40
        tw = sum(text_width(cr, ch, size, "Kalam") for ch in line)
        size = min(size, size * 560 / tw)
        if rule == hi and hi > 0:
            p = clamp_k = max(0.0, min(1.0, hk * 3 - (k - [r for _, r, _ in NOTE].index(rule))))
            if clamp_k > 0:
                tw = sum(text_width(cr, ch, size, "Kalam") for ch in line)
                cr.set_source_rgba(1, 0.9, 0.2, 0.55)
                cr.rectangle(-280, y - size * 0.95, (tw + 20) * p, size * 1.2)
                cr.fill()
        crayon(cr, line, -280, y, size, (0.75, 0.12, 0.15, 1) if head else (0.33, 0.14, 0.45, 1))
    cr.set_source_rgba(0.95, 0.95, 0.85, 0.75)
    for sx in (-1, 1):
        cr.save()
        cr.translate(sx * 270, -460)
        cr.rotate(sx * 0.5)
        cr.rectangle(-50, -16, 100, 32)
        cr.restore()
        cr.fill()
    cr.restore()


# ------------------------------------------------------------------ the kids
LINEUP = ["witch", "ghost", "skeleton", "pumpkin", "vampire", "ghost", "astronaut"]


def lineup(cr, t, counted=0.0, fear=0.3):
    """Frame 0: the last house behind, seven trick-or-treaters on the path facing you, your hand counting them;
    numbers pop over their heads as you count; the seventh is red."""
    cr.save()
    cr.translate(360, 330)
    cr.scale(0.62, 0.62)
    cr.translate(-360, -560)
    porch(cr, t)
    cr.restore()
    cr.set_source_rgba(0.02, 0.02, 0.05, 0.35)
    cr.paint()
    toon(cr, lambda c: poly(c, [(150, 640), (570, 640), (760, H), (-40, H)]), hexa("#4b4a52"), hexa("#2c2b33"),
         (0, -6), None)
    for side in (-1, 1):                                       # lawn
        cr.set_source_rgba(0.1, 0.16, 0.12, 1)
        cr.move_to(360 + side * 210, 640)
        cr.line_to(360 + side * 400, H)
        cr.line_to(360 + side * 400 + side * 400, H)
        cr.line_to(360 + side * 400, 640)
        cr.close_path()
        cr.fill()
    xs = [62, 160, 262, 360, 458, 560, 658]
    for k in sorted(range(7), key=lambda k: abs(k - 3), reverse=True):
        x, gy = xs[k], 860 + (20 if k % 2 else 0)
        c = LINEUP[k]
        if c == "ghost":
            tk.ghost_kid(cr, x, gy, 0.56, t, look=(0, 0.2), fog=1.0 if k == 1 else 0.0, seed=k,
                         eyeshine=0.0, rim=(1, 0.8, 0.5, 0.4), rim_from=(8, -8))
        else:
            tk.kid_full(cr, x, gy, 0.56, t, c, look=(0, 0.2), fear=fear, fog=1.0, seed=k, rim=(1, 0.8, 0.5, 0.4),
                        rim_from=(8, -8))
    glow(cr, 560, 300, 380, PORCH, 0.25)
    for k in range(7):                                        # the count over their heads
        p = max(0.0, min(1.0, (counted - k) * 3))
        if p <= 0:
            continue
        x, y = xs[k], 860 + (20 if k % 2 else 0) - 330 - 20 * (1 - p)
        red = k == 6
        cr.save()
        cr.translate(x, y)
        cr.scale(0.6 + 0.4 * p, 0.6 + 0.4 * p)
        if red:
            glow(cr, 0, 0, 90, hud2d.RED, 0.6)
        cr.arc(0, 0, 32, 0, 2 * math.pi)
        cr.set_source_rgba(*(hud2d.RED if red else (1, 1, 1, 1))[:3], p)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(4)
        cr.stroke()
        hud2d._text(cr, str(k + 1), 0, 14, 40, (1, 1, 1, p) if red else (0.08, 0.06, 0.1, p), hud2d.ROUND, "center")
        cr.restore()
    tk.hand_point(cr, 560, 1120, 1.0, t, skin=tk.RY_SKIN, sleeve=SLEEVE)


def ghost_pair(cr, t, look=(0.0, 0.0), ring=None):
    """The two ghosts side by side, waist up, under the porch light; the other kids blurred behind."""
    hud2d.blurred(cr, lambda c: lineup_bg(c, t), sigma=9)
    for k, x in ((0, 190), (1, 530)):
        tk.ghost_kid(cr, x, 1330, 1.25, t, look=look, fog=1.0 if k == 0 else 0.0, seed=k * 2,
                     rim=(1, 0.8, 0.5, 0.55), rim_from=(9, -8))
    if ring is not None:
        for x in (190, 530):
            hole_ring(cr, t, x - 34 * 1.25, 1330 - 462 * 1.25, ring)


def lineup_bg(cr, t):
    cr.save()
    cr.translate(360, 330)
    cr.scale(0.62, 0.62)
    cr.translate(-360, -560)
    porch(cr, t)
    cr.restore()
    for k, x in ((0, 90), (2, 250), (4, 470), (6, 640)):
        tk.kid_full(cr, x, 1000, 0.5, t, LINEUP[k], seed=k)


def hole_ring(cr, t, x, y, k):
    """A gold ring drawn round the crooked eye hole."""
    if k <= 0:
        return
    cr.save()
    cr.set_source_rgba(*GOLD[:3], 1)
    cr.set_line_width(7)
    cr.new_path()
    cr.arc(x, y, 46, -math.pi / 2, -math.pi / 2 + 2 * math.pi * min(1.0, k))
    cr.stroke()
    cr.restore()


def kitchen(cr, t, k=1.0):
    """This morning, warm: Sam in the sheet you just cut, grinning; your hand with the scissors."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.96, 0.86, 0.66)
    g.add_color_stop_rgb(1, 0.78, 0.6, 0.42)
    cr.set_source(g)
    cr.paint()
    toon(cr, lambda c: c.rectangle(420, 160, 250, 330), hexa("#fff6dc"), hexa("#e8d9b0"), (0, 0), None)   # window
    cr.set_source_rgba(*INK)
    cr.set_line_width(8)
    cr.move_to(545, 160)
    cr.line_to(545, 490)
    cr.move_to(420, 325)
    cr.line_to(670, 325)
    cr.stroke()
    glow(cr, 545, 325, 420, (1, 0.95, 0.75), 0.6)
    for x in (40, 200):                                        # cabinets
        toon(cr, lambda c, x=x: c.rectangle(x, 160, 150, 260), hexa("#c58f5a"), hexa("#93653a"), (-6, -6), None)
    cr.set_source_rgba(0.2, 0.5, 0.9, 0.9)                    # a drawing stuck on a cabinet: a ghost, by Sam
    cr.rectangle(70, 220, 90, 110)
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 1)
    cr.arc(115, 265, 26, math.pi, 0)
    cr.line_to(141, 310)
    cr.line_to(89, 310)
    cr.close_path()
    cr.fill()
    tk.sam_bust(cr, 340, 880, 1.55, t, smile=1.0, look=(0.3, -0.1))
    cr.save()                                                  # your hand with the scissors, bottom right
    cr.translate(600, 1120)
    cr.rotate(-0.5)
    cr.set_source_rgba(0.75, 0.78, 0.82, 1)
    for a in (-0.18, 0.18):
        cr.save()
        cr.rotate(a)
        cr.move_to(0, 0)
        cr.line_to(-8, -170)
        cr.line_to(8, 0)
        cr.close_path()
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(3)
        cr.stroke()
        cr.set_source_rgba(0.75, 0.78, 0.82, 1)
        cr.restore()
    for sx in (-1, 1):
        cr.set_source_rgba(0.85, 0.2, 0.2, 1)
        cr.arc(sx * 26, 40, 24, 0, 2 * math.pi)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(4)
        cr.stroke()
    toon(cr, lambda c: curve(c, [(-50, 60), (-40, 20), (40, 20), (60, 80), (30, 140), (-40, 140)]), tk.RY_SKIN,
         tk.RY_SKIN_D, (-6, -6), None)
    toon(cr, lambda c: c.rectangle(-60, 130, 130, 260), *SLEEVE, (-8, -6), None)
    cr.restore()


def inset(cr, x, y, r, draw, label=None, a=1.0):
    """A circular close-up with a gold ring (the reference study: insets keep a face on screen)."""
    if a <= 0:
        return
    cr.save()
    cr.push_group()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.clip()
    cr.save()
    draw(cr)
    cr.restore()
    cr.reset_clip()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*INK)
    cr.set_line_width(12)
    cr.stroke()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*GOLD[:3], 1)
    cr.set_line_width(7)
    cr.stroke()
    if label:
        w = text_width(cr, label, 24, hud2d.ROUND) + 28
        tk.tk_rrect(cr, x - w / 2, y + r - 20, w, 40, 20)
        cr.set_source_rgba(*GOLD[:3], 1)
        cr.fill()
        hud2d._text(cr, label, x, y + r + 9, 24, (0.08, 0.06, 0.04, 1), hud2d.ROUND, "center")
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def hands(cr, t, lights, ring=None, mark=None, dark=0.0, turn_left=0.0, shine=0.0):
    """From behind you on the dark street: a ghost holding each of your hands. ring = "left"/"right" draws a gold
    ring round that ghost; mark = "left"/"right" a red ring round the hand you'd let go."""
    street(cr, t, lights, kids_away=True)
    gl, gr = (110, 1170), (610, 1170)
    gs = 0.95
    tk.ghost_kid(cr, gl[0], gl[1], gs, t, look=(0.25 + 0.4 * turn_left, -0.1), arm=(81, -281), fog=1.0, seed=0.0,
                 eyeshine=shine, rim=(1, 0.8, 0.5, 0.35), rim_from=(9, -6))
    tk.ghost_kid(cr, gr[0], gr[1], gs, t, look=(-0.25, -0.1), arm=(-81, -281), fog=0.0, seed=2.0,
                 rim=(1, 0.8, 0.5, 0.35), rim_from=(9, -6))
    tk.riley_back(cr, 360, 500, 0.72, t, hands=1.0, rim=(1, 0.8, 0.5, 0.3), rim_from=(9, -4))
    if dark > 0:
        cr.set_source_rgba(0.0, 0.0, 0.03, 0.55 * dark)
        cr.paint()
    for side, (gx, gy) in (("left", gl), ("right", gr)):
        if ring == side:
            cr.set_source_rgba(*GOLD[:3], 1)
            cr.set_line_width(7)
            cr.arc(gx, gy - 470 * gs, 120, 0, 2 * math.pi)
            cr.stroke()
        if mark == side:
            hx = 360 + (-1 if side == "left" else 1) * 240 * 0.72
            hy = 500 + 560 * 0.72
            cr.set_source_rgba(*hud2d.RED[:3], 0.9 + 0.1 * math.sin(t * 10))
            cr.set_line_width(8)
            cr.arc(hx, hy, 70, 0, 2 * math.pi)
            cr.stroke()


def ghost_close(cr, t, side, lights, shine=0.0, look=(0.0, 0.0)):
    """One ghost, close, the street blurred behind it. Left: its breath fogs (and its eyes may catch the light);
    right: no breath at all."""
    hud2d.blurred(cr, lambda c: street(c, t, lights), sigma=9)
    tk.ghost_kid(cr, 360, 1560, 1.75, t, look=look, pail=False, fog=1.0 if side == "left" else 0.0,
                 eyeshine=shine, seed=0.0 if side == "left" else 2.0, rim=(1, 0.8, 0.5, 0.5), rim_from=(9, -8))
    w = text_width(cr, side.upper(), 30, hud2d.ROUND) + 40
    x = 40 if side == "left" else W - 40 - w
    tk.tk_rrect(cr, x, 215, w, 56, 28)
    cr.set_source_rgba(*GOLD[:3], 1)
    cr.fill()
    hud2d._text(cr, side.upper(), x + w / 2, 254, 30, (0.08, 0.06, 0.04, 1), hud2d.ROUND, "center")


def you_face(cr, t, lights, fear=0.6):
    hud2d.blurred(cr, lambda c: street(c, t, lights), sigma=8)
    tk.riley_bust(cr, 360, 980, 1.55, t, fear=fear, look=(0, 0.05), rim=(1, 0.8, 0.5, 0.55), rim_from=(10, -6),
                  fog=1.0)


# ------------------------------------------------------------------ shots, HUD, sound
def shots(tl):
    A, B = tl.at, tl.by_id
    return [
        (0.0, "count"), (B["k2"].start - 0.15, "ghosts"), (B["k3"].start - 0.25, "kitchen"),
        (B["k4"].start - 0.15, "holes"), (B["k5"].start - 0.15, "door"), (B["k6"].start - 0.15, "note1"),
        (B["k7"].start - 0.15, "note2"), (B["k8"].start - 0.15, "note3"), (B["k9"].start - 0.15, "street"),
        (B["k10"].start - 0.15, "hands"), (B["k11"].start - 0.15, "you"), (B["k12"].start - 0.15, "left"),
        (B["k13"].start - 0.15, "right"), (B["k14"].start - 0.15, "hands_l"), (B["k15"].start - 0.15, "you2"),
        (B["k16"].start - 0.25, "kitchen2"), (B["k17"].start - 0.15, "left2"), (B["k18"].start - 0.7, "street2"),
        (B["k19"].start - 0.15, "hands_dark"), (B["k20"].start - 0.15, "mark_l"), (B["k21"].start - 0.15, "mark_r"),
        (B["k22"].start - 0.15, "final"), (tl.total + 1, "end")]


_shots = {}


def lights_at(t, tl):
    """The porch lights still on: 12 until "Four minutes", then they go out a few at a time; two left at the end."""
    B = tl.by_id
    steps = [(B["k9"].end + 0.2, 11), (B["k11"].start, 10), (B["k13"].start - 0.2, 9), (B["k14"].end, 8),
             (B["k16"].start - 0.2, 6), (B["k17"].end, 5), (B["k18"].start - 0.8, 4), (B["k18"].start - 0.45, 3),
             (B["k18"].start - 0.1, 2)]
    n = 12.0
    for at, v in steps:
        if t >= at:
            n = v + max(0.0, 1 - (t - at) / 0.12) * (n - v)
    return n, steps


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    if id(tl) not in _shots:
        _shots[id(tl)] = shots(tl)
    sh = _shots[id(tl)]
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    s0, name, s1 = sh[k][0], sh[k][1], sh[k + 1][0]
    lights, steps = lights_at(t, tl)
    t_count0, t_seven = A("k1", "count"), A("k1", "seven.")
    counted = 7 * seg(t, t_count0, t_seven + 0.15)

    cr.save()
    if name == "count":
        camera(cr, t, s0, s1, 1.0, 1.07, cy=760)
        lineup(cr, t, counted, fear=0.3)
        grade(cr, *NIGHT)
    elif name == "ghosts":
        camera(cr, t, s0, s1, 1.02, 1.1, cy=700)
        ghost_pair(cr, t, look=(0.1 * math.sin(t * 0.8), 0.1))
        grade(cr, *NIGHT)
    elif name in ("kitchen", "kitchen2"):
        camera(cr, t, s0, s1, 1.0, 1.08, cy=760, shake=0.4)
        kitchen(cr, t)
        grade(cr, (1.0, 0.9, 0.72), (0.7, 0.55, 0.42))
        cr.set_source_rgba(1, 0.9, 0.7, 0.06 + 0.04 * math.sin(t * 23))       # old-film flicker
        cr.paint()
    elif name == "holes":
        camera(cr, t, s0, s1, 1.0, 1.04, shake=0.6)
        for half, (gx, side) in enumerate(((190, 0), (530, 1))):
            cr.save()
            cr.rectangle(0, half * H / 2, W, H / 2)
            cr.clip()
            cr.translate(0, half * H / 2)
            cr.translate(360, 320)
            cr.scale(2.2, 2.2)
            cr.translate(-gx, -(1330 - 462 * 1.25))
            ghost_pair(cr, t)
            cr.restore()
        grade(cr, *NIGHT)
        cr.set_source_rgba(0.9, 0.9, 1, 0.9)
        cr.rectangle(0, H / 2 - 3, W, 6)
        cr.fill()
        for half in (0, 1):                                    # rings round the crooked holes, as it's said
            hole_ring(cr, t, 360 - 34 * 1.25 * 2.2, half * H / 2 + 320, 3 * seg(t, B["k4"].start + 0.1,
                                                                                 B["k4"].start + 0.9))
    elif name == "door":
        camera(cr, t, s0, s1, 1.0, 1.35, cx=360, cy=590)
        porch(cr, t)
        grade(cr, *NIGHT)
    elif name.startswith("note"):
        r = int(name[-1])
        camera(cr, t, s0, s1, 1.02, 1.08, cy=500 + 120 * r)
        note_big(cr, t, hi=r, hk=seg(t, s0 + 0.2, s1 - 0.3))
        grade(cr, (1.0, 0.96, 0.9), (0.7, 0.62, 0.58))
    elif name in ("street", "street2"):
        camera(cr, t, s0, s1, 1.0, 1.1, cy=HZ)
        street(cr, t, lights, kids_away=name == "street")
        grade(cr, *NIGHT)
    elif name in ("hands", "hands_l", "hands_dark", "mark_l", "mark_r", "final"):
        camera(cr, t, s0, s1, 1.0, 1.06, cy=800, shake=1.0 + 0.6 * (name in ("hands_dark", "final")))
        hands(cr, t, lights, ring="left" if name == "hands_l" else None,
              mark={"mark_l": "left", "mark_r": "right"}.get(name), dark=0.6 if name in ("hands_dark", "final")
              else 0.0, shine=0.0)
        grade(cr, *NIGHT)
    elif name in ("you", "you2"):
        camera(cr, t, s0, s1, 1.03, 1.12, cy=700)
        you_face(cr, t, lights, fear=0.55 if name == "you" else 0.9)
        grade(cr, *NIGHT)
    elif name in ("left", "left2", "right"):
        side = "right" if name == "right" else "left"
        camera(cr, t, s0, s1, 1.02, 1.1, cy=760, shake=1.0 + 0.5 * (name == "left2"))
        shine = 0.0
        if name == "left":                                    # the clue: its eyes catch the light, once, briefly
            shine = max(0.0, 1 - abs(t - (B["k12"].end + 0.2)) / 0.25)
        elif name == "left2":
            shine = 0.8 * seg(t, B["k17"].end - 0.6, B["k17"].end)
        ghost_close(cr, t, side, lights, shine=shine,
                    look=(-0.3 + 0.5 * seg(t, s0, s0 + 1.0), 0.15) if name == "left2" else (0.0, 0.15))
        grade(cr, *NIGHT)
    cr.restore()

    # insets: a face on screen while the note is read
    if name == "note1":
        inset(cr, 590, 1050, 105, lambda c: (c.translate(590, 1050), c.scale(0.55, 0.55), c.translate(-360, -760),
                                             ghost_pair(c, t), grade(c, *NIGHT)), "BOTH GHOSTS")
    elif name == "note2":
        inset(cr, 590, 1050, 105, lambda c: (c.translate(590, 1050), c.scale(0.5, 0.5), c.translate(-360, -800),
                                             tk.riley_bust(c, 360, 980, 1.55, t, fear=0.7), grade(c, *NIGHT)), "YOU")
    elif name == "note3":
        inset(cr, 590, 1050, 105, lambda c: (c.translate(590, 1050), c.scale(0.45, 0.45), c.translate(-360, -900),
                                             hands(c, t, 12.0), grade(c, *NIGHT)), "YOUR HANDS")
    elif name == "you2":
        inset(cr, 590, 330, 110, lambda c: (c.translate(590, 330), c.scale(0.42, 0.42), c.translate(-340, -820),
                                            kitchen(c, t), grade(c, (1.0, 0.9, 0.72), (0.7, 0.55, 0.42))),
              "THIS MORNING", a=seg(t, A("k15", "five.", end=True), A("k15", "five.", end=True) + 0.2))

    hud.finish(cr, t, flash_at=[], vig=0.5, grain=0.06)
    if name in ("kitchen", "kitchen2"):
        tag(cr, "THIS MORNING")
    clock = "8:59 PM" if t >= B["k18"].start - 0.8 else "8:58 PM" if t >= B["k15"].start else \
        "8:57 PM" if t >= B["k10"].start else "8:56 PM"
    kids = ("KIDS", "7", "bad", t_seven) if t >= t_seven else ("KIDS", "6", None)
    last = max([at for at, _ in steps if at <= t], default=None)
    lstate = "bad" if lights <= 4 else "warn" if lights < 12 else None
    hud2d.stats(cr, t, [("TIME", clock, None), kids, ("PORCH LIGHTS", str(int(round(lights))), lstate, last)])
    rules_row(cr, t, tl)
    chip(cr, t, "THE SEVENTH KID · PART 1", 0.0, B["k2"].start)
    hud2d.hook(cr, t, [("YOU BROUGHT 6.", False), ("YOU COUNT 7.", True)], end=B["k1"].end + 0.1, y=250, size=88)
    hud2d.stamp(cr, t, A("k2", "one.", end=True) - 0.1, B["k2"].end + 0.3, ["ONLY 1 GHOST"], y=330)
    hud2d.stamp(cr, t, A("k4", "both"), B["k4"].end, ["BOTH"], y=H / 2, rot=-0.08)
    hud2d.rule_tag(cr, t, A("k9", "four"), B["k9"].end + 0.4, "LIGHTS OUT AT 9:00", y=230)
    hud2d.bubble(cr, t, A("k11", "what's"), B["k11"].end, "What's my name?", 360, 300, (360, 480))
    hud2d.bubble(cr, t, B["k12"].start, B["k12"].end, "You're Riley!", 360, 360, (360, 560))
    hud2d.bubble(cr, t, B["k13"].start, B["k13"].end, "You're silly. I want to go home.", 360, 360, (360, 560))
    hud2d.stamp(cr, t, A("k15", "r.", end=True) - 0.1, B["k15"].end + 0.35, ["CAN'T SAY R"], y=250)
    hud2d.bubble(cr, t, B["k16"].start, B["k16"].end, "Wiley! Look! I'm a ghost!", 380, 280, (330, 520))
    hud2d.stamp(cr, t, B["k18"].start - 0.1, B["k18"].end + 0.3, ["2 LIGHTS LEFT"], y=330)
    hud2d.ab_card(cr, t, A("k22", "which"), "SAID RILEY", "SAID SILLY", kicker="THE SEVENTH KID · PART 1 · YOUR CHOICE",
                  decides="Part 2", title="WHICH HAND DO YOU LET GO?", ask="COMMENT LEFT OR RIGHT",
                  letters=("L", "R"))
    hud2d.captions(cr, t, tl, KEY, skip=("k6", "k7", "k8", "k12", "k13", "k16"))
    cue("crickets", t, 0.0, tl.total)
    cue("musicbox", t, 0.0, B["k5"].start)
    for j in range(7):                                         # a tick for each kid counted, under "count seven"
        cue("click", t, t_count0 + j * (t_seven + 0.15 - t_count0) / 7)
    cue("sting", t, B["k1"].end + 0.05)
    cue("whoosh", t, B["k3"].start - 0.75)
    cue("whoosh", t, B["k16"].start - 0.75)
    for at, _ in steps:
        cue("porch_off", t, at)
    cue("heartbeat", t, B["k15"].start, B["k21"].end - B["k15"].start)
    cue("riser", t, B["k21"].start, B["k22"].start - B["k21"].start)


def chip(cr, t, text, start, end):
    """The series chip under the stats bar (first seconds)."""
    if t < start or t > end + 0.2:
        return
    a = 1 - max(0.0, min(1.0, (t - end) / 0.2))
    w = text_width(cr, text, 24, hud2d.ROUND) + 36
    cr.save()
    cr.push_group()
    tk.tk_rrect(cr, W / 2 - w / 2, 120, w, 44, 22)
    cr.set_source_rgba(0.04, 0.04, 0.06, 0.85)
    cr.fill_preserve()
    cr.set_source_rgba(*hud2d.YELLOW)
    cr.set_line_width(2.5)
    cr.stroke()
    hud2d._text(cr, text, W / 2, 150, 24, hud2d.YELLOW, hud2d.ROUND, "center")
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def rules_row(cr, t, tl):
    """Once read, the three rules stay as small chips under the stats bar; the one in play turns red."""
    A, B = tl.at, tl.by_id
    if t < B["k6"].start or t >= A("k22", "which"):
        return
    rules = [("#1 LOVED ONE", B["k6"].start, ()), ("#2 NO NAME", B["k7"].start, ("k11", "k14")),
             ("#3 LIGHTS OUT", B["k8"].start, ("k9", "k18", "k19"))]
    x = 22
    for text, at, hot_ids in rules:
        if t < at:
            break
        hot = any(B[i].start - 0.1 <= t <= B[i].end + 0.3 for i in hot_ids)
        w = text_width(cr, text, 20, hud2d.ROUND) + 26
        p = max(0.0, min(1.0, (t - at) / 0.25))
        cr.save()
        cr.push_group()
        tk.tk_rrect(cr, x, 116, w, 38, 19)
        cr.set_source_rgba(*(hud2d.RED[:3] if hot else (0.04, 0.04, 0.06)), 0.9)
        cr.fill_preserve()
        cr.set_source_rgba(1, 1, 1, 0.5)
        cr.set_line_width(2)
        cr.stroke()
        hud2d._text(cr, text, x + w / 2, 142, 20, (1, 1, 1, 1), hud2d.ROUND, "center")
        cr.pop_group_to_source()
        cr.paint_with_alpha(p)
        cr.restore()
        x += w + 10


def tag(cr, text):
    """The red flashback label."""
    w = text_width(cr, text, 30, hud2d.ROUND) + 40
    cr.save()
    cr.translate(40, 190)
    cr.rotate(-0.04)
    tk.tk_rrect(cr, 0, 0, w, 54, 8)
    cr.set_source_rgba(*hud2d.RED)
    cr.fill_preserve()
    cr.set_source_rgba(*INK)
    cr.set_line_width(4)
    cr.stroke()
    hud2d._text(cr, text, w / 2, 38, 30, (1, 1, 1, 1), hud2d.ROUND, "center")
    cr.restore()
