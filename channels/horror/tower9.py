"""Interactive 3D horror, episode 3: "Tower 9", Night 1 (original story).

Owner, 25 Oct 2026: "All a b c make them now" (premise C). Second person in a forest fire-watch tower; the resource
is the generator's fuel, the rules are in the last ranger's logbook, the counter is the torches circling below, the
radio makes it worse, and the last line is the two-way choice the comments vote on. Hidden detail for rewatches: in
the lightning, one of the figures holding a torch wears your orange ranger jacket.

    python channels/horror/make_horror.py tower9
"""
from motion import voice
from motion.engine import cue

from channels.horror import hud, sound  # noqa: F401  (sound registers the horror effects)

NARRATOR = dict(turbo=True)
SET = "tower"
CHARS = ("radio", "hatch", "base")
MOUTH = {}
TAIL = 0.5
MUSIC = "horror"

RADIO = "highpass=f=350,lowpass=f=3200,acompressor=threshold=0.1:ratio=6,volume=1.6"
voice.SPEAKERS.update({
    "radio": dict(voice="am_michael", turbo_ref="am_michael", fx=RADIO),            # your voice, over the radio
    "hatch": dict(voice="am_michael", turbo_ref="am_michael", fx="lowpass=f=1800,volume=1.2"),   # ...through the hatch
    "base": dict(voice="bf_isabella", turbo_ref="bf_isabella", fx=RADIO),
})

SCRIPT = [
    dict(id="t1", scene="radio_close", text="Your radio just crackled. The voice calling for help is yours."),
    dict(id="t2", scene="radio_close", text="Tower [nine,|9,] can anyone hear me? Something's climbing the ladder.",
         speaker="radio", gap=0.35),
    dict(id="t3", scene="you_close", text="But you are in tower [nine.|9.] Alone. Thirty metres above the forest.",
         gap=0.35),
    dict(id="t4", scene="logbook", text="The last ranger left two rules in the logbook."),
    dict(id="t5", scene="logbook", text="Never answer the radio after [three.|3 AM.] Never open the hatch."),
    dict(id="t6", scene="cabin", text="The clock says [three fourteen.|3:14.]"),
    dict(id="t7", scene="generator", text="The generator has fuel for one more hour. Then the lights go out."),
    dict(id="t8", scene="trees", text="Down in the trees, torches start moving. Circling the tower."),
    dict(id="t9", scene="trees", text="Five. Then nine. Then too many to count."),
    dict(id="t10", scene="radio_close", text="Please. Open the hatch. They're right behind me.", speaker="radio",
         gap=0.35),
    dict(id="t11", scene="ladder", text="Then, footsteps on the ladder. Slow. Getting closer.", gap=0.35),
    dict(id="t12", scene="hatch", text="Three knocks on the hatch. Right under your feet.", gap=1.4),   # the knocks land in this silence
    dict(id="t13", scene="radio_close", text="The radio crackles again. A different voice."),
    dict(id="t14", scene="radio_close", text="Tower [nine,|9,] this is base. Don't open anything. Help is two hours out.",
         speaker="base", gap=0.35),
    dict(id="t15", scene="you_close", text="Two hours. Your fuel has one.", gap=0.35),
    dict(id="t16", scene="hatch", text="Under the hatch, your own voice starts to cry."),
    dict(id="t17", scene="hatch_close", text="[crying] Please. I'm so cold.", speaker="hatch", gap=0.35),
    dict(id="t17b", scene="hatch", text="Open it, and you meet whatever has your voice."),
    dict(id="t17c", scene="generator", text="Keep it shut, and you're in the dark in one hour."),
    dict(id="t18", scene="choice", text="Whatever most of you choose happens on Night [two.|2.]"),
    dict(id="t19", scene="choice", text="So, do you open the hatch for the voice that sounds like you? "
                                        "Or keep it shut, and wait in the dark?", gap=0.3),
]

METADATA = dict(
    title="Your Radio Is Calling for Help. In YOUR Voice. 📻",
    alt_titles=["Never Answer the Radio After 3 AM (Night 1) 📻", "Something Is Knocking Under Your Feet 📻"],
    description="""3:14 AM in a fire-watch tower, 30 metres above the forest. Your radio crackles... and the voice calling for help is yours. 📻

The last ranger's logbook: never answer the radio after 3 AM. Never open the hatch.
The generator has one hour of fuel. Help is two hours away. And something is knocking under your feet. 🔦

Tower 9, Night 1. An interactive horror story: YOU decide what happens next.
💬 Open the hatch, or keep it shut? The most comments decide Night 2. 👇

(Fiction. 3D animation.)""",
    hashtags=["#HorrorStory", "#InteractiveStory", "#Shorts"],
    tags=["horror story", "interactive story", "you decide", "choose your ending", "fire tower", "forest horror",
          "scary story", "3d animation", "creepy", "night 1"],
    pinned_comment="Open the hatch 🚪 or keep it shut 🔒? Most comments decide Night 2. (Look closely at the lightning ⚡)",
)


KEY = {"yours", "help", "alone", "never", "hatch", "torches", "circling", "many", "behind", "footsteps", "closer",
       "knocks", "feet", "anything", "cry", "cold", "dark", "whatever", "voice", "ladder"}


