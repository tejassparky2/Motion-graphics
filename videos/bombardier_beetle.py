"""Episode 12: "The Beetle With a Cannon in Its Butt" — the bombardier beetle.

Facts:
- Wikipedia, "Bombardier beetle": hydroquinones + hydrogen peroxide are stored in a reservoir and flow into a
  reaction chamber with catalases and peroxidases. The heat brings the spray to near 100 °C, released in pulses at
  about 500 pulses per second. Some species can swivel the tip and aim.
- Sugiura & Sato (2018), Biology Letters 14: 20170647, "Successful escape of bombardier beetles from predator
  digestive systems": toads (Bufo japonicus, B. torrenticola) swallowed Pheropsophus jessoensis. 43% of toads vomited
  the beetles 12-107 minutes later, and all of the vomited beetles were alive and active.
"""
import math

from motion.captions import captions
from motion.critters import ant
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, smooth, write)
from motion.kit import camera, confetti, enter_world, fly, hl, set_camera, stamp, whip

NARRATOR = dict(speed=1.05)
TAIL = 0.8

SCRIPT = [
    dict(id="e1", scene="garden", text="This beetle has a weapon no predator expects. A boiling hot cannon, in its butt."),
    dict(id="e2", scene="garden",
         text="Meet the bombardier beetle. When an ant attacks, it doesn't run. It spins around, and fires."),
    dict(id="e3", scene="inside",
         text="Inside its body, it keeps its chemicals in one chamber. When it's attacked, they rush into a second "
              "chamber full of enzymes, and explode."),
    dict(id="e4", scene="inside", text="The spray hits nearly [one hundred degrees Celsius.|100 °C.] Boiling hot."),
    dict(id="e5", scene="pulses", text="And it fires in pulses, about [five hundred a second.|500 a second.] "
                                       "Like a tiny machine gun."),
    dict(id="e6", scene="toad", text="But here's the crazy part. Scientists in Japan fed these beetles to toads.",
         gap=0.2),
    dict(id="e7", scene="toad", text="The toads swallowed them whole, and the beetles fired, from inside the toad."),
    dict(id="e8", scene="toad2",
         text="[Forty-three percent|43%] of the toads threw them back up, some after almost [two hours.|2 hours.] "
              "And every beetle that came out, was alive."),
    dict(id="e9", scene="end", text="So next time you have a bad day, remember: this beetle got eaten, and walked it off.",
         gap=0.2),
]

