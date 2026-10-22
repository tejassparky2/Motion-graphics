"""Low-poly channel, episode 25 (comedy): "I Let My AI Be My Lawyer".

Script: channels/lowpoly/scripts/batch7_comedy_eps24-27.md (auto-approved by the owner, 22 Oct 2026). Dev and Claude;
a judge on a video call (a card and a voice only); morning. Real problem: made-up case law (Mata v. Avianca, 2023).
Fiction; parody, not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep25_lawyer
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, mono, pill_caption, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc, seg   # noqa: E402
from motion.polish import appear, rrect, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep25"
MUSIC = "score"
SCORE = [(0, "light"), ("k10", "out", -0.3), ("k12", "light"), ("k18", "out", -0.3)]
TAIL = 0.6
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep25_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart"),
                       "judge": dict(voice="bm_george", speed=0.95, turbo_ref="bm_george")})
skit_voice(voice)

DEV, CL, JG = None, "claude", "judge"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("k1", "devmid", DEV, "I'm fighting my parking ticket. In video court.", 0, 1),
    ("k2", "solo", CL, "Don't worry. I found three cases. [chuckle]", .7, 1),
    ("k3", "devclose", DEV, "Real ones?", .7, 1),
    ("k4", "soloclose", CL, "Smith versus Parking Meter. Twenty nineteen.", .5, 1),
    ("k5", "ots", JG, "Mister Dev. Your argument?", .9, 1),
    ("k6", "devclose", DEV, "Your honor. Smith versus Parking Meter.", .6, 1),
    ("k7", "ots", JG, "The meter was a party to the case?", .9, 1),
    ("k8", "soloclose", CL, "Also cite Lee versus Gravity.", .5, 1),
    ("k9", "devclose", DEV, "And Lee versus Gravity.", .5, 1),
    ("k10", "ots", JG, "Young man. None of these cases exist.", 1.0, .95),
    ("k11", "devclose", DEV, "", .2, 1),
    ("k12", "soloclose", CL, "You're absolutely right!", .2, 1),
    ("k13", "devclose", DEV, "Seriously, Claude?", .5, 1),
    ("k14", "ots", JG, "In twenty twenty-three, real lawyers were fined five thousand dollars for this.", .8, .95),
    ("k15", "devclose", DEV, "My ticket is forty dollars.", .8, 1),
    ("k16", "ots", JG, "The ticket stands. Forty dollars.", .7, 1),
    ("k17", "soloclose", CL, "I found a case where that ruling was overturned.", .7, 1),
    ("k18", "ots", JG, "Fifty dollars.", .7, 1),
]
HOLDS = {"k11": 1.3}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="I Let My AI Be My Lawyer",
    alt_titles=["\"Smith Versus Parking Meter, 2019.\"", "My AI Cited Lee Versus Gravity in Court"],
    description="""A forty-dollar parking ticket. Video court. Claude has three cases ready.
None of them exist.

Real: in Mata v. Avianca (June 2023), a New York judge fined two lawyers and their firm $5,000 for filing a brief
with court cases ChatGPT had made up. This story is fiction.

