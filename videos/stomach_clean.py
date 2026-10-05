"""Body Facts 14: "Your Stomach Growls to CLEAN Itself" — the migrating motor complex. Script approved by the owner.

Facts (sources in research_notes/body_facts_12-14.md):
- Between meals (fasting), a cycle of gut contractions called the migrating motor complex (MMC) recurs about every
  90-120 minutes; its strongest phase sweeps from the stomach down through the small intestine, clearing leftover
  food, secretions and bacteria (the "interdigestive housekeeper"). It is linked to the hormone motilin.
- Eating interrupts it; the fed (digestive) pattern takes over.
- The rumbling (borborygmi) is gas and fluid being pushed along. Hunger is real too: the script says "It's also us,
  cleaning", not that growling never means hunger.
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape, write
from motion.kit import camera, enter_world, set_camera, whip
from videos.kidney_donor import eyes, mouth

# Voices: natural stock voices at their own pitch. The doctor is Kokoro am_adam (owner: no cloned voice).
STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "stomach": dict(voice="af_heart", speed=0.95),
    "gut": dict(voice="am_onyx", speed=0.95),
    "crumb": dict(voice="am_michael", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"cleaning", "growling", "growl", "squeeze", "migrating", "motor", "complex", "rumble", "loudly"}

SCRIPT = [
    dict(id="c1", scene="gut", text="Okay. He hasn't eaten for two hours. You know what that means.",
         speaker="stomach"),
    dict(id="c2", scene="gut", text="Cleaning time! Big squeeze, coming through!", speaker="gut"),
    dict(id="c3", scene="gut", text="Wait! I'm a leftover crumb. Where are you taking me?", speaker="crumb"),
    dict(id="c4", scene="gut", text="Out. When there's no food, we sweep everything down, every couple of hours.",
         speaker="stomach"),
    dict(id="c5", scene="gut", text="And what's that loud rumble?", speaker="crumb"),
    dict(id="c6", scene="gut", text="That's air and liquid getting pushed along. Humans call it growling.",
         speaker="gut"),
    dict(id="c7", scene="gut", text="He thinks it's just hunger. It's also us, cleaning.", speaker="stomach"),
    dict(id="w1", scene="ward", text="Doctor, why does my stomach growl when it's empty?", speaker="mike"),
    dict(id="w2", scene="ward", text="It's a cleaning wave, called the migrating motor complex.", speaker="doctor"),
    dict(id="w3", scene="ward", text="Between meals, about every ninety minutes to two hours, your gut squeezes from "
                                     "the stomach down.", speaker="doctor"),
    dict(id="w4", scene="ward", text="It sweeps leftover food and bacteria along. The growl is air and liquid "
                                     "moving.", speaker="doctor"),
    dict(id="w5", scene="ward", text="When you eat, the cleaning stops, and normal digestion starts.",
         speaker="doctor"),
    dict(id="w6", scene="ward", text="So my stomach is just vacuuming, bro.", speaker="danny", gap=0.3),
    dict(id="w7", scene="ward", text="Loudly.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Your Stomach Growls to CLEAN Itself 🧹",
    alt_titles=["Why Your Stomach Growls (It's Not Just Hunger) 🧹", "Your Gut Has a Cleaning Crew 😳"],
    description="""That growl isn't only hunger. It's your gut cleaning itself. 🧹😳

Between meals, roughly every 90 minutes to 2 hours, a wave of squeezing called the migrating motor complex sweeps from your stomach down through your small intestine. It clears out leftover food and bacteria, like a housekeeper. The growl you hear is air and liquid being pushed along. As soon as you eat, the cleaning stops and normal digestion takes over.

Sources: physiology of the migrating motor complex (interdigestive cycle of about 90-120 minutes, linked to the hormone motilin); reviews of gut motility and bowel sounds (borborygmi).

(Cartoon, real facts. Not medical advice: talk to a doctor about ongoing stomach problems.)

💬 When does your stomach growl the loudest? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#BodyFacts", "#Gut", "#Doctor"],
    tags=["why does my stomach growl", "stomach growling", "migrating motor complex", "gut cleaning",
          "borborygmi", "body facts", "weird body facts", "digestion", "doctor explains", "medical animation"],
    pinned_comment="Be honest: has your stomach ever growled in a silent room? 😂 👇",
)

