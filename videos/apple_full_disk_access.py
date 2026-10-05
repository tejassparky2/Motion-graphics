"""Tech news: Apple will make "Full Disk Access" on Macs harder to grant, because of AI agents (2 October 2026).

Format: our host talks with the Globe, here shaped and coloured like Apple's mark (our own drawing), "APPLE" on the
base. Script approved by the owner on 5 Oct 2026.

Facts, as of 5 October 2026:
- On 2 Oct 2026 Apple posted "Updates to Full Disk Access in macOS" on its developer news site. It said: "Some
  developers are using Full Disk Access in ways that could put users at risk, exposing everything on their systems,
  including files, mail, messages, and even browsing history, without users' full knowledge and understanding." As AI
  agents become "increasingly capable and autonomous", the risks grow; access will be grantable only through "very
  explicit user action". No date, macOS version or app named.
  TechCrunch https://techcrunch.com/2026/10/02/apple-says-its-tightening-macos-full-disk-access-controls-due-to-new-risks-from-ai-agents/
  MacRumors https://www.macrumors.com/2026/10/02/apple-announces-macos-full-disk-access-changes/
  Engadget https://www.engadget.com/2276186/apple-sounds-the-alarm-on-ai-agents-and-full-disk-access/
  gHacks https://www.ghacks.net/2026/10/05/apple-will-require-explicit-user-action-to-grant-full-disk-access-in-macos-citing-ai-agents/
- Desktop AI agent apps often ask users to grant Full Disk Access so they can read files and messages (TechCrunch).
"""
import math

from motion.captions import captions
from motion.characters import person
from motion.engine import INK, RED, WHITE, at, blob, dot, ease_out, hexc, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, hl, stamp, whip
from motion.news import GREEN, PAPER, SKY, date_stamp, globe, panel, source_tag, tick
from motion.story import buttons

NARRATOR = dict(speed=0.95)
TAIL = 0.9

H, G = "reporter", "globe"
SCRIPT = [
    dict(id="a1", scene="talk", text="Your Mac is about to get stricter. And it's because of AI.", speaker=H),
    dict(id="a2", scene="talk",
         text="On October second, Apple warned app makers about a setting called Full Disk Access.", speaker=G),
    dict(id="a3", scene="talk", text="What does that setting do?", speaker=H),
    dict(id="a4", scene="talk",
         text="It lets an app see almost everything on your Mac. Your files. Your email. Your messages. "
              "Even your browsing history.", speaker=G),
    dict(id="a5", scene="talk", text="And AI agents want that?", speaker=H),
    dict(id="a6", scene="talk",
         text="Many do. AI helpers that work in the background often ask for it, so they can read your stuff.",
         speaker=G),
    dict(id="a7", scene="talk",
         text="Apple says this could expose everything on your Mac without your full knowledge and understanding.",
         speaker=G),
    dict(id="a8", scene="talk", text="So what's changing?", speaker=H),
    dict(id="a9", scene="talk", text="Soon, you can only turn it on with a very explicit action.", speaker=G),
    dict(id="a10", scene="talk", text="So no more clicking yes without thinking.", speaker=H),
    dict(id="a11", scene="talk", text="That's the idea. But Apple hasn't said when. No date yet.", speaker=G),
    dict(id="a12", scene="end",
         text="Would you let an AI read everything on your computer? Tell me in the comments.", speaker=H),
]
GLOBE_VOICE = "bm_george"   # the globe's own Kokoro voice; the host keeps the channel narrator (am_fenrir)
for _i, _s in enumerate(SCRIPT):   # a clear pause whenever the other one starts talking
    if _i and _s["speaker"] != SCRIPT[_i - 1]["speaker"]:
        _s["gap"] = 0.36
    if _s["speaker"] == G:
        _s["voice"] = GLOBE_VOICE
        _s.setdefault("pace", 1.12)   # George reads slower than the host; match their pace

