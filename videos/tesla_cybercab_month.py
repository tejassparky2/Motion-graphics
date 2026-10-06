"""Tech news: Tesla's Cybercab driverless taxi had a bumpy first month in Austin (CNBC, 3 Oct 2026).

Host-and-Globe format (motion/newsdesk.py); the Globe shaped like Tesla's T (our own drawing) in Tesla red, "TESLA"
on the base (owner's choice). Script approved by the owner on 5 Oct 2026.

Facts, as of 5 October 2026:
- Cybercab has no steering wheel, pedals, side mirrors or back window; Tesla began paid Cybercab rides in Austin,
  Texas, on 4 Sep 2026 (launch event 3 Sep). Wikipedia https://en.wikipedia.org/wiki/Tesla_Cybercab ;
  CNBC https://www.cnbc.com/2026/10/03/tesla-cybercab-pressure-to-expand-after-rocky-first-month-in-austin.html
- Complaints: long waits, wrong pickup and drop-off spots, butterfly doors and trunk problems. CNBC; Tesla North
  https://teslanorth.com/2026/10/04/elon-musk-touts-careful-cybercab-rollout-austin-fleet-169/ ;
  ARY News https://arynews.tv/teslas-cybercab-faces-a-tough-test-after-rocky-austin-debut-heres-why
- No major incidents reported (Tesla North citing CNBC). NHTSA opened a compliance review/audit (Wikipedia; ARY/CNBC).
- Austin fire captain asked for state or national emergency protocols for driverless cars (Tesla North citing CNBC;
  ARY: first responders raised concerns).
- Cybercabs registered in Texas: 45 at launch, 169 as of 2 Oct (Texas DMV records via CNBC; Tesla North).
- Musk (X, 3 Oct): "We are being extremely careful with autonomous safety..." (Tesla North).
"""
from motion.engine import INK, RED, ease_out, hexc, seg, write
from motion.kit import hl
from motion.news import GREEN, date_stamp, panel, source_tag
from motion.newsdesk import background, cam_keys, dialogue, end_scene, host, make_draw, mood, talking_globe
from motion.newsprops import clipboard, clock, counter, fire_helmet, no_wheel, open_trunk, robotaxi, wrong_pin

NARRATOR = dict(speed=0.95)
TAIL = 0.9
CODE = "tesla"

SCRIPT = dialogue([
    ("c1", "talk", "H", "Imagine a taxi with no steering wheel. No pedals. And no driver."),
    ("c2", "talk", "G", "That's Tesla's Cybercab. Paid rides started in Austin, Texas, in September."),
    ("c3", "talk", "H", "So how did the first month go?"),
    ("c4", "talk", "G", "Bumpy. Riders complained about long waits, wrong pickup spots, and doors and trunks acting up."),
    ("c5", "talk", "H", "Anything serious?"),
    ("c6", "talk", "G", "No major crashes have been reported. But federal safety regulators opened a review of the car."),
    ("c7", "talk", "G", "And Austin firefighters asked for clear rules on handling a car with no driver controls."),
    ("c8", "talk", "H", "Is Tesla slowing down?"),
    ("c9", "talk", "G", "Not really. Its Cybercabs registered in Texas went from [forty-five|45] to "
                        "[one hundred sixty-nine.|169.]"),
    ("c10", "talk", "G", "Elon Musk says they are being extremely careful with safety."),
    ("c11", "end", "H", "Would you ride in a car with no steering wheel? Tell me in the comments."),
])

METADATA = dict(
    title="Tesla's Driverless Taxi Had a Bumpy First Month 🚕",
    alt_titles=["A Taxi With No Steering Wheel: Month One in Austin",
                "Tesla Cybercab's First Month, Explained"],
    description="""Tesla's Cybercab has no steering wheel and no pedals. Paid rides started in Austin, Texas, in September 2026. 🚕

Month one: riders complained about long waits, wrong pickup spots, and doors and trunks acting up. No major crashes have been reported, but federal safety regulators (NHTSA) opened a review, and Austin firefighters asked for clear rules for cars with no driver controls. Tesla isn't slowing down: Cybercabs registered in Texas went from 45 to 169. Elon Musk says Tesla is being "extremely careful with autonomous safety".

Facts as of 5 October 2026.

💬 Would you ride in a car with no steering wheel? 👇

Sources:
• CNBC (3 Oct 2026): https://www.cnbc.com/2026/10/03/tesla-cybercab-pressure-to-expand-after-rocky-first-month-in-austin.html
• Tesla North (4 Oct 2026): https://teslanorth.com/2026/10/04/elon-musk-touts-careful-cybercab-rollout-austin-fleet-169/
• ARY News: https://arynews.tv/teslas-cybercab-faces-a-tough-test-after-rocky-austin-debut-heres-why
• Wikipedia, Tesla Cybercab: https://en.wikipedia.org/wiki/Tesla_Cybercab

Not affiliated with or endorsed by Tesla.""",
    hashtags=["#Tesla", "#Cybercab", "#TechNews"],
    tags=["tesla", "cybercab", "robotaxi", "self driving", "driverless car", "austin", "elon musk", "tech news",
          "autonomous vehicles", "news explained"],
    pinned_comment="Would you ride in a car with no steering wheel? Yes or no? 👇",
)


