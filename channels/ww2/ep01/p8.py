"""WW2 Episode 1, package P8 (script lines 117-131, SHOTLIST.md C7-S10 .. C8-S13): the end of the war in the Pacific,
the cost, what came after, and the closing question. Every beat sits on the shared clock's line and sentence times.

    /home/user/.venv-main/bin/python channels/ww2/ep01/render_pkg.py P8 --sheet       # review
    /home/user/.venv-main/bin/python channels/ww2/ep01/render_pkg.py P8               # final (once T.estimated is False)

Shots (line: picture):
    117  red arrows into Manchuria; Manchukuo floods red                                                8 AUG 1945
    118  the second flash over a distant skyline (P1's city shot as a callback), NAGASAKI                9 AUG 1945
    119  on black, in silence: AS MANY AS 200,000                                                             1945
    120  a family kneeling round the radio, heads bowed (helper 1's radio_family)                         15 AUG 1945
    121  the USS Missouri's deck: the signing table, a slow pull back                                     2 SEPT 1945
    C8   CHAPTER 8 AFTER THE WAR
    122  a slow pull back over a muted grey world
    123  SOVIET UNION counter to ~27,000,000; 123b: CHINA 15,000,000+ beside it
    124  the cold-open counter returns (P1's) and settles on 60-85 MILLION; "Most of them civilians." strip
    125  a generic round table, many nations as plain colour chips: UNITED NATIONS, 1945 (no logo)
    126  the courtroom, defendants in the dock: NUREMBERG, then TOKYO
    127  a US and a Soviet soldier turn back to back as the world map splits blue and red
    128  the map pulls back to the whole war
    129  three poster cards slide in; 130: each lights as it is named; 131: they hold, the comment strip,
         and the package ends ~0.5 s after the last word
"""
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from channels.ww2.kit.core import (H, LABEL, SLAB, STENCIL, TITLE, W, back_out, cairo, chapter_card, clamp01, col,  # noqa: E402
                                   counter, date_stamp, ease_in, ease_out, lerp, paper, print_finish, push_in, rays,
                                   seg, smooth, text)
from channels.ww2.ep01.timing import Timing, package_span  # noqa: E402
from channels.ww2.kit import fx, props, sets, setpieces  # noqa: E402
from channels.ww2.kit.maps import Map  # noqa: E402
from channels.ww2.kit.stick import Figure  # noqa: E402

T = Timing()
A, B = package_span("P8", T)


def L(i):
    return T.line(str(i))


ORDER = T.order


def cut(i):
    """The cut before line i (halfway through the pause before it)."""
    k = ORDER.index(str(i))
    return (T.line(ORDER[k - 1]).end + L(i).start) / 2


def at(i, u):
    ln = L(i)
    return ln.start + ln.dur * u


def sent(i, k):
    try:
        return T.sentence(str(i), k).start
    except (IndexError, KeyError):
        return at(i, 0.6)


CARD = T.chapter("C8").card


# ---------------------------------------------------------------- helpers (as P2's)
def push(cr, t, t0, t1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2):
    z = push_in(t, t0, t1, z0, z1)
    cr.translate(cx, cy)
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def backdrop(cr, t, tone=None, ray="khaki", ray_a=0.14, cy=H * 0.6):
    paper(cr)
    if tone:
        cr.set_source_rgba(*col(tone, 0.55))
        cr.paint()
    if ray_a:
        rays(cr, t, W / 2, cy, n=28, color=ray, alpha=ray_a)


def caption(cr, s, x, y, t, t0, size=56, color="cream", t_out=None):
    a = ease_out(seg(t, t0, t0 + 0.4))
    if t_out is not None:
        a *= 1 - ease_in(seg(t, t_out - 0.25, t_out))
    if a > 0:
        text(cr, s, x, y, size, font=STENCIL, color=color, alpha=a, outline="ink", outline_w=size * 0.16,
             spacing=size * 0.12)


