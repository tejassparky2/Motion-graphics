"""WW2 Episode 1, package P6 (helper 4): script lines 87-101 (SHOTLIST.md C4-S16 .. C6-S06), on the episode clock.

    87  Germany retreating in the east       Europe map, the occupied east, grey arrows turn back west (1943)
    88  Kursk                                the Kursk salient on the map, then a poster tank battle on the steppe
    89  U-boats starve Britain               dusk Atlantic: a convoy on the horizon, a periscope, a torpedo wake, a hit
    90  Bletchley Park, Turing, the Poles    the Bletchley hut: the Polish Cipher Bureau's 1932 file, the bombe, Enigma
    91  the U-boats are losing               an escort and a patrol bomber; depth charges; the U-BOATS LOST bar climbs
    C5  chapter card                         a sober black card (no red band, no rays, no fanfare)
    92-97 THE HOLOCAUST                      a muted grey map, text on black, ghetto and camp pins, the rail lines,
                                             6,000,000 and the other victim groups as text, a single candle.
                                             No figures, no rays, no colour; slow fades; the silences are held.
    C6  chapter card                         the standard poster card
    98  Sicily                               the Mediterranean map: the Allied landing arrows (July 1943)
    99  Mussolini overthrown, Italy out      his poster bust topples off its plinth; Italy splits on the map (Sept 1943)
    100 Germany fights on in Italy           the Gustav Line holds across Italy (1944)
    101 the biggest invasion from the sea    the Channel horizon fills with ships, planes overhead (June 1944)

Every time comes from Timing() (line starts/ends, chapter cards), never hard-coded seconds, so the package re-times
itself when the voiced timing.json lands. Sound: cues() (SFX only; the score's low tone for chapter 5 is helper 7's).

    python channels/ww2/ep01/render_pkg.py P6 --sheet | --still T | (final)
"""
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from channels.ww2.kit.core import (H, LABEL, SLAB, STENCIL, TITLE, UI, W, back_out, chapter_card, clamp01, col,  # noqa: E402
                                   date_stamp, ease_in, ease_out, halftone, lerp, paper, print_finish, push_in, rays,
                                   seg, shake, smooth, text)
from channels.ww2.kit import props as P  # noqa: E402
from channels.ww2.kit import things as TH  # noqa: E402
from channels.ww2.kit import sets as SE  # noqa: E402
from channels.ww2.kit import fx as FX  # noqa: E402
from channels.ww2.kit import heads as HD  # noqa: E402
from channels.ww2.kit.maps import Map, _poly_path  # noqa: E402
from channels.ww2.kit.map_content import KURSK_AUG_1943, KURSK_JUL_1943  # noqa: E402
from channels.ww2.ep01.timing import Timing, package_span  # noqa: E402

T = Timing()
A, B = package_span("P6", T)
C5 = T.chapter("C5").card
C6 = T.chapter("C6").card


def L(n):
    return T.line(str(n))


def _shots():
    """{line id: (t0, t1)}: each line's shot runs from the midpoint of the pause before it to the midpoint of the
    pause after it; a chapter card takes the pause before the first line of its chapter."""
    ids = [str(i) for i in range(87, 102)]
    out, start = {}, A
    for i, n in enumerate(ids):
        if n == "92":
            start = C5[1]
        if n == "98":
            start = C6[1]
        if i + 1 < len(ids):
            nxt = ids[i + 1]
            end = C5[0] if nxt == "92" else C6[0] if nxt == "98" else (L(n).end + L(nxt).start) / 2
        else:
            end = B
        out[n] = (start, end)
        start = end
    return out


S = _shots()


def at(n, u):
    """A time u (0..1) of the way through line n's speech (words are spread evenly, so this tracks phrases)."""
    ln = L(n)
    return ln.start + u * (ln.end - ln.start)


def zoomed(cr, t, t0, t1, z1=1.06, fx=W / 2, fy=H / 2):
    """Apply the shot's slow push-in about (fx, fy)."""
    z = push_in(t, t0, t1, 1.0, z1)
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)


def fade_black(cr, a):
    if a > 0:
        cr.set_source_rgba(*col("ink", min(1.0, a)))
        cr.paint()


# ============================================================================================ 87: retreat in the east
def _map_east():
    t0, t1 = S["87"]
    m = Map("europe", era="1941")
    m.zone("ussr_occupied_1942", t0 - 5)
    m.view("east_front", t0)
    m.camera_key(t1, (30.0, 51.5), 1.45)
    m.label("EASTERN FRONT", t0 + 0.2, lonlat=(33.0, 56.8), size=46)
    m.arrows("reverse_1943", at("87", 0.35), at("87", 0.95), side="germany")
    m.stamp("RETREAT", (27.5, 49.6), at("87", 0.75), size=70, color="ink")
    return m


M87 = _map_east()


def shot_87(cr, t):
    M87.draw(cr, t)
    date_stamp(cr, t, "1943", start=S["87"][0])


