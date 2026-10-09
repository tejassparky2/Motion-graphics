"""Body Facts 15: "Your Funny Bone Isn't a BONE" — the ulnar nerve at the elbow. Script approved by the owner.

Facts (sources in research_notes/body_facts_15-18.md):
- The "funny bone" is the ulnar nerve where it runs behind the medial epicondyle (the bump on the inside of the
  elbow), close to the skin with little padding; a knock sends a shock-like tingle into the little finger and half
  of the ring finger (AAOS OrthoInfo; Cleveland Clinic).
- The name is popularly linked to the upper-arm bone, the humerus ("humorous"); that origin isn't proven, so the
  script says "Probably".
- Tingling that keeps happening without a knock can mean ulnar nerve entrapment (cubital tunnel syndrome): see a
  doctor.
"""
import math

from motion.captions import captions
from motion.clinic import A_CLOSE, B_CLOSE, DOC_CLOSE, NEXT_BED, TWO_SHOT, label, ward, watermark
from motion.engine import INK, WHITE, at, blob, cue, ease_out, hexc, lerp, line, rrect_pts, seg, shape, \
    sharp_shape, write
from motion.kit import camera, enter_world, set_camera, whip
from videos.kidney_donor import eyes, mouth

# Voices: natural stock voices at their own pitch. The doctor is Kokoro am_adam (owner: no cloned voice).
STYLE = "clean"
NARRATOR = dict(voice="am_adam", speed=0.95, cast={   # the doctor: Kokoro am_adam (Mike is am_fenrir)
    "nerve": dict(voice="am_michael", speed=0.95),
    "bone": dict(voice="am_onyx", speed=0.95),
    "mike": dict(voice="am_fenrir", speed=0.95),
    "danny": dict(voice="am_puck", speed=0.95),
})
TAIL = 1.0
EMPHASIS = {"nerve", "bone", "humerus", "humorous", "elbow", "zap", "padding", "funny", "ulnar"}

SCRIPT = [
    dict(id="f1", scene="elbow", text="Ouch! Who hit the elbow?", speaker="nerve"),
    dict(id="f2", scene="elbow", text="Don't look at me. I'm just the humerus bone.", speaker="bone"),
    dict(id="f3", scene="elbow", text="And I'm the nerve that runs right past your bump, with almost no padding.",
         speaker="nerve"),
    dict(id="f4", scene="elbow", text="So every time he bumps it, you get squished.", speaker="bone"),
    dict(id="f5", scene="elbow", text="Yes. And I send that zap all the way down to the little finger and the ring "
                                      "finger.", speaker="nerve"),
    dict(id="f6", scene="elbow", text="So why do they call it the funny bone?", speaker="bone"),
    dict(id="f7", scene="elbow", text="Probably because the bone is called the humerus. Get it? Humorous.",
         speaker="nerve"),
    dict(id="w1", scene="ward", text="Doctor, why does hitting my funny bone hurt so weird?", speaker="mike"),
    dict(id="w2", scene="ward", text="Because it isn't a bone. It's a nerve, called the ulnar nerve.",
         speaker="doctor"),
    dict(id="w3", scene="ward", text="It runs behind the bump on the inside of your elbow, with very little "
                                     "padding.", speaker="doctor"),
    dict(id="w4", scene="ward", text="When you hit it, it sends a buzz to your little finger and ring finger.",
         speaker="doctor"),
    dict(id="w5", scene="ward", text="If your fingers tingle often, even without a bump, get it checked.",
         speaker="doctor"),
    dict(id="w6", scene="ward", text="So the funny bone isn't funny, and it isn't a bone, bro.", speaker="danny",
         gap=0.3),
    dict(id="w7", scene="ward", text="Exactly. Just like your jokes.", speaker="doctor", gap=0.35),
]

METADATA = dict(
    title="Your Funny Bone Isn't a BONE 😳",
    alt_titles=["What Your Funny Bone Really Is ⚡", "Why Hitting Your Elbow Feels So Weird 😳"],
    description="""Your "funny bone" isn't a bone at all. ⚡😳

It's a nerve: the ulnar nerve. It runs behind the bump on the inside of your elbow, close to the skin with very little padding. When you knock it, it sends that weird electric buzz down to your little finger and ring finger. The name probably comes from the upper-arm bone next to it, the humerus ("humorous"). If your fingers tingle often, even without a knock, get it checked: it can be a pinched nerve.

Sources: American Academy of Orthopaedic Surgeons (OrthoInfo, "Ulnar Nerve Entrapment at the Elbow"); Cleveland Clinic, "Ulnar Nerve Entrapment".

(Cartoon, real facts. Not medical advice.)

💬 When did you last hit your funny bone? 👇

🔔 Doc and the Organs: your organs argue, then the doctor explains what's really going on.""",
    hashtags=["#FunnyBone", "#BodyFacts", "#Doctor"],
    tags=["funny bone", "ulnar nerve", "why does hitting your elbow hurt", "funny bone not a bone", "humerus",
          "body facts", "weird body facts", "nerves", "doctor explains", "medical animation"],
    pinned_comment="Be honest: did you just touch your elbow to check? 😂 👇",
)

