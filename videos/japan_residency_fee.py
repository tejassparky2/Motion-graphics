"""News: Japan's permanent residency fee went up twenty times (1 October 2026).

Format: our host talks with the Globe (our recurring character, painted in the country's flag colours), one fact per
line. Script and drawings are our own.

Facts, as of 4 October 2026:
- From 1 Oct 2026 the permanent residence permission fee is 200,000 yen (was 10,000 yen) for applications filed on or
  after that date. Immigration Services Agency of Japan (Ministry of Justice):
  https://www.moj.go.jp/isa/01_00644.html ; https://www.moj.go.jp/isa/content/001469200.pdf
  Japan Times, 1 Oct 2026: https://www.japantimes.co.jp/news/2026/10/01/japan/permanent-residency-guidelines-revision/
  SBS (Korea), 1 Oct 2026: https://news.sbs.co.kr/english/article.do?news_id=N1008779480
- Dollars: USD/JPY about 157.8 on 2 Oct 2026, so 10,000 yen is about $63 and 200,000 yen about $1,270.
  Trading Economics https://tradingeconomics.com/japan/currency ; Bank of Japan daily rates
  https://www.boj.or.jp/en/statistics/market/forex/fxdaily/index.htm
- Record 4.12 million foreign residents at the end of 2025, first time above 4 million (Immigration Services Agency,
  27 Mar 2026). Japan Times https://www.japantimes.co.jp/news/2026/03/28/japan/society/japan-foreign-resident-population-record/
  Wikipedia summary https://en.wikipedia.org/wiki/Immigration_to_Japan
- The agency says the new fees take into account the real cost of processing applications, wider immigration costs and
  similar fees in other countries. SBS (above); The Standard HK
  https://www.thestandard.com.hk/world/article/344384/Japan-raises-permanent-residency-fee-by-20-times
- Permanent residency lets you live in Japan with no time limit; it is not citizenship (no Japanese passport).
  Immigration Services Agency https://www.moj.go.jp/isa/applications/procedures/16-4.html
- A higher income bar for permanent residency from October 2026. Nikkei Asia
  https://asia.nikkei.com/spotlight/japan-immigration/japan-plans-to-tighten-permanent-residency-requirements-for-foreigners ;
  Tokyo Weekender https://www.tokyoweekender.com/japan-life/news-and-opinion/permanent-residency-rules-explained-2026/
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import INK, RED, WHITE, at, blob, ease_out, hexc, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, hl, stamp, whip
from motion.news import (GREEN, JP_RED, PAPER, SKY, big_x, crowd, date_stamp, dinner, globe, panel, passport,
                         phone, price_tag, source_tag, tick)
from motion.story import buttons

NARRATOR = dict(speed=1.0)
TAIL = 0.9

H, J = "reporter", "globe"
SCRIPT = [
    dict(id="n1", scene="talk", text="Want to live in Japan for good? It just got a lot more expensive.", speaker=H),
    dict(id="n2", scene="talk", text="It did. Since October first, permanent residency in Japan costs twenty times more.",
         speaker=J),
    dict(id="n3", scene="talk", text="Twenty times? What did it cost before?", speaker=H),
    dict(id="n4", scene="talk", text="[Ten thousand yen.|10,000 yen.] That's about [sixty-three dollars.|$63.]",
         speaker=J),
    dict(id="n5", scene="talk", text="And now?", speaker=H),
    dict(id="n6", scene="talk",
         text="[Two hundred thousand yen.|200,000 yen.] About [twelve hundred and seventy dollars.|$1,270.]",
         speaker=J),
    dict(id="n7", scene="talk", text="So it went from the price of a nice dinner. To the price of a new phone.",
         speaker=H),
    dict(id="n8", scene="talk", text="Pretty much.", speaker=J),
    dict(id="n9", scene="talk", text="But why so much more?", speaker=H),
    dict(id="n10", scene="talk",
         text="More than four million foreign residents live in Japan now. That's a record.", speaker=J),
    dict(id="n11", scene="talk",
         text="The government says the new fee covers the real cost of handling applications. "
              "And it's closer to what other countries charge.", speaker=J),
    dict(id="n12", scene="talk", text="So if I pay, do I get a Japanese passport?", speaker=H),
    dict(id="n13", scene="talk", text="No. You can live there with no time limit. But you are not a citizen.",
         speaker=J),
    dict(id="n14", scene="talk", text="And you now need a higher income to qualify.", speaker=J),
    dict(id="n15", scene="talk", text="So it costs more. And it's harder to get.", speaker=H),
    dict(id="n16", scene="end",
         text="Would you pay [twelve hundred dollars|$1,200] to live in Japan? Tell me in the comments.", speaker=H),
]
for _i, _s in enumerate(SCRIPT):   # a clear pause whenever the other one starts talking
    if _i and _s["speaker"] != SCRIPT[_i - 1]["speaker"]:
        _s["gap"] = 0.36

METADATA = dict(
    title="Japan Just Made Permanent Residency 20x More Expensive 🇯🇵",
    alt_titles=["Living in Japan Just Got 20 Times Pricier 😳", "Japan's New ¥200,000 Residency Fee, Explained"],
    description="""Since 1 October 2026, applying for permanent residency in Japan costs ¥200,000 instead of ¥10,000. That's about $1,270 instead of $63 (at about 157.8 yen per dollar, 2 Oct 2026). 🇯🇵

