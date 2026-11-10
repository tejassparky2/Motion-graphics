"""Scenes for builder A's parts of the long video videos/six_stories.py (landscape 1920x1080): the intro (i1-i8), story
1 Kacha (k1-k17), story 6 Yayati (y1-y15) and the outro (o1-o2). scenes_six_stories routes every moment whose active
line is i*, k*, y* or o* here; draw() paints the whole frame.

Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code, as in the reels: a lamp-lit cloth (a wide
landscape version of puppet_core.screen, the lamp in the middle), translucent punched-leather puppets on rods
(six_cast_a plus the older casts) that move with the quick, swinging rhythm of rod puppets and then hold, two-tier
English headlines at the top centre (a small dark setup line, one big red key line). Long-form pace: a visible change
every 2-3 s. Explained so a child can follow: one plain label per step.

Respect: gods, sages and kings keep their dignity. No gore at all: the killings are a cut-away (the lamp goes dark, a
flash, the asuras walk off), the fire is only a fire, Kacha comes out of his guru in a burst of light, Devayani drops
out of sight into the well, nobody is hurt on screen. Faces are leather puppets, no actor likeness.

Every frame is a pure function of t. Cues are words of the line in the timeline's language (Hindi: CUES, Kannada:
CUES_KN) with a fraction fallback and minimum gaps. All on-screen words are English, shared by both languages.

Shot list (line: what is on the screen)
  i1-i6 INTRO: one big framed shadow panel per claim, numbered (a row of six numbered medallions below fills up), each
        sliding in over the last, with its headline (small setup + big red key):
        1 Shukra's silhouette, a glowing x-ray belly with tiny Kacha inside, a speech cloud GURUJI!: A STUDENT SPOKE
          FROM INSIDE / HIS GURU'S STOMACH
        2 a sage points at crowned Yama with his staff, a crack of red light: A SAGE / PUNISHED YAMA
        3 a sage on a rock, the sea pouring up into his mouth, the sea level dropping: A SAGE DRANK / THE WHOLE OCEAN
        4 a boy with a small horn in the forest, a doe beside him, a red "?": A BOY WHO HAD / NEVER SEEN A WOMAN
        5 a child before a tall dark door with a red glow inside, "?": A CHILD ASKED YAMA / THE SECRET OF DEATH
        6 a bent old man and a young man, a glow passing from the son to the father, who straightens as the son bends:
          A FATHER TOOK / HIS SON'S YOUTH
  i7    three palm-leaf books rise and open as named: MAHABHARATA (stories 1 2 3 4 6), RAMAYANA (4), UPANISHAD (5):
        ALL SIX STORIES ARE / IN OUR TEXTS
  i8    WATCH TILL / THE END; small panels 1 and 6, Devayani's silhouette with a red "?", a dotted arc from panel 1 to
        panel 6: THE GIRL FROM STORY 1 / RETURNS IN STORY 6
  k1    chapter card STORY 1 OF 6, THE STUDENT WHO SPOKE FROM HIS GURU'S STOMACH, MAHABHARATA · ADI PARVA; then gods
        (rayed crowns, gold light) against horned asuras (red light), silhouettes clashing: A WAR: / GODS VS ASURAS
  k2    Shukra (tag) with his staff: THE ASURAS' GURU: / SHUKRACHARYA; a glowing leaf SANJIVANI: HIS SECRET POWER: /
        SANJIVANI; a fallen asura lies on the right; Shukra raises his hand, light flows, a burst, the asura stands
        again: SANJIVANI: / BRINGS THE DEAD BACK
  k3    the gods' camp, small golden Brihaspati (tag): the leaf SANJIVANI crossed out: THE GODS DIDN'T KNOW /
        SANJIVANI; Kacha appears (tag): THEIR GURU'S SON: / KACHA; he turns and walks off toward a far Shukra along a
        dotted path: THE GODS SENT A / SPY STUDENT
  k4    Kacha bows to Shukra, then serves him water: KACHA BECAME / SHUKRA'S STUDENT; Devayani comes in (tag):
        THE GURU'S DAUGHTER: / DEVAYANI; she smiles, flowers drift: AND DEVAYANI / LIKED HIM
  k5    night forest, Kacha alone; horned asura silhouettes close in: THE ASURAS FOUND OUT / HIS PLAN; cut-away: the
        lamp goes dark, a flash; Kacha is gone, the asuras walk off, wolves slink in: KILLED... / FED TO WOLVES
  k6    Devayani weeps: DEVAYANI / WEPT; Shukra calls out (sound rings): SHUKRA CALLED OUT: / KACHA!; a burst of
        light among the wolves, they run, Kacha steps out of the light: KACHA CAME OUT / ALIVE AGAIN
  k7    the sea; asuras throw a dark cloud into it, a splash: KILLED AGAIN... / INTO THE SEA; Shukra raises his hand,
        a column of light, Kacha rises out of the water: KILLED AGAIN... / ALIVE AGAIN
  k8    THE THIRD TIME: / A TRICK (stamp 3RD TIME); a fire flares, its ashes rise into a wine cup an asura holds,
        he carries it to Shukra, who drinks: ASHES IN THE / GURU'S WINE
  k9    Shukra; an x-ray belly glows, tiny Kacha inside (tag): NOW KACHA WAS / INSIDE THE GURU
  k10   Devayani weeps, Shukra calls: DEVAYANI WEPT AGAIN. / SHUKRA CALLED KACHA; a speech cloud from the belly
        GURUJI, / I'M IN YOUR STOMACH!: THEN A VOICE CAME FROM / INSIDE
  k11   a balance: tiny Kacha in one pan, tiny Shukra in the other; KACHA OUT (the pan rises) / GURU DIES (the pan
        sinks, glows red): BUT HERE WAS / THE PROBLEM
  k12   Shukra, eyes shut, whispers to his own belly: lines of light curl inward, a leaf SANJIVANI points in, tiny
        Kacha lights up: SO HE TAUGHT HIM / INSIDE
  k13   a burst of light from the belly, Kacha stands beside him: A BURST OF LIGHT: / KACHA WAS OUT; Shukra falls:
        BUT THE GURU / FELL; Kacha's glowing hands, light flows, Shukra rises: THE STUDENT / SAVED HIS GURU
  k14   Shukra raises his hand over an overturned wine cup (red X): THAT DAY, SHUKRA MADE / A NEW RULE; card NEW RULE:
        NO WINE FOR BRAHMINS
  k15   Devayani offers a garland: DEVAYANI WANTED TO / MARRY KACHA; Kacha steps back, palm up: BUT KACHA SAID: / NO;
        his speech cloud BORN AGAIN FROM / YOUR FATHER'S BODY... / YOU ARE MY SISTER
  k16   both point, sparks crackle between them: IN ANGER, BOTH / CURSED EACH OTHER; card KACHA'S CURSE: NO SAGE'S SON
        / WILL MARRY YOU
  k17   the card freezes, a red pin pins it: REMEMBER / THIS CURSE; leaf IT RETURNS IN STORY 6
  y1    chapter card STORY 6 OF 6, THE FATHER WHO TOOK HIS SON'S YOUTH, MAHABHARATA · ADI PARVA; Devayani returns
        (tag): REMEMBER / DEVAYANI?; the pinned curse card flashes back
  y2    Sharmishtha (tag): THE ASURA PRINCESS: / SHARMISHTHA; they argue: DEVAYANI AND SHARMISHTHA / FOUGHT; a push,
        Devayani topples back into the well and drops out of sight, a splash: PUSHED INTO / A WELL
  y3    King Yayati walks up (tag): THEN CAME / KING YAYATI; he reaches down and pulls her out by the hand: HE PULLED
        HER OUT / BY THE HAND
  y4    holding his hand: DEVAYANI SAID: YOU HELD MY HAND, SO / MARRY ME!; YAYATI WAS / A KING, NOT A SAGE'S SON; the
        pinned curse card gets a red tick: SO KACHA'S CURSE / CAME TRUE
  y5    a door swings shut; Yayati and Sharmishtha in a warm light: YAYATI ALSO MARRIED SHARMISHTHA, / IN SECRET; three
        little sons appear: AND HAD / SONS WITH HER
  y6    Devayani sees them far off (red "!"): DEVAYANI / FOUND OUT; she runs, crying, to Shukra: SHE RAN, CRYING, /
        TO HER FATHER
  y7    Shukra points, a crack of light: SHUKRA CURSED / YAYATI; a flash and Yayati is old, white-haired, bent, a
        stick: SHUKRA'S CURSE: / OLD... RIGHT NOW!
  y8    BUT THERE WAS / ONE WAY OUT; card UNLESS SOMEONE / TAKES YOUR OLD AGE
  y9    old Yayati asks: YAYATI ASKED HIS SONS: / GIVE ME YOUR YOUTH; four son silhouettes shake their heads one by
        one, a NO over each: FOUR SONS SAID / NO
  y10   the youngest lights up and steps forward (tag PURU, THE YOUNGEST): THE YOUNGEST SON, / PURU; offering his
        hands: PURU SAID: / TAKE MY YOUTH
  y11   a glow swaps: Yayati young, Puru old; a counter ticks to 1000 YEARS: FATHER YOUNG, SON OLD: / FOR 1000 YEARS
  y12   young Yayati thinks: AFTER 1000 YEARS, YAYATI SAID: / DESIRE NEVER ENDS; ghee poured on a fire, it flares:
        DESIRE NEVER ENDS: / LIKE FIRE WITH GHEE
  y13   the glow swaps back: YAYATI GAVE BACK / PURU'S YOUTH; a crown drops onto Puru (tag KING PURU): AND MADE PURU /
        KING
  y14   AND NOW, THE BIGGEST / TWIST; a family tree grows from PURU through KURU to small Pandavas (Yudhishthira, Bhima,
        Arjuna) and Kaurava silhouettes: PURU'S LINE: / PANDAVAS & KAURAVAS
  y15   AND YADU, WHO SAID / NO; another branch grows from YADU down to a small Krishna: YADU'S LINE: / KRISHNA
  o1    the six panels in a grid, each lighting up (name plaque) as it is named: SO THESE WERE / SIX TRUE STORIES
  o2    big numbers 1-6 on the panels, a red ring hopping between them: WHICH ONE SHOCKED YOU MOST? / COMMENT 1-6
"""
import bisect
import functools
import math

import cairo
import numpy as np

import jayadratha_cast as J
import mandhata_cast as M
import puppet_cast as C
import puppet_core as pc
import ravana_cast as R
import six_cast_a as X
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, text_size, tick
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_arjuna import card2, cloud_text, yudh
from scenes_jarasandha import (INK, LIGHT, RED, big_word, bob_rot, fit, glow, motes, red_ring, small_line, stamp,
                               walk_legs, woman_angles)
from scenes_jayadratha import SIL, flash_at, shroud, silhouette, tag, tint, to_user
from scenes_kaikeyi import ANJALI, balance, fig, leaf_tag, plaque, settle
from scenes_lakshman_rekha import big_x, book, deer, partial, sparkle
from scenes_mandhata import aura, beam, burst, held, lights, mix, reach_arm, warm
from scenes_ravana import dotted
from scenes_ruru import flow, held_grip, petals, rishi, yama
from shots import T

MISSES = set()                       # cue words not found in a line (falls back to fractions)
FLOOR = 892                          # the stage floor (feet), as scenes_six_b
SM, SW = 0.57, 0.6                   # a standing man's / woman's scale on the stage
NIGHT = 0.42
OFFER = dict(front=(-1.3, -0.3), backa=(-1.2, -0.45))           # both hands held out in front
WEEP = dict(front=(-0.62, -2.55), backa=(-0.5, -2.35))          # hands to the face
HEART = dict(front=(-0.3, -2.45), backa=(0.12, -0.25))
GOLDC = (1.0, 0.86, 0.45)
COOL = (0.62, 0.90, 1.0)


# ------------------------------------------------------------------ cues


def cue(tl, bid, word, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, word)
    except (KeyError, ValueError):
        MISSES.add((bid, word))
        return T(tl, bid, frac)


# Every cue of every line: (name, Hindi word, fraction fallback, ((after, min gap), ...)); "t0" = the line's start.
# Words are exact substrings of the script lines (MISSES stays empty).
CUES = {
    "i1": (("S", "शिष्य", 0.3, (("t0", 0.4),)), ("P", "पेट", 0.6, (("S", 0.5),)), ("B", "बोला", 0.88, (("P", 0.4),))),
    "i2": (("R", "ऋषि", 0.1, ()), ("Y", "यमराज", 0.45, (("R", 0.5),)), ("Z", "सज़ा", 0.7, (("Y", 0.4),))),
    "i3": (("R", "ऋषि", 0.1, ()), ("S", "समुद्र", 0.5, (("R", 0.5),)), ("P", "पी", 0.75, (("S", 0.3),))),
    "i4": (("L", "लड़का", 0.1, ()), ("A", "औरत", 0.55, (("L", 0.6),)), ("N", "नहीं", 0.85, (("A", 0.3),))),
    "i5": (("C", "बच्चा", 0.1, ()), ("Y", "यमराज", 0.3, (("C", 0.5),)), ("M", "मौत", 0.6, (("Y", 0.5),)),
           ("Q", "पूछ", 0.85, (("M", 0.4),))),
    "i6": (("F", "पिता", 0.15, ()), ("B", "बेटे", 0.55, (("F", 0.5),)), ("J", "जवानी", 0.75, (("B", 0.3),))),
    "i7": (("C", "छह", 0.05, ()), ("S", "सच", 0.3, (("C", 0.6),)), ("M", "महाभारत", 0.55, (("S", 0.5),)),
           ("R", "रामायण", 0.72, (("M", 0.6),)), ("U", "उपनिषद", 0.88, (("R", 0.6),))),
    "i8": (("D", "देखना", 0.15, ()), ("P", "पहली", 0.3, (("D", 0.3),)), ("L", "लड़की", 0.5, (("P", 0.4),)),
           ("A", "आख़िरी", 0.65, (("L", 0.5),)), ("F", "आएगी", 0.9, (("A", 0.4),))),
    "k1": (("D", "देवताओं", 0.35, (("t0", 0.9),)), ("A", "असुरों", 0.55, (("D", 0.4),)),
           ("L", "लड़ाई", 0.75, (("A", 0.3),))),
    "k2": (("S", "शुक्राचार्य", 0.14, (("t0", 0.4),)), ("V", "विद्या", 0.3, (("S", 0.6),)),
           ("N", "संजीवनी", 0.42, (("V", 0.4),)), ("D", "मरे", 0.6, (("N", 0.8),)),
           ("Z", "ज़िंदा", 0.85, (("D", 0.9),))),
    "k3": (("N", "नहीं", 0.25, (("t0", 0.6),)), ("B", "बृहस्पति", 0.5, (("N", 0.8),)), ("K", "कच", 0.68, (("B", 0.5),)),
           ("S", "भेजा", 0.92, (("K", 0.8),))),
    "k4": (("W", "शिष्य", 0.2, (("t0", 0.4),)), ("V", "सेवा", 0.42, (("W", 0.6),)),
           ("D", "देवयानी", 0.65, (("V", 0.6),)),
           ("L", "पसंद", 0.82, (("D", 0.5),))),
    "k5": (("U", "समझ", 0.08, ()), ("M", "मार", 0.55, (("U", 1.6),)), ("W", "भेड़ियों", 0.82, (("M", 1.0),))),
    "k6": (("C", "रोने", 0.1, ()), ("P", "पुकारा", 0.45, (("C", 0.9),)), ("Z", "ज़िंदा", 0.8, (("P", 1.0),))),
    "k7": (("M", "मारा", 0.15, ()), ("P", "पीसकर", 0.35, (("M", 0.5),)), ("S", "समुद्र", 0.45, (("P", 0.5),)),
           ("G", "गुरु", 0.75, (("S", 0.9),)), ("Z", "ज़िंदा", 0.88, (("G", 0.5),))),
    "k8": (("T", "तीसरी", 0.02, ()), ("F", "जलाया", 0.32, (("T", 0.9),)), ("R", "राख", 0.45, (("F", 0.5),)),
           ("W", "शराब", 0.52, (("R", 0.3),)), ("C", "शुक्राचार्य", 0.8, (("W", 1.4),)),
           ("D", "पिला", 0.92, (("C", 0.4),))),
    "k9": (("P", "पेट", 0.5, (("t0", 0.4),)), ("I", "अंदर", 0.7, (("P", 0.3),))),
    "k10": (("C", "रोई", 0.12, ()), ("P", "पुकारा", 0.4, (("C", 0.7),)), ("V", "आवाज़", 0.6, (("P", 0.7),)),
            ("G", "गुरुजी", 0.72, (("V", 0.3),)), ("S", "पेट", 0.9, (("G", 0.4),))),
    "k11": (("M", "मुश्किल", 0.08, ()), ("O", "बाहर", 0.3, (("M", 0.6),)), ("F", "फटेगा", 0.6, (("O", 0.6),)),
            ("D", "मर", 0.85, (("F", 0.4),))),
    "k12": (("I", "अंदर", 0.35, (("t0", 0.5),)), ("N", "संजीवनी", 0.65, (("I", 0.5),)),
            ("T", "सिखा", 0.88, (("N", 0.4),))),
    "k13": (("O", "बाहर", 0.2, (("t0", 0.4),)), ("F", "गिर", 0.38, (("O", 0.6),)), ("V", "विद्या", 0.65, (("F", 0.8),)),
            ("Z", "ज़िंदा", 0.88, (("V", 0.6),))),
    "k14": (("N", "नियम", 0.3, (("t0", 0.6),)), ("B", "ब्राह्मण", 0.55, (("N", 0.6),)),
            ("W", "शराब", 0.65, (("B", 0.3),)),
            ("P", "पापी", 0.85, (("W", 0.5),))),
    "k15": (("D", "देवयानी", 0.03, ()), ("M", "शादी", 0.2, (("D", 0.5),)), ("B", "बोला", 0.4, (("M", 0.8),)),
            ("F", "पिता", 0.55, (("B", 0.5),)), ("J", "जन्मा", 0.72, (("F", 0.5),)), ("S", "बहन", 0.9, (("J", 0.6),))),
    "k16": (("A", "ग़ुस्से", 0.02, ()), ("C", "श्राप", 0.35, (("A", 0.6),)), ("Q", "था", 0.55, (("C", 0.6),)),
            ("K", "ऋषि", 0.7, (("Q", 0.3),)), ("N", "नहीं", 0.9, (("K", 0.4),))),
    "k17": (("Y", "याद", 0.02, ()), ("S", "श्राप", 0.3, (("Y", 0.3),)), ("L", "आख़िरी", 0.5, (("S", 0.4),))),
    "y1": (("Y", "याद", 0.25, (("t0", 1.6),)), ("D", "देवयानी", 0.3, (("Y", 0.2),)), ("C", "श्राप", 0.5, (("D", 0.6),)),
           ("N", "नहीं", 0.9, (("C", 0.8),))),
    "y2": (("R", "राजकुमारी", 0.2, (("t0", 0.5),)), ("S", "शर्मिष्ठा", 0.32, (("R", 0.3),)),
           ("F", "लड़", 0.45, (("S", 0.5),)),
           ("W", "कुएँ", 0.8, (("F", 1.2),)), ("P", "धकेल", 0.88, (("W", 0.2),))),
    "y3": (("Y", "ययाति", 0.2, (("t0", 0.4),)), ("H", "हाथ", 0.6, (("Y", 1.2),)), ("O", "निकाला", 0.9, (("H", 0.6),))),
    "y4": (("H", "हाथ", 0.2, (("t0", 0.4),)), ("M", "शादी", 0.4, (("H", 0.5),)), ("K", "राजा", 0.6, (("M", 0.6),)),
           ("R", "ऋषि", 0.7, (("K", 0.3),)), ("T", "सच", 0.9, (("R", 0.6),))),
    "y5": (("C", "चुपके", 0.15, (("t0", 0.2),)), ("S", "शर्मिष्ठा", 0.35, (("C", 0.4),)),
           ("B", "बेटे", 0.8, (("S", 0.8),))),
    "y6": (("P", "पता", 0.2, (("t0", 0.4),)), ("C", "रोती", 0.45, (("P", 0.6),)), ("F", "पिता", 0.65, (("C", 0.5),))),
    "y7": (("C", "श्राप", 0.35, (("t0", 0.6),)), ("A", "अभी", 0.55, (("C", 0.5),)), ("O", "बूढ़ा", 0.8, (("A", 0.4),))),
    "y8": (("R", "रास्ता", 0.1, (("t0", 0.3),)), ("J", "जवानी", 0.45, (("R", 0.8),)),
           ("B", "बुढ़ापा", 0.75, (("J", 0.6),))),
    "y9": (("B", "बेटों", 0.12, (("t0", 0.3),)), ("J", "जवानी", 0.4, (("B", 0.6),)), ("F", "चार", 0.65, (("J", 0.6),)),
           ("N", "मना", 0.85, (("F", 0.4),))),
    "y10": (("C", "छोटा", 0.1, ()), ("P", "पुरु", 0.3, (("C", 0.3),)), ("J", "जवानी", 0.75, (("P", 1.0),))),
    "y11": (("H", "हज़ार", 0.12, ()), ("Y", "जवान", 0.5, (("H", 0.5),)), ("O", "बूढ़ा", 0.85, (("Y", 0.5),))),
    "y12": (("I", "इच्छा", 0.3, (("t0", 0.8),)), ("N", "नहीं", 0.45, (("I", 0.5),)), ("G", "घी", 0.65, (("N", 0.8),)),
            ("F", "भड़कती", 0.85, (("G", 0.5),))),
    "y13": (("J", "जवानी", 0.3, (("t0", 0.5),)), ("L", "लौटा", 0.45, (("J", 0.3),)),
            ("K", "राजा", 0.75, (("L", 0.7),))),
    "y14": (("T", "ट्विस्ट", 0.2, (("t0", 0.6),)), ("P", "पुरु", 0.35, (("T", 0.4),)),
            ("D", "पांडव", 0.7, (("P", 1.2),)),
            ("K", "कौरव", 0.82, (("D", 0.4),))),
    "y15": (("Y", "यदु", 0.15, (("t0", 0.3),)), ("N", "मना", 0.3, (("Y", 0.4),)), ("K", "कृष्ण", 0.8, (("N", 1.2),))),
    "o1": (("S", "छह", 0.08, ()), ("P1", "शिष्य", 0.25, (("S", 0.6),)), ("P2", "ऋषि", 0.45, (("P1", 0.8),)),
           ("P3", "अगस्त्य", 0.62, (("P2", 0.8),)), ("P4", "लड़का", 0.75, (("P3", 0.7),)),
           ("P5", "नचिकेता", 0.85, (("P4", 0.5),)), ("P6", "ययाति", 0.95, (("P5", 0.5),))),
    "o2": (("Q", "शॉकिंग", 0.25, (("t0", 0.4),)), ("N", "छह", 0.6, (("Q", 0.6),)), ("C", "कमेंट", 0.85, (("N", 0.4),))),
}


