"""Vex episode 1: "Never Let a Vampire Bite a Pufferfish" -- the first mascot episode (owner approved 3 Nov 2026).
Vex, our baby vampire (owner's own ChatGPT design, flat 2D), on photos of the owner's home, with an off-screen keeper
who dares him; Vex's lines also pop up as small red text over his head, like the reference.

Script: out/scripts_vex_ep1.md. Facts: no antidote, cooking/freezing/drying don't destroy tetrodotoxin (UMEM
Educational Pearls #2689; Hong Kong Centre for Food Safety, Food Safety Focus 178, May 2021); the toxin comes mainly
from bacteria and builds up through the food chain (Noguchi & Arakawa, Marine Drugs 2008, PMC2525488); farmed fish
on clean food carry much less but are not guaranteed toxin-free (CFS 2021; Singapore Food Agency, "Pufferfish 101").
No "kills 30 people" number: lethal-dose estimates vary several-fold. The keeper is Turbo's stock female voice (never
the owner's); Vex is a small squeaky Turbo voice from a pitched-up Kokoro reference.
"""
import math

from motion import voice
from motion.engine import ease_out, lerp, seg
from motion.kit import whip
from motion.pkit import GOLD, GREEN, PURPLE, RED, buttons, card, red_x, sparkles, tag
from motion.polish import appear, bold_text, captions, paint, rrect, sign, stamp, stroke_line
from videos import vex_kit as K
from videos.bq_kit import hook2

NARRATOR = dict(turbo=True)
TAIL = 0.5
TWIST = "v11"         # music drops out under "Far less isn't zero" (research 18 Oct 2026, A5)
SERIES = "Vex the Vampire"
voice.SPEAKERS.update({"vex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+5")})

SCRIPT = [
    dict(id="v1", scene="palm", text="Vex, try and bite this pufferfish."),
    dict(id="v2", scene="palm", text="Easy. I'm a vampire.", speaker="vex"),
    dict(id="v3", scene="bowl", text="When a pufferfish gets scared, it gulps water and blows up into a spiky ball."),
    dict(id="v4", scene="bowl", text="Ow! It poked me!", speaker="vex"),
    dict(id="v5", scene="poison", text="And that's the nice part. Inside, it carries a poison far deadlier than "
                                       "cyanide."),
    dict(id="v6", scene="poison", text="There's no antidote. Cooking doesn't destroy it."),
    dict(id="v7", scene="poison", text="I'm vegetarian now.", speaker="vex"),
    dict(id="v8", scene="corner", text="But here's the strange part. The fish doesn't make its own poison."),
    dict(id="v9", scene="corner", text="It builds it up from its food, starting with tiny bacteria. Fish raised on "
                                       "clean food carry far less."),
    dict(id="v10", scene="farmed", text="So I can bite that one?", speaker="vex"),
    dict(id="v11", scene="farmed", text="Far less isn't zero. And it still puffs up. [chuckle]", gap=0.4),
    dict(id="v12", scene="end", text="In Japan, only licensed chefs may serve it. So, would you eat pufferfish? Or "
                                     "never?", gap=0.3),
]

METADATA = dict(
    title="Never Let a Vampire Bite a Pufferfish 🐡",
    alt_titles=["This Tiny Fish Is Deadlier Than a Vampire 🐡", "My Vampire Tried to Bite a Pufferfish 🐡"],
    description="""Vex is a baby vampire. Biting is his whole job. So we gave him a pufferfish. 🐡

When a pufferfish gets scared, it gulps water and blows up into a spiky ball. And that's the nice part: inside, it carries tetrodotoxin, a poison far deadlier than cyanide. There's no antidote, and cooking doesn't destroy it.

The strange part: the fish doesn't make its own poison. It builds it up from its food, starting with tiny bacteria. Pufferfish raised on clean food carry far less, but far less isn't zero. In Japan, only licensed chefs may serve it.

Sources: University of Maryland emergency medicine notes (UMEM Educational Pearls #2689); Hong Kong Centre for Food Safety, Food Safety Focus no. 178 (2021); Noguchi & Arakawa, "Tetrodotoxin: distribution and accumulation in aquatic organisms", Marine Drugs (2008); Singapore Food Agency, "Pufferfish 101".

💬 Would you eat pufferfish made by a licensed chef? Or never? 👇

🔔 Interestingly Strange: weird animals, clever twists and mind-bending questions, animated in under a minute.""",
    hashtags=["#Pufferfish", "#WeirdAnimals", "#Shorts"],
    tags=["pufferfish", "fugu", "tetrodotoxin", "poisonous fish", "vampire cartoon", "cute vampire", "weird animals",
          "animal facts", "science shorts", "interestingly strange"],
    pinned_comment="Licensed chef, fresh fugu, it's on the table. Would you eat it? I'D EAT IT or NEVER? 🐡👇",
)


