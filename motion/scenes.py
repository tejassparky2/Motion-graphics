"""The Pumpkin Trick — fast-cut version, driven by the narration timeline.

Pacing rules (see reports/Shorts retention for animated explainers.md):
- speech runs back to back (0.15-0.3 s gaps) at roughly 200-230 wpm
- something on screen changes about every second: number write-ons on the spoken word, pose changes,
  camera punch-ins, props flying
- word-by-word captions in the upper-middle safe band
- question hook on frame 0; the last line flows back into the first so the Short loops
"""
import math

from . import characters as ch
from .captions import captions
from .characters import person, stall, truck, exhaust, crate, money_pile, pumpkin, cash
from .engine import (CREAM, GROUND, INK, RED, WHITE, W, at, blob, cue, ease_in, ease_out, hexc, line, pop, seg,
                     shape, sharp_shape, smooth, lerp, write, write_t)

# ---------------------------------------------------------------- script
# [spoken|shown] = what the narrator says | what the captions show.
SCRIPT = [
    dict(id="h1", scene="village", text="Why would a rich man pay [a thousand rupees|₹1000] for a [seventy rupee|₹70] pumpkin?"),
    dict(id="h2", scene="village", text="He wouldn't. Unless it's a trap. Here's the trick.", gap=0.15),
    dict(id="v1", scene="village", text="Day one, he offers [a hundred rupees|₹100] per pumpkin."),
    dict(id="v2", scene="village", text="Market price is [seventy,|₹70,] so that's [thirty|₹30] profit! The farmer sells."),
    dict(id="v3", scene="village", text="He buys [a hundred and twenty.|120.] Pays [twelve thousand,|₹12,000,] cash."),
    dict(id="v4", scene="village", text="Next day, he offers [three hundred!|₹300!]", gap=0.15),
    dict(id="v5", scene="village", text="So the whole village sells. [Five hundred|500] more. [One and a half lakh!|₹1.5 Lakh!]"),
    dict(id="v6", scene="village", text="Then he offers [a thousand.|₹1000.] But there are no pumpkins left.", gap=0.15),
    dict(id="v7", scene="village", text="So he says: I'm off to the city. My assistant will buy for me.",
         speaker="seth", speaker_from="I'm"),
    dict(id="v8", scene="village",
         text="But the assistant whispers: buy mine at [seven hundred,|₹700,] sell to my boss at [a thousand!|₹1000!]",
         speaker="chotu", speaker_from="buy"),
    dict(id="v9", scene="village", text="Easy money, right? So the village buys back all [six hundred and twenty.|620.]"),
    dict(id="v10", scene="village", text="But the boss never comes back. Neither does the assistant.", gap=0.2),
    dict(id="v11", scene="village", text="The price crashes to [fifty.|₹50.] They lose [six hundred and fifty|₹650] on every pumpkin."),
    dict(id="e1", scene="city", text="Meanwhile in the city: bought for [one point six two lakh,|₹1.62 L,] sold for [four point three four.|₹4.34 L.]"),
    dict(id="e2", scene="city", text="Profit? [Two point seven two lakh!|₹2.72 Lakh!]", gap=0.15),
    dict(id="e3", scene="outro", text="So next time a price makes no sense, ask yourself:", gap=0.2),
]

# ---------------------------------------------------------------- layout
FEET = 840
STALL_X, STALL_Y = 470, 820
TRUCK_Y = 1010
SETH_X, RAMU_X, CHOTU_X = 190, 590, 150
PROP_X = 330  # the ₹70 pumpkin in the hook

# camera = (zoom, focus x, focus y) in world units; the focus point lands at ANCHOR on screen
ANCHOR = (360, 780)
WIDE = (1.2, 360, 760)
LOW = (1.2, 380, 800)       # wide, tilted down to show the truck lane
P_SETH = (1.5, 230, 700)
P_RAMU = (1.5, 560, 700)
P_CHOTU = (1.5, 190, 700)
HOOK = (1.6, 290, 690)
_cam = [WIDE]


def enter_world(cr):
    z, fx, fy = _cam[0]
    cr.translate(*ANCHOR)
    cr.scale(z, z)
    cr.translate(-fx, -fy)


