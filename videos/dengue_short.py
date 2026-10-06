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

from motion.captions import captions
from motion.engine import INK, RED, WHITE, at, blob, dot, ease_out, hexc, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
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
    dict(id="d2", scene="hook", text="More than [one hundred ninety|190] people caught it inside the state this year, "
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


def scene_hook(cr, t, tl):
    A = tl.at
    keys = [(0, (1.0, 640, 760)), (A("d2"), (1.0, 640, 760)), (A("d2", "190"), (1.1, 640, 720))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    sky_ground(cr, ground=hexc("#c7e3a3"))
    florida(cr, 660, 700, 1.1, t, 0.0)
    if t < A("d2", "190"):
        mosquito(cr, 640, 390, t, 1.6)
    else:   # the record, as two bars
        def chart(c):
            u = ease_out(seg(t, A("d2", "190"), A("d2", "190") + 0.6))
            items = [("2023", 186, hexc("#a9adb5"), "186"), ("2026", 190, FL_RED, "190+")]
            bars(c, 0, 40, items, u=u, s=2.0, top=110)
        with at(cr, 640, 520, pop(t, A("d2", "190"), 0.2) or 0.01):
            shape(cr, rrect_pts(-270, -170, 540, 330, 14, 14), WHITE, seed=30200, amp=0.4, lw=5)
            chart(cr)
            write(cr, [("local dengue cases", INK)], 0, 140, 30, align="center", bold=True)
        mosquito(cr, 900, 330, t, 0.8, facing=-1, seed=30210)
    hl(cr, t, [("DENGUE ", RED), ("RECORD", INK)], 215, 80, -1.0, end=A("d2") - 0.05, bold=True, sound=False)
    hl(cr, t, [("190+ ", RED), ("local cases", INK)], 215, 80, A("d2"), bold=True)
    if t >= A("d2"):
        source_tag(cr, t, A("d2"), "weather.com, 30 Sep 2026", y=270)


def scene_hospital(cr, t, tl):
    A = tl.at
    set_camera(camera(t, [(A("d3") - 0.6, (1.0, 600, 800)), (A("d3", "Tampa"), (1.2, 600, 740))], dur=0.14))
    enter_world(cr)
    sky_ground(cr)
    hospital(cr, 600)
    if t >= A("d3", "died"):
        sign(cr, 600, 330, "1 death near Tampa", RED, start=A("d3", "died"), t=t, seed=30300)
    hl(cr, t, [("first ", INK), ("DEATH", RED)], 215, 84, A("d3"), bold=True)


def scene_bite(cr, t, tl):
    A = tl.at
    set_camera(camera(t, [(A("d4") - 0.5, focus(420, 1.4, screen=640)), (A("d4", "fever"), (1.2, 560, 740))],
                        dur=0.14))
    enter_world(cr)
    sky_ground(cr, ground=hexc("#c7e3a3"))
    sick = t >= A("d4", "fever")
    actor(cr, "rider", 420, t, facing=1, arms=("face", "hold") if sick else ("hold", "down"),
          eyes="sad" if sick else "wide", mouth="sad" if sick else "o", sweat=sick)
    mosquito(cr, 560 if t < A("d4", "fever") else 760, 700 if t < A("d4", "fever") else 520, t, 0.9, facing=-1)
    for k, (word, label) in enumerate((("fever", "high fever"), ("aches", "body aches"), ("rash", "rash"))):
        if t >= A("d4", word):
            sign(cr, 760, 600 + k * 110, label, RED, start=A("d4", word), t=t, s=0.8, seed=30400 + k)
    hl(cr, t, [("spread by ", INK), ("BITES", RED)], 215, 84, A("d4"), bold=True)


USA = [(-300, -150), (40, -150), (60, -120), (120, -110), (150, -140), (200, -120), (270, -160), (300, -130),
       (240, -60), (250, -20), (210, 30), (200, 80), (220, 150), (190, 160), (170, 90), (100, 90), (40, 110), (0, 150),
       (-30, 120), (-80, 80), (-150, 80), (-220, 60), (-260, 30), (-300, -20), (-310, -90)]
STATE_DOTS = [(190, 120), (-270, -20), (230, -110), (150, -40), (60, -60), (-60, 20), (120, 40), (-180, -60),
              (20, 60), (240, -30), (-120, -110), (90, -120), (-10, -10), (180, 0), (-230, 30)]


def scene_map(cr, t, tl):
    A = tl.at
    set_camera(camera(t, [(A("d5") - 0.5, (1.0, 640, 760)), (A("d5", "fifteen"), (1.15, 640, 720))], dur=0.14))
    enter_world(cr)
    sky_ground(cr, ground=hexc("#c7e3a3"))
    with at(cr, 640, 600, 1.0):
        shape(cr, USA, hexc("#f7f1e3"), seed=30500, amp=0.8, lw=5)
        n = int(len(STATE_DOTS) * ease_out(seg(t, A("d5", "rising"), A("d5", "fifteen") + 0.6)))
        for k, (x, y) in enumerate(STATE_DOTS[:n]):
            dot(cr, x, y, 13, FL_RED)
            line(cr, [(x, y - 18), (x, y - 40)], 5, FL_RED, 30510 + k, amp=0.1)
            line(cr, [(x - 8, y - 32), (x, y - 42), (x + 8, y - 32)], 5, FL_RED, 30530 + k, amp=0.1)
    hl(cr, t, [("rising in ", INK), ("15+ STATES", RED)], 215, 72, A("d5"), bold=True)
    if t >= A("d5"):
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
    set_camera(camera(t, [(A("d6") - 0.5, (1.0, 640, 760))], dur=0.14))
    enter_world(cr)
    sky_ground(cr, ground=hexc("#c7e3a3"))
    if t >= A("d6", "spray"):
        with at(cr, 430, 700, pop(t, A("d6", "spray"), 0.25) or 0.01):
            spray_can(cr, 0, 0, 1.2)
    if t >= A("d6", "sleeves"):
        actor(cr, "health_official", 640, t, facing=1, arms=("point", "hip"), eyes="open", mouth="talk")
    if t >= A("d6", "water"):
        with at(cr, 860, 760, pop(t, A("d6", "water"), 0.25) or 0.01):
            bucket(cr, 0, 0, 1.2)
            line(cr, [(-70, -70), (70, 70)], 12, RED, 30660, amp=0.2)
            line(cr, [(70, -70), (-70, 70)], 12, RED, 30661, amp=0.2)
    hl(cr, t, [("how to ", INK), ("STAY SAFE", GREEN)], 215, 80, A("d6"), bold=True)
    if t >= A("d6"):
        source_tag(cr, t, A("d6"), "CDC; health officials via Newsweek", y=270)


def scene_end(cr, t, tl):
    A = tl.at
    set_camera(camera(t, [(A("d7") - 0.5, focus(420, 1.4, screen=700))], dur=0.14))
    enter_world(cr)
    sky_ground(cr, ground=hexc("#c7e3a3"))
    actor(cr, "shopper", 420, t, facing=1, arms=("face", "hip"), eyes="wide", mouth="o")
    mosquito(cr, 620, 600, t, 0.8, facing=-1)
    hl(cr, t, [("more ", INK), ("MOSQUITOES", RED), ("?", INK)], 215, 70, A("d7"), bold=True, underline=True)
    cr.identity_matrix()
    buttons(cr, t, A("d7") + 0.3, (("YES", GREEN), ("NO", RED)), y=330, s=0.85)
    comment_prompt(cr, t, A("d7") + 0.6)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"hook": scene_hook, "hospital": scene_hospital, "bite": scene_bite, "map": scene_map, "advice": scene_advice,
     "end": scene_end}[name](cr, t, tl)
    cr.restore()
    badge(cr, t, "US NEWS", "6 OCT 2026")
    captions(cr, t, tl)
