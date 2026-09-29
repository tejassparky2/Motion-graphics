"""Timeline for "The Pumpkin Trick" — an original retelling of the classic speculator parable.

Each scene is a function (cr, t) drawing one frame at scene-local time t (seconds).
"""
import math

from . import characters as ch
from .characters import person, stall, truck, exhaust, bubble, crate, money_pile, pumpkin, cash
from .engine import (CREAM, GROUND, INK, RED, WHITE, W, H, at, blob, cue, ease_in, ease_out, hexc, line,
                     poly_pts, pop, seg, shape, sharp_shape, smooth, lerp, write, write_t)

FEET = 840        # characters stand here
STALL_X, STALL_Y = 470, 820
TRUCK_Y = 1110
SETH_X, RAMU_X = 190, 590
SETH_MOUTH, RAMU_MOUTH = (200, 700), (580, 705)


# ---------------------------------------------------------------- camera
ZOOM, PIVOT, SHIFT = 1.2, (360, 760), 60


def enter_world(cr):
    """Camera for the village set: props and characters are zoomed in; captions (write_t) stay screen-space."""
    cr.translate(PIVOT[0], PIVOT[1] + SHIFT)
    cr.scale(ZOOM, ZOOM)
    cr.translate(-PIVOT[0], -PIVOT[1])


# ---------------------------------------------------------------- shared backdrops
def background(cr, sky=CREAM):
    enter_world(cr)
    cr.set_source_rgba(*sky)
    cr.paint()
    sharp_shape(cr, [(-10, 770), (730, 745), (730, 1290), (-10, 1290)], GROUND, seed=1, amp=0.8, lw=4)
    marks = [(60, 880), (250, 930), (430, 900), (640, 950), (120, 1020), (330, 1060), (560, 1030), (80, 1180),
             (280, 1210), (500, 1170), (660, 1230), (400, 1260)]
    for i, (x, y) in enumerate(marks):
        line(cr, [(x, y), (x + 8, y - 5), (x + 16, y), (x + 24, y - 4)], 2.5, hexc("#8f8a74"), seed=20 + i,
             amp=0.8)


def night(cr, t, start, dur=1.6, label="Next day..."):
    """Dim to night and back, with a moon and a caption. Returns True while active."""
    u = seg(t, start, start + dur)
    if u <= 0 or u >= 1:
        return
    cue("whoosh", t, start, dur)
    a = math.sin(u * math.pi)
    cr.save()
    cr.identity_matrix()
    cr.set_source_rgba(0.09, 0.08, 0.2, 0.85 * a)
    cr.paint()
    cr.push_group()
    blob(cr, 560, 210, 48, 48, hexc("#fff3c4"), seed=5, amp=0.8, lw=3)
    blob(cr, 585, 195, 44, 44, hexc("#1a1735"), seed=6, amp=0.8, lw=0, stroke=None)
    for i, (sx, sy) in enumerate([(120, 150), (240, 260), (380, 120), (660, 330), (90, 380), (450, 300)]):
        blob(cr, sx, sy, 4, 4, hexc("#fff3c4"), seed=i, amp=0.5, lw=0, stroke=None)
    write(cr, [(label, WHITE)], W / 2, 560, 64, align="center", bold=True)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def fly(cr, t, start, dur, p0, p1, draw, height=160):
    """Animate an object along an arc from p0 to p1; returns True once it has landed."""
    u = seg(t, start, start + dur)
    if u <= 0:
        return False
    if u >= 1:
        return True
    e = smooth(u)
    x = lerp(p0[0], p1[0], e)
    y = lerp(p0[1], p1[1], e) - math.sin(u * math.pi) * height
    draw(x, y, (u - 0.5) * 0.6)
    return False


def price(cr, t, start, amount, y=170, size=58, end=None):
    write_t(cr, [("Per pumpkin = ", INK), (f"₹{amount}", RED)], W / 2, y, size, t, start, end=end,
            align="center")


def truck_slot(i, tx):
    """World position (bottom-centre) of crate slot i on a truck parked at tx (cab on the left)."""
    slots = [(-5, 0), (85, 0), (165, 0), (40, 1), (125, 1)]
    cx, row = slots[i]
    return tx + cx + 20, TRUCK_Y - 80 - row * 56


