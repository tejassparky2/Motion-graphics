"""The leather cast and props for the Dharmavyadha reel (videos/dharmavyadha.py), in the Togalu Gombeyaata style of the
Jarasandha, Kaikeyi, Lakshman Rekha, Mandhata, Jayadratha, Arjuna and Ruru reels (puppet_cast, kaikeyi_cast,
lrekha_cast, mandhata_cast, jayadratha_cast, arjuna_cast, ruru_cast): profile figures with big almond eyes, perforated
garments and jointed limbs. Traditional leather puppets, modelled on no actor and no film. Every sprite name starts
with "dv_".

Cast (one look each, kept the same through the video):
  KAUSHIKA      the proud young ascetic: warm tan skin, dark matted hair piled in a round bun bound with rudraksha
                beads, matted locks down his back, a pointed dark beard and moustache, three ash lines, a rudraksha
                mala and the sacred thread on a bare chest, an ochre dhoti with a dark-red border. Faces: calm, angry,
                sad (eyes cast down, a tear), shock (wide eye, jaw dropped), humble (eyes gently shut, a small smile).
                Kneels; sits cross-legged. Props: an open palm leaf to read, the tied palm-leaf Veda bundle, a
                begging bowl.
  THE CRANE     a white she-crane (an egret): long S-neck, yellow beak, black legs, grey wing tips; perched, falling
                softly with her wings half open (eye shut), lying still on her side. A white feather, a white drop.
  THE HOUSEWIFE a simple teal-green cotton sari with a red pallu and border, a yellow blouse, hair in a bun with a few
                jasmine flowers, sindoor and a bindi, a small nose ring; calm and sure. Faces: open, calm (lids
                lowered), smile, speak. Her clay water pot is mandhata_cast's md_kalasha.
  THE HUSBAND   a tired working man: sun-tanned, a white head-cloth, a moustache, a short cream dhoti, a red towel
                over his shoulder, a hoe. Faces: tired, smile. Sits cross-legged to eat.
  THE BUTCHER   the meat-seller of Mithila, dignified and kind: deep brown skin, a maroon turban, a moustache, a
                white tilak with a red dot, a cream dhoti with a green border and a plain brown leather apron. Faces:
                calm, smile, speak. Kneels to wash his father's feet.
  HIS PARENTS   old, white-haired, seated side by side on a wooden bench, smiling: the father (white top-knot and
                beard, a green shawl), the mother (a grey bun with a flower, a rose sari).
  KAUSHIKA'S PARENTS  old and alone at a far-away hut, seated on a rope cot, eyes closed (blind with grief): the father
                (white top-knot with rudraksha, a long white beard, ash lines, a pale ochre robe), the mother (her
                cream sari over her white hair). Faces: shut (sad), smile (eyes still shut).
Sets and props: a big tree with a long bare branch for the crane, a village house with a lit doorway, a mud wall (the
house's edge), a room's back wall (niche, pots, window), the Mithila market stall (an awning, plain hanging shapes,
a wooden counter with a chopping block and a weighing scale; no blood), a basket stall, the Mithila skyline, a wooden
bench, a rope cot, a banana-leaf plate of food, a brass basin, a hoe. The palm-leaf book, speech cloud, thought
bubble, torn note, plaque, lota, hut, lamp, sun and flames come from the earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math
import random

import arjuna_cast as A
import kaikeyi_cast as K
import lrekha_cast as L  # noqa: F401  (registers the palm-leaf book, speech cloud, hut)
import mandhata_cast as M
import ravana_cast as R  # noqa: F401  (registers the torn note)
import ruru_cast as RU
import six_cast_a as SA  # noqa: F401  (registers the brass lota)
from puppet_cast import HAIR, _flower, _jewel, _shape, man, man_body, woman, woman_body
from puppet_core import (BROWN, DGREEN, DRED, GOLD, GREEN, INK, OCHRE, PALE, RED, SAFFRON, band, cut, dots_in, ell,
                         holes_line, ink, leather, poly, punch, register, rivet, spath)

KA_SKIN = (0.93, 0.66, 0.42)          # Kaushika
KA_CLOTH = (0.97, 0.58, 0.16)         # his ochre dhoti
KA_CLOTH2 = (1.0, 0.76, 0.40)
KA_SASH = (0.84, 0.42, 0.12)
JATA = (0.36, 0.22, 0.10)             # matted hair and beard
WHITE = (0.84, 0.88, 0.97)            # the crane: a cool white, so it reads on the warm cloth
WING_G = (0.62, 0.64, 0.70)
BEAK = (1.0, 0.76, 0.16)
WF_SKIN = (0.96, 0.70, 0.50)          # the housewife
WF_SARI = (0.22, 0.62, 0.52)          # teal green cotton
WF_PALLU = (0.82, 0.22, 0.14)
WF_CHOLI = (0.99, 0.74, 0.22)
HB_SKIN = (0.80, 0.52, 0.30)          # the husband
HB_DHOTI = (0.97, 0.92, 0.78)
HB_TOWEL = (0.86, 0.24, 0.16)
VY_SKIN = (0.74, 0.48, 0.28)          # the butcher
VY_DHOTI = (0.96, 0.90, 0.76)
VY_TURBAN = (0.62, 0.16, 0.12)
APRON = (0.58, 0.38, 0.20)
APRON2 = (0.44, 0.27, 0.13)
BF_SKIN = (0.80, 0.56, 0.36)          # the butcher's father
BF_SHAWL = (0.36, 0.60, 0.34)
BM_SKIN = (0.86, 0.62, 0.44)          # the butcher's mother
BM_SARI = (0.78, 0.30, 0.36)
KF_SKIN = (0.90, 0.68, 0.48)          # Kaushika's father
KF_ROBE = (0.98, 0.80, 0.52)
KM_SKIN = (0.94, 0.72, 0.54)          # Kaushika's mother
KM_SARI = (0.97, 0.93, 0.82)
ASH = (0.92, 0.91, 0.88)              # white hair
ASH2 = (0.66, 0.64, 0.62)
WOOD = K.WOOD
MUD = (0.88, 0.64, 0.38)
MUD2 = (0.94, 0.78, 0.54)
TILE = (0.80, 0.34, 0.18)
LEAFC = (0.94, 0.84, 0.56)            # palm leaf
BANANA = (0.40, 0.70, 0.28)
RICE = (1.0, 0.98, 0.92)
BRASS = (0.98, 0.76, 0.30)
WATER = (0.70, 0.86, 1.0)
HANG = (0.66, 0.46, 0.32)             # the plain hanging shapes in the stall

SEAT_H = 96.0                         # cross-legged: hip above the ground
BENCH_H = 268.0                       # seated on a bench or cot: hip above the ground (soles at +268)


# ------------------------------------------------------------------ shared pieces


def _ash_lines(cr, x0=6, x1=46, y0=-170, col=(1.0, 0.97, 0.9)):
    for k in range(3):
        ink(cr, [(x0, y0 + 9 * k), (x1, y0 - 2 + 9 * k)], 3.2, col=col)


def _sit_body(o, clip=64):
    """man_body with the front pleats tucked away (they would hang into the ground when he sits)."""
    def fn(cr):
        cr.save()
        cr.rectangle(-400, -600, 800, 600 + clip)
        cr.clip()
        man_body(cr, o)
        cr.restore()
    return fn


def _cross_seat(cr, dhoti, border, skin):
    """Cross-legged in profile (hip at 0, 0; the ground at y = +SEAT_H), as ruru_cast._khag_seat."""
    th = [(-80, -30), (40, -44), (160, -32), (250, -10), (266, 40), (250, 86), (120, 96), (-40, 96), (-92, 70),
          (-96, 14)]
    _shape(cr, th, dhoti, 5)
    dots_in(cr, lambda: spath(cr, th), 19, 2.8)
    band(cr, [(246, -8), (266, 40), (250, 86)], 14, border, spacing=11, hole_r=2.4)
    band(cr, [(-84, 88), (240, 90)], 10, border, holes=False)
    foot = [(104, 8), (150, -6), (204, 0), (222, 22), (196, 38), (118, 40)]
    _shape(cr, foot, skin, 4)
    for x in (196, 206, 214):
        ink(cr, [(x, 4), (x + 4, 18)], 2.2)
    rivet(cr, 0, 0, 9)


def _old_wrinkles(cr):
    ink(cr, [(18, -164), (40, -168)], 2.2)
    ink(cr, [(14, -176), (38, -180)], 2.2)
    ink(cr, [(40, -100), (48, -84)], 2.2)
    ink(cr, [(8, -96), (2, -80)], 2.0)


# ------------------------------------------------------------------ Kaushika


_KA_O = dict(skin=KA_SKIN, hair=False, moustache=True, tilak=False, earring=False)


def kau_head(cr, mood="calm"):
    """Kaushika: matted locks down his back, a pointed dark beard, a hair cap and a round matted bun bound with
    rudraksha, three ash lines and a red dot. mood: calm | angry | sad | shock | humble."""
    for k in range(3):                                                           # matted locks hanging behind
        x0 = -36 - 10 * k
        lock = [(x0 + 10, -170), (x0 - 18, -120), (x0 - 26 - 6 * k, -20), (x0 - 30 - 8 * k, 70 - 14 * k),
                (x0 - 12 - 8 * k, 74 - 14 * k), (x0 - 8, -30), (x0 + 6, -120)]
        _shape(cr, lock, JATA, 4)
        holes_line(cr, [(x0 - 6, -130), (x0 - 18 - 6 * k, -20), (x0 - 20 - 8 * k, 50 - 14 * k)], 16, 2.2)
    base = {"sad": "weep", "humble": "sleep"}.get(mood, mood)
    RU.rface(cr, _KA_O, base)
    if mood == "humble":
        ink(cr, [(56, -70), (62, -64), (70, -68)], 3.5)
    beard = [(60, -50), (66, -30), (60, 10), (44, 58), (26, 92), (16, 50), (0, 14), (-8, -34), (14, -40), (36, -52)]
    if mood == "shock":
        beard = [(60, -40), (66, -18), (60, 22), (44, 70), (26, 104), (16, 60), (0, 24), (-8, -30), (14, -34),
                 (36, -44)]
    _shape(cr, beard, JATA, 4)
    holes_line(cr, [(46, -30), (36, 20), (26, 70)], 14, 2.2)
    cap = [(-58, -116), (-62, -160), (-44, -196), (0, -212), (42, -200), (54, -184), (24, -186), (-8, -180),
           (-34, -160), (-42, -116)]
    _shape(cr, cap, JATA, 4)
    holes_line(cr, [(-50, -130), (-40, -176), (0, -200)], 15, 2.4)
    cr.new_path()                                                                # the round matted bun
    ell(cr, -16, -246, 50, 42, -0.1)
    leather(cr, JATA, 4)
    for r in (34, 20):
        cr.new_path()
        cr.arc(-16, -246, r, 0.4, 5.6)
        cr.set_source_rgb(0.62, 0.42, 0.22)
        cr.set_line_width(3)
        cr.stroke()
    punch(cr, [(-16 + 28 * math.cos(a), -246 + 24 * math.sin(a)) for a in (0.2, 1.4, 2.6, 3.8, 5.0)], 3.0)
    for i in range(7):                                                           # rudraksha strand round the bun
        u = i / 6
        cr.new_path()
        cr.arc(-60 + 88 * u, -214 - 16 * math.sin(math.pi * u), 6, 0, 2 * math.pi)
        leather(cr, BROWN, 2)
    _ash_lines(cr, 8, 48, -176)
    cr.new_path()
    cr.arc(30, -150, 5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()


_KA = dict(skin=KA_SKIN, bulk=0.94, dhoti=KA_CLOTH, border=DRED, pleat=KA_CLOTH2, sash=KA_SASH, neck=BROWN,
           beads=True, thread=True)
KAU = man("dv_kau", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"), **_KA)
for _m in ("calm", "angry", "sad", "shock", "humble"):
    register("dv_kau_head" + ("" if _m == "calm" else "_" + _m), (-150, -310, 120, 130),
             (lambda m: lambda cr: kau_head(cr, m))(_m))
register("dv_kau_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, KA_SKIN, KA_CLOTH, DRED, 0.94))
register("dv_kau_body_sit", (-200, -330, 140, 80), _sit_body(_KA))
register("dv_kau_seat", (-110, -60, 280, 110), lambda cr: _cross_seat(cr, KA_CLOTH, DRED, KA_SKIN))


def _pleaf(cr):
    """An open palm leaf held in both hands (pivot at its centre): lines of writing, two string holes."""
    pts = [(-170, -26), (170, -30), (184, -12), (180, 14), (166, 26), (-166, 30), (-182, 12), (-184, -10)]
    _shape(cr, pts, LEAFC, 4)
    for k, y in enumerate((-12, 0, 12)):
        for x0 in range(-150, 150, 46):
            ink(cr, [(x0, y), (x0 + 30 + 8 * ((x0 // 46 + k) % 2), y)], 2.2, smooth=False, col=(0.42, 0.28, 0.14))
    punch(cr, [(-110, 0), (110, 0)], 5)


def _bundle(cr):
    """The palm-leaf Veda bundle between two wooden boards, tied with a red string (pivot at the bottom centre)."""
    for y in (-30, -22, -14):
        _shape(cr, [(-150, y), (150, y - 1), (152, y + 8), (-152, y + 9)], LEAFC, 2.5, smooth=False)
    for y in (-46, -6):
        _shape(cr, [(-158, y), (158, y), (160, y + 14), (-160, y + 14)], WOOD, 4, smooth=False)
    for x in (-80, 80):
        ink(cr, [(x, -50), (x + 4, 10)], 4, col=RED)
    ink(cr, [(80, -50), (110, -74), (126, -66)], 3, col=RED)


def _bowl(cr):
    """A begging bowl of polished coconut shell (pivot at its bottom centre)."""
    pts = [(-90, -70), (90, -70), (82, -36), (56, -8), (0, 2), (-56, -8), (-82, -36)]
    _shape(cr, pts, (0.50, 0.30, 0.14), 5)
    band(cr, [(-90, -66), (90, -66)], 10, (0.72, 0.48, 0.24), holes=False)
    holes_line(cr, [(-62, -40), (0, -26), (62, -40)], 16, 2.6)


register("dv_pleaf", (-190, -36, 190, 36), _pleaf)
register("dv_bundle", (-165, -80, 165, 14), _bundle)
register("dv_bowl", (-96, -80, 96, 8), _bowl)


# ------------------------------------------------------------------ the crane


def _crane_body(cr, eye="open", wing_open=0.0, legs=True, lie=False):
    """The she-crane in profile facing +x, feet at (0, 0): a white teardrop body, an S-neck, a small head with a long
    yellow beak and two plumes, a folded wing with grey tips (or half open), long black legs."""
    if legs:
        for dx, k in ((-14, 0.75), (10, 1.0)):
            ink(cr, [(dx, -230), (dx + 4, -120), (dx, 0)], 14, smooth=False, col=INK)
            for tx in (-40, 0, 46):
                ink(cr, [(dx, 0), (dx + tx, 4)], 8, smooth=False, col=INK)
    body = [(-200, -330), (-120, -300), (-20, -260), (70, -270), (120, -310), (130, -360), (96, -400), (20, -410),
            (-80, -390), (-170, -360)]
    neck = [(90, -390), (130, -420), (120, -480), (80, -540), (90, -600), (130, -630), (160, -630), (150, -600),
            (120, -570), (120, -520), (160, -470), (166, -410), (126, -350)]
    if lie:                                                                      # the neck lies along the ground
        neck = [(100, -380), (150, -370), (200, -330), (250, -290), (300, -280), (320, -296), (310, -320),
                (260, -320), (210, -350), (150, -400), (120, -410)]
    _shape(cr, neck, WHITE, 9)
    _shape(cr, body, WHITE, 10)
    tail = [(-190, -340), (-260, -300), (-250, -290), (-180, -312)]
    _shape(cr, tail, WING_G, 6, smooth=False)
    if wing_open <= 0:
        wing = [(-150, -350), (-60, -390), (60, -380), (90, -340), (30, -310), (-80, -306), (-230, -296),
                (-250, -310)]
        _shape(cr, wing, (0.76, 0.81, 0.92), 7)
        for k in range(4):
            ink(cr, [(-60 + 30 * k, -370), (-150 + 26 * k, -316)], 4, col=WING_G)
        _shape(cr, [(-250, -310), (-230, -296), (-160, -304), (-190, -322)], (0.30, 0.30, 0.34), 5, smooth=False)
    hx, hy = (300, -306) if lie else (148, -616)
    ang = 0.35 if lie else 0.0
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(ang)
    head = [(-30, -6), (-16, -28), (14, -32), (34, -18), (36, 6), (14, 18), (-20, 16)]
    _shape(cr, head, WHITE, 7)
    beak = [(30, -12), (150, 2), (32, 10)]
    _shape(cr, beak, BEAK, 6, smooth=False)
    ink(cr, [(34, 0), (140, 2)], 3, smooth=False)
    for k in range(2):                                                           # the plumes behind the head
        ink(cr, [(-24, -18 + 8 * k), (-70, -10 + 14 * k), (-100, 6 + 16 * k)], 4)
    if eye == "open":
        cr.new_path()
        cr.arc(6, -10, 11, 0, 2 * math.pi)
        leather(cr, (1.0, 0.86, 0.20), 3.5)
        cr.new_path()
        cr.arc(8, -10, 5.5, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
    else:
        ink(cr, [(-6, -10), (6, -2), (18, -10)], 5)
    cr.restore()
    holes_line(cr, [(-150, -340), (-40, -356), (70, -344)], 20, 3.4)


def _crane_wing(cr):
    """A crane's wing spread (pivot at the shoulder, the wing reaching back and up)."""
    pts = [(0, 0), (-60, -60), (-160, -140), (-300, -180), (-360, -170), (-330, -130), (-280, -110), (-300, -90),
           (-240, -70), (-250, -50), (-170, -30), (-60, 20)]
    _shape(cr, pts, (0.76, 0.81, 0.92), 8)
    for k in range(5):
        ink(cr, [(-60 - 40 * k, -20 - 26 * k), (-110 - 46 * k, -60 - 22 * k)], 4, col=WING_G)
    _shape(cr, [(-300, -180), (-360, -170), (-330, -130), (-280, -110), (-300, -150)], (0.30, 0.30, 0.34), 5)
    rivet(cr, 0, 0, 9)