def camera(t, keys, dur=0.3):
    """Ease into each camera key [(time, (zoom, fx, fy))] from the previous one."""
    active = [k for k in sorted(keys, key=lambda k: k[0]) if k[0] <= t]
    if not active:
        return keys[0][1]
    kt, v = active[-1]
    before = active[-2][1] if len(active) > 1 else v
    u = ease_out(seg(t, kt, kt + dur))
    return tuple(lerp(a, b, u) for a, b in zip(before, v))


def background(cr):
    enter_world(cr)
    cr.set_source_rgba(*CREAM)
    cr.paint()
    sharp_shape(cr, [(-900, 772), (1600, 742), (1600, 1700), (-900, 1700)], GROUND, seed=1, amp=0.8, lw=4)
    marks = [(60, 880), (250, 930), (430, 900), (640, 950), (120, 1020), (330, 1060), (560, 1030), (80, 1180),
             (-120, 900), (820, 920), (-200, 1050), (900, 1080)]
    for i, (x, y) in enumerate(marks):
        line(cr, [(x, y), (x + 8, y - 5), (x + 16, y), (x + 24, y - 4)], 2.5, hexc("#8f8a74"), seed=20 + i, amp=0.8)


def hl(cr, t, runs, y, size, start, end=None, bold=False, underline=False):
    """Handwritten headline in the top safe band; writes on fast, starting on the spoken word."""
    if isinstance(runs, str):
        runs = [(runs, INK)]
    n = sum(len(s) for s, _ in runs)
    write_t(cr, runs, W / 2, y, size, t, start, dur=max(0.18, 0.022 * n), end=end, align="center", bold=bold,
            underline=underline)
    cue("pop", t, start)


def stamp(cr, t, start, text, dur=0.7):
    """Big rotated stamp (e.g. NEXT DAY) that slams in and out — a pattern interrupt instead of a slow fade."""
    if not (start <= t < start + dur):
        return
    cue("whoosh", t, start, 0.3)
    s = pop(t, start, 0.18)
    a = 1 - seg(t, start + dur - 0.15, start + dur)
    cr.save()
    cr.identity_matrix()
    cr.push_group()
    with at(cr, W / 2, 470, s, rot=-0.12):
        shape(cr, [(-230, -70), (230, -70), (230, 50), (-230, 50)], INK, seed=33, amp=1.5, lw=0, stroke=None)
        write(cr, [(text, hexc("#ffd23f"))], 0, 22, 84, align="center", bold=True)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def fly(cr, t, start, dur, p0, p1, draw, height=150):
    u = seg(t, start, start + dur)
    if u <= 0 or u >= 1:
        return
    e = smooth(u)
    draw(lerp(p0[0], p1[0], e), lerp(p0[1], p1[1], e) - math.sin(u * math.pi) * height)


def truck_slot(i, tx):
    slots = [(-5, 0), (85, 0), (165, 0), (40, 1), (125, 1)]
    cx, row = slots[i]
    return tx + cx + 20, TRUCK_Y - 80 - row * 56


def drive(t, t_in, t_out, x_park=380, x_from=950, x_to=-450, d_in=0.55, d_out=0.6):
    if t < t_out:
        x = lerp(x_from, x_park, ease_out(seg(t, t_in, t_in + d_in)))
    else:
        x = lerp(x_park, x_to, ease_in(seg(t, t_out, t_out + d_out)))
    return x, x / 28.0


def price_tag(cr, x, y, text):
    with at(cr, x, y, 1.0, rot=0.12):
        line(cr, [(-4, 32), (-58, 70)], 2.5, INK, seed=41, amp=0.3)  # string down to the stem
        shape(cr, [(-40, -12), (34, -12), (46, 10), (34, 32), (-40, 32)], WHITE, seed=42, amp=0.6, lw=3)
        write(cr, [(text, RED)], -4, 22, 30, align="center", bold=True)


def _mouth(talking, t, rest):
    return ("o" if int(t * 12) % 2 else "smile") if talking else rest


