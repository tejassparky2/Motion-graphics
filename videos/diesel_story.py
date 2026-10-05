"""Diesel record and the G7 release, told the Interestingly Strange way: characters act it out in drawn places,
the camera cuts to a new angle on the key words, handwritten headlines on top (owner, 5 Oct 2026).

Same approved facts as videos/diesel_g7_release.py (sources there and in METADATA), as of 5 October 2026:
- AAA diesel record $6.52 a gallon on 22 Sep 2026 (AP via BNN Bloomberg; TIME).
- The war involving Iran disrupted shipping through the Strait of Hormuz; diesel scarce worldwide (Al Jazeera; TIME).
- 2 Oct 2026: G7 and partners to release up to 100 million barrels over four months; diesel frontloaded within the
  first 20 days (AP; Al Jazeera; ABC News).
- Experts: diesel could fall around 25 cents a gallon within weeks (Bordoff in TIME; Lynch via AP: 25-50 cents).
- Stopgap; short-lived; reserves must be refilled later (Capital Economics via Al Jazeera; ABC News).
The seven officials are generic cartoon people, not portraits of real leaders.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import (INK, RED, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from motion.news import source_tag
from motion.newsprops import barrel, calendar, truck, wallet
from motion.story import buttons

NARRATOR = dict(speed=0.95)
TAIL = 0.9

SCRIPT = [
    dict(id="f1", scene="town", text="Almost everything you buy rode on a diesel truck."),
    dict(id="f2", scene="town", text="And diesel just hit a record."),
    dict(id="f3", scene="town", text="[Six dollars and fifty-two cents a gallon.|$6.52 a gallon.] "
                                     "On September twenty-second."),
    dict(id="f4", scene="sea", text="Why? The war with Iran choked oil shipping through the Strait of Hormuz."),
    dict(id="f5", scene="sea", text="And diesel got scarce around the world."),
    dict(id="f6", scene="summit", text="So on October second, the G7 made a move."),
    dict(id="f7", scene="summit", text="Up to [a hundred million|100 million] barrels. Out of emergency stockpiles. "
                                       "Over four months."),
    dict(id="f8", scene="summit", text="And most of the diesel comes first. Within twenty days."),
    dict(id="f9", scene="station", text="Will you actually pay less?"),
    dict(id="f10", scene="station", text="Two energy experts estimate diesel could drop around twenty-five cents a "
                                         "gallon. In a few weeks."),
    dict(id="f11", scene="station", text="But there is a catch."),
    dict(id="f12", scene="station", text="It's a stopgap. The stockpiles will have to be refilled later."),
    dict(id="f13", scene="station", text="So cheaper soon. But maybe not for long."),
    dict(id="f14", scene="end", text="Have you noticed higher prices at the store? Tell me in the comments."),
]

METADATA = dict(
    title="Diesel Hit a Record. Here's the Plan to Bring It Down ⛽",
    alt_titles=["Why Your Groceries Cost More: Diesel Explained", "The G7's 100 Million Barrel Plan, Explained"],
    description="""Diesel hit a record $6.52 a gallon on 22 September 2026 (AAA). Almost everything in stores travels by diesel truck, so it shows up in prices. ⛽

Why: the war involving Iran disrupted oil shipping through the Strait of Hormuz, and diesel became scarce worldwide.
The plan: on 2 October 2026 the G7 agreed to release up to 100 million barrels of oil and diesel from emergency reserves over four months, with most of the diesel in the first 20 days.
Will it help? Energy experts estimate diesel could fall around 25 cents a gallon within weeks. But it's a stopgap: the reserves have to be refilled later.

Facts as of 5 October 2026.

💬 Have you noticed higher prices at the store? 👇