# The same cues in the Kannada lines (videos/six_stories.py KN): {line: {cue name: Kannada word}}. Exact substrings of
# the Kannada text; where Kannada puts a word earlier or later than Hindi, the CUES gaps keep the beats in order.
CUES_KN = {
    "i1": dict(S="ಶಿಷ್ಯ", P="ಹೊಟ್ಟೆ", B="ಮಾತಾಡಿದ"),
    "i2": dict(R="ಋಷಿ", Y="ಯಮನಿಗೇ", Z="ಶಿಕ್ಷೆ"),
    "i3": dict(R="ಋಷಿ", S="ಸಮುದ್ರವನ್ನೇ", P="ಕುಡಿದು"),
    "i4": dict(L="ಹುಡುಗ", A="ಹೆಣ್ಣನ್ನೂ", N="ಇರಲಿಲ್ಲ"),
    "i5": dict(C="ಹುಡುಗ", Y="ಯಮನ", M="ಸಾವಿನ", Q="ಕೇಳಿ"),
    "i6": dict(F="ಅಪ್ಪ", B="ಮಗನ", J="ಯೌವನ"),
    "i7": dict(C="ಆರು", S="ನಿಜವಾಗಲೂ", M="ಮಹಾಭಾರತ", R="ರಾಮಾಯಣ", U="ಉಪನಿಷತ್ತಿನಲ್ಲಿ"),
    "i8": dict(D="ನೋಡಿ", P="ಮೊದಲನೇ", L="ಹುಡುಗಿ", A="ಕೊನೆಯ", F="ಬರ್ತಾಳೆ"),
    "k1": dict(D="ದೇವತೆಗಳು", A="ಅಸುರರ", L="ಯುದ್ಧ"),
    "k2": dict(S="ಶುಕ್ರಾಚಾರ್ಯರ", V="ವಿದ್ಯೆ", N="ಸಂಜೀವಿನಿ", D="ಸತ್ತ", Z="ಬದುಕಿಸ್ತಿದ್ರು"),
    "k3": dict(N="ಇರಲಿಲ್ಲ", B="ಬೃಹಸ್ಪತಿಯ", K="ಕಚನನ್ನ", S="ಕಳಿಸಿದ್ರು"),
    "k4": dict(W="ಶಿಷ್ಯ", V="ಸೇವೆ", D="ದೇವಯಾನಿಗೆ", L="ಇಷ್ಟ"),
    "k5": dict(U="ಗೊತ್ತಾಯ್ತು", M="ಕೊಂದು", W="ತೋಳಗಳಿಗೆ"),
    "k6": dict(C="ಅಳೋಕೆ", P="ಕರೆದ್ರು", Z="ಜೀವಂತವಾಗಿ"),
    "k7": dict(M="ಕೊಂದ್ರು", P="ಅರೆದು", S="ಸಮುದ್ರದ", G="ಗುರು", Z="ಬದುಕಿಸಿದ್ರು"),
    "k8": dict(T="ಮೂರನೇ", F="ಸುಟ್ಟು", R="ಬೂದಿಯನ್ನ", W="ಮದ್ಯದಲ್ಲಿ", C="ಶುಕ್ರಾಚಾರ್ಯರಿಗೇ", D="ಕುಡಿಸಿದ್ರು"),
    "k9": dict(P="ಹೊಟ್ಟೆ", I="ಒಳಗಿದ್ದ"),
    "k10": dict(C="ಅತ್ತಳು", P="ಕರೆದ್ರು", V="ಧ್ವನಿ", G="ಗುರುಗಳೇ", S="ಹೊಟ್ಟೆಯಲ್ಲಿದ್ದೀನಿ"),
    "k11": dict(M="ಸಮಸ್ಯೆ", O="ಹೊರಗೆ", F="ಒಡೆಯುತ್ತೆ", D="ಸತ್ತು"),
    "k12": dict(I="ಒಳಗೇ", N="ಸಂಜೀವಿನಿ", T="ಕಲಿಸಿಬಿಟ್ರು"),
    "k13": dict(O="ಹೊರಗೆ", F="ಬಿದ್ರು", V="ವಿದ್ಯೆಯಿಂದ", Z="ಬದುಕಿಸಿದ"),
    "k14": dict(N="ನಿಯಮ", B="ಬ್ರಾಹ್ಮಣ", W="ಮದ್ಯ", P="ಪಾಪಿ"),
    "k15": dict(D="ದೇವಯಾನಿ", M="ಮದುವೆ", B="ಹೇಳಿದ", F="ನಿಮ್ಮಪ್ಪನ", J="ಹುಟ್ಟಿದ್ದೀನಿ", S="ತಂಗಿ"),
    "k16": dict(A="ಕೋಪದಲ್ಲಿ", C="ಶಾಪ", Q="ಕಚನ", K="ಋಷಿಯ", N="ಆಗಲ್ಲ"),
    "k17": dict(Y="ನೆನಪಿಟ್ಕೊಳ್ಳಿ", S="ಶಾಪ", L="ಕೊನೆಯ"),
    "y1": dict(Y="ನೆನಪಿದೆಯಾ", D="ದೇವಯಾನಿ", C="ಋಷಿಯ", N="ಆಗಲ್ಲ"),
    "y2": dict(R="ರಾಜಕುಮಾರಿ", S="ಶರ್ಮಿಷ್ಠೆ", F="ಜಗಳ", W="ಬಾವಿಗೆ", P="ತಳ್ಳಿಬಿಟ್ಳು"),
    "y3": dict(Y="ಯಯಾತಿ", H="ಕೈ", O="ಎಳೆದ"),
    "y4": dict(H="ಕೈ", M="ಮದುವೆ", K="ರಾಜ", R="ಋಷಿಯ", T="ನಿಜ"),
    "y5": dict(C="ಗುಟ್ಟಾಗಿ", S="ಶರ್ಮಿಷ್ಠೆಯನ್ನೂ", B="ಮಕ್ಕಳಾದ್ರು"),
    "y6": dict(P="ಗೊತ್ತಾದಾಗ", C="ಅಳ್ತಾ", F="ಅಪ್ಪ"),
    "y7": dict(C="ಶಾಪ", A="ಈಗಲೇ", O="ಮುದುಕ"),
    "y8": dict(R="ದಾರಿನೂ", J="ಯೌವನ", B="ಮುಪ್ಪನ್ನ"),
    "y9": dict(B="ಮಕ್ಕಳಿಗೆ", J="ಯೌವನ", F="ನಾಲ್ಕು", N="ಬೇಡ"),
    "y10": dict(C="ಚಿಕ್ಕ", P="ಪುರು", J="ಯೌವನ"),
    "y11": dict(H="ಸಾವಿರ", Y="ಯುವಕ", O="ಮುದುಕ"),
    "y12": dict(I="ಆಸೆ", N="ತೀರಲ್ಲ", G="ತುಪ್ಪ", F="ಉರಿಯುತ್ತೆ"),
    "y13": dict(J="ಯೌವನ", L="ವಾಪಸ್", K="ರಾಜ"),
    "y14": dict(T="ಟ್ವಿಸ್ಟ್", P="ಪುರುವಿನ", D="ಪಾಂಡವರು", K="ಕೌರವರು"),
    "y15": dict(Y="ಯದುವಿನ", N="ಬೇಡ", K="ಕೃಷ್ಣ"),
    "o1": dict(S="ಆರು", P1="ಶಿಷ್ಯ", P2="ಋಷಿ", P3="ಅಗಸ್ತ್ಯ", P4="ಹುಡುಗ", P5="ನಚಿಕೇತ", P6="ಯಯಾತಿ"),
    "o2": dict(Q="ಶಾಕ್", N="ಆರರವರೆಗೆ", C="ಕಾಮೆಂಟ್"),
}


def cues(tl, bid):
    """{name: time} for a line in the timeline's language (cached on the timeline)."""
    cache = getattr(tl, "_six_a_cues", None)
    if cache is None:
        cache = {}
        tl._six_a_cues = cache
    if bid not in cache:
        kn = getattr(tl, "lang", "hi") == "kn"
        out = {"t0": T(tl, bid)}
        for name, word, frac, cons in CUES[bid]:
            v = cue(tl, bid, CUES_KN[bid][name] if kn else word, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


def line_end(tl, bid):
    return tl[bid].end


# ------------------------------------------------------------------ the landscape cloth and lamp


LAMP = (960.0, 1000.0)               # the oil lamp behind the cloth (wide frame), as in scenes_six_b


@functools.lru_cache(maxsize=1)
def stage_surface():
    """puppet_core.screen_surface's backlit cloth laid out for the wide frame (the same recipe as scenes_six_b, so all
    six stories are lit alike): the oil lamp low in the middle, a second small lamp lighting the headline, two stitched
    panel seams, gentle creases and a few oil stains."""
    from scipy.ndimage import gaussian_filter
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
    """puppet_core.lamp for the wide frame (as scenes_six_b): flicker, a drifting warm hot spot, a night tint, a flash
    of lamp light."""
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
    """In the dark shots the small lamp over the headline stays lit, so the words read (as scenes_six_b)."""
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


def ground(cr, alpha=1.0, x=W / 2, s=1.42, y=FLOOR + 6):
    prop(cr, "ground", x, y, s, alpha=alpha)


# ------------------------------------------------------------------ text


HY = 46                              # the headline's small line (top), as scenes_six_b


def head(cr, t, small, t_small, big=None, t_big=0.0, big_size=118, small_size=56, under=None, big_color=RED,
         ghost=None, alpha=1.0):
    """The two-tier headline at the top centre (as scenes_six_b.head2): a small dark setup line (fits 1600 px), one big
    red key line (fits 1460 px, 1740 px at its pop-in overshoot, inside the 90 px margins)."""
    if small:
        words = small.split()
        sw = sum(text_size(w_, small_size)[0] for w_ in words) + small_size * 0.34 * (len(words) - 1)
        if sw > 1600:
            small_size = int(small_size * 1600 / sw)
        small_line(cr, t, [(w_, t_small + 0.08 * k) for k, w_ in enumerate(words)], HY, small_size, alpha=alpha)
    if big:
        big_size = min(big_size, fit(big, big_size, 1460))
        return big_word(cr, t, big, t_big, HY + small_size * 1.25, big_size, big_color, alpha, ghost, under)
    return None


def medal(cr, x, y, r, text, kind="sx_medal", alpha=1.0, size=None, color=INK, font=HEAD_FONT, pop=None, t=0.0):
    """A leather medallion with a word or number on it (centred on x, y; r = its radius in px)."""
    if alpha <= 0.01:
        return
    k = 1.0
    if pop is not None and 0 <= t - pop < 0.3:
        k = 1.0 + 0.25 * math.sin(math.pi * (t - pop) / 0.3)
    prop(cr, kind, x, y, r * k / 100.0, alpha=alpha)
    if text:
        sz = size or int(r * 0.9)
        w_ = text_size(text, sz, font)[0]
        if w_ > 1.5 * r:
            sz = int(sz * 1.5 * r / w_)
        draw_text(cr, text, x, y + 2, sz * k, color, alpha, font, "cm")


def curse_card(cr, t, x, y, s, alpha=1.0, t_in=None, line_t=(None, None, None), pin_t=None, tick_t=None,
               frozen=False, rod=True):
    """The curse as a leather plaque: KACHA'S CURSE: / NO SAGE'S SON / WILL MARRY YOU. Drops in at t_in; line_t =
    when each line shows; pin_t = when the red pin lands on its top (it stops swinging); tick_t = a red tick."""
    q = back(clamp((t - t_in) / 0.35), 1.4) if t_in is not None else 1.0
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    yy = y + 60 * (1 - q)
    pinned = pin_t is not None and t >= pin_t
    r = 0.0 if (frozen or pinned) else sway(t, 0.012, 0.4, x * 0.01)
    if rod and not pinned:
        pc.rod(cr, x, yy + 110 * s, x + 30, H + 60, alpha=0.5 * a)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(r)
    cr.scale(s, s)
    pc.paint_part(cr, "plaque", a)
    for (txt, sz, col, dy), ts in zip((("KACHA'S CURSE:", 40, INK, -76), ("NO SAGE'S SON", 78, RED, -2),
                                        ("WILL MARRY YOU", 78, RED, 72)), line_t):
        p = prog(t, ts, 0.25) * a if ts is not None else a
        if p > 0:
            draw_text(cr, txt, 0, dy, sz, col, p, MONO_FONT if sz < 50 else HEAD_FONT, "cm", 3 if sz < 50 else 0)
    cr.restore()
    if pin_t is not None and t > pin_t - 0.35:
        u = clamp((t - pin_t + 0.35) / 0.35)
        e = u * u
        px, py = x + 6 * s, yy - 104 * s
        prop(cr, "sx_pin", px + 420 * (1 - e), py - 360 * (1 - e), 0.75 * s / 0.85, rot=0.3 * (1 - e), alpha=a)
        if 0 < t - pin_t < 0.5:
            sparkle(cr, px, py, 70 * (1 - (t - pin_t) / 0.5) + 10, a)
    if tick_t is not None:
        tick(cr, x + 300 * s, y - 10 * s, 150 * s, prog(t, tick_t, 0.35), alpha=a)


CARD_HOLD = 2.7                      # how long a chapter card holds before the story's first scene (as scenes_six_b)


def card_out(t0, t1):
    """When the chapter card flies up: after CARD_HOLD, or sooner on a short first line (leaves the scene 1.4 s)."""
    return t0 + max(1.6, min(CARD_HOLD, t1 - t0 - 1.4))


def seg_line(cr, parts, x, y, size, font=HEAD_FONT, alpha=1.0, tracking=0, gap=None):
    """A centred line of coloured pieces [(text, colour)]."""
    ws = [text_size(p, size, font, tracking)[0] for p, _ in parts]
    gap = size * 0.3 if gap is None else gap
    xx = x - (sum(ws) + gap * (len(parts) - 1)) / 2
    for (p, col), w_ in zip(parts, ws):
        draw_text(cr, p, xx, y, size, col, alpha, font, "lm", tracking)
        xx += w_ + gap


def chapter(cr, t, t_in, t_out, story, lines, source):
    """The palm-leaf chapter card, the same as scenes_six_b's: STORY n OF 6, the English title (lines of [(text,
    colour)]), the source in a red stamp box. It rises in at t_in and flies up and away at t_out."""
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


def big_mark(cr, t, t_in, text, x, y, size, color=RED, alpha=1.0, rot=0.08):
    """A big "?" or "!" popping on (cream edge so it reads on dark cloth)."""
    p = prog(t, t_in, 0.25) * alpha
    if p <= 0:
        return
    k = 1.25 - 0.25 * back(clamp((t - t_in) / 0.3))
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot + 0.03 * math.sin(t * 3))
    cr.scale(k, k)
    for dx, dy in ((-3, 0), (3, 0), (0, -3), (0, 3)):
        draw_text(cr, text, dx, dy, size, LIGHT, 0.8 * p, HEAD_FONT, "cm")
    draw_text(cr, text, 0, 0, size, color, p, HEAD_FONT, "cm")
    cr.restore()


# ------------------------------------------------------------------ pose helpers


def aim(x, hip_y, s, target, flip=False, bulk=1.0):
    """front=(upper, fore) for a straight front arm pointing from the shoulder at target."""
    sg = -1 if flip else 1
    sx, sy = x + sg * 26 * bulk * s, hip_y - 262 * s
    dx, dy = (target[0] - sx) * sg, target[1] - sy
    return (math.atan2(-dx, dy), 0.0)


def reach(hip, s, rot, flip, target, sh_dx):
    """(upper, fore) so a front arm (shoulder at (sh_dx, -262)) of a puppet at hip (rotated rot, flipped) lands its
    hand on target."""
    dx, dy = target[0] - hip[0], target[1] - hip[1]
    c, si = math.cos(-rot), math.sin(-rot)
    lx, ly = (dx * c - dy * si) / s, (dx * si + dy * c) / s
    if flip:
        lx = -lx
    return reach_arm(0.0, 0.0, 1.0, sh_dx, (lx, ly), False)


def hand_local(front, sh=(22.0, -262.0)):
    """Where a front hand sits (design units, from the hip) for arm angles front = (upper, fore)."""
    a1, a2 = front
    ux, uy = -150 * math.sin(a1), 150 * math.cos(a1)
    b = a1 + a2
    hx, hy = 6 * math.cos(b) - 160 * math.sin(b), 6 * math.sin(b) + 160 * math.cos(b)
    return sh[0] + ux + hx, sh[1] + uy + hy


def walking(t, t0, t1, x0, x1, step=0.42):
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step)
    return x, bob, rock, walk_legs(ph)


def fallen(fx, floor, s, theta, thick=60.0):
    """Hip position of a man() puppet pivoting about his feet at (fx, floor) by theta (lying when |theta| = pi/2)."""
    return (fx + 434 * s * math.sin(theta), floor - 434 * s * math.cos(theta) - thick * s * abs(math.sin(theta)))


