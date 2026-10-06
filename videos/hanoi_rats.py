"""Researchers found: "The Great Hanoi Rat Hunt" (French colonial Hanoi, 1902).

Documented by historian Michael G. Vann from the colonial archives (Aix-en-Provence): new sewers filled with rats; with
plague in the region, the administration paid a bounty of one cent per rat, payable on the tail. Officials then saw
tailless rats; hunters were cutting tails and releasing the rats to breed, and health inspectors found rat farms
outside the city. The textbook name for it is a "perverse incentive". (The similar Delhi "cobra" story is anecdotal and
is left out.) Structure follows the owner's "Napoleon was once asked" reference.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import camera, hl, stamp, whip

NARRATOR = dict()
TAIL = 0.8

SCRIPT = [
    dict(id="h1", scene="hook", text="In [nineteen oh two,|1902,] a city paid people to kill rats. And it ended up "
                                     "with more rats."),
    dict(id="h2", scene="city", text="The city was Hanoi, in Vietnam, which was ruled by France at the time."),
    dict(id="h3", scene="city", text="The French had just built new sewers under the city. And the sewers filled up "
                                     "with rats."),
    dict(id="h4", scene="bounty", text="Officials were scared the rats would spread plague. So they made an offer. One "
                                       "cent for every rat you kill."),
    dict(id="h5", scene="bounty", text="To get paid, you didn't need to bring the whole rat. Just its tail."),
    dict(id="h6", scene="tailless", text="Then officials noticed something strange. Rats running around the city, with "
                                         "no tails."),
    dict(id="h7", scene="tailless", text="The hunters were cutting off the tails, and letting the rats go. A free rat "
                                         "makes more baby rats. And more tails to sell."),
    dict(id="h8", scene="farm", text="Health inspectors even found rat farms outside the city."),
    dict(id="h9", scene="name", text="Economists call this a perverse incentive. Pay for the wrong thing, and people "
                                     "will give you more of the problem."),
    dict(id="h10", scene="end", text="So what do you think? Would you have farmed the rats? Be honest.", pace=0.95),
]

METADATA = dict(
    title="A City Paid People to Kill Rats… and Got MORE Rats 🐀",
    alt_titles=["The Great Hanoi Rat Hunt of 1902 🐀", "Why Paying for Rat Tails Backfired 😂"],
    description="""In 1902, a city paid people to kill rats… and ended up with more rats. 🐀

Hanoi, then ruled by France, had just built new sewers, and they filled up with rats. Afraid of plague, officials offered one cent for every rat, and all you had to bring was the tail. Soon there were rats running around with no tails: hunters were cutting off the tails and letting the rats go to breed. Health inspectors even found rat farms outside the city. 😳

Economists call it a perverse incentive: pay for the wrong thing, and people give you more of the problem.

Source: historian Michael G. Vann's research in the French colonial archives ("The Great Hanoi Rat Hunt").

💬 So what do you think? Would you have farmed the rats? Be honest 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#History", "#Economics", "#Rats"],
    tags=["great hanoi rat hunt", "hanoi rat massacre", "perverse incentive", "cobra effect", "weird history",
          "economics explained", "history facts", "unintended consequences", "researchers found",
          "interestingly strange"],
    pinned_comment="Be honest… you would've started a rat farm too 😂🐀 Wouldn't you?",
)

SKY, STREET = hexc("#f6e7c8"), hexc("#c9a77c")
SEWER, SEWER_D = hexc("#5b5446"), hexc("#3c372e")
RAT, RAT_D = hexc("#8c8f99"), hexc("#5f626b")
GOLD, GOLD_D = hexc("#f2c14e"), hexc("#b9862a")
GREEN = hexc("#2e9e52")
BLUE = hexc("#3f6fb5")
OFFICIAL, HUNTER, INSPECTOR = "hilbert", "ramu", "principal"


def bg(cr, t, keys, color=SKY, dur=0.3):
    cr.set_source_rgba(*color)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=dur)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)


