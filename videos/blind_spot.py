"""Body Facts 12: "You Have a HOLE in Your Vision Right Now" — the blind spot. Script approved by the owner.

Facts (sources in research_notes/body_facts_12-14.md):
- The optic disc, where the optic nerve and blood vessels leave the eye, has no light-detecting photoreceptors:
  every eye has a blind spot, about 15 degrees from the centre of vision, about 6 x 8 degrees across.
- We don't notice it: the brain fills it in from the surrounding picture ("perceptual filling-in"), and with both
  eyes open each eye covers the other's blind spot.
- The test: close the left eye, look at the cross with the right eye, move the screen closer or farther; the dot
  to the right of the cross vanishes when it lands on the right eye's blind spot.
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, set_camera, whip
from motion.organs import brain
from videos.kidney_donor import eyes, mouth

# Voices: natural stock voices at their own pitch. The doctor is Kokoro am_adam (owner: no cloned voice).
STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "retina": dict(voice="af_nova", speed=0.95),
    "spot": dict(voice="am_michael", speed=0.95),
    "brain": dict(voice="af_heart", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"hole", "blind", "spot", "nerve", "brain", "cross", "dot", "vanish"}

SCRIPT = [
    dict(id="a1", scene="eye", text="Light coming in! Everybody, catch it!", speaker="retina"),
    dict(id="a2", scene="eye", text="Sorry. I can't catch anything. I have no light cells at all.", speaker="spot"),
    dict(id="a3", scene="eye", text="The nerve cable to the brain plugs in right here. There's no room for them.",
         speaker="spot"),
    dict(id="a4", scene="eye", text="So there's a hole in his picture?", speaker="retina"),
    dict(id="a5", scene="eye", text="Relax. I paint over it with whatever is around it.", speaker="brain"),
    dict(id="a6", scene="eye", text="And the other eye covers that spot anyway.", speaker="brain"),
    dict(id="a7", scene="eye", text="So nobody ever notices me. Typical.", speaker="spot"),
    dict(id="d1", scene="ward", text="Doctor, I have a hole in my vision?", speaker="mike"),
    dict(id="d2", scene="ward", text="Yes. Everyone does. It's called the blind spot.", speaker="doctor"),
    dict(id="d3", scene="ward", text="It's where the optic nerve leaves your eye. There are no light cells there.",
         speaker="doctor"),
    dict(id="d4", scene="ward", text="Your brain fills in the gap, so you never see it.", speaker="doctor"),
    dict(id="d5", scene="ward", text="Want to find yours? Close your left eye, and stare at the cross with your "
                                     "right eye.", speaker="doctor"),
    dict(id="d6", scene="ward", text="Move your phone slowly closer, or farther. The dot will vanish.",
         speaker="doctor"),
    dict(id="d7", scene="ward", text="Bro, I closed both eyes. Now everything's a blind spot.", speaker="danny",
         gap=0.3),
]

METADATA = dict(
    title="You Have a HOLE in Your Vision Right Now 👁️",
    alt_titles=["Your Eye Has a Blind Spot. Find Yours 👁️", "Your Brain Is Hiding a Hole in Your Vision 😳"],
    description="""There's a hole in your vision right now. Your brain is hiding it. 👁️😳

Every eye has a blind spot: the place where the optic nerve leaves the eye. There are no light-sensing cells there, so that patch of the picture is missing. You never notice because your brain fills it in from what's around it, and with both eyes open, each eye covers the other's blind spot.

Try it: close your LEFT eye, stare at the cross with your RIGHT eye, and slowly move your phone closer or farther. At the right distance, the dot disappears.

Sources: reviews of blind-spot "filling-in" (e.g. Raman & Sarkar, Frontiers/PMC 2016: the blind spot sits about 15° from the centre of vision); standard eye anatomy (optic disc).

(Cartoon, real facts. Not medical advice.)

💬 Did the dot disappear for you? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#BlindSpot", "#BodyFacts", "#Eyes"],
    tags=["blind spot", "blind spot test", "optic nerve", "how eyes work", "brain fills in", "eye facts",
          "body facts", "weird body facts", "doctor explains", "medical animation"],
    pinned_comment="Did the dot disappear? 👀 (Close your LEFT eye, stare at the cross, move your phone.) 👇",
)

WALL, WALL_D = hexc("#c4544b"), hexc("#8e2f2c")
CELL, CELL_D = hexc("#f2a65a"), hexc("#c97a34")
DISC = hexc("#f6e3b4")
SPOT = (470, 760)          # the optic disc on the back of the eye


