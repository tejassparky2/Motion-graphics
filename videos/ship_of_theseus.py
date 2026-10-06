"""Episode 23: "The Ship of Theseus" — replace every plank of a ship; is it still the same ship?

Sources: Plutarch (Life of Theseus, about 75 AD) describes the Athenians preserving Theseus's ship by replacing rotten
timbers, and philosophers arguing over whether it stayed the same ship. Thomas Hobbes (De Corpore, 1655) added the
second ship rebuilt from the old planks. Body renewal figures are rounded and hedged: the skin's outer layer renews
over weeks, red blood cells last about four months, and the skeleton is remodelled over roughly ten years.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import INK, RED, WHITE, at, blob, cue, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import camera, hl, stamp, whip

NARRATOR = dict(speed=1.0)
TAIL = 0.9

SCRIPT = [
    dict(id="t1", scene="ship",
         text="If you replace every part of a ship, one plank at a time, is it still the same ship?"),
    dict(id="t2", scene="greek",
         text="People have argued about this for almost [two thousand years.|2,000 years.] "
              "It's called the Ship of Theseus."),
    dict(id="t3", scene="ship",
         text="The hero's old ship is kept in the harbor. Every time a plank rots, they swap in a new one."),
    dict(id="t4", scene="ship", text="Years go by. Then the last old plank is gone. Not one original piece is left."),
    dict(id="t5", scene="ship", text="So, is it still his ship?"),
    dict(id="t6", scene="two",
         text="Now the twist. Someone kept every old plank, and built a second ship out of them."),
    dict(id="t7", scene="two", text="Two ships. One has the history. The other has every original piece."),
    dict(id="t8", scene="two", text="Which one is the real Ship of Theseus?"),
    dict(id="t9", scene="you",
         text="Before you answer: your body does the same thing. Your skin, your blood, even your bones keep "
              "rebuilding themselves."),
    dict(id="t10", scene="you", text="So... are you still the same you?", gap=0.25),
]

METADATA = dict(
    title="If You Replace Every Part… Is It Still the Same Ship? 🚢🤯",
    alt_titles=["The 2,000-Year-Old Puzzle Nobody Can Solve 🚢", "Ship A or Ship B? (Ship of Theseus) 🤯"],
    description="""Replace every plank of a ship, one at a time. Is it still the same ship? 🚢

It's the Ship of Theseus, a puzzle people have argued about for almost 2,000 years. The Greek writer Plutarch described the Athenians keeping their hero's ship by swapping rotten planks for new ones. Centuries later, philosopher Thomas Hobbes added the twist: what if someone rebuilt a second ship from all the old planks?

And your body does something similar: your skin renews every few weeks, red blood cells last about 4 months, and your skeleton rebuilds itself over roughly 10 years. 🤯

💬 Ship A (the history) or Ship B (the original parts)? Comment A or B 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Paradox", "#Philosophy", "#MindBlown"],
    tags=["ship of theseus", "theseus paradox", "paradox", "philosophy", "thought experiment", "identity paradox",
          "mind blowing", "brain teaser", "philosophy shorts", "interestingly strange"],
    pinned_comment="Comment A or B 👇 A = the ship with the history, B = the ship with every original plank 🚢",
)

SKY = hexc("#9fd8f5")
SKY2 = hexc("#cdeefb")
SEA = hexc("#2f86c9")
SEA2 = hexc("#4aa3e0")
OLD = hexc("#7a4b26")
OLD_D = hexc("#5a3417")
NEW = hexc("#e8b66e")
NEW_D = hexc("#c99448")
SAIL = hexc("#f4efe1")
GOLD = hexc("#f2b51d")
BLUE = hexc("#3f6fb5")
GREEN = hexc("#3d8f45")
MARBLE = hexc("#efe9dc")
NPL = 8                    # planks in the hull
WATER_Y = 960


def world(cr, t, keys, dur=0.14):
    z, fx, fy = camera(t, keys, dur=dur)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)