def rat(cr, t, x, y, s=1.0, facing=1, tail=True, run=0.0, seed=0, scared=False):
    bob = abs(math.sin(run * 12 + seed)) * 6 if run else 0
    with at(cr, x, y - bob, s, flip=facing < 0):
        if tail:
            line(cr, [(-46, 4), (-76, -8 + 6 * math.sin(t * 8 + seed)), (-104, 6)], 5, hexc("#d9a0a0"), seed=seed,
                 amp=0.3)
        blob(cr, -4, 0, 48, 28, RAT, seed=seed + 1, amp=0.5, lw=3.5)
        blob(cr, 40, -6, 24, 20, RAT, seed=seed + 2, amp=0.4, lw=3.5)
        blob(cr, 30, -26, 11, 11, hexc("#d9a0a0"), seed=seed + 3, amp=0.2, lw=3)
        blob(cr, 50, -14, 6 if not scared else 8, 7 if not scared else 9, WHITE, seed=seed + 4, amp=0.1, lw=2)
        blob(cr, 52, -14, 3, 3, INK, seed=seed + 5, amp=0.1, lw=0, stroke=None)
        blob(cr, 64, -4, 4, 4, hexc("#d9707a"), seed=seed + 6, amp=0.1, lw=0, stroke=None)
        for k in (-20, 14):
            line(cr, [(k, 24), (k + 4, 34)], 4, RAT_D, seed=seed + 7 + k, amp=0.2)


def coin(cr, x, y, s=1.0, seed=0):
    with at(cr, x, y, s):
        blob(cr, 0, 0, 30, 30, GOLD, seed=seed, amp=0.3, lw=4, stroke=GOLD_D)
        write(cr, [("1¢", GOLD_D)], 0, 12, 30, align="center", bold=True)


def tails_bundle(cr, x, y, n, s=1.0):
    with at(cr, x, y, s):
        for k in range(n):
            a = -0.6 + k * 1.2 / max(1, n - 1)
            line(cr, [(0, 0), (90 * math.sin(a), -90 * math.cos(a)), (110 * math.sin(a) + 10, -100 * math.cos(a))],
                 5, hexc("#d9a0a0"), seed=900 + k, amp=0.4)
        shape(cr, rrect_pts(-16, -12, 32, 26, 6, 8), hexc("#9c6b43"), seed=899, amp=0.3, lw=3)


def street(cr, w0=-600, w1=1400):
    for k, (x, h, col) in enumerate(((60, 300, "#e9c9a0"), (220, 360, "#f1d7b0"), (400, 280, "#e3bd92"),
                                     (560, 340, "#f1d7b0"), (720, 300, "#e9c9a0"))):
        shape(cr, rrect_pts(x - 75, 760 - h, 150, h, 6, 12), hexc(col), seed=300 + k, amp=0.5, lw=4)
        for r in range(2):
            shape(cr, rrect_pts(x - 45, 790 - h + r * 90, 34, 46, 4, 6), hexc("#6e8fb0"), seed=310 + k * 3 + r,
                  amp=0.2, lw=2.5)
            shape(cr, rrect_pts(x + 11, 790 - h + r * 90, 34, 46, 4, 6), hexc("#6e8fb0"), seed=320 + k * 3 + r,
                  amp=0.2, lw=2.5)
    shape(cr, [(w0, 760), (w1, 760), (w1, 2200), (w0, 2200)], STREET, seed=330, amp=0.5, lw=4)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, (1.55, 360, 800)), (A("h1", "paid"), (1.7, 360, 820)), (A("h1", "more"), (1.5, 360, 800))]
    bg(cr, t, keys)
    street(cr)
    # coins raining while the rat count climbs instead of falling
    for k in range(8):
        u = (t * 0.7 + k / 8) % 1
        coin(cr, 80 + k * 85, lerp(560, 860, u), 0.6, seed=400 + k)
    n = 3 if t < A("h1", "ended") else 3 + int(min(14, (t - A("h1", "ended")) * 10))
    for k in range(n):
        rat(cr, t, (k * 137 + t * 220 * (1 if k % 2 else -1)) % 820 - 50, 800 + (k % 4) * 40, 0.6,
            facing=1 if k % 2 else -1, run=t, seed=k * 11)
    with at(cr, 360, 610, 0.8):
        shape(cr, rrect_pts(-170, -50, 340, 100, 20, 12), hexc("#2b2d3a"), seed=410, amp=0.3, lw=0, stroke=None)
        write(cr, [("RATS: ", WHITE), (f"{n * 1000:,}", RED if t >= A("h1", "more") else GOLD)], 0, 16, 44,
              align="center", bold=True)
    hl(cr, t, [("PAID", GREEN), (" to kill rats...", INK)], 215, 64, 0.0, end=A("h1", "more") - 0.05, bold=True,
       sound=False)
    hl(cr, t, [("...got ", INK), ("MORE", RED), (" rats", INK)], 215, 70, A("h1", "more"), bold=True)
    cue("hit", t, A("h1", "more"))