# ---------------------------------------------------------------- the village set
def village(cr, t, tl, outro=False):
    """Hook + whole village story. In the outro the set is shown in its hook state, so the Short loops."""
    A = tl.at
    s = 0.0 if outro else t   # story-state time (idle motion always uses t)

    # ---- camera
    if outro:
        _cam[0] = camera(t, [(A("e3") - 0.2, HOOK), (A("e3", "sense"), (1.7, 380, 690)),
                             (A("e3", "ask"), (1.7, 250, 690)), (A("e3", "yourself"), HOOK)])
    else:
        # a new framing on (almost) every spoken number keeps the picture changing about once a second
        keys = [(0, HOOK), (A("h1", "₹1000"), (1.7, 250, 690)), (A("h1", "₹70"), (1.7, 380, 690)),
                (A("h2"), HOOK), (A("h2", "trap"), (1.8, 230, 660)), (A("h2", "trick"), WIDE),
                (A("v1", "₹100"), P_SETH), (A("v2"), P_RAMU), (A("v2", "₹30", end=True), WIDE),
                (A("v3"), LOW), (A("v3", "₹12,000"), (1.4, 520, 720)), (A("v3", "cash"), (1.3, 420, 760)),
                (A("v4"), (1.6, 560, 700)), (A("v5"), LOW), (A("v5", "500"), (1.35, 450, 760)),
                (A("v5", "₹1.5"), P_RAMU), (A("v6"), WIDE), (A("v6", "no"), P_RAMU),
                (A("v7"), P_SETH), (A("v7", "assistant"), WIDE), (A("v8"), LOW), (A("v8", "buy"), P_CHOTU),
                (A("v8", "₹700"), (1.7, 190, 690)), (A("v8", "₹1000"), P_RAMU), (A("v9"), LOW),
                (A("v9", "buys"), (1.3, 380, 760)), (A("v9", "620"), (1.5, 470, 720)),
                (A("v10", "never"), (1.35, 520, 720)), (A("v10", "Neither"), LOW),
                (A("v11"), WIDE), (A("v11", "₹50"), (1.4, 560, 720)), (A("v11", "lose"), (1.6, 560, 700)),
                (A("v11", "₹650"), (1.7, 590, 700))]
        z, fx, fy = camera(t, keys)
        if t < A("h2", "trap"):
            z += 0.06 * seg(t, 0, A("h2", "trap"))  # slow push-in so frame 0 is already moving
        _cam[0] = (z, fx, fy)

    background(cr)

    # ---- trucks and crates (state)
    t1_in, t1_out = A("v3"), A("v3", end=True) - 0.05
    t1_crates = [A("v3", "120") + 0.2 * i for i in range(3)]
    t2_in, t2_out = A("v5"), A("v5", end=True)
    t2_crates = [A("v5", "whole") + 0.18 * i for i in range(5)]
    t3_in, t3_out = A("v8"), A("v10") + 0.25
    t3_crates = [A("v9", "buys") + 0.35 + 0.16 * i for i in range(5)]
    FL = 0.4
    stock = 1.0 - 0.15 * sum(s >= c for c in t1_crates) - 0.11 * sum(s >= c for c in t2_crates)
    stock = max(0.0, stock) + 0.2 * sum(s >= c + FL for c in t3_crates)
    stall(cr, STALL_X, STALL_Y, min(1.0, stock))

    # ---- the ₹70 pumpkin prop (hook); it hops onto the stall when the story starts
    prop_gone = A("v1")
    if s < prop_gone:
        b = abs(math.sin(t * 6)) * 6
        pumpkin(cr, PROP_X, FEET + 4 - b, 44, seed=880)
        price_tag(cr, PROP_X + 62, FEET - 150 - b, "₹70")
    fly(cr, s, prop_gone, 0.35, (PROP_X, FEET), (STALL_X - 20, STALL_Y - 190),
        lambda x, y: pumpkin(cr, x, y, 34, seed=880))

    # ---- Seth (the rich man)
    talk_s = tl.speaking("seth", t)
    if s < A("h2", "trick"):
        smirk = not outro and s > A("h2", "trap")
        person(cr, "seth", SETH_X, FEET, t, facing=1, arms=("give", "hip"), item="cash_big",
               mouth="smirk" if smirk else "grin", lean=math.sin(t * 9) * 0.02)
    elif s < A("v7", "assistant") + 1.0:
        leaving = s > A("v7", "assistant")
        sx = lerp(SETH_X, -170, seg(s, A("v7", "assistant"), A("v7", "assistant") + 0.9))
        if A("v1", "₹100") - 0.1 <= s < A("v1", "₹100") + 0.8:
            arms = ("point", "hip")
        elif A("v2", "sells") <= s < A("v3"):
            arms = ("thumb", "hip")
        elif A("v3", "cash") - 0.3 <= s < A("v3", "cash") + 0.4:
            arms = ("give", "hip")
        elif A("v4", "₹300") <= s < A("v4", end=True) or A("v6", "₹1000") <= s < A("v6", "no"):
            arms = ("point", "hip")
        elif leaving:
            arms = ("down", "wave")
        else:
            arms = ("hip", "hip")
        person(cr, "seth", sx, FEET, t, facing=-1 if leaving else 1, walk=(sx / 70) if leaving else None,
               arms=arms, item="cash" if arms[0] == "give" else "briefcase" if leaving else None,
               mouth=_mouth(talk_s, t, "grin" if s > A("v4") else "smile"))

    # ---- Chotu (the assistant)
    if not outro and A("v8") <= s < A("v10") + 1.2:
        talk_c = tl.speaking("chotu", t)
        cx = lerp(430, CHOTU_X, seg(s, A("v8") + 0.3, A("v8") + 0.8))
        leaving = s > A("v10")
        if leaving:
            cx = lerp(CHOTU_X, -160, seg(s, A("v10"), A("v10") + 1.0))
        got_cash = s > A("v9", "buys") + 0.35
        walking = A("v8") + 0.3 < s < A("v8") + 0.8 or leaving
        person(cr, "chotu", cx, FEET, t, facing=-1 if leaving else 1, walk=(cx / 60) if walking else None,
               arms=("point" if talk_c else "hold" if got_cash else "hip", "hip"),
               item="cash_big" if got_cash else None, eyes="happy" if got_cash else "sly",
               mouth=_mouth(talk_c, t, "grin" if got_cash else "smirk"))

    # ---- Ramu (the farmer)
    r = dict(facing=-1, arms=("hip", "hip"), eyes="dot", mouth="smile")
    if s < A("v1"):
        r.update(eyes="wide", mouth="o")
    elif s < A("v2"):
        r.update(eyes="happy" if s > A("v1", "₹100") else "dot")
    elif s < A("v3"):
        if s < A("v2", "₹70"):
            r.update(arms=("chin", "hip"), mouth="flat")
        elif s < A("v2", "₹30"):
            r.update(arms=("chin", "hip"), eyes="wide", mouth="o")
        elif s < A("v2", "sells"):
            r.update(eyes="rupee", mouth="grin")
        else:
            r.update(arms=("thumb", "hip"), eyes="happy", mouth="grin",
                     jump=abs(math.sin((s - A("v2", "sells")) * 9)) * 16 * (1 - seg(s, A("v2", "sells"), A("v3"))))
    elif s < A("v4"):
        if s >= A("v3", "cash"):
            r.update(arms=("cheer", "hip"), item="cash", eyes="happy", mouth="grin")
    elif s < A("v5"):
        if s >= A("v4", "₹300"):
            r.update(eyes="wide", mouth="o", shake=1.6 * (1 - seg(s, A("v4", "₹300") + 0.5, A("v4", "₹300") + 0.6)))
    elif s < A("v6"):
        if s < A("v5", "₹1.5"):
            r.update(arms=("rub", "hip"), eyes="rupee", mouth="grin")
        else:
            r.update(arms=("cheer", "hip"), item="cash_big", eyes="rupee", mouth="grin")
    elif s < A("v8"):
        if s >= A("v6", "no"):
            r.update(arms=("chin", "hip"), eyes="sad", mouth="wobble", sweat=True)
        else:
            r.update(eyes="wide", mouth="o")
    elif s < A("v9"):
        if s >= A("v8", "₹1000"):
            r.update(arms=("rub", "hip"), eyes="rupee", mouth="grin")
        else:
            r.update(eyes="wide", mouth="flat")
    elif s < A("v10"):
        if A("v9", "buys") - 0.2 <= s < A("v9", "buys") + 0.4:
            r.update(arms=("give", "hip"), item="cash_big", eyes="rupee", mouth="grin")
        else:
            r.update(eyes="happy", mouth="grin")
    elif s < A("v11"):
        r.update(eyes="sad", mouth="flat", lean=math.sin(t * 2.2) * 0.05)
    elif s >= A("v11", "lose"):
        r.update(arms=("face", "face"), eyes="cry", mouth="sad", tears=True)
    elif s >= A("v11", "₹50"):
        r.update(eyes="wide", mouth="o", shake=1.2)
    else:
        r.update(eyes="sad", mouth="sad")
    person(cr, "ramu", RAMU_X, FEET, t, **r)

    # ---- trucks
    if not outro:
        for t_in, t_out, crates_out, park, full in ((t1_in, t1_out, t1_crates, 380, False),
                                                    (t2_in, t2_out, t2_crates, 380, False),
                                                    (t3_in, t3_out, t3_crates, 420, True)):
            if not (t_in <= s < t_out + 0.7):
                continue
            tx, wheel = drive(s, t_in, t_out, x_park=park)
            if full:
                n = 5 - sum(s >= c for c in crates_out)
            else:
                n = sum(s >= c + FL for c in crates_out)
            cue("engine", t, t_in, 0.55)
            cue("engine", t, t_out, 0.6)
            truck(cr, tx, TRUCK_Y, t, crates=n, wheel=wheel, driver=ch.SKIN_TAN if full else ch.SKIN_MID)
            if s < t_in + 0.55 or s > t_out:
                exhaust(cr, tx + 210, TRUCK_Y - 40, t)
            for i, c in enumerate(crates_out):
                cue("thud", t, c + FL)
                if full:
                    fly(cr, s, c, FL, truck_slot(4 - i, tx), (STALL_X - 40, STALL_Y - 150),
                        lambda x, y, i=i: crate(cr, x, y, 80, 56, seed=304 - i))
                else:
                    fly(cr, s, c, FL, (STALL_X - 40, STALL_Y - 150), truck_slot(i, tx),
                        lambda x, y, i=i: crate(cr, x, y, 80, 56, seed=300 + i))

    # ---- screen-space graphics: headlines, stamps, chart
    if outro:
        hl(cr, t, "Price makes no sense?", 225, 60, A("e3", "price"), bold=True)
        return
    hl(cr, t, [("₹1000", RED)], 225, 96, A("h1", "₹1000"), end=A("v1"), bold=True)
    hl(cr, t, [("for a ", INK), ("₹70", RED), (" pumpkin?", INK)], 300, 56, A("h1", "₹70"), end=A("v1"))
    hl(cr, t, [("Per pumpkin = ", INK), ("₹100", RED)], 225, 60, A("v1", "₹100"), end=A("v2") - 0.05)
    hl(cr, t, [("Market price = ", INK), ("₹70", RED)], 200, 48, A("v2", "₹70"), end=A("v3") - 0.05)
    hl(cr, t, [("Offer = ", INK), ("₹100", RED)], 258, 48, A("v2", "₹70") + 0.25, end=A("v3") - 0.05)
    hl(cr, t, [("Profit = ", INK), ("₹30 each!", RED)], 330, 58, A("v2", "₹30"), end=A("v3") - 0.05, bold=True,
       underline=True)
    hl(cr, t, [("Buys ", INK), ("120", RED), (" pumpkins", INK)], 215, 56, A("v3", "120"), end=A("v4") - 0.05)
    hl(cr, t, [("₹12,000", RED), (" paid", INK)], 292, 56, A("v3", "₹12,000"), end=A("v4") - 0.05)
    stamp(cr, t, A("v4") - 0.1, "NEXT DAY")
    hl(cr, t, [("Per pumpkin = ", INK), ("₹300", RED)], 225, 62, A("v4", "₹300"), end=A("v5", "500") - 0.05,
       bold=True)
    cue("hit", t, A("v4", "₹300"))
    hl(cr, t, [("500", RED), (" more", INK)], 210, 56, A("v5", "500"), end=A("v6") - 0.05)
    hl(cr, t, [("₹1.5 Lakh", RED), (" paid", INK)], 292, 62, A("v5", "₹1.5"), end=A("v6") - 0.05, bold=True)
    cue("kaching", t, A("v5", "₹1.5"))
    hl(cr, t, [("Per pumpkin = ", INK), ("₹1000!!", RED)], 215, 62, A("v6", "₹1000"), end=A("v8") - 0.05, bold=True)
    hl(cr, t, "...but none left", 290, 48, A("v6", "no"), end=A("v8") - 0.05)
    cue("hit", t, A("v6", "no"))
    hl(cr, t, [("Buy from me @ ", INK), ("₹700", RED)], 205, 50, A("v8", "₹700"), end=A("v9") - 0.05)
    hl(cr, t, [("Sell to boss @ ", INK), ("₹1000", RED)], 275, 50, A("v8", "₹1000"), end=A("v9") - 0.05)
    hl(cr, t, "Village buys back", 205, 50, A("v9", "buys"), end=A("v10") - 0.05)
    hl(cr, t, [("620", RED), (" x ", INK), ("₹700", RED), (" = ", INK), ("₹4.34 L", RED)], 285, 56, A("v9", "620"),
       end=A("v10") - 0.05, bold=True)
    hl(cr, t, "Nobody comes back.", 235, 58, A("v10", "never"), end=A("v11") - 0.05)
    if t < A("v11", "lose"):
        _chart(cr, t, A("v11") - 0.05, A("v11", "₹50"))
    cue("fall", t, A("v11", "₹50") - 0.5, 0.6)
    cue("hit", t, A("v11", "₹50"))
    hl(cr, t, [("Per pumpkin = ", INK), ("₹50", RED)], 210, 58, A("v11", "lose"))
    hl(cr, t, [("Loss = ", INK), ("₹650", RED), (" each", INK)], 290, 62, A("v11", "₹650"), bold=True, underline=True)


