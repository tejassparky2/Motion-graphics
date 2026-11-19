"""The leather cast and props for the Nahusha reel (videos/nahusha.py), in the Togalu Gombeyaata style of the earlier
reels: profile figures with big almond eyes, perforated garments and jointed limbs. Traditional leather puppets,
modelled on no actor and no film. Every sprite name starts with "nh_".

Cast (one look each, kept the same through the video):
  NAHUSHA   the earthly king made king of heaven: wheat skin, a curled moustache, a tall gold kirita with a violet
            flare, a deep teal dhoti with a gold border, a saffron sash. Faces: calm, proud, laugh, angry, scold,
            shock, shame (arjuna_cast / ruru_cast faces). Seated cross-legged on his palanquin (nh_nahusha_seat).
  THE PYTHON  ruru_cast's old grey-green snake head (white brows) on scenes_ruru's leather snake body, with Nahusha's
            crown (nh_crown) on its head, so the viewer always knows who the python is.
Bhima (andhe_cast), Yudhishthira (arjuna_cast), Agastya (six_cast_c, the unnamed angry sage), the bearer sages
(scenes_bhrigu.sage) and Indra (mandhata_cast) come from earlier reels.
Props: the palanquin (nh_palki: a carved seat under a red domed canopy on gold posts, two long poles), the crown
alone (nh_crown) and a sage's angry head (c6_agastya_head_angry).
"""
import math

import andhe_cast as AK
import arjuna_cast as A  # noqa: F401
import mandhata_cast as M
import ravana_cast as R
import ruru_cast as RU
import six_cast_c as C6
from puppet_cast import HAIR, _jewel, _shape, man
from puppet_core import BLUE, BROWN, DRED, GOLD, INK, PALE, RED, SAFFRON, band, holes_line, ink, register

NH_SKIN = (0.92, 0.66, 0.44)
NH_DHOTI = (0.08, 0.42, 0.44)          # deep teal
NH_FLARE = (0.52, 0.22, 0.66)          # violet
WOOD = (0.56, 0.32, 0.14)
WOOD2 = (0.40, 0.22, 0.10)
CANOPY = (0.74, 0.10, 0.10)
CURTAIN = (0.98, 0.80, 0.36)

_NH_O = dict(skin=NH_SKIN, hair=True, moustache=True, tilak=True)
NH_MOODS = ("calm", "smile", "proud", "laugh", "angry", "scold", "shock", "shame")


def nahusha_head(cr, mood="calm"):
    RU.rface(cr, _NH_O, mood)
    ink(cr, [(64, -78), (82, -86), (90, -100)], 4, col=HAIR)                     # the moustache's curled tip
    R.kirita(cr, GOLD, None, tall=1.25, flare=NH_FLARE)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.25, 11, PALE)


NAHUSHA = man("nh_nahusha", skin=NH_SKIN, bulk=1.1, dhoti=NH_DHOTI, border=GOLD, pleat=GOLD, sash=SAFFRON, neck=GOLD,
              crown="tiara", halo=False, moustache=True, hands=("open", "open"))
for _m in NH_MOODS:
    register("nh_nahusha_head" + ("" if _m == "calm" else "_" + _m), (-200, -480, 130, 110),
             (lambda m: lambda cr: nahusha_head(cr, m))(_m))
register("nh_nahusha_seat", (-100, -60, 300, 290), lambda cr: M.seat_legs(cr, NH_SKIN, NH_DHOTI, GOLD, 1.0))  # throne
register("nh_nahusha_cross", (-110, -60, 280, 110), lambda cr: C6.seat_legs(cr, NH_SKIN, NH_DHOTI, GOLD))  # palki
CROSS_H = 96.0                        # cross-legged: the hip sits this far above the seat (design units)
register("c6_agastya_head_angry", (-150, -380, 120, 250), lambda cr: C6.agastya_head(cr, "angry"))


