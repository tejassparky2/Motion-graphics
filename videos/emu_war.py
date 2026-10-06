"""Episode 4: "The Great Emu War" (Western Australia, 1932).

Facts (checked against Wikipedia's "Emu War" article and its sources):
- Nov-Dec 1932, Campion district, Western Australia; many farmers were WWI ex-servicemen growing wheat
- about 20,000 emus migrated in and damaged crops
- the army sent 3 soldiers (Major G.P.W. Meredith + 2) with 2 Lewis guns and 10,000 rounds
- the emus split into small groups; the first attempt was withdrawn after ridicule in the press
- Meredith said they could "face machine guns with the invulnerability of tanks"
- a second attempt used 9,860 rounds before withdrawal
- later requests for military help (1934, 1943, 1948) were refused
Kill counts are disputed, so the script doesn't use them.
"""
import math

from motion.captions import captions
from motion.characters import person, truck
from motion.critters import emu, lewis_gun
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_in, ease_out, hexc, lerp, line, pop,
                           rrect_pts, seg, shape, sharp_shape, write)
from motion.kit import camera, confetti, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict(speed=1.05)   # long spoken numbers ("nineteen thirty-two") slow this one down

SCRIPT = [
    dict(id="e1", scene="field", text="In [nineteen thirty-two,|1932,] Australia went to war, against birds. And the birds won."),
    dict(id="e2", scene="field", text="Farmers in Western Australia, lots of them ex-soldiers, were growing wheat."),
    dict(id="e3", scene="field", text="Then around [twenty thousand|20,000] emus showed up, and started eating everything."),
    dict(id="e4", scene="army",
         text="So the government sent in the army. [Three|3] soldiers, [two|2] machine guns, and [ten thousand|10,000] bullets.",
         gap=0.25),
    dict(id="e5", scene="battle", text="Easy, right? Nope.", pace=0.92, gap=0.25),
    dict(id="e6", scene="battle",
         text="The emus split into tiny groups and scattered. Bullets missed, the birds kept eating, and newspapers made fun of the army."),
    dict(id="e7", scene="tank", text="The commander even said the emus could face machine guns like tanks."),
    dict(id="e8", scene="retreat",
         text="They tried again. Nearly [ten thousand|9,860] more bullets later, the army pulled out.", gap=0.25),
    dict(id="e9", scene="retreat", text="Farmers asked for the army three more times. The answer was always no."),
    dict(id="e10", scene="retreat", text="So yes. The emus won.", pace=0.92),
]

