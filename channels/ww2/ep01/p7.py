"""WW2 Episode 1, package P7 (script lines 102-116, helper 5): D-Day to Hiroshima, in the 1940s poster look.

Every beat is placed from the episode clock (timing.json via Timing), so the package follows the voiced timing:
shot cuts sit at line/sentence starts (a few tenths before), and the beats inside each shot are fractions of their
line. Shots (SHOTLIST.md C6-S07 .. C7-S09):

    102  D-DAY date poster: JUNE 6 / 1944 pop on khaki rays over the invasion fleet's silhouette; D-DAY slams in
    103  Normandy (Natural Earth 10m): the 156,000 counter, the nations named in turn, five sea arrows land on the five
         beaches, parachute icons drop inland; a Europe locator inset. Then paratroopers drift down at dawn ("by air")
    104  Omaha: a squad dashes across the sand past steel hedgehogs, flat bursts and sand puffs; then sunset on the
         held beach, plain flags in the sand, ASHORE
    105  Bagration: the grey ARMY GROUP CENTRE block in the German-held band; Soviet arrows smash it to shards, the
         front rolls west to the Vistula, DESTROYED
    106  Paris skyline, the crowd cheers, hats and confetti, PARIS LIBERATED
    107-108  The Bulge: the grey bulge pushes into the Allied line through the Ardennes (snow), Bastogne ringed;
         then it collapses, the Allied arrow relieves Bastogne, FAILED
    109-109b  Pacific: blue arrows hop island to island toward Japan; the camera swings west: China in gold holds its
         long front; a blue arrow pushes out of India into Burma
    110  Iwo Jima / Okinawa: a volcanic island under flat bursts, a casualty bar chart grows (no numbers); then three
         worried American generals around a map of Japan
    C7   Chapter 7 card (title from timing.json)
    111  Berlin: Soviet arrows and the red ring close round the city, flashes in the streets
    112  The bunker corridor: the steel door slams shut, then silence (no method, nothing shown)
    113  Reims: the surrender signed at a table, SURRENDER
    114  V-E Day: London's crowd cheering, hats flying (8 May); Moscow's crowd under fireworks (9 May)
    115  The quiet Pacific: one ship on calm water
    116  A lone bomber high over the clouds; far away, a white flash and a pale mushroom silhouette on the horizon
         (nothing graphic: no city, no people)

No national emblems beyond plain marks; no red rays; Soviet = red, Allies = navy, Germany = charcoal, China = gold.
"""
import math
import random

from channels.ww2.kit.core import *  # noqa: F401,F403
from channels.ww2.kit.core import (H, LABEL, SLAB, STENCIL, TITLE, W, back_out, cairo, chapter_card, col,
                                   date_stamp, ease_in, ease_out, halftone, lerp, paper, paper_surface, print_finish,
                                   rays, seg, shake, smooth, text, word_card)
from channels.ww2.kit import fx as F
from channels.ww2.kit import props as P
from channels.ww2.kit import sets as S
from channels.ww2.kit import setpieces as SP
from channels.ww2.kit import stick as St
from channels.ww2.kit import things as Th
from channels.ww2.kit import maps as M
from channels.ww2.kit.maps import Map
from channels.ww2.ep01.timing import Timing, package_span

T = Timing()
PA, PB = package_span("P7", T)


def L(i):
    return T.line(str(i))


def SN(i, k):
    return T.sentence(str(i), k)


def at(i, u):
    """A point u (0-1) of the way through line i (the beats inside a line, from its voiced span)."""
    ln = L(i)
    return ln.start + u * (ln.end - ln.start)


C7 = T.chapter("C7").card

# ---------------------------------------------------------------- the cuts (episode seconds)
CUT = dict(
    dday=PA,
    normandy=L(103).start - 0.35,
    para=at(103, 0.80),
    omaha=L(104).start - 0.3,
    sunset=SN(104, 1).start - 0.15,
    bagration=L(105).start - 0.3,
    paris=L(106).start - 0.3,
    bulge=L(107).start - 0.3,
    pacific=L(109).start - 0.3,
    iwo=L(110).start - 0.3,
    generals=at(110, 0.52),
    card7=C7[0],
    berlin=C7[1] - 0.1,
    bunker=L(112).start - 0.3,
    reims=L(113).start - 0.3,
    london=L(114).start - 0.3,
    moscow=SN(114, 1).start - 0.15,
    quiet=L(115).start - 0.3,
    bomber=L(116).start - 0.3,
    flash=at(116, 0.66),
)
ORDER = sorted(CUT, key=CUT.get)


def span(name):
    i = ORDER.index(name)
    return CUT[name], (CUT[ORDER[i + 1]] if i + 1 < len(ORDER) else PB)


# ---------------------------------------------------------------- shared helpers
def push(cr, t, a, b, z0=1.0, z1=1.07, fx=W / 2, fy=H / 2, dx=0.0, dy=0.0):
    """The slow push-in (every shot), toward (fx, fy), with an optional slow track (dx, dy px over the shot)."""
    u = smooth(seg(t, a, b))
    z = lerp(z0, z1, u)
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx - dx * u, -fy - dy * u)


def in_map(m, cr, fn):
    """Draw fn(z) in the map's pixel space with the camera of m's last draw()."""
    (cx, cy), z = m._c, m._z
    cr.save()
    cr.translate(W / 2, H / 2)
    cr.scale(z, z)
    cr.translate(-cx, -cy)
    fn(z)
    cr.restore()


def front_pts(f, t):
    """The current polyline (map px) of a front added with Map.front()."""
    keys = f["keys"]
    pts = keys[0][1]
    for (ta, pa), (tb, pb) in zip(keys, keys[1:]):
        if t >= tb:
            pts = pb
        elif t > ta:
            u = smooth(seg(t, ta, tb))
            return [(lerp(p[0], q[0], u), lerp(p[1], q[1], u)) for p, q in zip(pa, pb)]
    return pts


def band_zone(m, f, edge_key, side="germany"):
    """A held-ground band between a moving front and a fixed edge (one of the front's keyframes): an "occupied"
    zone whose outline is rebuilt every frame (update_band)."""
    zn = dict(kind="occupied", side=side, geom=[], t0=-1e9, t1=-1e9 + 0.01, t_out=None, path=None, f=f,
              edge=f["keys"][edge_key][1])
    m.zones.append(zn)
    return zn


def update_band(zn, t, t_in=None, t_out=None):
    cur = front_pts(zn["f"], t)
    zn["path"] = M._poly_path([cur + zn["edge"][::-1] + [cur[0]]])
    zn["t0"], zn["t1"] = (t_in, t_in + 0.5) if t_in is not None else (-1e9, -1e9 + 0.01)
    zn["t_out"] = t_out


