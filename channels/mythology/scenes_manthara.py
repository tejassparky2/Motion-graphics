"""Scenes for videos/manthara.py: why Manthara turned Kaikeyi against Rama (Valmiki Ramayana, Ayodhya Kanda 7-9;
Ramcharitmanas, Ayodhya Kand, doha 11-12), in Togalu Gombeyaata shadow puppets drawn in code, built on the lessons
from the owner's Ashtavakra reference (myth_out/LESSONS_FROM_REFERENCE_ASHTAVAKRA.md). Each shot (key mtN) covers
one or more script lines (FIRST maps it to its first line; CUES name the line of every cue word).

- Frame 0 is the stake happening: Manthara large in front, pointing, while Rama walks away into the forest with his
  bow. The callback (mt15) is the same framing in gold, with a golden path running on from Rama to Ravana.
- Short Hindi labels (the word being said) on a parchment strip; no English on screen.
- A colour for each place (dusk for the exile, palace warm, dawn on the terrace, red for anger, night blue for the
  question, heaven gold) and a closer camera where a face matters.

Shot list (line: what is on the screen)
  mt1   HOOK: Manthara big on the left, sly, pointing; Rama small, walking away into the trees on the right
  mt2   Manthara alone; a big red "?" pops; on "Tulsidas" a glowing book
  mtF   the king and his three queens; Rama comes up by the eldest, Bharata by Kaikeyi
  mt3   Kaikeyi with Manthara behind her; a little city far off (her father's home) and a dotted path to them
  mt4   the terrace at dawn: Ayodhya behind, flags and garlands; Manthara at the railing; a crown glows over the dome
  mt5   Manthara hurries in to Kaikeyi: alarm
  mt6   Kaikeyi glowing with joy, sparkles; the necklace flies from her hand to Manthara
  mt7   close: Manthara angry, flings the necklace away; beads scatter, red flash
  mt8   Manthara at Kaikeyi's ear; a thought cloud: Kaikeyi fanning the elder queen, then Bharata walking away with
        a bundle
  mt9   Kaikeyi afraid, hand on her heart; a bubble: the battle, Kaikeyi holding up the wounded king; two lights
  mt10  the two lights: one puts a crown on Bharata, the other sends Rama walking into the forest
  mt11  Manthara small in a spotlight, empty hands, a red "?"
  mt12  Ravana laughing inside a shield of light, arrows of light bounce off; Rama raises his bow
  mt13  Rama crowned before his palace; Ravana far away; a dotted path between ends in a red "?"
  mt14  heaven: the gods' prayers rise as lights; Saraswati appears with her veena; a ribbon of her light goes down
        into Manthara's head on earth, and her face turns
  mt15  CALLBACK: the hook's picture in gold, a golden path from Manthara's finger to Rama and on to Ravana
  mt16  two cards (दासी? / मोहरा?), a red ring alternating; Manthara small between them

Every frame is a pure function of t. Cues are words of the Hindi lines with a fraction fallback (CUES).
"""
import math

import cairo

import andhe_cast  # noqa: F401  (registers the palace pillars and arch)
import arjuna_cast  # noqa: F401  (registers the thought bubble)
import dharmavyadha_cast  # noqa: F401  (registers the little city)
import kaikeyi_cast as K
import lrekha_cast  # noqa: F401  (registers the palace and the clouds)
import manthara_cast as MC
import camera_beats
import puppet_core as pc
import six_cast_c  # noqa: F401  (registers Brahma and the book)
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import clamp, ease, prog
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, register
from scenes_ashtavakra2 import hcard, label, red_spot
from scenes_hanuman_curse import arc_path, orb, qmark, trail
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, motes, red_ring, walk_legs, woman_angles
from scenes_jayadratha import flash_at, tint, to_user
from scenes_kaikeyi import bharata, dasha, fig, kai, rama
from scenes_lakshman_rekha import HEART, forest, sparkle
from scenes_mandhata import burst, lights, warm
from scenes_ravana import rv, rv_angles
from scenes_ruru import sepia
from scenes_six_c import brahma
from shots import T