def harbor(cr, t, sun=True):
    cr.rectangle(-1200, -800, 3200, 2800)
    cr.set_source_rgba(*SKY)
    cr.fill()
    cr.rectangle(-1200, 600, 3200, WATER_Y - 600)
    cr.set_source_rgba(*SKY2)
    cr.fill()
    if sun:
        blob(cr, 600, 330, 60, 60, hexc("#ffe08a"), seed=40, amp=0.4, lw=3)
    for k in range(4):
        x = (-300 + k * 420 + t * 12) % 1800 - 400
        blob(cr, x, 260 + (k % 2) * 90, 70, 26, WHITE, seed=41 + k, amp=0.8, lw=0, stroke=None)
    # dock on the left
    sharp_shape(cr, [(-600, WATER_Y - 40), (-40, WATER_Y - 40), (-40, WATER_Y - 10), (-600, WATER_Y - 10)],
                hexc("#8e5a2e"), seed=50, amp=0.6, lw=3.5)
    for x in (-500, -300, -100):
        line(cr, [(x, WATER_Y - 10), (x, WATER_Y + 120)], 10, hexc("#6d4524"), seed=51 + x, amp=0.3)
    cr.rectangle(-1200, WATER_Y, 3200, 1600)
    cr.set_source_rgba(*SEA)
    cr.fill()
    for r in range(6):
        y = WATER_Y + 40 + r * 70
        for k in range(10):
            x = -400 + k * 160 + ((t * 30 + r * 50) % 160)
            line(cr, [(x, y), (x + 30, y - 10), (x + 60, y)], 4, SEA2, seed=60 + r * 10 + k, amp=0.2)


def hull(cr, x, y, s, planks, t, rock=True, sail_col=SAIL, flag=None):
    """planks: list of 'old' / 'new' / None (missing), bottom row first."""
    ang = 0.03 * math.sin(t * 1.6) if rock else 0.0
    with at(cr, x, y + (4 * math.sin(t * 1.6) if rock else 0), s, rot=ang):
        # mast and sail
        line(cr, [(0, -40), (0, -330)], 9, hexc("#6d4524"), seed=70, amp=0.3)
        shape(cr, [(8, -310), (150, -200), (130, -90), (8, -80)], sail_col, seed=71, amp=0.6, lw=3.5)
        if flag:
            shape(cr, [(0, -330), (60, -312), (0, -296)], flag, seed=72, amp=0.3, lw=3)
        # hull: planks stacked from the keel up, each a little longer
        for i, kind in enumerate(planks):
            yy = -i * 24
            half = 150 + i * 16
            top_half = 150 + (i + 1) * 16
            pts = [(-half, yy), (half, yy), (top_half, yy - 24), (-top_half, yy - 24)]
            if kind is None:
                sharp_shape(cr, pts, None, seed=80 + i, amp=0.4, lw=2.5, stroke=hexc("#2b2d3a", 0.35))
                continue
            sharp_shape(cr, pts, OLD if kind == "old" else NEW, seed=80 + i, amp=0.4, lw=3.5)
            col = OLD_D if kind == "old" else NEW_D
            for k in range(-2, 3):   # grain / cracks
                xx = k * half * 0.38
                line(cr, [(xx, yy - 6), (xx + 26, yy - 18)] if kind == "old" else [(xx, yy - 12), (xx + 40, yy - 12)],
                     2.5, col, seed=90 + i * 7 + k, amp=0.4)


def planks_at(t, start, end):
    """Hull state while planks are swapped one by one between start and end."""
    n = int(NPL * seg(t, start, end) + 1e-6)
    return ["new" if i < n else "old" for i in range(NPL)], n


ORDER = [3, 0, 6, 1, 7, 4, 2, 5]           # the order planks get swapped (looks random)


def swap_state(t, start, end):
    done = int(NPL * seg(t, start, end) + 1e-6)
    st = ["old"] * NPL
    for k in range(done):
        st[ORDER[k]] = "new"
    return st, done


