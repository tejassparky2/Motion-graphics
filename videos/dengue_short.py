"""Florida's record dengue outbreak (Oct 2026). 30-second format: the claim is on screen from frame 1, short hook,
faster voice, one fact per line, the comment question last.

Facts, as of 6 October 2026:
- More than 190 locally acquired dengue cases in Florida in 2026, beating the record of 186 (2023); most in
  Hillsborough County (Tampa). An 80-year-old Hillsborough woman died, the first dengue death in Tampa Bay in nearly
  a century. weather.com, 30 Sep 2026 https://weather.com/2026/09/30/health/dengue-fever-florida-record-mosquito
- 485 dengue cases in Florida this year (all types), CDC data. WSVN, 5 Oct 2026
  https://wsvn.com/news/local/miami-dade/florida-dengue-fever-outbreak/
- Cases rising in at least 15 states; spread by Aedes mosquitoes; symptoms fever, headache, pain, rash; advice:
  EPA-registered repellent, long sleeves, remove standing water. Newsweek, 4 Oct 2026
  https://www.newsweek.com/map-shows-states-where-dengue-fever-cases-have-risen-after-florida-outbreak-12521971
- CDC dengue prevention: https://www.cdc.gov/dengue/prevention/index.html
"""
import math

from motion import fx
from motion.captions import captions
from motion.engine import INK, RED, WHITE, at, blob, dot, ease_out, hexc, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp
from motion.news import source_tag
from motion.newsbrand import badge
from motion.newsprops import bars
from motion.story import buttons
from motion.storykit import (GREEN, NAVY, actor, comment_prompt, focus, hospital, news_pacing, reveal_gaps, sign,
                             sky_ground)

news_pacing()

NARRATOR = dict(speed=1.1)   # owner, 6 Oct 2026: faster voice for the 30-second format
TAIL = 0.3
MUSIC = dict(mood="urgent", drops=["d3"])   # a beat of silence before the death

SCRIPT = [   # approved by the owner, 6 Oct 2026
    dict(id="d1", scene="hook", text="Florida mosquitoes just spread a record number of dengue cases."),
    dict(id="d2", scene="record", text="More than [one hundred ninety|190] people caught it inside the state this year, "
                                     "beating the old record from [twenty twenty-three.|2023.]"),
    dict(id="d3", scene="hospital", text="An eighty-year-old woman near Tampa has died."),
    dict(id="d4", scene="bite", text="Dengue spreads through mosquito bites, and it can cause a high fever, body aches "
                                     "and a rash."),
    dict(id="d5", scene="map", text="Cases are now rising in at least fifteen states."),
    dict(id="d6", scene="advice", text="Health officials say use bug spray, wear long sleeves and empty standing water "
                                       "around your home."),
    dict(id="d7", scene="end", text="Have you seen more mosquitoes this year?"),
]
reveal_gaps(SCRIPT, MUSIC)

METADATA = dict(
    title="Florida's Mosquitoes Just Broke a Record 🦟",
    alt_titles=["Record Dengue Outbreak in Florida, Explained in 30 Seconds",
                "Dengue Is Spreading in Florida. Here's How to Protect Yourself"],
    description="""Florida has recorded more than 190 locally acquired dengue cases in 2026, beating the state's record of 186 from 2023. Most are in Hillsborough County (Tampa). An 80-year-old woman there has died, the first dengue death in Tampa Bay in nearly a century. 🦟

Dengue spreads through the bite of infected Aedes mosquitoes. It can cause a high fever, body aches and a rash; many people have no symptoms. Cases are rising in at least 15 states, according to CDC data.

How to protect yourself: use an EPA-registered insect repellent, wear long sleeves, and empty standing water around your home.

Facts as of 6 October 2026.

💬 Have you seen more mosquitoes this year? 👇

Sources:
• weather.com (30 Sep 2026): https://weather.com/2026/09/30/health/dengue-fever-florida-record-mosquito
• Newsweek (4 Oct 2026): https://www.newsweek.com/map-shows-states-where-dengue-fever-cases-have-risen-after-florida-outbreak-12521971
• WSVN 7News (5 Oct 2026), CDC data: https://wsvn.com/news/local/miami-dade/florida-dengue-fever-outbreak/
• CDC, preventing dengue: https://www.cdc.gov/dengue/prevention/index.html""",
    hashtags=["#Dengue", "#Florida", "#News"],
    tags=["dengue", "dengue fever", "florida dengue", "florida mosquitoes", "dengue outbreak", "tampa", "mosquito",
          "health news", "us news", "news explained"],
    pinned_comment="Have you seen more mosquitoes this year? Yes or no? 👇",
)

