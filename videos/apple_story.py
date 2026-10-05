"""Apple will make "Full Disk Access" on Macs harder to grant because of AI agents (2 Oct 2026), story style, our own
cast. The laptop is a generic drawn laptop (no logo); Apple's words are quoted on screen.

Facts, as of 5 October 2026:
- 2 Oct 2026, Apple developer news, "Updates to Full Disk Access in macOS": some developers use Full Disk Access in
  ways that could expose "files, mail, messages, and even browsing history ... without users' full knowledge and
  understanding"; risk grows as AI agents become "increasingly capable and autonomous"; access only through "very
  explicit user action"; no date, version or app named. TechCrunch
  https://techcrunch.com/2026/10/02/apple-says-its-tightening-macos-full-disk-access-controls-due-to-new-risks-from-ai-agents/ ;
  MacRumors https://www.macrumors.com/2026/10/02/apple-announces-macos-full-disk-access-changes/ ;
  Engadget https://www.engadget.com/2276186/apple-sounds-the-alarm-on-ai-agents-and-full-disk-access/
- Desktop AI agent apps often ask users to grant Full Disk Access (TechCrunch).
"""
import math

from motion.captions import captions
from motion.engine import INK, RED, WHITE, at, blob, ease_out, hexc, lerp, line, pop, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, hl, set_camera, stamp, whip
from motion.news import source_tag
from motion.newsbrand import badge
from motion.newsprops import calendar
from motion.story import buttons
from motion.storykit import (GREEN, NAVY, actor, desk, file_icon, focus, laptop, news_pacing, office, reveal_gaps,
                             robot, sign)

news_pacing()

NARRATOR = dict(speed=0.95)
TAIL = 0.5
MUSIC = dict(mood="tech", drops=['a6'])   # news bed (motion/newsmusic.py); drop = silence before Apple's warning

SCRIPT = [
    dict(id="a1", scene="home", text="If you use a Mac, an important setting is about to change."),
    dict(id="a2", scene="home", text="On October second, Apple warned app makers about a setting called Full Disk "
                                     "Access."),
    dict(id="a3", scene="screen", text="When you turn it on, an app can see almost everything on your Mac."),
    dict(id="a4", scene="screen", text="That includes your files, your emails, your messages and even your browsing "
                                       "history."),
    dict(id="a5", scene="agent", text="Many new AI helpers ask for this access, so they can work for you in the "
                                      "background."),
    dict(id="a6", scene="agent", text="Apple says this could expose everything on your computer without your full "
                                      "knowledge and understanding."),
    dict(id="a7", scene="change", text="So Apple plans to make this setting harder to turn on."),
    dict(id="a8", scene="change", text="You will need to take a very clear and deliberate step before an app gets that "
                                       "access."),
    dict(id="a9", scene="change", text="Apple has not said when this change will arrive."),
    dict(id="a10", scene="end", text="Would you let an AI read everything on your computer? Tell me in the comments."),
]
reveal_gaps(SCRIPT, MUSIC)