G = FEET + 120                       # the ground line of the near sets
FAR = FEET                           # the ground of far figures
MISSES = set()
register("mt_dasha_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, K.DS_SKIN, K.RED, K.GOLD, 1.12))
register("mt_kai_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, K.KK_SKIN, K.KK_SARI, K.GOLD, 0.9))

FIRST = {"mt1": "m01", "mt2": "m04", "mtF": "m06", "mt3": "m09", "mt4": "m11", "mt5": "m13", "mt6": "m15",
         "mt7": "m18", "mt8": "m19", "mt9": "m21", "mt10": "m25", "mt11": "m28", "mt12": "m29", "mt13": "m32",
         "mt14": "m33", "mt15": "m35", "mt16": "m36"}          # each shot's first line (a shot covers several lines)

# Every cue of every shot: (name, line, word, fraction fallback, ((after, min gap), ...)); "t0" = the shot's start.
CUES = {
    "mt1": (("R", "m02", "राम", 0.1, (("t0", 1.0),)), ("C", "m02", "चौदह", 0.3, (("R", 0.2),)),
            ("J", "m02", "जंगल", 0.6, (("C", 0.3),)), ("D", "m03", "दासी", 0.6, (("J", 0.4),)),
            ("M", "m03", "मंथरा", 0.9, (("D", 0.3),))),
    "mt2": (("Q", "m04", "क्यों", 0.8, (("t0", 0.3),)), ("M", "m05", "तुलसीदास", 0.4, (("Q", 0.4),))),
    "mtF": (("K", "m06", "तीन", 0.4, (("t0", 0.2),)), ("R", "m07", "राम", 0.8, (("K", 0.5),)),
            ("B", "m08", "भरत", 0.85, (("R", 0.5),))),
    "mt3": (("K", "m09", "कैकई", 0.4, (("t0", 0.1),)), ("D", "m09", "दासी", 0.8, (("K", 0.3),)),
            ("Y", "m10", "मायके", 0.4, (("D", 0.4),))),
    "mt4": (("C", "m11", "देखा", 0.3, (("t0", 0.3),)), ("A", "m11", "अयोध्या", 0.6, (("C", 0.3),)),
            ("S", "m11", "सजी", 0.75, (("A", 0.2),)), ("R", "m12", "राम राजा", 0.6, (("S", 0.6),))),
    "mt5": (("M", "m13", "भागी", 0.3, (("t0", 0.1),)), ("U", "m14", "उठो", 0.2, (("M", 0.8),)),
            ("X", "m14", "मुसीबत", 0.85, (("U", 0.4),))),
    "mt6": (("K", "m15", "खुश", 0.6, (("t0", 0.3),)), ("P", "m16", "प्यारे", 0.6, (("K", 0.5),)),
            ("G", "m17", "गहना", 0.8, (("P", 0.6),))),
    "mt7": (("A", "m18", "स्से", 0.4, (("t0", 0.3),)), ("F", "m18", "फेंक", 0.85, (("A", 0.4),))),
    "mt8": (("D", "m19", "बोली", 0.05, (("t0", 0.0),)), ("N", "m19", "नौकरानी", 0.75, (("D", 1.0),)),
            ("B", "m20", "भरत", 0.4, (("N", 0.6),)), ("X", "m20", "निकाल", 0.8, (("B", 0.4),))),
    "mt9": (("D", "m21", "डर", 0.7, (("t0", 0.2),)), ("Y", "m22", "याद", 0.2, (("D", 0.4),)),
            ("W", "m22", "युद्ध", 0.4, (("Y", 0.3),)), ("J", "m22", "जान", 0.75, (("W", 0.5),)),
            ("V", "m23", "वरदान", 0.7, (("J", 0.5),)), ("Z", "m24", "माँगोगी", 0.5, (("V", 0.5),))),
    "mt10": (("B", "m25", "भरत", 0.5, (("t0", 0.3),)), ("R", "m25", "राज", 0.8, (("B", 0.2),)),
             ("S", "m26", "दूसरे", 0.2, (("R", 0.4),)), ("V", "m26", "वनवास", 0.85, (("S", 0.6),)),
             ("K", "m27", "माँगा", 0.4, (("V", 0.4),))),
    "mt11": (("D", "m28", "दासी", 0.6, (("t0", 0.5),)), ("Q", "m28", "क्या", 0.85, (("D", 0.3),))),
    "mt12": (("H0", "m29", "छुपा", 0.5, (("t0", 0.3),)), ("R", "m30", "बनने", 0.2, (("H0", 0.4),)),
             ("D", "m30", "देवता", 0.75, (("R", 0.4),)), ("A", "m31", "अंत", 0.3, (("D", 0.6),)),
             ("H", "m31", "हाथों", 0.7, (("A", 0.4),))),
    "mt13": (("R", "m32", "राजा", 0.15, (("t0", 0.2),)), ("P", "m32", "महल", 0.35, (("R", 0.3),)),
             ("V", "m32", "रावण", 0.65, (("P", 0.5),)), ("K", "m32", "पहुँचते", 0.9, (("V", 0.3),))),
    "mt14": (("B", "m33", "देवताओं", 0.2, (("t0", 0.2),)), ("G", "m33", "सरस्वती", 0.75, (("B", 0.6),)),
             ("D", "m34", "आकर", 0.3, (("G", 0.6),)), ("P", "m34", "बुद्धि", 0.6, (("D", 0.8),)),
             ("M", "m34", "फेर", 0.85, (("P", 0.3),))),
    "mt15": (("V", "m35", "विलेन", 0.25, (("t0", 0.4),)), ("C", "m35", "वजह", 0.5, (("V", 0.6),)),
             ("R", "m35", "रावण", 0.8, (("C", 0.4),))),
    "mt16": (("G", "m36", "घर", 0.3, (("t0", 0.6),)), ("D", "m36", "देवताओं", 0.6, (("G", 0.8),)),
             ("M", "m36", "मोहरा", 0.75, (("D", 0.4),))),
}


def cue(tl, line, word, frac):
    try:
        return T(tl, line, {"hi": word})
    except (KeyError, ValueError):
        MISSES.add((line, word))
        return T(tl, line, frac)


def cues(tl, shot):
    cache = getattr(tl, "_mt_cues", None)
    if cache is None:
        cache = tl._mt_cues = {}
    if shot not in cache:
        out = {"t0": T(tl, FIRST[shot])}
        for name, line, word, frac, cons in CUES[shot]:
            v = cue(tl, line, word, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[shot] = out
    return cache[shot]


# ------------------------------------------------------------------ figures and sets


def mt(cr, t, x, s, mood="sly", front=(-0.3, -0.6), backa=(0.25, -0.3), head=0.12, hits=(), flip=False, alpha=1.0,
       blur=0.0, feet=G, ph=0.0, lean=0.14, rods=True, y=None):
    """Manthara, bent forward (lean), feet on `feet`."""
    ang = woman_angles("mt_manthara", t, front, backa, head, hits, ph)
    hy = feet - 470 * s if y is None else y
    swap = {"mt_manthara_head": "mt_manthara_head" + ("" if mood == "sly" else "_" + mood)}
    return puppet(cr, MC.MANTHARA, x, hy, s, lean * (-1 if flip else 1) + bob_rot(t, ph), flip, ang, alpha, blur,
                  swap=swap, rods=rods)


def mt_walk(cr, t, t0, t1, x0, x1, s, step=0.3, **kw):
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step)
    kw.setdefault("hits", [(t1, 1.0)])
    return mt(cr, t, x, s, y=kw.pop("feet", G) - 470 * s + bob, lean=0.14 + rock, **kw), x


def lady(cr, rig, key, t, x, s, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(), flip=False, alpha=1.0,
         blur=0.0, feet=G, ph=0.0, rot=0.0, rods=True):
    ang = woman_angles(key, t, front, backa, head, hits, ph)
    return puppet(cr, rig, x, feet - 470 * s, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, rods=rods)


def ground(cr, y=G, col=(0.50, 0.32, 0.16), a=0.85):
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    pc.poly(cr, [(-200, y - 6), (W + 200, y + 6), (W + 200, H + 200), (-200, H + 200)])
    cr.set_source_rgba(*col, a)
    cr.fill()
    cr.restore()


def hall(cr, alpha=1.0):
    """The palace inside: two carved pillars and an arch, a dark floor."""
    for x in (80, 1000):
        prop(cr, "ak_pillar", x, G, 1.0, alpha=0.8 * alpha, blur=3)
    prop(cr, "ak_arch", 540, 420, 1.0, alpha=0.6 * alpha, blur=5)
    ground(cr, col=(0.55, 0.30, 0.18), a=0.7 * alpha)


def dots_path(cr, pts, p, col=(1.0, 0.86, 0.45), a=1.0, r=7, every=4):
    n = int(len(pts) * clamp(p))
    for i in range(0, n, every):
        cr.new_path()
        cr.arc(*pts[i], r, 0, 2 * math.pi)
        cr.set_source_rgba(*col, a)
        cr.fill()


def fly(t, t_go, dur, p0, p1, lift):
    """Position along an arc from p0 to p1 starting at t_go."""
    u = ease(clamp((t - t_go) / dur))
    pts = arc_path(p0, p1, lift, 2)
    x = p0[0] + (p1[0] - p0[0]) * u
    y = p0[1] + (p1[1] - p0[1]) * u - lift * 4 * u * (1 - u)
    return x, y, u, pts


def cloud_vision(cr, t, t_in, x, y, s, a=1.0):
    """A big thought cloud (the vision of what Manthara says) fading in at t_in; returns its alpha."""
    q = prog(t, t_in, 0.4) * a
    if q > 0.01:
        prop(cr, "ar_think", x, y, s * (0.9 + 0.1 * ease(q)), alpha=q)
    return q


# ------------------------------------------------------------------ the shots


HK_M = (300, 1.15)                    # Manthara in the hook: x, scale


def hook_set(cr, t, gold=0.0):
    forest(cr, t, feet=FAR, hut_a=0.0, trees=((690, 0.62, 8, 0.75, False), (1040, 0.82, 3, 0.95, True),
                                             (880, 0.5, 12, 0.55, False)))
    ground(cr, FAR + 10, col=(0.48, 0.30, 0.15), a=0.6)


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "mt1")
    hook_set(cr, t)
    x, bob, rock, ph = hop_walk(t, 0.0, t1 + 1.0, 780, 1000, 0.5)
    s = 0.52 - 0.08 * clamp(t / max(1.0, t1))
    rama(cr, t, x, s, legs=walk_legs(ph), rot=rock, y=FAR - 434 * s + bob, front=(-0.1, -0.2), ph=0.4)
    mood = "smile" if t > c["M"] else "sly"
    red_spot(cr, HK_M[0] + 40, G - 640, 520, 0.7 * prog(t, c["M"] - 0.1, 0.4))
    mt(cr, t, HK_M[0], HK_M[1], mood=mood, front=keyed(t, [(0, (-1.45, -0.1)), (c["D"], (-1.6, 0.05))]),
       backa=(0.3, -0.5), head=0.16, hits=[(0.3, 0.5), (c["C"], 0.3), (c["M"], 0.4)], feet=G + 40)
    return dict(flash=flash_at(t, c["M"], 0.2))


def s_why(cr, t, tl, t0, t1):
    c = cues(tl, "mt2")
    ground(cr)
    mt(cr, t, 360, 1.0, mood="sly", front=(-0.6, -1.4), backa=(0.2, -0.4), head=0.1, hits=[(c["Q"], 0.5)])

    def ui(cr_):
        qmark(cr_, t, c["Q"] - 0.1, 800, 760, 330)
        if t > c["M"] - 0.2:
            q = prog(t, c["M"] - 0.2, 0.4)
            warm(cr_, 800, 1250, 330, q)
            lights(cr_, t, 800, 1250, 220, 10, q)
            prop(cr_, "c6_veda", 800, 1250, 1.3 * (0.8 + 0.2 * ease(q)), -0.05, alpha=q)
    return dict(ui=ui)


def s_who(cr, t, tl, t0, t1):
    c = cues(tl, "mt3")
    hall(cr)
    q = prog(t, c["Y"] - 0.2, 0.5)
    if q > 0.01:
        prop(cr, "dv_city", 170, 700, 0.42, alpha=q, blur=4)
        dots_path(cr, arc_path((220, 720), (430, 1150), 120, 60), prog(t, c["Y"], 1.0), a=q)
    kai(cr, t, 700, 0.95, flip=True, feet=G, hits=[(c["K"], 0.4)], ph=0.2)
    b, k, a = depth(t, c["D"] - 0.2, 0.45)
    mt(cr, t, 420, 0.82 * k, mood="sly", front=(-0.4, -0.8), alpha=a, blur=b, hits=[(c["Y"], 0.3)], ph=0.7)
    return {}


def s_city(cr, t, tl, t0, t1):
    c = cues(tl, "mt4")
    q = prog(t, c["A"] - 0.3, 0.6)
    prop(cr, "mt_city", 560, 1150, 0.92, alpha=0.35 + 0.65 * q, blur=4 * (1 - q))
    if t > c["S"]:
        lights(cr, t, 560, 800, 460, 18, prog(t, c["S"], 0.5))
    if t > c["R"] - 0.2:
        u = prog(t, c["R"] - 0.2, 0.5)
        warm(cr, 560, 440, 260, u)
        prop(cr, "kk_crown", 560, 420 - 30 * ease(u), 0.9 * (0.6 + 0.4 * ease(u)), alpha=u)
    mt(cr, t, 250, 0.82, mood="sly", front=(-1.1, -0.2), backa=(0.2, -0.4), head=-0.1,
       hits=[(c["C"], 0.4), (c["R"], 0.5)], feet=1700)
    prop(cr, "mt_rail", 540, 1330, 0.95)
    return dict(eve=0.25)


SUMITRA = MC.woman("mt_sumitra", skin=(0.97, 0.74, 0.54), skirt=(0.40, 0.70, 0.36), choli=(0.95, 0.60, 0.20),
                   border=MC.GOLD, pallu_col=(0.30, 0.56, 0.28), gem=MC.RED, hands=("open", "open"))
register("mt_sumitra_head", (-130, -300, 110, 40),
         lambda cr: (MC.C.woman_head(cr, dict(skin=(0.97, 0.74, 0.54), flower=MC.GOLD)), K.queen_crown(cr)))


def s_family(cr, t, tl, t0, t1):
    """The king and his three queens; Rama comes up by the eldest, Bharata by Kaikeyi."""
    c = cues(tl, "mtF")
    tK, tR, tB = c["K"], c["R"], c["B"]
    hall(cr)
    dasha(cr, t, 560, 0.7, feet=G - 60, front=(-0.4, -0.6), ph=0.1, hits=[(t0 + 0.2, 0.3)])
    for k, (rig, key, x, flip) in enumerate(((MC.KAUSALYA, "mt_kausalya", 170, False),
                                             (SUMITRA, "mt_sumitra", 340, False),
                                             (K.KAIKEYI, "kaikeyi", 900, True))):
        b, kk, a = depth(t, tK - 0.25 + 0.22 * k, 0.4)
        lady(cr, rig, key, t, x, 0.64 * kk, feet=G - 60, flip=flip, alpha=a, blur=b, ph=0.3 * k)
    for x, tc, fn, flip in ((230, tR, rama, False), (860, tB, bharata, True)):
        if t > tc - 0.3:
            b, kk, a = depth(t, tc - 0.3, 0.4)
            glow(cr, x, G - 300, 240, 0.6 * a)
            fn(cr, t, x, 0.56 * kk, feet=G + 60, flip=flip, alpha=a, blur=b, front=ANJ[0], backa=ANJ[1], ph=0.5)
    return {}


def s_alarm(cr, t, tl, t0, t1):
    c = cues(tl, "mt5")
    hall(cr)
    kai(cr, t, 860, 0.95, flip=True, front=(-0.05, -0.2), head=0.05 * (t > c["U"]), hits=[(c["U"], 0.6)], ph=0.2)
    mt_walk(cr, t, t0 + 0.1, c["U"] - 0.05, 100, 440, 0.88, step=0.26,
            mood="angry" if t > c["X"] - 0.2 else "sly",
            front=keyed(t, [(0, (-0.5, -0.4)), (c["U"], (-2.6, 0.3))]),
            backa=keyed(t, [(0, (0.4, -0.4)), (c["U"], (-2.4, 0.3))]))
    return dict(flash=flash_at(t, c["X"], 0.2))


def s_happy(cr, t, tl, t0, t1):
    c = cues(tl, "mt6")
    hall(cr)
    tG = c["G"]
    glow(cr, 720, G - 600, 420, 0.6 * prog(t, c["K"], 0.4))
    lights(cr, t, 720, G - 650, 300, 14, prog(t, c["K"], 0.4))
    reach = t > tG - 0.4
    pk = kai(cr, t, 720, 0.95, flip=True, front=(-1.4, -0.1) if reach else (-0.3, -0.9),
             backa=(-0.2, -1.6) if t < tG - 0.4 else (0.15, -0.2), hits=[(c["K"], 0.6), (tG - 0.4, 0.4)], ph=0.2)
    pm = mt(cr, t, 330, 0.86, mood="sly", front=(-1.3, -0.3) if t > tG else (-0.3, -0.6), hits=[(tG + 0.4, 0.4)])
    x, y, u, _ = fly(t, tG - 0.1, 0.55, to_user(cr, pk["handF"]), to_user(cr, pm["handF"]), 160)
    if t > tG - 0.6:
        prop(cr, "mt_haar", x, y - 20, 0.5, 0.2 * math.sin(u * 6), alpha=prog(t, tG - 0.6, 0.25))
    if t < c["P"] + 2.5 and t > c["P"] - 0.2:
        q = prog(t, c["P"] - 0.2, 0.3) * (1 - prog(t, c["P"] + 2.2, 0.3))
        prop(cr, "ar_think", 470, 560, 1.0, alpha=q)
        rama(cr, t, 470, 0.36, feet=760, alpha=q, rods=False, ph=0.5)
    return {}


def s_throw(cr, t, tl, t0, t1):
    c = cues(tl, "mt7")
    tF = c["F"]
    hall(cr)
    red_spot(cr, 420, G - 700, 600, 0.6 * prog(t, c["A"] - 0.2, 0.4))
    swing = keyed(t, [(0, (-0.4, -1.4)), (tF - 0.35, (-2.8, -0.6)), (tF, (-1.2, 0.2))], dur=0.22)
    pm = mt(cr, t, 400, 1.05, mood="angry", front=swing, backa=(0.4, -0.6), head=0.12, hits=[(tF, 0.6)])
    hx, hy = to_user(cr, pm["handF"])
    if t < tF:
        prop(cr, "mt_haar", hx, hy - 10, 0.55, 0.3)
    else:
        u = t - tF
        x0, y0 = hx, hy
        prop(cr, "mt_haar", x0 + 900 * u, y0 - 700 * u + 900 * u * u, 0.55, 6 * u, alpha=clamp(1.2 - u))
        for i in range(9):
            ang = -1.2 + 0.3 * i
            v = 420 + 60 * (i % 3)
            bx = x0 + 600 * u + v * math.cos(ang) * u
            by = y0 - 400 * u + v * math.sin(ang) * u + 1200 * u * u
            prop(cr, "mt_bead", bx, by, 0.8, alpha=clamp(1.6 - u))
    return dict(flash=flash_at(t, tF, 0.3))


def s_fear(cr, t, tl, t0, t1):
    c = cues(tl, "mt8")
    tN, tB = c["N"], c["B"]
    hall(cr, 0.7)
    kai(cr, t, 650, 0.82, front=HEART["front"] if t > tN else (-0.1, -0.3), head=0.12 * (t > tN), ph=0.2,
        hits=[(tN, 0.4), (c["X"], 0.5)])
    mt(cr, t, 420, 0.8, mood="sly", front=(-1.7, -0.9), backa=(0.3, -0.4), head=0.18, hits=[(c["D"], 0.3)])

    def ui(cr_):
        q = cloud_vision(cr_, t, c["D"] + 0.2, 560, 640, 1.25)
        if q <= 0.01:
            return
        a1 = q * (1 - prog(t, tB - 0.3, 0.3))
        if a1 > 0.01 and t > tN - 0.3:
            v = prog(t, tN - 0.3, 0.3) * a1
            lady(cr_, MC.KAUSALYA, "mt_kausalya", t, 690, 0.46, feet=900, alpha=v, rods=False, flip=True)
            pk = kai(cr_, t, 450, 0.38, feet=900, alpha=v, rods=False, front=(-1.6 - 0.4 * math.sin(t * 6), -0.3))
            prop(cr_, "mt_fan", *to_user(cr_, pk["handF"]), 0.45, 0.6 + 0.3 * math.sin(t * 6), alpha=v)
        if t > tB - 0.3:
            v = prog(t, tB - 0.3, 0.3) * q
            x, bob, rock, ph = hop_walk(t, tB, tB + 3.0, 520, 760, 0.42)
            pb = bharata(cr_, t, x, 0.42, y=900 - 434 * 0.42 + bob, legs=walk_legs(ph), rot=rock, alpha=v,
                         rods=False, backa=(-0.4, -0.6))
            prop(cr_, "mt_bundle", *to_user(cr_, pb["handB"]), 0.4, alpha=v)
            if t > c["X"] - 0.2:
                prop(cr_, "kk_crown", 380, 640 + 60 * prog(t, c["X"], 0.5), 0.35, 0.6 * prog(t, c["X"], 0.5),
                     alpha=v)
    return dict(ui=ui, flash=flash_at(t, c["X"], 0.15))


def s_boons(cr, t, tl, t0, t1):
    c = cues(tl, "mt9")
    tW, tV = c["W"], c["V"]
    hall(cr, 0.7)
    kai(cr, t, 700, 0.86, flip=True, front=HEART["front"], backa=HEART["backa"], head=0.1, hits=[(c["D"], 0.5)])
    mt(cr, t, 330, 0.82, mood="sly", front=(-1.5, -0.4), head=0.1, hits=[(c["Y"], 0.4)])

    def ui(cr_):
        q = cloud_vision(cr_, t, tW - 0.3, 540, 640, 1.2)
        if q <= 0.01:
            return
        dasha(cr_, t, 600, 0.32, kneel="mt_dasha_kneel", feet=860, alpha=q, rods=False, head=0.25, flip=True,
              front=(-0.2, -0.3))
        kai(cr_, t, 440, 0.32, feet=860, alpha=q, rods=False, front=(-1.3, -0.6), backa=(-1.1, -0.8))
        if t > tV - 0.3:
            v = prog(t, tV - 0.3, 0.4) * q
            for i, ox in enumerate((440, 640)):
                orb(cr_, t, ox, 520, 34, prog(t, tV - 0.3 + 0.25 * i, 0.3) * v)
    return dict(ui=ui)


def s_two(cr, t, tl, t0, t1):
    c = cues(tl, "mt10")
    tB, tS = c["B"], c["S"]
    ground(cr)
    forest(cr, t, feet=G, hut_a=0.0, trees=((1010, 0.75, 4, 0.9, True), (880, 0.5, 10, 0.5, False)))
    bx, by = to_user(cr, bharata(cr, t, 260, 0.82, feet=G, front=ANJ[0], backa=ANJ[1], ph=0.3)["top"])
    x1, y1, u1, _ = fly(t, tB, 0.7, (300, 520), (bx + 6, by - 40), 120)
    orb(cr, t, 300 if t < tB else x1, 520 if t < tB else y1, 40, 1 - prog(t, tB + 0.6, 0.3))
    if t > tB + 0.5:
        prop(cr, "kk_crown", bx + 6, by - 40, 0.5, alpha=prog(t, tB + 0.5, 0.3))
        warm(cr, bx, by, 180, 0.6)
    orb(cr, t, 760, 520, 40, 1 - prog(t, tS + 0.4, 0.3))
    burst(cr, t, 760, 520, tS + 0.3, rmax=360, alpha=0.7)
    if t > tS + 0.2:
        x, bob, rock, ph = hop_walk(t, tS + 0.2, t1 + 1.5, 620, 1010, 0.5)
        rama(cr, t, x, 0.78, legs=walk_legs(ph), rot=rock, y=G - 434 * 0.78 + bob, alpha=prog(t, tS + 0.2, 0.3))
    return dict(flash=flash_at(t, c["V"], 0.15))


ANJ = ((-0.75, -1.85), (-0.8, -1.8))


def s_question(cr, t, tl, t0, t1):
    c = cues(tl, "mt11")
    ground(cr)
    glow(cr, 540, G - 420, 380, 0.9)
    mt(cr, t, 540, 0.9, mood="sly", front=(-1.2, 0.3), backa=(-0.9, 0.4), head=0.1, hits=[(c["D"], 0.4)])

    def ui(cr_):
        qmark(cr_, t, c["Q"] - 0.2, 560, 560, 300)
    return dict(ui=ui, night=0.45)


def shield(cr, t, x, y, r, a):
    if a <= 0.01:
        return
    for k, w in ((1.0, 16), (0.94, 6)):
        cr.new_path()
        cr.arc(x, y, r * k, math.pi * 1.02, math.pi * 1.98)
        cr.set_source_rgba(1.0, 0.85, 0.40, (0.55 if w > 10 else 0.9) * a)
        cr.set_line_width(w)
        cr.stroke()
    warm(cr, x, y - r * 0.6, r, 0.3 * a)


def s_ravana(cr, t, tl, t0, t1):
    c = cues(tl, "mt12")
    tD, tA = c["D"], c["A"]
    ground(cr)
    rs = 0.9
    rv(cr, t, 780, G - 434 * rs, rs, flip=True, mood="laugh" if t > tD else "calm",
       ang=rv_angles(t, front=(-0.2, -1.3), hits=[(tD, 0.5)]))
    shield(cr, t, 780, G, 600, prog(t, c["R"] - 0.2, 0.4))
    for i in range(3):                                   # arrows of light from the gods, bouncing off
        ts = tD - 0.1 + 0.35 * i
        if t > ts:
            u = t - ts
            hx, hy = 420 - 20 * i, G - 520 - 90 * i
            if u < 0.3:
                x, y = 60 + (hx - 60) * u / 0.3, 300 + i * 60 + (hy - 300 - i * 60) * u / 0.3
            else:
                x, y = hx - 500 * (u - 0.3), hy - 600 * (u - 0.3) + 900 * (u - 0.3) ** 2
            trail(cr, [(x - 60, y - 40), (x, y)], clamp(1.4 - u))
            if 0.28 < u < 0.6:
                sparkle(cr, hx, hy, 60, 1 - (u - 0.28) / 0.32)
    if t > tA - 0.3:
        b, k, a = depth(t, tA - 0.3, 0.45)
        rama(cr, t, 170, 0.8 * k, alpha=a, blur=b, front=(-2.1, 0.0), backa=(-2.0, -0.1), feet=G, ph=0.4,
             hits=[(c["H"], 0.4)])
    return dict(night=0.2, flash=flash_at(t, c["H"], 0.2))


def s_palace(cr, t, tl, t0, t1):
    c = cues(tl, "mt13")
    prop(cr, "lr_palace", 300, 1220, 0.7, blur=3)
    ground(cr, 1240, a=0.6)
    prop(cr, "kk_throne", 300, 1240, 0.62)
    tx, ty = to_user(cr, rama(cr, t, 300, 0.62, feet=1240, front=(-0.2, -0.4), ph=0.3, hits=[(c["R"], 0.3)])["top"])
    prop(cr, "kk_crown", tx + 4, ty - 34, 0.38)
    warm(cr, tx, ty, 140, 0.5)
    rs = 0.34
    rv(cr, t, 880, 1240 - 434 * rs, rs, flip=True, mood="laugh", alpha=prog(t, c["V"] - 0.3, 0.4), blur=4)
    path = arc_path((420, 1180), (820, 1180), 220, 60)
    dots_path(cr, path, prog(t, c["P"], 1.4), col=(0.25, 0.15, 0.06), a=0.8)

    def ui(cr_):
        qmark(cr_, t, c["K"] - 0.1, 620, 920, 220)
    return {"ui": ui}


def puffs(cr, x, y, s, a=0.8):
    """A soft heaven cloud: overlapping pale puffs with a light ink edge."""
    for dx, dy, r in ((-150, 20, 90), (-60, -30, 120), (70, -20, 110), (160, 25, 85), (0, 40, 100)):
        cr.new_path()
        cr.arc(x + dx * s, y + dy * s, r * s, 0, 2 * math.pi)
        cr.set_source_rgba(0.30, 0.18, 0.06, 0.35 * a)
        cr.set_line_width(5)
        cr.stroke_preserve()
        cr.set_source_rgba(1.0, 0.97, 0.88, a)
        cr.fill()


def s_heaven(cr, t, tl, t0, t1):
    c = cues(tl, "mt14")
    """Ramcharitmanas, Ayodhya Kand 11-12: the gods' prayers rise as lights; Saraswati appears with her veena; a ribbon
    of her light comes down to Manthara on earth and goes into her head; her face turns (sly to a thin smile)."""
    tB, tG, tD, tP, tM = c["B"], c["G"], c["D"], c["P"], c["M"]
    glow(cr, 560, 560, 700, 0.9)
    for x, y, s_ in ((180, 930, 0.9), (560, 990, 1.1), (920, 930, 0.85)):
        puffs(cr, x, y + 10 * math.sin(t + x), s_)
    lights(cr, t, 560, 1150, 380, 16, prog(t, tB - 0.2, 0.4) * (1 - prog(t, tD, 0.6)))      # the gods' prayers rise
    sa = prog(t, tG - 0.4, 0.5)
    if sa > 0.01:
        glow(cr, 560, 640, 300, sa)
        warm(cr, 560, 600, 260, 0.8 * sa)
        lady(cr, MC.SARAS, "mt_saras", t, 560, 0.6, feet=940, alpha=sa, rods=False, ph=0.6,
             front=keyed(t, [(0, (-0.9, -1.2)), (tD, (-1.0, 0.2))]), backa=(-0.5, -1.4), hits=[(tG, 0.4)])
        prop(cr, "mt_veena", 540, 720, 0.45, 0.4, alpha=sa)
    ground(cr, a=0.75)
    head = (548, G - 590)
    mood = "smile" if t > tM - 0.1 else "sly"
    mt(cr, t, 540, 0.62, mood=mood, head=0.12 + 0.1 * prog(t, tP, 0.3), hits=[(tP, 0.5), (tM, 0.4)], ph=0.3)
    if t > tD - 0.1:
        u = clamp((t - tD + 0.1) / max(0.6, tP - tD))
        pts = arc_path((630, 760), head, -140, 50, u)
        trail(cr, pts, 1 - prog(t, tP + 0.2, 0.4))
        if t < tP:
            orb(cr, t, *pts[-1], 26, 1.0)
    if t > tP - 0.05:
        burst(cr, t, head[0], head[1], tP - 0.05, n=14, rmax=260, alpha=0.8)
        red_spot(cr, head[0], head[1], 220, 0.6 * prog(t, tM - 0.1, 0.3))
    return dict(flash=flash_at(t, tM, 0.3))


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "mt15")
    hook_set(cr, t)
    tC, tR = c["C"], c["R"]
    rs = 0.26
    rv(cr, t, 1010, FAR - 120 - 434 * rs, rs, flip=True, mood="laugh", alpha=prog(t, tR - 0.4, 0.4), blur=6,
       rods=False)
    x, bob, rock, ph = hop_walk(t, t0, t1 + 1.0, 780, 930, 0.5)
    rama(cr, t, x, 0.5, legs=walk_legs(ph), rot=rock, y=FAR - 434 * 0.5 + bob, ph=0.4)
    pm = mt(cr, t, HK_M[0], HK_M[1], mood="smile", front=(-1.45, -0.1), backa=(0.3, -0.5), head=0.16,
            hits=[(c["V"], 0.4)], feet=G + 40)
    if t > tC - 0.2:
        path = arc_path(to_user(cr, pm["handF"]), (x, FAR - 260), 160, 50, prog(t, tC - 0.2, 0.8))
        trail(cr, path, 0.9)
    if t > tR - 0.2:
        path = arc_path((x + 40, FAR - 300), (990, FAR - 360), 120, 40, prog(t, tR - 0.2, 0.7))
        trail(cr, path, 0.9)
    return {}


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "mt16")
    tG, tD = c["G"], c["D"]
    ground(cr)
    glow(cr, 540, G - 360, 380, 0.6)
    look = 1 if (t > tD and int((t - tD) / 0.9) % 2 == 0) else -1
    mt(cr, t, 540, 0.72, mood="sly", flip=look < 0, front=(-0.4, -0.6), hits=[(tG, 0.3), (tD, 0.3)], ph=0.3)
    cards = ((280, "दासी?", "घर तोड़ने वाली", tG - 0.1), (800, "मोहरा?", "देवताओं की चाल का", tD - 0.1))

    def ui(cr_):
        for cx, big, small, tc in cards:
            hcard(cr_, t, tc - 0.2, cx, 560, big, small)
        if t > tD + 0.3:
            n = int((t - tD - 0.3) / 0.9)
            k = n % 2
            red_ring(cr_, cards[k][0], 564, 230, 150, prog(t, tD + 0.3 + 0.9 * n, 0.35), 9)
    return dict(ui=ui, night=0.25, flash=flash_at(t, c["M"], 0.12))