def _crane_lie(cr):
    cr.translate(0, 262)                                                         # the ground at y = 0
    _crane_body(cr, "shut", legs=False, lie=True)


register("dv_crane", (-270, -660, 320, 20), lambda cr: _crane_body(cr))
register("dv_crane_shut", (-270, -660, 320, 20), lambda cr: _crane_body(cr, "shut"))
register("dv_crane_fly", (-270, -660, 320, 20), lambda cr: _crane_body(cr, "shut", 1.0, legs=True))
register("dv_crane_flyo", (-270, -660, 320, 20), lambda cr: _crane_body(cr, "open", 1.0, legs=True))
register("dv_crane_lie", (-270, -180, 480, 30), _crane_lie)
register("dv_crane_wing", (-375, -200, 24, 44), _crane_wing)
CR_C = (-40.0, -340.0)                # the crane's body centre (crane units; feet at 0, 0)
CR_SHOULDER = (60.0, -372.0)          # where a spread wing joins the body
CR_TAIL = (-240.0, -300.0)


def _feather(cr):
    """A white feather (pivot at its quill end)."""
    pts = [(0, 0), (-10, -40), (-14, -120), (-4, -200), (10, -240), (22, -200), (26, -120), (18, -40)]
    _shape(cr, pts, WHITE, 6)
    ink(cr, [(4, 10), (6, -120), (10, -232)], 3, col=WING_G)
    for k in range(6):
        y = -40 - 32 * k
        ink(cr, [(6, y), (-8, y - 18)], 2.2, col=WING_G)
        ink(cr, [(8, y), (20, y - 18)], 2.2, col=WING_G)