BG = hexc("#f7c6c0")
PINK, PINK_D = hexc("#f4a6a0"), hexc("#d67a7c")
ST = (360, 360)                          # the stomach
PATH = [(470, 470), (520, 560), (400, 610), (250, 620), (220, 720), (360, 760), (520, 770), (540, 870),
        (380, 920), (220, 930), (230, 1030), (400, 1060), (560, 1060)]     # the small intestine, coiled


def along(pts, u):
    u = min(1.0, max(0.0, u))
    f = u * (len(pts) - 1)
    i = min(len(pts) - 2, int(f))
    return lerp(pts[i][0], pts[i + 1][0], f - i), lerp(pts[i][1], pts[i + 1][1], f - i)


def stomach(cr, t, mood, talking, squeeze):
    with at(cr, ST[0], ST[1], 1.0):
        sx = 1 - 0.08 * squeeze
        cr.scale(sx, 1 / sx)
        shape(cr, [(-150, -80), (-60, -150), (60, -140), (150, -60), (160, 40), (110, 110), (20, 130),
                   (-60, 110), (-120, 50), (-170, -10)], PINK, seed=2100, amp=0, lw=4.5)
        line(cr, [(-150, -80), (-210, -170)], 30, PINK, seed=2101, amp=0)        # the food pipe coming in
        for k in range(3):
            line(cr, [(-90, -40 + 40 * k), (-20, -50 + 40 * k), (60, -40 + 40 * k)], 3, PINK_D, seed=2102 + k,
                 amp=0)
        eyes(cr, 0, -40, 0.95, mood)
        mouth(cr, 0, 6, 0.8, mood, talking, t)


def intestine(cr, t, wave, mood, talking):
    line(cr, PATH, 62, PINK_D, seed=2110, amp=0)
    line(cr, PATH, 52, PINK, seed=2111, amp=0)
    if wave is not None:   # the squeeze travelling down: a ring that pinches the tube
        x, y = along(PATH, wave)
        blob(cr, x, y, 40, 40, hexc("#c4544b", 0.55), seed=2112, amp=0, lw=0, stroke=None)
        for k in (-1, 1):
            x2, y2 = along(PATH, wave + 0.02 * k)
            line(cr, [(x2 - 26, y2 - 4), (x2 + 26, y2 + 4)], 6, PINK_D, seed=2113 + k, amp=0)
    fx, fy = PATH[3]
    blob(cr, fx, fy + 6, 44, 40, PINK, seed=2115, amp=0, lw=0, stroke=None)
    eyes(cr, fx, fy - 4, 0.95, mood)
    mouth(cr, fx, fy + 26, 0.75, mood, talking, t)


def crumb(cr, t, x, y, mood, talking):
    with at(cr, x, y, 1.0, rot=0.2 * math.sin(t * 6)):
        shape(cr, [(-34, -20), (6, -32), (36, -6), (26, 26), (-16, 30), (-38, 6)], hexc("#d9a35c"), seed=2120,
              amp=0, lw=3.5)
        for k in range(4):
            dot(cr, -14 + 10 * k, -10 + 8 * (k % 2), 3, hexc("#a8743a"))
        eyes(cr, 0, -4, 0.5, mood)
        mouth(cr, 0, 14, 0.4, mood, talking, t)


def clock_card(cr, t, x, y, start):
    with at(cr, x, y, 1.0):
        blob(cr, 0, 0, 70, 70, WHITE, seed=2130, amp=0, lw=4)
        u = seg(t, start, start + 1.2)
        a = -math.pi / 2 + 4 * math.pi * u
        line(cr, [(0, 0), (40 * math.cos(a), 40 * math.sin(a))], 6, INK, seed=2131, amp=0)
        line(cr, [(0, 0), (0, -30)], 6, INK, seed=2132, amp=0)
        write(cr, [("2 HOURS", INK)], 0, 106, 34, align="center", bold=True)


