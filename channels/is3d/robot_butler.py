"""Interestingly Strange in 3D, sample 1: "A Robot With 1 Rule. The Kid Found the Loophole."

Script: out/scripts_3d_sample.md (owner approved 18 Oct 2026; 3D asked for on 18 Oct: "I want ItsInterestinglyStrange
channel to adopt 3d animation ... make a sample"). Original genie-style story. 3D picture: scene_is3d.html?dir=robot
(directions/robot.js: the kid, Bolt the robot butler, the teacher; bedroom and classroom). This module adds the hook,
the logic cards, signs, the closing buttons, captions and sound. Turbo stock female narrator with tags; the kid, Bolt
and the teacher through Turbo with Kokoro reference voices.

    python channels/is3d/make_is3d.py robot_butler
"""
import os

from motion import thriller as th, voice
from motion.engine import FPS, W, cairo, cue, hexc, seg
from motion.polish import OUTLINE, WHITE, appear, bold_text, captions, rrect, sign, stamp, vignette

NARRATOR = dict(turbo=True)
DIRECTION = "robot"
TAIL = 1.0
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build",
                      "is3d", "robot_frames")

voice.SPEAKERS.update({
    "kid": dict(voice="am_puck", speed=1.04, pitch=2.5, turbo_ref="am_puck+3"),
    "bolt": dict(voice="bm_george", speed=0.95, turbo_ref="bm_george"),
    "teacher": dict(voice="af_bella", speed=1.0, turbo_ref="af_bella"),
})

SCRIPT = [
    dict(id="r1", scene="bed_wide", text="A robot butler has one rule. Always do what's best for the kid."),
    dict(id="r2", scene="kid_close", text="Bolt. What's best for me today, is no school. [chuckle]", speaker="kid"),
    dict(id="r3", scene="bolt_close", text="The robot freezes."),
    dict(id="r4", scene="bed_side", text="If it lets him skip, he falls behind. That's not best for him."),
    dict(id="r5", scene="kid_close", text="If it drags him to school, he's miserable. That's not best either."),
    dict(id="r6", scene="bolt_close", text="Either way, it breaks its own rule."),
    dict(id="r7", scene="bolt_close", text="Calculating. Solution found.", speaker="bolt", gap=0.3),
    dict(id="r8", scene="class_wide", text="Ten minutes later, a robot walks into class. And sits in the last row."),
    dict(id="r9", scene="teacher_close", text="Who are you?", speaker="teacher", gap=0.3),
    dict(id="r10", scene="bolt_class", text="I am here for the kid. I will learn for him.", speaker="bolt"),
    dict(id="r11", scene="class_wide", text="The robot gets every answer right. And that night, it hands the kid ten "
                                            "pages of notes. [laugh]"),
    dict(id="r12", scene="bed_night", text="Engineers building real A.I. argue about this exact rule."),
    dict(id="r13", scene="bed_night", text="So who should decide what's best for you? You, or the machine?", gap=0.3),
]

METADATA = dict(
    title="A Robot With 1 Rule. The Kid Found the Loophole. 🤖",
    alt_titles=["The Kid Told His Robot: No School Today 🤖", "This Robot Went to School Instead of Him 🤖"],
    description="""A robot butler has one rule: always do what's best for the kid. 🤖

The kid: "What's best for me today is no school." 😏

If the robot lets him skip, he falls behind. If it drags him to school, he's miserable. Either way, it breaks its own rule... so it finds a third option. 🏫

A short story with a twist (fiction). Engineers building real AI argue about this exact rule.

💬 Who should decide what's best for you: you, or the machine? 👇

🔔 Interestingly Strange: clever twists, The Last Bencher and mind-bending paradoxes, animated in under a minute.""",
    hashtags=["#Robot", "#PlotTwist", "#Shorts"],
    tags=["robot story", "robot butler", "ai rules", "kid outsmarts robot", "plot twist", "school story",
          "funny robot", "ai ethics", "3d animation", "interestingly strange"],
    pinned_comment="Who should decide what's best for you: you 🙋 or the machine 🤖? Pick a side 👇",
)

