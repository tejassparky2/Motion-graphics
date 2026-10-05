"""Body Facts 5: "They Put His TOOTH Inside His EYE" — tooth-in-eye surgery (osteo-odonto-keratoprosthesis).

Facts (kept general; sources in research_notes/body_facts_5-6.md):
- OOKP is for people blinded by severe surface damage to both eyes (e.g. Stevens-Johnson syndrome, chemical burns)
  when a normal cornea transplant has failed or can't work (EyeWiki / American Academy of Ophthalmology).
- A canine tooth is taken out with some of its bone, shaped into a plate, and a clear plastic (PMMA) optical cylinder
  is fixed through it (EyeWiki; All About Vision).
- The tooth-lens piece is put under the skin (cheek / below the eye) for weeks to months so living tissue grows
  around it; the eye's surface is covered with lining from inside the cheek (buccal mucosa); then the piece goes
  into the eye (EyeWiki: ~1 month + 3 months; All About Vision: 2-4 months). "A few months".
- Most patients get useful vision back (EyeWiki: 78% reach 20/400 or better), so "see again", not "perfect sight".
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, BED_A, DOC_CLOSE, TWO_SHOT, bed, doctor, label, patient, room, sheet, watermark
from motion.engine import WHITE, at, blob, cue, dot, ease_out, hexc, lerp, line, rrect_pts, seg, shape
from motion.kit import camera, enter_world, set_camera, whip
from motion.organs import calendar
from motion.surgery import BLOOD, BLOOD_D, SKIN, drapes, forceps, stitches
from videos.kidney_donor import eyes, mouth, scalpel

# Voices: natural stock voices at their own pitch. The doctor is Kokoro am_adam (owner: no cloned voice).
STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "eye": dict(voice="af_heart", speed=0.95),
    "tooth": dict(voice="am_michael", speed=0.95),
    "scalpel": dict(voice="af_bella", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"tooth", "eye", "lens", "cheek", "osteo-odonto-keratoprosthesis", "cornea"}

SCRIPT = [
    dict(id="t1", scene="eye", text="I can't see anything! Everything is cloudy!", speaker="eye"),
    dict(id="t2", scene="eye", text="Don't worry. I'm bringing you some help, my friend.", speaker="scalpel"),
    dict(id="t3", scene="mouth", text="Hey! Why are you pulling me out of the mouth?", speaker="tooth"),
    dict(id="t4", scene="mouth", text="You're going to hold a tiny lens for the eye.", speaker="scalpel"),
    dict(id="t5", scene="mouth", text="In the eye? I'm a tooth! I chew things!", speaker="tooth"),
    dict(id="t6", scene="cheek", text="First, you'll live in his cheek for a few months.", speaker="scalpel"),
    dict(id="t7", scene="cheek", text="In his cheek? This is the strangest job ever!", speaker="tooth"),
    dict(id="t8", scene="eye2", text="Wait. I can see light again!", speaker="eye"),
    dict(id="h1", scene="ward", text="Doctor, is there really a tooth in my eye?", speaker="danny"),
    dict(id="h2", scene="ward", text="Yes. There's a real tooth inside your eye.", speaker="doctor"),
    dict(id="h3", scene="ward", text="Its medical name is osteo-odonto-keratoprosthesis.", speaker="doctor"),
    dict(id="h4", scene="ward", text="We took one of your teeth with a little bone, and fixed a tiny plastic lens "
                                     "through it.", speaker="doctor"),
    dict(id="h5", scene="ward", text="Then it lived in your cheek for a few months, so living tissue could grow "
                                     "around it.", speaker="doctor"),
    dict(id="h6", scene="ward", text="Finally, we put it in your eye, and covered it with lining from inside your "
                                     "cheek.", speaker="doctor"),
    dict(id="h7", scene="ward", text="We only do this when a normal cornea transplant can't work.", speaker="doctor"),
    dict(id="h8", scene="ward", text="So if my eye gets a cavity, should I call my dentist?", speaker="danny", gap=0.3),
    dict(id="h9", scene="ward", text="Please don't.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="They Put His TOOTH Inside His EYE… And He Could See 😳",
    alt_titles=["Tooth-In-Eye Surgery Is Real 🦷👁️", "Doctors Used a Tooth to Fix a Blind Eye 😳"],
    description="""His eyes were blind. So surgeons took one of his teeth… and put it in his eye. 🦷👁️

