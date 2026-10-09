"""The Paradox of the Court (Protagoras and his student) -- Pinocchio-style paradox in the polished look.

Aulus Gellius, Attic Nights 5.10: Protagoras taught a pupil (Euathlus) on the terms that the fee be paid when the
pupil won his first case; the pupil never took a case; Protagoras sued. Each side argued he wins whichever way the
court rules; the jurors, finding both pleas "uncertain and insoluble", postponed the case to a distant day.
Script approved by the owner on 9 Oct 2026 (out/scripts_paradox_batch2.md) with an everyday example, a clever
closing question and character voices added at the owner's request.
"""
import math
import random

from motion import voice
from motion.engine import W, H, cue, ease_out, hexc, lerp, seg
from motion.kit import whip
from motion.pkit import (BLUE, GOLD, GREEN, INKC, PURPLE, RED, bubble, buttons, calendar, card, check, knot,
                         red_x, shake, sparkles, studio, tag)
from motion.polish import (OUTLINE, WHITE, alpha, appear, bold_text, camera, captions, ellipse, enter, ground_shadow,
                           light_rays, lin, paint, put, rad, rrect, shade, sign, smooth, soft_rrect, sprite, stamp,
                           stroke_line, vignette)
from motion.toons import person, portrait

NARRATOR = dict()
TAIL = 0.9
voice.SPEAKERS.update({"prof": dict(voice="bm_george", speed=0.98), "student": dict(voice="am_puck", speed=1.06)})

SCRIPT = [
    dict(id="c1", scene="hook", text="A teacher sued his own student. And the judges couldn't decide who wins."),
    dict(id="c2", scene="intro", text="Ancient Greece. Protagoras teaches people how to win in court."),
    dict(id="c3", scene="deal", text="His student makes a deal. He'll pay only after he wins his first case."),
    dict(id="c4", scene="never", text="Then the student never takes a case. So he never pays."),
    dict(id="c5", scene="example", text="It's like a friend who says: I'll pay you back after my first salary. Then he "
                                        "never takes a job."),
    dict(id="c6", scene="sue", text="So Protagoras sues him. Now listen to both sides.", gap=0.3),
    dict(id="c7", scene="prof", text="Protagoras says. If I win, the court makes you pay.", speaker="prof",
         speaker_from="If", gap=0.3),
    dict(id="c8", scene="prof", text="If I lose, you've won your first case. So you pay anyway!", speaker="prof"),
    dict(id="c9", scene="student", text="The student says. If I win, the court says I don't pay.",
         speaker="student", speaker_from="If", gap=0.4),
    dict(id="c10", scene="student", text="If I lose, I still haven't won a case. So I don't pay!", speaker="student"),
    dict(id="c11", scene="clash", text="Both of them are right. And both of them are wrong.", gap=0.4, pace=0.95),
    dict(id="c12", scene="giveup", text="The old story says the judges gave up. They postponed the case to a day far, "
                                        "far away."),
    dict(id="c13", scene="end", text="So you're the judge. Who pays? Careful. Whoever loses... wins.", gap=0.3,
         pace=0.95),
]

METADATA = dict(
    title="He Sued His Own Student. And Nobody Could Win. ⚖️",
    alt_titles=["The 2,000-Year-Old Lawsuit Nobody Can Solve ⚖️ (Paradox of the Court)",
                "Whoever Loses This Case... Wins 🤯"],
    description="""A teacher sued his own student, and the judges couldn't decide who wins. ⚖️

Ancient Greece: Protagoras teaches people how to win in court. His student makes a deal: he'll pay only after he wins his first case. Then he never takes a case, so he never pays. (Like a friend who says "I'll pay you back after my first salary", then never takes a job.)

So Protagoras sues him.
Protagoras: "If I win, the court makes you pay. If I lose, you've won your first case, so you pay anyway!"
The student: "If I win, the court says I don't pay. If I lose, I still haven't won a case, so I don't pay!"

Both of them are right, and both of them are wrong. The old story says the judges gave up and postponed the case to a day far, far away.

Source: Aulus Gellius, Attic Nights, Book 5, chapter 10 (2nd century AD): the "Paradox of the Court".

💬 You're the judge. Who pays? Careful: whoever loses... wins. 👇

🔔 Interestingly Strange: mind-bending paradoxes, weird animals, bizarre history and strange stories, animated in under a minute.""",
    hashtags=["#Paradox", "#Logic", "#Shorts"],
    tags=["paradox of the court", "protagoras paradox", "protagoras and euathlus", "logic paradox", "paradox",
          "brain teaser", "ancient greece", "lawyer paradox", "mind blowing", "interestingly strange"],
    pinned_comment="You're the judge 👨‍⚖️ Who pays: the student, or nobody? Explain your ruling 👇",
)

