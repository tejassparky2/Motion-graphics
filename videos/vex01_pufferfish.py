"""Vex episode 1 (version 2, owner approved 3 Nov 2026): "Never Let a Vampire Bite a Pufferfish". A conversation in
the reference's style: Vex (motion/vex2d.py, code-drawn) asks things or does the wrong thing in cute gibberish (his
meaning in red handwriting over his head); the keeper (off screen) answers and corrects him. One close, bright shot
of the owner's living-room floor, no music, no graphics, plain comic captions for the keeper only.

Script: out/scripts_vex_ep1_v2.md. Facts: cooking doesn't destroy tetrodotoxin and there is no antidote (UMEM
Educational Pearls #2689; Hong Kong Centre for Food Safety, Food Safety Focus 178, 2021); bacteria make it and it
builds up through the food chain (Noguchi & Arakawa, Marine Drugs 2008); farmed fish carry far less but not zero (CFS
2021; Singapore Food Agency); in Japan only licensed chefs may serve it. The keeper is a male Turbo voice (never the
owner's clone) until the owner sends his own recordings.
"""
import math

import numpy as np

from motion import voice
from motion.engine import cue, ease_out, lerp, seg
from motion.polish import ellipse, paint, rrect, stroke_line
from motion.vex2d import vex
from videos import vex_kit as K

NARRATOR = dict(turbo=True)            # the keeper: the channel's usual narrator (Turbo stock female)
TAIL = 0.2                             # hard cut right after the payoff, like the reference
MUSIC = "none"
# Vex: gibberish through Turbo (so tags like [laugh] come out), then +6 st with the formants moved: ~400 Hz like Grim
voice.SPEAKERS.update({"vex": dict(voice="af_heart", speed=1.05, turbo_ref="af_heart+5", post_pitch=6, babble=True)})

SCRIPT = [   # Vex's lines are 1-3 words of baby talk, like the reference's replies (deep study, 5 Nov 2026)
    dict(id="b1", scene="floor", text="Snack? [laugh]", speaker="vex"),
    dict(id="b2", scene="floor", text="Vex, no. That's a pufferfish.", gap=0.35),
    dict(id="b3", scene="floor", text="But I'm vampire.", speaker="vex", gap=0.3),
    dict(id="b4", scene="floor", text="Don't. When it's scared, it blows up into a spiky ball.", gap=0.3),
    dict(id="b5", scene="floor", text="OW!", speaker="vex", gap=0.15),
    dict(id="b5b", scene="floor", text="Told you. [laugh]", gap=0.25),
    dict(id="b6", scene="floor", text="Ok, I cook it.", speaker="vex", gap=1.0),
    dict(id="b7", scene="floor", text="Cooking won't help. Its poison doesn't break down with heat. And there's no "
                                      "antidote.", gap=0.3),
    dict(id="b8", scene="floor", text="Poison? From where?", speaker="vex", gap=0.3),
    dict(id="b9", scene="floor", text="From its food. Tiny bacteria make it, and it builds up inside the fish.",
         gap=0.3),
    dict(id="b10", scene="floor", text="Clean one ok?", speaker="vex", gap=0.3),
    dict(id="b11", scene="floor", text="Farmed ones on clean food? Far less poison. Not zero. And they still puff up. "
                                       "[chuckle]", gap=0.3),
    dict(id="b12", scene="floor", text="I have juice. [sigh]", speaker="vex", gap=0.5),
    dict(id="b13", scene="floor", text="Uh, Vex? It's drinking your juice. [laugh]", gap=1.3),
    dict(id="b14", scene="floor", text="MY JUICE!", speaker="vex", gap=0.15),
]