def strip(cr, t, t0, s, y=H - 150, size=64, color="ink", fg="cream"):
    u = ease_out(seg(t, t0, t0 + 0.45))
    if u <= 0:
        return
    cr.rectangle(0, y - size * 1.05, W * u, size * 1.6)
    cr.set_source_rgba(*col(color, 0.92))
    cr.fill()
    text(cr, s, W / 2, y, size, font=SLAB, color=fg, alpha=u, spacing=size * 0.05)


# ---------------------------------------------------------------- maps
S117 = (A, cut(118))
MAN = Map("pacific", era="1942", sides={"philippines": "allies", "burma": "allies", "png": "allies",
                                        "solomons": "allies"})
MAN.view("manchuria", S117[0], zoom=2.6)
MAN.camera_key(S117[1], (125.0, 44.5), 2.9)
MAN.arrows("manchuria_1945", S117[0] + 0.3, S117[0] + 1.8, stagger=0.2)
MAN.side("manchukuo", S117[0] + 1.0, "soviet", origin=(125.0, 46.5), dur=2.2)
MAN.label("SOVIET UNION", S117[0], lonlat=(122.0, 52.0), size=44)
MAN.label("MANCHURIA", S117[0] + 0.6, lonlat=(126.0, 45.2), size=40)

S122 = (CARD[1], cut(123))
GREY = Map("world", muted=0.85)
GREY.camera_key(S122[0], (20.0, 35.0), 1.7)
GREY.camera_key(S122[1], (15.0, 20.0), 1.05)

S127 = (cut(127), cut(128))
SPLIT = Map("world", compass=False)
SPLIT.camera_key(S127[0], (20.0, 40.0), 1.6)
SPLIT.camera_key(S127[1], (25.0, 40.0), 1.75)
SPLIT.side("nato_1949", at(127, 0.55), "allies", origin=(-40.0, 45.0), dur=1.6, occupied=False)
SPLIT.side("warsaw_pact", at(127, 0.55), "soviet", origin=(60.0, 55.0), dur=1.6, occupied=False)

S128 = (cut(128), cut(129))
WAR = Map("world")
for g, sd, occ in (("axis_1942_home", "germany", False), ("axis_1942_occupied", "germany", True),
                   ("axis_minors", "italy", False), ("allies_1942", "allies", False), ("ussr", "soviet", False)):
    WAR.side(g, -1e9 + 1, sd, occupied=occ)
WAR.side("jpn", -1e9 + 1, "japan", occupied=False)
WAR.side("chn", -1e9 + 1, "china", occupied=False)
WAR.side("ita", -1e9 + 1, "italy", occupied=False)
WAR.camera_key(S128[0], (25.0, 40.0), 2.0)
WAR.camera_key(S128[1], (40.0, 20.0), 0.95)

# ---------------------------------------------------------------- figures, props, sets
DECK = sets.ShipDeck(horizon=560, mode="day")
TABLE = props.SigningTable(x=W / 2, y=900, scale=1.5)
US_OFF = [Figure(nation="usa", x=x, y=930, scale=0.85, facing=f, seed=s) for x, f, s in ((560, 1, 11), (380, 1, 12))]
DELEGATES = [Figure(civilian="hat", x=x, y=930, scale=0.85, facing=-1, seed=s, color=None) for x, s in
             ((1360, 13), (1540, 14))]
SIGNER = Figure(civilian="hat", x=W / 2 + 115, y=880, scale=0.85, facing=-1, seed=15)
LEAN_SIGN = dict(lean=0.32, nod=0.3, sh_n=1.05, el_n=0.9, sh_f=0.7, el_f=0.85)   # standing, bent over the table
COURT = sets.Courtroom(horizon=600)
DOCK = [Figure(civilian="hat", x=560 + 140 * k, y=860 - 70 * (k % 2), scale=0.62, facing=1, seed=20 + k)
        for k in range(8)]
GI = Figure(nation="usa", x=W / 2 - 150, y=1010, scale=1.25, facing=-1, seed=31)
RED = Figure(nation="soviet", x=W / 2 + 150, y=1010, scale=1.25, facing=1, seed=32)
DELEGATES_UN = [Figure(civilian=c, x=0, y=0, scale=0.5, facing=1, seed=40 + k)
                for k, c in enumerate(["hat", "flatcap", "hat", "scarf", "hat", "hat", "flatcap", "hat"])]