def retina_bg(cr, t, light):
    """The back wall of the eye: a carpet of light cells (rods and cones), lit up as light lands."""
    cr.set_source_rgba(*WALL_D)
    cr.paint()
    shape(cr, rrect_pts(-200, 420, 1120, 1400, 40, 30), WALL, seed=1900, amp=0, lw=0, stroke=None)
    for row in range(9):
        for col in range(14):
            x = -40 + col * 60 + (row % 2) * 30
            y = 470 + row * 70
            if math.hypot(x - SPOT[0], y - SPOT[1]) < 120:
                continue
            glow = light * (0.5 + 0.5 * math.sin(t * 6 + col + row))
            c = hexc("#ffe28a") if glow > 0.6 else CELL
            shape(cr, rrect_pts(x - 10, y - 26, 20, 52, 10, 10), c, seed=1901 + col + row * 14, amp=0, lw=2.5,
                  stroke=CELL_D)


def optic_disc(cr, t, mood, talking):
    """The blind spot: a pale disc where the optic nerve leaves; blood vessels spread out from it."""
    for k in range(6):
        a = -0.4 + k * 1.05
        line(cr, [(SPOT[0], SPOT[1]), (SPOT[0] + 200 * math.cos(a), SPOT[1] + 200 * math.sin(a)),
                  (SPOT[0] + 330 * math.cos(a + 0.2), SPOT[1] + 330 * math.sin(a + 0.2))], 7, hexc("#7d1018"),
             seed=1920 + k, amp=0)
    blob(cr, SPOT[0], SPOT[1], 110, 100, DISC, seed=1930, amp=0, lw=4)
    blob(cr, SPOT[0], SPOT[1] + 6, 46, 40, hexc("#e9c98a"), seed=1931, amp=0, lw=0, stroke=None)
    eyes(cr, SPOT[0], SPOT[1] - 22, 0.8, mood)
    mouth(cr, SPOT[0], SPOT[1] + 28, 0.7, mood, talking, t)


def nerve_cable(cr, t, glow):
    """The optic nerve, a thick cable from the disc down and away to the brain."""
    pts = [(SPOT[0] + 40, SPOT[1] + 90), (SPOT[0] + 120, SPOT[1] + 260), (SPOT[0] + 260, SPOT[1] + 420)]
    line(cr, pts, 60, hexc("#e9c98a"), seed=1940, amp=0)
    line(cr, pts, 3, INK, seed=1941, amp=0)
    if glow > 0:
        u = (t * 1.5) % 1
        x, y = lerp(pts[0][0], pts[2][0], u), lerp(pts[0][1], pts[2][1], u)
        dot(cr, x, y, 12, hexc("#ffe28a"))


def picture(cr, t, x, y, s, hole, fill):
    """What the eye sends: a small landscape, with the blind-spot hole; `fill` paints it over."""
    with at(cr, x, y, s):
        shape(cr, rrect_pts(-150, -100, 300, 200, 16, 16), hexc("#9fd8f0"), seed=1950, amp=0, lw=4)
        shape(cr, [(-150, 40), (150, 20), (150, 100), (-150, 100)], hexc("#7cc36a"), seed=1951, amp=0, lw=0,
              stroke=None)
        dot(cr, -90, -50, 26, hexc("#ffd23f"))
        shape(cr, rrect_pts(60, -20, 16, 70, 4, 8), hexc("#8f6f4c"), seed=1952, amp=0, lw=2.5)
        blob(cr, 68, -40, 44, 38, hexc("#3fae5c"), seed=1953, amp=0, lw=2.5)
        if hole > 0:
            a = hole * (1 - fill)
            blob(cr, 20, 10, 44 * hole, 40 * hole, hexc("#15171c", a), seed=1954, amp=0, lw=0, stroke=None)
        shape(cr, rrect_pts(-150, -100, 300, 200, 16, 16), None, seed=1955, amp=0, lw=4)


def two_eyes(cr, x, y):
    """Two overlapping fields of view: each eye's blind spot falls inside the other eye's view."""
    blob(cr, x - 60, y, 130, 90, hexc("#5fb6ff", 0.35), seed=1960, amp=0, lw=3)
    blob(cr, x + 60, y, 130, 90, hexc("#ff9fc4", 0.35), seed=1961, amp=0, lw=3)
    dot(cr, x - 10, y, 12, INK)
    dot(cr, x + 10, y, 12, INK)
    write(cr, [("LEFT EYE", INK)], x - 110, y - 100, 24, align="center")
    write(cr, [("RIGHT EYE", INK)], x + 110, y - 100, 24, align="center")


