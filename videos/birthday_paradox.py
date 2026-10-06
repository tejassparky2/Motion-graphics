"""Episode 22: "The Birthday Paradox" — 23 people is enough for a better-than-even chance of a shared birthday.

Numbers (365-day year, birthdays equally likely): 23 people -> 50.7%, 30 -> 70.6%, 50 -> 97.0%, 70 -> 99.9%.
23 people make 23 * 22 / 2 = 253 pairs. Ends with a call to test it in the comments, which tends to bring lots of
comments.
"""
import math

from motion.captions import captions
from motion.engine import INK, RED, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, confetti, hl, stamp, whip

NARRATOR = dict(speed=1.0)
TAIL = 0.9

SCRIPT = [
    dict(id="b1", scene="room",
         text="Put just [twenty-three|23] people in a room, and there's a better than [fifty-fifty|50/50] chance "
              "two of them share a birthday."),
    dict(id="b2", scene="calendar",
         text="That sounds wrong. There are [three hundred sixty-five|365] days in a year. "
              "Surely you'd need way more people?"),
    dict(id="b3", scene="you",
         text="Here's the trick. You're not looking for someone with your birthday. Any two people can match."),
    dict(id="b4", scene="pairs",
         text="And [twenty-three|23] people make [two hundred fifty-three|253] different pairs. "
              "That's [two hundred fifty-three|253] chances for a match."),
    dict(id="b5", scene="curve", text="Every pair adds a tiny chance, and they pile up fast."),
    dict(id="b6", scene="curve", text="At [fifty|50] people, it's [ninety-seven percent.|97%.]"),
    dict(id="b7", scene="curve", text="At [seventy,|70,] it's [ninety-nine point nine percent.|99.9%.]"),
    dict(id="b8", scene="class",
         text="So next time you're in a class of [thirty,|30,] bet on it. You'll win about [seven times out of ten.|7 times out of 10.]"),
    dict(id="b9", scene="comments",
         text="Want proof? Drop your birthday in the comments. I bet you'll find a match.", gap=0.2),
]

