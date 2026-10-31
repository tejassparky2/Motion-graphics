"""WW2 Episode 1, package P4 (script lines 54-69, helper 1): the Battle of Britain, Chapter 3 "The war goes global",
Barbarossa, the stall before Moscow, the counter-attack and Pearl Harbor.

Every beat is placed on the episode clock (timing.json via Timing): shots cut halfway through the pause between two
lines, or at a fraction of a line where one line carries two shots. Nothing is hard-coded in seconds except small
offsets inside a shot.

Shots (SHOTLIST.md C2-S24 .. C3-S15):
    54  SKY      German bombers cross the Channel over the white cliffs, low heroic angle     AUG 1940
    55  RAYS     THE BATTLE OF BRITAIN title poster, blue rays, fighters climbing             AUG 1940
    56a COAST    radar masts on the cliffs, rings pulse, blips on the scope                   AUG 1940
    56b SKY      RAF fighters climb into the bomber stream (muzzle flashes only)               AUG 1940
    57a MAP eu   the invasion arrow fades, CALLED OFF stamp                                    SEPT 1940
    57b CITY     London at night: searchlights, flak bursts, fires on the skyline              SEPT 1940
    C3  CARD     poster wipe into CHAPTER 3: THE WAR GOES GLOBAL
    58  MAP eu   a die rolls across Europe: THE BIGGEST GAMBLE                                 JUNE 1941
    59  LEADER   Hitler and Stalin shake hands; the pact tears; the grey floor floods east      22 JUNE 1941
    60  MAP eu   the front from the Baltic to the Black Sea, three grey arrows, 3,000,000+      JUNE 1941
    61  RAYS     OPERATION BARBAROSSA stencil stamp, tanks rolling past                         JUNE 1941
    62  MAP eu   the arrows race east                                                           JULY 1941
    63a STEPPE   columns of Soviet prisoners into the haze, MILLIONS                            SEPT 1941
    63b MAP eu   the arrow tips stop at Moscow                                                  DEC 1941
    64  STEPPE   tanks and trucks stuck in autumn mud; then the snow starts                     OCT -> NOV 1941
    65  STEPPE   German soldiers shivering in thin coats; thermometer falls to -30              DEC 1941
    66  MAP eu   red arrows push the front back from Moscow, COUNTER-ATTACK                     5 DEC 1941
    67a MAP      whip pan across the world, cut to the Pacific: the arrow to Pearl Harbor       7 DEC 1941
    67b OCEAN    battleship row, dive bombers diving in                                         7 DEC 1941
    68  OCEAN    the ships list and smoke (flat puffs, no figures)                              7 DEC 1941
    69  COUNTER  2,403 on smoke-dark paper                                                      7 DEC 1941
No Nazi or Imperial Japanese symbols (German and Japanese aircraft are plain side colour), no red rays, no visible
deaths: losses are numbers.
"""
import math
import random

from channels.ww2.kit.core import *  # noqa: F401,F403
from channels.ww2.kit.core import (H, LABEL, SLAB, STENCIL, TITLE, W, back_out, camera, col, date_stamp,  # noqa
                                   ease_in, ease_out, halftone, lerp, paper, print_finish, rays, seg, shake, smooth,
                                   text, chapter_card)
from channels.ww2.kit import props as P
from channels.ww2.kit import fx, sets, things, stick
from channels.ww2.kit import setpieces as SP
from channels.ww2.kit.maps import Map
from channels.ww2.kit.stick import Figure
from channels.ww2.ep01.timing import Timing, package_span

T = Timing()
A0, B0 = package_span("P4", T)
L = T.line


def cut(i):
    """Halfway through the pause before line i (where a hard cut lands)."""
    prev = T.order[T.order.index(str(i)) - 1]
    return (L(prev).end + L(i).start) / 2


def at(i, f):
    """A fraction f of the way through line i."""
    ln = L(i)
    return ln.start + f * ln.dur


CARD = T.chapter("C3").card                       # (start, end)


def lt(t, a):
    return t - a


def push(cr, t, a, b, focus=(W / 2, H / 2), z0=1.0, z1=1.06):
    """The slow push-in on every shot: scale about the focus point."""
    z = lerp(z0, z1, smooth(seg(t, a, b)))
    cr.translate(*focus)
    cr.scale(z, z)
    cr.translate(-focus[0], -focus[1])


def stencil_tag(cr, s, x, y, size=34, color="ink", alpha=1.0, align="left"):
    text(cr, s, x, y, size, font=STENCIL, color=color, alpha=alpha, align=align, spacing=size * 0.12,
         outline="paper", outline_w=size * 0.12)


def stamp_box(cr, t, start, word, x, y, size=120, color="alert", tilt=-0.06, font=STENCIL, out=None):
    """A rubber stamp that slams down (overshoot), with a double frame, held in a group so it prints as one ink."""
    if t < start or (out is not None and t > out + 0.3):
        return
    u = back_out(seg(t, start, start + 0.22))
    a = 1.0 if out is None else 1 - ease_in(seg(t, out, out + 0.3))
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    s = 1.5 - 0.5 * u
    cr.scale(s, s)
    cr.push_group()
    cr.select_font_face(font)
    cr.set_font_size(size)
    w = cr.text_extents(word).x_advance + size * 0.12 * (len(word) - 1)
    pad = size * 0.32
    for k, lw in ((0, size * 0.07), (size * 0.12, size * 0.03)):
        cr.rectangle(-w / 2 - pad + k, -size * 0.62 - pad * 0.6 + k, w + 2 * pad - 2 * k, size * 1.24 + pad * 1.2 - 2 * k)
        cr.set_line_width(lw)
        cr.set_source_rgba(*col(color))
        cr.stroke()
    text(cr, word, 0, size * 0.36, size, font=font, color=color, bold=False, spacing=size * 0.12)
    cr.pop_group_to_source()
    cr.paint_with_alpha(min(1.0, u * 1.5) * a * 0.92)
    cr.restore()


