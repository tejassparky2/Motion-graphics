"""Body Facts 9: "His Brain Scan Showed HALF Was Missing…" — hemispherectomy.

Facts (kept general; sources in research_notes/body_facts_9-10.md):
- For children with severe seizures that start in one half of the brain and that medicine can't control (Rasmussen
  encephalitis, a stroke around birth, malformations of one hemisphere) (Johns Hopkins; epilepsy.com).
- That half is removed or disconnected; the space fills with cerebrospinal fluid. In young children the other half
  takes over many of its jobs (neuroplasticity).
- Johns Hopkins, 111 children (Neurology 2003): 65% seizure-free, 21% occasional non-handicapping seizures; 89% walk
  without help; 70% satisfactory spoken language. Script: "Most walk and talk afterwards", "many never have another
  seizure". The hand on the other side stays weaker (hemiparesis), stated in the script.
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, BED_A, BED_B, DOC_CLOSE, NEXT_BED, TWO_SHOT, bed, doctor, label, \
    patient, room, sheet, watermark
from motion.engine import WHITE, at, blob, cue, ease_out, hexc, lerp, line, rrect_pts, seg, shape, sharp_shape
from motion.kit import camera, enter_world, set_camera, whip
from motion.organs import PINK_A, PINK_B, skull
from motion.surgery import drapes, forceps, scalpel_tip
from videos.kidney_donor import eyes, grad_fill, mouth, scalpel

# Voices: natural stock voices at their own pitch. The doctor is Kokoro am_adam (owner: no cloned voice).
STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "good": dict(voice="af_heart", speed=0.95),
    "sick": dict(voice="am_michael", speed=0.95),
    "scalpel": dict(voice="af_bella", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"seizures", "half", "brain", "hemispherectomy", "fluid", "jobs"}

SCRIPT = [
    dict(id="s1", scene="skull", text="Sorry! I keep setting off seizures, and I can't stop!", speaker="sick"),
    dict(id="s2", scene="skull", text="He has seizures every single day. And no medicine can stop them.",
         speaker="good"),
    dict(id="s3", scene="skull", text="Then there's only one way. The sick half has to go.", speaker="scalpel"),
    dict(id="s4", scene="skull", text="Go? You're taking out half of his brain?", speaker="sick"),
    dict(id="s5", scene="skull", text="Wait. How will he walk and talk with only me?", speaker="good"),
    dict(id="s6", scene="skull", text="He's young. You'll learn to do both jobs.", speaker="scalpel"),
    dict(id="s7", scene="skull", text="Fine. But I'm getting a bigger office.", speaker="good"),
    dict(id="w1", scene="ward", text="Doctor, why is half of my brain scan empty?", speaker="mike"),
    dict(id="w2", scene="ward", text="Because you had a hemispherectomy, when you were little.", speaker="doctor"),
    dict(id="w3", scene="ward", text="One half of your brain kept causing seizures, and no medicine could stop them.",
         speaker="doctor"),
    dict(id="w4", scene="ward", text="So we took that half out. The empty space fills with fluid.", speaker="doctor"),
    dict(id="w5", scene="ward", text="In young children, the other half can take over most of its jobs.",
         speaker="doctor"),
    dict(id="w6", scene="ward", text="Most walk and talk afterwards, though one hand stays weaker.",
         speaker="doctor"),
    dict(id="w7", scene="ward", text="And many never have another seizure.", speaker="doctor"),
    dict(id="w8", scene="ward", text="So I've lived my whole life with half a brain?", speaker="mike", gap=0.3),
    dict(id="w9", scene="ward", text="Still more than me, bro.", speaker="danny", gap=0.35),
]

METADATA = dict(
    title="His Brain Scan Showed HALF Was Missing… 😳",
    alt_titles=["They Removed HALF His Brain… And He's Fine 🧠", "Living With Half a Brain Is Real 😳"],
    description="""His brain scan showed one half was simply… gone. 🧠😳

