"""The leather cast and props for the Jarasandha reel (Togalu Gombeyaata style): profile figures with big almond eyes,
tall crowns, perforated garments and jointed arms and legs; the two half-babies (frontal, one red and one green, each
with a punched decorative edge where it is cut); Jara the rakshasi; and the leather sets (palace arch, mango tree,
mango, moon, sun, cages, fire, cradle, palm-leaf book, clouds, wall).

Every sprite is drawn once in design units (a standing figure is ~1000 units tall, feet near y=+470 below the hip
pivot) and cached by puppet_core. Rigs list parts back to front.
"""
import math

from puppet_core import (BLUE, BROWN, DGREEN, DRED, GOLD, GREEN, INK, OCHRE, PALE, PARCH, RED, ROSE, SAFFRON,
                         SKIN, VIOLET, Rig, band, cut, dots_in, ell, holes_line, ink, leather, perforate, poly, punch,
                         register, rivet, spath, almond_eye)

HAIR = (0.20, 0.13, 0.10)
CREAM = (1.0, 0.93, 0.74)
BABY_L = (0.97, 0.40, 0.26)      # the half born to the first queen
BABY_R = (0.42, 0.74, 0.30)      # the half born to the second queen
JARA_SKIN = (0.36, 0.30, 0.40)


# ------------------------------------------------------------------ shared pieces


def _shape(cr, pts, col, lw=6.0, smooth=True, holes=None, keep_path=False):
    """Fill + outline a closed shape; holes=(inset, spacing, r) punches a perforated border."""
    cr.new_path()
    (spath if smooth else poly)(cr, pts, closed=True)
    pl = leather(cr, col, lw, keep=True)
    if holes:
        perforate(cr, pl, *holes)
    return pl


def _two_tone(cr, pts, colA, colB, seam, lw=6.0, smooth=True, holes=None):
    """A shape dyed colA left of x=seam and colB right of it, with a stitched seam (Jarasandha's two halves)."""
    cr.new_path()
    (spath if smooth else poly)(cr, pts, closed=True)
    path = cr.copy_path()
    cr.set_source_rgb(*colA)
    cr.fill()
    cr.save()
    cr.rectangle(seam, -5000, 10000, 10000)
    cr.clip()
    cr.append_path(path)
    cr.set_source_rgb(*colB)
    cr.fill()
    cr.restore()
    cr.save()
    cr.append_path(path)
    cr.clip()
    zz = [(seam + (5 if i % 2 else -5), -1200 + 18 * i) for i in range(140)]
    ink(cr, zz, 3.0, smooth=False)
    cr.restore()
    cr.append_path(path)
    cr.set_source_rgb(*INK)
    cr.set_line_width(lw)
    cr.stroke()
    if holes:
        cr.append_path(path)
        from puppet_core import flat_pts
        pl = flat_pts(cr)
        cr.new_path()
        perforate(cr, pl, *holes)


def _skin(cr, pts, o, lw=6.0, holes=None, side=None):
    """Skin-coloured shape; two-tone when o has 'seam' (side forces one colour for limbs)."""
    if side == "A":
        return _shape(cr, pts, o["skin"], lw, holes=holes)
    if side == "B":
        return _shape(cr, pts, o.get("skin2", o["skin"]), lw, holes=holes)
    if o.get("seam") is not None:
        return _two_tone(cr, pts, o["skin"], o["skin2"], o["seam"] + o.get("seam_dx", 0), lw, holes=holes)
    return _shape(cr, pts, o["skin"], lw, holes=holes)


def _jewel(cr, x, y, r, col=GOLD):
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    leather(cr, col, 3.0)
    punch(cr, [(x, y)], r * 0.38)


def _flower(cr, x, y, r, col=GOLD, n=6):
    pts = []
    for i in range(n * 2):
        a = math.pi * i / n
        rr = r if i % 2 == 0 else r * 0.5
        pts.append((x + rr * math.cos(a), y + rr * math.sin(a)))
    _shape(cr, pts, col, 3.0)
    punch(cr, [(x, y)], r * 0.25)


# ------------------------------------------------------------------ male figure (profile, facing +x)


def man_body(cr, o):
    b = o.get("bulk", 1.0)
    sc = o.get("sash", RED)
    # back sash tails, fluttering behind
    for dy, ln in ((0, 1.0), (22, 0.75)):
        pts = [(-50 * b, -26 + dy), (-92 * b, -6 + dy), (-118 * b * ln, 40 + dy), (-128 * b * ln, 92 + dy)]
        band(cr, pts, 14, sc, holes=True, spacing=12, hole_r=2.2)
    torso = [(-46 * b, -6), (-54 * b, -100), (-62 * b, -190), (-56 * b, -246), (-30, -284), (-10, -300), (24, -300),
             (36 * b + 4, -282), (68 * b, -252), (86 * b, -208), (82 * b, -160), (64 * b, -110), (55 * b, -50),
             (50 * b, -6)]
    _skin(cr, torso, o)
    ink(cr, [(36 * b, -222), (62 * b, -192), (80 * b, -176)], 4)                 # chest
    holes_line(cr, [(30 * b, -206), (54 * b, -176), (70 * b, -160)], 11, 2.4)
    holes_line(cr, [(-46 * b, -230), (-50 * b, -150), (-42 * b, -70)], 13, 2.4)
    holes_line(cr, [(20 * b, -150), (40 * b, -120), (44 * b, -60)], 13, 2.2)
    ink(cr, [(40 * b, -132), (60 * b, -122)], 3.5)
    punch(cr, [(46 * b, -78)], 4.5)                                           # navel
    if o.get("thread"):                                                        # sacred thread: a line of light
        cr.save()
        cr.set_operator(0)
        spath(cr, [(-44 * b, -258), (0, -170), (34 * b, -90), (52 * b, -28)], closed=False)
        cr.set_line_width(6)
        cr.stroke()
        cr.restore()
    nk = o.get("neck", GOLD)
    band(cr, [(-12, -290), (26 * b, -252), (64 * b, -222)], 13, nk, spacing=12)
    band(cr, [(-26, -282), (14 * b, -200), (56 * b, -150)], 9, nk, spacing=11, hole_r=2.2)
    _jewel(cr, 60 * b, -136, 12, RED)
    if o.get("beads"):
        for i in range(12):
            u = i / 11
            x, y = -24 + (70 * b) * u, -276 + 150 * u * u + 40 * u
            cr.new_path()
            cr.arc(x, y, 7, 0, 2 * math.pi)
            cr.set_source_rgb(*INK)
            cr.fill()
    if o.get("robe"):                                                          # sage's robe across the chest
        rp = [(-60 * b, -250), (-20, -270), (30, -150), (60 * b, -60), (58 * b, -10), (-50 * b, -10), (-62 * b, -150)]
        _shape(cr, rp, o["robe"], 5, holes=(10, 14, 2.8))
        ink(cr, [(-30, -230), (10, -130), (40, -40)], 3)
    # waist wrap
    wrap = [(-62 * b, -40), (0, -50), (64 * b, -42), (74 * b, 10), (70 * b, 48), (0, 56), (-70 * b, 48), (-74 * b, 10)]
    pl = _shape(cr, wrap, o["dhoti"], 6)
    dots_in(cr, lambda: spath(cr, wrap), 20, 3.0)
    band(cr, [(-64 * b, -32), (0, -42), (66 * b, -34)], 14, o.get("border", GOLD), spacing=12)
    # front pleats hanging over the legs
    pf = [(24 * b, 30), (60 * b, 26), (100 * b, 246), (88 * b, 262), (76 * b, 248), (64 * b, 264), (50 * b, 248),
          (38 * b, 262), (26 * b, 246), (16 * b, 258)]
    _shape(cr, pf, o.get("pleat", o.get("border", GOLD)), 5, smooth=False)
    for u in (0.3, 0.55, 0.8):
        ink(cr, [(24 * b + 36 * b * u, 34), (20 * b + 80 * b * u, 250)], 3, smooth=False)
    holes_line(cr, [(28 * b, 236), (94 * b, 232)], 12, 2.6)
    rivet(cr, 16 * b, 6, 7)