def scene_city(cr, t, tl):
    A = tl.at
    keys = [(A("h2") - 0.2, (1.55, 360, 800)), (A("h3", "sewers"), (1.55, 360, 900)), (A("h3", "rats."), (1.75, 380, 930))]
    bg(cr, t, keys)
    street(cr)
    # the new sewer under the street
    shape(cr, rrect_pts(-200, 880, 1120, 170, 70, 14), SEWER, seed=500, amp=0.4, lw=5)
    shape(cr, rrect_pts(-200, 1010, 1120, 40, 16, 12), SEWER_D, seed=501, amp=0.3, lw=0, stroke=None)
    if t >= A("h3", "rats."):
        for k in range(9):
            rat(cr, t, (k * 120 + t * 260) % 1000 - 120, 990, 0.75, facing=1, run=t, seed=k * 7)
    if t < A("h3"):
        with at(cr, 360, 620, max(0.6, pop(t, A("h2", "hanoi"), 0.3)) * 0.75, rot=-0.03):
            shape(cr, rrect_pts(-230, -95, 460, 190, 18, 14), hexc("#fdf6e3"), seed=510, amp=0.5, lw=5)
            write(cr, [("HANOI", INK)], 0, -14, 64, align="center", bold=True)
            write(cr, [("1902", RED)], 0, 58, 54, align="center", bold=True)
        if t >= A("h2", "france"):
            with at(cr, 560, 720, max(0.6, pop(t, A("h2", "france"), 0.25)) * 0.8, rot=0.08):   # a small French flag
                for k, col in enumerate(("#2c4fa3", "#ffffff", "#d8323c")):
                    shape(cr, rrect_pts(-60 + k * 40, -30, 40, 60, 2, 6), hexc(col), seed=520 + k, amp=0.2, lw=2.5)
    hl(cr, t, [("new ", INK), ("SEWERS", BLUE)], 215, 68, A("h3", "sewers"), end=A("h3", "rats.") - 0.05, bold=True)
    hl(cr, t, [("...full of ", INK), ("RATS", RED)], 215, 70, A("h3", "rats."), bold=True)


def poster(cr, x, y, lines, s=1.0):
    with at(cr, x, y, s, rot=-0.03):
        shape(cr, rrect_pts(-170, -110, 340, 220, 10, 14), hexc("#fdf6e3"), seed=600, amp=0.5, lw=5)
        for k, (txt, col, size) in enumerate(lines):
            write(cr, [(txt, col)], 0, -50 + k * 66, size, align="center", bold=True)


