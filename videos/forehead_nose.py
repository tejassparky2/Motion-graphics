"""Body Facts 10: "They Glued His Forehead to His Nose… On Purpose" — the paramedian forehead flap.

Facts (kept general; sources in research_notes/body_facts_9-10.md):
- Used to rebuild moderate to large holes in the nose, most often after skin cancer is cut out (StatPearls,
  "Paramedian Forehead Flaps"; OAE Plastic and Aesthetic Research review 2025).
- A strip of forehead skin is cut and swung down onto the nose, but left attached at the brow (the pedicle), so its
  own artery (the supratrochlear artery) keeps it alive.
- The pedicle is divided after about 3 weeks (2-4 in the sources), once the nose has grown new blood vessels into
  the flap. Good colour and texture match; the forehead scar usually heals well. Script: "about three weeks".
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, BED_A, BED_B, DOC_CLOSE, NEXT_BED, TWO_SHOT, bed, doctor, label, \
    patient, room, sheet, watermark
from motion.engine import INK, at, blob, cue, ease_out, hexc, line, seg, shape
from motion.kit import camera, enter_world, set_camera, whip
from motion.organs import calendar
from motion.surgery import DRAPE, DRAPE_D, SKIN, SKIN_D, cut_line, drapes, scalpel_tip, stitches, \
    wound
from videos.kidney_donor import eyes, mouth, scalpel

# Voices: natural stock voices at their own pitch; the doctor is the owner's own cloned voice.
STYLE = "clean"
NARRATOR = dict(clone_rate=4.9, cast={
    "nose": dict(voice="am_michael", speed=0.95),
    "forehead": dict(voice="af_heart", speed=0.95),
    "scalpel": dict(voice="af_bella", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"forehead", "nose", "skin", "cancer", "flap", "weeks", "blood"}

SCRIPT = [
    dict(id="n1", scene="face", text="Hey! Where did part of me go?", speaker="nose"),
    dict(id="n2", scene="face", text="Skin cancer. We had to cut it out, and now there's a hole.", speaker="scalpel"),
    dict(id="n3", scene="face", text="Don't worry, nose. I've got plenty of skin up here.", speaker="forehead"),
    dict(id="n4", scene="face", text="Your skin? How does it get all the way down here?", speaker="nose"),
    dict(id="n5", scene="face", text="I cut a strip of forehead, and swing it down onto the nose.", speaker="scalpel"),
    dict(id="n6", scene="face", text="But I stay attached up top, so blood keeps flowing to the new skin.",
         speaker="forehead"),
    dict(id="n7", scene="face", text="So we're stuck together like this? For how long?", speaker="nose"),
    dict(id="n8", scene="face", text="About three weeks. Get comfortable.", speaker="forehead"),
    dict(id="m1", scene="ward", text="Bro, why is your forehead glued to your nose?", speaker="danny"),
    dict(id="m2", scene="ward", text="That's on purpose. This is called a forehead flap.", speaker="doctor"),
    dict(id="m3", scene="ward", text="Skin cancer took part of his nose. His forehead gave the skin to fix it.",
         speaker="doctor"),
    dict(id="m4", scene="ward", text="The strip stays attached, so its own blood supply keeps the new skin alive.",
         speaker="doctor"),
    dict(id="m5", scene="ward", text="In about three weeks, the nose grows new blood vessels. Then we cut the strip.",
         speaker="doctor"),
    dict(id="m6", scene="ward", text="The forehead heals, and the new nose matches his skin.", speaker="doctor"),
    dict(id="m7", scene="ward", text="So technically, I'm smelling with my forehead?", speaker="mike", gap=0.3),
    dict(id="m8", scene="ward", text="Technically. Yes.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="They Glued His Forehead to His Nose… On Purpose 😳",
    alt_titles=["His New Nose Came From His FOREHEAD 😳", "The Forehead Flap Is Real 👃😳"],
    description="""For three weeks, his forehead was attached to his nose. On purpose. 😳

It's real. A forehead flap is used to rebuild a nose, most often after skin cancer is cut out. Surgeons cut a strip of forehead skin and swing it down onto the nose, but leave it attached at the brow, so its own blood supply keeps it alive. After about three weeks the nose has grown new blood vessels into it, and the strip is cut. The forehead heals, and the new nose matches the skin.

(Cartoon, real medicine. Not medical advice: talk to a doctor about your own health.)