BG = hexc("#bfe3ef")
SKIN, SKIN_D = hexc("#f2c29b"), hexc("#d89a72")
BONE, BONE_D = hexc("#f6efdf"), hexc("#d9c7a3")
NERVE, NERVE_D = hexc("#ffd23f"), hexc("#c99a12")
BUMP = (330, 660)                     # the inner elbow bump (medial epicondyle)
ARM = [(20, 520), (190, 590), (330, 660)]               # upper arm, shoulder to elbow
FORE = [(330, 660), (480, 860), (620, 1080)]             # forearm, elbow to wrist
NERVE_PATH = [(20, 590), (190, 640), (300, 700), (345, 715), (420, 800), (520, 920), (620, 1070)]


def arm(cr, t):
    """The arm in see-through cartoon style: skin outline, the humerus inside, the bump at the elbow."""
    line(cr, ARM, 170, SKIN_D, seed=2200, amp=0)
    line(cr, ARM, 160, SKIN, seed=2201, amp=0)
    line(cr, FORE, 150, SKIN_D, seed=2202, amp=0)
    line(cr, FORE, 140, SKIN, seed=2203, amp=0)
    blob(cr, *BUMP, 90, 90, SKIN, seed=2204, amp=0, lw=0, stroke=None)
    line(cr, ARM, 56, BONE_D, seed=2205, amp=0)
    line(cr, ARM, 48, BONE, seed=2206, amp=0)
    blob(cr, BUMP[0], BUMP[1], 46, 40, BONE, seed=2207, amp=0, lw=4)
    # the hand with its five fingers; the little and ring fingers glow on the zap
    with at(cr, 650, 1110, 1.0, rot=0.6):
        blob(cr, 0, 0, 70, 56, SKIN, seed=2208, amp=0, lw=4)


def fingers(cr, t, glow):
    with at(cr, 650, 1110, 1.0, rot=0.6):
        for k in range(4):
            x = -48 + 32 * k
            col = hexc("#ffe28a") if glow > 0 and k >= 2 and int(t * 10) % 2 == 0 else SKIN
            shape(cr, rrect_pts(x - 13, 40, 26, 80 - 6 * abs(k - 1.5), 12, 12), col, seed=2210 + k, amp=0, lw=3.5)


def nerve(cr, t, squish, mood, talking):
    line(cr, NERVE_PATH, 30, NERVE_D, seed=2220, amp=0)
    line(cr, NERVE_PATH, 22, NERVE, seed=2221, amp=0)
    fx, fy = 400, 770
    with at(cr, fx, fy, 1.0):
        cr.scale(1 + 0.15 * squish, 1 - 0.15 * squish)
        blob(cr, 0, 0, 56, 46, NERVE, seed=2222, amp=0, lw=4)
        eyes(cr, 0, -8, 0.7, mood)
        mouth(cr, 0, 22, 0.6, mood, talking, t)


def zap(cr, t, start, dur=1.4):
    """A spark running down the nerve from the elbow to the fingers."""
    u = seg(t, start, start + dur)
    if u <= 0 or u >= 1:
        return
    i = 3 + u * (len(NERVE_PATH) - 4)
    k = min(len(NERVE_PATH) - 2, int(i))
    f = i - k
    x = lerp(NERVE_PATH[k][0], NERVE_PATH[k + 1][0], f)
    y = lerp(NERVE_PATH[k][1], NERVE_PATH[k + 1][1], f)
    sharp_shape(cr, [(x - 10, y - 40), (x + 20, y - 6), (x + 2, y - 2), (x + 16, y + 34), (x - 20, y - 2),
                     (x - 2, y - 6)], hexc("#fff3c4"), seed=2230, amp=0, lw=3)


