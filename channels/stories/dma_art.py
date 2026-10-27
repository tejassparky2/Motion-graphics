"""DEAD MAN'S ALGORITHM: the cast and sets, drawn in cairo (anime-style 2D, cel-shaded like toon2d).

Story bible: channels/stories/dead_mans_algorithm_bible.md. Looks are production design (the bible gives none except
Momo's). Everything lays itself out from W and H, so the same drawings serve the 9:16 Shorts and the 16:9 long video.
"""
import math

from motion.engine import W, H, cairo, clamp01
from motion.polish import rad, text_width

from channels.horror import hud2d
from channels.horror import toon2d as tk
from channels.horror.toon2d import INK, curve, glow, grade, hexa, mix, noise, poly, toon

V = H > W                                     # vertical (Shorts) or landscape (long video)
U = H / 1280 if not V else 1.0                # scale for full-height compositions

# ------------------------------------------------------------------ cast
SKIN = (hexa("#f2d0b4"), hexa("#e8c09e"), hexa("#d9ab86"), hexa("#f5d8c2"))
GAKURAN = (hexa("#1b1f2b"), hexa("#0d1017"), hexa("#2c3346"))
SAILOR = (hexa("#1e2a4a"), hexa("#121a30"), hexa("#2f3f68"))
CAST = {   # sex, skin, hair, hair style, iris, extras
    "ren":    dict(sex="m", skin=SKIN[0], hair=hexa("#16151a"), style="messy", iris=hexa("#3a3550"), tired=True),
    "haruto": dict(sex="m", skin=SKIN[1], hair=hexa("#7a4a22"), style="spiky", iris=hexa("#6b4423"), open_collar=True),
    "yui":    dict(sex="f", skin=SKIN[3], hair=hexa("#3b2416"), style="long", iris=hexa("#6b4a2b"), clip=True),
    "riku":   dict(sex="m", skin=SKIN[2], hair=hexa("#c9c2a8"), style="swept", iris=hexa("#5a4a3a"), open_collar=True,
                   sharp=True),
    "kota":   dict(sex="m", skin=SKIN[0], hair=hexa("#121216"), style="bowl", iris=hexa("#2f2a26"), glasses=True),
    "go":     dict(sex="m", skin=SKIN[2], hair=hexa("#1a1612"), style="buzz", iris=hexa("#3b2d22"), big=True),
    "aoi":    dict(sex="f", skin=SKIN[0], hair=hexa("#18203a"), style="bob", iris=hexa("#2c3e66"), pin=True),
    "mio":    dict(sex="f", skin=SKIN[3], hair=hexa("#9a6a44"), style="wavy", iris=hexa("#7a5638"), earrings=True),
}
NAMES = {"ren": ("KURODA REN", "watches everything"), "haruto": ("SAKURAI HARUTO", "the joker"),
         "yui": ("TACHIBANA YUI", "always on Ren's side"), "riku": ("KANZAKI RIKU", "in charge"),
         "kota": ("HAYASHI KOTA", "the target"), "go": ("SHIBATA GŌ", "doesn't back down"),
         "aoi": ("FUJIMOTO AOI", "notices"), "mio": ("AOYAMA MIO", "reads people")}
EXTRA_STYLES = ["messy", "short", "pony", "long", "short", "bob", "messy", "pony", "short", "long", "spiky", "short"]
EXTRAS = [dict(sex="f" if st in ("pony", "long", "bob") else "m", skin=SKIN[k % 4],
               hair=[hexa("#1a1714"), hexa("#2a1c14"), hexa("#4a3020"), hexa("#151820")][k % 4], style=st,
               iris=hexa("#3a2c22")) for k, st in enumerate(EXTRA_STYLES)]     # the 12 unnamed students

EXPR = {   # eye opening, brow raise, worry (+ inner ends up, - angry), mouth, mouth open
    "calm":  dict(open=1.0, brow=0.0, worry=0.0, mouth="line", mo=0.0),
    "smirk": dict(open=0.82, brow=-0.1, worry=-0.4, mouth="smirk", mo=0.0),
    "grin":  dict(open=0.72, brow=0.15, worry=0.0, mouth="grin", mo=0.6),
    "smile": dict(open=0.9, brow=0.1, worry=0.1, mouth="smile", mo=0.0),
    "worry": dict(open=1.05, brow=0.25, worry=0.7, mouth="line", mo=0.1),
    "fear":  dict(open=1.25, brow=0.5, worry=1.0, mouth="o", mo=0.55),
    "shock": dict(open=1.35, brow=0.75, worry=0.4, mouth="o", mo=0.9),
    "angry": dict(open=0.8, brow=-0.2, worry=-0.9, mouth="grit", mo=0.3),
    "sad":   dict(open=0.75, brow=0.1, worry=0.9, mouth="frown", mo=0.0),
    "focus": dict(open=0.78, brow=-0.05, worry=-0.25, mouth="line", mo=0.0),
}


def _blink(t, seed):
    ph = (t + seed) % 4.1
    return 1 - 0.95 * math.sin(ph / 0.13 * math.pi) if ph < 0.13 else 1.0