# ---------------------------------------------------------------- helpers
def _hop(t, t0, dur=0.35, h=70):
    """Lift (px) of one hop starting at t0."""
    u = seg(t, t0, t0 + dur)
    return h * math.sin(u * math.pi) if 0 < u < 1 else 0.0


def _land(t, t0, k=0.8):
    """Squash after landing at t0 (damped)."""
    d = t - t0
    return k * math.exp(-9 * d) * math.cos(16 * d) if d > 0 else 0.0


def _jelly(t, t0, amp=24):
    d = t - t0
    return amp * math.exp(-5 * d) * math.sin(18 * d) if d > 0 else 0.0


def _gulps(t, t0, t1, n=3):
    """Puff 0 -> 1 in n gulps between t0 and t1."""
    u = max(0.0, min(1.0, (t - t0) / max(0.01, t1 - t0))) * n
    k = int(u)
    return min(1.0, (k + ease_out(u - k)) / n)


def _vex_line(cr, t, tl, beat, x, y, s, text):
    b = tl.by_id[beat]
    K.reply(cr, t, b.start, b.end + 0.3, x, K.head_top(y, s) - 34, text)


def _bowl(cr, t, x, y, r, fish_s, puff, facing=-1, eyes="open", shake=0.0, label=None):
    K.floor_shadow(cr, x, y + 2, r * 0.95)
    K.bowl_back(cr, x, y, r)
    K.pufferfish(cr, t, x + shake * math.sin(t * 60), y - r * 1.02, fish_s, puff=puff, facing=facing, eyes=eyes)
    K.bowl_front(cr, x, y, r)
    if label:
        rrect(cr, x - 56, y - r * 0.55, 112, 34, 8)
        paint(cr, (1, 1, 1, 0.92), K.INK, 3)
        bold_text(cr, label, x, y - r * 0.55 + 26, 24, GREEN, outline=None, shadow=0)


# ---------------------------------------------------------------- scenes
def scene_palm(cr, t, tl):
    A = tl.at
    z = K.photo(cr, t, "hand_palm", 0.0, focus=(380, 600))
    cr.save()
    K.zoom_at(cr, z, (380, 600))
    K.floor_shadow(cr, 382, 612, 64, 0.3)
    K.bowl_back(cr, 382, 612, 80)
    K.pufferfish(cr, t, 382, 530, 0.52, puff=0.0, facing=-1)
    K.bowl_front(cr, 382, 612, 80)
    h0 = A("v2")
    lift = _hop(t, h0, 0.38, 80)
    K.vex(cr, t, 160, 880, 0.19, lift=lift, squash=_land(t, h0 + 0.38) - (0.3 if lift > 0 else 0),
          wobble=_jelly(t, h0 + 0.38))
    cr.restore()
    _vex_line(cr, t, tl, "v2", 170, 880, 0.19, "easy. i'm a vampire")


def scene_bowl(cr, t, tl):
    A = tl.at
    s0 = tl.scene_at(t)[1]
    z = K.photo(cr, t, "floor_living", s0, focus=(380, 800))
    cr.save()
    K.zoom_at(cr, z, (380, 800))
    puff = _gulps(t, A("v3", "gulps"), A("v3", "ball", end=True))
    poke = A("v4")
    _bowl(cr, t, 480, 860, 120, 0.72, puff, eyes="angry" if puff > 0.5 else "open",
          shake=4 if poke <= t < poke + 0.3 else 0)
    lunge = seg(t, A("v3", "scared"), A("v3", "scared") + 0.35)
    if t < poke:
        x = lerp(190, 330, ease_out(lunge))
        K.vex(cr, t, x, 880, 0.19, rot=0.3 * math.sin(lunge * math.pi / 2), squash=-0.2 * math.sin(lunge * math.pi),
              wobble=_jelly(t, A("v3", "scared") + 0.35, 18))
    else:                                   # "Ow!": knocked back in a spin, lands on his bottom, dazed
        u = seg(t, poke, poke + 0.5)
        x = lerp(330, 160, ease_out(u))
        lift = 130 * math.sin(u * math.pi) if u < 1 else 0
        K.vex(cr, t, x, 885, 0.19, lift=lift, rot=-2 * math.pi * ease_out(u), pivot="center",
              squash=_land(t, poke + 0.5, 0.9) + (0.25 if u >= 1 else 0), blink=1.0 if u >= 1 else None)
        K.dizzy(cr, t, x, K.head_top(885, 0.19) + 10, poke + 0.5)
    cr.restore()
    _vex_line(cr, t, tl, "v4", 170, 885, 0.19, "OW! it poked me!")


