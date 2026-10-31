"""WW2 Episode 1, package P3 (lines 36-53): war declared -> Churchill refuses. Animator: XprL.

Every beat is placed on the shared clock (timing.json via Timing) relative to line and sentence times, so the package
re-times itself when the voiced narration lands. Shots (SHOTLIST.md C2-S05..S23):

    36  TELEGRAMS   LONDON / PARIS telegrams fly in over khaki rays; WAR DECLARED stamp       3 SEPT 1939
    37-38 MAP       Poland: red arrows from the east, the secret line, Poland floods red; DIVIDED   17 SEPT / OCT 1939
    39  TRENCH      a French and a British soldier in a quiet trench; one yawns                 OCT 1939
    40  CLOCK       the clock spins through the winter (the date tag flips), snow; PHONEY WAR   NOV 1939 -> MAR 1940
    41-43 MAP       Denmark and Norway flood grey; 10 May arrows into NL/BE/LUX/FR; the Maginot Line glows
    44a FOREST      the Ardennes in poster layers; a column of tanks threads through             MAY 1940
    44b-45 MAP      the sickle arrow curls round the Maginot Line to the Channel; 10 DAYS       20 MAY 1940
    46  BEACH       the Dunkirk beach (the approved style frame, re-timed)                       MAY 1940
    47  CHANNEL     the little ships cross from the white cliffs, each type as it is named      MAY 1940
    48  CHANNEL     the boats come back loaded; the counter climbs to 338,226                    4 JUNE 1940
    49  MAP         France greys out (the occupied zone floods, Vichy stays pale)               JUNE 1940
    50  CARRIAGE    the railway carriage in the Compiegne clearing                               22 JUNE 1940
    51  CARRIAGE    the same carriage in a sepia 1918 flashback, then a match cut back to 1940   NOV 1918 / JUNE 1940
    52  WORLD MAP   Britain against a grey continent; pull back as Canada, Australia, NZ, South Africa, India light up
    53  CHURCHILL   portrait on blue rays; a firm head shake on "refuses"; NO PEACE stamp       JUNE 1940

    /home/user/.venv-main/bin/python channels/ww2/ep01/render_pkg.py P3 [--sheet | --still T | --frames A-B]
"""
import math
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
from channels.ww2.ep01.timing import Timing, package_span  # noqa: E402
from channels.ww2.kit.core import (H, PAL, SLAB, STENCIL, TITLE, W, back_out, cairo, clamp01, col, date_stamp,  # noqa: E402,F401
                                   ease_in, ease_out, lerp, paper, print_finish, push_in, rays, seg, shake, smooth,
                                   text, word_card)
from channels.ww2.kit import props as P  # noqa: E402
from channels.ww2.kit import fx, sets, things  # noqa: E402
from channels.ww2.kit import heads  # noqa: E402
from channels.ww2.kit.maps import Map  # noqa: E402
from channels.ww2.kit.stick import Figure  # noqa: E402
from channels.ww2.style import dunkirk as DK  # noqa: E402

T = Timing()
A, B = package_span("P3", T)


def L(i):
    return T.line(str(i))


def S(i, k):
    return T.sentence(str(i), k)


def cut(i, j):
    """The cut between line i and line j: the middle of the pause."""
    return (L(i).end + L(j).start) / 2


def at(i, u):
    """A point u (0..1) of the way through line i."""
    return L(i).start + u * L(i).dur


MID44 = at(44, 0.42)                         # "...goes around it, | through the thick Ardennes forest"

# ================================================================ shot helpers
def zoom_about(cr, z, fx_=W / 2, fy=H / 2):
    cr.translate(fx_, fy)
    cr.scale(z, z)
    cr.translate(-fx_, -fy)


def sepia(cr, k=1.0):
    """Turn the frame so far into a faded 1918 print: drain the colour, warm it, and screen it with dots."""
    cr.save()
    cr.identity_matrix()
    cr.set_operator(cairo.OPERATOR_HSL_SATURATION)
    cr.set_source_rgba(0.5, 0.5, 0.5, k)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(0.86, 0.72, 0.5, 0.75 * k)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.rectangle(0, 0, W, H)
    P.dots(cr, "#5a4630", 1, 0.35 * k)
    cr.new_path()
    cr.restore()


# ================================================================ 36  telegrams
TEL_L = P.Telegram(lines=("FROM LONDON", "STATE OF WAR", "WITH GERMANY"), seed=1)
TEL_P = P.Telegram(lines=("FROM PARIS", "STATE OF WAR", "WITH GERMANY"), seed=2)