METADATA = dict(
    title="Australia Declared War on Emus… and Lost 🐦",
    alt_titles=["The Army That Lost a War to Birds 🐦", "3 Soldiers, 2 Machine Guns, 20,000 Emus 🐦"],
    description="""In 1932, Australia sent soldiers with machine guns to fight 20,000 emus… and the emus won. 🐦

This really happened. It's called the Great Emu War: farmers in Western Australia asked for help after emus flattened their wheat. The army came with 2 Lewis guns and 10,000 rounds — and still had to pull out.

💬 Who would you bet on: 3 soldiers or 20,000 emus?

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#EmuWar", "#WeirdHistory", "#History"],
    tags=["emu war", "great emu war", "weird history", "australia history", "history facts", "funny history",
          "emus", "strange but true", "history shorts", "interestingly strange"],
    pinned_comment="The emus are still undefeated 🐦🏆 What weird war should we cover next? 👇",
)

SKY = hexc("#9fd3f0")
WHEAT = hexc("#e3b24a")
WHEAT_D = hexc("#b8862e")
DIRT = hexc("#c89b62")
ARMY = (hexc("#6b7a3a"), hexc("#4a5528"))
GOLD = hexc("#b8862e")


def field_set(cr, t, eaten=0.0):
    cr.set_source_rgba(*SKY)
    cr.paint()
    for i, (x, y) in enumerate([(120, 330), (560, 280), (860, 400)]):
        blob(cr, x + math.sin(t * 0.3 + i) * 10, y, 70, 26, WHITE, seed=2000 + i, amp=2, lw=3)
    blob(cr, 620, 380, 50, 50, hexc("#ffd23f"), seed=2005, amp=1, lw=3.5)
    sharp_shape(cr, [(-800, 760), (1500, 740), (1500, 1800), (-800, 1800)], DIRT, seed=2010, amp=1, lw=4)
    # farmhouse
    sharp_shape(cr, [(-60, 600), (120, 600), (120, 760), (-60, 760)], hexc("#e8dcc0"), seed=2011, amp=0.8, lw=4)
    sharp_shape(cr, [(-80, 604), (30, 520), (140, 604)], hexc("#c0504d"), seed=2012, amp=0.8, lw=4)
    sharp_shape(cr, [(20, 690), (60, 690), (60, 760), (20, 760)], hexc("#8e4a1e"), seed=2013, amp=0.5, lw=3)
    # wheat rows (fewer standing where the emus have eaten)
    for row in range(5):
        y = 800 + row * 90
        for k in range(-6, 16):
            x = k * 60 + (row % 2) * 30
            standing = ((k * 7 + row * 3) % 10) / 10 >= eaten
            h = 70 if standing else 16
            sway = math.sin(t * 2 + k * 0.7 + row) * 4
            line(cr, [(x, y), (x + sway, y - h)], 4, WHEAT_D, seed=2020 + row * 40 + k, amp=0.4)
            if standing:
                blob(cr, x + sway, y - h - 10, 7, 14, WHEAT, seed=2021 + row * 40 + k, amp=0.4, lw=2.5)
    for k in range(-4, 12):   # fence
        line(cr, [(k * 110, 770), (k * 110, 700)], 6, hexc("#8e4a1e"), seed=2100 + k, amp=0.3)
    line(cr, [(-500, 720), (1400, 715)], 4, hexc("#8e4a1e"), seed=2120, amp=0.8)


def scene_field(cr, t, tl):
    A = tl.at
    arrive = A("e3", "20,000")
    keys = [(0, (1.7, 340, 800)), (A("e1", "Australia"), (2.1, 260, 800)), (A("e1", "war"), (1.9, 380, 800)),
            (A("e1", "birds"), (1.3, 400, 720)), (A("e1", "won"), (1.9, 470, 760)), (A("e2"), (1.4, 200, 700)),
            (A("e2", "Western"), (1.1, 300, 700)), (A("e2", "ex-soldiers"), (2.0, 260, 700)),
            (A("e2", "wheat"), (1.5, 380, 780)), (A("e3"), (1.2, 380, 760)), (A("e3", "around"), (1.6, 300, 800)),
            (arrive, (1.0, 380, 740)), (A("e3", "showed"), (1.4, 470, 860)), (A("e3", "eating"), (1.8, 420, 820))]
    z, fx, fy = camera(t, keys)
    set_camera((z, fx, fy))
    enter_world(cr)
    eaten = 0.7 * seg(t, A("e3", "eating"), A("e3", end=True))
    field_set(cr, t, eaten)
    # the farmer
    worried = t >= arrive
    person(cr, "farmer", 220, 880, t, facing=1, arms=("face", "face") if worried else ("hip", "hip"),
           eyes="wide" if worried else "happy", mouth="o" if worried else "smile", shake=1.0 if worried else 0)
    # in the hook, and when they arrive: a mob of emus
    show = t < A("e2") or t >= arrive
    if show:
        n = 3 if t < A("e2") else 7
        for i in range(n):
            ex = 460 + (i % 4) * 130 - (1 - ease_out(seg(t, arrive, arrive + 0.8))) * 700 * (t >= arrive)
            ey = 900 + (i // 4) * 110
            eating = t >= A("e3", "eating")
            emu(cr, ex, ey, t, s=0.55 + 0.05 * (i % 3), facing=-1, run=None if eating else t * 2 + i,
                peck=abs(math.sin(t * 5 + i)) if eating else 0, eye="smug" if t < A("e2") else "normal", seed=i * 7)
    hl(cr, t, [("1932", RED)], 215, 96, A("e1", "1932"), end=A("e1", "birds") - 0.05, bold=True)
    hl(cr, t, [("Army ", INK), ("vs ", RED), ("BIRDS", GOLD)], 215, 74, A("e1", "birds"), end=A("e2") - 0.05, bold=True)
    hl(cr, t, [("wheat ", GOLD), ("farmers", INK)], 215, 66, A("e2", "wheat"), end=A("e3") - 0.05, bold=True)
    hl(cr, t, [("20,000", RED), (" emus", INK)], 215, 80, arrive, bold=True, underline=True)


def scene_army(cr, t, tl):
    A = tl.at
    keys = [(A("e4") - 0.2, (1.2, 380, 760)), (A("e4", "government"), (1.5, 500, 800)),
            (A("e4", "army"), (1.3, 420, 760)), (A("e4", "3"), (1.7, 330, 780)), (A("e4", "2"), (1.8, 470, 740)),
            (A("e4", "10,000"), (1.4, 400, 760))]
    z, fx, fy = camera(t, keys)
    set_camera((z, fx, fy))
    enter_world(cr)
    field_set(cr, t, 0.7)
    tx = lerp(950, 420, ease_out(seg(t, A("e4"), A("e4") + 1.0)))
    cue("engine", t, A("e4"), 1.0)
    # soldiers + guns on the truck bed
    for i, sx in enumerate((-20, 60, 140)):
        if t >= A("e4", "3") + i * 0.12:
            person(cr, "soldier", tx + sx + 30, 814, t, facing=1, arms=("hip", "down"), mouth="flat", scale=0.62)
    for i, gx in enumerate((10, 150)):
        if t >= A("e4", "2") + i * 0.12:
            lewis_gun(cr, tx + gx + 30, 800, s=0.55, facing=1, seed=i * 9)
    truck(cr, tx, 900, t, wheel=tx / 28, facing=-1, color=ARMY)
    # bullets pile / counter
    if t >= A("e4", "10,000"):
        for k in range(18):
            bx, by = 170 + (k % 6) * 14, 1030 - (k // 6) * 12
            shape(cr, rrect_pts(bx, by - 18, 8, 18, 3, 8), hexc("#d9a15a"), seed=2200 + k, amp=0.2, lw=2)
    hl(cr, t, [("3", RED), (" soldiers", INK)], 195, 60, A("e4", "3"), bold=True)
    hl(cr, t, [("2", RED), (" machine guns", INK)], 265, 60, A("e4", "2"), bold=True)
    hl(cr, t, [("10,000", RED), (" bullets", INK)], 335, 60, A("e4", "10,000"), bold=True)


def scene_battle(cr, t, tl):
    A = tl.at
    nope = A("e5", "Nope")
    keys = [(A("e5") - 0.2, (1.6, 300, 800)), (A("e5", "right"), (2.0, 200, 780)), (nope, (1.2, 420, 780)),
            (A("e6", "split"), (1.6, 540, 940)), (A("e6", "scattered"), (1.0, 380, 760)),
            (A("e6", "missed"), (1.8, 250, 820)), (A("e6", "eating"), (1.5, 520, 850)),
            (A("e6", "newspapers"), (1.2, 380, 760))]
    z, fx, fy = camera(t, keys)
    set_camera((z, fx, fy))
    enter_world(cr)
    field_set(cr, t, 0.8)
    firing = A("e6", "missed") - 0.3 <= t < A("e6", "eating")
    person(cr, "soldier", 140, 900, t, facing=1, arms=("give", "hold"), mouth="o" if firing else "flat",
           eyes="wide" if t >= nope else "sly", sweat=t >= nope)
    rec = abs(math.sin(t * 40)) if firing else 0
    lewis_gun(cr, 250, 900, s=0.8, facing=1, recoil=rec)
    if firing and int(t * 20) % 2:
        blob(cr, 385, 822, 16, 10, hexc("#ffd23f"), seed=2300, amp=1.5, lw=2.5)
    # emus scattering in small groups
    scatter = ease_out(seg(t, A("e6", "split"), A("e6", "scattered") + 0.4))
    groups = [(520, 900, -1), (620, 1060, 1), (430, 1120, 1)]
    for gi, (gx, gy, d) in enumerate(groups):
        for j in range(2):
            ex = gx + j * 70 + scatter * d * 160 + math.sin(t * 3 + gi) * 30
            ey = gy + j * 30 - scatter * 60 * (gi == 0)
            eating = t >= A("e6", "eating")
            emu(cr, ex, ey, t, s=0.5, facing=d if t >= A("e6", "split") else -1,
                run=None if eating else t * 2.5 + gi + j, peck=abs(math.sin(t * 5 + gi + j)) if eating else 0,
                seed=gi * 5 + j)
    if firing:
        for k in range(3):
            sc = pop(t, A("e6", "missed") + k * 0.25, 0.2)
            if sc > 0:
                with at(cr, 480 + k * 100, 700 - k * 30, sc, rot=0.2 * (k - 1)):
                    write(cr, [("MISS!", RED)], 0, 0, 40, align="center", bold=True)
    # the newspaper
    ns = pop(t, A("e6", "newspapers"), 0.3)
    if ns > 0:
        cr.save()
        cr.identity_matrix()
        with at(cr, 360, 560, ns, rot=-0.08):
            shape(cr, rrect_pts(-230, -150, 460, 300, 8, 24), hexc("#f4efe1"), seed=2400, amp=0.8, lw=4)
            write(cr, [("THE WHEATBELT TIMES", INK)], 0, -105, 26, align="center", bold=True)
            line(cr, [(-200, -92), (200, -92)], 3, INK, seed=2401, amp=0.3)
            write(cr, [("ARMY OUTRUN", RED)], 0, -40, 50, align="center", bold=True)
            write(cr, [("BY BIRDS", RED)], 0, 12, 50, align="center", bold=True)
            for k in range(4):
                line(cr, [(-200, 50 + k * 22), (200 - (k % 2) * 60, 50 + k * 22)], 3, hexc("#b9ad96"), seed=2402 + k,
                     amp=0.5)
        cr.restore()
        cue("pop", t, A("e6", "newspapers"))
    hl(cr, t, [("Nope.", RED)], 215, 90, nope, end=A("e6") - 0.05, bold=True)
    hl(cr, t, [("tiny ", INK), ("groups", RED)], 215, 66, A("e6", "groups"), end=A("e6", "newspapers") - 0.05, bold=True)


def scene_tank(cr, t, tl):
    A = tl.at
    keys = [(A("e7") - 0.2, (1.3, 330, 780)), (A("e7", "commander"), (1.8, 230, 760)),
            (A("e7", "emus"), (1.6, 400, 840)), (A("e7", "tanks"), (1.7, 420, 840))]
    z, fx, fy = camera(t, keys)
    set_camera((z, fx, fy))
    enter_world(cr)
    field_set(cr, t, 0.9)
    person(cr, "soldier", 220, 900, t, facing=1, arms=("chin", "hip"), eyes="sad", mouth="wobble", sweat=True)
    # an emu in a sketched tank
    tk = pop(t, A("e7", "tanks"), 0.3)
    emu(cr, 430, 930, t, s=0.62, facing=-1, eye="smug", seed=3)
    if tk > 0:
        with at(cr, 430, 940, tk):
            shape(cr, rrect_pts(-150, -120, 300, 110, 30, 24), hexc("#6b7a3a", 0.92), seed=2500, amp=1, lw=4)
            for k in range(5):
                blob(cr, -120 + k * 60, -20, 22, 22, hexc("#3a3140"), seed=2501 + k, amp=0.4, lw=3)
            line(cr, [(-40, -150), (-160, -160)], 12, INK, seed=2510, amp=0.3)
    hl(cr, t, [("\"like ", INK), ("TANKS", RED), ("\"", INK)], 215, 80, A("e7", "tanks"), bold=True, underline=True)
    hl(cr, t, [("the commander:", INK)], 215, 58, A("e7", "commander"), end=A("e7", "tanks") - 0.05, bold=True)


def scene_retreat(cr, t, tl):
    A = tl.at
    out = A("e8", "pulled")
    keys = [(A("e8") - 0.2, (1.3, 380, 760)), (A("e8", "9,860"), (1.6, 380, 800)), (out, (1.1, 300, 760)),
            (A("e9"), (1.6, 220, 780)), (A("e9", "three"), (1.3, 420, 740)), (A("e9", "answer"), (1.7, 300, 760)),
            (A("e9", "always"), (1.9, 240, 760)), (A("e10"), (1.2, 420, 780)),
            (A("e10", "won"), (1.6, 470, 800))]
    z, fx, fy = camera(t, keys)
    set_camera((z, fx, fy))
    enter_world(cr)
    field_set(cr, t, 0.95)
    tx = lerp(420, -520, ease_in(seg(t, out, out + 1.2)))
    cue("engine", t, out, 1.2)
    truck(cr, tx, 900, t, wheel=tx / 28, facing=-1, color=ARMY)
    if tx > -400:
        for i, sx in enumerate((-20, 60, 140)):
            person(cr, "soldier", tx + sx + 30, 814, t, facing=1, arms=("down", "down"), mouth="sad", eyes="sad",
                   scale=0.62)
    if t >= A("e9"):
        person(cr, "farmer", 200, 900, t, facing=1, arms=("point", "hip"), eyes="sad", mouth="o")
        for k in range(3):   # three refused requests
            sc = pop(t, A("e9", "three") + k * 0.18, 0.2)
            if sc > 0:
                with at(cr, 360 + k * 90, 700, sc, rot=-0.15):
                    shape(cr, rrect_pts(-40, -28, 80, 56, 6, 12), hexc("#f4efe1"), seed=2600 + k, amp=0.5, lw=3)
                    write(cr, [("NO", RED)], 0, 12, 32, align="center", bold=True)
    party = t >= A("e10")
    for i in range(5):
        emu(cr, 440 + (i % 3) * 120, 960 + (i // 3) * 120, t, s=0.55, facing=-1, eye="smug",
            peck=0 if party else abs(math.sin(t * 5 + i)), seed=i * 3)
    if party:
        confetti(cr, t, A("e10", "won"))
    hl(cr, t, [("9,860", RED), (" more bullets", INK)], 215, 64, A("e8", "9,860"), end=A("e9") - 0.05, bold=True)
    hl(cr, t, [("asked ", INK), ("3x", RED), (": ", INK), ("NO", RED)], 215, 70, A("e9", "always"), end=A("e10") - 0.05,
       bold=True)
    hl(cr, t, [("EMUS ", GOLD), ("1", RED), (" - ARMY ", INK), ("0", RED)], 215, 70, A("e10", "won"), bold=True,
       underline=True)
    cue("kaching", t, A("e10", "won"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"field": scene_field, "army": scene_army, "battle": scene_battle, "tank": scene_tank,
     "retreat": scene_retreat}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