def scene_bounty(cr, t, tl):
    A = tl.at
    keys = [(A("h4") - 0.2, (1.55, 360, 800)), (A("h4", "offer."), (1.6, 370, 780)), (A("h5"), (1.55, 360, 800)),
            (A("h5", "tail."), (1.7, 430, 800))]
    bg(cr, t, keys)
    street(cr)
    lines = [("REWARD", RED, 46), ("1 cent", INK, 54), ("per rat", INK, 40)]
    if t >= A("h5", "tail."):
        lines = [("REWARD", RED, 46), ("1 cent", INK, 54), ("per TAIL", RED, 40)]
    if t >= A("h4", "offer."):
        poster(cr, 400, 660, lines, max(0.6, pop(t, A("h4", "offer."), 0.3)) * 0.75)
    person(cr, OFFICIAL, 230, 960, t, facing=1, arms=("point", "hip") if t >= A("h4", "offer.") else ("hip", "hip"),
           eyes="wide" if t < A("h4", "so") else "dot", mouth="o" if t < A("h4", "so") else "smile", scale=1.15)
    if t >= A("h5"):
        hand = A("h5", "tail.")
        person(cr, HUNTER, 560, 960, t, facing=-1, arms=("hold", "down"), eyes="happy", mouth="grin", scale=1.15)
        if t >= hand:
            line(cr, [(500, 760), (470, 700), (490, 650)], 6, hexc("#d9a0a0"), seed=610, amp=0.3)
            coin(cr, lerp(270, 470, ease_out(seg(t, hand + 0.3, hand + 0.8))), 760, 0.8, seed=611)
    if A("h4", "plague.") <= t < A("h4", "so"):
        stamp(cr, t, A("h4", "plague."), "PLAGUE?!", dur=0.7, y=330)
    hl(cr, t, [("1 cent ", GREEN), ("per rat", INK)], 215, 70, A("h4", "one"), end=A("h5") - 0.05, bold=True)
    hl(cr, t, [("just bring the ", INK), ("TAIL", RED)], 215, 66, A("h5", "tail."), bold=True)


