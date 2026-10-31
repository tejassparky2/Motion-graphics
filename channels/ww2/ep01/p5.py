"""WW2 Episode 1, package P5 (script lines 70-86; SHOTLIST C3-S16 .. C4-S15): the war goes global, chapter 4's card,
the Axis at its peak, Midway, El Alamein and Stalingrad.

Every beat is placed on the shared clock (timing.json via Timing): shot cuts sit halfway through the pauses between
lines, and beats inside a line are placed on its sentences, or on a phrase's share of its sentence (`at()`), so the
package re-times itself when the voiced narration lands. Nothing here is in hard-coded episode seconds.

    C3-S16  70  Roosevelt at the microphone, WAR ON JAPAN stamp                  DEC 1941   radio hiss, stamp
    C3-S17  71  Hitler points west across the Atlantic; an arrow to the US        DEC 1941   drum (gun_boom), stamp
    C3-S18  72  pull back over the world map; both oceans flicker with fire       DEC 1941   explosions
    C3-S19  73  THE AXIS: Hitler, Mussolini, Hirohito slide in (charcoal panels)  DEC 1941   page whoosh x3
    C3-S20  74  THE ALLIES: Churchill, Stalin, Roosevelt, Chiang + plain flags    DEC 1941   page whoosh x4
    C4 card     CHAPTER 4 THE TURNING POINTS (a poster wipe, then the card)                  fanfare
    C4-S02  75  world map: the Axis floods half the world                         EARLY 1942 page whoosh
    C4-S03  76  Pacific: Japan's sweep floods SE Asia, five arrows                EARLY 1942 artillery
    C4-S04  77a codebreakers' basement, a word circled in red, push in on it      MAY 1942   morse, typewriter
    C4-S05  77b Japan's course dashes across the Pacific; the pin drops on MIDWAY MAY 1942   stamp x2
    C4-S06  78a US dive bombers peel off into their dives; tilt down to the fleet JUNE 1942  dive whine x3
    C4-S07  78b three carriers hit and burning, IN 5 MINUTES; pull back           JUNE 1942  explosion x3
    C4-S08  79  four carrier icons crossed out (Akagi, Kaga, Soryu, Hiryu), TURNING POINT    stamp x5
    C4-S09  80  El Alamein: British tanks roll west; the inset map pushes Rommel back  NOV 1942  tank, guns
    C4-S10  81  the ruined city on the Volga, Stalin's medallion, STALINGRAD      AUG 1942   artillery barrage
    C4-S11  82  a building in cross-section, both sides on every floor; tilt up   AUG 1942   rifle cracks (muffled)
    C4-S12  83  red pincers close the ring round the 6th Army                     NOV 1942   tank, stamp
    C4-S13  84  Hitler slams the table: NO RETREAT                                NOV 1942   door slam, stamp
    C4-S14  85  a white flag in the snow                                          FEB 1943   blizzard
    C4-S15  86  the long line of prisoners walks into the snow; 91,000            FEB 1943   blizzard

Rules kept (STYLE.md): no symbols (plain charcoal for Germany and Japan, a plain roundel on British tanks, a plain
white star on US planes), rays only in ink, gold, blue or khaki, no visible deaths (hits are flat star bursts and
smoke; losses are numbers and crossed-out icons), a push-in and the date tag on every shot, print_finish last.
"""
import math
import random

from channels.ww2.kit.core import (H, LABEL, SLAB, STENCIL, W, back_out, cairo, camera, chapter_card,  # noqa
                                   col, counter, date_stamp, ease_in, ease_out, halftone, lerp, paper,
                                   print_finish, push_in, rays, seg, shake, smooth, text, word_card)
from channels.ww2.kit import fx, heads, props, sets, stick, things
from channels.ww2.kit import setpieces as sp
from channels.ww2.kit.maps import Map
from channels.ww2.kit.stick import Figure
from channels.ww2.ep01.timing import Timing, package_span

T = Timing()
SPAN = package_span("P5", T)


# ================================================================ the clock
def L(lid):
    return T.line(str(lid))


def sentences(lid):
    out, k = [], 0
    while True:
        try:
            out.append(T.sentence(str(lid), k))
        except IndexError:
            return out
        k += 1


def at(lid, phrase, end=False, n=0):
    """When `phrase` is spoken in line `lid`: its share of the characters in its sentence (the voice reads at an even
    pace inside a sentence). end=True: when it ends. n: the n-th occurrence."""
    for s in sentences(lid):
        i, k = -1, -1
        while k < n:
            i = s.text.lower().find(phrase.lower(), i + 1)
            if i < 0:
                break
            k += 1
        if i >= 0:
            j = i + (len(phrase) if end else 0)
            return s.start + (s.end - s.start) * j / max(1, len(s.text))
    raise KeyError(f"line {lid}: {phrase!r} not found")


def cut(a, b):
    """The cut between line a and line b: halfway through the pause."""
    return (L(a).end + L(b).start) / 2


# ================================================================ shared drawing helpers
def stamp(cr, t, start, label, x, y, size=110, tilt=-0.08, color="alert", font=SLAB, t_out=None):
    """A rubber stamp slamming onto the page: a double border, the word, worn ink (as the pact style frame)."""
    if t < start or (t_out is not None and t > t_out):
        return
    u = back_out(seg(t, start, start + 0.18))
    sc = 2.2 - 1.2 * u
    a = min(1.0, (t - start) / 0.08)
    if t_out is not None:
        a *= 1 - ease_in(seg(t, t_out - 0.25, t_out))
    cr.push_group()
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    cr.scale(sc, sc)
    cr.select_font_face(font)
    cr.set_font_size(size)
    w = cr.text_extents(label).x_advance + 6 * (len(label) - 1)
    pad = 26
    r, g, b, _ = col(color)
    cr.set_source_rgba(r, g, b, 0.92 * a)
    for k, inset in ((7, 0), (3, 13)):
        cr.set_line_width(k)
        cr.rectangle(-w / 2 - pad + inset, -size * 0.62 - pad * 0.8 + inset, w + 2 * pad - 2 * inset,
                     size * 1.24 + pad * 1.6 - 2 * inset)
        cr.stroke()
    text(cr, label, 0, size * 0.36, size, font=font, color=color, bold=False, alpha=0.92 * a, spacing=6)
    cr.set_operator(cairo.OPERATOR_DEST_OUT)
    rnd = random.Random(len(label) * 7 + 5)
    for _ in range(150):
        cr.arc(rnd.uniform(-w / 2 - pad, w / 2 + pad), rnd.uniform(-size * 0.7, size * 0.7), rnd.uniform(1, 3.2), 0,
               2 * math.pi)
        cr.set_source_rgba(0, 0, 0, 0.55)
        cr.fill()
    cr.restore()
    cr.pop_group_to_source()
    cr.paint()


def ribbon(cr, t, start, label, x, y, size=46, color="alert", txt="cream", align="left", sub=None):
    """A printed name ribbon that slides in from the side (`align` = the side it is anchored to)."""
    if t < start:
        return
    u = ease_out(seg(t, start, start + 0.35))
    cr.save()
    cr.select_font_face(STENCIL)
    cr.set_font_size(size)
    w = cr.text_extents(label).x_advance + 0.12 * size * len(label) + 2 * size * 0.6
    h = size * 1.35
    x0 = x if align == "left" else x - w
    dx = (-1 if align == "left" else 1) * (1 - u) * (w + 80)
    cr.translate(dx, 0)
    cr.rectangle(x0 + 7, y - h / 2 + 7, w, h)
    cr.set_source_rgba(*col("ink", 0.85))
    cr.fill()
    cr.rectangle(x0, y - h / 2, w, h)
    cr.set_source_rgba(*col(color))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(5)
    cr.stroke()
    text(cr, label, x0 + w / 2, y + size * 0.36, size, font=STENCIL, color=txt, spacing=0.12 * size)
    if sub:
        text(cr, sub, x0 + w / 2, y + h / 2 + size * 0.62, size * 0.5, font=LABEL, color="ink")
    cr.restore()


