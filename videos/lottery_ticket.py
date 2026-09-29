"""Episode 5: "The 40-Year Lottery Ticket" — an original twist story.

For 40 years an old man buys a $5 lottery ticket every day and never wins. On his 80th birthday the shop owner
hands him a check for $800,000: he never sent the tickets in, he invested the money instead.

Math (checked): $5 x 365 x 40 = $73,000 paid in. Yearly deposits growing 10%/year for 40 years = $807,731
("about $800,000"; daily compounding would give more). The 10% is an illustrative long-run stock-market figure,
stated as an assumption in the description.
"""
import math

from motion.captions import captions
from motion.characters import dollar, person, ticket
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, confetti, enter_world, fly, hl, set_camera, stamp, whip

NARRATOR = dict()

SCRIPT = [
    dict(id="l1", scene="shop",
         text="For forty years, this old man bought a lottery ticket every single day. [Five dollars.|$5.] "
              "He never won. Not once."),
    dict(id="l2", scene="shop", text="On his eightieth birthday, the shop owner hands him an envelope."),
    dict(id="l3", scene="check", text="Inside, a check for [eight hundred thousand dollars.|$800,000.]", gap=0.25),
    dict(id="l4", scene="shop2", text="He goes: wait, I finally won?", speaker="oldman", speaker_from="wait", gap=0.25),
    dict(id="l5", scene="shop2", text="The owner smiles. No. You never won. Because I never sent your tickets in.",
         speaker="owner", speaker_from="No"),
    dict(id="l6", scene="graph", text="Every day, I took your five dollars, and invested it instead.", gap=0.25),
    dict(id="l7", scene="graph",
         text="Forty years of five dollars is only [seventy-three thousand.|$73,000.] "
              "Growing about ten percent a year, it became [eight hundred thousand.|$800,000.]"),
    dict(id="l8", scene="shop3", text="The old man stares at him, and says: so you've been stealing my tickets for forty years?",
         speaker="oldman", speaker_from="so", gap=0.25),
    dict(id="l9", scene="shop3", text="Would you be mad, or grateful?", pace=0.95),
]