def drive(t, t_in, t_park, t_out=None, t_gone=None, x_from=900, x_park=380, x_to=-420):
    """Truck x position and wheel angle for an arrive-park-leave move."""
    if t < t_park:
        x = lerp(x_from, x_park, ease_out(seg(t, t_in, t_park)))
    elif t_out is None or t < t_out:
        x = x_park
    else:
        x = lerp(x_park, x_to, ease_in(seg(t, t_out, t_gone)))
    return x, x / 28.0


# ---------------------------------------------------------------- scenes
def s_intro(cr, t):
    background(cr)
    stall(cr, STALL_X, STALL_Y, 1.0)
    person(cr, "ramu", RAMU_X, FEET, t, facing=-1, arms=("hip", "hip"),
           eyes="wide" if t > 3.2 else "dot", mouth="o" if 3.2 < t < 4.4 else "smile")
    wx = lerp(-130, SETH_X, seg(t, 0.4, 3.2))
    walking = 0.4 < t < 3.2
    person(cr, "seth", wx, FEET, t, facing=1, walk=(wx / 95) if walking else None,
           arms=("down", "down") if t < 3.4 else ("down", "hip"), item="briefcase", mouth="smirk")
    write_t(cr, "A rich man comes", W / 2, 150, 54, t, 0.3, end=5.6, align="center")
    write_t(cr, "to the village to buy", W / 2, 218, 54, t, 1.2, end=5.6, align="center")
    write_t(cr, [("PUMPKINS!", RED)], W / 2, 305, 76, t, 2.2, end=5.6, align="center", bold=True, underline=True)


def s_offer(cr, t):
    background(cr)
    stall(cr, STALL_X, STALL_Y, 1.0)
    thumbs = t > 5.9
    person(cr, "seth", SETH_X, FEET, t, facing=1, arms=("thumb" if t > 6.6 else "point", "hip"), mouth="smile"
           if t < 6.6 else "grin")
    person(cr, "ramu", RAMU_X, FEET, t, facing=-1, arms=("thumb" if thumbs else "chin", "hip"),
           eyes="wide" if 4.2 < t < 5.9 else "happy" if thumbs else "dot",
           mouth="grin" if thumbs else "o" if t > 4.2 else "flat", jump=abs(math.sin((t - 5.9) * 7)) * 18
           if 5.9 < t < 6.8 else 0)
    price(cr, t, 0.2, 100, end=3.0)
    if 0.7 < t < 3.1:
        cue("pop", t, 0.7)
        bubble(cr, 250, 520, 330, 96, SETH_MOUTH, [("I'll pay ", INK), ("₹100", RED), (" each!", INK)],
               s=pop(t, 0.7), size=36, progress=seg(t, 0.9, 1.8))
    # Ramu's mental maths
    write_t(cr, [("Market price - ", INK), ("₹70", RED)], W / 2, 150, 50, t, 3.3, align="center")
    write_t(cr, [("Offer - ", INK), ("₹100", RED)], W / 2, 218, 50, t, 4.2, align="center")
    write_t(cr, [("Profit = ", INK), ("₹30 each!", RED)], W / 2, 300, 62, t, 5.0, align="center", bold=True,
            underline=True)


def _stall_to_truck(cr, t, starts, tx, n0):
    """Crates hop from the stall into the truck. Returns number landed."""
    landed = 0
    for i, s in enumerate(starts):
        slot = truck_slot(n0 + i, tx)
        cue("thud", t, s + 0.55)
        done = fly(cr, t, s, 0.55, (STALL_X - 40, STALL_Y - 150), slot,
                   lambda x, y, r, i=i: crate(cr, x, y, 80, 56, seed=300 + n0 + i))
        landed += done
    return landed