METADATA = dict(
    title="Never Let a Vampire Bite a Pufferfish 🐡",
    alt_titles=["My Vampire Found a Snack. It Was a Pufferfish. 🐡", "Vex vs the Pufferfish 🐡"],
    description="""Vex is a baby vampire. He bites everything. Today he found a pufferfish. 🐡

When a pufferfish gets scared, it blows up into a spiky ball. Cooking won't help either: its poison, tetrodotoxin, doesn't break down with heat, and there's no antidote. The fish doesn't even make its own poison: tiny bacteria make it, and it builds up through its food. Farmed pufferfish carry far less, but not zero. In Japan, only licensed chefs may serve it.

Sources: UMEM Educational Pearls #2689; Hong Kong Centre for Food Safety, Food Safety Focus no. 178 (2021); Noguchi & Arakawa, "Tetrodotoxin: distribution and accumulation in aquatic organisms", Marine Drugs (2008); Singapore Food Agency, "Pufferfish 101".

Then it drank his juice. 🧃

💬 Would you eat pufferfish made by a licensed chef? Or never? 👇""",
    hashtags=["#Pufferfish", "#CuteVampire", "#Shorts"],
    tags=["pufferfish", "fugu", "tetrodotoxin", "cute vampire", "vampire cartoon", "weird animals", "animal facts",
          "funny animation", "science shorts", "interestingly strange"],
    pinned_comment="Vex wants his juice back. Would YOU eat fugu from a licensed chef, or never? 🐡👇",
)


# Layout from the deep study of the references (research_notes/vex_deep_*.md, 5 Nov 2026): toy-sized mascot
# (~226 px of 1280), the pair centred on one floor line at y~752, one locked shot, captions at y 925.
S = 0.21                              # Vex ~226 px tall
KS = S / 0.33                         # scale for offsets first laid out at S = 0.33
VX, VY = 262, 752                     # Vex's home spot (feet)
FX, FY, FR = 470, 752, 82             # the fish's water dish: the co-star about as big as Vex
HX = FX - 128                         # where he stands to bite
FS = 0.58                             # fish size
REPLY_Y = VY - 1076 * S - 45          # his lines: fixed baseline ~45 px over his head
INK = (0.11, 0.06, 0.1, 1)
_env = {}


def talk(tl, t, who="vex"):
    """Mouth opening from the loudness of his voice right now (kept small: the reference's mouths barely move)."""
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


def gulps(t, t0, t1, n=3):
    u = max(0.0, min(1.0, (t - t0) / max(0.01, t1 - t0))) * n
    k = int(u)
    return min(1.0, (k + ease_out(u - k)) / n)


def land(t, t0, k=0.9):
    d = t - t0
    return k * math.exp(-9 * d) * math.cos(16 * d) if d > 0 else 0.0


def mouth_at(x, turn, lift=0.0, sit=False):
    return x + turn * 58 * 0.9 * S, VY - lift - (492 - (110 if sit else 0)) * S


def fangs(cr, mx, my):
    for side in (-1, 1):
        fx = mx + side * 30 * S
        cr.move_to(fx - 13 * S, my)
        cr.line_to(fx + 13 * S, my)
        cr.line_to(fx, my + 44 * S)
        cr.close_path()
        paint(cr, (1, 1, 1, 1), INK, 6 * S)


def pan_prop(cr, hx, hy, ang):
    """A frying pan in his fist (body units)."""
    cr.save()
    cr.translate(hx, hy)
    cr.rotate(ang)
    rrect(cr, 30, -12, 130, 24, 10)
    paint(cr, (0.36, 0.24, 0.16, 1), INK, 8)
    ellipse(cr, 240, 0, 95, 46)
    paint(cr, (0.22, 0.22, 0.26, 1), INK, 10)
    ellipse(cr, 240, -4, 72, 32)
    paint(cr, (0.33, 0.33, 0.38, 1), None, 0)
    cr.restore()


def pan_on_floor(cr, x, y):
    cr.save()
    cr.translate(x, y)
    cr.scale(S, S)
    rrect(cr, -170, -14, 130, 24, 10)
    paint(cr, (0.36, 0.24, 0.16, 1), INK, 8)
    ellipse(cr, 60, 0, 100, 34)
    paint(cr, (0.22, 0.22, 0.26, 1), INK, 10)
    cr.restore()