def tower(cr, k):
    """The blueprint of tower 9: the cabin 30 m up, the hatch and the ladder, the generator at the base."""
    hud.ink(cr, [(230, 110), (420, 110), (420, 200), (230, 200), (230, 110)], hud.INK, 5, k)
    hud.ink(cr, [(215, 110), (325, 75), (435, 110)], hud.INK, 4, k)
    hud.label(cr, "YOU", 250, 165, 28, hud.RED)
    hud.ink(cr, [(360, 200), (400, 200)], hud.RED, 7, k)
    hud.label(cr, "HATCH", 440, 215, 24, hud.RED)
    for x0, x1 in ((240, 200), (410, 450)):
        hud.ink(cr, [(x0, 200), (x1, 540)], hud.INK, 4, k)
    hud.ink(cr, [(240, 200), (450, 540)], hud.INK, 2, k)
    hud.ink(cr, [(410, 200), (200, 540)], hud.INK, 2, k)
    for y in range(215, 540, 22):                        # the ladder under the hatch
        hud.ink(cr, [(372, y), (390, y)], hud.INK, 2, k)
    hud.ink(cr, [(372, 200), (372, 540)], hud.INK, 2, k)
    hud.ink(cr, [(390, 200), (390, 540)], hud.INK, 2, k)
    hud.arrow(cr, 120, 330, 120, 205, k=k)
    hud.arrow(cr, 120, 410, 120, 535, k=k)
    hud.label(cr, "30 M", 80, 380, 34, hud.RED)
    for i in range(9):
        x = 40 + i * 68
        hud.ink(cr, [(x - 22, 560), (x, 515), (x + 22, 560), (x - 22, 560)], (0.2, 0.35, 0.22, 1), 3, k)
    hud.ink(cr, [(470, 520), (540, 520), (540, 556), (470, 556), (470, 520)], hud.INK, 3, k)
    hud.label(cr, "GENERATOR", 430, 505, 22, hud.INK)


def draw(cr, t, tl):
    A, B = tl.at, tl.by_id
    hud.frame(cr, t, FRAMES)
    flashes = [B["t9"].start + 0.4, B["t12"].start - 1.25, B["t16"].start + 0.2]   # same times as sets/tower.js
    hud.finish(cr, t, flash_at=flashes)
    # thunder follows its lightning, between lines (on "Then" it hid the word); the knocks need no thunder
    thunder = [B["t9"].end + 0.05, B["t16"].end + 0.05]
    fuel = 0.34 - 0.24 * hud.seg(t, A("t7", "fuel"), B["t19"].end)     # the resource: generator fuel
    hud.meter(cr, t, "GENERATOR FUEL", fuel, warn=0.2, icon="bar")
    torches = [(A("t8", "torches"), 2), (A("t9", "Five."), 5), (A("t9", "nine."), 9), (A("t9", "many"), 23)]
    n, bumped = 0, None
    for at, v in torches:
        if t >= at:
            n, bumped = v, at
    hud.tag(cr, t, "TOWER 9", "NIGHT 1")
    minute = 14 + int(max(0, t - A("t6", "three")) / 20)
    chips = [(f"03:{minute:02d} AM", None, False), ("SIGNAL X", None, True)]
    if t >= torches[0][0]:
        chips.append((f"TORCHES {n}", bumped, n >= 9))
    hud.chips(cr, t, chips)
    hud.rule(cr, t, A("t5", "Never"), "RULE: NO RADIO AFTER 3 AM. NO HATCH.")
    hud.hook(cr, t, [("THE VOICE ON", False), ("THE RADIO", False), ("IS YOURS", True)], end=B["t2"].start, y=360,
             size=90)
    hud.sign(cr, t, B["t4"].start + 0.2, B["t5"].end + 0.2, [("TOWER 9 LOG", False), ("1. Never answer the", False),
                                                            ("radio after 3 AM.", True), ("2. Never open", False),
                                                            ("the hatch.", True)], y=300, size=42, paper=(0.9, 0.86, 0.72))
    hud.time_card(cr, t, B["t6"].start, B["t6"].end + 0.4, "3:14 AM", "THE RULES START AT 3:00")
    hud.blueprint(cr, t, A("t3", "Alone."), B["t3"].end + 0.3, "TOWER 9", tower)
    hud.big(cr, t, A("t15", "Two"), B["t15"].end + 0.3, [("HELP: 2 HOURS", False), ("FUEL: 1 HOUR", True)], y=320, size=80)
    hud.your_call(cr, t, A("t19", "open"), "OPEN IT", "KEEP SHUT", "COMMENT: OPEN or KEEP SHUT")
    hud.captions(cr, t, tl, KEY)
    cue("rain", t, 0.0, tl.total)
    cue("generator", t, 0.0, tl.total)
    cue("static", t, B["t1"].start, 0.5)
    cue("static", t, B["t2"].start - 0.2, 0.3)
    cue("static", t, B["t10"].start - 0.2, 0.3)
    cue("static", t, B["t13"].start, 0.6)
    cue("static", t, B["t14"].start - 0.2, 0.3)
    for at in thunder:
        cue("thunder", t, at)
    for k in range(4):
        cue("ladder_step", t, B["t11"].start + 0.2 + k * 0.75)
    cue("knock", t, B["t12"].start - 1.25)   # in the silence before the line (on the words, "knocks" was heard as "knots")
    cue("heartbeat", t, B["t15"].start, B["t17c"].end - B["t15"].start)
    cue("riser", t, B["t18"].start, B["t19"].start - B["t18"].start)