def s_first_haul(cr, t):
    background(cr)
    n_fly = [1.8, 2.3, 2.8]
    landed = sum(t >= s + 0.55 for s in n_fly)
    stall(cr, STALL_X, STALL_Y, 1.0 - 0.15 * sum(t >= s for s in n_fly))
    paid = t > 3.4
    if paid:
        cue("kaching", t, 3.4)
    person(cr, "seth", SETH_X, FEET, t, facing=1, arms=("give" if 3.1 < t < 3.6 else "hip", "hip"),
           mouth="smirk")
    person(cr, "ramu", RAMU_X, FEET, t, facing=-1, arms=("cheer" if paid else "hip", "hip"),
           item="cash" if paid else None, eyes="happy" if paid else "dot", mouth="grin" if paid else "smile")
    tx, wheel = drive(t, 0.0, 1.6, 4.6, 6.2)
    cue("engine", t, 0.0, 1.6)
    cue("engine", t, 4.6, 1.6)
    truck(cr, tx, TRUCK_Y, t, crates=landed, wheel=wheel, driver=ch.SKIN_MID)
    if t < 1.6 or t > 4.6:
        exhaust(cr, tx + 210, TRUCK_Y - 40, t)
    _stall_to_truck(cr, t, n_fly, tx, 0)
    write_t(cr, [("Buys ", INK), ("120", RED), (" pumpkins", INK)], W / 2, 160, 54, t, 1.8, align="center")
    write_t(cr, [("₹12,000", RED), (" paid", INK)], W / 2, 235, 54, t, 2.9, align="center")
    night(cr, t, 6.2)


def s_price_300(cr, t):
    background(cr)
    n_fly = [4.4, 4.8, 5.2, 5.6, 6.0]
    landed = sum(t >= s + 0.55 for s in n_fly)
    stall(cr, STALL_X, STALL_Y, max(0.0, 0.55 - 0.11 * sum(t >= s for s in n_fly)))
    greedy = 1.3 < t < 4.2
    paid = t > 6.7
    if paid:
        cue("kaching", t, 6.7)
    person(cr, "seth", SETH_X, FEET, t, facing=1, arms=("point" if t < 3 else "hip", "hip"), mouth="smirk")
    person(cr, "ramu", RAMU_X, FEET, t, facing=-1,
           arms=("rub" if greedy else "cheer" if paid else "hip", "hip"), item="cash_big" if paid else None,
           eyes="wide" if t < 1.3 else "rupee" if greedy or paid else "happy",
           mouth="o" if t < 1.3 else "grin", shake=1.5 if t < 1.3 else 0)
    price(cr, t, 0.3, 300, end=3.6)
    write_t(cr, "The whole village sells!", W / 2, 250, 48, t, 1.6, end=3.6, align="center")
    tx, wheel = drive(t, 2.6, 4.2, 7.0, 8.2)
    cue("engine", t, 2.6, 1.6)
    cue("engine", t, 7.0, 1.2)
    truck(cr, tx, TRUCK_Y, t, crates=landed, wheel=wheel, driver=ch.SKIN_MID)
    if 2.6 < t < 4.2 or t > 7.0:
        exhaust(cr, tx + 210, TRUCK_Y - 40, t)
    _stall_to_truck(cr, t, n_fly, tx, 0)
    write_t(cr, [("Buys ", INK), ("500", RED), (" more", INK)], W / 2, 160, 54, t, 4.4, align="center")
    write_t(cr, [("₹1.5 Lakh", RED), (" paid", INK)], W / 2, 240, 58, t, 5.4, align="center", bold=True)
    night(cr, t, 8.2)


def s_price_1000(cr, t):
    background(cr)
    stall(cr, STALL_X, STALL_Y, 0.0)
    leaving = t > 6.4
    sx = lerp(SETH_X, -160, seg(t, 6.4, 8.0))
    person(cr, "seth", sx, FEET, t, facing=-1 if leaving else 1, walk=(sx / 95) if leaving else None,
           arms=("down", "wave") if leaving else ("point", "hip"), item="briefcase" if leaving else None,
           mouth="grin" if t < 6.4 else "smirk")
    person(cr, "ramu", RAMU_X, FEET, t, facing=-1, arms=("chin", "hip") if t > 1.4 else ("hip", "hip"),
           eyes="sad" if t > 1.4 else "wide", mouth="wobble" if t > 1.4 else "o", sweat=t > 1.4)
    write_t(cr, [("Per pumpkin = ", INK), ("₹1000!!", RED)], W / 2, 175, 62, t, 0.3, align="center", bold=True)
    write_t(cr, "...but there are none left", W / 2, 250, 44, t, 1.4, align="center")
    if 2.4 < t < 4.2:
        cue("pop", t, 2.4)
        bubble(cr, 230, 520, 320, 96, SETH_MOUTH, [("Bring me more!", INK)], s=pop(t, 2.4), size=38,
               progress=seg(t, 2.6, 3.2))
    if 4.3 < t < 6.6:
        cue("pop", t, 4.3)
        bubble(cr, 290, 520, 440, 140, SETH_MOUTH, None, s=pop(t, 4.3), size=34, progress=seg(t, 4.5, 5.6),
               lines=[[("I'm off to the city.", INK)], [("My ", INK), ("assistant", RED), (" will buy.", INK)]])