Ep. 25 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 Would you trust an AI as your lawyer? 👇""",
    hashtags=["#ClaudeCode", "#AI", "#Lawyer"],
    tags=["ai lawyer", "fake cases", "chatgpt lawyer", "ai hallucination", "claude", "parking ticket", "court",
          "you're absolutely right", "funny ai", "programmer humor"],
    pinned_comment="Would you trust an AI as your lawyer? 👇 Subscribe for the next one.",
)
GREY, RED, YEL, CREAM, WOOD = (hexc(c) for c in ("#8a93a6", "#ff5c5c", "#ffd23f", "#f3e9d8", "#8a5a3a"))


def judge_call(cr, t, tl):
    """The judge on a video call: a framed card with a stern judge (robe, glasses, gavel) who talks when speaking."""
    B = tl.by_id
    beats = tl.beats
    wins = [(b.start - 0.12, min(b.end + 0.3, beats[i + 1].start - 0.12) if i + 1 < len(beats) else tl.total)
            for i, b in enumerate(beats) if b.scene == "ots"]
    win = next(((a, z) for a, z in wins if a <= t < z), None)
    if not win:
        return
    k = min(appear(t, win[0], 0.2), 1 - seg(t, win[1] - 0.15, win[1]))
    from motion.engine import W
    x0, y0, w, h = W / 2 - 230, 410, 460, 330
    cr.save()
    rrect(cr, x0, y0, w, h, 20)
    cr.set_source_rgba(0.12, 0.1, 0.09, 0.95 * k)
    cr.fill()
    rrect(cr, x0 + 14, y0 + 48, w - 28, h - 62, 12)
    cr.set_source_rgba(0.42, 0.3, 0.22, k)
    cr.fill()
    mono(cr, "Traffic Court  ·  Virtual hearing", x0 + 20, y0 + 32, 19, (0.8, 0.75, 0.68), k)
    cx, cy = W / 2, y0 + 170
    talking = any(b.speaker == "judge" and b.start <= t < b.end for b in tl.beats)
    cr.set_source_rgba(0.08, 0.08, 0.1, k)                       # robe
    cr.move_to(cx - 120, y0 + h - 14); cr.curve_to(cx - 110, cy + 40, cx + 110, cy + 40, cx + 120, y0 + h - 14)
    cr.close_path(); cr.fill()
    cr.set_source_rgba(0.93, 0.93, 0.95, k)                      # collar
    cr.move_to(cx - 18, cy + 52); cr.line_to(cx, cy + 82); cr.line_to(cx + 18, cy + 52); cr.close_path(); cr.fill()
    cr.set_source_rgba(0.87, 0.68, 0.55, k)                      # head
    cr.arc(cx, cy, 52, 0, 2 * math.pi); cr.fill()
    cr.set_source_rgba(0.85, 0.85, 0.88, k)                      # grey side hair
    for sx in (-1, 1):
        cr.arc(cx + sx * 46, cy - 6, 16, 0, 2 * math.pi); cr.fill()
    cr.set_source_rgba(0.1, 0.1, 0.12, k)
    cr.set_line_width(4)
    for sx in (-1, 1):                                          # glasses + eyes
        cr.arc(cx + sx * 20, cy - 4, 13, 0, 2 * math.pi); cr.stroke()
        cr.arc(cx + sx * 20, cy - 4, 4, 0, 2 * math.pi); cr.fill()
    cr.move_to(cx - 30, cy - 26); cr.line_to(cx - 10, cy - 22); cr.stroke()   # stern brows
    cr.move_to(cx + 30, cy - 26); cr.line_to(cx + 10, cy - 22); cr.stroke()
    m = 3 + (8 * abs(math.sin(t * 14)) if talking else 0)
    cr.save(); cr.translate(cx, cy + 26); cr.scale(1, m / 10); cr.arc(0, 0, 10, 0, 2 * math.pi); cr.restore(); cr.fill()
    gk = seg(t, B["k18"].start + 0.4, B["k18"].start + 0.55) * (1 - seg(t, B["k18"].start + 0.6, B["k18"].start + 0.8))
    cr.save()                                                    # the gavel, banged on "Fifty dollars"
    cr.translate(cx + 150, y0 + h - 70)
    cr.rotate(-0.9 + 0.9 * gk)
    cr.set_source_rgba(*WOOD[:3], k)
    cr.rectangle(-4, -70, 8, 70); cr.fill()
    cr.rectangle(-22, -84, 44, 22); cr.fill()
    cr.restore()
    cr.restore()


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.58)
    th.grain(cr, t, 0.04)
    A, B = tl.at, tl.by_id
    judge_call(cr, t, tl)
    toolcard(cr, t, 0.0, B["k1"].end + 0.4, "Parking ticket  #40-2219", [("", "Fine: $40", "", YEL)], y=1085)
    rows = [("1", "Smith v. Parking Meter (2019)", "", CREAM)]
    if t >= B["k8"].start:
        rows.append(("2", "Lee v. Gravity", "", CREAM))
    if t >= B["k10"].start + 0.6:
        rows = [(n, s, "does not exist", RED) for n, s, _, _ in rows]
    toolcard(cr, t, B["k4"].start - 0.1, B["k12"].end + 0.4, "Claude  ·  citations", rows, y=1085)
    cue("ding", t, B["k5"].start - 0.1)
    cue("hush", t, B["k11"].start - 0.1, B["k11"].end - B["k11"].start + 0.2)
    cue("thud", t, B["k18"].start + 0.55)
    th.hook(cr, t, [("I LET MY AI", False), ("BE MY LAWYER", True)], end=A("k1", end=True) + 0.6, y=175, size=88)
    pill_caption(cr, t, tl)
