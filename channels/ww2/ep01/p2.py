"""WW2 Episode 1, package P2 (script lines 17-35, SHOTLIST.md C1-S14 .. C2-S04): the 1930s grabs, Munich, the pact,
Danzig and the first strike of the Blitzkrieg. Every beat is placed relative to the line and sentence times of the
shared clock (timing.json via Timing()), so the package re-times itself when the voiced narration lands.

    /home/user/.venv-main/bin/python channels/ww2/ep01/render_pkg.py P2 --sheet       # review
    /home/user/.venv-main/bin/python channels/ww2/ep01/render_pkg.py P2               # final (once T.estimated is False)

Shots (line: picture):
    17  pull back from Germany to the world; Germany, Italy and Japan picked out in charcoal
    18  Mussolini's poster portrait under a Roman arch; the map arrow from Italy to Ethiopia, Ethiopia floods
    19  East Asia: Japan floods Manchuria (1931 stamp), then arrows push into China (1937 stamp), China's front holds
    20  a whip pan back to Europe, Germany's 1937 borders lit
    21  rows of marching soldiers multiply; tanks stamp in, fighters fly over
    22  the Rhineland strip floods grey under arrows across the Rhine (MARCH 1936)
    23  a British and a French soldier shrug side by side
    24  Austria floods grey (MARCH 1938)
    25  the Sudetenland's edge flashes and pulses
    26  the Munich table: Hitler, Mussolini, Chamberlain, Daladier, the Czech chair empty, a pen signs; the Sudetenland
        floods grey
    27  Chamberlain at the airliner door waving the paper, a cheering crowd, PEACE FOR OUR TIME
    28  the rest of Czechoslovakia floods grey (MARCH 1939); the paper crumples in close-up
    29  a drum hit: AUGUST 1939 slams in
    30-31 the pact (helper 1's leaders_pact beats on this clock): the handshake, crossed fingers, NON-AGGRESSION PACT
    32  the secret line splits Poland under SECRET; the Baltic states, Finland and Bessarabia tint red
    33  Danzig: the battleship's salvo (stand-in until P1's DANZIG set lands)
    C2  CHAPTER 2 LIGHTNING WAR card
    34  grey arrows sweep across Poland, which floods grey; a tank rolls through, a dive bomber overhead
    35  BLITZKRIEG slams over a newspaper; "Lightning war." underlines it with a bolt
"""
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from channels.ww2.kit.core import (H, LABEL, SLAB, STENCIL, TITLE, W, back_out, cairo, chapter_card, clamp01, col,  # noqa: E402
                                   date_stamp, ease_in, ease_out, lerp, paper, print_finish, push_in, rays, seg,
                                   shake, smooth, text, word_card)
from channels.ww2.ep01.timing import Timing, package_span  # noqa: E402
from channels.ww2.kit import fx, heads, props, setpieces, sets, things  # noqa: E402
from channels.ww2.kit.maps import SPLIT_1939, Map  # noqa: E402
from channels.ww2.kit.stick import Figure  # noqa: E402

T = Timing()
A, B = package_span("P2", T)


def L(i):
    return T.line(str(i))


def cut(i):
    """The cut before line i: halfway through the pause before it."""
    return (L(i - 1).end + L(i).start) / 2


def at(i, u):
    """A point u (0-1) through line i's speech."""
    ln = L(i)
    return ln.start + ln.dur * u


CARD = T.chapter("C2").card                                          # (start, end) of CHAPTER 2's card
GREY = "germany"


# ---------------------------------------------------------------- helpers
def push(cr, t, t0, t1, z1=1.06, cx=W / 2, cy=H / 2):
    """The slow push-in every shot carries (call inside save/restore)."""
    z = push_in(t, t0, t1, 1.0, z1)
    cr.translate(cx, cy)
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def outline(cr, m, t, names, color="gold", lw=7.0, alpha=1.0, halo=True):
    """Stroke regions of map m in screen-constant widths with its camera at t (a lit border / a flashing edge)."""
    if alpha <= 0:
        return
    (cx, cy), z = m.camera_at(t)
    cr.save()
    cr.translate(W / 2, H / 2)
    cr.scale(z, z)
    cr.translate(-cx, -cy)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    for n in names:
        cr.new_path()
        cr.append_path(m.paths[n])
        if halo:
            cr.set_source_rgba(*col(color, 0.35 * alpha))
            cr.set_line_width(lw * 3.2 / z)
            cr.stroke_preserve()
        cr.set_source_rgba(*col(color, alpha))
        cr.set_line_width(lw / z)
        cr.stroke()
    cr.restore()


