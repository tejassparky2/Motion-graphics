"""Builder B's leather props and extra puppets for long video 2 (videos/yamlok_yatra.py, scenes_yy_b): the road, the
sixteen cities, the Vaitarani and the cold city. Togalu Gombeyaata style as in garuda_cast / six_cast_b: punched
leather, ink outlines, jointed rod puppets. Every sprite name starts with "yb_".

  THE MESSENGERS' MOODS  garuda_cast's Yamaduta head laughing (c2) and shouting (w6).
  KING JANGAMA           the king "who has the appearance of Death" (Garuda Purana II.52): a tall, gaunt, dark king
                         in a dark shroud and an iron crown with spikes, deep-set eyes, hollow cheeks. Never a skull.
  KING VICHITRA          Yama's younger brother (II.63): a big stern king, Yama's blue-grey skin, a tall gold crown
                         with a violet flare, a plum dhoti.
  Props                  a banyan tree with hanging roots, a thorn bush, a clump of sword-shaped leaves (no wounds
                         anywhere), crocodile backs, a soaring vulture, an ice peak, Yama's city on the horizon, a
                         kadhai (frying pan) of ghee.
"""
import math

import arjuna_cast as A
import garuda_cast as GC
import ravana_cast as R
from puppet_cast import HAIR, _jewel, _shape, man
from puppet_core import GOLD, INK, RED, VIOLET, band, dots_in, ell, holes_line, ink, leather, punch, register

BARK = (0.48, 0.32, 0.18)
BARK2 = (0.62, 0.42, 0.22)
LEAF1 = (0.24, 0.52, 0.22)
LEAF2 = (0.36, 0.64, 0.26)
THORN = (0.40, 0.26, 0.14)
STEEL = (0.62, 0.70, 0.66)            # the sword-leaves: a cold grey-green
STEEL2 = (0.44, 0.54, 0.50)
CROC = (0.36, 0.42, 0.26)
CROC2 = (0.26, 0.30, 0.18)
VUL = (0.30, 0.22, 0.16)
VUL2 = (0.50, 0.38, 0.26)
ICE = (0.86, 0.92, 0.98)
ICE2 = (0.62, 0.74, 0.88)
FORT = (0.30, 0.26, 0.30)
FORT2 = (0.44, 0.36, 0.38)
JG_SKIN = (0.36, 0.33, 0.40)          # Jangama: ash-grey
JG_ROBE = (0.16, 0.13, 0.18)
IRON = (0.42, 0.42, 0.48)
VC_SKIN = (0.32, 0.40, 0.56)          # Vichitra: Yama's blue-grey, a little lighter
VC_DHOTI = (0.50, 0.16, 0.36)
GHEE = (1.0, 0.80, 0.30)


# ------------------------------------------------------------------ the messengers laughing and shouting


def duta_head_mood(cr, mood):
    """garuda_cast.duta_head with another face (laugh | scold)."""
    locks = []
    cx, cy = -30, -130
    n = 15
    for i in range(n + 1):
        a = math.radians(-100 - 170 * i / n)
        r = 150 if i % 2 == 0 else 96
        r += 30 * math.sin(i * 1.7)
        locks.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    locks += [(-60, -10), (-20, -60), (10, -150)]
    _shape(cr, locks, GC.DU_HAIR, 5)
    for i in range(0, n, 2):
        a = math.radians(-100 - 170 * i / n)
        ink(cr, [(cx + 50 * math.cos(a), cy + 50 * math.sin(a)), (cx + 120 * math.cos(a), cy + 120 * math.sin(a))],
            2.6, col=(0.32, 0.30, 0.38))
    A.face(cr, dict(skin=GC.DU_SKIN, hair=False, moustache=True, tilak=False, earring=True), mood)
    ink(cr, [(22, -88), (6, -76), (12, -62), (24, -64)], 6, col=GC.DU_HAIR)
    if mood == "laugh":
        ink(cr, [(10, -166), (34, -158), (60, -166)], 8, col=GC.DU_HAIR)
    else:
        ink(cr, [(10, -160), (34, -150), (60, -164)], 9, col=GC.DU_HAIR)
    band(cr, [(-52, -168), (0, -192), (46, -186)], 22, IRON, spacing=12, hole_r=2.4)
    _jewel(cr, 18, -190, 10, RED)


