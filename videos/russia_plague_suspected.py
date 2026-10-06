"""News: a lab worker at Russia's Irkutsk Anti-Plague Institute died; plague is suspected but not confirmed (Oct 2026).

Host-and-Globe format (motion/newsdesk.py); Globe in Russia's colours. Script approved by the owner on 5 Oct 2026.
The worker is not named (privacy). "Suspected" throughout: Russia's health agency calls it pneumonia of unknown cause.

Facts, as of 5 October 2026:
- A 28-year-old laboratory technician at the Irkutsk Anti-Plague Institute (Siberia) was hospitalised on 29 Sep 2026
  and died days later; suspected pneumonic plague. Al Jazeera
  https://www.aljazeera.com/news/2026/10/5/russian-lab-worker-dies-of-suspected-plague-in-siberia-us-monitoring-case ;
  Meduza https://meduza.io/en/feature/2026/10/05/hospitals-in-irkutsk-impose-quarantines-after-an-employee-at-an-anti-plague-institute-dies-russia-s-public-health-agency-says-she-died-of-pneumonia-and-the-epidemiological-situation-remains-stable ;
  Business Standard https://www.business-standard.com/amp/health/russia-plague-scare-nearly-200-face-quarantine-after-lab-worker-dies-126100500079_1.html ;
  CNN https://www.cnn.com/2026/10/04/europe/russia-laboratory-plague-accident-intl
- 197 possible contacts isolated; several hospitals under three-week quarantine; Rospotrebnadzor: situation "stable",
  "pneumonia of unknown cause", no microorganisms linked to her work found. Meduza; Al Jazeera; Business Standard.
- US State Department: "We are aware ... monitoring the situation closely." Al Jazeera.
- Plague is caused by Yersinia pestis, "known as the 'Black Death' during the fourteenth century"; "antibiotic
  treatment is effective ... early diagnosis and treatment can save lives." WHO https://www.who.int/news-room/fact-sheets/detail/plague ;
  CDC https://www.cdc.gov/plague/diagnosis-testing/index.html
"""
from motion.engine import INK, RED, at, ease_out, hexc, pop, seg, write
from motion.kit import hl, stamp
from motion.news import GREEN, crowd, date_stamp, panel, source_tag, tick
from motion.newsdesk import background, cam_keys, dialogue, end_scene, host, make_draw, mood, talking_globe
from motion.newsprops import binoculars, biohazard_door, hospital, map_pin, old_scroll, pill_bottle

NARRATOR = dict(speed=0.95)
TAIL = 0.9
CODE = "ru"

SCRIPT = dialogue([
    ("p1", "talk", "H", "A lab worker in Siberia has died. And doctors suspect the plague."),
    ("p2", "talk", "G", "The suspected germ is the same one behind the Black Death."),
    ("p3", "talk", "H", "Wait. Where did this happen?"),
    ("p4", "talk", "G", "In Irkutsk, Russia. At an institute that studies plague."),
    ("p5", "talk", "G", "A twenty-eight-year-old lab technician was taken to hospital on September twenty-ninth. "
                        "She died days later."),
    ("p6", "talk", "H", "Is it spreading?"),
    ("p7", "talk", "G", "Officials say the situation is stable. But [one hundred ninety-seven|197] people "
                        "who may have had contact were isolated."),
    ("p8", "talk", "G", "And several hospitals went into a three-week quarantine."),
    ("p9", "talk", "H", "So is it confirmed plague?"),
    ("p10", "talk", "G", "Not yet. Russia's health agency calls it pneumonia of unknown cause."),
    ("p11", "talk", "G", "The US State Department says it is monitoring closely."),
    ("p12", "talk", "H", "And here's the good news. Today, plague can be treated with antibiotics if it's caught early."),
    ("p13", "end", "H", "Did you know plague still exists today? Tell me in the comments."),
])

METADATA = dict(
    title="A Lab Worker Died. Doctors Suspect the Plague 😷",
    alt_titles=["Suspected Plague Case at a Russian Lab: What We Know",
                "Nearly 200 Isolated After a Suspected Plague Death"],
    description="""A 28-year-old lab technician at the Irkutsk Anti-Plague Institute in Siberia, Russia, died days after being hospitalised on 29 September 2026. Doctors suspect pneumonic plague, caused by the same germ behind the Black Death. 😷

What we know: 197 people who may have had contact were isolated, and several hospitals went into a three-week quarantine. Russia's health agency says the situation is stable and calls the illness "pneumonia of unknown cause": plague is NOT confirmed. The US State Department says it is monitoring closely.
Good to know: plague is treatable with antibiotics if it is caught early (WHO, CDC).

Facts as of 5 October 2026.

💬 Did you know plague still exists today? 👇

Sources:
• Al Jazeera (5 Oct 2026): https://www.aljazeera.com/news/2026/10/5/russian-lab-worker-dies-of-suspected-plague-in-siberia-us-monitoring-case
• Meduza (5 Oct 2026): https://meduza.io/en/feature/2026/10/05/hospitals-in-irkutsk-impose-quarantines-after-an-employee-at-an-anti-plague-institute-dies-russia-s-public-health-agency-says-she-died-of-pneumonia-and-the-epidemiological-situation-remains-stable
• CNN (4 Oct 2026): https://www.cnn.com/2026/10/04/europe/russia-laboratory-plague-accident-intl
• Business Standard (5 Oct 2026): https://www.business-standard.com/amp/health/russia-plague-scare-nearly-200-face-quarantine-after-lab-worker-dies-126100500079_1.html
• WHO plague fact sheet: https://www.who.int/news-room/fact-sheets/detail/plague
• CDC: https://www.cdc.gov/plague/diagnosis-testing/index.html""",
    hashtags=["#Plague", "#Russia", "#News"],
    tags=["plague", "russia", "irkutsk", "black death", "suspected plague", "lab accident", "quarantine",
          "health news", "world news", "news explained"],
    pinned_comment="Did you know plague still exists today? Yes or no? 👇",
)


