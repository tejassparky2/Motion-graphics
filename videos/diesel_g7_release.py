"""News: diesel hit a record; the G7 will release up to 100 million barrels of emergency oil and diesel (2 Oct 2026).

Host-and-Globe format (motion/newsdesk.py); Globe in world colours. Script approved by the owner on 5 Oct 2026.

Facts, as of 5 October 2026:
- AAA national average diesel record $6.52 a gallon on 22 Sep 2026; $6.37 on 2 Oct. AP via BNN Bloomberg
  https://www.bnnbloomberg.ca/markets/oil/2026/10/02/g7-nations-will-release-100-million-barrels-of-oil-and-diesel-fuel-after-prices-soar/ ;
  TIME (on-highway diesel high $6.529) https://time.com/article/2026/10/03/the-g7-is-releasing-emergency-fuel-reserves-how-much-will-it-help-americans-/
- Cause: the war involving Iran disrupted shipping through the Strait of Hormuz; diesel supply fell worldwide
  (Middle East exports halted, Russia and China stopped exporting diesel). Al Jazeera
  https://www.aljazeera.com/news/2026/10/3/g7-to-release-100-million-barrels-of-oil-and-diesel-will-it-curb-prices ; TIME (above)
- 2 Oct 2026: G7 and partners to release up to 100 million barrels over four months via the IEA, with a "frontloaded
  substantial diesel release within the first 20 days". AP/BNN, Al Jazeera, ABC News
  https://www.abc.net.au/news/2026-10-03/g7-to-release-100m-barrels-oil-in-bid-to-curb-soaring-prices/107224282
- Price effect: Jason Bordoff (Columbia) up to 25 cents a gallon within weeks (TIME); Michael Lynch (Energy Policy
  Research Foundation) 25-50 cents after several weeks (AP).
- Stopgap; reserves must be refilled later: Capital Economics via Al Jazeera; ABC News.
"""
import math

from motion.engine import INK, RED, at, ease_out, hexc, pop, seg, write
from motion.kit import hl, stamp
from motion.news import GREEN, date_stamp, panel, source_tag
from motion.newsdesk import (G, H, background, cam_keys, dialogue, end_scene, host, make_draw, mood,
                             talking_globe)
from motion.newsprops import barrel, calendar, price_sign, strait, tank, truck

NARRATOR = dict(speed=0.95)
TAIL = 0.9
CODE = "world"

SCRIPT = dialogue([
    ("d1", "talk", "H", "Almost everything you buy rode on a diesel truck. And diesel just hit a record."),
    ("d2", "talk", "G", "[Six dollars and fifty-two cents a gallon.|$6.52 a gallon.] "
                        "That was the record, on September twenty-second."),
    ("d3", "talk", "H", "Why so high?"),
    ("d4", "talk", "G", "The war with Iran choked oil shipping through the Strait of Hormuz. "
                        "And diesel got scarce around the world."),
    ("d5", "talk", "H", "So what's the plan?"),
    ("d6", "talk", "G", "On October second, the G7 agreed to release up to a hundred million barrels "
                        "from emergency stockpiles. Over four months."),
    ("d7", "talk", "G", "And most of the diesel comes first. Within twenty days."),
    ("d8", "talk", "H", "Will I actually pay less?"),
    ("d9", "talk", "G", "Two energy experts estimate diesel could drop around twenty-five cents a gallon. "
                        "In a few weeks."),
    ("d10", "talk", "G", "But it's a stopgap. The stockpiles will have to be refilled later."),
    ("d11", "talk", "H", "So cheaper soon. But not for long?"),
    ("d12", "talk", "G", "Exactly. There is a catch."),
    ("d13", "end", "H", "Have you noticed higher prices at the store? Tell me in the comments."),
])

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