def shot_telegrams(cr, t, t0, t1):
    tt = t - t0
    paper(cr)
    cr.save()
    zoom_about(cr, push_in(t, t0, t1, 1.0, 1.08))
    rays(cr, t, W / 2, H * 0.55, n=28, color="khaki", alpha=0.3)
    for k, (tel, side, ang) in enumerate(((TEL_L, -1, -0.12), (TEL_P, 1, 0.1))):
        s = A + 0.05 + k * 0.8
        u = ease_out(seg(t, s, s + 0.55))
        if u <= 0:
            continue
        x = lerp(W / 2 + side * 1400, W / 2 + side * 330, u)
        y = lerp(H * 0.2, H * 0.52, u)
        cr.save()
        cr.translate(x, y)
        cr.rotate(ang + (1 - u) * side * 1.6)
        tel.draw(cr, t, x=0, y=0, scale=2.2, flutter=1.0 - 0.7 * u)
        cr.restore()
    if t >= L(36).start + 2.0:
        word_card(cr, t, L(36).start + 2.0, "WAR DECLARED", dur=99, y=H * 0.86, size=118, color="alert")
    cr.restore()
    date_stamp(cr, tt, "3 SEPT 1939", start=-1)


# ================================================================ 37-38  Poland
MAP_POL = Map("europe", era="1939")
MAP_POL.side("poland_w", 0.0, "germany")
MAP_POL.camera_key(cut(36, 37), (21.0, 52.0), 2.3)
MAP_POL.camera_key(cut(38, 39), (22.5, 52.0), 2.75)
MAP_POL.label("GERMANY", cut(36, 37), lonlat=(12.0, 51.4), size=46)
MAP_POL.label("SOVIET UNION", cut(36, 37), lonlat=(31.0, 54.4), size=46)
MAP_POL.label("POLAND", cut(36, 37), lonlat=(19.6, 51.4), size=50, t_out=L(38).start + 1.0)
MAP_POL.city("Warsaw", L(37).start + 0.2)
MAP_POL.arrows("soviet_poland_1939", L(37).start + 0.6, L(37).start + 2.0, stagger=0.3, hold=L(38).end)
MAP_POL.line("secret_1939", L(37).start + 2.2, L(37).end)
MAP_POL.side("poland_e", L(38).start + 0.1, "soviet", origin=(27.0, 51.6), dur=1.6)
MAP_POL.stamp("DIVIDED", (21.6, 52.6), L(38).start + 1.9, size=86)


def shot_poland(cr, t, t0, t1):
    MAP_POL.draw(cr, t)
    if t < L(38).start:
        date_stamp(cr, t - t0, "17 SEPT 1939", start=-1)
    else:
        date_stamp(cr, t - L(38).start, "OCT 1939", start=0)


# ================================================================ 39-40  the Phoney War trench
TRENCH = P.Trench(width=1300, depth=330, extent=1300, seed=3)
SKY_DUSK = sets.Sky(mode="dusk", horizon=520, clouds=4, seed=8)
YAWN = dict(sh_n=2.8, el_n=0.55, sh_f=2.7, el_f=0.6, nod=-0.4, lean=-0.1, turn=0.6,
            face={"mouth": "o", "brow": "sad"})
LEAN = dict(lean=0.25, sh_n=1.2, el_n=1.6, sh_f=1.0, el_f=1.8, nod=0.15, turn=0.3, face={"brow": "sad"})
SOLDIERS = [
    Figure(nation="france", x=700, y=860, scale=0.95, facing=1, prop="rifle", seed=31),
    Figure(nation="britain", x=1180, y=860, scale=0.95, facing=-1, seed=32),
    Figure(nation="france", x=1480, y=860, scale=0.85, facing=-1, seed=33),
]
MONTHS = ["OCT 1939", "NOV 1939", "DEC 1939", "JAN 1940", "FEB 1940", "MAR 1940"]