def _drop(cr):
    cr.new_path()
    cr.move_to(0, -34)
    cr.curve_to(18, -6, 18, 16, 0, 20)
    cr.curve_to(-18, 16, -18, -6, 0, -34)
    leather(cr, (1.0, 1.0, 1.0), 4)


def _splat(cr):
    """A small white splat (pivot at its centre)."""
    pts = []
    for i in range(14):
        a = 2 * math.pi * i / 14
        r = 34 if i % 2 == 0 else 18 + 6 * (i % 3)
        pts.append((r * math.cos(a), 0.7 * r * math.sin(a)))
    _shape(cr, pts, (1.0, 1.0, 1.0), 4)


register("dv_feather", (-30, -250, 40, 20), _feather)
register("dv_drop", (-22, -38, 22, 24), _drop)
register("dv_splat", (-40, -30, 40, 30), _splat)


# ------------------------------------------------------------------ the housewife


def wife_head(cr, eyes="open"):
    """The housewife: her hair parted with sindoor, a bun with jasmine, a bindi, gold studs, a small nose ring.
    eyes: open | calm (lids lowered, serene) | smile | speak (open, the mouth a little open)."""
    face = [(-20, 6), (-26, -36), (-44, -80), (-50, -126), (-38, -168), (0, -188), (36, -176), (50, -148), (54, -126),
            (58, -116), (76, -96), (60, -88), (63, -78), (56, -70), (60, -62), (50, -48), (46, -36), (30, -26), (22, 6)]
    _shape(cr, face, WF_SKIN, 6)
    hair = [(-40, -170), (0, -192), (36, -180), (46, -160), (20, -166), (-10, -152), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    ink(cr, [(10, -190), (30, -178)], 4, col=RED)                                 # sindoor in the parting
    cr.new_path()
    cr.arc(-60, -120, 34, 0, 2 * math.pi)
    leather(cr, HAIR, 4)
    for i in range(8):
        a = 2 * math.pi * i / 8
        punch(cr, [(-60 + 21 * math.cos(a), -120 + 21 * math.sin(a))], 3.0)
    for i in range(6):                                                            # a few jasmine
        a = math.pi * (0.6 + 0.9 * i / 5)
        _flower(cr, -60 + 38 * math.cos(a), -120 + 38 * math.sin(a), 9, PALE, 5)
    cr.new_path()
    cr.arc(46, -146, 5.5, 0, 2 * math.pi)                                         # bindi
    cr.set_source_rgb(*RED)
    cr.fill()
    from puppet_core import almond_eye
    if eyes == "smile":
        ink(cr, [(14, -110), (30, -122), (46, -110)], 5)
        ink(cr, [(14, -132), (30, -138), (46, -132)], 3.5)
    else:
        almond_eye(cr, 30, -112, 32, 11, col=PALE)
        ink(cr, [(46, -112), (60, -120)], 3)
        ink(cr, [(14, -130), (30, -136), (46, -130)], 3.5)
        if eyes == "calm":                                                        # lids lowered: serene, sure
            cr.new_path()
            cr.move_to(13, -112)
            cr.curve_to(22, -124, 38, -124, 47, -110)
            cr.line_to(47, -116)
            cr.curve_to(38, -132, 22, -132, 13, -118)
            cr.close_path()
            cr.set_source_rgb(*WF_SKIN)
            cr.fill()
            ink(cr, [(13, -113), (30, -119), (47, -111)], 4)
    if eyes == "smile":
        ink(cr, [(54, -74), (60, -68), (64, -72)], 3, col=RED)
    elif eyes == "speak":
        cr.new_path()
        ell(cr, 59, -71, 6, 7)
        leather(cr, (0.42, 0.06, 0.06), 2.5)
    else:
        ink(cr, [(62, -74), (56, -70)], 3, col=RED)
    cr.new_path()                                                                 # nose ring
    cr.arc(66, -88, 7, 0, 2 * math.pi)
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(3)
    cr.stroke()
    _jewel(cr, -10, -70, 9, GOLD)


WIFE = woman("dv_wife", skin=WF_SKIN, skirt=WF_SARI, choli=WF_CHOLI, border=WF_PALLU, pallu_col=WF_PALLU, gem=RED,
             flower=PALE, hands=("open", "open"))
for _e in ("open", "calm", "smile", "speak"):
    register("dv_wife_head" + ("" if _e == "open" else "_" + _e), (-140, -250, 100, 30),
             (lambda e: lambda cr: wife_head(cr, e))(_e))


# ------------------------------------------------------------------ the husband


_HB_O = dict(skin=HB_SKIN, hair=False, moustache=True, tilak=False, earring=False)


def hus_head(cr, mood="tired"):
    """The husband: a white head-cloth wrapped round his head with the end hanging behind, a moustache.
    mood: tired (heavy lids, sweat) | smile."""
    tail = [(-50, -150), (-90, -120), (-104, -60), (-86, -56), (-70, -110), (-40, -130)]
    _shape(cr, tail, PALE, 4)
    A.face(cr, _HB_O, "hurt" if mood == "tired" else mood)
    wrap = [(-56, -120), (-60, -170), (-40, -206), (0, -222), (40, -212), (58, -180), (52, -150), (20, -160),
            (-20, -150), (-44, -116)]
    _shape(cr, wrap, PALE, 5)
    for k in range(3):
        ink(cr, [(-50, -140 - 20 * k), (0, -170 - 14 * k), (50, -164 - 12 * k)], 2.6, col=(0.70, 0.66, 0.58))
    holes_line(cr, [(-46, -128), (0, -150), (48, -150)], 14, 2.2)
    if mood == "tired":
        for k, (x, y) in enumerate(((60, -170), (70, -150))):
            cr.new_path()
            cr.move_to(x, y - 10)
            cr.curve_to(x + 7, y, x + 7, y + 6, x, y + 8)
            cr.curve_to(x - 7, y + 6, x - 7, y, x, y - 10)
            leather(cr, (0.80, 0.92, 1.0), 2)


_HB = dict(skin=HB_SKIN, bulk=0.98, dhoti=HB_DHOTI, border=BROWN, pleat=HB_DHOTI, sash=HB_TOWEL, neck=BROWN)
HUS = man("dv_hus", crown="tiara", halo=False, hair=False, earring=False, tilak=False, moustache=True,
          hands=("open", "fist"), **_HB)
for _m in ("tired", "smile", "calm"):
    register("dv_hus_head" + ("" if _m == "tired" else "_" + _m), (-130, -250, 110, 30),
             (lambda m: lambda cr: hus_head(cr, m))(_m))
register("dv_hus_body_sit", (-200, -330, 140, 80), _sit_body(_HB))
register("dv_hus_seat", (-110, -60, 280, 110), lambda cr: _cross_seat(cr, HB_DHOTI, BROWN, HB_SKIN))


def _hoe(cr):
    """A farmer's hoe (grip at 0, 0): a long wooden handle, an iron blade at the top."""
    band(cr, [(0, 260), (0, -420)], 18, WOOD, holes=False)
    _shape(cr, [(-8, -440), (90, -430), (120, -380), (100, -370), (70, -404), (-8, -400)], (0.46, 0.46, 0.50), 4,
           smooth=False)
    punch(cr, [(20, -420)], 4)


register("dv_hoe", (-30, -450, 130, 270), _hoe)


# ------------------------------------------------------------------ the butcher


_VY_O = dict(skin=VY_SKIN, hair=False, moustache=True, tilak=False, earring=False)


def vy_head(cr, mood="calm"):
    """The butcher: a maroon turban with its end tucked behind, a moustache, a white tilak with a red dot.
    mood: calm | smile | speak."""
    A.face(cr, _VY_O, "smile" if mood in ("smile", "speak") else "calm")
    if mood == "speak":
        cr.new_path()
        ell(cr, 62, -66, 7, 6)
        leather(cr, (0.40, 0.06, 0.06), 2.5)
    tb = [(-58, -118), (-64, -170), (-46, -214), (0, -232), (44, -220), (62, -186), (56, -150), (24, -164),
          (-20, -152), (-44, -114)]
    _shape(cr, tb, VY_TURBAN, 5)
    for k in range(3):
        ink(cr, [(-56, -132 - 22 * k), (0, -166 - 16 * k), (54, -160 - 14 * k)], 3, col=(0.40, 0.08, 0.06))
    _shape(cr, [(-52, -130), (-80, -100), (-74, -70), (-60, -94), (-44, -120)], VY_TURBAN, 4)
    holes_line(cr, [(-50, -120), (0, -152), (52, -146)], 14, 2.4)
    _jewel(cr, 10, -224, 9, GOLD)
    ink(cr, [(50, -150), (52, -136)], 5, col=PALE)                                 # tilak: a white line, a red dot
    cr.new_path()
    cr.arc(52, -130, 4, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()


_VY = dict(skin=VY_SKIN, bulk=1.04, dhoti=VY_DHOTI, border=DGREEN, pleat=VY_DHOTI, sash=DGREEN, neck=BROWN)


def vy_body(cr, clip=None):
    """man_body with a plain brown leather apron tied over the dhoti, hanging to the knee in front."""
    if clip:
        cr.save()
        cr.rectangle(-400, -600, 800, 600 + clip)
        cr.clip()
    man_body(cr, _VY)
    b = _VY["bulk"]
    ap = [(-6, -54), (64 * b, -58), (92 * b, 30), (106 * b, 180), (90 * b, 236), (40, 246), (6, 236), (-4, 60)]
    _shape(cr, ap, APRON, 5)
    band(cr, [(0, -40), (70 * b, -44)], 10, APRON2, holes=False)
    holes_line(cr, [(10, -26), (12, 120), (24, 220), (84 * b, 224), (96 * b, 120), (80 * b, -30)], 15, 2.4)
    ink(cr, [(-20, -40), (-56, -20), (-70, 20)], 4, col=APRON2)                    # the apron string tied behind
    if clip:
        cr.restore()


VY = man("dv_vy", crown="tiara", halo=False, hair=False, earring=False, tilak=False, moustache=True,
         hands=("open", "open"), **_VY)
register("dv_vy_body", (-200, -330, 160, 300), vy_body)
for _m in ("calm", "smile", "speak"):
    register("dv_vy_head" + ("" if _m == "calm" else "_" + _m), (-130, -260, 110, 30),
             (lambda m: lambda cr: vy_head(cr, m))(_m))
register("dv_vy_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, VY_SKIN, VY_DHOTI, DGREEN, 1.04))


# ------------------------------------------------------------------ the old parents


def old_man_head(cr, skin, mood="smile", rishi=False):
    """An old man: white hair behind, a white top-knot (with rudraksha and ash lines for the old sage), a white beard
    and moustache, thick white brows, wrinkles. mood: smile | calm | shut (eyes closed, sad) | shut_smile."""
    hp = [(-30, -176), (-62, -146), (-84, -80), (-88, 10), (-70, 70), (-50, 40), (-40, -30), (-24, -100)]
    _shape(cr, hp, ASH, 5)
    for k in range(3):
        ink(cr, [(-48 - 8 * k, -140), (-70 - 4 * k, -40), (-62 - 2 * k, 40)], 2.4, col=ASH2)
    base = {"shut": "shame", "shut_smile": "calm"}.get(mood, mood)
    A.face(cr, dict(skin=skin, hair=False, moustache=False, tilak=False, earring=False), base)
    if mood == "shut_smile":
        M._sleep_eye(cr, skin)
        ink(cr, [(56, -70), (62, -64), (70, -68)], 3.5)
    _old_wrinkles(cr)
    long_ = 120 if rishi else 50
    bp = [(62, -50), (64, -22), (58, 20), (42, long_), (22, long_ - 40), (2, 10), (6, -40), (30, -54)]
    _shape(cr, bp, ASH, 4)
    for k in range(3):
        ink(cr, [(48 - 10 * k, -40), (42 - 12 * k, 10), (36 - 10 * k, long_ - 30)], 2.2, col=ASH2)
    m = [(66, -82), (46, -88), (24, -90), (12, -80), (30, -80), (52, -78), (68, -78)]
    _shape(cr, m, ASH, 3)
    if mood in ("smile", "shut_smile"):
        ink(cr, [(48, -68), (58, -62), (68, -66)], 3.5)
    by = -150 if mood != "shut" else -146
    ink(cr, [(12, by + 8), (34, by), (58, by + 8)], 7, col=ASH)
    cap = [(-56, -116), (-60, -160), (-40, -192), (0, -204), (36, -194), (48, -176), (20, -178), (-12, -172),
           (-34, -150), (-42, -116)]
    _shape(cr, cap, ASH, 4)
    cr.new_path()
    ell(cr, -24, -214, 30, 22, -0.2)
    leather(cr, ASH, 4)
    ink(cr, [(-48, -214), (-24, -224), (0, -216)], 2.2, col=ASH2)
    if rishi:
        for i in range(6):
            cr.new_path()
            cr.arc(-50 + 13 * i, -196 + 2 * math.sin(i), 5.5, 0, 2 * math.pi)
            leather(cr, BROWN, 2)
        _ash_lines(cr, 6, 46, -172)
    else:                                                                         # a sandal-paste U tilak
        ink(cr, [(44, -168), (48, -150), (56, -150), (58, -166)], 3.5, col=PALE)


def old_woman_head(cr, skin, mood="smile", veil=None):
    """An old woman: grey-white hair in a bun with a flower (or her sari over her head: veil = its colour), wrinkles,
    a bindi, gold studs. mood: smile | open | shut (eyes closed, sad) | shut_smile."""
    if veil:
        vp = [(-40, -176), (10, -200), (44, -186), (52, -164), (30, -170), (-10, -160), (-34, -120), (-60, -40),
              (-96, 40), (-110, 20), (-96, -60), (-76, -130)]
        _shape(cr, vp, veil, 5)
        dots_in(cr, lambda: spath(cr, vp), 20, 2.6)
    face = [(-20, 6), (-26, -36), (-44, -80), (-50, -126), (-38, -168), (0, -188), (36, -176), (50, -148), (54, -126),
            (58, -116), (74, -96), (60, -88), (62, -78), (56, -70), (58, -62), (50, -48), (44, -36), (30, -26), (22, 6)]
    _shape(cr, face, skin, 6)
    if veil:
        band(cr, [(-30, -176), (12, -196), (48, -176)], 14, SAFFRON, spacing=11, hole_r=2.2)
    else:
        hair = [(-40, -170), (0, -192), (36, -180), (46, -160), (20, -166), (-10, -152), (-30, -110), (-44, -90),
                (-52, -128)]
        _shape(cr, hair, ASH, 4)
        cr.new_path()
        cr.arc(-60, -124, 32, 0, 2 * math.pi)
        leather(cr, ASH, 4)
        ink(cr, [(-82, -128), (-60, -112), (-40, -128)], 2.4, col=ASH2)
        _flower(cr, -82, -150, 12, RED, 6)
    from puppet_core import almond_eye
    if mood in ("smile", "shut_smile"):
        if mood == "smile":
            ink(cr, [(14, -110), (30, -122), (46, -110)], 5)
        else:
            ink(cr, [(14, -114), (30, -106), (46, -114)], 4.5)
            for x in (22, 30, 38):
                ink(cr, [(x, -109), (x - 2, -101)], 2.2)
        ink(cr, [(14, -132), (30, -138), (46, -132)], 3.5, col=ASH2)
        ink(cr, [(52, -74), (58, -68), (64, -72)], 3, col=(0.62, 0.20, 0.16))
    elif mood == "shut":
        ink(cr, [(14, -114), (30, -106), (46, -114)], 4.5)
        for x in (22, 30, 38):
            ink(cr, [(x, -109), (x - 2, -101)], 2.2)
        ink(cr, [(12, -128), (30, -132), (48, -142)], 3.5, col=ASH2)
        ink(cr, [(62, -72), (54, -68)], 3, col=(0.62, 0.20, 0.16))
    else:
        almond_eye(cr, 30, -112, 30, 10, col=PALE)
        ink(cr, [(14, -130), (30, -136), (46, -130)], 3.5, col=ASH2)
        ink(cr, [(62, -74), (56, -70)], 3, col=(0.62, 0.20, 0.16))
    ink(cr, [(36, -96), (44, -82)], 2.0)
    ink(cr, [(20, -160), (36, -162)], 2.0)
    cr.new_path()
    cr.arc(44, -148, 4.5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    _jewel(cr, -10, -70, 8, GOLD)


def wbody_sit(o):
    """A woman seated on a bench (hip at 0, 0; soles at +BENCH_H): the sari over her lap and down to her feet, then
    woman_body's torso, blouse and pallu."""
    def fn(cr):
        shin = [(140, 30), (226, 30), (240, 150), (252, 258), (126, 258), (132, 150)]
        _shape(cr, shin, o["skirt"], 5)
        dots_in(cr, lambda: spath(cr, shin), 22, 3.0, shape="d")
        band(cr, [(124, 248), (254, 248)], 18, o.get("border", GOLD), spacing=11, hole_r=2.2)
        _shape(cr, [(234, 254), (276, 258), (280, 270), (230, 272)], o["skin"], 4)
        cr.save()
        cr.rectangle(-400, -600, 800, 640)
        cr.clip()
        woman_body(cr, o)
        cr.restore()
        lap = [(-100, -34), (40, -46), (200, -30), (230, 20), (214, 66), (60, 70), (-90, 60), (-112, 20)]
        _shape(cr, lap, o["skirt"], 5)
        dots_in(cr, lambda: spath(cr, lap), 22, 3.0, shape="d")
        for x0, x1 in ((40, 200), (60, 210)):
            ink(cr, [(x0, -20 + (x0 - 40) * 0.2), (x1, 10)], 2.6, smooth=False)
        band(cr, [(204, -26), (230, 20), (214, 62)], 14, o.get("border", GOLD), spacing=11, hole_r=2.2)
        band(cr, [(-40, -36), (0, -42), (40, -40)], 16, o.get("border", GOLD), spacing=11, hole_r=2.2)
        rivet(cr, 0, 0, 8)
    return fn


_BF = dict(skin=BF_SKIN, bulk=0.92, dhoti=PALE, border=BF_SHAWL, pleat=PALE, sash=BF_SHAWL, neck=BROWN,
           robe=BF_SHAWL, beads=False)
BFA = man("dv_bfa", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"), **_BF)
for _m in ("smile", "calm"):
    register("dv_bfa_head" + ("" if _m == "smile" else "_" + _m), (-130, -250, 110, 80),
             (lambda m: lambda cr: old_man_head(cr, BF_SKIN, m))(_m))
register("dv_bfa_body_sit", (-200, -330, 140, 80), _sit_body(_BF))
register("dv_bfa_seat", (-100, -60, 300, 290), lambda cr: M.seat_legs(cr, BF_SKIN, PALE, BF_SHAWL, 0.92))

_BM = dict(skin=BM_SKIN, skirt=BM_SARI, choli=PALE, border=GOLD, pallu_col=(0.62, 0.18, 0.24), gem=GREEN)
BMO = woman("dv_bmo", hands=("open", "open"), **_BM)
for _m in ("smile", "open"):
    register("dv_bmo_head" + ("" if _m == "smile" else "_" + _m), (-140, -250, 100, 30),
             (lambda m: lambda cr: old_woman_head(cr, BM_SKIN, m))(_m))
register("dv_bmo_body_sit", (-150, -310, 290, 290), wbody_sit(_BM))

_KF = dict(skin=KF_SKIN, bulk=0.88, dhoti=KF_ROBE, border=SAFFRON, pleat=KF_ROBE, sash=OCHRE, neck=BROWN,
           robe=KF_ROBE, beads=True)
KFA = man("dv_kfa", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"), **_KF)
for _m in ("shut", "shut_smile"):
    register("dv_kfa_head" + ("" if _m == "shut" else "_smile"), (-130, -260, 110, 160),
             (lambda m: lambda cr: old_man_head(cr, KF_SKIN, m, rishi=True))(_m))
register("dv_kfa_body_sit", (-200, -330, 140, 80), _sit_body(_KF))
register("dv_kfa_seat", (-100, -60, 300, 290), lambda cr: M.seat_legs(cr, KF_SKIN, KF_ROBE, SAFFRON, 0.88))

_KM = dict(skin=KM_SKIN, skirt=KM_SARI, choli=(0.98, 0.78, 0.42), border=SAFFRON, pallu_col=KM_SARI, gem=RED)
KMO = woman("dv_kmo", hands=("open", "open"), **_KM)
for _m in ("shut", "shut_smile"):
    register("dv_kmo_head" + ("" if _m == "shut" else "_smile"), (-140, -250, 100, 50),
             (lambda m: lambda cr: old_woman_head(cr, KM_SKIN, m, veil=KM_SARI))(_m))
register("dv_kmo_body_sit", (-150, -310, 290, 290), wbody_sit(_KM))


# ------------------------------------------------------------------ the tree, the house, the room


def _tree(cr):
    """A big shady tree (pivot at the trunk's foot) with one long, bare branch reaching left (the crane perches on
    it at about (-380, -846)) and a full canopy above."""
    trunk = [(-110, 0), (110, 0), (70, -60), (56, -420), (60, -700), (120, -900), (90, -920), (30, -800),
             (10, -1000), (-20, -1000), (-26, -760), (-60, -740), (-50, -440), (-70, -60)]
    _shape(cr, trunk, BROWN, 7, smooth=False)
    for k in range(4):
        ink(cr, [(-30 + 16 * k, -10), (-20 + 12 * k, -300), (-10 + 8 * k, -620)], 3)
    holes_line(cr, [(0, -40), (8, -380), (0, -700)], 26, 3.4)
    for x in (-90, 90):                                                           # roots
        _shape(cr, [(x * 0.4, -20), (x * 1.5, 8), (x * 1.6, 0), (x * 0.6, -40)], BROWN, 5)
    br = [(-40, -760), (-200, -812), (-400, -846), (-640, -852), (-730, -862), (-700, -880), (-400, -880),
          (-200, -852), (-30, -800)]
    _shape(cr, br, BROWN, 7)
    holes_line(cr, [(-80, -790), (-320, -850), (-660, -864)], 22, 2.6)
    _shape(cr, [(-300, -860), (-350, -950), (-330, -960), (-280, -868)], BROWN, 5)   # a twig
    _shape(cr, [(-372, -956), (-330, -980), (-300, -958), (-336, -944)], GREEN, 4)
    blobs = [(0, -1150, 330, 210), (-200, -1090, 190, 140), (250, -1050, 220, 160), (-120, -1290, 200, 130),
             (150, -1300, 210, 130), (380, -960, 130, 100), (-30, -1000, 180, 110)]
    for i, (x, y, rx, ry) in enumerate(blobs):
        cr.new_path()
        ell(cr, x, y, rx, ry)
        leather(cr, GREEN if i % 2 == 0 else DGREEN, 7)
    rng = random.Random(12)
    for _ in range(90):                                                           # leaf-shaped cut-outs
        x, y = rng.uniform(-420, 520), rng.uniform(-1420, -930)
        if ((x - 20) / 470) ** 2 + ((y + 1150) / 260) ** 2 > 1.0:
            continue
        a = rng.uniform(-1.2, 1.2)
        Ln = rng.uniform(22, 34)

        def lf(x=x, y=y, a=a, Ln=Ln):
            cr.save()
            cr.translate(x, y)
            cr.rotate(a)
            cr.move_to(-Ln, 0)
            cr.curve_to(-Ln / 2, -Ln / 3, Ln / 2, -Ln / 3, Ln, 0)
            cr.curve_to(Ln / 2, Ln / 3, -Ln / 2, Ln / 3, -Ln, 0)
            cr.restore()
        cut(cr, lf)


register("dv_tree", (-750, -1460, 560, 20), _tree)


def _house(cr):
    """A village house front (pivot at the bottom centre): a mud wall, a tiled roof, a lit doorway (cut through) at
    x = +190 with a wooden frame and a mango-leaf toran, a small barred window, a doorstep with rangoli dots."""
    wall = [(-480, 0), (480, 0), (480, -760), (-480, -760)]
    _shape(cr, wall, MUD, 6, smooth=False)
    dots_in(cr, lambda: poly(cr, [(-470, -60), (470, -60), (470, -740), (-470, -740)]), 34, 2.6)
    _shape(cr, [(-500, 0), (500, 0), (500, -60), (-500, -60)], (0.66, 0.42, 0.22), 5, smooth=False)
    holes_line(cr, [(-490, -30), (490, -30)], 20, 4, smooth=False)
    roof = [(-600, -720), (600, -720), (470, -1000), (-470, -1000)]
    _shape(cr, roof, TILE, 7, smooth=False)
    for k in range(5):
        y = -760 - 50 * k
        ink(cr, [(-580 + 26 * k, y), (580 - 26 * k, y)], 3, smooth=False)
    for i in range(24):
        x = -560 + 48 * i
        cr.new_path()
        cr.arc(x, -724, 24, 0, math.pi)
        cr.set_source_rgb(*INK)
        cr.set_line_width(3)
        cr.stroke()
    holes_line(cr, [(-440, -980), (440, -980)], 26, 3.2, smooth=False)
    dx = 190
    fr = [(dx - 190, -40), (dx - 190, -700), (dx + 190, -700), (dx + 190, -40)]
    _shape(cr, fr, WOOD, 6, smooth=False)
    dots_in(cr, lambda: poly(cr, fr), 26, 3.0, shape="d")
    cut(cr, lambda: poly(cr, [(dx - 140, -40), (dx - 140, -600), (dx - 90, -650), (dx + 90, -650), (dx + 140, -600),
                              (dx + 140, -40)]))
    ink(cr, [(dx - 140, -40), (dx - 140, -600), (dx - 90, -650), (dx + 90, -650), (dx + 140, -600), (dx + 140, -40)], 6,
        smooth=False)
    for i in range(9):                                                            # mango-leaf toran
        x = dx - 160 + 40 * i
        _shape(cr, [(x - 10, -690), (x + 10, -690), (x + 7, -646), (x, -626), (x - 7, -646)], GREEN, 2.6)
    for k in range(3):                                                            # painted bands on the wall
        band(cr, [(-470, -300 - 150 * k), (-30, -300 - 150 * k)], 10, (0.96, 0.86, 0.66), holes=False, lw=2.5)
    for i in range(7):                                                            # rangoli dots by the door
        punch(cr, [(dx - 150 + 50 * i, -14)], 5)


register("dv_house", (-610, -1010, 610, 10), _house)
DOOR_X = 190.0                        # the doorway's centre (house units)


def _wall(cr):
    """The edge of the house (pivot at its foot): a thick mud wall seen end-on with a wooden door post."""
    w = [(-70, 0), (70, 0), (70, -1150), (-70, -1150)]
    _shape(cr, w, MUD, 6, smooth=False)
    dots_in(cr, lambda: poly(cr, w), 30, 2.6)
    _shape(cr, [(40, 0), (90, 0), (90, -1150), (40, -1150)], WOOD, 5, smooth=False)
    for y in range(-1100, 0, 120):
        band(cr, [(42, y), (88, y)], 10, GOLD, holes=False, lw=3)
    _shape(cr, [(-110, -1150), (130, -1150), (130, -1200), (-110, -1200)], TILE, 5, smooth=False)


register("dv_wall", (-120, -1210, 140, 10), _wall)


def _room(cr):
    """A room's back wall (pivot at the bottom centre): plastered mud, an arched niche with a lamp, a shelf of pots,
    a rope sling with a pot, a barred window."""
    w = [(-640, 0), (640, 0), (640, -1100), (-640, -1100)]
    _shape(cr, w, MUD2, 6, smooth=False)
    dots_in(cr, lambda: poly(cr, w), 40, 2.4)
    _shape(cr, [(-640, 0), (640, 0), (640, -80), (-640, -80)], (0.80, 0.56, 0.32), 5, smooth=False)
    holes_line(cr, [(-630, -40), (630, -40)], 26, 3.4, smooth=False)
    niche = [(-470, -480), (-470, -700), (-420, -760), (-320, -760), (-270, -700), (-270, -480)]
    _shape(cr, niche, (0.50, 0.30, 0.16), 5, smooth=False)
    _shape(cr, [(-410, -480), (-330, -480), (-350, -510), (-390, -510)], BRASS, 3, smooth=False)
    _shape(cr, [(-376, -514), (-364, -514), (-370, -560)], SAFFRON, 2, smooth=False)
    _shape(cr, [(80, -620), (560, -620), (560, -596), (80, -596)], WOOD, 4, smooth=False)
    for x, r, col in ((150, 50, (0.74, 0.40, 0.20)), (270, 60, BRASS), (400, 46, (0.74, 0.40, 0.20)),
                      (500, 38, BRASS)):
        cr.new_path()
        ell(cr, x, -620 - r * 0.9, r, r * 0.9)
        leather(cr, col, 4)
        _shape(cr, [(x - r * 0.4, -620 - r * 1.7), (x + r * 0.4, -620 - r * 1.7), (x + r * 0.3, -620 - r * 1.95),
                    (x - r * 0.3, -620 - r * 1.95)], col, 3, smooth=False)
    win = [(-120, -900), (40, -900), (40, -720), (-120, -720)]
    _shape(cr, win, WOOD, 5, smooth=False)
    for i in range(3):
        x = -100 + 46 * i
        cut(cr, lambda x=x: poly(cr, [(x, -880), (x + 32, -880), (x + 32, -740), (x, -740)]))
    for sx in (-1, 1):                                                            # a rope sling with a pot
        ink(cr, [(480, -1100), (480 + sx * 50, -880)], 3, col=(0.56, 0.42, 0.24))
    cr.new_path()
    ell(cr, 480, -860, 56, 46)
    leather(cr, (0.74, 0.40, 0.20), 4)


register("dv_room", (-650, -1110, 650, 10), _room)


# ------------------------------------------------------------------ Mithila: the market


def _hang(cr, x, y, k):
    """A plain hanging shape on a hook (simple, no detail)."""
    ink(cr, [(x, y - 70), (x, y - 40)], 4, smooth=False, col=(0.40, 0.40, 0.44))
    ink(cr, [(x, y - 40), (x + 10, y - 30), (x, y - 20)], 4, col=(0.40, 0.40, 0.44))
    L_ = 150 + 30 * (k % 2)
    pts = [(x, y - 24), (x + 40, y), (x + 50, y + L_ * 0.5), (x + 30, y + L_), (x - 28, y + L_ * 0.95),
           (x - 46, y + L_ * 0.45), (x - 36, y)]
    _shape(cr, pts, HANG, 4)
    holes_line(cr, [(x - 6, y + 24), (x + 4, y + L_ * 0.8)], 18, 3.0)


def _stall_back(cr):
    """The butcher's stall (pivot at the bottom centre), the parts behind him: two posts, a striped awning with a
    scalloped edge, a rail with plain hanging shapes."""
    for x in (-430, 430):
        _shape(cr, [(x - 22, 0), (x + 22, 0), (x + 18, -1060), (x - 18, -1060)], WOOD, 5, smooth=False)
    aw = [(-500, -1040), (500, -1040), (540, -900), (-540, -900)]
    cr.new_path()
    poly(cr, aw)
    leather(cr, (1.0, 0.92, 0.74), 6)
    for i in range(9):
        x0 = -500 + i * 1000 / 9
        if i % 2 == 0:
            _shape(cr, [(x0, -1040), (x0 + 1000 / 9, -1040), (x0 + 1000 / 9 * 1.04 + 4, -900),
                        (x0 * 1.08 - 4, -900)], SAFFRON, 3, smooth=False)
    RU_sc = 60
    for i in range(18):
        x = -540 + RU_sc * i + 30
        cr.new_path()
        cr.arc(x, -900, 30, 0, math.pi)
        leather(cr, RED if i % 2 else SAFFRON, 3)
    band(cr, [(-420, -780), (420, -780)], 16, WOOD, holes=False)
    for i, x in enumerate((-350, -250, 250, 350)):
        _hang(cr, x, -760, i)


def _counter(cr):
    """The stall's front counter (pivot at the bottom centre): a wooden table with a carved front, a round chopping
    block (a plain wooden stump) and a weighing scale."""
    top = [(-470, -420), (470, -420), (470, -380), (-470, -380)]
    front = [(-450, -380), (450, -380), (440, 0), (-440, 0)]
    _shape(cr, front, (0.66, 0.40, 0.18), 6, smooth=False)
    dots_in(cr, lambda: poly(cr, [(-420, -350), (420, -350), (410, -30), (-410, -30)]), 28, 3.4, shape="d")
    for x in (-150, 150):
        ink(cr, [(x, -370), (x, -10)], 4, smooth=False)
    _shape(cr, top, WOOD, 5, smooth=False)
    cr.new_path()                                                                 # the chopping block
    poly(cr, [(-330, -420), (-330, -520), (-130, -520), (-130, -420)])
    leather(cr, (0.78, 0.56, 0.30), 5)
    cr.new_path()
    ell(cr, -230, -520, 100, 22)
    leather(cr, (0.90, 0.72, 0.44), 4)
    for r in (70, 40, 14):
        cr.new_path()
        ell(cr, -230, -520, r, r * 0.22)
        cr.set_source_rgb(0.62, 0.42, 0.20)
        cr.set_line_width(2.4)
        cr.stroke()
    ink(cr, [(250, -420), (250, -700)], 6, smooth=False, col=WOOD)               # the weighing scale
    ink(cr, [(150, -690), (350, -690)], 6, smooth=False, col=BRASS)
    for x in (150, 350):
        ink(cr, [(x, -690), (x - 40, -580)], 2, smooth=False)
        ink(cr, [(x, -690), (x + 40, -580)], 2, smooth=False)
        _shape(cr, [(x - 50, -580), (x + 50, -580), (x + 30, -556), (x - 30, -556)], BRASS, 3, smooth=False)


register("dv_stall_back", (-560, -1070, 560, 10), _stall_back)
register("dv_counter", (-480, -710, 480, 10), _counter)


def _basket(cr):
    """A basket stall: a woven basket heaped with round fruits and gourds (pivot at the bottom centre)."""
    rng = random.Random(5)
    for i in range(14):
        x, y = rng.uniform(-170, 170), rng.uniform(-230, -150) - 30 * math.cos(i)
        col = (GREEN, (1.0, 0.56, 0.16), GOLD, (0.86, 0.24, 0.16))[i % 4]
        cr.new_path()
        cr.arc(x, y, rng.uniform(26, 36), 0, 2 * math.pi)
        leather(cr, col, 3.5)
    bk = [(-210, -170), (210, -170), (170, 0), (-170, 0)]
    _shape(cr, bk, (0.86, 0.66, 0.34), 5, smooth=False)
    for k in range(4):
        ink(cr, [(-200 + 10 * k, -140 + 36 * k), (200 - 10 * k, -140 + 36 * k)], 2.4, smooth=False,
            col=(0.60, 0.40, 0.18))
    holes_line(cr, [(-190, -160), (190, -160)], 18, 3, smooth=False)


register("dv_basket", (-220, -280, 220, 10), _basket)


def _city(cr):
    """The skyline of Mithila (pivot at the bottom centre): a gateway, houses, domes and flags."""
    rng = random.Random(8)
    x = -700
    i = 0
    while x < 700:
        w = rng.uniform(110, 190)
        h = rng.uniform(220, 380)
        col = (MUD, (0.94, 0.80, 0.56), (0.82, 0.56, 0.34))[i % 3]
        _shape(cr, [(x, 0), (x + w, 0), (x + w, -h), (x, -h)], col, 5, smooth=False)
        if i % 2 == 0:
            cr.new_path()
            ell(cr, x + w / 2, -h, w * 0.36, w * 0.4)
            leather(cr, GOLD if i % 4 == 0 else (0.94, 0.88, 0.76), 4)
            ink(cr, [(x + w / 2, -h - w * 0.4), (x + w / 2, -h - w * 0.4 - 60)], 3, smooth=False)
            _shape(cr, [(x + w / 2, -h - w * 0.4 - 60), (x + w / 2 + 44, -h - w * 0.4 - 48),
                        (x + w / 2, -h - w * 0.4 - 36)], RED, 2.5, smooth=False)
        else:
            _shape(cr, [(x - 10, -h), (x + w + 10, -h), (x + w / 2, -h - 80)], TILE, 4, smooth=False)
        for k in range(2):
            cut(cr, lambda x=x, w=w, h=h, k=k: poly(cr, [(x + w * (0.22 + 0.36 * k), -h * 0.7),
                                                          (x + w * (0.36 + 0.36 * k), -h * 0.7),
                                                          (x + w * (0.36 + 0.36 * k), -h * 0.5),
                                                          (x + w * (0.22 + 0.36 * k), -h * 0.5)]))
        x += w + rng.uniform(-10, 20)
        i += 1
    gate = [(-150, 0), (150, 0), (150, -460), (110, -540), (0, -580), (-110, -540), (-150, -460)]
    _shape(cr, gate, OCHRE, 6, smooth=False, holes=(12, 16, 3.0))
    cut(cr, lambda: poly(cr, [(-80, 0), (-80, -300), (0, -380), (80, -300), (80, 0)]))
    ink(cr, [(-80, 0), (-80, -300), (0, -380), (80, -300), (80, 0)], 5, smooth=False)


register("dv_city", (-720, -720, 720, 10), _city)


# ------------------------------------------------------------------ seats, food, water


def _bench(cr):
    """A long low wooden bench (pivot at the bottom centre; its top at y = -(BENCH_H - 60))."""
    top = BENCH_H - 60
    for x in (-380, -130, 130, 380):
        _shape(cr, [(x - 30, -top + 40), (x + 30, -top + 40), (x + 24, 0), (x - 24, 0)], (0.48, 0.28, 0.12), 6,
               smooth=False)
    _shape(cr, [(-430, -top), (430, -top), (440, -top + 60), (-440, -top + 60)], WOOD, 7, smooth=False,
           holes=(12, 16, 3.0))
    band(cr, [(-420, -top + 30), (420, -top + 30)], 12, GOLD, holes=False, lw=3)


def _charpai(cr):
    """A rope cot (pivot at the bottom centre; its top at y = -(BENCH_H - 60)): a woven top, four legs."""
    top = BENCH_H - 60
    for x in (-400, 400):
        _shape(cr, [(x - 32, -top + 30), (x + 32, -top + 30), (x + 24, 0), (x - 24, 0)], WOOD, 6, smooth=False)
        cr.new_path()
        ell(cr, x, -top / 2, 38, 22)
        leather(cr, WOOD, 4)
    _shape(cr, [(-440, -top), (440, -top), (440, -top + 50), (-440, -top + 50)], (0.86, 0.70, 0.40), 7, smooth=False)
    for i in range(42):
        x = -430 + 21 * i
        ink(cr, [(x, -top + 4), (x + 14, -top + 46)], 2.6, smooth=False, col=(0.56, 0.40, 0.18))
    for x in (-440, 440):
        _shape(cr, [(x - 14, -top - 6), (x + 14, -top - 6), (x + 14, -top + 56), (x - 14, -top + 56)], WOOD, 4,
               smooth=False)


register("dv_bench", (-450, -(BENCH_H - 50), 450, 10), _bench)
register("dv_charpai", (-460, -(BENCH_H - 50), 460, 10), _charpai)


def _plate(cr):
    """A banana leaf of food (pivot at its middle): a heap of rice, two small bowls."""
    leaf = [(-170, 6), (-120, -14), (60, -16), (170, -8), (180, 6), (120, 14), (-120, 16)]
    _shape(cr, leaf, BANANA, 4)
    ink(cr, [(-160, 4), (170, 2)], 2.4, col=DGREEN)
    cr.new_path()
    ell(cr, -30, -30, 64, 34)
    leather(cr, RICE, 4)
    punch(cr, [(-50, -40), (-20, -48), (0, -30), (-40, -22)], 2.6)
    for x, col in ((80, GOLD), (130, GREEN)):
        _shape(cr, [(x - 26, -36), (x + 26, -36), (x + 18, -8), (x - 18, -8)], BRASS, 3, smooth=False)
        cr.new_path()
        ell(cr, x, -36, 26, 7)
        leather(cr, col, 2.5)


register("dv_plate", (-185, -70, 190, 24), _plate)


def _basin(cr):
    """A wide brass basin with water (pivot at the bottom centre)."""
    _shape(cr, [(-150, -70), (150, -70), (120, -10), (60, 0), (-60, 0), (-120, -10)], BRASS, 5)
    cr.new_path()
    ell(cr, 0, -70, 150, 22)
    leather(cr, WATER, 4)
    band(cr, [(-140, -54), (0, -44), (140, -54)], 10, RED, spacing=10, hole_r=2.0)


register("dv_basin", (-160, -100, 160, 8), _basin)