Japan had a record 4.12 million foreign residents at the end of 2025. The Immigration Services Agency says the new fees reflect the real cost of processing applications and fees in other countries. Permanent residency lets you live in Japan with no time limit, but it isn't citizenship. A higher income bar also applies from October 2026.

Facts as of 4 October 2026.

💬 Would you pay it? 👇

Sources:
• Immigration Services Agency of Japan (fee revision, 1 Oct 2026): https://www.moj.go.jp/isa/01_00644.html
• The Japan Times (1 Oct 2026): https://www.japantimes.co.jp/news/2026/10/01/japan/permanent-residency-guidelines-revision/
• SBS News (1 Oct 2026): https://news.sbs.co.kr/english/article.do?news_id=N1008779480
• The Japan Times, record 4.12 million foreign residents (28 Mar 2026): https://www.japantimes.co.jp/news/2026/03/28/japan/society/japan-foreign-resident-population-record/
• Nikkei Asia, income requirement: https://asia.nikkei.com/spotlight/japan-immigration/japan-plans-to-tighten-permanent-residency-requirements-for-foreigners
• Bank of Japan exchange rates: https://www.boj.or.jp/en/statistics/market/forex/fxdaily/index.htm""",
    hashtags=["#Japan", "#News", "#Shorts"],
    tags=["japan", "japan permanent residency", "japan news", "permanent residency fee", "living in japan",
          "japan immigration", "moving to japan", "world news", "news explained", "japan visa"],
    pinned_comment="Would you pay ¥200,000 (about $1,270) for permanent residency in Japan? Yes or no? 👇",
)

HOST_X, GLOBE_X, GROUND = 170, 530, 960
TWO = (1.0, 360, 720)
HOST_CLOSE = (1.75, 190, 770)
GLOBE_CLOSE = (1.35, 530, 668)


def _bg(cr, t, keys):
    cr.set_source_rgba(*SKY)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=0.22)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    # faint globe lines behind, then the floor
    for k in range(5):
        blob(cr, 360, 560, 520 - k * 110, 330, None, 8000 + k, amp=0.6, lw=2.5, stroke=hexc("#ffffff", 0.55))
    for k in range(-2, 3):
        line(cr, [(-200, 560 + k * 120), (920, 560 + k * 120)], 2.5, hexc("#ffffff", 0.45), 8010 + k, amp=0.8)
    shape(cr, [(-700, GROUND), (1500, GROUND), (1500, 2600), (-700, 2600)], PAPER, seed=8020, amp=0.5, lw=4)


def _cam_keys(tl):
    keys = [(0, TWO)]
    for b in tl.beats:
        if b.scene != "talk":
            continue
        keys.append((b.start - 0.05, HOST_CLOSE if b.speaker == H else GLOBE_CLOSE))
    A = tl.at
    keys += [(A("n7", "dinner"), (1.4, 300, 740)), (A("n10", "four"), (1.3, 470, 700)),
             (A("n15"), TWO)]
    return keys


