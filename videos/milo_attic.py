"""Milo thriller #2: "He Pointed Behind Me".

Script: out/scripts_thriller_batch1.md, story 2 (owner auto-approved all three on 14 Oct 2026). Fiction based on real
"phrogging" cases (strangers secretly living in someone's home). The old man never speaks: scarier.
"""
from motion import voice
from motion import thriller as th
from motion.engine import cue

NARRATOR = dict(turbo=True, turbo_ref="am_puck+3")
MUSIC = "thriller"
TAIL = 1.2

SCRIPT = [
    dict(id="b1", scene="s", text="Every night at [three a.m.|3 A.M.], the old man across the street stands at his "
                                  "window. Watching my house."),
    dict(id="b2", scene="s", text="Last night, I waved at him. He didn't wave back."),
    dict(id="b3", scene="s", text="He pointed. Not at me. Behind me.", pace=0.95),
    dict(id="b4", scene="s", text="I turned around. My closet door was open. Just a crack."),
    dict(id="b5", scene="s", text="When I looked back, he was pressing a note to his glass."),
    # said in one breath ("Turn." on its own was heard as "Done."); the note still shows one word at a time
    dict(id="b6", scene="s", text="Three words. [Don't,|Don't.] [turn,|Turn.] [around.|Around.]", pace=0.9),
    dict(id="b7", scene="s", text="The floor creaked behind me.", gap=0.5),
    dict(id="b8", scene="s", text="I ran. I didn't stop until I was banging on his door."),
    dict(id="b9", scene="s", text="The police searched our house all night."),
    dict(id="b10", scene="s", text="In the attic above my closet, they found a sleeping bag. Empty cans. And forty "
                                   "photos."),
    dict(id="b11", scene="s", text="Of me. Sleeping.", pace=0.9, gap=0.4),
    dict(id="b12", scene="s", text="Someone had been living in our house for weeks."),
    dict(id="b13", scene="s", text="And the old man had seen him every night. So why did he wait until last night to "
                                   "warn me?"),
]

S = dict(window="v2_01_window", wave="v2_02_wave", point="v2_03_point", closet="v2_04_closet", note="v2_05_note",
         eyes="v2_06_eyes", run="v2_07_run", police="v2_08_police", attic="v2_09_attic", photos="v2_10_photos",
         hatch="v2_11_hatch")

METADATA = dict(
    title="He Pointed Behind Me... 😨",
    alt_titles=["Someone Lived in Our Attic for Weeks", "The Note Said: Don't. Turn. Around."],
    description="""Every night at 3 A.M., the old man across the street stands at his window, watching my house.

Last night I waved. He didn't wave back. He pointed. Not at me. BEHIND me.

Then he pressed a note to his glass: "Don't. Turn. Around."

A short thriller story (fiction), inspired by real "phrogging" cases: people secretly living inside someone else's home.

Why did the old man wait until last night to warn me? 👇

🔔 Interestingly Strange: strange stories, paradoxes and twists, in under a minute.""",
    hashtags=["#Thriller", "#ScaryStories", "#Shorts"],
    tags=["scary story", "thriller story", "creepy story", "phrogging", "someone living in my attic", "suspense",
          "short horror story", "milo", "plot twist", "interestingly strange"],
    pinned_comment="Why did the old man wait so long to warn Milo? 🤔 Wrong answers only 👇",
)

def polaroids(cr, t, start, n=7):
    """The photos they found: Milo asleep, shot from above, pinned up one after another."""
    import math
    from motion.engine import W
    spots = [(-170, -260, -0.12), (150, -300, 0.09), (-40, -60, 0.04), (190, -20, -0.07), (-200, 170, 0.1),
             (60, 210, -0.05), (-60, 420, 0.07)]
    for k, (x, y, r) in enumerate(spots[:n]):
        at = start + 0.18 * k
        if t < at:
            break
        p = min(1, (t - at) / 0.15)
        img = th.image(("v2_12_sleep_a", "v2_12_sleep_b")[k % 2])
        cr.save()
        cr.translate(W / 2 + x, 600 + y)
        cr.rotate(r)
        cr.scale(1.25 - 0.25 * p, 1.25 - 0.25 * p)
        cr.rectangle(-120, -130, 240, 280)
        cr.set_source_rgba(0.94, 0.93, 0.9, 1)
        cr.fill()
        cr.rectangle(-105, -115, 210, 210)
        cr.clip()
        sc = 210 / img.get_width()
        cr.translate(-105, -115)
        cr.scale(sc, sc)
        cr.set_source_surface(img, 0, 0)
        cr.paint()
        cr.restore()


_plan = {}