def scene_ship(cr, t, tl):
    A = tl.at
    keys = [(0, (1.5, 360, 820)), (A("t1", "replace"), (1.0, 360, 800)), (A("t1", "every"), (1.3, 360, 880)),
            (A("t1", "plank"), (1.9, 330, 900)), (A("t1", "time,"), (1.2, 360, 840)), (A("t1", "still"), (1.0, 360, 800)),
            (A("t1", "same"), (1.4, 360, 760))]
    if A("t3") <= t:
        keys = [(A("t3") - 0.1, (1.25, 330, 820)), (A("t3", "harbor."), (0.95, 300, 820)),
                (A("t3", "rots,"), (1.8, 380, 900)), (A("t3", "swap"), (1.3, 360, 860)), (A("t3", "new"), (1.6, 340, 880)),
                (A("t4") - 0.1, (1.0, 360, 820)), (A("t4", "years"), (1.25, 360, 840)), (A("t4", "last"), (1.8, 360, 900)),
                (A("t4", "not"), (1.0, 360, 820)), (A("t4", "piece"), (1.4, 360, 860)),
                (A("t5") - 0.1, (1.1, 360, 780)), (A("t5", "still"), (1.5, 360, 760)), (A("t5", "ship?"), (1.0, 360, 780))]
    world(cr, t, keys)
    harbor(cr, t)
    x, y = 360, WATER_Y + 10
    if t < A("t3"):
        # the opening question: planks flash from old to new all the way up
        st, done = swap_state(t, A("t1", "replace"), A("t1", "time,", end=True))
        hull(cr, x, y, 1.0, st, t)
        for k in range(done):
            cue("pop", t, A("t1", "replace") + k * (A("t1", "time,", end=True) - A("t1", "replace")) / NPL)
        if t >= A("t1", "still"):
            with at(cr, 600, 560, max(0.85, pop(t, A("t1", "still"), 0.25)), rot=0.1 * math.sin(t * 5)):
                write(cr, [("?", RED)], 0, 50, 160, align="center", bold=True)
        hl(cr, t, [("replace ", INK), ("EVERY", RED), (" part", INK)], 215, 70, 0.0, end=A("t1", "still") - 0.05,
           bold=True, sound=False)
        hl(cr, t, [("still the ", INK), ("SAME", RED), (" ship?", INK)], 215, 70, A("t1", "still"), bold=True)
        return
    # t3..t5: slow swaps in the harbor, years passing
    if t < A("t4"):
        st, done = swap_state(t, A("t3", "rots,"), A("t3", end=True) + 0.3)
        done = min(done, 3)
        st = ["old"] * NPL
        for k in range(done):
            st[ORDER[k]] = "new"
    else:
        st, done = swap_state(t, A("t4") - 1.2, A("t4", "gone.", end=True))
        done = max(done, 3)
        st = ["old"] * NPL
        for k in range(done):
            st[ORDER[k]] = "new"
    hull(cr, x, y, 1.0, st, t, flag=hexc("#e0487a"))
    # the old plank being carried off to the dock
    if A("t3", "rots,") <= t < A("t4", "not"):
        bob = 6 * math.sin(t * 8)
        sharp_shape(cr, [(-260, WATER_Y - 70 + bob), (-120, WATER_Y - 74 + bob), (-118, WATER_Y - 52 + bob),
                         (-258, WATER_Y - 48 + bob)], OLD, seed=110, amp=0.4, lw=3)
    # counter
    cr.save()
    cr.identity_matrix()
    with at(cr, 360, 330, 1.0):
        shape(cr, rrect_pts(-150, -42, 300, 84, 16, 16), WHITE, seed=120, amp=0.4, lw=3.5)
        write(cr, [(f"{done}/{NPL}", RED if done == NPL else INK), (" planks new", INK)], 0, 16, 44,
              align="center", bold=True)
    if t >= A("t4", "years"):   # years passing
        yr = int(lerp(1, 40, seg(t, A("t4", "years"), A("t4", "gone.", end=True))))
        write(cr, [(f"year {yr}", INK)], 360, 420, 40, align="center", bold=True)
    cr.restore()
    if A("t4", "not") <= t < A("t5"):
        stamp(cr, t, A("t4", "not"), "0 ORIGINAL PIECES", dur=0.7, y=520)
    hl(cr, t, [("the hero's ", INK), ("ship", BLUE)], 215, 74, A("t3"), end=A("t3", "rots,") - 0.05, bold=True)
    hl(cr, t, [("a plank rots... ", INK), ("SWAP", RED)], 215, 70, A("t3", "rots,"), end=A("t4") - 0.05, bold=True)
    hl(cr, t, [("years go by", INK)], 215, 74, A("t4"), end=A("t4", "not") - 0.05, bold=True)
    hl(cr, t, [("still ", INK), ("HIS", RED), (" ship?", INK)], 215, 84, A("t5"), bold=True, underline=True)
    for w in (A("t4", "gone."), A("t5", "ship?")):
        cue("hit", t, w)


