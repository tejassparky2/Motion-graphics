"""Vex episode 2 (funny; owner, 5 Nov 2026: "Make 1 video auto approved"): "Never Give a Vampire Garlic Bread".
The keeper offers Vex garlic bread; he melts dramatically, sniffs, tries a tiny bite, loves it, eats the lot, and
faints from his own garlic breath. Reference craft (CLAUDE.md, Vex series): one locked floor shot, toy-scale Vex,
soft down-right shadows and a thick rim, coral 1-3 word replies over his head, comic captions for the keeper, no
music, hard cut on the payoff. Fact riding in the gag: garlic keeping vampires away is folklore (European vampire
legends, Bram Stoker's Dracula), said as "in old stories".
"""
import math

import numpy as np

from motion import voice
from motion.engine import cue, ease_out, lerp, seg
from motion.polish import ellipse, paint, rad, rrect, stroke_line
from motion.vex2d import vex
from videos import vex_kit as K

NARRATOR = dict(turbo=True)            # the keeper: the channel's usual narrator (Turbo stock female)
TAIL = 1.25                            # the faint lands, then a hard cut
MUSIC = "none"
voice.SPEAKERS.update({"vex": dict(voice="af_heart", speed=1.05, turbo_ref="af_heart+5", post_pitch=6, babble=True)})

SCRIPT = [
    dict(id="k1", scene="floor", text="Vex, want some garlic bread?"),
    dict(id="v1", scene="floor", text="Garlic?! [gasp]", speaker="vex", gap=0.3),
    dict(id="v2", scene="floor", text="I'm melting.", speaker="vex", gap=0.5),
    dict(id="k2", scene="floor", text="Relax. Garlic only scares vampires in old stories.", gap=0.5),
    dict(id="k3", scene="floor", text="More for me, then. [chuckle]", gap=0.3),
    dict(id="v3", scene="floor", text="Smells good?", speaker="vex", gap=1.1),
    dict(id="k4", scene="floor", text="Try a tiny bite.", gap=0.3),
    dict(id="v4", scene="floor", text="Tiny bite.", speaker="vex", gap=0.3),
    dict(id="v5", scene="floor", text="MORE!", speaker="vex", gap=1.0),
    dict(id="k4b", scene="floor", text="Vex! That was the whole plate!", gap=1.9),
    dict(id="v5b", scene="floor", text="Sorry.", speaker="vex", gap=0.3),
    dict(id="k5", scene="floor", text="Uh, Vex? Your breath. [laugh]", gap=0.5),
    dict(id="v6", scene="floor", text="Hah.", speaker="vex", gap=0.3),
]

METADATA = dict(
    title="Never Give a Vampire Garlic Bread 🧄",
    alt_titles=["My Vampire Tried Garlic Bread 🧄", "Vex vs Garlic Bread 🧄"],
    description="""Vex is a baby vampire. Today he met garlic bread. 🧄

In old vampire stories, garlic keeps vampires away. Vex has read them all. Then he smelled it.

💬 Would you share your garlic bread with a vampire? 👇""",
    hashtags=["#CuteVampire", "#GarlicBread", "#Shorts"],
    tags=["cute vampire", "vampire cartoon", "garlic bread", "vampire and garlic", "funny animation", "cute animation",
          "mascot", "funny shorts", "vex", "interestingly strange"],
    pinned_comment="Vex says the breath was worth it. Would YOU share your garlic bread with a vampire? 🧄👇",
)


S = 0.21                              # Vex ~226 px tall (reference scale)
VX, VY = 250, 752                     # Vex's home spot (feet)
PX = 488                              # the plate of garlic bread
HX = PX - 118                         # where he stands to eat
REPLY_Y = VY - 1076 * S - 45
INK = (0.11, 0.06, 0.1, 1)
CRUST, CRUMB, BUTTER, HERB = (0.80, 0.55, 0.22, 1), (0.86, 0.66, 0.32, 1), (1.0, 0.86, 0.45, 1), (0.33, 0.6, 0.2, 1)
SLICES = [(-56, -4, -0.3), (-20, -13, 0.15), (20, -9, -0.2), (56, -2, 0.28), (0, 10, 0.05)]   # x, y, angle on plate
_env = {}