def scene_tailless(cr, t, tl):
    A = tl.at
    keys = [(A("h6") - 0.2, (1.55, 360, 800)), (A("h6", "rats"), (1.8, 360, 860)), (A("h7"), (1.55, 360, 800)),
            (A("h7", "free"), (1.6, 410, 840)), (A("h7", "tails", nth=2), (1.55, 360, 800))]
    bg(cr, t, keys)
    street(cr)
    if t < A("h7"):   # tailless rats running around
        for k in range(5):
            rat(cr, t, (k * 170 + t * 200) % 900 - 80, 880 + (k % 2) * 70, 0.85, facing=1, tail=False, run=t,
                seed=k * 9)
        if t >= A("h6", "no"):
            stamp(cr, t, A("h6", "no"), "NO TAILS?!", dur=0.8, y=330)
    else:
        person(cr, HUNTER, 270, 960, t, facing=1, arms=("hold", "hold"), eyes="sly", mouth="smirk", scale=1.15)
        tails_bundle(cr, 220, 760, 3 + int(min(5, max(0, t - A("h7", "tails", nth=2)) * 6)), 0.8)
        # the released rat runs off and has babies
        rx = lerp(300, 520, ease_out(seg(t, A("h7", "go."), A("h7", "go.") + 0.8)))
        rat(cr, t, rx, 900, 0.9, facing=1, tail=False, run=t, seed=70)
        if t >= A("h7", "baby"):
            for k in range(min(6, int((t - A("h7", "baby")) * 8) + 1)):
                rat(cr, t, 470 + (k % 3) * 80, 1000 + (k // 3) * 60, 0.5, facing=-1 if k % 2 else 1, seed=80 + k)
    hl(cr, t, [("rats with ", INK), ("NO TAILS", RED)], 215, 66, A("h6", "rats"), end=A("h7") - 0.05, bold=True)
    hl(cr, t, [("cut the tail... ", INK), ("let it go", RED)], 215, 60, A("h7"), end=A("h7", "free") - 0.05, bold=True)
    hl(cr, t, [("free rat = ", INK), ("MORE TAILS", GREEN)], 215, 64, A("h7", "free"), bold=True)


def scene_farm(cr, t, tl):
    A = tl.at
    keys = [(A("h8") - 0.2, (1.55, 380, 820)), (A("h8", "farms"), (1.6, 410, 840))]
    bg(cr, t, keys, color=hexc("#dff0d0"))
    shape(cr, [(-600, 760), (1400, 760), (1400, 2200), (-600, 2200)], hexc("#a9cf7f"), seed=700, amp=0.5, lw=4)
    # the pen
    shape(cr, rrect_pts(260, 760, 420, 280, 12, 14), hexc("#c9a77c"), seed=701, amp=0.5, lw=4)
    for k in range(12):
        rat(cr, t, 300 + (k % 4) * 100, 820 + (k // 4) * 80, 0.6, facing=1 if k % 2 else -1, run=t * 0.5, seed=k * 5)
    for k in range(9):
        line(cr, [(260 + k * 52, 740), (260 + k * 52, 1050)], 6, hexc("#6d4524"), seed=710 + k, amp=0.2)
    with at(cr, 470, 690, max(0.6, pop(t, A("h8", "farms"), 0.3)) * 0.85, rot=-0.05):
        shape(cr, rrect_pts(-130, -40, 260, 80, 8, 12), hexc("#fdf6e3"), seed=720, amp=0.4, lw=4)
        write(cr, [("RAT FARM", RED)], 0, 14, 44, align="center", bold=True)
    person(cr, INSPECTOR, 220, 980, t, facing=1, arms=("face", "down"), eyes="wide", mouth="o", sweat=True, scale=1.15)
    hl(cr, t, [("actual ", INK), ("RAT FARMS", RED)], 215, 70, A("h8", "farms"), bold=True)


def scene_name(cr, t, tl):
    A = tl.at
    keys = [(A("h9") - 0.2, (1.55, 360, 800)), (A("h9", "pay"), (1.55, 360, 810))]
    bg(cr, t, keys)
    street(cr)
    with at(cr, 360, 630, max(0.6, pop(t, A("h9", "perverse"), 0.3)) * 0.75, rot=-0.03):
        shape(cr, rrect_pts(-260, -90, 520, 180, 18, 14), hexc("#fdf6e3"), seed=800, amp=0.5, lw=5)
        write(cr, [("PERVERSE", RED)], 0, -14, 60, align="center", bold=True)
        write(cr, [("INCENTIVE", INK)], 0, 56, 56, align="center", bold=True)
    if t >= A("h9", "pay"):   # pay for tails -> more rats
        with at(cr, 360, 800, 0.75):
            coin(cr, -170, 0, 1.2, seed=810)
            line(cr, [(-110, 0), (40, 0)], 8, INK, seed=811, amp=0.3)
            line(cr, [(15, -22), (42, 0), (15, 22)], 8, INK, seed=812, amp=0.2)
            for k in range(3):
                rat(cr, t, 120 + (k % 2) * 60, -30 + k * 30, 0.55, seed=820 + k)
    for k in range(4):
        rat(cr, t, (k * 230 + t * 180) % 900 - 80, 900, 0.8, facing=1, tail=bool(k % 2), run=t, seed=830 + k)
    hl(cr, t, [("pay for the ", INK), ("WRONG", RED), (" thing", INK)], 215, 60, A("h9", "pay"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("h10") - 0.2, (1.55, 360, 800)), (A("h10", "farmed"), (1.8, 280, 820)), (A("h10", "honest."), (1.55, 360, 800))]
    bg(cr, t, keys)
    street(cr)
    person(cr, HUNTER, 280, 960, t, facing=1, arms=("thumb", "hold"), eyes="sly", mouth="grin", scale=1.2)
    tails_bundle(cr, 230, 760, 7, 0.9)
    for k in range(3):
        rat(cr, t, 470 + k * 90, 900 + (k % 2) * 50, 0.7, facing=-1, tail=False, seed=900 + k)
    for k, (lab, col, x) in enumerate((("YES", GREEN, 200), ("NO", hexc("#e0483d"), 520))):
        if t >= A("h10", "honest."):
            with at(cr, x, 1060, max(0.6, pop(t, A("h10", "honest.") + k * 0.12, 0.25)) * 0.7):
                shape(cr, rrect_pts(-110, -46, 220, 92, 46, 14), col, seed=950 + k, amp=0.3, lw=4)
                write(cr, [(lab, WHITE)], 0, 16, 48, align="center", bold=True)
    hl(cr, t, [("would YOU ", INK), ("farm", RED), (" the rats?", INK)], 215, 58, A("h10"), bold=True, underline=True)
    stamp(cr, t, A("h10", "honest.", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "city": scene_city, "bounty": scene_bounty, "tailless": scene_tailless, "farm": scene_farm,
     "name": scene_name, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
