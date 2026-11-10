"""Scenes for long video 1 (videos/six_stories.py, landscape 1920x1080), builder B's parts: story 2, the sage Mandavya
who punished Yama (Mahabharata, Adi Parva 107-108), lines m1-m14, and story 5, Nachiketa at Yama's door (Katha
Upanishad 1.1-1.2), lines n1-n13. scenes_six_stories routes every moment whose active line is m* or n* here.

Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code, as in the reels: a lamp-lit cloth screen
(made here for the wide frame: the lamp sits low in the middle, a second small lamp lights the headline), translucent
punched-leather puppets on rods (six_cast_b; Yama is ruru_cast's puppet in both stories, Krishna and Arjuna come from
the Jayadratha reel), two-tier headlines (small dark setup line + one big red key line) at the top centre. Landscape
layout: the floor at FL (83% of the height), two characters facing each other on the left and right thirds, cards and
props in the free third; long-form pace: a visible change every 2-3 s. Told so a child can follow: one plain English
label per step.

Respect: Yama is a calm, dignified judge (dark blue-grey skin, gold crown, his staff and his book of deeds); the sages
and the king keep their dignity. No gore at all: the punishment is shown only as a tall pointed stake standing on its
own; the sage who survives it is a calm, glowing figure with closed eyes high above the ground behind a curtain of
light; the insect in the flashback only flinches; death in story 5 is a dotted outline that fades while the soul-light
stays bright.

Every frame is a pure function of t. Cues are words of the Hindi line (CUES, with fraction fallbacks and minimum gaps;
MISSES stays empty when every word is found).

Shot list (line: what is on the screen)
  m1  chapter card on a palm leaf: STORY 2 OF 6 / THE SAGE WHO / PUNISHED YAMA / MAHABHARATA · ADI PARVA; it flies up and
      the sage Mandavya sits meditating by his leaf hut (tag MANDAVYA): A SAGE NAMED / MANDAVYA; a VOW OF SILENCE tag with
      the silence badge (lips and a finger): HE HAD TAKEN A / VOW OF SILENCE; he raises a finger to his lips: MEANING:
      HE TALKED TO / NO ONE
  m2  two masked thieves with loot sacks run in from the left (far behind them, the king's soldiers' spears): ONE DAY,
      SOME / THIEVES, RUNNING FROM THE / KING'S SOLDIERS; they drop the sacks by the hut and run off: THE THIEVES HID
      THE LOOT / RIGHT HERE! (ringed, a red arrow, tag LOOT)
  m3  the soldiers march in; the lead one asks (cloud WHERE DID / THEY GO?): THE SOLDIERS ASKED THE SAGE:; the sage,
      eyes shut, a "..." cloud and the silence badge: BUT THE SAGE STAYED / SILENT
  m4  a soldier lifts a sack at the hut, coins spill (ringed, THE LOOT!): THE SOLDIERS FOUND / THE LOOT; both turn their
      spears toward the calm sage, a dotted red line from the loot to him: THEY THOUGHT THE SAGE WAS THE / CHIEF THIEF
  m5  the palace: the king points; the sage stands calm between soldiers; on the right a tall pointed stake rises
      (an object only): THE KING GAVE HIS / ORDER; card PUNISHMENT: / THE STAKE
  m6  dark; a curtain of light, and high above the ground behind it the sage sits glowing, eyes closed: BUT THE SAGE /
      DID NOT DIE; HIS TAPAS (PRAYER POWER) KEPT HIM / ALIVE
  m7  light returns; the king walks in and kneels at the sage's feet (cloud SORRY! / FORGIVE ME): THE KING LEARNED THE /
      TRUTH, HE FELL AT THE SAGE'S FEET: / SORRY!, AND THE SAGE WAS / FREED
  m8  Yama's hall: the sage walks in; Yama (tag YAMA) with his staff and his book of deeds: THEN THE SAGE WENT STRAIGHT TO
      / YAMA; the book opens on its stand: SINS / GOOD DEEDS with tally marks: YAMA = DHARMARAJA, / KEEPER OF SINS
  m9  the sage asks, palm up: THE SAGE ASKED YAMA: / WHAT WAS MY SIN?; cloud WHY THIS / PUNISHMENT?
  m10 Yama points at the open book; a sepia flashback card grows out of it: a small child kneels and pokes an insect with
      a blade of grass (tags AN INSECT, A BLADE OF GRASS; the insect flinches): YAMA SAID: / AS A CHILD...
  m11 a balance: A CHILD'S MISTAKE (a tiny insect) against THE PUNISHMENT (the stake) crashing down; the sage angry, a
      raised fist: A CHILD'S MISTAKE... / SUCH A BIG PUNISHMENT?, THE SAGE SAID: / UNFAIR!
  m12 the sage raises his hand; a big rule card: NEW RULE / UNDER 14 = NO SIN (14 big and red), a small child beside it;
      Yama nods: THAT DAY THE SAGE MADE A / NEW RULE
  m13 the sage points; a line of gold light to Yama, who bows; a dotted arrow down to a small human on the earth (EARTH):
      THEN THE SAGE CURSED YAMA: / BE BORN AS A HUMAN
  m14 Yama glows and dissolves into light; the hall fades into a palace and Vidura stands there, calm (tag VIDURA, plate
      THE WISEST MAN OF THE MAHABHARATA): AND YAMA WAS BORN... / YAMA WAS BORN AS / VIDURA
  n1  chapter card: STORY 5 OF 6 / THE CHILD WHO ASKED YAMA / THE SECRET OF DEATH / KATHA UPANISHAD; then a yajna fire,
      the father (tag VAJASHRAVAS, THE FATHER) giving away thin old cows: A FATHER WAS GIVING AWAY / GIFTS, BUT HIS GIFTS
      WERE / OLD, WEAK COWS (a ring on the ribs)
  n2  his son comes in (tag NACHIKETA): HIS SON / NACHIKETA; he frowns at the cows (cloud THAT'S NOT RIGHT...); he turns
      to his father, a hand on his chest: FATHER, TO WHOM / WILL YOU GIVE ME?
  n3  the father silent ("..."): THE FATHER STAYED / SILENT; the boy asks again: TO WHOM? x2, x3
  n4  the father, angry, points to the far right where a dark shadow of Yama appears; the boy recoils: cloud GO! / I GIVE
      YOU TO YAMA!: THE FATHER SHOUTED IN ANGER: / TO YAMA!
  n5  the boy walks along a dotted road into the dark toward a great door (tag YAMA'S DOOR): AND NACHIKETA REALLY WENT TO
      / YAMA'S HOUSE
  n6  the boy sits by the closed door: BUT YAMA WAS / NOT HOME; a sun and a moon cross the sky, DAY 1, DAY 2, DAY 3; an
      empty bowl and cup crossed out: 3 DAYS AT THE DOOR... / NO FOOD, NO WATER
  n7  Yama walks back, sees the boy and bows, a hand on his chest: YAMA CAME BACK AND FELT / ASHAMED (cloud A GUEST,
      HUNGRY / FOR 3 DAYS!); he raises his hand, three glowing boons: YAMA SAID: / 3 DAYS = 3 BOONS
  n8  two boon cards: BOON 1 / FATHER'S ANGER / CALMED, BOON 2 / THE FIRE THAT / LEADS TO HEAVEN, each ticked as Yama nods
  n9  the big third card (a big swinging ?, the body outline and the soul-light): AND THE THIRD BOON: / WHAT HAPPENS
      AFTER DEATH?
  n10 Yama raises a hand (cloud DON'T ASK / THIS!): YAMA TRIED TO / AVOID IT; gifts slide in one by one, labelled: GOLD,
      HORSES, ELEPHANTS, LAND, 100 YEARS: YAMA SAID: / TAKE THESE INSTEAD
  n11 the boy pushes the gifts away; they grey out and slide back: NACHIKETA SAID: / ALL THIS WILL END ONE DAY; a drum
      (dance and song) slides past too: KEEP THEM. / I WANT THE ANSWER.
  n12 Yama, pleased, teaches; a dotted body outline with a glowing soul-light (BODY, SOUL): THE SOUL IS / NEVER BORN,
      NEVER DIES; the outline fades away, the light rises and stays bright: THE BODY DIES, / THE SOUL DOES NOT
  n13 DOES THIS SOUND / FAMILIAR?; a small chariot with Krishna and Arjuna (tag KRISHNA AND ARJUNA); two palm leaves:
      KATHA UPANISHAD 1.2.18 and BHAGAVAD GITA 2.20, each न जायते म्रियते वा (ringed, =): CENTURIES LATER, KRISHNA SAID /
      ALMOST THE SAME WORDS
"""
import functools
import math

import cairo
import numpy as np
from scipy.ndimage import gaussian_filter

import puppet_core as pc
import ruru_cast as RU
import six_cast_b as SB
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, text_size, tick
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_arjuna import HAS_INDIC, card2, cloud_text, indic_surface
from scenes_jarasandha import FADE, INK, RED, bob_rot, fit, glow, man_angles, motes, red_ring, sound_rings, walk_legs
from scenes_jarasandha import head2 as _head2
from scenes_jayadratha import chariot, flash_at, silhouette, soldier, tag, tint
from scenes_kaikeyi import ANJALI, balance, pan_xy
from scenes_lakshman_rekha import big_q, big_x, sparkle
from scenes_mandhata import aura, burst, held, lights, local, mix, warm, yajna_fire
from scenes_ravana import dotted
from scenes_ruru import held_grip, nods, plate
from shots import T

MISSES = set()                       # cue words not found in a line (falls back to fractions)
FL = 892                             # the floor: where the puppets' feet stand (83% of the height)
HY = 46                              # headline: top of the small line
LAMP = (960.0, 1000.0)               # the oil lamp behind the cloth (wide frame)
GREEN_TICK = (0.16, 0.50, 0.24)
SOUL = (1.0, 0.94, 0.72)
HEART = dict(front=(-0.3, -2.45), backa=(0.12, -0.25))          # a hand on the heart
PUSH = dict(front=(-1.62, -0.05), backa=(0.25, -0.3))           # a palm pushed out: "keep them"
KID_HEAD = 1.32                      # the boys' heads are drawn bigger (they are children)


# ------------------------------------------------------------------ cues


def cue(tl, bid, word, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, word)
    except (KeyError, ValueError):
        MISSES.add((bid, word))
        return T(tl, bid, frac)


