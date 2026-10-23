"""Low-poly channel, episode 28: "I Asked Claude to Make GTA 5".

Script: channels/lowpoly/scripts/batch8_big_asks_eps28-31.md (owner approved, 23 Oct 2026). Made in reference 10's
form: Claude answers flat, Dev's lines are the comedy, full-screen screen cutaways with a clock that jumps, plain
white captions, no title card, music only at the end. Real: GTA V was made by about 1,000 people (Leslie Benzies,
Develop, 2013). Fiction; parody, not affiliated with Anthropic or Rockstar.

    python channels/lowpoly/make_skit.py ep28_gta
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, mono, plain_caption, screen_insert, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep28"
MUSIC = "score"
SCORE = [(0, "out"), ("g20", "tender"), ("g21", "end", 0.9)]
TAIL = 0.7
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep28_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart")})
skit_voice(voice, rate=3.4, tempo_min=0.8)

DEV, CL = None, "claude"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("g1", "devmid", DEV, "My laptop can't run [G T A five|GTA 5].", 0, 1),
    ("g2", "devclose", DEV, "Claude. Make me my own.", .6, 1),
    ("g3", "soloclose", CL, "Sure.", .5, 1),
    ("g4", "devmid", DEV, "A whole city. Cars. Police. Helicopters.", .7, 1),
    ("g5", "solo", CL, "Done.", .5, 1),
    ("g6", "ots", DEV, "That's a box.", 1.0, 1),
    ("g7", "soloclose", CL, "That's the city.", .5, 1),
    ("g8", "devclose", DEV, "Where are the cars?", .6, 1),
    ("g9", "soloclose", CL, "In the box.", .5, 1),
    ("g10", "devmid", DEV, "Add police.", .8, 1),
    ("g11", "solo", CL, "Done.", .5, 1),
    ("g12", "ots", DEV, "Why is the police a box?", 1.0, 1),
    ("g13", "soloclose", CL, "Your laptop.", .5, 1),
    ("g13h", "ots", DEV, "", .6, 1),
    ("g14", "devclose", DEV, "How many people made the real one?", .3, 1),
    ("g15", "soloclose", CL, "About a thousand.", .5, 1),
    ("g16", "devclose", DEV, "And we have?", .6, 1),
    ("g17", "solo", CL, "You. Me. And the box.", .5, 1),
    ("g17h", "ots", DEV, "", .6, 1),
    ("g18", "devclose", DEV, "This is the worst game ever made. [laugh]", .3, 1),
    ("g19", "solo", CL, "You've played it for four hours.", .6, 1),
    ("g20", "devclose", DEV, "One more round.", 1.5, .95),
    ("g21", "endside", CL, "Sure.", .6, 1),
]
HOLDS = {"g13h": 1.5, "g17h": 2.0}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="I Asked Claude to Make GTA 5",
    alt_titles=["My Laptop Can't Run GTA 5, So I Made My Own", "\"That's the City.\""],
    description="""His laptop can't run GTA 5. So he asks Claude to make him his own.
A whole city. Cars. Police. Helicopters. Claude delivers... a box.

Real: Rockstar has said GTA V took about 1,000 people to make (Leslie Benzies, Develop, 2013). This story is fiction.

Ep. 28 of Dev vs the bots. Parody. Not affiliated with Anthropic or Rockstar Games.