def floor_band(cr, y, color, dots=2, alpha=0.95):
    cr.rectangle(-400, y, W + 800, H - y + 400)
    cr.set_source_rgba(*col(color, alpha))
    cr.fill()
    halftone(cr, lambda c: c.rectangle(-400, y, W + 800, H - y + 400), "ink", density=dots, alpha=0.3)
    cr.move_to(-400, y)
    cr.line_to(W + 400, y)
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(5)
    cr.stroke()


def mirror_x(cr, cx):
    cr.translate(cx, 0)
    cr.scale(-1, 1)
    cr.translate(-cx, 0)


def rect_path(x, y, w, h):
    return lambda c: c.rectangle(x, y, w, h)


# ================================================================ C3-S16 (70): Roosevelt at the microphone
MIC = things.Microphone(x=1320, y=930, scale=1.35)


def s_roosevelt(cr, t, t0, t1):
    paper(cr)
    z = push_in(t, t0, t1, 1.0, 1.07)
    cr.save()
    camera(cr, z, W / 2 - 40, H / 2 + 30)
    rays(cr, t, 820, 470, n=28, color="allies", alpha=0.20, spin=0.02)
    halftone(cr, rect_path(-200, -200, W + 400, H + 400), "ink", density=1, alpha=0.07)
    heads.portrait(cr, t, "roosevelt", 760, 1110, height=1000, expr="determined", turn=0.42,
                   nod=0.03 * math.sin(2 * math.pi * (t - t0) / 1.7))          # speaking: a small nodding beat
    MIC.draw(cr, t, on=True)
    cr.rectangle(-300, 930, W + 600, 400)                                      # the desk edge in front
    cr.set_source_rgba(*col("#6b4a2f"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(6)
    cr.stroke()
    halftone(cr, rect_path(-300, 965, W + 600, 300), "ink", density=2, alpha=0.35)
    cr.restore()
    ribbon(cr, t, t0 + 0.6, "PRESIDENT ROOSEVELT", 70, 1000, size=40, color="allies")
    stamp(cr, t, at(70, "declares war"), "WAR ON JAPAN", 1440, 240, size=84, tilt=-0.07)


# ================================================================ C3-S17 (71): Hitler points across the Atlantic
def _world(**kw):
    """The world at the end of 1941: Germany, Italy, Japan and their conquests charcoal (occupied halftoned), the
    Soviet Union red, Britain, the Commonwealth and the US navy-blue, China mustard."""
    m = Map("world", **kw)
    m.side("ussr", -9, "soviet", occupied=False)
    m.side("commonwealth", -9, "allies", occupied=False)
    m.side("allies_1942", -9, "allies", occupied=False)
    m.side("chn", -9, "china", occupied=False)
    for r in ("deu", "aut", "ita", "jpn"):
        m.side(r, -9, "germany" if r != "jpn" else "japan", occupied=False)
    return m


EUROPE_OCC = ["cze", "pol", "fra", "bel", "nld", "lux", "dnk", "nor", "grc", "srb", "hrv", "bih", "mne", "mkd",
              "svn", "kos", "alb", "ukr", "blr", "est", "lva", "ltu"]
ASIA_1941 = ["kor", "prk", "twn", "vnm", "lao", "khm"]                  # Japan's by December 1941
ASIA_1942 = ["phl", "idn", "mys", "mmr", "brn", "sgp", "tls", "png", "tha"]
MINORS = ["hun", "rou", "bgr", "svk"]


def _late_1941(m):
    for r in EUROPE_OCC:
        m.side(r, -9, "germany")
    for r in ASIA_1941:
        m.side(r, -9, "japan")
    for r in MINORS:
        m.side(r, -9, "italy", occupied=False)


S17 = {}


def _setup_s17(t0, t1):
    m = _world()
    _late_1941(m)
    d = t1 - t0
    m.camera_key(0.0, (-30.0, 44.0), 2.0)
    m.camera_key(d, (-34.0, 43.0), 2.25)
    w = at(71, "declares war") - t0
    m.arrow([(9.0, 50.5), (-12.0, 50.0), (-40.0, 45.0), (-74.0, 41.0)], "germany", w - 0.2, w + 1.5, width=84)
    m.label("GERMANY", 0.3, lonlat=(10.5, 51.5), size=36)
    m.label("UNITED STATES", 0.3, lonlat=(-98.0, 39.5), size=44)
    m.label("ATLANTIC OCEAN", 0.6, lonlat=(-38.0, 31.0), size=30, color="ink_soft")
    m.city("Washington", w + 1.3, lonlat=(-77.0, 38.9), dx=-140, dy=26)
    S17.update(m=m, war=w)


HITLER_POINT = Figure(leader="hitler", x=1600, y=1480, scale=2.35, facing=-1, seed=4)


def s_hitler_atlantic(cr, t, t0, t1):
    m, w = S17["m"], S17["war"]
    lt = t - t0
    paper(cr)
    m.draw(cr, lt)
    # he turns to the map and jabs down at the Atlantic twice, elbow bent (no straight arms: STYLE.md); the arrow
    # does the pointing
    jab_up = dict(lean=0.18, nod=0.32, sh_n=0.85, el_n=1.25, turn=0.35, hand_n="fist",
                  face={"brow": "angry", "mouth": "grit", "look": (-4, 6)})
    jab = dict(lean=0.3, nod=0.42, sh_n=0.55, el_n=0.75, turn=0.35, hand_n="fist",
               face={"brow": "angry", "mouth": "grit", "look": (-4, 8)})
    track = [(0.0, "stand"), (0.35, dict(turn=0.5, face={"brow": "angry"})), (w - 0.5, jab_up), (w - 0.15, jab),
             (w + 0.25, jab_up), (w + 0.55, jab), (w + 1.6, dict(jab, nod=0.25, lean=0.2))]
    z = push_in(t, t0, t1, 1.0, 1.05)
    cr.save()
    camera(cr, z, W / 2, H / 2)
    HITLER_POINT.draw(cr, lt, track)
    cr.restore()
    stamp(cr, t, t0 + w + 1.5, "WAR ON THE U.S.", 640, 840, size=86, tilt=-0.06)


# ================================================================ C3-S18 (72): a world war
S18 = {}
FIRES = [(-40.0, 50.0), (-25.0, 38.0), (-60.0, 40.0), (-158.0, 21.3), (150.0, 12.0), (125.0, 8.0), (170.0, 30.0),
         (-170.0, 5.0), (-15.0, 55.0), (135.0, -5.0)]


def _setup_s18(t0, t1):
    m = _world(compass=True)
    _late_1941(m)
    d = t1 - t0
    m.camera_key(0.0, (5.0, 22.0), 1.75)
    m.camera_key(d, (10.0, 12.0), 1.02)
    S18.update(m=m, d=d)


def s_world_war(cr, t, t0, t1):
    m = S18["m"]
    lt = t - t0
    paper(cr)
    m.draw(cr, lt)
    for i, ll in enumerate(FIRES):                              # both oceans flicker: bursts in turn, then fire
        start = 0.15 + i * 0.22
        if lt < start:
            continue
        x, y = m.screen(m.xy(ll))
        age = lt - start
        k = m._z ** 0.5 * 0.5
        if age < 0.6:
            fx.starburst(cr, x, y, age, size=0.55 * k + 0.25, seed=i)
        props.fire(cr, x, y + 6, lt, size=26 * k + 14, seed=i)
    word_card(cr, t, L(72).start + 0.1, "A WORLD WAR", dur=t1 - L(72).start - 0.1, y=H * 0.16, size=128,
              color="alert")


# ================================================================ C3-S19 / S20 (73, 74): the two sides
def _panels(cr, t, t0, t1, cast, title, title_t, title_col, ray_cols, bot=930):
    """The printed panels are there from the cut (rays turning in each); each portrait rises into its panel when its
    country is named, and the name band drops in under it (cast: [(who, label, side colour, t_in, flip)])."""
    paper(cr)
    n = len(cast)
    z = push_in(t, t0, t1, 1.0, 1.04)
    cr.save()
    camera(cr, z, W / 2, H / 2 + 20)
    margin, gap = 70, 26
    pw = (W - 2 * margin - (n - 1) * gap) / n
    top = 210
    for i, (who, label, side, t_in, flip) in enumerate(cast):
        x0 = margin + i * (pw + gap)
        a_in = ease_out(seg(t, t0 + 0.06 * i, t0 + 0.06 * i + 0.3))          # the frames print in at the cut
        cr.save()
        cr.translate(0, (1 - a_in) * 40)
        cr.rectangle(x0 + 10, top + 10, pw, bot - top)                         # hard drop shadow
        cr.set_source_rgba(*col("ink", 0.8 * a_in))
        cr.fill()
        cr.save()
        cr.rectangle(x0, top, pw, bot - top)
        cr.clip()
        cr.set_source_rgba(*col("paper"))
        cr.paint()
        rays(cr, t + i, x0 + pw / 2, top + 260, n=24, color=ray_cols[i], alpha=0.42, spin=0.03)
        u = ease_out(seg(t, t_in, t_in + 0.45)) if t >= t_in else 0.0
        if u > 0:
            cr.save()
            cr.translate(0, (1 - u) * (bot - top + 60))
            if flip:
                mirror_x(cr, x0 + pw / 2)
            hgt = min(640.0, pw * 1.45)
            heads.portrait(cr, t, who, x0 + pw / 2, bot - 120, height=hgt, expr="determined", turn=0.38, seed=i + 2)
            cr.restore()
        bu = ease_out(seg(t, t_in + 0.15, t_in + 0.45)) if t >= t_in else 0.0
        cr.rectangle(x0, bot - 150 * bu, pw, 150)                               # the side's colour band
        cr.set_source_rgba(*col(side))
        cr.fill()
        halftone(cr, rect_path(x0, bot - 150 * bu, pw, 150), "ink", density=2, alpha=0.3)
        cr.restore()
        cr.rectangle(x0, top, pw, bot - top)
        cr.set_source_rgba(*col("ink", a_in))
        cr.set_line_width(7)
        cr.stroke()
        if bu > 0:
            text(cr, label, x0 + pw / 2, bot - 44 + (1 - bu) * 40, min(52.0, pw * 0.13), font=STENCIL,
                 color="cream", spacing=5, outline="ink", outline_w=4, alpha=bu)
        cr.restore()
    cr.restore()
    title_t = min(title_t, t0 + 0.25)
    if t >= title_t:
        u = back_out(seg(t, title_t, title_t + 0.3))
        cr.save()
        cr.translate(W / 2, 128)
        cr.scale(0.6 + 0.4 * u, 0.6 + 0.4 * u)
        text(cr, title, 0, 38, 104, font=SLAB, color=title_col, bold=False, outline="ink", outline_w=9, spacing=4,
             alpha=min(1.0, u * 2))
        cr.restore()


def s_axis(cr, t, t0, t1):
    cast = [("hitler", "GERMANY", "axis", at(73, "Germany") - 0.15, False),
            ("mussolini", "ITALY", "axis_it", at(73, "Italy") - 0.15, False),
            ("hirohito", "JAPAN", "axis_jp", at(73, "Japan") - 0.15, True)]
    _panels(cr, t, t0, t1, cast, "THE AXIS", at(73, "the Axis") - 0.1, "axis", ("ink", "ink", "ink"))


CHIPS = [("#2f5f8f", "#f8f2e2"), ("#c8372d", None), ("#3d7a4a", "#f8f2e2"), ("#d9a63a", "#2f5f8f"),
         ("#f8f2e2", "#2f5f8f"), ("#6f6a3c", None), ("#2f5f8f", "#c8372d"), ("#e3d3ad", "#3d7a4a"),
         ("#a89566", None), ("#c8372d", "#f8f2e2"), ("#3d7a4a", None), ("#2f5f8f", "#d9a63a")]
FLAGS = [things.Flag(x=110 + i * 112, y=1070, scale=0.62, color=c, stripe=s, seed=i) for i, (c, s) in enumerate(CHIPS)]


def s_allies(cr, t, t0, t1):
    cast = [("churchill", "BRITAIN", "allies", at(74, "Britain") - 0.15, False),
            ("stalin", "SOVIET UNION", "soviet", at(74, "the Soviet Union") - 0.15, False),
            ("roosevelt", "UNITED STATES", "allies", at(74, "the United States") - 0.15, True),
            ("chiang", "CHINA", "china", at(74, "China") - 0.15, True)]
    _panels(cr, t, t0, t1, cast, "THE ALLIES", at(74, "the Allies") - 0.1, "allies",
            ("allies", "gold", "allies", "gold"), bot=870)
    m0 = at(74, "and many more") - 0.1                      # "and many more": plain flags as colour chips
    if t >= m0:
        for i, f in enumerate(FLAGS):
            ti = m0 + i * 0.07
            if t < ti:
                continue
            u = back_out(seg(t, ti, ti + 0.3))
            f.draw(cr, t, y=1080 + 120 * (1 - u))
        ribbon(cr, t, m0 + 0.35, "AND MANY MORE", W - 70, 975, size=44, color="allies", align="right")


# ================================================================ chapter 4 card
def s_card(cr, t, t0, t1):
    c0, c1 = T.chapter("C4").card
    wipe = ease_in(seg(t, c0, c0 + 0.4))
    if wipe < 1:                                                # the outgoing shot under the wipe
        s_allies(cr, t, SHOTS_BY["allies"][0], SHOTS_BY["allies"][1])
    wx = wipe * (W + 300)
    cr.save()
    cr.move_to(-300, 0)
    cr.line_to(wx, 0)
    cr.line_to(wx - 300, H)
    cr.line_to(-300, H)
    cr.close_path()
    cr.clip_preserve()
    cr.new_path()
    paper(cr)
    rays(cr, t, W / 2, H / 2, n=28, color="khaki", alpha=0.35, spin=0.02)
    cr.restore()
    if wipe < 1:                                                # the wipe's printed edge
        cr.move_to(wx, 0)
        cr.line_to(wx - 300, H)
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(14)
        cr.stroke()
    chapter_card(cr, t, c0 + 0.4, 4, T.chapter("C4").title, dur=c1 - c0 - 0.4)   # once the wipe has crossed


# ================================================================ C4-S02 (75): the Axis at its peak
S02 = {}


def _setup_s02(t0, t1):
    m = _world()
    for r in MINORS:
        m.side(r, -9, "italy", occupied=False)
    d = t1 - t0
    m.camera_key(0.0, (55.0, 32.0), 1.55)
    m.camera_key(d, (40.0, 22.0), 1.12)
    f0 = 0.25
    for r in EUROPE_OCC:
        m.side(r, f0, "germany", origin=(11.0, 51.0), dur=1.6)
    for r in ASIA_1941 + ASIA_1942:
        m.side(r, f0 + 0.5, "japan", origin=(136.0, 36.0), dur=1.8)
    m.label("AXIS", f0 + 0.5, lonlat=(16.0, 47.0), size=64)
    m.label("AXIS", f0 + 1.0, lonlat=(112.0, 12.0), size=64)
    S02.update(m=m, f0=f0)


def s_axis_peak(cr, t, t0, t1):
    paper(cr)
    S02["m"].draw(cr, t - t0)
    stamp(cr, t, at(75, "unstoppable") - 0.05, "UNSTOPPABLE?", 1180, 930, size=74, tilt=-0.07, color="ink")


# ================================================================ C4-S03 (76): Japan's sweep
S03 = {}


def _setup_s03(t0, t1):
    m = Map("pacific", era="1941")
    d = t1 - t0
    m.camera_key(0.0, (128.0, 26.0), 1.55)
    m.camera_key(d, (122.0, 10.0), 1.85)
    a0 = at(76, "sweeps") - t0 - 0.2
    m.arrows("japan_1941_42", a0, a0 + 1.4, stagger=0.22)
    m.side("japan_1942_extent", a0 + 0.4, "japan", origin=(121.0, 22.0), dur=2.2)
    for name, lonlat, k in (("PHILIPPINES", (122.5, 12.5), 0.9), ("MALAYA", (102.0, 4.0), 1.3),
                            ("BURMA", (96.0, 21.0), 1.6), ("DUTCH EAST INDIES", (114.0, -2.0), 1.9)):
        m.label(name, a0 + k, lonlat=lonlat, size=32)
    m.label("JAPAN", 0.2, lonlat=(138.0, 37.5), size=40)
    m.label("PACIFIC OCEAN", 0.4, lonlat=(150.0, 18.0), size=34, color="ink_soft")
    S03.update(m=m)


def s_sweep(cr, t, t0, t1):
    paper(cr)
    S03["m"].draw(cr, t - t0)


# ================================================================ C4-S04 (77a): the codebreakers' basement
PAPERS = things.Papers(x=1180, y=842, scale=0.95)
PHONES = things.Headphones(x=800, y=850, scale=0.45)
RADIO = props.Radio(x=250, y=868, scale=0.8)
BREAKER_A = Figure(x=560, y=1180, scale=1.75, facing=1, seed=21)
BREAKER_B = Figure(x=1600, y=1200, scale=1.8, facing=-1, seed=22, prop="pen")


def _basement(cr, t):
    """A concrete basement: block wall, pipes, a high window's light shaft, a swinging lamp's halftone cone."""
    cr.set_source_rgba(*col("#9a917c"))
    cr.paint()
    for row in range(14):                                       # cinder-block courses
        y = row * 70
        cr.move_to(-200, y)
        cr.line_to(W + 200, y)
        off = 0 if row % 2 else 70
        for x in range(-200 + off, W + 200, 140):
            cr.move_to(x, y)
            cr.line_to(x, y + 70)
    cr.set_source_rgba(*col("ink", 0.25))
    cr.set_line_width(3)
    cr.stroke()
    halftone(cr, rect_path(-200, -200, W + 400, H + 400), "ink", density=2, alpha=0.18)
    for y, w in ((120, 26), (170, 16)):                         # pipes along the ceiling
        cr.rectangle(-200, y, W + 400, w)
        cr.set_source_rgba(*col("#6c6658"))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(4)
        cr.stroke()
    sw = 0.06 * math.sin(t * 1.7)                               # the lamp swings a little
    lx, ly = W / 2 + 420 * math.sin(sw), 300
    cr.move_to(W / 2, 0)
    cr.line_to(lx, ly - 30)
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(4)
    cr.stroke()
    cone = lambda c: (c.move_to(lx - 40, ly), c.line_to(lx - 520 + 300 * sw, H), c.line_to(lx + 520 + 300 * sw, H),  # noqa: E731
                      c.line_to(lx + 40, ly), c.close_path())
    cone(cr)
    cr.set_source_rgba(*col("cream", 0.30))
    cr.fill()
    halftone(cr, cone, "cream", density=3, alpha=0.35)
    cr.move_to(lx - 70, ly)
    cr.curve_to(lx - 60, ly - 50, lx + 60, ly - 50, lx + 70, ly)
    cr.close_path()
    cr.set_source_rgba(*col("#3e4a3c"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(5)
    cr.stroke()
    cr.arc(lx, ly + 6, 16, 0, 2 * math.pi)
    cr.set_source_rgba(*col("#fff4c8"))
    cr.fill()


def s_codebreakers(cr, t, t0, t1):
    s = sentences(77)[0]
    c0 = lerp(s.start, s.end, 0.55)                             # the word gets circled late in the sentence
    cr.save()
    zz = push_in(t, t0, t1, 1.0, 1.08)
    k = smooth(seg(t, c0 + 0.3, t1))                            # the push drifts onto the circled word
    camera(cr, zz + 0.35 * k, lerp(W / 2, 1180, k), lerp(H / 2, 820, k))
    _basement(cr, t)
    BREAKER_A.draw(cr, t, [(t0, dict(lean=0.22, nod=0.3, sh_n=0.75, el_n=0.75, sh_f=0.6, el_f=0.85, turn=0.4,
                                     face={"brow": "worried"}))])
    cr.save()                                                   # his headset on his head
    j = BREAKER_A.joints(t, [(t0, dict(lean=0.18, nod=0.25, turn=0.4))])
    hx, hy = j["head"]
    things.Headphones(x=hx, y=hy - 4, scale=0.36).draw(cr, t)
    cr.restore()
    BREAKER_B.draw(cr, t, [(t0, dict(lean=0.42, nod=0.45, sh_n=0.95, el_n=1.15, turn=0.3, face={"brow": "angry"})),
                           (c0, dict(lean=0.45, nod=0.5, sh_n=1.0, el_n=1.0, turn=0.3,
                                     face={"brow": "angry", "mouth": "o"}))])
    cr.rectangle(-300, 860, W + 600, 400)                       # the desk
    cr.set_source_rgba(*col("#6b4a2f"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(6)
    cr.stroke()
    halftone(cr, rect_path(-300, 900, W + 600, 300), "ink", density=2, alpha=0.35)
    RADIO.draw(cr, t, on=True)
    PHONES.draw(cr, t)
    PAPERS.draw(cr, t, circle=ease_out(seg(t, c0, c0 + 0.7)), word=8)
    cr.restore()
    ribbon(cr, t, t0 + 0.5, "U.S. NAVY CODEBREAKERS", 70, 990, size=40, color="allies")


# ================================================================ C4-S05 (77b): Midway
S05 = {}


def _setup_s05(t0, t1):
    m = Map("pacific", era="1942")
    d = t1 - t0
    m.camera_key(0.0, (170.0, 30.0), 1.35)
    m.camera_key(min(1.6, d * 0.6), (-177.4, 28.2), 3.6)
    m.camera_key(d, (-177.4, 28.2), 4.0)
    p = at(77, "Midway") - t0
    m.pins("midway", p - 0.15, size=44)
    m.label("JAPAN", 0.0, lonlat=(138.0, 37.5), size=40)
    m.label("PACIFIC OCEAN", 0.2, lonlat=(172.0, 37.0), size=40, color="ink_soft")
    m.secret_line([(136.0, 33.5), (152.0, 31.5), (168.0, 29.5), (-177.6, 28.3)], 0.15, p - 0.2,
                  color="axis_jp", width=7)                     # where Japan will strike next
    m.city("Pearl Harbor", 0.2, lonlat=(-157.95, 21.35), dx=18, dy=30)
    S05.update(m=m, p=p)


def s_midway(cr, t, t0, t1):
    paper(cr)
    m = S05["m"]
    m.draw(cr, t - t0)
    x, y = m.screen(m.xy((-177.37, 28.21)))
    p = t0 + S05["p"]
    if t >= p - 0.35:                                           # the pin drops onto the island
        u = ease_in(seg(t, p - 0.35, p - 0.05))
        py = lerp(y - 520, y, u)
        sq = 1 + 0.25 * math.exp(-12 * max(0.0, t - p + 0.05)) * (t > p - 0.05)
        cr.save()
        cr.translate(x, py)
        cr.scale(1 / sq, sq)
        cr.move_to(0, 0)
        cr.curve_to(-30, -50, -44, -70, -44, -96)
        cr.arc(0, -96, 44, math.pi, 0)
        cr.curve_to(44, -70, 30, -50, 0, 0)
        cr.close_path()
        cr.set_source_rgba(*col("alert"))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(6)
        cr.stroke()
        cr.arc(0, -96, 16, 0, 2 * math.pi)
        cr.set_source_rgba(*col("cream"))
        cr.fill()
        cr.restore()
    stamp(cr, t, p + 0.35, "TARGET: MIDWAY", 560, 880, size=72, tilt=-0.06)


# ================================================================ C4-S06 (78a): the dive bombers
SKY = sets.Sky(mode="day", horizon=1500, clouds=7, seed=12)


def _far_sea(cr, t, hz):
    """The sea far below the bombers (the Ocean set stops at the frame's bottom; this one runs on under the tilt)."""
    cr.rectangle(-400, hz, W + 800, 900)
    cr.set_source_rgba(*col("sea"))
    cr.fill()
    for i in range(40):
        y = hz + 6 + i * 22
        off = (t * 12 + i * 37) % 80
        cr.set_dash([60 + 3 * i, 20], -off)
        cr.move_to(-400, y)
        cr.line_to(W + 400, y)
        cr.set_source_rgba(*col("sea_dk", 0.9))
        cr.set_line_width(2.0)
        cr.stroke()
    cr.set_dash([])
    cr.move_to(-400, hz)
    cr.line_to(W + 400, hz)
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(3)
    cr.stroke()

BOMBERS = [props.DiveBomber(side="usa", scale=0.9, seed=k) for k in range(3)]
FAR_FLEET = [props.Carrier(side="japan", scale=0.16, seed=k, silhouette="#4a4c50") for k in range(3)]


def s_dive(cr, t, t0, t1):
    lt = t - t0
    d = t1 - t0
    tilt = smooth(seg(lt, d * 0.35, d * 0.95))                   # tilt down from the bombers to the sea
    paper(cr)
    cr.save()
    camera(cr, push_in(t, t0, t1, 1.0, 1.05), W / 2, lerp(H / 2, 1340, tilt))
    cr.save()
    cr.translate(0, -40)
    cr.scale(1, 1)
    sets.bands(cr, -600, 1500, ("#c9c3a8", "#d6d0b6", "#e2dcc4"))
    cr.restore()
    for i in range(7):                                         # clouds below and around
        x = (i * 380 + lt * (30 + 10 * i)) % (W + 700) - 350
        fx.cloud(cr, x, 300 + (i * 173) % 900, 360 + 40 * (i % 3), seed=i, color="cream")
    _far_sea(cr, t, 1500)
    for k, f in enumerate(FAR_FLEET):
        f.draw(cr, t, x=760 + k * 300, y=1580 + k * 40, speed=10)
    for k, b in enumerate(BOMBERS):                            # peel off one by one into their dives
        tk = d * 0.18 + k * 0.55
        u = smooth(seg(lt, tk, tk + 0.9))
        x0, y0 = 300 + k * 300, 170 + k * 110
        lx, ly = x0 + 150 * min(lt, tk), y0                    # level flight until it peels off
        tx, ty = 820 + k * 300, 1330 + k * 40                   # aimed at the carriers far below
        v = smooth(seg(lt, tk, d)) ** 1.3
        x = lerp(lx + 150 * (lt - tk) * (1 - v) if lt > tk else lx, tx, v)
        y = lerp(ly, ty, v)
        b.draw(cr, t, x=x, y=y, dive=u, rpm=20, scale=lerp(0.9, 0.7, v))
    cr.restore()
    ribbon(cr, t, t0 + 0.4, "U.S. DIVE BOMBERS", 70, 990, size=40, color="allies")


# ================================================================ C4-S07 (78b): three carriers on fire
OCEAN = sets.Ocean(horizon=560)
SKY7 = sets.Sky(mode="day", horizon=560, clouds=4, seed=7)
CARRIERS = [props.Carrier(side="japan", x=1350, y=650, scale=0.42, seed=1, facing=-1),
            props.Carrier(side="japan", x=560, y=760, scale=0.6, seed=2, facing=-1),
            props.Carrier(side="japan", x=1180, y=930, scale=0.85, seed=3, facing=-1)]


def s_carriers(cr, t, t0, t1):
    hits = [at(78, "three of them") + k * 0.45 for k in range(3)]
    cr.save()
    zz = lerp(1.14, 1.0, smooth(seg(t, hits[0], t1)))           # pull back as they burn
    camera(cr, zz, W / 2, H / 2 + 40)
    SKY7.draw(cr, t)
    OCEAN.draw(cr, t)
    for k, c in enumerate(CARRIERS):
        burn = ease_out(seg(t, hits[k], hits[k] + 1.6))
        c.draw(cr, t, speed=40 * (1 - burn), burn=burn)
    for k, c in enumerate(CARRIERS):
        if t >= hits[k]:
            age = t - hits[k]
            s = c.o["scale"]
            props.explosion(cr, c.o["x"] - 40 * s, c.o["y"] - 120 * s, age, size=1.6 * s + 0.3, seed=k)
    for k in range(3):                                         # the bombers pulling out overhead
        tk = hits[k] - 0.6
        if tk <= t <= tk + 1.4:
            u = (t - tk) / 1.4
            BOMBERS[k].draw(cr, t, x=lerp(-100, W + 200, u), y=lerp(260, 120, u) + 30 * k, dive=0.0, scale=0.55)
    cr.restore()
    for k in range(3):                                          # a short flash on each hit (not a white-out)
        if hits[k] <= t < hits[k] + 0.3:
            cr.set_source_rgba(*col("white", 0.42 * (1 - (t - hits[k]) / 0.3) ** 2))
            cr.paint()
    word_card(cr, t, at(78, "about five minutes") - 0.1, "IN 5 MINUTES", dur=t1 - at(78, "about five minutes"),
              y=H * 0.15, size=104, color="alert")


# ================================================================ C4-S08 (79): four carriers lost
LOST = ["AKAGI", "KAGA", "SORYU", "HIRYU"]
ICONS = [props.Carrier(side="japan", x=265 + k * 463, y=600, scale=0.5, seed=k + 4, water=None) for k in range(4)]


def s_lost(cr, t, t0, t1):
    s0, s1 = sentences(79)
    paper(cr)
    z = push_in(t, t0, t1, 1.0, 1.05)
    cr.save()
    camera(cr, z, W / 2, H / 2)
    rays(cr, t, W / 2, 560, n=28, color="ink", alpha=0.08, spin=0.02)
    cr.rectangle(-400, 640, W + 800, 18)
    cr.set_source_rgba(*col("sea_dk"))
    cr.fill()
    xs = [at(79, "four") + 0.15 + k * 0.42 for k in range(4)]
    for k, ic in enumerate(ICONS):
        sink = ease_in(seg(t, xs[k] + 0.4, xs[k] + 2.6))
        ic.draw(cr, t, y=600 + 26 * sink, alpha=1 - 0.45 * sink)
        text(cr, LOST[k], ic.o["x"], 730, 44, font=STENCIL, color="ink", spacing=5)
        if t >= xs[k]:                                          # the X stamped over each
            u = back_out(seg(t, xs[k], xs[k] + 0.16))
            cr.save()
            cr.translate(ic.o["x"], 555)
            cr.scale(2.0 - u, 2.0 - u)
            for a in (1, -1):
                cr.move_to(-130, -110 * a)
                cr.line_to(130, 110 * a)
            cr.set_source_rgba(*col("alert", 0.92))
            cr.set_line_width(26)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.stroke()
            cr.restore()
    cr.restore()
    counter(cr, t, xs[0] - 0.1, xs[3] + 0.1, 4, W / 2, 960, size=170, color="alert")
    if t > xs[0]:
        text(cr, "JAPANESE CARRIERS LOST", W / 2, 1030, 44, font=STENCIL, color="ink", spacing=6,
             alpha=ease_out(seg(t, xs[0], xs[0] + 0.4)))
    a = ease_out(seg(t, t0, t0 + 0.4)) * (1 - ease_in(seg(t, s1.start, s1.start + 0.25)))
    text(cr, "THE BATTLE OF MIDWAY", W / 2, 300, 84, font=SLAB, color="ink", bold=False, alpha=a, spacing=3)
    stamp(cr, t, s1.start + 0.25, "TURNING POINT", W / 2, 270, size=104, tilt=-0.05)


# ================================================================ C4-S09 (80): El Alamein
SKY9 = sets.Sky(mode="day", horizon=640, clouds=3, seed=9)
TANKS9 = [props.Tank(side="britain", x=1560, y=770, scale=0.62, facing=-1, seed=1),
          props.Tank(side="britain", x=1150, y=880, scale=0.85, facing=-1, seed=2),
          props.Tank(side="britain", x=1700, y=1040, scale=1.15, facing=-1, seed=3)]
S09 = {}


def _setup_s09(t0, t1):
    m = Map("europe", era="1941", compass=False)
    m.side("libya", -9, "italy", occupied=False)
    m.camera_key(0.0, (23.5, 30.2), 2.15)
    m.camera_key(t1 - t0, (24.0, 30.4), 2.3)
    r0 = at(80, "Erwin Rommel") - t0
    m.arrows("rommel_1942", -9, -8.5, width=150)
    m.arrows("el_alamein", r0 + 0.6, r0 + 2.4, width=150)
    m.city("El Alamein", 0.0, lonlat=(28.95, 30.83), dx=-80, dy=70, size=64)
    m.label("ROMMEL", r0 - 0.1, lonlat=(20.0, 33.6), size=72)
    m.label("EGYPT", 0.0, lonlat=(29.5, 26.0), size=72)
    m.label("LIBYA", 0.0, lonlat=(17.5, 27.0), size=72)
    m.label("MEDITERRANEAN SEA", 0.0, lonlat=(22.0, 35.2), size=54, color="ink_soft")
    S09.update(m=m, r0=r0)


def _desert(cr, t):
    SKY9.draw(cr, t)
    for y, c in ((640, "#d8bd83"), (700, "#cfae6f"), (800, "#c7a464"), (930, "#bd9a59")):
        cr.move_to(-300, y)
        for i in range(25):
            x = -300 + i * 110
            cr.line_to(x, y + 14 * math.sin(i * 0.9 + y))
        cr.line_to(W + 300, H + 300)
        cr.line_to(-300, H + 300)
        cr.close_path()
        cr.set_source_rgba(*col(c))
        cr.fill()
    halftone(cr, rect_path(-300, 640, W + 600, 600), "ink", density=1, alpha=0.18)
    cr.move_to(-300, 640)
    cr.line_to(W + 300, 640)
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(4)
    cr.stroke()


def s_alamein(cr, t, t0, t1):
    lt = t - t0
    cr.save()
    camera(cr, push_in(t, t0, t1, 1.0, 1.06), W / 2 - 60, H / 2)
    _desert(cr, t)
    for k in range(5):                                         # the enemy's guns: far flashes on the western horizon
        tk = 0.6 + k * 1.3
        if lt >= tk:
            fx.starburst(cr, 120 + k * 150, 650, lt - tk, size=0.35, seed=k + 9)
            props.smoke(cr, 120 + k * 150, 640, lt, height=200, width=40, rate=2.0, life=3.0, seed=k)
    for k, tk in enumerate(TANKS9):
        x = tk.o["x"] - 70 * lt * tk.o["scale"]
        fires = [t0 + 0.9 + k * 0.7 + 2.2 * j for j in range(4)]
        tk.draw(cr, t, x=x, speed=70, turret=0, fire=fires)
        props.smoke(cr, x + 260 * tk.o["scale"], tk.o["y"] - 20, lt, height=160 * tk.o["scale"],
                    width=60 * tk.o["scale"], color="#d8c08e", rate=3.0, life=2.0, seed=k + 3)
    cr.restore()
    r0 = t0 + S09["r0"]
    if t >= r0 - 0.4:                                           # the inset map slides down from the top
        u = ease_out(seg(t, r0 - 0.4, r0 + 0.1))
        ix, iy, iw, ih = 60 - (1 - u) * 1200, 150, 1000, 562
        cr.save()
        cr.rectangle(ix + 12, iy + 12, iw, ih)
        cr.set_source_rgba(*col("ink", 0.8))
        cr.fill()
        cr.rectangle(ix, iy, iw, ih)
        cr.clip()
        cr.translate(ix, iy)
        cr.scale(iw / W, ih / H)
        S09["m"].draw(cr, t - t0)
        cr.restore()
        cr.rectangle(ix, iy, iw, ih)
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(8)
        cr.stroke()
    ribbon(cr, t, at(80, "El Alamein") - 0.1, "EL ALAMEIN", 70, 990, size=44, color="allies",
           sub=None)


# ================================================================ C4-S10 (81): Stalingrad
SKY10 = sets.Sky(mode="dusk", horizon=700, clouds=3, seed=10)
RUIN = things.RuinedSkyline(x=W / 2, y=700, scale=1.0, width=2300, color="#5c564b")
VOLGA = sets.Ocean(horizon=760, color="#8fa29c")


def s_stalingrad(cr, t, t0, t1):
    lt = t - t0
    s0, s1 = sentences(81)
    cr.save()
    camera(cr, push_in(t, t0, t1, 1.0, 1.08), W / 2, H / 2 + 40)
    SKY10.draw(cr, t)
    for k, (x, h) in enumerate(((300, 520), (760, 640), (1240, 560), (1620, 480))):
        props.smoke(cr, x, 640, lt + k, height=h, width=110, color="#4f4a42", rate=2.5, life=5.0, seed=k + 20)
    RUIN.draw(cr, t)
    cr.rectangle(-300, 690, W + 600, 70)                         # the river bank
    cr.set_source_rgba(*col("#4b453c"))
    cr.fill()
    VOLGA.draw(cr, t)
    for k in range(7):                                         # guns flashing inside the city
        tk = 0.4 + k * 0.85
        if lt >= tk and lt - tk < 0.5:
            fx.starburst(cr, 200 + (k * 523) % 1500, 520 + (k * 97) % 140, lt - tk, size=0.4, seed=k)
    text(cr, "VOLGA", 1500, 905, 40, font=STENCIL, color="ink_soft", spacing=10)
    cr.restore()
    m0 = at(81, "named after Stalin")                           # Stalin's medallion
    if t >= m0 - 0.2:
        u = back_out(seg(t, m0 - 0.2, m0 + 0.15))
        mx, my, r = 1600, 300, 190
        cr.save()
        cr.translate(mx, my)
        cr.scale(u, u)
        cr.translate(-mx, -my)
        cr.arc(mx + 10, my + 10, r, 0, 2 * math.pi)
        cr.set_source_rgba(*col("ink", 0.8))
        cr.fill()
        cr.save()
        cr.arc(mx, my, r, 0, 2 * math.pi)
        cr.clip()
        cr.set_source_rgba(*col("paper"))
        cr.paint()
        rays(cr, t, mx, my, n=20, color="gold", alpha=0.45, spin=0.04)
        heads.portrait(cr, t, "stalin", mx, my + r + 30, height=440, expr="determined", turn=0.35)
        cr.restore()
        cr.arc(mx, my, r, 0, 2 * math.pi)
        cr.set_source_rgba(*col("gold"))
        cr.set_line_width(14)
        cr.stroke_preserve()
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(5)
        cr.stroke()
        cr.restore()
        ribbon(cr, t, m0 + 0.2, "STALIN", mx + 120, my + r + 20, size=34, color="soviet", align="right")
    if t >= s1.start - 0.15:                                   # STALINGRAD zooms up as slab type
        u = ease_out(seg(t, s1.start - 0.15, s1.start + 0.5))
        bw = ease_out(seg(t, s1.start - 0.15, s1.start + 0.2))
        cr.rectangle(0, 790, W * bw, 220)
        cr.set_source_rgba(*col("soviet"))
        cr.fill()
        halftone(cr, rect_path(0, 930, W * bw, 80), "ink", density=2, alpha=0.3)
        cr.move_to(0, 790)
        cr.line_to(W * bw, 790)
        cr.move_to(0, 1010)
        cr.line_to(W * bw, 1010)
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(7)
        cr.stroke()
        cr.save()
        cr.translate(W / 2, 900)
        cr.scale(0.3 + 0.7 * u, 0.3 + 0.7 * u)
        text(cr, "STALINGRAD", 0, 62, 176, font=SLAB, color="cream", bold=False, outline="ink", outline_w=12,
             spacing=6, alpha=min(1.0, 3 * u))
        cr.restore()


# ================================================================ C4-S11 (82): every floor
BLOCK = things.BuildingSection(x=W / 2, y=1000, scale=1.15)
RUIN_FAR = things.RuinedSkyline(x=W / 2, y=1000, scale=0.8, width=3000, color="#8a8274", smoke=False)
GUNS = []
# (stick.blend leaves "aim" None between a pose without it and "fire"; give the cover poses explicit zeros)
DUCK = dict(stick.POSES["duck"], aim=0.0, flash=0.0)
CROUCH = dict(stick.POSES["crouch"], aim=0.0, flash=0.0)


def _setup_s11():
    r = random.Random(4)
    for i, fy in enumerate(BLOCK.floors):
        for side, dx, face in (("soviet", -250, 1), ("germany", 250, -1)):
            if (i + (side == "germany")) % 2 == 0 or i == 0:
                f = Figure(nation=side, x=BLOCK.o["x"] + dx * BLOCK.o["scale"],
                           y=BLOCK.o["y"] + fy * BLOCK.o["scale"], scale=0.5, facing=face, seed=30 + i * 2 + face,
                           prop="rifle")
                GUNS.append((f, r.uniform(0, 1.2)))


_setup_s11()


def s_floors(cr, t, t0, t1):
    lt = t - t0
    up = [at(82, "every street"), at(82, "every building"), at(82, "every floor")]
    k = 0.0
    for i, ti in enumerate(up):                                 # the tilt rises in three steps, one per phrase
        k += smooth(seg(t, ti - 0.2, ti + 0.6)) / 3
    cr.save()
    camera(cr, 1.28 - 0.1 * k, W / 2, lerp(930, 470, k))
    SKY10.draw(cr, t)
    RUIN_FAR.draw(cr, t)
    cr.rectangle(-500, 1000, W + 1000, 500)
    cr.set_source_rgba(*col("#6e6556"))
    cr.fill()
    BLOCK.draw(cr, t)
    for f, ph in GUNS:                                          # duck, pop up, fire (muzzle flash only), duck
        cs = t - ((lt + ph) % 2.4)                             # this cycle's start (episode time)
        f.draw(cr, t, [(cs - 0.01, DUCK), (cs + 1.1, CROUCH), (cs + 1.45, "fire"), (cs + 2.4, DUCK)])
    for i, x in enumerate((120, 380, 1560, 1820)):              # dust and smoke in the street, either side
        props.smoke(cr, x, 1000, lt + i, height=240, width=60, color="#7d7466", rate=2.0, life=3.0, seed=40 + i)
    cr.restore()


# ================================================================ C4-S12 (83): the ring closes
S12 = {}


def _setup_s12(t0, t1):
    m = Map("europe", era="1941")
    d = t1 - t0
    m.zone("ussr_occupied_1942", -9, -8.5)
    m.front("case_blue_1942", -20, -10)
    m.camera_key(0.0, (43.6, 49.0), 4.6)
    m.camera_key(d, (43.9, 48.85), 6.4)
    a0 = at(83, "surround") - t0 - 0.6
    m.arrows("stalingrad_uranus", a0, a0 + 1.4, stagger=0.15, width=120)
    m.zone("stalingrad_ring", a0 + 1.1, a0 + 2.2)
    m.city("Stalingrad", 0.1, size=40)
    m.label("GERMAN 6TH ARMY", a0 + 2.0, lonlat=(43.1, 49.75), size=40)
    m.label("SOVIET UNION", 0.2, lonlat=(46.0, 50.6), size=44)
    S12.update(m=m, a0=a0)


def s_ring(cr, t, t0, t1):
    paper(cr)
    S12["m"].draw(cr, t - t0)
    stamp(cr, t, t0 + S12["a0"] + 2.3, "SURROUNDED", 1300, 900, size=76, tilt=-0.06)


# ================================================================ C4-S13 (84): no retreat
HITLER_SLAM = Figure(leader="hitler", x=700, y=1400, scale=2.7, facing=1, seed=6)


def s_slam(cr, t, t0, t1):
    hit = at(84, "forbids") + 0.05
    sx, sy = shake(t, hit, amp=10)
    sy += 18 * math.exp(-14 * (t - hit)) * math.cos(30 * (t - hit)) if t >= hit else 0.0   # a camera bump on impact
    paper(cr)
    cr.save()
    cr.translate(sx, sy)
    camera(cr, push_in(t, t0, t1, 1.0, 1.06), W / 2, H / 2 + 30)
    rays(cr, t, 820, 420, n=28, color="ink", alpha=0.13, spin=0.02)
    windup = dict(lean=0.2, nod=0.1, sh_n=2.3, el_n=1.6, hand_n="fist", turn=0.4,   # fist up by the head, elbow bent
                  face={"brow": "angry", "mouth": "grit"})
    down = dict(lean=0.4, nod=0.25, sh_n=0.3, el_n=1.05, hand_n="fist", turn=0.4,    # the fist DOWN on the table,
                face={"brow": "angry", "mouth": "grit"})                              # elbow bent
    track = [(t0, dict(turn=0.45, face={"brow": "angry", "mouth": "grit"})), (hit - 0.3, windup), (hit, down)]
    HITLER_SLAM.draw(cr, t, track)
    cr.rectangle(-300, 860, W + 600, 400)                       # the map table
    cr.set_source_rgba(*col("#5a3f29"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(6)
    cr.stroke()
    cr.save()
    cr.translate(1250, 885)
    cr.rotate(-0.04 + (0.03 * math.exp(-8 * (t - hit)) * math.sin(40 * (t - hit)) if t > hit else 0))
    cr.rectangle(-330, -40, 660, 120)
    cr.set_source_rgba(*col("land"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(4)
    cr.stroke()
    cr.move_to(-250, 10)
    cr.curve_to(-120, -20, 40, 40, 240, 0)
    cr.set_source_rgba(*col("soviet"))
    cr.set_line_width(9)
    cr.stroke()
    cr.restore()
    halftone(cr, rect_path(-300, 900, W + 600, 300), "ink", density=2, alpha=0.35)
    cr.restore()
    stamp(cr, t, hit + 0.08, "NO RETREAT", 1390, 230, size=110, tilt=-0.08)


# ================================================================ C4-S14 (85): the white flag
SKY14 = sets.Sky(mode="day", horizon=720, clouds=0, seed=14)
RUIN14 = things.RuinedSkyline(x=W / 2, y=720, scale=0.9, width=2600, color="#a49c8c", smoke=True)
FLAG = things.WhiteFlag(x=1080, y=880, scale=1.75, wind=0.8)


def _snowfield(cr, t, horizon):
    SKY14.draw(cr, t)
    cr.rectangle(-500, -500, W + 1000, horizon + 500)            # winter: wash the sky pale
    cr.set_source_rgba(*col("snow", 0.45))
    cr.fill()
    RUIN14.draw(cr, t)
    for y, c in ((horizon, "#e9e3d3"), (horizon + 90, "#f1ebdc"), (horizon + 230, "snow")):
        cr.move_to(-500, y)
        for i in range(30):
            cr.line_to(-500 + i * 110, y + 18 * math.sin(i * 0.7 + y * 0.01))
        cr.line_to(W + 500, H + 500)
        cr.line_to(-500, H + 500)
        cr.close_path()
        cr.set_source_rgba(*col(c))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink", 0.3))
        cr.set_line_width(3)
        cr.stroke()


def s_flag(cr, t, t0, t1):
    cr.save()
    camera(cr, push_in(t, t0, t1, 1.0, 1.07), W / 2 + 120, H / 2 + 20)
    _snowfield(cr, t, 720)
    cr.move_to(780, 900)                                        # the rubble mound the flag stands in
    cr.curve_to(880, 800, 1300, 790, 1420, 910)
    cr.close_path()
    cr.set_source_rgba(*col("#cfc7b4"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(5)
    cr.stroke()
    FLAG.draw(cr, t)
    cr.restore()
    props.snowfall(cr, t, density=220, wind=-60)
    s = at(85, "surrender") - 0.1
    if t >= s:
        a = ease_out(seg(t, s, s + 0.5))
        text(cr, "2 FEBRUARY 1943", W / 2, 1000, 64, font=STENCIL, color="ink", spacing=10, alpha=a,
             outline="paper", outline_w=6)


# ================================================================ C4-S15 (86): the prisoners
def s_prisoners(cr, t, t0, t1):
    lt = t - t0
    cr.save()
    camera(cr, push_in(t, t0, t1, 1.0, 1.06), lerp(W / 2 + 60, W / 2 - 60, smooth(seg(t, t0, t1))), H / 2)
    _snowfield(cr, t, 600)
    sp.prisoner_line(cr, lt + 3.0, nation="germany", ground=1010, horizon=600, n=18, scale=0.62, snow=False)
    cr.restore()
    props.snowfall(cr, t, density=200, wind=-40)
    c0 = at(86, "ninety-one thousand") - 0.1
    if t >= c0:
        cr.rectangle(1140, 90, 700, 250)
        cr.set_source_rgba(*col("paper", 0.92))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(6)
        cr.stroke()
    counter(cr, t, c0, c0 + 1.4, 91000, 1490, 260, size=150, color="ink")
    if t >= c0 + 0.3:
        text(cr, "TAKEN PRISONER", 1490, 318, 40, font=STENCIL, color="alert", spacing=6,
             alpha=ease_out(seg(t, c0 + 0.3, c0 + 0.7)))


# ================================================================ the shot list on the clock
def _shots():
    a, b = SPAN
    card0, card1 = T.chapter("C4").card
    s77, s78 = sentences(77), at(78, "and in about five minutes")
    seq = [
        ("roosevelt", a, cut(70, 71), s_roosevelt, "DEC 1941"),
        ("hitler", cut(70, 71), cut(71, 72), s_hitler_atlantic, "DEC 1941"),
        ("worldwar", cut(71, 72), cut(72, 73), s_world_war, "DEC 1941"),
        ("axis", cut(72, 73), cut(73, 74), s_axis, "DEC 1941"),
        ("allies", cut(73, 74), card0, s_allies, "DEC 1941"),
        ("card", card0, card1, s_card, None),
        ("axispeak", card1, cut(75, 76), s_axis_peak, "EARLY 1942"),
        ("sweep", cut(75, 76), cut(76, 77), s_sweep, "EARLY 1942"),
        ("codebreak", cut(76, 77), (s77[0].end + s77[1].start) / 2, s_codebreakers, "MAY 1942"),
        ("midway", (s77[0].end + s77[1].start) / 2, cut(77, 78), s_midway, "MAY 1942"),
        ("dive", cut(77, 78), s78 - 0.05, s_dive, "JUNE 1942"),
        ("carriers", s78 - 0.05, cut(78, 79), s_carriers, "JUNE 1942"),
        ("lost", cut(78, 79), cut(79, 80), s_lost, "JUNE 1942"),
        ("alamein", cut(79, 80), cut(80, 81), s_alamein, "NOV 1942"),
        ("stalingrad", cut(80, 81), cut(81, 82), s_stalingrad, "AUG 1942"),
        ("floors", cut(81, 82), cut(82, 83), s_floors, "AUG 1942"),
        ("ring", cut(82, 83), cut(83, 84), s_ring, "NOV 1942"),
        ("slam", cut(83, 84), cut(84, 85), s_slam, "NOV 1942"),
        ("flag", cut(84, 85), cut(85, 86), s_flag, "FEB 1943"),
        ("prisoners", cut(85, 86), b, s_prisoners, "FEB 1943"),
    ]
    return seq


SHOTS = _shots()
SHOTS_BY = {name: (t0, t1) for name, t0, t1, _f, _d in SHOTS}
_setup_s17(*SHOTS_BY["hitler"])
_setup_s18(*SHOTS_BY["worldwar"])
_setup_s02(*SHOTS_BY["axispeak"])
_setup_s03(*SHOTS_BY["sweep"])
_setup_s05(*SHOTS_BY["midway"])
_setup_s09(*SHOTS_BY["alamein"])
_setup_s12(*SHOTS_BY["ring"])


def draw(cr, t):
    """One complete frame at episode time t (inside package_span("P5"))."""
    prev = None
    for name, t0, t1, fn, date in SHOTS:
        if t < t1 or name == SHOTS[-1][0]:
            fn(cr, t, t0, t1)
            if date:
                date_stamp(cr, t, date, start=t0 if date != prev else -1e9)
            break
        prev = date or prev
    print_finish(cr, t)


def cues(T=T):
    """[(episode_time, sfx_name, gain_db, pan)] for the mix (sound.SFX names; "fanfare" is sound.MUSIC's newsreel
    fanfare for the chapter card, as PACKAGES.md asks)."""
    s = SHOTS_BY
    out = [(s["roosevelt"][0] + 0.1, "radio_static", -14, 0.3),
           (at(70, "declares war"), "stamp", -6, 0.3),
           (at(71, "declares war") - 0.2, "gun_boom", -10, 0.0),
           (S17["war"] + s["hitler"][0] + 1.5, "stamp", -6, -0.3)]
    out += [(s["worldwar"][0] + 0.15 + i * 0.22 * 3, "explosion", -16, -0.6 + 0.4 * i) for i in range(4)]
    out += [(at(73, w) - 0.15, "page_whoosh", -12, -0.6 + 0.6 * k) for k, w in enumerate(("Germany", "Italy", "Japan"))]
    out += [(at(74, w) - 0.15, "page_whoosh", -12, -0.7 + 0.45 * k)
            for k, w in enumerate(("Britain", "the Soviet Union", "the United States", "China"))]
    out += [(T.chapter("C4").card[0], "page_whoosh", -8, 0.0), (T.chapter("C4").card[0] + 0.2, "fanfare", -4, 0.0)]
    out += [(at(75, "the Axis") - 0.2, "page_whoosh", -12, 0.0), (at(75, "unstoppable"), "stamp", -8, 0.4),
            (at(76, "sweeps") - 0.2, "artillery", -14, 0.2)]
    out += [(s["codebreak"][0] + 0.1, "morse", -12, -0.3), (s["codebreak"][0] + 0.6, "typewriter", -16, 0.4),
            (at(77, "Midway") - 0.05, "stamp", -6, 0.2), (at(77, "Midway") + 0.35, "stamp", -10, 0.4)]
    t0 = s["dive"][0]
    d = s["dive"][1] - t0
    out += [(t0 + d * 0.18 + k * 0.55, "dive_whine", -8, -0.4 + 0.4 * k) for k in range(3)]
    out += [(at(78, "three of them") + k * 0.45, "explosion", -4, -0.4 + 0.4 * k) for k in range(3)]
    out += [(at(79, "four") + 0.15 + k * 0.42, "stamp", -8, -0.6 + 0.4 * k) for k in range(4)]
    out += [(sentences(79)[1].start + 0.25, "stamp", -5, 0.0)]
    a0 = s["alamein"][0]
    out += [(a0 + 0.1, "tank", -10, 0.3)] + [(a0 + 0.9 + k * 0.7 + 2.2 * j, "gun_boom", -14, 0.2 * k)
                                             for k in range(3) for j in range(3)]
    out += [(s["stalingrad"][0] + 0.1, "artillery_barrage", -12, 0.0), (sentences(81)[1].start, "stamp", -10, 0.0)]
    out += [(s["floors"][0] + 0.2 + k * 0.8, "rifle_crack", -18, -0.5 + 0.25 * (k % 5)) for k in range(8)]
    out += [(at(83, "surround") - 0.6, "tank", -10, 0.0), (s["ring"][0] + S12["a0"] + 2.3, "stamp", -6, 0.3)]
    out += [(at(84, "forbids") + 0.05, "door_slam", -4, 0.0), (at(84, "forbids") + 0.13, "stamp", -6, 0.3)]
    out += [(s["flag"][0] + 0.05, "blizzard", -12, 0.0), (s["prisoners"][0] + 0.05, "blizzard", -14, 0.0)]
    return sorted(out)