for _m in ("laugh", "scold"):
    register("yb_duta_head_" + _m, (-220, -330, 120, 100), (lambda m: lambda cr: duta_head_mood(cr, m))(_m))


# ------------------------------------------------------------------ King Jangama, who looks like Death


def jang_head(cr):
    """A gaunt dark king in profile: a long narrow face, hollow cheek, deep-set eye in a dark ring, a thin drooping
    moustache, a tall iron crown with spikes and a dull violet stone. Not a skull: a living, frightening face."""
    hood = [(-40, -170), (-96, -120), (-112, -20), (-104, 80), (-70, 120), (-40, 40), (-34, -60)]
    _shape(cr, hood, JG_ROBE, 5)
    fc = [(-26, 20), (-32, -40), (-46, -90), (-50, -140), (-36, -184), (4, -200), (38, -186), (52, -150), (56, -126),
          (62, -112), (84, -88), (62, -80), (64, -66), (54, -54), (56, -40), (46, -20), (40, 0), (20, 26)]
    _shape(cr, fc, JG_SKIN, 6)
    ink(cr, [(10, -92), (26, -62), (34, -36)], 4, col=(0.18, 0.15, 0.20))           # the hollow cheek
    cr.new_path()
    ell(cr, 26, -128, 30, 18, -0.1)
    cr.set_source_rgb(0.12, 0.10, 0.14)
    cr.fill()
    cr.new_path()
    ell(cr, 30, -128, 14, 7, -0.1)                                                   # a small cold eye
    leather(cr, (0.92, 0.94, 1.0), 2.5)
    cr.new_path()
    cr.arc(34, -128, 4.5, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.fill()
    ink(cr, [(4, -152), (30, -150), (58, -142)], 7, col=(0.12, 0.10, 0.14))         # a heavy brow
    ink(cr, [(60, -64), (48, -48), (40, -22)], 4, col=(0.12, 0.10, 0.14))           # the thin moustache
    cr.new_path()
    ell(cr, -18, -112, 11, 20)
    leather(cr, JG_SKIN, 4)
    base = [(-48, -176), (-30, -206), (40, -206), (52, -184)]
    _shape(cr, base + [(52, -170), (-50, -164)], IRON, 4, smooth=False)
    for k in range(5):                                                               # the spikes
        x = -40 + 22 * k
        h = 70 + 30 * (k % 2)
        _shape(cr, [(x - 9, -204), (x + 2, -204 - h), (x + 12, -204)], IRON, 3.5, smooth=False)
    _jewel(cr, 6, -190, 10, VIOLET)
    holes_line(cr, [(-40, -180), (46, -180)], 14, 2.2, smooth=False)


JANG = man("yb_jang", skin=JG_SKIN, bulk=0.82, dhoti=JG_ROBE, border=IRON, pleat=(0.24, 0.20, 0.26), sash=VIOLET,
           neck=IRON, crown="tiara", halo=False, hair=False, earring=False, tilak=False, robe=JG_ROBE,
           hands=("open", "open"))
register("yb_jang_head", (-150, -320, 110, 140), jang_head)


# ------------------------------------------------------------------ King Vichitra, Yama's younger brother


def vich_head(cr, mood="angry"):
    """Vichitra: Yama's blue-grey skin, long black hair, a curled moustache, a stern brow, a tall gold crown with a
    violet flare and green stones."""
    A.face(cr, dict(skin=VC_SKIN, hair=True, moustache=True, tilak=True, earring=True), mood)
    ink(cr, [(20, -88), (8, -78), (14, -66)], 5, col=HAIR)
    R.kirita(cr, GOLD, None, tall=1.2, flare=VIOLET)
    h = lambda y: -150 + (y + 150) * 1.2  # noqa: E731
    for sx in (-1, 1):
        _shape(cr, [(sx * 30, -170), (sx * 60, h(-236)), (sx * 48, h(-280)), (sx * 38, h(-236)), (sx * 18, -190)],
               GOLD, 4, smooth=False, holes=(7, 11, 2.2))
    _jewel(cr, 2, h(-292), 10, (0.16, 0.66, 0.40))


VICH = man("yb_vich", skin=VC_SKIN, bulk=1.3, dhoti=VC_DHOTI, border=GOLD, pleat=GOLD, sash=(0.16, 0.56, 0.42),
           neck=GOLD, crown="tiara", halo=False, moustache=True, thread=True, hands=("open", "fist"))
for _m in ("angry", "calm"):
    register("yb_vich_head" + ("" if _m == "angry" else "_" + _m), (-230, -500, 140, 120),
             (lambda m: lambda cr: vich_head(cr, m))(_m))


# ------------------------------------------------------------------ trees and plants


def _banyan(cr):
    """A great banyan (pivot at the trunk's foot): a thick fluted trunk, wide spreading arms, a broad roof of leaf
    clusters and hanging aerial roots."""
    for x0, x1, top in ((-430, -440, -560), (380, 400, -590), (-250, -246, -640), (560, 590, -520)):
        ink(cr, [(x0, top), (x0 + 6, top + 260), (x1, -10)], 9, col=INK)
        ink(cr, [(x0, top), (x0 + 6, top + 260), (x1, -10)], 5, col=BARK2)
    for x in range(-600, 680, 70):                                                  # thin hanging roots
        top = -560 - 40 * math.sin(x * 0.02)
        L_ = 160 + 120 * ((x * 0.37) % 1.0)
        ink(cr, [(x, top), (x + 6, top + L_ * 0.5), (x - 2, top + L_)], 3.2, col=(0.42, 0.28, 0.14))
    trunk = [(-150, 0), (-120, -120), (-110, -300), (-150, -460), (-260, -560), (-200, -580), (-60, -470),
             (0, -520), (60, -470), (220, -590), (280, -560), (130, -440), (110, -300), (130, -120), (170, 0)]
    _shape(cr, trunk, BARK, 6, holes=(14, 20, 2.6))
    for x in (-60, 0, 60):
        ink(cr, [(x, -20), (x + 8, -200), (x - 4, -380)], 3, col=(0.30, 0.18, 0.08))
    blobs = [(-520, -640, 200, 120), (-300, -760, 240, 150), (0, -800, 280, 160), (300, -760, 250, 150),
             (540, -650, 210, 120), (-160, -620, 200, 110), (180, -620, 210, 110), (-640, -560, 130, 80),
             (660, -560, 140, 80)]
    for i, (x, y, rx, ry) in enumerate(blobs):
        cr.new_path()
        ell(cr, x, y, rx, ry)
        leather(cr, LEAF1 if i % 2 == 0 else LEAF2, 6)
        dots_in(cr, lambda x=x, y=y, rx=rx, ry=ry: ell(cr, x, y, rx - 26, ry - 22), 30, 3.4)
    for i in range(26):                                                             # leaf marks
        a = i * 2.39
        x = 620 * math.sin(a) * ((i * 0.37) % 1.0)
        y = -700 + 120 * math.cos(a * 1.3)
        ink(cr, [(x - 14, y), (x + 14, y - 8)], 3, col=(0.16, 0.34, 0.14))


register("yb_banyan", (-760, -980, 800, 20), _banyan)


def _thorns(cr):
    """A low thorn bush (pivot on the ground): dark twisted branches bristling with sharp thorns."""
    rng = [(-180, -40, -260, -200), (-60, -10, -120, -260), (40, 0, 60, -280), (140, -30, 230, -200),
           (0, -10, -20, -180), (-120, -30, -230, -110), (100, -20, 240, -100)]
    for x0, y0, x1, y1 in rng:
        mx, my = (x0 + x1) / 2 + 20, (y0 + y1) / 2
        ink(cr, [(x0, y0), (mx, my), (x1, y1)], 14, col=INK)
        ink(cr, [(x0, y0), (mx, my), (x1, y1)], 8, col=THORN)
        for k in range(1, 6):
            u = k / 6
            px, py = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
            dx, dy = x1 - x0, y1 - y0
            ln = math.hypot(dx, dy) or 1
            nx, ny = -dy / ln, dx / ln
            sg = 1 if k % 2 else -1
            _shape(cr, [(px - dx / ln * 7, py - dy / ln * 7), (px + sg * nx * 34 + dx / ln * 10,
                                                                 py + sg * ny * 34 + dy / ln * 10),
                        (px + dx / ln * 7, py + dy / ln * 7)], THORN, 2.5, smooth=False)
    _shape(cr, [(-220, 6), (220, 6), (180, -24), (-180, -24)], (0.50, 0.36, 0.20), 4)


register("yb_thorns", (-300, -320, 300, 20), _thorns)


def _swordleaf(cr):
    """A clump of tall, stiff, sword-shaped leaves (pivot on the ground): straight blades with a sharp point, a bright
    edge line and a little cross-guard at the base of each, cold grey-green."""
    blades = [(-150, -0.30, 520), (-80, -0.14, 660), (-10, 0.0, 720), (60, 0.12, 640), (130, 0.26, 540),
              (-200, -0.42, 400), (190, 0.40, 420)]
    for x, a, L_ in sorted(blades, key=lambda b: -abs(b[1])):
        ca, sa = math.cos(a), math.sin(a)
        tip = (x + L_ * sa, -L_ * ca)
        w = 26
        pts = [(x - w * ca, -10 - w * sa), (x - w * ca + (L_ - 70) * sa, -10 - w * sa - (L_ - 70) * ca), tip,
               (x + w * ca + (L_ - 70) * sa, -10 + w * sa - (L_ - 70) * ca), (x + w * ca, -10 + w * sa)]
        _shape(cr, pts, STEEL if a >= 0 else STEEL2, 5, smooth=False)
        ink(cr, [(x + 30 * sa, -40 - 30 * ca), (x + (L_ - 60) * sa, -10 - (L_ - 60) * ca)], 3,
            col=(0.92, 0.97, 0.94))
        _shape(cr, [(x - 46 * ca, -34 - 46 * sa), (x + 46 * ca, -34 + 46 * sa), (x + 46 * ca + 14 * sa,
                                                                                -48 + 46 * sa),
                    (x - 46 * ca + 14 * sa, -48 - 46 * sa)], (0.56, 0.44, 0.22), 3, smooth=False)
    _shape(cr, [(-260, 6), (260, 6), (220, -26), (-220, -26)], (0.40, 0.46, 0.30), 4)


register("yb_swordleaf", (-420, -760, 420, 20), _swordleaf)


# ------------------------------------------------------------------ the river's creatures


def _croc(cr):
    """A crocodile's back and head showing above the water (pivot at the waterline, middle), facing +x: a humped
    back with ridged scutes, a raised eye, a long snout with nostrils, the tail's tip."""
    back = [(-460, 0), (-420, -30), (-300, -64), (-120, -88), (60, -86), (170, -76), (220, -104), (262, -118),
            (300, -100), (330, -64), (440, -52), (500, -40), (510, -16), (500, 0)]
    _shape(cr, back, CROC, 5, holes=(12, 18, 2.4))
    for k in range(10):                                                             # scutes
        x = -380 + 56 * k
        y = -60 - 26 * math.sin(math.pi * (k + 1) / 11)
        _shape(cr, [(x - 20, y + 10), (x, y - 28), (x + 20, y + 10)], CROC2, 3, smooth=False)
    for x in (-260, -140, -20, 100):
        ink(cr, [(x, -30), (x + 40, -34)], 2.5, col=CROC2)
    cr.new_path()
    ell(cr, 262, -112, 30, 24)
    leather(cr, CROC, 4)
    from puppet_core import almond_eye
    almond_eye(cr, 266, -116, 30, 12, col=(1.0, 0.84, 0.30), lw=3)
    for x in (360, 400, 440):
        ink(cr, [(x, -54), (x + 8, -40)], 2.5)
    cr.new_path()
    ell(cr, 486, -46, 12, 8)
    leather(cr, CROC2, 3)


register("yb_croc", (-480, -160, 530, 14), _croc)


def _vulture(cr):
    """A vulture circling high up, seen from below (pivot at its body, head toward -y): long broad wings with fingered
    tips, a short fan tail, a pale neck ruff and a small bare head."""
    for sg in (-1, 1):
        wing = [(sg * 30, -40), (sg * 180, -70), (sg * 340, -80), (sg * 430, -66), (sg * 470, -50),
                (sg * 520, -56), (sg * 500, -34), (sg * 540, -28), (sg * 506, -10), (sg * 532, 2), (sg * 490, 12),
                (sg * 500, 30), (sg * 440, 24), (sg * 360, 30), (sg * 200, 34), (sg * 40, 40)]
        _shape(cr, wing, VUL, 5, holes=(14, 22, 2.6))
        for k in range(5):
            ink(cr, [(sg * (110 + 60 * k), -58 + 2 * k), (sg * (130 + 60 * k), 26)], 2.5, col=VUL2)
    tail = [(-30, 40), (30, 40), (56, 120), (0, 136), (-56, 120)]
    _shape(cr, tail, VUL, 4)
    body = [(0, -80), (40, -40), (44, 40), (0, 70), (-44, 40), (-40, -40)]
    _shape(cr, body, VUL2, 5)
    cr.new_path()
    ell(cr, 0, -78, 40, 24)
    leather(cr, (0.92, 0.86, 0.76), 4)
    head = [(-16, -96), (-12, -128), (0, -140), (12, -128), (16, -96)]
    _shape(cr, head, (0.90, 0.62, 0.52), 3.5)
    ink(cr, [(0, -140), (0, -152)], 6)


register("yb_vulture", (-560, -170, 560, 150), _vulture)


# ------------------------------------------------------------------ cold, the far city, the pan of ghee


def _icepeak(cr):
    """Snowy mountain peaks (pivot at the base centre): pale blue-white rock with darker ridges and icicles."""
    for dx, s, col in ((-300, 0.75, ICE2), (320, 0.85, ICE2), (0, 1.0, ICE)):
        pk = [(dx - 420 * s, 0), (dx - 220 * s, -320 * s), (dx - 120 * s, -420 * s), (dx - 40 * s, -560 * s),
              (dx + 30 * s, -600 * s), (dx + 110 * s, -470 * s), (dx + 240 * s, -330 * s), (dx + 420 * s, 0)]
        _shape(cr, pk, col, 6, smooth=False, holes=(14, 22, 2.6))
        ink(cr, [(dx + 30 * s, -600 * s), (dx - 30 * s, -420 * s), (dx + 40 * s, -260 * s), (dx - 20 * s, -80 * s)],
            3.5, col=(0.40, 0.52, 0.70))
        ink(cr, [(dx - 120 * s, -420 * s), (dx - 160 * s, -250 * s)], 3, col=(0.40, 0.52, 0.70))
        snow = [(dx - 120 * s, -420 * s), (dx - 40 * s, -560 * s), (dx + 30 * s, -600 * s), (dx + 110 * s, -470 * s),
                (dx + 70 * s, -440 * s), (dx + 30 * s, -480 * s), (dx - 10 * s, -430 * s), (dx - 60 * s, -460 * s)]
        _shape(cr, snow, (1.0, 1.0, 1.0), 4, smooth=False)


register("yb_icepeak", (-780, -620, 740, 10), _icepeak)


def _yamapura(cr):
    """Yama's city far away (pivot at the bottom centre): a long dark wall with towers and red flags, a great gate
    in the middle with a glowing arch."""
    wall = [(-900, 0), (-900, -170), (900, -170), (900, 0)]
    _shape(cr, wall, FORT2, 6, smooth=False, holes=(12, 20, 2.4))
    for k in range(30):
        x = -890 + 60 * k
        _shape(cr, [(x, -170), (x, -200), (x + 34, -200), (x + 34, -170)], FORT2, 3, smooth=False)
    for x, h, w in ((-760, 330, 110), (-520, 280, 100), (-300, 360, 120), (300, 360, 120), (520, 280, 100),
                    (760, 330, 110)):
        _shape(cr, [(x - w / 2, 0), (x - w / 2, -h), (x + w / 2, -h), (x + w / 2, 0)], FORT, 5, smooth=False,
               holes=(10, 18, 2.2))
        cr.new_path()
        cr.arc(x, -h, w / 2, math.pi, 2 * math.pi)
        cr.close_path()
        leather(cr, FORT2, 4)
        ink(cr, [(x, -h - w / 2), (x, -h - w / 2 - 70)], 3.5)
        _shape(cr, [(x, -h - w / 2 - 70), (x + 50, -h - w / 2 - 56), (x, -h - w / 2 - 42)], RED, 2.5, smooth=False)
        punch(cr, [(x, -h * 0.6), (x, -h * 0.35)], 8)
    gate = [(-200, 0), (-200, -420), (-120, -500), (120, -500), (200, -420), (200, 0)]
    _shape(cr, gate, FORT, 6, smooth=False, holes=(12, 20, 2.4))
    for sx in (-1, 1):
        _shape(cr, [(sx * 200, 0), (sx * 200, -560), (sx * 280, -560), (sx * 280, 0)], FORT2, 5, smooth=False)
        cr.new_path()
        cr.arc(sx * 240, -560, 40, math.pi, 2 * math.pi)
        cr.close_path()
        leather(cr, GOLD, 3)
    band(cr, [(-200, -420), (200, -420)], 18, GOLD, spacing=12, hole_r=2.2)
    cr.new_path()
    cr.move_to(-110, 0)
    cr.line_to(-110, -250)
    cr.arc(0, -250, 110, math.pi, 2 * math.pi)
    cr.line_to(110, 0)
    cr.close_path()
    cr.set_source_rgb(*INK)
    cr.set_line_width(8)
    cr.stroke_preserve()
    cr.save()
    cr.set_operator(0)
    cr.fill()
    cr.restore()


register("yb_yamapura", (-920, -720, 920, 10), _yamapura)


def _kadhai(cr):
    """A kadhai (a deep iron frying pan) with two ring handles, full of golden ghee (pivot at the bottom)."""
    for sx in (-1, 1):
        cr.new_path()
        cr.arc(sx * 250, -150, 34, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.set_line_width(16)
        cr.stroke()
        cr.arc(sx * 250, -150, 34, 0, 2 * math.pi)
        cr.set_source_rgb(*IRON)
        cr.set_line_width(8)
        cr.stroke()
    pan = [(-240, -170), (-200, -80), (-120, -20), (0, 0), (120, -20), (200, -80), (240, -170)]
    _shape(cr, pan, (0.30, 0.28, 0.30), 6, holes=(12, 20, 2.4))
    cr.new_path()
    ell(cr, 0, -170, 240, 34)
    leather(cr, GHEE, 5)
    cr.new_path()
    ell(cr, -40, -176, 120, 12)
    cr.set_source_rgb(1.0, 0.94, 0.66)
    cr.fill()


register("yb_kadhai", (-300, -220, 300, 10), _kadhai)
