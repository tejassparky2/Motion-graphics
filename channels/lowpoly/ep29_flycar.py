"""Low-poly channel, episode 29: "I Asked Codex to Make My Car Fly".

Script: channels/lowpoly/scripts/batch8_big_asks_eps28-31.md (owner approved, 23 Oct 2026). Reference 10's form.
Real: on 15 Oct 2026 Tesla showed a Roadster prototype at a SpaceX site in Texas that climbed a ramp, hopped over
parked cars on air jets and landed; Musk says it "will be able to fly", production 2028; a Smithsonian curator: "We are
literally talking about hopping." (CNN via ABC30, 16 Oct 2026.) Fiction; parody, not affiliated with OpenAI or Tesla.

    python channels/lowpoly/make_skit.py ep29_flycar
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_script, frames, mono, plain_caption, screen_insert, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import rrect, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep29"
MUSIC = "score"
SCORE = [(0, "out"), ("f16", "tender"), ("f20h", "light"), ("f24", "end", 0.9)]
TAIL = 0.7
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep29_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2")})
skit_voice(voice, rate=3.4, tempo_min=0.8)

DEV, CX = None, "codex"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("f1", "devmid", DEV, "Tesla's new car jumped over other cars.", 0, 1),
    ("f2", "devclose", DEV, "Codex. Make my car fly.", .6, 1),
    ("f3", "cxclose", CX, "You drive a 2011 Honda.", .5, 1),
    ("f4", "devclose", DEV, "Make my Honda fly.", .7, 1),
    ("f5", "cx", CX, "Step one. Wings.", .5, 1),
    ("f6", "devmid", DEV, "Okay.", .5, 1),
    ("f7", "cxclose", CX, "Step two. A pilot's license.", .4, 1),
    ("f8", "devclose", DEV, "Okay.", .5, 1),
    ("f9", "cxclose", CX, "Step three. Tell your mom.", .4, 1),
    ("f10", "devclose", DEV, "Skip step three.", .6, 1),
    ("f11", "cxclose", CX, "Step three is the most important step.", .4, 1),
    ("f11h", "ots", DEV, "", .6, 1),
    ("f12", "devclose", DEV, "Can it at least jump?", .3, 1),
    ("f13", "cxclose", CX, "Over a speed bump. Once.", .5, 1),
    ("f14", "cx", CX, "Why do you want it to fly?", 1.1, .95),
    ("f15", "devclose", DEV, "Two hours of traffic. Every day.", 1.0, .95),
    ("f16", "cxclose", CX, "Leave at seven. Not eight.", 1.1, .95),
    ("f17", "devclose", DEV, "That's it?", .6, 1),
    ("f18", "cx", CX, "You told me your commute every morning. For three weeks. Seven is empty.", .5, 1),
    ("f19", "devclose", DEV, "You kept track?", .7, 1),
    ("f20", "cxclose", CX, "You complain a lot.", .5, 1),
    ("f20h", "ots", DEV, "", .7, 1),
    ("f21", "devmid", DEV, "Twenty-four minutes. [chuckle]", .3, 1),
    ("f22", "cxclose", CX, "Told you.", .5, 1),
    ("f23", "devclose", DEV, "Still want wings.", .7, 1),
    ("f24", "endside", CX, "Ordering stickers.", .5, 1),
]
HOLDS = {"f11h": 1.6, "f20h": 1.8}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap_fix=GAP_FIX)

METADATA = dict(
    title="I Asked Codex to Make My Car Fly",
    alt_titles=["Tesla's Car Can Jump. Mine Can't.", "\"Step Three. Tell Your Mom.\""],
    description="""Tesla's new car jumped over other cars. So he asks Codex to make his car fly.
His car is a 2011 Honda.

Real: on 15 Oct 2026 Tesla showed a Roadster prototype that climbed a ramp, hopped over parked cars on air jets and
landed; Musk says it "will be able to fly" and production is planned for 2028. A Smithsonian curator called it
"hopping". This story is fiction.

Ep. 29 of Dev vs the bots. Parody. Not affiliated with OpenAI or Tesla.

