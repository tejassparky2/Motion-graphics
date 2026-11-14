"""Scenes for videos/jatayu.py: who Jatayu was and why he fought Ravana for Sita (Valmiki Ramayana, Aranya Kanda 14,
50, 51, 68; Ayodhya Kanda 76), in Togalu Gombeyaata shadow puppets drawn in code, built on the lessons from the
owner's Ashtavakra reference: frame 0 is the fight itself (the old vulture flying at Ravana's chariot), short Hindi
labels, a colour for each place, close shots where a face matters, a callback in gold.

Respect: no blood anywhere. The wings are cut in a white flash and fall as leather pieces; the pyre is logs and a soft
glow, with no body in the fire.

Shot list (line: what is on the screen)
  jt1   HOOK: dusk sky; Jatayu big on the left, wings beating, talons out, at Ravana's flying chariot (Sita in it)
  jt2   Sita in the chariot, afraid; a single feather falls; a red "?"
  jt3   Jatayu perched on a big branch, crowned, white-browed; a counter runs up to 60,000
  jt4   the forest path: Rama, his brother and Sita walk in; the huge vulture on a tree above them
  jt5   Rama raises his bow (a demon?); Jatayu bows his head; a bubble: Jatayu beside King Dasharatha, friends
  jt6   the leaf hut: Jatayu spreads a wing over Sita (a gold ring of protection); the brothers walk off
  jt7   the chariot crosses the sky with Sita; below, Jatayu asleep on the tree wakes with a start
  jt8   Jatayu hovers in front of the chariot; Ravana with his bow
  jt9   Jatayu small before a huge dark Ravana; a red "?"
  jt10  close fight: the bow snaps, the chariot splits, the charioteer falls
  jt11  Jatayu tired; Ravana draws a sword; a white flash, the wings fall away as leather pieces
  jt12  Jatayu on the ground; Rama kneels by him; Jatayu lifts his head; an arrow points south
  jt13  a sepia memory: Ayodhya, a pyre lit by the younger brother; Rama far away in the forest, head bowed
  jt14  Rama sets the torch to Jatayu's pyre; a soft glow rises
  jt15  CALLBACK: the jt5 framing in gold; Jatayu's light rises into the sky
  jt16  two cards (हारा? / जीता?), a red ring alternating; Jatayu small between them
"""
import math

import cairo

import dharmavyadha_cast as DV
import jatayu_cast as JC
import kaikeyi_cast as K
import lrekha_cast  # noqa: F401  (registers the leaf hut)
import camera_beats
import puppet_core as pc
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import clamp, draw_text, ease, prog
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, register
from scenes_ashtavakra2 import hcard, label, red_spot
from scenes_hanuman_curse import arc_path, qmark
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, motes, red_ring, walk_legs
from scenes_jayadratha import flash_at, tint, to_user
from scenes_kaikeyi import dasha, fig, rama
from scenes_lakshman_rekha import HEART, forest, lakshmana, sita
from scenes_mandhata import lights, warm
from scenes_manthara import dots_path, ground, puffs
from scenes_ravana import rv, rv_angles
from scenes_ruru import sepia
from shots import T