# ---------------------------------------------------------------- shots
def shot117(cr, t, t0, t1):
    paper(cr)
    MAN.draw(cr, t)


def shot118(cr, t, t0, t1):
    from channels.ww2.ep01 import p1
    p1.s07_city(cr, t, t0, t1, at(118, 0.62))                          # the flash on "destroys"
    caption(cr, "NAGASAKI", W / 2, 150, t, t0 + 0.3, size=64, color="cream")


def shot119(cr, t, t0, t1):
    cr.set_source_rgba(*col("ink"))
    cr.paint()
    a = ease_out(seg(t, t0 + 0.3, t0 + 1.2))
    b = ease_out(seg(t, at(119, 0.55), at(119, 0.55) + 1.0))
    text(cr, "AS MANY AS", W / 2, H / 2 - 120, 60, font=STENCIL, color="cream", alpha=a, spacing=10)
    text(cr, "200,000", W / 2, H / 2 + 80, 230, font=TITLE, color="cream", alpha=b)
    text(cr, "PEOPLE", W / 2, H / 2 + 190, 56, font=STENCIL, color="cream", alpha=b * 0.85, spacing=10)


def shot120(cr, t, t0, t1):
    backdrop(cr, t, tone="paper_dk", ray=None, ray_a=0)
    cr.save()
    push(cr, t, t0, t1, 1.0, 1.08, cy=H * 0.75)
    cr.rectangle(0, 0, W, H)                                           # a dim room
    cr.set_source_rgba(*col("ink", 0.35))
    cr.fill()
    for k in range(7):                                                 # a paper-screen wall behind them
        x = k * 290 - 60
        cr.rectangle(x, 150, 270, 640)
        cr.set_source_rgba(*col("cream", 0.16))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink", 0.7))
        cr.set_line_width(8)
        cr.stroke()
        for j in range(1, 4):
            cr.move_to(x, 150 + j * 160)
            cr.line_to(x + 270, 150 + j * 160)
        cr.move_to(x + 135, 150)
        cr.line_to(x + 135, 790)
        cr.set_line_width(4)
        cr.stroke()
    cr.rectangle(0, 790, W, H - 790)                                   # the floor
    cr.set_source_rgba(*col("#6b5a3e", 0.9))
    cr.fill()
    setpieces.radio_family(cr, t, x=W / 2, ground=1010, scale=1.25, on=True)
    cr.restore()


def shot121(cr, t, t0, t1):
    cr.save()
    push(cr, t, t0, t1, 1.14, 1.0, cy=H * 0.62)                        # a slow pull back
    DECK.draw(cr, t)
    for f in US_OFF:
        f.draw(cr, t, track=[(0.0, "stand")])
    for f in DELEGATES:
        f.draw(cr, t, track=[(0.0, "head_down")])
    SIGNER.draw(cr, t, track=[(0.0, "stand"), (t0 + 0.6, LEAN_SIGN)])       # behind the table, bent over it
    TABLE.draw(cr, t, signed=smooth(seg(t, t0 + 1.2, t1 - 1.0)))
    cr.restore()
    caption(cr, "USS MISSOURI, TOKYO BAY", W / 2, 140, t, t0 + 0.3, size=54)


def card(cr, t, t0, t1):
    backdrop(cr, t, ray="gold", ray_a=0.2, cy=H / 2)
    chapter_card(cr, t, t0, 8, "After the war", dur=t1 - t0)


def shot122(cr, t, t0, t1):
    paper(cr)
    GREY.draw(cr, t)