def scene_talk(cr, t, tl):
    A = tl.at
    background(cr, t, cam_keys(tl))
    host(cr, t, tl, **mood(t, tl, [("d3", dict(eyes="dot", mouth="flat", arms=("chin", "hip"))),
                                    ("d4", {}), ("d8", dict(eyes="happy", mouth="smile", arms=("cheer", "hip"))),
                                    ("d9", {}), ("d11", dict(eyes="sly", mouth="flat", arms=("chin", "hip")))], {}))
    eyes, idle = mood(t, tl, [("d4", ("dot", "flat")), ("d6", ("happy", "smile")), ("d10", ("sly", "flat"))],
                      ("wide", "smile"))
    talking_globe(cr, t, tl, CODE, eyes, idle)

    cr.identity_matrix()
    hl(cr, t, [("DIESEL ", RED), ("prices", INK)], 215, 56, 0.0, bold=True, sound=False)
    date_stamp(cr, t, A("d6", "October"), "2 OCT 2026", x=585, y=118)

    panel(cr, t, 0.15, A("d1", "record"), 360, 400, 420, 220, lambda c: truck(c, 0, 0, 1.1), seed=9700)
    panel(cr, t, A("d1", "record"), A("d3"), 360, 400, 320, 200,
          lambda c: price_sign(c, 0, 0, "$6.52", "DIESEL RECORD"), seed=9710)
    source_tag(cr, t, A("d2", "record"), "AAA via AP, 22 Sep 2026", end=A("d3"))
    panel(cr, t, A("d4", "war"), A("d5"), 360, 400, 540, 230, lambda c: strait(c, 0, 0, t, 1.0), seed=9720)

    def stockpile(c):
        u = seg(t, A("d6", "G7"), A("d6", "hundred") + 0.6)
        for k in range(int(10 * ease_out(u))):
            barrel(c, -200 + (k % 5) * 100, -30 + (k // 5) * 90 - 40, 0.8, seed=9730 + k)
        write(c, [("100 MILLION barrels", INK)], 0, 120, 36, align="center", bold=True)
    panel(cr, t, A("d6", "G7"), A("d7"), 360, 400, 560, 300, stockpile, seed=9740)

    def first(c):
        calendar(c, -130, 0, "DIESEL FIRST", "20", 1.0)
        write(c, [("days", INK)], -130, 112, 28, align="center", bold=True)
        barrel(c, 100, 0, 1.2, col=hexc("#e0a03a"), label="DIESEL")
    panel(cr, t, A("d7", "diesel"), A("d8"), 360, 400, 460, 270, first, seed=9750)

    def drop(c):
        price_sign(c, -80, 0, "-25¢?", "DIESEL", col=GREEN)
        write(c, [("in a few weeks", INK)], 150, 10, 30, align="center", bold=True)
    panel(cr, t, A("d9", "drop"), A("d10"), 360, 400, 560, 200, drop, seed=9760)
    source_tag(cr, t, A("d9", "experts"), "TIME; AP (3 and 2 Oct 2026)", end=A("d10"))

    def refill(c):
        tank(c, -90, 0, 1 - seg(t, A("d10"), A("d10") + 1.5), 0.9)
        write(c, [("REFILL", RED)], 110, -10, 40, align="center", bold=True)
        write(c, [("LATER", RED)], 110, 36, 40, align="center", bold=True)
    panel(cr, t, A("d10", "stopgap"), A("d11", end=True) + 0.1, 360, 400, 440, 220, refill, seed=9770)
    if A("d12") <= t < A("d12", end=True) + 0.4:
        stamp(cr, t, A("d12", "catch"), "THE CATCH", dur=A("d12", end=True) + 0.4 - A("d12", "catch"), y=440)


def scene_end(cr, t, tl):
    end_scene(cr, t, tl, CODE, "d13", [("higher ", INK), ("PRICES", RED), ("?", INK)],
              prop=lambda c: truck(c, 0, 0, 0.9))


draw = make_draw({"talk": scene_talk, "end": scene_end})
