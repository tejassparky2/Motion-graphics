"""The leather cast and props for the snake-tongue reel (videos/snake_tongue.py), in the Togalu Gombeyaata style of the
earlier reels (puppet_cast, ruru_cast, shani_cast, mandhata_cast, hanuman_cast): profile figures with big almond eyes,
perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor and no film. Every sprite
name starts with "sn_".

Cast (one look each, kept the same through the video; Garuda, Indra and both mothers with dignity):
  GARUDA      the king of birds as a mighty eagle-man (sn_garuda, puppet_cast.man): golden feathered body and arms, a
              pale eagle's face with a big hooked orange beak and a dark eye-stripe (shani_cast's Garuda), a red and
              gold crest, a tall gold kirita, a red dhoti with a gold border, a green sash, and two great
              red-gold-green wings rising from his back (sn_gwing_far / sn_gwing_near, parts of the rig, so they can
              beat); kneeling legs (sn_garuda_kneel). Faces: calm, talk (the beak open), angry (the brow down), smile.
  VINATA      his mother, gentle and patient (sn_vinata, puppet_cast.woman): warm skin, a plain soft-yellow cotton sari
              with a rust border, no crown, her hair in a plain bun with one flower; sweeping with a broom (sn_broom).
              Faces: calm, sad (eyes lowered), joy (eyes closed in a smile), shock.
  KADRU       the snakes' mother (sn_kadru): a dark-green sari with a gold border, a purple blouse, a gold tiara in
              front of a fan of five cobra hoods (the snakes' mother at a glance). Faces: smug (half-lidded, a sly
              smile), laugh, shock, calm.
  THE SNAKES  her sons (the bodies are drawn by the scenes, as scenes_ruru's snakes): dark-brown leather with cream
              bands (ruru_cast's colours) or green with gold bands; heads sn_snake_b / sn_snake_g (closed, a sly
              half-lidded eye) and *_open (the jaw dropped). The tongue is drawn by the scenes so it can flick and,
              at the end, split. sn_snake_big is the same head drawn three times larger for the close-ups.
  THE HORSE   Uchchaihshravas, the white horse of the gods (sn_horse, from jayadratha_cast's horse): white leather, a
              silver mane, gold ornaments; its long tail is its own piece, white (sn_tail) or black (sn_tail_black).
Props: the pot of amrit (sn_amrit: a gold kalasha with a domed lid), a drop of amrit (sn_drop), kusha grass (sn_kusha_
back / sn_kusha_front: tall, straight, sharp blades; sn_kusha_blade: one big blade with a saw edge; sn_kusha_bundle:
a tied bundle for the puja), the broom, a brass puja plate (sn_thali). Indra (mandhata_cast), the vajra, the guards
(shani_cast's devas as silhouettes), clouds, the gate, waves, altar, diya, thought bubble and plaques come from the
earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; the rigs come from puppet_cast.man() / woman().
"""
import math

import kaikeyi_cast as K
import ruru_cast as RU
import shani_cast as SG
from puppet_cast import HAIR, _flower, _jewel, _shape, man, man_body, woman
from puppet_core import (GOLD, GREEN, INK, PALE, RED, almond_eye, band, dots_in, ell, holes_line, ink, leather,
                         poly, punch, register, rivet, spath)
from ravana_cast import kirita

GA_BODY, GA_FACE, GA_BEAK, GA_RED, GA_GREEN = SG.GA_BODY, SG.GA_FACE, SG.GA_BEAK, SG.GA_RED, SG.GA_GREEN
GA_FEATHER = (0.72, 0.40, 0.10)       # feather lines on his gold body
GA_STRIPE = (0.36, 0.22, 0.12)        # the dark stripe through his eye
VN_SKIN = (0.97, 0.72, 0.50)          # Vinata
VN_SARI = (0.99, 0.84, 0.50)          # plain soft yellow cotton
VN_BORDER = (0.70, 0.26, 0.14)        # rust
VN_CHOLI = (0.80, 0.40, 0.22)
KD_SKIN = (0.90, 0.64, 0.44)          # Kadru
KD_SARI = (0.16, 0.46, 0.34)          # dark green
KD_PALLU = (0.10, 0.32, 0.24)
KD_CHOLI = (0.46, 0.20, 0.46)         # purple
SN_B, SN_B_BELLY = RU.SN_BITE, RU.SN_BITE_B         # the snakes: dark brown, cream
SN_G, SN_G_BELLY = (0.30, 0.52, 0.22), (0.92, 0.86, 0.48)   # a green brother, gold-cream
SN_MOUTH = (0.42, 0.07, 0.08)
HORSE_W = (0.99, 0.97, 0.92)          # the white horse
HORSE_W2 = (0.88, 0.86, 0.82)
MANE_W = (0.93, 0.93, 0.97)           # silver-white mane and tail
TAIL_BLACK = (0.13, 0.11, 0.12)
POT_GOLD = (1.0, 0.80, 0.26)
POT_GOLD2 = (0.93, 0.62, 0.14)
KUSHA = ((0.64, 0.78, 0.30), (0.80, 0.82, 0.38), (0.92, 0.84, 0.46), (0.54, 0.70, 0.26))
STRAW = RU.STRAW
STRAW2 = RU.STRAW2

