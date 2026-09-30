"""Episode 9: "Hilbert's Infinite Hotel" — approved script B6 (out/scripts/weird_history_time_batch2.md).

Facts (Wikipedia, "Hilbert's paradox of the Grand Hotel"): introduced by David Hilbert in a 1924-25 lecture ("Über das
Unendliche"), popularised by George Gamow (1947). One new guest: everyone moves from room n to n+1. Infinitely many new
guests: everyone moves from n to 2n, freeing all the (infinitely many) odd rooms.
"""
import math

from motion.captions import captions
from motion.characters import briefcase, bubble, person
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, smooth, write)
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip

NARRATOR = dict(speed=1.02)
TAIL = 0.8

SCRIPT = [
    dict(id="h1", scene="outside", text="Imagine a hotel with [infinite rooms,|∞ rooms,] and every single one is full."),
    dict(id="h2", scene="lobby", text="A new guest shows up. Sorry, we're full?", speaker="host", speaker_from="Sorry"),
    dict(id="h2b", scene="lobby", text="Nope.", speaker="host", gap=0.22, pace=0.9),
    dict(id="h3", scene="hall",
         text="The manager asks everyone to move one room up. Room [one|1] goes to [two,|2,] [two|2] goes to [three,|3,] "
              "forever. Room [one|1] is now empty."),
    dict(id="h4", scene="bus", text="Then a bus shows up, with [infinite|∞] new guests.", gap=0.2),
    dict(id="h5", scene="hall2",
         text="Easy. Everyone moves to double their room number. [One|1] goes to [two,|2,] [two|2] to [four,|4,] "
              "[three|3] to [six.|6.] Now every odd-numbered room is free, and there are infinitely many of those."),
    dict(id="h6", scene="hilbert",
         text="A mathematician named David Hilbert came up with this about [a hundred years ago,|100 years ago,] "
              "to show that infinity doesn't behave like a normal number."),
    dict(id="h7", scene="end", text="So... how many rooms are left?", pace=0.95),
]

