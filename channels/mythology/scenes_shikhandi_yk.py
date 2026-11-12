"""Kannada scenes for videos/shikhandi.py, drawn as a Yakshagana stage play (yaksha_kit), so the Kannada reel shares
no pictures with the Hindi shadow-puppet reel (scenes_shikhandi). Cast and props: sy_yk_cast.

One idea a child can hold on to: Amba wears PINK; in her next life Shikhandi the warrior wears the same pink, and
her soul is a pink-gold figure of light that stands behind him. Bhishma is the old warrior in white with a white
beard; Arjuna the archer in green. Battle is light only: arrows are golden streaks, Bhishma sinks gently onto a bed
of arrows shown as a soft row of light and becomes a figure of light himself. No wounds, no flames on anyone: Amba
walks into the light of the sacred fire and is gone in a warm white wash, a pink light rising.

Every frame is a pure function of t. Cues are words of the Kannada line (CUES, exact substrings, MISSES stays empty)
with fraction fallbacks and minimum gaps; the cut list and cues are cached on the timeline under "_sy_" names only.

Shot list (line: what is on the screen)
  b1   HOOK, frame 0: Shikhandi alone and big in pink on the crimson stage, bow at his side: ಭೀಷ್ಮನನ್ನ ಸೋಲಿಸಿದ ಈ
       ಯೋಧ / ಹಿಂದೆ ಹುಡುಗಿ! (in by 0.6 s); a stamp; on "ಭೀಷ್ಮನಂಥ" he raises the bow and draws; on "ಸೋಲಿಸಿದ" the
       arrow flies off as a golden streak; on "ಹಿಂದಿನ" he steps aside and a pink girl of light (Amba's soul) rises
       behind him, tag ಹಿಂದಿನ ಜನ್ಮ; on "ಹುಡುಗಿ" she glows and the big line is underlined in red
  b2   the bhagavata and the chende drummer, big, playing; banner ಇದು ಮಹಾಭಾರತದ / ನಿಜವಾದ ಕಥೆ
  b3   Bhishma alone (white, beard, bow), a stamp with dust: ಭೀಷ್ಮ / ತುಂಬಾ ಶಕ್ತಿಶಾಲಿ; on "ಯಾರೂ" arrows of light fly at
       him from both sides and spark off a golden ring: ಭೀಷ್ಮನಿಗೆ / ಸೋಲೇ ಇಲ್ಲ!
  b4   Amba alone, a princess in pink: ರಾಜಕುಮಾರಿ / ಅಂಬೆ; on "ಬಲವಂತವಾಗಿ" Bhishma holds her wrist and leads her off,
       she pulls back, sad: ಭೀಷ್ಮ ಕರ್ಕೊಂಡು ಬಂದ / ಬಲವಂತವಾಗಿ!; on "ತಮ್ಮನ" his little brother waits with a garland
       (tag ತಮ್ಮ): ತನ್ನ ತಮ್ಮನ / ಮದುವೆಗೆ
  b5   Amba and the king she loved (blue, tag ಬೇರೆ ರಾಜ), a glowing heart: ಅಂಬೆ ಪ್ರೀತಿಸಿದ್ದು / ಬೇರೆ ರಾಜನನ್ನ; on
       "ಹೋದಾಗ" she walks to him with a garland; on "ಹೇಳಿದ" he turns away, palm up, the heart cracks, banner ಈಗ ನಾನು
       ನಿನ್ನನ್ನ / ಮದುವೆ ಆಗಲ್ಲ!; the garland falls
  b6   the stage goes dark blue, Amba alone and small, crying in a pool of light: ಅಂಬೆ / ಒಂಟಿಯಾದ್ಳು; on
       "ಭೀಷ್ಮನಿಂದಾನೇ" Bhishma's huge shadow rises on the backdrop and she turns to it, angry: ಇದೆಲ್ಲ / ಭೀಷ್ಮನಿಂದಾನೇ!
  b7   Amba big, fist up, stamps: ಅಂಬೆಯ ಶಪಥ and the banner ನಾನು ಭೀಷ್ಮನನ್ನ / ಸೋಲಿಸೇ ಸೋಲಿಸ್ತೀನಿ!; a second stamp
  b8   Amba prays before a Shiva linga while suns and moons race over the stage (years): ವರ್ಷಗಟ್ಟಲೆ / ಶಿವನ ಪೂಜೆ;
       on "ಬಂದು" Shiva (blue, crescent moon, trident, tag ಶಿವ) appears in a burst: ಆಗ / ಶಿವ ಬಂದ!; on "ಮುಂದಿನ" his
       words: banner ಮುಂದಿನ ಜನ್ಮದಲ್ಲಿ / ನೀನು ಭೀಷ್ಮನನ್ನ / ಸೋಲಿಸ್ತೀಯ!
  b9   the sacred fire as a tall soft light; Amba walks into it with joined hands: a warm white wash, she is gone,
       a pink light rises: ಅಂಬೆ / ಈ ಜನ್ಮ ಬಿಟ್ಟಳು
  b10  the pink light floats down into a cradle between a king (tag ರಾಜ) and a queen: ಮುಂದಿನ ಜನ್ಮದಲ್ಲಿ / ರಾಜನ
       ಮಗಳು; on "ಶಿಖಂಡಿ" ಹೆಸರು / ಶಿಖಂಡಿ, the baby glows pink
  b11  the forest stage: grown-up Shikhandi, a girl in the same pink (tag ಶಿಖಂಡಿ): ದೊಡ್ಡವಳಾದ ಮೇಲೆ; on "ಮಾಯಾವಿ" a
       green-faced yaksha appears in green light (tag ಮಾಯಾವಿ ಯಕ್ಷ): ಕಾಡಿನ ಒಬ್ಬ / ಮಾಯಾವಿ ಯಕ್ಷ; on "ದೇಹವನ್ನ" a green
       light and a pink light cross: ಯಕ್ಷ ಕೊಟ್ಟ / ಗಂಡಸಿನ ದೇಹ; on "ಕೊಟ್ಟ" she spins in a flash and stands as the
       pink warrior with a bow; on "ಗಂಡು" a stamp: ಈಗ ಶಿಖಂಡಿ / ಗಂಡು ಯೋಧ!
  b12  war: Bhishma draws his bow, enemy arrows of light spark off his golden ring, the drummer plays: ಆಮೇಲೆ /
       ದೊಡ್ಡ ಯುದ್ಧ; on "ಹತ್ತು" a day card counts ದಿನ 1 ... ದಿನ 10: ಹತ್ತು ದಿನ ಆದ್ರೂ / ಭೀಷ್ಮ ಸೋಲಲಿಲ್ಲ!
  b12q QUESTION: a big red "?" over the card ಭೀಷ್ಮನನ್ನ / ಹೇಗೆ ಸೋಲಿಸಿದ್ರು?, Shikhandi small, waiting, looking up
  b13  Bhishma, palm up: ಭೀಷ್ಮನ / ಒಂದು ನಿಯಮ; on "ಹುಡುಗಿಯಾಗಿದ್ದವರ" a girl of light appears at the left, banner
       ಒಮ್ಮೆ ಹುಡುಗಿಯಾಗಿದ್ದವರ ಜೊತೆ / ಯುದ್ಧ ಮಾಡಲ್ಲ!; on "ಯುದ್ಧ" a red X over crossed arrows between them
  b14  a chariot rolls in with Arjuna (tag ಅರ್ಜುನ); on "ಶಿಖಂಡಿಯನ್ನ" Shikhandi steps up to its very front (tag
       ಶಿಖಂಡಿ); on "ಮುಂದೆ" a red pointer ಮುಂದೆ!: ಅರ್ಜುನ, ಶಿಖಂಡಿಯನ್ನ / ಮುಂದೆ ನಿಲ್ಲಿಸಿದ!
  b15  Shikhandi in front with Amba's light behind him, Arjuna behind; Bhishma shuts his eyes and lays his bow on
       the floor: ಭೀಷ್ಮ / ಆಯುಧ ಕೆಳಗಿಟ್ಟ; on "ಅರ್ಜುನನ" golden streaks fly past Shikhandi to Bhishma; on "ಬಿದ್ದ" Bhishma
       sinks slowly back onto a bed of light and becomes a figure of light: ಅರ್ಜುನನ ಬಾಣಗಳಿಂದ / ಭೀಷ್ಮ ಬಿದ್ದ; on
       "ಸೇಡು" Amba's light rises over him: ಅಂಬೆಯ ಸೇಡು / ಪೂರ್ತಿ ಆಯ್ತು!
  b15c CALLBACK: the hook's picture again (Shikhandi in the same pose, crimson sun stage); on "ಅತ್ತ" the girl of light
       rises behind him with tears: ಭೀಷ್ಮನಿಂದ ಅತ್ತ ಹುಡುಗಿ; on "ಸೋಲಾದಳು" the bed of light glows at their feet:
       / ಭೀಷ್ಮನ ಸೋಲಾದಳು!
  b16  ಭೀಷ್ಮನನ್ನ ಸೋಲಿಸಿದ್ದು / ಯಾರು?; two cards ಅರ್ಜುನ? (Arjuna under it) and ಅಂಬೆ? (Amba under it), a red ring
       alternating between them
"""
import math

import cairo

import sy_yk_cast as C
import yaksha_kit as Y
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import W, back, clamp, ease, prog
from shots import CUT_LEAD, MIN_SHOT, T

MISSES = set()                       # cue words not found in a line (falls back to fractions)
FEET = 1815                          # where the actors stand on the boards
SY_Y = 150                           # headline top


def cue(tl, bid, word, frac):
    try:
        return T(tl, bid, word)
    except (KeyError, ValueError):
        MISSES.add((bid, word))
        return T(tl, bid, frac)