def trench_world(cr, t, t_scene, snow=0.0, night=0.0):
    SKY_DUSK.draw(cr, t)
    cr.rectangle(-200, 520, W + 400, H)
    P.fill(cr, "#8b7a5c")
    P.BarbedWire(length=1800, seed=2, silhouette="#2b2724").draw(cr, t, x=W / 2, y=560, scale=0.45)
    TRENCH.draw(cr, t, x=W / 2, y=560, scale=1.0)
    y0 = L(39).start
    SOLDIERS[0].draw(cr, t_scene, [(0.0, "idle"), (y0 + 0.7, YAWN), (y0 + 2.6, "idle")])
    SOLDIERS[1].draw(cr, t_scene, [(0.0, LEAN)])
    SOLDIERS[2].draw(cr, t_scene, [(0.0, "sit"), (y0 + 1.6, "head_down")])
    if night > 0:
        cr.rectangle(-200, -200, W + 400, H + 400)
        P.fill(cr, "#1f2430", 0.45 * night)
    if snow > 0:
        P.snowfall(cr, t, density=int(220 * snow), wind=50)


def shot_trench(cr, t, t0, t1):
    cr.save()
    zoom_about(cr, push_in(t, t0, t1, 1.0, 1.06), W / 2, H * 0.62)
    trench_world(cr, t, t)
    cr.restore()
    date_stamp(cr, t - t0, "OCT 1939", start=-1)


CLOCK = things.Clock(seed=4)


def shot_clock(cr, t, t0, t1):
    s0, s1 = L(40).start, S(40, 0).end                           # "For months, the armies just sit and wait."
    u = smooth(seg(t, s0 - 0.2, s1 + 0.2))
    snow = smooth(seg(u, 0.25, 0.45)) * (1 - smooth(seg(u, 0.75, 0.95)))
    cr.save()
    zoom_about(cr, push_in(t, t0, t1, 1.06, 1.12), W / 2, H * 0.62)
    trench_world(cr, t, t, snow=snow, night=0.35 * math.sin(u * math.pi))
    cr.restore()
    cr.save()                                                    # the clock spins through the months
    cr.translate(W * 0.8, H * 0.3)
    k = back_out(seg(t, t0, t0 + 0.35))
    cr.scale(k, k)
    CLOCK.draw(cr, t, x=0, y=0, scale=1.25, hours=4 + u * 12 * 30, tick=False)
    cr.restore()
    m = min(len(MONTHS) - 1, int(u * (len(MONTHS) - 0.001)))
    flip = s0 - 0.2 + (s1 - s0 + 0.4) * m / (len(MONTHS) - 1) if m else t0
    date_stamp(cr, t - flip, MONTHS[m], start=0 if m else -1)
    word_card(cr, t, S(40, 1).start + 0.15, "PHONEY WAR", dur=99, y=H * 0.84, size=150, color="alert")


# ================================================================ 41-43  Scandinavia, the West, the Maginot Line
MAP_W = Map("europe", era="1939")
MAP_W.side("poland_w", 0.0, "germany")
MAP_W.side("poland_e", 0.0, "soviet")
MAP_W.view("scandinavia", cut(40, 41), zoom=1.7)
MAP_W.view("scandinavia", L(41).end, zoom=1.9)
MAP_W.view("west_1940", cut(41, 42) + 0.5, zoom=2.6)
MAP_W.view("west_1940", L(42).end, zoom=3.0)
MAP_W.camera_key(L(43).start + 0.3, (7.0, 49.4), 4.4)
MAP_W.camera_key(cut(43, 44), (6.6, 48.9), 5.2)
MAP_W.label("DENMARK", L(41).start + 0.9, lonlat=(9.3, 56.1), size=34, t_out=L(41).end)
MAP_W.label("NORWAY", L(41).start + 1.3, lonlat=(9.6, 61.6), size=44, t_out=L(41).end)
MAP_W.arrows("denmark_1940", L(41).start + 0.6, L(41).start + 1.6, hold=L(41).end + 0.4)
MAP_W.arrows("norway_1940", L(41).start + 1.0, L(41).start + 2.4, stagger=0.2, hold=L(41).end + 0.4)
MAP_W.campaign("scandinavia_1940", L(41).start + 0.9, L(41).end)
MAP_W.label("NETHERLANDS", L(42).start + 1.2, lonlat=(5.6, 52.5), size=26, t_out=L(43).start + 0.5)
MAP_W.label("BELGIUM", L(42).start + 1.6, lonlat=(4.6, 50.75), size=26, t_out=L(43).start + 0.5)
MAP_W.label("LUXEMBOURG", L(42).start + 2.0, lonlat=(6.1, 49.35), size=20, t_out=L(43).start + 0.5)
MAP_W.label("FRANCE", L(42).start + 2.6, lonlat=(2.6, 47.6), size=50)
MAP_W.label("GERMANY", L(42).start, lonlat=(9.8, 50.6), size=44)
MAP_W.arrows("west_1940", L(42).start + 0.6, L(42).start + 2.0, stagger=0.35, hold=L(43).start + 0.4)
MAP_W.side("low_countries", L(42).start + 2.4, "germany", origin=(6.5, 51.5), dur=1.8)
MAP_W.line("maginot", L(43).start + 0.6, L(43).start + 3.0)
MAP_W.label("MAGINOT LINE", L(43).start + 2.6, lonlat=(8.7, 48.1), size=40, color="alert", tilt=-0.08)


