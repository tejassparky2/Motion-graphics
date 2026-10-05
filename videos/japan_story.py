"""Japan's permanent residency fee went up twenty times (1 Oct 2026), story style with our own cast.

Facts, as of 5 October 2026:
- From 1 Oct 2026 the permanent residence permission fee is 200,000 yen (was 10,000 yen). Immigration Services Agency
  of Japan https://www.moj.go.jp/isa/01_00644.html ; Japan Times, 1 Oct 2026
  https://www.japantimes.co.jp/news/2026/10/01/japan/permanent-residency-guidelines-revision/ ; SBS, 1 Oct 2026
  https://news.sbs.co.kr/english/article.do?news_id=N1008779480
- Dollars: USD/JPY about 157.8 on 2 Oct 2026, so 10,000 yen is about $63 and 200,000 yen about $1,270.
  Trading Economics https://tradingeconomics.com/japan/currency ; Bank of Japan
  https://www.boj.or.jp/en/statistics/market/forex/fxdaily/index.htm
- Permanent residency: no time limit on your stay; not citizenship, no Japanese passport. Immigration Services Agency
  https://www.moj.go.jp/isa/applications/procedures/16-4.html
- Record 4.12 million foreign residents at the end of 2025. Japan Times
  https://www.japantimes.co.jp/news/2026/03/28/japan/society/japan-foreign-resident-population-record/
- The agency says the fees reflect the real cost of processing and fees in other countries. SBS (above); The Standard HK
  https://www.thestandard.com.hk/world/article/344384/Japan-raises-permanent-residency-fee-by-20-times
- Higher income bar from October 2026. Nikkei Asia
  https://asia.nikkei.com/spotlight/japan-immigration/japan-plans-to-tighten-permanent-residency-requirements-for-foreigners ;
  Tokyo Weekender https://www.tokyoweekender.com/japan-life/news-and-opinion/permanent-residency-rules-explained-2026/
"""
from motion.captions import captions
from motion.engine import INK, RED, WHITE, at, blob, ease_out, hexc, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from motion.news import big_x, crowd, passport, price_tag, source_tag
from motion.newsbrand import badge
from motion.story import buttons
from motion.storykit import (GREEN, NAVY, actor, building, comment_prompt, focus, news_pacing, podium, reveal_gaps,
                             sign, sky_ground)

news_pacing()

NARRATOR = dict(speed=0.95)
TAIL = 0.3
# news bed (motion/newsmusic.py); the drop is a beat of silence before the new fee: 200,000 yen
MUSIC = dict(mood="money", drops=['j3'])

SCRIPT = [   # v3, approved by the owner 5 Oct 2026 (research_notes/news_scripts_v3.md)
    dict(id="j1", scene="office", text="Japan just made staying in the country for good twenty times more expensive."),
    dict(id="j2", scene="office", text="On October first, the fee for permanent residency jumped from "
                                       "[ten thousand|10,000] yen to [two hundred thousand|200,000] yen."),
    dict(id="j3", scene="office", text="That is a jump from about sixty-three dollars to about twelve hundred and "
                                       "seventy dollars."),
    dict(id="j3b", scene="meaning", text="So if you ever dreamed of moving to Japan, here is what you need to know."),
    dict(id="j5", scene="meaning", text="Permanent residency lets a foreigner stay in Japan with no time limit."),
    dict(id="j6", scene="meaning", text="But it does not make them a citizen, and it does not come with a Japanese "
                                        "passport."),
    dict(id="j7", scene="count", text="Japan now has more than four million foreign residents, which is a record."),
    dict(id="j7b", scene="why", text="So why did Japan raise the fee so much?"),
    dict(id="j8", scene="why", text="The government says the new fee covers the real cost of handling applications."),
    dict(id="j9", scene="why", text="It also says the fee is now closer to what other countries charge."),
    dict(id="j9b", scene="why", text="And there is one more change."),
    dict(id="j10", scene="why", text="Applicants now also need a higher income to qualify."),
    dict(id="j11", scene="end", text="Would you pay twelve hundred dollars to live in Japan for good?"),
]
reveal_gaps(SCRIPT, MUSIC)

