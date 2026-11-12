"""Long video 2 (videos/yamlok_yatra.py, 1920x1080, Hindi), builder C's part: Yama's court (lines y1-y12), the eastern
gate and Bhola's welcome (t1-t8), the ending (o1-o5). scenes_yamlok_yatra routes every moment whose active line is y*,
t* or o* here; draw() paints the whole frame.

This part closes the loop the intro opened ("one of them Yama will frighten, the other's feet Yama himself will
wash"). Yama has TWO looks and the change between them carries the whole video:
  TO DHANIRAM   the terrible form (Garuda Purana III.18-21): a giant risen over the mountains on a huge buffalo, the
                danda raised, a fierce face under a fire halo, a fan of shadow arms behind him, storm clouds and
                lightning, a red-dark sky; frightening, never monstrous (no fangs, no gore).
  TO BHOLA      the same Yama (ruru_cast's Yama Dharmaraja, the same crown and danda) as a gentle king in golden light
                who rises from his throne, comes forward, welcomes him again and again, gives him the throne, kneels
                and washes his feet (XIV.74-76).
Screen geography, kept through the part: Yama is on the LEFT facing right; everyone who comes to him (Dhaniram from the
south gate, Bhola from the east gate) stands on the right facing left. On the city map east is to the right and south
at the bottom; the dark south road and the golden east road are drawn the same on the map and in the scenes.

Togalu Gombeyaata leather shadow puppets on the wide lamp-lit cloth of long video 1 (six_cast_c's screen and lamp, the
floor at FL = 892, two-tier headlines: a small dark setup line + one big red key line, fitted inside 90 px margins);
cast: garuda_cast (the messengers, Chitragupta), ruru_cast (Yama), six_cast_b (Yama's smile, his hall), yc_cast (the
buffalo, Yama's fierce face, the Shravanas, the munim, the gates, the chariot, the Parijata tree...), and yy_cast
(builder A: Dhaniram alive, his thumb-sized soul, Bhola, the safe and the water pot), so all three parts show the same
two men. The callback in o4c uses builder A's hook road (scenes_yy_a.road_set) so it looks like the opening.

Shot list (line: what is on the screen)
  y1  chapter card YAMA'S CITY (GARUDA PURANA · PRETA KALPA); it flies up onto a pictorial map of the city: a
      diamond of walls round Yama's palace, the four gates pop in on "char" with N, E, S, W badges: YAMA'S CITY HAS /
      FOUR GATES; the south road is dark and thorny, the east road golden; little Dhaniram is led up the south road by
      a messenger (DHANIRAM plate), the south gate goes dark under a storm cloud and is ringed: FOR PEOPLE LIKE
      DHANIRAM: / THE SOUTH GATE
  y2  the hall: the doorkeeper (spear, tag DOORKEEPER) leans and whispers to Chitragupta (tag CHITRAGUPTA), a little
      cloud DHANIRAM / IS HERE; small Dhaniram on the right on the messenger's noose: THE DOORKEEPER TOLD /
      CHITRAGUPTA; the doorkeeper steps back, word card मुनीम = ACCOUNTANT: CHITRAGUPTA IS / YAMA'S ACCOUNTANT; the
      scroll of deeds unrolls (ticks and crosses)
  y3  a big swinging "?" and a "?" over Dhaniram: BUT HOW DOES HE / KNOW EVERYTHING?
  y4  Brahma in a medallion (BRAHMA); three glowing Shravanas step out on clouds of light (plate SHRAVANAS · SONS OF
      BRAHMA), word card श्रवण = HEARING: BRAHMA'S SONS: / THE SHRAVANAS; the world in three bands (SKY, EARTH,
      PATALA) and one Shravana flies into each as it is named: THEY GO / EVERYWHERE; sound waves at their great ears,
      beams from their eyes: THEY HEAR AND SEE / FROM FAR AWAY
  y5  a memory window: Dhaniram at his shop counter (sacks, his safe) pushes away a thirsty man with an empty bowl
      (NO FREE WATER! / MOVE ON!; plates SAID, DONE), a Shravana listens hidden at the window's edge, a hand at his
      ear: SECRETLY OR OPENLY, / ALL YOU SAY AND DO; he flies to Chitragupta and a red cross lands on the scroll: THE
      SHRAVANAS TELL / CHITRAGUPTA
  y6  the witnesses pop in as medallions on each word: SUN, MOON, FIRE, WIND, EARTH, WATER, DAY, NIGHT: AND WHO ARE /
      THE WITNESSES?; last a big beating heart: AND MOST OF ALL... / YOUR OWN HEART
  y7  the hall; smug Dhaniram's thought cloud: his munim at a low desk changes 500 into 50 in the ledger and winks
      (plate MY MUNIM): DHANIRAM THOUGHT: MY MUNIM / FIXED THE NUMBERS; SO HERE TOO, A LITTLE... / JUGAAD?
  y8  the cloud pops; Chitragupta's scroll rolls all the way down to the floor, stamp NEVER WRONG, Dhaniram's face
      falls: BUT CHITRAGUPTA IS / NEVER WRONG
  y9  the hall goes dark, storm clouds; Yama's terrible form rises beyond the horizon, backlit red, the mountains only
      up to his buffalo's flank (plate MOUNTAINS): the giant on his buffalo (tag BUFFALO), the danda raised (ringed), a
      fire halo, a fan of shadow arms, glowing eyes; tiny Dhaniram on the right, hands up, shaking:
      THEN DHANIRAM SAW / YAMA'S TERRIBLE FORM, ON A BUFFALO, DANDA IN HAND, / BIG AS A MOUNTAIN; lightning and
      thunder rings on "garaj": AND HIS VOICE: / LIKE THUNDER
  y10 closer on tiny Dhaniram shaking (sweat drops, shiver lines), the giant looming: DHANIRAM / SHOOK WITH FEAR
  y11 Chitragupta speaks; a balance scale: FOOL | WISE, BEGGAR | RICH (Dhaniram points at himself, hopeful), WEAK |
      STRONG drop into the pans, the beam stays level, "=" between each pair, stamp ALL EQUAL: CHITRAGUPTA SAID: FOR
      YAMA, / EVERYONE IS EQUAL
  y12 Dhaniram on his knees, hands joined (cloud FORGIVE ME!): DHANIRAM BEGGED: / FORGIVE ME!; the two messengers
      shrug together, a Vishnu medallion (VISHNU): THE MESSENGERS SAID: / FORGIVING IS VISHNU'S JOB; one holds up an
      order leaf, stamp ORDERS: WE ONLY / FOLLOW ORDERS
  t1  chapter card THE EASTERN GATE; the city map again: the east gate blazes, a tiny golden chariot comes up the
      east road and stops (ringed): THEN, AT THE / EAST GATE...
  t2  the eastern road: a golden road set with jewels (tag JEWELS), Parijata trees dropping white flowers (tag
      PARIJATA TREES), swans gliding on the lotus pond (tag SWANS), the golden gate on the left; the chariot rolls in
      from the right and slows: THE EASTERN ROAD: / PAVED WITH JEWELS
  t3  the chariot stops; its door swings open, light pours out, a dark figure steps down... held beat... and on
      "Bhola" he is lit, his water pot on his shoulder, a hand raised (tag BHOLA): AND OUT STEPPED... / BHOLA!
  t4  three memory windows pop in with ticks: FREE WATER (Bhola pours water for the thirsty man), ROTI FOR THE COW,
      SERVED HIS MOTHER (pressing her feet): IT WAS THE / SAME BHOLA
  t5  close on Dhaniram in the golden light from the left: his eyes grow huge, "!!": WHAT HE SAW NEXT... / HIS EYES
      POPPED!
  t6  the hall in golden light: the giant's dark ghost shrinks into Yama on his throne (plate THE SAME YAMA): THE SAME
      YAMA WHO / SCARED DHANIRAM...; Yama rises from the throne: FOR BHOLA, HE ROSE FROM HIS / THRONE!
  t7  Yama walks forward, bows to Bhola again and again (WELCOME! x1 x2 x3): YAMA WELCOMED HIM / AGAIN AND AGAIN; turns
      and shows him to the throne, Bhola shuffles across behind him and is seated on it (sparkle), his pot set down
      beside it: HE GAVE BHOLA / HIS OWN THRONE; Yama kneels and pours water from a kalasha over Bhola's feet into a
      basin, Bhola shy and sweating ("!"): AND BOWED, AND / WASHED HIS FEET
  t8  split card, two framed panels with the same Yama in both: BAD DEEDS (dark, the giant over tiny Dhaniram) / YAMA
      LOOKS TERRIFYING; GOOD DEEDS (gold, Yama bowing to Bhola) / YAMA RISES TO WELCOME; a "=" badge and SAME YAMA
      between: THE GARUDA PURANA SAYS: / SAME YAMA, TWO FORMS
  o1  chapter card WHAT GOES WITH YOU; Dhaniram's dark empty room: the safe, locked, cobwebbed (stamp LEFT BEHIND):
      DHANIRAM'S SAFE / STAYED AT HOME; Bhola's clay pot glows on the right ("?"): AND BHOLA'S / WATER POT?
  o2  the pot rises in light and travels the eastern road beside Bhola (tag PUNYA = GOOD DEEDS): IT BECAME HIS PUNYA,
      / AND WENT WITH HIM
  o3  Dhaniram walked away into the dark by the two messengers (no hells shown): NOW DHANIRAM HAD TO / PAY HIS
      ACCOUNT; a palm-leaf card NO KARMA / DISAPPEARS UNPAID (GARUDA PURANA I.46): THE GARUDA PURANA SAYS:
  o4c the hook's frame again (builder A's road: the long empty road to the horizon under a burning sky), a 1 YEAR
      badge: REMEMBER THE / 1-YEAR JOURNEY?; a coin bag and a shop scale crossed out (NO BUYING, NO SELLING): ON THAT
      ROAD: / NO BUYING. NO SELLING.; a glowing pot of good deeds on the road (GOOD DEEDS): WHAT YOU TAKE WITH YOU, /
      EARN IT HERE
  o5  the two gates as cards: DHANIRAM'S GATE (south, dark) and BHOLA'S GATE (east, golden), a red ring alternating:
      IF YOUR JOURNEY BEGAN TOMORROW: / WHICH GATE WILL YOU TAKE? (the question is the last line)

Every frame is a pure function of t. Cues are words of the Hindi line (CUES: exact substrings of the script, fraction
fallbacks, minimum gaps; MISSES stays empty), cached on the timeline under this module's own names (_yc_*).
"""
import math

import cairo

import dharmavyadha_cast  # noqa: F401  (room, house, shop counter, bench, bowl, basin)
import garuda_cast as GC
import jayadratha_cast  # noqa: F401  (horses, wheel, soldier)
import kaikeyi_cast as K  # noqa: F401  (the balance scale)
import kumbhakarna_cast  # noqa: F401  (the swan)
import mandhata_cast  # noqa: F401  (throne, kalasha, lotus)
import puppet_core as pc
import ruru_cast as RU
import six_cast_b  # noqa: F401  (Yama's smile, his hall)
import six_cast_c as C
import shani_cast  # noqa: F401  (Vishnu's chakra and conch)
import shikhandi_cast  # noqa: F401  (the coin bag)
import yc_cast as YC
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, cross, draw_text, ease, prog, text_size, tick
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_arjuna import HAS_INDIC, cloud_text, indic_surface
from scenes_dharmavyadha import bmo
from scenes_garuda_purana import light_rope, noose_loop
from scenes_jarasandha import INK, RED, bob_rot, fit, glow, man_angles, motes, red_ring, sound_rings, walk_legs
from scenes_jarasandha import head2 as _head2
from scenes_jayadratha import flash_at, silhouette, soldier, tag, tint, to_user
from scenes_kaikeyi import ANJALI, balance, fig, settle
from scenes_lakshman_rekha import big_q, big_x, sparkle
from scenes_mandhata import aura, burst, held, lights, mix, warm
from scenes_ravana import dotted
from scenes_ruru import held_grip, petals, plate
from scenes_six_b import counter_badge
from scenes_six_c import blob_cloud, fade_in, mark, medallion, seg_line, stamp, talk_marks
from shots import T

import yy_cast as YY                    # builder A's shared cast: Dhaniram, his soul, Bhola, the safe, the pot

MISSES = set()                          # cue words not found in a line (falls back to fractions)
FL = 892                                # the floor line (feet) of the stage
S = 0.56                                # a standing figure's scale
HY = 46                                 # the headline's top
LIGHT = (1.0, 0.95, 0.82)
GREEN_TICK = (0.16, 0.50, 0.24)
GOLDL = (1.0, 0.80, 0.36)               # golden light
STORM = (0.62, 0.42, 0.52)              # the terrible form's dark red-violet tint
SIL = (0.10, 0.05, 0.10)                # shadow arms, ghosts
PUSH = dict(front=(-1.62, -0.05), backa=(0.25, -0.3))         # a palm pushed out: "move on!"
SHRUG = dict(front=(-0.55, -1.25), backa=(0.45, -1.35))        # both palms up and out: "not our job"
OFFER = (-1.25, -0.2)                   # an open hand held out (offering, showing the way)
CG_X, DH_X, DU_X = 400, 1330, 1650      # the hall: Chitragupta, Dhaniram, the messenger
DH_H = 170                              # Dhaniram's soul in the hall (thumb-sized beside the grown-ups)
TH_X = 430                              # Yama's throne (golden hall)
MAP_C = (960, 650)                      # the city map: centre, and the four gates
MAP_N, MAP_E, MAP_S, MAP_W = (960, 405), (1500, 650), (960, 900), (420, 650)
MAP_GS = 0.2                            # gate scale on the map


# ------------------------------------------------------------------ cues


def cue(tl, bid, word, frac):
    """A word cue (its position in the line) with a fraction fallback."""
    try:
        return T(tl, bid, word)
    except (KeyError, ValueError):
        MISSES.add((bid, word))
        return T(tl, bid, frac)