def backdrop(cr, t, tone="paper", ray="khaki", ray_a=0.16, cx=W / 2, cy=H * 0.62):
    """A plain poster ground with a slow sunburst (never red)."""
    paper(cr)
    if tone != "paper":
        cr.set_source_rgba(*col(tone, 0.55))
        cr.paint()
    rays(cr, t, cx, cy, n=28, color=ray, alpha=ray_a)


def nametag(cr, s, x, y, t, t0, size=40, color="ink"):
    a = ease_out(seg(t, t0, t0 + 0.4))
    if a > 0:
        text(cr, s, x, y, size, font=STENCIL, color=color, alpha=a, outline="cream", outline_w=size * 0.18,
             spacing=size * 0.12)


def slam(cr, t, t0, s, x, y, size=150, color="alert", font=SLAB, tilt=-0.05, shadow=True):
    """A word that slams down with an overshoot and a hard shadow."""
    if t < t0:
        return
    u = back_out(seg(t, t0, t0 + 0.22))
    a = min(1.0, seg(t, t0, t0 + 0.08) * 1.0 + 0.2)
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    k = 1.7 - 0.7 * u
    cr.scale(k, k)
    if shadow:
        text(cr, s, 8, size * 0.36 + 10, size, font=font, color="ink", alpha=0.5 * a, spacing=size * 0.03)
    text(cr, s, 0, size * 0.36, size, font=font, color=color, alpha=a, outline="cream", outline_w=size * 0.1,
         spacing=size * 0.03)
    cr.restore()


# ---------------------------------------------------------------- the maps (built once, keyed on the clock)
# 17: the world, 1935
S17 = (A, cut(18))
WORLD = Map("world", sides={"deu": GREY, "ita": "italy", "jpn": "japan", "kor": "japan", "twn": "japan",
                            "gbr": "allies", "fra": "allies", **{c: "soviet" for c in
                                                                 ("rus", "ukr", "blr", "kaz", "uzb", "tkm", "kgz",
                                                                  "tjk", "geo", "arm", "aze")}},
            occupied={"kor", "twn"})
WORLD.view("world_europe", S17[0])
WORLD.camera_key(S17[0] + 0.25, (11.0, 50.5), 3.0)
WORLD.camera_key(S17[1], (25.0, 28.0), 1.0)
WORLD.label("GERMANY", at(17, 0.05), region="deu", size=40)
WORLD.label("ITALY", at(17, 0.45), region="ita", size=36)
WORLD.label("JAPAN", at(17, 0.65), region="jpn", size=40)

# 18b: Italy -> Ethiopia
S18A = (cut(18), at(18, 0.42))
S18B = (S18A[1], cut(19))
ETH = Map("europe", era="1936")
ETH.camera_key(S18B[0], (25.0, 30.0), 0.78)
ETH.camera_key(S18B[1], (31.0, 22.0), 0.92)
ETH.arrows("italy_ethiopia_1935", S18B[0] + 0.2, S18B[0] + 1.6)
ETH.side("ethiopia", S18B[0] + 1.4, "italy", origin=(39.0, 14.5), dur=1.3)
ETH.label("ITALY", S18B[0] + 0.1, lonlat=(12.6, 43.4), size=40)
ETH.label("ETHIOPIA", S18B[0] + 1.6, lonlat=(39.5, 8.6), size=40)
ETH.stamp("1935", (44.0, 15.5), S18B[0] + 1.5, size=70)

# 19: Manchuria 1931, China 1937
S19A = (cut(19), at(19, 0.47))
S19B = (S19A[1], cut(20))
MAN = Map("pacific", era="1937", sides={"manchukuo": "china", "china_occ": "china"}, occupied={"korea", "taiwan"})
MAN.view("manchuria", S19A[0])
MAN.camera_key(S19A[1], (124.0, 43.0), 3.25)
MAN.arrows("manchuria_1931", S19A[0] + 0.3, S19A[0] + 1.7)
MAN.side("manchukuo", S19A[0] + 0.8, "japan", origin=(121.8, 39.5), dur=1.6)
MAN.label("JAPAN", S19A[0], lonlat=(137.5, 37.0), size=40)
MAN.label("MANCHURIA", S19A[0] + 1.2, lonlat=(126.0, 46.5), size=40)
MAN.stamp("1931", (116.0, 47.5), S19A[0] + 1.0, size=70)
CHN = Map("pacific", era="1937")
CHN.view("china", S19B[0])
CHN.camera_key(S19B[1], (114.0, 31.5), 2.6)
CHN.arrows("china_1937", S19B[0] + 0.2, S19B[0] + 1.4, stagger=0.3)
CHN.side("china_occ", S19B[0] + 0.9, "japan", origin=(119.0, 36.0), dur=1.8)
CHN.front("china", S19B[0] + 2.4, S19B[0] + 120.0, side="china", width=8.0)      # holds (barely moves)
CHN.label("CHINA", S19B[0], lonlat=(104.0, 30.0), size=48)
CHN.stamp("1937", (122.5, 25.5), S19B[0] + 1.1, size=70)

