"""Low-poly channel, episode 11 (warm, then a surprise): "My Dad Found My AI at 3 AM".

Script: channels/lowpoly/scripts/batch3_research_eps07-11.md (auto-approved by the owner, 18 Oct 2026). Built on
reports/Shorts retention and AI dev humor.md (premise 13; HN "I'm 60 years old"). Dev, Dad (guest), Claude.
Parody, not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep11_dad
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import caption, frames, stat_card, steps_at, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc   # noqa: E402
from motion.polish import appear, vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep11"
MUSIC = "pad"
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep11_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart"),
                       "dad": dict(voice="am_onyx", speed=0.92, turbo_ref="am_onyx")})

SCRIPT = [
    dict(id="m1", scene="two", text="Dad. It's three a.m."),
    dict(id="m2", scene="dad", speaker="dad", text="Shh. We're almost done.", gap=0.4),
    dict(id="m3", scene="devside", text="Done with what?", gap=0.35),
    dict(id="m4", scene="dadclose", speaker="dad", text="An app. It tells me when the tomatoes need water.", gap=0.45),
    dict(id="m5", scene="devside2", text="You don't have tomatoes.", gap=0.4),
    dict(id="m6", scene="dad", speaker="dad", text="I will now.", gap=0.6),
    dict(id="m7", scene="solo", speaker="claude", text="Lovely work, Dan. Shall we add the rain forecast?", gap=0.35),
    dict(id="m8", scene="dadclose", speaker="dad", text="Oh, yes please.", gap=0.5),
    dict(id="m9", scene="devside2", text="It's never said lovely to me.", gap=0.4),
    dict(id="m10", scene="soloclose", speaker="claude", text="You've never said please to me.", gap=0.7),
    dict(id="m11", scene="dad", speaker="dad", text="Next one helps your sister's kids with their homework.", gap=0.4),
    dict(id="m12", scene="devside", text="You hate computers.", gap=0.6),
    dict(id="m13", scene="dadclose", speaker="dad", text="I thought my days of side projects were over.", gap=0.5, pace=0.92),
    dict(id="m14", scene="devside2", text="", hold=1.4, gap=0.3),
    dict(id="m15", scene="devside2", text="What else did you build?", gap=0.4),
    dict(id="m16", scene="dad", speaker="dad", text="A thing that tells me to sleep.", gap=0.5),
    dict(id="m17", scene="devside2", text="Does it work?", gap=0.4),
    dict(id="m18", scene="solo", speaker="claude", text="It's three a.m. You should both sleep.", gap=0.8),
    dict(id="m19", scene="dadclose", speaker="dad", text="You're absolutely right.", pace=0.9),
]

for _d in SCRIPT[1:]:                                    # a little more air between lines (comic timing)
    _d["gap"] = _d.get("gap", 0.18) + 0.15

METADATA = dict(
    title="My Dad Found My AI at 3 AM",
    alt_titles=["\"I Thought My Days of Side Projects Were Over.\"", "My Dad Built 3 Apps Last Night"],
    description="""3 AM. My dad is in my chair, building a tomato-watering app with my AI. He doesn't have tomatoes.

"I thought my days of side projects were over."

Ep. 11 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 Who in your family would secretly love coding with AI? 👇""",
    hashtags=["#ClaudeCode", "#DevLife", "#Dad"],
    tags=["dad", "claude", "ai coding", "learning to code", "side projects", "vibe coding", "wholesome",
          "developer life", "family", "programmer humor"],
    pinned_comment="Who in your family would secretly love coding with AI? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a5c"))


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.65)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    stat_card(cr, t, 170, 112, "TIME", "3:02 AM", RED, 0, appear(t, A("m1", end=True) + 0.3, 0.3), w=240)
    apps, ch = steps_at(t, [(0, 0), (A("m4", "water"), 1), (A("m11", "homework"), 2), (A("m16", "sleep"), 3)])
    if apps:
        stat_card(cr, t, 550, 112, "DAD'S APPS", str(apps), GREEN, ch, appear(t, A("m4", "water"), 0.25), w=200)
    toolcard(cr, t, A("m4", "tomatoes"), A("m6", end=True) + 0.5, "TomatoTime   Claude ▾",
             [("Write", "tomato_time/", "+88", GREEN), ("ok", "Reminds Dan to water the tomatoes", "", GREEN)])
    toolcard(cr, t, A("m7", "rain"), A("m8", end=True) + 0.4, "TomatoTime   Claude ▾", [("Write", "rain_forecast.py", "+41", GREEN)])
    toolcard(cr, t, A("m11", "homework"), A("m12", end=True) + 0.4, "HomeworkHelper   Claude ▾",
             [("Write", "homework_helper/", "+212", GREEN), ("ok", "For Mia and Sam", "", GREEN)])
    toolcard(cr, t, A("m16", "sleep"), A("m18", end=True) + 0.3, "SleepReminder   Claude ▾",
             [("Write", "sleep_reminder.py", "+19", GREEN), ("ok", "3:02 AM: GO TO BED, DAN", "", YEL)])
    cue("typing", t, 0.0, 1.6)
    cue("pop", t, A("m4", "water"))
    cue("ding", t, A("m6", end=True) + 0.1)
    cue("pop", t, A("m11", "homework"))
    cue("hush", t, A("m13") - 0.2, B["m14"].end - A("m13") + 0.5)
    cue("ding", t, A("m16", "sleep"))
    cue("hush", t, A("m18", end=True), 1.4)
    th.hook(cr, t, [("MY DAD FOUND", False), ("MY AI", True)], end=A("m1", end=True) + 0.3, y=175, size=88)
    caption(cr, t, tl)