# ------------------------------------------------------------------ labels


LABELS = {
    "mt1": [(0.3, "रामायण मूवी देखी?", dict(y=330, size=80)),
            ("C", "राम: 14 साल जंगल में", dict(y=330, size=80)),
            ("D", "वजह: एक कुबड़ी दासी", dict(y=330, size=84)),
            ("M", "मंथरा", dict(y=330, size=120, col=RED, under=True))],
    "mt2": [("Q", "पर क्यों?", dict(y=360, size=100, col=RED)),
            ("M", "जवाब: तुलसी रामायण में", dict(y=360, size=80))],
    "mtF": [(0.05, "राजा दशरथ की 3 रानियाँ", dict(y=300, size=80)),
            ("R", "बड़ी रानी का बेटा: राम", dict(y=300, size=80)),
            ("B", "कैकेयी का बेटा: भरत", dict(y=300, size=80, col=RED))],
    "mt3": [("D", "मंथरा: कैकेयी की दासी", dict(y=330, size=80)),
            ("Y", "मायके से साथ आई", dict(y=330, size=84))],
    "mt4": [("C", "मंथरा ने देखा...", dict(y=300)),
            ("S", "सजी हुई अयोध्या", dict(y=300, size=84)),
            ("R", "कल: राम राजा!", dict(y=300, size=96, col=RED, under=True))],
    "mt5": [("M", "मंथरा भागी!", dict(y=330, size=96)),
            ("U", "उठो रानी!", dict(y=330, size=100)),
            ("X", "मुसीबत!", dict(y=330, size=110, col=RED, under=True))],
    "mt6": [("K", "कैकेयी खुश!", dict(y=330, size=96)),
            ("P", "राम बहुत प्यारे", dict(y=330, size=84)),
            ("G", "इनाम: गहना", dict(y=330, size=90))],
    "mt7": [("A", "ग़ुस्सा!", dict(y=330, size=100, col=RED)),
            ("F", "गहना फेंका!", dict(y=330, size=104, col=RED, under=True))],
    "mt8": [("N", "बड़ी रानी की नौकरानी", dict(y=250, size=72)),
            ("B", "भरत: देश से बाहर!", dict(y=250, size=80, col=RED))],
    "mt9": [("D", "कैकेयी डर गई", dict(y=250, size=84)),
            ("W", "युद्ध में राजा की जान बचाई", dict(y=250, size=66)),
            ("V", "दो वरदान", dict(y=250, size=104, col=RED, under=True)),
            ("Z", "जो माँगो, वो मिलेगा", dict(y=250, size=84))],
    "mt10": [("B", "1: भरत को राज", dict(y=330, size=90)),
             ("S", "2: राम को 14 साल वनवास", dict(y=330, size=72, col=RED)),
             ("K", "राम जंगल गए", dict(y=330, size=96))],
    "mt11": [("D", "दासी को क्या मिलता?", dict(y=1600, size=84))],
    "mt12": [(0.05, "तुलसी रामायण का छुपा राज़", dict(y=330, size=78)),
             ("D", "देवता परेशान", dict(y=330, size=96)),
             ("A", "अंत: सिर्फ़ राम के हाथों", dict(y=330, size=84, col=RED, under=True))],
    "mt13": [("P", "राजा बनकर महल में रहते...", dict(y=330, size=76)),
             ("V", "तो रावण तक कैसे?", dict(y=330, size=96, col=RED))],
    "mt14": [("B", "देवताओं की विनती", dict(y=300, size=88)),
             ("G", "विद्या की देवी: सरस्वती", dict(y=300, size=80)),
             ("P", "मंथरा की बुद्धि फेर दी", dict(y=300, size=84, col=RED, under=True))],
    "mt15": [("V", "विलेन?", dict(y=330, size=110)),
             ("C", "उसी की वजह से...", dict(y=330, size=90)),
             ("R", "राम पहुँचे रावण तक", dict(y=330, size=82, col=RED, under=True))],
    "mt16": [(0.05, "मंथरा क्या थी?", dict(y=300, size=96))],
}


