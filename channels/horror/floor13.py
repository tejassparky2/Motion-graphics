"""Interactive 3D horror, episode 1: "Floor 13", Part 1 (original story).

Owner, 25 Oct 2026: "All a b c make them now" (premise A of the three proposed in this chat). Second person; the
resource is the emergency light's battery, the rule is the sign above the buttons, the phone makes it worse, and the
last line is the two-way choice the comments vote on. Hidden detail for rewatches: "Mrs. Gray" has her feet on
backwards, and the mirror never shows her.

    python channels/horror/make_horror.py floor13
"""
from motion import voice
from motion.engine import cue

from channels.horror import hud, sound  # noqa: F401  (sound registers the horror effects)

NARRATOR = dict(turbo=True)          # Chatterbox Turbo stock voice (synthetic), the channel default for now
SET = "lift"
CHARS = ("gray",)
MOUTH = {}
TAIL = 0.5
MUSIC = "thriller"

voice.SPEAKERS.update({
    "gray": dict(voice="bf_emma", turbo_ref="bf_emma-1.5"),
})

SCRIPT = [
    dict(id="f1", scene="you_close", text="The elevator just stopped at floor [thirteen.|13.] "
                                           "Your building doesn't have a floor [thirteen.|13.]"),
    dict(id="f2", scene="doors", text="The doors slide open. A dark hallway. Wet footprints, right up to the doors."),
    dict(id="f3", scene="panel", text="Above the buttons, there's a sign you've never seen before."),
    dict(id="f4", scene="panel", text="If the doors open on a floor that isn't there, don't step out. And don't answer."),
    dict(id="f5", scene="you_over", text="The lights die. The emergency light kicks in. Battery, twelve percent."),
    dict(id="f6", scene="hall_dark", text="Then, a voice from the dark."),
    dict(id="f7", scene="hall_dark", text="Sweetheart? It's me. Mrs. Gray, from your floor.", speaker="gray", gap=0.4),
    dict(id="f8", scene="hall_dark", text="The elevator is broken. Come out, quickly. I'll take you to the stairs.",
         speaker="gray"),
    dict(id="f9", scene="you_close", text="But Mrs. Gray walks with a cane. She can't do stairs.", gap=0.4),
    dict(id="f10", scene="phone", text="Your phone buzzes. The building group chat."),
    dict(id="f11", scene="phone", text="Elevator broken since six. Nobody use it."),
    dict(id="f12", scene="you_close", text="So who pressed the button for [thirteen?|13?]"),
    dict(id="f13", scene="phone", text="A second message. From Mrs. Gray."),
    dict(id="f14", scene="phone", text="Are you in the elevator? Don't come out. I'm at home, on fourteen."),
    dict(id="f15", scene="hall_dark", text="The voice in the hallway stops."),
    dict(id="f16", scene="mirror", text="In the mirror, the hallway behind you is empty."),
    dict(id="f17", scene="reveal", text="You turn around. [gasp] It isn't."),
    dict(id="f18", scene="drop", text="The elevator jolts. And drops half a metre."),
    dict(id="f19", scene="reveal_close", text="[whispering] Come out now. Or you'll fall.", speaker="gray"),
    dict(id="f20", scene="you_over", text="Battery, two percent."),
    dict(id="f20b", scene="reveal", text="Step out, and you're alone in the dark with whatever she is."),
    dict(id="f20c", scene="cable", text="Stay, and you're trusting a cable that just slipped."),
    dict(id="f21", scene="choice", text="Whatever most of you choose happens in Part [two.|2.]"),
    dict(id="f22", scene="choice", text="So, do you step out onto floor [thirteen?|13?] "
                                         "Or stay in an elevator that's falling?", gap=0.3),
]

