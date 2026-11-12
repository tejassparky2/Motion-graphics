"""Scenes for long video 2 (videos/yamlok_yatra.py, landscape 1920x1080), builder B's parts: the road (w1-w7), the
sixteen cities (c1-c9), the Vaitarani (v1-v10) and the cold city (s1-s5). scenes_yamlok_yatra routes every moment
whose active line is w*, c*, v* or s* here.

Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code, the same wide lamp-lit cloth, two-tier
headlines (small dark setup line + one big red key line) and chapter cards as long video 1 (scenes_six_b). Seth
Dhaniram is yy_cast's little soul: the hand-sized body made of the rice-balls (solid=1) until s4, where it falls
away like an empty shell and the thumb-sized soul of light (solid=0) goes on. The two Yamadutas are garuda_cast's
messengers; one walks behind him holding the noose round his neck, the other carries the staff. The fishermen are
dharmavyadha_cast's husband puppet (garuda_cast's boatman, with its bamboo pole) and hunter puppet; the townsfolk are
dharmavyadha_cast's two fathers, soft in the background. Bhola (c9) is yy_cast's, drawn only as a figure of dots: he
is not on this road. New faces and props are in yb_cast. Speech clouds are painted opaque so they read over the dark
river.

THE ROAD MAP. A child always knows where he is: in w1-w2 the whole road is a big map (home at the near end, sixteen
city gates, the dark-red Vaitarani half-way, Yama's city far off); at the end of w2 it folds down into a palm-leaf
strip along the bottom of the frame that stays for the whole journey: the winding road, sixteen city dots (lit when
reached), the river, Yama's city, a tiny Dhaniram walking along it, and a DAY / MONTH counter at its left end
(DAY 13 ... DAY 18, MONTH 1 ... MONTH 12, 1 YEAR).

Respect and calm: no gore anywhere. The Vaitarani is dark-red water with crocodile backs and circling vultures (the
on-screen words say NOT WATER, never blood); "like a fish on a hook" is Dhaniram dangling from the rope under the
flying messengers (no hook through anything); thorns, hot sand and the sword-leaves only make him hop and duck;
stones fall like hail around him and never hit; the king who looks like Death is a gaunt dark king (no skull); the
hand-sized body falls away as an empty shell.

Every frame is a pure function of t. Cues are words of the Hindi line (CUES, fraction fallbacks, minimum gaps; MISSES
stays empty when every word is found). Shot spans and cues are cached on the timeline under this module's own names
(_yb_spans, _yb_cues, _yb_jour).

Shot list (line: what is on the screen)
  w1  chapter card DAY 13 / THE ROAD / 86,000 YOJANAS / GARUDA PURANA · PRETA KALPA; it flies up and the big map draws
      itself: home (HOME) at the near left, the road winding back and forth up to the far right, sixteen city gates
      popping in, the dark-red river half-way, Yama's city glowing at the far end (YAMA'S CITY), badge 16 CITIES: THE
      ROAD TO YAMA'S CITY: / 86,000 YOJANAS
  w2  the map: little Dhaniram starts walking from home along a dotted trail; badge 247 YOJANAS EVERY DAY: EVERY DAY
      HE MUST WALK / 247 YOJANAS; the sun crosses the sky and sets, the moon and stars come out (night): NO REST: /
      DAY AND NIGHT; the big map shrinks down into the road-map strip at the bottom
  w3  close: Dhaniram counting on his fingers (the numbers pop from his fingertip), a sum card: 1 YOJANA ≈ 13 KM,
      247 YOJANAS ≈ 3,200 KM: DHANIRAM DID THE MATHS ON HIS FINGERS / 247 × 13 KM = ?; his eyes pop (shocked, he
      jumps, sweat flies): THAT'S... / THOUSANDS OF KM. EVERY DAY! (stamp EVERY DAY!)
  w4  the dry road scrolling past, the messengers and Dhaniram walking; three crossed-out icons: no shade (a tree),
      no food (a bowl), no water (a pot): ON THE ROAD: / NO SHADE, NO FOOD, NO WATER; twelve suns pop into the sky one
      by one in a row, heat shimmer, Dhaniram shades his eyes: AND IN THE SKY... / 12 SUNS!
  w5  on each word the ground changes round them: thorn bushes rise (he hops, THORNS), hot sand with steam (he hops
      foot to foot, HOT SAND), then tall sword-shaped leaves (they all duck through, SWORD-LEAF FOREST): ON THE WAY: /
      THORNS... HOT SAND..., THORNS... HOT SAND... AND A / SWORD-LEAF FOREST
  w6  Dhaniram falls flat (dust), gets up, falls again: DHANIRAM... / FELL! / FELL... GOT UP... / FELL... GOT UP...
      FELL!; the messenger behind him shouts (cloud KEEP / WALKING!)
  w7  they walk on; DAY 14 ... DAY 17 tick past (badge), then DAY 18 (ringed): AFTER 17 DAYS OF WALKING, / ON DAY 18;
      the first city gate rises ahead (glow), its name plate SAUMYA NAGAR, the strip's first dot lights: THE FIRST
      CITY
  c1  chapter card DAY 18 / THE 16 CITIES; then a pretty blue river with lotuses and a great banyan; Dhaniram sits
      under it and weeps (tears), three thought bubbles pop: his safe, his house, his son: A PRETTY RIVER, AND A /
      BANYAN TREE, HE SAT DOWN AND CRIED: / MY SAFE! MY HOUSE! MY SON!
  c2  two townsfolk come up behind the messengers; all laugh and point (HA HA): cloud WHERE IS YOUR / WEALTH NOW?
      (the safe and house bubbles pop), WHERE ARE / YOUR SONS? (the son bubble pops): THE TOWNSFOLK AND THE MESSENGERS
      LAUGHED:, HERE, ONLY / YOUR KARMA WORKS
  c3  the road again; a card: food on a leaf and a water pot (FOOD FOR THE JOURNEY, a green tick, EVEN KIDS KNOW!):
      ON A JOURNEY, YOU CARRY / FOOD; a market stall with coins, crossed out: BUT ON THIS ROAD: / NO BUYING. NO SELLING.
  c4  Dhaniram alone, close, a hand at his chin, head bowed; a thought cloud: a gold coin slides along a dotted arc
      into an empty bowl (the gift he never gave): FOR THE FIRST TIME, DHANIRAM THOUGHT: / IF ONLY I HAD GIVEN...
  c5  the road, home far behind on the left; rice-balls fly from home (FROM HOME) along a dotted arc like little
      parcels of light; he catches each and glows; MONTH 1, MONTH 2: ALL HE HAD TO EAT: / RICE-BALLS, OFFERED AT HOME /
      EVERY MONTH
  c6  the next city, dark; a tall gaunt dark king in a cold light steps out over Dhaniram: THE NEXT CITY'S KING
      LOOKED LIKE / DEATH; Dhaniram shakes and collapses to the ground: ONE LOOK, AND DHANIRAM / GAVE UP
  c7  MONTH 4 (badge); stones fall like hail from the sky, each landing just where he stood a moment ago: Dhaniram
      hops left and right, hands over his head (comic), the messengers don't even blink: MONTH 4: / IT RAINED STONES!
  c8  they walk on past city gates, MONTH 4 -> MONTH 5; then three framed panels pop in one after another: CRYING
      EVERYWHERE (a city, sound rings, Dhaniram weeping), SCORCHING HEAT (a blazing sun, heat waves), CLOUDS,
      CLOUDS (dark clouds, rain): MONTHS PASSED... / CITY AFTER CITY
  c9  an empty road; a dotted outline of Bhola with his water pot, a big red ?: AND BHOLA? / WHERE WAS HE?; the
      outline flickers: NOT A TRACE OF HIM / ON THIS ROAD
  v1  MONTH 6 (badge); a strange city of twisted, coloured towers; a big stern king (tag KING VICHITRA) towers over
      the bowing Dhaniram: MONTH 6: A STRANGE CITY / ITS KING: VICHITRA; plate YAMA'S YOUNGER BROTHER: VICHITRA WAS /
      YAMA'S YOUNGER BROTHER
  v2  the river comes up behind them; the chapter card MONTH 6 / THE VAITARANI rises as the river is named (the river
      dims behind it while it is up)
  v3  the wide dark-red river (whirlpools), Dhaniram and the messengers small on the near bank; a width arrow
      100 YOJANAS; plate NOT WATER...: 100 YOJANAS WIDE... / A RIVER OF DARK RED; crocodile backs surface, vultures
      circle: BELOW, CROCODILES... / ABOVE, VULTURES!
  v4  the near bank: fishermen with a boat at the edge (the boatman with his pole in it, one on the bank): ON THE
      BANK, SOME FISHERMEN / WITH A BOAT; cloud WANT TO / CROSS?
  v5  Dhaniram, delighted, steps up rubbing his fingers, little dotted coins glinting over his hand: DHANIRAM WAS
      THRILLED: / HOW MUCH?; cloud YES, YES! / HOW MUCH?
  v6  the fisherman shakes his head; the dotted coins are crossed out: THE FISHERMEN SAID: / MONEY DOESN'T WORK HERE;
      a card: GAVE A COW? -> BOAT (tick), NO COW? -> NO BOAT (cross): ONLY ONE THING WORKS HERE: / A GIFTED COW
  v7  a big word card: वैतरणी = ? (a big red ?), then वितरण = GIVING, then the ? becomes CROSSED BY GIVING (ringed):
      WHAT DOES THE NAME MEAN?
  v8  Dhaniram, close, a hand on his head, the other flung out; a gift-calf medallion crossed out (A GIFT CALF): IN
      HIS WHOLE LIFE HE NEVER GAVE / EVEN A CALF!; cloud हाय राम!
  v9  the river boils: bubbles rise and burst everywhere, steam; Dhaniram jumps back; inset: a kadhai of ghee
      bubbling (GHEE IN A KADHAI): THE RIVER STARTED TO / BOIL!, LIKE / GHEE IN A HOT PAN!
  v10 the two messengers fly over the river, Dhaniram dangling below on the rope, kicking (inset: a fish on a line,
      A FISH ON A LINE); the far bank slides in and they land, Dhaniram dizzy: THE MESSENGERS HUNG HIM / LIKE A FISH
      ON A LINE, AND FLEW HIM / ACROSS THE RIVER
  s1  chapter card MONTH 12 / THE CITY OF COLD; then snow, ice peaks, frost; Dhaniram shivering; the month counter
      rolls to 12; a small Himalaya card stamped × 100: MONTH 12: / THE CITY OF COLD, IT WAS / 100 × COLDER THAN THE
      HIMALAYA
  s2  shivering, Dhaniram looks left and right; ten little arrows ring him, each with a ?: SHIVERING, HE LOOKED IN /
      ALL 10 DIRECTIONS; HE CRIED OUT: + cloud ANYONE? / SAVE ME!
  s3  the messengers step up (cloud WHAT MERIT / DO YOU HAVE?, plate MERIT = GOOD DEEDS); Dhaniram holds out his
      empty hands (ringed): THE MESSENGERS ASKED:, AND DHANIRAM HAD / NO ANSWER
  s4  the last city: the hand-sized body stops; a burst of light, the small thumb-sized soul of light rises out of it
      and lands in front; the body is left an empty shell (a figure of dots, EMPTY SHELL) that slumps and crumbles to
      dust; the soul (tag THUMB-SIZED SOUL) walks on with the messengers: IN THE LAST CITY... / THE HAND-SIZED BODY /
      FELL AWAY, AND THE THUMB-SIZED SOUL / WENT ON
  s5  dawn-dark; Yama's city fills the horizon, its gate glowing; the soul and the messengers walk toward it; 1 YEAR
      (badge), the strip's marker reaches the end: AFTER 1 YEAR, AT LAST... / YAMA'S CITY
"""
import bisect
import functools
import math

import cairo

import dharmavyadha_cast as DV
import garuda_cast as GC
import puppet_core as pc
import six_cast_c  # noqa: F401  (registers the rock and the fish)
import yb_cast as YB
import yy_cast as YC
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import MONO_FONT, back, clamp, draw_text, ease, prog, text_size
from puppet_core import H, W, prop, sway
from scenes_arjuna import HAS_INDIC, indic_surface
from scenes_garuda_purana import pinda
from scenes_hanuman_curse import qmark
from scenes_jarasandha import INK, RED, glow, motes, red_ring, stars, walk_legs
from scenes_jayadratha import fit_size, flash_at, tag, tint
from scenes_lakshman_rekha import big_x, sparkle
from scenes_mandhata import aura, burst, held, lights, mix, warm
from scenes_ravana import dotted
from scenes_ruru import held_grip, plate
from scenes_six_b import FL, body, body_outline, chapter, counter_badge, head2, lamp, stage, title_lift
from shots import T