def juice_box(cr, x, y, k=1.0, crumple=0.0, straw_to=None):
    """A tomato-juice box standing at (x, y) (bottom centre); straw to `straw_to` (screen px) or straight up."""
    cr.save()
    cr.translate(x, y)
    tip = (straw_to[0] - x, straw_to[1] - y) if straw_to else (10 * k, -70 * k)
    straw = [(6 * k, -60 * k * (1 - 0.35 * crumple)), (14 * k, -84 * k), tip]
    stroke_line(cr, straw, 7 * k + 1, INK, curve=False)
    stroke_line(cr, straw, 3.5 * k + 0.5, (1, 1, 1, 1), curve=False)
    cr.scale(k * (1 - 0.15 * crumple), k * (1 - 0.35 * crumple))
    rrect(cr, -22, -64, 44, 64, 7)
    paint(cr, (0.86, 0.16, 0.2, 1), INK, 4)
    rrect(cr, -15, -48, 30, 26, 5)
    paint(cr, (1, 1, 1, 1), None, 0)
    ellipse(cr, 0, -35, 8, 7)
    paint(cr, (0.92, 0.2, 0.2, 1), INK, 2)
    stroke_line(cr, [(0, -43), (4, -47)], 3, (0.3, 0.7, 0.3, 1), curve=False)
    cr.restore()


def thought(cr, t, tl):
    """b9: a thought bubble over the dish: bacteria -> worm -> fish."""
    A = tl.at
    t0, t1 = A("b9", "food"), A("b10") - 0.4
    if not (t0 <= t < t1 + 0.2):
        return
    k = ease_out(seg(t, t0, t0 + 0.3)) * (1 - seg(t, t1, t1 + 0.2))
    if k <= 0.01:
        return
    cx, cy, z = 470, 440, 0.78
    for dx, dy, r in ((FX - 30, FY - 120, 9), (FX - 26, FY - 150, 14)):
        ellipse(cr, dx, dy, r * k, r * k)
        paint(cr, (1, 1, 1, 0.95), INK, 3)
    cr.save()
    cr.translate(cx, cy)
    cr.scale(k * z, k * z)
    lobes = ((-120, 0, 70), (-50, -40, 80), (50, -40, 80), (120, 0, 70), (0, 30, 90))
    for bx, by, r in lobes:
        ellipse(cr, bx, by, r + 4, r + 4)
        paint(cr, INK, None, 0)
    for bx, by, r in lobes:
        ellipse(cr, bx, by, r, r)
        paint(cr, (1, 1, 1, 1), None, 0)
    cr.restore()
    if t >= A("b9", "bacteria"):
        K.bacteria(cr, t, cx - 120 * z, cy, 0.8 * z * ease_out(seg(t, A("b9", "bacteria"), A("b9", "bacteria") + 0.3)))
    if t >= A("b9", "builds"):
        u = ease_out(seg(t, A("b9", "builds"), A("b9", "builds") + 0.3))
        K.worm(cr, t, cx + 5 * z, cy + 5 * z, 0.6 * z * u)
        K.pufferfish(cr, t, cx + 125 * z, cy, 0.42 * z * u, facing=-1)
        stroke_line(cr, [(cx - 75 * z, cy), (cx - 50 * z, cy)], 6, (0.9, 0.2, 0.2, u), curve=False)
        stroke_line(cr, [(cx + 52 * z, cy), (cx + 78 * z, cy)], 6, (0.9, 0.2, 0.2, u), curve=False)


def dash(t, t_out, t_back, x_from, x_to):
    """The reference's prop change: dash off-screen left (0.08 s), 0.25-0.3 s of empty floor, dash back in (0.12 s).
    Returns (x or None while off screen, smear direction)."""
    if t < t_out:
        return x_from, 0
    if t < t_out + 0.08:
        return lerp(x_from, -160, (t - t_out) / 0.08), -1
    if t < t_back:
        return None, 0
    if t < t_back + 0.12:
        return lerp(-160, x_to, ease_out((t - t_back) / 0.12)), 1
    return x_to, 0