def panel(cr, x, y, w, h, color="alert", tilt=-0.02, u=1.0):
    """A poster label band (ink key line, hard shadow)."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    cr.scale(u, u)
    P.poly(cr, [(-w / 2 + 8, -h / 2 + 8), (w / 2 + 8, -h / 2 + 4), (w / 2 + 4, h / 2 + 8), (-w / 2 + 4, h / 2 + 10)])
    P.fill(cr, "ink", 0.85)
    P.poly(cr, [(-w / 2, -h / 2), (w / 2, -h / 2 - 4), (w / 2 - 4, h / 2), (-w / 2 - 4, h / 2 + 2)])
    P.fill_ink(cr, color, 5, tone=False)
    cr.restore()


def caption(cr, t, t0, s, x, y, size=46, color="cream", band="ink", t_out=None, tilt=-0.02, font=None):
    """A stencil caption on a band that pops in at t0."""
    if t < t0 or (t_out is not None and t > t_out):
        return
    u = back_out(seg(t, t0, t0 + 0.28))
    cr.save()
    cr.select_font_face(font or STENCIL)
    cr.set_font_size(size)
    w = cr.text_extents(s).x_advance + size * 0.12 * len(s) + 50
    cr.restore()
    panel(cr, x, y, w, size * 1.35, band, tilt, u)
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    cr.scale(u, u)
    text(cr, s, 0, size * 0.36, size, font=font or STENCIL, color=color, spacing=size * 0.12)
    cr.restore()


def stamp(cr, t, t0, word, x, y, size=120, color="alert", tilt=-0.1):
    """A rubber stamp that slams down (overshoot), a boxed word in stencil with worn ink."""
    if t < t0:
        return
    u = seg(t, t0, t0 + 0.18)
    k = lerp(1.9, 1.0, ease_in(u))
    a = min(1.0, u * 3)
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    cr.scale(k, k)
    cr.select_font_face(STENCIL, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(size)
    w = cr.text_extents(word).x_advance + size * 0.1 * len(word)
    for pad, lw in ((26, 9), (40, 5)):
        P.rrect(cr, -w / 2 - pad, -size * 0.62 - pad * 0.5, w + 2 * pad, size * 1.2 + pad, 6)
        P.ink(cr, lw, color, a * 0.9)
    text(cr, word, 0, size * 0.36, size, font=STENCIL, color=color, alpha=a * 0.92, spacing=size * 0.1)
    cr.restore()


# ================================================================ 102: D-DAY date poster
def _fleet(cr, t, hz):
    r = random.Random(102)
    for i in range(16):                                           # far ships in haze, barrage balloons over them
        x = (i * 137 + r.uniform(-30, 30) + t * 9) % (W + 300) - 150
        cls = r.choice((P.Destroyer, P.Battleship, P.FishingBoat, P.Destroyer))
        s = r.uniform(0.09, 0.16)
        cls(silhouette="#6d6a5f", side="usa", water=None).draw(cr, t, x=x, y=hz + 4, scale=s, facing=1, speed=0)
        if i % 3 == 0:
            by = hz - 110 - r.uniform(0, 40) + 4 * math.sin(t * 0.9 + i)
            P.line(cr, x, hz - 20, x + 6, by, 1.2, "#6d6a5f")
            P.ellipse(cr, x + 6, by, 15, 8)
            P.fill_ink(cr, "#8b8778", 2, tone=False)


def _landing_craft(cr, x, y, s, t, seed=0, ramp=0.0, tone="#3f4a46"):
    """A flat-bottomed landing craft from the side (bow ramp at the right), bobbing; ramp 0..1 drops the ramp."""
    bob = math.sin(t * 2.1 + seed) * 4 * s
    cr.save()
    cr.translate(x, y + bob)
    cr.scale(s, s)
    P.poly(cr, [(-150, -40), (110, -44), (130, 0), (-140, 0)])
    P.fill_ink(cr, tone, 5)
    P.poly(cr, [(-150, -40), (-95, -40), (-95, -70), (-140, -70)])                    # the coxswain's box
    P.fill_ink(cr, P.shade(tone, -0.2), 4)
    cr.save()
    cr.translate(110, -44)
    cr.rotate(ramp * 1.2)
    P.poly(cr, [(0, 0), (14, 0), (26, 44), (12, 44)])
    P.fill_ink(cr, P.shade(tone, 0.12), 4)
    cr.restore()
    for k in range(5):                                                               # helmets over the gunwale
        cr.arc(-70 + k * 34, -46, 11, math.pi, 2 * math.pi)
        P.fill_ink(cr, "allies", 3, tone=False)
    cr.restore()


def shot_dday(cr, t, a, b):
    l102 = L(102)
    cr.save()
    push(cr, t, a, b, 1.0, 1.08, W / 2, H * 0.55)
    paper(cr)
    rays(cr, t, W / 2, 820, n=30, color="khaki", alpha=0.3, spin=0.02)
    hz = 820
    cr.rectangle(-200, hz, W + 400, H)
    P.fill(cr, "sea")
    for i, y in enumerate(range(hz + 10, H + 80, 22)):
        cr.set_dash([90, 30], -(t * 20 + i * 41) % 120)
        P.line(cr, -200, y, W + 200, y, 2 + i * 0.4, "sea_dk", 0.9)
        cr.set_dash([])
    _fleet(cr, t, hz)
    for i, (x0, y, s) in enumerate(((-120, 930, 0.55), (420, 1010, 0.75), (1300, 960, 0.6))):
        _landing_craft(cr, x0 + 70 * (t - a) + 40 * i, y, s, t, seed=i)
    P.line(cr, -200, hz, W + 200, hz, 3, "ink")
    cr.restore()
    u1 = back_out(seg(t, l102.start - 0.1, l102.start + 0.25))
    if u1 > 0:
        cr.save()
        cr.translate(W / 2, 250)
        cr.scale(u1, u1)
        text(cr, "JUNE 6", 0, 50, 150, font=SLAB, color="ink", bold=False, outline="paper", outline_w=14, spacing=4)
        cr.restore()
    u2 = back_out(seg(t, l102.start + 1.0, l102.start + 1.3))
    if u2 > 0:
        cr.save()
        cr.translate(W / 2, 400)
        cr.scale(u2, u2)
        panel(cr, 0, -36, 380, 120, "allies", -0.02)
        text(cr, "1944", 0, 8, 110, font=TITLE, color="cream", bold=False, spacing=8)
        cr.restore()
    d0 = SN(102, 1).start - 0.05
    if t >= d0:
        u = seg(t, d0, d0 + 0.2)
        k = lerp(2.2, 1.0, ease_in(u))
        cr.save()
        cr.translate(W / 2, 640 + shake(t, d0 + 0.2, 0.3, 10)[1])
        cr.rotate(-0.04)
        cr.scale(k, k)
        text(cr, "D-DAY", 8, 98, 270, font=SLAB, color="ink", bold=False, alpha=min(1, u * 3) * 0.6)
        text(cr, "D-DAY", 0, 90, 270, font=SLAB, color="alert", bold=False, alpha=min(1, u * 3), outline="ink",
             outline_w=16, spacing=6)
        cr.restore()
    date_stamp(cr, t, "6 JUNE 1944", start=a - 1)


# ================================================================ 103: Normandy map, then paratroopers
M103 = Map("normandy", era="1941")
_n0 = CUT["normandy"]
M103.camera_key(_n0, (-0.55, 49.75), 11.0)
M103.camera_key(at(103, 0.55), (-0.74, 49.45), 18.0)
M103.camera_key(CUT["para"] + 0.5, (-0.74, 49.38), 21.0)
M103.arrows("normandy_1944", at(103, 0.5), at(103, 0.68), stagger=0.18)
M103.pins("normandy_beaches", at(103, 0.62), stagger=0.18)
M103.label("FRANCE", at(103, 0.6), lonlat=(-0.2, 48.95), size=56, color="cream")
M103.label("ENGLAND", _n0 + 0.2, lonlat=(-1.2, 50.85), size=44, color="cream")
M103.label("ENGLISH CHANNEL", _n0 + 0.5, lonlat=(-0.95, 50.25), size=26, color="ink_soft", font=LABEL)
NATIONS = [("AMERICAN", 0.28, "allies"), ("BRITISH", 0.355, "allies"), ("CANADIAN", 0.42, "allies"),
           ("+ OTHER ALLIES", 0.5, "ink_soft")]
AIRBORNE = [(-1.32, 49.36), (-1.25, 49.42), (-1.4, 49.31), (-0.22, 49.24), (-0.16, 49.2), (-0.3, 49.2)]
_INSET = {}


def _inset_surface():
    """A small static Europe locator (cached): the 1941 map at a wide zoom, drawn once."""
    if "s" in _INSET:
        return _INSET["s"]
    m = Map("europe", era="1941", compass=False)
    m.camera_key(0, (6.0, 50.0), 1.6)
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    m.draw(cairo.Context(s), 0)
    box = [m.screen(m.xy(p)) for p in ((-2.2, 50.6), (0.8, 50.6), (0.8, 48.6), (-2.2, 48.6))]
    _INSET["s"], _INSET["box"] = s, box
    return s


def _inset(cr, t, t0):
    u = back_out(seg(t, t0, t0 + 0.35))
    if u <= 0:
        return
    s = _inset_surface()
    w, h = 400, 225
    x, y = W - w - 60, H - h - 70
    cr.save()
    cr.translate(x + w / 2, y + h / 2)
    cr.scale(u, u)
    cr.translate(-w / 2, -h / 2)
    cr.rectangle(10, 10, w, h)
    P.fill(cr, "ink", 0.8)
    cr.save()
    cr.rectangle(0, 0, w, h)
    cr.clip()
    sc = w / W
    cr.scale(sc, sc)
    cr.set_source_surface(s, 0, 0)
    cr.paint()
    P.poly(cr, _INSET["box"])
    P.ink(cr, 6 / sc * 0.6, "alert")
    cr.restore()
    cr.rectangle(0, 0, w, h)
    P.ink(cr, 5, "ink")
    text(cr, "EUROPE", 14, h - 14, 26, font=STENCIL, color="cream", align="left", outline="ink", outline_w=5,
         spacing=3)
    cr.restore()


def shot_normandy(cr, t, a, b):
    M103.draw(cr, t)
    z = M103._z
    for i, p in enumerate(AIRBORNE):                                   # parachute icons drop inland ("by air")
        t0 = at(103, 0.7) + i * 0.12
        if t >= t0:
            x, y = M103.screen(M103.xy(p))
            drop = (1 - ease_out(seg(t, t0, t0 + 0.8))) * 120
            Th.ParachuteIcon(side="allies").draw(cr, t, x=x, y=y - drop, scale=0.75 * min(1.0, z / 18))
    # the 156,000 counter panel
    c0 = L(103).start + 0.1
    pop = back_out(seg(t, c0 - 0.2, c0 + 0.1))
    if pop > 0:
        cr.save()
        cr.translate(W - 360, 170)
        cr.scale(pop, pop)
        cr.rotate(-0.025)
        panel(cr, 0, 70, 520, 66, "allies", 0)
        v = 156000 * ease_out(seg(t, c0, at(103, 0.27)))
        text(cr, f"{v:,.0f}", 0, 34, 150, font=TITLE, color="cream", bold=False, outline="ink", outline_w=13)
        text(cr, "ALLIED TROOPS", 0, 90, 40, font=STENCIL, color="cream", spacing=5)
        cr.restore()
    for i, (name, u, c) in enumerate(NATIONS):                          # the nations, as they're named
        t0 = at(103, u)
        if t >= t0:
            k = back_out(seg(t, t0, t0 + 0.25))
            cr.save()
            cr.translate(W - 360, 340 + i * 56)
            cr.scale(k, k)
            text(cr, name, 0, 0, 40, font=STENCIL, color=c if c != "allies" else "allies", outline="paper",
                 outline_w=8, spacing=4)
            cr.restore()
    _inset(cr, t, a + 0.4)
    caption(cr, t, at(103, 0.6), "NORMANDY", 330, 230, 54, band="allies")
    date_stamp(cr, t, "6 JUNE 1944", start=a - 1)


PARAS = []
_r = random.Random(7)
for _i in range(14):
    PARAS.append(dict(x=_r.uniform(80, W - 80), y0=_r.uniform(-260, 380), v=_r.uniform(55, 95), s=_r.uniform(0.22, 0.6),
                      seed=_i, open=_r.uniform(-0.6, 0.6)))
PARAS.sort(key=lambda p: p["s"])


def shot_para(cr, t, a, b):
    cr.save()
    push(cr, t, a, b, 1.0, 1.06, W / 2, H * 0.4)
    S.Sky(mode="dusk", horizon=900, clouds=3, seed=5).draw(cr, t)
    cr.rectangle(-200, 900, W + 400, 400)
    P.fill(cr, "#4d4a35")
    Th.forest(cr, t, -100, W + 100, 905, n=26, scale=0.45, seed=3, kind="oak", tone="#3b3a2b", rows=2)
    for i in range(3):                                                    # transports crossing high
        u = seg(t, a - 1.5 + i * 0.5, b + 2.5)
        P.Bomber(side="usa", silhouette="#2e2d29").draw(cr, t, x=lerp(-300, W + 300, u) - i * 260,
                                                       y=120 + i * 70, scale=0.32 - i * 0.04, engines=2)
    for p in PARAS:
        y = p["y0"] + p["v"] * (t - a) * (0.6 + p["s"])
        x = p["x"] + math.sin(t * 0.7 + p["seed"]) * 30
        tone = P.mix("#5a5648", "ink", p["s"] * 1.4)
        P.Parachute(side="usa", silhouette=None if p["s"] > 0.45 else tone).draw(
            cr, t, x=x, y=y, scale=p["s"], open_at=a + p["open"] if p["s"] > 0.45 else None)
    cr.restore()
    caption(cr, t, a + 0.25, "BY AIR", 260, 220, 60, band="allies")
    date_stamp(cr, t, "6 JUNE 1944", start=a - 1)


# ================================================================ 104: Omaha, then the held beach at sunset
SAND, SAND_DK = "#d2b985", "#b09a68"
HEDGE = [(x, y, s) for x, y, s in ((380, 700, 0.32), (760, 690, 0.3), (1180, 705, 0.34), (1560, 695, 0.3),
                                   (220, 790, 0.45), (980, 780, 0.48), (1420, 800, 0.5), (620, 900, 0.7),
                                   (1720, 930, 0.75))]
BURSTS = [0.35, 0.95, 1.5, 2.2, 2.75]


def _beach(cr, t, hz, sand=SAND, dk=SAND_DK, foam="cream"):
    cr.rectangle(-200, hz + 70, W + 400, H)
    P.fill(cr, sand)
    cr.rectangle(-200, hz + 70, W + 400, H)
    P.dots(cr, dk, 1, 0.6)
    cr.new_path()
    pts = [(x, hz + 70 + 8 * math.sin(x * 0.01 + t * 1.3)) for x in range(-200, W + 240, 40)]
    P.poly(cr, pts, close=False)
    P.ink(cr, 6, foam, 0.9)


def shot_omaha(cr, t, a, b):
    hz = 560
    cr.save()
    push(cr, t, a, b, 1.02, 1.09, W * 0.55, H * 0.6, dx=60)
    S.Sky(mode="day", horizon=hz, clouds=2, seed=9).draw(cr, t)
    S.Ocean(horizon=hz).draw(cr, t)
    for i, (x, cls, s) in enumerate(((260, P.Battleship, 0.16), (820, P.Destroyer, 0.14), (1380, P.Battleship, 0.15),
                                     (1750, P.Destroyer, 0.12))):
        cls(silhouette="#6d6a5f", side="usa", water=None).draw(cr, t, x=x, y=hz + 3, scale=s, facing=-1, speed=0)
    for i, x in enumerate((180, 760, 1350)):
        _landing_craft(cr, x, hz + 66, 0.42, t, seed=i, ramp=1.0)
    _beach(cr, t, hz)
    for x, y, s in HEDGE:
        Th.Hedgehog().draw(cr, t, x=x, y=y, scale=s)
    for k, s in enumerate(BURSTS):                                        # flat bursts and sand puffs behind
        bx = 300 + (k * 397) % 1400
        F.puff(cr, bx, 760 - k % 2 * 40, t - (a + s), size=0.9, seed=k, color=SAND_DK)
        F.starburst(cr, bx, 740 - k % 2 * 40, t - (a + s), size=0.7, seed=k)
    SP.squad_advance(cr, t - a + 0.6, nation="usa", x0=40.0, ground=1010.0, n=5, scale=0.5, spacing=210.0, speed=170)
    cr.restore()
    caption(cr, t, a + 0.3, "OMAHA BEACH", 1530, 190, 58, band="allies")
    date_stamp(cr, t, "6 JUNE 1944", start=a - 1)


def shot_sunset(cr, t, a, b):
    hz = 600
    s1 = SN(104, 1)
    cr.save()
    push(cr, t, a, b, 1.0, 1.06, W * 0.62, H * 0.55)
    S.Sky(mode="sunset", horizon=hz, clouds=3, seed=4).draw(cr, t)
    S.Ocean(horizon=hz, color="#8aa29c", swell=0.4).draw(cr, t)
    for i, (x, cls, s) in enumerate(((240, P.Battleship, 0.17), (700, P.Destroyer, 0.14), (1500, P.Battleship, 0.16))):
        cls(silhouette="#3e3a33", side="usa", water=None).draw(cr, t, x=x, y=hz + 3, scale=s, facing=1, speed=0)
    _beach(cr, t, hz, sand="#b98f58", dk="#8e6c3f", foam="#f0d39a")
    for i, x in enumerate((140, 1720)):
        _landing_craft(cr, x, hz + 96, 0.5, 0, seed=i, ramp=1.0, tone="#2f2d29")
    for x, y, s in HEDGE[4:]:
        Th.Hedgehog(silhouette="#3e3a33").draw(cr, t, x=x - 120, y=y, scale=s * 0.8)
    for i, x in enumerate((760, 1190)):                                   # plain flags in the sand
        Th.Flag(color="allies", seed=i).draw(cr, t, x=x, y=880 + i * 30, scale=0.9 + i * 0.1)
    poses = ["stand", "wave", "idle", "point", "stand"]
    for i, x in enumerate((470, 620, 990, 1330, 1500)):
        St.Figure(nation="usa", x=x, y=930 + (i % 2) * 50, scale=0.55 + (i % 2) * 0.07, facing=1 if i % 2 else -1,
                  color="#2b2925", seed=i).draw(cr, t, track=[(0, poses[i])])
    cr.restore()
    word_card(cr, t, s1.start + 0.62 * (s1.end - s1.start), "ASHORE", dur=10, y=H * 0.24, size=150, color="allies")
    date_stamp(cr, t, "6 JUNE 1944", start=a - 1)


# ================================================================ 105: Operation Bagration
def _era(view, era):
    return M.content()["eras"][view][era]


_e41 = _era("europe", "1941")
M105 = Map("europe", era="1941", sides={"latvia": "germany", "estonia": "germany"},
           occupied=set(_e41["occupied"]) | {"latvia", "estonia"})
_b0 = CUT["bagration"]
HIT105 = at(105, 0.42)
M105.camera_key(_b0, (28.0, 53.6), 2.0)
M105.camera_key(PB, (25.5, 53.4), 2.6)
M105.front("bagration", HIT105, at(105, 0.95), width=8, side="germany")
F105 = M105.fronts[-1]
Z105 = band_zone(M105, F105, 1)
M105.arrows("bagration", at(105, 0.18), HIT105, stagger=0.22)
for _p in ([[33.5, 55.8], [29.5, 55.4], [26.0, 55.6], [23.6, 55.0]], [[32.5, 51.3], [28.5, 51.2], [25.2, 51.7], [23.0, 51.6]]):
    M105.arrow([tuple(q) for q in _p], "soviet", at(105, 0.3), at(105, 0.62), width=60)
M105.city("Minsk", at(105, 0.58))
M105.city("Warsaw", at(105, 0.86))
M105.label("SOVIET UNION", _b0, lonlat=(34.0, 50.6), size=46, color="cream")
BLOCK = (28.6, 53.7)                                                         # Army Group Centre, east of Minsk


def _shards(cr, t, x, y, t_hit, w=330, h=130):
    """The grey block, whole until the hit, then five shards that fly apart, spin and fade."""
    pieces = [[(-1, -1), (-0.2, -1), (-0.35, 0.1), (-1, 0.2)], [(-0.2, -1), (0.45, -1), (0.2, 0.05), (-0.35, 0.1)],
              [(0.45, -1), (1, -1), (1, 0.3), (0.2, 0.05)], [(-1, 0.2), (-0.35, 0.1), (-0.1, 1), (-1, 1)],
              [(-0.35, 0.1), (0.2, 0.05), (1, 0.3), (1, 1), (-0.1, 1)]]
    age = t - t_hit
    for k, pc in enumerate(pieces):
        cx = sum(p[0] for p in pc) / len(pc)
        cy = sum(p[1] for p in pc) / len(pc)
        if age > 0:
            u = ease_out(min(1.0, age / 1.4))
            dx, dy = cx * 260 * u - 60 * u, cy * 160 * u + 90 * u * u
            rot = (k - 2) * 0.5 * u
            a = 1 - ease_in(seg(age, 0.7, 1.6))
        else:
            dx = dy = rot = 0.0
            a = 1.0
        if a <= 0:
            continue
        cr.save()
        cr.translate(x + dx + cx * w / 2, y + dy + cy * h / 2)
        cr.rotate(rot)
        P.poly(cr, [((p[0] - cx) * w / 2, (p[1] - cy) * h / 2) for p in pc])
        cr.push_group()
        P.fill_ink(cr, "axis", 5, a=1.0)
        cr.pop_group_to_source()
        cr.paint_with_alpha(a)
        cr.restore()
    if age < 0.05:
        text(cr, "ARMY GROUP", x, y - 8, 38, font=STENCIL, color="cream", spacing=4)
        text(cr, "CENTRE", x, y + 40, 46, font=STENCIL, color="cream", spacing=6)


def shot_bagration(cr, t, a, b):
    update_band(Z105, t)
    saved, M105.arrows_ = M105.arrows_, []
    M105.draw(cr, t)
    M105.arrows_ = saved
    x, y = M105.screen(M105.xy(BLOCK))
    pop = back_out(seg(t, a + 0.1, a + 0.45))
    if pop > 0:
        cr.save()
        cr.translate(x, y)
        cr.scale(pop, pop)
        cr.translate(-x, -y)
        _shards(cr, t, x, y, HIT105)
        cr.restore()
    in_map(M105, cr, lambda z: [M105._draw_arrow(cr, ar, t, z) for ar in M105.arrows_])
    for k in range(4):
        F.starburst(cr, x + (k - 1.5) * 90, y + (k % 2) * 50 - 20, t - HIT105 - k * 0.12, size=0.8, seed=k)
    word_card(cr, t, at(105, 0.4), "OPERATION BAGRATION", dur=at(105, 0.72) - at(105, 0.4), y=H * 0.15, size=96,
              color="soviet")
    stamp(cr, t, at(105, 0.8), "DESTROYED", x + 40, y + 10, 90, "alert", -0.12)
    date_stamp(cr, t, "22 JUNE 1944", start=a - 1)


# ================================================================ 106: Paris
def tricolour(cr, t, x, y, scale=0.9, facing=1, seed=0, h=260.0):
    """The French tricolour on a pole: three vertical stripes, blue at the hoist, then white, then red (no emblem),
    waving like things.Flag."""
    cr.save()
    cr.translate(x, y)
    cr.scale(scale * (1 if facing >= 0 else -1), scale)
    lw = 5.0
    P.line(cr, 0, 0, 0, -h, lw)

    def edge(u, top):
        wv = math.sin(t * 5 - u * 4 + seed) * 10 * u
        return (u * 150, (-h + 4 if top else -h + 84 - u * 10) + wv)

    for k, c in enumerate(("allies", "white", "alert")):
        us = [k / 3 + j / 12 for j in range(5)]
        P.poly(cr, [edge(u, True) for u in us] + [edge(u, False) for u in us[::-1]])
        P.fill(cr, c)
    us = [j / 12 for j in range(13)]
    P.poly(cr, [edge(u, True) for u in us] + [edge(u, False) for u in us[::-1]])
    P.ink(cr, lw * 0.7)
    cr.restore()


def shot_paris(cr, t, a, b):
    cr.save()
    push(cr, t, a, b, 1.0, 1.07, W * 0.5, H * 0.45)
    S.Sky(mode="day", horizon=700, clouds=2, rays=True, seed=12).draw(cr, t)
    S.Skyline(city="paris", ground=700, seed=6).draw(cr, t)
    for i, x in enumerate((260, 1660)):
        tricolour(cr, t, x, 720, scale=0.9, facing=1 if i == 0 else -1, seed=i)
    SP.cheering_crowd(cr, t, x0=-40, x1=W + 40, y0=690, y1=1090, n=48, scale=0.5, front=6, seed=11)
    cr.restore()
    word_card(cr, t, L(106).start + 0.9, "PARIS LIBERATED", dur=10, y=H * 0.2, size=118, color="allies")
    date_stamp(cr, t, "AUG 1944", start=a - 1)


# ================================================================ 107-108: the Battle of the Bulge
_side44 = {"france_occ": "allies", "france_north": "allies", "france_vichy": "allies", "belgium": "allies",
           "luxembourg": "allies", "channel_islands": "germany"}
M107 = Map("europe", era="1941", sides=_side44,
           occupied=set(_e41["occupied"]) - {"france_occ", "france_north", "belgium", "luxembourg"})
_g0 = CUT["bulge"]
P107 = at(107, 0.2)
E107 = at(107, 0.72)
H108 = L(108).start
M107.camera_key(_g0, (5.9, 50.15), 5.4)
M107.camera_key(E107, (5.6, 50.15), 6.6)
M107.camera_key(H108 - 0.2, (5.6, 50.15), 6.6)
M107.camera_key(CUT["pacific"], (5.9, 50.2), 5.6)
M107.front("bulge", P107, E107, width=8, side="germany")
M107.front([(H108 - 0.1, [tuple(p) for p in M.content()["fronts"]["bulge"]["keys"][1][1]]),
            (H108 + 0.9, [tuple(p) for p in M.content()["fronts"]["bulge"]["keys"][0][1]])],
           width=8, side="germany", t_in=H108 - 0.1)
F107a, F107b = M107.fronts
F107a["t_out"] = H108 - 0.1
Z107 = band_zone(M107, F107a, 0)
M107.arrows("bulge_1944", P107 + 0.2, at(107, 0.62))
M107.arrows("patton_bastogne", H108 - 0.35, H108 + 0.55)
M107.zone("bastogne_ring", at(107, 0.62), at(107, 0.8), t_out=H108 + 0.35)
M107.city("Bastogne", at(107, 0.62))
M107.label("ARDENNES", at(107, 0.5), lonlat=(5.45, 49.75), size=34, color="ink")
M107.label("GERMANY", _g0, lonlat=(7.2, 50.6), size=46, color="cream")
M107.label("BELGIUM", _g0 + 0.3, lonlat=(4.5, 50.75), size=40, color="cream")
M107.label("FRANCE", _g0 + 0.6, lonlat=(4.6, 49.4), size=40, color="cream")


def shot_bulge(cr, t, a, b):
    collapsing = t >= H108 - 0.1
    Z107["f"] = F107b if collapsing else F107a
    update_band(Z107, t)
    M107.draw(cr, t)
    P.snowfall(cr, t, density=70, wind=60.0, seed=4, size=3.5, alpha=0.75)
    word_card(cr, t, SN(107, 1).start, "BATTLE OF THE BULGE", dur=SN(107, 1).end - SN(107, 1).start + 0.6,
              y=H * 0.16, size=100, color="axis")
    stamp(cr, t, H108 + 0.2, "FAILED", W * 0.36, H * 0.42, 130, "allies", -0.1)
    date_stamp(cr, t, "JAN 1945" if collapsing else "DEC 1944", start=a - 1)


# ================================================================ 109-109b: the Pacific, China and Burma
MPAC = Map("pacific", era="1942")
_p0 = CUT["pacific"]
B1, B2 = SN("109b", 0), SN("109b", 1)
MPAC.camera_key(_p0, (162.0, 13.0), 1.35)
MPAC.camera_key(L(109).end, (140.0, 20.0), 1.75)
MPAC.camera_key(B1.start + 1.2, (114.0, 30.0), 2.3)
MPAC.camera_key(B1.end, (112.0, 30.0), 2.45)
MPAC.camera_key(B2.start + 0.6, (96.0, 22.0), 3.6)
MPAC.camera_key(CUT["iwo"], (95.5, 21.5), 3.9)
_hop = at(109, 0.12)
_step = (at(109, 0.85) - _hop) / 5
MPAC.arrows("island_hop", _hop, _hop + _step * 0.9, stagger=_step)
MPAC.pins("island_hop", _hop - 0.15, stagger=_step)
MPAC.label("JAPAN", at(109, 0.8), lonlat=(139.0, 38.5), size=46, color="cream")
MPAC.front([(B1.start, [tuple(p) for p in M.content()["fronts"]["china"]["keys"][0][1]])], width=9, side="axis_jp",
           t_in=B1.start + 0.2)
MPAC.side("china", B1.start + 0.3, "china", origin=(104.0, 30.0), dur=1.2, occupied=False)
MPAC.label("CHINA", B1.start + 0.6, lonlat=(104.0, 32.5), size=62, color="ink")
MPAC.label("HOLDING SINCE 1937", B1.start + 2.2, lonlat=(104.0, 30.3), size=30, color="ink", font=LABEL)
MPAC.label("INDIA", B2.start, lonlat=(84.0, 23.5), size=46, color="cream")
MPAC.label("BURMA", B2.start + 0.5, lonlat=(97.8, 19.5), size=36, color="ink")
MPAC.arrows("burma_1944", B2.start + 0.4, B2.start + 1.7, stagger=0.7)


def shot_pacific(cr, t, a, b):
    MPAC.draw(cr, t)
    if t < B1.start:
        caption(cr, t, a + 0.3, "ISLAND HOPPING", 360, 220, 52, band="allies")
    date_stamp(cr, t, "1943-1944" if t < B1.start else "1944", start=a - 1)


# ================================================================ 110: Iwo Jima / Okinawa, then the generals
def _bars(cr, t, x, y, t0):
    u0 = back_out(seg(t, t0, t0 + 0.3))
    if u0 <= 0:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(u0, u0)
    P.rrect(cr, -250, -380, 520, 470, 8)
    P.fill_ink(cr, "paper", 5, tone=False)
    text(cr, "U.S. CASUALTIES", 10, -330, 40, font=STENCIL, color="ink", spacing=4)
    P.line(cr, -200, 20, 220, 20, 5)
    for i, (name, hgt, d) in enumerate((("IWO JIMA", 0.53, 0.3), ("OKINAWA", 1.0, 1.2))):
        g = ease_out(seg(t, t0 + d, t0 + d + 1.4))
        bx = -120 + i * 220
        P.rrect(cr, bx - 60, 20 - 270 * hgt * g, 120, 270 * hgt * g, 0)
        P.fill_ink(cr, "alert", 5)
        text(cr, name, bx, 62, 30, font=STENCIL, color="ink", spacing=3)
    cr.restore()


def shot_iwo(cr, t, a, b):
    hz = 660
    okinawa = t >= at(110, 0.2)
    cr.save()
    push(cr, t, a, b, 1.0, 1.07, W * 0.35, H * 0.55)
    S.Sky(mode="dusk", horizon=hz, clouds=2, seed=21).draw(cr, t)
    S.Ocean(horizon=hz).draw(cr, t)
    bursts = [a + 0.2 + k * 0.45 for k in range(30)]
    Th.Island(width=1100, color="#4b4a3c" if not okinawa else "#4a5040", bursts=bursts).draw(
        cr, t, x=W * 0.33, y=hz + 4, scale=0.82, seed=3 if okinawa else 1)
    for i, x in enumerate((1080, 1420)):
        P.Battleship(side="usa", silhouette="#55524a", water=None).draw(cr, t, x=x, y=hz + 40 + i * 50,
                                                                       scale=0.2 + i * 0.04, facing=-1,
                                                                       fire=[a + 0.5 + i * 0.7 + k * 1.6 for k in range(5)])
    cr.restore()
    _bars(cr, t, W - 380, 560, a + 0.7)
    caption(cr, t, a + 0.2, "OKINAWA" if okinawa else "IWO JIMA", 330, 220, 62, band="axis_jp" if False else "ink")
    date_stamp(cr, t, "APR 1945" if okinawa else "FEB 1945", start=a - 1)


GENERALS = [dict(x=560, f=1, pose=[(0, "arms_crossed")], s=1.15, seed=3),
            dict(x=960, f=-1, pose=[(0, dict(sh_n=0.75, el_n=1.1, lean=0.12, nod=0.25, hand_n="fist", turn=0.3)), (2.2, "shrug")],
                 s=1.22, seed=5),
            dict(x=1370, f=-1, pose=[(0, "head_down")], s=1.15, seed=7)]


def shot_generals(cr, t, a, b):
    cr.save()
    push(cr, t, a, b, 1.0, 1.08, W / 2, H * 0.5)
    S.SigningRoom(kind="office", horizon=640).draw(cr, t)
    for g in GENERALS:
        St.Figure(nation="usa", x=g["x"], y=1010, scale=g["s"], facing=g["f"], seed=g["seed"]).draw(
            cr, t - a, track=g["pose"], face={"brow": "worried", "mouth": "frown"})
    cr.save()
    cr.translate(0, 120)
    P.poly(cr, [(320, 770), (1600, 770), (1700, 900), (220, 900)])              # the map table
    P.fill_ink(cr, "#6a4b31", 6)
    cr.rectangle(220, 900, 1480, 200)
    P.fill_ink(cr, P.shade("#6a4b31", -0.3), 6)
    P.poly(cr, [(560, 785), (1360, 785), (1420, 880), (500, 880)])              # a map of Japan on it
    P.fill_ink(cr, "sea", 4, tone=False)
    isl = [(980, 800), (1010, 812), (990, 836), (960, 856), (920, 866), (890, 872), (900, 860), (940, 846),
           (965, 826)]
    P.poly(cr, isl)
    P.fill_ink(cr, "axis_jp", 3, tone=False)
    for k in range(3):
        u = ease_out(seg(t, a + 0.4 + k * 0.35, a + 1.2 + k * 0.35))
        x0, y0 = 640 + k * 90, 868
        P.line(cr, x0, y0, lerp(x0, 900 + k * 20, u), lerp(y0, 850 - k * 8, u), 6, "allies")
    cr.restore()
    cr.restore()
    word_card(cr, t, at(110, 0.68), "INVADE JAPAN?", dur=10, y=H * 0.17, size=104, color="ink")
    date_stamp(cr, t, "SUMMER 1945", start=a - 1)


# ================================================================ C7: chapter card, then Berlin
def shot_card7(cr, t, a, b):
    paper(cr)
    rays(cr, t, W / 2, H / 2, n=28, color="ink", alpha=0.10, spin=0.02)
    chapter_card(cr, t, C7[0], 7, T.chapter("C7").title, dur=C7[1] - C7[0] + 0.05)
    date_stamp(cr, t, "1945", start=a - 1)


M111 = Map("europe", era="1941",
           sides={"poland_w": "soviet", "poland_e": "soviet", "g37east": "soviet", "east_prussia": "soviet",
                  "rhineland": "allies", "france_occ": "allies", "france_north": "allies", "belgium": "allies",
                  "luxembourg": "allies", "hungary": "soviet", "romania": "soviet", "slovakia": "soviet"},
           occupied=set(_e41["occupied"]) | {"g37east", "east_prussia", "rhineland", "hungary", "slovakia"})
_k0 = CUT["berlin"]
M111.camera_key(_k0, (14.6, 52.4), 5.4)
M111.camera_key(CUT["bunker"], (13.6, 52.5), 7.4)
M111.arrows("berlin_1945", L(111).start + 0.1, at(111, 0.45), stagger=0.25)
M111.zone("berlin_ring", at(111, 0.35), at(111, 0.8))
M111.city("Berlin", _k0 + 0.2)
M111.label("GERMANY", _k0, lonlat=(10.6, 51.6), size=46, color="cream")


def shot_berlin(cr, t, a, b):
    M111.draw(cr, t)
    x, y = M111.screen(M111.xy((13.4, 52.5)))
    r = random.Random(int(t * 6))
    if t > at(111, 0.4):
        for k in range(3):
            s0 = at(111, 0.4) + k * 0.33
            age = (t - s0) % 1.0
            rr = random.Random(int((t - s0) // 1.0) * 7 + k)
            F.starburst(cr, x + rr.uniform(-70, 70), y + rr.uniform(-50, 50), age, size=0.32, seed=k)
    del r
    caption(cr, t, a + 0.3, "BERLIN", 300, 220, 58, band="soviet")
    date_stamp(cr, t, "APRIL 1945", start=a - 1)


# ================================================================ 112: the bunker door
def shot_bunker(cr, t, a, b):
    slam = L(112).start + 0.55 * (L(112).end - L(112).start)
    u = ease_in(seg(t, slam - 0.9, slam))
    cr.save()
    dx, dy = shake(t, slam, 0.4, 16)
    cr.translate(dx, dy)
    push(cr, t, a, b, 1.0, 1.1, W / 2, H * 0.46)
    S.BunkerCorridor(close=u).draw(cr, t)
    cr.restore()
    if t > slam:                                                         # the lamps dim after the slam: silence
        cr.save()
        cr.rectangle(0, 0, W, H)
        cr.set_source_rgba(*col("ink", 0.35 * ease_out(seg(t, slam + 0.2, slam + 1.6))))
        cr.fill()
        cr.restore()
    date_stamp(cr, t, "30 APRIL 1945", start=a - 1)


# ================================================================ 113: Reims
def shot_reims(cr, t, a, b):
    s0 = L(113).start
    cr.save()
    push(cr, t, a, b, 1.0, 1.07, W / 2, H * 0.6)
    S.SigningRoom(kind="office", horizon=600).draw(cr, t)
    for i, (x, nat, pose) in enumerate(((420, "usa", "stand"), (690, "britain", "stand"),
                                        (1260, "soviet", "stand"), (1520, "france", "stand"))):
        St.Figure(nation=nat, x=x, y=990, scale=0.95, facing=1 if x < W / 2 else -1, seed=i).draw(
            cr, t - a, track=[(0, pose)])
    St.Figure(nation="germany", x=W / 2 - 100, y=1050, scale=1.0, facing=1, seed=9, prop="pen").draw(
        cr, t - a, track=[(0, "stand"), (0.6, dict(lean=0.45, nod=0.4, sh_n=1.05, el_n=0.9, sh_f=0.6, el_f=0.8,
                                                    turn=0.2, face={"mouth": "line", "brow": "sad"}))])
    P.SigningTable().draw(cr, t, x=W / 2 + 60, y=1080, scale=1.7, signed=ease_out(seg(t, s0 + 0.2, s0 + 1.5)))
    cr.restore()
    stamp(cr, t, s0 + 1.35, "SURRENDER", W / 2, H * 0.2, 120, "alert", -0.06)
    caption(cr, t, a + 0.2, "REIMS", 260, 220, 48, band="ink")
    date_stamp(cr, t, "7 MAY 1945", start=a - 1)


# ================================================================ 114: V-E Day, London then Moscow
def _bunting(cr, t, y0, n=3):
    for j in range(n):
        y = y0 + j * 70
        pts = [(x, y + 40 * math.sin(math.pi * (x + 200) / (W + 400))) for x in range(-200, W + 240, 60)]
        P.poly(cr, pts, close=False)
        P.ink(cr, 3, "ink_soft")
        for i, (x, yy) in enumerate(pts):
            c = ("alert", "cream", "allies")[(i + j) % 3]
            sw = math.sin(t * 4 + i + j) * 3
            P.poly(cr, [(x - 14, yy), (x + 14, yy), (x + sw, yy + 30)])
            P.fill_ink(cr, c, 2, tone=False)


def shot_london(cr, t, a, b):
    cr.save()
    push(cr, t, a, b, 1.0, 1.07, W / 2, H * 0.5)
    S.Sky(mode="day", horizon=700, clouds=2, rays=True, seed=14).draw(cr, t)
    S.Skyline(city="london", ground=700, seed=3).draw(cr, t)
    _bunting(cr, t, 120)
    SP.cheering_crowd(cr, t, x0=-40, x1=W + 40, y0=680, y1=1090, n=52, scale=0.5, front=6, seed=21)
    cr.restore()
    word_card(cr, t, L(114).start + 0.5, "V-E DAY", dur=10, y=H * 0.3, size=180, color="allies")
    date_stamp(cr, t, "8 MAY 1945", start=a - 1)


def shot_moscow(cr, t, a, b):
    cr.save()
    push(cr, t, a, b, 1.0, 1.07, W / 2, H * 0.45)
    S.Sky(mode="night", horizon=740, clouds=2, seed=15).draw(cr, t)
    F.fireworks(cr, t, 200, W - 200, 120, 420, n=9, start=a - 0.6, every=0.32, seed=9,
                colors=("gold", "alert", "cream", "gold"))
    S.Skyline(city="moscow", ground=740, night=True, lit=0.6, seed=4).draw(cr, t)
    St.crowd(cr, t, 44, -40, W + 40, 760, 1080, scale=0.5, nation=None, pose="cheer", seed=6, tone="#1d1c22")
    cr.restore()
    caption(cr, t, a + 0.2, "MOSCOW", 300, 220, 56, band="soviet")
    date_stamp(cr, t, "9 MAY 1945", start=a - 1)


# ================================================================ 115-116: the quiet Pacific, the bomber, the flash
def shot_quiet(cr, t, a, b):
    hz = 640
    cr.save()
    push(cr, t, a, b, 1.0, 1.05, W * 0.6, H * 0.6)
    S.Sky(mode="dusk", horizon=hz, clouds=2, seed=30, drift=4.0).draw(cr, t)
    S.Ocean(horizon=hz, swell=0.3).draw(cr, t)
    P.Destroyer(side="usa", silhouette="#3e3d38", water=None).draw(cr, t, x=W * 0.64 + 12 * (t - a), y=hz + 6,
                                                                  scale=0.2, facing=1, speed=10)
    cr.restore()
    caption(cr, t, a + 0.25, "THE PACIFIC", 330, 220, 52, band="ink")
    date_stamp(cr, t, "SUMMER 1945", start=a - 1)


def shot_bomber(cr, t, a, b):
    cr.save()
    push(cr, t, a, b, 1.0, 1.05, W / 2, H * 0.45)
    paper(cr)
    S.bands(cr, -200, H, ("#b9c2c4", "#c6ccc8", "#d3d4c8", "#dfdcc8"))
    r = random.Random(116)
    for row, (y, sp, sz) in enumerate(((760, 60, 0.9), (860, 110, 1.1), (990, 180, 1.4))):
        for i in range(8):                                                     # cloud deck scrolls under the plane
            x = (i * 330 + r.uniform(0, 120) - (t - a) * sp) % (W + 700) - 350
            F.cloud(cr, x, y, 420 * sz, seed=row * 10 + i, color=P.mix("cream", "#c9c3a8", 0.2 * row), dense=1)
    P.Bomber(side="usa").draw(cr, t, x=W * 0.44 + 70 * (t - a), y=380 + 8 * math.sin(t * 0.9), scale=1.05,
                              engines=4)
    cr.restore()
    date_stamp(cr, t, "6 AUG 1945", start=a - 1)


def shot_flash(cr, t, a, b):
    hz = 790
    tf = a + 0.35
    cr.save()
    push(cr, t, a, b, 1.0, 1.04, W * 0.6, hz)
    paper(cr)
    S.bands(cr, -200, hz, ("#a8a49a", "#b8b3a4", "#c7c0ac", "#d3caae"))
    F.mushroom(cr, W * 0.6, hz, t, tf, size=0.62, seed=7, color="#c8c1ae", grow=4.0)
    for k, (y, c) in enumerate(((hz - 30, "#7d7a6c"), (hz - 8, "#5f5c52"))):   # far hills, then the near ridge
        pts = [(-200, H)] + [(x, y - 40 * math.sin(x * 0.004 + k * 2) - 25 * math.sin(x * 0.011 + k))
                             for x in range(-200, W + 240, 40)] + [(W + 200, H)]
        P.poly(cr, pts)
        P.fill_ink(cr, c, 4, tone=False)
    cr.rectangle(-200, hz + 60, W + 400, H)
    P.fill(cr, "#4b483f")
    cr.restore()
    if t >= tf:                                                                 # the distant flash, white
        g = 1 - ease_out(seg(t, tf + 0.1, tf + 1.6))
        if g > 0:
            cr.save()
            rg = cairo.RadialGradient(W * 0.6, hz - 40, 0, W * 0.6, hz - 40, 900)
            rg.add_color_stop_rgba(0, 1, 1, 0.97, 1.0 * g)
            rg.add_color_stop_rgba(0.35, 1, 1, 0.95, 0.7 * g)
            rg.add_color_stop_rgba(1, 1, 1, 0.95, 0.0)
            cr.set_source(rg)
            cr.paint()
            cr.restore()
        F.flash(cr, t, tf, hold=0.06, fade=0.9, color="white")
    caption(cr, t, tf + 1.2, "HIROSHIMA", W * 0.6, hz + 150, 50, band="ink")
    date_stamp(cr, t, "6 AUG 1945", start=a - 1)


SHOTS = dict(dday=shot_dday, normandy=shot_normandy, para=shot_para, omaha=shot_omaha, sunset=shot_sunset,
             bagration=shot_bagration, paris=shot_paris, bulge=shot_bulge, pacific=shot_pacific, iwo=shot_iwo,
             generals=shot_generals, card7=shot_card7, berlin=shot_berlin, bunker=shot_bunker, reims=shot_reims,
             london=shot_london, moscow=shot_moscow, quiet=shot_quiet, bomber=shot_bomber, flash=shot_flash)


def draw(cr, t):
    name = ORDER[0]
    for n in ORDER:
        if t >= CUT[n]:
            name = n
    a, b = span(name)
    cr.save()
    SHOTS[name](cr, t, a, b)
    cr.restore()
    print_finish(cr, t)


def cues(T=T):
    """[(episode_time, sfx_name, gain_db, pan)] for helper 7's mix."""
    c = []
    c += [(CUT["dday"] + 0.1, "page_whoosh", -6, 0), (SN(102, 1).start - 0.05, "stamp", -2, 0),
          (CUT["dday"], "sea_waves", -14, 0)]
    c += [(at(103, 0.5), "plane_drone", -12, -0.3), (CUT["para"], "plane_drone", -6, 0.2)]
    c += [(CUT["omaha"], "sea_waves", -10, -0.4)]
    c += [(CUT["omaha"] + s, "explosion", -9, (k - 2) * 0.3) for k, s in enumerate(BURSTS)]
    c += [(CUT["omaha"] + 0.2 + k * 0.6, "rifle_crack", -12, 0.3) for k in range(5)]
    c += [(CUT["sunset"], "sea_waves", -12, 0)]
    c += [(at(105, 0.18), "artillery_barrage", -6, 0.2), (at(105, 0.2), "tank", -9, 0.3),
          (HIT105, "explosion", -4, 0), (at(105, 0.8), "stamp", -3, 0)]
    c += [(CUT["paris"], "crowd_cheer", -6, 0)]
    c += [(P107, "tank", -8, 0.3), (CUT["bulge"], "blizzard", -14, 0), (H108 + 0.2, "stamp", -3, 0)]
    c += [(_hop + k * _step, "page_whoosh", -12, -0.5 + k * 0.25) for k in range(5)]
    c += [(B1.start + 0.3, "artillery", -14, -0.3), (B2.start + 0.4, "page_whoosh", -10, -0.4)]
    c += [(CUT["iwo"] + 0.2 + k * 0.45, "gun_boom", -12, -0.2 + (k % 3) * 0.2) for k in range(0, 10, 2)]
    c += [(CUT["generals"], "clock_tick", -16, 0)]
    c += [(C7[0], "page_whoosh", -4, 0)]
    c += [(CUT["berlin"], "artillery_barrage", -8, 0)]
    slam = L(112).start + 0.55 * (L(112).end - L(112).start)
    c += [(slam, "door_slam", -2, 0)]
    c += [(L(113).start + 0.2, "typewriter", -18, 0), (L(113).start + 1.35, "stamp", -3, 0)]
    c += [(CUT["london"], "crowd_cheer", -4, 0), (CUT["moscow"], "crowd_cheer", -8, 0)]
    c += [(CUT["moscow"] + k * 0.32, "gun_boom", -18, -0.6 + (k % 5) * 0.3) for k in range(6)]
    c += [(CUT["quiet"], "sea_waves", -12, 0)]
    c += [(CUT["bomber"], "plane_drone", -6, 0)]
    c += [(CUT["flash"] + 0.35, "explosion", -6, 0)]
    return sorted(c)
