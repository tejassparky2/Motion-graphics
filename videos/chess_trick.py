"""Episode 20: "The Chess Trick" — an original school story (same class as Who Is Kevin?, The Excuses...).

Jake can barely play chess, but bets the two best players he won't lose to both. He plays them in two rooms, black
against one and white against the other, and copies each opponent's move onto the other board, so the champions are
really playing each other (the classic "simultaneous relay" trick). Result: one wins and one loses, or both draw, so
Jake can't lose both.

Retention design: challenge + stakes on screen in the first second; an open loop ("the trick is so simple you could do
it tomorrow"); constant motion (Jake runs between rooms, the camera follows); a mid-video reveal; a twist; and a
cliffhanger that sets up the next episode.
"""
import math

from motion.captions import captions
from motion.characters import cash, dollar, person
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, smooth, write)
from motion.kit import camera, confetti, enter_world, hl, set_camera, stamp, whip
from videos.backbencher import classroom, desk

NARRATOR = dict(speed=1.02)
TAIL = 0.8

SCRIPT = [
    dict(id="t1", scene="hall",
         text="Meet Jake. He can barely play chess. But he just bet the two best players in school, that he won't lose to both "
              "of them. At the same time."),
    dict(id="t2", scene="hall",
         text="[Twenty bucks.|$20.] Everyone laughs. But the trick is so simple, you could do it tomorrow."),
    dict(id="t3", scene="rooms",
         text="Two rooms. In room one, Emma plays white against Jake. In room two, Jake plays white against Tyler."),
    dict(id="t4", scene="rooms",
         text="Emma makes her first move. Jake walks to room two, and plays the exact same move against Tyler."),
    dict(id="t5", scene="rooms", text="Tyler answers. Jake walks back, and copies Tyler's move against Emma."),
    dict(id="t6", scene="reveal",
         text="See the trick? Jake isn't playing at all. Emma and Tyler are playing each other. Jake is just the "
              "messenger."),
    dict(id="t7", scene="reveal",
         text="So if Emma wins, Jake wins the other game. If they draw, Jake draws both. He can't lose both."),
    dict(id="t8", scene="twist",
         text="An hour later, Emma and Tyler compare their games. Move for move, they're identical.", gap=0.25),
    dict(id="t9", scene="twist", text="They've been playing each other the whole time.", pace=0.95),
    dict(id="t10", scene="end",
         text="And Jake? He's already walking to the teachers' lounge. Mr. Miller and the principal are next.",
         gap=0.25),
]