METADATA = dict(
    title="This Hotel Is FULL… But Always Has Room ∞🏨",
    alt_titles=["The Infinite Hotel Paradox Will Break Your Brain 🤯", "A Full Hotel That Fits Infinite Guests? 🏨"],
    description="""A hotel with infinite rooms, and every single one is full. A new guest shows up… and still gets a room. 🏨

Then a bus with INFINITE new guests arrives. Everyone moves to double their room number (1→2, 2→4, 3→6), and suddenly every odd-numbered room is free.

It's called Hilbert's Hotel, a thought experiment from mathematician David Hilbert (1924) showing that infinity doesn't behave like a normal number. ∞

💬 So… how many rooms are left? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Paradox", "#Infinity", "#Math"],
    tags=["hilbert's hotel", "infinite hotel paradox", "hilbert's paradox", "infinity", "paradox", "math paradox",
          "brain teaser", "mind blowing math", "math shorts", "interestingly strange"],
    pinned_comment="Bonus: what if INFINITELY many buses show up, each with infinite guests? (Yes, they still fit 🤯) 👇",
)

WALL = hexc("#f3d9a4")
CARPET = hexc("#b8325e")
DOOR = hexc("#8e5a2e")
GREEN = hexc("#3d8f45")
NEON = hexc("#ff4f8b")
GOLD = hexc("#f2b632")
BLUE = hexc("#3f6fb5")
SKY = hexc("#23346b")
GUESTS = ["sam", "mia", "farmer", "oldman", "kid_a", "kid_b", "owner", "kid_c", "teacher", "soldier", "chotu", "claimant"]
DX = 210                # distance between doors in the hall
N = 32                  # doors we actually draw


def door_x(n):
    return 140 + (n - 1) * DX


# ------------------------------------------------------------------ outside (hook + loop ending)
def hotel_outside(cr, t, full_at, neon_on=True):
    cr.set_source_rgba(*SKY)
    cr.paint()
    for k in range(40):   # stars
        dot(cr, (k * 173) % 1400 - 300, (k * 311) % 4600 - 3800, 2.5 + (k % 3), hexc("#fff3c4", 0.5 + 0.5 * math.sin(t * 3 + k)))
    sharp_shape(cr, [(-900, 900), (1700, 890), (1700, 1900), (-900, 1900)], hexc("#4a4f63"), seed=6001, amp=1, lw=4)
    # the tower never ends: floors run up past the top of any shot
    shape(cr, [(150, 900), (150, -4000), (570, -4000), (570, 900)], hexc("#e9dcc0"), seed=6002, amp=1.2, lw=5)
    for f in range(38):
        y = 820 - f * 130
        for c in range(4):
            x = 190 + c * 96
            k = f * 4 + c
            lit = t >= full_at + (k % 17) * 0.025
            shape(cr, rrect_pts(x, y - 80, 70, 84, 6, 12), hexc("#ffe28a") if lit else hexc("#39406b"), seed=6010 + k,
                  amp=0.5, lw=3)
            if lit:   # someone's home
                col = [hexc("#e0487a"), BLUE, GREEN, hexc("#ff8a3d"), hexc("#6a45b5")][k % 5]
                blob(cr, x + 35, y - 30, 16, 16, hexc("#2a2230", 0.85), seed=6200 + k, amp=0.5, lw=0, stroke=None)
                blob(cr, x + 35, y + 2, 24, 14, col, seed=6300 + k, amp=0.5, lw=0, stroke=None)
    # entrance + neon
    shape(cr, rrect_pts(310, 780, 100, 120, 10, 14), DOOR, seed=6003, amp=0.6, lw=4)
    shape(cr, rrect_pts(170, 640, 380, 110, 16, 18), INK, seed=6004, amp=0.8, lw=4)
    glow = 0.6 + 0.4 * math.sin(t * 9) if neon_on else 1
    write(cr, [("HOTEL ", hexc("#fff3c4")), ("∞", hexc("#ff4f8b", glow))], 360, 718, 70, align="center", bold=True)
    if t >= full_at:   # the NO VACANCY sign flickers on
        on = 1 if int(t * 5) % 4 else 0.45
        shape(cr, rrect_pts(470, 540, 230, 80, 12, 16), hexc("#3a1020"), seed=6005, amp=0.6, lw=4)
        write(cr, [("NO VACANCY", hexc("#ff4f4f", on))], 585, 594, 36, align="center", bold=True)


def scene_outside(cr, t, tl, end=False):
    A = tl.at
    if not end:
        full = A("h1", "full")
        keys = [(0, (1.3, 360, 700)), (A("h1", "hotel"), (1.0, 360, 620)), (A("h1", "infinite"), (0.55, 360, -300)),
                (A("h1", "every"), (0.8, 360, 300)), (A("h1", "full"), (1.25, 480, 620))]
    else:
        full = -1
        keys = [(A("h7") - 0.2, (1.25, 480, 640)), (A("h7", "how"), (0.9, 360, 560)), (A("h7", "rooms"), (0.6, 360, -100)),
                (A("h7", "left"), (1.2, 360, 680))]
    set_camera(camera(t, keys, dur=0.35 if not end else 0.25))
    enter_world(cr)
    hotel_outside(cr, t, full)
    if not end:
        hl(cr, t, [("∞", NEON), (" rooms", INK)], 215, 90, A("h1", "infinite"), end=A("h1", "full") - 0.05, bold=True)
        hl(cr, t, [("ALL ", INK), ("FULL", RED)], 215, 90, A("h1", "full"), bold=True)
        cue("hit", t, A("h1", "full"))
    else:
        hl(cr, t, [("how many rooms ", INK), ("left", NEON), ("?", INK)], 215, 64, A("h7", "how"), bold=True, underline=True)


# ------------------------------------------------------------------ lobby
def scene_lobby(cr, t, tl):
    A = tl.at
    keys = [(A("h2") - 0.2, (1.2, 400, 740)), (A("h2", "guest"), (1.7, 560, 740)), (A("h2", "Sorry"), (1.8, 230, 700)),
            (A("h2b"), (1.3, 360, 720))]
    set_camera(camera(t, keys, dur=0.2))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#e6c07b"))
    cr.paint()
    for k in range(-4, 14):
        line(cr, [(k * 80, 250), (k * 80, 900)], 3, hexc("#d6ac64"), seed=6400 + k, amp=0.6)
    sharp_shape(cr, [(-800, 900), (1600, 890), (1600, 1900), (-800, 1900)], CARPET, seed=6401, amp=1, lw=4)
    # key board behind the desk: every hook taken
    shape(cr, rrect_pts(60, 430, 320, 170, 8, 18), DOOR, seed=6402, amp=0.6, lw=4)
    for k in range(12):
        x, y = 90 + (k % 6) * 50, 470 + (k // 6) * 70
        dot(cr, x, y, 4, GOLD)
        write(cr, [("-", INK)], x - 2, y + 30, 26, bold=True)
    write(cr, [("...∞", GOLD)], 220, 588, 28, align="center", bold=True)
    person(cr, "host", 220, 900, t, facing=1,
           arms=("point", "hip") if t >= A("h2b") else (("hip", "hip") if t < A("h2", "Sorry") else ("chin", "hip")),
           eyes="happy" if t >= A("h2b") else "dot",
           mouth=("o" if int(t * 12) % 2 else "smile") if tl.speaking("host", t) else "smile")
    shape(cr, rrect_pts(40, 810, 360, 100, 10, 18), hexc("#6d4524"), seed=6403, amp=0.8, lw=4.5)   # desk
    write(cr, [("RECEPTION", GOLD)], 220, 872, 34, align="center", bold=True)
    blob(cr, 330, 802, 18, 12, GOLD, seed=6404, amp=0.4, lw=3)   # bell
    # the new guest walks in with a suitcase
    walk = seg(t, A("h2"), A("h2", "up", end=True))
    gx = lerp(780, 520, ease_out(walk))
    person(cr, "mia", gx, 900, t, facing=-1, walk=t * 2.6 if 0 < walk < 1 else None, arms=("hold", "down"),
           eyes="wide" if A("h2", "Sorry") <= t < A("h2b") else "happy", mouth="o" if t < A("h2b") else "grin")
    briefcase(cr, gx + 30, 860, seed=6405)
    if A("h2", "Sorry") <= t:
        s = pop(t, A("h2", "Sorry"), 0.2)
        bubble(cr, 250, 540, 300, 100, (220, 700), [("Sorry, full?", INK)], s=s, size=40)
        if t >= A("h2b"):
            with at(cr, 250, 540, 1.0, rot=-0.1):
                line(cr, [(-130, -40), (130, 40)], 9, RED, seed=6410, amp=0.5)
    if t >= A("h2b"):
        stamp(cr, t, A("h2b"), "NOPE!", dur=0.7, y=420)
    hl(cr, t, [("+1 ", GREEN), ("new guest", INK)], 215, 70, A("h2", "guest"), end=A("h2", "Sorry") - 0.05, bold=True)


# ------------------------------------------------------------------ the corridor
def corridor(cr, t, vacant=()):
    cr.set_source_rgba(*WALL)
    cr.paint()
    sharp_shape(cr, [(-800, 900), (N * DX + 1200, 890), (N * DX + 1200, 1900), (-800, 1900)], CARPET, seed=6500, amp=1,
                lw=4)
    for k in range(-2, N * 2 + 8):   # carpet diamonds, so pans read
        x = k * 105
        shape(cr, [(x, 960), (x + 26, 990), (x, 1020), (x - 26, 990)], GOLD, seed=6510 + k, amp=0.3, lw=2.5)
    for n in range(1, N + 1):
        x = door_x(n)
        free = n in vacant
        shape(cr, rrect_pts(x - 60, 640, 120, 260, 8, 18), GREEN if free else DOOR, seed=6600 + n, amp=0.6, lw=4)
        dot(cr, x + 40, 780, 6, GOLD)
        shape(cr, rrect_pts(x - 36, 572, 72, 50, 8, 12), WHITE, seed=6700 + n, amp=0.4, lw=3)
        write(cr, [(str(n), INK)], x, 612, 38, align="center", bold=True)
        if free:
            write(cr, [("FREE", WHITE)], x, 720, 34, align="center", bold=True)
        # wall lamp between doors
        blob(cr, x + DX / 2, 560, 14, 18, hexc("#ffe28a"), seed=6800 + n, amp=0.4, lw=3)
    write(cr, [("...", INK)], door_x(N) + 160, 780, 120, bold=True)


def guest(cr, i, x, y, t, happy=True, lift=0.0):
    person(cr, GUESTS[i % len(GUESTS)], x, y, t, facing=-1 if i % 2 else 1, scale=0.62, jump=lift,
           eyes="happy" if happy else "dot", mouth="grin" if lift > 0 else "smile")


def hop(cr, t, i, n0, n1, t0, dur=0.45):
    u = seg(t, t0, t0 + dur)
    x = lerp(door_x(n0), door_x(n1), smooth(u))
    lift = math.sin(u * math.pi) * (60 + 18 * abs(n1 - n0) ** 0.8)
    guest(cr, i, x, 905, t, lift=lift)
    if 0 < u < 1:
        cue("whoosh", t, t0, 0.2)


def arrow(cr, n0, n1, y, col, seed):
    x0, x1 = door_x(n0), door_x(n1)
    h = 60 + 22 * abs(n1 - n0)
    pts = [(x0 + (x1 - x0) * k / 10, y - math.sin(k / 10 * math.pi) * h) for k in range(11)]
    line(cr, pts, 6, col, seed=seed, amp=0.5)
    line(cr, [(x1 - 22, y - 22), (x1, y), (x1 + 6, y - 30)], 6, col, seed=seed + 1, amp=0.3)


def scene_hall(cr, t, tl):
    A = tl.at
    move = A("h3", "move")
    t1, t2, tf = A("h3", "goes"), A("h3", "goes", nth=2), A("h3", "forever")
    empty = A("h3", "empty")
    keys = [(A("h3") - 0.2, (0.8, 560, 760)), (A("h3", "manager"), (1.4, 300, 760)), (A("h3", "asks"), (1.9, door_x(1) - 140, 800)),
            (A("h3", "everyone"), (0.7, 700, 760)), (move, (1.4, door_x(3), 820)), (A("h3", "up"), (0.55, 900, 760)),
            (A("h3", "room", nth=2), (1.2, door_x(1) + 110, 760)), (t2, (1.2, door_x(2) + 110, 760)),
            (tf, (0.45, 2600, 760)), (A("h3", "room", nth=3), (1.0, door_x(1) + 80, 760)), (empty, (1.5, door_x(1), 760))]
    set_camera(camera(t, keys, dur=0.18))
    enter_world(cr)
    corridor(cr, t, vacant=(1,) if t >= empty else ())
    for i in range(N):
        n = i + 1
        t0 = t1 if n == 1 else (t2 if n == 2 else tf + (n % 5) * 0.03)
        hop(cr, t, i, n, n + 1, t0)
    # the manager, calling it out
    if t < tf:
        person(cr, "host", door_x(1) - 150, 905, t, facing=1, scale=0.7, arms=("cheer", "hip") if t >= move else ("hip", "hip"),
               mouth="o" if int(t * 10) % 2 and t >= A("h3", "manager") else "smile")
    if t1 <= t < tf:
        arrow(cr, 1, 2, 520, RED, 6900)
    if t2 <= t < tf:
        arrow(cr, 2, 3, 520, RED, 6910)
    if t >= empty:
        cue("kaching", t, empty)
    hl(cr, t, [("everyone: ", INK), ("+1 room", RED)], 215, 70, move, end=A("h3", "room", nth=2) - 0.05, bold=True)
    hl(cr, t, [("every room: ", INK), ("n+1", RED)], 215, 80, A("h3", "room", nth=2), end=empty - 0.05, bold=True)
    hl(cr, t, [("room 1: ", INK), ("EMPTY", GREEN)], 215, 84, empty, bold=True, underline=True)


def scene_bus(cr, t, tl):
    A = tl.at
    arrive = seg(t, A("h4") - 0.1, A("h4", "bus", end=True) + 0.2)
    keys = [(A("h4") - 0.2, (0.9, 360, 740)), (A("h4", "bus"), (1.2, 300, 720)), (A("h4", "infinite"), (0.4, 1600, 700)),
            (A("h4", "guests"), (1.0, 360, 700))]
    set_camera(camera(t, keys, dur=0.2))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#8fd0f0"))
    cr.paint()
    sharp_shape(cr, [(-1600, 900), (6000, 890), (6000, 1900), (-1600, 1900)], hexc("#555a66"), seed=7000, amp=1, lw=4)
    for k in range(-10, 60):
        line(cr, [(k * 120, 1000), (k * 120 + 60, 1000)], 6, WHITE, seed=7001 + k, amp=0.3)
    cr.save()
    cr.translate(lerp(900, 0, ease_out(arrive)), 0)
    # the bus that never ends
    shape(cr, rrect_pts(60, 560, 5200, 330, 30, 30), hexc("#ffc93c"), seed=7100, amp=1.2, lw=5)
    shape(cr, rrect_pts(60, 580, 90, 150, 12, 14), hexc("#bfe6ef"), seed=7101, amp=0.5, lw=3.5)   # windscreen
    for k in range(34):
        x = 180 + k * 150
        shape(cr, rrect_pts(x, 600, 120, 110, 10, 14), hexc("#bfe6ef"), seed=7110 + k, amp=0.5, lw=3.5)
        for j in range(2):   # packed: two faces a window
            col = [hexc("#f0c29c"), hexc("#b9794a"), hexc("#d9975f")][(k + j) % 3]
            blob(cr, x + 34 + j * 52, 660 + math.sin(t * 6 + k + j) * 3, 20, 20, col, seed=7200 + k * 2 + j, amp=0.5, lw=3)
            line(cr, [(x + 26 + j * 52, 664), (x + 34 + j * 52, 670), (x + 42 + j * 52, 664)], 2.5, INK, seed=7300 + k * 2 + j,
                 amp=0.2)
    line(cr, [(60, 780), (5260, 780)], 8, hexc("#e0487a"), seed=7102, amp=0.8)
    write(cr, [("∞", hexc("#e0487a"))], 700, 870, 90, bold=True, halo=WHITE)
    for wx in (250, 900, 1800, 2700, 3600, 4500):
        blob(cr, wx, 900, 50, 50, hexc("#2a2230"), seed=7400 + wx, amp=0.6, lw=4)
        blob(cr, wx, 900, 20, 20, hexc("#a9a2ae"), seed=7401 + wx, amp=0.3, lw=3)
    cr.restore()
    hl(cr, t, [("a BUS", INK)], 215, 90, A("h4", "bus"), end=A("h4", "infinite") - 0.05, bold=True)
    hl(cr, t, [("∞", NEON), (" new guests", INK)], 215, 80, A("h4", "infinite"), bold=True)
    cue("engine", t, A("h4"), 1.0)


def scene_hall2(cr, t, tl):
    A = tl.at
    t1, t2, t3 = A("h5", "1"), A("h5", "2", nth=2), A("h5", "3")
    tn = A("h5", "now")
    odd = A("h5", "odd")
    keys = [(A("h5") - 0.2, (0.9, 500, 760)), (A("h5", "double"), (0.6, 900, 760)), (t1, (1.1, door_x(1) + 110, 760)),
            (t2, (0.95, door_x(3), 760)), (t3, (0.75, door_x(4) + 60, 760)), (tn, (0.5, 1500, 760)),
            (odd, (0.75, door_x(3), 760)), (A("h5", "free"), (1.0, door_x(2), 760)),
            (A("h5", "infinitely"), (0.32, 3000, 760))]
    set_camera(camera(t, keys, dur=0.18))
    enter_world(cr)
    free = [n for n in range(1, N + 1, 2)]
    lit = seg(t, odd, odd + 0.6)
    corridor(cr, t, vacant=[n for n in free if lit > 0 and n <= 1 + lit * N])
    for i in range(N):
        n = i + 1
        t0 = t1 if n == 1 else t2 if n == 2 else t3 if n == 3 else tn + (n % 6) * 0.04
        hop(cr, t, i, n, 2 * n, t0, dur=0.5 if n <= 3 else 0.6)
    for k, (n0, tt) in enumerate(((1, t1), (2, t2), (3, t3))):
        if tt <= t < tn + 0.4:
            arrow(cr, n0, 2 * n0, 520 - k * 40, [RED, BLUE, GREEN][k], 7500 + k * 10)
    hl(cr, t, [("every room: ", INK), ("2n", RED)], 215, 96, A("h5", "double"), end=odd - 0.05, bold=True)
    hl(cr, t, [("every ", INK), ("ODD", GREEN), (" room free", INK)], 215, 66, odd, end=A("h5", "infinitely") - 0.05, bold=True)
    hl(cr, t, [("∞", NEON), (" free rooms", GREEN)], 215, 80, A("h5", "infinitely"), bold=True, underline=True)
    if t >= odd:
        cue("kaching", t, odd)


# ------------------------------------------------------------------ Hilbert
def scene_hilbert(cr, t, tl):
    A = tl.at
    keys = [(A("h6") - 0.2, (1.1, 360, 720)), (A("h6", "David"), (1.8, 200, 720)), (A("h6", "100"), (1.2, 400, 640)),
            (A("h6", "show"), (1.0, 380, 680)), (A("h6", "infinity"), (1.5, 470, 560)), (A("h6", "normal"), (1.1, 380, 680))]
    set_camera(camera(t, keys, dur=0.2))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#e9d3ae"))
    cr.paint()
    sharp_shape(cr, [(-800, 900), (1600, 890), (1600, 1900), (-800, 1900)], hexc("#b98a5a"), seed=7600, amp=1, lw=4)
    shape(cr, rrect_pts(250, 380, 470, 330, 8, 20), DOOR, seed=7601, amp=0.8, lw=4)
    shape(cr, rrect_pts(266, 396, 438, 298, 6, 20), hexc("#2f5b46"), seed=7602, amp=0.6, lw=3)
    chalk = hexc("#f4f1e6")
    rows = [("∞ + 1 = ∞", "show"), ("∞ × 2 = ∞", "infinity"), ("normal? NO.", "normal")]
    for k, (txt, key) in enumerate(rows):
        u = seg(t, A("h6", key), A("h6", key) + 0.35)
        if u > 0:
            write(cr, [(txt, chalk if k < 2 else hexc("#f7d774"))], 290, 470 + k * 90, 62, progress=u, bold=True)
            cue("scribble", t, A("h6", key), 0.35)
    person(cr, "hilbert", 170, 900, t, facing=1, arms=("point", "hip") if t >= A("h6", "show") else ("chin", "hip"),
           eyes="sly" if t >= A("h6", "infinity") else "dot", mouth="smirk" if t >= A("h6", "show") else "smile")
    # a calendar counting back a century
    if t >= A("h6", "100"):
        yr = int(lerp(2024, 1924, ease_out(seg(t, A("h6", "100"), A("h6", "100", end=True) + 0.3))))
        shape(cr, rrect_pts(40, 420, 170, 130, 8, 16), WHITE, seed=7603, amp=0.6, lw=4)
        shape(cr, rrect_pts(40, 420, 170, 34, 8, 16), RED, seed=7604, amp=0.5, lw=3)
        write(cr, [(str(yr), INK)], 125, 528, 56, align="center", bold=True)
    hl(cr, t, [("David ", INK), ("Hilbert", BLUE)], 215, 80, A("h6", "David"), end=A("h6", "100") - 0.05, bold=True)
    hl(cr, t, [("~100", RED), (" years ago", INK)], 215, 76, A("h6", "100"), end=A("h6", "infinity") - 0.05, bold=True)
    hl(cr, t, [("∞", NEON), (" isn't a normal number", INK)], 215, 54, A("h6", "infinity"), bold=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "outside":
        scene_outside(cr, t, tl)
    elif name == "lobby":
        scene_lobby(cr, t, tl)
    elif name == "hall":
        scene_hall(cr, t, tl)
    elif name == "bus":
        scene_bus(cr, t, tl)
    elif name == "hall2":
        scene_hall2(cr, t, tl)
    elif name == "hilbert":
        scene_hilbert(cr, t, tl)
    else:
        scene_outside(cr, t, tl, end=True)
    cr.restore()
    captions(cr, t, tl)
