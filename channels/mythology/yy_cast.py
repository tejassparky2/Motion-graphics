"""The shared leather cast of long video 2, "Yamlok Yatra" (videos/yamlok_yatra.py), in the Togalu Gombeyaata style
of the reels (puppet_cast, garuda_cast, ...): profile figures with big almond eyes, perforated garments, jointed limbs.
Traditional leather puppets, modelled on no actor and no film. Every sprite name starts with "yy_". Used by all three
scene modules (scenes_yy_a / _b / _c), so names here are never renamed or removed (only added to).

Cast (one look each, kept the same through the video):
  SETH DHANIRAM  the town's richest man and its biggest miser; comic, never hateful: plump with a round belly, a big
                 round Marwari pagdi in red and saffron leheriya stripes with a gold band, a jewelled sarpech and a
                 white plume, a thick curled moustache, round cheeks and a double chin, a gold-and-pearl earring; a
                 bright emerald angarkha (the curved chest panel edged in gold, a printed dot pattern, flared to the
                 knee), a red-and-gold waist sash with a BUNCH OF KEYS hanging at the front, a pearl necklace, gold
                 rings on both hands, cream pyjamas and red-and-gold curled-toe juttis.
                 Rig DHANI (sprites yy_dhani_*), from puppet_cast.man(). Faces (head sprites, swap "yy_dhani_head"):
                 calm | smug | talking | angry | shocked | crying | terrified | sheepish | shut.
                 Front-hand sprites (swap "yy_dhani_armF_lo"): open (default) | point | fist; back hand: open | fist.
                 Seated cross-legged (his shop gaddi): yy_dhani_body_sit + yy_dhani_seat (dhani(..., sit=True)).
  THE SOUL       the same little Dhaniram (same pagdi, moustache, angarkha) drawn small, glowing and a little
                 translucent: soul(cr, t, x, feet, h, ...) at any height h (thumb-sized, hand-sized, or big in a
                 hook). solid=0: the thumb-sized soul of light; solid=1: the hand-sized body from the rice-balls
                 (leather, a faint glow).
  BHOLA          the poor, kind water-seller: thin, sun-browned, a cream head-cloth with a red stripe and its end
                 hanging behind, a small moustache, a gentle face; bare chest, a red check gamchha over the shoulder,
                 a knee-length cream dhoti, bare feet; his clay water pot (matka) on his shoulder.
                 Rig BHOLA (sprites yy_bhola_*). Faces: calm | smile | joy | shy | talking.
Props: Dhaniram's iron safe (tijori: closed body yy_safe + hinged door yy_safe_door, the inside heaped with gold
bars and coins), a bunch of keys on an iron ring (yy_keys), Bhola's water pot (yy_pot), a heap of gold coins
(yy_gold), a gold coin (yy_coin), a water stream helper (water()).

Every sprite is drawn once in design units and cached by puppet_core. A standing figure: feet DH_FEET below the hip
pivot; Dhaniram's turban top DH_TOP above it (so his full height is DH_H design units).
"""
import math

import cairo

import puppet_core as pc
from puppet_cast import HAIR, _flower, _jewel, _shape, man
from puppet_core import (BROWN, DGREEN, DRED, GOLD, INK, PALE, RED, ROSE, SAFFRON, almond_eye, band, dangle, dots_in,
                         ell, holes_line, ink, leather, poly, punch, register, rivet, spath, sway)

# ------------------------------------------------------------------ colours

DH_SKIN = (0.99, 0.76, 0.56)          # Dhaniram: a well-fed, fair-ish wheat
DH_CHEEK = (1.0, 0.62, 0.50)
DH_COAT = (0.16, 0.60, 0.44)          # the angarkha: bright emerald
DH_COAT2 = (0.10, 0.44, 0.32)
DH_PAG1 = (0.92, 0.20, 0.14)          # the pagdi: red and saffron leheriya stripes
DH_PAG2 = (1.0, 0.60, 0.12)
DH_SASH = (0.80, 0.12, 0.16)
DH_PYJAMA = (1.0, 0.95, 0.84)
DH_JUTTI = (0.78, 0.12, 0.10)
IRON = (0.40, 0.42, 0.46)
IRON2 = (0.28, 0.30, 0.34)
SAFE_C = (0.22, 0.40, 0.36)           # the safe: dark green-painted iron
SAFE_C2 = (0.15, 0.28, 0.26)
BH_SKIN = (0.80, 0.52, 0.30)          # Bhola: sun-browned
BH_CLOTH = (0.99, 0.95, 0.84)
BH_STRIPE = (0.80, 0.18, 0.12)
BH_GAMCHHA = (0.88, 0.30, 0.22)
CLAY = (0.80, 0.40, 0.18)
CLAY2 = (0.62, 0.28, 0.12)
TEAR = (0.70, 0.88, 1.0)
WATER = (0.55, 0.80, 1.0)

DH_B = 1.3                            # Dhaniram's bulk (shoulders and arms)
BH_B = 0.84                           # Bhola's bulk
DH_FEET = 434.0                       # hip pivot to the soles (both men)
DH_TOP = 618.0                        # hip pivot to the top of Dhaniram's pagdi
DH_H = DH_FEET + DH_TOP               # Dhaniram's full height (design units)
BH_TOP = 530.0                        # hip pivot to the top of Bhola's head-cloth
SEAT_H = 104.0                        # seated cross-legged: hip above the ground
POT_R = 92.0                          # the water pot: belly radius; pivot at the belly's centre
POT_MOUTH = (0.0, -150.0)             # the pot's mouth (pot units, upright)
SAFE_W, SAFE_H = 300.0, 420.0         # the safe (pivot at the bottom centre): width, height
SAFE_HINGE = (-150.0, -20.0)          # the door's hinge (bottom of the left edge), the door 300 x 380 above it

FLOOR = 900.0                         # default stage floor (feet) for the helpers

FACES = ("calm", "smug", "talking", "angry", "shocked", "crying", "terrified", "sheepish", "shut")
BH_FACES = ("calm", "smile", "joy", "shy", "talking")


def _drop(cr, x, y, r=9, col=TEAR):
    """A tear / sweat drop."""
    cr.new_path()
    cr.move_to(x, y - 1.6 * r)
    cr.curve_to(x + r, y - 0.2 * r, x + r, y + r, x, y + r)
    cr.curve_to(x - r, y + r, x - r, y - 0.2 * r, x, y - 1.6 * r)
    leather(cr, col, 2.4)


def _cover(cr, col, x, y, rx, ry):
    cr.new_path()
    ell(cr, x, y, rx, ry)
    cr.set_source_rgb(*col)
    cr.fill()


# ------------------------------------------------------------------ Dhaniram: the head