# ============================================================================================ 88: Kursk
_NORTH = [(22.0, 60.5), (30.0, 59.6), (30.6, 57.5), (32.2, 55.8)]
_SOUTH = [(38.6, 47.6), (38.5, 46.0), (34.0, 45.0), (22.0, 44.0)]


def held_zone(m, line, t0, t1, t_out=None):
    """The German-held east behind a front line (lon/lat), hatched like the map's occupied bands."""
    geom = [m.xy(p) for p in _NORTH + line + _SOUTH]
    m.zones.append(dict(kind="occupied", side="germany", geom=geom, t0=t0, t1=t1, t_out=t_out,
                        path=_poly_path([geom + [geom[0]]])))


def _map_kursk():
    t0 = S["88"][0]
    jul = [(34.3, 54.5)] + KURSK_JUL_1943 + [(38.0, 48.8)]
    aug = [(33.2, 54.6)] + KURSK_AUG_1943
    ca, cb = at("88", 0.3), at("88", 0.45)
    m = Map("europe", era="1941")
    m.view("kursk", t0, 2.6)
    m.camera_key(cb, (36.2, 51.6), 3.2)
    held_zone(m, jul, t0 - 5, t0 - 4.4, t_out=cb - 0.3)
    held_zone(m, aug, cb - 0.4, cb)
    m.front([(t0, KURSK_JUL_1943), (ca, KURSK_JUL_1943), (cb, KURSK_AUG_1943)], width=8)
    m.arrows("kursk_1943", t0 + 0.25, ca, side="germany")
    m.arrows("kursk_counter", ca + 0.05, cb, side="soviet")
    m.city("KURSK", t0 + 0.4, lonlat=(36.19, 51.73))
    m.label("THE KURSK BULGE", t0 + 0.6, lonlat=(40.6, 52.0), size=44)
    return m


M88 = _map_kursk()
TANKS_DE = [P.Tank(x=0, y=0, scale=s, facing=1, side="germany", seed=i) for i, s in enumerate((0.42, 0.62, 0.95))]
TANKS_SU = [P.Tank(x=0, y=0, scale=s, facing=-1, side="soviet", seed=10 + i) for i, s in enumerate((0.4, 0.6, 0.9))]


def steppe(cr, t, hz=610, dusk=False):
    """The open steppe as a poster: a khaki sky with slow ink rays, a flat horizon, two tones of ground."""
    paper(cr)
    SE.bands(cr, -200, hz, SE.SKIES["dusk" if dusk else "day"])
    rays(cr, t, W * 0.62, hz, n=26, color="khaki", alpha=0.18, spin=0.01)
    cr.rectangle(-200, hz, W + 400, H - hz + 200)
    cr.set_source_rgba(*col("#9a8a5c"))
    cr.fill()
    cr.rectangle(-200, hz + 120, W + 400, H)
    cr.set_source_rgba(*col("#8a7a4e"))
    cr.fill()
    halftone(cr, lambda c: c.rectangle(-200, hz + 180, W + 400, H), "ink", density=2, alpha=0.18)
    P.line(cr, -200, hz, W + 200, hz, 5)


def shot_88(cr, t):
    t0, t1 = S["88"]
    split = at("88", 0.47)
    if t < split:
        M88.draw(cr, t)
        date_stamp(cr, t, "JULY 1943", start=t0)
        return
    cr.save()
    dx, dy = shake(t, at("88", 0.62), 0.3, 10) if t > at("88", 0.62) else (0, 0)
    cr.translate(dx, dy)
    zoomed(cr, t, split, t1, 1.07, W * 0.52, 700)
    hz = 600
    steppe(cr, t, hz)
    u = seg(t, split, t1)
    rows = [(hz + 70, 0), (hz + 190, 1), (hz + 380, 2)]
    for (y, k) in rows:
        de, su = TANKS_DE[k], TANKS_SU[k]
        sp = 40 + 60 * k
        fires_de = [split + 0.6 + 0.9 * k, split + 2.0 + 0.5 * k]
        fires_su = [split + 0.9 + 0.8 * k, split + 2.4 + 0.4 * k]
        de.draw(cr, t, x=lerp(260 - 120 * k, 520 - 60 * k, u), y=y, speed=sp, turret=0, fire=fires_de, elev=3)
        su.draw(cr, t, x=lerp(1660 + 120 * k, 1400 + 60 * k, u), y=y, speed=sp, turret=0, fire=fires_su, elev=3)
        for j, ft in enumerate(fires_de + fires_su):                  # shells land between the lines
            if t >= ft + 0.25:
                xx = 960 + (-1) ** j * (120 + 90 * k) + 40 * math.sin(ft * 7)
                FX.starburst(cr, xx, y - 10, t - ft - 0.25, size=0.55 + 0.25 * k, seed=j + 5 * k)
                FX.puff(cr, xx, y - 10, t - ft - 0.25, size=0.8 + 0.4 * k, seed=j + 7 * k)
    cr.restore()
    text(cr, "KURSK", W / 2, 170, 120, font=SLAB, color="cream", bold=False, outline="ink", outline_w=12,
         alpha=ease_out(seg(t, split + 0.15, split + 0.5)), spacing=4)
    text(cr, "ONE OF THE BIGGEST TANK BATTLES IN HISTORY", W / 2, 235, 34, font=STENCIL, color="ink",
         alpha=ease_out(seg(t, split + 0.6, split + 1.0)), spacing=4)
    v = back_out(seg(t, at("88", 0.86), at("88", 0.86) + 0.3))
    if v > 0:
        cr.save()
        cr.translate(W / 2, 470)
        cr.rotate(-0.08)
        cr.scale(1.6 - 0.6 * v, 1.6 - 0.6 * v)
        text(cr, "SOVIET VICTORY", 0, 0, 74, font=STENCIL, color="soviet", outline="paper", outline_w=6,
             alpha=min(1.0, v), spacing=6)
        cr.restore()
    date_stamp(cr, t, "JULY 1943", start=split)


