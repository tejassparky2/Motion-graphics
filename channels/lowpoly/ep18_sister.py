"""Low-poly channel, episode 18 (happy): "My Little Sister Asked Me to Make Her Cat Jump".

Script: channels/lowpoly/scripts/batch5_eps16-19.md (auto-approved by the owner, 21 Oct 2026). Dev, his 7-year-old
sister (guest), Claude; a sunny afternoon. Built on research_notes/Emotional AI dev skits that connect/.
Fiction; parody, not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep18_sister
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import frames, mono, pill_caption, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cairo, cue, hexc, seg   # noqa: E402
from motion.polish import appear, rrect, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep18"
MUSIC = "score"
SCORE = [(0, "light"), ("c6", "out"), ("c8", "light"), ("c18", "tender", -0.3), ("c24", "out"), ("c26", "tender"),
         ("c28", "swell"), ("c33", "light")]
TAIL = 0.7
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep18_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart"),
                       "kid": dict(voice="af_sky", speed=1.0, turbo_ref="af_sky+4")})

voice.CLONE_RATE = 4.3   # skits: Turbo's natural pace, slowed a touch, never sped up (refs ~165 wpm while speaking)
GAP = 1.15               # and a little more air between lines (refs: 10-21 pauses over 0.6 s a minute)

DEV, CL, KID = None, "claude", "kid"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("c1", "kid", KID, "Can you make my cat jump?", 0, 1),
    ("c2", "devmid", DEV, "I'm working.", .8, 1),
    ("c3", "kid", KID, "On what?", .6, 1),
    ("c4", "devmid", DEV, "Stuff.", .7, 1),
    ("c5", "kidclose", KID, "Is it fun?", .8, 1),
    ("c6", "devclose", DEV, "", .2, 1),
    ("c7", "devclose", DEV, "No.", .2, .9),
    ("c8", "two", KID, "Claude, can you make my cat jump?", 1.0, 1),
    ("c9", "solo", CL, "I can. Want to make it together?", .7, 1),
    ("c10", "kidclose", KID, "Me?", .6, 1),
    ("c11", "solo", CL, "Type: jump.", .7, 1),
    ("c12", "screen", DEV, "", .2, 1),
    ("c13", "kidclose", KID, "It jumped! [laugh]", .2, 1),
    ("c14", "kid", KID, "Make it jump a hundred!", .7, 1),
    ("c15", "screen", DEV, "", .2, 1),
    ("c16", "kidclose", KID, "Where did it go?", .2, 1),
    ("c17", "solo", CL, "Space. A hundred is a lot.", .7, 1),
    ("c18", "devmid", DEV, "Try ten.", .9, 1),
    ("c19", "screen", DEV, "", .2, 1),
    ("c20", "kid", KID, "Did you do this when you were little?", .8, 1),
    ("c21", "devclose", DEV, "I was seven. Like you.", .9, .92),
    ("c22", "devclose", DEV, "I made a ball bounce. I didn't sleep all night.", .7, .95),
    ("c23", "kidclose", KID, "Why did you stop?", .9, 1),
    ("c24", "devclose", DEV, "", .2, 1),
    ("c25", "devclose", DEV, "I forgot it was fun.", .2, .9),
    ("c26", "kid", KID, "Can we make it do a flip?", 1.0, 1),
    ("c27", "devmid", DEV, "Yeah. [chuckle]", .6, 1),
    ("c28", "highwide", DEV, "", .2, 1),
    ("c29", "kid", KID, "Is this your job?", .2, 1),
    ("c30", "devmid", DEV, "Kind of.", .7, 1),
    ("c31", "kidclose", KID, "Your job is the best job.", .7, 1),
    ("c32", "devclose", DEV, "Yeah. It is.", .9, .92),
    ("c33", "kid", KID, "Mom! Dev's job is fun!", .8, 1),
    ("c34", "devmid", DEV, "Don't tell my boss.", .5, 1),
]
HOLDS = {"c6": 1.4, "c12": 1.6, "c15": 1.1, "c19": 1.1, "c24": 1.6, "c28": 2.4}
SCRIPT = []
for i, (bid, shot, who, text, gap, pace) in enumerate(_lines):
    d = dict(id=bid, scene=shot, text=text)
    if who:
        d["speaker"] = who
    if i:
        d["gap"] = round(gap * GAP, 2)
    if pace != 1:
        d["pace"] = pace
    if not text:
        d["hold"] = HOLDS[bid]
    SCRIPT.append(d)

METADATA = dict(
    title="My Little Sister Asked Me to Make Her Cat Jump",
    alt_titles=["\"Is Your Job Fun?\" \"...No.\"", "I Forgot Coding Was Fun. My Sister Reminded Me."],
    description=""""Is it fun?" "...No."
His 7-year-old sister just wanted her cat to jump. Claude let her type the code herself.

Inspired by a real story on Hacker News: a dad and his 5-year-old built a giant Minecraft egg with a generator made
with Claude, and the boy talked about circles and radiuses for days. This story is fiction.

