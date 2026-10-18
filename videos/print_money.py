"""Big question 2: "Why Don't They Just Print More Money?" -- a girl finds a 100-trillion-dollar note in her grandpa's
drawer, in the polished look.

Script: out/scripts_big_questions_batch1.md, row 68 (owner approved 18 Oct 2026). Zimbabwe issued a Z$100 trillion
note in January 2009; at the peak of its hyperinflation (November 2008) prices doubled roughly every 24.7 hours
(Steve Hanke, Cato Institute). In 2020 many central banks created money to get through the pandemic; whether that
saved jobs or drove the 2021-23 price rises is still argued, so both sides are given. The note on screen is a generic
drawing, not a copy of the real banknote. Turbo stock female narrator with tags; the girl and grandpa through Turbo.
"""
import math
import random

from motion import thriller as th
from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import BLUE, GOLD, GREEN, PURPLE, RED, buttons, card, sparkles, studio, tag
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, lin, paint,
                           rad, rrect, shade, sign, soft_disc, stamp, stroke_line, vignette)
from motion.toons import person, portrait

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "m3"          # music drops out under this line (research 18 Oct 2026, A5)
SERIES = "Big Questions"
END_TAG = "Subscribe · a new question tomorrow"      # alternate videos test the silent subscribe wording (research E4/E5)
voice.SPEAKERS.update({"girl": dict(voice="af_sky", speed=1.05, turbo_ref="af_sky+3"),
                       "grandpa": dict(voice="bm_george", speed=0.95, pitch=-1.5, turbo_ref="bm_george-1.5")})
GIRL = dict(shirt=hexc("#ff8ab0"), tie=None, pants=hexc("#3b5b9a"))

SCRIPT = [
    dict(id="m1", scene="drawer", text="A girl finds an old banknote in her grandpa's drawer. It says, one hundred "
                                       "trillion dollars."),
    dict(id="m2", scene="rich", text="Grandpa! We're rich!", speaker="girl"),
    dict(id="m3", scene="rich", text="That note couldn't buy a bus ticket. [chuckle]", speaker="grandpa", gap=0.3),
    dict(id="m4", scene="map", text="It's real money. Zimbabwe printed it in [two thousand nine.|2009.]"),
    dict(id="m5", scene="press", text="But why not just print more money, so everyone's rich?", speaker="girl"),
    dict(id="m6", scene="bread", text="Here's the catch. Printing money doesn't make more bread."),
    dict(id="m7", scene="price", text="Same bread, but everyone has twice the money? The baker just doubles the "
                                      "price."),
    dict(id="m8", scene="spin", text="Zimbabwe printed so much that prices doubled about every day."),
    dict(id="m9", scene="sack", text="People carried bags of cash, to buy one loaf.", speaker="grandpa"),
    dict(id="m10", scene="covid", text="But in [twenty twenty,|2020,] many countries printed money to get through "
                                       "the pandemic. Some say it saved jobs. Others say it caused the price rises "
                                       "after."),
    dict(id="m11", scene="end", text="So should a country print money in a crisis? Yes, or no?", gap=0.3),
]

