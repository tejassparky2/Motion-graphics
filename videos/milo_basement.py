"""Milo thriller #3: "Never Open the Basement Door".

Script: out/scripts_thriller_batch1.md, story 3 (owner auto-approved all three on 14 Oct 2026). Original fiction.
Lily's drawing is drawn by our engine (crayon), the rest are film-like shots.
"""
import math

from motion import voice
from motion import thriller as th
from motion.engine import W, cue

NARRATOR = dict(turbo=True, turbo_ref="am_puck+3")
MUSIC = "thriller"
TAIL = 1.4
voice.SPEAKERS.update({"lily": dict(voice="af_sky", turbo_ref="af_sky+5"),
                       "boy": dict(voice="am_puck", turbo_ref="am_puck+6")})

SCRIPT = [
    dict(id="b1", scene="s", text="My first babysitting job came with one rule. Never open the basement door."),
    dict(id="b2", scene="s", text="At [ten p.m.|10 P.M.], something knocked. From inside the basement.", gap=0.4),
    dict(id="b3", scene="s", text="Lily, the little girl, didn't even look up from her drawing. That's just my brother.",
         speaker="lily", speaker_from="That's"),
    dict(id="b4", scene="s", text="But her parents told me Lily is an only child."),
    dict(id="b5", scene="s", text="The knocking stopped. Then a whisper through the door. Are they gone?",
         speaker="boy", speaker_from="Are", gap=0.4),
    dict(id="b6", scene="s", text="A boy's voice. Please. They said you'd be nice.", speaker="boy",
         speaker_from="Please."),
    dict(id="b7", scene="s", text="My phone lit up. A text from Lily's mom."),
    dict(id="b8", scene="s", text="Everything okay? Remember the rule."),
    dict(id="b9", scene="s", text="How did she know?", pace=0.95),
    dict(id="b10", scene="s", text="Then I saw it. A tiny red light in the corner of the ceiling. A camera. Pointed "
                                   "right at me."),
    dict(id="b11", scene="s", text="Lily smiled. [chuckle] Mommy's always watching.", speaker="lily",
         speaker_from="Mommy's", gap=0.4),
    dict(id="b12", scene="s", text="So. Do you open the door? Or pretend you never heard it?"),
]

S = dict(door="v3_01_door", knock="v3_02_knock", lily="v3_03_lily", photo="v3_04_photo", listen="v3_05_listen",
         gap="v3_06_gap", face="v3_07_phone", camera="v3_08_camera", smile="v3_09_smile")

METADATA = dict(
    title="Never Open the Basement Door 🚪",
    alt_titles=["Her Parents Said She Was an Only Child...", "The Babysitting Rule I Almost Broke"],
    description="""My first babysitting job came with ONE rule: never open the basement door.

At 10 P.M., something knocked. From inside. The little girl didn't even look up: "That's just my brother."

But her parents told me she's an only child...

Would you open the door, or pretend you never heard it? 👇

A short thriller story (fiction) starring Milo.

🔔 Interestingly Strange: strange stories, paradoxes and twists, in under a minute.""",
    hashtags=["#Thriller", "#ScaryStories", "#Shorts"],
    tags=["scary story", "thriller story", "babysitting story", "creepy story", "basement", "suspense",
          "short horror story", "milo", "plot twist", "interestingly strange"],
    pinned_comment="Open the door, or pretend you never heard it? 🚪 Be honest 👇",
)

_plan = {}


def plan(tl):
    if id(tl) in _plan:
        return _plan[id(tl)]
    A = tl.at
    P = lambda **d: dict(move="push", **d)
    cuts = [
        (0.0, S["door"], P(focus=(0.5, 0.45), zoom=(1.02, 1.22))),
        (A("b1", "Never"), S["door"], dict(move="push", focus=(0.5, 0.5), zoom=(1.35, 1.5))),
        (A("b2"), S["knock"], P(focus=(0.5, 0.8), zoom=(1.04, 1.3), shake=0.15)),
        (A("b3"), S["lily"], P(focus=(0.5, 0.45))),
        (A("b4"), S["lily"], dict(move="push", focus=(0.42, 0.22), zoom=(1.5, 1.75))),   # the photo take showed two kids
        (A("b5"), S["listen"], P(focus=(0.5, 0.4))),
        (A("b5", "Are"), S["gap"], P(focus=(0.5, 0.9), zoom=(1.05, 1.35))),
        (A("b6", "Please."), S["gap"], dict(move="push", focus=(0.5, 0.92), zoom=(1.4, 1.6), shake=0.1)),
        (A("b7"), S["face"], P(focus=(0.5, 0.4))),
        (A("b8"), S["face"], dict(move="hold", zoom=(1.2, 1.22), bright=0.45)),
        (A("b9"), S["face"], dict(move="push", zoom=(1.3, 1.45), focus=(0.5, 0.35))),
        (A("b10", "red"), S["camera"], P(focus=(0.75, 0.17), zoom=(1.04, 1.5), lift=0.7)),
        (A("b10", "Pointed"), S["camera"], dict(move="push", focus=(0.75, 0.17), zoom=(1.7, 2.0), shake=0.15, lift=0.7)),
        (A("b11"), S["smile"], P(focus=(0.5, 0.4), zoom=(1.03, 1.25))),
        (A("b12"), S["door"], dict(move="push", focus=(0.5, 0.5), zoom=(1.1, 1.5))),
    ]
    _plan[id(tl)] = th.Plan(cuts, tl.total)
    return _plan[id(tl)]


