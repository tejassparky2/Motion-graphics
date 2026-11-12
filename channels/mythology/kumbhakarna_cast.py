"""The leather cast and props for the Kumbhakarna reel (videos/kumbhakarna.py), in the Togalu Gombeyaata style of the
Jarasandha, Ravana, Kaikeyi, Lakshman Rekha, Mandhata, Ruru, Dharmavyadha and Shani-Ganesha reels (puppet_cast,
ravana_cast, kaikeyi_cast, lrekha_cast, mandhata_cast, ruru_cast, dharmavyadha_cast, shani_cast): profile figures with
big eyes, perforated garments and jointed limbs. Traditional leather puppets, modelled on no actor and no film. Every
sprite name starts with "kb_".

Cast (one look each, kept the same through the video):
  KUMBHAKARNA  the giant rakshasa, drawn far bigger than everyone else: dark olive-bronze skin, a great round belly
               over a deep-red dhoti with a gold border, wild flame-like black hair, a gold kirita with a red flare,
               round fierce eyes with a red ring, a heavy brow, a big nose, a curled moustache, two ivory tusks rising
               from the lower jaw, big gold kundala rings. Fierce, but a little comic when sleepy. Faces: open, daze
               (heavy, half-shut lids), sleep, snore (shut, the jaw a little open), shock, angry, speak (dazed, the
               mouth open: the words are not his), hungry (open-mouthed). His jaw is a separate jointed piece, so in
               the close-ups (kb_cu_*: the same head, larger, with finer lines) the mouth opens and Saraswati can sit
               on his tongue.
  SARASWATI    graceful: fair skin, a white sari with a gold border, a saffron-gold blouse, a gold crown with pearls in
               front of a ring of pale rays, jasmine in her hair; her veena (kb_veena) and her white swan (kb_swan).
               Standing, or seated cross-legged (kb_saras_body_sit + kb_saras_seat), which is also how she sits, tiny
               and glowing, on Kumbhakarna's tongue. Faces: open, smile, speak.
  RAVANA       ravana_cast.RAVANA (the ten-headed puppet). BRAHMA: six_cast_c.BRAHMA (three of his four faces showing,
               white beards, on his lotus). The gods: shani_cast.DEVA (silhouettes with halos). RAMA: kaikeyi_cast.RAMA.
               The elephants: six_cast_b's caparisoned elephant; the drummers: jayadratha_cast's soldier, in silhouette.
Props: the whole world (kb_world: a leather globe with sea, lands, trees and houses), a big dhol drum (kb_drum) and its
stick, a bolster pillow; the palm-leaf book, plaques, speech cloud, cot, lotus, trees, fire and ground come from the
earlier casts.

Every sprite is drawn once in design units and cached by puppet_core; rigs come from puppet_cast.man() / woman().
"""
import math

import arjuna_cast  # noqa: F401  (the cot)
import kaikeyi_cast as K  # noqa: F401  (Rama)
import lrekha_cast as LR  # noqa: F401  (palm-leaf book boards and leaves, speech cloud)
import mandhata_cast as M
import ravana_cast as R
import shani_cast as S
import six_cast_b  # noqa: F401  (the elephant)
import six_cast_c as C6  # noqa: F401  (Brahma, his Veda and seat)
from puppet_cast import HAIR, _flower, _jewel, _shape, man, woman, woman_body
from puppet_core import (GOLD, GREEN, INK, PALE, RED, band, dots_in, ell, holes_line, ink, leather,
                         perforate, poly, punch, register, rivet, spath)

KK_SKIN = (0.50, 0.55, 0.36)          # Kumbhakarna: dark olive-bronze
KK_LINE = (0.96, 0.90, 0.70)          # pale lines on his face
KK_DHOTI = (0.76, 0.16, 0.10)
KK_SASH = (1.0, 0.62, 0.14)
KK_HAIR = (0.16, 0.10, 0.08)
KK_HAIR2 = (0.42, 0.10, 0.07)
EYE_RED = (0.92, 0.26, 0.14)
TONGUE = (0.96, 0.46, 0.44)
TONGUE2 = (0.80, 0.28, 0.30)
LIP = (0.66, 0.20, 0.16)
IVORY = (1.0, 0.96, 0.84)
VB_SKIN = (0.62, 0.80, 0.68)          # Vibhishana: soft sea-green
SR_SKIN = (1.0, 0.86, 0.70)           # Saraswati
SR_SARI = (1.0, 0.97, 0.90)           # white
SR_CHOLI = (1.0, 0.70, 0.22)          # saffron-gold
SR_HALO = (0.82, 0.92, 1.0)           # pale rays
SR_BLUE = (0.36, 0.56, 0.96)
WOOD = (0.62, 0.36, 0.16)
WOOD2 = (0.80, 0.52, 0.22)
SWAN = (1.0, 0.98, 0.92)
SWAN2 = (0.86, 0.88, 0.92)
BEAK = (1.0, 0.56, 0.14)