MARBLE = hexc("#efe8dc")


# ---------------------------------------------------------------- backgrounds
def _court(c):
    c.rectangle(0, 0, W, H)
    c.set_source(lin(0, 0, 0, H, [(0, hexc("#8fc8f0")), (0.5, hexc("#dff0fa")), (0.52, hexc("#d8cdbb")),
                                  (1, hexc("#a8977e"))]))
    c.fill()
    c.rectangle(0, 140, W, 520)        # back wall
    c.set_source(lin(0, 140, 0, 660, [(0, hexc("#f4efe6")), (1, hexc("#ddd2c0"))]))
    c.fill()
    c.move_to(-20, 150)                 # pediment
    c.line_to(W / 2, 40)
    c.line_to(W + 20, 150)
    c.close_path()
    paint(c, lin(0, 40, 0, 150, [(0, WHITE), (1, hexc("#e4dccc"))]), alpha(OUTLINE, 0.6), 5)
    for k in range(5):                 # columns
        x = 40 + k * 160
        rrect(c, x, 170, 64, 490, 6)
        paint(c, lin(x, 0, x + 64, 0, [(0, hexc("#e8e0d0")), (0.4, WHITE), (1, hexc("#cfc4b0"))]),
              alpha(OUTLINE, 0.5), 3)
        for j in range(3):
            c.rectangle(x + 12 + j * 16, 186, 4, 460)
            c.set_source_rgba(0, 0, 0, 0.05)
            c.fill()
        rrect(c, x - 10, 160, 84, 22, 4)
        paint(c, hexc("#f6f1e8"), alpha(OUTLINE, 0.5), 3)
    for k in range(14):                 # floor tiles
        y = 660 + k * k * 4.5
        c.rectangle(0, y, W, 2)
        c.set_source_rgba(0.3, 0.25, 0.2, 0.15)
        c.fill()


def court(cr, t):
    put(cr, sprite("court_bg", W, H, _court), 0, 0)
    light_rays(cr, t, 560, 60, n=4, a=0.06)


def bench(cr, x, y, w=320):
    """The judges' stone bench (front face), top edge at y."""
    soft_rrect(cr, x - w / 2, y + 10, w, 200, 14, (0, 0, 0, 0.3), sigma=10)
    rrect(cr, x - w / 2, y, w, 200, 14)
    paint(cr, lin(0, y, 0, y + 200, [(0, WHITE), (1, hexc("#cfc4b0"))]), OUTLINE, 6)
    rrect(cr, x - w / 2 - 14, y - 16, w + 28, 26, 10)
    paint(cr, lin(0, y - 16, 0, y + 10, [(0, WHITE), (1, MARBLE)]), OUTLINE, 5)
    cr.arc(x, y + 96, 44, 0, 2 * math.pi)       # a laurel wreath emblem
    paint(cr, None, hexc("#5aa043"), 8)
    for k in range(10):
        a = -math.pi / 2 + (k - 4.5) * 0.55
        ellipse(cr, x + math.cos(a) * 44, y + 96 + math.sin(a) * 44, 12, 6, a + 1.4)
        paint(cr, hexc("#5aa043"), OUTLINE, 2.5)