It's real. Tooth-in-eye surgery (osteo-odonto-keratoprosthesis) is for people blinded by severe damage to the front of the eye, when a normal cornea transplant can't work. Surgeons take a canine tooth with a little bone, fix a tiny plastic lens through it, and let it live under the skin for a few months so living tissue grows around it. Then it goes into the eye, covered with lining from inside the cheek. Most patients can see again.

(Cartoon, real medicine. Not medical advice: talk to an eye doctor about your own eyes.)

💬 Would you give up a tooth to see again? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#ToothInEye", "#BodyFacts", "#Surgery"],
    tags=["tooth in eye surgery", "osteo-odonto-keratoprosthesis", "OOKP", "tooth in eye", "weird surgery",
          "rare surgery", "blindness surgery", "cornea", "body facts", "doctor explains", "medical animation"],
    pinned_comment="A tooth inside an eye… and it WORKS. 😳 Would you do it to see again? 👇",
)

# ---------------------------------------------------------------- shared drawing
GUM, GUM_D = hexc("#e98a96"), hexc("#b85a68")
ENAMEL, ROOT, BONE = hexc("#fbf8ef"), hexc("#f0dcb0"), hexc("#e8d6b0")
LENS = hexc("#bfe6ff", 0.85)


def tooth(cr, t, x, y, s, mood="calm", talking=False, rot=0.0, bone=False, lens=0.0, shake=0.0):
    """The canine tooth as a character: pointed crown, long root; optional block of jawbone and a lens through it."""
    x += math.sin(t * 50) * shake
    with at(cr, x, y, s, rot=rot):
        if bone:
            shape(cr, rrect_pts(-62, 10, 124, 120, 26, 16), BONE, seed=1000, amp=0, lw=3.5)
            for k in range(6):
                dot(cr, -40 + 16 * k, 40 + 14 * (k % 3), 3.5, hexc("#cdb88f"))
        shape(cr, [(-30, 0), (-24, 120), (-8, 168), (8, 168), (24, 120), (30, 0)], ROOT, seed=1001, amp=0, lw=3.5)
        shape(cr, [(-46, 4), (-44, -60), (-20, -104), (0, -122), (20, -104), (44, -60), (46, 4)], ENAMEL, seed=1002,
              amp=0, lw=3.5)
        blob(cr, -18, -70, 9, 20, hexc("#ffffff", 0.9), seed=1003, amp=0, lw=0, stroke=None)
        if lens > 0:   # the clear plastic optical cylinder fixed through it
            with at(cr, 0, -10, lens):
                shape(cr, rrect_pts(-22, -34, 44, 68, 10, 10), LENS, seed=1004, amp=0, lw=3)
                blob(cr, -6, -14, 6, 12, hexc("#ffffff", 0.9), seed=1005, amp=0, lw=0, stroke=None)
        eyes(cr, 0, -52, 0.7, mood)
        mouth(cr, 0, -22, 0.6, mood, talking, t)