def anime_eye(cr, x, y, sx, rx, ry, k, look, iris, fear=0.0, lash=True, tired=False, sharp=False):
    """A tall anime eye, mirrored for the left side (sx = -1): white, a big two-tone iris with two highlights, a heavy
    upper lash line with a flick at the outer corner."""
    cr.save()
    cr.translate(x, y)
    h = ry * k
    top = -h * (0.78 if sharp else 1.0)
    outer = -h * (0.3 if sharp else 0.12)

    def shape(c):
        c.new_path()
        c.move_to(-rx, 2)
        c.curve_to(-rx * 0.6, top, rx * 0.5, top, rx, outer)
        c.curve_to(rx * 0.7, h * 0.9, -rx * 0.6, h * 0.9, -rx, 2)
        c.close_path()
    cr.save()
    cr.scale(sx, 1)                                           # local -x is the inner corner (toward the nose)
    shape(cr)
    cr.restore()
    cr.set_source_rgba(0.99, 0.98, 0.97, 1)
    cr.fill_preserve()
    cr.save()
    cr.clip()
    px, py = look[0] * rx * 0.35, look[1] * ry * 0.25
    ir = rx * 0.74 * (1 - 0.32 * fear)
    g = cairo.LinearGradient(0, py - ir * 1.2, 0, py + ir * 1.2)
    g.add_color_stop_rgba(0, *mix(iris, (0, 0, 0, 1), 0.5)[:3], 1)
    g.add_color_stop_rgba(1, *mix(iris, (1, 1, 1, 1), 0.4)[:3], 1)
    cr.save()
    cr.translate(px, py)
    cr.scale(1, 1.2)
    cr.arc(0, 0, ir, 0, 2 * math.pi)
    cr.restore()
    cr.set_source(g)
    cr.fill()
    cr.set_source_rgba(0.03, 0.02, 0.04, 1)
    cr.save()
    cr.translate(px, py)
    cr.scale(1, 1.2)
    cr.arc(0, 0, ir * 0.42, 0, 2 * math.pi)
    cr.restore()
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.95)
    cr.arc(px + ir * 0.34, py - ir * 0.48, ir * 0.28, 0, 2 * math.pi)
    cr.fill()
    cr.set_source_rgba(1, 1, 1, 0.6)
    cr.arc(px - ir * 0.3, py + ir * 0.5, ir * 0.13, 0, 2 * math.pi)
    cr.fill()
    if tired:                                                 # a soft shadow under the upper lid
        cr.set_source_rgba(0.2, 0.15, 0.25, 0.28)
        cr.rectangle(-rx, top, 2 * rx, h * 0.45)
        cr.fill()
    cr.restore()
    cr.save()
    cr.scale(sx, 1)
    shape(cr)
    cr.restore()
    cr.set_source_rgba(*INK)
    cr.set_line_width(2.2)
    cr.stroke()
    if lash:
        cr.save()
        cr.scale(sx, 1)
        cr.new_path()
        cr.move_to(-rx * 1.02, 3)
        cr.curve_to(-rx * 0.6, top - 2, rx * 0.5, top - 3, rx * 1.05, outer - 3)
        cr.line_to(rx * 1.22, outer - 9)                      # the flick
        cr.restore()
        cr.set_line_width(5.5)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
    cr.restore()


def _hair(cr, spec, layer, light, rim, rim_from, t=0.0):
    """Hair, drawn in two layers: 'back' (behind the face) and 'front' (bangs)."""
    col, st = spec["hair"], spec["style"]
    dk = mix(col, (0, 0, 0, 1), 0.45)
    sway = 3 * math.sin(t * 1.3)
    if layer == "back":
        if st == "long":
            toon(cr, lambda c: curve(c, [(-100, -60), (-128, 60), (-140, 250), (-90, 290), (90, 290), (140, 250),
                                         (128, 60), (100, -60), (0, -150)]), col, dk, light, rim, rim_from)
        elif st == "wavy":
            toon(cr, lambda c: curve(c, [(-102, -60), (-138, 50), (-122, 140), (-150, 230), (-96, 286), (96, 286),
                                         (150, 230), (122, 140), (138, 50), (102, -60), (0, -150)]), col, dk, light,
                 rim, rim_from)
        elif st == "pony":
            toon(cr, lambda c: curve(c, [(40, -120), (118, -96), (140 + sway, 10), (130 + sway, 140),
                                         (108 + sway, 90), (100, -20), (60, -80)]), col, dk, light, rim, rim_from)
        elif st == "bob":
            toon(cr, lambda c: curve(c, [(-100, -60), (-108, 40), (-96, 98), (-40, 104), (40, 104), (96, 98),
                                         (108, 40), (100, -60), (0, -150)]), col, dk, light, rim, rim_from)
        return
    if st == "messy":
        pts = [(-100, 10), (-104, -70), (-70, -128), (-10, -148), (50, -140), (96, -104), (104, -40), (100, 14),
               (84, -26), (70, -10), (58, -54), (36, -18), (20, -62), (-2, -16), (-20, -58), (-40, -12), (-58, -50),
               (-76, -6), (-86, -40)]
    elif st == "spiky":
        pts = [(-100, 0), (-112, -60), (-124, -110), (-80, -110), (-70, -170), (-30, -128), (0, -186), (26, -132),
               (70, -168), (78, -112), (122, -112), (106, -56), (100, 0), (80, -40), (50, -30), (20, -56), (-10, -30),
               (-40, -52), (-70, -30)]
    elif st == "long":
        pts = [(-98, -16), (-100, -80), (-60, -134), (0, -148), (60, -134), (100, -80), (98, -16), (86, -48),
               (60, -56), (30, -46), (0, -58), (-30, -46), (-60, -56), (-86, -48)]
    elif st == "swept":
        pts = [(-96, -10), (-102, -80), (-60, -136), (0, -152), (64, -146), (104, -110), (110, -50), (98, -20),
               (90, -70), (40, -96), (-10, -100), (-60, -84), (-86, -46)]
    elif st == "bowl":
        pts = [(-100, 0), (-104, -70), (-64, -132), (0, -148), (64, -132), (104, -70), (100, 0), (86, -34),
               (40, -40), (0, -38), (-40, -40), (-86, -34)]
    elif st == "buzz":
        pts = [(-98, -40), (-96, -96), (-56, -136), (0, -146), (56, -136), (96, -96), (98, -40), (80, -80),
               (0, -96), (-80, -80)]
    elif st == "bob":
        pts = [(-100, 40), (-104, -70), (-62, -134), (0, -150), (62, -134), (104, -70), (100, 40), (86, -40),
               (52, -46), (52, -36), (-52, -36), (-52, -46), (-86, -40)]
    elif st == "wavy":
        pts = [(-98, -10), (-102, -80), (-60, -136), (10, -150), (70, -132), (102, -76), (98, -16), (90, -46),
               (72, -74), (40, -92), (10, -86), (-20, -62), (-52, -44), (-82, -32)]
    elif st == "pony":
        pts = [(-98, 0), (-102, -70), (-62, -132), (0, -148), (62, -132), (102, -70), (98, 0), (84, -36),
               (50, -48), (10, -58), (-30, -50), (-64, -48), (-86, -24)]
    else:   # short
        pts = [(-100, -4), (-104, -72), (-64, -132), (0, -148), (64, -132), (104, -72), (100, -4), (84, -40),
               (56, -36), (30, -56), (0, -40), (-30, -56), (-58, -36), (-84, -40)]
    toon(cr, lambda c: curve(c, pts), col, dk, light, rim, rim_from)
    if st in ("long", "wavy"):                                # thin side locks in front of the ears
        for sx in (-1, 1):
            toon(cr, lambda c, sx=sx: curve(c, [(sx * 100, -40), (sx * 108, 30), (sx * 104, 110), (sx * 92, 120),
                                                (sx * 90, 40), (sx * 88, -30)]), col, dk, light, rim, rim_from, lw=3)
    cr.set_source_rgba(1, 1, 1, 0.16)                         # a band of shine
    cr.set_line_width(5)
    cr.new_path()
    cr.arc(0, -40, 92, math.pi * 1.2, math.pi * 1.55)
    cr.stroke()


