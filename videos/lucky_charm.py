"""Episode 2: "The $5 Lucky Charm" — an original story.

A broke guy asks his gorgeous wife why she married him. Five years ago he gave a beggar $5; the beggar bought a
lottery ticket and won $10 million. Twist: the ex-beggar pays her $5,000 a month to keep the husband happy, because
he's convinced the husband is his lucky charm... and he's watching through the window.

Built on the same pacing rules as episode 1 (continuous narration, a visual change about every second, numbers
written on the spoken word, question hook, loop ending).
"""
import math

from motion import characters as ch
from motion.captions import captions
from motion.characters import binoculars, dollar, person, phone, ticket
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, confetti, enter_world, fly, hl, sepia, set_camera, stamp, whip

NARRATOR = dict()   # channel default narrator (see motion/voice.py)

SCRIPT = [
    dict(id="h1", scene="home", text="Why would a woman this gorgeous marry a broke guy like him?"),
    dict(id="h2", scene="home", text="One night, he finally asks her: babe, be honest. Why me?",
         speaker="sam", speaker_from="babe"),
    dict(id="b1", scene="home", text="She smiles, and pulls out her phone."),
    dict(id="b2", scene="phone", text="It's a photo of a beggar. Remember him?"),
    dict(id="b3", scene="street", text="Five years ago, this guy gave that exact beggar [five bucks.|$5.]", gap=0.25),
    dict(id="b4", scene="lotto", text="The beggar spent it on one lottery ticket, and won [ten million dollars.|$10,000,000.]"),
    dict(id="b5", scene="home2", text="So he goes: wait. You're his daughter? You married me to say thanks?",
         speaker="sam", speaker_from="wait", gap=0.25),
    dict(id="b6", scene="home2", text="She laughs. Nope. He pays me [five grand|$5,000] a month, to keep you happy.",
         speaker="mia", speaker_from="Nope", pace=0.95),
    dict(id="b7", scene="home2", text="He thinks you're his lucky charm. The day you stop smiling, his luck runs out.",
         speaker="mia", speaker_from="He"),
    dict(id="b8", scene="home2", text="And right now, he's watching.", pace=0.92, gap=0.25),
    dict(id="b9", scene="home2", text="So, whatever you do, never ask your wife why she married you."),
]

