"""Scenes for videos/lakshman_rekha.py: "Lakshman Rekha is not in the Valmiki Ramayana", in Togalu Gombeyaata (Karnataka
leather shadow-puppet theatre) drawn in code: the same lamp-lit screen, two-tier headlines and rod-puppet motion as the
Jarasandha, Ravana and Kaikeyi reels, with the cast from lrekha_cast. ONE idea, one point per shot: the famous glowing
line on the ground, then the text itself (Valmiki: no line, only a blessing), then where the line does come from (one
taunt of Mandodari's in Tulsidas' Lanka Kand). Both books are honoured the same way (the same palm-leaf manuscript,
opened the same way). Every frame is a pure function of t. English on-screen text only (shared by Hindi and Kannada);
cues are words of the line in each language ({"hi": ..., "kn": ...}) with a fraction fallback, kept in one table (CUES)
that the scenes and sfx() both read, with minimum gaps so a fast voice can't bunch the beats together.

Shot list (line: what is on the screen)
  l1  HOOK: frame 0 = the golden line being drawn across a big slab of lamp-lit earth, alone; LAKSHMAN REKHA? / NOT IN
      VALMIKI (big words in by 0.4 s); on "Lakshman" little flames run along it; WE QUOTE IT EVERY DAY tag; on
      "Valmiki" a big red X slashes across it (underlined); on "nahi" the line gutters out
  l2  THIS IS NOT A / RUMOUR (crossed out); a palm-leaf manuscript rises, opens on "Valmiki": VALMIKI RAMAYANA, then
      ARANYA KANDA 3.45 (ringed); DON'T BELIEVE ME? / READ IT YOURSELF
  l3  the hut; Sita and Rama; the golden deer prances in, shimmering: SITA SAW A / GOLDEN DEER; Sita points; Rama turns
      and goes after it into the trees: RAMA WENT TO / CATCH IT
  l4  night falls on the forest; trees sway; jagged letters HA SITA! HA LAKSHMANA! burst from the trees with ripples;
      Sita and Lakshmana start: A CRY IN / RAMA'S VOICE
  l5  Sita, afraid (hand at her heart), turns to Lakshmana, reaches out, points to the forest: SITA WAS / AFRAID, then
      SITA, TO LAKSHMANA: GO, SAVE / YOUR BROTHER
  l6  Lakshmana raises a calm hand and shakes his head: LAKSHMANA SAID: / NOT RAMA'S VOICE; card A DEMON'S / TRICK;
      leaf ARANYA KANDA 3.45.16
  l7  Sita, upset, speaks; harsh words only as dark jagged shapes flying to Lakshmana, who bows his head: SITA DID NOT /
      AGREE, then UPSET, SHE SPOKE / HARSH WORDS
  l8  the ground in front of the hut, seen large; Lakshmana turns and walks away: HURT, LAKSHMANA / LEFT; an empty
      dotted outline where people imagine the line: BUT ON THE GROUND HE DREW / NO LINE
  l9  Lakshmana folds his hands toward the trees; soft lights wake among the leaves; the note MAY ALL THE FOREST GODS /
      PROTECT YOU; NO LINE. ONLY / A BLESSING; leaf ARANYA KANDA 3.45.33-34
  l10 RE-HOOK: night; the line flickers back faintly on the bare earth; a big red "?": SO WHERE DID THE LINE / COME
      FROM?
  l11 a palm-leaf calendar flips (years go by): MUCH LATER, IN THE / 1500s; a second manuscript drops in and opens, a
      quill writes: TULSIDAS, RAMCHARITMANAS 1500s; TULSIDAS WROTE THE / RAMCHARITMANAS
  l12 the hut again (quick); Ravana's shadow comes near; the dotted outline: TULSIDAS TOO, AT THE ABDUCTION: / NO LINE
  l13 the hall of Lanka: THE LINE COMES LATER, IN / LANKA KAND (leaf LANKA KAND, DOHA 35); Mandodari speaks to
      Ravana: MANDODARI'S / TAUNT; on "Lakshman" a speech cloud pops (YOU COULDN'T EVEN CROSS), on "small" a
      golden line draws itself in it (LAKSHMANA'S SMALL LINE), ringed as she says "cross"; Ravana's heads droop
  l14 a palm leaf seen close, six lines of writing; one line lights up and is ringed: AND THAT TOO, IN / JUST ONE LINE
      (the line itself reads "रामानुज लघु रेख खचाई" when the Devanagari font is on the machine)
  l15 the two manuscripts side by side: VALMIKI / NO LINE and TULSIDAS / A LINE; SO, WHICH ONE DO YOU / BELIEVE?; a red
      ring alternates between them while the line on the earth below goes out and comes back with it
"""
import math
import os
import random

import cairo

import lrekha_cast as L
import puppet_core as pc
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, text_size
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_jarasandha import (FADE, FEET, INK, LIGHT, RED, bob_rot, glow, ground, motes, red_ring, sound_rings, tag,
                               walk_legs, woman_angles)
from scenes_kaikeyi import ANJALI, calendar, card, fig, leaf_tag, rama, segs_line
from scenes_ravana import dotted, head2, in_hand, rv, rv_angles
from shots import T, shot_at, starts

MISSES = set()                       # cue words not found in a line (falls back to fractions)
DEVA_FONT = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "Nirmala.ttc")
HAS_DEVA = os.path.exists(DEVA_FONT)
DOHA = "रामानुज लघु रेख खचाई"         # Ramcharitmanas, Lanka Kand, under doha 35 (Mandodari to Ravana)
SLAB_FEET = 1380                     # the ground-shots: the earth slab's top edge (figures stand on it)
DOT_C = (1.0, 0.88, 0.62)            # the empty, imagined outline on the earth
CRY_C = (0.66, 0.07, 0.04)


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, words)
    except (KeyError, ValueError):
        MISSES.add((bid, words[getattr(tl, "lang", "hi")] if isinstance(words, dict) else words))
        return T(tl, bid, frac)


