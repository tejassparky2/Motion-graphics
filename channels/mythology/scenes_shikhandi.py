"""Scenes for videos/shikhandi.py: "Bhishma was brought down by a warrior who, in his last life, was a girl" (Amba
and Shikhandi; Mahabharata, Udyoga Parva 173-195 and Bhishma Parva 108), in Togalu Gombeyaata (Karnataka leather
shadow-puppet theatre) drawn in code: the same lamp-lit screen, two-tier headlines and rod-puppet motion as the
Jarasandha, Kaikeyi, Lakshman Rekha, Mandhata, Jayadratha, Arjuna, Ruru, Dharmavyadha and Shani reels, with the cast
from shikhandi_cast. Rewritten 12 Nov 2026 for the kid-clear script (owner: "story clear so even a kid can
understand"): one idea on the screen at a time, plain English labels, only the five names spoken (Amba, Bhishma,
Shiva, Shikhandi, Arjuna). One device carries the idea: a girl's GLOWING SILHOUETTE behind a warrior (the hook, his
rule, the end), and two lights, a warm one and a green one, that cross when the bodies are exchanged.

Respect: Bhishma, Shiva, the kings and every woman with dignity. No gore at all: Amba walks into the fire's light and
is gone (a warm white wash, then a glow rising, nothing burns); the exchange is two lights crossing; arrows only
streak and spark; Bhishma's fall onto the bed of arrows is a silhouette against the setting sun.

Hindi only now (the Kannada channel gets another style); the Kannada cue words are kept so the module still runs for
kn. Every frame is a pure function of t. English on-screen text, except the name she is given (शिखंडी / ಶಿಖಂಡಿ) in
the viewer's script, shaped by matplotlib with Nirmala (left out without the font). Cues are words of the line
({"hi": ..., "kn": ...}) with a fraction fallback, in one table (CUES) that the scenes and sfx() both read, with
minimum gaps. Timeline caches live under "_sk_" names only (this module never uses shots.shot_at).

Shot list (line: what is on the screen)
  b1  HOOK, frame 0: a warrior (Shikhandi, armour, bow drawn) with a girl's golden glowing silhouette standing behind
      him, and Bhishma toppling back at the right: BHISHMA FELL TO A WARRIOR WHO WAS / ONCE A GIRL (in by 0.3 s); on
      "aise yoddha" an arrow streaks; on "giraya" Bhishma falls flat in a puff of dust; on "pichhle" the girl's glow
      flares (HIS LAST LIFE); on "ladki" the big line is underlined
  b2  THIS IS NOT A / FILM STORY (crossed out); a palm-leaf book opens: MAHABHARATA, BOOK 5: UDYOGA PARVA (ringed);
      IT'S WRITTEN IN THE / MAHABHARATA
  b3  Amba alone in the palace (tag AMBA): AMBA WAS A / PRINCESS; Bhishma strides in and reaches for her, she
      recoils: BHISHMA TOOK HER / BY FORCE; his chariot carries her away: FOR HIS BROTHER'S / WEDDING
  b4  Amba holds out a garland to the king she loved (tag): BUT AMBA LOVED / ANOTHER KING; she walks to him: SHE WENT
      BACK / TO HIM; he turns his back, the garland falls: BUT THE KING / REJECTED HER
  b5  Amba sinks down in tears, the wilted garland: AMBA'S LIFE WAS / RUINED; she rises with her fist up, a far
      Bhishma ringed: AMBA VOWED: card I WILL KILL / BHISHMA!
  b6  a tiny Amba before a giant, glowing Bhishma: BUT BEATING BHISHMA WAS / IMPOSSIBLE; then Amba with matted hair,
      arms raised, while suns, rain and snow pass and a YEAR counter runs: SO FOR YEARS, AMBA / PRAYED HARD
  b7  Shiva appears in a burst of light with his trident (tag SHIVA): THEN / SHIVA APPEARED; card IN YOUR NEXT
      LIFE... / YOU WILL KILL BHISHMA
  b8  she walks toward a great sacred fire: IN THAT VERY / MOMENT; she enters its light, a warm white wash, a glow
      rises: SHE GAVE UP / HER LIFE
  b9  the glow comes down into a cradle between a king (tag A KING) and his queen: SHE WAS BORN AGAIN / IN A KING'S
      HOME; the baby glows: AS A / DAUGHTER; HER NAME: / SHIKHANDI (tag, the name in script)
  b10 the dark forest: the grown princess walks in (teal sari, saffron pallu): WHEN SHIKHANDI / GREW UP; a tall
      glowing green yaksha appears (tag A FOREST YAKSHA): SHE MET A / FOREST YAKSHA; a warm light and a green light
      cross, a flash, and she stands there as a man (the same teal and saffron): THEY / SWAPPED BODIES; armour and a
      bow: SHIKHANDI BECAME A / MALE WARRIOR
  b11 two armies at sunrise: THEN CAME THE / MAHABHARATA WAR; Bhishma in his golden ring, enemy arrows sparking out
      before they reach him, a DAY counter running to 10: FOR 10 DAYS, NO ONE COULD / BEAT BHISHMA
  b12 Bhishma, his palm up: BHISHMA HAD A / RULE; Shikhandi at the left, a girl's glowing silhouette behind him;
      card ANYONE WHO WAS EVER A WOMAN, / I WON'T FIGHT THEM!
  b13 the chariot rolls in, Arjuna at the back (tags); Shikhandi steps to the very front, a red arrow: SO ARJUNA PUT
      SHIKHANDI / IN FRONT
  b14 Bhishma lowers his bow and shuts his eyes: BHISHMA / LOWERED HIS BOW; Arjuna's arrows streak past Shikhandi:
      AND ARJUNA'S / ARROWS; Bhishma falls back onto a bed of arrows, a silhouette against the sun: BHISHMA / FELL;
      Amba's glowing silhouette rises behind him: FROM HER LAST LIFE: / AMBA'S REVENGE
  b15 WHO BROUGHT / BHISHMA DOWN?; cards ARJUNA? / AMBA?, a red ring alternating; Arjuna and Amba small under them,
      the bed of arrows between
"""
import math

import cairo

import jayadratha_cast as J
import mandhata_cast as M
import puppet_core as pc
import shikhandi_cast as SK
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, back, clamp, ease, prog
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_arjuna import card2, cloud_text
from scenes_dharmavyadha import eye_of, script_strip, tears
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, motes, red_ring, walk_legs, woman_angles
from scenes_jayadratha import NIGHT, arjuna, arrow_at, flash_at, silhouette, soldier, tag, tint, title_lift, to_user
from scenes_kaikeyi import ANJALI, card, fig
from scenes_lakshman_rekha import big_q, book, sparkle
from scenes_mandhata import aura, burst, held, lights, mix, reach_arm, warm
from scenes_ravana import dotted, head2
from scenes_ruru import held_grip, plate
from shots import T, starts

MISSES = set()                       # cue words not found in a line (falls back to fractions)
G = FEET + 120                       # the ground line of most sets
SEAM = 540                           # the hook's seam
WARM_C = (1.0, 0.80, 0.42)           # Amba's light
GREEN_C = (0.55, 1.0, 0.50)          # the Yaksha's light
HEART = dict(front=(-0.3, -2.45), backa=(0.12, -0.25))          # a hand at the heart
BODY = {"hi": "शरीर", "kn": "ದೇಹ"}                               # the spoken word "body" (b1)
NAME_F = {"hi": "शिखंडिनी", "kn": "ಶಿಖಂಡಿನಿ"}                    # her name (b8)
NAME_M = {"hi": "शिखंडी", "kn": "ಶಿಖಂಡಿ"}                        # his name (b13)


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, words)
    except (KeyError, ValueError):
        MISSES.add((bid, words[getattr(tl, "lang", "hi")] if isinstance(words, dict) else words))
        return T(tl, bid, frac)


