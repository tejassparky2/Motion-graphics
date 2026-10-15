"""Hook test H4 (identity call-out): "Last-Row Students, Stop Scrolling".

Script: out/scripts_hook_test.md, H4 (owner approved the hook-test batch on 15 Oct 2026). Original story. Voices:
Chatterbox Turbo with tags (narrator = Turbo's stock voice; the kid and the teacher through Turbo with synthetic Kokoro
reference voices). Classroom set and helpers from The Last Bencher Part 4.
"""
import math

from motion import thriller as th
from motion import voice
from motion.engine import W, cue, hexc
from motion.kit import whip
from motion.polish import (WHITE, appear, camera, captions, enter, sign, stamp, stroke_line, vignette)
from motion.toons import person, portrait
from videos.last_bencher_4 import (BLUE, GOLD, GREEN, PURPLE, RED, chalk, classroom, mouth_of, room, sparkles,
                                   studio)

NARRATOR = dict(turbo=True)
TAIL = 0.9
voice.SPEAKERS.update({"kid": dict(voice="am_puck", speed=1.04, pitch=2.5, turbo_ref="am_puck+3"),
                       "sir": dict(voice="am_michael", speed=1.0, turbo_ref="am_michael")})

SCRIPT = [
    dict(id="b1", scene="hook", text="If you ever sat in the last row, stop scrolling. This one's for you."),
    dict(id="b2", scene="board", text="On the first day, the teacher pointed at the rows."),
    dict(id="b3", scene="board", text="Front row students become doctors. Second row, engineers.", speaker="sir"),
    dict(id="b4", scene="glare", text="Then he looked at the last row. And what do you become?", speaker="sir",
         speaker_from="And", gap=0.3),
    dict(id="b5", scene="kid", text="The last bencher didn't even stand up."),
    dict(id="b6", scene="kid", text="The ones who hire them, sir. [chuckle]", speaker="kid", gap=0.35),
    dict(id="b7", scene="laugh", text="The whole class went silent. Then the teacher laughed too. [laugh]", gap=0.4),
    dict(id="b8", scene="end", text="Front row, or last row. Where did you sit?", gap=0.3),
]