# Every cue of every line: (name, word, fraction fallback, ((after, min gap), ...)); "t0" = the line's start. Words are
# exact substrings of the Hindi lines (the first occurrence is the one meant; checked: MISSES stays empty).
CUES = {
    "y1": (("C", "चार", 0.22, (("t0", 0.9),)),
           ("D", "धनीराम", 0.55, (("C", 1.2),)),
           ("S", "दक्षिण", 0.8, (("D", 0.6),))),
    "y2": (("K", "ख़बर", 0.12, (("t0", 0.3),)),
           ("C", "चित्रगुप्त को", 0.22, (("K", 0.4),)),
           ("Y", "यानी", 0.42, (("C", 0.8),)),
           ("M", "मुनीम", 0.55, (("Y", 0.4),)),
           ("H", "हिसाब", 0.85, (("M", 0.8),))),
    "y3": (("H", "हिसाब", 0.5, (("t0", 0.6),)),
           ("Q", "कैसे", 0.8, (("H", 0.4),))),
    "y4": (("B", "ब्रह्मा", 0.18, (("t0", 0.5),)),
           ("S", "श्रवण", 0.33, (("B", 0.8),)),
           ("E", "धरती", 0.42, (("S", 1.2),)),
           ("A", "आकाश", 0.47, (("E", 0.35),)),
           ("P", "पाताल", 0.52, (("A", 0.35),)),
           ("G", "घूमते", 0.62, (("P", 0.4),)),
           ("L", "सुनते", 0.78, (("G", 0.6),)),
           ("V", "देखते", 0.92, (("L", 0.6),))),
    "y5": (("H", "छुपकर", 0.12, (("t0", 0.3),)),
           ("O", "खुलेआम", 0.22, (("H", 0.4),)),
           ("K", "कहा", 0.36, (("O", 0.4),)),
           ("D", "किया", 0.46, (("K", 0.4),)),
           ("C", "चित्रगुप्त", 0.68, (("D", 0.8),)),
           ("T", "बता", 0.85, (("C", 0.6),))),
    "y6": (("G", "गवाह", 0.05, (("t0", 0.1),)),
           ("1", "सूरज", 0.15, (("G", 0.4),)),
           ("2", "चाँद", 0.22, (("1", 0.25),)),
           ("3", "आग", 0.28, (("2", 0.25),)),
           ("4", "हवा", 0.34, (("3", 0.25),)),
           ("5", "धरती", 0.41, (("4", 0.25),)),
           ("6", "पानी", 0.48, (("5", 0.25),)),
           ("7", "दिन", 0.55, (("6", 0.25),)),
           ("8", "रात", 0.61, (("7", 0.25),)),
           ("Hd", "दिल", 0.92, (("8", 0.8),))),
    "y7": (("M", "मुनीम", 0.2, (("t0", 0.6),)),
           ("G", "गड़बड़", 0.45, (("M", 0.6),)),
           ("Y", "यहाँ", 0.68, (("G", 0.8),)),
           ("J", "जुगाड़", 0.85, (("Y", 0.4),))),
    "y8": (("C", "चित्रगुप्त", 0.12, (("t0", 0.1),)),
           ("N", "ग़लती", 0.6, (("C", 0.5),))),
    "y9": (("Y", "यमराज", 0.18, (("t0", 0.5),)),
           ("R", "रूप", 0.28, (("Y", 0.3),)),
           ("B", "भैंसे", 0.36, (("R", 0.5),)),
           ("P", "पहाड़", 0.48, (("B", 0.6),)),
           ("D", "दंड", 0.62, (("P", 0.6),)),
           ("L", "प्रलय", 0.72, (("D", 0.4),)),
           ("G", "गरज", 0.92, (("L", 0.6),))),
    "y10": (("T", "थर", 0.3, (("t0", 0.15),)),
            ("K", "काँपने", 0.6, (("T", 0.3),))),
    "y11": (("Y", "यमराज", 0.15, (("t0", 0.6),)),
            ("F", "मूर्ख", 0.27, (("Y", 0.5),)),
            ("W", "विद्वान", 0.35, (("F", 0.35),)),
            ("B", "भिखारी", 0.45, (("W", 0.45),)),
            ("R", "अमीर", 0.53, (("B", 0.35),)),
            ("K", "कमज़ोर", 0.63, (("R", 0.45),)),
            ("S", "ताक़तवर", 0.72, (("K", 0.35),)),
            ("E", "बराबर", 0.9, (("S", 0.5),))),
    "y12": (("J", "जोड़कर", 0.08, (("t0", 0.2),)),
            ("M", "माफ़ कर दो", 0.2, (("J", 0.4),)),
            ("D", "दूत", 0.33, (("M", 0.8),)),
            ("V", "विष्णु", 0.55, (("D", 0.8),)),
            ("H", "हुक्म", 0.88, (("V", 0.9),))),
    "t1": (("P", "पूरब", 0.18, (("t0", 0.3),)),
           ("R", "रथ", 0.65, (("P", 0.8),)),
           ("S", "रुका", 0.88, (("R", 0.4),))),
    "t2": (("J", "हीरों", 0.22, (("t0", 0.5),)),
           ("P", "पारिजात", 0.45, (("J", 0.7),)),
           ("K", "किनारे", 0.72, (("P", 0.7),)),
           ("H", "हंस", 0.9, (("K", 0.3),))),
    "t3": (("U", "उतरा", 0.5, (("t0", 0.4),)),
           ("B", "भोला", 0.85, (("U", 0.5),))),
    "t4": (("W", "प्यासों", 0.15, (("t0", 0.4),)),
           ("C", "गाय", 0.48, (("W", 1.0),)),
           ("M", "माँ", 0.78, (("C", 1.0),))),
    "t5": (("D", "देखकर", 0.25, (("t0", 0.5),)),
           ("A", "आँखें", 0.6, (("D", 0.6),)),
           ("F", "फटी", 0.72, (("A", 0.3),))),
    "t6": (("K", "काँप", 0.3, (("t0", 0.6),)),
           ("S", "सिंहासन", 0.7, (("K", 0.8),)),
           ("U", "उठ", 0.82, (("S", 0.3),))),
    "t7": (("A", "आगे", 0.02, (("t0", 0.0),)),
           ("B", "बार", 0.14, (("A", 0.5),)),
           ("W", "स्वागत", 0.3, (("B", 0.4),)),
           ("T", "सिंहासन", 0.5, (("W", 0.8),)),
           ("J", "झुककर", 0.75, (("T", 0.9),)),
           ("P", "पैर", 0.85, (("J", 0.4),)),
           ("D", "धोए", 0.93, (("P", 0.25),))),
    "t8": (("B", "बुरे", 0.22, (("t0", 0.6),)),
           ("D", "डरावने", 0.38, (("B", 0.6),)),
           ("A", "अच्छे", 0.55, (("D", 0.8),)),
           ("V", "वही", 0.72, (("A", 0.5),)),
           ("W", "स्वागत", 0.9, (("V", 0.5),))),
    "o1": (("T", "तिजोरी", 0.12, (("t0", 0.2),)),
           ("R", "रह", 0.35, (("T", 0.5),)),
           ("B", "भोला", 0.6, (("R", 0.6),)),
           ("G", "घड़ा", 0.9, (("B", 0.4),))),
    "o2": (("P", "पुण्य", 0.12, (("t0", 0.2),)),
           ("R", "रास्ते", 0.5, (("P", 0.5),)),
           ("S", "साथ", 0.8, (("R", 0.4),))),
    "o3": (("H", "हिसाब", 0.25, (("t0", 0.6),)),
           ("G", "गरुड़", 0.48, (("H", 1.0),)),
           ("F", "फल", 0.7, (("G", 0.8),)),
           ("M", "मिटता", 0.92, (("F", 0.6),))),
    "o4c": (("Y", "साल", 0.1, (("t0", 0.3),)),
            ("R", "रास्ते", 0.25, (("Y", 0.6),)),
            ("K", "ख़रीदा", 0.38, (("R", 0.4),)),
            ("B", "बेचा", 0.5, (("K", 0.5),)),
            ("S", "साथ", 0.66, (("B", 0.8),)),
            ("E", "कमाना", 0.88, (("S", 0.6),))),
    "o5": (("K", "किस", 0.3, (("t0", 0.8),)),
           ("D", "धनीराम", 0.45, (("K", 0.5),)),
           ("B", "भोला", 0.55, (("D", 0.5),)),
           ("I", "ईमानदारी", 0.72, (("B", 0.5),)),
           ("C", "कमेंट", 0.86, (("I", 0.4),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline, under this module's own name)."""
    cache = getattr(tl, "_yc_cues", None)
    if cache is None:
        cache = {}
        tl._yc_cues = cache
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


# ------------------------------------------------------------------ text and cards


def head(cr, t, small, t_small, big=None, t_big=0.0, big_size=118, small_size=56, maxw=1460, **kw):
    """The two-tier headline at the top centre: the big line fits maxw (inside the 90 px margins even at its pop-in
    overshoot), the small line 1600 px."""
    if big:
        big_size = min(big_size, fit(big, big_size, maxw))
    if small:
        words = small.split()
        sw = sum(text_size(w_, small_size)[0] for w_ in words) + small_size * 0.34 * (len(words) - 1)
        if sw > 1600:
            small_size = int(small_size * 1600 / sw)
    return _head2(cr, t, small, t_small, big, t_big, y=HY, small_size=small_size, big_size=big_size, **kw)


def chapter(cr, t, t_in, t_out, lines, source, kicker=None):
    """The palm-leaf chapter card of long video 1 (scenes_six_b / six_c): an optional red kicker, the English title
    (lines of [(text, colour)]), the source tag. It rises in at t_in and flies up and away at t_out."""
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
    p1, p2, p3 = prog(t, t_in + 0.15, 0.3), prog(t, t_in + 0.3, 0.35), prog(t, t_in + 0.6, 0.3)
    if kicker:
        draw_text(cr, kicker, 0, -138, 40, RED, a * p1, MONO_FONT, "cm", tracking=8)
    cr.set_source_rgba(*INK, 0.6 * a * p1)
    cr.set_line_width(2.5)
    cr.move_to(-300 * p1, -104)
    cr.line_to(300 * p1, -104)
    cr.stroke()
    n = len(lines)
    size = 92 if n <= 2 else 70
    for i, parts in enumerate(lines):
        yy = -10 + (i - (n - 1) / 2) * size * 1.08 + 10
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


def word_card(cr, t, t_in, word, latin, meaning, x, y, s=1.0, alpha=1.0, t_out=None):
    """A leather plaque on its rod: the Hindi word (shaped Devanagari) = its plain English meaning (screen coords)."""
    q = back(clamp((t - t_in) / 0.35), 1.4)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.25)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    yy = y + 60 * (1 - q)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(sway(t, 0.008, 0.4, x * 0.01))
    cr.scale(s * 0.8, s * 0.8)
    pc.paint_part(cr, "plaque", a)
    cr.restore()
    pc.rod(cr, x, yy + 95 * s, x + 30, H + 60, alpha=0.5 * a)
    if HAS_INDIC:
        su = indic_surface(word, int(80 * s), tuple(INK))
        sw_, sh_ = su.get_width(), su.get_height()
        k = min(1.0, 500 * s / sw_, 112 * s / sh_)
        cr.save()
        cr.translate(x, yy - 38 * s)
        cr.scale(k, k)
        cr.set_source_surface(su, -sw_ / 2, -sh_ / 2)
        cr.paint_with_alpha(a)
        cr.restore()
    else:
        draw_text(cr, latin, x, yy - 38 * s, int(64 * s), INK, a, anchor="cm")
    line = "= " + meaning
    msz = min(int(64 * s), fit(line, int(64 * s), 520 * s))
    draw_text(cr, line, x, yy + 52 * s, msz, RED, a, anchor="cm")


def badge(cr, t, t_in, text, x, y, r=34, alpha=1.0, color=INK, fill=(0.97, 0.87, 0.62)):
    """A round leather badge with a letter (the compass letters on the map)."""
    q = back(clamp((t - t_in) / 0.3), 1.6)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(max(0.05, q), max(0.05, q))
    cr.arc(0, 0, r + 5, 0, 2 * math.pi)
    cr.set_source_rgba(*pc.INK, a)
    cr.fill()
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.set_source_rgba(*fill, a)
    cr.fill()
    draw_text(cr, text, 0, 2, int(r * 1.25), color, a, anchor="cm")
    cr.restore()


def dev(cr, x, y):
    return cr.user_to_device(x, y)


# ------------------------------------------------------------------ light, weather, sets


def stone_floor(cr, a=1.0, col=(0.66, 0.60, 0.62), gold=1.0):
    """The hall's floor: dark stone flags from the floor line down, a gold inlay along the edge, joints running toward
    the middle."""
    if a <= 0.01:
        return
    cr.save()
    cr.rectangle(0, FL - 2, W, H - FL + 2)
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(*col, a)
    cr.fill()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.set_line_width(2.5)
    cr.set_source_rgba(0.22, 0.16, 0.14, 0.55 * a)
    for i in range(-9, 10):
        x0 = 960 + 120 * i
        cr.move_to(x0, FL)
        cr.line_to(960 + 330 * i, H)
    for yy in (FL + 40, FL + 100, FL + 180):
        cr.move_to(0, yy)
        cr.line_to(W, yy)
    cr.stroke()
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(5)
    cr.move_to(0, FL)
    cr.line_to(W, FL)
    cr.stroke()
    if gold > 0:
        cr.set_source_rgba(0.95, 0.72, 0.25, 0.8 * a * gold)
        cr.set_line_width(5)
        cr.move_to(0, FL + 12)
        cr.line_to(W, FL + 12)
        cr.stroke()
    cr.restore()


def hall(cr, t, a=1.0, blur=5):
    """Yama's hall behind the puppets (soft), and its stone floor."""
    prop(cr, "sb_yhall", 960, FL + 8, 0.6, alpha=0.6 * a, blur=blur)
    stone_floor(cr, a)


def storm_sky(cr, t, a, y1=FL):
    """The terrible form's sky: a red-violet gloom thickening upward, dark clouds drifting."""
    if a <= 0.01:
        return
    g = cairo.LinearGradient(0, 0, 0, y1)
    g.add_color_stop_rgba(0, 0.30, 0.12, 0.20, 0.75 * a)
    g.add_color_stop_rgba(0.7, 0.55, 0.22, 0.24, 0.45 * a)
    g.add_color_stop_rgba(1, 0.70, 0.35, 0.30, 0.2 * a)
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.rectangle(0, 0, W, y1)
    cr.set_source(g)
    cr.fill()
    cr.restore()


def clouds(cr, t, a, rows=((180, 150, 0.9, 0.0), (1260, 300, 0.8, 1.7), (1720, 200, 1.0, 0.8), (760, 90, 0.7, 2.6)),
           drift=1.0):
    """Dark storm clouds drifting slowly across."""
    if a <= 0.01:
        return
    for x, y, s, ph in rows:
        xx = x + drift * 30 * math.sin(t * 0.25 + ph)
        prop(cr, "cloud", xx, y + 8 * math.sin(t * 0.4 + ph), s, alpha=0.7 * a, blur=3)


def bolt_at(cr, t, t_b, x, y, s=1.0, a=1.0):
    """A lightning bolt striking at t_b (bright for a moment, flickering)."""
    u = t - t_b
    if not 0 <= u < 0.6:
        return
    f = (1 - u / 0.6) * (0.6 + 0.4 * (int(u * 30) % 2))
    glow(cr, x + 20 * s, y + 170 * s, 300 * s, 0.9 * f * a)
    prop(cr, "bolt", x, y, s, alpha=f * a)


def gold_light(cr, t, x, y, r, a):
    """Warm golden light (the east gate, Bhola, the gentle hall)."""
    if a <= 0.01:
        return
    glow(cr, x, y, r, 0.7 * a)
    warm(cr, x, y, r * 0.6, 0.6 * a, col=(1.0, 0.85, 0.45))


def sepia_lite(cr, a):
    """A flashback tint (inside a window): colours drained to warm brown."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_HSL_SATURATION)
    cr.set_source_rgba(0.5, 0.5, 0.5, 0.5 * a)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(1.0, 0.88, 0.70, 0.45 * a)
    cr.paint()
    cr.restore()


def window(cr, t, t_in, x, y, w, h, inner, alpha=1.0, sep=0.7, t_out=None, bg=(1.0, 0.93, 0.78)):
    """A memory window: a leather-framed picture popping in, its scene (inner(cr) draws it in screen coordinates,
    clipped) washed in flashback brown."""
    q = back(clamp((t - t_in) / 0.35), 1.4)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.3)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    k = 0.6 + 0.4 * q
    x0, y0 = x - w / 2, y - h / 2
    cr.save()
    cr.translate(x, y)
    cr.rotate(sway(t, 0.004, 0.3, x * 0.01))
    cr.scale(k, k)
    cr.translate(-x, -y)
    cr.push_group()
    cr.rectangle(x0, y0, w, h)
    cr.set_source_rgb(*bg)
    cr.fill()
    cr.save()
    cr.rectangle(x0, y0, w, h)
    cr.clip()
    inner(cr)
    sepia_lite(cr, sep)
    cr.restore()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, col in ((22, (0.40, 0.22, 0.10)), (6, (0.95, 0.72, 0.28))):
        cr.rectangle(x0 - 6, y0 - 6, w + 12, h + 12)
        cr.set_source_rgba(*col, a)
        cr.set_line_width(lw)
        cr.stroke()
    cr.rectangle(x0 - 17, y0 - 17, w + 34, h + 34)
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(4)
    cr.stroke()
    for px, py in ((x0, y0), (x0 + w, y0), (x0, y0 + h), (x0 + w, y0 + h)):
        cr.arc(px, py, 13, 0, 2 * math.pi)
        cr.set_source_rgba(0.95, 0.72, 0.28, a)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, a)
        cr.set_line_width(3)
        cr.stroke()
    cr.restore()


def deeds_scroll(cr, x, y, w, length, rows, alpha=1.0, title="DEEDS", crosses=None):
    """Chitragupta's scroll hanging from its top roller at (x, y): a title, rows of a green tick (True) or a red cross
    (False) with lines of writing, as far as it has unrolled; the bottom roller at its end. crosses = {row: 0..1}
    draws a red cross landing on that row."""
    if length < 4 or alpha <= 0.01:
        return
    cr.save()
    pc.poly(cr, [(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + length), (x - w / 2, y + length)])
    cr.set_source_rgba(0.98, 0.90, 0.68, 0.97 * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, alpha)
    cr.set_line_width(4)
    cr.stroke()
    draw_text(cr, title, x, y + 32, 30, INK, alpha * clamp((length - 60) / 40), MONO_FONT, "cm", tracking=4)
    for i, good in enumerate(rows):
        ry = y + 84 + 50 * i
        if ry + 26 > y + length:
            break
        if good:
            tick(cr, x - w / 2 + 20, ry, 32, 1.0, color=GREEN_TICK, alpha=alpha)
        else:
            cross(cr, x - w / 2 + 36, ry, 26, 1.0, alpha=alpha)
        cr.set_source_rgba(*pc.INK, 0.55 * alpha)
        cr.set_line_width(3)
        cr.move_to(x - w / 2 + 66, ry)
        for j in range(10):
            cr.line_to(x - w / 2 + 66 + (w - 86) * (j + 1) / 10, ry + 5 * math.sin(j * 2.1 + i))
        cr.stroke()
        if crosses and i in crosses and crosses[i] > 0:
            q = crosses[i]
            cr.save()
            cr.translate(x + w / 2 - 34, ry)
            sc = 1.8 - 0.8 * back(clamp(q), 2.0)
            cr.scale(sc, sc)
            cross(cr, 0, 0, 34, 1.0, alpha=alpha * clamp(q * 3))
            cr.restore()
    for yy in (y, y + length):
        pc.poly(cr, [(x - w / 2 - 18, yy - 11), (x + w / 2 + 18, yy - 11), (x + w / 2 + 18, yy + 11),
                     (x - w / 2 - 18, yy + 11)])
        cr.set_source_rgba(0.56, 0.33, 0.15, alpha)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, alpha)
        cr.stroke()
        for sx in (-1, 1):
            cr.arc(x + sx * (w / 2 + 26), yy, 13, 0, 2 * math.pi)
            cr.set_source_rgba(1.0, 0.82, 0.3, alpha)
            cr.fill_preserve()
            cr.set_source_rgba(*pc.INK, alpha)
            cr.stroke()
    cr.restore()


ROWS = (False, True, False, False, True, False, False, True, False, False, False, True, False, False)


def sweat(cr, t, x, y, s=1.0, a=1.0, n=3):
    """Sweat drops flying off a frightened head."""
    if a <= 0.01:
        return
    for i in range(n):
        u = (t * 1.6 + i / n) % 1.0
        dx = (-1 if i % 2 else 1) * (20 + 50 * u) * s
        dy = (-20 + 60 * u * u) * s
        cr.save()
        cr.translate(x + dx, y + dy)
        cr.scale(s, s)
        cr.move_to(0, -14)
        cr.curve_to(9, 0, 9, 8, 0, 10)
        cr.curve_to(-9, 8, -9, 0, 0, -14)
        cr.set_source_rgba(0.75, 0.90, 1.0, a * (1 - u))
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, 0.8 * a * (1 - u))
        cr.set_line_width(2)
        cr.stroke()
        cr.restore()


def shiver_lines(cr, t, x, y, h, a=1.0):
    """Little shake marks on both sides of a shivering figure."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_source_rgba(*pc.INK, 0.75 * a)
    cr.set_line_width(4)
    for sg in (-1, 1):
        for k in range(3):
            yy = y - h * (0.3 + 0.2 * k)
            xx = x + sg * (h * 0.32 + 6 * math.sin(t * 30 + k))
            cr.move_to(xx, yy - 14)
            cr.line_to(xx + sg * 8, yy)
            cr.line_to(xx, yy + 14)
    cr.stroke()
    cr.restore()


# ------------------------------------------------------------------ the shared cast (yy_cast, or stand-ins)


SOUL_MOODS = {"calm": "calm", "smug": "smug", "shock": "shocked", "terror": "terrified", "cry": "crying",
              "sheepish": "sheepish", "talk": "talking", "shut": "shut"}
SOUL_ARMS = {"rest": ((-0.32, -0.55), (0.3, -0.25)),
             "up": ((-2.45, -1.35), (-2.3, -1.5)),              # hands up by his face: terror
             "chest": ((-0.55, -2.05), (0.3, -0.25)),           # pointing at himself
             "beg": ((-0.75, -1.85), (-0.8, -1.8)),             # hands joined
             "out": ((-1.3, -0.2), (0.3, -0.25))}               # a hand held out


def dsoul(cr, t, x, feet, h, mood="calm", arms="rest", flip=True, alpha=1.0, shiver=0.0, halo=1.0, walk=None,
          kneel=False, hand="open", hits=(), head=0.0):
    """Dhaniram's thumb-sized soul (yy_cast.soul: the same little Dhaniram, glowing), feet at (x, feet), h tall,
    facing left (flip) by default; kneel = on one knee (yy_cast.dhani_kneel drawn the same way). Returns 'head',
    'chest', 'top' and 'handF' in user coordinates."""
    fr, ba = SOUL_ARMS[arms] if isinstance(arms, str) else arms
    md = SOUL_MOODS.get(mood, mood)
    legs = walk_legs(math.sin(walk), 0.3) if walk is not None else (0.0, 0.0)
    if kneel:
        pts = _soul_kneel(cr, t, x, feet, h, md, fr, ba, flip, alpha, shiver, halo, hand, hits, head)
    else:
        pts = YY.soul(cr, t, x, feet, h, mood=md, front=fr, backa=ba, legs=legs, flip=flip, alpha=alpha,
                      glow=halo, shiver=shiver, hand=hand, hits=hits, head=head)
    out = {"head": (x, feet - 0.75 * h), "chest": (x, feet - 0.5 * h), "top": (x, feet - h),
           "handF": (x, feet - 0.5 * h)}
    for k_ in ("head", "chest", "top", "handF"):
        if pts and k_ in pts:
            out[k_] = to_user(cr, pts[k_])
    return out


def _soul_kneel(cr, t, x, feet, h, md, fr, ba, flip, alpha, shiver, halo, hand, hits, head):
    """yy_cast.soul's look (a glow, a gold rim, a little translucent, lit from within) on Dhaniram kneeling."""
    if alpha <= 0.01 or h < 6:
        return {}
    s = h / YY.DH_H
    x += shiver * 0.02 * h * math.sin(t * 43)
    pul = 0.92 + 0.08 * math.sin(t * 3.3 + x * 0.013)
    if halo > 0:
        YY._glow(cr, x, feet - 0.4 * h, 1.2 * h + 40, 0.75 * alpha * halo * pul)
    cr.push_group()
    pts = YY.dhani_kneel(cr, t, x, s, md, ground=feet, front=fr, backa=ba, flip=flip, rods=False, hand=hand,
                         hits=hits, head=head)
    pat = cr.pop_group()
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7), (0.7, 0.7)):
        cr.save()
        r_ = max(2.0, 0.012 * h)
        cr.translate(dx * r_, dy * r_)
        cr.set_source_rgba(*YY.SOUL_GOLD, 0.5 * alpha)
        cr.mask(pat)
        cr.restore()
    cr.save()
    cr.set_source(pat)
    cr.paint_with_alpha(alpha * 0.8)
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source_rgba(*YY.SOUL_GOLD, 0.22 * alpha * pul)
    cr.mask(pat)
    cr.restore()
    return pts


BH_MOODS = {"calm": "calm", "smile": "smile", "joy": "joy", "shy": "shy", "talk": "talking"}


def bhola(cr, t, x, s, mood="calm", flip=True, front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0),
          feet=FL, alpha=1.0, blur=0.0, hits=(), ph=0.7, rot=0.0, y=None, rods=True, pot=False, kneel=False,
          sit=False, hand="open", bob=True):
    """Bhola (yy_cast), facing left (flip) by default: standing, kneeling (kneel) or seated on a throne / bench whose
    seat is 268 units above `feet` (sit). pot=True puts his water pot on his shoulder. Returns his points (device)."""
    md = BH_MOODS.get(mood, mood)
    kw = dict(front=front, head=head, hits=hits, flip=flip, alpha=alpha, blur=blur, rods=rods, rot=rot, ph=ph,
              hand=hand, bob=bob)
    if sit:
        return YY.bhola_seated(cr, t, x, s, md, ground=feet, backa=backa, **kw)
    if kneel:
        return YY.bhola_kneel(cr, t, x, s, md, ground=feet, backa=backa, **kw)
    return YY.bhola(cr, t, x, s, md, feet=feet, backa=None if pot else backa, legs=legs, y=y, pot=pot, **kw)


def dhani(cr, t, x, s, mood="calm", flip=True, front=(-0.32, -0.55), backa=(0.3, -0.25), feet=FL, alpha=1.0,
          blur=0.0, hits=(), ph=0.0, rods=True, hand="open"):
    """Seth Dhaniram alive (yy_cast; in the memory window), facing left by default."""
    return YY.dhani(cr, t, x, s, SOUL_MOODS.get(mood, mood), feet=feet, front=front, backa=backa, hits=hits,
                    flip=flip, alpha=alpha, blur=blur, rods=rods, ph=ph, hand=hand)