def scene_poison(cr, t, tl):
    A = tl.at
    s0 = tl.scene_at(t)[1]
    z = K.photo(cr, t, "floor_living", s0 - 3.0, focus=(380, 800))
    cr.save()
    K.zoom_at(cr, z, (380, 800))
    calm = seg(t, A("v6", "Cooking"), A("v6", "Cooking") + 1.2)
    _bowl(cr, t, 480, 860, 120, 0.72, 1 - 0.75 * calm, eyes="angry" if calm < 0.5 else "open")
    up = A("v5", "Inside")
    if t < up:
        K.vex(cr, t, 160, 885, 0.19, squash=0.25, blink=1.0)
        K.dizzy(cr, t, 160, K.head_top(885, 0.19) + 10, s0 - 1)
    else:
        K.vex(cr, t, 160, 885, 0.19, squash=_land(t, up, 0.6), wobble=_jelly(t, up, 14))
    if t >= A("v7"):
        k = appear(t, A("v7"), 0.35)
        K.carrot(cr, 240, 800, 0.9 * k, rot=0.5)
    cr.restore()
    card(cr, t, A("v5", "poison"), 360, 270, 470, 150, "TETRODOTOXIN", ["the poison inside"], col=PURPLE,
         end=A("v6") - 0.1, title_size=38, line_size=34)
    if A("v5", "deadlier") <= t < A("v6") - 0.1:
        K.skull(cr, 360, 430, appear(t, A("v5", "deadlier"), 0.3))
    if t >= A("v5", "cyanide"):
        stamp(cr, t, A("v5", "cyanide"), 360, 540, "DEADLIER THAN CYANIDE", col=RED, size=40, end=A("v6") - 0.1)
    if t >= A("v6", "antidote"):
        stamp(cr, t, A("v6", "antidote"), 360, 290, "NO ANTIDOTE", col=RED, size=70, end=A("v7") - 0.1)
    if A("v6", "Cooking") <= t < A("v7") - 0.1:
        K.pan(cr, t, 340, 470, appear(t, A("v6", "Cooking"), 0.35))
        red_x(cr, t, A("v6", "destroy"), 340, 460, 70)
    _vex_line(cr, t, tl, "v7", 170, 885, 0.19, "i'm vegetarian now")


def scene_corner(cr, t, tl):
    A = tl.at
    s0 = tl.scene_at(t)[1]
    z = K.photo(cr, t, "floor_swing", s0, focus=(420, 820))
    cr.save()
    K.zoom_at(cr, z, (420, 820))
    _bowl(cr, t, 450, 880, 112, 0.62, 0.0)
    K.vex(cr, t, 170, 900, 0.19)
    if A("v8", "strange") <= t < A("v9"):
        k = appear(t, A("v8", "strange"), 0.35)
        bold_text(cr, "?", 455, 610 + 6 * math.sin(t * 4), 120 * k, GOLD)
    cr.restore()
    sign(cr, t, A("v8", "own"), 360, 260, "NOT ITS OWN POISON", col=PURPLE, size=46, end=A("v9") - 0.1)
    chain_end = A("v9", "raised") - 0.1
    if A("v9", "food") <= t < chain_end + 0.2:
        out = 1 - seg(t, chain_end, chain_end + 0.2)
        k = appear(t, A("v9", "food"), 0.35) * out
        rrect(cr, 40, 262, 640, 140, 30)                   # a light panel so the chain reads over the dark mat
        paint(cr, (1, 1, 1, 0.82 * out), (0.1, 0.06, 0.08, 0.6 * out), 4)
        K.pufferfish(cr, t, 590, 330, 0.5 * k, facing=-1)
        if t >= A("v9", "starting"):
            K.worm(cr, t, 360, 335, appear(t, A("v9", "starting"), 0.35) * out)
            stroke_line(cr, [(430, 335), (505, 335)], 8, RED, curve=False)
        if t >= A("v9", "bacteria"):
            K.bacteria(cr, t, 130, 330, 1.1 * appear(t, A("v9", "bacteria"), 0.35) * out)
            stroke_line(cr, [(195, 335), (275, 335)], 8, RED, curve=False)
        tag(cr, t, A("v9", "food"), 360, 220, "IT COMES FROM ITS FOOD", col=GOLD, size=36, end=chain_end)
    if t >= A("v9", "raised"):
        card(cr, t, A("v9", "raised"), 190, 330, 280, 230, "WILD", [], col=RED, title_size=40)
        card(cr, t, A("v9", "clean"), 530, 330, 280, 230, "FARMED", [], col=GREEN, title_size=40)
        K.skull(cr, 190, 375, appear(t, A("v9", "raised"), 0.35) * 1.15)
        K.skull(cr, 530, 385, appear(t, A("v9", "clean"), 0.35) * 0.55)
        if t >= A("v9", "less"):
            tag(cr, t, A("v9", "less"), 530, 500, "FAR LESS", col=GREEN, size=40)