def eyeball(cr, t, x, y, s, mood="calm", talking=False, cloudy=1.0, fixed=0.0, look=0.0):
    """The patient's eye as a character: a big eyeball whose iris is its 'eye'; brows and a mouth on the lids.
    `cloudy` hazes the cornea; `fixed` (0..1) covers it with pink cheek lining and a clear lens window."""
    with at(cr, x, y, s):
        shape(cr, [(-250, 0), (-160, -120), (0, -160), (160, -120), (250, 0), (160, 120), (0, 160), (-160, 120)],
              SKIN, seed=1010, amp=0, lw=4)                                                       # lids
        cr.save()
        cr.new_path()
        for k in range(60):
            a = 2 * math.pi * k / 60
            px, py = 220 * math.cos(a), 118 * math.sin(a) * (1 - 0.25 * abs(math.cos(a)))
            (cr.move_to if k == 0 else cr.line_to)(px, py)
        cr.close_path()
        cr.clip()
        cr.set_source_rgba(*hexc("#fbf8ef"))
        cr.paint()
        for k in range(5):   # red veins, sore eye
            a = 0.4 + k * 1.2
            line(cr, [(200 * math.cos(a), 100 * math.sin(a)), (150 * math.cos(a + 0.1), 75 * math.sin(a + 0.15)),
                      (120 * math.cos(a), 60 * math.sin(a))], 2.5, hexc("#e06a6a", 0.8), seed=1011 + k, amp=0)
        ix = look * 30
        blob(cr, ix, 0, 92, 92, hexc("#6b4a2e"), seed=1016, amp=0, lw=3)                          # iris
        dot(cr, ix, 0, 40, hexc("#1f1a18"))                                                       # pupil
        dot(cr, ix + 22, -24, 14, WHITE)
        if cloudy > 0:   # scarred, cloudy cornea
            blob(cr, ix, 0, 104, 104, hexc("#f2f4f6", 0.85 * cloudy), seed=1017, amp=0, lw=0, stroke=None)
            for k in range(4):
                blob(cr, ix - 40 + 26 * k, -20 + 16 * (k % 2), 30, 18, hexc("#ffffff", 0.6 * cloudy), seed=1018 + k,
                     amp=0, lw=0, stroke=None)
        if fixed > 0:    # pink lining over the eye, with the tooth-lens window in the middle
            cr.push_group()
            cr.set_source_rgba(*hexc("#e98a96"))
            cr.paint()
            for k in range(7):
                line(cr, [(-220, -90 + 30 * k), (0, -80 + 30 * k), (220, -90 + 30 * k)], 2.5, hexc("#d07482"),
                     seed=1022 + k, amp=0)
            blob(cr, 0, 0, 46, 46, hexc("#f0dcb0"), seed=1030, amp=0, lw=3)                       # tooth plate rim
            dot(cr, 0, 0, 26, hexc("#1f1a18"))                                                     # the lens: dark, clear
            dot(cr, 8, -8, 7, WHITE)
            cr.pop_group_to_source()
            cr.paint_with_alpha(fixed)
        cr.restore()
        line(cr, [(-250, 0), (-160, -122), (0, -162), (160, -122), (250, 0)], 4, hexc("#2a2230"), seed=1031, amp=0)
        for k in range(7):   # lashes
            a = math.pi + 0.5 + k * 0.33
            line(cr, [(235 * math.cos(a), 150 * math.sin(a) * 0.95), (262 * math.cos(a), 178 * math.sin(a) * 0.95)],
                 4, hexc("#2a2230"), seed=1032 + k, amp=0)
        # brows and mouth make it a character
        tilt = {"worried": 0.35, "cry": 0.35, "shock": 0.0, "happy": -0.1}.get(mood, 0.1)
        for sx in (-1, 1):
            line(cr, [(sx * 60, -205 + 30 * tilt * sx), (sx * 180, -195 - 30 * tilt * sx)], 16, hexc("#3a2a1e"),
                 seed=1040 + sx, amp=0)
        mouth(cr, 0, 170, 2.0, mood, talking, t)


def mouth_scene(cr, t):
    """Inside the open mouth: dark back of the mouth, the upper lip line at the top (world: x 0..720)."""
    cr.set_source_rgba(*hexc("#5a1f2a"))
    cr.rectangle(-900, -900, 2600, 3200)
    cr.fill()
    shape(cr, [(-200, -400), (920, -400), (920, 120), (360, 170), (-200, 120)], GUM, seed=1050, amp=0, lw=4)


def lower_gum(cr, hole=False):
    """The lower gum, drawn over the roots of the bottom teeth."""
    shape(cr, [(-200, TY + 40), (360, TY + 20), (920, TY + 40), (920, 1500), (-200, 1500)], GUM, seed=1053, amp=0,
          lw=4)
    blob(cr, 360, TY + 520, 420, 200, hexc("#d4737f"), seed=1051, amp=0, lw=4)                    # tongue
    if hole:
        blob(cr, TX, TY + 40, 52, 22, hexc("#3a0f18"), seed=1080, amp=0, lw=3)


def cheek_scene(cr, t):
    """The side of the face: cheek skin (world: around x 1600..2320)."""
    cr.set_source_rgba(*hexc("#86cfdc"))
    cr.rectangle(1100, -900, 1800, 3200)
    cr.fill()
    shape(cr, [(1560, 100), (2300, 120), (2380, 700), (2280, 1300), (1560, 1300)], SKIN, seed=1060, amp=0, lw=4.5)
    blob(cr, 1700, 360, 60, 30, hexc("#ffffff"), seed=1061, amp=0, lw=3.5)                         # closed eye above
    line(cr, [(1640, 350), (1760, 350)], 4, hexc("#2a2230"), seed=1062, amp=0)
    blob(cr, 1780, 1000, 120, 26, hexc("#d9837c"), seed=1063, amp=0, lw=3.5)                       # lips


# ---------------------------------------------------------------- scenes
EX, EY = 360, 640           # the eye
TX, TY = 360, 560           # the canine in the lower gum
CX, CY = 1960, 640          # pocket in the cheek