💬 Could you walk around like this for three weeks? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#ForeheadFlap", "#WeirdSurgery", "#Doctor"],
    tags=["forehead flap", "paramedian forehead flap", "nose reconstruction", "skin cancer surgery", "weird surgery",
          "rare surgery", "plastic surgery", "doctor explains", "medical animation", "body facts"],
    pinned_comment="Three weeks with your forehead stuck to your nose. 😳 Could you do it? 👇",
)

FX, FY = 360, 780                    # the patient's face on the table (oval 270 x 420)
NX, NY = 360, 850                    # the nose
HOLE = (395, 905)                    # the hole left by the cancer, on the side of the nose
PIV = (322, 680)                     # the flap's base, at the brow (it stays attached here)
STRIP_LEN, STRIP_W, PAD_R = 160, 54, 56
STRIP_PTS = [(PIV[0] - STRIP_W / 2, PIV[1]), (PIV[0] - STRIP_W / 2, PIV[1] - STRIP_LEN),
             (PIV[0] - PAD_R, PIV[1] - STRIP_LEN - PAD_R), (PIV[0], PIV[1] - STRIP_LEN - 2 * PAD_R + 10),
             (PIV[0] + PAD_R, PIV[1] - STRIP_LEN - PAD_R), (PIV[0] + STRIP_W / 2, PIV[1] - STRIP_LEN),
             (PIV[0] + STRIP_W / 2, PIV[1])]
PAD = (PIV[0], PIV[1] - STRIP_LEN - PAD_R + 4)          # the paddle's centre before it swings
SWING = math.pi - math.atan2(HOLE[0] - PIV[0], HOLE[1] - PIV[1])   # rotation that points the strip at the hole


def face(cr, t):
    """The patient asleep on the table, seen from above: hairline, brows, closed eyes, ears; drapes round the face."""
    for sx in (-1, 1):
        blob(cr, FX + sx * 272, FY - 20, 34, 70, SKIN_D, seed=1600 + sx, amp=0, lw=3.5)       # ears
    shape(cr, [(FX + 270 * math.cos(a), FY + 420 * math.sin(a)) for a in [2 * math.pi * k / 90 for k in range(90)]],
          SKIN, seed=1602, amp=0, lw=4.5)
    hair = hexc("#2b1c14")
    shape(cr, [(FX - 250, FY - 170), (FX - 200, FY - 330), (FX - 90, FY - 405), (FX + 90, FY - 405),
               (FX + 200, FY - 330), (FX + 250, FY - 170), (FX + 215, FY - 290), (FX + 110, FY - 360),
               (FX - 110, FY - 360), (FX - 215, FY - 290)], hair, seed=1603, amp=0, lw=3.5)       # hairline
    for sx in (-1, 1):
        line(cr, [(FX + sx * 60, FY - 112), (FX + sx * 110, FY - 128), (FX + sx * 165, FY - 114)], 9, hair,
             seed=1604 + sx, amp=0)                                                          # brows
        line(cr, [(FX + sx * 75, FY - 66), (FX + sx * 118, FY - 56), (FX + sx * 162, FY - 66)], 4, INK,
             seed=1606 + sx, amp=0)                                                          # closed eyes
    line(cr, [(FX - 60, FY + 290), (FX, FY + 302), (FX + 60, FY + 290)], 4, SKIN_D, seed=1608, amp=0)   # lips
    # drapes over the top of the head and the chin
    shape(cr, [(-200, FY - 330), (FX - 200, FY - 380), (FX, FY - 395), (FX + 200, FY - 380), (920, FY - 330),
               (920, -600), (-200, -600)], DRAPE, seed=1609, amp=0, lw=4)
    shape(cr, [(-200, FY + 360), (FX - 150, FY + 372), (FX, FY + 390), (FX + 150, FY + 372), (920, FY + 360),
               (920, 1800), (-200, 1800)], DRAPE, seed=1610, amp=0, lw=4)
    for k in range(5):
        line(cr, [(40 + 160 * k, FY + 410), (70 + 160 * k, FY + 520)], 4, DRAPE_D, seed=1611 + k, amp=0)


