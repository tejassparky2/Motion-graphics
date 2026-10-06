"""Researchers found / history: Napoleon's answer to "why don't the poor rise up against the rich?"

Built on the owner's reference (Abhay Create's Hindi Short), with Napoleon's real recorded words instead of the
unsourced viral line. Sources:
- Council of State, 4 March 1806, recorded by Baron Joseph Pelet de la Lozère, "Opinions de Napoléon… recueillies par
  un membre de son conseil d'État" (1833): religion attaches "to heaven an idea of equality which keeps the rich from
  being massacred by the poor"; "Society could not exist without an inequality of fortunes, and an inequality of
  fortunes without religion" (also quoted by H. A. Taine, North American Review, May 1891, p. 568).
- "A man dying of starvation alongside of one who is surfeited would not yield to this difference unless he had some
  authority which assured him that God so orders it, that there must be both poor and rich in the world, but that in
  the future, and throughout eternity, the portion of each will be changed" (Napoleon's remarks recorded by his
  councillors; Taine).
- Concordat of 1801: Napoleon's agreement with the Pope that brought the Catholic Church back into French public life.
The video reports Napoleon's view and asks viewers what they think; it doesn't call for anything.
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
    dict(id="n1", scene="hook", text="Napoleon had an answer to a dangerous question. Why don't the poor rise up, and "
                                     "take everything from the rich?"),
    dict(id="n2", scene="crowd", text="Imagine the world has [a hundred|100] people. Five are rich. "
                                      "[Ninety-five|95] are poor."),
    dict(id="n3", scene="crowd", text="The [ninety-five|95] are much stronger. So why do they accept it?"),
    dict(id="n4", scene="council", text="In [eighteen oh six,|1806,] Napoleon gave his answer to his own advisers. "
                                        "And one of them wrote it down."),
    dict(id="n5", scene="quote", text="He said: society cannot exist without rich and poor. And rich and poor cannot "
                                      "exist without religion."),
    dict(id="n6", scene="starving", text="A starving man, next to a man with too much, would never accept it. Unless "
                                         "someone told him: God wants it this way. Your reward comes after you die."),
    dict(id="n7", scene="heaven", text="In his words, religion gives people an idea of equality in heaven. And that "
                                       "idea keeps the rich safe from the poor."),
    dict(id="n8", scene="church", text="He had already made a deal to bring the Church back to France, in "
                                       "[eighteen oh one.|1801.]"),
    dict(id="n9", scene="end", text="So what do you think? Was Napoleon right? Or is there another reason the "
                                    "[ninety-five|95] stay quiet?", pace=0.95),
]

METADATA = dict(
    title="Why Don't the Poor Rise Up? Napoleon's Answer Is Shocking 😳",
    alt_titles=["Napoleon Explained Why 95 Poor Never Fight 5 Rich 👑", "What Napoleon REALLY Said About Religion 😳"],
    description="""Why don't the poor rise up and take everything from the rich? Napoleon had an answer. 😳

Imagine the world has 100 people: 5 rich, 95 poor. The 95 are much stronger, so why do they accept it?

In 1806, Napoleon told his Council of State: society cannot exist without rich and poor, and rich and poor cannot exist without religion. A starving man next to a man with too much would never accept it, unless someone told him God wants it this way and his reward comes after he dies. In his words, religion gives people an idea of equality in heaven, and that keeps the rich safe from the poor.

He had already made a deal to bring the Church back to France in 1801 (the Concordat).

Source: Napoleon's remarks to the Council of State, 4 March 1806, recorded by Baron Pelet de la Lozère (1833). The viral line "religion is what keeps the poor from murdering the rich" is a shortened version of these words.

💬 So what do you think? Was Napoleon right, or is there another reason the 95 stay quiet? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Napoleon", "#History", "#Philosophy"],
    tags=["napoleon", "napoleon quote", "religion and power", "rich vs poor", "napoleon religion",
          "history facts", "philosophy", "inequality", "dark history", "interestingly strange"],
    pinned_comment="Was Napoleon right? Or is there another reason the 95 stay quiet? Let's hear it 👇",
)

ROYAL, ROYAL_D = hexc("#2b3a67"), hexc("#1d2849")
GOLD, GOLD_D = hexc("#f2c14e"), hexc("#b9862a")
SKIN = hexc("#f0c29c")
PALACE, PALACE_D = hexc("#3b2a2a"), hexc("#2a1d1d")
PARCH = hexc("#f4e4bc")
GREEN = hexc("#2e9e52")
BLUE = hexc("#3f6fb5")


