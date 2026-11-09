"""Scenes for videos/jayadratha.py: "To kill me, Krishna had to hide the sun": Jayadratha tells his own death, in
Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen, two-tier headlines
and rod-puppet motion as the Jarasandha, Kaikeyi, Lakshman Rekha and Mandhata reels, with the cast from
jayadratha_cast. ONE story, one step per shot, first person (the headlines say I / ME / MY FATHER).

Respect: Krishna is calm and wise, never a trickster cartoon; Arjuna keeps his dignity. No gore at all: the head is
only ever a small dark round silhouette (a pale rim so it reads on the dark sky), the father's death is a burst of light
and a white flash on his silhouette, after which he is gone and only drifting lights remain.

Every frame is a pure function of t. English on-screen text only (shared by Hindi and Kannada); cues are words of the
line in each language ({"hi": ..., "kn": ...}) with a fraction fallback, kept in one table (CUES) that the scenes and
sfx() both read, with minimum gaps so a fast voice can't bunch the beats together.

Shot list (line: what is on the screen)
  y1  COLD OPEN, frame 0: Krishna on the chariot points up at a sun half hidden by the dark disc; Arjuna behind him
      draws his bow; THE SUN HAS / NOT SET! (big word in by 0.25 s); the sun is ringed on "suraj", the big word
      underlined on "nahin"
  y2  Jayadratha alone, large and proud (fist on his chest): I AM / JAYADRATHA, tag KING OF SINDHU; then TO KILL ME,
      KRISHNA HAD TO HIDE THE / SUN: a sun rises behind him on "suraj" and the dark disc slides over it on "chhipana"
  y3  the chakravyuha: a spiral of soldiers; Jayadratha at its mouth, arms out; three shadows of the Pandavas pushed
      back: AT THE CHAKRAVYUHA, / I BLOCKED THE DOOR; inside, small Abhimanyu (tag) falls gently and fades: INSIDE,
      ABHIMANYU / FELL (in ink)
  y4  Arjuna raises Gandiva over his head beside a pyre: ARJUNA'S / VOW; a torn note: BEFORE SUNSET, / JAYADRATHA DIES
      ... / OR INTO THE FIRE (red), the pyre flares on "aag"
  y5  the Kaurava soldiers march in round Jayadratha in a ring, two deep; he ducks, shields go up: THE WHOLE ARMY
      KEPT ME / HIDDEN; the sun sinks and turns red, the light goes warm: AND THEN IT WAS / EVENING
  y6  the dark disc sweeps over the sun, darkness spreads from it: SUDDENLY, / DARKNESS; the soldiers jump and raise
      their spears (sound rings): EVERYONE SHOUTED: / THE SUN HAS SET!
  y7  in the dark, the soldiers part; Jayadratha steps out in front, happy, and looks up at the covered sun (a dotted
      line of sight): I CAME OUT / TO LOOK
  y8  the callback: the chariot again, the sun fully behind the disc with its corona showing: THEN THAT VOICE: ...
      THE SUN HAS / NOT SET! (ring on the corona); Arjuna draws
  y9  BUT I HAD ONE / SHIELD; the old father (tag MY FATHER) raises a warning hand; a torn note with his words:
      WHOEVER DROPS MY SON'S HEAD / TO THE GROUND, / THEIR OWN HEAD BURSTS / IN 100 PIECES; a red MY SHIELD stamp
  y10 Krishna close, calm, a soft glow and slow rays behind him, his hand raised in blessing: AND KRISHNA / KNEW
  y11 wide: Arjuna shoots from the left; the arrow takes Jayadratha (a flash, he fades away); the small dark round
      silhouette rides the arrow along a dotted arc across the sky to the far-off hermitage where the father prays
      by his fire (tag MY FATHER, AT PRAYER) and lands in his lap: THE ARROW CARRIED IT / FAR AWAY ... INTO MY
      FATHER'S / LAP
  y12 close on the hermitage: the father finishes his prayer and stands; the dark shape slips and falls to the ground
      (a bump, dust rings): MY FATHER / STOOD UP ... IT FELL TO THE / GROUND
  y13 HIS OWN / CURSE: a dark ring gathers round his head; on "gira" a burst of light from his head, his figure goes
      to silhouette, the screen flashes white; then he is gone and lights drift up
  y14 Jayadratha, Krishna and the father stand small in a row: THE CURSE MEANT TO SAVE ME... / TOOK MY FATHER (ink);
      three cards drop in, JAYADRATHA? KRISHNA? THE FATHER?, NOW YOU TELL ME: / WHOSE FAULT?, a red ring moving
      from card to card
"""
import math

import cairo

import jayadratha_cast as J
import puppet_cast as C
import puppet_core as pc
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, text_size
from puppet_core import H, W, depth, keyed, prop, puppet, sway
from scenes_jarasandha import (FADE, FEET, INK, RED, bob_rot, glow, ground, man_angles, motes, red_ring, sound_rings,
                               stamp)
from scenes_kaikeyi import ANJALI, card, fig
from scenes_lakshman_rekha import quote_note, sparkle
from scenes_mandhata import aura, burst, held, lights, local, mix, reach_arm, warm, yajna_fire
from scenes_ravana import dotted, head2
from shots import T, shot_at

MISSES = set()                       # cue words not found in a line (falls back to fractions)
NIGHT = 0.42
SIL = (0.07, 0.04, 0.03)             # silhouettes


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, words)
    except (KeyError, ValueError):
        MISSES.add((bid, words[getattr(tl, "lang", "hi")] if isinstance(words, dict) else words))
        return T(tl, bid, frac)