def shot123(cr, t, t0, t1):
    backdrop(cr, t, tone="paper_dk", ray="ink", ray_a=0.06, cy=H / 2)
    s1 = L("123b").start
    counter(cr, t, t0 + 0.4, L(123).end - 0.3, 27_000_000, W * 0.3, H * 0.55, size=150, color="soviet",
            label=None)
    caption(cr, "SOVIET UNION", W * 0.3, H * 0.55 - 190, t, t0 + 0.3, size=54, color="cream")
    if t > s1:
        counter(cr, t, s1 + 0.1, L("123b").end - 0.2, 15_000_000, W * 0.72, H * 0.55, size=150, color="china")
        caption(cr, "CHINA", W * 0.72, H * 0.55 - 190, t, s1, size=54, color="cream")
        if t > L("123b").end - 0.2:
            text(cr, "+", W * 0.72 + 360, H * 0.55 - 40, 120, font=TITLE, color="china", outline="paper",
                 outline_w=10, alpha=ease_out(seg(t, L("123b").end - 0.2, L("123b").end + 0.2)))
    text(cr, "AROUND", W * 0.3, H * 0.55 + 90, 40, font=STENCIL, color="ink_soft",
         alpha=ease_out(seg(t, t0 + 0.4, t0 + 0.8)), spacing=8)


def shot124(cr, t, t0, t1):
    from channels.ww2.ep01 import p1
    p1.s06_counter(cr, t, t0, t1)
    strip(cr, t, sent(124, 1), "MOST OF THEM CIVILIANS", y=H - 140, size=66)


