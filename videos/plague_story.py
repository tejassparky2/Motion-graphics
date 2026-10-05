"""A suspected plague death at a Russian lab (Oct 2026), story style with our own cast, ending on the US angle.
"Suspected" throughout; the worker is not named and not shown as a portrait (privacy).

Facts, as of 5 October 2026:
- A 28-year-old lab technician at the Irkutsk Anti-Plague Institute, Siberia, hospitalised 29 Sep 2026, died days
  later; suspected pneumonic plague. Al Jazeera
  https://www.aljazeera.com/news/2026/10/5/russian-lab-worker-dies-of-suspected-plague-in-siberia-us-monitoring-case ;
  Meduza https://meduza.io/en/feature/2026/10/05/hospitals-in-irkutsk-impose-quarantines-after-an-employee-at-an-anti-plague-institute-dies-russia-s-public-health-agency-says-she-died-of-pneumonia-and-the-epidemiological-situation-remains-stable ;
  CNN https://www.cnn.com/2026/10/04/europe/russia-laboratory-plague-accident-intl ;
  Business Standard https://www.business-standard.com/amp/health/russia-plague-scare-nearly-200-face-quarantine-after-lab-worker-dies-126100500079_1.html
- 197 possible contacts isolated; several hospitals under three-week quarantine; Rospotrebnadzor: "stable",
  "pneumonia of unknown cause" (Meduza; Al Jazeera).
- US State Department: "monitoring the situation closely" (Al Jazeera).
- Plague = Yersinia pestis, the Black Death; treatable with antibiotics if caught early. WHO
  https://www.who.int/news-room/fact-sheets/detail/plague ; CDC https://www.cdc.gov/plague/diagnosis-testing/index.html
- "An average of seven human plague cases are reported each year in the United States", mostly in the West (northern
  New Mexico, Arizona, southern Colorado; California, southern Oregon, western Nevada). CDC
  https://www.cdc.gov/plague/maps-statistics/index.html ; National Park Service https://www.nps.gov/articles/000/plague.htm
"""
import math

from motion.captions import captions
from motion.engine import INK, RED, WHITE, at, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from motion.news import crowd, source_tag, tick
from motion.newsbrand import badge
from motion.newsprops import binoculars, old_scroll, pill_bottle
from motion.story import buttons
from motion.storykit import (GOLD, GREEN, NAVY, actor, building, focus, hospital, podium, quarantine_tape, sign,
                             sky_ground, snowfall)

NARRATOR = dict(speed=0.95)
TAIL = 0.9

SCRIPT = [
    dict(id="p1", scene="lab", text="A lab worker in Siberia has died. And doctors suspect the plague."),
    dict(id="p2", scene="lab", text="Yes. The same germ behind the Black Death."),
    dict(id="p3", scene="lab", text="It happened in Irkutsk, Russia. At an institute that studies plague."),
    dict(id="p4", scene="hospital", text="A twenty-eight-year-old lab technician went to hospital on September "
                                         "twenty-ninth. She died days later."),
    dict(id="p5", scene="hospital", text="Officials say the situation is stable."),
    dict(id="p6", scene="hospital", text="But [one hundred ninety-seven|197] people who may have had contact were "
                                         "isolated. And several hospitals went into a three-week quarantine."),
    dict(id="p7", scene="podium", text="Is it confirmed? Not yet. Russia's health agency calls it pneumonia of "
                                       "unknown cause."),
    dict(id="p8", scene="podium", text="The US State Department says it is monitoring closely."),
    dict(id="p9", scene="usa", text="And here's what most Americans don't know. Plague still shows up in the US. "
                                    "About seven cases a year, mostly in the West."),
    dict(id="p10", scene="usa", text="The good news? It can be treated with antibiotics if it's caught early."),
    dict(id="p11", scene="end", text="Did you know plague still exists in America? Tell me in the comments."),
]