def _head(name, mood, base_mood):
    full = name + ("" if mood == base_mood else "_" + mood)
    return full if full in pc._DEFS else name


# ------------------------------------------------------------------ the cast


def shukra(cr, t, x, s, mood="calm", staff=True, feet=FLOOR, backa=(0.12, -0.4), extra=None, **kw):
    """Shukracharya; his staff upright in his back hand."""
    sw = {"sx_shukra_head": _head("sx_shukra_head", mood, "calm")}
    ex = dict(extra or {})
    if staff:
        ex["sx_shukra_armB_lo"] = held_grip("rv_staff", backa, 0.6, 0.0, -250.0, kw.get("alpha", 1.0),
                                            kw.get("blur", 0.0))
    kw.setdefault("ph", 0.4)
    return fig(cr, X.SHUKRA, "sx_shukra", t, x, s, backa=backa, swap=sw, extra=ex or None, feet=feet, **kw)


def kacha(cr, t, x, s, mood="calm", feet=FLOOR, **kw):
    sw = {"sx_kacha_head": _head("sx_kacha_head", mood, "calm")}
    kw.setdefault("ph", 1.0)
    return fig(cr, X.KACHA, "sx_kacha", t, x, s, swap=sw, feet=feet, **kw)


def brih(cr, t, x, s, feet=FLOOR, **kw):
    kw.setdefault("ph", 2.0)
    return fig(cr, X.BRIH, "sx_brih", t, x, s, feet=feet, **kw)


def lady(cr, rig, key, t, x, s, mood="open", feet=FLOOR, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0,
         hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.0, y=None, extra=None):
    ang = woman_angles(key, t, front, backa, head, hits, ph)
    hy = feet - 470 * s if y is None else y
    sw = {key + "_head": _head(key + "_head", mood, "open")}
    return puppet(cr, rig, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, swap=sw, rods=rods, extra=extra)


def deva(cr, t, x, s, mood="open", **kw):
    return lady(cr, X.DEVA, "sx_deva", t, x, s, mood, **kw)


def sharm(cr, t, x, s, mood="open", **kw):
    kw.setdefault("ph", 1.3)
    return lady(cr, X.SHARM, "sx_sharm", t, x, s, mood, **kw)


def aged(cr, rig, key, headname, t, x, s, mood="calm", old=0.0, feet=FLOOR, front=(-0.32, -0.55),
         backa=(0.3, -0.25), head=0.0, hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.5, y=None,
         stick=None, legs=(0.0, 0.0), king=False):
    """Yayati or Puru, young (old 0) or old (old 1: the old head, bent forward, a walking stick in the front hand)."""
    q = clamp(old)
    lean = 0.2 * q
    sg = -1 if flip else 1
    if king:
        hn = headname + "_king_head"
    elif q >= 0.5:
        hn = _head(headname + "_old_head", mood, "calm")
    else:
        hn = _head(headname + "_head", mood, "calm")
    ex = None
    if stick if stick is not None else q >= 0.5:
        ex = {key + "_armF_lo": held_grip("rv_staff", front, 0.5, -lean, -430.0, alpha, blur)}
    hy = (feet - 434 * s + 14 * s * q) if y is None else y
    return fig(cr, rig, key, t, x, s, front=front, backa=backa, head=head + 0.14 * q,
               legs=(legs[0] - lean, legs[1] - lean), hits=hits, flip=flip, alpha=alpha, blur=blur, rods=rods,
               rot=rot + sg * lean, ph=ph, swap={key + "_head": hn}, extra=ex, y=hy)


STICK = (-0.38, -0.3)                # an old man's front arm on his stick


def yayati(cr, t, x, s, mood="calm", old=0.0, **kw):
    if old >= 0.5:
        kw.setdefault("front", STICK)
    return aged(cr, X.YAY, "sx_yay", "sx_yay", t, x, s, mood, old, **kw)


def puru(cr, t, x, s, mood="calm", old=0.0, **kw):
    if old >= 0.5:
        kw.setdefault("front", STICK)
    kw.setdefault("ph", 1.7)
    return aged(cr, X.PURU, "sx_puru", "sx_puru", t, x, s, mood, old, **kw)


def asura(cr, t, x, s, weapon=True, front=(-0.4, -0.6), **kw):
    ex = {"sx_asura_armF_lo": held("rv_club", front, 0.9, 150, 0.0)} if weapon else None
    return fig(cr, X.ASURA, "sx_asura", t, x, s, front=front, extra=ex, **kw)


def god(cr, t, x, s, front=(-0.4, -0.6), **kw):
    ex = {"indra_armF_lo": held("mace", front, 0.8, 150, 0.0)}
    return fig(cr, M.INDRA, "indra", t, x, s, front=front, extra=ex, **kw)


def wolf(cr, t, x, s, flip=False, low=False, alpha=1.0, ph=0.0, step=0.0):
    """A wolf (feet on the floor at x): a slow prowl bob."""
    b = 4 * abs(math.sin(t * 3.2 + ph)) * step
    prop(cr, "sx_wolf_low" if low else "sx_wolf", x, FLOOR - b, s, rot=0.02 * math.sin(t * 1.7 + ph), alpha=alpha,
         flip=flip)


def sil(cr, fn, a=1.0, col=SIL):
    return silhouette(cr, fn, a, col)


def xray(cr, t, cx, cy, s, a, kid=1.0, kid_mood="calm", kid_front=(-0.32, -0.55), bright=0.0):
    """The x-ray belly: a pale glowing window over the guru's stomach with tiny Kacha standing inside."""
    if a <= 0.01:
        return
    rx, ry = 150 * s, 190 * s
    cr.save()
    cr.translate(cx, cy)
    cr.scale(rx, ry)
    cr.new_path()
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    path = cr.copy_path()
    cr.new_path()
    cr.append_path(path)
    g = cairo.RadialGradient(cx, cy, 0, cx, cy, max(rx, ry))
    g.add_color_stop_rgba(0, 0.93, 0.99, 1.0, 0.75 * a)
    g.add_color_stop_rgba(1, 0.55, 0.80, 0.95, 0.75 * a)
    cr.set_source(g)
    cr.fill()
    glow(cr, cx, cy + 20 * s, 330 * s, (0.45 + 0.4 * bright) * a)
    if kid > 0.01:
        kacha(cr, t, cx, 0.17 * s, mood=kid_mood, feet=cy + ry * 0.8, rods=False, alpha=kid * a, front=kid_front)
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for lw, al in ((30 * s, 0.14), (14 * s, 0.3)):
        cr.new_path()
        cr.append_path(path)
        cr.set_source_rgba(*COOL, al * a)
        cr.set_line_width(max(1.5, lw))
        cr.stroke()
    cr.restore()
    for lw, col in ((7 * s, (0.10, 0.40, 0.62)), (2.6 * s, (0.86, 0.98, 1.0))):
        cr.new_path()
        cr.append_path(path)
        cr.set_source_rgba(*col, 0.95 * a)
        cr.set_line_width(max(1.2, lw))
        cr.stroke()
    lights(cr, t, cx, cy, rx * 0.9, 5, 0.5 * a, COOL, 0.4)


def flame_fire(cr, t, x, ground_y, s=1.0, flare=0.0, alpha=1.0):
    """A sacred fire on its altar; flare 0..1 makes it leap up."""
    f = 1 + 0.9 * flare
    glow(cr, x, ground_y - 200 * s * f, (320 * s + 60) * f, (0.55 + 0.1 * math.sin(t * 7)) * alpha)
    prop(cr, "altar", x, ground_y + 14 * s, 0.72 * s, alpha=alpha)
    prop(cr, f"flame{int(t * 10) % 3}", x, ground_y - 44 * s, 0.5 * s * f, alpha=alpha)
    lights(cr, t, x, ground_y - 260 * s * f, 110 * s * f, 7, 0.6 * alpha, (1.0, 0.7, 0.3), 0.8)


def crack(cr, t, p0, p1, a, col=(1.0, 0.45, 0.25), seed=0):
    """A jagged crack of light (a curse) from p0 to p1."""
    if a <= 0.01:
        return
    n = 9
    pts = []
    for i in range(n + 1):
        u = i / n
        j = 0 if i in (0, n) else 26 * math.sin(i * 2.7 + seed + int(t * 12) * 1.3)
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        ln = math.hypot(dx, dy) or 1
        pts.append((p0[0] + dx * u - dy / ln * j, p0[1] + dy * u + dx / ln * j))
    cr.save()
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, al, c, op in ((24, 0.25, col, cairo.OPERATOR_ADD), (11, 0.85, (0.80, 0.16, 0.06), cairo.OPERATOR_OVER),
                          (4, 0.95, (1.0, 0.92, 0.70), cairo.OPERATOR_OVER)):
        cr.set_operator(op)
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
        cr.set_source_rgba(*c, al * a)
        cr.set_line_width(lw)
        cr.stroke()
    cr.restore()


def call_rings(cr, x, y, t, t0, n=4, period=0.32, rmax=480, color=INK, alpha=1.0, side=1):
    """A voice going out: arcs spreading on one side of (x, y) only (side 1 = to the right)."""
    for i in range(n):
        p = (t - t0 - i * period) / 1.1
        if 0 < p < 1:
            r = 40 + rmax * ease(p)
            cr.set_source_rgba(*color, 0.6 * (1 - p) * alpha)
            cr.set_line_width(12 * (1 - p) + 3)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            a0 = 0.0 if side > 0 else math.pi
            cr.new_path()
            cr.arc(x, y, r, a0 - 0.32 * math.pi, a0 + 0.32 * math.pi)
            cr.stroke()


# ------------------------------------------------------------------ the six intro panels


PU_W, PU_H, PF = 1600.0, 900.0, 820.0          # panel design units; the panel's floor


def pn1(cr, t, st, a):
    g, kid, talk = st.get("glow", 1.0), st.get("kid", 1.0), st.get("talk", 1.0)
    glow(cr, 760, 420, 640, 0.3 * a)
    pts = sil(cr, lambda c_: shukra(c_, t, 640, 0.74, feet=PF, rods=False, front=(-0.6, -1.2)), a)
    bx, by = to_user(cr, pts["belly"])
    xray(cr, t, bx, by - 10, 0.95, g * a, kid, "call" if talk > 0.5 else "calm", (-2.4, -0.3) if talk > 0.5 else
         (-0.32, -0.55), bright=talk)
    if talk > 0.01:
        cloud_text(cr, t, 1150, 300, 0.75, [("GURUJI!", 120, RED, 0, -1.0)], alpha=talk * a)


def pn2(cr, t, st, a):
    ym, hit = st.get("yama", 1.0), st.get("hit", 1.0)
    glow(cr, 800, 450, 700, 0.25 * a)
    store = {}

    def f(c_):
        store["r"] = rishi(c_, t, 400, 0.72, mood="calm", feet=PF, rods=False, front=(-1.75 - 0.25 * hit, 0.0),
                           backa=(0.3, -0.3), hits=[(st.get("t_hit", -9), 0.3)])
        if ym > 0.01:
            store["y"] = yama(c_, t, 1180, 0.66, nod=0.6 * hit, feet=PF, flip=True, rods=False, rot=-0.08 * hit,
                              alpha=ym)
    sil(cr, f, a)
    if hit > 0.01 and "y" in store:
        hp = to_user(cr, store["r"]["handF"])
        yc = to_user(cr, store["y"]["chest"])
        crack(cr, t, hp, yc, hit * a * (0.6 + 0.4 * math.sin(t * 9)), seed=2)
        glow(cr, yc[0], yc[1], 260, 0.5 * hit * a)


def pn3(cr, t, st, a):
    d = st.get("drink", 1.0)
    level = 560 + 170 * ease(d)
    sh = 40 * math.sin(t * 0.8)
    prop(cr, "sx_wave2", 520 + sh, level - 30, 0.6, alpha=a)
    prop(cr, "sx_wave", 470 - sh, level + 20, 0.6, alpha=a)
    store = {}

    def f(c_):
        rock = [(1000, 900), (1060, 700), (1130, 640), (1600, 630), (1600, 900)]
        pc.poly(c_, rock)
        c_.set_source_rgb(0.2, 0.2, 0.2)
        c_.fill()
        store["p"] = fig(c_, R.PULASTYA, "pulastya", t, 1280, 0.62, feet=640, flip=True, rods=False,
                         front=(-2.3, -1.3), backa=(-2.2, -1.2), head=-0.15, ph=0.3)
    sil(cr, f, a)
    if d > 0.01:
        hx, hy = to_user(cr, store["p"]["head"])
        mouth = (hx - 50, hy + 40)
        src = (720, level - 10)
        pts = [(src[0] + (mouth[0] - src[0]) * u, src[1] + (mouth[1] - src[1]) * u - 260 * 4 * u * (1 - u))
               for u in (i / 30 for i in range(31))]
        for lw, col, al in ((46, (0.20, 0.45, 0.85), 0.9), (26, (0.45, 0.72, 1.0), 0.9), (8, (0.9, 0.97, 1.0), 0.9)):
            cr.move_to(*pts[0])
            for p in pts[1:]:
                cr.line_to(*p)
            cr.set_source_rgba(*col, al * a * clamp(d * 4))
            cr.set_line_width(lw)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.stroke()
        for i in range(6):                                  # drops running up the stream
            u = (t * 0.9 + i / 6) % 1.0
            p = pts[min(30, int(u * 30))]
            sparkle(cr, p[0], p[1], 22, 0.8 * a, (0.85, 0.95, 1.0))


def pn4(cr, t, st, a):
    q = st.get("q", 1.0)
    glow(cr, 800, 460, 640, 0.25 * a)

    def f(c_):
        prop(c_, "tree", 200, PF + 10, 0.55, rot=sway(t, 0.006, 0.3))
        prop(c_, "tree", 1460, PF + 10, 0.5, rot=sway(t, 0.006, 0.3, 1.0), flip=True)
        deer(c_, t, 1120, PF, 0.62, flip=True, rods=False, shimmer=0.0)
        kacha(c_, t, 640, 0.6, feet=PF, rods=False, front=(-0.9, -0.6),
              extra={"sx_kacha_head": lambda cc: _horn(cc)})
    sil(cr, f, a)
    big_mark(cr, t, -9 if q >= 1 else st.get("t_q", -9), "?", 830, 300, 260, alpha=q * a)


def _horn(cr_):
    cr_.save()
    cr_.translate(34, -190)
    cr_.rotate(0.3)
    cr_.scale(1.6, 1.6)
    pc.paint_part(cr_, "sx_horn", 1.0)
    cr_.restore()


def pn5(cr, t, st, a):
    door, q = st.get("door", 1.0), st.get("q", 1.0)
    x, s = 1100, 0.92
    op = [(x - 190 * s, PF), (x - 190 * s, PF - 610 * s), (x - 140 * s, PF - 690 * s), (x, PF - 740 * s),
          (x + 140 * s, PF - 690 * s), (x + 190 * s, PF - 610 * s), (x + 190 * s, PF)]
    pc.poly(cr, op)
    cr.set_source_rgba(0.10, 0.03, 0.03, 0.92 * a)
    cr.fill()
    glow(cr, x, PF - 300 * s, 340, 0.0)
    cr.save()
    pc.poly(cr, op)
    cr.clip()
    g = cairo.RadialGradient(x, PF - 260 * s, 10, x, PF - 260 * s, 380 * s)
    g.add_color_stop_rgba(0, 0.95, 0.20, 0.08, 0.7 * door * a * (0.85 + 0.15 * math.sin(t * 3)))
    g.add_color_stop_rgba(1, 0.95, 0.20, 0.08, 0.0)
    cr.set_source(g)
    cr.paint()
    cr.restore()
    glow(cr, 560, 520, 520, 0.3 * a)

    def f(c_):
        prop(c_, "sx_door_frame", x, PF, s)
        kacha(c_, t, 560, 0.46, feet=PF, rods=False, **ANJALI)
    sil(cr, f, a)
    big_mark(cr, t, -9 if q >= 1 else st.get("t_q", -9), "?", 640, 270, 230, alpha=q * a)


def pn6(cr, t, st, a):
    sw_ = st.get("swap", 1.0)
    glow(cr, 800, 450, 700, 0.25 * a)
    store = {}

    def f(c_):
        store["y"] = yayati(c_, t, 470, 0.66, old=1 - sw_, feet=PF, rods=False)
        store["p"] = puru(c_, t, 1150, 0.62, old=sw_, feet=PF, flip=True, rods=False)
    sil(cr, f, a)
    yc = to_user(cr, store["y"]["chest"])
    pcst = to_user(cr, store["p"]["chest"])
    u = ease(clamp(sw_ * 1.15))
    ox = pcst[0] + (yc[0] - pcst[0]) * u
    oy = pcst[1] + (yc[1] - pcst[1]) * u - 220 * 4 * u * (1 - u)
    glow(cr, ox, oy, 260, 0.75 * a)
    sparkle(cr, ox, oy, 70 + 12 * math.sin(t * 6), a)
    lights(cr, t, ox, oy, 90, 6, 0.8 * a)


PANELS = {1: pn1, 2: pn2, 3: pn3, 4: pn4, 5: pn5, 6: pn6}
PANEL_HEADS = {1: ("A STUDENT SPOKE FROM INSIDE", "HIS GURU'S STOMACH"), 2: ("A SAGE", "PUNISHED YAMA"),
               3: ("A SAGE DRANK", "THE WHOLE OCEAN"), 4: ("A BOY WHO HAD", "NEVER SEEN A WOMAN"),
               5: ("A CHILD ASKED YAMA", "THE SECRET OF DEATH"), 6: ("A FATHER TOOK", "HIS SON'S YOUTH")}
PANEL_NAMES = {1: "KACHA", 2: "MANDAVYA", 3: "AGASTYA", 4: "RISHYASHRINGA", 5: "NACHIKETA", 6: "YAYATI"}


def panel(cr, t, k, x, y, w, st=None, alpha=1.0, dim=0.0, badge=True, lit=0.0):
    """Shadow panel k (1-6), top-left at (x, y), w wide (16:9): a lamp-lit window in a leather frame with its
    silhouette scene and a red numbered medallion on its corner. dim darkens it; lit adds a warm rim."""
    if alpha <= 0.01:
        return
    h = w * 9 / 16
    sc = w / PU_W
    cr.save()
    cr.set_source_rgba(0.05, 0.02, 0.01, 0.35 * alpha)
    cr.rectangle(x + 10, y + 14, w, h)
    cr.fill()
    cr.rectangle(x, y, w, h)
    cr.clip()
    g = cairo.RadialGradient(x + w / 2, y + h * 0.55, 0, x + w / 2, y + h * 0.55, w * 0.72)
    g.add_color_stop_rgba(0, 0.97, 0.84, 0.60, alpha)
    g.add_color_stop_rgba(0.5, 0.88, 0.64, 0.36, alpha)
    g.add_color_stop_rgba(1, 0.50, 0.26, 0.10, alpha)
    cr.set_source(g)
    cr.paint()
    cr.translate(x, y)
    cr.scale(sc, sc)
    PANELS[k](cr, t, st or {}, alpha)
    cr.restore()
    if dim > 0.01:
        cr.rectangle(x, y, w, h)
        cr.set_source_rgba(0.06, 0.03, 0.02, 0.62 * dim * alpha)
        cr.fill()
    fw = max(6.0, w * 0.013)
    if lit > 0.01:
        cr.save()
        cr.set_operator(cairo.OPERATOR_ADD)
        for lw, al in ((fw * 4, 0.18), (fw * 2, 0.35)):
            cr.rectangle(x, y, w, h)
            cr.set_source_rgba(1.0, 0.8, 0.4, al * lit * alpha)
            cr.set_line_width(lw)
            cr.stroke()
        cr.restore()
    cr.rectangle(x, y, w, h)
    cr.set_source_rgba(0.30, 0.15, 0.06, alpha)
    cr.set_line_width(fw)
    cr.stroke()
    cr.set_source_rgba(0.95, 0.80, 0.50, 0.85 * alpha)
    step = max(10.0, fw * 1.6)
    for i in range(int(w / step)):
        for yy in (y, y + h):
            cr.new_sub_path()
            cr.arc(x + step * (i + 0.5), yy, fw * 0.16, 0, 2 * math.pi)
    for j in range(int(h / step)):
        for xx in (x, x + w):
            cr.new_sub_path()
            cr.arc(xx, y + step * (j + 0.5), fw * 0.16, 0, 2 * math.pi)
    cr.fill()
    if badge:
        r = max(24.0, w * 0.045)
        medal(cr, x + r * 0.55, y + r * 0.55, r, str(k), "sx_medal_red", alpha, int(r * 1.1), LIGHT)