def shot_west(cr, t, t0, t1):
    MAP_W.draw(cr, t)
    if t < L(42).start - 0.3:
        date_stamp(cr, t - t0, "APRIL 1940", start=-1)
    elif t < L(43).start:
        date_stamp(cr, t - (L(42).start - 0.3), "10 MAY 1940", start=0)
    else:
        date_stamp(cr, t - L(43).start, "MAY 1940", start=-1)


# ================================================================ 44a  the Ardennes
TANKS = [P.Tank(side="germany", seed=50 + i) for i in range(5)]


def shot_forest(cr, t, t0, t1):
    tt = t - t0
    cr.save()
    zoom_about(cr, push_in(t, t0, t1, 1.0, 1.07), W / 2, H * 0.6)
    sets.Sky(mode="dusk", horizon=640, clouds=3, seed=5).draw(cr, t)
    things.forest(cr, t, -200, W + 200, 640, n=16, scale=0.9, seed=7, rows=3, tone="#56603a")
    cr.rectangle(-200, 640, W + 400, H)
    P.fill(cr, "#6b6046")
    P.poly(cr, [(-200, 800), (W + 200, 740), (W + 200, 880), (-200, 940)])         # the forest track
    P.fill(cr, "#8b7a5c", keep=True)
    P.dots(cr, "#5e4a33", 1, 0.8)
    cr.new_path()
    for i, tank in enumerate(TANKS):                                            # the column threads through
        x = (tt * 230 + i * 520) % (W + 1100) - 500
        y = 880 - (x + 200) / (W + 400) * 60
        tank.draw(cr, t, x=x, y=y, scale=0.72, speed=230, turret=0)
    for x, sc in ((-60, 2.2), (W + 40, 2.4)):                                    # dark framing trees at the edges
        things.Tree(kind="pine", seed=int(x), silhouette="#1f241a").draw(cr, t, x=x, y=H + 120, scale=sc)
    cr.restore()
    date_stamp(cr, tt, "MAY 1940", start=-1)


# ================================================================ 44b-45  the sickle to the sea
MAP_S = Map("europe", era="1939")
MAP_S.side("poland_w", 0.0, "germany")
MAP_S.side("poland_e", 0.0, "soviet")
for _r in ("denmark", "norway", "netherlands", "belgium", "luxembourg"):
    MAP_S.side(_r, 0.0, "germany")
MAP_S.view("ardennes", MID44, zoom=4.0)
MAP_S.view("west_1940", L(44).end, zoom=3.4)
MAP_S.camera_key(L(45).start + 0.6, (2.6, 50.2), 4.2)
MAP_S.camera_key(cut(45, 46), (2.4, 50.6), 4.6)
MAP_S.line("maginot", MID44 - 0.5, MID44 - 0.1)
MAP_S.label("ARDENNES", MID44 + 0.2, lonlat=(5.3, 50.05), size=34, t_out=L(45).start + 0.5)
MAP_S.label("MAGINOT LINE", MID44, lonlat=(8.7, 48.1), size=34, color="alert", tilt=-0.08, t_out=L(45).start)
MAP_S.arrows("sickle_1940", MID44 + 0.4, L(45).start + 1.2, hold=None)
MAP_S.label("ENGLISH CHANNEL", L(45).start + 0.6, lonlat=(-1.2, 50.2), size=36)
MAP_S.side("france_north", L(45).start + 1.0, "germany", origin=(5.0, 49.8), dur=1.8)
MAP_S.city("Dunkirk", L(45).start + 1.6, lonlat=(2.38, 51.03))


