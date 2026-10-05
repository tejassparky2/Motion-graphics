"""Tesla's Cybercab driverless taxis in Austin: a bumpy first month (CNBC, 3 Oct 2026), story style, our own cast.
The car is a generic drawn robotaxi (no logo); Elon Musk is only quoted on a card, not drawn.

Facts, as of 5 October 2026:
- No steering wheel or pedals; paid rides in Austin, Texas began in September 2026. Wikipedia
  https://en.wikipedia.org/wiki/Tesla_Cybercab ; CNBC https://www.cnbc.com/2026/10/03/tesla-cybercab-pressure-to-expand-after-rocky-first-month-in-austin.html
- Complaints: long waits, wrong pickup and drop-off spots, butterfly doors and trunk problems (CNBC; Tesla North
  https://teslanorth.com/2026/10/04/elon-musk-touts-careful-cybercab-rollout-austin-fleet-169/ ; ARY News
  https://arynews.tv/teslas-cybercab-faces-a-tough-test-after-rocky-austin-debut-heres-why).
- No major incidents reported (Tesla North citing CNBC); NHTSA review/audit (Wikipedia; ARY/CNBC).
- Austin fire captain asked for state or national emergency protocols (Tesla North citing CNBC; ARY).
- Cybercabs registered in Texas: 45 at launch, 169 as of 2 Oct (Texas DMV via CNBC; Tesla North).
- Musk on X, 3 Oct: "We are being extremely careful with autonomous safety..." (Tesla North).
"""
import math

from motion.captions import captions
from motion.engine import INK, RED, WHITE, at, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from motion.news import source_tag, tick
from motion.newsbrand import badge
from motion.newsprops import clipboard, clock, counter, robotaxi, wrong_pin
from motion.story import buttons
from motion.storykit import (GOLD, GREEN, NAVY, actor, billboard, building, focus, news_pacing, reveal_gaps, sign,
                             sky_ground)

news_pacing()

NARRATOR = dict(speed=0.95)
TAIL = 0.5
# news bed (motion/newsmusic.py); the drop is a beat of silence before the safety review line
MUSIC = dict(mood="tech", drops=['c8'])

SCRIPT = [
    dict(id="c1", scene="austin", text="In Austin, Texas, you can now pay for a taxi ride with no driver."),
    dict(id="c2", scene="austin", text="The car is Tesla's Cybercab, and it has no steering wheel and no pedals."),
    dict(id="c3", scene="austin", text="Tesla started charging for rides in September, so the first month is now over."),
    dict(id="c4", scene="ride", text="It was a bumpy start."),
    dict(id="c5", scene="ride", text="Passengers complained about long waits and about cars picking them up in the "
                                     "wrong spots."),
    dict(id="c6", scene="ride", text="Some also had problems with the doors and the trunk."),
    dict(id="c7", scene="safety", text="So far, no major crashes have been reported."),
    dict(id="c8", scene="safety", text="But federal safety regulators have opened a review of the car."),
    dict(id="c9", scene="safety", text="Austin firefighters have also asked for clear rules on how to handle a car "
                                       "with no driver controls."),
    dict(id="c10", scene="lot", text="Even so, Tesla is not slowing down."),
    dict(id="c11", scene="lot", text="The number of Cybercabs registered in Texas has grown from [forty-five|45] to "
                                     "[one hundred sixty-nine.|169.]"),
    dict(id="c12", scene="lot", text="Elon Musk says the company is being extremely careful with safety."),
    dict(id="c13", scene="end", text="Would you ride in a car with no steering wheel? Tell me in the comments."),
]
reveal_gaps(SCRIPT, MUSIC)