def bg(cr, t, keys, color=PALACE, dur=0.3):
    cr.set_source_rgba(*color)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=dur)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)


def palace(cr):
    cr.set_source_rgba(*PALACE)
    cr.rectangle(-600, -400, 2000, 2400)
    cr.fill()
    for k in range(-3, 12):   # wall panels
        shape(cr, rrect_pts(k * 120 + 10, 150, 100, 640, 6, 12), PALACE_D, seed=10 + k, amp=0.4, lw=2.5,
              stroke=hexc("#5a4040"))
    shape(cr, [(-600, 900), (1400, 900), (1400, 2400), (-600, 2400)], hexc("#6b4a3a"), seed=30, amp=0.4, lw=4)


def napoleon(cr, t, x, y, s=1.0, mood="stern", talking=False):
    """Our Napoleon: a bust with the bicorne hat, blue coat, gold epaulettes and a hand tucked in the waistcoat."""
    with at(cr, x, y, s):
        # coat
        shape(cr, [(-170, 120), (170, 120), (210, 430), (-210, 430)], ROYAL, seed=40, amp=0.5, lw=5)
        shape(cr, [(-60, 120), (0, 300), (60, 120)], WHITE, seed=41, amp=0.3, lw=4)
        for sx in (-1, 1):
            blob(cr, sx * 150, 130, 50, 22, GOLD, seed=42 + sx, amp=0.4, lw=3.5, stroke=GOLD_D)
        shape(cr, [(-40, 250), (60, 230), (70, 290), (-30, 310)], ROYAL_D, seed=44, amp=0.3, lw=4)   # arm across
        blob(cr, 40, 262, 22, 18, SKIN, seed=45, amp=0.3, lw=3)                                      # tucked hand
        # head
        blob(cr, 0, 0, 92, 104, SKIN, seed=46, amp=0.5, lw=5)
        for k in range(5):   # hair fringe
            line(cr, [(-60 + k * 30, -70), (-50 + k * 30, -30)], 6, hexc("#4a3020"), seed=47 + k, amp=0.4)
        for sx in (-1, 1):
            blob(cr, sx * 34, -2, 12, 10 if mood != "wide" else 15, WHITE, seed=55 + sx, amp=0.1, lw=3)
            blob(cr, sx * 34, 0, 6, 6, INK, seed=57 + sx, amp=0.1, lw=0, stroke=None)
            if mood == "stern":
                line(cr, [(sx * 56, -28), (sx * 16, -18)], 6, INK, seed=59 + sx, amp=0.2)
        if talking:
            blob(cr, 0, 52, 22, 6 + 10 * abs(math.sin(t * 20)), hexc("#7a2b35"), seed=61, amp=0.2, lw=3)
        elif mood == "smirk":
            line(cr, [(-26, 52), (10, 56), (30, 44)], 5, INK, seed=62, amp=0.2)
        else:
            line(cr, [(-26, 54), (26, 54)], 5, INK, seed=63, amp=0.2)
        # the bicorne
        shape(cr, [(-220, -40), (-120, -120), (0, -190), (120, -120), (220, -40), (120, -70), (0, -80), (-120, -70)],
              hexc("#1a1a22"), seed=64, amp=0.5, lw=5)
        for r, col in ((30, "#2c4fa3"), (20, "#ffffff"), (10, "#d8323c")):     # tricolour cockade
            blob(cr, 130, -110, r, r, hexc(col), seed=65 + r, amp=0.2, lw=2.5)


def little(cr, x, y, s, rich, seed):
    """A tiny figure for the 100-people model."""
    with at(cr, x, y, s):
        blob(cr, 0, 0, 18, 18, SKIN if rich else hexc("#d9a77c"), seed=seed, amp=0.3, lw=3)
        shape(cr, rrect_pts(-16, 18, 32, 34, 8, 8), GOLD if rich else hexc("#8a7a66"), seed=seed + 1, amp=0.3, lw=3)
        if rich:   # top hat
            shape(cr, rrect_pts(-14, -46, 28, 30, 2, 6), INK, seed=seed + 2, amp=0.2, lw=0, stroke=None)
            shape(cr, rrect_pts(-22, -20, 44, 6, 2, 6), INK, seed=seed + 3, amp=0.2, lw=0, stroke=None)


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, (1.15, 360, 600)), (A("n1", "why"), (1.0, 360, 640)), (A("n1", "rich?"), (1.1, 360, 620))]
    bg(cr, t, keys)
    palace(cr)
    napoleon(cr, t, 360, 560, 1.15, "stern")
    hl(cr, t, [("why don't the ", INK), ("POOR", RED), (" rise up?", INK)], 215, 50, A("n1", "why"), bold=True,
       halo=hexc("#fbf3e1", 0.95))
    cue("hit", t, A("n1", "dangerous"))