def drawing(cr, t, start):
    """Lily's crayon drawing: four stick figures, the fourth small one behind a door."""
    if t < start:
        return
    p = min(1, (t - start) / 0.35)
    cr.save()
    cr.translate(W / 2, 745)                            # below her face, above the captions
    cr.rotate(0.05)
    cr.scale(0.4 + 0.25 * p, 0.4 + 0.25 * p)
    cr.rectangle(-230, -170, 460, 340)
    cr.set_source_rgba(0.96, 0.95, 0.9, 0.97)
    cr.fill()
    cr.set_line_cap(1)
    cr.set_line_width(7)
    for k, (x, h, col) in enumerate(((-170, 150, (0.85, 0.2, 0.3)), (-90, 160, (0.2, 0.35, 0.85)),
                                     (-10, 100, (0.95, 0.65, 0.1)))):
        cr.set_source_rgba(*col, 0.9)
        cr.arc(x, 80 - h, 22, 0, 2 * math.pi)
        cr.stroke()
        cr.move_to(x, 102 - h)
        cr.line_to(x, 80 - h * 0.3)
        cr.move_to(x - 30, 60 - h * 0.6)
        cr.line_to(x + 30, 60 - h * 0.6)
        cr.move_to(x, 80 - h * 0.3)
        cr.line_to(x - 22, 120)
        cr.move_to(x, 80 - h * 0.3)
        cr.line_to(x + 22, 120)
        cr.stroke()
    cr.set_source_rgba(0.35, 0.22, 0.12, 0.95)       # the door, with the small one behind it
    cr.rectangle(70, -110, 120, 230)
    cr.stroke()
    cr.set_source_rgba(0.1, 0.1, 0.1, 0.9)
    cr.arc(130, -20, 14, 0, 2 * math.pi)
    cr.stroke()
    cr.move_to(130, -6)
    cr.line_to(130, 60)
    cr.stroke()
    for k in range(3):                                  # three bars scribbled across the door
        cr.move_to(80, -70 + k * 70)
        cr.line_to(180, -60 + k * 70)
    cr.set_source_rgba(0.1, 0.1, 0.1, 0.9)
    cr.stroke()
    cr.restore()


def draw(cr, t, tl):
    A = tl.at
    plan(tl).draw(cr, t)
    cue("knock", t, A("b2", "knocked."))
    cue("sting", t, A("b2", "inside"))
    cue("hush", t, A("b4") - 0.3, 0.3)
    cue("thud", t, A("b4", "only"))
    cue("whisper_air", t, A("b5", "Are"), 1.4)
    cue("heartbeat", t, A("b5"), A("b10") - A("b5"))
    cue("buzz", t, A("b7", "lit"))
    cue("riser", t, A("b9"), A("b10", "red") - A("b9"))
    cue("sting", t, A("b10", "red"))
    cue("hush", t, A("b11") - 0.4, 0.4)
    cue("sting", t, A("b11", "Mommy's"))
    cue("heartbeat", t, A("b12"), tl.total - A("b12"))
    th.flash(cr, t, A("b2", "inside"), (1, 1, 1), 0.15, 0.6)
    th.flash(cr, t, A("b10", "red"), (1, 0.1, 0.1), 0.25, 0.5)
    th.flash(cr, t, A("b11", "Mommy's"), (1, 1, 1), 0.15, 0.6)
    th.finish(cr, t, flicker=0.2 if A("b2") <= t < A("b3") else 0.08)
    th.phone(cr, t, A("b8") - 0.6, "Lily's Mom", "Everything okay? Remember the rule.", end=A("b9") + 0.4)
    if A("b11", "Mommy's") <= t < A("b12"):
        drawing(cr, t, A("b11", "Mommy's") + 0.6)
    th.choice(cr, t, A("b12", "open"), "OPEN IT", "PRETEND")
    th.hook(cr, t, [("NEVER OPEN THE", False), ("BASEMENT DOOR", True)], end=A("b2"))
    th.captions(cr, t, tl)
