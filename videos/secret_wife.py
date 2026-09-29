"""Episode 2: "The Secret of His Wife" — the viral beggar/lottery joke, told in our own words with original characters.

Beats: a broke guy asks his gorgeous wife why she picked him -> she shows him a beggar he gave $5 to five years ago ->
the beggar won $10 million on a lottery ticket -> he guesses she's the beggar's daughter -> she laughs: the beggar
went to Thailand, then Korea... and came back as his wife. Told as a pure twist: no mockery, and the wife stays
the confident, likeable one.
"""
import math

from motion import characters as ch
from motion.brand import sparkle
from motion.captions import captions
from motion.characters import dollar, person, phone
from motion.engine import (INK, RED, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, confetti, enter_world, fly, hl, sepia, set_camera, stamp, whip
from motion.sets import couch_back, couch_front, kiosk, living_room, street

NARRATOR = dict()   # channel default narrator (see motion/voice.py)

SCRIPT = [
    dict(id="s1", scene="home",
         text="This guy looks at his gorgeous, classy wife and asks her: babe, you're so beautiful. "
              "Why'd you pick a broke guy like me?", speaker="sam", speaker_from="babe"),
    dict(id="s2", scene="home", text="She goes: you really wanna know?", speaker="mia", speaker_from="you"),
    dict(id="s3", scene="home", text="He blushes: obviously I wanna know!", speaker="sam", speaker_from="obviously"),
    dict(id="s4", scene="home", text="So she pulls out her phone."),
    dict(id="s5", scene="phone", text="Remember this beggar? He goes: yeah, kinda."),
    dict(id="s6", scene="street", text="Turns out, five years ago, he gave that beggar [five bucks.|$5.]", gap=0.25),
    dict(id="s7", scene="lotto",
         text="She says: that beggar bought a lottery ticket with your money, and won [ten million dollars!|$10,000,000!]"),
    dict(id="s8", scene="home2", text="So he figures it out: you're the beggar's daughter, and you came to thank me?",
         speaker="sam", speaker_from="you're", gap=0.25),
    dict(id="s9", scene="travel", text="She laughs: after winning, the beggar went to Thailand first, then Korea,"),
    dict(id="s10", scene="travel", text="and finally came back,", pace=0.95, gap=0.12),
    dict(id="s10b", scene="home3", text="as your wife.", speaker="mia", pace=0.9, gap=0.15),
    dict(id="s11", scene="home3", text="Did you get it?", gap=0.3),
]

METADATA = dict(
    title="Why She Really Married a Broke Guy 😳 Wait for It",
    alt_titles=["He Gave a Beggar $5… Years Later His Wife Told Him Why 😳",
                "The Secret Behind His Gorgeous Wife 😳"],
    description="""He's broke. She's gorgeous. So he finally asks her why she picked him… 😳

She pulls out her phone and shows him a beggar he gave $5 to, five years ago. What happened to that $5 is the twist. Watch till the end. 👀

💬 Did you get it? Comment 👀 if you did.

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#PlotTwist", "#Storytime", "#Animation"],
    tags=["plot twist", "twist ending", "wait for the end", "storytime", "funny story", "animated story",
          "lottery winner story", "beggar story", "did you get it", "short story animation", "interestingly strange"],
    pinned_comment="Took me a second too 😂 Did you get it? 👀",
)

# ---------------------------------------------------------------- layout (world units)
FEET = 870
SAM_X, MIA_X = 290, 480
PINK = hexc("#e0487a")
BLUE = hexc("#3f6fb5")
GREEN = hexc("#3d8f45")

WIDE = (1.45, 385, 700)
HOOK = (1.5, 385, 700)
P_SAM = (1.9, 300, 715)
P_MIA = (1.9, 470, 712)


def _mouth(tl, who, t, rest):
    return ("o" if int(t * 12) % 2 else "smile") if tl.speaking(who, t) else rest


# ---------------------------------------------------------------- scenes
def scene_home(cr, t, tl, part=1):
    A = tl.at
    if part == 1:
        keys = [(0, HOOK), (A("s1", "gorgeous"), P_MIA), (A("s1", "classy"), (2.2, 475, 705)),
                (A("s1", "asks"), WIDE), (A("s1", "babe"), P_SAM), (A("s1", "beautiful"), (1.75, 400, 712)), (A("s1", "broke"), (2.1, 300, 712)),
                (A("s2"), P_MIA), (A("s3"), P_SAM), (A("s3", "obviously"), (2.1, 300, 712)), (A("s4"), P_MIA)]
        z, fx, fy = camera(t, keys)
        if t < A("s1", "gorgeous"):
            z += 0.05 * seg(t, 0, A("s1", "gorgeous"))   # slow push so frame 0 already moves
    elif part == 2:
        keys = [(A("s8") - 0.2, WIDE), (A("s8", "you're"), P_SAM), (A("s8", "daughter"), (2.1, 300, 710)),
                (A("s8", "thank"), P_MIA)]
        z, fx, fy = camera(t, keys)
    else:
        keys = [(A("s10b") - 0.2, P_MIA), (A("s10b", "wife"), (2.2, 470, 705)), (A("s11"), P_SAM),
                (A("s11", "get"), WIDE)]
        z, fx, fy = camera(t, keys, dur=0.35)
    set_camera((z, fx, fy))
    enter_world(cr)
    living_room(cr, t)
    couch_back(cr)

    # --- Sam
    s = dict(facing=1, arms=("hip", "down"), eyes="dot", mouth="smile")
    if part == 1:
        if t >= A("s1", "babe"):
            s.update(arms=("point", "down"), eyes="happy")
        if t >= A("s2"):
            s.update(arms=("hip", "down"), eyes="wide", mouth="o")
        if t >= A("s3"):
            s.update(eyes="happy", mouth="grin")   # blushing
        if t >= A("s4"):
            s.update(eyes="wide", mouth="o")
    elif part == 2:
        s.update(arms=("point", "down"), eyes="wide", mouth="o")
    else:
        s.update(eyes="wide", mouth="o", sweat=True)
        if t >= A("s10b", "wife"):
            s.update(shake=1.4 * (1 - seg(t, A("s10b", "wife") + 0.6, A("s10b", "wife") + 0.8)))
    s["mouth"] = _mouth(tl, "sam", t, s["mouth"])
    person(cr, "sam", SAM_X, FEET, t, **s)

    # --- Mia (the confident one)
    m = dict(facing=-1, arms=("hip", "down"), eyes="dot", mouth="smile")
    if part == 1:
        if t >= A("s2"):
            m.update(eyes="sly", mouth="smirk")
        if t >= A("s4", "pulls"):
            m.update(arms=("hold", "down"), item="phone")
    elif part == 2:
        m.update(eyes="sly", mouth="smirk")
    else:
        m.update(eyes="happy", mouth="smile", arms=("wave", "down") if A("s10b", "wife") <= t < A("s11") else ("hip", "down"))
    m["mouth"] = _mouth(tl, "mia", t, m["mouth"])
    person(cr, "mia", MIA_X, FEET, t, **m)
    couch_front(cr)

    # sparkles around Mia: in the hook, and again at the reveal
    if (part == 1 and t < A("s1", "babe")) or (part == 3 and t >= A("s10b", "wife")):
        for i, (sx, sy) in enumerate([(430, 640), (560, 620), (545, 700), (410, 700)]):
            sc = 0.6 + 0.4 * abs(math.sin(t * 5 + i))
            sparkle(cr, sx, sy, 14 * sc, hexc("#fff3c4"), seed=470 + i)
    if part == 1:
        sq = pop(t, A("s1", "broke"))
        if sq and t < A("s2"):
            with at(cr, SAM_X + 10, 620, sq):
                write(cr, [("?", BLUE)], 0, 0, 70, align="center", bold=True)

    # --- screen-space headlines
    if part == 1:
        hl(cr, t, [("gorgeous ", PINK), ("wife", INK)], 215, 64, A("s1", "gorgeous"), end=A("s1", "Why'd") - 0.05,
           bold=True)
        hl(cr, t, [("Why'd she pick", INK)], 205, 60, A("s1", "Why'd"), end=A("s2") - 0.05, bold=True)
        hl(cr, t, [("a ", INK), ("BROKE", BLUE), (" guy?", INK)], 285, 64, A("s1", "broke"), end=A("s2") - 0.05,
           bold=True)
        hl(cr, t, [("\"You really wanna know?\"", INK)], 240, 52, A("s2", "really"), end=A("s3") - 0.05, bold=True)
        hl(cr, t, [("\"Obviously!\"", BLUE)], 240, 66, A("s3", "obviously"), end=A("s4") - 0.05, bold=True)
    elif part == 2:
        hl(cr, t, [("His ", INK), ("daughter", PINK), ("?!", INK)], 240, 64, A("s8", "daughter"), bold=True)
    else:
        hl(cr, t, [("...as ", INK), ("YOUR WIFE.", PINK)], 240, 72, A("s10b", "wife"), end=A("s11") - 0.05, bold=True,
           underline=True)
        cue("hit", t, A("s10b", "wife"))
        hl(cr, t, [("Did you ", INK), ("get it?", RED)], 240, 72, A("s11", "Did"), bold=True, underline=True)


def scene_phone(cr, t, tl):
    A = tl.at
    cr.set_source_rgba(*hexc("#e9d3ae"))
    cr.paint()
    z = camera(t, [(A("s5") - 0.2, (1.0,)), (A("s5", "beggar"), (1.15,)), (A("s5", "goes"), (1.3,))])[0]
    with at(cr, 360, 640, z):
        blob(cr, -150, 260, 70, 50, hexc("#f0c29c"), seed=700, amp=0.6, lw=4)   # hand
        def screen(cr):
            cr.set_source_rgba(*hexc("#cfd9e6"))
            cr.paint()
            sc = pop(t, A("s5", "Remember"), 0.25)
            if sc:
                with at(cr, 0, 0, sc):
                    shape(cr, rrect_pts(-90, -160, 180, 320, 10, 20), hexc("#9a958a"), seed=701, amp=0.4, lw=0,
                          stroke=None)
                    person(cr, "beggar", 0, 250, t, facing=1, eyes="dot", mouth="smile", scale=1.45, bob=False)
        phone(cr, 0, 0, 1.6, screen=screen)
        blob(cr, 150, 150, 36, 60, hexc("#f0c29c"), seed=702, amp=0.6, lw=4)   # thumb side
    hl(cr, t, [("Remember ", INK), ("him?", RED)], 215, 70, A("s5", "Remember"), end=A("s5", "goes") - 0.05, bold=True)
    hl(cr, t, [("\"Yeah... kinda.\"", BLUE)], 215, 66, A("s5", "yeah"), bold=True)


def scene_street(cr, t, tl):
    A = tl.at
    give = A("s6", "$5")
    z, fx, fy = camera(t, [(A("s6") - 0.3, (1.5, 380, 740)), (A("s6", "gave"), (1.9, 470, 760)),
                           (give - 0.2, (1.9, 390, 750)), (give + 0.8, (1.6, 400, 745))])
    set_camera((z, fx, fy))
    enter_world(cr)
    street(cr, t)
    happy = t > give + 0.4
    person(cr, "beggar", 480, 900, t, facing=-1, arms=("thumb" if happy else "hold", "down"),
           eyes="happy" if happy else "sad", mouth="grin" if happy else "flat")
    sharp_shape(cr, [(425, 810), (540, 810), (540, 880), (425, 880)], hexc("#d9a15a"), seed=801, amp=0.8, lw=4)
    shape(cr, [(392, 836), (420, 836), (416, 872), (396, 872)], hexc("#e8e2d0"), seed=802, amp=0.4, lw=3)   # cup
    sx = lerp(-120, 300, ease_out(seg(t, A("s6"), A("s6") + 0.9)))
    walking = t < A("s6") + 0.9
    giving = give - 0.4 <= t < give + 0.3
    person(cr, "sam", sx, 880, t, facing=1, walk=(sx / 70) if walking else None,
           arms=("give" if giving else "hip", "down"), item="note5" if giving else None, mouth="smile")
    fly(cr, t, give + 0.3, 0.35, (360, 760), (406, 850), lambda x, y: dollar(cr, x, y, 0.45), height=60)
    cue("kaching", t, give + 0.3)
    sepia(cr)
    stamp(cr, t, A("s6") - 0.15, "5 YEARS AGO", dur=0.9)
    hl(cr, t, [("$5", GREEN)], 260, 110, give, bold=True)


def scene_lotto(cr, t, tl):
    A = tl.at
    won = A("s7", "won")
    big = A("s7", "$10,000,000")
    z, fx, fy = camera(t, [(A("s7") - 0.3, (1.45, 430, 720)), (A("s7", "bought"), (1.6, 330, 740)),
                           (A("s7", "lottery"), (1.8, 340, 740)), (A("s7", "money"), (1.6, 430, 700)),
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


def _stamp_mark(cr, x, y, text, color, round_=True, s=1.0, rot=-0.2, seed=0):
    with at(cr, x, y, s, rot):
        if round_:
            blob(cr, 0, 0, 92, 92, hexc("#ffffff", 0.0), seed=seed, amp=1.0, lw=7, stroke=color)
            blob(cr, 0, 0, 76, 76, hexc("#ffffff", 0.0), seed=seed + 1, amp=1.0, lw=3, stroke=color)
        else:
            shape(cr, rrect_pts(-110, -46, 220, 92, 10, 18), hexc("#ffffff", 0.0), seed=seed, amp=1.0, lw=7,
                  stroke=color)
        write(cr, [(text, color)], 0, 12, 36, align="center", bold=True)


def scene_travel(cr, t, tl):
    """Passport montage: the (now rich) beggar's passport gets THAILAND, then KOREA stamps."""
    A = tl.at
    cr.set_source_rgba(*hexc("#bfe3f2"))
    cr.paint()
    # dotted flight path + plane
    cr.set_source_rgba(*hexc("#3f6fb5", 0.5))
    cr.set_dash([10, 12])
    cr.set_line_width(5)
    cr.move_to(-40, 1020)
    cr.curve_to(200, 940, 520, 960, 760, 1010)
    cr.stroke()
    cr.set_dash([])
    back = t >= A("s10")
    u = seg(t, A("s10"), A("s10", end=True)) if back else seg(t, A("s9"), A("s9", end=True))
    px, py = (lerp(780, -60, u) if back else lerp(-60, 780, u)), 1020 - math.sin(u * math.pi) * 60
    with at(cr, px, py, 1.0, rot=-0.08 if back else 0.08, flip=back):
        shape(cr, [(-60, -8), (50, -12), (70, 0), (50, 12), (-60, 8)], WHITE, seed=900, amp=0.5, lw=4)
        shape(cr, [(-10, 0), (20, -50), (32, -50), (18, 0)], hexc("#e0487a"), seed=901, amp=0.4, lw=3.5)
        shape(cr, [(-50, -6), (-66, -34), (-56, -34), (-40, -6)], hexc("#e0487a"), seed=902, amp=0.4, lw=3.5)
    cue("whoosh", t, A("s9"), 0.6)
    cue("whoosh", t, A("s10"), 0.6)
    # the open passport
    z = camera(t, [(A("s9") - 0.2, (1.0,)), (A("s9", "after"), (1.1,)), (A("s9", "Thailand"), (1.06,)), (A("s9", "Korea"), (1.12,)),
                   (A("s10", "back"), (1.0,))])[0]
    with at(cr, 360, 630, z):
        shape(cr, rrect_pts(-300, -230, 600, 460, 22, 24), hexc("#1f3f7a"), seed=910, amp=0.8, lw=5)
        shape(cr, rrect_pts(-285, -215, 280, 430, 12, 22), hexc("#fbf3e1"), seed=911, amp=0.6, lw=3.5)
        shape(cr, rrect_pts(5, -215, 280, 430, 12, 22), hexc("#fbf3e1"), seed=912, amp=0.6, lw=3.5)
        write(cr, [("PASSPORT", hexc("#1f3f7a"))], -145, -170, 34, align="center", bold=True)
        cr.save()
        cr.rectangle(-230, -140, 170, 200)
        cr.clip()
        cr.set_source_rgba(*hexc("#cfd9e6"))
        cr.paint()
        person(cr, "richbeggar", -145, 200, t, facing=1, mouth="grin", scale=1.15, bob=False)
        cr.restore()
        sharp_shape(cr, [(-230, -140), (-60, -140), (-60, 60), (-230, 60)], None, seed=913, amp=0.4, lw=3)
        for k in range(3):
            line(cr, [(-240, 100 + k * 30), (-50, 100 + k * 30)], 3, hexc("#b9ad96"), seed=914 + k, amp=0.5)
        s1 = pop(t, A("s9", "Thailand"), 0.2)
        if s1:
            _stamp_mark(cr, 150, -90, "THAILAND", RED, True, 1.0 + 0.6 * (1 - s1), seed=920)
        s2 = pop(t, A("s9", "Korea"), 0.2)
        if s2:
            _stamp_mark(cr, 140, 110, "KOREA", BLUE, False, 1.0 + 0.6 * (1 - s2), rot=0.15, seed=930)
    cue("thud", t, A("s9", "Thailand"))
    cue("thud", t, A("s9", "Korea"))
    hl(cr, t, [("Thailand...", RED)], 190, 60, A("s9", "Thailand"), bold=True)
    hl(cr, t, [("then Korea...", BLUE)], 260, 60, A("s9", "Korea"), bold=True)
    hl(cr, t, [("...and came back", INK)], 330, 54, A("s10", "back"), bold=True)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "home":
        scene_home(cr, t, tl, 1)
    elif name == "phone":
        scene_phone(cr, t, tl)
    elif name == "street":
        scene_street(cr, t, tl)
    elif name == "lotto":
        scene_lotto(cr, t, tl)
    elif name == "home2":
        scene_home(cr, t, tl, 2)
    elif name == "travel":
        scene_travel(cr, t, tl)
    else:
        scene_home(cr, t, tl, 3)
    cr.restore()
    captions(cr, t, tl)