# Every cue of every line: (name, {"hi": word, "kn": word}, fraction fallback, ((after, min gap), ...)); "t0" = the
# line's start. Words are exact substrings of the script lines, each the first place that word occurs in its line
# (checked: MISSES stays empty for both languages).
CUES = {
    "b1": (("W", {"hi": "ऐसे", "kn": "ಒಬ್ಬ ಯೋಧ"}, 0.35, (("t0", 0.6),)),
           ("G", {"hi": "हराया", "kn": "ಸೋಲಿಸಿದ"}, 0.5, (("W", 0.5),)),
           ("P", {"hi": "पिछले", "kn": "ಹಿಂದಿನ"}, 0.7, (("G", 0.6),)),
           ("L", {"hi": "लड़की", "kn": "ಹುಡುಗಿ"}, 0.9, (("P", 0.4),))),
    "b2": (("M", {"hi": "महाभारत", "kn": "ಮಹಾಭಾರತದ"}, 0.25, (("t0", 0.2),)),
           ("S", {"hi": "सच्ची", "kn": "ನಿಜವಾದ"}, 0.6, (("M", 0.4),))),
    "b3": (("T", {"hi": "योद्धा", "kn": "ಯೋಧ"}, 0.3, (("t0", 0.5),)),
           ("K", {"hi": "कोई", "kn": "ಯಾರೂ"}, 0.6, (("T", 0.7),)),
           ("N", {"hi": "नहीं", "kn": "ಸೋಲಿಸೋಕಾಗ್ತಿರಲಿಲ್ಲ"}, 0.8, (("K", 0.3),))),
    "b4": (("A", {"hi": "अंबा", "kn": "ಅಂಬೆ"}, 0.15, (("t0", 0.4),)),
           ("F", {"hi": "उठा", "kn": "ಬಲವಂತವಾಗಿ"}, 0.55, (("A", 1.0),)),
           ("W", {"hi": "शादी", "kn": "ಮದುವೆಗೆ"}, 0.85, (("F", 0.9),))),
    "b5": (("S", {"hi": "राजा", "kn": "ರಾಜನನ್ನ"}, 0.15, (("t0", 0.3),)),
           ("L", {"hi": "प्यार", "kn": "ಪ್ರೀತಿಸ್ತಿದ್ಳು"}, 0.3, (("S", 0.4),)),
           ("F", {"hi": "गई", "kn": "ಹೋದಾಗ"}, 0.5, (("L", 1.0),)),
           ("R", {"hi": "कहा", "kn": "ಹೇಳಿದ"}, 0.7, (("F", 0.9),))),
    "b6": (("A", {"hi": "अकेली", "kn": "ಒಂಟಿಯಾದ್ಳು"}, 0.15, (("t0", 0.3),)),
           ("B", {"hi": "भीष्म", "kn": "ಭೀಷ್ಮನಿಂದಾನೇ"}, 0.65, (("A", 1.0),))),
    "b7": (("V", {"hi": "खाई", "kn": "ಶಪಥ"}, 0.25, (("t0", 0.3),)),
           ("K", {"hi": "हराकर", "kn": "ಸೋಲಿಸೇ"}, 0.7, (("V", 0.6),))),
    "b8": (("Y", {"hi": "सालों", "kn": "ವರ್ಷಗಟ್ಟಲೆ"}, 0.08, ()),
           ("P", {"hi": "पूजा", "kn": "ಪೂಜೆ"}, 0.3, (("Y", 0.6),)),
           ("S", {"hi": "आए", "kn": "ಬಂದು"}, 0.5, (("P", 1.1),)),
           ("N", {"hi": "अगले", "kn": "ಮುಂದಿನ"}, 0.7, (("S", 0.8),)),
           ("K", {"hi": "हराओगी", "kn": "ಸೋಲಿಸ್ತೀಯ"}, 0.9, (("N", 0.6),))),
    "b9": (("F", {"hi": "आग", "kn": "ಬೆಂಕಿಗೆ"}, 0.3, (("t0", 0.3),)),
           ("J", {"hi": "जन्म", "kn": "ಜನ್ಮ"}, 0.75, (("F", 0.8),))),
    "b10": (("J", {"hi": "जन्म", "kn": "ಜನ್ಮದಲ್ಲಿ"}, 0.1, (("t0", 0.2),)),
            ("K", {"hi": "राजा", "kn": "ರಾಜನ"}, 0.3, (("J", 0.4),)),
            ("B", {"hi": "बेटी", "kn": "ಮಗಳಾಗಿ"}, 0.55, (("K", 0.7),)),
            ("N", {"hi": "शिखंडी", "kn": "ಶಿಖಂಡಿ"}, 0.9, (("B", 0.9),))),
    "b11": (("Y", {"hi": "जादुई", "kn": "ಮಾಯಾವಿ"}, 0.25, (("t0", 0.9),)),
            ("S", {"hi": "शरीर", "kn": "ದೇಹವನ್ನ"}, 0.5, (("Y", 1.1),)),
            ("N", {"hi": "शिखंडी", "kn": "ಶಿಖಂಡಿ"}, 0.72, (("S", 1.1),)),
            ("M", {"hi": "लड़का", "kn": "ಗಂಡು"}, 0.85, (("N", 0.4),))),
    "b12": (("Y", {"hi": "युद्ध", "kn": "ಯುದ್ಧ"}, 0.25, (("t0", 0.3),)),
            ("D", {"hi": "दस", "kn": "ಹತ್ತು"}, 0.5, (("Y", 0.9),)),
            ("N", {"hi": "नहीं", "kn": "ಸೋಲಿಸೋಕಾಗಲಿಲ್ಲ"}, 0.85, (("D", 0.6),))),
    "b12q": (("Q", {"hi": "कैसे", "kn": "ಹೇಗೆ"}, 0.6, (("t0", 0.3),)),),
    "b13": (("R", {"hi": "नियम", "kn": "ನಿಯಮ"}, 0.2, (("t0", 0.3),)),
            ("G", {"hi": "लड़की", "kn": "ಹುಡುಗಿಯಾಗಿದ್ದವರ"}, 0.5, (("R", 0.9),)),
            ("F", {"hi": "नहीं", "kn": "ಯುದ್ಧ"}, 0.8, (("G", 0.6),))),
    "b14": (("A", {"hi": "अर्जुन", "kn": "ಅರ್ಜುನ"}, 0.1, (("t0", 0.1),)),
            ("S", {"hi": "शिखंडी", "kn": "ಶಿಖಂಡಿಯನ್ನ"}, 0.3, (("A", 0.4),)),
            ("R", {"hi": "रथ", "kn": "ರಥದಲ್ಲಿ"}, 0.55, (("S", 0.5),)),
            ("F", {"hi": "आगे", "kn": "ಮುಂದೆ"}, 0.8, (("R", 0.4),))),
    "b15": (("D", {"hi": "हथियार", "kn": "ಆಯುಧ"}, 0.12, (("t0", 0.3),)),
            ("A", {"hi": "अर्जुन", "kn": "ಅರ್ಜುನನ"}, 0.4, (("D", 0.9),)),
            ("G", {"hi": "गिर", "kn": "ಬಿದ್ದ"}, 0.65, (("A", 1.0),)),
            ("R", {"hi": "बदला", "kn": "ಸೇಡು"}, 0.85, (("G", 0.8),))),
    "b15c": (("R", {"hi": "रोई", "kn": "ಅತ್ತ"}, 0.35, (("t0", 0.4),)),
             ("N", {"hi": "अगले", "kn": "ಮುಂದಿನ"}, 0.6, (("R", 0.8),)),
             ("H", {"hi": "हार", "kn": "ಸೋಲಾದಳು"}, 0.88, (("N", 0.5),))),
    "b16": (("Q", {"hi": "किसने", "kn": "ಯಾರು"}, 0.3, (("t0", 0.3),)),
            ("A", {"hi": "अर्जुन", "kn": "ಅರ್ಜುನನಾ"}, 0.5, (("Q", 0.4),)),
            ("M", {"hi": "अंबा", "kn": "ಅಂಬೆನಾ"}, 0.65, (("A", 0.4),)),
            ("C", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.85, (("M", 0.4),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_sk_cues", None)
    if cache is None:
        cache = {}
        tl._sk_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, words, frac, cons in CUES[bid]:
            v = cue(tl, bid, words, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


def lang(tl):
    return getattr(tl, "lang", "hi")


def shot_at(t, tl, shots):
    """shots.shot_at with the cut list cached under this module's own name (tl._sk_starts)."""
    cached = getattr(tl, "_sk_starts", None)
    if cached is None:
        cached = tl._sk_starts = starts(tl, shots)
    k = max(i for i, s in enumerate(cached) if t >= s)
    return k, cached[k], cached[k + 1] if k + 1 < len(cached) else tl.total


# ------------------------------------------------------------------ small helpers


def ground(cr, y=G, alpha=1.0):
    prop(cr, "ground", W / 2, y + 6, 0.82, alpha=alpha)


def orb(cr, t, x, y, r, a, col=WARM_C):
    """A soft ball of light (Amba's warm one, the Yaksha's green one): a glow, a few turning rays, a bright core."""
    if a <= 0.01:
        return
    glow(cr, x, y, r * 4.2, 0.75 * a)
    warm(cr, x, y, r * 2.6, 0.8 * a, col)
    aura(cr, t, x, y, r * 0.8, r * 2.2, 0.7 * a, n=12, spin=0.7, col=col)
    cr.save()
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 1.0, 1.0, 0.96, a)
    g.add_color_stop_rgba(0.6, *col, 0.95 * a)
    g.add_color_stop_rgba(1, *[c * 0.8 for c in col], 0.0)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()
    sparkle(cr, x, y, r * 1.3, a, (1.0, 0.97, 0.85))


def arc_pos(p0, p1, u, lift):
    """A point a fraction u along an arc from p0 to p1 (lift > 0 bows it upward)."""
    e = u * u * (3 - 2 * u)
    return (p0[0] + (p1[0] - p0[0]) * e, p0[1] + (p1[1] - p0[1]) * e - lift * 4 * e * (1 - e))


def cross_lights(cr, t, t_go, pa, pb, dur=0.9, lift=220.0, settle=True, r=30.0, t_wake=None):
    """The exchange: the two lights wake at t_wake (default just before t_go) at pa (warm) and pb (green); at t_go they
    leave, cross on two arcs (one high, one low) and each settles into the other figure. Returns 0..1 (how far
    along)."""
    t_wake = t_go - 0.6 if t_wake is None else t_wake
    if t < t_wake:
        return 0.0
    u = clamp((t - t_go) / dur)
    pre = prog(t, t_wake, 0.5)
    after = 1 - 0.6 * prog(t, t_go + dur + 0.3, 0.8) if settle else 1.0
    wa = arc_pos(pa, pb, u, lift)
    ga = arc_pos(pb, pa, u, -lift * 0.6)
    trail = pre * (1 - prog(t, t_go + dur, 0.5))
    if trail > 0.01 and u > 0:                                      # ribbons of light behind each
        cr.save()
        cr.set_operator(cairo.OPERATOR_ADD)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        for p0, p1, lf, col in ((pa, pb, lift, WARM_C), (pb, pa, -lift * 0.6, GREEN_C)):
            pts = [arc_pos(p0, p1, u * i / 24, lf) for i in range(25)]
            for lw, k in ((26, 0.12), (10, 0.3), (3, 0.7)):
                cr.move_to(*pts[0])
                for p in pts[1:]:
                    cr.line_to(*p)
                cr.set_source_rgba(*col, k * trail)
                cr.set_line_width(lw)
                cr.stroke()
        cr.restore()
    for k in range(5):                                              # short trails
        uu = max(0.0, u - 0.05 * (k + 1))
        if 0 < u < 1:
            sparkle(cr, *arc_pos(pa, pb, uu, lift), 20 - 3 * k, 0.8 - 0.14 * k, WARM_C)
            sparkle(cr, *arc_pos(pb, pa, uu, -lift * 0.6), 20 - 3 * k, 0.8 - 0.14 * k, GREEN_C)
    orb(cr, t, *wa, r, pre * after, WARM_C)
    orb(cr, t, *ga, r, pre * after, GREEN_C)
    if 0.42 < u < 0.62:                                             # the moment they pass each other
        mx, my = (pa[0] + pb[0]) / 2, (pa[1] + pb[1]) / 2
        sparkle(cr, mx, my - 30, 90 * math.sin(math.pi * (u - 0.42) / 0.2), 1.0)
    return u


def wash(cr, a, col=(1.0, 0.93, 0.78)):
    """A warm white light over everything (the fire's light filling the screen)."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_source_rgba(*col, clamp(a))
    cr.paint()
    cr.restore()


def card_back(cr, t, t_in, x, y, s):
    """An opaque parchment backing under a card2 plaque (same drop-in and sway), so the leather card stays readable
    over the dark forest (the plaque sprite itself is translucent)."""
    q = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(q)
    if a <= 0.01:
        return
    yy = y + 60 * (1 - q)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(sway(t, 0.01, 0.4, x * 0.01))
    cr.scale(s, s)
    w, h, c = 372, 112, 30
    pc.poly(cr, [(-w, -h + c), (-w + c, -h), (w - c, -h), (w, -h + c), (w, h - c), (w - c, h), (-w + c, h),
                 (-w, h - c)])
    cr.set_source_rgba(0.98, 0.90, 0.70, 0.92 * a)
    cr.fill()
    cr.restore()


def dust(cr, t, x, y, a, n=8, ph=0.0):
    """Dust kicked up behind a moving chariot."""
    for i in range(n):
        u = ((t * 1.6 + i / n + ph) % 1.0)
        r = 30 + 90 * u
        cr.save()
        cr.set_source_rgba(0.55, 0.36, 0.18, 0.22 * a * (1 - u))
        cr.arc(x - 160 * u - 30 * (i % 3), y - 30 * u - 20 * (i % 2), r, 0, 2 * math.pi)
        cr.fill()
        cr.restore()


def forest(cr, t, a=1.0, x_off=0.0):
    """The dark forest: tree silhouettes at three depths."""
    for x, s, bl, al, fl in ((100, 0.84, 0.0, 0.92, False), (980, 0.86, 0.0, 0.92, True), (380, 0.6, 6.0, 0.6, True),
                             (720, 0.66, 6.0, 0.6, False), (560, 0.42, 12.0, 0.4, False)):
        silhouette(cr, lambda c_, x=x, s=s, bl=bl, fl=fl: prop(c_, "tree", x + x_off * (1 - bl / 12), G + 30, s,
                                                                rot=sway(t, 0.006, 0.3, x * 0.01), blur=bl, flip=fl),
                   al * a, (0.06, 0.08, 0.06))


def fireflies(cr, t, a, x=540, y=1300, r=460):
    lights(cr, t, x, y, r, 10, 0.6 * a, (0.80, 1.0, 0.55), 0.2)


# ------------------------------------------------------------------ puppets


def lady(cr, rig, key, t, x, s, mood="open", base="open", feet=G, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0,
         hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.4, y=None):
    """A woman puppet standing (feet on `feet`); her head per mood (`base` = the plain head's mood)."""
    hy = feet - 470 * s if y is None else y
    ang = woman_angles(key, t, front, backa, head, hits, ph)
    swap = {key + "_head": key + "_head" + ("" if mood == base else "_" + mood)}
    return puppet(cr, rig, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, swap=swap, rods=rods)


def amba(cr, t, x, s, mood="open", **kw):
    return lady(cr, SK.AMBA, "sk_amba", t, x, s, mood, **kw)


def tapas(cr, t, x, s, mood="fierce", **kw):
    return lady(cr, SK.TAPAS, "sk_tapas", t, x, s, mood, "fierce", **kw)


def queen(cr, t, x, s, mood="open", **kw):
    return lady(cr, SK.QUEEN, "sk_queen", t, x, s, mood, **kw)


def man_fig(cr, rig, key, t, x, s, mood, base="calm", swap=None, **kw):
    """A man() puppet standing (feet on G unless given), his head per mood."""
    sw = dict(swap or {})
    sw[key + "_head"] = key + "_head" + ("" if mood == base else "_" + mood)
    kw.setdefault("feet", G)
    return fig(cr, rig, key, t, x, s, swap=sw, **kw)


BOW_S = 0.66                         # Bhishma's bow in his hand (arm units)


def bhishma(cr, t, x, s, mood="calm", bow="hold", **kw):
    """Bhishma standing. bow: None | hold (upright in his back hand) | raise (high in his front hand) | low (in his
    front hand, lowered and pointing at the ground)."""
    a, b = kw.get("alpha", 1.0), kw.get("blur", 0.0)
    fr, ba = kw.setdefault("front", (-0.32, -0.55)), kw.setdefault("backa", (0.3, -0.25))
    ex = {}
    if bow == "hold":
        ex["sk_bhishma_armB_lo"] = held("sk_bow", ba, BOW_S, alpha=a, blur=b)
    elif bow == "raise":
        ex["sk_bhishma_armF_lo"] = held("sk_bow", fr, BOW_S, alpha=a, blur=b)
    elif bow == "low":
        ex["sk_bhishma_armF_lo"] = held("sk_bow", fr, BOW_S, dy=150, tilt=-1.15, alpha=a, blur=b)
    return man_fig(cr, SK.BHISHMA, "sk_bhishma", t, x, s, mood, extra=ex or None, **kw)


def salva(cr, t, x, s, mood="calm", **kw):
    return man_fig(cr, SK.SALVA, "sk_salva", t, x, s, mood, **kw)


def drupada(cr, t, x, s, mood="calm", **kw):
    return man_fig(cr, SK.DRUPADA, "sk_drupada", t, x, s, mood, **kw)


def yaksha(cr, t, x, s, mood="calm", **kw):
    return man_fig(cr, SK.YAKSHA, "sk_yaksha", t, x, s, mood, **kw)


def shk(cr, t, x, s, mood="open", war=False, bow=False, **kw):
    """Shikhandini / Shikhandi (the same face): war = the armour body; bow = a plain bow in the back hand."""
    sw = {"sk_shk_body": "sk_shk_body_war"} if war else None
    ex = dict(kw.pop("extra", None) or {})
    if bow:
        ba = kw.setdefault("backa", (0.3, -0.25))
        ex["sk_shk_armB_lo"] = held("ar_ybow", ba, 0.7, alpha=kw.get("alpha", 1.0), blur=kw.get("blur", 0.0))
    return man_fig(cr, SK.SHK, "sk_shk", t, x, s, mood, base="open", swap=sw, extra=ex or None, **kw)


SH_FRONT = (-0.95, -0.85)            # Shiva's front hand before his chest, the trident upright in it


def shiva(cr, t, x, s, mood="calm", **kw):
    """Shiva, his trident upright in his front hand (from the ground to above his head)."""
    fr = kw.setdefault("front", SH_FRONT)
    ex = {"sk_shiva_armF_lo": held_grip("sg_trishul", fr, 1.2, 0.0, -115.0, kw.get("alpha", 1.0),
                                        kw.get("blur", 0.0))}
    return man_fig(cr, SK.SHIVA, "sk_shiva", t, x, s, mood, extra=ex, **kw)


def glide(cr, t, fn, t0, t1, x0, x1, s, feet=G, t_in=None, **kw):
    """A woman puppet carried across the cloth in rod-puppet steps (she has no legs: only bob and rock)."""
    x, bob, rock, _ = hop_walk(t, t0, t1, x0, x1, 0.45)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    kw.setdefault("hits", [(t1, 1.0)])
    return fn(cr, t, x, s * k, y=feet - 470 * s + bob * 0.6 - (k - 1) * 300 * s, rot=rock * 0.6,
              alpha=a * kw.pop("alpha", 1.0), blur=b, feet=feet, **kw)


def stride(cr, t, fn, t0, t1, x0, x1, s, feet=G, t_in=None, step=0.42, **kw):
    """A man puppet walking in jerky rod-puppet steps (brought onto the cloth from t_in)."""
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    kw.setdefault("hits", [(t1, 1.0)])
    y = feet - 434 * s + bob - (k - 1) * 300 * s
    return fn(cr, t, x, s * k, legs=walk_legs(ph), rot=rock, alpha=a * kw.pop("alpha", 1.0), blur=b, y=y, feet=feet,
              **kw)


def clip_above(cr, y):
    """Clip to above the ground line (a puppet sinking down goes behind the stage edge)."""
    cr.save()
    cr.rectangle(-500, -500, W + 1000, y + 500)
    cr.clip()


def cradle(cr, t, x, ground_, s, baby=True, glow_a=0.0, alpha=1.0, blur=0.0, arms=(0.0, 0.0)):
    """The cradle (shani_cast's) with a baby (mandhata_cast's) in it. Returns the baby's head centre (scene)."""
    r = 0.025 * math.sin(t * 1.5)
    rim = ground_ + S_CRADLE_RIM * s
    bs = 0.6 * s
    hip = rim + 96 * bs
    head_c = (x, hip - 440 * bs)
    if glow_a > 0 and baby:
        glow(cr, head_c[0], head_c[1] + 60 * bs, 620 * bs + 60, glow_a * (0.88 + 0.12 * math.sin(t * 3.3)))
        aura(cr, t, head_c[0], head_c[1], 220 * bs, 720 * bs, 0.8 * glow_a * alpha)
    cr.save()
    cr.translate(x, ground_)
    cr.rotate(r)
    cr.translate(-x, -ground_)
    prop(cr, "sg_cradle_back", x, ground_, s, alpha=alpha, blur=blur)
    if baby:
        cr.save()
        cr.rectangle(-500, -500, W + 1000, rim + 8 * s + 500)
        cr.clip()
        ang = {"mb_armL": arms[0], "mb_armR": -arms[1]}
        puppet(cr, M.BABY, x, hip, bs, bob_rot(t, x * 0.01, 0.01), False, ang, alpha, blur,
               hide=("mb_legL", "mb_legR"), rods=False)
        cr.restore()
    prop(cr, "sg_cradle", x, ground_, s, alpha=alpha, blur=blur)
    cr.restore()
    pc.rod(cr, x + 200 * s, ground_ - 60 * s, x + 260 * s, H + 60, alpha=0.4 * alpha)
    return head_c


S_CRADLE_RIM = -330.0                # the cradle's front rim above the ground (shani_cast.CRADLE_RIM)


def chariot(cr, t, x, feet, s, riders=(), alpha=1.0, blur=0.0, horses=True, rods=True, ph=0.0, roll=0.0, gallop=0.0):
    """jayadratha_cast's chariot (pivot on the ground under the axle, the horses to the right) with any riders on its
    deck: riders = [(dx in chariot units, fn(cr, x, deck))], drawn behind the car's side panel. roll turns the wheel,
    gallop 0..1 makes the horses bound."""
    hx = x + J.HORSE_DX * s
    hb = -abs(math.sin(t * 9.0 + ph)) * 26 * s * gallop
    if horses:
        prop(cr, "jd_horse_far", hx + 80 * s, feet - 16 * s + hb * 0.8, s * 0.98,
             rot=sway(t, 0.006, 0.8, 1.0 + ph) + 0.03 * gallop * math.sin(t * 9 + 1), alpha=alpha, blur=blur + 1.5)
    prop(cr, "jd_chariot_back", x, feet, s, alpha=alpha, blur=blur)
    deck = feet - J.DECK * s
    cr.save()
    cr.new_path()
    cr.rectangle(-2000, -2000, W + 4000, H + 4000)
    pc.spath(cr, [(x + px * s, feet + py * s) for px, py in J.PANEL])
    cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    cr.clip()
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    cr.rectangle(-2000, -2000, W + 4000, deck + 2000 - 60 * s)
    cr.clip()
    out = [fn(cr, x + dx * s, deck) for dx, fn in riders]
    cr.restore()
    prop(cr, "jd_chariot", x, feet, s, alpha=alpha, blur=blur)
    if horses:
        prop(cr, "jd_horse", hx, feet + hb, s, rot=sway(t, 0.006, 0.8, ph) + 0.03 * gallop * math.sin(t * 9),
             alpha=alpha, blur=blur)
    prop(cr, "jd_wheel", x + J.WHEEL_XY[0] * s, feet + J.WHEEL_XY[1] * s, s, rot=roll + 0.04 * math.sin(t * 0.8),
         alpha=alpha, blur=blur)
    if rods:
        pc.rod(cr, x - 60 * s, feet - 420 * s, x - 110 * s, H + 60, alpha=0.6 * alpha, blur=blur)
        if horses:
            pc.rod(cr, hx, feet - 600 * s, hx + 40 * s, H + 60, alpha=0.6 * alpha, blur=blur)
    return out


def army(cr, t, xs, feet, s, raise_=0.0, flip=False, alpha=0.9, blur=0.0, march=0.0, dx=0.0):
    """A row of Kaurava-style soldiers as one dark silhouette (spears up with raise_); march > 0 walks them."""
    def fn(c_):
        for i, x in enumerate(xs):
            lg = walk_legs(math.sin(t * 7 + i)) if march > 0 else (0.0, 0.0)
            soldier(c_, t, x + dx, feet + 6 * math.sin(i * 1.7), s * (0.94 + 0.06 * math.sin(i * 2.3)),
                    raise_=raise_, flip=flip, ph=0.7 * i, blur=blur, legs=lg)
    silhouette(cr, fn, alpha)


def arrow_bed(cr, x, y, s, n=17):
    """The bed of arrows: arrows standing in the ground at slight angles, their fletchings up (fill only, for a
    silhouette)."""
    for i in range(n):
        u = i / (n - 1)
        ax = x + (u - 0.5) * 900 * s + 14 * math.sin(i * 3.7)
        ang = math.pi / 2 + 0.34 * math.sin(i * 2.3 + 0.5)
        L = (400 + 70 * math.sin(i * 1.3)) * s
        arrow_at(cr, ax - L * math.cos(ang), y - L * math.sin(ang), ang, L)


def bhishma_lying(cr, t, x, y_ground, s, p=1.0, alpha=1.0):
    """Bhishma falling back (p 0 -> 1) onto the bed of arrows at x, as one dark silhouette with the arrows."""
    q = ease(clamp(p))
    rot = (math.pi / 2) * q
    hy0 = y_ground - 434 * s
    hy1 = y_ground - 250 * s
    hy = hy0 + (hy1 - hy0) * q

    def fn(c_):
        if q > 0.2:
            arrow_bed(c_, x + 60 * s, y_ground, s)
        return bhishma(c_, t, x, s, mood="rest", bow=None, flip=True, rot=rot, y=hy, rods=False, front=(-0.2, -0.3),
                       backa=(0.25, -0.2), feet=y_ground)
    return silhouette(cr, fn, alpha, (0.08, 0.04, 0.03))


def sunset(cr, t, a=1.0, y=1250):
    """A low red-gold sun glow behind the battlefield."""
    if a <= 0.01:
        return
    glow(cr, 540, y, 900, 0.55 * a)
    warm(cr, 540, y, 700, 0.6 * a, (1.0, 0.45, 0.15))
    prop(cr, "sun", 540, y + 40, 0.9, rot=t * 0.1, alpha=0.75 * a)


def ghost(cr, fn, a, col=(1.0, 0.70, 0.22)):
    """A figure as a glowing spirit (a past life): whatever fn draws becomes a soft golden silhouette with its own
    details faint inside it."""
    if a <= 0.01:
        return None
    cr.push_group()
    res = fn(cr)
    pat = cr.pop_group()
    cr.save()                                                         # a deep amber rim, offset all round
    for dx, dy in ((-7, 0), (7, 0), (0, -7), (0, 7), (-5, -5), (5, 5), (-5, 5), (5, -5)):
        cr.save()
        cr.translate(dx, dy)
        cr.set_source_rgba(0.90, 0.42, 0.06, 0.16 * a)
        cr.mask(pat)
        cr.restore()
    cr.set_source_rgba(*col, 0.86 * a)                                # the golden body
    cr.mask(pat)
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source_rgba(1.0, 0.86, 0.55, 0.22 * a)
    cr.mask(pat)
    cr.restore()
    cr.save()
    cr.set_source(pat)
    cr.paint_with_alpha(0.3 * a)
    cr.restore()
    return res


def girl(cr, t, x, s, mood="open", **kw):
    return lady(cr, SK.GIRL, "sk_girl", t, x, s, mood, **kw)


def puff(cr, t, t0, x, y, a=1.0):
    """A puff of dust where something lands."""
    u = (t - t0) / 0.9
    if not 0 < u < 1:
        return
    for i in range(7):
        r = (30 + 110 * u) * (0.7 + 0.1 * (i % 4))
        cr.save()
        cr.set_source_rgba(0.55, 0.38, 0.20, 0.32 * a * (1 - u))
        cr.arc(x + (i - 3) * 60 * (0.4 + u), y - 30 * u - 15 * (i % 2), r, 0, 2 * math.pi)
        cr.fill()
        cr.restore()


def fly_arrow(cr, p0, p1, u, lift=60.0, a=1.0):
    """An arrow (with a light streak) a fraction u of the way from p0 to p1 on a shallow arc."""
    if not 0 <= u < 1:
        return
    px, py = arc_pos(p0, p1, u, lift)
    qx, qy = arc_pos(p0, p1, min(1.0, u + 0.05), lift)
    ang = math.atan2(qy - py, qx - px)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_source_rgba(1.0, 0.85, 0.55, 0.35 * a)
    cr.set_line_width(8)
    cr.move_to(px - 260 * math.cos(ang), py - 260 * math.sin(ang))
    cr.line_to(px - 120 * math.cos(ang), py - 120 * math.sin(ang))
    cr.stroke()
    cr.restore()
    arrow_at(cr, px - 120 * math.cos(ang), py - 120 * math.sin(ang), ang, 150, alpha=a)


# ------------------------------------------------------------------ b1  hook: a warrior who was once a girl


HK = dict(wx=390, ws=0.98, gx=215, gs=1.26, bx=740, bs=0.42, feet=1880)


def hook_scene(cr, t, q, ga, t_shots=(), hit=None):
    """The hook's image (also the callback before the end): the warrior, his bow drawn, a girl's golden glowing
    silhouette standing behind him (his last life), and Bhishma, a dark silhouette, falling back onto a bed of arrows
    at the right (q 0..1). Returns the girl's and Bhishma's points."""
    wx, ws, gx, gs, bx, bs, feet = (HK[k] for k in ("wx", "ws", "gx", "gs", "bx", "bs", "feet"))
    glow(cr, 380, feet - 640, 760, 0.45)
    store = {}
    glow(cr, gx, feet - 760 * gs, 420 + 160 * ga, 0.3 + 0.4 * ga)
    ghost(cr, lambda c_: store.setdefault("g", amba(c_, t, gx, gs, mood="open", feet=feet, rods=False, blur=4.0,
                                                    ph=0.3, **HEART)),
          0.8 + 0.2 * ga + 0.05 * math.sin(t * 3))
    if ga > 0.01:
        lights(cr, t, gx, feet - 900 * gs, 300, 10, 0.8 * ga)
    warm(cr, bx + 80, feet - 200, 420, 0.5, (1.0, 0.45, 0.15))
    bp = bhishma_lying(cr, t, bx, feet - 50, bs, q) or {}
    fr, ba = (-1.5, -0.12), (-1.35, -1.55)
    wp = shk(cr, t, wx, ws, mood="war", war=True, feet=feet, front=fr, backa=ba, ph=1.1, hits=hit or (),
             extra={"sk_shk_armF_lo": held("ar_ybow", fr, 0.74)})
    hand = to_user(cr, wp["handF"])
    chest = to_user(cr, bp["chest"]) if "chest" in bp else (bx, feet - 300 * bs)
    for ts in t_shots:                                                # arrows from his bow toward Bhishma
        fly_arrow(cr, (hand[0] + 60, hand[1] - 10), (chest[0], chest[1] - 20), (t - ts) / 0.55, 50)
    return store.get("g", {}), bp


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "b1")
    tW, tG, tP, tL = c["W"], c["G"], c["P"], c["L"]
    q = keyed(t, [(0.0, 0.3), (tG - 0.05, 1.0)], 0.5, 1.05)
    gp, _ = hook_scene(cr, t, q, prog(t, tP - 0.1, 0.4), (-0.45, tW, tW + 0.45), [(tW, 0.3)])
    puff(cr, t, tG + 0.4, HK["bx"] + 60, HK["feet"] - 60)
    gtop = gp.get("top", (HK["gx"], 800))

    def ui(cr):
        head2(cr, t, "THE WARRIOR WHO BEAT BHISHMA", -1.0, "WAS ONCE A GIRL", 0.3, big_size=230, ghost=-1.0,
              under=tL)
        plate(cr, t, tP + 0.05, "HIS LAST LIFE", max(gtop[0] + 10, 170), gtop[1] - 70, 32)
        tag(cr, t, 0.6, "BHISHMA", HK["bx"] + 90, 1440, 30)
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.2) + flash_at(t, tG + 0.4, 0.3) + flash_at(t, tP, 0.3))


# ------------------------------------------------------------------ b2  a true story


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "b2")
    tM, tS = c["M"], c["S"]
    leaves = [(None, [("MAHABHARATA", 92, HEAD_FONT)], 0),
              (tS - 0.1, [([("A TRUE", INK), ("STORY", RED)], 80, HEAD_FONT)], 0)]
    book(cr, t, 540, 960, 0.86, leaves, t_in=t0 - 0.1, t_open=tM - 0.1, ring=(1, 0, 1, tS + 0.3))

    def ui(cr):
        head2(cr, t, "A TRUE STORY FROM THE", t0 + 0.05, "MAHABHARATA", tM, big_size=210, under=tS + 0.2)
    return dict(ui=ui, flash=flash_at(t, tM, 0.25) + flash_at(t, tS, 0.2))


# ------------------------------------------------------------------ b3  Bhishma: the strongest warrior


def s_strong(cr, t, tl, t0, t1):
    c = cues(tl, "b3")
    tT, tK, tN = c["T"], c["K"], c["N"]
    glow(cr, 540, 1300, 680, 0.42)
    ground(cr)
    army(cr, t, (60, 150, 240), G, 0.46, raise_=0.6, alpha=0.6 * prog(t, tK - 0.3, 0.4), blur=2.0)
    bx, bs = 630, 0.9
    cy = G - 520 * bs
    shield(cr, t, bx, cy, 420 * bs, 0.5 + 0.5 * prog(t, tT, 0.4))
    b, k, a = depth(t, t0 - 0.2, 0.5)
    bp = bhishma(cr, t, bx, bs * k, mood="stern", flip=True, bow="raise", front=(-1.6, -0.25), ph=1.0, alpha=a, blur=b,
                 hits=[(tT, 0.3), (tN, 0.3)])
    for i in range(7):                                              # arrows spark out on his ring
        ts = tK - 0.1 + 0.3 * i
        u = (t - ts) / 0.4
        p0 = (280, G - 300 - 60 * math.sin(i * 1.7))
        ang = math.pi * (0.92 + 0.1 * math.sin(i * 2.3))
        p1 = (bx + 420 * bs * math.cos(ang), cy + 420 * bs * math.sin(ang))
        if 0 <= u < 1:
            fly_arrow(cr, p0, p1, u, 40)
        elif 1 <= u < 1.6:
            sparkle(cr, p1[0], p1[1], 46 * (1.6 - u), 1.0)
    btop = bp["top"]

    def ui(cr):
        if t < tK:
            head2(cr, t, "BHISHMA:", t0 + 0.05, "THE STRONGEST WARRIOR", tT, big_size=200)
        else:
            head2(cr, t, "NO ONE COULD", tK - 0.1, "BEAT HIM", tN, big_size=300, under=tN + 0.4)
        tag(cr, t, t0 + 0.3, "BHISHMA", min(btop[0], 860), btop[1] - 120, 36)
    return dict(ui=ui, flash=flash_at(t, tT, 0.2) + flash_at(t, tN, 0.2))


# ------------------------------------------------------------------ b4  Bhishma takes the princess Amba by force


AM3 = (650, 0.78)
BH3 = (300, 0.76)


def s_taken(cr, t, tl, t0, t1):
    c = cues(tl, "b4")
    tA, tF, tW = c["A"], c["F"], c["W"]
    tB = t0 + 0.45                                                  # "one day, Bhishma..." opens the line
    t_cut = tW - 0.2
    if t < t_cut:
        glow(cr, 600, 1250, 640, 0.4)
        prop(cr, "arch", 680, G + 10, 0.8, alpha=0.5, blur=6.0)
        ground(cr)
        alarm = keyed(t, [(t0, 0.0), (tA + 0.6, 1.0)], 0.25, 1.4)
        grab = keyed(t, [(t0, 0.0), (tF - 0.1, 1.0)], 0.3, 1.3)
        xa, sa = AM3[0] + 50 * grab, AM3[1]
        ap = amba(cr, t, xa, sa, mood="shock" if t > tA + 0.6 else "open", flip=True, ph=0.2,
                  front=mix((-0.08, -0.35), HEART["front"], alarm), head=-0.06 * alarm, rot=0.07 * grab,
                  hits=[(tA, 0.3), (tF, 0.4)])
        t_in = tB - 0.55
        bp = None
        bx, bs = BH3
        if t > t_in:
            if t < tB + 0.6:
                bp = stride(cr, t, bhishma, t_in, tB + 0.6, -260, bx, bs, mood="stern", bow="hold",
                            front=(-1.2, -0.4), ph=0.9)
            else:
                reach = reach_arm(bx, G - 434 * bs, bs, 26 * 1.1, (xa - 120, G - 470 * sa - 120))
                bp = bhishma(cr, t, bx, bs, mood="stern", bow="hold", front=mix((-1.2, -0.4), reach, grab),
                             hits=[(tF, 0.4)], ph=0.9)
        a_top = ap["top"]

        def ui(cr):
            if t < tF:
                head2(cr, t, "A PRINCESS NAMED", t0 + 0.05, "AMBA", tA, big_size=300)
            else:
                head2(cr, t, "BHISHMA TOOK HER", tF - 0.1, "BY FORCE", tF + 0.05, big_size=280)
            tag(cr, t, tA + 0.15, "AMBA", min(a_top[0], 880), a_top[1] - 110, 40)
            if bp:
                btop = bp["top"]
                tag(cr, t, tB + 0.35, "BHISHMA", min(max(btop[0] - 20, 200), 880), btop[1] - 150, 38)
        return dict(ui=ui, flash=flash_at(t, tA, 0.15) + flash_at(t, tF, 0.25))
    # his chariot carries her away
    sunset(cr, t, 0.25, 1300)
    glow(cr, 540, 1250, 700, 0.4)
    ground(cr)
    u = t - t_cut
    s = 0.48
    t_go = t_cut + 1.2
    w = max(0.0, t - t_go)
    x = -640 + 1020 * (1 - math.exp(-6.0 * u)) + 420 * w * w
    v = 1020 * 6.0 * math.exp(-6.0 * u) + 840 * w
    dust(cr, t, x - 120 * s, G - 30, clamp(v / 500))
    riders = [(-170, lambda c_, x_, d: amba(c_, t, x_, s, mood="shock", feet=d, flip=True, rods=False, ph=0.1,
                                           front=(-1.2, -0.5), head=-0.06)),
              (200, lambda c_, x_, d: bhishma(c_, t, x_, s, feet=d, rods=False, bow="hold", front=(-1.3, -0.4),
                                              ph=0.9))]
    out = chariot(cr, t, x, G, s, riders, roll=(x + 640) / (J.WHEEL_R * s), gallop=clamp(v / 300))
    a_top = out[0]["top"]

    def ui(cr):
        head2(cr, t, "FOR HIS BROTHER'S", t_cut + 0.05, "WEDDING", tW, big_size=290, under=tW + 0.5)
        tag(cr, t, t_cut + 0.5, "AMBA", min(max(a_top[0], 200), 880), a_top[1] - 110, 34)
    return dict(ui=ui, flash=flash_at(t, t_cut, 0.35), eve=0.12)


# ------------------------------------------------------------------ b5  the king she loved says no


SV4 = (830, 0.8)
AM4 = (230, 0.74)


def s_salva(cr, t, tl, t0, t1):
    c = cues(tl, "b5")
    tS, tL, tF, tR = c["S"], c["L"], c["F"], c["R"]
    glow(cr, 540, 1300, 660, 0.4)
    prop(cr, "arch", 930, G + 10, 0.5, alpha=0.4, blur=6.0)
    ground(cr)
    turned = t > tR - 0.05
    hop = 26 * math.sin(math.pi * clamp((t - tR + 0.05) / 0.25)) if turned else 0.0
    sp = salva(cr, t, SV4[0], SV4[1], mood="proud" if turned else "calm", flip=not turned,
               front=ANJALI["front"] if turned else (-0.4, -0.6), backa=ANJALI["backa"] if turned else (0.3, -0.25),
               head=-0.1 if turned else 0.0, y=G - 434 * SV4[1] - hop, hits=[(tS, 0.3), (tR, 0.5)], ph=0.8)
    x = AM4[0] if t < tF else hop_walk(t, tF, tF + 1.4, AM4[0], 520, 0.45)[0]
    offer = keyed(t, [(t0, 0.0), (tL - 0.2, 1.0), (tR + 0.15, 0.0)], 0.3, 1.3)
    mood = "smile" if t < tR else ("shock" if t < tR + 0.7 else "sad")
    fr = mix((-0.08, -0.35), (-1.25, -0.45), offer)
    if tF < t < tF + 1.4:
        ap = glide(cr, t, amba, tF, tF + 1.4, AM4[0], 520, AM4[1], mood=mood, front=fr, ph=0.2)
    else:
        ap = amba(cr, t, x, AM4[1], mood=mood, front=fr, hits=[(tR, 0.4)], head=0.12 * prog(t, tR + 0.5, 0.4),
                  ph=0.2)
    hand = to_user(cr, ap["handF"])
    t_drop = tR + 0.15
    if t < t_drop:
        prop(cr, "kk_garland", hand[0] + 30, hand[1] - 40, 0.85, rot=0.08 * math.sin(t * 2.2), alpha=prog(t, t0, 0.3))
        if t > tL - 0.3:
            warm(cr, (hand[0] + SV4[0]) / 2, hand[1] - 120, 380, 0.45 * prog(t, tL - 0.3, 0.5), (1.0, 0.6, 0.5))
    else:
        u = clamp((t - t_drop) / 0.55)
        prop(cr, "kk_garland", hand[0] + 30 + 40 * u, hand[1] - 40 + (G - hand[1] + 10) * u * u, 0.85, rot=1.3 * u)
    stop = sp["top"]
    a_top = ap["top"]

    def ui(cr):
        if t < tF:
            head2(cr, t, "BUT AMBA LOVED", t0 + 0.05, "ANOTHER KING", tL, big_size=250)
        elif t < tR:
            head2(cr, t, "SHE WENT", tF - 0.1, "TO HIM", tF + 0.1, big_size=300)
        else:
            head2(cr, t, "BUT THE KING SAID:", tR - 0.1, None, 0.0)
            cloud_text(cr, t, 560, 800, 0.82, [("I WON'T MARRY", 70, INK, -40, tR + 0.15),
                                               ("YOU NOW!", 104, RED, 52, tR + 0.45)], flip=True, t_in=tR)
        tag(cr, t, tS + 0.1, "THE KING SHE LOVED", min(max(stop[0] - 40, 260), 830), stop[1] - 150, 30,
            t_out=tR - 0.1)
        tag(cr, t, t0 + 0.2, "AMBA", min(max(a_top[0], 160), 880), a_top[1] - 110, 34, t_out=tF)
    return dict(ui=ui, flash=flash_at(t, tL, 0.15) + flash_at(t, tR, 0.3))


# ------------------------------------------------------------------ b6  alone; it was all because of Bhishma


AM5 = (380, 0.84)
BH5 = (910, 0.42, G - 70)
FIST = dict(front=(-2.85, -0.15), backa=(0.3, -0.5))             # her fist raised: the promise


def far_bhishma(cr, t, a):
    """Bhishma small and far away at the right (blurred), with a glow behind him."""
    if a <= 0.01:
        return
    glow(cr, BH5[0], BH5[2] - 260, 260, 0.35 * a)
    bhishma(cr, t, BH5[0], BH5[1], feet=BH5[2], flip=True, bow="hold", alpha=a, blur=3.0, rods=False, ph=1.0)


def s_alone(cr, t, tl, t0, t1):
    c = cues(tl, "b6")
    tA, tB = c["A"], c["B"]
    glow(cr, AM5[0], 1300, 560, 0.4)
    ground(cr)
    prop(cr, "kk_garland", AM5[0] + 210, G - 6, 0.75, rot=1.45, alpha=0.75)
    look = keyed(t, [(t0, 0.0), (tB - 0.1, 1.0)], 0.3, 1.2)
    sink = ease(clamp((t - t0) / 0.9)) * 190 * (1 - 0.6 * look)
    x, s = AM5
    clip_above(cr, G + 4)
    ap = amba(cr, t, x, s, mood="sad" if t < tB else "angry", y=G - 470 * s + sink,
              head=0.28 * (1 - look) - 0.05 * look, front=mix((-1.4, -1.9), (-0.3, -0.5), look),
              backa=mix((-1.1, -1.6), (0.2, -0.4), look), ph=0.2, hits=[(tB, 0.4)])
    cr.restore()
    eye = eye_of(cr, ap, k=0.13)
    if t < tB:
        tears(cr, t, t0 + 0.4, eye, n=8, period=0.55, alpha=0.85)
    far_bhishma(cr, t, prog(t, tB - 0.3, 0.4))
    dev_eye = cr.user_to_device(*eye)
    tgt = cr.user_to_device(BH5[0] - 20, BH5[2] - 260)
    ring = cr.user_to_device(BH5[0] - 10, BH5[2] - 240)

    def ui(cr):
        if t < tB:
            head2(cr, t, "AMBA WAS LEFT", t0 + 0.05, "ALL ALONE", tA, big_size=280)
        else:
            head2(cr, t, "ALL BECAUSE OF", tB - 0.1, "BHISHMA", tB + 0.05, big_size=280, under=tB + 0.5)
            line = [(dev_eye[0] + (tgt[0] - dev_eye[0]) * u, dev_eye[1] + (tgt[1] - dev_eye[1]) * u
                     - 50 * math.sin(math.pi * u)) for u in (i / 30 for i in range(31))]
            dotted(cr, line, prog(t, tB, 0.4), 28, 6.5, RED, 0.9)
            red_ring(cr, ring[0], ring[1], 110, 250, prog(t, tB + 0.35, 0.4), 8)
    return dict(ui=ui, eve=0.25 * prog(t, t0, 0.8), flash=flash_at(t, tB, 0.25))


# ------------------------------------------------------------------ b7  her promise: I will beat Bhishma


def s_vow(cr, t, tl, t0, t1):
    c = cues(tl, "b7")
    tV, tK = c["V"], c["K"]
    glow(cr, AM5[0], 1300, 560, 0.45)
    ground(cr)
    x, s = AM5
    up = keyed(t, [(t0, 0.0), (tV - 0.1, 1.0)], 0.3, 1.4)
    ap = amba(cr, t, x, s, mood="angry", front=mix((-0.3, -0.5), FIST["front"], up), backa=FIST["backa"],
              hits=[(tV, 0.5), (tK, 0.4)], ph=0.2)
    far_bhishma(cr, t, 1.0)
    ring = cr.user_to_device(BH5[0] - 10, BH5[2] - 240)
    btag = cr.user_to_device(BH5[0] - 20, BH5[2] - 560)
    a_top = ap["top"]

    def ui(cr):
        head2(cr, t, "AMBA PROMISED:", t0 + 0.05, None, 0.0)
        card2(cr, t, tV - 0.1, 540, 690, 0.8, [("I WILL BEAT", 96, INK, -46, tV + 0.1),
                                              ("BHISHMA!", 130, RED, 56, tK)])
        red_ring(cr, ring[0], ring[1], 110, 250, prog(t, tK + 0.2, 0.4), 8)
        tag(cr, t, tK + 0.1, "BHISHMA", btag[0], btag[1], 30)
        tag(cr, t, t0 + 0.2, "AMBA", min(max(a_top[0], 160), 880), a_top[1] - 110, 34, t_out=tV - 0.2)
    return dict(ui=ui, flash=flash_at(t, tV, 0.3) + flash_at(t, tK, 0.2))


# ------------------------------------------------------------------ b8  years of prayer; Shiva comes


TP6 = (540, 0.9)
UP = dict(front=(-2.95, -0.15), backa=(-2.85, -0.25))            # both arms raised over her head, palms joined


def seasons(cr, t, t0, t1, a=1.0):
    """Years going by: the sun and moon circling, a spell of rain, a spell of snow."""
    if a <= 0.01:
        return
    w = (t - t0) * 2.6
    cx, cy, rx, ry = 540, 860, 430, 190
    prop(cr, "sun", cx + rx * math.cos(w), cy - ry * math.sin(w), 0.42, rot=t, alpha=0.85 * a)
    prop(cr, "moon", cx - rx * math.cos(w), cy + ry * math.sin(w), 0.7, alpha=0.85 * a)
    ph = clamp((t - t0) / max(0.8, t1 - t0))
    rain = clamp(1 - abs(ph - 0.3) / 0.22) * a
    if rain > 0.01:
        for x in (260, 800):
            prop(cr, "cloud", x, 700, 0.55, alpha=0.8 * rain)
        cr.save()
        cr.set_source_rgba(0.30, 0.38, 0.62, 0.55 * rain)
        cr.set_line_width(3)
        for i in range(40):
            x = 120 + (i * 97) % 860
            y = 760 + ((t * 900 + i * 131) % 900)
            cr.move_to(x, y)
            cr.line_to(x - 10, y + 36)
        cr.stroke()
        cr.restore()
    snow = clamp(1 - abs(ph - 0.75) / 0.22) * a
    if snow > 0.01:
        for i in range(26):
            x = 80 + (i * 173) % 920 + 20 * math.sin(t * 1.5 + i)
            y = 640 + ((t * 160 + i * 97) % 1100)
            sparkle(cr, x, y, 12 + 4 * (i % 3), snow, (0.92, 0.96, 1.0))


def shield(cr, t, x, y, r, a):
    """Bhishma's invincibility: a golden ring of light round him, turning."""
    if a <= 0.01:
        return
    aura(cr, t, x, y, r * 0.55, r, 0.55 * a, n=24, spin=0.1)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for lw, k in ((26, 0.12), (10, 0.3), (3, 0.8)):
        cr.set_source_rgba(1.0, 0.82, 0.40, k * a * (0.85 + 0.15 * math.sin(t * 4)))
        cr.set_line_width(lw)
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.stroke()
    cr.restore()


def s_tapas(cr, t, tl, t0, t1):
    c = cues(tl, "b8")
    tY, tP, tS, tN, tK = c["Y"], c["P"], c["S"], c["N"], c["K"]
    t_s = tS - 0.15
    glow(cr, 540, 1300, 660, 0.4)
    ground(cr)
    if t < t_s:                                                       # years of prayer to Shiva
        seasons(cr, t, t0, t_s, prog(t, t0, 0.3))
        x, s = TP6
        lit = prog(t, tP - 0.1, 0.8)
        aura(cr, t, x + 20, G - 1000 * s, 160 * s, 600 * s, 0.7 * lit, n=20, spin=0.08)
        tapas(cr, t, x, s, mood="shut", ph=0.2, head=-0.06, **UP)
        n = 1 + int(max(0.0, t - tY) * 6.0)

        def ui(cr):
            head2(cr, t, "FOR YEARS, SHE", t0 + 0.05, "PRAYED TO SHIVA", tP, big_size=250)
            plate(cr, t, tY, f"YEAR {n}", 540, 650, 40)
        return dict(ui=ui, flash=flash_at(t, tP, 0.15))
    b, k, a = depth(t, t_s, 0.5)
    sx, ss = 790, 0.74
    glow(cr, sx, G - 560 * ss, 560, 0.7 * a)
    aura(cr, t, sx, G - 760 * ss, 200 * ss, 760 * ss, 0.8 * a, n=22, spin=0.06)
    burst(cr, t, sx, G - 600 * ss, t_s, n=22, rmax=760)
    shiva(cr, t, sx, ss * k, mood="speak" if (tN - 0.3 < t < t1 - 0.3 and math.sin(t * 13) > 0) else "calm",
          flip=True, alpha=a, blur=b, hits=[(tN, 0.3)], ph=0.6)
    bow_ = keyed(t, [(t0, 0.0), (t_s + 0.5, 1.0)], 0.3, 1.2)
    tapas(cr, t, 290, 0.72, mood="open", front=mix(UP["front"], ANJALI["front"], bow_),
          backa=mix(UP["backa"], ANJALI["backa"], bow_), head=0.08 * bow_, hits=[(t_s + 0.4, 0.3)], ph=0.2)

    def ui(cr):
        if t < tN - 0.45:
            head2(cr, t, "THEN SHIVA", t_s + 0.05, "CAME", tS + 0.1, big_size=300)
        else:
            head2(cr, t, "SHIVA SAID:", tN - 0.5, None, 0.0)
        tag(cr, t, tS + 0.4, "SHIVA", sx - 10, 880, 38, t_out=tN - 0.6)
        card2(cr, t, tN - 0.45, 540, 690, 0.78, [("IN YOUR NEXT LIFE,", 76, INK, -46, tN),
                                                ("YOU WILL BEAT BHISHMA", 74, RED, 52, tK)])
    return dict(ui=ui, flash=flash_at(t, t_s, 0.5) + flash_at(t, tK, 0.2))


# ------------------------------------------------------------------ b9  into the fire


FIRE7 = (790, G)


def big_fire(cr, t, x, ground_, s=1.0, a=1.0, flare=0.0):
    """The great sacred fire: an altar, three tongues of flame, a big glow, sparks rising."""
    glow(cr, x, ground_ - 320 * s, (520 + 300 * flare) * s, (0.7 + 0.1 * math.sin(t * 7)) * a)
    warm(cr, x, ground_ - 300 * s, (420 + 400 * flare) * s, (0.7 + 0.3 * flare) * a, (1.0, 0.62, 0.20))
    prop(cr, "altar", x, ground_ + 14 * s, 1.1 * s, alpha=a)
    for dx, sc, ph in ((-70, 0.75, 1), (70, 0.8, 2), (0, 1.05, 0)):
        prop(cr, f"flame{(int(t * 10) + ph) % 3}", x + dx * s, ground_ - 60 * s, sc * s * (1 + 0.4 * flare), alpha=a)
    lights(cr, t, x, ground_ - 460 * s, 200 * s, 12, 0.8 * a, (1.0, 0.7, 0.3), 0.9)


def s_fire(cr, t, tl, t0, t1):
    c = cues(tl, "b9")
    tF, tD = c["F"], c["J"]
    fx, fg = FIRE7
    fl = prog(t, tF - 0.2, 0.5)
    big_fire(cr, t, fx, fg, 1.0, flare=fl)
    ground(cr)
    gone = prog(t, tF, 0.45)
    if gone < 1:
        x1 = fx - 300
        if t < tF:
            glide(cr, t, tapas, t0 - 0.2, tF, 230, x1, 0.82, mood="shut", **ANJALI, ph=0.2, alpha=1.0)
        else:
            tapas(cr, t, x1 + 50 * gone, 0.82, mood="shut", alpha=1 - gone, **ANJALI, ph=0.2)
    if t > tD - 0.2:
        u = clamp((t - tD + 0.2) / 1.6)
        orb(cr, t, fx - 80 * u, fg - 520 - 520 * ease(u), 34, prog(t, tD - 0.2, 0.3), WARM_C)
    w = 0.85 * math.exp(-1.6 * max(0.0, t - tF)) * (t > tF)

    def ui(cr):
        if t < tD:
            head2(cr, t, "AMBA WENT INTO THE", t0 + 0.05, "FIRE", tF, big_size=320)
        else:
            head2(cr, t, "AND LEFT", tD - 0.1, "THIS LIFE", tD + 0.05, big_size=290, big_color=INK)
    return dict(ui=ui, eve=0.25, wash=w)


# ------------------------------------------------------------------ b10  born again: a king's daughter, Shikhandi


DR8 = (200, 0.74)
QN8 = (880, 0.7)
CR8 = (540, 0.66)


def palace(cr, t, a=0.62, blur=4.0):
    prop(cr, "arch", 540, G + 10, 0.84, rot=sway(t, 0.002, 0.3), alpha=a, blur=blur)


def s_reborn(cr, t, tl, t0, t1):
    c = cues(tl, "b10")
    tJ, tK, tB, tN = c["J"], c["K"], c["B"], c["N"]
    glow(cr, 540, 1300, 680, 0.42)
    palace(cr, t)
    ground(cr)
    happy = t > tB + 0.2
    dp = drupada(cr, t, DR8[0], DR8[1], mood="smile" if happy else "calm", front=(-0.6, -0.9), hits=[(tK, 0.3)],
                 ph=0.5)
    queen(cr, t, QN8[0], QN8[1], mood="smile" if happy else "open", flip=True, front=(-0.6, -1.0), ph=1.0)
    lit = prog(t, tB - 0.1, 0.5)
    hc = cradle(cr, t, CR8[0], G, CR8[1], baby=t > tB - 0.05, glow_a=0.3 + 0.6 * lit,
                arms=(0.3 * math.sin(t * 2.4), 0.25 * math.sin(t * 2 + 1)))
    if t < tB:
        u = clamp((t - t0 + 0.2) / max(0.6, tB - t0))
        orb(cr, t, hc[0] + 60 * math.sin(u * 4) * (1 - u), 260 + (hc[1] - 260) * ease(u), 34, 1.0, WARM_C)
    else:
        burst(cr, t, hc[0], hc[1], tB, n=18, rmax=520)
        lights(cr, t, hc[0], hc[1] - 60, 220, 10, 0.7 * lit)
    dtop = dp["top"]
    dev_c = cr.user_to_device(hc[0], hc[1] - 250)
    lng = lang(tl)

    def ui(cr):
        if t < tB:
            head2(cr, t, "SHE WAS BORN AGAIN", t0 + 0.05, "IN A KING'S HOME", tK, big_size=220)
        elif t < tN:
            head2(cr, t, "AS A", tB - 0.1, "DAUGHTER", tB + 0.05, big_size=280)
        else:
            head2(cr, t, "HER NAME:", tN - 0.15, "SHIKHANDI", tN, big_size=270, under=tN + 0.5)
            script_strip(cr, t, tN + 0.2, NAME_M[lng], 540, 650, 56)
        tag(cr, t, tK + 0.1, "A KING", min(max(dtop[0] + 30, 200), 860), dtop[1] - 150, 32, t_out=tN - 0.3)
        tag(cr, t, tN + 0.3, "SHIKHANDI", dev_c[0], dev_c[1], 34)
    return dict(ui=ui, flash=flash_at(t, tB, 0.3) + flash_at(t, tN, 0.15))


# ------------------------------------------------------------------ b11  a magic yaksha gives her his boy's body


SK10 = (300, 0.78)
YK10 = (790, 0.86)


def s_swap(cr, t, tl, t0, t1):
    c = cues(tl, "b11")
    tY, tS, tN, tM = c["Y"], c["S"], c["N"], c["M"]
    t_x = tS + 0.4                                                  # the lights pass each other: the bodies change
    forest(cr, t, 0.9)
    ground(cr)
    fireflies(cr, t, 1.0)
    sx, ss = SK10
    yx, ys = YK10
    if t < t_x:
        if t < t0 + 1.2:
            sp = glide(cr, t, girl, t0 - 0.3, t0 + 1.2, -120, sx, ss, mood="sad", ph=0.4, **HEART)
        else:
            sp = girl(cr, t, sx, ss, mood="shock" if tY < t < tY + 1.0 else "open", ph=0.4, hits=[(tY, 0.4)],
                      front=mix(HEART["front"], (-0.6, -0.9), prog(t, tY + 0.6, 0.4)))
    else:
        war = t > tM - 0.1
        glow(cr, sx, G - 520 * ss, 420, 0.5 * (1 - prog(t, t_x + 1.5, 1.0)) + 0.2)
        sp = shk(cr, t, sx, ss, mood="war" if war else "man", war=war, bow=war, ph=0.4,
                 front=(-0.25, -2.35) if war else (-0.6, -0.9), backa=(0.75, -1.6) if war else (0.3, -0.25),
                 hits=[(t_x, 0.6), (tM, 0.4)])
        burst(cr, t, sx, G - 560 * ss, t_x, n=18, rmax=520)
    yp = None
    t_in = tY - 0.35
    if t > t_in:
        b, k, ya = depth(t, t_in, 0.6)
        ya *= 1 - 0.35 * prog(t, t_x + 0.4, 0.6)
        glow(cr, yx, G - 560 * ys, 620, 0.7 * ya)
        warm(cr, yx, G - 560 * ys, 520, 0.55 * ya, (0.55, 1.0, 0.5))
        aura(cr, t, yx, G - 800 * ys, 200 * ys, 760 * ys, 0.6 * ya, n=20, spin=0.07, col=(0.6, 1.0, 0.45))
        lights(cr, t, yx, G - 700 * ys, 360, 12, 0.8 * ya, (0.7, 1.0, 0.5), 0.3)
        yp = yaksha(cr, t, yx, ys * k, mood="calm", flip=True, front=(-1.4, -0.6), alpha=ya, blur=b,
                    hits=[(t_x, 0.4)], ph=0.8)
    pa, pb = sp["chest"], (yp["chest"] if yp else None)
    stop = sp["top"]

    def ui(cr):
        if pb is not None and t > tS - 0.7:                       # drawn over the night, so the lights stay bright
            cross_lights(cr, t, tS - 0.1, (pa[0], pa[1] - 20), (pb[0], pb[1] - 20), dur=1.0, lift=300, r=40)
        if t < tY:
            head2(cr, t, "WHEN SHIKHANDI", t0 + 0.05, "GREW UP", t0 + 0.35, big_size=290)
        elif t < tS:
            head2(cr, t, "SHE MET A", tY - 0.1, "MAGIC YAKSHA", tY + 0.05, big_size=270)
            card_back(cr, t, tY + 0.3, 540, 660, 0.76)                # the hard word, explained
            card2(cr, t, tY + 0.3, 540, 660, 0.76, [("YAKSHA =", 88, INK, -48, tY + 0.35),
                                                    ("A MAGIC FOREST SPIRIT", 66, RED, 50, tY + 0.6)])
        elif t < tM:
            head2(cr, t, "HE GAVE HER", tS - 0.1, "HIS BOY'S BODY", tS + 0.1, big_size=250)
        else:
            head2(cr, t, "NOW SHIKHANDI WAS A", tM - 0.1, "BOY WARRIOR", tM + 0.05, big_size=270)
        tag(cr, t, t0 + 0.5, "SHIKHANDI", min(max(stop[0], 200), 880), stop[1] - 140, 34, t_out=tY + 0.2)
        tag(cr, t, tN, "SHIKHANDI", min(max(stop[0], 200), 880), stop[1] - 140, 34)
    return dict(ui=ui, night=NIGHT, lift=1.0, flash=flash_at(t, tY, 0.3) + flash_at(t, t_x, 0.5))


# ------------------------------------------------------------------ b12  the big war; ten days, nobody beats Bhishma


def s_ten(cr, t, tl, t0, t1):
    c = cues(tl, "b12")
    tY, tD, tB = c["Y"], c["D"], c["N"]
    t_cut = tD - 0.25
    if t < t_cut:
        sunset(cr, t, 0.8, 1240)
        ground(cr)
        r = prog(t, tY - 0.3, 0.5)
        adv = 45 * ease(clamp((t - tY - 0.2) / 1.6))
        mv = 1.0 if tY + 0.2 < t < tY + 1.8 else 0.0
        army(cr, t, (60, 150, 240, 330, 420), G, 0.5, raise_=r, alpha=0.9, blur=1.0, march=mv, dx=adv - 80)
        army(cr, t, (660, 750, 840, 930, 1020), G, 0.5, raise_=r, flip=True, alpha=0.9, blur=1.0, march=mv,
             dx=80 - adv)
        army(cr, t, (110, 210, 310, 410), G - 70, 0.36, raise_=r, alpha=0.55, blur=5.0)
        army(cr, t, (670, 770, 870, 970), G - 70, 0.36, raise_=r, flip=True, alpha=0.55, blur=5.0)

        def ui(cr):
            head2(cr, t, "THEN CAME A", t0 + 0.05, "GREAT BIG WAR", tY, big_size=250)
        return dict(ui=ui, eve=0.15, flash=flash_at(t, tY, 0.25))
    glow(cr, 540, 1300, 680, 0.4)
    day = clamp((t1 - t_cut - 0.5) / 10, 0.16, 0.42)                     # ten days fit before the cut
    days = (t - t_cut) / day
    sun_arc_x = 540 + 380 * math.cos(math.pi * (1 - (days % 1.0)))
    prop(cr, "sun", sun_arc_x, 980 - 160 * math.sin(math.pi * (days % 1.0)), 0.36, rot=t, alpha=0.7)
    ground(cr)
    army(cr, t, (60, 150, 240), G, 0.46, raise_=0.6, alpha=0.75, blur=2.0)
    bx, bs = 700, 0.78
    cy = G - 520 * bs
    shield(cr, t, bx, cy, 400 * bs, 1.0)
    bhishma(cr, t, bx, bs, mood="stern", flip=True, bow="raise", front=(-1.6, -0.25), ph=1.0, hits=[(tB, 0.3)])
    for i in range(9):                                              # enemy arrows spark out on his ring
        ts = t_cut + 0.15 + 0.8 * day * i
        u = (t - ts) / 0.4
        p0 = (300, G - 300 - 60 * math.sin(i * 1.7))
        ang = math.pi * (0.92 + 0.1 * math.sin(i * 2.3))
        p1 = (bx + 400 * bs * math.cos(ang), cy + 400 * bs * math.sin(ang))
        if 0 <= u < 1:
            fly_arrow(cr, p0, p1, u, 40)
        elif 1 <= u < 1.6:
            sparkle(cr, p1[0], p1[1], 46 * (1.6 - u), 1.0)
    n = min(10, 1 + int(max(0.0, t - t_cut) / day))

    def ui(cr):
        head2(cr, t, "FOR 10 DAYS, NO ONE", t_cut + 0.05, "COULD BEAT HIM", tB, big_size=250)
        plate(cr, t, t_cut + 0.1, f"DAY {n}", 540, 650, 44)
    return dict(ui=ui, flash=flash_at(t, t_cut, 0.3) + flash_at(t, tB, 0.15))


# ------------------------------------------------------------------ b12q  so how was Bhishma beaten?


def s_ask(cr, t, tl, t0, t1):
    c = cues(tl, "b12q")
    tQ = c["Q"]
    glow(cr, 540, 1400, 600, 0.45)
    ground(cr)
    bx, bs = 640, 0.5
    shield(cr, t, bx, G - 520 * bs, 400 * bs, 0.8)
    bp = bhishma(cr, t, bx, bs, mood="calm", flip=True, bow="hold", ph=1.0, front=(-0.4, -0.6))
    btop = bp["top"]

    def ui(cr):
        head2(cr, t, "SO HOW WAS", t0 + 0.05, "BHISHMA BEATEN?", t0 + 0.35, big_size=240)
        big_q(cr, t, min(tQ, t0 + 0.5), 540, 800, 380)
        tag(cr, t, t0 + 0.3, "BHISHMA", min(btop[0], 870), btop[1] - 110, 30)
    return dict(ui=ui, flash=flash_at(t, min(tQ, t0 + 0.5), 0.25))


# ------------------------------------------------------------------ b13  Bhishma's rule


def s_rule(cr, t, tl, t0, t1):
    c = cues(tl, "b13")
    tR, tW, tH = c["R"], c["G"], c["F"]
    glow(cr, 540, 1300, 660, 0.4)
    ground(cr)
    ga = prog(t, tW - 0.3, 1.1)                                     # the twist, revealed slowly
    sx, ss = 270, 0.7
    if ga > 0:
        glow(cr, sx - 40, G - 640, 420, 0.45 * ga)
        ghost(cr, lambda c_: girl(c_, t, sx - 60, 0.84, mood="open", rods=False, blur=5.0, ph=0.3, **HEART),
              ga * (0.85 + 0.1 * math.sin(t * 3)))
    sp = shk(cr, t, sx, ss, mood="war", war=True, bow=True, ph=0.4, front=(-0.4, -0.6))
    talk = tR - 0.2 < t < t1 - 0.3 and math.sin(t * 12) > 0
    stop = keyed(t, [(t0, 0.0), (tW - 0.1, 1.0)], 0.3, 1.3)
    bx, bs = 800, 0.76
    bp = bhishma(cr, t, bx, bs, mood="speak" if talk else "calm", flip=True, bow="hold",
                 front=mix((-0.4, -0.6), (-1.75, -0.85), stop), hits=[(tW, 0.3)], ph=1.0)
    btop = bp["top"]
    s_top = sp["top"]

    def ui(cr):
        if t < tW - 0.45:
            head2(cr, t, "BHISHMA HAD", t0 + 0.05, "ONE RULE", tR, big_size=300)
        else:
            head2(cr, t, "BHISHMA'S RULE:", tW - 0.5, None, 0.0)
        tag(cr, t, t0 + 0.3, "BHISHMA", min(btop[0], 870), btop[1] - 120, 34, t_out=tW - 0.5)
        tag(cr, t, tW + 0.3, "SHIKHANDI", min(max(s_top[0], 200), 880), s_top[1] - 150, 32)
        plate(cr, t, tW + 0.7, "ONCE A GIRL!", min(max(s_top[0] - 30, 190), 880), s_top[1] - 230, 32)
        card2(cr, t, tW - 0.45, 540, 650, 0.8, [("IF YOU WERE EVER A GIRL,", 64, INK, -46, tW),
                                               ("I WON'T FIGHT YOU!", 92, RED, 54, tH)])
    return dict(ui=ui, flash=flash_at(t, tR, 0.2) + flash_at(t, tW, 0.25) + flash_at(t, tW + 0.7, 0.2))


# ------------------------------------------------------------------ b14  Arjuna puts Shikhandi in front


def s_front(cr, t, tl, t0, t1):
    c = cues(tl, "b14")
    tA, tS, tR, tF = c["A"], c["S"], c["R"], c["F"]
    sunset(cr, t, 0.4, 1300)
    glow(cr, 540, 1300, 680, 0.4)
    ground(cr)
    s = 0.48
    u = t - t0 + 0.2
    x = -500 + 830 * (1 - math.exp(-3.0 * max(0.0, u)))
    v = 830 * 3.0 * math.exp(-3.0 * max(0.0, u))
    dust(cr, t, x - 120 * s, G - 30, clamp(v / 500))
    step = keyed(t, [(t0, 0.0), (tF - 0.1, 1.0)], 0.35, 1.2)
    hop = 40 * math.sin(math.pi * clamp((t - tF + 0.1) / 0.35)) * (t > tF - 0.1)
    riders = [(-262, lambda c_, x_, d: arjuna(c_, t, x_, s, bow="carry", feet=d, rods=False, ph=0.9,
                                              front=(-0.9, -0.4))),
              (-40 + 268 * step, lambda c_, x_, d: shk(c_, t, x_, s, mood="war", war=True, bow=True, feet=d,
                                                       y=d - 434 * s - hop, rods=False, ph=0.4, front=(-1.2, -0.3)))]
    out = chariot(cr, t, x, G, s, riders, roll=(x + 500) / (J.WHEEL_R * s), gallop=clamp(v / 300), ph=0.3)
    atop, stop = out[0]["top"], out[1]["top"]

    def ui(cr):
        head2(cr, t, "SO ARJUNA PUT SHIKHANDI", t0 + 0.05, "IN FRONT", tF, big_size=290, under=tF + 0.4)
        tag(cr, t, tA + 0.1, "ARJUNA", max(atop[0] - 20, 150), atop[1] - 170, 32)
        tag(cr, t, tS + 0.1, "SHIKHANDI", min(max(stop[0] + 30, 200), 880), stop[1] - 110, 32)
        if t > tF + 0.2:
            red_ring(cr, stop[0] + 10, stop[1] + 150, 110, 210, prog(t, tF + 0.2, 0.4), 8)
    return dict(ui=ui, eve=0.1, flash=flash_at(t, tF, 0.25))


# ------------------------------------------------------------------ b15  weapons down; the fall; Amba's revenge


CH16 = (225, 0.4)                    # the chariot: x, scale
BH16 = (965, 0.56)
SHOT_GAP = 0.2                       # one arrow every SHOT_GAP s


def s_fall(cr, t, tl, t0, t1):
    c = cues(tl, "b15")
    tD, tA, tG, tR = c["D"], c["A"], c["G"], c["R"]
    tP = tR - 0.35                                                  # Amba's glowing silhouette rises
    tS = tA + 0.1                                                   # Arjuna's arrows fly from his name on
    t_cut = max(tG - 0.15, tS + 0.9)
    if t < t_cut:
        sunset(cr, t, 0.55, 1300)
        glow(cr, 540, 1300, 680, 0.35)
        ground(cr)
        bx, bs = BH16
        low = keyed(t, [(t0, 0.0), (tD + 0.1, 1.0)], 0.3, 1.2)
        bp = bhishma(cr, t, bx, bs, mood="rest" if t > tD + 0.3 else "calm", flip=True,
                     bow="low" if low > 0.5 else "raise", front=mix((-1.6, -0.3), (-0.15, -0.2), low),
                     head=0.12 * low, hits=[(tD, 0.4)], ph=1.0)
        chest = to_user(cr, bp["chest"])
        cx, cs = CH16
        n_shot = int((t - tS) / SHOT_GAP) if t > tS else -1
        draw_ = 0.0
        if t > tS - 0.3:
            ph_ = ((t - tS) / SHOT_GAP) % 1.0 if t > tS else clamp((t - tS + 0.3) / 0.3)
            draw_ = 1 - ph_ if t > tS else ph_
        store = {}

        def ar(c_, x_, d):
            store["a"] = arjuna(c_, t, x_, cs, bow="aim", aim=-0.12, draw=draw_, feet=d, rods=False, ph=0.9)
            return store["a"]

        def sk_(c_, x_, d):
            return shk(c_, t, x_, cs, mood="war", war=True, feet=d, rods=False, front=(-1.2, -0.3), ph=0.4,
                       bow=True)
        out = chariot(cr, t, cx, G, cs, [(-262, ar), (228, sk_)], ph=0.3)
        if n_shot >= 0 and "a" in store and "grip" in store["a"]:
            g = store["a"]["grip"]
            for i in range(max(0, n_shot - 3), n_shot + 1):
                p1 = (chest[0] + 20 * math.sin(i * 2.1), chest[1] + 30 * math.cos(i * 1.7))
                u = (t - tS - i * SHOT_GAP) / 0.32
                if u >= 1:
                    sparkle(cr, p1[0], p1[1], 30 * (1 - clamp((u - 1) * 0.32 / 0.3)), 0.9)
                    continue
                fly_arrow(cr, (g[0] + 40, g[1] - 10), p1, u, 90)
        stop = out[1]["top"]
        atop = out[0]["top"]

        def ui(cr):
            if t < tA:
                head2(cr, t, "BHISHMA PUT DOWN", t0 + 0.05, "HIS WEAPONS", tD, big_size=260)
            else:
                head2(cr, t, "AND ARJUNA SHOT HIS", tA - 0.1, "ARROWS", tS, big_size=290)
            tag(cr, t, t0 + 0.3, "SHIKHANDI", min(max(stop[0] + 20, 200), 880), stop[1] - 110, 30)
            tag(cr, t, tA + 0.1, "ARJUNA", max(atop[0], 150), atop[1] - 190, 30)
            tag(cr, t, t0 + 0.2, "BHISHMA", bx - 20, 960, 32)
        return dict(ui=ui, eve=0.12, flash=flash_at(t, tD, 0.15) + flash_at(t, tS, 0.15))
    # the fall onto the bed of arrows, a silhouette against the setting sun; Amba's glowing silhouette rises
    glow(cr, 540, 1450, 900, 0.6)
    warm(cr, 540, 1480, 760, 0.7, (1.0, 0.42, 0.14))
    prop(cr, "sun", 560, 1500, 1.35, rot=t * 0.08, alpha=0.8)
    ga = prog(t, tP - 0.1, 0.6)
    if ga > 0:
        lift = 60 * (1 - ease(ga))
        glow(cr, 560, 1060, 520, 0.5 * ga)
        ghost(cr, lambda c_: amba(c_, t, 560, 0.9, mood="open", feet=G - 120 + lift, rods=False, blur=5.0, ph=0.3,
                                  **ANJALI), 0.9 * ga)
    ground(cr)
    p = clamp((t - t_cut) / 0.8)
    bhishma_lying(cr, t, 470, G, 0.72, p)
    puff(cr, t, t_cut + 0.75, 560, G - 20, 0.8)
    lights(cr, t, 540, 1350, 380, 12, 0.6 * prog(t, tR, 0.6), (1.0, 0.7, 0.35), 0.4)

    def ui(cr):
        if t < tP:
            head2(cr, t, "BHISHMA", t_cut + 0.1, "FELL", tG, big_size=320)
        else:
            head2(cr, t, "AT LAST:", tP - 0.1, "AMBA'S REVENGE", tR, big_size=240, under=tR + 0.5)
    return dict(ui=ui, eve=0.3, flash=flash_at(t, t_cut + 0.75, 0.3) + flash_at(t, tR, 0.3))


# ------------------------------------------------------------------ b15c  callback: the girl who cried beat Bhishma


def s_circle(cr, t, tl, t0, t1):
    c = cues(tl, "b15c")
    tR, tN, tH = c["R"], c["N"], c["H"]
    gp, _ = hook_scene(cr, t, 1.0, 0.4 + 0.6 * prog(t, tH - 0.1, 0.5))
    gtop = gp.get("top", (HK["gx"], 800))
    if "head" in gp and tR - 0.2 < t < tN + 0.6:                    # tears on the glowing girl: she cried
        g_eye = to_user(cr, gp["head"])
        tears(cr, t, tR - 0.1, (g_eye[0] + 10, g_eye[1] - 20), n=5, period=0.5, alpha=0.9)

    def ui(cr):
        head2(cr, t, "THE GIRL WHO CRIED...", t0 + 0.05, "BEAT BHISHMA", tH, big_size=280, under=tH + 0.45)
        plate(cr, t, tN, "NEXT LIFE", gtop[0] + 10, gtop[1] - 70, 32)
    return dict(ui=ui, eve=0.15, flash=flash_at(t, tH, 0.3))


# ------------------------------------------------------------------ b16  who beat Bhishma?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "b16")
    tQ, tA, tM, tC = c["Q"], c["A"], c["M"], c["C"]
    glow(cr, 540, 1450, 560, 0.45)
    warm(cr, 540, 1600, 420, 0.45, (1.0, 0.45, 0.15))
    prop(cr, "sun", 560, 1640, 0.62, rot=t * 0.08, alpha=0.6)
    ground(cr)
    bhishma_lying(cr, t, 470, G, 0.4, 1.0, 0.9)
    arjuna(cr, t, 250, 0.5, bow="raise", feet=G, ph=0.9)
    tapas(cr, t, 830, 0.5, mood="fierce", flip=True, ph=0.3, front=(-0.4, -0.8))
    cards = ((300, "ARJUNA?", tA - 0.1), (780, "AMBA?", tM - 0.1))

    def ui(cr):
        head2(cr, t, "WHO BEAT", t0 + 0.05, "BHISHMA?", min(tQ, t0 + 0.5), big_size=280)
        for cx, txt, tc in cards:
            card(cr, t, min(tc, t0 + 0.6) - 0.25, cx, 790, 0.58, [(txt, 132 if len(txt) < 6 else 112, RED, 4)])
        if t > tA:
            n = int((t - tA) / 0.9)
            k = n % 2
            red_ring(cr, cards[k][0], 794, 232, 96, prog(t, tA + 0.9 * n, 0.35), 9)
    return dict(ui=ui, eve=0.08, flash=flash_at(t, tQ, 0.15))


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("b1", None, s_hook, {"z": (1.0, 1.04)}),
    ("b2", None, s_book, {"z": (1.0, 1.03)}),
    ("b3", None, s_strong, {"z": (1.0, 1.03)}),
    ("b4", None, s_taken, {"z": (1.0, 1.03)}),
    ("b5", None, s_salva, {"z": (1.0, 1.03)}),
    ("b6", None, s_alone, {"z": (1.0, 1.04)}),
    ("b7", None, s_vow, {"z": (1.0, 1.04)}),
    ("b8", None, s_tapas, {"z": (1.0, 1.03)}),
    ("b9", None, s_fire, {"z": (1.0, 1.05), "focus": (700, 1300)}),
    ("b10", None, s_reborn, {"z": (1.0, 1.03)}),
    ("b11", None, s_swap, {"z": (1.0, 1.03)}),
    ("b12", None, s_ten, {"z": (1.0, 1.03)}),
    ("b12q", None, s_ask, {"z": (1.0, 1.04)}),
    ("b13", None, s_rule, {"z": (1.0, 1.03)}),
    ("b14", None, s_front, {"z": (1.0, 1.03)}),
    ("b15", None, s_fall, {"z": (1.0, 1.03)}),
    ("b15c", None, s_circle, {"z": (1.0, 1.04)}),
    ("b16", None, s_end, {"z": (1.0, 1.03)}),
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
    tint(cr, (1.0, 0.66, 0.42), out.get("eve", 0.0))
    cr.restore()
    motes(cr, t)
    pc.lamp(cr, t, night=out.get("night", 0.0), flash=out.get("flash", 0.0))
    title_lift(cr, out.get("lift", 0.0) * out.get("night", 0.0) / NIGHT)
    wash(cr, out.get("wash", 0.0))
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a conch
    as Shiva comes, shimmer as the yaksha gives his body, a bell on the closing question, then (only where they fit)
    shimmer as she is born again, a damaru as the war begins, a single hit as Bhishma falls. Chosen in THAT order of
    importance, each at least SFX_MIN_GAP from every sound already kept (as render_myth.calm_sfx keeps them), so the
    list returned is what plays (about 6 sounds); the bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["b8"]["S"], "conch", 0), (c["b11"]["S"], "shimmer", 0), (c["b16"]["C"], "bell", 0),
            (c["b10"]["B"], "shimmer", 0), (c["b12"]["Y"], "damaru", 0), (c["b15"]["G"], "hit", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["b8"]["S"] - 0.3, "dip", 0.45), (c["b11"]["S"] - 0.3, "dip", 0.45), (c["b13"]["G"] - 0.35, "dip", 0.5),
            (c["b15"]["G"] - 0.35, "dip", 0.5)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