💬 Flying car, or just leave at seven? 👇""",
    hashtags=["#Tesla", "#Codex", "#ProgrammerHumor"],
    tags=["tesla flying car", "tesla roadster", "flying car", "codex", "programmer humor", "coding memes", "traffic",
          "commute", "developer life", "funny ai"],
    pinned_comment="Flying car, or just leave at seven? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, BLUE, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#4d8dff", "#ff9a3d"))
WHITE = (1, 1, 1)


def _plan(n):
    """flight_plan.md with the first n steps; step three in red."""
    rows = [("1.", "Wings", WHITE), ("2.", "A pilot's license", WHITE), ("3.", "Tell your mom", RED)]

    def paint(cr, x, y, w, h, t, k):
        mono(cr, "# Make the Honda fly", x + 30, y + 70, 30, ORANGE, k)
        mono(cr, "Car: Honda Civic (2011)", x + 30, y + 120, 24, GREY, k)
        for i, (num, text, col) in enumerate(rows[:n]):
            mono(cr, num, x + 30, y + 200 + 70 * i, 34, GREY, k)
            mono(cr, text, x + 90, y + 200 + 70 * i, 34, col, k)
        if n >= 3:
            mono(cr, "^ most important", x + 90, y + 200 + 70 * 2 + 44, 22, RED, k * (0.6 + 0.4 * (int(t * 3) % 2)))
    return paint


def _sim(cr, x, y, w, h, t, k):
    mono(cr, "$ codex simulate --car honda_2011", x + 30, y + 60, 22, GREY, k)
    mono(cr, "Max height:   4 cm", x + 30, y + 140, 32, WHITE, k)
    mono(cr, "Clears:       1 speed bump", x + 30, y + 200, 32, WHITE, k)
    mono(cr, "Flights:      0", x + 30, y + 260, 32, RED, k)
    mono(cr, "Wings:        not found", x + 30, y + 320, 32, YEL, k)


def _chart(cr, x, y, w, h, t, k):
    """Three weeks of what Dev said every morning: leaving at 7 vs 8."""
    mono(cr, "commute.log  (21 mornings)", x + 30, y + 56, 24, GREY, k)
    rows = [("Leave 7:00", 24, GREEN), ("Leave 7:30", 55, YEL), ("Leave 8:00", 120, RED)]
    for i, (lab, mins, col) in enumerate(rows):
        yy = y + 130 + 120 * i
        mono(cr, lab, x + 30, yy, 28, WHITE, k)
        bw = (w - 80) * mins / 125
        rrect(cr, x + 30, yy + 18, max(8, bw), 34, 8)
        cr.set_source_rgba(*col[:3], 0.9 * k)
        cr.fill()
        txt = f"{mins} min" if mins < 60 else "2 hours"
        inside = bw > w - 240                     # the long bar carries its label inside; the others after the bar
        mono(cr, txt, x + 30 + bw - 120 if inside else x + 44 + bw, yy + 44, 24, (0.05, 0.05, 0.07) if inside else WHITE, k)


def _map(cr, x, y, w, h, t, k):
    cr.rectangle(x, y, w, h)
    cr.set_source_rgb(0.9, 0.92, 0.88)
    cr.fill()
    for i in range(7):
        cr.rectangle(x + 40 + i * 95, y, 18, h)
        cr.rectangle(x, y + 40 + i * 85, w, 18)
    cr.set_source_rgb(1, 1, 1)
    cr.fill()
    cr.set_line_width(12)
    cr.set_source_rgb(0.25, 0.55, 1)
    cr.move_to(x + 80, y + h - 60)
    cr.line_to(x + 80, y + 300)
    cr.line_to(x + 470, y + 300)
    cr.line_to(x + 470, y + 90)
    cr.stroke()
    rrect(cr, x + 30, y + h - 150, w - 60, 110, 18)
    cr.set_source_rgba(0.08, 0.09, 0.12, 0.95)
    cr.fill()
    mono(cr, "24 min", x + 60, y + h - 92, 44, GREEN, k)
    mono(cr, "Light traffic · Leave now", x + 60, y + h - 56, 22, WHITE, k)


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    toolcard(cr, t, 0.1, B["f2"].start - 0.1, "News  ·  Oct 15",
             [("", "Tesla Roadster prototype", "", WHITE), ("", "hops over parked cars", "", YEL)], y=1085)
    toolcard(cr, t, B["f3"].start + 0.2, B["f4"].end + 0.3, "Your car",
             [("", "Honda Civic (2011)", "", WHITE), ("", "Wings: 0", "", GREY)], y=1085)
    screen_insert(cr, t, B["f5"].end + 0.3, B["f6"].end + 0.4, "flight_plan.md", "1:05 AM", _plan(1))
    screen_insert(cr, t, B["f7"].end + 0.3, B["f8"].end + 0.4, "flight_plan.md", "1:06 AM", _plan(2))
    screen_insert(cr, t, B["f9"].end + 0.3, B["f10"].end + 0.4, "flight_plan.md", "1:06 AM", _plan(3))
    screen_insert(cr, t, B["f11h"].start, B["f11h"].end, "terminal", "2:30 AM", _sim)
    screen_insert(cr, t, B["f18"].start + 1.2, B["f19"].end + 0.4, "commute.log", "2:41 AM", _chart)
    screen_insert(cr, t, B["f20h"].start, B["f20h"].end, "Maps", "7:00 AM", _map)
    cue("buzz", t, 0.25, 0.6)
    cue("pop", t, B["f5"].end + 0.3)
    cue("pop", t, B["f7"].end + 0.3)
    cue("pop", t, B["f9"].end + 0.3)
    cue("typing", t, B["f11h"].start, 1.4)
    cue("sigh", t, B["f15"].start - 0.6)
    cue("ding", t, B["f20h"].start + 0.2)
    plain_caption(cr, t, tl)