# ============================================================================================ 89: the U-boats
def freighter(cr, x, y, s, t, list_=0.0, sink=0.0, seed=0, color="#4f4a44"):
    """A merchant ship in flat poster silhouette (bow right): hull, bridge, funnel, two masts with derricks.
    list_ rolls it, sink 0..1 lowers it under the waterline (clipped)."""
    r = random.Random(seed)
    bob = math.sin(t * 1.3 + seed) * 2.0
    cr.save()
    cr.rectangle(x - 400 * s, y - 400 * s, 800 * s, 400 * s + 4)              # nothing below the waterline
    cr.clip()
    cr.translate(x, y + bob + sink * 120 * s)
    cr.rotate(list_)
    cr.scale(s, s)
    P.poly(cr, [(-260, -6), (250, -6), (280, -48), (180, -44), (-230, -44), (-268, -40)])
    P.fill_ink(cr, color, 5)
    for mx in (-150, 120):
        P.line(cr, mx, -44, mx, -150, 6)
        P.line(cr, mx, -120, mx + 70, -60, 3)
    P.rrect(cr, -40, -100, 110, 58, 4)
    P.fill_ink(cr, P.shade(color, 0.15), 4)
    P.rrect(cr, 0, -140, 34, 42, 3)
    P.fill_ink(cr, "#2d2a27", 4)
    if r.random() < 0.5:
        P.rrect(cr, -230, -70, 70, 26, 3)
        P.fill_ink(cr, "khaki", 3)
    cr.restore()


SUB = P.Periscope(x=0, y=0, scale=1.0, facing=-1, side="germany", water=None)


def shot_89(cr, t):
    t0, t1 = S["89"]
    hit = at("89", 0.62)
    cr.save()
    dx, dy = shake(t, hit, 0.35, 8)
    cr.translate(dx, dy)
    zoomed(cr, t, t0, t1, 1.07, W * 0.6, 640)
    hz = 600
    paper(cr)
    SE.Sky(mode="dusk", horizon=hz, clouds=4, seed=5).draw(cr, t)
    SE.Ocean(horizon=hz, mode="day").draw(cr, t)
    convoy = [(520, 0.6, 0), (930, 0.72, 1), (1330, 0.66, 2), (1720, 0.58, 3)]
    for i, (x, s, sd) in enumerate(convoy):
        xx = x - 18 * (t - t0)
        if i == 2:
            k = seg(t, hit, t1 + 2)
            freighter(cr, xx, hz + 18, s, t, list_=-0.18 * ease_out(k), sink=0.5 * k, seed=sd)
            if t >= hit:
                P.explosion(cr, xx + 20, hz + 4, t - hit, size=0.9, seed=4)
                P.smoke(cr, xx - 10, hz - 10, t - hit, height=360, width=80, color="#3b3631", alpha=0.9, wind=0.5)
        else:
            freighter(cr, xx, hz + 14 + 4 * (i % 2), s, t, seed=sd)
    torp = seg(t, at("89", 0.3), hit)                                            # the torpedo wake runs out
    if 0 < torp:
        x0, y0, x1, y1 = 520, 980, 1230, hz + 22
        xe, ye = lerp(x0, x1, torp), lerp(y0, y1, torp)
        cr.set_source_rgba(*col("cream", 0.85 * (1 - seg(t, hit, hit + 1.5))))
        cr.set_line_width(lerp(14, 4, torp))
        cr.move_to(x0, y0)
        cr.line_to(xe, ye)
        cr.stroke()
    rise = ease_out(seg(t, t0 + 0.2, t0 + 1.2))
    SUB.draw(cr, t, x=420, y=lerp(1180, 1000, rise), scale=1.7, scope_turn=0.3 * seg(t, t0 + 1.0, at("89", 0.3)),
             speed=20)
    cr.restore()
    text(cr, "U-BOATS", W / 2, 190, 118, font=SLAB, color="cream", bold=False, outline="ink", outline_w=12,
         alpha=ease_out(seg(t, at("89", 0.08), at("89", 0.2))), spacing=4)
    text(cr, "THE BATTLE OF THE ATLANTIC", W / 2, 252, 34, font=STENCIL, color="ink",
         alpha=ease_out(seg(t, at("89", 0.2), at("89", 0.32))), spacing=4)
    date_stamp(cr, t, "1942", start=t0)