# ================================================================ shared scenery
CHALK, CHALK_DK = "#efe6cf", "#cfc2a2"


def cliffs(cr, t, top, x0=-100, x1=1300, seed=3, drop=260):
    """The white cliffs: a grassy cap on a cream chalk face with vertical ink cracks, falling to the sea."""
    r = random.Random(seed)
    pts = [(x0, top + r.uniform(-6, 6))]
    n = 14
    for i in range(1, n + 1):
        x = lerp(x0, x1, i / n)
        pts.append((x, top + 18 * math.sin(i * 0.9 + seed) + r.uniform(-5, 5) + (i / n) ** 3 * 60))
    base = top + drop
    face = pts + [(x1 + 40, base), (x0, base)]
    P.poly(cr, face)
    P.fill_ink(cr, CHALK, 5, tone=False)
    for i in range(18):                                            # cracks and the shadow side
        x = lerp(x0 + 30, x1 - 30, r.random())
        P.line(cr, x, top + 30, x + r.uniform(-14, 14), base - r.uniform(10, 80), 2.5, CHALK_DK)
    halftone(cr, lambda c: P.poly(c, [(x1 - 120, top + 40), (x1 + 40, base), (x1 - 260, base)]), "ink", 2, 0.25)
    cap = pts + [(p[0], p[1] + 26) for p in reversed(pts)]
    P.poly(cr, cap)
    P.fill_ink(cr, "#7d8a5a", 4, tone=False)


# ================================================================ 54: bombers over the Channel
def sh_bombers(cr, t, a, b):
    u = lt(t, a)
    cr.save()
    push(cr, t, a, b, (W * 0.55, H * 0.35))
    sets.Sky(mode="day", horizon=930, clouds=5, seed=6, drift=18).draw(cr, t)
    sets.Ocean(horizon=930).draw(cr, t)
    cliffs(cr, t, 905, x0=-100, x1=760, seed=4, drop=240)
    far = "#8c8573"
    for i in range(9):                                             # far stream, hazy silhouettes
        x = (2100 + i * 230 - 70 * u) - (i % 3) * 60
        y = 300 + (i % 3) * 46 + 18 * math.sin(i * 1.7)
        P.Bomber(x=x, y=y, scale=0.22, facing=-1, side="germany", seed=i, silhouette=far).draw(cr, t)
    for i in range(5):                                             # mid stream
        x = 2000 + i * 420 - 190 * u
        y = 480 + (i % 2) * 90
        P.Bomber(x=x, y=y, scale=0.5, facing=-1, side="germany", seed=10 + i, silhouette="#4e4b4f").draw(cr, t)
    for i, (t0, y, s) in enumerate(((0.0, 660, 1.25), (2.2, 290, 1.7), (4.0, 720, 1.1))):   # near, low and big
        x = 2500 - 520 * (u - t0) - i * 60
        P.Bomber(x=x, y=y, scale=s, facing=-1, side="germany", seed=20 + i, engines=2, pitch=2).draw(cr, t)
    cr.restore()
    if u > 2.8:
        stencil_tag(cr, "TARGET: THE R.A.F.", W - 80, H - 90, 44, align="right",
                    alpha=ease_out(seg(t, a + 2.8, a + 3.2)))


# ================================================================ 55: title poster
def sh_title(cr, t, a, b):
    u = lt(t, a)
    cr.save()
    push(cr, t, a, b, (W / 2, H * 0.45), 1.0, 1.08)
    paper(cr)
    rays(cr, t, W / 2, H + 120, n=26, color="allies", alpha=0.32, spin=0.03)
    halftone(cr, lambda c: c.rectangle(0, H * 0.72, W, H * 0.28), "allies", 2, 0.3)
    for i, (x0, y0, s) in enumerate(((260, 1000, 0.75), (620, 1120, 0.95), (-80, 1180, 1.1))):
        k = u + i * 0.25
        x, y = x0 + 420 * k, y0 - 300 * k
        P.Fighter(x=x, y=y, scale=s, facing=1, side="britain", pitch=32, seed=i, silhouette="ink").draw(cr, t)
    cr.restore()
    s1 = back_out(seg(t, a + 0.1, a + 0.4))
    if s1 > 0:
        cr.save()
        cr.translate(W / 2, H * 0.36)
        cr.rotate(-0.035)
        k = 1.5 - 0.5 * s1
        cr.scale(k, k)
        text(cr, "THE BATTLE OF", 0, -70, 64, font=STENCIL, color="ink", spacing=10, alpha=min(1, s1 * 2))
        text(cr, "BRITAIN", 0, 110, 200, font=SLAB, color="allies", bold=False, outline="ink", outline_w=12,
             spacing=6, alpha=min(1, s1 * 2))
        cr.restore()
    if u > 1.0:
        text(cr, "JULY - OCTOBER 1940", W / 2, H * 0.36 + 200, 40, font=LABEL, color="ink_soft",
             alpha=ease_out(seg(t, a + 1.0, a + 1.4)), spacing=6)


# ================================================================ 56a: radar
SCOPE = (1580, 790, 170)
BLIPS = [(1480, 690), (1530, 650), (1600, 700), (1660, 640), (1700, 690), (1560, 600)]


