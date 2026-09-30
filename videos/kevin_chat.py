"""Episode 16: "Who Is Kevin?" — an original classroom twist story (same class as The Backbencher / Class of Scammers).

The class has a secret group chat. A mystery member, Kevin, posts the "answer key" the night before the final.
Everyone memorises it; no question matches; 29 zeros. Kevin was the teacher all along.
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import (INK, RED, WHITE, W, at, blob, cue, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg,
                           shape, sharp_shape, write)
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from videos.backbencher import classroom, desk

NARRATOR = dict(speed=1.03)
TAIL = 0.8

SCRIPT = [
    dict(id="g1", scene="chat",
         text="Every class has a group chat the teacher doesn't know about. This class had one too."),
    dict(id="g2", scene="chat", text="[Thirty|30] kids. Memes all day. Roasting Mr. Miller's mustache every night."),
    dict(id="g3", scene="chat",
         text="And one mystery member: Kevin. Nobody knew who Kevin was. But Kevin had the best memes."),
    dict(id="g4", scene="night", text="The night before the final exam, Kevin drops a message: I got the answer key.",
         gap=0.25),
    dict(id="g5", scene="night", text="The chat explodes. Everyone memorizes every single answer."),
    dict(id="g6", scene="test", text="Next morning, the test starts, and not one question matches.", gap=0.25),
    dict(id="g7", scene="test",
         text="[Twenty-nine|29] zeros. The only kid who passed was Emma, because she muted the chat months ago."),
    dict(id="g8", scene="reveal",
         text="Then Mr. Miller picks up his phone, smiles, and types one last message.", gap=0.25),
    dict(id="g9", scene="reveal", text="Kevin has left the chat.", pace=0.92),
    dict(id="g10", scene="reveal", text="[Also,|P.S.] the mustache jokes were funny.", speaker="teacher", gap=0.3),
]

METADATA = dict(
    title="The Mystery Kid in the Class Group Chat Was… 😳",
    alt_titles=["Nobody Knew Who Kevin Was… Until the Exam 😂", "The Teacher Was in the Group Chat the Whole Time 💀"],
    description="""Every class has a secret group chat the teacher doesn't know about. This one had 30 kids, endless memes… and one mystery member named Kevin. 🤫

The night before the final, Kevin posted the "answer key." Everyone memorized it. Not one question matched. 😳

Then the teacher picked up his phone…

💬 Would you have trusted Kevin? 👇