Sources:
• AP via BNN Bloomberg (2 Oct 2026): https://www.bnnbloomberg.ca/markets/oil/2026/10/02/g7-nations-will-release-100-million-barrels-of-oil-and-diesel-fuel-after-prices-soar/
• TIME (3 Oct 2026): https://time.com/article/2026/10/03/the-g7-is-releasing-emergency-fuel-reserves-how-much-will-it-help-americans-/
• Al Jazeera (3 Oct 2026): https://www.aljazeera.com/news/2026/10/3/g7-to-release-100-million-barrels-of-oil-and-diesel-will-it-curb-prices
• ABC News (3 Oct 2026): https://www.abc.net.au/news/2026-10-03/g7-to-release-100m-barrels-oil-in-bid-to-curb-soaring-prices/107224282""",
    hashtags=["#Diesel", "#GasPrices", "#News"],
    tags=["diesel prices", "gas prices", "g7", "oil reserves", "strait of hormuz", "fuel prices", "inflation",
          "grocery prices", "world news", "news explained"],
    pinned_comment="Have you noticed higher prices at the store this fall? Yes or no? 👇",
)

GREEN = hexc("#2e9e52")
GOLD = hexc("#f2b632")
NAVY = hexc("#23346b")
ORANGE = hexc("#e0a03a")
SKY = hexc("#a9dcf5")
GROUND = 900


def sky_ground(cr, ground=hexc("#c9b48a")):
    cr.set_source_rgba(*SKY)
    cr.paint()
    for k, (cx, cy) in enumerate([(120, 330), (620, 290), (1100, 340), (1500, 300)]):
        blob(cr, cx, cy, 70, 26, WHITE, 15000 + k, amp=0.8, lw=0, stroke=None)
    sharp_shape(cr, [(-900, GROUND), (2200, GROUND), (2200, 2000), (-900, 2000)], ground, seed=15010, amp=0.8, lw=4)


# ---------------------------------------------------------------- town: grocery store, road, gas station
def store(cr):
    shape(cr, rrect_pts(-60, 440, 470, 460, 6, 18), hexc("#f1dfbd"), seed=15100, amp=0.6, lw=5)
    shape(cr, rrect_pts(-80, 410, 510, 70, 6, 18), GREEN, seed=15101, amp=0.5, lw=5)
    write(cr, [("GROCERY", WHITE)], 175, 462, 48, align="center", bold=True)
    shape(cr, rrect_pts(-30, 520, 260, 200, 6, 16), hexc("#cdeaf7"), seed=15102, amp=0.4, lw=4)
    for row in range(2):
        line(cr, [(-20, 600 + row * 80), (220, 600 + row * 80)], 6, hexc("#8e5a2e"), 15103 + row, amp=0.2)
        for k in range(5):
            col = [hexc("#e0483d"), GREEN, GOLD, hexc("#4fb3e8"), ORANGE][(k + row) % 5]
            shape(cr, rrect_pts(-10 + k * 46, 556 + row * 80, 30, 42, 4, 10), col, seed=15110 + k + row * 7, amp=0.3,
                  lw=3)
    shape(cr, rrect_pts(280, 600, 100, 300, 6, 14), hexc("#8e5a2e"), seed=15130, amp=0.4, lw=4)


def cart(cr, x, y, s=1.0, full=1.0):
    with at(cr, x, y, s):
        shape(cr, [(-70, -90), (70, -90), (56, -30), (-58, -30)], hexc("#c9ccd2"), seed=15140, amp=0.4, lw=4)
        line(cr, [(-70, -90), (-96, -120)], 6, INK, 15141, amp=0.2)
        line(cr, [(-58, -30), (-50, -10)], 4, INK, 15142, amp=0.2)
        for wx in (-44, 44):
            blob(cr, wx, -6, 10, 10, INK, 15143 + wx, amp=0.2, lw=0, stroke=None)
        for k, col in enumerate((hexc("#e0483d"), GREEN, GOLD, hexc("#8a63d2"))):
            if full * 4 > k:
                shape(cr, rrect_pts(-56 + k * 28, -128, 24, 44, 4, 10), col, seed=15150 + k, amp=0.3, lw=3)