def shot_sickle(cr, t, t0, t1):
    MAP_S.draw(cr, t)
    hit = L(45).start + 1.2
    if t >= hit:
        x, y = MAP_S.screen(MAP_S.xy((1.85, 50.15)))
        fx.starburst(cr, x, y, t - hit, 0.8, seed=3)
    s = L(45).start + 0.4                                        # the 10 DAYS counter
    if t >= s:
        n = int(round(10 * ease_out(seg(t, s, s + 1.6))))
        k = back_out(seg(t, s, s + 0.25))
        cr.save()
        cr.translate(W - 300, H - 230)
        cr.scale(k, k)
        P.poly(cr, [(-200, -120), (200, -126), (196, 70), (-196, 76)])
        P.fill_ink(cr, "cream", 6, tone=False)
        text(cr, f"{n}", -40, 30, 170, font=TITLE, color="alert", bold=False, outline="ink", outline_w=10)
        text(cr, "DAYS", 100, 20, 64, font=STENCIL, color="ink")
        cr.restore()
    if t < L(45).start:
        date_stamp(cr, t - t0, "MAY 1940", start=-1)
    else:
        date_stamp(cr, t - L(45).start, "20 MAY 1940", start=0)


# ================================================================ 46  the beach (the approved style frame)
def shot_beach(cr, t, t0, t1):
    tt = t - t0
    cr.save()
    fx_, fy = DK.FOCUS
    zoom_about(cr, push_in(t, t0, t1, 1.0, 1.08), fx_, fy)
    DK.scene(cr, tt + 0.6)
    cr.restore()
    date_stamp(cr, tt, "MAY 1940", start=-1)


# ================================================================ 47-48  the little ships, out and back
HZ = 520                                     # the Channel horizon (low sky, lots of sea for the boats)
SKY_CH = sets.Sky(mode="day", horizon=HZ, clouds=4, seed=12)
SEA_CH = sets.Ocean(horizon=HZ)
FLEET = [  # (class, kwargs, depth y, scale, which word of sentence 2 brings it in: 0..3)
    (P.Destroyer, dict(), 700, 0.5, 0), (P.Destroyer, dict(), 668, 0.3, 0),
    (P.PaddleFerry, dict(), 760, 0.62, 1), (P.PaddleFerry, dict(), 690, 0.36, 1),
    (P.FishingBoat, dict(), 840, 0.85, 2), (P.FishingBoat, dict(), 720, 0.5, 2), (P.FishingBoat, dict(), 940, 1.0, 2),
    (P.Yacht, dict(), 880, 0.95, 3), (P.Yacht, dict(sail=True), 790, 0.7, 3), (P.Yacht, dict(), 1010, 1.15, 3),
]
FLEET_P = [(cls(side="britain", seed=i), kw, HZ + (y - 640) * 1.25, s, w) for i, (cls, kw, y, s, w) in enumerate(FLEET)]


def cliffs(cr, t):
    """The white cliffs on the left horizon: chalk faces with a green top and a halftone shadow."""
    cr.save()
    cr.translate(0, HZ - 640)
    pts = [(-200, 640), (-200, 520), (80, 505), (180, 520), (300, 512), (420, 540), (520, 600), (560, 640)]
    P.poly(cr, pts)
    P.fill_ink(cr, "#e9e2cc", 4)
    P.poly(cr, [(-200, 520), (80, 505), (180, 520), (300, 512), (420, 540), (430, 552), (300, 528), (180, 536),
                (80, 521), (-200, 536)])
    P.fill(cr, "olive")
    for x in (40, 160, 290, 400):
        P.line(cr, x, 540, x + 20, 636, 3, "#b9b09a")
    cr.restore()


def far_smoke(cr, t):
    for i, x in enumerate((1600, 1700, 1790)):                  # Dunkirk burning on the far horizon
        P.smoke(cr, x, HZ + 6, t + i, height=420, width=34, dark=True, wind=0.8, rate=6, life=5.0, seed=60 + i)