HEAD_W = 100.0                        # a snake head's neck width (design units), as ruru_cast.HEAD_W
SNOUT = (214.0, 4.0)                  # where the tongue comes out of a snake head (head units)
TAIL_ROOT = (-296.0, -594.0)          # where the horse's tail joins its body (horse units)
POT_TOP = -420.0                      # the top of the amrit pot's finial (pot units)
POT_MOUTH = -318.0                    # the pot's rim (pot units)


# ------------------------------------------------------------------ Garuda


def garuda_head(cr, mood="calm"):
    """Garuda's eagle head facing +x, the neck at (0, 0): a ruff of pointed neck feathers, a red and gold crest
    sweeping back, a pale face, a big hooked orange beak, a dark eye-stripe, a tall gold kirita. mood: calm | talk
    (the beak open) | angry (the brow down) | smile (the eye curved)."""
    cr.save()                                                                    # the crest behind the head
    cr.translate(-40, -180)
    for k in range(6):
        cr.save()
        cr.rotate(math.pi * (0.80 + 0.075 * k))
        ln = 200 - 16 * k
        _shape(cr, [(0, -22), (ln * 0.8, -18), (ln, 0), (ln * 0.8, 18), (0, 22)], GA_RED if k % 2 == 0 else GOLD,
               3.5)
        ink(cr, [(10, 0), (ln * 0.8, 0)], 2, smooth=False, col=(0.5, 0.2, 0.06))
        cr.restore()
    cr.restore()
    cr.save()                                                                    # the ruff of neck feathers
    cr.translate(0, -70)
    for k in range(9):
        a = math.pi * (0.30 + 0.09 * k)
        cr.save()
        cr.rotate(a)
        _shape(cr, [(40, -18), (128 - 6 * (k % 2), 0), (40, 18)], GOLD if k % 2 else (1.0, 0.56, 0.16), 3,
               smooth=False)
        cr.restore()
    cr.restore()
    face = [(-60, -30), (-92, -90), (-96, -160), (-70, -214), (-14, -250), (50, -248), (98, -222), (124, -186),
            (130, -140), (116, -98), (84, -62), (40, -36), (-10, -22)]
    _shape(cr, face, GA_FACE, 6)
    for k in range(4):                                                           # feathered cheek lines
        ink(cr, [(-70 + 20 * k, -70 + 6 * k), (-30 + 20 * k, -48 + 2 * k), (16 + 16 * k, -50)], 2.4,
            col=(0.80, 0.60, 0.40))
    jaw_open = 0.32 if mood == "talk" else 0.0
    cr.save()                                                                    # the lower beak
    cr.translate(118, -118)
    cr.rotate(jaw_open)
    if jaw_open:
        _shape(cr, [(-6, -8), (70, -18), (96, -8), (60, 8)], (0.42, 0.06, 0.06), 3, smooth=False)
    _shape(cr, [(-6, 0), (52, -6), (84, -2), (70, 14), (24, 24), (-8, 20)], (0.92, 0.42, 0.10), 4.5)
    cr.restore()
    beak = [(110, -206), (160, -212), (210, -194), (242, -158), (248, -116), (232, -96), (224, -124), (204, -142),
            (164, -136), (114, -122)]
    _shape(cr, beak, GA_BEAK, 6)
    ink(cr, [(132, -150), (190, -156), (226, -132)], 3, col=(0.60, 0.24, 0.06))
    punch(cr, [(176, -182)], 5)
    _shape(cr, [(-14, -150), (40, -186), (112, -186), (96, -150), (24, -138)], GA_STRIPE, 3)   # the eye stripe
    if mood == "smile":
        ink(cr, [(40, -168), (62, -182), (86, -168)], 6, col=PALE)
        ink(cr, [(40, -168), (62, -182), (86, -168)], 3)
    else:
        almond_eye(cr, 62, -168, 50, 19, col=(1.0, 0.86, 0.30))
    if mood == "angry":                                                          # the brow down toward the beak
        _shape(cr, [(20, -214), (70, -206), (116, -184), (110, -172), (66, -190), (22, -200)], (0.46, 0.26, 0.10), 3)
    else:
        _shape(cr, [(18, -200), (66, -220), (116, -202), (108, -192), (66, -208), (24, -190)], (0.50, 0.30, 0.12), 3)
    _jewel(cr, -46, -110, 14, GOLD)                                              # an ear stud
    poly(cr, [(-52, -96), (-46, -70), (-40, -96)])
    leather(cr, RED, 3)
    cr.save()                                                                    # the crown
    cr.translate(8, -96)
    kirita(cr, GOLD, None, tall=0.9)
    cr.restore()