METADATA = dict(
    title="Why Would She Marry Him? The $5 Twist 😳",
    alt_titles=["He Gave a Beggar $5… His Wife Explains Everything 😳",
                "The $5 Lucky Charm 🍀 Never Ask Your Wife This"],
    description="""He's broke. She's gorgeous. So one night he finally asks her: why me? 😳

She pulls out her phone… and shows him a beggar he gave $5 to, five years ago. What happened to that $5 is the strangest lucky-charm story you'll hear today. 🍀

💬 Be honest: would YOU keep taking the $5,000 a month? 😂

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#PlotTwist", "#Storytime", "#Animation"],
    tags=["plot twist", "storytime", "funny story", "animated story", "lottery winner story", "lucky charm",
          "karma story", "kindness pays off", "short story animation", "relationship humor", "interestingly strange"],
    pinned_comment="Would you keep taking the $5,000 a month? 😂 Yes or no 👇",
)

# ---------------------------------------------------------------- layout (world units)
FEET = 870
SAM_X, MIA_X = 290, 480
PINK = hexc("#e0487a")
BLUE = hexc("#3f6fb5")
GREEN = hexc("#3d8f45")
WALL = hexc("#f1dfbd")
FLOOR = hexc("#c8976a")

WIDE = (1.45, 385, 700)
HOOK = (1.5, 385, 700)
P_SAM = (1.9, 300, 715)
P_MIA = (1.9, 470, 712)
WINDOW = (2.3, 145, 530)


def _mouth(tl, who, t, rest):
    return ("o" if int(t * 12) % 2 else "smile") if tl.speaking(who, t) else rest


# ---------------------------------------------------------------- sets
def living_room(cr, t, outside=None):
    cr.set_source_rgba(*WALL)
    cr.paint()
    for i in range(-2, 12):   # wallpaper stripes
        x = i * 90
        sharp_shape(cr, [(x, 300), (x + 40, 300), (x + 40, 820), (x, 820)], hexc("#ead3a8"), seed=400 + i, amp=0.6,
                    lw=0, stroke=None)
    sharp_shape(cr, [(-700, 805), (1500, 805), (1500, 1600), (-700, 1600)], FLOOR, seed=401, amp=0.8, lw=4)
    for i in range(8):
        line(cr, [(-600 + i * 260, 830), (-500 + i * 260, 1300)], 3, hexc("#a8784f"), seed=402 + i, amp=1.0)
    # window (night outside)
    shape(cr, rrect_pts(30, 390, 230, 270, 12, 18), hexc("#6b4a2e"), seed=410, amp=0.6, lw=4)
    cr.save()
    cr.rectangle(46, 406, 198, 238)
    cr.clip()
    cr.set_source_rgba(*hexc("#1f2a52"))
    cr.paint()
    blob(cr, 200, 450, 22, 22, hexc("#fff3c4"), seed=411, amp=0.5, lw=2.5)
    for i, (sx, sy) in enumerate([(80, 440), (130, 470), (170, 420), (95, 520)]):
        dot(cr, sx, sy, 3, hexc("#fff3c4"))
    line(cr, [(215, 660), (215, 540)], 6, hexc("#555a66"), seed=412, amp=0.3)   # street lamp
    blob(cr, 215, 536, 12, 8, hexc("#ffe28a"), seed=413, amp=0.3, lw=2.5)
    if outside:
        outside(cr)
    cr.restore()
    line(cr, [(145, 406), (145, 644)], 6, hexc("#6b4a2e"), seed=414, amp=0.3)
    line(cr, [(46, 525), (244, 525)], 6, hexc("#6b4a2e"), seed=415, amp=0.3)
    for cx0 in (18, 240):   # curtains
        shape(cr, [(cx0, 380), (cx0 + 34, 380), (cx0 + 40, 680), (cx0 - 4, 680)], hexc("#c0504d"), seed=416 + cx0,
              amp=1.0, lw=3.5)
    # framed picture: a tiny pumpkin, a nod to episode 1
    shape(cr, rrect_pts(330, 420, 120, 100, 6, 16), hexc("#8e4a1e"), seed=420, amp=0.5, lw=4)
    sharp_shape(cr, [(342, 432), (438, 432), (438, 508), (342, 508)], hexc("#fff3c4"), seed=421, amp=0.4, lw=2.5)
    ch.pumpkin(cr, 390, 500, 20, seed=422)
    # floor lamp
    line(cr, [(700, 590), (700, 860)], 7, INK, seed=430, amp=0.3)
    shape(cr, [(655, 590), (745, 590), (725, 530), (675, 530)], hexc("#ffd23f"), seed=431, amp=0.6, lw=3.5)
    blob(cr, 700, 865, 34, 8, INK, seed=432, amp=0.3, lw=0, stroke=None)


def couch_back(cr):
    shape(cr, rrect_pts(110, 640, 540, 180, 40, 22), hexc("#2f7f86"), seed=440, amp=1.0, lw=4)
    for x0 in (120, 390):
        shape(cr, rrect_pts(x0, 660, 250, 120, 30, 20), hexc("#3a939b"), seed=441 + x0, amp=0.8, lw=3)


def couch_front(cr):
    shape(cr, rrect_pts(100, 800, 560, 90, 22, 22), hexc("#2a6f75"), seed=450, amp=1.0, lw=4)
    for x0 in (72, 630):
        shape(cr, rrect_pts(x0, 720, 64, 180, 26, 16), hexc("#2f7f86"), seed=451 + x0, amp=0.8, lw=4)
    for x0 in (130, 630):
        line(cr, [(x0, 890), (x0 + 6, 915)], 7, INK, seed=452 + x0, amp=0.3)


def street(cr, t):
    cr.set_source_rgba(*hexc("#b5553c"))
    cr.paint()
    for row in range(14):
        y = 300 + row * 40
        off = 40 if row % 2 else 0
        line(cr, [(-600, y), (1400, y)], 2.5, hexc("#8c3f2b"), seed=500 + row, amp=0.8)
        for k in range(-8, 18):
            x = k * 80 + off
            line(cr, [(x, y), (x, y + 40)], 2.5, hexc("#8c3f2b"), seed=520 + row * 30 + k, amp=0.5)
    sharp_shape(cr, [(-700, 830), (1500, 830), (1500, 1600), (-700, 1600)], hexc("#9a958a"), seed=560, amp=0.8, lw=4)
    line(cr, [(-700, 870), (1500, 870)], 3, hexc("#7b776d"), seed=561, amp=1.0)
    line(cr, [(90, 840), (90, 380)], 9, INK, seed=562, amp=0.3)   # lamp post
    shape(cr, [(60, 380), (120, 380), (110, 340), (70, 340)], hexc("#555a66"), seed=563, amp=0.4, lw=3.5)


def kiosk(cr, t, jackpot_at):
    cr.set_source_rgba(*hexc("#3f6fb5"))
    cr.paint()
    sharp_shape(cr, [(-700, 830), (1500, 830), (1500, 1600), (-700, 1600)], hexc("#9a958a"), seed=600, amp=0.8, lw=4)
    shape(cr, rrect_pts(390, 450, 290, 90, 14, 18), RED, seed=601, amp=0.8)
    write(cr, [("LOTTO", WHITE)], 535, 515, 64, align="center", bold=True)
    shape(cr, rrect_pts(410, 560, 250, 110, 10, 18), hexc("#1d1b24"), seed=602, amp=0.6)
    if t < jackpot_at:
        write(cr, [("JACKPOT", hexc("#ffd23f"))], 535, 630, 44, align="center", bold=True)
    else:
        on = int((t - jackpot_at) * 8) % 2 == 0
        write(cr, [("$10,000,000", hexc("#ffd23f") if on else hexc("#ff8a3d"))], 535, 632, 40, align="center",
              bold=True)
    sharp_shape(cr, [(380, 700), (690, 700), (690, 850), (380, 850)], hexc("#d9a15a"), seed=603, amp=0.8, lw=4)
    line(cr, [(380, 740), (690, 740)], 3, hexc("#8e4a1e"), seed=604, amp=0.6)


# ---------------------------------------------------------------- scenes
def scene_home(cr, t, tl, part2=False):
    A = tl.at
    if not part2:
        keys = [(0, HOOK), (A("h1", "broke"), (1.75, 330, 712)), (A("h2"), WIDE), (A("h2", "babe"), P_SAM),
                (A("b1"), P_MIA)]
        z, fx, fy = camera(t, keys)
        if t < A("h1", "broke"):
            z += 0.05 * seg(t, 0, A("h1", "broke"))   # slow push so frame 0 already moves
    else:
        keys = [(A("b5") - 0.2, P_SAM), (A("b5", "daughter"), (2.1, 300, 710)), (A("b5", "married"), P_MIA),
                (A("b5", "thanks"), (1.6, 385, 705)), (A("b6"), P_MIA), (A("b6", "Nope"), (2.1, 470, 705)),
                (A("b6", "$5,000"), WIDE), (A("b6", "happy"), P_SAM), (A("b7", "lucky"), P_SAM),
                (A("b7", "stop"), P_MIA), (A("b7", "luck"), (2.0, 300, 712)), (A("b8"), WINDOW), (A("b9"), WIDE),
                (A("b9", "never"), HOOK)]
        z, fx, fy = camera(t, keys, dur=0.35)
    set_camera((z, fx, fy))
    enter_world(cr)

    watching = part2 and A("b8") - 0.1 <= t
    def outside(cr):
        if watching:
            blob(cr, 150, 560, 110, 120, hexc("#ffe28a", 0.55), seed=460, amp=0.8, lw=0, stroke=None)  # lamp glow
            person(cr, "richbeggar", 140, 700, t, facing=1, arms=("face", "thumb"), item="binoculars", mouth="grin",
                   scale=0.95)
    living_room(cr, t, outside=outside)
    couch_back(cr)

    # --- Sam
    s = dict(facing=1, arms=("hip", "down"), eyes="dot", mouth="smile")
    if not part2:
        if A("h1", "broke") <= t < A("h2"):
            s.update(eyes="happy", mouth="grin")
        if t >= A("h2", "babe"):
            s.update(arms=("point", "down"), eyes="wide")
        if t >= A("b1"):
            s.update(arms=("hip", "down"), eyes="wide", mouth="o")
    else:
        s.update(eyes="wide", mouth="o", arms=("point", "down"))
        if t >= A("b6", "Nope"):
            s.update(arms=("hip", "down"), mouth="flat", sweat=True)
        if t >= A("b7", "stop"):
            s.update(mouth="grin", eyes="happy", sweat=True)   # forced smile
        if t >= A("b8"):
            s.update(facing=-1, eyes="wide", mouth="grin", sweat=True, shake=1.0)
        if t >= A("b9", "never"):
            s.update(facing=1)
    s["mouth"] = _mouth(tl, "sam", t, s["mouth"])
    person(cr, "sam", SAM_X, FEET, t, **s)

    # --- Mia
    m = dict(facing=-1, arms=("hip", "down"), eyes="dot", mouth="smile")
    if not part2:
        if t >= A("b1"):
            m.update(eyes="sly", mouth="smirk")
        if t >= A("b1", "pulls"):
            m.update(arms=("hold", "down"), item="phone")
    else:
        if A("b6", "laughs") <= t < A("b6", "Nope"):
            m.update(eyes="closed", mouth="laugh")
        elif t >= A("b6", "Nope"):
            m.update(eyes="sly", mouth="smirk")
        if t >= A("b9"):
            m.update(eyes="happy", mouth="smile", arms=("hip", "down"))
    m["mouth"] = _mouth(tl, "mia", t, m["mouth"])
    person(cr, "mia", MIA_X, FEET, t, **m)
    couch_front(cr)

    # sparkle around Mia + a question mark over Sam in the hook
    if not part2 and t < A("h2"):
        for i, (sx, sy) in enumerate([(430, 640), (560, 620), (545, 700)]):
            sc = 0.6 + 0.4 * abs(math.sin(t * 5 + i))
            from motion.brand import sparkle
            sparkle(cr, sx, sy, 14 * sc, hexc("#fff3c4"), seed=470 + i)
        sq = pop(t, A("h1", "broke"))
        if sq:
            with at(cr, SAM_X + 10, 620, sq):
                write(cr, [("?", BLUE)], 0, 0, 70, align="center", bold=True)

    # --- screen-space headlines
    if not part2:
        hl(cr, t, [("Why would ", INK), ("SHE", PINK)], 215, 64, A("h1", "woman"), end=A("h2", "babe"), bold=True)
        hl(cr, t, [("marry ", INK), ("HIM?", BLUE)], 300, 64, A("h1", "marry"), end=A("h2", "babe"), bold=True)
        hl(cr, t, [("\"Why me?\"", INK)], 250, 64, A("h2", "Why", nth=1), bold=True)
    else:
        hl(cr, t, [("His ", INK), ("daughter", PINK), ("?!", INK)], 240, 62, A("b5", "daughter"), end=A("b6") - 0.05,
           bold=True)
        hl(cr, t, [("$5,000", GREEN), (" / month", INK)], 230, 66, A("b6", "$5,000"), end=A("b7") - 0.05, bold=True)
        cue("kaching", t, A("b6", "$5,000"))
        cue("hit", t, A("b6", "Nope"))
        hl(cr, t, [("his ", INK), ("LUCKY CHARM", GREEN)], 230, 66, A("b7", "lucky"), end=A("b8") - 0.05, bold=True)
        hl(cr, t, [("HE'S WATCHING.", RED)], 230, 70, A("b8", "watching"), end=A("b9") - 0.05, bold=True)
        cue("hit", t, A("b8", "watching"))
        hl(cr, t, [("Never ask ", INK), ("why.", RED)], 230, 70, A("b9", "never"), bold=True, underline=True)


def scene_phone(cr, t, tl):
    A = tl.at
    cr.set_source_rgba(*hexc("#e9d3ae"))
    cr.paint()
    z = camera(t, [(A("b2") - 0.2, (1.0,)), (A("b2", "photo"), (1.12,)), (A("b2", "Remember"), (1.3,))])[0]
    with at(cr, 360, 640, z):
        blob(cr, -150, 260, 70, 50, hexc("#f0c29c"), seed=700, amp=0.6, lw=4)   # hand
        def screen(cr):
            cr.set_source_rgba(*hexc("#cfd9e6"))
            cr.paint()
            sc = pop(t, A("b2", "photo"), 0.25)
            if sc:
                with at(cr, 0, 0, sc):
                    shape(cr, rrect_pts(-90, -160, 180, 320, 10, 20), hexc("#9a958a"), seed=701, amp=0.4, lw=0,
                          stroke=None)
                    person(cr, "beggar", 0, 250, t, facing=1, eyes="dot", mouth="smile", scale=1.45, bob=False)
        phone(cr, 0, 0, 1.6, screen=screen)
        blob(cr, 150, 150, 36, 60, hexc("#f0c29c"), seed=702, amp=0.6, lw=4)   # thumb side
    hl(cr, t, [("Remember ", INK), ("him?", RED)], 215, 70, A("b2", "Remember"), bold=True)


def scene_street(cr, t, tl):
    A = tl.at
    give = A("b3", "$5")
    z, fx, fy = camera(t, [(A("b3") - 0.3, (1.5, 380, 740)), (A("b3", "exact"), (1.9, 470, 760)),
                           (give - 0.2, (1.9, 390, 750)),
                           (give + 0.8, (1.6, 400, 745))])
    set_camera((z, fx, fy))
    enter_world(cr)
    street(cr, t)
    # beggar sitting on a crate with a cup
    happy = t > give + 0.4
    person(cr, "beggar", 480, 900, t, facing=-1, arms=("thumb" if happy else "hold", "down"),
           eyes="happy" if happy else "sad", mouth="grin" if happy else "flat")
    sharp_shape(cr, [(425, 810), (540, 810), (540, 880), (425, 880)], hexc("#d9a15a"), seed=801, amp=0.8, lw=4)
    shape(cr, [(392, 836), (420, 836), (416, 872), (396, 872)], hexc("#e8e2d0"), seed=802, amp=0.4, lw=3)   # cup
    # Sam walks in and hands over $5
    sx = lerp(-120, 300, ease_out(seg(t, A("b3"), A("b3") + 0.9)))
    walking = t < A("b3") + 0.9
    giving = give - 0.4 <= t < give + 0.3
    person(cr, "sam", sx, 880, t, facing=1, walk=(sx / 70) if walking else None,
           arms=("give" if giving else "hip", "down"), item="note5" if giving else None, mouth="smile")
    fly(cr, t, give + 0.3, 0.35, (360, 760), (406, 850), lambda x, y: dollar(cr, x, y, 0.45), height=60)
    cue("kaching", t, give + 0.3)
    sepia(cr)
    stamp(cr, t, A("b3") - 0.15, "5 YEARS AGO", dur=0.9)
    hl(cr, t, [("$5", GREEN)], 260, 110, give, bold=True)


def scene_lotto(cr, t, tl):
    A = tl.at
    won = A("b4", "won")
    big = A("b4", "$10,000,000")
    z, fx, fy = camera(t, [(A("b4") - 0.3, (1.45, 430, 720)), (A("b4", "spent"), (1.6, 330, 740)),
                           (A("b4", "lottery"), (1.8, 340, 740)),
                           (won, (1.7, 530, 630)), (big, (1.45, 430, 720))])
    set_camera((z, fx, fy))
    enter_world(cr)
    kiosk(cr, t, won)
    jumping = t >= big
    person(cr, "beggar", 290, 880, t, facing=1,
           arms=("cheer", "cheer") if jumping else ("hold", "down"), item=None if jumping else "ticket",
           eyes="happy" if jumping else ("wide" if t >= won else "dot"),
           mouth="laugh" if jumping else ("o" if t >= won else "smile"),
           jump=abs(math.sin((t - big) * 9)) * 30 if jumping else 0)
    sepia(cr, 0.8)
    confetti(cr, t, big)
    cue("kaching", t, won)
    cue("hit", t, big)
    hl(cr, t, [("$10,000,000", GREEN)], 250, 86, big, bold=True, underline=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "home":
        scene_home(cr, t, tl)
    elif name == "phone":
        scene_phone(cr, t, tl)
    elif name == "street":
        scene_street(cr, t, tl)
    elif name == "lotto":
        scene_lotto(cr, t, tl)
    else:
        scene_home(cr, t, tl, part2=True)
    cr.restore()
    captions(cr, t, tl)