def channel(cr, t, t0, t1, home=False):
    tt = t - t0
    SKY_CH.draw(cr, t)
    far_smoke(cr, t)
    SEA_CH.draw(cr, t)
    cliffs(cr, t)
    if home:
        words = [L(48).start + 0.2] * 4
    else:
        s2 = S(47, 1)                                            # warships early (sentence 1), then each type
        words = [t0 + 0.1] + [s2.start + f * (s2.end - s2.start) for f in (0.2, 0.45, 0.72)]
    for i, (cls_obj, kw, y, s, w) in enumerate(sorted(FLEET_P, key=lambda f: f[2])):
        r = random.Random(i * 7 + 3)
        start = words[w] + r.uniform(0, 0.3)
        u = t - start
        speed = 60 + 50 * s
        target = lerp(380, 1500, ((i * 0.37) % 1.0))
        if home:                                                 # heading home to the left, loaded
            x = target + 300 - u * speed
            crowd = {P.PaddleFerry: 10, P.FishingBoat: 5, P.Yacht: 4}.get(type(cls_obj), 0)
            cls_obj.draw(cr, t, x=x, y=y, scale=s, facing=-1, speed=speed, crowd=crowd, **kw)
        else:                                                    # sweeping in from the left as it is named
            if u < 0:
                continue
            x = lerp(-500, target - 200, ease_out(seg(u, 0, 1.1))) + max(0.0, u) * speed
            cls_obj.draw(cr, t, x=x, y=y, scale=s, facing=1, speed=speed, **kw)
    for i in range(3):                                           # fighters on patrol (outbound only)
        u = seg(t, t0 + 1.0 + i * 0.3, t0 + 4.4 + i * 0.3)
        if 0 < u < 1 and not home:
            P.Fighter(side="britain", seed=i).draw(cr, t, x=lerp(-200, W + 200, u) if not home else
                                                   lerp(W + 200, -200, u), y=200 + i * 50, scale=0.3,
                                                   facing=1 if not home else -1, bank=10)


def shot_out(cr, t, t0, t1):
    cr.save()
    zoom_about(cr, push_in(t, t0, t1, 1.0, 1.06), W * 0.45, H * 0.62)
    channel(cr, t, t0, t1)
    cr.restore()
    date_stamp(cr, t - t0, "MAY 1940", start=-1)


def tally(cr, t, s, e):
    if t < s:
        return
    pop = back_out(seg(t, s, s + 0.3))
    if pop < 0.01:
        return
    v = 338226 * ease_out(seg(t, s, e))
    cr.save()
    cr.translate(W - 330, 190)
    cr.scale(pop, pop)
    cr.rotate(-0.03)
    P.poly(cr, [(-250, 40), (250, 34), (244, 92), (-244, 96)])
    P.fill_ink(cr, "alert", 5, tone=False)
    text(cr, f"{v:,.0f}", 0, 22, 140, font=TITLE, color="cream", bold=False, outline="ink", outline_w=12)
    text(cr, "SOLDIERS RESCUED", 0, 80, 38, font=STENCIL, color="cream", spacing=4)
    cr.restore()


def shot_home(cr, t, t0, t1):
    cr.save()
    zoom_about(cr, push_in(t, t0, t1, 1.0, 1.06), W * 0.4, H * 0.7)
    channel(cr, t, t0, t1, home=True)
    cr.restore()
    tally(cr, t, L(48).start + 0.4, L(48).end - 0.2)
    date_stamp(cr, t - t0, "4 JUNE 1940", start=-1)


# ================================================================ 49  France greys out
MAP_F = Map("europe", era="1939")
MAP_F.side("poland_w", 0.0, "germany")
MAP_F.side("poland_e", 0.0, "soviet")
for _r in ("denmark", "norway", "netherlands", "belgium", "luxembourg", "france_north"):
    MAP_F.side(_r, 0.0, "germany")
MAP_F.camera_key(cut(48, 49), (2.5, 47.6), 2.6)
MAP_F.camera_key(cut(49, 50), (2.5, 47.0), 2.95)
MAP_F.label("FRANCE", cut(48, 49), lonlat=(2.6, 46.6), size=60, t_out=L(49).end - 0.4)
MAP_F.side("france_occ", L(49).start + 0.1, "germany", origin=(2.4, 49.6), dur=1.4)
MAP_F.label("VICHY", L(49).end - 0.4, lonlat=(2.5, 45.6), size=34, color="ink_soft")
MAP_F.city("Paris", L(49).start + 0.3)


def shot_france(cr, t, t0, t1):
    MAP_F.draw(cr, t)
    date_stamp(cr, t - t0, "JUNE 1940", start=-1)


# ================================================================ 50-51  the carriage
CARRIAGE = P.RailwayCarriage(seed=3)
GUARDS = [Figure(nation="germany", x=x, y=900, scale=0.42, facing=f, prop="rifle", seed=70 + i)
          for i, (x, f) in enumerate(((420, 1), (1500, -1)))]