METADATA = dict(
    title="Tesla's Driverless Taxi Had a Bumpy First Month 🚕",
    alt_titles=["A Taxi With No Steering Wheel: Month One in Austin", "Tesla Cybercab's First Month, Explained"],
    description="""In Austin, Texas, you can now ride in Tesla's Cybercab: no steering wheel, no pedals, no driver. Paid rides started in September 2026. 🚕

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

TEAL = hexc("#2e9e8f")


def austin_set(cr, t):
    sky_ground(cr)
    building(cr, -120, 360, 560, hexc("#e8c9a8"), "AUSTIN, TX", seed=19000)
    building(cr, 1300, 380, 480, hexc("#c9d8e8"), None, seed=19050)


def cab(cr, x, t, doors=0.0, s=1.6, label=True):
    robotaxi(cr, x, 840, s, t, doors=doors, seed=19100)
    if label:
        write(cr, [("CYBERCAB", INK)], x - 10, 832, 18 * s, align="center", bold=True)


def scene_austin(cr, t, tl):
    A = tl.at
    keys = [(0, (1.4, 480, 830)), (A("c1", "taxi"), (1.6, 640, 800)), (A("c1", "driver"), (1.6, 620, 800)),
            (A("c2"), (1.2, 620, 820)), (A("c2", "wheel"), (2.2, 700, 760)), (A("c3"), focus(300, 1.6)),
            (A("c3", "month"), (1.3, 480, 820))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    austin_set(cr, t)
    arrive = ease_out(seg(t, 0.2, A("c1", "taxi") + 0.3))
    cab(cr, lerp(1500, 640, arrive), t, doors=seg(t, A("c1", "driver"), A("c1", "driver") + 0.5))
    if A("c2", "wheel") <= t < A("c3"):   # inside: an empty seat, no wheel
        with at(cr, 700, 700, 1.0):
            shape(cr, rrect_pts(-130, -90, 260, 170, 16, 14), WHITE, seed=19120, amp=0.4, lw=4)
            shape(cr, rrect_pts(-110, -60, 70, 120, 14, 12), hexc("#3b3f4a"), seed=19121, amp=0.3, lw=3)
            with at(cr, 50, -10, 1.0):
                line(cr, [(-40, -40), (40, 40)], 9, RED, 19122, amp=0.2)
                line(cr, [(40, -40), (-40, 40)], 9, RED, 19123, amp=0.2)
            write(cr, [("no wheel", RED)], 50, 70, 26, align="center", bold=True)
    actor(cr, "rider", 300, t, facing=1, arms=("wave", "hold") if t < A("c3") else ("thumb", "hold"),
          eyes="wide" if A("c2", "wheel") <= t < A("c3") else "happy", mouth="o" if t < A("c3") else "grin")
    if t >= A("c3", "September"):
        sign(cr, 300, 470, "since SEP 2026", RED, start=A("c3", "September"), t=t)
    hl(cr, t, [("a taxi with ", INK), ("NO DRIVER", RED)], 215, 66, A("c1", "taxi"), end=A("c2") - 0.05, bold=True)
    hl(cr, t, [("Tesla ", RED), ("Cybercab", INK)], 215, 80, A("c2"), end=A("c3") - 0.05, bold=True)
    hl(cr, t, [("month ", INK), ("ONE", RED), (" is over", INK)], 215, 74, A("c3"), bold=True)


def scene_ride(cr, t, tl):
    A = tl.at
    keys = [(A("c4") - 0.2, (1.2, 560, 830)), (A("c5", "waits"), focus(300, 1.8)),
            (A("c5", "wrong"), (1.5, 560, 760)), (A("c6"), (1.5, 800, 800))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    austin_set(cr, t)
    bump = math.sin(t * 25) * 6 if A("c4", "bumpy") <= t < A("c4", "bumpy") + 0.6 else 0
    cr.save()
    cr.translate(0, bump)
    cab(cr, 820, t, doors=0.5 + 0.5 * math.sin(t * 4) if t >= A("c6") else 0.0)
    cr.restore()
    angry = t >= A("c5", "waits")
    actor(cr, "rider", 300, t, facing=1, arms=("chin", "hold") if angry else ("hip", "hip"),
          eyes="sly" if angry else "open", mouth="flat" if angry else "o")
    if t >= A("c5", "waits"):
        with at(cr, 300, 520, pop(t, A("c5", "waits"), 0.2) or 0.01):
            clock(cr, 0, 0, 1.3, t * 4)
    if t >= A("c5", "wrong"):
        with at(cr, 560, 560, pop(t, A("c5", "wrong"), 0.2) or 0.01):
            wrong_pin(cr, 0, 0, 1.5)
    hl(cr, t, [("a ", INK), ("BUMPY", RED), (" start", INK)], 215, 80, A("c4", "bumpy"), end=A("c5") - 0.05, bold=True)
    hl(cr, t, [("long ", INK), ("WAITS", RED)], 215, 84, A("c5", "waits"), end=A("c5", "wrong") - 0.05, bold=True)
    hl(cr, t, [("wrong ", INK), ("SPOTS", RED)], 215, 84, A("c5", "wrong"), end=A("c6") - 0.05, bold=True)
    hl(cr, t, [("doors and ", INK), ("TRUNKS", RED)], 215, 74, A("c6"), bold=True)
    if t >= A("c5"):
        source_tag(cr, t, A("c5"), "CNBC, 3 Oct 2026", y=270)


def scene_safety(cr, t, tl):
    A = tl.at
    keys = [(A("c7") - 0.2, (1.2, 640, 820)), (A("c8", "regulators"), focus(380, 1.6)), (A("c8", "review"), (1.4, 560, 800)),
            (A("c9"), focus(980, 1.6)), (A("c9", "rules"), (1.3, 860, 810))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    austin_set(cr, t)
    cab(cr, 640, t)
    if A("c7") <= t < A("c8"):
        with at(cr, 640, 560, pop(t, A("c7"), 0.2) or 0.01):
            shape(cr, rrect_pts(-170, -60, 340, 120, 14, 14), WHITE, seed=19300, amp=0.4, lw=5)
            tick(cr, -120, -6, 26, col=GREEN)
            write(cr, [("no major crashes", INK)], 30, 12, 32, align="center", bold=True)
    if t >= A("c8"):
        actor(cr, "inspector", 380, t, facing=1, arms=("hold", "point"), eyes="sly", mouth="flat")
        with at(cr, 420, 560, pop(t, A("c8", "review"), 0.2) or 0.01):
            clipboard(cr, 0, 0, "SAFETY REVIEW", 0.9)
    if t >= A("c9"):
        actor(cr, "firefighter", 980, t, facing=-1, arms=("chin", "hip"), eyes="open", mouth="flat")
        if t >= A("c9", "rules"):
            sign(cr, 940, 520, "clear rules, please?", INK, start=A("c9", "rules"), t=t, s=0.8, seed=19310)
    hl(cr, t, [("no major ", INK), ("CRASHES", GREEN)], 215, 74, A("c7"), end=A("c8") - 0.05, bold=True)
    hl(cr, t, [("federal ", INK), ("SAFETY REVIEW", RED)], 215, 62, A("c8"), end=A("c9") - 0.05, bold=True)
    hl(cr, t, [("firefighters ", INK), ("want rules", RED)], 215, 66, A("c9"), bold=True)


def scene_lot(cr, t, tl):
    A = tl.at
    keys = [(A("c10") - 0.2, (1.0, 640, 830)), (A("c11"), (1.05, 640, 800)), (A("c11", "169"), (1.3, 640, 740)),
            (A("c12"), (1.3, 640, 700))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    sky_ground(cr, ground=hexc("#b9bcc4"))
    n = 3 + int(9 * ease_out(seg(t, A("c11", "45"), A("c11", "169") + 0.5)))
    for k in range(n):
        row, col = divmod(k, 4)
        robotaxi(cr, 130 + col * 330 + (row % 2) * 90, 930 - row * 95, 1.15 - row * 0.08, t, seed=19400 + k)
    if t < A("c12"):
        def count(c):
            counter(c, 0, -40, 45, 169, seg(t, A("c11", "45"), A("c11", "169") + 0.4), 1.2, col=RED)
            write(c, [("Cybercabs registered in Texas", INK)], 0, 70, 28, align="center", bold=True)
        if t >= A("c11"):
            billboard(cr, 640, 500, 560, 260, count, seed=19450)
    else:
        def quote(c):
            write(c, [("\"extremely careful", INK)], 0, -30, 40, align="center", bold=True)
            write(c, [("with autonomous safety\"", INK)], 0, 16, 40, align="center", bold=True)
            write(c, [("Elon Musk on X, 3 Oct 2026", hexc("#b8102a"))], 0, 66, 26, align="center")
        billboard(cr, 640, 500, 600, 260, quote, seed=19460)
    hl(cr, t, [("NOT", RED), (" slowing down", INK)], 215, 74, A("c10"), end=A("c11") - 0.05, bold=True)
    hl(cr, t, [("45", INK), (" to ", INK), ("169", RED)], 215, 90, A("c11"), end=A("c12") - 0.05, bold=True)
    if A("c11") <= t < A("c12"):
        source_tag(cr, t, A("c11"), "Texas DMV records via CNBC", y=270)
    hl(cr, t, [("Musk: ", INK), ("\"extremely careful\"", RED)], 215, 58, A("c12"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    set_camera(camera(t, [(A("c13") - 0.2, (1.5, 520, 840))], dur=0.14))
    enter_world(cr)
    austin_set(cr, t)
    cab(cr, 720, t, doors=0.6)
    actor(cr, "rider", 360, t, facing=1, arms=("point", "hold"), eyes="open", mouth="talk")
    hl(cr, t, [("would ", INK), ("YOU", RED), (" ride?", INK)], 215, 74, A("c13"), bold=True, underline=True)
    cr.identity_matrix()
    buttons(cr, t, A("c13", "comments"), (("YES", GREEN), ("NO", RED)), y=470, s=0.85)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"austin": scene_austin, "ride": scene_ride, "safety": scene_safety, "lot": scene_lot,
     "end": scene_end}[name](cr, t, tl)
    cr.restore()
    badge(cr, t, "TECH", "5 OCT 2026")
    captions(cr, t, tl)
