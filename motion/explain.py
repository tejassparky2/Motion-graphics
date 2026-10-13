"""Reference-style kit (owner, 13 Oct 2026: "doesn't even look like explaining inside the human body, refer to the
reference video"). The references (Dr Healthcare Shorts) draw the real anatomy as a flat, clean cut-away (womb with
placenta and cord, esophagus with its veins, an opened knee), put googly eyes and a small mouth on the body part
that talks, tag parts with small white labels, then cut to the masked doctor and the patient in bed.

This module holds the shared pieces: the googly face, and the clean-style explanation cards (Step 1/2/3, Do this,
See a doctor, stamps) used in the doctor's part. Step and tip cards sit in screen space at y about 690, over the bed
sheet: below the faces and above the captions.
"""
import math

from motion.engine import INK, WHITE, at, blob, cue, ease_out, hexc, line, rrect_pts, seg, shape, text_width, write
from videos.kidney_donor import eyes, mouth

RED, GREEN, BLUE, PURPLE, GOLD = hexc("#d8363a"), hexc("#3fae5c"), hexc("#2f7fd6"), hexc("#7a5bd0"), hexc("#f2b632")
STEP_COLS = [BLUE, PURPLE, RED]


def googly(cr, t, x, y, s, mood="calm", talking=False, look=0.0, mouth_dy=34):
    """The reference look: big white googly eyes with black pupils and a small mouth, on the body part itself."""
    eyes(cr, x, y, s, mood, look, blink=(int(t * 10 + x) % 43 == 0))
    mouth(cr, x, y + mouth_dy * s, 0.8 * s, mood, talking, t)


def _pop(t, start, end=None, dur=0.3):
    if t < start or (end is not None and t > end + 0.2):
        return 0.0
    k = 0.85 + 0.15 * ease_out(seg(t, start, start + dur))
    a = min(1.0, (t - start) / 0.12)
    if end is not None and t > end:
        a *= 1 - seg(t, end, end + 0.2)
    return k if a > 0.02 else 0.0


def step_card(cr, t, start, n, text, end=None, y=690):
    """White 'STEP n' card with a coloured number badge (screen space)."""
    k = _pop(t, start, end)
    if not k:
        return
    col = STEP_COLS[(n - 1) % 3]
    cr.save()
    cr.identity_matrix()
    with at(cr, 360, y, k):
        shape(cr, rrect_pts(-320, -70, 640, 140, 22, 16), WHITE, seed=3000, amp=0, lw=4)
        blob(cr, -250, 0, 52, 52, col, seed=3001, amp=0, lw=4)
        write(cr, [(str(n), WHITE)], -250, 22, 60, align="center", bold=True)
        write(cr, [(f"STEP {n}", col)], -180, -18, 30, bold=True)
        size = 30
        w = text_width(cr, [(text, INK)], size)
        size *= min(1.0, 470 / max(1, w))
        write(cr, [(text, INK)], -180, 32, size)
    cr.restore()
    cue("pop", t, start)


def tip_card(cr, t, start, text, kind="ok", end=None, y=690):
    """'DO THIS' (green) or 'SEE A DOCTOR IF' (red) card (screen space)."""
    k = _pop(t, start, end)
    if not k:
        return
    col, head = (GREEN, "DO THIS") if kind == "ok" else (RED, "SEE A DOCTOR IF")
    cr.save()
    cr.identity_matrix()
    with at(cr, 360, y, k):
        shape(cr, rrect_pts(-320, -76, 640, 152, 22, 16), WHITE, seed=3010, amp=0, lw=4)
        shape(cr, rrect_pts(-320, -76, 640, 56, 22, 16), col, seed=3011, amp=0, lw=4)
        write(cr, [(head, WHITE)], 0, -34, 34, align="center", bold=True)
        size = 32
        w = text_width(cr, [(text, INK)], size)
        size *= min(1.0, 600 / max(1, w))
        write(cr, [(text, INK)], 0, 44, size, align="center")
    cr.restore()
    cue("pop", t, start)


def stamp(cr, t, start, text, x=360, y=300, col=RED, size=56, end=None):
    """A red rubber stamp that slams down (screen space)."""
    if t < start or (end is not None and t > end):
        return
    u = seg(t, start, start + 0.18)
    k = 1.6 - 0.6 * ease_out(u)
    cr.save()
    cr.identity_matrix()
    with at(cr, x, y, k, rot=-0.1):
        w = text_width(cr, [(text, col)], size, bold=True) + 50
        shape(cr, rrect_pts(-w / 2, -size * 0.85, w, size * 1.3, 12, 16), hexc("#ffffff", 0.85), seed=3020, amp=0,
              lw=6, stroke=col)
        write(cr, [(text, col)], 0, size * 0.25, size, align="center", bold=True)
    cr.restore()
    cue("hit", t, start)


def sign(cr, t, start, text, x=360, y=300, col=GOLD, size=60, end=None):
    """A chunky coloured sign with white text (screen space), e.g. "HIC!"."""
    k = _pop(t, start, end, 0.25)
    if not k:
        return
    cr.save()
    cr.identity_matrix()
    with at(cr, x, y, k * (1 + 0.04 * math.sin(t * 9)), rot=-0.04):
        w = text_width(cr, [(text, WHITE)], size, bold=True) + 50
        shape(cr, rrect_pts(-w / 2, -size * 0.8, w, size * 1.25, 18, 16), col, seed=3030, amp=0, lw=5)
        write(cr, [(text, WHITE)], 0, size * 0.28, size, align="center", bold=True)
    cr.restore()


def zap(cr, x, y, s=1.0, col=GOLD):
    """A small lightning spark (nerve signal)."""
    from motion.engine import sharp_shape
    with at(cr, x, y, s):
        sharp_shape(cr, [(-10, -36), (16, -6), (2, -2), (14, 30), (-18, -4), (-2, -8)], col, seed=3040, amp=0,
                    lw=3)


def along(pts, u):
    u = min(1.0, max(0.0, u))
    f = u * (len(pts) - 1)
    i = min(len(pts) - 2, int(f))
    a, b = pts[i], pts[i + 1]
    return a[0] + (b[0] - a[0]) * (f - i), a[1] + (b[1] - a[1]) * (f - i)


def vessel(cr, pts, w, col, seed=0):
    """A tube (artery, nerve, vein): outline, fill, light core."""
    line(cr, pts, w + 6, INK, seed=seed, amp=0)
    line(cr, pts, w, col, seed=seed + 1, amp=0)
    line(cr, pts, max(2, w * 0.3), hexc("#ffffff", 0.35), seed=seed + 2, amp=0)