def talk(tl, t, who="vex"):
    if not _env:
        for b in tl.beats:
            if b.speaker != who or b.audio is None:
                continue
            a = np.abs(np.asarray(b.audio, dtype=np.float32))
            win = int(44100 * 0.03)
            rms = np.sqrt(np.convolve(a * a, np.ones(win) / win, mode="same"))
            _env[b.id] = (b.start, rms / max(1e-6, np.percentile(rms, 95)))
    for st, env in _env.values():
        i = int((t - st) * 44100)
        if 0 <= i < len(env):
            return float(min(0.5, env[i] * 0.55))
    return None


def land(t, t0, k=0.9):
    d = t - t0
    return k * math.exp(-9 * d) * math.cos(16 * d) if d > 0 else 0.0


def slice_(cr, x, y, ang, k=1.0, bites=0):
    """One slice of garlic bread seen from above: crust, buttery middle, herbs; `bites` round bites out of its edge."""
    if k <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(ang)
    cr.scale(k, k)
    cr.push_group()
    ellipse(cr, 0, 0, 38, 17)                       # a baguette slice: crust ring, buttery crumb, herbs
    paint(cr, CRUST, INK, 3.5)
    ellipse(cr, 0, -1, 31, 11.5)
    paint(cr, BUTTER, None, 0)
    for hx, hy in ((-14, -3), (4, 2), (16, -4), (-3, -6), (-20, 3), (11, 5), (24, 1)):
        ellipse(cr, hx, hy, 2.2, 1.6)
        paint(cr, HERB, None, 0)
    ellipse(cr, -10, -5, 7, 2.5)
    paint(cr, (1, 1, 1, 0.55), None, 0)
    if bites:                                       # bite marks: scallops cut out of the end facing Vex (left)
        cr.set_operator(0)                          # CLEAR
        for j in range(bites):
            for dy in (-8, 0, 8):
                ellipse(cr, -38 + 12 * j, dy, 8, 8)
                cr.fill()
        cr.set_operator(2)                          # OVER
    cr.pop_group_to_source()
    cr.paint()
    cr.restore()


def plate(cr, x, y):
    ellipse(cr, x, y - 4, 104, 34)
    paint(cr, (0.93, 0.93, 0.95, 1), INK, 4)
    ellipse(cr, x, y - 6, 80, 24)
    paint(cr, (0.98, 0.98, 1.0, 1), (0.75, 0.75, 0.8, 1), 2.5)


def breath_cloud(cr, t, x, y, u, fade=1.0):
    """A green garlic-breath cloud growing (u 0..1) from the mouth at (x, y), drifting up and right."""
    if u <= 0.01:
        return
    cx, cy = x + 40 * u, y - 30 * u
    for dx, dy, r in ((0, 0, 30), (-24, 8, 20), (24, 6, 22), (-8, -20, 22), (16, -18, 18)):
        ellipse(cr, cx + dx * u, cy + dy * u, r * u + 3, r * u + 3)
        paint(cr, (0.18, 0.4, 0.12, 0.9 * fade), None, 0)
    for dx, dy, r in ((0, 0, 30), (-24, 8, 20), (24, 6, 22), (-8, -20, 22), (16, -18, 18)):
        ellipse(cr, cx + dx * u, cy + dy * u, r * u, r * u)
        paint(cr, (0.55, 0.82, 0.35, 0.92 * fade), None, 0)
    for j in range(3):                              # stink lines
        sx = cx - 26 + 26 * j
        pts = [(sx + 6 * math.sin(t * 9 + j + q), cy - 40 * u - q * 10) for q in range(5)]
        stroke_line(cr, pts, 4, (0.3, 0.55, 0.2, 0.9 * fade))


def crumbs(cr, t, t0, t1, x, y):
    """Crumbs flying off while he eats between t0 and t1 (each lives 0.55 s)."""
    rng = np.random.default_rng(3)
    for i in range(40):
        born = t0 + (t1 - t0) * i / 40
        a = t - born
        if not (0 <= a < 0.55):
            continue
        vx, vy = rng.uniform(-160, 160), rng.uniform(-260, -120)
        ellipse(cr, x + vx * a, y + vy * a + 900 * a * a, 3.2, 2.6)
        paint(cr, CRUMB, INK, 1.2)