def _chart(cr, t, start, crash_at):
    """Price history drawn fast; the final crash lands exactly on the spoken 'fifty'."""
    x0, y0, w, h = 150, 110, 440, 220
    p = seg(t, start, start + 0.25)
    if p <= 0:
        return
    cr.save()
    cr.identity_matrix()
    cr.set_source_rgba(*INK)
    cr.set_line_width(4)
    cr.set_line_cap(1)
    cr.move_to(x0, y0)
    cr.line_to(x0, y0 + h)
    cr.line_to(x0 + w * p, y0 + h)
    cr.stroke()
    write(cr, "price", x0 - 12, y0 + 20, 26, align="right")
    vals = [70, 100, 300, 1000, 50]
    pts = [(x0 + 20 + i * (w - 40) / 4, y0 + h - 10 - v / 1000 * (h - 30)) for i, v in enumerate(vals)]
    # climb to the peak quickly, then crash on the word
    if t < crash_at - 0.25:
        u = 3 * seg(t, start + 0.15, max(start + 0.2, crash_at - 0.25))
    else:
        u = 3 + seg(t, crash_at - 0.25, crash_at)
    k = int(min(u, 3.999))
    path = pts[:k + 1]
    f = u - k
    path.append((lerp(pts[k][0], pts[k + 1][0], f), lerp(pts[k][1], pts[k + 1][1], f)))
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
            write(cr, f"₹{v}", x, y - 16, 26, align="center", bold=i in (3, 4))
    cr.restore()