def scene_gut(cr, t, tl):
    A = tl.at
    wave_start = A("c2", "squeeze") - 0.2
    wave = None
    if wave_start <= t < A("c7"):
        wave = ((t - wave_start) / 4.0) % 1.0
    TOP, LOW, WIDE = (1.3, 360, 420), (1.2, 380, 860), (0.85, 380, 700)
    keys = [(0, TOP), (A("c2"), (1.3, 300, 600)), (A("c3"), LOW), (A("c4"), TOP), (A("c5"), LOW), (A("c6"), WIDE),
            (A("c7"), TOP)]
    set_camera(camera(t, keys))
    enter_world(cr)
    cr.set_source_rgba(*BG)
    cr.paint()
    sm = "calm" if t < A("c2") else "happy"
    if A("c7") <= t:
        sm = "sly"
    squeeze = math.sin(t * 5) ** 2 if wave is not None else 0.0
    intestine(cr, t, wave, "happy" if wave is not None else "calm", tl.speaking("gut", t))
    stomach(cr, t, "happy" if sm == "sly" else sm, tl.speaking("stomach", t), squeeze)
    # the crumb rides the wave once it starts
    if t < wave_start:
        cx, cy = ST[0] + 60, ST[1] + 80
    else:
        cx, cy = along(PATH, min(0.9, (t - wave_start) / 9.0))
    cm = "shock" if A("c3") <= t < A("c6") else "worried"
    crumb(cr, t, cx, cy, cm, tl.speaking("crumb", t))
    if A("c1", "two") - 0.1 <= t < A("c2"):
        clock_card(cr, t, 580, 220, A("c1", "two") - 0.1)
    if A("c6", "growling") - 0.4 <= t < A("c7"):
        u = (t * 2) % 1
        for k in range(3):
            write(cr, [("GRRR", hexc("#d8363a", 1 - u))], 560 + 20 * k, 640 - 40 * k - 60 * u, 40 + 6 * k,
                  align="center", bold=True)
        cue("hit", t, A("c6", "growling") - 0.4)
    if t < A("c3"):
        label(cr, "Stomach", 180, 220, 260, 300)
        label(cr, "Small intestine", 470, 990, 450, 920)
    if A("c3") <= t < A("c5"):
        label(cr, "Leftover crumb", 500, 480, cx + 20, cy - 30)
    for w in (A("c2", "squeeze"), A("c4", "sweep")):
        cue("hit", t, w)


def cycle_card(cr, t, start):
    """Between meals: cleaning waves every 90-120 minutes, stopped by a meal."""
    u = ease_out(seg(t, start, start + 0.3))
    if u <= 0:
        return
    with at(cr, 360, 690, 0.7 + 0.3 * u):     # over the bed sheet: clear of faces, above the captions
        shape(cr, rrect_pts(-320, -90, 640, 180, 22, 20), WHITE, seed=2140, amp=0, lw=4)
        line(cr, [(-280, 30), (280, 30)], 4, INK, seed=2141, amp=0)
        for k in range(4):
            x = -240 + 160 * k
            shape(cr, [(x - 30, 30), (x, -40), (x + 30, 30)], hexc("#f4a6a0"), seed=2142 + k, amp=0, lw=3)
        write(cr, [("CLEANING WAVE EVERY 90-120 MIN", INK)], 0, 72, 26, align="center", bold=True)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "growl"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w4"), DOC_CLOSE), (A("w5"), TWO_SHOT), (A("w6"), B_CLOSE), (A("w7"), NEXT_BED)]
    m = dict(eyes="wide", mouth="o", arms=("face", "down"))
    if A("w2") <= t < A("w6"):
        m.update(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w6") <= t:
        m.update(eyes="happy", mouth="grin", arms=("hold", "down"))
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w6") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w6"):
        d.update(arms=("hold", "down"))
    if A("w7") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    cr.save()
    cr.identity_matrix()
    if A("w2", "migrating") - 0.1 <= t < A("w3"):
        label(cr, "Migrating motor complex", 360, 320, size=40)
        cue("pop", t, A("w2", "migrating") - 0.1)
    if A("w3") <= t < A("w5"):
        cycle_card(cr, t, A("w3"))
    if A("w5") <= t < A("w6"):
        label(cr, "Eat = cleaning pauses", 360, 320, size=36)
    cr.restore()


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_gut(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