def progress_row(cr, t, k, t0, alpha=1.0):
    """Six small numbered medallions under the intro panels: done (gold), now (red, pops), still to come (pale)."""
    for i in range(1, 7):
        x = 960 + (i - 3.5) * 70
        if i < k:
            medal(cr, x, 1000, 24, str(i), "sx_medal_gold", alpha, 28)
        elif i == k:
            medal(cr, x, 1000, 27, str(i), "sx_medal_red", alpha, 32, LIGHT, pop=t0, t=t)
        else:
            medal(cr, x, 1000, 22, str(i), "sx_medal", 0.55 * alpha, 26)


PANEL_BIG = (365.0, 282.0, 1190.0)


def intro_state(k, c, t):
    if k == 1:
        return dict(glow=0.6 + 0.4 * prog(t, c["P"] - 0.1, 0.4), kid=prog(t, c["S"] - 0.05, 0.4),
                    talk=prog(t, c["B"] - 0.05, 0.3))
    if k == 2:
        return dict(yama=prog(t, c["Y"] - 0.25, 0.35), hit=prog(t, c["Z"] - 0.05, 0.3), t_hit=c["Z"])
    if k == 3:
        return dict(drink=clamp((t - c["P"] + 0.5) / 1.6))
    if k == 4:
        return dict(q=prog(t, c["A"], 0.3), t_q=c["A"])
    if k == 5:
        return dict(door=prog(t, c["Y"] - 0.2, 0.5), q=prog(t, c["Q"] - 0.1, 0.3), t_q=c["Q"] - 0.1)
    return dict(swap=clamp((t - c["J"] + 0.3) / 1.0))


INTRO_KEY = {1: "P", 2: "Z", 3: "P", 4: "A", 5: "M", 6: "J"}


def make_intro(k):
    def shot(cr, t, tl, t0, t1):
        c = cues(tl, f"i{k}")
        x, y, w = PANEL_BIG
        e = 1.0 if k == 1 else ease((t - t0) / 0.32)
        if k > 1 and e < 1:
            panel(cr, t, k - 1, x - 1750 * e, y, w)
        panel(cr, t, k, x + 1750 * (1 - e), y, w, intro_state(k, c, t))

        def ui(cr):
            sm, bg = PANEL_HEADS[k]
            head(cr, t, sm, t0 + 0.04, bg, t0 + (0.3 if k == 1 else 0.22), under=c[INTRO_KEY[k]])
            progress_row(cr, t, k, t0)
        return dict(ui=ui, flash=flash_at(t, c[INTRO_KEY[k]], 0.15))
    return shot


# ------------------------------------------------------------------ i7  in our texts


def s_i7(cr, t, tl, t0, t1):
    c = cues(tl, "i7")
    books = ((365, "MAHABHARATA", c["M"], (1, 2, 3, 4, 6)), (960, "RAMAYANA", c["R"], (4,)),
             (1555, "UPANISHAD", c["U"], (5,)))
    for i, (bx, name, tn, nums) in enumerate(books):
        glow(cr, bx, 560, 380, 0.25 + 0.4 * prog(t, tn, 0.4))
        book(cr, t, bx, 470, 0.5, [(tn - 0.05, [(name, 130, HEAD_FONT)], 0)], t_in=t0 + 0.05 + 0.18 * i,
             t_open=tn - 0.4)
        for j, n in enumerate(nums):
            q = prog(t, tn + 0.3 + 0.1 * j, 0.25)
            medal(cr, bx + (j - (len(nums) - 1) / 2) * 84, 720, 36, str(n), "sx_medal_red", q, 42, LIGHT,
                  pop=tn + 0.3 + 0.1 * j, t=t)
        if t > tn + 0.3:
            draw_text(cr, "STORIES" if len(nums) > 1 else "STORY", bx, 785, 28, INK, prog(t, tn + 0.3, 0.3),
                      MONO_FONT, "cm", 3)

    def ui(cr):
        head(cr, t, "ALL SIX STORIES ARE", t0 + 0.04, "IN OUR TEXTS", c["S"], under=c["S"] + 0.4)
        progress_row(cr, t, 7, t0)
    return dict(ui=ui, flash=flash_at(t, c["M"], 0.15) + flash_at(t, c["R"], 0.12) + flash_at(t, c["U"], 0.12))


# ------------------------------------------------------------------ i8  the open loop


def s_i8(cr, t, tl, t0, t1):
    c = cues(tl, "i8")
    e = ease((t - t0) / 0.45)
    p1 = (130.0, 360.0, 580.0)
    p6 = (1210.0, 360.0, 580.0)
    h = 580 * 9 / 16
    panel(cr, t, 1, p1[0] - 700 * (1 - e), p1[1], p1[2], lit=prog(t, c["P"], 0.3) * (1 - prog(t, c["A"], 0.4)))
    panel(cr, t, 6, p6[0] + 700 * (1 - e), p6[1], p6[2], lit=prog(t, c["A"], 0.3))
    girl = prog(t, c["L"] - 0.25, 0.45)
    if girl > 0.01:
        glow(cr, 960, 640, 380, 0.45 * girl)
        sil(cr, lambda c_: deva(c_, t, 960, 0.5, feet=FLOOR, rods=False, mood="proud", head=-0.05), girl)
        pc.rod(cr, 965, 660, 990, H + 60, alpha=0.4 * girl)
    arc = [((p1[0] + p1[2] - 20) + (p6[0] + 20 - p1[0] - p1[2] + 20) * u,
            p1[1] + h * 0.45 - 200 * 4 * u * (1 - u)) for u in (i / 60 for i in range(61))]
    dp = clamp((t - c["L"]) / max(0.6, c["A"] - c["L"] + 0.3))
    dotted(cr, arc, dp, 26, 6.5, RED, 0.9)
    if dp > 0.02:
        tip = arc[min(60, int(60 * dp))]
        sparkle(cr, tip[0], tip[1], 30, 0.9)

    def ui(cr):
        if t < c["L"] - 0.15:
            head(cr, t, "WATCH TILL", t0 + 0.04, "THE END", c["D"] - 0.1)
        else:
            head(cr, t, "THE GIRL FROM STORY 1", c["L"] - 0.12, "RETURNS IN STORY 6", c["A"])
        tag(cr, t, c["P"], "STORY 1", p1[0] + p1[2] / 2, p1[1] + h + 60, 34)
        tag(cr, t, c["A"], "STORY 6", p6[0] + p6[2] / 2, p6[1] + h + 60, 34)
        big_mark(cr, t, c["L"] + 0.15, "?", 1075, 470, 150)
        progress_row(cr, t, 7, t0, 1 - e)
    return dict(ui=ui, flash=flash_at(t, c["L"], 0.15))


# ------------------------------------------------------------------ k1  STORY 1; the war


def battle(cr, t, a, tL):
    """Gods (rayed crowns, gold light) against horned asuras (red light), silhouettes lunging."""
    glow(cr, 420, 560, 560, 0.45 * a)
    warm(cr, 1500, 560, 560, 0.45 * a, (1.0, 0.35, 0.15))
    clash = 0.5 + 0.5 * math.sin(2 * math.pi * (t - tL) / 1.3)
    lunge = 70 * clash

    def gods(c_):
        for i, (x, s, ph) in enumerate(((210, 0.48, 0.0), (390, 0.52, 1.1), (590, 0.5, 2.2))):
            fr = mix((-0.6, -0.5), (-2.6, -0.3), 0.5 + 0.5 * math.sin(t * 2.6 + ph))
            god(c_, t, x + lunge * (1 if i == 2 else 0.6), s, front=fr, feet=FLOOR, rods=False, ph=ph,
                legs=(0.25, -0.2))

    def asuras(c_):
        for i, (x, s, ph) in enumerate(((1330, 0.5, 0.5), (1530, 0.54, 1.6), (1710, 0.48, 2.7))):
            fr = mix((-0.6, -0.5), (-2.6, -0.3), 0.5 + 0.5 * math.sin(t * 2.6 + ph + 1.5))
            asura(c_, t, x - lunge * (1 if i == 0 else 0.6), s, front=fr, feet=FLOOR, rods=False, flip=True, ph=ph,
                  legs=(0.25, -0.2))
    sil(cr, gods, a, (0.16, 0.10, 0.04))
    sil(cr, asuras, a)
    for i in range(3):
        u = ((t - tL) * 1.4 + i / 3) % 1.0
        sparkle(cr, 960 + 60 * math.sin(i * 2.1 + t), 520 + 80 * math.cos(i * 1.7), 80 * math.sin(math.pi * u),
                0.9 * a)
    lights(cr, t, 960, 700, 380, 10, 0.5 * a, (1.0, 0.7, 0.35), 0.6)


def s_k1(cr, t, tl, t0, t1):
    c = cues(tl, "k1")
    t_out = card_out(t0, t1)                            # the chapter card holds, then flies up
    b = prog(t, t_out - 0.1, 0.5)
    if b > 0.01:
        ground(cr, b)
        battle(cr, t, b, c["L"])
    chapter(cr, t, t0 - 0.3, t_out, "STORY 1 OF 6",
            [[("THE STUDENT WHO SPOKE", INK)], [("FROM HIS GURU'S", INK), ("STOMACH", RED)]], "MAHABHARATA · ADI PARVA")

    def ui(cr):
        if t > t_out:
            head(cr, t, "A WAR:", t_out + 0.1, "GODS VS ASURAS", t_out + 0.3)
    return dict(ui=ui, eve=0.3 * b, flash=flash_at(t, t0, 0.2) + flash_at(t, c["L"], 0.12))


# ------------------------------------------------------------------ k2  Shukra and Sanjivani


def s_k2(cr, t, tl, t0, t1):
    c = cues(tl, "k2")
    tS, tN, tD, tZ = c["S"], c["N"], c["D"], c["Z"]
    ground(cr)
    x, s = 470, SM
    glow(cr, x, 560, 460, 0.3 + 0.3 * prog(t, tS, 0.3))
    raise_ = keyed(t, [(t0, 0.0), (tD + 0.2, 1.0)], 0.35, 1.3)
    pts = shukra(cr, t, x, s, mood="call" if tZ - 0.7 < t < tZ + 0.5 else ("smile" if t > tZ + 0.5 else "calm"),
                 front=mix((-0.4, -0.6), (-1.85, -0.25), raise_), hits=[(tS, 0.3), (tD + 0.2, 0.4)])
    hand = to_user(cr, pts["handF"])
    # the fallen asura on the right, lying, then standing again
    fx, fs = 1230, 0.58
    a_in = prog(t, tD - 0.3, 0.45)
    rise = ease(clamp((t - tZ - 0.15) / 0.8))
    th = (math.pi / 2) * (1 - rise)
    hip = fallen(fx, FLOOR - 8, fs, th, 95.0)
    if a_in > 0.01:
        glow(cr, hip[0] + 60, hip[1] - 40, 420, (0.25 + 0.6 * prog(t, tZ - 0.4, 0.5)) * a_in)
        sil(cr, lambda c_: asura(c_, t, hip[0], fs, weapon=False, y=hip[1], rot=th, flip=True, rods=False,
                                 front=(-0.2, -0.3) if rise < 0.5 else (-1.9, -0.5)), a_in)
        chest = (hip[0] + 200 * fs * (1 - rise), hip[1] - 200 * fs * rise)
        flow(cr, t, tD + 0.45, tZ - 0.1, (hand[0] + 20, hand[1] - 10), chest, n=14, lift=170)
        burst(cr, t, chest[0], chest[1], tZ, n=18, rmax=520, alpha=0.9)
        if t > tZ:
            lights(cr, t, chest[0], chest[1], 160, 8, 0.8 * (1 - prog(t, tZ + 2.0, 1.0)))
    leaf_glow = prog(t, tN - 0.1, 0.4)
    if leaf_glow > 0:
        glow(cr, 850, 330, 300, 0.5 * leaf_glow)
    leaf_tag(cr, t, tN - 0.1, 850, 330, 0.85, [("SANJIVANI", 64, HEAD_FONT)])

    def ui(cr):
        if t < tN - 0.15:
            head(cr, t, "THE ASURAS' GURU:", t0 + 0.04, "SHUKRACHARYA", tS)
        elif t < tZ - 0.15:
            head(cr, t, "HIS SECRET POWER:", tN - 0.15, "SANJIVANI", tN)
        else:
            head(cr, t, "SANJIVANI:", tZ - 0.15, "BRINGS THE DEAD BACK", tZ, under=tZ + 0.4)
        tag(cr, t, tS + 0.15, "SHUKRACHARYA", 230, 380, 32)
    return dict(ui=ui, flash=flash_at(t, tS, 0.12) + flash_at(t, tZ, 0.35))


# ------------------------------------------------------------------ k3  the gods send Kacha


def s_k3(cr, t, tl, t0, t1):
    c = cues(tl, "k3")
    tN, tB, tK, tS = c["N"], c["B"], c["K"], c["S"]
    ground(cr)
    glow(cr, 330, 560, 520, 0.5)
    aura(cr, t, 330, 520, 120, 520, 0.25, n=16, spin=0.05)

    def gods(c_):
        god(c_, t, 150, 0.46, front=(-0.4, -0.6), feet=FLOOR, rods=False, ph=0.2)
        god(c_, t, 300, 0.42, front=(-0.4, -0.6), feet=FLOOR, rods=False, ph=1.4)
    sil(cr, gods, 0.55, (0.20, 0.13, 0.05))
    point = keyed(t, [(t0, 0.0), (tS - 0.1, 1.0)], 0.3, 1.3)
    brih(cr, t, 470, 0.48, front=mix((-0.4, -0.6), (-1.7, -0.1), point), hits=[(tB, 0.3), (tS, 0.4)])
    # the Sanjivani leaf, crossed out: the gods don't have it
    leaf_out = tK - 0.3
    if t < leaf_out + 0.3:
        leaf_tag(cr, t, t0 + 0.3, 1160, 450, 0.95, [("SANJIVANI", 64, HEAD_FONT)], t_out=leaf_out)
        if t > tN:
            big_x(cr, 1160, 455, 560, 130, prog(t, tN, 0.35), alpha=1 - prog(t, leaf_out, 0.25))
    # Kacha: appears beside his father, then turns and walks off toward the asuras' guru
    if t > tK - 0.35:
        b, k, a = depth(t, tK - 0.35, 0.45)
        if t < tS:
            kacha(cr, t, 800, SM * k, mood="calm", flip=True, alpha=a, blur=b, hits=[(tK, 0.4)], **ANJALI)
        else:
            x, bob, rock, legs = walking(t, tS + 0.1, tS + 1.8, 800, 1380)
            kacha(cr, t, x, SM, mood="calm", y=FLOOR - 434 * SM + bob, rot=rock, legs=legs, hits=[(tS + 1.8, 0.6)])
    far = prog(t, tS - 0.1, 0.5)
    if far > 0.01:
        glow(cr, 1700, 640, 260, 0.35 * far)
        sil(cr, lambda c_: shukra(c_, t, 1700, 0.3, feet=FLOOR - 120, flip=True, rods=False), 0.7 * far)
        path = [(1000 + 600 * u, FLOOR - 40 - 80 * math.sin(math.pi * u)) for u in (i / 40 for i in range(41))]
        dotted(cr, path, clamp((t - tS) / 1.2), 24, 5.5, RED, far)

    def ui(cr):
        if t < tB - 0.15:
            head(cr, t, "THE GODS DIDN'T KNOW", t0 + 0.04, "SANJIVANI", tN)
        elif t < tS - 0.15:
            head(cr, t, "THEIR GURU BRIHASPATI'S SON:", tB - 0.15, "KACHA", tK)
        else:
            head(cr, t, "THE GODS SENT A", tS - 0.15, "SPY STUDENT", tS)
        tag(cr, t, tB + 0.1, "BRIHASPATI", 470, 330, 30, t_out=tS + 0.2)
        tag(cr, t, tK + 0.15, "KACHA", 820, 370, 34, t_out=tS)
        tag(cr, t, tS + 0.4, "SHUKRA", 1700, 520, 28)
    return dict(ui=ui, flash=flash_at(t, tK, 0.15))


# ------------------------------------------------------------------ k4  the student; Devayani


def s_k4(cr, t, tl, t0, t1):
    c = cues(tl, "k4")
    tW, tV, tD, tL = c["W"], c["V"], c["D"], c["L"]
    ground(cr)
    glow(cr, 650, 560, 520, 0.35)
    shukra(cr, t, 420, SM, mood="smile" if t > tV + 0.3 else "calm", front=(-0.6, -0.7), hits=[(tW, 0.3)])
    bow = keyed(t, [(t0, 0.0), (tW - 0.1, 1.0), (tV - 0.2, 0.0)], 0.3, 1.3)
    serve = keyed(t, [(t0, 0.0), (tV - 0.1, 1.0)], 0.3, 1.3)
    fr = mix(mix((-0.32, -0.55), ANJALI["front"], bow), (-1.35, -0.35), serve)
    ba = mix(mix((0.3, -0.25), ANJALI["backa"], bow), (0.2, -0.4), serve)
    ex = {"sx_kacha_armF_lo": held("md_kalasha", fr, 0.3, 175, 0.0)} if serve > 0.5 else None
    kacha(cr, t, 860, SM, mood="smile" if t > tL else "calm", flip=True, front=fr, backa=ba, head=0.25 * bow,
          extra=ex, hits=[(tV, 0.3), (tL + 0.2, 0.3)])
    if t > tD - 0.35:
        b, k, a = depth(t, tD - 0.35, 0.45)
        glow(cr, 1480, 560, 420, 0.4 * a + 0.3 * prog(t, tL, 0.4))
        deva(cr, t, 1480, SW * k, mood="smile" if t > tL else "open", flip=True, alpha=a, blur=b,
             front=mix((-0.08, -0.35), (-0.3, -2.45), prog(t, tL, 0.35)), hits=[(tL, 0.4)])
        if t > tL:
            warm(cr, 1180, 560, 360, 0.45 * prog(t, tL, 0.5))
            petals(cr, t, tL + 0.1, 1170, 330, n=10, spread=520, fall=560, dur=2.6, s=0.9)
            lights(cr, t, 1180, 560, 200, 8, 0.7 * prog(t, tL, 0.5))

    def ui(cr):
        if t < tD - 0.2:
            head(cr, t, "KACHA BECAME", t0 + 0.04, "SHUKRA'S STUDENT", tW)
        elif t < tL - 0.15:
            head(cr, t, "THE GURU'S DAUGHTER:", tD - 0.2, "DEVAYANI", tD)
        else:
            head(cr, t, "AND DEVAYANI", tL - 0.15, "LIKED HIM", tL, under=tL + 0.4)
        tag(cr, t, tD + 0.2, "DEVAYANI", 1480, 330, 34)
    return dict(ui=ui, flash=flash_at(t, tD, 0.12))


# ------------------------------------------------------------------ k5  killed... fed to wolves


def forest(cr, t, a=1.0):
    prop(cr, "tree", 120, FLOOR + 30, 0.62, rot=sway(t, 0.006, 0.3), alpha=0.55 * a, blur=9)
    prop(cr, "tree", 1800, FLOOR + 30, 0.58, rot=sway(t, 0.006, 0.3, 1.0), alpha=0.55 * a, blur=9, flip=True)
    prop(cr, "tree", 1500, FLOOR + 40, 0.42, rot=sway(t, 0.005, 0.3, 2.0), alpha=0.3 * a, blur=16)
    prop(cr, "tree", 420, FLOOR + 40, 0.4, rot=sway(t, 0.005, 0.3, 3.0), alpha=0.3 * a, blur=16, flip=True)


