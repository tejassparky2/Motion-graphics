"""US jobs report for September 2026 (released 2 Oct 2026), told in the story style with our own cast.

Facts, as of 5 October 2026:
- +29,000 jobs in September; unemployment 4.2%; average hourly earnings +3.0% over 12 months. U.S. Bureau of Labor
  Statistics, Employment Situation, 2 Oct 2026 https://www.bls.gov/news.release/empsit.nr0.htm
- Economists expected about 90,000 (Reuters poll 90,000; Dow Jones 84,000). Al Jazeera
  https://www.aljazeera.com/economy/2026/10/2/us-job-growth-slows-as-unemployment-rises-before-midterm-elections ;
  Yahoo Finance https://finance.yahoo.com/economy/article/septembers-jobs-report-shows-the-us-added-just-29000-jobs-and-unemployment-ticked-up-195320409.html
- July and August revised down by a combined 60,000. Yahoo Finance; CNBC
  https://www.cnbc.com/2026/10/02/jobs-report-september-2026.html
- 3% wage growth, slowest since 2021 (CNBC; Al Jazeera "slowest in five years").
- Gains: health care +17,000, construction +11,000, manufacturing +9,000 (Al Jazeera; Yahoo Finance).
- "Low-hire, low-fire labor market" (Adam Schickling, Vanguard, via Yahoo Finance); CNN
  https://www.cnn.com/2026/10/02/economy/us-jobs-report-september-final
"""
import math

from motion.captions import captions
from motion.engine import INK, RED, WHITE, at, dot, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from motion.news import source_tag
from motion.newsbrand import badge
from motion.newsprops import bars, gauge, job_icon, wallet
from motion.story import buttons
from motion.storykit import (GOLD, GREEN, NAVY, actor, billboard, building, focus, hospital, news_pacing, office,
                             comment_prompt, reveal_gaps, sign, sky_ground)

news_pacing()

NARRATOR = dict(speed=0.95)
TAIL = 0.3
# news bed (motion/newsmusic.py); the drop is a beat of silence before the real number: only 29,000 jobs
MUSIC = dict(mood="money", drops=['j2'])

SCRIPT = [   # v3, approved by the owner 5 Oct 2026 (research_notes/news_scripts_v3.md)
    dict(id="j1", scene="street", text="America added only [twenty-nine thousand|29,000] jobs in September."),
    dict(id="j2", scene="street", text="Economists expected about [ninety thousand,|90,000,] so the official number "
                                       "was less than a third of that."),
    dict(id="j3", scene="street", text="If you are looking for work, this matters to you."),
    dict(id="j4", scene="center", text="The unemployment rate also rose, from [four point one|4.1] to "
                                       "[four point two percent.|4.2%.]"),
    dict(id="j4b", scene="center", text="That means about four in every hundred people in the workforce are out of "
                                        "work and looking for a job."),
    dict(id="j6", scene="pay", text="Pay is growing slowly too."),
    dict(id="j7", scene="pay", text="Average hourly pay rose [three percent|3%] over the past year, the slowest rise "
                                    "since [twenty twenty-one.|2021.]"),
    dict(id="j8", scene="pay", text="So where are the new jobs?"),
    dict(id="j9", scene="pay", text="Most of them were in health care, with a few more in construction and in "
                                    "factories."),
    dict(id="j10", scene="door", text="Economists call this a low hire, low fire job market."),
    dict(id="j11", scene="door", text="Companies are not laying many people off, but they are not hiring many people "
                                      "either."),
    dict(id="j12", scene="door", text="The next jobs report comes out on November sixth, and we will tell you what it "
                                      "shows."),
    dict(id="j13", scene="end", text="Is it harder to find a job where you live?"),
]
reveal_gaps(SCRIPT, MUSIC)

