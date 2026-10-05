"""Episode 19: "The Last Bencher vs The Principal" — trick riddles in the principal's office, with a twist.

Riddles: which way the smoke blows from an electric train (there's no smoke), seventeen sheep where all but nine run
away (nine are left), a pound of bricks or a pound of feathers (same). The principal wins with "the more you take, the
more you leave behind" (footsteps), and sends him off with "tell your mom I'll be late for dinner": the principal is his
dad. The clue is planted from the first shot: a photo of the two of them on the desk.
"""
import math

from motion.captions import captions
from motion.timeline import clear_dialogue
from motion.characters import person
from motion.engine import (INK, RED, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape,
                           sharp_shape, write)
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict(speed=1.0, max_pause=0.42)
TAIL = 0.9

SCRIPT = [
    dict(id="p1", scene="office", text="The last bencher in class finally got sent to the principal's office."),
    dict(id="p2", scene="office", text="The principal leans back: so, you like riddles? Try me.",
         speaker="principal", speaker_from="so,"),
    dict(id="p3", scene="train", text="Sir, an electric train is going north. Which way does the smoke blow?",
         speaker="chotu"),
    dict(id="p4", scene="office", text="South, obviously.", speaker="principal"),
    dict(id="p5", scene="train2", text="Electric train, sir. No smoke.", speaker="chotu"),
    dict(id="p6", scene="sheep",
         text="A farmer has [seventeen|17] sheep. All but [nine|9] run away. How many are left?", speaker="chotu"),
    dict(id="p7", scene="office", text="It's eight, of course.", speaker="principal"),
    dict(id="p8", scene="sheep2", text="[Nine,|9,] sir. All but [nine|9] ran away.", speaker="chotu"),
    dict(id="p9", scene="scale", text="Which is heavier? A pound of bricks, or a pound of feathers?", speaker="chotu"),
    dict(id="p10", scene="office", text="The bricks.", speaker="principal"),
    dict(id="p11", scene="scale2", text="Same, sir. A pound is a pound.", speaker="chotu"),
    dict(id="p12", scene="office", text="The principal smiles. My turn.", speaker="principal", speaker_from="my"),
    dict(id="p13", scene="steps", text="The more you take, the more you leave behind. What am I?",
         speaker="principal"),
    dict(id="p14", scene="office", text="Detentions?", speaker="chotu"),
    dict(id="p15", scene="office", text="Footsteps. So take yours. To detention.", speaker="principal"),
    dict(id="p16", scene="office", text="Oh, and tell your mom I'll be late for dinner.", speaker="principal",
         gap=0.25),
    dict(id="p17", scene="end", text="Yep. The principal is his dad. Dinner was awkward.", gap=0.2),
]
clear_dialogue(SCRIPT)   # riddles and answers: slower, with clear turns