It's real. A hemispherectomy removes or disconnects one half of the brain. It's done for children whose seizures start in one half and can't be stopped with medicine. The space fills with fluid, and in young children the other half can take over most of the jobs. Most children walk and talk afterwards (one hand usually stays weaker), and many never have another seizure.

(Cartoon, real medicine. Not medical advice: talk to a doctor about your own health.)

💬 Did you know you could live with half a brain? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#Brain", "#WeirdSurgery", "#Doctor"],
    tags=["hemispherectomy", "half a brain", "brain surgery", "epilepsy surgery", "seizures", "neuroplasticity",
          "weird surgery", "rare surgery", "doctor explains", "medical animation"],
    pinned_comment="Danny says he has less than half a brain. 😂 Did you know the brain could do this? 👇",
)

BX, BY = 360, 640               # the brain, inside the open skull
PURPLE, SPARK = hexc("#9b6fd1", 0.45), hexc("#ffd23f")
FLUID, FLUID_D = hexc("#bfe6f2"), hexc("#8cc8db")


def half_pts(side, sx=1.0):
    """One half of the brain outline (side=-1 left of screen, 1 right), closed along the middle."""
    pts = []
    for k in range(61):
        a = -math.pi / 2 + math.pi * k / 60
        r = 1 + 0.035 * math.sin(a * 14)
        pts.append((side * 165 * sx * r * math.cos(a), 122 * r * math.sin(a) - 10 * max(0, -math.sin(a)) ** 3))
    pts.append((0, 112))
    pts.append((0, -132))
    return pts


def half(cr, t, side, x, y, s, mood, talking, sick=0.0, shake=0.0, sx=1.0):
    """A brain half as its own character. `sick` (0..1) tints it purple and makes it spark (seizures)."""
    x += math.sin(t * 50) * shake
    y += math.sin(t * 2.1 + side) * 3
    with at(cr, x, y, s):
        pts = half_pts(side, sx)
        grad_fill(cr, pts, PINK_A, PINK_B, side * 60, 0, 170, lw=4.5)
        if sick > 0:
            shape(cr, pts, hexc("#9b6fd1", 0.45 * sick), seed=1500, amp=0, lw=0, stroke=None)
        for k, (fx, fy, w) in enumerate([(70, -90, 46), (110, -60, 40), (130, 10, 30), (100, 70, 44), (40, 95, 34)]):
            fx = side * fx * sx
            line(cr, [(fx - w / 2, fy), (fx - w / 6, fy - 12), (fx + w / 6, fy + 8), (fx + w / 2, fy - 4)], 3.5,
                 hexc("#c75f7b"), seed=1510 + k + 10 * (side > 0), amp=0)
        blob(cr, side * 70 * sx, -76, 22, 12, hexc("#ffffff", 0.35), seed=1520, amp=0, lw=0, stroke=None)
        eyes(cr, side * 82 * sx, -14, 0.78, mood)
        mouth(cr, side * 82 * sx, 40, 0.72, mood, talking, t)
        if sick > 0.5:   # seizure sparks crackling round it
            for k in range(4):
                if int(t * 9 + k * 3) % 3 == 0:
                    continue
                a = -1.1 + 0.75 * k
                ox, oy = side * (190 * math.cos(a)), 150 * math.sin(a)
                sharp_shape(cr, [(ox, oy - 30), (ox + 14, oy - 4), (ox + 2, oy - 2), (ox + 12, oy + 28),
                                 (ox - 12, oy - 2), (ox, oy - 6)], SPARK, seed=1530 + k, amp=0, lw=3)


def fluid(cr, t, side, fill):
    """Clear fluid filling the space where the removed half was."""
    if fill <= 0:
        return
    with at(cr, BX, BY, 1.0):
        pts = half_pts(side, 1.0)
        cr.save()
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
        cr.close_path()
        cr.clip()
        top = lerp(140, -140, fill)
        shape(cr, [(-200 * side * 0, top + 6 * math.sin(t * 3)), (side * 200, top - 6 * math.sin(t * 3)),
                   (side * 200, 200), (0, 200)], FLUID, seed=1540, amp=0, lw=0, stroke=None)
        line(cr, [(0, top + 6 * math.sin(t * 3)), (side * 200, top - 6 * math.sin(t * 3))], 3, FLUID_D, seed=1541,
             amp=0)
        cr.restore()
        shape(cr, pts, None, seed=1542, amp=0, lw=3)


