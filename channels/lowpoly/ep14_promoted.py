"""Low-poly channel, episode 14 (credit debate): "My AI Wrote It. I Got Promoted."

Script: channels/lowpoly/scripts/batch4_eps14-15.md (auto-approved by the owner, 20 Oct 2026). Reference-10 form:
short lines, a reaction cut before each line, caption pill. Dev, Claude, Codex; the boss only as chat messages.
Parody, not affiliated with Anthropic or OpenAI.

    python channels/lowpoly/make_skit.py ep14_promoted
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import frames, pill_caption, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cairo, cue, hexc, seg   # noqa: E402
from motion.polish import appear, rrect, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep14"
MUSIC = "pad"
TAIL = 0.6
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep14_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart"),
                       "codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})

DEV, CL, CX = None, "claude", "codex"
_lines = [   # (id, shot, speaker, text, gap before)
    ("p1", "devmid", DEV, "I got promoted.", 0),
    ("p2", "cxots", CX, "Congratulations!", .35),
    ("p3", "devmid", DEV, "For the payments rewrite.", .4),
    ("p4", "codexclose", CX, "I wrote the payments rewrite.", .35),
    ("p5", "devclose", DEV, "I know.", .5),
    ("p6", "clots", CL, "You reviewed it.", .45),
    ("p7", "devmid", DEV, "I clicked approve.", .4),
    ("p8", "claudeclose", CL, "You clicked it with conviction.", .35),
    ("p9", "ots", DEV, "", .5),
    ("p10", "devclose", DEV, "Oh no.", .2),
    ("p11", "cxots", CX, "Put my name on the slide.", .4),
    ("p12", "devmid", DEV, "I can't.", .4),
    ("p13", "codexclose", CX, "Why not?", .3),
    ("p14", "devclose", DEV, "Then they'll ask why they need me.", .6),
    ("p15", "trio", DEV, "", .2),
    ("p16", "clots", CL, "Can I tell you what I saw?", .2),
    ("p17", "devclose", DEV, "Please.", .45),
    ("p18", "claudeclose", CL, "You knew what to build.", .5),
    ("p19", "claudeclose", CL, "You knew when it was wrong. Twice.", .45),
    ("p20", "clots", CL, "That part was you.", .55),
    ("p21", "cxots", CX, "The typing part was me.", .5),
    ("p22", "devmid", DEV, "Fair.", .35),
    ("p23", "ots", DEV, "", .4),
    ("p24", "codexclose", CX, "Bigger font for my name.", .2),
    ("p25", "devclose", DEV, "No.", .3),
    ("p26", "codexclose", CX, "Same font?", .35),
    ("p27", "devmid", DEV, "Same font.", .45),
]
SCRIPT = []
for i, (bid, shot, who, text, gap) in enumerate(_lines):
    d = dict(id=bid, scene=shot, text=text)
    if who:
        d["speaker"] = who
    if i:
        d["gap"] = gap
    if not text:
        d["hold"] = {"p9": 2.4, "p15": 1.5, "p23": 2.6}[bid]
    if bid in ("p14", "p18", "p19", "p20"):
        d["pace"] = 0.92
    SCRIPT.append(d)

METADATA = dict(
    title="My AI Wrote It. I Got Promoted.",
    alt_titles=["Codex Wrote the Code. I Got the Promotion.", "\"Put My Name on the Slide.\""],
    description="""Codex wrote the payments rewrite. Dev clicked approve. Dev got promoted.
Now the boss wants a presentation, and Codex wants its name on the slide.

Who actually did the work?

Ep. 14 of Dev vs the bots. Parody. Not affiliated with Anthropic or OpenAI.

💬 AI wrote the code. Do you deserve the promotion? 👇""",
    hashtags=["#ClaudeCode", "#Codex", "#DevLife"],
    tags=["ai wrote my code", "promotion", "claude", "codex", "ai coding", "programmer humor", "developer life",
          "software engineer", "who gets credit", "funny ai"],
    pinned_comment="AI wrote the code. Do you deserve the promotion? Yes or no? 👇 Subscribe for the next one.",
)
GREEN, GREY, YEL, ORANGE, BLUE = (hexc(c) for c in ("#7ee08a", "#8a93a6", "#ffd23f", "#e8865a", "#6aa8ff"))


def slide(cr, t, start, end, equal):
    """The title slide Dev types for Friday; the names go to the same size on the last line."""
    k = min(appear(t, start, 0.25), 1 - seg(t, end - 0.15, end))
    if k <= 0:
        return
    from motion.engine import W
    x, y, w, h = W / 2 - 300, 760, 600, 300
    cr.save()
    rrect(cr, x, y, w, h, 18)
    cr.set_source_rgba(0.97, 0.96, 0.93, 0.96 * k)
    cr.fill()
    cr.select_font_face("DejaVu Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    typed = "Payments Rewrite"[:max(0, int((t - start) * 14))]
    cr.set_font_size(48)
    ext = cr.text_extents("Payments Rewrite")
    cr.move_to(W / 2 - ext.x_advance / 2, y + 100)
    cr.set_source_rgba(0.1, 0.1, 0.14, k)
    cr.show_text(typed)
    if t > start + 1.3:
        k2 = k * appear(t, start + 1.3, 0.3)
        names = [("Dev", (0.1, 0.1, 0.14)), ("Claude", ORANGE[:3]), ("Codex", BLUE[:3])]
        sizes = [34, 34, 34] if equal else [34, 22, 22]
        parts = [("Dev", sizes[0], names[0][1]), ("  ·  with ", 22, (0.45, 0.45, 0.5)),
                 ("Claude", sizes[1], names[1][1]), (" & ", 22, (0.45, 0.45, 0.5)), ("Codex", sizes[2], names[2][1])]
        total = 0
        for s, sz, _ in parts:
            cr.set_font_size(sz)
            total += cr.text_extents(s).x_advance
        cx = W / 2 - total / 2
        for s, sz, col in parts:
            cr.set_font_size(sz)
            cr.move_to(cx, y + 190)
            cr.set_source_rgba(*col, k2)
            cr.show_text(s)
            cx += cr.text_extents(s).x_advance
        cr.set_font_size(18)
        cr.move_to(x + 30, y + h - 30)
        cr.set_source_rgba(0.5, 0.5, 0.55, k2)
        cr.show_text("All-hands · Friday")
    cr.restore()


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.62)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, A("p1", "promoted") - 0.1, B["p2"].end + 0.3, "Boss · 5:02 PM",
             [("", "Senior Engineer,", "", GREEN), ("", "effective Monday 🎉", "", GREEN)], y=900)
    p9 = B["p9"]
    toolcard(cr, t, p9.start + 0.3, A("p10", end=True) + 0.4, "Boss · 5:04 PM",
             [("", "Present it to the", "", GREY), ("", "whole company Friday?", "", YEL)], y=900)
    p23 = B["p23"]
    slide(cr, t, p23.start + 0.2, tl.total + 1, t >= A("p27", "Same"))
    cue("ding", t, A("p1", "promoted") - 0.1)
    cue("ding", t, p9.start + 0.3)
    cue("hush", t, B["p15"].start - 0.1, B["p15"].end - B["p15"].start + 0.2)
    cue("typing", t, p23.start + 0.2, 1.3)
    cue("pop", t, A("p27", "Same"))
    th.hook(cr, t, [("MY AI WROTE IT.", False), ("I GOT PROMOTED.", True)], end=A("p1", end=True) + 0.5, y=175, size=84)
    pill_caption(cr, t, tl)