def scene_farmed(cr, t, tl):
    A = tl.at
    s0 = tl.scene_at(t)[1]
    z = K.photo(cr, t, "floor_swing", s0 - 4.0, focus=(420, 820))
    cr.save()
    K.zoom_at(cr, z, (420, 820))
    hit = A("v11", "puffs")
    puff = seg(t, hit, hit + 0.25)
    _bowl(cr, t, 450, 880, 112, 0.62, puff, eyes="angry" if puff > 0.5 else "open", label="FARMED",
          shake=4 if hit <= t < hit + 0.35 else 0)
    v10 = A("v10")
    hops = [v10 + 0.05, v10 + 0.5]
    if t < hit:
        u = seg(t, hops[0], hops[1] + 0.4)
        x = lerp(170, 300, u)
        lift = _hop(t, hops[0], 0.38, 50) + _hop(t, hops[1], 0.38, 50)
        K.vex(cr, t, x, 900, 0.19, lift=lift, squash=_land(t, hops[1] + 0.38, 0.6), wobble=_jelly(t, hops[1] + 0.38))
        if t >= v10:
            sparkles(cr, t, v10, x, K.head_top(900, 0.19) + 60, n=8, col=GOLD, spread=110)
    else:                                   # knocked flat by the puff
        u = seg(t, hit, hit + 0.45)
        x = lerp(300, 170, ease_out(u))
        K.vex(cr, t, x, 905, 0.19, lift=90 * math.sin(u * math.pi) if u < 1 else 0, rot=-1.45 * ease_out(u),
              pivot="center", blink=1.0 if u >= 1 else None, squash=_land(t, hit + 0.45, 0.5))
        K.dizzy(cr, t, x - 120, 840, hit + 0.45)
    cr.restore()
    _vex_line(cr, t, tl, "v10", 200, 900, 0.19, "so i can bite that one?")
    if t >= A("v11", "zero"):
        stamp(cr, t, A("v11", "zero"), 360, 300, "NOT ZERO", col=RED, size=72)


def scene_end(cr, t, tl):
    A = tl.at
    s0 = tl.scene_at(t)[1]
    z = K.photo(cr, t, "hand_reach", s0, focus=(380, 640))
    cr.save()
    K.zoom_at(cr, z, (380, 640))
    up = A("v12", "would")
    if t < up:
        K.vex(cr, t, 215, 950, 0.19, rot=-1.45, pivot="center", blink=1.0)
        K.dizzy(cr, t, 95, 890, s0)
    else:
        K.vex(cr, t, 175, 950, 0.19, lift=_hop(t, up, 0.4, 70), squash=_land(t, up + 0.4, 0.7),
              wobble=_jelly(t, up + 0.4))
    cr.restore()
    if A("v12", "Japan") <= t < up:
        K.chef_hat(cr, 360, 300, appear(t, A("v12", "Japan"), 0.35) * 1.3)
        tag(cr, t, A("v12", "licensed"), 360, 430, "JAPAN: LICENSED CHEFS ONLY", col=GOLD, size=34, end=up - 0.1)
    sign(cr, t, up, 360, 220, "WOULD YOU EAT IT?", col=GOLD, size=56)
    buttons(cr, t, A("v12", "never"), [("I'D EAT IT", GREEN), ("NEVER", RED)], y=370, size=42, w=300)


SCENES = {"palm": scene_palm, "bowl": scene_bowl, "poison": scene_poison, "corner": scene_corner,
          "farmed": scene_farmed, "end": scene_end}


def draw(cr, t, tl):
    name, start, _ = tl.scene_at(t)
    cr.save()
    whip(cr, t, start)
    SCENES[name](cr, t, tl)
    cr.restore()
    K.grain(cr)
    hook2(cr, t, "THIS TINY FISH IS", "DEADLIER", end=tl.at("v1", end=True) + 0.4, y=190, big_at=tl.at("v1", "bite"),
          mark="circle", mark_at=tl.at("v1", "pufferfish"))
    # Vex's lines show as red handwriting over his head, so the bottom captions skip them (like the reference)
    if not any(b.speaker == "vex" and b.start - 0.05 <= t <= b.end + 0.35 for b in tl.beats):
        captions(cr, t, tl)