def _feathers(cr, b):
    """Feather chevrons over Garuda's gold chest and belly."""
    for row in range(5):
        for i in range(3):
            x = -30 * b + 34 * b * i + (16 * b if row % 2 else 0)
            y = -236 + 40 * row
            if x < 70 * b - row * 2:
                ink(cr, [(x - 14, y), (x, y + 14), (x + 14, y)], 2.6, col=GA_FEATHER)


def _gwing(cr, col, col2, tip, k=0.72):
    """Garuda's wing (pivot at the shoulder; reaching up and back): shani_cast's layered flight feathers in three
    colours and a perforated covert, a little smaller (k)."""
    cr.save()
    cr.scale(k, k)
    for i in reversed(range(9)):
        u = i / 8
        bx, by = -30 - 230 * u, -40 - 540 * u
        ang = math.pi - 0.25 + 1.15 * u
        ln = 240 + 110 * math.sin(math.pi * (0.25 + 0.7 * u))
        cr.save()
        cr.translate(bx, by)
        cr.rotate(ang)
        fp = [(0, -28), (ln * 0.5, -38), (ln * 0.9, -22), (ln, 0), (ln * 0.9, 20), (ln * 0.5, 32), (0, 26)]
        _shape(cr, fp, (col, col2, tip)[i % 3], 4.2)
        ink(cr, [(10, 0), (ln * 0.86, 0)], 2.2, smooth=False, col=(0.50, 0.26, 0.10))
        cr.restore()
    cov = [(40, 30), (10, -120), (-70, -330), (-170, -540), (-260, -640), (-300, -600), (-250, -480), (-190, -330),
           (-150, -180), (-120, -40), (-60, 50)]
    _shape(cr, cov, col2, 5, holes=(11, 15, 2.6))
    for j in range(2):
        ink(cr, [(-40 - 34 * j, 0), (-90 - 30 * j, -260), (-200 - 10 * j, -520)], 2.8, col=(0.66, 0.36, 0.10))
    rivet(cr, 0, 0, 10)
    cr.restore()


_GA = dict(skin=GA_BODY, bulk=1.28, dhoti=GA_RED, border=GOLD, pleat=GOLD, sash=GA_GREEN, neck=GOLD, halo=False,
           hands=("open", "open"))
GARUDA = man("sn_garuda", **_GA)
register("sn_garuda_body", (-200, -330, 140, 300), lambda cr: (man_body(cr, _GA), _feathers(cr, 1.28)))
GA_MOODS = ("calm", "talk", "angry", "smile")
for _m in GA_MOODS:
    register("sn_garuda_head" + ("" if _m == "calm" else "_" + _m), (-260, -560, 270, 40),
             (lambda m: lambda cr: garuda_head(cr, m))(_m))
register("sn_gwing_far", (-600, -820, 110, 130),
         lambda cr: _gwing(cr, (0.70, 0.16, 0.08), (0.86, 0.58, 0.18), (0.14, 0.44, 0.26)))