def scene_eye(cr, t, tl):
    A = tl.at
    light = ease_out(seg(t, 0.0, 0.6))
    hole = ease_out(seg(t, A("a4", "hole") - 0.2, A("a4", "hole") + 0.3))
    fill = ease_out(seg(t, A("a5", "paint"), A("a5", "around") + 0.3))
    SPOTC, UP = (1.4, SPOT[0], SPOT[1]), (1.0, 360, 380)
    keys = [(0, (1.1, 360, 640)), (A("a2"), SPOTC), (A("a3"), (1.0, 440, 820)), (A("a4"), UP), (A("a5"), UP),
            (A("a6"), UP), (A("a7"), SPOTC)]
    set_camera(camera(t, keys))
    enter_world(cr)
    retina_bg(cr, t, light)
    # light rays coming in from the top
    for k in range(6):
        x0 = 40 + 130 * k
        u = (t * 0.8 + k * 0.17) % 1
        line(cr, [(x0, -100 + 600 * u), (x0 + 30, -40 + 600 * u)], 8, hexc("#ffe28a", 0.8 * light), seed=1970 + k,
             amp=0)
    nerve_cable(cr, t, A("a3") <= t)
    sm = "sad"
    if A("a3") <= t < A("a4"):
        sm = "calm"
    if A("a7") <= t:
        sm = "sad"
    optic_disc(cr, t, sm, tl.speaking("spot", t))
    # the retina's face, on the carpet of cells to the left
    rm = "happy" if t < A("a2") else ("shock" if t < A("a5") else "happy")
    blob(cr, 180, 640, 90, 70, hexc("#f7c483"), seed=1980, amp=0, lw=4)
    eyes(cr, 180, 624, 0.8, rm)
    mouth(cr, 180, 666, 0.7, rm, tl.speaking("retina", t), t)
    # the brain up top and the picture it gets
    if A("a4") - 0.3 <= t < A("a7"):
        brain(cr, t, 560, 240, 0.55, "happy" if t >= A("a5") else "calm", tl.speaking("brain", t))
        picture(cr, t, 230, 260, 0.9, hole, fill)
        if A("a5", "paint") <= t < A("a6"):     # the brush
            u = seg(t, A("a5", "paint"), A("a5", "around") + 0.3)
            bx, by = 250 + 30 * math.sin(u * 12), 270 + 10 * math.cos(u * 9)
            line(cr, [(bx, by), (bx + 70, by - 90)], 8, hexc("#8f6f4c"), seed=1985, amp=0)
            blob(cr, bx, by, 12, 10, hexc("#3fae5c"), seed=1986, amp=0, lw=2)
        if A("a6") <= t < A("a7"):
            shape(cr, rrect_pts(40, 350, 640, 350, 24, 20), hexc("#ffffff", 0.85), seed=1987, amp=0, lw=3)
            with at(cr, 360, 540, 1.6):
                two_eyes(cr, 0, 0)
            cue("pop", t, A("a6"))
    # tags
    if A("a2") <= t < A("a4"):
        label(cr, "Blind spot (no light cells)", 470, 560, SPOT[0], SPOT[1] - 100)
    if A("a3", "nerve") <= t < A("a4"):
        label(cr, "Optic nerve", 640, 1080, SPOT[0] + 200, SPOT[1] + 360)
    if t < A("a2"):
        label(cr, "Light cells", 180, 540, 180, 580)
    for w in (A("a2"), A("a4", "hole"), A("a5", "paint")):
        cue("hit", t, w)


def test_card(cr, t, start):
    """The blind-spot test, full width so the cross and dot are far enough apart on a phone."""
    u = ease_out(seg(t, start, start + 0.3))
    if u <= 0:
        return
    with at(cr, 360, 690, 0.7 + 0.3 * u):     # over the bed sheet: clear of faces, above the captions
        shape(cr, rrect_pts(-340, -110, 680, 220, 24, 20), WHITE, seed=1990, amp=0, lw=4)
        line(cr, [(-290, 0), (-230, 0)], 10, INK, seed=1991, amp=0)
        line(cr, [(-260, -30), (-260, 30)], 10, INK, seed=1992, amp=0)
        dot(cr, 260, 0, 30, INK)
        write(cr, [("Close your LEFT eye. Stare at the cross.", INK)], 0, 84, 28, align="center")


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("d1") - 0.1, A_CLOSE), (A("d1", "vision"), TWO_SHOT), (A("d2"), DOC_CLOSE), (A("d3"), TWO_SHOT),
            (A("d4"), DOC_CLOSE), (A("d5"), TWO_SHOT), (A("d7"), B_CLOSE), (A("d7", "spot"), NEXT_BED)]
    m = dict(eyes="wide", mouth="o", arms=("hold", "down"))
    if A("d2") <= t < A("d5"):
        m.update(eyes="dot", mouth="smile")
    if A("d5") <= t:
        m.update(eyes="sly", mouth="smirk", arms=("face", "down"))
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("d5") <= t:
        n.update(eyes="sly", arms=("face", "down"))
    if A("d7") <= t:
        n.update(eyes="happy", mouth="grin", arms=("face", "down"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("d2") <= t < A("d7"):
        d.update(arms=("hold", "down"))
    if A("d7") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    cr.save()
    cr.identity_matrix()
    if A("d2", "blind") - 0.1 <= t < A("d4"):
        label(cr, "Blind spot", 360, 320, size=42)
        cue("pop", t, A("d2", "blind") - 0.1)
    if A("d5", "cross") - 0.3 <= t:
        test_card(cr, t, A("d5", "cross") - 0.3)
    cr.restore()


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_eye(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
