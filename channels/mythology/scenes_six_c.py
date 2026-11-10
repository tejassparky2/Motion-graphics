"""Scenes for stories 3 and 4 of the long video (videos/six_stories.py, 1920x1080, Hindi): Agastya who drank the ocean
(Mahabharata, Vana Parva 101-109; lines g1-g11) and Rishyashringa, the boy who had never seen a woman (Vana Parva
110-113, Valmiki Ramayana Bala Kanda 9-11 and 14-15; lines s1-s13). scenes_six_stories routes every moment whose
active line is g* or s* here; draw() paints the whole frame.

Togalu Gombeyaata leather shadow puppets as in the reels (cast: six_cast_c, plus Indra from mandhata_cast and
Dasharatha from kaikeyi_cast) on the same wide cloth, lamp, floor (FL = 892), headline (56 / 118 px, fitted to
1460 px) and palm-leaf chapter card (held 2.7 s, then it flies up) as scenes_six_b: two characters on the left and
right thirds, cards and props in the free third, a two-tier headline at the top centre (small dark setup line + one
big red key line). A visible change every 2-3 s; every step said plainly and put on screen as a simple label so a
child can follow.

Respect and no gore: the Kalakeyas are dark shadows (no faces beyond cut-out eyes and tusks); their night raids show
only the sages' hut lamps going out; the battle is flashes of light, two asuras topple and dissolve into dust and
the rest run into Patala; the gods, Agastya, Brahma, Ganga and King Dasharatha keep their dignity; Agastya's "I've
digested it" is a calm smile and a pat on the belly; baby Rama sleeps in a cradle in soft light.

Shot list (line: what is on the screen)
  g1  chapter card STORY 3 OF 6, THE SAGE WHO / DRANK THE OCEAN, MAHABHARATA · VANA PARVA; it flies up and the sea
      fades in, four horned shadows standing in it (tag KALAKEYA ASURAS), the sun rising; the shadows sink under the
      waves one by one, bubbles: BY DAY, THEY HID IN THE / OCEAN
  g2  night, a moon: the shadows rise out of the sea and stalk toward three huts in the forest, their eyes glowing;
      each hut's lamp goes out (a wisp of smoke): BY NIGHT, / THEY CAME OUT, then BY NIGHT, THEY / KILLED SAGES
  g3  dim: three gods on a cliff hold lamps over a huge, deep, dark ocean; the shadows hide on the far sea floor;
      red "?" over the gods: THE GODS COULD NOT / FIND THEM; a red arrow across the sea and one down into it: THE
      OCEAN WAS / TOO BIG, TOO DEEP
  g4  Agastya's hermitage: short, stout Agastya with his kamandalu (tag SAGE AGASTYA); the gods walk in and bow; a
      speech cloud ONLY YOU CAN HELP US!: THE GODS WENT TO / SAGE AGASTYA, then THE GODS SAID: / DRINK THE OCEAN!
  g5  Agastya on the shore bank, the sea beside him: AGASTYA WENT TO / THE SEA SHORE; a whirlpool turns, a twisting
      stream of water rises into his mouth and the sea level drains to a dry bed, the fish left flapping on the sand:
      HE DRANK IT / ALL!; the last drop flies up to him: stamp NOT ONE DROP LEFT
  g6  the dry sea floor: the crouching shadows are exposed ("!"): THE OCEAN DRIED UP. / THE ASURAS WERE SEEN!; the
      gods charge in, flashes of the vajra, two asuras topple and dissolve into dust: THE GODS / DEFEATED THEM; the
      rest run into a dark hole (tag THE UNDERWORLD): THE REST RAN AWAY TO / PATALA
  g7  Agastya on the shore, Indra before him with joined hands, the empty bed behind with a dotted line where the
      water was (THE OCEAN WAS HERE); a red arrow curving back into the bed: THE GODS SAID: / NOW FILL IT BACK!
  g8  close: Agastya smiles and pats his round belly; the gods start back, "!": AGASTYA SMILED: / I'VE DIGESTED IT!
  g9  the wide empty sea bed (EMPTY): THE OCEAN STAYED / EMPTY; the gods walk across it toward a light where Brahma
      appears on his lotus: SO THE GODS WENT TO / BRAHMA
  g10 Brahma (three of his four faces showing) on the lotus, blessing; a vision cloud: LONG, LONG AFTER..., then a
      small King Bhagiratha praying in it (tag KING BHAGIRATHA), then a little sea filling in it: BRAHMA SAID: ONE
      DAY, / BHAGIRATHA WILL FILL IT
  g11 Bhagiratha praying, a glow of tapas: BHAGIRATHA / PRAYED; Ganga comes down from the clouds, her body below
      the waist a ribbon of river water reaching back to the sky (tag GANGA): AND GANGA CAME / DOWN TO EARTH; water
      pours from her into the empty bed, the sea rises, waves and fish come back: GANGA FILLED THE / EMPTY OCEAN
  s1  chapter card STORY 4 OF 6, THE BOY WHO HAD / NEVER SEEN A WOMAN, MAHABHARATA · VANA PARVA & RAMAYANA; it
      flies up and the forest hut fades in, the sage (tag SAGE VIBHANDAKA) and his son (tag HIS SON): A SAGE IN THE
      FOREST, AND HIS SON: / RISHYASHRINGA
  s2  close on the boy's face: a small horn on his forehead (ringed, tag A SMALL HORN): ON HIS FOREHEAD: / A SMALL
      HORN; a spotted doe steps in and nuzzles him, he smiles (tag HIS MOTHER): THE MAHABHARATA SAYS: / HIS MOTHER
      WAS A DOE
  s3  a thought bubble over the puzzled boy: only his father's face (FATHER, a tick); dotted outlines of other people
      with "?": EXCEPT HIS FATHER, HE / NEVER SAW ANYONE ELSE; a woman's dotted outline with a big red "?": AND A
      WOMAN? / NEVER!
  s4  Anga: cracked earth, a hard sun with heat haze, a plaque counting NO RAIN: 1 YEAR ... MANY YEARS: MEANWHILE,
      IN THE KINGDOM OF ANGA: / NO RAIN FOR YEARS; green crops wither, a farmer and a village woman look down: THE
      FIELDS DRIED UP, / PEOPLE WENT HUNGRY
  s5  the palace gate: King Lomapada (tag) and two Brahmins (tag); a plaque IF THE FOREST BOY COMES, / RAIN WILL
      COME!: THE BRAHMINS TOLD THE KING: / BRING THE FOREST BOY
  s6  a big red "?": BUT HOW WOULD HE / LEAVE THE FOREST?; the king points, three women in bright saris (one with a
      plate of fruit-shaped sweets) walk off to the forest: SO THE KING SENT SOME / WOMEN TO THE FOREST
  s7  the forest: the boy stares ("?"), the women before him: HE THOUGHT: / STRANGE SAGES?; their saris ringed
      (DIFFERENT CLOTHES), little talk marks (DIFFERENT TALK); a woman holds out the plate, a "fruit" flies to him, he
      tastes it, sparkles: HE THOUGHT: / SWEET FRUITS?
  s8  close: the "fruit" splits in two, a laddu inside (tag A LADDU INSIDE!): THEY WERE NOT FRUITS. THEY WERE /
      SWEETS!; the boy, smiling, holds a half: IT WAS HIS / FIRST SWEET EVER
  s9  the boat-hermitage (a hut on a boat, flowers) floating down the river, the banks sliding by, the boy and the
      women aboard: THE WOMEN TOOK HIM ON A / BOAT-HERMITAGE; a post ANGA ->: ALL THE WAY TO / ANGA
  s10 he steps off the boat onto Anga's cracked earth; a ripple of light where his foot lands: THE MOMENT HE STEPPED
      / ON ANGA'S SOIL...; dark clouds roll in, rain pours, the earth turns dark and wet with puddles, the crops turn
      green, the farmer and the woman dance: THE MOMENT HE STEPPED IN, / THE RAIN CAME!
  s11 the wedding mandap: the boy and Princess Shanta (tag), King Lomapada blessing, a small fire; garlands drop on
      both, petals: THE KING'S OWN DAUGHTER, / PRINCESS SHANTA, then THEY GOT / MARRIED
  s12 YEARS LATER...: the same sage (tag THE SAME SAGE) and King Dasharatha (tag) kneel at the sacred fire, it flares:
      IN THE RAMAYANA, HE LED / DASHARATHA'S YAJNA; a soft light opens on the right and baby Rama sleeps in a cradle
      in it (tag BABY RAMA): AND THEN / RAMA WAS BORN
  s13 the yajna freezes in sepia; then a chain of medallions FOREST BOY -> RAIN -> WEDDING -> YAJNA -> RAMA ->
      RAMAYANA: WHAT IF HE / NEVER LEFT THE FOREST?; a red X on the boy and every link after it goes dark, a big "?"
      over the Ramayana: NO FOREST BOY... / NO RAMAYANA?

Every frame is a pure function of t. English on-screen text, shared by Hindi and Kannada. Cues are words of the line
in the timeline's language ({"hi": ..., "kn": ...}, tl.lang) with a fraction fallback, kept in one table (CUES) that
the scenes and sfx() both read, with minimum gaps so a fast voice can't bunch the beats together. The cue and shot
caches live on the timeline under their own names (_s6c_*), apart from the sibling modules' caches.
"""
import math

import cairo

import puppet_core as pc
import six_cast_c as C
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, text_size
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_arjuna import card2, cloud_text
from scenes_jarasandha import (INK, RED, bob_rot, fit, glow, man_angles, motes, red_ring, sound_rings,
                               walk_legs, woman_angles)
from scenes_jarasandha import head2 as _head2
from scenes_jayadratha import flash_at, silhouette, tag, tint, to_user
from scenes_kaikeyi import ANJALI, card, fig
from scenes_lakshman_rekha import big_q, big_x, sparkle
from scenes_mandhata import aura, burst, held, indra, lights, local, mix, reach_arm, warm
from scenes_ruru import fire, petals, sepia
from shots import T

MISSES = set()                       # cue words not found in a line (falls back to fractions)
FL = 892                             # the floor line (feet) of the standard stage (as scenes_six_b)
S = 0.56                             # a standing figure's scale
HY = 46                              # the headline's top (as scenes_six_b)
CARD_HOLD = 2.7                      # seconds a chapter card holds before the first scene (as scenes_six_b)
LIGHT = (1.0, 0.95, 0.82)
NIGHT = 0.42
TEACH = (-2.25, -0.55)               # a hand raised (teaching, blessing)
POINT = (-1.5, -0.12)                # an arm held straight out in front
OFFER = (-0.5, -1.05)                # a forearm held out in front at the waist (a plate on the palm)
PRAY_UP = (-2.75, -0.35)             # joined hands raised high


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) in the timeline's language, with a fraction fallback."""
    word = words[getattr(tl, "lang", "hi")] if isinstance(words, dict) else words
    try:
        return T(tl, bid, word)
    except (KeyError, ValueError):
        MISSES.add((bid, word))
        return T(tl, bid, frac)