🔔 Interestingly Strange: weird animals, bizarre history, mind-bending paradoxes and strange stories, hand-drawn in under a minute.""",
    hashtags=["#PlotTwist", "#School", "#Funny"],
    tags=["plot twist", "school story", "group chat", "teacher prank", "funny story", "twist ending", "exam story",
          "storytime", "animated story", "interestingly strange"],
    pinned_comment="Every group chat has a Kevin. Who's yours? 😂👇",
)

GREEN = hexc("#3d8f45")
BLUE = hexc("#3f6fb5")
PINK = hexc("#e0487a")
PURPLE = hexc("#6a45b5")
GOLD = hexc("#f2b632")
CHATBG = hexc("#eef3f7")
KEVIN = hexc("#8a8f99")
AVATARS = [(PINK, "E"), (BLUE, "T"), (PURPLE, "O"), (GOLD, "J"), (GREEN, "M"), (KEVIN, "?")]


def phone_frame(cr, x, y, w, h, seed=0):
    shape(cr, rrect_pts(x - w / 2 - 18, y - h / 2 - 30, w + 36, h + 60, 44, 24), INK, seed=seed, amp=0.6, lw=4)
    shape(cr, rrect_pts(x - w / 2, y - h / 2, w, h, 20, 24), CHATBG, seed=seed + 1, amp=0.3, lw=0, stroke=None)
    shape(cr, rrect_pts(x - w / 2, y - h / 2, w, 84, 20, 16), BLUE, seed=seed + 2, amp=0.3, lw=0, stroke=None)
    write(cr, [("CLASS 8B", WHITE)], x, y - h / 2 + 44, 34, align="center", bold=True)
    write(cr, [("(no teachers allowed)", hexc("#dfe9f2"))], x, y - h / 2 + 72, 20, align="center")


def msg(cr, x, y, who, text, t0, t, mine=False, big=False, seed=0):
    """One chat bubble with an avatar; pops in at t0."""
    sc = pop(t, t0, 0.2)
    if sc <= 0:
        return
    col, letter = AVATARS[who]
    with at(cr, x, y, sc):
        blob(cr, -150, 0, 30, 30, col, seed=seed, amp=0.3, lw=3)
        write(cr, [(letter, WHITE)], -150, 12, 32, align="center", bold=True)
        size = 34 if big else 32
        cr.save()
        from motion.engine import text_width
        tw = text_width(cr, [(text, INK)], size, bold=big) + 30
        cr.restore()
        shape(cr, rrect_pts(-110, -32, tw, 64, 20, 14), WHITE if not big else hexc("#fff3c4"), seed=seed + 1, amp=0.4,
              lw=3)
        write(cr, [(text, RED if big else INK)], -96, 11, size, bold=big)
    cue("pop", t, t0)


def scene_chat(cr, t, tl):
    A = tl.at
    keys = [(0, (1.0, 360, 640)), (A("g1", "group"), (1.3, 360, 420)), (A("g1", "teacher"), (1.0, 360, 640)),
            (A("g1", "know"), (1.5, 330, 380)), (A("g1", "class", nth=2), (1.1, 360, 560)), (A("g1", "too"), (1.6, 360, 470)),
            (A("g2", "30"), (1.5, 360, 400)), (A("g2", "kids"), (1.1, 360, 600)), (A("g2", "memes"), (1.4, 360, 480)),
            (A("g2", "roasting"), (1.2, 360, 700)), (A("g2", "mustache"), (1.7, 380, 570)), (A("g2", "night"), (1.3, 380, 660)),
            (A("g3", "mystery"), (1.1, 360, 780)), (A("g3", "Kevin"), (1.8, 300, 750)), (A("g3", "nobody"), (1.3, 360, 700)),
            (A("g3", "knew"), (1.8, 330, 840)), (A("g3", "had"), (1.1, 360, 800)), (A("g3", "best"), (1.6, 360, 900))]
    z, fx, fy = camera(t, keys, dur=0.15)
    cr.set_source_rgba(*hexc("#2b2d3a"))
    cr.paint()
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    phone_frame(cr, 360, 640, 600, 960, seed=13000)
    if t >= A("g2", "30"):
        write(cr, [("30 members", hexc("#dfe9f2"))], 520, 250, 20, align="center", bold=True)
    rows = [(0, "lol this class", 0.15), (1, "who has notes??", A("g1", "teacher")),
            (3, "MEMES ALL DAY", A("g2", "memes")), (2, "mr miller's mustache", A("g2", "roasting")),
            (4, "has its own zip code", A("g2", "night")), (5, "hi i'm kevin", A("g3", "Kevin")),
            (1, "who is kevin??", A("g3", "nobody"))]
    y = 290
    for who, text, t0 in rows:
        msg(cr, 330, y, who, text, t0, t, seed=13010 + y)
        y += 92
    if t >= A("g3", "best"):   # kevin's meme: a stick-figure teacher with a giant mustache
        with at(cr, 400, 980, 1.2 * (pop(t, A("g3", "best"), 0.25) or 0.01)):
            shape(cr, rrect_pts(-110, -60, 220, 120, 10, 14), WHITE, seed=13100, amp=0.4, lw=3)
            blob(cr, 0, -10, 30, 30, hexc("#f0c29c"), seed=13101, amp=0.4, lw=3)
            shape(cr, [(-50, 8), (-10, -2), (0, 6), (10, -2), (50, 8), (0, 18)], INK, seed=13102, amp=0.5, lw=2)
            write(cr, [("LOL", RED)], 70, -30, 24, bold=True)
    hl(cr, t, [("a SECRET ", RED), ("group chat", BLUE)], 215, 70, 0.0, end=A("g2") - 0.05, bold=True, sound=False,
       halo=hexc("#fbf3e1", 0.95))
    hl(cr, t, [("roasting ", INK), ("Mr. Miller", RED)], 215, 70, A("g2", "roasting"), end=A("g3") - 0.05, bold=True)
    hl(cr, t, [("who is ", INK), ("KEVIN", KEVIN), ("?", INK)], 215, 90, A("g3", "Kevin"), bold=True)


def scene_night(cr, t, tl):
    A = tl.at
    boom = A("g5", "explodes")
    keys = [(A("g4") - 0.2, (1.0, 360, 640)), (A("g4", "night"), (1.6, 360, 320)), (A("g4", "final"), (1.3, 360, 520)),
            (A("g4", "exam"), (1.0, 360, 640)), (A("g4", "Kevin"), (1.5, 360, 460)), (A("g4", "message"), (1.2, 360, 560)),
            (A("g4", "answer"), (1.9, 380, 640)), (boom, (1.0, 360, 640)), (A("g5", "memorizes"), (1.4, 360, 820)),
            (A("g5", "single"), (1.1, 360, 700))]
    z, fx, fy = camera(t, keys, dur=0.15)
    cr.set_source_rgba(*hexc("#141a33"))
    cr.paint()
    for k in range(30):
        dot(cr, (k * 211) % 720, (k * 157) % 1280, 2, hexc("#fff3c4", 0.4 + 0.3 * math.sin(t * 3 + k)))
    blob(cr, 600, 200, 50, 50, hexc("#fff3c4"), seed=13200, amp=0.4, lw=0, stroke=None)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    shake = math.sin(t * 60) * 6 if boom <= t < boom + 0.6 else 0
    cr.translate(shake, 0)
    phone_frame(cr, 360, 640, 600, 960, seed=13210)
    write(cr, [("11:58 PM", INK)], 360, 300, 28, align="center", bold=True)
    msg(cr, 330, 400, 5, "I GOT THE ANSWER KEY", A("g4", "answer"), t, big=True, seed=13220)
    if t >= A("g4", "key"):   # the "key" itself
        with at(cr, 400, 520, pop(t, A("g4", "key"), 0.2) or 0.01):
            shape(cr, rrect_pts(-130, -44, 260, 88, 8, 14), WHITE, seed=13230, amp=0.4, lw=3)
            write(cr, [("1-B  2-D  3-A  4-C", INK)], 0, 12, 34, align="center", bold=True)
    floods = ["OMG", "KEVIN = LEGEND", "saving this", "kevin for president", "memorizing NOW", "no way!!"]
    for k, text in enumerate(floods):
        msg(cr, 330, 620 + k * 82, k % 5, text, boom + k * 0.12, t, seed=13240 + k)
    if t >= A("g5", "memorizes"):
        write(cr, [("1-B 2-D 3-A 4-C 5-B...", hexc("#fff3c4"))], 360, 1180, 34, align="center", bold=True, halo=INK)
    hl(cr, t, [("the night before the ", INK), ("FINAL", RED)], 215, 58, A("g4", "final"), end=A("g4", "answer") - 0.05,
       bold=True)
    hl(cr, t, [("the ", INK), ("ANSWER KEY", GOLD)], 215, 84, A("g4", "answer"), end=boom - 0.05, bold=True)
    hl(cr, t, [("everyone ", INK), ("memorizes", GREEN)], 215, 76, A("g5", "memorizes"), bold=True)


def scene_test(cr, t, tl):
    A = tl.at
    keys = [(A("g6") - 0.2, (1.0, 470, 760)), (A("g6", "test"), (1.3, 600, 760)), (A("g6", "not"), (1.8, 360, 600)),
            (A("g6", "matches"), (1.2, 470, 760)), (A("g7", "29"), (1.0, 470, 760)), (A("g7", "zeros"), (1.4, 560, 700)),
            (A("g7", "only"), (1.1, 420, 740)), (A("g7", "Emma"), (2.0, 310, 730)), (A("g7", "because"), (1.3, 380, 720)),
            (A("g7", "muted"), (1.5, 360, 640))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    classroom(cr, t)
    person(cr, "teacher", 120, 900, t, facing=1, arms=("hip", "hip"), eyes="sly", mouth="smirk")
    kids = [("kid_a", 330), ("kid_c", 490), ("kid_d", 650), ("chotu", 830)]
    zeros = t >= A("g7", "29")
    for i, (who, x) in enumerate(kids):
        emma = who == "kid_a"
        panic = A("g6", "not") <= t
        person(cr, who, x, 900, t, facing=-1, eyes=("happy" if emma else "wide") if panic else "dot",
               mouth=("grin" if emma else "wobble") if panic else "smile", sweat=panic and not emma,
               shake=1.2 if panic and not emma and not zeros else 0)
        desk(cr, x, 13300 + i * 10)
        if zeros:
            sc = pop(t, A("g7", "29") + i * 0.1, 0.2)
            if sc > 0:
                with at(cr, x, 640, sc, rot=-0.1):
                    write(cr, [("100" if emma else "0", GREEN if emma else RED)], 0, 0, 72 if not emma else 58,
                          align="center", bold=True, halo=WHITE)
    # the test paper, when nothing matches
    if A("g6", "not") <= t < A("g7"):
        with at(cr, 360, 600, pop(t, A("g6", "not"), 0.2) or 0.01, rot=0.04):
            shape(cr, rrect_pts(-170, -210, 340, 420, 6, 18), WHITE, seed=13320, amp=0.6, lw=4)
            write(cr, [("FINAL EXAM", INK)], 0, -160, 36, align="center", bold=True)
            for k, q in enumerate(["1. Explain photosynthesis", "2. Solve for x", "3. Name 3 rivers",
                                   "4. Write an essay"]):
                write(cr, [(q, INK)], -150, -90 + k * 60, 22)
            write(cr, [("(no multiple choice)", RED)], 0, 170, 26, align="center", bold=True)
    hl(cr, t, [("not ONE question ", INK), ("matches", RED)], 215, 60, A("g6", "not"), end=A("g7") - 0.05, bold=True)
    hl(cr, t, [("29 ", RED), ("zeros", INK)], 215, 96, A("g7", "29"), end=A("g7", "Emma") - 0.05, bold=True)
    hl(cr, t, [("Emma ", PINK), ("muted the chat", INK)], 215, 66, A("g7", "muted"), bold=True)
    if zeros:
        cue("hit", t, A("g7", "29"))


def scene_reveal(cr, t, tl):
    A = tl.at
    left = A("g9")
    keys = [(A("g8") - 0.2, (1.4, 160, 740)), (A("g8", "phone"), (2.2, 200, 700)), (A("g8", "smiles"), (2.4, 150, 730)),
            (A("g8", "types"), (1.6, 330, 600)), (left, (1.3, 360, 620)), (A("g9", "chat"), (1.5, 360, 560)),
            (A("g10"), (1.9, 160, 730)), (A("g10", "mustache"), (2.4, 140, 740)), (A("g10", "funny"), (1.2, 400, 760))]
    set_camera(camera(t, keys, dur=0.15))
    enter_world(cr)
    classroom(cr, t)
    tlk = tl.speaking("teacher", t)
    person(cr, "teacher", 120, 900, t, facing=1, arms=("hold", "hip") if t < A("g10") else ("thumb", "hip"),
           eyes="sly", mouth=("o" if int(t * 12) % 2 else "smirk") if tlk else "smirk",
           item="phone" if t < A("g10") else None)
    for i, (who, x) in enumerate((("kid_a", 330), ("kid_c", 490), ("kid_d", 650), ("chotu", 830))):
        shocked = t >= left
        person(cr, who, x, 900, t, facing=-1, eyes="wide" if shocked else "sad", mouth="o" if shocked else "flat",
               sweat=shocked, jump=abs(math.sin(t * 9 + i)) * 6 if shocked else 0)
        desk(cr, x, 13400 + i * 10)
    if t >= A("g8", "types"):   # his phone, big
        with at(cr, 380, 560, 0.85, rot=-0.03):
            phone_frame(cr, 0, 0, 520, 640, seed=13410)
            write(cr, [("typing...", KEVIN)], 0, -120, 30, align="center")
            if t >= left:
                shape(cr, rrect_pts(-220, -40, 440, 90, 18, 16), hexc("#fff3c4"), seed=13420, amp=0.4, lw=3)
                write(cr, [("Kevin has left the chat", INK)], 0, 16, 36, align="center", bold=True)
            if t >= A("g10"):
                write(cr, [("P.S. the mustache jokes", INK)], 0, 140, 34, align="center", bold=True)
                write(cr, [("were funny", INK)], 0, 184, 34, align="center", bold=True)
        if t >= left:
            cue("hit", t, left)
    hl(cr, t, [("KEVIN", KEVIN), (" = ", INK), ("MR. MILLER", RED)], 215, 70, left, bold=True, underline=True)
    stamp(cr, t, left + 0.3, "IT WAS HIM", dur=0.9, y=470)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"chat": scene_chat, "night": scene_night, "test": scene_test, "reveal": scene_reveal}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