def draw(out, t, tl):
    A = tl.at
    b = {bb.id: bb.start for bb in tl.beats}
    e = {bb.id: bb.end for bb in tl.beats}
    K.photo(out, t, "close_living_ref", 0.0, push=0.0)
    layer, cr = K.world_layer()
    blink = K.auto_blink(t)
    tk = talk(tl, t)

    take = A("k3", "More")                          # the keeper takes a slice
    nibble = e["v4"] + 0.1                          # his tiny bite
    eat0, eat1 = e["v5"] + 0.15, e["v5"] + 0.15 + 1.6   # he eats the lot
    faint0 = e["v6"] + 0.15

    # ---- the plate and the slices
    plate(cr, PX, VY)
    for i, (sx, sy, ang) in enumerate(SLICES):
        x, y, k, bites = PX + sx, VY - 8 + sy, 1.0, 0
        if i == 4 and t >= take:                    # lifted out of the top of the frame by the keeper's hand
            u = seg(t, take, take + 0.35)
            x, y = lerp(x, x + 60, u), lerp(y, -80, ease_out(u))
        if i == 0 and t >= nibble:
            bites = 1
        if i < 4 and t >= eat0:                     # eaten one by one: three bites each, then gone
            u = (t - eat0) / (eat1 - eat0) * 4 - i
            if u >= 1:
                continue
            if u > 0:
                bites = max(bites, 1 + int(u * 3))
        slice_(cr, x, y, ang, 1.15, bites)
    cue("crunch", t, take + 0.55)

    # ---- Vex
    kw = dict(blink=blink, idle=0.0, shadow=False, turn=0.0)
    x, melt = VX, 0.0
    if t < b["v1"]:                                 # "Vex, want some garlic bread?" he looks at the plate, curious
        look = seg(t, A("k1", "garlic"), A("k1", "garlic") + 0.3)
        kw.update(turn=0.45 * look, look=(0.8 * look, 0.4 * look), eyes="open", mouth="smirk",
                  brows="up" if look > 0.5 else None)
    elif t < b["v2"]:                               # "GARLIC??" jumps back, hands on cheeks, cape up
        j = seg(t, b["v1"], b["v1"] + 0.35)
        x = lerp(VX, VX - 40, ease_out(j))
        kw.update(lift=50 * math.sin(j * math.pi), legs="jump" if j < 1 else "stand", eyes="shocked", brows="up",
                  mouth=None if tk is not None else "o", talk=tk, arms=("cheek", "cheek"), cape=1.0 - 0.5 * j,
                  squash=land(t, b["v1"] + 0.35, 0.6))
        cue("whoosh", t, b["v1"])
    elif t < take:                                  # "im melting..." melts into a puddle; peeks at "old stories"
        x = VX - 40
        melt = ease_out(seg(t, b["v2"], b["v2"] + 1.3))
        peek = t >= A("k2", "old")
        kw.update(eyes="open" if peek else "cry", brows="sad", mouth="wobble", arms=("out", "out"), tears=not peek,
                  look=(0.0, 0.3), tilt=-0.12 * melt)
    elif t < b["v3"]:                               # "More for me, then." pops back up, watches it go ... sniffs
        x = VX - 40
        melt = 1 - ease_out(seg(t, take, take + 0.25))
        sniff1, sniff2 = e["k3"] + 0.2, e["k3"] + 0.6
        lean = 0.12 * (math.sin(seg(t, sniff1, sniff1 + 0.3) * math.pi) + math.sin(seg(t, sniff2, sniff2 + 0.3) * math.pi))
        follows = t < e["k3"]
        kw.update(eyes="shocked" if follows else "closed", brows="up", mouth="o" if follows else "smirk",
                  look=(0.3, -1.0) if follows else (0, 0), turn=0.0 if follows else 0.5, lean=lean,
                  arms=("rest", "rest"), squash=land(t, take + 0.25, 0.5))
        cue("sniff", t, sniff1)
        cue("sniff", t, sniff2)
    elif t < b["k4"]:                               # "smells good?"
        x = VX - 40
        kw.update(turn=0.5, eyes="sparkle", look=(0.8, 0.4), talk=tk, mouth=None if tk is not None else "smirk",
                  arms=("chin", "rest"), tilt=0.08)
    elif t < nibble:                                # "Try a tiny bite." tiptoes over; "tiny bite"
        w = seg(t, b["k4"], b["v4"] - 0.05)
        x = lerp(VX - 40, HX, w)
        bend = seg(t, e["v4"] - 0.1, nibble)
        kw.update(turn=0.5 if t < b["v4"] else 0.0, eyes="sparkle", talk=tk, mouth=None if tk is not None else "smirk",
                  legs="walk" if w < 1 else "stand", walk=t * 14, arms=("up", "up") if w < 1 else ("front", "front"),
                  point=("claw", "claw"), lean=0.35 * bend)
    elif t < b["v5"]:                               # the bite ... freeze ... it's GOOD
        x = HX
        savor = t < nibble + 0.6
        kw.update(turn=0.5 if savor else 0.0, lean=0.35 * (1 - seg(t, nibble + 0.1, nibble + 0.4)),
                  eyes="closed" if savor else "sparkle", mouth="chomp" if t < nibble + 0.25 else "smirk",
                  arms=("front", "front"), point=("claw", "claw"))
        cue("crunch", t, nibble)
    elif t < eat0:                                  # "MORE!"
        x = HX
        kw.update(eyes="sparkle", talk=tk, mouth=None if tk is not None else "grin", arms=("up", "up"), cape=1.0,
                  squash=0.25 * math.sin(seg(t, b["v5"], b["v5"] + 0.3) * math.pi))
    elif t < eat1:                                  # eats the lot: head down, chomp chomp chomp
        x = HX
        ph = math.sin((t - eat0) * 2 * math.pi * 4.5)
        kw.update(turn=0.5, lean=0.3 + 0.08 * ph, eyes="happy", mouth="chomp" if ph > 0 else "bite",
                  arms=("front", "front"), point=("claw", "claw"))
        for k in range(8):
            cue("crunch", t, eat0 + k * 0.2)
    elif t < b["v5b"]:                              # full and happy ... "Vex! That was the whole plate!"
        x = HX
        sat = seg(t, eat1, eat1 + 0.3)
        caught = t >= A("k4b", "whole")
        kw.update(legs="sit" if sat > 0.5 else "stand", eyes="shocked" if caught else "happy",
                  brows="up" if caught else None, mouth="o" if caught else "smirk", arms=("front", "front"),
                  squash=land(t, eat1 + 0.15, 0.5), look=(0, 0))
    elif t < b["k5"]:                               # "sorry" guilty, hands together, head tilted
        x = HX
        kw.update(legs="sit", eyes="sad", brows="sad", talk=tk, mouth=None if tk is not None else "frown",
                  arms=("chin", "chin"), tilt=-0.12)
    elif t < b["v6"]:                               # "Uh, Vex? Your breath."
        x = HX
        sat = 1.0
        puzzled = t >= A("k5", "breath")
        kw.update(legs="sit", eyes="open" if puzzled else "happy",
                  brows="up" if puzzled else None, mouth="smirk", arms=("front", "front") if not puzzled else
                  ("chin", "front"), tilt=0.1 if puzzled else 0)
    elif t < faint0:                                # "hah." breathes into his hand
        x = HX
        kw.update(legs="sit", eyes="open", talk=tk, mouth=None if tk is not None else "open", arms=("chin", "front"))
    else:                                           # knocked out by his own breath
        x = HX
        f = seg(t, faint0 + 0.25, faint0 + 0.7)
        kw.update(legs="sit", eyes="dizzy", mouth="wobble", arms=("out", "out"), rot=-1.45 * ease_out(f),
                  pivot="center", squash=land(t, faint0 + 0.7, 0.6))
        cue("thud", t, faint0 + 0.7)
    if melt > 0.01:
        cr.save()
        cr.translate(x, VY)
        cr.scale(1 + 0.45 * melt, 1 - 0.62 * melt)
        cr.translate(-x, -VY)
        vex(cr, t, x, VY, S, **kw)
        cr.restore()
    else:
        vex(cr, t, x, VY, S, **kw)
    K.composite(out, layer)

    # ---- effects and text
    if eat0 <= t < eat1 + 0.6:
        crumbs(out, t, eat0, eat1, x + 48, VY - 70)
    mx, my = x + 6, VY - (492 - 110) * S
    if t >= e["v6"] - 0.15:
        g = ease_out(seg(t, e["v6"] - 0.15, e["v6"] + 0.45))
        breath_cloud(out, t, mx, my, g)
        cue("poof", t, e["v6"] - 0.15)
    if t >= faint0 + 0.7:
        K.dizzy(out, t, x - 40, VY - 60, faint0 + 0.7, r=45)
    for bid, text in (("v1", "GARLIC??"), ("v2", "im melting..."), ("v3", "smells good?"), ("v4", "tiny bite"),
                      ("v5", "MORE"), ("v5b", "sory"), ("v6", "hah")):
        bb = tl.by_id[bid]
        K.ref_reply(out, t, bb.start, bb.end, x, REPLY_Y, text)
    K.ref_captions(out, t, tl, skip="vex")
