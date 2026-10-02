"""Paradox: "Gabriel's Horn" — finite volume, infinite surface area (Torricelli, 1640s).

The horn is y = 1/x for x >= 1, spun around the x-axis: volume = pi (about 3.14 cubic units), surface area infinite.
The paradox: you can fill it with a finite amount of paint, but you could never paint its surface. Script kept to
facts that are standard and uncontested. Same structure as The Infinite Hotel.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="g1", scene="horn", text="This horn holds just a few cans of paint. But its surface is so big, you "
                                     "could never paint it."),
    dict(id="g2", scene="horn", text="It's called Gabriel's Horn. Take one simple curve, and spin it. The horn goes "
                                     "on forever, getting thinner and thinner."),
    dict(id="g3", scene="fill", text="Add up the space inside, and you get a fixed number. About "
                                     "[three point one four.|3.14.] So a few cans fill it, all the way to the tip."),
    dict(id="g4", scene="surface", text="But add up the surface, and it never stops growing. It's infinite."),
    dict(id="g5", scene="painter", text="So I can fill it, but I can't paint it?", speaker="sam", pace=0.92),
    dict(id="g6", scene="painter", text="Exactly.", gap=0.25),
    dict(id="g7", scene="name", text="Italian mathematician Evangelista Torricelli found it in the "
                                     "[sixteen forties,|1640s,] and people have argued about it ever since."),
    dict(id="g8", scene="end", text="So... can you paint it, or not?", pace=0.95),
]

METADATA = dict(
    title="You Can FILL This Horn… But You Can Never PAINT It 🎺🤯",
    alt_titles=["The Horn With Infinite Surface (Gabriel's Horn) 🤯", "A Few Cans Fill It… Infinity Can't Paint It 🎺"],
    description="""This horn holds just a few cans of paint… but its surface is so big you could never paint it. 🎺

It's called Gabriel's Horn: take the curve y = 1/x and spin it around. It goes on forever, getting thinner and thinner. The space inside adds up to a fixed number (pi, about 3.14), but the surface area never stops growing: it's infinite. 🤯

Italian mathematician Evangelista Torricelli found it in the 1640s, and people have argued about it ever since.

💬 So… can you paint it, or not? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Paradox", "#Math", "#Infinity"],
    tags=["gabriel's horn", "torricelli's trumpet", "painter's paradox", "infinity", "math paradox", "paradox",
          "calculus", "mind blowing math", "math shorts", "interestingly strange"],
    pinned_comment="Can you paint it or not? 🎺 Most people get this wrong… explain your answer 👇",
)

BG, GRID = hexc("#1f2a4d"), hexc("#2b3866")
GOLD, GOLD_D, GOLD_L = hexc("#f2c14e"), hexc("#b9862a"), hexc("#ffe7a3")
PAINT = hexc("#4fb3e8")
CREAM = hexc("#f4efe1")
YEL = hexc("#ffd23f")
PINK = hexc("#ff7aa8")
AX = 700           # horn axis (y)
X0 = 90            # mouth of the horn
R0 = 230           # mouth radius
STEP = 75          # px per unit of x


def hx(u):
    return X0 + (u - 1) * STEP


def hr(u):
    return R0 / u


def bg(cr, t, keys, dur=0.14):
    cr.set_source_rgba(*BG)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=dur)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    cr.set_line_width(2)
    cr.set_source_rgba(*GRID)
    for k in range(-20, 80):
        cr.move_to(k * 60, -600)
        cr.line_to(k * 60, 2200)
        cr.move_to(-1200, k * 60 - 600)
        cr.line_to(5000, k * 60 - 600)
    cr.stroke()


def infinity(cr, x, y, s, col, lw=8):
    cr.save()
    cr.translate(x, y)
    for k in range(121):
        a = k / 120 * 2 * math.pi
        d = 1 + math.sin(a) ** 2
        px, py = s * math.cos(a) / d, s * math.sin(a) * math.cos(a) / d
        (cr.move_to if k == 0 else cr.line_to)(px, py)
    cr.restore()
    cr.set_source_rgba(*col)
    cr.set_line_width(lw)
    cr.stroke()


