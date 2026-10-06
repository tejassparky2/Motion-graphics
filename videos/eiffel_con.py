"""Episode 13: "The Man Who Sold the Eiffel Tower (Twice)" — Victor Lustig, 1925.

Facts (Wikipedia, "Victor Lustig"): in 1925 Lustig read about the Eiffel Tower's costly upkeep, had a forger make fake
government stationery, and invited scrap-metal dealers to a confidential meeting at a hotel, saying the government
would sell the tower for scrap and needed secrecy. André Poisson was his mark; Lustig posed as a corrupt official and
got a bribe on top of roughly 70,000 francs, then fled to Austria. Poisson was too ashamed to report it, so Lustig came
back later that year to try again; this time the police were alerted and he fled to the US. In the early 1930s he
conned Al Capone into giving him money ($5,000, or $1,000 per other sources, so no amount is stated).
"""
import math

from motion.captions import captions
from motion.characters import cash, money_pile, person
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, smooth, write)
from motion.kit import camera, confetti, enter_world, fly, hl, sepia, set_camera, stamp, whip

NARRATOR = dict(speed=1.05)
TAIL = 0.8

SCRIPT = [
    dict(id="l1", scene="paris",
         text="In [nineteen twenty-five,|1925,] a man sold the Eiffel Tower. There was just one problem. He didn't own it."),
    dict(id="l2", scene="paris",
         text="Victor Lustig read in the newspaper that the tower cost a fortune to repair. So he made fake government "
              "letters,"),
    dict(id="l3", scene="hotel",
         text="invited scrap metal dealers to a secret meeting at a fancy hotel, and told them: the government is "
              "selling the tower for scrap. Keep it quiet."),
    dict(id="l4", scene="hotel",
         text="One dealer, André Poisson, wanted it badly. Lustig even pretended to be corrupt, and asked for a bribe. "
              "Poisson paid it, on top of about [seventy thousand francs.|70,000 francs.]"),
    dict(id="l5", scene="map", text="Lustig grabbed the money, and fled to Austria."),
    dict(id="l6", scene="wait",
         text="Then he waited for the police. Nothing. Poisson was too embarrassed to tell anyone he'd been fooled."),
    dict(id="l7", scene="again", text="So Lustig came back, and tried to sell the Eiffel Tower again.", gap=0.22),
    dict(id="l8", scene="again", text="This time, the police found out, and he escaped to America."),
    dict(id="l9", scene="capone", text="Where he later tricked Al Capone into handing him cash."),
    dict(id="l10", scene="end", text="Would you have bought it?", pace=0.95, gap=0.25),
]