METADATA = dict(
    title="Your Elevator Stopped at Floor 13. Your Building Doesn't Have One. 🛗",
    alt_titles=["Don't Step Out on Floor 13 (Part 1) 🛗", "The Voice on Floor 13 Knows Your Name 🛗"],
    description="""Your elevator stops at floor 13. Your building doesn't have a floor 13. 🛗

A sign you've never seen: "If the doors open on a floor that isn't there, don't step out. And don't answer."
Then your neighbour's voice calls from the dark... while she's texting you from home. 📱

Floor 13, Part 1. An interactive horror story: YOU decide what happens next.
💬 Step out, or stay in a falling elevator? The most comments decide Part 2. 👇

(Fiction. 3D animation.)""",
    hashtags=["#HorrorStory", "#InteractiveStory", "#Shorts"],
    tags=["horror story", "interactive story", "you decide", "choose your ending", "floor 13", "elevator horror",
          "scary story", "3d animation", "creepy", "part 1"],
    pinned_comment="Step out 🚪 or stay 🛗? Most comments decide Part 2. (Did anyone notice her feet? 👣)",
)


KEY = {"dark", "don't", "answer", "empty", "isn't", "fall", "falling", "drops", "stairs", "nobody", "cane", "die",
       "whatever", "alone", "doesn't", "who", "stops", "jolts", "slipped"}


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    hud.frame(cr, t, FRAMES)
    hud.finish(cr, t, flash_at=[A("f17", "isn't."), B["f18"].start + 0.1])
    if t >= A("f5", "Battery,"):            # the resource: the emergency light's battery, 12% down to 2%
        v = 0.12 - 0.10 * hud.seg(t, A("f5", "Battery,"), B["f20"].start + 0.3)
        hud.meter(cr, t, "EMERGENCY LIGHT", v, warn=0.15, shake_below=0.05)
    hud.tag(cr, t, "FLOOR 13", "PART 1")
    chips = [("FLOOR 13", None, True),
             ("SIGNAL 1 BAR" if t >= B["f10"].start else "SIGNAL X", B["f10"].start, t < B["f10"].start)]
    if t >= A("f18", "drops"):
        chips.append(("DROP -0.5M", A("f18", "drops"), True))
    hud.chips(cr, t, chips)
    hud.rule(cr, t, A("f4", "don't", nth=1), "RULE: DON'T STEP OUT. DON'T ANSWER.")
    hud.hook(cr, t, [("FLOOR 13?", True), ("YOUR BUILDING", False), ("DOESN'T HAVE ONE", False)],
             end=B["f2"].start, y=330, size=86)
    hud.sign(cr, t, A("f4"), B["f4"].end + 0.2, [("IF THE DOORS OPEN ON", False), ("A FLOOR THAT ISN'T THERE:", False),
                                                    ("DO NOT STEP OUT.", True), ("DO NOT ANSWER.", True)], y=300, size=38)
    hud.phone_thread(cr, t, B["f10"].start, B["f12"].end, "Tower B Residents", "84 members",
                     [(A("f10", "building") - 0.3, "in", "Elevator broken since 6 PM. Nobody use it.", None)])
    hud.phone_thread(cr, t, B["f13"].start, B["f14"].end + 0.4, "Mrs. Gray", "Flat 1402",
                     [(B["f13"].start + 0.1, "in", "Are you in the elevator??", None),
                      (A("f14", "Don't") - 0.3, "in", "Don't come out. I'm at home on 14.", None)])
    hud.big(cr, t, A("f12", "13?"), B["f12"].end + 0.3, [("WHO PRESSED 13?", True)], y=330, size=78)
    hud.your_call(cr, t, A("f22", "step"), "STEP OUT", "STAY", "COMMENT: STEP OUT or STAY")
    hud.captions(cr, t, tl, KEY)
    cue("hum", t, 0.0, B["f5"].start)
    cue("chime", t, A("f1", "stopped"))
    cue("doors", t, B["f2"].start + 0.1)
    cue("power_down", t, A("f5", "die."))
    cue("drip", t, B["f6"].start - 0.3)
    cue("sting", t, A("f17", "isn't."))
    cue("cable", t, B["f18"].start)
    cue("heartbeat", t, B["f19"].start, B["f20c"].end - B["f19"].start)
    cue("riser", t, B["f21"].start, B["f22"].start - B["f21"].start)
