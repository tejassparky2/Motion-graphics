"""Scenes for videos/mandhata.py: "The king who got pregnant" (Yuvanashva and the birth of Mandhata), in Togalu
Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen, two-tier headlines and
rod-puppet motion as the Jarasandha, Kaikeyi and Lakshman Rekha reels, with the cast from mandhata_cast. ONE story, one
step per shot. The wonder is the point: the king, the sages, Indra and the Ashvins keep their dignity; the birth is a
burst of light from the king's side and the baby appears in the glow (no blood, no cut flesh). Every frame is a pure
function of t. English on-screen text only (shared by Hindi and Kannada); cues are words of the line in each language
({"hi": ..., "kn": ...}) with a fraction fallback, kept in one table (CUES) that the scenes and sfx() both read, with
minimum gaps so a fast voice can't bunch the beats together.

Shot list (line: what is on the screen)
  m1  HOOK: frame 0 = Yuvanashva alone and large, a hand on his round belly, the other at the small of his back, a soft
      light in the belly; A KING WHO GOT / PREGNANT (big word in by 0.4 s), underlined on "garbhvati"; the belly is
      ringed on "pet"; on "beta" a small glowing baby appears beside him: HIS SON
  m2  THIS IS NOT A / JOKE (crossed out on "nahin"); two palm-leaf books rise and open: BHAGAVATA PURANA 9.6.25-37 and
      MAHABHARATA VANA PARVA 126; IT'S WRITTEN IN / BOTH, both numbers ringed
  m3  the palace arch, the king (KING YUVANASHVA tag): THE KING HAD / NO SON, an empty cradle swings down and is
      crossed; his head bows; the palace fades, trees come in and he walks off: SAD, HE LEFT FOR THE / FOREST
  m4  a forest clearing: two sages offer into the yajna fire, the king with folded hands; the fire flares on "yajna";
      THE SAGES DID A YAJNA / FOR A SON, a faint glowing baby in the smoke
  m5  the clay kalasha; light rises from its mouth on "pavitra": THE YAJNA'S / BLESSED WATER, IN A CLAY POT tag; the
      queen comes in as a soft shadow: THIS WATER WAS / FOR THE QUEEN, leaf BHAGAVATA PURANA 9.6.27
  m6  night falls (moon, stars); the sages asleep on their mats; the king's hand goes to his throat: AT NIGHT, THE
      KING GOT VERY / THIRSTY; then AND THE SAGES WERE / ASLEEP
  m7  he lifts the pot and drinks; the light runs into him: THE KING DRANK / THAT WATER
  m8  morning (the sun comes up); the pot tips over, empty; the sages throw up their hands: IN THE MORNING, THE POT
      WAS / EMPTY (ringed); then NOW THERE WAS NO WAY TO / UNDO IT
  m9  the king alone again; a light wakes in his belly and the belly rounds: A BABY... / INSIDE THE KING
  m10 the light grows and moves to his side: WHEN THE TIME CAME, / FROM HIS SIDE; a burst of light, the belly is flat
      again and the baby stands on a lotus in the glow; AND THE KING / LIVED, leaf BHAGAVATA PURANA 9.6.30
  m11 leaf MAHABHARATA / SOME TELLINGS; IN ONE PART OF THE / MAHABHARATA; the twin Ashvins walk in with a herb sprig
      and a medicine pot: DIVINE DOCTORS: / THE TWIN ASHVINS; healing light at the king's side, the baby comes out to
      them: DIVINE DOCTORS: / AN OPERATION
  m12 RE-HOOK: night; the baby alone on the lotus, crying (tears, sound rings): A NEW PROBLEM: THE BABY WAS / HUNGRY;
      a big red "?": WHO WILL / FEED HIM?
  m13 a shaft of light from above; Indra comes down in it (KING OF THE GODS), kneels and gives the baby his finger,
      the crying stops and the finger glows: THEN CAME / INDRA, HE GAVE THE BABY / HIS FINGER; note INDRA SAID: HE
      WILL / DRINK ME
  m14 name card: MANDHATA on a leather plaque, gloss = "HE WILL DRINK ME"; the baby on the lotus below
  m15 the world strip with its cities; the grown Mandhata on his throne: MANDHATA GREW UP TO BE AN / EMPEROR; the cities
      light up; a sun rises on the left, a dotted path arcs over, a sun sets on the right: FROM WHERE THE SUN RISES /
      TO WHERE IT SETS
  m16 leather YES / NO card: DID YOU KNOW / THIS STORY?, the king and the baby small at the bottom
"""
import math

import cairo

import mandhata_cast as M
import puppet_cast as C
import puppet_core as pc
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog
from puppet_core import H, W, depth, keyed, prop, puppet, sway
from scenes_jarasandha import (FADE, FEET, INK, RED, bob_rot, glow, ground, man_angles, motes, red_cross, red_ring,
                               sound_rings, stars, tag, woman_angles)
from scenes_kaikeyi import ANJALI, fig, leaf_tag
from scenes_lakshman_rekha import big_q, big_x, book, quote_note, sparkle, walk_at
from scenes_ravana import dotted, head2
from shots import T, shot_at

MISSES = set()                       # cue words not found in a line (falls back to fractions)
GLOW_C = (1.0, 0.86, 0.45)
HEAL_C = (0.75, 1.0, 0.55)


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, words)
    except (KeyError, ValueError):
        MISSES.add((bid, words[getattr(tl, "lang", "hi")] if isinstance(words, dict) else words))
        return T(tl, bid, frac)