KK_B = 1.45                           # his bulk (arms, legs, body)
HEAD_K = 1.22                         # his head is drawn this much bigger than a man() head
HINGE = (-8.0, -86.0)                 # the jaw's joint (head units, neck at 0, 0)
TONGUE_SEAT = (90.0, -86.0)           # where Saraswati sits on his tongue (jaw / head units, jaw closed)
LIP_UP = (116.0, -52.0)               # the upper lip's front (head units)
CU = 2.7                              # the close-up face: head units -> close-up sprite units
CU_L = CU ** -0.55                    # line widths in the close-up (finer than a plain scale-up)
SR_SEAT_H = 96.0                      # Saraswati seated: hip above the ground


# ------------------------------------------------------------------ Kumbhakarna's head (neck, upper part, jaw, tusks)


def _upper_pts():
    return [(-58, -62), (-70, -100), (-74, -140), (-60, -186), (-20, -218), (30, -214), (62, -190), (76, -164),
            (86, -146), (78, -134), (82, -122), (100, -108), (124, -94), (130, -78), (116, -66), (100, -66), (104, -58),
            (116, -52), (108, -46), (70, -48), (40, -52), (16, -60), (2, -76), (-8, -86), (-30, -76)]


def _jaw_pts():
    return [(-8, -86), (-18, -60), (-16, -20), (0, 12), (40, 24), (80, 22), (102, 12), (114, -8), (110, -26),
            (104, -34), (116, -40), (108, -46), (70, -48), (40, -52), (16, -60), (2, -76)]


def _neck_pts(low=12):
    return [(-56, -66), (-46, -20), (-42, low), (34, low), (36, -10), (20, -40), (0, -64)]


def _hair(cr, L):
    """Wild, flame-like locks all round the back of his head."""
    cx, cy = -46, -140
    mass = [(cx + 132 * math.cos(math.radians(a)) * (1 + 0.16 * math.sin(a * 0.31)),
             cy - 132 * math.sin(math.radians(a)) * (1 + 0.16 * math.cos(a * 0.27))) for a in range(50, 320, 18)]
    _shape(cr, mass, KK_HAIR, 5 * L)
    for i in range(13):
        a0 = math.radians(72 + 178 * i / 12)
        ln = 186 + 34 * math.sin(i * 2.3)
        ca, sa = math.cos(a0), -math.sin(a0)
        nx, ny = -sa, ca
        curl = 40 * (1 if i % 2 else -1)
        lock = [(cx + 56 * ca - 40 * nx, cy + 56 * sa - 40 * ny),
                (cx + ln * 0.55 * ca + curl * nx * 0.7, cy + ln * 0.55 * sa + curl * ny * 0.7),
                (cx + ln * ca + curl * nx, cy + ln * sa + curl * ny),
                (cx + ln * 0.66 * ca + (curl + 30) * nx * 0.7, cy + ln * 0.66 * sa + (curl + 30) * ny * 0.7),
                (cx + 56 * ca + 40 * nx, cy + 56 * sa + 40 * ny)]
        _shape(cr, lock, KK_HAIR if i % 3 else KK_HAIR2, 4 * L)
        holes_line(cr, [(cx + 76 * ca, cy + 76 * sa), (cx + ln * 0.76 * ca + curl * nx * 0.6,
                                                         cy + ln * 0.76 * sa + curl * ny * 0.6)], 15 * L, 2.6 * L)