def sh_radar(cr, t, a, b):
    u = lt(t, a)
    cr.save()
    push(cr, t, a, b, (700, 500), 1.0, 1.07)
    sets.Sky(mode="day", horizon=760, clouds=4, seed=11).draw(cr, t)
    sets.Ocean(horizon=760).draw(cr, t)
    cliffs(cr, t, 850, x0=-100, x1=1250, seed=7, drop=300)
    for i, (x, s) in enumerate(((240, 0.58), (620, 0.8), (1040, 0.68))):
        P.RadarTower(x=x, y=870, scale=s, side="britain", period=1.1, reach=900, ring="allies",
                     seed=i).draw(cr, t + i * 0.35)
    # blips over the sea: the bomber stream, far off
    fx.blips(cr, [(1250 + i * 70, 380 + 22 * math.sin(i)) for i in range(7)], t, start=a + 0.5, step=0.18,
             color="alert", size=9)
    cr.restore()
    # the scope (screen space): dark disc, sweep, rings, blips lighting up as the sweep passes
    cx, cy, r = SCOPE
    pop = back_out(seg(t, a + 0.3, a + 0.6))
    if pop <= 0.01:
        return
    cr.save()
    cr.translate(cx, cy)
    cr.scale(pop, pop)
    cr.translate(-cx, -cy)
    cr.arc(cx, cy, r + 18, 0, math.tau)
    P.fill_ink(cr, "#6b665e", 6, tone=False)
    cr.arc(cx, cy, r, 0, math.tau)
    P.fill(cr, "#26352f")
    for k in (0.33, 0.66):
        cr.arc(cx, cy, r * k, 0, math.tau)
        P.ink(cr, 2, "#5f8f74", 0.7)
    ang = (t - a) * 3.4
    cr.move_to(cx, cy)
    cr.arc(cx, cy, r, ang - 0.7, ang)
    cr.close_path()
    P.fill(cr, "#7fc79a", 0.25)
    P.line(cr, cx, cy, cx + r * math.cos(ang), cy + r * math.sin(ang), 3, "#a8f0c0")
    for i, (bx, by) in enumerate(BLIPS):
        if t < a + 0.7 + i * 0.22:
            continue
        cr.arc(bx, by, 7, 0, math.tau)
        P.fill(cr, "#c8ffd6")
    cr.restore()
    stencil_tag(cr, "RADAR", cx, cy + r + 66, 40, align="center", alpha=pop)


# ================================================================ 56b: fighters scramble
def sh_scramble(cr, t, a, b):
    u = lt(t, a)
    cr.save()
    cr.translate(-60 * smooth(seg(t, a, b)), 0)                  # track with the climb
    push(cr, t, a, b, (W * 0.6, H * 0.4))
    sets.Sky(mode="day", horizon=1030, clouds=6, seed=14, drift=30).draw(cr, t)
    for i in range(6):
        x = 2300 + i * 260 - 230 * u
        y = 230 + (i % 3) * 80
        P.Bomber(x=x, y=y, scale=0.42, facing=-1, side="germany", seed=30 + i,
                 trail=(i == 2 and u > 1.6)).draw(cr, t)
    for i, (x0, y0, s, d) in enumerate(((150, 1150, 0.62, 0.0), (520, 1260, 0.8, 0.35), (-100, 1300, 0.7, 0.6))):
        k = max(0.0, u - d)
        x, y = x0 + 520 * k, y0 - 420 * k
        P.Fighter(x=x, y=y, scale=s, facing=1, side="britain", pitch=36, seed=40 + i).draw(cr, t)
        for fire in (1.3, 1.55, 1.8):                            # guns: muzzle flashes only
            age = t - (a + fire + d * 0.3)
            if 0 <= age < 0.2:
                ang = -math.radians(36)
                P.muzzle_flash(cr, x + 120 * s * math.cos(ang), y + 120 * s * math.sin(ang) - 10 * s, age,
                               size=50 * s, angle=ang, smoke_puff=False, seed=i)
    cr.restore()


# ================================================================ 57a: Sea Lion called off
M_SEA = Map("europe", era="1940")
_a, _b = cut(57), at(57, 0.48)
M_SEA.camera_key(_a, (1.2, 51.2), 3.1)
M_SEA.camera_key(_b, (1.1, 51.0), 3.5)
M_SEA.arrows("sealion_1940", _a - 2.0, _a - 1.0, hold=_a + 1.0, width=90)
M_SEA.arrows("blitz_1940", _a - 2.0, _a - 1.0, hold=_a + 1.0, width=60)
M_SEA.label("BRITAIN", _a - 1.0, lonlat=(-1.6, 52.4), size=48)
M_SEA.label("FRANCE", _a - 1.0, lonlat=(2.3, 49.6), size=44)
M_SEA.label("OPERATION SEA LION", _a - 1.0, lonlat=(1.4, 50.35), size=28, t_out=_a + 1.0)
M_SEA.city("London", _a - 1.0)
M_SEA.stamp("CALLED OFF", (1.1, 50.95), _a + 1.05, size=84)


def sh_sealion(cr, t, a, b):
    paper(cr)
    M_SEA.draw(cr, t)


# ================================================================ 57b: the Blitz at night
BURSTS = [(0.5, 420, 260), (1.2, 1240, 180), (1.9, 760, 330), (2.5, 1500, 290), (3.1, 980, 150), (3.7, 300, 200)]
HITS = [(0.8, 560, 770), (1.7, 1340, 760), (2.8, 980, 790), (3.6, 1660, 780)]


