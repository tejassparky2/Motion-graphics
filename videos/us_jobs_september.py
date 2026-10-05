"""US news: the economy added just 29,000 jobs in September 2026 (jobs report, 2 Oct 2026).

Host-and-Globe format (motion/newsdesk.py); Globe in US colours. Script approved by the owner on 5 Oct 2026.

Facts, as of 5 October 2026:
- +29,000 nonfarm payroll jobs in September; unemployment rate 4.2% (from 4.1%); average hourly earnings +3.0% over
  12 months. U.S. Bureau of Labor Statistics, Employment Situation, released 2 Oct 2026
  https://www.bls.gov/news.release/empsit.nr0.htm
- Economists expected about 90,000 (Reuters and Bloomberg polls). Al Jazeera
  https://www.aljazeera.com/economy/2026/10/2/us-job-growth-slows-as-unemployment-rises-before-midterm-elections ;
  Yahoo Finance https://finance.yahoo.com/economy/article/septembers-jobs-report-shows-the-us-added-just-29000-jobs-and-unemployment-ticked-up-195320409.html
- July and August revised down by a combined 60,000. Yahoo Finance; CNBC
  https://www.cnbc.com/2026/10/02/jobs-report-september-2026.html
- 3% wage growth, slowest since 2021 (CNBC; Al Jazeera: slowest in five years).
- Gains in health care (+17,000), construction (+11,000), manufacturing (+9,000). Al Jazeera; Yahoo Finance.
- "Low-hire, low-fire labor market" (Adam Schickling, Vanguard, via Yahoo Finance); CNN
  https://www.cnn.com/2026/10/02/economy/us-jobs-report-september-final
"""
from motion.engine import INK, RED, ease_out, hexc, seg, write
from motion.kit import hl, stamp
from motion.news import GREEN, date_stamp, panel, source_tag
from motion.newsdesk import background, cam_keys, dialogue, end_scene, host, make_draw, mood, talking_globe
from motion.newsprops import bars, door, gauge, job_icon, wallet

NARRATOR = dict(speed=0.95)
TAIL = 0.9
CODE = "us"
NAVY = hexc("#3c3b6e")

SCRIPT = dialogue([
    ("j1", "talk", "H", "Economists expected [ninety thousand|90,000] new jobs last month. "
                        "America added [twenty-nine thousand.|29,000.]"),
    ("j2", "talk", "G", "That's from the official jobs report, out October second."),
    ("j3", "talk", "H", "Is that bad?"),
    ("j4", "talk", "G", "It's weak. Unemployment ticked up to [four point two percent.|4.2%.]"),
    ("j5", "talk", "G", "And earlier months were cut too. [Sixty thousand|60,000] fewer jobs than first reported."),
    ("j6", "talk", "H", "What about pay?"),
    ("j7", "talk", "G", "Wages grew [three percent|3%] in a year. The slowest since [twenty twenty-one.|2021.]"),
    ("j8", "talk", "H", "So where are the jobs?"),
    ("j9", "talk", "G", "Mostly health care. Plus some construction and factory work."),
    ("j10", "talk", "G", "Economists call it a low hire, low fire job market. Companies aren't firing much. "
                         "But they aren't hiring much either."),
    ("j11", "end", "H", "Is it harder to find a job where you live? Tell me in the comments."),
])

METADATA = dict(
    title="America Added Just 29,000 Jobs. Here's What That Means 💼",
    alt_titles=["Economists Expected 90,000 Jobs. We Got 29,000.", "The September Jobs Report, Explained"],
    description="""Economists expected about 90,000 new US jobs in September 2026. The official report (2 October) showed just 29,000. 💼

Unemployment ticked up to 4.2%, July and August were revised down by a combined 60,000 jobs, and wages grew 3% in a year, the slowest since 2021. Most new jobs were in health care, plus some construction and manufacturing. Economists call it a "low-hire, low-fire" job market: few layoffs, but little hiring.

Facts as of 5 October 2026.

💬 Is it harder to find a job where you live? 👇

Sources:
• U.S. Bureau of Labor Statistics, Employment Situation (2 Oct 2026): https://www.bls.gov/news.release/empsit.nr0.htm
• Al Jazeera (2 Oct 2026): https://www.aljazeera.com/economy/2026/10/2/us-job-growth-slows-as-unemployment-rises-before-midterm-elections
• Yahoo Finance (2 Oct 2026): https://finance.yahoo.com/economy/article/septembers-jobs-report-shows-the-us-added-just-29000-jobs-and-unemployment-ticked-up-195320409.html
• CNBC (2 Oct 2026): https://www.cnbc.com/2026/10/02/jobs-report-september-2026.html
• CNN (2 Oct 2026): https://www.cnn.com/2026/10/02/economy/us-jobs-report-september-final""",
    hashtags=["#Jobs", "#Economy", "#News"],
    tags=["jobs report", "unemployment", "us economy", "september jobs report", "job market", "wages", "hiring",
          "economy news", "news explained", "bls"],
    pinned_comment="Is it harder to find a job where you live right now? Yes or no? 👇",
)