def labels(cr, t, tl, bid, t1):
    specs = LABELS.get(bid, [])
    if not specs:
        return
    c = cues(tl, bid)
    starts = [c["t0"] + w if isinstance(w, (int, float)) else c[w] - 0.1 for w, _, _ in specs]
    if bid == "mt1":
        starts[0] = 0.25
    for i, (_, text, kw) in enumerate(specs):
        kw = dict(kw)
        t_out = kw.pop("out", None)
        if t_out is None:
            t_out = starts[i + 1] - 0.15 if i + 1 < len(starts) else t1 - 0.12
        label(cr, t, starts[i], text, t_out=t_out, **kw)


# ------------------------------------------------------------------ the cut list and the frame


DUSK = (1.0, 0.62, 0.42)
PALACE = (1.0, 0.82, 0.62)
DAWN = (1.0, 0.74, 0.52)
ANGER = (1.0, 0.55, 0.45)
NIGHT_BLUE = (0.55, 0.66, 1.0)
HEAVEN = (1.0, 0.92, 0.70)
GOLDC = (1.0, 0.86, 0.58)

SHOTS = [   # (line, draw function, options: zoom range, focus, place colour (rgb, strength), night)
    ("mt1", s_hook, dict(z=(1.0, 1.05), focus=(400, 1100), place=(DUSK, 0.45))),
    ("mt2", s_why, dict(z=(1.1, 1.15), focus=(540, 1125), place=(PALACE, 0.25))),
    ("mtF", s_family, dict(z=(1.0, 1.03), focus=(540, 1100), place=(PALACE, 0.3))),
    ("mt3", s_who, dict(z=(1.08, 1.12), focus=(560, 1100), place=(PALACE, 0.3))),
    ("mt4", s_city, dict(z=(1.0, 1.06), focus=(540, 900), place=(DAWN, 0.35))),
    ("mt5", s_alarm, dict(z=(1.08, 1.12), focus=(540, 1100), place=(PALACE, 0.3))),
    ("mt6", s_happy, dict(z=(1.1, 1.15), focus=(540, 1125), place=(GOLDC, 0.3))),
    ("mt7", s_throw, dict(z=(1.25, 1.3), focus=(470, 1515), place=(ANGER, 0.45))),
    ("mt8", s_fear, dict(z=(1.0, 1.03), focus=(540, 1000), place=(PALACE, 0.3), night=0.15)),
    ("mt9", s_boons, dict(z=(1.0, 1.03), focus=(540, 1000), place=(PALACE, 0.3), night=0.15)),
    ("mt10", s_two, dict(z=(1.05, 1.1), focus=(540, 1100), place=(DUSK, 0.35))),
    ("mt11", s_question, dict(z=(1.15, 1.2), focus=(540, 1342), place=(NIGHT_BLUE, 0.4))),
    ("mt12", s_ravana, dict(z=(1.05, 1.1), focus=(540, 1100), place=(ANGER, 0.3))),
    ("mt13", s_palace, dict(z=(1.0, 1.05), focus=(540, 1100), place=(DAWN, 0.25))),
    ("mt14", s_heaven, dict(z=(1.0, 1.04), focus=(540, 1000), place=(HEAVEN, 0.3))),
    ("mt15", s_callback, dict(z=(1.0, 1.05), focus=(400, 1100), place=(GOLDC, 0.45))),
    ("mt16", s_end, dict(z=(1.0, 1.03), focus=(540, 1200), frames=[(1.0, (540, 1200))])),   # cards: stay wide
]


