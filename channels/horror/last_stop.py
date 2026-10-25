"""Interactive 3D horror, episode 2: "Last Stop", Night 1 (original story).

Owner, 25 Oct 2026: "All a b c make them now" (premise B). Second person on the last night bus; the resource is the
stops left, the rule is the driver's, the counter is the passengers nobody saw get on, the phone makes it worse, and
the last line is the two-way choice the comments vote on. Hidden detail for rewatches: one of the faces reflected
behind you in the window is the old man, who is sitting at the front.

    python channels/horror/make_horror.py last_stop
"""
from motion import voice
from motion.engine import cue

from channels.horror import hud, sound  # noqa: F401  (sound registers the horror effects)

NARRATOR = dict(turbo=True)
SET = "bus"
CHARS = ("driver", "oldman")
MOUTH = {}
TAIL = 0.5
MUSIC = "thriller"

voice.SPEAKERS.update({
    "driver": dict(voice="am_onyx", turbo_ref="am_onyx-1.5"),
    "oldman": dict(voice="bm_lewis", turbo_ref="bm_lewis-1"),
})

SCRIPT = [
    dict(id="b1", scene="you_close", text="The driver told you one rule. Whatever you hear, don't look at the back seats."),
    dict(id="b2", scene="bus_wide", text="It's the last bus out of town. Just you, the driver, and an old man asleep by "
                                         "the window."),
    dict(id="b3", scene="you_over", text="Six stops to yours."),
    dict(id="b4", scene="stop_doors", text="At the next stop, the doors open. Nobody gets on."),
    dict(id="b5", scene="bus_dip", text="But the bus dips. Like someone heavy just stepped in."),
    dict(id="b6", scene="you_close", text="Behind you, a seat creaks. Then another."),
    dict(id="b7", scene="driver_mirror", text="Eyes front. Don't turn around.", speaker="driver", gap=0.35),
    dict(id="b8", scene="window", text="In the dark window, you see your own reflection. And three faces behind you."),
    dict(id="b9", scene="phone", text="Your phone buzzes. The live bus tracker."),
    dict(id="b10", scene="phone", text="Route [nine.|9.] Out of service. In the depot since [ten forty.|10:40.]"),
    dict(id="b11", scene="you_close", text="So what are you riding?"),
    dict(id="b12", scene="oldman", text="The old man opens his eyes. He leans in, and whispers."),
    dict(id="b13", scene="oldman_close", text="[whispering] The driver isn't taking us home. Get off at the next stop. "
                                              "With me.", speaker="oldman", gap=0.35),
    dict(id="b14", scene="neck", text="Something breathes on the back of your neck."),
    dict(id="b15", scene="forest_stop", text="The bus stops in the middle of the forest. No streetlight. No shelter. "
                                             "Just dark."),
    dict(id="b16", scene="driver_mirror", text="This isn't your stop. Sit down.", speaker="driver", gap=0.35),
    dict(id="b17", scene="oldman_out", text="The old man steps out into the dark. And holds out his hand."),
    dict(id="b17b", scene="oldman_out", text="Get off, and you're alone in a forest with a stranger."),
    dict(id="b17c", scene="back_seats", text="Stay, and you're riding with whatever got on."),
    dict(id="b18", scene="choice", text="Whatever most of you choose happens on Night [two.|2.]"),
    dict(id="b19", scene="choice", text="So, do you get off with the old man in the forest? "
                                        "Or ride on with whatever's in the back seats?", gap=0.3),
]

METADATA = dict(
    title="The Bus Driver Had One Rule: Don't Look at the Back Seats 🚌",
    alt_titles=["Nobody Got On. So Why Is the Bus Full? (Night 1) 🚌", "The Last Bus Isn't Taking You Home 🚌"],
    description="""The last bus out of town. The driver's only rule: whatever you hear, don't look at the back seats. 🚌

Nobody gets on... but the seats behind you keep creaking. Then the bus tracker says your bus has been in the depot all night. 📱

Last Stop, Night 1. An interactive horror story: YOU decide what happens next.
💬 Get off with the old man in the forest, or ride on? The most comments decide Night 2. 👇

(Fiction. 3D animation.)""",
    hashtags=["#HorrorStory", "#InteractiveStory", "#Shorts"],
    tags=["horror story", "interactive story", "you decide", "choose your ending", "night bus", "bus horror",
          "scary story", "3d animation", "creepy", "night 1"],
    pinned_comment="Get off 🌲 or ride on 🚌? Most comments decide Night 2. (Count the faces in the window 👀)",
)


KEY = {"don't", "back", "nobody", "dips", "heavy", "creaks", "another", "faces", "out", "service", "depot", "isn't",
       "breathes", "neck", "dark", "forest", "stranger", "whatever", "behind"}


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    hud.frame(cr, t, FRAMES)
    hud.finish(cr, t, flash_at=[A("b8", "three")])
    stops = 6 if t < B["b5"].start else 5     # the resource: stops left to yours
    hud.meter(cr, t, f"STOPS LEFT: {stops}", stops / 6 if t < B["b15"].start else 0.0, warn=0.2, icon="bar")
    bumps = [(B["b5"].start + 0.3, 4), (A("b6", "creaks."), 5), (A("b6", "another."), 6), (A("b14", "breathes"), 7)]
    n, bumped = 3, None
    for at, v in bumps:
        if t >= at:
            n, bumped = v, at
            cue("click", t, at)
    hud.tag(cr, t, "LAST STOP", "NIGHT 1")
    tracker = t >= A("b10", "Out")
    hud.chips(cr, t, [(f"PASSENGERS {n}", bumped, n > 3), ("ROUTE 9" if not tracker else "ROUTE 9: OUT OF SERVICE",
                                                            A("b10", "Out") if tracker else None, tracker)])
    hud.tag_line(cr, t, "11:58 PM" if t < B["b15"].start else "12:13 AM", x=W - 26 - 250 + 4, y=134)
    hud.rule(cr, t, A("b1", "Whatever"), "RULE: DON'T LOOK AT THE BACK SEATS")
    hud.hook(cr, t, [("ONE RULE:", False), ("DON'T LOOK AT", False), ("THE BACK SEATS", True)],
             end=B["b2"].start, y=360, size=84)
    hud.phone_thread(cr, t, B["b9"].start, B["b11"].end, "CityBus Live", "Route 9 tracker",
                     [(B["b9"].start + 0.2, "in", "Route 9: OUT OF SERVICE.", None),
                      (A("b10", "depot") - 0.4, "in", "Vehicle in depot since 10:40 PM.", None)])
    hud.big(cr, t, A("b8", "three"), B["b8"].end + 0.3, [("3 FACES", True)], y=330, size=100)
    hud.your_call(cr, t, A("b19", "get"), "GET OFF", "RIDE ON", "COMMENT: GET OFF or RIDE ON")
    hud.captions(cr, t, tl, KEY)
    cue("engine_idle", t, 0.0, tl.total)
    cue("doors", t, B["b4"].start + 0.1)
    cue("dip", t, B["b5"].start + 0.2)
    cue("creak", t, A("b6", "creaks."), 0.7)
    cue("creak", t, A("b6", "another."), 0.7)
    cue("sting", t, A("b8", "three"))
    cue("breath", t, A("b14", "breathes"))
    cue("brakes", t, B["b15"].start)
    cue("doors", t, B["b17"].start)
    cue("heartbeat", t, B["b16"].start, B["b18"].end - B["b16"].start)
    cue("riser", t, B["b18"].start, B["b19"].start - B["b18"].start)