FL_RED = hexc("#e0483d")
FLORIDA = [(-270, -130), (60, -130), (70, -110), (110, -60), (140, 0), (165, 70), (170, 140), (150, 190),
           (120, 175), (95, 120), (60, 60), (40, 0), (20, -50), (-10, -80), (-60, -85), (-120, -90), (-200, -95),
           (-270, -100)]


def mosquito(cr, x, y, t, s=1.0, facing=1, seed=30000):
    """A cartoon Aedes mosquito: striped body, see-through wings, long legs, a needle nose."""
    flap = math.sin(t * 40)
    with at(cr, x, y + 6 * math.sin(t * 5), s):
        cr.scale(facing, 1)
        for k, (dx, dy) in enumerate(((-30, 10), (-10, 14), (10, 14), (30, 10), (-20, 8), (20, 8))):
            line(cr, [(dx, dy), (dx * 2.2, 60), (dx * 2.6, 96)], 3, INK, seed + k, amp=0.2)   # legs
        for side in (-1, 1):   # wings
            with at(cr, side * 8, -26, 1.0, rot=side * (0.5 + 0.25 * flap)):
                blob(cr, side * 38, -10, 40, 16, hexc("#dff3ff", 0.75), seed + 10 + side, amp=0.3, lw=3)
        shape(cr, [(-70, -4), (-20, -18), (30, -10), (40, 8), (-20, 16), (-70, 8)], hexc("#2b2d3a"), seed=seed + 20,
              amp=0.3, lw=4)   # abdomen
        for k in range(3):   # white stripes (Aedes)
            line(cr, [(-58 + k * 22, -8), (-56 + k * 22, 10)], 4, WHITE, seed + 21 + k, amp=0.1)
        blob(cr, 52, -2, 22, 20, hexc("#3b3f4a"), seed + 30, amp=0.3, lw=4)   # head
        dot(cr, 60, -8, 7, WHITE)
        dot(cr, 62, -8, 3.5, INK)
        line(cr, [(72, 4), (120, 30)], 4, INK, seed + 31, amp=0.1)   # needle nose


def florida(cr, x, y, s, t, start, seed=30100):
    with at(cr, x, y, s):
        shape(cr, FLORIDA, hexc("#f7f1e3"), seed=seed, amp=0.6, lw=5)
        if t >= start:
            u = ease_out(seg(t, start, start + 0.6))
            cr.save()
            cr.move_to(*FLORIDA[0])
            for q in FLORIDA[1:]:
                cr.line_to(*q)
            cr.close_path()
            cr.clip()
            cr.set_source_rgba(*FL_RED[:3], 0.55 + 0.3 * u)
            cr.paint()
            cr.restore()
            shape(cr, FLORIDA, None, seed=seed, amp=0.6, lw=5)
        write(cr, [("FLORIDA", WHITE if t >= start else NAVY)], -90, -100, 34, align="center", bold=True)
        dot(cr, 70, 30, 10, INK)
        write(cr, [("Tampa", INK)], 70, 70, 26, align="center", bold=True)


START = [0.0]   # current scene's start, for its transition


def path(t):
    """The big mosquito's flight: a lazy figure-eight over Florida."""
    return 360 + 200 * math.sin(t * 1.5), 470 + 80 * math.sin(t * 3.0)


def scene_hook(cr, t, tl):
    A = tl.at
    fx.push(cr, t, 0.0, 0.025)
    fx.bg(cr, "sunburst", t)
    florida(cr, 380, 680, 1.05, t, 0.0)
    for k in range(10):   # dotted flight trail
        px, py = path(t - 0.06 * (k + 1))
        dot(cr, px, py, 5 - k * 0.4, hexc("#2b2d3a", 0.5 - k * 0.04))
    fx.swarm(cr, 380, 700, t, n=5, r=210, draw_one=lambda c, x, y, tt, s, f, sd: mosquito(c, x, y, tt, s, f, sd), s=0.4)
    x, y = path(t)
    mosquito(cr, x, y, t, 1.4, facing=1 if math.cos(t * 1.5) > 0 else -1)
    hl(cr, t, [("DENGUE ", RED), ("RECORD", INK)], 215, 80, -1.0, bold=True, sound=False, underline=True)