def man_head(cr, o):
    crown = o.get("crown", "kirita")
    if crown == "kirita" and o.get("halo", True):            # flame halo behind the crown
        pts = []
        for i in range(19):
            a = math.pi * (0.62 + 0.9 * i / 18)
            r = 160 if i % 2 == 0 else 128
            pts.append((-30 + r * math.cos(a) * 1.05, -190 + r * math.sin(a) * 1.1))
        pts += [(-40, -150), (0, -160)]
        _shape(cr, pts, o.get("halo_col", RED), 5, smooth=False, holes=(14, 15, 3))
    if o.get("hair", True):                                     # long hair down the back
        hp = [(-30, -176), (-62, -146), (-84, -80), (-88, 0), (-74, 64), (-50, 84), (-40, 30), (-36, -40), (-20, -90)]
        _shape(cr, hp, HAIR, 5)
        for k in range(4):
            holes_line(cr, [(-46 - 8 * k, -140 + 10 * k), (-70 - 4 * k, -40), (-62 - 2 * k, 50)], 16, 2.4)
    face = [(-24, 6), (-30, -38), (-50, -82), (-56, -130), (-42, -174), (0, -196), (40, -184), (56, -152),
            (60, -128), (66, -116), (92, -92), (68, -82), (70, -72), (62, -64), (66, -56), (56, -44), (52, -30),
            (34, -22), (26, 6)]
    _skin(cr, face, o)
    ink(cr, [(68, -70), (60, -68)], 3)                                           # lips
    almond_eye(cr, 34, -118, 38, 13, col=PALE)
    ink(cr, [(14, -136), (34, -144), (56, -136)], 4.5)                            # brow
    cr.new_path()
    ell(cr, -14, -108, 13, 21)
    leather(cr, o["skin"], 4)
    if o.get("tilak", True):
        ink(cr, [(52, -150), (54, -170)], 5, col=RED)
    if o.get("moustache"):
        m = [(64, -74), (44, -82), (26, -86), (14, -102), (24, -94), (44, -86), (66, -79)]
        _shape(cr, m, HAIR, 3)
    if o.get("whiskers"):
        ink(cr, [(20, -70), (8, -60), (14, -48)], 5, col=HAIR)
    if o.get("beard"):
        bp = [(60, -50), (62, -22), (56, 40), (40, 120), (20, 70), (0, 20), (6, -40), (28, -54)]
        _shape(cr, bp, CREAM, 4)
        for k in range(3):
            ink(cr, [(46 - 10 * k, -40), (40 - 12 * k, 20), (34 - 10 * k, 80)], 2.5)
    # crowns
    if crown == "kirita":
        kp = [(-50, -150), (-48, -196), (-34, -252), (-18, -312), (0, -350), (18, -312), (34, -252), (50, -196),
              (56, -150)]
        _shape(cr, kp, o.get("crown_col", GOLD), 6, smooth=False, holes=(11, 14, 2.8))
        for y, w in ((-196, 46), (-252, 32)):
            band(cr, [(-w - 2, y), (w + 4, y - 2)], 12, RED, spacing=11, hole_r=2.4)
        _jewel(cr, 4, -222, 13, RED)
        _jewel(cr, 2, -282, 10, GREEN)
        cr.new_path()
        cr.arc(0, -360, 13, 0, 2 * math.pi)
        leather(cr, GOLD, 4)
        poly(cr, [(-6, -370), (0, -404), (6, -370)])
        leather(cr, GOLD, 3)
        fl = [(-48, -168), (-96, -200), (-112, -170), (-96, -140), (-60, -140)]           # side flare
        _shape(cr, fl, RED, 4, holes=(9, 12, 2.4))
        band(cr, [(-52, -156), (60, -150)], 16, GOLD, spacing=12)
    elif crown == "tiara":
        pass
    elif crown == "feather":                                  # Krishna: hair knot with a peacock feather
        _shape(cr, [(-44, -150), (-36, -196), (0, -212), (38, -196), (50, -160), (0, -176)], HAIR, 4)
        band(cr, [(-46, -160), (52, -158)], 14, GOLD, spacing=12)
        ink(cr, [(-10, -196), (-30, -260), (-60, -330)], 6, col=INK)
        for r, col in ((54, GREEN), (40, GOLD), (28, BLUE), (14, INK)):
            cr.new_path()
            ell(cr, -66, -360, r * 0.75, r, -0.35)
            leather(cr, col, 3)
        punch(cr, [(-64, -364)], 4)
        for k in range(9):                                     # feather barbs
            a = -0.35 + (k - 4) * 0.28
            ink(cr, [(-66 - 50 * math.sin(a), -360 + 56 * math.cos(a)),
                     (-66 - 72 * math.sin(a), -360 + 80 * math.cos(a))], 2.5, col=DGREEN)
    elif crown == "shikha":                                   # Brahmin top-knot
        _shape(cr, [(-46, -150), (-40, -192), (0, -206), (40, -190), (46, -160), (0, -172)], HAIR, 4)
        cr.new_path()
        cr.arc(-34, -206, 24, 0, 2 * math.pi)
        leather(cr, HAIR, 4)
        holes_line(cr, [(-50, -206), (-34, -224), (-18, -206)], 9, 2.2)
    elif crown == "jata":                                     # sage: piled matted hair
        for k in range(5):
            cr.new_path()
            ell(cr, -6 - 3 * k, -196 - 30 * k, 50 - 5 * k, 22)
            leather(cr, (0.45, 0.28, 0.14), 4)
            ink(cr, [(-40 + 6 * k, -196 - 30 * k), (-6, -186 - 30 * k), (30 - 6 * k, -198 - 30 * k)], 2.5)
        for i in range(7):
            cr.new_path()
            cr.arc(-44 + 14 * i, -178, 6, 0, 2 * math.pi)
            cr.set_source_rgb(*INK)
            cr.fill()
    if o.get("earring", True):
        _jewel(cr, -12, -72, 16, GOLD)
        poly(cr, [(-20, -58), (-12, -36), (-4, -58)])
        leather(cr, RED, 3)


def upper_arm(cr, o, side=None):
    b = o.get("bulk", 1.0)
    pts = [(-28 * b, -8), (-18 * b, -30), (0, -36 * b), (20 * b, -30), (30 * b, -8), (25 * b, 80), (18 * b, 150),
           (0, 164), (-18 * b, 150), (-25 * b, 80)]
    _skin(cr, pts, o, 5, side=side)
    band(cr, [(-27 * b, 46), (27 * b, 50)], 14, o.get("neck", GOLD), spacing=10, hole_r=2.4)
    poly(cr, [(-9, 42), (0, 20), (9, 42)])
    leather(cr, GOLD, 3)
    rivet(cr, 0, 0, 6.5)