G = FEET + 120
FAR = FEET
MISSES = set()
register("jt_rama_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, K.RAMA_SKIN, K.GOLD, K.DRED, 1.05))

FIRST = {"jt1": "j01", "jt2": "j04", "jt3": "j07", "jt4": "j09", "jt5": "j11", "jt6": "j14", "jt7": "j16",
         "jt8": "j18", "jt9": "j21", "jt10": "j22", "jt11": "j24", "jt12": "j26", "jt13": "j30", "jt14": "j32",
         "jt15": "j34", "jt16": "j35"}          # each shot's first line (a shot covers several lines)

# Every cue of every shot: (name, line, word, fraction fallback, ((after, min gap), ...)); "t0" = the shot's start.
CUES = {
    "jt1": (("R", "j02", "रावण", 0.1, (("t0", 1.0),)), ("G", "j03", "गिद्ध", 0.6, (("R", 0.6),)),
            ("J", "j03", "जटायु", 0.85, (("G", 0.3),))),
    "jt2": (("S", "j04", "सीता", 0.05, (("t0", 0.0),)), ("J", "j05", "जान", 0.8, (("S", 1.0),)),
            ("Q", "j06", "क्यों", 0.8, (("J", 0.5),))),
    "jt3": (("R", "j07", "राजा", 0.8, (("t0", 0.4),)), ("B", "j08", "बूढ़ा", 0.4, (("R", 0.4),)),
            ("S", "j08", "साठ", 0.7, (("B", 0.4),))),
    "jt4": (("R", "j09", "राम", 0.05, (("t0", 0.0),)), ("J", "j09", "जंगल", 0.8, (("R", 0.8),)),
            ("P", "j10", "पेड़", 0.3, (("J", 0.5),)), ("V", "j10", "विशाल", 0.75, (("P", 0.3),))),
    "jt5": (("L", "j11", "लगा", 0.3, (("t0", 0.3),)), ("K", "j11", "राक्षस", 0.7, (("L", 0.2),)),
            ("D", "j12", "डरो", 0.75, (("K", 0.6),)), ("F", "j13", "दोस्त", 0.85, (("D", 0.6),))),
    "jt6": (("B", "j14", "बाहर", 0.35, (("t0", 0.4),)), ("S", "j14", "सीता", 0.7, (("B", 0.4),)),
            ("R", "j14", "रखवाली", 0.85, (("S", 0.3),)), ("W", "j15", "वादा", 0.8, (("R", 0.6),))),
    "jt7": (("U", "j16", "उठाकर", 0.5, (("t0", 0.4),)), ("A", "j16", "आसमान", 0.7, (("U", 0.4),)),
            ("C", "j17", "चीख", 0.15, (("A", 0.6),)), ("S", "j17", "सोया", 0.6, (("C", 0.6),)),
            ("J", "j17", "जाग", 0.88, (("S", 0.4),))),
    "jt8": (("O", "j18", "रास्ता", 0.6, (("t0", 0.3),)), ("B", "j19", "बूढ़ा", 0.25, (("O", 0.5),)),
            ("J", "j19", "जवान", 0.45, (("B", 0.5),)), ("R", "j19", "रथ", 0.75, (("J", 0.5),)),
            ("D", "j19", "धनुष", 0.85, (("R", 0.3),)), ("N", "j20", "जीते", 0.3, (("D", 0.6),))),
    "jt9": (("A", "j21", "अकेले", 0.5, (("t0", 0.6),)), ("Q", "j21", "जीत", 0.8, (("A", 0.6),))),
    "jt10": (("P", "j22", "पंजों", 0.3, (("t0", 0.3),)), ("D", "j22", "धनुष", 0.7, (("P", 0.4),)),
             ("R", "j23", "रथ", 0.15, (("D", 0.9),)), ("S", "j23", "चलाने", 0.6, (("R", 0.8),))),
    "jt11": (("B", "j24", "बूढ़ा", 0.3, (("t0", 0.2),)), ("Y", "j24", "थक", 0.8, (("B", 0.5),)),
             ("T", "j25", "तलवार", 0.3, (("Y", 0.6),)), ("K", "j25", "काट", 0.85, (("T", 0.8),))),
    "jt12": (("G", "j26", "गिर", 0.6, (("t0", 0.3),)), ("R", "j27", "राम", 0.3, (("G", 0.6),)),
             ("A", "j28", "बताया", 0.3, (("R", 0.4),)), ("D", "j28", "दक्षिण", 0.7, (("A", 0.6),)),
             ("Z", "j29", "दम", 0.7, (("D", 0.8),))),
    "jt13": (("J", "j30", "जंगल", 0.25, (("t0", 0.3),)), ("P", "j30", "पिता", 0.6, (("J", 0.5),)),
             ("G", "j30", "गुज", 0.8, (("P", 0.3),)), ("A", "j31", "आग", 0.75, (("G", 1.0),))),
    "jt14": (("H", "j32", "हाथों", 0.75, (("t0", 0.8),)), ("A", "j32", "आग", 0.9, (("H", 0.3),)),
             ("B", "j33", "बेटा", 0.6, (("A", 0.8),))),
    "jt15": (("D", "j34", "दोस्त", 0.3, (("t0", 0.6),)), ("P", "j34", "पिता बनकर", 0.7, (("D", 0.8),)),
             ("V", "j34", "विदा", 0.9, (("P", 0.4),))),
    "jt16": (("H", "j35", "हारा", 0.45, (("t0", 0.8),)), ("J", "j35", "जीता", 0.65, (("H", 0.5),))),
}


def cue(tl, line, word, frac):
    try:
        return T(tl, line, {"hi": word})
    except (KeyError, ValueError):
        MISSES.add((line, word))
        return T(tl, line, frac)


def cues(tl, shot):
    cache = getattr(tl, "_jt_cues", None)
    if cache is None:
        cache = tl._jt_cues = {}
    if shot not in cache:
        out = {"t0": T(tl, FIRST[shot])}
        for name, line, word, frac, cons in CUES[shot]:
            v = cue(tl, line, word, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[shot] = out
    return cache[shot]


# ------------------------------------------------------------------ Jatayu and the sets

PERCH = 315.0                         # body pivot height above the feet (design units)


def jt(cr, t, x, y, s, mood="calm", wing=0.0, flap=0.0, legs=(0.0, 0.0), head=0.0, flip=False, rot=0.0, alpha=1.0,
       blur=0.0, hide=(), rods=True, rate=2.2):
    """Jatayu with his body pivot at (x, y). wing: both wings' lift (0 folded); flap: beat amplitude."""
    w = flap * math.sin(2 * math.pi * rate * t)
    ang = {"jt_wingF": wing + w, "jt_wingB": wing * 0.85 + flap * math.sin(2 * math.pi * rate * t - 0.5),
           "jt_legF": legs[0], "jt_legB": legs[1], "jt_head": head + 0.03 * math.sin(t * 1.7)}
    swap = {"jt_head": "jt_head" + ("" if mood == "calm" else "_" + mood)}
    bob = -18 * flap * math.sin(2 * math.pi * rate * t + 1.0) if flap else 0.0
    return puppet(cr, JC.JATAYU, x, y + bob * s, s, rot + bob_rot(t, x * 0.01, 0.008), flip, ang, alpha, blur,
                  hide=hide, swap=swap, rods=rods)


def perched(cr, t, x, foot_y, s, **kw):
    return jt(cr, t, x, foot_y - PERCH * s, s, **kw)


def sky(cr, t, dusk=1.0):
    glow(cr, 540, 760, 760, 0.8)
    for x, y, s_ in ((170, 520, 0.8), (900, 430, 0.7), (560, 1500, 1.0), (120, 1560, 0.8), (980, 1620, 0.9)):
        puffs(cr, x + 30 * math.sin(t * 0.3 + x), y, s_, 0.55)


def ravana_car(cr, t, cx, floor, s, sita_on=True, bow_on=False, mood="angry", alpha=1.0, blur=0.0, sita_kw=None,
               rv_front=(-0.9, -0.4)):
    """Ravana standing in his flying chariot (facing left), Sita beside him; returns Ravana's points."""
    if sita_on:
        kw = dict(front=(-2.3, 0.2), backa=(-2.0, 0.3), head=-0.05)
        kw.update(sita_kw or {})
        sita(cr, t, cx + 150 * s, 0.85 * s, feet=floor - 60 * s, alpha=alpha, blur=blur, rods=False, ph=1.1, **kw)
    rs = 0.92 * s
    pts = rv(cr, t, cx - 40 * s, floor - 60 * s - 434 * rs, rs, flip=True, mood=mood, alpha=alpha, blur=blur,
             ang=rv_angles(t, front=rv_front, backa=(0.3, -0.4)), rods=False)
    if bow_on:
        hx, hy = to_user(cr, pts["handF"])
        prop(cr, "jt_bow", hx, hy, 0.55 * s, alpha=alpha)
    prop(cr, "jt_chariot", cx, floor, s, alpha=alpha, blur=blur)
    return pts


def tree_set(cr, x=820, s=1.0, alpha=1.0, blur=0.0):
    """The big tree (branch tip at x - 380 s, G - 846 s)."""
    prop(cr, "dv_tree", x, G, s, alpha=alpha, blur=blur)
    return x - 380 * s, G - 846 * s


def counter(cr, t, t_on, x, y, size, n=60000, dur=1.4):
    if t < t_on:
        return
    u = ease(clamp((t - t_on) / dur))
    v = int(n * u / 1000) * 1000 if u < 1 else n
    draw_text(cr, f"{v:,}", x, y, size, RED, prog(t, t_on, 0.2), anchor="cm")


# ------------------------------------------------------------------ the shots


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "jt1")
    sky(cr, t)
    cx = 850 - 40 * clamp(t / 8)
    ravana_car(cr, t, cx, 1300, 0.6, sita_kw=dict(front=(-2.4 + 0.2 * math.sin(t * 3), 0.2)))
    red_spot(cr, 400, 860, 420, 0.5 * prog(t, c["J"] - 0.1, 0.4))
    jt(cr, t, 400 + 20 * math.sin(t * 1.3), 900, 0.72, mood="fierce", wing=0.9, flap=0.55, legs=(-0.9, -0.6),
       head=-0.1, rate=2.4)
    return dict(flash=flash_at(t, c["J"], 0.25), night=0.1)


def s_sita(cr, t, tl, t0, t1):
    c = cues(tl, "jt2")
    sky(cr, t)
    ravana_car(cr, t, 600, 1500, 0.95, mood="calm", sita_kw=dict(front=HEART["front"], backa=HEART["backa"],
                                                                head=0.12))
    if t > c["J"] - 0.2:
        u = t - c["J"] + 0.2
        prop(cr, "jt_feather", 220 + 60 * math.sin(u * 2.2), 520 + 260 * u, 0.7, 0.6 * math.sin(u * 1.8),
             alpha=clamp(u * 3))

    def ui(cr_):
        qmark(cr_, t, c["Q"] - 0.1, 965, 1180, 250)
    return dict(ui=ui, night=0.25 * prog(t, c["J"], 0.6))


def s_king(cr, t, tl, t0, t1):
    c = cues(tl, "jt3")
    bx, by = tree_set(cr, 1000, 0.85)
    pts = perched(cr, t, bx + 30, by, flip=True, s=0.95, head=0.05 * math.sin(t * 0.8))
    if t > c["R"] - 0.1:
        tx, ty = to_user(cr, pts["top"])
        warm(cr, tx, ty, 200, prog(t, c["R"] - 0.1, 0.4) * (0.7 + 0.3 * math.sin(t * 4)))

    def ui(cr_):
        counter(cr_, t, c["S"] - 0.1, 480, 1600, 190)
    return dict(ui=ui)


def walkers(cr, t, t_a, x_lead, s, feet, alpha=1.0, step=0.42):
    """Rama, his brother and Sita walking in a line (Rama leading, facing right)."""
    for k, (fn, dx) in enumerate(((rama, 0), (lakshmana, -190), (sita, -360))):
        x, bob, rock, ph = hop_walk(t, t_a, t_a + 3.2, x_lead - 520 + dx, x_lead + dx, step)
        if fn is sita:
            fn(cr, t, x, s * 0.92, feet=feet, alpha=alpha, ph=k)
        else:
            fn(cr, t, x, s, legs=walk_legs(ph), rot=rock, y=feet - 434 * s + bob, alpha=alpha, ph=k)


def s_path(cr, t, tl, t0, t1):
    c = cues(tl, "jt4")
    bx, by = tree_set(cr, 900, 1.0)
    ground(cr, FAR + 20, a=0.5)
    q = prog(t, c["P"] - 0.3, 0.5)
    perched(cr, t, bx + 30, by, flip=True, s=0.85 * (0.9 + 0.1 * q), alpha=0.3 + 0.7 * q, blur=6 * (1 - q))
    walkers(cr, t, t0, 470, 0.58, FAR + 60)
    return {}


def s_friend(cr, t, tl, t0, t1):
    c = cues(tl, "jt5")
    tK, tD, tF = c["K"], c["D"], c["F"]
    bx, by = tree_set(cr, 900, 1.0)
    alarm = tK - 0.2 < t < tD - 0.1
    perched(cr, t, bx + 30, by, flip=True, s=0.85, head=0.35 if t > tD - 0.1 else 0.0, wing=0.5 * prog(t, tD, 0.4))
    rama(cr, t, 300, 0.7, feet=G, front=(-2.3, -0.2) if alarm else (-0.2, -0.3), backa=(-2.2, 0.1) if alarm else
         (0.3, -0.2), hits=[(tK, 0.5), (tD, 0.3)], ph=0.3)

    def ui(cr_):
        q = prog(t, tF - 0.4, 0.4)
        if q > 0.01:
            prop(cr_, "ar_think", 680, 1330, 1.0, alpha=q)
            dasha(cr_, t, 590, 0.36, feet=1540, alpha=q, rods=False, ph=0.2)
            jt(cr_, t, 790, 1540 - PERCH * 0.33, 0.33, flip=True, alpha=q, rods=False)
    return dict(ui=ui, flash=flash_at(t, tK, 0.12))


def s_promise(cr, t, tl, t0, t1):
    c = cues(tl, "jt6")
    forest(cr, t, feet=G, hut_x=820, hut_s=0.75, hut_a=0.35, trees=((60, 0.6, 6, 0.75, True),))
    for k, (fn, x0) in enumerate(((rama, 330), (lakshmana, 170))):
        x, bob, rock, ph = hop_walk(t, c["B"] - 0.2, c["B"] + 2.8, x0, x0 - 420, 0.42)
        fn(cr, t, x, 0.62, flip=True, legs=walk_legs(ph), rot=rock, y=G - 434 * 0.62 + bob, ph=k,
           alpha=1 - prog(t, c["B"] + 2.2, 0.5))
    sita(cr, t, 460, 0.72, feet=G, ph=0.5)
    g = prog(t, c["R"] - 0.2, 0.5)
    glow(cr, 460, G - 380, 360, 0.6 * g)
    glow(cr, 900, G - 420, 300, 0.5)
    jt(cr, t, 960, G - PERCH * 0.85, 0.85, flip=True, wing=1.1 * g, head=0.15 - 0.2 * g)

    def ui(cr_):
        if g > 0.01:
            cr_.save()
            cr_.new_path()
            cr_.arc(460, G - 400, 330, 0, 2 * math.pi)
            cr_.set_source_rgba(1.0, 0.82, 0.32, 0.8 * g)
            cr_.set_line_width(10)
            cr_.stroke()
            cr_.restore()
    return dict(ui=ui)


def s_taken(cr, t, tl, t0, t1):
    c = cues(tl, "jt7")
    tJ = c["J"]
    sky(cr, t)
    u = clamp((t - c["U"] + 0.3) / max(2.0, c["S"] - c["U"]))
    bx, by = tree_set(cr, 1000, 0.8)
    awake = t > tJ - 0.1
    perched(cr, t, bx + 30, by, flip=True, s=0.8, mood="fierce" if awake else "shut", head=-0.1 if awake else 0.55,
            wing=0.6 * prog(t, tJ, 0.3))
    ravana_car(cr, t, 1180 - 800 * u, 900, 0.5, mood="laugh", sita_kw=dict(front=(-2.5, 0.2)))
    return dict(flash=flash_at(t, tJ, 0.3), night=0.15)


def s_stand(cr, t, tl, t0, t1):
    c = cues(tl, "jt8")
    sky(cr, t)
    ravana_car(cr, t, 780, 1300, 0.66, bow_on=t > c["D"] - 0.2, mood="laugh" if t < c["N"] else "angry",
               rv_front=(-1.2, -0.3))
    u = ease(clamp((t - t0) / max(0.6, c["O"] - t0)))          # he flies in and blocks the way
    jt(cr, t, -250 + 550 * u, 1080 - 200 * u, 0.72, mood="fierce", wing=0.8, flap=0.45, legs=(-0.4, -0.2),
       rate=2.0, head=keyed(t, [(0, 0.0), (c["N"], -0.15)]))
    return dict(flash=flash_at(t, c["N"], 0.15))


def s_odds(cr, t, tl, t0, t1):
    c = cues(tl, "jt9")
    ground(cr)
    rs = 1.35
    rv(cr, t, 820, G - 434 * rs, rs, flip=True, mood="laugh", alpha=0.55, blur=8, rods=False)
    perched(cr, t, 280, G, 0.45, mood="fierce", wing=0.3)

    def ui(cr_):
        qmark(cr_, t, c["Q"] - 0.2, 300, 700, 280)
    return dict(ui=ui, night=0.4)


def s_fight(cr, t, tl, t0, t1):
    c = cues(tl, "jt10")
    tD, tR, tS = c["D"], c["R"], c["S"]
    sky(cr, t)
    cx, floor, s = 720, 1380, 0.78
    drop = 260 * ease(clamp((t - tR - 0.2) / 0.8))
    if t < tR:
        pts = ravana_car(cr, t, cx, floor, s, sita_on=True, bow_on=False, rv_front=(-1.2, -0.3))
    else:
        sita(cr, t, cx + 150 * s, 0.85 * s, feet=floor - 60 * s + drop, rods=False, front=HEART["front"], ph=1.1)
        rs = 0.92 * s
        pts = rv(cr, t, cx - 40 * s, floor - 60 * s - 434 * rs + drop, rs, flip=True, mood="angry",
                 ang=rv_angles(t, front=(-0.6, -0.6)), rods=False)
        u = t - tR
        prop(cr, "jt_chariotL", cx - 60 - 240 * u, floor + 300 * u + 500 * u * u, s, -0.5 * u, alpha=clamp(1.6 - u))
        prop(cr, "jt_chariotR", cx + 60 + 260 * u, floor + 260 * u + 500 * u * u, s, 0.6 * u, alpha=clamp(1.6 - u))
    hx, hy = to_user(cr, pts["handF"])
    if t < tD:
        if t < tR:
            prop(cr, "jt_bow", hx, hy, 0.5 * s)
    else:
        u = t - tD
        prop(cr, "jt_bowT", hx - 120 * u, hy - 200 * u + 600 * u * u, 0.5 * s, -2.0 * u, alpha=clamp(1.5 - u))
        prop(cr, "jt_bowB", hx + 60 * u, hy + 100 * u + 600 * u * u, 0.5 * s, 2.0 * u, alpha=clamp(1.5 - u))
    if t > tS - 0.1:
        u = t - tS + 0.1
        fig(cr, DV.HUS, "dv_hus", t, 990 + 40 * u, 0.42, feet=1200 + 380 * u * u, rot=1.2 * u, rods=False,
            alpha=clamp(2.2 - u), front=(-2.4, 0.3), backa=(-2.2, 0.2))
    lunge = keyed(t, [(0, 0.0), (tD - 0.3, 1.0), (tD + 0.3, 0.3), (tR - 0.3, 1.0), (tR + 0.3, 0.3),
                      (tS - 0.3, 1.0), (tS + 0.3, 0.3)])
    jt(cr, t, 240 + 160 * lunge, 980 - 60 * lunge, 0.72, mood="fierce", wing=0.9, flap=0.5,
       legs=(-0.5 - 0.6 * lunge, -0.3 - 0.4 * lunge), rate=2.6)
    return dict(flash=max(flash_at(t, tD, 0.3), flash_at(t, tR, 0.3), flash_at(t, tS, 0.15)))


def s_cut(cr, t, tl, t0, t1):
    c = cues(tl, "jt11")
    tT, tK = c["T"], c["K"]
    ground(cr)
    rs = 0.82
    pts = rv(cr, t, 860, G - 434 * rs, rs, flip=True, mood="angry",
             ang=rv_angles(t, front=keyed(t, [(0, (-0.3, -0.5)), (tT, (-2.6, 0.1)), (tK - 0.05, (-1.9, 0.0)),
                                              (tK + 0.45, (-2.5, 0.1))], dur=0.18)))
    if t > tT - 0.1:
        hx, hy = to_user(cr, pts["handF"])
        ang = keyed(t, [(0, -0.6), (tT, -2.6), (tK - 0.05, -1.9), (tK + 0.45, -2.5)], dur=0.18)
        glow(cr, hx, hy - 120, 160, 0.5 * prog(t, tT - 0.1, 0.2))
        prop(cr, "ar_sword", hx, hy, 0.75, ang + math.pi, alpha=prog(t, tT - 0.1, 0.2))
    cut = t > tK
    fall = ease(clamp((t - tK - 0.1) / 0.7)) if cut else 0.0
    tired = t > c["Y"] - 0.2
    jt(cr, t, 200 + 20 * fall, 1260 + 260 * fall, 0.62, mood="tired" if tired else "fierce",
       wing=0.9 if tired else 0.7, flap=0.0 if cut else (0.12 if tired else 0.4), rate=1.2 if tired else 2.2,
       head=-0.25 * tired + 0.5 * fall, rot=0.5 * fall, hide=("jt_wingF", "jt_wingB") if cut else ())
    if cut:
        u = t - tK
        for k, (dx, sp) in enumerate(((-120, -1.0), (60, 1.3))):
            prop(cr, "jt_wing_loose", 280 + dx - 160 * u * (1 if k else -1), 1100 + 500 * u * u + 80 * u, 0.62,
                 sp * u + 0.3, alpha=clamp(2.2 - u))
    return dict(flash=max(flash_at(t, tK, 0.6, 3.0), flash_at(t, tT, 0.12)))


def lying(cr, t, x, s, head_up=0.0, alpha=1.0, feet=G):
    """Jatayu on the ground without his wings, on his side; head_up lifts his head."""
    return jt(cr, t, x, feet - 150 * s, s, mood="tired" if head_up > 0.3 else "shut", head=0.9 - 0.9 * head_up,
              rot=0.35, legs=(0.9, 0.7), hide=("jt_wingF", "jt_wingB"), alpha=alpha, rods=False)


def s_last(cr, t, tl, t0, t1):
    c = cues(tl, "jt12")
    forest(cr, t, feet=G, hut_a=0.0, trees=((80, 0.6, 6, 0.6, True), (1040, 0.7, 4, 0.8, False)))
    tR, tA, tD = c["R"], c["A"], c["D"]
    lying(cr, t, 470, 0.8, head_up=prog(t, tR, 0.6) * (1 - prog(t, c["Z"], 0.8)))
    if t > tR - 0.4:
        x, bob, rock, ph = hop_walk(t, tR - 0.4, tR + 0.8, 1060, 820, 0.4)
        kneel = t > tR + 0.8
        rama(cr, t, x, 0.72, flip=True, kneel="jt_rama_kneel" if kneel else None, legs=walk_legs(ph),
             rot=rock if not kneel else 0.0, feet=G, y=None if kneel else G - 434 * 0.72 + bob,
             front=(-1.2, -0.3) if kneel else (-0.2, -0.3), ph=0.4)

    def ui(cr_):
        q = prog(t, tD - 0.2, 0.4)
        if q > 0.01:
            cr_.save()
            cr_.translate(840, 760)
            cr_.new_path()
            cr_.arc(0, 0, 130, 0, 2 * math.pi)
            cr_.set_source_rgba(0.97, 0.87, 0.62, 0.95 * q)
            cr_.fill_preserve()
            cr_.set_source_rgba(*INK, q)
            cr_.set_line_width(5)
            cr_.stroke()
            v = ease(q)
            pc.poly(cr_, [(-22, -80), (22, -80), (22, 30 * v), (54, 30 * v), (0, 100 * v), (-54, 30 * v),
                          (-22, 30 * v)])
            cr_.set_source_rgba(*RED, q)
            cr_.fill()
            cr_.restore()
    return dict(ui=ui)


def s_memory(cr, t, tl, t0, t1):
    c = cues(tl, "jt13")
    tP, tA = c["P"], c["A"]
    ground(cr, G - 200, a=0.6)
    q = prog(t, tP - 0.3, 0.5)
    prop(cr, "dv_city", 300, 820, 0.5, alpha=0.7 * q, blur=3)
    prop(cr, "jt_pyre", 300, G - 230, 0.6, alpha=q)
    glow(cr, 300, G - 380, 240, 0.7 * q)
    lights(cr, t, 300, G - 400, 120, 8, q)
    pb = fig(cr, K.BHARATA, "bharata", t, 520, 0.55, feet=G - 200, flip=True, alpha=q, front=(-1.3, -0.4), ph=0.2)
    hx, hy = to_user(cr, pb["handF"])
    prop(cr, "jt_torch", hx, hy + 20, 0.45, -0.5, alpha=q)
    warm(cr, hx - 70, hy - 110, 80, q, col=(1.0, 0.55, 0.15))
    prop(cr, "dv_tree", 960, G - 200, 0.55, alpha=0.8, blur=4, flip=True)
    for i in range(14):                                   # the fold between the two places
        y0 = 560 + 80 * i
        cr.move_to(690, y0)
        cr.line_to(690, y0 + 44)
    cr.set_source_rgba(0.25, 0.14, 0.05, 0.55 * q)
    cr.set_line_width(6)
    cr.stroke()
    rama(cr, t, 830, 0.52, feet=G - 200, head=0.25, alpha=prog(t, t0, 0.4), front=(-0.1, -0.2), ph=0.5)
    if t > tA - 0.2:
        dots_path(cr, arc_path((790, G - 600), (400, G - 600), 140, 50), prog(t, tA - 0.2, 0.8),
                  col=(0.3, 0.15, 0.05), a=0.8)

    def ui(cr_):
        sepia(cr_, 0.55)
    return dict(ui=ui)


def s_pyre(cr, t, tl, t0, t1):
    c = cues(tl, "jt14")
    tA = c["A"]
    forest(cr, t, feet=G, hut_a=0.0, trees=((1040, 0.7, 4, 0.8, False),))
    prop(cr, "jt_pyre", 640, G, 0.8)
    lying(cr, t, 600, 0.55, feet=G - 190, alpha=1.0)
    g = prog(t, tA, 0.8)
    if g > 0.01:
        warm(cr, 640, G - 300, 420, g * (0.8 + 0.2 * math.sin(t * 9)), col=(1.0, 0.55, 0.15))
        glow(cr, 640, G - 320, 360, g)
        lights(cr, t, 640, G - 360, 220, 18, g, col=(1.0, 0.62, 0.20), speed=0.8)
    lakshmana(cr, t, 120, 0.6, feet=G, front=ANJ[0], backa=ANJ[1], ph=0.8)
    pts = rama(cr, t, 330, 0.72, feet=G, front=keyed(t, [(0, (-0.6, -0.6)), (tA - 0.3, (-1.4, -0.2))]), ph=0.4,
               hits=[(tA, 0.3)])
    hx, hy = to_user(cr, pts["handF"])
    prop(cr, "jt_torch", hx, hy + 30, 0.6, 0.5)
    warm(cr, hx + 120, hy - 140, 110, 0.9 + 0.1 * math.sin(t * 11), col=(1.0, 0.55, 0.15))
    return dict(eve=0.3, night=0.2)


ANJ = ((-0.75, -1.85), (-0.8, -1.8))


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "jt15")
    tP, tV = c["P"], c["V"]
    bx, by = tree_set(cr, 900, 1.0)
    rama(cr, t, 300, 0.7, feet=G, front=ANJ[0], backa=ANJ[1], head=-0.15, ph=0.3)
    a = 1 - prog(t, tP, 0.5)
    if a > 0.01:
        perched(cr, t, bx + 30, by, flip=True, s=0.85, head=0.35, alpha=a)
    if t > tP - 0.2:
        u = clamp((t - tP + 0.2) / 3.0)
        yy = by - 200 - 260 * u
        glow(cr, bx + 60, yy, 300, 0.8 * (1 - u * 0.5))
        jt(cr, t, bx + 60, yy, 0.6, wing=0.9, flap=0.3, alpha=0.75 * prog(t, tP - 0.2, 0.4), blur=3, rods=False,
           rate=1.2)
        lights(cr, t, bx + 60, yy, 200, 12, 1.0)
    return {}


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "jt16")
    tH, tJ = c["H"], c["J"]
    ground(cr)
    glow(cr, 540, G - 300, 360, 0.6)
    perched(cr, t, 540, G, 0.5, flip=(t > tJ and int((t - tJ) / 0.9) % 2 == 1), head=0.1)
    cards = ((280, "हारा?", "लड़ाई में", tH - 0.1), (800, "जीता?", "वादा निभाया", tJ - 0.1))

    def ui(cr_):
        for cx, big, small, tc in cards:
            hcard(cr_, t, tc - 0.2, cx, 560, big, small)
        if t > tJ + 0.3:
            n = int((t - tJ - 0.3) / 0.9)
            k = n % 2
            red_ring(cr_, cards[k][0], 564, 230, 150, prog(t, tJ + 0.3 + 0.9 * n, 0.35), 9)
    return dict(ui=ui, night=0.25)


