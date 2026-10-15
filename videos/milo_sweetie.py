"""Milo thriller #1: "Mom Never Calls Me Sweetie".

Script: out/scripts_thriller_batch1.md, story 1 (owner auto-approved all three on 14 Oct 2026 before going to sleep:
"auto approval for all 3, I will review tomorrow morning"). Original fiction. Shots: tools/shots.py with
assets/milo/shots_v1.json (picked takes in assets/milo/shots/). Voices: Chatterbox Turbo; Milo from a younger
Kokoro reference, the voice downstairs breathy and too calm.
"""
from motion import voice
from motion import thriller as th
from motion.engine import cue

NARRATOR = dict(turbo=True, turbo_ref="am_puck+3")
MUSIC = "thriller"
TAIL = 3.2      # the 3-2-1 countdown after the last line
voice.SPEAKERS.update({"her": dict(voice="af_nicole", turbo_ref="af_nicole")})

SCRIPT = [
    dict(id="b1", scene="s", text="Come down for dinner, sweetie.", speaker="her"),
    dict(id="b1b", scene="s", text="But my mom has never called me sweetie."),
    dict(id="b2", scene="s", text="The kitchen light is on. And someone down there is humming her favorite song."),
    dict(id="b3", scene="s", text="Then my phone buzzes. A text from Mom."),
    dict(id="b4", scene="s", text="Working late. Order pizza. Love you."),
    dict(id="b5", scene="s", text="The humming stops.", gap=0.5),
    dict(id="b6", scene="s", text="Milo? I can hear you breathing. [chuckle]", speaker="her", gap=0.6, pace=0.9),
    dict(id="b7", scene="s", text="One step. Then another. She's coming up."),
    dict(id="b8", scene="s", text="I lock myself in my room. And I call Mom."),
    dict(id="b9", scene="s", text="[gasp] Her ringtone starts playing. Right under my bed.", gap=0.4),
    dict(id="b10", scene="s", text="Someone in my room has her phone. Someone in the hall is wearing her voice."),
    dict(id="b11", scene="s", text="The doorknob turns. And the bed creaks."),
    dict(id="b12", scene="s", text="Door, or window? You have three seconds.", gap=0.4),
]

# the take picked for each shot (assets/milo/shots/<name>.jpg)
S = dict(stairs="v1_01_stairs", kitchen="v1_02_kitchen", face="v1_03_phone", doorway="v1_05_doorway",
         woman="v1_06_woman", foot="v1_07_foot", lock="v1_08_lock", underbed="v1_09_underbed",
         feet="v1_10_feet", knob="v1_11_knob", choice="v1_12_choice")

METADATA = dict(
    title="Mom Never Calls Me Sweetie... 😨",
    alt_titles=["Her Phone Was Ringing Under My Bed", "Door or Window? You Have 3 Seconds."],
    description="""Mom calls me down for dinner. "Come eat, sweetie." But my mom has NEVER called me sweetie...

Then she texts me: "Working late. Order pizza." So who is downstairs, humming her song? And why is her phone ringing under MY bed?

Door or window? You have three seconds. 👇

A short thriller story (fiction) starring Milo.

🔔 Interestingly Strange: strange stories, paradoxes and twists, in under a minute.""",
    hashtags=["#Thriller", "#ScaryStories", "#Shorts"],
    tags=["scary story", "thriller story", "creepy story", "suspense", "short horror story", "milo",
          "home alone story", "plot twist", "door or window", "interestingly strange"],
    pinned_comment="Door or window? 🚪🪟 You have 3 seconds. Comment before you scroll 👇",
)

_plan = {}