# Every cue of every line: (name, Hindi word, fraction fallback, ((after, min gap), ...)); "t0" = the line's start.
# Words are exact substrings of the script lines (checked: MISSES stays empty).
CUES = {
    "m1": (("R", "ऋषि", 0.17, (("t0", 0.6),)),
           ("N", "मांडव्य", 0.27, (("R", 0.3),)),
           ("V", "मौन", 0.42, (("N", 0.6),)),
           ("B", "बात", 0.8, (("V", 1.0),))),
    "m2": (("C", "चोर", 0.15, (("t0", 0.3),)),
           ("S", "सिपाहियों", 0.3, (("C", 0.5),)),
           ("R", "भागते", 0.45, (("S", 0.4),)),
           ("A", "आश्रम", 0.62, (("R", 0.6),)),
           ("M", "माल", 0.8, (("A", 0.5),)),
           ("H", "छिपा", 0.88, (("M", 0.3),))),
    "m3": (("P", "पूछा", 0.25, (("t0", 0.6),)),
           ("Q", "कहाँ", 0.38, (("P", 0.3),)),
           ("M", "मौन", 0.62, (("Q", 1.0),)),
           ("N", "कुछ", 0.8, (("M", 0.6),))),
    "m4": (("M", "माल", 0.15, (("t0", 0.4),)),
           ("F", "मिल", 0.4, (("M", 0.6),)),
           ("L", "लगा", 0.55, (("F", 0.6),)),
           ("C", "सरदार", 0.85, (("L", 0.8),))),
    "m5": (("Z", "सज़ा", 0.25, (("t0", 0.5),)),
           ("S", "शूली", 0.65, (("Z", 0.8),))),
    "m6": (("D", "मरे", 0.12, (("t0", 0.3),)),
           ("T", "तप", 0.35, (("D", 1.0),)),
           ("Z", "ज़िंदा", 0.8, (("T", 0.8),))),
    "m7": (("S", "सच", 0.12, (("t0", 0.3),)),
           ("P", "पैर", 0.4, (("S", 0.9),)),
           ("M", "माफ़ी", 0.55, (("P", 0.5),)),
           ("U", "उतरवा", 0.85, (("M", 0.9),))),
    "m8": (("Y", "यमराज", 0.15, (("t0", 0.5),)),
           ("D", "धर्मराज", 0.5, (("Y", 1.2),)),
           ("P", "पाप", 0.7, (("D", 0.6),)),
           ("H", "हिसाब", 0.88, (("P", 0.6),))),
    "m9": (("P", "पूछा", 0.15, (("t0", 0.3),)),
           ("K", "कौन", 0.35, (("P", 0.4),)),
           ("S", "सज़ा", 0.85, (("K", 0.9),))),
    "m10": (("B", "बचपन", 0.15, (("t0", 0.4),)),
            ("K", "कीड़े", 0.45, (("B", 0.9),)),
            ("G", "घास", 0.65, (("K", 0.6),)),
            ("C", "चुभोया", 0.88, (("G", 0.5),))),
    "m11": (("N", "नादानी", 0.3, (("t0", 0.5),)),
            ("S", "सज़ा", 0.6, (("N", 0.7),)),
            ("A", "अन्याय", 0.85, (("S", 0.6),))),
    "m12": (("R", "नियम", 0.25, (("t0", 0.5),)),
            ("F", "चौदह", 0.42, (("R", 0.6),)),
            ("B", "बच्चा", 0.6, (("F", 0.5),)),
            ("P", "पाप", 0.8, (("B", 0.5),))),
    "m13": (("S", "श्राप", 0.3, (("t0", 0.6),)),
            ("I", "इंसान", 0.55, (("S", 0.5),)),
            ("D", "धरती", 0.75, (("I", 0.5),))),
    "m14": (("J", "जन्म", 0.2, (("t0", 0.4),)),
            ("M", "महाभारत", 0.4, (("J", 1.0),)),
            ("S", "समझदार", 0.62, (("M", 0.5),)),
            ("V", "विदुर", 0.85, (("S", 0.5),))),
    "n1": (("K", "कठ", 0.12, (("t0", 0.4),)),
           ("F", "पिता", 0.3, (("K", 0.6),)),
           ("D", "दान", 0.38, (("F", 0.4),)),
           ("O", "बूढ़ी", 0.8, (("D", 0.9),)),
           ("C", "गायें", 0.95, (("O", 0.4),))),
    "n2": (("N", "नचिकेता", 0.15, (("t0", 0.3),)),
           ("G", "ग़लत", 0.35, (("N", 0.6),)),
           ("P", "पूछा", 0.5, (("G", 0.6),)),
           ("M", "मुझे", 0.72, (("P", 0.6),))),
    "n3": (("C", "चुप", 0.1, (("t0", 0.2),)),
           ("D", "दूसरी", 0.4, (("C", 0.8),)),
           ("T", "तीसरी", 0.8, (("D", 0.9),))),
    "n4": (("A", "ग़ुस्से", 0.1, (("t0", 0.2),)),
           ("J", "जा,", 0.4, (("A", 0.5),)),
           ("Y", "यमराज", 0.7, (("J", 0.5),))),
    "n5": (("N", "नचिकेता", 0.1, (("t0", 0.2),)),
           ("Y", "यमराज", 0.5, (("N", 0.6),)),
           ("G", "चला", 0.8, (("Y", 0.5),))),
    "n6": (("N", "नहीं", 0.18, (("t0", 0.4),)),
           ("T", "तीन", 0.4, (("N", 0.6),)),
           ("B", "बिना", 0.55, (("T", 0.5),)),
           ("D", "दरवाज़े", 0.8, (("B", 0.8),))),
    "n7": (("L", "लौटे", 0.08, (("t0", 0.2),)),
           ("S", "शर्मिंदा", 0.2, (("L", 0.5),)),
           ("G", "मेहमान", 0.35, (("S", 0.6),)),
           ("B", "बदले", 0.72, (("G", 1.0),)),
           ("V", "वरदान", 0.85, (("B", 0.4),))),
    "n8": (("C", "शांत", 0.35, (("t0", 0.8),)),
           ("T", "दूसरा", 0.55, (("C", 0.5),)),
           ("A", "अग्नि", 0.85, (("T", 0.8),))),
    "n9": (("T", "तीसरा", 0.08, (("t0", 0.2),)),
           ("M", "मरने", 0.4, (("T", 0.5),)),
           ("Q", "क्या", 0.8, (("M", 0.5),))),
    "n10": (("T", "टालना", 0.1, (("t0", 0.2),)),
            ("M", "मत", 0.28, (("T", 0.5),)),
            ("B", "बदले", 0.42, (("M", 0.6),)),
            ("G", "सोना", 0.52, (("B", 0.3),)),
            ("H", "घोड़े", 0.62, (("G", 0.45),)),
            ("E", "हाथी", 0.7, (("H", 0.45),)),
            ("L", "ज़मीन", 0.78, (("E", 0.45),)),
            ("Y", "सौ", 0.87, (("L", 0.45),))),
    "n11": (("E", "ख़त्म", 0.3, (("t0", 0.8),)),
            ("D", "नाच", 0.58, (("E", 0.8),)),
            ("K", "रखिए", 0.72, (("D", 0.5),)),
            ("J", "जवाब", 0.9, (("K", 0.6),))),
    "n12": (("K", "ख़ुश", 0.1, (("t0", 0.2),)),
            ("A", "आत्मा", 0.32, (("K", 0.6),)),
            ("N", "मरती", 0.55, (("A", 0.6),)),
            ("S", "शरीर", 0.7, (("N", 0.5),)),
            ("X", "नहीं", 0.95, (("S", 0.6),))),
    "n13": (("Q", "लगी", 0.2, (("t0", 0.4),)),
            ("C", "सदियों", 0.3, (("Q", 0.4),)),
            ("K", "कृष्ण", 0.42, (("C", 0.4),)),
            ("G", "गीता", 0.55, (("K", 0.4),)),
            ("W", "लगभग", 0.78, (("G", 0.8),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_s6b_cues", None)
    if cache is None:
        cache = {}
        tl._s6b_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, word, frac, cons in CUES[bid]:
            v = cue(tl, bid, word, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


# ------------------------------------------------------------------ the wide screen


@functools.lru_cache(maxsize=1)
def stage_surface():
    """puppet_core.screen_surface's backlit cloth, laid out for the wide frame: the oil lamp low in the middle, a second
    small lamp lighting the headline, two stitched panel seams, gentle creases and a few oil stains."""
    rng = np.random.default_rng(1729)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    dx = (xx - LAMP[0]) / 1150.0
    dy = (yy - LAMP[1]) / 1250.0
    d2 = dx * dx + dy * dy
    L = np.exp(-1.55 * d2 ** 1.15)
    hx, hy = (xx - 960) / 900.0, (yy - 150) / 330.0
    L = L + 0.30 * np.exp(-(hx * hx + hy * hy) ** 1.1) * (1 - 0.6 * L)
    L *= 1 + 0.025 * pc._smooth_noise(rng, (H // 8 + 1, W // 8 + 1), 9).repeat(8, 0).repeat(8, 1)[:H, :W]
    fib = pc._smooth_noise(rng, (H, W), 0.8) * 0.010
    slub = gaussian_filter(rng.normal(0, 1, (H, W // 16 + 1)).astype(np.float32), (0.6, 2.0)).repeat(16, 1)[:, :W]
    slub = slub / (slub.std() + 1e-6) * 0.012
    tex = 1 + fib + slub
    for sx in (330.0, 1590.0):
        d = xx - sx - 6 * np.sin(yy / 260.0)
        tex *= 1 - 0.07 * np.exp(-(d / 2.2) ** 2)
        tex *= 1 + 0.03 * np.exp(-((d - 5) / 5.0) ** 2)
        st = (np.abs(d) < 2.5) & ((yy.astype(np.int32) // 9) % 2 == 0)
        tex *= np.where(st, 0.93, 1.0)
    for (x0, y0, ang, wdt, k) in ((560, 340, 1.35, 30, 0.03), (1400, 760, 1.75, 40, 0.03), (980, 160, 1.5, 24, 0.02)):
        nx, ny = math.cos(ang), math.sin(ang)
        d = (xx - x0) * ny - (yy - y0) * nx
        along = np.exp(-(((xx - x0) * nx + (yy - y0) * ny) / 700.0) ** 2)
        tex *= 1 - k * along * np.exp(-(d / wdt) ** 2) + 0.6 * k * along * np.exp(-((d - wdt) / wdt) ** 2)
    stain = np.zeros((H, W), np.float32)
    for (sx, sy, r, k) in ((150, 930, 120, 0.10), (1760, 230, 90, 0.07), (1660, 990, 70, 0.08), (90, 420, 60, 0.05)):
        stain += k * np.exp(-(((xx - sx) ** 2 + (yy - sy) ** 2) / (r * r)) ** 1.5)
    stops = np.array([0.0, 0.2, 0.4, 0.6, 0.8, 1.0])
    cols = np.array([(0.03, 0.012, 0.006), (0.24, 0.10, 0.04), (0.62, 0.36, 0.15), (0.90, 0.68, 0.40),
                     (0.98, 0.88, 0.66), (1.0, 0.96, 0.84)])
    Lc = np.clip(L, 0, 1.05)
    img = np.stack([np.interp(Lc, stops, cols[:, c]) for c in range(3)], -1).astype(np.float32)
    img *= tex[..., None]
    img *= (1 - stain[..., None] * np.array([0.45, 0.65, 0.95], np.float32))
    a = np.concatenate([np.clip(img, 0, 1), np.ones((H, W, 1), np.float32)], -1)
    return pc.surface_from_rgba(a)


def stage(cr):
    cr.set_source_surface(stage_surface(), 0, 0)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.paint()


def lamp(cr, t, night=0.0, flash=0.0):
    """puppet_core.lamp for the wide frame: flicker, a drifting warm hot spot, a night tint, a flash of lamp light."""
    f = pc.flicker(t)
    lx = LAMP[0] + 20 * math.sin(t * 1.3) + 8 * math.sin(t * 3.1)
    ly = LAMP[1] - 60 + 10 * math.sin(t * 0.9 + 1)
    hs, n = pc._hotspot()
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.translate(lx, ly)
    cr.scale(1400 / n, 1000 / n)
    cr.set_source_surface(hs, -n, -n)
    cr.get_source().set_filter(cairo.FILTER_BILINEAR)
    cr.paint_with_alpha(clamp(0.10 + 0.05 * f))
    cr.restore()
    if night > 0:
        cr.save()
        cr.set_operator(cairo.OPERATOR_MULTIPLY)
        cr.set_source_rgba(0.40, 0.48, 0.78, clamp(night))
        cr.paint()
        cr.restore()
    dark = 0.05 + 0.035 * f
    if dark > 0:
        cr.set_source_rgba(0.02, 0.01, 0.0, clamp(dark))
        cr.paint()
    if flash > 0:
        cr.save()
        cr.set_operator(cairo.OPERATOR_ADD)
        cr.translate(960, 760)
        cr.scale(2300 / n, 1500 / n)
        cr.set_source_surface(hs, -n, -n)
        cr.get_source().set_filter(cairo.FILTER_BILINEAR)
        cr.paint_with_alpha(clamp(flash) * 0.5)
        cr.restore()


def title_lift(cr, a):
    """In the dark shots the small lamp over the headline stays lit, so the words read."""
    if a <= 0.01:
        return
    cr.save()
    cr.translate(960, 150)
    cr.scale(1.0, 0.24)
    g = cairo.RadialGradient(0, 0, 60, 0, 0, 1050)
    g.add_color_stop_rgba(0, 1.0, 0.93, 0.76, 0.55 * a)
    g.add_color_stop_rgba(0.6, 1.0, 0.90, 0.70, 0.3 * a)
    g.add_color_stop_rgba(1, 1.0, 0.88, 0.66, 0.0)
    cr.set_source(g)
    cr.paint()
    cr.restore()


def ground(cr, alpha=1.0, y=FL + 6, blur=0.0):
    prop(cr, "ground", W / 2, y, 1.42, alpha=alpha, blur=blur)


def head2(cr, t, small, t_small, big, t_big, big_size=118, small_size=56, y=HY, **kw):
    """scenes_jarasandha.head2 at the top centre of the wide frame: the big line fits 1460 px (1740 px at its pop-in
    overshoot, inside the 90 px margins), the small line 1600 px."""
    if big:
        big_size = min(big_size, fit(big, big_size, 1460))
    if small:
        sw = sum(text_size(wd, small_size)[0] for wd in small.split()) + small_size * 0.34 * (len(small.split()) - 1)
        if sw > 1600:
            small_size = int(small_size * 1600 / sw)
    return _head2(cr, t, small, t_small, big, t_big, y=y, small_size=small_size, big_size=big_size, **kw)


def seg_line(cr, parts, x, y, size, font=HEAD_FONT, alpha=1.0, tracking=0, gap=None):
    """A centred line of coloured pieces [(text, colour)]."""
    ws = [text_size(p, size, font, tracking)[0] for p, _ in parts]
    gap = size * 0.3 if gap is None else gap
    xx = x - (sum(ws) + gap * (len(parts) - 1)) / 2
    for (p, col), w in zip(parts, ws):
        draw_text(cr, p, xx, y, size, col, alpha, font, "lm", tracking)
        xx += w + gap


def to_user(cr, p):
    return cr.device_to_user(*p)


# ------------------------------------------------------------------ the chapter card


def chapter(cr, t, t_in, t_out, story, lines, source):
    """The palm-leaf chapter card: STORY n OF 6, the English title (lines of [(text, colour)]), the source tag. It
    rises in at t_in and flies up and away at t_out."""
    a_in = prog(t, t_in, 0.45)
    out = ease((t - t_out) / 0.5) if t > t_out else 0.0
    a = a_in * (1 - out)
    if a <= 0.01:
        return
    b, k, _ = depth(t, t_in - 0.1, 0.5)
    y = 560 + 120 * (1 - ease((t - t_in) / 0.5)) - 760 * out * out
    s = 1.42 * k
    r = sway(t, 0.006, 0.35) - 0.05 * out
    glow(cr, 960, y, 760, 0.35 * a)
    for sx in (-1, 1):
        pc.rod(cr, 960 + sx * 420 * s, y + 160 * s, 960 + sx * 330, H + 60, alpha=0.5 * a)
    cr.save()
    cr.translate(960, y)
    cr.rotate(r)
    cr.scale(s, s)
    pc.paint_part(cr, "lr_bigleaf", a, b)
    p1, p2, p3 = prog(t, t_in + 0.2, 0.3), prog(t, t_in + 0.45, 0.35), prog(t, t_in + 0.8, 0.3)
    draw_text(cr, story, 0, -138, 40, RED, a * p1, MONO_FONT, "cm", tracking=8)
    cr.set_source_rgba(*INK, 0.6 * a * p1)
    cr.set_line_width(2.5)
    cr.move_to(-300 * p1, -104)
    cr.line_to(300 * p1, -104)
    cr.stroke()
    n = len(lines)
    size = 86 if n <= 2 else 70
    for i, parts in enumerate(lines):
        yy = -10 + (i - (n - 1) / 2) * size * 1.08 + 20
        full = sum(text_size(p, size)[0] for p, _ in parts) + size * 0.3 * (len(parts) - 1)
        sz = min(size, int(size * 820 / max(1, full)))
        cr.save()
        cr.translate(0, yy + 10 * (1 - p2))
        seg_line(cr, parts, 0, 0, sz, HEAD_FONT, a * p2)
        cr.restore()
    w_, h_ = text_size(source, 30, MONO_FONT, 4)
    cr.set_source_rgba(0.62, 0.12, 0.08, 0.92 * a * p3)
    cr.rectangle(-w_ / 2 - 26, 158 - h_ / 2 - 14, w_ + 52, h_ + 28)
    cr.set_line_width(3)
    cr.stroke()
    draw_text(cr, source, 0, 158, 30, (0.62, 0.12, 0.08), a * p3, MONO_FONT, "cm", tracking=4)
    cr.restore()


# ------------------------------------------------------------------ puppets


def ik(sh, tgt, a=150.0, b=160.0):
    """(upper, fore) angles (man_angles convention: 0 hangs down, -pi/2 points forward) for a two-link arm from the
    shoulder sh so the point b along the forearm lands on tgt (root units, facing right); the elbow below the line."""
    dx, dy = tgt[0] - sh[0], tgt[1] - sh[1]
    d = max(abs(a - b) + 1e-3, min(math.hypot(dx, dy), a + b - 1e-3))
    base = math.atan2(-dx, dy)
    ang_a = math.acos(clamp((a * a + d * d - b * b) / (2 * a * d), -1, 1))
    ang_e = math.acos(clamp((a * a + b * b - d * d) / (2 * a * b), -1, 1))
    return base + ang_a, -(math.pi - ang_e)


def body(cr, rig, key, t, x, s, front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0), hits=(),
         flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, feet=FL, ph=0.0, extra=None, swap=None, kneel=None,
         sit=None, y=None, scales=None, hop=0.0):
    """A man() puppet standing (hip at feet - 434 s), kneeling (kneel = the kneeling-legs sprite) or sitting
    cross-legged (sit = (seat sprite, body-without-pleats sprite)). Returns its points (device)."""
    ang = man_angles(key, t, front, backa, head, legs, hits, ph)
    hide = ()
    sw = dict(swap or {})
    ex = dict(extra or {})
    r = rot + bob_rot(t, ph, 0.008 if (sit or kneel) else 0.012)
    if kneel:
        hy = feet - 250 * s if y is None else y
        prop(cr, kneel, x, hy, s, r, alpha, blur, flip)
        hide = (key + "_legF", key + "_legB")
    elif sit:
        seat, body_sit = sit
        hy = feet - SB.SEAT_H * s - hop if y is None else y
        sw[key + "_body"] = body_sit
        hide = (key + "_legF", key + "_legB")
        prev = ex.get(key + "_body")

        def seat_fn(c, prev=prev):
            pc.paint_part(c, seat, alpha, blur)
            if prev:
                prev(c)
        ex[key + "_body"] = seat_fn
    else:
        hy = feet - 434 * s if y is None else y
    return puppet(cr, rig, x, hy, s, r, flip, ang, alpha, blur, hide=hide, swap=sw or None, rods=rods,
                  extra=ex or None, scales=scales)


HUSH_TGT = (96.0, -362.0)            # Mandavya's hush: where the middle of the raised finger goes (hip units)
LAP = (-0.5, -1.15)                  # a hand resting on the lap (back arm, seated)


def mand(cr, t, x, s, mood="calm", sit=False, hush=0.0, front=(-0.32, -0.55), backa=(0.3, -0.25), **kw):
    """Mandavya (mood calm | sleep | angry | teach); sit = cross-legged; hush 0..1 raises his finger to his lips (the
    other hand goes down to his lap)."""
    swap = {"sb_mand_head": "sb_mand_head" + ("" if mood == "calm" else "_" + mood)}
    if hush > 0:
        front = mix(front, ik((26 * 0.92, -262), HUSH_TGT, 150, 186), ease(hush))
        backa = mix(backa, LAP, ease(hush))
        if hush > 0.45:
            swap["sb_mand_armF_lo"] = "sb_mand_armF_lo_hush"
    return body(cr, SB.MAND, "sb_mand", t, x, s, front=front, backa=backa, swap=swap,
                sit=("sb_mand_seat", "sb_mand_body_sit") if sit else None, **kw)


def thief(cr, t, x, s, sack=True, **kw):
    """A masked thief; sack = a loot sack slung over his back shoulder (drawn behind him)."""
    flip = kw.get("flip", False)
    a, b = kw.get("alpha", 1.0), kw.get("blur", 0.0)
    if sack:
        hy = kw.get("y", FL - 434 * s)
        sx, sy = local(x, hy, s, kw.get("rot", 0.0), flip, -70, -150)
        prop(cr, "sb_sack", sx, sy, 0.62 * s, rot=-0.35 * (-1 if flip else 1) + kw.get("rot", 0.0), alpha=a, blur=b,
             flip=flip)
    kw.setdefault("backa", (-2.5, -0.9))
    return body(cr, SB.THIEF, "sb_thief", t, x, s, **kw)


def king(cr, t, x, s, mood="calm", **kw):
    swap = {"sb_king_head": "sb_king_head" + ("" if mood == "calm" else "_" + mood)}
    return body(cr, SB.KING, "sb_king", t, x, s, swap=swap, **kw)


def yama(cr, t, x, s, mood="calm", nod=0.0, front=(-0.95, -1.15), backa=(0.3, -0.3), head=0.0, book=True, staff=True,
         **kw):
    """Yama Dharmaraja (ruru_cast's puppet): his danda upright in the back hand, the book of deeds held at his chest in
    the front hand; mood calm | smile | shame | teach; nod 0..1 bows his head."""
    a, b = kw.get("alpha", 1.0), kw.get("blur", 0.0)
    swap = {"rr_yama_head": "rr_yama_head" if mood == "calm" else "sb_yama_head_" + mood}
    ex = {}
    if staff:
        ex["rr_yama_armB_lo"] = held_grip("rr_danda", backa, 0.68, 0.0, 120, a, b)
    if book:
        ex["rr_yama_armF_lo"] = held("sb_ledger", front, 0.5, dy=150, tilt=0.12, alpha=a, blur=b)
    return body(cr, RU.YAMA, "rr_yama", t, x, s, front=front, backa=backa, head=head + 0.2 * nod, extra=ex, swap=swap,
                **kw)


def vidura(cr, t, x, s, mood="calm", **kw):
    swap = {"sb_vidura_head": "sb_vidura_head" + ("" if mood == "calm" else "_" + mood)}
    return body(cr, SB.VIDURA, "sb_vidura", t, x, s, swap=swap, **kw)


def nachi(cr, t, x, s, mood="calm", sit=False, **kw):
    """Nachiketa (mood calm | smile | shock | shame), his head drawn bigger (a boy)."""
    swap = {"sb_nachi_head": "sb_nachi_head" + ("" if mood == "calm" else "_" + mood)}
    return body(cr, SB.NACHI, "sb_nachi", t, x, s, swap=swap, scales={"sb_nachi_head": KID_HEAD},
                sit=("sb_nachi_seat", "sb_nachi_body_sit") if sit else None, **kw)


def vaja(cr, t, x, s, mood="calm", **kw):
    swap = {"sb_vaja_head": "sb_vaja_head" + ("" if mood == "calm" else "_" + mood)}
    return body(cr, SB.VAJA, "sb_vaja", t, x, s, swap=swap, **kw)


def walking(fn, cr, t, t0, t1, x0, x1, s, step=0.42, t_in=None, lean=0.0, stride=0.32, **kw):
    """A puppet (fn = mand / king / nachi ...) walking in jerky rod-puppet steps, brought onto the cloth at t_in."""
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, kw.pop("alpha", 1.0))
    kw.setdefault("hits", [(t1, 1.0)])
    flip = kw.get("flip", False)
    y = FL - 434 * s + bob - (k - 1) * 300 * s
    pts = fn(cr, t, x, s * k, legs=walk_legs(ph, stride), rot=rock + lean * (-1 if flip else 1), alpha=a,
             blur=b + kw.pop("blur", 0.0), y=y, **kw)
    return pts, x


# ------------------------------------------------------------------ sets and small things


def trees(cr, t, a=1.0, xs=((120, 0.5, 9, True), (1830, 0.46, 11, False))):
    if a <= 0.01:
        return
    for i, (x, s, b, fl) in enumerate(xs):
        prop(cr, "tree", x, FL + 20, s, rot=sway(t, 0.006, 0.3, i), alpha=0.55 * a, blur=b, flip=fl)


def hut(cr, t, x=1590, s=0.66, alpha=1.0, blur=0.0):
    prop(cr, "lr_hut", x, FL + 6, s, rot=sway(t, 0.002, 0.3), alpha=alpha, blur=blur)


def hall(cr, t, a=1.0):
    """Yama's hall behind the puppets (soft, a little out of focus)."""
    prop(cr, "sb_yhall", 960, FL + 8, 0.6, alpha=0.62 * a, blur=5)


def palace(cr, t, a=1.0):
    prop(cr, "lr_palace", 960, FL + 8, 0.62, alpha=0.6 * a, blur=5)


def sack_at(cr, t, x, s=0.34, alpha=1.0, rot=0.0):
    if s > 0.005 and alpha > 0.01:
        prop(cr, "sb_sack", x, FL + 4, s, rot=rot, alpha=alpha)


def silence_badge(cr, t, t_in, x, y, s=0.62, alpha=1.0, t_out=None):
    """The silence badge (lips with a finger across them) popping in on its rod."""
    q = back(clamp((t - t_in) / 0.35), 1.6)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.25)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    pc.rod(cr, x, y + 120 * s, x + 30, H + 60, alpha=0.5 * a)
    prop(cr, "sb_hush", x, y, s * (0.6 + 0.4 * q), rot=sway(t, 0.02, 0.5, x), alpha=a)


def dots_cloud(cr, t, t_in, x, y, s=0.5, flip=False, alpha=1.0):
    """A speech cloud with only "..." in it (he says nothing)."""
    cloud_text(cr, t, x, y, s, [("...", 150, INK, -40, t_in + 0.05)], flip=flip, alpha=alpha, t_in=t_in)


def red_arrow(cr, pts, p, alpha=1.0, w=9.0):
    """A red brush arrow along pts (screen coordinates), drawn to fraction p."""
    if p <= 0:
        return
    from poster import path as _path
    _path(cr, pts, p, w, RED, 0.92 * alpha, arrow=True)


def counter_badge(cr, t, t_in, text, x, y, size=120, color=RED, alpha=1.0):
    """A number on a small leather plaque that thumps in (and kicks when it changes)."""
    q = back(clamp((t - t_in) / 0.3), 2.0)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    w, h = text_size(text, size)
    cr.save()
    cr.translate(x, y)
    cr.rotate(-0.06 + sway(t, 0.01, 0.5, x))
    cr.scale(0.7 + 0.3 * q, 0.7 + 0.3 * q)
    pc.poly(cr, [(-w / 2 - 30, -h / 2 - 20), (w / 2 + 30, -h / 2 - 20), (w / 2 + 40, 0), (w / 2 + 30, h / 2 + 20),
                 (-w / 2 - 30, h / 2 + 20), (-w / 2 - 40, 0)])
    cr.set_source_rgba(0.97, 0.87, 0.62, 0.96 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(4)
    cr.stroke()
    draw_text(cr, text, 0, 2, size, color, a, anchor="cm")
    cr.restore()


def flashback(cr, t, t_in, src, dst, wh, content, alpha=1.0, caption="LONG AGO..."):
    """A sepia flashback card growing out of src to dst (w, h = wh); content(cr, w, h) draws inside it (card units:
    origin at the card's centre)."""
    q = ease((t - t_in) / 0.7)
    if q <= 0 or alpha <= 0.01:
        return
    w, h = wh
    x = src[0] + (dst[0] - src[0]) * q
    y = src[1] + (dst[1] - src[1]) * q - 60 * math.sin(math.pi * q)
    k = 0.08 + 0.92 * q
    a = clamp(q * 2) * alpha
    cr.save()
    cr.translate(x, y)
    cr.rotate(-0.02 * (1 - q) + sway(t, 0.004, 0.3))
    cr.scale(k, k)
    cr.set_source_rgba(0, 0, 0, 0.3 * a)
    cr.rectangle(-w / 2 + 12, -h / 2 + 18, w, h)
    cr.fill()
    cr.push_group()
    cr.rectangle(-w / 2, -h / 2, w, h)
    cr.clip()
    cr.set_source_rgb(0.97, 0.88, 0.68)
    cr.paint()
    g = cairo.RadialGradient(0, 0, 0.2 * w, 0, 0, 0.75 * w)
    g.add_color_stop_rgba(0, 1, 0.97, 0.88, 0.0)
    g.add_color_stop_rgba(1, 0.45, 0.28, 0.12, 0.5)
    cr.set_source(g)
    cr.paint()
    content(cr, w, h)
    cr.set_operator(cairo.OPERATOR_HSL_SATURATION)
    cr.set_source_rgba(0.5, 0.5, 0.5, 0.6)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(1.0, 0.88, 0.68, 0.55)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.set_source_rgba(0.30, 0.17, 0.07, a)
    cr.set_line_width(12)
    cr.rectangle(-w / 2, -h / 2, w, h)
    cr.stroke()
    cr.set_line_width(3)
    cr.rectangle(-w / 2 + 16, -h / 2 + 16, w - 32, h - 32)
    cr.stroke()
    if caption:
        draw_text(cr, caption, -w / 2 + 34, -h / 2 + 34, 30, (0.30, 0.17, 0.07), a, MONO_FONT, tracking=4)
    cr.restore()


def body_outline(cr, x, feet, hgt, p=1.0, alpha=1.0, crumble=0.0, t=0.0):
    """A standing body drawn only as a dotted outline (the body in Yama's teaching); crumble 0..1: the dots fall and
    fade."""
    if alpha <= 0.01:
        return
    s = hgt / 1000.0
    head_c = (x, feet - 900 * s)
    pts = [(x - 40 * s, feet - 790 * s), (x - 150 * s, feet - 740 * s), (x - 175 * s, feet - 560 * s),
           (x - 150 * s, feet - 380 * s), (x - 110 * s, feet - 420 * s), (x - 105 * s, feet - 520 * s),
           (x - 100 * s, feet - 300 * s), (x - 115 * s, feet - 10 * s), (x - 30 * s, feet - 10 * s),
           (x, feet - 330 * s), (x + 30 * s, feet - 10 * s), (x + 115 * s, feet - 10 * s), (x + 100 * s, feet - 300 * s),
           (x + 105 * s, feet - 520 * s), (x + 110 * s, feet - 420 * s), (x + 150 * s, feet - 380 * s),
           (x + 175 * s, feet - 560 * s), (x + 150 * s, feet - 740 * s), (x + 40 * s, feet - 790 * s)]
    ring = [(head_c[0] + 95 * s * math.cos(a_), head_c[1] + 105 * s * math.sin(a_))
            for a_ in (math.pi / 2 + 0.45 + i * (2 * math.pi - 0.9) / 30 for i in range(31))]
    col = (0.30, 0.20, 0.10)
    for poly_pts in (pts, ring):
        L_ = [0.0]
        for a_, b_ in zip(poly_pts, poly_pts[1:]):
            L_.append(L_[-1] + math.dist(a_, b_))
        n = int(L_[-1] / 22)
        j = 0
        for i in range(n):
            d = L_[-1] * i / max(1, n - 1)
            while j < len(L_) - 2 and L_[j + 1] < d:
                j += 1
            seg = (L_[j + 1] - L_[j]) or 1.0
            f = (d - L_[j]) / seg
            px = poly_pts[j][0] + (poly_pts[j + 1][0] - poly_pts[j][0]) * f
            py = poly_pts[j][1] + (poly_pts[j + 1][1] - poly_pts[j][1]) * f
            if i / max(1, n) > p:
                break
            h_ = ((i * 0.618) % 1.0)
            fall = crumble * (60 + 220 * h_) * crumble
            aa = alpha * (1 - clamp(crumble * 1.4 - 0.4 * h_))
            if aa <= 0.01:
                continue
            cr.new_path()
            cr.arc(px + 20 * crumble * math.sin(i), py + fall, 6.0, 0, 2 * math.pi)
            cr.set_source_rgba(*col, 0.85 * aa)
            cr.fill()


def soul_light(cr, t, x, y, r, a=1.0):
    """The soul: a small flame of warm-white light (a jyoti) that flickers gently, with a golden edge, a soft glow
    and drifting sparks."""
    if a <= 0.01:
        return
    pul = 0.9 + 0.1 * math.sin(t * 3.1)
    glow(cr, x, y, r * 3.6, 0.9 * a * pul)
    warm(cr, x, y, r * 2.4, 0.7 * a)
    lean = 0.12 * math.sin(t * 2.3) + 0.06 * math.sin(t * 5.1)
    h = r * (2.3 + 0.15 * math.sin(t * 4.0))
    for k, (sc, col, al) in enumerate(((1.0, (1.0, 0.72, 0.20), 0.95), (0.62, (1.0, 0.97, 0.86), 1.0))):
        w_, hh = r * sc, h * sc
        cr.save()
        cr.translate(x, y + r * 0.5 * (1 - sc))
        cr.move_to(0, r * 0.95 * sc)
        cr.curve_to(-w_ * 1.25, r * 0.6 * sc, -w_ * 0.9, -hh * 0.35, lean * hh, -hh)
        cr.curve_to(w_ * 0.9, -hh * 0.35, w_ * 1.25, r * 0.6 * sc, 0, r * 0.95 * sc)
        cr.close_path()
        if k == 0:
            cr.set_source_rgba(*pc.INK, 0.55 * a)
            cr.set_line_width(3)
            cr.stroke_preserve()
        cr.set_source_rgba(*col, al * a)
        cr.fill()
        cr.restore()
    sparkle(cr, x, y - r * 0.2, r * 0.7 * pul, 0.7 * a, (1.0, 0.97, 0.85))
    lights(cr, t, x, y, r * 1.8, 8, 0.7 * a, (1.0, 0.92, 0.6), 0.35)


def boon_token(cr, t, x, y, a=1.0):
    """A boon: a glowing gold medallion (its number is drawn over it in the headline layer)."""
    if a <= 0.01:
        return
    k = 0.6 + 0.4 * back(clamp(a), 1.6)
    glow(cr, x, y, 160, 0.6 * a)
    aura(cr, t, x, y, 50, 120, 0.5 * a, n=12, spin=0.2)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    pc.poly(cr, [(56 * math.cos(i * math.pi / 8), 56 * math.sin(i * math.pi / 8) * 1.0) for i in range(16)])
    cr.set_source_rgba(1.0, 0.80, 0.30, a)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(4)
    cr.stroke()
    cr.arc(0, 0, 40, 0, 2 * math.pi)
    cr.set_source_rgba(1.0, 0.93, 0.70, a)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(3)
    cr.stroke()
    cr.restore()


def boon_card(cr, t, t_in, x, y, s, num, lines, alpha=1.0, t_tick=None, big=False):
    """A leather boon card dropping in on its rod: BOON n, then lines [(text, colour)]; a green tick at t_tick."""
    q = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    yy = y + 60 * (1 - q)
    pc.rod(cr, x - 200 * s, yy + 180 * s, x - 160 * s, H + 60, alpha=0.5 * a)
    pc.rod(cr, x + 200 * s, yy + 180 * s, x + 220 * s, H + 60, alpha=0.5 * a)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(sway(t, 0.008, 0.4, x * 0.01))
    cr.scale(s, s)
    pc.paint_part(cr, "card", a)
    draw_text(cr, num, 0, -122, 44, RED, a, MONO_FONT, "cm", tracking=6)
    size = 92 if big else 78
    n = len(lines)
    for i, (txt, col) in enumerate(lines):
        sz = min(size, int(size * 720 / max(1, text_size(txt, size)[0])))
        draw_text(cr, txt, 0, 10 + (i - (n - 1) / 2) * size * 1.12, sz, col, a, anchor="cm")
    cr.restore()
    if t_tick is not None and t > t_tick:
        tick(cr, x + 300 * s, yy - 150 * s, 90 * s / 0.62, prog(t, t_tick, 0.3), GREEN_TICK, a)


def note(cr, x, y, s=1.0, a=1.0):
    """A music note (an ink head and stem with a flag)."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_source_rgba(*INK, a)
    pc.ell(cr, x, y, 14 * s, 10 * s, -0.4)
    cr.fill()
    cr.set_line_width(4 * s)
    cr.move_to(x + 12 * s, y - 2 * s)
    cr.line_to(x + 12 * s, y - 56 * s)
    cr.curve_to(x + 24 * s, y - 46 * s, x + 34 * s, y - 40 * s, x + 30 * s, y - 22 * s)
    cr.stroke()
    cr.restore()


def gift(cr, t, kind, x, t_in, a=1.0, t_back=None, grey=0.0):
    """One of Yama's gifts sliding in from the right to x on the floor (and back out to the right after t_back);
    grey 0..1 drains it (it will not last). Returns its label anchor (scene x, y) and the alpha."""
    u = ease((t - t_in) / 0.7)
    if u <= 0:
        return None
    x0 = W + 420
    xx = x0 + (x - x0) * u
    if t_back is not None and t > t_back:
        v = ease((t - t_back) / 0.8)
        xx += (x0 - x) * v
        a *= 1 - 0.6 * v
    hop = 14 * abs(math.sin(math.pi * clamp((t - t_in) / 0.7) * 3)) * (u < 1)
    aa = a * clamp(u * 3) * (1 - 0.55 * grey)
    bl = 2.5 * grey
    if kind == "gold":
        glow(cr, xx, FL - 90, 200, 0.45 * aa * (1 - grey))
        prop(cr, "sb_gold", xx, FL + 4 - hop, 0.54, alpha=aa, blur=bl)
        return (xx, FL - 160), aa
    if kind == "horses":
        prop(cr, "jd_horse_far", xx + 60, FL - 8 - hop, 0.27, alpha=aa, blur=bl + 1.5, flip=True)
        prop(cr, "jd_horse", xx - 20, FL + 4 - hop, 0.3, alpha=aa, blur=bl, flip=True)
        return (xx, FL - 250), aa
    if kind == "elephants":
        prop(cr, "sb_elephant", xx + 90, FL - 10 - hop, 0.36, alpha=0.8 * aa, blur=bl + 2, flip=True)
        prop(cr, "sb_elephant", xx - 20, FL + 4 - hop, 0.42, alpha=aa, blur=bl, flip=True)
        return (xx, FL - 250), aa
    if kind == "land":
        prop(cr, "sb_land", xx, FL + 4 - hop, 0.6, alpha=aa, blur=bl, flip=True)
        return (xx, FL - 170), aa
    if kind == "years":
        prop(cr, "sb_hourglass", xx, FL + 4 - hop, 0.72, alpha=aa, blur=bl)
        return (xx, FL - 250), aa
    if kind == "drum":
        prop(cr, "kk_drum", xx, FL + 4 - hop, 0.62, alpha=aa, blur=bl)
        for i in range(3):                                # music notes rising
            u2 = (t * 0.5 + i / 3) % 1.0
            note(cr, xx - 70 + 70 * i, FL - 150 - 130 * u2, 1.0, aa * math.sin(math.pi * u2))
        return (xx, FL - 130), aa
    return None


# ------------------------------------------------------------------ story 2: Mandavya


M1 = (700, 0.68)                     # Mandavya seated by his hut: x, scale
CARD_HOLD = 2.7                      # how long a chapter card holds (s) before the story's first scene


def s_m1(cr, t, tl, t0, t1):
    c = cues(tl, "m1")
    t_out = t0 + CARD_HOLD                              # the chapter card holds, then flies up
    tV = max(c["V"], t_out + 0.35)
    tB = max(c["B"], tV + 1.2)
    named = tV - t_out > 1.0                           # room for "A SAGE NAMED MANDAVYA" before the vow
    sc = prog(t, t_out - 0.1, 0.6)
    trees(cr, t, sc)
    hut(cr, t, alpha=sc)
    ground(cr, sc)
    x, s = M1
    glow(cr, x, FL - 300, 480, 0.4 * sc)
    b, k, a = depth(t, t_out - 0.1, 0.6)
    hush = keyed(t, [(t0, 0.0), (tB - 0.25, 1.0)], 0.35, 1.2)
    mp = mand(cr, t, x, s * k, mood="sleep", sit=True, hush=hush, front=ANJALI["front"], backa=ANJALI["backa"],
              alpha=a, blur=b, ph=0.4)
    lights(cr, t, x, FL - 380, 200, 6, 0.4 * sc, (1.0, 0.9, 0.6), 0.2)
    chapter(cr, t, t0 - 0.3, t_out, "STORY 2 OF 6", [[("THE SAGE WHO", INK)], [("PUNISHED", INK), ("YAMA", RED)]],
            "MAHABHARATA · ADI PARVA")
    dev_top = mp["top"]

    def ui(cr):
        if t > t_out:
            if t < tV and named:
                head2(cr, t, "A SAGE NAMED", t_out + 0.1, "MANDAVYA", t_out + 0.3)
            elif t < tB:
                head2(cr, t, "HE HAD TAKEN A", max(tV - 0.15, t_out + 0.1), "VOW OF SILENCE", tV + 0.05)
            else:
                head2(cr, t, "MEANING: HE TALKED TO", tB - 0.15, "NO ONE", tB + 0.1, under=tB + 0.5)
            tag(cr, t, t_out + 0.3, "MANDAVYA", dev_top[0] + 230, dev_top[1] + 40, 40, t_out=tB - 0.1)
            if t > tV - 0.3:
                silence_badge(cr, t, tV, 1160, 450, 0.7)
                plate(cr, t, tV + 0.2, "VOW OF SILENCE", 1160, 620, 34)
    return dict(ui=ui, flash=flash_at(t, t_out, 0.2) + flash_at(t, tV, 0.15))


M2_SAGE = (600, 0.62)
SACK_X = (1350, 1440)


def s_m2(cr, t, tl, t0, t1):
    c = cues(tl, "m2")
    tC, tS, tR, tA, tM, tH = c["C"], c["S"], c["R"], c["A"], c["M"], c["H"]
    trees(cr, t)
    hut(cr, t)
    ground(cr)
    # far behind, the king's soldiers (their spears bob at the left edge)
    fa = prog(t, tS - 0.3, 0.5)
    if fa > 0:
        for i, (x, ph) in enumerate(((70, 0.0), (190, 1.3))):
            soldier(cr, t, x + 30 * math.sin(t * 2 + ph), FL - 10, 0.44, raise_=0.0, ph=ph, alpha=0.5 * fa, blur=10,
                    legs=walk_legs(math.sin(t * 7 + ph), 0.3))
    # the thieves run in from the left to the hut, drop the sacks, and run off right
    t_in = tC - 0.35
    t_hut = max(tA, t_in + 1.6)
    t_off0 = max(tH + 0.15, t_hut + 0.6)
    dropped = t > tM
    for i, (dx, ph) in enumerate(((0, 0.0), (-170, 0.7))):
        if t < t_in + 0.25 * i:
            continue
        if t < t_off0:
            x, bob, rock, lp = hop_walk(t, t_in + 0.25 * i, t_hut + 0.25 * i, -180 + dx, SACK_X[i] - 120, 0.3)
        else:
            x, bob, rock, lp = hop_walk(t, t_off0 + 0.15 * i, t_off0 + 1.2 + 0.15 * i, SACK_X[i] - 120, 2200, 0.28)
        s = 0.56
        bend = keyed(t, [(t0, 0.0), (tM - 0.3, 1.0), (tM + 0.35, 0.0)], 0.25, 1.2)
        thief(cr, t, x, s, sack=not dropped, legs=walk_legs(lp, 0.45), rot=rock + 0.08 + 0.25 * bend,
              y=FL - 434 * s + bob, ph=ph, blur=1.5, backa=(-2.5, -0.9) if not dropped else (0.3, -0.4),
              front=(-0.9, -0.6))
    if dropped:
        for i, x in enumerate(SACK_X):
            q = back(clamp((t - tM - 0.05 * i) / 0.3), 1.4)
            sack_at(cr, t, x, 0.36 * clamp(q), alpha=clamp(q * 2), rot=0.05 * (i - 0.5))
    x, s = M2_SAGE
    glow(cr, x, FL - 300, 420, 0.3)
    mand(cr, t, x, s, mood="sleep", sit=True, front=ANJALI["front"], backa=ANJALI["backa"], ph=0.4)
    dev_s = cr.user_to_device((SACK_X[0] + SACK_X[1]) / 2, FL - 70)
    dev_far = cr.user_to_device(150, FL - 430)

    def ui(cr):
        if t < tR:
            head2(cr, t, "ONE DAY, SOME", t0 + 0.05, "THIEVES", tC)
        elif t < tH:
            head2(cr, t, "RUNNING FROM THE", tR - 0.15, "KING'S SOLDIERS", tR + 0.05)
        else:
            head2(cr, t, "THE THIEVES HID THE LOOT", tH - 0.15, "RIGHT HERE!", tH + 0.05)
        tag(cr, t, tS + 0.1, "THE KING'S SOLDIERS", dev_far[0] + 120, dev_far[1], 28, t_out=tA)
        if t > tH:
            red_ring(cr, dev_s[0], dev_s[1], 150, 95, prog(t, tH + 0.1, 0.45), 9)
            red_arrow(cr, [(1180, 300), (1240, 420), (dev_s[0] - 110, dev_s[1] - 60)], prog(t, tH + 0.3, 0.4))
            plate(cr, t, tH + 0.5, "LOOT", dev_s[0], dev_s[1] - 150, 34)
    return dict(ui=ui, flash=flash_at(t, tC, 0.15) + flash_at(t, tH, 0.2))


M3_SAGE = (1180, 0.62)
SOLDIERS3 = ((560, 0.0), (390, 0.9))


def s_m3(cr, t, tl, t0, t1):
    c = cues(tl, "m3")
    tP, tQ, tM, tN = c["P"], c["Q"], c["M"], c["N"]
    trees(cr, t)
    for i, x in enumerate(SACK_X):                       # the hidden sacks, half behind the hut
        sack_at(cr, t, x + 120, 0.3, alpha=0.9)
    hut(cr, t)
    ground(cr)
    for i, (x, ph) in enumerate(SOLDIERS3):
        xx, bob, rock, lp = hop_walk(t, t0 - 0.2 + 0.2 * i, t0 + 1.4 + 0.2 * i, -260 - 150 * i, x, 0.38)
        ask = keyed(t, [(t0, 0.0), (tP - 0.1, 1.0)], 0.3, 1.3) if i == 0 else 0.0
        soldier(cr, t, xx, FL, 0.58, raise_=0.0, ph=ph, legs=walk_legs(lp, 0.3), rot=rock, rods=True,
                guard=0.0 + 0.0 * ask)
    x, s = M3_SAGE
    glow(cr, x, FL - 300, 420, 0.35 + 0.2 * prog(t, tM, 0.4))
    hush = keyed(t, [(t0, 0.0), (tM - 0.1, 1.0)], 0.35, 1.2)
    mp = mand(cr, t, x, s, mood="sleep", sit=True, flip=True, hush=hush, front=ANJALI["front"],
              backa=ANJALI["backa"], ph=0.4)
    dev_top = mp["top"]

    def ui(cr):
        if t < tM:
            head2(cr, t, "THE SOLDIERS ASKED THE SAGE:", t0 + 0.05, None, 0.0)
        else:
            head2(cr, t, "BUT THE SAGE STAYED", tM - 0.15, "SILENT", tM + 0.05, under=tN)
        cloud_text(cr, t, 860, 420, 0.56, [("WHERE DID", 66, INK, -40, tQ - 0.1), ("THEY GO?", 84, RED, 46, tQ + 0.2)],
                   alpha=1 - prog(t, tM - 0.2, 0.25), t_in=tP - 0.1)
        if t > tM - 0.2:
            dots_cloud(cr, t, tM - 0.1, dev_top[0] - 200, dev_top[1] - 30, 0.42, flip=True)
            silence_badge(cr, t, tN, 1560, 420, 0.6)
    return dict(ui=ui, flash=flash_at(t, tQ, 0.12) + flash_at(t, tM, 0.15))


def s_m4(cr, t, tl, t0, t1):
    c = cues(tl, "m4")
    tM, tF, tL, tC = c["M"], c["F"], c["L"], c["C"]
    trees(cr, t)
    hut(cr, t)
    ground(cr)
    # soldier 1 walks behind the sage to the hut, lifts a sack; soldier 2 waits; both turn their spears to the sage
    t_go, t_at = t0 - 0.1, max(tM - 0.3, t0 + 1.0)
    x1, bob, rock, lp = hop_walk(t, t_go, t_at, SOLDIERS3[0][0], 1370, 0.38)
    turn = keyed(t, [(t0, 0.0), (tL - 0.1, 1.0)], 0.3, 1.3)
    lift = keyed(t, [(t0, 0.0), (tM, 1.0), (tL - 0.2, 0.0)], 0.3, 1.3)
    for i, x in enumerate(SACK_X):
        if i == 0 and lift > 0.02:
            continue
        sack_at(cr, t, x + (60 if i else 0), 0.36)
    sx, sy = 1300, FL - 150 * lift
    if lift > 0.02:
        prop(cr, "sb_sack", sx, sy + 4, 0.36, rot=0.3 * lift, alpha=1.0)
        for i in range(7):                                   # coins spill out (and stay on the floor)
            ti = tM + 0.08 * i
            if t < ti:
                continue
            u = clamp((t - ti) / 0.5)
            cxx = sx - 30 + 26 * i + 40 * u * (i % 3 - 1)
            cyy = sy - 90 + (FL - 6 - (sy - 90)) * u * u
            prop(cr, "sb_coin", cxx, cyy, 0.7, rot=t * 3 + i)
    soldier(cr, t, x1, FL, 0.58, raise_=0.0, ph=0.0, legs=walk_legs(lp, 0.3), rot=rock + 0.15 * lift, blur=1.5,
            flip=turn > 0.5)
    soldier(cr, t, SOLDIERS3[1][0] + 150, FL, 0.58, raise_=0.0, ph=0.9)
    x, s = M3_SAGE
    glow(cr, x, FL - 300, 420, 0.35)
    mp = mand(cr, t, x, s, mood="sleep", sit=True, flip=True, front=ANJALI["front"], backa=ANJALI["backa"], ph=0.4)
    dev_loot = cr.user_to_device(sx, sy - 60)
    dev_sage = to_user(cr, mp["chest"])
    dev_sage = cr.user_to_device(*dev_sage)

    def ui(cr):
        if t < tL:
            head2(cr, t, "THE SOLDIERS FOUND", t0 + 0.05, "THE LOOT", tM)
        else:
            head2(cr, t, "THEY THOUGHT THE SAGE WAS THE", tL - 0.15, "CHIEF THIEF", tC, under=tC + 0.5)
        if t > tM and t < tL + 0.6:
            red_ring(cr, dev_loot[0], dev_loot[1], 140, 110, prog(t, tM + 0.1, 0.4), 8,
                     alpha=1 - prog(t, tL + 0.3, 0.3))
            plate(cr, t, tM + 0.25, "THE LOOT!", dev_loot[0], dev_loot[1] - 165, 34, t_out=tL + 0.3)
        if t > tL:
            p = prog(t, tL + 0.2, 0.6)
            dotted(cr, [(dev_loot[0] - 20, dev_loot[1] - 60), (dev_loot[0] - 110, dev_loot[1] - 230),
                        (dev_sage[0] + 60, dev_sage[1] - 160)], p, 24, 6, RED, 0.9)
            if t > tC:
                red_ring(cr, dev_sage[0] + 10, dev_sage[1] - 40, 190, 300, prog(t, tC + 0.05, 0.5), 9)
    return dict(ui=ui, flash=flash_at(t, tM, 0.15) + flash_at(t, tC, 0.25))


KING5 = (380, 0.64)
SAGE5 = (860, 0.55)
STAKE5 = (1560, 0.6)


def s_m5(cr, t, tl, t0, t1):
    c = cues(tl, "m5")
    tZ, tS = c["Z"], c["S"]
    palace(cr, t)
    ground(cr)
    dim = prog(t, tS + 0.6, 1.2)
    glow(cr, 960, 700, 700, 0.3)
    # the stake rises on the right (an object only)
    if t > tS - 0.3:
        b, k, a = depth(t, tS - 0.3, 0.6)
        px, ps = STAKE5
        glow(cr, px, FL - 360, 360, 0.5 * a)
        prop(cr, "sb_stake", px, FL + 6 + 200 * (1 - ease((t - tS + 0.3) / 0.6)), ps * k, alpha=a, blur=b)
    x, s = SAGE5
    mand(cr, t, x, s, mood="sleep", flip=True, front=ANJALI["front"], backa=ANJALI["backa"], ph=0.4)
    kx, ks = KING5
    point = keyed(t, [(t0, 0.0), (tZ - 0.1, 1.0)], 0.3, 1.4)
    king(cr, t, kx, ks, mood="angry" if t > tZ - 0.2 else "calm", front=mix((-0.35, -0.5), (-1.62, 0.0), point),
         backa=(0.6, -1.4), hits=[(tZ, 0.4), (tS, 0.3)], ph=1.0)
    dev_k = cr.user_to_device(kx - 10, FL - 434 * ks - 470 * ks)

    def ui(cr):
        head2(cr, t, "THE KING GAVE HIS", t0 + 0.05, "ORDER", tZ)
        tag(cr, t, t0 + 0.2, "THE KING", 170, 470, 34, t_out=tS - 0.2)
        card2(cr, t, tS - 0.15, 1240, 420, 0.7, [("PUNISHMENT:", 70, INK, -48, tS), ("THE STAKE", 100, RED, 44, tS + 0.3)])
    return dict(ui=ui, eve=0.18 * dim, flash=flash_at(t, tZ, 0.2) + flash_at(t, tS, 0.25))


def curtain(cr, t, x, y0, y1, w, a):
    """A curtain of light: soft vertical streaks of warm light that shimmer, from y0 down to y1."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for i in range(15):
        u = i / 14
        xx = x - w / 2 + w * u + 10 * math.sin(t * 0.9 + i * 1.7)
        ww = w * (0.05 + 0.04 * math.sin(i * 2.3) ** 2)
        k = (0.55 + 0.45 * math.sin(t * 1.6 + i * 2.1)) * (1 - 0.6 * abs(u - 0.5) * 2)
        g = cairo.LinearGradient(0, y0, 0, y1)
        g.add_color_stop_rgba(0, 1.0, 0.92, 0.66, 0.0)
        g.add_color_stop_rgba(0.15, 1.0, 0.92, 0.66, 0.30 * k * a)
        g.add_color_stop_rgba(0.8, 1.0, 0.86, 0.52, 0.22 * k * a)
        g.add_color_stop_rgba(1, 1.0, 0.86, 0.52, 0.0)
        cr.rectangle(xx - ww / 2, y0, ww, y1 - y0)
        cr.set_source(g)
        cr.fill()
    cr.restore()
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgba(0, 1.0, 0.96, 0.84, 0.0)
    g.add_color_stop_rgba(0.25, 1.0, 0.96, 0.84, 0.55 * a)
    g.add_color_stop_rgba(1, 1.0, 0.93, 0.78, 0.75 * a)
    cr.save()
    cr.rectangle(x - w / 2, y0, w, y1 - y0)
    cr.set_source(g)
    cr.fill()
    cr.restore()


def s_m6(cr, t, tl, t0, t1):
    c = cues(tl, "m6")
    tD, tT, tZ = c["D"], c["T"], c["Z"]
    ground(cr, 0.8)
    light = prog(t, t0 + 0.1, 0.8)
    hy = 640
    glow(cr, 960, hy - 120, 700, 0.75 * light)
    aura(cr, t, 960, hy - 210, 160, 520, 0.55 * light * (0.6 + 0.4 * prog(t, tT, 0.6)), n=22, spin=0.05)
    mand(cr, t, 960, 0.55, mood="sleep", sit=True, front=ANJALI["front"], backa=ANJALI["backa"], ph=0.4,
         y=hy + 6 * math.sin(t * 1.2), rods=False)
    lights(cr, t, 960, hy - 200, 320, 12, 0.7 * light, (1.0, 0.9, 0.6), 0.25)
    curtain(cr, t, 960, hy - 10, FL - 4, 560, light)
    if t > tT:
        burst(cr, t, 960, hy - 220, tT, n=18, rmax=560, alpha=0.6)

    def ui(cr):
        if t < tT:
            head2(cr, t, "BUT THE SAGE", t0 + 0.05, "DID NOT DIE", tD)
        else:
            head2(cr, t, "HIS TAPAS (HIS PRAYER POWER) KEPT HIM", tT - 0.1, "ALIVE", tZ, under=tZ + 0.4)
    return dict(ui=ui, night=0.38, lift=1.0, flash=flash_at(t, tD, 0.25) + flash_at(t, tZ, 0.2))


SAGE7 = (1260, 0.56)


def s_m7(cr, t, tl, t0, t1):
    c = cues(tl, "m7")
    tS, tP, tM, tU = c["S"], c["P"], c["M"], c["U"]
    palace(cr, t)
    ground(cr)
    x, s = SAGE7
    glow(cr, x, FL - 340, 460, 0.45 + 0.2 * prog(t, tU, 0.5))
    aura(cr, t, x - 10, FL - 520, 120, 420, 0.25, n=16, spin=0.03)
    free = keyed(t, [(t0, 0.0), (tU - 0.1, 1.0)], 0.35, 1.2)
    mand(cr, t, x, s, mood="calm" if t < tU else "teach", flip=True, front=mix((-0.3, -0.5), (-1.3, -0.6), free),
         backa=(0.3, -0.3), ph=0.4, hits=[(tU, 0.3)])
    kneel = t > tP - 0.05
    ks = 0.6
    if not kneel:
        (kp, kx) = walking(king, cr, t, tS - 0.6, tP - 0.15, -200, 990, ks, mood="calm", ph=1.0,
                           front=(-0.4, -0.5))
    else:
        bow = keyed(t, [(t0, 0.0), (tP + 0.1, 1.0)], 0.3, 1.2)
        kp = king(cr, t, 990, ks, mood="shame", kneel="sb_king_kneel", front=ANJALI["front"], backa=ANJALI["backa"],
                  head=0.2 * bow, rot=0.12 * bow, hits=[(tP, 0.5)], ph=1.0)
    dev_k = kp["top"]

    def ui(cr):
        if t < tP:
            head2(cr, t, "THE KING LEARNED THE", t0 + 0.05, "TRUTH", tS)
        elif t < tU:
            head2(cr, t, "HE FELL AT THE SAGE'S FEET:", tP - 0.15, "SORRY!", tM)
        else:
            head2(cr, t, "AND THE SAGE WAS", tU - 0.15, "FREED", tU + 0.05, under=tU + 0.5)
        if t > tM - 0.25:
            cloud_text(cr, t, dev_k[0] - 330, dev_k[1] + 10, 0.5,
                       [("I WAS WRONG.", 58, INK, -40, tM), ("FORGIVE ME!", 80, RED, 46, tM + 0.35)], flip=True,
                       t_in=tM - 0.25, alpha=1 - prog(t, tU + 0.6, 0.4))
    return dict(ui=ui, flash=flash_at(t, tS, 0.15) + flash_at(t, tU, 0.25))


YAMA8 = (1400, 0.52)
LEDGER8 = (1040, 0.62)


def ledger_open(cr, t, t_in, x, s, tallies=0.0, alpha=1.0):
    """The book of deeds open on its stand (rising in at t_in): SINS / GOOD DEEDS with tally marks (tallies 0..1).
    Returns the page centre (scene) for the flashback."""
    if t < t_in - 0.05:
        return None
    b, k, a = depth(t, t_in, 0.5)
    a *= alpha
    yy = FL + 6 + 80 * (1 - ease((t - t_in) / 0.5))
    prop(cr, "sb_ledger_open", x, yy, s * k, alpha=a, blur=b)
    for side, (txt, col) in enumerate((("SINS", RED), ("GOOD DEEDS", GREEN_TICK))):
        px, py = SB.LEDGER_PAGES[side]
        cx, cy = x + px * s * k, yy + py * s * k
        draw_text(cr, txt, cx, cy - 128 * s * k, int(25 * s * k / 0.62), col, a * prog(t, t_in + 0.3, 0.3),
                  MONO_FONT, "cm", tracking=1)
        n = int(18 * tallies)
        for i in range(n):
            row, col_ = divmod(i, 6)
            tx = cx - 100 * s * k + col_ * 34 * s * k
            ty = cy - 60 * s * k + row * 60 * s * k
            cr.set_source_rgba(*(INK if side == 0 else GREEN_TICK), 0.85 * a)
            cr.set_line_width(4 * s * k / 0.62)
            cr.move_to(tx, ty)
            cr.line_to(tx + 4 * s, ty + 40 * s * k)
            cr.stroke()
    return x, yy - 440 * s * k


def s_m8(cr, t, tl, t0, t1):
    c = cues(tl, "m8")
    tY, tD, tP, tH = c["Y"], c["D"], c["P"], c["H"]
    hall(cr, t)
    ground(cr)
    yx, ys = YAMA8
    glow(cr, yx, FL - 380, 480, 0.35 + 0.2 * prog(t, tY, 0.5))
    lx, ls = LEDGER8
    tall = clamp((t - tP) / max(0.8, tH - tP + 0.6))
    ledger_open(cr, t, tP - 0.4, lx, ls, tallies=tall)
    yp = yama(cr, t, yx, ys, flip=True, book=t < tP - 0.4, nod=nods(t, (tD + 0.2,), 0.6), hits=[(tY, 0.3)], ph=0.6)
    mp, _ = walking(mand, cr, t, t0 - 0.2, tY - 0.1, -220, 560, 0.56, mood="calm", ph=0.4, front=(-0.4, -0.5))
    dev_y = yp["top"]

    def ui(cr):
        if t < tD:
            head2(cr, t, "THEN THE SAGE WENT STRAIGHT TO", t0 + 0.05, "YAMA", tY)
        else:
            head2(cr, t, "YAMA IS DHARMARAJA,", tD - 0.15, "KEEPER OF SINS", tD + 0.1)
        tag(cr, t, tY + 0.2, "YAMA", dev_y[0] + 170, dev_y[1] + 90, 40)
    return dict(ui=ui, cool=0.18, flash=flash_at(t, tY, 0.2) + flash_at(t, tP, 0.12))


SAGE9 = (600, 0.56)


def s_m9(cr, t, tl, t0, t1):
    c = cues(tl, "m9")
    tP, tK, tS = c["P"], c["K"], c["S"]
    hall(cr, t)
    ground(cr)
    yx, ys = YAMA8
    glow(cr, yx, FL - 380, 480, 0.4)
    ledger_open(cr, t, -10.0, LEDGER8[0], LEDGER8[1], tallies=1.0)
    yama(cr, t, yx, ys, flip=True, book=False, ph=0.6)
    ask = keyed(t, [(t0, 0.0), (tP - 0.1, 1.0)], 0.3, 1.3)
    x, s = SAGE9
    mp = mand(cr, t, x, s, mood="calm", front=mix((-0.4, -0.5), (-1.25, -0.75), ask), backa=(0.3, -0.4),
              head=-0.06 * ask, hits=[(tP, 0.3), (tS, 0.3)], ph=0.4)
    dev_m = mp["top"]

    def ui(cr):
        head2(cr, t, "THE SAGE ASKED YAMA:", t0 + 0.05, "WHAT WAS MY SIN?", tK, under=tK + 0.6)
        cloud_text(cr, t, dev_m[0] + 300, dev_m[1] + 130, 0.42, [("WHY THIS", 64, INK, -38, tS),
                                                                 ("PUNISHMENT?", 76, RED, 44, tS + 0.25)],
                   t_in=tS - 0.2)
    return dict(ui=ui, cool=0.18, flash=flash_at(t, tK, 0.2))


def kid_scene(cr, t, w, h, tK, tG, tC):
    """Inside the flashback card: little Mandavya kneels and pokes an insect with a blade of grass."""
    gy = h / 2 - 70
    cr.set_source_rgba(0.45, 0.30, 0.14, 0.9)
    cr.rectangle(-w / 2, gy, w, 80)
    cr.fill()
    for i in range(14):                                       # grass tufts
        gx = -w / 2 + 30 + i * (w - 60) / 13
        for k in (-1, 0, 1):
            pc.poly(cr, [(gx + 6 * k - 4, gy + 2), (gx + 16 * k, gy - 26 - 8 * abs(k)), (gx + 6 * k + 4, gy + 2)])
            cr.set_source_rgba(0.30, 0.50, 0.18, 0.95)
            cr.fill()
    ks = 0.42
    kx = -110
    poke = 0.0
    if t > tC - 0.15:
        u = (t - tC + 0.15) / 0.5
        poke = math.sin(math.pi * clamp(u)) if u < 1 else 0.25 * max(0.0, math.sin(math.pi * clamp(u - 1)))
    reach = (-1.25 - 0.2 * poke, -0.35 + 0.25 * poke)
    pts = body(cr, SB.KID, "sb_kid", t, kx + 12 * poke, ks, front=reach, backa=(-0.2, -0.6), head=0.1,
               kneel="sb_kid_kneel", feet=gy, rot=0.12 + 0.03 * poke, scales={"sb_kid_head": KID_HEAD}, rods=False)
    hand = to_user(cr, pts["handF"])
    bx, by = 150, gy - 4
    flinch = math.exp(-4 * (t - tC - 0.2)) * (t > tC + 0.1)
    prop(cr, "sb_bug", bx + 30 * flinch, by - 30 * flinch * abs(math.sin((t - tC) * 20)), 0.5,
         rot=-0.2 * flinch, flip=True)
    tip = (bx - 46 + 10 * poke, by - 24)
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_source_rgba(0.20, 0.42, 0.10, 1)
    cr.set_line_width(7)
    cr.move_to(*hand)
    cr.curve_to(hand[0] + 60, hand[1] - 20, tip[0] - 60, tip[1] - 30, *tip)
    cr.stroke()
    cr.set_source_rgba(0.45, 0.72, 0.25, 1)
    cr.set_line_width(3)
    cr.move_to(*hand)
    cr.curve_to(hand[0] + 60, hand[1] - 20, tip[0] - 60, tip[1] - 30, *tip)
    cr.stroke()
    cr.restore()
    if t > tC + 0.1 and t < tC + 1.2:                          # the insect's little start: two short lines
        for k in (-1, 1):
            cr.set_source_rgba(*INK, 0.8 * (1 - clamp((t - tC - 0.1) / 1.1)))
            cr.set_line_width(4)
            cr.move_to(bx + 60 + 30 * k, by - 90)
            cr.line_to(bx + 70 + 50 * k, by - 130)
            cr.stroke()
    return (bx, by - 30), hand


def s_m10(cr, t, tl, t0, t1):
    c = cues(tl, "m10")
    tB, tK, tG, tC = c["B"], c["K"], c["G"], c["C"]
    hall(cr, t)
    ground(cr)
    yx, ys = YAMA8
    lx, ls = LEDGER8
    glow(cr, yx, FL - 380, 480, 0.4)
    page = ledger_open(cr, t, -10.0, lx, ls, tallies=1.0)
    point = keyed(t, [(t0, 0.0), (tB - 0.4, 1.0)], 0.3, 1.3)
    yama(cr, t, yx, ys, flip=True, book=False, front=mix((-0.95, -1.15), (-1.45, -0.15), point), ph=0.6,
         hits=[(tB - 0.3, 0.3)])
    mand(cr, t, 330, 0.56, mood="calm", front=(-0.4, -0.5), ph=0.4)
    if page and t > tB - 0.6:
        glow(cr, page[0], page[1], 300, 0.6 * prog(t, tB - 0.6, 0.4))
        lights(cr, t, page[0], page[1] - 40, 120, 8, 0.7 * prog(t, tB - 0.6, 0.4))
    dev_card = cr.user_to_device(840, 520)
    src = cr.user_to_device(*(page or (lx, FL - 400)))
    store = {}

    def content(cr_, w, h):
        store["bug"], store["hand"] = kid_scene(cr_, t, w, h, tK, tG, tC)

    def ui(cr):
        head2(cr, t, "YAMA SAID:", t0 + 0.05, "AS A CHILD...", tB)
        flashback(cr, t, tB - 0.1, src, dev_card, (820, 500), content)
        if "bug" in store and t > tK:
            bx, by = store["bug"]
            gx, gy = dev_card[0] + bx, dev_card[1] + by
            red_ring(cr, gx + 10, gy, 90, 60, prog(t, tK + 0.05, 0.4), 7)
            plate(cr, t, tK + 0.15, "AN INSECT", gx + 60, gy - 120, 30)
            plate(cr, t, tG + 0.1, "A BLADE OF GRASS", dev_card[0] + 170, dev_card[1] - 120, 30)
    return dict(ui=ui, cool=0.18, flash=flash_at(t, tB, 0.2) + flash_at(t, tC, 0.15))


def s_m11(cr, t, tl, t0, t1):
    c = cues(tl, "m11")
    tN, tS, tA = c["N"], c["S"], c["A"]
    hall(cr, t)
    ground(cr)
    yx, ys = YAMA8
    glow(cr, yx, FL - 380, 480, 0.35)
    yama(cr, t, yx + 80, ys, flip=True, book=False, ph=0.6)
    tilt = lambda tt: 0.0 if tt < tS else -0.42 * (1 - math.exp(-3 * (tt - tS)) * math.cos(9 * (tt - tS)))

    def bug_fig(cr_, tt, y, a):
        prop(cr_, "sb_bug", 0, y - 20, 0.8, alpha=a)

    def stake_fig(cr_, tt, y, a):
        prop(cr_, "sb_stake", -30, y + 12, 0.3, rot=1.5, alpha=a)

    sa = prog(t, t0 + 0.05, 0.4)
    pans = balance(cr, t, 960, FL + 4, 0.56, tilt, left=[dict(kind="fig", fn=bug_fig, t=tN + 0.1)],
                   right=[dict(kind="fig", fn=stake_fig, t=tS)], alpha=sa, labels=0.0)
    angry = keyed(t, [(t0, 0.0), (tA - 0.15, 1.0)], 0.25, 1.5)
    mp = mand(cr, t, 400, 0.56, mood="angry" if t > tS - 0.2 else "calm",
              front=mix((-0.6, -0.7), (-2.6, -0.5), angry), backa=(0.5, -1.2), head=-0.05 * angry,
              hits=[(tA, 0.6)], ph=0.4)
    dl = cr.user_to_device(*pan_xy(pans[0], 0.56, 0, 420)) if pans else (0, 0)
    dr = cr.user_to_device(*pan_xy(pans[1], 0.56, 0, 420)) if pans else (0, 0)

    def ui(cr):
        if t < tA:
            head2(cr, t, "A CHILD'S MISTAKE...", t0 + 0.05, "SUCH A BIG PUNISHMENT?", tS)
        else:
            head2(cr, t, "THE SAGE SAID:", tA - 0.15, "UNFAIR!", tA + 0.05, under=tA + 0.4)
        plate(cr, t, tN + 0.2, "A CHILD'S MISTAKE", dl[0] - 60, dl[1], 28, alpha=sa)
        plate(cr, t, tS + 0.15, "THE PUNISHMENT", dr[0] + 60, dr[1], 28, alpha=sa)
    return dict(ui=ui, cool=0.15, flash=flash_at(t, tS, 0.2) + flash_at(t, tA, 0.25))


def rule_card(cr, t, t_in, x, y, s, tF, tP, alpha=1.0):
    """The big NEW RULE card: UNDER 14 = NO SIN, the 14 big and red."""
    q = back(clamp((t - t_in) / 0.4), 1.4)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    yy = y + 80 * (1 - q)
    for sx in (-1, 1):
        pc.rod(cr, x + sx * 300 * s, yy + 190 * s, x + sx * 260 * s, H + 60, alpha=0.5 * a)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(sway(t, 0.006, 0.35, 1.0))
    cr.scale(s, s)
    pc.paint_part(cr, "card", a)
    draw_text(cr, "NEW RULE", 0, -128, 46, RED, a, MONO_FONT, "cm", tracking=10)
    p1, p2 = prog(t, tF, 0.3), prog(t, tP, 0.3)
    k = 1.25 - 0.25 * back(clamp((t - tF) / 0.35))
    draw_text(cr, "UNDER", -232, 10, 84, INK, a * p1, anchor="cm")
    cr.save()
    cr.translate(-30, 6)
    cr.scale(k, k)
    draw_text(cr, "14", 0, 0, 210, RED, a * p1, anchor="cm")
    cr.restore()
    draw_text(cr, "=", 118, 12, 96, INK, a * p2, MONO_FONT, "cm")
    draw_text(cr, "NO SIN", 162, 10, 84, INK, a * p2, anchor="lm")
    draw_text(cr, "WHAT A CHILD DOES IS NOT A SIN", 0, 122, 26, FADE, a * prog(t, tP + 0.3, 0.3), MONO_FONT, "cm",
              tracking=3)
    cr.restore()


def s_m12(cr, t, tl, t0, t1):
    c = cues(tl, "m12")
    tR, tF, tB, tP = c["R"], c["F"], c["B"], c["P"]
    hall(cr, t)
    ground(cr)
    glow(cr, 960, 560, 640, 0.35 + 0.3 * prog(t, tR, 0.5))
    yx, ys = YAMA8
    yama(cr, t, yx + 160, ys, flip=True, book=False, nod=nods(t, (tP + 0.2,), 0.6), ph=0.6)
    raise_ = keyed(t, [(t0, 0.0), (tR - 0.15, 1.0)], 0.3, 1.4)
    mand(cr, t, 330, 0.56, mood="teach", front=mix((-0.4, -0.5), (-2.7, -0.3), raise_), backa=(0.3, -0.4),
         hits=[(tR, 0.4)], ph=0.4)
    if t > tB - 0.2:                                          # a small child beside the card
        b, k, a = depth(t, tB - 0.2, 0.5)
        glow(cr, 530, FL - 160, 220, 0.5 * a)
        body(cr, SB.KID, "sb_kid", t, 530, 0.3 * k, front=(-0.4, -0.6), alpha=a, blur=b,
             scales={"sb_kid_head": KID_HEAD}, ph=2.0)
    if t > tR:
        burst(cr, t, 960, 520, tR + 0.2, n=16, rmax=520, alpha=0.5)

    def ui(cr):
        head2(cr, t, "THAT DAY THE SAGE MADE A", t0 + 0.05, "NEW RULE", tR)
        rule_card(cr, t, tR + 0.15, 1000, 520, 0.92, tF, tP)
    return dict(ui=ui, cool=0.12, flash=flash_at(t, tR, 0.2) + flash_at(t, tF, 0.25))


def s_m13(cr, t, tl, t0, t1):
    c = cues(tl, "m13")
    tS, tI, tD = c["S"], c["I"], c["D"]
    hall(cr, t)
    ground(cr)
    yx, ys = 1420, 0.52
    glow(cr, yx, FL - 380, 480, 0.35)
    hit = prog(t, tS + 0.25, 0.4)
    yp = yama(cr, t, yx, ys, mood="shame" if t > tS + 0.4 else "calm", flip=True, book=False,
              head=0.18 * hit, ph=0.6, hits=[(tS + 0.3, 0.4)])
    aim = keyed(t, [(t0, 0.0), (tS - 0.15, 1.0)], 0.3, 1.5)
    mp = mand(cr, t, 460, 0.56, mood="angry", front=mix((-0.5, -0.6), (-1.42, 0.0), aim), backa=(0.5, -1.2),
              hits=[(tS, 0.5)], ph=0.4)
    hand = to_user(cr, mp["handF"])
    chest = to_user(cr, yp["chest"])
    if t > tS:                                                # a line of gold light from the finger to Yama
        p = prog(t, tS, 0.35)
        ex, ey = hand[0] + (chest[0] - hand[0]) * p, hand[1] + (chest[1] - hand[1]) * p
        cr.save()
        cr.set_operator(cairo.OPERATOR_ADD)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        f = 1 - 0.6 * prog(t, tS + 1.0, 0.8)
        for lw, a in ((28, 0.16), (12, 0.4), (4, 0.9)):
            cr.move_to(*hand)
            cr.line_to(ex, ey)
            cr.set_source_rgba(1.0, 0.85, 0.45, a * f)
            cr.set_line_width(lw)
            cr.stroke()
        cr.restore()
        if p >= 1:
            glow(cr, chest[0], chest[1], 260, 0.5 * f)
    wa = prog(t, tD - 0.2, 0.5)
    if wa > 0:
        glow(cr, 960, FL - 200, 360, 0.4 * wa)
        prop(cr, "md_world", 960, FL - 190 + 30 * (1 - wa), 0.42, rot=sway(t, 0.006, 0.4), alpha=wa)
        pc.rod(cr, 900, FL - 100, 930, H + 60, alpha=0.5 * wa)
        pc.rod(cr, 1020, FL - 100, 1050, H + 60, alpha=0.5 * wa)
    dev_y = cr.user_to_device(yx - 60, FL - 560)
    dev_w = cr.user_to_device(960, FL - 196)

    def ui(cr):
        head2(cr, t, "THEN THE SAGE CURSED YAMA:", t0 + 0.05, "BE BORN AS A HUMAN", tI, under=tI + 0.7)
        if t > tD - 0.1:
            from poster import person
            q = prog(t, tD + 0.3, 0.4)
            person(cr, dev_w[0] + 20, dev_w[1] - 4, 130 * q, INK, 0.9 * q)
            dotted(cr, [(dev_y[0] - 40, dev_y[1] + 40), (dev_y[0] - 220, dev_y[1] + 120),
                        (dev_w[0] + 80, dev_w[1] - 110)], prog(t, tD, 0.6), 24, 6, RED, 0.9)
            plate(cr, t, tD + 0.3, "EARTH", dev_w[0] - 200, dev_w[1] + 60, 32)
            plate(cr, t, tD + 0.5, "A HUMAN", dev_w[0] + 20, dev_w[1] - 175, 28)
    return dict(ui=ui, cool=0.15, flash=flash_at(t, tS, 0.3) + flash_at(t, tI, 0.15))


def s_m14(cr, t, tl, t0, t1):
    c = cues(tl, "m14")
    tJ, tM, tS, tV = c["J"], c["M"], c["S"], c["V"]
    turn = prog(t, tJ, 1.2)
    if turn < 1:
        hall(cr, t, 1 - turn)
    if turn > 0:
        palace(cr, t, turn)
    ground(cr)
    x = 960
    if turn < 1:                                             # Yama glows and dissolves into light
        glow(cr, x, FL - 380, 520, 0.4 + 0.6 * turn)
        aura(cr, t, x, FL - 420, 140, 520, 0.6 * turn * (1 - turn) * 4, n=22, spin=0.08)
        yama(cr, t, x, 0.52, alpha=1 - turn, blur=10 * turn, book=False, nod=0.3, ph=0.6, rods=turn < 0.5)
        lights(cr, t, x, FL - 400, 260, 14, 0.9 * turn, (1.0, 0.9, 0.6), 0.5)
    if t > tJ:
        burst(cr, t, x, FL - 420, tJ + 0.5, n=20, rmax=640, alpha=0.8)
    if t > tM - 0.4:
        b, k, a = depth(t, tM - 0.4, 0.7)
        glow(cr, x, FL - 360, 460, 0.5 * a)
        vp = vidura(cr, t, x, 0.6 * k, mood="smile" if t > tV else "calm", front=ANJALI["front"],
                    backa=ANJALI["backa"], alpha=a, blur=b, ph=0.3, hits=[(tV, 0.3)])
        dev_v = vp["top"]
    else:
        dev_v = None

    def ui(cr):
        if t < tV:
            head2(cr, t, "AND YAMA WAS BORN...", t0 + 0.05, None, 0.0)
        else:
            head2(cr, t, "YAMA WAS BORN AS", tV - 0.15, "VIDURA", tV + 0.05, under=tV + 0.5)
        if dev_v is not None:
            tag(cr, t, tV - 0.1, "VIDURA", dev_v[0] - 330, dev_v[1] + 60, 44)
            plate(cr, t, tS + 0.1, "THE WISEST MAN OF THE MAHABHARATA", 960, 960, 32)
    return dict(ui=ui, cool=0.15 * (1 - turn), flash=flash_at(t, tJ + 0.5, 0.4) + flash_at(t, tV, 0.2))


# ------------------------------------------------------------------ story 5: Nachiketa


FATHER = (380, 0.6)
FIRE = (700, 1.0)
COWS = ((1150, 0.5, 0.0), (1610, 0.48, 1.3))


def cows(cr, t, alpha=1.0, walk_from=None, xs=COWS):
    """The thin old cows, heads low, shifting slowly (walk_from: they plod off to the right from then)."""
    for i, (x, s, ph) in enumerate(xs):
        dx = 0.0
        if walk_from is not None and t > walk_from:
            dx = 40 * (t - walk_from)
        bob = 4 * math.sin(t * 1.3 + ph)
        prop(cr, "sb_cow_low", x + dx, FL + 4 + bob * 0.3, s, rot=sway(t, 0.006, 0.4, ph), alpha=alpha,
             flip=False)
        pc.rod(cr, x + dx, FL - 420 * s, x + dx + 30, H + 60, alpha=0.4 * alpha)


def s_n1(cr, t, tl, t0, t1):
    c = cues(tl, "n1")
    t_out = t0 + CARD_HOLD
    tD = max(c["D"], t_out + 0.5)
    tO = max(c["O"], tD + 1.2)
    tC = max(c["C"], tO + 0.3)
    sc = prog(t, t_out - 0.1, 0.6)
    trees(cr, t, sc)
    ground(cr, sc)
    fx, fs = FIRE
    if sc > 0:
        yajna_fire(cr, t, fx, FL, fs, 0.2, alpha=sc)
        cows(cr, t, sc)
    b, k, a = depth(t, t_out - 0.1, 0.6)
    give = keyed(t, [(t0, 0.0), (tD - 0.15, 1.0)], 0.35, 1.3)
    vp = vaja(cr, t, FATHER[0], FATHER[1] * k, front=mix((-0.4, -0.5), (-1.55, -0.2), give), backa=(0.3, -0.4),
              alpha=a, blur=b, ph=0.8, hits=[(tD, 0.3)])
    chapter(cr, t, t0 - 0.3, t_out, "STORY 5 OF 6",
            [[("THE CHILD WHO ASKED YAMA", INK)], [("THE SECRET OF", INK), ("DEATH", RED)]], "KATHA UPANISHAD")
    dev_f = vp["top"]
    dev_cow = cr.user_to_device(COWS[0][0] - 10, FL - 240)

    def ui(cr):
        if t > t_out:
            if t < tO:
                head2(cr, t, "A FATHER WAS GIVING AWAY", t_out + 0.1, "GIFTS", tD)
            else:
                head2(cr, t, "BUT HIS GIFTS WERE", tO - 0.15, "OLD, WEAK COWS", tO + 0.1, under=tC + 0.3)
            tag(cr, t, t_out + 0.4, "VAJASHRAVAS, THE FATHER", dev_f[0] + 40, dev_f[1] - 30, 30)
            if t > tO:
                red_ring(cr, dev_cow[0], dev_cow[1], 170, 110, prog(t, tO + 0.2, 0.45), 8)
    return dict(ui=ui, flash=flash_at(t, t_out, 0.2) + flash_at(t, tO, 0.15))


NACHI2 = (900, 0.4)


def s_n2(cr, t, tl, t0, t1):
    c = cues(tl, "n2")
    tN, tG, tP, tM = c["N"], c["G"], c["P"], c["M"]
    trees(cr, t)
    ground(cr)
    fx, fs = FIRE
    yajna_fire(cr, t, fx - 140, FL, 0.8, 0.1)
    cows(cr, t, 1.0, xs=((1250, 0.46, 0.0), (1690, 0.44, 1.3)))
    vp = vaja(cr, t, FATHER[0] - 60, FATHER[1], front=(-0.4, -0.5), backa=(0.3, -0.4), ph=0.8)
    x, s = NACHI2
    b, k, a = depth(t, tN - 0.3, 0.5)
    turn = t > tP - 0.1
    ask = keyed(t, [(t0, 0.0), (tM - 0.15, 1.0)], 0.3, 1.3)
    np_ = nachi(cr, t, x, s * k, mood="shame" if (tG - 0.1 < t < tP - 0.1) else "calm", flip=turn,
                front=mix((-0.3, -0.5), HEART["front"], ask), backa=(0.25, -0.3), head=0.08 * (tG < t < tP),
                alpha=a, blur=b, hits=[(tP, 0.4)], ph=0.2)
    dev_n = np_["top"]
    dev_f = vp["top"]

    def ui(cr):
        if t < tP:
            head2(cr, t, "HIS SON", t0 + 0.05, "NACHIKETA", tN)
        else:
            head2(cr, t, "FATHER, TO WHOM", tP - 0.1, "WILL YOU GIVE ME?", tM)
        tag(cr, t, tN + 0.2, "NACHIKETA", dev_n[0] - 230, dev_n[1] + 30, 38, t_out=tP - 0.1)
        if tG - 0.2 < t < tP + 0.2:
            cloud_text(cr, t, dev_n[0] + 270, dev_n[1] + 10, 0.44, [("OLD COWS?", 60, INK, -36, tG),
                                                                    ("THAT'S NOT RIGHT", 52, RED, 42, tG + 0.3)],
                       t_in=tG - 0.2, alpha=1 - prog(t, tP - 0.1, 0.3))
        if t > tM - 0.1:
            big_q(cr, t, tM, dev_n[0] - 140, dev_n[1] - 20, 110)
    return dict(ui=ui, flash=flash_at(t, tN, 0.15) + flash_at(t, tM, 0.2))


def s_n3(cr, t, tl, t0, t1):
    c = cues(tl, "n3")
    tC, tD, tT = c["C"], c["D"], c["T"]
    trees(cr, t)
    ground(cr)
    yajna_fire(cr, t, 200, FL, 0.8, 0.0)
    vp = vaja(cr, t, 620, 0.62, flip=True, front=(-0.25, -0.35), backa=(0.3, -0.3), head=0.06, ph=0.8)
    asks = (tD, tT)
    bob = 0.0
    for ta in asks:
        if 0 < t - ta < 0.4:
            bob = math.sin(math.pi * (t - ta) / 0.4)
    np_ = nachi(cr, t, 1100, 0.42, flip=True, front=mix((-0.6, -0.6), (-1.5, -0.3), bob), backa=(0.25, -0.3),
                head=-0.05 * bob, hits=[(tD, 0.4), (tT, 0.4)], ph=0.2)
    dev_f = vp["top"]
    dev_n = np_["top"]

    def ui(cr):
        head2(cr, t, "THE FATHER STAYED", t0 + 0.05, "SILENT", tC)
        dots_cloud(cr, t, tC, dev_f[0] - 250, dev_f[1] + 70, 0.42, flip=True)
        plate(cr, t, tC + 0.3, "HE TURNED AWAY", dev_f[0] - 250, dev_f[1] + 230, 28)
        if t > tD - 0.2:
            cloud_text(cr, t, dev_n[0] - 220, dev_n[1] + 20, 0.4, [("TO WHOM?", 70, INK, 0, tD)], flip=True,
                       t_in=tD - 0.2)
            counter_badge(cr, t, tD + 0.1, "x2" if t < tT else "x3", dev_n[0] + 170, dev_n[1] - 20, 96)
            if t > tT:
                counter_badge(cr, t, tT, "x3", dev_n[0] + 170, dev_n[1] - 20, 110)
    return dict(ui=ui, flash=flash_at(t, tD, 0.12) + flash_at(t, tT, 0.2))


def s_n4(cr, t, tl, t0, t1):
    c = cues(tl, "n4")
    tA, tJ, tY = c["A"], c["J"], c["Y"]
    trees(cr, t, 0.8)
    ground(cr)
    yajna_fire(cr, t, 170, FL, 0.8, 0.4 * prog(t, tA, 0.3))
    if t > tY - 0.3:                                          # far right: a dark shadow of Yama
        q = prog(t, tY - 0.3, 0.6)
        silhouette(cr, lambda c_: yama(c_, t, 1700, 0.5, flip=True, book=False, blur=6, rods=False), 0.55 * q)
    point = keyed(t, [(t0, 0.0), (tJ - 0.15, 1.0)], 0.25, 1.6)
    vp = vaja(cr, t, 560, 0.62, mood="angry" if t > tA - 0.2 else "calm",
              front=mix((-0.95, -1.9), (-1.6, 0.02), point), backa=mix((-0.85, -1.75), (0.6, -1.3), point),
              hits=[(tJ, 0.5), (tY, 0.3)], ph=0.8)
    recoil = keyed(t, [(t0, 0.0), (tJ, 1.0)], 0.2, 1.8)
    np_ = nachi(cr, t, 1050 + 70 * recoil, 0.42, mood="shock" if t > tJ else "calm", flip=True,
                front=mix((-0.6, -0.6), (-2.4, -0.9), recoil), backa=(-1.2, -1.0), rot=-0.06 * recoil,
                hits=[(tJ, 0.5)], ph=0.2)
    dev_f = vp["top"]
    mouth = cr.user_to_device(*local(560, FL - 434 * 0.62, 0.62, 0.0, False, 80, -370))

    def ui(cr):
        head2(cr, t, "THE FATHER SHOUTED IN ANGER:", t0 + 0.05, "TO YAMA!", tY, under=tY + 0.4)
        if t > tJ - 0.2:
            sound_rings(cr, mouth[0] + 40, mouth[1], t, tJ, 3, 0.3, 260, alpha=0.5)
            cloud_text(cr, t, dev_f[0] + 280, dev_f[1] + 100, 0.36, [("GO!", 120, RED, 16, tJ)], t_in=tJ - 0.2)
        if t > tY:
            plate(cr, t, tY + 0.2, "YAMA", 1700, 300, 34)
    return dict(ui=ui, eve=0.15 * prog(t, tY, 0.6), flash=flash_at(t, tJ, 0.2) + flash_at(t, tY, 0.3))


DOOR5 = (1640, 0.44)


def road(cr, t, x0, x1, a=1.0):
    """The road: a dotted path along the floor with a few stones."""
    if a <= 0.01:
        return
    dotted(cr, [(x0, FL + 40), (x1, FL + 30)], 1.0, 34, 6, (0.36, 0.22, 0.10), 0.7 * a)
    for i, x in enumerate(range(int(x0) + 60, int(x1), 190)):
        cr.new_path()
        pc.ell(cr, x + 30 * math.sin(i * 2.1), FL + 58, 18, 9)
        cr.set_source_rgba(0.30, 0.22, 0.16, 0.7 * a)
        cr.fill()


def dark_right(cr, a, x0=900, x1=1920):
    """Darkness thickening toward the right (the way to Yama's house)."""
    if a <= 0.01:
        return
    g = cairo.LinearGradient(x0, 0, x1, 0)
    g.add_color_stop_rgba(0, 0.03, 0.02, 0.06, 0.0)
    g.add_color_stop_rgba(1, 0.03, 0.02, 0.06, 0.7 * a)
    cr.save()
    cr.set_source(g)
    cr.paint()
    cr.restore()


def s_n5(cr, t, tl, t0, t1):
    c = cues(tl, "n5")
    tN, tY, tG = c["N"], c["Y"], c["G"]
    ground(cr)
    road(cr, t, 100, 1500)
    dx, ds = DOOR5
    glow(cr, dx, FL - 300, 420, 0.25)
    prop(cr, "sb_door", dx, FL + 6, ds)
    pc.rod(cr, dx - 200, FL - 300, dx - 160, H + 60, alpha=0.4)
    dark_right(cr, prog(t, t0, 1.5))
    np_, x = walking(nachi, cr, t, t0 - 0.2, max(t1 - 0.3, t0 + 2.4), 120, 1260, 0.38, step=0.46, ph=0.2,
                     front=(-0.3, -0.5))
    glow(cr, x, FL - 200, 240, 0.35)
    dev_d = cr.user_to_device(dx, FL - 1500 * ds - 10)

    def ui(cr):
        head2(cr, t, "AND NACHIKETA REALLY WENT TO", t0 + 0.05, "YAMA'S HOUSE", tY)
        tag(cr, t, tG, "YAMA'S DOOR", dev_d[0] - 320, dev_d[1] + 120, 36)
    return dict(ui=ui, night=0.12 + 0.18 * prog(t, t0, 2.5), lift=1.0, flash=flash_at(t, tY, 0.15))


DOOR6 = (1540, 0.44)


def bowl_cup(cr, t, t_in, x, y, alpha=1.0):
    """An empty bowl and an empty cup, each crossed out in red: no food, no water."""
    q = prog(t, t_in, 0.3) * alpha
    if q <= 0.01:
        return
    cr.save()
    cr.translate(x, y + 20 * (1 - q))
    cr.scale(1.4, 1.4)
    cr.set_source_rgba(0.62, 0.36, 0.16, q)
    cr.move_to(-150, -10)
    cr.curve_to(-150, 60, -30, 60, -30, -10)
    cr.close_path()
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, q)
    cr.set_line_width(4)
    cr.stroke()
    cr.set_source_rgba(0.62, 0.36, 0.16, q)
    pc.poly(cr, [(40, -40), (120, -40), (110, 46), (50, 46)])
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, q)
    cr.stroke()
    cr.restore()
    big_x(cr, x - 126, y + 14, 190, 150, prog(t, t_in + 0.3, 0.3), q)
    big_x(cr, x + 112, y + 6, 160, 160, prog(t, t_in + 0.5, 0.3), q)


def s_n6(cr, t, tl, t0, t1):
    c = cues(tl, "n6")
    tN, tT, tB, tD = c["N"], c["T"], c["B"], c["D"]
    ground(cr)
    dx, ds = DOOR6
    prop(cr, "sb_door", dx, FL + 6, ds)
    pc.rod(cr, dx - 200, FL - 300, dx - 160, H + 60, alpha=0.4)
    d1, d3 = tT, max(tD, tT + 1.8)
    days = (d1, (d1 + d3) / 2, d3)
    span = (d3 - d1) / 2 + 0.6
    # the sky: the sun and the moon cross the top once per day after DAY 1 shows
    night = 0.0
    if t > d1:
        k = min(2, int((t - d1) / span))
        u = ((t - d1) - k * span) / span
        sun_u = clamp(u * 2)
        moon_u = clamp(u * 2 - 1)
        if u < 0.5:
            ang = math.pi * (1 - sun_u)
            prop(cr, "sun", 900 + 640 * math.cos(ang), 640 - 280 * math.sin(ang), 0.36, rot=t * 0.2, alpha=0.8)
        else:
            ang = math.pi * (1 - moon_u)
            prop(cr, "moon", 900 + 640 * math.cos(ang), 640 - 280 * math.sin(ang), 0.5, alpha=0.8)
            night = 0.32 * math.sin(math.pi * moon_u)
    droop = clamp((t - d1) / (d3 - d1 + 1.0)) if t > d1 else 0.0
    np_ = nachi(cr, t, 1060, 0.4, mood="calm", sit=True, front=ANJALI["front"], backa=ANJALI["backa"],
                head=0.12 * droop, ph=0.2)
    glow(cr, 1060, FL - 160, 240, 0.3)
    dev_n = np_["top"]

    def ui(cr):
        if t < tB:
            head2(cr, t, "BUT YAMA WAS", t0 + 0.05, "NOT HOME", tN)
        else:
            head2(cr, t, "3 DAYS AT HIS DOOR...", tB - 0.15, "NO FOOD, NO WATER", tB + 0.05)
        if t > d1 - 0.2:
            k = sum(1 for d in days if t >= d)
            counter_badge(cr, t, days[max(0, k - 1)], f"DAY {max(1, k)}", 420, 460, 104)
        bowl_cup(cr, t, tB + 0.1, 600, 700)
    return dict(ui=ui, night=0.1 + night, lift=1.0, flash=flash_at(t, tN, 0.12) + flash_at(t, tB, 0.15))


def s_n7(cr, t, tl, t0, t1):
    c = cues(tl, "n7")
    tL, tS, tG, tB, tV = c["L"], c["S"], c["G"], c["B"], c["V"]
    ground(cr)
    prop(cr, "sb_door", 1720, FL + 6, 0.42, alpha=0.8, blur=3)
    np_ = nachi(cr, t, 560, 0.42, front=(-0.4, -0.5), backa=(0.25, -0.3), ph=0.2)
    shame = keyed(t, [(t0, 0.0), (tS - 0.1, 1.0), (tB - 0.2, 0.0)], 0.3, 1.2)
    give = keyed(t, [(t0, 0.0), (tB - 0.1, 1.0)], 0.3, 1.3)
    t_stop = max(tS - 0.2, t0 + 1.2)
    if t < t_stop:
        yp, yx = walking(yama, cr, t, t0 - 0.3, t_stop, 2150, 1260, 0.52, flip=True, book=False, ph=0.6,
                         front=(-0.4, -0.5))
    else:
        fr = mix(mix((-0.4, -0.5), HEART["front"], shame), (-2.3, -0.4), give)
        yp = yama(cr, t, 1260, 0.52, mood="shame" if shame > 0.5 else ("smile" if t > tB else "calm"), flip=True,
                  book=False, front=fr, head=0.14 * shame, rot=0.05 * shame, ph=0.6, hits=[(tB, 0.4)])
    glow(cr, 1260, FL - 380, 460, 0.35)
    if t > tV - 0.2:                                         # three glowing boons
        for i in range(3):
            q = prog(t, tV - 0.2 + 0.25 * i, 0.4)
            bx, by = 680 + 150 * i, 470 + 12 * math.sin(t * 2 + i)
            boon_token(cr, t, bx, by, q)
    dev_y = yp["top"]
    dev_b = [cr.user_to_device(680 + 150 * i, 470) for i in range(3)]

    def ui(cr):
        if t < tB:
            head2(cr, t, "YAMA CAME BACK AND FELT", t0 + 0.05, "ASHAMED", tS)
        else:
            head2(cr, t, "YAMA SAID:", tB - 0.15, "3 DAYS = 3 BOONS", tV, under=tV + 0.5)
        if tG - 0.2 < t < tB + 0.3:
            cloud_text(cr, t, dev_y[0] - 440, dev_y[1] + 70, 0.5, [("A GUEST, HUNGRY", 58, INK, -36, tG),
                                                                    ("FOR 3 DAYS!", 72, RED, 44, tG + 0.3)],
                       flip=True, t_in=tG - 0.2, alpha=1 - prog(t, tB, 0.3))
        for i, d in enumerate(dev_b):
            if t > tV - 0.2 + 0.25 * i:
                draw_text(cr, str(i + 1), d[0], d[1] + 3, 64, INK, prog(t, tV - 0.1 + 0.25 * i, 0.3), anchor="cm")
    return dict(ui=ui, flash=flash_at(t, tS, 0.12) + flash_at(t, tV, 0.25))


def small_pair(cr, t, boy_x=380, yama_x=1500, mood="calm", ymood="calm", boy_front=(-0.3, -0.5), yfront=(-0.4, -0.5),
               ynod=0.0, sit=False):
    glow(cr, boy_x, FL - 260, 300, 0.35)
    glow(cr, yama_x, FL - 360, 480, 0.7)
    warm(cr, yama_x, FL - 380, 300, 0.35)
    np_ = nachi(cr, t, boy_x, 0.4, mood=mood, front=boy_front, backa=(0.25, -0.3), ph=0.2, sit=sit)
    yp = yama(cr, t, yama_x, 0.5, mood=ymood, flip=True, book=False, front=yfront, nod=ynod, ph=0.6)
    return np_, yp


def s_n8(cr, t, tl, t0, t1):
    c = cues(tl, "n8")
    tC, tT, tA = c["C"], c["T"], c["A"]
    ground(cr)
    prop(cr, "sb_door", 1720, FL + 6, 0.42, alpha=0.5, blur=6)
    small_pair(cr, t, ynod=nods(t, (tC + 0.1, tA + 0.1), 0.5))

    def ui(cr):
        head2(cr, t, "NACHIKETA ASKED FOR:", t0 + 0.05, None, 0.0)
        q = prog(t, tC - 0.3, 0.3)
        if q > 0:                                         # the father's face, calm again
            glow(cr, 640, 400, 160, 0.5 * q)
            prop(cr, "sb_vaja_head_smile", 640, 480, 0.62 * (0.7 + 0.3 * q), alpha=q)
        boon_card(cr, t, t0 + 0.15, 1010, 400, 0.72, "BOON 1", [("FATHER'S ANGER", INK), ("CALMED", RED)],
                  t_tick=tC + 0.2)
        if t > tT - 0.2:
            q = prog(t, tA - 0.3, 0.3)
            if q > 0:                                     # the sacred fire
                glow(cr, 640, 640, 180, 0.6 * q)
                prop(cr, "altar", 640, 760, 0.5, alpha=q)
                prop(cr, f"flame{int(t * 10) % 3}", 640, 730, 0.4 * (0.7 + 0.3 * q), alpha=q)
            boon_card(cr, t, tT - 0.15, 1010, 690, 0.72, "BOON 2", [("THE FIRE THAT", INK), ("LEADS TO HEAVEN", RED)],
                      t_tick=tA + 0.25)
    return dict(ui=ui, flash=flash_at(t, tC, 0.12) + flash_at(t, tA, 0.15))


def s_n9(cr, t, tl, t0, t1):
    c = cues(tl, "n9")
    tT, tM, tQ = c["T"], c["M"], c["Q"]
    ground(cr)
    prop(cr, "sb_door", 1720, FL + 6, 0.42, alpha=0.5, blur=6)
    small_pair(cr, t, boy_front=(-1.3, -0.6))

    def ui(cr):
        head2(cr, t, "AND THE THIRD BOON:", t0 + 0.05, "WHAT HAPPENS AFTER DEATH?", tM, under=tQ + 0.2)
        for i, (x, num, lines) in enumerate(((620, "BOON 1", [("FATHER'S ANGER", INK), ("CALMED", RED)]),
                                             (1300, "BOON 2", [("THE FIRE THAT", INK), ("LEADS TO HEAVEN", RED)]))):
            boon_card(cr, t, -10.0, x, 790, 0.36, num, lines, alpha=0.8, t_tick=-10.0)
        q = back(clamp((t - tT + 0.1) / 0.4), 1.4)
        if q > 0:
            yy = 470 + 60 * (1 - q)
            for sx in (-1, 1):
                pc.rod(cr, 960 + sx * 300, yy + 170, 960 + sx * 260, H + 60, alpha=0.5 * clamp(q))
            cr.save()
            cr.translate(960, yy)
            cr.rotate(sway(t, 0.008, 0.4))
            cr.scale(0.95, 0.95)
            pc.paint_part(cr, "card", clamp(q))
            draw_text(cr, "BOON 3", 0, -140, 46, RED, clamp(q), MONO_FONT, "cm", tracking=8)
            cr.restore()
            body_outline(cr, 820, yy + 165, 280, prog(t, tM, 0.6), clamp(q))
            soul_light(cr, t, 820, yy + 165 - 0.62 * 280, 26, prog(t, tM + 0.3, 0.4))
            big_q(cr, t, tQ, 1110, yy + 20, 230)
    return dict(ui=ui, flash=flash_at(t, tM, 0.15) + flash_at(t, tQ, 0.2))


GIFTS = (("gold", 500, "GOLD"), ("horses", 720, "HORSES"), ("elephants", 960, "ELEPHANTS"), ("land", 1190, "LAND"),
         ("years", 1395, "100 YEARS"))


def s_n10(cr, t, tl, t0, t1):
    c = cues(tl, "n10")
    tT, tM, tB, tG, tH, tE, tL, tY = c["T"], c["M"], c["B"], c["G"], c["H"], c["E"], c["L"], c["Y"]
    ground(cr)
    prop(cr, "sb_door", 1760, FL + 6, 0.42, alpha=0.4, blur=8)
    stop = keyed(t, [(t0, 0.0), (tM - 0.15, 1.0), (tB - 0.1, 0.0)], 0.3, 1.3)
    offer = keyed(t, [(t0, 0.0), (tB - 0.1, 1.0)], 0.3, 1.3)
    yf = mix(mix((-0.4, -0.5), (-2.1, -0.9), stop), (-1.5, -0.2), offer)
    np_, yp = small_pair(cr, t, boy_x=300, yama_x=1620, yfront=yf)
    labels = []
    order = sorted(zip(GIFTS, (tG, tH, tE, tL, tY)), key=lambda g: g[0][0] != "land")
    for (kind, x, lab), ti in order:
        r = gift(cr, t, kind, x, ti - 0.35)
        if r:
            labels.append((lab, cr.user_to_device(x, FL + 66), ti))
    dev_y = yp["top"]

    def ui(cr):
        if t < tB:
            head2(cr, t, "YAMA TRIED TO", t0 + 0.05, "AVOID IT", tT + 0.2)
        else:
            head2(cr, t, "YAMA SAID:", tB - 0.15, "TAKE THESE INSTEAD", tB + 0.1)
        if t < tB + 0.4:
            cloud_text(cr, t, dev_y[0] - 330, dev_y[1] + 40, 0.48, [("DON'T ASK", 70, INK, -36, tM),
                                                                     ("THIS!", 90, RED, 46, tM + 0.25)],
                       flip=True, t_in=tM - 0.2, alpha=1 - prog(t, tB + 0.1, 0.3))
        for lab, (lx, ly), ti in labels:
            plate(cr, t, ti + 0.1, lab, lx, ly, 30)
    return dict(ui=ui, flash=flash_at(t, tM, 0.12) + flash_at(t, tB, 0.15))


def s_n11(cr, t, tl, t0, t1):
    c = cues(tl, "n11")
    tE, tD, tK, tJ = c["E"], c["D"], c["K"], c["J"]
    ground(cr)
    prop(cr, "sb_door", 1760, FL + 6, 0.42, alpha=0.4, blur=8)
    push = keyed(t, [(t0, 0.0), (t0 + 0.4, 1.0)], 0.3, 1.4)
    np_, yp = small_pair(cr, t, boy_x=300, yama_x=1620, boy_front=mix((-0.3, -0.5), PUSH["front"], push),
                         yfront=(-1.5, -0.2))
    grey = prog(t, tE, 0.8)
    t_back = tK - 0.1
    for i, (kind, x, lab) in sorted(enumerate(GIFTS), key=lambda g: g[1][0] != "land"):
        gift(cr, t, kind, x, -10.0, t_back=t_back + 0.1 * i, grey=grey)
    gift(cr, t, "drum", 1020, tD - 0.3, t_back=t_back + 0.5)
    if t > tJ - 0.2:
        glow(cr, 960, 560, 300, 0.4 * prog(t, tJ - 0.2, 0.4))

    def ui(cr):
        if t < tK:
            head2(cr, t, "NACHIKETA SAID:", t0 + 0.05, "ALL THIS WILL END ONE DAY", tE)
        else:
            head2(cr, t, "KEEP THEM.", tK - 0.15, "I WANT THE ANSWER.", tJ, under=tJ + 0.5)
        if t > tE and t < tK:
            plate(cr, t, tE + 0.3, "IT WON'T LAST", 960, 600, 34, t_out=tK - 0.2)
        if t > tJ:
            big_q(cr, t, tJ + 0.1, 960, 520, 200)
    return dict(ui=ui, flash=flash_at(t, tE, 0.12) + flash_at(t, tJ, 0.2))


SOUL12 = (960, FL)


def s_n12(cr, t, tl, t0, t1):
    c = cues(tl, "n12")
    tK, tA, tN, tS, tX = c["K"], c["A"], c["N"], c["S"], c["X"]
    ground(cr)
    prop(cr, "sb_door", 1760, FL + 6, 0.42, alpha=0.4, blur=8)
    teach = keyed(t, [(t0, 0.0), (tA - 0.1, 1.0)], 0.3, 1.3)
    glow(cr, 400, FL - 200, 280, 0.35)
    glow(cr, 1500, FL - 360, 480, 0.7)
    warm(cr, 1500, FL - 380, 300, 0.35)
    nachi(cr, t, 400, 0.4, sit=True, front=ANJALI["front"], backa=ANJALI["backa"], ph=0.2)
    yp = yama(cr, t, 1500, 0.5, mood="smile" if t < tA else "teach", flip=True, book=False,
              front=mix((-0.4, -0.5), (-1.3, -0.4), teach), ph=0.6, hits=[(tK, 0.3)])
    x, feet = SOUL12
    hgt = 470
    crumble = prog(t, tS + 0.1, 1.4)
    oa = prog(t, t0 + 0.3, 0.5)
    body_outline(cr, x, feet, hgt, prog(t, t0 + 0.2, 0.8), oa, crumble, t)
    rise = ease((t - tS - 0.1) / 1.6) if t > tS else 0.0
    sy = feet - hgt * 0.62 - 230 * rise
    soul_light(cr, t, x, sy, 22 + 8 * prog(t, tA, 0.5) + 6 * rise, prog(t, t0 + 0.4, 0.5))
    if t > tA:
        glow(cr, x, sy, 260 + 80 * rise, 0.5 * prog(t, tA, 0.5))
    dev_s = cr.user_to_device(x, sy)
    dev_b = cr.user_to_device(x + 90, feet - 160)

    def ui(cr):
        if t < tA:
            head2(cr, t, "YAMA WAS PLEASED, AND TAUGHT:", t0 + 0.05, None, 0.0)
        elif t < tS:
            head2(cr, t, "THE SOUL IS", tA - 0.15, "NEVER BORN, NEVER DIES", tN)
        else:
            head2(cr, t, "THE BODY DIES,", tS - 0.15, "THE SOUL DOES NOT", tX, under=tX + 0.4)
        plate(cr, t, tA + 0.1, "SOUL", dev_s[0] + 150, dev_s[1] - 30, 32)
        plate(cr, t, t0 + 0.6, "BODY", dev_b[0] + 60, dev_b[1], 30, t_out=tS + 0.8)
        if t > tX:
            red_ring(cr, dev_s[0], dev_s[1], 110, 110, prog(t, tX + 0.05, 0.45), 8)
    return dict(ui=ui, night=0.12, lift=1.0, flash=flash_at(t, tA, 0.15) + flash_at(t, tS, 0.15))


VERSE = "न जायते म्रियते वा"
VERSE_LATIN = "NA JAYATE MRIYATE VA"


def verse_leaf(cr, t, t_in, x, y, s, title, t_ring=None, alpha=1.0):
    """A palm leaf (lr_bigleaf) with a title (the text and verse), the verse's first words (Devanagari when the font
    is there) and their meaning in small English."""
    q = back(clamp((t - t_in) / 0.4), 1.3)
    a = clamp(q) * alpha
    if a <= 0.01:
        return None
    yy = y + 50 * (1 - q)
    r = sway(t, 0.005, 0.4, x * 0.01) - 0.01
    pc.rod(cr, x + 360 * s, yy + 150 * s, x + 400 * s, H + 60, alpha=0.5 * a)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(r)
    cr.scale(s, s)
    pc.paint_part(cr, "lr_bigleaf", a)
    draw_text(cr, title, 0, -118, 44, (0.62, 0.12, 0.08), a, MONO_FONT, "cm", tracking=5)
    draw_text(cr, "(NOT BORN, DOES NOT DIE)", 0, 118, 34, FADE, a, MONO_FONT, "cm", tracking=3)
    cr.restore()
    vy = yy + 6 * s
    if HAS_INDIC:
        su = indic_surface(VERSE, int(110 * s), INK)
        cr.set_source_surface(su, x - su.get_width() / 2, vy - su.get_height() / 2)
        cr.paint_with_alpha(a)
        vw = su.get_width()
    else:
        _, _, vw, _ = draw_text(cr, VERSE_LATIN, x, vy, int(90 * s), INK, a, anchor="cm")
    if t_ring is not None and t > t_ring:
        red_ring(cr, x, vy, vw / 2 + 34, 78 * s, prog(t, t_ring, 0.45), 7, a)
    return vy


def s_n13(cr, t, tl, t0, t1):
    c = cues(tl, "n13")
    tQ, tC, tK, tG, tW = c["Q"], c["C"], c["K"], c["G"], c["W"]
    ground(cr)
    fade_soul = 1 - prog(t, tC, 0.6)
    if fade_soul > 0:
        soul_light(cr, t, 960, 600, 40, fade_soul)
        body_outline(cr, 960, FL, 420, 1.0, 0.5 * fade_soul)
    if t > tK - 0.4:
        b, k, a = depth(t, tK - 0.4, 0.6)
        glow(cr, 470, FL - 300, 420, 0.4 * a)
        ch = chariot(cr, t, 300, FL + 2, 0.36 * k, ar=dict(head=0.05), kr=dict(flip=True, front=(-1.35, -0.4)),
                     alpha=a, blur=b)
        dev_c = (450, 330)
    else:
        dev_c = None

    def ui(cr):
        if t < tC:
            head2(cr, t, "DOES THIS SOUND", t0 + 0.05, "FAMILIAR?", tQ)
        elif t < tW:
            head2(cr, t, "CENTURIES LATER, IN THE GITA...", tC - 0.1, None, 0.0)
        else:
            head2(cr, t, "KRISHNA SAID TO ARJUNA", tW - 0.2, "ALMOST THE SAME WORDS", tW, under=tW + 0.5)
        if t < tC + 0.3:
            big_q(cr, t, tQ, 1240, 560, 240, alpha=1 - prog(t, tC, 0.3))
        if dev_c is not None:
            tag(cr, t, tK + 0.2, "KRISHNA AND ARJUNA", dev_c[0], dev_c[1], 30)
        if t > tG - 0.3:
            y1 = verse_leaf(cr, t, tG - 0.3, 1380, 400, 0.6, "KATHA UPANISHAD 1.2.18", t_ring=tW + 0.1)
            y2 = verse_leaf(cr, t, tG, 1380, 690, 0.6, "BHAGAVAD GITA 2.20", t_ring=tW + 0.3)
            if y1 and y2 and t > tW + 0.4:
                q = prog(t, tW + 0.4, 0.3)
                draw_text(cr, "=", 1040, (y1 + y2) / 2, int(160 * (1.2 - 0.2 * q)), RED, q, MONO_FONT, "cm")
    return dict(ui=ui, flash=flash_at(t, tG, 0.15) + flash_at(t, tW, 0.2))


# ------------------------------------------------------------------ the shot list and the frame


SHOTS = [   # (line, draw function, options) - one shot per line; "cont" = same set as the line before (no lamp dip)
    ("m1", s_m1, {"z": (1.0, 1.02)}),
    ("m2", s_m2, {"z": (1.0, 1.03)}),
    ("m3", s_m3, {"z": (1.0, 1.03), "cont": True}),
    ("m4", s_m4, {"z": (1.03, 1.05), "cont": True}),
    ("m5", s_m5, {"z": (1.0, 1.04)}),
    ("m6", s_m6, {"z": (1.0, 1.05), "focus": (960, 520)}),
    ("m7", s_m7, {"z": (1.0, 1.03)}),
    ("m8", s_m8, {"z": (1.0, 1.03)}),
    ("m9", s_m9, {"z": (1.03, 1.06), "cont": True}),
    ("m10", s_m10, {"z": (1.0, 1.03), "cont": True}),
    ("m11", s_m11, {"z": (1.0, 1.04), "cont": True}),
    ("m12", s_m12, {"z": (1.0, 1.03), "cont": True}),
    ("m13", s_m13, {"z": (1.0, 1.04), "cont": True}),
    ("m14", s_m14, {"z": (1.0, 1.04), "cont": True}),
    ("n1", s_n1, {"z": (1.0, 1.02)}),
    ("n2", s_n2, {"z": (1.0, 1.03), "cont": True}),
    ("n3", s_n3, {"z": (1.02, 1.05)}),
    ("n4", s_n4, {"z": (1.0, 1.04), "cont": True}),
    ("n5", s_n5, {"z": (1.0, 1.03)}),
    ("n6", s_n6, {"z": (1.0, 1.03)}),
    ("n7", s_n7, {"z": (1.0, 1.03)}),
    ("n8", s_n8, {"z": (1.0, 1.02), "cont": True}),
    ("n9", s_n9, {"z": (1.0, 1.03), "cont": True}),
    ("n10", s_n10, {"z": (1.0, 1.02), "cont": True}),
    ("n11", s_n11, {"z": (1.0, 1.03), "cont": True}),
    ("n12", s_n12, {"z": (1.0, 1.04)}),
    ("n13", s_n13, {"z": (1.0, 1.03)}),
]
_IDX = {bid: k for k, (bid, _, _) in enumerate(SHOTS)}


def shot_at(t, tl):
    """(shot index, start, end) for the line active at t: a shot runs from its line's start to the next line's start
    (the pause after a line belongs to it). Cached on the timeline under this module's own name."""
    spans = getattr(tl, "_s6b_spans", None)
    if spans is None:
        spans = {}
        for i, b in enumerate(tl.beats):
            if b.id in _IDX:
                spans[b.id] = (b.start, tl.beats[i + 1].start if i + 1 < len(tl.beats) else tl.total)
        tl._s6b_spans = spans
    bid = None
    for b in tl.beats:
        if b.start <= t:
            bid = b.id
        else:
            break
    if bid not in _IDX:                       # (only when called outside its lines: the nearest of mine)
        bid = min(spans, key=lambda k: abs(spans[k][0] - t))
    return _IDX[bid], spans[bid][0], spans[bid][1]


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl)
    _, fn, opt = SHOTS[k]
    z0, z1 = opt.get("z", (1.0, 1.03))
    z = z0 + (z1 - z0) * clamp((t - t0) / max(0.5, t1 - t0))
    fx, fy = opt.get("focus", (960, 640))
    cr.save()
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    stage(cr)
    out = fn(cr, t, tl, t0, t1) or {}
    tint(cr, (1.0, 0.66, 0.42), out.get("eve", 0.0))
    tint(cr, (0.74, 0.80, 1.0), out.get("cool", 0.0))
    cr.restore()
    motes(cr, t)
    lamp(cr, t, night=out.get("night", 0.0), flash=out.get("flash", 0.0))
    title_lift(cr, out.get("lift", 0.0) * min(1.0, 2.5 * out.get("night", 0.0)))
    if out.get("ui"):
        out["ui"](cr)
    if not opt.get("cont") and t - t0 < 0.22:      # the lamp dips for a moment on a change of scene
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur) for story 2 and story 5 only, sparse (owner, 8 Nov 2026: "only use sounds where necessary"):
    a damaru on each chapter card, a conch on Mandavya's new rule, shimmer as Yama becomes Vidura, a bell on Yama's
    three boons, shimmer on the soul that never dies; bed dips before the reveals (he did not die; Yama born as Vidura;
    the road to Yama's house; the soul). render_myth.calm_sfx keeps sounds >= SFX_MIN_GAP apart over the whole video."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(c["m1"]["t0"] + 0.05, "damaru", 0), (c["m12"]["R"], "conch", 0), (c["m14"]["J"] + 0.5, "shimmer", 0),
            (c["n1"]["t0"] + 0.05, "damaru", 0), (c["n7"]["V"], "bell", 0), (c["n12"]["A"], "shimmer", 0)]
    dips = [(c["m6"]["t0"] - 0.3, "dip", 0.5), (c["m14"]["J"] - 0.3, "dip", 0.5), (c["n5"]["t0"] - 0.3, "dip", 0.5),
            (c["n12"]["A"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(want + dips)]