def sh_blitz(cr, t, a, b):
    u = lt(t, a)
    cr.save()
    push(cr, t, a, b, (W * 0.5, H * 0.62), 1.0, 1.07)
    sets.Sky(mode="night", horizon=830, clouds=3, seed=21, drift=8).draw(cr, t)
    for i, (x, aim, sw) in enumerate(((330, 62, 14), (900, 104, 10), (1520, 70, 16), (1220, 118, 12))):
        P.Searchlight(x=x, y=860, scale=0.7, side="britain", aim=aim, sweep=sw, sweep_speed=0.18 + 0.05 * i,
                      seed=i, length=1500, beam_alpha=0.32).draw(cr, t)
    for i in range(5):                                             # bombers high in the beams
        x = 2100 + i * 380 - 160 * u
        P.Bomber(x=x, y=150 + (i % 2) * 90, scale=0.26, facing=-1, side="germany", seed=50 + i,
                 silhouette="#14161d").draw(cr, t)
    for i, (s, x, y) in enumerate(BURSTS):                         # flak: small flat bursts in the sky
        fx.starburst(cr, x, y, t - (a + s), size=0.32, seed=i, life=0.5, lines=False,
                     colors=("gold", "cream", "fire", "gold"))
    for i, (s, x, y) in enumerate(HITS):                           # smoke and fires behind the skyline
        if t > a + s:
            P.smoke(cr, x, y - 30, t, height=520, width=110, color="#3a3836", alpha=0.9, wind=0.5, seed=i, dark=True)
    sets.Skyline(city="london", ground=830, night=True, lit=0.35, seed=11).draw(cr, t)
    for i, (s, x, y) in enumerate(HITS):
        P.explosion(cr, x, y - 20, t - (a + s), size=0.7, seed=i)
        if t > a + s + 0.3:
            P.fire(cr, x, y - 6, t, size=34, seed=i)
    cr.restore()


# ================================================================ chapter 3 card (with a poster wipe)
def sh_card(cr, t, a, b):
    paper(cr)
    rays(cr, t, W / 2, H / 2, n=28, color="khaki", alpha=0.35, spin=0.02)
    halftone(cr, lambda c: c.rectangle(0, 0, W, H), "ink", 1, 0.08)
    chapter_card(cr, t, a, 3, T.chapter("C3").title, dur=b - a)
    w = seg(t, a - 0.0, a + 0.35)                                  # the wipe: an ink bar sweeping across
    if 0 < w < 1:
        x = lerp(-300, W + 300, ease_in(w))
        cr.save()
        cr.rectangle(x, 0, W + 600, H)
        cr.clip()
        sh_blitz(cr, t, cut_blitz_a(), a)
        cr.restore()
        P.poly(cr, [(x - 60, 0), (x + 40, 0), (x - 20, H), (x - 120, H)])
        P.fill(cr, "ink")


def cut_blitz_a():
    return at(57, 0.48)


# ================================================================ 58: the gamble (a die across Europe)
M_DIE = Map("europe", era="1941")
_a = CARD[1]
M_DIE.camera_key(_a, (22.0, 52.0), 1.25)
M_DIE.camera_key(cut(59), (24.0, 52.5), 1.38)
M_DIE.label("GERMANY", _a - 1, lonlat=(10.6, 51.2), size=44)
M_DIE.label("SOVIET UNION", _a - 1, lonlat=(36.0, 55.6), size=50)


def sh_gamble(cr, t, a, b):
    paper(cr)
    M_DIE.draw(cr, t)
    roll = seg(t, a + 0.15, a + 1.55)
    landed = a + 1.55
    cr.save()
    dx, dy = shake(t, landed, 0.3, 10)
    cr.translate(dx, dy)
    things.Die(x=W * 0.5 + 200 * ease_out(roll), y=H * 0.56, scale=1.5, roll=roll, value=6).draw(cr, t)
    cr.restore()
    if t > landed:
        s = back_out(seg(t, landed, landed + 0.25))
        cr.save()
        cr.translate(W / 2, 190)
        cr.rotate(-0.03)
        cr.scale(1.4 - 0.4 * s, 1.4 - 0.4 * s)
        text(cr, "THE BIGGEST GAMBLE", 0, 40, 110, font=SLAB, color="ink", bold=False, outline="paper",
             outline_w=12, spacing=3, alpha=min(1, s * 2))
        cr.restore()


# ================================================================ 59: the pact tears
S_P = 1.32
G_P = 975
SHAKE_POSE = lambda t: dict(stick._shake(t), sh_f=-0.45, el_f=0.22, hand_f="crossed",   # noqa: E731
                            face={"name": "smiling"})
POINT_POSE = dict(sh_n=1.55, el_n=0.05, sh_f=-0.3, el_f=0.4, turn=0.3, hand_n="fist", lean=0.08,
                  face={"name": "angry"})
BACK_POSE = dict(sh_n=0.75, el_n=1.6, sh_f=0.6, el_f=1.7, lean=-0.1, nod=-0.1, turn=0.6, hand_n="splay",
                 hand_f="splay", face={"name": "shocked"})


def _hand_dx():
    f = Figure(leader="hitler", x=0, y=G_P, scale=S_P, facing=1)
    return f.joints(0.5, [(0, SHAKE_POSE)])["hand_n"][0]


_DX = _hand_dx()
HITLER = Figure(leader="hitler", x=W / 2 - _DX + 4, y=G_P, scale=S_P, facing=1, seed=3)
STALIN = Figure(leader="stalin", x=W / 2 + _DX - 4, y=G_P, scale=S_P, facing=-1, seed=8)


