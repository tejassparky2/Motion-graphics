"""Body Facts clean style (from the owner's two reference Shorts): the doctor's room (a plain olive wall with a
rail, a masked doctor, patients in blue shirts sitting up in bed under white sheets), white anatomy tags with a
pointer line, and a faint channel watermark. World units unless noted; call inside a camera."""
import math

from motion.characters import person
from motion.engine import INK, WHITE, at, blob, cairo, hexc, line, rrect_pts, shape, text_width, write

WALL, WALL_LOW, RAIL = hexc("#b8c48f"), hexc("#a8b57d"), hexc("#8f6f4c")
SHEET, SHEET_D = hexc("#f7f8fa"), hexc("#d5dbe3")

# Medium shot like the references: big characters, the bed sheet across the front hiding everyone below the waist.
DOC = (190, 900, 2.8)           # the doctor: x, feet y (hidden), scale
BED_A = (545, 960, 2.6)         # first patient, sitting up in bed
BED_B = (1010, 960, 2.6)        # second patient, in the next bed (off to the right)
TWO_SHOT = (1.15, 365, 760)     # camera: doctor + first patient
NEXT_BED = (1.0, 780, 760)      # camera: both patients
DOC_CLOSE = (1.2, 245, 680)
A_CLOSE = (1.3, 545, 700)
B_CLOSE = (1.3, 1010, 700)


def room(cr):
    cr.set_source_rgba(*WALL)
    cr.rectangle(-900, -900, 3200, 3200)
    cr.fill()
    cr.set_source_rgba(*WALL_LOW)
    cr.rectangle(-900, 662, 3200, 3000)
    cr.fill()
    shape(cr, rrect_pts(-900, 638, 3200, 26, 4, 40), RAIL, seed=900, amp=0, lw=3)


def sheet(cr):
    """White bed sheet across the front of the frame (both beds), drawn after the people."""
    shape(cr, [(-400, 860), (60, 842), (300, 872), (560, 835), (820, 866), (1100, 838), (1500, 860), (1500, 1700),
               (-400, 1700)], SHEET, seed=903, amp=0, lw=3.5)
    for k in range(9):   # folds
        x0 = -60 + 170 * k
        line(cr, [(x0, 900 + 24 * (k % 2)), (x0 + 60, 990), (x0 + 40, 1110)], 3, SHEET_D, seed=904 + k, amp=0)


def bed(cr, x):
    """Headboard and pillow behind a patient (draw before them; the sheet goes on last)."""
    shape(cr, rrect_pts(x - 110, 360, 330, 540, 34, 30), hexc("#e6e9ee"), seed=901, amp=0, lw=3.5)
    blob(cr, x + 70, 610, 150, 84, WHITE, seed=902, amp=0, lw=3.5)


def patient(cr, who, x, y, s, t, facing=-1, eyes="dot", mouth="smile", arms=("hold", "down"), talking=False,
            sweat=False):
    if talking:
        mouth = "o" if int(t * 12) % 2 else "smile"
    person(cr, who, x, y, t, facing=facing, eyes=eyes, mouth=mouth, arms=arms, scale=s, sweat=sweat)


def doctor(cr, t, eyes="dot", arms=("hold", "hip"), talking=False, facing=1):
    x, y, s = DOC
    puff = abs(math.sin(t * 11)) if talking else 0.0
    person(cr, "doctor", x, y, t, facing=facing, eyes=eyes, mouth="flat", arms=arms, scale=s, mask=puff)


def label(cr, text, x, y, px=None, py=None, size=26):
    """White anatomy tag at (x, y) (its centre), with a pointer line to (px, py), like the references' labels."""
    w = text_width(cr, [(text, INK)], size) + 22
    h = size * 1.35
    if px is not None:
        line(cr, [(x, y + h / 2 - 2), (px, py)], 2.5, INK, seed=910, amp=0)
    shape(cr, rrect_pts(x - w / 2, y - h / 2, w, h, 5, 20), WHITE, seed=911, amp=0, lw=3)
    write(cr, [(text, INK)], x, y + size * 0.38, size, align="center")


def watermark(cr, logo=True, name=None):
    """The channel's corner logo, plus its name faint across the frame (deters re-uploads, like the references).
    Screen space; every doctor-channel video calls this last in its frame function. Videos made before the logo
    (owner: logo from new videos on, not old ones) pass logo=False, name="Body Facts" so re-renders look the same."""
    from motion.doc_brand import CHANNEL, corner_logo
    name = name or CHANNEL
    cr.save()
    cr.identity_matrix()
    for x, y in ((190, 470), (520, 760)):
        with at(cr, x, y, 1.0, rot=0.38):
            cr.select_font_face("Anton", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
            cr.set_font_size(30)
            wd = cr.text_extents(name).x_advance
            cr.move_to(-wd / 2, 0)
            cr.set_source_rgba(1, 1, 1, 0.22)
            cr.show_text(name)
    cr.restore()
    if logo:
        corner_logo(cr)


def ward(cr, t, tl, keys, mike, danny, doc, dur=0.25):
    """The doctor's room with Mike (bed A) and Danny (bed B): camera, set, people and sheet. `mike`, `danny` and
    `doc` are the keyword moods for patient()/doctor() at time t; who's talking comes from the timeline."""
    from motion.kit import camera, enter_world, set_camera
    set_camera(camera(t, keys, dur=dur))
    enter_world(cr)
    room(cr)
    (xa, ya, sa), (xb, yb, sb) = BED_A, BED_B
    bed(cr, xa)
    bed(cr, xb)
    patient(cr, "mike_b", xa, ya, sa, t, talking=tl.speaking("mike", t), **mike)
    patient(cr, "danny_b", xb, yb, sb, t, talking=tl.speaking("danny", t), **danny)
    doctor(cr, t, talking=tl.speaking("doctor", t), **doc)
    sheet(cr)
