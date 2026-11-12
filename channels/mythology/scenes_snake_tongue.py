"""Scenes for videos/snake_tongue.py: "Why is a snake's tongue split?" (Mahabharata, Adi Parva, Astika sub-book
20-34), in Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen,
two-tier headlines and rod-puppet motion as the earlier reels, with the cast from snake_cast. Written so a 5-year-old
can follow it: every line has a shot that shows exactly what is said, in the order it is said, with one big, short
English headline per idea; the twist (the tongue splitting on the sharp grass) gets a slow close-up reveal.

Respect: Garuda, Indra, both mothers and the gods' guards with dignity. No injury is drawn: the guards are dark
silhouettes beaten only by flashes of light (they fall back and fade), the snakes' tongues split like a leather strip
coming apart with a spark (never a wound).

Every frame is a pure function of t. On-screen text is short English, except the two word cards (अमृत, कुश), where the
spoken Hindi word shows in Devanagari (shaped by matplotlib with Nirmala.ttc as in scenes_arjuna; Latin letters without
the font). Cues are words of the Hindi line with a fraction fallback, in one table (CUES) that the scenes and sfx() both
read, with minimum gaps so a fast voice can't bunch the beats together. Shot starts and cues are cached on the timeline
under this module's own names (_sn_shot_starts, _sn_cues). Hindi only (Kannada is routed to scenes_snake_tongue_yk).

Shot list (line: what is on the screen)
  sn1   HOOK, frame 0: one big snake head on the plain cloth, its forked tongue flicking: WHY IS A SNAKE'S TONGUE /
        SPLIT?; on "do" the tongue holds out and its two tips are ringed (TWO TIPS!); on "Mahabharat" THE MAHABHARATA
        SAYS: / AMRIT DID IT! and a glowing pot pops in
  sn2   a palm-leaf book opens: MAHABHARATA, then THE VERY FIRST CHAPTERS (ringed): A STORY FROM THE / MAHABHARATA,
        then RIGHT AT THE / VERY START
  sn3   Garuda lands big, wings beating (tags GARUDA / KING OF BIRDS): THIS IS / GARUDA; he spreads his wings:
        A HUGE AND MIGHTY / BIRD!
  sn3b  his mother sweeps (tag HIS MOTHER) before the snakes' mother with her snakes (tag SNAKES' MOTHER), who points
        at the floor; Garuda watches small: HIS MOTHER WAS A / SERVANT
  sn4   the white horse; the two mothers either side: BECAUSE OF A / BET!; a "?" over the tail (ringed): THE BET: /
        TAIL COLOUR?; their guesses WHITE! / BLACK!
  sn5   close on the tail: three snakes slither up and wrap it: SNEAKY SNAKES / CHEATED!; it turns black: NOW THE TAIL
        LOOKED / BLACK!
  sn5b  his mother, sad, her WHITE! struck out; the snakes' mother laughs, her snakes bob: SO HIS MOTHER / LOST THE BET
  sn6   Garuda asks the raised snakes; his mother small behind him, sweeping (ringed on "chhodne"): GARUDA ASKED /
        THE SNAKES, then TO FREE MY MOTHER, / WHAT DO YOU WANT?
  sn7   the snakes answer; a thought bubble: the glowing pot in heaven's clouds: THE SNAKES SAID: / BRING AMRIT!; card
        अमृत = DRINK OF FOREVER LIFE: DRINK IT, AND YOU / NEVER DIE
  sn8   heaven (the gold gate, clouds): Garuda flies in: GARUDA FLEW UP TO / HEAVEN; he dashes past the guards, flash,
        flash, flash, they fall back and fade: HE BEAT ALL THE / GUARDS
  sn8b  the pot glowing on a lotus; he lifts it high: AND HE TOOK THE / AMRIT POT; he holds it away, a drop in a red
        "no" sign by his beak: BUT HE DRANK / NOT ONE SIP!
  sn9   Indra flashes in with his vajra (tags INDRA / KING OF THE GODS), his hand up: stop; a speech cloud: pot ->
        snake, crossed out: THE KING OF THE GODS, / INDRA, then DON'T GIVE AMRIT / TO SNAKES!
  sn9q  the question card SAVE MOM, / KEEP AMRIT? under a big red "?", Garuda small with the pot: NOW WHAT?
  sn10  Garuda whispers to Indra (SHH!); a plan board: 1 the pot goes down on the grass, 2 Indra lifts it:
        GARUDA HAD A / CLEVER PLAN, I'LL PUT THE POT / DOWN..., THEN YOU TAKE IT BACK, / SECRETLY!
  sn11  the kusha patch; card कुश = SHARP GRASS; the blade tips glint (ringed: SHARP!); he kneels and sets the pot
        down on it: HE PUT THE POT ON / KUSHA GRASS
  sn12  Garuda by the pot to the raised snakes: speech HERE'S AMRIT! then BATHE FIRST!, a river to the right: HERE'S /
        THE AMRIT!, BUT FIRST, / GO BATHE!
  sn12b his mother drops the broom, lifts her head, joy, light: AND MY MOTHER / IS FREE!
  sn13  the snakes slither off happily to the river: THE SNAKES WENT TO / BATHE; Indra flashes in behind the pot, lifts
        it, rises into the clouds: AND INDRA / TOOK IT BACK!
  sn14  the snakes come back dripping: the empty grass, a dotted outline: THE SNAKES CAME BACK... / POT GONE!; drops
        glint on the blades, a thought bubble of drops: MAYBE A FEW DROPS / FELL ON THE GRASS?
  sn15  the snakes lick the sharp blades: THEY LICKED THE / SHARP GRASS
  sn15b the twist, slowly: close-up of one head, its tongue sliding along the saw-edged blade; it splits from the tip to
        the middle with a spark: AND THEIR TONGUES / SPLIT!
  sn16  a row of snakes, every one flicking a forked tongue (ringed): SINCE THEN: / SPLIT FOREVER
  sn16b a puja: the brass plate, the diya, the kalasha, the kusha bundle glowing: AND KUSHA GRASS / BECAME HOLY
  sn16c the hook's picture again (the big head, the forked tongue); the black tail of the bet as a faint memory:
        THEY WON BY / CHEATING..., then AND THE TONGUE / REMEMBERS
  sn17  SO WAS GARUDA / RIGHT?, OR DID HE / CHEAT TOO?; cards GARUDA WAS RIGHT / GARUDA CHEATED TOO, a red ring
        alternating; Garuda small below
"""
import bisect
import math

import cairo

import jayadratha_cast  # noqa: F401  (registers the spear)
import mandhata_cast as M
import puppet_core as pc
import ruru_cast  # noqa: F401  (registers the light clouds)
import shani_cast as SG
import six_cast_a  # noqa: F401  (registers the waves)
import snake_cast as SC
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, back, clamp, draw_text, ease, prog
from puppet_core import H, W, depth, keyed, prop, puppet, sway
from scenes_arjuna import HAS_INDIC, card2, cloud_text, down_arrow, indic_surface
from scenes_garuda_purana import diya
from scenes_hanuman_curse import qmark, trail
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, man_angles, motes, red_ring, woman_angles
from scenes_jayadratha import NIGHT, flash_at, silhouette, tag, tint, title_lift, to_user
from scenes_kaikeyi import card, fig
from scenes_lakshman_rekha import big_x, book, sparkle
from scenes_mandhata import aura, burst, held, lights, local, mix, reach_arm, warm
from scenes_ravana import dotted, head2
from scenes_ruru import _resample, held_grip, plate, sepia, spine_coil
from shots import CUT_LEAD, MIN_SHOT, T

_prop = prop


def prop(cr, name, x, y, s=1.0, *a, **k):
    """puppet_core.prop, but a prop growing in from scale 0 is simply not drawn (cairo can't invert a zero scale)."""
    if abs(s) < 1e-4:
        return
    _prop(cr, name, x, y, s, *a, **k)

MISSES = set()                       # cue words not found in a line (falls back to fractions)
G = FEET + 120                       # the ground line of most sets
TONGUE = (0.90, 0.18, 0.24)
PALS = {"b": (SC.SN_B, SC.SN_B_BELLY, SC.SN_B_BELLY), "g": (SC.SN_G, SC.SN_G_BELLY, SC.SN_G_BELLY)}
AMRIT_W, KUSHA_W = "अमृत", "कुश"                          # the spoken words on the two word cards


def cue(tl, bid, word, frac):
    """A word cue (the word's place in the line) with a fraction fallback."""
    try:
        return T(tl, bid, word)
    except (KeyError, ValueError):
        MISSES.add((bid, word))
        return T(tl, bid, frac)