# 20-28: Europe, 1935-39 (one map per state, each keyed on the clock)
S20 = (cut(20), cut(21))
EU20 = Map("europe", era="1936")
EU20.camera_key(S20[0], (34.0, 46.0), 1.3)
EU20.camera_key(S20[0] + 0.4, (11.5, 51.0), 2.1)                   # the whip pan
EU20.camera_key(S20[1], (11.5, 51.0), 2.22)

S22 = (cut(22), cut(23))
RH = Map("europe", era="1936")
RH.view("rhineland", S22[0])
RH.camera_key(S22[1], (7.6, 50.4), 4.35)
for k, path in enumerate([[(10.2, 51.3), (9.2, 51.1), (8.1, 51.0)], [(10.4, 50.2), (9.3, 50.15), (7.9, 50.1)],
                          [(10.1, 49.3), (9.1, 49.35), (8.0, 49.4)]]):
    RH.arrow(path, GREY, at(22, 0.25) + 0.2 * k, at(22, 0.25) + 0.2 * k + 1.0, width=52)
RH.side("rhineland", at(22, 0.3), GREY, origin=(8.9, 50.3), dur=2.4, occupied=False)
RH.label("RHINELAND", at(22, 0.15), lonlat=(6.6, 50.15), size=44, tilt=-0.08)
RH.city("Paris", S22[0], lonlat=(2.35, 48.86), label=False, pulse=False)

S24 = (cut(24), cut(25))
AU = Map("europe", era="1936", sides={"rhineland": GREY})
AU.view("central_europe", S24[0])
AU.camera_key(S24[1], (15.0, 49.0), 2.85)
AU.side("austria", at(24, 0.35), GREY, origin=(12.9, 48.2), dur=1.7)
AU.owner("austria", at(24, 0.35) + 1.7, "germany")
AU.label("AUSTRIA", at(24, 0.25), lonlat=(14.4, 47.55), size=44)
AU.city("Vienna", at(24, 0.45))

_after_austria = dict(sides={"rhineland": GREY, "austria": GREY}, owners={"austria": "germany"})
S25 = (cut(25), cut(26))
SU = Map("europe", era="1936", occupied={"austria"}, **_after_austria)
SU.camera_key(S25[0], (15.0, 49.6), 3.0)
SU.camera_key(S25[1], (14.6, 50.0), 3.2)
SU.label("SUDETENLAND", at(25, 0.3), lonlat=(13.4, 50.95), size=38, tilt=-0.1)
SU.label("CZECHOSLOVAKIA", at(25, 0.1), lonlat=(17.6, 49.2), size=36)

S26A = (cut(26), at(26, 0.55))
S26B = (S26A[1], cut(27))
SU2 = Map("europe", era="1936", occupied={"austria"}, **_after_austria)
SU2.camera_key(S26B[0], (14.8, 49.9), 3.1)
SU2.camera_key(S26B[1], (14.8, 49.9), 3.3)
SU2.side("sudeten", S26B[0] + 0.15, GREY, origin=(12.4, 50.2), dur=1.4)
SU2.owner("sudeten", S26B[0] + 1.6, "germany")
SU2.label("SUDETENLAND", S26B[0], lonlat=(13.4, 50.95), size=38, tilt=-0.1)

S28A = (cut(28), at(28, 0.55))
S28B = (S28A[1], cut(29))
CZ = Map("europe", era="1936", occupied={"austria", "sudeten"},
         sides={"rhineland": GREY, "austria": GREY, "sudeten": GREY},
         owners={"austria": "germany", "sudeten": "germany"})
CZ.camera_key(S28A[0], (16.5, 49.5), 2.7)
CZ.camera_key(S28A[1], (16.0, 49.6), 2.95)
CZ.side("czech", S28A[0] + 0.25, GREY, origin=(13.4, 50.0), dur=1.2)
CZ.owner("czech", S28A[0] + 1.45, "germany")
CZ.side("slovakia", S28A[0] + 0.6, "italy", occupied=False)                       # a separate, Axis-aligned state
CZ.owner("slovakia", S28A[0] + 0.6, "slovakia")
CZ.owner("carpatho", S28A[0] + 0.6, "hungary")
CZ.city("Prague", S28A[0] + 0.3)