def _kk_eye(cr, mood, L):
    """His eye and brow (the eye at 48, -124): open | daze | sleep | snore | shock | angry | speak | hungry."""
    ex, ey = 48, -124
    if mood in ("sleep", "snore"):
        ink(cr, [(ex - 24, ey + 2), (ex, ey + 12), (ex + 24, ey + 2)], 6 * L)
        for dx in (-12, 0, 12):
            ink(cr, [(ex + dx, ey + 9), (ex + dx - 2, ey + 19)], 3 * L)
        _shape(cr, [(ex - 30, ey - 22), (ex, ey - 30), (ex + 34, ey - 22), (ex + 32, ey - 14), (ex, ey - 20),
                    (ex - 28, ey - 14)], KK_HAIR, 3 * L)
        return
    r = 30 if mood == "shock" else 25
    cr.new_path()
    ell(cr, ex, ey, r * 1.1, r * 0.92)
    leather(cr, PALE, 4.5 * L)
    pr = 9 if mood == "shock" else 15
    px = ex + (6 if mood in ("open", "angry", "hungry") else 2)
    py = ey + (6 if mood in ("daze", "speak") else 0)
    cr.new_path()
    cr.arc(px, py, pr, 0, 2 * math.pi)
    leather(cr, EYE_RED, 3 * L)
    cr.new_path()
    cr.arc(px + 1, py, pr * 0.5, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    punch(cr, [(px + 4, py - 4)], 2.6 * L)
    if mood in ("daze", "speak"):                       # a heavy, half-shut lid: drowsy, under a spell
        cr.new_path()
        cr.move_to(ex - r * 1.2, ey + 2)
        cr.curve_to(ex - r * 0.8, ey - r * 1.4, ex + r * 0.8, ey - r * 1.4, ex + r * 1.2, ey + 2)
        cr.curve_to(ex + r * 0.6, ey - 4, ex - r * 0.6, ey - 4, ex - r * 1.2, ey + 2)
        cr.close_path()
        leather(cr, KK_SKIN, 0)
        ink(cr, [(ex - r * 1.15, ey + 1), (ex, ey - 5), (ex + r * 1.15, ey + 1)], 5.5 * L)
        for dx in (-14, 0, 14):
            ink(cr, [(ex + dx, ey - 3), (ex + dx - 2, ey + 6)], 2.6 * L)
    brow = {"open": [(ex - 32, ey - 30), (ex, ey - 40), (ex + 38, ey - 34)],
            "daze": [(ex - 32, ey - 26), (ex, ey - 32), (ex + 38, ey - 28)],
            "speak": [(ex - 32, ey - 26), (ex, ey - 32), (ex + 38, ey - 28)],
            "shock": [(ex - 34, ey - 44), (ex, ey - 58), (ex + 38, ey - 50)],
            "angry": [(ex - 34, ey - 46), (ex, ey - 34), (ex + 38, ey - 20)],
            "hungry": [(ex - 34, ey - 44), (ex, ey - 36), (ex + 38, ey - 24)]}[mood]
    bx = [(p[0], p[1] - 6) for p in brow]
    _shape(cr, bx + [(p[0], p[1] + 9) for p in reversed(brow)], KK_HAIR, 3 * L)
    if mood == "shock":
        for k in range(3):
            ink(cr, [(ex - 20 + 18 * k, ey - 70 - 4 * k), (ex - 14 + 18 * k, ey - 84 - 4 * k)], 3.5 * L, col=INK)


def kk_upper(cr, mood="open", L=1.0):
    """The head without its jaw: wild hair, the big ear and kundala, face, eye and brow, nose, curled moustache, upper
    fangs, a red tilak, the kirita."""
    _hair(cr, L)
    _shape(cr, _upper_pts(), KK_SKIN, 6 * L)
    holes_line(cr, [(-50, -170), (-60, -120), (-50, -76)], 14 * L, 2.6 * L)      # perforated cheek and skull
    holes_line(cr, [(10, -110), (34, -94), (50, -80)], 13 * L, 2.4 * L)
    ink(cr, [(84, -92), (96, -82), (104, -74)], 3.5 * L)                           # the nose's wing
    cr.new_path()
    ell(cr, 108, -76, 7, 5)
    cr.set_source_rgb(*INK)
    cr.fill()
    _kk_eye(cr, mood, L)
    for x in (70, 84, 98):                                                         # upper fangs
        _shape(cr, [(x - 5, -48), (x + 5, -48), (x + 1, -36)], IVORY, 2.2 * L, smooth=False)
    m = [(118, -56), (94, -62), (66, -60), (40, -64), (24, -76), (20, -96), (32, -104), (36, -88), (46, -74),
         (70, -70), (96, -68), (118, -62)]
    _shape(cr, m, KK_HAIR, 3.5 * L)                                                # curled moustache
    ink(cr, [(68, -172), (70, -190)], 6 * L, col=RED)                              # tilak
    ink(cr, [(58, -176), (60, -186)], 3 * L, col=KK_LINE)
    cr.save()
    cr.translate(6, -16)
    cr.scale(1.22, 1.22)
    R.kirita(cr, GOLD, None, tall=0.62, flare=RED)
    cr.restore()


def kk_neck(cr, L=1.0, low=12):
    """The neck behind the jaw (it shows when the mouth opens wide)."""
    _shape(cr, _neck_pts(low), KK_SKIN, 5 * L)
    ink(cr, [(-26, -40), (-22, low - 20)], 3 * L)


def kk_ear(cr, L=1.0):
    """The big ear and its gold kundala disc, which hides the jaw's joint (drawn over everything else)."""
    cr.new_path()
    ell(cr, -22, -118, 18, 30)
    leather(cr, KK_SKIN, 4.5 * L)
    ink(cr, [(-18, -136), (-28, -118), (-18, -102)], 3 * L)
    cr.new_path()
    cr.arc(-16, -76, 30, 0, 2 * math.pi)
    pl = leather(cr, GOLD, 4 * L, keep=True)
    perforate(cr, pl, 7 * L, 11 * L, 2.2 * L)
    cr.new_path()
    cr.arc(-16, -76, 16, 0, 2 * math.pi)
    leather(cr, (1.0, 0.62, 0.18), 3 * L)
    _jewel(cr, -16, -76, 7, RED)
    _jewel(cr, -16, -38, 8, RED)
    ink(cr, [(-16, -46), (-16, -40)], 3 * L, col=GOLD)


def kk_jaw(cr, L=1.0):
    """The jaw (a separate jointed piece): the tongue lying above its top edge (it shows only when the mouth opens),
    lower teeth, a red lower lip, the chin, a rivet at the joint."""
    tongue = [(6, -62), (28, -76), (66, -86), (98, -86), (112, -70), (106, -52), (66, -50), (30, -56)]
    _shape(cr, tongue, TONGUE, 3.5 * L)
    ink(cr, [(30, -68), (68, -76), (100, -70)], 2.5 * L, col=TONGUE2)
    for x in (76, 90, 104):
        _shape(cr, [(x - 5, -47), (x + 5, -47), (x, -58)], IVORY, 2.2 * L, smooth=False)
    _shape(cr, _jaw_pts(), KK_SKIN, 6 * L)
    _shape(cr, [(64, -48), (108, -46), (116, -40), (108, -32), (72, -38)], LIP, 3 * L)
    ink(cr, [(90, -10), (104, 2)], 3.5 * L)
    holes_line(cr, [(-14, -50), (6, -8), (60, 12)], 13 * L, 2.4 * L)
    rivet(cr, HINGE[0], HINGE[1], 7 * L)


def kk_tusks(cr, L=1.0):
    """Two ivory tusks rising from the lower jaw, outside the lips (drawn over the face)."""
    _shape(cr, [(30, -50), (26, -70), (30, -92), (42, -110), (52, -118), (54, -110), (46, -94), (44, -72), (46, -50)],
           IVORY, 4 * L)
    ink(cr, [(34, -62), (36, -84), (46, -104)], 2.2 * L, col=(0.70, 0.62, 0.48))
    _shape(cr, [(96, -46), (98, -60), (106, -72), (112, -76), (112, -66), (106, -56), (106, -46)], IVORY, 3.5 * L)


def _rot_about(cr, c, a):
    cr.translate(*c)
    cr.rotate(a)
    cr.translate(-c[0], -c[1])


def jaw_pt(p, jaw):
    """A point of the jaw (head units, as drawn closed) with the jaw opened by `jaw` radians."""
    c, s = math.cos(jaw), math.sin(jaw)
    dx, dy = p[0] - HINGE[0], p[1] - HINGE[1]
    return HINGE[0] + dx * c - dy * s, HINGE[1] + dx * s + dy * c


def mouth_cavity(cr, jaw, col=(0.30, 0.05, 0.05)):
    """The dark inside of the mouth for a jaw opened by `jaw` radians (head units): between the upper lip line and the
    jaw's rotated top edge."""
    if jaw <= 0.005:
        return
    top = [(2, -76), (16, -60), (40, -52), (70, -48), (108, -46), (118, -50)]
    low = [jaw_pt(p, jaw) for p in [(120, -42), (108, -46), (70, -48), (40, -52), (16, -60), (2, -76)]]
    cr.new_path()
    poly(cr, [HINGE] + top + low)
    cr.set_source_rgb(*col)
    cr.fill()


def kk_head(cr, mood="open", jaw=0.0, L=1.0):
    """The whole head in one piece (head units), the jaw opened by `jaw` radians."""
    kk_neck(cr, L)
    mouth_cavity(cr, jaw)
    cr.save()
    _rot_about(cr, HINGE, jaw)
    kk_jaw(cr, L)
    cr.restore()
    kk_upper(cr, mood, L)
    cr.save()
    _rot_about(cr, HINGE, jaw)
    kk_tusks(cr, L)
    cr.restore()
    kk_ear(cr, L)


KK_MOODS = {"open": 0.0, "daze": 0.0, "sleep": 0.0, "snore": 0.16, "shock": 0.22, "angry": 0.12, "speak": 0.24,
            "hungry": 0.42}


def _kk_head_sprite(mood):
    def fn(cr):
        cr.scale(HEAD_K, HEAD_K)
        kk_head(cr, mood, KK_MOODS[mood], 1 / HEAD_K)
    return fn


# ------------------------------------------------------------------ Kumbhakarna's body (the great belly)


def kk_body(cr):
    """A man() body with a great round belly hanging over the waist wrap, a heavy gold necklace."""
    b = KK_B
    for dy, ln in ((0, 1.0), (24, 0.75)):                                          # sash tails behind
        pts = [(-50 * b, -26 + dy), (-92 * b, -6 + dy), (-118 * b * ln, 40 + dy), (-128 * b * ln, 92 + dy)]
        band(cr, pts, 16, KK_SASH, holes=True, spacing=12, hole_r=2.4)
    torso = [(-50 * b, -6), (-58 * b, -100), (-64 * b, -190), (-56 * b, -246), (-30, -284), (-10, -300), (24, -300),
             (36 * b + 4, -282), (66 * b, -254), (84 * b, -214), (90 * b, -176), (106 * b, -140), (122 * b, -96),
             (128 * b, -52), (122 * b, -14), (102 * b, 14), (70 * b, 22), (50 * b, -6)]
    _shape(cr, torso, KK_SKIN)
    ink(cr, [(36 * b, -226), (62 * b, -200), (84 * b, -182)], 4.5)                # chest
    holes_line(cr, [(30 * b, -210), (56 * b, -184), (74 * b, -170)], 12, 2.6)
    holes_line(cr, [(-50 * b, -230), (-54 * b, -150), (-46 * b, -70)], 13, 2.6)
    for k, r in enumerate((150, 118, 86)):                                        # the belly's roundness
        holes_line(cr, [(64 * b - k * 8, -150 + k * 10), (100 * b - k * 10, -110 + k * 6),
                        (112 * b - k * 14, -60), (100 * b - k * 14, -10 - k * 6)], 15, 2.6)
    ink(cr, [(90 * b, -150), (108 * b, -132)], 3.5)
    cr.new_path()                                                                  # navel
    ell(cr, 110 * b, -58, 6, 9)
    cr.set_source_rgb(*INK)
    cr.fill()
    nk = GOLD
    band(cr, [(-12, -290), (26 * b, -252), (66 * b, -222)], 16, nk, spacing=12)
    band(cr, [(-26, -282), (14 * b, -196), (60 * b, -146)], 12, nk, spacing=11, hole_r=2.4)
    for i in range(7):
        u = i / 6
        _jewel(cr, -20 + 80 * b * u * 0.85, -282 + 136 * u + 20 * u * u, 8, RED if i % 2 else GREEN)
    _jewel(cr, 62 * b, -132, 15, RED)
    wrap = [(-66 * b, -30), (0, -36), (66 * b, -30), (80 * b, 14), (76 * b, 52), (0, 60), (-72 * b, 52),
            (-78 * b, 14)]
    _shape(cr, wrap, KK_DHOTI, 6)
    dots_in(cr, lambda: spath(cr, wrap), 20, 3.0)
    band(cr, [(-70 * b, -22), (0, -28), (70 * b, -22)], 18, GOLD, spacing=12)
    for x in (-40, 0, 40, 80):
        _jewel(cr, x * b * 0.8, -24, 7, RED)
    pf = [(24 * b, 30), (62 * b, 26), (104 * b, 246), (92 * b, 262), (80 * b, 248), (66 * b, 264), (52 * b, 248),
          (38 * b, 262), (26 * b, 246), (16 * b, 258)]
    _shape(cr, pf, GOLD, 5, smooth=False)
    for u in (0.3, 0.55, 0.8):
        ink(cr, [(24 * b + 38 * b * u, 34), (20 * b + 84 * b * u, 250)], 3, smooth=False)
    holes_line(cr, [(28 * b, 236), (98 * b, 232)], 12, 2.6)
    rivet(cr, 16 * b, 6, 8)


_KK = dict(skin=KK_SKIN, bulk=KK_B, dhoti=KK_DHOTI, border=GOLD, pleat=GOLD, sash=KK_SASH, neck=GOLD)
KUMBHA = man("kb_kk", crown="tiara", halo=False, hair=False, earring=False, tilak=False, hands=("open", "open"), **_KK)
register("kb_kk_body", (-220, -330, 220, 300), kk_body)
KUMBHA.points["mouth"] = ("kb_kk_head", (96 * HEAD_K, -58 * HEAD_K))
KUMBHA.points["eye"] = ("kb_kk_head", (48 * HEAD_K, -124 * HEAD_K))
KUMBHA.points["belly"] = ("kb_kk_body", (124 * KK_B, -70))
for _m in KK_MOODS:
    register("kb_kk_head" + ("" if _m == "open" else "_" + _m), (-410, -540, 185, 80), _kk_head_sprite(_m))


def kk_body_sit(cr):
    """His body seated (the front pleats tucked away)."""
    cr.save()
    cr.rectangle(-500, -600, 1000, 664)
    cr.clip()
    kk_body(cr)
    cr.restore()


def kk_seat(cr):
    """His legs folded, cross-legged (hip at 0, 0; the ground at y = +SEAT_H * 1.3)."""
    k = 1.3
    th = [(-90 * k, -30), (40 * k, -46), (170 * k, -34), (260 * k, -10), (276 * k, 40), (260 * k, 90), (124 * k, 100),
          (-40 * k, 100), (-100 * k, 74), (-104 * k, 14)]
    _shape(cr, th, KK_DHOTI, 6)
    dots_in(cr, lambda: spath(cr, th), 20, 3.0)
    band(cr, [(254 * k, -8), (276 * k, 40), (260 * k, 90)], 16, GOLD, spacing=11, hole_r=2.4)
    band(cr, [(-92 * k, 92), (250 * k, 94)], 12, GOLD, holes=False)
    foot = [(110 * k, 8), (160 * k, -8), (214 * k, -2), (232 * k, 22), (204 * k, 40), (124 * k, 42)]
    _shape(cr, foot, KK_SKIN, 5)
    rivet(cr, 0, 0, 9)


register("kb_kk_body_sit", (-220, -330, 220, 80), kk_body_sit)
register("kb_kk_seat", (-150, -80, 380, 150), kk_seat)


# ------------------------------------------------------------------ the close-up head (finer lines, bigger)


def _cu(fn):
    def draw(cr):
        cr.scale(CU, CU)
        fn(cr)
    return draw


CU_BOX = (-330 * CU, -440 * CU, 150 * CU, 4 * CU)
for _m in ("open", "daze", "shock", "angry", "speak", "sleep"):
    register("kb_cu_up" + ("" if _m == "open" else "_" + _m), CU_BOX,
             _cu((lambda m: lambda cr: kk_upper(cr, m, CU_L))(_m)))
register("kb_cu_jaw", (-42 * CU, -92 * CU, 125 * CU, 32 * CU), _cu(lambda cr: kk_jaw(cr, CU_L)))
register("kb_cu_neck", (-60 * CU, -76 * CU, 42 * CU, 140 * CU), _cu(lambda cr: kk_neck(cr, CU_L, 130)))
register("kb_cu_tusk", (16 * CU, -126 * CU, 122 * CU, -40 * CU), _cu(lambda cr: kk_tusks(cr, CU_L)))
register("kb_cu_ear", (-52 * CU, -152 * CU, 18 * CU, -26 * CU), _cu(lambda cr: kk_ear(cr, CU_L)))


# ------------------------------------------------------------------ Saraswati, her veena and swan


def saras_head(cr, mood="open"):
    """Saraswati: a ring of pale rays, her hair in a bun with jasmine, a gold crown with pearl strings, a white flower,
    a red bindi, a nose ring and gold earrings."""
    M._ray_halo(cr, -20, -168, 108, 160, 18, (PALE, SR_HALO))
    S._face_w(cr, SR_SKIN)
    hair = [(-40, -170), (0, -190), (36, -178), (44, -160), (20, -164), (-10, -150), (-30, -110), (-44, -90),
            (-52, -128)]
    _shape(cr, hair, HAIR, 4)
    hp = [(-40, -150), (-70, -110), (-84, -40), (-80, 40), (-60, 80), (-44, 30), (-40, -40), (-30, -100)]
    _shape(cr, hp, HAIR, 4)
    for k in range(3):
        holes_line(cr, [(-50 - 6 * k, -120), (-66 - 4 * k, -40), (-60 - 2 * k, 40)], 15, 2.2)
    for i in range(7):
        _flower(cr, -58 - 8 * math.sin(i), -110 + 26 * i, 8, PALE, 5)
    cr.save()
    cr.translate(4, -21)
    cr.scale(0.86, 0.86)
    S.parvati_crown(cr)
    cr.restore()
    S._w_eyes(cr, SR_SKIN, mood)
    cr.new_path()
    cr.arc(46, -148, 5.5, 0, 2 * math.pi)
    cr.set_source_rgb(*RED)
    cr.fill()
    cr.new_path()
    cr.arc(64, -90, 8, 0, 2 * math.pi)
    cr.set_source_rgb(*GOLD)
    cr.set_line_width(3)
    cr.stroke()
    _jewel(cr, -10, -70, 10, GOLD)
    for x in (-18, -8, 2):
        cr.new_path()
        cr.arc(x, -50, 4, 0, 2 * math.pi)
        leather(cr, PALE, 1.5)


def _sr_extra(cr):
    """Pearl strings and a gold necklace with a blue pendant."""
    band(cr, [(-20, -282), (14, -226), (42, -184)], 8, GOLD, spacing=10, hole_r=1.8)
    for i in range(10):
        u = i / 9
        cr.new_path()
        cr.arc(-28 + 66 * u, -276 + 130 * u + 20 * u * u, 5, 0, 2 * math.pi)
        leather(cr, PALE, 2)
    _jewel(cr, 38, -126, 11, SR_BLUE)


SARAS = woman("kb_saras", skin=SR_SKIN, skirt=SR_SARI, choli=SR_CHOLI, border=GOLD, pallu_col=SR_SARI, gem=SR_BLUE,
              ornaments_extra=_sr_extra, hands=("open", "open"))
for _e in ("open", "smile", "speak"):
    register("kb_saras_head" + ("" if _e == "open" else "_" + _e), (-240, -390, 190, 110),
             (lambda e: lambda cr: saras_head(cr, e))(_e))


def _sr_body_sit(cr):
    cr.save()
    cr.rectangle(-400, -600, 800, 640)
    cr.clip()
    woman_body(cr, dict(skin=SR_SKIN, skirt=SR_SARI, choli=SR_CHOLI, border=GOLD, pallu_col=SR_SARI, gem=SR_BLUE,
                        ornaments_extra=_sr_extra))
    cr.restore()


def _sr_seat(cr):
    """Her lap, cross-legged, in the white sari with its gold border (hip at 0, 0; ground at y = +SR_SEAT_H)."""
    lap = [(-90, -30), (40, -40), (170, -26), (236, -4), (250, 44), (234, 90), (100, 96), (-50, 96), (-104, 70),
           (-108, 10)]
    _shape(cr, lap, SR_SARI, 5)
    dots_in(cr, lambda: spath(cr, lap), 22, 2.8, shape="d")
    band(cr, [(-96, 88), (236, 88)], 18, GOLD, spacing=12, hole_r=2.4)
    band(cr, [(230, -2), (250, 44), (234, 86)], 14, GOLD, spacing=11, hole_r=2.2)
    foot = [(110, 10), (156, -4), (204, 2), (222, 24), (196, 40), (120, 42)]
    _shape(cr, foot, SR_SKIN, 4)
    for x in (196, 206, 214):
        ink(cr, [(x, 6), (x + 4, 20)], 2.2)
    band(cr, [(124, 30), (150, 28)], 8, GOLD, spacing=8, hole_r=1.8)
    rivet(cr, 0, 0, 8)


register("kb_saras_body_sit", (-140, -310, 170, 50), _sr_body_sit)
register("kb_saras_seat", (-130, -60, 270, 120), _sr_seat)


def _veena(cr):
    """The veena (pivot at the middle of its neck), lying along +x: the great round resonator at the +x end with a
    perforated face, a long wooden neck with gold frets and strings, the small gourd hung under the neck's far end, a
    curled yali head at the tip."""
    cr.new_path()                                                                  # the great resonator
    ell(cr, 330, 8, 128, 118)
    pl = leather(cr, WOOD2, 6, keep=True)
    perforate(cr, pl, 12, 16, 3.0)
    cr.new_path()
    ell(cr, 338, 8, 84, 78)
    leather(cr, (0.92, 0.66, 0.28), 4)
    for i in range(8):
        a = 2 * math.pi * i / 8
        _flower(cr, 338 + 52 * math.cos(a), 8 + 50 * math.sin(a), 11, GOLD, 6)
    _jewel(cr, 338, 8, 14, RED)
    cr.new_path()                                                                  # the small gourd under the neck
    ell(cr, -250, 64, 60, 56)
    leather(cr, WOOD2, 5)
    dots_in(cr, lambda: ell(cr, -250, 64, 44, 40), 16, 2.6)
    ink(cr, [(-250, 8), (-250, 20)], 8, col=GOLD)
    neck = [(-330, -24), (230, -24), (240, 24), (-330, 24)]                        # the neck
    _shape(cr, neck, WOOD, 5, smooth=False)
    band(cr, [(-326, -14), (236, -14)], 8, GOLD, holes=False, lw=2.5)
    for i in range(16):
        x = -300 + 33 * i
        ink(cr, [(x, -24), (x, 24)], 3, smooth=False, col=GOLD)
    for dy in (-6, 2, 10):
        ink(cr, [(-330, dy), (420, dy * 0.4 + 8)], 1.6, smooth=False, col=PALE)
    yali = [(-330, -24), (-372, -40), (-404, -76), (-396, -110), (-370, -116), (-362, -92), (-380, -70),
            (-358, -40), (-330, 24)]
    _shape(cr, yali, GOLD, 5)
    _jewel(cr, -386, -94, 8, GREEN)
    for x in (-310, 210):
        band(cr, [(x, -30), (x, 30)], 14, GOLD, spacing=9, hole_r=2.0)


def _swan(cr):
    """Saraswati's swan (hamsa) in profile facing +x, feet at (0, 0): a white body with perforated feather rows, a
    long neck, an orange beak, a small gold crest and a necklace."""
    tail = [(-200, -130), (-292, -196), (-276, -150), (-232, -104)]
    _shape(cr, tail, SWAN2, 4)
    body = [(-236, -124), (-180, -176), (-70, -200), (40, -196), (110, -170), (134, -126), (108, -80), (20, -58),
            (-110, -58), (-206, -84)]
    _shape(cr, body, SWAN, 6)
    wing = [(-220, -136), (-130, -206), (-10, -222), (80, -190), (30, -150), (-80, -120), (-180, -108)]
    _shape(cr, wing, SWAN2, 4, holes=(10, 14, 2.4))
    for k in range(4):
        ink(cr, [(-160 + 52 * k, -192 + 4 * k), (-120 + 52 * k, -136)], 2.4, col=(0.62, 0.64, 0.70))
    neck = [(84, -176), (118, -236), (112, -300), (96, -360), (110, -420), (150, -446), (190, -436), (204, -410),
            (180, -404), (152, -410), (134, -386), (140, -330), (154, -260), (138, -170)]
    _shape(cr, neck, SWAN, 5)
    beak = [(198, -432), (258, -412), (198, -402)]
    _shape(cr, beak, BEAK, 3.5, smooth=False)
    cr.new_path()
    cr.arc(174, -424, 6, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    _shape(cr, [(140, -444), (130, -472), (152, -462), (160, -448)], GOLD, 3, smooth=False)
    band(cr, [(112, -290), (150, -282)], 10, GOLD, spacing=9, hole_r=1.8)
    _jewel(cr, 130, -274, 7, RED)
    for dx in (-30, 20):
        ink(cr, [(dx, -64), (dx + 4, -24), (dx, 0)], 6, smooth=False, col=BEAK)
        ink(cr, [(dx - 20, 2), (dx + 26, 2)], 5, smooth=False, col=BEAK)


def _pillow(cr):
    """A fat bolster pillow with gold ends (pivot at its bottom centre): it turns a cot into a bed."""
    pts = [(-120, 0), (-132, -40), (-110, -84), (0, -96), (110, -84), (132, -40), (120, 0), (0, 8)]
    _shape(cr, pts, PALE, 5)
    dots_in(cr, lambda: spath(cr, pts), 20, 2.6, shape="d")
    for sx in (-1, 1):
        band(cr, [(sx * 104, -86), (sx * 124, -40), (sx * 112, 2)], 16, GOLD, spacing=10, hole_r=2.0)
    ink(cr, [(-60, -80), (-40, -10)], 2.5, col=(0.70, 0.62, 0.48))
    ink(cr, [(40, -84), (56, -12)], 2.5, col=(0.70, 0.62, 0.48))


register("kb_veena", (-420, -130, 470, 130), _veena)
register("kb_swan", (-310, -490, 270, 12), _swan)
register("kb_pillow", (-150, -110, 150, 20), _pillow)


# ------------------------------------------------------------------ the whole world, the drum, a drumstick


def _world(cr):
    """The whole world as one leather disc (pivot at its centre): blue sea, green lands with trees, little houses and a
    temple, a perforated gold rim."""
    cr.new_path()
    cr.arc(0, 0, 236, 0, 2 * math.pi)
    leather(cr, GOLD, 6)
    cr.new_path()
    cr.arc(0, 0, 210, 0, 2 * math.pi)
    pl = leather(cr, (0.46, 0.70, 0.98), 5, keep=True)
    perforate(cr, pl, -14, 18, 3.0)
    for k in range(3):
        ink(cr, [(-170 + 40 * k, 120 + 18 * k), (-120 + 40 * k, 110 + 18 * k), (-70 + 40 * k, 122 + 18 * k)], 3,
            col=(0.30, 0.50, 0.86))
    land1 = [(-180, -40), (-130, -120), (-40, -150), (40, -110), (60, -40), (0, 20), (-90, 40), (-160, 20)]
    land2 = [(60, 30), (120, -40), (190, -20), (200, 60), (150, 130), (70, 120)]
    for land in (land1, land2):
        _shape(cr, land, (0.48, 0.76, 0.34), 4)
        dots_in(cr, lambda land=land: spath(cr, land), 22, 2.6)
    for x, y in ((-130, -40), (-60, -100), (150, 40)):                            # trees
        ink(cr, [(x, y + 26), (x, y)], 6, col=(0.42, 0.24, 0.10))
        cr.new_path()
        cr.arc(x, y - 14, 22, 0, 2 * math.pi)
        leather(cr, (0.20, 0.52, 0.24), 3)
    for x, y in ((-20, -40), (10, -60), (120, 80)):                                # little houses
        _shape(cr, [(x - 16, y + 14), (x + 16, y + 14), (x + 16, y - 6), (x, y - 22), (x - 16, y - 6)], RED, 3,
               smooth=False)
    _shape(cr, [(-100, 10), (-70, 10), (-70, -20), (-85, -50), (-100, -20)], GOLD, 3, smooth=False)   # a temple
    cr.new_path()
    ell(cr, -60, -180, 56, 20)                                                     # a cloud
    leather(cr, PALE, 3)


def _drum(cr, stand=True):
    """A big dhol on its side (pivot at the bottom centre): a red barrel with gold bands, laced skins at both ends,
    on a wooden stand (stand=False: hung from a drummer's waist by its strap)."""
    if stand:
        _shape(cr, [(-150, 0), (150, 0), (130, -30), (-130, -30)], WOOD, 4, smooth=False)
    else:
        band(cr, [(-150, -140), (-60, -320), (60, -320), (150, -140)], 12, (0.86, 0.62, 0.30), holes=False)
    body = [(-160, -60), (-120, -210), (0, -232), (120, -210), (160, -60), (0, -40)]
    _shape(cr, body, (0.86, 0.20, 0.12), 6)
    for x in (-90, 0, 90):
        band(cr, [(x, -54), (x + (0 if x == 0 else x * 0.08), -226)], 14, GOLD, spacing=11, hole_r=2.2)
    for k in range(9):
        ink(cr, [(-150 + 33 * k, -70), (-134 + 33 * k, -200)], 2.2, col=(0.98, 0.86, 0.60))
    for sx in (-1, 1):
        cr.new_path()
        ell(cr, sx * 160, -136, 30, 92)
        leather(cr, PALE, 5)
        cr.new_path()
        ell(cr, sx * 160, -136, 14, 50)
        leather(cr, (0.96, 0.84, 0.62), 2.5)


def _stick(cr):
    """A drumstick (grip at 0, 0, the knob at the far end)."""
    band(cr, [(0, 40), (0, -190)], 12, WOOD, holes=False)
    cr.new_path()
    cr.arc(0, -200, 18, 0, 2 * math.pi)
    leather(cr, RED, 3)


register("kb_world", (-245, -245, 245, 245), _world)
register("kb_drum", (-200, -245, 200, 8), _drum)
register("kb_dhol", (-200, -340, 200, 8), lambda cr: _drum(cr, False))
register("kb_stick", (-24, -225, 24, 50), _stick)