def scene_skull(cr, t, tl):
    A = tl.at
    lift = ease_out(seg(t, A("s6") - 0.1, A("s6", "jobs")))            # the sick half lifted out
    gone = seg(t, A("s6", "jobs"), A("s6", "jobs") + 0.4)
    fill = ease_out(seg(t, A("s6", "jobs"), A("s7") + 0.2))
    grow = ease_out(seg(t, A("s7", "bigger") - 0.1, A("s7", "office") + 0.3))
    keys = [(0, (1.15, 360, 640)), (A("s1"), (1.5, 470, 640)), (A("s2"), (1.5, 250, 640)),
            (A("s3"), (1.05, 380, 600)), (A("s4"), (1.5, 470, 640)), (A("s5"), (1.5, 250, 640)),
            (A("s6"), (1.05, 380, 600)), (A("s7"), (1.25, 330, 640))]
    set_camera(camera(t, keys))
    enter_world(cr)
    drapes(cr)
    skull(cr, BX, BY, 0.0)        # the bone ring round the opening (the cap is off-screen)
    # inside the skull: dark red behind the brain
    blob(cr, BX, BY, 250, 200, hexc("#6e2730"), seed=1550, amp=0, lw=0, stroke=None)
    fluid(cr, t, 1, fill)
    # the healthy half (left)
    gm = "worried"
    if t < A("s2"):
        gm = "shock"
    if A("s3") <= t < A("s5"):
        gm = "worried"
    if A("s5") <= t < A("s7"):
        gm = "shock"
    if A("s7") <= t:
        gm = "happy"
    half(cr, t, -1, BX - 6 + 40 * grow, BY, 1.0, gm, tl.speaking("good", t),
         shake=1.6 if t < A("s3") else 0.0, sx=1 + 0.35 * grow)
    # the sick half (right), lifted out with forceps
    if gone < 1:
        hx, hy = BX + 6 + 160 * lift, BY - 560 * lift
        sm = "cry" if t < A("s4") else "shock"
        cr.push_group()
        half(cr, t, 1, hx, hy, 1.0, sm, tl.speaking("sick", t), sick=1.0 if t < A("s6", "jobs") else 0.6,
             shake=2.0 if t < A("s3") else 0.0)
        if lift > 0:
            forceps(cr, hx + 80, hy - 60, 1.0, grip=1.0)
        cr.pop_group_to_source()
        cr.paint_with_alpha(1 - gone)
    # the scalpel watches from the side
    if t >= A("s1", "stop") - 0.3:
        ent = ease_out(seg(t, A("s1", "stop") - 0.3, A("s2") + 0.2))
        rot = 2.7
        sx, sy = lerp(900, 600, ent), 330
        if A("s3", "go") <= t < A("s4"):
            u = math.sin(math.pi * seg(t, A("s3", "go"), A("s3", "go") + 0.6))
            sx, sy = scalpel_tip(BX + 170 - 30 * u, BY - 150 + 40 * u, math.pi - 0.3, 1.0)
            rot = math.pi - 0.3
        scalpel(cr, t, sx, sy, 1.0, rot, talking=tl.speaking("scalpel", t), mood="calm")
    # tags
    if t < A("s3"):
        label(cr, "Healthy half", 190, 420, 250, 520)
        label(cr, "Sick half (seizures)", 520, 880, 460, 760)
    elif t < A("s6"):
        label(cr, "Skull", 120, 900, 150, 800)
    if A("s6", "jobs") + 0.3 <= t:
        label(cr, "Fluid", 560, 880, 470, 700)
    if A("s7", "office") <= t:
        label(cr, "One half, both jobs", 360, 420, size=30)
    for w in (A("s1"), A("s3", "go"), A("s4", "half"), A("s6", "jobs")):
        cue("hit", t, w)
    cue("whoosh", t, A("s6") + 0.1)
    cue("pop", t, A("s7", "office"))