Ep. 18 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 AI can write the code now. Should kids still learn to code? 👇""",
    hashtags=["#ClaudeCode", "#LearnToCode", "#DevLife"],
    tags=["kids coding", "learn to code", "claude", "coding for kids", "programmer life", "burnout",
          "developer life", "ai coding", "wholesome", "little sister"],
    pinned_comment="AI can write the code now. Should kids still learn to code? 👇 Subscribe for the next one.",
)
GREEN, GREY, YEL, ORANGE, CREAM = (hexc(c) for c in ("#7ee08a", "#8a93a6", "#ffd23f", "#e8865a", "#f3e9d8"))


def cat(cr, x, y, s, rot=0.0, k=1.0):
    """A crayon cat face, like a kid's drawing."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.set_line_width(5)
    cr.set_source_rgba(1.0, 0.6, 0.25, k)
    cr.move_to(-38, -20); cr.line_to(-30, -62); cr.line_to(-8, -36); cr.close_path()
    cr.move_to(38, -20); cr.line_to(30, -62); cr.line_to(8, -36); cr.close_path()
    cr.fill()
    cr.arc(0, 0, 44, 0, 2 * math.pi)
    cr.fill()
    cr.set_source_rgba(0.15, 0.1, 0.1, k)
    for ex in (-15, 15):
        cr.arc(ex, -6, 6, 0, 2 * math.pi)
        cr.fill()
    cr.move_to(-8, 12); cr.curve_to(-4, 18, 4, 18, 8, 12); cr.stroke()
    for sgn in (-1, 1):
        for dy in (-4, 6):
            cr.move_to(sgn * 20, 8 + dy * .5); cr.line_to(sgn * 60, 2 + dy); cr.stroke()
    cr.restore()


def code_screen(cr, t, tl):
    """The little program: a code line she types and the cat it moves (jump, jump(100), jump(10), flip)."""
    B = tl.by_id
    start, end = B["c11"].end, B["c28"].end + 0.4
    if not (start - 0.2 <= t < end):
        return
    k = appear(t, start - 0.2, 0.3) * (1 - seg(t, end - 0.3, end))
    from motion.engine import W
    x0, y0, w, h = W / 2 - 300, 690, 600, 420
    cr.save()
    rrect(cr, x0, y0, w, h, 20)
    cr.set_source_rgba(0.98, 0.97, 0.93, 0.96 * k)
    cr.fill()
    if t < B["c14"].end:
        code, kind, t0 = "cat.jump()"[:max(0, int((t - B["c12"].start) * 6))], "jump", B["c12"].start + 1.6
    elif t < B["c18"].end:
        code, kind, t0 = "cat.jump(100)", "space", B["c15"].start + 0.3
    elif t < B["c26"].start:
        code, kind, t0 = "cat.jump(10)", "jump", B["c19"].start + 0.2
    else:
        code, kind, t0 = "cat.flip()", "flip", B["c28"].start + 0.3
    mono(cr, code, x0 + 30, y0 + 52, 30, (0.2, 0.25, 0.45), k)
    gx, gy = W / 2, y0 + h - 70
    cr.set_source_rgba(0.55, 0.8, 0.45, k)
    rrect(cr, x0 + 20, gy + 40, w - 40, 14, 7)
    cr.fill()
    u = t - t0
    if kind == "space":
        y = gy - (0 if u < 0 else 1600 * u * u + 300 * u)
        cat(cr, gx, y, 1.0, 0, k)
    elif kind == "flip":
        q = (u % 1.6) / 1.0
        y = gy - (220 * math.sin(math.pi * q) if 0 <= q < 1 else 0)
        cat(cr, gx, y, 1.0, 2 * math.pi * min(max(q, 0), 1), k)
    else:
        q = (u % 1.3) / 0.8
        y = gy - (180 * math.sin(math.pi * q) if 0 <= q < 1 and u >= 0 else 0)
        cat(cr, gx, y, 1.0, 0, k)
    cr.restore()


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.55)
    th.grain(cr, t, 0.04)
    A, B = tl.at, tl.by_id
    if t < B["c3"].end:                         # her drawing, held up for him
        k = appear(t, 0.0, 0.2) * (1 - seg(t, B["c3"].end - 0.2, B["c3"].end))
        from motion.engine import W
        cr.save()
        rrect(cr, W / 2 - 170, 760, 340, 300, 14)
        cr.set_source_rgba(0.99, 0.98, 0.95, 0.96 * k)
        cr.fill()
        cat(cr, W / 2, 905, 1.2, -0.08, k)
        cr.restore()
    code_screen(cr, t, tl)
    cue("typing", t, B["c12"].start + 0.2, 1.0)
    cue("pop", t, B["c12"].start + 1.6)
    cue("typing", t, B["c15"].start, 0.5)
    cue("whoosh", t, B["c15"].start + 0.3)
    cue("pop", t, B["c19"].start + 0.2)
    cue("typing", t, B["c28"].start + 0.1, 1.6)
    cue("hush", t, B["c24"].start - 0.1, B["c24"].end - B["c24"].start + 0.2)
    th.hook(cr, t, [("MY LITTLE SISTER ASKED ME", False), ("TO MAKE HER CAT JUMP", True)], end=A("c1", end=True) + 0.6, y=175, size=66)
    pill_caption(cr, t, tl)