METADATA = dict(
    title="A Lab Worker Died. Doctors Suspect the Plague 😷",
    alt_titles=["Suspected Plague Death in Russia, and the US Cases Nobody Talks About",
                "Plague Still Exists in America. Here's What Just Happened"],
    description="""A 28-year-old lab technician at the Irkutsk Anti-Plague Institute in Siberia, Russia, died days after being hospitalised on 29 September 2026. Doctors suspect pneumonic plague, caused by the same germ behind the Black Death. 😷

197 people who may have had contact were isolated and several hospitals went into a three-week quarantine. Russia's health agency says the situation is stable and calls it "pneumonia of unknown cause": plague is NOT confirmed. The US State Department says it is monitoring closely.

In the US: the CDC says about seven human plague cases are reported each year, mostly in the West. Plague can be treated with antibiotics if it's caught early.

Facts as of 5 October 2026.

💬 Did you know plague still exists in America? 👇

Sources:
• Al Jazeera (5 Oct 2026): https://www.aljazeera.com/news/2026/10/5/russian-lab-worker-dies-of-suspected-plague-in-siberia-us-monitoring-case
• Meduza (5 Oct 2026): https://meduza.io/en/feature/2026/10/05/hospitals-in-irkutsk-impose-quarantines-after-an-employee-at-an-anti-plague-institute-dies-russia-s-public-health-agency-says-she-died-of-pneumonia-and-the-epidemiological-situation-remains-stable
• CNN (4 Oct 2026): https://www.cnn.com/2026/10/04/europe/russia-laboratory-plague-accident-intl
• CDC, plague in the United States: https://www.cdc.gov/plague/maps-statistics/index.html
• WHO plague fact sheet: https://www.who.int/news-room/fact-sheets/detail/plague""",
    hashtags=["#Plague", "#Health", "#News"],
    tags=["plague", "russia", "irkutsk", "black death", "suspected plague", "plague in america", "cdc",
          "health news", "world news", "news explained"],
    pinned_comment="Did you know there are plague cases in the US every year? Yes or no? 👇",
)

ICE = hexc("#dfe9f2")


def lab_set(cr, t):
    sky_ground(cr, snow=True)
    building(cr, 640, 560, 470, hexc("#c9ccd2"), "ANTI-PLAGUE INSTITUTE", seed=21000)
    snowfall(cr, t)