# ---------------------------------------------------------------- city payoff
def city(cr, t, tl):
    A = tl.at
    t0 = A("e1") - 0.2
    z, fx, fy = camera(t, [(t0, (1.0, 360, 900)), (A("e1", "city"), (1.08, 360, 880)),
                           (A("e1", "₹1.62"), (1.15, 320, 870)), (A("e1", "₹4.34"), (1.15, 410, 870)),
                           (A("e2"), (1.05, 360, 890)), (A("e2", "₹2.72"), (1.3, 370, 830))])
    cr.save()
    cr.translate(360, 900)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    cr.set_source_rgba(*hexc("#f5e6c4"))
    cr.paint()
    for i, (x, w, hgt, col) in enumerate([(-80, 190, 420, "#9c8fb8"), (100, 110, 330, "#b3a6c9"),
                                          (470, 120, 380, "#9c8fb8"), (580, 220, 300, "#b3a6c9")]):
        sharp_shape(cr, [(x, 900 - hgt), (x + w, 900 - hgt), (x + w, 900), (x, 900)], hexc(col), seed=700 + i,
                    amp=0.8, lw=3.5)
        for rr in range(int(hgt // 60) - 1):
            for c in range(int(w // 40)):
                wx, wy = x + 14 + c * 40, 900 - hgt + 26 + rr * 60
                sharp_shape(cr, [(wx, wy), (wx + 20, wy), (wx + 20, wy + 30), (wx, wy + 30)], hexc("#fff3c4"),
                            seed=720 + i * 10 + rr + c, amp=0.4, lw=2.5)
    sharp_shape(cr, [(215, 440), (505, 440), (505, 900), (215, 900)], ch.PURPLE, seed=760, amp=1.0, lw=4)
    shape(cr, [(240, 465), (480, 465), (480, 525), (240, 525)], ch.GOLD, seed=761, amp=0.6, lw=3)
    write(cr, [("SETH & CO.", INK)], 360, 510, 38, align="center", bold=True)
    for rr in range(5):
        for c in range(4):
            wx, wy = 240 + c * 62, 555 + rr * 66
            sharp_shape(cr, [(wx, wy), (wx + 40, wy), (wx + 40, wy + 40), (wx, wy + 40)], hexc("#fff3c4"),
                        seed=770 + rr * 4 + c, amp=0.4, lw=2.5)
    sharp_shape(cr, [(-60, 900), (780, 890), (780, 1400), (-60, 1400)], hexc("#a9a391"), seed=780, amp=0.8, lw=4)
    rise = ease_out(seg(t, t0, t0 + 0.5))
    money_pile(cr, 360, 1060 + (1 - rise) * 250, 1.45)
    laugh = t > A("e2", "₹2.72")
    person(cr, "seth", 300, 870 + (1 - rise) * 250, t, facing=1, arms=("cheer" if laugh else "hold", "hip"),
           item="cash_big", mouth="laugh" if laugh else "grin", jump=abs(math.sin(t * 9)) * 6 if laugh else 0)
    person(cr, "chotu", 455, 890 + (1 - rise) * 250, t, facing=-1, arms=("thumb", "hip"),
           eyes="closed" if laugh else "happy", mouth="laugh" if laugh else "grin",
           jump=abs(math.sin(t * 9 + 1)) * 6 if laugh else 0)
    # falling notes keep the frame alive
    for i in range(6):
        k = (t * 0.7 + i / 6) % 1
        cash(cr, 60 + i * 120 + math.sin(t * 2 + i) * 20, 380 + k * 520, 0.55, seed=990 + i, rot=math.sin(t * 3 + i))
    if laugh:
        for i, (hx, hy) in enumerate([(130, 560), (590, 540)]):
            sc = pop(t, A("e2", "₹2.72") + 0.1 + i * 0.15)
            if sc:
                with at(cr, hx, hy, sc, rot=0.2 * (i * 2 - 1)):
                    write(cr, [("HA HA!", RED)], 0, 0, 46, align="center", bold=True)
    cr.restore()
    # the ledger (screen space, top safe band)
    shape(cr, [(90, 140), (630, 140), (630, 355), (90, 355)], hexc("#fbf8ef", 0.94), seed=790, amp=1.0, lw=3.5)
    hl(cr, t, [("Bought 620 for ", INK), ("₹1.62 L", RED)], 200, 44, A("e1", "₹1.62"))
    hl(cr, t, [("Sold 620 for ", INK), ("₹4.34 L", RED)], 260, 44, A("e1", "₹4.34"))
    hl(cr, t, [("Profit = ", INK), ("₹2.72 Lakh", RED)], 335, 58, A("e2", "₹2.72"), bold=True, underline=True)
    cue("kaching", t, A("e2", "₹2.72"))


# ---------------------------------------------------------------- frame
def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    whip = 0.16
    cr.save()
    if start > 0 and t - start < whip:
        u = ease_out((t - start) / whip)
        cr.set_source_rgba(*INK)
        cr.paint()
        cr.translate(W * (1 - u), 0)
        cue("whoosh", t, start, 0.25)
    if name == "village":
        village(cr, t, tl)
    elif name == "city":
        city(cr, t, tl)
    else:  # outro: back to the hook frame so the Short loops into its first line
        village(cr, t, tl, outro=True)
    cr.restore()
    captions(cr, t, tl)