def fore_arm(cr, o, side=None, hand="open"):
    b = o.get("bulk", 1.0)
    pts = [(-19 * b, -6), (0, -22 * b), (19 * b, -6), (16 * b, 90), (13 * b, 128), (-13 * b, 128), (-16 * b, 90)]
    _skin(cr, pts, o, 5, side=side)
    col = o["skin"] if side != "B" else o.get("skin2", o["skin"])
    if hand == "open":
        hp = [(-13, 122), (14, 122), (24, 148), (22, 176), (12, 196), (4, 186), (-2, 162), (-14, 146)]
        _shape(cr, hp, col, 4)
        _shape(cr, [(14, 136), (32, 146), (30, 158), (16, 154)], col, 3)
        ink(cr, [(8, 150), (12, 182)], 2.5)
    elif hand == "fist":
        cr.new_path()
        ell(cr, 2, 148, 22, 26)
        leather(cr, col, 4)
        ink(cr, [(-8, 140), (16, 140)], 2.5)
        ink(cr, [(-8, 152), (16, 152)], 2.5)
    elif hand == "claw":
        hp = [(-14, 122), (16, 122), (26, 150), (30, 196), (20, 172), (14, 200), (6, 172), (-2, 196), (-6, 164),
              (-14, 180), (-16, 146)]
        _shape(cr, hp, col, 4, smooth=False)
    for y in (106, 118):
        band(cr, [(-15 * b, y), (15 * b, y + 2)], 8, o.get("neck", GOLD), spacing=9, hole_r=2.0)
    rivet(cr, 0, 0, 6)


def leg(cr, o, side=None):
    b = o.get("bulk", 1.0)
    shin = [(-24 * b, 196), (18 * b, 196), (16 * b, 300), (12 * b, 388), (-10 * b, 392), (-24 * b, 300)]
    _skin(cr, shin, o, 5, side=side)
    col = o["skin"] if side != "B" else o.get("skin2", o["skin"])
    foot = [(-14, 382), (14, 380), (32, 396), (70, 410), (72, 424), (-16, 426)]
    _shape(cr, foot, col, 4)
    band(cr, [(-12 * b, 374), (14 * b, 374)], 9, GOLD, spacing=8, hole_r=2.0)
    dl = [(-42 * b, -10), (0, -26), (46 * b, -10), (54 * b, 80), (46 * b, 170), (32 * b, 214), (-26 * b, 214),
          (-38 * b, 170), (-48 * b, 80)]
    pl = _shape(cr, dl, o["dhoti"], 5)
    dots_in(cr, lambda: spath(cr, dl), 19, 2.8)
    band(cr, [(-30 * b, 204), (34 * b, 204)], 14, o.get("border", GOLD), spacing=11, hole_r=2.4)
    ink(cr, [(-10, 20), (-4, 120), (6, 196)], 3)
    rivet(cr, 0, 0, 9)


def man(key, **o):
    """Register a male figure's parts and return its Rig. Options: skin, skin2+seam (two-tone), bulk, dhoti, border,
    pleat, sash, crown (kirita|feather|shikha|jata|none), moustache, beard, thread, beads, robe, hands=(front, back)."""
    o.setdefault("skin", SKIN)
    o.setdefault("dhoti", RED)
    b = o.get("bulk", 1.0)
    hf, hb = o.get("hands", ("open", "open"))
    two = o.get("seam") is not None
    sB, sF = ("A", "B") if two else (None, None)
    register(key + "_body", (-200, -330, 140, 300), lambda cr: man_body(cr, o))
    oh = dict(o, seam_dx=-6)
    register(key + "_head", (-190, -420, 110, 100), lambda cr: man_head(cr, oh))
    register(key + "_armF_up", (-45, -50, 45, 175), lambda cr: upper_arm(cr, o, sF))
    register(key + "_armF_lo", (-45, -30, 45, 210), lambda cr: fore_arm(cr, o, sF, hf))
    register(key + "_armB_up", (-45, -50, 45, 175), lambda cr: upper_arm(cr, o, sB))
    register(key + "_armB_lo", (-45, -30, 45, 210), lambda cr: fore_arm(cr, o, sB, hb))
    register(key + "_legF", (-70, -40, 90, 440), lambda cr: leg(cr, o, sF))
    register(key + "_legB", (-70, -40, 90, 440), lambda cr: leg(cr, o, sB))
    parts = [
        (key + "_armB_up", key + "_body", (-14 * b, -262), 0.30),
        (key + "_armB_lo", key + "_armB_up", (0, 150), -0.25),
        (key + "_legB", key + "_body", (-12 * b, 8), 0.06),
        (key + "_legF", key + "_body", (16 * b, 8), -0.06),
        (key + "_body", None, (0, 0), 0.0),
        (key + "_head", key + "_body", (6, -300), 0.0),
        (key + "_armF_up", key + "_body", (26 * b, -262), -0.32),
        (key + "_armF_lo", key + "_armF_up", (0, 150), -0.55),
    ]
    pts = {"handF": (key + "_armF_lo", (6, 160)), "handB": (key + "_armB_lo", (6, 160)),
           "chest": (key + "_body", (0, -200)), "head": (key + "_head", (10, -110)),
           "top": (key + "_head", (0, -300)), "hip": (key + "_body", (0, 0))}
    rods = [("chest", 30, 0), ("handF", 110, 0)]
    return Rig(parts, pts, rods)


# ------------------------------------------------------------------ female figure (queens, Jara)


def woman_body(cr, o):
    skirt = [(-40, -30), (40, -34), (70, 120), (104, 300), (140, 448), (126, 466), (-110, 466), (-120, 448),
             (-86, 300), (-62, 120)]
    _shape(cr, skirt, o["skirt"], 6)
    dots_in(cr, lambda: spath(cr, skirt), 24, 3.2, shape="d")
    for x0, x1 in ((-10, -40), (10, 20), (30, 70), (50, 110)):
        ink(cr, [(x0, 0), (x1, 440)], 3, smooth=False)
    band(cr, [(-114, 438), (0, 442), (132, 438)], 30, o.get("border", GOLD), spacing=13)
    holes_line(cr, [(-108, 452), (126, 452)], 12, 2.4)
    _shape(cr, [(108, 452), (150, 456), (156, 470), (104, 472)], o["skin"], 4)        # toes
    torso = [(-38, -10), (-46, -120), (-48, -200), (-44, -250), (-20, -288), (18, -296), (36, -272), (60, -232),
             (64, -206), (52, -180), (44, -120), (40, -10)]
    _shape(cr, torso, o["skin"], 6)
    choli = [(-46, -250), (-20, -286), (20, -292), (38, -270), (62, -232), (64, -204), (50, -178), (-46, -176)]
    _shape(cr, choli, o.get("choli", RED), 5, holes=(9, 12, 2.4))
    band(cr, [(-40, -20), (0, -26), (42, -22)], 18, o.get("border", GOLD), spacing=11, hole_r=2.4)
    if o.get("pallu", True):                                   # the sari's end over the shoulder, hanging behind
        pal = [(-6, -280), (30, -282), (8, -200), (-30, -60), (-70, 120), (-110, 110), (-80, -40), (-52, -200)]
        _shape(cr, pal, o.get("pallu_col", o["skirt"]), 5)
        dots_in(cr, lambda: spath(cr, pal), 20, 2.8)
        band(cr, [(-104, 108), (-72, 116)], 14, GOLD, spacing=10, hole_r=2.2)
    band(cr, [(-14, -286), (24, -250), (52, -210)], 11, GOLD, spacing=10, hole_r=2.2)
    _jewel(cr, 54, -204, 10, o.get("gem", GREEN))
    if o.get("ornaments_extra"):
        o["ornaments_extra"](cr)