def horn(cr, t, umax=60.0, fill=0.0, spin=0.0, grow=1.0):
    """The horn from u=1 to umax. `fill` (0-1) = how far the paint reaches; `grow` reveals it left to right."""
    import cairo
    us = [1 + k * 0.05 for k in range(int((umax - 1) / 0.05))]
    us = [u for u in us if hx(u) <= hx(1) + (hx(umax) - hx(1)) * grow]
    if len(us) < 2:
        return
    top = [(hx(u), AX - hr(u)) for u in us]
    bot = [(hx(u), AX + hr(u)) for u in reversed(us)]
    cr.move_to(*top[0])
    for p in top[1:] + bot:
        cr.line_to(*p)
    cr.close_path()
    g = cairo.LinearGradient(0, AX - R0, 0, AX + R0)
    g.add_color_stop_rgba(0, *GOLD_L)
    g.add_color_stop_rgba(0.45, *GOLD)
    g.add_color_stop_rgba(1, *GOLD_D)
    cr.set_source(g)
    cr.fill_preserve()
    cr.set_source_rgba(*INK)
    cr.set_line_width(4)
    cr.stroke()
    # rings, so it reads as a 3D horn (they drift along when it spins)
    for k in range(14):
        u = 1 + ((k * 0.9 + spin) % 13)
        if hx(u) > top[-1][0]:
            continue
        cr.save()
        cr.translate(hx(u), AX)
        cr.scale(max(0.15, hr(u) * 0.18 / max(hr(u), 1)) * 1.0, 1.0)
        cr.arc(0, 0, hr(u), -math.pi / 2, math.pi / 2)
        cr.restore()
        cr.set_source_rgba(*hexc("#8a6420", 0.55))
        cr.set_line_width(2.5)
        cr.stroke()
    # paint inside
    if fill > 0:
        uf = 1 + (umax - 1) * fill
        pu = [u for u in us if u <= uf]
        if len(pu) > 1:
            cr.move_to(hx(pu[0]), AX - hr(pu[0]) * 0.86)
            for u in pu[1:]:
                cr.line_to(hx(u), AX - hr(u) * 0.86)
            for u in reversed(pu):
                cr.line_to(hx(u), AX + hr(u) * 0.86)
            cr.close_path()
            cr.set_source_rgba(*hexc("#4fb3e8", 0.85))
            cr.fill()
    # the mouth
    cr.save()
    cr.translate(hx(1), AX)
    cr.scale(0.22, 1.0)
    cr.arc(0, 0, R0, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(*hexc("#3a2a10"))
    cr.fill_preserve()
    cr.set_source_rgba(*INK)
    cr.set_line_width(4)
    cr.stroke()


def can(cr, x, y, s, tip=0.0):
    with at(cr, x, y, s, rot=tip):
        shape(cr, rrect_pts(-46, -60, 92, 120, 10, 12), hexc("#d9dde3"), seed=4000, amp=0.3, lw=4)
        shape(cr, rrect_pts(-46, -20, 92, 46, 4, 10), PAINT, seed=4001, amp=0.2, lw=3)
        write(cr, [("PAINT", WHITE)], 0, 12, 24, align="center", bold=True)
        line(cr, [(-40, -60), (0, -100), (40, -60)], 4, INK, seed=4002, amp=0.2)


def counter(cr, t, x, y, label, value, col):
    with at(cr, x, y, 1.0):
        shape(cr, rrect_pts(-170, -60, 340, 120, 18, 14), hexc("#141b33"), seed=4100, amp=0.3, lw=4, stroke=CREAM)
        write(cr, [(label, CREAM)], 0, -18, 30, align="center", bold=True)
        if value == "INF":
            infinity(cr, 0, 30, 64, col, lw=9)
        else:
            write(cr, [(value, col)], 0, 44, 52, align="center", bold=True)


def scene_horn(cr, t, tl):
    A = tl.at
    keys = [(0, (1.15, 330, 700)), (A("g1", "few"), (1.0, 360, 760)), (A("g1", "surface"), (1.4, 300, 640)),
            (A("g1", "never"), (1.0, 360, 700)),
            (A("g2"), (1.0, 360, 700)), (A("g2", "gabriel's"), (1.3, 360, 520)), (A("g2", "spin"), (1.0, 360, 700)),
            (A("g2", "forever,"), (1.0, 1200, 700)), (A("g2", "thinner."), (1.2, 2400, 700))]
    bg(cr, t, keys, dur=0.4)
    grow = 1.0 if t < A("g2", "curve,") else 0.15 + 0.85 * ease_out(seg(t, A("g2", "spin"), A("g2", "forever,") + 0.5))
    if t < A("g2"):
        grow = 1.0
    horn(cr, t, umax=45, spin=t * 2 if t >= A("g2", "spin") else 0, grow=grow)
    if A("g1", "few") <= t < A("g2"):
        can(cr, 200, 1080, 1.1)
        can(cr, 330, 1100, 1.0)
    if A("g2", "gabriel's") <= t < A("g2", "spin"):
        with at(cr, 360, 420, max(0.85, pop(t, A("g2", "gabriel's"), 0.25)), rot=-0.03):
            write(cr, [("GABRIEL'S HORN", YEL)], 0, 0, 64, align="center", bold=True)
    hl(cr, t, [("fill it: ", INK), ("EASY", hexc("#2e9e52"))], 215, 70, 0.0, end=A("g1", "surface") - 0.05, bold=True,
       sound=False)
    hl(cr, t, [("paint it: ", INK), ("NEVER", RED)], 215, 70, A("g1", "surface"), end=A("g2", "forever,") - 0.05,
       bold=True)
    hl(cr, t, [("it goes on ", INK), ("FOREVER", RED)], 215, 66, A("g2", "forever,"), bold=True)
    if t >= A("g2", "forever,"):
        _, fx, _ = camera(t, keys, dur=0.4)
        infinity(cr, fx + 120, 520, 90, YEL, lw=10)
        line(cr, [(fx - 160, 520), (fx + 10, 520)], 7, YEL, seed=4010, amp=0.3)
        line(cr, [(fx - 15, 500), (fx + 10, 520), (fx - 15, 540)], 7, YEL, seed=4011, amp=0.3)
    cue("whoosh", t, A("g2", "forever,"))


def scene_fill(cr, t, tl):
    A = tl.at
    keys = [(A("g3") - 0.2, (1.0, 360, 700)), (A("g3", "inside,"), (1.2, 260, 700)), (A("g3", "3.14."), (1.0, 360, 700)),
            (A("g3", "cans"), (1.2, 300, 760)), (A("g3", "tip."), (1.0, 460, 700))]
    bg(cr, t, keys)
    fill = ease_out(seg(t, A("g3", "cans"), A("g3", "tip.", end=True) + 0.3))
    horn(cr, t, umax=20, fill=fill)
    can(cr, 300, 440, 1.0, tip=1.2 if A("g3", "cans") <= t else 0.0)
    if A("g3", "cans") <= t < A("g3", "tip.", end=True):
        line(cr, [(330, 470), (300, 560), (260, 630)], 14, PAINT, seed=4200, amp=0.3)
        cue("whoosh", t, A("g3", "cans"))
    if t >= A("g3", "3.14."):
        with at(cr, 420, 1140, max(0.85, pop(t, A("g3", "3.14."), 0.25))):
            counter(cr, t, 0, 0, "SPACE INSIDE", "3.14", hexc("#6fd67a"))
    hl(cr, t, [("inside: a ", INK), ("FIXED", hexc("#2e9e52")), (" number", INK)], 215, 60, A("g3", "inside,"),
       end=A("g3", "cans") - 0.05, bold=True)
    hl(cr, t, [("a few cans ", INK), ("FILL IT", hexc("#2e9e52"))], 215, 64, A("g3", "cans"), bold=True)


def scene_surface(cr, t, tl):
    A = tl.at
    keys = [(A("g4") - 0.2, (1.0, 360, 700)), (A("g4", "surface,"), (1.1, 360, 760)), (A("g4", "growing."), (1.0, 900, 700)),
            (A("g4", "infinite."), (1.15, 900, 760))]
    bg(cr, t, keys, dur=0.3)
    horn(cr, t, umax=45, fill=1.0)
    # the surface keeps adding up
    k = max(0.0, t - A("g4", "surface,"))
    val = int(10 ** min(9, 1 + k * 3.2))
    label = "INF" if t >= A("g4", "infinite.") else f"{val:,}"
    with at(cr, 360 if t < A("g4", "growing.") else 900, 1130, 1.0):
        counter(cr, t, 0, 0, "SURFACE", label, PINK)
    if A("g4", "surface,") <= t:
        cue("pop", t, A("g4", "surface,"))
    hl(cr, t, [("the surface ", INK), ("NEVER STOPS", RED)], 215, 60, A("g4", "surface,"), end=A("g4", "infinite.") - 0.05,
       bold=True)
    hl(cr, t, [("it's ", INK), ("INFINITE", RED)], 215, 76, A("g4", "infinite."), bold=True)
    cue("hit", t, A("g4", "infinite."))


def scene_painter(cr, t, tl):
    A = tl.at
    keys = [(A("g5") - 0.2, (1.2, 420, 820)), (A("g5", "fill"), (1.0, 360, 800)), (A("g5", "paint"), (1.25, 460, 860)),
            (A("g6"), (1.1, 400, 820))]
    bg(cr, t, keys)
    horn(cr, t, umax=20, fill=1.0)
    shocked = t >= A("g6")
    mouth = "o" if shocked else "smirk"
    if tl.speaking("sam", t):
        mouth = "o" if int(t * 12) % 2 else "smirk"
    person(cr, "sam", 560, 1080, t, facing=-1, arms=("point", "chin") if not shocked else ("face", "down"),
           eyes="wide" if shocked else "sly", mouth=mouth, scale=1.5, sweat=shocked)
    hl(cr, t, [("fill it... but ", INK), ("CAN'T", RED), (" paint it?", INK)], 215, 52, A("g5", "fill"),
       end=A("g6") - 0.05, bold=True)
    stamp(cr, t, A("g6"), "EXACTLY.", dur=0.7, y=330)
    cue("hit", t, A("g6"))


def scene_name(cr, t, tl):
    A = tl.at
    keys = [(A("g7") - 0.2, (1.0, 360, 660)), (A("g7", "torricelli"), (1.3, 360, 560)), (A("g7", "1640s,"), (1.0, 360, 640)),
            (A("g7", "argued"), (1.0, 400, 680))]
    bg(cr, t, keys)
    horn(cr, t, umax=20, spin=t * 2)
    with at(cr, 360, 420, max(0.85, pop(t, A("g7", "torricelli"), 0.3)), rot=-0.03):
        shape(cr, rrect_pts(-270, -80, 540, 160, 18, 14), CREAM, seed=4400, amp=0.4, lw=5)
        write(cr, [("EVANGELISTA TORRICELLI", INK)], 0, -8, 40, align="center", bold=True)
        write(cr, [("1640s", RED)], 0, 52, 48, align="center", bold=True)
    hl(cr, t, [("argued about ", INK), ("EVER SINCE", RED)], 215, 64, A("g7", "argued"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("g8") - 0.2, (1.1, 360, 700)), (A("g8", "paint"), (1.5, 300, 700)), (A("g8", "not?"), (1.1, 360, 760))]
    bg(cr, t, keys)
    horn(cr, t, umax=20, fill=0.5 + 0.5 * math.sin(t * 2) ** 2)
    for k, (lab, col, x) in enumerate((("YES", hexc("#2e9e52"), 200), ("NO", hexc("#e0483d"), 520))):
        if t >= A("g8", "not?"):
            with at(cr, x, 1110, max(0.85, pop(t, A("g8", "not?") + k * 0.12, 0.25))):
                shape(cr, rrect_pts(-110, -46, 220, 92, 46, 14), col, seed=4500 + k, amp=0.3, lw=4)
                write(cr, [(lab, WHITE)], 0, 16, 48, align="center", bold=True)
    hl(cr, t, [("can you ", INK), ("PAINT", RED), (" it?", INK)], 215, 70, A("g8"), bold=True, underline=True)
    stamp(cr, t, A("g8", "not?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"horn": scene_horn, "fill": scene_fill, "surface": scene_surface, "painter": scene_painter, "name": scene_name,
     "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