def s_assistant(cr, t):
    background(cr)
    n_fly = [7.2, 7.5, 7.8, 8.1, 8.4]
    stall(cr, STALL_X, STALL_Y, min(1.0, 0.2 * sum(t >= s + 0.55 for s in n_fly)))
    tx, wheel = drive(t, 0.0, 1.5, 8.9, 10.2, x_park=420)
    cue("engine", t, 0.0, 1.5)
    cue("engine", t, 8.9, 1.3)
    on_truck = 5 - sum(t >= s for s in n_fly)
    # Chotu hops down from the truck and strolls over
    cx = lerp(430, 250, seg(t, 1.5, 2.6))
    if t > 9.0:
        cx = lerp(250, -140, seg(t, 9.0, 10.4))
    walking = 1.5 < t < 2.6 or t > 9.0
    deal = 5.4 < t < 7.2
    got_cash = t > 7.0
    if got_cash:
        cue("kaching", t, 7.0)
    person(cr, "chotu", cx, FEET, t, facing=-1 if t > 9.0 else 1, walk=(cx / 80) if walking else None,
           arms=("point" if 2.8 < t < 5.3 else "hold" if got_cash else "hip", "hip"),
           item="cash_big" if got_cash else None, eyes="sly" if t < 7 else "happy",
           mouth="smirk" if t < 7 else "grin")
    person(cr, "ramu", RAMU_X, FEET, t, facing=-1,
           arms=("give" if 6.3 < t < 7.1 else "rub" if deal else "chin" if t < 5.4 else "hip", "hip"),
           item="cash_big" if 6.3 < t < 7.1 else None,
           eyes="rupee" if t > 5.4 else "wide" if t > 2.8 else "sad", mouth="grin" if t > 5.4 else "flat")
    truck(cr, tx, TRUCK_Y, t, crates=on_truck, wheel=wheel, driver=ch.SKIN_TAN)
    if t < 1.5 or t > 8.9:
        exhaust(cr, tx + 210, TRUCK_Y - 40, t)
    for i, s in enumerate(n_fly):
        slot = truck_slot(4 - i, tx)
        cue("thud", t, s + 0.55)
        fly(cr, t, s, 0.55, slot, (STALL_X - 40, STALL_Y - 150),
            lambda x, y, r, i=i: crate(cr, x, y, 80, 56, seed=304 - i))
    mouth = (cx + 10, 700)
    if 2.8 < t < 5.3:
        cue("pop", t, 2.8)
        bubble(cr, 330, 520, 420, 140, mouth, None, s=pop(t, 2.8), size=34, progress=seg(t, 3.0, 4.2),
               lines=[[("Psst... buy these", INK)], [("from me at ", INK), ("₹700", RED)]])
    if 5.4 < t < 7.3:
        cue("pop", t, 5.4)
        bubble(cr, 330, 520, 420, 140, mouth, None, s=pop(t, 5.4), size=34, progress=seg(t, 5.6, 6.6),
               lines=[[("...and sell them to", INK)], [("my boss at ", INK), ("₹1000!", RED)]])
    write_t(cr, "The village buys back", W / 2, 150, 50, t, 6.2, align="center")
    write_t(cr, [("620", RED), (" pumpkins @ ", INK), ("₹700", RED)], W / 2, 225, 54, t, 7.0, align="center",
            bold=True)


