"""WW2 Episode 1, package P1 (helper 10): lines 1-16, the cold open in Danzig to Hitler's dictatorship.

Shots (SHOTLIST.md C0-S01 ... C1-S13), every one placed relative to the episode clock (timing.json via Timing()):

    C0-S01  1   night harbour, low angle up the battleship's bow; the dock clock ticks to 4:45      1 SEPT 1939
    C0-S02  2   the turret swings across frame toward the fort
    C0-S03  2   across the water: tiny guards on the Westerplatte wall look up
    C0-S04  3   "And fires.": the muzzle star-burst, halftone smoke, shake, smash to black (silence)
    C0-S05  4   the world map; fire floods out from Poland, pull back                                 1939-1945
    C0-S06  5   a huge counter races to 60-85 MILLION over the darkening world
    C0-S07  6   a distant skyline; one white flash wipes it to paper
    C0-S08  7   the title poster WORLD WAR II 1939-1945 on gold rays; C0-S09 the subtitle strip
    C1-S01  8   CHAPTER 1 THE BROKEN PEACE; the calendar flips back 1939 -> 1919                       1919
    C1-S02  9   a tired German soldier lowers his rifle against grey rays                             NOV 1918
    C1-S03  10  the long signing table, the German delegate alone; C1-S04 the four treaty stamps      JUNE 1919
    C1-S05  11  a crowd, heads bowed, a newspaper strip
    C1-S06  12  the poster stock chart plunges (1929); C1-S07 coins drain off the world map           OCT 1929
    C1-S08  13  the jobless queue in profile; counter 6,000,000                                         1932
    C1-S09  14  low-angle podium, the speaker's shadow grows on the wall; C1-S10 the rally crowd
    C1-S11  15  Hitler poster portrait (heads.portrait), name strip                                     1933
    C1-S12  16  the parliament silhouette, JAN 1933; C1-S13 a giant padlock snaps across the doors    JAN 1933

Rules (PACKAGES.md / STYLE.md): poster look, push-in on every shot, a date tag, no symbols, no red rays, no gore.
Sound: cues(T) for helper 7's mix.
"""
import math
import random

from channels.ww2.kit.core import *  # noqa: F401,F403
from channels.ww2.kit.core import (FPS, H, W, LABEL, SLAB, STENCIL, TITLE, back_out, cairo, camera, chapter_card,
                                   clamp01, col, counter, date_stamp, ease_in, ease_out, halftone, lerp, paper,
                                   print_finish, push_in, rays, seg, shake, smooth, text)
from channels.ww2.ep01.timing import Timing
from channels.ww2.kit import fx, heads, props, sets, setpieces, stick, things

T = Timing()


def L(i):
    return T.line(str(i))


def S(i, k):
    return T.sentence(str(i), k)


def word_t(i, word, frac=0.0):
    """When `word` is said in line i (estimated from its position in the text: no word-level timing)."""
    ln = L(i)
    k = ln.text.lower().find(word.lower())
    if k < 0:
        return ln.start
    return ln.start + (ln.dur * (k + frac * len(word)) / max(1, len(ln.text)))


# ---------------------------------------------------------------- the props (made once)
SHIP = props.Battleship(side="germany", length=760.0, smoke=True)
TURRET = things.TurretCloseup(side="germany")
FORT = things.FortWall(length=900.0)
CLOCK = things.Clock()
SKY_N = sets.Sky(mode="night", horizon=780, clouds=3)
SEA_N = sets.Ocean(horizon=780, mode="night")
SKY_D = sets.Sky(mode="dusk", horizon=760, clouds=4)
CAL = props.Calendar()
CHART = things.Chart()
PODIUM = things.Podium()
PARL = things.Parliament()
LOCK = things.Padlock()
TABLE = things.LongTable(length=1500.0, chairs=9)
ROOM = sets.SigningRoom(kind="hall", horizon=640)
SKYLINE = sets.Skyline(city="generic", ground=860, seed=21)
NEWS = things.Newspaper(masthead="EXTRA!", headline="PEACE SIGNED", sub="GERMANY ACCEPTS THE TERMS",
                        date="29 JUNE 1919")
_MAPS = {}


def _world_map():
    if "w" in _MAPS:
        return _MAPS["w"]
    from channels.ww2.kit.maps import Map
    m = Map("world", era="1939") if True else None
    _MAPS["w"] = m
    return m


# ---------------------------------------------------------------- shot helpers
def _frame(cr, t, t0, t1, z0=1.0, z1=1.07, cx=W / 2, cy=H / 2):
    """Enter a shot's camera: the slow push-in every shot carries."""
    cr.save()
    camera(cr, push_in(t, t0, t1, z0, z1), cx, cy)


def _flat_bg(cr, c="paper"):
    cr.save()
    cr.identity_matrix()
    if c == "paper":
        paper(cr)
    else:
        cr.set_source_rgba(*col(c))
        cr.paint()
    cr.restore()