# (name, Kannada word (an exact substring of the line), fraction fallback, ((after, min gap), ...)); "t0" = start
CUES = {
    "b1": (("B", "ಭೀಷ್ಮನಂಥ", 0.12, (("t0", 0.6),)),
           ("S", "ಸೋಲಿಸಿದ", 0.45, (("B", 1.0),)),
           ("P", "ಹಿಂದಿನ", 0.68, (("S", 0.9),)),
           ("L", "ಹುಡುಗಿ", 0.92, (("P", 0.6),))),
    "b2": (("M", "ಮಹಾಭಾರತದ", 0.2, (("t0", 0.1),)),
           ("S", "ನಿಜವಾದ", 0.55, (("M", 0.4),))),
    "b3": (("T", "ಶಕ್ತಿಶಾಲಿ", 0.2, (("t0", 0.3),)),
           ("K", "ಯಾರೂ", 0.6, (("T", 0.9),)),
           ("N", "ಸೋಲಿಸೋಕಾಗ್ತಿರಲಿಲ್ಲ", 0.75, (("K", 0.3),))),
    "b4": (("A", "ಅಂಬೆ", 0.2, (("t0", 0.2),)),
           ("F", "ಬಲವಂತವಾಗಿ", 0.5, (("A", 1.2),)),
           ("T", "ತಮ್ಮನ", 0.8, (("F", 1.3),)),
           ("W", "ಮದುವೆಗೆ", 0.9, (("T", 0.3),))),
    "b5": (("S", "ರಾಜನನ್ನ", 0.15, (("t0", 0.2),)),
           ("L", "ಪ್ರೀತಿಸ್ತಿದ್ಳು", 0.3, (("S", 0.3),)),
           ("F", "ಹೋದಾಗ", 0.5, (("L", 0.9),)),
           ("R", "ಹೇಳಿದ", 0.65, (("F", 0.8),)),
           ("N", "ಆಗಲ್ಲ", 0.95, (("R", 0.9),))),
    "b6": (("A", "ಒಂಟಿಯಾದ್ಳು", 0.12, (("t0", 0.2),)),
           ("B", "ಭೀಷ್ಮನಿಂದಾನೇ", 0.4, (("A", 1.0),))),
    "b7": (("V", "ಶಪಥ", 0.12, (("t0", 0.2),)),
           ("K", "ಸೋಲಿಸೇ", 0.7, (("V", 1.0),))),
    "b8": (("P", "ಪೂಜೆ", 0.25, (("t0", 0.4),)),
           ("S", "ಬಂದು", 0.45, (("P", 1.0),)),
           ("N", "ಮುಂದಿನ", 0.6, (("S", 0.8),)),
           ("K", "ಸೋಲಿಸ್ತೀಯ", 0.9, (("N", 0.8),))),
    "b9": (("F", "ಬೆಂಕಿಗೆ", 0.2, (("t0", 0.2),)),
           ("J", "ಜನ್ಮ", 0.6, (("F", 0.6),))),
    "b10": (("K", "ರಾಜನ", 0.3, (("t0", 0.6),)),
            ("B", "ಮಗಳಾಗಿ", 0.55, (("K", 0.7),)),
            ("N", "ಶಿಖಂಡಿ", 0.9, (("B", 0.9),))),
    "b11": (("Y", "ಮಾಯಾವಿ", 0.22, (("t0", 0.8),)),
            ("S", "ದೇಹವನ್ನ", 0.45, (("Y", 1.0),)),
            ("K", "ಕೊಟ್ಟ", 0.6, (("S", 0.8),)),
            ("N", "ಶಿಖಂಡಿ", 0.72, (("K", 0.5),)),
            ("M", "ಗಂಡು", 0.85, (("N", 0.3),))),
    "b12": (("Y", "ಯುದ್ಧ", 0.2, (("t0", 0.2),)),
            ("D", "ಹತ್ತು", 0.4, (("Y", 0.8),)),
            ("N", "ಸೋಲಿಸೋಕಾಗಲಿಲ್ಲ", 0.8, (("D", 1.0),))),
    "b12q": (("Q", "ಹೇಗೆ", 0.55, (("t0", 0.3),)),),
    "b13": (("R", "ನಿಯಮ", 0.25, (("t0", 0.3),)),
            ("G", "ಹುಡುಗಿಯಾಗಿದ್ದವರ", 0.45, (("R", 0.9),)),
            ("F", "ಯುದ್ಧ", 0.8, (("G", 0.9),))),
    "b14": (("A", "ಅರ್ಜುನ", 0.1, (("t0", 0.4),)),
            ("S", "ಶಿಖಂಡಿಯನ್ನ", 0.25, (("A", 0.5),)),
            ("R", "ರಥದಲ್ಲಿ", 0.5, (("S", 0.7),)),
            ("F", "ಮುಂದೆ", 0.8, (("R", 0.6),))),
    "b15": (("D", "ಆಯುಧ", 0.05, (("t0", 0.15),)),
            ("A", "ಅರ್ಜುನನ", 0.3, (("D", 1.0),)),
            ("G", "ಬಿದ್ದ", 0.6, (("A", 1.0),)),
            ("R", "ಸೇಡು", 0.8, (("G", 1.3),))),
    "b15c": (("R", "ಅತ್ತ", 0.2, (("t0", 0.4),)),
             ("N", "ಮುಂದಿನ", 0.45, (("R", 0.6),)),
             ("H", "ಸೋಲಾದಳು", 0.85, (("N", 0.8),))),
    "b16": (("Q", "ಯಾರು", 0.3, (("t0", 0.3),)),
            ("A", "ಅರ್ಜುನನಾ", 0.45, (("Q", 0.4),)),
            ("M", "ಅಂಬೆನಾ", 0.65, (("A", 0.6),)),
            ("C", "ಕಾಮೆಂಟ್", 0.85, (("M", 0.5),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_sy_cues", None)
    if cache is None:
        cache = {}
        tl._sy_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, word, frac, cons in CUES[bid]:
            v = cue(tl, bid, word, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


# ------------------------------------------------------------------ figures of light made once

C.ghost_def("amba", C.AMBA, dict(mood="calm", lid=0.35, armL=C.ANJALI, armR=C.ANJALI, bend=0.12))
C.ghost_def("bhishma", C.BHISHMA, dict(mood="joy", armL=(0.10, 0.05, 0.0), armR=(0.10, 0.05, 0.0), bend=0.02))


# ------------------------------------------------------------------ small helpers


def heads(cr, t, seq, y=SY_Y, small_size=72, big_size=150, alpha=1.0):
    """seq = [(t_on, small, big, delay of the big line)]: each headline replaces the one before at its t_on.
    Returns the big line's box (or None)."""
    cur = None
    for i, it in enumerate(seq):
        if t >= it[0]:
            cur = i
    if cur is None:
        return None
    t_on, small, big, dtb = seq[cur]
    return Y.kn_headline(cr, t, small, big, t_on, t_on + dtb, y=y, small_size=small_size, big_size=big_size,
                         alpha=alpha)


def zoom(t, t0, t1, z0=1.0, z1=1.04, fx=540, fy=1150):
    return (z0 + (z1 - z0) * clamp((t - t0) / max(0.5, t1 - t0)), fx, fy)


def stamp_at(t, t_s, dur=0.8, side="R"):
    """step() keyed so the foot lands at t_s."""
    return Y.step(t, t_s - dur * 0.62, dur, side)


def bow_pose(raise_, release=0.0):
    """Arms from the bow at rest (0) to drawn (1); after the release the string hand drops back to the hip."""
    armL = C.mix(C.BOW_REST, C.BOW_HOLD, raise_)
    armR = C.mix(C.AKIMBO, C.BOW_DRAW, raise_ * (1 - release))
    return armL, armR


def draw_bow(c, o, t, drawn, arrow, h=440, s=1.0, alpha=1.0, hand="L"):
    """The bow in the figure's `hand` ("L" / "R", the rig's names), its back bulging away from the body; the string
    to the other hand while drawn."""
    hb = C.U(c, o["hand" + hand])
    hs = C.U(c, o["handR" if hand == "L" else "handL"])
    out = -1 if hb[0] < C.U(c, o["chest"])[0] else 1
    pull = None
    if drawn > 0.05:
        tipx = hb[0] - out * 0.20 * h * s
        pull = (tipx + (hs[0] - tipx) * drawn, hb[1] + (hs[1] - hb[1]) * drawn)
    C.bow(c, hb[0], hb[1] + 4 * s, h * s, out, pull=pull, arrow=arrow and drawn > 0.3, alpha=alpha, lw=s)


def silhouette(cr, draw_fn, col, a):
    """Paint whatever draw_fn draws as one flat colour (a shadow on the backdrop)."""
    if a <= 0.01:
        return
    cr.push_group()
    draw_fn(cr)
    pat = cr.pop_group()
    cr.set_source_rgba(*col, a)
    cr.mask(pat)


def pool(cr, x, y, r, a, col=(1.0, 0.85, 0.6)):
    """A spotlight pool on the boards round an actor's feet."""
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(1.0, 0.25)
    g = cairo.RadialGradient(0, 0, 0, 0, 0, r)
    g.add_color_stop_rgba(0, *col, 0.5 * a)
    g.add_color_stop_rgba(1, *col, 0.0)
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source(g)
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def darken(cr, a, col=(0.02, 0.02, 0.08)):
    if a <= 0.01:
        return
    cr.set_source_rgba(*col, a)
    cr.paint()


# ------------------------------------------------------------------ b1: the hook (and b15c, the callback)

HOOK_X, HOOK_S = 600, 0.95
GHOST_X = 815                        # where the girl of light stands beside him (hook and callback)


def shikhandi_hook_pose(t, raise_, release, t2=2.3):
    armL, armR = bow_pose(raise_, release)
    lift, bb, stamp = stamp_at(t, 1.25, 0.8, "R")
    lift2, bb2, stamp2 = stamp_at(t, t2, 0.8, "L")          # a second stamp while the bow is drawn
    p = C.pose(t, 1.0, 0.45, mood="fierce" if raise_ > 0.3 else "calm", gaze=(-0.6 * raise_, 0.0),
               turn=-0.35 * raise_, armL=armL, armR=armR, handL="fist", handR="fist",
               bend=0.30 + 0.25 * (bb + bb2) + 0.1 * raise_, liftR=0.7 * lift, liftL=0.6 * lift2)
    return p, max(stamp, stamp2)


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "b1")
    raise_ = prog(t, c["B"], 0.6) * (1 - prog(t, c["S"] + 0.5, 0.5))
    release = clamp((t - c["S"]) / 0.12)
    drawn = raise_ * (1 - release)
    p, stamp = shikhandi_hook_pose(t, raise_, release, (c["B"] + c["S"]) / 2 + 0.2)
    side = prog(t, c["P"] - 0.1, 0.6)                    # he steps left; the girl of light rises at his right
    x = HOOK_X - 150 * side
    lit = prog(t, c["L"], 0.4)

    def behind(cc):
        a = prog(t, c["P"], 0.7)
        C.ghost(cc, "amba", GHOST_X, FEET - 10 + 60 * (1 - a), 0.86, a * (0.85 + 0.15 * lit), t=t,
                glow=1.0 + 0.8 * lit)

    def actors(cc):
        o = C.fig(cc, C.SHIKHANDI, x, FEET, HOOK_S, t, p)
        draw_bow(cc, o, t, drawn, True, 440, HOOK_S)
        return o

    def extra(cc, pts):
        o = pts[0]
        if 0 < t - c["S"] < 1.0:                           # the arrow of light shoots off across the stage
            hb = C.U(cc, o["handL"])
            C.streak(cc, (x + 40, hb[1]), (-160, hb[1] - 40), (t - c["S"]) / 0.4, 1.0, 520, 1.4)
            Y.glow(cc, hb[0], hb[1], 220, 0.7 * (1 - clamp((t - c["S"]) / 0.4)))
        fr = C.U(cc, o["footR" if t < c["B"] + 0.3 else "footL"])
        C.dust(cc, fr[0], fr[1], stamp)
        if lit > 0:
            Y.sparks(cc, t, GHOST_X, 1300, 220, 9, lit, 0.5, seed=4)

    def ui(cc, pts):
        box = heads(cc, t, [(-0.3, "ಭೀಷ್ಮನನ್ನ ಸೋಲಿಸಿದ ಈ ಯೋಧ", "ಹಿಂದೆ ಹುಡುಗಿ!", 0.55)])
        if box:
            C.underline(cc, box[0] + 10, box[0] + box[2] - 10, box[1] + box[3] + 10, prog(t, c["L"], 0.45))
        C.tag(cc, t, c["P"] + 0.35, "ಹಿಂದಿನ ಜನ್ಮ", GHOST_X - 20, 820, None, 52, field=C.PINK_DK)

    flash = 0.35 * stamp + 0.5 * clamp(1 - (t - c["S"]) / 0.3) * (t >= c["S"])
    Y.compose(cr, t, [actors], "crimson", "sun", extra=extra, ui=ui, behind=behind, flash=flash,
              zoom=zoom(t, t0, t1, 1.0, 1.04), musicians_at=(112, 0.5, False) if t > 2.0 else None)


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "b15c")
    p, _ = shikhandi_hook_pose(t + 3.0, 0.0, 0.0)
    up = prog(t, c["H"], 0.5)                              # he lifts the bow in victory
    p["armL"] = C.mix(C.BOW_REST, BOW_UP, up)
    p["mood"] = "calm" if up < 0.5 else "smile"
    side = prog(t, c["R"] - 0.1, 0.6)
    x = HOOK_X - 150 * side

    def behind(cc):
        a = prog(t, c["R"], 0.6)
        C.ghost(cc, "amba", GHOST_X, FEET - 10 + 60 * (1 - a), 0.86, a, t=t, glow=1.0 + 0.6 * up)

    def actors(cc):
        o = C.fig(cc, C.SHIKHANDI, x, FEET, HOOK_S, t, p)
        draw_bow(cc, o, t, 0.0, False, 440, HOOK_S)
        return o

    def extra(cc, pts):
        a = prog(t, c["R"] + 0.3, 0.4) * (1 - prog(t, c["H"], 0.5))
        for k in range(2):                                 # her tears, falling
            u = ((t - c["R"]) * 0.8 + k * 0.5) % 1.0
            C.tear(cc, GHOST_X - 5 + (k * 2 - 1) * 26, 905 + 140 * u, 1.3, a * (1 - u))
        if up > 0:
            C.light_bed(cc, t, 240, 920, 1690, 1830, 0.7 * up, 13)
            Y.sparks(cc, t, GHOST_X, 1250, 200, 8, up, 0.5, seed=2)

    def ui(cc, pts):
        Y.kn_headline(cc, t, "ಭೀಷ್ಮನಿಂದ ಅತ್ತ ಹುಡುಗಿ", "ಭೀಷ್ಮನ ಸೋಲಾದಳು!", t0 - 0.05, c["H"], y=SY_Y,
                      small_size=72, big_size=146)

    Y.compose(cr, t, [actors], "crimson", "sun", extra=extra, ui=ui, behind=behind, flash=0.3 * prog(t, c["H"], 0.2)
              * (1 - prog(t, c["H"] + 0.3, 0.5)), zoom=zoom(t, t0, t1, 1.0, 1.04), musicians_at=(112, 0.5, False))


# ------------------------------------------------------------------ b2: the story (the singer and the drummer)


def s_story(cr, t, tl, t0, t1):
    c = cues(tl, "b2")
    op = prog(t, c["M"] - 0.1, 0.6)

    def actors(cc):
        C.palm_book(cc, 560, 1280 - 30 * ease(op), 1.0, t, op)
        return {}

    def ui(cc, pts):
        Y.kn_banner(cc, t, t0 + 0.05, [("ಇದು ಮಹಾಭಾರತದ", 84, Y.CREAM), ("ನಿಜವಾದ ಕಥೆ", 140, Y.YEL)], W / 2, 400,
                    rot=-0.025, max_w=900)

    def extra(cc, pts):
        Y.sparks(cc, t, 560, 1350, 300, 8, prog(t, c["S"], 0.3), 0.4, seed=5)

    Y.compose(cr, t, [actors], "indigo", "rays", ui=ui, extra=extra, shadow=False,
              musicians_at=(95, 0.62, False), zoom=zoom(t, t0, t1, 1.0, 1.05, 540, 1500))


# ------------------------------------------------------------------ b3: Bhishma, whom nobody could beat


def s_bhishma(cr, t, tl, t0, t1):
    c = cues(tl, "b3")
    lift, bb, stamp = stamp_at(t, t0 + 0.55, 0.8, "L")
    lift2, bb2, stamp2 = stamp_at(t, c["K"] + 0.9, 0.8, "R")
    up = prog(t, c["T"] - 0.1, 0.4) * (1 - prog(t, c["K"] - 0.2, 0.4))     # he lifts his bow high on "ಶಕ್ತಿಶಾಲಿ"
    p = C.pose(t, 0.9, 0.45, mood="smile" if t < c["K"] else "calm", gaze=(0.0, -0.3 * up), armL=C.AKIMBO,
               armR=C.mix(C.BOW_REST, BOW_UP, up), handL="fist", handR="fist", bend=0.25 + 0.3 * (bb + bb2),
               liftL=0.7 * lift, liftR=0.7 * lift2)
    hit = prog(t, c["K"], 0.3)

    def behind(cc):
        Y.rays(cc, t, 540, 1050, 150, 1100, 0.5 + 0.4 * max(hit, up), 24, (1.0, 0.85, 0.5), 0.05)

    def actors(cc):
        o = C.fig(cc, C.BHISHMA, 540, FEET, 0.95, t, p)
        draw_bow(cc, o, t, 0.0, False, 440, 0.95, hand="R")
        return o

    def extra(cc, pts):
        o = pts[0]
        fr = C.U(cc, o["footL" if t < c["K"] else "footR"])
        C.dust(cc, fr[0], fr[1], max(stamp, stamp2))
        ch = C.U(cc, o["chest"])
        if hit > 0:                                        # arrows of light spark off a golden ring round him
            R = 430
            cc.save()
            cc.set_operator(cairo.OPERATOR_ADD)
            cc.set_source_rgba(1.0, 0.85, 0.45, 0.35 * hit)
            cc.set_line_width(14)
            cc.arc(ch[0], ch[1] + 80, R, 0, 2 * math.pi)
            cc.stroke()
            cc.restore()
            for k in range(6):
                tk = c["K"] + 0.18 * k
                sd = -1 if k % 2 == 0 else 1
                y0 = 900 + 170 * ((k * 37) % 5)
                tgt = (ch[0] + sd * R * 0.92, ch[1] + 80 + (y0 - ch[1] - 80) * 0.35)
                u = (t - tk) / 0.35
                C.streak(cc, (540 + sd * 700, y0), tgt, u, 1.0, 260, 1.0)
                if 1.0 < u < 2.4:
                    s_ = 1 - (u - 1.0) / 1.4
                    Y.sparkle(cc, tgt[0], tgt[1], 60 * s_, s_)
                    Y.glow(cc, tgt[0], tgt[1], 120, 0.5 * s_)

    def ui(cc, pts):
        heads(cc, t, [(t0 - 0.05, "ಭೀಷ್ಮ", "ತುಂಬಾ ಶಕ್ತಿಶಾಲಿ", 0.3), (c["K"], "ಭೀಷ್ಮನಿಗೆ", "ಸೋಲೇ ಇಲ್ಲ!", 0.25)])

    Y.compose(cr, t, [actors], "crimson", "rays", extra=extra, ui=ui, behind=behind,
              flash=0.3 * max(stamp, stamp2), zoom=zoom(t, t0, t1, 1.0, 1.04), musicians_at=(90, 0.45, False))


# ------------------------------------------------------------------ b4: Amba is taken


def s_amba1(cr, t, tl, t0, t1):
    c = cues(tl, "b4")

    def actors(cc):
        tw = C.spin(t, c["A"] + 0.35, 0.9)               # a graceful turn as her name is said
        p = C.pose(t, 1.0, 0.45, mood="smile", gaze=(0.0, 0.1), armL=(0.35, 1.6, 0.0),
                   armR=C.mix((0.55, 0.2, 0.0), (1.3, -0.6, 0.2), math.sin(math.pi * clamp((t - c["A"]) / 1.3))),
                   handL="open", handR="open", bend=0.15, spin=tw)
        return C.fig(cc, C.AMBA, 540, FEET, 1.0, t, p)

    def extra(cc, pts):
        o = pts[0]
        h = C.U(cc, o["handL"])
        Y.sparks(cc, t, h[0], h[1], 120, 5, 0.6, 0.4, seed=1)

    def ui(cc, pts):
        heads(cc, t, [(t0 - 0.05, "ರಾಜಕುಮಾರಿ", "ಅಂಬೆ", 0.0 if t0 < c["A"] - 0.3 else 0.2)])
        f = C.U(cc, pts[0]["face"])
        Y.glow(cc, f[0], f[1], 160, 0.10)

    Y.compose(cr, t, [actors], "green", "sun", extra=extra, ui=ui, zoom=zoom(t, t0, t1, 1.0, 1.05))


def s_amba2(cr, t, tl, t0, t1):
    c = cues(tl, "b4")
    u = prog(t, t0 + 0.1, 1.6)                             # he leads her off to the left; she pulls back
    pull = 0.5 + 0.5 * math.sin((t - t0) * 5.0)

    def actors(cc):
        bx = 310 - 70 * u
        lift, bb, _ = Y.step(t, t0 + 0.2, 0.7, "L")
        lift2, bb2, _ = Y.step(t, t0 + 0.9, 0.7, "R")
        pb = C.pose(t, 0.6, 0.5, mood="angry", turn=0.35, gaze=(0.7, 0.0), lean=-0.06, head=0.04,
                    armL=(0.35, 0.5, 0.0), armR=(1.02, 0.55, 0.0), handL="fist", handR="fist",
                    bend=0.25 + 0.3 * (bb + bb2), liftL=0.6 * lift, liftR=0.6 * lift2)
        ax = 770 - 70 * u
        pa = C.pose(t, 0.4, 0.6, mood="sad", turn=-0.4, gaze=(-0.8, 0.1), lean=0.08 + 0.03 * pull, head=0.06,
                    armL=(1.05, 0.62, 0.0), armR=FACE_ONE, handL="open", handR="open", bend=0.1)
        oa = C.fig(cc, C.AMBA, ax, FEET, 0.8, t, pa)
        ob = C.fig(cc, C.BHISHMA, bx, FEET, 0.8, t, pb)
        return {"a": oa, "b": ob}

    def extra(cc, pts):
        o = pts[0]
        ha = C.U(cc, o["a"]["face"])
        C.tear(cc, ha[0] - 22, ha[1] + 30 + 40 * ((t * 0.9) % 1.0), 1.1, 0.9 * (1 - (t * 0.9) % 1.0))

    def ui(cc, pts):
        heads(cc, t, [(t0, "ಭೀಷ್ಮ ಕರ್ಕೊಂಡು ಬಂದ", "ಬಲವಂತವಾಗಿ!", 0.25)])

    Y.compose(cr, t, [actors], "green", "sun", extra=extra, ui=ui, zoom=zoom(t, t0, t1, 1.0, 1.03))


FACE_ONE = (0.30, 2.65, -0.3)        # one hand up at the face
BOW_UP = (2.1, -0.7, 0.0)             # the bow raised high (victory), kept inside the frame


def s_amba3(cr, t, tl, t0, t1):
    c = cues(tl, "b4")

    def actors(cc):
        pb = C.pose(t, 0.6, 0.5, mood="calm", turn=0.3, gaze=(0.8, 0.0), armL=C.AKIMBO, armR=(1.2, 0.0, 0.2),
                    handL="fist", handR="open", bend=0.2)
        pk = C.pose(t, 1.0, 0.6, mood="joy", armL=(0.35, 2.15, 0.0), armR=(0.35, 2.15, 0.0), handL="fist",
                    handR="fist", bend=0.3)
        pa = C.pose(t, 0.4, 0.5, mood="sad", turn=-0.3, gaze=(-0.6, 0.2), armL=FACE_ONE, armR=REST_DN,
                    handL="open", handR="open")
        ob = C.fig(cc, C.BHISHMA, 190, FEET, 0.62, t, pb)
        ok = C.fig(cc, C.BROTHER, 540, FEET, 0.66, t, pk)
        oa = C.fig(cc, C.AMBA, 890, FEET, 0.68, t, pa)
        hl, hr = C.U(cc, ok["handL"]), C.U(cc, ok["handR"])
        C.garland(cc, (hl[0] + hr[0]) / 2, (hl[1] + hr[1]) / 2 - 4, 80)
        return {"b": ob, "k": ok, "a": oa}

    def ui(cc, pts):
        heads(cc, t, [(t0, "ತನ್ನ ತಮ್ಮನ", "ಮದುವೆಗೆ", 0.2)])
        k = C.U(cc, pts[0]["k"]["crown"])
        C.tag(cc, t, t0 + 0.15, "ತಮ್ಮ", k[0], k[1] - 60, None, 60)

    Y.compose(cr, t, [actors], "green", "tree", ui=ui, zoom=zoom(t, t0, t1, 1.0, 1.03))


REST_DN = (0.12, 0.10, 0.0)


# ------------------------------------------------------------------ b5: the king she loved says no


def s_love(cr, t, tl, t0, t1):
    c = cues(tl, "b5")
    walk = prog(t, c["F"], 0.9)
    no = prog(t, c["R"], 0.35)
    drop = clamp((t - c["N"] + 0.2) / 0.6)

    def actors(cc):
        lift, bb, _ = Y.step(t, c["F"], 0.8, "R")
        ax = 270 + 90 * walk
        pa = C.pose(t, 0.6, 0.5, mood="smile" if no < 0.5 else "sad", turn=0.35, gaze=(0.8, -0.1),
                    armL=C.mix((0.35, 2.05, 0.0), REST_DN, drop), armR=C.mix((0.35, 2.05, 0.0), FACE_ONE, drop),
                    handL="open", handR="open", liftR=0.5 * lift, bend=0.15 + 0.2 * bb)
        sx = 800
        ps = C.pose(t, 0.6, 0.45, ph=1.0, mood="smile" if no < 0.5 else "angry", turn=-0.4 + 1.2 * no,
                    gaze=(-0.8 + 1.7 * no, 0.0), head=0.07 * no, lean=0.05 * no,
                    armL=C.mix(REST_DN, C.PALM_UP, no), armR=C.mix(REST_DN, C.AKIMBO, no), handL="open",
                    handR="fist", bend=0.2)
        oa = C.fig(cc, C.AMBA, ax, FEET, 0.8, t, pa)
        os_ = C.fig(cc, C.SALVA, sx, FEET, 0.8, t, ps)
        return {"a": oa, "s": os_}

    def extra(cc, pts):
        o = pts[0]
        hl, hr = C.U(cc, o["a"]["handL"]), C.U(cc, o["a"]["handR"])
        gx, gy = (hl[0] + hr[0]) / 2, (hl[1] + hr[1]) / 2
        if drop > 0:
            gy = gy + (FEET - 60 - gy) * ease(drop)
            gx = gx + 40 * drop
        C.garland(cc, gx, gy, 70, prog(t, c["F"] - 0.2, 0.3), droop=1.0 - 0.6 * drop, rot=0.9 * drop)
        hx = (C.U(cc, o["a"]["face"])[0] + C.U(cc, o["s"]["face"])[0]) / 2
        C.heart(cc, hx, 860, 1.5, prog(t, c["L"] - 0.3, 0.3), crack=prog(t, c["R"] + 0.15, 0.6), t=t)

    def ui(cc, pts):
        heads(cc, t, [(t0 - 0.05, "ಅಂಬೆ ಪ್ರೀತಿಸಿದ್ದು", "ಬೇರೆ ರಾಜನನ್ನ", 0.35)], alpha=1 - prog(t, c["R"] - 0.1, 0.2))
        Y.kn_banner(cc, t, c["R"] + 0.05, [("ಈಗ ನಾನು ನಿನ್ನನ್ನ", 84, Y.CREAM), ("ಮದುವೆ ಆಗಲ್ಲ!", 136, Y.YEL)],
                    W / 2, 330, rot=0.02, max_w=900)
        s = C.U(cc, pts[0]["s"]["crown"])
        C.tag(cc, t, c["S"], "ಬೇರೆ ರಾಜ", s[0] + 40, s[1] - 50, None, 54, alpha=1 - prog(t, c["R"] - 0.1, 0.2))

    Y.compose(cr, t, [actors], "crimson", "tree", extra=extra, ui=ui, zoom=zoom(t, t0, t1, 1.0, 1.03))


# ------------------------------------------------------------------ b6: alone; it was all Bhishma's doing


def s_alone(cr, t, tl, t0, t1):
    c = cues(tl, "b6")
    turn = prog(t, c["B"], 0.6)

    def behind(cc):
        a = prog(t, c["B"], 0.7)
        Y.glow(cc, 660, 1150, 620, 0.55 * a, (1.0, 0.35, 0.15))     # a red backlight comes up on the cloth

        def shadow(g):
            Y.figure(g, C.BHISHMA, 670, 1900, 1.1, t, C.pose(t, 0.5, 0.4, armL=C.AKIMBO, armR=C.PALM_OUT,
                                                               handL="fist"))
        cc.save()
        x0, y0, x1, y1 = Y.CURT
        cc.rectangle(x0 + 64, y0 + 64, x1 - x0 - 128, y1 - y0 - 128)       # only on the painted cloth
        cc.clip()
        silhouette(cc, shadow, (0.03, 0.01, 0.03), 0.85 * a)
        cc.restore()

    def actors(cc):
        p = C.pose(t, 0.4, 0.4, mood="sad" if turn < 0.5 else "angry", turn=-0.5 * turn,
                   gaze=(-0.4 * turn, -0.9 * turn), head=-0.06 * turn,
                   armL=C.mix(C.FACE_HANDS, (0.3, 0.6, 0.0), turn), armR=C.mix(C.FACE_HANDS, (0.3, 0.6, 0.0), turn),
                   handL="open" if turn < 0.5 else "fist", handR="open" if turn < 0.5 else "fist", bend=0.1)
        return C.fig(cc, C.AMBA, 360, FEET, 0.72, t, p)

    def extra(cc, pts):
        f = C.U(cc, pts[0]["face"])
        a = 1 - turn
        for k in range(2):
            u = ((t - t0) * 0.9 + k * 0.5) % 1.0
            C.tear(cc, f[0] + (k * 2 - 1) * 24, f[1] + 30 + 110 * u, 1.1, a * (1 - u))
        pool(cc, 360, FEET, 330, 1.0)
        Y.glow(cc, f[0], f[1] + 200, 360, 0.14)

    def ui(cc, pts):
        heads(cc, t, [(t0 - 0.05, "ಅಂಬೆ", "ಒಂಟಿಯಾದ್ಳು", 0.3), (c["B"], "ಇದೆಲ್ಲ", "ಭೀಷ್ಮನಿಂದಾನೇ!", 0.25)])

    Y.compose(cr, t, [actors], "indigo", "plain", extra=extra, ui=ui, behind=behind, light_strength=0.6,
              zoom=zoom(t, t0, t1, 1.0, 1.04, 400, 1300))


# ------------------------------------------------------------------ b7: the vow


def s_vow(cr, t, tl, t0, t1):
    c = cues(tl, "b7")
    lift, bb, st1 = stamp_at(t, c["V"] + 0.15, 0.8, "R")
    lift2, bb2, st2 = stamp_at(t, c["K"] + 0.1, 0.8, "L")
    up = prog(t, c["V"] - 0.2, 0.45)
    stamp = max(st1, st2)

    def behind(cc):
        Y.rays(cc, t, 540, 1050, 160, 1100, 0.35 + 0.5 * prog(t, c["K"], 0.3), 22, (1.0, 0.55, 0.35), 0.05)

    def actors(cc):
        p = C.pose(t, 0.7, 0.5, mood="fierce" if up > 0.3 else "angry", gaze=(0.0, -0.2 * up),
                   armL=C.mix(REST_DN, (0.45, 0.4, 0.0), up), armR=C.mix(REST_DN, C.FIST_UP, up), handL="fist",
                   handR="fist", bend=0.2 + 0.3 * (bb + bb2), liftR=0.5 * lift, liftL=0.5 * lift2)
        return C.fig(cc, C.AMBA, 540, FEET, 1.0, t, p)

    def extra(cc, pts):
        o = pts[0]
        h = C.U(cc, o["handR"])
        Y.glow(cc, h[0], h[1], 220, 0.35 * up + 0.4 * st2)
        Y.sparkle(cc, h[0], h[1] - 20, 70 * (0.6 + 0.4 * math.sin(t * 7)), up)
        fr = C.U(cc, o["footR"] if t < c["K"] - 0.4 else o["footL"])
        C.dust(cc, fr[0], fr[1], stamp)

    def ui(cc, pts):
        Y.kn_text(cc, "ಅಂಬೆಯ ಶಪಥ", W / 2, 150, 76, Y.YEL, Y.INK, 7, alpha=prog(t, t0 - 0.1, 0.3), anchor="ct")
        Y.kn_banner(cc, t, c["V"] + 0.2, [("ನಾನು ಭೀಷ್ಮನನ್ನ", 84, Y.CREAM), ("ಸೋಲಿಸೇ ಸೋಲಿಸ್ತೀನಿ!", 120, Y.YEL)],
                    W / 2, 400, rot=-0.02, max_w=920)

    Y.compose(cr, t, [actors], "crimson", "rays", extra=extra, ui=ui, behind=behind, flash=0.35 * stamp,
              zoom=zoom(t, t0, t1, 1.0, 1.05))


# ------------------------------------------------------------------ b8: years of prayer; Shiva


def s_pray(cr, t, tl, t0, t1):
    c = cues(tl, "b8")

    def behind(cc):
        # suns and moons racing over the stage: the years going by
        for k in range(6):
            u = ((t - t0) * 0.75 + k / 6.0) % 1.0
            x = 120 + 840 * u
            y = 1000 - 330 * math.sin(math.pi * u)
            if k % 2 == 0:
                Y.glow(cc, x, y, 150, 0.5, (1.0, 0.7, 0.3))
                Y.rays(cc, t, x, y, 40, 95, 1.0, 12, (1.0, 0.8, 0.3), 0.5)
                Y.dot(cc, x, y, 36, (1.0, 0.78, 0.25), 4.0)
            else:
                Y.glow(cc, x, y, 100, 0.35, (0.7, 0.8, 1.0))
                C.crescent(cc, x, y, 30)

    def actors(cc):
        p = C.pose(t, 0.35, 0.35, mood="calm", lid=0.75, turn=-0.3, head=-0.05, armL=C.ANJALI, armR=C.ANJALI,
                   handL="open", handR="open", bend=0.1)
        return C.fig(cc, C.AMBA, 720, FEET, 0.86, t, p)

    def extra(cc, pts):
        C.linga(cc, 290, FEET + 10, 1.05, t, 0.35 + 0.15 * math.sin(t * 3))
        Y.sparks(cc, t, 290, 1560, 140, 6, 0.6, 0.35, seed=8)

    def ui(cc, pts):
        heads(cc, t, [(t0 - 0.05, "ವರ್ಷಗಟ್ಟಲೆ", "ಶಿವನ ಪೂಜೆ", 0.35)])

    Y.compose(cr, t, [actors], "indigo", "sun", extra=extra, ui=ui, behind=behind,
              zoom=zoom(t, t0, t1, 1.0, 1.04), musicians_at=(860, 0.42, True))


def s_shiva(cr, t, tl, t0, t1):
    c = cues(tl, "b8")
    app = prog(t, t0 + 0.05, 0.6)

    def behind(cc):
        Y.rays(cc, t, 470, 1000, 140, 1150, 0.9 * app, 26, (0.75, 0.85, 1.0), 0.04)
        Y.glow(cc, 470, 1050, 650, 0.35 * app, (0.75, 0.85, 1.0))

    def actors(cc):
        ps = C.pose(t, 0.6, 0.4, mood="smile", gaze=(0.5, 0.2), turn=0.2, armL=(0.38, 0.55, 0.0),
                    armR=(0.35, -2.59, 0.0), handL="fist", handR="bless", bend=0.2)
        o = C.fig(cc, C.SHIVA, 470, FEET + 40 * (1 - app), 0.9, t, ps, alpha=clamp(app * 1.5))
        h = C.U(cc, o["handL"])
        C.trishula(cc, h[0], FEET + 5, 0.95, alpha=clamp(app * 1.5))
        pa = C.pose(t, 0.3, 0.4, mood="wonder", turn=-0.5, gaze=(-0.8, -0.6), armL=C.ANJALI, armR=C.ANJALI,
                    handL="open", handR="open", bend=0.25)
        oa = C.fig(cc, C.AMBA, 905, FEET, 0.6, t, pa)
        return {"s": o, "a": oa}

    def extra(cc, pts):
        o = pts[0]
        cw = C.U(cc, o["s"]["crown"])
        C.crescent(cc, cw[0] - 70, cw[1] + 150, 34, clamp(app * 1.5))
        hb = C.U(cc, o["s"]["handR"])
        Y.glow(cc, hb[0], hb[1], 180, 0.5 * app, (0.8, 0.9, 1.0))
        bl = prog(t, c["K"], 0.4)
        if bl > 0:
            fa = C.U(cc, o["a"]["face"])
            Y.sparks(cc, t, fa[0], fa[1] + 200, 200, 8, bl, 0.5, seed=3)
            Y.glow(cc, fa[0], fa[1] + 150, 260, 0.35 * bl, C.SOUL)

    def ui(cc, pts):
        a = 1 - prog(t, c["N"] - 0.1, 0.2)
        heads(cc, t, [(t0, "ಆಗ", "ಶಿವ ಬಂದ!", 0.2)], alpha=a)
        Y.kn_banner(cc, t, c["N"], [("ಮುಂದಿನ ಜನ್ಮದಲ್ಲಿ", 80, Y.CREAM), ("ನೀನು ಭೀಷ್ಮನನ್ನ", 80, Y.CREAM),
                                    ("ಸೋಲಿಸ್ತೀಯ!", 136, Y.YEL)], W / 2, 400, rot=0.02, max_w=880)
        s = C.U(cc, pts[0]["s"]["face"])
        C.tag(cc, t, t0 + 0.4, "ಶಿವ", s[0] + 250, s[1] - 230, None, 64, alpha=a)

    Y.compose(cr, t, [actors], "indigo", "sun", extra=extra, ui=ui, behind=behind,
              flash=0.6 * clamp(1 - (t - t0) / 0.5), zoom=zoom(t, t0, t1, 1.0, 1.04))


# ------------------------------------------------------------------ b9: into the fire's light


def fire_light(cr, t, x, y, s, a):
    """The sacred fire as a tall soft light in a brick pit (no one is shown burning)."""
    Y.glow(cr, x, y - 220 * s, 520 * s, 0.55 * a, (1.0, 0.62, 0.20))
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for k, (w, hh, col, al) in enumerate(((150, 520, (1.0, 0.40, 0.08), 0.55), (100, 400, (1.0, 0.70, 0.20), 0.6),
                                          (52, 260, (1.0, 0.95, 0.70), 0.75))):
        sw = 20 * math.sin(t * 5 + k) * s
        cr.new_path()
        cr.move_to(x - w * s, y)
        cr.curve_to(x - w * s, y - hh * 0.5 * s, x + sw - w * 0.3 * s, y - hh * 0.7 * s, x + sw * 1.5, y - hh * s)
        cr.curve_to(x + sw + w * 0.3 * s, y - hh * 0.7 * s, x + w * s, y - hh * 0.5 * s, x + w * s, y)
        cr.close_path()
        cr.set_source_rgba(*col, al * a)
        cr.fill()
    cr.restore()
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    Y.shape(cr, [(-190, -30), (190, -30), (210, 60), (-210, 60)], (0.62, 0.26, 0.12), 6.0, smooth=False)
    for k in range(5):
        Y.stroke(cr, [(-200 + 100 * k, -30), (-205 + 102 * k, 60)], 4, Y.INK)
    Y.stroke(cr, [(-200, 14), (200, 14)], 4, Y.INK)
    Y.stroke(cr, [(-196, -26), (196, -26)], 8, Y.GOLD)
    cr.restore()


def s_fire(cr, t, tl, t0, t1):
    c = cues(tl, "b9")
    go = prog(t, c["F"] - 0.4, 0.9)
    gone = prog(t, c["F"] + 0.25, 0.4)
    rise = clamp((t - c["J"] + 0.1) / 1.2)

    def actors(cc):
        if gone >= 0.99:
            return {}
        p = C.pose(t, 0.3, 0.5, mood="calm", lid=0.5, turn=0.4, armL=C.ANJALI, armR=C.ANJALI, handL="open",
                   handR="open", bend=0.1)
        return C.fig(cc, C.AMBA, 260 + 230 * go, FEET, 0.78, t, p, alpha=1 - gone)

    def extra(cc, pts):
        fire_light(cc, t, 600, FEET - 20, 1.0, 1.0)
        if rise > 0:
            y = 1350 - 650 * ease(rise)
            Y.glow(cc, 600, y, 260, 0.6, C.SOUL)
            Y.orb(cc, t, 600, y, 34, 1.0)
            Y.sparks(cc, t, 600, y, 120, 6, 1.0, 0.6, seed=6)

    def ui(cc, pts):
        white = clamp(1 - abs(t - (c["F"] + 0.3)) / 0.45)
        if white > 0:
            cc.set_source_rgba(1.0, 0.95, 0.85, 0.75 * white)
            cc.paint()
        heads(cc, t, [(t0 - 0.05, "ಅಂಬೆ", "ಈ ಜನ್ಮ ಬಿಟ್ಟಳು", 0.35)])

    Y.compose(cr, t, [actors], "crimson", "plain", extra=extra, ui=ui, zoom=zoom(t, t0, t1, 1.0, 1.04))


# ------------------------------------------------------------------ b10: born again as a king's daughter


def s_birth(cr, t, tl, t0, t1):
    c = cues(tl, "b10")
    land = clamp((t - t0) / 1.1)
    named = prog(t, c["N"], 0.4)

    def actors(cc):
        joy = prog(t, c["B"], 0.4)
        pk = C.pose(t, 0.6, 0.45, mood="joy" if joy > 0.5 else "smile", turn=0.4, gaze=(0.8, 0.3),
                    armL=C.AKIMBO, armR=C.mix(REST_DN, (1.2, -0.5, 0.2), joy), handL="fist", handR="bless",
                    bend=0.2)
        pq = C.pose(t, 0.6, 0.45, ph=1.3, mood="joy" if joy > 0.5 else "smile", turn=-0.4, gaze=(-0.8, 0.3),
                    armL=C.mix(REST_DN, (0.35, 2.05, 0.0), joy), armR=C.mix(REST_DN, (0.35, 2.05, 0.0), joy),
                    handL="open", handR="open")
        ok = C.fig(cc, C.DRUPADA, 195, FEET, 0.72, t, pk)
        oq = C.fig(cc, C.QUEEN, 885, FEET, 0.72, t, pq)
        return {"k": ok, "q": oq}

    def extra(cc, pts):
        bx, by = C.cradle(cc, 540, 1640, 0.85, t, 1.0, rope_top=640)
        if land < 1:
            y = 640 + (by - 640) * ease(land)
            Y.glow(cc, 540, y, 220, 0.6, C.SOUL)
            Y.orb(cc, t, 540 + 20 * math.sin(t * 3) * (1 - land), y, 28, 1 - 0.8 * land)
        b = prog(t, c["B"], 0.4)
        Y.glow(cc, bx, by, 260, 0.25 + 0.3 * b + 0.2 * named, C.SOUL)
        if named > 0:
            Y.sparks(cc, t, bx, by, 160, 8, named, 0.5, seed=9)
            C.red_ring(cc, bx + 40, by + 20, 170, 95, named, 1.0, 8)

    def ui(cc, pts):
        heads(cc, t, [(t0 - 0.05, "ಮುಂದಿನ ಜನ್ಮದಲ್ಲಿ", "ರಾಜನ ಮಗಳು", c["B"] - t0 + 0.05),
                      (c["N"], "ಹೆಸರು", "ಶಿಖಂಡಿ", 0.2)])
        k = C.U(cc, pts[0]["k"]["crown"])
        C.tag(cc, t, c["K"], "ರಾಜ", k[0] + 20, k[1] - 40, None, 60, alpha=1 - prog(t, c["N"], 0.3))

    Y.compose(cr, t, [actors], "green", "sun", extra=extra, ui=ui, zoom=zoom(t, t0, t1, 1.0, 1.04))


# ------------------------------------------------------------------ b11: the yaksha gives his body


def s_yaksha(cr, t, tl, t0, t1):
    c = cues(tl, "b11")
    yk = prog(t, c["Y"], 0.6)
    cross = (t - c["S"]) / max(0.4, c["K"] - c["S"])       # 0 -> 1 as the lights travel, then they fade
    t_sp = c["K"] - 0.1
    sp = C.spin(t, t_sp, 0.8)                             # (the kit's spin_phase jumps half way; this one is smooth)
    swapped = t >= t_sp + 0.8 / 3.0                        # the look changes when she is edge-on
    lift, bb, stamp = stamp_at(t, c["M"] + 0.2, 0.8, "R")
    hx = 330

    def actors(cc):
        out = {}
        py = C.pose(t, 0.6, 0.45, ph=2.0, mood="smile", turn=-0.4, gaze=(-0.8, 0.0),
                    armL=C.mix(REST_DN, C.PALM_UP, prog(t, c["S"] - 0.3, 0.4)), armR=C.AKIMBO,
                    handL="bless", handR="fist", bend=0.2)
        out["y"] = C.fig(cc, C.YAKSHA, 790, FEET + 30 * (1 - yk), 0.86, t, py,
                         alpha=clamp(yk * 1.4) * (1 - 0.45 * prog(t, c["M"], 0.6)))
        if not swapped:
            pw = C.pose(t, 0.5, 0.45, mood="wonder" if t > c["Y"] else "calm", turn=0.35 * yk, gaze=(0.8 * yk, 0),
                        armL=REST_DN, armR=C.mix(REST_DN, (1.05, 0.3, 0.0), prog(t, c["S"] - 0.3, 0.4)),
                        handL="open", handR="open", spin=sp)
            out["h"] = C.fig(cc, C.AMBA, hx, FEET, 0.82, t, pw)
        else:
            up = prog(t, c["N"], 0.4)
            pm = C.pose(t, 0.8, 0.5, mood="fierce" if t > c["M"] else "wonder", turn=0.2, gaze=(0.3, 0.0),
                        armL=C.mix(C.BOW_REST, BOW_UP, up), armR=C.AKIMBO, handL="fist", handR="fist",
                        bend=0.3 + 0.3 * bb, liftR=0.6 * lift, spin=sp)
            out["h"] = C.fig(cc, C.SHIKHANDI, hx, FEET, 0.84, t, pm)
            ba = 1.0 if sp == 0.0 else clamp((sp - 0.75) / 0.2)
            if ba > 0:
                draw_bow(cc, out["h"], t, 0.0, False, 400, 0.84, alpha=ba)
        return out

    def behind(cc):
        Y.glow(cc, 790, 1150, 520, 0.4 * yk, C.GREENL)

    def extra(cc, pts):
        o = pts[0]
        ha = C.U(cc, o["h"]["chest"])
        hy = C.U(cc, o["y"]["chest"])
        if 0 < cross < 1.2:                                # two lights crossing in arcs
            u = ease(min(cross, 1.0))
            for (p0, p1, col, sg) in ((hy, ha, C.GREENL, -1), (ha, hy, C.SOUL, 1)):
                x = p0[0] + (p1[0] - p0[0]) * u
                y = p0[1] + (p1[1] - p0[1]) * u + sg * 230 * math.sin(math.pi * u)
                a = 1.0 if cross < 1 else clamp(1 - (cross - 1) / 0.2)
                Y.glow(cc, x, y, 230, 0.6 * a, col)
                Y.sparkle(cc, x, y, 70, a, col)
                Y.sparks(cc, t, x, y, 90, 5, a, 0.7, seed=int(sg + 2))
        if sp > 0:
            Y.glow(cc, ha[0], ha[1], 380, 0.8 * math.sin(math.pi * sp), (1.0, 0.85, 0.9))
        fr = C.U(cc, o["h"]["footR"])
        C.dust(cc, fr[0], fr[1], stamp)

    def ui(cc, pts):
        heads(cc, t, [(t0 - 0.05, "ದೊಡ್ಡವಳಾದ ಮೇಲೆ", "ಶಿಖಂಡಿ", 0.3), (c["Y"], "ಕಾಡಿನ ಒಬ್ಬ", "ಮಾಯಾವಿ ಯಕ್ಷ", 0.25),
                      (c["S"], "ಯಕ್ಷ ಕೊಟ್ಟ", "ಗಂಡಸಿನ ದೇಹ", 0.25), (c["M"], "ಈಗ ಶಿಖಂಡಿ", "ಗಂಡು ಯೋಧ!", 0.2)])
        y = C.U(cc, pts[0]["y"]["face"])
        C.tag(cc, t, c["Y"] + 0.4, "ಯಕ್ಷ", y[0] - 250, y[1] - 250, None, 58, alpha=1 - prog(t, c["S"], 0.3),
              field=Y.DGREEN)

    Y.compose(cr, t, [actors], "green", "tree", extra=extra, ui=ui, behind=behind,
              flash=0.7 * math.sin(math.pi * sp) + 0.3 * stamp, zoom=zoom(t, t0, t1, 1.0, 1.04))


# ------------------------------------------------------------------ b12: ten days of war


def s_war(cr, t, tl, t0, t1):
    c = cues(tl, "b12")
    cyc = ((t - t0) % 1.1) / 1.1
    drawn = clamp(cyc / 0.6) if cyc < 0.7 else 0.0

    def actors(cc):
        p = C.pose(t, 0.6, 0.6, mood="fierce", turn=0.3, gaze=(0.8, 0.0), armL=C.mix(C.AKIMBO, C.BOW_DRAW, drawn),
                   armR=C.BOW_HOLD, handL="fist", handR="fist", bend=0.35)
        o = C.fig(cc, C.BHISHMA, 480, FEET, 0.88, t, p)
        draw_bow(cc, o, t, drawn, True, 440, 0.88, hand="R")
        return o

    def extra(cc, pts):
        o = pts[0]
        ch = C.U(cc, o["chest"])
        R = 420
        cc.save()
        cc.set_operator(cairo.OPERATOR_ADD)
        cc.set_source_rgba(1.0, 0.85, 0.45, 0.3)
        cc.set_line_width(12)
        cc.arc(ch[0], ch[1] + 90, R, 0, 2 * math.pi)
        cc.stroke()
        cc.restore()
        for k in range(12):                                # enemy arrows from the left spark off the ring
            tk = t0 + 0.28 * k
            y0 = 760 + (k * 173) % 760
            tgt = (ch[0] - R * 0.95, ch[1] + 90 + (y0 - ch[1] - 90) * 0.3)
            u = (t - tk) / 0.35
            C.streak(cc, (-80, y0), tgt, u, 1.0, 240, 0.9)
            if 1.0 < u < 2.0:
                s_ = 2.0 - u
                Y.sparkle(cc, tgt[0], tgt[1], 55 * s_, s_)
        k = int((t - t0) / 1.1)                            # his own arrows fly off to the right
        tr = t0 + 1.1 * k + 0.7
        hb = C.U(cc, o["handR"])
        C.streak(cc, (hb[0] + 40, hb[1]), (1250, hb[1] - 60), (t - tr) / 0.4, 1.0, 380, 1.2)

    def ui(cc, pts):
        heads(cc, t, [(t0 - 0.05, "ಆಮೇಲೆ", "ದೊಡ್ಡ ಯುದ್ಧ", 0.3), (c["D"], "ಹತ್ತು ದಿನ ಆದ್ರೂ", "ಭೀಷ್ಮ ಸೋಲಲಿಲ್ಲ!", 0.3)])
        if t >= c["D"]:
            n = 1 + int(9 * clamp((t - c["D"]) / max(0.8, c["N"] - c["D"])))
            C.card(cc, t, c["D"], 870, 700, 270, 150, [(f"ದಿನ {n}", 84, Y.YEL)], rot=0.03)

    Y.compose(cr, t, [actors], "crimson", "rays", extra=extra, ui=ui, zoom=zoom(t, t0, t1, 1.0, 1.04),
              musicians_at=(70, 0.42, False))


# ------------------------------------------------------------------ b12q: the question


def s_question(cr, t, tl, t0, t1):
    c = cues(tl, "b12q")

    def actors(cc):
        p = C.pose(t, 0.8, 0.5, mood="wonder", turn=0.4, gaze=(0.6, -0.9), head=-0.05, armL=C.BOW_REST,
                   armR=C.AKIMBO, handL="fist", handR="fist", bend=0.25)
        o = C.fig(cc, C.SHIKHANDI, 250, FEET, 0.52, t, p)
        draw_bow(cc, o, t, 0.0, False, 400, 0.52)
        return o

    def ui(cc, pts):
        C.big_q(cc, t, t0, 560, 480, 520)
        C.card(cc, t, t0 + 0.1, 560, 990, 900, 360, [("ಭೀಷ್ಮನನ್ನ", 100, Y.CREAM), ("ಹೇಗೆ ಸೋಲಿಸಿದ್ರು?", 124, Y.YEL)],
               rot=-0.02)
        C.red_ring(cc, 560, 1062, 390, 95, prog(t, c["Q"], 0.5), 1.0, 9)

    Y.compose(cr, t, [actors], "indigo", "plain", ui=ui, zoom=zoom(t, t0, t1, 1.0, 1.03))


# ------------------------------------------------------------------ b13: Bhishma's rule


def arrow_icon(cr, x0, y0, x1, y1, s, alpha=1.0):
    """A plain golden arrow from (x0, y0) (feathers) to (x1, y1) (point)."""
    a = math.atan2(y1 - y0, x1 - x0)
    cr.push_group()
    Y.stroke(cr, [(x0, y0), (x1, y1)], 16 * s, Y.INK, smooth=False)
    Y.stroke(cr, [(x0, y0), (x1, y1)], 9 * s, Y.GOLD, smooth=False)
    cr.save()
    cr.translate(x1, y1)
    cr.rotate(a)
    Y.shape(cr, [(40 * s, 0), (-6 * s, -20 * s), (4 * s, 0), (-6 * s, 20 * s)], Y.GOLD_HI, 4.0, smooth=False)
    cr.restore()
    cr.save()
    cr.translate(x0, y0)
    cr.rotate(a)
    for sg in (-1, 1):
        Y.shape(cr, [(0, 0), (-10 * s, sg * 24 * s), (40 * s, sg * 6 * s)], Y.RED, 3.0, smooth=False)
    cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(alpha)


def crossed_no(cr, x, y, s, p):
    """Two crossed arrows (a fight) with a big red X over them."""
    if p <= 0.01:
        return
    Y.glow(cr, x, y, 260 * s, 0.4 * p, (1.0, 0.8, 0.4))
    for sd in (-1, 1):
        a = sd * 0.42
        dx, dy = 170 * s * math.cos(a), 170 * s * math.sin(a)
        arrow_icon(cr, x - dx, y - dy, x + dx, y + dy, s, clamp(p * 2))
    q = back(clamp((p - 0.3) / 0.7), 1.8)
    if q > 0:
        cr.save()
        cr.translate(x, y)
        cr.scale(q, q)
        for sd in (-1, 1):
            Y.stroke(cr, [(-110 * s, -110 * s * sd), (110 * s, 110 * s * sd)], 44 * s, Y.INK, smooth=False)
            Y.stroke(cr, [(-110 * s, -110 * s * sd), (110 * s, 110 * s * sd)], 30 * s, (0.90, 0.08, 0.08),
                     smooth=False)
        cr.restore()


def s_rule(cr, t, tl, t0, t1):
    c = cues(tl, "b13")
    g = prog(t, c["G"], 0.6)
    no = prog(t, c["F"], 0.4)

    def behind(cc):
        C.ghost(cc, "amba", 250, FEET - 10 + 50 * (1 - g), 0.78, g, t=t)

    def actors(cc):
        p = C.pose(t, 0.6, 0.45, mood="calm", turn=-0.45, gaze=(-0.8, 0.0),
                   armL=C.mix(REST_DN, C.PALM_OUT, prog(t, c["R"] - 0.2, 0.4)), armR=C.mix(C.BOW_REST, REST_DN, no),
                   handL="open", handR="fist", bend=0.2)
        o = C.fig(cc, C.BHISHMA, 740, FEET, 0.86, t, p)
        hb = C.U(cc, o["handR"])
        C.bow(cc, hb[0], hb[1] + 4, 420 * 0.86, 1, rot=1.1 * no, lw=0.86)
        return o

    def extra(cc, pts):
        crossed_no(cc, 440, 1520, 0.72, no)

    def ui(cc, pts):
        heads(cc, t, [(t0 - 0.05, "ಭೀಷ್ಮನ", "ಒಂದು ನಿಯಮ", c["R"] - t0)], alpha=1 - prog(t, c["G"] - 0.1, 0.2))
        Y.kn_banner(cc, t, c["G"], [("ಒಮ್ಮೆ ಹುಡುಗಿಯಾಗಿದ್ದವರ ಜೊತೆ", 74, Y.CREAM), ("ಯುದ್ಧ ಮಾಡಲ್ಲ!", 136, Y.YEL)],
                    W / 2, 360, rot=-0.02, max_w=940)

    Y.compose(cr, t, [actors], "indigo", "sun", extra=extra, ui=ui, behind=behind, zoom=zoom(t, t0, t1, 1.0, 1.04))


# ------------------------------------------------------------------ b14: Shikhandi in front, in Arjuna's chariot

CH_Y = 1740                           # the chariot panel's bottom edge


def s_chariot(cr, t, tl, t0, t1):
    c = cues(tl, "b14")
    roll = ease(clamp((t - t0 + 0.1) / 1.1))
    cx = -520 + 980 * roll
    step_in = prog(t, c["S"], 0.6)
    front = prog(t, c["F"], 0.4)

    def actors(cc):
        pa = C.pose(t, 0.5, 0.5, mood="calm", turn=0.4, gaze=(0.8, 0.0), armL=C.BOW_REST, armR=C.AKIMBO,
                    handL="fist", handR="fist", bend=0.2)
        oa = C.fig(cc, C.ARJUNA, cx - 210, CH_Y - 70, 0.62, t, pa, shadow=0)
        draw_bow(cc, oa, t, 0.0, False, 400, 0.62)
        out = {"a": oa}
        if step_in > 0:
            ps = C.pose(t, 0.6, 0.5, ph=1.0, mood="fierce" if front > 0.5 else "calm", turn=0.4, gaze=(0.9, 0.0),
                        armL=C.AKIMBO, armR=C.mix(REST_DN, C.REACH, front), handL="fist", handR="point", bend=0.25)
            out["s"] = C.fig(cc, C.SHIKHANDI, cx + 190 + 200 * (1 - step_in), CH_Y - 70 - 60 * (1 - step_in),
                             0.66, t, ps, alpha=clamp(step_in * 2), shadow=0)
        C.chariot(cc, cx, CH_Y, 0.95, t, roll=-roll * 6.0)
        return out

    def behind(cc):
        if step_in > 0:
            Y.glow(cc, cx + 190, 1250, 330, 0.35 * front, C.SOUL)

    def extra(cc, pts):
        if 0 < roll < 1:
            for k in range(5):
                Y.sparkle(cc, cx - 300 - 60 * k, 1820 - 30 * (k % 2), 26 * (1 - roll), 1 - roll)

    def ui(cc, pts):
        o = pts[0]
        a = C.U(cc, o["a"]["crown"])
        C.tag(cc, t, c["A"], "ಅರ್ಜುನ", a[0] - 30, a[1] - 40, None, 58, alpha=1 - prog(t, c["F"], 0.3))
        if "s" in o:
            s = C.U(cc, o["s"]["crown"])
            C.tag(cc, t, c["S"] + 0.3, "ಶಿಖಂಡಿ", s[0] + 40, s[1] - 40, None, 58, field=C.PINK_DK,
                  alpha=1 - prog(t, c["F"], 0.3))
            if front > 0:
                f = C.U(cc, o["s"]["face"])
                y = f[1] - 290 - 30 * math.sin(t * 6)
                Y.stroke(cc, [(f[0], y - 150), (f[0], y)], 30, Y.INK, smooth=False, alpha=front)
                Y.stroke(cc, [(f[0], y - 150), (f[0], y)], 18, (0.9, 0.08, 0.08), smooth=False, alpha=front)
                Y.shape(cc, [(f[0] - 50, y - 10), (f[0] + 50, y - 10), (f[0], y + 50)], (0.9, 0.08, 0.08), 6.0,
                        smooth=False)
                Y.kn_text(cc, "ಮುಂದೆ!", f[0] + 150, y - 110, 84, Y.YEL, Y.INK, 7, alpha=front)
        heads(cc, t, [(c["S"], "ಅರ್ಜುನ, ಶಿಖಂಡಿಯನ್ನ", "ಮುಂದೆ ನಿಲ್ಲಿಸಿದ!", c["F"] - c["S"])])

    Y.compose(cr, t, [actors], "crimson", "sun", extra=extra, ui=ui, behind=behind, zoom=zoom(t, t0, t1, 1.0, 1.03))


# ------------------------------------------------------------------ b15: Bhishma lays down his bow; he falls

BH_X = 800


def s_down(cr, t, tl, t0, t1):
    c = cues(tl, "b15")
    lay = prog(t, c["D"], 0.9)
    fire = c["A"]

    def behind(cc):
        C.ghost(cc, "amba", 360, FEET - 20, 0.92, 0.8, t=t, glow=1.3)

    def actors(cc):
        pa = C.pose(t, 0.4, 0.5, mood="fierce", turn=0.4, gaze=(0.9, 0.0), armL=C.BOW_DRAW, armR=C.BOW_HOLD,
                    handL="fist", handR="fist", bend=0.3)
        oa = C.fig(cc, C.ARJUNA, 165, FEET - 40, 0.54, t, pa)
        draw_bow(cc, oa, t, 1.0, True, 400, 0.54, hand="R")
        ps = C.pose(t, 0.5, 0.5, mood="calm", turn=0.4, gaze=(0.8, 0.0), armL=C.BOW_REST, armR=C.AKIMBO,
                    handL="fist", handR="fist", bend=0.25)
        os_ = C.fig(cc, C.SHIKHANDI, 360, FEET, 0.64, t, ps)
        draw_bow(cc, os_, t, 0.0, False, 400, 0.64)
        pb = C.pose(t, 0.4 * (1 - lay), 0.4, mood="calm" if lay < 0.5 else "joy", turn=-0.45, gaze=(-0.8, 0.0),
                    lid=0.6 * lay, armL=C.mix(REST_DN, PALM_DN, lay), armR=C.mix(C.BOW_REST, (0.5, 0.2, 0.0), lay),
                    handL="open", handR="open" if lay > 0.6 else "fist", bend=0.2 + 0.15 * lay)
        ob = C.fig(cc, C.BHISHMA, BH_X, FEET, 0.84, t, pb)
        hb = C.U(cc, ob["handR"])
        bx = hb[0] + (930 - hb[0]) * lay
        by = hb[1] + (FEET - 25 - hb[1]) * lay
        C.bow(cc, bx, by, 420 * 0.84, 1, rot=1.57 * lay, lw=0.84)
        return {"a": oa, "s": os_, "b": ob}

    def extra(cc, pts):
        o = pts[0]
        hb = C.U(cc, o["a"]["handR"])
        bc = C.U(cc, o["b"]["chest"])
        for k in range(4):
            u = (t - fire - 0.22 * k) / 0.45
            tgt = (bc[0] - 40 + 25 * k, bc[1] - 60 + 70 * k)
            C.streak(cc, (hb[0] + 30, hb[1] - 10), tgt, u, 1.0, 380, 1.1)
            if 1.0 < u < 2.2:
                Y.sparkle(cc, tgt[0], tgt[1], 55 * (2.2 - u), (2.2 - u) / 1.2)
        g = prog(t, fire + 0.4, 0.5)
        Y.glow(cc, bc[0], bc[1], 380, 0.4 * g, C.GOLDL)

    def ui(cc, pts):
        heads(cc, t, [(t0 - 0.05, "ಭೀಷ್ಮ", "ಆಯುಧ ಕೆಳಗಿಟ್ಟ", c["D"] - t0 + 0.1),
                      (fire, "ಅರ್ಜುನನ", "ಬಾಣಗಳು!", 0.2)])

    Y.compose(cr, t, [actors], "indigo", "rays", extra=extra, ui=ui, behind=behind, zoom=zoom(t, t0, t1, 1.0, 1.03))


PALM_DN = (0.40, -0.35, 0.6)          # an open hand held out low, palm down (laying the weapon down)


def s_fall(cr, t, tl, t0, t1):
    c = cues(tl, "b15")
    u = clamp((t - t0 - 0.05) / 1.9)                       # the slow sink, eased in and out
    f = 0.5 - 0.5 * math.cos(math.pi * u)
    lit = clamp((f - 0.55) / 0.45)
    rev = prog(t, c["R"], 0.8)
    s = 0.6
    ang = -1.5 * f
    fx, fy = 900, FEET + (1530 - FEET) * f                 # his feet rise onto the bed as he leans back

    def actors(cc):
        if lit >= 0.99:
            return {}
        pb = dict(mood="joy", armL=(0.10, 0.05, 0.0), armR=(0.10, 0.05, 0.0), bend=0.02)
        cc.save()
        cc.translate(fx, fy)
        cc.rotate(ang)
        o = Y.figure(cc, C.BHISHMA, 0, 0, s, t, pb, alpha=1 - lit)
        cc.restore()
        return o

    def extra(cc, pts):
        C.light_bed(cc, t, 230, 930, 1560, FEET, prog(t, t0, 0.5), 19)
        C.ghost(cc, "bhishma", fx, fy, s, lit, col=C.GOLDL, rot=ang, t=t)
        if rev > 0:
            C.ghost(cc, "amba", 540, 1180 - 120 * rev, 0.55, rev, t=t, glow=1.4)
            Y.sparks(cc, t, 540, 900, 200, 9, rev, 0.4, seed=7)

    def ui(cc, pts):
        heads(cc, t, [(t0 - 0.05, "ಅರ್ಜುನನ ಬಾಣಗಳಿಂದ", "ಭೀಷ್ಮ ಬಿದ್ದ", 0.3),
                      (c["R"], "ಅಂಬೆಯ ಸೇಡು", "ಪೂರ್ತಿ ಆಯ್ತು!", 0.25)])

    Y.compose(cr, t, [actors], "indigo", "rays", extra=extra, ui=ui, light_strength=0.8,
              zoom=zoom(t, t0, t1, 1.0, 1.04, 540, 1500))


# ------------------------------------------------------------------ b16: who brought Bhishma down?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "b16")

    def actors(cc):
        pa = C.pose(t, 0.6, 0.5, mood="fierce", turn=0.3, gaze=(0.5, -0.3), armL=C.BOW_REST, armR=C.AKIMBO,
                    handL="fist", handR="fist", bend=0.25)
        oa = C.fig(cc, C.ARJUNA, 270, FEET, 0.58, t, pa)
        draw_bow(cc, oa, t, 0.0, False, 400, 0.58)
        pm = C.pose(t, 0.6, 0.5, ph=1.5, mood="calm", turn=-0.3, gaze=(-0.5, -0.3), armL=C.AKIMBO,
                    armR=(0.35, 2.05, 0.0), handL="fist", handR="open")
        om = C.fig(cc, C.AMBA, 810, FEET, 0.64, t, pm)
        return {"a": oa, "m": om}

    def extra(cc, pts):
        C.light_bed(cc, t, 430, 690, 1690, FEET, 0.7, 8)   # the fallen Bhishma, small, between them
        C.ghost(cc, "bhishma", 690, 1695, 0.27, 0.9, col=C.GOLDL, rot=-1.5, t=t)

    def ui(cc, pts):
        Y.kn_headline(cc, t, "ಭೀಷ್ಮನನ್ನ ಸೋಲಿಸಿದ್ದು", "ಯಾರು?", t0 - 0.05, t0 + 0.25, y=SY_Y, small_size=76,
                      big_size=170)
        which = -1
        if t >= c["A"]:
            which = 0 if t < c["M"] else 1
            if t >= c["M"] + 0.7:
                which = int((t - c["M"] - 0.7) / 0.6 + 1) % 2
        for k, (x, txt) in enumerate(((275, "ಅರ್ಜುನ?"), (805, "ಅಂಬೆ?"))):
            C.card(cc, t, t0 + 0.25 + 0.15 * k, x, 700, 440, 200, [(txt, 104, Y.YEL)], rot=(-0.03, 0.03)[k],
                   lit=1.0 if which == k else 0.0)
            if which == k:
                C.red_ring(cc, x, 700, 270, 145, prog(t, c["A"] if k == 0 else c["M"], 0.35)
                           if t < c["M"] + 0.7 else 1.0, 1.0, 10)

    Y.compose(cr, t, [actors], "green", "plain", extra=extra, ui=ui, zoom=zoom(t, t0, t1, 1.0, 1.03))


# ------------------------------------------------------------------ the cut list

SHOTS = [
    ("b1", None, s_hook),
    ("b2", None, s_story),
    ("b3", None, s_bhishma),
    ("b4", None, s_amba1),
    ("b4", "F", s_amba2),
    ("b4", "T", s_amba3),
    ("b5", None, s_love),
    ("b6", None, s_alone),
    ("b7", None, s_vow),
    ("b8", None, s_pray),
    ("b8", "S", s_shiva),
    ("b9", None, s_fire),
    ("b10", None, s_birth),
    ("b11", None, s_yaksha),
    ("b12", None, s_war),
    ("b12q", None, s_question),
    ("b13", None, s_rule),
    ("b14", None, s_chariot),
    ("b15", None, s_down),
    ("b15", "G", s_fall),
    ("b15c", None, s_callback),
    ("b16", None, s_end),
]


def _starts(tl):
    st = getattr(tl, "_sy_starts", None)
    if st is None:
        st = []
        for k, (bid, cu, _) in enumerate(SHOTS):
            if k == 0:
                st.append(0.0)
                continue
            s = T(tl, bid) if cu is None else cues(tl, bid)[cu] - CUT_LEAD
            st.append(max(s, st[-1] + MIN_SHOT))
        tl._sy_starts = st
    return st


def shot_at(t, tl):
    st = _starts(tl)
    k = max(i for i, s in enumerate(st) if t >= s)
    return k, st[k], st[k + 1] if k + 1 < len(st) else tl.total


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl)
    cr.save()
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    SHOTS[k][2](cr, t, tl, t0, t1)
    cr.restore()
    if k > 0 and t - t0 < 0.2:                           # the lamps dip for a moment on a scene change
        darken(cr, 0.4 * (1 - (t - t0) / 0.2), (0.02, 0.01, 0.0))


def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a conch
    as Shiva appears, shimmer as the yaksha's light and hers cross, a bell on the closing question, a single soft hit
    as Bhishma falls, then (only where they fit) shimmer as the arrows spark off Bhishma, a damaru as the war begins,
    a hit as he takes Amba. Chosen in THAT order, each at least SFX_MIN_GAP from every sound already kept (as
    render_myth.calm_sfx keeps them), so the list returned is what plays (about 6 sounds); bed dips before the
    reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["b8"]["S"], "conch", 0), (c["b11"]["K"], "shimmer", 0), (c["b16"]["Q"], "bell", 0),
            (c["b15"]["G"], "hit", 0), (c["b3"]["K"], "shimmer", 0), (c["b12"]["Y"], "damaru", 0),
            (c["b4"]["F"], "hit", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["b8"]["S"] - 0.3, "dip", 0.45), (c["b11"]["K"] - 0.3, "dip", 0.45), (c["b15"]["G"] - 0.35, "dip", 0.5),
            (c["b15c"]["H"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