def student_head(cr, t, spec, expr="calm", look=(0.0, 0.0), light=(-14, -10), rim=None, rim_from=(9, 0), seed=0.0,
                 talk=0.0, sweat=0.0, tears=0.0, back=True):
    """A teenager's head, centred at (0, 0): ~200 px wide. expr: a key of EXPR. talk 0..1 opens the mouth.
    back=False leaves out the long hair behind (student_bust draws it behind the shoulders)."""
    e = EXPR[expr]
    sk = spec["skin"]
    sk_d = mix(sk, hexa("#8a5a48"), 0.35)
    if back:
        _hair(cr, spec, "back", light, rim, rim_from, t)
    for sx in (-1, 1):
        toon(cr, lambda c, sx=sx: curve(c, [(sx * 88, -20), (sx * 104, -26), (sx * 106, 10), (sx * 90, 26)]), sk,
             sk_d, light, rim, rim_from, lw=3.5)
    jaw = 104 if spec["sex"] == "m" else 96
    face = lambda c: curve(c, [(-90, -40), (-88, -98), (-50, -134), (0, -142), (50, -134), (88, -98), (90, -40),
                               (82, 20), (56, 66), (0, jaw), (-56, 66), (-82, 20)])
    if spec.get("big"):
        face = lambda c: curve(c, [(-96, -40), (-94, -98), (-54, -136), (0, -144), (54, -136), (94, -98), (96, -40),
                                   (92, 30), (66, 76), (0, 106), (-66, 76), (-92, 30)])
    toon(cr, face, sk, sk_d, light, rim, rim_from)
    cr.save()
    cr.new_path()
    face(cr)
    cr.clip()
    for sx in (-1, 1):
        cr.set_source(rad(sx * 52, 30, 26, [(0, (0.95, 0.5, 0.5, 0.22)), (1, (0.95, 0.5, 0.5, 0))]))
        cr.paint()
    cr.restore()
    ok = _blink(t, seed) * e["open"]
    fear = max(0.0, e["worry"]) * (e["open"] > 1.1)
    for sx in (-1, 1):
        anime_eye(cr, sx * 39, -2, sx, 25, 31, ok, look, spec["iris"], fear=fear, tired=spec.get("tired", False),
                  sharp=spec.get("sharp", False))
        cr.save()                                             # brows
        cr.translate(sx * 40, -50 - 12 * e["brow"])
        cr.scale(sx, 1)
        cr.rotate(0.3 * e["worry"])                           # + lifts the inner end (worry), - drops it (anger)
        cr.set_source_rgba(*mix(spec["hair"], (0, 0, 0, 1), 0.3))
        cr.set_line_width(5)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.new_path()
        cr.move_to(-20, 2)
        cr.curve_to(-8, -6, 10, -8, 24, -1)
        cr.stroke()
        cr.restore()
    cr.set_source_rgba(*sk_d[:3], 0.9)                        # nose
    cr.set_line_width(2.4)
    cr.new_path()
    cr.move_to(2, 20)
    cr.line_to(-3, 30)
    cr.line_to(3, 31)
    cr.stroke()
    m, mo = e["mouth"], max(e["mo"], 0.45 * talk * (0.5 + 0.5 * math.sin(t * 22)))
    cr.save()
    cr.translate(0, 56)
    if m in ("o",) or mo > 0.2 and m not in ("grin", "grit"):
        cr.save()
        cr.scale(1, 0.4 + 1.0 * mo)
        cr.new_path()
        cr.arc(0, 0, 11, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(0.42, 0.12, 0.14, 1)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(2.5)
        cr.stroke()
    elif m in ("grin", "grit"):
        cr.new_path()
        cr.move_to(-24, -4)
        cr.curve_to(-12, 14 if m == "grin" else 6, 12, 14 if m == "grin" else 6, 24, -4)
        cr.close_path()
        cr.set_source_rgba(0.98, 0.97, 0.95, 1)
        cr.fill_preserve()
        cr.set_source_rgba(*INK)
        cr.set_line_width(2.6)
        cr.stroke()
        if m == "grit":
            cr.move_to(-18, 2)
            cr.line_to(18, 2)
            cr.stroke()
    else:
        cr.set_source_rgba(*INK)
        cr.set_line_width(2.8)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.new_path()
        if m == "smile":
            cr.move_to(-16, -2)
            cr.curve_to(-6, 8, 6, 8, 16, -2)
        elif m == "smirk":
            cr.move_to(-14, 2)
            cr.curve_to(-2, 4, 10, 0, 18, -6)
        elif m == "frown":
            cr.move_to(-14, 4)
            cr.curve_to(-4, -4, 4, -4, 14, 4)
        else:
            cr.move_to(-12, 0)
            cr.line_to(12, 0)
        cr.stroke()
    cr.restore()
    _hair(cr, spec, "front", light, rim, rim_from, t)
    if spec.get("glasses"):
        cr.set_source_rgba(0.15, 0.15, 0.18, 1)
        cr.set_line_width(3.5)
        for sx in (-1, 1):
            cr.new_path()
            cr.arc(sx * 38, -2, 30, 0, 2 * math.pi)
            cr.stroke()
        cr.move_to(-8, -4)
        cr.line_to(8, -4)
        cr.stroke()
        cr.set_source_rgba(1, 1, 1, 0.25)
        for sx in (-1, 1):
            cr.new_path()
            cr.arc(sx * 38, -2, 24, math.pi * 1.1, math.pi * 1.4)
            cr.stroke()
    if spec.get("clip"):
        toon(cr, lambda c: tk.tk_rrect(c, 52, -96, 34, 12, 5), hexa("#f2c14e"), None, (0, 0), None, lw=2.5)
    if spec.get("pin"):
        for k in range(2):
            cr.set_source_rgba(0.85, 0.2, 0.3, 1)
            cr.rectangle(-70 + k * 12, -64 - k * 6, 4, 26)
            cr.fill()
    if spec.get("earrings"):
        for sx in (-1, 1):
            glow(cr, sx * 98, 32, 10, (1, 0.9, 0.5), 0.6)
            cr.set_source_rgba(0.95, 0.85, 0.45, 1)
            cr.arc(sx * 98, 32, 4, 0, 2 * math.pi)
            cr.fill()
    if sweat > 0:
        cr.set_source_rgba(0.75, 0.9, 1, 0.85 * sweat)
        cr.save()
        cr.translate(84, -50 + 30 * ((t * 0.4) % 1))
        cr.move_to(0, -12)
        cr.curve_to(8, 0, 8, 9, 0, 10)
        cr.curve_to(-8, 9, -8, 0, 0, -12)
        cr.restore()
        cr.fill()
    if tears > 0:
        cr.set_source_rgba(0.75, 0.9, 1, 0.8 * tears)
        for sx in (-1, 1):
            ty = 22 + 40 * ((t * 0.5 + (sx > 0) * 0.5) % 1)
            cr.arc(sx * 38, ty, 5, 0, 2 * math.pi)
            cr.fill()


def student_bust(cr, x, y, s, t, who, expr="calm", look=(0.0, 0.0), light=(-14, -10), rim=None, rim_from=(9, 0),
                 talk=0.0, tilt=0.0, sweat=0.0, tears=0.0, tremble=0.0):
    """A student from the chest up in Class 3-B's uniform (gakuran or sailor). (x, y) = the base of the neck.
    who: a CAST key or an int (one of the 12 unnamed students)."""
    spec = CAST[who] if isinstance(who, str) else EXTRAS[who % 12]
    seed = (hash(who) % 97) / 30 if isinstance(who, str) else who * 0.7
    cr.save()
    cr.translate(x + tremble * 2.4 * math.sin(t * 39), y)
    cr.scale(s, s)
    up = -3 * (0.5 + 0.5 * math.sin(t * 2 * math.pi * 0.3 + seed))
    wide = 1.18 if spec.get("big") else 1.0
    cr.save()                                                  # long hair falls behind the shoulders
    cr.translate(0, -186)
    cr.rotate(tilt + 0.01 * noise(t * 0.5, seed))
    _hair(cr, spec, "back", light, rim, rim_from, t)
    cr.restore()
    if spec["sex"] == "m":
        base, shade, lite = GAKURAN
        toon(cr, lambda c: curve(c, [(-56 * wide, -6 + up), (-160 * wide, 28 + up), (-196 * wide, 130),
                                     (-206 * wide, 430), (206 * wide, 430), (196 * wide, 130), (160 * wide, 28 + up),
                                     (56 * wide, -6 + up)]), base, shade, light, rim, rim_from)
        toon(cr, lambda c: poly(c, [(-32, -80), (32, -80), (36, 0), (-36, 0)]), spec["skin"],
             mix(spec["skin"], hexa("#8a5a48"), 0.35), (0, 8), None, lw=3.5)
        if spec.get("open_collar"):                            # jacket open: a white shirt at the neck
            toon(cr, lambda c: poly(c, [(-40, 0), (40, 0), (14, 150), (-14, 150)]), hexa("#f0f0f2"), hexa("#c8c8d0"),
                 (0, -4), None, lw=3)
        else:                                                  # the standing collar, buttoned to the top
            toon(cr, lambda c: tk.tk_rrect(c, -48, -16 + up, 96, 34, 8), lite, shade, light, rim, rim_from, lw=3.5)
            for k in range(4):
                glow(cr, 0, 50 + k * 80, 12, (1, 0.85, 0.4), 0.4)
                toon(cr, lambda c, k=k: c.arc(0, 50 + k * 80, 8, 0, 2 * math.pi), hexa("#e2b64a"), hexa("#a07a20"),
                     (-2, -2), None, lw=2)
    else:
        base, shade, lite = SAILOR
        toon(cr, lambda c: curve(c, [(-52, -6 + up), (-150, 26 + up), (-186, 130), (-194, 430), (194, 430),
                                     (186, 130), (150, 26 + up), (52, -6 + up)]), hexa("#f3f3f6"), hexa("#cfd2da"),
             light, rim, rim_from)                             # the white blouse
        toon(cr, lambda c: poly(c, [(-32, -80), (32, -80), (34, 0), (-34, 0)]), spec["skin"],
             mix(spec["skin"], hexa("#8a5a48"), 0.35), (0, 8), None, lw=3.5)
        for sx in (-1, 1):                                     # the sailor collar flaps, navy with a white stripe
            toon(cr, lambda c, sx=sx: poly(c, [(sx * 26, -4 + up), (sx * 160, 24 + up), (sx * 150, 120),
                                               (sx * 12, 150)]), base, shade, light, rim, rim_from, lw=4)
            cr.set_source_rgba(0.95, 0.95, 0.97, 1)
            cr.set_line_width(4)
            cr.move_to(sx * 40, 10 + up)
            cr.line_to(sx * 140, 36 + up)
            cr.line_to(sx * 132, 106)
            cr.stroke()
        toon(cr, lambda c: poly(c, [(-34, 130), (34, 130), (16, 190), (0, 230), (-16, 190)]), hexa("#c0262d"),
             hexa("#86161b"), (0, -4), None, lw=3)            # the red scarf
        toon(cr, lambda c: c.arc(0, 136, 18, 0, 2 * math.pi), hexa("#d8343b"), hexa("#86161b"), (0, -3), None, lw=3)
    cr.translate(0, -186)
    cr.rotate(tilt + 0.01 * noise(t * 0.5, seed))
    if spec.get("big"):
        cr.scale(1.06, 1.06)
    student_head(cr, t, spec, expr, look, light, rim, rim_from, seed, talk, sweat, tears, back=False)
    cr.restore()


# ------------------------------------------------------------------ Momo
MOMO_W, MOMO_D = hexa("#fbfbf8"), hexa("#cfd2d6")


def momo(cr, x, y, s, t, mood="happy", wave=0.0, lean=0.0):
    """Momo, the administrator: a small white round-eared rodent with black bead eyes, a red bow tie and a gold bell.
    (x, y) = its feet. It bounces; the bell swings. mood: happy / wink / sly."""
    hop = abs(math.sin(t * 2.6)) * 10
    cr.save()
    cr.translate(x, y - hop * s)
    cr.scale(s, s)
    cr.rotate(lean + 0.04 * math.sin(t * 1.3))
    for sx in (-1, 1):                                         # feet
        toon(cr, lambda c, sx=sx: (c.save(), c.translate(sx * 34, -10), c.scale(1.4, 0.7),
                                   c.arc(0, 0, 18, 0, 2 * math.pi), c.restore()), MOMO_W, MOMO_D, (-6, -6), None,
             lw=4)
    toon(cr, lambda c: (c.save(), c.translate(0, -92), c.scale(1.0, 1.06), c.arc(0, 0, 86, 0, 2 * math.pi),
                        c.restore()), MOMO_W, MOMO_D, (-14, -12), (0.8, 0.9, 1, 0.5), (8, -4))      # round body/head
    for sx in (-1, 1):                                         # round ears with pink inside
        toon(cr, lambda c, sx=sx: c.arc(sx * 66, -168, 38, 0, 2 * math.pi), MOMO_W, MOMO_D, (-8, -8), None, lw=4)
        toon(cr, lambda c, sx=sx: c.arc(sx * 66, -166, 22, 0, 2 * math.pi), hexa("#f4b6c2"), hexa("#e08a9c"),
             (-4, -4), None, lw=2.5)
    for sx in (-1, 1):                                         # bead eyes
        if mood == "wink" and sx > 0:
            cr.set_source_rgba(*INK)
            cr.set_line_width(5)
            cr.move_to(sx * 30 - 12, -104)
            cr.curve_to(sx * 30 - 4, -112, sx * 30 + 4, -112, sx * 30 + 12, -104)
            cr.stroke()
            continue
        cr.set_source_rgba(0.02, 0.02, 0.03, 1)
        cr.save()
        cr.translate(sx * 30, -104)
        cr.scale(1, 1.2 if mood != "sly" else 0.7)
        cr.arc(0, 0, 13, 0, 2 * math.pi)
        cr.restore()
        cr.fill()
        cr.set_source_rgba(1, 1, 1, 0.95)
        cr.arc(sx * 30 + 4, -110, 4, 0, 2 * math.pi)
        cr.fill()
    for sx in (-1, 1):                                         # blush
        cr.set_source(rad(sx * 54, -78, 18, [(0, (1, 0.6, 0.7, 0.5)), (1, (1, 0.6, 0.7, 0))]))
        cr.paint()
    toon(cr, lambda c: c.arc(0, -84, 6, 0, 2 * math.pi), hexa("#f08aa0"), None, (0, 0), None, lw=2)   # nose
    cr.set_source_rgba(*INK)                                   # a small 'w' smile
    cr.set_line_width(3.5)
    cr.new_path()
    cr.move_to(-14, -70)
    cr.curve_to(-10, -62, -2, -62, 0, -70)
    cr.curve_to(2, -62, 10, -62, 14, -70)
    cr.stroke()
    toon(cr, lambda c: poly(c, [(0, -30), (-34, -46), (-34, -14)]), hexa("#d7262e"), hexa("#8e151a"), (0, -3), None,
         lw=3)                                                 # the bow tie
    toon(cr, lambda c: poly(c, [(0, -30), (34, -46), (34, -14)]), hexa("#d7262e"), hexa("#8e151a"), (0, -3), None,
         lw=3)
    toon(cr, lambda c: c.arc(0, -30, 8, 0, 2 * math.pi), hexa("#e8393f"), None, (0, 0), None, lw=2.5)
    sw = 0.3 * math.sin(t * 5.2)                               # the bell, swinging
    cr.save()
    cr.translate(0, -20)
    cr.rotate(sw)
    toon(cr, lambda c: c.arc(0, 20, 14, 0, 2 * math.pi), hexa("#e8c04a"), hexa("#a8821c"), (-3, -3), (1, 1, 0.8, 0.6),
         (-4, -4), lw=2.5)
    cr.set_source_rgba(*INK)
    cr.rectangle(-6, 24, 12, 2.5)
    cr.fill()
    cr.restore()
    if wave > 0:                                               # a little paw raised
        toon(cr, lambda c: (c.save(), c.translate(84, -110 - 40 * wave), c.arc(0, 0, 18, 0, 2 * math.pi),
                            c.restore()), MOMO_W, MOMO_D, (-4, -4), None, lw=3.5)
    cr.restore()


# ------------------------------------------------------------------ sets
def classroom(cr, t, meteor=0.0, clock=(12, 16, 0)):
    """Class 3-B at lunch: the window wall on the left (blue noon sky; the meteor grows in it), the blackboard on the
    right, the 3-B sign, the wall clock. Laid out from W and H."""
    sky = cairo.LinearGradient(0, 0, 0, H)
    sky.add_color_stop_rgb(0, *mix(hexa("#7cb8ec"), hexa("#ffb35c"), 0.6 * meteor)[:3])
    sky.add_color_stop_rgb(1, *mix(hexa("#cfe6f7"), hexa("#ffd9a0"), 0.6 * meteor)[:3])
    wall = mix(hexa("#e9dfcc"), hexa("#ffcf9a"), 0.35 * meteor)
    cr.set_source_rgba(*wall)
    cr.paint()
    wx0, wx1, wy0, wy1 = 0, W * (0.46 if not V else 0.62), H * 0.08, H * 0.62
    cr.save()
    cr.rectangle(wx0, wy0, wx1 - wx0, wy1 - wy0)
    cr.clip()
    cr.set_source(sky)
    cr.paint()
    for k in range(6):                                         # trees outside, bending one way (the wind)
        bx = wx0 + (k + 0.5) * (wx1 - wx0) / 6
        bend = 14 + 6 * math.sin(t * 1.4 + k)
        cr.set_source_rgba(0.2, 0.45, 0.28, 1)
        cr.arc(bx + bend, wy1 - 60, 60, 0, 2 * math.pi)
        cr.fill()
        cr.set_source_rgba(0.3, 0.55, 0.32, 1)
        cr.arc(bx + bend - 10, wy1 - 80, 38, 0, 2 * math.pi)
        cr.fill()
    if meteor > 0:
        meteor_streak(cr, t, wx0 + (wx1 - wx0) * 0.35, wy0 + (wy1 - wy0) * 0.35, meteor)
    cr.restore()
    for k in range(4):                                         # window frames
        x = wx0 + k * (wx1 - wx0) / 3
        toon(cr, lambda c, x=x: c.rectangle(x - 7, wy0, 14, wy1 - wy0), hexa("#cfd6dc"), hexa("#9aa4ad"), (-2, -2),
             None, lw=3)
    toon(cr, lambda c: c.rectangle(wx0, wy0 + (wy1 - wy0) * 0.5 - 6, wx1 - wx0, 12), hexa("#cfd6dc"), hexa("#9aa4ad"),
         (-2, -2), None, lw=3)
    toon(cr, lambda c: c.rectangle(wx0, wy1 - 8, wx1 - wx0 + 10, 22), hexa("#d9cdb6"), hexa("#b0a28a"), (0, -3), None,
         lw=3)
    bx0 = wx1 + W * 0.05                                       # the blackboard
    toon(cr, lambda c: c.rectangle(bx0, H * 0.14, W - bx0 + 20, H * 0.3), hexa("#2f4a3a"), hexa("#1f3328"), (-3, -3),
         None, lw=5)
    cr.set_source_rgba(0.9, 0.92, 0.88, 0.55)                 # chalk scribbles (nothing readable: no invented facts)
    cr.set_line_width(3)
    for k in range(4):
        y = H * 0.14 + (50 + 46 * k) * max(U, 0.7)
        cr.move_to(bx0 + 30, y)
        for j in range(8):
            cr.line_to(bx0 + 30 + j * 26, y + 5 * math.sin(j * 1.7 + k))
        cr.stroke()
    sy = H * 0.07                                               # the 3-B sign and the clock, side by side
    sx = W - 210 if V else W - 260
    toon(cr, lambda c: tk.tk_rrect(c, sx - 60, sy - 26, 120, 44, 6), hexa("#f4f1ea"), hexa("#cfc8b8"), (-2, -2), None,
         lw=3)
    hud2d._text(cr, "3-B", sx, sy + 8, 30, INK, hud2d.ROUND, "center")
    wall_clock(cr, t, sx + 120, sy, 36, clock)
    for row in range(2):                                       # desks
        for k in range(4):
            dx = W * (0.12 + k * 0.25) + row * 30
            dy = H * (0.78 + row * 0.12)
            toon(cr, lambda c, dx=dx, dy=dy: c.rectangle(dx - 70, dy - 20, 140, 26), hexa("#c79a63"), hexa("#9a7244"),
                 (-3, -3), None, lw=3)
    if meteor > 0:
        glow(cr, wx0 + (wx1 - wx0) * 0.35, wy0 + (wy1 - wy0) * 0.35, 900 * U, (1, 0.6, 0.2), 0.4 * meteor)


def wall_clock(cr, t, x, y, r, hms):
    h, m, sec = hms
    toon(cr, lambda c: c.arc(x, y, r + 5, 0, 2 * math.pi), hexa("#2b2b2b"), None, (0, 0), None, lw=3)
    toon(cr, lambda c: c.arc(x, y, r, 0, 2 * math.pi), hexa("#f4f1ea"), hexa("#cfc8b8"), (-2, -2), None, lw=2)
    for frac, ln, w, col in (((h % 12 + m / 60) / 12, r * 0.5, 4, INK), ((m + sec / 60) / 60, r * 0.78, 3, INK),
                             (sec / 60, r * 0.85, 1.6, (0.8, 0.1, 0.08, 1))):
        a = frac * 2 * math.pi
        cr.set_source_rgba(*col)
        cr.set_line_width(w)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(x, y)
        cr.line_to(x + ln * math.sin(a), y - ln * math.cos(a))
        cr.stroke()


def meteor_streak(cr, t, x, y, k):
    """The meteor: a burning head with a long tail, growing with k (0..1)."""
    r = 6 + 120 * k ** 2
    ang = -0.6
    tail = 200 + 700 * k
    cr.save()
    cr.translate(x, y)
    cr.rotate(ang)
    g = cairo.LinearGradient(0, 0, tail, 0)
    g.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.9)
    g.add_color_stop_rgba(1, 1, 0.5, 0.2, 0)
    cr.set_source(g)
    cr.move_to(0, -r)
    cr.line_to(tail, -r * 0.25)
    cr.line_to(tail, r * 0.25)
    cr.line_to(0, r)
    cr.close_path()
    cr.fill()
    cr.restore()
    glow(cr, x, y, r * 4, (1, 0.7, 0.3), 0.8)
    cr.set_source_rgba(1, 0.97, 0.85, 1)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()