def scene_crowd(cr, t, tl):
    A = tl.at
    keys = [(A("n2") - 0.2, (1.0, 360, 640)), (A("n3", "stronger."), (1.05, 360, 660)), (A("n3", "why"), (1.0, 360, 640))]
    bg(cr, t, keys, color=hexc("#efe6d6"))
    shape(cr, [(-600, 900), (1400, 900), (1400, 2400), (-600, 2400)], hexc("#d9c7a8"), seed=70, amp=0.4, lw=4)
    shown = int(100 * ease_out(seg(t, A("n2") - 0.1, A("n2", "100", end=True) + 0.6)))
    # 5 rich on a platform, 95 poor below
    if t >= A("n2", "five"):
        shape(cr, rrect_pts(200, 400, 320, 40, 8, 10), GOLD_D, seed=71, amp=0.3, lw=4)
    k = 0
    for i in range(5):
        if k < shown or t >= A("n2", "five"):
            little(cr, 240 + i * 60, 360, 1.0, True, seed=100 + i)
        k += 1
    glow = t >= A("n3", "stronger.")
    if glow:
        shape(cr, rrect_pts(40, 480, 640, 360, 20, 12), hexc("#2e9e52", 0.18), seed=72, amp=0.4, lw=0, stroke=None)
    for i in range(95):
        if k + i < shown:
            r, c = divmod(i, 19)
            little(cr, 60 + c * 33, 520 + r * 70, 0.75, False, seed=200 + i)
    if t >= A("n2", "five"):
        write(cr, [("5 RICH", GOLD_D)], 360, 300, 44, align="center", bold=True)
    if t >= A("n2", "95"):
        write(cr, [("95 POOR", INK)], 360, 498, 34, align="center", bold=True)
    hl(cr, t, [("100", RED), (" people", INK)], 215, 70, A("n2", "100"), end=A("n3") - 0.05, bold=True)
    hl(cr, t, [("95 ", GREEN), ("are stronger", INK)], 215, 66, A("n3"), end=A("n3", "why") - 0.05, bold=True)
    hl(cr, t, [("so why ", INK), ("ACCEPT", RED), (" it?", INK)], 215, 70, A("n3", "why"), bold=True, underline=True)


def scene_council(cr, t, tl):
    A = tl.at
    keys = [(A("n4") - 0.2, (1.25, 380, 720)), (A("n4", "advisers."), (1.3, 380, 730)), (A("n4", "wrote"), (1.5, 530, 770))]
    bg(cr, t, keys)
    palace(cr)
    shape(cr, rrect_pts(80, 820, 560, 60, 10, 12), hexc("#5a3a2a"), seed=80, amp=0.4, lw=4)    # council table
    for k, (who, x) in enumerate((("hilbert", 170), ("pujol", 300), ("claimant", 560))):
        person(cr, who, x, 900, t, facing=-1 if x > 360 else 1, eyes="wide" if t >= A("n4", "answer") else "dot",
               mouth="o" if t >= A("n4", "answer") else "flat", scale=0.95)
    napoleon(cr, t, 400, 520, 0.6, "stern", talking=A("n4", "answer") <= t < A("n4", "and"))
    if t >= A("n4", "wrote"):   # the councillor writing it down
        with at(cr, 560, 740, max(0.6, pop(t, A("n4", "wrote"), 0.25)) * 0.9, rot=-0.08):
            shape(cr, rrect_pts(-70, -46, 140, 92, 6, 10), PARCH, seed=81, amp=0.4, lw=3.5)
            for r in range(3):
                line(cr, [(-50, -20 + r * 20), (lerp(-50, 50, seg(t, A("n4", "wrote") + r * 0.2,
                                                                      A("n4", "wrote") + r * 0.2 + 0.4)), -20 + r * 20)],
                     3, INK, seed=82 + r, amp=0.3)
            line(cr, [(40, 30), (90, -40)], 4, hexc("#d9d9d9"), seed=85, amp=0.2)     # quill
    with at(cr, 360, 330, max(0.6, pop(t, A("n4", "1806,"), 0.3)) * 0.8, rot=-0.03):
        shape(cr, rrect_pts(-230, -70, 460, 140, 16, 12), PARCH, seed=86, amp=0.5, lw=5)
        write(cr, [("COUNCIL OF STATE", INK)], 0, -10, 40, align="center", bold=True)
        write(cr, [("1806", RED)], 0, 46, 46, align="center", bold=True)