def sh_pact(cr, t, a, b):
    u = lt(t, a)
    tear = at(59, 0.40) - a                                        # "...he breaks his deal with Stalin"
    flood = at(59, 0.72) - a                                       # "...and invades the Soviet Union"
    dx, dy = shake(t, a + tear, 0.4, 16)
    cr.save()
    cr.translate(dx, dy)
    push(cr, t, a, b, (W / 2, H * 0.5), 1.0, 1.06)
    paper(cr)
    rays(cr, t, W / 2, 640, n=28, color="khaki", alpha=0.4, spin=0.025)
    halftone(cr, lambda c: c.rectangle(0, 0, W, H), "ink", 1, 0.08)
    xf = W / 2 + (W / 2 + 200) * smooth(seg(u, flood, flood + 1.6))     # the grey floor floods east
    for side, x0, x1 in (("axis", -200, xf), ("soviet", xf, W + 200)):
        cr.rectangle(x0, G_P + 4, x1 - x0, H)
        cr.set_source_rgba(*col(side, 0.92))
        cr.fill()
    halftone(cr, lambda c: c.rectangle(-200, G_P + 4, W + 400, H), "ink", 2, 0.35)
    P.line(cr, -200, G_P + 4, W + 200, G_P + 4, 5)
    if u > flood:                                                   # a fat grey arrow drives along the floor
        g = smooth(seg(u, flood, flood + 1.3))
        x0, x1 = W * 0.3, W * 0.3 + (W * 0.66) * g
        y = G_P + 55
        P.poly(cr, [(x0, y - 22), (x1 - 40, y - 22), (x1 - 40, y - 46), (x1 + 30, y), (x1 - 40, y + 46),
                    (x1 - 40, y + 22), (x0, y + 22)])
        P.fill_ink(cr, "axis", 5, tone=False)
    h_tr = [(0, SHAKE_POSE), (tear + 0.02, POINT_POSE)]
    s_tr = [(0, SHAKE_POSE), (tear + 0.02, BACK_POSE)]
    STALIN.draw(cr, u, s_tr, move=[(tear, STALIN.x), (tear + 0.5, STALIN.x + 150)])
    HITLER.draw(cr, u, h_tr)
    tr = ease_out(seg(u, tear, tear + 0.55))
    things.Pact(x=W / 2, y=330, scale=0.62, tear=tr, title="PACT", seed=2).draw(cr, t)
    cr.restore()


# ================================================================ 60/62/63b/66: the eastern front map
M_E = Map("europe", era="1941")
a60, a62, a63b, a66 = cut(60), cut(62), at(63, 0.5), cut(66)
b60, b62, b63b, b66 = cut(61), cut(63), cut(64), cut(67)
M_E.camera_key(a60, (24.5, 53.0), 2.1)
M_E.camera_key(b60, (30.0, 52.3), 1.35)
M_E.camera_key(a62, (30.0, 52.3), 1.35)
M_E.camera_key(b62, (32.5, 53.5), 1.5)
M_E.camera_key(a63b, (34.0, 54.8), 1.85)
M_E.camera_key(b63b, (35.5, 55.2), 2.15)
M_E.camera_key(a66, (35.5, 55.0), 2.05)
M_E.camera_key(b66, (35.0, 54.8), 2.3)
M_E.front("barbarossa", a60 + 1.2, a63b + 2.0, t_out=a66 + 0.9)
M_E.arrows("barbarossa", a60 + 1.0, a60 + 3.4, stagger=0.35, hold=a66 + 0.6)
M_E.zone("ussr_occupied_1941", a63b + 0.6, a63b + 1.4, t_out=a66 + 0.9)
M_E.front("moscow_1941", a66 + 0.9, b66 - 0.6)
M_E.arrows("moscow_counter", a66 + 0.9, a66 + 2.6, stagger=0.3)
M_E.label("GERMANY", a60 - 1, lonlat=(12.5, 51.6), size=44, t_out=a63b - 1)
M_E.label("SOVIET UNION", a60 - 1, lonlat=(38.5, 53.2), size=50, t_out=a63b - 1)
M_E.label("BALTIC SEA", at(60, 0.62), lonlat=(19.2, 57.6), size=30, color="ink_soft", t_out=a63b - 1)
M_E.label("BLACK SEA", at(60, 0.84), lonlat=(34.0, 43.4), size=30, color="ink_soft", t_out=a63b - 1)
M_E.city("Leningrad", a60 - 1, pulse=False)
M_E.city("Kiev", a60 - 1, pulse=False)
M_E.city("Moscow", a63b + 0.5)
M_E.stamp("COUNTER-ATTACK", (37.4, 54.15), a66 + 2.2, size=60)


def sh_east(cr, t, a, b):
    paper(cr)
    M_E.draw(cr, t)
    if a == a60 and t > a + 0.7:                                    # 3,000,000+ soldiers attack
        k = ease_out(seg(t, a + 0.7, a + 3.0))
        v = 3_000_000 * k
        s = f"{v:,.0f}" + ("+" if k >= 1 else "")
        cr.save()
        cr.rectangle(1330, 820, 520, 190)
        P.fill_ink(cr, "paper", 5, tone=False)
        cr.restore()
        text(cr, s, 1590, 935, 110, font=TITLE, color="axis", bold=False)
        text(cr, "SOLDIERS ATTACK", 1590, 990, 30, font=LABEL, color="ink_soft", spacing=4)


# ================================================================ 61: OPERATION BARBAROSSA
def sh_barbarossa(cr, t, a, b):
    u = lt(t, a)
    cr.save()
    push(cr, t, a, b, (W / 2, H * 0.4), 1.0, 1.07)
    paper(cr)
    rays(cr, t, W / 2, H * 0.42, n=28, color="ink", alpha=0.13, spin=0.03)
    halftone(cr, lambda c: c.rectangle(0, H * 0.74, W, H * 0.26), "ink", 2, 0.25)
    for i in range(4):                                              # a tank column rolls east along the bottom
        x = -500 + i * 520 + 260 * u
        P.Tank(x=x, y=1010, scale=0.55, facing=1, side="germany", speed=260, seed=i, silhouette="#3b393e").draw(cr, t)
    cr.restore()
    s = back_out(seg(t, a + 0.1, a + 0.35))
    if s > 0:
        cr.save()
        cr.translate(W / 2, H * 0.42)
        cr.rotate(-0.04)
        cr.scale(1.5 - 0.5 * s, 1.5 - 0.5 * s)
        text(cr, "OPERATION", 0, -120, 70, font=STENCIL, color="ink", spacing=14, alpha=min(1, 2 * s))
        cr.restore()
    stamp_box(cr, t, a + 0.35, "BARBAROSSA", W / 2, H * 0.47, size=170, color="ink", tilt=-0.04)