def scene_eye(cr, t, tl, final=False):
    A = tl.at
    if final:
        keys = [(A("t8") - 0.1, (1.0, EX, 720)), (A("t8", "light"), (1.25, EX, 770))]
    else:
        keys = [(0, (1.15, EX, 770)), (A("t1", "cloudy"), (1.3, EX, 780)), (A("t2"), (1.0, 420, 680))]
    set_camera(camera(t, keys))
    enter_world(cr)
    drapes(cr)
    if final:
        mood = "shock" if t < A("t8", "light") else "happy"
        eyeball(cr, t, EX, EY, 1.0, mood, tl.speaking("eye", t), cloudy=0.0, fixed=1.0)
        if t >= A("t8", "light"):   # light gets in
            for k in range(8):
                a = k * math.pi / 4 + t * 0.6
                line(cr, [(EX + 70 * math.cos(a), EY + 70 * math.sin(a)), (EX + 120 * math.cos(a), EY + 120 * math.sin(a))],
                     6, hexc("#ffd23f"), seed=1070 + k, amp=0)
        label(cr, "Tooth + lens", 560, 390, EX + 20, EY - 20)
        label(cr, "Cheek lining", 160, 420, EX - 160, EY - 40)
        return
    mood = "worried" if t < A("t2") else "shock"
    eyeball(cr, t, EX, EY, 1.0, mood, tl.speaking("eye", t), cloudy=1.0, look=0.4 if t >= A("t2") else 0.0)
    label(cr, "Cloudy cornea", 520, 380, EX + 40, EY - 60)
    if t >= A("t2") - 0.2:   # the scalpel arrives
        u = ease_out(seg(t, A("t2") - 0.2, A("t2") + 0.4))
        scalpel(cr, t, lerp(820, 600, u), lerp(200, 300, u), 1.1, -0.5, talking=tl.speaking("scalpel", t), mood="happy")


def scene_mouth(cr, t, tl):
    A = tl.at
    pull = ease_out(seg(t, A("t3", "pulling") - 0.1, A("t3", "pulling") + 0.9))
    lens = ease_out(seg(t, A("t4", "lens") - 0.1, A("t4", "lens") + 0.5))
    keys = [(A("t3") - 0.1, (1.3, 360, 600)), (A("t3", "mouth"), (1.0, 360, 560)), (A("t4"), (1.35, 400, 470)),
            (A("t5"), (1.5, 360, 420))]
    set_camera(camera(t, keys))
    enter_world(cr)
    mouth_scene(cr, t)
    for k, x in enumerate((100, 210, 510, 620)):       # neighbours
        tooth(cr, t, x, TY + 30, 0.75, "calm" if t < A("t3") + 0.4 else "shock")
    if pull <= 0.02:
        tooth(cr, t, TX, TY, 0.9, "shock" if t >= A("t3") else "calm", tl.speaking("tooth", t))
        lower_gum(cr)
    else:
        lower_gum(cr, hole=True)
        tx, ty = TX + 20 * pull, TY - 260 * pull
        for k in range(3):
            u = (t * 1.4 + k / 3) % 1
            blob(cr, TX - 26 + 26 * k, TY + 50 + 90 * u, 6, 9, BLOOD, seed=1081 + k, amp=0, lw=2, stroke=BLOOD_D)
        mood = "shock" if t < A("t5") else ("angry" if t < A("t5", "chew") else "worried")
        tooth(cr, t, tx, ty, 0.95, mood, tl.speaking("tooth", t), bone=True, lens=lens,
              shake=1.5 if A("t5") <= t else 0)
        forceps(cr, tx + 10, ty - 110, 1.0, grip=1.0)
        if lens > 0:
            label(cr, "Plastic lens", 570, 210, tx + 10, ty - 30)
        label(cr, "Jawbone", 160, 250, tx - 40, ty + 60)
    if t < A("t4", "lens"):
        scalpel(cr, t, 620, 250, 1.0, -0.5, talking=tl.speaking("scalpel", t), mood="happy")
    if pull <= 0.02:
        label(cr, "Canine tooth", 560, 330, TX + 30, TY - 60)