METADATA = dict(
    title="Last Bencher vs The PRINCIPAL 😂 (Wait for the Twist)",
    alt_titles=["He Tried His Riddles on the Principal… 😂", "3 Trick Riddles vs the Principal 🤣"],
    description="""The last bencher finally got sent to the principal's office… so he brought riddles. 😂

Riddle 1: An electric train is going north. Which way does the smoke blow?
Riddle 2: A farmer has 17 sheep. All but 9 run away. How many are left?
Riddle 3: Which is heavier, a pound of bricks or a pound of feathers?

Then the principal plays his card. 👀 Did you spot the clue in the very first shot?

💬 How many did you get right?

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Riddles", "#LastBencher", "#Funny"],
    tags=["riddles", "trick questions", "last bencher", "backbenchers", "principal", "funny riddles", "school jokes", "brain teaser",
          "riddle challenge", "plot twist", "classroom comedy", "interestingly strange"],
    pinned_comment="The clue was there from the very first second 👀 Did you spot it? Rewatch and look at the desk 😂",
)

WALL = hexc("#ead7b4")
WAIN = hexc("#c9a77a")
CARPET = hexc("#8e4b45")
WOOD = hexc("#8e5a2e")
WOOD_L = hexc("#b9824a")
MB = hexc("#2f6fd1")     # markers
MR = hexc("#e03b3b")
MG = hexc("#2e9e52")
MO = hexc("#f08c1a")
BLUE = hexc("#3f6fb5")

PX, PY = 300, 850        # principal, behind his desk
KX = 560                 # the kid
DOOR = 700
PHOTO = (178, 770)
PRIN = (2.1, 300, 700)
KIDC = (2.0, 570, 760)
TWO = (1.3, 430, 730)
WIDE = (1.0, 400, 700)


def laughing(t, tl):
    return False


# ------------------------------------------------------------------ the office
def photo(cr, t, x, y, s=1.0):
    """Framed photo of the principal and the kid together (the clue)."""
    with at(cr, x, y, s, rot=-0.08):
        sharp_shape(cr, [(-36, -60), (36, -60), (36, 0), (-36, 0)], WOOD, seed=6000, amp=0.4, lw=3)
        cr.rectangle(-28, -52, 56, 44)
        cr.set_source_rgba(*hexc("#bfe6ff"))
        cr.fill_preserve()
        cr.save()
        cr.clip()
        person(cr, "principal", -12, 20, t, scale=0.3, arms=("hold", "hip"), eyes="happy", mouth="grin", bob=False)
        person(cr, "chotu", 14, 22, t, scale=0.3, arms=("cheer", "hip"), eyes="happy", mouth="grin", bob=False)
        cr.restore()
        line(cr, [(0, 0), (-10, 14)], 3, INK, seed=6001, amp=0.2)   # stand


def office(cr, t, door_open=0.0):
    cr.set_source_rgba(*WALL)
    cr.paint()
    sharp_shape(cr, [(-800, 640), (1600, 640), (1600, 900), (-800, 900)], WAIN, seed=6010, amp=0.8, lw=3)
    for k in range(-8, 18):
        line(cr, [(k * 80, 650), (k * 80, 890)], 2.5, hexc("#b8956a"), seed=6011 + k, amp=0.5)
    sharp_shape(cr, [(-800, 900), (1600, 895), (1600, 1900), (-800, 1900)], CARPET, seed=6040, amp=0.8, lw=4)
    # bookshelf
    sharp_shape(cr, [(-160, 360), (90, 360), (90, 900), (-160, 900)], WOOD, seed=6050, amp=0.6, lw=4)
    for r in range(4):
        y = 400 + r * 120
        sharp_shape(cr, [(-140, y), (70, y), (70, y + 100), (-140, y + 100)], hexc("#5e3a1c"), seed=6051 + r, amp=0.4,
                    lw=2.5)
        for b in range(7):
            col = [MR, MB, MG, MO, hexc("#7b4bb5"), hexc("#d9b44a"), hexc("#3a8f8f")][(b + r * 3) % 7]
            hgt = 70 + (b * 13 + r * 7) % 26
            sharp_shape(cr, [(-130 + b * 28, y + 100 - hgt), (-106 + b * 28, y + 100 - hgt), (-106 + b * 28, y + 100),
                             (-130 + b * 28, y + 100)], col, seed=6060 + r * 10 + b, amp=0.3, lw=2)
    # window
    sharp_shape(cr, [(170, 380), (420, 380), (420, 580), (170, 580)], hexc("#bfe6ff"), seed=6080, amp=0.6, lw=4)
    blob(cr, 240, 430, 36, 14, WHITE, seed=6081, amp=0.8, lw=0, stroke=None)
    line(cr, [(295, 380), (295, 580)], 4, INK, seed=6082, amp=0.3)
    line(cr, [(170, 480), (420, 480)], 4, INK, seed=6083, amp=0.3)
    # framed certificate
    sharp_shape(cr, [(470, 400), (590, 400), (590, 490), (470, 490)], hexc("#d9b44a"), seed=6090, amp=0.4, lw=3.5)
    sharp_shape(cr, [(482, 412), (578, 412), (578, 478), (482, 478)], WHITE, seed=6091, amp=0.3, lw=2)
    write(cr, [("PRINCIPAL", INK)], 530, 440, 15, align="center", bold=True)
    line(cr, [(495, 458), (565, 458)], 2, INK, seed=6092, amp=0.3)
    blob(cr, 565, 470, 9, 9, MR, seed=6093, amp=0.3, lw=2)
    # door (opens for the exit)
    sharp_shape(cr, [(DOOR - 10, 470), (DOOR + 150, 470), (DOOR + 150, 900), (DOOR - 10, 900)], INK, seed=6100,
                amp=0.4, lw=3)
    w = 140 * (1 - 0.8 * door_open)
    sharp_shape(cr, [(DOOR, 480), (DOOR + w, 485), (DOOR + w, 895), (DOOR, 900)], WOOD_L, seed=6101, amp=0.4, lw=3.5)
    dot(cr, DOOR + w - 20, 700, 7, hexc("#d9b44a"))


def desk_front(cr, t, show_photo=True):
    sharp_shape(cr, [(110, 776), (500, 776), (500, 800), (110, 800)], WOOD_L, seed=6200, amp=0.5, lw=4)
    sharp_shape(cr, [(126, 800), (484, 800), (484, 905), (126, 905)], WOOD, seed=6201, amp=0.5, lw=4)
    sharp_shape(cr, [(230, 830), (370, 830), (370, 870), (230, 870)], hexc("#d9b44a"), seed=6202, amp=0.3, lw=2.5)
    write(cr, [("PRINCIPAL", INK)], 300, 858, 20, align="center", bold=True)
    # on the desk: papers, a mug, and the photo
    sharp_shape(cr, [(380, 776), (450, 770), (452, 762), (382, 768)], WHITE, seed=6210, amp=0.3, lw=2)
    sharp_shape(cr, [(420, 776), (446, 776), (444, 744), (422, 744)], MR, seed=6211, amp=0.3, lw=2.5)
    if show_photo:
        photo(cr, t, *PHOTO)


def scene_office(cr, t, tl):
    A = tl.at
    keys = [(0, (1.6, 240, 720)), (A("p1", "bencher"), (1.7, 620, 760)), (A("p1", "sent"), (1.2, 520, 740)),
            (A("p1", "principal's"), (1.9, 300, 700)), (A("p1", "office"), WIDE),
            (A("p2") - 0.1, PRIN), (A("p2", "back"), (1.6, 320, 720)), (A("p2", "riddles"), (2.3, 300, 690)),
            (A("p2", "try"), TWO),
            (A("p4") - 0.1, PRIN), (A("p4", "obviously"), (2.4, 300, 680)),
            (A("p7") - 0.1, (2.4, 300, 690)),
            (A("p10") - 0.1, PRIN), (A("p10", "bricks"), (2.5, 300, 680)),
            (A("p12") - 0.1, TWO), (A("p12", "smiles"), PRIN), (A("p12", "my"), (2.5, 300, 680)),
            (A("p14") - 0.1, KIDC), (A("p14", "detentions", end=True) - 0.2, (2.4, 570, 740)),
            (A("p15") - 0.1, PRIN), (A("p15", "take"), TWO), (A("p15", "detention"), (1.5, 640, 760)),
            (A("p16") - 0.1, PRIN), (A("p16", "mom"), (2.2, 300, 690)), (A("p16", "late"), (1.6, 620, 740)),
            (A("p16", "dinner"), (2.3, 730, 730))]
    z, fx, fy = camera(t, keys)
    set_camera((z, fx, fy))
    enter_world(cr)
    exit_t = A("p15", "take")
    door = seg(t, exit_t, exit_t + 0.4)
    office(cr, t, door)
    # ---- principal (behind the desk)
    s = dict(facing=1, arms=("hold", "hold"), eyes="dot", mouth="flat")
    lean = 0.0
    if A("p1", "office") <= t < A("p2"):
        s.update(eyes="sly", mouth="flat", arms=("hip", "hip"))
    if A("p2") <= t < A("p3"):
        lean = -0.12 * seg(t, A("p2", "leans"), A("p2", "leans") + 0.3)
        s.update(arms=("chin", "hip"), eyes="sly", mouth="smirk")
        if t >= A("p2", "try"):
            s.update(arms=("point", "hip"))
    if A("p4") <= t < A("p5") or A("p7") <= t < A("p8") or A("p10") <= t < A("p11"):
        s.update(arms=("point", "hip"), eyes="sly", mouth="smirk")
    if A("p10") <= t < A("p11"):
        s.update(sweat=True)
    if A("p12") <= t < A("p13"):
        s.update(eyes="happy", mouth="grin", arms=("hip", "hip"))
        if t >= A("p12", "my"):
            s.update(eyes="sly", mouth="smirk", arms=("point", "hip"))
    if A("p14") <= t:
        s.update(eyes="sly", mouth="smirk", arms=("hip", "hip"))
    if A("p15") <= t < A("p16"):
        s.update(arms=("point", "hip"), eyes="happy" if t < A("p15", "take") else "sly", mouth="grin")
    if A("p16") <= t:
        s.update(arms=("wave", "hip"), eyes="happy", mouth="grin")
    if tl.speaking("principal", t):
        s["mouth"] = "o" if int(t * 12) % 2 else "smile"
    person(cr, "principal", PX, PY, t, lean=lean, **s)
    desk_front(cr, t)
    # ---- the kid: walks in, answers, walks out to detention
    walk_in = ease_out(seg(t, 0.0, A("p1", "sent")))
    x = lerp(DOOR + 70, KX, walk_in)
    k = dict(facing=-1, arms=("hip", "hip"), eyes="dot", mouth="smile")
    walking = walk_in < 1
    if A("p1", "office") <= t < A("p2", "try"):
        k.update(eyes="sly", mouth="smirk", arms=("hip", "hip"))
    if A("p2", "try") <= t < A("p3"):
        k.update(eyes="happy", mouth="grin", arms=("cheer", "hip"))
    if A("p4") <= t < A("p5") or A("p7") <= t < A("p8") or A("p10") <= t < A("p11"):
        k.update(eyes="sly", mouth="smirk", arms=("chin", "hip"))
    if A("p12") <= t < A("p14"):
        k.update(eyes="wide", mouth="o", sweat=t >= A("p12", "my"))
    if A("p14") <= t < A("p15"):
        k.update(eyes="sly", mouth="smirk", arms=("chin", "hip"))
    out = 0.0
    prints = []
    if t >= exit_t:
        out = seg(t, exit_t, A("p16") - 0.05)
        x = lerp(KX, DOOR + 40, out)
        walking = out < 1
        k.update(facing=1, eyes="sad", mouth="wobble", arms=("down", "down"))
        n = int(out * 6)
        prints = [(lerp(KX, DOOR + 40, i / 6), i % 2) for i in range(n)]
    if A("p16") <= t:
        x = DOOR + 40
        walking = False
        k.update(facing=-1, eyes="wide", mouth="o", sweat=t >= A("p16", "dinner"), arms=("down", "down"))
        prints = [(lerp(KX, DOOR + 40, i / 6), i % 2) for i in range(6)]
    for px, side in prints:   # footsteps on the carpet
        blob(cr, px + (10 if side else -10), 925 + (6 if side else 0), 12, 7, hexc("#5e2e2a"), seed=6300 + int(px),
             amp=0.4, lw=0, stroke=None)
    if tl.speaking("chotu", t):
        k["mouth"] = "o" if int(t * 12) % 2 else "smirk"
    person(cr, "chotu", x, 900, t, walk=t * 1.8 if walking else None, **k)
    # ---- screen text
    hl(cr, t, [("LAST BENCHER", RED), (" vs ", INK), ("PRINCIPAL", BLUE)], 215, 54, 0.0, end=A("p1", "sent") - 0.05,
       bold=True, sound=False)
    hl(cr, t, [("sent to the ", INK), ("PRINCIPAL", RED)], 215, 62, A("p1", "sent"), end=A("p2") - 0.05, bold=True)
    hl(cr, t, [("\"Try me.\"", BLUE)], 215, 80, A("p2", "try"), end=A("p3") - 0.05, bold=True)
    hl(cr, t, [("\"SOUTH", BLUE), (", obviously.\"", INK)], 215, 64, A("p4"), end=A("p5") - 0.05, bold=True)
    hl(cr, t, [("\"EIGHT.\"", BLUE)], 215, 90, A("p7"), end=A("p8") - 0.05, bold=True)
    hl(cr, t, [("\"The ", INK), ("BRICKS", BLUE), (".\"", INK)], 215, 80, A("p10", "bricks"), end=A("p11") - 0.05,
       bold=True)
    hl(cr, t, [("\"MY TURN.\"", RED)], 215, 90, A("p12", "my"), end=A("p13") - 0.05, bold=True)
    hl(cr, t, [("\"Detentions?\"", INK)], 215, 72, A("p14"), end=A("p15") - 0.05, bold=True)
    hl(cr, t, [("FOOTSTEPS", RED)], 215, 90, A("p15"), end=A("p15", "take") - 0.05, bold=True)
    hl(cr, t, [("take yours... to ", INK), ("DETENTION", RED)], 215, 54, A("p15", "take"), end=A("p16") - 0.05,
       bold=True)
    hl(cr, t, [("\"tell your ", INK), ("MOM", RED), ("...\"", INK)], 215, 76, A("p16", "mom"),
       end=A("p16", "dinner") - 0.05, bold=True)
    hl(cr, t, [("\"late for ", INK), ("DINNER", RED), (".\"", INK)], 215, 72, A("p16", "dinner"), bold=True)
    for w in (A("p15"), A("p16", "dinner")):
        cue("hit", t, w)
    if out > 0:
        cue("whoosh", t, exit_t)


# ------------------------------------------------------------------ whiteboard scenes
def whiteboard(cr, t, keys):
    cr.set_source_rgba(*hexc("#b8bcc4"))
    cr.paint()
    z, fx, fy = camera(t, keys, dur=0.14)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    sharp_shape(cr, [(-500, -300), (1220, -300), (1220, 1580), (-500, 1580)], hexc("#fbfbf8"), seed=6400, amp=1.0,
                lw=6)
    cr.set_line_width(26)
    for k in range(9):   # old marker ghosts, so camera moves read on screen
        cr.set_source_rgba(0.2, 0.3, 0.5, 0.06)
        x0, y0 = -300 + (k * 263) % 1300, -100 + (k * 397) % 1500
        cr.move_to(x0, y0)
        cr.curve_to(x0 + 80, y0 - 40, x0 + 160, y0 + 40, x0 + 260, y0)
        cr.stroke()


def qmark(cr, t, start, x, y, size=140, col=MR):
    sc = pop(t, start, 0.3)
    if sc > 0:
        with at(cr, x, y, sc, rot=0.12 * math.sin(t * 5)):
            write(cr, [("?", col)], 0, size * 0.35, size, align="center", bold=True)
        cue("pop", t, start)


def train(cr, x, y, s=1.0, t=0.0):
    with at(cr, x, y, s):
        sharp_shape(cr, [(-180, -90), (150, -90), (190, -40), (190, 30), (-180, 30)], None, seed=6500, amp=0.6, lw=6,
                    stroke=MB)
        for k in range(4):
            sharp_shape(cr, [(-150 + k * 80, -70), (-100 + k * 80, -70), (-100 + k * 80, -30), (-150 + k * 80, -30)],
                        None, seed=6501 + k, amp=0.4, lw=4, stroke=MB)
        for wx in (-130, -40, 60, 140):
            blob(cr, wx, 40, 22, 22, None, seed=6510 + wx, amp=0.4, lw=5, stroke=INK)
            line(cr, [(wx, 40), (wx + 16 * math.cos(t * 12), 40 + 16 * math.sin(t * 12))], 3, INK, seed=6520, amp=0)
        # pantograph up to the wire: it's electric
        line(cr, [(-20, -90), (-50, -140), (10, -170)], 4, INK, seed=6530, amp=0.3)


def scene_train(cr, t, tl, part):
    A = tl.at
    if part == 1:
        keys = [(A("p3") - 0.2, (1.1, 360, 760)), (A("p3", "electric"), (1.8, 330, 600)), (A("p3", "train"), (1.0, 360, 760)),
                (A("p3", "north"), (1.6, 560, 480)), (A("p3", "which"), (1.1, 360, 700)), (A("p3", "smoke"), (1.7, 300, 560)),
                (A("p3", "blow"), (1.0, 360, 700))]
    else:
        keys = [(A("p5") - 0.2, (1.4, 340, 700)), (A("p5", "train"), (1.0, 360, 740)), (A("p5", "no"), (1.8, 300, 560)),
                (A("p5", "smoke"), (1.1, 360, 680))]
    whiteboard(cr, t, keys)
    # overhead wire and track
    line(cr, [(-300, 530), (1000, 530)], 4, INK, seed=6540, amp=0.6)
    line(cr, [(-300, 900), (1000, 900)], 6, INK, seed=6541, amp=0.6)
    for k in range(14):
        line(cr, [(-260 + k * 90, 900), (-280 + k * 90, 925)], 4, INK, seed=6542 + k, amp=0.3)
    tx = 340 + (math.sin(t * 1.5) * 16 if part == 1 else 0)
    train(cr, tx, 830, 1.0, t)
    # north
    sc = pop(t, A("p3", "north"), 0.25) if part == 1 else 1.0
    if sc > 0:
        with at(cr, 560, 420, sc):
            line(cr, [(-70, 0), (70, 0)], 7, MG, seed=6550, amp=0.4)
            line(cr, [(40, -26), (72, 0), (40, 26)], 7, MG, seed=6551, amp=0.3)
            write(cr, [("NORTH", MG)], 0, -26, 40, align="center", bold=True)
    if part == 1:
        if t >= A("p3", "electric"):
            sc = pop(t, A("p3", "electric"), 0.25)
            with at(cr, 330, 600, sc, rot=0.2):   # spark on the wire
                sharp_shape(cr, [(0, -40), (-20, 6), (6, 6), (-10, 46), (30, -8), (4, -8), (18, -40)], MO, seed=6560,
                            amp=0.3, lw=3)
        if t >= A("p3", "smoke"):
            for i in range(3):
                sc = pop(t, A("p3", "smoke") + i * 0.08, 0.25)
                with at(cr, 140 + i * 70, 560 - i * 40, sc):
                    blob(cr, 0, 0, 40 + i * 6, 30 + i * 4, hexc("#d9dde3"), seed=6570 + i, amp=1.0, lw=3.5)
        if t >= A("p3", "which"):
            for side, col, sd in ((-1, MB, 6580), (1, MR, 6590)):
                with at(cr, 360 + side * 230, 680, pop(t, A("p3", "which") + (0.1 if side > 0 else 0), 0.25)):
                    line(cr, [(-50, 0), (50, 0)], 6, col, seed=sd, amp=0.4)
                    line(cr, [(side * 28, -22), (side * 52, 0), (side * 28, 22)], 6, col, seed=sd + 1, amp=0.3)
        qmark(cr, t, A("p3", "blow"), 600, 640)
        hl(cr, t, [("ELECTRIC", MO), (" train", INK)], 215, 70, A("p3", "electric"), end=A("p3", "which") - 0.05,
           bold=True)
        hl(cr, t, [("which way does the ", INK), ("smoke", RED), (" go?", INK)], 215, 52, A("p3", "which"), bold=True)
    else:
        for i in range(3):   # the smoke we imagined, crossed out
            with at(cr, 140 + i * 70, 560 - i * 40, 1.0):
                blob(cr, 0, 0, 40 + i * 6, 30 + i * 4, hexc("#d9dde3", 0.6), seed=6570 + i, amp=1.0, lw=3)
        if t >= A("p5", "no"):
            k = seg(t, A("p5", "no"), A("p5", "no") + 0.2)
            line(cr, [(90, 450), (90 + 260 * k, 450 + 160 * k)], 10, MR, seed=6600, amp=0.5)
            line(cr, [(350, 450), (350 - 260 * k, 450 + 160 * k)], 10, MR, seed=6601, amp=0.5)
            cue("hit", t, A("p5", "no"))
        stamp(cr, t, A("p5", "smoke"), "NO SMOKE", dur=0.7, y=330)
        hl(cr, t, [("It's ", INK), ("ELECTRIC", MO), (".", INK)], 215, 76, A("p5"), bold=True, underline=True)


def sheep(cr, x, y, s=1.0, seed=0, legs=0.0, col=INK):
    with at(cr, x, y, s):
        for k in range(5):
            blob(cr, -26 + k * 13, -6 - (k % 2) * 8, 18, 16, WHITE, seed=seed + k, amp=0.6, lw=3, stroke=col)
        blob(cr, 38, -4, 14, 12, hexc("#3a3a3a"), seed=seed + 6, amp=0.4, lw=2.5)
        dot(cr, 42, -8, 2.5, WHITE)
        for k, lx in enumerate((-20, -6, 10, 22)):
            sw = math.sin(legs + k * 1.6) * 8 if legs else 0
            line(cr, [(lx, 8), (lx + sw, 30)], 4, INK, seed=seed + 10 + k, amp=0.2)


SHEEP = [(105 + (k % 5) * 128, 450 + (k // 5) * 150) for k in range(17)]
RUN = {1, 3, 5, 6, 8, 11, 13, 16}      # the eight that run off


def scene_sheep(cr, t, tl, part):
    A = tl.at
    if part == 1:
        keys = [(A("p6") - 0.2, (1.4, 200, 700)), (A("p6", "farmer"), (1.8, 140, 1040)), (A("p6", "17"), (1.0, 360, 700)),
                (A("p6", "sheep"), (1.3, 360, 640)), (A("p6", "all"), (1.0, 360, 720)), (A("p6", "9"), (1.5, 400, 700)),
                (A("p6", "run"), (1.0, 380, 700)), (A("p6", "how"), (1.2, 360, 760)), (A("p6", "left"), (1.0, 360, 720))]
    else:
        keys = [(A("p8") - 0.2, (1.2, 360, 700)), (A("p8", "sir"), (1.0, 360, 700)), (A("p8", "all"), (1.3, 360, 640)),
                (A("p8", "but"), (1.1, 360, 700)), (A("p8", "9.", nth=1), (1.4, 360, 760))]
    whiteboard(cr, t, keys)
    # fence and farmer
    line(cr, [(-200, 1000), (1000, 1000)], 5, MG, seed=6700, amp=0.8)
    if part == 1:
        sc = pop(t, A("p6", "farmer"), 0.25)
        if sc > 0:
            with at(cr, 140, 1180, sc):
                blob(cr, 0, -150, 24, 24, None, seed=6710, amp=0.5, lw=5, stroke=INK)
                sharp_shape(cr, [(-40, -170), (40, -170), (20, -186), (-20, -186)], None, seed=6711, amp=0.3, lw=4,
                            stroke=MO)
                line(cr, [(0, -126), (0, -50), (-20, 0)], 5, INK, seed=6712, amp=0.4)
                line(cr, [(0, -50), (20, 0)], 5, INK, seed=6713, amp=0.4)
                line(cr, [(-30, -80), (0, -110), (40, -120)], 5, INK, seed=6714, amp=0.4)
    run_t = A("p6", "run") if part == 1 else -1
    count = 0
    for k, (x, y) in enumerate(SHEEP):
        if part == 1:
            sc = pop(t, A("p6", "17") + k * 0.025, 0.2)
            if sc <= 0:
                continue
            legs = 0.0
            if k in RUN and t >= run_t:
                u = seg(t, run_t + (k % 4) * 0.05, run_t + 0.7 + (k % 4) * 0.05)
                x = lerp(x, x + 900, u * u)
                legs = t * 20
            with at(cr, x, y, sc * 1.1):
                sheep(cr, 0, 0, 1.0, seed=6800 + k * 20, legs=legs)
        else:
            if k in RUN:
                continue
            sheep(cr, x, y, 1.1, seed=6800 + k * 20)
            count += 1
            tick = A("p8") + (count - 1) * 0.07
            if t >= tick:
                write(cr, [(str(count), MB)], x, y - 50, 44, align="center", bold=True)
    if part == 1:
        if t >= run_t:
            for i in range(4):   # dust
                blob(cr, 720 + i * 30, 900 + (i % 2) * 40, 20, 14, hexc("#d9dde3"), seed=6900 + i, amp=0.8, lw=2)
        hl(cr, t, [("17", MB), (" sheep", INK)], 215, 80, A("p6", "17"), end=A("p6", "all") - 0.05, bold=True)
        hl(cr, t, [("all but ", INK), ("9", RED), (" run away", INK)], 215, 66, A("p6", "all"), end=A("p6", "how") - 0.05,
           bold=True)
        hl(cr, t, [("how many are ", INK), ("left", RED), ("?", INK)], 215, 66, A("p6", "how"), bold=True)
        cue("whoosh", t, run_t)
    else:
        stamp(cr, t, A("p8", "all"), "ALL BUT 9 = 9 STAY", dur=0.7, y=330)
        cue("hit", t, A("p8", "all"))
        hl(cr, t, [("NINE", RED), (" stay", INK)], 215, 84, A("p8"), bold=True, underline=True)


def balance(cr, t, tilt, left_item, right_item, seed=7000):
    """A balance scale; tilt > 0 = left pan down."""
    line(cr, [(360, 1200), (360, 720)], 8, INK, seed=seed, amp=0.4)
    sharp_shape(cr, [(260, 1200), (460, 1200), (420, 1170), (300, 1170)], None, seed=seed + 1, amp=0.4, lw=5,
                stroke=INK)
    ax, ay = 360, 720
    a = 0.22 * tilt
    for side in (-1, 1):
        px = ax + side * 230 * math.cos(a)
        py = ay - side * 230 * math.sin(a)          # tilt > 0: left end goes down
        line(cr, [(ax, ay), (px, py)], 7, INK, seed=seed + 2 + side, amp=0.3)
        line(cr, [(px, py), (px - 80, py + 140)], 3, INK, seed=seed + 5 + side, amp=0.2)
        line(cr, [(px, py), (px + 80, py + 140)], 3, INK, seed=seed + 7 + side, amp=0.2)
        shape(cr, [(px - 100, py + 140), (px + 100, py + 140), (px + 70, py + 170), (px - 70, py + 170)], None,
              seed=seed + 9 + side, amp=0.4, lw=5, stroke=INK)
        item = left_item if side < 0 else right_item
        if item:
            item(cr, px, py + 138)
    blob(cr, ax, ay, 12, 12, MO, seed=seed + 20, amp=0.3, lw=3)


def bricks(cr, x, y):
    for r in range(2):
        for c in range(3 - r):
            bx, by = x - 66 + c * 44 + r * 22, y - 20 - r * 26
            sharp_shape(cr, [(bx - 20, by - 12), (bx + 20, by - 12), (bx + 20, by + 12), (bx - 20, by + 12)],
                        hexc("#c0504d"), seed=7100 + r * 5 + c, amp=0.3, lw=3)


def feathers(cr, x, y):
    # a big fluffy pile: a pound of feathers takes up a lot of room
    for k in range(7):
        a = -0.9 + k * 0.3
        with at(cr, x - 60 + k * 20, y - 30 - (k % 3) * 22, 1.0, rot=a):
            shape(cr, [(-8, 50), (-18, 0), (0, -50), (18, 0), (8, 50)], hexc("#f5f5f0"), seed=7200 + k, amp=0.5,
                  lw=3)
            line(cr, [(0, 50), (0, -44)], 2.5, MB, seed=7210 + k, amp=0.2)


def scene_scale(cr, t, tl, part):
    A = tl.at
    if part == 1:
        keys = [(A("p9") - 0.2, (1.4, 360, 640)), (A("p9", "heavier"), (1.0, 360, 760)), (A("p9", "pound"), (1.5, 140, 820)),
                (A("p9", "bricks"), (1.8, 140, 860)), (A("p9", "feathers"), (1.8, 580, 860)),
                (A("p9", "feathers", end=True), (1.0, 360, 760))]
        tilt = 0.0
        if t >= A("p9", "bricks"):
            tilt = 1.0 * ease_out(seg(t, A("p9", "bricks"), A("p9", "bricks") + 0.3))
        if t >= A("p9", "feathers"):
            tilt = 1.0 - ease_out(seg(t, A("p9", "feathers"), A("p9", "feathers") + 0.3)) * 1.6
        if t >= A("p9", "feathers", end=True):
            tilt = -0.6 + 0.9 * math.sin((t - A("p9", "feathers", end=True)) * 5) * 0.6   # wobbling: which one?
    else:
        keys = [(A("p11") - 0.2, (1.4, 360, 760)), (A("p11", "pound"), (1.0, 360, 760)), (A("p11", "is"), (1.5, 360, 620)),
                (A("p11", "pound", nth=2), (1.0, 360, 760))]
        tilt = 0.6 * (1 - ease_out(seg(t, A("p11"), A("p11") + 0.4)))
    whiteboard(cr, t, keys)
    balance(cr, t, tilt, bricks if (part == 2 or t >= A("p9", "bricks")) else None,
            feathers if (part == 2 or t >= A("p9", "feathers")) else None)
    if part == 1:
        for key, x, lab, col in (("bricks", 130, "1 lb", MR), ("feathers", 590, "1 lb", MB)):
            if t >= A("p9", key):
                write(cr, [(lab, col)], x, 660, 50, align="center", bold=True)
                cue("thud" if key == "bricks" else "pop", t, A("p9", key))
        qmark(cr, t, A("p9", "feathers", end=True), 360, 560, 120)
        hl(cr, t, [("which is ", INK), ("heavier", RED), ("?", INK)], 215, 70, A("p9", "heavier"), bold=True)
    else:
        write(cr, [("1 lb", MR)], 130, 660, 50, align="center", bold=True)
        write(cr, [("1 lb", MB)], 590, 660, 50, align="center", bold=True)
        if t >= A("p11", "is"):
            with at(cr, 360, 560, pop(t, A("p11", "is"), 0.25)):
                write(cr, [("=", MR)], 0, 30, 140, align="center", bold=True)
            cue("hit", t, A("p11", "is"))
        hl(cr, t, [("SAME", RED), (". A pound is a pound.", INK)], 215, 56, A("p11"), bold=True)


def scene_steps(cr, t, tl):
    """Footprints: the more you take, the more you leave behind."""
    A = tl.at
    keys = [(A("p13") - 0.2, (1.5, 160, 1100)), (A("p13", "take"), (1.0, 360, 860)), (A("p13", "leave"), (1.4, 300, 820)),
            (A("p13", "behind"), (1.0, 360, 760)), (A("p13", "what"), (1.5, 560, 560)), (A("p13", "am"), (1.0, 360, 760))]
    whiteboard(cr, t, keys)
    t0, t1 = A("p13"), A("p13", "behind", end=True)
    n = 1 + int(13 * seg(t, t0, t1))
    for k in range(n):
        u = k / 13
        x = 80 + u * 520 + (24 if k % 2 else -24) * 0.6
        y = 1100 - u * 680
        with at(cr, x, y, 1.0, rot=-0.55):
            blob(cr, 0, 0, 16, 26, MB, seed=7300 + k, amp=0.5, lw=2.5)
            for j in range(4):
                blob(cr, -10 + j * 7, -32 - (j % 2) * 3, 5, 5, MB, seed=7320 + k * 4 + j, amp=0.2, lw=1.5)
        cue("pop", t, t0 + k * (t1 - t0) / 14)
    qmark(cr, t, A("p13", "am"), 600, 520, 150)
    hl(cr, t, [("the more you ", INK), ("TAKE", BLUE), ("...", INK)], 215, 70, A("p13", "take"),
       end=A("p13", "leave") - 0.05, bold=True)
    hl(cr, t, [("...the more you ", INK), ("LEAVE", RED)], 215, 70, A("p13", "leave"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    dinner = A("p17", "dinner")
    if t < dinner:
        keys = [(A("p17") - 0.2, (2.6, PHOTO[0], PHOTO[1] - 30)), (A("p17", "principal"), (3.8, PHOTO[0], PHOTO[1] - 30)),
                (A("p17", "dad"), (5.0, PHOTO[0], PHOTO[1] - 30))]
        set_camera(camera(t, keys))
        enter_world(cr)
        office(cr, t, 1.0)
        person(cr, "principal", PX, PY, t, arms=("wave", "hip"), eyes="happy", mouth="grin")
        desk_front(cr, t)
        if t >= A("p17", "dad"):   # a doodled heart and "ME + DAD" on the photo
            with at(cr, PHOTO[0], PHOTO[1] - 70, pop(t, A("p17", "dad"), 0.25)):
                write(cr, [("ME + DAD", MR)], 0, 0, 14, align="center", bold=True)
            cue("hit", t, A("p17", "dad"))
        hl(cr, t, [("the principal is ", INK), ("HIS DAD", RED)], 215, 62, A("p17", "principal"), bold=True,
           underline=True, end=dinner - 0.05)
        return
    # dinner: the most awkward table in town
    keys = [(dinner - 0.05, (1.3, 360, 760)), (A("p17", "awkward"), (1.6, 360, 740)),
            (A("p17", "awkward") + 0.5, (2.2, 520, 720))]
    set_camera(camera(t, keys))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#f2d9a8"))
    cr.paint()
    sharp_shape(cr, [(-800, 900), (1600, 895), (1600, 1900), (-800, 1900)], hexc("#a87a4f"), seed=7400, amp=0.8, lw=4)
    blob(cr, 360, 380, 60, 40, hexc("#ffe08a"), seed=7401, amp=0.6, lw=3)             # lamp
    line(cr, [(360, 200), (360, 340)], 3, INK, seed=7402, amp=0.2)
    for who, x, face in (("principal", 160, 1), ("mom", 360, 1), ("chotu", 560, -1)):
        side_eye = "sly"
        person(cr, who, x, 880, t, facing=face, eyes=side_eye, mouth="flat", sweat=who != "mom",
               arms=("hold", "hold"))
    sharp_shape(cr, [(40, 790), (680, 790), (680, 820), (40, 820)], hexc("#f4efe1"), seed=7410, amp=0.6, lw=4)
    sharp_shape(cr, [(60, 820), (660, 820), (660, 900), (60, 900)], hexc("#c0504d"), seed=7411, amp=0.6, lw=4)
    for x in (160, 360, 560):
        blob(cr, x, 786, 46, 10, WHITE, seed=7420 + x, amp=0.4, lw=3)
    if t >= A("p17", "awkward"):
        write(cr, [("...", INK)], 360, 560, 80, align="center", bold=True)
        write(cr, [("*fork scrape*", INK)], 560, 640, 26, align="center")
    hl(cr, t, [("dinner was ", INK), ("AWKWARD", RED)], 215, 68, A("p17", "awkward"), bold=True, underline=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "train":
        scene_train(cr, t, tl, 1)
    elif name == "train2":
        scene_train(cr, t, tl, 2)
    elif name == "sheep":
        scene_sheep(cr, t, tl, 1)
    elif name == "sheep2":
        scene_sheep(cr, t, tl, 2)
    elif name == "scale":
        scene_scale(cr, t, tl, 1)
    elif name == "scale2":
        scene_scale(cr, t, tl, 2)
    elif name == "steps":
        scene_steps(cr, t, tl)
    elif name == "end":
        scene_end(cr, t, tl)
    else:
        scene_office(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