# ============================================================================================ 90: Bletchley Park
BOMBE = TH.Bombe(x=1480, y=910, scale=0.95)
ENIGMA = P.Enigma(x=640, y=1000, scale=1.15)
PAPERS = TH.Papers(x=1020, y=930, scale=0.9)


def polish_file(cr, t, t0, x, y):
    """The Polish Cipher Bureau's file slides in: a buff folder stamped WARSAW 1932 / 1939, three names."""
    u = back_out(seg(t, t0, t0 + 0.45))
    if u <= 0:
        return
    cr.save()
    cr.translate(lerp(x - 500, x, u), y)
    cr.rotate(-0.06)
    P.rrect(cr, -250, -170, 500, 340, 10)
    P.fill_ink(cr, "#d8c08a", 6)
    P.rrect(cr, -250, -200, 170, 40, 8)
    P.fill_ink(cr, "#d8c08a", 5)
    text(cr, "POLISH CIPHER BUREAU", 0, -110, 40, font=STENCIL, color="ink", spacing=3)
    text(cr, "ENIGMA BROKEN 1932", 0, -58, 34, font=LABEL, color="ink_soft")
    for i, nm in enumerate(("REJEWSKI", "RÓŻYCKI", "ZYGALSKI")):
        text(cr, nm, 0, 4 + i * 44, 34, font=TITLE, color="ink", bold=False, spacing=2,
             alpha=ease_out(seg(t, t0 + 0.4 + 0.18 * i, t0 + 0.7 + 0.18 * i)))
    a = back_out(seg(t, t0 + 1.1, t0 + 1.35))
    if a > 0:
        cr.save()
        cr.translate(120, 120)
        cr.rotate(-0.22)
        cr.scale(1.8 - 0.8 * a, 1.8 - 0.8 * a)
        text(cr, "SHARED WITH BRITAIN · JULY 1939", 0, 0, 26, font=STENCIL, color="alert", spacing=2,
             alpha=min(1, a))
        cr.restore()
    cr.restore()


def shot_90(cr, t):
    t0, t1 = S["90"]
    cr.save()
    zoomed(cr, t, t0, t1, 1.06, W * 0.5, 760)
    paper(cr)
    SE.BletchleyHut(horizon=700).draw(cr, t)
    crack = at("90", 0.82)
    BOMBE.draw(cr, t, run=1.0 - 0.0 * (t > crack), stop_at=crack)
    lit = None
    ENIGMA.draw(cr, t, auto=t < crack, lit=lit)
    PAPERS.draw(cr, t, circle=ease_out(seg(t, crack, crack + 0.6)), word=7)
    cr.restore()
    # "including Alan Turing": a name card at the bombe
    a = ease_out(seg(t, at("90", 0.2), at("90", 0.3))) * (1 - ease_in(seg(t, at("90", 0.42), at("90", 0.48))))
    if a > 0:
        P.rrect(cr, 1250, 300, 470, 96, 8)
        P.fill(cr, "ink", 0.85 * a)
        text(cr, "ALAN TURING", 1485, 365, 54, font=TITLE, color="cream", bold=False, alpha=a, spacing=3)
    # "building on the work of Polish codebreakers": the Polish file
    pf = at("90", 0.42)
    if t >= pf:
        out = 1 - ease_in(seg(t, at("90", 0.78), at("90", 0.84)))
        cr.save()
        cr.push_group()
        polish_file(cr, t, pf, 700, 430)
        cr.pop_group_to_source()
        cr.paint_with_alpha(out)
        cr.restore()
    # "crack the German Enigma cipher": the scrambled groups click into plain words
    if t >= crack:
        u = seg(t, crack, crack + 0.9)
        msg = "U-BOATS GATHER  GRID AK 52"
        rnd = random.Random(int(t * 12))
        shown = "".join(c if (i / len(msg) < u or c == " ") else chr(65 + rnd.randrange(26)) for i, c in enumerate(msg))
        P.rrect(cr, 440, 150, 1040, 110, 8)
        P.fill(cr, "paper", 0.95)
        P.ink(cr, 5)
        text(cr, shown, W / 2, 228, 64, font=STENCIL, color="ink" if u >= 1 else "alert", spacing=4)
    text(cr, "BLETCHLEY PARK", 360, 640, 40, font=STENCIL, color="cream", spacing=5,
         alpha=ease_out(seg(t, t0 + 0.2, t0 + 0.6)) * (1 - ease_in(seg(t, at("90", 0.4), at("90", 0.45)))))
    date_stamp(cr, t, "1940-1943", start=t0)