def _chart(cr, t, start):
    """Price history: 70 -> 100 -> 300 -> 1000 -> crash to 50."""
    x0, y0, w, h = 150, 80, 440, 230
    p = seg(t, start, start + 0.5)
    if p <= 0:
        return
    cr.save()
    cr.identity_matrix()
    cr.set_source_rgba(*INK)
    cr.set_line_width(4)
    cr.set_line_join(1)
    cr.set_line_cap(1)
    cr.move_to(x0, y0)
    cr.line_to(x0, y0 + h)
    cr.line_to(x0 + w * p, y0 + h)
    cr.stroke()
    write(cr, "price", x0 - 12, y0 + 20, 26, align="right")
    vals = [70, 100, 300, 1000, 50]
    pts = [(x0 + 20 + i * (w - 40) / 4, y0 + h - 10 - v / 1000 * (h - 30)) for i, v in enumerate(vals)]
    u = seg(t, start + 0.4, start + 2.6) * (len(pts) - 1)
    k = int(u)
    path = pts[:k + 1]
    if k < len(pts) - 1:
        f = u - k
        path.append((lerp(pts[k][0], pts[k + 1][0], f), lerp(pts[k][1], pts[k + 1][1], f)))
    if len(path) > 1:
        cr.set_source_rgba(*RED)
        cr.set_line_width(6)
        cr.set_line_join(1)
        cr.move_to(*path[0])
        for q in path[1:]:
            cr.line_to(*q)
        cr.stroke()
    for i, v in enumerate(vals):
        if u >= i:
            x, y = pts[i]
            blob(cr, x, y, 7, 7, RED, seed=910 + i, amp=0.3, lw=2.5)
            write(cr, f"₹{v}", x, y - 16 if i < 4 else y - 18, 26, align="center", bold=i in (3, 4))
    cr.restore()


def s_crash(cr, t):
    background(cr)
    stall(cr, STALL_X, STALL_Y, 1.0)
    crying = t > 6.8
    look = 0 < t < 3.6
    person(cr, "ramu", RAMU_X - 60, FEET, t, facing=-1,
           arms=("face" if crying else "hip", "face" if crying else "hip"),
           eyes="cry" if crying else "sad" if t > 3.6 else "dot", mouth="sad" if t > 3.6 else "flat",
           tears=crying, lean=math.sin(t * 2) * 0.04 if look else 0)
    write_t(cr, "Days pass...", W / 2, 160, 56, t, 0.6, end=3.5, align="center")
    write_t(cr, "The rich man never returns.", W / 2, 240, 44, t, 1.5, end=3.5, align="center")
    cue("fall", t, 5.6, 0.9)
    if t < 6.6:
        _chart(cr, t, 3.8)
    else:
        price(cr, t, 6.8, 50, y=175)
        write_t(cr, [("Loss: ", INK), ("₹650", RED), (" on each one", INK)], W / 2, 255, 46, t, 7.6,
                align="center")
    night(cr, t, -0.8, 1.6, label="")