def scene_talk(cr, t, tl):
    A = tl.at
    background(cr, t, cam_keys(tl))
    host(cr, t, tl, **mood(t, tl, [("p3", dict(eyes="wide", mouth="o", arms=("cheer", "hip"))), ("p4", {}),
                                    ("p6", dict(eyes="sad", mouth="flat", sweat=True)), ("p7", {}),
                                    ("p9", dict(eyes="dot", mouth="flat", arms=("chin", "hip"))), ("p10", {}),
                                    ("p12", dict(eyes="happy", mouth="smile", arms=("thumb", "hip")))], {}))
    eyes, idle = mood(t, tl, [("p5", ("sad", "flat")), ("p7", ("dot", "flat")), ("p10", ("sly", "flat"))],
                      ("wide", "flat"))
    talking_globe(cr, t, tl, CODE, eyes, idle)

    cr.identity_matrix()
    hl(cr, t, [("SUSPECTED ", RED), ("plague", INK)], 215, 56, 0.0, bold=True, sound=False)

    panel(cr, t, 0.15, A("p2"), 360, 400, 260, 260, lambda c: biohazard_door(c, 0, 0, 1.0), seed=9800)
    panel(cr, t, A("p2", "Black"), A("p3"), 360, 400, 460, 200,
          lambda c: old_scroll(c, 0, 0, "the Black Death", "Europe, 1300s"), seed=9810)
    source_tag(cr, t, A("p2", "Black"), "World Health Organization", end=A("p3"))
    panel(cr, t, A("p4", "Irkutsk"), A("p5"), 360, 400, 500, 220, lambda c: map_pin(c, 0, 0, "Irkutsk, Siberia, Russia"),
          seed=9820)

    def admitted(c):
        hospital(c, 0, 0, 1.0)
    panel(cr, t, A("p5", "hospital"), A("p6"), 360, 400, 300, 220, admitted, seed=9830)
    date_stamp(cr, t, A("p5", "September"), "29 SEP 2026", x=585, y=118, end=A("p6"))

    def isolated(c):
        u = seg(t, A("p7", "hundred"), A("p7", "hundred") + 1.2)
        crowd(c, 0, -20, t, 60, cols=15, gap=26, progress=ease_out(u))
        write(c, [(f"{int(197 * ease_out(u))} isolated", RED)], 0, 96, 44, align="center", bold=True)
    panel(cr, t, A("p7", "hundred"), A("p8"), 360, 400, 520, 260, isolated, seed=9840)

    def quarantine(c):
        hospital(c, -90, 0, 0.8)
        write(c, [("QUARANTINE", RED)], 110, -6, 34, align="center", bold=True)
        write(c, [("3 weeks", INK)], 110, 36, 32, align="center", bold=True)
    panel(cr, t, A("p8", "hospitals"), A("p9"), 360, 400, 520, 220, quarantine, seed=9850)
    source_tag(cr, t, A("p7", "Officials"), "Meduza; Al Jazeera (5 Oct 2026)", end=A("p9"))

    if A("p10") <= t < A("p10", "health"):
        stamp(cr, t, A("p10"), "NOT CONFIRMED", dur=A("p10", "health") - A("p10"), y=440)

    def agency(c):
        write(c, [("\"pneumonia of", INK)], 0, -20, 40, align="center", bold=True)
        write(c, [("unknown cause\"", INK)], 0, 26, 40, align="center", bold=True)
        write(c, [("Russia's health agency", hexc("#1f4fb0"))], 0, 70, 26, align="center")
    panel(cr, t, A("p10", "health"), A("p11"), 360, 400, 480, 200, agency, seed=9860)

    def monitoring(c):
        binoculars(c, -120, 0, 1.0)
        write(c, [("US State Dept:", INK)], 90, -14, 30, align="center", bold=True)
        write(c, [("\"monitoring\"", INK)], 90, 26, 30, align="center", bold=True)
    panel(cr, t, A("p11", "State"), A("p12"), 360, 400, 500, 190, monitoring, seed=9870)

    def treatable(c):
        pill_bottle(c, -110, 10, 1.0)
        tick(c, 60, -20, 22, col=GREEN)
        write(c, [("treatable", GREEN)], 110, 30, 36, align="center", bold=True)
        write(c, [("if caught early", INK)], 110, 66, 26, align="center", bold=True)
    panel(cr, t, A("p12", "antibiotics"), A("p13") + 0.1, 360, 400, 500, 240, treatable, seed=9880)
    source_tag(cr, t, A("p12", "antibiotics"), "WHO; CDC", end=A("p13"))


def scene_end(cr, t, tl):
    end_scene(cr, t, tl, CODE, "p13", [("plague ", RED), ("still exists?", INK)],
              prop=lambda c: pill_bottle(c, 0, 0, 0.9))


draw = make_draw({"talk": scene_talk, "end": scene_end})
