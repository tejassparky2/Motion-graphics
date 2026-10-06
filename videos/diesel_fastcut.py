"""Diesel record and the G7 release, as a fast-cut full animation (owner's test of the new format, 5 Oct 2026).

Same approved facts as videos/diesel_g7_release.py, told by one narrator over ~17 full-screen shots cut on the spoken
words (motion/fastcut.py).

Facts, as of 5 October 2026 (sources in METADATA and videos/diesel_g7_release.py):
- AAA diesel record $6.52 a gallon on 22 Sep 2026 (AP via BNN Bloomberg; TIME).
- The war involving Iran disrupted shipping through the Strait of Hormuz; diesel scarce worldwide (Al Jazeera; TIME).
- 2 Oct 2026: G7 and partners to release up to 100 million barrels over four months; diesel frontloaded within the
  first 20 days (AP; Al Jazeera; ABC News).
- Experts: diesel could fall around 25 cents a gallon within weeks (Bordoff in TIME; Lynch via AP: 25-50 cents).
- Stopgap; impact short-lived; reserves must be refilled later (Capital Economics via Al Jazeera; ABC News).
"""
import math

from motion.captions import captions
from motion.engine import INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, line, pop, rrect_pts, seg, shape, write
from motion.fastcut import run, shake, slam, sunburst
from motion.kit import stamp
from motion.news import date_stamp, globe, source_tag
from motion.newsprops import GREEN, NAVY, barrel, calendar, price_sign, strait, tank, truck, wallet
from motion.story import buttons

NARRATOR = dict(speed=0.95)
TAIL = 0.9