# ------------------------------------------------------------------ labels


LABELS = {
    "jt1": [(0.3, "रामायण मूवी देखी?", dict(y=330, size=80)),
            ("R", "रावण से पहली लड़ाई", dict(y=330, size=80)),
            ("G", "एक बूढ़ा गिद्ध", dict(y=330, size=90)),
            ("J", "जटायु", dict(y=330, size=120, col=RED, under=True))],
    "jt2": [("S", "सीता: कोई रिश्तेदार नहीं", dict(y=330, size=76)),
            ("J", "फिर भी जान दे दी", dict(y=330, size=84)),
            ("Q", "क्यों?", dict(y=330, size=110, col=RED))],
    "jt3": [("R", "गिद्धों का राजा", dict(y=1420, size=90)),
            ("B", "बहुत बूढ़ा", dict(y=1420, size=96, col=RED))],
    "jt4": [("R", "राम, लक्ष्मण और सीता", dict(y=330, size=84)),
            ("P", "पेड़ पर: विशाल गिद्ध", dict(y=330, size=84))],
    "jt5": [("K", "राक्षस?", dict(y=330, size=110, col=RED)),
            ("D", "डरो मत, बेटा", dict(y=330, size=90)),
            ("F", "मैं राजा दशरथ का दोस्त", dict(y=330, size=80, col=RED, under=True))],
    "jt6": [("B", "तुम दोनों बाहर जाओगे...", dict(y=330, size=76)),
            ("R", "मैं सीता की रखवाली करूँगा", dict(y=330, size=72, col=RED)),
            ("W", "दोस्त के बेटे से वादा", dict(y=330, size=84, col=RED, under=True))],
    "jt7": [("A", "रावण सीता को ले उड़ा", dict(y=330, size=82)),
            ("C", "सीता की चीख़!", dict(y=330, size=96, col=RED)),
            ("J", "जटायु जागा!", dict(y=330, size=104, under=True))],
    "jt8": [("O", "रावण का रास्ता रोका", dict(y=330, size=84)),
            ("B", "मैं बूढ़ा, तुम जवान", dict(y=330, size=84)),
            ("R", "रथ है, धनुष है", dict(y=330, size=88)),
            ("N", "मेरे जीते जी: नहीं!", dict(y=330, size=96, col=RED, under=True))],
    "jt9": [("A", "अकेला गिद्ध, रावण के सामने", dict(y=330, size=70)),
            ("Q", "क्या वो जीत सकता था?", dict(y=330, size=86, col=RED))],
    "jt10": [("D", "धनुष तोड़ा!", dict(y=330, size=100)),
             ("R", "रथ तोड़ा!", dict(y=330, size=104)),
             ("S", "सारथी गिराया!", dict(y=330, size=100, col=RED))],
    "jt11": [("B", "बूढ़ा जटायु थक गया", dict(y=330, size=84)),
             ("T", "तलवार!", dict(y=330, size=110, col=RED)),
             ("K", "दोनों पंख काटे", dict(y=330, size=96, col=RED, under=True))],
    "jt12": [("G", "जटायु गिर पड़ा", dict(y=330, size=90)),
             ("R", "राम के आने तक ज़िंदा रहा", dict(y=330, size=76)),
             ("D", "रावण गया: दक्षिण", dict(y=330, size=90, col=RED, under=True)),
             ("Z", "जटायु ने दम तोड़ दिया", dict(y=330, size=80))],
    "jt13": [("P", "पिता गुज़र गए", dict(y=330, size=92)),
             ("A", "राम आग भी नहीं दे पाए", dict(y=330, size=76, col=RED))],
    "jt14": [("H", "राम ने अपने हाथों से", dict(y=330, size=80)),
             ("A", "आग दी", dict(y=330, size=110, col=RED)),
             ("B", "जैसे बेटा, पिता को", dict(y=330, size=90, under=True))],
    "jt15": [("D", "पिता का दोस्त बनकर मिला...", dict(y=330, size=72)),
             ("P", "पिता बनकर विदा हुआ", dict(y=330, size=84, col=RED, under=True))],
    "jt16": [(0.05, "जटायु वो लड़ाई...", dict(y=300, size=90))],
}