def column(cr, x, y, h, seed):
    sharp_shape(cr, [(x - 50, y), (x + 50, y), (x + 50, y - 26), (x - 50, y - 26)], MARBLE, seed=seed, amp=0.4, lw=3.5)
    sharp_shape(cr, [(x - 36, y - 26), (x + 36, y - 26), (x + 36, y - h), (x - 36, y - h)], MARBLE, seed=seed + 1,
                amp=0.4, lw=3.5)
    for k in (-18, 0, 18):
        line(cr, [(x + k, y - 34), (x + k, y - h + 8)], 2.5, hexc("#c9c2b0"), seed=seed + 2 + k, amp=0.3)
    sharp_shape(cr, [(x - 56, y - h), (x + 56, y - h), (x + 56, y - h - 30), (x - 56, y - h - 30)], MARBLE,
                seed=seed + 5, amp=0.4, lw=3.5)


def scene_greek(cr, t, tl):
    A = tl.at
    keys = [(A("t2") - 0.2, (1.3, 360, 760)), (A("t2", "argued"), (1.0, 360, 780)), (A("t2", "2,000"), (1.5, 360, 600)),
            (A("t2", "called"), (1.0, 360, 780)), (A("t2", "theseus."), (1.35, 360, 820))]
    world(cr, t, keys)
    cr.rectangle(-1200, -800, 3200, 2800)
    cr.set_source_rgba(*hexc("#f6e7c8"))
    cr.fill()
    sharp_shape(cr, [(-800, 1150), (1600, 1150), (1600, 2000), (-800, 2000)], hexc("#d8c7a3"), seed=200, amp=0.6, lw=4)
    sharp_shape(cr, [(-60, 420), (780, 420), (360, 300)], MARBLE, seed=201, amp=0.6, lw=4)    # pediment
    sharp_shape(cr, [(-60, 420), (780, 420), (780, 450), (-60, 450)], MARBLE, seed=202, amp=0.5, lw=4)
    for k, x in enumerate((20, 250, 470, 700)):
        column(cr, x, 1150, 700, 210 + k * 10)
    # two thinkers arguing
    for who, x, face in (("claimant", 170, 1), ("successor", 550, -1)):
        argue = int(t * 4 + (x > 360)) % 2 == 0
        person(cr, who, x, 1150, t, facing=face, arms=("point", "hip") if argue else ("chin", "hip"),
               eyes="sly", mouth="o" if argue else "flat")
    # a scroll with the name
    if t >= A("t2", "called"):
        k = ease_out(seg(t, A("t2", "called"), A("t2", "called") + 0.35))
        w = 260 * k + 10
        sharp_shape(cr, [(360 - w, 600), (360 + w, 600), (360 + w, 740), (360 - w, 740)], hexc("#f4e2b8"), seed=220,
                    amp=0.4, lw=3.5)
        for sx in (360 - w, 360 + w):
            blob(cr, sx, 670, 16, 80, hexc("#c99448"), seed=221 + int(sx), amp=0.3, lw=3)
        if k >= 1:
            write(cr, [("SHIP OF", INK)], 360, 660, 46, align="center", bold=True)
            write(cr, [("THESEUS", RED)], 360, 720, 58, align="center", bold=True)
        cue("whoosh", t, A("t2", "called"))
    if A("t2", "2,000") <= t < A("t2", "called"):
        with at(cr, 360, 640, max(0.85, pop(t, A("t2", "2,000"), 0.25)), rot=-0.05):
            write(cr, [("~2,000", RED)], 0, 0, 110, align="center", bold=True)
            write(cr, [("YEARS", INK)], 0, 70, 60, align="center", bold=True)
    hl(cr, t, [("argued for almost ", INK), ("2,000 years", RED)], 215, 54, A("t2", "argued"),
       end=A("t2", "called") - 0.05, bold=True)
    hl(cr, t, [("the ", INK), ("SHIP OF THESEUS", BLUE)], 215, 64, A("t2", "called"), bold=True)