def thirsty(cr, t, x, s, flip=False, front=(-1.1, -0.9), feet=FL, alpha=1.0, ph=0.0, bowl=True):
    """A thirsty man holding out an empty bowl (six_cast_c's farmer). Returns his points and 'bowl' (user xy)."""
    pts = fig(cr, C.FARMER, "c6_farmer", t, x, s, front=front, backa=(0.2, -0.3), flip=flip, alpha=alpha,
              feet=feet, ph=ph, rods=False)
    if bowl:
        hx, hy = to_user(cr, pts["handF"])
        bx, by = hx + (-1 if flip else 1) * 12 * s / 0.34, hy + 18 * s / 0.34
        prop(cr, "dv_bowl", bx, by, 0.42 * s / 0.34, alpha=alpha)
        pts["bowl"] = (bx, by - 30 * s / 0.34)
    return pts


def water_pot(cr, x, y, s, alpha=1.0, rot=0.0):
    """Bhola's clay water pot (yy_cast) standing with its bottom at (x, y); s ~ its height / 320 px.
    Returns its mouth (user xy)."""
    k = s * 1.2
    return YY.pot(cr, x, y - 100 * k, k, rot=rot, alpha=alpha)


def safe(cr, x, y, s, alpha=1.0, open_=0.0):
    """Dhaniram's iron safe (yy_cast; pivot at its bottom centre)."""
    YY.safe(cr, x, y, s, open_=open_, alpha=alpha)


def _seated(cr, rig, key, t, x, s, seat, front, backa, head, flip, alpha, blur, hits, ph, swap=None, ground=FL,
            seat_h=246.0, extra=None):
    """A man() puppet seated on a throne or bench (its legs swapped for the seated-legs sprite)."""
    hy = ground - seat_h * s
    prop(cr, seat, x, hy, s, flip=flip, alpha=alpha, blur=blur)
    ang = man_angles(key, t, front, backa, head, (0.0, 0.0), hits, ph)
    return puppet(cr, rig, x, hy, s, bob_rot(t, ph, 0.006), flip, ang, alpha, blur,
                  hide=(key + "_legF", key + "_legB"), swap=swap, extra=extra)


# ------------------------------------------------------------------ the court's puppets


def chitra(cr, t, x, s=S, hold=1.0, flip=False, head=0.0, hits=(), ph=0.3, alpha=1.0, blur=0.0, front=None,
           backa=None):
    """Chitragupta (garuda_cast), his scroll hand raised by `hold`. Returns his points (device)."""
    fr = front or mix((-0.4, -0.5), (-1.1, -0.45), hold)
    ba = backa or mix((0.3, -0.3), (-1.0, -0.6), hold)
    return fig(cr, GC.CHITRA, "gp_chitra", t, x, s, front=fr, backa=ba, head=head + 0.06 * hold, hits=hits,
               flip=flip, alpha=alpha, blur=blur, feet=FL, ph=ph)


def messenger(cr, t, x, s=S, flip=True, front=(-0.4, -0.5), backa=(0.3, -0.3), hold="staff", head=0.0, legs=(0, 0),
              alpha=1.0, blur=0.0, hits=(), ph=0.0, rot=0.0, y=None, extra=None):
    """A Yamaduta (garuda_cast), facing left by default, his staff or noose in the front hand."""
    ex = dict(extra or {})
    if hold == "staff":
        ex["gp_duta_armF_lo"] = held_grip("gp_dstaff", front, 0.62, 0.0, 40, alpha, blur)
    elif hold == "noose":
        ex["gp_duta_armF_lo"] = held("gp_noose", front, 0.62, 150, 0.0, alpha, blur)
    return fig(cr, GC.DUTA, "gp_duta", t, x, s, front=front, backa=backa, head=head, legs=legs, hits=hits, flip=flip,
               alpha=alpha, blur=blur, feet=FL, ph=ph, extra=ex, rot=rot, y=y)


YAMA_HEADS = {"calm": "rr_yama_head", "smile": "sb_yama_head_smile", "fierce": "yc_yama_head_fierce",
              "shame": "sb_yama_head_shame"}


def yama(cr, t, x, s=S, mood="calm", flip=False, front=(-0.32, -0.55), backa=(0.3, -0.3), head=0.0, legs=(0, 0),
         alpha=1.0, blur=0.0, hits=(), ph=0.6, rot=0.0, y=None, kneel=False, danda=True, extra=None, rods=True):
    """Yama Dharmaraja (ruru_cast) standing (or kneeling), facing right by default, his danda in the back hand."""
    ex = dict(extra or {})
    if danda:
        ex["rr_yama_armB_lo"] = held_grip("rr_danda", backa, 0.68, 0.0, 120, alpha, blur)
    return fig(cr, RU.YAMA, "rr_yama", t, x, s, front=front, backa=backa, head=head, legs=legs, hits=hits, flip=flip,
               alpha=alpha, blur=blur, rods=rods, rot=rot, feet=FL, ph=ph, extra=ex,
               swap={"rr_yama_head": YAMA_HEADS[mood]}, kneel="yc_yama_kneel" if kneel else None, y=y)


def yama_throne(cr, t, x, s=S, rise=0.0, mood="calm", flip=False, front=None, backa=None, head=0.0, alpha=1.0,
                blur=0.0, hits=(), ph=0.6, throne=True, step=110.0):
    """Yama on his throne (mandhata_cast's md_throne) at x; rise 0 = seated, 1 = standing in front of it (a quick
    rod-puppet lift, the seated legs swapped for the standing ones half-way). Returns his points (device)."""
    if throne:
        prop(cr, "md_throne", x, FL, s, flip=flip, alpha=alpha, blur=blur)
    q = clamp(rise)
    e = ease(q)
    sg = -1 if flip else 1
    hy = (FL - 246 * s) + ((FL - 434 * s) - (FL - 246 * s)) * e
    xx = x + sg * step * s * e
    fr = front or mix((-0.55, -0.85), (-0.32, -0.55), e)
    ba = backa or (0.3, -0.3)
    hide = ()
    if q < 0.5:
        prop(cr, "gp_yama_seat", xx, hy, s, flip=flip, alpha=alpha, blur=blur)
        hide = ("rr_yama_legF", "rr_yama_legB")
    ang = man_angles("rr_yama", t, fr, ba, head, (0.0, 0.0), hits, ph)
    ex = {"rr_yama_armB_lo": held_grip("rr_danda", ba, 0.68, 0.0, 120, alpha, blur)}
    b_extra = 5 * math.sin(math.pi * q) if 0 < q < 1 else 0.0
    return puppet(cr, RU.YAMA, xx, hy, s, bob_rot(t, ph, 0.006), flip, ang, alpha, blur + b_extra, hide=hide,
                  swap={"rr_yama_head": YAMA_HEADS[mood]}, extra=ex)


def fan_arms(cr, t, x, hip_y, s, flip=False, n=7, spread=1.0, ph=0.0):
    """A fan of extra arms (Yama's terrible form): copies of his arm, each at its own angle, all from the shoulder."""
    for k in range(n):
        u = k / (n - 1)
        up = -0.5 - 2.6 * u * spread + 0.06 * math.sin(t * 1.3 + k)
        lo = -0.5 + 0.35 * math.sin(k * 1.7)
        ang = {"rr_yama_armF_up": up + 0.32, "rr_yama_armF_lo": lo + 0.55, "rr_yama_head": 0.0,
               "rr_yama_armB_up": 0.0, "rr_yama_armB_lo": 0.0, "rr_yama_legF": 0.0, "rr_yama_legB": 0.0}
        puppet(cr, RU.YAMA, x, hip_y, s, 0.0, flip, ang, 1.0, 0.0, rods=False,
               only=("rr_yama_armF_up", "rr_yama_armF_lo"))


def giant(cr, t, x, ground, s, alpha=1.0, toss=0.0, raise_=1.0, fan=1.0, eyes=1.0, store=None, fan_a=0.75):
    """Yama's terrible form: seated on his buffalo (facing right), the fierce face under a fire halo, the danda raised
    in the front hand, the noose in the back hand, a fan of shadow arms behind, glowing eyes. Returns his points."""
    hip_x, hip_y = x + YC.BUF_SEAT[0] * s, ground + YC.BUF_SEAT[1] * s
    if fan > 0.01:
        silhouette(cr, lambda c_: fan_arms(c_, t, hip_x, hip_y, s * 1.05, spread=fan), fan_a * alpha * fan, col=SIL)
    nx, ny = x + YC.BUF_NECK[0] * s, ground + YC.BUF_NECK[1] * s
    prop(cr, "yc_buf_body", x, ground, s, alpha=alpha)
    prop(cr, "yc_buf_head", nx, ny, s, rot=toss, alpha=alpha)
    prop(cr, "gp_yama_seat", hip_x, hip_y, s, alpha=alpha)
    fr = mix((-0.6, -0.6), (-2.05, -0.45), raise_)
    ba = (-0.55, -0.9)
    ang = man_angles("rr_yama", t, fr, ba, -0.05, (0.0, 0.0), (), 0.6)
    st = {} if store is None else store
    ex = {"rr_yama_armF_lo": held_grip("rr_danda", fr, 0.68, 0.0, 60, alpha, 0.0, st),
          "rr_yama_armB_lo": held("gp_noose", ba, 0.55, 150, 0.0, alpha)}
    pts = puppet(cr, RU.YAMA, hip_x, hip_y, s, bob_rot(t, 0.6, 0.004), False, ang, alpha, 0.0,
                 hide=("rr_yama_legF", "rr_yama_legB"), swap={"rr_yama_head": "yc_yama_head_fierce"}, extra=ex,
                 rods=False)
    if eyes > 0.01:
        ex_, ey_ = to_user(cr, pts["head"])
        ex_ += 26 * s
        warm(cr, ex_, ey_ - 6 * s, 60 * s + 10, 0.9 * eyes * alpha, col=(1.0, 0.25, 0.08))
        sparkle(cr, ex_, ey_ - 6 * s, 26 * s + 4, 0.8 * eyes * alpha, (1.0, 0.55, 0.3))
    pts["danda"] = st.get("top")
    return pts


def shravana(cr, t, x, s, feet=FL, flip=False, front=(-2.0, -2.2), backa=(0.25, -0.3), head=0.0, alpha=1.0,
             blur=0.0, ph=0.0, y=None, glow_a=1.0, mood="calm", rods=True, rot=0.0):
    """A Shravana: a pale silver-blue son of Brahma with a great ear and a big eye, a soft blue glow; by default the
    front hand shades his eyes (looking far)."""
    hy = feet - 434 * s if y is None else y
    if glow_a > 0.01:
        glow(cr, x, hy - 120 * s, 520 * s + 40, 0.5 * glow_a * alpha)
        warm(cr, x, hy - 120 * s, 340 * s, 0.35 * glow_a * alpha, col=(0.75, 0.88, 1.0))
    return fig(cr, YC.SHR, "yc_shr", t, x, s, front=front, backa=backa, head=head, flip=flip, alpha=alpha, blur=blur,
               feet=feet, ph=ph, y=y, rods=rods, rot=rot,
               swap={"yc_shr_head": "yc_shr_head" + ("_smile" if mood == "smile" else "")})


def munim(cr, t, x, ground, s, sly=False, write=0.0, alpha=1.0):
    """Dhaniram's munim seated on the floor behind his low desk (facing right), writing (write = pen stroke phase)."""
    pen = 0.12 * math.sin(write * 12) if write > 0 else 0.0
    fr = (-0.95 + pen, -1.05)
    pts = _seated(cr, YC.MUNIM, "yc_munim", t, x, s, "yc_munim_seat", fr, (-0.4, -0.9), 0.08, False, alpha, 0.0, (),
                  0.4, swap={"yc_munim_head": "yc_munim_head" + ("_sly" if sly else "")}, ground=ground,
                  seat_h=268.0)
    prop(cr, "yc_desk", x + 250 * s, ground, s, alpha=alpha)
    return pts


# ------------------------------------------------------------------ the city map


def map_point(a, b, u):
    return a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u


S_ROAD = [MAP_S, (900, 960), (800, 1010), (640, 1060)]
E_ROAD = [MAP_E, (1640, 640), (1780, 610), (1940, 600)]


def city_map(cr, t, gate_in=(0.0, 0.0, 0.0, 0.0), dark_s=0.0, lit_e=0.0, blaze_e=0.0, a=1.0):
    """A pictorial plan of Yama's city: a diamond of walls round Yama's palace, four roads (the south one dark and
    thorny, the east one golden and set with jewels), the four gates standing upright at the corners (N, E, S, W pop
    in at gate_in); dark_s darkens the south gate under a storm cloud, lit_e / blaze_e light the east gate."""
    if a <= 0.01:
        return
    cr.save()
    # roads
    for pts, col, w_ in ((S_ROAD, (0.36, 0.22, 0.20), 46), (E_ROAD, (1.0, 0.78, 0.30), 46),
                         ([MAP_N, (960, 300)], (0.84, 0.70, 0.50), 40), ([MAP_W, (220, 650), (-20, 640)],
                                                                       (0.84, 0.70, 0.50), 40)):
        cr.new_path()
        pc.spath(cr, pts, closed=False)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_operator(cairo.OPERATOR_MULTIPLY)
        cr.set_source_rgba(*col, 0.9 * a)
        cr.set_line_width(w_)
        cr.stroke_preserve()
        cr.set_operator(cairo.OPERATOR_OVER)
        cr.set_source_rgba(*pc.INK, 0.55 * a)
        cr.set_line_width(3)
        cr.set_dash([18, 14])
        cr.stroke()
        cr.set_dash([])
    for i in range(7):                                            # thorns along the south road
        u = (i + 0.5) / 7
        k = min(2, int(u * 3))
        px, py = map_point(S_ROAD[k], S_ROAD[k + 1], u * 3 - k)
        for sg in (-1, 1):
            cr.move_to(px + sg * 30, py - 6)
            cr.line_to(px + sg * 46, py - 22)
            cr.line_to(px + sg * 38, py)
        cr.set_source_rgba(0.25, 0.12, 0.10, 0.9 * a)
        cr.set_line_width(4)
        cr.stroke()
    for i in range(6):                                            # jewels along the east road
        u = (i + 0.5) / 6
        k = min(2, int(u * 3))
        px, py = map_point(E_ROAD[k], E_ROAD[k + 1], u * 3 - k)
        sparkle(cr, px, py, 10 + 4 * math.sin(t * 3 + i), (0.6 + 0.4 * lit_e) * a,
                ((0.6, 0.9, 1.0), (1.0, 0.5, 0.5), (0.6, 1.0, 0.6))[i % 3])
    # the city inside the walls
    pc.poly(cr, [MAP_N, MAP_E, MAP_S, MAP_W])
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(0.93, 0.82, 0.62, a)
    cr.fill()
    cr.set_operator(cairo.OPERATOR_OVER)
    for i, (hx, hy) in enumerate(((760, 600), (840, 520), (1120, 560), (1180, 690), (800, 760), (1060, 790),
                                  (700, 680), (1250, 640))):
        pc.poly(cr, [(hx - 22, hy), (hx + 22, hy), (hx + 22, hy - 24), (hx, hy - 40), (hx - 22, hy - 24)])
        cr.set_source_rgba(*((0.80, 0.50, 0.30) if i % 2 else (0.70, 0.56, 0.40)), 0.9 * a)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, a)
        cr.set_line_width(2.5)
        cr.stroke()
    prop(cr, "sb_yhall", MAP_C[0], MAP_C[1] + 70, 0.13, alpha=a)
    cr.set_line_join(cairo.LINE_JOIN_MITER)
    for lw_, col_ in ((34, pc.INK), (24, (0.72, 0.58, 0.44))):
        pc.poly(cr, [MAP_N, MAP_E, MAP_S, MAP_W])
        cr.set_source_rgba(*col_, a)
        cr.set_line_width(lw_)
        cr.stroke()
    for (xa, ya), (xb, yb) in zip([MAP_N, MAP_E, MAP_S, MAP_W], [MAP_E, MAP_S, MAP_W, MAP_N]):
        n = int(math.hypot(xb - xa, yb - ya) / 22)
        for i in range(2, n - 1):
            cr.arc(xa + (xb - xa) * i / n, ya + (yb - ya) * i / n, 2.6, 0, 2 * math.pi)
            cr.set_source_rgba(1.0, 0.95, 0.80, 0.8 * a)
            cr.fill()
    # gates (back to front)
    for (gx, gy), kind, ti in ((MAP_N, "P", gate_in[0]), (MAP_W, "P", gate_in[3]), (MAP_E, "E", gate_in[1]),
                               (MAP_S, "S", gate_in[2])):
        q = back(clamp((t - ti) / 0.35), 1.6)
        if q <= 0.01:
            continue
        if kind == "S" and dark_s > 0:                   # a dark pall and a storm cloud behind the south gate
            g = cairo.RadialGradient(gx, gy - 80, 20, gx, gy - 80, 230)
            g.add_color_stop_rgba(0, 0.22, 0.10, 0.20, 0.7 * dark_s * a)
            g.add_color_stop_rgba(0.6, 0.30, 0.14, 0.24, 0.45 * dark_s * a)
            g.add_color_stop_rgba(1, 0.30, 0.16, 0.26, 0.0)
            cr.save()
            cr.set_operator(cairo.OPERATOR_MULTIPLY)
            cr.arc(gx, gy - 80, 230, 0, 2 * math.pi)
            cr.set_source(g)
            cr.fill()
            cr.restore()
            prop(cr, "cloud", gx + 6, gy - 160, 0.3 * (0.7 + 0.3 * dark_s), alpha=dark_s * a)
        if kind == "E" and lit_e > 0:
            gold_light(cr, t, gx, gy - 70, 260 + 140 * blaze_e, (0.6 + 0.6 * blaze_e) * lit_e * a)
            if blaze_e > 0:
                aura(cr, t, gx, gy - 70, 70, 230 + 30 * math.sin(t * 2), 0.8 * blaze_e * a, n=18, spin=0.08)
        prop(cr, "yc_gate_" + kind, gx, gy, MAP_GS * q, alpha=clamp(q) * a)
    cr.restore()


def map_ui(cr, t, gate_in, a=1.0):
    """The compass letters beside the four gates (screen coordinates: the map is drawn unzoomed)."""
    for (x, y), ch, ti in (((MAP_N[0] + 125, MAP_N[1] - 60), "N", gate_in[0]),
                           ((MAP_E[0] + 40, MAP_E[1] - 200), "E", gate_in[1]),
                           ((MAP_S[0] + 170, MAP_S[1] - 30), "S", gate_in[2]),
                           ((MAP_W[0] - 135, MAP_W[1] - 60), "W", gate_in[3])):
        badge(cr, t, ti + 0.1, ch, x, y, 34, a, color=RED if ch in "SE" else INK)


# ------------------------------------------------------------------ y1  Yama's city: four gates


def y1_times(c):
    """(card out, gates pop) for y1: the chapter card holds at least 1.7 s, then the four gates pop in."""
    t_out = max(c["t0"] + 1.7, c["C"] - 0.3)
    return t_out, max(c["C"], t_out + 0.25)