# Every cue of every line: (name, Hindi word, fraction fallback, ((after, min gap), ...)); "t0" = the line's start.
# Words are exact substrings of the Hindi lines (checked: MISSES stays empty).
CUES = {
    "sn1": (("J", "जीभ", 0.15, (("t0", 0.6),)),
            ("D", "दो", 0.3, (("J", 0.5),)),
            ("Q", "क्यों", 0.42, (("D", 0.3),)),
            ("M", "महाभारत", 0.62, (("Q", 0.8),)),
            ("A", "अमृत", 0.8, (("M", 0.6),))),
    "sn2": (("M", "महाभारत", 0.3, (("t0", 0.3),)),
            ("S", "शुरू", 0.7, (("M", 0.6),))),
    "sn3": (("W", "ताक़तवर", 0.3, (("t0", 0.9),)),
            ("P", "पक्षी", 0.38, (("W", 0.3),)),
            ("U", "उसकी", 0.5, (("P", 0.5),)),
            ("S", "साँपों", 0.62, (("U", 0.5),)),
            ("N", "नौकरानी", 0.8, (("S", 0.5),))),
    "sn4": (("B", "शर्त", 0.2, (("t0", 0.3),)),
            ("H", "घोड़े", 0.5, (("B", 0.6),)),
            ("T", "पूँछ", 0.62, (("H", 0.4),)),
            ("C", "रंग", 0.8, (("T", 0.4),))),
    "sn5": (("S", "चुपके", 0.1, (("t0", 0.2),)),
            ("W", "लिपट", 0.3, (("S", 0.6),)),
            ("K", "काला", 0.5, (("W", 0.8),)),
            ("G", "गरुड़", 0.68, (("K", 0.6),)),
            ("L", "हार", 0.88, (("G", 0.5),))),
    "sn6": (("A", "पूछा", 0.22, (("t0", 0.4),)),
            ("F", "छोड़ने", 0.55, (("A", 0.7),)),
            ("W", "क्या", 0.85, (("F", 0.6),))),
    "sn7": (("S", "स्वर्ग", 0.15, (("t0", 0.3),)),
            ("A", "अमृत", 0.3, (("S", 0.3),)),
            ("D", "पीकर", 0.66, (("A", 0.9),)),
            ("N", "मरता", 0.9, (("D", 0.5),))),
    "sn8": (("F", "उड़कर", 0.06, (("t0", 0.15),)),
            ("H", "स्वर्ग", 0.15, (("F", 0.3),)),
            ("G", "पहरेदारों", 0.28, (("H", 0.6),)),
            ("D", "हराया", 0.4, (("G", 0.5),)),
            ("P", "घड़ा", 0.55, (("D", 0.8),)),
            ("U", "उठा", 0.62, (("P", 0.3),)),
            ("B", "बूँद", 0.85, (("U", 0.8),))),
    "sn9": (("I", "इंद्र", 0.3, (("t0", 0.4),)),
            ("R", "रोका", 0.45, (("I", 0.4),)),
            ("S", "साँपों", 0.8, (("R", 0.6),))),
    "sn9q": (("W", "क्या", 0.15, (("t0", 0.2),)),
             ("M", "माँ", 0.4, (("W", 0.6),)),
             ("A", "अमृत", 0.7, (("M", 0.8),))),
    "sn10": (("C", "चाल", 0.15, (("t0", 0.3),)),
             ("I", "इंद्र", 0.3, (("C", 0.5),)),
             ("P", "घड़ा", 0.5, (("I", 0.6),)),
             ("D", "नीचे", 0.58, (("P", 0.3),)),
             ("Y", "चुपके", 0.85, (("D", 0.9),))),
    "sn11": (("P", "घड़ा", 0.25, (("t0", 0.3),)),
             ("K", "कुश", 0.45, (("P", 0.5),)),
             ("S", "नुकीली", 0.65, (("K", 0.5),)),
             ("R", "रखा", 0.92, (("S", 0.6),))),
    "sn12": (("L", "लो", 0.22, (("t0", 0.4),)),
             ("B", "नहाकर", 0.42, (("L", 0.7),)),
             ("P", "पीना", 0.6, (("B", 0.6),)),
             ("M", "मेरी", 0.75, (("P", 0.6),)),
             ("F", "आज़ाद", 0.9, (("M", 0.5),))),
    "sn13": (("H", "नहाने", 0.22, (("t0", 0.4),)),
             ("P", "पीछे", 0.5, (("H", 0.8),)),
             ("I", "इंद्र", 0.62, (("P", 0.3),)),
             ("U", "उठाकर", 0.75, (("I", 0.5),)),
             ("S", "स्वर्ग", 0.88, (("U", 0.5),))),
    "sn14": (("L", "लौटे", 0.1, (("t0", 0.2),)),
             ("G", "गायब", 0.3, (("L", 0.6),)),
             ("T", "सोचा", 0.5, (("G", 0.8),)),
             ("D", "गिरा", 0.9, (("T", 0.8),))),
    "sn15": (("S", "नुकीली", 0.1, (("t0", 0.2),)),
             ("L", "चाटने", 0.3, (("S", 0.5),)),
             ("C2", "चाटते", 0.5, (("L", 0.8),)),
             ("J", "जीभ", 0.7, (("C2", 0.8),)),
             ("C", "चिर", 0.88, (("J", 0.6),))),
    "sn16": (("E", "हर", 0.12, (("t0", 0.3),)),
             ("D", "दो", 0.3, (("E", 0.5),)),
             ("K", "कुश", 0.6, (("D", 0.9),)),
             ("P", "पूजा", 0.75, (("K", 0.5),)),
             ("V", "पवित्र", 0.85, (("P", 0.4),))),
    "sn16c": (("D", "धोखे", 0.2, (("t0", 0.4),)),
              ("W", "जीती", 0.35, (("D", 0.4),)),
              ("J", "जीभ", 0.55, (("W", 0.9),)),
              ("N", "निशानी", 0.9, (("J", 0.8),))),
    "sn17": (("R", "सही", 0.2, (("t0", 0.4),)),
             ("C", "धोखा", 0.6, (("R", 0.9),)),
             ("K", "कमेंट", 0.85, (("C", 0.6),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_sn_cues", None)
    if cache is None:
        cache = {}
        tl._sn_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, word, frac, cons in CUES[bid]:
            v = cue(tl, bid, word, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


# ------------------------------------------------------------------ small helpers


def ground(cr, y=G, alpha=1.0, blur=0.0):
    prop(cr, "ground", W / 2, y + 6, 0.82, alpha=alpha, blur=blur)


def cloud_floor(cr, t, y=G, alpha=1.0):
    """Heaven's floor: a row of light clouds drifting slowly."""
    for i, (x, s) in enumerate(((60, 0.9), (330, 1.0), (620, 0.95), (900, 1.05), (1140, 0.9))):
        prop(cr, "rr_lcloud", x + 14 * math.sin(t * 0.4 + i), y + 20 + 14 * (i % 2), s, rot=sway(t, 0.006, 0.3, i),
             alpha=alpha)


def board(cr, x, y, w, h, a):
    """A parchment board (octagon, an ink rim, a row of punched dots) centred on (x, y)."""
    c = 18
    pc.poly(cr, [(x - w / 2, y - h / 2 + c), (x - w / 2 + c, y - h / 2), (x + w / 2 - c, y - h / 2),
                 (x + w / 2, y - h / 2 + c), (x + w / 2, y + h / 2 - c), (x + w / 2 - c, y + h / 2),
                 (x - w / 2 + c, y + h / 2), (x - w / 2, y + h / 2 - c)])
    cr.set_source_rgba(0.97, 0.87, 0.62, 0.96 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(4.5)
    cr.stroke()
    for k in range(int((w - 40) // 22)):
        for yd in (y - h / 2 + 11, y + h / 2 - 11):
            cr.new_sub_path()
            cr.arc(x - w / 2 + 24 + k * 22, yd, 2.6, 0, 2 * math.pi)
    cr.set_source_rgba(0.55, 0.32, 0.14, 0.8 * a)
    cr.fill()


def word_card(cr, t, t_in, word, latin, lines, x, y, s=1.0, alpha=1.0, t_lines=None):
    """A parchment card on its rod: the spoken word big in Devanagari (Latin letters without the Nirmala font), a red
    "=", and its plain English meaning in one or two lines (shown at t_lines)."""
    q = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    w, h = 700 * s, 460 * s
    yy = y + 60 * (1 - q)
    pc.rod(cr, x, yy + h / 2, x + 30, H + 60, alpha=0.5 * a)
    board(cr, x, yy, w, h, a)
    wy = yy - 128 * s
    if HAS_INDIC:
        su = indic_surface(word, int(150 * s), tuple(RED))
        k = min(1.0, (w - 120) / max(1, su.get_width()))
        cr.save()
        cr.translate(x, wy)
        cr.scale(k, k)
        cr.set_source_surface(su, -su.get_width() / 2, -su.get_height() / 2)
        cr.paint_with_alpha(a)
        cr.restore()
    else:
        draw_text(cr, latin, x, wy, int(120 * s), RED, a, anchor="cm")
    p = prog(t, t_lines if t_lines is not None else t_in + 0.3, 0.25) * a
    if p > 0.01:
        for k in (-1, 1):                                      # the "="
            cr.set_source_rgba(*INK, p)
            cr.rectangle(x - 34 * s, yy + 2 * s + k * 13 * s - 4 * s, 68 * s, 9 * s)
            cr.fill()
        sz = int(64 * s)
        for i, ln in enumerate(lines):
            draw_text(cr, ln, x, yy + (124 + 70 * i - 35 * (len(lines) - 1)) * s, sz, INK, p, anchor="cm")


def flick(t, ph=0.0, period=1.25):
    """A snake's tongue flicking: 0 (in) .. 1 (out), quick out, a short hold, quick in."""
    u = (t + ph) % period
    if u < 0.10:
        return ease(u / 0.10)
    if u < 0.42:
        return 1.0
    if u < 0.54:
        return 1 - ease((u - 0.42) / 0.12)
    return 0.0


def tongue(cr, root, ang, L, w, fork=1.0, flen=0.36, spread=0.62, wig=0.0, alpha=1.0, crease=0.0):
    """A snake's tongue from root along ang, L long, w wide: fork 0 = one tongue with a round tip (before the end of
    the story), 1 = forked (its last `flen` split into two prongs spread apart). crease draws the line down the
    middle where it will split."""
    if alpha <= 0.01 or L < 2:
        return
    c, s = math.cos(ang), math.sin(ang)
    fl = L * flen * clamp(fork)
    se = (root[0] + c * (L - fl), root[1] + s * (L - fl))
    segs = [(root, se, w)]
    tips = []
    if fork > 0.01:
        sp = spread * clamp(fork) / 2
        pw = w * (1 - 0.42 * clamp(fork * 3))
        for sg in (-1, 1):
            a2 = ang + sg * (sp + wig)
            tip = (se[0] + math.cos(a2) * fl, se[1] + math.sin(a2) * fl)
            segs.append((se, tip, pw))
            tips.append(tip)
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for col, extra in ((pc.INK, max(2.0, w * 0.18)), (TONGUE, 0.0)):
        for p0, p1, ww in segs:
            cr.move_to(*p0)
            cr.line_to(*p1)
            cr.set_source_rgba(*col, alpha)
            cr.set_line_width(ww + 2 * extra)
            cr.stroke()
    if crease > 0.01:
        cr.set_source_rgba(0.42, 0.04, 0.08, 0.8 * crease * alpha)
        cr.set_line_width(max(1.5, w * 0.07))
        cr.move_to(root[0] + c * L * 0.45, root[1] + s * L * 0.45)
        cr.line_to(se[0] + c * fl * 0.0, se[1])
        cr.line_to(root[0] + c * (L - w * 0.3), root[1] + s * (L - w * 0.3))
        cr.stroke()
    cr.restore()
    return tips or [(root[0] + c * L, root[1] + s * L)]


def naga(cr, t, spine, w0, pal="b", face=1, head=None, head_w=SC.HEAD_W, alpha=1.0, rods=True, n=72, head_rot=0.0,
         tng=None, tongue_w=None, tng_kw=None, head_dir=None):
    """A leather snake (scenes_ruru.snake with this video's palettes and heads): spine = screen points from the neck
    to the tail tip; w0 = the body's width at the neck. tng = (length px, fork 0..1, spread, wiggle) draws the tongue
    under the head. Returns {snout, dir, head, cen, tips}."""
    if alpha <= 0.01 or len(spine) < 2:
        return None
    P, L = _resample(spine, n)
    col, belly, bandc = PALS[pal]
    Nn, Ww = [], []
    for i in range(n):
        a, b = P[max(0, i - 1)], P[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1.0
        Nn.append((ty / ln * face, -tx / ln * face))
        u = i / (n - 1)
        Ww.append(w0 * (1 + 0.15 * math.sin(math.pi * clamp(u / 0.5))) * (1 - 0.92 * clamp((u - 0.4) / 0.6) ** 1.4))
    bk = [(p[0] - nn[0] * w / 2, p[1] - nn[1] * w / 2) for p, nn, w in zip(P, Nn, Ww)]
    be = [(p[0] + nn[0] * w / 2, p[1] + nn[1] * w / 2) for p, nn, w in zip(P, Nn, Ww)]
    inner = [(p[0] + nn[0] * w * 0.14, p[1] + nn[1] * w * 0.14) for p, nn, w in zip(P, Nn, Ww)]
    period = 1.15 * w0
    lw = max(2.2, 0.065 * w0) if w0 < 120 else max(5.0, 0.03 * w0)
    cr.push_group()
    m = 8
    s = n - 1
    while s > 0:
        a = max(0, s - m - 1)
        idx = range(a, s + 1)
        pc.poly(cr, [bk[i] for i in idx] + [be[i] for i in reversed(idx)])
        cr.set_source_rgb(*col)
        cr.fill()
        for i in range(a, s):
            if ((L * i / (n - 1)) / period) % 1.0 < 0.3 and i > 2:
                pc.poly(cr, [bk[i], bk[i + 1], be[i + 1], be[i]])
                cr.set_source_rgb(*bandc)
                cr.fill()
        pc.poly(cr, [be[i] for i in idx] + [inner[i] for i in reversed(idx)])
        cr.set_source_rgb(*belly)
        cr.fill()
        for edge in (bk, be):
            cr.move_to(*edge[a])
            for i in range(a + 1, s + 1):
                cr.line_to(*edge[i])
            cr.set_source_rgb(*pc.INK)
            cr.set_line_width(lw)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke()
        holes = [(P[i][0] - Nn[i][0] * Ww[i] * 0.2, P[i][1] - Nn[i][1] * Ww[i] * 0.2) for i in idx
                 if i % 3 == 0 and Ww[i] > 0.35 * w0 and i > 2]
        pc.punch(cr, holes, max(1.6, 0.05 * w0))
        s = a
    cr.new_path()
    cr.arc(P[-1][0], P[-1][1], max(1.5, Ww[-1] / 2), 0, 2 * math.pi)
    cr.set_source_rgb(*col)
    cr.fill()
    pat = cr.pop_group()
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source(pat)
    cr.paint_with_alpha(alpha)
    cr.restore()
    hp = P[0]
    q = P[min(4, n - 1)]
    ang = math.atan2(hp[1] - q[1], hp[0] - q[0])
    if head_dir is not None:                          # turn the head to look along head_dir
        head_rot = (head_dir - ang + math.pi) % (2 * math.pi) - math.pi
    hs = w0 / head_w
    kk = head_w / SC.HEAD_W
    name = head or f"sn_snake_{pal}"
    hrot = ang + head_rot if face > 0 else ang - math.pi + head_rot
    fx = 1 if face > 0 else -1
    dir_ = ang + head_rot

    def scr(px, py):
        x_, y_ = fx * px * hs, py * hs
        return (hp[0] + x_ * math.cos(hrot) - y_ * math.sin(hrot), hp[1] + x_ * math.sin(hrot) + y_ * math.cos(hrot))
    tips = None
    if tng is not None and tng[0] > 2:
        Lt, fork, spread, wig = tng
        tips = tongue(cr, scr((SC.SNOUT[0] - 26) * kk, SC.SNOUT[1] * kk + 4 * kk), dir_, Lt + 26 * kk * hs,
                      tongue_w or max(4.0, 0.10 * w0), fork, spread=spread, wig=wig, alpha=alpha, **(tng_kw or {}))
    prop(cr, name, hp[0], hp[1], hs, rot=hrot, alpha=alpha, flip=face < 0)
    if rods:
        mid = P[n // 3]
        pc.rod(cr, mid[0], mid[1], mid[0] + 40, H + 60, alpha=0.45 * alpha)
        pc.rod(cr, hp[0], hp[1] + 20 * hs, hp[0] + 60, H + 60, alpha=0.45 * alpha)
    return dict(snout=scr(SC.SNOUT[0] * kk, SC.SNOUT[1] * kk), dir=dir_, head=hp, cen=scr(100 * kk, 0), tips=tips)


def raised(cr, t, x, y, w0, face=1, pal="b", lift=1.0, bob=0.0, ph=0.0, tng=None, head=None, alpha=1.0, rods=True,
           turns=1.4, look=0.0):
    """A snake coiled on the ground at (x, y), its neck raised (lift 0..1) with the head at the top; bob nods it."""
    R = 2.3 * w0
    hx = x + face * (0.45 * R + 0.06 * w0 * math.sin(t * 1.3 + ph))
    hy = y - (1.8 + 2.4 * lift) * w0 - bob * 0.45 * w0 * abs(math.sin(t * 7 + ph)) - 0.1 * w0 * math.sin(t * 1.7 + ph)
    sp = spine_coil(x, y, R, face, (hx, hy), turns=turns, stack=0.45 * w0, arch=0.9 * w0 * lift)
    return naga(cr, t, sp, w0, pal, face, head, alpha=alpha, rods=rods, head_rot=-0.25 * lift * face + look, tng=tng)


def tng_flick(t, Lmax, fork=0.0, ph=0.0, period=1.25, spread=0.62):
    f = flick(t, ph, period)
    return (Lmax * f, fork, spread, 0.10 * math.sin(t * 38 + ph) * fork)


def cum_len(path):
    c = [0.0]
    for a, b in zip(path, path[1:]):
        c.append(c[-1] + math.dist(a, b))
    return c


def point_at(path, cum, s):
    s = clamp(s, 0.0, cum[-1])
    i = max(1, min(len(path) - 1, bisect.bisect_left(cum, s)))
    seg = (cum[i] - cum[i - 1]) or 1.0
    f = (s - cum[i - 1]) / seg
    a, b = path[i - 1], path[i]
    return a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f


def follow(path, cum, s_head, length, n=40):
    """A spine along a path: from arc length s_head back `length` (clamped at the path's start)."""
    return [point_at(path, cum, s_head - length * i / (n - 1)) for i in range(n)]


def wave_path(x0, x1, y, amp, wl, n=60):
    """A slithering track along the ground from x0 to x1."""
    return [(x0 + (x1 - x0) * i / (n - 1), y + amp * math.sin(2 * math.pi * (x1 - x0) * i / (n - 1) / wl))
            for i in range(n)]


def slither(cr, t, t0, t1, x0, x1, y, w0, pal="b", ph=0.0, tng=None, alpha=1.0, rods=True, length=None):
    """A snake slithering along the ground from x0 (its head) to x1 between t0 and t1, its body waving behind."""
    face = 1 if x1 > x0 else -1
    length = length or 9.0 * w0
    path = wave_path(x0 - face * (length + 40), x1, y, 0.7 * w0, 6.0 * w0)
    cum = cum_len(path)
    u = ease(clamp((t - t0) / max(0.1, t1 - t0)) * 0.85 + 0.15 * clamp((t - t0) / max(0.1, t1 - t0)) ** 2)
    sh = length + 40 + (cum[-1] - length - 40) * u
    sp = follow(path, cum, sh, length)
    return naga(cr, t, sp, w0, pal, face, alpha=alpha, rods=rods, tng=tng)


# ------------------------------------------------------------------ puppets


GA_HEAD = {m: "sn_garuda_head" + ("" if m == "calm" else "_" + m) for m in SC.GA_MOODS}
VN_HEAD = {m: "sn_vinata_head" + ("" if m == "calm" else "_" + m) for m in SC.VN_MOODS}
KD_HEAD = {m: "sn_kadru_head" + ("" if m == "smug" else "_" + m) for m in SC.KD_MOODS}


def talking(t, t0, t1, rate=4.6):
    return t0 < t < t1 and int(t * rate) % 3 != 0


def garuda(cr, t, x, s, mood="calm", front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0), hits=(),
           flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, feet=G, y=None, ph=0.0, flap=0.0, spread=0.0, rate=2.2,
           extra=None, kneel=False):
    """Garuda standing (feet on `feet`, or hip at y); flap 0..1 beats his wings, spread raises them (+) or folds them
    back (-). mood: calm | talk | angry | smile."""
    hy = feet - (250 if kneel else 434) * s if y is None else y
    ang = man_angles("sn_garuda", t, front, backa, head, legs, hits, ph)
    hide = ()
    if kneel:                                       # on one knee
        prop(cr, "sn_garuda_kneel", x, hy, s, rot + bob_rot(t, ph), alpha, blur, flip)
        hide = ("sn_garuda_legF", "sn_garuda_legB")
    beat = flap * math.sin(2 * math.pi * rate * t + ph)
    ang["sn_gwing_near"] = spread + 0.5 * beat + sway(t, 0.03, 0.4, ph)
    ang["sn_gwing_far"] = 0.7 * spread + 0.42 * beat + sway(t, 0.03, 0.4, ph + 1)
    return puppet(cr, SC.GARUDA, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur,
                  swap={"sn_garuda_head": GA_HEAD[mood]}, rods=rods, extra=extra, hide=hide)


def garuda_fly(cr, t, x, y, s, mood="calm", flip=False, alpha=1.0, blur=0.0, front=(-2.85, -0.15),
               backa=(-2.55, -0.3), tilt=0.0, ph=0.0, extra=None, flap=1.0):
    """Garuda in flight (hip at x, y), body along the flight, head up, arms reaching ahead, legs trailing, wings
    beating."""
    r = 1.22 + tilt + 0.03 * math.sin(t * 4.4 + ph)
    return garuda(cr, t, x, s, mood, front=front, backa=backa, head=-1.0, legs=(0.35, 0.55), flip=flip,
                  alpha=alpha, blur=blur, rods=False, rot=r if not flip else -r, y=y, ph=ph, flap=flap, rate=2.6,
                  spread=0.1, extra=extra)


def vinata(cr, t, x, s, mood="calm", front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(), flip=False,
           alpha=1.0, blur=0.0, rods=True, rot=0.0, feet=G, y=None, ph=0.0, sweep=0.0, broom=True, broom_drop=None):
    """Garuda's mother (feet on `feet`); sweep 0..1 bends her over the broom and swings it; broom_drop = the time she
    lets it fall (it is then drawn by broom_fall)."""
    hy = feet - 470 * s if y is None else y
    if sweep > 0.01:
        sw_ = math.sin(t * 5.2 + ph)
        front = mix(front, (-0.62 + 0.24 * sw_, -0.18), sweep)
        backa = mix(backa, (-0.45 + 0.2 * sw_, -0.4), sweep)
        rot += 0.10 * sweep * (-1 if flip else 1)
        head += 0.14 * sweep
    ang = woman_angles("sn_vinata", t, front, backa, head, hits, ph)
    ex = None
    if broom and (broom_drop is None or t < broom_drop):
        ex = {"sn_vinata_armF_lo": held_grip("sn_broom", front, 0.92, 0.42 * sweep + 0.1, 30, alpha, blur)}
    return puppet(cr, SC.VINATA, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur,
                  swap={"sn_vinata_head": VN_HEAD[mood]}, rods=rods, extra=ex)


def kadru(cr, t, x, s, mood="smug", front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(), flip=True,
          alpha=1.0, blur=0.0, rods=True, rot=0.0, feet=G, y=None, ph=0.0):
    """The snakes' mother (feet on `feet`). mood: smug | laugh | shock | calm."""
    hy = feet - 470 * s if y is None else y
    ang = woman_angles("sn_kadru", t, front, backa, head, hits, ph)
    return puppet(cr, SC.KADRU, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur,
                  swap={"sn_kadru_head": KD_HEAD[mood]}, rods=rods)


def indra(cr, t, x, s, front=(-0.6, -0.9), backa=(0.15, -0.95), head=0.0, flip=True, alpha=1.0, blur=0.0, rods=True,
          rot=0.0, feet=G, y=None, ph=0.0, vajra=True, glow_a=0.6, hits=(), legs=(0.0, 0.0)):
    """Indra, king of the gods (mandhata_cast), the vajra upright in his back hand, a soft glow about him."""
    hy = feet - 434 * s if y is None else y
    if glow_a > 0.01:
        hx_, hy_ = local(x, hy, s, rot, flip, 10, -420)
        glow(cr, hx_, hy_, 380 * s + 60, 0.5 * glow_a * alpha)
        warm(cr, hx_, hy_, 300 * s, 0.4 * glow_a * alpha)
    ex = {"indra_armB_lo": held("md_vajra", backa, 0.62, alpha=alpha, blur=blur)} if vajra else None
    return fig(cr, M.INDRA, "indra", t, x, s, front=front, backa=backa, head=head, flip=flip, alpha=alpha, blur=blur,
               rods=rods, rot=rot, feet=feet, y=y, ph=ph, extra=ex, hits=hits, legs=legs)


def guard(cr, t, x, s, flip=True, alpha=1.0, blur=0.0, rot=0.0, feet=G, y=None, ph=0.0, halo=1.0):
    """A guard of heaven: a dark silhouette (shani_cast's deva) with a spear and a faint gold ring of a halo."""
    if alpha <= 0.01:
        return None
    hy = feet - 434 * s if y is None else y
    if halo > 0.01:
        hc = local(x, hy, s, rot, flip, 16, -440)
        cr.save()
        cr.set_source_rgba(1.0, 0.78, 0.30, 0.6 * alpha * halo)
        cr.set_line_width(max(3.0, 8 * s))
        cr.arc(hc[0], hc[1], 140 * s, 0, 2 * math.pi)
        cr.stroke()
        cr.restore()
    ba = (0.15, -0.95)
    ex = {"sg_deva_armB_lo": held_grip("jd_spear", ba, 0.8, 0.0, 60, 1.0, blur)}
    return silhouette(cr, lambda c: fig(c, SG.DEVA, "sg_deva", t, x, s, front=(-0.5, -0.6), backa=ba, flip=flip,
                                        feet=feet, y=y, ph=ph, rods=True, rot=rot, alpha=1.0, blur=blur, extra=ex),
                      0.86 * alpha)


def horse(cr, t, x, ground_, s, black=0.0, alpha=1.0, blur=0.0, tail=None):
    """The white horse (feet on ground_) and its tail (white, or black by `black`); returns the tail's root and
    rotation."""
    prop(cr, "sn_horse", x, ground_, s, rot=sway(t, 0.003, 0.3), alpha=alpha, blur=blur)
    root = local(x, ground_, s, 0.0, False, *SC.TAIL_ROOT)
    tr = sway(t, 0.045, 0.45) + 0.04 if tail is None else tail
    if black < 0.99:
        prop(cr, "sn_tail", root[0], root[1], s, rot=tr, alpha=alpha * (1 - black), blur=blur)
    if black > 0.01:
        prop(cr, "sn_tail_black", root[0], root[1], s, rot=tr, alpha=alpha * black, blur=blur)
    return root, tr


TAIL_C = [(-6, 10), (-34, 135), (-72, 270), (-115, 400), (-155, 510), (-180, 590)]    # the tail's middle line


def tail_pt(root, tr, s, v):
    """A point on the tail's middle line, v = 0 (root) .. 1 (tip), and the normal there."""
    f = v * (len(TAIL_C) - 1)
    i = min(len(TAIL_C) - 2, int(f))
    u = f - i
    a, b = TAIL_C[i], TAIL_C[i + 1]
    px, py = a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u
    tx, ty = b[0] - a[0], b[1] - a[1]
    ln = math.hypot(tx, ty) or 1.0
    c, si = math.cos(tr), math.sin(tr)
    p = (root[0] + s * (px * c - py * si), root[1] + s * (px * si + py * c))
    nx, ny = -ty / ln, tx / ln
    return p, (nx * c - ny * si, nx * si + ny * c)


def amrit(cr, t, x, y, s, glow_a=1.0, alpha=1.0, rot=0.0, blur=0.0):
    """The pot of amrit with its bottom at (x, y), glowing: light, slow golden rays, sparkles rising from its lid."""
    if alpha <= 0.01:
        return
    cx, cy = local(x, y, s, rot, False, 0, -200)
    if glow_a > 0.01:
        glow(cr, cx, cy, 560 * s + 80, 0.6 * glow_a * alpha)
        warm(cr, cx, cy, 420 * s, 0.5 * glow_a * alpha)
        aura(cr, t, cx, cy, 170 * s, 560 * s, 0.6 * glow_a * alpha, n=16, spin=0.2)
    prop(cr, "sn_amrit", x, y, s, rot=rot, alpha=alpha, blur=blur)
    if glow_a > 0.01:
        tx, ty = local(x, y, s, rot, False, 0, SC.POT_TOP)
        lights(cr, t, tx, ty - 20 * s, 140 * s + 20, 6, 0.85 * glow_a * alpha)


def kusha(cr, t, x, ground_, s, part="back", alpha=1.0, blur=0.0):
    prop(cr, "sn_kusha_" + part, x, ground_, s, rot=sway(t, 0.005, 0.4, x * 0.01), alpha=alpha, blur=blur)


def blade_tips(x, ground_, s, n=8):
    """Screen points of the tall kusha blades' tips (snake_cast._BACK)."""
    out = []
    for bx, L, a in SC._BACK[:n]:
        out.append((x + s * (bx * 0.5 + L * math.sin(a)), ground_ + s * (-8 - L * math.cos(a))))
    return out


def think(cr, t, t_in, x, y, s, alpha=1.0, flip=False, t_out=None):
    """arjuna_cast's thought bubble popping in at t_in; returns its alpha (0 = not shown)."""
    q = back(clamp((t - t_in) / 0.35), 1.5)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.3)
    if q <= 0.01:
        return 0.0
    prop(cr, "ar_think", x, y, s * (0.6 + 0.4 * q), rot=sway(t, 0.006, 0.4), alpha=clamp(q) * alpha, flip=flip)
    return clamp(q) * alpha


def bubble_clip(cr, x, y, s):
    cr.new_path()
    pc.ell(cr, x, y, 270 * s, 190 * s)
    cr.clip()


def drops(cr, t, pts, a, size=0.45):
    """Little drops of amrit twinkling on the blades."""
    if a <= 0.01:
        return
    for i, (x, y) in enumerate(pts):
        tw = 0.75 + 0.25 * math.sin(t * 5 + i * 1.9)
        glow(cr, x, y, 70, 0.4 * a * tw)
        prop(cr, "sn_drop", x, y, size, alpha=a)
        sparkle(cr, x + 8, y - 12, 18 * tw, a)


# ------------------------------------------------------------------ sn1  hook


HOOK = dict(x=170, y=1200, w0=270, rot=0.08)


def hook_spine(hx, hy):
    """The hook snake's body: from the neck back to the left, coiling down and sweeping off the bottom right."""
    return [(hx, hy), (hx - 160, hy + 6), (hx - 330, hy + 90), (hx - 430, hy + 260), (hx - 400, hy + 450),
            (hx - 220, hy + 590), (hx + 60, hy + 650), (hx + 380, hy + 680), (hx + 700, hy + 730),
            (hx + 1000, hy + 860)]


def hook_snake(cr, t, hold=(), mood_open=False, fork=1.0, alpha=1.0, tlen=210):
    """The hook's big snake: the head large on the left, facing right, its body coiling down out of the frame; the
    forked tongue flicks (hold = [(t_from, t_to), ...] keeps it out). Returns naga()'s points."""
    hx, hy, w0 = HOOK["x"], HOOK["y"] + 10 * math.sin(t * 1.1), HOOK["w0"]
    f = flick(t, 0.2, 1.3)
    held_out = False
    for h0, h1 in hold:
        if h0 < t < h1:
            held_out = True
            f = max(f, prog(t, h0, 0.12))
    tn = (tlen * f, fork, 0.62, 0.08 * math.sin(t * 40) * (0 if held_out else 1))
    return naga(cr, t, hook_spine(hx, hy), w0, "b", 1, "sn_snake_big_open" if mood_open else "sn_snake_big",
                head_w=300.0, alpha=alpha, head_rot=HOOK["rot"] + 0.04 * math.sin(t * 1.3), tng=tn, tongue_w=28, n=90)


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "sn1")
    tD, tM, tA = c["D"], c["M"], c["A"]
    glow(cr, 420, 1250, 680, 0.42)
    hold = (tD - 0.05, tD + 1.3)
    sn = hook_snake(cr, t, [(-1.0, 1.1), hold])
    tips = sn["tips"] if sn and sn["tips"] else None
    pq = back(clamp((t - tA + 0.1) / 0.4), 1.5)
    if pq > 0.01:                                       # the pot of amrit pops in: the Mahabharata's answer
        amrit(cr, t, 870, 900, 0.42 * pq, alpha=clamp(pq))

    def ui(cr):
        if t < tM - 0.1:
            head2(cr, t, "WHY IS A SNAKE'S TONGUE", -1.0, "SPLIT?", 0.3, big_size=290, ghost=-1.0, under=tD + 0.1)
        else:
            head2(cr, t, "THE MAHABHARATA SAYS:", tM - 0.1, "AMRIT DID IT!", tA, big_size=230)
        if hold[0] < t < hold[1] + 0.4 and tips and len(tips) == 2:
            mx = (tips[0][0] + tips[1][0]) / 2
            my = (tips[0][1] + tips[1][1]) / 2
            a = 1 - prog(t, hold[1], 0.4)
            red_ring(cr, mx - 6, my, 76, 70, prog(t, hold[0] + 0.1, 0.35), 9, a)
            plate(cr, t, hold[0] + 0.3, "TWO TIPS!", min(mx - 20, 900), my + 120, 40, alpha=a)
        if tA - 0.1 < t:
            plate(cr, t, tA + 0.2, "AMRIT", 870, 945, 36)
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.2) + flash_at(t, tD, 0.2) + flash_at(t, tA, 0.25))


# ------------------------------------------------------------------ sn2  the very first chapters of the Mahabharata


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "sn2")
    tM, tS = c["M"], c["S"]
    leaves = [(None, [("MAHABHARATA", 100, HEAD_FONT)], 0),
              (tS, [([("THE VERY FIRST", INK)], 70, HEAD_FONT), ([("CHAPTERS", RED)], 86, HEAD_FONT)], 0)]
    book(cr, t, 540, 960, 0.86, leaves, t_in=t0 + 0.05, t_open=tM - 0.15, ring=(1, 1, 0, tS + 0.3))

    def ui(cr):
        if t < tS - 0.1:
            head2(cr, t, "A STORY FROM THE", t0 + 0.05, "MAHABHARATA", tM, big_size=200)
        else:
            head2(cr, t, "RIGHT AT THE", tS - 0.1, "VERY START", tS + 0.05, big_size=240, under=tS + 0.4)
    return dict(ui=ui, flash=flash_at(t, tM, 0.25) + flash_at(t, tS, 0.2))


# ------------------------------------------------------------------ sn3  Garuda; his mother, a servant


GA3 = (560, 0.86)


def s_garuda(cr, t, tl, t0, t1):
    c = cues(tl, "sn3")
    tW, tP = c["W"], c["P"]
    x, s = GA3
    glow(cr, x, 1150, 700, 0.45)
    ground(cr)
    land = ease(clamp((t - t0 + 0.1) / 0.8))
    b, k, a = depth(t, t0 - 0.1, 0.5)
    flex = keyed(t, [(t0, 0.0), (tW - 0.1, 1.0)], 0.3, 1.4)
    feet = G + 30 - 160 * (1 - land)
    pts = garuda(cr, t, x, s * k, mood="calm" if t < tW else "smile", feet=feet, alpha=a, blur=b,
                 front=mix((-0.5, -0.6), (-2.65, -0.3), flex), backa=mix((0.3, -0.3), (-2.4, -0.4), flex),
                 flap=1.0 - 0.75 * land + 0.4 * flex * math.exp(-1.5 * max(0.0, t - tW)), spread=0.35 * flex,
                 hits=[(t0 + 0.7, 0.6), (tW, 0.5)], ph=0.4)
    if t > tW:
        ch = to_user(cr, pts["chest"])
        burst(cr, t, ch[0], ch[1] - 120, tW, n=18, rmax=640, alpha=0.6)
    if t < t0 + 0.9:                                    # dust where he lands
        for i in range(6):
            q = clamp((t - t0 - 0.5) / 0.6)
            if q > 0:
                prop(cr, "cloud", x + (i - 2.5) * (50 + 110 * q), G - 10 - 40 * q, 0.15 + 0.1 * q,
                     alpha=0.4 * (1 - q))
    def ui(cr):
        if t < tW - 0.1:
            head2(cr, t, "THIS IS", t0 + 0.05, "GARUDA", t0 + 0.25, big_size=280)
        else:
            head2(cr, t, "A HUGE AND MIGHTY", tW - 0.1, "BIRD!", tP, big_size=300)
        tag(cr, t, t0 + 0.6, "GARUDA", 860, 1180, 44)
        plate(cr, t, t0 + 0.9, "KING OF BIRDS", 860, 1252, 32)
    return dict(ui=ui, flash=flash_at(t, t0 + 0.6, 0.2) + flash_at(t, tW, 0.3))


VN3 = (330, 0.68)
KD3 = (800, 0.7)
SNK3 = ((630, 1805, 46, -1, "g", 0.3), (985, 1810, 50, -1, "b", 1.4), (1060, 1720, 38, -1, "b", 2.2))


def snakes_by(cr, t, specs, alpha=1.0, bob=0.0, tng=True, fork=0.0, look=0.0):
    """A few raised snakes: specs = (x, y, w0, face, palette, phase)."""
    out = []
    for x, y, w0, face, pal, ph in specs:
        out.append(raised(cr, t, x, y, w0, face, pal, 1.0, bob, ph, tng_flick(t, 2.0 * w0, fork, ph) if tng else None,
                          alpha=alpha, look=look))
    return out


def s_servant(cr, t, tl, t0, t1):
    c = cues(tl, "sn3")
    tU, tS, tN = c["U"], c["S"], c["N"]
    glow(cr, 540, 1350, 640, 0.4)
    ground(cr)
    garuda(cr, t, 105, 0.42, mood="calm", feet=G - 60, blur=4, alpha=0.75, front=(-0.5, -0.8), rods=False, ph=0.2,
           flap=0.0, spread=-0.1)
    kx, ks = KD3
    point = keyed(t, [(t0, 0.0), (tS + 0.1, 1.0)], 0.3, 1.4)
    kadru(cr, t, kx, ks, mood="smug", front=mix((-0.3, -0.5), (-1.2, -0.25), point), backa=(0.5, -1.6), ph=1.0,
          hits=[(tS + 0.1, 0.4)])
    snakes_by(cr, t, SNK3)
    vx, vs = VN3
    vp = vinata(cr, t, vx, vs, mood="sad", sweep=1.0, ph=0.3, head=0.1)
    hand = to_user(cr, vp["handF"])
    for i in range(4):                                  # dust puffs from her broom
        u = (t * 1.1 + i / 4) % 1.0
        prop(cr, "cloud", hand[0] + 110 + 70 * u + 20 * i, G - 20 - 50 * u, 0.08 + 0.08 * u, alpha=0.35 * (1 - u))
    vtop = to_user(cr, vp["top"])
    dev_k = (kx + 10, G - 1260 * ks)

    def ui(cr):
        head2(cr, t, "HIS MOTHER WAS A", tU - 0.05, "SERVANT", tN, big_size=290, under=tN + 0.4)
        tag(cr, t, tU + 0.1, "HIS MOTHER", max(170, vtop[0] - 10), vtop[1] - 60, 38)
        tag(cr, t, tS + 0.05, "SNAKES' MOTHER", min(860, dev_k[0]), dev_k[1] - 30, 36)
    return dict(ui=ui, flash=flash_at(t, tU, 0.15) + flash_at(t, tN, 0.2))


# ------------------------------------------------------------------ sn4  the bet: the white horse's tail colour


HS4 = (505, 0.6)                     # the horse: x, scale (feet on G)


def s_bet(cr, t, tl, t0, t1):
    c = cues(tl, "sn4")
    tB, tH, tT, tC = c["B"], c["H"], c["T"], c["C"]
    glow(cr, 560, 1300, 700, 0.42)
    ground(cr)
    hx, hs = HS4
    b, k, a = depth(t, t0 - 0.2, 0.5)
    root, tr = horse(cr, t, hx, G, hs * k, alpha=a, blur=b)
    for who, x, ph in (("v", 115, 0.3), ("k", 975, 1.1)):
        bb, kk, aa = depth(t, tB - 0.2 + (0.15 if who == "k" else 0), 0.45)
        if who == "v":
            vinata(cr, t, x, 0.52 * kk, mood="calm", alpha=aa, blur=bb, ph=ph, broom=False, front=(-0.6, -0.9))
        else:
            kadru(cr, t, x, 0.52 * kk, mood="smug", alpha=aa, blur=bb, ph=ph, front=(-0.6, -0.9))
    mid, _ = tail_pt(root, tr, hs, 0.55)

    def ui(cr):
        if t < tT - 0.1:
            head2(cr, t, "BECAUSE OF A", t0 + 0.05, "BET!", tB, big_size=300)
        else:
            head2(cr, t, "THE BET:", tT - 0.1, "TAIL COLOUR?", tC, big_size=230)
        plate(cr, t, tH + 0.1, "A WHITE HORSE", 640, 1440, 34, t_out=tT + 0.2)
        if t > tT - 0.05:
            red_ring(cr, mid[0] - 10, mid[1] - 10, 120, 250, prog(t, tT, 0.4), 9)
            qmark(cr, t, tT + 0.1, mid[0] - 10, mid[1] - 330, 190, RED)
        plate(cr, t, tC + 0.35, "WHITE!", 125, 1330, 40)
        plate(cr, t, tC + 0.6, "BLACK!", 950, 1250, 40, color=RED)
    return dict(ui=ui, flash=flash_at(t, tB, 0.2) + flash_at(t, tT, 0.2))


# ------------------------------------------------------------------ sn5  the snakes wrap the tail; it looks black


HS5 = (1000, 1.3, G)                # the horse close: x, scale, ground (its rear and tail on the left)
WRAP = ((0.97, 0.64, 1.6, "b", 0.0), (0.68, 0.36, 1.6, "g", 0.18), (0.42, 0.06, 1.7, "b", 0.36))


def wrap_path(root, tr, s, v_top, v_bot, turns, ground_, x_start):
    """Track of a snake from the ground at the left up to the tail's tip, then winding up the tail from v_bot to v_top
    (a zig-zag across it, so it looks wrapped round)."""
    tip, _ = tail_pt(root, tr, s, 1.0)
    path = wave_path(x_start, tip[0] - 20, ground_ - 14, 14, 160, 30)
    for i in range(1, 13):                                # up the middle of the tail to its own stretch
        v = 1.0 - (1.0 - v_bot) * i / 12
        p, _ = tail_pt(root, tr, s, v)
        path.append(p)
    n = 70
    for i in range(1, n + 1):
        u = i / n
        v = v_bot + (v_top - v_bot) * u
        p, nn = tail_pt(root, tr, s, v)
        hw = 46 * s * (1 - 0.15 * v)
        off = hw * math.sin(2 * math.pi * turns * u)
        path.append((p[0] + nn[0] * off, p[1] + nn[1] * off))
    return path


def s_wrap(cr, t, tl, t0, t1):
    c = cues(tl, "sn5")
    tS, tW, tK = c["S"], c["W"], c["K"]
    hx, hs, gy = HS5
    glow(cr, 420, 1350, 640, 0.4)
    ground(cr, y=gy)
    black = prog(t, tK - 0.1, 0.6)
    root, tr = horse(cr, t, hx, gy, hs, black=black, tail=0.06 + 0.02 * math.sin(t * 0.8))
    heads = []
    for i, (vb, vt, turns, pal, dl) in enumerate(WRAP):
        path = wrap_path(root, tr, hs, vt, vb, turns, gy, -420 - 140 * i)
        cum = cum_len(path)
        L = 560
        u = clamp((t - tS - dl) / max(0.8, tK - 0.15 - tS - dl))
        sh = L + (cum[-1] - L) * ease(u)
        sp = follow(path, cum, sh, L, 60)
        out = naga(cr, t, sp, 40, pal, 1, alpha=1.0, rods=False, tng=tng_flick(t, 60, 0.0, i), n=60)
        if out:
            heads.append(out["head"])
    if tK - 0.1 < t < tK + 1.2:
        p, _ = tail_pt(root, tr, hs, 0.5)
        red_ring(cr, p[0] - 20, p[1], 190, 440, prog(t, tK, 0.4), 9, 1 - prog(t, tK + 0.9, 0.3))

    def ui(cr):
        if t < tK - 0.1:
            head2(cr, t, "SNEAKY SNAKES", t0 + 0.05, "CHEATED!", tW, big_size=290)
        else:
            head2(cr, t, "NOW THE TAIL LOOKED", tK - 0.1, "BLACK!", tK + 0.05, big_size=310, under=tK + 0.5)
        if heads and tW < t < tK + 0.5:
            hx_, hy_ = heads[0]
            plate(cr, t, tW + 0.3, "SHH!", min(940, hx_ + 140), hy_ - 60, 40, t_out=tK)
    return dict(ui=ui, flash=flash_at(t, tW, 0.15) + flash_at(t, tK, 0.3))


def s_lost(cr, t, tl, t0, t1):
    c = cues(tl, "sn5")
    tG, tL = c["G"], c["L"]
    glow(cr, 540, 1350, 640, 0.4)
    horse(cr, t, 600, G - 150, 0.42, black=1.0, alpha=0.5, blur=6)
    ground(cr)
    laugh = t > tL - 0.1
    kadru(cr, t, 800, 0.62, mood="laugh" if laugh else "smug", front=(-2.4, -0.4) if laugh else (-0.3, -0.5),
          backa=(0.5, -1.6), ph=1.0, hits=[(tL, 0.5)])
    snakes_by(cr, t, SNK3, bob=1.0 if laugh else 0.3)
    sad = prog(t, tG, 0.5)
    vinata(cr, t, 300, 0.62, mood="sad" if t > tG + 0.1 else "calm", head=0.3 * sad, broom=False,
           front=mix((-0.3, -0.5), (-0.15, -0.2), sad), backa=mix((0.2, -0.3), (0.1, -0.1), sad), ph=0.3,
           rot=0.05 * sad)

    def ui(cr):
        head2(cr, t, "SO HIS MOTHER", tG - 0.05, "LOST THE BET", tL, big_size=230, under=tL + 0.4)
        plate(cr, t, t0 - 0.5, "WHITE!", 300, 1050, 44)
        if t > tL - 0.2:
            big_x(cr, 300, 1050, 220, 90, prog(t, tL - 0.1, 0.3), alpha=0.92, lw=14)
        plate(cr, t, t0 - 0.5, "BLACK!", 800, 990, 44, color=RED)
    return dict(ui=ui, flash=flash_at(t, tL, 0.2), night=0.06 * sad)


# ------------------------------------------------------------------ sn6  Garuda asks the snakes: what do you want?


GA6 = (360, 0.7)
SNK6 = ((700, 1810, 60, -1, "b", 0.4), (880, 1760, 52, -1, "g", 1.3), (1010, 1830, 48, -1, "b", 2.1))


def s_ask(cr, t, tl, t0, t1):
    c = cues(tl, "sn6")
    tA, tF, tW = c["A"], c["F"], c["W"]
    glow(cr, 540, 1300, 680, 0.42)
    ground(cr)
    vp = vinata(cr, t, 135, 0.42, mood="sad", sweep=1.0, ph=0.3, blur=2.5, alpha=0.85, rods=False, feet=G - 30)
    vtop = to_user(cr, vp["top"])
    gx, gs = GA6
    ask = keyed(t, [(t0, 0.0), (tA, 1.0), (tW, 2.0)], 0.3, 1.4)
    fr = (-1.3, -0.35) if ask < 1.5 else (-1.55, -0.6)
    garuda(cr, t, gx, gs, mood="talk" if talking(t, tA - 0.2, t1 - 0.2) else "calm",
           front=mix((-0.4, -0.6), fr, min(1.0, ask)), hits=[(tA, 0.4), (tW, 0.4)], ph=0.6, flap=0.0)
    snakes_by(cr, t, SNK6)

    def ui(cr):
        if t < tF - 0.1:
            head2(cr, t, "GARUDA ASKED", t0 + 0.05, "THE SNAKES", tA, big_size=270)
        else:
            head2(cr, t, "TO FREE MY MOTHER,", tF - 0.1, "WHAT DO YOU WANT?", tW, big_size=170)
        if t > tF:
            red_ring(cr, vtop[0] - 10, vtop[1] + 190, 110, 250, prog(t, tF + 0.1, 0.4), 8,
                     1 - prog(t, tW + 0.8, 0.4))
        if t > tW - 0.1:
            cloud_text(cr, t, 790, 1000, 0.62, [("WHAT DO", 54, INK, -26, tW), ("YOU WANT?", 60, RED, 36, tW + 0.1)],
                       t_in=tW - 0.1)
    return dict(ui=ui, flash=flash_at(t, tF, 0.15) + flash_at(t, tW, 0.2))


# ------------------------------------------------------------------ sn7  "bring amrit"; amrit = drink of forever life


SNK7 = ((560, 1820, 76, 1, "b", 0.2), (800, 1790, 64, 1, "g", 1.1), (980, 1840, 56, 1, "b", 1.9))


def s_bring(cr, t, tl, t0, t1):
    c = cues(tl, "sn7")
    tS, tA, tD, tN = c["S"], c["A"], c["D"], c["N"]
    glow(cr, 540, 1300, 680, 0.42)
    ground(cr)
    for i, (x, y, w0, face, pal, ph) in enumerate(SNK7):
        talk = talking(t, t0, tD) and i == 0
        tn = tng_flick(t, 2.0 * w0, 0.0, ph) if not talk else None
        raised(cr, t, x, y, w0, -1, pal, 1.0, 0.0, ph, tn, head=f"sn_snake_{pal}_open" if talk else None,
               look=-0.1)
    bx, by, bs = 440, 1080, 0.82
    ba = think(cr, t, tS - 0.1, bx, by, bs, t_out=tD - 0.1)
    if ba > 0.3:                                        # in the bubble: heaven's clouds, the glowing pot
        cr.save()
        bubble_clip(cr, bx, by - 14, bs)
        for i, (dx, dy) in enumerate(((-150, 70), (130, 80), (0, 100))):
            prop(cr, "rr_lcloud", bx + dx * bs, by + dy * bs, 0.5 * bs, alpha=ba)
        amrit(cr, t, bx, by + 80 * bs, 0.36 * bs * clamp((t - tA + 0.2) / 0.3), alpha=ba)
        cr.restore()

    def ui(cr):
        if t < tD - 0.1:
            head2(cr, t, "THE SNAKES SAID:", t0 + 0.05, "BRING AMRIT!", tA, big_size=250)
        else:
            head2(cr, t, "DRINK IT, AND YOU", tD - 0.1, "NEVER DIE", tN, big_size=270, under=tN + 0.4)
        if t > tD - 0.2:
            word_card(cr, t, tD - 0.2, AMRIT_W, "AMRIT", ["DRINK OF", "FOREVER LIFE"], 540, 960, 0.95,
                      t_lines=tD + 0.15)
    return dict(ui=ui, flash=flash_at(t, tA, 0.2) + flash_at(t, tD, 0.2))


# ------------------------------------------------------------------ sn8  to heaven; the guards; the pot; not one sip


GATE = (790, 0.6)
GUARDS = ((560, 0.5, 0.2), (720, 0.52, 1.1), (900, 0.5, 2.0))


def heaven(cr, t, alpha=1.0, gate=True):
    """Heaven: a golden glow, slow rays behind the gold gate, a floor of light clouds."""
    glow(cr, 620, 1150, 720, 0.55 * alpha)
    gx, gs = GATE
    aura(cr, t, gx, 1250, 160, 860, 0.35 * alpha, n=22, spin=0.05)
    if gate:
        prop(cr, "arch", gx, G + 30, gs, alpha=alpha)
    cloud_floor(cr, t, G + 10, alpha)


def s_heaven(cr, t, tl, t0, t1):
    c = cues(tl, "sn8")
    tF, tH, tG, tD = c["F"], c["H"], c["G"], c["D"]
    heaven(cr, t)
    fallen = []
    for i, (x, s, ph) in enumerate(GUARDS):
        th = tG + (tD - tG) * (0.2 + 0.4 * i)           # when Garuda's flash reaches this guard
        hit = prog(t, th, 0.5)
        b, k, a = depth(t, t0 - 0.4, 0.4, t_out=th + 0.15, out_dur=0.6)
        guard(cr, t, x + 120 * hit, s * k, alpha=a, blur=b, rot=0.5 * hit, ph=ph, feet=G + 20 - 60 * hit)
        fallen.append((th, x, G - 300 * s))
    # Garuda: flies in from the top left, hovers, then dashes past the guards to the gate
    if t < tG:
        u = ease(clamp((t - t0 + 0.1) / max(0.8, tH - t0 + 0.4)))
        x, y = -200 + (300 + 200) * u, 820 + (1300 - 820) * u
        tilt = -0.25 * (1 - u)
    else:
        u = ease(clamp((t - tG) / max(0.6, tD + 0.5 - tG)))
        x, y = 300 + (760 - 300) * u, 1300 + 150 * math.sin(math.pi * u)
        tilt = 0.1
    garuda_fly(cr, t, x, y + 10 * math.sin(t * 3), 0.55, mood="angry" if t > tG else "calm", tilt=tilt, ph=0.3)
    if t > tG:
        trail(cr, [(300 + (x - 300) * k / 20, 1300 + 150 * math.sin(math.pi * k / 20 * u)) for k in range(21)],
              0.6 * (1 - prog(t, tD + 0.8, 0.5)), 0.7)
    white = 0.0
    for th, gx_, gy_ in fallen:
        if t > th:
            burst(cr, t, gx_, gy_, th, n=14, rmax=420, alpha=0.7)
            white = max(white, 0.4 * math.exp(-10 * (t - th)))

    def ui(cr):
        if t < tG - 0.1:
            head2(cr, t, "GARUDA FLEW UP TO", t0 + 0.05, "HEAVEN", tH, big_size=290)
        else:
            head2(cr, t, "HE BEAT ALL THE", tG - 0.1, "GUARDS", tD, big_size=300)
        tag(cr, t, tG - 0.3, "THE GUARDS", 730, 1050, 36, t_out=tD)
    return dict(ui=ui, white=white, flash=flash_at(t, tF, 0.15) + flash_at(t, tH, 0.2))


GA8 = (300, 0.68)
POT8 = (680, G - 70, 0.55)          # the pot on its lotus: x, bottom y, scale


def s_grab(cr, t, tl, t0, t1):
    c = cues(tl, "sn8")
    tP, tU, tB = c["P"], c["U"], c["B"]
    heaven(cr, t, gate=False)
    gx_, gs_ = GATE
    prop(cr, "arch", gx_ + 60, G + 30, gs_, alpha=0.5, blur=5)
    px, py, ps = POT8
    prop(cr, "md_lotus", px, py + 40, 0.6, rot=sway(t, 0.006, 0.4))
    gx, gs = GA8
    lift = keyed(t, [(t0, 0.0), (tU, 1.0)], 0.3, 1.3)
    away = keyed(t, [(t0, 0.0), (tB - 0.1, 1.0)], 0.3, 1.3)
    walk_x = gx + (px - 170 - gx) * ease(clamp((t - t0) / max(0.6, tU - t0 - 0.1)))
    if lift < 0.02:
        pts = garuda(cr, t, walk_x, gs, mood="calm", front=(-1.2, -0.4), ph=0.6, flap=0.15)
        amrit(cr, t, px, py, ps, glow_a=1.0)
    else:
        fr = mix((-1.2, -0.4), (-2.75, -0.2), lift)
        fr = mix(fr, (-1.15, 0.05), away)
        pts = garuda(cr, t, walk_x, gs, mood="calm", front=fr, backa=mix((-1.1, -1.2), (0.3, -0.3), away), ph=0.6,
                     flap=0.3 * lift * (1 - away), spread=0.25 * lift, head=-0.16 * away, hits=[(tU, 0.5)])
        hand = to_user(cr, pts["handF"])
        amrit(cr, t, hand[0] + 6, hand[1] + 70 * ps / 0.55, ps * 0.9, glow_a=1.0)
    beak = to_user(cr, pts["beak"])

    def ui(cr):
        if t < tB - 0.1:
            head2(cr, t, "AND HE TOOK THE", tP - 0.1, "AMRIT POT", tU, big_size=260)
        else:
            head2(cr, t, "BUT HE DRANK", tB - 0.1, "NOT ONE SIP!", tB + 0.2, big_size=250, under=tB + 0.6)
        if t > tB - 0.05:                               # a drop by his beak in a red "no" sign
            no_sign(cr, t, tB - 0.05, beak[0] + 90, beak[1] - 170, 82)
    return dict(ui=ui, flash=flash_at(t, tU, 0.3) + flash_at(t, tB, 0.2))


def no_sign(cr, t, t_in, x, y, r, alpha=1.0):
    """A drop of amrit inside a red circle with a slash: no drinking."""
    q = back(clamp((t - t_in) / 0.3), 1.6)
    if q <= 0.01:
        return
    a = clamp(q) * alpha
    cr.save()
    cr.translate(x, y)
    cr.scale(q, q)
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.set_source_rgba(0.98, 0.92, 0.76, 0.85 * a)
    cr.fill()
    prop(cr, "sn_drop", 0, 6, 1.25, alpha=a)
    cr.set_source_rgba(*RED, 0.95 * a)
    cr.set_line_width(13)
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.stroke()
    p = prog(t, t_in + 0.25, 0.25)
    if p > 0:
        d = r * 0.72
        cr.move_to(-d, -d)
        cr.line_to(-d + 2 * d * p, -d + 2 * d * p)
        cr.stroke()
    cr.restore()


# ------------------------------------------------------------------ sn9  Indra: "don't give it to the snakes!"


GA9 = (250, 0.66)
IN9 = (830, 0.68)


def held_pot(cr, t, pts, s, glow_a=0.8):
    hand = to_user(cr, pts["handF"])
    amrit(cr, t, hand[0] + 6, hand[1] + 70 * s / 0.66, 0.5 * s / 0.66, glow_a=glow_a)


def s_indra(cr, t, tl, t0, t1):
    c = cues(tl, "sn9")
    tI, tR, tS = c["I"], c["R"], c["S"]
    heaven(cr, t, alpha=0.8, gate=False)
    gx, gs = GA9
    gp = garuda(cr, t, gx, gs, mood="calm" if t < tR else "angry", front=(-1.75, -0.2), backa=(-0.4, -0.7),
                ph=0.6, hits=[(tR, 0.3)], head=-0.04)
    held_pot(cr, t, gp, gs)
    ix, is_ = IN9
    t_in = tI - 0.25
    b, k, a = depth(t, t_in, 0.35)
    if t > t_in - 0.1:
        glow(cr, ix, 1250, 600, 0.6 * a)
        burst(cr, t, ix, 1200, t_in, n=18, rmax=560, alpha=0.6)
        stop = keyed(t, [(t0, 0.0), (tR - 0.1, 1.0)], 0.25, 1.4)
        indra(cr, t, ix, is_ * k, front=mix((-0.6, -0.9), (-1.6, -1.35), stop), alpha=a, blur=b, ph=1.1,
                   hits=[(tR, 0.4)])

    def ui(cr):
        if t < tR - 0.1:
            head2(cr, t, "THE KING OF THE GODS,", t0 + 0.05, "INDRA", tI, big_size=300)
        else:
            head2(cr, t, "DON'T GIVE AMRIT", tR - 0.1, "TO SNAKES!", tS, big_size=270)
        tag(cr, t, tI + 0.1, "INDRA", 560, 860, 44, t_out=tR + 0.2)
        plate(cr, t, tI + 0.35, "KING OF THE GODS", 560, 932, 30, t_out=tR + 0.2)
        if t > tR + 0.1:                                # a picture speech cloud: pot -> snake, crossed out
            q = back(clamp((t - tR - 0.1) / 0.3), 1.6)
            cx, cy = 560, 800
            prop(cr, "lr_scloud", cx, cy, 0.85 * (0.6 + 0.4 * q), rot=sway(t, 0.008, 0.5), alpha=clamp(q), flip=True)
            if q > 0.7:
                amrit(cr, t, cx - 150, cy + 70, 0.26, glow_a=0.4)
                dotted(cr, [(cx - 90, cy - 20), (cx + 30, cy - 20)], prog(t, tR + 0.3, 0.3), 20, 6, RED)
                prop(cr, "sn_snake_b", cx + 60, cy - 10, 0.6)
                big_x(cr, cx + 20, cy - 16, 300, 170, prog(t, tS, 0.3), alpha=0.95, lw=16)
    return dict(ui=ui, flash=flash_at(t, t_in, 0.35) + flash_at(t, tS, 0.2))


# ------------------------------------------------------------------ sn9q  save mom AND keep the amrit?


def s_question(cr, t, tl, t0, t1):
    c = cues(tl, "sn9q")
    tW, tM, tA = c["W"], c["M"], c["A"]
    glow(cr, 540, 1400, 560, 0.4)
    ground(cr)
    gp = garuda(cr, t, 540, 0.5, mood="calm", front=(-1.75, -0.2), backa=(-0.6, -1.5), head=0.12 + 0.04 * math.sin(t),
                ph=0.6)
    held_pot(cr, t, gp, 0.5, glow_a=0.6)

    def ui(cr):
        head2(cr, t, "NOW WHAT?", t0 + 0.05, None, 0.0)
        qmark(cr, t, tW - 0.1, 540, 620, 300, RED)
        card2(cr, t, tW, 540, 930, 1.08, [("SAVE MOM", 84, INK, -52, tM), ("& KEEP AMRIT?", 92, RED, 38, tA)])
    return dict(ui=ui, flash=flash_at(t, tW, 0.15) + flash_at(t, tA, 0.2), night=0.1)


# ------------------------------------------------------------------ sn10  the plan: put it down; Indra takes it back


GA10 = (380, 0.6)
IN10 = (730, 0.6)
PLAN = (540, 800, 900, 330)          # the plan board: centre x, y, width, height


def plan_board(cr, t, tP, tD, tY, alpha=1.0):
    """The plan on a parchment board: 1, the pot goes down on the grass (a red arrow down); 2, Indra lifts it away
    (a red arrow up)."""
    x, y, w, h = PLAN
    q = back(clamp((t - tP + 0.2) / 0.35), 1.4)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    yy = y + 50 * (1 - q)
    board(cr, x, yy, w, h, a)
    cr.set_source_rgba(*pc.INK, 0.5 * a)
    cr.set_line_width(3)
    cr.move_to(x, yy - h / 2 + 30)
    cr.line_to(x, yy + h / 2 - 30)
    cr.stroke()
    l1, l2 = x - w / 4, x + w / 4
    gy = yy + h / 2 - 40
    for lx, num in ((l1, "1"), (l2, "2")):
        draw_text(cr, num, lx - w / 4 + 34, yy - h / 2 + 40, 44, RED, a, anchor="cm")
        prop(cr, "sn_kusha_back", lx, gy, 0.22, alpha=a)
    d = ease(clamp((t - tD) / 0.6))                      # 1: the pot comes down onto the grass
    prop(cr, "sn_amrit", l1, gy - 18 - 120 * (1 - d), 0.34, alpha=a)
    down_arrow(cr, l1 + 120, yy - 110, yy + 30, prog(t, tD - 0.1, 0.4), a, w=12)
    if t > tY - 0.2:                                     # 2: Indra lifts it up and away
        up = ease(clamp((t - tY) / 0.8))
        py = gy - 18 - 140 * up
        prop(cr, "sn_amrit", l2, py, 0.34, alpha=a)
        prop(cr, "indra_head", l2 - 80, py - 10, 0.36, alpha=a * prog(t, tY - 0.2, 0.3))
        q2 = prog(t, tY, 0.4)
        if q2 > 0:
            cr.save()
            cr.set_source_rgba(*RED, 0.95 * a)
            cr.set_line_width(12)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            ax, y0, y1 = l2 + 130, yy + 40, yy - 110
            ye = y0 + (y1 - y0) * q2
            cr.move_to(ax, y0)
            cr.line_to(ax, ye + 20)
            cr.stroke()
            if q2 > 0.6:
                pc.poly(cr, [(ax - 28, ye + 30), (ax + 28, ye + 30), (ax, ye - 16)])
                cr.fill()
            cr.restore()


def s_plan(cr, t, tl, t0, t1):
    c = cues(tl, "sn10")
    tC, tI, tP, tD, tY = c["C"], c["I"], c["P"], c["D"], c["Y"]
    glow(cr, 540, 1350, 640, 0.42)
    ground(cr)
    lean = prog(t, tI - 0.2, 0.5)
    ix, is_ = IN10
    indra(cr, t, ix, is_, front=(-0.6, -0.9), head=0.1 * lean, ph=1.1, glow_a=0.4, rot=-0.04 * lean)
    gx, gs = GA10
    idea = keyed(t, [(t0, 0.0), (tC, 1.0), (tI, 0.0)], 0.3, 1.4)
    fr = mix((-0.5, -0.6), (-2.6, -0.3), idea) if t < tI else (-1.5, -1.9)
    gp = garuda(cr, t, gx + 40 * lean, gs, mood="talk" if talking(t, tI, t1 - 0.3) else ("smile" if t > tC else "calm"),
                front=fr, rot=0.08 * lean, head=0.08 * lean, ph=0.6, hits=[(tC, 0.4)])
    if tC < t < tI + 0.4:                               # the idea: a little light over his head
        top = to_user(cr, gp["top"])
        sparkle(cr, top[0] + 40, top[1] + 20, 60 * (0.8 + 0.2 * math.sin(t * 8)), 1 - prog(t, tI, 0.4))
        glow(cr, top[0] + 40, top[1] + 20, 160, 0.5 * (1 - prog(t, tI, 0.4)))
    plan_board(cr, t, tP, tD, tY)
    beak = to_user(cr, gp["beak"])

    def ui(cr):
        if t < tP - 0.1:
            head2(cr, t, "GARUDA HAD A", t0 + 0.05, "CLEVER PLAN", tC, big_size=260)
        elif t < tY - 0.1:
            head2(cr, t, "I'LL PUT THE POT", tP - 0.1, "DOWN...", tD, big_size=280)
        else:
            head2(cr, t, "THEN YOU TAKE IT BACK,", tY - 0.1, "SECRETLY!", tY + 0.1, big_size=270)
        plate(cr, t, tI + 0.2, "SHH!", beak[0] - 30, beak[1] - 150, 40)
    return dict(ui=ui, flash=flash_at(t, tC, 0.2) + flash_at(t, tP, 0.15) + flash_at(t, tY, 0.15))


# ------------------------------------------------------------------ sn11  the pot on the kusha grass


KU = (700, G, 0.75)                  # the kusha patch: x, ground, scale
POT_ON = (655, G - 40, 0.46)         # the pot standing on it: x, bottom y, scale


def s_kusha(cr, t, tl, t0, t1):
    c = cues(tl, "sn11")
    tP, tK, tS, tR = c["P"], c["K"], c["S"], c["R"]
    glow(cr, 540, 1400, 640, 0.42)
    ground(cr)
    kx, ky, ks = KU
    kusha(cr, t, kx, ky, ks, "back")
    px, py, ps = POT_ON
    gs = 0.66
    t_k = tK + 0.3
    kneel = t > t_k                                     # he kneels by the grass and sets the pot down on it
    down = ease(clamp((t - t_k) / max(0.5, tR - t_k)))
    gx = 220 + 210 * ease(clamp((t - t0) / max(0.5, t_k - t0)))
    hold = (gx + 171, 1350 + 300 * ps)                  # the pot's bottom while he carries it
    bx, by = hold[0] + (px - hold[0]) * down, hold[1] + (py - hold[1]) * down
    neck = (bx + 4, by - 300 * ps)
    hip = G - (250 if kneel else 434) * gs
    fr = reach_arm(gx, hip, gs, 26 * 1.28, neck)
    garuda(cr, t, gx, gs, mood="smile" if t > tR else "calm", front=fr, backa=(0.2, -0.4), ph=0.6,
           y=hip, head=0.12 * down, hits=[(tK, 0.3)], kneel=kneel)
    amrit(cr, t, bx, by, ps)
    kusha(cr, t, kx, ky, ks, "front")
    tips = blade_tips(kx, ky, ks)

    def ui(cr):
        head2(cr, t, "HE PUT THE POT ON", t0 + 0.05, "KUSHA GRASS", tK, big_size=250)
        word_card(cr, t, tK - 0.2, KUSHA_W, "KUSHA", ["SHARP GRASS"], 540, 820, 0.82, t_lines=tK + 0.2)
        if t > tS - 0.1:                                 # the sharp tips glint
            for i, (x, y) in enumerate(tips):
                q = prog(t, tS + 0.07 * i, 0.25)
                sparkle(cr, x, y + 6, 30 * q * (0.8 + 0.2 * math.sin(t * 9 + i)), q)
            tx, ty = tips[6]
            red_ring(cr, tx, ty + 40, 60, 90, prog(t, tS + 0.1, 0.35), 8)
            plate(cr, t, tS + 0.3, "SHARP!", tx - 40, ty + 175, 40)
    return dict(ui=ui, flash=flash_at(t, tK, 0.2) + flash_at(t, tR, 0.15))


# ------------------------------------------------------------------ sn12  "here's amrit! but bathe first"; mother free


KU12 = (470, G, 0.6)
SNK12 = ((800, 1815, 56, -1, "b", 0.4), (930, 1765, 50, -1, "g", 1.3), (1050, 1830, 46, -1, "b", 2.1))


def pot_patch(cr, t, kx, ky, ks, pot=1.0, glow_a=1.0, alpha=1.0):
    """The kusha patch with the pot standing on it (pot 0..1 its alpha)."""
    kusha(cr, t, kx, ky, ks, "back", alpha=alpha)
    if pot > 0.01:
        amrit(cr, t, kx, ky - 55 * ks, 0.5 * ks / 0.95, glow_a=glow_a, alpha=pot * alpha)
    kusha(cr, t, kx, ky, ks, "front", alpha=alpha)


def river(cr, t, x0=760, alpha=1.0):
    """A river behind the ground on the right (it fades in from the left): rolling strips of water."""
    cr.push_group()
    cr.rectangle(0, 1540, W, G + 40 - 1540)
    cr.clip()
    for k in range(2):
        sh = 14 * math.sin(t * (0.7 + 0.2 * k) + k)
        prop(cr, "sx_wave2" if k == 0 else "sx_wave", x0 + 420 + sh, 1590 + 80 * k, 0.42, alpha=0.85 * alpha)
    pat = cr.pop_group()
    g = cairo.LinearGradient(x0 - 140, 0, x0 + 60, 0)
    g.add_color_stop_rgba(0, 0, 0, 0, 0.0)
    g.add_color_stop_rgba(1, 0, 0, 0, 1.0)
    cr.save()
    cr.set_source(pat)
    cr.mask(g)
    cr.restore()


def s_bathe(cr, t, tl, t0, t1):
    c = cues(tl, "sn12")
    tL, tB, tP = c["L"], c["B"], c["P"]
    glow(cr, 540, 1350, 660, 0.42)
    ground(cr)
    kx, ky, ks = KU12
    pot_patch(cr, t, kx, ky, ks)
    point = keyed(t, [(t0, 0.0), (tL, 1.0), (tB, 2.0)], 0.3, 1.4)
    fr = (-0.5, -0.6) if point < 0.5 else ((-1.25, -0.3) if point < 1.5 else (-2.2, -0.25))
    garuda(cr, t, 215, 0.62, mood="talk" if talking(t, tL - 0.2, t1) else "calm", front=fr, ph=0.6,
           hits=[(tL, 0.4), (tB, 0.4)])
    look = 0.0 if t < tB else -0.3
    snakes_by(cr, t, SNK12, bob=0.6 if tL < t < tB else 0.0, look=look)

    def ui(cr):
        if t < tB - 0.1:
            head2(cr, t, "HERE'S", tL - 0.2, "THE AMRIT!", tL, big_size=270)
        else:
            head2(cr, t, "BUT FIRST,", tB - 0.1, "GO BATHE!", tB + 0.05, big_size=300)
        if t > tB - 0.1:
            cloud_text(cr, t, 480, 900, 0.62, [("BATHE FIRST,", 50, INK, -26, tB), ("THEN DRINK!", 58, RED, 36, tP)],
                       t_in=tB - 0.1)
        else:
            cloud_text(cr, t, 480, 900, 0.62, [("HERE'S", 50, INK, -26, tL), ("AMRIT!", 64, RED, 36, tL + 0.1)],
                       t_in=tL - 0.1)
    return dict(ui=ui, flash=flash_at(t, tL, 0.15) + flash_at(t, tB, 0.2))


def broom_fall(cr, t, t_drop, x, y, s):
    """The broom she lets go of: it tips over and lands flat on the ground."""
    u = clamp((t - t_drop) / 0.5)
    rot = 0.4 + (1.45 - 0.4) * (u * u)
    prop(cr, "sn_broom", x + 140 * s * u, y + (G - 40 - y) * u * u, 0.92 * s, rot=rot)


def s_free(cr, t, tl, t0, t1):
    c = cues(tl, "sn12")
    tM, tF = c["M"], c["F"]
    glow(cr, 420, 1300, 660, 0.42 + 0.3 * prog(t, tF, 0.6))
    ground(cr)
    t_drop = tM + 0.15
    free = prog(t, tF - 0.1, 0.5)
    vx, vs = 360, 0.62
    if free > 0.01:
        glow(cr, vx, 1350, 520, 0.5 * free)
        aura(cr, t, vx + 10, 1290, 120, 520, 0.45 * free, n=16, spin=0.2)
    vp = vinata(cr, t, vx, vs, mood="joy" if t > tF - 0.1 else ("calm" if t > t_drop else "sad"),
                sweep=1 - prog(t, t_drop - 0.2, 0.4), broom_drop=t_drop, ph=0.3,
                front=mix((-0.3, -0.5), (-2.5, -0.4), free), backa=mix((0.2, -0.3), (-2.3, -0.5), free),
                hits=[(t_drop, 0.4), (tF, 0.5)])
    if t > t_drop:
        broom_fall(cr, t, t_drop, vx + 70, G - 330, vs)
    garuda(cr, t, 720, 0.66, mood="smile", flip=True, front=(-1.2, -0.5), ph=0.6, spread=0.2 * free, flap=0.2 * free)
    if t > tF:
        ch = to_user(cr, vp["chest"])
        burst(cr, t, ch[0], ch[1] - 80, tF, n=18, rmax=560, alpha=0.6)
        lights(cr, t, ch[0], ch[1] - 100, 260, 10, 0.8 * free)

    def ui(cr):
        head2(cr, t, "AND MY MOTHER", tM - 0.05, "IS FREE!", tF, big_size=300, under=tF + 0.4)
    return dict(ui=ui, flash=flash_at(t, tF, 0.3))


# ------------------------------------------------------------------ sn13  the snakes go to bathe; Indra takes it


KU13 = (400, G, 0.6)


def s_takeback(cr, t, tl, t0, t1):
    c = cues(tl, "sn13")
    tH, tP, tI, tU, tS = c["H"], c["P"], c["I"], c["U"], c["S"]
    glow(cr, 540, 1350, 660, 0.42)
    river(cr, t, 760)
    ground(cr)
    kx, ky, ks = KU13
    up = ease(clamp((t - tU) / max(0.6, tS + 0.6 - tU)))
    pot_on = t < tU
    pot_patch(cr, t, kx, ky, ks, pot=1.0 if pot_on else 0.0)
    for i, (y, w0, pal, dl) in enumerate(((1800, 50, "b", 0.0), (1755, 46, "g", 0.3), (1835, 42, "b", 0.6))):
        t_end = tH + 1.5 + dl                           # they slither off into the river
        gone = prog(t, t_end - 0.5, 0.5)
        if gone < 1:
            slither(cr, t, t0 + dl - 0.3, t_end, 640 - 70 * i, 1060 + 40 * i, y, w0, pal, i, tng_flick(t, 70, 0.0, i),
                    alpha=1 - gone)
        if 0 < t - t_end + 0.4 < 0.8:                   # a splash
            q = (t - t_end + 0.4) / 0.8
            for k in range(5):
                prop(cr, "sn_drop", 960 + 40 * i + (k - 2) * 30 * (1 + q), y - 140 * math.sin(math.pi * q) - 10 * k,
                     0.4, alpha=1 - q)
    if t > tI - 0.3:                                    # Indra flashes in behind, lifts the pot, rises away
        b, k, a = depth(t, tI - 0.3, 0.35)
        lift = keyed(t, [(t0, 0.0), (tU - 0.1, 1.0)], 0.25, 1.3)
        iy = G - 434 * 0.6 - 700 * up * up
        fade = 1 - clamp((up - 0.4) / 0.4)
        ip = indra(cr, t, kx - 170, 0.6 * k, front=mix((-0.8, -0.6), (-1.6, -0.1), lift), alpha=a * fade, blur=b,
                   flip=False, y=iy, ph=1.1, rods=up < 0.2, vajra=True)
        if not pot_on:
            hand = to_user(cr, ip["handF"])
            amrit(cr, t, hand[0] + 6, hand[1] + 70, 0.38, alpha=fade)
        glow(cr, kx - 170, 1300 - 700 * up * up, 520, 0.5 * a * fade)
        burst(cr, t, kx - 150, 1350, tI - 0.3, n=16, rmax=520, alpha=0.5)
    if t > tU - 0.2:                                    # he rises into the clouds, back to heaven
        for i in range(3):
            prop(cr, "rr_lcloud", 90 + 300 * i, 1000 + 30 * (i % 2), 0.95, rot=sway(t, 0.01, 0.4, i),
                 alpha=prog(t, tU - 0.2, 0.4) * 0.95)

    def ui(cr):
        if t < tI - 0.1:
            head2(cr, t, "THE SNAKES WENT TO", t0 + 0.05, "BATHE", tH, big_size=300)
        else:
            head2(cr, t, "AND BEHIND THEM, INDRA", tI - 0.1, "TOOK IT BACK!", tU, big_size=240, under=tS + 0.2)
        plate(cr, t, tH + 0.3, "RIVER", 960, 1650, 38)
    return dict(ui=ui, flash=flash_at(t, tI - 0.3, 0.35) + flash_at(t, tS, 0.2))


# ------------------------------------------------------------------ sn14  the snakes come back: pot gone!


KU14 = (380, G, 0.6)
SNK14 = ((790, 1815, 58, -1, "b", 0.4), (930, 1765, 52, -1, "g", 1.3), (1050, 1830, 48, -1, "b", 2.1))


def s_gone(cr, t, tl, t0, t1):
    c = cues(tl, "sn14")
    tL, tG, tT, tD = c["L"], c["G"], c["T"], c["D"]
    glow(cr, 540, 1350, 660, 0.42)
    ground(cr)
    kx, ky, ks = KU14
    pot_patch(cr, t, kx, ky, ks, pot=0.0)
    back_in = ease(clamp((t - t0 + 0.2) / max(0.8, tL + 0.6 - t0)))
    shocked = t > tG
    specs = [(x + 300 * (1 - back_in), y, w0, f, pal, ph) for x, y, w0, f, pal, ph in SNK14]
    heads = snakes_by(cr, t, specs, bob=0.0, tng=not shocked, look=0.12 if shocked else 0.0)
    for i, hd in enumerate(heads):                      # dripping wet from their bath
        if hd and t < tG + 1.5:
            u = (t * 1.6 + i * 0.37) % 1.0
            hx, hy = hd["head"]
            prop(cr, "sn_drop", hx - 10, hy + 40 + 80 * u, 0.32, alpha=0.8 * (1 - u))
    tips = blade_tips(kx, ky, ks)
    glint = prog(t, tT, 0.5)
    drops(cr, t, [(x, y + 60) for x, y in tips[1:7:2]], glint)
    bx, by, bs = 700, 1080, 0.62
    ba = think(cr, t, tT, bx, by, bs, flip=False)
    if ba > 0.3:
        cr.save()
        bubble_clip(cr, bx, by - 14, bs)
        prop(cr, "sn_kusha_back", bx, by + 120 * bs, 0.3, alpha=ba)
        drops(cr, t, [(bx - 60 * bs, by - 40 * bs), (bx + 40 * bs, by - 80 * bs), (bx + 100 * bs, by - 10 * bs)],
              ba, 0.5)
        cr.restore()

    def ui(cr):
        if t < tT - 0.1:
            head2(cr, t, "THE SNAKES CAME BACK...", t0 + 0.05, "POT GONE!", tG, big_size=300)
        else:
            head2(cr, t, "MAYBE A FEW DROPS", tT - 0.1, "FELL ON THE GRASS?", tD, big_size=170)
        if t > tG - 0.1:                                 # a dotted outline where the pot stood, a "?"
            q = prog(t, tG - 0.1, 0.3) * (1 - 0.5 * prog(t, tT, 0.4))
            cx, cy = kx, ky - 55 * ks - 170
            pts = [(cx + 130 * math.cos(a_), cy + 140 * math.sin(a_))
                   for a_ in (i / 40 * 2 * math.pi for i in range(41))]
            dotted(cr, pts, prog(t, tG - 0.1, 0.5), 22, 5, RED, q)
            qmark(cr, t, tG, cx, cy, 170, RED, q)
    return dict(ui=ui, flash=flash_at(t, tG, 0.25) + flash_at(t, tT, 0.15))


# ------------------------------------------------------------------ sn15  they lick the sharp grass; tongues split


LICK = ((1, 400, 70, "b", 1, 95, 0.0, -0.45), (6, 400, 70, "g", -1, 1000, 0.9, math.pi + 0.45),
        (10, 160, 60, "b", 1, 300, 1.7, -0.55))   # (blade, distance up it, neck width, palette, facing, coil x, ...


def s_lick(cr, t, tl, t0, t1):
    c = cues(tl, "sn15")
    tS, tL = c["S"], c["L"]
    glow(cr, 540, 1350, 660, 0.42)
    ground(cr)
    kx, ky, ks = 540, G, 1.0
    kusha(cr, t, kx, ky, ks, "back")
    kusha(cr, t, kx, ky, ks, "front")
    tips = blade_tips(kx, ky, ks)
    lick = prog(t, tL - 0.2, 0.3)
    for i, (bi, d, w0, pal, face, cx, ph, hd) in enumerate(LICK):   # ... phase, head direction)
        bx, L_, a_ = SC._BACK[bi]
        u = math.sin(t * 3.4 + ph) * lick                 # the head slides up and down the blade
        dd = d + 70 * u
        px = kx + ks * (bx * 0.5 + dd * math.sin(a_))
        py = ky + ks * (-8 - dd * math.cos(a_))
        reach = 2.14 * w0 + 0.75 * w0
        hx, hy = px - math.cos(hd) * reach, py - math.sin(hd) * reach
        sp = spine_coil(cx, G + 12, 2.3 * w0, face, (hx, hy), turns=1.3, stack=0.45 * w0, arch=0.5 * w0)
        tn = (w0 * (0.8 + 0.25 * math.sin(t * 9 + ph)) * lick, 0.0, 0.6, 0.0) if lick > 0 else \
            tng_flick(t, 1.6 * w0, 0.0, ph)
        naga(cr, t, sp, w0, pal, face, alpha=1.0, tng=tn, head_dir=hd)

    def ui(cr):
        head2(cr, t, "THEY LICKED THE", t0 + 0.05, "SHARP GRASS", tL, big_size=260)
        if t > tS:
            tx, ty = tips[5]
            red_ring(cr, tx, ty + 50, 60, 90, prog(t, tS + 0.1, 0.35), 8)
            plate(cr, t, tS + 0.3, "SHARP!", tx, ty - 60, 38)
    return dict(ui=ui, flash=flash_at(t, tL, 0.15))


SPLIT_HEAD = (150, 1250, 250)       # the close-up head: neck x, y, neck width (px)
BLADE = (1010, 1960, 0.95, -0.14)   # the big blade: base x, y, scale, rotation


def s_split(cr, t, tl, t0, t1):
    c = cues(tl, "sn15")
    tJ, tC = c["J"], c["C"]
    glow(cr, 560, 1200, 720, 0.45)
    bx, by, bsc, brot = BLADE
    prop(cr, "sn_kusha_blade", bx, by, bsc, rot=brot + sway(t, 0.006, 0.4))
    hx, hy, w0 = SPLIT_HEAD
    spine = hook_spine(hx, hy)
    split = ease(clamp((t - tC + 0.35) / 0.8))           # slow: from the tip back to the middle
    lick = 0.0 if t > tJ else 0.5 + 0.5 * math.sin((t - t0) * 6.0)
    L = 250 + 70 * lick
    sn = naga(cr, t, spine, w0, "b", 1, "sn_snake_big", head_w=300.0, head_rot=0.08 + 0.03 * math.sin(t * 1.2),
              tng=(L, split, 0.75, 0.0), tongue_w=32, tng_kw=dict(flen=0.5, crease=1.0 - split), n=80)
    tips = sn["tips"]
    c_, s_ = math.cos(sn["dir"]), math.sin(sn["dir"])
    r0 = sn["snout"]
    if split > 0.02:                                     # the spark where it comes apart
        fx = r0[0] + c_ * L * (1 - 0.5 * split)
        fy = r0[1] + s_ * L * (1 - 0.5 * split)
        if split < 0.98:
            sparkle(cr, fx, fy, 70, 1.0, (1.0, 0.95, 0.8))
            glow(cr, fx, fy, 160, 0.6)

    def ui(cr):
        if t < tJ - 0.1:
            head2(cr, t, "AND AS THEY LICKED", t0 + 0.05, "AND LICKED...", t0 + 0.6, big_size=230)
        else:
            head2(cr, t, "THEIR TONGUES", tJ - 0.1, "SPLIT!", tC + 0.1, big_size=320, under=tC + 0.6)
        if split > 0.95 and tips and len(tips) == 2:
            mx, my = (tips[0][0] + tips[1][0]) / 2, (tips[0][1] + tips[1][1]) / 2
            red_ring(cr, mx - 40, my, 140, 120, prog(t, tC + 0.45, 0.3), 9)
    return dict(ui=ui, flash=flash_at(t, tC, 0.35))


# ------------------------------------------------------------------ sn16  split forever; kusha holy


ROW16 = ((190, 1790, 54, 1, "b", 0.0), (400, 1820, 54, 1, "g", 0.4), (610, 1780, 54, 1, "b", 0.8),
         (820, 1820, 54, 1, "g", 1.2))


def s_forever(cr, t, tl, t0, t1):
    c = cues(tl, "sn16")
    tE, tD = c["E"], c["D"]
    glow(cr, 540, 1350, 680, 0.42)
    ground(cr)
    tipsets = []
    for i, (x, y, w0, face, pal, ph) in enumerate(ROW16):
        b, k, a = depth(t, t0 - 0.3 + 0.12 * i, 0.4)
        hold = tD - 0.05 < t < tD + 1.2
        f = 1.0 if hold else flick(t, ph, 1.1)
        out = raised(cr, t, x - 110, y, w0 * k, face, pal, 1.0, 0.0, ph, (2.1 * w0 * f, 1.0, 0.7,
                                                                            0.1 * math.sin(t * 40 + ph) * (not hold)),
                     alpha=a)
        if out and out["tips"]:
            tipsets.append(out["tips"])

    def ui(cr):
        head2(cr, t, "SINCE THEN:", t0 + 0.05, "SPLIT FOREVER", tD, big_size=250)
        plate(cr, t, tE + 0.1, "EVERY SNAKE!", 540, 1300, 40)
        if tD - 0.05 < t < tD + 1.4:
            for tp in tipsets:
                if len(tp) == 2:
                    mx, my = (tp[0][0] + tp[1][0]) / 2, (tp[0][1] + tp[1][1]) / 2
                    red_ring(cr, mx, my, 46, 40, prog(t, tD, 0.35), 6, 1 - prog(t, tD + 1.1, 0.3))
    return dict(ui=ui, flash=flash_at(t, tD, 0.2))


def s_puja(cr, t, tl, t0, t1):
    c = cues(tl, "sn16")
    tK, tP, tV = c["K"], c["P"], c["V"]
    glow(cr, 540, 1400, 640, 0.5)
    ground(cr)
    holy = prog(t, tV - 0.1, 0.6)
    at = G + 14 - 90 * 2.6                              # the top of the brick altar the puja is laid on
    prop(cr, "altar", 540, G + 14, 2.6)
    diya(cr, t, 165, at + 4, 1.15, lit=1.0)
    prop(cr, "md_kalasha", 928, at + 2, 0.6)
    prop(cr, "sn_thali", 530, at + 6, 1.15)
    kx, ky = 548, at - 62
    glow(cr, kx + 40, ky, 520, 0.3 + 0.5 * holy)
    aura(cr, t, kx + 40, ky, 100, 520, 0.6 * holy, n=18, spin=0.2)
    prop(cr, "sn_kusha_bundle", kx, ky, 1.0, rot=-0.04 + sway(t, 0.006, 0.4))
    lights(cr, t, kx + 40, ky - 80, 320, 10, 0.8 * holy)
    if tK < t:
        sparkle(cr, kx + 300, ky - 12, 50 * (0.8 + 0.2 * math.sin(t * 7)), prog(t, tK, 0.3))

    def ui(cr):
        if t < tP - 0.1:
            head2(cr, t, "AND KUSHA GRASS...", tK - 0.1, None, 0.0)
        else:
            head2(cr, t, "AND KUSHA GRASS", tK - 0.1, "BECAME HOLY", tV, big_size=260, under=tV + 0.5)
        tag(cr, t, tK + 0.1, "KUSHA", kx + 40, ky - 260, 46)
        plate(cr, t, tP + 0.1, "USED IN PUJA", 540, 1010, 44)
    return dict(ui=ui, flash=flash_at(t, tK, 0.15) + flash_at(t, tV, 0.25))


# ------------------------------------------------------------------ sn16c  the hook's picture again


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "sn16c")
    tD, tW, tJ, tN = c["D"], c["W"], c["J"], c["N"]
    glow(cr, 420, 1250, 680, 0.42)
    mem = prog(t, tD - 0.1, 0.5) * (1 - prog(t, tJ, 0.6))
    if mem > 0.01:                                       # the cheat, remembered: the horse with the black tail
        mx_, my_, mr = 820, 790, 175
        glow(cr, mx_, my_, 360, 0.35 * mem)
        cr.save()
        cr.arc(mx_, my_, mr, 0, 2 * math.pi)
        cr.set_source_rgba(0.97, 0.87, 0.62, 0.85 * mem)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, 0.8 * mem)
        cr.set_line_width(4.5)
        cr.stroke_preserve()
        cr.clip()
        horse(cr, t, mx_ + 20, my_ + 150, 0.27, black=1.0, alpha=0.9 * mem)
        cr.restore()
    hold = (tN - 0.1, tN + 2.0)
    sn = hook_snake(cr, t, [hold])
    tips = sn["tips"] if sn else None

    def ui(cr):
        if t < tJ - 0.1:
            head2(cr, t, "THEY WON BY", t0 + 0.05, "CHEATING...", tW, big_size=270)
        else:
            head2(cr, t, "AND THE TONGUE", tJ - 0.1, "REMEMBERS", tN, big_size=270, under=tN + 0.4)
        if mem > 0.3:
            plate(cr, t, tD + 0.2, "THE CHEAT", 820, 990, 36, alpha=mem)
        if t > tN - 0.1 and tips and len(tips) == 2:
            mx, my = (tips[0][0] + tips[1][0]) / 2, (tips[0][1] + tips[1][1]) / 2
            red_ring(cr, mx - 6, my, 90, 80, prog(t, tN, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tW, 0.15) + flash_at(t, tN, 0.2))


# ------------------------------------------------------------------ sn17  was Garuda right, or did he cheat too?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "sn17")
    tR, tC = c["R"], c["C"]
    glow(cr, 540, 1420, 520, 0.45)
    ground(cr)
    pts = garuda(cr, t, 540, 0.56, mood="calm", front=(-0.6, -0.9), backa=(0.3, -0.4), ph=0.6, hits=[(tR, 0.3),
                                                                                                   (tC, 0.3)])
    pa = to_user(cr, pts["handF"])
    amrit(cr, t, pa[0] + 6, pa[1] + 60, 0.28, glow_a=0.6)
    raised(cr, t, 930, 1800, 34, -1, "b", 1.0, 0.0, 0.4, tng_flick(t, 80, 1.0, 0.4))
    cards = ((290, ("GARUDA", "WAS RIGHT"), tR - 0.25), (790, ("GARUDA", "CHEATED TOO"), tC - 0.25))

    def ui(cr):
        if t < tC - 0.1:
            head2(cr, t, "SO WAS GARUDA", t0 + 0.05, "RIGHT?", tR, big_size=300)
        else:
            head2(cr, t, "OR DID HE", tC - 0.1, "CHEAT TOO?", tC + 0.05, big_size=280)
        for cx, (l1, l2), tc in cards:
            card(cr, t, tc, cx, 800, 0.62, [(l1, 54, INK, -40), (l2, 74, RED, 34)])
        if t > tR:
            if t < tC:
                k, ts = 0, tR
            else:
                n = int((t - tC) / 0.9)
                k, ts = (1 + n) % 2, tC + 0.9 * n
            red_ring(cr, cards[k][0], 804, 270, 104, prog(t, ts, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tR, 0.15) + flash_at(t, tC, 0.15))


SHOTS = [   # (line, cue: None = line start, draw function, options)
    ("sn1", None, s_hook, {"z": (1.0, 1.04)}),
    ("sn2", None, s_book, {"z": (1.0, 1.03)}),
    ("sn3", None, s_garuda, {"z": (1.0, 1.04)}),
    ("sn3", "उसकी", s_servant, {"z": (1.0, 1.03)}),
    ("sn4", None, s_bet, {"z": (1.0, 1.03)}),
    ("sn5", None, s_wrap, {"z": (1.0, 1.04), "focus": (420, 1400)}),
    ("sn5", "गरुड़", s_lost, {"z": (1.0, 1.03)}),
    ("sn6", None, s_ask, {"z": (1.0, 1.03)}),
    ("sn7", None, s_bring, {"z": (1.0, 1.03)}),
    ("sn8", None, s_heaven, {"z": (1.0, 1.03)}),
    ("sn8", "अमृत", s_grab, {"z": (1.0, 1.03)}),
    ("sn9", None, s_indra, {"z": (1.0, 1.03)}),
    ("sn9q", None, s_question, {"z": (1.0, 1.03)}),
    ("sn10", None, s_plan, {"z": (1.0, 1.03)}),
    ("sn11", None, s_kusha, {"z": (1.0, 1.04), "focus": (560, 1500)}),
    ("sn12", None, s_bathe, {"z": (1.0, 1.03)}),
    ("sn12", "मेरी", s_free, {"z": (1.0, 1.04)}),
    ("sn13", None, s_takeback, {"z": (1.0, 1.03)}),
    ("sn14", None, s_gone, {"z": (1.0, 1.03)}),
    ("sn15", None, s_lick, {"z": (1.0, 1.04), "focus": (540, 1500)}),
    ("sn15", "चाटते", s_split, {"z": (1.0, 1.06), "focus": (700, 1200)}),
    ("sn16", None, s_forever, {"z": (1.0, 1.03)}),
    ("sn16", "कुश", s_puja, {"z": (1.06, 1.12), "focus": (540, 1500)}),
    ("sn16c", None, s_callback, {"z": (1.0, 1.04)}),
    ("sn17", None, s_end, {"z": (1.0, 1.03)}),
]


def _starts(tl):
    """Each shot's start (cached on the timeline under this module's own name, not shots.shot_at's)."""
    st = getattr(tl, "_sn_shot_starts", None)
    if st is None:
        st = []
        for k, (bid, cu, _, _) in enumerate(SHOTS):
            if k == 0:
                st.append(0.0)
                continue
            s = T(tl, bid, cu)
            if cu is not None:
                s -= CUT_LEAD
            st.append(max(s, st[-1] + MIN_SHOT))
        tl._sn_shot_starts = st
    return st


def shot_at(t, tl):
    st = _starts(tl)
    k = max(i for i, s in enumerate(st) if t >= s)
    return k, st[k], st[k + 1] if k + 1 < len(st) else tl.total


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl)
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
    sepia(cr, out.get("sepia", 0.0))
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
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook,
    shimmer as the tongue splits, a hit as Garuda beats the guards, a conch as Indra takes the pot back, a bell on the
    closing question, then (only where it fits) a hit as the tail turns black. Chosen in THAT order of importance,
    each at least SFX_MIN_GAP from every sound already kept (as render_myth.calm_sfx keeps them), so the list returned
    is what plays (about 6 sounds); the bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["sn15"]["C"], "shimmer", 0), (c["sn8"]["D"], "hit", 0),
            (c["sn13"]["U"], "conch", 0), (c["sn17"]["R"], "bell", 0), (c["sn5"]["K"], "hit", 0),
            (c["sn12"]["F"], "bell", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["sn13"]["I"] - 0.35, "dip", 0.5), (c["sn15"]["C"] - 0.35, "dip", 0.5),
            (c["sn5"]["K"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