# ============================================================================================ 91: the U-boats lose
DD = P.Destroyer(x=0, y=0, scale=0.9, facing=-1, side="britain")
PATROL = P.Bomber(x=0, y=0, scale=0.55, facing=-1, side="britain")
SUB2 = P.Submarine(x=0, y=0, scale=0.75, facing=1, side="germany")


def shot_91(cr, t):
    t0, t1 = S["91"]
    cr.save()
    zoomed(cr, t, t0, t1, 1.06, W * 0.5, 620)
    hz = 560
    paper(cr)
    SE.Sky(mode="day", horizon=hz, clouds=5, seed=9).draw(cr, t)
    SE.Ocean(horizon=hz, mode="day").draw(cr, t)
    u = seg(t, t0, t1)
    DD.draw(cr, t, x=lerp(1640, 1320, u), y=hz + 130, speed=160)
    SUB2.draw(cr, t, x=lerp(900, 980, u), y=hz + 300, depth=ease_in(seg(t, t0 + 0.3, t0 + 1.8)), periscope=False)
    PATROL.draw(cr, t, x=lerp(1900, 300, seg(t, t0, t0 + 3.2)), y=230, speed=200)
    for j in range(4):                                                         # depth charges: water columns
        dt = t0 + 1.4 + 0.45 * j
        if t >= dt:
            age = t - dt
            x = 1000 + 110 * j
            hgt = 260 * ease_out(clamp01(age / 0.5)) * (1 - ease_in(clamp01((age - 0.6) / 1.2)))
            if hgt > 2:
                P.poly(cr, [(x - 40, hz + 220), (x - 14, hz + 220 - hgt), (x + 14, hz + 220 - hgt * 0.9),
                            (x + 40, hz + 220)])
                P.fill_ink(cr, "cream", 4)
    cr.restore()
    # the score bar: U-BOATS LOST climbs past SHIPS SUNK (no numbers: shapes only)
    bx, by = 90, 1010
    lost = ease_out(seg(t, at("91", 0.2), at("91", 0.9)))
    sunk = 1 - 0.55 * ease_out(seg(t, at("91", 0.2), at("91", 0.9)))
    P.rrect(cr, bx - 30, by - 330, 560, 380, 10)
    P.fill(cr, "paper", 0.92)
    P.ink(cr, 5)
    for i, (lab, v, c) in enumerate((("SHIPS SUNK", sunk, "allies"), ("U-BOATS LOST", lost, "axis"))):
        x = bx + 40 + i * 260
        hh = 230 * v
        P.rrect(cr, x, by - 40 - hh, 160, hh, 3)
        P.fill_ink(cr, c, 5)
        text(cr, lab, x + 80, by + 6, 30, font=STENCIL, color="ink", spacing=2)
    text(cr, "BLACK MAY", W / 2, 180, 110, font=SLAB, color="cream", bold=False, outline="ink", outline_w=11,
         alpha=ease_out(seg(t, at("91", 0.45), at("91", 0.6))), spacing=4)
    date_stamp(cr, t, "MAY 1943", start=t0)


# ============================================================================================ C5: the Holocaust card
def card_c5(cr, t):
    a0, a1 = C5
    fade_black(cr, 1.0)
    a = ease_out(seg(t, a0 + 0.3, a0 + 1.0)) * (1 - ease_in(seg(t, a1 - 0.5, a1)))
    text(cr, "CHAPTER 5", W / 2, H / 2 - 50, 44, font=STENCIL, color="cream", alpha=0.7 * a, spacing=8)
    text(cr, "THE HOLOCAUST", W / 2, H / 2 + 60, 104, font=SLAB, color="cream", bold=False, alpha=a, spacing=4)


# ============================================================================================ 92-97: the Holocaust
def _map_holo():
    t92, t94 = S["92"][0], S["94"][0]
    m = Map("europe", era="1941", muted=1.0, compass=False)
    m.zone("ussr_occupied_1942", t92 - 5)
    m.camera_key(t92, (17.5, 51.0), 1.35)
    m.camera_key(S["92"][1], (18.0, 51.0), 1.45)
    m.camera_key(t94, (20.0, 51.0), 1.75)
    m.camera_key(S["94"][1], (20.0, 50.8), 1.9)
    m.pins("ghettos", at("94", 0.05), stagger=0.18)
    m.label("MASS SHOOTINGS", at("94", 0.38), lonlat=(30.5, 50.2), size=40, color="ink")
    m.line("rails_holocaust", at("94", 0.55), at("94", 0.95))
    m.pins("camps", at("94", 0.7), stagger=0.12)
    return m


MHOLO = _map_holo()