def s_y1(cr, t, tl, t0, t1):
    c = cues(tl, "y1")
    t_out, tC = y1_times(c)                             # the chapter card holds, then flies up
    tD = max(c["D"], tC + 1.0)
    tS = max(c["S"], tD + 0.6)
    gate_in = (tC, tC + 0.22, tC + 0.44, tC + 0.66)
    dark_s = prog(t, tS - 0.15, 0.5)
    u = 0.88 * ease((t - tD + 0.2) / max(1.0, tS - tD + 0.6)) if t > tD - 0.2 else 0.0
    seg = min(2, int((1 - u) * 3))
    px, py = map_point(S_ROAD[seg], S_ROAD[seg + 1], (1 - u) * 3 - seg)

    def scene(cr):
        city_map(cr, t, gate_in, dark_s=dark_s, lit_e=prog(t, tC + 0.9, 0.6))
        # little Dhaniram led up the south road by a messenger
        if t > tD - 0.4:
            a_ = prog(t, tD - 0.4, 0.3)
            mx, my = px - 60, py + 34
            messenger(cr, t, mx, 0.075, flip=False, hold="none", front=(-1.2, -0.2), y=my - 434 * 0.075,
                      alpha=a_, legs=walk_legs(math.sin(t * 9) if 0 < u < 1 else 0.0), rot=0.0)
            light_rope(cr, [(mx + 18, my - 36), ((mx + px) / 2, py - 20), (px, py - 24)], a_ * 0.8, 0.3)
            dsoul(cr, t, px, py, 62, mood="calm", flip=True, alpha=a_, walk=t * 9 if 0 < u < 0.88 else None,
                  halo=0.5)
    fade_in(cr, prog(t, t_out - 0.1, 0.5), scene)
    chapter(cr, t, t0 - 0.2, t_out, [[("YAMA'S", INK), ("CITY", RED)]], "GARUDA PURANA · PRETA KALPA")

    def ui(cr):
        if t > t_out:
            if t < tD:
                head(cr, t, "YAMA'S CITY HAS", t_out + 0.05, "FOUR GATES", tC + 0.1, under=tC + 0.8)
            else:
                head(cr, t, "FOR PEOPLE LIKE DHANIRAM:", tD, "THE SOUTH GATE", tS, under=tS + 0.4)
            map_ui(cr, t, gate_in)
            plate(cr, t, tD + 0.3, "DHANIRAM", px - 150, py - 40, 26, t_out=tS + 0.8)
            if t > tS:
                red_ring(cr, MAP_S[0], MAP_S[1] - 72, 112, 96, prog(t, tS + 0.05, 0.45), 9)
    return dict(ui=ui, flash=flash_at(t, t_out, 0.2) + flash_at(t, tC, 0.1), night=0.06 * dark_s)


# ------------------------------------------------------------------ the hall of Chitragupta (y2, y3, y5, y7, y8)


def hall_cast(cr, t, cg_hold=1.0, dh_mood="calm", dh_arms="rest", dh_shiver=0.0, rope=1.0, scroll_len=0.0,
              scroll_a=1.0, crosses=None, cg_head=0.0, cg_hits=(), dh_x=DH_X, du=True, dh_alpha=1.0):
    """Chitragupta on the left with his scroll, little Dhaniram on the right on the messenger's noose. Returns
    (Chitragupta's points, Dhaniram's soul, the scroll's top)."""
    cp = chitra(cr, t, CG_X, hold=cg_hold, head=cg_head, hits=cg_hits)
    hand = to_user(cr, cp["handF"])
    top = (hand[0] + 34, hand[1] - 4)
    if scroll_len > 4:
        deeds_scroll(cr, top[0], top[1], 220, scroll_len, ROWS, alpha=scroll_a, crosses=crosses)
    if du:
        dp = messenger(cr, t, DU_X, S, flip=True, hold="none", front=(-1.15, -0.25), ph=0.4)
        dh = to_user(cr, dp["handF"])
    dsp = dsoul(cr, t, dh_x, FL, DH_H, mood=dh_mood, arms=dh_arms, shiver=dh_shiver, alpha=dh_alpha)
    if du and rope > 0.01:
        wx, wy = dh_x, FL - 0.45 * DH_H
        light_rope(cr, [dh, ((dh[0] + wx) / 2, wy + 30), (wx + 0.18 * DH_H, wy)], rope * 0.9, 0.55)
        noose_loop(cr, t, wx, wy, 0.2 * DH_H + 6, 0.07 * DH_H + 4, rope * 0.9)
    return cp, dsp, top


def s_y2(cr, t, tl, t0, t1):
    c = cues(tl, "y2")
    tK, tC, tY, tM, tH = c["K"], c["C"], c["Y"], c["M"], c["H"]
    hall(cr, t)
    glow(cr, CG_X + 60, FL - 380, 420, 0.35)
    hold = keyed(t, [(t0, 0.0), (tY + 0.2, 1.0)], 0.35, 1.2)
    unroll = ease((t - tH + 0.3) / 1.4) if t > tH - 0.3 else 0.0
    cp, dsp, top = hall_cast(cr, t, cg_hold=hold, scroll_len=40 + 420 * unroll if hold > 0.3 else 0.0,
                             scroll_a=clamp(hold * 1.5), cg_head=0.1 * (1 - hold) * prog(t, tK, 0.3))
    # the doorkeeper leans in and whispers, then steps back out
    bk, kk, ak = depth(t, t0 - 0.3, 0.4, t_out=tY - 0.1, out_dur=0.45)
    lean = keyed(t, [(t0, 0.0), (tK - 0.2, 1.0), (tY - 0.3, 0.0)], 0.3, 1.2)
    kp = soldier(cr, t, 800 + 60 * (1 - ak), FL, S * kk, flip=True, alpha=ak, blur=bk, rot=-0.07 * lean, ph=0.7,
                 rods=True)
    mouth = to_user(cr, kp["head"])
    dev_c = cp["top"]
    dev_k = kp["top"]
    dev_dh = dev(cr, DH_X, FL - DH_H - 70)

    def ui(cr):
        if t < tY:
            head(cr, t, "THE DOORKEEPER TOLD", t0 + 0.05, "CHITRAGUPTA", tC)
        else:
            head(cr, t, "CHITRAGUPTA IS", tY - 0.1, "YAMA'S ACCOUNTANT", tM, under=tH + 0.2)
        tag(cr, t, t0 + 0.3, "DOORKEEPER", dev_k[0] + 20, dev_k[1] - 50, 32, t_out=tK - 0.1)
        tag(cr, t, tY - 0.1, "CHITRAGUPTA", dev_c[0] - 10, dev_c[1] - 60, 34)
        plate(cr, t, t0 + 0.6, "DHANIRAM", dev_dh[0], dev_dh[1], 26, t_out=tM)
        if tK - 0.2 < t < tY:
            talk_marks(cr, t, tK - 0.2, mouth[0] - 70, mouth[1] - 10, alpha=ak, dirn=-1)
            cloud_text(cr, t, 600, 320, 0.5, [("DHANIRAM", 52, RED, -22, tK + 0.1), ("IS HERE", 44, INK, 30,
                                                                                        tK + 0.25)],
                       flip=True, t_in=tK, alpha=1 - prog(t, tY - 0.3, 0.3))
        word_card(cr, t, tM - 0.1, "मुनीम", "MUNEEM", "ACCOUNTANT", 1100, 480, 0.9)
    return dict(ui=ui, night=0.12, lift=1.0, flash=flash_at(t, tM, 0.12))


def s_y3(cr, t, tl, t0, t1):
    c = cues(tl, "y3")
    tH, tQ = c["H"], c["Q"]
    hall(cr, t)
    glow(cr, CG_X + 60, FL - 380, 420, 0.35)
    _, dsp, top = hall_cast(cr, t, scroll_len=460 + 30 * math.sin(math.pi * prog(t, tH, 0.5)),
                            cg_head=-0.08 * prog(t, tH, 0.4))
    if t > tH:                                          # the rows flash, one after another
        k = int((t - tH) * 6) % len(ROWS)
        ry = top[1] + 84 + 50 * k
        if ry < top[1] + 440:
            glow(cr, top[0], ry, 120, 0.35)
    dev_q = dev(cr, dsp["head"][0], dsp["head"][1] - 70)

    def ui(cr):
        head(cr, t, "BUT HOW DOES HE", t0 + 0.05, "KNOW EVERYTHING?", tQ - 0.1)
        big_q(cr, t, tQ - 0.05, 960, 560, 260)
        mark(cr, t, tH, "?", dev_q[0], dev_q[1], 80)
    return dict(ui=ui, night=0.12, lift=1.0, flash=flash_at(t, tQ, 0.12))


# ------------------------------------------------------------------ y4  the Shravanas


SHR_POSES = (((-2.25, -1.05), (0.25, -0.3)),        # shading his eyes, looking far
             ((-1.5, -0.12), (-2.9, -1.2)),         # pointing, the back hand cupped at his ear
             ((-0.6, -1.3), (-2.9, -1.2)))          # a hand at his chest, the back hand cupped at his ear