def s_k5(cr, t, tl, t0, t1):
    c = cues(tl, "k5")
    tU, tM, tW = c["U"], c["M"], c["W"]
    forest(cr, t)
    ground(cr)
    gone = t > tM + 0.25
    dark = prog(t, tM - 0.15, 0.2) * (1 - prog(t, tM + 0.45, 0.35))
    if not gone:
        glow(cr, 960, 560, 420, 0.45)
        kacha(cr, t, 960, SM, mood="shock" if t > tM - 1.0 else "calm", front=(-0.32, -0.55) if t < tM - 1.0
              else (-1.3, -1.2), hits=[(tM - 1.0, 0.4)])
    close = ease(clamp((t - t0 - 0.2) / max(0.6, tM - t0 - 0.4)))
    leave = ease(clamp((t - tM - 0.5) / 1.6))
    raise_ = prog(t, tM - 0.6, 0.3) * (1 - leave)

    def asuras(c_):
        for x0, x1, s, fl, ph in ((-200, 620, 0.52, False, 0.3), (-380, 450, 0.48, False, 1.2),
                                  (2120, 1300, 0.52, True, 2.0), (2300, 1470, 0.48, True, 2.9)):
            x = x0 + (x1 - x0) * close + (x0 - x1) * 0.9 * leave
            fr = mix((-0.6, -0.5), (-2.6, -0.3), raise_)
            asura(c_, t, x, s, front=fr, feet=FLOOR, flip=fl, rods=False, ph=ph,
                  legs=walk_legs(math.sin(t * 7 + ph) * (0.5 if 0.02 < close < 0.98 or 0.02 < leave < 0.98 else 0)))
    sil(cr, asuras, 1.0)
    if gone:
        fade = 1 - prog(t, tM + 2.5, 1.2)
        lights(cr, t, 960, 760, 120, 7, 0.7 * fade, GOLDC, 0.35)
    # the wolves slink in
    wl = prog(t, tW - 0.7, 0.5)
    if wl > 0.01:
        u = ease(clamp((t - tW + 0.7) / 1.6))
        sil(cr, lambda c_: (wolf(c_, t, 2150 - 950 * u, 0.6, flip=True, low=True, step=1 - u),
                            wolf(c_, t, 2500 - 950 * u, 0.54, flip=True, low=False, step=1 - u, ph=1.0)), wl)
    shroud(cr, 960, 560, 1500, 0.92 * dark)

    def ui(cr):
        if t < tM - 0.1:
            head(cr, t, "THE ASURAS FOUND OUT", t0 + 0.04, "HIS PLAN", tU + 0.3)
        else:
            head(cr, t, "KILLED...", tM, "FED TO WOLVES", tW)
    return dict(ui=ui, night=0.25 + 0.12 * prog(t, tM, 0.3), lift=1.0, flash=flash_at(t, tM + 0.25, 0.5, 6.0))


# ------------------------------------------------------------------ k6  alive again


def s_k6(cr, t, tl, t0, t1):
    c = cues(tl, "k6")
    tC, tP, tZ = c["C"], c["P"], c["Z"]
    forest(cr, t)
    ground(cr)
    glow(cr, 450, 560, 520, 0.4)
    cry = keyed(t, [(t0, 0.0), (tC - 0.1, 1.0)], 0.3, 1.3)
    dp = deva(cr, t, 270, SW, mood="weep" if t > tC - 0.15 else "open", front=mix((-0.08, -0.35), WEEP["front"], cry),
              backa=mix((0.15, -0.2), WEEP["backa"], cry), head=0.18 * cry, rot=0.012 * math.sin(t * 9) * cry)
    eye = to_user(cr, dp["head"])
    if t > tC:
        for i in range(7):
            u = (t - tC - 0.1 - 0.6 * i) / 0.9
            if 0 < u < 1:
                prop(cr, "rr_tear", eye[0] + 26, eye[1] + 40 + 240 * u * u, 0.9, alpha=1 - u * u)
    call = keyed(t, [(t0, 0.0), (tP - 0.1, 1.0)], 0.3, 1.3)
    sp = shukra(cr, t, 600, SM, mood="call" if tP - 0.15 < t < tZ + 0.3 else ("smile" if t > tZ + 0.3 else "calm"),
                front=mix((-0.4, -0.6), (-2.1, -0.3), call), hits=[(tP, 0.4)])
    mo = to_user(cr, sp["head"])
    if t > tP:
        call_rings(cr, mo[0] + 70, mo[1] + 30, t, tP, n=5, period=0.35, rmax=520, alpha=0.8)
    # the wolves; the burst; Kacha steps out of the light
    run = ease(clamp((t - tZ - 0.1) / 1.2))
    sil(cr, lambda c_: (wolf(c_, t, 1290 + 800 * run, 0.56, flip=run > 0.02, ph=0.3, step=run),
                        wolf(c_, t, 1660 + 800 * run, 0.5, flip=True, low=run < 0.02, ph=1.4, step=run)), 1.0)
    burst(cr, t, 1450, 640, tZ, n=20, rmax=620, alpha=1.0)
    if t > tZ:
        b, k, a = depth(t, tZ + 0.05, 0.5)
        glow(cr, 1440, 560, 420, 0.55 * a)
        kacha(cr, t, 1440, SM * k, mood="smile", flip=True, alpha=a, blur=b, hits=[(tZ + 0.5, 0.4)])

    def ui(cr):
        if t < tP - 0.15:
            head(cr, t, "DEVAYANI", t0 + 0.04, "WEPT", tC)
        elif t < tZ - 0.15:
            head(cr, t, "SHUKRA CALLED OUT:", tP - 0.15, "KACHA!", tP + 0.1)
        else:
            head(cr, t, "KACHA CAME OUT", tZ - 0.15, "ALIVE AGAIN", tZ, under=tZ + 0.4)
    return dict(ui=ui, night=0.22, lift=1.0, flash=flash_at(t, tZ, 0.45))


# ------------------------------------------------------------------ k7  the sea


SEA_Y = 760


def sea(cr, t, a=1.0, x=1330):
    sh = 40 * math.sin(t * 0.7)
    prop(cr, "sx_wave2", x + sh, SEA_Y - 30, 0.55, alpha=a)


def sea_front(cr, t, a=1.0, x=1330):
    sh = 40 * math.sin(t * 0.7)
    prop(cr, "sx_wave", x - 30 - sh, SEA_Y + 30, 0.55, alpha=a)


SHORE = [(-20, 690), (300, 672), (600, 690), (770, 735), (850, 810), (890, 1100), (-20, 1100)]


def shore(cr):
    """A rocky bank on the left, in front of the sea's edge."""
    pc.poly(cr, SHORE)
    cr.set_source_rgb(0.50, 0.32, 0.16)
    cr.fill_preserve()
    cr.set_source_rgb(*pc.INK)
    cr.set_line_width(5)
    cr.stroke()
    cr.set_source_rgba(0.95, 0.80, 0.55, 0.6)
    for i in range(70):
        x = (i * 131) % 860
        y = 710 + ((i * 53) % 330)
        if x < 760 + 0.4 * (y - 735):
            cr.new_sub_path()
            cr.arc(x, y, 3, 0, 2 * math.pi)
    cr.fill()
    for pts in (((40, 760), (220, 740), (360, 770)), ((420, 820), (600, 800), (720, 840))):
        pc.ink(cr, list(pts), 3, col=(0.32, 0.18, 0.08))


def s_k7(cr, t, tl, t0, t1):
    c = cues(tl, "k7")
    tM, tP, tS, tG, tZ = c["M"], c["P"], c["S"], c["G"], c["Z"]
    sea(cr, t)
    col = prog(t, tG + 0.1, 0.5)
    beam(cr, 1330, 120, 420, SEA_Y + 40, 0.8 * col)
    rise = ease(clamp((t - tZ + 0.25) / 0.9))
    if rise > 0:
        glow(cr, 1330, 600, 420, 0.7 * rise)
        cr.save()
        cr.rectangle(0, 0, W, SEA_Y + 5)
        cr.clip()
        kacha(cr, t, 1330, SM, mood="smile", flip=True, y=FLOOR - 434 * SM + 520 * (1 - rise) - 120, rods=False,
              hits=[(tZ + 0.7, 0.4)])
        cr.restore()
        lights(cr, t, 1330, 560, 180, 9, 0.8 * rise)
    sea_front(cr, t)
    shore(cr)
    ground(cr, x=420, s=0.64)
    throw = keyed(t, [(t0, 0.0), (tP - 0.15, 1.0), (tP + 0.3, 0.2)], 0.22, 1.3)
    flinch = prog(t, tZ, 0.3)

    def asuras(c_):
        asura(c_, t, 640 - 60 * flinch, 0.5, weapon=False, front=mix((-0.4, -0.6), (-2.7, -0.2), throw),
              feet=FLOOR, rods=False, ph=0.4)
        asura(c_, t, 480 - 60 * flinch, 0.46, front=(-0.5, -0.5), feet=FLOOR, rods=False, ph=1.6)
    sil(cr, asuras, 1.0)
    # the dark cloud thrown into the sea
    u = clamp((t - tP + 0.05) / 0.75)
    if 0 < u < 1:
        x = 700 + (1330 - 700) * u
        y = 520 + (SEA_Y - 520) * u - 300 * 4 * u * (1 - u)
        prop(cr, "cloud", x, y, 0.32, rot=u * 3, alpha=0.95)
    if t > tP + 0.7:
        v = (t - tP - 0.7) / 0.9
        if v < 1:
            for i in range(9):
                a_ = -math.pi * (0.15 + 0.7 * i / 8)
                sparkle(cr, 1330 + 160 * v * math.cos(a_), SEA_Y - 10 + 190 * v * math.sin(a_) + 220 * v * v, 28,
                        1 - v, (0.85, 0.95, 1.0))
        ra = 0.8 * (1 - prog(t, tP + 1.4, 0.5))
        if ra > 0.01:
            cr.save()
            cr.translate(1330, SEA_Y + 6)
            cr.scale(1.0, 0.22)
            cr.new_path()
            cr.arc(0, 0, 120 + 90 * clamp(v), 0, 2 * math.pi)
            cr.restore()
            cr.set_source_rgba(0.90, 0.97, 1.0, ra)
            cr.set_line_width(6)
            cr.stroke()
    # Shukra comes; a column of light; Kacha rises out of the sea
    if t > tG - 0.35:
        b, k, a = depth(t, tG - 0.35, 0.45)
        glow(cr, 220, 560, 380, 0.4 * a)
        up = keyed(t, [(t0, 0.0), (tG + 0.1, 1.0)], 0.3, 1.3)
        shukra(cr, t, 230, SM * k, mood="call" if t < tZ + 0.4 else "smile", front=mix((-0.4, -0.6), (-2.0, -0.3), up),
               alpha=a, blur=b)

    def ui(cr):
        big, tb = ("ALIVE AGAIN", tZ) if t > tZ - 0.15 else ("INTO THE SEA", tS)
        head(cr, t, "KILLED AGAIN...", t0 + 0.04, big, tb, under=tZ + 0.4 if big == "ALIVE AGAIN" else None)
    return dict(ui=ui, flash=flash_at(t, tZ, 0.4))


# ------------------------------------------------------------------ k8  the third time: ashes in the wine


FIRE8 = (520, FLOOR)
SH8 = (1540, SM)


def s_k8(cr, t, tl, t0, t1):
    c = cues(tl, "k8")
    tT, tF, tR, tW, tC, tD = c["T"], c["F"], c["R"], c["W"], c["C"], c["D"]
    ground(cr)
    fx, fg = FIRE8
    flame_fire(cr, t, fx, fg, 1.25, flare=prog(t, tF - 0.1, 0.3) * (1 - 0.6 * prog(t, tR + 1.0, 0.8)))
    # the asura with the cup: at the fire, then carrying it to Shukra
    turn = t > tW + 0.4
    ax, bob, rock, legs = walking(t, tW + 0.45, tW + 1.6, 860, 1140)
    afr = (-1.45, -0.15)
    store = {}

    def asura_fn(c_):
        store["a"] = asura(c_, t, ax, 0.52, weapon=False, front=afr, flip=not turn, feet=FLOOR, rods=False, ph=0.6,
                           y=FLOOR - 434 * 0.52 + bob, rot=rock, legs=legs)
    sil(cr, asura_fn, 1.0)
    ahand = to_user(cr, store["a"]["handF"])
    sx, ss = SH8
    t_give = max(tW + 1.7, tC - 0.6)
    t_drink = max(t_give + 0.6, tD - 0.25)
    sh_hip = (sx, FLOOR - 434 * ss)
    mouth_hint = (sx - 60 * ss, FLOOR - 434 * ss - 410 * ss)
    if t < t_give:
        cup = (ahand[0] + (0 if turn else -10), ahand[1] + 6)
        crot = 0.0
    else:
        g = ease(clamp((t - t_give) / 0.45))
        hold = (sx - 170, FLOOR - 434 * ss - 120 * ss)
        cup = (ahand[0] + (hold[0] - ahand[0]) * g, ahand[1] + 6 + (hold[1] - ahand[1] - 6) * g)
        crot = 0.0
        if t > t_drink:
            d = ease(clamp((t - t_drink) / 0.45))
            cup = (cup[0] + (mouth_hint[0] + 30 - cup[0]) * d, cup[1] + (mouth_hint[1] + 120 - cup[1]) * d)
            crot = -1.0 * d
    reach_on = t > t_give
    fr = reach(sh_hip, ss, 0.0, True, (cup[0] + 10, cup[1] - 30), 26) if reach_on else (-0.4, -0.6)
    tilt_back = -0.18 * prog(t, t_drink, 0.4)
    glow(cr, sx, 560, 420, 0.35)
    shukra(cr, t, sx, ss, mood="calm", flip=True, front=fr, head=tilt_back, hits=[(t_give, 0.3)])
    prop(cr, "sx_cup", cup[0], cup[1] + 40, 0.5, rot=crot)
    if t > tW - 0.1:
        glow(cr, cup[0], cup[1] - 40, 120, 0.45 * prog(t, tW - 0.1, 0.3) * (1 - prog(t, t_drink + 0.8, 0.5)))
    # the ashes rise from the fire and drift into the cup
    if tR - 0.1 < t < tW + 1.0:
        for i in range(16):
            ti = tR - 0.1 + 0.07 * i
            u = (t - ti) / 0.9
            if 0 < u < 1:
                e = u * u * (3 - 2 * u)
                x = fx + (ahand[0] - fx) * e + 14 * math.sin(t * 6 + i)
                y = fg - 360 + (ahand[1] - 20 - fg + 360) * e - 160 * 4 * e * (1 - e)
                cr.new_path()
                cr.arc(x, y, 6 + (i % 3) * 2, 0, 2 * math.pi)
                cr.set_source_rgba(0.35, 0.33, 0.32, 0.85 * min(1, 4 * (1 - u)))
                cr.fill()

    def ui(cr):
        if t < tR - 0.15:
            head(cr, t, "THE THIRD TIME:", t0 + 0.04, "A TRICK", tT + 0.4)
        else:
            head(cr, t, "ASHES IN THE", tR - 0.15, "GURU'S WINE", tW, under=t_drink)
        stamp(cr, t, tT + 0.2, "3RD TIME", fx, 380, 56, color=RED)
        tag(cr, t, tW + 0.3, "WINE", 1000, 420, 30, t_out=t_give)
    return dict(ui=ui, flash=flash_at(t, tF, 0.2))


# ------------------------------------------------------------------ k9 / k10 / k12  inside the guru


XR = (720, 0.6)


def s_k9(cr, t, tl, t0, t1):
    c = cues(tl, "k9")
    tP, tI = c["P"], c["I"]
    ground(cr)
    x, s = XR
    glow(cr, x, 560, 480, 0.35)
    pts = shukra(cr, t, x, s, front=(-0.5, -1.4), hits=[(tP, 0.3)])
    bx, by = to_user(cr, pts["belly"])
    xr = prog(t, tP - 0.25, 0.5)
    xray(cr, t, bx, by, s, xr, kid=prog(t, tI - 0.15, 0.4))
    if t > tI:
        dotted(cr, [(bx + 120, by), (1050, by - 60), (1180, by - 90)], prog(t, tI, 0.4), 22, 5, RED)

    def ui(cr):
        head(cr, t, "NOW KACHA WAS", t0 + 0.04, "INSIDE THE GURU", tI, under=tI + 0.4)
        tag(cr, t, tI + 0.3, "KACHA", 1270, by - 100, 36)
    return dict(ui=ui, flash=flash_at(t, tP, 0.2))


def s_k10(cr, t, tl, t0, t1):
    c = cues(tl, "k10")
    tC, tP, tV, tG, tS = c["C"], c["P"], c["V"], c["G"], c["S"]
    ground(cr)
    x, s = XR
    glow(cr, x, 560, 480, 0.35)
    call = keyed(t, [(t0, 0.0), (tP - 0.1, 1.0), (tV, 0.3)], 0.3, 1.3)
    pts = shukra(cr, t, x, s, mood="shock" if t > tV else ("call" if t > tP - 0.15 else "calm"),
                 front=mix((-0.5, -1.4), (-2.1, -0.3), call), hits=[(tP, 0.3), (tV, 0.5)])
    bx, by = to_user(cr, pts["belly"])
    talk = t > tV
    xray(cr, t, bx, by, s, 1.0, kid=1.0, kid_mood="call" if talk else "calm",
         kid_front=(-2.6, -0.3) if talk else (-0.32, -0.55), bright=prog(t, tV, 0.3))
    if tP < t < tV + 0.2:
        mo = to_user(cr, pts["head"])
        call_rings(cr, mo[0] + 60, mo[1] + 30, t, tP, n=3, period=0.35, rmax=380, alpha=0.7)
    cry = keyed(t, [(t0, 0.0), (tC, 1.0)], 0.3, 1.3)
    dp = deva(cr, t, 1640, 0.55, mood="weep" if t > tC - 0.15 else "open", flip=True,
              front=mix((-0.08, -0.35), WEEP["front"], cry), backa=mix((0.15, -0.2), WEEP["backa"], cry),
              head=0.18 * cry)
    eye = to_user(cr, dp["head"])
    if t > tC:
        for i in range(8):
            u = (t - tC - 0.1 - 0.6 * i) / 0.9
            if 0 < u < 1:
                prop(cr, "rr_tear", eye[0] - 24, eye[1] + 40 + 220 * u * u, 0.85, alpha=1 - u * u)
    if talk:
        call_rings(cr, bx + 40, by, t, tV, n=3, period=0.3, rmax=260, color=(0.10, 0.40, 0.62), alpha=0.7)
    cloud_text(cr, t, 1150, 480, 0.85, [("GURUJI,", 66, INK, -46, tG), ("I'M IN YOUR STOMACH!", 58, RED, 34, tS - 0.1)],
               t_in=tV - 0.1)

    def ui(cr):
        if t < tV - 0.15:
            head(cr, t, "DEVAYANI WEPT AGAIN.", t0 + 0.04, "SHUKRA CALLED KACHA", tP)
        else:
            head(cr, t, "THEN A VOICE CAME FROM", tV - 0.15, "INSIDE", tV)
    return dict(ui=ui, flash=flash_at(t, tV, 0.3))