def price_board(cr, x, price, col=RED, arrow=None):
    line(cr, [(x, GROUND), (x, 560)], 12, INK, 15200, amp=0.2)
    line(cr, [(x, GROUND), (x, 560)], 6, hexc("#8f939b"), 15200, amp=0.2)
    shape(cr, rrect_pts(x - 130, 360, 260, 220, 12, 14), NAVY, seed=15201, amp=0.4, lw=5)
    write(cr, [("DIESEL", WHITE)], x, 410, 36, align="center", bold=True)
    shape(cr, rrect_pts(x - 112, 430, 224, 120, 8, 12), hexc("#111318"), seed=15202, amp=0.2, lw=0, stroke=None)
    write(cr, [(price, col)], x, 518, 74, align="center", bold=True)
    if arrow == "down":
        shape(cr, [(x + 150, 430), (x + 190, 430), (x + 190, 490), (x + 215, 490), (x + 170, 545), (x + 125, 490),
                   (x + 150, 490)], GREEN, seed=15203, amp=0.3, lw=4)
    elif arrow == "maybe":
        write(cr, [("?", hexc("#8a63d2"))], x + 175, 520, 110, align="center", bold=True, halo=WHITE)


def gas_station(cr, t):
    shape(cr, rrect_pts(760, 560, 420, 40, 6, 14), hexc("#e0483d"), seed=15300, amp=0.4, lw=5)
    for px in (790, 1150):
        line(cr, [(px, 600), (px, GROUND)], 12, hexc("#c9ccd2"), 15301 + px, amp=0.2)
    shape(cr, rrect_pts(900, 700, 90, 200, 10, 12), hexc("#e0483d"), seed=15310, amp=0.4, lw=4)
    shape(cr, rrect_pts(912, 716, 66, 50, 6, 10), WHITE, seed=15311, amp=0.3, lw=3)
    write(cr, [("DIESEL", WHITE)], 945, 820, 18, align="center", bold=True)
    line(cr, [(990, 760), (1020, 790), (1020, 860)], 6, INK, 15312, amp=0.2)


def town_set(cr, t):
    sky_ground(cr)
    for k in range(-2, 18):   # road markings
        line(cr, [(k * 120, 960), (k * 120 + 60, 960)], 8, GOLD, 15400 + k, amp=0.2)
    store(cr)
    gas_station(cr, t)