def nose_char(cr, t, mood, talking, hole, healed=0.0):
    """The nose as a character: a big rounded nose with a face; `hole` 0..1 shows the cancer cut on its side."""
    shape(cr, [(NX - 26, NY - 150), (NX + 26, NY - 150), (NX + 70, NY + 20), (NX + 96, NY + 70), (NX + 60, NY + 104),
               (NX, NY + 112), (NX - 60, NY + 104), (NX - 96, NY + 70), (NX - 70, NY + 20)], hexc("#f4d2b0"),
          seed=1620, amp=0, lw=4.5)
    for sx in (-1, 1):
        blob(cr, NX + sx * 40, NY + 88, 18, 10, hexc("#9a5a48"), seed=1621 + sx, amp=0, lw=0, stroke=None)  # nostrils
    if hole > 0 and healed < 1:
        wound(cr, t, HOLE[0], HOLE[1] - 10, 44, 36, hole, seed=40)


def nose_face(cr, t, mood, talking):
    eyes(cr, NX - 42, NY - 34, 0.62, mood)
    mouth(cr, NX - 42, NY + 2, 0.55, mood, talking, t)


def strip(cr, t, swing, cut, mood, talking, raw):
    """The forehead strip: outlined by the cut, then swung down onto the nose, still attached at the brow."""
    if swing <= 0:
        if cut > 0:
            cut_line(cr, STRIP_PTS, cut)
        return
    # the raw forehead where the strip came from
    shape(cr, STRIP_PTS, hexc("#c4544b"), seed=1630, amp=0, lw=3)
    if raw > 0:
        stitches(cr, [(PIV[0], PIV[1] - 40 - k * 12) for k in range(int(STRIP_LEN / 12) + 6)], raw)
    with at(cr, PIV[0], PIV[1], 1.0, rot=SWING * swing):
        cr.translate(-PIV[0], -PIV[1])
        shape(cr, STRIP_PTS, SKIN, seed=1631, amp=0, lw=4)
        line(cr, [(PIV[0] - STRIP_W / 2 + 8, PIV[1] - 20), (PIV[0] - STRIP_W / 2 + 8, PIV[1] - STRIP_LEN + 10)], 3,
             hexc("#c4544b"), seed=1632, amp=0)                       # its artery, keeping it alive
        with at(cr, PAD[0], PAD[1], 1.0, rot=-SWING * swing):
            eyes(cr, 0, -10, 0.6, mood)
            mouth(cr, 0, 22, 0.5, mood, talking, t)


def scene_face(cr, t, tl):
    A = tl.at
    cut = seg(t, A("n5", "cut") - 0.2, A("n5", "swing"))
    swing = ease_out(seg(t, A("n5", "swing"), A("n5", "nose") + 0.3))
    raw = seg(t, A("n7") + 0.2, A("n8"))
    NOSE, BROW, WIDE = (1.6, NX, 860), (1.5, 340, 560), (1.0, 360, 740)
    keys = [(0, (1.15, 360, 780)), (A("n1"), NOSE), (A("n2"), (1.2, 420, 760)), (A("n3"), BROW),
            (A("n4"), NOSE), (A("n5"), WIDE), (A("n6"), (1.3, 350, 720)), (A("n7"), NOSE), (A("n8"), (1.2, 360, 740))]
    set_camera(camera(t, keys))
    enter_world(cr)
    drapes(cr)
    face(cr, t)
    nm = "shock"
    if A("n2") <= t < A("n3"):
        nm = "cry"
    if A("n3") <= t < A("n5"):
        nm = "worried"
    if A("n5") <= t < A("n7"):
        nm = "shock"
    if A("n7") <= t:
        nm = "worried"
    hole = ease_out(seg(t, 0.0, 0.5))
    nose_char(cr, t, nm, tl.speaking("nose", t), hole, healed=1.0 if swing >= 1 else 0.0)
    fm = "happy" if t < A("n6") or t >= A("n8") else "calm"
    if swing <= 0:   # the forehead's face, before the strip is cut
        eyes(cr, FX - 10, FY - 250, 0.95, fm)
        mouth(cr, FX - 10, FY - 200, 0.8, fm, tl.speaking("forehead", t), t)
    strip(cr, t, swing, cut, fm, tl.speaking("forehead", t), raw)
    nose_face(cr, t, nm, tl.speaking("nose", t))
    # the scalpel: talks, then draws the strip outline
    sc = 1.05
    if A("n5", "cut") - 0.2 <= t < A("n5", "swing"):
        px, py = STRIP_PTS[min(len(STRIP_PTS) - 1, int(cut * (len(STRIP_PTS) - 1)))]
        rot = math.pi - 0.3
        sx, sy = scalpel_tip(px, py, rot, sc)
    else:
        rot, sx, sy = 2.7, 600, 480
    if t >= A("n2") - 0.3:
        scalpel(cr, t, sx, sy, sc, rot, talking=tl.speaking("scalpel", t), mood="calm")
    # three weeks
    if A("n8") <= t:
        calendar(cr, t, 570, 470, "3 WEEKS", A("n8", "three"))
    # tags
    if A("n2", "hole") <= t < A("n5"):
        label(cr, "Hole left by the cancer", 470, 1050, HOLE[0], HOLE[1] + 20)
    if A("n3") <= t < A("n5"):
        label(cr, "Forehead skin", 470, 430, FX + 40, FY - 260)
    if A("n6") <= t < A("n8"):
        label(cr, "Still attached here", 170, 560, PIV[0] - 20, PIV[1] - 10)
    for w in (A("n1"), A("n2", "hole"), A("n5", "swing"), A("n7", "stuck")):
        cue("hit", t, w)
    cue("whoosh", t, A("n5", "swing"))
    cue("scribble", t, A("n5", "cut") - 0.2, 0.6)