def ear_waves(cr, t, x, y, s, side, a=1.0):
    """Sound coming in to a great ear: three arcs on the outer side (side -1 = behind a right-facing head), moving
    in toward the ear."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    a0 = math.pi if side < 0 else 0.0
    for k in range(3):
        u = 1 - ((t * 1.3 + k / 3) % 1.0)
        r = (26 + 60 * u) * s
        cr.new_path()
        cr.arc(x, y, r, a0 - 0.6, a0 + 0.6)
        cr.set_source_rgba(0.25, 0.40, 0.85, 0.85 * a * math.sin(math.pi * u))
        cr.set_line_width(5 * s + 1)
        cr.stroke()
    cr.restore()


BANDS = (("SKY", 250, 520, (0.70, 0.84, 1.0)), ("EARTH", 520, 720, (0.80, 0.90, 0.60)),
         ("PATALA", 720, 1080, (0.38, 0.30, 0.34)))
SHR_HOME = ((780, FL), (1000, FL), (1220, FL))                       # standing in a row (phase A)
SHR_WORLD = ((1180, 700, 0.26), (700, 515, 0.24), (1560, 975, 0.24))  # earth, sky, patala (phase B)


def world_bands(cr, t, on=(1.0, 1.0, 1.0), a=1.0):
    """The world in three bands: the sky (clouds, stars), the earth (a strip of land with houses, trees and people),
    patala below (dark rock, roots, glowing gems). on = how lit each band is."""
    if a <= 0.01:
        return
    cr.save()
    for (name, y0, y1, col), o in zip(BANDS[:2], (on[1], on[0])):
        cr.rectangle(0, y0, W, y1 - y0)
        cr.set_operator(cairo.OPERATOR_MULTIPLY)
        k = 0.45 + 0.55 * o
        cr.set_source_rgba(*tuple(1 - (1 - cc) * k for cc in col), a)
        cr.fill()
    cr.set_operator(cairo.OPERATOR_OVER)
    for x, y, s in ((420, 340, 0.4), (1460, 300, 0.5), (1760, 430, 0.35)):
        prop(cr, "rr_lcloud", x + 20 * math.sin(t * 0.3 + x), y, s, alpha=0.8 * a)
    for i, (x, y) in enumerate(((300, 290), (560, 420), (1050, 300), (1320, 450), (1650, 300))):
        prop(cr, "star", x, y, 0.35, rot=0.3 * i, alpha=(0.6 + 0.3 * math.sin(t * 3 + i)) * a * on[1])
    prop(cr, "c6_ground", 960, 716, 1.42, alpha=a)
    cr.rectangle(0, 760, W, H - 760)                                # patala: dark rock under the earth
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    k = 0.5 + 0.5 * on[2]
    cr.set_source_rgba(0.42 + 0.1 * (1 - k), 0.32 + 0.1 * (1 - k), 0.38 + 0.1 * (1 - k), a)
    cr.fill()
    cr.set_operator(cairo.OPERATOR_OVER)
    for x in (120, 640, 1180, 1640):
        pc.poly(cr, [(x, 1080), (x + 40, 980), (x + 110, 940), (x + 190, 990), (x + 230, 1080)])
        cr.set_source_rgba(0.30, 0.22, 0.24, 0.8 * a)
        cr.fill()
    for x, s in ((330, 0.2), (1720, 0.22), (900, 0.17)):
        prop(cr, "tree", x, 712, s, rot=sway(t, 0.006, 0.3, x), alpha=0.9 * a)
    for x, s in ((560, 0.16), (1420, 0.15)):
        prop(cr, "dv_house", x, 716, s, alpha=a)
    for i, x in enumerate((700, 1500, 1840)):                       # little people
        fig(cr, C.FARMER, "c6_farmer", t, x, 0.11, flip=i % 2 == 0, feet=716, rods=False, ph=i)
    cr.set_source_rgba(0.30, 0.20, 0.16, 0.7 * a)                   # roots and rock in patala
    cr.set_line_width(5)
    for x in (300, 820, 1340, 1750):
        cr.move_to(x, 740)
        cr.curve_to(x + 30, 800, x - 40, 860, x + 10, 930)
    cr.stroke()
    for i, (x, y) in enumerate(((520, 860), (1100, 900), (1800, 840), (240, 960))):
        sparkle(cr, x, y, 12 + 3 * math.sin(t * 2 + i), 0.8 * a * on[2], ((0.6, 1.0, 0.7), (1.0, 0.5, 0.5))[i % 2])
    cr.restore()


def s_y4(cr, t, tl, t0, t1):
    c = cues(tl, "y4")
    tB, tS, tE, tA, tP, tG, tL, tV = (c[k] for k in ("B", "S", "E", "A", "P", "G", "L", "V"))
    wa = prog(t, tE - 0.1, 0.5)                          # the world fades in
    world_bands(cr, t, (prog(t, tE, 0.4), prog(t, tA, 0.4), prog(t, tP, 0.4)), wa)
    # Brahma in a medallion (phase A)
    aa = 1 - wa
    if aa > 0.01:
        glow(cr, 960, 560, 700, 0.35 * aa)

        def brahma_in(cr_):
            glow(cr_, 330, 520, 200, 0.6)
            prop(cr_, "c6_brahma_head", 330, 600, 0.36)
        medallion(cr, t, min(tB - 0.1, t0 + 0.3), 330, 520, 135, brahma_in, "BRAHMA", alpha=aa)
        for k in range(3):
            dotted(cr, [(470, 520), (560, 560 + 40 * (k - 1)), (SHR_HOME[k][0] - 60, 620)], prog(t, tS - 0.2, 0.5),
                   24, 5, (0.40, 0.55, 0.95), 0.8 * aa)
    eyes, ears = [], []
    for k in range(3):
        hx, hf = SHR_HOME[k]
        wx, wf, ws = SHR_WORLD[k]
        t_go = (tE, tA, tP)[k]
        u = ease((t - t_go + 0.1) / 0.7) if t > t_go - 0.1 else 0.0
        b_, k_, a_ = depth(t, tS - 0.15 + 0.15 * k, 0.5)
        if t < tS - 0.15 + 0.15 * k:
            continue
        x = hx + (wx - hx) * u
        f = hf + (wf - hf) * u - 140 * math.sin(math.pi * u)
        s_ = (0.42 + (ws - 0.42) * u) * k_
        bob = 6 * math.sin(t * 2 + k)
        if u < 0.95 or k != 0:
            prop(cr, "rr_lcloud", x, f + bob + 16, s_ * 0.9, alpha=0.9 * a_)
        flip = k == 2 and u > 0.5
        fr, ba = SHR_POSES[k]
        pts = shravana(cr, t, x, s_, feet=f + bob, flip=flip, front=fr, backa=ba, alpha=a_, blur=b_, ph=k * 1.3,
                       mood="calm", rods=u < 0.5, glow_a=0.6)
        hd = to_user(cr, pts["head"])
        sg = -1 if flip else 1
        ears.append((hd[0] - sg * 40 * s_ / 0.3, hd[1] - 5, s_))
        eyes.append((hd[0] + sg * 18 * s_ / 0.3, hd[1] - 8, sg, s_))
    for i, (ex, ey, s_) in enumerate(ears):              # they listen: sound coming in to the great ears
        if t > tL:
            ear_waves(cr, t, ex, ey, s_ / 0.25, -1 if not (i == 2 and t > tP + 0.5) else 1, prog(t, tL + 0.1 * i, 0.3))
    for i, (ex, ey, sg, s_) in enumerate(eyes):          # they see: beams from the eyes
        q = prog(t, tV + 0.1 * i, 0.4)
        if q > 0:
            L_ = 520 * q
            sweep = 0.25 * math.sin(t * 1.2 + i)
            cr.save()
            cr.translate(ex, ey)
            cr.scale(sg, 1)
            cr.rotate(0.15 + sweep)
            g = cairo.LinearGradient(0, 0, L_, 0)
            g.add_color_stop_rgba(0, 1.0, 0.97, 0.80, 0.55)
            g.add_color_stop_rgba(1, 1.0, 0.97, 0.80, 0.0)
            cr.move_to(0, 0)
            cr.line_to(L_, -70 * q)
            cr.line_to(L_, 70 * q)
            cr.close_path()
            cr.set_source(g)
            cr.fill()
            cr.restore()
    band_on = (prog(t, tA, 0.3), prog(t, tE, 0.3), prog(t, tP, 0.3))     # sky, earth, patala plates

    def ui(cr):
        if t < tS:
            head(cr, t, "THE GARUDA PURANA SAYS:", t0 + 0.05, "BRAHMA HAS SONS...", tB)
        elif t < tE:
            head(cr, t, "BRAHMA'S SONS:", tS - 0.1, "THE SHRAVANAS", tS)
        elif t < tL:
            head(cr, t, "THEY GO", tE - 0.1, "EVERYWHERE", tG - 0.2)
        else:
            head(cr, t, "THEY HEAR AND SEE", tL - 0.1, "FROM FAR AWAY", tV - 0.2, under=tV + 0.3)
        if t < tE + 0.3:
            word_card(cr, t, tS + 0.1, "श्रवण", "SHRAVAN", "HEARING", 1600, 520, 0.85, alpha=1 - prog(t, tE, 0.3))
            plate(cr, t, tS + 0.4, "SHRAVANAS · SONS OF BRAHMA", 1000, 960, 30, t_out=tE)
        for (name, y0, y1, _), on in zip(BANDS, band_on):
            plate(cr, t, {"SKY": tA, "EARTH": tE, "PATALA": tP}[name], name, 150, (y0 + y1) / 2 - (30 if
                                                                                                   name == "PATALA"
                                                                                                   else 0), 32)
    return dict(ui=ui, night=0.06 * wa, lift=1.0, flash=flash_at(t, tS, 0.15) + flash_at(t, tE, 0.1))


# ------------------------------------------------------------------ y5  everything said and done is reported


WIN5 = (1240, 545, 880, 500)                          # the memory window: centre, size


def s_y5(cr, t, tl, t0, t1):
    c = cues(tl, "y5")
    tH, tO, tK, tD, tC, tT = (c[k] for k in ("H", "O", "K", "D", "C", "T"))
    hall(cr, t, a=0.6)
    wx, wy, ww, wh = WIN5
    win_floor = wy + wh / 2 - 40

    def inner(cr_):
        prop(cr_, "sb_sack", wx + 330, win_floor - 170, 0.32)
        prop(cr_, "sb_sack", wx + 90, win_floor - 170, 0.3)
        safe(cr_, wx + 388, win_floor, 0.3)
        push = keyed(t, [(t0, 0.0), (tK - 0.2, 1.0)], 0.25, 1.6)
        dhani(cr_, t, wx + 230, 0.36, mood="angry" if t > tK - 0.3 else "calm", flip=True,
              front=mix((-0.3, -0.5), PUSH["front"], push),
              backa=PUSH["backa"], feet=win_floor, hits=[(tD, 0.6)], rods=False)
        prop(cr_, "dv_counter", wx + 200, win_floor, 0.36)
        back_off = ease((t - tD) / 0.8) if t > tD else 0.0
        thirsty(cr_, t, wx - 170 - 60 * back_off, 0.36, feet=win_floor,
                front=mix((-1.1, -0.9), (-0.4, -0.5), back_off))
        cloud_text(cr_, t, wx + 40, wy - 130, 0.46, [("NO FREE WATER!", 46, RED, -18, tK - 0.1),
                                                     ("MOVE ON!", 40, INK, 30, tK + 0.2)], flip=True, t_in=tK - 0.3)
    window(cr, t, t0 - 0.1, wx, wy, ww, wh, inner)
    # the Shravana hidden at the window's edge, then flying to Chitragupta's ear
    cp = chitra(cr, t, CG_X - 60, hold=1.0, head=0.08 * prog(t, tT - 0.3, 0.3))
    hand = to_user(cr, cp["handF"])
    cross_q = prog(t, tT + 0.25, 0.3)
    deeds_scroll(cr, hand[0] + 34, hand[1] - 4, 220, 470, ROWS, crosses={6: cross_q})
    ear = to_user(cr, cp["head"])
    p0, p2 = (wx - ww / 2 - 70, wy + 120), (ear[0] + 210, ear[1] + 250)
    p1 = ((p0[0] + p2[0]) / 2, 200)
    u = ease((t - tC + 0.1) / max(0.8, tT - tC + 0.3)) if t > tC - 0.1 else 0.0
    sx = (1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0]
    sy = (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1]
    if 0 < u < 1:
        pts = [((1 - v) ** 2 * p0[0] + 2 * (1 - v) * v * p1[0] + v * v * p2[0],
                (1 - v) ** 2 * p0[1] + 2 * (1 - v) * v * p1[1] + v * v * p2[1]) for v in (i / 40 * u for i in
                                                                                         range(41))]
        dotted(cr, pts, 1.0, 26, 5, (0.55, 0.70, 1.0), 0.8)
    peek = keyed(t, [(t0, 0.0), (tH, 1.0)], 0.3, 1.4)
    shp = shravana(cr, t, sx + 40 * (1 - peek) * (1 - u), 0.3, feet=sy, flip=u > 0.02,
                   front=(-2.25, -1.05) if u < 0.05 else ((-2.4, -0.4) if u < 1 else (-1.2, -1.6)),
                   backa=(-2.9, -1.2) if u < 0.05 else (0.25, -0.3), alpha=prog(t, t0, 0.3), rods=False,
                   rot=-0.25 * math.sin(math.pi * u), glow_a=0.6)
    sh_head = to_user(cr, shp["head"])
    if u < 0.05 and t > tH:
        ear_waves(cr, t, sh_head[0] - 40, sh_head[1], 1.0, -1, prog(t, tH, 0.3))
    if u >= 1:
        talk_marks(cr, t, tT, sh_head[0] - 60, sh_head[1] - 6, dirn=-1)
    dev_said = dev(cr, wx + 40, wy - 230)
    dev_done = dev(cr, wx + 60, wy + 40)
    dev_c = cp["top"]

    def ui(cr):
        if t < tC:
            head(cr, t, "SECRETLY OR OPENLY,", t0 + 0.05, "ALL YOU SAY AND DO", tK - 0.1)
        else:
            head(cr, t, "THE SHRAVANAS TELL", tC - 0.1, "CHITRAGUPTA", tT - 0.1, under=tT + 0.4)
        plate(cr, t, tK, "SAID", dev_said[0], dev_said[1], 30, color=RED, t_out=tC + 0.3)
        plate(cr, t, tD, "DONE", dev_done[0], dev_done[1], 30, color=RED, t_out=tC + 0.3)
        tag(cr, t, tC + 0.2, "CHITRAGUPTA", dev_c[0] - 10, dev_c[1] - 60, 32)
    return dict(ui=ui, night=0.1, lift=1.0, flash=flash_at(t, tT + 0.25, 0.12))


# ------------------------------------------------------------------ y6  the witnesses


def _wit_sun(cr, x, y):
    prop(cr, "sun", x, y, 0.32)


def _wit_moon(cr, x, y):
    cr.arc(x, y, 90, 0, 2 * math.pi)
    cr.set_source_rgba(0.30, 0.32, 0.50, 0.85)
    cr.fill()
    prop(cr, "moon", x + 10, y, 0.48)
    prop(cr, "star", x - 45, y - 40, 0.3)


def _wit_fire(cr, x, y):
    glow(cr, x, y, 120, 0.6)
    prop(cr, "flame0", x, y + 70, 0.36)


def _wit_wind(cr, x, y):
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for k, (dy, L_) in enumerate(((-40, 110), (0, 140), (40, 100))):
        cr.move_to(x - L_ / 2 - 20, y + dy)
        cr.curve_to(x - 10, y + dy - 10, x + 20, y + dy + 10, x + L_ / 2, y + dy)
        cr.arc_negative(x + L_ / 2, y + dy - 18, 18, math.pi / 2, -math.pi * 0.9)
        cr.set_source_rgb(0.25, 0.42, 0.62)
        cr.set_line_width(9)
        cr.stroke()
    prop(cr, "yc_flower", x - 50, y - 50, 0.6, rot=0.5)


def _wit_earth(cr, x, y):
    pc.poly(cr, [(x - 110, y + 90), (x - 110, y + 30), (x - 40, y - 10), (x + 30, y + 10), (x + 110, y - 20),
                 (x + 110, y + 90)])
    cr.set_source_rgb(0.58, 0.42, 0.24)
    cr.fill()
    prop(cr, "tree", x + 10, y + 20, 0.09)


def _wit_water(cr, x, y):
    cr.rectangle(x - 110, y - 10, 220, 110)
    cr.set_source_rgb(0.42, 0.66, 0.86)
    cr.fill()
    for k in range(3):
        cr.move_to(x - 100, y + 10 + 30 * k)
        for j in range(8):
            cr.curve_to(x - 100 + 25 * j + 8, y + 2 + 30 * k, x - 100 + 25 * j + 17, y + 18 + 30 * k,
                        x - 100 + 25 * (j + 1), y + 10 + 30 * k)
        cr.set_source_rgb(0.92, 0.97, 1.0)
        cr.set_line_width(5)
        cr.stroke()
    cr.move_to(x, y - 70)
    cr.curve_to(x + 20, y - 40, x + 20, y - 26, x, y - 22)
    cr.curve_to(x - 20, y - 26, x - 20, y - 40, x, y - 70)
    cr.set_source_rgb(0.42, 0.66, 0.86)
    cr.fill()


def _wit_day(cr, x, y):
    cr.rectangle(x - 110, y - 110, 220, 220)
    cr.set_source_rgb(0.80, 0.92, 1.0)
    cr.fill()
    prop(cr, "sun", x, y + 20, 0.24)
    cr.rectangle(x - 110, y + 40, 220, 80)
    cr.set_source_rgb(0.56, 0.74, 0.40)
    cr.fill()


def _wit_night(cr, x, y):
    cr.rectangle(x - 110, y - 110, 220, 220)
    cr.set_source_rgb(0.16, 0.18, 0.34)
    cr.fill()
    prop(cr, "moon", x + 20, y - 10, 0.36)
    for dx, dy in ((-60, -50), (-30, 30), (60, 50), (-70, 60)):
        prop(cr, "star", x + dx, y + dy, 0.22)


WITNESSES = (("SUN", _wit_sun), ("MOON", _wit_moon), ("FIRE", _wit_fire), ("WIND", _wit_wind),
             ("EARTH", _wit_earth), ("WATER", _wit_water), ("DAY", _wit_day), ("NIGHT", _wit_night))
WIT_XY = [(300 + 270 * (i % 4), 430 + 300 * (i // 4)) for i in range(8)]


def s_y6(cr, t, tl, t0, t1):
    c = cues(tl, "y6")
    tG, tHd = c["G"], c["Hd"]
    ts = [c[str(i + 1)] for i in range(8)]
    stone_floor(cr, 0.5, gold=0.0)
    hx, hy = 1530, 540
    q = back(clamp((t - tHd + 0.05) / 0.4), 1.6)
    beat = 1 + 0.06 * max(0.0, math.sin(t * 7.5)) ** 8 if t > tHd + 0.4 else 1.0
    if q > 0.01:
        glow(cr, hx, hy, 420, 0.7 * clamp(q))
        warm(cr, hx, hy, 300, 0.5 * clamp(q), col=(1.0, 0.45, 0.35))
        prop(cr, "yc_heart", hx, hy, 0.78 * q * beat, alpha=clamp(q))
        if t > tHd + 0.4:
            k = int((t - tHd - 0.4) / 0.84)
            for j in range(2):
                sound_rings(cr, hx, hy, t, tHd + 0.4 + 0.84 * k + 0.2 * j, n=1, rmax=260, alpha=0.4,
                            color=(0.7, 0.1, 0.1))
    dim = prog(t, tHd, 0.4)

    def ui(cr):
        if t < tHd:
            head(cr, t, "AND WHO ARE", t0 + 0.05, "THE WITNESSES?", tG + 0.1)
        else:
            head(cr, t, "AND MOST OF ALL...", tHd - 0.1, "YOUR OWN HEART", tHd + 0.05, under=tHd + 0.6)
        for i, ((label, fn), (x, y), ti) in enumerate(zip(WITNESSES, WIT_XY, ts)):
            medallion(cr, t, ti - 0.1, x, y, 100, (lambda f, xx, yy: lambda c_: f(c_, xx, yy))(fn, x, y), label,
                      dim=0.35 * dim)
    return dict(ui=ui, night=0.04, lift=1.0, flash=flash_at(t, tHd, 0.2))


# ------------------------------------------------------------------ y7, y8  jugaad? never wrong


CLOUD7 = (900, 520, 760, 440)


def s_y7(cr, t, tl, t0, t1):
    c = cues(tl, "y7")
    tM, tG, tY, tJ = c["M"], c["G"], c["Y"], c["J"]
    hall(cr, t)
    glow(cr, CG_X + 60, FL - 380, 420, 0.3)
    _, dsp, _ = hall_cast(cr, t, scroll_len=180, dh_mood="smug")
    cx, cy, cw, ch = CLOUD7
    hdx, hdy = dsp["head"]
    q = back(clamp((t - t0 - 0.1) / 0.4), 1.4)
    ca = clamp(q)
    if ca > 0.01:
        cr.save()
        cr.translate(cx, cy)
        cr.scale(0.7 + 0.3 * q, 0.7 + 0.3 * q)
        cr.translate(-cx, -cy)
        clip = blob_cloud(cr, cx, cy, cw, ch, alpha=ca, tail=(hdx - 30, hdy - 40))
        cr.save()
        clip()
        glow(cr, cx, cy, 420, 0.3 * ca)
        munim_scene(cr, t, cx, cy, tM, tG, ca)
        cr.restore()
        cr.restore()
    dev_m = dev(cr, cx - 190, cy + 175)

    def ui(cr):
        if t < tY:
            head(cr, t, "DHANIRAM THOUGHT: MY MUNIM", t0 + 0.05, "FIXED THE NUMBERS", tG)
        else:
            head(cr, t, "SO HERE TOO, A LITTLE...", tY - 0.1, "JUGAAD?", tJ, big_size=130)
        plate(cr, t, tM, "MY MUNIM", dev_m[0], dev_m[1], 28)
    return dict(ui=ui, night=0.12, lift=1.0)


def munim_scene(cr, t, cx, cy, tM, tG, a=1.0):
    """Inside Dhaniram's thought: the munim at his desk, the ledger open with 500 written in it; on "gadbad" the 500 is
    struck out and 50 written, and he winks."""
    gnd = cy + 185
    sly = t > tG + 0.5
    write = (t - tG) if tG < t < tG + 0.6 else 0.0
    ms = 0.44
    mp = munim(cr, t, cx - 170, gnd, ms, sly=sly, write=write, alpha=a)
    lx, ly = cx - 170 + 250 * ms + 40, gnd - 250 * ms - 34
    prop(cr, "yc_ledger", lx, ly, 0.6, rot=-0.05, alpha=a)
    cr.save()
    cr.translate(lx + 72, ly)
    cr.rotate(-0.05)
    draw_text(cr, "500", 0, -14, 62, INK, a * prog(t, tM - 0.3, 0.3), anchor="cm")
    if t > tG:
        p = prog(t, tG, 0.25)
        cr.set_source_rgba(*RED, 0.95 * a)
        cr.set_line_width(7)
        cr.move_to(-58, -14)
        cr.line_to(-58 + 116 * p, -18)
        cr.stroke()
        draw_text(cr, "50", 6, 36, 50, RED, a * prog(t, tG + 0.3, 0.25), anchor="cm")
    cr.restore()
    if sly:
        hx, hy = to_user(cr, mp["head"])
        sparkle(cr, hx + 30, hy - 20, 22, a * (0.5 + 0.5 * math.sin(t * 6)), (1.0, 0.95, 0.7))


def s_y8(cr, t, tl, t0, t1):
    c = cues(tl, "y8")
    tC, tN = c["C"], c["N"]
    hall(cr, t)
    glow(cr, CG_X + 60, FL - 380, 420, 0.4)
    unroll = ease((t - tC + 0.1) / 0.9) if t > tC - 0.1 else 0.0
    shock = t > tN + 0.1
    _, dsp, top = hall_cast(cr, t, scroll_len=180 + 660 * unroll, dh_mood="shock" if shock else "smug",
                            cg_hits=[(tC, 0.3)])
    if t < t0 + 0.5:                                     # the thought cloud pops
        cx, cy, cw, ch = CLOUD7
        q = 1 - prog(t, t0, 0.25)
        if q > 0.01:
            cr.save()
            cr.translate(cx, cy)
            cr.scale(1 + 0.15 * (1 - q), 1 + 0.15 * (1 - q))
            cr.translate(-cx, -cy)
            blob_cloud(cr, cx, cy, cw, ch, alpha=q)
            cr.restore()
        burst(cr, t, cx, cy, t0, n=14, rmax=420, alpha=0.6)
    dev_s = dev(cr, top[0] + 250, top[1] + 330)
    dev_q = dev(cr, dsp["head"][0], dsp["head"][1] - 70)

    def ui(cr):
        head(cr, t, "BUT CHITRAGUPTA IS", t0 + 0.05, "NEVER WRONG", tN, under=tN + 0.5)
        stamp(cr, t, tN + 0.1, "NEVER WRONG", dev_s[0], dev_s[1], 56)
        if shock:
            mark(cr, t, tN + 0.15, "!", dev_q[0], dev_q[1], 90)
    return dict(ui=ui, night=0.12, lift=1.0, flash=flash_at(t, tN + 0.1, 0.18))


# ------------------------------------------------------------------ y9, y10  the terrible form


GX, GS = 450, 0.72                                    # the giant: buffalo x, scale
G_GROUND = FL + 315                                   # where the buffalo stands (its legs hidden below the horizon)


def terrible(cr, t, rise, a=1.0, toss=0.0, raise_=1.0, fan=1.0, eyes=1.0, grow=0.0, store=None, fan_a=0.75,
             back=1.0):
    """The giant rising beyond the horizon (clipped at the floor line), backlit by a red glow."""
    s = GS * (1 + 0.05 * grow)
    e = ease(rise)
    ground = G_GROUND + (1 - e) * 1250 + 20 * grow
    hy = ground + YC.BUF_SEAT[1] * s
    if back > 0.01:
        glow(cr, GX - 40, hy - 330 * s, 760, 0.8 * back * e)
        warm(cr, GX - 40, hy - 420 * s, 620, 0.9 * back * e, col=(1.0, 0.36, 0.16))
    cr.save()
    cr.rectangle(-200, -200, W + 400, FL + 202)
    cr.clip()
    pts = giant(cr, t, GX, ground, s, alpha=a, toss=toss, raise_=raise_, fan=fan, eyes=eyes, store=store,
                fan_a=fan_a)
    cr.restore()
    return pts


def hills(cr, a=1.0):
    """Mountains on the horizon, round the giant's knees: they come up only to his buffalo's flank."""
    for x, s, b in ((1180, 0.42, 2.5), (1500, 0.3, 3.5), (1820, 0.36, 3.0), (60, 0.34, 3.0)):
        prop(cr, "yc_hills", x, FL + 8, s, alpha=0.9 * a, blur=b)


def s_y9(cr, t, tl, t0, t1):
    c = cues(tl, "y9")
    tY, tR, tB, tP, tD, tL, tG = (c[k] for k in ("Y", "R", "B", "P", "D", "L", "G"))
    dark = prog(t, t0, 1.2)
    storm_sky(cr, t, dark)
    clouds(cr, t, dark)
    rise = clamp((t - t0 - 0.1) / max(1.4, min(2.0, tR + 0.6 - t0 - 0.1)))
    toss = 0.12 * math.sin(math.pi * clamp((t - tB) / 0.6)) - 0.04 * math.sin(math.pi * clamp((t - tB - 0.6) / 0.5))
    raise_ = keyed(t, [(t0, 0.0), (tD - 0.1, 1.0)], 0.35, 1.3)
    if t > tG:                                          # lightning
        for k, (bx, by, bs) in enumerate(((1380, 270, 1.0), (1060, 300, 0.8), (1720, 230, 0.9))):
            bolt_at(cr, t, tG + 0.12 * k, bx, by, bs)
    hills(cr, dark)
    st = {}
    gp = terrible(cr, t, rise, toss=toss, raise_=raise_, fan=prog(t, tR + 0.6, 0.8), eyes=prog(t, tR + 0.8, 0.4),
                  grow=prog(t, tP, 0.6), store=st)
    stone_floor(cr, 0.9, col=(0.52, 0.46, 0.52), gold=0.3)
    if t > tB:                                          # the buffalo snorts
        nx = GX + (YC.BUF_NECK[0] + 350) * GS
        ny = G_GROUND + (YC.BUF_NECK[1] + 150) * GS
        for k in range(3):
            if t - tB - 0.25 * k > 0:
                u = (t - tB - 0.25 * k) % 1.2 / 1.2
                glow(cr, nx + 70 * u, ny - 20 * u, 40 + 60 * u, 0.3 * (1 - u))
    if t > tG:
        hd = to_user(cr, gp["head"])
        sound_rings(cr, hd[0] + 60, hd[1], t, tG, n=4, period=0.25, rmax=900, alpha=0.6, color=(0.25, 0.08, 0.10))
    fear = prog(t, tR + 0.5, 0.3)
    dsoul(cr, t, 1520, FL, 115, mood="terror" if fear > 0.5 else "calm", arms="up" if fear > 0.5 else "rest",
          shiver=fear, flip=True)
    shiver_lines(cr, t, 1520, FL, 115, fear)
    dev_b = dev(cr, GX + (YC.BUF_NECK[0] + 300) * GS, G_GROUND + (YC.BUF_NECK[1] - 160) * GS)
    dev_dd = st.get("top")
    dev_h = dev(cr, 1180, FL - 380)

    def ui(cr):
        if t < tB:
            head(cr, t, "THEN DHANIRAM SAW", t0 + 0.05, "YAMA'S TERRIBLE FORM", tR, maxw=860)
        elif t < tL:
            head(cr, t, "ON A BUFFALO, DANDA IN HAND,", tB - 0.1, "BIG AS A MOUNTAIN", tP, maxw=860)
        else:
            head(cr, t, "AND HIS VOICE:", tL - 0.1, "LIKE THUNDER", tG, maxw=860, under=tG + 0.3)
        tag(cr, t, tB + 0.1, "BUFFALO", dev_b[0], dev_b[1], 30, t_out=tL)
        plate(cr, t, tP + 0.2, "MOUNTAINS", dev_h[0], dev_h[1], 26, t_out=tL)
        if dev_dd and t > tD:
            red_ring(cr, dev_dd[0], dev_dd[1] + 30, 70, 90, prog(t, tD + 0.05, 0.4), 8, 1 - prog(t, tG, 0.3))
    return dict(ui=ui, night=0.3 * dark, lift=1.4, flash=flash_at(t, tR, 0.2) + flash_at(t, tG, 0.45, 9.0),
                storm=0.4 * dark)


def s_y10(cr, t, tl, t0, t1):
    c = cues(tl, "y10")
    tT, tK = c["T"], c["K"]
    storm_sky(cr, t, 1.0)
    clouds(cr, t, 1.0)
    hills(cr, 1.0)
    terrible(cr, t, 1.0, toss=0.03 * math.sin(t * 2), raise_=1.0, fan=1.0, eyes=1.0, grow=1.0)
    stone_floor(cr, 0.9, col=(0.52, 0.46, 0.52), gold=0.3)
    sh = 0.6 + 0.4 * prog(t, tT, 0.2)
    dsp = dsoul(cr, t, 1450, FL, 230, mood="terror", arms="up", shiver=1.6 * sh, flip=True)
    shiver_lines(cr, t, 1450, FL, 230, sh)
    hx, hy = dsp["head"]
    sweat(cr, t, hx, hy - 10, 1.4, prog(t, tT, 0.2))

    def ui(cr):
        head(cr, t, "DHANIRAM", t0 + 0.05, "SHOOK WITH FEAR", tT + 0.1, maxw=920)
    return dict(ui=ui, night=0.3, lift=1.4, flash=flash_at(t, t0 + 0.3, 0.1), storm=0.4)


# ------------------------------------------------------------------ y11  all equal


PAIRS = (("FOOL", "WISE", "F", "W"), ("BEGGAR", "RICH", "B", "R"), ("WEAK", "STRONG", "K", "S"))
BAL = (1000, 0.72)                                    # the balance: x, scale


def word_tile(text, slot, t_land):
    """A word tile lying in a pan (pan units: the hook at 0, 0; the rim at y = K.PAN_DROP), stacked by slot."""
    def fn(cr, t, rim_y, a):
        y = rim_y - 66 - 66 * slot
        w_ = max(150, text_size(text, 52)[0] + 40)
        cr.save()
        cr.translate(0, y)
        cr.rotate((-0.03, 0.025, -0.015)[slot % 3])
        pc.poly(cr, [(-w_ / 2, -32), (w_ / 2, -32), (w_ / 2, 32), (-w_ / 2, 32)])
        cr.set_source_rgba(0.98, 0.88, 0.62, a)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, a)
        cr.set_line_width(4)
        cr.stroke()
        draw_text(cr, text, 0, 2, 50, RED if text == "RICH" else INK, a, anchor="cm")
        cr.restore()
    return dict(kind="fig", fn=fn, t=t_land)


def s_y11(cr, t, tl, t0, t1):
    c = cues(tl, "y11")
    tY, tE = c["Y"], c["E"]
    storm_sky(cr, t, 0.7)
    clouds(cr, t, 0.3)
    silhouette(cr, lambda c_: giant(c_, t, 300, FL + 140, 0.5, fan=1.0, eyes=0.0), 0.28, col=SIL)
    hall(cr, t, a=0.5)
    cp = chitra(cr, t, 330, hold=0.0, front=mix((-0.4, -0.5), (-1.3, -0.3), prog(t, tY, 0.3)),
                hits=[(c["F"], 0.2), (c["B"], 0.2), (c["K"], 0.2)])
    mouth = to_user(cr, cp["head"])
    left, right = [], []
    for k, (lw, rw, kl, kr) in enumerate(PAIRS):
        left.append(word_tile(lw, k, c[kl] + 0.15))
        right.append(word_tile(rw, k, c[kr] + 0.15))
    keys = [(t0, 0.0)]
    for _, _, kl, kr in PAIRS:
        keys += [(c[kl] + 0.15, 0.09), (c[kr] + 0.15, 0.0)]
    bx, bs = BAL
    pans = balance(cr, t, bx, FL, bs, lambda tt: settle(tt, keys, 1.1, 3.2), left=left, right=right, labels=0.0)
    # Dhaniram on the right: perks up at RICH, then droops
    rich = c["R"]
    hope = prog(t, rich + 0.2, 0.25) * (1 - prog(t, rich + 1.3, 0.4))
    dsp = dsoul(cr, t, 1640, FL, DH_H, mood="smug" if hope > 0.5 else "calm",
                arms="chest" if hope > 0.3 else "rest", hand="point" if hope > 0.3 else "open", flip=True)
    eqs = []
    for k, (_, _, kl, kr) in enumerate(PAIRS):
        if t > c[kr] + 0.4:
            ly = pans[0][1] + (K.PAN_DROP - 32 - 66 * k) * bs
            eqs.append((cr.user_to_device(bx, ly), c[kr] + 0.4))
    dev_e = dev(cr, bx, FL - 300)
    dev_d = dev(cr, dsp["head"][0], dsp["head"][1] - 70)

    def ui(cr):
        head(cr, t, "CHITRAGUPTA SAID: FOR YAMA,", t0 + 0.05, "EVERYONE IS EQUAL", tE, under=tE + 0.5)
        if t > tY:
            talk_marks(cr, t, tY, mouth[0] + 60, mouth[1] - 10, dirn=1)
        for (ex, ey), te in eqs:
            badge(cr, t, te, "=", ex, ey, 30, color=RED)
        stamp(cr, t, tE + 0.1, "ALL EQUAL", dev_e[0], dev_e[1], 64)
        if hope > 0.3:
            mark(cr, t, rich + 0.2, "?", dev_d[0], dev_d[1], 70, t_out=rich + 1.3)
    return dict(ui=ui, night=0.2, lift=1.2, flash=flash_at(t, tE + 0.1, 0.15), storm=0.3)


# ------------------------------------------------------------------ y12  forgive me!


def vishnu_badge(cr, t, t_in, x, y, r=96, alpha=1.0):
    """A medallion of Vishnu's chakra and conch (screen coordinates)."""
    def inner(c_):
        glow(c_, x, y, 160, 0.5)
        prop(c_, "sg_chakra", x - 32, y - 10, 0.42, rot=t * 0.8)
        prop(c_, "sg_conch", x + 40, y + 30, 0.42, rot=-0.4)
    medallion(cr, t, t_in, x, y, r, inner, "VISHNU", alpha=alpha)