# Every cue of every line: (name, {"hi": word, "kn": word}, fraction fallback, ((after, min gap), ...)); "t0" = the
# line's start. Words are given without nukta / chandrabindu tails where the speech recogniser may drop them.
CUES = {
    "l1": (("D", {"hi": "रोज", "kn": "ದಿನಾ"}, 0.45, (("t0", 0.9),)),
           ("L", {"hi": "लक्ष्मण", "kn": "ಲಕ್ಷ್ಮಣ"}, 0.2, (("t0", 0.9),)),
           ("V", {"hi": "वाल्मीकि", "kn": "ವಾಲ್ಮೀಕಿ"}, 0.6, (("L", 1.0), ("D", 0.7), ("t0", 2.2))),
           ("N", {"hi": "नहीं", "kn": "ಇಲ್ಲ"}, 0.92, (("V", 0.8),))),
    "l2": (("X", {"hi": "नहीं", "kn": "ಅಲ್ಲ"}, 0.3, (("t0", 0.6),)),
           ("V", {"hi": "वाल्मीकि", "kn": "ವಾಲ್ಮೀಕಿ"}, 0.42, (("X", 0.6),)),
           ("A", {"hi": "अरण्य", "kn": "ಅರಣ್ಯ"}, 0.62, (("V", 0.8),)),
           ("P", {"hi": "पढ", "kn": "ನೀವೇ"}, 0.82, (("A", 0.7),))),
    "l3": (("G", {"hi": "सोने", "kn": "ಬಂಗಾರ"}, 0.25, (("t0", 0.5),)),
           ("D", {"hi": "हिरण", "kn": "ಜಿಂಕೆ"}, 0.42, (("G", 0.35),)),
           ("R", {"hi": "राम", "kn": "ರಾಮ"}, 0.62, (("D", 0.6),)),
           ("C", {"hi": "गए", "kn": "ಹೋದ"}, 0.92, (("R", 0.5),))),
    "l4": (("J", {"hi": "जंगल", "kn": "ಕಾಡಿಂದ"}, 0.3, (("t0", 0.7),)),
           ("R", {"hi": "राम", "kn": "ರಾಮನ"}, 0.48, (("J", 0.4),)),
           ("C", {"hi": "चीख", "kn": "ಕೂಗು"}, 0.85, (("R", 0.6),))),
    "l5": (("F", {"hi": "डर", "kn": "ಹೆದರಿದ್ಲು"}, 0.12, (("t0", 0.3),)),
           ("L", {"hi": "लक्ष्मण", "kn": "ಲಕ್ಷ್ಮಣನಿಗೆ"}, 0.4, (("F", 0.6),)),
           ("G", {"hi": "जाओ", "kn": "ಹೋಗು"}, 0.62, (("L", 0.5),)),
           ("B", {"hi": "बचाओ", "kn": "ಕಾಪಾಡು"}, 0.9, (("G", 0.5),))),
    "l6": (("N", {"hi": "नहीं", "kn": "ಅಲ್ಲ"}, 0.5, (("t0", 0.8),)),
           ("D", {"hi": "राक्षस", "kn": "ರಾಕ್ಷಸನ"}, 0.78, (("N", 0.7),))),
    "l7": (("N", {"hi": "मानी", "kn": "ಒಪ್ಪಲಿಲ್ಲ"}, 0.15, (("t0", 0.3),)),
           ("A", {"hi": "उन्होंने", "kn": "ಕೋಪದಲ್ಲಿ"}, 0.4, (("N", 0.6),)),
           ("H", {"hi": "बहुत", "kn": "ತುಂಬಾ"}, 0.7, (("A", 0.6),))),
    "l8": (("W", {"hi": "चले", "kn": "ಹೊರಟ"}, 0.3, (("t0", 0.5),)),
           ("P", {"hi": "पर", "kn": "ಆದ್ರೆ"}, 0.5, (("W", 0.6),)),
           ("R", {"hi": "रेखा", "kn": "ಗೆರೆಯನ್ನೂ"}, 0.78, (("P", 0.6),)),
           ("N", {"hi": "नहीं", "kn": "ಎಳೀಲಿಲ್ಲ"}, 0.9, (("R", 0.4),))),
    "l9": (("B", {"hi": "बस", "kn": "ಬರೀ"}, 0.2, (("t0", 0.4),)),
           ("G", {"hi": "देवता", "kn": "ದೇವತೆಗಳು"}, 0.58, (("B", 0.8),)),
           ("P", {"hi": "रक्षा", "kn": "ಕಾಪಾಡಲಿ"}, 0.85, (("G", 0.5),))),
    "l10": (("R", {"hi": "रेखा", "kn": "ರೇಖೆ"}, 0.5, (("t0", 0.4),)),
            ("Q", {"hi": "कहा", "kn": "ಎಲ್ಲಿಂದ"}, 0.85, (("R", 0.4),))),
    "l11": (("C", {"hi": "सोलह", "kn": "ಹದಿನಾರ"}, 0.3, (("t0", 0.9),)),
            ("T", {"hi": "तुलसीदास", "kn": "ತುಳಸೀ"}, 0.55, (("C", 0.8),)),
            ("M", {"hi": "रामचरितमानस", "kn": "ರಾಮಚರಿತಮಾನಸ"}, 0.8, (("T", 0.6),))),
    "l12": (("S", {"hi": "हरण", "kn": "ಸೀತಾಪ"}, 0.3, (("t0", 0.4),)),
            ("R", {"hi": "रेखा", "kn": "ರೇಖೆ"}, 0.72, (("S", 0.6),))),
    "l13": (("L", {"hi": "लंका", "kn": "ಲಂಕಾ"}, 0.22, (("t0", 0.8),)),
            ("M", {"hi": "मंदोदरी", "kn": "ಮಂಡೋದರಿ"}, 0.38, (("L", 0.9),)),
            ("T", {"hi": "ताना", "kn": "ಚುಚ್ಚಿ"}, 0.5, (("M", 0.6),)),
            ("K", {"hi": "लक्ष्मण", "kn": "ಲಕ್ಷ್ಮಣ"}, 0.7, (("T", 0.6),)),
            ("X", {"hi": "छोटी", "kn": "ಚಿಕ್ಕ"}, 0.8, (("K", 0.45), ("T", 1.0))),
            ("P", {"hi": "पार", "kn": "ದಾಟ"}, 0.9, (("X", 0.6),))),
    "l14": (("O", {"hi": "एक", "kn": "ಒಂದೇ"}, 0.6, (("t0", 0.5),)),),
    "l15": (("V", {"hi": "वाल्मीकि", "kn": "ವಾಲ್ಮೀಕಿ"}, 0.42, (("t0", 0.9),)),
            ("R", {"hi": "रेखा", "kn": "ರೇಖೆ"}, 0.62, (("V", 0.7),)),
            ("C", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.88, (("R", 0.6),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_lr_cues", None)
    if cache is None:
        cache = {}
        tl._lr_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, words, frac, cons in CUES[bid]:
            v = cue(tl, bid, words, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


# ------------------------------------------------------------------ puppets


LK_BOW = {"lakshmana_armB_lo": in_hand("bow", 160, 0.0, 0.62)}
HEART = dict(front=(-0.3, -2.45), backa=(0.12, -0.25))          # a hand at the heart (afraid, hurt)


def lakshmana(cr, t, x, s, **kw):
    kw.setdefault("extra", LK_BOW)
    return fig(cr, L.LAKSHMANA, "lakshmana", t, x, s, **kw)


def lady(cr, rig, key, t, x, s, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(), flip=False, alpha=1.0,
         blur=0.0, rods=True, rot=0.0, feet=FEET, ph=0.0, y=None):
    """A woman() puppet with her feet on `feet`."""
    ang = woman_angles(key, t, front, backa, head, hits, ph)
    hy = feet - 470 * s if y is None else y
    return puppet(cr, rig, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, rods=rods)


def sita(cr, t, x, s, **kw):
    return lady(cr, L.SITA, "sita", t, x, s, **kw)


def mandodari(cr, t, x, s, **kw):
    return lady(cr, L.MANDODARI, "mandodari", t, x, s, **kw)


def walk_at(cr, t, fn, t0, t1, x0, x1, s, feet=FEET, t_in=None, step=0.42, **kw):
    """scenes_kaikeyi.walk on any ground line: a man() puppet walking in jerky rod-puppet steps."""
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    kw.setdefault("hits", [(t1, 1.0)])
    y = feet - 434 * s + bob - (k - 1) * 300 * s
    return fn(cr, t, x, s * k, legs=walk_legs(ph), rot=rock, alpha=a, blur=b, y=y, **kw)


def sparkle(cr, x, y, r, a, col=(1.0, 0.86, 0.45)):
    """A four-pointed glint of light."""
    if a <= 0.01 or r <= 0.5:
        return
    k = 0.16 * r
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    pc.poly(cr, [(x, y - r), (x + k, y - k), (x + r, y), (x + k, y + k), (x, y + r), (x - k, y + k), (x - r, y),
                 (x - k, y - k)])
    cr.set_source_rgba(*col, clamp(a))
    cr.fill()
    cr.restore()


def deer_hops(t, t0, t1, x0, x1, hop=0.4, height=120.0):
    """The deer prancing from x0 to x1 in leaps: (x, lift, front legs, hind legs, pitch); standing still outside."""
    if t <= t0 or t1 <= t0:
        return x0, 0.0, 0.0, 0.0, 0.0
    if t >= t1:
        return x1, 0.0, 0.0, 0.0, 0.0
    n = max(1, round((t1 - t0) / hop))
    st = (t1 - t0) / n
    k = int((t - t0) / st)
    f = (t - t0 - k * st) / st
    s_ = math.sin(math.pi * f)
    return x0 + (x1 - x0) * (k + f) / n, height * 4 * f * (1 - f), -0.75 * s_, 0.85 * s_, -0.2 * math.cos(math.pi * f)


def deer(cr, t, x, feet, s, flip=False, lift=0.0, fl=0.0, hl=0.0, pitch=0.0, alpha=1.0, blur=0.0, rods=True,
         shimmer=1.0):
    """The golden deer (feet on `feet`), shimmering: a warm glow and glints around it."""
    sg = -1 if flip else 1
    y = feet - L.DEER_FEET * s - lift
    if shimmer > 0:
        glow(cr, x + sg * 50 * s, y - 120 * s, 340 * s, 0.5 * shimmer * alpha * (0.8 + 0.2 * math.sin(t * 5)))
    ang = {"deer_legF": fl + 0.04 * math.sin(t * 3), "deer_legBf": 0.8 * fl + 0.06, "deer_legH": hl,
           "deer_legBh": 0.8 * hl - 0.06}
    pts = puppet(cr, L.DEER_RIG, x, y, s, sg * pitch + bob_rot(t, 3.0, 0.02), flip, ang, alpha, blur, rods=rods)
    if shimmer > 0:
        for i in range(7):
            u = (t * 0.9 + i * 0.143) % 1.0
            gx = x + sg * (-230 + 80 * i) * s + 20 * math.sin(t * 2 + i)
            gy = y - (60 + 90 * (i % 3)) * s - 120 * s * u
            sparkle(cr, gx, gy, (18 + 10 * (i % 2)) * s / 0.5 * math.sin(math.pi * u), 0.9 * shimmer * alpha)
    return pts


# ------------------------------------------------------------------ the line, the outline, the X


def rekha_pts(cx=540.0, y=1180.0, half=450.0, sag=110.0, n=64):
    """A line on the ground seen from a little above: lower (nearer) in the middle."""
    return [(cx + half * u, y + sag * (1 - u * u)) for u in (-1 + 2 * i / n for i in range(n + 1))]


def partial(pts, p):
    """The first fraction p of a polyline."""
    if p >= 1:
        return list(pts)
    lens = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total, acc, out = sum(lens) * clamp(p), 0.0, [pts[0]]
    for (a, b), ln in zip(zip(pts, pts[1:]), lens):
        if acc + ln >= total:
            f = (total - acc) / ln if ln else 0.0
            out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
            return out
        out.append(b)
        acc += ln
    return out


def _poly_path(cr, pts):
    cr.new_path()
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)


def rekha(cr, t, pts, p=1.0, alpha=1.0, w=1.0, fire=0.0, embers=0.0):
    """The glowing golden line (for the dark earth): a soft halo, a bright core, flames running along it, embers."""
    if p <= 0 or alpha <= 0.01:
        return
    q = partial(pts, p)
    if len(q) < 2:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_operator(cairo.OPERATOR_ADD)
    for lw, a, col in ((84, 0.10, (1.0, 0.55, 0.12)), (42, 0.22, (1.0, 0.66, 0.20)), (18, 0.50, (1.0, 0.80, 0.35))):
        _poly_path(cr, q)
        cr.set_source_rgba(*col, a * alpha)
        cr.set_line_width(lw * w)
        cr.stroke()
    if fire > 0:                                        # soft tongues of flame, each flickering on its own
        for i in range(1, len(q) - 1, 3):
            x, y = q[i]
            f = abs(math.sin(t * 5.1 + i * 2.9)) * (0.55 + 0.45 * abs(math.sin(t * 3.3 + i * 1.3)))
            h = (10 + 44 * f) * fire * w
            wd = (11 + 5 * f) * w
            tip = 0.6 * wd * math.sin(t * 9 + i)
            for sc, col, a in ((1.0, (1.0, 0.50, 0.10), 0.35), (0.6, (1.0, 0.78, 0.30), 0.45)):
                cr.new_path()
                cr.move_to(x - wd * sc, y)
                cr.curve_to(x - wd * sc, y - h * sc * 0.45, x - 2, y - h * sc * 0.75, x + tip * sc, y - h * sc)
                cr.curve_to(x + 2, y - h * sc * 0.75, x + wd * sc, y - h * sc * 0.45, x + wd * sc, y)
                cr.close_path()
                cr.set_source_rgba(*col, a * alpha * fire)
                cr.fill()
    cr.set_operator(cairo.OPERATOR_OVER)
    _poly_path(cr, q)
    cr.set_source_rgba(1.0, 0.94, 0.66, alpha)
    cr.set_line_width(7 * w)
    cr.stroke()
    cr.restore()
    if p < 1:
        tx, ty = q[-1]
        glow(cr, tx, ty, 120 * w, 0.9 * alpha)
        sparkle(cr, tx, ty, 40 * w, alpha)
    if embers > 0:
        for i in range(14):
            u = (t * 0.45 + i * 0.071) % 1.0
            j = int(len(q) * ((i * 0.618) % 1.0))
            x, y = q[min(j, len(q) - 1)]
            sparkle(cr, x + 14 * math.sin(t * 2 + i), y - 30 - 200 * u, 12 * w * math.sin(math.pi * u),
                    embers * alpha)


def outline(cr, t, pts, p, alpha=1.0):
    """The empty dotted outline where people imagine the line (nothing is drawn there)."""
    dotted(cr, pts, p, 34, 9.5, DOT_C, alpha * (0.8 + 0.2 * math.sin(t * 4)))


def big_x(cr, x, y, w, h, p, alpha=1.0, rot=0.0, lw=None):
    """A big red brush X (w x h) with a pale edge, so it reads on the dark earth as well as on the cloth."""
    if p <= 0:
        return
    lw = lw or 0.1 * min(w, 1.4 * h)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for k, ((ax, ay), (bx, by)) in enumerate((((-1, -1), (1, 1)), ((1, -1), (-1, 1)))):
        q = clamp(p * 2 - k)
        if q <= 0:
            continue
        ex, ey = ax + (bx - ax) * q, ay + (by - ay) * q
        for wd, col, a in ((1.4, LIGHT, 0.85), (1.0, RED, 0.95)):
            cr.move_to(ax * w / 2, ay * h / 2)
            cr.line_to(ex * w / 2, ey * h / 2)
            cr.set_source_rgba(*col, a * alpha)
            cr.set_line_width(lw * wd)
            cr.stroke()
    cr.restore()


def big_q(cr, t, t_in, x, y, size, alpha=1.0):
    """A big red question mark swinging in on its rod."""
    q = back(clamp((t - t_in) / 0.35), 1.6)
    if q <= 0:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(0.12 * math.sin(t * 2.6) + 0.4 * (1 - q))
    cr.scale(q, q)
    draw_text(cr, "?", 0, 0, size, RED, clamp(q) * alpha, anchor="cm")
    cr.restore()
    pc.rod(cr, x + 10, y + size * 0.42 * q, x + 60, H + 60, alpha=0.5 * clamp(q) * alpha)


# ------------------------------------------------------------------ writing and books


def scribble(cr, x0, y, w, size, seed, col=INK, alpha=1.0, p=1.0):
    """A line of hand-written, Devanagari-like script: words hanging from a head-stroke, each with a few strokes
    below it; p = how much of the line is written."""
    if alpha <= 0.01 or p <= 0:
        return
    rng = random.Random(seed)
    words, x = [], x0
    while x < x0 + w - size:
        ww = min(rng.uniform(1.6, 3.4) * size, x0 + w - x)
        n = max(2, int(ww / (0.55 * size)))
        words.append((x, ww, [rng.randrange(4) for _ in range(n)]))
        x += ww + 0.45 * size
    xend = x0 + w * p
    cr.save()
    cr.set_source_rgba(*col, alpha)
    cr.set_line_width(max(2.0, size * 0.11))
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for x, ww, kinds in words:
        if x >= xend:
            break
        e = min(x + ww, xend)
        cr.move_to(x, y)
        cr.line_to(e, y)
        cr.stroke()
        for i, kind in enumerate(kinds):
            gx = x + (i + 0.5) * ww / len(kinds)
            if gx > e:
                break
            s = size
            if kind == 0:
                cr.move_to(gx + 0.18 * s, y)
                cr.line_to(gx + 0.18 * s, y + 0.9 * s)
            elif kind == 1:
                cr.move_to(gx + 0.2 * s, y)
                cr.line_to(gx + 0.2 * s, y + 0.9 * s)
                cr.new_sub_path()
                cr.arc(gx - 0.08 * s, y + 0.5 * s, 0.2 * s, 0, 2 * math.pi)
            elif kind == 2:
                cr.move_to(gx - 0.22 * s, y)
                cr.curve_to(gx - 0.36 * s, y + 0.5 * s, gx + 0.22 * s, y + 0.6 * s, gx + 0.1 * s, y + 0.92 * s)
            else:
                cr.move_to(gx - 0.2 * s, y + 0.25 * s)
                cr.curve_to(gx + 0.3 * s, y + 0.15 * s, gx + 0.3 * s, y + 0.75 * s, gx - 0.15 * s, y + 0.7 * s)
                cr.move_to(gx + 0.24 * s, y)
                cr.line_to(gx + 0.24 * s, y + 0.9 * s)
            cr.stroke()
    cr.restore()


BOOK_GAP = 150.0                     # leaf spacing in an opened manuscript (design units)


def book(cr, t, x, y, s, leaves, t_in=None, t_open=None, alpha=1.0, ring=None, rods=True, blank=1, quill=False):
    """A palm-leaf manuscript (two wooden boards, leaves between, top leaf at (x, y)): rises in at t_in, opens at
    t_open (the top board lifts and flips away, the leaves fan down one under another). leaves = [(t_show, lines,
    write)] per text leaf, lines = [(text or [(text, colour)], size, font)] in leaf units; write = seconds the text
    takes to be written (a quill follows it) or 0. ring = (leaf, line, segment, t) rings that segment in red.
    Returns the leaf centres on screen."""
    a, b, k, yy = alpha, 0.0, 1.0, y
    if t_in is not None:
        if t < t_in:
            return []
        b, k, a0 = depth(t, t_in, 0.5)
        yy = y + 460 * (1 - ease((t - t_in) / 0.5))
        a *= a0
    q = 0.0 if t_open is None else ease((t - t_open) / 0.55)
    n = len(leaves) + blank
    r = sway(t, 0.008, 0.35, x * 0.01)
    sk = s * k
    bot = 52 + (BOOK_GAP * (n - 1) + 96 - 52) * q
    cr.save()
    cr.translate(x, yy)
    cr.rotate(r)
    cr.scale(sk, sk)
    quill_at = None
    for kk in reversed(range(n)):
        ly = (6 + 9 * kk) * (1 - q) + BOOK_GAP * kk * q
        cr.save()
        cr.translate(0, ly)
        pc.paint_part(cr, "lr_pleaf", a, b)
        ta = a * clamp((q - 0.45) / 0.35)
        if kk < len(leaves) and ta > 0:
            t_show, lines, write = leaves[kk]
            if t_show is not None:
                ta *= prog(t, t_show, 0.3) if not write else float(t > t_show)
            if ta > 0:
                if write:
                    wp = clamp((t - t_show) / write)
                    cr.save()
                    cr.rectangle(-440, -70, 880 * wp, 140)
                    cr.clip()
                hs = [sz * 1.12 for _, sz, _ in lines]
                y0 = -sum(hs) / 2
                for i, ((txt, sz, font), hh) in enumerate(zip(lines, hs)):
                    cy = y0 + hh / 2
                    segs = [(txt, INK)] if isinstance(txt, str) else txt
                    full = sum(text_size(sg, sz, font)[0] for sg, _ in segs) + sz * 0.4 * (len(segs) - 1)
                    sz2 = min(sz, int(sz * 740 / max(1, full)))
                    boxes = segs_line(cr, segs, 0, cy, sz2, font, ta, 3 if font == MONO_FONT else 0)
                    if ring and ring[0] == kk and ring[1] == i and t > ring[3]:
                        bx, bw = boxes[ring[2]]
                        red_ring(cr, bx + bw / 2, cy, bw / 2 + 30, sz2 * 0.72, prog(t, ring[3], 0.4), 9 / sk, a)
                    y0 += hh
                if write:
                    cr.restore()
                    if wp < 1:
                        quill_at = (-440 + 880 * wp, ly + 20)
        elif kk >= len(leaves) and ta > 0:
            scribble(cr, -360, -34, 720, 24, 50 + 7 * kk, INK, 0.55 * ta)
        cr.restore()
    cr.save()                                           # the bottom board, in front of the last leaf's lower edge
    cr.translate(0, bot)
    pc.paint_part(cr, "lr_board", a, b)
    cr.restore()
    if q < 1:                                           # the top board lifts and flips away
        cr.save()
        cr.translate(0, -170 * q)
        cr.scale(1, max(0.03, abs(1 - 2 * q)))
        pc.paint_part(cr, "lr_board", a * (1 - q) ** 0.6, b)
        cr.restore()
    if quill and quill_at is not None:
        prop(cr, "kk_quill", quill_at[0], quill_at[1] + 10 * math.sin(t * 25), 1.0, rot=0.1 * math.sin(t * 22),
             alpha=a)
    cr.restore()
    if rods:
        for sx in (-1, 1):
            pc.rod(cr, x + sx * 380 * sk, yy + bot * sk, x + sx * 300, H + 60, alpha=0.5 * a)
    c, si = math.cos(r), math.sin(r)
    return [(x - si * BOOK_GAP * kk * q * sk, yy + c * BOOK_GAP * kk * q * sk) for kk in range(n)]


def quote_note(cr, t, t_in, x, y, s, lines, alpha=1.0):
    """A torn parchment note (rv_note) with lines [(text, size, colour, font, t_show)] in note units."""
    p = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(p) * alpha
    if a <= 0.01:
        return
    yy = y + 70 * (1 - p)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(-0.02 + sway(t, 0.006, 0.4))
    cr.scale(s, s)
    pc.paint_part(cr, "rv_note", a)
    for txt, sz, col, font, dy, ts in lines:
        q = prog(t, ts, 0.3) * a
        if q > 0:
            sz2 = min(sz, int(sz * 680 / max(1, text_size(txt, sz, font)[0])))
            draw_text(cr, txt, 0, dy + 12 * (1 - q), sz2, col, q, font, "cm", 4 if font == MONO_FONT else 0)
    cr.restore()


def jag_text(cr, t, text, x, y, size, t_in, color=CRY_C, alpha=1.0):
    """A cry in jagged, shaking letters: each letter pops on in turn, tilted, on a zig-zag baseline."""
    if t < t_in:
        return
    ws = [text_size(ch, size)[0] if ch != " " else size * 0.3 for ch in text]
    gap = size * 0.07
    xx = x - (sum(ws) + gap * (len(text) - 1)) / 2
    sh = 0.25 + 0.75 * math.exp(-2.2 * (t - t_in))
    edge = max(3, int(size * 0.045))
    for i, (ch, w) in enumerate(zip(text, ws)):
        q = back(clamp((t - t_in - 0.035 * i) / 0.18), 2.0)
        if ch != " " and q > 0:
            dx = 7 * sh * math.sin(t * 37 + i * 2.3)
            dy = 10 * sh * math.sin(t * 29 + i * 1.9) + (12 if i % 2 else -12)
            rot = (0.15 if i % 2 else -0.12) + 0.07 * sh * math.sin(t * 23 + i)
            cr.save()
            cr.translate(xx + w / 2 + dx, y + dy)
            cr.rotate(rot)
            cr.scale(q, q)
            for ox, oy in ((-edge, 0), (edge, 0), (0, -edge), (0, edge), (-edge, -edge), (edge, edge),
                           (edge, -edge), (-edge, edge)):           # a pale edge: readable on dark leaves
                draw_text(cr, ch, ox, oy, size, LIGHT, 0.9 * alpha * clamp(q), anchor="cm")
            draw_text(cr, ch, 0, 0, size, color, alpha * clamp(q), anchor="cm")
            cr.restore()
        xx += w + gap


# ------------------------------------------------------------------ sets


def forest(cr, t, feet=FEET, hut_x=860.0, hut_s=0.72, trees=((40, 0.6, 6, 0.75, True), (1050, 0.62, 10, 0.6, False)),
           hut_a=1.0, hut_b=0.0, slab=False, wind=0.0):
    """The forest at Panchavati: trees (x, scale, blur, alpha, flip), the leaf hut, and the ground (a thin strip, or
    the big earth slab for the ground shots)."""
    for i, (x, s, b, a, fl) in enumerate(trees):
        prop(cr, "tree", x, feet + 10, s, rot=sway(t, 0.006 + 0.03 * wind, 0.3 + 0.5 * wind, i), alpha=a, blur=b,
             flip=fl)
    if hut_x is not None:
        prop(cr, "lr_hut", hut_x, feet + 8, hut_s, alpha=hut_a, blur=hut_b)
    if slab:
        prop(cr, "lr_earth", 540, feet, 1.0)
    else:
        ground(cr, y=feet + 6)


# ------------------------------------------------------------------ l1  hook


HOOK_EARTH = 920
HOOK_LINE = rekha_pts(540, 1100, 450, 110)


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "l1")
    tD, tL, tV, tN = c["D"], c["L"], c["V"], c["N"]
    prop(cr, "lr_earth", 540, HOOK_EARTH, 1.0)
    out = prog(t, tN, 0.7)
    flick = 0.8 + 0.2 * math.sin(t * 31) * math.sin(t * 13)
    p = 0.35 + 0.65 * ease(t / 0.8)
    rekha(cr, t, HOOK_LINE, p, 1.0 - 0.72 * out * flick, 1.25, prog(t, tL, 0.5) * (1 - out),
          prog(t, 0.8, 0.5) * (1 - out))
    sh = 12 * math.exp(-8 * max(0, t - tV)) * math.sin(55 * (t - tV)) if t > tV else 0.0

    def ui(cr):
        head2(cr, t, "LAKSHMAN REKHA?", -1.0, "NOT IN VALMIKI", 0.4, big_size=190, ghost=-1.0, under=tV + 0.25)
        tag(cr, t, tD, "WE QUOTE IT EVERY DAY", 540, 730, 40, t_out=tV - 0.1)
        big_x(cr, 540 + sh, 1170, 640, 440, prog(t, tV, 0.32), rot=-0.05, lw=56)
    return dict(ui=ui, flash=0.45 * math.exp(-5 * max(0, t - tV)) * (t > tV))


# ------------------------------------------------------------------ l2  read it yourself


def s_source(cr, t, tl, t0, t1):
    c = cues(tl, "l2")
    tX, tV, tA, tP = c["X"], c["V"], c["A"], c["P"]
    leaves = [(None, [("VALMIKI RAMAYANA", 86, HEAD_FONT)], 0),
              (tA, [([("ARANYA KANDA", INK), ("3.45", RED)], 74, HEAD_FONT)], 0)]
    book(cr, t, 540, 880, 0.92, leaves, t_in=t0 + 0.05, t_open=tV, ring=(1, 0, 1, tA + 0.3))

    def ui(cr):
        if t < tP:
            struck = t > tX + 0.25
            box = head2(cr, t, "THIS IS NOT A", t0, "RUMOUR", t0 + 0.42, big_size=200,
                        big_color=FADE if struck else INK)
            if box and t > tX:
                bx, by, bw, bh = box
                big_x(cr, W / 2, by + bh / 2, bw + 50, bh * 0.95, prog(t, tX, 0.3), lw=24)
        else:
            head2(cr, t, "DON'T BELIEVE ME?", tP, "READ IT YOURSELF", tP + 0.06, big_size=170, under=tP + 0.45)
    return dict(ui=ui, flash=0.25 * math.exp(-4 * max(0, t - tV)) * (t > tV))


# ------------------------------------------------------------------ l3  the golden deer


def s_deer(cr, t, tl, t0, t1):
    c = cues(tl, "l3")
    tG, tD, tR, tC = c["G"], c["D"], c["R"], c["C"]
    forest(cr, t, hut_x=930, hut_s=0.7, trees=((60, 0.62, 5, 0.8, True), (1060, 0.6, 10, 0.55, False)))
    # the deer: prances in, stops and looks (shimmering), then leaps away into the trees
    t_stop = min(t0 + 1.3, tD - 0.05)
    t_go = tR + 0.15
    if t < t_go:
        x, lift, fl, hl, pitch = deer_hops(t, t0, t_stop, -90, 190, 0.36, 120)
        deer(cr, t, x, FEET, 0.6, lift=lift, fl=fl, hl=hl, pitch=pitch, shimmer=0.7 + 0.3 * prog(t, tG, 0.4))
    else:
        x, lift, fl, hl, pitch = deer_hops(t, t_go, t_go + 0.9, 190, -360, 0.3, 140)
        deer(cr, t, x, FEET, 0.6, flip=True, lift=lift, fl=fl, hl=hl, pitch=pitch)
    ground(cr)
    # Sita points at the deer; Rama, behind her, turns to it and goes after it into the trees
    point = keyed(t, [(t0, 0.0), (tD - 0.1, 1.0)], 0.3, 1.4)
    sita(cr, t, 480, 0.74, flip=True, front=(-0.2 - 1.1 * point, -0.4 + 0.3 * point), hits=[(tD, 0.6)], ph=1.4)
    if t < tR:
        rama(cr, t, 750, 0.74, flip=True, front=(-0.4, -0.5), head=0.04, hits=[(tD, 0.5)], ph=0.5)
    else:
        walk_at(cr, t, rama, tR + 0.1, max(tC + 0.8, tR + 1.5), 750, -230, 0.74, flip=True, ph=0.5, step=0.38)

    def ui(cr):
        if t < tR:
            head2(cr, t, "SITA SAW A", t0 + 0.05, "GOLDEN DEER", tG, big_size=200)
        else:
            head2(cr, t, "RAMA WENT TO", tR, "CATCH IT", tR + 0.06, big_size=210)
    return dict(ui=ui, flash=0.25 * math.exp(-4 * max(0, t - tG)) * (t > tG))


# ------------------------------------------------------------------ l4  the cry


def s_cry(cr, t, tl, t0, t1):
    c = cues(tl, "l4")
    tJ, tR, tC = c["J"], c["R"], c["C"]
    sh = 10 * math.exp(-6 * max(0, t - tC)) * math.sin(50 * (t - tC)) if t > tC else 0.0
    cr.translate(sh, 0.5 * sh)
    sun = prog(t, t0, 1.6)
    prop(cr, "sun", 900, 640 + 380 * sun, 0.36, rot=t * 0.3, alpha=0.8 * (1 - sun))
    wind = prog(t, tJ, 0.6)
    forest(cr, t, hut_x=900, hut_s=0.66, trees=((380, 0.58, 6, 0.8, False), (110, 0.74, 0, 0.95, True)), wind=wind)
    start = keyed(t, [(t0, 0.0), (tC + 0.05, 1.0)], 0.25, 1.6)
    lakshmana(cr, t, 600, 0.66, flip=True, front=(-0.3 - 0.6 * start, -0.5), head=-0.1 * start, hits=[(tC, 0.9)],
              ph=2.0)
    sita(cr, t, 800, 0.66, flip=True, front=(-0.3 - 0.1 * start, -0.6 - 1.8 * start), head=-0.08 * start,
         hits=[(tC, 0.8)], ph=1.4)
    if t > tC:
        sound_rings(cr, 150, 980, t, tC, 5, 0.28, 620, alpha=0.9)

    def ui(cr):
        if t < tR:
            head2(cr, t, "A LITTLE LATER, FROM THE", t0 + 0.05, "FOREST", tJ, big_size=210)
        else:
            head2(cr, t, "A CRY IN", tR, "RAMA'S VOICE", tR + 0.06, big_size=200)
        jag_text(cr, t, "HA SITA!", 470, 680, 140, tC)
        jag_text(cr, t, "HA LAKSHMANA!", 520, 850, 120, tC + 0.3)
    return dict(ui=ui, night=0.22 + 0.16 * prog(t, t0, 1.0), flash=0.4 * math.exp(-6 * max(0, t - tC)) * (t > tC))


# ------------------------------------------------------------------ l5  Sita afraid: go, save your brother


def s_fear(cr, t, tl, t0, t1):
    c = cues(tl, "l5")
    tF, tL, tG, tB = c["F"], c["L"], c["G"], c["B"]
    forest(cr, t)
    sound_rings(cr, -60, 940, t, t0 - 0.9, 4, 0.45, 420, alpha=0.35)             # the cry still echoing
    lakshmana(cr, t, 330, 0.76, front=(-0.35, -0.5), head=0.06 * prog(t, tG, 0.4), hits=[(tL, 0.4)], ph=2.0)
    fear = prog(t, tF, 0.3)
    jit = 0.012 * fear * math.sin(t * 34) * (1 - prog(t, tG, 0.4))
    if t < tL:
        sita(cr, t, 760, 0.76, head=0.08 * fear, rot=jit, hits=[(tF, 0.6)], ph=1.4, **HEART)
    else:
        go = keyed(t, [(tL, 0.0), (tG - 0.05, 1.0)], 0.28, 1.5)
        sita(cr, t, 760, 0.76, flip=True, front=(-1.15 - 0.75 * go, -0.6 + 0.45 * go), head=-0.04 * go, rot=jit,
             hits=[(tL, 0.6), (tB, 1.0)], ph=1.4)
    if t > tB:                                          # where to go: a dotted path into the forest
        pts = [(300 - 340 * u, 1150 - 120 * math.sin(math.pi * u)) for u in (i / 30 for i in range(31))]
        dotted(cr, pts, prog(t, tB, 0.5), 26, 6.5)

    def ui(cr):
        if t < tG:
            head2(cr, t, "SITA WAS", t0 + 0.05, "AFRAID", tF, big_size=220)
        else:
            head2(cr, t, "SITA, TO LAKSHMANA: GO, SAVE", tG, "YOUR BROTHER", tG + 0.06, big_size=200, under=tB)
    return dict(ui=ui, night=0.12 * (1 - prog(t, t0, 0.8)), flash=0.25 * math.exp(-4 * max(0, t - tG)) * (t > tG))


# ------------------------------------------------------------------ l6  not Rama's voice


EV_16 = [("ARANYA KANDA", 34, MONO_FONT), ("3.45.16", 54, HEAD_FONT)]
EV_33 = [("ARANYA KANDA", 34, MONO_FONT), ("3.45.33-34", 54, HEAD_FONT)]
EV_D35 = [("LANKA KAND", 34, MONO_FONT), ("DOHA 35", 54, HEAD_FONT)]


def s_trick(cr, t, tl, t0, t1):
    c = cues(tl, "l6")
    tN, tD = c["N"], c["D"]
    forest(cr, t)
    calm = keyed(t, [(t0, 0.0), (t0 + 0.25, 1.0), (tD + 0.6, 0.5)], 0.3, 1.4)
    env = clamp((t - t0 - 0.3) / 0.2) * (1 - clamp((t - tN - 0.7) / 0.3))
    shake = 0.14 * env * math.sin(2 * math.pi * 2.4 * (t - t0 - 0.3))
    lakshmana(cr, t, 330, 0.76, front=(-0.35 - 1.0 * calm, -0.5 - 0.5 * calm), head=shake, hits=[(tN, 0.5)], ph=2.0)
    sita(cr, t, 760, 0.76, flip=True, head=0.05, ph=1.4, **HEART)

    def ui(cr):
        head2(cr, t, "LAKSHMANA SAID:", t0 + 0.05, "NOT RAMA'S VOICE", tN, big_size=190, ghost=t0 + 0.3)
        card(cr, t, tD, 540, 690, 0.74, [("A DEMON'S", 78, INK, -42), ("TRICK", 102, RED, 44)])
        leaf_tag(cr, t, tD + 0.4, 790, 880, 0.8, EV_16, rot=0.04)
    return dict(ui=ui, flash=0.25 * math.exp(-4 * max(0, t - tD)) * (t > tD))


# ------------------------------------------------------------------ l7  harsh words (only as shapes)


SHARD_FLY = 0.55


def shard_times(tl):
    """When each dark shape leaves Sita (it reaches Lakshmana SHARD_FLY later): a steady stream from "in anger",
    a burst of three on "very"."""
    c = cues(tl, "l7")
    end = tl["l7"].end
    out = [c["A"] + 0.32 * i for i in range(14) if c["A"] + 0.32 * i < end - 0.35]
    out += [c["H"] + 0.12 * i for i in range(3)]
    return sorted(out)


def s_harsh(cr, t, tl, t0, t1):
    c = cues(tl, "l7")
    tN, tA, tH = c["N"], c["A"], c["H"]
    forest(cr, t)
    shots_t = shard_times(tl)
    hits = [(ts + SHARD_FLY, 0.5) for ts in shots_t]
    hurt = prog(t, tA + 0.5, 0.6)
    back_ = keyed(t, [(t0, 0.0), (tH + 0.55, 1.0)], 0.3, 1.3)
    lp = lakshmana(cr, t, 330 - 40 * back_, 0.76, front=(-0.25, -0.3), head=0.2 * hurt, rot=-0.03 * hurt,
                   hits=hits, ph=2.0)
    speak = keyed(t, [(t0, 0.0), (tN - 0.05, 0.4), (tA, 1.0)], 0.3, 1.4)
    no = 0.08 * math.sin(2 * math.pi * 2.2 * (t - tN)) * clamp((t - tN) / 0.15) * (1 - clamp((t - tN - 0.6) / 0.2))
    sp = sita(cr, t, 760, 0.76, flip=True, front=(-0.4 - 1.0 * speak, -0.5 - 0.5 * speak), head=no - 0.04 * speak,
              hits=[(tA, 0.6), (tH, 0.9)], ph=1.4)
    hx, hy = sp["head"]
    cx, cy = lp["chest"]
    for i, ts in enumerate(shots_t):                    # the dark shapes fly from her to him
        u = (t - ts) / SHARD_FLY
        if 0 < u < 1.3:
            e = ease(min(u, 1.0))
            x = hx - 40 + (cx + 40 - hx + 40) * e
            y = hy + 10 + (cy + 10 - hy - 10) * e - 60 * math.sin(math.pi * min(u, 1.0)) * (1 - 0.3 * (i % 2))
            a = clamp(u * 5) * (1 - clamp((u - 1.0) / 0.3))
            prop(cr, f"lr_shard{i % 3}", x, y, 0.55 + 0.2 * e, rot=3.5 * u + i, alpha=a)

    def ui(cr):
        if t < tH:
            head2(cr, t, "SITA DID NOT", t0 + 0.05, "AGREE", tN, big_size=220)
        else:
            head2(cr, t, "UPSET, SHE SPOKE", tH, "HARSH WORDS", tH + 0.06, big_size=200)
    return dict(ui=ui, night=0.15 * prog(t, tA, 0.6), flash=0.2 * math.exp(-4 * max(0, t - tH)) * (t > tH))


# ------------------------------------------------------------------ l8  no line


HUT_LINE = rekha_pts(700, 1470, 330, 70, 48)


def s_noline(cr, t, tl, t0, t1):
    c = cues(tl, "l8")
    tW, tP, tR, tN = c["W"], c["P"], c["R"], c["N"]
    forest(cr, t, feet=SLAB_FEET, hut_x=860, hut_s=0.66, trees=((60, 0.5, 8, 0.6, True),), slab=True)
    sita(cr, t, 690, 0.66, flip=True, feet=SLAB_FEET, head=0.08, ph=1.4, **HEART)
    if t < tW:
        lakshmana(cr, t, 380, 0.68, front=(-0.2, -0.3), head=0.22, feet=SLAB_FEET, ph=2.0)
    else:
        walk_at(cr, t, lakshmana, tW + 0.1, tW + 1.6, 380, -230, 0.68, feet=SLAB_FEET, flip=True, head=0.22,
                front=(-0.2, -0.3), ph=2.0, step=0.45)
    if t > tR:
        outline(cr, t, HUT_LINE, prog(t, tR, 0.6))

    def ui(cr):
        if t < tP:
            head2(cr, t, "HURT, LAKSHMANA", t0 + 0.05, "LEFT", tW, big_size=230)
        else:
            head2(cr, t, "BUT ON THE GROUND HE DREW", tP, "NO LINE", tN, big_size=240, under=tN + 0.35)
    return dict(ui=ui, flash=0.3 * math.exp(-5 * max(0, t - tN)) * (t > tN))


# ------------------------------------------------------------------ l9  only a blessing


def s_prayer(cr, t, tl, t0, t1):
    c = cues(tl, "l9")
    tB, tG, tP = c["B"], c["G"], c["P"]
    forest(cr, t, hut_x=760, hut_s=0.6, hut_b=3, trees=((70, 0.62, 3, 0.9, True), (1010, 0.66, 2, 0.9, False)))
    lights = prog(t, tG, 0.7)
    for i, (gx, gy) in enumerate(((60, 900), (150, 1040), (990, 860), (1060, 1010), (900, 1000))):
        glow(cr, gx, gy, 170, 0.55 * lights * (0.8 + 0.2 * math.sin(t * 3 + i)))
    for i in range(12):                                 # little lights rising from the leaves
        u = (t * 0.35 + i * 0.083) % 1.0
        gx = (40 + 70 * (i % 4)) if i % 2 else (900 + 50 * (i % 4))
        sparkle(cr, gx + 20 * math.sin(t + i), 1080 - 330 * u, 16 * math.sin(math.pi * u), lights)
    sita(cr, t, 660, 0.6, flip=True, alpha=0.95, blur=2, ph=1.4)
    pray = keyed(t, [(t0, 0.0), (tB, 1.0)], 0.35, 1.3)
    if pray < 0.5:
        lakshmana(cr, t, 330, 0.74, front=(-0.3, -0.4), head=0.1, ph=2.0)
    else:
        lakshmana(cr, t, 330, 0.74, head=0.12, ph=2.0, extra=None, **ANJALI)

    def ui(cr):
        if t < tG:
            head2(cr, t, "LEAVING, HE SAID ONLY THIS", t0 + 0.05, None, 0.0)
        else:
            head2(cr, t, "NO LINE. ONLY", tG, "A BLESSING", tG + 0.06, big_size=210)
        quote_note(cr, t, tB, 560, 730, 0.74,
                   [("LAKSHMANA TO SITA:", 40, INK, MONO_FONT, -160, tB),
                    ("MAY ALL THE FOREST GODS", 80, INK, HEAD_FONT, -50, tB + 0.25),
                    ("PROTECT YOU", 120, RED, HEAD_FONT, 76, tG)])
        leaf_tag(cr, t, tP, 790, 1010, 0.78, EV_33, rot=0.04)
    return dict(ui=ui, flash=0.25 * math.exp(-3 * max(0, t - tG)) * (t > tG))


# ------------------------------------------------------------------ l10  re-hook: so where did it come from?


def s_rehook(cr, t, tl, t0, t1):
    c = cues(tl, "l10")
    tR, tQ = c["R"], c["Q"]
    prop(cr, "lr_earth", 540, HOOK_EARTH, 1.0)
    on = prog(t, tR - 0.1, 0.3)
    f = pc.flicker(t * 1.7)
    rekha(cr, t, HOOK_LINE, 1.0, on * clamp(0.3 + 0.35 * f), 1.25, 0.0, 0.4 * on)

    def ui(cr):
        head2(cr, t, "SO WHERE DID THE LINE", t0 + 0.05, "COME FROM?", t0 + 0.45, big_size=220)
        big_q(cr, t, tQ, 540, 690, 360)
    return dict(ui=ui, night=0.4 + 0.15 * prog(t, t0, 0.5), flash=0.3 * math.exp(-5 * max(0, t - tQ)) * (t > tQ))


# ------------------------------------------------------------------ l11  Tulsidas, the 1500s


def s_tulsi(cr, t, tl, t0, t1):
    c = cues(tl, "l11")
    tC, tT, tM = c["C"], c["T"], c["M"]
    t_book = tT - 0.25
    if t < t_book:
        calendar(cr, t, t0 + 0.05, t_book - 0.1, n=11)
    leaves = [(tT + 0.2, [("TULSIDAS", 96, HEAD_FONT)], 0),
              (tM, [([("RAMCHARITMANAS", INK), ("1500s", RED)], 74, HEAD_FONT)], 0.6)]
    book(cr, t, 540, 820, 0.92, leaves, t_in=t_book, t_open=tT + 0.1, ring=(1, 0, 1, tM + 0.75), quill=True)

    def ui(cr):
        if t < tT:
            head2(cr, t, "MUCH LATER, IN THE", t0 + 0.05, "1500s", tC, big_size=240)
        else:
            head2(cr, t, "TULSIDAS WROTE THE", tT, "RAMCHARITMANAS", tM, big_size=190)
    return dict(ui=ui, flash=0.25 * math.exp(-4 * max(0, t - tC)) * (t > tC))


# ------------------------------------------------------------------ l12  still no line at the abduction


def s_abduct(cr, t, tl, t0, t1):
    c = cues(tl, "l12")
    tS, tR = c["S"], c["R"]
    forest(cr, t, feet=SLAB_FEET, hut_x=860, hut_s=0.66, trees=((60, 0.5, 8, 0.6, True),), slab=True)
    if t > tS - 0.3:                                    # Ravana's shadow comes near: nothing stops it
        u = ease((t - tS + 0.3) / 1.4)
        rs = 0.66
        rv(cr, t, -260 + 560 * u, SLAB_FEET - 434 * rs, rs, bob_rot(t, 1), ang=rv_angles(t, front=(-0.9, -0.6)),
           alpha=0.38 * clamp(u * 3), blur=17, rods=False)
    sita(cr, t, 690, 0.66, flip=True, feet=SLAB_FEET, head=0.04, ph=1.4, front=(-0.3, -0.6))
    if t > tR - 0.1:
        outline(cr, t, HUT_LINE, prog(t, tR - 0.1, 0.5))

    def ui(cr):
        head2(cr, t, "TULSIDAS TOO, AT THE ABDUCTION:", t0 + 0.05, "NO LINE", tR, big_size=240, under=tR + 0.4)
        leaf_tag(cr, t, t0 + 0.25, 790, 690, 0.72, [("RAMCHARITMANAS", 34, MONO_FONT), ("ARANYA KAND", 54, HEAD_FONT)],
                 rot=0.04, rod=False)
    return dict(ui=ui, flash=0.3 * math.exp(-5 * max(0, t - tR)) * (t > tR))


# ------------------------------------------------------------------ l13  Lanka: Mandodari's taunt


CLOUD = (480, 735, 0.8)


def s_lanka(cr, t, tl, t0, t1):
    c = cues(tl, "l13")
    tL, tM, tT, tK, tX, tP = c["L"], c["M"], c["T"], c["K"], c["X"], c["P"]
    b, k, a = depth(t, t0, 0.5)
    prop(cr, "lr_palace", 540, FEET + 10, 0.86 * k, alpha=0.8 * a, blur=3 + b)
    ground(cr)
    droop = prog(t, tP, 0.6)
    rs = 0.6
    rv(cr, t, 830, FEET - 434 * rs, rs, bob_rot(t, 1), flip=True,
       ang=rv_angles(t, front=(-0.5 + 0.3 * droop, -0.7 + 0.3 * droop), backa=(0.3, -0.4), head=0.2 * droop,
                     hits=[(tP, 0.6)]), look=0.25 * droop)
    if t > tM - 0.35:
        bm, km, am = depth(t, tM - 0.35, 0.45)
        talk = keyed(t, [(tM, 0.0), (tT - 0.05, 1.0)], 0.3, 1.4)
        mp = mandodari(cr, t, 290, 0.76 * km, front=(-0.3 - 1.1 * talk, -0.5 - 0.3 * talk), alpha=am, blur=bm,
                       hits=[(tT, 0.7), (tK, 0.5), (tX, 0.5), (tP, 0.8)], ph=0.8)
        if t > tT:
            sound_rings(cr, mp["head"][0] + 60, mp["head"][1] + 10, t, tT, 3, 0.35, 140, alpha=0.7)
    fl = 0.25 * math.exp(-4 * max(0, t - tL)) * (t > tL)

    def ui(cr):
        if t < tM:
            head2(cr, t, "THE LINE COMES LATER, IN", t0 + 0.05, "LANKA KAND", tL, big_size=200)
        else:
            head2(cr, t, "MANDODARI'S", tM, "TAUNT", tT, big_size=240)
        leaf_tag(cr, t, tL + 0.3, 540, 620, 0.85, EV_D35, rot=-0.03, t_out=tK - 0.25)
        q = back(clamp((t - tK + 0.1) / 0.35), 1.5)
        if q > 0:
            cx, cy, cs = CLOUD
            cr.save()
            cr.translate(cx, cy)
            cr.rotate(sway(t, 0.008, 0.4))
            cr.scale(cs * q, cs * q)
            pc.paint_part(cr, "lr_scloud", clamp(q * 2), op=cairo.OPERATOR_OVER)
            a2 = clamp(q * 2)
            draw_text(cr, "YOU COULDN'T EVEN CROSS", 0, -86, 60, INK, a2, anchor="cm")
            p = prog(t, tX + 0.1, 0.6)
            pts = [(-170 + 340 * u, 6 + 10 * math.sin(math.pi * u)) for u in (i / 30 for i in range(31))]
            q2 = partial(pts, p)
            if len(q2) > 1:
                for wd, col in ((22, INK), (12, L.DEER)):
                    _poly_path(cr, q2)
                    cr.set_source_rgba(*col, a2)
                    cr.set_line_width(wd)
                    cr.set_line_cap(cairo.LINE_CAP_ROUND)
                    cr.stroke()
            draw_text(cr, "LAKSHMANA'S SMALL LINE", 0, 92, 60, RED, a2 * prog(t, tX + 0.3, 0.3), anchor="cm")
            if t > tP:
                red_ring(cr, 0, 12, 230, 60, prog(t, tP, 0.4), 10)
            cr.restore()
            if 0 < p < 1:
                sparkle(cr, cx + cs * (-170 + 340 * p), cy + cs * 12, 30, 0.9)
    return dict(ui=ui, flash=fl + 0.25 * math.exp(-4 * max(0, t - tX)) * (t > tX))


# ------------------------------------------------------------------ l14  just one line


LEAF_LINES = 6
HI_LINE = 3


def s_oneline(cr, t, tl, t0, t1):
    tO = cues(tl, "l14")["O"]
    x, y, s = 540, 960, 0.96
    q = back(clamp((t - t0) / 0.35), 1.3)
    yy = y + 120 * (1 - q)
    r = -0.02 + sway(t, 0.008, 0.4)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(r)
    cr.scale(s, s)
    pc.paint_part(cr, "lr_bigleaf", clamp(q * 2))
    hl = prog(t, tO, 0.45)
    for i in range(LEAF_LINES):
        ly = -150 + 60 * i
        if i == HI_LINE:
            if hl > 0:                                  # the one line lights up: a gold band sweeps along it
                cr.save()
                cr.set_operator(cairo.OPERATOR_MULTIPLY)
                cr.rectangle(-390, ly - 26, 780 * hl, 56)
                cr.set_source_rgba(1.0, 0.80, 0.30, 0.9)
                cr.fill()
                cr.restore()
            col = RED if hl > 0.5 else INK
            if HAS_DEVA:
                draw_text(cr, DOHA, 0, ly + 2, 46, col, clamp(q * 2), DEVA_FONT, "cm")
            else:
                scribble(cr, -360, ly - 14, 720, 34, 200 + i, col, clamp(q * 2))
            if t > tO + 0.35:
                red_ring(cr, 0, ly + 2, 420, 46, prog(t, tO + 0.35, 0.45), 10)
        else:
            scribble(cr, -360, ly - 14, 720, 34, 200 + i, INK, 0.8 * clamp(q * 2))
    cr.restore()
    pc.rod(cr, x - 300, yy + 190, 330, H + 60, alpha=0.5)
    pc.rod(cr, x + 300, yy + 190, 760, H + 60, alpha=0.5)

    def ui(cr):
        head2(cr, t, "AND THAT TOO, IN", t0 + 0.05, "JUST ONE LINE", tO, big_size=210, under=tO + 0.4)
        tag(cr, t, tO + 0.5, "LANKA KAND, DOHA 35", 540, 1290, 36)
    return dict(ui=ui, flash=0.3 * math.exp(-4 * max(0, t - tO)) * (t > tO))


# ------------------------------------------------------------------ l15  which do you believe?


END_LINE = rekha_pts(540, 1500, 400, 70, 48)
BOOKS = ((300, "VALMIKI", "NO LINE"), (780, "TULSIDAS", "A LINE"))


def ring_side(t, tV, tR, period=0.9):
    """Which side the red ring is on (0 = Valmiki, 1 = Tulsidas, None = not yet) and when it moved there."""
    if t < tV:
        return None, None
    if t < tR:
        return 0, tV
    n = int((t - tR) / period)
    return (1 if n % 2 == 0 else 0), tR + period * n


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "l15")
    tV, tR = c["V"], c["R"]
    prop(cr, "lr_earth", 540, SLAB_FEET, 1.0)
    side, ts = ring_side(t, tV, tR)
    lit = 0.0 if side is None else (prog(t, ts, 0.3) if side == 1 else 1 - prog(t, ts, 0.3))
    rekha(cr, t, END_LINE, 1.0, lit, 1.0, 0.6 * lit, 0.5 * lit)
    outline(cr, t, END_LINE, 1.0, alpha=1 - lit)
    for i, (bx, name, _) in enumerate(BOOKS):
        book(cr, t, bx, 660, 0.48, [(None, [(name, 128, HEAD_FONT)], 0)], t_in=t0 + 0.05 + 0.15 * i,
             t_open=t0 + 0.3 + 0.15 * i, rods=True)

    def ui(cr):
        head2(cr, t, "SO, WHICH ONE DO YOU", t0 + 0.05, "BELIEVE?", t0 + 0.45, big_size=240)
        for i, (bx, _, lab) in enumerate(BOOKS):
            card(cr, t, t0 + 0.45 + 0.15 * i, bx, 1000, 0.6, [(lab, 150, RED, 4)], rod=False)
        if side is not None:
            red_ring(cr, BOOKS[side][0], 1000, 250, 100, prog(t, ts, 0.35), 10)
    return dict(ui=ui)


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("l1", None, s_hook, {"z": (1.0, 1.04)}),
    ("l2", None, s_source, {"z": (1.0, 1.03)}),
    ("l3", None, s_deer, {}),
    ("l4", None, s_cry, {"z": (1.0, 1.06)}),
    ("l5", None, s_fear, {}),
    ("l6", None, s_trick, {}),
    ("l7", None, s_harsh, {"z": (1.0, 1.04)}),
    ("l8", None, s_noline, {"z": (1.0, 1.04)}),
    ("l9", None, s_prayer, {}),
    ("l10", None, s_rehook, {"z": (1.0, 1.1)}),
    ("l11", None, s_tulsi, {"z": (1.0, 1.03)}),
    ("l12", None, s_abduct, {}),
    ("l13", None, s_lanka, {"z": (1.0, 1.03)}),
    ("l14", None, s_oneline, {"z": (1.02, 1.08)}),
    ("l15", None, s_end, {"z": (1.0, 1.03)}),
]


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
    cr.restore()
    motes(cr, t)
    pc.lamp(cr, t, night=out.get("night", 0.0), flash=out.get("flash", 0.0))
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur): the Kaikeyi / Ravana vocabulary: a whoosh on every cut, damaru on hits, conch on the big
    reveals (the books, Lanka), bell on sacred beats and the end, shimmer on the line, the deer and the forest gods,
    steps for walking, ticks for marks and the rings, scribble for the writing, pops as things land."""
    st = starts(tl, SHOTS)
    ev = [(s, "whoosh", 0.45) for s in st[1:]]
    c = {b: cues(tl, b) for b in CUES}
    # l1
    k = c["l1"]
    ev += [(0.0, "damaru", 0), (0.05, "bell", 0), (0.1, "shimmer", 0), (0.4, "pop", 0), (k["L"], "shimmer", 0),
           (k["D"], "pop", 0), (k["V"] - 0.3, "dip", 0.35), (k["V"], "slam", 0), (k["V"] + 0.02, "hit", 0),
           (k["V"] + 0.25, "tick", 0), (k["N"], "thud", 0)]
    # l2
    k = c["l2"]
    ev += [(k["t0"] + 0.15, "pop", 0), (k["X"], "slam", 0), (k["V"] - 0.25, "whoosh", 0.5), (k["V"], "conch", 0),
           (k["V"] + 0.3, "creak", 0.5), (k["V"] + 0.6, "pop", 0), (k["A"], "pop", 0), (k["A"] + 0.3, "tick", 0),
           (k["P"], "damaru", 0)]
    # l3
    k = c["l3"]
    t_stop = min(k["t0"] + 1.3, k["D"] - 0.05)
    n = max(1, round((t_stop - k["t0"]) / 0.38))
    ev += [(k["t0"] + (t_stop - k["t0"]) * (i + 1) / n, "step", 0) for i in range(n)]
    ev += [(k["G"], "shimmer", 0), (k["D"], "bell", 0), (k["R"], "whoosh", 0.5), (k["R"] + 0.2, "shimmer", 0)]
    ev += [(k["R"] + 0.1 + 0.38 * i, "step", 0) for i in range(4)]
    # l4
    k = c["l4"]
    ev += [(k["t0"], "dip", 0.6), (k["J"], "whoosh", 0.8), (k["C"] - 0.3, "dip", 0.4), (k["C"], "sting", 0),
           (k["C"] + 0.02, "hit", 0), (k["C"] + 0.3, "hit", 0), (k["C"] + 0.4, "heartbeat", 1.4)]
    # l5
    k = c["l5"]
    ev += [(k["F"], "heartbeat", 1.2), (k["L"], "whoosh", 0.35), (k["G"], "damaru", 0), (k["B"], "hit", 0),
           (k["B"] + 0.1, "tick", 0)]
    # l6
    k = c["l6"]
    ev += [(k["t0"] + 0.3, "whoosh", 0.3), (k["t0"] + 0.5, "whoosh", 0.3), (k["N"], "slam", 0),
           (k["D"] - 0.3, "dip", 0.4), (k["D"], "damaru", 0), (k["D"] + 0.05, "thud", 0), (k["D"] + 0.4, "pop", 0)]
    # l7
    k = c["l7"]
    ev += [(k["N"], "thud", 0), (k["A"], "dip", 0.5)]
    ev += [(ts + SHARD_FLY, "thud", 0) for ts in shard_times(tl)]
    ev += [(k["H"], "damaru", 0), (k["H"] + SHARD_FLY, "hit", 0)]
    # l8
    k = c["l8"]
    ev += [(k["W"] + 0.1 + 0.45 * i, "step", 0) for i in range(4)]
    ev += [(k["P"] - 0.2, "dip", 0.5), (k["R"], "tick", 0), (k["R"] + 0.3, "tick", 0), (k["N"], "slam", 0),
           (k["N"] + 0.05, "damaru", 0)]
    # l9
    k = c["l9"]
    ev += [(k["B"], "pop", 0), (k["B"] + 0.05, "bell", 0), (k["G"], "shimmer", 0), (k["G"] + 0.1, "conch", 0),
           (k["P"], "pop", 0), (k["P"] + 0.3, "bell", 0)]
    # l10: re-hook
    k = c["l10"]
    ev += [(k["t0"] - 0.35, "tick", 0), (k["t0"] - 0.3, "dip", 0.5), (k["t0"], "sting", 0),
           (k["t0"] + 0.2, "heartbeat", 1.6), (k["R"], "shimmer", 0), (k["Q"], "hit", 0), (k["Q"] + 0.05, "damaru", 0)]
    # l11
    k = c["l11"]
    t_book = k["T"] - 0.25
    nf = int(max(0, t_book - k["t0"] - 0.2) / 0.16)
    ev += [(k["t0"] + 0.15 + 0.16 * i, "tick", 0) for i in range(min(nf, 11))]
    ev += [(k["C"], "conch", 0), (t_book, "whoosh", 0.5), (t_book + 0.45, "thud", 0), (k["T"] + 0.1, "creak", 0.5),
           (k["T"] + 0.25, "pop", 0), (k["M"], "scribble", 0.6), (k["M"] + 0.75, "tick", 0)]
    # l12
    k = c["l12"]
    ev += [(k["t0"] + 0.25, "pop", 0), (k["S"] - 0.3, "whoosh", 1.0), (k["R"], "tick", 0), (k["R"] + 0.05, "slam", 0)]
    # l13
    k = c["l13"]
    ev += [(k["L"], "conch", 0), (k["L"] + 0.3, "pop", 0), (k["M"] - 0.35, "whoosh", 0.4), (k["T"], "damaru", 0),
           (k["K"] - 0.1, "pop", 0), (k["X"] + 0.1, "shimmer", 0), (k["P"], "hit", 0), (k["P"] + 0.05, "tick", 0)]
    # l14
    k = c["l14"]
    ev += [(k["t0"] + 0.05, "pop", 0), (k["O"], "shimmer", 0), (k["O"] + 0.02, "bell", 0), (k["O"] + 0.35, "tick", 0),
           (k["O"] + 0.5, "pop", 0)]
    # l15
    k = c["l15"]
    ev += [(k["t0"] + 0.05, "pop", 0), (k["t0"] + 0.2, "pop", 0), (k["t0"] + 0.45, "pop", 0), (k["t0"] + 0.6, "pop", 0)]
    t_end = tl.total
    tt = k["R"]
    ev += [(k["V"], "tick", 0)]
    while tt < t_end - 0.3:
        ev.append((tt, "tick", 0))
        tt += 0.9
    ev += [(k["R"], "shimmer", 0), (k["C"], "bell", 0)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in ev]