def woman_head(cr, o):
    if o.get("wild"):                                          # Jara: wild flame-like locks all round the head
        cx, cy = -30, -120
        mass = [(cx + 120 * math.cos(math.radians(a)) * (1 + 0.18 * math.sin(a * 0.31)),
                 cy - 120 * math.sin(math.radians(a)) * (1 + 0.18 * math.cos(a * 0.27))) for a in range(40, 320, 20)]
        _shape(cr, mass, HAIR, 5)
        for i in range(13):
            a0 = math.radians(60 + 250 * i / 12)
            L = 190 + 40 * math.sin(i * 2.3)
            ca, sa = math.cos(a0), -math.sin(a0)
            nx, ny = -sa, ca
            curl = 30 * (1 if i % 2 else -1)
            lock = [(cx + 50 * ca - 26 * nx, cy + 50 * sa - 26 * ny),
                    (cx + L * 0.55 * ca + curl * nx * 0.5, cy + L * 0.55 * sa + curl * ny * 0.5),
                    (cx + L * ca + curl * nx, cy + L * sa + curl * ny),
                    (cx + L * 0.62 * ca + (curl + 22) * nx * 0.6, cy + L * 0.62 * sa + (curl + 22) * ny * 0.6),
                    (cx + 50 * ca + 26 * nx, cy + 50 * sa + 26 * ny)]
            _shape(cr, lock, HAIR if i % 3 else (0.42, 0.10, 0.08), 4)
            holes_line(cr, [(cx + 70 * ca, cy + 70 * sa), (cx + L * 0.75 * ca + curl * nx * 0.6,
                                                             cy + L * 0.75 * sa + curl * ny * 0.6)], 14, 2.6)
    face = [(-20, 6), (-26, -36), (-44, -80), (-50, -126), (-38, -168), (0, -188), (36, -176), (50, -148),
            (54, -126), (58, -116), (76, -96), (60, -88), (63, -78), (56, -70), (60, -62), (50, -48), (46, -36),
            (30, -26), (22, 6)]
    if o.get("wild"):
        face = [(-24, 6), (-30, -40), (-48, -84), (-54, -128), (-40, -172), (0, -192), (40, -180), (56, -150),
                (60, -128), (64, -116), (96, -94), (70, -84), (76, -70), (64, -58), (70, -50), (58, -40), (52, -28),
                (34, -22), (26, 6)]
    _shape(cr, face, o["skin"], 6)
    if not o.get("wild"):
        hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
                (-52, -128)]
        _shape(cr, hair, HAIR, 4)
        cr.new_path()
        cr.arc(-62, -128, 36, 0, 2 * math.pi)
        leather(cr, HAIR, 4)
        for i in range(8):
            a = 2 * math.pi * i / 8
            punch(cr, [(-62 + 24 * math.cos(a), -128 + 24 * math.sin(a))], 3.5)
        _flower(cr, -62, -128, 14, o.get("flower", GOLD))
        tp = [(-30, -172), (-20, -200), (-6, -184), (8, -212), (20, -184), (34, -204), (40, -170)]
        _shape(cr, tp, GOLD, 4, smooth=False)
        _jewel(cr, 8, -190, 7, RED)
        almond_eye(cr, 30, -112, 32, 11, col=PALE)
        ink(cr, [(46, -112), (60, -120)], 3)
        ink(cr, [(14, -128), (30, -134), (46, -128)], 3.5)
        ink(cr, [(62, -74), (56, -70)], 3, col=RED)
        cr.new_path()
        cr.arc(64, -90, 8, 0, 2 * math.pi)
        cr.set_source_rgb(*GOLD)
        cr.set_line_width(3)
        cr.stroke()
        cr.new_path()
        cr.arc(44, -150, 5, 0, 2 * math.pi)
        cr.set_source_rgb(*RED)
        cr.fill()
        _jewel(cr, -10, -70, 11, GOLD)
        poly(cr, [(-24, -58), (-10, -66), (4, -58), (8, -34), (-28, -34)])
        leather(cr, GOLD, 3)
        punch(cr, [(-18, -40), (-10, -40), (-2, -40)], 2.2)
    else:                                                       # Jara's face: round eye, heavy brow, tusks
        cr.new_path()
        cr.arc(28, -120, 22, 0, 2 * math.pi)
        leather(cr, PALE, 4)
        cr.new_path()
        cr.arc(34, -120, 12, 0, 2 * math.pi)
        leather(cr, RED, 3)
        cr.arc(36, -120, 6, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        punch(cr, [(38, -124)], 2.5)
        _shape(cr, [(4, -146), (30, -160), (62, -150), (58, -140), (30, -148), (6, -138)], HAIR, 3)
        for tx in (52, 64):                                      # tusks curving up from the mouth
            _shape(cr, [(tx - 8, -58), (tx + 2, -60), (tx + 14, -90), (tx + 10, -98), (tx - 2, -76)], PALE, 3,
                   smooth=False)
        ink(cr, [(76, -64), (48, -60)], 4)
        _jewel(cr, -12, -70, 16, GOLD)
        cr.new_path()
        cr.arc(-12, -40, 12, 0, 2 * math.pi)
        leather(cr, RED, 3)
        ink(cr, [(40, -168), (54, -186)], 5, col=RED)
        band(cr, [(-48, -160), (50, -170)], 14, RED, spacing=11, hole_r=2.4)


def woman(key, **o):
    """Register a female figure (queens; Jara with wild=True). Options: skin, skirt, choli, border, pallu_col, gem,
    flower, wild, hands=(front, back), size."""
    o.setdefault("skin", SKIN)
    o.setdefault("skirt", GREEN)
    hf, hb = o.get("hands", ("open", "open"))
    register(key + "_body", (-140, -310, 170, 490), lambda cr: woman_body(cr, o))
    register(key + "_head", (-260, -380, 120, 110) if o.get("wild") else (-120, -240, 100, 30),
             lambda cr: woman_head(cr, o))
    ob = dict(o, bulk=o.get("bulk", 0.85))
    register(key + "_armF_up", (-45, -50, 45, 175), lambda cr: upper_arm(cr, ob))
    register(key + "_armF_lo", (-45, -30, 45, 210), lambda cr: fore_arm(cr, ob, None, hf))
    register(key + "_armB_up", (-45, -50, 45, 175), lambda cr: upper_arm(cr, ob))
    register(key + "_armB_lo", (-45, -30, 45, 210), lambda cr: fore_arm(cr, ob, None, hb))
    parts = [
        (key + "_armB_up", key + "_body", (-12, -262), 0.15),
        (key + "_armB_lo", key + "_armB_up", (0, 150), -0.2),
        (key + "_body", None, (0, 0), 0.0),
        (key + "_head", key + "_body", (2, -292), 0.0),
        (key + "_armF_up", key + "_body", (22, -262), -0.08),
        (key + "_armF_lo", key + "_armF_up", (0, 150), -0.35),
    ]
    pts = {"handF": (key + "_armF_lo", (6, 160)), "handB": (key + "_armB_lo", (6, 160)),
           "chest": (key + "_body", (0, -200)), "head": (key + "_head", (10, -110)),
           "top": (key + "_head", (0, -200)), "hip": (key + "_body", (0, 0))}
    return Rig(parts, pts, [("chest", 30, 0), ("handF", 140, 0)])


# ------------------------------------------------------------------ the two half-babies (frontal)


def baby_body(cr, s, col):
    """Half a baby, cut down the middle: s=-1 the left half, s=+1 the right half; x=0 is the cut edge."""
    X = lambda x: -s * x
    torso = [(0, -244), (X(-60), -242), (X(-118), -218), (X(-150), -176), (X(-154), -100), (X(-140), -36),
             (X(-118), 6), (X(-70), 24), (0, 28)]
    cr.new_path()
    poly(cr, [(0, 28), (0, -244)], closed=False)
    spath(cr, torso[1:-1], closed=False, cont=True)
    cr.line_to(0, 28)
    cr.close_path()
    leather(cr, col, 7)
    langot = [(0, -14), (X(-112), -12), (X(-96), 30), (X(-50), 56), (0, 66)]
    cr.new_path()
    poly(cr, langot)
    pl = leather(cr, GOLD, 5, keep=True)
    perforate(cr, pl, 9, 13, 2.6)
    band(cr, [(0, -18), (X(-60), -18), (X(-116), -22)], 16, RED if s < 0 else DGREEN, spacing=12)
    # head
    head = [(X(-70), -598), (X(-128), -566), (X(-166), -500), (X(-174), -424), (X(-160), -350), (X(-126), -292),
            (X(-72), -262)]
    cr.new_path()
    cr.move_to(0, -246)
    cr.line_to(0, -606)
    spath(cr, head, closed=False, cont=True)
    cr.line_to(X(-40), -256)
    cr.line_to(0, -250)
    cr.close_path()
    leather(cr, col, 7)
    cr.new_path()
    ell(cr, X(-176), -428, 24, 40)
    leather(cr, col, 5)
    _jewel(cr, X(-180), -378, 13, GOLD)
    # hair tuft (half a top-knot) and forehead
    cr.new_path()
    cr.move_to(0, -650)
    cr.curve_to(X(-40), -650, X(-58), -620, X(-40), -596)
    cr.line_to(0, -600)
    cr.close_path()
    leather(cr, HAIR, 5)
    ink(cr, [(X(-150), -520), (X(-110), -572), (X(-50), -596)], 5, col=HAIR)
    ink(cr, [(X(-108), -482), (X(-74), -494), (X(-36), -486)], 6)                 # brow
    ink(cr, [(0, -392), (X(-22), -376), (X(-6), -362)], 5)                          # half a nose
    ink(cr, [(0, -320), (X(-26), -322), (X(-44), -334)], 6, col=DRED)               # half a mouth
    cr.new_path()
    cr.arc(X(-110), -352, 22, 0, 2 * math.pi)
    cr.set_source_rgb(*(DRED if s < 0 else DGREEN))
    cr.set_line_width(3)
    cr.stroke()
    punch(cr, [(X(-110) + 12 * math.cos(a), -352 + 12 * math.sin(a)) for a in [i * 1.047 for i in range(6)]], 2.6)
    band(cr, [(0, -226), (X(-70), -222), (X(-124), -196)], 14, GOLD, spacing=11, hole_r=2.4)
    ink(cr, [(X(-60), -150), (X(-110), -120)], 4)
    punch(cr, [(X(-34), -96)], 5)
    # the cut edge: an ochre strip with a row of punched holes, so it reads as a puppet piece, not a wound
    cr.new_path()
    cr.rectangle(min(0, X(-18)), -604, 18, 632)
    leather(cr, OCHRE, 4)
    punch(cr, [(X(-9), -596 + 16 * i) for i in range(39)], 3.4)
    cr.new_path()
    cr.rectangle(min(0, X(-4)), -650, 4, 720)
    cr.set_source_rgb(*INK)
    cr.fill()


def baby_eye(cr, s, shut=False):
    if shut:
        ink(cr, [(-46, 6), (0, -14), (46, 6)], 9)
        for k in (-1, 0, 1):
            ink(cr, [(k * 26, -2), (k * 30, 14)], 4)
        return
    cr.new_path()
    cr.move_to(-50, 0)
    cr.curve_to(-24, -40, 24, -40, 50, 0)
    cr.curve_to(24, 34, -24, 34, -50, 0)
    cr.close_path()
    leather(cr, PALE, 6)
    cr.new_path()
    cr.arc(4 * s, 0, 22, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    punch(cr, [(4 * s + 8, -8)], 6)
    ink(cr, [(-52, -6), (-62, -22)], 5)
    ink(cr, [(52, -6), (62, -22)], 5)
    ink(cr, [(-40, -40), (0, -54), (40, -40)], 7)


def baby_arm(cr, s, col):
    pts = [(-26, -12), (0, -32), (26, -10), (22, 90), (14, 168), (-12, 176), (-26, 160), (-30, 80)]
    _shape(cr, pts, col, 6)
    cr.new_path()
    ell(cr, 0, 196, 28, 32)
    leather(cr, col, 5)
    for k in (-1, 0, 1):
        ink(cr, [(10 * k, 206), (12 * k, 222)], 3)
    band(cr, [(-20, 150), (20, 150)], 12, GOLD, spacing=9, hole_r=2.2)
    band(cr, [(-28, 30), (28, 30)], 14, GOLD, spacing=9, hole_r=2.2)
    rivet(cr, 0, 0, 11)


def baby_leg(cr, s, col):
    pts = [(-36, -10), (0, -30), (36, -10), (32, 110), (24, 200), (-24, 204), (-34, 110)]
    _shape(cr, pts, col, 6)
    fp = [(s * 30, 192), (s * -26, 196), (s * -60, 222), (s * -56, 236), (s * 34, 236)]
    _shape(cr, fp, col, 5)
    band(cr, [(-26, 180), (26, 180)], 12, GOLD, spacing=9, hole_r=2.2)
    rivet(cr, 0, 0, 11)


def baby_mouth(cr, s):
    cr.new_path()
    cr.move_to(0, -350)
    cr.curve_to(-40 * s, -350, -56 * s, -330, -50 * s, -306)
    cr.curve_to(-40 * s, -286, -16 * s, -280, 0, -280)
    cr.close_path()
    leather(cr, (0.35, 0.05, 0.06), 5)
    cr.new_path()
    cr.move_to(0, -300)
    cr.curve_to(-20 * s, -304, -32 * s, -296, -30 * s, -290)
    cr.line_to(0, -286)
    cr.close_path()
    cr.set_source_rgb(*ROSE)
    cr.fill()


for _s, _k, _c in ((-1, "L", BABY_L), (1, "R", BABY_R)):
    bb = (-200, -660, 30, 80) if _s < 0 else (-30, -660, 200, 80)
    register(f"baby{_k}_body", bb, (lambda s, c: lambda cr: baby_body(cr, s, c))(_s, _c))
    register(f"baby{_k}_eye", (-70, -60, 70, 45), (lambda s: lambda cr: baby_eye(cr, s))(_s))
    register(f"baby{_k}_eyeshut", (-70, -60, 70, 45), (lambda s: lambda cr: baby_eye(cr, s, True))(_s))
    register(f"baby{_k}_arm", (-50, -50, 50, 240), (lambda s, c: lambda cr: baby_arm(cr, s, c))(_s, _c))
    register(f"baby{_k}_leg", (-80, -45, 80, 250), (lambda s, c: lambda cr: baby_leg(cr, s, c))(_s, _c))
    register(f"baby{_k}_mouth", (-70, -360, 70, -270), (lambda s: lambda cr: baby_mouth(cr, s))(_s))


def baby_rig(k):
    s = -1 if k == "L" else 1
    parts = [(f"baby{k}_leg", f"baby{k}_body", (s * 72, 14), s * -0.12),
             (f"baby{k}_body", None, (0, 0), 0.0),
             (f"baby{k}_arm", f"baby{k}_body", (s * 128, -196), s * -0.42),
             (f"baby{k}_eye", f"baby{k}_body", (s * 70, -420), 0.0)]
    pts = {"chest": (f"baby{k}_body", (s * 70, -150)), "hand": (f"baby{k}_arm", (0, 196)),
           "head": (f"baby{k}_body", (s * 80, -430)), "mouth": (f"baby{k}_body", (s * 20, -320))}
    return Rig(parts, pts, [("chest", s * 60, 0), ("hand", s * 160, 0)])


BABY = {"L": baby_rig("L"), "R": baby_rig("R")}


# ------------------------------------------------------------------ the cast

KING = man("king", skin=SKIN, dhoti=RED, border=GOLD, pleat=GOLD, sash=DGREEN, moustache=True, crown_col=GOLD,
           halo_col=DRED)
QUEEN1 = woman("queen1", skin=SKIN, skirt=GREEN, choli=RED, border=GOLD, pallu_col=DGREEN, gem=RED)
QUEEN2 = woman("queen2", skin=(0.99, 0.76, 0.56), skirt=RED, choli=GREEN, border=GOLD, pallu_col=DRED, gem=GREEN,
               flower=PALE)
SAGE = man("sage", skin=(0.88, 0.58, 0.34), bulk=0.86, dhoti=SAFFRON, border=DRED, pleat=SAFFRON, sash=SAFFRON,
           crown="jata", beard=True, hair=False, robe=SAFFRON, beads=True, halo=False, earring=False, neck=BROWN,
           hands=("open", "fist"))
JARA = woman("jara", skin=JARA_SKIN, skirt=DRED, choli=(0.20, 0.18, 0.22), border=GOLD, pallu=False, gem=RED,
             wild=True, hands=("claw", "claw"), bulk=1.0)
JSANDHA = man("jsandha", skin=BABY_L, skin2=BABY_R, seam=0, bulk=1.32, dhoti=DRED, border=GOLD, pleat=GOLD,
              sash=GOLD, moustache=True, whiskers=True, crown_col=GOLD, halo_col=DRED, hands=("fist", "fist"))
KRISHNA = man("krishna", skin=BLUE, dhoti=GOLD, border=RED, pleat=RED, sash=GREEN, crown="feather", thread=True,
              hair=True, halo=False)
ARJUNA = man("arjuna", skin=(0.98, 0.74, 0.44), dhoti=PALE, border=RED, pleat=RED, sash=RED, crown="shikha",
             thread=True, moustache=True, hair=False, hands=("open", "fist"))
BHIMA = man("bhima", skin=(0.80, 0.52, 0.26), bulk=1.38, dhoti=PALE, border=BLUE, pleat=BLUE, sash=BLUE,
            crown="shikha", thread=True, moustache=True, whiskers=True, hair=False, hands=("fist", "fist"))


# ------------------------------------------------------------------ props


def _mango(cr):
    pts = [(0, -78), (36, -70), (62, -30), (64, 20), (44, 62), (6, 80), (-34, 66), (-56, 26), (-56, -24), (-34, -64)]
    _shape(cr, pts, GOLD, 6)
    cr.save()
    cr.new_path()
    spath(cr, pts)
    cr.clip()
    cr.new_path()
    ell(cr, 30, -30, 46, 52)
    cr.set_source_rgb(*SAFFRON)
    cr.fill()
    cr.restore()
    cr.new_path()
    spath(cr, pts)
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.stroke()
    punch(cr, [(-20, 10), (-6, 30), (10, 44), (-28, -16), (16, 2)], 3)
    ink(cr, [(0, -78), (6, -100)], 6, col=BROWN)
    leaf = [(6, -96), (40, -120), (86, -112), (50, -92)]
    _shape(cr, leaf, GREEN, 4)
    ink(cr, [(10, -98), (80, -110)], 2.5)


def _mango_half(cr, s):
    """Half a mango, cut down the middle (s=-1 the left half): the cut face shows the pale flesh and the seed."""
    pts = [(0, -78), (s * 35, -66), (s * 58, -26), (s * 60, 24), (s * 40, 64), (0, 80)]
    cr.new_path()
    cr.move_to(0, 80)
    spath(cr, pts, closed=False, cont=True)
    cr.close_path()
    leather(cr, GOLD, 6)
    cr.new_path()
    cr.rectangle(min(0, s * 16), -74, 16, 150)
    leather(cr, PALE, 3)
    cr.new_path()
    ell(cr, s * 10, 0, 10, 44)
    leather(cr, CREAM, 3)
    punch(cr, [(s * 34, -10), (s * 24, 30)], 3)


def _moon(cr):
    cr.new_path()
    cr.arc(0, 0, 120, 0, 2 * math.pi)
    leather(cr, CREAM, 6)
    cut(cr, lambda: cr.arc(52, -30, 104, 0, 2 * math.pi))
    cr.save()
    cr.arc(0, 0, 120, 0, 2 * math.pi)
    cr.clip()
    cr.new_path()
    cr.arc(52, -30, 104, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.stroke()
    cr.restore()
    for i in range(8):
        a = math.radians(118 + 16 * i)
        punch(cr, [(98 * math.cos(a), 98 * math.sin(a))], 4.5)
    ink(cr, [(-92, -10), (-84, 30)], 3)


def _sun(cr):
    pts = []
    for i in range(32):
        a = 2 * math.pi * i / 32
        r = 200 if i % 2 == 0 else 128
        pts.append((r * math.cos(a), r * math.sin(a)))
    _shape(cr, pts, SAFFRON, 6, smooth=False)
    for i in range(16):
        a = 2 * math.pi * (i + 0.5) / 16
        punch(cr, [(150 * math.cos(a), 150 * math.sin(a))], 5)
    cr.new_path()
    cr.arc(0, 0, 112, 0, 2 * math.pi)
    leather(cr, RED, 6)
    cr.new_path()
    cr.arc(0, 0, 86, 0, 2 * math.pi)
    leather(cr, GOLD, 4)
    for i in range(12):
        a = 2 * math.pi * i / 12
        punch(cr, [(66 * math.cos(a), 66 * math.sin(a))], 4.5)
    _flower(cr, 0, 0, 38, RED, 8)


def _star(cr):
    pts = []
    for i in range(8):
        a = math.pi * i / 4
        r = 40 if i % 2 == 0 else 12
        pts.append((r * math.cos(a), r * math.sin(a)))
    _shape(cr, pts, CREAM, 3, smooth=False)


def _arch(cr):
    # pillars
    for s in (-1, 1):
        x0 = s * 410
        pil = [(x0 - 52, 0), (x0 + 52, 0), (x0 + 44, -40), (x0 + 38, -820), (x0 + 56, -860), (x0 - 56, -860),
               (x0 - 38, -820), (x0 - 44, -40)]
        _shape(cr, pil, OCHRE, 7, smooth=False, holes=(12, 16, 3.2))
        dots_in(cr, lambda: poly(cr, [(x0 - 22, -80), (x0 + 22, -80), (x0 + 22, -780), (x0 - 22, -780)]), 22, 4,
                shape="d")
        band(cr, [(x0 - 50, -40), (x0 + 50, -40)], 22, RED, spacing=14)
        band(cr, [(x0 - 48, -820), (x0 + 48, -820)], 22, RED, spacing=14)
    # arch band with cusped opening
    cr.new_path()
    poly(cr, [(-470, -860), (470, -860), (470, -1010), (-470, -1010)])
    pts = []
    for i in range(121):
        th = math.pi * i / 120
        r = 1 - 0.07 * abs(math.sin(7 * th))
        x = -360 * math.cos(th) * r
        y = -860 - 96 * math.sin(th) * r - 30 * math.sin(th) ** 6
        pts.append((x, y))
    cr.move_to(-360, -860)
    for p in pts:
        cr.line_to(*p)
    cr.close_path()
    cr.set_fill_rule(1)
    cr.set_source_rgb(*GREEN)
    cr.fill_preserve()
    cr.set_source_rgb(*INK)
    cr.set_line_width(7)
    cr.stroke()
    cr.set_fill_rule(0)
    dots_in(cr, lambda: poly(cr, [(-460, -1000), (460, -1000), (460, -870), (-460, -870)]), 26, 4.5, shape="d")
    band(cr, [(-480, -1016), (480, -1016)], 30, RED, spacing=15)
    # dome and finials
    dome = [(-230, -1030), (-236, -1100), (-180, -1190), (-90, -1250), (0, -1290), (90, -1250), (180, -1190),
            (236, -1100), (230, -1030)]
    _shape(cr, dome, GOLD, 7, holes=(14, 17, 3.4))
    for k in range(-3, 4):
        ink(cr, [(k * 60, -1036), (k * 46, -1150), (k * 20, -1270)], 4)
    for (x, y, r) in ((0, -1310, 22), (0, -1350, 15)):
        cr.new_path()
        cr.arc(x, y, r, 0, 2 * math.pi)
        leather(cr, RED, 5)
    poly(cr, [(-6, -1364), (0, -1420), (6, -1364)])
    leather(cr, GOLD, 4)
    for s in (-1, 1):
        x0 = s * 410
        sm = [(x0 - 70, -1030), (x0 - 60, -1100), (x0, -1150), (x0 + 60, -1100), (x0 + 70, -1030)]
        _shape(cr, sm, RED, 6, holes=(10, 14, 3))
        poly(cr, [(x0 - 4, -1150), (x0 - 4, -1240), (x0 + 60, -1220), (x0 + 4, -1200), (x0 + 4, -1150)])
        leather(cr, SAFFRON, 4)


def _tree(cr):
    U = 320                                                     # the canopy sits this much higher than before
    trunk = [(-62, 0), (62, 0), (42, -150), (38, -420), (74, -560 - U * 0.3), (140, -660 - U * 0.6),
             (118, -684 - U * 0.6), (42, -600 - U * 0.4), (12, -700 - U * 0.5), (-12, -700 - U * 0.5),
             (-32, -590 - U * 0.4), (-116, -664 - U * 0.6), (-138, -640 - U * 0.6), (-64, -550 - U * 0.3),
             (-38, -420), (-42, -150)]
    _shape(cr, trunk, BROWN, 7, smooth=False)
    for k in range(4):
        ink(cr, [(-20 + 12 * k, -10), (-14 + 10 * k, -260), (-4 + 6 * k, -520)], 3)
    holes_line(cr, [(0, -40), (6, -300), (0, -560)], 26, 3.4)
    blobs = [(0, -760, 300, 230), (-230, -620, 190, 150), (230, -620, 190, 150), (-150, -860, 170, 130),
             (150, -860, 170, 130), (0, -960, 180, 120), (-300, -720, 120, 100), (300, -720, 120, 100)]
    for i, (x, y, rx, ry) in enumerate(blobs):
        cr.new_path()
        ell(cr, x, y - U, rx, ry)
        leather(cr, GREEN if i % 2 == 0 else DGREEN, 7)
    import random
    rng = random.Random(4)
    for _ in range(80):                                          # leaf-shaped cut-outs
        x, y = rng.uniform(-380, 380), rng.uniform(-1050, -500)
        if ((x / 400) ** 2 + ((y + 760) / 300) ** 2) > 1.0:
            continue
        a = rng.uniform(-1.2, 1.2)
        L = rng.uniform(22, 34)

        def lf(x=x, y=y - U, a=a, L=L):
            cr.save()
            cr.translate(x, y)
            cr.rotate(a)
            cr.move_to(-L, 0)
            cr.curve_to(-L / 2, -L / 3, L / 2, -L / 3, L, 0)
            cr.curve_to(L / 2, L / 3, -L / 2, L / 3, -L, 0)
            cr.restore()
        cut(cr, lf)
    for (x, y) in ((-180, -560), (120, -600), (220, -700), (-60, -640), (-260, -700), (40, -540)):
        ink(cr, [(x, y - 40 - U), (x, y - 14 - U)], 4, col=BROWN)
        cr.new_path()
        ell(cr, x, y + 10 - U, 20, 28, 0.2)
        leather(cr, GOLD, 4)


def _cage(cr):
    fr = [(-46, 0), (46, 0), (46, -86), (36, -110), (0, -130), (-36, -110), (-46, -86)]
    cr.new_path()
    spath(cr, fr)
    path = cr.copy_path()
    cr.set_source_rgb(0.42, 0.24, 0.12)
    cr.fill()
    for i in range(5):                                           # gaps between the bars
        x = -36 + 18 * i
        cut(cr, lambda x=x: poly(cr, [(x, -10), (x + 10, -10), (x + 10, -96), (x + 5, -104), (x, -96)]))
    cr.append_path(path)
    cr.set_source_rgb(*INK)
    cr.set_line_width(4)
    cr.stroke()
    band(cr, [(-48, -4), (48, -4)], 10, OCHRE, spacing=9, hole_r=2)
    poly(cr, [(-4, -128), (0, -148), (4, -128)])
    leather(cr, OCHRE, 3)


def _cage_door(cr):
    """The front bars, hinged at the top-left corner (pivot)."""
    cr.new_path()
    poly(cr, [(0, 0), (90, 0), (90, 100), (0, 100)])
    leather(cr, (0.5, 0.28, 0.12), 3)
    for i in range(4):
        x = 10 + 20 * i
        cut(cr, lambda x=x: poly(cr, [(x, 8), (x + 11, 8), (x + 11, 92), (x, 92)]))
    rivet(cr, 4, 4, 5)


def _small_king(cr, col):
    body = [(-24, 0), (24, 0), (26, -40), (18, -58), (-16, -58), (-26, -40)]
    _shape(cr, body, col, 3)
    cr.new_path()
    cr.arc(0, -72, 15, 0, 2 * math.pi)
    leather(cr, SKIN, 3)
    poly(cr, [(-13, -82), (-10, -104), (0, -96), (10, -104), (13, -82)])
    leather(cr, GOLD, 2.5)
    _shape(cr, [(4, -50), (22, -66), (26, -60), (10, -44)], SKIN, 2.5)
    punch(cr, [(-10, -26), (0, -26), (10, -26)], 2.2)


def _altar(cr):
    k = [(-150, 0), (150, 0), (130, -40), (150, -80), (-150, -80), (-130, -40)]
    _shape(cr, k, (0.62, 0.22, 0.10), 6, smooth=False, holes=(10, 14, 3))
    for y in (-20, -60):
        for x in range(-120, 140, 40):
            cut(cr, lambda x=x, y=y: poly(cr, [(x, y - 6), (x + 8, y), (x, y + 6), (x - 8, y)]))


def _flame(cr, ph):
    import random
    rng = random.Random(ph)
    for layer, (col, sc) in enumerate(((RED, 1.0), (SAFFRON, 0.72), (GOLD, 0.45))):
        pts = [(-130 * sc, 0)]
        n = 7
        for i in range(n):
            x = -130 * sc + 260 * sc * (i + 0.5) / n
            h = (220 + 120 * math.sin(i * 1.7 + ph * 2.1) + rng.uniform(-40, 40)) * sc
            pts += [(x - 10 * sc, -h * 0.55), (x + rng.uniform(-14, 14), -h), (x + 12 * sc, -h * 0.5)]
        pts += [(130 * sc, 0)]
        _shape(cr, pts, col, 4 if layer == 0 else 0)


def _cradle(cr):
    for s in (-1, 1):
        ink(cr, [(s * 20, 0), (s * 150, 330)], 5, smooth=False, col=BROWN)
    bar = [(-200, -14), (200, -14), (200, 14), (-200, 14)]
    _shape(cr, bar, BROWN, 5, smooth=False)
    body = [(-220, 320), (220, 320), (180, 420), (-180, 420)]
    _shape(cr, body, RED, 6, holes=(10, 14, 3))
    dots_in(cr, lambda: poly(cr, [(-170, 340), (170, 340), (150, 400), (-150, 400)]), 22, 4, shape="d")
    band(cr, [(-224, 320), (224, 320)], 18, GOLD, spacing=12)
    rivet(cr, 0, 0, 12)


def _book(cr):
    for i, y in enumerate((-60, -28, 4, 36)):
        _shape(cr, [(-330, y), (330, y - 2), (338, y + 30), (-338, y + 32)], PARCH, 4, smooth=False)
    for y in (-96, 70):
        cv = [(-360, y), (360, y), (368, y + 34), (-368, y + 34)]
        _shape(cr, cv, BROWN, 6, smooth=False, holes=(9, 13, 3))
    for x in (-220, 220):
        punch(cr, [(x, -10)], 12)
        ink(cr, [(x, -10), (x + 20, 130), (x - 10, 190)], 4, col=RED)


def _cloud(cr):
    blobs = [(0, 0, 170, 90), (-140, 30, 110, 70), (140, 30, 120, 74), (-60, -50, 100, 70), (70, -60, 110, 74)]
    for x, y, rx, ry in blobs:
        cr.new_path()
        ell(cr, x, y, rx, ry)
        leather(cr, (0.36, 0.34, 0.44), 6)
    for i in range(12):
        x = -200 + 36 * i
        cut(cr, lambda x=x: poly(cr, [(x, 40), (x + 6, 40), (x - 14, 110), (x - 20, 110)]))
    holes_line(cr, [(-220, 10), (-80, -40), (80, -50), (230, 0)], 18, 4)


def _bolt(cr):
    pts = [(0, 0), (60, 0), (20, 120), (70, 120), (-40, 330), (0, 170), (-50, 170)]
    _shape(cr, pts, GOLD, 5, smooth=False)


def _wall(cr):
    w = [(-600, 0), (600, 0), (600, -420)]
    for i in range(12, -1, -1):
        x = -600 + 100 * i
        w += [(x, -420), (x, -470), (x - 50, -470), (x - 50, -420)] if i > 0 else []
    w += [(-600, -420)]
    _shape(cr, w, (0.70, 0.30, 0.14), 7, smooth=False)
    for row in range(5):
        y = -40 - 80 * row
        holes_line(cr, [(-590, y), (590, y)], 40, 4, smooth=False)
    gate = [(-150, 0), (150, 0), (150, -260), (90, -340), (0, -370), (-90, -340), (-150, -260)]
    _shape(cr, gate, (0.30, 0.18, 0.10), 6)
    ink(cr, [(0, 0), (0, -366)], 4)
    for gx in (-90, -40, 40, 90):
        for gy in (-60, -140, -220):
            cr.new_path()
            cr.arc(gx, gy, 9, 0, 2 * math.pi)
            leather(cr, GOLD, 2.5)


def _ground(cr):
    pts = [(-700, 0), (700, 0), (700, 140), (-700, 140)]
    _shape(cr, pts, (0.45, 0.30, 0.14), 6, smooth=False)
    import random
    rng = random.Random(9)
    tufts = []
    for i in range(24):
        x = -680 + 58 * i + rng.uniform(-10, 10)
        tufts.append(x)
        for k in (-1, 0, 1):
            poly(cr, [(x + 8 * k - 5, 4), (x + 22 * k, -36 - 12 * abs(k - 0.3)), (x + 8 * k + 5, 4)])
            leather(cr, GREEN, 3)
    holes_line(cr, [(-690, 70), (690, 70)], 22, 4, smooth=False)


def _mace(cr):
    ink(cr, [(0, 40), (0, -230)], 16, smooth=False, col=INK)
    ink(cr, [(0, 40), (0, -230)], 9, smooth=False, col=GOLD)
    cr.new_path()
    ell(cr, 0, -300, 70, 84)
    leather(cr, GOLD, 6)
    for k in (-1, 0, 1):
        ink(cr, [(k * 50, -370), (k * 66, -300), (k * 50, -226)], 4)
    band(cr, [(-70, -300), (70, -300)], 14, RED, spacing=11)
    poly(cr, [(-10, -380), (0, -420), (10, -380)])
    leather(cr, GOLD, 4)


def _bow(cr):
    cr.new_path()
    cr.move_to(0, -300)
    cr.curve_to(-120, -150, -120, 150, 0, 300)
    cr.set_line_width(22)
    cr.set_source_rgb(*INK)
    cr.stroke_preserve()
    cr.set_line_width(13)
    cr.set_source_rgb(*OCHRE)
    cr.stroke()
    ink(cr, [(0, -300), (0, 300)], 2.5, smooth=False)
    holes_line(cr, [(-60, -200), (-90, 0), (-60, 200)], 30, 3)


def _plaque(cr):
    """A blank leather name plaque (cartouche) 760 x 230; text is drawn over it per frame."""
    pts = [(-380, -80), (-330, -115), (330, -115), (380, -80), (380, 80), (330, 115), (-330, 115), (-380, 80)]
    _shape(cr, pts, PARCH, 7, smooth=False, holes=(14, 16, 3.4))
    for s in (-1, 1):
        _flower(cr, s * 340, 0, 26, RED, 8)


def _card(cr):
    """The closing YES / NO card: a wide leather board (text drawn over it per frame)."""
    pts = [(-420, -150), (-370, -190), (370, -190), (420, -150), (420, 150), (370, 190), (-370, 190), (-420, 150)]
    _shape(cr, pts, PARCH, 8, smooth=False, holes=(16, 17, 3.6))
    cr.new_path()
    poly(cr, [(-380, -150), (380, -150), (380, 150), (-380, 150)])
    cr.set_source_rgb(*INK)
    cr.set_line_width(3)
    cr.stroke()
    for sx in (-1, 1):
        for y in (-150, 150):
            _flower(cr, sx * 380, y, 24, RED, 8)


def _lamp(cr):
    """A brass oil lamp (deepa) with its flame: the opening card of the show."""
    stand = [(-60, 0), (60, 0), (40, -30), (14, -50), (14, -200), (60, -220), (90, -250), (-90, -250), (-60, -220),
             (-14, -200), (-14, -50), (-40, -30)]
    _shape(cr, stand, GOLD, 6, smooth=False, holes=(8, 12, 2.6))


register("mango", (-70, -130, 100, 90), _mango)
register("mangoL", (-70, -90, 20, 90), lambda cr: _mango_half(cr, -1))
register("mangoR", (-20, -90, 70, 90), lambda cr: _mango_half(cr, 1))
register("moon", (-130, -130, 60, 130), _moon)
register("sun", (-210, -210, 210, 210), _sun)
register("star", (-45, -45, 45, 45), _star)
register("arch", (-500, -1440, 500, 10), _arch)
register("tree", (-420, -1420, 420, 10), _tree)
register("cage", (-52, -152, 52, 8), _cage)
register("cage_door", (-6, -6, 96, 106), _cage_door)
for _i, _c in enumerate((RED, GREEN, OCHRE, BLUE, VIOLET)):
    register(f"kingS{_i}", (-32, -110, 32, 6), (lambda c: lambda cr: _small_king(cr, c))(_c))
register("altar", (-160, -90, 160, 6), _altar)
for _i in range(3):
    register(f"flame{_i}", (-140, -400, 140, 6), (lambda ph: lambda cr: _flame(cr, ph))(_i), tex=0.5)
register("cradle", (-230, -20, 230, 430), _cradle)
register("book", (-375, -100, 375, 200), _book)
register("cloud", (-260, -140, 270, 120), _cloud)
register("bolt", (-60, -10, 80, 340), _bolt)
register("wall", (-610, -480, 610, 10), _wall)
register("ground", (-710, -60, 710, 150), _ground)
register("mace", (-80, -430, 80, 50), _mace)
register("bow", (-120, -310, 20, 310), _bow)
register("plaque", (-390, -125, 390, 125), _plaque)
register("card", (-430, -200, 430, 200), _card)