METADATA = dict(
    title="The Man Who Sold the Eiffel Tower… TWICE 🗼😳",
    alt_titles=["He Sold the Eiffel Tower and Got Away With It 🗼", "The Greatest Con Man in History 😳🗼"],
    description="""In 1925, a con man named Victor Lustig sold the Eiffel Tower. There was just one problem: he didn't own it. 🗼

He forged government letters, told scrap-metal dealers the tower was being sold for scrap, and took the money (plus a bribe!). His victim was too embarrassed to go to the police… so Lustig came back and tried to sell it AGAIN. 😳 He later even tricked Al Capone.

💬 Would you have bought it? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#History", "#WeirdHistory", "#TrueStory"],
    tags=["victor lustig", "eiffel tower", "sold the eiffel tower", "con man", "history facts", "weird history",
          "true story", "scam history", "history shorts", "interestingly strange"],
    pinned_comment="Imagine being the guy who bought the Eiffel Tower 😂 Would you have fallen for it? 👇",
)

GOLD = hexc("#f2b632")
NAVY = hexc("#23346b")
GREEN = hexc("#3d8f45")
IRON = hexc("#6b4a2e")
PARIS = hexc("#f3d9a4")
CON, MARK = "lustig", "owner"


def eiffel(cr, x, y, s=1.0, sign=None, t=0.0, seed=0):
    """The tower, ground at (x, y), ~620 tall at s=1."""
    with at(cr, x, y, s):
        sharp_shape(cr, [(-150, 0), (-70, -250), (-40, -420), (-8, -600), (8, -600), (40, -420), (70, -250), (150, 0),
                         (95, 0), (0, -140), (-95, 0)], IRON, seed=seed, amp=0.8, lw=4.5)
        for k in range(1, 9):   # lattice
            y0 = -k * 65
            w = 150 - k * 17
            line(cr, [(-w + 20, y0), (w - 20, y0 - 30)], 2.5, hexc("#3a2a1e"), seed=seed + k, amp=0.3)
            line(cr, [(w - 20, y0), (-w + 20, y0 - 30)], 2.5, hexc("#3a2a1e"), seed=seed + 20 + k, amp=0.3)
        for yy, ww in ((-250, 90), (-420, 50)):   # platforms
            shape(cr, rrect_pts(-ww, yy - 8, 2 * ww, 16, 3, 12), hexc("#8e5a2e"), seed=seed + 40 + yy, amp=0.3, lw=3)
        line(cr, [(0, -600), (0, -650)], 4, INK, seed=seed + 50, amp=0.2)
        if sign:
            with at(cr, 0, -330, 1.0, rot=-0.06 + 0.03 * math.sin(t * 3)):
                shape(cr, rrect_pts(-150, -50, 300, 100, 8, 16), WHITE, seed=seed + 60, amp=0.6, lw=4)
                write(cr, [(sign, RED)], 0, 20, 52, align="center", bold=True)


def paris_set(cr, t):
    cr.set_source_rgba(*PARIS)
    cr.paint()
    for k in range(-5, 14):   # rooftops
        h = 140 + (k * 53) % 90
        sharp_shape(cr, [(k * 120, 900), (k * 120, 900 - h), (k * 120 + 60, 860 - h - 40), (k * 120 + 120, 900 - h),
                         (k * 120 + 120, 900)], hexc("#d9c2a0"), seed=10000 + k, amp=0.6, lw=3)
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#b9a58a"), seed=10020, amp=1, lw=4)
    for k in range(-8, 18):   # cobbles
        blob(cr, k * 90, 960 + (k % 2) * 30, 30, 12, hexc("#a8947a"), seed=10030 + k, amp=0.6, lw=2.5)
    line(cr, [(60, 900), (60, 560)], 8, INK, seed=10060, amp=0.3)   # street lamp
    blob(cr, 60, 548, 22, 16, hexc("#ffe28a"), seed=10061, amp=0.4, lw=3)


def newspaper(cr, x, y, s, t, seed=0):
    with at(cr, x, y, s, rot=-0.08):
        shape(cr, rrect_pts(-150, -110, 300, 220, 4, 18), hexc("#f4efe1"), seed=seed, amp=0.6, lw=4)
        write(cr, [("LE JOURNAL", INK)], 0, -66, 36, align="center", bold=True)
        write(cr, [("1925", RED)], 110, -76, 20, align="center")
        write(cr, [("TOWER REPAIRS", RED)], 0, -18, 28, align="center", bold=True)
        write(cr, [("COST A FORTUNE!", RED)], 0, 16, 28, align="center", bold=True)
        for k in range(3):
            line(cr, [(-130, 50 + k * 18), (130, 50 + k * 18)], 2, hexc("#9a958a"), seed=seed + k, amp=0.4)
        eiffel(cr, -100, 100, 0.12, seed=seed + 10)


def letter(cr, x, y, s, seed=0, stamp_on=True):
    with at(cr, x, y, s, rot=0.05):
        shape(cr, rrect_pts(-130, -170, 260, 340, 6, 18), WHITE, seed=seed, amp=0.6, lw=4)
        write(cr, [("RÉPUBLIQUE", NAVY)], 0, -120, 30, align="center", bold=True)
        write(cr, [("FRANÇAISE", NAVY)], 0, -88, 30, align="center", bold=True)
        for k in range(5):
            line(cr, [(-100, -40 + k * 28), (100, -40 + k * 28)], 2.5, hexc("#9a958a"), seed=seed + k, amp=0.5)
        if stamp_on:
            blob(cr, 60, 120, 44, 44, None, seed=seed + 9, amp=0.6, lw=5, stroke=RED)
            write(cr, [("FAKE", RED)], 60, 132, 26, align="center", bold=True)


# ------------------------------------------------------------------ scenes
def scene_paris(cr, t, tl):
    A = tl.at
    keys = [(0, (1.5, 480, 560)), (A("l1", "man"), (0.9, 380, 560)), (A("l1", "sold"), (1.3, 480, 560)), (A("l1", "Eiffel"), (0.7, 420, 560)),
            (A("l1", "problem"), (1.6, 200, 740)), (A("l1", "own"), (2.1, 190, 720)),
            (A("l2", "Victor"), (1.5, 200, 740)), (A("l2", "newspaper"), (1.9, 330, 660)),
            (A("l2", "fortune"), (1.4, 420, 600)), (A("l2", "fake"), (1.9, 330, 660))]
    set_camera(camera(t, keys, dur=0.16))
    enter_world(cr)
    paris_set(cr, t)
    eiffel(cr, 480, 900, 1.0, sign="SOLD!" if t < A("l2") else None, t=t, seed=10100)
    person(cr, CON, 190, 905, t, facing=1, arms=("thumb", "hip") if t < A("l2") else ("hold", "hip"),
           eyes="sly", mouth="smirk" if t < A("l1", "problem") else ("grin" if t >= A("l1", "own") else "smirk"))
    if A("l2", "newspaper") <= t < A("l2", "fake"):
        newspaper(cr, 330, 660, pop(t, A("l2", "newspaper"), 0.2) or 0.01, t, seed=10200)
    if t >= A("l2", "fake"):
        letter(cr, 330, 660, pop(t, A("l2", "fake"), 0.2) or 0.01, seed=10210)
    sepia(cr, 0.35)
    hl(cr, t, [("1925", RED)], 215, 96, A("l1", "1925"), end=A("l1", "sold") - 0.05, bold=True)
    hl(cr, t, [("he ", INK), ("SOLD", RED), (" the Eiffel Tower", INK)], 215, 60, A("l1", "sold"),
       end=A("l1", "problem") - 0.05, bold=True)
    hl(cr, t, [("he didn't ", INK), ("OWN", RED), (" it", INK)], 215, 84, A("l1", "own"), end=A("l2") - 0.05, bold=True)
    hl(cr, t, [("Victor ", INK), ("Lustig", RED)], 215, 84, A("l2", "Victor"), end=A("l2", "fake") - 0.05, bold=True)
    hl(cr, t, [("FAKE", RED), (" government letters", INK)], 215, 58, A("l2", "fake"), bold=True)
    if t >= A("l1", "sold") and t < A("l2"):
        cue("kaching", t, A("l1", "sold"))


def hotel_set(cr, t):
    cr.set_source_rgba(*hexc("#8e2f2c"))
    cr.paint()
    for k in range(-5, 14):   # wallpaper
        line(cr, [(k * 80, 250), (k * 80, 900)], 5, hexc("#7a2826"), seed=10300 + k, amp=0.5)
        for j in range(6):
            dot(cr, k * 80 + 40, 300 + j * 110, 6, hexc("#c9a64a"))
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#5a3e2b"), seed=10320, amp=1, lw=4)
    # chandelier
    line(cr, [(360, 250), (360, 330)], 4, GOLD, seed=10330, amp=0.2)
    shape(cr, [(260, 330), (460, 330), (420, 380), (300, 380)], GOLD, seed=10331, amp=0.6, lw=4)
    for k in range(5):
        blob(cr, 280 + k * 40, 318, 8, 12, hexc("#ffe28a", 0.8 + 0.2 * math.sin(t * 5 + k)), seed=10332 + k, amp=0.3,
             lw=2)
    write(cr, [("GRAND HÔTEL", GOLD)], 360, 460, 44, align="center", bold=True)
    # easel with a scrap pitch
    line(cr, [(640, 900), (680, 560), (720, 900)], 5, IRON, seed=10340, amp=0.3)
    shape(cr, rrect_pts(570, 540, 220, 200, 6, 16), WHITE, seed=10341, amp=0.6, lw=4)
    eiffel(cr, 680, 720, 0.25, seed=10342)
    write(cr, [("SCRAP", RED)], 680, 590, 40, align="center", bold=True)


def scene_hotel(cr, t, tl):
    A = tl.at
    keys = [(A("l3") - 0.2, (1.0, 400, 720)), (A("l3", "scrap"), (1.5, 320, 740)), (A("l3", "secret"), (1.1, 360, 700)),
            (A("l3", "hotel"), (1.4, 360, 520)), (A("l3", "told"), (1.7, 150, 720)), (A("l3", "selling"), (1.6, 660, 660)),
            (A("l3", "quiet"), (2.0, 150, 720)),
            (A("l4", "dealer"), (1.3, 380, 740)), (A("l4", "Poisson"), (2.0, 380, 720)), (A("l4", "badly"), (1.5, 380, 740)),
            (A("l4", "corrupt"), (1.9, 150, 720)), (A("l4", "bribe"), (1.4, 270, 720)), (A("l4", "paid"), (1.8, 330, 740)),
            (A("l4", "70,000"), (1.1, 360, 700))]
    set_camera(camera(t, keys, dur=0.16))
    enter_world(cr)
    hotel_set(cr, t)
    quiet = A("l3", "quiet") <= t < A("l4")
    person(cr, CON, 150, 905, t, facing=1,
           arms=("point", "hip") if A("l3", "selling") <= t < A("l3", "quiet") else
           (("face", "hip") if quiet else (("give", "hip") if A("l4", "bribe") <= t < A("l4", "paid") else ("hip", "hip"))),
           eyes="sly", mouth="smirk" if not quiet else "flat")
    if quiet:
        write(cr, [("shhh!", INK)], 250, 690, 40, bold=True, halo=WHITE)
    dealers = [("oldman", 520), ("farmer", 600), (MARK, 380)]
    for i, (who, x) in enumerate(dealers):
        eager = who == MARK and t >= A("l4", "Poisson")
        person(cr, who, x, 905, t, facing=-1, eyes="happy" if eager and t < A("l4", "paid") else
               ("wide" if A("l3", "selling") <= t < A("l3", "quiet") else "dot"),
               mouth="o" if A("l3", "selling") <= t < A("l3", "quiet") else ("grin" if eager else "smile"),
               arms=("give", "hip") if who == MARK and t >= A("l4", "paid") else ("hip", "hip"),
               jump=abs(math.sin(t * 8)) * 8 if eager and t < A("l4", "corrupt") else 0)
    if t >= A("l4", "paid"):   # the money crosses the room
        fly(cr, t, A("l4", "paid"), 0.5, (360, 760), (200, 760), lambda x, y: cash(cr, x, y, 1.6, seed=10400), height=90)
        if t >= A("l4", "paid") + 0.5:
            money_pile(cr, 190, 900, 0.45, seed=10410)
    if A("l4", "bribe") <= t < A("l4", "paid"):
        with at(cr, 270, 720, pop(t, A("l4", "bribe"), 0.2) or 0.01, rot=0.1):
            shape(cr, rrect_pts(-60, -36, 120, 72, 4, 12), hexc("#f4efe1"), seed=10420, amp=0.5, lw=3.5)
            write(cr, [("bribe", RED)], 0, 12, 32, align="center", bold=True)
    sepia(cr, 0.3)
    hl(cr, t, [("SECRET", RED), (" meeting", INK)], 215, 84, A("l3", "secret"), end=A("l3", "told") - 0.05, bold=True)
    hl(cr, t, [("tower ", INK), ("for SCRAP", RED)], 215, 84, A("l3", "selling"), end=A("l4") - 0.05, bold=True)
    hl(cr, t, [("André ", INK), ("Poisson", NAVY)], 215, 84, A("l4", "Poisson"), end=A("l4", "corrupt") - 0.05, bold=True)
    hl(cr, t, [("+ a ", INK), ("BRIBE", RED)], 215, 90, A("l4", "bribe"), end=A("l4", "70,000") - 0.05, bold=True)
    hl(cr, t, [("~70,000", GREEN), (" francs", INK)], 215, 80, A("l4", "70,000"), bold=True)


def scene_map(cr, t, tl):
    A = tl.at
    z = camera(t, [(A("l5") - 0.2, (1.0, 360, 640)), (A("l5", "money"), (1.4, 260, 640)), (A("l5", "Austria"), (1.3, 480, 560))],
               dur=0.16)
    cr.set_source_rgba(*hexc("#bfe0f0"))
    cr.paint()
    cr.translate(360, 640)
    cr.scale(z[0], z[0])
    cr.translate(-z[1], -z[2])
    blob(cr, 380, 620, 420, 360, hexc("#e9d9a8"), seed=10500, amp=6, lw=4)   # rough Europe blob
    blob(cr, 200, 700, 150, 150, hexc("#c9dca0"), seed=10501, amp=3, lw=3.5)
    blob(cr, 560, 560, 110, 70, hexc("#f2c29c"), seed=10502, amp=3, lw=3.5)
    write(cr, [("FRANCE", INK)], 200, 790, 40, align="center", bold=True)
    write(cr, [("AUSTRIA", INK)], 560, 640, 40, align="center", bold=True)
    dot(cr, 220, 660, 12, RED)
    write(cr, [("Paris", RED)], 220, 640, 30, align="center", bold=True)
    dot(cr, 600, 540, 12, RED)
    u = ease_out(seg(t, A("l5", "fled"), A("l5", "Austria", end=True) + 0.2))
    pts = [(lerp(220, 600, k / 20 * u), lerp(660, 540, k / 20 * u) - math.sin(k / 20 * u * math.pi) * 60) for k in range(21)]
    line(cr, pts, 6, RED, seed=10510, amp=0.3)
    person(cr, CON, pts[-1][0], pts[-1][1] + 20, t, facing=1, scale=0.4, walk=t * 4 if u < 1 else None,
           arms=("hold", "down"), eyes="happy", mouth="grin")
    cash(cr, pts[-1][0] + 20, pts[-1][1] - 30, 0.8, seed=10520)
    sepia(cr, 0.3)
    hl(cr, t, [("grabbed the ", INK), ("money", GREEN)], 215, 80, A("l5", "money"), end=A("l5", "fled") - 0.05, bold=True)
    hl(cr, t, [("fled to ", INK), ("AUSTRIA", RED)], 215, 84, A("l5", "fled"), bold=True)
    cue("whoosh", t, A("l5", "fled"), 0.3)


def scene_wait(cr, t, tl):
    A = tl.at
    keys = [(A("l6") - 0.2, (1.3, 220, 720)), (A("l6", "police"), (1.8, 220, 700)), (A("l6", "nothing"), (1.0, 360, 720)),
            (A("l6", "Poisson"), (1.9, 520, 720)), (A("l6", "embarrassed"), (2.3, 520, 700)), (A("l6", "fooled"), (1.3, 400, 720))]
    set_camera(camera(t, keys, dur=0.16))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#e9d3ae"))
    cr.paint()
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#b98a5a"), seed=10600, amp=1, lw=4)
    line(cr, [(360, 250), (360, 1000)], 8, INK, seed=10601, amp=0.4)   # split screen: Vienna | Paris
    write(cr, [("VIENNA", INK)], 180, 440, 44, align="center", bold=True)
    write(cr, [("PARIS", INK)], 540, 440, 44, align="center", bold=True)
    # Lustig waiting with newspapers
    person(cr, CON, 200, 905, t, facing=1, arms=("hold", "hip"), eyes="wide" if t < A("l6", "nothing") else "happy",
           mouth="flat" if t < A("l6", "nothing") else "grin", sweat=t < A("l6", "nothing"))
    with at(cr, 285, 830, 0.5):
        newspaper(cr, 0, 0, 1.0, t, seed=10610)
    if t >= A("l6", "nothing"):
        write(cr, [("no news!", GREEN)], 200, 560, 44, align="center", bold=True, halo=WHITE)
    # Poisson hiding his red face
    red = seg(t, A("l6", "embarrassed"), A("l6", "embarrassed") + 0.3)
    person(cr, MARK, 540, 905, t, facing=-1, arms=("face", "face") if t >= A("l6", "embarrassed") else ("hip", "hip"),
           eyes="sad", mouth="wobble", tears=t >= A("l6", "fooled"))
    if red > 0:
        blob(cr, 540, 905 - 26 - 108 - 40 + 12, 42, 38, hexc("#e53935", 0.45 * red), seed=10620, amp=0.4, lw=0,
             stroke=None)
    sepia(cr, 0.3)
    hl(cr, t, [("waiting for ", INK), ("police", NAVY), ("...", INK)], 215, 66, A("l6", "police"),
       end=A("l6", "nothing") - 0.05, bold=True)
    hl(cr, t, [("NOTHING", GREEN)], 215, 96, A("l6", "nothing"), end=A("l6", "Poisson") - 0.05, bold=True)
    hl(cr, t, [("too ", INK), ("EMBARRASSED", RED)], 215, 66, A("l6", "embarrassed"), bold=True)


def scene_again(cr, t, tl):
    A = tl.at
    keys = [(A("l7") - 0.2, (0.8, 380, 600)), (A("l7", "came"), (1.6, 190, 740)), (A("l7", "sell"), (0.75, 420, 560)),
            (A("l7", "again"), (1.2, 480, 520)), (A("l8", "police"), (1.1, 360, 720)), (A("l8", "escaped"), (1.5, 560, 800)),
            (A("l8", "America"), (1.1, 520, 740))]
    set_camera(camera(t, keys, dur=0.16))
    enter_world(cr)
    paris_set(cr, t)
    eiffel(cr, 480, 900, 1.0, sign="FOR SALE AGAIN" if t >= A("l7", "sell") else None, t=t, seed=10100)
    police = t >= A("l8", "police")
    run = seg(t, A("l8", "escaped"), A("l8", "America", end=True) + 0.3)
    person(cr, CON, lerp(190, 760, run), 905, t, facing=1, walk=t * 4 if run > 0 else None,
           arms=("wave", "hip") if not police else ("down", "down"), eyes="sly" if not police else "wide",
           mouth="grin" if not police else "o", sweat=police)
    if police:
        on = int(t * 6) % 2
        cr.save()
        cr.identity_matrix()
        cr.set_source_rgba(*(hexc("#e53935", 0.18) if on else hexc("#3f6fb5", 0.18)))
        cr.paint()
        cr.restore()
        write(cr, [("POLICE!", NAVY)], 200, 520, 60, align="center", bold=True, halo=WHITE)
        cue("hit", t, A("l8", "police"))
    if t >= A("l8", "America"):   # the steamship out
        u = seg(t, A("l8", "America"), A("l8", end=True) + 0.4)
        with at(cr, lerp(640, 820, u), 1060, 0.7):
            sharp_shape(cr, [(-160, -40), (160, -40), (120, 30), (-130, 30)], INK, seed=10700, amp=0.6, lw=3)
            sharp_shape(cr, [(-80, -40), (60, -40), (60, -90), (-80, -90)], WHITE, seed=10701, amp=0.4, lw=3)
            shape(cr, rrect_pts(-20, -150, 40, 60, 4, 10), RED, seed=10702, amp=0.4, lw=3)
    sepia(cr, 0.3)
    hl(cr, t, [("he came ", INK), ("BACK", RED)], 215, 90, A("l7", "came"), end=A("l7", "sell") - 0.05, bold=True)
    hl(cr, t, [("sold it ", INK), ("AGAIN", RED), ("?!", INK)], 215, 90, A("l7", "again"), end=A("l8") - 0.05, bold=True)
    hl(cr, t, [("escaped to ", INK), ("America", NAVY)], 215, 72, A("l8", "escaped"), bold=True)


def scene_capone(cr, t, tl):
    A = tl.at
    keys = [(A("l9") - 0.2, (1.2, 360, 740)), (A("l9", "tricked"), (1.8, 200, 720)), (A("l9", "Capone"), (1.9, 520, 700)),
            (A("l9", "cash"), (1.3, 360, 740))]
    set_camera(camera(t, keys, dur=0.16))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#3a2f2a"))
    cr.paint()
    for k in range(-4, 12):   # dark wood office
        line(cr, [(k * 90, 250), (k * 90, 900)], 4, hexc("#2e2521"), seed=10800 + k, amp=0.5)
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#5a3e2b"), seed=10801, amp=1, lw=4)
    shape(cr, rrect_pts(420, 440, 240, 70, 8, 16), GOLD, seed=10802, amp=0.5, lw=4)
    write(cr, [("CHICAGO", INK)], 540, 488, 40, align="center", bold=True)
    person(cr, "gangster", 540, 905, t, facing=-1, arms=("give", "hip") if t >= A("l9", "handing") else ("hip", "hip"),
           eyes="sly", mouth="flat")
    shape(cr, rrect_pts(400, 846, 290, 60, 8, 16), hexc("#6d4524"), seed=10803, amp=0.6, lw=4)
    person(cr, CON, 200, 905, t, facing=1, eyes="happy" if t >= A("l9", "cash") else "sly",
           mouth="grin" if t >= A("l9", "cash") else "smirk", arms=("give", "hip") if t >= A("l9", "cash") else ("hip", "hip"))
    if t >= A("l9", "handing"):
        fly(cr, t, A("l9", "handing"), 0.5, (470, 760), (270, 760), lambda x, y: cash(cr, x, y, 1.6, seed=10810), height=80)
    write(cr, [("AL CAPONE", GOLD)], 540, 640, 36, align="center", bold=True, halo=INK)
    hl(cr, t, [("he even tricked ", INK), ("AL CAPONE", RED)], 215, 52, A("l9", "Capone"), bold=True, underline=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("l10") - 0.2, (0.8, 380, 600)), (A("l10", "bought"), (1.1, 480, 520))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    paris_set(cr, t)
    eiffel(cr, 480, 900, 1.0, sign="FOR SALE?", t=t, seed=10100)
    person(cr, CON, 190, 905, t, facing=1, arms=("thumb", "hip"), eyes="sly", mouth="smirk")
    sepia(cr, 0.3)
    hl(cr, t, [("would YOU ", INK), ("buy it", RED), ("?", INK)], 215, 80, A("l10"), bold=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"paris": scene_paris, "hotel": scene_hotel, "map": scene_map, "wait": scene_wait, "again": scene_again,
     "capone": scene_capone, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