def s_k12(cr, t, tl, t0, t1):
    c = cues(tl, "k12")
    tI, tN, tT = c["I"], c["N"], c["T"]
    ground(cr)
    x, s = XR
    glow(cr, x, 560, 480, 0.35)
    pts = shukra(cr, t, x, s, mood="shut", front=(-0.3, -2.0), head=0.18, hits=[(tI, 0.2)])
    bx, by = to_user(cr, pts["belly"])
    hx, hy = to_user(cr, pts["head"])
    mouth = (hx + 52, hy + 52)
    learn = prog(t, tT - 0.1, 0.4)
    xray(cr, t, bx, by, s, 1.0, kid=1.0, kid_mood="smile" if learn > 0.5 else "calm",
         kid_front=ANJALI["front"], bright=0.4 + 0.6 * learn)
    w = prog(t, tI - 0.2, 0.4)
    if w > 0.01:                                         # lines of light curling from his lips into his belly
        for k in range(3):
            c1 = (mouth[0] + 150 + 40 * k, mouth[1] + 60)
            pts_ = []
            for i in range(41):
                u = i / 40
                px = (1 - u) ** 2 * mouth[0] + 2 * (1 - u) * u * c1[0] + u * u * (bx + 30)
                py = (1 - u) ** 2 * mouth[1] + 2 * (1 - u) * u * c1[1] + u * u * (by - 40 + 30 * k)
                pts_.append((px, py))
            ph = (t * 0.8 + k * 0.33) % 1.0
            cr.save()
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.set_dash([18, 22], -ph * 400)
            for lw, col, al in ((9, (0.86, 0.42, 0.04), 0.75), (3.5, (1.0, 0.92, 0.6), 0.95)):
                cr.move_to(*pts_[0])
                for p in pts_[1:]:
                    cr.line_to(*p)
                cr.set_source_rgba(*col, al * w)
                cr.set_line_width(lw)
                cr.stroke()
            cr.restore()
            u = (t * 0.7 + k / 3) % 1.0
            p = pts_[int(u * 40)]
            sparkle(cr, p[0], p[1], 26, 0.9 * w)
    if t > tN - 0.1:
        glow(cr, 1260, 470, 260, 0.4 * prog(t, tN, 0.3))
        dotted(cr, [(1080, 470), (960, by - 40), (bx + 150, by)], prog(t, tN + 0.2, 0.5), 22, 5, RED)
    leaf_tag(cr, t, tN - 0.1, 1290, 470, 0.85, [("SANJIVANI", 64, HEAD_FONT)])

    def ui(cr):
        head(cr, t, "SO HE TAUGHT HIM", t0 + 0.04, "INSIDE", tI, under=tT)
    return dict(ui=ui, flash=flash_at(t, tT, 0.15))


# ------------------------------------------------------------------ k11  the problem: a balance


def s_k11(cr, t, tl, t0, t1):
    c = cues(tl, "k11")
    tM, tO, tF, tD = c["M"], c["O"], c["F"], c["D"]
    ground(cr)
    glow(cr, 330, 560, 400, 0.35)
    pts = shukra(cr, t, 330, 0.52, mood="shock" if t > tF else "calm", front=(-0.5, -1.4), hits=[(tF, 0.4)])
    bx, by = to_user(cr, pts["belly"])
    xray(cr, t, bx, by, 0.52, 1.0)
    tilt = lambda tt: settle(tt, [(t0 - 5, 0.0), (tO, -0.22), (tD, -0.34)])
    lit = prog(t, tD, 0.4)
    bx_, s_ = 1150, 0.62
    pans = balance(cr, t, bx_, FLOOR, s_, tilt, labels=0.0, lit=lit)
    for (ex, ey, swp), side in zip(pans, (-1, 1)):
        rim_y = ey + K_PAN_DROP * s_
        if side < 0:
            kacha(cr, t, ex, 0.17, feet=rim_y - 6, rods=False, mood="smile" if t > tO else "calm",
                  front=(-2.6, -0.3) if t > tO else (-0.32, -0.55))
            if t > tO:
                lights(cr, t, ex, rim_y - 120, 70, 5, 0.7)
        else:
            shukra(cr, t, ex, 0.15, feet=rim_y - 6, rods=False, staff=False,
                   mood="shut" if t > tD else "calm")
        q = prog(t, tO if side < 0 else tD, 0.3)
        if q > 0:
            label = "KACHA OUT" if side < 0 else "GURU DIES"
            col = INK if side < 0 else RED
            cr.set_source_rgba(*INK, 0.7 * q)
            cr.set_line_width(3)
            cr.move_to(ex, rim_y + 34)
            cr.line_to(ex, rim_y + 62)
            cr.stroke()
            plaque(cr, label, ex, rim_y + 96, 44, col, q)

    def ui(cr):
        head(cr, t, "BUT HERE WAS", t0 + 0.04, "THE PROBLEM", tM, under=tD)
    return dict(ui=ui, flash=flash_at(t, tD, 0.2))


K_PAN_DROP = 300.0 + 34.0             # kaikeyi_cast.PAN_DROP + the pan's rim under its hook


# ------------------------------------------------------------------ k13  the student saves the guru


def s_k13(cr, t, tl, t0, t1):
    c = cues(tl, "k13")
    tO, tF, tV, tZ = c["O"], c["F"], c["V"], c["Z"]
    ground(cr)
    fx, s = 600, SM
    fall = ease(clamp((t - tF + 0.15) / 0.55)) * (1 - ease(clamp((t - tZ - 0.15) / 0.8)))
    th = -math.pi / 2 * fall
    hip = fallen(fx, FLOOR - 8, s, th, 90.0)
    glow(cr, fx - 100 * fall, 600 + 150 * fall, 460, 0.35)
    mood = "smile" if t > tZ + 0.6 else ("shut" if fall > 0.3 else ("shock" if t > tO - 0.4 else "calm"))
    pts = shukra(cr, t, hip[0], s, mood=mood, staff=fall < 0.05 and t < tF, y=hip[1], rot=th,
                 front=(-0.5, -1.4) if fall < 0.2 else (-0.4, -0.5), rods=fall < 0.05)
    bx, by = to_user(cr, pts["belly"])
    if t < tO + 0.1:
        xray(cr, t, bx, by, s, 1.0, bright=prog(t, tO - 0.6, 0.6))
    burst(cr, t, bx, by, tO, n=22, rmax=700, alpha=1.0)
    chest = to_user(cr, pts["chest"])
    if t > tO:
        b, k, a = depth(t, tO, 0.45)
        heal = keyed(t, [(t0, 0.0), (tV - 0.1, 1.0), (tZ + 0.6, 0.0)], 0.3, 1.3)
        kx = 1040
        kp = kacha(cr, t, kx, SM * k, mood="calm", flip=True, alpha=a, blur=b,
                   front=mix((-0.32, -0.55), (-1.1, -0.2), heal), backa=mix((0.3, -0.25), (-1.0, -0.3), heal),
                   head=0.15 * heal)
        hand = to_user(cr, kp["handF"])
        if heal > 0.05:
            glow(cr, hand[0], hand[1], 200, 0.7 * heal)
            sparkle(cr, hand[0], hand[1], 40 + 8 * math.sin(t * 8), heal)
        flow(cr, t, tV + 0.15, tZ - 0.1, hand, chest, n=14, lift=140)
        burst(cr, t, chest[0], chest[1], tZ, n=16, rmax=420, alpha=0.8)

    def ui(cr):
        if t < tF - 0.1:
            head(cr, t, "A BURST OF LIGHT:", t0 + 0.04, "KACHA WAS OUT", tO)
        elif t < tZ - 0.15:
            head(cr, t, "AND THE GURU", tF - 0.1, "FELL", tF)
        else:
            head(cr, t, "THE STUDENT", tZ - 0.15, "SAVED HIS GURU", tZ, under=tZ + 0.4)
    return dict(ui=ui, flash=flash_at(t, tO, 0.5) + flash_at(t, tZ, 0.3))


# ------------------------------------------------------------------ k14  the new rule


def s_k14(cr, t, tl, t0, t1):
    c = cues(tl, "k14")
    tN, tB, tW, tP = c["N"], c["B"], c["W"], c["P"]
    ground(cr)
    glow(cr, 500, 560, 460, 0.4)
    up = keyed(t, [(t0, 0.0), (tN - 0.1, 1.0)], 0.3, 1.3)
    shukra(cr, t, 500, SM, mood="angry" if t > tW else "calm", front=mix((-0.4, -0.6), (-2.75, -0.15), up),
           hits=[(tN, 0.4), (tP, 0.3)])
    cx_, cy_ = 900, FLOOR - 4
    spill = prog(t, tW - 0.2, 0.6)
    cr.save()
    cr.translate(cx_ + 120, cy_ + 2)
    cr.scale(1.0, 0.22)
    cr.new_path()
    cr.arc(0, 0, 120 * spill, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(*X.WINE, 0.75 * spill)
    cr.fill()
    prop(cr, "sx_cup", cx_, cy_ - 4, 0.6, rot=-math.pi / 2 + 0.06)
    big_x(cr, cx_ + 40, cy_ - 50, 260, 170, prog(t, tP - 0.1, 0.3))
    card_lines = (("NEW RULE:", 44, INK, -78, tN + 0.1), ("NO WINE FOR", 74, RED, -6, tW),
                  ("BRAHMINS", 74, RED, 64, tW + 0.2))
    card2(cr, t, tN - 0.1, 1440, 540, 1.0, card_lines)

    def ui(cr):
        head(cr, t, "THAT DAY, SHUKRA MADE", t0 + 0.04, "A NEW RULE", tN, under=tP)
    return dict(ui=ui, flash=flash_at(t, tN, 0.15))


# ------------------------------------------------------------------ k15  "you are my sister"


def s_k15(cr, t, tl, t0, t1):
    c = cues(tl, "k15")
    tD, tM, tB, tF, tJ, tS = c["D"], c["M"], c["B"], c["F"], c["J"], c["S"]
    ground(cr)
    glow(cr, 560, 560, 440, 0.4)
    glow(cr, 1480, 560, 440, 0.35)
    offer = keyed(t, [(t0, 0.0), (tM - 0.1, 1.0)], 0.35, 1.3)
    dx = 90 * ease(clamp((t - tM + 0.1) / 0.6))
    dp = deva(cr, t, 460 + dx, SW, mood="smile" if t < tB else ("weep" if t > tS else "open"),
              front=mix((-0.08, -0.35), OFFER["front"], offer), backa=mix((0.15, -0.2), OFFER["backa"], offer),
              hits=[(tM, 0.3)])
    hf, hb = to_user(cr, dp["handF"]), to_user(cr, dp["handB"])
    gx, gy = (hf[0] + hb[0]) / 2 + 10, min(hf[1], hb[1]) - 30
    prop(cr, "kk_garland", gx, gy, 0.85, rot=0.05 * math.sin(t * 2.2))
    back_ = ease(clamp((t - tB + 0.1) / 0.5))
    stop = keyed(t, [(t0, 0.0), (tB, 1.0)], 0.3, 1.3)
    kacha(cr, t, 1400 + 110 * back_, SM, mood="calm", flip=True, front=mix((-0.32, -0.55), (-1.9, -1.0), stop),
          head=-0.05 * stop, hits=[(tB, 0.4)])
    cloud_text(cr, t, 1090, 480, 0.95, [("BORN AGAIN FROM", 48, INK, -80, tF - 0.1),
                                        ("YOUR FATHER'S BODY...", 48, INK, -26, tJ - 0.1),
                                        ("YOU ARE MY SISTER", 76, RED, 56, tS - 0.05)], flip=True, t_in=tF - 0.3)

    def ui(cr):
        if t < tB - 0.15:
            head(cr, t, "DEVAYANI WANTED TO", t0 + 0.04, "MARRY KACHA", tM)
        else:
            head(cr, t, "BUT KACHA SAID:", tB - 0.15, "NO", tB + 0.05)
    return dict(ui=ui, flash=flash_at(t, tS, 0.2))


# ------------------------------------------------------------------ k16 / k17  the curse; pinned


def s_k16(cr, t, tl, t0, t1):
    c = cues(tl, "k16")
    tA, tC, tQ, tK, tN = c["A"], c["C"], c["Q"], c["K"], c["N"]
    ground(cr)
    glow(cr, 480, 560, 440, 0.35)
    glow(cr, 1440, 560, 440, 0.35)
    dx_, kx = 470, 1450
    point = keyed(t, [(t0, 0.0), (tA + 0.2, 1.0)], 0.3, 1.4)
    dhy = FLOOR - 470 * SW
    khy = FLOOR - 434 * SM
    dfr = mix((-0.08, -0.35), aim(dx_, dhy, SW, (960, 520), bulk=0.85), point)
    kfr = mix((-0.32, -0.55), aim(kx, khy, SM, (960, 520), flip=True, bulk=0.92), point)
    dp = deva(cr, t, dx_, SW, mood="angry", front=dfr, hits=[(tA + 0.2, 0.3), (tC, 0.3)])
    kp = kacha(cr, t, kx, SM, mood="angry", flip=True, front=kfr, hits=[(tA + 0.2, 0.3), (tQ, 0.3)])
    sp = prog(t, tA + 0.3, 0.3) * (1 - 0.5 * prog(t, tQ, 0.4))
    if sp > 0.01:
        h1, h2 = to_user(cr, dp["handF"]), to_user(cr, kp["handF"])
        mid = (960, 540 + 20 * math.sin(t * 5))
        crack(cr, t, h1, mid, sp, (1.0, 0.5, 0.2), seed=1)
        crack(cr, t, h2, mid, sp, (1.0, 0.35, 0.3), seed=4)
        glow(cr, mid[0], mid[1], 240, 0.6 * sp)
        for i in range(4):
            u = (t * 2.2 + i / 4) % 1.0
            sparkle(cr, mid[0] + 90 * math.cos(i * 1.6 + t), mid[1] + 70 * math.sin(i * 2.3 + t),
                    40 * math.sin(math.pi * u), sp)
    curse_card(cr, t, 960, 470, 1.0, t_in=tQ - 0.15, line_t=(tQ, tK - 0.1, tN - 0.1))

    def ui(cr):
        if t < tQ - 0.15:
            head(cr, t, "IN ANGER, BOTH", t0 + 0.04, "CURSED EACH OTHER", tC)
        else:
            head(cr, t, "AND KACHA'S CURSE ON DEVAYANI WAS:", tQ - 0.15)
    return dict(ui=ui, flash=flash_at(t, tC, 0.2))


def s_k17(cr, t, tl, t0, t1):
    c = cues(tl, "k17")
    tY, tS, tL = c["Y"], c["S"], c["L"]
    ground(cr)
    sil(cr, lambda c_: (deva(c_, t, 280, SW, mood="angry", rods=False),
                        kacha(c_, t, 1640, SM, mood="angry", flip=True, rods=False)), 0.35)
    glow(cr, 960, 540, 520, 0.45)
    pin_t = tY + 0.45
    curse_card(cr, t, 960, 545, 1.15, pin_t=pin_t)
    if t > pin_t:
        u = clamp((t - pin_t) / 0.4)
        cr.rectangle(960 - 470, 545 - 150, 940, 300)
        cr.set_source_rgba(1.0, 0.97, 0.9, 0.35 * (1 - u))
        cr.fill()
    leaf_tag(cr, t, tL - 0.1, 960, 758, 1.15, [("IT RETURNS IN STORY 6", 32, MONO_FONT)])

    def ui(cr):
        head(cr, t, "REMEMBER", t0 + 0.04, "THIS CURSE", tS, under=tL)
    return dict(ui=ui, flash=flash_at(t, pin_t, 0.3))


# ------------------------------------------------------------------ y1  STORY 6; Devayani returns


def s_y1(cr, t, tl, t0, t1):
    c = cues(tl, "y1")
    t_out = card_out(t0, t1)                            # the chapter card holds, then flies up
    tY, tD = c["Y"], max(c["D"], t_out + 0.3)
    tC = max(c["C"], tD + 0.6)
    b = prog(t, t_out - 0.1, 0.5)
    if b > 0.01:
        ground(cr, b)
        bb, k, a = depth(t, t_out, 0.5)
        glow(cr, 560, 560, 480, 0.45 * a)
        deva(cr, t, 560, SW * k, mood="proud", alpha=a, blur=bb, head=-0.05, hits=[(tD, 0.3)])
    if t > tC - 0.3:
        fl = prog(t, tC - 0.3, 0.35)
        glow(cr, 1330, 500, 520, 0.6 * fl)
        curse_card(cr, t, 1330, 500, 0.85, t_in=tC - 0.3, pin_t=tC - 0.3, rod=False)
        cr.save()
        cr.set_operator(cairo.OPERATOR_MULTIPLY)
        cr.rectangle(1330 - 345, 500 - 115, 690, 230)
        cr.set_source_rgba(1.0, 0.86, 0.62, 0.5 * fl)
        cr.fill()
        cr.restore()
    chapter(cr, t, t0 - 0.3, t_out, "STORY 6 OF 6", [[("THE FATHER WHO TOOK", INK)], [("HIS SON'S", INK),
                                                                                     ("YOUTH", RED)]],
            "MAHABHARATA · ADI PARVA")

    def ui(cr):
        if t > t_out:
            head(cr, t, "REMEMBER", t_out + 0.1, "DEVAYANI?", tD)
            tag(cr, t, tD + 0.2, "DEVAYANI", 560, 330, 34)
            if t > tC:
                draw_text(cr, "FROM STORY 1", 1330, 690, 30, INK, prog(t, tC + 0.2, 0.3), MONO_FONT, "cm", 3)
    return dict(ui=ui, flash=flash_at(t, t0, 0.2) + flash_at(t, tC, 0.3))


# ------------------------------------------------------------------ y2  pushed into a well


WELL2 = (1180, 0.8)


def well_clip(cr, wx, s, inside=False):
    """Clip to everything outside the well's front wall (a figure inside it drops out of sight); inside=True also
    hides whatever is below the rim's level on either side (a figure that is in the well)."""
    rim = X.well_mouth_front(wx, FLOOR, s)
    cr.rectangle(0, 0, W, H)
    if inside:
        cr.move_to(-10, rim[0][1])
    else:
        cr.move_to(*rim[0])
    for p in rim[1:]:
        cr.line_to(*p)
    if inside:
        cr.line_to(W + 10, rim[-1][1])
        cr.line_to(W + 10, H + 10)
        cr.line_to(-10, H + 10)
    else:
        cr.line_to(rim[-1][0], H + 10)
        cr.line_to(rim[0][0], H + 10)
    cr.close_path()
    cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    cr.clip()
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)


def s_y2(cr, t, tl, t0, t1):
    c = cues(tl, "y2")
    tR, tS, tF, tW, tP = c["R"], c["S"], c["F"], c["W"], c["P"]
    ground(cr)
    wx, ws = WELL2
    rim_y = FLOOR - X.WELL_H * ws
    glow(cr, 700, 560, 560, 0.4)
    prop(cr, "sx_well_back", wx, FLOOR, ws)
    tp = max(tF + 1.0, min(tW, tP - 0.35))
    angry = t > tF - 0.15
    lunge = keyed(t, [(t0, 0.0), (tp - 0.1, 1.0), (tp + 0.6, 0.35)], 0.22, 1.2)
    if t > tS - 0.35:
        b, k, a = depth(t, tS - 0.35, 0.45)
        sharm(cr, t, 450 + 170 * lunge, SW * k, mood="angry" if angry else "open", alpha=a, blur=b,
              front=mix((-0.08, -0.35), (-1.45, -0.1), lunge), backa=mix((0.15, -0.2), (-1.3, -0.2), lunge),
              hits=[(tF, 0.4)])
    u = clamp((t - tp) / 1.0)
    dx0 = 860
    if u <= 0:
        deva(cr, t, dx0, SW, mood="angry" if angry else "open", flip=True, hits=[(tF, 0.4)],
             front=(-1.2, -0.6) if angry else (-0.08, -0.35))
    else:
        e = ease(clamp(u / 0.55))
        x = dx0 + (wx - dx0) * e
        rot = 1.1 * ease(clamp(u / 0.45))
        drop = 900 * clamp((u - 0.4) / 0.6) ** 2
        y = FLOOR - 470 * SW - 70 * math.sin(math.pi * clamp(u / 0.5)) + drop
        cr.save()
        well_clip(cr, wx, ws, inside=u > 0.4)
        deva(cr, t, x, SW, mood="shut", flip=True, y=y, rot=rot, rods=False, front=(-2.4, -0.4), backa=(-2.2, -0.5))
        cr.restore()
    prop(cr, "sx_well_front", wx, FLOOR, ws)
    ts = tp + 0.85
    if t > ts:
        v = (t - ts) / 1.0
        if v < 1:
            for i in range(10):
                a_ = -math.pi * (0.12 + 0.76 * i / 9)
                sparkle(cr, wx + 170 * v * math.cos(a_), rim_y + 120 * v * math.sin(a_) + 200 * v * v, 26, 1 - v,
                        (0.85, 0.95, 1.0))
        glow(cr, wx, rim_y, 260, 0.5 * (1 - prog(t, ts + 0.4, 0.8)))

    def ui(cr):
        if t < tF - 0.15:
            head(cr, t, "THE ASURA PRINCESS:", t0 + 0.04, "SHARMISHTHA", tS)
        elif t < tp - 0.1:
            head(cr, t, "DEVAYANI AND SHARMISHTHA", tF - 0.15, "FOUGHT", tF)
        else:
            head(cr, t, "PUSHED INTO", tp - 0.1, "A WELL", tp + 0.3, under=ts)
        tag(cr, t, tS + 0.15, "SHARMISHTHA", 470, 330, 32, t_out=tp)
        tag(cr, t, t0 + 0.3, "DEVAYANI", 860, 330, 32, t_out=tp)
    return dict(ui=ui, flash=flash_at(t, tp, 0.2))