METADATA = dict(
    title="America Added Just 29,000 Jobs. Here's What That Means 💼",
    alt_titles=["Economists Expected 90,000 Jobs. We Got 29,000.", "The September Jobs Report, Explained"],
    description="""Economists expected about 90,000 new US jobs in September 2026. The official report (2 October) showed just 29,000. 💼

Unemployment ticked up to 4.2%, July and August were revised down by a combined 60,000 jobs, and paychecks grew 3% in a year, the slowest since 2021. Most new jobs were in health care, plus some construction and manufacturing. Economists call it a "low-hire, low-fire" job market: few layoffs, but little hiring.

Facts as of 5 October 2026.

💬 Is it harder to find a job where you live? 👇

Sources:
• U.S. Bureau of Labor Statistics, Employment Situation (2 Oct 2026): https://www.bls.gov/news.release/empsit.nr0.htm
• Al Jazeera (2 Oct 2026): https://www.aljazeera.com/economy/2026/10/2/us-job-growth-slows-as-unemployment-rises-before-midterm-elections
• Yahoo Finance (2 Oct 2026): https://finance.yahoo.com/economy/article/septembers-jobs-report-shows-the-us-added-just-29000-jobs-and-unemployment-ticked-up-195320409.html
• CNBC (2 Oct 2026): https://www.cnbc.com/2026/10/02/jobs-report-september-2026.html
• CNN (2 Oct 2026): https://www.cnn.com/2026/10/02/economy/us-jobs-report-september-final
• BLS release schedule (next report 6 Nov 2026): https://www.bls.gov/schedule/news_release/empsit.htm""",
    hashtags=["#Jobs", "#Economy", "#News"],
    tags=["jobs report", "unemployment", "us economy", "september jobs report", "job market", "wages", "hiring",
          "economy news", "news explained", "bls"],
    pinned_comment="Is it harder to find a job where you live right now? Yes or no? 👇",
)


def street_set(cr, t):
    sky_ground(cr)
    building(cr, 150, 380, 430, hexc("#f1dfbd"), "JOB CENTER", seed=18000)
    building(cr, 1400, 360, 520, hexc("#d9c7e8"), "OFFICES", seed=18050)