METADATA = dict(
    title="Apple Is Locking Down Your Mac Because of AI 🔒",
    alt_titles=["Your Mac Is About to Get Stricter (Because of AI Agents)",
                "Apple's New Warning About AI Apps on Your Mac"],
    description="""On 2 October 2026, Apple told developers it will add new controls to "Full Disk Access" on macOS, the setting that lets an app see almost everything on your Mac: files, mail, messages and browsing history. 🔒

AI agents that work in the background often ask for it. Apple says it could expose everything "without users' full knowledge and understanding", and that the risk grows as AI agents become "increasingly capable and autonomous". Soon, the setting can only be turned on through "very explicit user action". Apple hasn't given a date or named any app.

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

GRAPHITE = hexc("#2b2d33")


def toggle(cr, x, y, on, s=1.0, seed=20000):
    with at(cr, x, y, s):
        col = hexc("#a9a2ae") if on < 0.5 else GREEN
        shape(cr, rrect_pts(-46, -24, 92, 48, 24, 12), col, seed=seed, amp=0.3, lw=4)
        blob(cr, -22 + 44 * ease_out(on), 0, 18, 18, WHITE, seed + 1, amp=0.3, lw=3.5)


def big_screen(cr, x, y, w, h, seed=20010):
    shape(cr, rrect_pts(x - w / 2 - 20, y - h / 2 - 20, w + 40, h + 50, 18, 16), hexc("#c9ccd2"), seed=seed, amp=0.5,
          lw=6)
    shape(cr, rrect_pts(x - w / 2, y - h / 2, w, h, 8, 14), hexc("#eef6fb"), seed=seed + 1, amp=0.3, lw=4)


def home_set(cr, t):
    office(cr, t)
    desk(cr, 620)


def scene_home(cr, t, tl):
    A = tl.at
    keys = [(0, focus(520, 1.6, screen=620)), (A("a1", "setting"), (1.8, 600, 770)), (A("a2"), (1.3, 640, 830)),
            (A("a2", "Apple"), (1.5, 820, 690)), (A("a2", "Full"), (1.8, 660, 720))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    home_set(cr, t)
    actor(cr, "mac_user", 470, t, facing=1, arms=("hold", "down"), eyes="open" if t < A("a1", "setting") else "wide",
          mouth="smile" if t < A("a1", "setting") else "o")
    laptop(cr, 660, 750, 1.3)
    write(cr, [("Mac", INK)], 660, 700, 30, align="center", bold=True)
    if t >= A("a2", "Apple"):   # Apple's notice to developers pins up on the wall
        with at(cr, 840, 600, pop(t, A("a2", "Apple"), 0.2) or 0.01, rot=0.04):
            shape(cr, rrect_pts(-150, -120, 300, 240, 6, 14), WHITE, seed=20100, amp=0.4, lw=4)
            write(cr, [("NOTICE TO", INK)], 0, -70, 28, align="center", bold=True)
            write(cr, [("APP MAKERS", INK)], 0, -36, 28, align="center", bold=True)
            write(cr, [("Full Disk Access", RED)], 0, 20, 32, align="center", bold=True)
            write(cr, [("Apple, 2 Oct 2026", GRAPHITE)], 0, 80, 24, align="center")
    if t >= A("a2", "Full"):
        toggle(cr, 660, 690, 0.0, 0.9)
    hl(cr, t, [("Mac users, ", INK), ("listen", RED)], 215, 80, A("a1"), end=A("a2") - 0.05, bold=True)
    hl(cr, t, [("FULL DISK ACCESS", RED)], 215, 66, A("a2", "Full"), bold=True)
    if t >= A("a2", "Apple"):
        source_tag(cr, t, A("a2", "Apple"), "Apple Developer News, 2 Oct 2026", y=270)


def scene_screen(cr, t, tl):
    A = tl.at
    keys = [(A("a3") - 0.2, (1.0, 600, 760)), (A("a4", "files"), (1.15, 600, 740)), (A("a4", "history"), (1.0, 600, 760))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    home_set(cr, t)
    big_screen(cr, 600, 620, 620, 440)
    write(cr, [("Full Disk Access", INK)], 520, 470, 40, align="center", bold=True)
    toggle(cr, 790, 456, 1.0)
    for k, (kind, word, label) in enumerate((("files", "files", "files"), ("email", "emails", "emails"),
                                             ("messages", "messages", "messages"),
                                             ("history", "history", "history"))):
        if t >= A("a4", word):
            with at(cr, 450 + (k % 2) * 270, 590 + (k // 2) * 140, pop(t, A("a4", word), 0.25) or 0.01):
                file_icon(cr, kind, -40, 0, 1.3, seed=20200 + k * 5)
                write(cr, [(label, INK)], 30, 14, 40, bold=True)
    hl(cr, t, [("sees almost ", INK), ("EVERYTHING", RED)], 215, 64, A("a3", "everything"), bold=True)


def scene_agent(cr, t, tl):
    A = tl.at
    keys = [(A("a5") - 0.2, (1.4, 660, 840)), (A("a5", "AI"), focus(860, 1.7, y=760)), (A("a5", "access"), (1.4, 660, 830)),
            (A("a5", "background"), (1.6, 660, 780)), (A("a6"), (1.3, 640, 700)), (A("a6", "knowledge"), (1.4, 640, 660))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    home_set(cr, t)
    laptop(cr, 660, 750, 1.3)
    walk = ease_out(seg(t, A("a5"), A("a5", "access") + 0.2))
    reach = 0.5 + 0.5 * math.sin(t * 5) if t >= A("a5", "background") else 0.0
    robot(cr, lerp(1150, 860, walk), 905, t, 1.4, reach=reach)
    worried = t >= A("a5", "background")
    actor(cr, "mac_user", 470, t, facing=1, arms=("face", "down") if worried else ("hold", "down"),
          eyes="wide" if worried else "open", mouth="o" if worried else "smile", sweat=worried)
    if t >= A("a5", "background"):
        for k, kind in enumerate(("files", "email", "messages")):
            file_icon(cr, kind, 700 + 80 * (k - 1) + 30 * math.sin(t * 3 + k), 600 - 20 * k, 1.0, seed=20300 + k * 5)
    if t >= A("a6", "expose"):
        with at(cr, 640, 470, pop(t, A("a6", "expose"), 0.2) or 0.01):
            shape(cr, rrect_pts(-290, -90, 580, 180, 12, 14), hexc("#f5f5f7"), seed=20400, amp=0.4, lw=5)
            write(cr, [("\"...without users' full", INK)], 0, -26, 38, align="center", bold=True)
            write(cr, [("knowledge and understanding\"", INK)], 0, 20, 38, align="center", bold=True)
            write(cr, [("Apple, 2 Oct 2026", GRAPHITE)], 0, 66, 26, align="center")
    hl(cr, t, [("AI helpers ", RED), ("want it", INK)], 215, 80, A("a5"), end=A("a6") - 0.05, bold=True)
    hl(cr, t, [("Apple's ", GRAPHITE), ("warning", RED)], 215, 80, A("a6"), bold=True)


def scene_change(cr, t, tl):
    A = tl.at
    keys = [(A("a7") - 0.2, (1.0, 600, 760)), (A("a8", "deliberate"), (1.15, 600, 700)), (A("a9"), (1.3, 660, 830)),
            (A("a9", "when"), (1.5, 760, 700))]
    set_camera(camera(t, keys, dur=0.14))
    enter_world(cr)
    home_set(cr, t)
    if t < A("a9"):
        big_screen(cr, 600, 620, 620, 440)
        write(cr, [("Full Disk Access", INK)], 520, 470, 40, align="center", bold=True)
        toggle(cr, 790, 456, ease_out(seg(t, A("a8", "deliberate"), A("a8", "deliberate") + 0.6)))
        if t >= A("a8", "deliberate"):
            with at(cr, 600, 640, pop(t, A("a8", "deliberate"), 0.2) or 0.01):
                shape(cr, rrect_pts(-250, -90, 500, 200, 16, 14), WHITE, seed=20500, amp=0.4, lw=5)
                write(cr, [("ARE YOU SURE?", RED)], 0, -24, 50, align="center", bold=True)
                for k, (lab, col) in enumerate((("Cancel", hexc("#a9adb5")), ("Allow", GREEN))):
                    shape(cr, rrect_pts(-210 + k * 230, 30, 190, 56, 12, 12), col, seed=20501 + k, amp=0.3, lw=4)
                    write(cr, [(lab, WHITE)], -115 + k * 230, 70, 32, align="center", bold=True)
    else:
        laptop(cr, 660, 750, 1.3)
        robot(cr, 900, 905, t, 1.3)
        actor(cr, "mac_user", 470, t, facing=1, arms=("chin", "down"), eyes="open", mouth="flat")
        if t >= A("a9", "when"):
            with at(cr, 760, 520, pop(t, A("a9", "when"), 0.2) or 0.01):
                calendar(cr, 0, 0, "WHEN?", "?", 1.1)
    hl(cr, t, [("harder to ", INK), ("TURN ON", RED)], 215, 72, A("a7"), end=A("a8") - 0.05, bold=True)
    hl(cr, t, [("a clear, ", INK), ("deliberate", GREEN), (" step", INK)], 215, 62, A("a8"), end=A("a9") - 0.05,
       bold=True)
    hl(cr, t, [("when? ", INK), ("NO DATE YET", RED)], 215, 70, A("a9"), bold=True)


def scene_end(cr, t, tl):
    A = tl.at
    set_camera(camera(t, [(A("a10") - 0.2, (1.35, 660, 840))], dur=0.14))
    enter_world(cr)
    home_set(cr, t)
    laptop(cr, 660, 750, 1.3)
    robot(cr, 870, 905, t, 1.2, reach=0.5 + 0.5 * math.sin(t * 4))
    actor(cr, "mac_user", 470, t, facing=1, arms=("point", "down"), eyes="open", mouth="talk")
    hl(cr, t, [("would ", INK), ("YOU", RED), (" allow it?", INK)], 215, 66, A("a10"), bold=True, underline=True)
    cr.identity_matrix()
    buttons(cr, t, A("a10", "comments"), (("YES", GREEN), ("NO", RED)), y=470, s=0.85)


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    {"home": scene_home, "screen": scene_screen, "agent": scene_agent, "change": scene_change,
     "end": scene_end}[name](cr, t, tl)
    cr.restore()
    badge(cr, t, "TECH", "5 OCT 2026")
    captions(cr, t, tl)