def scene_record(cr, t, tl):
    A = tl.at
    fx.transition(cr, t, START[0], "zoom")
    fx.shake(cr, t, A("d2", "beating"), 0.35, 16)
    fx.bg(cr, "comic", t)
    fx.speed_lines(cr, 360, 560, t, alpha=0.45)
    fx.big_number(cr, t, A("d2", "190"), 190, 360, 600, 190, RED, suffix="+", burst_col=fx.CREAM)
    write(cr, [("people caught it", INK)], 360, 690, 44, align="center", bold=True, halo=fx.CREAM)
    write(cr, [("inside Florida", INK)], 360, 740, 44, align="center", bold=True, halo=fx.CREAM)

    def chart(c):
        bars(c, 0, 30, [("2023", 186, hexc("#a9adb5"), "186"), ("2026", 190, FL_RED, "190+")], u=1.0, s=1.4, top=80)
    fx.panel(cr, t, A("d2", "record"), 420, 300, 270, 200, chart, frm="right", tilt=0.04)
    if t >= A("d2", "beating"):
        stamp(cr, t, A("d2", "beating"), "NEW RECORD", dur=10, y=820)
    hl(cr, t, [("190+ ", RED), ("local cases", INK)], 215, 80, A("d2"), bold=True)
    source_tag(cr, t, A("d2"), "weather.com, 30 Sep 2026", y=270)


def ambulance(cr, x, y, t, seed=30700):
    with at(cr, x, y, 1.0):
        shape(cr, rrect_pts(-110, -90, 220, 90, 12, 14), WHITE, seed=seed, amp=0.3, lw=4)
        shape(cr, rrect_pts(-40, -64, 80, 22, 4, 10), FL_RED, seed=seed + 1, amp=0.2, lw=0, stroke=None)
        on = int(t * 6) % 2
        blob(cr, -20, -100, 12, 10, FL_RED if on else hexc("#4fb3e8"), seed + 2, amp=0.2, lw=3)
        blob(cr, 20, -100, 12, 10, hexc("#4fb3e8") if on else FL_RED, seed + 3, amp=0.2, lw=3)
        for wx in (-60, 60):
            blob(cr, wx, 0, 20, 20, INK, seed + 4 + wx, amp=0.2, lw=0, stroke=None)


def scene_hospital(cr, t, tl):
    A = tl.at
    fx.transition(cr, t, START[0], "iris")
    fx.push(cr, t, START[0], 0.03)
    fx.bg(cr, "night", t)
    shape(cr, [(-50, 900), (770, 900), (770, 1400), (-50, 1400)], hexc("#3a3f66"), seed=30710, amp=0.5, lw=4)
    with at(cr, 0, 0, 1.0):
        hospital(cr, 360)
    ambulance(cr, -200 + (t - A("d3") + 0.5) * 260, 900, t)
    if t >= A("d3", "died"):
        sign(cr, 360, 360, "1 death near Tampa", RED, start=A("d3", "died"), t=t, seed=30300)
    hl(cr, t, [("first ", INK), ("DEATH", RED)], 215, 84, A("d3"), bold=True)


def arm(c, t, rash=0.0):
    shape(c, [(-330, 40), (330, -10), (330, 110), (-330, 160)], hexc("#e8b98f"), seed=30800, amp=0.5, lw=5)
    for k in range(int(9 * rash)):
        blob(c, -200 + (k * 53) % 400, 50 + (k * 29) % 60, 9, 7, FL_RED, 30810 + k, amp=0.2, lw=0, stroke=None)