def shot_at(t, tl):
    cache = getattr(tl, "_mt_shots", None)
    if cache is None:
        starts = [0.0]
        for bid, _, _ in SHOTS[1:]:
            starts.append(max(T(tl, FIRST[bid]) - 0.12, starts[-1] + 0.5))
        cache = tl._mt_shots = starts
    k = 0
    for i, s in enumerate(cache):
        if t >= s:
            k = i
    return k, cache[k], cache[k + 1] if k + 1 < len(cache) else tl.total


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl)
    bid, fn, opt = SHOTS[k]
    z, (fx, fy) = camera_beats.camera(tl, t, t0, t1, opt)     # a new framing every line, no hold > 2.6 s
    cr.save()
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    pc.screen(cr)
    out = fn(cr, t, tl, t0, t1) or {}
    tint(cr, (1.0, 0.66, 0.42), out.get("eve", 0.0))
    if opt.get("place"):
        col, a = opt["place"]
        tint(cr, col, a)
    if out.get("ui"):
        out["ui"](cr)
    cr.restore()
    motes(cr, t)
    pc.lamp(cr, t, night=max(out.get("night", 0.0), opt.get("night", 0.0)), flash=out.get("flash", 0.0))
    labels(cr, t, tl, bid, t1)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """Sparse sounds, most important first, each at least SFX_MIN_GAP apart: a damaru as the hook opens on Manthara,
    a hit as she throws the necklace, a conch on Rama's exile, shimmer as the heavenly singer is born as Manthara,
    a bell on the closing question; dips before the reveals."""
    c = {b: cues(tl, b) for b in CUES}
    t_end = min(c["mt16"]["D"], tl["m36"].end - 0.05)
    want = [(c["mt1"]["M"], "damaru", 0), (c["mt7"]["F"], "hit", 0), (c["mt14"]["P"], "shimmer", 0),
            (c["mt10"]["V"], "conch", 0), (t_end, "bell", 0), (c["mt4"]["R"], "bell", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["mt7"]["F"] - 0.3, "dip", 0.45), (c["mt14"]["P"] - 0.3, "dip", 0.5)]
    kept = [(after_voice(tl, a), n, d) for a, n, d in kept]          # never over a spoken word
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]


def after_voice(tl, a):
    """A sound effect time moved out of any spoken line into the pause right after it, so no effect covers a word."""
    for b in tl.beats:
        if b.start - 0.15 <= a < b.end:
            return b.end + 0.06 if b.end + 1.0 < tl.total else max(0.0, b.start - 0.3)   # last line: just before it
    return a