register("sn_gwing_near", (-600, -820, 110, 130), lambda cr: _gwing(cr, GA_RED, GA_BODY, GA_GREEN))
GARUDA.parts.insert(0, ("sn_gwing_far", "sn_garuda_body", (-50, -236), 0.10))
GARUDA.parts.insert(1, ("sn_gwing_near", "sn_garuda_body", (-60, -226), -0.30))
register("sn_garuda_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, GA_BODY, GA_RED, GOLD, 1.28))
GARUDA.points["beak"] = ("sn_garuda_head", (240, -130))
GARUDA.points["eye"] = ("sn_garuda_head", (62, -168))
GARUDA.points["wing"] = ("sn_gwing_near", (-200, -500))


# ------------------------------------------------------------------ the two mothers


def _hoods(cr):
    """Kadru's fan of five cobra hoods behind her head (each a hood with a small head, two eyes and the cream
    'spectacle' mark)."""
    cx, cy = -14, -122
    for k, a in enumerate((-162, -128, -94, -60, -26)):
        r = math.radians(a)
        cr.save()
        cr.translate(cx + 112 * math.cos(r), cy + 112 * math.sin(r))
        cr.rotate(r + math.pi / 2)
        cr.scale(1.18, 1.18)
        hood = [(0, 40), (-30, 22), (-40, -12), (-30, -46), (-14, -62), (0, -66), (14, -62), (30, -46), (40, -12),
                (30, 22)]
        _shape(cr, hood, SN_B, 4.5)
        _shape(cr, [(0, 30), (-16, 6), (-20, -18), (-8, -36), (0, -40), (8, -36), (20, -18), (16, 6)], SN_B_BELLY, 3)
        cr.new_path()
        ell(cr, 0, -78, 16, 20)
        leather(cr, SN_B, 4)
        punch(cr, [(-7, -82), (7, -82)], 3.4)
        ink(cr, [(-8, -12), (0, -4), (8, -12)], 2.6, col=SN_B)
        cr.restore()


def mom_head(cr, skin, mood="calm", kadru=False):
    """A mother's head (the neck at 0, 0), as puppet_cast.woman_head: Vinata (plain bun with one flower, no crown, a
    small bindi) or Kadru (the cobra hoods, a gold tiara, a nose ring). mood: calm | sad | joy | shock | smug |
    laugh."""
    if kadru:
        _hoods(cr)
    face = [(-20, 6), (-26, -36), (-44, -80), (-50, -126), (-38, -168), (0, -188), (36, -176), (50, -148),
            (54, -126), (58, -116), (76, -96), (60, -88), (63, -78), (56, -70), (60, -62), (50, -48), (46, -36),
            (30, -26), (22, 6)]
    if mood in ("laugh", "shock"):                                               # the mouth open
        face = face[:11] + [(60, -86), (64, -76), (52, -66), (60, -56), (50, -46), (46, -36), (30, -26), (22, 6)]
    _shape(cr, face, skin, 6)
    if mood in ("laugh", "shock"):
        cr.new_path()
        ell(cr, 56, -70, 6, 8 if mood == "shock" else 5)
        leather(cr, SN_MOUTH, 2.5)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    cr.new_path()
    cr.arc(-62, -128, 36, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    for i in range(8):
        a = 2 * math.pi * i / 8
        punch(cr, [(-62 + 24 * math.cos(a), -128 + 24 * math.sin(a))], 3.5)
    if kadru:
        _flower(cr, -62, -128, 14, GOLD)
        tp = [(-30, -172), (-20, -204), (-6, -186), (8, -216), (20, -186), (34, -206), (40, -170)]
        _shape(cr, tp, GOLD, 4, smooth=False)
        _jewel(cr, 8, -192, 7, GREEN)
        cr.new_path()                                                            # nose ring
        cr.arc(64, -90, 8, 0, 2 * math.pi)
        cr.set_source_rgb(*GOLD)
        cr.set_line_width(3)
        cr.stroke()
    else:
        _flower(cr, -82, -150, 13, RED, 6)
        band(cr, [(-32, -168), (2, -184), (36, -172)], 9, VN_BORDER, holes=False)
    # eyes and brows
    if mood == "sad":
        ink(cr, [(14, -114), (30, -106), (46, -114)], 4.5)
        for x in (22, 30, 38):
            ink(cr, [(x, -109), (x - 2, -101)], 2.2)
        ink(cr, [(12, -126), (30, -132), (48, -142)], 3.5)
    elif mood == "joy":
        ink(cr, [(14, -110), (30, -122), (46, -110)], 5)
        ink(cr, [(14, -134), (30, -142), (46, -136)], 3.5)
    elif mood == "shock":
        cr.new_path()
        ell(cr, 30, -114, 15, 13)
        leather(cr, PALE, 3.5)
        cr.new_path()
        cr.arc(32, -114, 6, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
        ink(cr, [(12, -138), (30, -148), (48, -140)], 3.5)
    elif mood in ("smug", "laugh"):
        almond_eye(cr, 30, -112, 32, 10, col=PALE)
        cr.new_path()                                                            # a half-lowered lid: sly
        cr.move_to(13, -112)
        cr.curve_to(22, -124, 40, -124, 47, -112)
        cr.curve_to(38, -116, 22, -116, 13, -112)
        cr.close_path()
        leather(cr, skin, 2.5)
        ink(cr, [(12, -132), (32, -130), (50, -122)], 3.5)
    else:
        almond_eye(cr, 30, -112, 32, 11, col=PALE)
        ink(cr, [(14, -128), (30, -134), (46, -128)], 3.5)
    ink(cr, [(46, -112), (60, -120)], 3)
    if mood in ("joy", "smug"):
        ink(cr, [(64, -76), (58, -70), (48, -72)], 3, col=(0.62, 0.20, 0.16))   # a smile
    elif mood == "sad":
        ink(cr, [(62, -70), (56, -74), (48, -72)], 3, col=(0.62, 0.20, 0.16))
    elif mood == "calm":
        ink(cr, [(62, -74), (56, -70)], 3, col=(0.62, 0.20, 0.16))
    cr.new_path()
    cr.arc(44, -150, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    _jewel(cr, -10, -70, 9 if not kadru else 11, GOLD)
    if kadru:
        poly(cr, [(-24, -58), (-10, -66), (4, -58), (8, -34), (-28, -34)])
        leather(cr, GOLD, 3)
        punch(cr, [(-18, -40), (-10, -40), (-2, -40)], 2.2)


VINATA = woman("sn_vinata", skin=VN_SKIN, skirt=VN_SARI, choli=VN_CHOLI, border=VN_BORDER, pallu_col=VN_SARI,
               gem=VN_BORDER, hands=("open", "open"))
VN_MOODS = ("calm", "sad", "joy", "shock")
for _m in VN_MOODS:
    register("sn_vinata_head" + ("" if _m == "calm" else "_" + _m), (-120, -240, 100, 30),
             (lambda m: lambda cr: mom_head(cr, VN_SKIN, m))(_m))
KADRU = woman("sn_kadru", skin=KD_SKIN, skirt=KD_SARI, choli=KD_CHOLI, border=GOLD, pallu_col=KD_PALLU, gem=RED,
              hands=("open", "open"))
KD_MOODS = ("smug", "laugh", "shock", "calm")
for _m in KD_MOODS:
    register("sn_kadru_head" + ("" if _m == "smug" else "_" + _m), (-230, -400, 180, 40),
             (lambda m: lambda cr: mom_head(cr, KD_SKIN, m, kadru=True))(_m))


def _broom(cr):
    """A short Indian broom (pivot at the grip): a red-bound handle, then fine straw fanning out to the bottom."""
    for i in range(15):
        u = (i - 7) / 7
        x1 = 80 * u
        ink(cr, [(4 * u, 60), (x1 * 0.6, 240), (x1, 430)], 6, col=INK)
        ink(cr, [(4 * u, 60), (x1 * 0.6, 240), (x1, 430)], 3.4, col=STRAW if i % 2 else STRAW2)
    _shape(cr, [(-18, -70), (18, -70), (16, 80), (-16, 80)], STRAW2, 4, smooth=False)
    for y in (-50, -10, 30, 66):
        band(cr, [(-18, y), (18, y + 4)], 12, RED, holes=False)


register("sn_broom", (-110, -90, 110, 450), _broom)


# ------------------------------------------------------------------ the snakes' heads


def snake_head(cr, col, belly, open_=0.0, k=1.0, lwk=1.0):
    """A snake's head in profile facing +x, the neck at x = 0 (HEAD_W * k wide), the snout at SNOUT * k: a sly
    half-lidded yellow eye with a slit pupil, a brow ridge, a smirk, punched holes; open_ 0..1 drops the jaw (the
    tongue is drawn by the scenes). k scales the drawing (sn_snake_big is k = 3), lwk the outlines."""
    cr.save()
    cr.scale(k, k)
    L = lambda w: w * lwk / k * (1 if k == 1 else 2.0)                          # outline widths
    hinge = (70, 16)
    ja = 0.42 * open_
    if open_ > 0:                                                                # the inside of the mouth
        c, s = math.cos(ja), math.sin(ja)
        tip = (hinge[0] + (198 - hinge[0]) * c - (12 - hinge[1]) * s,
               hinge[1] + (198 - hinge[0]) * s + (12 - hinge[1]) * c)
        _shape(cr, [hinge, (200, 8), tip], SN_MOUTH, L(3), smooth=False)
    jaw = [(-12, 24), (50, 22), (110, 16), (170, 12), (202, 10), (196, 26), (150, 40), (90, 48), (30, 52), (-12, 50)]
    cr.save()
    cr.translate(*hinge)
    cr.rotate(ja)
    cr.translate(-hinge[0], -hinge[1])
    _shape(cr, jaw, belly, L(5))
    holes_line(cr, [(20, 38), (100, 36), (160, 26)], 14, 2.2)
    cr.restore()
    top = [(-12, -50), (40, -62), (110, -64), (160, -50), (196, -26), (214, 0), (204, 10), (160, 12), (110, 14),
           (60, 20), (-12, 26)]
    _shape(cr, top, col, L(5))
    if k > 1:                                                                    # scales on the big head
        for row in range(3):
            for i in range(6):
                x = 10 + 26 * i + 13 * (row % 2)
                y = -44 + 14 * row
                if x < 150 - 12 * row:
                    ink(cr, [(x - 10, y), (x, y + 8), (x + 10, y)], 1.4, col=(0.24, 0.16, 0.08))
    cr.new_path()                                                                # the eye
    ell(cr, 128, -24, 19, 16)
    leather(cr, (1.0, 0.86, 0.22), L(3.5))
    cr.new_path()
    ell(cr, 130, -24, 4, 12)
    cr.set_source_rgb(*INK)
    cr.fill()
    punch(cr, [(124, -30)], 3.2)
    cr.new_path()                                                                # a half-lowered lid: sly
    cr.move_to(108, -24)
    cr.curve_to(114, -44, 142, -44, 148, -24)
    cr.curve_to(140, -32, 116, -32, 108, -24)
    cr.close_path()
    leather(cr, col, L(2.5))
    _shape(cr, [(96, -46), (130, -54), (164, -40), (160, -32), (130, -44), (100, -38)], (0.20, 0.12, 0.06), L(2.5))
    punch(cr, [(194, -10)], 3.2)
    if open_ <= 0:
        ink(cr, [(206, 6), (176, 12), (150, 10), (138, 2)], L(3.2), col=belly)  # a smirk
    holes_line(cr, [(0, -38), (60, -50), (100, -54)], 15, 2.4)
    for j in range(3):                                                           # neck creases
        ink(cr, [(8 + 14 * j, -36), (12 + 14 * j, -12), (8 + 14 * j, 14)], L(2.2), col=(0.2, 0.12, 0.06))
    cr.restore()


for _n, (_c, _b) in (("b", (SN_B, SN_B_BELLY)), ("g", (SN_G, SN_G_BELLY))):
    register(f"sn_snake_{_n}", (-30, -80, 230, 70), (lambda c, b: lambda cr: snake_head(cr, c, b))(_c, _b))
    register(f"sn_snake_{_n}_open", (-30, -80, 230, 150),
             (lambda c, b: lambda cr: snake_head(cr, c, b, 1.0))(_c, _b))
register("sn_snake_big", (-90, -240, 690, 210), lambda cr: snake_head(cr, SN_B, SN_B_BELLY, 0.0, 3.0, 0.55))
register("sn_snake_big_open", (-90, -240, 690, 460), lambda cr: snake_head(cr, SN_B, SN_B_BELLY, 0.6, 3.0, 0.55))


# ------------------------------------------------------------------ the white horse and its tail


def _horse(cr):
    """jayadratha_cast's horse in profile facing +x (pivot on the ground under the middle of its body), in white
    leather with a silver mane, a gold crest and collar, a red and gold saddle-cloth; no tail (sn_tail is separate)."""
    col, c2 = HORSE_W, HORSE_W2

    def fore(x, c):
        p = [(x - 36, -500), (x + 36, -500), (x + 28, -330), (x + 18, -150), (x + 22, -70), (x + 34, -24), (x + 40, 0),
             (x - 16, 0), (x - 14, -30), (x - 18, -90), (x - 22, -160), (x - 30, -330)]
        _shape(cr, p, c, 5)
        band(cr, [(x - 16, -16), (x + 38, -16)], 14, GOLD, holes=False)
        band(cr, [(x - 22, -150), (x + 20, -150)], 9, GOLD, spacing=8, hole_r=1.8)

    def hind(x, c):
        p = [(x - 64, -530), (x + 52, -530), (x + 40, -400), (x + 12, -300), (x + 30, -200), (x + 24, -80),
             (x + 34, -24), (x + 40, 0), (x - 16, 0), (x - 14, -30), (x - 10, -90), (x - 14, -200), (x - 36, -290),
             (x - 54, -400)]
        _shape(cr, p, c, 5)
        band(cr, [(x - 16, -16), (x + 38, -16)], 14, GOLD, holes=False)

    hind(-236, c2)
    fore(150, c2)
    body = [(-300, -560), (-288, -622), (-220, -664), (-60, -664), (100, -654), (222, -642), (292, -600), (304, -530),
            (272, -452), (160, -424), (0, -432), (-160, -424), (-262, -452), (-302, -502)]
    _shape(cr, body, col, 6)
    neck = [(170, -626), (232, -726), (302, -826), (362, -884), (420, -904), (452, -872), (432, -802), (384, -722),
            (334, -604), (284, -524)]
    _shape(cr, neck, col, 6)
    head = [(382, -902), (432, -934), (474, -922), (524, -862), (584, -792), (594, -762), (564, -742), (512, -752),
            (462, -792), (412, -830)]
    _shape(cr, head, col, 6)
    _shape(cr, [(402, -912), (412, -976), (434, -918)], col, 4, smooth=False)
    cr.new_path()
    ell(cr, 456, -872, 16, 10, 0.5)
    leather(cr, PALE, 3)
    cr.new_path()
    cr.arc(460, -870, 6, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    punch(cr, [(572, -770)], 5)
    ink(cr, [(560, -752), (536, -748)], 3)
    band(cr, [(448, -900), (500, -800), (560, -760)], 10, GOLD, spacing=10, hole_r=1.8)          # bridle
    mane = [(178, -660), (238, -758), (306, -858), (372, -918), (402, -930)]
    band(cr, mane, 30, MANE_W, spacing=12, hole_r=2.6)
    for i in range(7):
        u = i / 6
        x = 190 + (390 - 190) * u
        y = -680 - (928 - 680) * u
        _shape(cr, [(x - 12, y), (x - 46, y + 8), (x - 10, y + 24)], MANE_W, 2.5, smooth=False)
    _shape(cr, [(410, -930), (392, -1010), (420, -1060), (434, -1000), (428, -930)], GOLD, 3, holes=(6, 10, 2))
    cloth = [(-140, -664), (70, -660), (84, -548), (-150, -552)]
    _shape(cr, cloth, RED, 5, smooth=False, holes=(9, 12, 2.4))
    dots_in(cr, lambda: poly(cr, [(-120, -640), (60, -640), (66, -572), (-128, -572)]), 20, 3.0, shape="d")
    band(cr, [(-150, -556), (86, -552)], 14, GOLD, spacing=11, hole_r=2.2)
    band(cr, [(250, -650), (300, -570), (290, -486)], 18, GOLD, spacing=11, hole_r=2.4)       # breast collar
    for y in (-600, -540):
        _jewel(cr, 298, y, 7, RED)
    fore(214, col)
    hind(-196, col)
    holes_line(cr, [(-240, -600), (0, -620), (200, -600)], 26, 3)


def _tail(cr, col, strand):
    """The horse's long tail (pivot at its root): a flowing switch down to the ground with long strands."""
    pts = [(-12, -20), (26, 4), (16, 110), (-20, 240), (-70, 380), (-120, 500), (-150, 590), (-210, 600),
           (-190, 520), (-160, 420), (-124, 300), (-84, 160), (-44, 30)]
    _shape(cr, pts, col, 5)
    for k in range(5):
        ink(cr, [(-4 - 8 * k, 30), (-34 - 12 * k, 200), (-90 - 12 * k, 400), (-150 - 8 * k, 560)], 2.6, col=strand)
    band(cr, [(-16, 0), (20, 10)], 18, GOLD, spacing=9, hole_r=2.0)


register("sn_horse", (-330, -1080, 610, 10), _horse)
register("sn_tail", (-230, -40, 50, 620), lambda cr: _tail(cr, MANE_W, (0.62, 0.62, 0.70)))
register("sn_tail_black", (-230, -40, 50, 620), lambda cr: _tail(cr, TAIL_BLACK, (0.42, 0.40, 0.42)))


# ------------------------------------------------------------------ the pot of amrit, a drop


def _amrit(cr):
    """The pot of amrit (pivot at the bottom centre): a gold kalasha with red bands, a painted lotus, a domed lid and
    a finial."""
    _shape(cr, [(-62, 0), (62, 0), (52, -34), (-52, -34)], POT_GOLD2, 5, smooth=False)
    belly = [(-52, -30), (-110, -70), (-136, -150), (-122, -230), (-70, -278), (-44, -290), (44, -290), (70, -278),
             (122, -230), (136, -150), (110, -70), (52, -30)]
    _shape(cr, belly, POT_GOLD, 6)
    dots_in(cr, lambda: spath(cr, belly), 26, 2.6)
    band(cr, [(-132, -186), (0, -196), (132, -186)], 18, RED, spacing=12, hole_r=2.4)
    band(cr, [(-118, -90), (0, -80), (118, -90)], 14, RED, spacing=12, hole_r=2.2)
    for k, a in enumerate((-0.9, -0.45, 0.0, 0.45, 0.9)):                         # a painted lotus
        cr.save()
        cr.translate(0, -112)
        cr.rotate(a)
        _shape(cr, [(0, 0), (-14, -26), (0, -50), (14, -26)], (0.96, 0.44, 0.40) if k % 2 else (0.98, 0.62, 0.52),
               2.6)
        cr.restore()
    _shape(cr, [(-46, -286), (46, -286), (40, -310), (-40, -310)], POT_GOLD2, 4.5, smooth=False)
    _shape(cr, [(-80, -306), (80, -306), (74, -326), (-74, -326)], POT_GOLD, 4.5, smooth=False, holes=(6, 11, 2))
    lid = [(-70, -322), (-60, -360), (-26, -384), (26, -384), (60, -360), (70, -322)]
    _shape(cr, lid, POT_GOLD, 5)
    band(cr, [(-62, -346), (0, -356), (62, -346)], 10, RED, spacing=10, hole_r=2.0)
    _shape(cr, [(-14, -380), (14, -380), (10, -398), (-10, -398)], POT_GOLD2, 3.5, smooth=False)
    _shape(cr, [(0, POT_TOP), (-16, -404), (0, -396), (16, -404)], POT_GOLD, 3, smooth=False)
    _jewel(cr, 0, -240, 12, GREEN)


def _drop(cr):
    """A drop of amrit (pivot at its centre): a golden-white tear shape with a shine."""
    _shape(cr, [(0, -46), (18, -10), (22, 12), (10, 28), (-10, 28), (-22, 12), (-18, -10)], (1.0, 0.92, 0.56), 4)
    punch(cr, [(-6, 8)], 5)


register("sn_amrit", (-150, POT_TOP - 20, 150, 10), _amrit)
register("sn_drop", (-30, -56, 30, 36), _drop)


# ------------------------------------------------------------------ kusha grass


def _blade(cr, L, w, col, bend=0.0):
    """One kusha blade from (0, 0) straight up L units, w wide at the base, a needle-sharp tip, a mid-rib."""
    tip = (bend * L, -L)
    pts = [(-w / 2, 0), (-w * 0.42 + bend * L * 0.4, -L * 0.45), (bend * L * 0.9 - w * 0.12, -L * 0.88), tip,
           (bend * L * 0.9 + w * 0.12, -L * 0.88), (w * 0.42 + bend * L * 0.4, -L * 0.45), (w / 2, 0)]
    _shape(cr, pts, col, 3.4, smooth=False)
    ink(cr, [(0, -4), (bend * L * 0.5, -L * 0.5), (bend * L * 0.93, -L * 0.93)], 1.8, smooth=False,
        col=(0.30, 0.40, 0.12))


_BACK = [(-420, 560, -0.30), (-370, 700, -0.20), (-320, 640, -0.08), (-280, 480, 0.02), (280, 500, -0.02),
         (320, 660, 0.08), (370, 720, 0.20), (420, 560, 0.30), (-200, 260, -0.12), (-110, 230, -0.04), (0, 220, 0.0),
         (110, 240, 0.05), (200, 250, 0.12), (-470, 400, -0.5), (470, 420, 0.5)]
_FRONT = [(-380, 300, -0.42), (-300, 380, -0.25), (-220, 200, -0.2), (-140, 150, -0.1), (-60, 120, -0.04),
          (60, 130, 0.04), (140, 160, 0.1), (220, 210, 0.2), (300, 370, 0.25), (380, 310, 0.42), (-450, 220, -0.7),
          (450, 230, 0.7)]


def _kusha(cr, blades, w=30, mound=True):
    """A patch of kusha (pivot at its middle on the ground): tall sharp blades at the two sides, short ones in the
    middle (where the pot stands), on a low mound."""
    if mound:
        _shape(cr, [(-280, 6), (-230, -30), (0, -44), (230, -30), (280, 6), (0, 16)], (0.56, 0.44, 0.20), 4)
    for i, (x, L, a) in enumerate(blades):
        cr.save()
        cr.translate(x * 0.5, -8)
        cr.rotate(a)
        _blade(cr, L, w, KUSHA[i % len(KUSHA)], 0.02 * (1 if i % 2 else -1))
        cr.restore()


def _kusha_blade(cr):
    """One big kusha blade for the close-up (pivot at the base): its edges cut into tiny saw teeth (it is sharp)."""
    L, w = 1000, 70
    pts = [(-w / 2, 0)]
    n = 26
    for i in range(1, n):
        u = i / n
        hw = w / 2 * (1 - u) ** 0.8
        pts.append((-hw - (6 if i % 2 else 0), -L * u))
    pts.append((0, -L))
    for i in reversed(range(1, n)):
        u = i / n
        hw = w / 2 * (1 - u) ** 0.8
        pts.append((hw + (6 if i % 2 else 0), -L * u))
    pts.append((w / 2, 0))
    _shape(cr, pts, KUSHA[0], 4, smooth=False)
    ink(cr, [(0, -6), (0, -L * 0.96)], 2.6, smooth=False, col=(0.30, 0.40, 0.12))
    holes_line(cr, [(-10, -60), (-6, -500)], 30, 2.2, smooth=False)


def _bundle(cr):
    """A tied bundle of kusha for the puja (pivot at its middle): straight blades with sharp tips, a red thread."""
    for i in range(9):
        y = -36 + 9 * i
        L = 250 + 30 * math.sin(i * 1.7)
        _shape(cr, [(-230, y - 6), (L - 40, y - 7), (L, y), (L - 40, y + 7), (-230, y + 6)], KUSHA[i % 4], 2.6,
               smooth=False)
    for x in (-160, -120):
        band(cr, [(x, -46), (x + 8, 46)], 14, RED, holes=False)


register("sn_kusha_back", (-560, -780, 560, 30), lambda cr: _kusha(cr, _BACK))
register("sn_kusha_front", (-560, -440, 560, 30), lambda cr: _kusha(cr, _FRONT, 32, False))
register("sn_kusha_blade", (-50, -1010, 50, 10), _kusha_blade)
register("sn_kusha_bundle", (-240, -60, 300, 60), _bundle)


def _thali(cr):
    """A brass puja plate seen from the side (pivot at its bottom centre), a red painted band."""
    _shape(cr, [(-270, -22), (-210, -50), (210, -50), (270, -22), (226, 0), (-226, 0)], POT_GOLD2, 5)
    band(cr, [(-246, -26), (0, -20), (246, -26)], 10, RED, spacing=11, hole_r=2.0)
    holes_line(cr, [(-200, -40), (200, -40)], 18, 2.4)


register("sn_thali", (-290, -70, 290, 12), _thali)