METADATA = dict(
    title="Only 23 People… and 2 Share a Birthday? 🎂🤯 (Birthday Paradox)",
    alt_titles=["This Math Trick Wins 7 Times Out of 10 🎂", "Why Two People in Your Class Share a Birthday 🤯"],
    description="""Put just 23 people in a room, and there's a better than 50/50 chance two of them share a birthday. 🎂

It sounds impossible with 365 days in a year. The trick: you're not looking for someone with YOUR birthday. Any two people can match, and 23 people make 253 different pairs.

📊 The real numbers:
23 people → 50.7%
30 people → 70.6%
50 people → 97%
70 people → 99.9%

(Assuming 365 equally likely birthdays.)

💬 Test it right now: comment your birthday (just the month and day) and find your twin 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Paradox", "#Math", "#Birthday"],
    tags=["birthday paradox", "birthday problem", "probability", "math paradox", "paradox", "math trick",
          "mind blowing math", "brain teaser", "statistics", "math shorts", "interestingly strange"],
    pinned_comment="Comment your birthday (month + day) and reply if you find your birthday twin 🎂👇",
)

BG = hexc("#1f2a4d")
GRID = hexc("#2b3866")
CREAM = hexc("#f4efe1")
YEL = hexc("#ffd23f")
PINK = hexc("#ff7aa8")
CYAN = hexc("#5fd3f3")
GREEN = hexc("#6fd67a")
SKINS = [hexc(c) for c in ("#f0c29c", "#d9975f", "#e8b48a", "#a8693f", "#f5d0b0", "#c68654")]
SHIRTS = [hexc(c) for c in ("#e0487a", "#4fb3e8", "#79b061", "#f2b51d", "#9b6bd6", "#f08c1a", "#3f6fb5")]

N = 23
MATCH = (4, 15)            # the two who share a birthday
CENTER = (360, 820)
RAD = 260


def seat(i):
    a = -math.pi / 2 + i * 2 * math.pi / N
    return CENTER[0] + RAD * math.cos(a), CENTER[1] + RAD * math.sin(a)


def bg(cr, t, keys, dur=0.14):
    cr.set_source_rgba(*BG)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=dur)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    cr.set_line_width(2)
    cr.set_source_rgba(*GRID)
    for k in range(-20, 40):
        cr.move_to(k * 60, -600)
        cr.line_to(k * 60, 2200)
        cr.move_to(-600, k * 60)
        cr.line_to(1400, k * 60)
    cr.stroke()


def face(cr, x, y, r, i, happy=False, glow=None):
    if glow:
        blob(cr, x, y, r * 1.5, r * 1.5, hexc(glow, 0.35), seed=500 + i, amp=0.5, lw=0, stroke=None)
    blob(cr, x, y + r * 1.15, r * 0.95, r * 0.6, SHIRTS[i % len(SHIRTS)], seed=600 + i, amp=0.4, lw=3)
    blob(cr, x, y, r, r, SKINS[i % len(SKINS)], seed=700 + i, amp=0.4, lw=3)
    dot(cr, x - r * 0.35, y - r * 0.1, max(2, r * 0.12), INK)
    dot(cr, x + r * 0.35, y - r * 0.1, max(2, r * 0.12), INK)
    if happy:
        line(cr, [(x - r * 0.35, y + r * 0.3), (x, y + r * 0.5), (x + r * 0.35, y + r * 0.3)], 3, INK, seed=800 + i,
             amp=0.2)
    else:
        line(cr, [(x - r * 0.25, y + r * 0.38), (x + r * 0.25, y + r * 0.38)], 3, INK, seed=800 + i, amp=0.2)


def cake(cr, x, y, s=1.0):
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-26, -14, 52, 28, 5, 12), PINK, seed=901, amp=0.4, lw=3)
        shape(cr, rrect_pts(-26, -24, 52, 12, 4, 12), CREAM, seed=902, amp=0.4, lw=2.5)
        line(cr, [(0, -24), (0, -40)], 3.5, CYAN, seed=903, amp=0.1)
        blob(cr, 0, -46, 4, 7, YEL, seed=904, amp=0.2, lw=0, stroke=None)


def room(cr, t, start, match_t=None, size=34):
    for i in range(N):
        sc = pop(t, start + i * 0.03, 0.2)
        if sc <= 0:
            continue
        x, y = seat(i)
        m = match_t is not None and t >= match_t and i in MATCH
        with at(cr, x, y, sc):
            face(cr, 0, 0, size, i, happy=m, glow="#ffd23f" if m else None)
            if m:
                cake(cr, 0, -size - 34, 0.9)


def scene_room(cr, t, tl):
    A = tl.at
    keys = [(A("b1") - 0.2, (1.4, 360, 760)), (A("b1", "23"), (0.95, 360, 820)), (A("b1", "room"), (1.1, 360, 800)),
            (A("b1", "better"), (0.95, 360, 820)), (A("b1", "chance"), (1.2, 360, 820)),
            (A("b1", "share"), (1.3, 380, 760)), (A("b1", "birthday."), (1.0, 360, 820))]
    bg(cr, t, keys)
    m = A("b1", "share")
    room(cr, t, 0.0, match_t=m)
    if t >= m:
        (x1, y1), (x2, y2) = seat(MATCH[0]), seat(MATCH[1])
        k = ease_out(seg(t, m, m + 0.35))
        line(cr, [(x1, y1), (lerp(x1, x2, k), lerp(y1, y2, k))], 6, YEL, seed=950, amp=0.6)
        if k >= 1:
            with at(cr, CENTER[0], CENTER[1], pop(t, m + 0.35, 0.25), rot=-0.05):
                shape(cr, rrect_pts(-90, -34, 180, 68, 14, 16), YEL, seed=951, amp=0.4, lw=3.5)
                write(cr, [("MAR 14", INK)], 0, 16, 46, align="center", bold=True)
        cue("kaching", t, m + 0.35)
    if t >= 0.7:
        write(cr, [("23 people", CREAM)], CENTER[0], CENTER[1] + RAD + 120, 46, align="center", bold=True)
    hl(cr, t, [("just ", INK), ("23", RED), (" people", INK)], 215, 74, 0.0, end=A("b1", "better") - 0.05,
       bold=True)
    hl(cr, t, [("better than ", INK), ("50/50", RED)], 215, 74, A("b1", "better"), end=A("b1", "share") - 0.05,
       bold=True)
    hl(cr, t, [("same ", INK), ("BIRTHDAY", RED), ("?!", INK)], 215, 74, A("b1", "share"), bold=True)


def scene_calendar(cr, t, tl):
    A = tl.at
    keys = [(A("b2") - 0.2, (1.6, 360, 740)), (A("b2", "wrong"), (1.0, 360, 760)), (A("b2", "365"), (1.6, 360, 640)),
            (A("b2", "days"), (1.0, 360, 740)), (A("b2", "year"), (1.5, 300, 760)), (A("b2", "surely"), (1.0, 360, 900)),
            (A("b2", "way"), (1.6, 360, 1020)), (A("b2", "more"), (1.0, 360, 860))]
    bg(cr, t, keys)
    cols, cell = 25, 21
    x0, y0 = 360 - cols * cell / 2, 560
    n = int(365 * seg(t, A("b2", "365"), A("b2", "year", end=True)))
    for k in range(365):
        r, c = divmod(k, cols)
        x, y = x0 + c * cell, y0 + r * cell
        col = hexc("#3a4880") if k >= n else (YEL if k % 30 else PINK)
        cr.rectangle(x, y, cell - 4, cell - 4)
        cr.set_source_rgba(*col)
        cr.fill()
    if t >= A("b2", "365"):
        write(cr, [(str(max(1, n)), YEL), (" days", CREAM)], 360, 520, 70, align="center", bold=True)
    if t >= A("b2", "surely"):   # a crowd that keeps growing
        m = 6 + int(30 * seg(t, A("b2", "surely"), A("b2", "more", end=True)))
        for i in range(m):
            face(cr, 60 + (i % 12) * 54, 940 + (i // 12) * 70, 20, i)
        write(cr, [("100? 200?", CREAM)], 360, 1200, 50, align="center", bold=True)
    if t < A("b2", "365"):
        with at(cr, 360, 760, max(0.85, pop(t, A("b2", "wrong"), 0.25)), rot=-0.08):
            write(cr, [("???", PINK)], 0, 0, 160, align="center", bold=True)
    hl(cr, t, [("sounds ", INK), ("WRONG", RED)], 215, 80, A("b2"), end=A("b2", "365") - 0.05, bold=True)
    hl(cr, t, [("365", RED), (" days in a year", INK)], 215, 64, A("b2", "365"), end=A("b2", "surely") - 0.05, bold=True)
    hl(cr, t, [("need ", INK), ("way more", RED), (" people?", INK)], 215, 64, A("b2", "surely"), bold=True)


def scene_you(cr, t, tl):
    A = tl.at
    keys = [(A("b3") - 0.2, (1.2, 360, 800)), (A("b3", "trick"), (1.5, 360, 560)), (A("b3", "looking"), (1.0, 360, 820)),
            (A("b3", "your", nth=2), (1.6, seat(0)[0], seat(0)[1] + 60)), (A("b3", "any"), (0.95, 360, 820)),
            (A("b3", "match."), (1.15, 360, 820))]
    bg(cr, t, keys)
    any_t = A("b3", "any")
    you = seat(0)
    if t < any_t:
        k = seg(t, A("b3", "your", nth=2), A("b3", "your", nth=2) + 0.4)
        for i in range(1, int(1 + 22 * k)):
            line(cr, [you, seat(i)], 2.5, hexc("#ffd23f", 0.6), seed=1000 + i, amp=0.3)
    else:
        k = seg(t, any_t, any_t + 0.6)
        total = int(253 * k)
        c = 0
        for i in range(N):
            for j in range(i + 1, N):
                if c >= total:
                    break
                line(cr, [seat(i), seat(j)], 1.6, hexc("#5fd3f3", 0.45), seed=1100 + c % 97, amp=0.2)
                c += 1
        cue("whoosh", t, any_t)
    room(cr, t, -10, size=30)
    if t >= A("b3", "your", nth=2):
        write(cr, [("YOU", YEL)], you[0], you[1] - 56, 34, align="center", bold=True)
    hl(cr, t, [("here's the ", INK), ("TRICK", RED)], 215, 76, A("b3", "trick"), end=A("b3", "your", nth=2) - 0.05, bold=True)
    hl(cr, t, [("not just ", INK), ("YOUR", RED), (" birthday", INK)], 215, 66, A("b3", "your", nth=2), end=any_t - 0.05,
       bold=True)
    hl(cr, t, [("ANY TWO", RED), (" people", INK)], 215, 76, any_t, bold=True, underline=True)


def scene_pairs(cr, t, tl):
    A = tl.at
    keys = [(A("b4") - 0.2, (1.0, 360, 820)), (A("b4", "23"), (1.5, 360, 820)), (A("b4", "253", nth=1), (0.95, 360, 820)),
            (A("b4", "different"), (1.5, 360, 820)), (A("b4", "pairs."), (1.0, 360, 800)), (A("b4", "chances"), (1.6, 360, 820)),
            (A("b4", "match."), (1.0, 360, 840))]
    bg(cr, t, keys)
    k = seg(t, A("b4", "253", nth=1), A("b4", "pairs.", end=True))
    total = int(253 * ease_out(k))
    c = 0
    for i in range(N):
        for j in range(i + 1, N):
            if c >= total:
                break
            hue = (CYAN, PINK, YEL)[c % 3]
            line(cr, [seat(i), seat(j)], 1.6, (*hue[:3], 0.5), seed=1200 + c % 97, amp=0.2)
            c += 1
    room(cr, t, -10, size=30)
    with at(cr, CENTER[0], CENTER[1], 1.0):
        blob(cr, 0, 0, 92, 70, BG, seed=1300, amp=0.5, lw=4, stroke=CREAM)
        write(cr, [(str(total), YEL)], 0, 20, 70, align="center", bold=True)
    if t >= A("b4", "pairs."):
        write(cr, [("pairs", CREAM)], CENTER[0], CENTER[1] + 60, 30, align="center", bold=True)
    for q in range(0, 253, 23):
        cue("pop", t, A("b4", "253", nth=1) + q / 253 * (A("b4", "pairs.", end=True) - A("b4", "253", nth=1)))
    hl(cr, t, [("23", RED), (" people = ", INK), ("253", RED), (" pairs", INK)], 215, 64, A("b4", "253", nth=1),
       end=A("b4", "chances") - 0.05, bold=True)
    hl(cr, t, [("253", RED), (" chances to match", INK)], 215, 62, A("b4", "chances"), bold=True)


def prob(n):
    p = 1.0
    for k in range(int(n)):
        p *= (365 - k) / 365
    return 1 - p


GX, GY, GW, GH = 110, 1080, 520, 560     # graph origin (bottom-left) and size


def gpt(n, p):
    return GX + GW * n / 80, GY - GH * p


def scene_curve(cr, t, tl):
    A = tl.at
    t0 = A("b5")
    keys = [(t0 - 0.2, (1.0, 370, 820)), (A("b5", "pair"), (1.5, 250, 980)), (A("b5", "tiny"), (1.0, 370, 820)),
            (A("b5", "pile"), (1.5, 300, 900)), (A("b5", "fast"), (1.0, 370, 820)),
            (A("b6"), (1.5, 450, 660)), (A("b6", "97%."), (1.0, 370, 820)),
            (A("b7"), (1.5, 500, 660)), (A("b7", "99.9%."), (1.0, 370, 820))]
    bg(cr, t, keys)
    line(cr, [(GX, GY - GH - 30), (GX, GY)], 5, CREAM, seed=1400, amp=0.4)
    line(cr, [(GX, GY), (GX + GW + 30, GY)], 5, CREAM, seed=1402, amp=0.4)
    for p in (0.5, 1.0):
        cr.set_dash([10, 10])
        line(cr, [gpt(0, p), gpt(80, p)], 2, hexc("#f4efe1", 0.35), seed=1401, amp=0)
        cr.set_dash([])
        write(cr, [(f"{int(p * 100)}%", CREAM)], GX - 50, gpt(0, p)[1] + 10, 28, align="center", bold=True)
    for n in (0, 20, 40, 60, 80):
        write(cr, [(str(n), CREAM)], gpt(n, 0)[0], GY + 40, 28, align="center")
    write(cr, [("people", CREAM)], GX + GW / 2, GY + 84, 30, align="center", bold=True)
    # the curve draws itself, reaching 23 then 50 then 70
    if t < A("b6"):
        nmax = lerp(1, 23, seg(t, t0, A("b5", "fast", end=True)))
    elif t < A("b7"):
        nmax = lerp(23, 50, seg(t, A("b6"), A("b6", "97%.")))
    else:
        nmax = lerp(50, 80, seg(t, A("b7"), A("b7", "99.9%.")))
    pts = [gpt(n / 2, prob(n / 2)) for n in range(0, int(nmax * 2) + 1)]
    if len(pts) > 1:
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
        cr.set_source_rgba(*YEL)
        cr.set_line_width(7)
        cr.stroke()
    for n, key, label, col in ((23, ("b5", None), "23: 50.7%", PINK), (50, ("b6", "50"), "50: 97%", CYAN),
                               (70, ("b7", "70,"), "70: 99.9%", GREEN)):
        st = A(*key) if key[1] else t0
        if t >= st and nmax >= n - 0.5:
            x, y = gpt(n, prob(n))
            blob(cr, x, y, 13, 13, col, seed=1410 + n, amp=0.2, lw=3)
            lx, ly = {23: (x + 24, y + 12), 50: (x - 16, y + 100), 70: (x - 16, y + 190)}[n]
            with at(cr, lx, ly, max(0.85, pop(t, st, 0.25))):
                write(cr, [(label, col)], 0, 0, 40, align="right" if n > 23 else "left", bold=True)
            cue("pop", t, st)
    hl(cr, t, [("every pair adds a ", INK), ("tiny", RED), (" chance", INK)], 215, 54, A("b5", "tiny"),
       end=A("b5", "pile") - 0.05, bold=True)
    hl(cr, t, [("...and they ", INK), ("PILE UP", RED)], 215, 70, A("b5", "pile"), end=A("b6") - 0.05, bold=True)
    hl(cr, t, [("50", RED), (" people: ", INK), ("97%", RED)], 215, 80, A("b6", "50"), end=A("b7") - 0.05, bold=True)
    hl(cr, t, [("70", RED), (" people: ", INK), ("99.9%", RED)], 215, 80, A("b7", "70,"), bold=True)


def scene_class(cr, t, tl):
    A = tl.at
    keys = [(A("b8") - 0.2, (1.3, 360, 760)), (A("b8", "30,"), (0.95, 360, 800)), (A("b8", "bet"), (1.3, 360, 680)),
            (A("b8", "win"), (1.0, 360, 800)), (A("b8", "7"), (1.4, 360, 1040))]
    bg(cr, t, keys)
    for i in range(30):
        r, c = divmod(i, 6)
        sc = pop(t, A("b8") + i * 0.02, 0.2)
        if sc > 0:
            with at(cr, 110 + c * 100, 520 + r * 110, sc):
                face(cr, 0, 0, 30, i, happy=t >= A("b8", "win"))
    if t >= A("b8", "bet"):
        with at(cr, 360, 690, max(0.85, pop(t, A("b8", "bet"), 0.25)), rot=-0.06):
            shape(cr, rrect_pts(-150, -50, 300, 100, 16, 16), YEL, seed=1500, amp=0.5, lw=4)
            write(cr, [("BET ON IT", INK)], 0, 18, 52, align="center", bold=True)
        cue("hit", t, A("b8", "bet"))
    if t >= A("b8", "7"):   # 7 wins out of 10 bets
        for k in range(10):
            x = 135 + k * 50
            col = GREEN if k < 7 else hexc("#e05a5a")
            blob(cr, x, 1100, 20, 20, col, seed=1510 + k, amp=0.3, lw=3)
            if k < 7:
                line(cr, [(x - 9, 1100), (x - 2, 1108), (x + 10, 1092)], 4, INK, seed=1520 + k, amp=0.1)
            else:
                line(cr, [(x - 8, 1092), (x + 8, 1108)], 4, INK, seed=1530 + k, amp=0.1)
                line(cr, [(x + 8, 1092), (x - 8, 1108)], 4, INK, seed=1540 + k, amp=0.1)
    hl(cr, t, [("class of ", INK), ("30", RED), ("?", INK)], 215, 80, A("b8", "30,"), end=A("b8", "win") - 0.05,
       bold=True)
    hl(cr, t, [("you win ", INK), ("7 out of 10", RED)], 215, 70, A("b8", "win"), bold=True)


COMMENTS = [("Maya", "March 14"), ("Leo", "July 2"), ("Ava", "Oct 30"), ("Sam", "March 14!!"), ("Zoe", "Jan 9")]


def scene_comments(cr, t, tl):
    A = tl.at
    keys = [(A("b9") - 0.2, (1.2, 360, 720)), (A("b9", "drop"), (1.0, 360, 760)), (A("b9", "comments."), (1.15, 360, 820)),
            (A("b9", "bet"), (1.0, 360, 780)), (A("b9", "match."), (1.3, 360, 820))]
    bg(cr, t, keys)
    shape(cr, rrect_pts(90, 420, 540, 760, 30, 24), CREAM, seed=1600, amp=0.5, lw=4)
    write(cr, [("Comments", INK)], 130, 480, 38, bold=True)
    line(cr, [(110, 505), (610, 505)], 2.5, hexc("#c9c2b0"), seed=1601, amp=0.3)
    match = t >= A("b9", "bet")
    for k, (who, txt) in enumerate(COMMENTS):
        sc = pop(t, A("b9") + k * 0.25, 0.2)
        if sc <= 0:
            continue
        y = 570 + k * 115
        hot = match and k in (0, 3)
        with at(cr, 360, y, sc):
            if hot:
                shape(cr, rrect_pts(-260, -46, 520, 92, 14, 16), hexc("#ffd23f", 0.55), seed=1610 + k, amp=0.4,
                      lw=0, stroke=None)
            blob(cr, -215, 0, 30, 30, SHIRTS[k], seed=1620 + k, amp=0.3, lw=3)
            write(cr, [(who[0], WHITE)], -215, 12, 30, align="center", bold=True)
            write(cr, [("@" + who.lower(), hexc("#6b6e75"))], -170, -12, 24)
            write(cr, [(txt, INK)], -170, 26, 34, bold=True)
        cue("pop", t, A("b9") + k * 0.25)
    if match:
        y0, y1 = 570, 570 + 3 * 115
        line(cr, [(640, y0), (680, (y0 + y1) / 2), (640, y1)], 6, PINK, seed=1630, amp=0.6)
        cue("kaching", t, A("b9", "bet"))
        confetti(cr, t, A("b9", "match."), n=40, seed=7)
    hl(cr, t, [("drop your ", INK), ("BIRTHDAY", RED), ("!", INK)], 215, 64, A("b9", "drop"),
       end=A("b9", "bet") - 0.05, bold=True)
    hl(cr, t, [("find your ", INK), ("MATCH", RED)], 215, 76, A("b9", "bet"), bold=True, underline=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"room": scene_room, "calendar": scene_calendar, "you": scene_you, "pairs": scene_pairs, "curve": scene_curve,
     "class": scene_class, "comments": scene_comments}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