def gavel(cr, hx, hy, ang=0.0):
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(-0.8 + ang)
    rrect(cr, -6, -10, 12, 90, 5)
    paint(cr, hexc("#7a4a2a"), OUTLINE, 3.5)
    rrect(cr, -30, -40, 60, 34, 10)
    paint(cr, lin(0, -40, 0, -6, [(0, hexc("#c9824a")), (1, hexc("#7a4a2a"))]), OUTLINE, 4)
    cr.restore()


def scroll(cr, hx, hy):
    cr.save()
    cr.translate(hx + 10, hy - 30)
    cr.rotate(-0.2)
    rrect(cr, -18, -60, 70, 120, 8)
    paint(cr, lin(0, -60, 0, 60, [(0, hexc("#fff6dc")), (1, hexc("#e8d6a8"))]), OUTLINE, 4)
    for k in range(4):
        stroke_line(cr, [(-6, -36 + k * 22), (40, -36 + k * 22)], 3, alpha(OUTLINE, 0.4), curve=False)
    for yy in (-60, 60):
        ellipse(cr, 17, yy, 42, 10)
        paint(cr, hexc("#c9a46a"), OUTLINE, 4)
    cr.restore()


def phone(cr, hx, hy):
    cr.save()
    cr.translate(hx + 6, hy - 40)
    cr.rotate(0.15)
    rrect(cr, -26, -48, 52, 96, 10)
    paint(cr, hexc("#2b2b33"), OUTLINE, 4)
    rrect(cr, -20, -40, 40, 78, 6)
    paint(cr, lin(0, -40, 0, 38, [(0, hexc("#7cc6ff")), (1, hexc("#4a6ad0"))]), None, 0)
    cr.restore()


def couch(cr, x, y, w=420):
    col = hexc("#8a4fc9")
    rrect(cr, x - w / 2, y - 190, w, 130, 34)
    paint(cr, lin(0, y - 190, 0, y - 60, [(0, shade(col, 0.3)), (1, col)]), OUTLINE, 6)
    rrect(cr, x - w / 2 + 20, y - 90, w - 40, 70, 24)
    paint(cr, lin(0, y - 90, 0, y - 20, [(0, shade(col, 0.4)), (1, shade(col, 0.05))]), OUTLINE, 6)
    for side in (-1, 1):
        rrect(cr, x + side * (w / 2 - 30) - 40, y - 140, 80, 120, 30)
        paint(cr, lin(0, y - 140, 0, y - 20, [(0, shade(col, 0.35)), (1, shade(col, -0.1))]), OUTLINE, 6)


def mouth(tl, who, t, rest="smile"):
    return "talk" if tl.speaking(who, t) else rest


# ---------------------------------------------------------------- scenes
def scene_hook(cr, t, tl):
    A = tl.at
    court(cr, t)
    dx, dy = shake(t, A("c1", "sued"), 0.35, 8)
    cam = camera(t, [(0, (1.0, 360, 640)), (A("c1", "judges"), (1.12, 360, 600))], dur=0.8)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, cam)
    stuck = t >= A("c1", "judges")
    person(cr, t, 360, 690, 0.7, "judge", eyes="wide" if stuck else "half", mouth="o" if stuck else "flat",
           brows="up" if stuck else None, arms=("chin", "down"), sweat=stuck, shadow=False)
    bench(cr, 360, 560, 300)
    person(cr, t, 150, 900, 0.88, "protagoras", eyes="angry", mouth="flat", brows="angry", arms=("point", "hips"),
           look=(0.6, 0))
    person(cr, t, 575, 900, 0.88, "student_gr", eyes="angry", mouth="smug", brows="angry", arms=("hips", "hips"),
           facing=-1, look=(0.6, 0))
    cr.restore()
    sign(cr, t, 0.05, 360, 160, "TEACHER VS STUDENT", col=RED, size=54, end=A("c1", "judges") - 0.05)
    if stuck:
        bold_text(cr, "?", 360, 330 + math.sin(t * 5) * 8, 150 * appear(t, A("c1", "judges"), 0.4), GOLD)
    sign(cr, t, A("c1", "decide"), 360, 160, "NO ONE CAN WIN?", col=PURPLE, size=56)
    vignette(cr, 0.4)