💬 Would you play the box game? Be honest 👇""",
    hashtags=["#GTA5", "#ClaudeAI", "#ProgrammerHumor"],
    tags=["gta 5", "ai made a game", "claude", "vibe coding", "programmer humor", "coding memes", "game dev",
          "ai game", "developer life", "funny ai"],
    pinned_comment="Would you play the box game? Be honest 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, BLUE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#4d8dff"))


def _cube(cr, x, y, s, top, left, right):
    """An isometric box centred at (x, y), edge s."""
    c, h = s * 0.87, s * 0.5
    faces = [((x, y - s), (x + c, y - s + h), (x, y - s + 2 * h), (x - c, y - s + h), top),
             ((x - c, y - s + h), (x, y - s + 2 * h), (x, y + 2 * h - s + s), (x - c, y + h), left),
             ((x + c, y - s + h), (x, y - s + 2 * h), (x, y + s), (x + c, y + h), right)]
    for *pts, col in faces:
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
        cr.close_path()
        cr.set_source_rgb(*col)
        cr.fill_preserve()
        cr.set_source_rgba(0, 0, 0, 0.25)
        cr.set_line_width(2)
        cr.stroke()


def _game(police=False, hud=None, fast=1.0):
    """gta_but_mine.exe: green grass under a flat sky, one grey box (the city, the car, everything), maybe a blue
    police box chasing it."""
    def paint(cr, x, y, w, h, t, k):
        cr.rectangle(x, y, w, h * 0.42)
        cr.set_source_rgb(0.55, 0.78, 0.98)
        cr.fill()
        cr.rectangle(x, y + h * 0.42, w, h * 0.58)
        cr.set_source_rgb(0.36, 0.7, 0.33)
        cr.fill()
        cx, cy = x + w / 2, y + h * 0.66
        a = t * 1.3 * fast
        bx, by = cx + math.cos(a) * 150 * (fast > 1), cy + math.sin(a) * 60 * (fast > 1)
        if police:
            pa = a - 0.9
            px, py = cx + math.cos(pa) * 170, cy + math.sin(pa) * 70
            if fast == 1.0:
                px, py = cx - 190 + 40 * math.sin(t * 2), cy + 10
            _cube(cr, px, py, 46, (0.45, 0.6, 1.0), (0.2, 0.32, 0.75), (0.3, 0.45, 0.9))
            on = int(t * 6) % 2
            cr.rectangle(px - 14, py - 62, 12, 9)
            cr.set_source_rgb(*(RED[:3] if on else (0.4, 0.1, 0.1)))
            cr.fill()
            cr.rectangle(px + 2, py - 62, 12, 9)
            cr.set_source_rgb(*((0.1, 0.1, 0.4) if on else BLUE[:3]))
            cr.fill()
        _cube(cr, bx, by, 58, (0.78, 0.78, 0.8), (0.5, 0.5, 0.54), (0.64, 0.64, 0.68))
        if police:
            mono(cr, "WANTED ★", x + 24, y + 44, 30, YEL, k)
        if hud:
            mono(cr, hud, x + 24, y + 86, 26, (1, 1, 1), k)
        mono(cr, "gta_but_mine.exe", x + w - 250, y + h - 20, 18, (0.15, 0.2, 0.15), k)
    return paint


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, 0.0, B["g2"].start - 0.1, "GTA5.exe",
             [("", "Not enough memory.", "", RED), ("", "Your laptop: 4 GB", "", GREY)], y=1085)
    screen_insert(cr, t, B["g5"].end + 0.35, B["g6"].end + 0.5, "gta_but_mine.exe", "11:48 PM", _game())
    screen_insert(cr, t, B["g11"].end + 0.35, B["g12"].end + 0.5, "gta_but_mine.exe", "11:52 PM", _game(police=True))
    screen_insert(cr, t, B["g13h"].start, B["g13h"].end, "gta_but_mine.exe", "1:12 AM", _game(police=True))
    screen_insert(cr, t, B["g17h"].start, B["g17h"].end, "gta_but_mine.exe", "4:40 AM",
                  _game(police=True, hud="Escapes: 212", fast=2.6))
    cue("buzz", t, 0.2, 0.8)
    cue("pop", t, B["g5"].end + 0.35)
    cue("police", t, B["g11"].end + 0.35, 2.0)
    cue("typing", t, B["g17h"].start, 1.8)
    cue("police", t, B["g17h"].start + 0.2, 1.6)
    plain_caption(cr, t, tl)