def scene_bite(cr, t, tl):
    A = tl.at
    fx.transition(cr, t, START[0], "slide")
    fx.bg(cr, "sky", t, c1=hexc("#cfe9f7"))

    def macro(c):   # the bite, close up
        fx.speed_lines(c, 0, 0, t, col=hexc("#ffffff"), r0=60, r1=500, alpha=0.5)
        arm(c, t, ease_out(seg(t, A("d4", "rash"), A("d4", "rash") + 0.6)))
        land = ease_out(seg(t, A("d4"), A("d4") + 0.8))
        mosquito(c, 260 - 230 * land, -150 + 140 * land, t, 1.5, facing=-1)
    fx.panel(cr, t, A("d4") - 0.4, 30, 290, 660, 300, macro, frm="left")

    def fever(c):
        fx.bg(c, "sky", t, c1=hexc("#ffe2d6"))
        lvl = ease_out(seg(t, A("d4", "fever"), A("d4", "fever") + 0.8))
        shape(c, rrect_pts(-22, -100, 44, 170, 22, 12), WHITE, seed=30900, amp=0.3, lw=4)
        shape(c, rrect_pts(-10, 50 - 140 * lvl, 20, 20 + 140 * lvl, 10, 10), FL_RED, seed=30901, amp=0.2, lw=0,
              stroke=None)
        blob(c, 0, 80, 30, 30, FL_RED, 30902, amp=0.2, lw=4)
        fx.heat_waves(c, 70, -10, t)
        write(c, [("FEVER", FL_RED)], 0, 112, 30, align="center", bold=True)
    fx.panel(cr, t, A("d4", "fever"), 30, 610, 320, 240, fever, frm="bottom", tilt=-0.03)

    def aches(c):
        fx.bg(c, "sky", t, c1=hexc("#e8e0ff"))
        actor(c, "rider", 0, t, y=150, scale=0.75, arms=("face", "hold"), eyes="sad", mouth="sad")
        for k, (x, y) in enumerate(((-90, -70), (90, -40), (-70, 40))):
            if int(t * 5 + k) % 2:
                line(c, [(x, y - 20), (x + 10, y), (x - 6, y + 4), (x + 6, y + 26)], 6, fx.YELLOW, 30950 + k, amp=0.1)
        write(c, [("ACHES", NAVY)], 0, 112, 30, align="center", bold=True)
    fx.panel(cr, t, A("d4", "aches"), 370, 610, 320, 240, aches, frm="bottom", tilt=0.03)
    hl(cr, t, [("spread by ", INK), ("BITES", RED)], 215, 84, A("d4"), bold=True)


USA = [(-300, -150), (40, -150), (60, -120), (120, -110), (150, -140), (200, -120), (270, -160), (300, -130),
       (240, -60), (250, -20), (210, 30), (200, 80), (220, 150), (190, 160), (170, 90), (100, 90), (40, 110), (0, 150),
       (-30, 120), (-80, 80), (-150, 80), (-220, 60), (-260, 30), (-300, -20), (-310, -90)]
STATE_DOTS = [(190, 120), (-270, -20), (230, -110), (150, -40), (60, -60), (-60, 20), (120, 40), (-180, -60),
              (20, 60), (240, -30), (-120, -110), (90, -120), (-10, -10), (180, 0), (-230, 30)]


def scene_map(cr, t, tl):
    A = tl.at
    fx.transition(cr, t, START[0], "zoom")
    fx.bg(cr, "blueprint", t)
    with at(cr, 360, 640, 1.0):
        shape(cr, USA, hexc("#2c3d78"), seed=30500, amp=0.8, lw=4, stroke=fx.CREAM)
        n = int(len(STATE_DOTS) * ease_out(seg(t, A("d5", "rising"), A("d5", "fifteen") + 0.6)))
        for k, (x, y) in enumerate(STATE_DOTS[:n]):
            age = t - (A("d5", "rising") + k * 0.05)
            ring = (age * 1.2) % 1.0
            cr.set_source_rgba(*FL_RED[:3], 0.6 * (1 - ring))
            cr.set_line_width(3)
            cr.arc(x, y, 12 + 30 * ring, 0, 2 * math.pi)
            cr.stroke()
            dot(cr, x, y, 11, FL_RED)
    fx.big_number(cr, t, A("d5", "fifteen"), 15, 360, 450, 120, fx.YELLOW, suffix="+ states", dur=0.5)
    hl(cr, t, [("rising in ", INK), ("15+ STATES", RED)], 215, 72, A("d5"), bold=True)
    source_tag(cr, t, A("d5"), "CDC data via Newsweek, 4 Oct 2026", y=270)