def shot125(cr, t, t0, t1):
    backdrop(cr, t, ray="allies", ray_a=0.12, cy=H * 0.35)
    cr.save()
    push(cr, t, t0, t1, 1.0, 1.06, cy=H * 0.6)
    chips = ["allies", "soviet", "china", "gold", "olive", "khaki", "alert", "sea_dk", "fire", "ink_soft", "allies",
             "snow"]
    for k, c in enumerate(chips):                                      # nations as plain colour chips on poles
        x = 220 + k * 135
        cr.rectangle(x, 230, 6, 300)
        cr.set_source_rgba(*col("ink"))
        cr.fill()
        wave = 6 * math.sin(t * 2.4 + k)
        cr.rectangle(x + 6, 232 + wave * 0.3, 92, 58)
        cr.set_source_rgba(*col(c))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(3)
        cr.stroke()
    cx, cy, rx, ry = W / 2, 820, 620, 150                              # the round table, in perspective
    for k, f in enumerate(DELEGATES_UN):                               # delegates seated behind it
        a = math.pi + (k + 0.5) / len(DELEGATES_UN) * math.pi
        x, y = cx + rx * 0.92 * math.cos(a), cy + ry * 0.92 * math.sin(a) + 40
        f.draw(cr, t, track=[(0.0, "sit")], move=[(0.0, x, y)])
    cr.save()
    cr.translate(cx, cy)
    cr.scale(1, ry / rx)
    cr.arc(0, 0, rx, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(*col("#6e5a3e"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(6)
    cr.stroke()
    cr.save()
    cr.translate(cx, cy)
    cr.scale(1, ry / rx)
    cr.arc(0, 0, rx * 0.55, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(*col("allies", 0.85))
    cr.fill()
    cr.restore()
    caption(cr, "THE UNITED NATIONS, 1945", W / 2, 140, t, t0 + 0.3, size=56)


def shot126(cr, t, t0, t1):
    tokyo = at(126, 0.62)                                              # "...and Japanese leaders in Tokyo"
    cr.save()
    push(cr, t, t0 if t < tokyo else tokyo, t1 if t >= tokyo else tokyo, 1.0, 1.05, cy=H * 0.6)
    COURT.draw(cr, t)
    for k, f in enumerate(DOCK if t < tokyo else DOCK[:6]):
        f.draw(cr, t, track=[(0.0, "head_down")])
    cr.restore()
    if t < tokyo:
        caption(cr, "NUREMBERG, 1945-46", W / 2, 140, t, t0 + 0.3, size=56, t_out=tokyo)
    else:
        cr.set_source_rgba(*col("sea_dk", 0.18))                       # a cooler print for the second courtroom
        cr.paint()
        caption(cr, "TOKYO, 1946-48", W / 2, 140, t, tokyo, size=56)


def shot127(cr, t, t0, t1):
    paper(cr)
    SPLIT.draw(cr, t)
    cr.rectangle(0, 980, W, H - 980)                                   # the ground band under the two soldiers
    cr.set_source_rgba(*col("ink", 0.85))
    cr.fill()
    turn = at(127, 0.5)
    GI.facing, RED.facing = (1, -1) if t < turn else (-1, 1)          # allies face each other, then turn back to back
    GI.draw(cr, t, track=[(0.0, "stand"), (turn, "arms_crossed")])
    RED.draw(cr, t, track=[(0.0, "stand"), (turn, "arms_crossed")])
    caption(cr, "THE COLD WAR", W / 2, 140, t, turn + 0.3, size=60)


def shot128(cr, t, t0, t1):
    paper(cr)
    WAR.draw(cr, t)


CARDS = [("1", "BARBAROSSA", "JUNE 1941", "germany"), ("2", "AMERICA JOINS", "DECEMBER 1941", "allies"),
         ("3", "STALINGRAD", "1942-43", "soviet")]


def shot129(cr, t, t0, t1):
    backdrop(cr, t, ray="gold", ray_a=0.18, cy=H * 0.55)
    text(cr, "WHEN DID GERMANY REALLY LOSE THE WAR?", W / 2, 175, 50, font=SLAB, color="ink", outline="cream",
         outline_w=10, alpha=ease_out(seg(t, t0 + 0.1, t0 + 0.5)), spacing=2)
    names = [sent(130, 0), sent(130, 1), sent(130, 2)]
    for k, (num, title, sub, side) in enumerate(CARDS):
        tin = t0 + 0.2 + 0.25 * k
        u = back_out(seg(t, tin, tin + 0.4))
        if u <= 0:
            continue
        lit = ease_out(seg(t, names[k], names[k] + 0.3))
        now = lit * (1 - 0.35 * seg(t, names[k] + 1.6, names[k] + 2.0)) if t < L(131).start else 1.0
        cx = W / 2 + (k - 1) * 560
        cy = H / 2 + 80 + (1 - u) * 600
        poster_card(cr, cx, cy, num, title, sub, side, now, t)


def poster_card(cr, cx, cy, num, title, sub, side, lit, t):
    w, h = 470, 560
    s = 1.0 + 0.06 * lit
    cr.save()
    cr.translate(cx, cy)
    cr.scale(s, s)
    cr.rectangle(-w / 2 + 14, -h / 2 + 16, w, h)                        # hard shadow
    cr.set_source_rgba(*col("ink", 0.55))
    cr.fill()
    cr.rectangle(-w / 2, -h / 2, w, h)
    cr.set_source_rgba(*col("gold" if lit > 0.5 else "cream"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(8)
    cr.stroke()
    cr.rectangle(-w / 2, -h / 2, w, 150)                                # the side-colour band with the number
    cr.set_source_rgba(*col(side))
    cr.fill()
    text(cr, num, 0, -h / 2 + 125, 120, font=TITLE, color="cream")
    icon(cr, num, 0, 0, lit)
    text(cr, title, 0, h / 2 - 112, 46 if len(title) < 12 else 40, font=SLAB, color="ink", spacing=2)
    text(cr, sub, 0, h / 2 - 50, 34, font=STENCIL, color="ink_soft", spacing=5)
    cr.restore()


def icon(cr, num, x, y, lit):
    """1: an arrow east; 2: a plain white star; 3: a snowflake (flat ink shapes)."""
    cr.save()
    cr.translate(x, y)
    cr.set_source_rgba(*col("ink"))
    if num == "1":
        cr.move_to(-120, -22)
        cr.line_to(40, -22)
        cr.line_to(40, -60)
        cr.line_to(120, 0)
        cr.line_to(40, 60)
        cr.line_to(40, 22)
        cr.line_to(-120, 22)
        cr.close_path()
        cr.set_source_rgba(*col("germany"))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(5)
        cr.stroke()
    elif num == "2":
        props.star(cr, 0, 0, 82, color="cream", disc="allies")
    else:
        cr.set_line_width(12)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        for k in range(6):
            a = k * math.pi / 3
            cr.move_to(0, 0)
            cr.line_to(95 * math.cos(a), 95 * math.sin(a))
            for d in (0.55, 0.8):
                bx, by = 95 * d * math.cos(a), 95 * d * math.sin(a)
                for s in (-1, 1):
                    cr.move_to(bx, by)
                    cr.line_to(bx + 26 * math.cos(a + s * 0.9), by + 26 * math.sin(a + s * 0.9))
        cr.set_source_rgba(*col("sea_dk"))
        cr.stroke()
    cr.restore()


def shot131(cr, t, t0, t1):
    shot129(cr, t, cut(129), t1)
    strip(cr, t, L(131).start + 0.2, "YOUR ANSWER: 1, 2 OR 3?  TELL ME IN THE COMMENTS", y=H - 60, size=46)


# (start, end, draw, date tag)
SHOTS = [
    (S117[0], S117[1], shot117, "8 AUG 1945"),
    (cut(118), cut(119), shot118, "9 AUG 1945"),
    (cut(119), cut(120), shot119, "1945"),
    (cut(120), cut(121), shot120, "15 AUG 1945"),
    (cut(121), CARD[0], shot121, "2 SEPT 1945"),
    (CARD[0], CARD[1], card, None),
    (S122[0], S122[1], shot122, "1945"),
    (cut(123), cut(124), shot123, "1939-1945"),
    (cut(124), cut(125), shot124, "1939-1945"),
    (cut(125), cut(126), shot125, "1945"),
    (cut(126), cut(127), shot126, "1945-48"),
    (S127[0], S127[1], shot127, "1947"),
    (S128[0], S128[1], shot128, "1939-1945"),
    (cut(129), cut(131), shot129, "1939-1945"),
    (cut(131), B + 1.0, shot131, "1939-1945"),
]


def draw(cr, t):
    for i, (t0, t1, fn, tag) in enumerate(SHOTS):
        if t < t1 or i == len(SHOTS) - 1:
            break
    cr.save()
    fn(cr, t, t0, t1)
    cr.restore()
    if tag:
        prev = SHOTS[i - 1][3] if i > 0 else None
        date_stamp(cr, t, tag, start=t0 if tag != prev else -1e9)
    print_finish(cr, t)


def cues(T=T):
    """[(episode time, sfx, gain dB, pan)] for helper 7's mix. Line 119 stays silent (the number on black)."""
    c = [(S117[0] + 0.3, "tank", -12, 0.3), (S117[0] + 1.0, "page_whoosh", -12, 0.0),
         (at(118, 0.62), "explosion", -8, 0.0),
         (cut(120) + 0.2, "radio_static", -10, 0.0), (cut(120) + 0.6, "voice_crackle", -16, 0.0),
         (cut(121) + 0.1, "sea_waves", -14, 0.0), (cut(121) + 1.2, "typewriter", -22, 0.0),
         (CARD[0], "stamp", -6, 0.0),
         (cut(123) + 0.4, "clock_tick", -14, -0.3), (L("123b").start + 0.1, "clock_tick", -14, 0.3),
         (cut(124) + 0.1, "clock_tick", -12, 0.0),
         (cut(125) + 0.4, "door_slam", -14, 0.0),
         (cut(126) + 0.3, "door_slam", -12, 0.0), (at(126, 0.62), "door_slam", -12, 0.0),
         (at(127, 0.55), "page_whoosh", -10, 0.0),
         (cut(128), "page_whoosh", -10, 0.0),
         (cut(129) + 0.2, "page_whoosh", -10, -0.4), (cut(129) + 0.45, "page_whoosh", -10, 0.0),
         (cut(129) + 0.7, "page_whoosh", -10, 0.4),
         (sent(130, 0), "stamp", -8, -0.4), (sent(130, 1), "stamp", -8, 0.0), (sent(130, 2), "stamp", -8, 0.4),
         (L(131).start + 0.2, "stamp", -10, 0.0)]
    return sorted(c)