def pagdi(cr):
    """The big round Marwari pagdi: red and saffron leheriya (diagonal) stripes, a gold band at the brow, a jewelled
    sarpech with a white plume at the front, the tail (turra) hanging behind."""
    tail = [(-74, -150), (-112, -118), (-126, -50), (-118, 6), (-98, 2), (-96, -60), (-84, -110)]
    _shape(cr, tail, DH_PAG1, 4)
    holes_line(cr, [(-100, -110), (-112, -50), (-108, -6)], 12, 2.2)
    dome = [(-78, -116), (-98, -158), (-100, -214), (-80, -262), (-36, -294), (14, -302), (60, -288), (92, -256),
            (104, -214), (98, -182), (80, -164), (66, -164)]
    cr.new_path()
    spath(cr, dome)
    path = cr.copy_path()
    cr.set_source_rgb(*DH_PAG1)
    cr.fill()
    cr.save()                                                   # leheriya: saffron diagonal stripes
    cr.append_path(path)
    cr.clip()
    cr.set_source_rgb(*DH_PAG2)
    for k in range(-8, 9):
        x0 = 30 * k
        poly(cr, [(x0 - 200, -100), (x0 - 186, -100), (x0 + 14, -320), (x0, -320)])
        cr.fill()
    for k in range(-8, 9):                                      # the wound folds
        ink(cr, [(-104, -110 - 9.6 * k), (0, -150 - 8.4 * k), (104, -130 - 8.4 * k)], 2.4, col=(0.55, 0.10, 0.06))
    cr.restore()
    cr.append_path(path)
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.stroke()
    dots_in(cr, lambda: spath(cr, dome), 26, 2.6)
    band(cr, [(-82, -128), (-10, -156), (76, -168)], 20, GOLD, spacing=12, hole_r=2.4)
    ink(cr, [(-96, -176), (0, -220), (100, -196)], 4)                             # a cross-wound fold
    ink(cr, [(-80, -236), (10, -262), (90, -238)], 3.5)
    _jewel(cr, 62, -200, 15, RED)                                                  # the sarpech
    for i in range(6):
        a = -1.2 + 0.48 * i
        _jewel(cr, 62 + 26 * math.cos(a), -200 + 26 * math.sin(a), 5.5, PALE)
    _shape(cr, [(54, -216), (66, -258), (58, -302), (76, -342), (86, -306), (78, -258), (70, -218)], PALE, 3.5)
    holes_line(cr, [(64, -232), (70, -278), (78, -322)], 11, 2.0)
    _shape(cr, [(58, -212), (70, -212), (66, -228)], GOLD, 2.5, smooth=False)


OPEN = {"talking": 10, "angry": 14, "shocked": 20, "crying": 18, "terrified": 16}     # how far the jaw drops