def spray_can(cr, x, y, s=1.0, seed=30600):
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-34, -80, 68, 150, 10, 12), GREEN, seed=seed, amp=0.3, lw=4)
        shape(cr, rrect_pts(-20, -104, 40, 26, 6, 10), WHITE, seed=seed + 1, amp=0.2, lw=4)
        write(cr, [("BUG", WHITE)], 0, -10, 26, align="center", bold=True)
        write(cr, [("SPRAY", WHITE)], 0, 20, 22, align="center", bold=True)
        for k in range(4):
            dot(cr, 50 + k * 14, -96 - (k % 2) * 10, 4, hexc("#7fc8e8"))


def bucket(cr, x, y, s=1.0, seed=30650):
    with at(cr, x, y, s):
        shape(cr, [(-60, -50), (60, -50), (46, 60), (-46, 60)], hexc("#8f939b"), seed=seed, amp=0.3, lw=4)
        shape(cr, rrect_pts(-56, -56, 112, 18, 8, 10), hexc("#7fc8e8"), seed=seed + 1, amp=0.3, lw=3)


def scene_advice(cr, t, tl):
    A = tl.at
    fx.transition(cr, t, START[0], "slide")
    fx.bg(cr, "comic", t, c1=hexc("#c7f0c0"), c2=hexc("#a6dc9c"))

    def spray(c):
        spray_can(c, -200, 20, 1.0)
        fx.mist(c, -160, -80, t, A("d6", "spray"))
        mosquito(c, 180 + 20 * math.sin(t * 9), -10 + 30 * seg(t, A("d6", "spray") + 0.4, A("d6", "spray") + 1.2), t,
                 0.7, facing=-1)
        write(c, [("use bug spray", INK)], 120, 70, 34, align="center", bold=True)

    def sleeves(c):
        actor(c, "health_official", -200, t, y=150, scale=0.75, arms=("point", "hip"), eyes="open", mouth="talk")
        write(c, [("wear long sleeves", INK)], 90, 10, 34, align="center", bold=True)

    def water(c):
        bucket(c, -200, 20, 1.0)
        u = ease_out(seg(t, A("d6", "water") + 0.2, A("d6", "water") + 0.6))
        line(c, [(-260, -40), (-260 + 120 * u, 80 * u - 40)], 12, RED, 30662, amp=0.2)
        line(c, [(-140, -40), (-140 - 120 * u, 80 * u - 40)], 12, RED, 30663, amp=0.2)
        write(c, [("empty standing water", INK)], 90, 10, 32, align="center", bold=True)
    for k, (key, fn, frm) in enumerate((("spray", spray, "left"), ("sleeves", sleeves, "right"),
                                        ("water", water, "left"))):
        fx.panel(cr, t, A("d6", key), 30, 300 + k * 190, 660, 170, fn, frm=frm, tilt=0.02 * (1 - 2 * (k % 2)),
                 seed=40100 + 10 * k)
    hl(cr, t, [("how to ", INK), ("STAY SAFE", GREEN)], 215, 80, A("d6"), bold=True)
    source_tag(cr, t, A("d6"), "CDC; health officials via Newsweek", y=270)


def scene_end(cr, t, tl):
    A = tl.at
    fx.transition(cr, t, START[0], "whip")
    fx.bg(cr, "sunburst", t)   # bookends the hook, so the loop back to frame 1 feels like one piece
    swat = int(t * 4) % 2
    actor(cr, "shopper", 360, t, y=880, scale=1.3, arms=("cheer", "hip") if swat else ("hip", "cheer"),
          eyes="wide", mouth="o", sweat=True)
    fx.swarm(cr, 360, 600, t, n=4, r=170, draw_one=lambda c, x, y, tt, s, f, sd: mosquito(c, x, y, tt, s, f, sd),
             s=0.5)
    hl(cr, t, [("more ", INK), ("MOSQUITOES", RED), ("?", INK)], 215, 70, A("d7"), bold=True, underline=True)
    cr.identity_matrix()
    buttons(cr, t, A("d7") + 0.3, (("YES", GREEN), ("NO", RED)), y=330, s=0.85)
    comment_prompt(cr, t, A("d7") + 0.6)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    START[0] = start
    cr.save()
    {"hook": scene_hook, "record": scene_record, "hospital": scene_hospital, "bite": scene_bite, "map": scene_map,
     "advice": scene_advice, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    badge(cr, t, "US NEWS", "6 OCT 2026")
    captions(cr, t, tl)