def face_strip(cr, x, y, s, t):
    """The flap on Mike's face in the ward: a skin bridge from his forehead to the side of his nose."""
    with at(cr, x, y, s):
        hy = -158 + math.sin(t * 2.6 + 239) * 1.6
        pts = [(4, hy - 30), (-6, hy - 22), (-16, hy - 6), (-18, hy + 10), (-10, hy + 14), (-8, hy + 4),
               (0, hy - 10), (10, hy - 24)]
        shape(cr, pts, hexc("#f2c9a4"), seed=1640, amp=0, lw=2.4)
        line(cr, [(2, hy - 26), (-11, hy - 2)], 1.4, hexc("#c4544b"), seed=1641, amp=0)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("m1") - 0.1, B_CLOSE), (A("m1", "forehead"), A_CLOSE), (A("m1", "nose"), NEXT_BED),
            (A("m2"), DOC_CLOSE), (A("m3"), TWO_SHOT), (A("m4"), A_CLOSE), (A("m5"), DOC_CLOSE),
            (A("m6"), TWO_SHOT), (A("m7"), A_CLOSE), (A("m8"), DOC_CLOSE), (A("m8", "yes"), TWO_SHOT)]
    set_camera(camera(t, keys, dur=0.25))
    enter_world(cr)
    room(cr)
    (xa, ya, sa), (xb, yb, sb) = BED_A, BED_B
    bed(cr, xa)
    bed(cr, xb)
    cut_done = t >= A("m5", "cut") + 0.2
    m = dict(eyes="sad", mouth="wobble", arms=("hold", "down"))
    if A("m2") <= t < A("m5"):
        m.update(eyes="dot", mouth="smile")
    if A("m5") <= t < A("m7"):
        m.update(eyes="happy", mouth="grin")
    if A("m7") <= t:
        m.update(eyes="wide", mouth="o", arms=("point", "down"))
    if A("m8", "yes") <= t:
        m.update(eyes="wide", mouth="o", sweat=True, arms=("hold", "down"))
    patient(cr, "mike_b", xa, ya, sa, t, talking=tl.speaking("mike", t), **m)
    if not cut_done:
        face_strip(cr, xa, ya, sa, t)
    n = dict(eyes="wide", mouth="o", arms=("point", "down"))
    if A("m2") <= t:
        n.update(eyes="dot", mouth="smile", arms=("hold", "down"))
    patient(cr, "danny_b", xb, yb, sb, t, talking=tl.speaking("danny", t), **n)
    d = dict(eyes="dot", arms=("down", "down"))
    if A("m2") <= t < A("m7"):
        d.update(arms=("hold", "down"), eyes="happy" if A("m6") <= t < A("m7") else "dot")
    if A("m8") <= t:
        d.update(eyes="sly")
    doctor(cr, t, talking=tl.speaking("doctor", t), **d)
    sheet(cr)
    cr.save()
    cr.identity_matrix()
    if A("m2", "forehead") - 0.1 <= t < A("m4"):
        label(cr, "Forehead flap", 360, 320, size=42)
        cue("pop", t, A("m2", "forehead") - 0.1)
    if A("m5", "three") <= t < A("m5", "cut"):
        calendar(cr, t, 560, 290, "3 WEEKS", A("m5", "three"))
    if A("m5", "cut") <= t < A("m6"):
        label(cr, "Strip cut. The nose has its own blood now.", 360, 320, size=30)
        cue("pop", t, A("m5", "cut"))
    cr.restore()


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_face(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