# 32: the secret line; 34: Poland
S32 = (cut(32), cut(33))
SEC = Map("europe", era="1939")
SEC.camera_key(S32[0], (21.0, 54.0), 1.55)
SEC.camera_key(S32[1], (22.0, 54.5), 1.8)
SEC.secret_line(SPLIT_1939, at(32, 0.35), at(32, 0.35) + 1.5)
SEC.stamp("SECRET", (23.8, 53.1), at(32, 0.35) + 1.4, size=60)
SEC.side("baltics", at(32, 0.62), "soviet", origin=(28.0, 56.8), dur=1.2)
SEC.side("finland_1939", at(32, 0.66), "soviet", origin=(30.5, 61.5), dur=1.3)
SEC.side("bessarabia", at(32, 0.7), "soviet", origin=(29.6, 47.0), dur=1.0)
SEC.label("POLAND", S32[0], lonlat=(19.3, 51.9), size=44)
SEC.label("SOVIET UNION", S32[0], lonlat=(33.5, 56.0), size=44)

S34A = (CARD[1], at(34, 0.55))
S34B = (S34A[1], cut(35))
PL = Map("europe", era="1939")
PL.view("poland", S34A[0], zoom=2.3)
PL.camera_key(S34A[1], (20.4, 52.1), 2.6)
PL.arrows("poland_1939", S34A[0] + 0.05, S34A[0] + 0.9, stagger=0.12)
PL.side("poland_w", S34A[0] + 0.5, GREY, origin=(16.4, 52.0), dur=1.2)
PL.city("Warsaw", S34A[0] + 0.3)
PL.label("POLAND", S34A[0], lonlat=(19.6, 51.1), size=46)

# ---------------------------------------------------------------- figures and props (built once)
SHRUG_B = Figure(nation="britain", x=780, y=985, scale=1.25, facing=1, seed=4)
SHRUG_F = Figure(nation="france", x=1150, y=985, scale=1.25, facing=-1, seed=5)
CHAMBERLAIN = Figure(leader="chamberlain", prop="paper", x=0, y=0, scale=0.95, facing=-1, seed=6)
PLANE = things.Airliner(x=1250, y=900, scale=1.35, facing=-1, door=1.0)
TABLE = things.LongTable(x=W / 2, y=1060, scale=1.0, length=1700, chairs=5)
ROOM = sets.SigningRoom(kind="office")
SKY = sets.Sky(mode="day", horizon=820, clouds=4)
DAWN = sets.Sky(mode="dusk", horizon=640, clouds=3)
OCEAN = sets.Ocean(horizon=640)
SHIP = props.Battleship(x=980, y=820, scale=1.15, facing=-1, side="germany")
TANKS = [props.Tank(x=0, y=0, scale=s, facing=1, side="germany") for s in (0.9, 0.62)]
FIGHTERS = [props.Fighter(x=0, y=0, scale=0.55, facing=1, side="germany") for _ in range(3)]
STUKA = props.DiveBomber(x=0, y=0, scale=0.8, facing=1, side="germany")
FIELD_TANK = props.Tank(x=0, y=0, scale=1.25, facing=1, side="germany")
PAPER = things.Paper(x=W / 2, y=H / 2 - 20, scale=1.6, lines=("PEACE FOR", "OUR TIME"))
NEWS = things.Newspaper(x=W / 2 + 330, y=H / 2 + 60, scale=1.35, masthead="THE DAILY HERALD",
                        headline="POLAND INVADED", sub="Tanks and planes strike at dawn", date="SEPT 1939")


# ---------------------------------------------------------------- shots
def shot17(cr, t, t0, t1):
    paper(cr)
    WORLD.draw(cr, t)


def shot18a(cr, t, t0, t1):
    backdrop(cr, t, ray="gold", ray_a=0.2, cy=H * 0.42)
    cr.save()
    push(cr, t, t0, t1, 1.07)
    arch(cr, W / 2, 1000)
    heads.portrait(cr, t, "mussolini", W / 2 - 40, H + 30, height=980, expr="determined", turn=0.5)
    cr.restore()
    nametag(cr, "BENITO MUSSOLINI", W / 2, H - 70, t, t0 + 0.4, size=48, color="cream")