def _crown(cr):
    """Nahusha's crown alone, its base at (0, 0) (for the python's head)."""
    cr.save()
    cr.translate(0, 150)
    R.kirita(cr, GOLD, None, tall=1.25, flare=NH_FLARE)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.25, 11, PALE)
    cr.restore()


register("nh_crown", (-130, -260, 90, 30), _crown)


def _palki(cr):
    """The palanquin, pivot at the middle of its seat floor (0, 0): the poles run at y = +70 from x = -620 to +620."""
    for y0, col in ((52, WOOD2), (70, WOOD)):                                    # the far pole, then the near pole
        p = [(-620, y0 - 14), (620, y0 - 14), (636, y0), (620, y0 + 14), (-620, y0 + 14), (-636, y0)]
        _shape(cr, p, col, 5, smooth=False)
        for x in (-560, 560):
            band(cr, [(x - 16, y0), (x + 16, y0)], 30, GOLD, spacing=10, hole_r=2)
    _shape(cr, [(-200, -360), (-180, -350), (-180, 0), (-200, 0)], GOLD, 4, smooth=False)    # back posts
    _shape(cr, [(180, -360), (200, -350), (200, 0), (180, 0)], GOLD, 4, smooth=False)
    cur = [(-180, -350), (-120, -320), (-150, -200), (-176, -120)]                 # tied-back curtains
    _shape(cr, cur, CURTAIN, 4, holes=(8, 12, 2.2))
    _shape(cr, [(180, -350), (120, -320), (150, -200), (176, -120)], CURTAIN, 4, holes=(8, 12, 2.2))
    dome = [(-250, -350), (-210, -420), (-120, -500), (0, -540), (120, -500), (210, -420), (250, -350)]
    _shape(cr, dome, CANOPY, 6, holes=(12, 16, 3))
    band(cr, [(-250, -352), (250, -352)], 22, GOLD, spacing=13, hole_r=2.6)
    for k in range(9):                                                            # gold scallops along the edge
        x = -224 + 56 * k
        cr.new_path()
        cr.arc(x, -340, 24, 0, math.pi)
        cr.close_path()
        cr.set_source_rgb(*GOLD)
        cr.fill_preserve()
        cr.set_source_rgb(*INK)
        cr.set_line_width(3)
        cr.stroke()
    _shape(cr, [(-14, -540), (0, -600), (14, -540)], GOLD, 4, smooth=False)       # the finial
    _jewel(cr, 0, -606, 12, RED)
    base = [(-236, -10), (236, -10), (250, 30), (220, 92), (-220, 92), (-250, 30)]
    _shape(cr, base, WOOD, 6, smooth=False)
    band(cr, [(-236, -6), (236, -6)], 18, GOLD, spacing=12, hole_r=2.4)
    holes_line(cr, [(-200, 40), (200, 40)], 22, 4)
    for x in (-150, 0, 150):
        _jewel(cr, x, 66, 10, DRED)
    _shape(cr, [(-150, -28), (150, -28), (160, -6), (-160, -6)], (0.86, 0.20, 0.36), 4)   # the cushion
    ink(cr, [(-226, 92), (-236, 128)], 6, col=BROWN)
    ink(cr, [(226, 92), (236, 128)], 6, col=BROWN)


register("nh_palki", (-660, -640, 660, 140), _palki)


# ------------------------------------------------------------------ Bhima's extra faces (andhe_cast has calm, laugh)


def _bhima_head(cr, mood):
    """andhe_cast.bhima_head with ruru_cast's wider set of moods (angry, hurt, shock, smile)."""
    RU.rface(cr, AK._BH_O, mood)
    ink(cr, [(20, -70), (8, -60), (14, -46)], 5, col=HAIR)
    R.kirita(cr, GOLD, None, tall=1.05, flare=BLUE)
    _jewel(cr, 2, -150 + (-282 + 150) * 1.05, 9, RED)


for _m in ("angry", "hurt", "shock", "smile"):
    register("ak_bhima_head_" + _m, (-200, -440, 120, 110), (lambda m: lambda cr: _bhima_head(cr, m))(_m))