MISSES = set()                       # cue words not found in a line (falls back to fractions)
SOURCE = "GARUDA PURANA · PRETA KALPA"
GREEN_TICK = (0.16, 0.50, 0.24)
FADE = (0.42, 0.34, 0.26)
PARCH = (0.97, 0.87, 0.62)
DU_S = 0.54                          # the messengers' scale on the road
DH_H = 250                           # the hand-sized soul body's height (soles to pagdi top), px
HAND = 1.0                           # solid: the hand-sized body
WORD = {"vitaran": "वितरण", "vaitarani": "वैतरणी", "hairam": "हाय राम!"}


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
    "w1": (("R", "रास्ता", 0.4, (("t0", 0.4),)),
           ("N", "छियासी", 0.55, (("R", 0.3),)),
           ("Y", "योजन", 0.8, (("N", 0.4),))),
    "w2": (("R", "रोज़", 0.12, (("t0", 0.2),)),
           ("N", "सैंतालीस", 0.4, (("R", 0.4),)),
           ("D", "दिन", 0.68, (("N", 0.6),)),
           ("Rt", "रात", 0.88, (("D", 0.4),))),
    "w3": (("U", "उँगलियों", 0.15, (("t0", 0.3),)),
           ("H", "हिसाब", 0.3, (("U", 0.5),)),
           ("O", "होश", 0.5, (("H", 0.9),)),
           ("K", "हज़ारों", 0.78, (("O", 0.8),)),
           ("M", "किलोमीटर", 0.88, (("K", 0.3),))),
    "w4": (("C", "छाँव", 0.2, (("t0", 0.4),)),
           ("K", "खाना", 0.3, (("C", 0.35),)),
           ("P", "पानी", 0.4, (("K", 0.35),)),
           ("A", "आसमान", 0.6, (("P", 0.6),)),
           ("B", "बारह", 0.72, (("A", 0.4),)),
           ("S", "सूरज", 0.8, (("B", 0.25),))),
    "w5": (("K", "काँटे", 0.12, (("t0", 0.2),)),
           ("R", "रेत", 0.35, (("K", 0.8),)),
           ("T", "तलवार", 0.55, (("R", 0.8),)),
           ("J", "जंगल", 0.9, (("T", 0.5),))),
    "w6": (("G1", "गिरता", 0.12, (("t0", 0.2),)),
           ("U", "उठता", 0.28, (("G1", 0.6),)),
           ("G2", "फिर", 0.38, (("U", 0.5),)),
           ("D", "दूत", 0.6, (("G2", 0.5),)),
           ("C", "चलता", 0.85, (("D", 0.4),))),
    "w7": (("S", "सत्रह", 0.1, (("t0", 0.2),)),
           ("A", "अठारहवें", 0.45, (("S", 1.0),)),
           ("P", "पहला", 0.65, (("A", 0.5),)),
           ("N", "सौम्य", 0.85, (("P", 0.5),))),
    "c1": (("N", "नदी", 0.12, (("t0", 0.4),)),
           ("B", "बरगद", 0.25, (("N", 0.4),)),
           ("Bt", "बैठकर", 0.45, (("B", 0.6),)),
           ("R", "रोने", 0.55, (("Bt", 0.3),)),
           ("Tj", "तिजोरी", 0.68, (("R", 0.4),)),
           ("G", "घर", 0.8, (("Tj", 0.5),)),
           ("Bk", "बेटा", 0.93, (("G", 0.5),))),
    "c2": (("L", "लोग", 0.1, (("t0", 0.2),)),
           ("D", "धन", 0.35, (("L", 0.8),)),
           ("B", "बेटे", 0.55, (("D", 0.8),)),
           ("Y", "यहाँ", 0.7, (("B", 0.5),)),
           ("K", "कर्म", 0.85, (("Y", 0.4),))),
    "c3": (("K", "खाना", 0.1, (("t0", 0.2),)),
           ("Bc", "बच्चे", 0.32, (("K", 0.8),)),
           ("R", "रास्ते", 0.55, (("Bc", 0.8),)),
           ("Kh", "ख़रीदा", 0.7, (("R", 0.4),)),
           ("Bh", "बेचा", 0.88, (("Kh", 0.4),))),
    "c4": (("P", "पहली", 0.2, (("t0", 0.3),)),
           ("K", "काश", 0.45, (("P", 0.6),)),
           ("D", "दान", 0.85, (("K", 0.8),))),
    "c5": (("P", "पिंडों", 0.35, (("t0", 0.6),)),
           ("G", "घर", 0.6, (("P", 0.5),)),
           ("M", "महीने", 0.8, (("G", 0.4),))),
    "c6": (("N", "नगर", 0.1, (("t0", 0.2),)),
           ("M", "मौत", 0.22, (("N", 0.3),)),
           ("R", "राजा", 0.45, (("M", 0.6),)),
           ("D", "देखते", 0.62, (("R", 0.5),)),
           ("H", "हिम्मत", 0.8, (("D", 0.5),))),
    "c7": (("C", "चौथे", 0.05, (("t0", 0.0),)),
           ("A", "आसमान", 0.55, (("C", 0.8),)),
           ("P", "पत्थर", 0.75, (("A", 0.3),))),
    "c8": (("B", "बीतते", 0.08, (("t0", 0.2),)),
           ("N", "आते", 0.22, (("B", 0.5),)),
           ("R", "रोने", 0.45, (("N", 0.8),)),
           ("T", "तपती", 0.68, (("R", 1.2),)),
           ("Bd", "बादल", 0.88, (("T", 1.0),))),
    "c9": (("B", "भोला", 0.08, (("t0", 0.2),)),
           ("K", "कहाँ", 0.25, (("B", 0.4),)),
           ("R", "रास्ते", 0.5, (("K", 0.6),)),
           ("N", "नामो", 0.75, (("R", 0.5),))),
    "v1": (("C", "छठे", 0.03, (("t0", 0.0),)),
           ("A", "अजीब", 0.3, (("C", 0.6),)),
           ("R", "राजा", 0.5, (("A", 0.6),)),
           ("V", "विचित्र", 0.6, (("R", 0.3),)),
           ("Y", "यमराज", 0.75, (("V", 0.5),)),
           ("B", "भाई", 0.92, (("Y", 0.4),))),
    "v2": (("B", "बहती", 0.5, (("t0", 0.4),)),
           ("V", "वैतरणी", 0.75, (("B", 0.3),))),
    "v3": (("S", "सौ", 0.05, (("t0", 0.0),)),
           ("C", "चौड़ी", 0.15, (("S", 0.3),)),
           ("P", "पानी", 0.3, (("C", 0.5),)),
           ("K", "ख़ून", 0.45, (("P", 0.4),)),
           ("M", "मगरमच्छ", 0.7, (("K", 0.6),)),
           ("G", "गिद्ध", 0.92, (("M", 0.6),))),
    "v4": (("M", "मछुआरे", 0.25, (("t0", 0.4),)),
           ("N", "नाव", 0.42, (("M", 0.4),)),
           ("B", "बोले", 0.7, (("N", 0.6),)),
           ("P", "पार", 0.85, (("B", 0.3),))),
    "v5": (("K", "ख़ुश", 0.3, (("t0", 0.4),)),
           ("H", "हाँ", 0.55, (("K", 0.3),)),
           ("P", "पैसे", 0.88, (("H", 0.6),))),
    "v6": (("P", "पैसे", 0.2, (("t0", 0.4),)),
           ("N", "चलते", 0.32, (("P", 0.3),)),
           ("G", "गाय", 0.55, (("N", 0.8),)),
           ("Nv", "नाव", 0.75, (("G", 0.6),)),
           ("V", "वरना", 0.9, (("Nv", 0.5),))),
    "v7": (("V", "वैतरणी", 0.02, (("t0", 0.0),)),
           ("Vt", "वितरण", 0.4, (("V", 0.8),)),
           ("D", "दान", 0.55, (("Vt", 0.5),)),
           ("P", "पार", 0.78, (("D", 0.6),)),
           ("V2", "वो", 0.9, (("P", 0.4),))),
    "v8": (("B", "बछड़ा", 0.35, (("t0", 0.6),)),
           ("N", "नहीं", 0.55, (("B", 0.4),)),
           ("H", "हाय", 0.85, (("N", 0.8),))),
    "v9": (("U", "उबलने", 0.4, (("t0", 0.5),)),
           ("K", "कढ़ाई", 0.75, (("U", 0.6),)),
           ("G", "घी", 0.92, (("K", 0.3),))),
    "v10": (("D", "दूत", 0.1, (("t0", 0.2),)),
            ("M", "मछली", 0.35, (("D", 0.6),)),
            ("L", "लटकाकर", 0.5, (("M", 0.4),)),
            ("U", "उड़ते", 0.65, (("L", 0.4),)),
            ("P", "पार", 0.88, (("U", 0.6),))),
    "s1": (("S", "शीत", 0.3, (("t0", 0.6),)),
           ("T", "ठंड", 0.5, (("S", 0.5),)),
           ("Hm", "हिमालय", 0.65, (("T", 0.4),)),
           ("G", "गुना", 0.85, (("Hm", 0.4),))),
    "s2": (("K", "काँपता", 0.05, (("t0", 0.0),)),
           ("D", "दसों", 0.35, (("K", 0.8),)),
           ("A", "अपना", 0.7, (("D", 1.0),)),
           ("B", "बचा", 0.9, (("A", 0.4),))),
    "s3": (("P", "पूछा", 0.15, (("t0", 0.3),)),
           ("Pn", "पुण्य", 0.45, (("P", 0.6),)),
           ("J", "जवाब", 0.85, (("Pn", 1.0),))),
    "s4": (("A", "आख़िरी", 0.05, (("t0", 0.0),)),
           ("H", "हाथ", 0.3, (("A", 0.6),)),
           ("C", "छूट", 0.55, (("H", 0.6),)),
           ("Ag", "अंगूठे", 0.7, (("C", 0.8),)),
           ("B", "बढ़ी", 0.92, (("Ag", 0.6),))),
    "s5": (("S", "साल", 0.15, (("t0", 0.2),)),
           ("A", "आख़िरकार", 0.35, (("S", 0.4),)),
           ("Y", "यमराज", 0.75, (("A", 0.6),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_yb_cues", None)
    if cache is None:
        cache = {}
        tl._yb_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, word, frac, cons in CUES[bid]:
            v = cue(tl, bid, word, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


def to_user(cr, p):
    return cr.device_to_user(*p)


def pop(t, t_in, dur=0.3, k=1.6):
    """0 before t_in, an overshooting 0..1 after."""
    return back(clamp((t - t_in) / dur), k) if t > t_in else 0.0


@functools.lru_cache(maxsize=32)
def indic(text, size, color):
    return indic_surface(text, size, color)


# ------------------------------------------------------------------ Dhaniram's soul (yy_cast) and the messengers


def dh(cr, t, x, feet, h=DH_H, mood="calm", solid=HAND, **kw):
    """Dhaniram's soul (yy_cast.soul): h px tall from his soles at (x, feet); solid 1 = the hand-sized body (a faint
    glow), 0 = the thumb-sized soul of light. Returns its points (device xy)."""
    kw.setdefault("glow", 0.5 if solid >= 0.5 else 1.0)
    return YC.soul(cr, t, x, feet, h, mood=mood, solid=solid, **kw) or {}


def cloud_text(cr, t, x, y, s, lines, flip=False, alpha=1.0, t_in=None):
    """scenes_arjuna.cloud_text (lrekha_cast's speech cloud popping in at t_in, lines = [(text, size, colour, dy,
    t_show)]), with the cloud painted opaque so it reads over the dark river and the night as well."""
    q = back(clamp((t - t_in) / 0.3), 1.6) if t_in is not None else 1.0
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    sc = s * (0.6 + 0.4 * q)
    cr.save()
    cr.translate(x, y)
    cr.rotate(sway(t, 0.008, 0.5))
    cr.scale(-sc if flip else sc, sc)
    pc.paint_part(cr, "lr_scloud", a, 0.0, cairo.OPERATOR_OVER)
    cr.restore()
    for txt, sz, col, dy, ts in lines:
        p = prog(t, ts, 0.25) * a
        if p > 0:
            sz2 = min(sz, fit_size(txt, sz, 520 * s / 0.8))
            k = 1.15 - 0.15 * back(clamp((t - ts) / 0.3))
            cr.save()
            cr.translate(x, y + dy)
            cr.scale(k, k)
            draw_text(cr, txt, 0, 0, sz2, col, p, anchor="cm")
            cr.restore()


def neck_of(cr, pts):
    """Where the noose sits on Dhaniram (scene xy), from his points (device)."""
    if "chest" not in pts or "head" not in pts:
        return None
    c, hd = to_user(cr, pts["chest"]), to_user(cr, pts["head"])
    return c[0] + 0.45 * (hd[0] - c[0]), c[1] + 0.45 * (hd[1] - c[1])


def duta(cr, t, x, s=DU_S, feet=FL, flip=False, front=(-0.4, -0.5), backa=(0.3, -0.3), hold="staff", mood=None,
         head=0.0, legs=(0.0, 0.0), rot=0.0, alpha=1.0, blur=0.0, hits=(), ph=0.0, y=None, tilt=0.0, rods=True):
    """A Yamaduta (garuda_cast), facing right unless flip; hold = staff | noose | None; mood None | laugh | scold."""
    ex = {}
    if hold == "staff":
        ex["gp_duta_armF_lo"] = held_grip("gp_dstaff", front, 0.6, tilt, 40, alpha, blur)
    elif hold == "noose":
        ex["gp_duta_armF_lo"] = held("gp_noose", front, 0.5, 150, 0.0, alpha, blur)
    sw = {"gp_duta_head": "yb_duta_head_" + mood} if mood else None
    return body(cr, GC.DUTA, "gp_duta", t, x, s, front=front, backa=backa, head=head, legs=legs, hits=hits, flip=flip,
                alpha=alpha, blur=blur, feet=feet, ph=ph, extra=ex, swap=sw, rot=rot, y=y, rods=rods)


def rope_to(cr, p0, p1, sag=40.0, w=7.0, loop=None, alpha=1.0):
    """The noose's rope from p0 (a messenger's hand) to p1 (Dhaniram's neck), sagging; loop = (rx, ry) draws the loop
    round his neck."""
    if alpha <= 0.01 or p0 is None or p1 is None:
        return
    mx, my = (p0[0] + p1[0]) / 2, max(p0[1], p1[1]) + sag
    pts = [((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * mx + u * u * p1[0],
            (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * my + u * u * p1[1]) for u in (i / 10 for i in range(11))]
    cr.save()
    if alpha < 1:
        cr.push_group()
    GC.rope(cr, pts, w)
    if loop:
        rx, ry = loop
        GC.rope(cr, [(p1[0] + rx * math.cos(a), p1[1] + ry * math.sin(a))
                     for a in (2 * math.pi * i / 16 for i in range(17))], w * 0.8)
    if alpha < 1:
        cr.pop_group_to_source()
        cr.paint_with_alpha(alpha)
    cr.restore()


def walk_cycle(t, step=0.42, ph=0.0, amp=1.0):
    """Walking in place (the ground scrolls past): (bob_y, rock, leg phase)."""
    u = (t + ph) / step
    k = int(math.floor(u))
    f = u - k
    bob = -abs(math.sin(math.pi * f)) * 14 * amp
    rock = 0.04 * amp * math.sin(math.pi * f) * (1 if k % 2 else -1)
    return bob, rock, (1 if k % 2 else -1) * math.sin(math.pi * f) * amp


def trio(cr, t, x, walk=1.0, s=DU_S, h=DH_H, gap=270, dmood="sheepish", dkw=None, d1=None, d2=None, rope=1.0,
         alpha=1.0, feet=FL, show2=True):
    """Dhaniram walking in front (at x), a messenger behind him holding the noose round his neck (x - gap), the second
    messenger with the staff behind him (x - 2 gap), all facing right, walking in place when walk > 0. Returns the
    points {"dh": ..., "d1": ..., "d2": ...} (device)."""
    out = {}
    if show2:
        bob, rock, lp = walk_cycle(t, 0.46, 0.21, walk)
        kw = dict(front=(-0.45, -0.35), backa=(0.35, -0.3), legs=walk_legs(lp, 0.3), rot=rock,
                  y=feet - 434 * s + bob, ph=0.7, alpha=alpha)
        kw.update(d2 or {})
        out["d2"] = duta(cr, t, x - 2 * gap, s, hold="staff", **kw)
    bob, rock, lp = walk_cycle(t, 0.44, 0.0, walk)
    kw = dict(front=(-1.25, -0.25), backa=(0.35, -0.3), legs=walk_legs(lp, 0.3), rot=rock, y=feet - 434 * s + bob,
              ph=0.2, hold=None, alpha=alpha)
    kw.update(d1 or {})
    out["d1"] = duta(cr, t, x - gap, s, **kw)
    bob, rock, lp = walk_cycle(t, 0.36, 0.1, walk)
    kd = dict(front=(-0.25, -0.35), backa=(0.35, -0.4), legs=walk_legs(lp, 0.42), rot=rock * 1.5, alpha=alpha)
    kd.update(dkw or {})
    fy = kd.pop("feet", feet) + bob * 0.8
    out["dh"] = dh(cr, t, x, fy, h, mood=dmood, **kd)
    if rope > 0.01:
        hand = to_user(cr, out["d1"]["handF"]) if "handF" in out["d1"] else None
        rope_to(cr, hand, neck_of(cr, out["dh"]), sag=50, w=6, loop=(0.05 * h, 0.022 * h), alpha=rope * alpha)
    return out


def jang(cr, t, x, s, front=(-0.4, -0.5), backa=(0.3, -0.3), **kw):
    """King Jangama, who looks like Death (yb_cast)."""
    return body(cr, YB.JANG, "yb_jang", t, x, s, front=front, backa=backa, **kw)


def vich(cr, t, x, s, mood="angry", front=(-0.4, -0.5), backa=(0.3, -0.3), **kw):
    """King Vichitra, Yama's younger brother (yb_cast)."""
    sw = {"yb_vich_head": "yb_vich_head" + ("" if mood == "angry" else "_" + mood)}
    return body(cr, YB.VICH, "yb_vich", t, x, s, front=front, backa=backa, swap=sw, **kw)


# ------------------------------------------------------------------ the road map: the big map and the strip


class Path:
    """A smooth path through control points, sampled densely, with points at a fraction of its length."""

    def __init__(self, ctrl, n=400):
        P = [ctrl[0]] + list(ctrl) + [ctrl[-1]]
        pts = []
        for i in range(1, len(P) - 2):
            p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
            for k in range(n // (len(ctrl) - 1)):
                u = k / (n // (len(ctrl) - 1))
                u2, u3 = u * u, u * u * u
                pts.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j])
                                        * u2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in (0, 1)))
        pts.append(tuple(ctrl[-1]))
        self.pts = pts
        self.cum = [0.0]
        for a, b in zip(pts, pts[1:]):
            self.cum.append(self.cum[-1] + math.dist(a, b))
        self.L = self.cum[-1]

    def at(self, u):
        d = clamp(u) * self.L
        i = min(len(self.cum) - 2, max(0, bisect.bisect_right(self.cum, d) - 1))
        seg = (self.cum[i + 1] - self.cum[i]) or 1.0
        f = (d - self.cum[i]) / seg
        a, b = self.pts[i], self.pts[i + 1]
        return a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f

    def upto(self, u, n=120):
        return [self.at(u * i / n) for i in range(n + 1)]


CITY_U = [0.06 + 0.0545 * k for k in range(16)]          # the sixteen cities along the road (0 home .. 1 Yama)
RIVER_U = (CITY_U[7] + CITY_U[8]) / 2                     # the Vaitarani, after the 8th city (Vichitra's)
END_U = 0.975
BIG = Path([(250, 860), (800, 856), (1360, 836), (1560, 786), (1450, 732), (960, 712), (560, 680), (480, 628),
            (700, 590), (1120, 574), (1400, 536), (1470, 490), (1560, 450), (1640, 420)], n=520)
STRIP = Path([(392 + 1340 * i / 24, 985 + 11 * math.sin(i * 1.3)) for i in range(25)])
STRIP_BOX = (350, 947, 1770, 1017)                         # x0, y0, x1, y1
COUNTER_XY = (208, 982)


def journey(tl):
    """(keys, labels): Dhaniram's place on the road [(time, u)] and the counter's text [(time, text)], from the cues."""
    cached = getattr(tl, "_yb_jour", None)
    if cached:
        return cached
    c = {b: cues(tl, b) for b in CUES}
    a1, a2 = c5_arrivals(tl)
    keys = [(c["w1"]["t0"], 0.0), (c["w2"]["N"], 0.0), (c["w7"]["P"], CITY_U[0]), (c["c5"]["P"], CITY_U[0]),
            (c["c6"]["N"], CITY_U[1]), (c["c7"]["t0"] - 0.1, CITY_U[1]), (c["c7"]["C"] + 0.6, CITY_U[4]),
            (c["c8"]["B"], CITY_U[4]),
            (c["c8"]["Bd"] + 0.6, CITY_U[6]), (c["v1"]["C"], CITY_U[7]), (c["v2"]["B"], RIVER_U - 0.014),
            (c["v10"]["L"], RIVER_U - 0.014), (c["v10"]["P"], RIVER_U + 0.016), (c["s1"]["S"], RIVER_U + 0.016),
            (c["s1"]["T"], CITY_U[14]), (c["s4"]["A"], CITY_U[15]), (c["s5"]["S"], CITY_U[15]),
            (c["s5"]["Y"], END_U)]
    roll = [(c["s1"]["S"] + 0.12 * k, f"MONTH {7 + k}") for k in range(6)]
    labels = ([(c["w1"]["t0"], "DAY 13"), (c["w4"]["t0"], "DAY 14"), (c["w5"]["t0"], "DAY 15"),
               (c["w6"]["t0"], "DAY 16"), (c["w7"]["S"], "DAY 17"), (c["w7"]["A"], "DAY 18"), (a1, "MONTH 1"),
               (a2, "MONTH 2"), (c["c7"]["C"], "MONTH 4"), (c["c8"]["N"] + 0.2, "MONTH 5"), (c["v1"]["C"], "MONTH 6")]
              + roll + [(c["s5"]["S"], "1 YEAR")])
    tl._yb_jour = (keys, labels)
    return tl._yb_jour


def where(tl, t):
    """Dhaniram's place on the road (0..1) at t."""
    keys, _ = journey(tl)
    if t <= keys[0][0]:
        return keys[0][1]
    for (ta, ua), (tb, ub) in zip(keys, keys[1:]):
        if t < tb:
            return ua + (ub - ua) * ease((t - ta) / max(0.01, tb - ta))
    return keys[-1][1]


def counter_text(tl, t):
    """(text, time it last changed) of the DAY / MONTH counter."""
    _, labels = journey(tl)
    txt, tc = labels[0][1], labels[0][0]
    for tt, lab in labels:
        if t >= tt:
            txt, tc = lab, tt
    return txt, tc


def house_glyph(cr, x, y, s, a=1.0, col=(0.80, 0.46, 0.22)):
    """A tiny house (home): walls and a roof."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    pc.poly(cr, [(-20, 0), (-20, -24), (0, -42), (20, -24), (20, 0)])
    cr.set_source_rgba(*col, a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(3)
    cr.stroke()
    cr.rectangle(-6, -14, 12, 14)
    cr.set_source_rgba(*INK, a)
    cr.fill()
    cr.restore()


def gate_glyph(cr, x, y, s, a=1.0, col=(0.36, 0.30, 0.34)):
    """Yama's city on the strip: a little dark gate with two towers."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    for sx in (-1, 1):
        cr.rectangle(sx * 18 - 7, -40, 14, 40)
    cr.rectangle(-18, -28, 36, 28)
    cr.set_source_rgba(*col, a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(2.5)
    cr.stroke()
    cr.arc(0, -10, 7, math.pi, 2 * math.pi)
    cr.line_to(7, 0)
    cr.line_to(-7, 0)
    cr.close_path()
    cr.set_source_rgba(1.0, 0.86, 0.5, a)
    cr.fill()
    cr.restore()


def river_mark(cr, x, y0, y1, t, a=1.0, w=16.0):
    """The Vaitarani crossing a map: a short dark-red wavy band from y0 to y1."""
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, col, al in ((w + 6, INK, 0.8), (w, (0.62, 0.10, 0.10), 1.0), (w * 0.3, (0.92, 0.45, 0.40), 0.9)):
        cr.new_path()
        for i in range(21):
            yy = y0 + (y1 - y0) * i / 20
            xx = x + 5 * math.sin(i * 1.1 + t * 2.0)
            (cr.move_to if i == 0 else cr.line_to)(xx, yy)
        cr.set_source_rgba(*col, al * a)
        cr.set_line_width(lw)
        cr.stroke()
    cr.restore()


def strip(cr, t, tl, a=1.0):
    """The road-map strip along the bottom: a palm-leaf band, the winding road, home, sixteen city dots (lit once
    reached), the Vaitarani, Yama's city, little Dhaniram at his place, the DAY / MONTH counter at the left."""
    if a <= 0.01:
        return
    u = where(tl, t)
    x0, y0, x1, y1 = STRIP_BOX
    cr.save()
    pc.poly(cr, [(x0 + 14, y0), (x1 - 14, y0), (x1, y0 + 14), (x1, y1 - 14), (x1 - 14, y1), (x0 + 14, y1),
                 (x0, y1 - 14), (x0, y0 + 14)])
    cr.set_source_rgba(*PARCH, 0.95 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(3.5)
    cr.stroke()
    for k in range(int((x1 - x0 - 40) // 22)):
        for yd in (y0 + 7, y1 - 7):
            cr.new_sub_path()
            cr.arc(x0 + 22 + k * 22, yd, 2.0, 0, 2 * math.pi)
    cr.set_source_rgba(0.55, 0.32, 0.14, 0.7 * a)
    cr.fill()
    dotted(cr, STRIP.upto(1.0), 1.0, 12, 2.6, (0.45, 0.30, 0.16), 0.75 * a)
    walked = STRIP.upto(u, 80)
    if u > 0.004:
        cr.set_source_rgba(0.85, 0.30, 0.12, 0.85 * a)
        cr.set_line_width(5)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(*walked[0])
        for p in walked[1:]:
            cr.line_to(*p)
        cr.stroke()
    rx, ry = STRIP.at(RIVER_U)
    river_mark(cr, rx, y0 + 8, y1 - 8, t, a, 10)
    hx, hy = STRIP.at(0.0)
    house_glyph(cr, hx - 6, hy + 14, 0.62, a)
    for k, cu in enumerate(CITY_U):
        px, py = STRIP.at(cu)
        reached = u >= cu - 0.002
        cr.new_path()
        cr.arc(px, py, 8.5, 0, 2 * math.pi)
        cr.set_source_rgba(*((0.93, 0.62, 0.16) if reached else PARCH), a)
        cr.fill_preserve()
        cr.set_source_rgba(*INK, a)
        cr.set_line_width(3)
        cr.stroke()
    ex, ey = STRIP.at(END_U)
    glow(cr, ex, ey - 10, 60, 0.5 * a)
    gate_glyph(cr, ex + 8, ey + 16, 0.72, a)
    mx, my = STRIP.at(u)
    glow(cr, mx, my - 18, 70, 0.6 * a)
    if a > 0.3:
        dh(cr, t, mx, my + 8, 50, mood="calm", solid=HAND if t < s4_drop(tl) else 0.0, glow=0.5,
           alpha=a, legs=walk_legs(math.sin(t * 7), 0.3))
    cr.restore()
    txt, tc = counter_text(tl, t)
    kick = 1 + 0.25 * math.exp(-6 * max(0.0, t - tc)) * (t > tc)
    cx, cy = COUNTER_XY
    w_, h_ = text_size(txt, 38)
    cr.save()
    cr.translate(cx, cy)
    cr.scale(kick, kick)
    bw, bh = w_ / 2 + 22, h_ / 2 + 14
    pc.poly(cr, [(-bw, -bh), (bw, -bh), (bw + 8, 0), (bw, bh), (-bw, bh), (-bw - 8, 0)])
    cr.set_source_rgba(*PARCH, 0.97 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(3.5)
    cr.stroke()
    draw_text(cr, txt, 0, 2, 38, RED, a, anchor="cm")
    cr.restore()


def s4_drop(tl):
    """When the hand-sized body falls away (s4)."""
    return cues(tl, "s4")["C"]


def big_map(cr, t, tl, t_in, a=1.0, u_dh=0.0, trail=0.0):
    """The whole road as a big map on the cloth: home, the winding road (drawn in from t_in), sixteen city gates
    popping in, the dark-red river, Yama's city far away; little Dhaniram at u_dh."""
    if a <= 0.01:
        return {}
    p = ease((t - t_in) / 1.4) if t > t_in else 0.0
    if p > 0.004:
        n = max(2, int(200 * p))
        us = [p * i / n for i in range(n + 1)]
        cen = [BIG.at(u) for u in us]
        half = [15 - 9 * u for u in us]                            # the road narrows into the distance
        left, right = [], []
        for i, (x, y) in enumerate(cen):
            x0, y0 = cen[max(0, i - 1)]
            x1, y1 = cen[min(n, i + 1)]
            ln = math.hypot(x1 - x0, y1 - y0) or 1.0
            nx, ny = -(y1 - y0) / ln, (x1 - x0) / ln
            left.append((x + nx * half[i], y + ny * half[i]))
            right.append((x - nx * half[i], y - ny * half[i]))
        cr.save()
        pc.poly(cr, left + right[::-1])
        cr.set_source_rgba(0.88, 0.70, 0.44, 0.95 * a)
        cr.fill_preserve()
        cr.set_source_rgba(0.36, 0.22, 0.10, 0.6 * a)
        cr.set_line_width(3)
        cr.stroke()
        cr.restore()
        dotted(cr, cen, 1.0, 24, 3.0, (0.45, 0.28, 0.12), 0.75 * a)
    hx, hy = BIG.at(0.0)
    prop(cr, "dv_house", hx - 70, hy + 24, 0.12, alpha=a * prog(t, t_in, 0.3))
    if p > RIVER_U:
        rx, ry = BIG.at(RIVER_U)
        river_mark(cr, rx, ry - 46, ry + 46, t, a * prog(t, t_in + 0.6, 0.3), 18)
    for k, cu in enumerate(CITY_U):
        q = pop(t, t_in + 0.25 + 0.07 * k, 0.3, 1.8)
        if q <= 0.01 or cu > p + 0.02:
            continue
        x, y = BIG.at(cu)
        xa, ya = BIG.at(cu - 0.01)
        xb, yb = BIG.at(cu + 0.01)
        ln = math.hypot(xb - xa, yb - ya) or 1.0
        nx, ny = -(yb - ya) / ln, (xb - xa) / ln
        if ny > 0:
            nx, ny = -nx, -ny                                       # always beside the road, on its far side
        sc = (0.10 - 0.045 * cu) * q
        off = 30 - 12 * cu
        prop(cr, "gp_gate", x + nx * off, y + ny * off + 6, sc, alpha=clamp(q) * a)
    q = pop(t, t_in + 1.3, 0.4, 1.4)
    ex, ey = BIG.at(1.0)
    if q > 0.01:
        glow(cr, ex + 30, ey - 50, 260, 0.6 * q * a)
        aura(cr, t, ex + 30, ey - 50, 50, 170, 0.35 * q * a, n=14, spin=0.03, col=(0.95, 0.45, 0.25))
        prop(cr, "yb_yamapura", ex + 30, ey + 16, 0.13 * q, alpha=clamp(q) * a)
    pts = {}
    if trail > 0:
        tr = BIG.upto(u_dh, 40)
        dotted(cr, tr, 1.0, 16, 4.0, (0.95, 0.75, 0.30), 0.9 * a * trail)
        x, y = BIG.at(u_dh)
        pts = dh(cr, t, x, y + 8, 150, mood="calm", alpha=a * trail, legs=walk_legs(math.sin(t * 6), 0.35))
    return pts


# ------------------------------------------------------------------ small things


def sky_sun(cr, t, x, y, s=0.3, a=1.0, hot=0.0):
    if a <= 0.01:
        return
    warm(cr, x, y, 160 * s / 0.3, (0.55 + 0.3 * hot) * a, (1.0, 0.62, 0.2))
    prop(cr, "sun", x, y, s, rot=t * 0.25, alpha=a)


def scroll_x(x0, t, speed, period, margin=300):
    """A scenery item scrolling left: its x at time t (wrapping every `period` px)."""
    return (x0 - speed * t) % period - margin


def cracks(cr, t, speed=0.0, a=1.0, y0=FL + 18):
    """Dry, cracked earth along the floor, scrolling with the walk."""
    cr.save()
    cr.set_source_rgba(0.36, 0.22, 0.10, 0.6 * a)
    cr.set_line_width(3)
    for i in range(16):
        x0 = scroll_x(80 + 160 * i, t, speed, 2560, 320)
        y = y0 + 22 * ((i * 0.618) % 1.0)
        pts = [(x0, y), (x0 + 30, y + 18), (x0 + 22, y + 44), (x0 + 50, y + 60)]
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
        cr.move_to(x0 + 30, y + 18)
        cr.line_to(x0 + 70, y + 12)
        cr.stroke()
    cr.restore()


def far_hills(cr, t, speed=0.0, a=1.0, col=(0.62, 0.42, 0.26), y=FL - 40):
    """Low hills along the horizon, scrolling slowly (far away)."""
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    off = (speed * t * 0.25) % 640
    cr.move_to(-700, y + 60)
    for i in range(0, 41):
        x = -700 + 80 * i - off
        cr.line_to(x, y - 60 - 55 * abs(math.sin(i * 0.9 + 0.4)) - 30 * math.sin(i * 0.37))
    cr.line_to(W + 700, y + 60)
    cr.close_path()
    cr.set_source_rgba(*col, 0.45 * a)
    cr.fill()
    cr.restore()


def ground_line(cr, a=1.0, y=FL + 6, blur=0.0):
    """The grassy floor (puppet_cast's ground strip)."""
    prop(cr, "ground", W / 2, y, 1.42, alpha=a, blur=blur)


def dry_ground(cr, t, speed=0.0, a=1.0, col=(0.80, 0.58, 0.34), y=FL + 4):
    """The bare floor of the road: dry earth with an inked edge, pebbles and cracks scrolling with the walk."""
    if a <= 0.01:
        return
    cr.save()
    cr.move_to(-20, y + 4)
    off = speed * t
    for i in range(0, 50):
        x = -20 + 40 * i
        cr.line_to(x, y - 4 * abs(math.sin((x + off) * 0.013)) - 3 * math.sin((x + off) * 0.041))
    cr.line_to(W + 20, H + 20)
    cr.line_to(-20, H + 20)
    cr.close_path()
    path = cr.copy_path()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(*col, 0.85 * a)
    cr.fill()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.append_path(path)
    cr.set_source_rgba(*INK, 0.8 * a)
    cr.set_line_width(5)
    cr.stroke()
    cr.restore()
    cracks(cr, t, speed, a, y + 14)
    for i in range(12):
        x = scroll_x(90 + 230 * i, t, speed, 2760, 200)
        cr.new_path()
        pc.ell(cr, x, y + 30 + 40 * ((i * 0.37) % 1.0), 11 + 5 * (i % 3), 6)
        cr.set_source_rgba(0.36, 0.24, 0.14, 0.7 * a)
        cr.fill()


def bubble(cr, t, t_in, x, y, r, src, a=1.0, t_pop=None, content=None):
    """A thought bubble (cloud ellipse with little trailing circles toward src) popping in at t_in; content(cr, x, y,
    r) draws inside; t_pop bursts it."""
    q = pop(t, t_in, 0.32, 1.6)
    if t_pop is not None and t > t_pop:
        u = (t - t_pop) / 0.35
        if u >= 1:
            return
        q *= 1 + 0.4 * u
        a *= 1 - u
    if q <= 0.01 or a <= 0.01:
        return
    for i, f in enumerate((0.3, 0.55, 0.78)):
        bx = src[0] + (x - src[0]) * f
        by = src[1] + (y + r * 0.7 - src[1]) * f
        cr.new_path()
        cr.arc(bx, by, (6 + 6 * i) * clamp(q), 0, 2 * math.pi)
        cr.set_source_rgba(1.0, 0.97, 0.88, 0.95 * a)
        cr.fill_preserve()
        cr.set_source_rgba(*INK, a)
        cr.set_line_width(3)
        cr.stroke()
    rr = r * q
    cr.save()
    cr.translate(x, y)
    cr.new_path()
    for i in range(12):
        ang = 2 * math.pi * i / 12
        cr.new_sub_path()
        cr.arc(0.78 * rr * math.cos(ang), 0.62 * rr * math.sin(ang), 0.36 * rr, 0, 2 * math.pi)
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(7)
    cr.stroke_preserve()
    cr.set_source_rgba(1.0, 0.97, 0.88, 0.97 * a)
    cr.fill()
    cr.new_path()
    pc.ell(cr, 0, 0, 0.92 * rr, 0.74 * rr)
    cr.fill()
    cr.restore()
    if content is not None:
        cr.save()
        cr.push_group()
        content(cr, x, y, rr)
        cr.pop_group_to_source()
        cr.paint_with_alpha(a)
        cr.restore()


def tears(cr, t, x, y, a=1.0, side=1, n=3):
    """Glowing tears falling from (x, y)."""
    if a <= 0.01:
        return
    for i in range(n):
        u = (t * 1.3 + i / n) % 1.0
        tx = x + side * (6 + 20 * u)
        ty = y + 70 * u * u + 6
        cr.new_path()
        cr.move_to(tx, ty - 9)
        cr.curve_to(tx + 6, ty, tx + 5, ty + 7, tx, ty + 7)
        cr.curve_to(tx - 5, ty + 7, tx - 6, ty, tx, ty - 9)
        cr.set_source_rgba(0.70, 0.88, 1.0, 0.9 * a * (1 - u))
        cr.fill_preserve()
        cr.set_source_rgba(0.12, 0.30, 0.52, 0.6 * a * (1 - u))
        cr.set_line_width(1.5)
        cr.stroke()


def sweat(cr, t, t0, x, y, a=1.0):
    """Drops of sweat flying off a head (shock)."""
    u = (t - t0) / 0.7
    if not 0 < u < 1:
        return
    for i, ang in enumerate((-2.4, -1.9, -1.2, -0.7)):
        r = 30 + 90 * ease(u)
        dx, dy = math.cos(ang) * r, math.sin(ang) * r + 60 * u * u
        cr.new_path()
        cr.arc(x + dx, y + dy, 7 * (1 - u) + 3, 0, 2 * math.pi)
        cr.set_source_rgba(0.72, 0.90, 1.0, a * (1 - u))
        cr.fill_preserve()
        cr.set_source_rgba(*INK, 0.6 * a * (1 - u))
        cr.set_line_width(2)
        cr.stroke()


def shock_marks(cr, t, t0, x, y, a=1.0, dur=1.2):
    """Little shock lines bursting round a head."""
    u = (t - t0) / dur
    if not 0 < u < 1:
        return
    k = math.sin(math.pi * min(1.0, u * 2.5))
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for i, ang in enumerate((-2.7, -2.2, -1.57, -0.95, -0.45)):
        r0, r1 = 50 + 10 * k, 90 + 30 * k
        cr.move_to(x + r0 * math.cos(ang), y + r0 * math.sin(ang))
        cr.line_to(x + r1 * math.cos(ang), y + r1 * math.sin(ang))
    cr.set_source_rgba(*RED, 0.9 * a * (1 - u * 0.6))
    cr.set_line_width(7)
    cr.stroke()
    cr.restore()


def dust(cr, t, t0, x, y, a=1.0, w=1.0):
    """A puff of dust where something lands."""
    u = (t - t0) / 0.8
    if not 0 < u < 1:
        return
    for i in range(7):
        ang = math.pi + math.pi * i / 6
        r = (30 + 110 * ease(u)) * w
        cr.new_path()
        cr.arc(x + r * math.cos(ang), y + 0.35 * r * math.sin(ang) - 10 * u, (16 + 20 * u) * w, 0, 2 * math.pi)
        cr.set_source_rgba(0.74, 0.60, 0.42, 0.55 * a * (1 - u))
        cr.fill()


def ha_ha(cr, t, x, y, a=1.0, ph=0.0, size=40):
    """"HA HA" popping up and floating off a laughing head."""
    if a <= 0.01:
        return
    for i in range(2):
        u = ((t + ph) * 0.9 + i * 0.5) % 1.0
        draw_text(cr, "HA HA", x + 30 * i - 10, y - 70 * u, size, RED, a * math.sin(math.pi * u), anchor="cm")


def icon_card(cr, t, t_in, x, y, w, h, alpha=1.0, rods=True, t_out=None):
    """An empty parchment card on two rods, dropping in at t_in; returns its alpha (0 = not shown)."""
    q = pop(t, t_in, 0.35, 1.4)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.3)
    a = clamp(q) * alpha
    if a <= 0.01:
        return 0.0
    yy = y + 50 * (1 - clamp(q))
    if rods:
        pc.rod(cr, x - w * 0.3, yy + h / 2, x - w * 0.3 + 20, H + 60, alpha=0.5 * a)
        pc.rod(cr, x + w * 0.3, yy + h / 2, x + w * 0.3 + 30, H + 60, alpha=0.5 * a)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(sway(t, 0.006, 0.4, x * 0.01))
    pc.poly(cr, [(-w / 2, -h / 2 + 16), (-w / 2 + 16, -h / 2), (w / 2 - 16, -h / 2), (w / 2, -h / 2 + 16),
                 (w / 2, h / 2 - 16), (w / 2 - 16, h / 2), (-w / 2 + 16, h / 2), (-w / 2, h / 2 - 16)])
    cr.set_source_rgba(*PARCH, 0.97 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(4)
    cr.stroke()
    for k in range(int((w - 40) // 20)):
        for yd in (-h / 2 + 9, h / 2 - 9):
            cr.new_sub_path()
            cr.arc(-w / 2 + 20 + k * 20, yd, 2.2, 0, 2 * math.pi)
    cr.set_source_rgba(0.55, 0.32, 0.14, 0.75 * a)
    cr.fill()
    cr.restore()
    return a


def card_y(t, t_in, y):
    return y + 50 * (1 - clamp(pop(t, t_in, 0.35, 1.4)))


def green_tick(cr, x, y, size, p, alpha=1.0):
    from poster import tick
    tick(cr, x, y, size, p, color=GREEN_TICK, alpha=alpha)


def arrow_r(cr, x0, x1, y, p, a=1.0, col=INK, w=8):
    """A short arrow pointing right, drawn to fraction p."""
    if p <= 0:
        return
    xe = x0 + (x1 - x0) * p
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_source_rgba(*col, a)
    cr.set_line_width(w)
    cr.move_to(x0, y)
    cr.line_to(xe - 6, y)
    cr.stroke()
    pc.poly(cr, [(xe + 8, y), (xe - 18, y - 16), (xe - 18, y + 16)])
    cr.fill()
    cr.restore()


def snow(cr, t, a=1.0, n=70, speed=1.0):
    """Snowflakes drifting down over the cloth."""
    if a <= 0.01:
        return
    cr.save()
    for i in range(n):
        ph = i * 2.399
        x = (i * 271 + 60 * math.sin(t * 0.8 + ph)) % W
        y = ((t * (60 + 25 * (i % 5)) * speed + i * 137) % (H + 60)) - 30
        r = 3 + (i % 4) * 1.6
        cr.new_path()
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.85 * a)
        cr.fill_preserve()
        cr.set_source_rgba(0.35, 0.45, 0.62, 0.5 * a)
        cr.set_line_width(1.2)
        cr.stroke()
    cr.restore()


def frost(cr, a=1.0):
    """Snow lying along the floor."""
    if a <= 0.01:
        return
    cr.save()
    cr.move_to(-20, FL - 4)
    for i in range(0, 41):
        x = -20 + 49 * i
        cr.line_to(x, FL - 10 - 10 * abs(math.sin(i * 1.7)))
    cr.line_to(W + 20, H)
    cr.line_to(-20, H)
    cr.close_path()
    cr.set_source_rgba(0.95, 0.97, 1.0, 0.85 * a)
    cr.fill_preserve()
    cr.set_source_rgba(0.40, 0.50, 0.66, 0.6 * a)
    cr.set_line_width(3)
    cr.stroke()
    cr.restore()


def heat(cr, t, a=1.0, y0=330, y1=FL - 40):
    """Heat shimmer: wavy pale lines rising."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(10):
        x = 120 + 190 * i
        u = (t * 0.5 + i * 0.37) % 1.0
        yb = y1 - (y1 - y0) * u
        cr.new_path()
        for k in range(9):
            yy = yb - 14 * k
            (cr.move_to if k == 0 else cr.line_to)(x + 8 * math.sin(k * 1.2 + t * 6 + i), yy)
        cr.set_source_rgba(1.0, 0.86, 0.6, 0.45 * a * math.sin(math.pi * u))
        cr.set_line_width(4)
        cr.stroke()
    cr.restore()


def river_band(cr, t, top, bottom, a=1.0, speed=1.0, boil=0.0, whirl=0.6):
    """The Vaitarani across the stage from y=top (far bank) to y=bottom (near edge): dark-red water (never gore),
    rows of slow leather waves, whirlpools; boil 0..1 adds rising bubbles and steam."""
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    g = cairo.LinearGradient(0, top, 0, bottom)
    g.add_color_stop_rgba(0, 0.70, 0.30, 0.28, a)
    g.add_color_stop_rgba(1, 0.86, 0.38, 0.32, a)
    cr.rectangle(0, top, W, bottom - top)
    cr.set_source(g)
    cr.fill()
    cr.restore()
    n = 6
    for k in range(n):
        v = k / (n - 1)
        y = top + 24 + (bottom - top - 40) * v ** 1.15
        s = 0.42 + 0.42 * v
        per = 2080 * s
        off = (t * (22 + 30 * v) * speed * (1 if k % 2 else -1)) % (160 * s)
        for xx in (off - per, off, off + per, off + 2 * per):
            prop(cr, "gp_rwaveA" if k % 2 == 0 else "gp_rwaveB", xx, y, s, alpha=0.8 * a)
    for i, (x, v, r) in enumerate(((330, 0.35, 110), (900, 0.2, 80), (1350, 0.55, 140), (1700, 0.3, 90),
                                   (620, 0.75, 120))):
        y = top + 24 + (bottom - top - 40) * v ** 1.15 - 30
        sc = 0.5 + 0.6 * v
        spin = -t * (0.8 + 0.25 * i) * speed
        cr.save()
        cr.translate(x, y)
        cr.scale(1.0, 0.35)
        for lw, col, al in ((12, (0.25, 0.04, 0.04), 0.5), (6, (1.0, 0.62, 0.48), 0.85)):
            cr.new_path()
            for j in range(80):
                q = j / 79
                ang = spin + q * 3.4 * math.pi
                rr = r * sc * (0.1 + q)
                (cr.move_to if j == 0 else cr.line_to)(rr * math.cos(ang), rr * math.sin(ang))
            cr.set_source_rgba(*col, al * a * whirl)
            cr.set_line_width(lw)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.stroke()
        cr.restore()
    if boil > 0.01:
        bubbles(cr, t, top, bottom, boil * a)


def bubbles(cr, t, top, bottom, a=1.0, n=34):
    """Bubbles rising and bursting all over the river, wisps of steam above."""
    cr.save()
    for i in range(n):
        ph = (i * 0.618) % 1.0
        u = (t * (0.9 + 0.5 * ((i * 0.37) % 1.0)) + ph) % 1.0
        x = 60 + (i * 157) % (W - 120)
        v = ((i * 0.29) % 1.0)
        y = top + 30 + (bottom - top - 50) * v
        r = (10 + 26 * v) * (0.3 + 0.9 * u)
        if u < 0.85:
            cr.new_path()
            cr.arc(x, y - 6 * u, r, math.pi, 2 * math.pi)
            cr.close_path()
            cr.set_source_rgba(0.95, 0.52, 0.42, 0.85 * a)
            cr.fill_preserve()
            cr.set_source_rgba(0.30, 0.04, 0.04, 0.9 * a)
            cr.set_line_width(3)
            cr.stroke()
            cr.new_path()
            cr.arc(x - r * 0.35, y - r * 0.45, r * 0.18, 0, 2 * math.pi)
            cr.set_source_rgba(1.0, 0.92, 0.85, 0.8 * a)
            cr.fill()
        else:
            k = (u - 0.85) / 0.15
            for j in range(5):
                ang = math.pi + math.pi * j / 4
                cr.new_path()
                cr.arc(x + (r + 20 * k) * math.cos(ang), y + (r + 20 * k) * math.sin(ang), 3.5, 0, 2 * math.pi)
                cr.set_source_rgba(0.95, 0.55, 0.45, a * (1 - k))
                cr.fill()
    for i in range(9):
        x = 120 + 210 * i
        u = (t * 0.35 + i * 0.41) % 1.0
        yb = top - 10 - 160 * u
        cr.new_path()
        for k in range(7):
            (cr.move_to if k == 0 else cr.line_to)(x + 14 * math.sin(k * 1.3 + t * 3 + i), yb - 16 * k)
        cr.set_source_rgba(1.0, 0.96, 0.92, 0.5 * a * math.sin(math.pi * u))
        cr.set_line_width(10)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.stroke()
    cr.restore()


def blue_river(cr, t, top, bottom, a=1.0):
    """The pretty river at Saumya: a band of clear blue water with gentle moving ripples and lotuses."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    g = cairo.LinearGradient(0, top, 0, bottom)
    g.add_color_stop_rgba(0, 0.62, 0.82, 0.96, a)
    g.add_color_stop_rgba(1, 0.74, 0.90, 0.98, a)
    cr.rectangle(0, top, W, bottom - top)
    cr.set_source(g)
    cr.fill()
    cr.restore()
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for edge in (top, bottom):
        cr.move_to(0, edge)
        for i in range(0, 97):
            x = 20 * i
            cr.line_to(x, edge + 3 * math.sin(x * 0.03 + t * 1.5))
        cr.set_source_rgba(0.10, 0.26, 0.42, 0.7 * a)
        cr.set_line_width(3.5)
        cr.stroke()
    for k in range(3):
        y = top + (bottom - top) * (k + 1) / 4
        off = (t * (22 + 8 * k) * (1 if k % 2 else -1)) % 160
        for i in range(-1, 14):
            x0 = i * 160 + off + 40 * k
            cr.move_to(x0, y)
            cr.curve_to(x0 + 14, y - 7, x0 + 30, y - 7, x0 + 44, y)
            cr.set_source_rgba(1.0, 1.0, 1.0, 0.65 * a)
            cr.set_line_width(4)
            cr.stroke()
    cr.restore()
    for i, x in enumerate((180, 560, 940)):
        prop(cr, "md_lotus", x + 10 * math.sin(t * 0.7 + i), top + 26 + 18 * (i % 2), 0.26, alpha=a)


def thought_cloud(cr, t, t_in, x, y, w, h, src, items, a=1.0, t_out=None):
    """One thought cloud (a scalloped cream cloud, little circles trailing down to src) popping in at t_in; items =
    [(t_show, t_pop, dx, fn)], fn(cr, cx, cy) draws a thing in it at its place, which bursts in a puff at t_pop."""
    q = pop(t, t_in, 0.35, 1.5)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.3)
    a *= clamp(q)
    if a <= 0.01:
        return
    for i, f in enumerate((0.35, 0.62, 0.85)):
        bx = src[0] + (x - 0.25 * w - src[0]) * f
        by = src[1] + (y + 0.45 * h - src[1]) * f
        cr.new_path()
        cr.arc(bx, by, 7 + 7 * i, 0, 2 * math.pi)
        cr.set_source_rgba(1.0, 0.97, 0.88, 0.95 * a)
        cr.fill_preserve()
        cr.set_source_rgba(*INK, a)
        cr.set_line_width(3)
        cr.stroke()
    k = 0.6 + 0.4 * clamp(q)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    cr.new_path()
    n = 14
    for i in range(n):
        ang = 2 * math.pi * i / n
        cr.new_sub_path()
        cr.arc(0.42 * w * math.cos(ang), 0.36 * h * math.sin(ang), 0.17 * w if abs(math.cos(ang)) > 0.7 else 0.2 * h,
               0, 2 * math.pi)
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(7)
    cr.stroke_preserve()
    cr.set_source_rgba(1.0, 0.97, 0.88, 0.97 * a)
    cr.fill()
    cr.new_path()
    pc.ell(cr, 0, 0, 0.47 * w, 0.42 * h)
    cr.fill()
    cr.restore()
    for t_show, t_pop, dx, fn in items:
        p = pop(t, t_show, 0.3, 1.8)
        if p <= 0.01:
            continue
        al = a
        if t_pop is not None and t > t_pop:
            u = (t - t_pop) / 0.35
            if u >= 1:
                continue
            al *= 1 - u
            p *= 1 + 0.5 * u
            for j in range(8):
                ang = 2 * math.pi * j / 8
                cr.new_path()
                cr.arc(x + dx + (40 + 60 * u) * math.cos(ang), y + (40 + 60 * u) * math.sin(ang), 8 * (1 - u) + 2, 0,
                       2 * math.pi)
                cr.set_source_rgba(0.85, 0.75, 0.55, a * (1 - u))
                cr.fill()
        cr.save()
        cr.translate(x + dx, y)
        cr.scale(p * k, p * k)
        cr.push_group()
        fn(cr, 0, 0)
        cr.pop_group_to_source()
        cr.paint_with_alpha(clamp(al))
        cr.restore()


# ------------------------------------------------------------------ the shots: the road


def w1_card_out(tl):
    """When the road's chapter card flies off (w1) and the big map starts drawing itself."""
    c = cues(tl, "w1")
    return min(max(c["t0"] + 2.0, c["N"] + 0.7), cues(tl, "w2")["t0"] - 1.0)


def map_labels(cr, t, t_out, a=1.0):
    """HOME, YAMA'S CITY and 16 CITIES on the big map (w1, w2)."""
    hx, hy = BIG.at(0.0)
    ex, ey = BIG.at(1.0)
    plate(cr, t, t_out + 0.3, "HOME", hx - 70, hy - 90, 32, alpha=a)
    plate(cr, t, t_out + 1.4, "YAMA'S CITY", ex - 20, ey - 140, 32, alpha=a)
    counter_badge(cr, t, t_out + 1.1, "16 CITIES", 1690, 640, 60, alpha=a)


def s_w1(cr, t, tl, t0, t1):
    c = cues(tl, "w1")
    tY = c["Y"]
    t_out = w1_card_out(tl)
    big_map(cr, t, tl, t_out - 0.15)
    chapter(cr, t, t0 - 0.3, t_out, "DAY 13", [[("THE ROAD", INK)], [("86,000", RED), ("YOJANAS", INK)]], SOURCE)

    def ui(cr):
        if t > t_out:
            head2(cr, t, "THE ROAD TO YAMA'S CITY:", t_out + 0.05, "86,000 YOJANAS", t_out + 0.25,
                  under=max(tY, t_out + 0.6))
            map_labels(cr, t, t_out)
    return dict(ui=ui, flash=flash_at(t, t_out, 0.2), strip=0.0)


def s_w2(cr, t, tl, t0, t1):
    c = cues(tl, "w2")
    tR, tN, tD, tRt = c["R"], c["N"], c["D"], c["Rt"]
    fu = clamp((t - (t1 - 0.85)) / 0.75)
    fold = fu * fu * (3 - 2 * fu)                       # the map folds down into the strip at the bottom
    gone = clamp((fold - 0.6) / 0.4)
    # the sky: the sun crosses and sets, then the moon (day and night)
    span = max(1.2, tRt - tD + 0.8)
    night = 0.0
    if t > tD - 0.6:
        u = clamp((t - tD + 0.6) / span)
        if u < 0.55:
            v = u / 0.55
            ang = math.pi * (1 - v)
            sky_sun(cr, t, 960 + 700 * math.cos(ang), 560 - 260 * math.sin(ang), 0.3, 1 - fold)
        else:
            v = (u - 0.55) / 0.45
            ang = math.pi * (1 - v)
            night = 0.45 * math.sin(math.pi * min(1.0, v * 1.3))
            stars(cr, t, night / 0.45 * (1 - fold), ((380, 330), (620, 420), (1120, 330), (1300, 420), (1700, 520),
                                                      (220, 520)))
            prop(cr, "moon", 960 + 700 * math.cos(ang), 560 - 260 * math.sin(ang), 0.5, alpha=0.85 * (1 - fold))
    cr.save()
    cr.translate(985 + 75 * fold, 640 + 349 * fold)
    cr.scale(1 - 0.16 * fold, 1 - 0.865 * fold)
    cr.translate(-985, -640)
    walk_u = 0.035 * clamp((t - tR) / max(1.0, t1 - tR))
    t_map = w1_card_out(tl)
    pts = big_map(cr, t, tl, t_map - 0.15, 1 - gone, walk_u, prog(t, tR - 0.2, 0.4) * (1 - fold))
    cr.restore()

    def ui(cr):
        if t < tD:
            head2(cr, t, "EVERY DAY, HE MUST WALK", t0 + 0.05, "247 YOJANAS", tN)
        else:
            head2(cr, t, "NO REST:", tD - 0.15, "DAY AND NIGHT", tD + 0.05, under=tRt)
        counter_badge(cr, t, tN + 0.15, "247 YOJANAS / DAY", 1250, 960, 52, alpha=1 - clamp(3 * fold))
        map_labels(cr, t, t_map, 1 - clamp(3 * fold))
        if pts and "top" in pts and fold < 0.3:
            tag(cr, t, tR + 0.1, "DHANIRAM", pts["top"][0] + 10, pts["top"][1] - 50, 28, alpha=1 - clamp(3 * fold))
    return dict(ui=ui, night=night, lift=1.0, flash=flash_at(t, tN, 0.12), strip=clamp((fold - 0.55) / 0.45))


SUM_X = 1340


def s_w3(cr, t, tl, t0, t1):
    c = cues(tl, "w3")
    tU, tH, tO, tK, tM = c["U"], c["H"], c["O"], c["K"], c["M"]
    far_hills(cr, t, 0.0, 0.8)
    dry_ground(cr, t)
    x, hh = 640, 540
    glow(cr, x, FL - 300, 520, 0.4)
    # counting: the front hand up before his face, tapping as he counts; at the shock he jumps, arms flung up
    shock = prog(t, tO - 0.05, 0.2)
    tap = 0.12 * math.sin(t * 13) * (1 - shock) * (tU < t < tO)
    jump = -45 * math.sin(math.pi * clamp((t - tO) / 0.45)) if t > tO else 0.0
    front = mix((-1.25 + tap, -1.55), (-2.15, -0.55), shock)
    backa = mix((0.25, -0.6), (-1.95, -0.7), shock)
    mood = "talking" if t < tO else "shocked"
    pts = dh(cr, t, x, FL + jump, hh, mood=mood, front=front, backa=backa, hand="point" if t < tO else "open",
             hits=[(tO, 0.6)], head=-0.08 * shock, glow=0.6)
    hd = to_user(cr, pts["head"]) if "head" in pts else (x + 40, FL - 520)
    fing = to_user(cr, pts["handF"]) if "handF" in pts else (x + 120, FL - 480)
    # numbers popping off his fingertip
    if tU - 0.2 < t < tO + 0.3:
        for i, txt in enumerate(("247", "× 13", "= ?")):
            ts = tU + 0.15 + 0.55 * i
            u = (t - ts) / 1.6
            if 0 < u < 1:
                draw_text(cr, txt, fing[0] + 50 + 60 * u, fing[1] - 40 - 170 * u, 74, RED,
                          math.sin(math.pi * min(1.0, u * 1.4)) * (1 - prog(t, tO, 0.3)), anchor="cm")
    sweat(cr, t, tO, hd[0], hd[1] - 60)
    shock_marks(cr, t, tO, hd[0] + 10, hd[1] - 40)
    dev_card = (SUM_X, 470)

    def ui(cr):
        if t < tK:
            head2(cr, t, "DHANIRAM DID THE MATHS ON HIS FINGERS:", t0 + 0.05, "247 × 13 KM = ?", tH)
        else:
            head2(cr, t, "THAT'S...", tK - 0.15, "THOUSANDS OF KM. EVERY DAY!", tK + 0.05, under=tM + 0.4)
        a = icon_card(cr, t, tU, dev_card[0], dev_card[1], 640, 330)
        if a > 0:
            yy = card_y(t, tU, dev_card[1])
            draw_text(cr, "1 YOJANA ≈ 13 KM", dev_card[0], yy - 110, 44, FADE, a * prog(t, tU + 0.2, 0.3),
                      MONO_FONT, "cm", tracking=2)
            draw_text(cr, "247 YOJANAS ≈", dev_card[0], yy - 20, 64, INK, a * prog(t, tH, 0.3), anchor="cm")
            q = pop(t, tO - 0.1, 0.3, 2.0)
            if q > 0:
                cr.save()
                cr.translate(dev_card[0], yy + 85)
                cr.scale(0.6 + 0.4 * q, 0.6 + 0.4 * q)
                draw_text(cr, "3,200 KM", 0, 0, 104, RED, a * clamp(q), anchor="cm")
                cr.restore()
            if t > tK:
                red_ring(cr, dev_card[0], yy + 85, 240, 70, prog(t, tK, 0.4), 8, a)
        if t > tM:
            from scenes_jarasandha import stamp
            stamp(cr, t, tM + 0.1, "EVERY DAY!", dev_card[0] + 40, dev_card[1] + 270, 76)
    return dict(ui=ui, flash=flash_at(t, tO, 0.25), strip=1.0)


W4_X = 900                           # Dhaniram's x on the road (the messengers behind him to the left)
SUNS = [(170 + 1580 * k / 11, 312 + 22 * math.sin(k * 1.9)) for k in range(12)]     # the twelve suns


def s_w4(cr, t, tl, t0, t1):
    c = cues(tl, "w4")
    tC, tK, tP, tA, tB, tS = c["C"], c["K"], c["P"], c["A"], c["B"], c["S"]
    sp = 120.0
    hot = prog(t, tB, 1.2)
    far_hills(cr, t, sp, 0.9, (0.70, 0.44, 0.24))
    if t < tB + 0.3:
        sky_sun(cr, t, 1660, 330, 0.3, 1.0 - prog(t, tB, 0.3))
    for k in range(12):
        ts = tB + 0.12 * k
        q = pop(t, ts, 0.3, 1.8)
        if q <= 0.01:
            continue
        sx, sy = SUNS[k]
        sky_sun(cr, t + k, sx, sy, 0.2 * q, clamp(q), hot)
    for i in range(5):
        x = scroll_x(200 + 520 * i, t, sp * 0.6, 2600, 300)
        prop(cr, "c6_rock", x, FL + 4, 0.22 + 0.06 * (i % 2), alpha=0.85, blur=2)
    dry_ground(cr, t, sp)
    heat(cr, t, hot)
    look = prog(t, tS, 0.3)
    trio(cr, t, W4_X, dmood="sheepish" if t < tS else "shocked",
         dkw=dict(front=mix((-0.25, -0.35), (-2.3, -1.6), look), head=-0.18 * look, hits=[(tS, 0.3)]))
    icons = ((tC, 1250, "yb_tree"), (tK, 1480, "dv_bowl"), (tP, 1700, "md_kalasha"))

    def ui(cr):
        if t < tA:
            head2(cr, t, "ON THE ROAD:", t0 + 0.05, "NO SHADE, NO FOOD, NO WATER", tC)
        else:
            head2(cr, t, "AND IN THE SKY...", tA - 0.1, "12 SUNS!", tB + 0.1, under=tS + 0.4)
        fade = 1 - prog(t, tA - 0.1, 0.35)
        for tt, x, name in icons:
            q = pop(t, tt - 0.1, 0.32, 1.6)
            if q <= 0.01 or fade <= 0.01:
                continue
            a = clamp(q) * fade
            y = 560
            cr.new_path()
            cr.arc(x, y, 92 * q, 0, 2 * math.pi)
            cr.set_source_rgba(*PARCH, 0.95 * a)
            cr.fill_preserve()
            cr.set_source_rgba(*INK, a)
            cr.set_line_width(4)
            cr.stroke()
            if name == "yb_tree":
                prop(cr, "tree", x, y + 70, 0.13 * q, alpha=a)
            elif name == "dv_bowl":
                prop(cr, "dv_bowl", x, y + 10, 0.9 * q, alpha=a)
            else:
                prop(cr, "md_kalasha", x, y + 60, 0.3 * q, alpha=a)
            big_x(cr, x, y, 150, 150, prog(t, tt + 0.15, 0.25), a, lw=16)
    return dict(ui=ui, eve=0.15 + 0.3 * hot, flash=flash_at(t, tB, 0.15) + 0.25 * hot * (0.5 + 0.5 * math.sin(t * 3)) *
                0.3, strip=1.0)


def s_w5(cr, t, tl, t0, t1):
    c = cues(tl, "w5")
    tK, tR, tT, tJ = c["K"], c["R"], c["T"], c["J"]
    sp = 120.0
    x_dh = 900
    far_hills(cr, t, sp * 0.4, 0.8)
    # "somewhere thorns, somewhere hot sand, somewhere a forest of sword-leaves": each rises round them on its word
    th = prog(t, tK - 0.25, 0.35) * (1 - prog(t, tR - 0.2, 0.3))
    sa = prog(t, tR - 0.2, 0.35) * (1 - prog(t, tT - 0.2, 0.3))
    sw = prog(t, tT - 0.25, 0.45)
    if sw > 0:
        for i, (x, s) in enumerate(((150, 0.62), (480, 0.74), (1240, 0.8), (1560, 0.66), (1820, 0.72))):
            prop(cr, "yb_swordleaf", x - sp * (t - tT) * 0.5,
                 FL + 8 + 500 * (1 - ease(sw)), s, alpha=clamp(sw * 2), flip=i % 2 == 1)
    if sa > 0:
        dry_ground(cr, t, sp, sa, (1.0, 0.72, 0.36), FL - 6)
        for i in range(9):
            hx = scroll_x(80 + 230 * i, t, sp, 2070, 120)
            cr.new_path()
            pc.ell(cr, hx, FL + 2, 120, 22)
            cr.set_source_rgba(0.98, 0.74, 0.42, 0.9 * sa)
            cr.fill_preserve()
            cr.set_source_rgba(*INK, 0.6 * sa)
            cr.set_line_width(3)
            cr.stroke()
            u = (t * 0.9 + i * 0.31) % 1.0
            cr.new_path()
            for k in range(6):
                (cr.move_to if k == 0 else cr.line_to)(hx + 10 * math.sin(k + t * 5 + i), FL - 24 - 80 * u - 14 * k)
            cr.set_source_rgba(1.0, 0.96, 0.88, 0.7 * sa * math.sin(math.pi * u))
            cr.set_line_width(6)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.stroke()
    dry_ground(cr, t, sp, 1 - sa)
    if th > 0:
        for i, x in enumerate((200, 560, 1240, 1560, 1840)):
            prop(cr, "yb_thorns", scroll_x(x, t, sp, 2200, 140), FL + 12 + 200 * (1 - ease(th)), 0.62 + 0.1 * (i % 2),
                 alpha=clamp(th * 2))
    hop = 0.0
    if th > 0.5:
        hop = abs(math.sin(t * 7.0)) * 46
    elif sa > 0.5:
        hop = abs(math.sin(t * 11.0)) * 28
    duck = sw
    trio(cr, t, x_dh, dmood="terrified" if (th > 0.5 or sa > 0.5 or sw > 0.5) else "sheepish",
         dkw=dict(feet=FL - hop, rot=0.3 * duck, front=mix((-0.25, -0.35), (-2.5, -0.7), duck),
                  backa=mix((0.35, -0.4), (-2.3, -0.8), duck)),
         d1=dict(rot=0.12 * duck), d2=dict(rot=0.12 * duck))
    if sw > 0:                                                 # a few blades in front of them (near, blurred)
        for i, x in enumerate((760, 1400)):
            prop(cr, "yb_swordleaf", x - sp * (t - tT) * 0.8, FL + 170 + 400 * (1 - ease(sw)), 0.8, alpha=0.9,
                 blur=6, flip=i % 2 == 0)

    def ui(cr):
        if t < tT:
            head2(cr, t, "ON THE WAY:", t0 + 0.05, "THORNS... HOT SAND...", tK)
        else:
            head2(cr, t, "THORNS... HOT SAND... AND A", tT - 0.15, "SWORD-LEAF FOREST", tT + 0.05, under=tJ + 0.2)
        for txt, tz, x in (("THORNS", tK, 1500), ("HOT SAND", tR, 1500), ("SWORD-LEAF FOREST", tT, 1440)):
            nxt = {"THORNS": tR, "HOT SAND": tT}.get(txt)
            tag(cr, t, tz + 0.1, txt, x, 400, 40, t_out=(nxt - 0.2) if nxt else None)
    return dict(ui=ui, eve=0.1 + 0.2 * sa, strip=1.0)


def s_w6(cr, t, tl, t0, t1):
    c = cues(tl, "w6")
    tG1, tU, tG2, tD, tC = c["G1"], c["U"], c["G2"], c["D"], c["C"]
    far_hills(cr, t, 0.0, 0.8)
    dry_ground(cr, t)
    x = 1180
    # down at G1, up at U, down again at G2 (and a little struggle at the end)
    fall = keyed_fall(t, [(tG1, 1.0), (tU, 0.0), (tG2, 1.0)])
    sc = clamp((t - tD) / 0.5)
    d1 = dict(mood="scold" if t > tD - 0.2 else None, front=mix((-1.25, -0.25), (-1.9, 0.1), sc),
              hits=[(tC, 0.5)])
    h = DH_H + 40
    s = h / 1052.0
    rot = 1.42 * fall
    hip_y = FL - 434 * s * (1 - fall) - 70 * s * fall
    feet = hip_y + 434 * s
    out = trio(cr, t, x, walk=0.0, h=h, gap=300, dmood="terrified" if fall > 0.3 else "crying",
               dkw=dict(feet=feet, rot=rot, front=mix((-0.25, -0.35), (-2.6, -0.3), fall),
                        backa=mix((0.35, -0.4), (-2.4, -0.2), fall), legs=(0.2 * fall, -0.1 * fall)),
               d1=d1, d2=dict(mood="scold" if t > tC else None))
    for tf in (tG1, tG2):
        dust(cr, t, tf + 0.22, x + 200, FL, 1.0, 1.2)
    dev_d1 = out["d1"].get("top", (500, 300))

    def ui(cr):
        if t < tD:
            big = "FELL!" if t < tU else ("FELL... GOT UP..." if t < tG2 else "FELL... GOT UP... FELL!")
            tb = tG1 if t < tU else (tU if t < tG2 else tG2)
            head2(cr, t, "DHANIRAM...", t0 + 0.05, big, tb)
        else:
            head2(cr, t, "AND FROM BEHIND, THE MESSENGERS:", tD - 0.1, None, 0.0)
        cloud_text(cr, t, dev_d1[0] + 300, dev_d1[1] - 20, 0.56, [("KEEP", 70, INK, -44, tC - 0.05),
                                                                  ("WALKING!", 80, RED, 46, tC + 0.15)],
                   t_in=tC - 0.25)
    return dict(ui=ui, flash=flash_at(t, tG1 + 0.2, 0.12) + flash_at(t, tG2 + 0.2, 0.12), strip=1.0)


def keyed_fall(t, keys, down=0.3, up=0.45):
    """0 standing .. 1 lying flat: falls are quick, getting up is slower."""
    v = 0.0
    for tk, val in keys:
        if t < tk:
            break
        d = down if val > v else up
        v = v + (val - v) * ease((t - tk) / d)
    return clamp(v)


def s_w7(cr, t, tl, t0, t1):
    c = cues(tl, "w7")
    tS, tA, tP, tN = c["S"], c["A"], c["P"], c["N"]
    gx = 1480
    rise = ease((t - tP + 0.3) / 0.8) if t > tP - 0.3 else 0.0
    sp = 160.0 * (1 - prog(t, tP, 0.8))
    far_hills(cr, t, sp, 0.8)
    if rise > 0:
        glow(cr, gx, FL - 260, 520, 0.5 * rise)
        aura(cr, t, gx, FL - 260, 120, 420, 0.25 * rise, n=16, spin=0.04)
        prop(cr, "gp_gate", gx, FL + 6 + 300 * (1 - rise), 0.62, alpha=clamp(rise * 1.5))
    dry_ground(cr, t, sp)
    trio(cr, t, 860, walk=1 - prog(t, tP + 0.3, 0.5), dmood="sheepish" if t < tP else "shocked")
    days = [tS + 0.2 + 0.28 * k for k in range(4)]
    dev_g = cr.user_to_device(gx, FL - 420)

    def ui(cr):
        if t < tP:
            head2(cr, t, "AFTER 17 DAYS OF WALKING,", t0 + 0.05, "ON DAY 18", tA)
        else:
            head2(cr, t, "DAY 18:", tP - 0.15, "THE FIRST CITY", tP + 0.05)
        if t < tP + 0.2:
            k = sum(1 for d in days if t >= d)
            if t >= tA:
                counter_badge(cr, t, tA, "DAY 18", 1480, 420, 96)
                red_ring(cr, 1480, 420, 190, 80, prog(t, tA + 0.15, 0.4), 8, 1 - prog(t, tP, 0.2))
            elif k:
                counter_badge(cr, t, days[k - 1], f"DAY {13 + k}", 1480, 420, 96)
        tag(cr, t, tN, "SAUMYA NAGAR", dev_g[0], dev_g[1] - 40, 44)
    return dict(ui=ui, flash=flash_at(t, tP, 0.2) + flash_at(t, tN, 0.12), strip=1.0)


# ------------------------------------------------------------------ the shots: the sixteen cities


BANYAN = (1440, 0.62)                # the banyan at Saumya: x, scale
SIT = (1210, 300)                    # Dhaniram sitting under it: x, height
THOUGHT = (1340, 440, 600, 250)      # Dhaniram's thought cloud over Saumya: x, y, w, h
SIT_LEGS = (-1.45, -1.35)            # legs straight out in front (sitting)


def sit_feet(h, ground=FL, lift=60.0):
    """The `feet` to pass for a soul sitting on the ground with its legs straight out (hip `lift` units up)."""
    s = h / 1052.0
    return ground - lift * s + 434 * s


def saumya_set(cr, t, a=1.0):
    """Saumya: far hills, a pretty blue river with lotuses, the floor, the banyan."""
    far_hills(cr, t, 0.0, 0.7 * a, (0.50, 0.56, 0.36), FL - 220)
    blue_river(cr, t, FL - 190, FL - 120, a)
    ground_line(cr, a)
    bx, bs = BANYAN
    prop(cr, "yb_banyan", bx, FL + 8, bs, rot=sway(t, 0.003, 0.3), alpha=a)


def safe_icon(cr, x, y, s):
    """Dhaniram's safe (yy_cast), door open on its gold, for a thought cloud (s: about 0.5)."""
    YC.safe(cr, x, y + 230 * s, s * 0.95, open_=0.7)


def sitting_dh(cr, t, mood, a=1.0, front=(-1.0, -1.7), backa=(-0.8, -1.8), head=0.12, shiver=0.0):
    x, h = SIT
    return dh(cr, t, x, sit_feet(h), h, mood=mood, flip=True, legs=SIT_LEGS, front=front, backa=backa, head=head,
              alpha=a, shiver=shiver)


def thought_bubbles(cr, t, times, src, pops=(None, None, None)):
    """Dhaniram's thought cloud: his safe, his house, his son, popping in one by one (and bursting when mocked)."""
    x, y, w, h = THOUGHT
    items = [(times[0], pops[0], -180, lambda c_, cx, cy: safe_icon(c_, cx, cy, 0.5)),
             (times[1], pops[1], 0, lambda c_, cx, cy: prop(c_, "dv_house", cx, cy + 72, 0.12)),
             (times[2], pops[2], 180, lambda c_, cx, cy: prop(c_, "gp_son_head_calm", cx + 12, cy + 62, 0.46))]
    thought_cloud(cr, t, times[0] - 0.3, x, y, w, h, (src[0] + 30, src[1] - 20), items,
                  t_out=(pops[2] + 0.3) if pops[2] is not None else None)


def s_c1(cr, t, tl, t0, t1):
    c = cues(tl, "c1")
    tN, tB, tBt, tR, tTj, tG, tBk = c["N"], c["B"], c["Bt"], c["R"], c["Tj"], c["G"], c["Bk"]
    t_out = min(max(t0 + 1.3, tN + 0.25), t0 + 2.2)
    sc = prog(t, t_out - 0.2, 0.5)
    saumya_set(cr, t, sc)
    # the messengers stand back on the left; Dhaniram trudges in and sits under the tree
    duta(cr, t, 190, hold="staff", front=(-0.45, -0.35), alpha=sc, ph=0.7)
    d1 = duta(cr, t, 420, hold=None, front=(-1.1, -0.3), alpha=sc, ph=0.2)
    x, h = SIT
    sat = prog(t, tBt - 0.2, 0.5)
    pts = {}
    if sat < 1:
        bob, rock, lp = walk_cycle(t, 0.4, 0.0, 1 - prog(t, tBt - 0.6, 0.4))
        xw = 900 + (x - 900) * prog(t, t_out, max(0.6, tBt - t_out - 0.4))
        pts = dh(cr, t, xw, FL + bob, h, mood="sheepish", alpha=sc * (1 - sat), legs=walk_legs(lp, 0.4),
                 front=(-0.25, -0.35))
    if sat > 0:
        crying = prog(t, tR, 0.3)
        pts = sitting_dh(cr, t, "crying" if t > tR else "sheepish", a=sat * sc,
                         front=mix((-0.2, -0.4), (-1.0, -1.75), crying), backa=mix((0.1, -0.3), (-0.8, -1.85), crying),
                         head=0.12 * crying)
    rope_to(cr, to_user(cr, d1["handF"]) if "handF" in d1 else None, neck_of(cr, pts), sag=150, w=6,
            loop=(0.07 * h, 0.03 * h), alpha=sc)
    if t > tR and "head" in pts:
        hd = to_user(cr, pts["head"])
        tears(cr, t, hd[0] - 30, hd[1] + 10, prog(t, tR, 0.4), side=-1)
        tears(cr, t + 0.4, hd[0] - 10, hd[1] + 14, prog(t, tR, 0.4), side=-1)
    chapter(cr, t, t0 - 0.3, t_out, "DAY 18", [[("THE", INK), ("16", RED), ("CITIES", INK)]], SOURCE)
    src = pts.get("top", (x, FL - 300))

    def ui(cr):
        if t > t_out:
            if t < tR:
                head2(cr, t, "A PRETTY RIVER, AND A", t_out + 0.05, "BANYAN TREE", max(tB, t_out + 0.2))
            else:
                big = "MY SAFE!" if t < tG else ("MY SAFE! MY HOUSE!" if t < tBk else "MY SAFE! MY HOUSE! MY SON!")
                tb = tTj if t < tG else (tG if t < tBk else tBk)
                head2(cr, t, "HE SAT DOWN AND CRIED:", tR - 0.1, big, tb)
            thought_bubbles(cr, t, (tTj, tG, tBk), src)
    return dict(ui=ui, flash=flash_at(t, t_out, 0.15), strip=1.0)


def s_c2(cr, t, tl, t0, t1):
    c = cues(tl, "c2")
    c1 = cues(tl, "c1")
    tL, tD, tB, tY, tK = c["L"], c["D"], c["B"], c["Y"], c["K"]
    saumya_set(cr, t)
    laugh = tD - 0.3 < t < tY + 0.2
    # two townsfolk come up behind the messengers; everyone laughs at him
    for i, (rig, key, x) in enumerate(((DV.BFA, "dv_bfa", 640), (DV.KFA, "dv_kfa", 800))):
        b_, k_, a_ = pc.depth(t, tL - 0.2 + 0.2 * i, 0.5)
        shake = 0.04 * math.sin(t * 16 + i) * laugh
        body(cr, rig, key, t, x, 0.4 * k_, front=(-1.3, -0.4), backa=(0.4, -1.6), rot=shake, alpha=0.9 * a_,
             blur=4 + b_, ph=i)
    shake = 0.05 * math.sin(t * 15) if laugh else 0.0
    d2 = duta(cr, t, 190, hold="staff", front=(-0.45, -0.35), mood="laugh" if laugh else None, rot=shake, ph=0.7,
              backa=(0.4, -1.7) if laugh else (0.3, -0.3))
    point = prog(t, tD - 0.3, 0.3)
    d1 = duta(cr, t, 420, hold=None, front=mix((-1.1, -0.3), (-1.55, 0.0), point), mood="laugh" if laugh else None,
              rot=-shake, ph=0.2)
    x, h = SIT
    pts = sitting_dh(cr, t, "crying" if t < tD else "shocked", front=(-1.0, -1.75), backa=(-0.8, -1.85),
                     head=0.12 if t < tD else -0.05)
    rope_to(cr, to_user(cr, d1["handF"]) if "handF" in d1 else None, neck_of(cr, pts), sag=150, w=6,
            loop=(0.07 * h, 0.03 * h))
    if t < tD and "head" in pts:
        hd = to_user(cr, pts["head"])
        tears(cr, t, hd[0] - 30, hd[1] + 10, 1.0, side=-1)
    src = pts.get("top", (x, FL - 300))
    dev_d = d1.get("top", (420, 300))
    dev_d2 = d2.get("top", (190, 300))

    def ui(cr):
        if t < tY:
            head2(cr, t, "THE TOWNSFOLK AND THE MESSENGERS LAUGHED:", t0 + 0.05, None, 0.0)
        else:
            head2(cr, t, "HERE, ONLY", tY - 0.1, "YOUR KARMA WORKS", tK, under=tK + 0.5)
        thought_bubbles(cr, t, (c1["Tj"], c1["G"], c1["Bk"]), src, pops=(tD + 0.3, tD + 0.5, tB + 0.3))
        out_q = prog(t, tY - 0.2, 0.25)
        if t < tB:
            cloud_text(cr, t, 770, 400, 0.56, [("WHERE IS YOUR", 60, INK, -40, tD - 0.1),
                                             ("WEALTH NOW?", 80, RED, 48, tD + 0.15)], t_in=tD - 0.3)
        else:
            cloud_text(cr, t, 770, 400, 0.56, [("WHERE ARE", 64, INK, -40, tB - 0.1),
                                             ("YOUR SONS?", 80, RED, 48, tB + 0.15)], t_in=tB - 0.3,
                       alpha=1 - out_q)
        if laugh:
            ha_ha(cr, t, dev_d[0] - 40, dev_d[1] - 10, 1.0)
            ha_ha(cr, t, dev_d2[0] - 40, dev_d2[1] - 10, 0.9, ph=0.4)
    return dict(ui=ui, flash=flash_at(t, tD, 0.12) + flash_at(t, tK, 0.15), strip=1.0)


def s_c3(cr, t, tl, t0, t1):
    c = cues(tl, "c3")
    tK, tBc, tR, tKh, tBh = c["K"], c["Bc"], c["R"], c["Kh"], c["Bh"]
    sp = 130.0
    far_hills(cr, t, sp, 0.8)
    dry_ground(cr, t, sp)
    trio(cr, t, 820, dmood="sheepish")
    cx, cy = 1450, 520

    def ui(cr):
        if t < tR:
            head2(cr, t, "ON A JOURNEY, YOU CARRY", t0 + 0.05, "FOOD", tK)
        else:
            head2(cr, t, "BUT ON THIS ROAD:", tR - 0.1, "NO BUYING. NO SELLING.", tKh, under=tBh + 0.3)
        a = icon_card(cr, t, tK - 0.2, cx, cy, 560, 400, t_out=tR - 0.2)
        if a > 0:
            yy = card_y(t, tK - 0.2, cy)
            prop(cr, "gp_leaf", cx - 60, yy + 50, 0.62, alpha=a)
            for i in range(4):
                pinda(cr, cx - 180 + 80 * i, yy + 20 - 30 * (i % 2), 0.6, alpha=a * prog(t, tK + 0.1 * i, 0.25))
            prop(cr, "md_kalasha", cx + 150, yy + 80, 0.36, alpha=a)
            draw_text(cr, "FOOD FOR THE JOURNEY", cx, yy - 140, 36, INK, a, MONO_FONT, "cm", tracking=2)
            green_tick(cr, cx + 210, yy - 60, 70, prog(t, tK + 0.4, 0.3), a)
            plate(cr, t, tBc, "EVEN KIDS KNOW!", cx, yy + 150, 34, color=RED, alpha=a)
        a = icon_card(cr, t, tR - 0.1, cx, cy, 560, 420)
        if a > 0:
            yy = card_y(t, tR - 0.1, cy)
            cr.save()
            cr.rectangle(cx - 270, yy - 200, 540, 400)
            cr.clip()
            prop(cr, "dv_stall_back", cx, yy + 180, 0.33, alpha=a)
            for i in range(4):
                prop(cr, "sb_coin", cx - 90 + 60 * i, yy + 120 - 14 * (i % 2), 1.0, alpha=a)
            cr.restore()
            big_x(cr, cx, yy, 380, 300, prog(t, tKh, 0.3), a, lw=26)
    return dict(ui=ui, flash=flash_at(t, tKh, 0.15), strip=1.0)


def s_c4(cr, t, tl, t0, t1):
    c = cues(tl, "c4")
    tP, tK, tD = c["P"], c["K"], c["D"]
    far_hills(cr, t, 0.0, 0.6)
    dry_ground(cr, t, 0.0, 0.8)
    x, h = 640, 560
    glow(cr, x, FL - 300, 500, 0.45)
    lights(cr, t, x, FL - 300, 260, 6, 0.3, (1.0, 0.9, 0.6), 0.15)
    think = prog(t, tP - 0.2, 0.6)
    pts = dh(cr, t, x, FL, h, mood="sheepish" if t < tK else "crying", head=0.16 * think,
             front=mix((-0.25, -0.35), (-0.55, -2.0), think), backa=(0.3, -0.25), glow=0.6)
    src = pts.get("top", (x, FL - 560))

    def regret(c_, bx, by, r):
        k = r / 200
        u = ease((t - tD) / 1.0) if t > tD else 0.0
        cx0, cx1 = bx - 110 * k, bx + 110 * k
        cy = by + 10 * k
        dotted(c_, [(cx0, cy - 40 * k), (bx, cy - 110 * k), (cx1, cy - 40 * k)], prog(t, tK + 0.3, 0.5), 18 * k,
               4.5 * k, (0.55, 0.36, 0.16), 0.9)
        prop(c_, "dv_bowl", cx1, cy + 50 * k, 1.2 * k, alpha=0.9)
        px = cx0 + (cx1 - cx0) * u
        py = cy - 30 * k - 90 * k * math.sin(math.pi * u)
        prop(c_, "sb_coin", px, py, 1.9 * k, alpha=0.55 + 0.45 * (1 - u))
        if u >= 1:
            sparkle(c_, cx1, cy + 10 * k, 50 * k, 0.8)

    def ui(cr):
        head2(cr, t, "FOR THE FIRST TIME, DHANIRAM THOUGHT:", t0 + 0.05, "IF ONLY I HAD GIVEN...", tK,
              under=tD + 0.3)
        bubble(cr, t, tP, 1300, 560, 200, (src[0] + 60, src[1]), content=regret)
    return dict(ui=ui, night=0.12, lift=1.0, flash=flash_at(t, tK, 0.12), strip=1.0)


def c5_arrivals(tl):
    """When the two monthly rice-balls reach Dhaniram (c5)."""
    c = cues(tl, "c5")
    b = tl["c5"]
    end = b.start + b.dur + 0.3
    a1 = c["P"] + 1.3
    a2 = min(max(c["M"] + 0.4, a1 + 2.0), end - 0.2)
    return a1, max(a2, a1 + 0.6)


def s_c5(cr, t, tl, t0, t1):
    c = cues(tl, "c5")
    tP, tG, tM = c["P"], c["G"], c["M"]
    a1, a2 = c5_arrivals(tl)
    sp = 110.0
    far_hills(cr, t, sp, 0.8)
    prop(cr, "dv_house", 150, FL + 4, 0.22, alpha=0.8, blur=4)
    glow(cr, 150, FL - 120, 220, 0.4)
    dry_ground(cr, t, sp)
    x = 1240
    fed = sum(prog(t, a, 0.4) for a in (a1, a2))
    catching = any(a - 0.5 < t < a + 0.4 for a in (a1, a2))
    pts = trio(cr, t, x, gap=290, dmood="sheepish" if fed < 0.5 else "smug",
               dkw=dict(front=(-1.35, -0.5) if catching else (-0.25, -0.35), glow=1.0 + 0.6 * min(1.0, fed)))
    hand = to_user(cr, pts["dh"]["handF"]) if "handF" in pts["dh"] else (x + 60, FL - 150)
    for a in (a1, a2):
        ts = a - 1.6
        if not ts < t < a + 0.5:
            continue
        u = clamp((t - ts) / 1.6)
        arc = [(160 + (hand[0] - 160) * v, FL - 200 + (hand[1] - FL + 200) * v - 420 * math.sin(math.pi * v))
               for v in (ease(u) * i / 12 for i in range(13))]
        px, py = arc[-1]
        k = 1 - prog(t, a, 0.4)
        dotted(cr, arc, 1.0, 22, 4.0, (1.0, 0.85, 0.45), 0.7 * k)
        glow(cr, px, py, 190, 0.8 * k)
        warm(cr, px, py, 90, 0.8 * k, (1.0, 0.85, 0.45))
        aura(cr, t, px, py, 40, 95, 0.5 * k, n=10, spin=0.4)
        pinda(cr, px, py, 0.75 * (0.6 + 0.4 * k), alpha=k)
        if t > a:
            burst(cr, t, hand[0], hand[1], a, n=12, rmax=260, alpha=0.7)

    def ui(cr):
        if t < tM:
            head2(cr, t, "ALL HE HAD TO EAT:", t0 + 0.05, "RICE-BALLS", tP)
        else:
            head2(cr, t, "OFFERED AT HOME", tM - 0.2, "EVERY MONTH", tM, under=tM + 0.5)
        plate(cr, t, tG - 0.1, "FROM HOME", 210, FL - 330, 32)
        if t > a2 - 0.05:
            counter_badge(cr, t, a2, "MONTH 2", 1560, 420, 80)
        elif t > a1 - 0.05:
            counter_badge(cr, t, a1, "MONTH 1", 1560, 420, 80)
    return dict(ui=ui, flash=flash_at(t, a1, 0.15) + flash_at(t, a2, 0.15), strip=1.0)


def dark_city(cr, t, a=1.0, col=(0.30, 0.30, 0.40), x=960, s=1.05, blur=6):
    """A city skyline behind the scene, darkened."""
    if a <= 0.01:
        return
    prop(cr, "dv_city", x, FL - 40, s, alpha=0.7 * a, blur=blur)
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.rectangle(0, 0, W, FL)
    cr.set_source_rgba(*col, 0.5 * a)
    cr.fill()
    cr.restore()


def s_c6(cr, t, tl, t0, t1):
    c = cues(tl, "c6")
    tN, tM, tR, tD, tH = c["N"], c["M"], c["R"], c["D"], c["H"]
    dark_city(cr, t)
    dry_ground(cr, t, 0.0, 1.0, (0.55, 0.52, 0.60))
    kx, ks = 1460, 0.6
    b_, k_, a_ = pc.depth(t, tM - 0.3, 0.7)
    glow(cr, kx, FL - 380, 560, 0.55 * a_)
    aura(cr, t, kx, FL - 420, 140, 520, 0.3 * a_, n=18, spin=0.02, col=(0.62, 0.70, 0.95))
    lean = keyed_fall(t, [(tD, 1.0)], 0.5)
    jang(cr, t, kx, ks * k_, flip=True, front=mix((-0.4, -0.5), (-1.45, -0.2), lean), backa=(0.25, -0.35),
         alpha=a_, blur=b_, rot=-0.06 * lean, ph=0.4)
    # Dhaniram: shocked at the sight, then he gives up: his knees give way and he sinks to the ground
    col = keyed_fall(t, [(tH - 0.1, 1.0)], 0.7)
    h = DH_H + 20
    feet = FL * (1 - col) + sit_feet(h) * col
    legs = (SIT_LEGS[0] * col, SIT_LEGS[1] * col)
    trio(cr, t, 840, walk=1 - prog(t, tM, 0.4), h=h, gap=280, dmood="shocked" if t < tH else "terrified",
         dkw=dict(feet=feet, legs=legs, head=0.25 * col, shiver=0.6 * prog(t, tD, 0.3) * (1 - col),
                  front=mix((-0.25, -0.35), (-0.1, -0.2), col), backa=mix((0.35, -0.4), (0.1, -0.1), col)))

    def ui(cr):
        if t < tD:
            head2(cr, t, "THE NEXT CITY'S KING LOOKED LIKE", t0 + 0.05, "DEATH", tM, under=tR)
        else:
            head2(cr, t, "ONE LOOK, AND DHANIRAM", tD - 0.1, "GAVE UP", tH, under=tH + 0.4)
    return dict(ui=ui, night=0.25, lift=1.0, cool=0.35, flash=flash_at(t, tM, 0.2), strip=1.0)


DODGE = (820, 1060)                  # Dhaniram's two spots while the stones fall
DODGE_STEP = 0.55


def dodge_at(t, t_a):
    """(x, hop, k): Dhaniram hopping between his two spots every DODGE_STEP s from t_a."""
    if t < t_a:
        return DODGE[0], 0.0, -1
    k = int((t - t_a) / DODGE_STEP)
    f = (t - t_a - k * DODGE_STEP) / DODGE_STEP
    xa, xb = DODGE[k % 2], DODGE[(k + 1) % 2]
    m = clamp(f / 0.45)
    return xa + (xb - xa) * ease(m), 50 * math.sin(math.pi * m) * (f < 0.45), k


def stone(cr, x, y, r, rot=0.0, a=1.0, seed=0):
    """A falling stone: a lumpy grey-brown pebble, inked, with a pale chip of light."""
    if a <= 0.01 or r < 1:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    n = 9
    pts = [(r * (0.82 + 0.22 * math.sin(seed * 1.7 + i * 2.3)) * math.cos(2 * math.pi * i / n),
            r * (0.72 + 0.2 * math.cos(seed * 1.3 + i * 1.9)) * math.sin(2 * math.pi * i / n)) for i in range(n)]
    cr.new_path()
    pc.spath(cr, pts)
    cr.set_source_rgba(0.62, 0.56, 0.50, a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(max(2.0, 0.12 * r))
    cr.stroke()
    cr.new_path()
    pc.ell(cr, -0.3 * r, -0.3 * r, 0.25 * r, 0.14 * r, -0.5)
    cr.set_source_rgba(0.92, 0.88, 0.80, 0.8 * a)
    cr.fill()
    cr.restore()


def s_c7(cr, t, tl, t0, t1):
    c = cues(tl, "c7")
    tC, tA, tP = c["C"], c["A"], c["P"]
    far_hills(cr, t, 0.0, 1.0, (0.50, 0.46, 0.44), FL - 30)
    dry_ground(cr, t, 0.0, 1.0, (0.70, 0.64, 0.58))
    tdg = min(tA - 0.1, t0 + 0.9)
    x, hop, kk = dodge_at(t, tdg)
    duta(cr, t, 200, hold="staff", front=(-0.45, -0.35), ph=0.7)
    d1 = duta(cr, t, 450, hold=None, front=(-1.1, -0.3), ph=0.2)
    up = t > tdg
    pts = dh(cr, t, x, FL - hop, DH_H, mood="terrified" if up else "shocked",
             front=(-2.75, -0.95) if up else (-0.25, -0.35), backa=(-2.55, -1.05) if up else (0.35, -0.4),
             flip=kk % 2 == 0 and kk >= 0)
    rope_to(cr, to_user(cr, d1["handF"]) if "handF" in d1 else None, neck_of(cr, pts), sag=60, w=6,
            loop=(0.05 * DH_H, 0.022 * DH_H))
    # stones fall like hail: each lands where he stood a moment ago (he has just hopped away), bounces and rests
    for k in range(int(max(0.0, t1 - tdg) / DODGE_STEP) + 2):
        t_land = tdg + DODGE_STEP * (k + 0.62)
        for j in range(2):
            land_x = DODGE[k % 2] + (-50 + 100 * j) + 30 * math.sin(k * 1.7 + j)
            tl_j = t_land + 0.12 * j
            u = (t - (tl_j - 0.6)) / 0.6
            if u < 0:
                continue
            r = 22 + 8 * ((k + j) % 3)
            if u < 1:
                sx, sy, rot = land_x - 60 * (1 - u), FL - 900 * (1 - u * u) - r, t * 4 + k
                a = 1.0
            else:
                v = t - tl_j
                if v > 1.6:
                    continue
                sx = land_x + 30 * min(v, 0.4) * (1 if j else -1)
                sy = FL - r - 50 * math.sin(math.pi * min(1.0, v / 0.4)) * (v < 0.4)
                rot = tl_j * 4 + k
                a = 1.0 - prog(t, tl_j + 1.2, 0.4)
                dust(cr, t, tl_j, land_x, FL, 1.0, 0.5)
            stone(cr, sx, sy + 6, r, rot, a, k * 3 + j)
    for i in range(10):                                  # far stones raining across the sky
        if t > tdg - 0.4:
            u = ((t - tdg + 0.4) * 1.2 + i / 10) % 1.0
            stone(cr, 120 + 175 * i + 40 * math.sin(i), 250 + 600 * u, 9 + 3 * (i % 3), t * 3 + i,
                  0.7 * math.sin(math.pi * u), i)

    def ui(cr):
        head2(cr, t, "MONTH 4:", t0 + 0.05, "IT RAINED STONES!", min(tP, tdg + 0.4))
        counter_badge(cr, t, tC, "MONTH 4", 1560, 430, 84)
    return dict(ui=ui, flash=flash_at(t, tC, 0.12) + flash_at(t, tP, 0.12), strip=1.0, cool=0.12)


PANELS = ((390, "CRYING EVERYWHERE"), (960, "SCORCHING HEAT"), (1530, "CLOUDS, CLOUDS"))
PANEL_Y, PANEL_W, PANEL_H = 560, 500, 440


def panel(cr, t, t_in, k, alpha=1.0):
    """One framed city panel of the c8 montage (k = 0 crying, 1 heat, 2 clouds), dropping in on its rods."""
    x, label = PANELS[k]
    q = pop(t, t_in, 0.4, 1.3)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    y = PANEL_Y + 60 * (1 - clamp(q))
    w, h = PANEL_W, PANEL_H
    pc.rod(cr, x - 150, y + h / 2, x - 130, H + 60, alpha=0.5 * a)
    pc.rod(cr, x + 150, y + h / 2, x + 170, H + 60, alpha=0.5 * a)
    cr.save()
    cr.translate(x, y)
    cr.rotate(sway(t, 0.006, 0.4, k))
    cr.rectangle(-w / 2, -h / 2, w, h)
    cr.set_source_rgba(0.30, 0.17, 0.07, a)
    cr.fill()
    cr.rectangle(-w / 2 + 14, -h / 2 + 14, w - 28, h - 28)
    cr.clip()
    bg = ((0.70, 0.74, 0.86), (1.0, 0.70, 0.40), (0.62, 0.64, 0.70))[k]
    cr.set_source_rgba(*bg, a)
    cr.paint()
    gy = h / 2 - 70
    cr.rectangle(-w / 2, gy, w, 80)
    cr.set_source_rgba(0.62, 0.46, 0.30, a)
    cr.fill()
    if k == 0:
        prop(cr, "dv_city", 0, gy + 4, 0.3, alpha=a)
        for i in range(4):
            u = ((t - t_in) * 0.8 + i / 4) % 1.0
            cr.new_path()
            cr.arc(0, gy - 140, 40 + 200 * u, math.pi * 1.1, math.pi * 1.9)
            cr.set_source_rgba(0.20, 0.30, 0.55, 0.7 * a * (1 - u))
            cr.set_line_width(6)
            cr.stroke()
    elif k == 1:
        warm(cr, 0, -60, 260, 0.8 * a, (1.0, 0.5, 0.1))
        prop(cr, "sun", 0, -60, 0.42, rot=t * 0.4, alpha=a)
        heat(cr, t, a, -h / 2, gy)
    else:
        for i in range(5):
            cx = -180 + 95 * i + 20 * math.sin(t * 0.8 + i)
            prop(cr, "cloud", cx, -110 + 40 * (i % 2), 0.32, alpha=a)
        cr.set_source_rgba(0.30, 0.40, 0.60, 0.7 * a)
        cr.set_line_width(3)
        for i in range(16):
            rx = -220 + 28 * i
            u = (t * 1.6 + i * 0.37) % 1.0
            cr.move_to(rx, -60 + 200 * u)
            cr.line_to(rx - 8, -40 + 200 * u)
        cr.stroke()
    pts = dh(cr, t, -120 + 30 * math.sin(t * 0.6 + k), gy + 10, 110, mood="crying" if k == 0 else "sheepish",
             alpha=a, legs=walk_legs(math.sin(t * 6 + k), 0.35), glow=0.4)
    if k == 0 and "head" in pts:
        hd = to_user(cr, pts["head"])
        tears(cr, t, hd[0] + 8, hd[1] + 4, a, 1, 2)
    cr.restore()
    cr.save()
    cr.translate(x, y)
    cr.set_source_rgba(0.30, 0.17, 0.07, a)
    cr.set_line_width(10)
    cr.rectangle(-w / 2, -h / 2, w, h)
    cr.stroke()
    cr.restore()
    plate(cr, t, t_in + 0.25, label, x, y + h / 2 + 34, 32, color=RED)


def s_c8(cr, t, tl, t0, t1):
    c = cues(tl, "c8")
    tB, tN, tR, tT, tBd = c["B"], c["N"], c["R"], c["T"], c["Bd"]
    sp = 260.0
    walk_a = 1 - prog(t, tR - 0.6, 0.4)
    if walk_a > 0.01:                                   # months pass: they walk on, city gates slide by behind them
        far_hills(cr, t, sp, 0.8 * walk_a)
        for i in range(4):
            gx = scroll_x(300 + 640 * i, t, sp, 2560, 300)
            glow(cr, gx, FL - 200, 260, 0.25 * walk_a)
            prop(cr, "gp_gate", gx, FL + 4, 0.5, alpha=0.8 * walk_a, blur=2)
    dry_ground(cr, t, sp * walk_a, 0.8)
    if walk_a > 0.01:
        trio(cr, t, 1100, alpha=walk_a, dmood="sheepish")
    for k, tk in enumerate((tR - 0.15, tT - 0.15, tBd - 0.15)):
        panel(cr, t, tk, k)

    def ui(cr):
        head2(cr, t, "MONTHS PASSED...", t0 + 0.05, "CITY AFTER CITY", tN)
        if walk_a > 0.01:
            counter_badge(cr, t, tB, "MONTH 4", 1560, 430, 84, alpha=walk_a * (1 - prog(t, tN + 0.2, 0.15)))
            if t > tN + 0.2:
                counter_badge(cr, t, tN + 0.2, "MONTH 5", 1560, 430, 84, alpha=walk_a)
    return dict(ui=ui, flash=flash_at(t, tR, 0.1) + flash_at(t, tT, 0.1) + flash_at(t, tBd, 0.1), strip=1.0)


@functools.lru_cache(maxsize=2)
def dot_grid(spacing, r):
    """A sheet of small dark dots (the frame's size) for drawing a figure 'made of dots'."""
    s = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    c = cairo.Context(s)
    c.set_source_rgba(0.36, 0.22, 0.10, 1.0)
    j = 0
    y = spacing / 2
    while y < H:
        x = spacing / 2 + (spacing / 2 if j % 2 else 0)
        while x < W:
            c.new_sub_path()
            c.arc(x, y, r, 0, 2 * math.pi)
            x += spacing
        c.fill()
        y += spacing * 0.87
        j += 1
    return s


def ghost(cr, fn, a, spacing=12, r=3.4, faint=0.22):
    """Whatever fn(cr) draws, as a figure of dots only (with a faint shadow of itself): someone who isn't there."""
    if a <= 0.01:
        return
    cr.push_group()
    fn(cr)
    fig = cr.pop_group()
    cr.save()
    cr.set_source(fig)
    cr.paint_with_alpha(faint * a)
    cr.push_group()
    m = cr.get_matrix()
    cr.identity_matrix()
    cr.set_source_surface(dot_grid(spacing, r), 0, 0)
    cr.paint()
    cr.set_matrix(m)
    cr.set_operator(cairo.OPERATOR_DEST_IN)
    cr.set_source(fig)
    cr.paint()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def bhola_fig(cr, t, x, h):
    """Bhola standing with his water pot on his shoulder (yy_cast), h px tall."""
    YC.bhola(cr, t, x, h / (YC.DH_FEET + YC.BH_TOP), mood="smile", feet=FL, rods=False)


def s_c9(cr, t, tl, t0, t1):
    c = cues(tl, "c9")
    tB, tK, tR, tN = c["B"], c["K"], c["R"], c["N"]
    far_hills(cr, t, 0.0, 0.7, (0.56, 0.42, 0.30), FL - 300)
    cr.save()                                           # an empty road running into the distance
    pc.poly(cr, [(560, FL + 200), (1360, FL + 200), (1010, FL - 360), (910, FL - 360)])
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(0.86, 0.66, 0.40, 0.8)
    cr.fill()
    cr.restore()
    for sx in (-1, 1):
        dotted(cr, [(960 + sx * 400, FL + 200), (960 + sx * 50, FL - 360)], 1.0, 30, 4.5, (0.36, 0.22, 0.10), 0.7)
    flick = 0.75 + 0.25 * math.sin(t * 9) * math.sin(t * 2.3)
    gone = prog(t, tN, 0.8) * 0.6
    ghost(cr, lambda c_: bhola_fig(c_, t, 760, 520), prog(t, tB - 0.1, 0.4) * flick * (1 - gone))

    def ui(cr):
        if t < tR:
            head2(cr, t, "AND BHOLA?", t0 + 0.05, "WHERE WAS HE?", tK)
        else:
            head2(cr, t, "ON THIS WHOLE ROAD...", tR - 0.1, "NOT A TRACE OF HIM", tN, under=tN + 0.5)
        qmark(cr, t, tK, 1260, 520, 300)
        plate(cr, t, tB + 0.1, "BHOLA", 760, 300, 40, alpha=1 - 0.5 * gone)
    return dict(ui=ui, night=0.15, lift=1.0, flash=flash_at(t, tK, 0.15), strip=1.0)


# ------------------------------------------------------------------ the shots: the Vaitarani


def strange_city(cr, t, a=1.0):
    """Vichitra's strange city: coloured, crooked towers behind the scene."""
    prop(cr, "dv_city", 700, FL - 30, 0.9, alpha=0.6 * a, blur=5)
    prop(cr, "dv_city", 1520, FL - 50, 0.75, alpha=0.5 * a, blur=7, flip=True)
    for x, rot, s in ((330, -0.14, 0.44), (1130, 0.12, 0.36), (1780, -0.08, 0.4)):
        prop(cr, "gp_gate", x, FL - 10, s, rot=rot, alpha=0.55 * a, blur=4)
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    g = cairo.LinearGradient(0, 0, W, 0)
    g.add_color_stop_rgba(0, 0.78, 0.62, 0.95, 0.6 * a)
    g.add_color_stop_rgba(0.5, 0.62, 0.90, 0.80, 0.5 * a)
    g.add_color_stop_rgba(1, 0.95, 0.66, 0.80, 0.6 * a)
    cr.rectangle(0, 0, W, FL)
    cr.set_source(g)
    cr.fill()
    cr.restore()


def s_v1(cr, t, tl, t0, t1):
    c = cues(tl, "v1")
    tC, tA, tR, tV, tY, tB = c["C"], c["A"], c["R"], c["V"], c["Y"], c["B"]
    strange_city(cr, t, prog(t, tA - 0.6, 0.6) * 0.6 + 0.4)
    dry_ground(cr, t, 0.0, 1.0, (0.72, 0.60, 0.72))
    kx, ks = 1460, 0.6
    b_, k_, a_ = pc.depth(t, tR - 0.3, 0.6)
    glow(cr, kx, FL - 380, 520, 0.45 * a_)
    point = prog(t, tY, 0.3)
    kp = vich(cr, t, kx, ks * k_, flip=True, front=mix((-0.35, -1.6), (-1.35, -0.1), point), backa=(0.9, -1.9),
              alpha=a_, blur=b_, ph=0.5)
    bow = keyed_fall(t, [(tV, 1.0)], 0.4)
    trio(cr, t, 820, walk=1 - prog(t, tR - 0.4, 0.4), gap=280, dmood="sheepish" if t < tV else "terrified",
         dkw=dict(rot=0.35 * bow, front=mix((-0.25, -0.35), (-1.1, -1.15), bow),
                  backa=mix((0.35, -0.4), (-1.0, -1.2), bow)))
    dev_k = kp.get("top", (kx, 300))

    def ui(cr):
        if t < tY:
            head2(cr, t, "MONTH 6: A STRANGE CITY", t0 + 0.05, "ITS KING: VICHITRA", tV)
        else:
            head2(cr, t, "VICHITRA WAS", tY - 0.15, "YAMA'S YOUNGER BROTHER", tB, under=tB + 0.4)
        counter_badge(cr, t, tC, "MONTH 6", 1040, 420, 84)
        tag(cr, t, tV + 0.1, "KING VICHITRA", dev_k[0] - 30, dev_k[1] - 20, 36)
    return dict(ui=ui, flash=flash_at(t, tR, 0.15) + flash_at(t, tY, 0.12), strip=1.0)


V_TOP, V_BOT = 440, 840              # the Vaitarani's far bank and near edge


def vait_set(cr, t, a=1.0, top=V_TOP, bottom=V_BOT, boil=0.0, speed=1.0, near=True):
    """The Vaitarani: dim far hills, the dark-red river, the near bank."""
    far_hills(cr, t, 0.0, 0.6 * a, (0.46, 0.30, 0.30), top + 20)
    prop(cr, "ground", W / 2, top + 10, 1.2, alpha=0.5 * a, blur=2)
    river_band(cr, t, top, bottom, a, speed=speed, boil=boil)
    if near:
        dry_ground(cr, t, 0.0, a, (0.72, 0.50, 0.42))


def chapter_v(cr, t, tl):
    """The VAITARANI chapter card: rises as the river is named (v2), flies off early in v3."""
    c = cues(tl, "v2")
    t_in = max(c["t0"] + 0.1, c["V"] - 0.5)
    t_out = cues(tl, "v3")["t0"] + 0.7
    chapter(cr, t, t_in, t_out, "MONTH 6", [[("THE", INK), ("VAITARANI", RED)]], SOURCE)
    return t_in, t_out


def card_dim(t, tl):
    """0..1: how far the river dims while the VAITARANI chapter card is up (so the card reads)."""
    c = cues(tl, "v2")
    t_in = max(c["t0"] + 0.1, c["V"] - 0.5)
    t_out = cues(tl, "v3")["t0"] + 0.7
    return prog(t, t_in - 0.2, 0.4) * (1 - prog(t, t_out, 0.5))


def s_v2(cr, t, tl, t0, t1):
    c = cues(tl, "v2")
    tB, tV = c["B"], c["V"]
    vait_set(cr, t, prog(t, t0, 0.6) * (1 - 0.7 * card_dim(t, tl)))
    trio(cr, t, 600, walk=1 - prog(t, tB, 0.5), gap=230, dmood="shocked" if t > tB else "sheepish")
    t_in, _ = chapter_v(cr, t, tl)

    def ui(cr):
        if t < t_in + 0.1:
            head2(cr, t, "AND BEYOND THAT CITY FLOWED...", t0 + 0.05, None, 0.0)
    return dict(ui=ui, night=0.12, lift=1.0, flash=flash_at(t, tV, 0.25), strip=1.0, red=0.15)


CROCS = ((480, 640, 1, 0.34), (1120, 730, -1, 0.42), (1560, 560, 1, 0.28))
VULT_C = (1150, 330)


def s_v3(cr, t, tl, t0, t1):
    c = cues(tl, "v3")
    tS, tC, tP, tK, tM, tG = c["S"], c["C"], c["P"], c["K"], c["M"], c["G"]
    vait_set(cr, t, 1 - 0.7 * card_dim(t, tl))
    for i, (x, y, d, s) in enumerate(CROCS):
        q = prog(t, tM - 0.2 + 0.25 * i, 0.6)
        if q > 0.01:
            xx = x + d * 22 * (t - tM)
            cr.save()
            cr.rectangle(0, 0, W, y + 4)
            cr.clip()
            prop(cr, "yb_croc", xx, y + 50 * (1 - q), s, alpha=clamp(q * 1.5), flip=d < 0)
            cr.restore()
            for k in range(2):
                u = (t * 0.6 + k * 0.5 + i * 0.3) % 1.0
                cr.new_path()
                pc.ell(cr, xx, y + 4, (120 + 200 * u) * s / 0.34, (10 + 18 * u) * s / 0.34)
                cr.set_source_rgba(1.0, 0.7, 0.6, 0.5 * q * (1 - u))
                cr.set_line_width(3)
                cr.stroke()
    for i in range(3):
        q = prog(t, tG - 0.3 + 0.15 * i, 0.5)
        if q > 0.01:
            ang = t * 0.55 + i * 2.09
            prop(cr, "yb_vulture", VULT_C[0] + 420 * math.cos(ang), VULT_C[1] + 70 * math.sin(ang), 0.16,
                 rot=0.18 * math.sin(ang), alpha=0.9 * q, blur=1.5)
    trio(cr, t, 600, walk=0.0, gap=230, dmood="shocked" if t < tM else "terrified")
    ax = 1660
    from scenes_garuda_purana import arrow_v
    arrow_v(cr, ax, V_TOP + 14, V_BOT - 10, prog(t, tC - 0.1, 0.5))
    chapter_v(cr, t, tl)

    def ui(cr):
        if t < tM:
            head2(cr, t, "100 YOJANAS WIDE...", t0 + 0.05, "A RIVER OF DARK RED", tK)
        else:
            head2(cr, t, "BELOW, CROCODILES...", tM - 0.1, "ABOVE, VULTURES!", tG)
        plate(cr, t, tC + 0.2, "100 YOJANAS", ax - 150, (V_TOP + V_BOT) / 2, 32)
        plate(cr, t, tP, "NOT WATER...", 1160, 600, 40, color=RED, t_out=tM - 0.2)
    return dict(ui=ui, night=0.12, lift=1.0, flash=flash_at(t, tM, 0.12) + flash_at(t, tG, 0.12), strip=1.0,
                red=0.15)


BOAT = (1480, 0.42)                  # the moored boat: x, scale (its waterline at V_BOT)


def boatmen(cr, t, shake=0.0, ask=0.0):
    """The boat at the near edge with the boatman standing in it (pole in hand), a second fisherman on the bank.
    Returns the boatman's points (device)."""
    bx, bs = BOAT
    by = V_BOT + 8
    bob = 5 * math.sin(t * 2.0)
    glow(cr, bx, by - 200, 380, 0.4)
    hs = 0.42
    ang_front = mix((-1.6, -0.9), (-1.2, -0.5), ask)
    ex = {"dv_hus_armF_lo": held_grip("gp_pole", ang_front, 0.9, 0.2 + 0.05 * math.sin(t * 1.4), 150)}
    p = body(cr, DV.HUS, "dv_hus", t, bx - 120, hs, front=ang_front, backa=(-1.2, -1.2), flip=True,
             y=by + bob - 30 - 434 * hs, head=0.18 * math.sin(t * 12) * shake, extra=ex, rods=False, ph=0.8)
    prop(cr, "gp_boat", bx, by + bob, bs, rot=0.015 * math.sin(t * 1.3))
    glow(cr, 1760, FL - 220, 280, 0.45)
    body(cr, DV.VY, "dv_vy", t, 1760, 0.44, flip=True, front=(-0.6, -0.9), backa=(0.3, -0.3), ph=1.6)
    return p


def s_v4(cr, t, tl, t0, t1):
    c = cues(tl, "v4")
    tM, tN, tB, tP = c["M"], c["N"], c["B"], c["P"]
    vait_set(cr, t, 1.0, 470, V_BOT)
    b_, k_, a_ = pc.depth(t, tM - 0.3, 0.6)
    cr.save()
    cr.push_group()
    bp = boatmen(cr, t, ask=prog(t, tB, 0.3))
    cr.pop_group_to_source()
    cr.paint_with_alpha(a_)
    cr.restore()
    trio(cr, t, 640, walk=0.0, gap=260, dmood="shocked" if t < tB else "smug")
    dev_b = bp.get("top", (1360, 380))

    def ui(cr):
        head2(cr, t, "ON THE BANK, SOME FISHERMEN", t0 + 0.05, "WITH A BOAT", tN)
        cloud_text(cr, t, dev_b[0] - 330, dev_b[1] + 30, 0.48, [("WANT TO", 66, INK, -40, tB),
                                                                 ("CROSS?", 92, RED, 48, tP)], flip=True, t_in=tB - 0.2)
    return dict(ui=ui, night=0.1, lift=1.0, flash=flash_at(t, tN, 0.12), strip=1.0, red=0.12)


def fake_coins(cr, t, x, y, a=1.0):
    """Coins that aren't there: dotted gold outlines glinting over his hand."""
    if a <= 0.01:
        return
    for i in range(3):
        cx, cy = x + 40 * (i - 1), y - 40 - 30 * (i % 2) + 6 * math.sin(t * 5 + i)
        cr.save()
        cr.set_dash([0.1, 9])
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_width(5)
        cr.arc(cx, cy, 24, 0, 2 * math.pi)
        cr.set_source_rgba(1.0, 0.80, 0.25, a)
        cr.stroke()
        cr.restore()
        sparkle(cr, cx + 14, cy - 12, 16 + 6 * math.sin(t * 7 + i), a)


def s_v5(cr, t, tl, t0, t1):
    c = cues(tl, "v5")
    tK, tH, tP = c["K"], c["H"], c["P"]
    vait_set(cr, t, 1.0, 470, V_BOT)
    bp = boatmen(cr, t)
    step = prog(t, tK - 0.2, 0.7)
    x = 640 + 200 * ease(step)
    rub = 0.12 * math.sin(t * 16) * (t > tH - 0.2)
    out = trio(cr, t, x, walk=0.6 * (0 < step < 1), gap=260, dmood="smug" if t < tP else "talking",
               dkw=dict(front=(-1.45 + rub, -0.9), backa=(0.35, -0.4), hand="point"))
    hand = out["dh"].get("handF")
    dev_dh = out["dh"].get("top", (x, 600))
    del bp

    def ui(cr):
        head2(cr, t, "DHANIRAM WAS THRILLED:", t0 + 0.05, "HOW MUCH?", tP)
        if hand and t > tH - 0.2:
            fake_coins(cr, t, hand[0] + 10, hand[1], prog(t, tH - 0.2, 0.3))
        cloud_text(cr, t, dev_dh[0] + 120, dev_dh[1] - 230, 0.5, [("YES, YES!", 70, INK, -42, tH),
                                                                  ("HOW MUCH?", 80, RED, 44, tP)], t_in=tH - 0.25)
    return dict(ui=ui, night=0.1, lift=1.0, flash=flash_at(t, tP, 0.12), strip=1.0, red=0.12)


COWCARD = (930, 430, 720, 300)       # the gift-cow card: x, y, w, h


def cow_card(cr, t, t1_, t2_, alpha=1.0):
    """GAVE A COW? -> BOAT (tick); NO COW? -> NO BOAT (cross)."""
    from scenes_garuda_purana import cow_badge
    x, y, w, h = COWCARD
    a = icon_card(cr, t, t1_ - 0.15, x, y, w, h)
    if a <= 0:
        return
    yy = card_y(t, t1_ - 0.15, y)
    for row, (tt, label, empty) in enumerate(((t1_, "GAVE A COW?", False), (t2_, "NO COW?", True))):
        q = prog(t, tt, 0.3) * a
        if q <= 0.01:
            continue
        ry = yy - 62 + 128 * row
        cow_badge(cr, t, tt, x - 290, ry, 50, empty=empty, alpha=a)
        draw_text(cr, label, x - 222, ry, 46, INK, q, anchor="lm")
        arrow_r(cr, x + 40, x + 120, ry, prog(t, tt + 0.2, 0.3), q)
        prop(cr, "gp_boat", x + 220, ry + 22, 0.15, alpha=q)
        if row == 0:
            green_tick(cr, x + 300, ry - 6, 54, prog(t, tt + 0.45, 0.3), q)
        else:
            big_x(cr, x + 220, ry, 200, 90, prog(t, tt + 0.45, 0.3), q, lw=14)


def s_v6(cr, t, tl, t0, t1):
    c = cues(tl, "v6")
    tP, tN, tG, tNv, tV = c["P"], c["N"], c["G"], c["Nv"], c["V"]
    vait_set(cr, t, 1.0, 470, V_BOT)
    bp = boatmen(cr, t, shake=1.0 if tP - 0.2 < t < tN + 0.8 else 0.0)
    drop = prog(t, tN, 0.4)
    out = trio(cr, t, 840, walk=0.0, gap=260, dmood="smug" if t < tP else "shocked",
               dkw=dict(front=mix((-1.45, -0.9), (-0.25, -0.35), drop), backa=(0.35, -0.4), hand="point"))
    hand = out["dh"].get("handF")
    dev_b = bp.get("top", (1360, 380))

    def ui(cr):
        if t < tG:
            head2(cr, t, "THE FISHERMEN SAID:", t0 + 0.05, "MONEY DOESN'T WORK HERE", tN)
        else:
            head2(cr, t, "ONLY ONE THING WORKS HERE:", tG - 0.15, "A GIFTED COW", tG + 0.05)
        if hand and t < tN + 0.6:
            a = 1 - prog(t, tN + 0.3, 0.3)
            fake_coins(cr, t, hand[0] + 10, hand[1], a)
            big_x(cr, hand[0] + 10, hand[1] - 50, 170, 120, prog(t, tN - 0.1, 0.25), a, lw=16)
        cloud_text(cr, t, dev_b[0] - 360, dev_b[1] + 30, 0.48, [("MONEY DOESN'T", 58, INK, -40, tP),
                                                                 ("WORK HERE!", 82, RED, 48, tN)], flip=True,
                   t_in=tP - 0.25, alpha=1 - prog(t, tG - 0.35, 0.25))
        cow_card(cr, t, tG, max(tV, tNv + 0.4))
    return dict(ui=ui, night=0.1, lift=1.0, flash=flash_at(t, tG, 0.12), strip=1.0, red=0.12)


def s_v7(cr, t, tl, t0, t1):
    c = cues(tl, "v7")
    tV, tVt, tD, tP, tV2 = c["V"], c["Vt"], c["D"], c["P"], c["V2"]
    vait_set(cr, t, 0.45, 470, V_BOT)
    trio(cr, t, 600, walk=0.0, gap=230, dmood="sheepish", alpha=0.6)

    def ui(cr):
        head2(cr, t, "WHAT DOES THE NAME MEAN?", t0 + 0.05, None, 0.0)
        a = icon_card(cr, t, t0 + 0.1, 960, 580, 1160, 440)
        if a <= 0.01:
            return
        y = card_y(t, t0 + 0.1, 580)
        # the river's name first, with a big ?; then वितरण = GIVING; then the ? turns into CROSSED BY GIVING
        rows = ((y + 105, WORD["vaitarani"], tV + 0.15, "= CROSSED BY GIVING", tP + 0.1, 66),
                (y - 95, WORD["vitaran"], tVt, "= GIVING", tD, 84))
        for ry, word, tw, eng, te, esz in rows:
            p = prog(t, tw, 0.3) * a
            if p > 0.01:
                if HAS_INDIC:
                    su = indic(word, 104, INK)
                    k = 1.15 - 0.15 * back(clamp((t - tw) / 0.3))
                    cr.save()
                    cr.translate(700, ry)
                    cr.scale(k, k)
                    cr.set_source_surface(su, -su.get_width() / 2, -su.get_height() / 2)
                    cr.paint_with_alpha(p)
                    cr.restore()
                else:
                    draw_text(cr, word, 700, ry, 90, INK, p, anchor="cm")
            p2 = prog(t, te, 0.3) * a
            if p2 > 0.01:
                draw_text(cr, eng, 870, ry + 4, esz, RED, p2, anchor="lm")
        q = pop(t, tV + 0.4, 0.3, 1.8) * (1 - prog(t, tP - 0.1, 0.2))
        if q > 0.01:
            draw_text(cr, "= ?", 870, y + 109, int(110 * (0.7 + 0.3 * q)), RED, clamp(q) * a, anchor="lm")
        if t > tV2:
            red_ring(cr, 690, y + 105, 150, 78, prog(t, tV2, 0.4), 8, a)
    return dict(ui=ui, night=0.1, lift=1.0, flash=flash_at(t, tVt, 0.12) + flash_at(t, tP, 0.15), strip=1.0,
                red=0.08)


def hairam_cloud(cr, t, t_in, x, y, s=0.46, flip=False):
    """A speech cloud with हाय राम! in it."""
    cloud_text(cr, t, x, y, s, [], flip=flip, t_in=t_in)
    p = prog(t, t_in + 0.05, 0.25)
    if p <= 0.01:
        return
    k = 1.15 - 0.15 * back(clamp((t - t_in) / 0.3))
    cr.save()
    cr.translate(x, y + 4)
    cr.scale(k, k)
    if HAS_INDIC:
        su = indic(WORD["hairam"], int(92 * s / 0.46), RED)
        cr.set_source_surface(su, -su.get_width() / 2, -su.get_height() / 2)
        cr.paint_with_alpha(p)
    else:
        draw_text(cr, "HAI RAM!", 0, 0, 80, RED, p, anchor="cm")
    cr.restore()


def s_v8(cr, t, tl, t0, t1):
    from scenes_garuda_purana import cow_badge
    c = cues(tl, "v8")
    tB, tN, tH = c["B"], c["N"], c["H"]
    vait_set(cr, t, 0.6, 470, V_BOT)
    x, h = 620, 520
    glow(cr, x, FL - 280, 460, 0.4)
    head_hold = prog(t, tH - 0.3, 0.3)
    pts = dh(cr, t, x, FL, h, mood="sheepish" if t < tN else ("crying" if t < tH else "terrified"),
             front=mix((-0.25, -0.35), (-1.95, -0.35), head_hold), backa=mix((0.3, -0.25), (-2.75, -1.45), head_hold),
             head=-0.1 * head_hold, glow=0.5, shiver=0.5 * head_hold)
    dev_h = pts.get("top", (x, 400))

    def ui(cr):
        head2(cr, t, "IN HIS WHOLE LIFE HE NEVER GAVE", t0 + 0.05, "EVEN A CALF!", tB, under=tN)
        cow_badge(cr, t, tB - 0.1, 1360, 600, 150)
        plate(cr, t, tB + 0.2, "A GIFT CALF", 1360, 800, 34)
        big_x(cr, 1360, 600, 300, 300, prog(t, tN, 0.3), 1.0, lw=28)
        hairam_cloud(cr, t, tH - 0.15, dev_h[0] + 330, dev_h[1] + 40)
    return dict(ui=ui, night=0.1, lift=1.0, flash=flash_at(t, tN, 0.15), strip=1.0, red=0.1)


def s_v9(cr, t, tl, t0, t1):
    c = cues(tl, "v9")
    tU, tK, tG = c["U"], c["K"], c["G"]
    boil = prog(t, tU - 0.3, 0.8)
    vait_set(cr, t, 1.0, 420, V_BOT, boil=boil, speed=1.0 + 1.5 * boil)
    jump = keyed_fall(t, [(tU, 1.0)], 0.25)
    trio(cr, t, 600 - 90 * jump, walk=0.0, gap=230, dmood="terrified" if t > tU else "sheepish",
         dkw=dict(feet=FL - 60 * math.sin(math.pi * clamp((t - tU) / 0.4)) * (t > tU), front=(-2.6, -0.6),
                  backa=(-2.4, -0.6), shiver=0.6 * jump))
    cx, cy = 1450, 520

    def ui(cr):
        if t < tK:
            head2(cr, t, "THE RIVER STARTED TO", t0 + 0.05, "BOIL!", tU)
        else:
            head2(cr, t, "LIKE", tK - 0.1, "GHEE IN A HOT PAN!", tK + 0.05, under=tG + 0.2)
        a = icon_card(cr, t, tK - 0.15, cx, cy, 480, 330)
        if a > 0:
            yy = card_y(t, tK - 0.15, cy)
            warm(cr, cx, yy + 60, 200, 0.6 * a, (1.0, 0.5, 0.15))
            prop(cr, "yb_kadhai", cx, yy + 110, 0.7, alpha=a)
            for i in range(6):
                u = (t * 1.5 + i / 6) % 1.0
                bx = cx - 130 + 52 * i
                cr.new_path()
                cr.arc(bx, yy + 110 - 120 * 0.7 - 4 * u, 6 + 14 * u, math.pi, 2 * math.pi)
                cr.set_source_rgba(1.0, 0.9, 0.5, a * (1 - u))
                cr.fill_preserve()
                cr.set_source_rgba(*INK, 0.7 * a * (1 - u))
                cr.set_line_width(2)
                cr.stroke()
            plate(cr, t, tK + 0.1, "GHEE IN A KADHAI", cx, yy - 120, 32, alpha=a)
    return dict(ui=ui, night=0.1, lift=1.0, flash=flash_at(t, tU, 0.2), strip=1.0, red=0.15 + 0.1 * boil)


def s_v10(cr, t, tl, t0, t1):
    c = cues(tl, "v10")
    tD, tM, tL, tU, tP = c["D"], c["M"], c["L"], c["U"], c["P"]
    landed = prog(t, tP + 0.1, 0.4)
    fly_sp = 2.4 * (1 - landed)
    vait_set(cr, t, 1.0, 380, FL + 160, speed=1.0 + fly_sp, near=False)
    # the far bank slides in from the right as they cross
    bank = ease((t - tU) / max(0.6, tP - tU + 0.3)) if t > tU else 0.0
    bx0 = W + 120 - 760 * bank
    if bank > 0:
        cr.save()
        pc.poly(cr, [(bx0, FL - 30), (W + 50, FL - 30), (W + 50, H + 50), (bx0 - 60, H + 50)])
        cr.set_operator(cairo.OPERATOR_MULTIPLY)
        cr.set_source_rgba(0.70, 0.54, 0.36, 1.0)
        cr.fill()
        cr.restore()
        prop(cr, "ground", bx0 + 900, FL + 6, 1.0)
    # the messengers fly across; Dhaniram dangles from the rope under them, kicking
    gx = 380 + 520 * ease(clamp((t - t0) / max(1.0, tP - t0)))
    gy = 400 + 18 * math.sin(t * 2.4)
    if landed < 1:
        a = 1 - landed
        for k, (dx, dy, hold) in enumerate(((-260, -30, "staff"), (0, 0, None))):
            kw = dict(front=(-2.6, -0.2), backa=(-2.4, -0.3), legs=(0.5 + 0.1 * math.sin(t * 5 + k), 0.7), rot=1.25,
                      y=gy + dy, hold=hold, ph=k, alpha=a, rods=False)
            p = duta(cr, t, gx + dx, 0.46, **kw)
        hand = to_user(cr, p["handF"]) if "handF" in p else (gx + 200, gy)
        phi = 0.32 * math.sin(t * 3.4)
        L_ = 210
        nx, ny = hand[0] + L_ * math.sin(phi), hand[1] + L_ * math.cos(phi)
        h = DH_H
        s = h / 1052.0
        th = -phi
        hx = nx - (7 * math.cos(th) + 294 * math.sin(th)) * s
        hy = ny - (7 * math.sin(th) - 294 * math.cos(th)) * s
        kick = math.sin(t * 13)
        dh(cr, t, hx, hy + 434 * s, h, mood="terrified", rot=th, legs=(0.5 * kick, -0.5 * kick),
           front=(-2.7 + 0.4 * kick, -0.4), backa=(-2.5 - 0.4 * kick, -0.5), alpha=a)
        rope_to(cr, hand, (nx, ny), sag=6, w=6, loop=(0.07 * h, 0.03 * h), alpha=a)
        for i in range(5):                                   # speed lines
            yy = gy - 60 + 50 * i
            u = (t * 2 + i * 0.3) % 1.0
            cr.set_source_rgba(1.0, 0.92, 0.75, 0.5 * a * (1 - u))
            cr.set_line_width(5)
            cr.move_to(gx - 520 - 200 * u, yy)
            cr.line_to(gx - 380 - 200 * u, yy)
            cr.stroke()
    if landed > 0:
        x = 1500
        trio(cr, t, x, walk=0.0, gap=230, dmood="terrified", alpha=landed,
             dkw=dict(feet=sit_feet(DH_H), legs=SIT_LEGS, head=0.2, front=(-0.2, -0.3), backa=(0.1, -0.2)))
        from scenes_ravana import stars_spin
        if landed > 0.5:
            stars_spin(cr, t, x + 10, FL - 250, 70, tP, landed)

    def ui(cr):
        if t < tU:
            head2(cr, t, "THE MESSENGERS HUNG HIM", t0 + 0.05, "LIKE A FISH ON A LINE", tM)
        else:
            head2(cr, t, "AND FLEW HIM", tU - 0.1, "ACROSS THE RIVER", tP, under=tP + 0.4)
        a = icon_card(cr, t, tM - 0.1, 1560, 420, 330, 300, t_out=tU + 0.2)
        if a > 0:
            yy = card_y(t, tM - 0.1, 420)
            sw = 0.25 * math.sin(t * 4)
            top = (1560, yy - 140)
            end = (1560 + 80 * math.sin(sw), yy - 140 + 80 * math.cos(sw))
            cr.set_source_rgba(*INK, a)
            cr.set_line_width(3)
            cr.move_to(*top)
            cr.line_to(*end)
            cr.stroke()
            cr.save()                                     # the fish hangs head-up from the end of the line
            cr.translate(*end)
            cr.rotate(math.pi / 2 - sw + 0.2 * math.sin(t * 9))
            prop(cr, "c6_fish0", 0.7 * 120, 0, 0.7, alpha=a, flip=True)
            cr.restore()
            plate(cr, t, tM + 0.1, "A FISH ON A LINE", 1560, yy + 120, 28, alpha=a)
    return dict(ui=ui, night=0.1, lift=1.0, flash=flash_at(t, tP + 0.1, 0.15), strip=1.0, red=0.12)


# ------------------------------------------------------------------ the shots: the cold city, the last body


def cold_set(cr, t, a=1.0):
    """Shitadhya: ice peaks, snow on the floor, snow falling."""
    prop(cr, "yb_icepeak", 1360, FL - 10, 0.82, alpha=0.85 * a, blur=3)
    prop(cr, "yb_icepeak", 360, FL - 10, 0.58, alpha=0.7 * a, blur=5, flip=True)
    dry_ground(cr, t, 0.0, a, (0.78, 0.82, 0.92))
    frost(cr, a)


def breath(cr, t, pts, a=1.0, flip=False):
    """Little puffs of cold breath from his mouth."""
    if "head" not in pts or a <= 0.01:
        return
    hx, hy = to_user(cr, pts["head"])
    sg = -1 if flip else 1
    for i in range(2):
        u = (t * 0.9 + i * 0.5) % 1.0
        cr.new_path()
        cr.arc(hx + sg * (30 + 50 * u), hy + 10 - 20 * u, 8 + 14 * u, 0, 2 * math.pi)
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.6 * a * (1 - u))
        cr.fill()


HUG = dict(front=(-0.85, -2.05), backa=(-0.7, -2.1))        # arms wrapped round himself


def s_s1(cr, t, tl, t0, t1):
    c = cues(tl, "s1")
    tS, tT, tHm, tG = c["S"], c["T"], c["Hm"], c["G"]
    t_out = min(max(t0 + 1.6, tS + 0.5), t1 - 2.0)
    sc = prog(t, t_out - 0.3, 0.5)
    cold_set(cr, t, sc)
    out = trio(cr, t, 860, walk=0.0, gap=270, dmood="terrified", alpha=sc,
               dkw=dict(shiver=1.0, **HUG))
    breath(cr, t, out["dh"], sc)
    chapter(cr, t, t0 - 0.3, t_out, "MONTH 12", [[("THE CITY OF", INK)], [("COLD", RED)]], SOURCE)
    cx, cy = 1490, 470

    def ui(cr):
        if t > t_out:
            if t < tHm:
                head2(cr, t, "MONTH 12:", t_out + 0.05, "THE CITY OF COLD", max(tT, t_out + 0.2))
            else:
                head2(cr, t, "IT WAS", tHm - 0.15, "100 × COLDER THAN THE HIMALAYA", tG, under=tG + 0.5)
            a = icon_card(cr, t, tHm - 0.15, cx, cy, 380, 330)
            if a > 0:
                yy = card_y(t, tHm - 0.15, cy)
                prop(cr, "yb_icepeak", cx, yy + 120, 0.32, alpha=a)
                draw_text(cr, "HIMALAYA", cx, yy - 120, 38, INK, a, MONO_FONT, "cm", tracking=3)
                if t > tG:
                    from scenes_jarasandha import stamp
                    stamp(cr, t, tG, "× 100", cx + 120, yy + 30, 96)
    return dict(ui=ui, cool=0.45 * sc, night=0.08, lift=1.0, flash=flash_at(t, t_out, 0.15), strip=1.0,
                snow=sc)


def s_s2(cr, t, tl, t0, t1):
    c = cues(tl, "s2")
    tK, tD, tA, tB = c["K"], c["D"], c["A"], c["B"]
    cold_set(cr, t)
    x = 1000
    look = t > tD and int((t - tD) / 0.5) % 2 == 1
    out = trio(cr, t, x, walk=0.0, gap=560, dmood="terrified" if t < tA else "crying",
               dkw=dict(shiver=1.0, flip=look, **HUG))
    breath(cr, t, out["dh"], 1.0, flip=look)
    dev = out["dh"].get("chest", (x, FL - 200))
    dev_top = out["dh"].get("top", (x, FL - 300))

    def ui(cr):
        if t < tA:
            head2(cr, t, "SHIVERING, HE LOOKED IN", t0 + 0.05, "ALL 10 DIRECTIONS", tD)
        else:
            head2(cr, t, "HE CRIED OUT:", tA - 0.15, None, 0.0)
        for k in range(10):
            q = pop(t, tD + 0.08 * k, 0.3, 1.6) * (1 - prog(t, tA + 0.6, 0.4))
            if q <= 0.01:
                continue
            ang = -math.pi / 2 + 2 * math.pi * k / 10
            r0, r1 = 190, 190 + 110 * clamp(q)
            x0, y0 = dev[0] + r0 * math.cos(ang), dev[1] - 40 + r0 * 0.8 * math.sin(ang)
            x1, y1 = dev[0] + r1 * math.cos(ang), dev[1] - 40 + r1 * 0.8 * math.sin(ang)
            if y1 > FL + 40:
                continue
            cr.set_source_rgba(*RED, 0.9 * clamp(q))
            cr.set_line_width(7)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.move_to(x0, y0)
            cr.line_to(x1, y1)
            cr.stroke()
            draw_text(cr, "?", x1 + 26 * math.cos(ang), y1 + 26 * math.sin(ang), 48, RED, clamp(q), anchor="cm")
        cloud_text(cr, t, dev_top[0] + 360, dev_top[1] - 10, 0.48, [("ANYONE?", 80, INK, -40, tA),
                                                                     ("SAVE ME!", 88, RED, 48, tB)], t_in=tA - 0.2)
    return dict(ui=ui, cool=0.45, night=0.08, lift=1.0, flash=flash_at(t, tD, 0.12), strip=1.0, snow=1.0)


def s_s3(cr, t, tl, t0, t1):
    c = cues(tl, "s3")
    tP, tPn, tJ = c["P"], c["Pn"], c["J"]
    cold_set(cr, t)
    from puppet_core import hop_walk
    x1, bob1, rock1, ph1 = hop_walk(t, tP - 0.8, tP + 0.2, 440, 660, 0.4)
    x2, bob2, rock2, ph2 = hop_walk(t, tP - 0.7, tP + 0.3, 180, 400, 0.4)
    duta(cr, t, x2, DU_S, hold="staff", front=(-0.45, -0.35), legs=walk_legs(ph2, 0.3), rot=rock2,
         y=FL - 434 * DU_S + bob2, ph=0.7)
    d1 = duta(cr, t, x1, DU_S, hold=None, front=(-1.5, 0.0) if t > tP - 0.2 else (-1.1, -0.3),
              mood="scold" if t > tP - 0.2 else None, legs=walk_legs(ph1, 0.3), rot=rock1, y=FL - 434 * DU_S + bob1,
              ph=0.2)
    hands = prog(t, tJ - 0.3, 0.4)
    x = 1180
    pts = dh(cr, t, x, FL, DH_H + 30, mood="terrified" if t < tJ else "sheepish", flip=True, shiver=1.0 - 0.6 * hands,
             front=mix(HUG["front"], (-1.45, -0.15), hands), backa=mix(HUG["backa"], (-1.3, -0.25), hands))
    breath(cr, t, pts, 1.0, flip=True)
    rope_to(cr, to_user(cr, d1["handF"]) if "handF" in d1 else None, neck_of(cr, pts), sag=90, w=6,
            loop=(0.07 * DH_H, 0.03 * DH_H))
    dev_d = d1.get("top", (x1, 300))
    hand_pts = [pts[k] for k in ("handF", "handB") if k in pts]

    def ui(cr):
        if t < tJ:
            head2(cr, t, "THE MESSENGERS ASKED:", t0 + 0.05, None, 0.0)
        else:
            head2(cr, t, "AND DHANIRAM HAD", tJ - 0.15, "NO ANSWER", tJ + 0.05, under=tJ + 0.5)
        cloud_text(cr, t, dev_d[0] + 330, dev_d[1] + 10, 0.5, [("WHAT MERIT", 76, INK, -40, tP),
                                                               ("DO YOU HAVE?", 74, RED, 48, tPn)], t_in=tP - 0.25,
                   alpha=1 - prog(t, tJ + 0.4, 0.3))
        plate(cr, t, tPn + 0.3, "MERIT = GOOD DEEDS", dev_d[0] + 780, dev_d[1] + 30, 30,
              t_out=tJ + 0.4)
        if hand_pts and t > tJ:
            hx = sum(p[0] for p in hand_pts) / len(hand_pts)
            hy = sum(p[1] for p in hand_pts) / len(hand_pts)
            red_ring(cr, hx - 10, hy, 110, 70, prog(t, tJ + 0.1, 0.4), 8)
            plate(cr, t, tJ + 0.4, "EMPTY HANDS", hx - 10, hy + 110, 30, color=RED)
    return dict(ui=ui, cool=0.45, night=0.08, lift=1.0, flash=flash_at(t, tJ, 0.12), strip=1.0, snow=1.0)


S4_X = 900                           # where the hand-sized body stops and falls away


def s_s4(cr, t, tl, t0, t1):
    c = cues(tl, "s4")
    tA, tH, tC, tAg, tB = c["A"], c["H"], c["C"], c["Ag"], c["B"]
    prop(cr, "gp_gate", 260, FL + 6, 0.62, alpha=0.75, blur=3)
    glow(cr, 260, FL - 200, 300, 0.25)
    far_hills(cr, t, 0.0, 0.6, (0.42, 0.40, 0.50), FL - 40)
    dry_ground(cr, t, 0.0, 1.0, (0.66, 0.60, 0.66))
    walk_in = clamp((t - t0) / max(0.8, tH - t0))
    x_body = 600 + (S4_X - 600) * ease(walk_in)
    on = tC < t
    h = DH_H + 40
    # the thumb-sized soul: rises out of the body's chest, lands in front of it and walks on
    out = ease((t - tC) / 0.8) if on else 0.0
    soul_h = 130
    go = ease(clamp((t - tAg) / max(0.8, t1 - tAg - 0.3))) if t > tAg else 0.0
    soul_x = S4_X + 170 * out + 420 * go
    d_x = (x_body if not on else S4_X + 420 * go) - 280
    bob, rock, lp = walk_cycle(t, 0.46, 0.2, 1.0 if (t < tH or t > tAg) else 0.0)
    duta(cr, t, d_x - 280, DU_S, hold="staff", front=(-0.45, -0.35), legs=walk_legs(lp, 0.3), rot=rock,
         y=FL - 434 * DU_S + bob, ph=0.7)
    d1 = duta(cr, t, d_x, DU_S, hold=None, front=(-1.25, -0.25), legs=walk_legs(-lp, 0.3), rot=-rock,
              y=FL - 434 * DU_S + bob, ph=0.2)
    if not on:
        bobb, rockb, lpb = walk_cycle(t, 0.38, 0.1, 1.0 - prog(t, tH - 0.3, 0.3))
        pts = dh(cr, t, x_body, FL + bobb * 0.8, h, mood="sheepish" if t < tH else "shocked",
                 legs=walk_legs(lpb, 0.42), rot=rockb)
    else:
        # the empty body: it stands still, goes dark and hollow (a figure of dots), slumps and falls away to dust
        slump = ease((t - tC - 0.5) / 0.9)
        fade = 1 - prog(t, tC + 1.5, 0.9)
        if fade > 0.01:
            def shell(c_):
                dh(c_, t, S4_X, FL + 6 * slump, h, mood="shut", glow=0.0, rot=-0.22 * slump,
                   front=(0.05, -0.05), backa=(0.1, -0.05), head=0.25 * slump)
            ghost(cr, shell, prog(t, tC, 0.4) * fade, faint=0.3)
        if t < tC + 0.5:
            cr.save()
            cr.push_group()
            dh(cr, t, S4_X, FL, h, mood="shocked", glow=0.0)
            cr.pop_group_to_source()
            cr.paint_with_alpha(1 - prog(t, tC, 0.5))
            cr.restore()
        body_outline(cr, S4_X, FL, h * 0.95, 1.0, 0.45 * prog(t, tC + 1.2, 0.4) * (1 - prog(t, tC + 2.4, 0.6)),
                     crumble=prog(t, tC + 1.6, 1.0))
        sy = FL - 0.55 * h * math.sin(math.pi * min(1.0, out)) * (out < 1)
        bobs, rocks, lps = walk_cycle(t, 0.3, 0.0, 1.0 if t > tAg else 0.0)
        pts = dh(cr, t, soul_x, sy + bobs * 0.6, soul_h * (0.5 + 0.5 * out), mood="terrified", solid=0.0, glow=1.6,
                 legs=walk_legs(lps, 0.4), rot=rocks)
        if t < tC + 1.2:
            burst(cr, t, S4_X, FL - 0.55 * h, tC, n=16, rmax=380, alpha=0.7)
    rope_to(cr, to_user(cr, d1["handF"]) if "handF" in d1 else None, neck_of(cr, pts), sag=60, w=6 if not on else 4,
            loop=((0.05 * h, 0.022 * h) if not on else (0.05 * soul_h, 0.022 * soul_h)))
    dev_s = pts.get("top", (soul_x, FL - 200))

    def ui(cr):
        if t < tC:
            head2(cr, t, "IN THE LAST CITY...", t0 + 0.05, "THE HAND-SIZED BODY...", tH)
        elif t < tAg:
            head2(cr, t, "THE HAND-SIZED BODY", tC - 0.15, "FELL AWAY", tC + 0.05)
        else:
            head2(cr, t, "AND THE THUMB-SIZED SOUL", tAg - 0.15, "WENT ON", tB, under=tB + 0.4)
        plate(cr, t, tH, "HAND-SIZED BODY", S4_X, FL - h - 70, 30, t_out=tC + 0.2)
        plate(cr, t, tC + 0.9, "EMPTY SHELL", S4_X - 20, FL - h - 40, 28, t_out=tC + 2.2)
        if t > tAg:
            tag(cr, t, tAg + 0.1, "THUMB-SIZED SOUL", dev_s[0] + 40, dev_s[1] - 80, 30)
    return dict(ui=ui, night=0.15, lift=1.0, cool=0.15, flash=flash_at(t, tC, 0.3), strip=1.0)


def s_s5(cr, t, tl, t0, t1):
    c = cues(tl, "s5")
    tS, tA, tY = c["S"], c["A"], c["Y"]
    rise = ease((t - t0) / 1.6)
    cy = FL - 90 + 120 * (1 - rise)
    glow(cr, 960, cy - 230, 640, 0.6)
    aura(cr, t, 960, cy - 230, 160, 640, 0.35 * prog(t, tA, 0.6), n=22, spin=0.02, col=(1.0, 0.55, 0.3))
    prop(cr, "yb_yamapura", 960, cy, 0.76, alpha=0.95 * rise, blur=1.5)
    cr.save()                                           # the road to its gate
    pc.poly(cr, [(200, FL + 200), (900, FL + 200), (990, cy), (930, cy)])
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(0.86, 0.66, 0.40, 0.7)
    cr.fill()
    cr.restore()
    dry_ground(cr, t, 0.0, 0.8, (0.70, 0.56, 0.44))
    u = ease(clamp((t - t0) / max(1.0, t1 - t0)))
    x = 560 + 220 * u
    bob, rock, lp = walk_cycle(t, 0.5, 0.0, 1.0)
    duta(cr, t, x - 420, 0.4, hold="staff", front=(-0.45, -0.35), legs=walk_legs(lp, 0.3), rot=rock,
         y=FL - 434 * 0.4 + bob, ph=0.7)
    d1 = duta(cr, t, x - 210, 0.4, hold=None, front=(-1.25, -0.25), legs=walk_legs(-lp, 0.3), rot=-rock,
              y=FL - 434 * 0.4 + bob, ph=0.2)
    pts = dh(cr, t, x, FL + bob * 0.5, 120, mood="terrified", solid=0.0, glow=1.4, legs=walk_legs(lp, 0.4),
             head=-0.1)
    rope_to(cr, to_user(cr, d1["handF"]) if "handF" in d1 else None, neck_of(cr, pts), sag=40, w=4,
            loop=(9, 4))

    def ui(cr):
        head2(cr, t, "AFTER 1 YEAR, AT LAST...", t0 + 0.05, "YAMA'S CITY", tY, under=tY + 0.5)
        counter_badge(cr, t, tS, "1 YEAR", 300, 380, 84)
    return dict(ui=ui, night=0.25, lift=1.0, flash=flash_at(t, tY, 0.3), strip=1.0)


# ------------------------------------------------------------------ the shot list and the frame


SHOTS = [   # (line, draw function, options) - one shot per line; "cont" = same set as the line before (no lamp dip)
    ("w1", s_w1, {"z": (1.0, 1.02)}),
    ("w2", s_w2, {"z": (1.02, 1.03), "cont": True}),
    ("w3", s_w3, {"z": (1.0, 1.04), "focus": (760, 600)}),
    ("w4", s_w4, {"z": (1.0, 1.03)}),
    ("w5", s_w5, {"z": (1.0, 1.02), "cont": True}),
    ("w6", s_w6, {"z": (1.0, 1.04), "focus": (900, 700)}),
    ("w7", s_w7, {"z": (1.0, 1.03), "cont": True}),
    ("c1", s_c1, {"z": (1.0, 1.02)}),
    ("c2", s_c2, {"z": (1.02, 1.04), "cont": True}),
    ("c3", s_c3, {"z": (1.0, 1.03)}),
    ("c4", s_c4, {"z": (1.0, 1.05), "focus": (760, 560)}),
    ("c5", s_c5, {"z": (1.0, 1.03)}),
    ("c6", s_c6, {"z": (1.0, 1.05), "focus": (1100, 600)}),
    ("c7", s_c7, {"z": (1.0, 1.03)}),
    ("c8", s_c8, {"z": (1.0, 1.02)}),
    ("c9", s_c9, {"z": (1.0, 1.05), "focus": (960, 560)}),
    ("v1", s_v1, {"z": (1.0, 1.03)}),
    ("v2", s_v2, {"z": (1.0, 1.02)}),
    ("v3", s_v3, {"z": (1.02, 1.04), "cont": True}),
    ("v4", s_v4, {"z": (1.0, 1.03)}),
    ("v5", s_v5, {"z": (1.0, 1.03), "cont": True}),
    ("v6", s_v6, {"z": (1.0, 1.02), "cont": True}),
    ("v7", s_v7, {"z": (1.0, 1.02), "cont": True}),
    ("v8", s_v8, {"z": (1.0, 1.04), "focus": (760, 560)}),
    ("v9", s_v9, {"z": (1.0, 1.03)}),
    ("v10", s_v10, {"z": (1.0, 1.02), "cont": True}),
    ("s1", s_s1, {"z": (1.0, 1.03)}),
    ("s2", s_s2, {"z": (1.0, 1.03), "cont": True}),
    ("s3", s_s3, {"z": (1.0, 1.03), "cont": True}),
    ("s4", s_s4, {"z": (1.0, 1.04), "focus": (960, 640)}),
    ("s5", s_s5, {"z": (1.0, 1.04), "focus": (960, 600)}),
]
_IDX = {bid: k for k, (bid, _, _) in enumerate(SHOTS)}


def shot_at(t, tl):
    """(shot index, start, end) for the line active at t: a shot runs from its line's start to the next line's start
    (the pause after a line belongs to it). Cached on the timeline under this module's own name."""
    spans = getattr(tl, "_yb_spans", None)
    if spans is None:
        spans = {}
        for i, b in enumerate(tl.beats):
            if b.id in _IDX:
                spans[b.id] = (b.start, tl.beats[i + 1].start if i + 1 < len(tl.beats) else tl.total)
        tl._yb_spans = spans
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
    fx, fy = opt.get("focus", (960, 600))
    cr.save()
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    stage(cr)
    out = fn(cr, t, tl, t0, t1) or {}
    tint(cr, (1.0, 0.66, 0.42), out.get("eve", 0.0))
    tint(cr, (0.74, 0.82, 1.0), out.get("cool", 0.0))
    tint(cr, (1.0, 0.62, 0.58), out.get("red", 0.0))
    cr.restore()
    motes(cr, t)
    snow(cr, t, out.get("snow", 0.0))
    lamp(cr, t, night=out.get("night", 0.0), flash=out.get("flash", 0.0))
    title_lift(cr, out.get("lift", 0.0) * min(1.0, 2.5 * out.get("night", 0.0)))
    strip(cr, t, tl, out.get("strip", 1.0))
    if out.get("ui"):
        out["ui"](cr)
    if not opt.get("cont") and t - t0 < 0.22:      # the lamp dips for a moment on a change of scene
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur) for the road, the cities, the Vaitarani and the cold city only, sparse (owner, 8 Nov 2026:
    "only use sounds where necessary"; 2-3 per part): a damaru on the road's chapter card, a hit as the twelve suns
    blaze, a bell at the first city's gate; shimmer as the first rice-ball of light arrives, a hit at the king who
    looks like Death, a bell on the re-hook "and Bhola?"; a conch as the Vaitarani is named, a bell on the gift cow;
    a damaru on the cold city's card, shimmer as the hand-sized body falls away. Chosen in that order of importance
    within each part and at least SFX_MIN_GAP apart (as render_myth.calm_sfx keeps them); bed dips before the reveals
    (the Death-like king, the re-hook, the Vaitarani, Yama's city)."""
    c = {b: cues(tl, b) for b in CUES}
    a1, _ = c5_arrivals(tl)
    want = [(c["w1"]["t0"] + 0.05, "damaru", 0), (c["w4"]["B"], "hit", 0), (c["w7"]["N"], "bell", 0),
            (a1, "shimmer", 0), (c["c6"]["M"], "hit", 0), (c["c9"]["B"], "bell", 0),
            (c["v2"]["V"], "conch", 0), (c["v6"]["G"], "bell", 0),
            (c["s1"]["t0"] + 0.05, "damaru", 0), (c["s4"]["C"], "shimmer", 0)]
    rank = {n: i for i, n in enumerate(SFX_KEEP)}
    kept = []
    for e in sorted(want, key=lambda e: rank.get(e[1], 99)):
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["c6"]["M"] - 0.3, "dip", 0.45), (c["c9"]["t0"] - 0.3, "dip", 0.45), (c["v2"]["V"] - 0.3, "dip", 0.5),
            (c["s5"]["Y"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