def labels(cr, t, tl, bid, t1):
    specs = LABELS.get(bid, [])
    if not specs:
        return
    c = cues(tl, bid)
    starts = [c["t0"] + w if isinstance(w, (int, float)) else c[w] - 0.1 for w, _, _ in specs]
    if bid == "jt1":
        starts[0] = 0.25
    for i, (_, text, kw) in enumerate(specs):
        kw = dict(kw)
        t_out = kw.pop("out", None)
        if t_out is None:
            t_out = starts[i + 1] - 0.15 if i + 1 < len(starts) else t1 - 0.12
        label(cr, t, starts[i], text, t_out=t_out, **kw)


# ------------------------------------------------------------------ the cut list and the frame


DUSK = (1.0, 0.62, 0.42)
FOREST = (0.86, 1.0, 0.78)
ANGER = (1.0, 0.55, 0.45)
NIGHT_BLUE = (0.55, 0.66, 1.0)
GOLDC = (1.0, 0.86, 0.58)
FIRE = (1.0, 0.70, 0.45)

SHOTS = [
    ("jt1", s_hook, dict(z=(1.0, 1.04), focus=(540, 1000), place=(DUSK, 0.45))),
    ("jt2", s_sita, dict(z=(1.05, 1.1), focus=(540, 1000), place=(DUSK, 0.4))),
    ("jt3", s_king, dict(z=(1.0, 1.06), focus=(560, 900), place=(GOLDC, 0.3))),
    ("jt4", s_path, dict(z=(1.0, 1.04), focus=(540, 1100), place=(FOREST, 0.35))),
    ("jt5", s_friend, dict(z=(1.05, 1.1), focus=(560, 1100), place=(FOREST, 0.3))),
    ("jt6", s_promise, dict(z=(1.05, 1.1), focus=(560, 1100), place=(GOLDC, 0.3))),
    ("jt7", s_taken, dict(z=(1.0, 1.04), focus=(540, 1000), place=(DUSK, 0.45))),
    ("jt8", s_stand, dict(z=(1.05, 1.1), focus=(540, 1000), place=(ANGER, 0.35))),
    ("jt9", s_odds, dict(z=(1.1, 1.15), focus=(540, 1125), place=(NIGHT_BLUE, 0.4))),
    ("jt10", s_fight, dict(z=(1.05, 1.1), focus=(540, 1000), place=(ANGER, 0.4))),
    ("jt11", s_cut, dict(z=(1.1, 1.15), focus=(540, 1125), place=(ANGER, 0.45))),
    ("jt12", s_last, dict(z=(1.1, 1.15), focus=(560, 1125), place=(DUSK, 0.35))),
    ("jt13", s_memory, dict(z=(1.0, 1.04), focus=(540, 1000))),
    ("jt14", s_pyre, dict(z=(1.05, 1.1), focus=(500, 1100), place=(FIRE, 0.35))),
    ("jt15", s_callback, dict(z=(1.0, 1.04), focus=(560, 1000), place=(GOLDC, 0.45))),
    ("jt16", s_end, dict(z=(1.0, 1.03), focus=(540, 1200), frames=[(1.0, (540, 1200))])),   # cards: stay wide
]


