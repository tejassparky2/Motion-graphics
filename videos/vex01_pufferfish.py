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
TAIL = 0.6
MUSIC = "none"
# Vex: gibberish through Turbo (so tags like [laugh] come out), then +6 st with the formants moved: ~400 Hz like Grim
voice.SPEAKERS.update({"vex": dict(voice="af_heart", speed=1.05, turbo_ref="af_heart+5", post_pitch=6, babble=True)})

SCRIPT = [
    dict(id="b1", scene="floor", text="Snack? [laugh]", speaker="vex"),
    dict(id="b2", scene="floor", text="Vex, no. That's a pufferfish.", gap=0.5),
    dict(id="b3", scene="floor", text="I'm a vampire. I bite everything.", speaker="vex"),
    dict(id="b4", scene="floor", text="Don't. When it's scared, it blows up into a spiky ball."),
    dict(id="b5", scene="floor", text="OW!", speaker="vex", gap=0.15),
    dict(id="b6", scene="floor", text="Then I'll cook it first.", speaker="vex", gap=1.4),
    dict(id="b7", scene="floor", text="Cooking won't help. Its poison doesn't break down with heat. And there's no "
                                      "antidote."),
    dict(id="b8", scene="floor", text="Poison? Where does a tiny fish get poison?", speaker="vex"),
    dict(id="b9", scene="floor", text="From its food. Tiny bacteria make it, and it builds up inside the fish."),
    dict(id="b10", scene="floor", text="So a fish with clean food is safe to bite!", speaker="vex"),
    dict(id="b11", scene="floor", text="Farmed ones carry far less. Not zero. And they still puff up. [chuckle]",
         gap=0.3),
    dict(id="b12", scene="floor", text="I'll have juice. [sigh]", speaker="vex", gap=0.6),
    dict(id="b13", scene="floor", text="Uh, Vex? It's drinking your juice. [laugh]", gap=1.3),
    dict(id="b14", scene="floor", text="MY JUICE! [sniff]", speaker="vex", gap=0.2),
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


VX, VY, S = 205, 742, 0.33           # Vex's home spot
HX = 355                              # where he stands to bite
FX, FY, FR = 480, 742, 78             # the fish's water dish
INK = (0.11, 0.06, 0.1, 1)
_env = {}


def talk(tl, t, who="vex"):
    """Mouth opening 0..1 from the loudness of his voice right now; None when he isn't speaking."""
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
            return float(min(1.0, env[i] * 1.1))
    return None


def gulps(t, t0, t1, n=3):
    u = max(0.0, min(1.0, (t - t0) / max(0.01, t1 - t0))) * n
    k = int(u)
    return min(1.0, (k + ease_out(u - k)) / n)


def land(t, t0, k=0.9):
    d = t - t0
    return k * math.exp(-9 * d) * math.cos(16 * d) if d > 0 else 0.0


def mouth_at(x, turn, lift=0.0):
    return x + turn * 58 * 0.9 * S, VY - lift - 492 * S


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


def pan_on_floor(cr, x, y, k=1.0):
    cr.save()
    cr.translate(x, y)
    cr.scale(S * k, S * k)
    K.floor_shadow(cr, 60, 6, 120, 0.3)
    rrect(cr, -170, -14, 130, 24, 10)
    paint(cr, (0.36, 0.24, 0.16, 1), INK, 8)
    ellipse(cr, 60, 0, 100, 34)
    paint(cr, (0.22, 0.22, 0.26, 1), INK, 10)
    cr.restore()


def juice_box(cr, mx, my, sip):
    bx, by = mx + 6, my + 70
    stroke_line(cr, [(bx + 8, by - 40), (mx + 4, my + 6)], 7, INK, curve=False)          # straw
    stroke_line(cr, [(bx + 8, by - 40), (mx + 4, my + 6)], 4, (1, 1, 1, 1), curve=False)
    rrect(cr, bx - 26, by - 40, 52, 74, 8)
    paint(cr, (0.86, 0.16, 0.2, 1), INK, 4)
    rrect(cr, bx - 18, by - 22, 36, 30, 5)
    paint(cr, (1, 1, 1, 1), None, 0)
    ellipse(cr, bx, by - 7, 10, 9)
    paint(cr, (0.92, 0.2, 0.2, 1), INK, 2)
    stroke_line(cr, [(bx, by - 16), (bx + 4, by - 20)], 3, (0.3, 0.7, 0.3, 1), curve=False)
    if sip:                                         # little sip bubbles
        for k in range(2):
            ellipse(cr, mx + 22 + 8 * k, my - 6 - ((sip * 2 + k * 0.5) % 1.0) * 20, 4, 4)
            cr.set_source_rgba(1, 1, 1, 0.8)
            cr.fill()


def thought(cr, t, tl):
    """b9: a thought bubble over the dish: bacteria -> worm -> fish."""
    A = tl.at
    t0, t1 = A("b9", "food"), A("b10") + 0.2
    if not (t0 <= t < t1 + 0.25):
        return
    k = ease_out(seg(t, t0, t0 + 0.3)) * (1 - seg(t, t1, t1 + 0.25))
    if k <= 0.01:
        return
    cx, cy = 450, 470
    for i, (dx, dy, r) in enumerate(((440, 640, 12), (445, 600, 18))):
        ellipse(cr, dx, dy, r * k, r * k)
        paint(cr, (1, 1, 1, 0.95), INK, 4)
    cr.save()
    cr.translate(cx, cy)
    cr.scale(k, k)
    for bx, by, r in ((-120, 0, 70), (-50, -40, 80), (50, -40, 80), (120, 0, 70), (0, 30, 90)):
        ellipse(cr, bx, by, r, r)
        paint(cr, (1, 1, 1, 0.97), None, 0)
    for bx, by, r in ((-120, 0, 70), (-50, -40, 80), (50, -40, 80), (120, 0, 70), (0, 30, 90)):
        cr.save()
        ellipse(cr, bx, by, r, r)
        cr.set_source_rgba(*INK)
        cr.set_line_width(4)
        cr.stroke()
        cr.restore()
    for bx, by, r in ((-120, 0, 66), (-50, -40, 76), (50, -40, 76), (120, 0, 66), (0, 30, 86)):
        ellipse(cr, bx, by, r, r)
        paint(cr, (1, 1, 1, 1), None, 0)
    cr.restore()
    if t >= A("b9", "bacteria"):
        K.bacteria(cr, t, cx - 120, cy, 0.8 * ease_out(seg(t, A("b9", "bacteria"), A("b9", "bacteria") + 0.3)))
    if t >= A("b9", "builds"):
        u = ease_out(seg(t, A("b9", "builds"), A("b9", "builds") + 0.3))
        K.worm(cr, t, cx + 5, cy + 5, 0.6 * u)
        K.pufferfish(cr, t, cx + 125, cy, 0.42 * u, facing=-1)
        stroke_line(cr, [(cx - 75, cy), (cx - 50, cy)], 6, (0.9, 0.2, 0.2, u), curve=False)
        stroke_line(cr, [(cx + 52, cy), (cx + 78, cy)], 6, (0.9, 0.2, 0.2, u), curve=False)


def draw(cr, t, tl):
    A = tl.at
    K.photo(cr, t, "close_living", 0.0, push=0.04, dur=40, focus=(380, 700))
    blink = K.auto_blink(t)
    tk = talk(tl, t)
    b = {k: A(k) for k in ("b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8", "b9", "b10", "b11", "b12", "b13",
                           "b14")}
    put_down = A("b12", end=True) + 0.25          # he sets the juice box on the floor ...
    sneak0, slurp0 = put_down + 0.35, b["b13"] - 0.7   # ... the fish sneaks over and drinks it
    slurp = seg(t, slurp0, slurp0 + 1.6)
    BOX = (382, VY - 2)
    straw_end = (436, FY - 36)                     # a bendy straw from the box down into the fish's lips
    chomp, poke = A("b4", "scared"), b["b5"]
    grab2, freeze, puff2 = b["b11"], A("b11", "Not"), A("b11", "puff")
    drop_pan = A("b7", "antidote")
    hat_on = b["b6"] - 0.35

    # ---- the fish: in the dish, held, puffed, dropped back, deflating
    if t < poke:
        puff = gulps(t, A("b4", "blows"), A("b4", "ball", end=True)) if t >= chomp else 0.0
    elif t < b["b7"]:
        puff = 1.0
    elif t < grab2:
        puff = 1 - ease_out(seg(t, b["b7"], b["b7"] + 1.2))
    elif t < puff2:
        puff = 0.0
    elif t < slurp0:
        puff = 1 - 0.85 * seg(t, b["b12"], put_down)
        puff = min(puff, ease_out(seg(t, puff2, puff2 + 0.25)))
    else:                                         # drinking his juice: gulp, gulp, gulp, and it turns tomato red
        puff = 0.15 + 0.85 * gulps(t, slurp0, slurp0 + 1.6)
    held1 = b["b4"] + 0.6 <= t < poke
    held2 = grab2 + 0.5 <= t < puff2 + 0.25
    shake = 5 * math.sin(t * 60) if (chomp <= t < chomp + 0.25 or poke <= t < poke + 0.3 or
                                    puff2 <= t < puff2 + 0.3) else 0
    fs = 0.55 + 0.05 * puff

    K.dish_back(cr, FX, FY, FR)
    turn_bite = 0.45
    mx, my = mouth_at(HX, turn_bite)
    in_dish = (FX, FY - 34 - 30 * puff)

    def fish_pos():
        if held1:
            lift = ease_out(seg(t, b["b4"] + 0.6, chomp - 0.08))
            snap = seg(t, chomp - 0.06, chomp + 0.04)
            hy = lerp(my + 62, my + 24, snap)
            return lerp(FX, mx + 6, lift), lerp(FY - 34, hy, lift)
        if held2:
            lift = ease_out(seg(t, grab2 + 0.5, grab2 + 0.9))
            return lerp(FX, mx + 6, lift), lerp(FY - 34, my + 66, lift)
        if poke <= t < poke + 0.35:                 # falling back into the dish
            u = seg(t, poke, poke + 0.35)
            return lerp(mx + 6, in_dish[0], u), lerp(my + 24, in_dish[1], u * u)
        if puff2 + 0.25 <= t < puff2 + 0.6:
            u = seg(t, puff2 + 0.25, puff2 + 0.6)
            return lerp(mx + 6, in_dish[0], u), lerp(my + 66, in_dish[1], u * u)
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
    if t >= put_down:                               # the juice box on the floor, crumpling as it's drunk
        cr.save()
        cr.translate(*BOX)
        cr.scale(1 - 0.15 * slurp, 1 - 0.35 * slurp)
        K.floor_shadow(cr, 0, 2, 34, 0.3)
        straw = [(6, -60), (14, -92), (straw_end[0] - BOX[0] - 6, straw_end[1] - BOX[1])]
        stroke_line(cr, straw, 8, INK, curve=False)
        stroke_line(cr, straw, 4, (1, 1, 1, 1), curve=False)
        rrect(cr, -22, -64, 44, 64, 7)
        paint(cr, (0.86, 0.16, 0.2, 1), INK, 4)
        rrect(cr, -15, -48, 30, 26, 5)
        paint(cr, (1, 1, 1, 1), None, 0)
        ellipse(cr, 0, -35, 8, 7)
        paint(cr, (0.92, 0.2, 0.2, 1), INK, 2)
        cr.restore()
        for k in range(3):
            cue("pop", t, slurp0 + 0.15 + k * 0.5)
    if not holding:
        draw_fish()
    K.dish_front(cr, FX, FY, FR)
    if t >= drop_pan:                               # the dropped pan stays on the floor
        u = seg(t, drop_pan, drop_pan + 0.3)
        pan_on_floor(cr, lerp(250, 150, u), lerp(560, VY + 30, u * u), 1.0)
        cue("thud", t, drop_pan + 0.3)

    def hands_on_fish(x):
        px, py = fish_pos()
        bx, by = (px - x) / S, (py - VY) / S
        reach = (70 + 44 * puff) * fs / S + 18
        return ((-(bx - reach) + turn_bite * 25, by), (bx + reach - turn_bite * 25, by))

    def in_hands(c):
        draw_fish()
        if held1 and t >= chomp:
            fangs(c, mx + shake * 0.6, my + 4)

    hat_x, hat_y, show_hat = None, None, hat_on <= t < puff2 + 0.2
    kw = dict(blink=blink)
    x = VX
    # ---- Vex, beat by beat
    if t < b["b2"]:                                 # "Snack?"
        x = VX
        kw.update(turn=0.5, look=(0.8, 0.4), eyes="sparkle", brows=None, mouth="grin" if tk is None else None,
                  talk=tk, lean=0.06)
    elif t < b["b3"]:                               # "Vex, no. That's a pufferfish."
        glance = seg(t, A("b2", "pufferfish"), A("b2", "pufferfish") + 0.3)
        kw.update(turn=0.4 * glance, look=(0.8 * glance, 0.2 * glance), eyes="open", mouth="smirk",
                  squash=0.15 * math.sin(seg(t, b["b2"], b["b2"] + 0.3) * math.pi))
    elif t < b["b4"]:                               # "I'm a vampire. I bite everything."
        big = seg(t, A("b3", "vampire") - 0.1, A("b3", "vampire") + 0.15)
        claws = t >= A("b3", "bite")
        kw.update(turn=0.1, eyes="angry", brows="angry", talk=tk, mouth=None if tk is not None else "smirk",
                  arms=("up", "up") if claws else (("out", "out") if big > 0.5 else ("hips", "hips")),
                  point=("claw", "claw") if claws else (False, False), cape=big, tilt=-0.05)
    elif t < poke:                                  # "Don't." hop over, grab it, CHOMP on "scared"
        hop = seg(t, b["b4"], b["b4"] + 0.45)
        x = lerp(VX, HX, ease_out(hop))
        biting = t >= chomp
        arms = ("up", "up") if hop < 1 else hands_on_fish(x)
        kw.update(turn=turn_bite, lift=70 * math.sin(hop * math.pi) if hop < 1 else 0,
                  legs="jump" if 0 < hop < 1 else "stand", squash=0.4 * math.sin(seg(t, b["b4"] + 0.45,
                                                                                      b["b4"] + 0.6) * math.pi),
                  eyes=("cry" if puff > 0.8 else "shocked" if puff > 0.25 else "closed") if biting else "angry",
                  brows=("up" if puff > 0.25 else None) if biting else "angry",
                  mouth="chomp" if biting else "bite", arms=arms, point=("claw", "claw"), look=(0.6, 0.5),
                  cape=0.3 if biting else 0.7, blink=0.0,
                  held=in_hands if held1 and puff < 0.5 else None)
    elif t < hat_on:                                # "OW!" spin back, sit, dizzy
        v = seg(t, poke, poke + 0.5)
        x = lerp(HX, 190, ease_out(v))
        kw.update(rot=-2 * math.pi * ease_out(v), pivot="center", lift=130 * math.sin(v * math.pi) if v < 1 else 0,
                  legs="sit" if v >= 1 else "jump", eyes="dizzy" if v >= 1 else "cry", talk=tk,
                  mouth="wobble" if tk is None else None, arms=("up", "up") if v < 1 else ("out", "out"),
                  squash=land(t, poke + 0.5), cape=0.5, tears=v >= 1)
    elif t < b["b7"]:                               # "Then I'll cook it first." chef hat + pan
        pop = seg(t, hat_on, hat_on + 0.35)
        x = 190
        kw.update(turn=0.2, lift=60 * math.sin(pop * math.pi) if pop < 1 else 0, squash=land(t, hat_on + 0.35, 0.6),
                  eyes="happy" if tk is not None else "sparkle", talk=tk, mouth=None if tk is not None else "smirk",
                  arms=("hips", "up"), hold=(None, pan_prop))
    elif t < b["b8"]:                               # "Cooking won't help ... no antidote." smile fades, pan drops
        x = 190
        shocked = t >= A("b7", "poison")
        dropped = t >= drop_pan
        kw.update(turn=0.1, eyes="shocked" if shocked else "open", brows="up" if shocked else "flat",
                  mouth="o" if dropped else ("frown" if shocked else "smirk"),
                  arms=("out", "out") if dropped else ("hips", "up"), hold=(None, None if dropped else pan_prop),
                  squash=land(t, drop_pan, 0.4) if dropped else 0)
    elif t < b["b9"]:                               # "Poison? Where does a tiny fish get poison?"
        x = 190
        think = t >= A("b8", "Where")
        kw.update(turn=0.3 if think else 0, eyes="shocked" if not think else "open", brows="up" if not think else "flat",
                  talk=tk, mouth=None if tk is not None else "o", look=(0.6, 0.2) if think else (0, 0),
                  arms=("chin", "hips") if think else ("cheek", "cheek"), tilt=0.08 if think else 0)
    elif t < b["b10"]:                              # the keeper explains; Vex watches the bubble, nodding
        x = 190
        kw.update(turn=0.35, look=(0.7, -0.6), eyes="open", mouth="smirk", arms=("chin", "rest"),
                  tilt=0.05 * math.sin(t * 6))
    elif t < grab2:                                 # "So a fish with clean food is safe to bite!" tiptoes over
        w = seg(t, b["b10"], A("b10", end=True) + 0.1)
        x = lerp(190, HX, w)
        kw.update(turn=0.5, eyes="sparkle", talk=tk, mouth=None if tk is not None else "grin", legs="walk",
                  walk=t * 14, arms=("up", "up"), point=("claw", "claw"), lean=0.05)
    elif t < puff2:                                 # "Farmed ones ... far less. Not zero." grabs it, freezes
        x = HX
        frozen = t >= freeze
        kw.update(turn=turn_bite if not frozen else 0.15, look=(-0.8, 0.0) if frozen else (0.6, 0.5),
                  eyes="open" if frozen else "angry", brows="flat" if frozen else "angry",
                  mouth="smirk" if frozen else "bite", arms=hands_on_fish(x), point=("claw", "claw"), blink=0.0,
                  held=in_hands if held2 else None)
    elif t < b["b12"] - 0.35:                       # "And they still puff up." knocked flat
        v = seg(t, puff2, puff2 + 0.45)
        x = lerp(HX, 230, ease_out(v))
        kw.update(rot=-1.45 * ease_out(v), pivot="center", lift=80 * math.sin(v * math.pi) if v < 1 else 0,
                  eyes="dizzy" if v >= 1 else "cry", mouth="wobble", arms=("up", "up"), squash=land(t, puff2 + 0.45, 0.5),
                  tears=v >= 1)
    elif t < put_down:                              # "I'll have juice." sulking, sipping
        x = 250
        kw.update(legs="sit", eyes="sad", brows="sad", mouth="o", arms=("front", "front"), turn=0.0,
                  held=lambda c, x=x: juice_box(c, mouth_at(x, 0.0)[0], mouth_at(x, 0.0)[1] + 110 * S, t))
    elif t < b["b14"]:                              # sets it down, sulks ... then sees the fish drinking it
        x = 250
        sees = t >= A("b13", "Vex")
        shocked = t >= A("b13", "drinking")
        kw.update(legs="sit", turn=0.5 if sees else 0.0, look=(0.8, 0.3) if sees else (0.0, 0.6),
                  eyes="shocked" if shocked else ("open" if sees else "sad"), brows="up" if sees else "sad",
                  mouth="o" if shocked else "frown", arms=("cheek", "cheek") if shocked else ("down", "down"))
    else:                                           # "MY JUICE!" jumps up, crying
        x = 250
        j = seg(t, b["b14"], b["b14"] + 0.4)
        kw.update(lift=70 * math.sin(j * math.pi) if j < 1 else 0, legs="jump" if j < 1 else "stand",
                  squash=land(t, b["b14"] + 0.4, 0.6), turn=0.4, eyes="cry", brows="sad", tears=True,
                  talk=tk, mouth=None if tk is not None else "wobble", arms=("up", "up"), cape=0.6)
    vex(cr, t, x + (shake * 0.6 if holding else 0), VY, S, **kw)
    if holding and puff >= 0.5:                     # fully puffed: it fills his arms, in front of everything
        in_hands(cr)
    if show_hat and kw.get("rot", 0) == 0:
        K.chef_hat(cr, x + kw.get("turn", 0) * 12 * S, VY - kw.get("lift", 0) - 1040 * S,
                   1.25 * ease_out(seg(t, hat_on, hat_on + 0.3)))
    if b["b5"] <= t < hat_on and t >= poke + 0.5:
        K.dizzy(cr, t, 190, VY - 1000 * S + 20, poke + 0.5, r=80)
    if puff2 + 0.45 <= t < b["b12"] - 0.35:
        K.dizzy(cr, t, 150, VY - 300 * S, puff2 + 0.45, r=70)
    K.impact(cr, t, chomp, mx + 8, my + 8, 70)
    cue("hit", t, chomp)
    K.impact(cr, t, poke, mx + 6, my + 10, 60)
    K.impact(cr, t, puff2, mx + 6, my + 50, 60)
    thought(cr, t, tl)
    K.grain(cr)
    for bid, text in (("b1", "snack?"), ("b3", "i'm a vampire. i bite everything."), ("b5", "OW!"),
                      ("b6", "then i'll cook it first"), ("b8", "poison?? where does a tiny fish get poison?"),
                      ("b10", "so a fish with clean food is safe to bite!"), ("b12", "i'll have juice."),
                      ("b14", "MY JUICE!")):
        bb = tl.by_id[bid]
        lift_sub = 55 if bid in ("b6", "b8", "b10") else 0            # clear of the chef hat
        K.reply(cr, t, bb.start, bb.end + 0.7, x, VY - 1110 * S - lift_sub + (110 * S if bid == "b12" else 0), text,
                size=50 if len(text) > 26 else 58, font="Comic Neue")
    K.comic_captions(cr, t, tl, skip="vex", y=880, size=54, line_chars=21)