def arch(cr, cx, ground):
    """A Roman triumphal arch: one tall opening framing the portrait, an attic band, columns (flat khaki, ink key
    line, olive halftone shading)."""
    w, h, r = 1500, 1020, 400                                           # outer width/height, opening radius
    top_open = ground - 300 - 2 * r                                     # spring line of the opening's arch
    cr.new_path()
    cr.rectangle(cx - w / 2, ground - h, w, h)
    cr.move_to(cx + r, ground)                                          # the opening (cut out: even-odd)
    cr.line_to(cx + r, top_open + r)
    cr.arc_negative(cx, top_open + r, r, 0, math.pi)
    cr.line_to(cx - r, ground)
    cr.close_path()
    cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    cr.set_source_rgba(*col("khaki", 0.9))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink", 0.9))
    cr.set_line_width(6)
    cr.stroke()
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    for dx in (-w / 2 + 60, -r - 120, r + 70, w / 2 - 110):            # columns on the piers
        cr.rectangle(cx + dx, ground - h + 190, 50, h - 190)
        cr.set_source_rgba(*col("olive", 0.4))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink", 0.7))
        cr.set_line_width(3)
        cr.stroke()
    for y in (ground - h + 70, ground - h + 160):                       # the attic's two bands
        cr.rectangle(cx - w / 2 - 20, y, w + 40, 18)
        cr.set_source_rgba(*col("ink", 0.75))
        cr.fill()


def shot18b(cr, t, t0, t1):
    paper(cr)
    ETH.draw(cr, t)


def shot19a(cr, t, t0, t1):
    paper(cr)
    MAN.draw(cr, t)


def shot19b(cr, t, t0, t1):
    paper(cr)
    CHN.draw(cr, t)


def shot20(cr, t, t0, t1):
    paper(cr)
    EU20.draw(cr, t)
    lit = ease_out(seg(t, t0 + 0.45, t0 + 0.9))
    outline(cr, EU20, t, ["germany", "g37east", "east_prussia", "rhineland"], color="gold", lw=6, alpha=lit)
    if t < t0 + 0.4:                                                   # the whip: speed streaks
        u = seg(t, t0, t0 + 0.4)
        cr.set_source_rgba(*col("cream", 0.45 * (1 - u)))
        for k in range(14):
            y = 60 + k * 72
            cr.rectangle(0, y, W, 6)
        cr.fill()
    nametag(cr, "GERMANY", W / 2 - 60, H / 2 + 20, t, t0 + 0.6, size=56, color="cream")


def shot21(cr, t, t0, t1):
    backdrop(cr, t, ray="khaki", ray_a=0.18, cy=H * 0.5)
    cr.save()
    push(cr, t, t0, t1, 1.05, cy=H * 0.6)
    u = seg(t, t0, t1)
    rows = 2 + int(6 * u)                                              # the rows multiply
    for k, xc in enumerate((W * 0.3, W * 0.7)):
        if u > 0.15 * k:
            setpieces.march_column(cr, t, nation="germany", ground=1000, horizon=600, rows=rows, cols=3, scale=0.5,
                                   x_center=xc, seed=2 + k)
    for k, tk in enumerate(TANKS):                                     # tanks stamp in
        tt = t0 + 1.0 + 0.6 * k
        if t > tt:
            s = back_out(seg(t, tt, tt + 0.25))
            cr.save()
            x, y = (330, 1035) if k == 0 else (1590, 1010)
            cr.translate(x, y)
            cr.scale(s, s)
            tk.draw(cr, t, x=0, y=0, speed=0)
            cr.restore()
    for k, f in enumerate(FIGHTERS):                                   # fighters across the sky
        tt = t0 + 1.6 + 0.25 * k
        if t > tt:
            f.draw(cr, t, x=-300 + (t - tt) * 900 + k * 120, y=170 + k * 60)
    cr.restore()


def shot22(cr, t, t0, t1):
    paper(cr)
    RH.draw(cr, t)


def shot23(cr, t, t0, t1):
    backdrop(cr, t, ray="ink", ray_a=0.07, cy=H * 0.55)
    cr.save()
    push(cr, t, t0, t1, 1.05, cy=H * 0.7)
    for f in (SHRUG_B, SHRUG_F):
        f.draw(cr, t, track=[(t0, "stand"), (t0 + 0.35, "shrug"), (t1 - 0.2, "shrug")])
    cr.restore()
    nametag(cr, "BRITAIN", 760, 1050, t, t0 + 0.1)
    nametag(cr, "FRANCE", 1170, 1050, t, t0 + 0.1)


def shot24(cr, t, t0, t1):
    paper(cr)
    AU.draw(cr, t)


def shot25(cr, t, t0, t1):
    paper(cr)
    SU.draw(cr, t)
    k = 0.5 + 0.5 * math.sin((t - t0) * 2 * math.pi * 1.6)             # the edge flashes and pulses
    outline(cr, SU, t, ["sudeten"], color="alert", lw=5 + 4 * k, alpha=ease_out(seg(t, t0 + 0.2, t0 + 0.6)) *
            (0.55 + 0.45 * k))