METADATA = dict(
    title="Last-Row Students, This One's for You 😏",
    alt_titles=["Front Row Becomes Doctors. Last Row Becomes… 😏", "The Last Bencher's 6-Word Comeback 🔥"],
    description="""If you ever sat in the last row, stop scrolling. This one's for you. 😏

First day of school. The teacher points at the rows: "Front row students become doctors. Second row, engineers."
Then he looks at the last row: "And what do you become?"

The last bencher doesn't even stand up... 😂

💬 Front row or last row: where did YOU sit? 👇

🔔 Interestingly Strange: The Last Bencher, clever twists and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#TheLastBencher", "#Shorts", "#Funny"],
    tags=["the last bencher", "last bencher", "backbencher", "teacher vs student", "funny school story", "comeback",
          "front row vs last row", "school memes", "plot twist", "interestingly strange"],
    pinned_comment="Front row 🤓 or last row 😎? Be honest 👇",
)


def scene_hook(cr, t, tl):
    A = tl.at
    room(cr, t)
    cam = camera(t, [(0.0, (1.75, 540, 470)), (A("b1", "This"), (2.0, 560, 480))], dur=1.0)
    cr.save()
    enter(cr, cam)
    classroom(cr, t, tl, kid_pose=dict(arms=("hips", "hips"), eyes="happy", mouth="grin", brows="raise"))
    k = appear(t, 0.0, 0.3)                      # red arrow bobbing at the last bench (there from frame 0)
    y = 330 + 10 * math.sin(t * 6)
    stroke_line(cr, [(560, y - 60 * k), (560, y)], 14, RED, curve=False)
    stroke_line(cr, [(540, y - 18), (560, y), (580, y - 18)], 14, RED, curve=False)
    cr.restore()
    vignette(cr, 0.45)


def scene_board(cr, t, tl):
    A = tl.at
    room(cr, t, board=True)
    cam = camera(t, [(A("b2") - 0.3, (1.0, 360, 640)), (A("b3"), (1.08, 340, 600))], dur=1.0)
    cr.save()
    enter(cr, cam)
    chalk(cr, t, A("b3", "Front"), 100, 240, "FRONT ROW  ->  DOCTOR", 40)
    chalk(cr, t, A("b3", "Second"), 100, 320, "2ND ROW  ->  ENGINEER", 40)
    chalk(cr, t, A("b3", "engineers.", end=True), 100, 400, "LAST ROW  ->  ???", 40, dur=0.4)
    talk = tl.speaking("sir", t)
    person(cr, t, 560, 900, 1.0, "sir", facing=-1, eyes="half" if talk else "open", mouth="talk" if talk else "smug",
           arms=("point", "hips") if t >= A("b2", "pointed") else ("down", "down"), look=(-0.5, -0.3))
    cr.restore()
    for key in ("Front", "Second"):
        cue("pop", t, A("b3", key))
    vignette(cr, 0.4)


def scene_glare(cr, t, tl):
    A = tl.at
    room(cr, t)
    turn = t >= A("b4", "And")
    cam = camera(t, [(A("b4") - 0.3, (1.0, 360, 640)), (A("b4", "And"), (1.35, 470, 520))], dur=0.6)
    cr.save()
    enter(cr, cam)
    classroom(cr, t, tl, look_at=(560, 0) if turn else None,
              kid_pose=dict(arms=("hips", "hips"), eyes="half", mouth="smug"))
    cr.restore()
    portrait(cr, t, A("b4") + 0.05, 130, 300, 90, "sir", mouth=mouth_of(tl, "sir", t, "flat"),
             eyes="angry" if turn else "half", brows="angry" if turn else None, bg=hexc("#9fc8ef"))
    sign(cr, t, A("b4", "And"), 400, 200, "AND YOU?", col=PURPLE, size=72)
    cue("hit", t, A("b4", "become?"))
    vignette(cr, 0.45)


def scene_kid(cr, t, tl):
    A = tl.at
    room(cr, t)
    line = A("b6")
    cam = camera(t, [(A("b5") - 0.3, (1.7, 545, 470)), (line, (2.3, 560, 450))], dur=0.5)
    cr.save()
    enter(cr, cam)
    talk = tl.speaking("kid", t)
    classroom(cr, t, tl, kid_pose=dict(arms=("hips", "hips"), eyes="half" if not talk else "open",
                                       mouth="talk" if talk else "smug", brows="raise"))
    cr.restore()
    stamp(cr, t, A("b6", "hire"), 360, 230, "THE ONES WHO HIRE THEM", col=RED, size=50)
    cue("hit", t, A("b6", "hire"))
    sparkles(cr, t, A("b6", "sir."), 560, 520, n=8, seed=3, col=GOLD, spread=140)
    vignette(cr, 0.45)


def scene_laugh(cr, t, tl):
    A = tl.at
    room(cr, t)
    laugh = t >= A("b7", "Then")
    cam = camera(t, [(A("b7") - 0.3, (1.0, 360, 640)), (A("b7", "Then"), (1.06, 360, 620))], dur=0.6)
    cr.save()
    enter(cr, cam)
    classroom(cr, t, tl, gasp=not laugh, kid_pose=dict(arms=("hips", "hips"), eyes="happy", mouth="grin"))
    cr.restore()
    if laugh:
        for k in range(6):                       # "HA" bubbles popping over the class
            st = A("b7", "Then") + 0.12 * k
            if t >= st:
                kk = appear(t, st, 0.3)
                x, y = 120 + (k * 113) % 500, 380 + (k * 71) % 260
                sign(cr, t, st, x, y - 20 * math.sin(t * 4 + k), "HA", col=(GOLD, GREEN, BLUE)[k % 3],
                     size=int(40 * kk) + 1, sound=None)
    portrait(cr, t, A("b7", "Then"), 130, 300, 90, "sir", mouth="grin", eyes="happy", bg=hexc("#9fc8ef"))
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#cdb8ff"), hexc("#fff1d6"), seed=8)
    sign(cr, t, A("b8"), 360, 200, "WHERE DID YOU SIT?", col=GOLD, size=54)
    sign(cr, t, A("b8", "Front"), 200, 480, "FRONT ROW", col=BLUE, size=50, sound="pop")
    sign(cr, t, A("b8", "last"), 520, 480, "LAST ROW", col=RED, size=50, sound="pop")
    person(cr, t, 360, 900, 0.55, "kid", eyes="happy", mouth="grin", arms=("wave", "hips"))
    vignette(cr, 0.35)


SCENES = {"hook": scene_hook, "board": scene_board, "glare": scene_glare, "kid": scene_kid, "laugh": scene_laugh,
          "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    th.hook(cr, t, [("LAST ROW?", True), ("STOP SCROLLING", False)], end=tl.at("b2"), y=200, size=92)
    captions(cr, t, tl)