def _japan(cr, t, tl, eyes="dot", idle="smile"):
    talking = tl.speaking(J, t)
    mouth = ("o" if int(t * 12) % 2 else idle) if talking else idle
    globe(cr, "jp", GLOBE_X, GROUND, t, eyes=eyes, mouth=mouth, look=-1,
            bounce=abs(math.sin(t * 9)) * 3 if talking else 0)


def _host(cr, t, tl, **kw):
    talking = tl.speaking(H, t)
    k = dict(facing=1, arms=("hip", "hip"), eyes="dot", mouth="smile")
    k.update(kw)
    if talking:
        k["mouth"] = "o" if int(t * 12) % 2 else k["mouth"]
    person(cr, H, HOST_X, GROUND, t, **k)


def scene_talk(cr, t, tl):
    A = tl.at
    _bg(cr, t, _cam_keys(tl))
    # ---- host reactions
    h = {}
    if A("n3") <= t < A("n4"):
        h = dict(eyes="wide", mouth="o", arms=("cheer", "hip"))
    elif A("n5") <= t < A("n7"):
        h = dict(eyes="wide", mouth="o", sweat=t >= A("n6", "two"))
    elif A("n7") <= t < A("n8"):
        h = dict(eyes="sly", mouth="smirk", arms=("point", "hip"))
    elif A("n9") <= t < A("n10"):
        h = dict(eyes="dot", mouth="flat", arms=("chin", "hip"))
    elif A("n12") <= t < A("n13"):
        h = dict(eyes="happy", mouth="grin", arms=("thumb", "hip"))
    elif A("n13") <= t < A("n15"):
        h = dict(eyes="sad", mouth="flat")
    elif t >= A("n15"):
        h = dict(eyes="sly", mouth="flat", arms=("chin", "hip"))
    _host(cr, t, tl, **h)
    # ---- Japan's face
    if t < A("n3"):
        _japan(cr, t, tl, "dot", "smile")
    elif t < A("n7"):
        _japan(cr, t, tl, "sly", "smirk")
    elif t < A("n9"):
        _japan(cr, t, tl, "happy", "smile")
    elif t < A("n12"):
        _japan(cr, t, tl, "dot", "flat")
    elif t < A("n14"):
        _japan(cr, t, tl, "sly", "smirk")
    else:
        _japan(cr, t, tl, "dot", "smile")

    # ---- screen-space overlays
    cr.identity_matrix()
    hl(cr, t, [("JAPAN ", JP_RED), ("permanent residency", INK)], 215, 46, 0.0, bold=True, sound=False)
    date_stamp(cr, t, A("n2", "October"), "1 OCT 2026", x=585, y=118)
    if A("n2", "twenty") <= t < A("n3"):
        stamp(cr, t, A("n2", "twenty"), "x20", dur=A("n3") - A("n2", "twenty"), y=440)

    def old_tag(c):
        price_tag(c, 0, 0, "¥10,000", "about $63", col=GREEN, crossed=ease_out(seg(t, A("n6"), A("n6") + 0.3)))
    panel(cr, t, A("n4", "ten"), A("n6", "two") + 0.45, 360, 420, 360, 200, old_tag, seed=8100)

    def new_tag(c):
        price_tag(c, 0, 0, "¥200,000", "about $1,270", col=JP_RED, s=1.05, seed=8150)
    panel(cr, t, A("n6", "two") + 0.45, A("n7", "dinner"), 360, 420, 380, 210, new_tag, seed=8160, fill=hexc("#fde7e3"))

    def compare(c):
        dinner(c, -140, 10, 0.95)
        write(c, [("$63", GREEN)], -140, 104, 40, align="center", bold=True)
        if t >= A("n7", "phone"):
            phone(c, 140, -8, 0.9, seed=8210)
            write(c, [("$1,270", JP_RED)], 140, 104, 40, align="center", bold=True)
        write(c, [("then", INK)], -140, -96, 30, align="center", bold=True)
        write(c, [("now", INK)], 140, -112, 30, align="center", bold=True)
    panel(cr, t, A("n7", "dinner"), A("n8", end=True) + 0.2, 360, 410, 560, 270, compare, seed=8200)

    def residents(c):
        crowd(c, 0, -18, t, 60, cols=15, gap=26, progress=ease_out(seg(t, A("n10", "four"), A("n10", "four") + 1.0)))
        write(c, [("4.12 MILLION", JP_RED)], 0, 92, 46, align="center", bold=True)
        write(c, [("foreign residents, end of 2025", INK)], 0, -96, 24, align="center", bold=True)
    panel(cr, t, A("n10", "four"), A("n11"), 360, 420, 520, 260, residents, seed=8300)
    source_tag(cr, t, A("n10", "four"), "Immigration Services Agency of Japan", end=A("n11"))

    def reasons(c):
        write(c, [("why the new fee?", INK)], 0, -76, 32, align="center", bold=True)
        tick(c, -200, -20, 16, seed=8410)
        write(c, [("real cost of handling", INK)], -170, -10, 30, bold=True)
        write(c, [("applications", INK)], -170, 26, 30, bold=True)
        if t >= A("n11", "closer"):
            tick(c, -200, 70, 16, seed=8420)
            write(c, [("closer to other countries", INK)], -170, 80, 30, bold=True)
    panel(cr, t, A("n11", "cost"), A("n12"), 360, 420, 520, 230, reasons, seed=8400)
    source_tag(cr, t, A("n11", "government"), "Immigration Services Agency (2026)", end=A("n12"))

    def pp(c):
        passport(c, 0, 0, 1.0)
        if t >= A("n13", "no"):
            big_x(c, 0, 0, 72, seg(t, A("n13", "no"), A("n13", "no") + 0.3))
    panel(cr, t, A("n12", "passport"), A("n13", "live"), 360, 420, 260, 240, pp, seed=8500)

    def status(c):
        tick(c, -190, -40, 18, seed=8610)
        write(c, [("live here, no time limit", INK)], -160, -28, 32, bold=True)
        if t >= A("n13", "citizen"):
            big_x(c, -190, 40, 18, 1.0, seed=8620)
            write(c, [("not a citizen", JP_RED)], -160, 52, 32, bold=True)
    panel(cr, t, A("n13", "live"), A("n14"), 360, 420, 520, 200, status, seed=8600)

    def income(c):
        u = ease_out(seg(t, A("n14", "higher"), A("n14", "higher") + 0.6))
        for k, (hgt, col) in enumerate(((60, hexc("#a9a2ae")), (60 + 70 * u, GREEN))):
            x0 = -90 + k * 120
            shape(c, rrect_pts(x0, 70 - hgt, 70, hgt, 6, 12), col, seed=8700 + k, amp=0.4, lw=3.5)
        line(c, [(-130, 70), (150, 70)], 4, INK, 8710, amp=0.3)
        write(c, [("before", INK)], -55, 104, 24, align="center", bold=True)
        write(c, [("now", INK)], 65, 104, 24, align="center", bold=True)
        write(c, [("income needed", INK)], 0, -94, 32, align="center", bold=True)
    panel(cr, t, A("n14", "higher"), A("n15"), 360, 410, 420, 260, income, seed=8720)

    def summary(c):
        write(c, [("costs ", INK), ("20x", JP_RED), (" more", INK)], 0, -26, 44, align="center", bold=True)
        if t >= A("n15", "harder"):
            write(c, [("harder", JP_RED), (" to get", INK)], 0, 44, 44, align="center", bold=True)
    panel(cr, t, A("n15", "costs"), A("n15", end=True) + 0.4, 360, 410, 460, 190, summary, seed=8800)


def scene_end(cr, t, tl):
    A = tl.at
    _bg(cr, t, [(A("n16") - 0.4, (1.0, 360, 715))])
    _host(cr, t, tl, arms=("point", "hip"), eyes="happy")
    _japan(cr, t, tl, "wide", "smile")
    cr.identity_matrix()
    hl(cr, t, [("would you ", INK), ("PAY", JP_RED), (" it?", INK)], 215, 66, A("n16"), bold=True, underline=True)

    def tag(c):
        price_tag(c, 0, 0, "¥200,000", "about $1,270", col=JP_RED, s=0.9, seed=8900)
    panel(cr, t, A("n16", "twelve"), 999, 360, 390, 340, 180, tag, seed=8910, fill=hexc("#fde7e3"))
    buttons(cr, t, A("n16", "comments"), (("YES", GREEN), ("NO", RED)), y=545, s=0.75)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"talk": scene_talk, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