# Every cue of every line: (name, {"hi": word, "kn": word}, fraction fallback, ((after, min gap), ...)); "t0" = the
# line's start. Words are exact substrings of the script lines (checked by the build: MISSES stays empty).
CUES = {
    "m1": (("G", {"hi": "गर्भवती", "kn": "ಗರ್ಭಿಣಿ"}, 0.25, (("t0", 0.6),)),
           ("P", {"hi": "पेट", "kn": "ಹೊಟ್ಟೆ"}, 0.6, (("G", 0.7),)),
           ("B", {"hi": "बेटा", "kn": "ಮಗ"}, 0.8, (("P", 0.6),))),
    "m2": (("X", {"hi": "नहीं", "kn": "ಅಲ್ಲ"}, 0.3, (("t0", 0.6),)),
           ("A", {"hi": "भागवत", "kn": "ಭಾಗವತ"}, 0.45, (("X", 0.5),)),
           ("B", {"hi": "महाभारत", "kn": "ಮಹಾಭಾರತ"}, 0.65, (("A", 0.6),)),
           ("D", {"hi": "दोनों", "kn": "ಎರಡರಲ್ಲೂ"}, 0.8, (("B", 0.5),))),
    "m3": (("Y", {"hi": "युवनाश्व", "kn": "ಯುವನಾಶ್ವ"}, 0.1, (("t0", 0.2),)),
           ("N", {"hi": "नहीं", "kn": "ಮಕ್ಕಳಿರಲಿಲ್ಲ"}, 0.4, (("Y", 0.6),)),
           ("S", {"hi": "दुखी", "kn": "ದುಃಖ"}, 0.6, (("N", 0.7),)),
           ("F", {"hi": "जंगल", "kn": "ಕಾಡಿಗೆ"}, 0.85, (("S", 0.6),))),
    "m4": (("R", {"hi": "ऋषियों", "kn": "ಋಷಿಗಳು"}, 0.1, (("t0", 0.2),)),
           ("Y", {"hi": "यज्ञ", "kn": "ಯಜ್ಞ"}, 0.5, (("R", 0.6),)),
           ("B", {"hi": "बेटा", "kn": "ಮಗ"}, 0.85, (("R", 0.8),))),
    "m5": (("P", {"hi": "पवित्र", "kn": "ಪವಿತ್ರ"}, 0.15, (("t0", 0.3),)),
           ("G", {"hi": "घड़े", "kn": "ಕೊಡದಲ್ಲಿ"}, 0.4, (("P", 0.7),)),
           ("Q", {"hi": "रानी", "kn": "ರಾಣಿ"}, 0.75, (("G", 0.8),))),
    "m6": (("N", {"hi": "रात", "kn": "ರಾತ್ರಿ"}, 0.1, (("t0", 0.1),)),
           ("T", {"hi": "प्यास", "kn": "ಬಾಯಾರಿಕೆ"}, 0.45, (("N", 0.7),)),
           ("S", {"hi": "सो", "kn": "ಮಲಗಿದ್ರು"}, 0.85, (("T", 0.8),))),
    "m7": (("D", {"hi": "पी", "kn": "ಕುಡಿದು"}, 0.6, (("t0", 0.6),)),),
    "m8": (("M", {"hi": "सुबह", "kn": "ಬೆಳಿಗ್ಗೆ"}, 0.05, ()),
           ("E", {"hi": "ख़ाली", "kn": "ಖಾಲಿ"}, 0.45, (("t0", 0.9),)),
           ("X", {"hi": "अब", "kn": "ಈಗ"}, 0.65, (("E", 0.8),))),
    "m9": (("P", {"hi": "पेट", "kn": "ಹೊಟ್ಟೆ"}, 0.45, (("t0", 0.5),)),
           ("B", {"hi": "बच्चा", "kn": "ಮಗು"}, 0.65, (("P", 0.35),)),
           ("G", {"hi": "पलने", "kn": "ಬೆಳೆಯೋಕೆ"}, 0.8, (("B", 0.3),))),
    "m10": (("S", {"hi": "समय", "kn": "ಸಮಯ"}, 0.03, ()),
            ("T", {"hi": "तरफ", "kn": "ಬದಿ"}, 0.5, (("t0", 1.2),)),
            ("O", {"hi": "बाहर", "kn": "ಹೊರಗೆ"}, 0.65, (("T", 0.6),)),
            ("L", {"hi": "ज़िंदा", "kn": "ಬದುಕುಳಿದ"}, 0.88, (("O", 1.0),))),
    "m11": (("M", {"hi": "महाभारत", "kn": "ಮಹಾಭಾರತ"}, 0.03, ()),
            ("V", {"hi": "वैद्य", "kn": "ವೈದ್ಯರು"}, 0.42, (("t0", 1.5),)),
            ("A", {"hi": "अश्विनी", "kn": "ಅಶ್ವಿನೀ"}, 0.52, (("V", 0.4),)),
            ("O", {"hi": "ऑपरेशन", "kn": "ಆಪರೇಷನ್"}, 0.68, (("A", 0.8),))),
    "m12": (("H", {"hi": "भूख", "kn": "ಹಸಿವಿಂದ"}, 0.35, (("t0", 0.6),)),
            ("C", {"hi": "रो", "kn": "ಅಳ್ತಿತ್ತು"}, 0.45, (("H", 0.3),)),
            ("Q", {"hi": "कौन", "kn": "ಯಾರು"}, 0.8, (("C", 0.8),))),
    "m13": (("I", {"hi": "इंद्र", "kn": "ಇಂದ್ರ"}, 0.08, (("t0", 0.2),)),
            ("F", {"hi": "उंगली", "kn": "ಬೆರಳನ್ನ"}, 0.35, (("I", 1.4),)),
            ("Q", {"hi": "कहा", "kn": "ಹೇಳಿದ"}, 0.7, (("F", 0.9),)),
            ("D", {"hi": "पिएगा", "kn": "ಕುಡೀತಾನೆ"}, 0.9, (("Q", 0.4),))),
    "m14": (("N", {"hi": "नाम", "kn": "ಹೆಸರು"}, 0.55, (("t0", 0.3),)),
            ("M", {"hi": "मांधाता", "kn": "ಮಾಂಧಾತ"}, 0.8, (("N", 0.4),))),
    "m15": (("U", {"hi": "उगता", "kn": "ಹುಟ್ಟೋ"}, 0.7, (("t0", 1.8),)),
            ("D", {"hi": "डूबता", "kn": "ಮುಳುಗೋ"}, 0.9, (("U", 0.9),))),
    "m16": (("Y", {"hi": "यस", "kn": "ಹೌದಾ"}, 0.6, (("t0", 0.6),)),
            ("C", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.8, (("Y", 0.4),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_md_cues", None)
    if cache is None:
        cache = {}
        tl._md_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, words, frac, cons in CUES[bid]:
            v = cue(tl, bid, words, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


# ------------------------------------------------------------------ geometry helpers


def local(x, y, s, rot, flip, dx, dy):
    """A point (dx, dy) in a puppet's root coordinates -> scene coordinates."""
    sg = -1 if flip else 1
    px, py = sg * dx * s, dy * s
    c, si = math.cos(rot), math.sin(rot)
    return x + px * c - py * si, y + px * si + py * c


def reach_arm(hip_x, hip_y, s, sh_dx, target, flip=False):
    """(upper, fore) arm angles so the hand of an arm with its shoulder at (sh_dx, -262) (front arm: 26 * bulk, back
    arm: -14 * bulk) lands on target: scenes_ravana.reach for either arm."""
    sgn = -1 if flip else 1
    sx, sy = hip_x + sgn * sh_dx * s, hip_y - 262 * s
    dx, dy = (target[0] - sx) * sgn, target[1] - sy
    a, b = 150 * s, 160 * s
    d = max(1e-3, min(math.hypot(dx, dy), a + b - 1e-3))
    base = math.atan2(-dx, dy)
    ang_a = math.acos(clamp((a * a + d * d - b * b) / (2 * a * d), -1, 1))
    ang_e = math.acos(clamp((a * a + b * b - d * d) / (2 * a * b), -1, 1))
    return base + ang_a, -(math.pi - ang_e)


def mix(p, q, u):
    return tuple(a + (b - a) * u for a, b in zip(p, q))


def held(sprite, arm, s=1.0, dy=150, tilt=0.0, alpha=1.0, blur=0.0):
    """extra= callback: a prop held upright in a hand whose (upper, fore) angles are `arm`."""
    rot = -(arm[0] + arm[1]) + tilt

    def fn(cr_):
        cr_.save()
        cr_.translate(4, dy)
        cr_.rotate(rot)
        cr_.scale(s, s)
        pc.paint_part(cr_, sprite, alpha, blur)
        cr_.restore()
    return fn


def to_user(cr, p):
    return cr.device_to_user(*p)


# ------------------------------------------------------------------ puppets


YV_B = 1.06


def yuva(cr, t, x, s, belly=0.0, feet=FEET, front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0),
         hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.0, y=None, extra=None, hold=0.0,
         back_hand=0.0):
    """King Yuvanashva (feet on `feet`); belly 0..1 rounds his belly (in steps); hold 0..1 brings the front hand onto
    the belly, back_hand 0..1 the back hand to the small of his back. Returns his points (device) plus "belly" (device)
    and "belly_u" (scene coordinates)."""
    lvl = int(round(clamp(belly) * M.BELLY_LEVELS))
    k = lvl / M.BELLY_LEVELS
    hy = feet - 434 * s if y is None else y
    (cx, cy), (fx, fy) = M.belly_xy(k, YV_B)
    if hold > 0:
        tgt = local(x, hy, s, 0, flip, fx - 8, fy - 6)
        front = mix(front, reach_arm(x, hy, s, 26 * YV_B, tgt, flip), ease(hold))
    if back_hand > 0:
        tgt = local(x, hy, s, 0, flip, -72 * YV_B, -84)
        backa = mix(backa, reach_arm(x, hy, s, -14 * YV_B, tgt, flip), ease(back_hand))
    ang = man_angles("yuva", t, front, backa, head, legs, hits, ph)
    r = rot + bob_rot(t, ph)
    swap = {"yuva_body": f"yuva_body_b{lvl}"} if lvl > 0 else None
    pts = puppet(cr, M.YUVA, x, hy, s, r, flip, ang, alpha, blur, swap=swap, rods=rods, extra=extra)
    bu = local(x, hy, s, r, flip, cx, cy)
    pts["belly_u"] = bu
    pts["belly"] = cr.user_to_device(*bu)
    pts["side_u"] = local(x, hy, s, r, flip, fx - 6, -70)
    return pts


def sage(cr, t, rig, key, x, s, **kw):
    return fig(cr, rig, key, t, x, s, **kw)


def sleeper(cr, t, rig, key, x, s, feet=FEET, alpha=1.0, blur=0.0, ph=0.0):
    """A sage asleep on his back (head to the left, eyes closed), breathing slowly; returns his face position. Lying
    down he is ~1090 s long: hair at x - 660 s, soles at x + 426 s."""
    hy = feet - 100 * s
    r = -math.pi / 2 + 0.012 * math.sin(t * 1.5 + ph)
    ang = man_angles(key, t, front=(0.3, -0.25), backa=(0.25, -0.15), head=0.04)
    puppet(cr, rig, x, hy, s, r, False, ang, alpha, blur, swap={key + "_head": "md_sage_sleep"}, rods=True)
    return x - 420 * s, hy - 80 * s


def zzz(cr, t, x, y, s=1.0, alpha=1.0, ph=0.0):
    """Soft sleep letters rising from a sleeper's head."""
    for i in range(3):
        u = (t * 0.42 + i / 3 + ph) % 1.0
        a = math.sin(math.pi * u) * alpha * 0.75
        if a > 0.02:
            draw_text(cr, "z", x + 40 * u * s + 14 * math.sin(t * 2 + i), y - 170 * u * s, int((34 + 22 * u) * s),
                      FADE, a, anchor="cm")


def baby(cr, t, x, feet, s, mode="open", alpha=1.0, blur=0.0, rods=True, rot=0.0, arms=(0.0, 0.0), legs=(0.0, 0.0),
         hits=(), glow_a=0.0, lotus=False, y=None, shake=0.0):
    """The whole baby (soles on `feet`, or hip at y); mode open | shut | cry; glow_a lights it from behind; lotus
    stands it in a lotus. Returns its points (device)."""
    hy = feet - M.BABY_FEET * s if y is None else y
    if glow_a > 0:
        glow(cr, x, hy - 260 * s, 560 * s + 60, glow_a * (0.88 + 0.12 * math.sin(t * 3.3)))
        aura(cr, t, x, hy - 330 * s, 200 * s, 560 * s, glow_a * alpha)
        warm(cr, x, hy - 330 * s, 420 * s, 0.8 * glow_a * alpha)
    if lotus:
        prop(cr, "md_lotus", x, hy + M.BABY_FEET * s - 10 * s, s * 1.15, rot=sway(t, 0.01, 0.4, x), alpha=alpha,
             blur=blur)
    d = pc.dangle(t, hits, 0.3, 1.6, 2.4)
    flail = 0.0
    if mode == "cry":
        flail = 0.35 * math.sin(t * 11) + 0.2 * math.sin(t * 7.3)
    ang = {"mb_armL": arms[0] + d + flail, "mb_armR": -arms[1] - d - flail * 0.8,
           "mb_legL": legs[0], "mb_legR": -legs[1]}
    swap = {"mb_eyes": "mb_eyes_cry"} if mode == "cry" else {"mb_eyes": "mb_eyes_shut"} if mode == "shut" else None
    extra = None
    if mode == "cry":
        extra = {"mb_body": lambda cr_: pc.paint_part(cr_, "mb_mouth", alpha, blur)}
    jig = shake * 0.03 * math.sin(t * 23)
    return puppet(cr, M.BABY, x, hy, s, rot + jig + bob_rot(t, x * 0.01, 0.01), False, ang, alpha, blur, swap=swap,
                  rods=rods, extra=extra)


def ashvin(cr, t, x, s, tool="md_herb", front=(-0.4, -0.5), **kw):
    kw.setdefault("extra", {"ashvin_armF_lo": held(tool, front, 0.9, alpha=kw.get("alpha", 1.0),
                                                   blur=kw.get("blur", 0.0))})
    return fig(cr, M.ASHVIN, "ashvin", t, x, s, front=front, **kw)


IN_BACK = (0.3, -0.45)               # Indra's back hand, low at his side, the vajra upright in it


def indra(cr, t, x, s, front=(-0.32, -0.55), backa=IN_BACK, **kw):
    kw.setdefault("extra", {"indra_armB_lo": held("md_vajra", backa, 0.75, alpha=kw.get("alpha", 1.0),
                                                  blur=kw.get("blur", 0.0))})
    return fig(cr, M.INDRA, "indra", t, x, s, front=front, backa=backa, **kw)


def emperor(cr, t, x, hip_y, s, front=(-1.3, -0.5), backa=(0.25, -0.9), alpha=1.0, blur=0.0, hits=()):
    """Mandhata seated (hip at x, hip_y), the chakra sceptre held up in his front hand, the other on his lap."""
    prop(cr, "mandhata_seat", x, hip_y, s, alpha=alpha, blur=blur)
    ang = man_angles("mandhata", t, front, backa, 0.0, (0.0, 0.0), hits, 1.0)
    return puppet(cr, M.MANDHATA, x, hip_y, s, bob_rot(t, 1.0, 0.006), False, ang, alpha, blur,
                  hide=("mandhata_legF", "mandhata_legB"),
                  extra={"mandhata_armF_lo": held("md_sceptre", front, 0.7, alpha=alpha, blur=blur)})


# ------------------------------------------------------------------ light effects


def lights(cr, t, x, y, r, n, a, col=GLOW_C, speed=0.5, ph=0.0):
    """Sparkles drifting up around (x, y) within radius r."""
    if a <= 0.01:
        return
    for i in range(n):
        u = (t * speed + i / n + ph) % 1.0
        gx = x + r * 0.8 * math.sin(i * 2.4 + ph) + 14 * math.sin(t * 2 + i)
        gy = y + r * 0.4 - r * 1.4 * u
        sparkle(cr, gx, gy, (12 + 8 * (i % 3)) * math.sin(math.pi * u), a, col)


RAY_C = (1.0, 0.72, 0.18)


def warm(cr, x, y, r, a, col=RAY_C):
    """A golden light that shows on the bright middle of the cloth too (glow() only lifts the darker parts)."""
    if a <= 0.01:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, 0.5 * clamp(a))
    g.add_color_stop_rgba(0.45, *col, 0.24 * clamp(a))
    g.add_color_stop_rgba(1, *col, 0.0)
    cr.save()
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def aura(cr, t, x, y, r0, r1, a, n=18, a0=0.0, a1=2 * math.pi, col=RAY_C, spin=0.15):
    """Golden rays of light around (x, y), from r0 to r1, slowly turning and breathing; a0..a1 limits them to a fan."""
    if a <= 0.01:
        return
    cr.save()
    full = abs(a1 - a0) >= 2 * math.pi - 1e-6
    for i in range(n):
        u = (i + 0.5) / n
        ang = a0 + (a1 - a0) * u + (spin * t if full else 0.06 * math.sin(t * 1.3 + i))
        L = r1 * (0.78 + 0.22 * math.sin(t * 2.1 + i * 1.7)) * (1.0 if i % 2 == 0 else 0.8)
        w = 0.07 if i % 2 == 0 else 0.05
        pts = [(x + r0 * math.cos(ang - w * 1.6), y + r0 * math.sin(ang - w * 1.6)),
               (x + L * math.cos(ang), y + L * math.sin(ang)),
               (x + r0 * math.cos(ang + w * 1.6), y + r0 * math.sin(ang + w * 1.6))]
        pc.poly(cr, pts)
        g = cairo.RadialGradient(x, y, r0, x, y, L)
        g.add_color_stop_rgba(0, *col, 0.55 * clamp(a))
        g.add_color_stop_rgba(1, *col, 0.0)
        cr.set_source(g)
        cr.fill()
    cr.restore()


def burst(cr, t, x, y, t_b, n=20, rmax=760.0, alpha=1.0):
    """A burst of light: rays shooting out from (x, y) at t_b, then fading."""
    u = t - t_b
    if u < 0:
        return
    p = ease(u / 0.55)
    fade = math.exp(-1.4 * u) * alpha
    if fade < 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for i in range(n):
        a = 2 * math.pi * i / n + 0.13 * math.sin(i * 2.3) + 0.15 * u
        L = rmax * p * (0.55 + 0.45 * ((i * 7) % 5) / 4)
        w = 0.05 + 0.02 * (i % 2)
        pc.poly(cr, [(x, y), (x + L * math.cos(a - w), y + L * math.sin(a - w)),
                     (x + L * math.cos(a + w), y + L * math.sin(a + w))])
        cr.set_source_rgba(1.0, 0.86, 0.52, 0.32 * fade)
        cr.fill()
    cr.restore()
    glow(cr, x, y, 420, 0.95 * fade)


def beam(cr, x, w0, w1, y1, a):
    """A shaft of light from the top of the screen down to y1 (Indra's arrival)."""
    if a <= 0.01:
        return
    g = cairo.LinearGradient(0, 0, 0, y1)
    g.add_color_stop_rgba(0, 1.0, 0.92, 0.66, 0.42 * a)
    g.add_color_stop_rgba(0.75, 1.0, 0.86, 0.52, 0.22 * a)
    g.add_color_stop_rgba(1, 1.0, 0.82, 0.45, 0.0)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    pc.poly(cr, [(x - w0 / 2, -20), (x + w0 / 2, -20), (x + w1 / 2, y1), (x - w1 / 2, y1)])
    cr.set_source(g)
    cr.fill()
    cr.restore()


def kalasha(cr, t, x, feet, s, light=0.0, rot=0.0, alpha=1.0, blur=0.0, pivot=None):
    """The clay pot of blessed water; light 0..1 = how much the water glows (a column of light out of its mouth).
    pivot = (x, y) of its bottom centre when it is lifted or tipped (else it stands at x, feet)."""
    px, py = pivot if pivot is not None else (x, feet)
    mx, my = local(px, py, s, rot, False, 0, -318)
    if light > 0:
        glow(cr, mx, my - 40 * s, 260 * s + 80, 0.75 * light * (0.85 + 0.15 * math.sin(t * 4)))
        glow(cr, mx, my - 260 * s, 200 * s + 40, 0.4 * light)
        up = rot - math.pi / 2                          # the pot's "up", for the fan of light out of its mouth
        aura(cr, t, mx, my, 40 * s, 520 * s, light, n=9, a0=up - 0.75, a1=up + 0.75)
        warm(cr, mx, my - 60 * s, 300 * s, 0.7 * light)
    prop(cr, "md_kalasha", px, py, s, rot=rot, alpha=alpha, blur=blur)
    if light > 0:
        lights(cr, t, mx, my - 60 * s, 120 * s + 30, 8, light, speed=0.6)
    return mx, my


# ------------------------------------------------------------------ m1  hook


HOOK = (420, 1.06, 1840)             # the king's x, scale and feet in the hook
HOOK_BABY = (860, 1330, 0.34)        # the baby beside him: x, hip y, scale


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "m1")
    tG, tP, tB = c["G"], c["P"], c["B"]
    x, s, feet = HOOK
    look = keyed(t, [(0.0, 0.13), (tB + 0.05, -0.02)], 0.35, 1.3)
    pts = yuva(cr, t, x, s, belly=1.0, feet=feet, hold=1.0, back_hand=1.0, head=look, hits=[(tG, 0.4)], ph=0.3)
    bx, by = pts["belly_u"]
    beat = 0.5 + 0.5 * math.sin(t * 3.4)
    glow(cr, bx, by, 260 + 80 * prog(t, tG, 0.5),
         (0.3 + 0.3 * prog(t, tG, 0.4)) * (0.8 + 0.2 * beat) + 0.4 * math.exp(-4 * max(0, t - tG)) * (t > tG))
    warm(cr, bx, by, 150 + 30 * beat, 0.45 + 0.35 * prog(t, tG, 0.4))
    lights(cr, t, bx, by, 110, 5, 0.6 * prog(t, tG, 0.4), speed=0.45)
    if t > tB - 0.05:                                   # the son: a small glowing baby beside him
        q = back(clamp((t - tB + 0.05) / 0.45), 1.6)
        bxx, hy, bs = HOOK_BABY
        hy += 10 * math.sin(t * 2.4)
        baby(cr, t, bxx, None, bs * max(q, 0.01), y=hy, alpha=clamp(q * 2), hits=[(tB + 0.35, 1.0)],
             glow_a=0.9 * clamp(q))
        lights(cr, t, bxx, hy - 200 * bs, 160, 7, clamp(q))
    dev_belly = pts["belly"]

    def ui(cr):
        head2(cr, t, "A KING WHO GOT", -1.0, "PREGNANT", 0.4, big_size=240, ghost=-1.0, under=tG + 0.2)
        if t > tP:
            red_ring(cr, dev_belly[0] - 4, dev_belly[1] - 4, 160, 145, prog(t, tP, 0.45), 10,
                     alpha=1 - prog(t, tB + 0.6, 0.4))
        tag(cr, t, tB + 0.35, "HIS SON", HOOK_BABY[0], 1560, 42)
    fl = 0.4 * math.exp(-5 * max(0, t - tG)) * (t > tG) + 0.35 * math.exp(-5 * max(0, t - tB)) * (t > tB)
    return dict(ui=ui, flash=fl)


# ------------------------------------------------------------------ m2  it's in both books


def s_books(cr, t, tl, t0, t1):
    c = cues(tl, "m2")
    tX, tA, tB, tD = c["X"], c["A"], c["B"], c["D"]
    bh = [(None, [("BHAGAVATA PURANA", 84, HEAD_FONT)], 0),
          (tA + 0.35, [([("BOOK 9, CHAPTER 6:", INK), ("9.6.25-37", RED)], 66, HEAD_FONT)], 0)]
    mb = [(None, [("MAHABHARATA", 92, HEAD_FONT)], 0),
          (tB + 0.35, [([("VANA PARVA", INK), ("126", RED)], 74, HEAD_FONT)], 0)]
    book(cr, t, 540, 720, 0.8, bh, t_in=t0 + 0.05, t_open=tA, ring=(1, 0, 1, tD + 0.15))
    book(cr, t, 540, 1190, 0.8, mb, t_in=t0 + 0.3, t_open=tB, ring=(1, 0, 1, tD + 0.3))

    def ui(cr):
        if t < tD:
            struck = t > tX + 0.25
            box = head2(cr, t, "THIS IS NOT A", t0 + 0.05, "JOKE", t0 + 0.4, big_size=230,
                        big_color=FADE if struck else INK)
            if box and t > tX:
                bx, by, bw, bh_ = box
                big_x(cr, W / 2, by + bh_ / 2, bw + 70, bh_ * 0.95, prog(t, tX, 0.3), lw=24)
        else:
            head2(cr, t, "IT'S WRITTEN IN", tD, "BOTH", tD + 0.06, big_size=250, under=tD + 0.4)
    return dict(ui=ui, flash=0.25 * math.exp(-4 * max(0, t - tA)) * (t > tA) + 0.2 * math.exp(-4 * max(0, t - tD)) * (
        t > tD))


# ------------------------------------------------------------------ m3  no son; to the forest


def s_noson(cr, t, tl, t0, t1):
    c = cues(tl, "m3")
    tY, tN, tS, tF = c["Y"], c["N"], c["S"], c["F"]
    leave = prog(t, tF - 0.1, 0.6)
    if leave < 1:
        b, k, a = depth(t, t0 - 0.2, 0.45)
        prop(cr, "arch", 540, FEET + 10, 0.8 * k, alpha=0.85 * a * (1 - leave), blur=b + 3 + 4 * leave)
    if leave > 0:                                       # the forest comes in
        for i, (tx, ts, fl, ph) in enumerate(((990, 0.66, False, 0.0), (80, 0.6, True, 1.0), (640, 0.5, False, 2.0))):
            b, k, a = depth(t, tF - 0.1 + 0.12 * i, 0.5)
            prop(cr, "tree", tx, FEET + 10, ts * k, rot=sway(t, 0.006, 0.3, ph), alpha=a * (0.9 if i < 2 else 0.6),
                 blur=b + (0 if i < 2 else 6), flip=fl)
    ground(cr)
    cradle_a = 1 - leave
    if t > tN - 0.3 and cradle_a > 0:                    # an empty cradle swings down
        p = ease((t - tN + 0.3) / 0.4)
        sw = 0.22 * math.exp(-0.8 * max(0, t - tN)) * math.sin(3.2 * (t - tN)) + 0.04 * math.sin(t * 1.7)
        prop(cr, "cradle", 720, 820 - 320 * (1 - p), 0.6, rot=sw, alpha=p * cradle_a)
        pc.rod(cr, 720, 820 - 320 * (1 - p), 720, 300, alpha=0.6 * p * cradle_a)
    sad = prog(t, tS - 0.1, 0.6)
    if t < tF:
        yuva(cr, t, 360, 0.82, front=(-0.3 - 0.2 * (1 - sad), -0.5), head=0.04 + 0.2 * sad, hits=[(tN, 0.4)], ph=0.4)
    else:
        walk_at(cr, t, yuva, tF, tF + 1.8, 360, 1260, 0.82, step=0.45, head=0.22, front=(-0.25, -0.4), ph=0.4)

    def ui(cr):
        tag(cr, t, tY, "KING YUVANASHVA", 730, 1310, 38, t_out=tF - 0.2)
        if t < tS:
            head2(cr, t, "THE KING HAD", t0 + 0.05, "NO SON", tN, big_size=240, under=tN + 0.35)
        else:
            head2(cr, t, "SAD, HE LEFT FOR THE", tS, "FOREST", tF, big_size=240)
        if tN < t and cradle_a > 0:
            red_cross(cr, 720, 1020, 170, prog(t, tN + 0.35, 0.3), alpha=cradle_a)
    return dict(ui=ui, flash=0.25 * math.exp(-4 * max(0, t - tN)) * (t > tN))


# ------------------------------------------------------------------ m4  the yajna


FIRE = (640, FEET)


def yajna_fire(cr, t, x, feet, s=1.0, flare=0.0, alpha=1.0):
    glow(cr, x, feet - 190 * s, (320 + 160 * flare) * s, (0.55 + 0.35 * flare) * (0.85 + 0.15 * math.sin(t * 7)) * alpha)
    prop(cr, "altar", x, feet + 14, 0.72 * s, alpha=alpha)
    prop(cr, f"flame{int(t * 10) % 3}", x, feet - 44 * s, (0.5 + 0.28 * flare) * s, alpha=alpha)
    lights(cr, t, x, feet - 260 * s, 110 * s, 9, (0.6 + 0.4 * flare) * alpha, (1.0, 0.7, 0.3), 0.8)


def s_yajna(cr, t, tl, t0, t1):
    c = cues(tl, "m4")
    tR, tY, tB = c["R"], c["Y"], c["B"]
    prop(cr, "tree", 1020, FEET + 10, 0.6, rot=sway(t, 0.006, 0.3), alpha=0.55, blur=10)
    prop(cr, "tree", 30, FEET + 10, 0.55, rot=sway(t, 0.006, 0.3, 1), alpha=0.5, blur=12, flip=True)
    flare = math.exp(-1.6 * max(0, t - tY)) * (t > tY) * 0.9 + 0.25 * prog(t, tY, 0.3)
    fx, ff = FIRE
    if t > tB - 0.2:                                    # the wish: a faint glowing child in the smoke
        q = prog(t, tB - 0.2, 0.7)
        glow(cr, fx, 880, 260, 0.5 * q)
        baby(cr, t, fx, None, 0.22, y=900 - 30 * q + 8 * math.sin(t * 2), alpha=0.45 * q, blur=4, rods=False)
    yajna_fire(cr, t, fx, ff, 1.0, flare)
    ground(cr)
    yuva(cr, t, 150, 0.66, head=0.08, ph=0.4, **ANJALI)

    def offer(ph):
        if t < tR:
            return 0.0
        u = ((t - tR) / 0.9 + ph) % 1.0
        return math.sin(math.pi * clamp(u / 0.5)) if u < 0.5 else 0.0
    oa, ob = offer(0.0), offer(0.45)
    sage(cr, t, M.PULASTYA, "pulastya", 400, 0.72, front=(-0.55 - 0.35 * oa, -0.35 + 0.25 * oa),
         backa=(-0.2, -0.6), head=0.1, ph=1.0)
    sage(cr, t, M.MDSAGE, "mdsage", 900, 0.72, flip=True, front=(-0.55 - 0.35 * ob, -0.35 + 0.25 * ob),
         backa=(-0.2, -0.6), head=0.1, ph=2.2)

    def ui(cr):
        head2(cr, t, "THE SAGES DID A YAJNA", t0 + 0.05, "FOR A SON", tB, big_size=230, under=tB + 0.4)
        tag(cr, t, tR + 0.1, "THE SAGES", 650, 760, 36, t_out=tB - 0.1)
    return dict(ui=ui, flash=0.4 * math.exp(-4 * max(0, t - tY)) * (t > tY))


# ------------------------------------------------------------------ m5  the blessed water, for the queen


EV_27 = [("BHAGAVATA PURANA", 34, MONO_FONT), ("9.6.27", 56, HEAD_FONT)]
EV_30 = [("BHAGAVATA PURANA", 34, MONO_FONT), ("9.6.30", 56, HEAD_FONT)]


def s_water(cr, t, tl, t0, t1):
    c = cues(tl, "m5")
    tP, tG, tQ = c["P"], c["G"], c["Q"]
    if t > tQ - 0.3:                                    # the queen: a soft shadow, away from the cloth
        m = prog(t, tQ - 0.3, 0.6)
        puppet(cr, C.QUEEN1, 880, 1250 - 50 * m, 0.88, bob_rot(t, 2), flip=True,
               angles=woman_angles("queen1", t, front=(-0.5, -0.7)), alpha=0.7 * m, blur=9 + 10 * (1 - m),
               rods=False)
    ground(cr)
    b, k, a = depth(t, t0, 0.5)
    light = prog(t, tP - 0.1, 0.5)
    kalasha(cr, t, 470, FEET, 1.25 * k, light, alpha=a, blur=b)
    bless = keyed(t, [(t0, 0.0), (tP - 0.1, 1.0), (tQ, 0.3)], 0.35, 1.3)
    sage(cr, t, M.PULASTYA, "pulastya", 140, 0.7, front=(-0.5 - 1.1 * bless, -0.6 + 0.3 * bless), head=0.05, ph=1.0)

    def ui(cr):
        if t < tQ:
            head2(cr, t, "THE YAJNA'S", t0 + 0.05, "BLESSED WATER", tP, big_size=210)
            tag(cr, t, tG, "IN A CLAY POT", 470, 1060, 38, t_out=tQ - 0.1)
        else:
            head2(cr, t, "THIS WATER WAS", tQ, "FOR THE QUEEN", tQ + 0.06, big_size=210, under=tQ + 0.4)
            leaf_tag(cr, t, tQ + 0.35, 760, 690, 0.8, EV_27, rot=0.04)
    return dict(ui=ui, flash=0.3 * math.exp(-4 * max(0, t - tP)) * (t > tP))


# ------------------------------------------------------------------ m6  night: thirsty; the sages asleep


NIGHT = 0.42
POT_N = (950, FEET, 0.62)            # the pot in the night shot: x, feet, scale


def night_sky(cr, t, dark, mx=210):
    prop(cr, "moon", mx, 780 - 130 * dark, 0.8, rot=-0.3, alpha=dark)
    stars(cr, t, dark, pts=((420, 640), (640, 720), (860, 620), (990, 820), (90, 900)))


def s_night(cr, t, tl, t0, t1):
    c = cues(tl, "m6")
    tN, tT, tS = c["N"], c["T"], c["S"]
    dark = prog(t, tN - 0.3, 0.9)
    night_sky(cr, t, dark)
    ground(cr)
    prop(cr, "md_mat", 470, FEET - 96, 0.7, alpha=0.85, blur=2.5)
    h1 = sleeper(cr, t, M.MDSAGE, "mdsage", 500, 0.56, feet=FEET - 92, alpha=0.9, blur=2.0, ph=1.0)
    prop(cr, "md_mat", 420, FEET - 30, 0.76)
    h2 = sleeper(cr, t, M.PULASTYA, "pulastya", 470, 0.66, feet=FEET - 26, ph=0.0)
    heads = [h1, h2]
    px, pf, ps = POT_N
    kalasha(cr, t, px, pf, ps, 0.8)
    thirst = keyed(t, [(t0, 0.0), (tT - 0.1, 1.0)], 0.35, 1.3)
    x, s = 805, 0.78                                    # the king stands by them, facing the glowing pot
    hy = FEET - 434 * s
    throat = local(x, hy, s, 0, False, 40, -292)
    front = mix((-0.4, -0.5), reach_arm(x, hy, s, 26 * YV_B, throat, False), thirst)
    wob = 0.02 * thirst * math.sin(t * 5)
    yuva(cr, t, x, s, front=front, head=-0.16 * thirst, rot=wob, hits=[(tT, 0.4)], ph=0.4)
    for i, (hx, hy2) in enumerate(heads):
        zzz(cr, t, hx, hy2 - 30, 1.0, prog(t, tS - 0.3, 0.5) * (0.6 if i == 0 else 1.0), ph=0.4 * i)

    def ui(cr):
        if t < tS:
            head2(cr, t, "AT NIGHT, THE KING GOT VERY", t0 + 0.05, "THIRSTY", tT, big_size=240)
        else:
            head2(cr, t, "AND THE SAGES WERE", tS, "ASLEEP", tS + 0.06, big_size=240)
    return dict(ui=ui, night=NIGHT * dark, flash=0.2 * math.exp(-4 * max(0, t - tT)) * (t > tT))


# ------------------------------------------------------------------ m7  he drinks it


def s_drink(cr, t, tl, t0, t1):
    tD = cues(tl, "m7")["D"]
    night_sky(cr, t, 1.0, mx=900)
    ground(cr)
    x, s = 420, 0.92
    hy = FEET - 434 * s
    lift = keyed(t, [(t0, 0.0), (tD - 0.4, 1.0)], 0.45, 1.15)
    tilt = keyed(t, [(t0, 0.0), (tD - 0.05, 1.0)], 0.5, 1.1)
    head = -0.26 * tilt
    ps = 0.55
    r = -1.25 * tilt
    rest_mouth = (196, -232)
    hm = (52 + 10, -388 + 6)                            # his mouth with his head tipped back (body units)
    mxu, myu = mix(rest_mouth, hm, lift)
    L = 318 * ps
    pvx = mxu - L * math.sin(r)                         # the pot's bottom centre, so its mouth sits at (mxu, myu)
    pvy = myu + L * math.cos(r)
    piv = (x + s * pvx, hy + s * pvy)
    hold_f = local(piv[0], piv[1], s * ps, r, False, 70, -120)
    hold_b = local(piv[0], piv[1], s * ps, r, False, -30, -40)
    front = reach_arm(x, hy, s, 26 * YV_B, hold_f)
    backa = reach_arm(x, hy, s, -14 * YV_B, hold_b)
    light = 1.0 - prog(t, tD + 0.2, 1.0)
    m0 = cr.get_matrix()

    def pot_fn(cr_):                                    # drawn between his body and his front arm
        cr_.save()
        cr_.set_matrix(m0)
        kalasha(cr_, t, 0, 0, s * ps, light, rot=r, pivot=piv)
        cr_.restore()
    pts = yuva(cr, t, x, s, front=front, backa=backa, head=head, extra={"yuva_head": pot_fn}, ph=0.4)
    drink = prog(t, tD - 0.1, 0.3) * (1 - prog(t, tD + 1.6, 0.5))
    if drink > 0:                                       # the light runs into him, down to the belly
        mx, my = x + s * hm[0], hy + s * hm[1]
        bx, by = pts["belly_u"]
        for i in range(12):
            u = (t * 0.9 + i / 12) % 1.0
            gx = mx + (bx - mx) * u + 12 * math.sin(t * 3 + i)
            gy = my + (by - my) * u
            sparkle(cr, gx, gy, 16 * math.sin(math.pi * u) + 4, drink)
    seed = prog(t, tD + 0.3, 0.8)
    if seed > 0:
        bx, by = pts["belly_u"]
        glow(cr, bx, by, 220, 0.45 * seed)
        warm(cr, bx, by, 120, 0.6 * seed)

    def ui(cr):
        head2(cr, t, "THE KING DRANK", t0 + 0.05, "THAT WATER", tD, big_size=240, under=tD + 0.4)
    return dict(ui=ui, night=NIGHT, flash=0.3 * math.exp(-4 * max(0, t - tD)) * (t > tD))


# ------------------------------------------------------------------ m8  morning: the pot is empty


def s_empty(cr, t, tl, t0, t1):
    c = cues(tl, "m8")
    tM, tE, tX = c["M"], c["E"], c["X"]
    rise = ease((t - t0) / 1.4)
    prop(cr, "sun", 180, 900 - 230 * rise, 0.34, rot=t * 0.3, alpha=0.9 * rise)
    ground(cr)
    px, pf, ps = 600, FEET, 0.78
    tip = clamp((t - tE + 0.25) / 0.35)                 # the pot tips over as they look
    r = -(math.pi / 2 - 0.08) * ease(tip)
    if tip >= 1:
        dt = t - tE - 0.1
        r += 0.08 * math.exp(-5 * dt) * math.sin(14 * dt)
    piv = (px, pf - 140 * ps * math.sin(-r))
    kalasha(cr, t, px, pf, ps, 0.0, rot=r, pivot=piv)
    shock = keyed(t, [(t0, 0.0), (tE, 1.0), (tX + 0.2, 0.25)], 0.22, 1.8)
    for rig, key, x, fl, ph in ((M.PULASTYA, "pulastya", 250, False, 1.0), (M.MDSAGE, "mdsage", 870, True, 2.2)):
        sage(cr, t, rig, key, x, 0.74, flip=fl, front=(-0.4 - 2.0 * shock, -0.5 - 0.6 * shock),
             backa=(0.2 - 1.6 * shock, -0.4 - 0.5 * shock), head=-0.14 * shock + 0.16 * prog(t, tX, 0.5),
             hits=[(tE, 0.9)], ph=ph)
    mx, my = cr.user_to_device(*local(piv[0], piv[1], ps, r, False, 0, -150))

    def ui(cr):
        if t < tX:
            head2(cr, t, "IN THE MORNING, THE POT WAS", t0 + 0.05, "EMPTY", tE, big_size=250, under=tE + 0.35)
            if t > tE:
                red_ring(cr, mx, my, 230, 160, prog(t, tE + 0.3, 0.45), 10)
        else:
            head2(cr, t, "NOW THERE WAS NO WAY TO", tX, "UNDO IT", tX + 0.06, big_size=240)
    return dict(ui=ui, night=NIGHT * (1 - rise), flash=0.3 * math.exp(-4 * max(0, t - tE)) * (t > tE))


# ------------------------------------------------------------------ m9  a baby inside the king


def s_inside(cr, t, tl, t0, t1):
    c = cues(tl, "m9")
    tP, tB, tG = c["P"], c["B"], c["G"]
    t_full = max(tG + 0.7, tP + 1.4)
    grow = clamp((t - tP + 0.1) / (t_full - tP + 0.1))
    x, s, feet = 450, 1.0, 1800
    hold = prog(t, tP - 0.3, 0.5)
    pts = yuva(cr, t, x, s, belly=grow, feet=feet, hold=hold, back_hand=prog(t, tG, 0.6),
               head=0.1 * hold, hits=[(tP, 0.3)], ph=0.3)
    bx, by = pts["belly_u"]
    beat = math.exp(-5 * ((t - tB) % 0.85)) if t > tB else 0.0
    on = prog(t, tP - 0.2, 0.4)
    glow(cr, bx, by, 180 + 140 * grow + 50 * beat, (0.25 + 0.55 * grow) * on + 0.25 * beat)
    warm(cr, bx, by, 90 + 90 * grow + 25 * beat, (0.3 + 0.6 * grow) * on)
    lights(cr, t, bx, by, 90 + 40 * grow, 6, 0.8 * prog(t, tB, 0.4), speed=0.4)
    dev = pts["belly"]

    def ui(cr):
        if t < tB:
            head2(cr, t, "AND THEN...", t0 + 0.05, None, 0.0)
        else:
            head2(cr, t, "A BABY...", tB, "INSIDE THE KING", tB + 0.2, big_size=210)
        if t > tB:
            sound_rings(cr, dev[0], dev[1], t, tB + 0.1, 4, 0.85, 200, alpha=0.5, color=RED)
    return dict(ui=ui, flash=0.35 * math.exp(-4 * max(0, t - tB)) * (t > tB))


# ------------------------------------------------------------------ m10  the birth: a burst of light


LOTUS_B = (790, FEET - 30, 0.5)      # where the newborn stands on the lotus: x, soles, scale


def s_birth(cr, t, tl, t0, t1):
    c = cues(tl, "m10")
    tS, tT, tO, tL = c["S"], c["T"], c["O"], c["L"]
    born = t >= tO
    belly = 1.0 if not born else 1.0 - ease((t - tO) / 0.5)
    lift = keyed(t, [(t0, 0.0), (tL, 1.0)], 0.35, 1.4)
    ground(cr)
    x, s = 330, 0.92
    hold = 1.0 - prog(t, tO, 0.4)
    front = (-0.6 - 1.4 * lift, -0.4 + 0.3 * lift)
    pts = yuva(cr, t, x, s, belly=belly, front=front, hold=hold, back_hand=0.0, head=0.08 * hold - 0.1 * lift,
               hits=[(tO, 0.8), (tL, 0.5)], ph=0.3)
    bx, by = pts["belly_u"]
    sx_, sy_ = pts["side_u"]
    side = prog(t, tT - 0.2, 0.6)
    gx, gy = bx + (sx_ - bx) * side, by + (sy_ - by) * side
    before = 1 - prog(t, tO + 0.1, 0.4)
    grow = prog(t, tS, 1.2)
    glow(cr, gx, gy, 220 + 160 * prog(t, tS, 1.5), (0.4 + 0.5 * grow) * before)
    warm(cr, gx, gy, 150 + 70 * grow, (0.6 + 0.4 * grow) * before)
    aura(cr, t, gx, gy, 60, 170 + 120 * prog(t, tT, 0.8), 0.7 * prog(t, tT - 0.3, 0.5) * before, n=14)
    lights(cr, t, gx, gy, 120, 7, 0.8 * before, speed=0.6)
    burst(cr, t, sx_, sy_, tO)
    lx, lf, ls = LOTUS_B
    if born:                                            # the baby comes out in the light and lands on the lotus
        q = ease((t - tO) / 0.7)
        hy0 = sy_
        hy1 = lf - M.BABY_FEET * ls
        bxx = sx_ + (lx - sx_) * q
        byy = hy0 + (hy1 - hy0) * q - 160 * math.sin(math.pi * q)
        sc = 0.12 + (ls - 0.12) * q
        if q >= 1:
            prop(cr, "md_lotus", lx, lf - 10 * ls, ls * 1.15, rot=sway(t, 0.01, 0.4))
        else:
            prop(cr, "md_lotus", lx, lf - 10 * ls, ls * 1.15 * q, alpha=q)
        baby(cr, t, bxx, None, sc, y=byy, glow_a=0.85, hits=[(tO + 0.7, 1.0)], rods=q > 0.6)
        lights(cr, t, bxx, byy - 200 * sc, 150, 8, 1.0)
    dev = pts["belly"]

    def ui(cr):
        if t < tO:                                      # the light inside beats, faster as the time comes
            sound_rings(cr, dev[0], dev[1], t, t0 + 0.7, 4, 0.55, 190, alpha=0.5, color=RED)
        if t < tL:
            head2(cr, t, "WHEN THE TIME CAME,", t0 + 0.05, "FROM HIS SIDE" if t > tT else None, tT, big_size=220)
        else:
            head2(cr, t, "AND THE KING", tL, "LIVED", tL + 0.06, big_size=260, under=tL + 0.35)
            leaf_tag(cr, t, tL + 0.3, 790, 700, 0.8, EV_30, rot=0.04)
    return dict(ui=ui, flash=0.9 * math.exp(-3 * max(0, t - tO)) * born + 0.2 * math.exp(-4 * max(0, t - tL)) * (
        t > tL))


# ------------------------------------------------------------------ m11  the Ashvins: an operation


def s_ashvins(cr, t, tl, t0, t1):
    c = cues(tl, "m11")
    tM, tV, tA, tO = c["M"], c["V"], c["A"], c["O"]
    ground(cr)
    out = prog(t, tO + 0.3, 0.6)
    x, s = 540, 0.74
    pts = yuva(cr, t, x, s, belly=1.0 - out, hold=prog(t, t0 + 0.9, 0.45) * (1.0 - out), head=-0.04, ph=0.3,
               hits=[(t0 + 0.9, 0.4)])
    sx_, sy_ = pts["side_u"]
    heal = prog(t, tO - 0.2, 0.5)
    glow(cr, sx_, sy_, 260, (0.3 + 0.5 * heal) * (0.85 + 0.15 * math.sin(t * 5)) * (1 - 0.5 * out))
    warm(cr, sx_, sy_, 150, (0.35 + 0.5 * heal) * (1 - 0.6 * out))
    aura(cr, t, sx_, sy_, 50, 230, 0.8 * heal * (1 - 0.6 * out), n=14, col=(0.55, 0.85, 0.25))
    lights(cr, t, sx_, sy_, 130, 8, heal * (1 - 0.6 * out), HEAL_C, 0.6)
    t_in = min(tV - 0.35, t0 + 1.7)                     # the twins come in early enough to fill a long line
    raise_ = keyed(t, [(t0, 0.0), (tO - 0.1, 1.0)], 0.3, 1.4)
    fr = (-0.4 - 1.0 * raise_, -0.5 + 0.25 * raise_)
    for tool, x0, x1, fl, d in (("md_herb", -260, 215, False, 0.0), ("md_medpot", 1340, 870, True, 0.12)):
        if t < t_in + d:
            continue
        if t < t_in + d + 1.2:
            walk_at(cr, t, lambda cr_, t_, x_, s_, **kw: ashvin(cr_, t_, x_, s_, tool, front=(-0.4, -0.5), **kw),
                    t_in + d, t_in + d + 1.2, x0, x1, 0.74, t_in=t_in + d, step=0.4, flip=fl, ph=d * 10)
        else:
            ashvin(cr, t, x1, 0.74, tool, front=fr, flip=fl, head=0.04 * raise_, hits=[(tO, 0.5)], ph=d * 10)
    if t > tO + 0.25:                                   # the baby comes out into the light, to the healers
        q = ease((t - tO - 0.25) / 0.8)
        bxx = sx_ + (735 - sx_) * q
        byy = sy_ + (1290 - sy_) * q - 120 * math.sin(math.pi * q)
        baby(cr, t, bxx, None, 0.12 + 0.2 * q, y=byy, glow_a=0.8, rods=False, mode="shut")

    def ui(cr):
        leaf_tag(cr, t, tM + 0.3, 790, 680, 0.8, [("MAHABHARATA", 52, HEAD_FONT), ("SOME TELLINGS", 34, MONO_FONT)],
                 rot=0.04)
        if t < tV:
            head2(cr, t, "IN ONE PART OF THE", t0 + 0.05, "MAHABHARATA", tM + 0.15, big_size=210)
        elif t < tO:
            head2(cr, t, "DIVINE DOCTORS:", tV, "THE TWIN ASHVINS", tA, big_size=190)
        else:
            head2(cr, t, "DIVINE DOCTORS:", tV, "AN OPERATION", tO, big_size=210, under=tO + 0.4)
    return dict(ui=ui, flash=0.3 * math.exp(-4 * max(0, t - tO)) * (t > tO))


# ------------------------------------------------------------------ m12  re-hook: who will feed him?


def s_hungry(cr, t, tl, t0, t1):
    c = cues(tl, "m12")
    tH, tC, tQ = c["H"], c["C"], c["Q"]
    ground(cr)
    crying = t > tC
    bx, bf, bs = 540, FEET - 40, 0.76
    pts = baby(cr, t, bx, bf, bs, mode="cry" if crying else "open", lotus=True, glow_a=0.45,
               hits=[(tH, 0.8)], shake=1.0 if crying else 0.0)
    mx, my = pts["mouth"]

    def ui(cr):
        if t < tQ:
            head2(cr, t, "A NEW PROBLEM: THE BABY WAS", t0 + 0.05, "HUNGRY", tH, big_size=240)
        else:
            head2(cr, t, "WHO WILL", tQ, "FEED HIM?", tQ + 0.06, big_size=240)
        if crying:
            sound_rings(cr, mx, my, t, tC, 8, 0.4, 260, alpha=0.6)
        big_q(cr, t, tQ, 900, 860, 300)
    return dict(ui=ui, night=0.32 + 0.12 * prog(t, tQ, 0.4), flash=0.3 * math.exp(-5 * max(0, t - tQ)) * (t > tQ))


# ------------------------------------------------------------------ m13  Indra: "he will drink me"


IN_X, IN_S = 700, 0.85               # Indra in the feeding shot
BB = (455, FEET - 30, 0.5)           # the baby there: x, soles, scale


def s_indra(cr, t, tl, t0, t1):
    c = cues(tl, "m13")
    tI, tF, tQ, tD = c["I"], c["F"], c["Q"], c["D"]
    light = prog(t, tI - 0.35, 0.6)
    beam(cr, IN_X, 300, 620, FEET + 40, light * (0.85 + 0.1 * math.sin(t * 2.3)))
    glow(cr, IN_X, 300, 420, 0.6 * light)
    ground(cr)
    t_kneel = max(tI + 1.0, tF - 0.6)
    fed = t > tF + 0.15
    bx, bf, bs = BB
    bpts = baby(cr, t, bx, bf, bs, mode="shut" if fed else "cry", lotus=True, glow_a=0.4 + 0.4 * prog(t, tF, 0.5),
                shake=0.0 if fed else 0.7)
    mouth = to_user(cr, bpts["mouth"])
    if t < t_kneel:                                     # he comes down in the light
        d = ease((t - tI + 0.25) / 0.9)
        b, k, a = depth(t, tI - 0.25, 0.9)
        y = FEET - 434 * IN_S - 820 * (1 - d)
        indra(cr, t, IN_X, IN_S * k, flip=True, y=y, alpha=a, blur=b, front=(-2.35, 0.45), head=0.02, ph=0.5)
    else:
        kq = ease((t - t_kneel) / 0.3)
        ky = FEET - 250 * IN_S
        hip = (IN_X, ky + 12 * (1 - kq))
        reach_ = keyed(t, [(t_kneel, 0.0), (tF - 0.12, 1.0)], 0.35, 1.15)
        tgt = (mouth[0] + 14, mouth[1] + 6)
        fr = mix((-2.35, 0.45), reach_arm(hip[0], hip[1], IN_S, 26 * 1.1, tgt, True), reach_)
        indra(cr, t, IN_X, IN_S, flip=True, kneel="indra_kneel", y=hip[1], front=fr, head=0.1 * reach_, ph=0.5)
        if fed:
            glow(cr, tgt[0], tgt[1], 160, 0.6 * (0.85 + 0.15 * math.sin(t * 5)))
            lights(cr, t, tgt[0], tgt[1], 70, 6, 0.9, speed=0.5)

    def ui(cr):
        if t < tF:
            head2(cr, t, "THEN CAME", tI - 0.1, "INDRA", tI, big_size=260)
            tag(cr, t, tI + 0.45, "KING OF THE GODS", 300, 700, 36)
        else:
            head2(cr, t, "HE GAVE THE BABY", tF, "HIS FINGER", tF + 0.06, big_size=230)
        if t > tQ:
            quote_note(cr, t, tQ, 296, 840, 0.6,
                       [("INDRA SAID:", 44, INK, MONO_FONT, -150, tQ),
                        ("HE WILL", 110, INK, HEAD_FONT, -42, tQ + 0.12),
                        ("DRINK ME", 140, RED, HEAD_FONT, 96, tD)])
    return dict(ui=ui, flash=0.3 * math.exp(-3 * max(0, t - tI)) * (t > tI) + 0.25 * math.exp(-4 * max(0, t - tF)) * (
        t > tF))


# ------------------------------------------------------------------ m14  the name


def s_name(cr, t, tl, t0, t1):
    c = cues(tl, "m14")
    tN, tM = c["N"], c["M"]
    beam(cr, 540, 260, 560, FEET + 40, 0.45)            # the light Indra came in, still on the child
    ground(cr)
    baby(cr, t, 540, FEET - 30, 0.42, mode="shut", lotus=True, glow_a=0.6 + 0.3 * prog(t, tM, 0.4))
    y = 790
    q = back(clamp((t - t0) / 0.4), 1.3)
    cr.save()
    cr.translate(540, y + 70 * (1 - q))
    cr.rotate(sway(t, 0.008, 0.4))
    cr.scale(1.12, 1.12)
    pc.paint_part(cr, "plaque", alpha=clamp(q))
    cr.restore()
    pc.rod(cr, 540, y + 70 * (1 - q) + 130, 560, H + 60, alpha=0.5 * clamp(q))

    def ui(cr):
        head2(cr, t, "FROM THIS, THE BABY'S NAME:", t0 + 0.05, None, 0.0)
        name = "MANDHATA"
        col = RED if t > tM - 0.05 else INK
        a = prog(t, tN, 0.25)
        k = 1.0 + 0.12 * math.exp(-6 * max(0, t - tM)) * (t > tM)
        cr.save()
        cr.translate(540, y + 70 * (1 - q))
        cr.scale(k, k)
        draw_text(cr, name, 0, 4, 170, col, a, anchor="cm")
        cr.restore()
        tag(cr, t, tM + 0.35, "= \"HE WILL DRINK ME\"", 540, 1010, 40)
    return dict(ui=ui, flash=0.35 * math.exp(-4 * max(0, t - tM)) * (t > tM))


# ------------------------------------------------------------------ m15  the emperor: where the sun rises to where it sets


HZ = 900                             # the horizon of the world strip
WS = (0.82, 0.6)                     # the world strip's scale (wide, flattened: a far land behind the emperor)
SUN_L, SUN_R = (150, HZ - 30), (930, HZ - 30)
CITIES = ((-320, 96), (-60, 96), (250, 96), (560, 96))


def sun_clipped(cr, t, x, y, s, alpha=1.0):
    """A sun that hides below the horizon."""
    cr.save()
    cr.rectangle(-100, -100, W + 200, HZ + 6 + 100)
    cr.clip()
    prop(cr, "sun", x, y, s, rot=t * 0.25, alpha=alpha)
    cr.restore()


def s_emperor(cr, t, tl, t0, t1):
    c = cues(tl, "m15")
    tU, tD = c["U"], c["D"]
    wb, wk, wa = depth(t, t0, 0.5)
    cr.save()
    cr.translate(540, HZ)
    cr.scale(WS[0] * wk, WS[1] * wk)
    pc.paint_part(cr, "md_world", 0.8 * wa, wb + 2)
    cr.restore()
    t_c0 = t0 + 1.0
    for i, (cx, cy) in enumerate(CITIES):               # his cities light up one by one
        tc = t_c0 + (tU - 0.3 - t_c0) * i / (len(CITIES) - 1) if tU - 0.3 > t_c0 else t_c0 + 0.2 * i
        on = prog(t, tc, 0.35)
        gx, gy = 540 + cx * WS[0], HZ + (cy - 50) * WS[1]
        glow(cr, gx, gy, 130, 0.6 * on * (0.85 + 0.15 * math.sin(t * 4 + i)))
        warm(cr, gx, gy, 80, 0.7 * on)
    up = ease((t - tU) / 0.6) if t > tU - 0.1 else 0.0
    sun_clipped(cr, t, SUN_L[0], HZ + 80 - 150 * up, 0.3, alpha=clamp(up * 3))
    if t > tU:                                          # the sun's path over his whole kingdom
        p = clamp((t - tU - 0.2) / max(0.5, tD - tU - 0.2))
        pts = [(SUN_L[0] + (SUN_R[0] - SUN_L[0]) * u, SUN_L[1] - 40 - 250 * math.sin(math.pi * u))
               for u in (i / 60 for i in range(61))]
        dotted(cr, pts, p, 30, 6.5, RED, 0.85)
        if 0 < p < 1:
            j = int(p * 60)
            prop(cr, "sun", pts[j][0], pts[j][1], 0.13, rot=t)
    if t > tD - 0.1:                                    # ... and sets on the far side: it sinks half under
        down = ease((t - tD) / 1.6)
        warm(cr, SUN_R[0], HZ - 20, 200, 0.6 * clamp((t - tD + 0.1) / 0.3), (0.95, 0.35, 0.12))
        sun_clipped(cr, t, SUN_R[0], HZ - 70 + 72 * down, 0.3, alpha=clamp((t - tD + 0.1) / 0.2))
    ground(cr)
    st = 0.82
    b, k, a = depth(t, t0, 0.5)
    glow(cr, 540, FEET - 520 * st, 460, 0.5 * a)
    warm(cr, 520, FEET - 600 * st, 360, 0.35 * a)
    prop(cr, "md_throne", 540, FEET, st * k, alpha=a, blur=b)
    hip = FEET - 246 * st * k
    rise = keyed(t, [(t0, 0.0), (t0 + 0.9, 1.0)], 0.35, 1.3)
    emperor(cr, t, 520, hip, st * k, front=(-0.5 - 0.9 * rise, -0.6 + 0.2 * rise), alpha=a, blur=b,
            hits=[(t0 + 0.9, 0.5)])

    def ui(cr):
        if t < tU:
            head2(cr, t, "MANDHATA GREW UP TO BE AN", t0 + 0.05, "EMPEROR", t0 + 0.3, big_size=250, under=t0 + 1.0)
        else:
            head2(cr, t, "FROM WHERE THE SUN RISES", tU, "TO WHERE IT SETS", tD, big_size=200, under=tD + 0.4)
        tag(cr, t, tU + 0.2, "RISES", SUN_L[0], HZ + 190, 34)
        tag(cr, t, tD + 0.2, "SETS", SUN_R[0], HZ + 190, 34)
    return dict(ui=ui, flash=0.2 * math.exp(-4 * max(0, t - tU)) * (t > tU))


# ------------------------------------------------------------------ m16  yes / no


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "m16")
    tY = c["Y"]
    ground(cr)
    yuva(cr, t, 390, 0.44, front=(-0.7, -0.6), head=0.02, ph=0.3)
    baby(cr, t, 640, FEET - 20, 0.3, lotus=True, glow_a=0.5)
    p = back(clamp((t - t0) / 0.4), 1.4)
    yb = 930 + 80 * (1 - p)
    cr.save()
    cr.translate(540, yb)
    pc.paint_part(cr, "card", alpha=clamp(p))
    cr.restore()
    pc.rod(cr, 400, yb + 200, 380, H + 60, alpha=clamp(p))
    pc.rod(cr, 680, yb + 200, 700, H + 60, alpha=clamp(p))

    def ui(cr):
        a = clamp(p)
        head2(cr, t, "DID YOU KNOW", t0, "THIS STORY?", t0 + 0.12, big_size=220)
        for i, lab in enumerate(("YES", "NO")):
            bx = 540 - 175 + 350 * i
            cr.set_source_rgba(*INK, a)
            cr.set_line_width(7)
            cr.rectangle(bx - 118, yb - 38, 66, 66)
            cr.stroke()
            draw_text(cr, lab, bx - 32, yb - 5, 104, INK, a, anchor="lm")
        if t > tY:
            n = int((t - tY) / 0.9)
            side = n % 2
            red_ring(cr, 540 - 175 + 350 * side + 20, yb - 5, 145, 85, prog(t, tY + 0.9 * n, 0.35), 9)
    return dict(ui=ui)


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("m1", None, s_hook, {"z": (1.0, 1.04)}),
    ("m2", None, s_books, {"z": (1.0, 1.03)}),
    ("m3", None, s_noson, {}),
    ("m4", None, s_yajna, {}),
    ("m5", None, s_water, {"z": (1.0, 1.04)}),
    ("m6", None, s_night, {}),
    ("m7", None, s_drink, {"z": (1.02, 1.08)}),
    ("m8", None, s_empty, {}),
    ("m9", None, s_inside, {"z": (1.0, 1.06)}),
    ("m10", None, s_birth, {"z": (1.0, 1.04)}),
    ("m11", None, s_ashvins, {}),
    ("m12", None, s_hungry, {"z": (1.0, 1.08)}),
    ("m13", None, s_indra, {}),
    ("m14", None, s_name, {"z": (1.0, 1.04)}),
    ("m15", None, s_emperor, {"z": (1.0, 1.03)}),
    ("m16", None, s_end, {"z": (1.0, 1.03)}),
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
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook,
    shimmer on the blessed water, a conch on the baby inside the king, shimmer on the birth's light or on the divine
    doctors, a dip and a conch for Indra, shimmer on the name, a bell on the yes / no. Filtered here the way
    render_myth.calm_sfx filters (SFX_KEEP order, SFX_MIN_GAP apart), so the list returned is what plays (5-6 sounds
    on the voiced timelines); the bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["m5"]["P"], "shimmer", 0), (c["m9"]["P"], "conch", 0),
            (c["m10"]["O"], "shimmer", 0), (c["m11"]["V"], "shimmer", 0), (c["m13"]["I"], "conch", 0),
            (c["m14"]["M"], "shimmer", 0), (c["m16"]["Y"], "bell", 0)]
    rank = {n: i for i, n in enumerate(SFX_KEEP)}
    kept = []
    for e in sorted(want, key=lambda e: (rank[e[1]], e[0])):
        if all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["m9"]["t0"] - 0.35, "dip", 0.5), (c["m12"]["t0"] - 0.3, "dip", 0.6), (c["m13"]["I"] - 0.4, "dip", 0.4)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