# Every cue of every line: (name, {"hi": word, "kn": word}, fraction fallback, ((after, min gap), ...)); "t0" = the
# line's start. Words are exact substrings of the script lines (checked: MISSES stays empty).
CUES = {
    "y1": (("S", {"hi": "सूरज", "kn": "ಸೂರ್ಯ"}, 0.3, (("t0", 0.3),)),
           ("N", {"hi": "नहीं", "kn": "ಮುಳುಗಿಲ್ಲ"}, 0.72, (("S", 0.35),))),
    "y2": (("J", {"hi": "जयद्रथ", "kn": "ಜಯದ್ರಥ"}, 0.06, (("t0", 0.15),)),
           ("R", {"hi": "राजा", "kn": "ರಾಜ"}, 0.3, (("J", 0.5),)),
           ("K", {"hi": "मारने", "kn": "ಕೊಲ್ಲೋಕೆ"}, 0.47, (("R", 0.7),)),
           ("S", {"hi": "सूरज", "kn": "ಸೂರ್ಯನನ್ನೇ"}, 0.74, (("K", 0.7),)),
           ("H", {"hi": "छिपाना", "kn": "ಮುಚ್ಚಬೇಕಾಯ್ತು"}, 0.84, (("S", 0.35),))),
    "y3": (("C", {"hi": "चक्रव्यूह", "kn": "ಚಕ್ರವ್ಯೂಹದ"}, 0.02, ()),
           ("P", {"hi": "पांडवों", "kn": "ಪಾಂಡವರನ್ನ"}, 0.4, (("t0", 1.0),)),
           ("B", {"hi": "रोका", "kn": "ತಡೆದೆ"}, 0.55, (("P", 0.4),)),
           ("A", {"hi": "अभिमन्यु", "kn": "ಅಭಿಮನ್ಯು"}, 0.75, (("B", 0.8),)),
           ("M", {"hi": "मारा", "kn": "ಸತ್ತುಹೋದ"}, 0.88, (("A", 0.45),))),
    "y4": (("V", {"hi": "क़सम", "kn": "ಪ್ರತಿಜ್ಞೆ"}, 0.1, (("t0", 0.3),)),
           ("S", {"hi": "सूरज", "kn": "ಸೂರ್ಯ"}, 0.28, (("V", 0.6),)),
           ("J", {"hi": "जयद्रथ", "kn": "ಜಯದ್ರಥ"}, 0.49, (("S", 0.6),)),
           ("F", {"hi": "आग", "kn": "ಬೆಂಕಿಗೆ"}, 0.8, (("J", 0.8),))),
    "y5": (("K", {"hi": "कौरव", "kn": "ಕೌರವ"}, 0.08, (("t0", 0.1),)),
           ("H", {"hi": "छिपा", "kn": "ಬಚ್ಚಿಟ್ಟುಕೊಂಡಿತು"}, 0.55, (("K", 1.2),)),
           ("E", {"hi": "शाम", "kn": "ಸಂಜೆ"}, 0.82, (("H", 0.8),))),
    "y6": (("D", {"hi": "अंधेरा", "kn": "ಕತ್ತಲು"}, 0.23, (("t0", 0.3),)),
           ("C", {"hi": "चिल्लाए", "kn": "ಕೂಗಿದ್ರು"}, 0.6, (("D", 0.8),)),
           ("S", {"hi": "डूब", "kn": "ಮುಳುಗಿದ"}, 0.85, (("C", 0.35),))),
    "y7": (("J", {"hi": "ख़ुशी", "kn": "ಖುಷಿಯಿಂದ"}, 0.12, (("t0", 0.1),)),
           ("L", {"hi": "आसमान", "kn": "ಆಕಾಶ"}, 0.6, (("J", 1.0),))),
    "y8": (("V", {"hi": "आवाज़", "kn": "ಧ್ವನಿ"}, 0.14, (("t0", 0.15),)),
           ("A", {"hi": "अर्जुन", "kn": "ಅರ್ಜುನ"}, 0.4, (("V", 0.4),)),
           ("S", {"hi": "सूरज", "kn": "ಸೂರ್ಯ"}, 0.55, (("A", 0.3),)),
           ("N", {"hi": "नहीं", "kn": "ಮುಳುಗಿಲ್ಲ"}, 0.82, (("S", 0.35),))),
    "y9": (("D", {"hi": "ढाल", "kn": "ರಕ್ಷೆ"}, 0.1, (("t0", 0.3),)),
           ("F", {"hi": "पिता", "kn": "ತಂದೆ"}, 0.25, (("D", 0.6),)),
           ("G", {"hi": "ज़मीन", "kn": "ನೆಲಕ್ಕೆ"}, 0.56, (("F", 1.2),)),
           ("B", {"hi": "सौ", "kn": "ನೂರು"}, 0.82, (("G", 0.8),))),
    "y10": (("K", {"hi": "कृष्ण", "kn": "ಕೃಷ್ಣನಿಗೆ"}, 0.05, ()),
            ("W", {"hi": "जानते", "kn": "ಗೊತ್ತಿತ್ತು"}, 0.52, (("t0", 0.35),))),
    "y11": (("A", {"hi": "तीर", "kn": "ಬಾಣ"}, 0.1, (("t0", 0.7),)),
            ("P", {"hi": "पूजा", "kn": "ಪೂಜೆ"}, 0.5, (("A", 1.0),)),
            ("L", {"hi": "गोद", "kn": "ತೊಡೆ"}, 0.78, (("P", 0.8),))),
    "y12": (("U", {"hi": "उठे", "kn": "ಎದ್ರು"}, 0.17, (("t0", 0.15),)),
            ("G", {"hi": "ज़मीन", "kn": "ನೆಲಕ್ಕೆ"}, 0.52, (("U", 0.75),))),
    "y13": (("C", {"hi": "श्राप", "kn": "ಶಾಪವೇ"}, 0.3, (("t0", 0.25),)),
            ("F", {"hi": "गिरा", "kn": "ಬಿತ್ತು"}, 0.8, (("C", 0.6),))),
    "y14": (("S", {"hi": "बचाने", "kn": "ಕಾಪಾಡೋಕೆ"}, 0.13, (("t0", 0.3),)),
            ("L", {"hi": "जान", "kn": "ಪ್ರಾಣ"}, 0.55, (("S", 0.8),)),
            ("Q", {"hi": "बताओ", "kn": "ಹೇಳಿ"}, 0.75, (("L", 0.8),)),
            ("W", {"hi": "ग़लती", "kn": "ತಪ್ಪು"}, 0.82, (("Q", 0.3),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_jd_cues", None)
    if cache is None:
        cache = {}
        tl._jd_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, words, frac, cons in CUES[bid]:
            v = cue(tl, bid, words, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


def to_user(cr, p):
    return cr.device_to_user(*p)


def tag(cr, t, t_in, text, x, y, size=44, alpha=1.0, color=INK, t_out=None):
    """scenes_jarasandha.tag (a small leather name plaque dropping in on its rod), with the edge dots drawn as dots
    and the parchment opaque, so it also reads on the dark shots."""
    p = clamp((t - t_in) / 0.3)
    if t_out is not None:
        p = min(p, 1 - clamp((t - t_out) / 0.25))
    if p <= 0:
        return
    w, h = text_size(text, size, MONO_FONT, 2)
    bw, bh = w + 54, h + 34
    yy = y - 40 * (1 - back(p))
    pc.rod(cr, x, yy + bh / 2, x + 30, H + 50, alpha=0.5 * p * alpha)
    cr.save()
    cr.translate(x, yy)
    pc.poly(cr, [(-bw / 2, -bh / 2 + 10), (-bw / 2 + 10, -bh / 2), (bw / 2 - 10, -bh / 2), (bw / 2, -bh / 2 + 10),
                 (bw / 2, bh / 2 - 10), (bw / 2 - 10, bh / 2), (-bw / 2 + 10, bh / 2), (-bw / 2, bh / 2 - 10)])
    cr.set_source_rgba(0.96, 0.84, 0.58, 0.96 * p * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, p * alpha)
    cr.set_line_width(4)
    cr.stroke()
    for k in range(int(bw // 18)):
        for yd in (-bh / 2 + 7, bh / 2 - 7):
            cr.new_sub_path()
            cr.arc(-bw / 2 + 12 + k * 18, yd, 2.2, 0, 2 * math.pi)
    cr.set_source_rgba(0.55, 0.32, 0.14, 0.8 * p * alpha)
    cr.fill()
    draw_text(cr, text, 0, 1, size, color, p * alpha, MONO_FONT, "cm", tracking=2)
    cr.restore()


def flash_at(t, t_f, k=0.3, rate=4.0):
    return k * math.exp(-rate * max(0.0, t - t_f)) * (t > t_f)


# ------------------------------------------------------------------ light, dark and silhouettes


def shroud(cr, x, y, r, a):
    """Darkness spreading from (x, y): full `a` inside 0.55 r, fading out at r."""
    if a <= 0.01 or r <= 1:
        return
    g = cairo.RadialGradient(x, y, r * 0.55, x, y, r)
    g.add_color_stop_rgba(0, 0.03, 0.02, 0.06, a)
    g.add_color_stop_rgba(1, 0.03, 0.02, 0.06, 0.0)
    cr.save()
    cr.set_source(g)
    cr.paint()
    cr.restore()


def tint(cr, col, a):
    """A coloured light over the whole cloth (evening)."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(*col, a)
    cr.paint()
    cr.restore()


def silhouette(cr, fn, a, col=SIL):
    """Whatever fn(cr) draws, as one flat dark shadow (punched holes stay light)."""
    if a <= 0.01:
        return None
    cr.push_group()
    res = fn(cr)
    pat = cr.pop_group()
    cr.save()
    cr.set_source_rgba(*col, a)
    cr.mask(pat)
    cr.restore()
    return res


def head_sil(cr, x, y, r, rot=0.0, alpha=1.0, rim=1.0):
    """The head: only ever a small dark round silhouette with a tiny crown outline, a pale rim so it reads on dark."""
    if alpha <= 0.01:
        return
    if rim > 0:
        glow(cr, x, y, r * 3.0, 0.35 * rim * alpha)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.new_path()
    pc.ell(cr, 0, 0, r, r * 1.08)
    pts = [(-0.62 * r, -0.72 * r), (-0.55 * r, -1.25 * r), (-0.28 * r, -0.95 * r), (0, -1.42 * r),
           (0.28 * r, -0.95 * r), (0.55 * r, -1.25 * r), (0.62 * r, -0.72 * r)]
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.close_path()
    path = cr.copy_path()
    if rim > 0:
        cr.set_source_rgba(1.0, 0.9, 0.66, 0.75 * rim * alpha)
        cr.set_line_width(5)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
        cr.append_path(path)
    cr.set_source_rgba(*SIL, 0.96 * alpha)
    cr.fill()
    cr.restore()


def sun_disc(cr, t, x, y, s, cover=0.0, side=1.0, glow_a=1.0, alpha=1.0, red=0.0):
    """The sun (radius 200 s) and the dark disc of yoga-maya sliding over it from `side` (cover 0 = away, 1 = right
    over it); while it covers the sun, a corona of light still shows round its rim: the sun is still up."""
    glow(cr, x, y, 420 * s + 120, glow_a * alpha * (0.55 * (1 - 0.75 * cover) + 0.12))
    warm(cr, x, y, 300 * s, 0.5 * (1 - cover) * glow_a * alpha, (1.0, 0.72 - 0.3 * red, 0.18))
    prop(cr, "sun", x, y, s, rot=t * 0.2, alpha=alpha)
    if red > 0:
        tint_disc(cr, x, y, 200 * s, red * alpha)
    if cover > 0.01:
        ca = clamp((cover - 0.55) / 0.45)
        aura(cr, t, x, y, 200 * s, 380 * s, 0.95 * ca * alpha, n=26, spin=0.08)
        d = (1 - cover) * 470 * s
        prop(cr, "jd_maya", x + d * side, y - 0.3 * d, s, rot=-0.25 * t, alpha=alpha)


def tint_disc(cr, x, y, r, a):
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(1.0, 0.45, 0.30, 0.6 * a)
    cr.fill()
    cr.restore()


def drift_lights(cr, t, x, y, w, h, n, a, col=(1.0, 0.86, 0.45), speed=0.35, ph=0.0):
    for i in range(n):
        u = (t * speed + i / n + ph) % 1.0
        gx = x + w * (((i * 0.618) % 1.0) - 0.5) + 16 * math.sin(t * 1.7 + i)
        gy = y - h * u
        sparkle(cr, gx, gy, (10 + 7 * (i % 3)) * math.sin(math.pi * u), a, col)


# ------------------------------------------------------------------ puppets


AR_B = 1.05


def bow_cb(store, arm, bs, tilt, sprite, alpha, blur):
    """extra= callback: the bow held in a hand (upright + tilt), recording its string tips and grip (device)."""
    rot = -(arm[0] + arm[1]) + tilt

    def fn(cr_):
        cr_.save()
        cr_.translate(4, 150)
        cr_.rotate(rot)
        cr_.scale(bs, bs)
        pc.paint_part(cr_, sprite, alpha, blur)
        store["tips"] = (cr_.user_to_device(-88, -338), cr_.user_to_device(-88, 338))
        store["grip"] = cr_.user_to_device(0, 0)
        cr_.restore()
    return fn


def arrow_at(cr, x0, y0, ang, length, alpha=1.0, blur=0.0):
    """The arrow sprite from its nock at (x0, y0) pointing along ang, `length` px long."""
    prop(cr, "jd_arrow", x0, y0, length / 356.0, rot=ang, alpha=alpha, blur=blur)


def arjuna(cr, t, x, s, bow="carry", aim=-0.6, draw=0.0, arrow=True, feet=FEET, y=None, front=None, backa=None,
           alpha=1.0, blur=0.0, rods=True, head=0.0, hits=(), ph=0.0, rot=0.0):
    """Arjuna (facing right). bow: 'carry' (strung bow upright in the back hand), 'raise' (held high in the front
    hand: the vow), 'aim' (the bow arm straight out along the screen angle `aim`, draw 0..1 pulls the string back
    with an arrow nocked). Returns his points (device) plus 'grip' / 'nock' (user) when aiming."""
    hy = feet - 434 * s if y is None else y
    store = {}
    if bow == "aim":
        fr = (aim - math.pi / 2, 0.0)
        dx, dy = math.cos(aim), math.sin(aim)
        sx, sy = x + 26 * AR_B * s, hy - 262 * s
        k = (300 - 70 - 170 * draw) * s
        ba = reach_arm(x, hy, s, -14 * AR_B, (sx + k * dx, sy + k * dy))
        extra = {"jd_arjuna_armF_lo": bow_cb(store, fr, 0.8, aim, "jd_gandiva_bare" if draw > 0.02 else "jd_gandiva",
                                             alpha, blur)}
    elif bow == "raise":
        fr = front or (-2.95, -0.12)
        ba = backa or (0.3, -0.25)
        extra = {"jd_arjuna_armF_lo": bow_cb(store, fr, 0.8, 0.0, "jd_gandiva", alpha, blur)}
    else:
        fr = front or (-0.32, -0.55)
        ba = backa or (0.3, -0.25)
        extra = {"jd_arjuna_armB_lo": bow_cb(store, ba, 0.72, 0.0, "jd_gandiva", alpha, blur)}
    pts = fig(cr, J.ARJUNA, "jd_arjuna", t, x, s, front=fr, backa=ba, head=head, hits=hits, alpha=alpha, blur=blur,
              rods=rods, rot=rot, feet=feet, ph=ph, extra=extra, y=y)
    if bow == "aim" and "tips" in store:
        g = to_user(cr, store["grip"])
        hb = to_user(cr, pts["handB"])
        pts["grip"] = g
        pts["nock"] = hb
        if draw > 0.02:
            ta, tb = to_user(cr, store["tips"][0]), to_user(cr, store["tips"][1])
            cr.save()
            cr.set_source_rgba(*pc.INK, 0.9 * alpha)
            cr.set_line_width(max(1.6, 2.6 * s))
            cr.move_to(*ta)
            cr.line_to(*hb)
            cr.line_to(*tb)
            cr.stroke()
            cr.restore()
            if arrow:
                ang = math.atan2(g[1] - hb[1], g[0] - hb[0])
                arrow_at(cr, hb[0], hb[1], ang, math.dist(g, hb) + 80 * s, alpha, blur)
    return pts


def krishna(cr, t, x, s, whip=False, **kw):
    if whip:
        ba = kw.get("backa", (0.3, -0.25))
        kw.setdefault("extra", {"krishna_armB_lo": held("jd_whip", ba, 0.75, tilt=-0.3, alpha=kw.get("alpha", 1.0),
                                                        blur=kw.get("blur", 0.0))})
    return fig(cr, C.KRISHNA, "krishna", t, x, s, **kw)


def jaya(cr, t, x, s, **kw):
    return fig(cr, J.JAYA, "jd_jaya", t, x, s, **kw)


JD_PROUD = dict(front=(-0.25, -2.35), backa=(0.75, -1.6))          # fist on the chest, the other hand on the hip


def soldier(cr, t, x, feet, s, raise_=0.0, flip=False, ph=0.0, alpha=1.0, blur=0.0, legs=(0.0, 0.0), cheer=0.0,
            guard=0.0, rods=False, rot=0.0):
    """A Kaurava soldier, a spear in the front hand (raise_ lifts it overhead), a round shield on the back arm
    (guard 0..1 raises it in front of him); cheer 0..1 makes him jump."""
    jump = cheer * abs(math.sin(t * 7.0 + ph * 3.1)) * 42 * s
    fr = (-0.45 - 2.1 * raise_, -1.15 + 1.0 * raise_)
    ba = mix((-0.25, -1.25), (-1.55, -0.75), guard)
    sh = {"jd_soldier_armB_lo": lambda cr_: _shield_in(cr_, alpha, blur),
          "jd_soldier_armF_lo": held("jd_spear", fr, 0.75, tilt=0.15 * raise_, alpha=alpha, blur=blur)}
    return fig(cr, J.SOLDIER, "jd_soldier", t, x, s, front=fr, backa=ba, legs=legs, flip=flip, alpha=alpha, blur=blur,
               rods=rods, rot=rot + 0.04 * cheer * math.sin(t * 7.0 + ph * 3.1), feet=feet - jump, ph=ph, extra=sh)


def _shield_in(cr_, alpha, blur):
    cr_.save()
    cr_.translate(6, 90)
    cr_.scale(0.95, 0.95)
    pc.paint_part(cr_, "jd_shield", alpha, blur)
    cr_.restore()


def father(cr, t, x, feet, s, rise=0.0, alpha=1.0, blur=0.0, flip=False, ph=0.0, rods=True, eyes=None, front=None,
           backa=None, head=0.0):
    """Vriddhakshatra. rise 0 = seated cross-legged in prayer (hands joined, eyes shut), 1 = standing; in between a
    quick rod-puppet lift. Returns his points (device) plus 'lap' and 'head_u' (user)."""
    q = clamp(rise)
    seated = q < 0.5
    hy_sit = feet - J.SEAT_H * s
    hy_st = feet - 434 * s
    hy = hy_sit + (hy_st - hy_sit) * ease(q)
    shut = (q < 0.3) if eyes is None else (eyes == "shut")
    fr = front or mix(ANJALI["front"], (-0.35, -0.45), ease(q))
    ba = backa or mix(ANJALI["backa"], (0.25, -0.3), ease(q))
    swap = {"jd_vk_head": "jd_vk_head_pray"} if shut else {}
    hide = ()
    extra = None
    if seated:
        swap["jd_vk_body"] = "jd_vk_body_sit"
        hide = ("jd_vk_legF", "jd_vk_legB")
        extra = {"jd_vk_body": lambda cr_: pc.paint_part(cr_, "jd_vk_seat", alpha, blur)}
    b_extra = 6 * math.sin(math.pi * q) if 0 < q < 1 else 0.0
    ang = man_angles("jd_vk", t, fr, ba, head, (0.0, 0.0), (), ph)
    r = bob_rot(t, ph, 0.008)
    pts = puppet(cr, J.VK, x, hy, s, r, flip, ang, alpha, blur + b_extra, hide=hide, swap=swap, rods=rods, extra=extra)
    pts["lap"] = local(x, hy, s, r, flip, *J.LAP)
    pts["head_u"] = to_user(cr, pts["head"])
    return pts


# ------------------------------------------------------------------ the chariot


AR_DX, KR_DX = -262.0, 228.0          # where Arjuna and Krishna stand on the deck (chariot units)


def chariot(cr, t, x, feet, s, ar=None, kr=None, alpha=1.0, blur=0.0, horses=True, rods=True, ph=0.0):
    """The chariot (pivot on the ground under the axle), Arjuna at the back, Krishna at the front; ar / kr = keyword
    dicts for arjuna() / krishna() or None. Returns {'arjuna': pts, 'krishna': pts, 'mouth': (x, y)}."""
    out = {}
    hx = x + J.HORSE_DX * s
    if horses:
        prop(cr, "jd_horse_far", hx + 80 * s, feet - 16 * s, s * 0.98, rot=sway(t, 0.006, 0.8, 1.0 + ph), alpha=alpha,
             blur=blur + 1.5)
    prop(cr, "jd_chariot_back", x, feet, s, alpha=alpha, blur=blur)
    deck = feet - J.DECK * s
    cr.save()                                           # the riders stand behind the car's side panel
    cr.new_path()
    cr.rectangle(-2000, -2000, W + 4000, H + 4000)
    pc.spath(cr, [(x + px * s, feet + py * s) for px, py in J.PANEL])
    cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    cr.clip()
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    cr.rectangle(-2000, -2000, W + 4000, deck + 2000 - 60 * s)
    cr.clip()
    if ar is not None:
        out["arjuna"] = arjuna(cr, t, x + AR_DX * s, s, feet=deck, alpha=alpha, blur=blur, rods=False, **ar)
    if kr is not None:
        out["krishna"] = krishna(cr, t, x + KR_DX * s, s, feet=deck, alpha=alpha, blur=blur, rods=False, **kr)
    cr.restore()
    prop(cr, "jd_chariot", x, feet, s, alpha=alpha, blur=blur)
    if horses:
        prop(cr, "jd_horse", hx, feet, s, rot=sway(t, 0.006, 0.8, ph), alpha=alpha, blur=blur)
    prop(cr, "jd_wheel", x + J.WHEEL_XY[0] * s, feet + J.WHEEL_XY[1] * s, s, rot=0.04 * math.sin(t * 0.8),
         alpha=alpha, blur=blur)
    if rods:
        pc.rod(cr, x - 60 * s, feet - 420 * s, x - 110 * s, H + 60, alpha=0.6 * alpha, blur=blur)
        if horses:
            pc.rod(cr, hx, feet - 600 * s, hx + 40 * s, H + 60, alpha=0.6 * alpha, blur=blur)
    out["mouth"] = (hx + 570 * s, feet - 770 * s)
    return out


def point_at(x, hy, s, target, bulk=1.0):
    """front=(upper, fore) for a straight front arm pointing from the shoulder at target (facing right)."""
    sx, sy = x + 26 * bulk * s, hy - 262 * s
    a = math.atan2(target[1] - sy, target[0] - sx)
    return (a - math.pi / 2, 0.0)


# ------------------------------------------------------------------ y1 / y8  "the sun has not set!"


SHOUT = dict(x=262, feet=1790, s=0.53)        # the chariot in the shout shots
SUN_SHOUT = (770, 830, 0.68)


def shout_scene(cr, t, t0, tS, tN, t_draw0, t_draw1, cover, night=0.0):
    sx, sy, ss = SUN_SHOUT
    sun_disc(cr, t, sx, sy, ss, cover=cover)
    ground(cr, y=SHOUT["feet"] + 6)
    x, feet, s = SHOUT["x"], SHOUT["feet"], SHOUT["s"]
    deck = feet - J.DECK * s
    kx = x + KR_DX * s
    hy = deck - 434 * s
    fr = point_at(kx, hy, s, (sx - 40, sy + 30))
    lift = keyed(t, [(t0 - 0.5, 0.75), (t0 + 0.15, 1.0)], 0.3, 1.4)
    fr = mix((-1.0, -0.6), fr, lift)
    draw = clamp((t - t_draw0) / max(0.3, t_draw1 - t_draw0))
    out = chariot(cr, t, x, feet, s,
                  ar=dict(bow="aim", aim=-0.72, draw=0.35 + 0.65 * ease(draw), head=-0.06, ph=1.0),
                  kr=dict(front=fr, backa=(0.35, -0.3), head=-0.14, hits=[(tS, 0.4)], ph=0.4))
    return out


def s_shout(cr, t, tl, t0, t1):
    c = cues(tl, "y1")
    tS, tN = c["S"], c["N"]
    shout_scene(cr, t, t0, tS, tN, -0.5, tN, 0.62)
    sx, sy, ss = SUN_SHOUT
    dev = cr.user_to_device(sx, sy)

    def ui(cr):
        head2(cr, t, "THE SUN HAS", -1.0, "NOT SET!", -0.4, big_size=250, under=tN + 0.1)
        if t > tS:
            red_ring(cr, dev[0] - 10, dev[1], 180, 170, prog(t, tS, 0.45), 10)
    return dict(ui=ui, flash=flash_at(t, tS, 0.25) + flash_at(t, tN, 0.3))


def s_shout2(cr, t, tl, t0, t1):
    c = cues(tl, "y8")
    tV, tA, tS, tN = c["V"], c["A"], c["S"], c["N"]
    out = shout_scene(cr, t, tA - 0.3, tS, tN, tA, tN, 1.0)
    sx, sy, ss = SUN_SHOUT
    dev = cr.user_to_device(sx, sy)
    kh = out["krishna"]["head"]

    def ui(cr):
        if t < tA:
            head2(cr, t, "THEN THAT VOICE:", t0 + 0.05, None, 0.0)
        else:
            head2(cr, t, "THE SUN HAS", tA, "NOT SET!", tS, big_size=250, under=tN + 0.1)
        if t > tS:
            red_ring(cr, dev[0], dev[1], 250, 240, prog(t, tS + 0.1, 0.45), 10)
        if t > tV:
            sound_rings(cr, kh[0] + 50, kh[1] + 10, t, tV, 3, 0.3, 150, alpha=0.4)
    return dict(ui=ui, night=0.3 * (1 - 0.35 * prog(t, tS, 0.6)), flash=flash_at(t, tS, 0.35) + flash_at(t, tN, 0.3))


# ------------------------------------------------------------------ y2  I am Jayadratha


IAM = (470, 1.02, 1890)
IAM_SUN = (890, 880, 0.42)


def s_iam(cr, t, tl, t0, t1):
    c = cues(tl, "y2")
    tJ, tR, tK, tS, tH = c["J"], c["R"], c["K"], c["S"], c["H"]
    sx, sy, ss = IAM_SUN
    if t > tS - 0.2:                                    # the sun rises behind him; the dark disc covers it
        up = ease((t - tS + 0.2) / 0.6)
        cov = ease((t - tH) / 0.7) if t > tH else 0.0
        sun_disc(cr, t, sx, sy + 120 * (1 - up), ss, cover=cov, alpha=clamp(up * 2), glow_a=1.0)
    x, s, feet = IAM
    proud = keyed(t, [(t0, 0.0), (tJ, 1.0)], 0.3, 1.4)
    fr = mix((-0.3, -0.55), (0.2, -2.55), proud)
    look = keyed(t, [(t0, -0.04), (tK, 0.06), (tS, -0.2)], 0.35, 1.3)
    glow(cr, x + 40, feet - 640 * s, 520, 0.25)
    jaya(cr, t, x, s, front=fr, backa=JD_PROUD["backa"], head=look, feet=feet, hits=[(tJ + 0.1, 0.5)], ph=0.3)
    dev_sun = cr.user_to_device(sx, sy)

    def ui(cr):
        if t < tK:
            head2(cr, t, "I AM", t0 + 0.05, "JAYADRATHA", tJ, big_size=210)
            tag(cr, t, tR, "KING OF SINDHU", 790, 1290, 38, t_out=tK - 0.15)
        else:
            head2(cr, t, "TO KILL ME, KRISHNA HAD TO HIDE THE", tK, "SUN", tS, big_size=270, under=tH + 0.1)
        if t > tH:
            red_ring(cr, dev_sun[0], dev_sun[1], 140, 130, prog(t, tH + 0.5, 0.45), 9)
    return dict(ui=ui, flash=flash_at(t, tJ, 0.2) + flash_at(t, tS, 0.3), night=0.18 * prog(t, tH, 0.7))


# ------------------------------------------------------------------ y3  the chakravyuha


VY_C = (560.0, 985.0)                # the spiral's centre
VY_SQ = 0.8                          # vertical squash (seen a little from above)
VY_T = 2.2 * 2 * math.pi             # how far the spiral winds
VY_R0, VY_R1 = 60.0, 420.0


def vy_pt(u):
    """A point on the spiral, u = 0 (the centre) .. 1 (the mouth, at the bottom)."""
    th = VY_T * u
    r = VY_R0 + (VY_R1 - VY_R0) * u
    a = th + (math.pi / 2 - VY_T)
    return VY_C[0] + r * math.cos(a), VY_C[1] + VY_SQ * r * math.sin(a)


VY_N = 27
VY_SOLDIERS = [0.14 + i / (VY_N - 1) * 0.83 for i in range(VY_N)]


def s_vyuha(cr, t, tl, t0, t1):
    c = cues(tl, "y3")
    tC, tP, tB, tA, tM = c["C"], c["P"], c["B"], c["A"], c["M"]
    build = clamp((t - t0 + 0.25) / 0.8)
    path = [vy_pt(i / 200) for i in range(201)]
    dotted(cr, path, build, 19, 7.5, (0.50, 0.24, 0.12), 0.8)
    ax, ay = VY_C
    if t > tA - 0.3:                                    # Abhimanyu inside, small, in a soft light; he falls, fades
        fall = ease((t - tM) / 0.9) if t > tM else 0.0
        a = prog(t, tA - 0.3, 0.4) * (1 - 0.65 * fall)
        glow(cr, ax, ay - 40, 200, 0.5 * a)
        fig(cr, J.ABHI, "jd_abhi", t, ax + 30 * fall, 0.2, front=(-1.2, -0.4), backa=(0.6, -0.2), feet=ay + 50,
            rot=-1.35 * fall, alpha=a, blur=2.5 * fall, rods=False, ph=2.0)
    pts = sorted(((vy_pt(u), u, i) for i, u in enumerate(VY_SOLDIERS)), key=lambda p: p[0][1])
    for (px, py), u, i in pts:                          # the soldiers stand along it, in from the mouth inwards
        ti = t0 - 0.2 + 0.75 * (1 - u)
        q = back(clamp((t - ti) / 0.3), 1.5)
        if q <= 0:
            continue
        sc = 0.105 + 0.05 * u
        soldier(cr, t, px, py + 4 - 30 * (1 - q), sc, flip=px > ax, ph=i * 0.7, alpha=clamp(q * 1.5))
    ground(cr, y=FEET + 6 + 60)
    push = keyed(t, [(t0, 0.0), (tP, 1.0), (tB, 0.0), (tB + 0.5, 0.5), (tB + 0.9, 0.0)], 0.3, 1.5)
    if t > tP - 0.4:                                    # the Pandavas: shadows pushing in from the left
        b, k, a = depth(t, tP - 0.4, 0.5)
        for i, (rig, key, xx, sc) in enumerate(((C.BHIMA, "bhima", 120, 0.56), (C.KING, "king", 250, 0.5),
                                                (J.SOLDIER, "jd_soldier", 0, 0.5))):
            def sh(cr_, rig=rig, key=key, xx=xx, sc=sc, i=i):
                fig(cr_, rig, key, t, xx + 60 * push - 30 * i, sc * k, front=(-1.5, -0.3), backa=(-1.2, -0.4),
                    feet=FEET + 70, rods=False, ph=i, hits=[(tB, 1.0)])
            silhouette(cr, sh, 0.72 * a * (0.85 if i else 1.0))
    jx, js, jf = 520, 0.5, FEET + 70
    arms = keyed(t, [(t0, 0.0), (tP - 0.2, 1.0)], 0.3, 1.5)
    b, k, a = depth(t, t0 - 0.1, 0.45)
    jaya(cr, t, jx, js * k, flip=True, front=(-0.3 - 1.45 * arms, -0.55 + 0.55 * arms),
         backa=(0.3 + 1.35 * arms, -0.25 + 0.25 * arms), feet=jf, alpha=a, blur=b, hits=[(tB, 0.8)], ph=0.5)
    dev_a = cr.user_to_device(ax, ay - 140)

    def ui(cr):
        if t < tA:
            head2(cr, t, "AT THE CHAKRAVYUHA,", t0 + 0.05, "I BLOCKED THE DOOR", tB, big_size=170, under=tB + 0.35)
            tag(cr, t, tP, "THE PANDAVAS", 200, 1150, 34, t_out=tA - 0.2)
        else:
            head2(cr, t, "INSIDE, ABHIMANYU", tA, "FELL", tM, big_size=230, big_color=INK)
            tag(cr, t, tA + 0.1, "ABHIMANYU", dev_a[0] + 170, dev_a[1] - 100, 34)
    return dict(ui=ui, flash=flash_at(t, tB, 0.3), night=0.15 * prog(t, tM, 0.8))


# ------------------------------------------------------------------ y4  Arjuna's vow


PYRE = (820, FEET + 40, 0.82)


def pyre(cr, t, x, feet, s, fire=0.0, alpha=1.0):
    if fire > 0:
        glow(cr, x, feet - 330 * s, (420 + 160 * fire) * s, (0.4 + 0.5 * fire) * (0.85 + 0.15 * math.sin(t * 7)))
    prop(cr, "jd_pyre", x, feet, s, alpha=alpha)
    if fire > 0:
        for i, dx in enumerate((-150, 0, 150)):
            f = int(t * 10 + i) % 3
            fs = (0.55 + 0.55 * fire) * s * (0.9 if i != 1 else 1.15)
            prop(cr, f"flame{f}", x + dx * s, feet - 250 * s, fs * (0.92 + 0.1 * math.sin(t * 6 + i)), alpha=alpha)
        lights(cr, t, x, feet - 520 * s, 160 * s, 10, fire * alpha, (1.0, 0.7, 0.3), 0.8)


def s_vow(cr, t, tl, t0, t1):
    c = cues(tl, "y4")
    tV, tS, tJ, tF = c["V"], c["S"], c["J"], c["F"]
    ground(cr, y=FEET + 46)
    fire = 0.25 * prog(t, t0, 0.5) + 0.75 * prog(t, tF, 0.5)
    pyre(cr, t, *PYRE, fire=fire)
    up = keyed(t, [(t0, 0.0), (tV - 0.1, 1.0)], 0.35, 1.3)
    fr = mix((-0.9, -0.7), (-2.4, -0.25), up)
    arjuna(cr, t, 230, 0.84, bow="raise", front=fr, backa=(0.35 - 0.2 * up, -0.4), head=-0.1 * up, feet=FEET + 40,
           hits=[(tV, 0.6)], ph=1.0)

    def ui(cr):
        head2(cr, t, "ARJUNA'S", t0 + 0.05, "VOW", tV, big_size=250, under=tV + 0.4)
        if t > tS - 0.1:
            quote_note(cr, t, tS - 0.1, 640, 900, 0.72,
                       [("BEFORE SUNSET,", 92, INK, HEAD_FONT, -128, tS),
                        ("JAYADRATHA DIES...", 92, INK, HEAD_FONT, -14, tJ),
                        ("OR INTO THE FIRE", 112, RED, HEAD_FONT, 116, tF)])
    return dict(ui=ui, flash=flash_at(t, tV, 0.35) + flash_at(t, tF, 0.45))


# ------------------------------------------------------------------ y5  hidden; evening


BACK_ROW = (150, 345, 735, 930)       # the soldiers behind him (x), feet at HID_BACK
FRONT_ROW = (100, 280, 460, 620, 800, 980)
HID_BACK, HID_J, HID_FRONT = 1480, 1560, 1700


def s_hidden(cr, t, tl, t0, t1):
    c = cues(tl, "y5")
    tK, tH, tE = c["K"], c["H"], c["E"]
    eve = prog(t, tE - 0.2, 0.9)
    sun_disc(cr, t, 905, 700 + 330 * eve, 0.42, red=eve, glow_a=1.0 + 0.6 * eve)
    ground(cr, y=HID_FRONT + 6)
    ring = [(540 + 470 * math.cos(a), 1590 + 120 * math.sin(a)) for a in (2 * math.pi * i / 120 for i in range(121))]
    dotted(cr, ring, prog(t, tK, 1.2), 26, 6.0, (0.50, 0.24, 0.12), 0.6)
    close = keyed(t, [(t0, 0.0), (tH, 1.0)], 0.3, 1.2)
    for i, x in enumerate(BACK_ROW):                    # the back of the ring
        q = ease((t - tK - 0.1 * i) / 0.7)
        x0 = -150 if x < 540 else W + 150
        soldier(cr, t, x0 + (x - x0) * q, HID_BACK, 0.42, flip=x > 540, ph=i * 0.8 + 3, alpha=0.9 * clamp(q * 2),
                guard=0.0)
    jf = HID_J + 130 * close
    jaya(cr, t, 540, 0.5, feet=jf, front=(-0.4, -0.6), backa=(0.4, -0.4), head=0.14 * close, ph=0.3, rods=False,
         alpha=1.0 - 0.35 * close, blur=3.0 * close)
    for i, x in enumerate(FRONT_ROW):                   # the front of the ring closes in, shields up
        q = ease((t - tK - 0.3 - 0.1 * i) / 0.7)
        x0 = -200 if x < 540 else W + 200
        xx = x0 + (x - x0) * q + (1 if x < 540 else -1) * 45 * close * (abs(x - 540) < 150)
        soldier(cr, t, xx, HID_FRONT, 0.5, flip=x > 540, ph=i * 0.9, alpha=clamp(q * 2), guard=close)
    jx, jy = cr.user_to_device(540, jf - 0.5 * 690)

    def ui(cr):
        if t < tE:
            head2(cr, t, "THE WHOLE ARMY KEPT ME", t0 + 0.05, "HIDDEN", tH, big_size=250)
            if t > tH:
                red_ring(cr, jx, jy, 130, 105, prog(t, tH + 0.2, 0.45), 9)
        else:
            head2(cr, t, "AND THEN IT WAS", tE, "EVENING", tE + 0.06, big_size=250)
    return dict(ui=ui, eve=0.32 * eve, flash=flash_at(t, tH, 0.25))


# ------------------------------------------------------------------ y6  sudden darkness; "the sun has set!"


DARK_SUN = (820, 790, 0.5)


def cheering_row(cr, t, cheer, raise_, alpha=1.0, part=0.0):
    for i, (x, sc, fl, b) in enumerate(((150, 0.44, False, 3.0), (380, 0.44, True, 3.0), (640, 0.44, False, 3.0),
                                        (900, 0.44, True, 3.0))):
        soldier(cr, t, x + (1 if x > 540 else -1) * 200 * part, FEET - 40, sc, flip=fl, ph=i * 1.3 + 5,
                alpha=0.85 * alpha, blur=b, raise_=raise_, cheer=cheer)
    ground(cr, y=FEET + 6 + 70)
    for i, (x, sc, fl) in enumerate(((110, 0.62, False), (330, 0.62, True), (560, 0.62, False), (780, 0.62, True),
                                     (990, 0.62, True))):
        soldier(cr, t, x + (1 if x > 540 else -1) * 260 * part, FEET + 80, sc, flip=fl, ph=i * 0.9,
                alpha=alpha, raise_=raise_, cheer=cheer)


def s_dark(cr, t, tl, t0, t1):
    c = cues(tl, "y6")
    tD, tC, tS = c["D"], c["C"], c["S"]
    sx, sy, ss = DARK_SUN
    cov = ease((t - tD + 0.35) / 0.55)
    dark = prog(t, tD - 0.1, 1.2)
    shroud(cr, sx, sy, 200 + 2400 * dark, 0.45 * dark)
    sun_disc(cr, t, sx, sy, ss, cover=cov, side=1.0)
    cheer = prog(t, tC - 0.1, 0.3)
    raise_ = keyed(t, [(t0, 0.0), (tC - 0.05, 1.0)], 0.25, 1.5)
    cheering_row(cr, t, cheer, raise_)

    def ui(cr):
        if t < tC:
            head2(cr, t, "SUDDENLY,", t0 + 0.05, "DARKNESS", tD, big_size=250)
        else:
            head2(cr, t, "EVERYONE SHOUTED:", tC, "THE SUN HAS SET!", tS, big_size=170, under=tS + 0.35)
        if t > tC:
            for x in (330, 780):
                d = cr.user_to_device(x, 1250)
                sound_rings(cr, d[0], d[1], t, tC, 6, 0.3, 300, alpha=0.5)
    return dict(ui=ui, night=NIGHT * dark, flash=flash_at(t, tC, 0.2), lift=dark)


# ------------------------------------------------------------------ y7  I came out to look


LOOK_SUN = (290, 800, 0.46)


def s_look(cr, t, tl, t0, t1):
    c = cues(tl, "y7")
    tJ, tL = c["J"], c["L"]
    sx, sy, ss = LOOK_SUN
    shroud(cr, sx, sy, 2600, 0.45)
    aura(cr, t, sx, sy, 200 * ss, 380 * ss, 0.8, n=26, spin=0.08)
    prop(cr, "sun", sx, sy, ss, rot=t * 0.2)
    prop(cr, "jd_maya", sx, sy, ss, rot=-0.25 * t)
    part = ease((t - tJ + 0.2) / 0.6)
    out_ = clamp((t - tJ) / 1.0)
    for i, (x, sc, fl) in enumerate(((180, 0.44, False), (420, 0.44, True), (660, 0.44, False), (900, 0.44, True))):
        soldier(cr, t, x + (1 if x > 540 else -1) * 120 * part, FEET - 40, sc, flip=fl, ph=i * 1.3, alpha=0.85,
                blur=3.0)
    behind = out_ < 0.5

    def jd(cr_):
        x = 640 - 60 * ease(out_)
        s = 0.5 + 0.18 * ease(out_)
        feet = FEET - 30 + 112 * ease(out_)
        look = keyed(t, [(t0, 0.06), (tJ + 0.3, -0.05), (tL, -0.42)], 0.4, 1.3)
        up = keyed(t, [(t0, 0.0), (tL + 0.1, 1.0)], 0.35, 1.3)
        hop = abs(math.sin(math.pi * clamp((t - tJ) / 0.5))) * 30 * (0 < t - tJ < 1.0)
        jaya(cr_, t, x, s, flip=True, feet=feet - hop, head=look, front=(-0.4 - 2.0 * up, -0.4 + 0.15 * up),
             backa=(0.5, -0.6), ph=0.3, blur=2.0 * (1 - out_) if behind else 0.0, hits=[(tJ + 0.5, 0.6)])
        return x, s, feet
    if behind:
        jd(cr)
    ground(cr, y=FEET + 86)
    for i, (x, sc, fl) in enumerate(((120, 0.6, False), (350, 0.6, True), (760, 0.6, False), (980, 0.6, True))):
        soldier(cr, t, x + (1 if x > 540 else -1) * 160 * part, FEET + 84, sc, flip=fl, ph=i * 0.9)
    if not behind:
        jx, js, jf = jd(cr)
        if t > tL:                                      # his line of sight to the sky
            ex, ey = jx - 30 * js, jf - 434 * js - 410 * js
            pts = [(ex + (sx + 120 - ex) * u, ey + (sy + 110 - ey) * u) for u in (i / 40 for i in range(41))]
            dotted(cr, pts, prog(t, tL + 0.1, 0.5), 30, 6.0, (1.0, 0.86, 0.5), 0.8)

    def ui(cr):
        head2(cr, t, "I CAME OUT", t0 + 0.05, "TO LOOK", tL, big_size=250, under=tL + 0.4)
    return dict(ui=ui, night=NIGHT, lift=1.0, flash=flash_at(t, tJ, 0.15))


# ------------------------------------------------------------------ y9  my shield: my father's words


def s_shield(cr, t, tl, t0, t1):
    c = cues(tl, "y9")
    tD, tF, tG, tB = c["D"], c["F"], c["G"], c["B"]
    ground(cr, y=FEET + 46)
    warn = keyed(t, [(t0, 0.0), (tF, 1.0)], 0.35, 1.3)
    b, k, a = depth(t, t0 - 0.1, 0.45)
    glow(cr, 200, 1420, 420, 0.3 * a)
    father(cr, t, 185, FEET + 40, 0.68 * k, rise=1.0, eyes="open", alpha=a, blur=b,
           front=mix((-0.35, -0.45), (-2.05, -0.85), warn), backa=(0.25, -0.3), head=-0.06, ph=0.6)

    def ui(cr):
        head2(cr, t, "BUT I HAD ONE", t0 + 0.05, "SHIELD", tD, big_size=250, under=tD + 0.4)
        tag(cr, t, tF + 0.1, "MY FATHER", 470, 1330, 36)
        if t > tF - 0.1:
            quote_note(cr, t, tF - 0.1, 610, 880, 0.88,
                       [("MY FATHER SAID:", 46, INK, MONO_FONT, -178, tF + 0.1),
                        ("WHOEVER DROPS MY SON'S HEAD", 70, INK, HEAD_FONT, -92, tF + 0.45),
                        ("TO THE GROUND,", 70, INK, HEAD_FONT, -8, tG),
                        ("THEIR OWN HEAD BURSTS", 70, INK, HEAD_FONT, 76, tG + 0.6),
                        ("IN 100 PIECES", 104, RED, HEAD_FONT, 172, tB)])
        if t > tB + 0.5:
            stamp(cr, t, tB + 0.5, "MY SHIELD", 780, 1200, 64, rot=-0.08)
    return dict(ui=ui, flash=flash_at(t, tD, 0.25) + flash_at(t, tB, 0.3))


# ------------------------------------------------------------------ y10  Krishna knew


def s_knew(cr, t, tl, t0, t1):
    c = cues(tl, "y10")
    tK, tW = c["K"], c["W"]
    x, s, feet = 430, 1.32, 2230
    hy = feet - 434 * s
    on = prog(t, t0, 0.6)
    hx, hyy = x + 30 * s, hy - 410 * s
    glow(cr, hx, hyy, 640, (0.55 + 0.25 * prog(t, tW, 0.5)) * on * (0.9 + 0.1 * math.sin(t * 2.2)))
    aura(cr, t, hx - 20, hyy - 40, 160, 520 + 80 * prog(t, tW, 0.6), 0.5 * on + 0.3 * prog(t, tW, 0.5), n=22,
         spin=0.06)
    bless = keyed(t, [(t0, 0.0), (tW - 0.1, 1.0)], 0.4, 1.2)
    krishna(cr, t, x, s, feet=feet, front=mix((-0.3, -0.55), (-0.55, -1.75), bless), backa=(0.25, -0.3),
            head=0.04 - 0.05 * bless, ph=0.4, rods=False)
    lights(cr, t, hx + 140, hyy + 200, 260, 9, 0.5 * on + 0.4 * prog(t, tW, 0.5), speed=0.3)

    def ui(cr):
        head2(cr, t, "AND KRISHNA", t0 + 0.05, "KNEW", tW, big_size=270, under=tW + 0.4)
    return dict(ui=ui, night=0.32, lift=0.8, flash=flash_at(t, tW, 0.3))


# ------------------------------------------------------------------ y11  the arrow carries it to the father's lap


AR11 = (130, FEET + 90, 0.44)        # Arjuna (x, feet, scale)
JD11 = (455, FEET + 90, 0.4)         # Jayadratha
HERM = (850, 1440, 0.36)             # the far hermitage: the father's x, ground y, scale


def hill(cr, cx, top, w, base, col=(0.86, 0.74, 0.50), alpha=1.0):
    """A far hill of leather (a soft mound from base up to top)."""
    pts = [(cx - w, base + 40), (cx - 0.82 * w, top + 120), (cx - 0.5 * w, top + 14), (cx, top),
           (cx + 0.5 * w, top + 10), (cx + 0.9 * w, top + 70), (cx + 1.2 * w, base + 40)]
    cr.save()
    cr.new_path()
    pc.spath(cr, pts)
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(*col, alpha)
    cr.fill_preserve()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.set_source_rgba(*pc.INK, 0.85 * alpha)
    cr.set_line_width(5)
    cr.stroke()
    cr.restore()


def hermitage_far(cr, t, alpha=1.0, glow_a=0.0):
    fx, gy, fs = HERM
    prop(cr, "tree", fx + 200, gy + 8, 0.4, rot=sway(t, 0.006, 0.3, 2), alpha=0.6 * alpha, blur=5)
    hill(cr, fx + 30, gy, 330, FEET + 52, alpha=alpha)
    prop(cr, "lr_hut", fx + 125, gy + 6, 0.32, alpha=0.8 * alpha, blur=2.0)
    yajna_fire(cr, t, fx - 135, gy, 0.42, 0.2, alpha)
    prop(cr, "md_mat", fx + 30, gy - 2, 0.3, alpha=alpha)
    if glow_a > 0:
        glow(cr, fx + 20, gy - 120, 260, glow_a)
    return father(cr, t, fx, gy, fs, rise=0.0, alpha=alpha, rods=False, ph=0.6)


def arc_pts(p0, p1, peak, n=80):
    """A parabola-like arc from p0 to p1 rising to y = peak."""
    out = []
    for i in range(n + 1):
        u = i / n
        base = p0[1] + (p1[1] - p0[1]) * u
        out.append((p0[0] + (p1[0] - p0[0]) * u, base - (min(p0[1], p1[1]) - peak) * 4 * u * (1 - u)))
    return out


def along(pts, p):
    """The point at fraction p of a polyline's length, and the direction there."""
    lens = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(lens) * clamp(p)
    acc = 0.0
    for (a, b), ln in zip(zip(pts, pts[1:]), lens):
        if acc + ln >= total:
            f = (total - acc) / ln if ln else 0.0
            return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f), math.atan2(b[1] - a[1], b[0] - a[0])
        acc += ln
    a, b = pts[-2], pts[-1]
    return b, math.atan2(b[1] - a[1], b[0] - a[0])


def s_arrow(cr, t, tl, t0, t1):
    c = cues(tl, "y11")
    tA, tP, tL = c["A"], c["P"], c["L"]
    sx, sy, ss = 160, 780, 0.34
    shroud(cr, sx, sy, 2600, 0.32)
    aura(cr, t, sx, sy, 200 * ss, 380 * ss, 0.75, n=26, spin=0.08)
    prop(cr, "sun", sx, sy, ss, rot=t * 0.2)
    prop(cr, "jd_maya", sx, sy, ss, rot=-0.25 * t)
    lap_glow = 0.5 * prog(t, tL, 0.3) * math.exp(-1.2 * max(0.0, t - tL - 0.3)) + 0.3 * prog(t, tP, 0.4)
    fp = hermitage_far(cr, t, glow_a=lap_glow)
    lap = fp["lap"]
    ground(cr, y=FEET + 96)
    ax, af, as_ = AR11
    jx, jf, js = JD11
    t_hit = tA + 0.28
    head0 = (jx - 20 * js, jf - 434 * js - 410 * js)
    arc = arc_pts(head0, (lap[0], lap[1] - 22), 720)
    fly = clamp((t - t_hit) / max(0.5, tL - t_hit))
    if t > t_hit:                                       # the path (a dotted arc), drawn ahead of the flight
        dotted(cr, arc, min(1.0, fly + 0.18), 30, 6.5, RED, 0.85)
    if t < t_hit + 0.4:                                 # Jayadratha, looking up; struck, he is gone in the flash
        gone = ease((t - t_hit) / 0.3) if t > t_hit else 0.0
        jaya(cr, t, jx, js, flip=True, feet=jf, head=-0.32, front=(-1.6, -0.3), backa=(0.5, -0.5),
             alpha=1 - gone, blur=10 * gone, rods=t < t_hit, ph=0.3)
    draw = clamp((t - t0 - 0.1) / max(0.3, tA - t0 - 0.2))
    released = t >= tA
    pts = arjuna(cr, t, ax, as_, bow="aim", aim=-0.08, draw=0.0 if released else 0.2 + 0.8 * ease(draw),
                 arrow=not released, feet=af, hits=[(tA, 0.5)], ph=1.0)
    if released and t < t_hit:                          # the arrow to him
        nk = pts.get("nock", (ax + 120, af - 300 * as_))
        u = (t - tA) / (t_hit - tA)
        x0, y0 = nk[0] + (head0[0] - 60 - nk[0]) * u, nk[1] + (head0[1] - nk[1]) * u
        arrow_at(cr, x0, y0, math.atan2(head0[1] - nk[1], head0[0] - 60 - nk[0]), 150)
    if t > t_hit:
        burst(cr, t, head0[0], head0[1] + 80, t_hit, n=18, rmax=420, alpha=1.0)
    if t_hit < t:                                       # the head: a small dark silhouette riding the arrow, seen
        (hx, hy), ang = along(arc, fly)                 # only once it is well away from him, out of the light
        if fly < 1:
            show = clamp((fly - 0.07) / 0.06)
            arrow_at(cr, hx - 125 * math.cos(ang), hy - 125 * math.sin(ang), ang, 118,
                     alpha=show * (1.0 - prog(t, tL - 0.4, 0.3)))
            for k in range(6):                          # a faint trail of light
                (qx, qy), _ = along(arc, max(0.0, fly - 0.02 * (k + 1)))
                sparkle(cr, qx, qy, 14 - 2 * k, (0.5 - 0.07 * k) * show)
            head_sil(cr, hx, hy, 24, rot=0.6 * math.sin(6 * fly), alpha=show)
        else:
            head_sil(cr, lap[0], lap[1] - 22, 22, rot=0.3, alpha=1.0, rim=0.8)
    dev_lap = cr.user_to_device(*lap)
    dev_h = cr.user_to_device(HERM[0], HERM[1] - 330 * HERM[2])

    def ui(cr):
        if t < tL:
            head2(cr, t, "THE ARROW CARRIED IT", t0 + 0.05, "FAR AWAY", tP, big_size=220)
        else:
            head2(cr, t, "INTO MY FATHER'S", tL, "LAP", tL + 0.06, big_size=260, under=tL + 0.35)
            red_ring(cr, dev_lap[0], dev_lap[1] - 10, 90, 70, prog(t, tL + 0.25, 0.4), 8)
        tag(cr, t, tP, "MY FATHER, AT PRAYER", min(dev_h[0], 800), dev_h[1] + 330, 30)
    return dict(ui=ui, night=0.3, lift=1.0, flash=flash_at(t, t_hit, 0.6, 3.0))


# ------------------------------------------------------------------ y12 / y13  he stands; it falls; his own curse


HC = (470, FEET + 60, 0.84)          # the father in the close shots: x, ground, scale


def herm_close(cr, t, tU, tG, tC=None, tF=None):
    """The hermitage close: the fire, the hut and a tree behind; the father seated with the dark shape in his lap,
    rising at tU (it slips and lands on the ground at tG); tC / tF: the curse and the burst (y13)."""
    x, gy, s = HC
    prop(cr, "tree", 60, gy + 10, 0.66, rot=sway(t, 0.006, 0.3, 1), alpha=0.55, blur=10, flip=True)
    prop(cr, "lr_hut", 960, gy + 8, 0.7, alpha=0.6, blur=7)
    ground(cr, y=gy + 6)
    yajna_fire(cr, t, 920, gy, 0.9, 0.15)
    prop(cr, "md_mat", x + 60, gy - 2, 0.58)
    rise = ease((t - tU) / 0.4) if t > tU else 0.0
    burst_t = tF
    gone = 0.0
    if burst_t is not None and t > burst_t:
        gone = ease((t - burst_t - 0.35) / 0.9)
    sil = clamp((t - burst_t + 0.15) / 0.15) if burst_t is not None else 0.0

    def draw_f(cr_):
        return father(cr_, t, x, gy, s, rise=rise, ph=0.6, rods=False, head=-0.08 * rise)
    if sil > 0:
        silhouette(cr, draw_f, sil * (1 - gone))
    else:
        draw_f(cr)
    hy = gy - J.SEAT_H * s + (J.SEAT_H - 434) * s * rise
    head = (x + 22 * s, hy - 412 * s)
    lap_sit = local(x, gy - J.SEAT_H * s, s, 0, False, *J.LAP)
    # the dark shape: in his lap, then slipping off as he stands and dropping to the ground
    r_h = 46
    if t < tU + 0.12:
        hp, rot = (lap_sit[0], lap_sit[1] - r_h * 0.9), 0.3
    else:
        u = clamp((t - tU - 0.12) / max(0.3, tG - tU - 0.12))
        x0, y0 = lap_sit[0] + 30, lap_sit[1] - r_h * 0.9
        x1, y1 = lap_sit[0] + 125, gy - r_h * 1.05
        hp = (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u * u)
        rot = 0.3 + 0.5 * u
        if t > tG:
            dt = t - tG
            hp = (x1, y1 - 30 * abs(math.sin(9 * dt)) * math.exp(-5 * dt))
            rot = 0.8 - 0.3 * math.exp(-4 * dt)
    head_sil(cr, hp[0], hp[1], r_h, rot=rot, alpha=1.0, rim=0.6)
    if t > tG:
        d = cr.user_to_device(hp[0], gy)
        sound_rings(cr, d[0], d[1] - 10, t, tG, 3, 0.18, 160, alpha=0.4)
    if tC is not None and t > tC and (burst_t is None or t < burst_t + 0.2):
        k = prog(t, tC, 0.5)                            # the curse gathers round his head: a dark ring
        cr.save()
        cr.set_source_rgba(0.12, 0.05, 0.1, 0.5 * k)
        cr.set_line_width(14)
        for i in range(3):
            rr = 120 - 25 * i + 10 * math.sin(t * 5 + i)
            cr.arc(head[0], head[1], rr * (1.3 - 0.3 * k), 0, 2 * math.pi)
            cr.stroke()
        cr.restore()
    if burst_t is not None and t > burst_t:
        burst(cr, t, head[0], head[1], burst_t, n=26, rmax=900, alpha=1.0)
        for i in range(14):                             # shards of light flying out
            a = 2 * math.pi * i / 14 + 0.3
            u = (t - burst_t)
            rr = 40 + 900 * (1 - math.exp(-2.2 * u))
            aa = math.exp(-1.6 * u)
            sparkle(cr, head[0] + rr * math.cos(a), head[1] + rr * math.sin(a), 26 * aa + 4, aa)
        drift_lights(cr, t, x, gy - 200, 260, 700, 10, 0.8 * gone * math.exp(-0.3 * max(0.0, t - burst_t - 1.2)))
    return head, hp


def s_fall(cr, t, tl, t0, t1):
    c = cues(tl, "y12")
    tU, tG = c["U"], c["G"]
    head, hp = herm_close(cr, t, tU, tG)
    dev = cr.user_to_device(*hp)

    def ui(cr):
        if t < tG:
            head2(cr, t, "MY FATHER", t0 + 0.05, "STOOD UP", tU, big_size=250)
        else:
            head2(cr, t, "IT FELL TO THE", tG, "GROUND", tG + 0.06, big_size=250, under=tG + 0.35)
            red_ring(cr, dev[0], dev[1], 90, 80, prog(t, tG + 0.2, 0.4), 8)
    return dict(ui=ui, night=0.22, lift=0.6, flash=flash_at(t, tG, 0.3))


def s_curse(cr, t, tl, t0, t1):
    c12 = cues(tl, "y12")
    c = cues(tl, "y13")
    tC, tF = c["C"], c["F"]
    herm_close(cr, t, c12["U"], c12["G"], tC, tF)
    white = 0.85 * math.exp(-3.2 * max(0.0, t - tF - 0.05)) * clamp((t - tF + 0.05) / 0.08) if t > tF - 0.05 else 0.0

    def ui(cr):
        head2(cr, t, "HIS OWN", t0 + 0.05, "CURSE", tC, big_size=270, under=tF + 0.3)
    return dict(ui=ui, night=0.22, lift=0.6, flash=flash_at(t, tF, 0.9, 2.5), white=white)


# ------------------------------------------------------------------ y14  whose fault?


END_FIGS = ((204, "JAYADRATHA?"), (540, "KRISHNA?"), (876, "THE FATHER?"))
END_CS = 0.36                        # the cards' scale (the plaque is 780 units wide: 281 px)
END_S = 0.58                         # the three figures' scale


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "y14")
    tS, tL, tQ, tW = c["S"], c["L"], c["Q"], c["W"]
    ground(cr, y=FEET + 46)
    side = None
    if t > tW:
        n = int((t - tW) / 0.8)
        side = n % 3
    gl = [0.25, 0.25, 0.25]
    if side is not None:
        gl[side] = 0.55
    for i, (x, _) in enumerate(END_FIGS):
        glow(cr, x, 1450, 340, gl[i])
    s = END_S
    jx = END_FIGS[0][0]
    shield = prog(t, tS, 0.5)                           # the curse as a ring of light round him, meant to save him
    broken = prog(t, tL, 0.6)                           # ... then it breaks, and the father's light goes
    if shield > 0 and broken < 1:
        cy = FEET + 40 - 540 * s
        grow = 1 + 0.25 * broken
        for i in range(30):
            a0 = 2 * math.pi * i / 30 + 0.2 * t
            if broken > 0 and i % 3 == 0:
                continue
            cr.save()
            cr.translate(jx, cy)
            cr.scale(165 * grow, 312 * grow)
            cr.new_path()
            cr.arc(0, 0, 1, a0, a0 + 0.13 * shield)
            cr.restore()
            cr.set_source_rgba(*(RED if broken > 0 else (1.0, 0.80, 0.30)), 0.9 * shield * (1 - broken))
            cr.set_line_width(10)
            cr.stroke()
        glow(cr, jx, cy, 340, 0.4 * shield * (1 - broken))
    jaya(cr, t, jx, s, feet=FEET + 40, front=(-0.4, -0.6), backa=(0.4, -0.4), head=0.06, ph=0.3)
    krishna(cr, t, END_FIGS[1][0], s, feet=FEET + 40, front=(-0.55, -1.75), backa=(0.25, -0.3), ph=0.5)
    fa = 1.0 - 0.45 * broken + 0.45 * prog(t, tQ, 0.5) * broken
    father(cr, t, END_FIGS[2][0], FEET + 40, s, rise=1.0, eyes="shut", flip=True, alpha=fa, ph=0.8, head=0.08)
    if t < tQ + 0.5:
        drift_lights(cr, t, END_FIGS[2][0], 1450, 160, 420, 7, 0.7 * broken * (1 - prog(t, tQ, 0.5)))

    def ui(cr):
        if t < tQ:
            head2(cr, t, "THE CURSE MEANT TO SAVE ME...", t0 + 0.05, "TOOK MY FATHER", tL, big_size=170,
                  big_color=INK)
        else:
            head2(cr, t, "NOW YOU TELL ME:", tQ, "WHOSE FAULT?", tW, big_size=230, under=tW + 0.35)
        size = min(150, *[int(64 * 590 / text_size(txt, 64)[0]) for _, txt in END_FIGS])
        for i, (cx, txt) in enumerate(END_FIGS):
            card(cr, t, tQ - 0.25 + 0.15 * i, cx, 880, END_CS, [(txt, size, RED, 4)])
        if side is not None:
            ts = tW + 0.8 * int((t - tW) / 0.8)
            red_ring(cr, END_FIGS[side][0], 884, 172, 66, prog(t, ts, 0.3), 9)
    return dict(ui=ui, flash=flash_at(t, tW, 0.25))


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("y1", None, s_shout, {"z": (1.0, 1.04)}),
    ("y2", None, s_iam, {"z": (1.0, 1.04)}),
    ("y3", None, s_vyuha, {"z": (1.0, 1.03)}),
    ("y4", None, s_vow, {}),
    ("y5", None, s_hidden, {"z": (1.0, 1.03)}),
    ("y6", None, s_dark, {"z": (1.0, 1.04)}),
    ("y7", None, s_look, {"z": (1.0, 1.05)}),
    ("y8", None, s_shout2, {"z": (1.02, 1.07)}),
    ("y9", None, s_shield, {"z": (1.0, 1.03)}),
    ("y10", None, s_knew, {"z": (1.0, 1.07)}),
    ("y11", None, s_arrow, {"z": (1.0, 1.02)}),
    ("y12", None, s_fall, {"z": (1.0, 1.04)}),
    ("y13", None, s_curse, {"z": (1.04, 1.08)}),
    ("y14", None, s_end, {"z": (1.0, 1.03)}),
]


def title_lift(cr, a):
    """In the dark shots, the small lamp over the title stays lit so the headline reads."""
    if a <= 0.01:
        return
    g = cairo.RadialGradient(540, 420, 60, 540, 420, 620)
    g.add_color_stop_rgba(0, 1.0, 0.93, 0.76, 0.5 * a)
    g.add_color_stop_rgba(0.6, 1.0, 0.90, 0.70, 0.28 * a)
    g.add_color_stop_rgba(1, 1.0, 0.88, 0.66, 0.0)
    cr.save()
    cr.set_source(g)
    cr.paint()
    cr.restore()


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl, SHOTS)
    _, _, fn, opt = SHOTS[k]
    z0, z1 = opt.get("z", (1.0, 1.05))
    z = z0 + (z1 - z0) * clamp((t - t0) / max(0.5, t1 - t0))
    fx, fy = opt.get("focus", (540, 1060))
    cr.save()
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    pc.screen(cr)
    out = fn(cr, t, tl, t0, t1) or {}
    tint(cr, (1.0, 0.66, 0.42), out.get("eve", 0.0))
    cr.restore()
    motes(cr, t)
    pc.lamp(cr, t, night=out.get("night", 0.0), flash=out.get("flash", 0.0))
    title_lift(cr, out.get("lift", 0.0) * out.get("night", 0.0) / NIGHT)
    if out.get("white", 0.0) > 0.01:
        cr.set_source_rgba(1.0, 0.98, 0.93, clamp(out["white"]))
        cr.paint()
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the cold open, a
    conch on Arjuna's vow, a conch as the darkness falls, a single hit when the head falls to the ground, a bell on the
    closing question, then (only where they fit) a damaru on the callback shout, shimmer as Krishna "knew" and on the
    burst of light. Chosen in THAT order of importance, each at least SFX_MIN_GAP from every sound already kept, so the
    hit is never pushed out by a shimmer; render_myth.calm_sfx then keeps the whole list (it is already spaced). 6-7
    sounds on the voiced timelines; the bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["y4"]["V"], "conch", 0), (c["y6"]["D"], "conch", 0), (c["y12"]["G"], "hit", 0),
            (c["y14"]["W"], "bell", 0), (c["y8"]["N"], "damaru", 0), (c["y10"]["W"], "shimmer", 0),
            (c["y13"]["F"], "shimmer", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["y2"]["t0"] - 0.3, "dip", 0.5), (c["y8"]["t0"] - 0.3, "dip", 0.5), (c["y13"]["F"] - 0.35, "dip", 0.5)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