def carriage_world(cr, t, era="1940"):
    sets.Sky(mode="day", horizon=700, clouds=3, seed=21).draw(cr, t)
    things.forest(cr, t, -200, W + 200, 720, n=16, scale=0.9, seed=11, rows=3, tone="#4a5a34")
    cr.rectangle(-200, 700, W + 400, H)
    P.fill(cr, "#9a8a5c")
    for k in (-1, 1):                                            # the rails into the clearing
        P.line(cr, -200, 915 + k * 14, W + 200, 915 + k * 14, 6, "ink_soft")
    for x in range(-200, W + 200, 60):
        P.line(cr, x, 908, x + 10, 940, 8, "#6b4e3a")
    CARRIAGE.draw(cr, t, x=W / 2, y=912, scale=1.45, era=era, lit=era == "1918")
    if era == "1940":
        for g in GUARDS:
            g.draw(cr, t, [(0.0, "stand")])


def shot_clearing(cr, t, t0, t1):
    cr.save()
    zoom_about(cr, push_in(t, t0, t1, 1.0, 1.07), W / 2, H * 0.62)
    carriage_world(cr, t)
    cr.restore()
    date_stamp(cr, t - t0, "22 JUNE 1940", start=-1)


FLASH_IN, FLASH_OUT = at(51, 0.5), at(51, 0.92)                  # "...the very same railway carriage" / "1918."


def shot_flashback(cr, t, t0, t1):
    old = FLASH_IN <= t < FLASH_OUT
    cr.save()
    if old:
        zoom_about(cr, push_in(t, FLASH_IN, FLASH_OUT, 1.12, 1.18), W / 2, H * 0.6)
    else:
        zoom_about(cr, push_in(t, t0, t1, 1.07, 1.14), W / 2, H * 0.6)
    carriage_world(cr, t, era="1918" if old else "1940")
    cr.restore()
    if old:
        sepia(cr)
        text(cr, "1918", W / 2, H * 0.24, 170, font=SLAB, color="paper", bold=False, outline="ink", outline_w=12,
             alpha=smooth(seg(t, FLASH_IN, FLASH_IN + 0.4)))
        date_stamp(cr, t - FLASH_IN, "11 NOV 1918", start=0)
    else:
        date_stamp(cr, t - t0, "22 JUNE 1940", start=-1)
    fx.flash(cr, t, FLASH_IN, hold=0.04, fade=0.35, color="cream")
    fx.flash(cr, t, FLASH_OUT, hold=0.04, fade=0.35, color="cream")


# ================================================================ 52  Britain alone
MAP_UK = Map("world", grid=True)
_GREY = ["deu", "fra", "pol", "nld", "bel", "lux", "dnk", "nor", "cze", "svk", "aut"]
for _c in _GREY:
    MAP_UK.side(_c, 0.0, "germany")
MAP_UK.side("ita", 0.0, "italy")
MAP_UK.side("world:ussr", 0.0, "soviet")
MAP_UK.side("gbr", 0.0, "allies", occupied=False)
MAP_UK.camera_key(cut(51, 52), (2.0, 51.0), 6.5)
MAP_UK.camera_key(L(52).start + 1.2, (2.0, 50.0), 5.6)
MAP_UK.camera_key(cut(52, 53), (45.0, 2.0), 1.0)               # wide enough for Australia, NZ and South Africa
DOMINIONS = ["can", "aus", "nzl", "zaf", "ind", "pak", "bgd"]   # the Dominions and British India (1940 borders)
for _k, _c in enumerate(DOMINIONS):
    MAP_UK.side(_c, L(52).start + 0.5 + 0.2 * min(_k, 4), "allies", occupied=False)
MAP_UK.label("BRITAIN", cut(51, 52), lonlat=(-6.0, 55.5), size=44, t_out=L(52).start + 1.6)


def shot_alone(cr, t, t0, t1):
    MAP_UK.draw(cr, t)
    s = L(52).start + 2.2
    if t >= s:
        word_card(cr, t, s, "ALMOST ALONE", dur=99, y=H * 0.13, size=110, color="allies")
    date_stamp(cr, t - t0, "JUNE 1940", start=-1)


# ================================================================ 53  Churchill
REFUSE = at(53, 0.62)                                            # "...refuses to make peace"