METADATA = dict(
    title="This Note Says 100 TRILLION. It Couldn't Buy Bread 💵",
    alt_titles=["Why Don't Countries Just Print More Money? 💵", "A 100 Trillion Dollar Note. Worth Nothing. Why?"],
    description="""A girl finds an old banknote in her grandpa's drawer: one hundred trillion dollars. "Grandpa, we're rich!" 💵

It's real money: Zimbabwe printed it in 2009. So why not just print more money so everyone's rich? Because printing money doesn't make more bread. Same bread, twice the money, and the baker just doubles the price. At the worst point, Zimbabwe's prices doubled about every day.

But in 2020 many countries printed money to get through the pandemic. Some say it saved jobs; others say it caused the price rises after.

Sources: Zimbabwe's Z$100 trillion note (January 2009); hyperinflation peak in November 2008, prices doubling roughly every 24.7 hours (Steve Hanke, Cato Institute).

💬 Should a country print money in a crisis? Yes or no, and why? 👇

🔔 Interestingly Strange: how money works, clever twists and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#Money", "#Economics", "#Shorts"],
    tags=["why not print more money", "zimbabwe 100 trillion", "hyperinflation", "inflation explained", "money",
          "economics", "how money works", "zimbabwe dollar", "finance facts", "interestingly strange"],
    pinned_comment="Should a country print money in a crisis? YES 🖨️ or NO 🚫? Give your reason 👇",
)


def note(cr, x, y, s=1.0, rot=0.0, big=True, zeros=14):
    """A generic old banknote: '100 TRILLION DOLLARS' (not a copy of any real design)."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    soft_disc(cr, 8, 14, 170, (0, 0, 0, 0.25))
    rrect(cr, -190, -90, 380, 180, 10)
    paint(cr, lin(0, -90, 0, 90, [(0, hexc("#d8f0c8")), (1, hexc("#a8d898"))]), OUTLINE, 5)
    rrect(cr, -176, -76, 352, 152, 6)
    paint(cr, None, alpha(hexc("#2f6a2a"), 0.6), 3)
    cr.arc(-110, 0, 46, 0, 2 * math.pi)
    paint(cr, alpha(hexc("#2f6a2a"), 0.2), alpha(hexc("#2f6a2a"), 0.7), 3)
    digits = "100," + ",".join(["000"] * max(0, min(4, (zeros - 2) // 3)))
    bold_text(cr, digits, 50, -26, 30 if len(digits) > 12 else 38, hexc("#1f4a1a"), outline=None, shadow=0)
    if big:
        bold_text(cr, "TRILLION", 50, 22, 40, hexc("#1f4a1a"), outline=None, shadow=0)
        bold_text(cr, "DOLLARS", 50, 60, 26, hexc("#2f6a2a"), outline=None, shadow=0)
    cr.restore()


def loaf(cr, x, y, s=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    ellipse(cr, 0, 0, 80, 40)
    paint(cr, rad(-20, -14, 90, [(0, hexc("#f0b860")), (1, hexc("#b8702e"))]), OUTLINE, 5)
    for k in range(3):
        stroke_line(cr, [(-40 + k * 32, -24), (-24 + k * 32, 16)], 4, alpha(OUTLINE, 0.5), curve=False)
    cr.restore()


def cash_pile(cr, x, y, n, seed=1, s=0.35):
    rng = random.Random(seed)
    for k in range(n):
        note(cr, x + rng.uniform(-80, 80), y - k * 8, s, rng.uniform(-0.3, 0.3), big=False, zeros=5)


def price_tag(cr, x, y, text, s=1.0, col=RED, rot=-0.1):
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.move_to(-120, -55)
    cr.line_to(90, -55)
    cr.line_to(130, 0)
    cr.line_to(90, 55)
    cr.line_to(-120, 55)
    cr.close_path()
    paint(cr, WHITE, OUTLINE, 6)
    cr.arc(95, 0, 10, 0, 2 * math.pi)
    paint(cr, OUTLINE, None)
    bold_text(cr, text, -20, 18, 54, col, outline=None, shadow=0)
    cr.restore()


def home(cr, t):
    cr.rectangle(0, 0, W, H)
    cr.set_source(lin(0, 0, 0, H, [(0, hexc("#f4e2c4")), (0.66, hexc("#e8cfa4")), (0.66, hexc("#b5824e")),
                                   (1, hexc("#8a5a30"))]))
    cr.fill()
    rrect(cr, 430, 150, 220, 260, 12)                              # window
    paint(cr, lin(0, 150, 0, 410, [(0, hexc("#9fd6ff")), (1, hexc("#e8f6ff"))]), OUTLINE, 6)
    rrect(cr, 60, 560, 300, 290, 10)                               # the old dresser
    paint(cr, hexc("#8a5a30"), OUTLINE, 6)
    for k in range(3):
        rrect(cr, 80, 580 + k * 90, 260, 70, 6)
        paint(cr, hexc("#a8713e"), OUTLINE, 4)
        cr.arc(210, 615 + k * 90, 8, 0, 2 * math.pi)
        paint(cr, GOLD, OUTLINE, 3)


def girl(cr, t, tl, x, y, s, **kw):
    kw.setdefault("mouth", "talk" if tl is not None and tl.speaking("girl", t) else "smile")
    person(cr, t, x, y, s, "student1", **dict(GIRL, **kw))


def grandpa(cr, t, tl, x, y, s, **kw):
    kw.setdefault("mouth", "talk" if tl is not None and tl.speaking("grandpa", t) else "smile")
    person(cr, t, x, y, s, "grandpa", **kw)


# ---------------------------------------------------------------- scenes
def scene_drawer(cr, t, tl):
    A = tl.at
    home(cr, t)
    girl(cr, t, None, 470, 1000, 0.9, eyes="wide", mouth="o", arms=("hold", "hold"), look=(-0.2, -0.3))
    z = int(lerp(2, 14, seg(t, A("m1", "says,"), A("m1", "dollars.", end=True))))
    cr.save()
    enter(cr, camera(t, [(0, (1.0, 360, 640)), (A("m1", "says,"), (1.12, 360, 560))], dur=0.6))
    note(cr, 360, 540, 1.0 + 0.04 * math.sin(t * 3), -0.05, big=t >= A("m1", "trillion"), zeros=z)
    cr.restore()
    vignette(cr, 0.35)


def scene_rich(cr, t, tl):
    A = tl.at
    home(cr, t)
    jump = t < A("m3")
    hop = 40 * abs(math.sin(t * 7)) if jump else 0
    girl(cr, t, tl, 470, 1000 - hop, 0.9, eyes="happy" if jump else "wide", arms=("up", "up") if jump else
         ("hold", "down"), hold=lambda c, hx, hy: note(c, hx, hy, 0.25, 0.2))
    grandpa(cr, t, tl, 200, 1000, 0.95, eyes="happy", arms=("hips", "hips") if jump else ("down", "point"))
    if jump:
        sparkles(cr, t, A("m2"), 470, 520, n=10, seed=3, col=GOLD, spread=200)
        sign(cr, t, A("m2", "rich!"), 360, 200, "WE'RE RICH!", col=GREEN, size=72)
    else:
        sign(cr, t, A("m3", "bus"), 360, 200, "NOT EVEN A BUS TICKET", col=RED, size=48)
    vignette(cr, 0.35)


def scene_map(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f3a4a"), hexc("#3f5a6e"), seed=4)
    note(cr, 360, 620, 1.2, 0.04)
    if t >= A("m4", "Zimbabwe"):
        sign(cr, t, A("m4", "Zimbabwe"), 360, 380, "ZIMBABWE", col=GOLD, size=70)
    if t >= A("m4", "2009."):
        tag(cr, t, A("m4", "2009."), 360, 820, "2009", col=RED, size=60)
    sign(cr, t, A("m4", "real"), 360, 190, "REAL MONEY", col=GREEN, size=64)
    vignette(cr, 0.4)


def scene_press(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffe7a8"), hexc("#fff6e8"), seed=5)
    rrect(cr, 380, 520, 280, 300, 20)                              # a printing press
    paint(cr, lin(0, 520, 0, 820, [(0, hexc("#7a8aa8")), (1, hexc("#4a5a78"))]), OUTLINE, 6)
    for k in range(2):
        cr.arc(450 + k * 140, 600, 40, 0, 2 * math.pi)
        paint(cr, hexc("#3a4a68"), OUTLINE, 5)
        a = t * 8
        stroke_line(cr, [(450 + k * 140, 600), (450 + k * 140 + 34 * math.cos(a), 600 + 34 * math.sin(a))], 6, GOLD,
                    curve=False)
    for k in range(6):                                             # notes flying out
        ph = (t * 1.2 + k / 6) % 1
        note(cr, 380 - 260 * ph, 700 - 300 * ph + 200 * ph * ph, 0.28, ph * 4, big=False, zeros=5)
    girl(cr, t, tl, 170, 1000, 0.85, eyes="open", arms=("point", "down"), brows="raise")
    sign(cr, t, A("m5", "print"), 360, 190, "JUST PRINT MORE?", col=PURPLE, size=60)
    vignette(cr, 0.3)


def scene_bread(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#f4e6c8"), hexc("#fff6e8"), seed=6)
    loaf(cr, 200, 640, 1.4)
    n = int(3 + 20 * seg(t, A("m6"), A("m6", end=True)))
    cash_pile(cr, 520, 760, n, seed=2)
    bold_text(cr, "1 LOAF", 200, 780, 44, hexc("#a8713e"))
    sign(cr, t, A("m6", "catch."), 360, 190, "THE CATCH", col=RED, size=66, end=A("m6", "Printing") - 0.05)
    sign(cr, t, A("m6", "Printing"), 360, 190, "MORE MONEY, SAME BREAD", col=GOLD, size=48)
    vignette(cr, 0.3)


def scene_price(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd8a0"), hexc("#fff1d6"), seed=7)
    loaf(cr, 360, 520, 1.6)
    doubled = t >= A("m7", "doubles")
    price_tag(cr, 360, 760, "$20" if doubled else "$10", 1.3, RED if doubled else GREEN)
    if t >= A("m7", "twice"):
        card(cr, t, A("m7", "twice"), 360, 300, 560, 120, "EVERYONE: 2X MONEY", [], col=BLUE, title_size=42,
             end=A("m7", "baker") - 0.05)
    if doubled:
        stamp(cr, t, A("m7", "doubles"), 360, 300, "PRICE: 2X", col=RED, size=70)
        cue("kaching", t, A("m7", "doubles"))
    vignette(cr, 0.3)


def scene_spin(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#2a1420"), hexc("#5a2a3a"), seed=8)
    loaf(cr, 360, 520, 1.3)
    u = seg(t, A("m8", "printed"), A("m8", end=True))
    val = int(10 * 2 ** (u * 20))
    price_tag(cr, 360, 760, f"${val:,}" if val < 10 ** 6 else f"${val // 10 ** 6:,}M", 1.25, RED)
    if t >= A("m8", "doubled"):
        tag(cr, t, A("m8", "doubled"), 360, 300, "PRICES DOUBLED", col=RED, size=50)
        tag(cr, t, A("m8", "every"), 360, 380, "ABOUT EVERY DAY", col=GOLD, size=44)
    vignette(cr, 0.45)


def scene_sack(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#c8b898"), hexc("#f2e6c8"), seed=9)
    x = lerp(150, 430, seg(t, A("m9"), A("m9", end=True)))
    person(cr, t, x, 1000, 0.85, "villager", eyes="half", mouth="flat", arms=("hold", "down"), walk=t * 8, sweat=True)
    ellipse(cr, x + 70, 720, 90, 110)                              # the sack of cash
    paint(cr, hexc("#c8a878"), OUTLINE, 5)
    cash_pile(cr, x + 70, 640, 5, seed=4, s=0.22)
    loaf(cr, 560, 900, 0.6)
    tag(cr, t, A("m9", "bags"), 360, 230, "A BAG OF CASH", col=GOLD, size=48)
    tag(cr, t, A("m9", "loaf."), 360, 310, "= 1 LOAF", col=RED, size=48)
    portrait(cr, t, A("m9"), 600, 470, 66, "grandpa", mouth="talk" if tl.speaking("grandpa", t) else "smile",
             eyes="half", bg=hexc("#ffd84d"))
    vignette(cr, 0.35)


def scene_covid(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#1f2f4a"), hexc("#4a5a7e"), seed=10)
    tag(cr, t, A("m10"), 360, 190, "2020", col=BLUE, size=70)
    if t < A("m10", "Some"):
        for k in range(5):                                          # printers running around the world
            ph = (t * 1.1 + k / 5) % 1
            note(cr, 120 + k * 120, 380 + 320 * ph, 0.25, ph * 3, big=False, zeros=5)
    card(cr, t, A("m10", "saved"), 190, 560, 300, 200, "SIDE A", ["SAVED", "JOBS"], col=GREEN, title_size=34,
         line_size=44)
    card(cr, t, A("m10", "caused"), 530, 560, 300, 200, "SIDE B", ["PRICES", "WENT UP"], col=RED, title_size=34,
         line_size=44)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=11)
    note(cr, 360, 700, 0.9, -0.06)
    sign(cr, t, A("m11", "crisis?"), 360, 200, "PRINT IN A CRISIS?", col=GOLD, size=56)
    buttons(cr, t, A("m11", "Yes,"), [("YES", GREEN), ("NO", RED)], y=390, size=56)
    vignette(cr, 0.3)


SCENES = {"drawer": scene_drawer, "rich": scene_rich, "map": scene_map, "press": scene_press, "bread": scene_bread,
          "price": scene_price, "spin": scene_spin, "sack": scene_sack, "covid": scene_covid, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("100 TRILLION", False), ("DOLLARS?", True)], end=tl.at("m2"), y=170, size=104)
    captions(cr, t, tl)