def s_city(cr, t):
    cr.set_source_rgba(*hexc("#f5e6c4"))
    cr.paint()
    # skyline
    for i, (x, w, hgt, col) in enumerate([(-20, 130, 420, "#9c8fb8"), (100, 110, 330, "#b3a6c9"),
                                          (470, 120, 380, "#9c8fb8"), (580, 160, 300, "#b3a6c9")]):
        sharp_shape(cr, [(x, 900 - hgt), (x + w, 900 - hgt), (x + w, 900), (x, 900)], hexc(col), seed=700 + i,
                    amp=0.8, lw=3.5)
        for r in range(int(hgt // 60) - 1):
            for c in range(int(w // 40)):
                sharp_shape(cr, [(x + 14 + c * 40, 900 - hgt + 26 + r * 60), (x + 34 + c * 40, 900 - hgt + 26 + r * 60),
                                 (x + 34 + c * 40, 900 - hgt + 56 + r * 60), (x + 14 + c * 40, 900 - hgt + 56 + r * 60)],
                            hexc("#fff3c4"), seed=720 + i * 10 + r + c, amp=0.4, lw=2.5)
    # the rich man's tower
    sharp_shape(cr, [(215, 330), (505, 330), (505, 900), (215, 900)], ch.PURPLE, seed=760, amp=1.0, lw=4)
    shape(cr, [(240, 360), (480, 360), (480, 420), (240, 420)], ch.GOLD, seed=761, amp=0.6, lw=3)
    write(cr, [("SETH & CO.", INK)], 360, 405, 38, align="center", bold=True)
    for r in range(6):
        for c in range(4):
            sharp_shape(cr, [(240 + c * 62, 450 + r * 70), (280 + c * 62, 450 + r * 70),
                             (280 + c * 62, 490 + r * 70), (240 + c * 62, 490 + r * 70)],
                        hexc("#fff3c4"), seed=770 + r * 4 + c, amp=0.4, lw=2.5)
    sharp_shape(cr, [(-10, 900), (730, 890), (730, 1290), (-10, 1290)], hexc("#a9a391"), seed=780, amp=0.8, lw=4)
    rise = ease_out(seg(t, 0.0, 0.8))
    money_pile(cr, 360, 1240 + (1 - rise) * 200, 1.55)
    cue("kaching", t, 0.4)
    laugh = t > 3.4
    person(cr, "seth", 300, 1040 + (1 - rise) * 200, t, facing=1, arms=("cheer" if laugh else "hold", "hip"),
           item="cash_big", mouth="laugh" if laugh else "grin", jump=abs(math.sin(t * 9)) * 6 if laugh else 0)
    person(cr, "chotu", 460, 1060 + (1 - rise) * 200, t, facing=-1, arms=("thumb", "hip"),
           eyes="closed" if laugh else "happy", mouth="laugh" if laugh else "grin",
           jump=abs(math.sin(t * 9 + 1)) * 6 if laugh else 0)
    if laugh:
        cue("laugh", t, 3.4, 2.0)
        for i, (hx, hy) in enumerate([(150, 640), (560, 620), (120, 760)]):
            s = pop(t, 3.5 + i * 0.25)
            if s:
                with at(cr, hx, hy - (t - 3.5) * 8, s, rot=0.2 * (i - 1)):
                    write(cr, [("HA HA!", RED)], 0, 0, 44, align="center", bold=True)
    # the ledger
    shape(cr, [(90, 70), (630, 70), (630, 310), (90, 310)], hexc("#fbf8ef", 0.92), seed=790, amp=1.0, lw=3.5)
    write_t(cr, [("Bought 620 for ", INK), ("₹1.62 L", RED)], W / 2, 135, 44, t, 0.8, align="center")
    write_t(cr, [("Sold 620 for ", INK), ("₹4.34 L", RED)], W / 2, 200, 44, t, 1.7, align="center")
    write_t(cr, [("Profit = ", INK), ("₹2.72 Lakh", RED)], W / 2, 282, 56, t, 2.6, align="center", bold=True,
            underline=True)


def s_moral(cr, t):
    cr.set_source_rgba(*CREAM)
    cr.paint()
    write_t(cr, "When prices rise", W / 2, 330, 62, t, 0.3, align="center")
    write_t(cr, "for no reason...", W / 2, 410, 62, t, 1.2, align="center")
    write_t(cr, "ask who is", W / 2, 540, 70, t, 2.3, align="center", bold=True)
    write_t(cr, [("selling to you.", RED)], W / 2, 630, 78, t, 3.0, align="center", bold=True, underline=True)
    s = pop(t, 3.9, 0.5)
    if s:
        for i, dx in enumerate((-150, 0, 150)):
            b = abs(math.sin(t * 5 + i)) * 26
            with at(cr, W / 2 + dx, 960 - b, s):
                pumpkin(cr, 0, 0, 58, seed=950 + i)
                if i == 1:
                    # a tiny face on the middle pumpkin
                    blob(cr, -16, -56, 6, 8, INK, seed=960, amp=0, lw=0, stroke=None)
                    blob(cr, 18, -56, 6, 8, INK, seed=961, amp=0, lw=0, stroke=None)
                    line(cr, [(-18, -34), (1, -24), (20, -34)], 4.5, INK, seed=962, amp=0.3)
        cue("pop", t, 3.9)
    if t > 5.4:
        cr.set_source_rgba(*CREAM[:3], seg(t, 5.4, 6.0))
        cr.paint()


SCENES = [
    (5.9, s_intro),
    (7.6, s_offer),
    (7.8, s_first_haul),
    (9.8, s_price_300),
    (8.0, s_price_1000),
    (10.4, s_assistant),
    (9.6, s_crash),
    (6.4, s_city),
    (6.0, s_moral),
]


def total_duration():
    return sum(d for d, _ in SCENES)


def scene_at(t):
    """(scene_fn, local_t, scene_start) for global time t."""
    acc = 0.0
    for d, fn in SCENES:
        if t < acc + d:
            return fn, t - acc, acc
        acc += d
    d, fn = SCENES[-1]
    return fn, d - 1e-3, acc - d