def the_eye(cr, t, x, y, r, a=1.0):
    """What Ren sees inside the meteor: a pattern like an eye (rings and a slit). Never explained."""
    if a <= 0:
        return
    cr.save()
    cr.push_group()
    glow(cr, x, y, r * 2.2, (1, 0.55, 0.15), 0.9)
    for k, (rr, col) in enumerate(((1.0, (0.35, 0.05, 0.02)), (0.78, (0.9, 0.35, 0.08)), (0.56, (1, 0.75, 0.3)))):
        cr.set_source_rgba(*col, 1)
        cr.arc(x, y, r * rr, 0, 2 * math.pi)
        cr.fill()
    cr.set_source_rgba(0.12, 0.02, 0.02, 0.6)                  # radial streaks, like an iris
    cr.set_line_width(2)
    for k in range(48):
        aa = k * 2 * math.pi / 48 + 0.05 * math.sin(t * 2 + k)
        cr.move_to(x + r * 0.25 * math.cos(aa), y + r * 0.25 * math.sin(aa))
        cr.line_to(x + r * 0.95 * math.cos(aa), y + r * 0.95 * math.sin(aa))
    cr.stroke()
    cr.set_source_rgba(0.02, 0.01, 0.01, 1)                    # the slit
    cr.save()
    cr.translate(x, y)
    cr.scale(0.16, 1)
    cr.arc(0, 0, r * 0.72, 0, 2 * math.pi)
    cr.restore()
    cr.fill()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def chamber(cr, t, flicker=True, screen=None, dark=0.0):
    """The underground chamber: raw concrete, pipes, a flickering strip light, four cameras in the corners, a huge
    wall screen (screen(cr, x0, y0, w, h) draws on it), a sealed steel door."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, 0.36, 0.37, 0.38)
    g.add_color_stop_rgb(0.62, 0.3, 0.31, 0.32)
    g.add_color_stop_rgb(1, 0.22, 0.22, 0.23)
    cr.set_source(g)
    cr.paint()
    cr.set_source_rgba(0, 0, 0, 0.12)                          # form-work seams
    for k in range(1, 6):
        cr.rectangle(0, H * 0.62 * k / 6, W, 2)
        cr.rectangle(W * k / 6, 0, 2, H * 0.62)
    cr.fill()
    cr.set_source_rgba(0.18, 0.18, 0.19, 1)                    # floor
    cr.rectangle(0, H * 0.62, W, H * 0.38)
    cr.fill()
    for k in range(-8, 9):
        cr.set_source_rgba(1, 1, 1, 0.03)
        cr.set_line_width(2)
        cr.move_to(W / 2 + k * 40, H * 0.62)
        cr.line_to(W / 2 + k * 160, H)
        cr.stroke()
    for y in (H * 0.05, H * 0.09):                             # pipes along the ceiling
        toon(cr, lambda c, y=y: c.rectangle(-10, y, W + 20, 16), hexa("#5a5f63"), hexa("#3a3e41"), (0, -3), None, lw=3)
    on = 1.0
    if flicker:
        on = 0.35 if noise(t * 9, 4) > 0.55 else 1.0
    lx = W * 0.5
    toon(cr, lambda c: c.rectangle(lx - 140, H * 0.03, 280, 14), hexa("#e8f0f2"), None, (0, 0), None, lw=3)
    glow(cr, lx, H * 0.04, 700 * max(U, 0.7), (0.85, 0.95, 1), 0.35 * on)
    if screen is not None:                                     # the wall screen
        sw, sh = (W * 0.8, H * 0.24) if V else (W * 0.56, H * 0.36)
        sx0, sy0 = (W - sw) / 2, H * (0.16 if V else 0.13)
        toon(cr, lambda c: tk.tk_rrect(c, sx0 - 14, sy0 - 14, sw + 28, sh + 28, 10), hexa("#1d1f22"), None, (0, 0),
             None, lw=5)
        cr.save()
        cr.rectangle(sx0, sy0, sw, sh)
        cr.clip()
        cr.set_source_rgba(0.02, 0.04, 0.05, 1)
        cr.paint()
        screen(cr, sx0, sy0, sw, sh)
        for yy in range(int(sy0), int(sy0 + sh), 4):           # scan lines
            cr.set_source_rgba(0, 0, 0, 0.18)
            cr.rectangle(sx0, yy, sw, 1.5)
            cr.fill()
        cr.restore()
        glow(cr, W / 2, sy0 + sh / 2, sw * 0.7, (0.4, 0.9, 1), 0.18)
    dx = W * (0.86 if not V else 0.82)                         # the sealed door
    dy0 = H * (0.43 if V else 0.36)
    toon(cr, lambda c: c.rectangle(dx - 70, dy0, 140, H * 0.62 - dy0), hexa("#555b60"), hexa("#3a3f43"), (-4, -4), None,
         lw=4)
    cr.set_source_rgba(0.8, 0.15, 0.1, 0.9)
    cr.arc(dx + 44, (dy0 + H * 0.62) / 2, 6, 0, 2 * math.pi)
    cr.fill()
    for cx, cy, sx in ((W * 0.06, H * 0.12, 1), (W * 0.94, H * 0.12, -1)):   # cameras
        camera_unit(cr, t, cx, cy, sx, 0.8 * max(U, 0.75))
    if dark > 0:
        cr.set_source_rgba(0, 0, 0, dark)
        cr.paint()


def camera_unit(cr, t, x, y, sx, s, turn=0.0):
    """A ceiling camera on a bracket, its red light blinking."""
    cr.save()
    cr.translate(x, y)
    cr.scale(sx * s, s)
    toon(cr, lambda c: c.rectangle(-8, -60, 16, 60), hexa("#7b8085"), hexa("#55595d"), (-2, -2), None, lw=3)
    cr.rotate(0.45 + turn)
    toon(cr, lambda c: tk.tk_rrect(c, -20, -24, 120, 48, 12), hexa("#d9dcdf"), hexa("#9ea3a8"), (-4, -4), None, lw=3.5)
    toon(cr, lambda c: c.arc(100, 0, 20, 0, 2 * math.pi), hexa("#16181b"), None, (0, 0), None, lw=3)
    on = 1.0 if (t % 1.2) < 0.7 else 0.25
    glow(cr, 12, -12, 16, (1, 0.15, 0.1), 0.8 * on)
    cr.set_source_rgba(1, 0.15, 0.1, on)
    cr.arc(12, -12, 5, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def screen_text(lines, col=(0.55, 1, 0.85, 1), size=None, momo_at=None, t=0.0):
    """A screen painter: centred mono lines (and Momo, if momo_at = its pop-in 0..1)."""
    def paint(cr, x0, y0, w, h):
        n = len(lines)
        sz = size or min(h / (n + 1.6), 46 * max(U, 0.8))
        for k, ln in enumerate(lines):
            fit = min(sz, sz * (w - 40) / max(1, text_width(cr, ln, sz, "Liberation Mono")))
            yy = y0 + h * (k + 1) / (n + 1) + fit * 0.35
            glow(cr, x0 + w / 2, yy - fit * 0.3, w * 0.35, col[:3], 0.08)
            hud2d._text(cr, ln, x0 + w / 2, yy, fit, col, "Liberation Mono", "center")
        if momo_at is not None and momo_at > 0:
            momo(cr, x0 + w * 0.5, y0 + h * 0.98 + (1 - momo_at) * h, h * 0.0034, t)
    return paint


def lying_students(cr, t, stir=0.0):
    """From above: Class 3-B on the concrete floor, uniforms in a scatter, some starting to move."""
    cr.set_source_rgba(0.24, 0.24, 0.25, 1)
    cr.paint()
    cr.set_source_rgba(0, 0, 0, 0.12)
    for k in range(12):
        cr.rectangle(0, k * H / 12, W, 2)
    cr.fill()
    for k in range(20):
        u, v = (k * 0.618 + 0.11) % 1, (k * 0.7548 + 0.07) % 1
        x, y = W * (0.1 + 0.8 * u), H * (0.1 + 0.8 * v)
        ang = (k * 1.7) % (2 * math.pi)
        f = k % 3 == 0 or k in (1, 4, 6)
        sc = 0.8 * max(U, 0.75)
        cr.save()
        cr.translate(x, y + 3 * stir * math.sin(t * 3 + k) * (k % 4 == 0))
        cr.rotate(ang)
        cr.scale(sc, sc)
        legs = hexa("#1b1f2b") if not f else hexa("#e9d4c0")
        for sy in (-1, 1):                                     # legs
            toon(cr, lambda c, sy=sy: tk.tk_rrect(c, 40, sy * 12 - 9, 90, 18, 9), legs, None, (-2, -2), None, lw=2.5)
        if f:                                                  # pleated skirt
            toon(cr, lambda c: poly(c, [(20, -26), (66, -34), (66, 34), (20, 26)]), SAILOR[0], SAILOR[1], (-2, -2),
                 None, lw=2.5)
        toon(cr, lambda c: tk.tk_rrect(c, -40, -26, 66, 52, 16), *(SAILOR[:2] if f else GAKURAN[:2]), (-3, -3), None,
             lw=3)                                             # torso
        for sy in (-1, 1):                                     # arms flung out
            toon(cr, lambda c, sy=sy: (c.save(), c.translate(-30, sy * 22), c.rotate(sy * (0.6 + 0.3 * (k % 3))),
                                       tk.tk_rrect(c, 0, -7, 56, 14, 7), c.restore()),
                 *(SAILOR[:2] if f else GAKURAN[:2]), (-2, -2), None, lw=2.5)
        sk = SKIN[k % 4]
        toon(cr, lambda c: c.arc(-62, 0, 24, 0, 2 * math.pi), sk, mix(sk, (0, 0, 0, 1), 0.2), (-3, -3), None, lw=3)
        hair = (EXTRAS + list(CAST.values()))[k % 20]["hair"]
        toon(cr, lambda c: (c.save(), c.translate(-70, 0), c.scale(0.95, 1.05), c.arc(0, 0, 25, math.pi * 0.45,
                                                                                          math.pi * 1.55),
                            c.restore()), hair, None, (0, 0), None, lw=2.5)
        cr.restore()


# ------------------------------------------------------------------ the Glass Auction
def glass_case(cr, t, x, y, s, glow_k=1.0):
    """The exit key on a velvet stand inside a glass case."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    toon(cr, lambda c: c.rectangle(-110, 120, 220, 70), hexa("#2c2f33"), hexa("#1a1c1f"), (0, -4), None, lw=4)
    toon(cr, lambda c: c.rectangle(-60, 60, 120, 60), hexa("#7a1a22"), hexa("#4a0e14"), (0, -4), None, lw=3)
    glow(cr, 0, 30, 140, (1, 0.85, 0.45), 0.4 * glow_k)
    cr.save()                                                  # the key
    cr.translate(0, 30)
    cr.rotate(-0.4 + 0.05 * math.sin(t))
    toon(cr, lambda c: (c.arc(-40, 0, 22, 0, 2 * math.pi)), hexa("#e8c04a"), hexa("#a8821c"), (-3, -3),
         (1, 1, 0.8, 0.6), (-4, -4), lw=3)
    cr.set_source_rgba(0.06, 0.05, 0.03, 1)
    cr.arc(-40, 0, 9, 0, 2 * math.pi)
    cr.fill()
    toon(cr, lambda c: c.rectangle(-20, -6, 80, 12), hexa("#e8c04a"), hexa("#a8821c"), (-2, -2), None, lw=3)
    toon(cr, lambda c: poly(c, [(40, 6), (40, 22), (50, 22), (50, 14), (58, 14), (58, 6)]), hexa("#e8c04a"),
         hexa("#a8821c"), (-2, -2), None, lw=2.5)
    cr.restore()
    cr.set_source_rgba(0.8, 0.92, 1, 0.12)                     # the glass
    cr.rectangle(-100, -100, 200, 220)
    cr.fill()
    cr.set_source_rgba(0.85, 0.95, 1, 0.7)
    cr.set_line_width(4)
    cr.rectangle(-100, -100, 200, 220)
    cr.stroke()
    cr.set_source_rgba(1, 1, 1, 0.35)
    cr.set_line_width(6)
    cr.move_to(-80, -60)
    cr.line_to(-40, -100)
    cr.move_to(-80, 0)
    cr.line_to(0, -90)
    cr.stroke()
    cr.restore()