# ------------------------------------------------------------------ y3  King Yayati pulls her out


WELL3 = (680, 0.8)
UP_ARM, HOLD_ARM = (-2.0, -0.2), (-1.5, -0.2)       # Devayani's hand reaching up out of the well / held out


def s_y3(cr, t, tl, t0, t1):
    c = cues(tl, "y3")
    tY, tH, tO = c["Y"], c["H"], c["O"]
    ground(cr)
    wx, ws = WELL3
    rim_y = FLOOR - X.WELL_H * ws
    glow(cr, 1000, 560, 560, 0.4)
    prop(cr, "sx_well_back", wx, FLOOR, ws)
    ys = 0.55
    # Yayati walks up to the well, leans and reaches in, then steps back as she climbs out
    t_out1 = min(tO + 0.95, t1 - 0.15)                 # she is pulled up inside the well, then steps over the rim
    t_up1 = min(tO + 0.1, t_out1 - 0.55)
    t_up0 = min(tO - 0.75, t_up1 - 0.6)
    if t < t_up1:
        x, bob, rock, legs = walking(t, t0 + 0.1, tY + 0.9, 1780, 990)
    else:
        x, bob, rock, legs = walking(t, t_up1, t_out1, 990, 1300, 0.3)
    reach_t = tH - 0.2
    lean = 0.34 * keyed(t, [(t0, 0.0), (reach_t, 1.0), (t_up1, 0.1)], 0.3, 1.2)
    hip = (x, FLOOR - 434 * ys + bob)
    u1 = ease(clamp((t - t_up0) / (t_up1 - t_up0)))
    u2 = ease(clamp((t - t_up1) / (t_out1 - t_up1)))
    dfront = mix(UP_ARM, HOLD_ARM, u2)
    hl = hand_local(dfront)
    h_in = (wx + 20, rim_y + 260 - 280 * u1)
    h_out = (wx + 330, FLOOR - 470 * SW)
    d_hip = (h_in[0] + (h_out[0] - h_in[0]) * u2, h_in[1] + (h_out[1] - h_in[1]) * u2 - 60 * math.sin(math.pi * u2))
    grip = (d_hip[0] + hl[0] * SW, d_hip[1] + hl[1] * SW)
    holding = t > tH - 0.05
    if t < reach_t:
        fr = (-0.32, -0.55)
    else:
        fr = reach(hip, ys, -lean, True, grip if holding else (wx + 190, rim_y + 6), 26 * 1.06)
        fr = mix((-0.32, -0.55), fr, prog(t, reach_t, 0.3))
    if holding:
        cr.save()
        well_clip(cr, wx, ws, inside=u2 < 0.02)
        deva(cr, t, d_hip[0], SW, mood="shut" if u1 < 0.6 else ("open" if u2 < 0.9 else "smile"), y=d_hip[1],
             front=dfront, backa=mix((-2.2, -0.4), (0.15, -0.2), u2), rods=u2 > 0.95)
        cr.restore()
    prop(cr, "sx_well_front", wx, FLOOR, ws)
    yayati(cr, t, x, ys, mood="calm", flip=True, y=hip[1], rot=rock - lean, legs=legs, front=fr,
           hits=[(tY + 0.9, 0.5)])
    if holding:
        glow(cr, grip[0], grip[1], 140, 0.5)

    def ui(cr):
        if t < tO - 0.25:
            head(cr, t, "THEN CAME", t0 + 0.04, "KING YAYATI", tY)
        else:
            head(cr, t, "HE PULLED HER OUT", tO - 0.25, "BY THE HAND", tO, under=tO + 0.5)
        tag(cr, t, tY + 0.2, "KING YAYATI", min(x + 200, 1700), 360, 32, t_out=tO - 0.2)
    return dict(ui=ui, flash=flash_at(t, tO, 0.15))


# ------------------------------------------------------------------ y4  "marry me"; the curse came true


def s_y4(cr, t, tl, t0, t1):
    c = cues(tl, "y4")
    tH, tM, tK, tR, tT = c["H"], c["M"], c["K"], c["R"], c["T"]
    ground(cr)
    glow(cr, 800, 560, 520, 0.45)
    dx_, yx = 640, 980
    ys = 0.55
    grip = (810, 620)
    dfr = reach((dx_, FLOOR - 470 * SW), SW, 0.0, False, grip, 22)
    yfr = reach((yx, FLOOR - 434 * ys), ys, 0.0, True, grip, 26 * 1.06)
    deva(cr, t, dx_, SW, mood="smile" if t > tM else "open", front=dfr, hits=[(tM, 0.3)], head=-0.04)
    yayati(cr, t, yx, ys, mood="smile" if t > tM + 0.5 else "calm", flip=True, front=yfr, hits=[(tK, 0.3)])
    glow(cr, grip[0], grip[1], 150, 0.5 + 0.2 * math.sin(t * 4))
    if t > tM:
        warm(cr, 810, 500, 300, 0.35 * prog(t, tM, 0.5))
    curse_card(cr, t, 1490, 640, 0.62, t_in=tK - 0.4, pin_t=tK - 0.4, tick_t=tT, rod=False)

    def ui(cr):
        if t < tK - 0.15:
            head(cr, t, "DEVAYANI SAID: YOU HELD MY HAND, SO", t0 + 0.04, "MARRY ME!", tM)
        elif t < tT - 0.15:
            head(cr, t, "YAYATI WAS", tK - 0.15, "A KING, NOT A SAGE'S SON", tR)
        else:
            head(cr, t, "SO KACHA'S CURSE", tT - 0.15, "CAME TRUE", tT, under=tT + 0.4)
        tag(cr, t, tK, "KING", yx + 200, 400, 32)
    return dict(ui=ui, flash=flash_at(t, tT, 0.25))


# ------------------------------------------------------------------ y5  in secret


def s_y5(cr, t, tl, t0, t1):
    c = cues(tl, "y5")
    tC, tS, tB = c["C"], c["S"], c["B"]
    ground(cr)
    warm(cr, 1150, 600, 620, 0.5)
    glow(cr, 1150, 560, 560, 0.5)
    dx_, ds = 400, 0.72
    shut = ease(clamp((t - tC + 0.2) / 0.7))
    prop(cr, "sx_door_frame", dx_, FLOOR, ds)
    for sg in (-1, 1):                                   # two door leaves swing shut
        cr.save()
        cr.translate(dx_ + sg * 190 * ds, FLOOR)
        cr.scale(-sg * ds * (0.12 + 0.88 * shut), ds)
        pc.paint_part(cr, "sx_door_leaf", 1.0)
        cr.restore()
    if shut < 0.9:
        glow(cr, dx_, FLOOR - 300 * ds, 200, 0.3 * (1 - shut))
    yayati(cr, t, 860, 0.55, mood="smile", front=(-1.2, -0.5), hits=[(tS, 0.3)])
    sharm(cr, t, 1130, SW, mood="smile", flip=True, front=(-1.1, -0.5), hits=[(tS, 0.3)])
    for i, kx in enumerate((1380, 1520, 1660)):
        ti = tB - 0.1 + 0.2 * i
        if t > ti - 0.3:
            b, k, a = depth(t, ti - 0.3, 0.4)
            puru(cr, t, kx, (0.30 - 0.025 * i) * k, mood="smile", flip=True, alpha=a, blur=b, ph=i * 1.3)
    lights(cr, t, 1150, 520, 360, 10, 0.4)

    def ui(cr):
        if t < tB - 0.2:
            head(cr, t, "YAYATI ALSO MARRIED SHARMISHTHA,", t0 + 0.04, "IN SECRET", tC + 0.2, under=tS + 0.3)
        else:
            head(cr, t, "AND HAD", tB - 0.2, "SONS WITH HER", tB)
    return dict(ui=ui, eve=0.15, flash=flash_at(t, tB, 0.12))


# ------------------------------------------------------------------ y6  Devayani runs to her father


def s_y6(cr, t, tl, t0, t1):
    c = cues(tl, "y6")
    tP, tC, tF = c["P"], c["C"], c["F"]
    ground(cr)
    glow(cr, 420, 560, 460, 0.4)
    far = 1 - prog(t, tC + 0.6, 0.6)
    if far > 0.01:
        sil(cr, lambda c_: (yayati(c_, t, 1600, 0.36, feet=FLOOR - 60, rods=False, mood="smile"),
                            sharm(c_, t, 1740, 0.38, feet=FLOOR - 60, flip=True, rods=False)), 0.55 * far)
    turn = t > tC - 0.1
    x, bob, rock, legs = walking(t, tC, tF + 0.5, 1280, 760, 0.3)
    sh_turn = t > tF + 0.4
    shukra(cr, t, 420, SM, mood="shock" if sh_turn else "calm",
           front=(-1.4, -0.4) if sh_turn else (-0.4, -0.6), hits=[(tF + 0.4, 0.4)])
    dp = deva(cr, t, x, SW, mood="weep" if turn else "angry", flip=turn, y=FLOOR - 470 * SW + bob, rot=rock,
              front=WEEP["front"] if turn else (-0.6, -1.6), backa=WEEP["backa"] if turn else (0.15, -0.2),
              head=0.15 if turn else -0.05)
    eye = to_user(cr, dp["head"])
    if turn:
        for i in range(8):
            u = (t - tC - 0.3 * i) / 0.8
            if 0 < u < 1:
                prop(cr, "rr_tear", eye[0] + 40 + 140 * u, eye[1] + 30 + 160 * u * u, 0.85, alpha=1 - u)

    def ui(cr):
        if t < tC - 0.15:
            head(cr, t, "DEVAYANI", t0 + 0.04, "FOUND OUT", tP)
        else:
            head(cr, t, "SHE RAN, CRYING,", tC - 0.15, "TO HER FATHER", tF)
        big_mark(cr, t, tP, "!", 1330, 330, 150, alpha=1 - prog(t, tC, 0.3))
        tag(cr, t, tF + 0.3, "SHUKRA", 420, 300, 32)
    return dict(ui=ui, flash=flash_at(t, tP, 0.15))


# ------------------------------------------------------------------ y7  old, right now


def s_y7(cr, t, tl, t0, t1):
    c = cues(tl, "y7")
    tC, tA, tO = c["C"], c["A"], c["O"]
    ground(cr)
    glow(cr, 460, 560, 460, 0.4)
    glow(cr, 1380, 560, 460, 0.4)
    sx, yx, ys = 470, 1380, 0.55
    point = keyed(t, [(t0, 0.0), (tC - 0.1, 1.0)], 0.3, 1.4)
    fr = mix((-0.4, -0.6), aim(sx, FLOOR - 434 * SM, SM, (yx, 560)), point)
    sp = shukra(cr, t, sx, SM, mood="angry" if t > tC - 0.15 else "calm", front=fr, hits=[(tC, 0.4)])
    old = prog(t, tO, 0.12)
    yayati(cr, t, yx, ys, mood="shock" if t > tC else "calm", old=old, flip=True,
           front=(-1.3, -1.6) if tC < t < tO else (STICK if old > 0.5 else (-0.32, -0.55)),
           hits=[(tO, 0.6)])
    if tC < t < tO + 0.5:
        hand = to_user(cr, sp["handF"])
        crack(cr, t, hand, (yx - 30, 560), prog(t, tC, 0.25) * (1 - prog(t, tO + 0.2, 0.3)), seed=3)
    burst(cr, t, yx, 560, tO, n=20, rmax=520, alpha=0.9)

    def ui(cr):
        if t < tA - 0.15:
            head(cr, t, "SHUKRA CURSED", t0 + 0.04, "YAYATI", tC)
        else:
            head(cr, t, "SHUKRA'S CURSE:", tA - 0.15, "OLD... RIGHT NOW!", tA, under=tO)
    return dict(ui=ui, flash=flash_at(t, tO, 0.55))


# ------------------------------------------------------------------ y8  one way out


def s_y8(cr, t, tl, t0, t1):
    c = cues(tl, "y8")
    tR, tJ, tB = c["R"], c["J"], c["B"]
    ground(cr)
    glow(cr, 960, 470, 560, 0.45)
    one = keyed(t, [(t0, 0.0), (tR, 1.0)], 0.3, 1.3)
    shukra(cr, t, 400, SM, mood="calm", front=mix((-0.4, -0.6), (-2.3, -0.9), one), hits=[(tR, 0.3)])
    yayati(cr, t, 1520, 0.55, mood="shame", old=1.0, flip=True, hits=[(tB, 0.3)])
    card2(cr, t, tR + 0.1, 960, 470, 1.0, [("UNLESS SOMEONE", 76, INK, -42, tJ - 0.2),
                                          ("TAKES YOUR OLD AGE", 76, RED, 46, tB - 0.1)])
    if t > tB + 0.2:
        medal(cr, 790, 700, 58, "YOUTH", "sx_medal_gold", prog(t, tB + 0.2, 0.3), 26)
        medal(cr, 1130, 700, 58, "OLD AGE", "sx_medal", prog(t, tB + 0.3, 0.3), 24)
        q = prog(t, tB + 0.4, 0.4)
        for sg in (-1, 1):
            arc = [(960 + 100 * math.cos(math.pi * u) * -sg, 700 + sg * 50 * math.sin(math.pi * u))
                   for u in (i / 20 for i in range(21))]
            dotted(cr, arc, q, 16, 4.5, RED)

    def ui(cr):
        head(cr, t, "BUT THERE WAS", t0 + 0.04, "ONE WAY OUT", tR)
    return dict(ui=ui, flash=flash_at(t, tB, 0.12))


# ------------------------------------------------------------------ y9 / y10  four sons say no; Puru says yes


SONS = (1100, 1265, 1430, 1595)
PURU9 = (1760, 0.45)


def sons_row(cr, t, a=1.0, tN=None, puru_a=1.0):
    store = {}

    def f(c_):
        for i, x in enumerate(SONS):
            nod = 0.0
            if tN is not None and t > tN + 0.4 * i:
                dt = t - tN - 0.4 * i
                nod = 0.22 * math.sin(2 * math.pi * 2.2 * dt) * math.exp(-2.2 * dt)
            store[i] = puru(c_, t, x, 0.5 - 0.01 * i, mood="calm", flip=True, rods=False, head=nod, ph=0.8 * i)
        if puru_a > 0.01:
            store["p"] = puru(c_, t, PURU9[0], PURU9[1], flip=True, rods=False, ph=3.1)
    sil(cr, f, a)
    return store


def s_y9(cr, t, tl, t0, t1):
    c = cues(tl, "y9")
    tB, tJ, tF, tN = c["B"], c["J"], c["F"], c["N"]
    ground(cr)
    glow(cr, 400, 560, 440, 0.4)
    glow(cr, 1400, 600, 560, 0.35)
    ask = keyed(t, [(t0, 0.0), (tJ - 0.1, 1.0)], 0.3, 1.3)
    yayati(cr, t, 400, 0.55, mood="shame", old=1.0, front=mix(STICK, (-1.5, -0.3), ask), stick=True,
           hits=[(tJ, 0.3)])
    st = sons_row(cr, t, 1.0, tF, 0.7)

    def ui(cr):
        if t < tF - 0.15:
            head(cr, t, "YAYATI ASKED HIS SONS:", t0 + 0.04, "GIVE ME YOUR YOUTH", tJ)
        else:
            head(cr, t, "FOUR SONS SAID", tF - 0.15, "NO", tN)
        for i, x in enumerate(SONS):
            q = prog(t, tF + 0.4 * i, 0.25)
            if q > 0:
                top = to_user(cr, st[i]["top"])
                plaque(cr, "NO", x - 8, top[1] - 34, 46, RED, q)
    return dict(ui=ui, flash=flash_at(t, tN, 0.12))


def s_y10(cr, t, tl, t0, t1):
    c = cues(tl, "y10")
    tC, tP, tJ = c["C"], c["P"], c["J"]
    ground(cr)
    glow(cr, 400, 560, 440, 0.4)
    yayati(cr, t, 400, 0.55, mood="shock" if t > tJ else "shame", old=1.0, stick=True, hits=[(tJ, 0.3)])
    lit = prog(t, tC - 0.1, 0.4)
    sons_row(cr, t, 1.0 - 0.45 * lit, None, 1 - lit)
    x, bob, rock, legs = walking(t, tP - 0.1, tP + 1.5, PURU9[0], 860, 0.36)
    u = clamp((x - PURU9[0]) / (860 - PURU9[0]))
    s = PURU9[1] + (0.55 - PURU9[1]) * u
    feet = FLOOR + 10 * u
    if lit > 0.01:
        glow(cr, x, 600, 360, 0.55 * lit)
        offer = keyed(t, [(t0, 0.0), (tJ - 0.1, 1.0)], 0.3, 1.3)
        puru(cr, t, x, s, mood="smile" if t > tJ else "calm", flip=True, y=feet - 434 * s + bob, rot=rock,
             legs=legs, alpha=lit, front=mix((-0.32, -0.55), OFFER["front"], offer),
             backa=mix((0.3, -0.25), OFFER["backa"], offer), hits=[(tJ, 0.4)])
        if lit < 0.99:
            sil(cr, lambda c_: puru(c_, t, PURU9[0], PURU9[1], flip=True, rods=False, ph=3.1), 1 - lit)

    def ui(cr):
        if t < tJ - 0.15:
            head(cr, t, "THE YOUNGEST SON,", t0 + 0.04, "PURU", tP)
        else:
            head(cr, t, "PURU SAID:", tJ - 0.15, "TAKE MY YOUTH", tJ, under=tJ + 0.4)
        tag(cr, t, tP + 0.2, "PURU, THE YOUNGEST", min(x, 1600), 330, 30)
    return dict(ui=ui, flash=flash_at(t, tJ, 0.2))


# ------------------------------------------------------------------ y11 / y13  the swap