def scene_lab(cr, t, tl):
    A = tl.at
    keys = [(0, (0.9, 640, 820)), (A("p1", "plague"), (1.4, 640, 700)), (A("p2"), (1.3, 640, 640)),
            (A("p3"), (0.85, 640, 820)), (A("p3", "institute"), (1.2, 640, 680))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    lab_set(cr, t)
    if t >= A("p1", "plague"):   # a hazard sign on the door
        with at(cr, 640, 700, pop(t, A("p1", "plague"), 0.2) or 0.01):
            from motion.newsprops import biohazard_door
            biohazard_door(cr, 0, 40, 0.9)
    if A("p2", "Black") <= t < A("p3"):
        with at(cr, 640, 520, pop(t, A("p2", "Black"), 0.2) or 0.01):
            old_scroll(cr, 0, 0, "the Black Death", "Europe, 1300s", 1.1)
    if t >= A("p3", "Irkutsk"):
        sign(cr, 300, 470, "Irkutsk, Russia", NAVY, start=A("p3", "Irkutsk"), t=t, seed=21010)
    hl(cr, t, [("SUSPECTED ", RED), ("plague", INK)], 215, 74, A("p1", "plague"), end=A("p2") - 0.05, bold=True)
    hl(cr, t, [("the ", INK), ("BLACK DEATH", RED), (" germ", INK)], 215, 62, A("p2"), end=A("p3") - 0.05, bold=True)
    if A("p2", "Black") <= t < A("p3"):
        source_tag(cr, t, A("p2", "Black"), "World Health Organization", y=270)
    hl(cr, t, [("Siberia, ", INK), ("RUSSIA", NAVY)], 215, 80, A("p3"), bold=True)


def scene_hospital(cr, t, tl):
    A = tl.at
    keys = [(A("p4") - 0.2, (0.9, 600, 830)), (A("p4", "September"), (1.3, 600, 700)), (A("p5"), focus(1060, 1.7)),
            (A("p6"), (1.0, 640, 830)), (A("p6", "isolated"), (1.2, 640, 760)), (A("p6", "quarantine"), (1.0, 620, 760))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    sky_ground(cr, snow=True)
    hospital(cr, 600)
    snowfall(cr, t)
    if A("p4", "September") <= t < A("p5"):
        sign(cr, 600, 360, "29 SEP 2026", RED, start=A("p4", "September"), t=t, seed=21100)
    actor(cr, "doctor", 1060, t, facing=-1, arms=("hold", "hip"), eyes="sad" if t < A("p5") else "open",
          mouth="flat")
    if t >= A("p6"):
        u = ease_out(seg(t, A("p6", "197"), A("p6", "197") + 1.2))
        with at(cr, 640, 560, 1.0):
            shape(cr, rrect_pts(-260, -110, 520, 220, 14, 14), WHITE, seed=21110, amp=0.4, lw=5)
            crowd(cr, 0, -30, t, 60, cols=15, gap=26, progress=u)
            write(cr, [(f"{int(197 * u)} isolated", RED)], 0, 86, 44, align="center", bold=True)
    if t >= A("p6", "quarantine"):
        quarantine_tape(cr, 260, 960, 820)
    hl(cr, t, [("age ", INK), ("28", RED), (", lab technician", INK)], 215, 60, A("p4"), end=A("p5") - 0.05,
       bold=True)
    hl(cr, t, [("officials: ", INK), ("\"stable\"", NAVY)], 215, 74, A("p5"), end=A("p6") - 0.05, bold=True)
    hl(cr, t, [("197", RED), (" isolated", INK)], 215, 84, A("p6"), end=A("p6", "quarantine") - 0.05, bold=True)
    hl(cr, t, [("3-week ", INK), ("QUARANTINE", RED)], 215, 66, A("p6", "quarantine"), bold=True)
    if t >= A("p5"):
        source_tag(cr, t, A("p5"), "Meduza; Al Jazeera, 5 Oct 2026", y=270)


def scene_podium(cr, t, tl):
    A = tl.at
    keys = [(A("p7") - 0.2, focus(420, 1.6)), (A("p7", "agency"), (1.3, 480, 720)), (A("p8"), (1.0, 900, 820)),
            (A("p8", "monitoring"), (1.4, 980, 700))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    sky_ground(cr, ground=hexc("#c9c4b8"))
    actor(cr, "health_official", 420, t, facing=1, arms=("point", "hip"), eyes="open", mouth="talk")
    podium(cr, 420, "HEALTH AGENCY", hexc("#1f4fb0"))
    if A("p7", "Not") <= t < A("p7", "agency"):
        stamp(cr, t, A("p7", "Not"), "NOT CONFIRMED", dur=A("p7", "agency") - A("p7", "Not"), y=460)
    if A("p7", "agency") <= t < A("p8"):
        with at(cr, 480, 500, pop(t, A("p7", "agency"), 0.2) or 0.01):
            shape(cr, rrect_pts(-250, -70, 500, 140, 12, 14), WHITE, seed=21200, amp=0.4, lw=5)
            write(cr, [("\"pneumonia of", INK)], 0, -10, 40, align="center", bold=True)
            write(cr, [("unknown cause\"", INK)], 0, 36, 40, align="center", bold=True)
    if t >= A("p8"):
        building(cr, 980, 420, 420, hexc("#f1ede4"), "US STATE DEPT", seed=21210)
        with at(cr, 980, 560, 1.2):
            binoculars(cr, 0, 0, 1.0)
    hl(cr, t, [("confirmed? ", INK), ("NOT YET", RED)], 215, 74, A("p7"), end=A("p8") - 0.05, bold=True)
    hl(cr, t, [("US ", NAVY), ("monitoring", INK)], 215, 84, A("p8"), bold=True)


def scene_usa(cr, t, tl):
    A = tl.at
    keys = [(A("p9") - 0.2, (1.0, 640, 820)), (A("p9", "US."), (1.0, 640, 760)), (A("p9", "seven"), (1.3, 640, 680)),
            (A("p9", "West"), (1.1, 640, 740)), (A("p10"), focus(420, 1.6)), (A("p10", "antibiotics"), (1.4, 560, 720))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    sky_ground(cr, ground=hexc("#e2c48f"))
    if t < A("p10"):
        # a simple US map shape with the western region highlighted
        with at(cr, 640, 600, 1.0):
            usa = [(-300, -150), (40, -150), (60, -120), (120, -110), (150, -140), (200, -120), (270, -160),
                   (300, -130), (240, -60), (250, -20), (210, 30), (200, 80), (220, 150), (190, 160), (170, 90),
                   (100, 90), (40, 110), (0, 150), (-30, 120), (-80, 80), (-150, 80), (-220, 60), (-260, 30),
                   (-300, -20), (-310, -90)]
            shape(cr, usa, hexc("#f7f1e3"), seed=21300, amp=0.8, lw=5)
            if t >= A("p9", "West"):
                cr.save()
                cr.move_to(*usa[0])
                for q in usa[1:]:
                    cr.line_to(*q)
                cr.close_path()
                cr.clip()
                cr.rectangle(-320, -170, 200, 340)
                cr.set_source_rgba(*hexc("#f2b632", 0.75))
                cr.fill()
                cr.restore()
                shape(cr, usa, None, seed=21300, amp=0.8, lw=5)
                write(cr, [("WEST", RED)], -215, 0, 40, align="center", bold=True)
            write(cr, [("USA", NAVY)], 60, 0, 60, align="center", bold=True)
        if t >= A("p9", "seven"):
            sign(cr, 640, 400, "about 7 cases a year", RED, start=A("p9", "seven"), t=t, seed=21310)
    else:
        actor(cr, "doctor", 420, t, facing=1, arms=("hold", "thumb"), eyes="happy", mouth="smile")
        if t >= A("p10", "antibiotics"):
            with at(cr, 640, 640, pop(t, A("p10", "antibiotics"), 0.2) or 0.01):
                pill_bottle(cr, 0, 0, 1.4)
            tick(cr, 760, 560, 26, col=GREEN)
    hl(cr, t, [("plague in the ", INK), ("USA", NAVY), ("?", INK)], 215, 70, A("p9"), end=A("p9", "seven") - 0.05,
       bold=True)
    hl(cr, t, [("~7 cases ", RED), ("a year", INK)], 215, 80, A("p9", "seven"), end=A("p10") - 0.05, bold=True)
    if A("p9", "seven") <= t < A("p10"):
        source_tag(cr, t, A("p9", "seven"), "CDC", y=270)
    hl(cr, t, [("treatable ", GREEN), ("if caught early", INK)], 215, 62, A("p10"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    set_camera(camera(t, [(A("p11") - 0.2, focus(420, 1.5, screen=640))], dur=0.14))
    enter_world(cr)
    sky_ground(cr, ground=hexc("#e2c48f"))
    actor(cr, "doctor", 420, t, facing=1, arms=("point", "hip"), eyes="open", mouth="talk")
    hl(cr, t, [("plague ", RED), ("in America?", INK)], 215, 70, A("p11"), bold=True, underline=True)
    cr.identity_matrix()
    buttons(cr, t, A("p11", "comments"), (("YES", GREEN), ("NO", RED)), y=470, s=0.85)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"lab": scene_lab, "hospital": scene_hospital, "podium": scene_podium, "usa": scene_usa,
     "end": scene_end}[name](cr, t, tl)
    cr.restore()
    badge(cr, t, "WORLD", "5 OCT 2026")
    captions(cr, t, tl)