def order_leaf(cr, t, t_in, x, y, s=1.0, alpha=1.0):
    """The messengers' palm-leaf order with Yama's seal (screen coordinates)."""
    q = back(clamp((t - t_in) / 0.3), 1.5)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(-0.08 + 0.02 * math.sin(t * 2))
    cr.scale(s * q, s * q)
    pc.paint_part(cr, "kk_leaf", a)
    draw_text(cr, "YAMA'S ORDER", 0, 4, 54, INK, a, MONO_FONT, "cm", tracking=3)
    cr.restore()


def s_y12(cr, t, tl, t0, t1):
    c = cues(tl, "y12")
    tJ, tM, tD, tV, tH = (c[k] for k in ("J", "M", "D", "V", "H"))
    storm_sky(cr, t, 0.6)
    clouds(cr, t, 0.3)
    silhouette(cr, lambda c_: giant(c_, t, 300, FL + 140, 0.5, fan=1.0, eyes=0.0), 0.22, col=SIL)
    hall(cr, t, a=0.5)
    kneel = keyed(t, [(t0, 0.0), (tJ - 0.1, 1.0)], 0.3, 1.3)
    plead = 0.04 * math.sin(t * 6) * kneel
    dsp = dsoul(cr, t, 860, FL, 240, mood="cry" if kneel > 0.5 else "calm",
                arms=((-0.75 + plead, -1.85), (-0.8 + plead, -1.8)) if kneel > 0.5 else "rest", flip=False,
                shiver=0.3 * kneel, kneel=kneel > 0.5)
    shrug = keyed(t, [(t0, 0.0), (tD + 0.3, 1.0), (tV + 0.9, 0.0)], 0.3, 1.4)
    show = keyed(t, [(t0, 0.0), (tH - 0.2, 1.0)], 0.3, 1.3)
    m1 = messenger(cr, t, 1330, S, flip=True, hold="noose" if shrug < 0.5 and show < 0.3 else "none",
                   front=mix(mix((-0.4, -0.5), SHRUG["front"], shrug), (-2.0, -0.5), show),
                   backa=mix((0.3, -0.3), SHRUG["backa"], shrug), head=0.12 * shrug, ph=0.2)
    m2 = messenger(cr, t, 1580, S, flip=True, hold="staff" if shrug < 0.5 else "none",
                   front=mix((-0.62, -0.55), SHRUG["front"], shrug), backa=mix((0.3, -0.3), SHRUG["backa"], shrug),
                   head=0.12 * shrug, ph=0.9)
    if kneel > 0.5:
        hx, hy = dsp["head"]
        if t > tM:
            sound_rings(cr, hx + 30, hy, t, tM, n=2, period=0.3, rmax=150, alpha=0.5)
    hand1 = to_user(cr, m1["handF"])
    dev_o = cr.user_to_device(hand1[0] - 40, hand1[1] - 100)
    dev_v = dev(cr, 1090, 420)
    dev_c = dev(cr, 700, 520)
    del m2

    def ui(cr):
        if t < tD:
            head(cr, t, "DHANIRAM BEGGED:", t0 + 0.05, "FORGIVE ME!", tM)
        elif t < tH:
            head(cr, t, "THE MESSENGERS SAID:", tD - 0.1, "FORGIVING IS VISHNU'S JOB", tV)
        else:
            head(cr, t, "WE ONLY", tH - 0.2, "FOLLOW ORDERS", tH + 0.05, under=tH + 0.5)
        cloud_text(cr, t, dev_c[0], dev_c[1] - 40, 0.55, [("FORGIVE ME!", 64, RED, 0, tM + 0.05)], flip=True,
                   t_in=tM - 0.2, alpha=1 - prog(t, tV, 0.3))
        if tV - 0.2 < t < tH + 0.2:
            vishnu_badge(cr, t, tV - 0.1, dev_v[0], dev_v[1], 100, alpha=1 - prog(t, tH, 0.3))
        if t > tH - 0.3:
            order_leaf(cr, t, tH - 0.2, dev_o[0], dev_o[1], 0.6)
            stamp(cr, t, tH + 0.35, "ORDERS", dev_o[0] + 60, dev_o[1] + 90, 46, rot=-0.12)
    return dict(ui=ui, night=0.18, lift=1.2, flash=flash_at(t, tM, 0.1), storm=0.25)


# ------------------------------------------------------------------ t1  the eastern gate


def s_t1(cr, t, tl, t0, t1):
    c = cues(tl, "t1")
    tR, tS = c["R"], c["S"]
    t_out = max(t0 + 1.4, min(tR - 0.6, t0 + 1.8))
    tS = max(tS, t_out + 0.8)
    gate_in = (-10.0, -10.0, -10.0, -10.0)
    blaze = prog(t, t_out + 0.1, 0.5)
    u = ease((t - t_out) / max(0.8, tS - t_out)) if t > t_out else 0.0

    def scene(cr):
        city_map(cr, t, gate_in, dark_s=1.0, lit_e=1.0, blaze_e=blaze)
        pts = E_ROAD[::-1]
        seg = min(2, int(u * 3))
        f = u * 3 - seg
        px, py = map_point(pts[seg], pts[seg + 1], f) if u < 1 else (MAP_E[0] + 80, MAP_E[1] + 10)
        bob = 3 * math.sin(t * 12) * (0 < u < 1)
        glow(cr, px, py - 30, 110, 0.6)
        cr.save()
        cr.translate(px, 0)
        cr.scale(-1, 1)
        cr.translate(-px, 0)
        prop(cr, "jd_horse", px + 0.07 * 760, py + bob, 0.06)
        prop(cr, "yc_ratha", px, py + bob, 0.075)
        prop(cr, "jd_wheel", px, py - 250 * 0.075 + bob, 0.075, rot=t * 5 * (0 < u < 1))
        cr.restore()
    fade_in(cr, prog(t, t_out - 0.1, 0.5), scene)
    chapter(cr, t, t0 - 0.2, t_out, [[("THE", INK), ("EASTERN", RED), ("GATE", INK)]], "GARUDA PURANA · PRETA KALPA")

    def ui(cr):
        if t > t_out:
            head(cr, t, "THEN, AT THE", t_out + 0.05, "EAST GATE...", t_out + 0.3)
            map_ui(cr, t, gate_in)
            if t > tS:
                red_ring(cr, MAP_E[0] + 30, MAP_E[1] - 60, 150, 115, prog(t, tS, 0.4), 9)
                plate(cr, t, tS + 0.1, "A CHARIOT", MAP_E[0] + 150, MAP_E[1] + 90, 28)
    return dict(ui=ui, flash=flash_at(t, t_out, 0.2) + flash_at(t, tS, 0.12), eve=0.1 * blaze)


# ------------------------------------------------------------------ t2, t3  the eastern road, Bhola arrives


ROAD_Y = 800                                          # the golden road's top edge (the lotus pond below it)
GATE_E = (250, 0.78)                                  # the east gate on the left: x, scale
CAR_STOP = 1010                                       # where the chariot stops (car pivot x)
CAR_S = 0.46


def east_set(cr, t, swans_in=-10.0, trees_in=-10.0, jewels_in=-10.0, a=1.0):
    """The eastern road: a dawn-gold sky, the golden gate on the left, Parijata trees dropping white flowers, a golden
    road set with jewels, a lotus pond with swans along the front."""
    gold_light(cr, t, 250, FL - 360, 700, 0.8 * a)
    aura(cr, t, GATE_E[0], FL - 420, 160, 700, 0.35 * a, n=22, spin=0.02)
    for x, s, b, ti in ((1560, 0.5, 2, trees_in), (720, 0.42, 5, trees_in + 0.15), (1880, 0.44, 6, trees_in + 0.3)):
        q = back(clamp((t - ti) / 0.4), 1.5)
        if q > 0.01:
            prop(cr, "yc_parijata", x, ROAD_Y + 10, s * q, rot=sway(t, 0.006, 0.3, x), alpha=clamp(q) * a, blur=b)
    prop(cr, "yc_gate_E", GATE_E[0], ROAD_Y + 6, GATE_E[1], alpha=a)
    cr.save()                                             # the road
    cr.rectangle(0, ROAD_Y - 4, W, 70)
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(1.0, 0.82, 0.40, a)
    cr.fill()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(5)
    for yy in (ROAD_Y - 4, ROAD_Y + 66):
        cr.move_to(0, yy)
        cr.line_to(W, yy)
    cr.stroke()
    cr.restore()
    jq = prog(t, jewels_in, 0.5)
    for i in range(16):                                   # jewels set in the road
        x = 70 + 120 * i
        col = ((0.55, 0.85, 1.0), (1.0, 0.40, 0.40), (0.50, 0.95, 0.55), (1.0, 0.85, 0.35))[i % 4]
        cr.save()
        cr.translate(x, ROAD_Y + 31)
        pc.poly(cr, [(0, -18), (16, 0), (0, 18), (-16, 0)])
        cr.set_source_rgba(*col, a)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, a)
        cr.set_line_width(3)
        cr.stroke()
        cr.restore()
        if jq > 0:
            sparkle(cr, x, ROAD_Y + 31, (10 + 10 * max(0.0, math.sin(t * 3 + i * 1.3))) * jq, a * jq, LIGHT)
    cr.save()                                             # the lotus pond
    cr.rectangle(0, ROAD_Y + 68, W, H - ROAD_Y - 68)
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(0.42, 0.62, 0.84, a)
    cr.fill()
    cr.restore()
    for k in range(2):
        prop(cr, "rv_waveA", 960 + 60 * math.sin(t * 0.6 + k), ROAD_Y + 110 + 50 * k, 0.95, alpha=0.5 * a)
    for x in (380, 860, 1420):
        cr.save()
        pc.ell(cr, x, ROAD_Y + 150, 60, 14)
        cr.set_source_rgba(0.30, 0.60, 0.30, a)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, a)
        cr.set_line_width(3)
        cr.stroke()
        cr.restore()
        prop(cr, "md_lotus", x + 10, ROAD_Y + 146, 0.12, alpha=a)
    for k, x0 in enumerate((1250, 1600)):                 # swans glide in from the right
        q = prog(t, swans_in + 0.25 * k, 0.6)
        if q > 0.01:
            sx = x0 + 260 * (1 - ease(q)) - 14 * max(0.0, t - swans_in)
            glow(cr, sx, ROAD_Y + 130, 140, 0.4 * q * a)
            prop(cr, "kb_swan", sx, ROAD_Y + 178 + 4 * math.sin(t * 1.5 + k), 0.3, rot=0.02 * math.sin(t + k),
                 alpha=q * a, flip=True)


def chariot_l(cr, t, x, door=0.0, moving=False, alpha=1.0, s=CAR_S):
    """The celestial chariot facing left (its car at x on the road), two horses ahead; door 0..1 swings its door
    open. Returns the doorway's centre (user coordinates)."""
    bob = 4 * math.sin(t * 11) if moving else 0.0
    cr.save()
    cr.translate(x, 0)
    cr.scale(-1, 1)
    cr.translate(-x, 0)
    hx = x + 700 * s
    prop(cr, "jd_horse_far", hx + 80 * s, ROAD_Y - 14 * s + bob * 0.5, s * 0.98, alpha=alpha, blur=1.5)
    glow(cr, x + 60 * s, ROAD_Y - 600 * s, 500 * s, 0.4 * alpha)
    prop(cr, "yc_ratha", x, ROAD_Y + bob, s, alpha=alpha)
    dx, dy = YC.RATHA_DOOR
    door_x, door_top = x + dx * s, ROAD_Y - YC.RATHA_DECK * s + bob
    dc = (door_x + YC.RATHA_DOOR_W * s / 2, door_top - YC.RATHA_DOOR_H * s / 2)
    if door > 0.01:
        glow(cr, dc[0], dc[1], 220 * s + 40, 0.9 * door * alpha)
        warm(cr, dc[0], dc[1], 200 * s, 0.7 * door * alpha, col=(1.0, 0.92, 0.6))
    k = math.cos(math.pi * 0.5 * ease(door) * 1.12)
    if abs(k) > 0.03:
        cr.save()
        cr.translate(door_x, dc[1])
        cr.scale(k, 1)
        cr.scale(s, s)
        pc.paint_part(cr, "yc_ratha_door", alpha)
        cr.restore()
    prop(cr, "jd_wheel", x, ROAD_Y - 250 * s + bob, s, rot=(t * 4 if moving else 0.0), alpha=alpha)
    prop(cr, "jd_horse", hx, ROAD_Y + bob * 0.5, s, rot=sway(t, 0.006, 0.8), alpha=alpha)
    cr.restore()
    return (2 * x - dc[0], dc[1])


def car_x(t, t_in, t_stop):
    """The chariot rolls in from off the right and slows to a stop at CAR_STOP."""
    if t >= t_stop:
        return CAR_STOP
    u = clamp((t - t_in) / max(0.5, t_stop - t_in))
    return 2150 + (CAR_STOP - 2150) * (1 - (1 - u) ** 2.2)


def s_t2(cr, t, tl, t0, t1):
    c = cues(tl, "t2")
    tJ, tP, tK, tH = c["J"], c["P"], c["K"], c["H"]
    east_set(cr, t, swans_in=tK, trees_in=tP - 0.1, jewels_in=tJ)
    petals_on = tP + 0.3
    if t > petals_on:
        for k, x in enumerate((1560, 720)):
            for i in range(6):
                ti = petals_on + 0.5 * i + 0.25 * k
                u = ((t - ti) / 3.2) % 1.0 if t > ti else None
                if u is None:
                    continue
                px = x - 200 + 400 * ((i * 0.618 + k * 0.3) % 1.0) + 40 * math.sin(t * 1.5 + i)
                py = ROAD_Y - 520 + 560 * u
                prop(cr, "yc_flower", px, py, 0.5, rot=t * 1.4 + i, alpha=min(1.0, 4 * u, 4 * (1 - u)))
    x = car_x(t, t0 - 0.2, t1 + 0.6)
    chariot_l(cr, t, x, moving=True)
    dev_j = dev(cr, 1500, ROAD_Y + 32)
    dev_p = dev(cr, 1560, ROAD_Y - 470)
    dev_s = dev(cr, 1320, ROAD_Y + 110)

    def ui(cr):
        head(cr, t, "THE EASTERN ROAD:", t0 + 0.05, "PAVED WITH JEWELS", tJ, under=tJ + 0.5)
        tag(cr, t, tJ + 0.1, "JEWELS", dev_j[0], dev_j[1] - 80, 30, t_out=tK + 0.4)
        tag(cr, t, tP + 0.15, "PARIJATA TREES", dev_p[0], dev_p[1], 30)
        tag(cr, t, tH, "SWANS", dev_s[0] + 120, dev_s[1] - 30, 30)
    return dict(ui=ui, eve=0.12, flash=flash_at(t, tJ, 0.1))


def s_t3(cr, t, tl, t0, t1):
    c = cues(tl, "t3")
    tU, tB = c["U"], c["B"]
    east_set(cr, t)
    door = prog(t, t0 + 0.05, 0.6)
    dc = chariot_l(cr, t, CAR_STOP, door=door)
    step = ease((t - tU + 0.2) / 0.8) if t > tU - 0.2 else 0.0
    lit = prog(t, tB, 0.35)
    if t > t0 + 0.4:
        bx = dc[0] + (CAR_STOP - 130 - dc[0]) * step
        feet = (dc[1] + 90) + (ROAD_Y - dc[1] - 90) * step
        a_ = prog(t, t0 + 0.4, 0.4)
        gold_light(cr, t, bx, feet - 260, 420, 0.6 * lit)
        aura(cr, t, bx, feet - 280, 120, 420, 0.5 * lit, n=18, spin=0.05)
        cr.push_group()
        bp = bhola(cr, t, bx, 0.5, mood="smile" if lit > 0.5 else "calm", flip=True,
                   front=mix((-0.3, -0.5), (-2.0, -0.85), lit), feet=feet, alpha=a_, rods=step > 0.8, pot=True)
        pat = cr.pop_group()
        cr.set_source(pat)
        cr.paint()
        if lit < 1:                                    # a dark figure until his name
            cr.save()
            cr.set_source_rgba(*SIL, 0.85 * (1 - lit))
            cr.mask(pat)
            cr.restore()
        if lit > 0:
            lights(cr, t, bx, feet - 300, 260, 10, 0.7 * lit)
        dev_b = dev(cr, bx + 200, feet - 330)
    else:
        dev_b = None

    def ui(cr):
        if t < tB:
            head(cr, t, "AND OUT STEPPED...", t0 + 0.05)
        else:
            head(cr, t, "AND OUT STEPPED...", -1.0, "BHOLA!", tB, big_size=140, under=tB + 0.4)
        if dev_b:
            tag(cr, t, tB + 0.15, "BHOLA", dev_b[0], dev_b[1], 36)
    return dict(ui=ui, eve=0.12, flash=flash_at(t, tB, 0.35))