def terminal(cr, t, x, y, s, tokens=100, bid=None, who_hand=None):
    """A bidding tablet on its stand: TOKENS 100, BID ___ and a keypad."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    toon(cr, lambda c: tk.tk_rrect(c, -170, -230, 340, 460, 26), hexa("#222428"), hexa("#141518"), (-4, -4),
         (0.5, 0.9, 1, 0.35), (0, -6), lw=5)
    cr.set_source_rgba(0.03, 0.06, 0.08, 1)
    tk.tk_rrect(cr, -146, -206, 292, 300, 14)
    cr.fill()
    glow(cr, 0, -60, 200, (0.4, 0.9, 1), 0.15)
    hud2d._text(cr, "TOKENS", -120, -150, 30, (0.55, 1, 0.85, 0.8), "Liberation Mono")
    hud2d._text(cr, str(tokens), -120, -84, 70, (0.55, 1, 0.85, 1), "Liberation Mono")
    hud2d._text(cr, "BID", -120, -20, 30, (1, 0.8, 0.4, 0.85), "Liberation Mono")
    hud2d._text(cr, "___" if bid is None else str(bid), -40, -20, 40, (1, 0.8, 0.4, 1), "Liberation Mono")
    for r in range(3):                                         # keypad
        for c in range(3):
            n = r * 3 + c + 1
            toon(cr, lambda cc, r=r, c=c: tk.tk_rrect(cc, -120 + c * 84, 110 + r * 34, 72, 28, 6), hexa("#3a3e44"),
                 None, (0, 0), None, lw=2)
            hud2d._text(cr, str(n), -84 + c * 84, 132 + r * 34, 20, (0.85, 0.88, 0.9, 1), "Liberation Mono", "center")
    cr.restore()


# ------------------------------------------------------------------ overlays
def name_card(cr, t, start, end, who, x=None, y=None, side=1):
    """Anime-style freeze label: a slanted black band with the name and a red tag line, sliding in."""
    if t < start or t > end + 0.25:
        return
    name, tag = NAMES[who]
    p = clamp01((t - start) / 0.18)
    a = 1 - clamp01((t - end) / 0.25)
    sz = 34 if V else 30
    w = max(text_width(cr, name, sz, hud2d.ROUND), text_width(cr, tag.upper(), sz * 0.55, hud2d.ROUND)) + 60
    x = x if x is not None else (W * 0.06 if side > 0 else W * 0.94 - w)
    y = y if y is not None else H * (0.64 if V else 0.68)
    cr.save()
    cr.push_group()
    cr.translate(x - (1 - p) * 60 * side, y)
    cr.rotate(-0.05)
    cr.set_source_rgba(0.04, 0.04, 0.06, 0.9)
    poly(cr, [(0, -sz * 1.1), (w, -sz * 1.1), (w - 18, sz * 0.95), (-18, sz * 0.95)])
    cr.fill()
    cr.set_source_rgba(*hud2d.RED)
    cr.rectangle(-18, sz * 0.95, w, 6)
    cr.fill()
    hud2d._text(cr, name, 18, sz * 0.05, sz, (1, 1, 1, 1), hud2d.ROUND)
    hud2d._text(cr, tag.upper(), 18, sz * 0.75, sz * 0.55, hud2d.RED, hud2d.ROUND)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def status_bar(cr, t, left, right=None, alert=False):
    """The thin top bar: '● CLASS 3-B · 12:16:43' on the left, a status on the right."""
    h = 54 if V else 44
    cr.set_source_rgba(0.02, 0.02, 0.03, 0.82)
    cr.rectangle(0, 0, W, h)
    cr.fill()
    dot = 1.0 if (t % 1.0) < 0.6 else 0.3
    cr.set_source_rgba(*(hud2d.RED[:3] if alert else (0.4, 1, 0.6)), dot)
    cr.arc(22, h / 2, 7, 0, 2 * math.pi)
    cr.fill()
    hud2d._text(cr, left, 40, h / 2 + 9, 24 if V else 21, (1, 1, 1, 0.95), "Liberation Mono")
    if right:
        hud2d._text(cr, right, W - 18, h / 2 + 9, 22 if V else 19, (*(hud2d.RED[:3] if alert else (1, 0.85, 0.4)), 1),
                    "Liberation Mono", "right")


def flash(cr, t, at, dur=0.5):
    if at <= t < at + dur:
        cr.set_source_rgba(1, 0.97, 0.9, 1 - (t - at) / dur)
        cr.paint()