METADATA = dict(
    title="Apple Is Locking Down Your Mac Because of AI 🔒",
    alt_titles=["Your Mac Is About to Get Stricter (Because of AI Agents)",
                "Apple's New Warning About AI Apps on Your Mac"],
    description="""On 2 October 2026, Apple told developers it will add new controls to "Full Disk Access" on macOS, the setting that lets an app see almost everything on your Mac: files, mail, messages and browsing history. 🔒

Apple says some apps use it in ways that could expose everything "without users' full knowledge and understanding", and that the risk grows as AI agents become "increasingly capable and autonomous". Soon, the setting can only be turned on through "very explicit user action". Apple hasn't given a date or named any app.

Facts as of 5 October 2026.

💬 Would you let an AI read everything on your computer? 👇

Sources:
• Apple Developer News, "Updates to Full Disk Access in macOS" (2 Oct 2026)
• TechCrunch (2 Oct 2026): https://techcrunch.com/2026/10/02/apple-says-its-tightening-macos-full-disk-access-controls-due-to-new-risks-from-ai-agents/
• MacRumors (2 Oct 2026): https://www.macrumors.com/2026/10/02/apple-announces-macos-full-disk-access-changes/
• Engadget: https://www.engadget.com/2276186/apple-sounds-the-alarm-on-ai-agents-and-full-disk-access/

Not affiliated with or endorsed by Apple.""",
    hashtags=["#Apple", "#Mac", "#AI", "#TechNews"],
    tags=["apple", "mac", "macos", "full disk access", "ai agents", "apple news", "mac privacy", "tech news",
          "ai privacy", "news explained"],
    pinned_comment="Would you give an AI app access to everything on your computer? Yes or no? 👇",
)

HOST_X, GLOBE_X, GROUND = 170, 530, 960
TWO = (0.95, 360, 700)
HOST_CLOSE = (1.75, 190, 770)
GLOBE_CLOSE = (1.2, 530, 640)
GRAPHITE = hexc("#2b2d33")


def _bg(cr, t, keys):
    cr.set_source_rgba(*SKY)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=0.22)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    for k in range(5):
        blob(cr, 360, 560, 520 - k * 110, 330, None, 9000 + k, amp=0.6, lw=2.5, stroke=hexc("#ffffff", 0.55))
    for k in range(-2, 3):
        line(cr, [(-200, 560 + k * 120), (920, 560 + k * 120)], 2.5, hexc("#ffffff", 0.45), 9010 + k, amp=0.8)
    shape(cr, [(-700, GROUND), (1500, GROUND), (1500, 2600), (-700, 2600)], PAPER, seed=9020, amp=0.5, lw=4)


def _cam_keys(tl):
    keys = [(0, TWO)]
    for b in tl.beats:
        if b.scene == "talk":
            keys.append((b.start - 0.05, HOST_CLOSE if b.speaker == H else GLOBE_CLOSE))
    return keys


def _globe(cr, t, tl, eyes="dot", idle="smile"):
    talking = tl.speaking(G, t)
    mouth = ("o" if int(t * 12) % 2 else idle) if talking else idle
    globe(cr, "apple", GLOBE_X, GROUND, t, eyes=eyes, mouth=mouth, look=-1,
          bounce=abs(math.sin(t * 9)) * 3 if talking else 0)


def _host(cr, t, tl, **kw):
    k = dict(facing=1, arms=("hip", "hip"), eyes="dot", mouth="smile")
    k.update(kw)
    if tl.speaking(H, t):
        k["mouth"] = "o" if int(t * 12) % 2 else k["mouth"]
    person(cr, H, HOST_X, GROUND, t, **k)


# ---------------------------------------------------------------- props (drawn around (0, 0))
def laptop(c, x, y, s=1.0, lock=0.0, seed=9100):
    with at(c, x, y, s):
        shape(c, rrect_pts(-110, -90, 220, 140, 10, 14), hexc("#c9ccd2"), seed=seed, amp=0.4, lw=4)
        shape(c, rrect_pts(-96, -78, 192, 116, 6, 14), hexc("#7fc8e8"), seed=seed + 1, amp=0.3, lw=0, stroke=None)
        shape(c, [(-140, 50), (140, 50), (120, 72), (-120, 72)], hexc("#a9adb5"), seed=seed + 2, amp=0.4, lw=4)
        if lock > 0:
            with at(c, 0, -22, max(0.01, pop(lock, 0.0, 0.3))):
                blob(c, 0, -26, 22, 26, None, seed + 3, amp=0.3, lw=7, stroke=INK)
                shape(c, rrect_pts(-34, -14, 68, 56, 8, 12), hexc("#f2b632"), seed=seed + 4, amp=0.3, lw=4)
                dot(c, 0, 10, 6, INK)


