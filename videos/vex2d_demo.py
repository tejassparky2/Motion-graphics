"""Demo (3 Nov 2026, owner: "Create 2.5d or 2d mascot yourself which you can animate yourself"): the opening of Vex
episode 1 played by the fully code-drawn Vex (motion/vex2d.py) in the reference's style: one close bright floor shot,
no music, no overlays, plain comic captions, Vex's lines as red handwriting, lip sync from the loudness of his voice."""
import math

import numpy as np

from motion import voice
from motion.engine import cue, ease_out, lerp, seg
from motion.vex2d import vex
from videos import vex_kit as K

NARRATOR = dict(turbo=True)
TAIL = 0.6
MUSIC = "none"
voice.SPEAKERS.update({"vex": dict(voice="af_heart", speed=1.12, pitch=11, formant="shifted", babble=True)})   # cute gibberish ~400 Hz like Grim; the red subtitles carry the meaning

SCRIPT = [
    dict(id="v1", scene="floor", text="Vex, try and bite this pufferfish."),
    dict(id="v2", scene="floor", text="Easy. I'm a vampire.", speaker="vex"),
    dict(id="v3", scene="floor", text="When a pufferfish gets scared, it gulps water and blows up into a spiky ball."),
    dict(id="v4", scene="floor", text="Ow! It poked me!", speaker="vex"),
]

VX, VY, S = 205, 742, 0.33
FX, FY, FR = 480, 740, 78             # the pufferfish's water dish
THETA = 1.25                          # dive angle that puts his jaws on the fish (see bite geometry below)
_env = {}


def talk(tl, t, who="vex"):
    """Mouth opening 0..1 from the loudness of `who`'s voice right now (30 ms windows), 0 when silent."""
    if not _env:
        for b in tl.beats:
            if b.speaker != who or b.audio is None:
                continue
            a = np.abs(np.asarray(b.audio, dtype=np.float32))
            win = int(44100 * 0.03)
            rms = np.sqrt(np.convolve(a * a, np.ones(win) / win, mode="same"))
            _env[b.id] = (b.start, rms / max(1e-6, np.percentile(rms, 95)))
    for bid, (st, env) in _env.items():
        i = int((t - st) * 44100)
        if 0 <= i < len(env):
            return float(min(1.0, env[i] * 1.1))
    return None


def _fangs(cr, mx, my, s, sink=1.0):
    """Two fangs over whatever he's biting (drawn after the fish so they sink into it)."""
    for side in (-1, 1):
        fx = mx + side * 30 * s
        cr.move_to(fx - 13 * s, my)
        cr.line_to(fx + 13 * s, my)
        cr.line_to(fx, my + 44 * s * sink)
        cr.close_path()
        cr.set_source_rgba(1, 1, 1, 1)
        cr.fill_preserve()
        cr.set_source_rgba(0.11, 0.06, 0.1, 1)
        cr.set_line_width(6 * s)
        cr.stroke()