def _strip(cr, t, start, s, y=H - 150, color="ink", fg="cream", size=58, dur=None):
    """A poster name/subtitle strip that slides in from the left."""
    if t < start or (dur is not None and t > start + dur + 0.3):
        return
    u = ease_out(seg(t, start, start + 0.35))
    a = 1.0 if dur is None else 1 - seg(t, start + dur, start + dur + 0.3)
    cr.save()
    cr.select_font_face(SLAB, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    w = cr.text_extents(s).x_advance + 80
    x = lerp(-w, W / 2 - w / 2, u)
    cr.rectangle(x, y - size * 0.95, w, size * 1.35)
    cr.set_source_rgba(*col(color, 0.95 * a))
    cr.fill()
    cr.restore()
    text(cr, s, x + w / 2, y, size, font=SLAB, color=fg, bold=False, alpha=a)


def _stamp(cr, t, start, word, x, y, size=110, color="alert", tilt=-0.08):
    """A rubber stamp that slams down (overshoot), with a slightly misregistered double print."""
    if t < start:
        return
    u = clamp01((t - start) / 0.16)
    s = lerp(2.2, 1.0, back_out(u, 1.6))
    a = min(1.0, u * 2)
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    cr.scale(s, s)
    cr.select_font_face(STENCIL, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    cr.set_font_size(size)
    w = cr.text_extents(word).x_advance
    cr.rectangle(-w / 2 - 26, -size * 0.92, w + 52, size * 1.18)
    cr.set_source_rgba(*col(color, 0.9 * a))
    cr.set_line_width(9)
    cr.stroke()
    cr.restore()
    cr.save()
    cr.translate(x, y)
    cr.rotate(tilt)
    cr.scale(s, s)
    text(cr, word, 3, 3, size, font=STENCIL, color=color, alpha=0.35 * a)
    text(cr, word, 0, 0, size, font=STENCIL, color=color, alpha=0.92 * a)
    cr.restore()


# ---------------------------------------------------------------- C0: the cold open (lines 1-7)
def s01_harbour(cr, t, t0, t1):
    """Night harbour, low angle up the battleship's bow; the dock clock ticks toward 4:45; the hook text."""
    _frame(cr, t, t0, t1, 1.0, 1.1, W * 0.55, H * 0.55)
    SKY_N.draw(cr, t)
    for i in range(46):                                           # stars
        r = random.Random(i)
        x, y = r.uniform(0, W), r.uniform(0, 600)
        tw = 0.5 + 0.5 * math.sin(t * r.uniform(1, 3) + i)
        cr.arc(x, y, r.uniform(1.2, 2.6), 0, 2 * math.pi)
        cr.set_source_rgba(*col("cream", 0.35 + 0.5 * tw))
        cr.fill()
    # the distant city across the harbour, a few lit windows
    sets.Skyline(city="generic", ground=790, night=True, lit=0.25, seed=5, floor=False).draw(cr, t)
    SEA_N.draw(cr, t)
    # the battleship from a low angle: big, bow toward the right, moving barely
    bob = 4 * math.sin(t * 0.9)
    SHIP.draw(cr, t, x=W * 0.86 - 40 * seg(t, t0, t1), y=840 + bob, scale=2.5, facing=-1,
              turrets=(0.0, 0.0, 180.0), elev=4.0, smoke=True)   # bow to the left, gliding in
    # searchlight sweep from the ship over the water
    props.beam(cr, W * 0.62, 520 + bob, math.pi + 0.3 + 0.15 * math.sin(t * 0.5), length=1700, width=120,
               alpha=0.16)
    # the dock clock in the foreground: a post and the face, ticking 4:44:50 -> 4:45
    cr.restore()
    cr.save()
    camera(cr, push_in(t, t0, t1, 1.0, 1.08), W * 0.5, H * 0.5)
    cr.rectangle(W * 0.13 - 12, 420, 24, 900)                     # the dock clock's post, foreground left
    cr.set_source_rgba(*col("ink"))
    cr.fill()
    secs = 50 + (t - t0) * (10 / max(0.1, L(1).end - 0.8 - t0))   # reaches :00 just before the line ends
    h = 4 + (44 + min(60.0, secs) / 60.0) / 60.0
    CLOCK.draw(cr, t, x=W * 0.13, y=420, scale=0.95, hours=h)
    cr.restore()
    # the hook: big type over the frame
    s1 = S(1, 0) if len(T._lines["1"]["sentences"]) > 1 else L(1)
    _hook(cr, t, t0 - 0.4, "1 SEPTEMBER 1939", W * 0.6, 190, 104)   # full size on frame 0 (the hook)
    _hook(cr, t, S(1, 1).start - 0.1 if len(T._lines["1"]["sentences"]) > 1 else s1.start + 2.5, "4:45 AM",
          W * 0.6, 335, 120, color="fire")


def _hook(cr, t, start, s, x, y, size, color="cream"):
    if t < start:
        return
    u = max(0.02, back_out(clamp01((t - start) / 0.3), 1.4))
    cr.save()
    cr.translate(x, y)
    cr.scale(u, u)
    cr.select_font_face(TITLE, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(size)
    w = cr.text_extents(s).x_advance
    cr.rectangle(-w / 2 - 34, -size * 0.92, w + 68, size * 1.12)       # the ink plate (clear of the mast)
    cr.set_source_rgba(*col("ink", 0.92))
    cr.fill()
    text(cr, s, 0, 0, size, font=TITLE, color=color, bold=False)
    cr.restore()


def s02_turret(cr, t, t0, t1, fire_t=None):
    """Low heroic angle on the main turret; it swings across frame toward the fort (and fires on 'fires')."""
    _frame(cr, t, t0, t1, 1.0, 1.08, W / 2, H * 0.6)
    sets.Sky(mode="night", horizon=900, clouds=4, seed=8).draw(cr, t)
    rays(cr, t, W * 0.75, H * 0.9, n=24, color="cream", alpha=0.05)
    u = smooth(seg(t, t0 + 0.4, t0 + 3.6))
    ang = lerp(-58.0, 0.0, u)                                     # the barrels come round to aim right
    TURRET.draw(cr, t, x=W * 0.46, y=H * 0.98, scale=1.35, turret=ang, elev=lerp(4, 10, u),
                fire=(fire_t,) if fire_t else ())
    cr.restore()


def s03_fort(cr, t, t0, t1):
    """Across the water: the Westerplatte wall and its tiny guards; they look up toward the ship."""
    _frame(cr, t, t0, t1, 1.0, 1.06, W / 2, H * 0.62)
    sets.Sky(mode="night", horizon=700, clouds=3, seed=4).draw(cr, t)
    cr.rectangle(-200, 640, W + 400, 120)                         # the low dark shore
    cr.set_source_rgba(*col("#2a2c30"))
    cr.fill()
    FORT.draw(cr, t, x=W * 0.52, y=700, scale=1.15, lit=True)
    sets.Ocean(horizon=760, mode="night").draw(cr, t)
    for i, gx in enumerate((W * 0.38, W * 0.47, W * 0.62)):       # tiny poster-silhouette guards
        f = stick.Figure(civilian="flatcap", x=gx, y=598, scale=0.36, facing=-1 if i == 2 else 1, seed=40 + i,
                         color="#3c4a3a")
        look_t = t0 + 1.2 + i * 0.25
        f.draw(cr, t, [(0.0, "idle"), (look_t, "stand")], face={"look": (0.0, -1.0)} if t > look_t else None)
    # the ship's dark mass at the far right, its searchlight finding the wall
    props.beam(cr, W + 60, 520, math.pi - 0.18 + 0.05 * math.sin(t), length=1500, width=140, alpha=0.2)
    cr.restore()


def s04_fires(cr, t, t0, t1, fire_t):
    """'And fires.': the turret fires toward the camera's right; a full-frame star burst, smoke, shake."""
    if t < fire_t:
        s02_turret(cr, t, t0 - 3.0, t1, fire_t=None)
        return
    dx, dy = shake(t, fire_t, dur=0.6, amp=26.0, seed=3)
    cr.save()
    cr.translate(dx, dy)
    s02_turret(cr, t, t0 - 3.0, t1, fire_t=fire_t)
    age = t - fire_t
    fx.starburst(cr, W * 0.82, H * 0.48, age, size=4.2, seed=2, life=0.7)
    for k in range(5):
        fx.puff(cr, W * 0.7 + k * 70, H * 0.5 + (k % 2) * 40, age - 0.05 * k, size=2.4, seed=k, life=2.6)
    cr.restore()
    fx.flash(cr, t, fire_t, hold=0.05, fade=0.25, color="white")


def s05_world(cr, t, t0, t1):
    """The world map: the war's fire floods out from Poland; a slow pull back."""
    m = _world_map()
    if not getattr(m, "_p1", False):
        m._p1 = True
        m.camera_key(t0, (19.0, 50.0), 3.2)
        m.camera_key(t0 + 4.0, (25.0, 35.0), 1.25)
        m.camera_key(t1 + 6.0, (25.0, 30.0), 1.1)
        o = (19.0, 52.0)
        neutral = {"che", "swe", "esp", "prt", "irl", "afg", "sau", "yem", "arg", "chl", "atf", "ata"}
        for r in sorted(m._side):                                 # the war's fire spreads out from Poland
            if r not in neutral:
                m.side(r, t0 + 0.3, "fire", origin=o, dur=4.4, occupied=False)
    m.draw(cr, t)


def s06_counter(cr, t, t0, t1):
    """The counter races to 85 million over the darkening world; then the 60-85 MILLION range card."""
    s05_world(cr, t, t0 - 5.0, t1)
    cr.save()
    cr.rectangle(0, 0, W, H)
    cr.set_source_rgba(*col("ink", 0.45 * smooth(seg(t, t0, t0 + 1.2))))
    cr.fill()
    cr.restore()
    z = push_in(t, t0, t1, 1.0, 1.08)
    cr.save()
    cr.translate(W / 2, H / 2)
    cr.scale(z, z)
    cr.translate(-W / 2, -H / 2)
    if t < t0 + 2.6:
        counter(cr, t, t0 + 0.1, t0 + 2.4, 85_000_000, W / 2, H * 0.56, size=230, color="cream")
    else:
        u = max(0.02, back_out(clamp01((t - t0 - 2.6) / 0.3), 1.5))
        cr.save()
        cr.translate(W / 2, H * 0.5)
        cr.scale(u, u)
        text(cr, "60-85", 0, 40, 260, font=TITLE, color="cream", bold=False, outline="ink", outline_w=20)
        text(cr, "MILLION DEAD", 0, 170, 96, font=SLAB, color="fire", bold=False, outline="ink", outline_w=10)
        cr.restore()
    cr.restore()


def s07_city(cr, t, t0, t1, flash_t):
    """A distant city skyline at dusk; one white flash wipes it to bare paper."""
    _frame(cr, t, t0, t1, 1.0, 1.06)
    if t < flash_t + 0.15:
        SKY_D.draw(cr, t)
        rays(cr, t, W / 2, 860, n=28, color="gold", alpha=0.12)
        SKYLINE.draw(cr, t)
        props.Bomber(side="usa").draw(cr, t, x=lerp(-200, W * 0.56, seg(t, t0, flash_t)), y=180, scale=0.32,
                                      facing=1) if t < flash_t else None
    else:
        paper(cr)                                                 # the city is gone: only the paper and a faint line
        fx.mushroom(cr, W / 2, 860, t, flash_t + 0.2, size=0.55, seed=7)   # a flat poster cloud rising far away
        cr.move_to(-100, 860)
        cr.line_to(W + 100, 860)
        cr.set_source_rgba(*col("ink", 0.6))
        cr.set_line_width(4)
        cr.stroke()
    cr.restore()
    fx.flash(cr, t, flash_t, hold=0.25, fade=1.4, color="white")


def s08_title(cr, t, t0, t1, sub_t):
    """The title poster: WORLD WAR II on gold rays, 1939-1945 stamps in; the subtitle strip slides in."""
    _frame(cr, t, t0, t1 + 4, 1.0, 1.08)
    paper(cr)
    rays(cr, t, W / 2, H * 0.48, n=32, color="gold", alpha=0.3, spin=0.04)
    u = max(0.02, back_out(clamp01((t - t0) / 0.35), 1.3))
    cr.save()
    cr.translate(W / 2, H * 0.44)
    cr.scale(u, u)
    text(cr, "WORLD WAR II", 0, 40, 168, font=SLAB, color="alert", bold=False, outline="ink", outline_w=14, spacing=2)
    cr.restore()
    if t > t0 + 0.6:
        _stamp(cr, t, t0 + 0.6, "1939 - 1945", W / 2, H * 0.66, size=96, color="ink", tilt=-0.03)
    cr.restore()
    _strip(cr, t, sub_t, "20 YEARS AFTER THE WAR TO END ALL WARS", y=H - 110, size=54)


# ---------------------------------------------------------------- C1: the broken peace (lines 8-16)
def s_card(cr, t, t0, t1, card, cal_t):
    """CHAPTER 1 THE BROKEN PEACE, then the calendar flips back 1939 -> 1919."""
    _frame(cr, t, t0, t1, 1.0, 1.05)
    paper(cr)
    rays(cr, t, W / 2, H / 2, n=28, color="khaki", alpha=0.16)
    n, dur = 20, 1.4
    k = min(n, int(clamp01((t - cal_t) / dur) * n)) if t >= cal_t else 0      # 1939 -> 1919, a page a year
    prev = ("SEPT", "1", str(1939 - k + 1)) if 0 < k else None
    CAL.draw(cr, t, x=W / 2, y=H / 2 + 20, scale=1.8, date=("JAN", "1", str(1939 - k)) if k < n else
             ("JUNE", "28", "1919"), prev=prev, flip_at=cal_t + (k / n) * dur if k else None,
             flip_dur=dur / n if k < n else 0.28)
    cr.restore()
    if card:
        chapter_card(cr, t, card[0], 1, "The broken peace", dur=card[1] - card[0])


def s09_soldier(cr, t, t0, t1):
    """A tired German soldier of 1918 (flared helmet, charcoal) lowers his rifle against grey rays."""
    _frame(cr, t, t0, t1, 1.0, 1.08, W / 2, H * 0.62)
    paper(cr)
    rays(cr, t, W / 2, H * 0.95, n=26, color="ink", alpha=0.14)
    fx.mud(cr, t, -100, W + 100, 900, depth=200)
    props.BarbedWire().draw(cr, t, x=W * 0.2, y=900, scale=1.1)
    props.BarbedWire().draw(cr, t, x=W * 0.83, y=905, scale=0.9)
    f = stick.Figure(nation="germany", x=W * 0.5, y=940, scale=1.8, facing=1, seed=9, prop=None)
    f.draw(cr, t, [(t0, "stand"), (t0 + 1.4, "head_down")], face={"name": "sad"})
    cr.restore()


def s10_signing(cr, t, t0, t1):
    """The Hall of Mirrors as a long signing table: the winners in silhouette, the German delegate alone, signing."""
    u = smooth(seg(t, t0, t1))
    _frame(cr, t, t0, t1, 1.12, 1.55, lerp(W * 0.55, W * 0.76, u), lerp(H * 0.62, H * 0.74, u))
    ROOM.draw(cr, t)
    TABLE.draw(cr, t, x=W * 0.5, y=880, scale=1.0)
    for i, (x, who) in enumerate(((W * 0.24, "churchill"), (W * 0.36, None), (W * 0.5, None), (W * 0.64, None))):
        f = stick.Figure(civilian="hat" if i % 2 else None, x=x, y=760, scale=0.62, facing=1, seed=60 + i,
                         color="#3a3e4c")
        f.draw(cr, t + i * 0.3, [(0.0, "arms_crossed" if i % 2 else "stand")])
    g = stick.Figure(civilian=None, x=W * 0.83, y=930, scale=0.85, facing=-1, seed=71, prop="pen")
    g.draw(cr, t, [(0.0, "stand"), (t0 + 1.0, "sign")], face={"name": "sad"})
    cr.restore()


def s11_stamps(cr, t, t0, t1, stamps):
    """The treaty page fills the frame; four stamps thump in on their words."""
    _frame(cr, t, t0, t1 + 1, 1.0, 1.05)
    paper(cr)
    cr.save()
    cr.translate(W / 2, H / 2 + 20)
    cr.rotate(-0.02)
    cr.rectangle(-560, -470, 1120, 960)
    cr.set_source_rgba(*col("white"))
    cr.fill_preserve()
    cr.set_source_rgba(*col("ink"))
    cr.set_line_width(5)
    cr.stroke()
    text(cr, "TREATY OF PEACE", 0, -380, 74, font=SLAB, bold=False)
    text(cr, "VERSAILLES  ·  28 JUNE 1919", 0, -318, 30, font=LABEL, color="ink_soft")
    for k in range(13):
        y = -250 + k * 46
        cr.move_to(-460, y)
        cr.line_to(460 - (k * 37 % 160), y)
        cr.set_source_rgba(*col("ink_soft", 0.45))
        cr.set_line_width(5)
        cr.stroke()
    cr.restore()
    spots = ((W * 0.33, H * 0.36, -0.1), (W * 0.67, H * 0.44, 0.07), (W * 0.36, H * 0.68, 0.05),
             (W * 0.66, H * 0.76, -0.08))
    for (word, st), (x, y, tl) in zip(stamps, spots):
        _stamp(cr, t, st, word, x, y, size=104, tilt=tl)
    cr.restore()


def s12_crowd(cr, t, t0, t1):
    """A crowd in silhouette, heads bowed; a newspaper strip spins in."""
    _frame(cr, t, t0, t1, 1.0, 1.06)
    paper(cr)
    rays(cr, t, W / 2, H * 1.1, n=24, color="ink", alpha=0.08)
    stick.crowd(cr, t, 34, 0, W, 640, 1000, scale=0.62, pose="head_down", seed=12, tone="ink_soft")
    u = clamp01((t - t0 - 0.3) / 0.7)
    NEWS.draw(cr, t, x=W * 0.74, y=H * 0.35, scale=0.8, spin=u)
    cr.restore()


def s13_chart(cr, t, t0, t1, crash_t):
    """The poster stock chart climbs, then plunges off the bottom on 'crashes'; the camera follows it down."""
    follow = smooth(seg(t, crash_t, t1))
    _frame(cr, t, t0, t1, 1.05, 1.25, W / 2, lerp(H * 0.48, H * 0.66, follow))
    paper(cr)
    prog = lerp(0.3, 0.62, seg(t, t0, crash_t)) if t < crash_t else lerp(0.62, 1.0, ease_out(seg(t, crash_t,
                                                                                                 crash_t + 0.45)))
    CHART.draw(cr, t, x=W / 2, y=H / 2, scale=1.5, progress=prog, crash=0.62, label="1929")
    cr.restore()
    if t > crash_t:
        _stamp(cr, t, crash_t + 0.25, "CRASH!", W * 0.7, H * 0.25, size=120, tilt=-0.1)


NYC = (-74.0, 40.7)


def _depression_map(t0):
    if "d" in _MAPS and _MAPS["d"][1] == round(t0, 3):
        return _MAPS["d"][0]
    from channels.ww2.kit.maps import Map
    m = Map("world", era="1939")
    m.camera_key(t0, (-40.0, 38.0), 2.2)
    m.camera_key(t0 + 3.2, (10.0, 25.0), 1.12)
    for r in sorted(m._side):                                     # grey spreads out from the US
        m.side(r, t0 + 0.35, "#9b968b", origin=NYC, dur=2.6, occupied=False)
    m.city("WALL STREET", t0 + 0.1, lonlat=NYC, size=40)
    _MAPS["d"] = (m, round(t0, 3))
    return m


def s14_drain(cr, t, t0, t1):
    """The Depression spreads: the world greys out from a Wall Street pin while coins spill out of it and drain away
    off the map's edges."""
    m = _depression_map(t0)
    m.draw(cr, t)
    nx, ny = m.screen(m.xy(NYC))
    r = random.Random(4)
    for i in range(46):
        st = t0 + 0.2 + r.uniform(0, 2.4)
        age = t - st
        if age < 0:
            continue
        ang = r.uniform(-1.1, 1.3) if r.random() < 0.7 else r.uniform(1.6, 2.6)   # mostly east, over the Atlantic
        spd = r.uniform(420, 760)
        x = nx + math.cos(ang) * spd * age
        y = ny + math.sin(ang) * spd * age * 0.6 + 380 * age * age            # arcs, then falls off the edge
        if y > H + 40 or x > W + 40 or x < -40:
            continue
        things.coin(cr, x, y, 15, t * 9 + i)
    cr.arc(nx, ny, 14 + 6 * math.sin(t * 6), 0, 2 * math.pi)
    cr.set_source_rgba(*col("alert"))
    cr.fill()


def s15_queue(cr, t, t0, t1):
    """An endless jobless queue in profile (coats, flat caps); the camera pans along; counter 6,000,000."""
    pan = lerp(0, 520, smooth(seg(t, t0, t1)))
    _frame(cr, t, t0, t1, 1.0, 1.04)
    paper(cr)
    rays(cr, t, W / 2, H * 1.2, n=24, color="khaki", alpha=0.1)
    cr.save()
    cr.translate(-pan, 0)
    cr.rectangle(-200, 900, W + 1200, 300)
    cr.set_source_rgba(*col("khaki", 0.55))
    cr.fill()
    for i in range(12):
        r = random.Random(300 + i)
        f = stick.Figure(civilian=r.choice(["flatcap", "hat", "flatcap", "scarf"]), x=150 + i * 210, y=990,
                         scale=1.0, facing=-1, seed=300 + i)
        f.draw(cr, t + r.uniform(0, 3), [(0.0, r.choice(["head_down", "stand", "head_down"]))])
    cr.restore()
    cr.restore()
    counter(cr, t, t0 + 0.2, t1 - 0.3, 6_000_000, W / 2, H * 0.24, size=170, color="ink",
            label="JOBLESS IN GERMANY, 1932")


def s16_podium(cr, t, t0, t1):
    """A low-angle rostrum; the speaker (seen from behind) gestures and his shadow grows huge on the wall."""
    _frame(cr, t, t0, t1, 1.0, 1.1, W / 2, H * 0.62)
    paper(cr)
    cr.rectangle(-200, -200, W + 400, H * 0.86 + 200)
    cr.set_source_rgba(*col("#cfc3a5"))
    cr.fill()
    grow = smooth(seg(t, t0 + 0.6, t1))
    sh = stick.Figure(leader="hitler", x=W * 0.64, y=H * 0.86, scale=1.2 + 1.9 * grow, facing=-1, seed=81,
                      color="#a9997a")                            # his shadow on the wall, growing
    cr.save()
    cr.translate(0, -H * 0.04 * grow)
    sh.draw(cr, t, [(0.0, "slam_down"), (t0 + 1.6, "slam"), (t0 + 3.0, "slam_down")])
    cr.restore()
    PODIUM.draw(cr, t, x=W * 0.5, y=H * 0.98, scale=1.45)
    sp = stick.Figure(leader="hitler", x=W * 0.5, y=H * 0.98 + PODIUM.top_y * 1.45 + 6, scale=0.95, facing=-1,
                      seed=81)
    sp.draw(cr, t, [(0.0, "slam_down"), (t0 + 1.6, "slam"), (t0 + 3.0, "slam_down")])
    cr.restore()


def _poster_crowd(cr, t, rows=7, y0=560.0, y1=1120.0, seed=31):
    """A dense poster crowd filling the lower frame: rows of heads and shoulders packed shoulder to shoulder, looking
    up at the speaker, back rows smaller and paler; a few raised fists and hats (no straight-arm gestures)."""
    for row in range(rows):
        k = row / (rows - 1)                                      # 0 = back, 1 = front
        y = lerp(y0, y1, k)
        sz = lerp(22, 74, k)
        tone = stick._mix(col("ink_soft"), col("paper"), 0.55 * (1 - k))
        r = random.Random(seed * 100 + row)
        x = -sz * r.uniform(0.2, 1.2)
        while x < W + sz:
            bob = 3 * k * math.sin(t * 2.2 + x * 0.05)
            cr.save()
            cr.translate(x, y + bob)
            cr.move_to(-sz * 1.25, sz * 2.6)                      # shoulders
            cr.curve_to(-sz * 1.2, sz * 0.9, -sz * 0.7, sz * 0.75, 0, sz * 0.72)
            cr.curve_to(sz * 0.7, sz * 0.75, sz * 1.2, sz * 0.9, sz * 1.25, sz * 2.6)
            cr.close_path()
            cr.arc(0, -sz * 0.05, sz * 0.62, 0, 2 * math.pi)        # the head, tipped up
            cr.set_source_rgba(*tone)
            cr.fill()
            u = r.random()
            if u < 0.12:                                          # a raised fist (arm up, bent)
                cr.move_to(sz * 0.7, sz * 1.0)
                cr.line_to(sz * 0.95, -sz * 1.3)
                cr.set_line_width(sz * 0.36)
                cr.set_line_cap(cairo.LINE_CAP_ROUND)
                cr.set_source_rgba(*tone)
                cr.stroke()
                cr.arc(sz * 0.97, -sz * 1.45, sz * 0.3, 0, 2 * math.pi)
                cr.fill()
            elif u < 0.22:                                        # a hat
                cr.rectangle(-sz * 0.85, -sz * 0.55, sz * 1.7, sz * 0.16)
                cr.rectangle(-sz * 0.5, -sz * 1.05, sz * 1.0, sz * 0.55)
                cr.set_source_rgba(*stick._shade(tone, 0.25))
                cr.fill()
            cr.restore()
            x += sz * r.uniform(1.55, 1.95)


def _speaker_back(cr, t, x, y, s, raise_t):
    """Over the shoulder: the speaker's back of head and ear, collar, broad shoulders, one fist raised to the side."""
    ink, tone = col("#1f1c1b"), col("#1f1c1b")
    up = smooth(seg(t, raise_t, raise_t + 0.35)) - 0.6 * smooth(seg(t, raise_t + 1.6, raise_t + 2.0))
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ang = lerp(-0.25, -1.25, up)                                  # the raised arm swings up to the side (bent)
    ex, ey = 230 + 120 * math.cos(ang), -260 + 160 * math.sin(ang)
    cr.move_to(170, -230)
    cr.line_to(ex, ey)
    cr.line_to(ex + 40, ey - 150 * (0.4 + up))
    cr.set_line_width(70)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_source_rgba(*tone)
    cr.stroke()
    cr.arc(ex + 44, ey - 150 * (0.4 + up) - 30, 48, 0, 2 * math.pi)      # the fist
    cr.fill()
    cr.move_to(-330, 260)                                         # broad shoulders and back
    cr.curve_to(-330, -120, -260, -230, -110, -250)
    cr.line_to(110, -250)
    cr.curve_to(260, -230, 330, -120, 330, 260)
    cr.close_path()
    cr.fill()
    cr.rectangle(-70, -330, 140, 110)                              # the neck in the collar
    cr.fill()
    cr.save()                                                     # the back of the head: hair mass and an ear
    cr.translate(0, -440)
    cr.scale(1.0, 1.12)
    cr.arc(0, 0, 118, 0, 2 * math.pi)
    cr.restore()
    cr.fill()
    cr.save()
    cr.translate(118, -440)
    cr.scale(0.45, 0.75)
    cr.arc(0, 0, 50, 0, 2 * math.pi)
    cr.restore()
    cr.fill()
    cr.move_to(-150, -262)                                        # the collar's rim light
    cr.curve_to(-60, -236, 60, -236, 150, -262)
    cr.set_source_rgba(*col("cream", 0.55))
    cr.set_line_width(6)
    cr.stroke()
    cr.arc(0, -440, 121, math.pi * 1.15, math.pi * 1.65)         # a rim of light on the hair
    cr.set_source_rgba(*col("cream", 0.4))
    cr.set_line_width(5)
    cr.stroke()
    cr.restore()


def s17_rally(cr, t, t0, t1):
    """The rally seen over the speaker's shoulder: a packed poster crowd fills the lower half, looking up; ink rays
    (never red) behind."""
    _frame(cr, t, t0, t1, 1.0, 1.06)
    paper(cr)
    rays(cr, t, W * 0.55, H * 0.2, n=30, color="ink", alpha=0.14)
    _poster_crowd(cr, t)
    _speaker_back(cr, t, W * 0.14, H * 1.12, 0.9, t0 + 1.2)
    cr.restore()


def s18_portrait(cr, t, t0, t1):
    """Hitler poster portrait, 3/4 (heads.portrait) on khaki rays; the name strip ADOLF HITLER."""
    _frame(cr, t, t0, t1 + 0.6, 1.0, 1.1, W / 2, H * 0.5)
    paper(cr)
    rays(cr, t, W / 2, H * 0.36, n=28, color="khaki", alpha=0.28)
    heads.portrait(cr, t, "hitler", W / 2, H + 40, height=980, expr="determined", turn=0.42, seed=12)
    cr.restore()
    _strip(cr, t, t0 + 0.3, "ADOLF HITLER", y=H - 110, size=70, color="ink")


def s19_parliament(cr, t, t0, t1, lock_t):
    """The parliament building in silhouette at dusk; a giant padlock drops and snaps shut across its doors."""
    dx, dy = shake(t, lock_t, dur=0.5, amp=18.0, seed=5) if t >= lock_t else (0, 0)
    cr.save()
    cr.translate(dx, dy)
    _frame(cr, t, t0, t1, 1.0, 1.08, W / 2, H * 0.56)
    SKY_D.draw(cr, t)
    rays(cr, t, W / 2, H * 0.62, n=26, color="gold", alpha=0.14)
    PARL.draw(cr, t, x=W / 2, y=H * 0.88, scale=1.05, silhouette="#3a3632")
    cr.rectangle(-200, H * 0.88, W + 400, 400)
    cr.set_source_rgba(*col("#3a3632"))
    cr.fill()
    drop = ease_in(seg(t, lock_t - 0.45, lock_t))
    if t >= lock_t - 0.45:
        LOCK.draw(cr, t, x=W / 2, y=lerp(-200, H * 0.66, drop), scale=1.25, snap_at=lock_t + 0.05)
    cr.restore()
    cr.restore()


# ---------------------------------------------------------------- the edit
def _shots():
    """[(t_start, t_end, fn)] on the episode clock: every cut sits on a line, a sentence or a word."""
    L2, L3, L4, L5, L6, L7 = L(2), L(3), L(4), L(5), L(6), L(7)
    card = T.chapter("C1").card
    fort_cut = word_t(2, "turns its guns")
    fire_t = S(3, 0).end + 0.05                                    # BOOM right after "fires." (not over it)
    sh = [
        (0.0, L2.start - 0.05, s01_harbour),
        (L2.start - 0.05, fort_cut, s02_turret),
        (fort_cut, L3.start - 0.1, s03_fort),
        (L3.start - 0.1, fire_t + 0.85, lambda cr, t, a, b: s04_fires(cr, t, a, b, fire_t)),
        (fire_t + 0.85, max(L4.start - 0.25, fire_t + 0.9), None),   # silence: black
        (max(L4.start - 0.25, fire_t + 0.9), L5.start - 0.2, s05_world),
        (L5.start - 0.2, L6.start - 0.2, s06_counter),
        (L6.start - 0.2, L7.start - 0.4,
         lambda cr, t, a, b: s07_city(cr, t, a, b, word_t(6, "one bomb", 0.5))),
        (L7.start - 0.4, card[0], lambda cr, t, a, b: s08_title(cr, t, a, b, word_t(7, "just twenty"))),
        (card[0], L(9).start - 0.2, lambda cr, t, a, b: s_card(cr, t, a, b, card, L(8).start + 0.2)),
        (L(9).start - 0.2, L(10).start - 0.2, s09_soldier),
        (L(10).start - 0.2, word_t(10, "responsibility") - 0.35, s10_signing),
        (word_t(10, "responsibility") - 0.35, L(11).start - 0.2,
         lambda cr, t, a, b: s11_stamps(cr, t, a, b, [("RESPONSIBILITY", word_t(10, "responsibility", 0.6)),
                                                       ("LAND", word_t(10, "land", 0.6)),
                                                       ("ARMY", word_t(10, "army", 0.6)),
                                                       ("MONEY", word_t(10, "money", 0.6))])),
        (L(11).start - 0.2, L(12).start - 0.2, s12_crowd),
        (L(12).start - 0.2, max(word_t(12, "Great Depression") - 0.2, word_t(12, "crashes", 0.3) + 1.9),
         lambda cr, t, a, b: s13_chart(cr, t, a, b, word_t(12, "crashes", 0.3))),
        (max(word_t(12, "Great Depression") - 0.2, word_t(12, "crashes", 0.3) + 1.9), L(13).start - 0.2, s14_drain),
        (L(13).start - 0.2, L(14).start - 0.2, s15_queue),
        (L(14).start - 0.2, word_t(14, "and who blames"), s16_podium),
        (word_t(14, "and who blames"), L(15).start - 0.2, s17_rally),
        (L(15).start - 0.2, L(16).start - 0.2, s18_portrait),
        (L(16).start - 0.2, 1e9, lambda cr, t, a, b: s19_parliament(cr, t, a, b, word_t(16, "dictatorship", 0.2))),
    ]
    return sh


DATES = [  # (from shot index, tag)
    (0, "1 SEPT 1939"), (5, "1939 - 1945"), (8, None), (9, None), (10, "NOV 1918"), (11, "JUNE 1919"), (13, "1919"),
    (14, "OCT 1929"), (15, "1930"), (16, "1932"), (17, "1932"), (19, "1933"), (20, "JAN 1933"),
]


def draw(cr, t):
    shots = _shots()
    idx = max(i for i, (a, b, f) in enumerate(shots) if t >= a or i == 0)
    a, b, fn = shots[idx]
    if fn is None:
        cr.set_source_rgba(0, 0, 0, 1)
        cr.paint()
    else:
        fn(cr, t, a, b)
    tag = None
    for i, d in DATES:
        if idx >= i:
            tag = d
    if tag and fn is not None:
        date_stamp(cr, t, tag, start=a)
    print_finish(cr, t)


def cues(T=T):
    """(episode time, sfx, gain dB, pan) for helper 7's mix."""
    fire_t = S(3, 0).end + 0.05
    c = [(0.0, "sea_waves", -14, 0.0), (0.0, "clock_tick", -10, -0.6), (L(2).start + 0.3, "tank", -18, 0.2),
         (fire_t, "gun_boom", 0, 0.3), (fire_t + 0.05, "explosion", -6, 0.5),
         (L(4).start - 0.2, "artillery", -20, 0.0),
         (L(5).start, "clock_tick", -12, 0.0),
         (word_t(6, "one bomb", 0.5), "explosion", -4, 0.0),
         (L(7).start - 0.3, "stamp", -6, 0.0), (L(7).start + 0.3, "stamp", -8, 0.0),
         (word_t(7, "just twenty"), "page_whoosh", -10, -0.3),
         (T.chapter("C1").card[0], "page_whoosh", -8, 0.0), (L(8).start + 0.2, "page_whoosh", -10, 0.2),
         (L(9).start + 1.4, "rifle_crack", -24, 0.0),
         (L(10).start + 1.0, "typewriter", -20, 0.3)]
    for w in ("responsibility", "land", "army", "money"):
        c.append((word_t(10, w, 0.6), "stamp", -4, 0.0))
    c += [(word_t(12, "crashes", 0.3), "door_slam", -4, 0.0), (word_t(12, "crashes", 0.3) + 0.25, "stamp", -6, 0.2), (L(13).start, "train", -26, -0.4),
          (L(14).start + 0.5, "crowd_cheer", -14, 0.0), (word_t(14, "and who blames"), "crowd_cheer", -10, 0.0),
          (L(15).start, "gun_boom", -16, 0.0),
          (word_t(16, "dictatorship", 0.2), "door_slam", -2, 0.0)]
    return c