def scene_elbow(cr, t, tl):
    A = tl.at
    hit = ease_out(seg(t, 0.0, 0.35))
    squish = math.sin(math.pi * seg(t, 0.25, 0.85)) if t < 1.0 else 0.0
    if A("f4") <= t < A("f5"):
        squish = 0.6 + 0.2 * math.sin(t * 8)
    ELB, BONEC, HAND, WIDE = (1.4, 380, 720), (1.3, 240, 620), (1.2, 560, 960), (0.9, 330, 760)
    keys = [(0, ELB), (A("f2"), BONEC), (A("f3"), ELB), (A("f4"), BONEC), (A("f5"), WIDE), (A("f5", "little"), HAND),
            (A("f6"), BONEC), (A("f7"), WIDE)]
    set_camera(camera(t, keys))
    enter_world(cr)
    cr.set_source_rgba(*BG)
    cr.paint()
    # the table corner that hit it
    if t < 1.4:
        a = 1 - seg(t, 1.0, 1.4)
        shape(cr, [(lerp(80, 220, hit), 820), (lerp(500, 640, hit) - 200, 820), (lerp(500, 640, hit) - 200, 1400),
                   (lerp(80, 220, hit), 1400)], hexc("#8f6f4c", a), seed=2240, amp=0, lw=0, stroke=None)
    arm(cr, t)
    glow = A("f5", "zap") <= t < A("f6") or A("w4") <= t
    fingers(cr, t, glow)
    nm = "cry" if t < A("f2") else ("worried" if t < A("f5") else ("shock" if t < A("f7") else "happy"))
    nerve(cr, t, squish, nm, tl.speaking("nerve", t))
    bm = "calm" if t < A("f6") else ("worried" if t < A("f7") else "happy")
    eyes(cr, 150, 552, 0.9, bm)
    mouth(cr, 150, 590, 0.7, bm, tl.speaking("bone", t), t)
    if t < 0.9:
        for k in range(5):   # the bang
            a = 2 * math.pi * k / 5
            line(cr, [(BUMP[0] + 70 * math.cos(a), BUMP[1] + 70 * math.sin(a)),
                      (BUMP[0] + 120 * math.cos(a), BUMP[1] + 120 * math.sin(a))], 7, hexc("#ffd23f"),
                 seed=2245 + k, amp=0)
    zap(cr, t, A("f5", "zap"))
    zap(cr, t, A("f5", "little") - 0.4)
    # tags
    if A("f2") <= t < A("f4"):
        label(cr, "Humerus (upper arm bone)", 250, 420, 160, 530)
    if A("f3", "nerve") <= t < A("f5"):
        label(cr, "Ulnar nerve", 560, 640, 430, 740)
    if A("f3", "bump") <= t < A("f5"):
        label(cr, "Elbow bump", 180, 820, 300, 690)
    if A("f5", "little") <= t < A("f6"):
        label(cr, "Little + ring finger", 420, 1180, 640, 1160)
    if A("f7", "humorous") - 0.3 <= t:
        with at(cr, 360, 330, 1.0):
            shape(cr, rrect_pts(-250, -60, 500, 120, 20, 20), WHITE, seed=2250, amp=0, lw=4)
            write(cr, [("HUMERUS = HUMOROUS?", INK)], 0, 16, 44, align="center", bold=True)
        cue("pop", t, A("f7", "humorous") - 0.3)
    for w in (0.1, A("f5", "zap"), A("f5", "little")):
        cue("hit", t, w)


def scene_ward(cr, t, tl):
    A = tl.at
    keys = [(A("w1") - 0.1, A_CLOSE), (A("w1", "funny"), TWO_SHOT), (A("w2"), DOC_CLOSE), (A("w3"), TWO_SHOT),
            (A("w4"), DOC_CLOSE), (A("w5"), TWO_SHOT), (A("w6"), B_CLOSE), (A("w7"), NEXT_BED)]
    m = dict(eyes="sad", mouth="wobble", arms=("face", "down"))
    if A("w2") <= t < A("w6"):
        m.update(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w6") <= t:
        m.update(eyes="happy", mouth="grin", arms=("hold", "down"))
    n = dict(eyes="dot", mouth="smile", arms=("hold", "down"))
    if A("w6") <= t:
        n.update(eyes="happy", mouth="grin", arms=("thumb", "down"))
    if A("w7") <= t:
        n.update(eyes="wide", mouth="o", arms=("hold", "down"))
    d = dict(eyes="dot", arms=("down", "down"))
    if A("w2") <= t < A("w6"):
        d.update(arms=("hold", "down"))
    if A("w7") <= t:
        d.update(eyes="sly")
    ward(cr, t, tl, keys, m, n, d)
    cr.save()
    cr.identity_matrix()
    if A("w2", "nerve") - 0.1 <= t < A("w4"):
        label(cr, "Not a bone: the ulnar nerve", 360, 320, size=38)
        cue("pop", t, A("w2", "nerve") - 0.1)
    if A("w4") <= t < A("w5"):
        label(cr, "Buzz: little finger + ring finger", 360, 320, size=34)
    if A("w5") <= t < A("w6"):
        label(cr, "Tingling often? Get it checked.", 360, 320, size=34)
    cr.restore()


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    if name == "ward":
        scene_ward(cr, t, tl)
    else:
        scene_elbow(cr, t, tl)
    cr.restore()
    captions(cr, t, tl)
    watermark(cr)