METADATA = dict(
    title="Japan Just Made Permanent Residency 20x More Expensive 🇯🇵",
    alt_titles=["Living in Japan for Good Just Got 20 Times Pricier 😳", "Japan's New ¥200,000 Residency Fee, Explained"],
    description="""Since 1 October 2026, applying for permanent residency in Japan costs ¥200,000 instead of ¥10,000. That's about $1,270 instead of $63 (at about 157.8 yen per dollar, 2 Oct 2026). 🇯🇵

Permanent residency lets a foreigner stay in Japan with no time limit, but it isn't citizenship and doesn't come with a Japanese passport. Japan had a record 4.12 million foreign residents at the end of 2025. The Immigration Services Agency says the new fees reflect the real cost of processing applications and are closer to fees in other countries. A higher income bar also applies from October 2026.

Facts as of 5 October 2026.

💬 Would you pay it? 👇

Sources:
• Immigration Services Agency of Japan (fee revision, 1 Oct 2026): https://www.moj.go.jp/isa/01_00644.html
• The Japan Times (1 Oct 2026): https://www.japantimes.co.jp/news/2026/10/01/japan/permanent-residency-guidelines-revision/
• SBS News (1 Oct 2026): https://news.sbs.co.kr/english/article.do?news_id=N1008779480
• The Standard HK: https://www.thestandard.com.hk/world/article/344384/Japan-raises-permanent-residency-fee-by-20-times
• The Japan Times, record 4.12 million foreign residents (28 Mar 2026): https://www.japantimes.co.jp/news/2026/03/28/japan/society/japan-foreign-resident-population-record/
• Nikkei Asia, income requirement: https://asia.nikkei.com/spotlight/japan-immigration/japan-plans-to-tighten-permanent-residency-requirements-for-foreigners
• Bank of Japan exchange rates: https://www.boj.or.jp/en/statistics/market/forex/fxdaily/index.htm""",
    hashtags=["#Japan", "#News", "#Shorts"],
    tags=["japan", "japan permanent residency", "japan news", "permanent residency fee", "living in japan",
          "japan immigration", "moving to japan", "world news", "news explained", "japan visa"],
    pinned_comment="Would you pay ¥200,000 (about $1,270) for permanent residency in Japan? Yes or no? 👇",
)

JP_RED = hexc("#bc002d")


def flag_pole(cr, x, seed=22000):
    """A plain white flag with a red disc on a pole."""
    line(cr, [(x, 900), (x, 470)], 8, hexc("#8f939b"), seed, amp=0.1)
    shape(cr, rrect_pts(x + 4, 476, 150, 100, 4, 10), WHITE, seed=seed + 1, amp=0.4, lw=4)
    blob(cr, x + 79, 526, 28, 28, JP_RED, seed + 2, amp=0.2, lw=0, stroke=None)


def suitcase(cr, x, y, s=1.0, seed=22010):
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-34, -60, 68, 90, 8, 12), hexc("#e8743b"), seed=seed, amp=0.3, lw=4)
        line(cr, [(-14, -60), (-14, -76), (14, -76), (14, -60)], 5, INK, seed + 1, amp=0.1)


def traveller(cr, x, t, **kw):
    actor(cr, "jobseeker", x, t, **kw)
    suitcase(cr, x + 70, 900, 1.0)