METADATA = dict(
    title="This Beetle Has a Boiling Cannon in Its Butt 🪲🔥",
    alt_titles=["The Beetle That Survives Being EATEN 🐸🪲", "It Got Swallowed by a Toad… Then Fired 🔥"],
    description="""The bombardier beetle has a weapon no predator expects: a boiling-hot chemical cannon in its butt. 🪲🔥

It mixes chemicals with enzymes in a special chamber, and the spray hits nearly 100 °C, fired in pulses about 500 times a second.

And in a 2018 study, scientists in Japan found that when toads swallowed these beetles, the beetles fired from INSIDE. 43% of the toads threw them back up (some after almost 2 hours), and every beetle that came out was alive. 🐸

Source: Sugiura & Sato, Biology Letters (2018).

💬 Which animal has the weirdest defense you know? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Animals", "#Insects", "#Nature"],
    tags=["bombardier beetle", "weird insects", "animal facts", "insect facts", "beetle", "toad", "nature facts",
          "weird animals", "animal defense", "interestingly strange"],
    pinned_comment="Imagine being the toad in this story 😂🐸 Would you eat this beetle? 👇",
)

ORANGE = hexc("#f28c28")
YELLOW = hexc("#f7d774")
GREEN = hexc("#3d8f45")
TOAD = hexc("#8a9a4a")
TOAD_D = hexc("#6b7a36")
BLUE = hexc("#3f6fb5")
PURPLE = hexc("#6a45b5")
HOT = hexc("#ff6b2b")


# ------------------------------------------------------------------ critters
def beetle(cr, x, y, t, s=1.0, facing=1, walk=None, fire=0.0, eye="normal", shades=False, seed=0):
    """Bombardier beetle, side view, ground at y. `fire` 0..1 draws the spray out of the back end."""
    with at(cr, x, y, s, flip=facing < 0):
        ph = walk * 2 * math.pi if walk is not None else 0.0
        for k, lx in enumerate((-40, 0, 40)):   # legs
            sw = math.sin(ph + k * 2.1) * 10 if walk is not None else 0
            line(cr, [(lx, -34), (lx - 14 + sw, -14), (lx - 6 + sw, 0)], 5, INK, seed=seed + k, amp=0.3)
        # abdomen / wing cases: dark with yellow stripes
        shape(cr, [(-90, -40), (-70, -76), (0, -90), (40, -70), (40, -34), (-80, -28)], hexc("#1f2a3d"), seed=seed + 5,
              amp=0.6, lw=4)
        for k in range(3):
            line(cr, [(-70 + k * 30, -72 + k * 4), (-60 + k * 30, -38)], 6, YELLOW, seed=seed + 6 + k, amp=0.4)
        # thorax + head (orange)
        blob(cr, 56, -56, 26, 24, ORANGE, seed=seed + 10, amp=0.5, lw=4)
        blob(cr, 92, -58, 22, 20, ORANGE, seed=seed + 11, amp=0.5, lw=4)
        line(cr, [(104, -72), (126, -104), (140, -108)], 3.5, INK, seed=seed + 12, amp=0.4)   # antennae
        line(cr, [(110, -66), (140, -84), (154, -84)], 3.5, INK, seed=seed + 13, amp=0.4)
        if shades:
            shape(cr, rrect_pts(88, -72, 36, 14, 4, 8), INK, seed=seed + 14, amp=0.3, lw=2)
        elif eye == "x":
            line(cr, [(96, -70), (108, -58)], 3, INK, seed=seed + 15, amp=0.1)
            line(cr, [(108, -70), (96, -58)], 3, INK, seed=seed + 16, amp=0.1)
        else:
            blob(cr, 102, -64, 9, 10, WHITE, seed=seed + 15, amp=0.2, lw=2.5)
            dot(cr, 104 + (2 if eye == "normal" else 0), -63, 4.5 if eye != "wide" else 3, INK)
        line(cr, [(96, -48), (106, -46)], 3, INK, seed=seed + 17, amp=0.2)
        # the nozzle + spray
        blob(cr, -92, -46, 8, 8, ORANGE, seed=seed + 18, amp=0.3, lw=3)
        if fire > 0:
            reach = 60 + 200 * fire
            for k in range(7):
                u = ((t * 9 + k / 7) % 1)
                px = -96 - u * reach
                py = -46 - math.sin(u * math.pi) * 10 + (k - 3) * 6 * u
                blob(cr, px, py, 10 + 22 * u, 8 + 18 * u, hexc("#fff3c4" if k % 2 else "#ffd23f", 0.9 * (1 - u) + 0.1),
                     seed=seed + 20 + k, amp=1.2, lw=2.5, stroke=hexc("#e8a93b", 1 - u))


def toad(cr, x, y, t, s=1.0, facing=1, mouth="closed", sick=0.0, bulge=0.0, jolt=0.0, seed=0):
    col = TOAD if sick <= 0 else hexc("#9ab04a")
    with at(cr, x, y - jolt * 30, s, flip=facing < 0):
        for k, lx in enumerate((-90, 60)):   # legs
            blob(cr, lx, -22, 50, 26, TOAD_D, seed=seed + k, amp=0.8, lw=4)
        shape(cr, [(-130, -30), (-120, -120), (-40, -170), (60, -170), (130, -120), (140, -40), (100, -10), (-100, -10)],
              col, seed=seed + 3, amp=1.2, lw=4.5)
        for k in range(9):   # warts
            dot(cr, -100 + (k * 47) % 200, -60 - (k * 31) % 90, 6, TOAD_D)
        blob(cr, 0, -40 - bulge * 10, 70 + bulge * 30, 30 + bulge * 24, hexc("#e8dca0"), seed=seed + 4, amp=0.8, lw=3)
        for ex in (40, 100):   # eyes
            blob(cr, ex, -170, 26, 26, col, seed=seed + 5 + ex, amp=0.5, lw=4)
            blob(cr, ex, -172, 16, 16, hexc("#f7d774"), seed=seed + 6 + ex, amp=0.3, lw=2.5)
            if sick > 0.5:
                line(cr, [(ex - 8, -180), (ex + 8, -164)], 3, INK, seed=seed + 7 + ex, amp=0.1)
                line(cr, [(ex + 8, -180), (ex - 8, -164)], 3, INK, seed=seed + 8 + ex, amp=0.1)
            else:
                dot(cr, ex + 4, -172, 7, INK)
        if mouth == "open":
            shape(cr, [(60, -110), (150, -100), (148, -60), (70, -70)], hexc("#7a1f1f"), seed=seed + 9, amp=0.5, lw=4)
            blob(cr, 110, -80, 22, 12, hexc("#e0487a"), seed=seed + 10, amp=0.4, lw=2.5)
        elif mouth == "puke":
            shape(cr, [(70, -104), (150, -110), (146, -58), (80, -66)], hexc("#7a1f1f"), seed=seed + 9, amp=0.6, lw=4)
        else:
            line(cr, [(40, -96), (100, -90), (140, -98)], 4.5, INK, seed=seed + 11, amp=0.4)


def garden(cr, t):
    cr.set_source_rgba(*hexc("#bfe6c8"))
    cr.paint()
    blob(cr, 620, 300, 60, 60, hexc("#ffe28a"), seed=9000, amp=0.5, lw=3)
    for k in range(-4, 12):   # far bushes
        blob(cr, k * 110, 720, 90, 70, hexc("#8cc47a"), seed=9001 + k, amp=1.4, lw=3)
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#b88a58"), seed=9020, amp=1, lw=4)
    for k in range(-20, 50):   # grass blades
        x = k * 30
        h = 40 + (k * 17) % 50
        line(cr, [(x, 905), (x + 8 * math.sin(t * 2 + k), 905 - h)], 4, GREEN, seed=9030 + k, amp=0.4)
    for k in range(6):   # pebbles
        blob(cr, -200 + k * 190, 960 + (k % 2) * 40, 26, 16, hexc("#a9a2ae"), seed=9100 + k, amp=0.6, lw=3)


# ------------------------------------------------------------------ scenes
def scene_garden(cr, t, tl):
    A = tl.at
    spin = seg(t, A("e2", "spins"), A("e2", "around", end=True))
    firing = t >= A("e2", "fires")
    keys = [(0, (1.8, 360, 820)), (A("e1", "weapon"), (1.2, 360, 800)), (A("e1", "predator"), (2.4, 470, 800)),
            (A("e1", "expects"), (1.0, 380, 790)), (A("e1", "boiling"), (2.2, 330, 820)), (A("e1", "hot"), (1.5, 300, 810)),
            (A("e1", "butt"), (2.6, 260, 830)), (A("e2", "meet"), (1.4, 380, 800)), (A("e2", "bombardier"), (2.0, 420, 800)),
            (A("e2", "ant"), (1.4, 200, 820)), (A("e2", "run"), (1.8, 330, 820)), (A("e2", "spins"), (1.5, 330, 800)),
            (A("e2", "fires"), (1.0, 280, 780))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    garden(cr, t)
    # hook: a glimpse of the cannon firing, then the meet-and-greet
    hook_fire = A("e1", "cannon") <= t < A("e2")
    facing = 1 if spin < 0.5 else -1
    bx = 380
    beetle(cr, bx, 905, t, 1.2, facing=facing, fire=1.0 if hook_fire or firing else 0.0,
           eye="wide" if A("e2", "ant") <= t < A("e2", "spins") else "normal", seed=9200)
    if hook_fire or firing:
        cue("hit", t, A("e1", "cannon") if hook_fire else A("e2", "fires"))
    # the ant
    if t >= A("e2", "ant"):
        if not firing:
            ax = lerp(-80, 180, ease_out(seg(t, A("e2", "ant"), A("e2", "attacks", end=True))))
            ant(cr, ax, 905, t, 1.0, facing=1, walk=t * 3, seed=9300)
        else:
            u = seg(t, A("e2", "fires"), A("e2", "fires") + 0.7)   # blasted away, spinning
            with at(cr, lerp(180, -160, u), 905 - math.sin(u * math.pi) * 260, 1.0, rot=u * 9):
                ant(cr, 0, 0, t, 1.0, facing=1, seed=9300, eye="spiral")
    hl(cr, t, [("a ", INK), ("WEAPON", RED)], 215, 90, A("e1", "weapon"), end=A("e1", "boiling") - 0.05, bold=True)
    hl(cr, t, [("BOILING", HOT), (" butt cannon", INK)], 215, 70, A("e1", "boiling"), end=A("e2") - 0.05, bold=True)
    hl(cr, t, [("bombardier", ORANGE), (" beetle", INK)], 215, 80, A("e2", "bombardier"), end=A("e2", "ant") - 0.05,
       bold=True)
    hl(cr, t, [("ant ", INK), ("attacks!", RED)], 215, 84, A("e2", "ant"), end=A("e2", "spins") - 0.05, bold=True)
    hl(cr, t, [("FIRE!", HOT)], 215, 110, A("e2", "fires"), bold=True)


def scene_inside(cr, t, tl):
    """X-ray: reservoir → enzyme chamber → boom, and a thermometer to 100 °C."""
    A = tl.at
    keys = [(A("e3") - 0.2, (0.9, 420, 560)), (A("e3", "chemicals"), (1.7, 460, 540)), (A("e3", "attacked"), (1.0, 420, 560)),
            (A("e3", "rush"), (1.9, 340, 540)), (A("e3", "second"), (1.2, 300, 560)), (A("e3", "enzymes"), (2.0, 235, 530)), (A("e3", "explode"), (1.25, 260, 540)), (A("e4", "spray"), (0.9, 420, 560)),
            (A("e4", "nearly"), (1.3, 600, 560)), (A("e4", "100"), (1.6, 720, 560)), (A("e4", "boiling"), (0.95, 420, 560)),
            (A("e4", "hot"), (1.4, 300, 540))]
    z, fx, fy = camera(t, keys, dur=0.15)
    cr.set_source_rgba(*hexc("#1d2b45"))
    cr.paint()
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    for k in range(-10, 30):   # blueprint grid
        line(cr, [(k * 60, -400), (k * 60, 1800)], 1.5, hexc("#2f4368"), seed=9400 + k, amp=0.2)
        line(cr, [(-600, k * 60), (1400, k * 60)], 1.5, hexc("#2f4368"), seed=9450 + k, amp=0.2)
    # the beetle's outline
    shape(cr, [(80, 520), (200, 440), (560, 430), (680, 520), (560, 610), (200, 620)], hexc("#2a3a5c"), seed=9500,
          amp=0.8, lw=5, stroke=hexc("#9fd3f0"))
    write(cr, [("head", hexc("#9fd3f0"))], 640, 420, 30, align="center", bold=True)
    # reservoir (chemicals)
    fill = 1 - 0.6 * seg(t, A("e3", "rush"), A("e3", "rush") + 0.5)
    shape(cr, rrect_pts(380, 470, 160, 110, 30, 18), None, seed=9510, amp=0.6, lw=4, stroke=hexc("#9fd3f0"))
    cr.save()
    cr.rectangle(380, 470 + 110 * (1 - fill), 160, 110 * fill)
    cr.clip()
    shape(cr, rrect_pts(382, 472, 156, 106, 28, 18), hexc("#4fb3e8"), seed=9511, amp=0.5, lw=0, stroke=None)
    cr.restore()
    write(cr, [("chemicals", WHITE)], 460, 540, 30, align="center", bold=True)
    # enzyme chamber
    boom = seg(t, A("e3", "explode"), A("e3", "explode") + 0.25)
    shape(cr, rrect_pts(170, 480, 130, 90, 26, 16), hexc("#f28c28", 0.4 + 0.6 * boom), seed=9520, amp=0.8 + boom * 2,
          lw=4, stroke=hexc("#ffd23f"))
    write(cr, [("enzymes", WHITE)], 235, 534, 26, align="center", bold=True)
    if t >= A("e3", "rush"):   # the flow between them
        for k in range(5):
            u = (t * 2 + k / 5) % 1
            dot(cr, lerp(380, 300, u), 525 + math.sin(u * 8) * 8, 7, hexc("#4fb3e8"))
    if t >= A("e3", "explode"):
        for k in range(8):
            u = (t * 3 + k / 8) % 1
            blob(cr, 150 - u * 260, 525 + (k - 4) * 8 * u, 14 + 26 * u, 12 + 20 * u, hexc("#ffd23f", 1 - u), seed=9530 + k,
                 amp=1.3, lw=2, stroke=hexc("#ff6b2b", 1 - u))
        sc = pop(t, A("e3", "explode"), 0.2)
        if sc > 0 and t < A("e4"):
            with at(cr, 120, 400, sc, rot=-0.15):
                blob(cr, 0, 0, 110, 70, hexc("#ffd23f"), seed=9540, amp=3.0, lw=4)
                write(cr, [("BOOM!", RED)], 0, 18, 56, align="center", bold=True)
        cue("hit", t, A("e3", "explode"))
    # thermometer
    temp = seg(t, A("e4", "spray"), A("e4", "100", end=True))
    shape(cr, rrect_pts(760, 300, 50, 300, 24, 16), WHITE, seed=9550, amp=0.5, lw=4)
    blob(cr, 785, 610, 40, 40, HOT, seed=9551, amp=0.4, lw=4)
    shape(cr, rrect_pts(773, 590 - 280 * temp, 24, 280 * temp + 10, 10, 12), HOT, seed=9552, amp=0.3, lw=0, stroke=None)
    write(cr, [(f"{int(20 + 80 * temp)}°C", HOT if temp > 0.9 else WHITE)], 785, 270, 60, align="center", bold=True)
    hl(cr, t, [("chamber ", INK), ("1", BLUE)], 215, 84, A("e3", "chemicals"), end=A("e3", "second") - 0.05, bold=True)
    hl(cr, t, [("chamber ", INK), ("2", ORANGE), (": enzymes", INK)], 215, 70, A("e3", "second"),
       end=A("e3", "explode") - 0.05, bold=True)
    hl(cr, t, [("EXPLODE", RED)], 215, 96, A("e3", "explode"), end=A("e4") - 0.05, bold=True)
    hl(cr, t, [("~100 °C", HOT)], 215, 110, A("e4", "100"), bold=True, underline=True)


def scene_pulses(cr, t, tl):
    A = tl.at
    keys = [(A("e5") - 0.2, (1.3, 360, 800)), (A("e5", "fires"), (1.0, 380, 780)), (A("e5", "pulses"), (2.0, 250, 820)),
            (A("e5", "about"), (1.3, 400, 790)), (A("e5", "500"), (1.1, 360, 780)), (A("e5", "second"), (1.6, 470, 800)),
            (A("e5", "tiny"), (1.1, 330, 790)), (A("e5", "machine"), (1.8, 200, 800))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    garden(cr, t)
    beetle(cr, 480, 905, t, 1.4, facing=1, fire=0.6 + 0.4 * (int(t * 16) % 2), eye="happy", seed=9600)
    for k in range(10):   # rapid-fire puffs down range
        u = (t * 4 + k / 10) % 1
        blob(cr, 320 - u * 520, 840 - (k % 3) * 20, 12, 10, hexc("#ffd23f", 1 - u), seed=9610 + k, amp=0.8, lw=2)
    if t >= A("e5", "500"):
        count = int(500 * seg(t, A("e5", "500"), A("e5", "500", end=True)))
        cr.save()
        cr.identity_matrix()
        with at(cr, 360, 480, pop(t, A("e5", "500"), 0.2) or 0.01, rot=-0.05):
            shape(cr, rrect_pts(-200, -80, 400, 150, 20, 20), INK, seed=9620, amp=0.8, lw=0, stroke=None)
            write(cr, [(f"{count}", YELLOW)], -30, 34, 100, align="center", bold=True)
            write(cr, [("/sec", WHITE)], 120, 34, 48, align="center", bold=True)
        cr.restore()
    if t >= A("e5", "machine") and int(t * 8) % 2:
        write(cr, [("PEW PEW PEW", RED)], 180, 700, 44, align="center", bold=True, halo=WHITE)
    hl(cr, t, [("in ", INK), ("PULSES", ORANGE)], 215, 90, A("e5", "pulses"), end=A("e5", "500") - 0.05, bold=True)
    hl(cr, t, [("tiny ", INK), ("machine gun", RED)], 215, 80, A("e5", "machine"), bold=True)


def lab_bg(cr, t):
    cr.set_source_rgba(*hexc("#e8eef2"))
    cr.paint()
    for k in range(-6, 16):   # tiles
        line(cr, [(k * 90, 250), (k * 90, 900)], 2, hexc("#d5dde3"), seed=9700 + k, amp=0.3)
        line(cr, [(-600, 250 + k * 90), (1400, 250 + k * 90)], 2, hexc("#d5dde3"), seed=9720 + k, amp=0.3)
    shape(cr, rrect_pts(-200, 900, 1100, 60, 6, 18), hexc("#a9a2ae"), seed=9740, amp=0.6, lw=4)
    shape(cr, rrect_pts(380, 380, 260, 90, 10, 16), WHITE, seed=9741, amp=0.5, lw=3.5)
    write(cr, [("LAB", RED)], 510, 424, 40, align="center", bold=True)
    write(cr, [("JAPAN", INK)], 510, 460, 26, align="center", bold=True)


def scene_toad(cr, t, tl, part):
    A = tl.at
    if part == 1:
        keys = [(A("e6") - 0.2, (1.2, 360, 760)), (A("e6", "crazy"), (1.7, 360, 720)), (A("e6", "Japan"), (1.3, 510, 560)),
                (A("e6", "toads"), (1.2, 330, 780)), (A("e7", "swallowed"), (1.8, 380, 740)),
                (A("e7", "beetles"), (1.3, 330, 780)), (A("e7", "fired"), (1.9, 300, 780)), (A("e7", "inside"), (1.4, 320, 760))]
    else:
        keys = [(A("e8") - 0.2, (1.2, 330, 760)), (A("e8", "43%"), (1.0, 360, 700)), (A("e8", "back"), (1.8, 420, 740)),
                (A("e8", "almost"), (1.2, 400, 700)), (A("e8", "every"), (1.5, 560, 820)), (A("e8", "alive"), (2.0, 600, 840))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    lab_bg(cr, t)
    tx, ty = 300, 900
    if part == 1:
        swallow = A("e7", "swallowed")
        eaten = t >= swallow + 0.3
        pops = t >= A("e7", "fired")
        jolt = abs(math.sin(t * 20)) if pops else 0
        toad(cr, tx, ty, t, 1.2, mouth="open" if swallow <= t < swallow + 0.3 else "closed", bulge=0.6 if eaten else 0,
             jolt=jolt * 0.5, seed=9800)
        if not eaten:   # the beetle dropped in
            if t < swallow:
                beetle(cr, 560, 905, t, 0.7, facing=-1, eye="normal", seed=9810)
            else:
                u = seg(t, swallow, swallow + 0.3)
                beetle(cr, lerp(560, 440, u), 905 - math.sin(u * math.pi) * 120, t, 0.7, facing=-1, seed=9810)
        if pops:   # BANG inside the belly
            for k in range(3):
                sc = pop(t, A("e7", "fired") + k * 0.3, 0.15) * (1 - seg(t, A("e7", "fired") + k * 0.3 + 0.2,
                                                                         A("e7", "fired") + k * 0.3 + 0.35))
                if sc > 0:
                    with at(cr, tx - 20 + k * 30, ty - 90, sc):
                        blob(cr, 0, 0, 60, 40, hexc("#ffd23f"), seed=9820 + k, amp=2.0, lw=3.5)
                        write(cr, [("POP", RED)], 0, 12, 36, align="center", bold=True)
                    cue("hit", t, A("e7", "fired") + k * 0.3)
        hl(cr, t, [("scientists in ", INK), ("Japan", RED)], 215, 70, A("e6", "Japan"), end=A("e6", "toads") - 0.05,
           bold=True)
        hl(cr, t, [("fed them to ", INK), ("TOADS", GREEN)], 215, 76, A("e6", "toads"), end=A("e7") - 0.05, bold=True)
        hl(cr, t, [("swallowed ", INK), ("whole", RED)], 215, 80, A("e7", "swallowed"), end=A("e7", "fired") - 0.05,
           bold=True)
        hl(cr, t, [("fired from ", INK), ("INSIDE", HOT)], 215, 76, A("e7", "fired"), bold=True)
    else:
        puke = A("e8", "threw")
        u = seg(t, puke, puke + 0.6)
        toad(cr, tx, ty, t, 1.2, mouth="puke" if puke <= t < puke + 0.5 else "closed", sick=1.0 if t < puke + 1.2 else 0.3,
             bulge=0.6 if t < puke else 0, seed=9800)
        if t >= puke:
            if u < 1:
                beetle(cr, lerp(430, 600, u), 900 - math.sin(u * math.pi) * 240, t, 0.7, facing=1, seed=9810)
            else:
                walk = seg(t, A("e8", "every"), A("e8", "alive", end=True) + 0.4)
                beetle(cr, lerp(600, 680, walk), 905, t, 0.8, facing=1, walk=t * 3 if 0 < walk < 1 else None,
                       eye="happy" if t >= A("e8", "alive") else "wide", seed=9810)
            cue("whoosh", t, puke, 0.3)
        # 43% pie + timer
        if t >= A("e8", "43%"):
            cr.save()
            cr.identity_matrix()
            with at(cr, 180, 480, 1.35 * (pop(t, A("e8", "43%"), 0.2) or 0.01)):
                blob(cr, 0, 0, 90, 90, WHITE, seed=9830, amp=0.5, lw=4)
                cr.move_to(0, 0)
                cr.arc(0, 0, 84, -math.pi / 2, -math.pi / 2 + 2 * math.pi * 0.43)
                cr.close_path()
                cr.set_source_rgba(*GREEN)
                cr.fill()
                write(cr, [("43%", INK)], 0, 130, 52, align="center", bold=True, halo=WHITE)
            if t >= A("e8", "almost"):
                with at(cr, 530, 480, 1.3 * (pop(t, A("e8", "almost"), 0.2) or 0.01), rot=0.05):
                    shape(cr, rrect_pts(-130, -70, 260, 140, 16, 18), INK, seed=9840, amp=0.6, lw=0, stroke=None)
                    write(cr, [("up to", WHITE)], 0, -20, 30, align="center", bold=True)
                    write(cr, [("107 min", YELLOW)], 0, 40, 56, align="center", bold=True)
            cr.restore()
        hl(cr, t, [("threw them ", INK), ("UP", GREEN)], 215, 84, A("e8", "threw"), end=A("e8", "every") - 0.05, bold=True)
        hl(cr, t, [("ALL ", INK), ("ALIVE", GREEN)], 215, 96, A("e8", "alive"), bold=True, underline=True)
        if t >= A("e8", "alive"):
            cue("kaching", t, A("e8", "alive"))


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("e9") - 0.2, (1.3, 360, 800)), (A("e9", "bad"), (1.8, 200, 780)), (A("e9", "remember"), (1.2, 360, 800)),
            (A("e9", "eaten"), (1.8, 200, 800)), (A("e9", "walked"), (1.9, 520, 820))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    garden(cr, t)
    toad(cr, 200, 905, t, 0.9, sick=1.0, seed=9900)
    walk = seg(t, A("e9", "walked"), A("e9", end=True) + 0.6)
    beetle(cr, lerp(420, 640, walk), 905, t, 1.1, facing=1, walk=t * 2.5 if walk > 0 else None, shades=True, seed=9910)
    hl(cr, t, [("a ", INK), ("bad day", RED), ("?", INK)], 215, 84, A("e9", "bad"), end=A("e9", "eaten") - 0.05, bold=True)
    hl(cr, t, [("got ", INK), ("EATEN", RED), ("... walked it off", INK)], 215, 56, A("e9", "eaten"), bold=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "garden":
        scene_garden(cr, t, tl)
    elif name == "inside":
        scene_inside(cr, t, tl)
    elif name == "pulses":
        scene_pulses(cr, t, tl)
    elif name == "toad":
        scene_toad(cr, t, tl, 1)
    elif name == "toad2":
        scene_toad(cr, t, tl, 2)
    else:
        scene_end(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