# ------------------------------------------------------------------ t4  the same Bhola


WINS4 = ((360, 560), (960, 560), (1560, 560))
WIN4 = (520, 380)


def s_t4(cr, t, tl, t0, t1):
    c = cues(tl, "t4")
    tW, tC, tM = c["W"], c["C"], c["M"]
    gold_light(cr, t, 960, 560, 900, 0.5)
    stone_floor(cr, 0.4, gold=0.5)
    ww, wh = WIN4

    def water(cr_):
        x, y = WINS4[0]
        g = y + wh / 2 - 30
        tp = thirsty(cr_, t, x - 165, 0.36, feet=g, front=(-1.35, -0.45))
        pour = keyed(t, [(t0, 0.0), (tW + 0.3, 1.0)], 0.4, 1.2)
        bp = bhola(cr_, t, x + 135, 0.36, mood="smile", flip=True, front=(-1.75, -0.45), feet=g, rods=False,
                   hand="hold")
        hx, hy = to_user(cr_, bp["handF"])
        mouth = YY.pot(cr_, hx - 6, hy - 34, 0.3, rot=-1.45 * pour)
        if pour > 0.6:
            YY.water(cr_, t, mouth, tp["bowl"], a=prog(t, tW + 0.45, 0.2), w=9, lift=20)

    def cow(cr_):
        x, y = WINS4[1]
        g = y + wh / 2 - 30
        prop(cr_, "gp_cow", x - 75, g, 0.3)
        feed = keyed(t, [(t0, 0.0), (tC + 0.2, 1.0)], 0.4, 1.2)
        bp = bhola(cr_, t, x + 175, 0.36, mood="smile", flip=True, front=mix((-0.4, -0.5), (-0.95, -0.2), feed),
                   feet=g, rods=False)
        hx, hy = to_user(cr_, bp["handF"])
        cr_.save()                                     # half his roti in his hand
        cr_.translate(hx - 8, hy + 4)
        cr_.scale(0.3, 0.3)
        cr_.rectangle(-90, -90, 90, 180)
        cr_.clip()
        pc.paint_part(cr_, "yc_roti", 1.0)
        cr_.restore()

    def mother(cr_):
        x, y = WINS4[2]
        g = y + wh / 2 - 30
        prop(cr_, "dv_bench", x - 70, g, 0.34)
        bmo(cr_, t, x - 110, g, 0.34, mood="smile", front=(-0.3, -0.6), backa=(0.1, -0.5), rods=False)
        press = 0.1 * math.sin(t * 5) * prog(t, tM, 0.3)
        bhola(cr_, t, x + 70, 0.36, mood="smile", flip=True, front=(-0.55 + press, -0.75), backa=(-0.4, -0.8),
              feet=g, kneel=True, rods=False, head=0.15)
    for (x, y), fn, ti, label in ((WINS4[0], water, min(tW - 0.1, t0 + 0.25), "FREE WATER"), (WINS4[1], cow, tC - 0.1,
                                                                            "ROTI FOR THE COW"),
                                  (WINS4[2], mother, tM - 0.1, "SERVED HIS MOTHER")):
        window(cr, t, ti, x, y, ww, wh, fn, sep=0.45)

    def ui(cr):
        head(cr, t, "IT WAS THE", t0 + 0.05, "SAME BHOLA", t0 + 0.3)
        for (x, y), ti, label in ((WINS4[0], tW, "FREE WATER"), (WINS4[1], tC, "ROTI FOR THE COW"),
                                  (WINS4[2], tM, "SERVED HIS MOTHER")):
            plate(cr, t, ti + 0.2, label, x, y + wh / 2 + 52, 30)
            q = prog(t, ti + 0.5, 0.3)
            if q > 0:
                pw = text_size(label, 30, MONO_FONT, 2)[0] + 40
                tick(cr, x + pw / 2 + 18, y + wh / 2 + 44, 56, q, color=GREEN_TICK)
    return dict(ui=ui, eve=0.1)


# ------------------------------------------------------------------ t5  his eyes popped


def s_t5(cr, t, tl, t0, t1):
    c = cues(tl, "t5")
    tD, tA, tF = c["D"], c["A"], c["F"]
    gold_light(cr, t, 200, 520, 900, 0.9)
    aura(cr, t, -60, 520, 200, 1300, 0.45, n=26, a0=-0.7, a1=0.7, spin=0.02)
    prop(cr, "sb_yhall", 960, FL + 8, 0.6, alpha=0.45, blur=9)
    stone_floor(cr, 0.6)
    pop = prog(t, tA - 0.05, 0.25)
    jolt = 1 + 0.06 * math.sin(math.pi * clamp((t - tA + 0.05) / 0.3))
    dsp = dsoul(cr, t, 1240, FL + 250, 780 * jolt, mood="shocked" if pop > 0.3 else "calm",
                arms=((-1.0, -0.55), (0.7, -0.6)) if pop > 0.5 else "rest", flip=True, halo=0.6,
                shiver=0.3 * pop)
    hx, hy = dsp["head"]
    if pop > 0:                                          # the eye pops out big, pop lines round it
        sc_ = 780 / YY.DH_H
        ex, ey = hx - 18 * sc_ / 0.74, hy - 8
        q = back(clamp((t - tA + 0.05) / 0.3), 2.2)
        r_ = 30 * q * (1 + 0.04 * math.sin(t * 9))
        if r_ > 1:
            cr.save()
            cr.arc(ex, ey, r_, 0, 2 * math.pi)
            cr.set_source_rgba(1, 1, 1, pop)
            cr.fill_preserve()
            cr.set_source_rgba(*pc.INK, pop)
            cr.set_line_width(5)
            cr.stroke()
            cr.arc(ex - 0.3 * r_, ey + 0.05 * r_, 0.38 * r_, 0, 2 * math.pi)
            cr.fill()
            cr.restore()
        cr.save()
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_source_rgba(*pc.INK, pop)
        cr.set_line_width(7)
        for i in range(7):
            a_ = -math.pi * (0.25 + 0.6 * i / 6)
            r0, r1 = 60 * q + 10, 105 * q + 10
            cr.move_to(ex + r0 * math.cos(a_), ey + r0 * math.sin(a_))
            cr.line_to(ex + r1 * math.cos(a_), ey + r1 * math.sin(a_))
        cr.stroke()
        cr.restore()
    dev_m = dev(cr, hx - 230, hy - 60)

    def ui(cr):
        if t < tA:
            head(cr, t, "AND WHAT HAPPENED NEXT...", t0 + 0.05, "DHANIRAM WATCHED", tD)
        else:
            head(cr, t, "AND WHAT HAPPENED NEXT...", -1.0, "HIS EYES POPPED!", tA, under=tF + 0.3)
        mark(cr, t, tF, "!", dev_m[0] - 40, dev_m[1], 110)
        mark(cr, t, tF + 0.12, "!", dev_m[0] + 40, dev_m[1] - 10, 110)
    return dict(ui=ui, eve=0.12, flash=flash_at(t, tA, 0.15))


# ------------------------------------------------------------------ t6, t7  Yama rises and washes Bhola's feet


BH_X = 1160
BH_SIT = 0.52                                         # Bhola seated on Yama's throne: his scale


def golden_hall(cr, t, a=1.0):
    gold_light(cr, t, 960, FL - 420, 1000, 0.7 * a)
    prop(cr, "sb_yhall", 960, FL + 8, 0.6, alpha=0.55 * a, blur=5)
    stone_floor(cr, a, col=(0.80, 0.70, 0.62), gold=1.0)


def s_t6(cr, t, tl, t0, t1):
    c = cues(tl, "t6")
    tK, tS, tU = c["K"], c["S"], c["U"]
    golden_hall(cr, t)
    # the terrible form's dark ghost shrinks into the gentle king
    gh = 1 - prog(t, tK + 0.2, 1.0)
    if gh > 0.01:
        k = 1 - 0.45 * (1 - gh)
        silhouette(cr, lambda c_: giant(c_, t, TH_X - 60, FL + 300 * (1 - gh), 0.62 * k, fan=gh, eyes=0.0),
                   0.5 * gh, col=SIL)
    rise = prog(t, tU - 0.05, 0.6)
    yp = yama_throne(cr, t, TH_X, S, rise=rise, mood="smile" if t > tU + 0.4 else "calm",
                     alpha=prog(t, t0, 0.5) if gh > 0.99 else 1.0)
    if t > tU:
        burst(cr, t, TH_X + 60, FL - 380, tU + 0.2, n=16, rmax=420, alpha=0.5)
    gold_light(cr, t, BH_X, FL - 260, 360, 0.5)
    bp = bhola(cr, t, BH_X, 0.52, mood="calm" if t < tU + 0.3 else "shy", flip=True, front=(-0.3, -2.45),
               pot=True)
    dsoul(cr, t, 1720, FL, 120, mood="shock", flip=True)
    dev_y = yp["top"]
    dev_b = bp["top"]

    def ui(cr):
        if t < tS:
            head(cr, t, "THE SAME YAMA WHO", t0 + 0.05, "SCARED DHANIRAM...", tK)
        else:
            head(cr, t, "FOR BHOLA, HE ROSE FROM HIS", tS - 0.1, "THRONE!", tU, big_size=130, under=tU + 0.5)
        plate(cr, t, tK + 0.3, "THE SAME YAMA", dev_y[0], dev_y[1] - 90, 30, color=RED, t_out=tS + 0.2)
        tag(cr, t, t0 + 0.3, "BHOLA", dev_b[0], dev_b[1] - 70, 30, t_out=tS)
    return dict(ui=ui, eve=0.1, flash=flash_at(t, tU, 0.25))


def s_t7(cr, t, tl, t0, t1):
    c = cues(tl, "t7")
    tA, tB, tW, tT, tJ, tP, tD = (c[k] for k in ("A", "B", "W", "T", "J", "P", "D"))
    golden_hall(cr, t)
    petals(cr, t, tW, 960, 160, n=14, spread=1500, fall=900, dur=3.4, loop=True, alpha=0.9)
    stand_x = TH_X + 110 * S
    walk_end = max(tA + 0.9, tB - 0.05)
    seat_t = tT + 0.7                                     # Bhola is seated on the throne
    kneel_t = tJ - 0.05
    prop(cr, "md_throne", TH_X, FL, S)
    seated = t > seat_t
    if not seated:                                       # Bhola standing, bashful; led across to the throne
        sx_, sbob, srock, sph = hop_walk(t, tT + 0.05, seat_t, BH_X, TH_X + 60, 0.2)
        bp = bhola(cr, t, sx_, 0.52, mood="shy", flip=True, front=(-0.3, -2.45), head=0.1, pot=True,
                   legs=walk_legs(sph), rot=srock, y=FL - 434 * 0.52 + sbob)
    if seated:                                           # Bhola on the throne, facing right
        lit = prog(t, seat_t, 0.3)
        sparkle(cr, TH_X + 40, FL - 300, 120 * math.sin(math.pi * clamp((t - seat_t) / 0.5)), 1.0)
        bp = bhola(cr, t, TH_X, BH_SIT, mood="shy" if t > tJ else "calm", flip=False, front=ANJALI["front"],
                   backa=ANJALI["backa"], sit=True, alpha=lit, hits=[(tP, 0.3)])
        prop(cr, "dv_basin", TH_X + 92, FL + 8, 0.42)
        water_pot(cr, TH_X - 215, FL + 4, 0.36, alpha=lit)
    # Yama: walks forward, bows again and again; turns to offer the throne; kneels and pours
    if t < kneel_t:
        x, bob, rock, ph = hop_walk(t, tA, walk_end, stand_x, 770, 0.42)
        turned = t > tT
        bows = [tB + 0.15, tB + 0.75, tW + 0.35]
        bow = sum(math.sin(math.pi * clamp((t - b) / 0.55)) for b in bows)
        offer = prog(t, tT, 0.3)
        fr = mix(mix((-0.32, -0.55), ANJALI["front"], clamp(bow * 1.5) * (1 - offer)), OFFER, offer)
        ba = mix((0.3, -0.3), ANJALI["backa"], clamp(bow * 1.5) * (1 - offer))
        yp = yama(cr, t, x, S, mood="smile", flip=turned, front=fr, backa=ba, head=0.35 * bow,
                  rot=(0.14 * bow) * (-1 if turned else 1) + rock, legs=walk_legs(ph), y=FL - 434 * S + bob,
                  danda=bow < 0.2 and offer < 0.5)
    else:
        kx = TH_X + 330
        lean = prog(t, kneel_t, 0.4)
        yp = yama(cr, t, kx, S, mood="smile", flip=True, front=(-1.05, -0.25), backa=(-0.5, -0.9),
                  head=0.3 * lean, kneel=True, danda=False, rot=-0.12 * lean)
        hx, hy = to_user(cr, yp["handF"])
        pour = prog(t, tP - 0.1, 0.3)
        ang = -0.3 - 1.15 * pour
        cr.save()
        cr.translate(hx + 4, hy + 10)
        cr.rotate(ang)
        cr.scale(0.3, 0.3)
        cr.translate(0, 160)
        pc.paint_part(cr, "md_kalasha", 1.0)
        cr.restore()
        if pour > 0.6:
            mx = hx + 4 + 0.3 * (318 - 160) * math.sin(ang)
            my = hy + 10 - 0.3 * (318 - 160) * math.cos(ang)
            fx, fy = TH_X + 92, FL - 20
            cr.save()
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            for lw, col in ((16, (0.35, 0.55, 0.85)), (8, (0.80, 0.92, 1.0))):
                cr.move_to(mx, my)
                cr.curve_to(mx - 30, my + 10, fx + 10, fy - 90, fx, fy)
                cr.set_source_rgba(*col, 0.9)
                cr.set_line_width(lw)
                cr.stroke()
            cr.restore()
            for k in range(4):
                u = (t * 2.2 + k / 4) % 1.0
                sparkle(cr, fx - 30 + 60 * u * (1 if k % 2 else -1), fy + 4 - 30 * math.sin(math.pi * u), 10,
                        1 - u, (0.85, 0.95, 1.0))
    dsoul(cr, t, 1720, FL, 120, mood="shock", flip=True)
    if seated and t > tP:
        bh = to_user(cr, bp["head"])
        sweat(cr, t, bh[0], bh[1] - 20, 1.2, 0.8)
    dev_y = yp["top"]
    dev_bh = to_user(cr, bp["head"]) if seated else None
    dev_bh = cr.user_to_device(*dev_bh) if dev_bh else None
    nwel = sum(1 for b in (tB + 0.15, tB + 0.75, tW + 0.35) if t > b)
    dev_w = dev(cr, 975, 300)

    def ui(cr):
        if t < tT:
            head(cr, t, "YAMA WELCOMED HIM", t0 + 0.05, "AGAIN AND AGAIN", tB + 0.1)
            if nwel:
                cloud_text(cr, t, dev_w[0], dev_w[1], 0.5,
                           [("WELCOME!", 62, RED, -10, tB + 0.2), (f"x{nwel}", 44, INK, 44, tB + 0.2)],
                           t_in=tB + 0.1, alpha=1 - prog(t, tT, 0.25))
        elif t < tJ:
            head(cr, t, "HE GAVE BHOLA", tT - 0.1, "HIS OWN THRONE", tT + 0.2)
        else:
            head(cr, t, "AND BOWED, AND", tJ - 0.1, "WASHED HIS FEET", tP, under=tD + 0.3)
        if dev_bh and t > tP:
            mark(cr, t, tP + 0.2, "!", dev_bh[0] + 50, dev_bh[1] - 90, 70)
    return dict(ui=ui, eve=0.1, flash=flash_at(t, tT + 0.35, 0.15) + flash_at(t, tD, 0.15))


# ------------------------------------------------------------------ t8  same Yama, two forms


def s_t8(cr, t, tl, t0, t1):
    c = cues(tl, "t8")
    tB, tD, tA, tV, tW = (c[k] for k in ("B", "D", "A", "V", "W"))
    la = prog(t, min(tB - 0.15, t0 + 0.3), 0.4)
    ra = prog(t, tA - 0.15, 0.4)
    stone_floor(cr, 0.5, gold=0.0)

    def dark(cr_):                                        # left: the terrible form over tiny Dhaniram
        storm_sky(cr_, t, 1.0)
        glow(cr_, 300, 520, 520, 0.6)
        warm(cr_, 300, 480, 420, 0.8, col=(1.0, 0.36, 0.16))
        cr_.save()
        cr_.rectangle(0, 0, W, FL)
        cr_.clip()
        giant(cr_, t, 300, FL + 60, 0.4, fan=1.0, eyes=1.0, raise_=1.0)
        cr_.restore()
        stone_floor(cr_, 0.8, col=(0.52, 0.46, 0.52), gold=0.0)
        dsoul(cr_, t, 790, FL, 110, mood="terror", arms="up", shiver=1.0, flip=True)

    def gold(cr_):                                        # right: golden, Yama bowing to Bhola
        gold_light(cr_, t, 1440, FL - 380, 700, 0.9)
        stone_floor(cr_, 0.8, col=(0.80, 0.70, 0.62), gold=1.0)
        petals(cr_, t, tA, 1440, 300, n=10, spread=700, fall=600, dur=3.0, loop=True)
        bow = 0.5 + 0.5 * math.sin(math.pi * clamp((t - tA - 0.3) / 0.8)) if t > tA else 0.0
        yama(cr_, t, 1240, 0.5, mood="smile", flip=False, front=mix((-0.32, -0.55), ANJALI["front"], bow),
             backa=mix((0.3, -0.3), ANJALI["backa"], bow), head=0.3 * bow, rot=0.12 * bow)
        bhola(cr_, t, 1640, 0.46, mood="calm", flip=True, front=ANJALI["front"], backa=ANJALI["backa"])
    for (x0, fn, a_) in ((90, dark, la), (990, gold, ra)):
        panel(cr, t, x0, 290, 840, 660, fn, a_)

    def ui(cr):
        head(cr, t, "THE GARUDA PURANA SAYS:", t0 + 0.05, "SAME YAMA, TWO FORMS", tV, under=tV + 0.5)
        card_label(cr, t, tB, "BAD DEEDS", 510, 290, la)
        card_label(cr, t, tD, "YAMA LOOKS TERRIFYING", 510, 950, la, small=True)
        card_label(cr, t, tA, "GOOD DEEDS", 1410, 290, ra)
        card_label(cr, t, tW - 0.1, "YAMA RISES TO WELCOME", 1410, 950, ra, small=True)
        if t > tV:
            badge(cr, t, tV + 0.1, "=", 960, 560, 56, color=RED)
            plate(cr, t, tV + 0.2, "SAME YAMA", 960, 650, 28)
    return dict(ui=ui, eve=0.05 * ra)


def panel(cr, t, x0, y0, w, h, fn, a=1.0):
    """One half of a split card: a framed panel of the stage (fn(cr) draws its scene, clipped) that settles in."""
    if a <= 0.01:
        return
    k = 0.92 + 0.08 * ease(a)
    cx, cy = x0 + w / 2, y0 + h / 2
    cr.save()
    cr.translate(cx, cy)
    cr.scale(k, k)
    cr.translate(-cx, -cy)
    cr.save()
    cr.rectangle(x0, y0, w, h)
    cr.clip()
    cr.push_group()
    C.screen(cr)
    fn(cr)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()
    for lw, col in ((20, (0.40, 0.22, 0.10)), (6, (0.95, 0.72, 0.28))):
        cr.rectangle(x0 - 5, y0 - 5, w + 10, h + 10)
        cr.set_source_rgba(*col, a)
        cr.set_line_width(lw)
        cr.stroke()
    cr.restore()


def card_label(cr, t, t_in, text, x, y, a=1.0, small=False):
    """A parchment label for one half of the split card (BAD DEEDS / GOOD DEEDS, and what Yama looks like)."""
    p = prog(t, t_in, 0.3) * a
    if p <= 0.01:
        return
    size = 40 if small else 58
    w, h = text_size(text, size, HEAD_FONT)
    bw, bh = w + 50, h + 28
    q = back(clamp((t - t_in) / 0.3), 1.5)
    cr.save()
    cr.translate(x, y)
    cr.scale(max(0.05, q), max(0.05, q))
    pc.poly(cr, [(-bw / 2, -bh / 2), (bw / 2, -bh / 2), (bw / 2, bh / 2), (-bw / 2, bh / 2)])
    cr.set_source_rgba(0.98, 0.90, 0.66, 0.96 * p)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, p)
    cr.set_line_width(4)
    cr.stroke()
    draw_text(cr, text, 0, 2, size, RED if not small else INK, p, anchor="cm")
    cr.restore()