def shot_92(cr, t):
    t0, t1 = S["92"]
    MHOLO.draw(cr, t)
    cr.set_source_rgba(*col("ink", 0.35))
    cr.paint()
    fade_black(cr, 1 - ease_out(seg(t, t0, t0 + 2.0)))
    fade_black(cr, ease_in(seg(t, t1 - 0.6, t1)))
    if t > t0 + 1.0:
        date_stamp(cr, t, "1941-1945", start=t0 + 1.0)


def shot_93(cr, t):
    t0, t1 = S["93"]
    fade_black(cr, 1.0)
    s0, s1 = T.sentence("93", 0), T.sentence("93", 1)
    a0 = ease_out(seg(t, s0.start - 0.2, s0.start + 0.6))
    text(cr, "Nazi Germany and its collaborators", W / 2, H / 2 - 120, 60, font=SLAB, color="cream", bold=False,
         alpha=a0)
    text(cr, "are carrying out the Holocaust.", W / 2, H / 2 - 40, 60, font=SLAB, color="cream", bold=False, alpha=a0)
    a1 = ease_out(seg(t, s1.start - 0.1, s1.start + 0.7))
    text(cr, "A plan to murder every Jewish person in Europe.", W / 2, H / 2 + 90, 46, font=LABEL, color="cream",
         alpha=a1 * 0.92)


def shot_94(cr, t):
    t0, t1 = S["94"]
    MHOLO.draw(cr, t)
    cr.set_source_rgba(*col("ink", 0.25))
    cr.paint()
    fade_black(cr, 1 - ease_out(seg(t, t0, t0 + 0.8)))
    fade_black(cr, ease_in(seg(t, t1 - 0.5, t1)))
    lab = [("GHETTOS", at("94", 0.05), at("94", 0.36)), ("DEPORTATION TO DEATH CAMPS", at("94", 0.55), t1)]
    for s, a, b in lab:
        al = ease_out(seg(t, a, a + 0.4)) * (1 - ease_in(seg(t, b - 0.3, b)))
        if al > 0:
            text(cr, s, W / 2, 990, 46, font=STENCIL, color="cream", alpha=al, spacing=6)
    date_stamp(cr, t, "1941-1945", start=t0)


def shot_95(cr, t):
    t0, t1 = S["95"]
    fade_black(cr, 1.0)
    a = ease_out(seg(t, L("95").start - 0.1, L("95").start + 1.2))
    text(cr, "6,000,000", W / 2, H / 2 + 40, 230, font=TITLE, color="cream", bold=False, alpha=a, spacing=6)
    a2 = ease_out(seg(t, at("95", 0.4), at("95", 0.8)))
    text(cr, "JEWISH MEN, WOMEN AND CHILDREN", W / 2, H / 2 + 150, 44, font=STENCIL, color="cream", alpha=a2 * 0.8,
         spacing=6)


def shot_96(cr, t):
    t0, t1 = S["96"]
    fade_black(cr, 1.0)
    text(cr, "6,000,000", W / 2, 250, 120, font=TITLE, color="cream", bold=False, alpha=0.35, spacing=4)
    a = ease_out(seg(t, L("96").start - 0.1, at("96", 0.25)))
    text(cr, "AND MILLIONS OF OTHERS, INCLUDING", W / 2, 400, 40, font=STENCIL, color="cream", alpha=0.75 * a,
         spacing=5)
    groups = ("ROMA AND SINTI", "DISABLED PEOPLE", "POLISH CIVILIANS", "SOVIET PRISONERS OF WAR")
    for i, g in enumerate(groups):
        ga = ease_out(seg(t, at("96", 0.3 + 0.16 * i), at("96", 0.3 + 0.16 * i) + 0.6))
        text(cr, g, W / 2, 520 + i * 95, 64, font=SLAB, color="cream", bold=False, alpha=ga)


CANDLE = P.Candle(x=W / 2, y=760, scale=1.6)


def shot_97(cr, t):
    """The candle: held through the line and the silence after it, fading to black before the chapter 6 card."""
    t0, t1 = S["97"]
    fade_black(cr, 1.0)
    a = ease_out(seg(t, t0, t0 + 1.2)) * (1 - ease_in(seg(t, t1 - 1.0, t1)))
    if a > 0:
        cr.push_group()
        CANDLE.draw(cr, t, burn=0.2 * seg(t, t0, t1))
        cr.pop_group_to_source()
        cr.paint_with_alpha(a)
    a2 = ease_out(seg(t, at("97", 0.1), at("97", 0.6))) * (1 - ease_in(seg(t, t1 - 1.0, t1)))
    text(cr, "ONE OF THE WORST CRIMES IN HUMAN HISTORY", W / 2, 950, 38, font=STENCIL, color="cream",
         alpha=0.7 * a2, spacing=6)


# ============================================================================================ C6 card
def card_c6(cr, t):
    paper(cr)
    rays(cr, t, W / 2, H / 2, n=28, color="khaki", alpha=0.25, spin=0.02)
    chapter_card(cr, t, C6[0], 6, "Closing in", dur=C6[1] - C6[0])