def dhani_face(cr, mood="calm"):
    """Dhaniram's plump face in profile (pivot at the base of the neck): round cheeks, a double chin, a round nose, a
    thick curled moustache, a gold-and-pearl earring, under the pagdi; the mood sets eye, brow, mouth, tears."""
    sk = DH_SKIN
    d = OPEN.get(mood, 0)
    top = [(-34, 14), (-40, -26), (-60, -70), (-66, -120), (-52, -166), (0, -194), (46, -184), (62, -162), (66, -140),
           (70, -130), (86, -122), (100, -108), (106, -94), (98, -84), (84, -84)]
    if d:
        fc = top + [(80, -80), (60, -74), (74, -62 + d), (68, -52 + d), (76, -40 + d), (64, -24 + d * 0.5), (48, -12),
                    (40, 14)]
    else:
        fc = top + [(80, -78), (72, -72), (76, -64), (68, -54), (76, -42), (64, -24), (48, -12), (40, 14)]
    _shape(cr, fc, sk, 6)
    cr.new_path()                                                                  # the round cheek, a rosy blush
    ell(cr, 24, -66, 24, 17, -0.3)
    cr.set_source_rgb(*DH_CHEEK)
    cr.fill()
    if not d:
        ink(cr, [(54, -44), (72, -44)], 3)                                         # the double chin
    cr.new_path()                                                                  # the ear
    ell(cr, -18, -104, 15, 23)
    leather(cr, sk, 4)
    ink(cr, [(-22, -114), (-14, -100)], 2.4)
    _jewel(cr, -18, -76, 12, GOLD)                                                 # earring: gold with pearls
    for i in range(3):
        cr.new_path()
        cr.arc(-28 + 10 * i, -58, 5, 0, 2 * math.pi)
        leather(cr, PALE, 2)
    # mouth
    if d:
        _shape(cr, [(82, -80), (60, -74), (74, -62 + d)], (0.40, 0.05, 0.06), 3.5, smooth=False)
        if mood in ("talking", "angry"):
            _shape(cr, [(80, -79), (64, -75), (68, -71), (80, -76)], PALE, 2, smooth=False)   # upper teeth
        if mood == "terrified":
            ink(cr, [(64, -70), (68, -64), (64, -58), (70, -52)], 2.4, col=PALE)
    elif mood == "smug":
        ink(cr, [(64, -70), (72, -66), (80, -72)], 3.5)                            # a satisfied smile
    elif mood == "sheepish":
        ink(cr, [(62, -66), (70, -68), (76, -72), (80, -78)], 3.5)                 # a crooked, embarrassed grin
    else:
        ink(cr, [(78, -70), (66, -68)], 3)
    # the big curled moustache (thick under the nose, the tip curling up; drooping when he weeps)
    if mood in ("crying", "terrified"):
        m = [(94, -84), (78, -90), (58, -90), (42, -84), (32, -72), (28, -58), (34, -52), (40, -64), (48, -78),
             (62, -78), (80, -76), (92, -78)]
    else:
        up = 4 if mood == "smug" else 0
        m = [(94, -84), (80, -91), (62, -93), (46, -90), (34, -92 - up), (26, -98 - up), (26, -106 - up),
             (34, -106 - up), (36, -98 - up), (44, -82), (60, -76), (78, -76), (92, -78)]
    _shape(cr, m, HAIR, 3)
    holes_line(cr, [(84, -84), (64, -86), (48, -85)], 11, 2.0)
    pagdi(cr)
    # eyes and brows over the pagdi's lower edge
    if mood == "smug":
        almond_eye(cr, 36, -122, 38, 13, col=PALE)
        _cover(cr, sk, 36, -131, 24, 9)                                            # a heavy, half-shut lid
        ink(cr, [(16, -126), (36, -128), (56, -124)], 5.5)
        ink(cr, [(14, -146), (36, -158), (60, -150)], 5)                           # one brow raised
    elif mood == "talking":
        almond_eye(cr, 36, -122, 38, 13, col=PALE)
        ink(cr, [(16, -142), (36, -150), (58, -142)], 5)
    elif mood == "angry":
        almond_eye(cr, 36, -120, 40, 14, col=PALE)
        ink(cr, [(10, -154), (36, -144), (64, -128)], 9)                           # brow pulled down hard
        ink(cr, [(6, -148), (0, -132)], 3)
    elif mood == "shocked":
        _cover(cr, sk, 36, -122, 28, 18)
        almond_eye(cr, 36, -122, 46, 22, col=PALE)                                 # eye popping wide
        ink(cr, [(12, -156), (36, -168), (62, -160)], 5)
        for k in range(3):                                                         # shock lines
            a = -0.9 + 0.5 * k
            ink(cr, [(110 + 30 * math.cos(a), -150 + 30 * math.sin(a)),
                     (110 + 60 * math.cos(a), -150 + 60 * math.sin(a))], 5, smooth=False)
    elif mood == "crying":
        ink(cr, [(16, -126), (36, -114), (56, -124)], 7)                           # eyes squeezed shut, turned down
        ink(cr, [(12, -136), (36, -146), (60, -160)], 5)                           # brows up at the front, sad
        for k, (x0, y0) in enumerate(((38, -110), (48, -106))):
            ink(cr, [(x0, y0), (x0 + 4, y0 + 30), (x0 + 1, y0 + 56)], 6 - 2 * k, col=TEAR)
        _drop(cr, 40, -36, 8)
        _drop(cr, 54, -16, 6)
    elif mood == "terrified":
        _cover(cr, sk, 36, -122, 28, 18)
        almond_eye(cr, 36, -122, 46, 22, col=PALE, pupil=False)                   # a wide eye, a tiny pupil
        cr.new_path()
        cr.arc(44, -122, 5.5, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        ink(cr, [(10, -148), (30, -164), (56, -170)], 5)                           # brows up and slanted
        _drop(cr, -40, -150, 9, (0.80, 0.92, 1.0))                                 # sweat
        _drop(cr, -52, -112, 7, (0.80, 0.92, 1.0))
    elif mood == "sheepish":
        almond_eye(cr, 34, -120, 36, 12, col=PALE)
        cr.new_path()                                                              # looking down and away
        cr.arc(28, -116, 7, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        _cover(cr, sk, 34, -128, 22, 6)
        ink(cr, [(14, -128), (34, -130), (54, -124)], 4)
        ink(cr, [(12, -142), (30, -154), (56, -146)], 4.5)                         # brow up in the middle
        _drop(cr, -44, -150, 8, (0.80, 0.92, 1.0))
    elif mood == "shut":
        ink(cr, [(16, -118), (36, -110), (56, -118)], 5)                           # eyes closed, peaceful
        for x in (24, 36, 48):
            ink(cr, [(x, -112), (x - 2, -104)], 2.2)
        ink(cr, [(14, -138), (36, -144), (58, -138)], 4.5)
    else:
        almond_eye(cr, 36, -122, 38, 13, col=PALE)
        ink(cr, [(16, -140), (36, -148), (58, -140)], 4.5)
    ink(cr, [(64, -146), (66, -156)], 5, col=RED)                                  # a small red tilak


# ------------------------------------------------------------------ Dhaniram: body, arms, legs


def _keys_on(cr, x, y, s=1.0):
    """A bunch of big old keys on an iron ring hanging from (x, y) (the ring's top)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.new_path()
    cr.arc(0, 26, 24, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(13)
    cr.stroke_preserve()
    cr.set_source_rgb(*IRON)
    cr.set_line_width(6)
    cr.stroke()
    for k, a in enumerate((-0.5, -0.12, 0.26, 0.62)):
        cr.save()
        cr.translate(24 * math.sin(a), 26 + 24 * math.cos(a))
        cr.rotate(-a * 0.8)
        L = 92 - 10 * (k % 2)
        _shape(cr, [(-7, 0), (7, 0), (7, L), (-7, L)], GOLD if k % 2 == 0 else IRON, 3, smooth=False)
        _shape(cr, [(-7, L - 30), (-24, L - 30), (-24, L - 18), (-14, L - 18), (-14, L - 8), (-24, L - 8),
                    (-24, L + 2), (-7, L + 2)], GOLD if k % 2 == 0 else IRON, 3, smooth=False)
        cr.new_path()
        cr.arc(0, -4, 14, 0, 2 * math.pi)
        leather(cr, GOLD if k % 2 == 0 else IRON, 3)
        punch(cr, [(0, -4)], 6)
        cr.restore()
    cr.restore()


def dhani_body(cr, sit=False):
    """The fat torso in the angarkha (hip pivot at 0, 0): a round belly, the curved chest panel edged in gold, a
    printed dot pattern, gold buttons, a pearl necklace, the red-and-gold waist sash with the keys hanging at the front,
    the angarkha flaring to the knee (left off when he sits)."""
    if not sit:
        skirt = [(-82, -40), (112, -40), (136, 60), (164, 200), (170, 236), (-118, 236), (-110, 200), (-96, 60)]
        _shape(cr, skirt, DH_COAT, 6)
        dots_in(cr, lambda: poly(cr, skirt), 24, 3.0, shape="d")
        for x0, x1 in ((-40, -60), (0, -6), (40, 50), (80, 116)):
            ink(cr, [(x0, -30), (x1, 226)], 3, smooth=False, col=DH_COAT2)
        band(cr, [(-114, 222), (24, 228), (168, 222)], 22, GOLD, spacing=12, hole_r=2.4)
        band(cr, [(112, -36), (136, 60), (162, 214)], 14, GOLD, spacing=11, hole_r=2.2)
    torso = [(-62, -10), (-72, -100), (-78, -190), (-68, -250), (-38, -290), (-10, -304), (30, -302), (58, -284),
             (84, -252), (104, -206), (122, -150), (132, -96), (126, -50), (104, -14), (60, 0)]
    _shape(cr, torso, DH_COAT, 6)
    dots_in(cr, lambda: spath(cr, torso), 24, 3.0, shape="d")
    panel = [(-10, -300), (30, -300), (60, -280), (40, -230), (8, -150), (-20, -110), (-40, -150), (-30, -240)]
    _shape(cr, panel, DH_COAT2, 4)                                                 # the overlapping chest panel
    band(cr, [(30, -300), (40, -230), (6, -150), (-24, -108), (-58, -96)], 14, GOLD, spacing=11, hole_r=2.2)
    ink(cr, [(100, -200), (120, -140), (124, -90)], 3.5, col=DH_COAT2)             # the belly's curve
    for x, y in ((112, -190), (124, -140), (126, -92)):                            # gold buttons down the front
        cr.new_path()
        cr.arc(x - 12, y, 7, 0, 2 * math.pi)
        leather(cr, GOLD, 2.5)
    for k in range(2):                                                             # the ties of the angarkha
        ink(cr, [(-24, -112 + 18 * k), (-50, -86 + 18 * k), (-46, -60 + 18 * k)], 3.5, col=GOLD)
    for i in range(14):                                                            # pearl necklace
        u = i / 13
        x, y = -30 + 120 * u, -290 + 120 * u * u + 50 * u
        cr.new_path()
        cr.arc(x, y, 7.5, 0, 2 * math.pi)
        leather(cr, PALE, 2.2)
    band(cr, [(-24, -286), (40, -250), (90, -210)], 10, GOLD, spacing=10, hole_r=2.0)
    _jewel(cr, 92, -200, 13, RED)
    # the waist sash
    sash = [(-70, -56), (20, -66), (130, -60), (134, -24), (20, -26), (-72, -20)]
    _shape(cr, sash, DH_SASH, 5)
    dots_in(cr, lambda: poly(cr, sash), 18, 2.4)
    band(cr, [(-70, -40), (30, -46), (132, -42)], 8, GOLD, holes=False, lw=2.5)
    tails = [(96, -36), (124, -30), (134, 40), (118, 70), (100, 40)]
    _shape(cr, tails, DH_SASH, 4)
    band(cr, [(102, 52), (128, 58)], 12, GOLD, spacing=9, hole_r=2.0)
    _keys_on(cr, 62, -30, 0.95)                                                    # the bunch of keys
    rivet(cr, 20, -6, 7)


def dhani_upper(cr):
    """An angarkha sleeve, upper arm (shoulder pivot at 0, 0; the elbow at 0, 150)."""
    b = DH_B
    pts = [(-30 * b, -8), (-20 * b, -32), (0, -38 * b), (22 * b, -32), (32 * b, -8), (28 * b, 80), (22 * b, 150),
           (0, 166), (-22 * b, 150), (-28 * b, 80)]
    _shape(cr, pts, DH_COAT, 5)
    dots_in(cr, lambda: spath(cr, pts), 22, 2.6, shape="d")
    band(cr, [(-27 * b, 60), (27 * b, 64)], 12, GOLD, spacing=10, hole_r=2.2)
    rivet(cr, 0, 0, 6.5)


def dhani_fore(cr, hand="open"):
    """An angarkha sleeve to the wrist with a gold cuff, and a plump hand with gold rings (elbow pivot at 0, 0).
    hand: open | point (the index finger raised: "PAANI MUFT NAHI!") | fist."""
    b = DH_B
    sk = DH_SKIN
    if hand == "open":
        hp = [(-16, 116), (16, 116), (28, 146), (26, 178), (14, 200), (4, 190), (-4, 164), (-18, 144)]
        _shape(cr, hp, sk, 4)
        _shape(cr, [(16, 132), (36, 144), (34, 158), (18, 154)], sk, 3)
        ink(cr, [(8, 150), (12, 184)], 2.5)
        band(cr, [(2, 170), (24, 172)], 7, GOLD, holes=False, lw=2.2)              # rings
        band(cr, [(4, 158), (26, 160)], 7, GOLD, holes=False, lw=2.2)
    elif hand == "point":
        hp = [(-16, 116), (16, 116), (26, 140), (24, 168), (-6, 172), (-18, 144)]
        _shape(cr, hp, sk, 4)
        _shape(cr, [(4, 166), (16, 166), (20, 230), (14, 240), (6, 232)], sk, 3)   # the raised index finger
        ink(cr, [(-4, 152), (18, 152)], 2.4)
        band(cr, [(4, 186), (20, 186)], 7, GOLD, holes=False, lw=2.2)
        _jewel(cr, 12, 186, 5, RED)
    else:
        cr.new_path()
        ell(cr, 2, 146, 24, 28)
        leather(cr, sk, 4)
        ink(cr, [(-10, 138), (18, 138)], 2.5)
        ink(cr, [(-10, 152), (18, 152)], 2.5)
        band(cr, [(-12, 144), (20, 146)], 7, GOLD, holes=False, lw=2.2)
    pts = [(-21 * b, -6), (0, -24 * b), (21 * b, -6), (18 * b, 90), (16 * b, 122), (-16 * b, 122), (-18 * b, 90)]
    _shape(cr, pts, DH_COAT, 5)
    dots_in(cr, lambda: spath(cr, pts), 22, 2.6, shape="d")
    band(cr, [(-17 * b, 112), (17 * b, 114)], 14, GOLD, spacing=9, hole_r=2.0)
    rivet(cr, 0, 0, 6)


def dhani_leg(cr):
    """A leg in cream pyjamas with a red-and-gold curled-toe jutti (hip pivot at 0, 0; the sole at +426)."""
    lg = [(-50, -10), (0, -32), (54, -10), (58, 90), (44, 200), (30, 300), (26, 376), (-14, 380), (-22, 300),
          (-40, 200), (-54, 90)]
    _shape(cr, lg, DH_PYJAMA, 5)
    dots_in(cr, lambda: spath(cr, lg), 20, 2.4)
    for k in range(4):                                                             # churidar folds at the ankle
        ink(cr, [(-18, 330 + 12 * k), (24, 326 + 12 * k)], 2.4, col=(0.75, 0.66, 0.52))
    ink(cr, [(-6, 20), (2, 140), (6, 280)], 3)
    jut = [(-24, 372), (28, 370), (60, 390), (96, 396), (118, 376), (126, 386), (112, 408), (80, 422), (-26, 426)]
    _shape(cr, jut, DH_JUTTI, 4)
    band(cr, [(-22, 384), (40, 384), (90, 404)], 9, GOLD, spacing=9, hole_r=1.8)
    cr.new_path()
    cr.arc(120, 376, 6, 0, 2 * math.pi)
    leather(cr, GOLD, 2)
    rivet(cr, 0, 0, 9)


def dhani_seat(cr):
    """Cross-legged on his gaddi (hip at 0, 0; the ground at +SEAT_H): the angarkha over a broad lap, the pyjama
    knees, one jutti tucked in front."""
    lap = [(-110, -40), (40, -54), (170, -40), (262, -14), (280, 40), (262, 90), (120, 104), (-60, 104), (-112, 80),
           (-120, 20)]
    _shape(cr, lap, DH_PYJAMA, 5)
    dots_in(cr, lambda: spath(cr, lap), 20, 2.4)
    ink(cr, [(150, 0), (230, 20), (262, 60)], 3, col=(0.75, 0.66, 0.52))
    jut = [(110, 40), (160, 30), (214, 36), (240, 20), (244, 34), (226, 58), (120, 64)]
    _shape(cr, jut, DH_JUTTI, 4)
    band(cr, [(120, 46), (210, 44)], 8, GOLD, spacing=9, hole_r=1.8)
    flap = [(-100, -50), (130, -50), (150, 30), (100, 70), (-110, 60)]
    _shape(cr, flap, DH_COAT, 5)
    dots_in(cr, lambda: poly(cr, flap), 24, 3.0, shape="d")
    band(cr, [(-104, 52), (100, 64), (148, 30)], 18, GOLD, spacing=12, hole_r=2.2)
    rivet(cr, 0, 0, 9)


_DH = dict(skin=DH_SKIN, bulk=DH_B, dhoti=DH_PYJAMA, border=GOLD, pleat=DH_COAT, sash=DH_SASH, neck=GOLD)
DHANI = man("yy_dhani", crown="tiara", halo=False, hair=False, earring=False, tilak=False, moustache=True,
            hands=("open", "open"), **_DH)
register("yy_dhani_body", (-140, -330, 190, 250), lambda cr: dhani_body(cr))
register("yy_dhani_body_sit", (-140, -330, 190, 90), lambda cr: dhani_body(cr, sit=True))
register("yy_dhani_seat", (-140, -70, 300, 120), dhani_seat)
register("yy_dhani_head", (-140, -350, 140, 30), lambda cr: dhani_face(cr, "calm"))
for _m in FACES[1:]:
    register("yy_dhani_head_" + _m, (-140, -350, 150, 40), (lambda m: lambda cr: dhani_face(cr, m))(_m))
for _side in ("F", "B"):
    register(f"yy_dhani_arm{_side}_up", (-50, -55, 50, 180), dhani_upper)
    register(f"yy_dhani_arm{_side}_lo", (-45, -40, 50, 215), lambda cr: dhani_fore(cr, "open"))
    register(f"yy_dhani_arm{_side}_lo_fist", (-45, -40, 50, 215), lambda cr: dhani_fore(cr, "fist"))
    register(f"yy_dhani_leg{_side}", (-70, -45, 140, 440), dhani_leg)
register("yy_dhani_armF_lo_point", (-45, -40, 50, 250), lambda cr: dhani_fore(cr, "point"))
DHANI.points["keys"] = ("yy_dhani_body", (62, 20))         # the bunch of keys at his waist
DHANI.points["belly"] = ("yy_dhani_body", (110, -110))
DHANI.points["pocket"] = ("yy_dhani_body", (96, -40))      # where a pocket would be (the bribe joke)


# ------------------------------------------------------------------ Bhola


def bhola_face(cr, mood="calm"):
    """Bhola: a thin, gentle face, a small moustache, a cream head-cloth with a red stripe and its end hanging
    behind. mood: calm | smile | joy (laughing, eyes squeezed) | shy (eyes down, a small smile) | talking."""
    sk = BH_SKIN
    tail = [(-48, -150), (-86, -126), (-100, -60), (-84, -52), (-70, -108), (-40, -132)]
    _shape(cr, tail, BH_CLOTH, 4)
    band(cr, [(-84, -100), (-92, -64)], 8, BH_STRIPE, holes=False, lw=2)
    fc = [(-22, 8), (-28, -36), (-48, -80), (-54, -126), (-40, -170), (0, -192), (38, -182), (54, -152), (58, -128),
          (64, -116), (88, -94), (66, -84), (68, -74), (60, -66), (64, -58), (54, -46), (48, -30), (30, -22), (22, 8)]
    if mood in ("joy", "talking"):
        d = 16 if mood == "joy" else 8
        fc = [(-22, 8), (-28, -36), (-48, -80), (-54, -126), (-40, -170), (0, -192), (38, -182), (54, -152),
              (58, -128), (64, -116), (88, -94), (68, -84), (48, -76), (64, -60 + d), (58, -46 + d), (48, -32 + d * 0.6),
              (30, -22), (22, 8)]
    _shape(cr, fc, sk, 6)
    ink(cr, [(40, -100), (46, -82)], 2.4)                                         # a thin cheek line
    cr.new_path()
    ell(cr, -14, -106, 12, 20)
    leather(cr, sk, 4)
    if mood in ("joy", "talking"):
        d = 16 if mood == "joy" else 8
        _shape(cr, [(68, -84), (48, -76), (64, -60 + d)], (0.40, 0.05, 0.06), 3, smooth=False)
        _shape(cr, [(66, -83), (52, -77), (56, -72), (66, -79)], PALE, 2, smooth=False)
    elif mood in ("smile", "shy"):
        ink(cr, [(50, -70), (58, -64), (66, -68)], 3.5)
    else:
        ink(cr, [(64, -70), (56, -68)], 3)
    if mood == "joy":
        ink(cr, [(14, -112), (30, -126), (48, -114)], 6.5)
        ink(cr, [(18, -104), (30, -98), (44, -104)], 2.5)
        ink(cr, [(10, -146), (30, -156), (52, -146)], 4.5)
    elif mood == "smile":
        ink(cr, [(14, -112), (30, -124), (48, -112)], 5.5)                         # a happy, curved eye
        ink(cr, [(10, -140), (30, -150), (52, -142)], 4.5)
    elif mood == "shy":
        ink(cr, [(14, -114), (30, -106), (48, -114)], 5)                           # eyes down
        for x in (20, 30, 40):
            ink(cr, [(x, -108), (x - 1, -101)], 2.2)
        ink(cr, [(10, -132), (30, -140), (52, -134)], 4)
        cr.new_path()
        ell(cr, 34, -82, 14, 9)
        cr.set_source_rgb(*(0.90, 0.48, 0.34))
        cr.fill()
    else:
        almond_eye(cr, 30, -116, 36, 12, col=PALE)
        ink(cr, [(12, -134), (30, -142), (50, -134)], 4)
    m = [(60, -76), (42, -82), (26, -82), (16, -92), (26, -88), (42, -80), (60, -72)]
    _shape(cr, m, HAIR, 2.5)
    wrap = [(-54, -118), (-58, -166), (-40, -204), (0, -222), (40, -212), (58, -180), (56, -152), (20, -158),
            (-20, -150), (-42, -114)]
    _shape(cr, wrap, BH_CLOTH, 5)
    for k in range(3):
        ink(cr, [(-50, -138 - 20 * k), (0, -168 - 14 * k), (52, -164 - 12 * k)], 2.6, col=(0.72, 0.66, 0.56))
    band(cr, [(-50, -150), (0, -178), (54, -170)], 9, BH_STRIPE, holes=False, lw=2.2)
    holes_line(cr, [(-44, -128), (0, -150), (50, -150)], 14, 2.2)
    _shape(cr, [(-30, -206), (-6, -224), (8, -214), (-10, -196)], BH_CLOTH, 3)      # the knot on top


def bhola_body(cr):
    """Thin, bare-chested (hip at 0, 0): a red check gamchha over the shoulder, a cream dhoti wrap with a red stripe."""
    b = BH_B
    gam = [(-30, -294), (0, -298), (-40, -220), (-70, -150), (-96, -150), (-74, -230)]
    _shape(cr, gam, BH_GAMCHHA, 4)                                                 # the gamchha down his back
    for k in range(3):
        ink(cr, [(-26 - 14 * k, -286 + 6 * k), (-62 - 12 * k, -160 + 4 * k)], 2.4, col=PALE)
    ink(cr, [(-60, -200), (-30, -250)], 2.4, col=PALE)
    torso = [(-46 * b, -6), (-54 * b, -100), (-60 * b, -190), (-54 * b, -246), (-30, -284), (-10, -298), (24, -298),
             (36 * b + 4, -282), (66 * b, -252), (80 * b, -208), (74 * b, -160), (58 * b, -110), (52 * b, -50),
             (48 * b, -6)]
    _shape(cr, torso, BH_SKIN, 6)
    for k in range(3):                                                             # thin ribs
        ink(cr, [(10, -200 + 22 * k), (40 * b, -190 + 22 * k), (60 * b, -170 + 22 * k)], 2.4)
    ink(cr, [(36 * b, -230), (60 * b, -206), (76 * b, -192)], 3.5)
    punch(cr, [(42 * b, -70)], 4)
    band(cr, [(-26, -290), (0, -270), (40 * b, -244)], 8, BROWN, holes=False, lw=2)  # a plain thread
    gf = [(-8, -298), (26, -298), (34, -250), (8, -214), (-14, -222)]
    _shape(cr, gf, BH_GAMCHHA, 4)                                                  # its end over the shoulder
    ink(cr, [(4, -292), (10, -226)], 2.4, col=PALE)
    ink(cr, [(18, -294), (24, -240)], 2.4, col=PALE)
    wrap = [(-58 * b, -40), (0, -50), (60 * b, -42), (68 * b, 10), (64 * b, 46), (0, 54), (-64 * b, 46),
            (-68 * b, 10)]
    _shape(cr, wrap, BH_CLOTH, 6)
    dots_in(cr, lambda: spath(cr, wrap), 22, 2.6)
    band(cr, [(-60 * b, -32), (0, -42), (62 * b, -34)], 10, BH_STRIPE, holes=False, lw=2.5)
    pf = [(24 * b, 30), (56 * b, 26), (84 * b, 186), (70 * b, 200), (40 * b, 190), (18 * b, 196)]
    _shape(cr, pf, BH_CLOTH, 4, smooth=False)
    ink(cr, [(36 * b, 34), (44 * b, 190)], 2.6, smooth=False, col=(0.72, 0.66, 0.56))
    rivet(cr, 16 * b, 6, 7)


def bhola_upper(cr):
    b = BH_B
    pts = [(-28 * b, -8), (-18 * b, -30), (0, -36 * b), (20 * b, -30), (30 * b, -8), (25 * b, 80), (18 * b, 150),
           (0, 164), (-18 * b, 150), (-25 * b, 80)]
    _shape(cr, pts, BH_SKIN, 5)
    ink(cr, [(-10, 60), (8, 64)], 2.2, col=INK)                                   # a black thread
    rivet(cr, 0, 0, 6.5)


def bhola_fore(cr, hand="open"):
    b = BH_B
    sk = BH_SKIN
    if hand == "open":
        hp = [(-13, 122), (14, 122), (24, 148), (22, 176), (12, 196), (4, 186), (-2, 162), (-14, 146)]
        _shape(cr, hp, sk, 4)
        _shape(cr, [(14, 136), (32, 146), (30, 158), (16, 154)], sk, 3)
        ink(cr, [(8, 150), (12, 182)], 2.5)
    else:                                                                          # cupped, holding (a pot, a roti)
        hp = [(-14, 122), (16, 122), (30, 146), (34, 170), (20, 186), (-4, 182), (-16, 150)]
        _shape(cr, hp, sk, 4)
        ink(cr, [(4, 150), (28, 156)], 2.4)
    pts = [(-17 * b, -6), (0, -22 * b), (17 * b, -6), (15 * b, 90), (12 * b, 128), (-12 * b, 128), (-15 * b, 90)]
    _shape(cr, pts, sk, 5)
    ink(cr, [(-12, 112), (12, 114)], 3, col=INK)                                  # a black thread at the wrist
    rivet(cr, 0, 0, 6)


def bhola_leg(cr):
    b = BH_B
    shin = [(-22 * b, 186), (16 * b, 186), (14 * b, 300), (10 * b, 388), (-10 * b, 392), (-22 * b, 300)]
    _shape(cr, shin, BH_SKIN, 5)
    foot = [(-14, 382), (12, 380), (30, 396), (66, 410), (68, 424), (-16, 426)]
    _shape(cr, foot, BH_SKIN, 4)
    dl = [(-40 * b, -10), (0, -26), (44 * b, -10), (50 * b, 80), (42 * b, 160), (30 * b, 204), (-26 * b, 204),
          (-36 * b, 160), (-46 * b, 80)]
    _shape(cr, dl, BH_CLOTH, 5)
    dots_in(cr, lambda: spath(cr, dl), 20, 2.4)
    band(cr, [(-28 * b, 196), (32 * b, 196)], 8, BH_STRIPE, holes=False, lw=2)
    ink(cr, [(-10, 20), (-4, 120), (6, 190)], 3)
    rivet(cr, 0, 0, 9)


_BH = dict(skin=BH_SKIN, bulk=BH_B, dhoti=BH_CLOTH, border=BH_STRIPE, pleat=BH_CLOTH, sash=BH_GAMCHHA, neck=BROWN)
BHOLA = man("yy_bhola", crown="tiara", halo=False, hair=False, earring=False, tilak=False, moustache=True,
            hands=("open", "open"), **_BH)
register("yy_bhola_body", (-160, -320, 120, 230), bhola_body)
register("yy_bhola_head", (-120, -250, 110, 30), lambda cr: bhola_face(cr, "calm"))
for _m in BH_FACES[1:]:
    register("yy_bhola_head_" + _m, (-120, -250, 110, 40), (lambda m: lambda cr: bhola_face(cr, m))(_m))
for _side in ("F", "B"):
    register(f"yy_bhola_arm{_side}_up", (-45, -50, 45, 175), bhola_upper)
    register(f"yy_bhola_arm{_side}_lo", (-45, -30, 50, 210), lambda cr: bhola_fore(cr, "open"))
    register(f"yy_bhola_arm{_side}_lo_hold", (-45, -30, 50, 210), lambda cr: bhola_fore(cr, "hold"))
    register(f"yy_bhola_leg{_side}", (-70, -40, 90, 440), bhola_leg)


# ------------------------------------------------------------------ props


def _pot(cr):
    """Bhola's clay water pot (matka), pivot at the centre of its belly: a round terracotta belly, painted cream
    bands and dots, a short neck, a rolled rim (the mouth at POT_MOUTH)."""
    r = POT_R
    cr.new_path()
    cr.arc(0, 0, r, 0, 2 * math.pi)
    leather(cr, CLAY, 6)
    cr.save()
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.clip()
    cr.new_path()
    ell(cr, 26, 30, 80, 70)
    cr.set_source_rgb(*CLAY2)
    cr.fill()
    cr.restore()
    cr.new_path()
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(6)
    cr.stroke()
    band(cr, [(-86, -30), (0, -40), (86, -30)], 12, (0.98, 0.88, 0.66), holes=False, lw=2.5)
    band(cr, [(-80, 34), (0, 44), (80, 34)], 8, (0.98, 0.88, 0.66), holes=False, lw=2.5)
    for i in range(7):
        x = -60 + 20 * i
        _shape(cr, [(x, -8), (x + 6, 2), (x, 12), (x - 6, 2)], (0.98, 0.88, 0.66), 1.8, smooth=False)
    _shape(cr, [(-36, -80), (36, -80), (30, -124), (-30, -124)], CLAY, 5)          # the neck
    _shape(cr, [(-50, -124), (50, -124), (54, -142), (40, -154), (-40, -154), (-54, -142)], CLAY2, 5)   # the rim
    ink(cr, [(-40, -148), (40, -148)], 3, col=(0.30, 0.14, 0.06))
    punch(cr, [(-40, 66), (-10, 74), (20, 70)], 3)
    cr.new_path()
    ell(cr, -38, -40, 16, 26, 0.4)                                                 # a cool damp gleam
    cr.set_source_rgb(0.92, 0.62, 0.40)
    cr.fill()


register("yy_pot", (-110, -170, 110, 110), _pot)


def _safe_body(cr, inside=False):
    """The iron tijori (pivot at the bottom centre), SAFE_W x SAFE_H: riveted dark-green iron, brass corners, four
    stubby feet, a top rail; inside=True paints the open inside heaped with gold bars and coin stacks."""
    w, h = SAFE_W / 2, SAFE_H
    for x in (-w + 30, w - 30):
        _shape(cr, [(x - 24, 0), (x + 24, 0), (x + 18, -26), (x - 18, -26)], IRON2, 4, smooth=False)
    box = [(-w, -20), (w, -20), (w, -h), (-w, -h)]
    _shape(cr, box, SAFE_C, 6, smooth=False, holes=(14, 20, 2.6))
    band(cr, [(-w - 10, -h - 6), (w + 10, -h - 6)], 22, IRON, spacing=14, hole_r=2.4)
    for cx, cy in ((-w, -20), (w, -20), (-w, -h), (w, -h)):                        # brass corners
        _shape(cr, [(cx - 22, cy - 22), (cx + 22, cy - 22), (cx + 22, cy + 22), (cx - 22, cy + 22)], GOLD, 3,
               smooth=False)
        punch(cr, [(cx, cy)], 4)
    if inside:
        cav = [(-w + 28, -48), (w - 28, -48), (w - 28, -h + 28), (-w + 28, -h + 28)]
        _shape(cr, cav, (0.18, 0.12, 0.08), 4, smooth=False)
        band(cr, [(-w + 30, -h / 2 - 10), (w - 30, -h / 2 - 10)], 12, IRON2, holes=False, lw=3)    # a shelf
        for row, y0 in enumerate((-h / 2 - 22, -56)):                              # gold bars and coin stacks
            for k in range(3 if row == 0 else 2):
                x0 = -w + 50 + k * 70
                _shape(cr, [(x0, y0), (x0 + 60, y0), (x0 + 52, y0 - 34), (x0 + 8, y0 - 34)], GOLD, 3.5, smooth=False)
                ink(cr, [(x0 + 12, y0 - 26), (x0 + 48, y0 - 26)], 2, col=(0.7, 0.5, 0.1))
            for k in range(2 if row == 0 else 3):
                x0 = w - 70 - k * 46 if row == 0 else -w + 200 + k * 0
                if row == 1 and k > 0:
                    x0 = -w + 200 + 46 * k
                for j in range(5 + k):
                    cr.new_path()
                    ell(cr, x0 + 20, y0 - 6 - 10 * j, 22, 7)
                    leather(cr, GOLD, 2.4)
        for i in range(7):
            cr.new_path()
            cr.arc(-w + 60 + 30 * i, -h + 70 + 8 * math.sin(i), 9, 0, 2 * math.pi)
            leather(cr, GOLD if i % 3 else RED, 2)
    else:
        _shape(cr, [(-w + 24, -44), (w - 24, -44), (w - 24, -h + 24), (-w + 24, -h + 24)], SAFE_C2, 4, smooth=False)


def _safe_door(cr):
    """The safe's door (hinge at its bottom-left, 0, 0): riveted iron, a brass lock plate with a big keyhole, a
    handle, a painted gold medallion (a stylised swastika-free lotus)."""
    w, h = 252.0, 352.0
    door = [(0, 0), (w, 0), (w, -h), (0, -h)]
    _shape(cr, door, SAFE_C, 6, smooth=False, holes=(12, 18, 2.4))
    for y in (-30, -h + 30):
        for x in (20, w - 20):
            rivet(cr, x, y, 7)
    plate = [(w / 2 - 44, -h / 2 + 70), (w / 2 + 44, -h / 2 + 70), (w / 2 + 44, -h / 2 - 30),
             (w / 2, -h / 2 - 60), (w / 2 - 44, -h / 2 - 30)]
    _shape(cr, plate, GOLD, 4, smooth=False)
    cr.new_path()                                                                  # the keyhole
    cr.arc(w / 2, -h / 2 - 8, 13, 0, 2 * math.pi)
    poly(cr, [(w / 2 - 8, -h / 2), (w / 2 + 8, -h / 2), (w / 2 + 12, -h / 2 + 40), (w / 2 - 12, -h / 2 + 40)])
    cr.set_source_rgb(*INK)
    cr.fill()
    band(cr, [(w - 40, -h / 2 - 50), (w - 26, -h / 2), (w - 40, -h / 2 + 50)], 14, IRON, holes=False)  # handle
    _flower(cr, w / 2, -h + 74, 34, GOLD, 8)
    _jewel(cr, w / 2, -h + 74, 12, RED)
    band(cr, [(10, -h + 130), (w - 10, -h + 130)], 8, GOLD, holes=False, lw=2)


register("yy_safe", (-180, -460, 180, 10), lambda cr: _safe_body(cr, False))
register("yy_safe_open", (-180, -460, 180, 10), lambda cr: _safe_body(cr, True))
register("yy_safe_door", (-10, -362, 262, 10), _safe_door)


def _keys(cr):
    """The bunch of keys as a separate prop (pivot at the top of the ring)."""
    _keys_on(cr, 0, 0, 1.0)


register("yy_keys", (-90, -30, 90, 150), _keys)


def _coin(cr):
    cr.new_path()
    cr.arc(0, 0, 30, 0, 2 * math.pi)
    leather(cr, GOLD, 4)
    cr.new_path()
    cr.arc(0, 0, 20, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(2.5)
    cr.stroke()
    ink(cr, [(-6, -10), (8, -10)], 3)
    ink(cr, [(-6, -2), (8, -2)], 3)
    ink(cr, [(-4, -10), (6, 12)], 3)
    punch(cr, [(-14, -14)], 3)


register("yy_coin", (-36, -36, 36, 36), _coin)


def _gold(cr):
    """A heap of gold coins (pivot at the bottom centre)."""
    import random
    rng = random.Random(13)
    heap = [(-200, 0), (200, 0), (150, -60), (60, -120), (-40, -130), (-140, -70)]
    _shape(cr, heap, GOLD, 5)
    for _ in range(46):
        x, y = rng.uniform(-170, 170), rng.uniform(-120, -6)
        if abs(x) / 200 + (-y) / 130 > 1.0:
            continue
        cr.new_path()
        ell(cr, x, y, 22, 9, rng.uniform(-0.3, 0.3))
        leather(cr, GOLD if rng.random() > 0.2 else (1.0, 0.70, 0.20), 2.4)
    for x, y in ((-60, -100), (40, -110), (100, -50)):
        _jewel(cr, x, y, 9, RED)


register("yy_gold", (-210, -150, 210, 10), _gold)


# ------------------------------------------------------------------ helpers (draw the cast in a scene)


def angles(key, t, front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0), hits=(), ph=0.0):
    """Joint angles for a man() rig (as scenes_jarasandha.man_angles): front / backa are the arms' (upper, fore)
    angles (0 hangs down, -pi/2 points forward, -pi points up); hits = [(time, strength)] swing the arms."""
    d = dangle(t, hits, 0.22, 1.4, 2.4)
    return {key + "_armF_up": front[0] + 0.32 + d + sway(t, 0.03, 0.5, ph),
            key + "_armF_lo": front[1] + 0.55 + d * 0.6,
            key + "_armB_up": backa[0] - 0.30 - d * 0.5 + sway(t, 0.025, 0.45, ph + 1),
            key + "_armB_lo": backa[1] + 0.25,
            key + "_head": head + sway(t, 0.015, 0.4, ph + 2),
            key + "_legF": legs[0], key + "_legB": legs[1]}


def _face(name, mood, faces):
    if mood in (None, "calm") or mood not in faces:
        return name
    return name + "_" + mood


def dhani(cr, t, x, s, mood="calm", feet=FLOOR, front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0),
          hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.0, y=None, hand="open", bhand="open",
          sit=False, extra=None, swap=None, bob=True, hide=()):
    """Seth Dhaniram standing with his feet on `feet` (hip at feet - DH_FEET * s), or sitting cross-legged (sit=True:
    the hip at feet - SEAT_H * s). mood: one of FACES; hand: the front hand open | point | fist; bhand: open | fist.
    Returns the puppet's points (device xy): handF, handB, chest, head, top, hip, keys, belly, pocket."""
    ang = angles("yy_dhani", t, front, backa, head, legs, hits, ph)
    sw = {"yy_dhani_head": _face("yy_dhani_head", mood, FACES)}
    if hand in ("point", "fist"):
        sw["yy_dhani_armF_lo"] = "yy_dhani_armF_lo_" + hand
    if bhand == "fist":
        sw["yy_dhani_armB_lo"] = "yy_dhani_armB_lo_fist"
    sw.update(swap or {})
    r = rot + (sway(t, 0.012, 0.55, ph) if bob else 0.0)
    hide = tuple(hide)
    if sit:
        hy = feet - SEAT_H * s if y is None else y
        pc.prop(cr, "yy_dhani_seat", x, hy, s, r, alpha, blur, flip)
        sw["yy_dhani_body"] = "yy_dhani_body_sit"
        hide += ("yy_dhani_legF", "yy_dhani_legB")
    else:
        hy = feet - DH_FEET * s if y is None else y
    return pc.puppet(cr, DHANI, x, hy, s, r, flip, ang, alpha, blur, hide=hide, swap=sw, rods=rods, extra=extra)


POT_HOLD = dict(backa=(1.43, 1.84))         # Bhola's back arm: the elbow out behind, the hand up on the pot
POT_ON = (-100.0, -350.0, -0.15, 0.8)      # the pot on his shoulder: centre (body units), tilt, scale


def bhola(cr, t, x, s, mood="calm", feet=FLOOR, front=(-0.32, -0.55), backa=None, head=0.0, legs=(0.0, 0.0),
          hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.7, y=None, pot=True, hand="open",
          bhand=None, extra=None, swap=None, bob=True, hide=()):
    """Bhola standing (hip at feet - DH_FEET * s). pot=True: the water pot on his shoulder (drawn behind him), his
    back arm up holding it; pot=False: no pot (the scene can put yy_pot in his hands). hand / bhand: open | hold.
    Returns the puppet's points plus "pot" (device xy of the pot's centre when on the shoulder)."""
    if backa is None:
        backa = POT_HOLD["backa"] if pot else (0.3, -0.25)
    if bhand is None:
        bhand = "hold" if pot else "open"
    ang = angles("yy_bhola", t, front, backa, head, legs, hits, ph)
    sw = {"yy_bhola_head": _face("yy_bhola_head", mood, BH_FACES)}
    if hand == "hold":
        sw["yy_bhola_armF_lo"] = "yy_bhola_armF_lo_hold"
    if bhand == "hold":
        sw["yy_bhola_armB_lo"] = "yy_bhola_armB_lo_hold"
    sw.update(swap or {})
    r = rot + (sway(t, 0.012, 0.55, ph) if bob else 0.0)
    hy = feet - DH_FEET * s if y is None else y
    pot_xy = None
    if pot:
        cr.save()                                                                  # the pot rides on the body
        cr.translate(x, hy)
        cr.rotate(r)
        cr.scale(-s if flip else s, s)
        cr.translate(POT_ON[0], POT_ON[1])
        cr.rotate(POT_ON[2])
        cr.scale(POT_ON[3], POT_ON[3])
        pc.paint_part(cr, "yy_pot", alpha, blur)
        pot_xy = cr.user_to_device(0, 0)
        cr.restore()
    pts = pc.puppet(cr, BHOLA, x, hy, s, r, flip, ang, alpha, blur, hide=tuple(hide), swap=sw, rods=rods,
                    extra=extra)
    if pot_xy is not None:
        pts["pot"] = pot_xy
    return pts


def pot(cr, x, y, s=1.0, rot=0.0, alpha=1.0, blur=0.0):
    """The water pot alone (pivot at the belly's centre); returns its mouth (scene xy)."""
    pc.prop(cr, "yy_pot", x, y, s, rot, alpha, blur)
    mx, my = POT_MOUTH
    c, si = math.cos(rot), math.sin(rot)
    return x + (mx * c - my * si) * s, y + (mx * si + my * c) * s


def water(cr, t, p0, p1, a=1.0, w=14.0, lift=60.0):
    """A stream of water from p0 (a pot's mouth) falling to p1 (a cup, cupped hands): a pale blue arc with drops."""
    if a <= 0.01:
        return
    mx, my = (p0[0] + p1[0]) / 2, min(p0[1], p1[1]) - lift
    pts = []
    for i in range(13):
        u = i / 12
        pts.append(((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * mx + u * u * p1[0],
                    (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * my + u * u * p1[1]))
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, col, al in ((w + 8, (0.12, 0.30, 0.52), 0.5), (w, WATER, 0.9), (w * 0.35, (0.92, 0.98, 1.0), 0.9)):
        cr.new_path()
        spath(cr, pts, closed=False)
        cr.set_source_rgba(*col, al * a)
        cr.set_line_width(lw)
        cr.stroke()
    for k in range(5):                                                             # splashing drops
        u = (t * 2.3 + k * 0.2) % 1.0
        ang = -math.pi / 2 + (k - 2) * 0.5
        dx, dy = math.cos(ang) * 50 * u, math.sin(ang) * 40 * u + 60 * u * u
        cr.new_path()
        cr.arc(p1[0] + dx, p1[1] + dy - 4, 5 * (1 - u) + 1.5, 0, 2 * math.pi)
        cr.set_source_rgba(*WATER, 0.85 * (1 - u) * a)
        cr.fill()
    cr.restore()


def safe(cr, x, ground, s=1.0, open_=0.0, alpha=1.0, blur=0.0, rot=0.0):
    """The tijori on the floor (pivot at the bottom centre); open_ 0..1 swings its door open on the left hinge and
    shows the gold inside."""
    pc.prop(cr, "yy_safe_open" if open_ > 0.02 else "yy_safe", x, ground, s, rot, alpha, blur)
    k = math.cos(math.pi * 0.62 * min(1.0, max(0.0, open_)))           # the door's apparent width
    if abs(k) < 0.03:
        return
    cr.save()
    cr.translate(x, ground)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.translate(SAFE_HINGE[0] + 24, SAFE_HINGE[1] - 4)
    cr.scale(k, 1.0)
    pc.paint_part(cr, "yy_safe_door", alpha, blur)
    cr.restore()


SOUL_W = (1.0, 0.96, 0.82)            # the soul's light
SOUL_GOLD = (1.0, 0.78, 0.30)


def _glow(cr, x, y, r, a):
    if a <= 0.01 or r <= 1:
        return
    hs, n = pc._hotspot()
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.translate(x, y)
    cr.scale(r / n, r / n)
    cr.set_source_surface(hs, -n, -n)
    cr.paint_with_alpha(min(1.0, a))
    cr.restore()


def soul(cr, t, x, feet, h, mood="terrified", front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0),
         hits=(), flip=False, alpha=1.0, rot=0.0, glow=1.0, solid=0.0, hand="open", bhand="open", shiver=0.0,
         ph=1.3, extra=None):
    """Dhaniram's soul: the same little Dhaniram (pagdi, moustache, angarkha), h px tall from his soles at (x, feet)
    to the top of his pagdi, glowing and a little translucent. solid 0 = the thumb-sized soul of light; solid 1 = the
    hand-sized body from the rice-balls (plain leather, a faint warm rim). glow scales the halo. shiver shakes him.
    Returns the puppet's points (device xy) or {} when too small to draw."""
    if alpha <= 0.01 or h < 6:
        return {}
    s = h / DH_H
    x += shiver * 0.02 * h * math.sin(t * 43)
    pul = 0.92 + 0.08 * math.sin(t * 3.3 + x * 0.013)
    sol = min(1.0, max(0.0, solid))
    cy = feet - 0.5 * h
    if glow > 0:
        _glow(cr, x, cy, 1.25 * h + 40, (0.75 - 0.4 * sol) * alpha * glow * pul)
    pad = 0.75 * h + 30
    cr.save()
    cr.rectangle(x - pad, feet - h - 0.25 * h - 30, 2 * pad, 1.55 * h + 60)
    cr.clip()
    cr.push_group()
    pts = dhani(cr, t, x, s, mood, feet=feet, front=front, backa=backa, head=head, legs=legs, hits=hits, flip=flip,
                rods=False, rot=rot, ph=ph, hand=hand, bhand=bhand, extra=extra)
    fig_pat = cr.pop_group()
    if sol < 1.0:                                                     # a warm rim of light round the figure
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)):
            cr.save()
            r_ = max(2.0, 0.012 * h)
            cr.translate(dx * r_, dy * r_)
            cr.set_source_rgba(*SOUL_GOLD, 0.5 * (1 - sol) * alpha)
            cr.mask(fig_pat)
            cr.restore()
    cr.set_source(fig_pat)
    cr.paint_with_alpha(alpha * (0.80 + 0.20 * sol))                  # a little translucent until it has a body
    if sol < 1.0:                                                     # lit from within: pale gold light over it
        cr.set_operator(cairo.OPERATOR_ADD)
        cr.set_source_rgba(*SOUL_GOLD, 0.22 * (1 - sol) * alpha * pul)
        cr.mask(fig_pat)
    cr.restore()
    return pts


# ------------------------------------------------------------------ additions (kneeling, Bhola seated)


def _kneel(skin, cloth, border, b, foot=None):
    """kaikeyi_cast.kneel_legs in the man's own cloth (hip at 0, 0; the ground at +KNEEL_H)."""
    import kaikeyi_cast as K
    return lambda cr: K.kneel_legs(cr, skin, cloth, border, b)


def _bhola_body_sit(cr):
    cr.save()
    cr.rectangle(-400, -600, 800, 660)
    cr.clip()
    bhola_body(cr)
    cr.restore()


def _bhola_bench(cr):
    """Bhola's legs seated on a bench / cot / throne (hip at 0, 0; the soles at +BENCH_H)."""
    import mandhata_cast as M
    M.seat_legs(cr, BH_SKIN, BH_CLOTH, BH_STRIPE, BH_B)


KNEEL_H = 250.0                       # kneeling: hip above the ground
BENCH_H = 268.0                       # seated on a bench / throne: hip above the floor (soles at +268)
register("yy_dhani_kneel", (-250, -60, 240, 260), _kneel(DH_SKIN, DH_PYJAMA, GOLD, 1.1))
register("yy_bhola_kneel", (-250, -60, 240, 260), _kneel(BH_SKIN, BH_CLOTH, BH_STRIPE, 0.84))
register("yy_bhola_body_sit", (-160, -320, 120, 70), _bhola_body_sit)
register("yy_bhola_bench", (-100, -60, 300, 290), _bhola_bench)


def dhani_kneel(cr, t, x, s, mood="calm", ground=FLOOR, **kw):
    """Dhaniram kneeling on one knee (hip at ground - KNEEL_H * s); the same options as dhani()."""
    sw = dict(kw.pop("swap", None) or {})
    hide = ("yy_dhani_legF", "yy_dhani_legB")
    r = kw.get("rot", 0.0)
    pc.prop(cr, "yy_dhani_kneel", x, ground - KNEEL_H * s, s, r, kw.get("alpha", 1.0), kw.get("blur", 0.0),
            kw.get("flip", False))
    kw.setdefault("bob", False)
    return _hidden(dhani, hide)(cr, t, x, s, mood, y=ground - KNEEL_H * s, swap=sw, **kw)


def bhola_kneel(cr, t, x, s, mood="calm", ground=FLOOR, **kw):
    """Bhola kneeling on one knee (no pot by default); the same options as bhola()."""
    kw.setdefault("pot", False)
    kw.setdefault("bob", False)
    pc.prop(cr, "yy_bhola_kneel", x, ground - KNEEL_H * s, s, kw.get("rot", 0.0), kw.get("alpha", 1.0),
            kw.get("blur", 0.0), kw.get("flip", False))
    return _hidden(bhola, ("yy_bhola_legF", "yy_bhola_legB"))(cr, t, x, s, mood, y=ground - KNEEL_H * s, **kw)


def bhola_seated(cr, t, x, s, mood="calm", ground=FLOOR, **kw):
    """Bhola seated on a bench / cot / throne whose seat is at ground - BENCH_H * s (legs down, soles on ground)."""
    kw.setdefault("pot", False)
    kw.setdefault("bob", False)
    sw = dict(kw.pop("swap", None) or {})
    sw["yy_bhola_body"] = "yy_bhola_body_sit"
    pc.prop(cr, "yy_bhola_bench", x, ground - BENCH_H * s, s, kw.get("rot", 0.0), kw.get("alpha", 1.0),
            kw.get("blur", 0.0), kw.get("flip", False))
    return _hidden(bhola, ("yy_bhola_legF", "yy_bhola_legB"))(cr, t, x, s, mood, y=ground - BENCH_H * s, swap=sw,
                                                              **kw)


def _hidden(fn, hide):
    """dhani() / bhola() with some parts hidden."""
    def call(*a, **kw):
        kw["hide"] = tuple(kw.get("hide") or ()) + tuple(hide)
        return fn(*a, **kw)
    return call