def scene_office(cr, t, tl):
    A = tl.at
    keys = [(0, focus(300, 1.7)), (A("j1", "twenty"), (1.2, 640, 700)), (A("j2"), (1.2, 640, 700)),
            (A("j2", "10,000"), (1.3, 560, 680)), (A("j2", "200,000"), (1.1, 640, 690)), (A("j3"), (1.0, 640, 720))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    sky_ground(cr)
    building(cr, 640, 460, 470, hexc("#f1ede4"), "IMMIGRATION OFFICE", seed=22020)
    flag_pole(cr, 960)
    traveller(cr, 300, t, facing=1, arms=("wave", "hold") if t < A("j1", "twenty") else ("hold", "hip"),
              eyes="happy" if t < A("j1", "twenty") else "wide", mouth="smile" if t < A("j1", "twenty") else "o")
    if A("j2", "October") <= t < A("j2", "10,000"):
        sign(cr, 640, 360, "since 1 OCT 2026", RED, start=A("j2", "October"), t=t, seed=22030)
    if A("j1", "twenty") <= t < A("j2", "October"):
        with at(cr, 640, 560, pop(t, A("j1", "twenty"), 0.25) or 0.01):
            blob(cr, 0, 0, 110, 110, hexc("#ffd23f"), 22040, amp=0.6, lw=5)
            write(cr, [("20x", RED)], 0, 26, 90, align="center", bold=True)
    if t >= A("j2", "10,000"):
        old = min(1.0, seg(t, A("j2", "200,000"), A("j2", "200,000") + 0.5)) if t >= A("j2", "200,000") else 0.0
        with at(cr, 520, 560, pop(t, A("j2", "10,000"), 0.2) or 0.01):
            price_tag(cr, 0, 0, "¥10,000", "about $63", s=0.9, crossed=old)
    if t >= A("j2", "200,000"):
        with at(cr, 760, 700, pop(t, A("j2", "200,000"), 0.2) or 0.01):
            price_tag(cr, 0, 0, "¥200,000", "about $1,270", col=RED, s=0.9, rot=0.04, seed=22050)
    hl(cr, t, [("staying in ", INK), ("JAPAN", JP_RED)], 215, 76, 0.05, end=A("j1", "twenty") - 0.05, bold=True)
    hl(cr, t, [("x20", RED), (" more expensive", INK)], 215, 66, A("j1", "twenty"), end=A("j2") - 0.05, bold=True)
    hl(cr, t, [("residency fee: ", INK), ("1 OCT", RED)], 215, 70, A("j2"), end=A("j2", "10,000") - 0.05, bold=True)
    hl(cr, t, [("¥10,000", GREEN), (" to ", INK), ("¥200,000", RED)], 215, 66, A("j2", "10,000"), end=A("j3") - 0.05,
       bold=True)
    hl(cr, t, [("$63", GREEN), (" to ", INK), ("$1,270", RED)], 215, 80, A("j3"), bold=True)
    if t >= A("j2"):
        source_tag(cr, t, A("j2"), "Immigration Services Agency of Japan", y=270)


def scene_meaning(cr, t, tl):
    A = tl.at
    keys = [(A("j3b") - 0.2, focus(360, 1.6)), (A("j5"), (1.1, 540, 780)), (A("j5", "limit"), (1.3, 500, 720)),
            (A("j6"), (1.3, 500, 720))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    sky_ground(cr)
    building(cr, 700, 300, 380, hexc("#f7d9a8"), "HOME", seed=22100)
    flag_pole(cr, 900, seed=22110)
    traveller(cr, 360, t, facing=1, arms=("cheer", "hip") if t < A("j6") else ("hold", "hip"),
              eyes="happy" if t < A("j6") else "open", mouth="grin" if t < A("j6") else "flat")
    if A("j5", "limit") <= t < A("j6"):
        sign(cr, 560, 520, "no time limit", GREEN, start=A("j5", "limit"), t=t, seed=22120)
    if t >= A("j6", "citizen"):
        sign(cr, 560, 520, "NOT a citizen", RED, start=A("j6", "citizen"), t=t, seed=22130)
    if t >= A("j6", "passport"):
        with at(cr, 560, 700, pop(t, A("j6", "passport"), 0.2) or 0.01):
            passport(cr, 0, 0, 1.0)
            big_x(cr, 0, 0, 70, seg(t, A("j6", "passport") + 0.2, A("j6", "passport") + 0.6))
    hl(cr, t, [("dream of ", INK), ("JAPAN?", JP_RED)], 215, 76, A("j3b"), end=A("j5") - 0.05, bold=True)
    hl(cr, t, [("permanent ", INK), ("RESIDENCY", NAVY)], 215, 66, A("j5"), end=A("j6") - 0.05, bold=True)
    hl(cr, t, [("NOT ", RED), ("citizenship", INK)], 215, 74, A("j6"), bold=True)


def scene_count(cr, t, tl):
    A = tl.at
    set_camera(camera(t, [(A("j7") - 0.2, (1.0, 640, 780)), (A("j7", "record"), (1.2, 640, 700))], dur=0.14))
    enter_world(cr)
    sky_ground(cr)
    u = ease_out(seg(t, A("j7"), A("j7", "four") + 1.2))
    with at(cr, 640, 600, 1.0):
        shape(cr, rrect_pts(-300, -170, 600, 340, 14, 14), WHITE, seed=22200, amp=0.4, lw=5)
        crowd(cr, 0, -70, t, 120, cols=20, gap=26, progress=u)
        write(cr, [(f"{4.12 * u:.2f} million", NAVY)], 0, 140, 50, align="center", bold=True)
    if t >= A("j7", "record"):
        stamp(cr, t, A("j7", "record"), "RECORD", dur=1.2, y=430)
    hl(cr, t, [("4 million+ ", NAVY), ("foreigners", INK)], 215, 66, A("j7"), bold=True)
    source_tag(cr, t, A("j7"), "Immigration Services Agency, end of 2025", y=270)


def scene_why(cr, t, tl):
    A = tl.at
    keys = [(A("j7b") - 0.2, focus(420, 1.6)), (A("j8", "cost"), (1.2, 620, 720)), (A("j9"), (1.2, 620, 720)),
            (A("j9b"), focus(420, 1.6)), (A("j10"), (1.1, 800, 760)), (A("j10", "income"), (1.3, 900, 700))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    sky_ground(cr, ground=hexc("#c9c4b8"))
    actor(cr, "official_4", 420, t, facing=1, arms=("point", "hip"), eyes="open", mouth="talk")
    podium(cr, 420, "IMMIGRATION", NAVY, seed=22300)
    if A("j8", "cost") <= t < A("j9"):
        with at(cr, 760, 560, pop(t, A("j8", "cost"), 0.2) or 0.01):
            for k in range(5):   # a stack of application forms
                shape(cr, rrect_pts(-90 + k * 6, -110 + k * 14, 180, 120, 6, 10), WHITE, seed=22310 + k, amp=0.4,
                      lw=4)
            write(cr, [("FORMS", INK)], 12, 60, 34, align="center", bold=True)
    if A("j9", "countries") <= t < A("j9b"):
        with at(cr, 760, 560, pop(t, A("j9", "countries"), 0.2) or 0.01):
            for k, (lab, h) in enumerate([("JAPAN", 150), ("OTHERS", 170)]):
                shape(cr, rrect_pts(-110 + k * 140, 80 - h, 90, h, 6, 10), JP_RED if k == 0 else hexc("#8a63d2"),
                      seed=22330 + k, amp=0.3, lw=4)
                write(cr, [(lab, INK)], -65 + k * 140, 112, 26, align="center", bold=True)
    if t >= A("j10"):
        u = ease_out(seg(t, A("j10", "higher"), A("j10", "higher") + 0.8))
        with at(cr, 900, 640, 1.0):
            line(cr, [(-140, 120), (140, 120)], 6, INK, 22340, amp=0.2)
            shape(cr, rrect_pts(-60, 120 - 80 - 140 * u, 120, 80 + 140 * u, 6, 10), GREEN, seed=22341, amp=0.3, lw=4)
            write(cr, [("income needed", INK)], 0, 160, 32, align="center", bold=True)
            line(cr, [(90, 60), (90, -60 - 60 * u)], 8, RED, 22342, amp=0.2)
            line(cr, [(70, -40 - 60 * u), (90, -64 - 60 * u), (110, -40 - 60 * u)], 8, RED, 22343, amp=0.2)
    hl(cr, t, [("why ", INK), ("x20", RED), ("?", INK)], 215, 84, A("j7b"), end=A("j8") - 0.05, bold=True)
    hl(cr, t, [("the ", INK), ("REAL COST", RED)], 215, 74, A("j8"), end=A("j9") - 0.05, bold=True)
    hl(cr, t, [("like ", INK), ("other countries", NAVY)], 215, 70, A("j9"), end=A("j9b") - 0.05, bold=True)
    hl(cr, t, [("one more ", INK), ("CHANGE", RED)], 215, 74, A("j9b"), end=A("j10") - 0.05, bold=True)
    hl(cr, t, [("higher ", RED), ("income", INK), (" needed", INK)], 215, 66, A("j10"), bold=True)
    if A("j10") <= t:
        source_tag(cr, t, A("j10"), "Nikkei Asia", y=270)
    elif t >= A("j7b"):
        source_tag(cr, t, A("j7b"), "SBS; The Standard HK, 1 Oct 2026", y=270)


def scene_end(cr, t, tl):
    A = tl.at
    set_camera(camera(t, [(A("j11") - 0.2, focus(360, 1.5, screen=640))], dur=0.14))
    enter_world(cr)
    sky_ground(cr)
    flag_pole(cr, 620, seed=22400)
    traveller(cr, 300, t, facing=1, arms=("point", "hip"), eyes="open", mouth="talk")
    hl(cr, t, [("would you pay ", INK), ("$1,270", RED), ("?", INK)], 215, 66, A("j11"), bold=True, underline=True)
    cr.identity_matrix()
    buttons(cr, t, A("j11") + 0.3, (("YES", GREEN), ("NO", RED)), y=330, s=0.85)
    comment_prompt(cr, t, A("j11") + 0.6)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"office": scene_office, "meaning": scene_meaning, "count": scene_count, "why": scene_why,
     "end": scene_end}[name](cr, t, tl)
    cr.restore()
    badge(cr, t, "WORLD", "5 OCT 2026")
    captions(cr, t, tl)