# ============================================================================================ 98: Sicily
def _map_sicily():
    t0, t1 = S["98"]
    m = Map("europe", era="1941", sides={"libya": "allies", "tunisia": "allies", "algeria": "allies",
                                          "morocco": "allies", "egypt": "allies"})
    m.view("italy", t0, 2.3)
    m.camera_key(t1, (14.0, 38.4), 3.6)
    m.arrows("sicily_1943", at("98", 0.15), at("98", 0.75), side="allies")
    m.label("SICILY", at("98", 0.6), lonlat=(14.1, 37.55), size=44)
    m.label("ITALY", t0 + 0.2, lonlat=(13.4, 42.5), size=52)
    return m


M98 = _map_sicily()


def shot_98(cr, t):
    M98.draw(cr, t)
    date_stamp(cr, t, "JULY 1943", start=S["98"][0])


# ============================================================================================ 99: Mussolini falls
PLINTH = TH.Pedestal(x=W * 0.42, y=1000, scale=1.5)


def _map_italy_out():
    t1 = S["99"][1]
    m = Map("europe", era="1941", sides={"libya": "allies", "tunisia": "allies", "sicily": "allies"})
    sw = at("99", 0.52)
    m.view("italy", sw, 2.5)
    m.camera_key(t1, (13.5, 41.5), 2.75)
    m.side("italy_south", at("99", 0.62), "allies", origin=(16.0, 38.5), dur=1.0, occupied=False)
    m.side("italy", at("99", 0.75), "germany", origin=(11.5, 46.0), dur=1.2, occupied=True)
    m.stamp("ITALY SURRENDERS", (14.5, 40.2), at("99", 0.8), size=56)
    return m


M99 = _map_italy_out()


def shot_99(cr, t):
    t0, t1 = S["99"]
    sw = at("99", 0.52)
    if t >= sw:
        M99.draw(cr, t)
        date_stamp(cr, t, "SEPT 1943", start=sw)
        return
    cr.save()
    zoomed(cr, t, t0, sw, 1.05, W * 0.45, 600)
    paper(cr)
    rays(cr, t, W * 0.42, 420, n=26, color="khaki", alpha=0.3, spin=0.02)
    fall = seg(t, at("99", 0.18), at("99", 0.42))
    crack = ease_out(seg(t, at("99", 0.12), at("99", 0.2)))
    PLINTH.draw(cr, t, crack=crack)
    cr.save()
    base_x, base_y = W * 0.42, 1000 - 300 * 1.5 * 0.86
    cr.translate(base_x + 260 * ease_in(fall), base_y + 520 * ease_in(fall) ** 2)
    cr.rotate(1.1 * ease_in(fall))
    HD.portrait(cr, t, "mussolini", 0, 0, height=560, expr="shocked" if fall > 0 else "smug", turn=0.45)
    cr.restore()
    cr.restore()
    text(cr, "MUSSOLINI OVERTHROWN", W * 0.7, 300, 70, font=SLAB, color="ink", bold=False, outline="paper",
         outline_w=7, alpha=ease_out(seg(t, at("99", 0.2), at("99", 0.32))), spacing=2)
    text(cr, "25 JULY 1943", W * 0.7, 370, 40, font=STENCIL, color="alert",
         alpha=ease_out(seg(t, at("99", 0.28), at("99", 0.38))), spacing=5)
    date_stamp(cr, t, "JULY 1943", start=t0)


# ============================================================================================ 100: Italy fights on
def _map_gustav():
    t0, t1 = S["100"]
    m = Map("europe", era="1941", sides={"sicily": "allies", "italy_south": "allies", "tunisia": "allies"},
            occupied=["italy"])
    m.sides = None
    m.side("italy", t0 - 5, "germany", occupied=True)
    m.view("italy", t0, 2.6)
    m.camera_key(t1, (14.0, 41.7), 3.6)
    m.line("gustav", at("100", 0.15), at("100", 0.6))
    m.label("GUSTAV LINE", at("100", 0.5), lonlat=(13.9, 42.35), size=40)
    m.arrows("salerno_1943", t0 + 0.1, at("100", 0.3), side="allies")
    m.stamp("FIGHTING ON · 1943-1945", (12.4, 43.3), at("100", 0.75), size=48, color="ink")
    return m


M100 = _map_gustav()


def shot_100(cr, t):
    M100.draw(cr, t)
    date_stamp(cr, t, "1944", start=S["100"][0])


# ============================================================================================ 101: the fleet
FLEET = []
_r = random.Random(11)
for _i in range(18):
    _k = _r.random()
    FLEET.append((-60 + (_i % 9) * 245 + _r.uniform(-60, 60), 0.18 + 0.5 * _k, _r.choice(("bs", "dd", "dd", "fb")),
                  _r.random()))