def draw(cr, t, tl):
    A = tl.at
    K.photo(cr, t, "close_living", 0.0, push=0.03, dur=12, focus=(380, 700))
    g0, g1 = A("v3", "gulps"), A("v3", "ball", end=True)
    u = max(0.0, min(1.0, (t - g0) / (g1 - g0))) * 3
    k = int(u)
    puff = min(1.0, (k + ease_out(u - k)) / 3)
    v2, v3, poke = A("v2"), A("v3"), A("v4")
    chomp = A("v3", "scared")
    blink = K.auto_blink(t)
    tk = talk(tl, t)

    # where he stands to bite, and where the fish is while he holds it (in front of his mouth)
    HX = FX - 125
    turn = 0.45
    mouth = (HX + turn * 58 * 0.9 * S, VY - 492 * S)
    hold_low = (mouth[0] + 6, mouth[1] + 62)       # held under his open jaws ...
    hold_bit = (mouth[0] + 6, mouth[1] + 24)       # ... then snapped up into them
    snap = seg(t, chomp - 0.06, chomp + 0.04)
    hold_fish = (hold_low[0], lerp(hold_low[1], hold_bit[1], snap))
    hop = seg(t, v3, v3 + 0.45)                     # hops over to the dish
    grab = seg(t, v3 + 0.45, v3 + 0.6)              # crouches and grabs it
    lift = seg(t, v3 + 0.6, chomp - 0.08)           # lifts it up to his open jaws
    drop = seg(t, poke, poke + 0.35)                # lets go when the spikes get him

    in_dish = (FX, FY - 34)
    if t < v3 + 0.6 or t >= poke + 0.35:
        fpos = (in_dish[0], in_dish[1] - 30 * puff)
    elif t < poke:
        fpos = (lerp(in_dish[0], hold_fish[0], ease_out(lift)), lerp(in_dish[1], hold_fish[1], ease_out(lift)))
    else:                                           # falls back into the dish
        fpos = (lerp(hold_fish[0], in_dish[0], drop), lerp(hold_fish[1], in_dish[1] - 30 * puff, drop * drop))
    fs = 0.55 + 0.05 * puff
    fish_r = (70 + 44 * puff) * fs                  # its half width on screen, for his hands
    shake = 5 * math.sin(t * 60) if (chomp <= t < chomp + 0.25 or poke <= t < poke + 0.3) else 0

    K.dish_back(cr, FX, FY, FR)
    held = v3 + 0.6 <= t < poke

    def draw_fish():
        K.pufferfish(cr, t, fpos[0] + shake, fpos[1], fs, puff=puff, facing=-1,
                     eyes="angry" if puff > 0.5 else "open", flap=not held or t < chomp)

    if not held:
        draw_fish()
    K.dish_front(cr, FX, FY, FR)

    if t < v2:                                      # listening, then perks up at "bite"
        perk = seg(t, A("v1", "bite"), A("v1", "bite") + 0.3)
        vex(cr, t, VX, VY, S, turn=0.35 * perk, look=(0.7 * perk, 0.3 * perk),
            eyes="sparkle" if perk > 0.5 else "open", brows="angry", mouth="smirk", blink=blink,
            squash=0.2 * math.sin(perk * math.pi))
    elif t < v3:                                    # "Easy." hands on hips ... "I'm a vampire" cape spread
        big = seg(t, A("v2", "vampire") - 0.15, A("v2", "vampire") + 0.15)
        vex(cr, t, VX, VY, S, turn=-0.15, eyes="angry", brows="angry", mouth="smirk", talk=tk,
            arms=("out", "out") if big > 0.5 else ("hips", "hips"), cape=big, blink=blink,
            squash=0.25 * math.sin(seg(t, v2, v2 + 0.3) * math.pi), tilt=-0.06)
    elif t < poke:
        x = lerp(VX, HX, ease_out(hop))
        lift_px = 70 * math.sin(hop * math.pi) if hop < 1 else 0
        bx, by = (fpos[0] - x) / S, (fpos[1] - VY) / S          # fish in his body units
        reach = fish_r / S + 18
        if t < v3 + 0.45:                           # mid-hop: claws up, jaws open
            arms, point = ("up", "up"), ("claw", "claw")
        else:                                       # hands on both sides of the fish
            arms = ((-(bx - reach) + turn * 25, by), (bx + reach - turn * 25, by))
            point = ("claw", "claw")
        crouch = 0.45 * math.sin(grab * math.pi)
        biting = t >= chomp
        pain = puff > 0.8
        def in_hands(c):                            # the fish in front of his face, then his fangs in it
            if held:
                draw_fish()
                if biting:
                    _fangs(c, mouth[0] + shake * 0.6, mouth[1] + 4, S, sink=1.0)
        vex(cr, t, x + shake * 0.6, VY, S, turn=turn, lift=lift_px, legs="jump" if 0 < hop < 1 else "stand",
            held=in_hands if held and puff < 0.5 else None,
            squash=crouch, eyes=("cry" if pain else "shocked" if puff > 0.25 else "closed") if biting else "angry",
            brows=("up" if puff > 0.25 else None) if biting else "angry",
            mouth="chomp" if biting else "bite", arms=arms, point=point, cape=0.7 if not biting else 0.3,
            look=(0.6, 0.5), blink=0.0)
        if held and puff >= 0.5:                    # fully puffed: it fills his arms, in front of everything
            in_hands(cr)
        K.impact(cr, t, chomp, mouth[0] + 8, mouth[1] + 8, 70)
        cue("hit", t, chomp)
    else:                                           # "Ow!": knocked back in a spin, lands sitting, dizzy
        draw_fish() if held else None
        v = seg(t, poke, poke + 0.5)
        x = lerp(HX, 190, ease_out(v))
        land = t - (poke + 0.5)
        sq = 0.9 * math.exp(-9 * land) * math.cos(16 * land) if land > 0 else 0
        vex(cr, t, x, VY, S, rot=-2 * math.pi * ease_out(v), pivot="center",
            lift=130 * math.sin(v * math.pi) if v < 1 else 0, legs="sit" if v >= 1 else "jump",
            eyes="dizzy" if v >= 1 else "cry", mouth="wobble" if tk is None else None, talk=tk,
            arms=("up", "up") if v < 1 else ("out", "out"), squash=sq, cape=0.5, tears=v >= 1)
        K.impact(cr, t, poke, hold_fish[0], hold_fish[1] - 30, 60)
        K.dizzy(cr, t, x, VY - 1000 * S + 20, poke + 0.5, r=80)
    K.grain(cr)
    K.reply(cr, t, v2, A("v2", end=True) + 0.4, VX + 20, VY - 1080 * S - 20, "easy. i'm a vampire", size=52,
            font="Comic Neue")
    K.reply(cr, t, poke, A("v4", end=True) + 0.5, 230, VY - 1080 * S - 20, "OW! it poked me!", size=54,
            font="Comic Neue")
    K.comic_captions(cr, t, tl, skip="vex", y=860, size=56, line_chars=20)