def scene_talk(cr, t, tl):
    A = tl.at
    background(cr, t, cam_keys(tl))
    host(cr, t, tl, **mood(t, tl, [("c3", dict(eyes="dot", mouth="flat", arms=("chin", "hip"))), ("c4", {}),
                                    ("c5", dict(eyes="wide", mouth="o", sweat=True)), ("c6", {}),
                                    ("c8", dict(eyes="sly", mouth="flat", arms=("chin", "hip")))], {}))
    eyes, idle = mood(t, tl, [("c4", ("sly", "smirk")), ("c6", ("dot", "flat")), ("c9", ("happy", "smile"))],
                      ("happy", "smile"))
    talking_globe(cr, t, tl, CODE, eyes, idle)

    cr.identity_matrix()
    hl(cr, t, [("TESLA ", RED), ("Cybercab", INK)], 215, 56, 0.0, bold=True, sound=False)

    panel(cr, t, 0.15, A("c2"), 360, 400, 420, 240, lambda c: no_wheel(c, -40, 0, 1.2), seed=9900)
    panel(cr, t, A("c2", "Cybercab"), A("c3"), 360, 400, 440, 220,
          lambda c: (robotaxi(c, 0, -10, 1.1, t), write(c, [("Austin, Texas", INK)], 0, 90, 28, align="center",
                                                             bold=True)), seed=9910)
    date_stamp(cr, t, A("c2", "September"), "SEP 2026", x=585, y=118)

    def complaints(c):
        if t >= A("c4", "waits"):
            clock(c, -180, -10, 1.1, t)
            write(c, [("long waits", INK)], -180, 70, 24, align="center", bold=True)
        if t >= A("c4", "pickup"):
            wrong_pin(c, 0, 0, 1.2)
            write(c, [("wrong spots", INK)], 0, 70, 24, align="center", bold=True)
        if t >= A("c4", "doors"):
            open_trunk(c, 180, 0, 1.1)
            write(c, [("doors, trunks", INK)], 180, 70, 24, align="center", bold=True)
    panel(cr, t, A("c4", "waits"), A("c5"), 360, 400, 600, 210, complaints, seed=9920)
    source_tag(cr, t, A("c4", "Riders"), "CNBC (3 Oct 2026)", end=A("c5"))

    panel(cr, t, A("c6", "regulators"), A("c7"), 360, 400, 300, 240,
          lambda c: clipboard(c, 0, 0, "SAFETY REVIEW"), seed=9930)
    panel(cr, t, A("c7", "firefighters"), A("c8"), 360, 400, 460, 210,
          lambda c: (fire_helmet(c, -110, 0, 0.9), write(c, [("clear rules,", INK)], 110, -6, 30, align="center",
                                                             bold=True),
                     write(c, [("please", INK)], 110, 30, 30, align="center", bold=True)), seed=9940)

    def fleet(c):
        u = seg(t, A("c9", "45"), A("c9", "169") + 0.4)
        counter(c, 0, -20, 45, 169, u, 1.0, col=RED)
        write(c, [("Cybercabs registered in Texas", INK)], 0, 74, 26, align="center", bold=True)
    panel(cr, t, A("c9", "registered"), A("c10"), 360, 400, 520, 220, fleet, seed=9950)
    source_tag(cr, t, A("c9", "registered"), "Texas DMV records via CNBC", end=A("c10"))

    def quote(c):
        write(c, [("\"extremely careful", INK)], 0, -16, 38, align="center", bold=True)
        write(c, [("with autonomous safety\"", INK)], 0, 26, 38, align="center", bold=True)
        write(c, [("Elon Musk, 3 Oct 2026", hexc("#b8102a"))], 0, 70, 26, align="center")
    panel(cr, t, A("c10", "Musk"), A("c11") + 0.1, 360, 400, 560, 200, quote, seed=9960)


def scene_end(cr, t, tl):
    end_scene(cr, t, tl, CODE, "c11", [("would ", INK), ("YOU", RED), (" ride?", INK)],
              prop=lambda c: robotaxi(c, 0, 0, 0.9, t))


draw = make_draw({"talk": scene_talk, "end": scene_end})
