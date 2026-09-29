"""Reusable sets for story episodes: living room (with couch drawn in two layers so characters look seated),
city street, lottery kiosk. All in world units; call inside a camera (motion.kit.enter_world)."""
from motion import characters as ch
from motion.engine import INK, RED, WHITE, blob, dot, hexc, line, rrect_pts, shape, sharp_shape, write

WALL = hexc("#f1dfbd")
FLOOR = hexc("#c8976a")


def living_room(cr, t, outside=None):
    cr.set_source_rgba(*WALL)
    cr.paint()
    for i in range(-2, 12):   # wallpaper stripes
        x = i * 90
        sharp_shape(cr, [(x, 300), (x + 40, 300), (x + 40, 820), (x, 820)], hexc("#ead3a8"), seed=400 + i, amp=0.6,
                    lw=0, stroke=None)
    sharp_shape(cr, [(-700, 805), (1500, 805), (1500, 1600), (-700, 1600)], FLOOR, seed=401, amp=0.8, lw=4)
    for i in range(8):
        line(cr, [(-600 + i * 260, 830), (-500 + i * 260, 1300)], 3, hexc("#a8784f"), seed=402 + i, amp=1.0)
    # window (night outside)
    shape(cr, rrect_pts(30, 390, 230, 270, 12, 18), hexc("#6b4a2e"), seed=410, amp=0.6, lw=4)
    cr.save()
    cr.rectangle(46, 406, 198, 238)
    cr.clip()
    cr.set_source_rgba(*hexc("#1f2a52"))
    cr.paint()
    blob(cr, 200, 450, 22, 22, hexc("#fff3c4"), seed=411, amp=0.5, lw=2.5)
    for i, (sx, sy) in enumerate([(80, 440), (130, 470), (170, 420), (95, 520)]):
        dot(cr, sx, sy, 3, hexc("#fff3c4"))
    line(cr, [(215, 660), (215, 540)], 6, hexc("#555a66"), seed=412, amp=0.3)   # street lamp
    blob(cr, 215, 536, 12, 8, hexc("#ffe28a"), seed=413, amp=0.3, lw=2.5)
    if outside:
        outside(cr)
    cr.restore()
    line(cr, [(145, 406), (145, 644)], 6, hexc("#6b4a2e"), seed=414, amp=0.3)
    line(cr, [(46, 525), (244, 525)], 6, hexc("#6b4a2e"), seed=415, amp=0.3)
    for cx0 in (18, 240):   # curtains
        shape(cr, [(cx0, 380), (cx0 + 34, 380), (cx0 + 40, 680), (cx0 - 4, 680)], hexc("#c0504d"), seed=416 + cx0,
              amp=1.0, lw=3.5)
    # framed picture: a tiny pumpkin, a nod to episode 1
    shape(cr, rrect_pts(330, 420, 120, 100, 6, 16), hexc("#8e4a1e"), seed=420, amp=0.5, lw=4)
    sharp_shape(cr, [(342, 432), (438, 432), (438, 508), (342, 508)], hexc("#fff3c4"), seed=421, amp=0.4, lw=2.5)
    ch.pumpkin(cr, 390, 500, 20, seed=422)
    # floor lamp
    line(cr, [(700, 590), (700, 860)], 7, INK, seed=430, amp=0.3)
    shape(cr, [(655, 590), (745, 590), (725, 530), (675, 530)], hexc("#ffd23f"), seed=431, amp=0.6, lw=3.5)
    blob(cr, 700, 865, 34, 8, INK, seed=432, amp=0.3, lw=0, stroke=None)


def couch_back(cr):
    shape(cr, rrect_pts(110, 640, 540, 180, 40, 22), hexc("#2f7f86"), seed=440, amp=1.0, lw=4)
    for x0 in (120, 390):
        shape(cr, rrect_pts(x0, 660, 250, 120, 30, 20), hexc("#3a939b"), seed=441 + x0, amp=0.8, lw=3)


def couch_front(cr):
    shape(cr, rrect_pts(100, 800, 560, 90, 22, 22), hexc("#2a6f75"), seed=450, amp=1.0, lw=4)
    for x0 in (72, 630):
        shape(cr, rrect_pts(x0, 720, 64, 180, 26, 16), hexc("#2f7f86"), seed=451 + x0, amp=0.8, lw=4)
    for x0 in (130, 630):
        line(cr, [(x0, 890), (x0 + 6, 915)], 7, INK, seed=452 + x0, amp=0.3)


def street(cr, t):
    cr.set_source_rgba(*hexc("#b5553c"))
    cr.paint()
    for row in range(14):
        y = 300 + row * 40
        off = 40 if row % 2 else 0
        line(cr, [(-600, y), (1400, y)], 2.5, hexc("#8c3f2b"), seed=500 + row, amp=0.8)
        for k in range(-8, 18):
            x = k * 80 + off
            line(cr, [(x, y), (x, y + 40)], 2.5, hexc("#8c3f2b"), seed=520 + row * 30 + k, amp=0.5)
    sharp_shape(cr, [(-700, 830), (1500, 830), (1500, 1600), (-700, 1600)], hexc("#9a958a"), seed=560, amp=0.8, lw=4)
    line(cr, [(-700, 870), (1500, 870)], 3, hexc("#7b776d"), seed=561, amp=1.0)
    line(cr, [(90, 840), (90, 380)], 9, INK, seed=562, amp=0.3)   # lamp post
    shape(cr, [(60, 380), (120, 380), (110, 340), (70, 340)], hexc("#555a66"), seed=563, amp=0.4, lw=3.5)


def kiosk(cr, t, jackpot_at):
    cr.set_source_rgba(*hexc("#3f6fb5"))
    cr.paint()
    sharp_shape(cr, [(-700, 830), (1500, 830), (1500, 1600), (-700, 1600)], hexc("#9a958a"), seed=600, amp=0.8, lw=4)
    shape(cr, rrect_pts(390, 450, 290, 90, 14, 18), RED, seed=601, amp=0.8)
    write(cr, [("LOTTO", WHITE)], 535, 515, 64, align="center", bold=True)
    shape(cr, rrect_pts(410, 560, 250, 110, 10, 18), hexc("#1d1b24"), seed=602, amp=0.6)
    if t < jackpot_at:
        write(cr, [("JACKPOT", hexc("#ffd23f"))], 535, 630, 44, align="center", bold=True)
    else:
        on = int((t - jackpot_at) * 8) % 2 == 0
        write(cr, [("$10,000,000", hexc("#ffd23f") if on else hexc("#ff8a3d"))], 535, 632, 40, align="center",
              bold=True)
    sharp_shape(cr, [(380, 700), (690, 700), (690, 850), (380, 850)], hexc("#d9a15a"), seed=603, amp=0.8, lw=4)
    line(cr, [(380, 740), (690, 740)], 3, hexc("#8e4a1e"), seed=604, amp=0.6)