def plan(tl):
    if id(tl) in _plan:
        return _plan[id(tl)]
    A = tl.at
    P = lambda d: dict(move="push", **d)
    cuts = [
        (0.0, S["stairs"], P(dict(focus=(0.5, 0.3), zoom=(1.02, 1.2)))),
        (A("b2"), S["kitchen"], P(dict(focus=(0.5, 0.3), zoom=(1.05, 1.22)))),
        (A("b2", "humming"), S["kitchen"], dict(move="hold", zoom=(1.28, 1.3), focus=(0.62, 0.25))),
        (A("b3"), S["face"], P(dict(focus=(0.5, 0.4)))),
        (A("b4"), S["face"], dict(move="hold", zoom=(1.2, 1.22), bright=0.45)),
        (A("b5"), S["doorway"], P(dict(focus=(0.5, 0.4), zoom=(1.0, 1.08)))),
        (A("b6"), S["woman"], P(dict(focus=(0.5, 0.3), zoom=(1.05, 1.3), shake=0.25))),
        (A("b7"), S["foot"], P(dict(focus=(0.5, 0.6)))),
        (A("b7", "coming"), "v1_06_woman_b", dict(move="push", zoom=(1.35, 1.5), focus=(0.5, 0.3), shake=0.15)),
        (A("b8"), S["lock"], P(dict(focus=(0.5, 0.5), shake=0.2))),
        (A("b8", "call"), S["face"], dict(move="hold", zoom=(1.25, 1.27), bright=0.45)),
        (A("b9"), S["underbed"], P(dict(focus=(0.65, 0.6), zoom=(1.04, 1.3), shake=0.1, lift=0.8))),
        (A("b10", "hall"), S["feet"], P(dict(focus=(0.5, 0.9), zoom=(1.04, 1.25)))),
        (A("b11"), S["knob"], P(dict(focus=(0.5, 0.5), shake=0.2))),
        (A("b11", "bed"), S["underbed"], dict(move="push", zoom=(1.3, 1.45), focus=(0.6, 0.55), shake=0.5, lift=0.8)),
        (A("b12"), S["choice"], P(dict(focus=(0.45, 0.45), zoom=(1.02, 1.12)))),
    ]
    _plan[id(tl)] = th.Plan(cuts, tl.total)
    return _plan[id(tl)]


def draw(cr, t, tl):
    A = tl.at
    plan(tl).draw(cr, t)
    # sound: hum (music box) until it stops dead, the silence, the shocks, the heartbeat to the end
    cue("musicbox", t, A("b2", "humming"), A("b5", "stops", end=True) - A("b2", "humming"))
    cue("hush", t, A("b5", "stops", end=True), A("b6") - A("b5", "stops", end=True) + 0.05)
    cue("sting", t, A("b6"))
    cue("whisper_air", t, A("b6"), 1.6)
    cue("step", t, A("b7", "One"))
    cue("step", t, A("b7", "another"))
    cue("creak", t, A("b7", "coming"), 0.8)
    cue("heartbeat", t, A("b7"), tl.total - A("b7"))
    cue("slam", t, A("b8", "lock"))
    cue("lock", t, A("b8", "room", end=True))
    cue("riser", t, A("b8", "call"), A("b9") - A("b8", "call"))
    cue("ring", t, A("b9", "ringtone"), A("b10") - A("b9", "ringtone"))
    cue("sting", t, A("b9", "Right"))
    cue("sniff", t, A("b10", "voice.", end=True) + 0.05)
    cue("gasp_in", t, A("b11") - 0.3)
    cue("hush", t, A("b11") - 0.35, 0.35)
    cue("creak", t, A("b11", "doorknob"), 0.6)
    cue("creak", t, A("b11", "bed"), 1.0)
    cue("sting", t, A("b11", "creaks"))
    th.flash(cr, t, A("b6"), (1, 1, 1), 0.12, 0.5)
    th.flash(cr, t, A("b9", "Right"), (1, 1, 1), 0.2, 0.8)
    th.flash(cr, t, A("b11", "bed"), (1, 1, 1), 0.15, 0.6)
    flick = 0.35 if A("b5") <= t < A("b7") else 0.18 if t >= A("b11") else 0.08
    th.finish(cr, t, flicker=flick)
    # the text the image model can't draw
    th.phone(cr, t, A("b4") - 0.6, "Mom", "Working late. Order pizza. Love you.", end=A("b5") - 0.1)
    th.phone(cr, t, A("b8", "call"), "Calling Mom...", "ringing...", typing=0.01, end=A("b9", "ringtone"))
    if t >= A("b9", "ringtone") and t < A("b11"):
        th.glow(cr, 470, 760, 160, (0.5, 0.7, 1.0), 0.18 + 0.12 * (int(t * 4) % 2))
    th.choice(cr, t, A("b12", "Door"), "DOOR", "WINDOW", count_from=A("b12", "seconds.", end=True) + 0.1)
    th.hook(cr, t, [("MOM NEVER CALLS ME", False), ("SWEETIE", True)], end=A("b2"))
    th.captions(cr, t, tl)