def swap_scene(cr, t, ts, back_=False, crown_t=None):
    """Yayati (left) and Puru (right); at ts youth passes from Puru to Yayati (back_: from Yayati back to Puru)."""
    ground(cr)
    glow(cr, 480, 560, 440, 0.4)
    glow(cr, 1440, 560, 440, 0.4)
    q = prog(t, ts, 0.15)
    y_old = q if back_ else 1 - q
    p_old = 1 - q if back_ else q
    yp = yayati(cr, t, 480, 0.55, mood="smile" if y_old < 0.5 else "shame", old=y_old, hits=[(ts, 0.5)])
    king = crown_t is not None and t > crown_t + 0.45
    pp = puru(cr, t, 1440, 0.55, mood="smile" if p_old < 0.5 else "shame", old=p_old, flip=True, king=king,
              hits=[(ts, 0.5)] + ([(crown_t + 0.45, 0.3)] if crown_t else []))
    yc, pcst = to_user(cr, yp["chest"]), to_user(cr, pp["chest"])
    src, dst = (yc, pcst) if back_ else (pcst, yc)
    flow(cr, t, ts - 0.7, ts - 0.1, src, dst, n=10, lift=200)
    burst(cr, t, dst[0], dst[1], ts, n=16, rmax=420, alpha=0.8)
    burst(cr, t, src[0], src[1], ts, n=10, rmax=260, alpha=0.4)
    if crown_t is not None and t > crown_t - 0.5 and not king:
        top = to_user(cr, pp["head"])
        u = clamp((t - crown_t + 0.5) / 0.95)
        prop(cr, "kk_crown", top[0] + 4, top[1] - 34 - 520 * (1 - u) ** 2, 0.36, rot=0.3 * (1 - u))
    if king:
        burst(cr, t, pcst[0], pcst[1] - 160, crown_t + 0.45, n=14, rmax=360, alpha=0.7)
        aura(cr, t, pcst[0], pcst[1] - 180, 90, 300, 0.35 * prog(t, crown_t + 0.45, 0.5), n=14, spin=0.08)
    return yp, pp


def s_y11(cr, t, tl, t0, t1):
    c = cues(tl, "y11")
    tH, tY, tO = c["H"], c["Y"], c["O"]
    ts = t0 + 0.45
    swap_scene(cr, t, ts)
    yrs = int(1000 * ease(clamp((t - tH) / max(1.0, t1 - tH - 0.4))))
    if t > tH - 0.2:
        a = prog(t, tH - 0.2, 0.3)
        plaque(cr, f"{yrs} YEARS", 960, 520, 96, RED, a, pad=(70, 40))

    def ui(cr):
        head(cr, t, "FATHER YOUNG, SON OLD:", t0 + 0.04, "FOR 1000 YEARS", tH)
        tag(cr, t, ts + 0.2, "YOUNG", 480, 330, 30)
        tag(cr, t, ts + 0.3, "OLD", 1440, 330, 30)
    return dict(ui=ui, flash=flash_at(t, ts, 0.35))


def s_y13(cr, t, tl, t0, t1):
    c = cues(tl, "y13")
    tJ, tL, tK = c["J"], c["L"], c["K"]
    ts = tL
    swap_scene(cr, t, ts, back_=True, crown_t=tK - 0.2)

    def ui(cr):
        if t < tK - 0.15:
            head(cr, t, "YAYATI GAVE BACK", t0 + 0.04, "PURU'S YOUTH", tJ)
        else:
            head(cr, t, "AND MADE PURU", tK - 0.15, "KING", tK + 0.3, under=tK + 0.8)
        tag(cr, t, tK + 0.3, "KING PURU", 1690, 430, 32)
    return dict(ui=ui, flash=flash_at(t, ts, 0.3) + flash_at(t, tK + 0.45, 0.25))


# ------------------------------------------------------------------ y12  fire with ghee


def s_y12(cr, t, tl, t0, t1):
    c = cues(tl, "y12")
    tI, tN, tG, tF = c["I"], c["N"], c["G"], c["F"]
    ground(cr)
    glow(cr, 440, 560, 440, 0.4)
    yayati(cr, t, 440, 0.55, mood="shame" if t < tG else "calm", front=(-0.3, -2.3) if t < tG else (-1.3, -0.4),
           head=0.12 if t < tG else 0.0, hits=[(tI, 0.3), (tG, 0.3)])
    fx = 1260
    pour = prog(t, tG - 0.3, 0.35)
    flare = prog(t, tF - 0.2, 0.35)
    flame_fire(cr, t, fx, FLOOR, 1.25, flare=0.25 * pour + 0.75 * flare)
    if pour > 0.01:
        lx, ly = 1080, 380
        prop(cr, "sx_lota", lx, ly, 0.9, rot=0.75 * pour)
        sp = (lx + 150 * math.cos(0.75 * pour) + 60 * math.sin(0.75 * pour),
              ly + 150 * math.sin(0.75 * pour) - 70 * math.cos(0.75 * pour))
        end = (fx - 20, FLOOR - 160)
        pts = [(sp[0] + (end[0] - sp[0]) * u + 30 * math.sin(math.pi * u), sp[1] + (end[1] - sp[1]) * u)
               for u in (i / 20 for i in range(21))]
        cr.save()
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        for lw, col, al in ((16, (0.85, 0.6, 0.12), 0.9), (7, (1.0, 0.86, 0.4), 0.95)):
            cr.move_to(*pts[0])
            for p in pts[1:]:
                cr.line_to(*p)
            cr.set_source_rgba(*col, al * pour)
            cr.set_line_width(lw)
            cr.stroke()
        cr.restore()
        pc.rod(cr, lx - 40, ly + 60, lx - 80, H + 60, alpha=0.5 * pour)
    if flare > 0:
        burst(cr, t, fx, FLOOR - 260, tF - 0.1, n=16, rmax=480, alpha=0.6)

    def ui(cr):
        if t < tG - 0.2:
            head(cr, t, "AFTER 1000 YEARS, YAYATI SAID:", t0 + 0.04, "DESIRE NEVER ENDS", tN)
        else:
            head(cr, t, "DESIRE NEVER ENDS:", tG - 0.2, "LIKE FIRE WITH GHEE", tF - 0.1, under=tF + 0.3)
        tag(cr, t, tG, "GHEE", 880, 400, 30)
    return dict(ui=ui, flash=flash_at(t, tF, 0.3))


# ------------------------------------------------------------------ y14 / y15  the family tree


TREE_BROWN = (0.55, 0.32, 0.14)


def branch(cr, pts, p, w=16.0, alpha=1.0, col=TREE_BROWN):
    if p <= 0.01 or alpha <= 0.01:
        return
    q = partial(pts, p)
    if len(q) < 2:
        return
    cr.save()
    cr.push_group()
    pc.band(cr, q, w, col, holes=True, lw=3.5, hole_r=2.4, spacing=16)
    pat = cr.pop_group()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source(pat)
    cr.paint_with_alpha(alpha)
    cr.restore()


PURU_M = (420, 330)
KURU_M = (700, 500)
YADU_M = (1520, 330)
PANDAVA_X = (300, 420, 540)
KAURAVA_X = (830, 920, 1010, 1100)


def puru_tree(cr, t, tP, tD, tK, a=1.0, t_puru=-99.0):
    trunk = [(PURU_M[0], PURU_M[1] + 70), (450, 410), (560, 460), (KURU_M[0] - 40, KURU_M[1] - 10)]
    branch(cr, trunk, clamp((t - tP) / 0.8), 18, a)
    if t > tP + 0.3:
        draw_text(cr, "MANY GENERATIONS LATER", 470, 500, 24, INK, prog(t, tP + 0.3, 0.4) * a, MONO_FONT, "cm", 2)
    lb = [(KURU_M[0] - 30, KURU_M[1] + 30), (560, 560), (420, 580)]
    rb = [(KURU_M[0] + 30, KURU_M[1] + 30), (840, 560), (965, 580)]
    branch(cr, lb, clamp((t - tD + 0.6) / 0.5), 14, a)
    branch(cr, rb, clamp((t - tK + 0.5) / 0.5), 14, a)
    medal(cr, PURU_M[0], PURU_M[1], 72, "PURU", "sx_medal_gold", a * prog(t, t_puru, 0.3), 34, pop=t_puru, t=t)
    medal(cr, KURU_M[0], KURU_M[1], 46, "KURU", "sx_medal", a * prog(t, tP + 0.7, 0.3), 24)
    pa = prog(t, tD - 0.1, 0.4) * a
    if pa > 0.01:
        glow(cr, 420, 760, 320, 0.4 * pa)
        yudh(cr, t, PANDAVA_X[0], 0.24, feet=FLOOR, flip=False, alpha=pa, rods=False)
        fig(cr, C.BHIMA, "bhima", t, PANDAVA_X[1], 0.22, feet=FLOOR, alpha=pa, rods=False, ph=1.2)
        fig(cr, J.ARJUNA, "jd_arjuna", t, PANDAVA_X[2], 0.24, feet=FLOOR, alpha=pa, rods=False, ph=2.1)
        plaque(cr, "PANDAVAS", 420, 600, 34, INK, pa)
    ka = prog(t, tK - 0.1, 0.4) * a
    if ka > 0.01:
        glow(cr, 965, 760, 320, 0.35 * ka)
        sil(cr, lambda c_: [fig(c_, C.KING, "king", t, x, 0.22, feet=FLOOR, flip=True, rods=False, ph=i * 0.9)
                            for i, x in enumerate(KAURAVA_X)], ka, (0.16, 0.10, 0.06))
        plaque(cr, "KAURAVAS", 965, 600, 34, INK, ka)


def s_y14(cr, t, tl, t0, t1):
    c = cues(tl, "y14")
    tT, tP, tD, tK = c["T"], c["P"], c["D"], c["K"]
    ground(cr)
    puru_tree(cr, t, tP, tD, tK, t_puru=t0 + 0.15)
    b, k, a = depth(t, t0 + 0.1, 0.5)
    glow(cr, 1380, 640, 380, 0.45 * a)
    puru(cr, t, 1380, 0.46 * k, mood="smile", king=True, flip=True, alpha=a, blur=b, front=(-1.2, -0.6))

    def ui(cr):
        if t < tP - 0.1:
            head(cr, t, "AND NOW, THE BIGGEST", t0 + 0.04, "TWIST", tT)
        else:
            head(cr, t, "PURU'S LINE:", tP - 0.1, "PANDAVAS & KAURAVAS", tD, under=tK + 0.3)
        tag(cr, t, t0 + 0.4, "KING PURU", 1610, 470, 30)
    return dict(ui=ui, flash=flash_at(t, tT, 0.15))


def s_y15(cr, t, tl, t0, t1):
    c = cues(tl, "y15")
    tY, tN, tK = c["Y"], c["N"], c["K"]
    ground(cr)
    puru_tree(cr, t, -99, -99, -99, a=1 - 0.5 * prog(t, t0, 0.5))
    medal(cr, YADU_M[0], YADU_M[1], 72, "YADU", "sx_medal_gold", prog(t, tY - 0.2, 0.3), 34, pop=tY - 0.2, t=t)
    if t > tN:
        q = prog(t, tN, 0.3)
        draw_text(cr, "SAID NO", YADU_M[0] + 170, YADU_M[1], 30, RED, q, MONO_FONT, "cm", 3)
    line = [(YADU_M[0], YADU_M[1] + 72), (1540, 430), (1500, 520), (1520, 575)]
    branch(cr, line, clamp((t - tN - 0.2) / max(0.8, tK - tN - 0.4)), 16)
    if t > tN + 0.4:
        draw_text(cr, "MANY GENERATIONS LATER", 1300, 470, 24, INK, prog(t, tN + 0.4, 0.4), MONO_FONT, "cm", 2)
    ka = prog(t, tK - 0.15, 0.4)
    if ka > 0.01:
        glow(cr, 1520, 740, 380, 0.6 * ka)
        aura(cr, t, 1520, 720, 80, 320, 0.4 * ka, n=16, spin=0.06)
        b, k, a = depth(t, tK - 0.15, 0.5)
        fig(cr, C.KRISHNA, "krishna", t, 1520, 0.3 * k, feet=FLOOR, flip=True, alpha=a, blur=b, rods=False,
            front=(-0.9, -1.2), ph=0.7)
        plaque(cr, "KRISHNA", 1520, 600, 38, RED, ka)

    def ui(cr):
        if t < tK - 0.15:
            head(cr, t, "AND YADU, WHO SAID", t0 + 0.04, "NO", tN)
        else:
            head(cr, t, "YADU'S LINE:", tK - 0.15, "KRISHNA", tK, under=tK + 0.4)
    return dict(ui=ui, flash=flash_at(t, tK, 0.3))


# ------------------------------------------------------------------ o1 / o2  the six again


def grid_xy(i):
    """Top-left of panel i (1-6) in the 3 x 2 grid."""
    return 170 + ((i - 1) % 3) * 540, 300 + ((i - 1) // 3) * 345


GRID_W = 500.0


def s_o1(cr, t, tl, t0, t1):
    c = cues(tl, "o1")
    for i in range(1, 7):
        x, y = grid_xy(i)
        ti = c[f"P{i}"]
        e = ease((t - t0 - 0.06 * i) / 0.45)
        on = prog(t, ti - 0.1, 0.3)
        k = 1.0 + 0.05 * math.sin(math.pi * clamp((t - ti + 0.1) / 0.4)) if t > ti - 0.1 else 1.0
        w = GRID_W * k
        panel(cr, t, i, x - (w - GRID_W) / 2, y - (w - GRID_W) * 9 / 32 + 60 * (1 - e), w, alpha=e,
              dim=1 - on, lit=on * (1 - prog(t, ti + 1.2, 0.6)) + 0.0)
        if on > 0:
            plaque(cr, PANEL_NAMES[i], x + GRID_W / 2, y + GRID_W * 9 / 16 + 4, 30, RED if t < ti + 1.2 else INK, on)

    def ui(cr):
        head(cr, t, "SO THESE WERE", t0 + 0.04, "SIX TRUE STORIES", c["S"])
    return dict(ui=ui, flash=sum(flash_at(t, c[f"P{i}"], 0.08) for i in range(1, 7)))


def s_o2(cr, t, tl, t0, t1):
    c = cues(tl, "o2")
    tQ, tN, tC = c["Q"], c["N"], c["C"]
    hop = int(max(0.0, t - tQ) / 0.45) % 6 + 1 if t > tQ else 0
    for i in range(1, 7):
        x, y = grid_xy(i)
        h = GRID_W * 9 / 16
        panel(cr, t, i, x, y, GRID_W, dim=0.45, badge=False, lit=1.0 if i == hop else 0.0)
        medal(cr, x + GRID_W / 2, y + h / 2, 70, str(i), "sx_medal_red", 1.0, 90, LIGHT,
              pop=tQ + 0.45 * (i - 1) if t < tQ + 2.8 else None, t=t)
        if i == hop:
            red_ring(cr, x + GRID_W / 2, y + h / 2, 150, 120, prog(t, tQ + 0.45 * ((t - tQ) // 0.45), 0.25), 9)

    def ui(cr):
        if t < tN - 0.15:
            head(cr, t, "WHICH ONE", t0 + 0.04, "SHOCKED YOU MOST?", tQ)
        else:
            head(cr, t, "WHICH ONE SHOCKED YOU MOST?", tN - 0.15, "COMMENT 1-6", tC, under=tC + 0.4)
    return dict(ui=ui, flash=flash_at(t, tC, 0.15))


# ------------------------------------------------------------------ the frame


SHOTS = {f"i{k}": (make_intro(k), {"z": (1.0, 1.02), "cont": k > 1}) for k in range(1, 7)}
SHOTS.update({
    "i7": (s_i7, {"z": (1.0, 1.03)}),
    "i8": (s_i8, {"z": (1.0, 1.02)}),
    "k1": (s_k1, {"z": (1.0, 1.03)}),
    "k2": (s_k2, {"z": (1.0, 1.04)}),
    "k3": (s_k3, {"z": (1.0, 1.03)}),
    "k4": (s_k4, {"z": (1.0, 1.03)}),
    "k5": (s_k5, {"z": (1.0, 1.05)}),
    "k6": (s_k6, {"z": (1.0, 1.03)}),
    "k7": (s_k7, {"z": (1.0, 1.03)}),
    "k8": (s_k8, {"z": (1.0, 1.03)}),
    "k9": (s_k9, {"z": (1.0, 1.06), "focus": (720, 640)}),
    "k10": (s_k10, {"z": (1.0, 1.03)}),
    "k11": (s_k11, {"z": (1.0, 1.03)}),
    "k12": (s_k12, {"z": (1.02, 1.07), "focus": (720, 640)}),
    "k13": (s_k13, {"z": (1.0, 1.03)}),
    "k14": (s_k14, {"z": (1.0, 1.03)}),
    "k15": (s_k15, {"z": (1.0, 1.03)}),
    "k16": (s_k16, {"z": (1.0, 1.04)}),
    "k17": (s_k17, {"z": (1.0, 1.05), "focus": (960, 520)}),
    "y1": (s_y1, {"z": (1.0, 1.03)}),
    "y2": (s_y2, {"z": (1.0, 1.04)}),
    "y3": (s_y3, {"z": (1.0, 1.03)}),
    "y4": (s_y4, {"z": (1.0, 1.03)}),
    "y5": (s_y5, {"z": (1.0, 1.03)}),
    "y6": (s_y6, {"z": (1.0, 1.03)}),
    "y7": (s_y7, {"z": (1.0, 1.04)}),
    "y8": (s_y8, {"z": (1.0, 1.03)}),
    "y9": (s_y9, {"z": (1.0, 1.03)}),
    "y10": (s_y10, {"z": (1.0, 1.03), "cont": True}),
    "y11": (s_y11, {"z": (1.0, 1.03)}),
    "y12": (s_y12, {"z": (1.0, 1.03)}),
    "y13": (s_y13, {"z": (1.0, 1.03), "cont": False}),
    "y14": (s_y14, {"z": (1.0, 1.02)}),
    "y15": (s_y15, {"z": (1.0, 1.02), "cont": True}),
    "o1": (s_o1, {"z": (1.0, 1.02)}),
    "o2": (s_o2, {"z": (1.0, 1.0), "cont": True}),
})


def active(tl, t):
    """The active line at t (the last one that has started), its start and the next line's start."""
    st = getattr(tl, "_six_a_starts", None)
    if st is None:
        st = tl._six_a_starts = [b.start for b in tl.beats]
    i = max(0, bisect.bisect_right(st, t) - 1)
    b = tl.beats[i]
    t1 = tl.beats[i + 1].start if i + 1 < len(tl.beats) else tl.total
    return b, (0.0 if i == 0 else b.start), t1


def draw(cr, t, tl):
    b, t0, t1 = active(tl, t)
    fn, opt = SHOTS[b.id]
    z0, z1 = opt.get("z", (1.0, 1.03))
    z = z0 + (z1 - z0) * clamp((t - t0) / max(0.5, t1 - t0))
    fx, fy = opt.get("focus", (960, 620))
    cr.save()
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    stage(cr)
    out = fn(cr, t, tl, t0, t1) or {}
    tint(cr, (1.0, 0.66, 0.42), out.get("eve", 0.0))
    cr.restore()
    motes(cr, t)
    night = out.get("night", 0.0)
    lamp(cr, t, night=night, flash=out.get("flash", 0.0))
    title_lift(cr, out.get("lift", 0.0) * min(1.0, 2.5 * night))
    if out.get("ui"):
        out["ui"](cr)
    if not opt.get("cont") and t0 > 0 and t - t0 < 0.22:      # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur) for the intro, story 1, story 6 and the outro, sparse (owner, 8 Nov 2026: "only use sounds
    where necessary"; at most three per story): a damaru on the hook; story 1: a conch on its chapter card, a shimmer
    as the guru's belly lights up, a hit on the burst of light; story 6: a conch on its chapter card, a hit as Yayati
    turns old, a bell on Krishna; a bell on the closing question. Each at least SFX_MIN_GAP from every sound already
    kept (render_myth.calm_sfx also keeps them apart across the whole video); the bed dips before the big reveals."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["k1"]["t0"], "conch", 0), (c["y1"]["t0"], "conch", 0),
            (c["k9"]["P"], "shimmer", 0), (c["k13"]["O"], "hit", 0), (c["y7"]["O"], "hit", 0),
            (c["y15"]["K"], "bell", 0), (c["o2"]["C"], "bell", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["k9"]["P"] - 0.35, "dip", 0.5), (c["k10"]["V"] - 0.3, "dip", 0.45), (c["y7"]["O"] - 0.3, "dip", 0.5),
            (c["y15"]["K"] - 0.35, "dip", 0.5)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