def scene_two(cr, t, tl):
    A = tl.at
    xa, xb = 200, 560
    keys = [(A("t6") - 0.2, (1.1, 220, 860)), (A("t6", "twist."), (1.35, 220, 820)), (A("t6", "kept"), (1.5, -220, 900)),
            (A("t6", "built"), (1.35, xb, 880)), (A("t6", "second"), (0.95, 380, 860)),
            (A("t7", "two"), (0.95, 380, 860)), (A("t7", "one"), (1.15, xa + 60, 820)), (A("t7", "other"), (1.15, xb - 60, 820)),
            (A("t8"), (0.95, 380, 860)), (A("t8", "real"), (1.1, 380, 840)), (A("t8", "theseus?"), (0.95, 380, 860))]
    world(cr, t, keys)
    harbor(cr, t, sun=False)
    # ship A: all new planks, with the flag (the history)
    hull(cr, xa, WATER_Y + 10, 0.7, ["new"] * NPL, t, flag=hexc("#e0487a"))
    # ship B: built from the old planks, plank by plank
    built = int(NPL * seg(t, A("t6", "built"), A("t6", "them.", end=True)) + 1e-6)
    if t >= A("t7"):
        built = NPL
    if t >= A("t6", "built"):
        hull(cr, xb, WATER_Y + 10, 0.7, ["old" if i < built else None for i in range(NPL)], t + 1.3,
             sail_col=hexc("#d8cfba"))
    # the pile of old planks on the dock
    left = NPL - built if t >= A("t6", "kept") else 0
    for k in range(left):
        sharp_shape(cr, [(-420, WATER_Y - 50 - k * 16), (-200, WATER_Y - 52 - k * 16), (-198, WATER_Y - 38 - k * 16),
                         (-418, WATER_Y - 36 - k * 16)], OLD, seed=300 + k, amp=0.4, lw=2.5)
    if t >= A("t7"):
        for x, lab, sub, col in ((xa, "A", "the history", BLUE), (xb, "B", "the original parts", hexc("#8e5a2e"))):
            with at(cr, x, 600, max(0.85, pop(t, A("t7", "one" if lab == "A" else "other"), 0.25))):
                blob(cr, 0, 0, 50, 50, col, seed=310 + ord(lab), amp=0.4, lw=4)
                write(cr, [(lab, WHITE)], 0, 24, 66, align="center", bold=True)
                write(cr, [(sub, INK)], 0, -66, 40, align="center", bold=True)
    if t >= A("t8", "real"):
        with at(cr, 380, 760, 1.0, rot=0.1 * math.sin(t * 5)):
            write(cr, [("?", RED)], 0, 50, 170, align="center", bold=True)
        cue("hit", t, A("t8", "real"))
    hl(cr, t, [("now the ", INK), ("TWIST", RED)], 215, 80, A("t6", "twist."), end=A("t6", "kept") - 0.05, bold=True)
    hl(cr, t, [("a ", INK), ("SECOND", RED), (" ship from the old planks", INK)], 215, 44, A("t6", "kept"),
       end=A("t7") - 0.05, bold=True)
    hl(cr, t, [("TWO", RED), (" ships", INK)], 215, 84, A("t7"), end=A("t8") - 0.05, bold=True)
    hl(cr, t, [("which one is ", INK), ("REAL", RED), ("?", INK)], 215, 72, A("t8"), bold=True, underline=True)