def plan(tl):
    if id(tl) in _plan:
        return _plan[id(tl)]
    A = tl.at
    P = lambda **d: dict(move="push", **d)
    cuts = [
        (0.0, S["window"], P(focus=(0.5, 0.42), zoom=(1.02, 1.25))),
        (A("b1", "Watching"), S["window"], dict(move="push", focus=(0.5, 0.45), zoom=(1.4, 1.55))),
        (A("b2"), S["wave"], P(focus=(0.5, 0.35))),
        (A("b3"), S["point"], P(focus=(0.6, 0.4), zoom=(1.04, 1.3))),
        (A("b3", "Behind"), S["point"], dict(move="push", focus=(0.75, 0.42), zoom=(1.4, 1.6), shake=0.2)),
        (A("b4"), S["closet"], P(focus=(0.5, 0.5), zoom=(1.02, 1.3))),
        (A("b4", "crack"), S["closet"], dict(move="push", focus=(0.5, 0.45), zoom=(1.5, 1.8))),
        (A("b5"), S["note"], P(focus=(0.5, 0.45), zoom=(1.04, 1.2))),
        (A("b7"), S["eyes"], P(focus=(0.5, 0.45), zoom=(1.05, 1.25), shake=0.35)),
        (A("b8"), S["run"], P(focus=(0.5, 0.6), zoom=(1.05, 1.3), shake=0.6)),
        (A("b9"), S["police"], P(focus=(0.5, 0.5))),
        (A("b10"), S["attic"], P(focus=(0.5, 0.6), zoom=(1.03, 1.25))),
        (A("b10", "forty"), S["photos"], dict(move="push", focus=(0.5, 0.45), zoom=(1.03, 1.2), bright=0.6)),
        (A("b11"), S["photos"], dict(move="push", focus=(0.5, 0.45), zoom=(1.3, 1.5), shake=0.1, bright=0.5)),
        (A("b12"), S["hatch"], P(focus=(0.5, 0.15), zoom=(1.03, 1.3))),
        (A("b13"), S["window"], dict(move="push", focus=(0.5, 0.45), zoom=(1.3, 1.5))),
        (A("b13", "So"), S["point"], dict(move="push", focus=(0.45, 0.25), zoom=(1.5, 1.9), shake=0.05)),
    ]
    _plan[id(tl)] = th.Plan(cuts, tl.total)
    return _plan[id(tl)]


def draw(cr, t, tl):
    A = tl.at
    plan(tl).draw(cr, t)
    cue("heartbeat", t, A("b3"), A("b8") - A("b3"))
    cue("riser", t, A("b3", "Not"), A("b3", "Behind") - A("b3", "Not"))
    cue("sting", t, A("b3", "Behind"))
    cue("creak", t, A("b4", "open"), 0.7)
    cue("hush", t, A("b6") - 0.3, 0.3)
    cue("thud", t, A("b6", "Don't."))
    cue("thud", t, A("b6", "Turn."))
    cue("thud", t, A("b6", "Around."))
    cue("hush", t, A("b7") - 0.45, 0.45)
    cue("creak", t, A("b7", "floor"), 0.9)
    cue("sting", t, A("b7", "creaked"))
    for w in ("ran.", "stop", "banging"):
        cue("step", t, A("b8", w))
    cue("knock", t, A("b8", "banging"))
    cue("police", t, A("b9"), A("b10") - A("b9") + 0.5)
    cue("riser", t, A("b10", "And"), A("b11") - A("b10", "And"))
    cue("hush", t, A("b11") - 0.4, 0.4)
    cue("sting", t, A("b11", "Sleeping."))
    cue("heartbeat", t, A("b12"), tl.total - A("b12"))
    th.flash(cr, t, A("b3", "Behind"), (1, 1, 1), 0.15, 0.6)
    th.flash(cr, t, A("b7", "creaked"), (1, 1, 1), 0.2, 0.75)
    th.flash(cr, t, A("b11", "Sleeping."), (1, 1, 1), 0.2, 0.75)
    if A("b9") <= t < A("b10"):          # red and blue police light washing over the shot
        k = int(t * 3) % 2
        cr.set_source_rgba(*((0.9, 0.05, 0.05) if k else (0.05, 0.2, 0.95)), 0.18)
        cr.paint()
    th.finish(cr, t, flicker=0.25 if A("b10") <= t < A("b12") else 0.1)
    if A("b10", "forty") <= t < A("b12"):
        polaroids(cr, t, A("b10", "forty"))
    if A("b6") <= t < A("b7"):
        th.note(cr, t, [("DON'T.", A("b6", "Don't.")), ("TURN.", A("b6", "Turn.")), ("AROUND.", A("b6", "Around."))],
                y=500)
    th.hook(cr, t, [("HE WATCHES MY HOUSE", False), ("EVERY NIGHT", True)], end=A("b2"))
    th.captions(cr, t, tl)