# ================================================================ 63a: prisoners on the steppe
def sh_prisoners(cr, t, a, b):
    u = lt(t, a)
    cr.save()
    cr.translate(80 - 160 * smooth(seg(t, a, b)), 0)                # slow pan
    push(cr, t, a, b, (W * 0.5, H * 0.6), 1.0, 1.05)
    sets.Sky(mode="dusk", horizon=560, clouds=3, seed=31, drift=10).draw(cr, t)
    cr.rectangle(-300, 560, W + 600, H)
    P.fill(cr, "#b8a678")
    halftone(cr, lambda c: c.rectangle(-300, 560, W + 600, H), "khaki", 2, 0.45)
    P.line(cr, -300, 560, W + 300, 560, 3)
    SP.prisoner_line(cr, u + 3.0, nation="soviet", ground=1000, horizon=575, n=22, scale=0.58, x_front=1450,
                     x_back=280, seed=63, snow=False)
    cr.restore()
    s = back_out(seg(t, a + 0.4, a + 0.65))
    if s > 0:
        cr.save()
        cr.translate(W / 2, 200)
        cr.rotate(-0.03)
        cr.scale(1.4 - 0.4 * s, 1.4 - 0.4 * s)
        text(cr, "MILLIONS", 0, 50, 150, font=SLAB, color="soviet", bold=False, outline="ink", outline_w=10,
             spacing=6, alpha=min(1, 2 * s))
        cr.restore()
    if u > 1.2:
        text(cr, "KILLED OR CAPTURED", W / 2, 320, 40, font=STENCIL, color="ink", spacing=8,
             alpha=ease_out(seg(t, a + 1.2, a + 1.6)), outline="paper", outline_w=5)


# ================================================================ 64: mud, then the snow
def sh_mud(cr, t, a, b):
    u = lt(t, a)
    snow_t = T.sentence(64, 1).start - 0.25 - a                    # "Then winter arrives."
    k = smooth(seg(u, snow_t, snow_t + 2.2))
    cr.save()
    cr.translate(-70 * smooth(seg(t, a, b)), 0)
    push(cr, t, a, b, (W * 0.5, H * 0.65), 1.0, 1.06)
    sets.Sky(mode="day", horizon=520, clouds=6, seed=41, drift=14).draw(cr, t)
    cr.rectangle(-200, 0, W + 400, 520)                            # the sky greys over as winter comes
    P.fill(cr, "#8d8f90", 0.15 + 0.4 * k)
    cr.rectangle(-200, 520, W + 400, H)
    P.fill(cr, "#8b7a5c")
    P.line(cr, -200, 520, W + 200, 520, 3)
    fx.mud(cr, t, -200, W + 300, 570, depth=520, seed=3)
    snow_cover(cr, k, 520)
    rock = math.sin(t * 9) * 0.8
    P.Truck(x=1480, y=760, scale=0.95, facing=1, side="germany", speed=120, seed=2).draw(cr, t)
    fx.mud_splash(cr, 1340, 760, (u * 1.0) % 0.9, size=0.9, seed=int(u / 0.9))
    cr.save()
    cr.translate(700, 935 + rock)
    cr.rotate(-0.04 + 0.006 * math.sin(t * 7))
    P.Tank(x=0, y=0, scale=1.4, facing=1, side="germany", speed=220, seed=1, exhaust=True).draw(cr, t)
    cr.restore()
    for i, x in enumerate((470, 600)):                             # tracks churn: clods thrown up behind
        fx.mud_splash(cr, x, 925, ((u + i * 0.4) % 0.8), size=1.1, seed=i * 7 + int((u + i * 0.4) / 0.8))
    fx.mud(cr, t, -200, W + 300, 890, depth=260, seed=8)          # the foreground lip buries the tracks
    snow_cover(cr, k, 890)
    cr.restore()
    if k > 0:
        P.snowfall(cr, t, density=int(40 + 200 * k), wind=60, seed=5, size=4.5, alpha=min(0.95, k * 1.4))


def snow_cover(cr, k, y0):
    """Snow settling on the ground from y0 down (drawn under the vehicles, so they stay readable)."""
    if k <= 0:
        return
    cr.rectangle(-200, y0, W + 400, H - y0 + 200)
    P.fill(cr, "#eef0ee", 0.8 * k)
    for i in range(12):
        r = random.Random(i)
        P.ellipse(cr, r.uniform(0, W), r.uniform(y0 + 30, H), r.uniform(80, 220), r.uniform(8, 18))
        P.fill(cr, "#ffffff", 0.5 * k)