def toggle(c, x, y, on=0.0, seed=9200):
    with at(c, x, y):
        col = hexc("#a9a2ae") if on < 0.5 else GREEN
        shape(c, rrect_pts(-46, -24, 92, 48, 24, 12), col, seed=seed, amp=0.3, lw=4)
        blob(c, -22 + 44 * ease_out(on), 0, 18, 18, WHITE, seed + 1, amp=0.3, lw=3.5)


def icon(c, kind, x, y, s=1.0, seed=9300):
    with at(c, x, y, s):
        if kind == "files":
            shape(c, [(-40, -22), (-12, -22), (-4, -30), (40, -30), (40, 30), (-40, 30)], hexc("#7fb3e8"),
                  seed=seed, amp=0.4, lw=4)
        elif kind == "mail":
            shape(c, rrect_pts(-42, -28, 84, 56, 6, 12), WHITE, seed=seed, amp=0.4, lw=4)
            line(c, [(-40, -24), (0, 6), (40, -24)], 4, INK, seed + 1, amp=0.3)
        elif kind == "messages":
            blob(c, 0, -4, 42, 30, GREEN, seed, amp=0.5, lw=4)
            shape(c, [(-24, 18), (-34, 36), (-6, 24)], GREEN, seed=seed + 1, amp=0.3, lw=0, stroke=None)
        elif kind == "history":
            blob(c, 0, 0, 34, 34, hexc("#7fc8e8"), seed, amp=0.4, lw=4)
            line(c, [(0, -34), (0, 34)], 3, INK, seed + 1, amp=0.3)
            blob(c, 0, 0, 14, 34, None, seed + 2, amp=0.3, lw=3)
            line(c, [(-34, 0), (34, 0)], 3, INK, seed + 3, amp=0.3)


def robot(c, x, y, s=1.0, t=0.0, seed=9400):
    with at(c, x, y, s):
        line(c, [(0, -70), (0, -88)], 4, INK, seed, amp=0.2)
        dot(c, 0, -92, 7, RED)
        shape(c, rrect_pts(-40, -70, 80, 58, 14, 12), hexc("#c9ccd2"), seed=seed + 1, amp=0.4, lw=4)
        for sx in (-1, 1):
            blob(c, sx * 16, -44, 9, 9, hexc("#7fc8e8"), seed + 2 + sx, amp=0.2, lw=3)
        shape(c, rrect_pts(-32, -8, 64, 56, 10, 12), hexc("#a9adb5"), seed=seed + 4, amp=0.4, lw=4)
        reach = 18 * math.sin(t * 6)
        line(c, [(32, 10), (70 + reach, -6)], 7, INK, seed + 5, amp=0.3)