# ------------------------------------------------------------------ o1, o2  the safe stays, the pot goes


def s_o1(cr, t, tl, t0, t1):
    c = cues(tl, "o1")
    tT, tR, tB, tG = c["T"], c["R"], c["B"], c["G"]
    t_out = max(t0 + 1.5, min(tR - 0.2, t0 + 2.0))
    tR = max(tR, t_out + 0.4)
    tB = max(tB, tR + 0.6)

    def scene(cr):
        # left: Dhaniram's dark empty room, the safe locked
        prop(cr, "dv_room", 560, FL + 6, 0.62, alpha=0.6, blur=4)
        stone_floor(cr, 0.6, col=(0.62, 0.56, 0.50), gold=0.0)
        safe(cr, 560, FL + 4, 0.75)
        cr.save()                                          # a cobweb in the corner of the safe
        cr.set_source_rgba(0.95, 0.95, 0.95, 0.75)
        cr.set_line_width(2)
        cx_, cy_ = 560 + 150 * 0.75 * 1.0, FL - 410 * 0.75
        for k in range(5):
            a_ = math.pi * (0.5 + 0.5 * k / 4)
            cr.move_to(cx_, cy_)
            cr.line_to(cx_ + 110 * math.cos(a_), cy_ + 110 * math.sin(a_))
        for r_ in (35, 65, 95):
            cr.arc(cx_, cy_, r_, math.pi * 0.5, math.pi)
        cr.stroke()
        cr.restore()
        # right: Bhola's doorway, the pot glowing
        ga = prog(t, tB - 0.1, 0.4)
        gold_light(cr, t, 1420, FL - 200, 420, ga * (0.7 + 0.15 * math.sin(t * 3)))
        prop(cr, "dv_house", 1460, FL + 6, 0.5, alpha=0.6 + 0.4 * ga, blur=3)
        water_pot(cr, 1420, FL + 2, 0.62)
        if ga > 0:
            lights(cr, t, 1420, FL - 120, 160, 8, ga)
    fade_in(cr, prog(t, t_out - 0.1, 0.5), scene)
    chapter(cr, t, t0 - 0.2, t_out, [[("WHAT GOES", INK), ("WITH YOU", RED)]], "GARUDA PURANA · PRETA KALPA")

    def ui(cr):
        if t > t_out:
            if t < tB:
                head(cr, t, "DHANIRAM'S SAFE", t_out + 0.05, "STAYED AT HOME", tR)
            else:
                head(cr, t, "AND BHOLA'S", tB - 0.1, "WATER POT?", tG - 0.1)
            stamp(cr, t, tR + 0.3, "LEFT BEHIND", 560, 560, 52, rot=-0.1)
            mark(cr, t, tG, "?", 1420, 560, 120)
    return dict(ui=ui, night=0.1, flash=flash_at(t, t_out, 0.2))


def s_o2(cr, t, tl, t0, t1):
    c = cues(tl, "o2")
    tP, tR, tS = c["P"], c["R"], c["S"]
    cut = t0 + 0.55
    if t < cut:                                            # the pot rises in light from Bhola's doorstep
        u = (t - t0) / 0.55
        gold_light(cr, t, 1420, FL - 200 - 200 * u, 520, 0.9)
        prop(cr, "dv_house", 1460, FL + 6, 0.5, blur=3)
        stone_floor(cr, 0.6, col=(0.62, 0.56, 0.50), gold=0.0)
        water_pot(cr, 1420, FL + 2 - 260 * ease(u), 0.62)
        burst(cr, t, 1420, FL - 200, t0 + 0.1, n=14, rmax=400, alpha=0.6)
        dev_p = None
    else:
        east_set(cr, t)
        x, bob, rock, ph = hop_walk(t, cut, t1 + 1.0, 1700, 900, 0.5)
        gold_light(cr, t, x, ROAD_Y - 260, 360, 0.5)
        bp = bhola(cr, t, x, 0.5, mood="smile", flip=True, legs=walk_legs(ph), rot=rock,
                   y=ROAD_Y - 434 * 0.5 + bob)
        hd = to_user(cr, bp["head"])
        px, py = hd[0] + 120, hd[1] + 40 + 12 * math.sin(t * 2.2)
        gold_light(cr, t, px, py - 70, 220, 0.9)
        aura(cr, t, px, py - 80, 70, 170, 0.6, n=14, spin=0.1)
        water_pot(cr, px, py, 0.36)
        lights(cr, t, px, py - 60, 100, 6, 0.8)
        trail = [(px + 40 + 30 * k, py - 60 + 6 * math.sin(t * 3 + k)) for k in range(12)]
        dotted(cr, trail, 1.0, 26, 4, (1.0, 0.86, 0.5), 0.6)
        dev_p = dev(cr, px + 250, py - 40)

    def ui(cr):
        head(cr, t, "IT BECAME HIS PUNYA,", t0 + 0.05, "AND WENT WITH HIM", tR)
        if dev_p:
            tag(cr, t, tP + 0.2, "PUNYA = GOOD DEEDS", dev_p[0], dev_p[1], 30)
    return dict(ui=ui, eve=0.1, flash=flash_at(t, cut, 0.2))


# ------------------------------------------------------------------ o3  no karma disappears unpaid


def s_o3(cr, t, tl, t0, t1):
    c = cues(tl, "o3")
    tH, tG, tF, tM = c["H"], c["G"], c["F"], c["M"]
    storm_sky(cr, t, 0.5)
    stone_floor(cr, 0.85, col=(0.56, 0.50, 0.56), gold=0.0)
    cr.save()                                              # darkness on the left: the way he is led
    g = cairo.LinearGradient(0, 0, 700, 0)
    g.add_color_stop_rgba(0, 0.06, 0.03, 0.06, 0.9)
    g.add_color_stop_rgba(1, 0.06, 0.03, 0.06, 0.0)
    cr.rectangle(0, 0, 700, H)
    cr.set_source(g)
    cr.fill()
    cr.restore()
    walk_end = t0 + 6.0
    x, bob, rock, ph = hop_walk(t, t0 + 0.2, walk_end, 1500, 300, 0.45)
    fade = 1 - prog(t, walk_end - 1.2, 1.0)
    ca = prog(t, tG - 0.1, 0.4)
    dim = 1 - 0.55 * ca
    m1 = messenger(cr, t, x - 230, S, flip=True, hold="none", front=(-1.3, -0.2), legs=walk_legs(ph), rot=rock,
                   y=FL - 434 * S + bob, alpha=fade * dim, ph=0.2)
    dsoul(cr, t, x, FL, DH_H, mood="cry", flip=True, alpha=fade * dim, walk=ph * 3 if t < walk_end else None)
    messenger(cr, t, x + 260, S, flip=True, hold="staff", front=(-0.62, -0.55), legs=walk_legs(-ph), rot=-rock,
              y=FL - 434 * S + bob, alpha=fade * dim, ph=0.8)
    hand = to_user(cr, m1["handF"])
    if fade > 0.01:
        wx, wy = x, FL - 0.45 * DH_H
        light_rope(cr, [hand, ((hand[0] + wx) / 2, wy + 20), (wx - 0.18 * DH_H, wy)], 0.8 * fade * dim, 0.55)
        noose_loop(cr, t, wx, wy, 0.2 * DH_H + 6, 0.07 * DH_H + 4, 0.8 * fade * dim)
    # his scroll of account hovers over him
    if t < tG:
        sa = prog(t, tH - 0.1, 0.3) * fade
        deeds_scroll(cr, x + 10, FL - 520 + 8 * math.sin(t * 2), 180, 220, ROWS, alpha=sa, title="ACCOUNT")

    def ui(cr):
        if t < tG:
            head(cr, t, "NOW DHANIRAM HAD TO", t0 + 0.05, "PAY HIS ACCOUNT", tH)
        else:
            head(cr, t, "THE GARUDA PURANA SAYS:", tG - 0.1)
        if t > tG - 0.2:
            chapter(cr, t, tG - 0.1, t1 + 5.0, [[("NO KARMA", INK)], [("DISAPPEARS", INK), ("UNPAID", RED)]],
                    "GARUDA PURANA · PRETA KALPA 1.46")
    return dict(ui=ui, night=0.2, lift=1.2, storm=0.2)


# ------------------------------------------------------------------ o4c  the road: no buying, no selling


def burning_road(cr, t, a=1.0):
    """The hook's road: a long empty road winding to the horizon under a burning sky, cracked earth, heat haze."""
    if a <= 0.01:
        return
    from scenes_six_c import heat, sun
    cr.save()
    g = cairo.LinearGradient(0, 0, 0, 640)
    g.add_color_stop_rgba(0, 1.0, 0.55, 0.25, 0.55 * a)
    g.add_color_stop_rgba(1, 1.0, 0.80, 0.45, 0.1 * a)
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.rectangle(0, 0, W, 640)
    cr.set_source(g)
    cr.fill()
    cr.rectangle(0, 600, W, H - 600)
    cr.set_source_rgba(0.92, 0.70, 0.46, a)
    cr.fill()
    cr.restore()
    sun(cr, t, 1560, 330, 0.5, a=a, hard=1.0)
    cr.save()                                              # the road, narrowing to the horizon
    cr.move_to(880, 600)
    cr.curve_to(1000, 680, 600, 780, 760, 900)
    cr.curve_to(860, 980, 1000, 1040, 1100, H + 10)
    cr.line_to(1500, H + 10)
    cr.curve_to(1300, 1030, 1050, 980, 960, 900)
    cr.curve_to(820, 790, 1060, 690, 900, 600)
    cr.close_path()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(0.80, 0.56, 0.36, a)
    cr.fill_preserve()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.set_source_rgba(*pc.INK, 0.8 * a)
    cr.set_line_width(4)
    cr.stroke()
    cr.restore()
    cr.save()                                              # cracks in the earth
    cr.set_source_rgba(0.35, 0.20, 0.10, 0.55 * a)
    cr.set_line_width(3)
    for i, (x, y) in enumerate(((240, 720), (520, 860), (1400, 760), (1700, 900), (300, 980), (1650, 680))):
        cr.move_to(x, y)
        for k in range(4):
            x += 40 * math.cos(i + k * 1.7)
            y += 22 * math.sin(i * 2 + k)
            cr.line_to(x, y)
    cr.stroke()
    cr.restore()
    heat(cr, t, 640, a=0.8 * a)
    prop(cr, "gp_deadtree", 300, 640, 0.28, alpha=0.8 * a, blur=3)


def coin_bag_x(cr, t, t_in, x, y, s, t_x):
    """A coin bag (its middle at (x, y)) with coins spilled at its foot, crossed out at t_x (screen coordinates)."""
    q = back(clamp((t - t_in) / 0.35), 1.5)
    a = clamp(q)
    if a <= 0.01:
        return
    prop(cr, "sk_bag", x, y - 100 * s * q, 0.9 * s * q, alpha=a)
    for dx, dy in ((-120, 120), (-60, 136), (90, 128), (140, 112)):
        prop(cr, "yy_coin", x + dx * s, y + dy * s, 0.7 * s, alpha=a)
    pa = prog(t, t_x, 0.35)
    if pa > 0:
        big_x(cr, x, y, 360 * s, 320 * s, pa, lw=22)


POT4 = (1080, 850)                                    # the glowing pot of good deeds on the road (o4c)


def hook_road(cr, t):
    """The hook's frame (builder A's i1 road set: the burning sky, the long empty road to the horizon), so the
    callback looks the same; this module's own burning road if that is not available."""
    try:
        from scenes_yy_a import road_set
    except Exception:
        burning_road(cr, t)
        return
    road_set(cr, t)


def s_o4c(cr, t, tl, t0, t1):
    c = cues(tl, "o4c")
    tY, tR, tK, tB, tS, tE = (c[k] for k in ("Y", "R", "K", "B", "S", "E"))
    hook_road(cr, t)
    ea = prog(t, tS + 0.1, 0.4)
    if ea > 0:                                         # good deeds: the one thing that goes with you
        px, py = POT4[0], POT4[1] + 6 * math.sin(t * 2)
        gold_light(cr, t, px, py - 90, 320, 0.9 * ea)
        aura(cr, t, px, py - 100, 90, 230, 0.6 * ea, n=16, spin=0.1)
        water_pot(cr, px, py, 0.42 * (0.6 + 0.4 * ease(ea)), alpha=ea)
        lights(cr, t, px, py - 80, 140, 8, 0.8 * ea)

    def ui(cr):
        if t < tR:
            head(cr, t, "REMEMBER THE", t0 + 0.05, "1-YEAR JOURNEY?", tY)
            counter_badge(cr, t, tY + 0.1, "1 YEAR", 330, 340, 84, alpha=1 - prog(t, tR, 0.3))
        elif t < tS:
            head(cr, t, "ON THAT ROAD:", tR - 0.1, "NO BUYING. NO SELLING.", tK)
        else:
            head(cr, t, "WHAT YOU TAKE WITH YOU,", tS - 0.1, "EARN IT HERE", tE, under=tE + 0.4)
        if tK - 0.2 < t < tS + 0.4:
            a_ = 1 - prog(t, tS, 0.35)
            if a_ > 0.01:
                cr.push_group()
                coin_bag_x(cr, t, tK - 0.1, 420, 560, 0.9, tK + 0.25)
                cr.save()
                cr.translate(1560, 600)
                q = back(clamp((t - tB + 0.1) / 0.35), 1.5)
                if q > 0.01:
                    cr.scale(0.36 * q, 0.36 * q)
                    pc.paint_part(cr, "kk_beam", clamp(q))
                    for sx in (-1, 1):
                        cr.save()
                        cr.translate(sx * K.BEAM_L, 0)
                        pc.paint_part(cr, "kk_pan", clamp(q))
                        cr.restore()
                cr.restore()
                if t > tB + 0.25:
                    big_x(cr, 1560, 660, 330, 300, prog(t, tB + 0.25, 0.35), lw=22)
                cr.pop_group_to_source()
                cr.paint_with_alpha(a_)
        plate(cr, t, tK + 0.3, "NO BUYING", 420, 790, 30, color=RED, t_out=tS)
        plate(cr, t, tB + 0.3, "NO SELLING", 1560, 790, 30, color=RED, t_out=tS)
        if ea > 0:
            plate(cr, t, tE, "GOOD DEEDS", POT4[0], POT4[1] - 270, 32, color=RED)
    return dict(ui=ui, lift_abs=0.85, flash=flash_at(t, tE, 0.15))


# ------------------------------------------------------------------ o5  which gate will you take?


GATE_CARDS = ((540, "S", "DHANIRAM'S GATE"), (1380, "E", "BHOLA'S GATE"))


def s_o5(cr, t, tl, t0, t1):
    c = cues(tl, "o5")
    tK, tD, tB, tI = c["K"], c["D"], c["B"], c["I"]
    stone_floor(cr, 0.5, gold=0.0)
    for k, (x, kind, _) in enumerate(GATE_CARDS):
        ti = t0 + 0.15 + 0.3 * k
        q = back(clamp((t - ti) / 0.4), 1.5)
        if q <= 0.01:
            continue
        if kind == "S":
            warm(cr, x, FL - 300, 420, 0.5 * clamp(q), col=(0.55, 0.15, 0.20))
            prop(cr, "cloud", x + 20, FL - 520, 0.9 * q, alpha=0.8 * clamp(q), blur=2)
        else:
            gold_light(cr, t, x, FL - 300, 520, 0.9 * clamp(q))
            aura(cr, t, x, FL - 330, 160, 480, 0.5 * clamp(q), n=20, spin=0.05)
        prop(cr, "yc_gate_" + kind, x, FL + 6, 0.7 * q, alpha=clamp(q))
        if kind == "S":
            dsoul(cr, t, x + 300, FL, 110, mood="cry", flip=True, alpha=clamp(q))
        else:
            bhola(cr, t, x + 320, 0.4, mood="smile", flip=True, front=(-0.3, -2.45), alpha=clamp(q), pot=True)

    def ui(cr):
        if t < tD:
            head(cr, t, "IF YOUR JOURNEY BEGAN TOMORROW,", t0 + 0.05, "WHICH GATE WILL YOU TAKE?", tK)
        else:
            head(cr, t, "BE HONEST:", tD - 0.1, "WHICH GATE WILL YOU TAKE?", -1.0)
        for k, (x, kind, label) in enumerate(GATE_CARDS):
            card_label(cr, t, (tD, tB)[k] - 0.1, label, x, 975, 1.0)
        if t > tD:
            n = int((t - tD) / 0.9)
            k = n % 2
            red_ring(cr, GATE_CARDS[k][0], FL - 260, 330, 330, prog(t, tD + 0.9 * n, 0.35), 10)
    return dict(ui=ui, flash=flash_at(t, tK, 0.12))


# ------------------------------------------------------------------ frame


SHOTS = [   # (line, draw function, options); "cont" = the same set continues (no lamp dip)
    ("y1", s_y1, {"z": (1.0, 1.02)}),
    ("y2", s_y2, {"z": (1.0, 1.03)}),
    ("y3", s_y3, {"z": (1.03, 1.05), "cont": True}),
    ("y4", s_y4, {"z": (1.0, 1.03)}),
    ("y5", s_y5, {"z": (1.0, 1.03)}),
    ("y6", s_y6, {"z": (1.0, 1.02)}),
    ("y7", s_y7, {"z": (1.0, 1.03)}),
    ("y8", s_y8, {"z": (1.03, 1.05), "cont": True}),
    ("y9", s_y9, {"z": (1.0, 1.04), "focus": (900, 700)}),
    ("y10", s_y10, {"z": (1.22, 1.3), "focus": (1450, 760), "cont": True}),
    ("y11", s_y11, {"z": (1.0, 1.03)}),
    ("y12", s_y12, {"z": (1.0, 1.03)}),
    ("t1", s_t1, {"z": (1.0, 1.02)}),
    ("t2", s_t2, {"z": (1.0, 1.03)}),
    ("t3", s_t3, {"z": (1.03, 1.07), "focus": (1000, 640), "cont": True}),
    ("t4", s_t4, {"z": (1.0, 1.02)}),
    ("t5", s_t5, {"z": (1.0, 1.05), "focus": (1260, 600)}),
    ("t6", s_t6, {"z": (1.0, 1.03)}),
    ("t7", s_t7, {"z": (1.03, 1.06), "cont": True}),
    ("t8", s_t8, {"z": (1.0, 1.0)}),
    ("o1", s_o1, {"z": (1.0, 1.03)}),
    ("o2", s_o2, {"z": (1.0, 1.03)}),
    ("o3", s_o3, {"z": (1.0, 1.02)}),
    ("o4c", s_o4c, {"z": (1.0, 1.04), "focus": (960, 600)}),
    ("o5", s_o5, {"z": (1.0, 1.02)}),
]


def shot_at(t, tl):
    """(index, start, end) of the shot showing at t: each shot runs from its line's start to the next line's start
    (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_yc_spans", None)
    if cache is None:
        cache = [(T(tl, bid), line_end(tl, bid)) for bid, _, _ in SHOTS]
        tl._yc_spans = cache
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
    tint(cr, STORM, out.get("storm", 0.0))
    cr.restore()
    motes(cr, t)
    C.lamp(cr, t, night=out.get("night", 0.0), flash=out.get("flash", 0.0))
    C.title_lift(cr, max(out.get("lift", 0.0) * out.get("night", 0.0) / 0.42, out.get("lift_abs", 0.0)))
    if out.get("ui"):
        out["ui"](cr)
    if t - t0 < 0.22 and not opt.get("cont"):          # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur) for lines y*, t*, o* only, sparse (owner, 8 Nov 2026: "only use sounds where necessary"):
    shimmer as Bhola is revealed, a hit on Yama's thunder, a damaru as the four gates of YAMA'S CITY pop in (after the
    chapter card, so it clears the shimmer at the end of builder B's part by 8 s), a bell as Yama washes the feet,
    shimmer on the closing question. Chosen in THAT order, each at least SFX_MIN_GAP from every sound already
    kept (render_myth.calm_sfx also spaces them across the whole video); the bed dips before the reveals."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(c["t3"]["B"], "shimmer", 0), (c["y9"]["G"], "hit", 0), (y1_times(c["y1"])[1], "damaru", 0),
            (c["t7"]["D"], "bell", 0), (c["o5"]["K"], "shimmer", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["y9"]["R"] - 0.3, "dip", 0.5), (c["t3"]["B"] - 0.35, "dip", 0.5), (c["t6"]["U"] - 0.3, "dip", 0.45),
            (c["o5"]["K"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