# ================================================================ 65: winter, -30
def sh_winter(cr, t, a, b):
    u = lt(t, a)
    cr.save()
    push(cr, t, a, b, (W * 0.42, H * 0.6), 1.0, 1.07)
    sets.Sky(mode="day", horizon=700, clouds=2, seed=51, drift=40).draw(cr, t)
    cr.rectangle(-200, 0, W + 400, 700)
    P.fill(cr, "#9a9fa3", 0.45)
    SP.shivering_soldiers(cr, u, nation="germany", x=640, ground=960, n=3, scale=1.12, spacing=330, seed=9,
                          snow=True, coats=False)
    temp = -30 * smooth(seg(u, 0.6, 4.2))
    things.Thermometer(x=1560, y=960, scale=0.95, temp=temp, seed=1).draw(cr, t)
    cr.restore()
    P.snowfall(cr, t, density=230, wind=160, seed=9, size=5, alpha=0.95)
    if u > 4.2:
        s = back_out(seg(u, 4.2, 4.45))
        cr.save()
        cr.translate(1560, 200)
        cr.rotate(-0.05)
        cr.scale(1.4 - 0.4 * s, 1.4 - 0.4 * s)
        text(cr, "-30°C", 0, 40, 120, font=TITLE, color="allies", bold=False, outline="paper", outline_w=10,
             alpha=min(1, 2 * s))
        cr.restore()
    if u > 2.4:
        stencil_tag(cr, "NO WINTER UNIFORMS", 70, 190, 42, alpha=ease_out(seg(u, 2.4, 2.8)))


# ================================================================ 67a: whip pan to the Pacific
M_W = Map("world", era=None)
M_P = Map("pacific", era="1941")
a67, s67 = cut(67), at(67, 0.42)
WHIP = a67 + 1.0
M_W.camera_key(a67, (18.0, 48.0), 1.7)
M_W.camera_key(WHIP, (140.0, 30.0), 1.7)
M_P.camera_key(WHIP, (-178.0, 33.0), 1.15)
M_P.camera_key(s67, (-172.0, 30.0), 1.3)
M_P.arrows("pearl_harbor", WHIP + 0.2, WHIP + 1.8, width=80)
M_P.label("JAPAN", WHIP - 1, lonlat=(138.0, 37.5), size=40)
M_P.label("PACIFIC OCEAN", WHIP - 1, lonlat=(-170.0, 40.0), size=34, color="ink_soft")
M_P.city("Pearl Harbor", WHIP + 1.6, dx=18, dy=30)
M_P.label("HAWAII", WHIP + 1.6, lonlat=(-156.5, 18.6), size=30)


def sh_globe(cr, t, a, b):
    paper(cr)
    if t < WHIP:
        M_W.draw(cr, t)
        u = seg(t, a + 0.25, WHIP)                                  # speed streaks during the whip
        if 0 < u < 1:
            r = random.Random(int(t * 24))
            for i in range(14):
                y = r.uniform(80, H - 80)
                ln = r.uniform(200, 600) * math.sin(math.pi * u)
                x = r.uniform(0, W)
                P.line(cr, x, y, x - ln, y, 5, "ink", 0.35)
    else:
        M_P.draw(cr, t)


# ================================================================ 67b/68: Pearl Harbor
ROW = [(640, 975, 1.05), (1090, 850, 0.78), (1410, 776, 0.58), (1650, 730, 0.44)]
DIVES = [(0.2, 1500, -100, 640, 830), (0.9, 1850, -60, 1090, 730), (1.6, 1300, -140, 1410, 680)]


def ocean_scene(cr, t, a, hz=600, listing=0.0, smoke_k=0.0, dives=True, bursts=()):
    sets.Sky(mode="day", horizon=hz, clouds=4, seed=61, drift=10).draw(cr, t)
    cr.rectangle(-200, 0, W + 400, hz)
    P.fill(cr, "#6e6a62", 0.12 + 0.45 * smoke_k)
    things.Island(x=W * 0.3, y=hz + 4, scale=0.55, width=2400, seed=3).draw(cr, t)
    sets.Ocean(horizon=hz).draw(cr, t)
    for i, (x, y, s) in reversed(list(enumerate(ROW))):
        if smoke_k > 0:
            P.smoke(cr, x + 40 * s, y - 220 * s, t, height=700 * s + 400 * smoke_k, width=160 * s, color="#3d3a37",
                    alpha=0.9 * min(1, smoke_k * 2), wind=0.4, seed=i, dark=True)
        P.Battleship(x=x, y=y, scale=s, facing=-1, side="usa", speed=0, seed=i,
                     list_=listing * (1 if i % 2 == 0 else 0.4)).draw(cr, t)
    for k, (s, x, y, size) in enumerate(bursts):
        P.explosion(cr, x, y, t - s, size=size, seed=k)
    if dives:
        for i, (d, x0, y0, x1, y1) in enumerate(DIVES):
            u = seg(t, a + d, a + d + 1.3)
            if 0 < u < 1:
                x, y = lerp(x0, x1, u), lerp(y0, y1 - 380, u)
                P.DiveBomber(x=x, y=y, scale=0.62, facing=-1, side="japan", dive=1.0, release=a + d + 0.9,
                             seed=i).draw(cr, t)


def sh_pearl(cr, t, a, b):
    cr.save()
    push(cr, t, a, b, (W * 0.5, H * 0.6), 1.0, 1.07)
    bursts = [(a + d + 1.35, x1 + 30, y1 - 70, 0.7) for d, x0, y0, x1, y1 in DIVES]
    ocean_scene(cr, t, a, bursts=bursts, smoke_k=0.6 * seg(t, a + 1.6, b))
    cr.restore()


def sh_smoke(cr, t, a, b):
    u = lt(t, a)
    cr.save()
    cr.translate(-80 * smooth(seg(t, a, b)), 0)
    push(cr, t, a, b, (W * 0.45, H * 0.6), 1.08, 1.16)
    bursts = [(a + 0.5, 1020, 770, 0.9), (a + 1.8, 600, 860, 1.0), (a + 3.1, 1300, 730, 0.8),
              (a + 4.3, 820, 800, 0.9)]
    ocean_scene(cr, t, a - 10, listing=0.07 * smooth(seg(u, 0.3, 4.0)), smoke_k=0.6 + 0.4 * seg(u, 0, 3),
                dives=False, bursts=bursts)
    cr.restore()