def draw(out, t, tl):
    A = tl.at
    K.photo(out, t, "close_living_ref", 0.0, push=0.0)      # one locked shot, like the reference
    layer, cr = K.world_layer()
    blink = K.auto_blink(t)
    tk = talk(tl, t)
    b = {k: A(k) for k in ("b1", "b2", "b3", "b4", "b5", "b5b", "b6", "b7", "b8", "b9", "b10", "b11", "b12", "b13",
                           "b14")}
    e = {k: A(k, end=True) for k in b}
    chomp, poke = A("b4", "scared"), b["b5"]
    grab2, freeze, puff2 = A("b11", "less"), A("b11", "Not"), A("b11", "puff")
    drop_pan = A("b7", "antidote")
    hat_out, hat_back = b["b6"] - 0.75, b["b6"] - 0.42          # dash off, come back in a chef hat with a pan
    juice_out, juice_back = e["b11"] - 0.05, b["b12"] - 0.2     # dash off, come back with a juice box
    put_down = e["b12"] + 0.25
    sneak0, slurp0 = put_down + 0.35, b["b13"] - 0.7
    slurp = seg(t, slurp0, slurp0 + 1.6)
    kd = FR / 78
    BOX = (FX - 96 * kd, VY - 2)
    straw_end = (FX - 44 * kd, FY - 30 * kd)

    # ---- the fish: in the dish, held, puffed, dropped back, deflating, drinking
    if t < poke:
        puff = gulps(t, A("b4", "blows"), A("b4", "ball", end=True)) if t >= chomp else 0.0
    elif t < b["b7"]:
        puff = 1.0
    elif t < grab2:
        puff = 1 - ease_out(seg(t, b["b7"], b["b7"] + 1.2))
    elif t < puff2:
        puff = 0.0
    elif t < slurp0:
        puff = min(1 - 0.85 * seg(t, b["b12"], put_down), ease_out(seg(t, puff2, puff2 + 0.25)))
    else:
        puff = 0.15 + 0.85 * gulps(t, slurp0, slurp0 + 1.6)
    held1 = b["b4"] + 0.6 <= t < poke
    held2 = grab2 + 0.35 <= t < puff2 + 0.25
    shake = 5 * math.sin(t * 60) if (chomp <= t < chomp + 0.25 or poke <= t < poke + 0.3 or
                                    puff2 <= t < puff2 + 0.3) else 0
    fs = FS + 0.04 * puff
    turn_bite = 0.45
    mx, my = mouth_at(HX, turn_bite)
    in_dish = (FX, FY - 27 * kd - 24 * kd * puff)

    def fish_pos():
        if held1:
            lift = ease_out(seg(t, b["b4"] + 0.6, chomp - 0.08))
            snap = seg(t, chomp - 0.06, chomp + 0.04)
            hy = lerp(my + 62 * KS, my + 24 * KS, snap)
            return lerp(FX, mx + 6 * KS, lift), lerp(FY - 27 * kd, hy, lift)
        if held2:
            lift = ease_out(seg(t, grab2 + 0.35, grab2 + 0.75))
            return lerp(FX, mx + 6 * KS, lift), lerp(FY - 27 * kd, my + 66 * KS, lift)
        if poke <= t < poke + 0.35:                 # falling back into the dish
            u = seg(t, poke, poke + 0.35)
            return lerp(mx + 6 * KS, in_dish[0], u), lerp(my + 24 * KS, in_dish[1], u * u)
        if puff2 + 0.25 <= t < puff2 + 0.6:
            u = seg(t, puff2 + 0.25, puff2 + 0.6)
            return lerp(mx + 6 * KS, in_dish[0], u), lerp(my + 66 * KS, in_dish[1], u * u)
        if t >= sneak0:                             # scoots to the dish's edge, lips on the straw
            u = ease_out(seg(t, sneak0, slurp0))
            lip = straw_end[0] + (70 + 44 * puff) * fs * 0.96
            return lerp(in_dish[0], lip, u), lerp(in_dish[1], straw_end[1] - 10 * puff, u)
        return in_dish

    def draw_fish():
        px, py = fish_pos()
        K.pufferfish(cr, t, px + shake, py, fs, puff=puff, facing=-1,
                     eyes="open" if t >= slurp0 else ("angry" if puff > 0.5 else "open"),
                     flap=not (held1 or held2), tint=ease_out(slurp))

    holding = held1 or held2
    K.dish_back(cr, FX, FY, FR, shadow=False)
    if t >= put_down:
        juice_box(cr, BOX[0], BOX[1], kd, crumple=slurp, straw_to=straw_end)
        for k in range(3):
            cue("pop", t, slurp0 + 0.15 + k * 0.5)
    if not holding:
        draw_fish()
    K.dish_front(cr, FX, FY, FR)
    if t >= drop_pan:                               # the dropped pan stays on the floor
        u = seg(t, drop_pan, drop_pan + 0.3)
        pan_on_floor(cr, lerp(VX - 10, VX - 90, u), lerp(VY - 160, VY + 22, u * u))
        cue("thud", t, drop_pan + 0.3)

    def hands_on_fish(x):
        px, py = fish_pos()
        bx, by = (px - x) / S, (py - VY) / S
        reach = (70 + 44 * puff) * fs / S + 18
        return ((-(bx - reach) + turn_bite * 25, by), (bx + reach - turn_bite * 25, by))

    def in_hands(c):
        draw_fish()
        if held1 and t >= chomp:
            fangs(c, mx + shake * 0.6, my + 4 * KS)

    kw = dict(blink=blink, idle=0.0, shadow=False)
    x = VX
    hat = False
    # ---- Vex, beat by beat: faces the camera when he talks, turns to the fish when he acts
    if t < b["b2"]:                                 # "snack?"
        kw.update(turn=0.5, look=(0.8, 0.4), eyes="sparkle", mouth="grin" if tk is None else None, talk=tk)
    elif t < b["b3"]:                               # "Vex, no. That's a pufferfish."
        glance = seg(t, A("b2", "no"), A("b2", "no") + 0.25)
        kw.update(turn=0.5 * (1 - glance), look=(0.8 * (1 - glance), 0.4 * (1 - glance)), eyes="open",
                  brows="up" if glance > 0.5 else None, mouth="smirk")
    elif t < b["b4"]:                               # "but im vampire": cape flares, claws up
        big = seg(t, b["b3"], b["b3"] + 0.25)
        kw.update(turn=0.0, eyes="angry", brows="angry", talk=tk, mouth=None if tk is not None else "smirk",
                  arms=("up", "up") if big > 0.5 else ("hips", "hips"), point=("claw", "claw"), cape=big,
                  squash=0.2 * math.sin(big * math.pi))
        cue("whoosh", t, b["b3"])
    elif t < poke:                                  # "Don't." hop over, grab it, CHOMP on "scared"
        hop = seg(t, b["b4"], b["b4"] + 0.45)
        x = lerp(VX, HX, ease_out(hop))
        biting = t >= chomp
        arms = ("up", "up") if hop < 1 else hands_on_fish(x)
        kw.update(turn=turn_bite, lift=55 * math.sin(hop * math.pi) if hop < 1 else 0,
                  legs="jump" if 0 < hop < 1 else "stand",
                  squash=0.4 * math.sin(seg(t, b["b4"] + 0.45, b["b4"] + 0.6) * math.pi),
                  eyes=("cry" if puff > 0.8 else "shocked" if puff > 0.25 else "closed") if biting else "angry",
                  brows=("up" if puff > 0.25 else None) if biting else "angry",
                  mouth="chomp" if biting else "bite", arms=arms, point=("claw", "claw"), look=(0.6, 0.5),
                  cape=0.3 if biting else 0.7, blink=0.0, held=in_hands if held1 and puff < 0.5 else None)
        cue("whoosh", t, b["b4"])
        cue("thud", t, b["b4"] + 0.45)
    elif t < hat_out:                               # "OW!" spins back, sits dizzy; "Told you."
        v = seg(t, poke, poke + 0.5)
        x = lerp(HX, VX - 20, ease_out(v))
        kw.update(rot=-2 * math.pi * ease_out(v), pivot="center", lift=100 * math.sin(v * math.pi) if v < 1 else 0,
                  legs="sit" if v >= 1 else "jump", eyes="dizzy" if v >= 1 else "cry", talk=tk,
                  mouth="wobble" if tk is None else None, arms=("up", "up") if v < 1 else ("out", "out"),
                  squash=land(t, poke + 0.5), cape=0.5, tears=v >= 1, turn=0.0)
        cue("thud", t, poke + 0.5)
    elif t < b["b7"]:                               # dashes off ... back in a chef hat with a pan: "ok i cook it"
        dx, smear = dash(t, hat_out, hat_back, VX - 20, VX)
        x = dx
        hat = t >= hat_back
        kw.update(turn=0.0 if tk is not None else 0.2, eyes="happy" if tk is not None else "sparkle", talk=tk,
                  mouth=None if tk is not None else "smirk", arms=("hips", "up"), hold=(None, pan_prop) if hat else
                  (None, None), legs="sit" if t < hat_out + 0.02 else "jump" if smear else "stand",
                  squash=land(t, hat_back + 0.12, 0.5))
        cue("whoosh", t, hat_out)
        cue("whoosh", t, hat_back)
    elif t < b["b8"]:                               # "Cooking won't help ... no antidote." pan drops
        hat = True
        shocked = t >= A("b7", "poison")
        dropped = t >= drop_pan
        kw.update(turn=0.0, eyes="shocked" if shocked else "open", brows="up" if shocked else "flat",
                  mouth="o" if dropped else ("frown" if shocked else "smirk"),
                  arms=("out", "out") if dropped else ("hips", "up"), hold=(None, None if dropped else pan_prop),
                  squash=land(t, drop_pan, 0.4) if dropped else 0)
    elif t < b["b9"]:                               # "poison?? from wer"
        hat = True
        kw.update(turn=0.0, eyes="shocked", brows="up", talk=tk, mouth=None if tk is not None else "o",
                  arms=("cheek", "cheek"))
    elif t < b["b10"]:                              # the keeper explains; Vex watches the bubble, hand on chin
        hat = True
        kw.update(turn=0.4, look=(0.7, -0.6), eyes="open", mouth="smirk", arms=("chin", "rest"), tilt=0.06)
    elif t < grab2:                                 # "clean one ok?" ... then tiptoes over to it
        hat = True
        asking = t < e["b10"] + 0.1
        w = seg(t, e["b10"] + 0.1, grab2)
        x = lerp(VX, HX, w)
        kw.update(turn=0.0 if asking else 0.5, eyes="sparkle", talk=tk, mouth=None if tk is not None else "grin",
                  legs="stand" if asking else "walk", walk=t * 14, arms=("chin", "chin") if asking else ("up", "up"),
                  point=(False, False) if asking else ("claw", "claw"))
    elif t < puff2:                                 # grabs it ... "Not zero." freezes, side-eye at the camera
        hat = True
        x = HX
        frozen = t >= freeze
        kw.update(turn=0.15 if frozen else turn_bite, look=(-0.8, 0.0) if frozen else (0.6, 0.5),
                  eyes="open" if frozen else "angry", brows="flat" if frozen else "angry",
                  mouth="smirk" if frozen else "bite", arms=hands_on_fish(x), point=("claw", "claw"), blink=0.0,
                  held=in_hands if held2 else None)
    elif t < juice_out:                             # "And they still puff up." knocked flat
        v = seg(t, puff2, puff2 + 0.45)
        x = lerp(HX, VX + 10, ease_out(v))
        kw.update(rot=-1.45 * ease_out(v), pivot="center", lift=70 * math.sin(v * math.pi) if v < 1 else 0,
                  eyes="dizzy" if v >= 1 else "cry", mouth="wobble", arms=("up", "up"),
                  squash=land(t, puff2 + 0.45, 0.5), tears=v >= 1)
        cue("thud", t, puff2 + 0.45)
    elif t < put_down:                              # dashes off, back with a juice box: "i have juice" (sigh)
        dx, smear = dash(t, juice_out, juice_back, VX + 10, VX - 5)
        x = dx
        kw.update(legs="sit" if not smear and t >= juice_back else "jump", eyes="sad", brows="sad", mouth="o",
                  arms=("front", "front"), turn=0.0,
                  held=(lambda c, x=x: juice_box(c, mouth_at(x, 0.0, sit=True)[0] + 4,
                                                 mouth_at(x, 0.0, sit=True)[1] + 82 * KS, KS * 0.9))
                  if x is not None and t >= juice_back else None)
        cue("whoosh", t, juice_out)
        cue("whoosh", t, juice_back)
    elif t < b["b14"]:                              # sets it down, sulks ... then sees the fish drinking it
        x = VX - 5
        sees = t >= A("b13", "Vex")
        shocked = t >= A("b13", "drinking")
        kw.update(legs="sit", turn=0.5 if sees else 0.0, look=(0.8, 0.3) if sees else (0.0, 0.6),
                  eyes="shocked" if shocked else ("open" if sees else "sad"), brows="up" if sees else "sad",
                  mouth="o" if shocked else "frown", arms=("cheek", "cheek") if shocked else ("down", "down"))
    else:                                           # "MY JUICE!" jumps up crying
        x = VX - 5
        j = seg(t, b["b14"], b["b14"] + 0.35)
        kw.update(lift=60 * math.sin(j * math.pi) if j < 1 else 0, legs="jump" if j < 1 else "stand",
                  squash=land(t, b["b14"] + 0.35, 0.6), turn=0.0, eyes="cry", brows="sad", tears=True,
                  talk=tk, mouth=None if tk is not None else "wobble", arms=("up", "up"), cape=0.6)
    if x is not None:
        smear = 0
        if hat_out <= t < hat_back + 0.12 or juice_out <= t < juice_back + 0.12:
            smear = -1 if (hat_out <= t < hat_out + 0.08 or juice_out <= t < juice_out + 0.08) else 1
        for g in ((2, 1) if smear else ()):         # motion smear: two fading copies behind him
            cr.push_group()
            vex(cr, t, x - smear * 38 * g, VY, S, **kw)
            cr.pop_group_to_source()
            cr.paint_with_alpha(0.28 / g)
        vex(cr, t, x + (shake * 0.6 if holding else 0), VY, S, **kw)
        if holding and puff >= 0.5:                 # fully puffed: it fills his arms, in front of everything
            in_hands(cr)
        if hat and kw.get("rot", 0) == 0:
            K.chef_hat(cr, x + kw.get("turn", 0) * 12 * S, VY - kw.get("lift", 0) - 1040 * S, 1.25 * KS)
    K.composite(out, layer)
    # effects and text over everything
    if b["b5"] + 0.5 <= t < hat_out:
        K.dizzy(out, t, VX - 20, VY - 900 * S, poke + 0.5, r=55)
    if puff2 + 0.45 <= t < juice_out:
        K.dizzy(out, t, VX - 40, VY - 260 * S, puff2 + 0.45, r=45)
    K.impact(out, t, chomp, mx + 6, my + 6, 46)
    cue("hit", t, chomp)
    K.impact(out, t, poke, mx + 4, my + 8, 40)
    K.impact(out, t, puff2, mx + 4, my + 34, 40)
    cue("hit", t, puff2)
    thought(out, t, tl)
    for bid, text in (("b1", "snack?"), ("b3", "but im vampire"), ("b5", "OWWIE"), ("b6", "ok i cook it"),
                      ("b8", "poison?? from wer"), ("b10", "clean one ok?"), ("b12", "i have juice"),
                      ("b14", "MY JUICE")):
        bb = tl.by_id[bid]
        K.ref_reply(out, t, bb.start, bb.end, x if x is not None else VX, REPLY_Y, text)
    K.ref_captions(out, t, tl, skip="vex")