METADATA = dict(
    title="He Can't Play Chess… But He Can't Lose 🤯♟️",
    alt_titles=["The Chess Trick You Can Use Tomorrow ♟️", "How to Never Lose to 2 Chess Champions 😏"],
    description="""Jake can barely play chess. So he bet the two best players in school that he wouldn't lose to BOTH of them, at the same time. ♟️

Two rooms. White against one, black against the other… and the trick is so simple you could do it tomorrow. 😏

💬 Did you figure it out before the reveal? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#Chess", "#LifeHack", "#PlotTwist"],
    tags=["chess trick", "chess hack", "clever trick", "school story", "plot twist", "mind trick", "chess",
          "genius kid", "animated story", "interestingly strange"],
    pinned_comment="Would this trick work on you? 😏♟️ Who should Jake play next? 👇",
)

GOLD = hexc("#f2b632")
GREEN = hexc("#3d8f45")
BLUE = hexc("#3f6fb5")
PINK = hexc("#e0487a")
LIGHT, DARK = hexc("#f0dcb4"), hexc("#a8744a")
ROOM1, ROOM2 = 0, 1000          # world x of each room's centre
JAKE, EMMA, TYLER = "chotu", "kid_a", "kid_c"


def board(cr, x, y, size, moved, seed=0):
    """Chess board centred at (x, y). `moved` = {'e4': u, 'e5': u} slide progress for the two opening moves."""
    sq = size / 8
    x0, y0 = x - size / 2, y - size / 2
    shape(cr, rrect_pts(x0 - 10, y0 - 10, size + 20, size + 20, 6, 14), hexc("#6b4a2e"), seed=seed, amp=0.4, lw=4)
    for r in range(8):
        for c in range(8):
            cr.rectangle(x0 + c * sq, y0 + r * sq, sq, sq)
            cr.set_source_rgba(*(LIGHT if (r + c) % 2 == 0 else DARK))
            cr.fill()

    def piece(col_, row_, white, big=False):
        px, py = x0 + (col_ + 0.5) * sq, y0 + (row_ + 0.5) * sq
        blob(cr, px, py, sq * (0.36 if big else 0.28), sq * (0.36 if big else 0.28), WHITE if white else INK,
             seed=seed + int(col_ * 10 + row_), amp=0.2, lw=2, stroke=INK if white else hexc("#555a66"))
    for c in range(8):   # back ranks + pawns (e-pawns handled separately)
        piece(c, 7, True, big=True)
        piece(c, 0, False, big=True)
        if c != 4:
            piece(c, 6, True)
            piece(c, 1, False)
    u = smooth(moved.get("e4", 0))
    piece(4, lerp(6, 4, u), True)
    v = smooth(moved.get("e5", 0))
    piece(4, lerp(1, 3, v), False)


def room(cr, cx, label, col, t):
    shape(cr, rrect_pts(cx - 330, 380, 660, 520, 8, 20), hexc("#e6dcc8"), seed=17000 + cx, amp=0.6, lw=4)
    shape(cr, rrect_pts(cx - 120, 400, 240, 70, 10, 16), col, seed=17001 + cx, amp=0.5, lw=4)
    write(cr, [(label, WHITE)], cx, 448, 40, align="center", bold=True)
    shape(cr, rrect_pts(cx - 150, 790, 300, 110, 8, 16), hexc("#6d4524"), seed=17002 + cx, amp=0.6, lw=4)   # table


def moves_at(tl, t):
    A = tl.at
    e4_room1 = seg(t, A("t4", "first"), A("t4", "first") + 0.5)
    e4_room2 = seg(t, A("t4", "same"), A("t4", "same") + 0.5)
    e5_room2 = seg(t, A("t5", "answers"), A("t5", "answers") + 0.5)
    e5_room1 = seg(t, A("t5", "copies"), A("t5", "copies") + 0.5)
    return {"e4": e4_room1, "e5": e5_room1}, {"e4": e4_room2, "e5": e5_room2}


def jake_x(tl, t):
    A = tl.at
    x = ROOM1 + 120
    x = lerp(x, ROOM2 - 120, smooth(seg(t, A("t4", "walks"), A("t4", "plays"))))
    x = lerp(x, ROOM1 + 120, smooth(seg(t, A("t5", "walks"), A("t5", "copies"))))
    return x


def scene_hall(cr, t, tl):
    A = tl.at
    keys = [(0, (2.0, 560, 720)), (A("t1", "chess"), (1.4, 560, 740)), (A("t1", "bet"), (1.1, 450, 740)),
            (A("t1", "best"), (1.8, 330, 720)), (A("t1", "won't"), (2.1, 560, 720)), (A("t1", "same"), (1.0, 450, 760)),
            (A("t2", "$20"), (1.8, 450, 640)), (A("t2", "laughs"), (1.1, 450, 760)), (A("t2", "trick"), (1.9, 560, 700)),
            (A("t2", "tomorrow"), (1.3, 450, 700))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    classroom(cr, t)
    lol = A("t2", "laughs") <= t < A("t2", "but")
    for who, x in ((EMMA, 330), (TYLER, 450)):
        person(cr, who, x, 905, t, facing=1, arms=("hold", "hip"), eyes="closed" if lol else "sly",
               mouth="laugh" if lol else "smirk", jump=abs(math.sin(t * 9 + x)) * 8 if lol else 0)
        # champion medals
        blob(cr, x + 6, 905 - 26 - 60, 14, 14, GOLD, seed=17100 + x, amp=0.3, lw=2.5)
    person(cr, JAKE, 600, 905, t, facing=-1, arms=("thumb", "hip") if t >= A("t1", "bet") else ("hip", "hip"),
           eyes="sly", mouth="smirk")
    if t >= A("t2", "$20"):
        dollar(cr, 560, 760, 1.2, amount="$20", seed=17110)
    # the challenge card, on screen from the first frame
    cr.save()
    cr.identity_matrix()
    with at(cr, 360, 470, 1.2, rot=-0.04):
        shape(cr, rrect_pts(-250, -70, 500, 140, 16, 18), INK, seed=17120, amp=0.6, lw=0, stroke=None)
        write(cr, [("can't play chess", WHITE)], 0, -14, 40, align="center", bold=True)
        write(cr, [("vs ", WHITE), ("2 CHAMPIONS", GOLD)], 0, 40, 40, align="center", bold=True)
    cr.restore()
    hl(cr, t, [("won't lose to ", INK), ("BOTH", RED)], 215, 76, A("t1", "won't"), end=A("t2") - 0.05, bold=True)
    hl(cr, t, [("the trick: ", INK), ("SO simple", GREEN)], 215, 76, A("t2", "trick"), bold=True)
    if lol:
        write(cr, [("HA HA", RED)], 400, 640, 44, align="center", bold=True, halo=WHITE)


def scene_rooms(cr, t, tl):
    A = tl.at
    jx = jake_x(tl, t)
    running = (A("t4", "walks") <= t < A("t4", "plays")) or (A("t5", "walks") <= t < A("t5", "copies"))
    keys = [(A("t3") - 0.2, (0.95, 500, 680)), (A("t3", "one"), (1.2, ROOM1, 640)), (A("t3", "Emma"), (1.8, ROOM1 - 150, 720)),
            (A("t3", "two", nth=2), (1.2, ROOM2, 640)), (A("t3", "Tyler"), (1.8, ROOM2 + 150, 720)),
            (A("t4", "Emma"), (1.8, ROOM1, 760)), (A("t4", "first"), (2.4, ROOM1, 620))]
    board1, board2 = moves_at(tl, t)
    if running:
        z, fx, fy = 1.3, jx, 740
    else:
        z, fx, fy = camera(t, keys + [(A("t4", "plays"), (1.8, ROOM2, 700)), (A("t4", "same"), (2.4, ROOM2, 620)),
                                      (A("t5", "Tyler"), (1.8, ROOM2 + 150, 720)), (A("t5", "answers"), (2.4, ROOM2, 620)),
                                      (A("t5", "copies"), (2.4, ROOM1, 620)), (A("t5", "Emma"), (1.6, ROOM1 - 100, 720))],
                          dur=0.15)
    set_camera((z, fx, fy))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#c9b99a"))
    cr.paint()
    sharp_shape(cr, [(-900, 900), (2400, 890), (2400, 1900), (-900, 1900)], hexc("#8a8f99"), seed=17200, amp=1, lw=4)
    room(cr, ROOM1, "ROOM 1", PINK, t)
    room(cr, ROOM2, "ROOM 2", BLUE, t)
    shape(cr, rrect_pts(ROOM1 + 400, 600, 100, 300, 6, 14), hexc("#6b4a2e"), seed=17210, amp=0.5, lw=4)   # hallway door
    board(cr, ROOM1, 640, 220, board1, seed=17300)
    board(cr, ROOM2, 640, 220, board2, seed=17400)
    person(cr, EMMA, ROOM1 - 220, 905, t, facing=1, arms=("chin", "hip"), eyes="sly", mouth="flat")
    person(cr, TYLER, ROOM2 + 220, 905, t, facing=-1, arms=("chin", "hip"), eyes="sly", mouth="flat")
    person(cr, JAKE, jx, 905, t, facing=1 if jx < (ROOM1 + ROOM2) / 2 and running and t < A("t5") else -1,
           walk=t * 3.5 if running else None, arms=("hip", "hip"), eyes="sly", mouth="smirk")
    for key, nth, room_x, label in (("first", 1, ROOM1, "e4"), ("same", 1, ROOM2, "COPY"), ("answers", 1, ROOM2, "e5"),
                                    ("copies", 1, ROOM1, "PASTE")):
        tb = A("t4" if key in ("first", "same") else "t5", key)
        if tb <= t < tb + 0.8:
            write(cr, [(label, RED if label in ("COPY", "PASTE") else INK)], room_x, 490, 48, align="center", bold=True,
                  halo=WHITE)
            cue("pop", t, tb)
    # a move counter keeps the progress visible
    cr.save()
    cr.identity_matrix()
    n = (1 if t >= A("t4", "first") else 0) + (1 if t >= A("t5", "answers") else 0)
    shape(cr, rrect_pts(520, 320, 170, 60, 14, 14), INK, seed=17500, amp=0.4, lw=0, stroke=None)
    write(cr, [(f"MOVE {max(1, n)}", GOLD)], 605, 362, 30, align="center", bold=True)
    cr.restore()
    hl(cr, t, [("Emma: ", PINK), ("white", INK)], 215, 76, A("t3", "Emma"), end=A("t3", "two", nth=2) - 0.05, bold=True)
    hl(cr, t, [("Jake: ", RED), ("white", INK), (" vs Tyler", BLUE)], 215, 66, A("t3", "Tyler"), end=A("t4") - 0.05,
       bold=True)
    hl(cr, t, [("the ", INK), ("EXACT", RED), (" same move", INK)], 215, 70, A("t4", "exact"), end=A("t5") - 0.05, bold=True)
    hl(cr, t, [("copies ", INK), ("Tyler's", BLUE), (" move", INK)], 215, 70, A("t5", "copies"), bold=True)


def scene_reveal(cr, t, tl):
    A = tl.at
    keys = [(A("t6") - 0.2, (1.0, 360, 640)), (A("t6", "trick"), (1.3, 360, 600)), (A("t6", "isn't"), (1.5, 360, 620)),
            (A("t6", "Emma"), (1.3, 180, 640)), (A("t6", "Tyler"), (1.3, 540, 640)), (A("t6", "each"), (1.0, 360, 640)),
            (A("t6", "messenger"), (1.4, 360, 620)),
            (A("t7", "Emma"), (1.2, 360, 760)), (A("t7", "wins", nth=2), (1.5, 360, 820)), (A("t7", "draw"), (1.2, 360, 900)),
            (A("t7", "both"), (1.5, 360, 960)), (A("t7", "can't"), (1.0, 360, 760))]
    z, fx, fy = camera(t, keys, dur=0.15)
    cr.set_source_rgba(*hexc("#fbf3e1"))
    cr.paint()
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    # Emma <---- Jake (a pipe) ----> Tyler
    person(cr, EMMA, 110, 720, t, facing=1, scale=1.1, arms=("point", "hip"), eyes="sly", mouth="flat")
    person(cr, TYLER, 610, 720, t, facing=-1, scale=1.1, arms=("point", "hip"), eyes="sly", mouth="flat")
    shape(cr, rrect_pts(200, 550, 320, 60, 30, 16), hexc("#c7c2cc"), seed=17600, amp=0.4, lw=5)   # the pipe
    for k in range(4):   # moves travelling both ways
        u = (t * 0.8 + k / 4) % 1
        x = lerp(215, 505, u) if k % 2 == 0 else lerp(505, 215, u)
        dot(cr, x, 580, 16, WHITE if k % 2 == 0 else INK)
    person(cr, JAKE, 360, 740, t, facing=1, scale=1.1, arms=("hold", "hold"), eyes="happy", mouth="grin")
    write(cr, [("JAKE = messenger", RED)], 360, 470, 50, align="center", bold=True, halo=WHITE)
    if t >= A("t6", "each"):
        write(cr, [("Emma vs Tyler", INK)], 360, 400, 58, align="center", bold=True, halo=WHITE)
    # the outcome table
    if t >= A("t7"):
        rows = [("Emma wins", "Jake wins game 2", A("t7", "Emma")), ("Tyler wins", "Jake wins game 1", A("t7", "wins", nth=2)),
                ("draw", "Jake draws both", A("t7", "draw"))]
        for k, (a, b, tt) in enumerate(rows):
            sc = pop(t, tt, 0.2)
            if sc > 0:
                with at(cr, 360, 830 + k * 84, sc):
                    shape(cr, rrect_pts(-330, -34, 660, 68, 14, 14), WHITE, seed=17610 + k, amp=0.4, lw=3.5)
                    write(cr, [(a, INK), ("  =  ", INK), (b, GREEN)], 0, 13, 36, align="center", bold=True)
    hl(cr, t, [("see the ", INK), ("TRICK", RED), ("?", INK)], 215, 90, A("t6", "trick"), end=A("t6", "each") - 0.05,
       bold=True)
    hl(cr, t, [("they're playing ", INK), ("EACH OTHER", RED)], 215, 52, A("t6", "each"), end=A("t7") - 0.05, bold=True)
    hl(cr, t, [("he ", INK), ("CAN'T", RED), (" lose both", INK)], 215, 84, A("t7", "can't"), bold=True, underline=True)


def scene_twist(cr, t, tl):
    A = tl.at
    keys = [(A("t8") - 0.2, (1.0, 360, 700)), (A("t8", "hour"), (1.5, 560, 420)), (A("t8", "compare"), (1.2, 360, 660)),
            (A("t8", "move"), (1.8, 200, 620)), (A("t8", "identical"), (1.8, 520, 620)), (A("t9"), (1.1, 360, 700)),
            (A("t9", "each"), (1.9, 360, 740)), (A("t9", "whole"), (1.2, 360, 700))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    classroom(cr, t)
    full = {"e4": 1, "e5": 1}
    board(cr, 200, 640, 220, full, seed=17700)
    board(cr, 520, 640, 220, full, seed=17710)
    if t >= A("t8", "identical"):
        write(cr, [("=", RED)], 360, 670, 110, align="center", bold=True, halo=WHITE)
    shock = t >= A("t9")
    person(cr, EMMA, 170, 905, t, facing=1, eyes="wide" if shock else "sly", mouth="o" if shock else "flat",
           sweat=shock, arms=("face", "hip") if shock else ("point", "hip"))
    person(cr, TYLER, 550, 905, t, facing=-1, eyes="wide" if shock else "sly", mouth="o" if shock else "flat",
           sweat=shock, arms=("face", "hip") if shock else ("point", "hip"))
    cr.save()
    cr.identity_matrix()
    shape(cr, rrect_pts(470, 320, 220, 60, 14, 14), INK, seed=17720, amp=0.4, lw=0, stroke=None)
    write(cr, [("1 HOUR LATER", GOLD)], 580, 362, 28, align="center", bold=True)
    cr.restore()
    hl(cr, t, [("move for move: ", INK), ("IDENTICAL", RED)], 215, 60, A("t8", "identical"), end=A("t9") - 0.05, bold=True)
    if t >= A("t9", "each"):
        stamp(cr, t, A("t9", "each"), "PLAYING EACH OTHER", dur=1.1, y=470)


def scene_end(cr, t, tl):
    A = tl.at
    keys = [(A("t10") - 0.2, (1.6, 300, 740)), (A("t10", "walking"), (1.1, 420, 740)), (A("t10", "lounge"), (1.8, 620, 620)),
            (A("t10", "Miller"), (1.3, 500, 700)), (A("t10", "next"), (2.0, 300, 720))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    cr.set_source_rgba(*hexc("#c9b99a"))
    cr.paint()
    sharp_shape(cr, [(-900, 900), (2400, 890), (2400, 1900), (-900, 1900)], hexc("#8a8f99"), seed=17800, amp=1, lw=4)
    shape(cr, rrect_pts(540, 540, 170, 360, 6, 16), hexc("#6b4a2e"), seed=17810, amp=0.5, lw=4)
    shape(cr, rrect_pts(510, 470, 230, 56, 8, 14), WHITE, seed=17811, amp=0.4, lw=3)
    write(cr, [("TEACHERS' LOUNGE", INK)], 625, 508, 26, align="center", bold=True)
    walk = seg(t, A("t10", "walking"), A("t10", "lounge", end=True) + 0.4)
    x = lerp(160, 440, walk)
    person(cr, JAKE, x, 905, t, facing=1, walk=t * 3 if 0 < walk < 1 else None, arms=("hold", "hip"), eyes="sly",
           mouth="smirk")
    with at(cr, x + 60, 790, 0.35):
        board(cr, 0, 0, 220, {}, seed=17820)
    if t >= A("t10", "next"):
        cash(cr, x - 40, 700, 1.4, seed=17830)
    hl(cr, t, [("next: ", INK), ("the TEACHERS", RED)], 215, 76, A("t10", "Miller"), bold=True, underline=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hall": scene_hall, "rooms": scene_rooms, "reveal": scene_reveal, "twist": scene_twist, "end": scene_end}[name](
        cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