def scroll(cr, t, lines, x, y, s):
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-300, -170, 600, 340, 14, 14), PARCH, seed=90, amp=0.6, lw=5)
        for sx in (-1, 1):
            blob(cr, sx * 300, 0, 26, 175, hexc("#d9c08a"), seed=91 + sx, amp=0.5, lw=4)
        for k, (runs, st) in enumerate(lines):
            if t >= st:
                write(cr, runs, 0, -100 + k * 74, 46, align="center", bold=True,
                      progress=ease_out(seg(t, st, st + 0.4)))


def scene_quote(cr, t, tl):
    A = tl.at
    keys = [(A("n5") - 0.2, (1.0, 360, 620)), (A("n5", "religion."), (1.08, 360, 640))]
    bg(cr, t, keys)
    palace(cr)
    lines = [([("No society without", INK)], A("n5", "society")),
             ([("RICH", GOLD_D), (" and ", INK), ("POOR", RED)], A("n5", "rich")),
             ([("No rich and poor", INK)], A("n5", "and", nth=2)),
             ([("without ", INK), ("RELIGION", BLUE)], A("n5", "religion."))]
    scroll(cr, t, lines, 360, 560, 1.1)
    napoleon(cr, t, 600, 900, 0.45, "stern", talking=tl.at("n5") <= t)
    hl(cr, t, [("Napoleon, ", INK), ("1806", RED)], 215, 62, A("n5"), bold=True, halo=hexc("#fbf3e1", 0.95))
    cue("hit", t, A("n5", "religion."))


def scene_starving(cr, t, tl):
    A = tl.at
    keys = [(A("n6") - 0.2, (1.6, 350, 790)), (A("n6", "unless"), (1.55, 350, 770)), (A("n6", "reward"), (1.6, 350, 760))]
    bg(cr, t, keys, color=hexc("#efe6d6"))
    shape(cr, [(-600, 900), (1400, 900), (1400, 2400), (-600, 2400)], hexc("#d9c7a8"), seed=100, amp=0.4, lw=4)
    # the man with too much, at a feast
    shape(cr, rrect_pts(380, 800, 200, 26, 6, 10), hexc("#8a5a3a"), seed=101, amp=0.3, lw=4)
    for k in range(4):
        blob(cr, 405 + k * 50, 788, 26, 18, (GOLD, hexc("#c0504d"), hexc("#79b061"), hexc("#e0a050"))[k], seed=102 + k,
             amp=0.4, lw=3)
    person(cr, "seth", 500, 900, t, facing=-1, arms=("hold", "hold"), eyes="happy", mouth="grin", scale=1.0)
    person(cr, "beggar", 200, 900, t, facing=1, arms=("hold", "down"), eyes="wide" if t < A("n6", "unless") else "dot",
           mouth="o", scale=1.0, sweat=t < A("n6", "unless"))
    if t >= A("n6", "god"):
        with at(cr, 350, 650, max(0.6, pop(t, A("n6", "god"), 0.25)) * 0.82):
            shape(cr, rrect_pts(-230, -60, 460, 120, 30, 12), WHITE, seed=110, amp=0.4, lw=4)
            write(cr, [("\"God wants it this way.\"", INK)], 0, -6, 34, align="center", bold=True)
            if t >= A("n6", "reward"):
                write(cr, [("your reward: ", INK), ("LATER", GOLD_D)], 0, 40, 32, align="center", bold=True)
    hl(cr, t, [("starving ", RED), ("next to ", INK), ("too much", GOLD_D)], 215, 60, A("n6"), end=A("n6", "unless") - 0.05,
       bold=True)