def scene_cheek(cr, t, tl):
    A = tl.at
    tuck = ease_out(seg(t, A("t6", "cheek") - 0.2, A("t6", "cheek") + 0.6))
    keys = [(A("t6") - 0.1, (1.0, CX - 20, 700)), (A("t6", "cheek"), (1.25, CX, 680)), (A("t7"), (1.45, CX, 700))]
    set_camera(camera(t, keys))
    enter_world(cr)
    cheek_scene(cr, t)
    tx, ty = lerp(CX + 300, CX, tuck), lerp(CY - 500, CY, tuck)
    if tuck < 1:
        tooth(cr, t, tx, ty, 0.8, "worried", tl.speaking("tooth", t), bone=True, lens=1.0)
    else:   # under the skin: a bump with the tooth showing through
        blob(cr, CX, CY + 20, 120, 150, hexc("#f2cdb0"), seed=1090, amp=0, lw=3.5)
        cr.push_group()
        mood = "angry" if t < A("t7", "strangest") else "worried"
        tooth(cr, t, CX, CY, 0.8, mood, tl.speaking("tooth", t), bone=True, lens=1.0)
        cr.pop_group_to_source()
        cr.paint_with_alpha(0.75)
        stitches(cr, [(CX - 60 + 6 * k, CY - 160) for k in range(20)], 1.0)
        for k in range(5):   # living tissue growing around it
            a = k * 1.25 + t
            line(cr, [(CX + 90 * math.cos(a), CY + 120 * math.sin(a)), (CX + 110 * math.cos(a + 0.3),
                                                                          CY + 140 * math.sin(a + 0.3))],
                 3.5, hexc("#d9534f"), seed=1095 + k, amp=0)
        cr.save()
        cr.identity_matrix()
        months = 1 + int(2.99 * seg(t, A("t6", "few"), A("t7", end=True)))
        calendar(cr, t, 590, 380, f"MONTH {months}", A("t6", "few"))
        cr.restore()
    if tuck < 1:
        scalpel(cr, t, CX + 260, CY - 300, 1.0, -0.5, talking=tl.speaking("scalpel", t), mood="happy")
    label(cr, "Under the cheek skin", CX - 120, 260, CX - 20, CY - 80)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("h1") - 0.1, A_CLOSE), (A("h1", "eye"), TWO_SHOT),
            (A("h2"), DOC_CLOSE), (A("h3"), TWO_SHOT), (A("h4"), DOC_CLOSE), (A("h5"), TWO_SHOT),
            (A("h6"), DOC_CLOSE), (A("h7"), TWO_SHOT), (A("h8"), A_CLOSE), (A("h9"), DOC_CLOSE),
            (A("h9", "don't"), TWO_SHOT)]
    set_camera(camera(t, keys, dur=0.25))
    enter_world(cr)
    room(cr)
    x, y, s = BED_A
    bed(cr, x)
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("h1") <= t < A("h2"):
        n.update(eyes="wide", mouth="o")
    if A("h8") <= t:
        n.update(eyes="sly", mouth="smirk", arms=("point", "down"))
    if A("h9") <= t:
        n.update(eyes="wide", mouth="o", sweat=True, arms=("hold", "down"))
    patient(cr, "danny_b", x, y, s, t, talking=tl.speaking("danny", t), **n)
    with at(cr, x, y, s):   # his treated eye: pink lining with the dark lens window
        hy = -26 - 104 - 40 + 12 + math.sin(t * 2.6 + 241) * 1.6
        blob(cr, -15 + 7 * -1, hy + 2, 11, 11, hexc("#e98a96"), seed=1100, amp=0, lw=2)
        dot(cr, -15 + 7 * -1, hy + 2, 4, hexc("#1f1a18"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("h2") <= t < A("h8"):
        d.update(arms=("hold", "down"), eyes="happy" if A("h5") <= t < A("h7") else "dot")
    if A("h8") <= t < A("h9"):
        d.update(eyes="wide")
    if A("h9") <= t:
        d.update(eyes="sly")
    doctor(cr, t, talking=tl.speaking("doctor", t), **d)
    sheet(cr)
    if A("h2") <= t < A("h5"):   # the operation's names, on screen
        cr.save()
        cr.identity_matrix()
        label(cr, "Tooth-in-eye surgery", 360, 300, size=44)
        if t >= A("h3"):
            label(cr, "Osteo-odonto-keratoprosthesis", 360, 380, size=34)
        cr.restore()
        cue("pop", t, A("h2"))


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    elif name == "mouth":
        scene_mouth(cr, t, tl)
    elif name == "cheek":
        scene_cheek(cr, t, tl)
    elif name == "eye2":
        scene_eye(cr, t, tl, final=True)
    else:
        scene_eye(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr, logo=False, name="Body Facts")   # made before the logo: stays as released