# Every cue of every line: (name, {"hi": word, "kn": word}, fraction fallback, ((after, min gap), ...)); "t0" = the
# line's start. Words are exact substrings of the script lines in both languages, each the word that carries the same
# meaning (checked: MISSES stays empty for hi and kn).
CUES = {
    "g1": (("C", {"hi": "कहानी", "kn": "ಕಥೆ"}, 0.1, (("t0", 0.3),)),
           ("K", {"hi": "कालकेय", "kn": "ಕಾಲಕೇಯ"}, 0.22, (("C", 0.4),)),
           ("D", {"hi": "दिन", "kn": "ಹಗಲಲ್ಲಿ"}, 0.5, (("K", 0.8),)),
           ("S", {"hi": "समुद्र", "kn": "ಸಮುದ್ರದ"}, 0.62, (("D", 0.3),)),
           ("H", {"hi": "छिप", "kn": "ಅಡಗಿ"}, 0.85, (("S", 0.5),))),
    "g2": (("R", {"hi": "रात", "kn": "ರಾತ್ರಿ"}, 0.08, (("t0", 0.1),)),
           ("N", {"hi": "निकलकर", "kn": "ಹೊರಗೆ"}, 0.3, (("R", 0.5),)),
           ("J", {"hi": "जंगलों", "kn": "ಕಾಡಲ್ಲಿ"}, 0.5, (("N", 0.6),)),
           ("K", {"hi": "मार", "kn": "ಕೊಲ್ತಿದ್ರು"}, 0.8, (("J", 0.7),))),
    "g3": (("F", {"hi": "ढूँढ", "kn": "ಹುಡುಕೋ"}, 0.15, (("t0", 0.4),)),
           ("X", {"hi": "समुद्र", "kn": "ಸಮುದ್ರ"}, 0.5, (("F", 1.0),)),
           ("B", {"hi": "बड़ा", "kn": "ದೊಡ್ಡದು"}, 0.66, (("X", 0.4),)),
           ("G", {"hi": "गहरा", "kn": "ಆಳ"}, 0.92, (("B", 0.6),))),
    "g4": (("A", {"hi": "अगस्त्य", "kn": "ಅಗಸ್ತ್ಯ"}, 0.18, (("t0", 0.4),)),
           ("B", {"hi": "बोले", "kn": "ಹೇಳಿದ್ರು"}, 0.4, (("A", 0.8),)),
           ("Y", {"hi": "आप", "kn": "ನೀವೇ"}, 0.47, (("B", 0.3),)),
           ("P", {"hi": "पी", "kn": "ಕುಡಿದು"}, 0.9, (("Y", 1.0),))),
    "g5": (("K", {"hi": "किनारे", "kn": "ದಡಕ್ಕೆ"}, 0.3, (("t0", 0.5),)),
           ("P", {"hi": "पूरा", "kn": "ಇಡೀ"}, 0.5, (("K", 0.7),)),
           ("D", {"hi": "पी", "kn": "ಕುಡಿದು"}, 0.65, (("P", 0.3),)),
           ("B", {"hi": "बूँद", "kn": "ಹನಿ"}, 0.85, (("D", 0.9),))),
    "g6": (("S", {"hi": "सूखा", "kn": "ಒಣಗಿದ"}, 0.1, (("t0", 0.2),)),
           ("A", {"hi": "दिख", "kn": "ಕಾಣಿಸಿ"}, 0.3, (("S", 0.4),)),
           ("D", {"hi": "देवताओं", "kn": "ದೇವತೆಗಳು"}, 0.4, (("A", 0.5),)),
           ("H", {"hi": "हरा", "kn": "ಸೋಲಿಸಿ"}, 0.55, (("D", 0.7),)),
           ("B", {"hi": "बचे", "kn": "ಉಳಿದವರು"}, 0.68, (("H", 0.6),)),
           ("P", {"hi": "पाताल", "kn": "ಪಾತಾಳ"}, 0.86, (("B", 0.6),))),
    "g7": (("B", {"hi": "बोले", "kn": "ಹೇಳಿದ್ರು"}, 0.25, (("t0", 0.4),)),
           ("R", {"hi": "ऋषिवर", "kn": "ಋಷಿಗಳೇ"}, 0.38, (("B", 0.3),)),
           ("V", {"hi": "वापस", "kn": "ಮತ್ತೆ"}, 0.72, (("R", 0.6),))),
    "g8": (("M", {"hi": "मुस्कुराए", "kn": "ನಕ್ಕರು"}, 0.18, (("t0", 0.3),)),
           ("W", {"hi": "पानी", "kn": "ನೀರನ್ನ"}, 0.48, (("M", 0.5),)),
           ("P", {"hi": "पचा", "kn": "ಜೀರ್ಣ"}, 0.75, (("W", 0.4),))),
    "g9": (("K", {"hi": "रह", "kn": "ಖಾಲಿ"}, 0.32, (("t0", 0.5),)),
           ("D", {"hi": "देवता", "kn": "ದೇವತೆಗಳು"}, 0.5, (("K", 0.5),)),
           ("B", {"hi": "ब्रह्मा", "kn": "ಬ್ರಹ್ಮನ"}, 0.68, (("D", 0.5),))),
    "g10": (("S", {"hi": "समय", "kn": "ಕಾಲದ"}, 0.3, (("t0", 0.6),)),
            ("B", {"hi": "भगीरथ", "kn": "ಭಗೀರಥ"}, 0.55, (("S", 0.8),)),
            ("F", {"hi": "भरेंगे", "kn": "ತುಂಬಿಸ್ತಾನೆ"}, 0.9, (("B", 0.8),))),
    "g11": (("T", {"hi": "तपस्या", "kn": "ತಪಸ್ಸಿನಿಂದ"}, 0.2, (("t0", 0.5),)),
            ("G", {"hi": "गंगा", "kn": "ಗಂಗೆ"}, 0.3, (("T", 0.5),)),
            ("A", {"hi": "धरती", "kn": "ಭೂಮಿಗೆ"}, 0.38, (("G", 0.4),)),
            ("P", {"hi": "पानी", "kn": "ನೀರಿಂದ"}, 0.6, (("A", 0.9),)),
            ("B", {"hi": "भरा", "kn": "ತುಂಬಿತು"}, 0.94, (("P", 1.2),))),
    "s1": (("C", {"hi": "कहानी", "kn": "ಕಥೆ"}, 0.1, (("t0", 0.3),)),
           ("J", {"hi": "जंगल", "kn": "ಕಾಡಲ್ಲಿ"}, 0.25, (("C", 0.4),)),
           ("R", {"hi": "ऋषि", "kn": "ಋಷಿ"}, 0.38, (("J", 0.4),)),
           ("B", {"hi": "बेटे", "kn": "ಮಗ"}, 0.55, (("R", 0.5),)),
           ("N", {"hi": "ऋष्यशृंग", "kn": "ಋಷ್ಯಶೃಂಗ"}, 0.7, (("B", 0.3),))),
    "s2": (("S", {"hi": "सिर", "kn": "ತಲೆ"}, 0.08, (("t0", 0.2),)),
           ("H", {"hi": "सींग", "kn": "ಕೊಂಬು"}, 0.3, (("S", 0.6),)),
           ("M", {"hi": "महाभारत", "kn": "ಮಹಾಭಾರತ"}, 0.5, (("H", 0.9),)),
           ("D", {"hi": "हिरनी", "kn": "ಜಿಂಕೆ"}, 0.9, (("M", 1.0),))),
    "s3": (("P", {"hi": "पिता", "kn": "ಅಪ್ಪನ"}, 0.12, (("t0", 0.3),)),
           ("I", {"hi": "इंसान", "kn": "ಮನುಷ್ಯ"}, 0.45, (("P", 0.8),)),
           ("N", {"hi": "देखा", "kn": "ನೋಡಿರಲಿಲ್ಲ"}, 0.6, (("I", 0.4),)),
           ("A", {"hi": "औरत", "kn": "ಹೆಣ್ಣ"}, 0.78, (("N", 0.7),))),
    "s4": (("A", {"hi": "अंग", "kn": "ಅಂಗ"}, 0.08, (("t0", 0.3),)),
           ("S", {"hi": "सालों", "kn": "ವರ್ಷ"}, 0.3, (("A", 0.5),)),
           ("R", {"hi": "बारिश", "kn": "ಮಳೆ"}, 0.42, (("S", 0.4),)),
           ("K", {"hi": "खेत", "kn": "ಹೊಲ"}, 0.65, (("R", 0.9),)),
           ("L", {"hi": "लोग", "kn": "ಜನ"}, 0.85, (("K", 0.6),))),
    "s5": (("K", {"hi": "राजा", "kn": "ರಾಜನಿಗೆ"}, 0.2, (("t0", 0.4),)),
           ("J", {"hi": "जंगल", "kn": "ಕಾಡಿನ"}, 0.45, (("K", 0.7),)),
           ("R", {"hi": "बारिश", "kn": "ಮಳೆ"}, 0.85, (("J", 1.0),))),
    "s6": (("Q", {"hi": "कैसे", "kn": "ಹೇಗೆ"}, 0.3, (("t0", 0.4),)),
           ("R", {"hi": "राजा", "kn": "ರಾಜ"}, 0.55, (("Q", 0.8),)),
           ("A", {"hi": "औरतों", "kn": "ಹೆಣ್ಣುಮಕ್ಕಳ"}, 0.72, (("R", 0.4),)),
           ("J", {"hi": "भेजा", "kn": "ಕಳಿಸಿದ"}, 0.92, (("A", 0.5),))),
    "s7": (("D", {"hi": "देखा", "kn": "ನೋಡಿ"}, 0.1, (("t0", 0.3),)),
           ("A", {"hi": "अजीब", "kn": "ವಿಚಿತ್ರ"}, 0.28, (("D", 0.6),)),
           ("K", {"hi": "कपड़े", "kn": "ಬಟ್ಟೆ"}, 0.45, (("A", 0.9),)),
           ("B", {"hi": "बातें", "kn": "ಮಾತು"}, 0.56, (("K", 0.6),)),
           ("F", {"hi": "फल", "kn": "ಹಣ್ಣು"}, 0.74, (("B", 0.7),)),
           ("M", {"hi": "मीठे", "kn": "ಸಿಹಿ"}, 0.9, (("F", 0.8),))),
    "s8": (("S", {"hi": "मिठाइयाँ", "kn": "ಸಿಹಿತಿಂಡಿ"}, 0.3, (("t0", 0.6),)),
           ("P", {"hi": "पहली", "kn": "ಮೊದಲ"}, 0.68, (("S", 1.2),)),
           ("K", {"hi": "खाई", "kn": "ತಿಂದಿದ್ದ"}, 0.9, (("P", 0.5),))),
    "s9": (("N", {"hi": "नाव", "kn": "ದೋಣಿ"}, 0.42, (("t0", 0.6),)),
           ("A", {"hi": "अंग", "kn": "ಅಂಗ"}, 0.75, (("N", 0.8),))),
    "s10": (("P", {"hi": "पैर", "kn": "ಕಾಲಿಟ್ಟ"}, 0.5, (("t0", 1.0),)),
            ("B", {"hi": "बारिश", "kn": "ಮಳೆ"}, 0.78, (("P", 0.6),))),
    "s11": (("B", {"hi": "बेटी", "kn": "ಮಗಳು"}, 0.22, (("t0", 0.3),)),
            ("S", {"hi": "शांता", "kn": "ಶಾಂತ"}, 0.38, (("B", 0.3),)),
            ("V", {"hi": "शादी", "kn": "ಮದುವೆ"}, 0.55, (("S", 0.5),))),
    "s12": (("R", {"hi": "रामायण", "kn": "ರಾಮಾಯಣ"}, 0.05, ()),
            ("Y", {"hi": "यही", "kn": "ಇದೇ"}, 0.15, (("t0", 0.4),)),
            ("D", {"hi": "दशरथ", "kn": "ದಶರಥ"}, 0.3, (("Y", 0.5),)),
            ("G", {"hi": "यज्ञ", "kn": "ಯಜ್ಞ"}, 0.5, (("D", 0.6),)),
            ("M", {"hi": "बाद", "kn": "ಮೇಲೆ"}, 0.72, (("G", 0.9),)),
            ("B", {"hi": "जन्म", "kn": "ಹುಟ್ಟಿದ"}, 0.9, (("M", 0.4),))),
    "s13": (("J", {"hi": "जंगल", "kn": "ಕಾಡಿಂದ"}, 0.3, (("t0", 1.2),)),
            ("N", {"hi": "आता", "kn": "ಬರದೇ"}, 0.55, (("J", 0.6),)),
            ("R", {"hi": "रामायण", "kn": "ರಾಮಾಯಣ"}, 0.8, (("N", 0.8),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline, under this module's own name)."""
    cache = getattr(tl, "_s6c_cues", None)
    if cache is None:
        cache = {}
        tl._s6c_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, word, frac, cons in CUES[bid]:
            v = cue(tl, bid, word, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


def line_end(tl, bid):
    """When the next line starts (the end of this line's pause)."""
    i = [b.id for b in tl.beats].index(bid)
    return tl.beats[i + 1].start if i + 1 < len(tl.beats) else tl.total


# ------------------------------------------------------------------ text


def head(cr, t, small, t_small, big=None, t_big=0.0, big_size=118, small_size=56, **kw):
    """The two-tier headline at the top centre (as scenes_six_b.head2): the big line fits 1460 px (inside the 90 px
    margins even at its pop-in overshoot), the small line 1600 px."""
    if big:
        big_size = min(big_size, fit(big, big_size, 1460))
    if small:
        words = small.split()
        sw = sum(text_size(w_, small_size)[0] for w_ in words) + small_size * 0.34 * (len(words) - 1)
        if sw > 1600:
            small_size = int(small_size * 1600 / sw)
    return _head2(cr, t, small, t_small, big, t_big, y=HY, small_size=small_size, big_size=big_size, **kw)


def seg_line(cr, parts, x, y, size, font=HEAD_FONT, alpha=1.0, tracking=0, gap=None):
    """A centred line of coloured pieces [(text, colour)]."""
    ws = [text_size(p, size, font, tracking)[0] for p, _ in parts]
    gap = size * 0.3 if gap is None else gap
    xx = x - (sum(ws) + gap * (len(parts) - 1)) / 2
    for (p, col), w in zip(parts, ws):
        draw_text(cr, p, xx, y, size, col, alpha, font, "lm", tracking)
        xx += w + gap


def chapter(cr, t, t_in, t_out, story, lines, source):
    """The palm-leaf chapter card, the same as scenes_six_b.chapter: STORY n OF 6, the English title (lines of
    [(text, colour)]), the source tag. It rises in at t_in and flies up and away at t_out."""
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
    ssz = min(30, int(30 * 760 / max(1, text_size(source, 30, MONO_FONT, 4)[0])))
    w_, h_ = text_size(source, ssz, MONO_FONT, 4)
    cr.set_source_rgba(0.62, 0.12, 0.08, 0.92 * a * p3)
    cr.rectangle(-w_ / 2 - 26, 158 - h_ / 2 - 14, w_ + 52, h_ + 28)
    cr.set_line_width(3)
    cr.stroke()
    draw_text(cr, source, 0, 158, ssz, (0.62, 0.12, 0.08), a * p3, MONO_FONT, "cm", tracking=4)
    cr.restore()


def fade_in(cr, a, fn):
    """Draw a scene (fn(cr)) fading up from the bare cloth: the cloth and the scene go into a group painted at alpha a
    (the leather keeps its multiply-on-light look throughout). Returns fn's result."""
    if a >= 0.999:
        return fn(cr)
    if a <= 0.001:
        return None
    cr.push_group()
    C.screen(cr)
    res = fn(cr)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    return res


def mark(cr, t, t_in, ch, x, y, size=90, color=RED, alpha=1.0, t_out=None):
    """A "?" or "!" popping up over a head and bobbing."""
    q = back(clamp((t - t_in) / 0.3), 1.8)
    a = clamp(q) * alpha
    if t_out is not None:
        a *= 1 - prog(t, t_out, 0.3)
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y - 8 * math.sin(t * 4 + x))
    cr.rotate(0.12 * math.sin(t * 3 + x * 0.1))
    cr.scale(q, q)
    for ox, oy in ((-4, 0), (4, 0), (0, -4), (0, 4)):
        draw_text(cr, ch, ox, oy, size, LIGHT, 0.9 * a, anchor="cm")
    draw_text(cr, ch, 0, 0, size, color, a, anchor="cm")
    cr.restore()


def stamp(cr, t, t_in, text, x, y, size=64, rot=-0.06, color=RED, alpha=1.0):
    """A red rubber stamp that thumps on, with a pale edge so it reads on any ground."""
    p = clamp((t - t_in) / 0.2)
    if p <= 0:
        return
    s = 1.7 - 0.7 * back(p, 2.0)
    w, h = text_size(text, size, tracking=4)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.set_source_rgba(*LIGHT, 0.75 * p * alpha)
    cr.rectangle(-w / 2 - 30, -h / 2 - 22, w + 60, h + 44)
    cr.fill()
    cr.set_source_rgba(*color, 0.9 * p * alpha)
    cr.set_line_width(7)
    cr.rectangle(-w / 2 - 24, -h / 2 - 16, w + 48, h + 32)
    cr.stroke()
    draw_text(cr, text, 0, 0, size, color, 0.95 * p * alpha, anchor="cm", tracking=4)
    cr.restore()


def arrow2(cr, p0, p1, p, both=True, width=12, alpha=1.0, col=RED):
    """A red arrow drawn out from the middle (both = heads at both ends), with a pale edge."""
    if p <= 0:
        return
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    a0 = (mx + (p0[0] - mx) * p, my + (p0[1] - my) * p) if both else p0
    a1 = (mx + (p1[0] - mx) * p, my + (p1[1] - my) * p) if both else (p0[0] + (p1[0] - p0[0]) * p,
                                                                        p0[1] + (p1[1] - p0[1]) * p)
    ends = [(a1, a0)] + ([(a0, a1)] if both else [])
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, c, al in ((width + 8, LIGHT, 0.8), (width, col, 0.95)):
        cr.set_source_rgba(*c, al * alpha)
        cr.set_line_width(lw)
        cr.move_to(*a0)
        cr.line_to(*a1)
        cr.stroke()
        for tip, frm in ends:
            ang = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
            L_ = width * 3.4 + (lw - width)
            pc.poly(cr, [(tip[0] + 0.4 * L_ * math.cos(ang), tip[1] + 0.4 * L_ * math.sin(ang)),
                         (tip[0] - L_ * math.cos(ang - 0.5), tip[1] - L_ * math.sin(ang - 0.5)),
                         (tip[0] - L_ * math.cos(ang + 0.5), tip[1] - L_ * math.sin(ang + 0.5))])
            cr.fill()
    cr.restore()


def curve_arrow(cr, p0, c_, p1, p, width=12, alpha=1.0, dash=True):
    """A red dotted arrow along a quadratic curve, revealed to fraction p, its head at the moving tip."""
    if p <= 0:
        return
    pts = [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c_[0] + u * u * p1[0],
            (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c_[1] + u * u * p1[1]) for u in (k / 60 * p for k in range(61))]
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, c, al in ((width + 8, LIGHT, 0.75), (width, RED, 0.95)):
        if dash:
            cr.set_dash([lw * 0.2 + 18, 22])
        cr.set_source_rgba(*c, al * alpha)
        cr.set_line_width(lw)
        cr.move_to(*pts[0])
        for q in pts[1:]:
            cr.line_to(*q)
        cr.stroke()
        cr.set_dash([])
        tip, frm = pts[-1], pts[-4]
        ang = math.atan2(tip[1] - frm[1], tip[0] - frm[0])
        L_ = width * 3.4 + (lw - width)
        pc.poly(cr, [(tip[0] + 0.4 * L_ * math.cos(ang), tip[1] + 0.4 * L_ * math.sin(ang)),
                     (tip[0] - L_ * math.cos(ang - 0.5), tip[1] - L_ * math.sin(ang - 0.5)),
                     (tip[0] - L_ * math.cos(ang + 0.5), tip[1] - L_ * math.sin(ang + 0.5))])
        cr.fill()
    cr.restore()


def talk_marks(cr, t, t0, x, y, alpha=1.0, dirn=-1):
    """Three short curved strokes in front of a mouth (someone talking), pulsing outward, facing dirn."""
    if t < t0 or alpha <= 0.01:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    a0 = math.pi if dirn < 0 else 0.0
    for k in range(3):
        u = ((t - t0) * 1.6 - k * 0.25) % 1.0
        r = 16 + 18 * k + 8 * u
        cr.new_path()
        cr.arc(x, y, r, a0 - 0.55, a0 + 0.55)
        cr.set_source_rgba(*INK, 0.8 * alpha * (0.4 + 0.6 * math.sin(math.pi * u)))
        cr.set_line_width(5)
        cr.stroke()
    cr.restore()


def dotted_line(cr, x0, x1, y, t, alpha=1.0, gap=30.0, r=6.0):
    cr.save()
    cr.set_source_rgba(*RED, 0.85 * alpha)
    x = x0
    while x <= x1:
        cr.new_sub_path()
        cr.arc(x, y + 3 * math.sin(x * 0.02 + t * 2), r, 0, 2 * math.pi)
        x += gap
    cr.fill()
    cr.restore()


def blob_cloud(cr, cx, cy, w, h, alpha=1.0, tail=None, fill=(0.98, 0.92, 0.76)):
    """A thought cloud (parchment, inked outline) of bumps round an ellipse w x h; tail = (x, y) it trails toward
    with three shrinking bubbles. Returns a function that clips to its inside."""
    bumps = []
    n = 14
    for i in range(n):
        a = 2 * math.pi * i / n
        bumps.append((cx + 0.5 * w * math.cos(a) * 0.86, cy + 0.5 * h * math.sin(a) * 0.80,
                      0.16 * (w + h) * 0.5 * (1.0 + 0.12 * math.sin(i * 2.3))))
    core = (cx, cy, 0.46 * w, 0.42 * h)

    def path(grow=0.0):
        cr.new_path()
        pc.ell(cr, core[0], core[1], core[2] + grow, core[3] + grow)
        for x, y, r in bumps:
            cr.new_sub_path()
            cr.arc(x, y, r + grow, 0, 2 * math.pi)
    cr.save()
    if tail is not None:
        for k, f in enumerate((0.62, 0.78, 0.9)):
            bx = cx + (tail[0] - cx) * f
            by = cy + (tail[1] - cy) * f
            r = 26 - 7 * k
            cr.new_path()
            cr.arc(bx, by, r + 4, 0, 2 * math.pi)
            cr.set_source_rgba(*pc.INK, alpha)
            cr.fill()
            cr.arc(bx, by, r, 0, 2 * math.pi)
            cr.set_source_rgba(*fill, alpha)
            cr.fill()
    path(5.0)
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    cr.set_source_rgba(*pc.INK, alpha)
    cr.fill()
    path(0.0)
    cr.set_source_rgba(*fill, alpha)
    cr.fill()
    cr.restore()

    def clip():
        path(-2.0)
        cr.clip()
    return clip


def plaque_text(cr, t, t_in, text, x, y, size=40, alpha=1.0, t_out=None, color=INK):
    """A leather plaque (no rod) with one line of text, centred on (x, y), dropping in."""
    p = prog(t, t_in, 0.25)
    if t_out is not None:
        p = min(p, 1 - prog(t, t_out, 0.25))
    a = p * alpha
    if a <= 0.01:
        return
    w, h = text_size(text, size, MONO_FONT, 2)
    bw, bh = w + 46, h + 26
    yy = y - 18 * (1 - back(clamp(p)))
    cr.save()
    cr.translate(x, yy)
    pc.poly(cr, [(-bw / 2, -bh / 2 + 8), (-bw / 2 + 8, -bh / 2), (bw / 2 - 8, -bh / 2), (bw / 2, -bh / 2 + 8),
                 (bw / 2, bh / 2 - 8), (bw / 2 - 8, bh / 2), (-bw / 2 + 8, bh / 2), (-bw / 2, bh / 2 - 8)])
    cr.set_source_rgba(0.97, 0.87, 0.62, 0.96 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(3.5)
    cr.stroke()
    draw_text(cr, text, 0, 1, size, color, a, MONO_FONT, "cm", tracking=2)
    cr.restore()


# ------------------------------------------------------------------ the sea


def edge_x(edge, y):
    """x of a shore line edge = (x_top, y_top, x_bottom, y_bottom) at height y (extended straight beyond its ends)."""
    xa, ya, xb, yb = edge
    return xa + (xb - xa) * (y - ya) / ((yb - ya) or 1.0)


def bank(cr, edge, side=-1, col=C.SAND, rock=False, top_extra=40):
    """The land beside the sea: everything on `side` (-1 left, 1 right) of the shore line `edge`, from a little above
    its top down off the frame, sandy (or rocky), inked along the shore, with pebbles punched along it."""
    xa, ya, xb, yb = edge
    y0, y1 = ya - top_extra, H + 80
    far = -200 if side < 0 else W + 200
    pts = [(far, y0), (edge_x(edge, y0), y0), (edge_x(edge, y1), y1), (far, y1)]
    cr.save()
    pc.poly(cr, pts)
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgb(*((0.66, 0.62, 0.62) if rock else col))
    cr.fill()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.set_source_rgb(*pc.INK)
    cr.set_line_width(5)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.move_to(far, y0)
    cr.line_to(edge_x(edge, y0), y0)
    cr.line_to(edge_x(edge, y1), y1)
    cr.stroke()
    for k in range(9):                                    # strata / ripples along the bank
        y = y0 + 40 + k * 70
        if y > y1:
            break
        xe = edge_x(edge, y) - side * 18
        cr.move_to(xe, y)
        cr.line_to(xe - side * (160 + 40 * (k % 3)), y + 8 * (1 if k % 2 else -1))
        cr.set_source_rgba(*((0.40, 0.38, 0.42) if rock else C.SAND2), 0.9)
        cr.set_line_width(3)
        cr.stroke()
    cr.restore()


def sea(cr, t, level, floor=1130, x0=-120, x1=W + 120, speed=1.0, rows=4, dark=0.0, sc=0.82, alpha=1.0, edge=None,
        side=1):
    """The ocean between x0 and x1: its water body (a blue light filter, darker with depth) from the surface `level`
    down to `floor`, and the wave strips scrolling on the surface (they thin out as the water gets shallow).
    edge = a shore line (x_top, y_top, x_bottom, y_bottom): the water only on `side` of it (1 = right of it)."""
    depth_ = floor - level
    if depth_ <= 4 or alpha <= 0.01:
        return
    thin = clamp(depth_ / 260.0)
    cr.save()
    cr.rectangle(x0, -200, x1 - x0, floor + 200 + 6)
    cr.clip()
    if edge is not None:
        far = W + 300 if side > 0 else -300
        pc.poly(cr, [(edge_x(edge, -200), -200), (far, -200), (far, H + 300), (edge_x(edge, H + 300), H + 300)])
        cr.clip()
    g = cairo.LinearGradient(0, level, 0, max(level + 1, floor))
    g.add_color_stop_rgba(0, 0.62, 0.80, 1.0, alpha)
    g.add_color_stop_rgba(1, 0.30 - 0.15 * dark, 0.48 - 0.25 * dark, 0.86 - 0.3 * dark, alpha)
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.rectangle(x0, level + 20 * thin, x1 - x0, floor - level)
    cr.set_source(g)
    cr.fill()
    cr.restore()
    gap = 36 * thin
    for k in range(rows):
        off = (t * speed * (36 + 14 * k) * (1 if k % 2 == 0 else -1) + 61 * k) % C.WAVE_P
        x = W / 2 + (off - C.WAVE_P / 2) * sc
        prop(cr, f"c6_wave{min(k, 3)}", x, level + gap * k + 4 * math.sin(t * 1.3 + k), sc * (0.6 + 0.4 * thin),
             alpha=alpha * (0.5 + 0.5 * thin))
    cr.restore()


def ribbon(cr, t, pts, w0, w1, alpha=1.0, flow=1.0, col=C.WATER, twist=True):
    """A ribbon of water along a spine (a list of points, from its source to its end), w0 -> w1 wide: a blue leather
    strip with an inked edge, a twisting white line spiralling along it and flecks of foam running down it."""
    n = len(pts)
    if n < 2 or alpha <= 0.01:
        return
    nrm, wid = [], []
    for i in range(n):
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1.0
        nrm.append((-ty / ln, tx / ln))
        u = i / (n - 1)
        wid.append(w0 + (w1 - w0) * u)
    left = [(p[0] + nn[0] * w / 2, p[1] + nn[1] * w / 2) for p, nn, w in zip(pts, nrm, wid)]
    right = [(p[0] - nn[0] * w / 2, p[1] - nn[1] * w / 2) for p, nn, w in zip(pts, nrm, wid)]
    cr.save()
    pc.poly(cr, left + right[::-1])
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(*col, alpha)
    cr.fill_preserve()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.set_source_rgba(*pc.INK, 0.85 * alpha)
    cr.set_line_width(4)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()
    if twist:
        tw = []
        for i, (p, nn, w) in enumerate(zip(pts, nrm, wid)):
            s_ = 0.36 * w * math.sin(i * 0.55 - t * 7.0 * flow)
            tw.append((p[0] + nn[0] * s_, p[1] + nn[1] * s_))
        cr.set_source_rgba(*C.FOAM, 0.8 * alpha)
        cr.set_line_width(5)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(*tw[0])
        for q in tw[1:]:
            cr.line_to(*q)
        cr.stroke()
    for k in range(int(n / 3)):                           # foam flecks running along it
        u = ((k * 0.37 + t * 0.9 * flow) % 1.0)
        i = min(n - 1, int(u * (n - 1)))
        side = 0.3 * math.sin(k * 2.1)
        p, nn, w = pts[i], nrm[i], wid[i]
        cr.new_path()
        cr.arc(p[0] + nn[0] * side * w, p[1] + nn[1] * side * w, 3 + 0.05 * w, 0, 2 * math.pi)
        cr.set_source_rgba(*C.FOAM, 0.85 * alpha * math.sin(math.pi * u))
        cr.fill()
    cr.restore()


def quad(p0, c_, p1, n=40, wave=0.0, t=0.0, amp=0.0):
    """Points along a quadratic curve, optionally waving sideways (amp px) as it flows."""
    out = []
    for k in range(n + 1):
        u = k / n
        x = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * c_[0] + u * u * p1[0]
        y = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * c_[1] + u * u * p1[1]
        if amp:
            x += amp * math.sin(u * 7 - t * 3 + wave) * math.sin(math.pi * u)
        out.append((x, y))
    return out


def vortex(cr, t, x, y, r, a):
    """A whirlpool: foam rings turning round (x, y), flattened (seen from the side)."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(4):
        rr = r * (0.3 + 0.24 * k)
        cr.save()
        cr.translate(x, y)
        cr.scale(1, 0.28)
        a0 = t * (5 - k) + k
        cr.set_source_rgba(*C.FOAM, 0.85 * a)
        cr.set_line_width(6 / 0.28 * 0.3)
        cr.arc(0, 0, rr, a0, a0 + 4.2)
        cr.stroke()
        cr.restore()
    cr.restore()


def bubbles(cr, t, t0, x, y, n=6, rise=260.0, alpha=1.0):
    for i in range(n):
        u = (t - t0 - 0.18 * i) / 1.4
        if 0 < u < 1:
            cr.new_path()
            cr.arc(x + 30 * math.sin(i * 2.2 + t * 3), y - rise * u, 6 + 3 * (i % 3), 0, 2 * math.pi)
            cr.set_source_rgba(*C.FOAM, 0.85 * alpha * (1 - u))
            cr.set_line_width(3)
            cr.stroke()


def seabed(cr, y, x=W / 2, s=0.85, wet=False):
    prop(cr, "c6_seabed", x, y, s)


FISH_REST = ((520, 0, 0.55, 0.3), (760, 1, 0.5, -0.2), (1010, 2, 0.6, 0.15), (1260, 0, 0.5, -0.1),
             (1500, 1, 0.55, 0.25), (1740, 2, 0.5, 0.0))


def stranded(cr, t, floor, items=FISH_REST, flap=1.0, alpha=1.0, dx=0.0):
    """Fish lying on the dry sea floor, flapping now and then; shells and a starfish."""
    for i, (x, k, s, r) in enumerate(items):
        f = flap * max(0.0, math.sin(t * 5 + i * 1.7)) ** 6
        prop(cr, f"c6_fish{k}", x + dx, floor - 16 - 14 * f, s, rot=r * 0.3 + 0.25 * f * (1 if i % 2 else -1),
             alpha=alpha, flip=i % 2 == 1)
    for x, nm, s in ((640, "c6_shell", 0.6), (1130, "c6_star", 0.5), (1600, "c6_shell", 0.5), (380, "c6_star", 0.45)):
        prop(cr, nm, x + dx, floor + 6, s, alpha=alpha)


def ground(cr, y=FL, alpha=1.0):
    prop(cr, "c6_ground", W / 2, y + 6, 1.42, alpha=alpha)


def trees(cr, t, xs=((120, 0.62, 8, 0.6, True), (1800, 0.6, 10, 0.55, False)), feet=FL):
    for i, (x, s, b, a, fl) in enumerate(xs):
        prop(cr, "tree", x, feet + 10, s, rot=sway(t, 0.006, 0.3, i), alpha=a, blur=b, flip=fl)


def sun(cr, t, x, y, s, a=1.0, hard=0.0):
    glow(cr, x, y, 420 * s + 120, (0.55 + 0.25 * hard) * a)
    warm(cr, x, y, 300 * s + 60 * hard, (0.5 + 0.4 * hard) * a)
    if hard > 0:
        aura(cr, t, x, y, 200 * s, (470 + 60 * math.sin(t * 3)) * s, 0.8 * hard * a, n=22, spin=0.1)
    prop(cr, "sun", x, y, s, rot=t * 0.15, alpha=a)


def heat(cr, t, y, x0=100, x1=W - 100, a=1.0):
    """Heat haze: faint wavy lines rising off the hot ground."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(9):
        x = x0 + (x1 - x0) * (i + 0.5) / 9
        u = (t * 0.5 + i * 0.37) % 1.0
        yy = y - 40 - 220 * u
        cr.set_source_rgba(1.0, 0.85, 0.6, 0.35 * a * math.sin(math.pi * u))
        cr.set_line_width(4)
        cr.move_to(x, yy)
        for k in range(1, 9):
            cr.line_to(x + 10 * math.sin(k * 1.2 + t * 4), yy - 12 * k)
        cr.stroke()
    cr.restore()


def rain(cr, t, a, x0=-50, x1=W + 50, y0=-40, y1=FL + 40, n=160):
    """Rain streaks falling (pale blue lines), splashes where they land."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_source_rgba(0.80, 0.90, 1.0, 0.7 * a)
    cr.set_line_width(3)
    span = y1 - y0
    for i in range(n):
        x = x0 + (x1 - x0) * ((i * 0.6180339) % 1.0)
        u = (t * 1.6 + i * 0.137) % 1.0
        y = y0 + span * u
        cr.move_to(x - 10, y)
        cr.line_to(x - 22, y + 46)
    cr.stroke()
    for i in range(40):
        x = x0 + (x1 - x0) * ((i * 0.381) % 1.0)
        u = (t * 2.2 + i * 0.29) % 1.0
        cr.set_source_rgba(0.85, 0.93, 1.0, 0.6 * a * (1 - u))
        cr.set_line_width(2.5)
        cr.save()
        cr.translate(x, y1 - 40)
        cr.scale(1, 0.3)
        cr.arc(0, 0, 8 + 22 * u, math.pi, 2 * math.pi)
        cr.restore()
        cr.stroke()
    cr.restore()


def dust(cr, t, t0, x, y, r=120.0, alpha=1.0):
    """A puff of dust (a defeated shadow dissolving): grey rings and flecks spreading and fading."""
    u = (t - t0) / 1.1
    if not 0 < u < 1:
        return
    for i in range(9):
        a = 2 * math.pi * i / 9 + 0.4
        d = r * ease(u) * (0.6 + 0.4 * (i % 3) / 2)
        cr.new_path()
        cr.arc(x + d * math.cos(a), y + 0.6 * d * math.sin(a) - 60 * u, 18 + 26 * u, 0, 2 * math.pi)
        cr.set_source_rgba(0.62, 0.56, 0.52, 0.55 * alpha * (1 - u))
        cr.fill()


def hole(cr, x, y, s=1.0, alpha=1.0, glow_a=0.0):
    """Patala's hole in the sea floor: a dark pit (a faint red glow deep inside) and its broken rock lip."""
    cr.save()
    g = cairo.RadialGradient(x, y + 10 * s, 10, x, y, 270 * s)
    g.add_color_stop_rgba(0, 0.30, 0.04, 0.02, alpha)
    g.add_color_stop_rgba(0.35, 0.05, 0.02, 0.02, alpha)
    g.add_color_stop_rgba(1, 0.03, 0.02, 0.02, alpha)
    pc.ell(cr, x, y, 262 * s, 66 * s)
    cr.set_source(g)
    cr.fill()
    cr.restore()
    if glow_a > 0:
        warm(cr, x, y, 160 * s, glow_a, (1.0, 0.3, 0.1))
    prop(cr, "c6_hole_rim", x, y, s, alpha=alpha)


# ------------------------------------------------------------------ puppets


def asura(cr, t, k, x, feet, s, flip=False, front=(-0.5, -0.4), backa=(0.4, -0.3), legs=(0.0, 0.0), rot=0.0,
          alpha=1.0, eyes=0.0, ph=0.0, y=None, head=0.0, hits=()):
    """A Kalakeya: always a dark shadow, its eyes cut through (eyes > 0 adds a red glow to them at night)."""
    if alpha <= 0.01:
        return {}
    rig = C.KALAS[k % 3]
    key = f"c6_kala{k % 3}"
    hy = feet - 434 * s if y is None else y
    ang = man_angles(key, t, front, backa, head, legs, hits, ph)
    pts = silhouette(cr, lambda cr_: puppet(cr_, rig, x, hy, s, rot + bob_rot(t, ph), flip, ang, 1.0, 0.0),
                     0.95 * alpha, C.SIL) or {}
    if eyes > 0 and "head" in pts:
        hx, hy_ = to_user(cr, pts["head"])
        ex = hx + (-1 if flip else 1) * 44 * s
        ey = hy_ - 16 * s
        glow(cr, ex, ey, 70 * s + 20, 0.6 * eyes * alpha)
        cr.new_path()
        cr.arc(ex, ey, 9 * s + 3, 0, 2 * math.pi)
        cr.set_source_rgba(1.0, 0.35, 0.12, 0.9 * eyes * alpha)
        cr.fill()
    return pts


def deva(cr, t, k, x, s, **kw):
    rig, key = (C.DEVA1, "c6_deva1") if k == 1 else (C.DEVA2, "c6_deva2")
    return fig(cr, rig, key, t, x, s, **kw)


def lamp_in(front, s=0.85, alpha=1.0):
    return held("c6_handlamp", front, s, dy=160, alpha=alpha)


def agastya(cr, t, x, s, mood="calm", pot=True, feet=FL, front=(-0.32, -0.55), backa=(0.3, -0.25), **kw):
    """Agastya (short and stout: draw him ~0.9 of the gods' scale), his kamandalu hanging from his back hand."""
    sw = {"c6_agastya_head": "c6_agastya_head" + ("" if mood == "calm" else "_" + mood)}
    ex = dict(kw.pop("extra", {}) or {})
    if pot:
        ex["c6_agastya_armB_lo"] = held("c6_kamandalu", backa, 0.55, dy=158, alpha=kw.get("alpha", 1.0),
                                        blur=kw.get("blur", 0.0))
    return fig(cr, C.AGASTYA, "c6_agastya", t, x, s, front=front, backa=backa, swap=sw, extra=ex, feet=feet, **kw)


def brahma(cr, t, x, ground, s, front=(-0.7, -1.7), backa=(0.25, -1.0), alpha=1.0, blur=0.0, glow_a=1.0, hits=()):
    """Brahma seated cross-legged on his lotus (the lotus on `ground`), blessing; the Vedas in his other hand."""
    if glow_a > 0:
        glow(cr, x, ground - 420 * s, 620 * s + 160, 0.6 * glow_a * alpha)
        aura(cr, t, x, ground - 520 * s, 240 * s, 760 * s, 0.4 * glow_a * alpha, n=22, spin=0.05)
    prop(cr, "md_lotus", x + 30 * s, ground - 110 * s * 1.5, s * 1.5, rot=sway(t, 0.005, 0.3, 2.0), alpha=alpha,
         blur=blur)
    hy = ground - 110 * s * 1.5 - C.SEAT_H * s + 10 * s
    prop(cr, "c6_brahma_seat", x, hy, s, alpha=alpha, blur=blur)
    ang = man_angles("c6_brahma", t, front, backa, 0.0, (0.0, 0.0), hits, 0.8)
    return puppet(cr, C.BRAHMA, x, hy, s, bob_rot(t, 0.8, 0.005), False, ang, alpha, blur,
                  hide=("c6_brahma_legF", "c6_brahma_legB"), swap={"c6_brahma_body": "c6_brahma_body_sit"},
                  extra={"c6_brahma_armB_lo": held("c6_veda", backa, 0.8, dy=160, alpha=alpha, blur=blur)})


def bhagi(cr, t, x, s, pray=True, **kw):
    kw.setdefault("front", ANJALI["front"])
    kw.setdefault("backa", ANJALI["backa"])
    sw = {"c6_bhagi_head": "c6_bhagi_head_pray"} if pray else None
    return fig(cr, C.BHAGI, "c6_bhagi", t, x, s, swap=sw, **kw)


def rishya(cr, t, x, s, mood="calm", **kw):
    sw = {"c6_rishya_head": "c6_rishya_head" + ("" if mood == "calm" else "_" + mood)}
    if kw.pop("kneel", False):
        kw["kneel"] = "c6_rishya_kneel"
    return fig(cr, C.RISHYA, "c6_rishya", t, x, s, swap=sw, **kw)


def vibha(cr, t, x, s, **kw):
    return fig(cr, C.VIBHA, "c6_vibha", t, x, s, **kw)


def loma(cr, t, x, s, **kw):
    return fig(cr, C.LOMA, "c6_loma", t, x, s, **kw)


def farmer(cr, t, x, s, mood="sad", **kw):
    sw = {"c6_farmer_head": "c6_farmer_head" + ("" if mood == "sad" else "_" + mood)}
    return fig(cr, C.FARMER, "c6_farmer", t, x, s, swap=sw, **kw)


def lady(cr, t, rig, key, x, s, feet=FL, mood=None, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(),
         flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.0, y=None, extra=None):
    """A woman() puppet with her feet on `feet`; mood swaps her head (key + '_head_' + mood)."""
    ang = woman_angles(key, t, front, backa, head, hits, ph)
    hy = feet - 470 * s if y is None else y
    sw = {key + "_head": key + "_head_" + mood} if mood else None
    return puppet(cr, rig, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, rods=rods, swap=sw, extra=extra)


def woman_k(cr, t, k, x, s, plate=False, **kw):
    if plate:
        fr = kw.get("front", OFFER)
        kw["front"] = fr
        kw["extra"] = {f"c6_wom{k}_armF_lo": held("c6_plate", fr, 0.62, dy=172, alpha=kw.get("alpha", 1.0))}
    return lady(cr, t, C.WOMEN[k], f"c6_wom{k}", x, s, **kw)


def doe(cr, t, x, feet, s, flip=False, nod=0.0, lift=0.0, legs=0.0, alpha=1.0, blur=0.0, rods=True):
    """The doe standing (feet on `feet`); nod > 0 lowers her head (to nuzzle); legs swings her legs (a step)."""
    sg = -1 if flip else 1
    rot = 0.03 * legs * math.sin(t * 9)
    prop(cr, "c6_doe_body", x, feet - lift, s, rot=rot, alpha=alpha, blur=blur, flip=flip)
    nx, ny = local(x, feet - lift, s, rot, flip, *C.DOE_NECK)
    hr = sg * (0.42 * nod + sway(t, 0.03, 0.4, 1.0))
    prop(cr, "c6_doe_head", nx, ny, s, rot=hr, alpha=alpha, blur=blur, flip=flip)
    if rods:
        pc.rod(cr, x, feet - lift - 380 * s, x + 30, H + 60, alpha=0.45 * alpha)
    return (nx + sg * 230 * s * math.cos(hr) + 200 * s * math.sin(hr) * sg * 0, ny - 230 * s)


def walker(cr, t, fn, t0, t1, x0, x1, s, feet=FL, t_in=None, step=0.42, **kw):
    """A man() puppet walking in jerky rod-puppet steps (fn = a figure function taking legs, rot, y...)."""
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    kw.setdefault("hits", [(t1, 1.0)])
    y = feet - 434 * s + bob - (k - 1) * 300 * s
    return fn(cr, t, x, s * k, legs=walk_legs(ph), rot=rock, alpha=a * kw.pop("alpha", 1.0), blur=b, y=y, **kw), x


def medallion(cr, t, t_in, x, y, r, inner, label, dim=0.0, alpha=1.0):
    """A round leather medallion with a picture inside (inner(cr) draws it, clipped) and a label under it; dim greys
    it out."""
    q = back(clamp((t - t_in) / 0.35), 1.5)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(max(0.01, q), max(0.01, q))
    cr.new_path()
    cr.arc(0, 0, r + 8, 0, 2 * math.pi)
    cr.set_source_rgba(*pc.INK, a)
    cr.fill()
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.set_source_rgba(0.98, 0.90, 0.70, a)
    cr.fill()
    for i in range(24):
        aa = 2 * math.pi * i / 24
        cr.new_sub_path()
        cr.arc((r - 14) * math.cos(aa), (r - 14) * math.sin(aa), 3, 0, 2 * math.pi)
    cr.set_source_rgba(0.62, 0.42, 0.18, 0.8 * a)
    cr.fill()
    cr.arc(0, 0, r - 24, 0, 2 * math.pi)
    cr.clip()
    cr.translate(-x, -y)
    cr.push_group()
    inner(cr)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()
    draw_text(cr, label, x, y + r + 42, 30, INK, a, MONO_FONT, "cm", tracking=2)
    if dim > 0.01:
        cr.save()
        cr.new_path()
        cr.arc(x, y, (r + 8) * q, 0, 2 * math.pi)
        cr.set_source_rgba(0.12, 0.08, 0.06, 0.62 * dim * a)
        cr.fill()
        cr.restore()


# ------------------------------------------------------------------ story 3: Agastya


G1_ASURAS = ((560, 0, 0.42, False), (860, 1, 0.38, True), (1160, 2, 0.44, False), (1450, 1, 0.4, True))


def s_g1(cr, t, tl, t0, t1):
    c = cues(tl, "g1")
    t_out = t0 + CARD_HOLD                              # the chapter card holds, then flies up
    tS = max(c["S"], t_out + 0.3)
    tH = max(c["H"], tS + 0.5, t_out + 0.9)
    lev = 640
    sc = prog(t, t_out - 0.1, 0.6)

    def scene(cr):
        rise = ease((t - t_out) / 0.9)
        sun(cr, t, 1660, 470 - 150 * rise, 0.42, a=0.4 + 0.6 * rise)
        for i, (x, k, s, fl) in enumerate(G1_ASURAS):
            ts = tH - 0.15 + 0.2 * i
            sink = ease((t - ts) / 0.9)
            asura(cr, t, k, x + 20 * math.sin(t * 0.8 + i), lev + 200 + 470 * sink, s, flip=fl,
                  alpha=1 - 0.6 * sink, ph=i * 0.7, front=(-0.6, -0.5), backa=(0.5, -0.4))
            if t > ts + 0.3:
                bubbles(cr, t, ts + 0.3, x, lev + 60, 5, 120)
        sea(cr, t, lev)
    fade_in(cr, sc, scene)
    chapter(cr, t, t0 - 0.3, t_out, "STORY 3 OF 6", [[("THE SAGE WHO", INK)], [("DRANK THE", INK), ("OCEAN", RED)]],
            "MAHABHARATA · VANA PARVA")
    dev_tag = cr.user_to_device(1010, 300)

    def ui(cr):
        if t > t_out:
            tag(cr, t, t_out + 0.2, "KALAKEYA ASURAS", dev_tag[0], dev_tag[1], 36, t_out=tH + 0.2)
            head(cr, t, "BY DAY, THEY HID IN THE", t_out + 0.1, "OCEAN", tS, under=tH + 0.3)
    return dict(ui=ui, flash=flash_at(t, t_out, 0.2) + flash_at(t, tH, 0.12))


G2_HUTS = (1180, 1450, 1720)


def s_g2(cr, t, tl, t0, t1):
    c = cues(tl, "g2")
    tR, tN, tJ, tK = c["R"], c["N"], c["J"], c["K"]
    dark = prog(t, t0, 0.6)
    edge = (800, 880, 900, 1080)
    prop(cr, "moon", 300, 330, 0.62, alpha=0.9)
    glow(cr, 300, 330, 260, 0.35 * dark)
    trees(cr, t, ((1300, 0.5, 10, 0.55, False), (1860, 0.55, 8, 0.6, True), (1580, 0.42, 14, 0.4, False)))
    bank(cr, edge, side=1, top_extra=10)
    prop(cr, "c6_ground", 2564, FL + 6, 1.42)
    lamps = []
    for i, hx in enumerate(G2_HUTS):
        prop(cr, "lr_hut", hx, FL + 6, 0.34)
        out = tK + 0.1 + 0.32 * i
        on = 1 - prog(t, out, 0.25)
        lamps.append((hx, on, i))
        if t > out:
            u = clamp((t - out) / 1.6)
            for k in range(5):                            # a wisp of smoke from the dead lamp
                cr.new_path()
                cr.arc(hx + 14 * math.sin(k * 1.3 + t * 2), FL - 60 - 40 * k - 60 * u, 10 + 4 * k, 0, 2 * math.pi)
                cr.set_source_rgba(0.75, 0.72, 0.70, 0.35 * (1 - u) * (1 - k / 6))
                cr.fill()
    lev = 880
    eyes = []
    for i, (x0, x1, k, s) in enumerate(((180, 1000, 0, 0.4), (380, 1270, 1, 0.37), (560, 1540, 2, 0.42))):
        up = ease((t - tN + 0.2 - 0.15 * i) / 0.8)
        tw0, tw1 = tJ - 0.3 + 0.12 * i, tK + 0.1 + 0.32 * i
        x, bob, rock, ph = hop_walk(t, tw0, tw1, x0, x1, 0.5)
        p = asura(cr, t, k, x, FL + 420 * (1 - up) + bob, s, legs=walk_legs(ph, 0.4), rot=rock + 0.08,
                  front=(-1.1, -0.6), backa=(0.6, -0.5), ph=i)
        if p.get("head"):
            hx_, hy_ = to_user(cr, p["head"])
            eyes.append((hx_ + 44 * s, hy_ - 16 * s, s, up * (1 if hy_ < lev - 20 else 0.4)))
    sea(cr, t, lev, speed=0.6, dark=0.4, edge=edge, side=-1)

    def post(cr):
        for hx, on, i in lamps:
            if on > 0.01:
                glow(cr, hx, FL - 44, 130, 0.9 * on * (0.85 + 0.15 * math.sin(t * 9 + i)))
                warm(cr, hx, FL - 44, 80, 0.9 * on, (1.0, 0.75, 0.3))
        for ex, ey, s_, a in eyes:
            glow(cr, ex, ey, 70 * s_ + 20, 0.6 * a)
            cr.new_path()
            cr.arc(ex, ey, 9 * s_ + 3, 0, 2 * math.pi)
            cr.set_source_rgba(1.0, 0.35, 0.12, 0.9 * a)
            cr.fill()

    def ui(cr):
        if t < tK - 0.15:
            head(cr, t, "BY NIGHT,", tR, "THEY CAME OUT", tN)
        else:
            head(cr, t, "BY NIGHT, THEY", tK - 0.15, "KILLED SAGES", tK + 0.05)
        tag(cr, t, tJ + 0.1, "SAGES' HUTS", 1450, 590, 32, t_out=tK)
    return dict(ui=ui, post=post, night=0.5 * dark, blue=0.55 * dark, lift=1.0, flash=flash_at(t, tK + 0.1, 0.08))


G3_GODS = ((110, "indra"), (215, 1), (320, 2))


def s_g3(cr, t, tl, t0, t1):
    c = cues(tl, "g3")
    tF, tB, tG = c["F"], c["B"], c["G"]
    lev = 480
    for i, x in enumerate((1180, 1420, 1650)):            # the asuras hiding on the far sea floor
        p = asura(cr, t, i, x, 1050, 0.3, flip=i % 2 == 1, alpha=0.55, **CROUCH, y=1050 - 110 * 0.3, ph=i)
        if p.get("head"):
            hx, hy = to_user(cr, p["head"])
            sparkle(cr, hx + (-1 if i % 2 else 1) * 14, hy - 4, 9 + 3 * math.sin(t * 5 + i), 0.7)
    edge = (430, lev, 480, 1080)
    sea(cr, t, lev, dark=1.0, speed=0.7, edge=edge)
    bank(cr, edge, side=-1, rock=True, top_extra=8)
    pts = []
    for i, (x, who) in enumerate(G3_GODS):
        fr = (-1.35, -0.45)
        look = 0.12 * math.sin(t * 0.9 + i * 1.3)
        if who == "indra":
            p = indra(cr, t, x + 40, 0.34, front=fr, feet=lev - 6, head=0.1 + look, ph=i,
                      extra={"indra_armF_lo": lamp_in(fr)})
        else:
            p = deva(cr, t, who, x + 40, 0.34, front=fr, feet=lev - 6, head=0.1 + look, ph=i,
                     extra={f"c6_deva{who}_armF_lo": lamp_in(fr)})
        pts.append(p)
        hx, hy = to_user(cr, p["handF"])
        lx, ly = hx + 26, hy - 26
        glow(cr, lx, ly, 90, 0.7)
        cr.save()                                         # its small cone of light into the water
        g = cairo.LinearGradient(lx, ly, lx + 120, ly + 300)
        g.add_color_stop_rgba(0, 1.0, 0.85, 0.5, 0.35)
        g.add_color_stop_rgba(1, 1.0, 0.85, 0.5, 0.0)
        pc.poly(cr, [(lx, ly), (lx + 40 + 30 * math.sin(t + i), ly + 320), (lx + 230 + 30 * math.sin(t + i), ly + 300)])
        cr.set_operator(cairo.OPERATOR_ADD)
        cr.set_source(g)
        cr.fill()
        cr.restore()
    tops = [cr.user_to_device(*to_user(cr, p["top"])) for p in pts]

    def ui(cr):
        if t < tB - 0.1:
            head(cr, t, "THE GODS COULD NOT", t0 + 0.1, "FIND THEM", tF)
        else:
            head(cr, t, "THE OCEAN WAS", tB - 0.1, "TOO BIG, TOO DEEP", tB + 0.05)
        for i, (x, y) in enumerate(tops):
            mark(cr, t, tF + 0.15 * i, "?", x + 10, y - 40, 70, t_out=tB)
        arrow2(cr, (480, 420), (1830, 420), prog(t, tB, 0.5), True, 12)
        arrow2(cr, (1800, 540), (1800, 1030), prog(t, min(tG, tB + 0.6), 0.45), True, 12)
    return dict(ui=ui, night=0.25, blue=0.3, lift=1.0, flash=flash_at(t, tB, 0.1))


def s_g4(cr, t, tl, t0, t1):
    c = cues(tl, "g4")
    tA, tB, tY, tP = c["A"], c["B"], c["Y"], c["P"]
    trees(cr, t, ((140, 0.6, 9, 0.55, True), (1250, 0.5, 12, 0.45, False)))
    prop(cr, "lr_hut", 1700, FL + 8, 0.5, alpha=0.95)
    ground(cr)
    ax, as_ = 1400, 0.5
    nod = keyed(t, [(t0, 0.0), (tP + 0.35, 1.0), (tP + 0.75, 0.0)], 0.25, 1.3)
    agastya(cr, t, ax, as_, mood="smile" if t > tP + 0.3 else "calm", flip=True, head=0.15 * nod,
            front=mix((-0.32, -0.55), TEACH, keyed(t, [(t0, 0.0), (tP + 0.3, 1.0)], 0.3, 1.2)), ph=0.4)
    bow = keyed(t, [(t0, 0.0), (tB - 0.2, 1.0)], 0.3, 1.3)
    arr = tA + 0.4
    out = {}
    for i, (x0, x1, who) in enumerate(((-150, 760, "indra"), (-380, 550, 1), (-600, 340, 2))):
        fr = mix((-0.32, -0.55), ANJALI["front"], bow)
        bk = mix((0.3, -0.25), ANJALI["backa"], bow) if who != "indra" else mix((0.3, -0.45), ANJALI["backa"], bow)
        if who == "indra":
            fn = (lambda cr_, t_, x_, s_, **kw: indra(cr_, t_, x_, s_, front=fr, backa=bk, head=0.2 * bow,
                                                      extra={}, **kw))
        else:
            fn = (lambda cr_, t_, x_, s_, who=who, **kw: deva(cr_, t_, who, x_, s_, front=fr, backa=bk, head=0.2 * bow,
                                                              **kw))
        p, _ = walker(cr, t, fn, t0 + 0.05 * i, arr, x0, x1, 0.5 if who == "indra" else S, ph=i)
        out[who] = p
    top_a = cr.user_to_device(ax, FL - 640 * as_)

    def ui(cr):
        if t < tP - 0.1:
            head(cr, t, "THE GODS WENT TO", t0 + 0.1, "SAGE AGASTYA", tA)
        else:
            head(cr, t, "THE GODS SAID:", tP - 0.1, "DRINK THE OCEAN!", tP + 0.05)
        tag(cr, t, tA + 0.15, "SAGE AGASTYA", top_a[0], top_a[1] - 40, 34, t_out=tP)
        tag(cr, t, arr, "THE GODS", 550, 330, 30, t_out=tY)
        if t < tP + 0.2:
            cloud_text(cr, t, 1120, 380, 0.56, [("ONLY YOU", 58, INK, -30, tY),
                                                ("CAN HELP US!", 58, RED, 32, tY + 0.3)],
                       alpha=1 - prog(t, tP, 0.25), t_in=tY - 0.15)
    return dict(ui=ui, flash=flash_at(t, tP, 0.15))


G5_FISH = ((760, 700, 0, 0.5), (1020, 820, 1, 0.55), (1320, 640, 2, 0.5), (1600, 780, 0, 0.55), (1180, 900, 1, 0.45))


G5_TOP = 600                         # the sea's surface (and the top of Agastya's bank) before he drinks


def g5_level(t, c):
    return G5_TOP + (950 - G5_TOP) * ease(clamp((t - (c["D"] - 0.1)) / max(1.2, c["B"] - c["D"] + 0.5)))


def s_g5(cr, t, tl, t0, t1):
    c = cues(tl, "g5")
    tK, tP, tD, tB = c["K"], c["P"], c["D"], c["B"]
    floor = 950
    lev = g5_level(t, c)
    edge = (600, G5_TOP, 720, floor)
    seabed(cr, floor - 20, x=1200)
    for i, (x, y, k, s) in enumerate(G5_FISH):            # fish swim, then fall with the water and lie on the sand
        swim = 40 * math.sin(t * 0.8 + i * 1.9)
        yy = max(y, lev + 40)
        rest = floor - 30
        landed = yy >= rest
        yy = min(yy, rest)
        f = max(0.0, math.sin(t * 5 + i * 1.7)) ** 6 if landed else 0.0
        prop(cr, f"c6_fish{k}", x + (0 if landed else swim), yy - 14 * f, s,
             rot=(0.25 * f if landed else 0.08 * math.sin(t * 3 + i)), flip=(i % 2 == 1))
    for x, nm, s in ((900, "c6_shell", 0.55), (1450, "c6_star", 0.5), (1720, "c6_shell", 0.45)):
        prop(cr, nm, x, floor - 8, s)
    sea(cr, t, lev, floor=floor, edge=edge)
    bank(cr, edge, side=-1, top_extra=12)
    for x, s in ((90, 0.7), (520, 0.6)):
        prop(cr, f"rr_grass{int(x) % 3}", x, G5_TOP - 10, s * 0.6, rot=sway(t, 0.02, 0.5, x * 0.01), alpha=0.9)
    drink = tD - 0.25 < t < tB + 0.6
    tilt = keyed(t, [(t0, 0.0), (tD - 0.3, 1.0), (tB + 0.7, 0.0)], 0.3, 1.2)
    pts = agastya(cr, t, 330, 0.47, mood="drink" if drink else ("smile" if t > tB + 0.6 else "calm"), feet=G5_TOP - 10,
                  head=-0.22 * tilt, front=mix((-0.32, -0.55), (-0.9, -0.9), tilt),
                  backa=mix((0.3, -0.25), (-0.5, -0.6), tilt), ph=0.3)
    hx, hy = to_user(cr, pts["head"])
    mouth = (hx + 34, hy + 22)
    vx = 1150
    va = prog(t, tD - 0.3, 0.3) * (1 - prog(t, tB + 0.4, 0.4))
    vortex(cr, t, vx, lev + 26, 260 * (0.6 + 0.4 * clamp((floor - lev) / 400)), va)
    g_in, g_out = prog(t, tD - 0.2, 0.45), prog(t, tB + 0.15, 0.35)
    if g_in > 0.01 and g_out < 0.99:                       # the stream rises from the whirlpool; its tail follows it in
        path = quad((vx, lev + 20), (760, min(lev, mouth[1]) - 300), mouth, 46, t=t, amp=18)
        n0, n1 = int(len(path) * g_out), max(2, int(len(path) * g_in))
        if n1 - n0 >= 2:
            w0 = 90 * clamp((floor - lev) / 300 + 0.3)
            ribbon(cr, t, path[n0:n1], w0 + (18 - w0) * n0 / len(path), 18, alpha=0.95, flow=1.4)
        glow(cr, mouth[0], mouth[1], 90, 0.4 * g_in * (1 - g_out))
    if t > tB:                                            # the last drop flies up to him
        u = clamp((t - tB) / 0.45)
        dx, dy = 1300 + (mouth[0] - 1300) * ease(u), floor - 40 + (mouth[1] - floor + 40) * ease(u) - 220 * math.sin(
            math.pi * u)
        if u < 1:
            prop(cr, "rv_drop", dx, dy, 2.2)
            sparkle(cr, dx, dy, 26, 0.8)

    def ui(cr):
        if t < tP - 0.1:
            head(cr, t, "AGASTYA WENT TO", t0 + 0.1, "THE SEA SHORE", tK)
        else:
            head(cr, t, "HE DRANK IT", tP - 0.1, "ALL!", tD, big_size=124, under=tB - 0.2)
        stamp(cr, t, tB + 0.3, "NOT ONE DROP LEFT", 1200, 760, 58)
    return dict(ui=ui, flash=flash_at(t, tD, 0.15) + flash_at(t, tB + 0.35, 0.12))


G6_AS = ((880, 0, 0.36, True), (1060, 1, 0.33, True), (1250, 2, 0.38, True), (1420, 1, 0.34, True))
G6_HOLE = (1700, 960)
CROUCH = dict(front=(-1.6, -1.8), backa=(-1.4, -1.9), head=0.3, legs=(-1.35, -1.0))   # hiding, knees drawn up


def crouch_pose(up, front_up, back_up):
    """An asura between crouching (up 0) and standing (up 1): arm angles, leg angles and hip height (in s units)."""
    return (mix(CROUCH["front"], front_up, up), mix(CROUCH["backa"], back_up, up), 0.3 * (1 - up),
            mix(CROUCH["legs"], (0.0, 0.0), up), 110 + 324 * up)


def s_g6(cr, t, tl, t0, t1):
    c = cues(tl, "g6")
    tA, tD, tH, tB, tP = c["A"], c["D"], c["H"], c["B"], c["P"]
    floor = 950
    seabed(cr, floor - 20)
    stranded(cr, t, floor, items=((420, 0, 0.5, 0.2), (640, 1, 0.45, -0.1), (980, 2, 0.4, 0.1)))
    hx, hy = G6_HOLE
    hole(cr, hx, hy, 0.85, glow_a=0.5 * prog(t, tB, 0.5))
    tops = []
    for i, (x, k, s, fl) in enumerate(G6_AS):
        up = keyed(t, [(t0, 0.0), (tA + 0.1 * i, 1.0)], 0.3, 1.4)
        if i < 2:                                        # struck down: topple back and dissolve into dust
            fr, bk, hd, lg, hh = crouch_pose(up, (-2.6, -0.4), (0.8, -0.6))
            th = tH + 0.15 + 0.25 * i
            fall = ease((t - th) / 0.5)
            a = 1 - prog(t, th + 0.35, 0.5)
            if a > 0.01:
                p = asura(cr, t, k, x + 60 * fall, floor + 10, s, flip=fl, rot=1.1 * fall, front=fr, backa=bk, head=hd,
                          legs=lg, alpha=a, y=floor + 10 - hh * s, ph=i)
                tops.append(p.get("top"))
            dust(cr, t, th + 0.3, x + 90, floor - 120, 150)
            if tH - 0.05 < t < th + 0.4:
                burst(cr, t, x, floor - 200 * s * 2, th, n=14, rmax=260, alpha=0.9)
        else:                                            # run to the hole and drop into it
            fr, bk, hd, lg, hh = crouch_pose(up, (-2.2, -0.5), (0.6, -0.6))
            tr0 = tB + 0.1 * (i - 2)
            tr1 = tP + 0.1 + 0.25 * (i - 2)
            x_, bob, rock, ph = hop_walk(t, tr0, tr1, x, hx - 20, 0.32)
            sinkp = ease((t - tr1) / 0.5)
            a = 1 - sinkp
            if a > 0.01:
                p = asura(cr, t, k, x_, floor + 10, s * (1 - 0.3 * sinkp), flip=t < tr0 and fl,
                          legs=walk_legs(ph, 0.5) if t > tr0 else lg, rot=rock + 0.12 * (t > tr0), front=fr,
                          backa=bk, head=hd, alpha=a, y=floor + 10 - hh * s + bob + 160 * sinkp, ph=i)
                tops.append(p.get("top"))
    gods_in = tD - 0.1
    gs = 0.5
    for i, (x0, x1, who) in enumerate(((-150, 600, "indra"), (-350, 410, 1), (-560, 220, 2))):
        if who == "indra":
            raise_ = keyed(t, [(t0, 0.0), (tH - 0.3, 1.0)], 0.3, 1.3)
            bk = mix((0.3, -0.45), (-2.7, -0.3), raise_)
            fn = (lambda cr_, t_, x_, s_, bk=bk, **kw: indra(cr_, t_, x_, s_, front=(-1.2, -0.4), backa=bk, **kw))
        else:
            fn = (lambda cr_, t_, x_, s_, who=who, **kw: deva(cr_, t_, who, x_, s_, front=(-1.5, -0.3), **kw))
        p, xi = walker(cr, t, fn, gods_in + 0.06 * i, tH - 0.1, x0, x1, gs, feet=floor + 6, step=0.3, ph=i)
        if who == "indra" and tH - 0.1 < t < tH + 0.8:   # the vajra's flash reaching the first asuras
            hand = to_user(cr, p["handB"])
            for j in range(2):
                tx = G6_AS[j][0]
                q = clamp((t - tH - 0.05 - 0.2 * j) / 0.2)
                if q > 0:
                    a_ = 1 - clamp((t - tH - 0.35 - 0.2 * j) / 0.35)
                    cr.save()
                    cr.set_operator(cairo.OPERATOR_ADD)
                    cr.set_source_rgba(1.0, 0.9, 0.55, 0.8 * a_)
                    cr.set_line_width(10)
                    cr.move_to(*hand)
                    cr.line_to(hand[0] + (tx - hand[0]) * q, hand[1] + (floor - 150 - hand[1]) * q)
                    cr.stroke()
                    cr.restore()
    dev_hole = cr.user_to_device(hx, hy - 120)
    seen = [d for d in tops if d]

    def ui(cr):
        if t < tD - 0.1:
            head(cr, t, "THE OCEAN DRIED UP.", t0 + 0.05, "THE ASURAS WERE SEEN!", tA)
        elif t < tB - 0.1:
            head(cr, t, "THE GODS", tD - 0.1, "DEFEATED THEM", tH)
        else:
            head(cr, t, "THE REST RAN AWAY TO", tB - 0.1, "PATALA", tP)
        if t < tD + 0.6:
            for i, d in enumerate(seen):
                mark(cr, t, tA + 0.1 * i, "!", d[0] + 10, d[1] - 40, 80, t_out=tD + 0.4)
        tag(cr, t, tP + 0.15, "THE UNDERWORLD", dev_hole[0], dev_hole[1] - 60, 32)
    return dict(ui=ui, flash=flash_at(t, tH + 0.15, 0.3) + flash_at(t, tH + 0.4, 0.2))


def s_g7(cr, t, tl, t0, t1):
    c = cues(tl, "g7")
    tB, tR, tV = c["B"], c["R"], c["V"]
    floor = 1010
    seabed(cr, floor - 20, x=1500)
    stranded(cr, t, floor, items=((1020, 0, 0.45, 0.2), (1270, 1, 0.42, -0.1), (1530, 2, 0.45, 0.1),
                                  (1780, 0, 0.4, 0.0)))
    bank(cr, (840, FL - 10, 960, floor + 30), side=-1, top_extra=0)
    prop(cr, "c6_ground", -866, FL + 6, 1.42)
    agastya(cr, t, 380, 0.5, mood="calm", ph=0.3)
    bow = keyed(t, [(t0, 0.0), (tR - 0.15, 1.0)], 0.3, 1.3)
    indra(cr, t, 690, 0.5, flip=True, front=mix((-0.32, -0.55), ANJALI["front"], bow),
          backa=mix((0.3, -0.45), ANJALI["backa"], bow), head=0.18 * bow, feet=FL, ph=0.6)
    old = 600
    dev_lbl = cr.user_to_device(1500, old - 60)

    def ui(cr):
        head(cr, t, "THE GODS SAID:", t0 + 0.1, "NOW FILL IT BACK!", tV)
        q = prog(t, tB, 0.6)
        if q > 0:
            dotted_line(cr, 900, 900 + (1840 - 900) * q, old, t)
        tag(cr, t, tB + 0.4, "THE OCEAN WAS HERE", dev_lbl[0], dev_lbl[1], 30)
        curve_arrow(cr, (820, 440), (1150, 300), (1420, 800), prog(t, tV + 0.1, 0.7), 12)
    return dict(ui=ui, flash=flash_at(t, tV, 0.12))


def s_g8(cr, t, tl, t0, t1):
    c = cues(tl, "g8")
    tM, tW, tP = c["M"], c["W"], c["P"]
    ground(cr, y=FL + 40)
    x, s, feet = 640, 0.74, 1112
    b = C._AG["bulk"]
    hy = feet - 434 * s
    pat = prog(t, tP - 0.45, 0.3)
    bel = local(x, hy, s, 0, False, 118 * b, -100)
    tgt = (bel[0] + 10, bel[1] - 6 + 26 * math.sin((t - tP) * 10) * pat * (t > tP - 0.2))
    fr = mix((-0.32, -0.55), reach_arm(x, hy, s, 26 * b, tgt), pat)
    glow(cr, bel[0], bel[1], 220, 0.25 + 0.2 * pat * (0.6 + 0.4 * math.sin(t * 3)))
    agastya(cr, t, x, s, mood="smile" if t > tM else "calm", feet=feet, front=fr, head=0.05 * math.sin(t * 2) * pat,
            ph=0.2)
    if t > tP - 0.1:                                       # little pat marks by the belly
        for k in range(2):
            ph_ = (t - tP) * 10 / (2 * math.pi) % 1.0
            a = math.sin(math.pi * ph_) * pat
            cr.save()
            cr.set_source_rgba(*INK, 0.6 * a)
            cr.set_line_width(5)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.arc(bel[0] + 40, bel[1] - 10, 60 + 22 * k, -0.7, 0.7)
            cr.stroke()
            cr.restore()
    jolt = keyed(t, [(t0, 0.0), (tP + 0.15, 1.0)], 0.2, 1.8)
    p1 = indra(cr, t, 1400, 0.55, flip=True, head=-0.16 * jolt, rot=-0.04 * jolt, feet=FL + 60,
               front=mix((-0.32, -0.55), (-1.9, -1.3), jolt), ph=0.5)
    p2 = deva(cr, t, 1, 1630, 0.53, flip=True, head=-0.14 * jolt, rot=-0.04 * jolt, feet=FL + 60,
              front=mix((-0.32, -0.55), (-2.0, -1.4), jolt), ph=1.1)
    tops = [p1["top"], p2["top"]]

    def ui(cr):
        head(cr, t, "AGASTYA SMILED:", t0 + 0.1, "I'VE DIGESTED IT!", tP)
        for i, d in enumerate(tops):
            mark(cr, t, tP + 0.25 + 0.12 * i, "!", d[0] - 20, d[1] - 30, 86)
    return dict(ui=ui, flash=flash_at(t, tP, 0.12))


def s_g9(cr, t, tl, t0, t1):
    c = cues(tl, "g9")
    tK, tD, tB = c["K"], c["D"], c["B"]
    floor = 930
    seabed(cr, floor - 20)
    stranded(cr, t, floor, flap=0.6)
    old = 560
    bx = 1640
    if t > tB - 0.3:
        b, k, a = depth(t, tB - 0.3, 0.6)
        brahma(cr, t, bx, floor + 6, 0.4 * k, alpha=a, blur=b, glow_a=a)
    for i, (x0, x1, who) in enumerate(((-120, 1250, "indra"), (-300, 1080, 1), (-480, 900, 2))):
        if who == "indra":
            fn = (lambda cr_, t_, x_, s_, **kw: indra(cr_, t_, x_, s_, **kw))
        else:
            fn = (lambda cr_, t_, x_, s_, who=who, **kw: deva(cr_, t_, who, x_, s_, **kw))
        walker(cr, t, fn, tD - 0.2 + 0.08 * i, max(tB + 0.9, t1 - 0.4), x0, x1, 0.4, feet=floor + 6, ph=i)
    dev_b = cr.user_to_device(bx, floor - 560)

    def ui(cr):
        if t < tD - 0.1:
            head(cr, t, "THE OCEAN STAYED", t0 + 0.1, "EMPTY", tK, under=tK + 0.4)
        else:
            head(cr, t, "SO THE GODS WENT TO", tD - 0.1, "BRAHMA", tB)
        dotted_line(cr, 100, 1820, old, t, alpha=1 - prog(t, tD + 0.5, 0.4))
        tag(cr, t, tK + 0.2, "EMPTY", 960, old - 50, 34, t_out=tD + 0.5)
        tag(cr, t, tB + 0.25, "BRAHMA", dev_b[0], dev_b[1], 34)
    return dict(ui=ui, flash=flash_at(t, tB, 0.15))


def s_g10(cr, t, tl, t0, t1):
    c = cues(tl, "g10")
    tS, tB, tF = c["S"], c["B"], c["F"]
    bp = brahma(cr, t, 470, FL + 60, 0.6, front=mix((-0.32, -0.55), (-0.6, -1.75), prog(t, t0 + 0.3, 0.4)))
    for i, (x, who) in enumerate(((1480, "indra"), (1630, 1), (1780, 2))):
        if who == "indra":
            indra(cr, t, x, 0.42, flip=True, feet=FL + 10, front=ANJALI["front"], backa=ANJALI["backa"], head=0.15,
                  ph=i)
        else:
            deva(cr, t, who, x, 0.42, flip=True, feet=FL + 10, front=ANJALI["front"], backa=ANJALI["backa"], head=0.15,
                 ph=i)
    ground(cr, y=FL + 16)
    hx, hy = to_user(cr, bp["top"])
    cx, cy = 1090, 560
    q = back(clamp((t - tS + 0.2) / 0.4), 1.4)
    if q > 0.01:
        cr.save()
        cr.translate(cx, cy)
        cr.scale(q, q)
        cr.translate(-cx, -cy)
        clip = blob_cloud(cr, cx, cy, 700, 420, alpha=clamp(q), tail=(hx + 120, hy + 120))
        cr.save()
        clip()
        a1 = 1 - prog(t, tB - 0.1, 0.3)
        if a1 > 0.01:
            draw_text(cr, "LONG, LONG", cx, cy - 40, 72, INK, a1, HEAD_FONT, "cm")
            draw_text(cr, "AFTER...", cx, cy + 40, 72, RED, a1, HEAD_FONT, "cm")
        if t > tB - 0.2:
            b_, k, a = depth(t, tB - 0.2, 0.45)
            glow(cr, cx - 190, cy, 160, 0.4 * a)
            bhagi(cr, t, cx - 190, 0.3 * k, feet=cy + 150, alpha=a, blur=b_, front=PRAY_UP, backa=PRAY_UP, rods=False)
            pc.poly(cr, [(cx - 420, cy + 150), (cx - 70, cy + 150), (cx + 10, cy + 260), (cx - 420, cy + 260)])
            cr.set_source_rgba(*C.SAND, a)
            cr.fill_preserve()
            cr.set_source_rgba(*pc.INK, a)
            cr.set_line_width(4)
            cr.stroke()
        if t > tF - 0.3:                                    # a little sea filling up beside him in the vision
            lv = cy + 230 - 150 * ease((t - tF + 0.3) / 1.0)
            sea(cr, t, lv, floor=cy + 260, x0=cx - 30, x1=cx + 420, sc=0.4, rows=3)
        cr.restore()
        cr.restore()
    dev_bh = cr.user_to_device(cx - 190, cy - 185)

    def ui(cr):
        head(cr, t, "BRAHMA SAID: ONE DAY,", t0 + 0.1, "BHAGIRATHA WILL FILL IT", tB)
        tag(cr, t, tB + 0.25, "KING BHAGIRATHA", dev_bh[0], dev_bh[1], 30)
    return dict(ui=ui, flash=flash_at(t, tB, 0.12))


G11_TOP = 640                        # the top of Bhagiratha's bank; the ocean fills up to just under it


def g11_level(t, c, floor):
    return floor - (floor - G11_TOP - 20) * ease(clamp((t - c["P"] - 0.2) / max(1.5, c["B"] - c["P"] + 0.6)))


def s_g11(cr, t, tl, t0, t1):
    c = cues(tl, "g11")
    tT, tG, tA, tP, tB = c["T"], c["G"], c["A"], c["P"], c["B"]
    floor = 1000
    lev = g11_level(t, c, floor)
    edge = (620, G11_TOP, 760, floor)
    for i, (x, y, s) in enumerate(((1560, 300, 1.0), (1790, 250, 1.15), (1380, 360, 0.8), (1880, 380, 0.9))):
        prop(cr, "rr_lcloud", x + 10 * math.sin(t * 0.5 + i), y, s, alpha=0.9)
    glow(cr, 1650, 320, 420, 0.3 + 0.3 * prog(t, tG - 0.3, 0.5))
    seabed(cr, floor - 20, x=1350)
    for i, (x, k, s) in enumerate(((900, 0, 0.5), (1200, 1, 0.5), (1500, 2, 0.5), (1760, 0, 0.45))):
        covered = lev < floor - 120
        if not covered:
            f = max(0.0, math.sin(t * 5 + i * 1.7)) ** 6
            prop(cr, f"c6_fish{k}", x, floor - 30 - 14 * f, s, rot=0.25 * f, flip=i % 2 == 1)
        else:
            yy = max(lev + 80, floor - 200 + 30 * math.sin(t + i))
            prop(cr, f"c6_fish{k}", x + 50 * math.sin(t * 0.7 + i), min(yy, floor - 40), s,
                 rot=0.08 * math.sin(t * 3 + i), flip=i % 2 == 1)
    sea(cr, t, lev, floor=floor, edge=edge)
    bank(cr, edge, side=-1, top_extra=12)
    prop(cr, "c6_ground", -1284, G11_TOP - 6, 1.42)
    tap = prog(t, tT, 0.6)
    bx_, bf = 300, G11_TOP - 12
    aura(cr, t, bx_, bf - 300, 120, 420, 0.5 * tap, n=18, spin=0.08)
    glow(cr, bx_, bf - 260, 300, 0.3 + 0.3 * tap)
    bp = bhagi(cr, t, bx_, 0.44, feet=bf, ph=0.4)
    # Ganga: comes down from the clouds, her river-body trailing back up to the sky
    dsc = ease((t - tG + 0.3) / max(1.0, tA - tG + 0.6))
    gx = 1630 - 170 * dsc + 14 * math.sin(t * 1.3)
    gy = -260 + (470 + 260) * dsc + 10 * math.sin(t * 1.7)
    gs = 0.5
    if t > tG - 0.35:
        glow(cr, gx, gy - 120, 340, 0.55)
        trail = quad((gx - 10, gy + 10), (gx + 260, gy + 180), (1990, 290), 44, t=t, amp=22)
        ribbon(cr, t, trail, 120, 230, alpha=0.95, flow=1.0)
        if t > tP - 0.2:                                   # her water pours down into the empty bed
            g = prog(t, tP - 0.2, 0.5)
            pour = quad((gx + 30, gy + 30), (gx - 80, gy + 260), (1000, max(lev, G11_TOP + 40)), 40, t=t, amp=14)
            n = max(2, int(len(pour) * g))
            ribbon(cr, t, pour[:n], 90, 160, alpha=0.95, flow=1.6)
            if g >= 1:
                bubbles(cr, t, tP + 0.3, 1000, max(lev, G11_TOP + 40), 8, 160)
        ang = woman_angles("c6_ganga", t, (-1.0, -0.6), (-0.5, -0.9), 0.1, (), 0.3)
        puppet(cr, C.GANGA, gx, gy, gs, -0.12 + 0.03 * math.sin(t * 1.4), True, ang, 1.0, 0.0, rods=False)
    dev_b = bp["top"]
    dev_g = cr.user_to_device(gx - 300, max(310, gy - 130))

    def ui(cr):
        if t < tG - 0.1:
            head(cr, t, "BHAGIRATHA", t0 + 0.1, "PRAYED", tT)
        elif t < tP - 0.1:
            head(cr, t, "AND GANGA CAME", tG - 0.1, "DOWN TO EARTH", tA)
        else:
            head(cr, t, "GANGA FILLED THE", tP - 0.1, "EMPTY OCEAN", tB)
        tag(cr, t, t0 + 0.4, "KING BHAGIRATHA", dev_b[0], dev_b[1] - 40, 30, t_out=tP)
        tag(cr, t, tA + 0.1, "GANGA", dev_g[0], dev_g[1], 34)
    return dict(ui=ui, flash=flash_at(t, tG, 0.15) + flash_at(t, tB, 0.1))


# ------------------------------------------------------------------ story 4: Rishyashringa


def forest(cr, t, hut=(1320, 0.5), tree_set=None):
    trees(cr, t, tree_set or ((140, 0.62, 7, 0.65, True), (1820, 0.6, 9, 0.6, False), (980, 0.45, 14, 0.4, True)))
    if hut:
        prop(cr, "lr_hut", hut[0], FL + 8, hut[1])
    ground(cr)


def s_s1(cr, t, tl, t0, t1):
    c = cues(tl, "s1")
    t_out = t0 + CARD_HOLD                              # the chapter card holds, then flies up
    tN = max(c["N"], t_out + 0.4)
    sc = prog(t, t_out - 0.1, 0.6)

    def scene(cr):
        forest(cr, t, hut=(1450, 0.52))
        wave = keyed(t, [(t0, 0.0), (tN - 0.2, 1.0)], 0.3, 1.3)
        pv = vibha(cr, t, 700, 0.58, feet=FL, front=mix((-0.32, -0.55), TEACH, wave), ph=0.3, hits=[(t_out, 0.4)])
        pb = rishya(cr, t, 1010, 0.47, flip=True, feet=FL, mood="smile" if t > tN + 0.3 else "calm", ph=1.1,
                    hits=[(tN, 0.5)])
        return pv, pb
    res = fade_in(cr, sc, scene)
    chapter(cr, t, t0 - 0.3, t_out, "STORY 4 OF 6", [[("THE BOY WHO HAD", INK)], [("NEVER SEEN A", INK),
                                                                                  ("WOMAN", RED)]],
            "MAHABHARATA · VANA PARVA & RAMAYANA")

    def ui(cr):
        if t > t_out and res:
            pv, pb = res
            head(cr, t, "A SAGE IN THE FOREST, AND HIS SON:", t_out + 0.1, "RISHYASHRINGA", tN)
            tag(cr, t, t_out + 0.3, "SAGE VIBHANDAKA", pv["top"][0] - 40, pv["top"][1] - 30, 30)
            tag(cr, t, tN + 0.1, "HIS SON", pb["top"][0] + 20, pb["top"][1] - 40, 30)
    return dict(ui=ui, flash=flash_at(t, t_out, 0.2))


def s_s2(cr, t, tl, t0, t1):
    c = cues(tl, "s2")
    tS, tH, tM, tD = c["S"], c["H"], c["M"], c["D"]
    trees(cr, t, ((1500, 0.7, 12, 0.5, False), (200, 0.7, 14, 0.45, True)))
    x, s = 660, 1.25
    hy = 1072
    reach = keyed(t, [(t0, 0.0), (tD - 0.1, 1.0)], 0.3, 1.2)
    pb = rishya(cr, t, x, s, mood="smile" if t > tD else "calm", y=hy, front=mix((-0.32, -0.55), (-1.2, -0.5), reach),
                head=-0.04 * reach, ph=0.4, rods=False)
    dx = 2150 + (1290 - 2150) * ease((t - tM + 0.2) / 1.0)
    walking = tM - 0.2 < t < tM + 0.8
    nuz = keyed(t, [(t0, 0.0), (tD - 0.15, 1.0)], 0.3, 1.2)
    doe(cr, t, dx, 1090, 0.95, flip=True, nod=0.5 * nuz + 0.1 * math.sin(t * 2) * nuz, legs=1.0 if walking else 0.0)
    horn_tip = local(x, hy, s, 0, False, 6 + 60, -300 - 236)
    dev_h = cr.user_to_device(*horn_tip)
    dev_d = cr.user_to_device(dx - 60, 380)

    def ui(cr):
        if t < tM - 0.1:
            head(cr, t, "ON HIS FOREHEAD:", t0 + 0.1, "A SMALL HORN", tH)
        else:
            head(cr, t, "AND THE MAHABHARATA SAYS:", tM - 0.1, "HIS MOTHER WAS A DOE", tD)
        if t > tH:
            red_ring(cr, dev_h[0], dev_h[1] + 20, 80, 110, prog(t, tH + 0.05, 0.45), 9,
                     alpha=1 - prog(t, tM, 0.3))
        tag(cr, t, tH + 0.3, "A SMALL HORN", dev_h[0] + 300, dev_h[1] + 10, 36, t_out=tM)
        tag(cr, t, tD + 0.2, "HIS MOTHER", dev_d[0], dev_d[1], 36)
    return dict(ui=ui, flash=flash_at(t, tH, 0.12))


def outline_person(cr, x, feet, h, alpha=1.0, woman_=False, col=None):
    """A dotted outline of a person (someone he has never seen), feet at (x, feet), h tall."""
    col = col or (0.30, 0.20, 0.12)
    r = h * 0.11
    cr.save()
    cr.set_dash([10, 9])
    cr.set_line_width(5)
    cr.set_source_rgba(*col, alpha)
    cr.arc(x, feet - h + r, r, 0, 2 * math.pi)
    cr.stroke()
    top = feet - h + 2.3 * r
    if woman_:
        cr.arc(x - r * 1.1, feet - h + r * 0.9, r * 0.55, 0, 2 * math.pi)
        cr.stroke()
        pc.poly(cr, [(x - 0.12 * h, top), (x + 0.12 * h, top), (x + 0.14 * h, feet - 0.5 * h),
                     (x + 0.26 * h, feet), (x - 0.26 * h, feet), (x - 0.12 * h, feet - 0.5 * h)])
    else:
        pc.poly(cr, [(x - 0.15 * h, top), (x + 0.15 * h, top), (x + 0.13 * h, feet - 0.45 * h),
                     (x + 0.1 * h, feet), (x - 0.1 * h, feet), (x - 0.13 * h, feet - 0.45 * h)])
    cr.stroke()
    cr.restore()


def s_s3(cr, t, tl, t0, t1):
    c = cues(tl, "s3")
    tP, tI, tN, tA = c["P"], c["I"], c["N"], c["A"]
    forest(cr, t, hut=None, tree_set=((140, 0.62, 7, 0.6, True), (1850, 0.6, 9, 0.55, False)))
    pb = rishya(cr, t, 420, 0.6, mood="puzzled" if t > tI else "calm", feet=FL, head=-0.08, ph=0.3,
                front=mix((-0.32, -0.55), (-0.6, -2.3), keyed(t, [(t0, 0.0), (tA, 1.0)], 0.3, 1.2)))
    hx, hy = to_user(cr, pb["top"])
    cx, cy = 1160, 570
    q = back(clamp((t - t0 - 0.1) / 0.4), 1.4)
    if q > 0.01:
        cr.save()
        cr.translate(cx, cy)
        cr.scale(q, q)
        cr.translate(-cx, -cy)
        clip = blob_cloud(cr, cx, cy, 900, 470, alpha=clamp(q), tail=(hx + 60, hy + 40))
        cr.save()
        clip()
        pa = prog(t, tP, 0.3)
        fx = cx - 230 + 120 * prog(t, tA, 0.4)
        if pa > 0:
            cr.save()
            cr.translate(fx, cy + 110)
            cr.scale(0.62 * (0.8 + 0.2 * pa), 0.62 * (0.8 + 0.2 * pa))
            pc.paint_part(cr, "c6_vibha_head", pa)
            cr.restore()
        pi = prog(t, tI, 0.3) * (1 - prog(t, tA - 0.1, 0.3))
        for k, ox in enumerate((60, 230)):
            outline_person(cr, cx + ox, cy + 180, 300, alpha=pi * prog(t, tI + 0.2 * k, 0.3))
        pw = prog(t, tA, 0.3)
        if pw > 0:
            outline_person(cr, cx + 170, cy + 190, 330, alpha=pw, woman_=True, col=RED)
        cr.restore()
        cr.restore()
    dev_f = cr.user_to_device(cx - 230, cy - 140)

    def ui(cr):
        if t < tA - 0.1:
            head(cr, t, "EXCEPT HIS FATHER, HE", t0 + 0.1, "NEVER SAW ANYONE ELSE", tN)
        else:
            head(cr, t, "AND A WOMAN?", tA - 0.1, "NEVER!", tA + 0.3, big_size=124)
        if t < tA + 0.2:
            plaque_text(cr, t, tP + 0.2, "FATHER", dev_f[0], dev_f[1], 30, t_out=tA)
        for k, ox in enumerate((60, 230)):
            mark(cr, t, tI + 0.25 + 0.2 * k, "?", cx + ox, cy - 150, 80, t_out=tA - 0.1)
        mark(cr, t, tA + 0.15, "?", cx + 330, cy - 60, 150)
    return dict(ui=ui, flash=flash_at(t, tA, 0.1))


CROPS = ((230, 0.85), (420, 0.8), (610, 0.85), (1220, 0.8), (1420, 0.85), (1620, 0.8))


def anga_land(cr, t, wet=0.0, crops_dry=1.0, green=0.0):
    prop(cr, "c6_earth", W / 2, FL - 30, 0.82, alpha=1 - wet)
    if wet > 0:
        prop(cr, "c6_earth_wet", W / 2, FL - 30, 0.82, alpha=wet)
    for i, (x, s) in enumerate(CROPS):
        d = clamp(crops_dry * 1.4 - 0.08 * i) if crops_dry < 1 else 1.0
        g = clamp(green * 1.3 - 0.06 * i)
        a_green = max(1 - d, g)
        if a_green < 0.99:
            prop(cr, "c6_crop_dry", x, FL - 26, s, rot=0.05 * math.sin(t + i), alpha=1 - a_green)
        if a_green > 0.01:
            prop(cr, "c6_crop_green", x, FL - 26, s * (0.8 + 0.2 * a_green), rot=sway(t, 0.03, 0.5, i), alpha=a_green)


def s_s4(cr, t, tl, t0, t1):
    c = cues(tl, "s4")
    tA, tS, tR, tK, tL = c["A"], c["S"], c["R"], c["K"], c["L"]
    sun(cr, t, 1620, 380, 0.5, hard=1.0)
    heat(cr, t, FL - 30, a=0.8)
    anga_land(cr, t, crops_dry=clamp((t - tK + 0.1) / 1.0))
    vin = prog(t, tL - 0.2, 0.5)
    if vin > 0.01:
        b, k, a = depth(t, tL - 0.2, 0.5)
        farmer(cr, t, 900, 0.52 * k, feet=FL - 26, alpha=a, blur=b, head=0.18, ph=0.3,
               front=(-0.15, -0.3), backa=(0.2, -0.2))
        lady(cr, t, C.VWOMAN, "c6_vwom", 1080, 0.5 * k, feet=FL - 26, mood=None, flip=True, alpha=a, blur=b,
             head=0.12, ph=0.9)
    years = ("1 YEAR", "2 YEARS", "3 YEARS", "MANY YEARS")
    kk = min(3, max(0, int((t - tS) / 0.45))) if t > tS else 0

    def ui(cr):
        if t < tK - 0.1:
            head(cr, t, "MEANWHILE, IN THE KINGDOM OF ANGA:", tA - 0.1, "NO RAIN FOR YEARS", tR)
        else:
            head(cr, t, "THE FIELDS DRIED UP,", tK - 0.1, "PEOPLE WENT HUNGRY", tL)
        if t > tS - 0.3:
            card(cr, t, tS - 0.3, 420, 440, 0.64, [("NO RAIN:", 70, INK, -36), (years[kk], 90, RED, 46)])
    return dict(ui=ui, eve=0.22, flash=flash_at(t, tR, 0.08))


def s_s5(cr, t, tl, t0, t1):
    c = cues(tl, "s5")
    tK, tJ, tR = c["K"], c["J"], c["R"]
    prop(cr, "arch", 400, FL - 26, 0.44)
    anga_land(cr, t, crops_dry=1.0)
    pk = loma(cr, t, 400, S, feet=FL - 26, ph=0.3, head=0.05 * math.sin(t * 0.8),
              front=mix((-0.32, -0.55), (-0.6, -1.7), keyed(t, [(t0, 0.0), (tR + 0.2, 1.0)], 0.3, 1.2)))
    teach = keyed(t, [(t0, 0.0), (tJ - 0.2, 1.0)], 0.3, 1.3)
    pa = fig(cr, C.BRAHMIN_A, "c6_brahA", t, 1340, 0.54, flip=True, feet=FL - 26,
             front=mix((-0.32, -0.55), TEACH, teach), ph=0.7, hits=[(tJ, 0.4)])
    fig(cr, C.BRAHMIN_B, "c6_brahB", t, 1560, 0.52, flip=True, feet=FL - 26, front=ANJALI["front"],
        backa=ANJALI["backa"], ph=1.4)

    def ui(cr):
        head(cr, t, "THE BRAHMINS TOLD THE KING:", t0 + 0.1, "BRING THE FOREST BOY", tJ)
        tag(cr, t, tK + 0.1, "KING LOMAPADA", pk["top"][0] - 20, pk["top"][1] - 30, 30)
        tag(cr, t, t0 + 0.6, "BRAHMINS", pa["top"][0] + 110, pa["top"][1] - 50, 30)
        card2(cr, t, tJ + 0.1, 870, 500, 0.8, [("IF THE FOREST BOY COMES,", 60, INK, -40, tJ + 0.2),
                                                ("RAIN WILL COME!", 92, RED, 48, tR)])
    return dict(ui=ui, eve=0.12, flash=flash_at(t, tR, 0.1))


def s_s6(cr, t, tl, t0, t1):
    c = cues(tl, "s6")
    tQ, tR, tA, tJ = c["Q"], c["R"], c["A"], c["J"]
    trees(cr, t, ((1620, 0.58, 4, 0.8, False), (1860, 0.62, 3, 0.85, True), (1420, 0.45, 10, 0.5, False)))
    prop(cr, "arch", 300, FL - 26, 0.44, alpha=0.9)
    anga_land(cr, t, crops_dry=1.0)
    point = keyed(t, [(t0, 0.0), (tR + 0.1, 1.0)], 0.3, 1.3)
    loma(cr, t, 330, S, feet=FL - 26, front=mix((-0.32, -0.55), POINT, point), ph=0.3, hits=[(tR, 0.5)])
    for i in range(3):
        tw0 = tA - 0.2 + 0.25 * i
        x, bob, rock, ph = hop_walk(t, tw0, tw0 + 3.2, 480 - 160 * i, 1500 - 160 * i, 0.5)
        if t > tw0 - 0.3:
            b, k, a = depth(t, tw0 - 0.3, 0.45)
            woman_k(cr, t, i, x, 0.5 * k, plate=(i == 0), feet=FL - 26, y=FL - 26 - 470 * 0.5 * k + bob, rot=rock,
                    alpha=a, blur=b, ph=i)

    def ui(cr):
        if t < tR - 0.1:
            head(cr, t, "BUT HOW WOULD HE", t0 + 0.1, "LEAVE THE FOREST?", tQ)
        else:
            head(cr, t, "SO THE KING SENT SOME", tR - 0.1, "WOMEN TO THE FOREST", tA)
        if t < tR + 0.4:
            big_q(cr, t, tQ, 960, 520, 300, alpha=1 - prog(t, tR, 0.35))
    return dict(ui=ui, eve=0.1, flash=flash_at(t, tQ, 0.08))


def s_s7(cr, t, tl, t0, t1):
    c = cues(tl, "s7")
    tD, tA, tK, tB, tF, tM = c["D"], c["A"], c["K"], c["B"], c["F"], c["M"]
    forest(cr, t, hut=None, tree_set=((140, 0.62, 7, 0.6, True), (1860, 0.6, 9, 0.55, False)))
    taste = keyed(t, [(t0, 0.0), (tF + 0.7, 1.0)], 0.3, 1.2)
    pb = rishya(cr, t, 440, S, mood="smile" if t > tM - 0.1 else ("wonder" if t > tD else "calm"), feet=FL, ph=0.3,
                front=mix((-0.32, -0.55), (-0.75, -2.1), taste), head=-0.05)
    step = keyed(t, [(t0, 0.0), (tF - 0.1, 1.0)], 0.4, 1.1)
    pts = []
    for i, x in enumerate((1010, 1240, 1470)):
        xx = x - 180 * step if i == 0 else x
        talk = 0.08 * math.sin(t * 7 + i) * (tB < t < tB + 1.4)
        p = woman_k(cr, t, i, xx, 0.54, plate=(i == 0), flip=True, feet=FL, ph=i * 0.8, head=talk,
                    mood="smile" if t > tF else None,
                    front=mix(OFFER, (-1.2, -0.6), step) if i == 0 else (-0.08, -0.35))
        pts.append(p)
    if tF + 0.2 < t < tF + 0.75:                           # a "fruit" flies from the plate to his hand
        u = ease((t - tF - 0.2) / 0.55)
        hand = to_user(cr, pts[0]["handF"])
        tgt = to_user(cr, pb["handF"])
        fx = hand[0] + (tgt[0] - hand[0]) * u
        fy = hand[1] - 60 + (tgt[1] - hand[1]) * u - 160 * math.sin(math.pi * u)
        prop(cr, "c6_fruit", fx, fy, 0.5, rot=3 * u)
    elif t >= tF + 0.75:
        hand = to_user(cr, pb["handF"])
        prop(cr, "c6_fruit", hand[0] + 6, hand[1] - 20, 0.5)
        if t > tM - 0.1:
            for k in range(4):
                sparkle(cr, hand[0] + 50 * math.cos(t * 2 + k * 1.6), hand[1] - 70 + 40 * math.sin(t * 2 + k * 1.6),
                        18 + 6 * math.sin(t * 6 + k), 0.85)
    top_b = pb["top"]
    dev_sari = cr.user_to_device(1240, FL - 150)
    heads = [p["head"] for p in pts]

    def ui(cr):
        if t < tM - 0.1:
            head(cr, t, "HE THOUGHT:", tD, "STRANGE SAGES?", tA)
        else:
            head(cr, t, "HE THOUGHT:", tM - 0.1, "SWEET FRUITS?", tM)
        for k in range(3):
            mark(cr, t, tD + 0.15 + 0.15 * k, "?", top_b[0] - 60 + 60 * k, top_b[1] - 50 - 20 * (k % 2), 64,
                 t_out=tF)
        if t > tK:
            red_ring(cr, dev_sari[0], dev_sari[1], 110, 180, prog(t, tK, 0.4), 8, alpha=1 - prog(t, tF, 0.3))
        tag(cr, t, tK + 0.2, "DIFFERENT CLOTHES", dev_sari[0], 330, 30, t_out=tB + 0.1)
        if tB < t < tF + 0.3:
            for i, hd in enumerate(heads):
                talk_marks(cr, t, tB + 0.15 * i, hd[0] - 46, hd[1] + 30, alpha=1 - prog(t, tF, 0.3))
        tag(cr, t, tB + 0.25, "DIFFERENT TALK", 1470, 330, 30, t_out=tF + 0.2)
    return dict(ui=ui, flash=flash_at(t, tM, 0.1))


def s_s8(cr, t, tl, t0, t1):
    c = cues(tl, "s8")
    tS, tP, tK = c["S"], c["P"], c["K"]
    glow(cr, 760, 600, 520, 0.4)
    fx, fy, fs = 760, 640, 2.4
    split = ease((t - tS + 0.1) / 0.5)
    take = ease((t - tP + 0.1) / 0.6)
    x, s, feet = 1450, 0.78, 1112
    reach = keyed(t, [(t0, 0.0), (tP + 0.3, 1.0)], 0.3, 1.2)
    pb = rishya(cr, t, x, s, mood="smile" if t > tP else "wonder", flip=True, feet=feet, ph=0.4,
                front=mix((-0.32, -0.55), (-0.85, -2.0), reach))
    hand = to_user(cr, pb["handF"])
    if split <= 0:
        prop(cr, "c6_fruit", fx, fy + 8 * math.sin(t * 2), fs, rot=0.05 * math.sin(t * 1.6))
    else:
        prop(cr, "c6_fruitL", fx - 150 * split, fy + 30 * split, fs, rot=-0.25 * split)
        rx = fx + 150 * split + (hand[0] - fx - 150 * split) * take
        ry = fy + 30 * split + (hand[1] - 40 - fy - 30 * split) * take - 200 * math.sin(math.pi * take)
        prop(cr, "c6_fruitR", rx, ry, fs * (1 - 0.6 * take), rot=0.25 * split - 0.2 * take)
        if t < tS + 1.2:
            burst(cr, t, fx, fy, tS, n=14, rmax=420, alpha=0.6)
        for k in range(5):
            sparkle(cr, fx + 230 * math.cos(t * 1.5 + k * 1.25), fy + 200 * math.sin(t * 1.5 + k * 1.25),
                    16 + 8 * math.sin(t * 5 + k), 0.8 * split * (1 - take * 0.6))
    if t > tK - 0.2:
        for k in range(4):
            sparkle(cr, hand[0] + 60 * math.cos(t * 2 + k * 1.6), hand[1] - 90 + 40 * math.sin(t * 2 + k * 1.6),
                    20, 0.85)

    def ui(cr):
        if t < tP - 0.1:
            head(cr, t, "THEY WERE NOT FRUITS. THEY WERE", t0 + 0.1, "SWEETS!", tS, big_size=124)
        else:
            head(cr, t, "IT WAS HIS", tP - 0.1, "FIRST SWEET EVER", tK, under=tK + 0.4)
        tag(cr, t, tS + 0.35, "A LADDU INSIDE!", fx, 930, 36, t_out=tP + 0.2)
    return dict(ui=ui, flash=flash_at(t, tS, 0.15))


def boat(cr, t, x, deck, s, passengers=True, alpha=1.0, boy_mood="wonder"):
    rock = 0.02 * math.sin(t * 1.6)
    by = deck + 6 * math.sin(t * 1.9)
    prop(cr, "c6_boat_hut", x, by, s, rot=rock, alpha=alpha)
    if passengers:
        rishya(cr, t, x - 220 * s, 0.42 * s / 0.6, mood=boy_mood, feet=by + 4, rot=rock, ph=0.4, rods=False)
        woman_k(cr, t, 1, x + 200 * s, 0.4 * s / 0.6, flip=True, feet=by + 4, rot=rock, ph=1.0, rods=False)
        woman_k(cr, t, 2, x + 330 * s, 0.4 * s / 0.6, flip=True, feet=by + 4, rot=rock, ph=1.6, rods=False)
    prop(cr, "c6_boat_hull", x, by, s, rot=rock, alpha=alpha)
    pc.rod(cr, x - 200 * s, by + 80 * s, x - 160, H + 60, alpha=0.4 * alpha)
    pc.rod(cr, x + 260 * s, by + 80 * s, x + 300, H + 60, alpha=0.4 * alpha)


def s_s9(cr, t, tl, t0, t1):
    c = cues(tl, "s9")
    tN, tA = c["N"], c["A"]
    for i, (x0, s, b, a) in enumerate(((0, 0.5, 10, 0.55), (520, 0.45, 12, 0.5), (1040, 0.5, 10, 0.55),
                                       (1560, 0.42, 12, 0.5), (2080, 0.5, 10, 0.55))):
        x = (x0 - 90 * (t - t0)) % 2600 - 340
        prop(cr, "tree", x, 650, s, rot=sway(t, 0.006, 0.3, i), alpha=a, blur=b, flip=i % 2 == 0)
    prop(cr, "c6_ground", W / 2 + 220 - 60 * (t - t0), 650, 1.0, alpha=0.8)
    bx = 760 + 120 * clamp((t - t0) / max(1.0, t1 - t0))
    boat(cr, t, bx, 768, 0.62)
    sea(cr, t, 806, floor=1130, speed=2.6, rows=3)

    def ui(cr):
        if t < tA - 0.1:
            head(cr, t, "THE WOMEN TOOK HIM ON A", t0 + 0.1, "BOAT-HERMITAGE", tN)
        else:
            head(cr, t, "ALL THE WAY TO", tA - 0.1, "ANGA", tA)
        tag(cr, t, tA + 0.1, "ANGA  →", 1660, 560, 40)
    return dict(ui=ui)


S10_DANCERS = ((1320, "farmer"), (1520, "vwom"), (1710, "farmer2"))


def s_s10(cr, t, tl, t0, t1):
    c = cues(tl, "s10")
    tP, tB = c["P"], c["B"]
    wet = prog(t, tB, 0.9)
    clouds = ease((t - tP - 0.2) / max(0.6, tB - tP))
    for i, (x, y, s) in enumerate(((-200 + 560 * clouds, 220, 0.8), (2100 - 560 * clouds, 230, 0.85),
                                   (-300 + 840 * clouds, 300, 0.62), (2200 - 800 * clouds, 310, 0.66))):
        prop(cr, "cloud", x + 10 * math.sin(t + i), y, s, alpha=clouds)
    sun(cr, t, 1620, 380, 0.45, a=1 - clouds, hard=1 - clouds)
    anga_land(cr, t, wet=wet, crops_dry=1.0, green=prog(t, tB + 0.3, 1.2))
    sea(cr, t, 820, floor=1130, x0=-120, x1=380, speed=0.6, rows=2)
    boat(cr, t, 60, 810, 0.55, passengers=False)
    step_x, bob, rock, ph = hop_walk(t, t0 + 0.3, tP + 0.02, 330, 640, 0.42)
    pb = rishya(cr, t, step_x, S, mood="wonder" if t > tB - 0.1 else "calm", y=FL - 26 - 434 * S + bob, rot=rock,
                legs=walk_legs(ph), head=-0.2 * prog(t, tB, 0.4), ph=0.3,
                front=mix((-0.32, -0.55), (-2.4, -0.3), prog(t, tB + 0.2, 0.4)))
    if t > tP:
        sound_rings(cr, 650, FL - 20, t, tP, 3, 0.25, 260, alpha=0.6, color=LIGHT)
        glow(cr, 650, FL - 30, 200, 0.6 * math.exp(-3 * (t - tP)))
    dance = prog(t, tB + 0.3, 0.4)
    for i, (x, who) in enumerate(S10_DANCERS):
        hop = abs(math.sin((t - tB) * 5 + i)) * 26 * dance
        arms = mix((-0.15, -0.3), PRAY_UP, dance * (0.6 + 0.4 * abs(math.sin((t - tB) * 5 + i))))
        if who == "vwom":
            lady(cr, t, C.VWOMAN, "c6_vwom", x, 0.5, feet=FL - 26 - hop, mood="smile" if dance > 0.5 else None,
                 flip=True, front=arms, backa=arms, head=-0.1 * dance, ph=i)
        else:
            farmer(cr, t, x, 0.5, mood="happy" if dance > 0.5 else "sad", flip=True, feet=FL - 26 - hop,
                   front=arms, backa=arms, head=-0.12 * dance + 0.15 * (1 - dance), ph=i)
    rain(cr, t, prog(t, tB, 0.4))

    def ui(cr):
        if t < tB - 0.1:
            head(cr, t, "THE MOMENT HE STEPPED", t0 + 0.1, "ON ANGA'S SOIL...", tP)
        else:
            head(cr, t, "THE MOMENT HE STEPPED IN,", tB - 0.1, "THE RAIN CAME!", tB)
    return dict(ui=ui, night=0.22 * clouds, lift=1.0, flash=flash_at(t, tP, 0.2) + flash_at(t, tB, 0.15))


def s_s11(cr, t, tl, t0, t1):
    c = cues(tl, "s11")
    tB, tS, tV = c["B"], c["S"], c["V"]
    prop(cr, "rr_mandap", 960, FL + 8, 0.47, rot=sway(t, 0.003, 0.3))
    ground(cr)
    fire(cr, t, 960, FL, 0.42)
    bless = keyed(t, [(t0, 0.0), (tB, 1.0)], 0.3, 1.3)
    loma(cr, t, 1530, 0.54, flip=True, feet=FL, front=mix((-0.32, -0.55), TEACH, bless), ph=0.6)
    joined = keyed(t, [(t0, 0.0), (tV - 0.1, 1.0)], 0.3, 1.3)
    pb = rishya(cr, t, 720, S, mood="smile" if t > tV else "calm", feet=FL, ph=0.3,
                front=mix((-0.32, -0.55), ANJALI["front"], joined), backa=mix((0.3, -0.25), ANJALI["backa"], joined))
    b, k, a = depth(t, tS - 0.35, 0.45)
    ps = lady(cr, t, C.SHANTA, "c6_shanta", 1200, 0.55 * k, feet=FL, flip=True, mood="smile" if t > tV else None,
              alpha=a, blur=b, front=mix((-0.08, -0.35), ANJALI["front"], joined), ph=0.9)
    for i, p in enumerate((pb, ps)):                       # garlands drop onto both
        if t > tV - 0.3 + 0.15 * i:
            q = back(clamp((t - tV + 0.3 - 0.15 * i) / 0.45), 1.4)
            cx_, cy_ = to_user(cr, p["chest"])
            prop(cr, "kk_garland", cx_ + (8 if i == 0 else -8), cy_ - 90 - 360 * (1 - q), 0.62,
                 rot=0.07 * math.sin(t * 2.3 + i), alpha=clamp(q))
    if t > tV:
        petals(cr, t, tV, 960, 120, n=14, spread=1100, fall=900, dur=2.6, s=1.0)
        lights(cr, t, 960, 600, 260, 9, 0.7 * prog(t, tV, 0.4))
    dev_s = ps.get("top", (1200, 400))

    def ui(cr):
        if t < tV - 0.1:
            head(cr, t, "THE KING'S OWN DAUGHTER,", t0 + 0.1, "PRINCESS SHANTA", tS)
        else:
            head(cr, t, "THEY GOT", tV - 0.1, "MARRIED", tV, under=tV + 0.4)
        tag(cr, t, tS + 0.2, "PRINCESS SHANTA", dev_s[0], dev_s[1] - 40, 30, t_out=tV + 0.6)
    return dict(ui=ui, flash=flash_at(t, tV, 0.18))


S12_FIRE = (790, FL)


def s12_scene(cr, t, c, frozen=False):
    """The yajna: the sage and King Dasharatha kneeling at the fire; then a soft light on the right with baby Rama in
    his cradle. Returns the points the UI needs."""
    tY, tD, tG, tM = c["Y"], c["D"], c["G"], c["M"]
    prop(cr, "arch", 960, FL + 6, 0.5, alpha=0.5, blur=6)
    ground(cr)
    fx, fg = S12_FIRE
    flare = math.exp(-2.0 * max(0.0, t - tG)) * (t > tG)
    fire(cr, t, fx, fg, 0.62 + 0.3 * flare)
    if t > tG:
        burst(cr, t, fx, fg - 220, tG, n=16, rmax=420, alpha=0.6)
    offer = keyed(t, [(c["t0"], 0.0), (tG - 0.2, 1.0)], 0.3, 1.2)
    pr = rishya(cr, t, 480, 0.58, kneel=True, feet=FL, ph=0.3, front=mix(ANJALI["front"], (-1.2, -0.7), offer),
                backa=ANJALI["backa"])
    turn = t > tM + 0.3
    pd = fig(cr, K_DASHA[0], K_DASHA[1], t, 1100, 0.58, kneel="c6_dasha_kneel", feet=FL, flip=not turn,
             front=ANJALI["front"], backa=ANJALI["backa"], head=-0.1 if turn else 0.05, ph=0.8)
    light = prog(t, tM - 0.1, 0.7)
    cx_, cy_ = 1560, FL
    if light > 0.01:
        glow(cr, cx_, cy_ - 200, 520, 0.8 * light)
        warm(cr, cx_, cy_ - 200, 380, 0.8 * light, (1.0, 0.86, 0.55))
        aura(cr, t, cx_, cy_ - 200, 160, 520, 0.45 * light, n=20, spin=0.05)
        b, k, a = depth(t, tM, 0.6)
        prop(cr, "c6_rama_cradle", cx_, cy_ + 4, 0.78 * k, rot=0.03 * math.sin(t * 1.4), alpha=a, blur=b)
        lights(cr, t, cx_, cy_ - 260, 220, 10, 0.8 * light)
    return pr, pd


def _k_dasha():
    import kaikeyi_cast as K
    return K.DASHARATHA, "dasharatha"


K_DASHA = _k_dasha()


def s_s12(cr, t, tl, t0, t1):
    c = cues(tl, "s12")
    tY, tD, tG, tM, tB = c["Y"], c["D"], c["G"], c["M"], c["B"]
    pr, pd = s12_scene(cr, t, c)

    def ui(cr):
        if t < tM - 0.1:
            head(cr, t, "IN THE RAMAYANA, HE LED", t0 + 0.1, "DASHARATHA'S YAJNA", tG)
        else:
            head(cr, t, "AND THEN", tM - 0.1, "RAMA WAS BORN", tB, under=tB + 0.4)
        plaque_text(cr, t, t0 + 0.05, "YEARS LATER...", 960, 300, 38, t_out=tD)
        tag(cr, t, tY + 0.1, "THE SAME SAGE", pr["top"][0] - 20, pr["top"][1] + 30, 30, t_out=tM + 0.2)
        tag(cr, t, tD + 0.1, "KING DASHARATHA", pd["top"][0] + 20, pd["top"][1] - 30, 30, t_out=tM + 0.2)
        tag(cr, t, tB + 0.1, "BABY RAMA", 1560, 470, 36)
    return dict(ui=ui, flash=flash_at(t, tG, 0.15) + flash_at(t, tM, 0.2))


def s_s13(cr, t, tl, t0, t1):
    c = cues(tl, "s13")
    tJ, tN, tR = c["J"], c["N"], c["R"]
    t_chain = t0 + 0.9
    fz = 1 - prog(t, t_chain, 0.4)
    if fz > 0.01:                                          # the yajna frozen in sepia
        c12 = cues(tl, "s12")
        cr.push_group()
        pc_scene = s12_scene(cr, t0 - 0.05, c12, frozen=True)  # noqa: F841
        sepia(cr, 1.0)
        cr.pop_group_to_source()
        cr.paint_with_alpha(fz)
    xs = (210, 480, 750, 1020, 1290)
    y = 620
    r = 108
    dark = [prog(t, tN + 0.25 * i, 0.3) if t > tN else 0.0 for i in range(6)]

    def m_boy(cr_):
        prop(cr_, "c6_rishya_head", xs[0] - 6, y + 66, 0.56)

    def m_rain(cr_):
        prop(cr_, "cloud", xs[1], y - 36, 0.3)
        rain(cr_, t, 1.0, x0=xs[1] - 70, x1=xs[1] + 80, y0=y - 4, y1=y + 90, n=22)

    def m_wed(cr_):
        prop(cr_, "kk_garland", xs[2], y - 90, 0.55)

    def m_fire(cr_):
        fire(cr_, t, xs[3], y + 70, 0.32)

    def m_rama(cr_):
        prop(cr_, "c6_rama_cradle", xs[4] + 20, y + 80, 0.32)
    fns = (m_boy, m_rain, m_wed, m_fire, m_rama)
    labels = ("FOREST BOY", "RAIN", "WEDDING", "YAJNA", "RAMA")
    if t > t_chain - 0.2:
        for i, (x, fn, lb) in enumerate(zip(xs, fns, labels)):
            ti = t_chain + 0.22 * i
            medallion(cr, t, ti, x, y, r, fn, lb, dim=dark[i] if i > 0 else 0.0)
            if i < 4:
                arrow2(cr, (x + r + 18, y), (xs[i + 1] - r - 18, y), prog(t, ti + 0.15, 0.25), False, 9,
                       alpha=1 - 0.7 * dark[i + 1])
        arrow2(cr, (xs[4] + r + 18, y), (1450, y), prog(t, t_chain + 1.1, 0.25), False, 9, alpha=1 - 0.7 * dark[5])
        bt = t_chain + 1.2
        if t > bt:                                         # the Ramayana: a palm-leaf book under its name plaque
            b, k, a = depth(t, bt, 0.45)
            a *= 1 - 0.6 * dark[5]
            prop(cr, "c6_veda", 1640, y + 70, 1.75 * k, rot=sway(t, 0.008, 0.4), alpha=a, blur=b)
            card(cr, t, bt, 1640, y - 50, 0.42, [("RAMAYANA", 120, INK, 4)], alpha=1 - 0.6 * dark[5])

    t_sw = max(tN - 0.1, tJ + 0.8)                     # the question stays up at least 0.8 s (Kannada says it fast)

    def ui(cr):
        if t < t_sw:
            head(cr, t, "WHAT IF HE", t0 + 0.2, "NEVER LEFT THE FOREST?", tJ)
        else:
            head(cr, t, "NO FOREST BOY...", t_sw, "NO RAMAYANA?", tR)
        if t > tN:
            big_x(cr, xs[0], y, 2 * r + 20, 2 * r + 20, prog(t, tN, 0.35), lw=22)
        if t > tR - 0.1:
            big_q(cr, t, tR, 1640, 380, 200)
    return dict(ui=ui, flash=flash_at(t, tR, 0.12))


# ------------------------------------------------------------------ frame


SHOTS = [   # (line, draw function, options)
    ("g1", s_g1, {"z": (1.0, 1.03)}),
    ("g2", s_g2, {"z": (1.0, 1.04)}),
    ("g3", s_g3, {"z": (1.02, 1.0), "focus": (960, 700)}),
    ("g4", s_g4, {"z": (1.0, 1.03)}),
    ("g5", s_g5, {"z": (1.0, 1.03), "focus": (900, 700)}),
    ("g6", s_g6, {"z": (1.0, 1.03), "focus": (960, 800)}),
    ("g7", s_g7, {"z": (1.0, 1.03)}),
    ("g8", s_g8, {"z": (1.0, 1.04), "focus": (700, 700)}),
    ("g9", s_g9, {"z": (1.0, 1.02)}),
    ("g10", s_g10, {"z": (1.0, 1.03)}),
    ("g11", s_g11, {"z": (1.0, 1.03), "focus": (960, 700)}),
    ("s1", s_s1, {"z": (1.0, 1.03)}),
    ("s2", s_s2, {"z": (1.0, 1.04), "focus": (760, 500)}),
    ("s3", s_s3, {"z": (1.0, 1.03)}),
    ("s4", s_s4, {"z": (1.0, 1.03)}),
    ("s5", s_s5, {"z": (1.0, 1.03)}),
    ("s6", s_s6, {"z": (1.0, 1.02)}),
    ("s7", s_s7, {"z": (1.0, 1.03)}),
    ("s8", s_s8, {"z": (1.0, 1.04), "focus": (900, 600)}),
    ("s9", s_s9, {"z": (1.0, 1.02)}),
    ("s10", s_s10, {"z": (1.0, 1.03)}),
    ("s11", s_s11, {"z": (1.0, 1.03)}),
    ("s12", s_s12, {"z": (1.0, 1.03)}),
    ("s13", s_s13, {"z": (1.0, 1.0)}),
]


def shot_at(t, tl):
    """(index, start, end) of the shot showing at t: each shot runs from its line's start to the next line's start
    (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_s6c_spans", None)
    if cache is None:
        cache = [(T(tl, bid), line_end(tl, bid)) for bid, _, _ in SHOTS]
        tl._s6c_spans = cache
    k = 0
    for i, (s, _) in enumerate(cache):
        if t >= s:
            k = i
    return k, cache[k][0], cache[k][1]


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl)
    _, fn, opt = SHOTS[k]
    z0, z1 = opt.get("z", (1.0, 1.03))
    z = z0 + (z1 - z0) * clamp((t - t0) / max(0.5, t1 - t0))
    fx, fy = opt.get("focus", (960, 620))
    cr.save()
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    C.screen(cr)
    out = fn(cr, t, tl, t0, t1) or {}
    tint(cr, (1.0, 0.66, 0.42), out.get("eve", 0.0))
    tint(cr, (0.36, 0.42, 0.72), out.get("blue", 0.0))     # moonlight / deep-sea gloom
    if out.get("post"):                                    # lights that stay bright in the dark (lamps, eyes)
        out["post"](cr)
    cr.restore()
    motes(cr, t)
    C.lamp(cr, t, night=out.get("night", 0.0), flash=out.get("flash", 0.0))
    sepia(cr, out.get("sepia", 0.0))
    C.title_lift(cr, out.get("lift", 0.0) * out.get("night", 0.0) / NIGHT)
    if out.get("ui"):
        out["ui"](cr)
    if t - t0 < 0.22:                                      # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur) for lines g* and s* only, sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a
    damaru on each chapter card, a conch as Agastya drinks the ocean, shimmer as Ganga comes down, shimmer as the rain
    comes, a bell as Rama is born, then (only where they fit) a hit on the vajra's flash. Chosen in THAT order, each
    at least SFX_MIN_GAP from every sound already kept; the bed dips before the reveals."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(c["g1"]["t0"], "damaru", 0), (c["s1"]["t0"], "damaru", 0), (c["g5"]["D"], "conch", 0),
            (c["g11"]["G"], "shimmer", 0), (c["s10"]["B"], "shimmer", 0), (c["s12"]["M"], "bell", 0),
            (c["g6"]["H"] + 0.15, "hit", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["g5"]["D"] - 0.35, "dip", 0.5), (c["g8"]["P"] - 0.3, "dip", 0.45), (c["g11"]["P"] - 0.3, "dip", 0.5),
            (c["s8"]["S"] - 0.3, "dip", 0.45), (c["s10"]["B"] - 0.35, "dip", 0.5), (c["s12"]["M"] - 0.3, "dip", 0.5),
            (c["s13"]["R"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