METADATA = dict(
    title="He Lost the Lottery for 40 Years… Then Got $800,000 😳",
    alt_titles=["The Shop Owner Never Sent His Lottery Tickets In 😳", "$5 a Day for 40 Years = $800,000? 🤯"],
    description="""For 40 years, he bought a $5 lottery ticket every day and never won. Then, on his 80th birthday, the shop owner handed him a check for $800,000… 😳

The twist is in the math: $5 a day for 40 years is $73,000. Invested and growing about 10% a year, it becomes roughly $800,000. (Illustrative — real returns vary. Not financial advice.)

💬 Would you be mad… or grateful?

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#PlotTwist", "#CompoundInterest", "#Storytime"],
    tags=["plot twist", "lottery story", "compound interest", "money story", "investing", "5 dollars a day",
          "twist ending", "storytime", "animated story", "interestingly strange"],
    pinned_comment="Mad or grateful? Be honest 😂👇",
)

SHOP_WALL = hexc("#2e7f86")
GREEN = hexc("#3d8f45")
GOLD = hexc("#f2b632")
OLD_X, OWNER_X = 250, 520


def shop_set(cr, t, pile=0):
    cr.set_source_rgba(*SHOP_WALL)
    cr.paint()
    for k in range(-3, 14):   # wall panels
        line(cr, [(k * 90, 300), (k * 90, 900)], 3, hexc("#27707a"), seed=3000 + k, amp=0.6)
    sharp_shape(cr, [(-800, 900), (1500, 890), (1500, 1800), (-800, 1800)], hexc("#b98a5a"), seed=3001, amp=1, lw=4)
    # shelves with jars behind the counter
    for r, y in enumerate((540, 660)):
        shape(cr, rrect_pts(360, y, 330, 14, 4, 18), hexc("#8e4a1e"), seed=3002 + r, amp=0.5, lw=3)
        for k in range(5):
            col = [hexc("#e0487a"), GOLD, hexc("#79b061"), hexc("#4fb3e8"), hexc("#ff8a3d")][(k + r) % 5]
            shape(cr, rrect_pts(372 + k * 64, y - 62, 44, 60, 10, 14), hexc("#e8f4f8", 0.85), seed=3010 + r * 10 + k,
                  amp=0.5, lw=3)
            blob(cr, 394 + k * 64, y - 22, 16, 14, col, seed=3030 + r * 10 + k, amp=0.6, lw=0, stroke=None)
    shape(cr, rrect_pts(390, 330, 270, 80, 14, 18), RED, seed=3050, amp=0.8)
    write(cr, [("LOTTO", WHITE)], 525, 390, 56, align="center", bold=True)
    line(cr, [(420, 330), (420, 250)], 4, INK, seed=3051, amp=0.3)
    line(cr, [(630, 330), (630, 250)], 4, INK, seed=3052, amp=0.3)


def counter(cr, pile=0):
    sharp_shape(cr, [(340, 760), (760, 760), (760, 920), (340, 920)], hexc("#d9a15a"), seed=3060, amp=0.8, lw=4)
    line(cr, [(340, 800), (760, 800)], 3, hexc("#8e4a1e"), seed=3061, amp=0.6)
    for k in range(pile):   # the growing pile of losing tickets
        with at(cr, 380 + (k * 37) % 150, 752 - (k // 5) * 10, 0.28, rot=((k * 13) % 7 - 3) * 0.08):
            ticket(cr, 0, 0, 1.0, seed=3070 + k)


def scene_shop(cr, t, tl, part=1):
    A = tl.at
    OLD, OWN, WIDE = (1.9, 280, 800), (1.9, 520, 730), (1.45, 400, 770)
    if part == 1:
        keys = [(0, (1.55, 380, 790)), (A("l1", "old"), OLD), (A("l1", "every"), WIDE),
                (A("l1", "$5"), (2.0, 340, 790)), (A("l1", "never"), (1.7, 330, 800)), (A("l2"), WIDE),
                (A("l2", "birthday"), (1.9, 600, 760)), (A("l2", "owner"), OWN), (A("l2", "envelope"), (1.6, 400, 780))]
    elif part == 2:
        keys = [(A("l4") - 0.2, OLD), (A("l4", "won"), (2.2, 280, 790)), (A("l5"), OWN),
                (A("l5", "never", nth=2), (2.3, 520, 720)), (A("l5", "tickets"), WIDE)]
    else:
        keys = [(A("l8") - 0.2, (1.7, 300, 790)), (A("l8", "says"), OWN), (A("l8", "stealing"), (2.3, 280, 790)),
                (A("l8", "forty"), WIDE), (A("l9"), (1.5, 390, 780)), (A("l9", "grateful"), (1.9, 400, 770))]
    z, fx, fy = camera(t, keys)
    if part == 1 and t < A("l1", "old"):
        z += 0.05 * seg(t, 0, A("l1", "old"))
    set_camera((z, fx, fy))
    enter_world(cr)
    shop_set(cr, t)
    years = int(1 + 39 * seg(t, A("l1", "every"), A("l1", "never"))) if part == 1 else 40
    person(cr, "owner", OWNER_X, 820, t, facing=-1,
           arms=("give", "hip") if part == 1 and t >= A("l2", "hands") else ("hip", "hip"),
           eyes="sly" if part > 1 else "dot", mouth="smirk" if part == 2 else ("o" if part == 3 else "smile"),
           sweat=part == 3)
    counter(cr, pile=min(20, years // 2) if part == 1 else 20)
    # daily $5 in the montage
    buying = part == 1 and A("l1", "every") <= t < A("l1", "never")
    s = dict(facing=1, arms=("give", "hip") if buying else ("hip", "hip"), item="note5" if buying else None,
             eyes="dot", mouth="smile")
    if part == 1 and t >= A("l1", "never"):
        s.update(eyes="sad", mouth="sad")
    if part == 1 and t >= A("l2", "birthday"):
        s.update(eyes="happy", mouth="smile")
    if part == 2:
        s.update(eyes="happy" if t < A("l5") else "wide", mouth="grin" if t < A("l5") else "o",
                 jump=abs(math.sin((t - A("l4")) * 8)) * 14 if t < A("l5") else 0)
    if part == 3:
        s.update(eyes="sad" if t < A("l9") else "wide", mouth="wobble" if t < A("l9") else "o",
                 arms=("point", "hip") if t >= A("l8", "stealing") else ("hip", "hip"), shake=1.2 if t >= A("l8", "stealing") else 0)
    if tl.speaking("oldman", t):
        s["mouth"] = "o" if int(t * 12) % 2 else "smile"
    person(cr, "oldman", OLD_X, 900, t, **s)
    if part == 1:
        # birthday cake with an 80
        ck = pop(t, A("l2", "birthday"), 0.3)
        if ck > 0:
            with at(cr, 640, 760, ck):
                shape(cr, rrect_pts(-60, -60, 120, 60, 12, 16), hexc("#f4efe1"), seed=3100, amp=0.6, lw=3.5)
                shape(cr, rrect_pts(-60, -60, 120, 18, 8, 16), hexc("#e0487a"), seed=3101, amp=0.6, lw=3)
                write(cr, [("80", RED)], 0, -84, 40, align="center", bold=True)
                blob(cr, 0, -112, 6, 10, GOLD, seed=3102, amp=0.4, lw=2)
        # the envelope passing across
        fly(cr, t, A("l2", "envelope") - 0.2, 0.45, (470, 760), (300, 740),
            lambda x, y: shape(cr, rrect_pts(x - 40, y - 26, 80, 52, 4, 10), WHITE, seed=3110, amp=0.4, lw=3), height=60)
        hl(cr, t, [("40 YEARS", RED)], 215, 78, A("l1", "forty"), end=A("l1", "every") - 0.05, bold=True)
        if A("l1", "every") <= t < A("l1", "never"):
            cr.save()
            cr.identity_matrix()
            write(cr, [("year ", INK), (str(years), RED)], W / 2, 215, 72, align="center", bold=True,
                  halo=hexc("#fbf3e1", 0.92))
            cr.restore()
        hl(cr, t, [("Never won.", RED)], 215, 76, A("l1", "never"), end=A("l2") - 0.05, bold=True)
        hl(cr, t, [("80th", RED), (" birthday", INK)], 215, 70, A("l2", "eightieth"), bold=True)
    elif part == 2:
        hl(cr, t, [("\"I WON?!\"", GREEN)], 215, 80, A("l4", "won"), end=A("l5") - 0.05, bold=True)
        hl(cr, t, [("never ", INK), ("sent", RED), (" them in", INK)], 215, 66, A("l5", "sent"), bold=True)
    else:
        hl(cr, t, [("STEALING", RED), (" my tickets?!", INK)], 215, 62, A("l8", "stealing"), end=A("l9") - 0.05, bold=True)
        hl(cr, t, [("mad", RED), (" or ", INK), ("grateful", GREEN), ("?", INK)], 215, 74, A("l9", "mad"), bold=True,
           underline=True)


def scene_check(cr, t, tl):
    A = tl.at
    big = A("l3", "$800,000")
    cr.set_source_rgba(*hexc("#e9d3ae"))
    cr.paint()
    z = camera(t, [(A("l3") - 0.2, (1.0,)), (A("l3", "check"), (1.12,)), (big, (1.3,))])[0]
    with at(cr, 360, 640, z, rot=-0.05):
        shape(cr, rrect_pts(-300, -150, 600, 300, 10, 24), hexc("#e8f4ec"), seed=3200, amp=0.8, lw=4)
        for k in range(6):
            line(cr, [(-290, -140 + k * 56), (290, -140 + k * 56)], 1.5, hexc("#cfe6d6"), seed=3201 + k, amp=0.3)
        write(cr, [("PAY TO THE ORDER OF:", INK)], -270, -80, 24, bold=True)
        write(cr, [("the man who never won", hexc("#3f6fb5"))], -270, -40, 30)
        shape(cr, rrect_pts(40, -20, 230, 60, 6, 16), WHITE, seed=3210, amp=0.5, lw=3)
        if t >= big:
            write(cr, [("$800,000.00", GREEN)], 155, 22, 38, align="center", bold=True)
        line(cr, [(-270, 90), (-40, 90)], 2.5, INK, seed=3220, amp=0.3)
        line(cr, [(-250, 80), (-210, 60), (-180, 86), (-140, 58), (-100, 84), (-60, 70)], 3, hexc("#3f6fb5"),
             seed=3221, amp=0.6)   # signature scribble
    if t >= big:
        confetti(cr, t, big)
    cue("kaching", t, big)
    hl(cr, t, [("$800,000", GREEN)], 250, 100, big, bold=True, underline=True)


def scene_graph(cr, t, tl):
    """Growth of $5/day at ~10%/yr, against the $73,000 actually paid in."""
    A = tl.at
    cr.set_source_rgba(*hexc("#fbf3e1"))
    cr.paint()
    z, fx, fy = camera(t, [(A("l6") - 0.2, (1.25, 250, 780)), (A("l6", "took"), (1.5, 200, 820)),
                           (A("l6", "five"), (1.2, 300, 700)), (A("l6", "invested"), (1.0, 360, 640)),
                           (A("l7", "$73,000"), (1.3, 520, 760)), (A("l7", "ten"), (1.0, 360, 640)),
                           (A("l7", "$800,000"), (1.15, 460, 600))])
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    # graph paper, so every camera move reads on screen
    cr.set_line_width(1.5)
    cr.set_source_rgba(*hexc("#bcd3e0", 0.8))
    for k in range(-20, 50):
        cr.move_to(k * 40, -400)
        cr.line_to(k * 40, 1800)
        cr.move_to(-800, k * 40)
        cr.line_to(2000, k * 40)
    cr.stroke()
    cr.set_line_width(3)
    cr.set_source_rgba(*hexc("#9fc0d2", 0.9))
    for k in range(-4, 11):
        cr.move_to(k * 200, -400)
        cr.line_to(k * 200, 1800)
        cr.move_to(-800, k * 200)
        cr.line_to(2000, k * 200)
    cr.stroke()
    x0, y0, w, h = 90, 400, 560, 470
    cr.set_source_rgba(*INK)
    cr.set_line_width(4)
    cr.move_to(x0, y0)
    cr.line_to(x0, y0 + h)
    cr.line_to(x0 + w, y0 + h)
    cr.stroke()
    write(cr, [("years", INK)], x0 + w, y0 + h + 36, 26, align="right")
    write(cr, [("0", INK)], x0, y0 + h + 36, 24, align="center")
    write(cr, [("40", INK)], x0 + w - 10, y0 + h + 36, 24, align="center")
    fv_max = 5 * 365 * ((1.10 ** 40 - 1) / 0.10)
    paid_y = y0 + h - 73000 / fv_max * h
    grow = seg(t, A("l6", "invested"), A("l7", "$800,000", end=True))
    # paid-in line (straight) and the invested curve
    n = int(40 * min(1.0, grow)) + 1
    cr.set_source_rgba(*hexc("#8a8a8a"))
    cr.set_dash([10, 8])
    cr.set_line_width(4)
    cr.move_to(x0, y0 + h)
    cr.line_to(x0 + w * min(1.0, grow), y0 + h - (73000 * min(1.0, grow)) / fv_max * h)
    cr.stroke()
    cr.set_dash([])
    pts = []
    for yr in range(n):
        v = 5 * 365 * ((1.10 ** yr - 1) / 0.10)
        pts.append((x0 + w * yr / 40, y0 + h - v / fv_max * h))
    if len(pts) > 1:   # filled area under the growth curve: big, bold change as it grows
        cr.move_to(x0, y0 + h)
        for px, py in pts:
            cr.line_to(px, py)
        cr.line_to(pts[-1][0], y0 + h)
        cr.close_path()
        cr.set_source_rgba(*hexc("#79b061", 0.55))
        cr.fill()
    cr.set_source_rgba(*GREEN)
    cr.set_line_width(7)
    for i, (px, py) in enumerate(pts):
        cr.line_to(px, py) if i else cr.move_to(px, py)
    cr.stroke()
    # milestone tags pop on as the curve passes years 10/20/30/40 (values from the same formula)
    t0, t1 = A("l6", "invested"), A("l7", "$800,000", end=True)
    for yr, label in ((10, "$29K"), (20, "$105K"), (30, "$300K"), (40, "$808K")):
        tc = t0 + (t1 - t0) * yr / 40
        sc = pop(t, tc, 0.3)
        if sc > 0:
            v = 5 * 365 * ((1.10 ** yr - 1) / 0.10)
            px, py = x0 + w * yr / 40, y0 + h - v / fv_max * h
            dot(cr, px, py, 9, GREEN)
            with at(cr, px - 10, py - 34, sc):
                shape(cr, rrect_pts(-62, -30, 124, 48, 12, 14), WHITE, seed=3400 + yr, amp=0.6, lw=3.5)
                write(cr, [(label, GREEN)], 0, 8, 32, align="center", bold=True)
            cue("pop", t, tc)
    if grow > 0:   # big year counter riding the curve
        yr = min(40, max(1, int(40 * grow)))
        write(cr, [("year ", INK), (str(yr), RED)], x0 + 150, y0 + 80, 56, align="center", bold=True)
    # $5 bills dropping into the chart during 'every day'
    for k in range(8):
        fly(cr, t, A("l6", "took") + k * 0.18, 0.55, (120 + k * 60, 250), (140 + k * 55, y0 + h - 30),
            lambda x, y, k=k: dollar(cr, x, y, 0.8, seed=3300 + k), height=60)
    if t >= A("l7", "$73,000"):
        write(cr, [("$73,000 paid in", hexc("#6b6b6b"))], x0 + w - 10, paid_y - 14, 28, align="right", bold=True)
    hl(cr, t, [("$5 a day", GREEN), (" -> invested", INK)], 215, 60, A("l6", "invested"), end=A("l7") - 0.05, bold=True)
    hl(cr, t, [("$73,000", hexc("#6b6b6b")), (" in", INK)], 200, 60, A("l7", "$73,000"), bold=True)
    hl(cr, t, [("$800,000", GREEN), (" out", INK)], 280, 70, A("l7", "$800,000"), bold=True, underline=True)
    hl(cr, t, [("~10%/yr", RED)], 350, 46, A("l7", "ten"), bold=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "shop":
        scene_shop(cr, t, tl, 1)
    elif name == "check":
        scene_check(cr, t, tl)
    elif name == "shop2":
        scene_shop(cr, t, tl, 2)
    elif name == "graph":
        scene_graph(cr, t, tl)
    else:
        scene_shop(cr, t, tl, 3)
    cr.restore()
    captions(cr, t, tl)