def shot_at(t, tl):
    cache = getattr(tl, "_jt_shots", None)
    if cache is None:
        starts = [0.0]
        for bid, _, _ in SHOTS[1:]:
            starts.append(max(T(tl, FIRST[bid]) - 0.12, starts[-1] + 0.5))
        cache = tl._jt_shots = starts
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
    if k > 0 and t - t0 < 0.22:
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """Sparse sounds, most important first, at least SFX_MIN_GAP apart: a damaru on the hook's name, a hit as the bow
    snaps, a conch as Jatayu wakes, shimmer as the pyre glows and as his light rises, a bell on the closing question;
    dips before the wings are cut and before the pyre."""
    c = {b: cues(tl, b) for b in CUES}
    t_end = min(c["jt16"]["J"], tl["j35"].end - 0.05)
    want = [(c["jt1"]["J"], "damaru", 0), (c["jt10"]["D"], "hit", 0), (c["jt7"]["J"], "conch", 0),
            (c["jt14"]["A"], "shimmer", 0), (t_end, "bell", 0), (c["jt15"]["V"], "shimmer", 0),
            (c["jt11"]["K"], "hit", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["jt11"]["K"] - 0.3, "dip", 0.5), (c["jt14"]["A"] - 0.3, "dip", 0.45)]
    kept = [(after_voice(tl, a), n, d) for a, n, d in kept]          # never over a spoken word
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]


def after_voice(tl, a):
    """A sound effect time moved out of any spoken line into the pause right after it, so no effect covers a word."""
    for b in tl.beats:
        if b.start - 0.15 <= a < b.end:
            return b.end + 0.06 if b.end + 1.0 < tl.total else max(0.0, b.start - 0.3)   # last line: just before it
    return a