def scan_card(cr, t, start):
    """The MRI: a head seen from above, one half of the brain grey and the other half dark (fluid)."""
    u = ease_out(seg(t, start, start + 0.3))
    if u <= 0:
        return
    with at(cr, 530, 300, 0.75 * (0.6 + 0.4 * u)):
        shape(cr, rrect_pts(-170, -150, 340, 300, 20, 20), hexc("#15171c"), seed=1560, amp=0, lw=4)
        blob(cr, 0, 6, 120, 128, hexc("#d7d9de"), seed=1561, amp=0, lw=0, stroke=None)          # skull
        blob(cr, 0, 6, 106, 114, hexc("#2a2d33"), seed=1562, amp=0, lw=0, stroke=None)
        cr.save()
        cr.rectangle(-120, -130, 120, 270)
        cr.clip()
        blob(cr, -4, 6, 96, 104, hexc("#9a9ea8"), seed=1563, amp=0, lw=0, stroke=None)     # the remaining half
        for k in range(5):
            line(cr, [(-80, -60 + 30 * k), (-50, -50 + 30 * k), (-20, -64 + 30 * k)], 3, hexc("#6d717b"),
                 seed=1564 + k, amp=0)
        cr.restore()
        line(cr, [(0, -100), (0, 112)], 3, hexc("#6d717b"), seed=1570, amp=0)
        cr.select_font_face("Anton")
        cr.set_font_size(24)
        cr.set_source_rgba(*WHITE)
        cr.move_to(-150, -118)
        cr.show_text("MRI")


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "empty"), TWO_SHOT),
            (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT), (A("w4"), DOC_CLOSE), (A("w5"), TWO_SHOT),
            (A("w6"), DOC_CLOSE), (A("w7"), TWO_SHOT), (A("w8"), A_CLOSE), (A("w9"), B_CLOSE),
            (A("w9", "bro"), NEXT_BED)]
    set_camera(camera(t, keys, dur=0.25))
    enter_world(cr)
    room(cr)
    (xa, ya, sa), (xb, yb, sb) = BED_A, BED_B
    bed(cr, xa)
    bed(cr, xb)
    m = dict(eyes="wide", mouth="o", arms=("hold", "down"))
    if A("w2") <= t < A("w5"):
        m.update(eyes="sad", mouth="wobble")
    if A("w5") <= t < A("w8"):
        m.update(eyes="happy", mouth="grin")
    if A("w8") <= t:
        m.update(eyes="wide", mouth="o", arms=("face", "down"))
    if A("w9") <= t:
        m.update(eyes="sly", mouth="smirk", arms=("hold", "down"))
    patient(cr, "mike_b", xa, ya, sa, t, talking=tl.speaking("mike", t), **m)
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w9") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    patient(cr, "danny_b", xb, yb, sb, t, talking=tl.speaking("danny", t), **n)
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w8"):
        d.update(arms=("hold", "down"), eyes="happy" if A("w7") <= t < A("w8") else "dot")
    if A("w9") <= t:
        d.update(eyes="sly")
    doctor(cr, t, talking=tl.speaking("doctor", t), **d)
    sheet(cr)
    cr.save()
    cr.identity_matrix()
    if A("w1", "scan") - 0.2 <= t < A("w2", "hemispherectomy") - 0.1 or A("w4") <= t < A("w5"):
        scan_card(cr, t, A("w1", "scan") - 0.2 if t < A("w4") else A("w4"))
        if A("w4") <= t:
            label(cr, "Fluid", 610, 440, 570, 350, size=24)
    if A("w2", "hemispherectomy") - 0.1 <= t < A("w4"):
        label(cr, "Hemispherectomy", 360, 320, size=42)
        cue("pop", t, A("w2", "hemispherectomy") - 0.1)
    cr.restore()


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_skull(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