def scene_heaven(cr, t, tl):
    A = tl.at
    keys = [(A("n7") - 0.2, (1.0, 360, 640)), (A("n7", "safe"), (1.05, 360, 700))]
    bg(cr, t, keys, color=hexc("#cfe3f5"))
    for k in range(5):   # clouds
        blob(cr, 80 + k * 140, 380 + (k % 2) * 30, 90, 40, WHITE, seed=120 + k, amp=0.6, lw=3)
    # in heaven: rich and poor, equal
    little(cr, 250, 420, 2.4, True, seed=130)
    little(cr, 470, 420, 2.4, False, seed=131)
    write(cr, [("=", INK)], 360, 460, 110, align="center", bold=True)
    shape(cr, [(-600, 900), (1400, 900), (1400, 2400), (-600, 2400)], hexc("#d9c7a8"), seed=132, amp=0.4, lw=4)
    if t >= A("n7", "safe"):   # down here: the 5 stay safe
        for i in range(5):
            little(cr, 200 + i * 80, 700, 1.5, True, seed=140 + i)
        shape(cr, rrect_pts(160, 790, 400, 26, 6, 10), GOLD_D, seed=146, amp=0.3, lw=3)
        for i in range(8):
            little(cr, 80 + i * 80, 860, 1.1, False, seed=150 + i)
    hl(cr, t, [("equality... ", INK), ("in heaven", BLUE)], 215, 64, A("n7", "equality"), end=A("n7", "safe") - 0.05,
       bold=True)
    hl(cr, t, [("so the rich stay ", INK), ("SAFE", GOLD_D)], 215, 62, A("n7", "safe"), bold=True)


def scene_church(cr, t, tl):
    A = tl.at
    keys = [(A("n8") - 0.2, (1.0, 360, 640)), (A("n8", "1801."), (1.08, 360, 620))]
    bg(cr, t, keys, color=hexc("#efe6d6"))
    shape(cr, [(-600, 900), (1400, 900), (1400, 2400), (-600, 2400)], hexc("#d9c7a8"), seed=160, amp=0.4, lw=4)
    shape(cr, rrect_pts(220, 520, 280, 380, 6, 12), hexc("#e9dcc0"), seed=161, amp=0.5, lw=5)          # church
    sharp_shape(cr, [(200, 530), (360, 380), (520, 530)], hexc("#a0453a"), seed=162, amp=0.4, lw=5)
    shape(cr, rrect_pts(330, 760, 60, 140, 26, 10), hexc("#6d4524"), seed=163, amp=0.3, lw=4)
    line(cr, [(360, 300), (360, 380)], 8, INK, seed=164, amp=0.2)
    line(cr, [(335, 325), (385, 325)], 8, INK, seed=165, amp=0.2)
    napoleon(cr, t, 600, 880, 0.4, "smirk")
    if t >= A("n8", "1801."):
        with at(cr, 360, 300, max(0.6, pop(t, A("n8", "1801."), 0.3)) * 0.8, rot=-0.04):
            shape(cr, rrect_pts(-200, -60, 400, 120, 16, 12), PARCH, seed=166, amp=0.5, lw=5)
            write(cr, [("THE DEAL: ", INK), ("1801", RED)], 0, 16, 46, align="center", bold=True)
    hl(cr, t, [("bring back the ", INK), ("CHURCH", BLUE)], 215, 62, A("n8", "church"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("n9") - 0.2, (1.1, 360, 620)), (A("n9", "right?"), (1.0, 360, 640))]
    bg(cr, t, keys)
    palace(cr)
    napoleon(cr, t, 360, 560, 1.05, "smirk")
    for k, (lab, col, x) in enumerate((("RIGHT", GREEN, 200), ("WRONG", hexc("#e0483d"), 520))):
        if t >= A("n9", "right?"):
            with at(cr, x, 1040, max(0.6, pop(t, A("n9", "right?") + k * 0.12, 0.25)) * 0.8):
                shape(cr, rrect_pts(-120, -46, 240, 92, 46, 14), col, seed=170 + k, amp=0.3, lw=4)
                write(cr, [(lab, WHITE)], 0, 16, 48, align="center", bold=True)
    hl(cr, t, [("was Napoleon ", INK), ("RIGHT", GREEN), ("?", INK)], 215, 64, A("n9", "napoleon"), bold=True,
       underline=True, halo=hexc("#fbf3e1", 0.95))
    stamp(cr, t, A("n9", "quiet?", end=True), "COMMENT BELOW!", dur=0.8, y=330)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "crowd": scene_crowd, "council": scene_council, "quote": scene_quote,
     "starving": scene_starving, "heaven": scene_heaven, "church": scene_church, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