def scene_talk(cr, t, tl):
    A = tl.at
    background(cr, t, cam_keys(tl))
    host(cr, t, tl, **mood(t, tl, [("j3", dict(eyes="sad", mouth="flat")), ("j4", {}),
                                    ("j6", dict(eyes="dot", mouth="flat", arms=("chin", "hip"))), ("j7", {}),
                                    ("j8", dict(eyes="wide", mouth="o", arms=("cheer", "hip")))], {}))
    eyes, idle = mood(t, tl, [("j4", ("sad", "flat")), ("j9", ("dot", "smile")), ("j10", ("sly", "flat"))],
                      ("dot", "flat"))
    talking_globe(cr, t, tl, CODE, eyes, idle)

    cr.identity_matrix()
    hl(cr, t, [("US ", NAVY), ("JOBS", RED), (" report", INK)], 215, 56, 0.0, bold=True, sound=False)
    date_stamp(cr, t, A("j2", "October"), "2 OCT 2026", x=585, y=118)

    def chart(c):
        items = [("expected", 90, hexc("#a9adb5"), "90K")]
        if t >= A("j1", "America"):
            items.append(("actual", 29, RED, "29K"))
        bars(c, 0, 10, items, u=1.0, s=1.0, top=110)
    panel(cr, t, 0.15, A("j3"), 360, 400, 420, 260, chart, seed=10000)
    source_tag(cr, t, A("j2", "official"), "U.S. Bureau of Labor Statistics", end=A("j3"))

    panel(cr, t, A("j4", "Unemployment"), A("j5"), 360, 400, 360, 240,
          lambda c: gauge(c, 0, -20, "4.2%", u=seg(t, A("j4", "Unemployment"), A("j4", "Unemployment") + 0.8)),
          seed=10010)
    if A("j5", "60,000") <= t < A("j6"):
        stamp(cr, t, A("j5", "60,000"), "-60,000 jobs", dur=A("j6") - A("j5", "60,000"), y=440)

    def pay(c):
        wallet(c, -110, 0, 1.0)
        write(c, [("+3%", GREEN)], 100, 0, 60, align="center", bold=True)
        if t >= A("j7", "slowest"):
            write(c, [("slowest since 2021", RED)], 100, 50, 26, align="center", bold=True)
    panel(cr, t, A("j7", "Wages"), A("j8"), 360, 400, 480, 220, pay, seed=10020)

    def where(c):
        job_icon(c, "health", -170, -10, 1.2)
        write(c, [("health care", INK)], -170, 70, 24, align="center", bold=True)
        if t >= A("j9", "construction"):
            job_icon(c, "build", 0, -10, 1.1)
            write(c, [("construction", INK)], 0, 70, 24, align="center", bold=True)
        if t >= A("j9", "factory"):
            job_icon(c, "factory", 170, -10, 1.0)
            write(c, [("factories", INK)], 170, 70, 24, align="center", bold=True)
    panel(cr, t, A("j9", "health"), A("j10"), 360, 400, 560, 210, where, seed=10030)

    def lowhire(c):
        door(c, -150, 0, open_=0.25 + 0.1 * ease_out(seg(t, A("j10", "hiring"), A("j10", "hiring") + 0.5)), s=0.9)
        write(c, [("low hire,", RED)], 60, -16, 40, align="center", bold=True)
        write(c, [("low fire", NAVY)], 60, 32, 40, align="center", bold=True)
    panel(cr, t, A("j10", "low"), A("j11") + 0.1, 360, 400, 480, 240, lowhire, seed=10040)


def scene_end(cr, t, tl):
    end_scene(cr, t, tl, CODE, "j11", [("harder to find a ", INK), ("JOB", RED), ("?", INK)],
              prop=lambda c: door(c, 0, 0, open_=0.2, s=0.8))


draw = make_draw({"talk": scene_talk, "end": scene_end})