def shot26a(cr, t, t0, t1):
    cr.save()
    push(cr, t, t0, t1, 1.05, cy=H * 0.55)
    ROOM.draw(cr, t)
    xs = [W / 2 + (i - 2) * 1700 / 5 for i in range(5)]
    who = ["chamberlain", "daladier", None, "hitler", "mussolini"]          # the Czech chair (centre) stays empty
    for x, w_ in zip(xs, who):
        if w_:
            facing_in = 0.3 if x < W / 2 else 0.6
            heads.portrait(cr, t, w_, x, 960, height=470, expr="smug" if w_ in ("hitler", "mussolini") else "worried",
                           turn=facing_in, seed=hash(w_) % 7)
    TABLE.draw(cr, t)
    # the pen signs (on the table near Chamberlain)
    u = seg(t, t0 + 0.6, t1 - 0.3)
    px0, py = W / 2 - 520, 960
    cr.rectangle(px0 - 30, py - 40, 260, 70)
    cr.set_source_rgba(*col("cream"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(3)
    cr.stroke()
    if u > 0:
        cr.new_path()
        n = int(40 * u) + 2
        for k in range(n):
            x = px0 + k * 5
            y = py - 6 + 8 * math.sin(k * 0.9)
            (cr.move_to if k == 0 else cr.line_to)(x, y)
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(3.5)
        cr.stroke()
        tip = (px0 + (n - 1) * 5, py - 6 + 8 * math.sin((n - 1) * 0.9))
        cr.move_to(*tip)
        cr.line_to(tip[0] + 40, tip[1] - 90)
        cr.set_line_width(9)
        cr.set_source_rgba(*col("ink"))
        cr.stroke()
    cr.restore()
    for x, w_ in zip(xs, ["CHAMBERLAIN", "DALADIER", "CZECHOSLOVAKIA", "HITLER", "MUSSOLINI"]):
        nametag(cr, w_, x, 1050, t, t0 + 0.3, size=30, color="gold" if w_[0] == "C" and w_[1] == "Z" else "cream")
    text(cr, "MUNICH, SEPTEMBER 1938", W / 2, 120, 54, font=STENCIL, color="cream", outline="ink", outline_w=8,
         spacing=6, alpha=ease_out(seg(t, t0, t0 + 0.4)))


def shot26b(cr, t, t0, t1):
    paper(cr)
    SU2.draw(cr, t)


def shot27(cr, t, t0, t1):
    SKY.draw(cr, t)
    cr.rectangle(0, 820, W, H - 820)                                    # the airfield
    cr.set_source_rgba(*col("khaki"))
    cr.fill()
    cr.save()
    push(cr, t, t0, t1, 1.08, cx=PLANE.o["x"] - 200, cy=600)
    PLANE.draw(cr, t)
    dx, dy = things.Airliner.door_xy()
    sc = PLANE.o["scale"]
    x, y = PLANE.o["x"] - dx * sc, PLANE.o["y"] + dy * sc                # the door sill (mirrored: facing -1)
    CHAMBERLAIN.draw(cr, t, track=[(t0, "stand"), (t0 + 0.6, "hold_paper"), (t0 + 1.2, "wave"), (t1, "wave")],
                     move=[(t0, x, y)])
    cr.restore()
    setpieces.cheering_crowd(cr, t, 0, W, 900, 1100, n=30, scale=0.42, hats=True)
    a = ease_out(seg(t, at(27, 0.62), at(27, 0.62) + 0.4))             # PEACE FOR OUR TIME on "peace"
    if a > 0:
        cr.rectangle(0, 70, W * a, 130)
        cr.set_source_rgba(*col("ink", 0.9))
        cr.fill()
        text(cr, "“PEACE FOR OUR TIME”", W / 2, 162, 84, font=SLAB, color="cream", alpha=a, spacing=4)


def shot28a(cr, t, t0, t1):
    paper(cr)
    CZ.draw(cr, t)


def shot28b(cr, t, t0, t1):
    backdrop(cr, t, tone="paper_dk", ray="ink", ray_a=0.06, cy=H / 2)
    cr.save()
    push(cr, t, t0, t1, 1.1)
    PAPER.draw(cr, t, crumple=smooth(seg(t, t0 + 0.2, t1 - 0.1)))
    cr.restore()


def shot29(cr, t, t0, t1):
    sx, sy = shake(t, t0 + 0.12, amp=14)
    cr.save()
    cr.translate(sx, sy)
    backdrop(cr, t, ray="ink", ray_a=0.1, cy=H / 2)
    slam(cr, t, t0 + 0.1, "AUGUST", W / 2, H / 2 - 110, size=190, color="ink", font=TITLE, tilt=0.0)
    slam(cr, t, t0 + 0.3, "1939", W / 2, H / 2 + 120, size=230, color="alert", font=TITLE, tilt=0.0)
    cr.restore()


def shot30(cr, t, t0, t1):
    """Helper 1's pact beats, remapped: the handshake through line 30, the stamp on line 31, the SECRET folder slides
    up just before the cut to the map (the pact scene draws its own date tag and print finish)."""
    from channels.ww2.style import leaders_pact as lp
    keys = [(t0, 0.0), (L(30).start + 0.2, 0.6), (L(31).start + 0.1, lp.T_STAMP - 0.15), (t1, lp.T_FOLDER + 0.5)]
    for (ta, la), (tb, lb) in zip(keys, keys[1:]):
        if t <= tb:
            local = lerp(la, lb, seg(t, ta, tb))
            break
    else:
        local = keys[-1][1]
    lp.draw(cr, local)
    return True


def shot32(cr, t, t0, t1):
    paper(cr)
    SEC.draw(cr, t)


def shot33(cr, t, t0, t1):
    DAWN.draw(cr, t)                                                   # 4:45 a.m., 1 September
    OCEAN.draw(cr, t)
    cr.save()
    push(cr, t, t0, t1, 1.06, cx=900, cy=760)
    fire_t = at(33, 0.55)                                              # on "open fire"
    SHIP.draw(cr, t, fire=[fire_t, fire_t + 0.9], turrets=(-12, -12, 192), elev=14)
    cr.restore()
    fx.flash(cr, t, fire_t + 0.02, hold=0.05, fade=0.5)
    text(cr, "DANZIG", W / 2, 150, 70, font=STENCIL, color="cream", outline="ink", outline_w=10, spacing=8,
         alpha=ease_out(seg(t, t0 + 0.2, t0 + 0.6)))


def card(cr, t, t0, t1):
    backdrop(cr, t, ray="gold", ray_a=0.2, cy=H / 2)
    chapter_card(cr, t, t0, 2, "Lightning war", dur=t1 - t0)


def shot34a(cr, t, t0, t1):
    paper(cr)
    PL.draw(cr, t)


def shot34b(cr, t, t0, t1):
    SKY.draw(cr, t, mode="day")
    cr.rectangle(0, 820, W, H - 820)
    cr.set_source_rgba(*col("olive", 0.85))
    cr.fill()
    cr.save()
    push(cr, t, t0, t1, 1.05, cy=800)
    u = seg(t, t0, t1)
    FIELD_TANK.draw(cr, t, x=lerp(-350, 1500, u), y=990, speed=650)
    for k in range(3):
        fx.puff(cr, lerp(-350, 1500, u) - 260 - k * 120, 975, (t - t0) * 1.0 + k * 0.4, size=0.7, seed=k)
    STUKA.draw(cr, t, x=lerp(1700, 500, u), y=lerp(150, 420, u), dive=0.6 + 0.4 * u)
    cr.restore()


def shot35(cr, t, t0, t1):
    backdrop(cr, t, ray="gold", ray_a=0.18, cy=H / 2)
    cr.save()
    push(cr, t, t0, t1, 1.05)
    NEWS.draw(cr, t, spin=ease_out(seg(t, t0, t0 + 0.6)))
    cr.restore()
    slam(cr, t, t0 + 0.55, "BLITZKRIEG", W / 2 - 160, H / 2 - 120, size=170, color="alert", tilt=-0.06)
    s1 = T.sentence("35", 1).start if len(_sentences(35)) > 1 else at(35, 0.6)
    u = ease_out(seg(t, s1, s1 + 0.45))
    if u > 0:                                                           # "Lightning war.": the underline and a bolt
        x0, x1, y = W / 2 - 700, W / 2 + 380, H / 2 + 10
        cr.rectangle(x0, y, (x1 - x0) * u, 22)
        cr.set_source_rgba(*col("ink"))
        cr.fill()
        text(cr, "LIGHTNING WAR", W / 2 - 160, H / 2 + 120, 84, font=STENCIL, color="ink", alpha=u, outline="cream",
             outline_w=12, spacing=10)
        bolt(cr, W / 2 + 470, H / 2 - 300, 1.0, u)


def _sentences(i):
    try:
        k = 0
        while True:
            T.sentence(str(i), k)
            k += 1
    except (IndexError, KeyError):
        return list(range(k))


def bolt(cr, x, y, s, a):
    pts = [(0, 0), (80, 0), (40, 150), (110, 150), (-30, 400), (20, 210), (-50, 210)]
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.new_path()
    for i, p in enumerate(pts):
        (cr.move_to if i == 0 else cr.line_to)(*p)
    cr.close_path()
    cr.set_source_rgba(*col("gold", a))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink", a))
    cr.set_line_width(7)
    cr.stroke()
    cr.restore()


# (start, end, draw, date tag)
SHOTS = [
    (S17[0], S17[1], shot17, "1935"),
    (S18A[0], S18A[1], shot18a, "1935"),
    (S18B[0], S18B[1], shot18b, "1935"),
    (S19A[0], S19A[1], shot19a, "1931"),
    (S19B[0], S19B[1], shot19b, "1937"),
    (S20[0], S20[1], shot20, "1935"),
    (cut(21), cut(22), shot21, "1935"),
    (S22[0], S22[1], shot22, "MARCH 1936"),
    (cut(23), cut(24), shot23, "MARCH 1936"),
    (S24[0], S24[1], shot24, "MARCH 1938"),
    (S25[0], S25[1], shot25, "SEPT 1938"),
    (S26A[0], S26A[1], shot26a, "SEPT 1938"),
    (S26B[0], S26B[1], shot26b, "SEPT 1938"),
    (cut(27), cut(28), shot27, "SEPT 1938"),
    (S28A[0], S28A[1], shot28a, "MARCH 1939"),
    (S28B[0], S28B[1], shot28b, "MARCH 1939"),
    (cut(29), cut(30), shot29, "AUG 1939"),
    (cut(30), cut(32), shot30, "AUG 1939"),
    (S32[0], S32[1], shot32, "AUG 1939"),
    (cut(33), CARD[0], shot33, "1 SEPT 1939"),
    (CARD[0], CARD[1], card, None),
    (S34A[0], S34A[1], shot34a, "SEPT 1939"),
    (S34B[0], S34B[1], shot34b, "SEPT 1939"),
    (cut(35), B + 1.0, shot35, "SEPT 1939"),
]


def draw(cr, t):
    for i, (t0, t1, fn, tag) in enumerate(SHOTS):
        if t < t1 or i == len(SHOTS) - 1:
            break
    cr.save()
    done = fn(cr, t, t0, t1)
    cr.restore()
    if done:                                                           # (the pact scene finishes its own frame)
        return
    if tag:
        prev = SHOTS[i - 1][3] if i > 0 else None
        date_stamp(cr, t, tag, start=t0 if tag != prev else -1e9)
    print_finish(cr, t)


def cues(T=T):
    """[(episode time, sfx, gain dB, pan)] for helper 7's mix."""
    c = [(S17[0] + 0.2, "page_whoosh", -8, 0.0),
         (S18A[0] + 0.1, "stamp", -10, 0.0),
         (S18B[0] + 0.25, "page_whoosh", -10, -0.2),
         (S19A[0] + 1.0, "stamp", -6, 0.3), (S19A[0] + 0.3, "page_whoosh", -12, 0.0),
         (S19B[0] + 1.1, "stamp", -6, 0.3), (S19B[0] + 0.2, "artillery", -16, 0.2),
         (S20[0], "page_whoosh", -6, -0.4),
         (cut(21) + 0.2, "tank", -14, 0.0), (cut(21) + 1.6, "plane_drone", -14, 0.4),
         (at(22, 0.25), "tank", -16, 0.2),
         (S24[0] + 0.3, "page_whoosh", -14, 0.0),
         (S25[0] + 0.2, "clock_tick", -12, 0.0),
         (S26A[0] + 0.6, "typewriter", -18, -0.3),
         (S26B[0] + 0.15, "page_whoosh", -14, 0.0),
         (cut(27) + 0.4, "crowd_cheer", -10, 0.0),
         (S28A[0] + 0.25, "page_whoosh", -14, 0.0), (S28B[0] + 0.2, "page_whoosh", -10, 0.0),
         (cut(29) + 0.12, "door_slam", -2, 0.0),
         (L(31).start + 0.1, "stamp", -4, 0.0),
         (at(32, 0.35) + 1.4, "stamp", -6, 0.2),
         (at(33, 0.55), "gun_boom", 0, -0.2), (at(33, 0.55) + 0.9, "gun_boom", -3, 0.1),
         (CARD[0], "stamp", -6, 0.0),
         (S34A[0], "tank", -8, 0.0), (S34B[0], "dive_whine", -8, 0.4),
         (cut(35) + 0.55, "stamp", -4, 0.0), (cut(35) + 0.1, "typewriter", -14, 0.0)]
    return sorted(c)