def scene_town(cr, t, tl):
    A = tl.at
    keys = [(0, (1.7, 330, 837)), (A("f1", "everything"), (1.4, 330, 872)), (A("f1", "diesel"), (1.2, 560, 917)),
            (A("f1", "truck"), (1.6, 600, 900)),
            (A("f2"), (1.0, 1060, 880)), (A("f2", "record"), (1.6, 1270, 682)),
            (A("f3"), (1.5, 1270, 697)), (A("f3", "September"), (1.8, 1080, 828))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    town_set(cr, t)
    person(cr, "shopper", 320, 905, t, facing=1, arms=("hold", "hip"), eyes="dot",
           mouth="o" if A("f1", "truck") <= t < A("f2") else "smile")
    cart(cr, 420, 905, 1.0)
    u = ease_out(seg(t, A("f1", "diesel") - 0.2, A("f1", "truck") + 0.3))
    if u > 0:
        truck(cr, lerp(-250, 610, u), 860, 1.2)
        if u < 1:
            for k in range(3):
                line(cr, [(lerp(-250, 610, u) - 200 - k * 30, 800 + k * 20), (lerp(-250, 610, u) - 150 - k * 30,
                                                                           800 + k * 20)], 4, WHITE, 15500 + k, amp=0.2)
    v = 4.0 + 2.52 * ease_out(seg(t, A("f2"), A("f2", "record") + 0.3))
    price_board(cr, 1260, f"${v:.2f}")
    shocked = t >= A("f2", "record")
    person(cr, "trucker", 1060, 905, t, facing=-1, arms=("face", "hip") if shocked else ("hip", "hip"),
           eyes="wide" if shocked else "dot", mouth="o" if shocked else "smile", sweat=shocked,
           shake=1.5 if A("f2", "record") <= t < A("f2", "record") + 0.4 else 0)
    if t >= A("f3", "September"):
        with at(cr, 1080, 600, pop(t, A("f3", "September"), 0.2) or 0.01, rot=-0.06):
            shape(cr, rrect_pts(-110, -34, 220, 68, 8, 12), WHITE, seed=15510, amp=0.4, lw=4, stroke=RED)
            write(cr, [("22 SEP 2026", RED)], 0, 14, 38, align="center", bold=True)
        cue("thud", t, A("f3", "September"))
    hl(cr, t, [("almost ", INK), ("EVERYTHING", RED)], 215, 70, A("f1", "everything"), end=A("f1", "diesel") - 0.05,
       bold=True)
    hl(cr, t, [("rode on a ", INK), ("DIESEL", RED), (" truck", INK)], 215, 62, A("f1", "diesel"),
       end=A("f2") - 0.05, bold=True)
    hl(cr, t, [("a new ", INK), ("RECORD", RED)], 215, 84, A("f2", "record"), end=A("f3") - 0.05, bold=True)
    hl(cr, t, [("$6.52", RED), (" a gallon", INK)], 215, 80, A("f3"), bold=True)
    if t >= A("f3"):
        source_tag(cr, t, A("f3"), "AAA via AP", y=280)
    if A("f2", "record") <= t < A("f3"):
        stamp(cr, t, A("f2", "record"), "RECORD!", dur=A("f3") - A("f2", "record"), y=560)


# ---------------------------------------------------------------- sea: tankers stuck at the strait
def tanker(cr, x, y, s, seed, captain=None, t=0.0):
    with at(cr, x, y + 4 * math.sin(t * 2 + seed), s):
        shape(cr, [(-150, -10), (150, -10), (120, 50), (-130, 50)], hexc("#555a66"), seed=seed, amp=0.4, lw=5)
        shape(cr, rrect_pts(80, -90, 60, 80, 6, 12), WHITE, seed=seed + 1, amp=0.3, lw=4)
        for k in range(4):
            blob(cr, -110 + k * 52, -24, 22, 14, ORANGE, seed + 2 + k, amp=0.3, lw=3)


def sea_set(cr, t):
    cr.set_source_rgba(*SKY)
    cr.paint()
    sharp_shape(cr, [(-900, 760), (2200, 760), (2200, 2000), (-900, 2000)], hexc("#5f9fd8"), seed=15600, amp=0.6, lw=4)
    for k in range(12):
        line(cr, [(-400 + k * 180, 820 + 20 * (k % 3)), (-340 + k * 180, 820 + 20 * (k % 3))], 4,
             hexc("#ffffff", 0.6), 15610 + k, amp=0.6)
    shape(cr, [(880, 760), (900, 420), (1000, 380), (1060, 760)], hexc("#c9a777"), seed=15620, amp=1.0, lw=5)
    shape(cr, [(1240, 760), (1270, 400), (1400, 360), (1700, 400), (1700, 760)], hexc("#c9a777"), seed=15621,
          amp=1.0, lw=5)
    shape(cr, rrect_pts(960, 300, 300, 70, 8, 12), WHITE, seed=15622, amp=0.4, lw=4)
    write(cr, [("STRAIT OF HORMUZ", INK)], 1110, 346, 28, align="center", bold=True)


def scene_sea(cr, t, tl):
    A = tl.at
    keys = [(A("f4") - 0.2, (0.9, 600, 904)), (A("f4", "war"), (1.6, -220, 737)), (A("f4", "shipping"), (1.1, 400, 878)),
            (A("f4", "Strait"), (1.3, 1130, 760)), (A("f5"), (0.75, 650, 890)), (A("f5", "world"), (1.1, 900, 860))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    sea_set(cr, t)
    blocked = t >= A("f4", "choked")
    for k in range(4):
        x0 = -200 + k * 330
        x = x0 + (0 if blocked else 80 * seg(t, A("f4"), A("f4") + 3))
        tanker(cr, x, 760, 1.0, 15700 + k * 9, t=t)
        if k == 0:   # the captain on the first tanker's deck
            person(cr, "oldman", x - 60, 752, t, scale=0.9, facing=1, arms=("chin", "hip"),
                   eyes="wide" if blocked else "dot", mouth="o" if blocked else "flat")
    if blocked:
        u = ease_out(seg(t, A("f4", "choked"), A("f4", "choked") + 0.3))
        line(cr, [(1100, 520), (1100 + 80 * u, 520 + 200 * u)], 16, RED, 15730, amp=0.2)
        line(cr, [(1180, 520), (1180 - 80 * u, 520 + 200 * u)], 16, RED, 15731, amp=0.2)
        cue("hit", t, A("f4", "choked"))
    if t >= A("f5"):
        for k, x in enumerate((-260, 1500, 360)):
            with at(cr, x, 620 if k != 2 else 470, pop(t, A("f5") + 0.2 * k, 0.25) or 0.01):
                shape(cr, rrect_pts(-90, -40, 180, 80, 8, 12), WHITE, seed=15740 + k, amp=0.3, lw=4)
                write(cr, [("NO DIESEL", RED)], 0, 14, 30, align="center", bold=True)
    hl(cr, t, [("WHY?", RED)], 215, 110, A("f4"), end=A("f4", "war") - 0.05, bold=True)
    hl(cr, t, [("WAR", RED), (" with Iran", INK)], 215, 80, A("f4", "war"), end=A("f4", "Strait") - 0.05, bold=True)
    hl(cr, t, [("shipping ", INK), ("BLOCKED", RED)], 215, 74, A("f4", "Strait"), end=A("f5") - 0.05, bold=True)
    hl(cr, t, [("diesel ", INK), ("SCARCE", RED), (" worldwide", INK)], 215, 58, A("f5"), bold=True)


# ---------------------------------------------------------------- summit room and the emergency warehouse
OFFICIALS = ["principal", "teacher", "hilbert", "sub", "oldman", "mia", "sam"]


def summit_set(cr, t):
    cr.set_source_rgba(*hexc("#e9e2d0"))
    cr.paint()
    for k in range(-4, 10):
        line(cr, [(k * 100, 250), (k * 100, 880)], 4, hexc("#ddd3bc"), 15800 + k, amp=0.4)
    sharp_shape(cr, [(-900, 880), (2200, 880), (2200, 2000), (-900, 2000)], hexc("#7b5a3f"), seed=15810, amp=0.8, lw=4)
    shape(cr, rrect_pts(150, 330, 320, 130, 10, 14), NAVY, seed=15820, amp=0.4, lw=5)
    write(cr, [("G7", GOLD)], 310, 430, 100, align="center", bold=True)
    # the warehouse on the right
    shape(cr, rrect_pts(900, 380, 640, 520, 6, 18), hexc("#a9adb5"), seed=15830, amp=0.6, lw=5)
    write(cr, [("EMERGENCY STOCKPILE", WHITE)], 1220, 450, 40, align="center", bold=True)


def scene_summit(cr, t, tl):
    A = tl.at
    keys = [(A("f6") - 0.2, (1.0, 330, 830)), (A("f6", "G7"), (1.7, 310, 589)), (A("f6", "move"), (1.4, 330, 875)),
            (A("f7"), (0.9, 1220, 840)), (A("f7", "stockpiles"), (1.3, 1220, 888)), (A("f7", "four"), (1.6, 700, 707)),
            (A("f8"), (1.2, 1250, 933)), (A("f8", "twenty"), (1.6, 700, 707))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    summit_set(cr, t)
    for k, who in enumerate(OFFICIALS):
        x = 40 + k * 90
        vote = t >= A("f6", "move") + 0.05 * k
        person(cr, who, x, 905, t, scale=0.8, facing=1, arms=("cheer", "hip") if vote else ("hip", "hip"),
               eyes="happy" if vote else "dot", mouth="smile")
    shape(cr, rrect_pts(-40, 830, 680, 70, 8, 14), hexc("#8e5a2e"), seed=15840, amp=0.4, lw=5)   # table front
    # warehouse doors slide open, barrels pile up
    door = ease_out(seg(t, A("f7"), A("f7") + 0.6))
    n = int(18 * ease_out(seg(t, A("f7"), A("f7", "stockpiles") + 0.3)))
    for k in range(n):
        row, col = divmod(k, 6)
        barrel(cr, 990 + col * 90, 850 - row * 90, 1.0, seed=15900 + k)
    for side in (-1, 1):
        dx = side * 300 * door
        shape(cr, rrect_pts(1220 - 300 + (0 if side < 0 else 300) + dx, 480, 300, 420, 4, 14), hexc("#8f939b"),
              seed=15850 + side, amp=0.4, lw=4)
    if t >= A("f7", "four"):
        with at(cr, 700, 520, pop(t, A("f7", "four"), 0.2) or 0.01):
            calendar(cr, 0, 0, "MONTHS", "4", 1.0)
    if t >= A("f8"):
        u = (t - A("f8")) * 0.6
        for k in range(3):
            bx = 1000 + ((u * 300 + k * 160) % 520)
            barrel(cr, bx, 850, 1.1, col=ORANGE, label="DIESEL", seed=15960 + k)
    if t >= A("f8", "twenty"):
        with at(cr, 700, 520, pop(t, A("f8", "twenty"), 0.2) or 0.01):
            calendar(cr, 0, 0, "WITHIN", "20", 1.0)
            write(cr, [("days", INK)], 0, 116, 34, align="center", bold=True)
    hl(cr, t, [("2 OCT 2026", RED)], 215, 80, A("f6"), end=A("f6", "G7") - 0.05, bold=True)
    hl(cr, t, [("the ", INK), ("G7", NAVY), (" acts", INK)], 215, 84, A("f6", "G7"), end=A("f7") - 0.05, bold=True)
    hl(cr, t, [("100 MILLION", RED), (" barrels", INK)], 215, 66, A("f7"), end=A("f7", "four") - 0.05, bold=True)
    hl(cr, t, [("over ", INK), ("4 months", RED)], 215, 80, A("f7", "four"), end=A("f8") - 0.05, bold=True)
    hl(cr, t, [("DIESEL", RED), (" first", INK)], 215, 84, A("f8"), bold=True)


# ---------------------------------------------------------------- back at the station: experts, the catch
def big_tank(cr, x, level):
    shape(cr, rrect_pts(x - 140, 430, 280, 470, 40, 16), WHITE, seed=16000, amp=0.5, lw=5)
    h = 440 * max(0.0, level)
    if h > 4:
        shape(cr, rrect_pts(x - 126, 886 - h, 252, h, 28, 14), hexc("#3a6ea5"), seed=16001, amp=0.3, lw=0,
              stroke=None)
    write(cr, [("RESERVE", INK)], x, 420, 34, align="center", bold=True)


def scene_station(cr, t, tl):
    A = tl.at
    keys = [(A("f9") - 0.2, (1.8, 1060, 828)), (A("f10"), (1.2, 900, 890)), (A("f10", "drop"), (1.6, 1300, 682)),
            (A("f10", "weeks"), (1.8, 1060, 828)), (A("f11"), (1.0, 1560, 885)), (A("f12", "refilled"), (1.2, 1560, 848)),
            (A("f13"), (1.6, 1300, 682)), (A("f13", "maybe"), (1.5, 1320, 690))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    town_set(cr, t)
    big_tank(cr, 1560, 1 - seg(t, A("f12"), A("f12", "refilled")))
    drop = ease_out(seg(t, A("f10", "drop"), A("f10", "drop") + 0.9))
    price = 6.52 - 0.25 * drop
    if t >= A("f13"):
        price_board(cr, 1260, "$6.27", GREEN, arrow="maybe" if t >= A("f13", "maybe") else "down")
    else:
        price_board(cr, 1260, f"${price:.2f}", GREEN if drop > 0 else RED, arrow="down" if drop > 0 else None)
    happy = A("f10", "weeks") <= t < A("f11")
    person(cr, "trucker", 1060, 905, t, facing=-1,
           arms=("hold", "hip") if t < A("f10") else (("cheer", "hip") if happy else ("chin", "hip")),
           eyes="happy" if happy else ("sad" if t >= A("f11") else "dot"), mouth="grin" if happy else "flat")
    if A("f9") <= t < A("f10"):
        wallet(cr, 980, 640, pop(t, A("f9"), 0.2) or 0.01)
        write(cr, [("?", hexc("#8a63d2"))], 1060, 600, 100, align="center", bold=True, halo=WHITE)
    if A("f10") <= t < A("f11"):
        for k, who in enumerate(("teacher", "oldman")):
            walk = seg(t, A("f10") + 0.1 * k, A("f10") + 0.8 + 0.1 * k)
            person(cr, who, lerp(560, 760 + k * 110, ease_out(walk)), 905, t, facing=1,
                   walk=t * 2.5 if walk < 1 else None, arms=("point", "hip"), eyes="dot",
                   mouth="o" if int(t * 10 + k) % 2 else "smile")
    hl(cr, t, [("will you ", INK), ("PAY LESS", GREEN), ("?", INK)], 215, 66, A("f9"), end=A("f10") - 0.05, bold=True)
    hl(cr, t, [("2 energy ", INK), ("EXPERTS", NAVY)], 215, 72, A("f10"), end=A("f10", "drop") - 0.05, bold=True)
    hl(cr, t, [("about ", INK), ("-25¢", GREEN), (" a gallon", INK)], 215, 66, A("f10", "drop"), end=A("f11") - 0.05,
       bold=True)
    if A("f10", "drop") <= t < A("f11"):
        source_tag(cr, t, A("f10", "drop"), "TIME; AP", y=280)
    hl(cr, t, [("the ", INK), ("CATCH", RED)], 215, 90, A("f11"), end=A("f12") - 0.05, bold=True)
    hl(cr, t, [("a ", INK), ("STOPGAP", RED)], 215, 90, A("f12"), end=A("f12", "refilled") - 0.05, bold=True)
    hl(cr, t, [("REFILL", RED), (" later", INK)], 215, 90, A("f12", "refilled"), end=A("f13") - 0.05, bold=True)
    hl(cr, t, [("cheaper ", GREEN), ("soon...", INK)], 215, 80, A("f13"), end=A("f13", "maybe") - 0.05, bold=True)
    hl(cr, t, [("not for ", INK), ("LONG?", RED)], 215, 84, A("f13", "maybe"), bold=True)
    if A("f12", "refilled") <= t < A("f13"):
        stamp(cr, t, A("f12", "refilled"), "REFILL LATER", dur=A("f13") - A("f12", "refilled"), y=560)


# ---------------------------------------------------------------- end: the shopper at the store
def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("f14") - 0.2, (1.7, 330, 837)), (A("f14", "store"), (1.3, 260, 819))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    town_set(cr, t)
    person(cr, "shopper", 320, 905, t, facing=1, arms=("hold", "hip"), eyes="wide", mouth="o")
    cart(cr, 420, 905, 1.0)
    with at(cr, 180, 640, pop(t, A("f14", "prices"), 0.25) or 0.01, rot=-0.05):   # a long receipt
        shape(cr, rrect_pts(-60, -140, 120, 280, 4, 12), WHITE, seed=16100, amp=0.4, lw=4)
        for k in range(7):
            line(cr, [(-44, -110 + k * 32), (30, -110 + k * 32)], 3, hexc("#a9adb5"), 16101 + k, amp=0.3)
        write(cr, [("TOTAL $$$", RED)], 0, 128, 22, align="center", bold=True)
    hl(cr, t, [("higher ", INK), ("PRICES", RED), ("?", INK)], 215, 84, A("f14"), bold=True, underline=True)
    buttons(cr, t, A("f14", "comments"), (("YES", GREEN), ("NO", RED)), y=470, s=0.85)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"town": scene_town, "sea": scene_sea, "summit": scene_summit, "station": scene_station,
     "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