SCRIPT = [
    dict(id="f1", scene="main", text="Almost everything you buy rode on a diesel truck."),
    dict(id="f2", scene="main", text="And diesel just hit a record."),
    dict(id="f3", scene="main", text="[Six dollars and fifty-two cents a gallon.|$6.52 a gallon.] "
                                     "On September twenty-second."),
    dict(id="f4", scene="main", text="Why? The war with Iran choked oil shipping through the Strait of Hormuz."),
    dict(id="f5", scene="main", text="And diesel got scarce around the world."),
    dict(id="f6", scene="main", text="So on October second, the G7 made a move."),
    dict(id="f7", scene="main", text="Up to [a hundred million|100 million] barrels. Out of emergency stockpiles. "
                                     "Over four months."),
    dict(id="f8", scene="main", text="And most of the diesel comes first. Within twenty days."),
    dict(id="f9", scene="main", text="Will you actually pay less?"),
    dict(id="f10", scene="main", text="Two energy experts estimate diesel could drop around twenty-five cents a gallon. "
                                      "In a few weeks."),
    dict(id="f11", scene="main", text="But there is a catch."),
    dict(id="f12", scene="main", text="It's a stopgap. The stockpiles will have to be refilled later."),
    dict(id="f13", scene="main", text="So cheaper soon. But maybe not for long."),
    dict(id="f14", scene="main", text="Have you noticed higher prices at the store? Tell me in the comments."),
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

YELLOW = hexc("#ffd23f")
ORANGE = hexc("#ff8a3d")
SKY = hexc("#9fd6f2")
DARK = hexc("#23252f")


_TL = [None]


def _tl():
    return _TL[0]


# ---------------------------------------------------------------- props
def cart(c, x, y, s, t, t0):
    with at(c, x, y, s):
        shape(c, [(-150, -40), (150, -40), (120, 80), (-120, 80)], hexc("#c9ccd2"), seed=13000, amp=0.4, lw=5)
        for k in range(5):
            line(c, [(-140 + k * 70, -40), (-112 + k * 58, 80)], 3, hexc("#8f939b"), 13001 + k, amp=0.2)
        line(c, [(-150, -40), (-200, -100)], 7, INK, 13010, amp=0.2)
        for wx in (-90, 90):
            blob(c, wx, 110, 22, 22, INK, 13011 + wx, amp=0.2, lw=0, stroke=None)
        items = [(-90, -90, hexc("#e0483d"), 34, 50), (-20, -110, GREEN, 30, 70), (50, -95, YELLOW, 40, 52),
                 (110, -80, hexc("#8a63d2"), 26, 40), (-40, -60, ORANGE, 44, 30), (60, -55, hexc("#4fb3e8"), 40, 28)]
        for k, (ix, iy, col, rx, ry) in enumerate(items):
            sc = pop(t, t0 + 0.08 * k, 0.25)
            if sc > 0:
                with at(c, ix, iy, sc):
                    shape(c, rrect_pts(-rx, -ry, 2 * rx, 2 * ry, 10, 12), col, seed=13020 + k, amp=0.4, lw=4)


def pump(c, x, y, s, t, t0, needle=1.0):
    with at(c, x, y, s):
        shape(c, rrect_pts(-110, -220, 220, 380, 20, 14), hexc("#e0483d"), seed=13100, amp=0.5, lw=5)
        shape(c, rrect_pts(-80, -190, 160, 120, 10, 12), WHITE, seed=13101, amp=0.3, lw=4)
        c.save()
        c.new_path()
        c.arc(0, -110, 56, math.pi, 2 * math.pi)
        c.set_line_width(10)
        c.set_source_rgba(*hexc("#e8e2d4"))
        c.stroke()
        c.restore()
        a = math.pi + math.pi * min(1.0, needle) * ease_out(seg(t, t0, t0 + 0.6)) + 0.05 * math.sin(t * 40)
        line(c, [(0, -110), (50 * math.cos(a), -110 + 50 * math.sin(a))], 5, RED, 13102, amp=0.1)
        write(c, [("DIESEL", WHITE)], 0, 30, 46, align="center", bold=True)
        line(c, [(110, -40), (170, -10), (170, 120)], 9, INK, 13103, amp=0.3)
        shape(c, rrect_pts(150, 100, 40, 70, 8, 10), DARK, seed=13104, amp=0.3, lw=4)


def big_price(c, x, y, s, text, col=RED):
    with at(c, x, y, s):
        shape(c, rrect_pts(-230, -130, 460, 260, 24, 16), NAVY, seed=13200, amp=0.5, lw=6)
        shape(c, rrect_pts(-200, -70, 400, 160, 12, 14), hexc("#111318"), seed=13201, amp=0.3, lw=0, stroke=None)
        write(c, [("DIESEL / GALLON", hexc("#fbf3e1"))], 0, -88, 30, align="center", bold=True)
        write(c, [(text, col)], 0, 50, 120, align="center", bold=True)


def tanker(c, x, y, s, seed):
    with at(c, x, y, s):
        shape(c, [(-90, 0), (90, 0), (70, 36), (-80, 36)], hexc("#555a66"), seed=seed, amp=0.3, lw=4)
        shape(c, rrect_pts(40, -36, 40, 36, 4, 10), WHITE, seed=seed + 1, amp=0.2, lw=3)
        for k in range(3):
            blob(c, -60 + k * 36, -6, 14, 8, hexc("#e0a03a"), seed + 2 + k, amp=0.2, lw=2)


def hook(c, x, y, s, t):
    with at(c, x, y + 10 * math.sin(t * 3), s):
        line(c, [(0, -400), (0, 0)], 4, INK, 13300, amp=0.1)
        c.save()
        c.new_path()
        c.arc(-30, 0, 30, 0, math.pi)
        c.set_line_width(12)
        c.set_source_rgba(*hexc("#a9adb5"))
        c.stroke()
        c.restore()
        shape(c, [(-60, 0), (-70, -18), (-52, -6)], hexc("#a9adb5"), seed=13301, amp=0.1, lw=2)
        with at(c, -30, 60, 1.0, rot=0.1 * math.sin(t * 2)):   # a price tag on the hook
            shape(c, rrect_pts(-70, 0, 140, 70, 10, 12), WHITE, seed=13302, amp=0.3, lw=4)
            write(c, [("LOW PRICE", GREEN)], 0, 46, 26, align="center", bold=True)


def chart(c, x, y, s, u):
    with at(c, x, y, s):
        line(c, [(-260, 120), (260, 120)], 5, INK, 13400, amp=0.2)
        line(c, [(-260, 120), (-260, -150)], 5, INK, 13401, amp=0.2)
        pts = [(-240, -60), (-140, -100), (-60, -110), (20, -10), (100, 10)]
        n = max(2, int(len(pts) * min(1.0, u * 1.5)))
        line(c, pts[:n], 9, RED, 13402, amp=0.3)
        if u > 0.6:
            v = (u - 0.6) / 0.4
            c.save()
            c.set_dash([14, 12])
            line(c, [(100, 10), (100 + 140 * v, 10 - 120 * v)], 8, hexc("#8a63d2"), 13403, amp=0.2)
            c.restore()
            write(c, [("?", hexc("#8a63d2"))], 260, -110, 90, bold=True)
        write(c, [("diesel price", INK)], -110, 170, 30, align="center", bold=True)
        write(c, [("now", INK)], 100, 170, 28, align="center", bold=True)
        write(c, [("later", INK)], 230, 170, 28, align="center", bold=True)


def shelf(c, x, y, s):
    with at(c, x, y, s):
        for row in range(2):
            yy = -60 + row * 140
            line(c, [(-260, yy + 50), (260, yy + 50)], 10, hexc("#8e5a2e"), 13500 + row, amp=0.2)
            for k in range(5):
                col = [hexc("#e0483d"), GREEN, YELLOW, hexc("#4fb3e8"), ORANGE][(k + row) % 5]
                shape(c, rrect_pts(-240 + k * 100, yy - 40, 70, 90, 8, 12), col, seed=13510 + k + row * 9,
                      amp=0.3, lw=4)
                shape(c, rrect_pts(-232 + k * 100, yy + 52, 54, 26, 4, 10), WHITE, seed=13530 + k + row * 9,
                      amp=0.2, lw=3)
                write(c, [("$$", RED)], -205 + k * 100, yy + 72, 18, align="center", bold=True)


# ---------------------------------------------------------------- shots (screen space)
def s_cart(cr, t, t0, t1):
    sunburst(cr, t, YELLOW, hexc("#ffe27a"))
    cart(cr, 360, 560, 1.4, t, t0)
    slam(cr, t, t0 + 0.05, [("EVERYTHING", INK)], 300, 76)


def s_truck(cr, t, t0, t1):
    cr.set_source_rgba(*SKY)
    cr.paint()
    shape(cr, [(0, 640), (720, 640), (720, 1280), (0, 1280)], hexc("#6b6f78"), seed=13600, amp=0.4, lw=0, stroke=None)
    off = (t * 900) % 160
    for k in range(7):
        line(cr, [(k * 160 - off, 760), (k * 160 - off + 80, 760)], 10, YELLOW, 13601 + k, amp=0.1)
    u = ease_out(seg(t, t0, t0 + 0.5))
    tx = -300 + 660 * u
    for k in range(5):   # speed lines
        line(cr, [(tx - 220 - k * 30, 560 + k * 22), (tx - 120 - k * 30, 560 + k * 22)], 5, WHITE, 13610 + k, amp=0.2)
    truck(cr, tx, 640, 1.8)
    slam(cr, t, t0 + 0.1, [("DIESEL", RED), (" truck", INK)], 300, 70)


def s_pump(cr, t, t0, t1):
    tl = _tl()
    hit = tl.at("f2", "record")
    dx, dy = shake(t, hit, 14)
    sunburst(cr, t, hexc("#ffb3a7"), hexc("#ffc9bf"))
    cr.save()
    cr.translate(dx, dy)
    pump(cr, 360, 620, 1.3, t, t0, needle=1.0 if t >= hit else 0.5)
    cr.restore()
    slam(cr, t, hit, [("RECORD!", RED)], 300, 96)


def s_price(cr, t, t0, t1):
    tl = _tl()
    dx, dy = shake(t, t0 + 0.05, 16)
    cr.set_source_rgba(*DARK)
    cr.paint()
    cr.save()
    cr.translate(dx, dy)
    v = 4.00 + 2.52 * ease_out(seg(t, t0, t0 + 0.7))
    big_price(cr, 360, 520, 1.25, f"${v:.2f}")
    cr.restore()
    source_tag(cr, t, t0 + 0.3, "AAA via AP")


def s_date(cr, t, t0, t1):
    sunburst(cr, t, hexc("#ffb3a7"), hexc("#ffc9bf"))
    with at(cr, 360, 580, pop(t, t0, 0.25) * 2.2, rot=-0.04):
        calendar(cr, 0, 0, "SEPTEMBER", "22", 1.0)
    slam(cr, t, t0 + 0.25, [("ALL-TIME HIGH", RED)], 300, 70)


def s_why(cr, t, t0, t1):
    cr.set_source_rgba(*INK)
    cr.paint()
    slam(cr, t, t0 + 0.02, [("WHY?", YELLOW)], 600, 200, halo=None)


def s_strait(cr, t, t0, t1):
    tl = _tl()
    cr.set_source_rgba(*hexc("#7fb3e8"))
    cr.paint()
    shape(cr, [(-20, 240), (740, 240), (740, 480), (420, 520), (300, 470), (-20, 540)], hexc("#e8d9a8"),
          seed=13800, amp=1.0, lw=5)
    shape(cr, [(-20, 900), (740, 900), (740, 640), (440, 620), (300, 660), (-20, 610)], hexc("#e8d9a8"),
          seed=13801, amp=1.0, lw=5)
    blocked = t >= tl.at("f4", "choked")
    for k in range(4):
        x = 40 + k * 150 + (0 if blocked else 60 * seg(t, t0, t0 + 2))
        tanker(cr, min(x, 300 - (3 - k) * 10) if blocked else x, 570, 0.9, 13810 + k * 5)
    if blocked:
        u = ease_out(seg(t, tl.at("f4", "choked"), tl.at("f4", "choked") + 0.3))
        line(cr, [(380, 500), (380 + 90 * u, 500 + 140 * u)], 18, RED, 13830, amp=0.2)
        line(cr, [(470, 500), (470 - 90 * u, 500 + 140 * u)], 18, RED, 13831, amp=0.2)
        cue("hit", t, tl.at("f4", "choked"))
    slam(cr, t, tl.at("f4", "Strait"), [("Strait of Hormuz", INK)], 300, 58)
    slam(cr, t, tl.at("f4", "war"), [("WAR", RED), (" with Iran", INK)], 820, 52, end=tl.at("f4", "Strait"))


def s_world(cr, t, t0, t1):
    sunburst(cr, t, hexc("#cfe6f2"), hexc("#e2f0f8"))
    cr.save()
    cr.translate(360, 640)
    cr.scale(1.25, 1.25)
    cr.translate(-360, -660)
    globe(cr, "world", 360, 900, t, eyes="sad", mouth="sad")
    cr.restore()
    for k, (x, y) in enumerate([(110, 330), (610, 360), (90, 690), (630, 700)]):
        sc = pop(t, t0 + 0.15 * k, 0.25)
        if sc > 0:
            with at(cr, x, y, sc * 0.9, rot=0.1 * (1 if k % 2 else -1)):
                shape(cr, rrect_pts(-80, -40, 160, 80, 10, 12), WHITE, seed=13900 + k, amp=0.3, lw=4)
                write(cr, [("EMPTY", RED)], 0, 14, 34, align="center", bold=True)
    slam(cr, t, t0 + 0.1, [("SCARCE", RED)], 260, 80)


def s_g7(cr, t, t0, t1):
    tl = _tl()
    sunburst(cr, t, hexc("#2b2d3a"), hexc("#363a4a"))
    slam(cr, t, t0 + 0.05, [("G7", YELLOW)], 520, 220, halo=None)
    for k in range(7):
        a = math.pi + k * math.pi / 6
        sc = pop(t, t0 + 0.2 + 0.06 * k, 0.2)
        if sc > 0:
            with at(cr, 360 + 260 * math.cos(a), 640 + 160 * math.sin(a) + 120, sc):
                blob(cr, 0, 0, 30, 30, hexc("#f0c29c"), 13950 + k, amp=0.3, lw=4)
                line(cr, [(0, -30), (0, -80)], 8, hexc("#f0c29c"), 13960 + k, amp=0.2)
    date_stamp(cr, t, tl.at("f6", "October"), "2 OCT 2026", x=360, y=300)


def s_barrels(cr, t, t0, t1):
    tl = _tl()
    cr.set_source_rgba(*hexc("#dff1fb"))
    cr.paint()
    u = seg(t, t0, tl.at("f7", "stockpiles"))
    n = int(24 * ease_out(u))
    for k in range(n):
        row, col = divmod(k, 6)
        fall = 1 - ease_out(seg(t, t0 + k * 0.04, t0 + k * 0.04 + 0.25))
        barrel(cr, 110 + col * 100, 800 - row * 95 - 400 * fall, 1.0, seed=14000 + k)
    v = int(100_000_000 * ease_out(seg(t, t0, t0 + 1.2)))
    write(cr, [(f"{v:,}", RED)], 360, 330, 72, align="center", bold=True, halo=WHITE)
    write(cr, [("barrels", INK)], 360, 395, 44, align="center", bold=True)
    if t >= tl.at("f7", "emergency"):
        slam(cr, t, tl.at("f7", "emergency"), [("EMERGENCY STOCKPILES", NAVY)], 250, 46)


def s_months(cr, t, t0, t1):
    sunburst(cr, t, hexc("#d6f0d0"), hexc("#e6f7e1"))
    for k in range(4):
        sc = pop(t, t0 + 0.12 * k, 0.22)
        if sc > 0:
            with at(cr, 150 + k * 140, 560, sc, rot=0.05 * (k - 1.5)):
                calendar(cr, 0, 0, "MONTH", str(k + 1), 0.8)
    slam(cr, t, t0 + 0.05, [("4 MONTHS", GREEN)], 330, 84)


def s_first(cr, t, t0, t1):
    tl = _tl()
    cr.set_source_rgba(*hexc("#fff1d6"))
    cr.paint()
    off = ((t - t0) * 600) % 720
    for k in range(4):
        barrel(cr, (k * 180 + off) % 900 - 100, 640, 1.4, col=hexc("#e0a03a"), label="DIESEL", seed=14100 + k)
    line(cr, [(0, 700), (720, 700)], 8, INK, 14110, amp=0.3)
    slam(cr, t, t0 + 0.05, [("DIESEL ", ORANGE), ("FIRST", INK)], 270, 80)
    if t >= tl.at("f8", "twenty"):
        with at(cr, 360, 460, pop(t, tl.at("f8", "twenty"), 0.2)):
            calendar(cr, 0, 0, "WITHIN", "20", 0.85)
            write(cr, [("days", INK)], 0, 108, 30, align="center", bold=True)


def s_question(cr, t, t0, t1):
    sunburst(cr, t, hexc("#e9ddff"), hexc("#f2eaff"))
    wallet(cr, 360, 620, 2.0 + 0.05 * math.sin(t * 8))
    slam(cr, t, t0 + 0.05, [("?", hexc("#8a63d2"))], 420, 220, halo=None)


def s_experts(cr, t, t0, t1):
    from motion.characters import person
    sunburst(cr, t, hexc("#d6f0d0"), hexc("#e6f7e1"))
    for k, (who, x) in enumerate((("teacher", 220), ("oldman", 500))):
        if t >= t0 + 0.15 * k:
            person(cr, who, x, 820, t, scale=1.6, facing=1 if k == 0 else -1, arms=("point", "hip"), eyes="dot",
                   mouth="o" if int(t * 10 + k) % 2 else "smile")
    slam(cr, t, t0 + 0.05, [("2 energy experts", INK)], 290, 64)


def s_drop(cr, t, t0, t1):
    tl = _tl()
    cr.set_source_rgba(*DARK)
    cr.paint()
    k0 = tl.at("f10", "drop")
    v = 6.52 - 0.25 * ease_out(seg(t, k0, k0 + 0.9))
    big_price(cr, 360, 520, 1.15, f"${v:.2f}", col=GREEN if t >= k0 else RED)
    if t >= k0:
        slam(cr, t, k0, [("-25¢", GREEN)], 790, 110, halo=None)
    if t >= tl.at("f10", "weeks"):
        write(cr, [("in a few weeks", WHITE)], 360, 300, 48, align="center", bold=True)
    source_tag(cr, t, t0 + 0.3, "experts in TIME and AP")


def s_catch(cr, t, t0, t1):
    tl = _tl()
    cr.set_source_rgba(*hexc("#7fb3e8"))
    cr.paint()
    for k in range(4):   # water waves
        line(cr, [(0, 780 + k * 40 + 6 * math.sin(t * 3 + k)), (720, 780 + k * 40 - 6 * math.sin(t * 3 + k))], 4,
             hexc("#ffffff", 0.5), 14200 + k, amp=0.6)
    hook(cr, 400, 460, 1.4, t)
    slam(cr, t, tl.at("f11", "catch"), [("THE CATCH", RED)], 300, 96)


def s_refill(cr, t, t0, t1):
    tl = _tl()
    sunburst(cr, t, hexc("#ffe0cc"), hexc("#ffeadd"))
    level = 1 - seg(t, t0, tl.at("f12", "stockpiles") + 0.6)
    tank(cr, 360, 600, level, 2.0)
    slam(cr, t, t0 + 0.05, [("STOPGAP", ORANGE)], 290, 90)


def s_later(cr, t, t0, t1):
    cr.set_source_rgba(*DARK)
    cr.paint()
    tank(cr, 360, 600, 0.0, 2.0)
    stamp(cr, t, t0 + 0.05, "REFILL LATER", dur=t1 - t0, y=330)


def s_chart(cr, t, t0, t1):
    tl = _tl()
    cr.set_source_rgba(*WHITE)
    cr.paint()
    chart(cr, 360, 560, 1.1, seg(t, t0, t1 - 0.2))
    slam(cr, t, t0 + 0.05, [("cheaper ", GREEN), ("soon", INK)], 300, 70, end=tl.at("f13", "maybe"))
    slam(cr, t, tl.at("f13", "maybe"), [("not for ", INK), ("long?", RED)], 300, 70)


def s_end(cr, t, t0, t1):
    tl = _tl()
    sunburst(cr, t, YELLOW, hexc("#ffe27a"))
    shelf(cr, 360, 520, 1.1)
    slam(cr, t, t0 + 0.05, [("higher ", INK), ("PRICES?", RED)], 290, 80)
    buttons(cr, t, tl.at("f14", "comments"), (("YES", GREEN), ("NO", RED)), y=800, s=0.9)


SHOTS = [
    ("f1", None, s_cart), ("f1", "diesel", s_truck), ("f2", None, s_pump), ("f3", None, s_price), ("f3", "September", s_date),
    ("f4", None, s_why), ("f4", "war", s_strait), ("f5", None, s_world), ("f6", None, s_g7),
    ("f7", None, s_barrels), ("f7", "four", s_months), ("f8", None, s_first), ("f9", None, s_question),
    ("f10", None, s_experts), ("f10", "drop", s_drop), ("f11", None, s_catch), ("f12", None, s_refill), ("f12", "refilled", s_later), ("f13", None, s_chart),
    ("f14", None, s_end),
]


def draw(cr, t, tl):
    _TL[0] = tl
    run(cr, t, tl, SHOTS)
    captions(cr, t, tl)