def shot_churchill(cr, t, t0, t1):
    paper(cr)
    cr.save()
    zoom_about(cr, push_in(t, t0, t1 + 0.6, 1.0, 1.1), W / 2, H * 0.52)
    rays(cr, t, W / 2, H * 0.36, n=28, color="allies", alpha=0.16)
    sh = 0.0
    if REFUSE <= t <= REFUSE + 1.7:                              # a firm shake: three swings, settling
        u = (t - REFUSE) / 1.7
        sh = 0.32 * math.sin(u * 3 * 2 * math.pi) * (1 - u) ** 0.8
    heads.portrait(cr, t, "churchill", W / 2, H + 40, height=980, expr="determined", turn=0.42, shake=sh, seed=5)
    cr.restore()
    s = REFUSE + 0.9
    if t >= s:
        word_card(cr, t, s, "NO PEACE", dur=99, y=H * 0.84, size=150, color="alert", tilt=-0.06)
    text(cr, "WINSTON CHURCHILL", W - 70, 92, 36, font=STENCIL, color="ink", align="right",
         alpha=smooth(seg(t, t0, t0 + 0.4)) * (1 - smooth(seg(t, s - 0.3, s))))
    date_stamp(cr, t - t0, "JUNE 1940", start=-1)


# ================================================================ the cut list
SHOTS = [
    (A, cut(36, 37), shot_telegrams),
    (cut(36, 37), cut(38, 39), shot_poland),
    (cut(38, 39), cut(39, 40), shot_trench),
    (cut(39, 40), cut(40, 41), shot_clock),
    (cut(40, 41), cut(43, 44), shot_west),
    (cut(43, 44), MID44, shot_forest),
    (MID44, cut(45, 46), shot_sickle),
    (cut(45, 46), cut(46, 47), shot_beach),
    (cut(46, 47), cut(47, 48), shot_out),
    (cut(47, 48), cut(48, 49), shot_home),
    (cut(48, 49), cut(49, 50), shot_france),
    (cut(49, 50), cut(50, 51), shot_clearing),
    (cut(50, 51), cut(51, 52), shot_flashback),
    (cut(51, 52), cut(52, 53), shot_alone),
    (cut(52, 53), B + 1.0, shot_churchill),
]


def draw(cr, t):
    for t0, t1, fn in SHOTS:
        if t < t1 or fn is SHOTS[-1][2]:
            cr.save()
            fn(cr, t, t0, t1)
            cr.restore()
            break
    print_finish(cr, t)


def cues(T=T):
    """[(episode_time, sfx_name, gain_db, pan)] for the mix (names from channels/ww2/sound.py SFX)."""
    c = [
        (L(36).start + 0.15, "page_whoosh", -8, -0.4), (L(36).start + 0.9, "page_whoosh", -8, 0.4),
        (L(36).start + 0.3, "morse", -14, 0.0), (L(36).start + 2.0, "stamp", -6, 0.0),
        (L(37).start + 0.6, "tank", -12, 0.5), (L(38).start + 1.9, "stamp", -6, 0.1),
        (cut(38, 39), "clock_tick", -20, 0.0),
        (L(39).start + 0.7, "radio_static", -26, -0.3),
        (L(40).start - 0.2, "clock_tick", -10, 0.3), (S(40, 1).start + 0.15, "stamp", -5, 0.0),
        (L(41).start + 0.6, "tank", -14, 0.0), (L(42).start + 0.6, "tank", -10, 0.0),
        (L(43).start + 0.6, "artillery", -18, 0.0),
        (cut(43, 44), "tank", -8, -0.3),
        (MID44 + 0.4, "tank", -10, 0.2), (L(45).start + 1.2, "explosion", -10, -0.2),
        (cut(45, 46), "sea_waves", -12, 0.0), (cut(45, 46) + 0.6, "plane_drone", -14, -0.6),
        (cut(45, 46) + 1.0, "artillery", -20, -0.5),
        (cut(46, 47), "sea_waves", -12, 0.0), (cut(46, 47) + 1.0, "plane_drone", -16, -0.5),
        (cut(47, 48), "sea_waves", -12, 0.0), (L(48).start + 0.4, "clock_tick", -14, 0.4),
        (L(49).start + 0.1, "page_whoosh", -12, 0.0),
        (cut(49, 50), "train", -20, 0.0), (FLASH_IN, "page_whoosh", -8, 0.0), (FLASH_OUT, "page_whoosh", -8, 0.0),
        (L(52).start + 1.4, "page_whoosh", -12, 0.0), (L(52).start + 2.2, "stamp", -8, 0.0),
        (REFUSE + 0.9, "stamp", -4, 0.0),
    ]
    return sorted(c)


if __name__ == "__main__":
    print("P3", A, B, "estimated" if T.estimated else "voiced")
    for t0, t1, fn in SHOTS:
        print(f"{t0:8.2f} {t1:8.2f} {t1 - t0:5.2f}  {fn.__name__}")