def scene_intro(cr, t, tl):
    A = tl.at
    court(cr, t)
    cr.save()
    enter(cr, camera(t, [(A("c2") - 0.3, (1.15, 330, 600))]))
    person(cr, t, 330, 900, 1.0, "protagoras", eyes="happy" if t >= A("c2", "win") else "open", mouth="grin",
           arms=("hold", "point"), hold=scroll)
    cr.restore()
    sign(cr, t, A("c2"), 360, 150, "ANCIENT GREECE", col=BLUE, size=60, end=A("c2", "Protagoras") - 0.05)
    tag(cr, t, A("c2", "Protagoras"), 330, 300, "PROTAGORAS", col=hexc("#c9a6ff"))
    sign(cr, t, A("c2", "win"), 360, 150, "HOW TO WIN IN COURT", col=GOLD, size=50)
    vignette(cr, 0.4)


def scene_deal(cr, t, tl):
    A = tl.at
    court(cr, t)
    shake_t = A("c3", "deal.")
    cr.save()
    enter(cr, camera(t, [(A("c3") - 0.3, (1.05, 360, 620))]))
    together = ease_out(seg(t, A("c3"), shake_t))
    person(cr, t, lerp(120, 230, together), 900, 0.9, "protagoras", eyes="happy", mouth="grin",
           arms=("out", "down") if t >= shake_t else ("hips", "down"))
    person(cr, t, lerp(600, 490, together), 900, 0.9, "student_gr", eyes="happy", mouth="grin", facing=-1,
           arms=("out", "down") if t >= shake_t else ("hips", "down"))
    cr.restore()
    sparkles(cr, t, shake_t, 360, 600, n=7, seed=3, col=GOLD)
    card(cr, t, A("c3", "pay"), 360, 260, 520, 210, "THE DEAL", ["Pay only after", "your FIRST WIN"], col=GREEN)
    vignette(cr, 0.4)