FLEET.sort(key=lambda f: f[1])
SHIPS = {"bs": P.Battleship(side="allies"), "dd": P.Destroyer(side="allies"), "fb": P.FishingBoat(side="allies")}
PLANES = [P.Bomber(side="allies", seed=i) for i in range(5)]


def shot_101(cr, t):
    t0, t1 = S["101"]
    cr.save()
    zoomed(cr, t, t0, t1, 1.08, W * 0.5, 600)
    hz = 560
    paper(cr)
    SE.Sky(mode="dawn" if "dawn" in SE.SKIES else "dusk", horizon=hz, clouds=4, seed=2).draw(cr, t)
    SE.Ocean(horizon=hz, mode="day").draw(cr, t)
    u = seg(t, t0, t1)
    for i, (x, s, kind, ph) in enumerate(FLEET):                               # far ships first
        appear = ease_out(seg(t, t0 + 0.12 * i, t0 + 0.12 * i + 0.6))
        if appear <= 0:
            continue
        y = hz + 14 + 360 * (s - 0.18) ** 1.3
        SHIPS[kind].draw(cr, t, x=x + 30 * u * (1 + s), y=y, scale=s * (1.0 if kind != "fb" else 1.6), facing=1,
                         speed=60, alpha=appear, seed=i, silhouette="#3d3f45" if s < 0.4 else None)
    for i, pl in enumerate(PLANES):
        k = seg(t, t0 + 0.4 * i, t0 + 0.4 * i + 4.5)
        if 0 < k < 1:
            pl.draw(cr, t, x=lerp(-200, 2100, k), y=300 + 45 * i, scale=0.28 + 0.04 * i, facing=1, speed=220)
    cr.restore()
    text(cr, "THE BIGGEST INVASION FROM THE SEA", W / 2, 200, 70, font=SLAB, color="cream", bold=False,
         outline="ink", outline_w=8, alpha=ease_out(seg(t, at("101", 0.3), at("101", 0.5))), spacing=2)
    date_stamp(cr, t, "JUNE 1944", start=t0)


# ============================================================================================ the frame
SHOT_FN = {"87": shot_87, "88": shot_88, "89": shot_89, "90": shot_90, "91": shot_91, "92": shot_92,
           "93": shot_93, "94": shot_94, "95": shot_95, "96": shot_96, "97": shot_97, "98": shot_98,
           "99": shot_99, "100": shot_100, "101": shot_101}
HOLO = ("92", "93", "94", "95", "96", "97")


def draw(cr, t):
    if C5[0] <= t < C5[1]:
        card_c5(cr, t)
        print_finish(cr, t, strength=0.35)
        return
    if C6[0] <= t < C6[1]:
        card_c6(cr, t)
        print_finish(cr, t)
        return
    for n, (a, b) in S.items():
        if a <= t < b or (n == "101" and t >= b):
            SHOT_FN[n](cr, t)
            print_finish(cr, t, strength=0.35 if n in HOLO else 1.0)
            return
    paper(cr)
    print_finish(cr, t)


def cues(T=T):
    """[(episode time, sfx, gain dB, pan)] for helper 7. Nothing in chapter 5: the score's low tone and silence only."""
    c = []
    s88 = at("88", 0.47)
    c += [(S["87"][0] + 0.3, "page_whoosh", -14, 0.0), (at("87", 0.35), "tank", -16, -0.3),
          (at("87", 0.75), "stamp", -10, 0.2),
          (S["88"][0] + 0.2, "tank", -12, 0.0), (s88, "artillery_barrage", -10, 0.0),
          (s88 + 0.6, "gun_boom", -8, -0.4), (s88 + 0.9, "gun_boom", -8, 0.4), (at("88", 0.62), "explosion", -9, 0.0),
          (S["89"][0], "sea_waves", -14, 0.0), (at("89", 0.3), "morse", -20, -0.5), (at("89", 0.62), "explosion", -6, 0.2),
          (S["90"][0], "typewriter", -16, -0.3), (at("90", 0.42), "page_whoosh", -12, -0.2),
          (at("90", 0.42) + 1.1, "stamp", -10, 0.1), (at("90", 0.82), "morse", -14, 0.0),
          (S["91"][0], "plane_drone", -14, 0.4)]
    for j in range(4):
        c.append((S["91"][0] + 1.4 + 0.45 * j, "explosion", -14 - 2 * j, -0.3 + 0.2 * j))
    c += [(S["98"][0] + 0.2, "page_whoosh", -12, 0.0), (at("98", 0.15), "artillery", -12, 0.0),
          (at("99", 0.12), "stamp", -12, 0.0), (at("99", 0.42), "door_slam", -10, 0.2), (at("99", 0.8), "stamp", -9, 0.0),
          (at("100", 0.15), "artillery_barrage", -14, 0.0), (at("100", 0.75), "stamp", -12, -0.2),
          (S["101"][0], "sea_waves", -12, 0.0), (S["101"][0] + 0.3, "plane_drone", -10, 0.0)]
    return sorted(c)