def scene_you(cr, t, tl):
    A = tl.at
    keys = [(A("t9") - 0.2, (1.1, 360, 780)), (A("t9", "body"), (1.45, 300, 740)), (A("t9", "skin,"), (1.3, 400, 700)),
            (A("t9", "blood,"), (1.3, 420, 760)), (A("t9", "bones"), (1.3, 400, 820)), (A("t9", "rebuilding"), (1.05, 360, 780)),
            (A("t10"), (1.2, 360, 720)), (A("t10", "same"), (1.8, 360, 640)), (A("t10", "you?", nth=2), (1.0, 360, 760))]
    world(cr, t, keys)
    cr.rectangle(-1200, -800, 3200, 2800)
    cr.set_source_rgba(*hexc("#f6e7c8"))
    cr.fill()
    for k in range(12):   # sparkles: the body rebuilding itself
        u = (t * 0.7 + k / 12) % 1
        a = k * 2.4
        x = 220 + math.cos(a) * (90 + 40 * u)
        y = 760 + math.sin(a) * 200 * (1 - u) - 60
        blob(cr, x, y, 7 * (1 - u) + 1, 7 * (1 - u) + 1, hexc("#f2b51d", 1 - u), seed=400 + k, amp=0.2, lw=0,
             stroke=None)
    mirror = t >= A("t10")
    person(cr, "sam", 230 if mirror else 220, 980, t, scale=1.6, arms=("chin", "hip") if mirror else ("hip", "hip"),
           eyes="wide" if mirror else "dot", mouth="o" if mirror else "smile")
    if mirror:   # the "same" you, a little different, in the mirror
        sharp_shape(cr, [(410, 520), (660, 520), (660, 1000), (410, 1000)], hexc("#d7eef9"), seed=410, amp=0.5, lw=5)
        cr.save()
        cr.rectangle(410, 520, 250, 480)
        cr.clip()
        person(cr, "sam", 535, 980, t, scale=1.35, facing=-1, arms=("chin", "hip"), eyes="sly", mouth="smirk")
        cr.restore()
    labels = (("skin,", "skin: every few weeks", 490, 620), ("blood,", "blood cells: ~4 months", 490, 740),
              ("bones", "bones: ~10 years", 490, 860))
    if not mirror:
        for key, txt, x, y in labels:
            if t >= A("t9", key):
                with at(cr, x, y, max(0.85, pop(t, A("t9", key), 0.25))):
                    shape(cr, rrect_pts(-170, -36, 340, 60, 12, 14), WHITE, seed=420 + y, amp=0.4, lw=3)
                    write(cr, [(txt, INK)], 0, 6, 28, align="center", bold=True)
                cue("pop", t, A("t9", key))
    hl(cr, t, [("your ", INK), ("BODY", RED), (" does it too", INK)], 215, 66, A("t9", "body"),
       end=A("t9", "skin,") - 0.05, bold=True)
    hl(cr, t, [("always ", INK), ("REBUILDING", RED)], 215, 70, A("t9", "skin,"), end=A("t10") - 0.05, bold=True)
    hl(cr, t, [("still the ", INK), ("SAME YOU", RED), ("?", INK)], 215, 70, A("t10", "same"), bold=True,
       underline=True)
    if t >= A("t10", "you?", end=True, nth=2) - 0.1:
        stamp(cr, t, A("t10", "you?", end=True, nth=2) - 0.1, "A or B? COMMENT", dur=0.8, y=330)
    cue("hit", t, A("t10", "same"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"ship": scene_ship, "greek": scene_greek, "two": scene_two, "you": scene_you}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