def scene_never(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#ffd6a8"), hexc("#fff1d6"), seed=4)
    couch(cr, 300, 900, 440)
    person(cr, t, 300, 850, 0.82, "student_gr", eyes="happy", mouth="smug", arms=("chin", "hips"), tilt=-0.12,
           shadow=False)
    pages = ("DAY 1", "DAY 30", "DAY 365", "DAY 900")
    st = A("c4", "never")
    k = min(3, int(max(0.0, t - st) / 0.35)) if t >= st else 0
    calendar(cr, t, st, 560, 330, "CASES TAKEN: 0", pages[k], col=RED)
    if t >= A("c4", "pays."):
        person(cr, t, 620, 900, 0.62, "protagoras", eyes="angry", mouth="flat", brows="angry", arms=("hips", "hips"),
               facing=-1)
    stamp(cr, t, A("c4", "pays."), 300, 180, "NEVER PAYS", col=RED, size=70)
    vignette(cr, 0.35)


def scene_example(cr, t, tl):
    A = tl.at
    studio(cr, t, hexc("#9fd8ff"), hexc("#fff1d6"), seed=6)
    friend = dict(fedora=None, suit=None, shirt=hexc("#ff8a3c"), pants=hexc("#3b5b9a"), tie=None)
    person(cr, t, 200, 880, 0.85, "reporter", eyes="happy", mouth="talk" if t < A("c5", "Then") else "grin",
           arms=("hold", "down"), hold=phone, **friend)
    later = t >= A("c5", "never")
    person(cr, t, 540, 880, 0.85, "villager", beard=None, shirt=hexc("#4aa3f0"), eyes="half" if later else "open",
           mouth="flat" if later else "smile", arms=("hips", "hips") if later else ("down", "down"), facing=-1,
           sweat=later)
    bubble(cr, t, A("c5", "I'll"), 300, 330, "I'll pay you back after", size=40, tail=-1, end=A("c5", "Then") - 0.05)
    bubble(cr, t, A("c5", "salary."), 300, 420, "my FIRST SALARY!", size=44, tail=-1, col=hexc("#fff3c4"),
           end=A("c5", "Then") - 0.05)
    sign(cr, t, A("c5"), 360, 150, "LIKE THIS FRIEND", col=BLUE, size=56, end=A("c5", "Then") - 0.05)
    sign(cr, t, A("c5", "Then"), 360, 150, "JOBS TAKEN: 0", col=RED, size=62)
    vignette(cr, 0.35)


def scene_sue(cr, t, tl):
    A = tl.at
    court(cr, t)
    bang = A("c6", "sues")
    dx, dy = shake(t, bang + 0.15, 0.35, 10)
    cr.save()
    cr.translate(dx, dy)
    enter(cr, camera(t, [(A("c6") - 0.3, (1.0, 360, 640))]))
    hit = seg(t, bang, bang + 0.18)
    person(cr, t, 360, 690, 0.7, "judge", eyes="angry", mouth="flat", arms=("hold", "down"), shadow=False,
           hold=lambda c, hx, hy: gavel(c, hx, hy, -0.9 * math.sin(hit * math.pi)))
    bench(cr, 360, 560, 300)
    person(cr, t, 150, 900, 0.88, "protagoras", eyes="half", mouth="smug", arms=("point", "hips"))
    person(cr, t, 575, 900, 0.88, "student_gr", eyes="wide", mouth="o", arms=("hips", "hips"), facing=-1)
    cr.restore()
    if t >= bang + 0.15:
        cue("hit", t, bang + 0.15)
    stamp(cr, t, bang + 0.15, 360, 170, "SUED!", col=RED, size=100)
    tag(cr, t, A("c6", "both"), 150, 420, "SIDE 1", col=hexc("#c9a6ff"))
    tag(cr, t, A("c6", "sides."), 575, 420, "SIDE 2", col=GREEN)
    vignette(cr, 0.4)


def scene_prof(cr, t, tl):
    A = tl.at
    court(cr, t)
    c8 = A("c8")
    cr.save()
    enter(cr, camera(t, [(A("c7") - 0.3, (1.25, 260, 600))]))
    person(cr, t, 200, 900, 1.0, "protagoras", eyes="half", mouth=mouth(tl, "prof", t, "smug"), brows="raise",
           arms=("point", "hips") if t < c8 else ("up", "hips"))
    cr.restore()
    card(cr, t, A("c7", "If"), 500, 330, 380, 220, "IF I WIN", ["The court says:", "YOU PAY"], col=PURPLE,
         mark="ok", mark_at=A("c7", "pay."))
    card(cr, t, c8, 500, 610, 380, 250, "IF I LOSE", ["You won a case.", "Deal says:", "YOU PAY"], col=PURPLE,
         mark="ok", mark_at=A("c8", "anyway!"))
    tag(cr, t, A("c7"), 200, 250, "PROTAGORAS", col=hexc("#c9a6ff"), end=A("c7", "If") - 0.05)
    vignette(cr, 0.4)


def scene_student(cr, t, tl):
    A = tl.at
    court(cr, t)
    c10 = A("c10")
    cr.save()
    enter(cr, camera(t, [(A("c9") - 0.3, (1.25, 460, 600))]))
    person(cr, t, 520, 900, 1.0, "student_gr", eyes="half", mouth=mouth(tl, "student", t, "smug"), brows="raise",
           arms=("point", "hips") if t < c10 else ("shrug", "shrug"), facing=-1)
    cr.restore()
    card(cr, t, A("c9", "If"), 220, 330, 380, 220, "IF I WIN", ["The court says:", "NO PAY"], col=GREEN,
         mark="no", mark_at=A("c9", "pay."))
    card(cr, t, c10, 220, 610, 380, 250, "IF I LOSE", ["Still no win.", "Deal says:", "NO PAY"], col=GREEN,
         mark="no", mark_at=A("c10", "pay!"))
    tag(cr, t, A("c9"), 520, 250, "THE STUDENT", col=GREEN, end=A("c9", "If") - 0.05)
    vignette(cr, 0.4)


def scene_clash(cr, t, tl):
    A = tl.at
    court(cr, t)
    wrong = A("c11", "wrong.")
    u = ease_out(seg(t, A("c11"), A("c11") + 0.6))
    card(cr, t, A("c11") - 0.2, lerp(-60, 210, u), 300, 360, 200, "TEACHER", ["Either way:", "YOU PAY"], col=PURPLE,
         rot=0.06)
    card(cr, t, A("c11") - 0.2, lerp(780, 510, u), 300, 360, 200, "STUDENT", ["Either way:", "NO PAY"], col=GREEN,
         rot=-0.06)
    if u >= 1:
        cue("hit", t, A("c11") + 0.6)
    cr.save()
    enter(cr, (1.0, 360, 640))
    person(cr, t, 360, 930, 0.7, "judge", eyes="wide", mouth="o", brows="up", arms=("face", "face"), sweat=True)
    cr.restore()
    stamp(cr, t, A("c11", "right."), 360, 480, "BOTH RIGHT", col=GREEN, size=64, rot=-0.08, end=wrong - 0.05)
    stamp(cr, t, wrong, 360, 480, "BOTH WRONG", col=RED, size=64, rot=0.08)
    vignette(cr, 0.4)


def scene_giveup(cr, t, tl):
    A = tl.at
    court(cr, t)
    gone = A("c12", "postponed")
    walk = seg(t, A("c12", "gave"), A("c12", "gave") + 2.5)
    cr.save()
    enter(cr, (1.0, 360, 640))
    bench(cr, 360, 560, 300)
    for k in range(3):
        x = lerp(220 + k * 140, 880 + k * 140, ease_out(walk) if t >= A("c12", "gave") else 0)
        person(cr, t, x, 900, 0.62, "judge", eyes="closed", mouth="flat", arms=("down", "down"), walk=t * 8,
               seed=k)
    cr.restore()
    pages = ("TOMORROW", "NEXT YEAR", "SOME DAY", "FAR AWAY")
    k = min(3, int(max(0.0, t - gone) / 0.45)) if t >= gone else 0
    calendar(cr, t, gone, 360, 360, "NEW DATE", pages[k], col=BLUE, s=1.15)
    sign(cr, t, A("c12", "gave"), 360, 150, "THE JUDGES GAVE UP", col=hexc("#5a6478"), size=50)
    vignette(cr, 0.4)


def scene_end(cr, t, tl):
    A = tl.at
    court(cr, t)
    cr.save()
    enter(cr, (1.0, 360, 640))
    bench(cr, 360, 640, 300)
    gavel(cr, 360, 600, 0.4 * math.sin(t * 3))
    person(cr, t, 120, 900, 0.72, "protagoras", eyes="half", mouth="smug", arms=("hips", "point"), look=(0.5, 0))
    person(cr, t, 600, 900, 0.72, "student_gr", eyes="half", mouth="smug", arms=("hips", "hips"), facing=-1,
           look=(0.5, 0))
    cr.restore()
    sign(cr, t, A("c13"), 360, 150, "YOU'RE THE JUDGE", col=GOLD, size=60)
    buttons(cr, t, A("c13", "pays?"), [("STUDENT PAYS", PURPLE), ("NOBODY PAYS", GREEN)], y=300, size=40, w=320)
    stamp(cr, t, A("c13", "wins."), 360, 480, "WHOEVER LOSES... WINS", col=RED, size=46, rot=-0.04)
    vignette(cr, 0.4)


SCENES = {"hook": scene_hook, "intro": scene_intro, "deal": scene_deal, "never": scene_never,
          "example": scene_example, "sue": scene_sue, "prof": scene_prof, "student": scene_student,
          "clash": scene_clash, "giveup": scene_giveup, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