def scene_street(cr, t, tl):
    A = tl.at
    keys = [(0, (1.0, 700, 830)), (A("j1", "29,000"), (1.2, 800, 700)), (A("j2"), (1.15, 780, 710)),
            (A("j2", "third"), (1.25, 760, 700)), (A("j3"), (1.4, 560, 800))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    street_set(cr, t)

    def chart(c):
        items = []
        if t >= A("j2", "90,000"):
            items.append(("expected", 90, hexc("#a9adb5"), "90K"))
        if t >= A("j1", "29,000"):
            items.append(("actual", 29, RED, "29K"))
        if items:
            bars(c, 0, 30, items, u=1.0, s=1.7, top=110 if len(items) > 1 else 36)
    billboard(cr, 800, 590, 540, 460, chart)
    walk = seg(t, 0, A("j2") + 1.0)
    actor(cr, "jobseeker", lerp(470, 560, walk), t, facing=1, walk=t * 2 if walk < 1 else None,
          arms=("hold", "down") if t < A("j3") else ("point", "hip"), eyes="sad" if t >= A("j1", "29,000") else "open",
          mouth="o" if A("j2", "third") <= t < A("j3") else "flat")
    hl(cr, t, [("only ", INK), ("29,000", RED), (" jobs", INK)], 215, 80, A("j1"), end=A("j2") - 0.05, bold=True)
    hl(cr, t, [("expected: ", INK), ("90,000", NAVY)], 215, 72, A("j2"), end=A("j3") - 0.05, bold=True)
    hl(cr, t, [("looking for ", INK), ("WORK?", RED)], 215, 72, A("j3"), bold=True)
    if t >= A("j1"):
        source_tag(cr, t, A("j1"), "U.S. Bureau of Labor Statistics", y=270)
    if A("j2", "third") <= t < A("j3"):
        stamp(cr, t, A("j2", "third"), "LESS THAN 1/3", dur=A("j3") - A("j2", "third"), y=480)


def scene_center(cr, t, tl):
    A = tl.at
    keys = [(A("j4") - 0.2, (1.0, 600, 850)), (A("j4", "4.1"), (1.7, 620, 610)), (A("j4b"), (1.2, 980, 840)),
            (A("j4b", "four"), (1.6, 990, 640))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    office(cr, t)
    write(cr, [("JOB CENTER", NAVY)], 620, 360, 56, align="center", bold=True)
    with at(cr, 620, 540, 1.3):
        gauge(cr, 0, -20, "4.2%" if t >= A("j4", "4.2%") else "4.1%",
              u=0.85 + 0.15 * seg(t, A("j4", "4.2%"), A("j4", "4.2%") + 0.5))
    for k, who in enumerate(("jobseeker", "worker", "rider", "mac_user")):   # a line of job seekers
        actor(cr, who, 300 + k * 130, t, facing=1, scale=0.9, arms=("hold", "down") if k == 0 else ("down", "down"),
              eyes="sad" if k % 2 == 0 else "open", mouth="flat")
    # "4 in every 100": a board of 100 people, 4 of them out of work
    shape(cr, rrect_pts(860, 430, 260, 300, 8, 14), WHITE, seed=18200, amp=0.4, lw=5)
    if t >= A("j4b"):
        u = seg(t, A("j4b", "four"), A("j4b", "four") + 0.6)
        for k in range(100):
            r, c = divmod(k, 10)
            out = k in (12, 37, 64, 88)
            dot(cr, 892 + c * 22, 470 + r * 22, 7, RED if out and u > 0 else hexc("#3f6fb5"))
        if u > 0:
            write(cr, [("4 in 100", RED)], 990, 712, 40, align="center", bold=True)
    actor(cr, "expert_b", 1200, t, facing=-1, arms=("point", "hip"), eyes="sly", mouth="flat")
    hl(cr, t, [("unemployment ", INK), ("UP", RED), (" to 4.2%", INK)], 215, 60, A("j4"),
       end=A("j4b") - 0.05, bold=True)
    hl(cr, t, [("about ", INK), ("4 in 100", RED), (" out of work", INK)], 215, 56, A("j4b"), bold=True)


def scene_pay(cr, t, tl):
    A = tl.at
    keys = [(A("j6") - 0.2, focus(300, 1.8)), (A("j7"), (1.5, 340, 790)), (A("j7", "slowest"), (1.4, 360, 800)),
            (A("j8"), (1.0, 800, 860)), (A("j9", "health"), (1.4, 560, 790)), (A("j9", "construction"), (1.5, 960, 820)),
            (A("j9", "factories"), (1.4, 1340, 800))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    sky_ground(cr)
    hospital(cr, 560)
    # construction frame and a factory
    for k in range(4):
        line(cr, [(860 + k * 70, 900), (860 + k * 70, 560)], 10, ORANGE_S, 18300 + k, amp=0.2)
    for k in range(3):
        line(cr, [(860, 640 + k * 90), (1070, 640 + k * 90)], 10, ORANGE_S, 18310 + k, amp=0.2)
    building(cr, 1340, 300, 380, hexc("#a9adb5"), "FACTORY", windows=False, seed=18320)
    actor(cr, "worker", 300, t, facing=1, arms=("hold", "hip"), eyes="happy" if t < A("j7", "slowest") else "sad",
          mouth="smile" if t < A("j7", "slowest") else "flat")
    with at(cr, 380, 700, 0.9):
        wallet(cr, 0, 0, 1.0)
    if t >= A("j7", "3%"):
        sign(cr, 300, 520, "+3% a year", GREEN, start=A("j7", "3%"), t=t)
    if t >= A("j7", "slowest"):
        sign(cr, 330, 440, "slowest since 2021", RED, start=A("j7", "slowest"), t=t, s=0.8, seed=18330)
    actor(cr, "doctor", 560, t, facing=1, arms=("wave", "down"), eyes="happy", mouth="smile")
    actor(cr, "builder", 1000, t, facing=-1, arms=("cheer", "down"), eyes="happy", mouth="grin")
    actor(cr, "worker", 1340, t, facing=-1, arms=("thumb", "down"), eyes="open", mouth="smile")
    hl(cr, t, [("pay grows ", INK), ("SLOWLY", RED)], 215, 74, A("j6"), end=A("j7") - 0.05, bold=True)
    hl(cr, t, [("+3%", GREEN), (" a year", INK)], 215, 80, A("j7"), end=A("j8") - 0.05, bold=True)
    hl(cr, t, [("where are the ", INK), ("JOBS", RED), ("?", INK)], 215, 66, A("j8"), end=A("j9", "health") - 0.05,
       bold=True)
    hl(cr, t, [("health care", RED)], 215, 84, A("j9", "health"), end=A("j9", "construction") - 0.05, bold=True)
    hl(cr, t, [("construction", ORANGE_S)], 215, 84, A("j9", "construction"), end=A("j9", "factories") - 0.05,
       bold=True)
    hl(cr, t, [("factories", NAVY)], 215, 84, A("j9", "factories"), bold=True)


ORANGE_S = hexc("#e8743b")


def scene_door(cr, t, tl):
    A = tl.at
    keys = [(A("j10") - 0.2, (1.1, 700, 840)), (A("j10", "low"), focus(560, 1.8)), (A("j11"), (1.3, 820, 810)),
            (A("j11", "hiring"), (1.7, 900, 620)), (A("j12"), focus(560, 1.5, screen=660))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    sky_ground(cr)
    building(cr, 900, 460, 560, hexc("#d9c7e8"), "COMPANY HQ", seed=18400)
    open_ = 0.15 + 0.1 * math.sin(t * 2)
    shape(cr, rrect_pts(860, 770, 80 * (1 - open_), 130, 4, 10), hexc("#b07a45"), seed=18410, amp=0.2, lw=3)
    actor(cr, "jobseeker", 560, t, facing=1, arms=("point", "hold") if t < A("j12") else ("hold", "hip"),
          eyes="sad" if A("j11", "hiring") <= t < A("j12") else "open", mouth="flat")
    actor(cr, "official_2", 1180, t, facing=-1, arms=("hip", "hip"), eyes="sly", mouth="smile")
    if t >= A("j10", "low"):
        sign(cr, 900, 470, "few layoffs", GREEN, start=A("j10", "low"), t=t, seed=18420)
    if t >= A("j11", "hiring"):
        sign(cr, 900, 560, "few hires", RED, start=A("j11", "hiring"), t=t, seed=18430)
    hl(cr, t, [("low hire, ", RED), ("low fire", NAVY)], 215, 80, A("j10", "low"), end=A("j12") - 0.05, bold=True)
    hl(cr, t, [("next report: ", INK), ("NOV 6", RED)], 215, 72, A("j12"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    set_camera(camera(t, [(A("j13") - 0.2, focus(520, 1.7, screen=640))], dur=0.14))
    enter_world(cr)
    street_set(cr, t)
    actor(cr, "jobseeker", 520, t, facing=1, arms=("point", "hold"), eyes="open", mouth="talk")
    hl(cr, t, [("harder to find a ", INK), ("JOB", RED), ("?", INK)], 215, 62, A("j13"), bold=True, underline=True)
    cr.identity_matrix()
    buttons(cr, t, A("j13") + 0.3, (("YES", GREEN), ("NO", RED)), y=330, s=0.85)
    comment_prompt(cr, t, A("j13") + 0.6)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"street": scene_street, "center": scene_center, "pay": scene_pay, "door": scene_door,
     "end": scene_end}[name](cr, t, tl)
    cr.restore()
    badge(cr, t, "US NEWS", "5 OCT 2026")
    captions(cr, t, tl)