# ================================================================ 69: 2,403
def sh_toll(cr, t, a, b):
    u = lt(t, a)
    paper(cr)
    cr.rectangle(0, 0, W, H)
    P.fill(cr, "#2c2a28", 0.78)
    for i in range(9):                                              # slow smoke drifting through
        fx.puff(cr, 200 + i * 200, 1100, (u + i * 0.55) % 4.0, size=2.2, seed=i, life=4.0, color="#45413c",
                rise=260)
    k = ease_out(seg(t, a + 0.3, a + 2.4))
    text(cr, f"{2403 * k:,.0f}", W / 2, H / 2 + 80, 260, font=TITLE, color="cream", bold=False, outline="ink",
         outline_w=14)
    if u > 1.6:
        text(cr, "AMERICANS KILLED", W / 2, H / 2 + 190, 52, font=STENCIL, color="cream", spacing=10,
             alpha=ease_out(seg(u, 1.6, 2.0)))


# ================================================================ the shot table
SHOTS = [
    (A0, cut(55), sh_bombers, "AUG 1940"),
    (cut(55), cut(56), sh_title, "AUG 1940"),
    (cut(56), at(56, 0.5), sh_radar, "AUG 1940"),
    (at(56, 0.5), cut(57), sh_scramble, "AUG 1940"),
    (cut(57), at(57, 0.48), sh_sealion, "SEPT 1940"),
    (at(57, 0.48), CARD[0], sh_blitz, "SEPT 1940"),
    (CARD[0], CARD[1], sh_card, None),
    (CARD[1], cut(59), sh_gamble, "JUNE 1941"),
    (cut(59), cut(60), sh_pact, "22 JUNE 1941"),
    (a60, b60, sh_east, "JUNE 1941"),
    (cut(61), cut(62), sh_barbarossa, "JUNE 1941"),
    (a62, b62, sh_east, "JULY 1941"),
    (cut(63), a63b, sh_prisoners, "SEPT 1941"),
    (a63b, b63b, sh_east, "DEC 1941"),
    (cut(64), cut(65), sh_mud, "OCT 1941"),
    (cut(65), cut(66), sh_winter, "DEC 1941"),
    (a66, b66, sh_east, "5 DEC 1941"),
    (a67, s67, sh_globe, "7 DEC 1941"),
    (s67, cut(68), sh_pearl, "7 DEC 1941"),
    (cut(68), cut(69), sh_smoke, "7 DEC 1941"),
    (cut(69), B0, sh_toll, "7 DEC 1941"),
]
SNOW_TAG = T.sentence(64, 1).start


def _shot(t):
    for k, s in enumerate(SHOTS):
        if t < s[1] or k == len(SHOTS) - 1:
            return k, s
    return len(SHOTS) - 1, SHOTS[-1]


def draw(cr, t):
    k, (a, b, fn, tag) = _shot(t)
    cr.save()
    fn(cr, t, a, b)
    cr.restore()
    if fn is sh_mud and t >= SNOW_TAG:
        date_stamp(cr, t, "NOV 1941", start=SNOW_TAG)
    elif tag:
        prev = SHOTS[k - 1][3] if k > 0 else None
        date_stamp(cr, t, tag, start=a if tag != prev else a - 10)
    print_finish(cr, t)


def cues(T=T):
    c = []
    a = SHOTS[0][0]
    c += [(a + 0.1, "plane_drone", -6, -0.3), (cut(55) + 0.1, "stamp", -4, 0), (cut(56) + 0.7, "morse", -14, 0.4)]
    c += [(at(56, 0.5) + 0.1, "plane_drone", -8, 0.2), (at(56, 0.5) + 1.3, "rifle_crack", -16, 0.3)]
    c += [(cut(57) + 1.05, "stamp", -3, 0.1)]
    s = at(57, 0.48)
    c += [(s + 0.1, "plane_drone", -10, 0)] + [(s + h[0], "explosion", -12, (h[1] / W) * 2 - 1) for h in HITS]
    c += [(CARD[0] + 0.05, "page_whoosh", -4, 0), (CARD[1] + 0.15, "clock_tick", -10, 0)]
    p = cut(60)
    c += [(at(59, 0.40), "page_whoosh", -2, 0), (at(59, 0.72), "tank", -6, 0.3)]
    c += [(p + 1.0, "artillery_barrage", -8, 0.2), (p + 1.2, "tank", -6, 0.4)]
    c += [(cut(61) + 0.35, "stamp", -2, 0), (cut(61) + 0.1, "tank", -8, 0)]
    c += [(cut(62) + 0.1, "tank", -8, 0.4), (cut(63) + 0.4, "stamp", -6, 0)]
    c += [(cut(64) + 0.2, "tank", -6, -0.3), (SNOW_TAG - 0.2, "blizzard", -12, 0), (cut(65), "blizzard", -6, 0)]
    c += [(a66 + 0.9, "artillery_barrage", -8, 0.4), (a66 + 2.2, "stamp", -4, 0.2)]
    c += [(a67 + 0.2, "page_whoosh", -4, 0.6), (WHIP + 0.2, "plane_drone", -10, 0.3)]
    c += [(s67 + d + 0.2, "dive_whine", -6, 0.4) for d, *_ in DIVES]
    c += [(s67 + d + 1.35, "explosion", -10, (x1 / W) * 2 - 1) for d, x0, y0, x1, y1 in DIVES]
    c += [(cut(68) + o, "explosion", -14, 0) for o in (0.5, 1.8, 3.1, 4.3)]
    c += [(cut(69) + 2.4, "clock_tick", -10, 0)]
    return sorted(c)