def scene_talk(cr, t, tl):
    A = tl.at
    _bg(cr, t, _cam_keys(tl))
    h = {}
    if A("a3") <= t < A("a4"):
        h = dict(eyes="dot", mouth="flat", arms=("chin", "hip"))
    elif A("a5") <= t < A("a6"):
        h = dict(eyes="wide", mouth="o", arms=("cheer", "hip"))
    elif A("a7") <= t < A("a8"):
        h = dict(eyes="wide", mouth="o", sweat=True)
    elif A("a8") <= t < A("a9"):
        h = dict(eyes="dot", mouth="flat", arms=("chin", "hip"))
    elif A("a10") <= t:
        h = dict(eyes="happy", mouth="grin", arms=("thumb", "hip"))
    _host(cr, t, tl, **h)
    if t < A("a4"):
        _globe(cr, t, tl, "dot", "smile")
    elif t < A("a8"):
        _globe(cr, t, tl, "wide", "flat")
    elif t < A("a11"):
        _globe(cr, t, tl, "sly", "smirk")
    else:
        _globe(cr, t, tl, "dot", "flat")

    cr.identity_matrix()
    hl(cr, t, [("APPLE ", GRAPHITE), ("vs ", INK), ("AI agents", RED)], 215, 50, 0.0, bold=True, sound=False)
    date_stamp(cr, t, A("a2", "October"), "2 OCT 2026", x=585, y=118)

    def lock(c):
        laptop(c, 0, 0, 1.0, lock=t - A("a1", "stricter"))
    panel(cr, t, A("a1", "Mac"), A("a2"), 360, 400, 380, 240, lock, seed=9500)

    def fda(c):
        write(c, [("Full Disk Access", INK)], -40, 10, 40, align="center", bold=True)
        toggle(c, 190, -4, on=0.0)
    panel(cr, t, A("a2", "Full"), A("a4", "files"), 360, 400, 560, 140, fda, seed=9510)

    def everything(c):
        for k, (kind, word) in enumerate((("files", "files"), ("mail", "mail"), ("messages", "messages"),
                                          ("history", "history"))):
            if t >= A("a4", word):
                with at(c, -195 + k * 130, -6, pop(t, A("a4", word), 0.25)):
                    icon(c, kind, 0, 0, 1.0, seed=9520 + k * 5)
                write(c, [(word, INK)], -195 + k * 130, 66, 22, align="center", bold=True)
    panel(cr, t, A("a4", "files"), A("a5"), 360, 400, 600, 190, everything, seed=9540)

    def agent(c):
        robot(c, -140, 50, 1.0, t)
        for k, kind in enumerate(("files", "mail", "messages")):
            icon(c, kind, 60 + k * 90, 0, 0.7, seed=9550 + k * 5)
    panel(cr, t, A("a6", "AI"), A("a7"), 360, 400, 520, 220, agent, seed=9560)

    def quote(c):
        write(c, [("\"...without users' full", INK)], 0, -30, 34, align="center", bold=True)
        write(c, [("knowledge and understanding.\"", INK)], 0, 14, 34, align="center", bold=True)
        write(c, [("Apple, 2 Oct 2026", GRAPHITE)], 0, 62, 26, align="center")
    panel(cr, t, A("a7", "expose"), A("a8"), 360, 400, 600, 190, quote, seed=9570, fill=hexc("#f5f5f7"))
    source_tag(cr, t, A("a7", "Apple"), "Apple Developer News", end=A("a8"))

    def explicit(c):
        write(c, [("Full Disk Access", INK)], -40, -40, 36, align="center", bold=True)
        toggle(c, 190, -52, on=ease_out(seg(t, A("a9", "explicit"), A("a9", "explicit") + 0.5)))
        shape(c, rrect_pts(-230, 0, 460, 70, 16, 14), hexc("#fde7e3"), seed=9581, amp=0.4, lw=4)
        write(c, [("ARE YOU SURE?", RED)], 0, 48, 40, align="center", bold=True)
    panel(cr, t, A("a9", "only"), A("a10", end=True) + 0.2, 360, 400, 560, 220, explicit, seed=9580)
    if A("a10", "yes") <= t < A("a10", end=True) + 0.2:
        stamp(cr, t, A("a10", "yes"), "THINK FIRST", dur=A("a10", end=True) + 0.2 - A("a10", "yes"), y=560)

    def calendar(c):
        shape(c, rrect_pts(-90, -80, 180, 170, 14, 14), WHITE, seed=9590, amp=0.4, lw=4)
        shape(c, rrect_pts(-90, -80, 180, 44, 14, 14), RED, seed=9591, amp=0.3, lw=4)
        write(c, [("?", INK)], 0, 70, 110, align="center", bold=True)
    panel(cr, t, A("a11", "when"), A("a12") + 0.1, 360, 400, 260, 240, calendar, seed=9595)


def scene_end(cr, t, tl):
    A = tl.at
    _bg(cr, t, [(A("a12") - 0.4, TWO)])
    _host(cr, t, tl, arms=("point", "hip"), eyes="happy")
    _globe(cr, t, tl, "wide", "smile")
    cr.identity_matrix()
    hl(cr, t, [("would ", INK), ("YOU", RED), (" allow it?", INK)], 215, 62, A("a12"), bold=True, underline=True)

    def agent(c):
        robot(c, -60, 40, 0.9, t)
        icon(c, "files", 90, 0, 0.8)
    panel(cr, t, A("a12", "AI"), 999, 360, 380, 360, 190, agent, seed=9600)
    buttons(cr, t, A("a12", "comments"), (("YES", GREEN), ("NO", RED)), y=530, s=0.75)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"talk": scene_talk, "end": scene_end}[name](cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