RED, GREEN, GOLD, BLUE, PURPLE = (hexc(c) for c in ("#e8473f", "#3fbf6a", "#ffcf3f", "#4aa3f0", "#7a5bd0"))
_n_frames = []


def _frame(t):
    if not _n_frames:
        _n_frames.append(len(os.listdir(FRAMES)))
    i = min(int(round(t * FPS)), _n_frames[0] - 1)
    return cairo.ImageSurface.create_from_png(os.path.join(FRAMES, f"f{i:05d}.png"))


def card(cr, t, start, end, y, left, right, col):
    """A logic card: LEFT -> RIGHT, crossed out."""
    if t < start or t > end + 0.2:
        return
    k = max(0.01, appear(t, start, 0.35)) * (1 - seg(t, end, end + 0.2))
    cr.save()
    cr.translate(W / 2, y)
    cr.scale(k, k)
    rrect(cr, -320, -62, 640, 124, 30)
    cr.set_source_rgba(1, 1, 1, 0.93)
    cr.fill_preserve()
    cr.set_source_rgba(*OUTLINE[:3], 1)
    cr.set_line_width(6)
    cr.stroke()
    bold_text(cr, left, -150, 16, 46, col)
    bold_text(cr, "->", -8, 14, 40, OUTLINE, outline=None, shadow=0)
    bold_text(cr, right, 155, 16, 42, RED)
    if t >= start + 0.6:                                   # crossed out
        u = seg(t, start + 0.6, start + 0.85)
        cr.set_source_rgba(*RED[:3], 0.9)
        cr.set_line_width(10)
        cr.move_to(-290, -40)
        cr.line_to(-290 + 580 * u, -40 + 80 * u)
        cr.stroke()
    cr.restore()


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.35)
    A, B = tl.at, tl.by_id
    th.hook(cr, t, [("ONE RULE:", False), ("DO WHAT'S BEST", True), ("FOR THE KID", True)], end=A("r2"), y=150,
            size=88)
    sign(cr, t, A("r3", "freezes."), 360, 200, "FROZEN", col=BLUE, size=70, end=B["r3"].end + 0.2)
    card(cr, t, A("r4", "skip,"), B["r5"].start - 0.05, 260, "SKIP", "FALLS BEHIND", BLUE)
    card(cr, t, A("r5", "school,"), B["r6"].start - 0.05, 260, "SCHOOL", "MISERABLE", PURPLE)
    if B["r6"].start <= t < B["r7"].start:
        stamp(cr, t, A("r6", "breaks"), 360, 250, "RULE BROKEN", col=RED, size=70)
    sign(cr, t, A("r7", "Solution"), 360, 220, "SOLUTION FOUND", col=GREEN, size=62, end=B["r7"].end + 0.3)
    sign(cr, t, A("r8"), 360, 180, "10 MINUTES LATER", col=GOLD, size=56, end=A("r8", "And") - 0.05)
    sign(cr, t, A("r8", "last"), 360, 180, "THE LAST ROW", col=RED, size=62, end=B["r8"].end + 0.3)
    sign(cr, t, A("r11", "right."), 360, 190, "100% RIGHT", col=GREEN, size=66, end=A("r11", "night,") - 0.05)
    sign(cr, t, A("r11", "ten"), 360, 190, "10 PAGES OF NOTES", col=PURPLE, size=56, end=B["r11"].end + 0.3)
    sign(cr, t, A("r12", "Engineers"), 360, 220, "WHAT'S BEST FOR YOU?", col=GOLD, size=54, end=B["r12"].end + 0.2)
    if t >= B["r13"].start:
        sign(cr, t, A("r13", "decide"), 360, 200, "WHO DECIDES?", col=GOLD, size=62)
        sign(cr, t, A("r13", "You,"), 190, 400, "ME", col=GREEN, size=78, rot=-0.06)
        sign(cr, t, A("r13", "machine?"), 520, 400, "THE MACHINE", col=BLUE, size=48, rot=0.05)

    cue("ding", t, 0.05)
    cue("whoosh", t, B["r8"].start)
    cue("hit", t, A("r6", "breaks"))
    cue("ding", t, A("r7", "Solution"))
    cue("step", t, A("r8", "walks"))
    cue("thud", t, A("r11", "ten") + 0.3)
    captions(cr, t, tl)
