"""Scenes for builder A's parts of long video 2, videos/yamlok_yatra.py ("Yamlok Yatra", landscape 1920x1080): the intro
(i1-i8), the two lives and the night of death (d1-d13), the ten rice-balls (p1-p8). scenes_yamlok_yatra routes every
moment whose active line is i*, d* or p* here; draw() paints the whole frame.

Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code, as in the reels and long video 1: the wide
lamp-lit cloth of scenes_six_a, translucent punched-leather puppets on rods (the shared cast yy_cast: Seth Dhaniram,
his thumb-sized soul, Bhola; garuda_cast's Yamadutas, Yama and the son), two-tier English headlines at the top centre
(a small dark setup line, one big red key line). Long-form pace: a visible change every 2-3 s, faster in the hook.

Respect and calm: Vishnu, Garuda, Yama and the mourners keep their dignity; the messengers are tall dark figures,
fierce but never monstrous; death is two lamps going out and a man closing his eyes; the soul is a little glowing
Dhaniram (comic, never hurt); the noose is a rope of light; nothing gory anywhere. Dhaniram's comedy (no pocket for the
bribe, "commission?!") lands with clear faces and timing.

Every frame is a pure function of t. Cues are words of the Hindi line (CUES: exact substrings, so MISSES stays empty)
with a fraction fallback and minimum gaps. On-screen words are short English, plus हाय, हाय! and पिंड in Devanagari.

Shot list (line: what is on the screen)
  i1  HOOK, frame 0: Dhaniram's little glowing soul alone, big, on a long empty road under a burning sky (a red sun on
      the horizon): WHAT REALLY HAPPENS / AFTER DEATH? (both tiers on from frame 0); on "सुनो" two tall dark messenger
      silhouettes rise behind him; on "तेरह" a DAY 13 badge thumps in and the headline turns: 13 DAYS AFTER DEATH... /
      A 1-YEAR WALK; on "साल" a 1 YEAR / 365 DAYS counter (its days ticking up), "1-YEAR" underlined; on "पैदल" he
      starts to walk, footprints behind him
  i2  the same road: NO FOOD / NO WATER / NO SHADE: three medallions (a plate, a water pot, a tree) pop up one by one
      and are crossed in red as named; on "यमराज" WITH YAMA'S / 2 MESSENGERS; on "दूत" the two Yamadutas step out of
      the shadow (noose, staff), the soul spins round, terrified, shivering
  i3  a film clapper HORROR FILM, crossed out: THIS IS NOT A / HORROR FILM (struck through); on "पुराण" the palm-leaf
      title card MARNE KE BAAD KA SAFAR (GARUDA PURANA · PRETA KALPA): IT'S ALL IN THE / GARUDA PURANA; on "विष्णु"
      Vishnu (tag) speaks, Garuda (tag) listens with folded hands, sound rings: VISHNU HIMSELF TOLD GARUDA / DAY BY
      DAY, small palm leaves DAY 1, DAY 2, DAY 3... float from Vishnu to Garuda
  i4  two dark silhouettes walk in from either side, a "?" over each: TODAY THE JOURNEY, WITH / 2 TRAVELLERS
  i5  the left one lights up: Seth Dhaniram (smug, tag), his safe beside him swings open on its gold (RICHEST stamp),
      then slams shut as he clutches his keys (STINGIEST stamp): TRAVELLER 1: / SETH DHANIRAM
  i6  the right one lights up: Bhola with his water pot (smile, tag), POOR WATER-SELLER leaf; Dhaniram turns his nose
      up: TRAVELLER 2: / BHOLA
  i7  both stand; a banner OUR STORY'S TRAVELLERS hangs between them; on "पर" a palm-leaf book rises and opens: WHAT
      HAPPENS TO THEM: / GARUDA PURANA (ringed, a tick on "लिखा"): headline the same
  i8  split screen: left, Dhaniram trembles before a huge dark Yama (red glow): ONE WILL BE SCARED...; right, in gold
      light, Yama kneels and washes the feet of a seated figure in shadow with a big "?": ONE WILL BE WELCOMED;
      WATCH TILL THE END...
  d1  chapter card DHANIRAM & BHOLA / THE LAST NIGHT; then Dhaniram's shop (striped awning, sacks, a hanging scale), he
      sits on his gaddi beside his safe; the sun blazes; a thirsty traveller comes up, cupped hands, cloud PAANI...?;
      Dhaniram raises a finger (angry): cloud PAANI MUFT / NAHI AATA!, then AAGE BADHO!; the man trudges off:
      IN THE HEAT, A THIRSTY MAN ASKED FOR WATER / NO FREE WATER!
  d2  he turns to his safe: it opens on heaps of gold (glow, coins hop), smug: HIS SAFE WAS / FULL OF GOLD; a roti pops
      up and is crossed; badge FREE ROTIS GIVEN: 0: BUT IN HIS WHOLE LIFE / NOT ONE FREE ROTI
  d3  the lane: Bhola walks in with his pot; a coin drops into his bowl: AND BHOLA? / HE SOLD WATER; the same thirsty
      traveller comes, shows empty hands (NO MONEY); Bhola smiles and pours water into his hands, the man smiles:
      BUT IF SOMEONE COULDN'T PAY / FREE WATER
  d4  sunrise: Bhola breaks his roti in two and feeds half to the street cow: EVERY MORNING, / HALF HIS ROTI TO THE COW;
      dusk, his hut, a lamp: he kneels and presses his old mother's feet (she smiles): EVERY EVENING / HIS MOTHER'S FEET
  d5  night, a crescent moon: Dhaniram's haveli with a brass lamp, Bhola's hut with a clay lamp; on "पूरी" both flames
      go out (smoke): THEN, ONE NIGHT... / BOTH LIVES ENDED
  d6  Dhaniram on his bed, eyes open; above him the worlds (sun, moon, stars, earth, lands) pop up in a ring and merge
      into one bright circle: GARUDA PURANA: AT THE LAST MOMENT / ALL WORLDS AS ONE; a speech cloud "..." from him is
      crossed out: HE CAN'T / SAY A WORD
  d7  his room at night; two messengers step in through the dark doorway: THEN CAME / TWO MESSENGERS; a crow flies
      across: BLACK AS CROWS; tags HAIR ON END, NOOSE, STAFF ringed as named
  d8  a messenger casts a noose of light; the little glowing Dhaniram is drawn up out of his chest: THEY PULLED OUT /
      HIS SOUL; a big thumb rises beside it, dotted lines from tip and base: THUMB-SIZED
  d9  close: the little soul, hands to his head, crying: cloud HAAY HAAY! with हाय, हाय!; he turns and stares at his
      own body on the bed (tag HIS OWN BODY): LITTLE DHANIRAM CRIED / HAAY HAAY!, then AND STARED AT / HIS OWN BODY
  d10 a loop of light drops round his neck; the messenger: cloud CHAL! JALDI CHAL!, a tug: A NOOSE, AND THEN... /
      CHAL! JALDI CHAL!
  d11 he pats his side for his purse, sheepish: cloud BHAI SAHAB... KUCH LE-DEKAR?, rubbing his fingers; the two
      messengers look at each other; a red ring at his side, stamp NO POCKET!: A BRIBE? / NO POCKET!
  d12 Yama's hall: the soul streaks in before Yama on his throne (tag YAMA): IN A SHORT TIME / BEFORE YAMA; Yama raises
      his hand, the soul flies up along a dotted arc as the hall fades to the night, down at his house door: BY YAMA'S
      ORDER, THROUGH THE AIR / BACK HOME
  d13 his room: his body under a white sheet, his son and his wife weeping (EVERYONE WAS CRYING); the soul dives at his
      body twice and bounces back, the noose of light pulls him back to the messenger at the door: HE TRIED TO GET
      BACK IN... / THE NOOSE PULLED HIM BACK
  p1  chapter card 10 DAYS, / 10 RICE-BALLS; the soul floats beside a dotted Dhaniram-shaped outline (NO BODY), the
      long road behind, a red "?": NO BODY... / HOW WILL HE WALK?
  p2  the son kneels by a lamp and sets a rice-ball on a banana leaf; a word card पिंड = PINDA, A RICE-BALL; badge
      10 DAYS; a dotted body takes shape at the right, light flows from the ball into it: FOR 10 DAYS, THE SON OFFERS
      / RICE-BALLS, then EACH ONE BUILDS / A NEW BODY PART
  p3  the new body, big, as a faint shadow; a DAY counter and the leaf of ten balls; each day a ball drops on the leaf
      and a band of the body forms from the top (a glow at the forming edge), a DAY n tag at the part: DAY 1: / HEAD,
      DAY 2: / NECK & SHOULDERS, DAY 3: / HEART (a red heart glows in the chest)
  p4  the same: DAY 4: / BACK, DAY 5: / NAVEL, DAY 6: / HIPS, DAY 7: / THIGHS, DAY 8: / KNEES, DAY 9: / FEET
  p5  DAY 10: the whole body glows; his hand goes to his belly (rumble lines, HUNGER), then to his throat (THIRST):
      DAY 10: / HUNGER & THIRST
  p6  one big rice-ball on a leaf splits into four portions: A FUNNY THING: EACH RICE-BALL HAS / 4 PORTIONS; two glow
      BODY, BODY; one goes to little Dhaniram, who eats it (DHANIRAM); the last gets a "?", then a messenger's hand
      takes it: YAMADUTAS: AND ONE GOES TO THE / MESSENGERS!
  p7  Dhaniram, outraged, finger up: cloud YAHAN BHI / COMMISSION?!; the messenger chews on: EVEN HERE, / COMMISSION?!
  p8  his new body beside a big open hand, dotted lines: HAND-SIZED; then the burning road: a DAY 13 badge, a rope
      binds his hands, an inset of a captured monkey, the two messengers lead him off along the road: DAY 13: TIED UP
      / LIKE A CAPTURED MONKEY
"""
import bisect
import math
import random

import cairo

import ashtavakra_cast  # noqa: F401  (registers the brass lamp)
import dharmavyadha_cast as DV  # noqa: F401  (registers the room, house, cot, plate, the traveller and the mother)
import garuda_cast as GC
import kaikeyi_cast as K
import kumbhakarna_cast  # noqa: F401  (registers kb_world)
import lrekha_cast  # noqa: F401  (registers the hut, the palm leaves, the speech cloud)
import mandhata_cast as M  # noqa: F401  (registers md_throne, md_world)
import puppet_core as pc
import ruru_cast as RU
import shani_cast as SG
import six_cast_b  # noqa: F401  (registers Yama's hall)
import snake_cast as SN
import yy_cast as Y
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, text_size
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from puppet_cast import _jewel, _shape
from puppet_core import band, dots_in, ell, ink, leather, poly, register, rivet
from scenes_arjuna import HAS_INDIC, indic_surface
from scenes_dharmavyadha import hus, kmo
from scenes_garuda_purana import bezier, diya, duta, light_rope, noose_loop, pinda, ripple, yama_seated
from scenes_jarasandha import INK, RED, fit, glow, man_angles, red_ring, small_line, stamp, stars, walk_legs
from scenes_jayadratha import SIL, flash_at, silhouette, tag, tint, to_user
from scenes_kaikeyi import ANJALI, fig
from scenes_lakshman_rekha import big_x, book, sparkle
from scenes_mandhata import aura, burst, lights, mix, reach_arm
from scenes_ravana import dotted
from scenes_ruru import flow, nods, plate
from scenes_six_a import big_mark, card_out, chapter, head, lamp, stage, title_lift
from scenes_six_b import counter_badge
from shots import T

MISSES = set()                       # cue words not found in a line (falls back to fractions)
FLOOR = 905.0                        # the stage floor (feet)
SM = 0.58                            # a standing man's scale (Dhaniram ~610 px tall)
NIGHT = 0.42
GOLDC = (1.0, 0.86, 0.45)
SRC = "GARUDA PURANA · PRETA KALPA"


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
    "i1": (("Q", "क्या", 0.12, (("t0", 0.3),)),
           ("L", "सुनो", 0.3, (("Q", 0.5),)),
           ("T", "तेरह", 0.45, (("L", 0.6),)),
           ("S", "सफ़र", 0.62, (("T", 0.5),)),
           ("Y", "साल", 0.85, (("S", 0.5),)),
           ("P", "पैदल", 0.95, (("Y", 0.3),))),
    "i2": (("F", "खाना", 0.08, (("t0", 0.15),)),
           ("W", "पानी", 0.2, (("F", 0.45),)),
           ("S", "छाँव", 0.32, (("W", 0.45),)),
           ("Y", "यमराज", 0.75, (("S", 0.8),)),
           ("D", "दूत", 0.92, (("Y", 0.35),))),
    "i3": (("F", "फ़िल्म", 0.15, (("t0", 0.3),)),
           ("N", "नहीं", 0.22, (("F", 0.3),)),
           ("G", "पुराण", 0.35, (("N", 0.6),)),
           ("V", "विष्णु", 0.5, (("G", 1.1),)),
           ("K", "ख़ुद", 0.58, (("V", 0.3),)),
           ("D", "दिन-ब-दिन", 0.85, (("K", 0.6),)),
           ("B", "बताया", 0.93, (("D", 0.3),))),
    "i4": (("D", "दो", 0.45, (("t0", 0.5),)),
           ("L", "लोगों", 0.55, (("D", 0.2),))),
    "i5": (("N", "धनीराम", 0.18, (("t0", 0.2),)),
           ("A", "अमीर", 0.48, (("N", 0.7),)),
           ("K", "कंजूस", 0.9, (("A", 0.9),))),
    "i6": (("B", "भोला", 0.2, (("t0", 0.15),)),
           ("G", "ग़रीब", 0.65, (("B", 0.7),)),
           ("W", "पानी", 0.8, (("G", 0.3),))),
    "i7": (("K", "कहानी", 0.18, (("t0", 0.4),)),
           ("M", "मुसाफ़िर", 0.38, (("K", 0.5),)),
           ("P", "पर", 0.5, (("M", 0.5),)),
           ("G", "गरुड़", 0.78, (("P", 0.8),)),
           ("L", "लिखा", 0.92, (("G", 0.4),))),
    "i8": (("W", "आख़िर", 0.05, ()),
           ("O", "एक", 0.35, (("W", 0.8),)),
           ("S", "डराएँगे", 0.5, (("O", 0.4),)),
           ("T", "दूसरे", 0.65, (("S", 0.5),)),
           ("P", "पैर", 0.72, (("T", 0.3),)),
           ("F", "धोएँगे", 0.92, (("P", 0.5),))),
    "d1": (("Du", "दुकान", 0.12, (("t0", 0.2),)),
           ("G", "गर्मी", 0.25, (("Du", 0.3),)),
           ("P", "प्यासा", 0.33, (("G", 0.3),)),
           ("M", "माँगता", 0.45, (("P", 0.4),)),
           ("K", "कहता", 0.55, (("M", 0.4),)),
           ("F", "मुफ़्त", 0.68, (("K", 0.3),)),
           ("A", "आगे", 0.88, (("F", 0.6),))),
    "d2": (("T", "तिजोरी", 0.08, (("t0", 0.1),)),
           ("S", "सोने", 0.2, (("T", 0.4),)),
           ("Z", "ज़िंदगी", 0.5, (("S", 0.8),)),
           ("R", "रोटी", 0.72, (("Z", 0.5),)),
           ("N", "नहीं", 0.9, (("R", 0.5),))),
    "d3": (("B", "भोला", 0.05, ()),
           ("S", "बेचता", 0.35, (("B", 0.8),)),
           ("P", "प्यासा", 0.58, (("S", 0.8),)),
           ("Pa", "पैसे", 0.66, (("P", 0.3),)),
           ("F", "मुफ़्त", 0.85, (("Pa", 0.6),)),
           ("D", "पिला", 0.93, (("F", 0.2),))),
    "d4": (("S", "सुबह", 0.05, ()),
           ("R", "रोटी", 0.15, (("S", 0.3),)),
           ("A", "आधी", 0.25, (("R", 0.4),)),
           ("G", "गाय", 0.38, (("A", 0.5),)),
           ("E", "शाम", 0.58, (("G", 0.9),)),
           ("M", "माँ", 0.8, (("E", 0.6),)),
           ("P", "दबाता", 0.92, (("M", 0.3),))),
    "d5": (("R", "रात", 0.2, (("t0", 0.2),)),
           ("D", "दोनों", 0.45, (("R", 0.3),)),
           ("P", "पूरी", 0.75, (("D", 0.4),))),
    "d6": (("A", "आख़िरी", 0.22, (("t0", 0.4),)),
           ("S", "सारी", 0.45, (("A", 0.6),)),
           ("E", "दिखती", 0.62, (("S", 0.6),)),
           ("B", "बोल", 0.85, (("E", 0.8),))),
    "d7": (("D", "दूत", 0.33, (("t0", 0.4),)),
           ("C", "कौवे", 0.48, (("D", 0.6),)),
           ("H", "बाल", 0.65, (("C", 0.6),)),
           ("N", "फंदा", 0.82, (("H", 0.5),)),
           ("S", "डंडा", 0.95, (("N", 0.4),))),
    "d8": (("A", "आत्मा", 0.35, (("t0", 0.5),)),
           ("P", "खींचकर", 0.45, (("A", 0.3),)),
           ("O", "निकाली", 0.62, (("P", 0.5),)),
           ("T", "अंगूठे", 0.78, (("O", 0.4),))),
    "d9": (("C", "चिल्लाया", 0.22, (("t0", 0.3),)),
           ("H", "हाय", 0.38, (("C", 0.3),)),
           ("S", "शरीर", 0.7, (("H", 0.8),)),
           ("L", "देखता", 0.82, (("S", 0.3),))),
    "d10": (("N", "फंदा", 0.3, (("t0", 0.4),)),
            ("B", "बोले", 0.6, (("N", 0.5),)),
            ("C", "जल्दी", 0.82, (("B", 0.3),))),
    "d11": (("J", "जेब", 0.15, (("t0", 0.3),)),
            ("B", "भाई", 0.28, (("J", 0.5),)),
            ("L", "ले-देकर", 0.42, (("B", 0.4),)),
            ("P", "पर", 0.62, (("L", 0.6),)),
            ("N", "नहीं", 0.92, (("P", 0.6),))),
    "d12": (("D", "देर", 0.18, (("t0", 0.3),)),
            ("S", "सामने", 0.32, (("D", 0.4),)),
            ("H", "हुक्म", 0.55, (("S", 0.8),)),
            ("A", "हवा", 0.68, (("H", 0.5),)),
            ("G", "घर", 0.9, (("A", 0.6),))),
    "d13": (("R", "रो", 0.08, (("t0", 0.15),)),
            ("G", "घुसना", 0.45, (("R", 0.9),)),
            ("F", "फंदा", 0.75, (("G", 0.9),)),
            ("P", "पीछे", 0.85, (("F", 0.3),))),
    "p1": (("S", "शरीर", 0.3, (("t0", 0.4),)),
           ("N", "नहीं", 0.42, (("S", 0.3),)),
           ("A", "आगे", 0.62, (("N", 0.4),)),
           ("K", "कैसे", 0.93, (("A", 0.5),))),
    "p2": (("D", "दस", 0.22, (("t0", 0.6),)),
           ("B", "बेटा", 0.35, (("D", 0.4),)),
           ("P", "पिंड", 0.48, (("B", 0.4),)),
           ("C", "चढ़ाता", 0.55, (("P", 0.3),)),
           ("H", "हर", 0.67, (("C", 0.5),)),
           ("N", "नए", 0.8, (("H", 0.4),)),
           ("Hi", "हिस्सा", 0.92, (("N", 0.3),))),
    "p3": (("D1", "पहले", 0.02, ()),
           ("H1", "सिर", 0.15, (("D1", 0.35),)),
           ("D2", "दूसरे", 0.3, (("H1", 0.45),)),
           ("H2", "गर्दन", 0.45, (("D2", 0.35),)),
           ("D3", "तीसरे", 0.72, (("H2", 0.7),)),
           ("H3", "दिल", 0.9, (("D3", 0.35),))),
    "p4": (("D4", "चौथे", 0.02, ()),
           ("H4", "पीठ", 0.15, (("D4", 0.3),)),
           ("D5", "पाँचवें", 0.3, (("H4", 0.35),)),
           ("H5", "नाभि", 0.45, (("D5", 0.35),)),
           ("H6", "कमर", 0.6, (("H5", 0.5),)),
           ("H7", "जांघें", 0.72, (("H6", 0.4),)),
           ("H8", "घुटने", 0.84, (("H7", 0.4),)),
           ("H9", "पैर", 0.95, (("H8", 0.4),))),
    "p5": (("D", "दसवें", 0.15, ()),
           ("Hu", "भूख", 0.6, (("D", 0.7),)),
           ("Th", "प्यास", 0.9, (("Hu", 0.6),))),
    "p6": (("M", "मज़ेदार", 0.12, (("t0", 0.2),)),
           ("C", "चार", 0.3, (("M", 0.6),)),
           ("B", "दो", 0.45, (("C", 0.8),)),
           ("E", "खाता", 0.65, (("B", 0.8),)),
           ("Q", "एक?", 0.78, (("E", 0.6),)),
           ("Y", "यमदूतों", 0.88, (("Q", 0.5),))),
    "p7": (("B", "बोला", 0.3, ()),
           ("C", "कमीशन", 0.75, (("B", 0.4),))),
    "p8": (("H", "हाथ", 0.25, (("t0", 0.4),)),
           ("T", "तेरहवें", 0.45, (("H", 0.8),)),
           ("B", "बंदर", 0.7, (("T", 0.8),)),
           ("Ba", "बाँधकर", 0.78, (("B", 0.3),)),
           ("C", "चले", 0.95, (("Ba", 0.5),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_ya_cues", None)
    if cache is None:
        cache = {}
        tl._ya_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, word, frac, cons in CUES[bid]:
            v = cue(tl, bid, word, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


def lang(tl):
    return getattr(tl, "lang", "hi")


# ------------------------------------------------------------------ text helpers


def parts_line(cr, t, parts, y, size, font=HEAD_FONT, alpha=1.0, gap=None, anchor_x=W / 2):
    """A centred line laid out in full from the start, each piece [(text, t_in, colour)] popping in at its own time.
    Returns the boxes [(x, y, w, h)]."""
    gap = size * 0.32 if gap is None else gap
    ws = [text_size(p, size, font)[0] for p, _, _ in parts]
    x = anchor_x - (sum(ws) + gap * (len(parts) - 1)) / 2
    boxes = []
    for (p, ti, col), w_ in zip(parts, ws):
        q = prog(t, ti, 0.22)
        if q > 0:
            k = 1.15 - 0.15 * back(clamp((t - ti) / 0.3))
            h_ = text_size(p, size, font)[1]
            cr.save()
            cr.translate(x + w_ / 2, y + h_ / 2)
            cr.scale(k, k)
            draw_text(cr, p, -w_ / 2, -h_ / 2, size, col, q * alpha, font)
            cr.restore()
        boxes.append((x, y, w_, text_size(p, size, font)[1]))
        x += w_ + gap
    return boxes


def strike_at(cr, t, box, t_in, alpha=1.0, w=14):
    """A red stroke striking a text box (x, y, w, h) through, drawn from left to right at t_in."""
    if box is None or t <= t_in:
        return
    p = ease((t - t_in) / 0.3)
    x, y, w_, h_ = box
    cr.save()
    cr.set_source_rgba(*RED, 0.95 * alpha)
    cr.set_line_width(w)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(x - 16, y + h_ * 0.58)
    cr.line_to(x - 16 + (w_ + 32) * p, y + h_ * 0.58 - 10 * p)
    cr.stroke()
    cr.restore()


def underline(cr, t, x0, x1, y, t_in, alpha=1.0):
    if t <= t_in:
        return
    q = ease((t - t_in) / 0.35)
    cr.save()
    cr.set_source_rgba(*RED, 0.9 * alpha)
    cr.set_line_width(12)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(x0, y)
    cr.curve_to(x0 + (x1 - x0) * 0.3, y - 8, x0 + (x1 - x0) * 0.6, y + 8, x0 + (x1 - x0) * q, y)
    cr.stroke()
    cr.restore()


def deva(cr, t, t_in, text, x, y, size, color=INK, alpha=1.0):
    """Devanagari text centred on (x, y) (left out without the Nirmala font)."""
    if not HAS_INDIC or t < t_in or alpha <= 0.01:
        return
    q = prog(t, t_in, 0.3) * alpha
    su = indic_surface(text, int(size), tuple(color))
    w_, h_ = su.get_width(), su.get_height()
    yy = y + 12 * (1 - q)
    pc.poly(cr, [(x - w_ / 2 - 28, yy - h_ / 2 - 14), (x + w_ / 2 + 28, yy - h_ / 2 - 14), (x + w_ / 2 + 40, yy),
                 (x + w_ / 2 + 28, yy + h_ / 2 + 14), (x - w_ / 2 - 28, yy + h_ / 2 + 14), (x - w_ / 2 - 40, yy)])
    cr.set_source_rgba(0.97, 0.87, 0.62, 0.96 * q)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, q)
    cr.set_line_width(3.5)
    cr.stroke()
    cr.set_source_surface(su, x - w_ / 2, yy - h_ / 2)
    cr.paint_with_alpha(q)


def caption(cr, t, t_in, text, x, y, size=56, color=RED, alpha=1.0, t_out=None, field=(0.97, 0.88, 0.66)):
    """A key caption on a parchment strip (in a panel), centred on (x, y), popping in at t_in."""
    q = back(clamp((t - t_in) / 0.3), 1.6)
    a = clamp(q) * alpha
    if t_out is not None:
        a *= 1 - prog(t, t_out, 0.25)
    if a <= 0.01:
        return
    w_, h_ = text_size(text, size)
    k = 0.8 + 0.2 * q
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    cr.rotate(-0.015)
    pc.poly(cr, [(-w_ / 2 - 34, -h_ / 2 - 16), (w_ / 2 + 34, -h_ / 2 - 16), (w_ / 2 + 46, 0),
                 (w_ / 2 + 34, h_ / 2 + 16), (-w_ / 2 - 34, h_ / 2 + 16), (-w_ / 2 - 46, 0)])
    cr.set_source_rgba(*field, 0.95 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(4)
    cr.stroke()
    draw_text(cr, text, 0, 2, size, color, a, anchor="cm")
    cr.restore()


CLOUD_C = (0.99, 0.94, 0.80)


def say(cr, t, t_in, x, y, lines, tail=None, alpha=1.0, t_out=None, pad=30):
    """An opaque speech cloud centred on (x, y) (screen px; it never lets a busy set show through the words):
    lines = [(text, size, colour, t_show)], the tail pointing at `tail` (x, y)."""
    q = back(clamp((t - t_in) / 0.3), 1.6)
    a = clamp(q) * alpha
    if t_out is not None:
        a *= 1 - prog(t, t_out, 0.25)
    if a <= 0.01:
        return
    tw = max(text_size(txt, sz)[0] for txt, sz, _, _ in lines)
    th = sum(sz * 1.12 for _, sz, _, _ in lines)
    rw, rh = tw / 2 + pad + 24, th / 2 + pad
    k = 0.75 + 0.25 * q
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    n = 14
    bumps = [(rw * math.cos(2 * math.pi * i / n), rh * math.sin(2 * math.pi * i / n), 0.42 * rh + 10)
             for i in range(n)]
    tri = None
    if tail is not None:
        tx, ty = (tail[0] - x) / k, (tail[1] - y) / k
        ang = math.atan2(ty, tx)
        ex, ey = 0.7 * rw * math.cos(ang), 0.7 * rh * math.sin(ang)
        d = math.hypot(tx - ex, ty - ey)
        ux, uy = (tx - ex) / max(1, d), (ty - ey) / max(1, d)
        tip = (ex + ux * min(d - 20, 140 + 0.25 * d), ey + uy * min(d - 20, 140 + 0.25 * d))
        nx, ny = -uy, ux
        tri = [(ex + nx * 34, ey + ny * 34), tip, (ex - nx * 34, ey - ny * 34)]
    for col, grow in ((pc.INK, 5.0), (CLOUD_C, 0.0)):
        cr.set_source_rgba(*col, 0.97 * a)
        if tri:
            pc.poly(cr, [(px + (grow if px > 0 else -grow) * 0.3, py) for px, py in tri])
            if grow:
                cr.set_line_width(2 * grow)
                cr.set_line_join(cairo.LINE_JOIN_ROUND)
                cr.stroke_preserve()
            cr.fill()
        cr.new_path()
        pc.ell(cr, 0, 0, rw + grow, rh + grow)
        cr.fill()
        for bx, by, br in bumps:
            cr.new_path()
            cr.arc(bx, by, br + grow, 0, 2 * math.pi)
            cr.fill()
    yy = -th / 2
    for txt, sz, col, ts in lines:
        p = prog(t, ts, 0.22) * a
        if p > 0:
            kk = 1.12 - 0.12 * back(clamp((t - ts) / 0.3))
            cr.save()
            cr.translate(0, yy + sz * 0.56)
            cr.scale(kk, kk)
            draw_text(cr, txt, 0, 0, sz, col, p, anchor="cm")
            cr.restore()
        yy += sz * 1.12
    cr.restore()


def medallion(cr, t, t_in, x, y, r, draw_in, alpha=1.0, cross_t=None):
    """A round cream medallion popping in at t_in with an icon (draw_in(cr) in medallion pixels round its centre);
    cross_t = a red X across it."""
    q = back(clamp((t - t_in) / 0.32), 1.8)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    rr = r * (0.6 + 0.4 * q)
    glow(cr, x, y, rr * 2.0, 0.3 * a)
    cr.save()
    cr.arc(x, y, rr, 0, 2 * math.pi)
    cr.set_source_rgba(0.97, 0.88, 0.66, 0.95 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(5)
    cr.stroke()
    cr.arc(x, y, rr - 11, 0, 2 * math.pi)
    cr.set_source_rgba(0.80, 0.55, 0.15, a)
    cr.set_line_width(3)
    cr.stroke()
    cr.translate(x, y)
    cr.scale(rr / r, rr / r)
    draw_in(cr, a)
    cr.restore()
    if cross_t is not None and t > cross_t:
        big_x(cr, x, y, 1.5 * r, 1.5 * r, prog(t, cross_t, 0.3), a)


def sil(cr, fn, a=1.0, col=SIL):
    return silhouette(cr, fn, a, col)


def rings(cr, t, t0, x, y, side=1, n=3, period=0.3, rmax=260, alpha=1.0, color=INK):
    """A voice going out: arcs spreading on one side of (x, y)."""
    for i in range(n):
        p = (t - t0 - i * period) / 1.0
        if 0 < p < 1:
            r = 30 + rmax * ease(p)
            cr.set_source_rgba(*color, 0.55 * (1 - p) * alpha)
            cr.set_line_width(10 * (1 - p) + 3)
            a0 = 0.0 if side > 0 else math.pi
            cr.new_path()
            cr.arc(x, y, r, a0 - 0.35 * math.pi, a0 + 0.35 * math.pi)
            cr.stroke()


def smoke(cr, t, t0, x, y, alpha=1.0):
    """A thin curl of smoke rising from a lamp that has just gone out."""
    u = (t - t0) / 2.2
    if u <= 0 or u >= 1:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    pts = [(x + 14 * math.sin(k * 0.9 + t * 2.0) * k / 6, y - 26 * k * (0.3 + u)) for k in range(7)]
    cr.new_path()
    pc.spath(cr, pts, closed=False)
    cr.set_source_rgba(0.85, 0.82, 0.78, 0.6 * (1 - u) * alpha)
    cr.set_line_width(7)
    cr.stroke()
    cr.restore()


def footprints(cr, t, pts, t0, dt=0.35, alpha=1.0):
    """Small footprints that appear one by one along pts from t0."""
    for i, (x, y, s) in enumerate(pts):
        q = prog(t, t0 + i * dt, 0.25) * alpha
        if q <= 0:
            continue
        cr.save()
        cr.translate(x, y + (8 * s if i % 2 else 0))
        cr.scale(s, s * 0.45)
        cr.arc(0, 0, 16, 0, 2 * math.pi)
        cr.set_source_rgba(0.35, 0.16, 0.08, 0.55 * q)
        cr.fill()
        cr.restore()


# ------------------------------------------------------------------ the new sprites (ya_*)


SHOP_TOP = 140.0                     # the gaddi's top above the floor (shop units)


def _shop(cr):
    """Dhaniram's shop (pivot at the floor centre): a plastered back wall with two shelves of grain sacks and clay
    jars, a hanging balance, carved wooden posts, a red-and-cream scalloped awning, a wooden takht with a white gaddi
    (cushion) and a round bolster."""
    wall = [(-720, 0), (720, 0), (720, -760), (-720, -760)]
    _shape(cr, wall, (0.88, 0.66, 0.40), 6, smooth=False, holes=(14, 22, 2.6))
    dots_in(cr, lambda: poly(cr, [(-690, -40), (690, -40), (690, -730), (-690, -730)]), 46, 3.0, shape="d")
    rng = random.Random(5)
    for sy in (-560, -330):                                            # shelves with sacks and jars
        band(cr, [(-600, sy), (600, sy)], 18, (0.52, 0.30, 0.14), spacing=16, hole_r=2.4)
        x = -560
        while x < 560:
            if rng.random() < 0.55:
                w_ = rng.uniform(70, 100)
                h_ = rng.uniform(90, 130)
                sack = [(x, sy - 8), (x + w_, sy - 8), (x + w_ - 6, sy - h_ * 0.8), (x + w_ * 0.75, sy - h_),
                        (x + w_ * 0.25, sy - h_), (x + 6, sy - h_ * 0.8)]
                _shape(cr, sack, (0.82, 0.66, 0.42), 4)
                ink(cr, [(x + w_ * 0.25, sy - h_ * 0.86), (x + w_ * 0.75, sy - h_ * 0.86)], 3)
                band(cr, [(x + 8, sy - h_ * 0.5), (x + w_ - 8, sy - h_ * 0.5)], 7, RED, holes=False, lw=2)
                x += w_ + 12
            else:
                r_ = rng.uniform(34, 46)
                cr.new_path()
                cr.arc(x + r_, sy - 8 - r_, r_, 0, 2 * math.pi)
                leather(cr, Y.CLAY if rng.random() < 0.5 else (0.70, 0.50, 0.24), 4)
                _shape(cr, [(x + r_ - 14, sy - 8 - 2 * r_ + 4), (x + r_ + 14, sy - 8 - 2 * r_ + 4),
                            (x + r_ + 10, sy - 2 * r_ - 26), (x + r_ - 10, sy - 2 * r_ - 26)], Y.CLAY2, 3, smooth=False)
                x += 2 * r_ + 14
    ink(cr, [(380, -740), (380, -660)], 3)                              # the hanging balance
    ink(cr, [(300, -660), (460, -660)], 6)
    for bx in (300, 460):
        ink(cr, [(bx, -660), (bx - 30, -590)], 2)
        ink(cr, [(bx, -660), (bx + 30, -590)], 2)
        cr.new_path()
        ell(cr, bx, -588, 38, 10)
        leather(cr, (0.85, 0.62, 0.22), 3)
    for sx in (-1, 1):                                                  # carved posts
        x = sx * 690
        _shape(cr, [(x - 30, 0), (x + 30, 0), (x + 30, -780), (x - 30, -780)], (0.50, 0.28, 0.12), 5, smooth=False,
               holes=(9, 16, 2.4))
        for y in (-120, -380, -640):
            band(cr, [(x - 30, y), (x + 30, y)], 14, GOLDC, holes=False, lw=3)
    beam = [(-760, -770), (760, -770), (760, -820), (-760, -820)]
    _shape(cr, beam, (0.50, 0.28, 0.12), 5, smooth=False)
    n = 13                                                              # the scalloped awning
    for i in range(n):
        x0 = -760 + 1520 * i / n
        x1 = -760 + 1520 * (i + 1) / n
        col = RED if i % 2 == 0 else (0.99, 0.93, 0.80)
        cr.new_path()
        cr.move_to(x0, -900)
        cr.line_to(x1, -900)
        cr.line_to(x1, -800)
        cr.curve_to(x1, -760, x0, -760, x0, -800)
        cr.close_path()
        leather(cr, col, 4)
    band(cr, [(-770, -900), (770, -900)], 16, GOLDC, spacing=13, hole_r=2.4)
    # the takht and the gaddi
    _shape(cr, [(-560, 0), (-540, -110), (540, -110), (560, 0)], (0.56, 0.32, 0.14), 6, smooth=False,
           holes=(10, 18, 2.6))
    for x in (-520, -180, 180, 520):
        _shape(cr, [(x - 20, 0), (x + 20, 0), (x + 16, -40), (x - 16, -40)], (0.40, 0.22, 0.10), 4, smooth=False)
    _shape(cr, [(-546, -110), (546, -110), (540, -SHOP_TOP), (-540, -SHOP_TOP)], (0.99, 0.96, 0.88), 5,
           smooth=False)
    band(cr, [(-546, -116), (546, -116)], 8, RED, holes=False, lw=2.5)
    cr.new_path()                                                       # the round bolster at the left
    ell(cr, -470, -SHOP_TOP - 50, 60, 52)
    leather(cr, (0.80, 0.16, 0.14), 5)
    band(cr, [(-470, -SHOP_TOP - 100), (-470, -SHOP_TOP)], 12, GOLDC, holes=False, lw=3)


register("ya_shop", (-780, -920, 780, 12), _shop)


BED_TOP = 300.0                      # the mattress top above the floor (bed units)


def _bed(cr):
    """A rich man's carved bed (palang), pivot at the floor centre: turned legs with gold knobs, a carved headboard
    at the left, a thick mattress, a pillow, a red-and-gold spread hanging over the front."""
    for x in (-430, 430):
        _shape(cr, [(x - 26, 0), (x + 26, 0), (x + 30, -60), (x + 18, -120), (x + 26, -200), (x - 26, -200),
                    (x - 18, -120), (x - 30, -60)], (0.50, 0.26, 0.10), 5, smooth=False)
        cr.new_path()
        cr.arc(x, -128, 16, 0, 2 * math.pi)
        leather(cr, GOLDC, 3)
    hb = [(-470, -200), (-470, -560), (-440, -600), (-400, -560), (-400, -200)]
    _shape(cr, hb, (0.50, 0.26, 0.10), 5, smooth=False, holes=(9, 16, 2.4))
    _jewel(cr, -435, -540, 16, RED)
    _shape(cr, [(-460, -200), (460, -200), (460, -240), (-460, -240)], (0.58, 0.32, 0.14), 5, smooth=False)
    _shape(cr, [(-440, -240), (450, -240), (456, -BED_TOP), (-440, -BED_TOP)], (0.99, 0.95, 0.86), 5, smooth=False)
    spread = [(-300, -BED_TOP + 6), (460, -BED_TOP + 6), (470, -130), (-300, -130)]
    _shape(cr, spread, (0.80, 0.14, 0.12), 5, smooth=False)
    dots_in(cr, lambda: poly(cr, spread), 26, 3.2, shape="d")
    band(cr, [(-300, -140), (470, -140)], 16, GOLDC, spacing=12, hole_r=2.2)
    cr.new_path()
    ell(cr, -360, -BED_TOP - 22, 70, 30)
    leather(cr, (0.99, 0.95, 0.86), 4)
    band(cr, [(-420, -BED_TOP - 22), (-300, -BED_TOP - 22)], 6, GOLDC, holes=False, lw=2)


register("ya_bed", (-490, -620, 490, 12), _bed)


def _roti(cr, half=False):
    """A roti (pivot at the centre): pale brown with toasted spots; half=True: the left half, torn."""
    cr.new_path()
    if half:
        cr.move_to(0, -70)
        cr.arc_negative(0, 0, 70, -math.pi / 2, math.pi / 2)
        for k in range(6):
            cr.line_to(8 * (1 if k % 2 else -1), 70 - 28 * (k + 1))
        cr.close_path()
    else:
        cr.arc(0, 0, 70, 0, 2 * math.pi)
    leather(cr, (0.94, 0.80, 0.52), 5)
    rng = random.Random(3)
    for _ in range(9):
        a, r = rng.uniform(0, 2 * math.pi), rng.uniform(10, 54)
        x, y = r * math.cos(a), r * math.sin(a)
        if half and x > 0:
            continue
        cr.new_path()
        ell(cr, x, y, rng.uniform(6, 12), rng.uniform(4, 8), a)
        cr.set_source_rgb(0.62, 0.40, 0.18)
        cr.fill()


register("ya_roti", (-80, -80, 80, 80), _roti)
register("ya_roti_half", (-80, -80, 20, 80), lambda cr: _roti(cr, True))


def _clap(cr):
    """A film clapperboard (pivot at the centre of the slate); the text goes on per frame."""
    slate = [(-230, -110), (230, -110), (230, 170), (-230, 170)]
    _shape(cr, slate, (0.24, 0.23, 0.27), 6, smooth=False)
    for y in (0, 60):
        ink(cr, [(-210, y + 30), (210, y + 30)], 3, smooth=False, col=(0.85, 0.82, 0.76))
    cr.save()
    cr.translate(-230, -110)
    cr.rotate(-0.22)
    bar = [(0, 0), (460, 0), (460, -60), (0, -60)]
    _shape(cr, bar, (0.24, 0.23, 0.27), 5, smooth=False)
    for k in range(6):
        x = 20 + 76 * k
        _shape(cr, [(x, 0), (x + 36, 0), (x + 66, -60), (x + 30, -60)], (0.96, 0.94, 0.88), 0, smooth=False)
    cr.restore()
    rivet(cr, -222, -112, 10)


register("ya_clap", (-250, -230, 250, 180), _clap)


def _palm(cr):
    """A big open hand, palm out, fingers up (pivot at the bottom of the wrist): for HAND-SIZED."""
    sk = Y.DH_SKIN
    _shape(cr, [(-110, 10), (-120, -150), (120, -150), (110, 10)], sk, 6, smooth=False, holes=(12, 18, 2.6))
    band(cr, [(-124, -60), (0, -66), (124, -60)], 30, GOLDC, spacing=14)
    palm = [(-170, -140), (-176, -300), (-150, -440), (150, -440), (176, -300), (166, -140)]
    _shape(cr, palm, sk, 6)
    fingers = [(-120, -430, 46, 230, -0.08), (-40, -440, 48, 290, -0.02), (44, -440, 48, 300, 0.02),
               (124, -430, 44, 250, 0.08)]
    for fx, fy, fw, fl, a in fingers:
        cr.save()
        cr.translate(fx, fy)
        cr.rotate(a)
        _shape(cr, [(-fw / 2, 20), (fw / 2, 20), (fw / 2, -fl + fw / 2), (0, -fl), (-fw / 2, -fl + fw / 2)], sk, 5)
        for k in (1, 2):
            ink(cr, [(-fw / 2 + 8, -fl * k / 3), (fw / 2 - 8, -fl * k / 3)], 2.6)
        cr.restore()
    thumb = [(-160, -180), (-250, -280), (-300, -360), (-270, -390), (-210, -330), (-150, -290)]
    _shape(cr, thumb, sk, 5)
    ink(cr, [(-120, -210), (-60, -300), (40, -330)], 3)
    ink(cr, [(-100, -180), (20, -220), (120, -230)], 3)


register("ya_palm", (-320, -760, 200, 20), _palm)


def _haveli(cr):
    """Dhaniram's haveli at night (pivot at the bottom centre): two storeys of sandstone, arched jharokha windows, a
    small dome and chhatris on top; one window cut through (the scene lights it)."""
    st = (0.84, 0.58, 0.32)
    _shape(cr, [(-420, 0), (420, 0), (420, -560), (-420, -560)], st, 6, smooth=False, holes=(14, 22, 2.6))
    band(cr, [(-440, -300), (440, -300)], 22, (0.66, 0.40, 0.18), spacing=14, hole_r=2.4)
    band(cr, [(-440, -560), (440, -560)], 26, (0.66, 0.40, 0.18), spacing=14, hole_r=2.4)
    for row, y0 in enumerate((-60, -340)):
        for k in range(4):
            x = -300 + 200 * k
            cr.new_path()
            cr.move_to(x - 50, y0)
            cr.line_to(x - 50, y0 - 130)
            cr.arc(x, y0 - 130, 50, math.pi, 2 * math.pi)
            cr.line_to(x + 50, y0)
            cr.close_path()
            if row == 1 and k == 1:
                cr.save()
                cr.set_operator(cairo.OPERATOR_CLEAR)
                cr.fill_preserve()
                cr.restore()
                cr.set_source_rgb(*INK)
                cr.set_line_width(6)
                cr.stroke()
            else:
                leather(cr, (0.40, 0.22, 0.10), 5)
    cr.new_path()
    cr.arc(0, -560, 150, math.pi, 2 * math.pi)
    cr.close_path()
    leather(cr, st, 6)
    for sx in (-1, 1):
        x = sx * 340
        _shape(cr, [(x - 60, -560), (x + 60, -560), (x + 50, -640), (x - 50, -640)], st, 5, smooth=False)
        cr.new_path()
        cr.arc(x, -640, 60, math.pi, 2 * math.pi)
        cr.close_path()
        leather(cr, (0.66, 0.40, 0.18), 5)
    poly(cr, [(-8, -700), (0, -760), (8, -700)])
    leather(cr, GOLDC, 3)


register("ya_haveli", (-450, -770, 450, 10), _haveli)
HAVELI_WIN = (-100.0, -470.0)        # the lit window's centre (haveli units)


register("ya_yama_kneel", (-250, -60, 240, 260), lambda cr: K.kneel_legs(cr, RU.YM_SKIN, RU.YM_DHOTI, pc.GOLD, 1.18))


def _monkey_badge(cr):
    """A round leather badge with a little monkey (sitting, hands tied with a rope): LIKE A CAPTURED MONKEY."""
    cr.new_path()
    cr.arc(0, 0, 150, 0, 2 * math.pi)
    leather(cr, (0.97, 0.88, 0.66), 6)
    cr.new_path()
    cr.arc(0, 0, 136, 0, 2 * math.pi)
    cr.set_source_rgb(*INK)
    cr.set_line_width(3)
    cr.stroke()
    fur, face = (0.62, 0.38, 0.18), (0.95, 0.74, 0.55)
    tail = [(40, 70), (110, 60), (130, 0), (110, -40), (100, -20), (112, 10), (96, 44), (40, 54)]
    _shape(cr, tail, fur, 4)
    _shape(cr, [(-60, 100), (60, 100), (56, 20), (30, -40), (-30, -40), (-56, 20)], fur, 5)        # body
    cr.new_path()
    cr.arc(0, -78, 52, 0, 2 * math.pi)                                                              # head
    leather(cr, fur, 5)
    for sx in (-1, 1):
        cr.new_path()
        cr.arc(sx * 52, -82, 18, 0, 2 * math.pi)
        leather(cr, face, 3)
    cr.new_path()
    ell(cr, 0, -66, 36, 32)
    leather(cr, face, 3)
    for sx in (-1, 1):
        cr.new_path()
        cr.arc(sx * 14, -78, 6, 0, 2 * math.pi)
        cr.set_source_rgb(*INK)
        cr.fill()
    ink(cr, [(-12, -50), (0, -56), (12, -50)], 3)                                                 # a sad mouth
    _shape(cr, [(-40, 20), (40, 20), (34, 50), (-34, 50)], face, 4)                                  # hands together
    for k in range(3):
        band(cr, [(-46, 26 + 10 * k), (46, 30 + 10 * k)], 7, GC.ROPE, holes=False, lw=2)
    ink(cr, [(46, 36), (90, 60), (120, 110)], 6, col=GC.ROPE)


register("ya_monkey", (-160, -160, 160, 160), _monkey_badge)


# ------------------------------------------------------------------ sets


HOR = 600.0                          # the horizon of the road sets
VP = (1440.0, HOR + 6)               # the road's vanishing point


def burning_sky(cr, t, a=1.0):
    """A red, burning sky over a dusty plain, a big low sun on the horizon, dark hills."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    g = cairo.LinearGradient(0, 0, 0, HOR + 30)
    g.add_color_stop_rgba(0, 0.28, 0.05, 0.03, a)
    g.add_color_stop_rgba(0.55, 0.62, 0.17, 0.07, a)
    g.add_color_stop_rgba(1, 0.96, 0.52, 0.24, a)
    cr.rectangle(0, 0, W, HOR + 30)
    cr.set_source(g)
    cr.fill()
    g2 = cairo.LinearGradient(0, HOR, 0, H)
    g2.add_color_stop_rgba(0, 0.70, 0.40, 0.20, a)
    g2.add_color_stop_rgba(1, 0.46, 0.24, 0.12, a)
    cr.rectangle(0, HOR + 30, W, H - HOR - 30)
    cr.set_source(g2)
    cr.fill()
    cr.restore()
    glow(cr, 1600, HOR - 60, 560, 0.55 * a)
    prop(cr, "sun", 1600, HOR - 60, 0.62, rot=0.05 * t, alpha=a)
    hills = [(0, HOR + 30), (0, HOR - 10)]
    for i in range(25):
        x = 80 * i
        hills.append((x, HOR - 18 - 26 * abs(math.sin(i * 1.3)) - 14 * math.sin(i * 0.7)))
    hills += [(W, HOR - 10), (W, HOR + 30)]
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    pc.poly(cr, hills)
    cr.set_source_rgba(0.48, 0.20, 0.10, a)
    cr.fill()
    cr.restore()


def road(cr, t, a=1.0):
    """A long empty road from the bottom left to the far horizon on the right, stones along its edges."""
    if a <= 0.01:
        return
    lx0, rx0 = -80.0, 980.0
    cr.save()
    cr.set_operator(cairo.OPERATOR_SCREEN)
    pc.poly(cr, [(lx0, H), (rx0, H), (VP[0] + 14, VP[1]), (VP[0] - 14, VP[1])])
    cr.set_source_rgba(0.42, 0.30, 0.18, 0.55 * a)
    cr.fill()
    cr.restore()
    for edge, x0 in ((0, lx0), (1, rx0)):
        for k in range(26):
            u = (k / 26.0) ** 1.6
            x = x0 + (VP[0] + (14 if edge else -14) - x0) * u
            y = H + (VP[1] - H) * u
            r = 10 * (1 - u) + 2
            cr.new_path()
            pc.ell(cr, x, y, r * 1.6, r)
            cr.set_source_rgba(0.38, 0.20, 0.10, 0.7 * a)
            cr.fill()
    prop(cr, "gp_deadtree", 200, HOR + 120, 0.34, alpha=0.9 * a)
    prop(cr, "gp_deadtree", 1820, HOR + 70, 0.24, alpha=0.8 * a, flip=True)


def road_set(cr, t, a=1.0):
    burning_sky(cr, t, a)
    road(cr, t, a)


def ground(cr, alpha=1.0, y=FLOOR + 6):
    prop(cr, "ground", W / 2, y, 1.42, alpha=alpha)


def night_tint(cr, a, y1=H):
    """A deep blue night over the cloth (the lamp still glows through)."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    g = cairo.LinearGradient(0, 0, 0, y1)
    g.add_color_stop_rgba(0, 0.20, 0.22, 0.42, a)
    g.add_color_stop_rgba(1, 0.50, 0.50, 0.72, a)
    cr.rectangle(0, 0, W, y1)
    cr.set_source(g)
    cr.fill()
    cr.restore()


ROOM_X = 960.0


def room(cr, t, a=1.0, door=None):
    """Dhaniram's room at night: dharmavyadha's back wall (soft), the floor; door = x of the dark doorway."""
    prop(cr, "dv_room", ROOM_X - 380, FLOOR + 6, 0.86, alpha=0.75 * a, blur=4)
    prop(cr, "dv_room", ROOM_X + 700, FLOOR + 6, 0.86, alpha=0.75 * a, blur=4, flip=True)
    if door is not None:
        s = 0.8
        x0, x1 = door - 176 * s, door + 176 * s
        y0, y1 = FLOOR - 930 * s, FLOOR - 20 * s
        cr.save()
        cr.rectangle(x0, y0, x1 - x0, y1 - y0)
        cr.set_source_rgba(0.22, 0.25, 0.42, 0.8 * a)
        cr.fill()
        cr.restore()
        for i, (px, py) in enumerate(((0.3, 0.15), (0.75, 0.3), (0.5, 0.5), (0.2, 0.62))):
            sparkle(cr, x0 + (x1 - x0) * px, y0 + (y1 - y0) * py, 8 + 3 * math.sin(t * 2 + i), 0.7 * a,
                    (0.95, 0.95, 1.0))
        prop(cr, "gp_doorway", door, FLOOR, s, alpha=a)
    ground(cr, alpha=a)


def bed(cr, x, s, alpha=1.0):
    """The rich carved bed; returns the mattress top (y)."""
    prop(cr, "ya_bed", x, FLOOR, s, alpha=alpha)
    return FLOOR - BED_TOP * s


def lying(cr, t, x, top, s, mood="calm", alpha=1.0, front=(0.0, 0.0), sheet=0.0, breath=1.0):
    """Dhaniram lying on his back on a bed whose top is at `top` (hip at x, head to the left); sheet 0..1: a white
    sheet drawn up over him to the chest. Returns his points (device)."""
    hy = top - 84 * s + 2.5 * math.sin(t * 2.0) * breath
    pts = Y.dhani(cr, t, x, s, mood, y=hy, rot=-math.pi / 2, front=front, backa=(0.1, -0.1), rods=False,
                  alpha=alpha, bob=False)
    if sheet > 0.01:
        cr.save()
        a = sheet * alpha
        x0 = x - 210 * s
        pc.poly(cr, [(x0, top + 4), (x + 520 * s, top + 4), (x + 520 * s, hy - 150 * s), (x + 300 * s, hy - 140 * s),
                     (x - 20 * s, hy - 150 * s), (x0, hy - 120 * s)])
        cr.set_source_rgba(0.98, 0.97, 0.93, 0.96 * a)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, a)
        cr.set_line_width(4)
        cr.stroke()
        for k in range(3):
            pc.poly(cr, [(x + (40 + 140 * k) * s, hy - 140 * s), (x + (80 + 140 * k) * s, top)], closed=False)
            cr.set_source_rgba(0.70, 0.66, 0.58, 0.7 * a)
            cr.set_line_width(3)
            cr.stroke()
        cr.restore()
    return pts


# ------------------------------------------------------------------ the cast


def dh(cr, t, x, s=SM, mood="calm", feet=FLOOR, **kw):
    return Y.dhani(cr, t, x, s, mood, feet=feet, **kw)


def bh(cr, t, x, s=SM, mood="calm", feet=FLOOR, **kw):
    return Y.bhola(cr, t, x, s, mood, feet=feet, **kw)


def du(cr, t, x, s=0.6, feet=FLOOR, legs=None, **kw):
    """A Yamaduta (facing left unless flip=False); hold staff | noose | none; legs = walking leg angles."""
    if legs is None:
        return duta(cr, t, x, s, feet=feet, **kw)
    from scenes_ruru import held_grip
    from scenes_mandhata import held
    front, alpha = kw.pop("front", (-0.4, -0.5)), kw.get("alpha", 1.0)
    hold = kw.pop("hold", "staff")
    ex = None
    if hold == "staff":
        ex = {"gp_duta_armF_lo": held_grip("gp_dstaff", front, 0.62, 0.0, 40, alpha, 0.0)}
    elif hold == "noose":
        ex = {"gp_duta_armF_lo": held("gp_noose", front, 0.62, 150, 0.0, alpha, 0.0)}
    kw.setdefault("flip", True)
    return fig(cr, GC.DUTA, "gp_duta", t, x, s, front=front, legs=legs, feet=feet, extra=ex, **kw)


def vishnu(cr, t, x, s, feet=FLOOR, alpha=1.0, blur=0.0, talk=()):
    """Vishnu standing, four-armed: the chakra and the conch raised, his front hand raised as he teaches."""
    ang = man_angles("sg_vishnu", t, (-1.25, -1.05), (0.3, -0.3), 0.0, (0.0, 0.0), [(tt, 0.25) for tt in talk], 0.3)
    ang["sg_vishnu_armF2_up"] = -2.5 + 0.32
    ang["sg_vishnu_armF2_lo"] = -0.4 + 0.55
    ang["sg_vishnu_armB2_up"] = 2.6 - 0.30
    ang["sg_vishnu_armB2_lo"] = 0.5 + 0.25
    pts = puppet(cr, SG.VISHNU, x, feet - 434 * s, s, sway(t, 0.008, 0.5), False, ang, alpha, blur)
    hx, hy = cr.device_to_user(*pts["handF2"])
    prop(cr, "sg_chakra", hx, hy - 95 * s, 0.7 * s, rot=t * 1.2, alpha=alpha)
    bx, by = cr.device_to_user(*pts["handB2"])
    prop(cr, "sg_conch", bx, by - 60 * s, 0.6 * s, alpha=alpha)
    return pts


def garuda(cr, t, x, s, feet=FLOOR, flip=True, alpha=1.0, blur=0.0, head=0.12):
    """Garuda (snake_cast) standing, hands folded, head bowed a little, listening."""
    return fig(cr, SN.GARUDA, "sn_garuda", t, x, s, front=ANJALI["front"], backa=ANJALI["backa"], head=head,
               flip=flip, alpha=alpha, blur=blur, feet=feet, ph=0.8)


def yama(cr, t, x, s, feet=FLOOR, flip=False, front=(-0.5, -0.6), backa=(0.3, -0.3), alpha=1.0, blur=0.0,
         kneel=False, staff=True, hits=(), head=0.0):
    """ruru_cast's Yama standing (or kneeling), his danda in his front hand."""
    from scenes_ruru import held_grip
    ex = {"rr_yama_armF_lo": held_grip("rr_danda", front, 0.68, 0.0, 120.0, alpha, blur)} if staff else None
    return fig(cr, RU.YAMA, "rr_yama", t, x, s, front=front, backa=backa, head=head, flip=flip, alpha=alpha,
               blur=blur, feet=feet, ph=0.6, extra=ex, hits=hits, kneel="ya_yama_kneel" if kneel else None)


# ------------------------------------------------------------------ i1  hook: the lone soul on the road


SOUL1 = (870.0, 1000.0, 650.0)       # x, feet, height
DU1 = ((300.0, 0.66, 1010.0), (560.0, 0.58, 960.0))    # the messengers behind him: x, scale, feet


def soul_walk(t, tP, x0):
    """The soul's x and leg angles: still until tP, then a slow trudge to the right."""
    if t < tP:
        return x0, (0.0, 0.0), 0.0
    x, bob, rock, ph = hop_walk(t, tP, tP + 12.0, x0, x0 + 340, 0.55)
    return x, walk_legs(ph, 0.28), bob


def messengers(cr, t, step, a_sil, a_lit, tD=None):
    """The two Yamadutas behind the soul (facing right): dark silhouettes, stepping out lit (a_lit) by `step`."""
    for k, (x, s, f) in enumerate(DU1):
        xx = x + 110 * step
        hold = "noose" if k == 0 else "staff"
        hits = [(tD + 0.2 + 0.15 * k, 0.4)] if tD is not None else ()
        if a_sil > 0.01:
            sil(cr, lambda c_: du(c_, t, xx, s, feet=f, flip=False, hold=hold, ph=0.4 + k, front=(-0.5, -0.5)),
                0.9 * a_sil)
        if a_lit > 0.01:
            du(cr, t, xx, s, feet=f, flip=False, hold=hold, ph=0.4 + k, front=(-0.5, -0.5), alpha=a_lit, hits=hits)


def s_i1(cr, t, tl, t0, t1):
    c = cues(tl, "i1")
    tQ, tL, tT, tS, tY, tP = c["Q"], c["L"], c["T"], c["S"], c["Y"], c["P"]
    road_set(cr, t)
    rise = prog(t, tL, 0.9)
    if rise > 0.01:
        cr.save()
        cr.translate(0, 60 * (1 - rise))
        messengers(cr, t, 0.0, rise, 0.0)
        cr.restore()
    x0, f, h = SOUL1
    x, legs, bob = soul_walk(t, tP, x0)
    footprints(cr, t, [(x0 - 60 - 90 * k, f - 4 + 2 * k, 1.4 - 0.08 * k) for k in range(4)][::-1], tP + 0.4, 0.5)
    mood = "shocked" if t < tT else "terrified"
    Y.soul(cr, t, x, f + bob * 0.6, h, mood, front=(-0.6, -0.5) if t < tT else (-0.9, -0.9), backa=(0.4, -0.3),
           legs=legs, shiver=0.6 * prog(t, tL, 0.4) * (1 - prog(t, tP, 0.3)))
    tick_end = tY + 1.6

    def ui(cr):
        if t < tT - 0.05:
            a = 1 - prog(t, tT - 0.25, 0.2)
            head(cr, t, "WHAT REALLY HAPPENS", -1.0, "AFTER DEATH?", -1.0, alpha=a)
        else:
            box = head(cr, t, "13 DAYS AFTER DEATH...", tT - 0.05, "A 1-YEAR WALK", tS)
            if box and t > tY:
                bx, by, bw, bh_ = box
                size = bh_
                full = "A 1-YEAR WALK"
                sz = min(118, fit(full, 118, 1460))
                xa = bx + text_size("A ", sz)[0]
                xb = bx + text_size("A 1-YEAR", sz)[0]
                underline(cr, t, xa - 6, xb + 6, by + size + 22, tY)
        counter_badge(cr, t, tT, "DAY 13", 205, 375, 76)
        if t > tY - 0.05:
            counter_badge(cr, t, tY, "1 YEAR", 1690, 360, 84)
            n = int(365 * ease((t - tY) / (tick_end - tY)))
            plate(cr, t, tY + 0.2, f"{max(1, n)} / 365 DAYS", 1690, 460, 34)
    return dict(ui=ui, lift_abs=0.85)


# ------------------------------------------------------------------ i2  no food, no water, no shade; the messengers


ICONS2 = ((1150, 400), (1395, 400), (1640, 400))


def s_i2(cr, t, tl, t0, t1):
    c = cues(tl, "i2")
    tF, tW, tS, tY, tD = c["F"], c["W"], c["S"], c["Y"], c["D"]
    tP = cues(tl, "i1")["P"]
    road_set(cr, t)
    step = prog(t, tD - 0.1, 0.7)
    messengers(cr, t, step, 1 - step, step, tD)
    x0, f, h = SOUL1
    turn = t > tD + 0.15
    if not turn:
        x, legs, bob = soul_walk(t, tP, x0)
    else:
        x, legs, bob = soul_walk(tD + 0.15, tP, x0)
        legs = (0.0, 0.0)
    Y.soul(cr, t, x, f + bob * 0.6, h, "terrified", front=(-2.1, -1.0) if turn else (-0.9, -0.9),
           backa=(-1.9, -1.0) if turn else (0.4, -0.3), legs=legs, flip=turn, shiver=prog(t, tD + 0.15, 0.3))
    fade = 1 - prog(t, tY + 0.2, 0.4)

    def plate_icon(c_, a):
        prop(c_, "dv_plate", 0, 26, 0.44, alpha=a)

    def pot_icon(c_, a):
        Y.pot(c_, 0, 18, 0.62, alpha=a)

    def tree_icon(c_, a):
        prop(c_, "tree", 0, 78, 0.105, alpha=a)

    def ui(cr):
        small = [("NO FOOD", tF, INK), ("·", tW, INK), ("NO WATER", tW, INK), ("·", tS, INK), ("NO SHADE", tS, INK)]
        if t < tY:
            parts_line(cr, t, small, 46, 66)
        else:
            head(cr, t, "AND WALKING WITH HIM:", tY - 0.1, "YAMA'S 2 MESSENGERS", tY + 0.1)
        for (ix, iy), ti, fn in zip(ICONS2, (tF, tW, tS), (plate_icon, pot_icon, tree_icon)):
            medallion(cr, t, ti - 0.05, ix, iy, 92, fn, alpha=fade, cross_t=ti + 0.3)
        if t > tD:
            tag(cr, t, tD + 0.35, "YAMADUTAS", 470, 985, 38)
    return dict(ui=ui, lift_abs=0.85, flash=flash_at(t, tD, 0.2))


# ------------------------------------------------------------------ i3  not a horror film: the Garuda Purana


VI3 = (500.0, 0.56)
GA3 = (1420.0, 0.56)


def s_i3(cr, t, tl, t0, t1):
    c = cues(tl, "i3")
    tF, tN, tG, tV, tK, tD, tB = c["F"], c["N"], c["G"], c["V"], c["K"], c["D"], c["B"]
    ground(cr)
    # A: the clapperboard, crossed out
    aA = 1 - prog(t, tG - 0.25, 0.3)
    if aA > 0.01:
        b, k, a = depth(t, t0 - 0.05, 0.45)
        cx, cy = 960, 600
        clap = keyed(t, [(t0, 0.0), (tF - 0.1, -0.35), (tF + 0.05, 0.0)], 0.12, 1.0)
        glow(cr, cx, cy, 520, 0.3 * aA * a)
        prop(cr, "ya_clap", cx, cy, 1.25 * k, rot=sway(t, 0.01, 0.4) + 0.4 * clap * 0, alpha=aA * a, blur=b)
        draw_text(cr, "HORROR", cx, cy + 10, 88, (0.97, 0.93, 0.85), aA * a, HEAD_FONT, "cm")
        draw_text(cr, "FILM", cx, cy + 108, 70, (0.97, 0.93, 0.85), aA * a, HEAD_FONT, "cm")
        if t > tN:
            big_x(cr, cx, cy, 640, 460, prog(t, tN, 0.3), aA)
    # B: the title card
    tOut = min(max(tV + 0.6, tG + 1.9), tD - 0.6)        # the title card holds ~2 s
    chapter(cr, t, tG - 0.1, tOut, "THE JOURNEY AFTER DEATH", [[("MARNE KE BAAD", INK)], [("KA SAFAR", RED)]],
            SRC)
    # C: Vishnu tells Garuda
    aC = prog(t, tOut - 0.25, 0.5)
    if aC > 0.01:
        b, k, a = depth(t, tOut - 0.25, 0.5)
        vx, vs = VI3
        glow(cr, vx, FLOOR - 380, 520, 0.45 * aC)
        aura(cr, t, vx - 10, FLOOR - 560, 120, 380, 0.18 * aC, n=16, spin=0.04)
        vp = vishnu(cr, t, vx, vs * k, alpha=a, blur=b, talk=(tV + 0.2, tD))
        gx, gs = GA3
        b2, k2, a2 = depth(t, max(tK - 0.2, tOut - 0.05), 0.5)
        garuda(cr, t, gx, gs * k2, alpha=a2, blur=b2, head=0.12 + 0.1 * nods(t, (tD + 0.4, tB + 0.2), 0.5))
        mouth = to_user(cr, vp["head"])
        for tt in (tV + 0.3, tV + 1.5, tD + 0.2):
            rings(cr, t, tt, mouth[0] + 60, mouth[1], 1, 3, 0.25, 300, aC)
        hand = to_user(cr, vp["handF"])
        for i in range(4):                                   # the days, leaf by leaf, to Garuda
            ts = tD + 0.25 * i
            u = ease((t - ts) / 0.6)
            if u <= 0:
                continue
            p0, p2 = (hand[0] + 30, hand[1] - 20), (960 + 24 * (i % 2), 380 + 100 * i)
            p1 = ((p0[0] + p2[0]) / 2, min(p0[1], p2[1]) - 150)
            px, py = bezier(p0, p1, p2, u)
            sc = 0.3 + 0.06 * u
            prop(cr, "lr_pleaf", px, py, sc, rot=0.2 * (1 - u) - 0.03 * (i % 2), alpha=aC)
            draw_text(cr, f"DAY {i + 1}" if i < 3 else "DAY 4...", px, py + 4, 50, INK if i < 3 else RED, aC * u,
                      HEAD_FONT, "cm")
    dev_v = cr.user_to_device(VI3[0], FLOOR + 72)
    dev_g = cr.user_to_device(GA3[0], FLOOR + 72)

    def ui(cr):
        if t < tG - 0.1:
            box = head(cr, t, "THIS IS NOT A", t0 + 0.05, "HORROR FILM", tF)
            strike_at(cr, t, box, tN)
        elif t < tOut - 0.2:
            pass
        else:
            head(cr, t, "VISHNU HIMSELF TOLD GARUDA", tV - 0.1, "DAY BY DAY", tD)
            tag(cr, t, tOut, "VISHNU", dev_v[0], dev_v[1], 38)
            tag(cr, t, tOut + 0.2, "GARUDA", dev_g[0], dev_g[1], 38)
    return dict(ui=ui, lift=0.6)


# ------------------------------------------------------------------ i4 - i7  the two travellers


DX, BX = 400.0, 1520.0               # Dhaniram's and Bhola's places
SAFE5 = (740.0, 0.62)


def travellers(cr, t, tl, lit_d, lit_b, d_kw=None, b_kw=None, walk_t=None):
    """Dhaniram (left, facing right) and Bhola (right, facing left), dark silhouettes until lit (0..1)."""
    d_kw, b_kw = dict(d_kw or {}), dict(b_kw or {})
    xd, xb = DX, BX
    dl, bl = (0.0, 0.0), (0.0, 0.0)
    if walk_t is not None and t < walk_t[1]:
        xd, bob, rock, ph = hop_walk(t, walk_t[0], walk_t[1], DX - 360, DX, 0.36)
        dl = walk_legs(ph)
        xb, bob2, rock2, ph2 = hop_walk(t, walk_t[0] + 0.1, walk_t[1], BX + 360, BX, 0.36)
        bl = walk_legs(ph2)
    d_kw.setdefault("legs", dl)
    b_kw.setdefault("legs", bl)
    out = {}
    if lit_d < 0.99:
        sil(cr, lambda c_: dh(c_, t, xd, rods=True, **d_kw), 0.92 * (1 - lit_d))
    if lit_d > 0.01:
        out["d"] = dh(cr, t, xd, alpha=lit_d, **d_kw)
    if lit_b < 0.99:
        sil(cr, lambda c_: bh(c_, t, xb, flip=True, rods=True, **b_kw), 0.92 * (1 - lit_b))
    if lit_b > 0.01:
        out["b"] = bh(cr, t, xb, flip=True, alpha=lit_b, **b_kw)
    return out


def safe5(cr, t, tA, tK, alpha=1.0):
    """Dhaniram's safe: swings open on its gold at tA, slams shut at tK."""
    sx, ss = SAFE5
    o = keyed(t, [(0.0, 0.0), (tA, 1.0), (tK, 0.0)], 0.3, 1.2) if tA is not None else 0.0
    if o > 0.05:
        glow(cr, sx, FLOOR - 140 * ss * 1.6, 260, 0.8 * o * alpha)
    Y.safe(cr, sx, FLOOR, ss, open_=o, alpha=alpha)
    if tA is not None and tA < t < tK:
        lights(cr, t, sx, FLOOR - 220 * ss, 120, 6, 0.7 * o * alpha, GOLDC, 0.6)
    if tK is not None and 0 < t - tK < 0.4:
        burst(cr, t, sx - 60, FLOOR - 200 * ss, tK, n=8, rmax=180, alpha=0.5 * alpha)


def s_i4(cr, t, tl, t0, t1):
    c = cues(tl, "i4")
    tD, tL = c["D"], c["L"]
    ground(cr)
    travellers(cr, t, tl, 0.0, 0.0, walk_t=(t0, t0 + 0.9))

    def ui(cr):
        head(cr, t, "TODAY WE TAKE THIS JOURNEY WITH", t0 + 0.05, "2 TRAVELLERS", tD)
        big_mark(cr, t, tD + 0.05, "?", DX + 20, 230, 150)
        big_mark(cr, t, tL + 0.1, "?", BX - 10, 260, 150)
    return dict(ui=ui, lift=0.5)


def s_i5(cr, t, tl, t0, t1):
    c = cues(tl, "i5")
    tN, tA, tK = c["N"], c["A"], c["K"]
    ground(cr)
    lit = prog(t, t0 + 0.05, 0.45)
    safe5(cr, t, tA, tK, alpha=lit)
    present = keyed(t, [(t0, 0.0), (tA - 0.1, 1.0), (tK - 0.2, 0.0)], 0.3, 1.3)
    clutch = prog(t, tK - 0.15, 0.25)
    front = mix(mix((-0.32, -0.55), (-1.3, -0.2), present), (-0.05, -1.55), clutch)
    mood = "calm" if t < tN else ("smug" if t < tK else "angry")
    travellers(cr, t, tl, lit, 0.0, d_kw=dict(mood=mood, front=front, hits=[(tA, 0.3)], head=-0.08 * present))

    def ui(cr):
        head(cr, t, "TRAVELLER 1:", t0 + 0.05, "SETH DHANIRAM", tN)
        tag(cr, t, tN + 0.1, "SETH DHANIRAM", DX, 985, 38)
        stamp(cr, t, tA + 0.15, "RICHEST", SAFE5[0] + 20, 430, 66, -0.08)
        stamp(cr, t, tK + 0.15, "STINGIEST", SAFE5[0] + 20, 545, 66, 0.05)
        big_mark(cr, t, -1.0, "?", BX - 10, 260, 150)
    return dict(ui=ui, lift=0.5, flash=flash_at(t, tA, 0.15))


def s_i6(cr, t, tl, t0, t1):
    c = cues(tl, "i6")
    tB, tG, tW = c["B"], c["G"], c["W"]
    tA5, tK5 = cues(tl, "i5")["A"], cues(tl, "i5")["K"]
    ground(cr)
    safe5(cr, t, None, None)
    lit = prog(t, t0 + 0.05, 0.45)
    snub = prog(t, tG - 0.1, 0.4)
    travellers(cr, t, tl, 1.0, lit, d_kw=dict(mood="smug" if t > tG - 0.1 else "angry", front=(-0.05, -1.55),
                                              head=-0.2 * snub, rot=-0.03 * snub),
               b_kw=dict(mood="smile" if t > tB else "calm", hits=[(tB, 0.2)]))

    def ui(cr):
        head(cr, t, "TRAVELLER 2:", t0 + 0.05, "BHOLA", tB)
        tag(cr, t, -1.0, "SETH DHANIRAM", DX, 985, 38)
        tag(cr, t, tB + 0.1, "BHOLA", BX, 985, 38)
        a = 1 - prog(t, t0, 0.3)
        stamp(cr, t, -1.0, "RICHEST", SAFE5[0] + 20, 430, 66, -0.08, alpha=a)
        stamp(cr, t, -1.0, "STINGIEST", SAFE5[0] + 20, 545, 66, 0.05, alpha=a)
        big_mark(cr, t, -1.0, "?", BX - 10, 260, 150, alpha=1 - prog(t, t0, 0.25))
        caption(cr, t, tG, "POOR", BX - 360, 430, 64, RED)
        caption(cr, t, tW, "WATER-SELLER", BX - 360, 535, 58, INK)
    return dict(ui=ui, lift=0.5)


BOOK7 = (960.0, 520.0, 0.62)


def s_i7(cr, t, tl, t0, t1):
    c = cues(tl, "i7")
    tK, tM, tP, tG, tL = c["K"], c["M"], c["P"], c["G"], c["L"]
    ground(cr)
    safe5(cr, t, None, None, alpha=1 - prog(t, tP - 0.3, 0.4))
    travellers(cr, t, tl, 1.0, 1.0, d_kw=dict(mood="smug", front=(-0.05, -1.55), hits=[(tK, 0.2)]),
               b_kw=dict(mood="smile", hits=[(tK + 0.2, 0.2)]))
    bx, by, bs = BOOK7
    leaves = [(tP + 0.6, [("WHAT HAPPENS TO THEM:", 46, MONO_FONT)], 0),
              (tG - 0.1, [([("GARUDA PURANA", RED)], 92, HEAD_FONT)], 0)]
    cen = book(cr, t, bx, by, bs, leaves, t_in=tP - 0.1, t_open=tP + 0.3, ring=(1, 0, 0, tG + 0.2), blank=1)
    from poster import tick
    if t > tL and cen:
        lx, ly = cr.device_to_user(*cen[1]) if len(cen) > 1 else (bx, by)
        tick(cr, lx + 330, ly - 6, 110, prog(t, tL, 0.35))

    def ui(cr):
        if t < tP - 0.1:
            head(cr, t, "DHANIRAM & BHOLA:", t0 + 0.05, "OUR STORY'S TRAVELLERS", tK)
        else:
            head(cr, t, "BUT WHAT HAPPENS TO THEM IS", tP - 0.1, "IN THE GARUDA PURANA", tG)
        tag(cr, t, -1.0, "SETH DHANIRAM", DX, 985, 38)
        tag(cr, t, -1.0, "BHOLA", BX, 985, 38)
        if t < tP + 0.3:
            card_a = 1 - prog(t, tP - 0.1, 0.3)
            caption(cr, t, tK + 0.1, "OUR STORY'S", 960, 470, 56, INK, alpha=card_a)
            caption(cr, t, tM, "TRAVELLERS", 960, 580, 84, RED, alpha=card_a)
    return dict(ui=ui, lift=0.5)


# ------------------------------------------------------------------ i8  the open loop: scared / welcomed


SEAM = 960.0


def panel_clip(cr, side):
    if side < 0:
        cr.rectangle(0, 0, SEAM - 8, H)
    else:
        cr.rectangle(SEAM + 8, 0, W - SEAM - 8, H)
    cr.clip()


def s_i8(cr, t, tl, t0, t1):
    c = cues(tl, "i8")
    tW, tO, tS, tT, tP, tF = c["W"], c["O"], c["S"], c["T"], c["P"], c["F"]
    a0 = prog(t, t0, 0.35)
    aL, aR = prog(t, tO - 0.3, 0.5), prog(t, tT - 0.3, 0.5)
    # left: Dhaniram, then a huge dark Yama towers over him
    cr.save()
    panel_clip(cr, -1)
    tint(cr, (0.62, 0.20, 0.12), 0.15 * a0 + 0.4 * aL)
    ground(cr)
    if aL > 0.01:
        glow(cr, 300, 420, 700, 0.5 * aL)
        tower = ease((t - tO + 0.3) / 0.8)
        cr.save()
        cr.translate(0, 160 * (1 - tower))
        sil(cr, lambda c_: yama(c_, t, 300, 1.05, feet=1150, front=(-2.35, -0.35), hits=[(tS, 0.4)]), 0.95 * aL,
            (0.12, 0.03, 0.03))
        cr.restore()
        aura(cr, t, 300, 300, 160, 560, 0.25 * aL, n=18, spin=0.05, col=(1.0, 0.35, 0.18))
    shake = prog(t, tS - 0.2, 0.3)
    scared = t > tO
    dh(cr, t, 720 + 6 * shake * math.sin(t * 40), 0.46, "terrified" if scared else "smug", flip=True,
       front=(-2.1, -1.0) if scared else (-0.05, -1.55), backa=(-1.9, -1.0) if scared else (0.3, -0.25),
       alpha=a0, rods=False, hits=[(tO, 0.4)])
    cr.restore()
    # right: an empty throne in gold light; then Yama kneels and washes the feet of a seated figure in shadow
    cr.save()
    panel_clip(cr, 1)
    tint(cr, (1.0, 0.86, 0.55), 0.25 * a0)
    ground(cr)
    glow(cr, 1500, 600, 760, (0.3 + 0.35 * aR) * a0)
    aura(cr, t, 1640, 520, 140, 520, 0.28 * aR, n=20, spin=0.03)
    prop(cr, "md_throne", 1660, FLOOR, 0.58, alpha=a0)
    if aR > 0.01:
        sil(cr, lambda c_: Y.bhola_seated(c_, t, 1660, 0.58, flip=True, rods=False), 0.95 * aR)
        feet = (1660 - 230 * 0.58, FLOOR - 14)
        reach_ = reach_arm(1250, FLOOR - 250 * 0.5, 0.5, 26 * 1.18, (feet[0] - 10, feet[1] - 30))
        yp = yama(cr, t, 1250, 0.5, front=reach_,
                  backa=(-1.6, -0.9), alpha=aR, kneel=True, staff=False, head=0.15)
        hb = to_user(cr, yp["handB"])
        mouth = Y.pot(cr, hb[0] + 10, hb[1] - 40, 0.42, rot=1.25, alpha=aR)
        if t > tP:
            Y.water(cr, t, mouth, (feet[0], feet[1] - 30), prog(t, tP, 0.3) * aR, 12, 30)
    cr.restore()
    # the seam
    band(cr, [(SEAM, 150), (SEAM, H + 20)], 18, (0.52, 0.30, 0.14), spacing=16, hole_r=2.6)

    def ui(cr):
        small_line(cr, t, [(w_, tW + 0.08 * k) for k, w_ in enumerate("WATCH TILL THE END...".split())], 46, 58)
        caption(cr, t, tS, "ONE WILL BE SCARED...", 480, 200, 56, RED)
        caption(cr, t, tF, "ONE WILL BE WELCOMED", 1440, 200, 56, RED)
        big_mark(cr, t, tT + 0.2, "?", 1700, 360, 170, alpha=aR)
    return dict(ui=ui, lift=0.8, flash=flash_at(t, tS, 0.2))


# ------------------------------------------------------------------ d1 - d2  Dhaniram's shop


SHOP = (600.0, 0.6)                  # the shop: x, scale
GADDI = FLOOR - SHOP_TOP * 0.6       # the cushion's top
DH1 = (590.0, 0.5)                   # Dhaniram on his gaddi: x, scale
SAFE1 = (380.0, 0.42)                # his safe on the takht
TRAV = (1330.0, 0.56)                # the thirsty traveller: x, scale


def shop_set(cr, t, a=1.0, heat=1.0):
    prop(cr, "ya_shop", SHOP[0], FLOOR, SHOP[1], alpha=a)
    ground(cr, alpha=a)
    if heat > 0.01:                                      # the blazing sun, heat shimmer
        glow(cr, 1740, 330, 420, 0.6 * heat * a)
        prop(cr, "sun", 1740, 330, 0.38, rot=0.06 * t, alpha=heat * a)
        cr.save()
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        for k in range(4):
            x = 1180 + 150 * k
            pts = [(x + 10 * math.sin(t * 3 + i * 0.9 + k), 760 - 50 * i) for i in range(6)]
            cr.new_path()
            pc.spath(cr, pts, closed=False)
            cr.set_source_rgba(1.0, 0.85, 0.55, 0.35 * heat * a)
            cr.set_line_width(5)
            cr.stroke()
        cr.restore()


def traveller(cr, t, x, mood="tired", flip=True, **kw):
    """The thirsty traveller (dharmavyadha's tired working man, no hoe)."""
    return hus(cr, t, x, TRAV[1], mood=mood, feet=FLOOR, hoe=False, flip=flip, **kw)


def s_d1(cr, t, tl, t0, t1):
    c = cues(tl, "d1")
    tDu, tG, tP, tM, tK, tF, tA = c["Du"], c["G"], c["P"], c["M"], c["K"], c["F"], c["A"]
    out_t = card_out(t0, t1)
    shop_set(cr, t, heat=prog(t, tG, 0.5))
    Y.safe(cr, SAFE1[0], GADDI, SAFE1[1])
    x, s = DH1
    point = keyed(t, [(t0, 0.0), (tK - 0.1, 1.0), (tA + 0.9, 0.3)], 0.25, 1.6)
    mood = "smug" if t < tK - 0.1 else ("angry" if t < tA + 0.8 else "smug")
    dp = dh(cr, t, x, s, mood, feet=GADDI, sit=True, front=mix((-0.9, -0.9), (-2.6, -0.25), point),
            hand="point" if point > 0.5 else "open", hits=[(tK, 0.3), (tF, 0.2), (tA, 0.3)])
    # the thirsty man comes up, asks, and trudges away
    tx = TRAV[0]
    if t < tA + 0.5:
        xx, bob, rock, ph = hop_walk(t, max(tP - 1.2, out_t - 0.3), tP + 0.2, W + 240, tx, 0.45)
        ask = keyed(t, [(t0, 0.0), (tM - 0.1, 1.0), (tK + 0.3, 0.4)], 0.3, 1.2)
        tp = traveller(cr, t, xx, front=mix((-0.32, -0.55), (-1.3, -0.5), ask),
                       backa=mix((0.3, -0.25), (-1.2, -0.6), ask), legs=walk_legs(ph), rot=rock, head=0.1 * ask)
    else:
        xx, bob, rock, ph = hop_walk(t, tA + 0.5, tA + 2.6, tx, W + 260, 0.5)
        tp = traveller(cr, t, xx, flip=False, legs=walk_legs(ph), rot=rock, head=0.18, front=(-0.1, -0.3))
    dh_head, tr_head = dp["head"], tp["head"]

    def ui(cr):
        if t > out_t:
            if t < tK - 0.1:
                head(cr, t, "IN THE HEAT, A THIRSTY MAN", out_t, "ASKED FOR WATER", max(tM, out_t + 0.2))
            else:
                head(cr, t, "DHANIRAM SAID:", tK - 0.1, "NO FREE WATER!", tF)
            say(cr, t, tM - 0.05, 1560, 400, [("PAANI...?", 62, INK, tM + 0.1)],
                tail=(tr_head[0] + 30, tr_head[1] - 40),
                t_out=tK + 0.3)
            if t < tA:
                say(cr, t, tK - 0.1, 980, 380, [("PAANI MUFT", 64, RED, tK + 0.05), ("NAHI AATA!", 64, RED, tF)],
                    tail=(dh_head[0] + 50, dh_head[1] - 40))
            else:
                say(cr, t, tA - 0.05, 980, 380, [("AAGE BADHO!", 70, RED, tA)], tail=(dh_head[0] + 50, dh_head[1] - 40),
                    t_out=tA + 2.4)
        chapter(cr, t, t0 - 0.05, out_t, "PART 1", [[("DHANIRAM & BHOLA:", INK)], [("THE LAST NIGHT", RED)]],
                "OUR STORY · " + SRC)
    return dict(ui=ui, lift=0.4)


def s_d2(cr, t, tl, t0, t1):
    c = cues(tl, "d2")
    tT, tS, tZ, tR, tN = c["T"], c["S"], c["Z"], c["R"], c["N"]
    shop_set(cr, t, heat=1.0 - prog(t, t0, 0.6) * 0.6)
    o = keyed(t, [(t0, 0.0), (tT, 1.0)], 0.35, 1.2)
    if o > 0.05:
        glow(cr, SAFE1[0], GADDI - 110, 300, 0.9 * o)
    Y.safe(cr, SAFE1[0], GADDI, SAFE1[1], open_=o)
    if o > 0.3:
        lights(cr, t, SAFE1[0], GADDI - 100, 90, 6, 0.8 * o, GOLDC, 0.6)
    x, s = DH1
    count = (t > tS) * (0.5 + 0.5 * math.sin((t - tS) * 9))
    turn = t > tT - 0.25
    dp = dh(cr, t, x, s, "smug", feet=GADDI, sit=True, flip=turn,
            front=(-1.3, -0.6 - 0.5 * count) if turn else (-0.9, -0.9), hits=[(tT, 0.3), (tS, 0.2)])
    if turn and t > tS:                                  # coins hop from the safe to his hand
        hand = to_user(cr, dp["handF"])
        for k in range(3):
            u = ((t - tS) * 1.6 + k / 3) % 1.0
            p0, p2 = (SAFE1[0] + 20, GADDI - 90), (hand[0], hand[1] - 10)
            px, py = bezier(p0, ((p0[0] + p2[0]) / 2, min(p0[1], p2[1]) - 90), p2, u)
            prop(cr, "yy_coin", px, py, 0.5, rot=u * 6, alpha=math.sin(math.pi * u))

    def roti_icon(c_, a):
        prop(c_, "ya_roti", 0, 0, 0.95, alpha=a)

    def ui(cr):
        if t < tZ - 0.1:
            head(cr, t, "HIS SAFE WAS", t0 + 0.05, "FULL OF GOLD", tS)
        else:
            head(cr, t, "BUT IN HIS WHOLE LIFE...", tZ - 0.1, "NOT ONE FREE ROTI", tR)
        medallion(cr, t, tR - 0.05, 1440, 470, 100, roti_icon, cross_t=tN)
        plate(cr, t, tR + 0.45, "FREE ROTIS GIVEN", 1440, 640, 36)
        counter_badge(cr, t, tR + 0.6, "0", 1440, 735, 96)
    return dict(ui=ui, lift=0.4, flash=flash_at(t, tT, 0.2))


# ------------------------------------------------------------------ d3  Bhola in the lane


BH3 = 700.0
BOWL3 = (850.0, FLOOR + 2)


def lane_set(cr, t, a=1.0, warm=0.0):
    prop(cr, "dv_house", 330, FLOOR + 6, 0.62, alpha=0.8 * a, blur=4)
    prop(cr, "lr_hut", 1620, FLOOR + 6, 0.62, alpha=0.8 * a, blur=4)
    ground(cr, alpha=a)


def s_d3(cr, t, tl, t0, t1):
    c = cues(tl, "d3")
    tB, tS, tP, tPa, tF, tD = c["B"], c["S"], c["P"], c["Pa"], c["F"], c["D"]
    lane_set(cr, t)
    glow(cr, 1500, 300, 380, 0.5)
    prop(cr, "dv_bowl", BOWL3[0], BOWL3[1], 0.55)
    # Bhola walks in, then pours
    x, bob, rock, ph = hop_walk(t, t0, tB + 0.7, 260, BH3, 0.42)
    pour = prog(t, tF - 0.45, 0.4)
    if pour < 0.5:
        bh(cr, t, x, mood="smile" if t > tS else "calm", legs=walk_legs(ph), rot=rock, hits=[(tB + 0.6, 0.2)])
    else:
        fr = (-1.5, -0.35)
        bp = bh(cr, t, x, mood="smile", pot=False, hand="hold", front=fr, backa=(-1.25, -0.6))
        hand = to_user(cr, bp["handF"])
        mouth = Y.pot(cr, hand[0] + 30, hand[1] - 20, 0.6, rot=1.15 + 0.2 * prog(t, tF, 0.4))
    # a coin drops into his bowl
    if t > tS:
        u = ease((t - tS) / 0.7)
        p0, p2 = (W + 40, 520), (BOWL3[0], BOWL3[1] - 30)
        px, py = bezier(p0, (1300, 300), p2, u)
        if u < 1:
            prop(cr, "yy_coin", px, py, 0.7, rot=u * 9)
        else:
            sparkle(cr, p2[0], p2[1] - 10, 40 * (1 - prog(t, tS + 0.7, 0.4)) + 2, 1 - prog(t, tS + 1.1, 0.3))
    # the same thirsty traveller comes, with empty hands
    tr = None
    if t > tP - 1.0:
        xx, bob2, rock2, ph2 = hop_walk(t, tP - 1.0, tP + 0.3, W + 240, 1190, 0.45)
        show = keyed(t, [(t0, 0.0), (tPa - 0.1, 1.0), (tF - 0.4, 2.0)], 0.3, 1.3)
        fr = mix((-0.32, -0.55), (-1.5, 0.1), min(1.0, show))
        if show > 1:
            fr = mix((-1.5, 0.1), (-1.25, -0.75), show - 1)
        tr = traveller(cr, t, xx, mood="smile" if t > tD + 0.3 else "tired", front=fr,
                       backa=mix((0.3, -0.25), (-1.2, -0.7), min(1.0, show)), legs=walk_legs(ph2), rot=rock2,
                       head=0.12 * min(1.0, show))
    if pour >= 0.5 and tr is not None:
        cup = to_user(cr, tr["handF"])
        Y.water(cr, t, mouth, (cup[0] - 6, cup[1] - 20), prog(t, tF, 0.25), 13, 40)
    dev_tr = cr.user_to_device(1190, 330)

    def ui(cr):
        if t < tP - 0.2:
            head(cr, t, "AND BHOLA?", t0 + 0.05, "HE SOLD WATER ALL DAY", tS)
        else:
            head(cr, t, "BUT IF SOMEONE COULDN'T PAY...", tP - 0.2, "FREE WATER", tF)
        if t > tPa:
            caption(cr, t, tPa + 0.15, "NO MONEY", dev_tr[0], dev_tr[1] + 40, 44, INK, t_out=tF + 0.4)
        stamp(cr, t, tF + 0.35, "FREE!", 960, 335, 80, -0.1)
    return dict(ui=ui, lift=0.4)


# ------------------------------------------------------------------ d4  the cow, the mother


COW4 = (1320.0, 0.55)
MO4 = (800.0, 0.68)                  # the mother on her cot: x, scale
BHK4 = (1150.0, 0.68)                # Bhola kneeling at her feet


def s_d4(cr, t, tl, t0, t1):
    c = cues(tl, "d4")
    tS, tR, tA, tG, tE, tM, tP = c["S"], c["R"], c["A"], c["G"], c["E"], c["M"], c["P"]
    eve = prog(t, tE - 0.35, 0.5)
    morn = 1 - eve
    if morn > 0.01:                                      # sunrise in the lane: half his roti to the cow
        tint(cr, (1.0, 0.82, 0.55), 0.25 * morn)
        glow(cr, 260, 470, 420, 0.6 * morn)
        prop(cr, "sun", 260, 470, 0.4, alpha=morn)
        lane_set(cr, t, morn)
        cx, cs = COW4
        munch = (t > tG + 0.4) * 0.04 * math.sin((t - tG) * 10)
        prop(cr, "gp_cow", cx, FLOOR, cs, rot=munch, alpha=morn, flip=True)
        give = keyed(t, [(t0, 0.0), (tR - 0.1, 1.0), (tG - 0.2, 2.0)], 0.3, 1.2)
        fr = mix((-0.32, -0.55), (-1.1, -0.9), min(1.0, give))
        if give > 1:
            fr = mix((-1.1, -0.9), (-1.45, -0.15), give - 1)
        bp = bh(cr, t, 720, mood="smile", pot=False, hand="hold", bhand="hold", front=fr,
                backa=(-1.0, -1.0) if t > tA else (0.3, -0.25), alpha=morn, hits=[(tA, 0.25)])
        hf, hb = to_user(cr, bp["handF"]), to_user(cr, bp["handB"])
        if tR < t < tA:
            prop(cr, "ya_roti", hf[0] + 14, hf[1] - 26, 0.62, alpha=morn * prog(t, tR, 0.2))
        elif t >= tA:
            prop(cr, "ya_roti_half", hb[0] + 8, hb[1] - 28, 0.62, rot=0.3, alpha=morn)
            if t < tG + 0.5:
                prop(cr, "ya_roti_half", hf[0] + 18, hf[1] - 26, 0.62, rot=math.pi + 0.2, alpha=morn)
            if 0 < t - tA < 0.4:
                sparkle(cr, hf[0], hf[1] - 30, 40, morn)
    if eve > 0.01:                                       # dusk at his hut: his mother's feet
        tint(cr, (0.80, 0.55, 0.62), 0.35 * eve)
        prop(cr, "lr_hut", 380, FLOOR + 6, 0.62, alpha=eve, blur=2)
        ground(cr, alpha=eve)
        diya(cr, t, 620, FLOOR + 10, 0.8, alpha=eve)
        mx, ms = MO4
        prop(cr, "dv_charpai", mx + 40, FLOOR, ms, alpha=eve)
        kmo(cr, t, mx, FLOOR - 4, ms, smile=t > tP, alpha=eve, rods=False)
        feet = (mx + 200 * ms, FLOOR - 150 * ms)
        kx, ks = BHK4
        press = 4 * math.sin((t - tP) * 7) if t > tP else 0.0
        fr = reach_arm(kx, FLOOR - Y.KNEEL_H * ks, ks, 26 * Y.BH_B, (feet[0], feet[1] + press), True)
        Y.bhola_kneel(cr, t, kx, ks, "smile", ground=FLOOR, flip=True, front=fr, backa=(fr[0] + 0.15, fr[1] - 0.1),
                      alpha=eve, rods=False)
    dev_mo = cr.user_to_device(MO4[0], FLOOR - 560 * MO4[1])

    def ui(cr):
        if t < tG - 0.1:
            head(cr, t, "EVERY MORNING,", t0 + 0.05, "HALF HIS ROTI", tA)
        elif t < tE - 0.2:
            head(cr, t, "EVERY MORNING, HALF HIS ROTI", tG - 0.1, "TO THE STREET COW", tG)
        else:
            head(cr, t, "AND EVERY EVENING,", tE - 0.1, "HIS MOTHER'S FEET", tP)
            tag(cr, t, tM + 0.1, "HIS OLD MOTHER", dev_mo[0], 985, 36)
    return dict(ui=ui, lift=0.5, night=0.12 * eve)


# ------------------------------------------------------------------ d5  one night, two lamps go out


HAV5 = (500.0, 0.62)
HUT5 = (1440.0, 0.6)


def s_d5(cr, t, tl, t0, t1):
    c = cues(tl, "d5")
    tR, tD, tP = c["R"], c["D"], c["P"]
    night_tint(cr, 0.5)
    stars(cr, t, 0.8, ((300, 420), (760, 360), (1180, 330), (1610, 400), (1840, 300), (120, 300)))
    glow(cr, 960, 350, 260, 0.4)
    prop(cr, "moon", 960, 350, 0.55)
    hx, hs = HAV5
    out = 1 - prog(t, tP, 0.35)
    wx, wy = hx + HAVELI_WIN[0] * hs, FLOOR + HAVELI_WIN[1] * hs
    glow(cr, wx, wy, 160, 0.7 * out)
    prop(cr, "ya_haveli", hx, FLOOR + 6, hs)
    ux, us = HUT5
    glow(cr, ux, FLOOR - 140, 200, 0.45 * out)
    prop(cr, "lr_hut", ux, FLOOR + 6, us)
    ground(cr)
    lx = hx + 330
    prop(cr, "av_lamp", lx, FLOOR, 0.9)
    fx, fy = lx + 70 * 0.9, FLOOR - 236 * 0.9
    if out > 0.01:
        glow(cr, fx, fy - 30, 220, 0.6 * out)
        prop(cr, f"flame{int(t * 10) % 3}", fx, fy + 4, 0.2 * (0.4 + 0.6 * out), alpha=out)
    smoke(cr, t, tP + 0.1, fx, fy - 10)
    dx_ = ux - 260
    diya(cr, t, dx_, FLOOR + 10, 0.85, lit=out)
    smoke(cr, t, tP + 0.15, dx_ + GC.DIYA_WICK[0] * 0.85, FLOOR + 10 + GC.DIYA_WICK[1] * 0.85 - 10)

    def ui(cr):
        head(cr, t, "THEN, ONE NIGHT...", t0 + 0.05, "BOTH LIVES ENDED", tP)
        tag(cr, t, tD - 0.1, "DHANIRAM", hx, 985, 36)
        tag(cr, t, tD + 0.1, "BHOLA", ux, 985, 36)
    return dict(ui=ui, lift=1.0, night=0.18 + 0.12 * (1 - out))


# ------------------------------------------------------------------ d6  the last moment


BED6 = (600.0, 0.78)
DHL6 = (640.0, 0.5)                  # lying Dhaniram: hip x, scale
VIS6 = (1340.0, 470.0, 250.0)        # the vision: centre, ring radius
WORLDS = (("sun", 0.3), ("moon", 0.42), ("kb_world", 0.3), ("star", 1.1), ("md_world", 0.17), ("cloud", 0.3),
          ("star", 0.9), ("sun", 0.2))


def s_d6(cr, t, tl, t0, t1):
    c = cues(tl, "d6")
    tA, tS, tE, tB = c["A"], c["S"], c["E"], c["B"]
    room(cr, t)
    bx, bs = BED6
    top = bed(cr, bx, bs)
    diya(cr, t, 1000, FLOOR + 10, 0.8)
    x, s = DHL6
    mood = "calm" if t < tS else ("shocked" if t < tB else "talking")
    lp = lying(cr, t, x, top, s, mood, front=(-0.6, -0.4) if t > tB else (0.0, 0.0))
    vx, vy, vr = VIS6
    merge = ease((t - tE) / 0.8)
    if t > tS - 0.1:
        glow(cr, vx, vy, 420 + 200 * merge, 0.4 + 0.4 * merge)
        if merge > 0.01:                                 # one bright circle that holds them all
            cr.save()
            cr.set_operator(cairo.OPERATOR_ADD)
            cr.arc(vx, vy, 175 * merge, 0, 2 * math.pi)
            cr.set_source_rgba(0.55, 0.42, 0.22, 0.6 * merge)
            cr.fill()
            cr.restore()
        for i, (name, sc) in enumerate(WORLDS):
            ti = tS + 0.12 * i
            q = back(clamp((t - ti) / 0.35), 1.6)
            if q <= 0.01:
                continue
            ang = 2 * math.pi * i / len(WORLDS) + 0.25 * t + 2 * merge
            r = vr * (1 - 0.6 * merge)
            px, py = vx + r * math.cos(ang), vy + (0.62 + 0.38 * merge) * r * math.sin(ang)
            k = q * (1 - 0.45 * merge)
            if k > 0.02:
                prop(cr, name, px, py, sc * k, rot=0.1 * t, alpha=clamp(q))
        if merge > 0.01:
            red_ring(cr, vx, vy, 190, 190, prog(t, tE + 0.2, 0.5), 8)
            if t - tE < 0.6:
                burst(cr, t, vx, vy, tE + 0.3, n=16, rmax=380, alpha=0.6)
        dotted(cr, [to_user(cr, lp["head"]), (vx - 200, vy + 80)], prog(t, tS, 0.6), 26, 5, GOLDC, 0.8)
    mouth = lp["head"]

    def ui(cr):
        if t < tE - 0.1:
            head(cr, t, "THE GARUDA PURANA SAYS:", t0 + 0.05, "AT THE LAST MOMENT...", tA)
        elif t < tB - 0.1:
            head(cr, t, "HE SEES ALL THE WORLDS", tE - 0.1, "AS ONE", tE + 0.2)
        else:
            head(cr, t, "AND HE CAN'T", tB - 0.1, "SAY A WORD", tB + 0.1)
        if t > tB:
            say(cr, t, tB, mouth[0] + 200, mouth[1] - 200, [("...", 100, INK, tB + 0.05)], tail=(mouth[0] + 40,
                                                                                            mouth[1] - 30))
            big_x(cr, mouth[0] + 200, mouth[1] - 200, 210, 150, prog(t, tB + 0.6, 0.3))
        plate(cr, t, tA, "GARUDA PURANA I.26", 1650, 985, 28)
    return dict(ui=ui, lift=1.0, night=0.32)


# ------------------------------------------------------------------ d7  the messengers arrive


DOOR7 = 1560.0
BED7 = (560.0, 0.78)
DU7 = ((1560.0, 0.6), (1290.0, 0.62))     # in the doorway (noose), stepping in (staff)


def s_d7(cr, t, tl, t0, t1):
    c = cues(tl, "d7")
    tD, tC, tH, tN, tS = c["D"], c["C"], c["H"], c["N"], c["S"]
    room(cr, t, door=DOOR7)
    bx, bs = BED7
    top = bed(cr, bx, bs)
    diya(cr, t, 900, FLOOR + 10, 0.8, lit=1 - 0.4 * prog(t, tD, 0.6))
    lying(cr, t, 600, top, 0.5, "terrified" if t > tD + 0.3 else "shocked")
    pts = []
    for k, (x, s) in enumerate(DU7):
        b, kk, a = depth(t, tD - 0.2 + 0.25 * k, 0.7)
        if a <= 0.01:
            pts.append(None)
            continue
        step = ease((t - tD - 0.1) / 1.2) if k == 1 else 0.0
        xx = x + (DOOR7 - x) * (1 - step) if k == 1 else x
        glow(cr, xx, FLOOR - 500, 300, 0.2 * a)
        p = du(cr, t, xx, s * kk, hold="noose" if k == 0 else "staff", front=(-0.5, -0.6), alpha=a, blur=b,
               ph=0.3 + k, hits=[(tN, 0.3)] if k == 0 else [(tS, 0.3)])
        pts.append(p)
    if t > tC - 0.2:                                     # a crow across the night
        u = (t - tC + 0.2) / 1.6
        if u < 1:
            prop(cr, "sg_crow_fly", W + 200 - (W + 600) * u, 360 + 40 * math.sin(u * 7), 0.42,
                 rot=0.05 * math.sin(u * 20))
    dev = [p for p in pts]

    def ui(cr):
        head(cr, t, "THEN, IN HIS ROOM, CAME", t0 + 0.05, "TWO MESSENGERS", tD)
        cx_, cy_ = 900, 330                              # one caption at a time, the feature ringed
        caption(cr, t, tC + 0.1, "BLACK AS CROWS", cx_, cy_, 52, INK, t_out=tH - 0.1)
        if dev[1] is not None and tH < t < tN:
            hx, hy = dev[1]["top"]
            red_ring(cr, hx - 10, hy + 70, 110, 90, prog(t, tH, 0.4), 8)
            caption(cr, t, tH + 0.05, "HAIR ON END", cx_, cy_, 52, RED, t_out=tN - 0.1)
        if dev[0] is not None and tN < t < tS:
            nx, ny = dev[0]["handF"]
            red_ring(cr, nx - 10, ny + 120, 70, 150, prog(t, tN, 0.4), 8)
            caption(cr, t, tN + 0.05, "A NOOSE", cx_, cy_, 52, RED, t_out=tS - 0.1)
        if dev[1] is not None and t > tS:
            sx_, sy_ = dev[1]["handF"]
            red_ring(cr, sx_ - 4, sy_ - 220, 50, 140, prog(t, tS, 0.4), 8)
            caption(cr, t, tS + 0.05, "AND A STAFF", cx_, cy_, 52, RED)
    return dict(ui=ui, lift=1.0, night=0.36, flash=flash_at(t, tD, 0.25))


# ------------------------------------------------------------------ d8  the thumb-sized soul is pulled out


BED8 = (700.0, 0.95)
DHL8 = (760.0, 0.62)
DU8 = (1600.0, 0.62)
SOUL8 = (1060.0, 600.0, 210.0)       # where the soul ends up: x, feet, height


def soul_out(t, tP, tO, chest):
    """The soul's (x, feet, h, seen) as it is drawn up out of the chest between tP and tO."""
    rise = ease((t - tP + 0.15) / max(0.9, tO - tP + 0.45))
    sx_, sf_, sh_ = SOUL8
    x = chest[0] + (sx_ - chest[0]) * rise
    f = chest[1] + 40 + (sf_ - chest[1] - 40) * rise - 80 * math.sin(math.pi * rise)
    h = 50 + (sh_ - 50) * rise
    return x, f, h, rise


def s_d8(cr, t, tl, t0, t1):
    c = cues(tl, "d8")
    tA, tP, tO, tT = c["A"], c["P"], c["O"], c["T"]
    room(cr, t)
    bx, bs = BED8
    top = bed(cr, bx, bs)
    x, s = DHL8
    lp = lying(cr, t, x, top, s, "shut", breath=1 - prog(t, tP, 0.5))
    chest = to_user(cr, lp["chest"])
    seen = prog(t, tA - 0.2, 0.5)
    glow(cr, chest[0], chest[1] - 20, 200, 0.6 * seen)
    sx, sf, sh, rise = soul_out(t, tP, tO, chest)
    dx_, ds = DU8
    hy = FLOOR - 434 * ds
    pull = keyed(t, [(t0, 0.0), (tP - 0.1, 1.0)], 0.35, 1.2)
    from scenes_dharmavyadha import point_to
    aim = point_to(dx_, hy, ds, (sx, sf - 0.55 * sh), flip=True, bulk=1.12)
    dp = du(cr, t, dx_, ds, hold="none", front=mix((-0.4, -0.5), (aim[0] + 0.2, -0.25), pull), backa=(0.2, -0.6),
            ph=0.6, hits=[(tP, 0.3)])
    hand = to_user(cr, dp["handF"])
    if t > tP - 0.3:
        la = prog(t, tP - 0.3, 0.4)
        wx, wy = sx, sf - 0.45 * sh
        light_rope(cr, [hand, ((hand[0] + wx) / 2, min(hand[1], wy) - 60), (wx + 0.18 * sh, wy)], la)
        noose_loop(cr, t, wx, wy, 0.22 * sh + 6, 0.07 * sh + 4, la)
    if seen > 0.01 and t > tA - 0.2:
        Y.soul(cr, t, sx, sf, sh * seen, "terrified" if rise > 0.5 else "shut", alpha=seen,
               front=(-0.9, -0.9) if rise > 0.5 else (-0.32, -0.55))
    # the thumb beside it: the same size
    th = prog(t, tT - 0.1, 0.4)
    if th > 0.01:
        sx_, sf_, sh_ = SOUL8
        ts = sh_ / (GC.THUMB_TIP - GC.THUMB_BASE)
        wx, wy = 1330, sf_ + GC.THUMB_BASE * ts
        glow(cr, wx - 30, sf_ - sh_ / 2, 260, 0.4 * th)
        prop(cr, "gp_thumb", wx, wy + 60 * (1 - th), ts, alpha=th)
        if t > tT + 0.3:
            for yy in (sf_ - sh_, sf_):
                dotted(cr, [(sx_ - 60, yy), (wx - 0.14 * 800 * ts + 30, yy)], prog(t, tT + 0.3, 0.5), 20, 4.5,
                       RED, 0.9)

    def ui(cr):
        if t < tT - 0.1:
            head(cr, t, "THEY PULLED OUT", t0 + 0.05, "HIS SOUL", tP)
        else:
            box = head(cr, t, "AND IT WAS", tT - 0.1, "THUMB-SIZED", tT)
            if box:
                underline(cr, t, box[0], box[0] + box[2], box[1] + box[3] + 22, tT + 0.5)
    return dict(ui=ui, lift=1.0, night=0.3, flash=flash_at(t, tP, 0.2))


# ------------------------------------------------------------------ d9 - d11  the little soul, the noose, the bribe


BED9 = (1420.0, 0.75)
SOUL9 = (600.0, 915.0, 420.0)


def s_d9(cr, t, tl, t0, t1):
    c = cues(tl, "d9")
    tC, tH, tS, tL = c["C"], c["H"], c["S"], c["L"]
    room(cr, t)
    bx, bs = BED9
    top = bed(cr, bx, bs)
    lp = lying(cr, t, bx + 30, top, 0.48, "shut", breath=0.0)
    x, f, h = SOUL9
    cry = prog(t, tC - 0.1, 0.3) * (1 - prog(t, tS - 0.1, 0.3))
    mood = "crying" if cry > 0.5 else ("shocked" if t > tS else "terrified")
    fr = mix((-0.9, -0.9), (-2.75, -1.85), cry)
    ba = mix((0.3, -0.3), (-2.65, -1.95), cry)
    sp = Y.soul(cr, t, x, f - 10 * math.sin(t * 1.6), h, mood, front=fr, backa=ba, hits=[(tH, 0.3)],
                shiver=0.5 * cry, head=-0.1 * cry)
    if t > tL - 0.2 and sp:
        eye = to_user(cr, sp["head"])
        dotted(cr, [(eye[0] + 30, eye[1]), to_user(cr, lp["chest"])], prog(t, tL - 0.2, 0.6), 26, 5, GOLDC, 0.8)
    dev_body = cr.user_to_device(bx, top - 230)

    def ui(cr):
        if t < tS - 0.1:
            head(cr, t, "LITTLE DHANIRAM CRIED:", t0 + 0.05, "HAAY HAAY!", tH)
            hd = sp["head"] if sp else (700, 520)
            say(cr, t, tH - 0.1, 1060, 430, [("HAAY!", 84, RED, tH), ("HAAY!", 84, RED, tH + 0.3)],
                tail=(hd[0] + 60, hd[1] - 20))
            deva(cr, t, tH + 0.5, "हाय, हाय!", 1060, 660, 64, RED)
        else:
            head(cr, t, "AND HE STARED AT", tS - 0.1, "HIS OWN BODY", tL)
            tag(cr, t, tS + 0.1, "HIS OWN BODY", dev_body[0], dev_body[1], 38)
    return dict(ui=ui, lift=1.0, night=0.28)


SOUL10 = (760.0, 915.0, 380.0)
DU10 = ((1480.0, 0.62), (240.0, 0.6))     # the noose man (facing left), the staff man (facing right)


def noose_scene(cr, t, tN, tug=0.0, look=0.0, soul_kw=None, du_hits=()):
    """The little soul between the two messengers, a loop of light round his neck from tN; tug pulls him to the
    right; look turns the messengers' heads to each other. Returns (soul points, noose man's points, staff man's)."""
    x, f, h = SOUL10
    x += 60 * tug
    sx, ss = DU10[1]
    pb = du(cr, t, sx, ss, flip=False, hold="staff", front=(-0.45, -0.5), head=0.12 * look, ph=0.2)
    nx, ns = DU10[0]
    pn = du(cr, t, nx, ns, hold="none", front=(-1.1 - 0.15 * tug, -0.35), backa=(0.25, -0.4), head=0.12 * look,
            ph=0.7, hits=du_hits)
    kw = dict(soul_kw or {})
    sp = Y.soul(cr, t, x, f - 8 * math.sin(t * 1.5), h, **kw)
    if t > tN - 0.3 and sp:
        la = prog(t, tN - 0.3, 0.4)
        hand = to_user(cr, pn["handF"])
        drop = ease((t - tN + 0.3) / 0.5)
        neck = (x + 0.02 * h, f - 0.66 * h - 200 * (1 - drop))
        light_rope(cr, [hand, ((hand[0] + neck[0]) / 2, neck[1] + 30 - 40 * tug), (neck[0] + 0.12 * h, neck[1])],
                   la, 0.9)
        noose_loop(cr, t, neck[0], neck[1], 0.13 * h, 0.05 * h, la)
    return sp, pn, pb


def s_d10(cr, t, tl, t0, t1):
    c = cues(tl, "d10")
    tN, tB, tC = c["N"], c["B"], c["C"]
    room(cr, t)
    tug = keyed(t, [(t0, 0.0), (tC + 0.1, 1.0)], 0.2, 2.0)
    sp, pn, pb = noose_scene(cr, t, tN, tug, soul_kw=dict(mood="terrified", front=(-1.0, -0.8),
                                                          shiver=prog(t, tN, 0.3)), du_hits=[(tB, 0.3), (tC, 0.5)])
    mouth = pn["head"]

    def ui(cr):
        if t < tB - 0.1:
            head(cr, t, "THE MESSENGERS PUT", t0 + 0.05, "A NOOSE ON HIM", tN)
        else:
            head(cr, t, "AND THE MESSENGERS SAID:", tB - 0.1, "CHAL! JALDI CHAL!", tC)
        say(cr, t, tB - 0.1, mouth[0] - 360, max(450, mouth[1] + 40), [("CHAL!", 96, RED, tB),
                                                                        ("JALDI CHAL!", 64, RED, tC)],
            tail=(mouth[0] - 30, mouth[1] - 10))
    return dict(ui=ui, lift=1.0, night=0.28, flash=flash_at(t, tC, 0.15))


def s_d11(cr, t, tl, t0, t1):
    c = cues(tl, "d11")
    tJ, tB, tL, tP, tN = c["J"], c["B"], c["L"], c["P"], c["N"]
    room(cr, t)
    pat = (tJ < t < tB) * abs(math.sin((t - tJ) * 9))
    rub = prog(t, tL - 0.1, 0.25) * (1 - prog(t, tP, 0.25))
    look = prog(t, tP - 0.2, 0.3) * (1 - prog(t, tN + 0.8, 0.3))
    if t < tB:
        fr = (-0.15 - 0.15 * pat, -1.55)
    else:
        fr = mix((-0.15, -1.55), (-1.25, -1.35), rub)
    if t > tN:
        fr = (-0.15, -1.6)
    mood = "sheepish" if t < tN else "shocked"
    sp, pn, pb = noose_scene(cr, t, -10.0, 1.0, look, soul_kw=dict(mood=mood, front=fr, backa=(0.3, -0.25),
                                                                     hand="fist" if rub > 0.5 else "open",
                                                                     head=0.15 * (t > tN)))
    if rub > 0.3 and sp:
        hp = to_user(cr, sp["handF"])
        for k in range(3):
            sparkle(cr, hp[0] + 20 * math.sin(t * 8 + k * 2), hp[1] - 30 - 18 * k, 12, rub, GOLDC)
    pocket = sp["pocket"] if sp else None

    def ui(cr):
        if t < tN - 0.1:
            head(cr, t, "THE OLD TRICK:", tJ - 0.1, "A BRIBE?", tL)
            hd = sp["head"] if sp else (760, 560)
            say(cr, t, tB - 0.1, 470, 420, [("BHAI SAHAB...", 56, INK, tB), ("KUCH LE-DEKAR?", 56, RED, tL)],
                tail=(hd[0] - 40, hd[1] - 30), t_out=tN - 0.1)
        else:
            head(cr, t, "BUT NOW...", tN - 0.1, "NO POCKET!", tN + 0.1)
        if pocket and t > tN:
            red_ring(cr, pocket[0], pocket[1], 70, 60, prog(t, tN, 0.4), 9)
            stamp(cr, t, tN + 0.3, "NO POCKET!", pocket[0] - 300, pocket[1] - 140, 64, -0.08)
    return dict(ui=ui, lift=1.0, night=0.28)


# ------------------------------------------------------------------ d12  before Yama and back home


YM12 = (1450.0, 0.62)
DU12 = (300.0, 0.6)
SOUL12 = (760.0, 840.0, 160.0)
HOUSE12 = (1150.0, 0.6)


def s_d12(cr, t, tl, t0, t1):
    c = cues(tl, "d12")
    tD, tS, tH, tA, tG = c["D"], c["S"], c["H"], c["A"], c["G"]
    aB = prog(t, tA + 0.15, 0.6)
    aA = 1 - aB
    door = (HOUSE12[0] + DV.DOOR_X * HOUSE12[1], FLOOR - 40)
    arrive = ease((t - t0) / 0.9)
    if aA > 0.01:
        prop(cr, "sb_yhall", 960, FLOOR + 8, 0.8, alpha=0.6 * aA, blur=5)
        ground(cr, alpha=aA)
        yx, ys = YM12
        glow(cr, yx, FLOOR - 400, 520, 0.4 * aA)
        aura(cr, t, yx - 20, FLOOR - 600, 120, 420, 0.22 * aA, n=16, spin=0.03, col=(0.95, 0.45, 0.25))
        order = keyed(t, [(t0, 0.0), (tH - 0.1, 1.0)], 0.3, 1.4)
        yp = yama_seated(cr, t, yx, FLOOR, ys, front=mix((-0.55, -0.85), (-2.2, -0.3), order),
                         nod=nods(t, (tS,), 0.6), alpha=aA, hits=[(tH, 0.4)])
        dx_, ds = DU12
        dxx = dx_ - 700 * (1 - arrive)
        dp = du(cr, t, dxx, ds, flip=False, hold="none", front=(-1.25, -0.2), alpha=aA, ph=0.4)
        hand = to_user(cr, dp["handF"])
        if t < tA:
            sx_, sf_, sh_ = SOUL12
            sxx = sx_ - 700 * (1 - arrive)
            wx, wy = sxx, sf_ - 0.45 * sh_
            fade = aA * (1 - prog(t, tH, 0.4))
            light_rope(cr, [hand, ((hand[0] + wx) / 2, wy + 30), (wx - 0.15 * sh_, wy)], fade)
            noose_loop(cr, t, wx, wy, 0.2 * sh_ + 6, 0.07 * sh_ + 4, fade)
            if arrive < 1:
                for k in range(5):
                    yy = sf_ - sh_ * (0.2 + 0.15 * k)
                    cr.set_source_rgba(1.0, 0.9, 0.6, 0.6 * (1 - arrive))
                    cr.set_line_width(4)
                    cr.move_to(sxx - 80 - 260 * (1 - arrive), yy)
                    cr.line_to(sxx - 80, yy)
                    cr.stroke()
        if t > tH:
            burst(cr, t, yx - 150, FLOOR - 560, tH, n=14, rmax=420, alpha=0.6 * aA)
        dev_y = yp["top"]
    else:
        dev_y = None
    if aB > 0.01:
        night_tint(cr, 0.5 * aB)
        stars(cr, t, 0.8 * aB, ((300, 420), (760, 360), (1610, 400), (1840, 300), (120, 300)))
        hx, hs = HOUSE12
        prop(cr, "dv_house", hx, FLOOR + 6, hs, alpha=aB)
        ground(cr, alpha=aB)
        glow(cr, door[0], door[1] - 200, 260, 0.5 * aB)
    sx_, sf_, sh_ = SOUL12
    p0, p1, p2 = (sx_, sf_), (420, 260), (door[0], door[1])
    dur = max(1.3, tG - tA + 0.7)
    u = ease((t - tA + 0.1) / dur) if t > tA - 0.1 else 0.0
    if u > 0:
        dotted(cr, [bezier(p0, p1, p2, i / 60) for i in range(61)], u, 30, 6.5, (1.0, 0.86, 0.5), 0.9)
    if t < tA - 0.1:
        px, py = sx_ - 700 * (1 - arrive), sf_
    else:
        px, py = bezier(p0, p1, p2, u)
    hgt = sh_ * (1 - 0.2 * math.sin(math.pi * u))
    Y.soul(cr, t, px, py, hgt, "terrified" if u < 0.98 else "crying",
           front=(-2.2, -0.4) if 0 < u < 0.98 else (-0.9, -0.9), backa=(-2.0, -0.4) if 0 < u < 0.98 else (0.3, -0.3),
           rot=-0.4 * math.sin(math.pi * u))
    if 0.98 < u and t < tA + dur + 0.6:
        burst(cr, t, p2[0], p2[1] - 80, tA - 0.1 + dur, n=10, rmax=260, alpha=0.5)

    def ui(cr):
        if t < tH - 0.1:
            head(cr, t, "IN A SHORT TIME, THEY TOOK HIM", t0 + 0.05, "BEFORE YAMA", tS)
        else:
            head(cr, t, "BY YAMA'S ORDER, THROUGH THE AIR,", tH - 0.1, "BACK HOME", tG)
        if dev_y is not None:
            tag(cr, t, tS + 0.1, "YAMA", dev_y[0] - 30, dev_y[1] - 120, 40, alpha=aA)
    return dict(ui=ui, lift=1.0, night=0.1 + 0.25 * aB, flash=flash_at(t, tS, 0.2) + flash_at(t, tH, 0.2))


# ------------------------------------------------------------------ d13  the weeping family; the noose pulls him back


BED13 = (800.0, 0.85)
DOOR13 = 1640.0
DU13 = (1640.0, 0.58)


def s_d13(cr, t, tl, t0, t1):
    c = cues(tl, "d13")
    tR, tG, tF, tP = c["R"], c["G"], c["F"], c["P"]
    room(cr, t, door=DOOR13)
    bx, bs = BED13
    top = bed(cr, bx, bs)
    from scenes_dharmavyadha import wife
    wife(cr, t, 250, 0.56, eyes="calm", feet=FLOOR, front=(-0.62, -2.55), backa=(-0.5, -2.35), ph=0.3,
         hits=[(tR + 0.4, 0.2)])
    lp = lying(cr, t, bx + 40, top, 0.5, "shut", sheet=1.0, breath=0.0)
    fig(cr, GC.SON, "gp_son", t, 1270, 0.56, front=(-0.62, -2.55), backa=(-0.5, -2.35), feet=FLOOR,
        kneel="gp_son_kneel", flip=True, ph=0.7, head=0.1)
    dp = du(cr, t, DU13[0], DU13[1], hold="none", front=(-1.2, -0.3), backa=(0.25, -0.4), ph=0.5,
            hits=[(tP, 0.5)])
    hand = to_user(cr, dp["handF"])
    body = to_user(cr, lp["chest"])
    hover = (bx + 40, top - 260)
    dy, dx = 0.0, 0.0
    hits = []
    for td in (tG + 0.05, tG + 1.0):
        u = (t - td) / 0.8
        if 0 < u < 1:
            dy = (body[1] - 40 - hover[1]) * math.sin(math.pi * min(1.0, u / 0.5)) * (u < 0.5) + \
                 (body[1] - 40 - hover[1]) * (1 - (u - 0.5) / 0.2) * (0.5 <= u < 0.7)
        hits.append(td + 0.4)
    pullb = keyed(t, [(t0, 0.0), (tP, 1.0)], 0.3, 1.6)
    dx = 160 * pullb
    sx, sf = hover[0] + dx, hover[1] + max(0.0, dy) - 60 * pullb + 6 * math.sin(t * 1.7)
    Y.soul(cr, t, sx, sf, 140, "crying" if t < tG else "terrified", front=(-1.2, -0.6) if dy > 10 else (-0.9, -0.9),
           rot=0.2 * pullb)
    for th in hits:
        ripple(cr, t, th, body[0], body[1] - 30)
    la = 1.0
    wx, wy = sx, sf - 0.45 * 140
    light_rope(cr, [hand, ((hand[0] + wx) / 2, min(hand[1], wy) - 40 + 60 * (1 - pullb)), (wx + 20, wy)], la, 0.9)
    noose_loop(cr, t, wx, wy, 0.2 * 140 + 6, 0.07 * 140 + 4, la)

    def ui(cr):
        if t < tG - 0.1:
            head(cr, t, "AT HOME, EVERYONE", t0 + 0.05, "WAS CRYING", tR)
        elif t < tF - 0.1:
            head(cr, t, "HE TRIED TO", tG - 0.1, "GET BACK IN", tG + 0.2)
        else:
            head(cr, t, "BUT THE NOOSE", tF - 0.1, "PULLED HIM BACK", tP)
    return dict(ui=ui, lift=1.0, night=0.3,
                flash=sum(flash_at(t, th, 0.12) for th in hits) + flash_at(t, tP, 0.15))


# ------------------------------------------------------------------ p1  no body: how will he walk?


GHOST_C = (0.42, 0.26, 0.12)


def ghost(cr, t, x, s, a=1.0, feet=FLOOR, **kw):
    """The body still to come: Dhaniram's shape as a faint brown shadow."""
    if a <= 0.01:
        return None
    return sil(cr, lambda c_: dh(c_, t, x, s, "calm", feet=feet, rods=False, **kw), 0.3 * a, GHOST_C)


def s_p1(cr, t, tl, t0, t1):
    c = cues(tl, "p1")
    tS, tN, tA, tK = c["S"], c["N"], c["A"], c["K"]
    out_t = card_out(t0, t1)
    road_set(cr, t, 0.55)
    gx, gs = 1120.0, 0.56
    ga = prog(t, out_t - 0.2, 0.5)
    ghost(cr, t, gx, gs, ga)
    Y.soul(cr, t, 720, 700 + 10 * math.sin(t * 1.6), 210, "sheepish" if t < tK else "terrified",
           alpha=prog(t, out_t - 0.3, 0.4), front=(-0.9, -0.9))
    dev_g = cr.user_to_device(gx + 20, FLOOR - 300)

    def ui(cr):
        if t > out_t:
            if t < tK - 0.1:
                head(cr, t, "NOW HE HAD", out_t, "NO BODY...", out_t + 0.15)
                red_ring(cr, dev_g[0], dev_g[1], 230, 360, prog(t, out_t + 0.3, 0.5), 9)
            else:
                head(cr, t, "SO FOR THE JOURNEY AHEAD,", tK - 0.15, "HOW WILL HE WALK?", tK)
                big_mark(cr, t, tK + 0.15, "?", 1560, 430, 190)
        chapter(cr, t, t0 - 0.05, out_t, "PART 2", [[("10 DAYS,", INK)], [("10 RICE-BALLS", RED)]],
                SRC + " I.47-55")
    return dict(ui=ui, lift_abs=0.7, night=0.1)


# ------------------------------------------------------------------ p2  the son offers rice-balls


SON2 = (330.0, 0.62)
LEAF2 = (650.0, FLOOR - 2, 0.72)
LAMP2 = (900.0, 0.9)
BODY2 = (1460.0, 0.5)


def s_p2(cr, t, tl, t0, t1):
    c = cues(tl, "p2")
    tD, tB, tP, tC, tH, tN, tHi = c["D"], c["B"], c["P"], c["C"], c["H"], c["N"], c["Hi"]
    ground(cr)
    tint(cr, (1.0, 0.80, 0.60), 0.2)
    lx, ls = LAMP2
    diya(cr, t, lx, FLOOR + 18, ls)
    vx, vy, vs = LEAF2
    prop(cr, "gp_leaf", vx, vy, vs)
    sx_, ss = SON2
    hy = FLOOR - 250 * ss
    spot = (vx - 30, vy - 32)
    reach = reach_arm(sx_, hy, ss, 26 * 0.95, (spot[0], spot[1] - 20))
    give = keyed(t, [(t0, 0.0), (tP - 0.55, 1.0), (tP + 0.5, 0.0)], 0.4, 1.2)
    b, k, a = depth(t, t0, 0.5)
    sp = fig(cr, GC.SON, "gp_son", t, sx_, ss * k, front=mix(ANJALI["front"], reach, give),
             backa=mix(ANJALI["backa"], (-0.2, -0.6), give), head=0.12 + 0.08 * give, feet=FLOOR,
             kneel="gp_son_kneel", ph=0.5, hits=[(tB, 0.3)], alpha=a, blur=b)
    hand = to_user(cr, sp["handF"])
    if t < tP:
        if t > tB:
            pinda(cr, hand[0] + 8, hand[1] - 10, 0.66, alpha=prog(t, tB, 0.3))
    else:
        q = back(clamp((t - tP) / 0.3), 1.5)
        pinda(cr, spot[0], spot[1] - 6 * (1 - q), 0.66)
        glow(cr, spot[0], spot[1] - 20, 170, 0.5 * prog(t, tP, 0.3))
    bxx, bs = BODY2
    ba = prog(t, tH - 0.2, 0.6)
    if ba > 0.01:
        glow(cr, bxx, FLOOR - 300, 420, 0.35 * ba)
        ghost(cr, t, bxx, bs, ba, flip=True)
        Y.soul(cr, t, bxx - 10, FLOOR - 0.6 * Y.DH_H * bs + 110, 100, "sheepish", alpha=ba, flip=True, glow=0.8)
        if t > tH:
            flow(cr, t, tH, tH + 1.6, (spot[0], spot[1] - 30), (bxx, FLOOR - 0.5 * Y.DH_H * bs), n=12, lift=240,
                 dur=0.8)
    dev_son = sp["top"]

    def ui(cr):
        if t < tH - 0.15:
            head(cr, t, "FOR 10 DAYS, HIS SON OFFERS", t0 + 0.05, "RICE-BALLS", tP)
        else:
            head(cr, t, "AND EACH ONE BUILDS", tH - 0.15, "A NEW BODY PART", tN)
        counter_badge(cr, t, tD, "10 DAYS", 1190, 330, 74)
        tag(cr, t, tB + 0.15, "HIS SON", dev_son[0], 985, 36)
        wq = back(clamp((t - tP - 0.1) / 0.35), 1.4)
        if wq > 0.01:                                    # the word card: पिंड = PINDA, A RICE-BALL
            a_ = clamp(wq) * (1 - prog(t, tH - 0.2, 0.3))
            if a_ > 0.01:
                cx, cy = 690, 410
                cr.save()
                cr.translate(cx, cy + 40 * (1 - wq))
                cr.scale(0.62, 0.62)
                pc.paint_part(cr, "plaque", a_)
                cr.restore()
                deva(cr, t, tP + 0.1, "पिंड", cx, cy - 22, 96, RED, a_)
                if not HAS_INDIC:
                    draw_text(cr, "PINDA", cx, cy - 22, 70, RED, a_, anchor="cm")
                draw_text(cr, "PINDA = A RICE-BALL", cx, cy + 46, 30, INK, a_, MONO_FONT, "cm", 2)
    return dict(ui=ui, lift=0.4, night=0.08, flash=flash_at(t, tP, 0.2))


# ------------------------------------------------------------------ p3 - p5  the new body, day by day


BODYX, BODYS = 1150.0, 0.6
ROW = (520.0, FLOOR - 30, 1.15)
PART_NAMES = ("HEAD", "NECK & SHOULDERS", "HEART", "BACK", "NAVEL", "HIPS", "THIGHS", "KNEES", "FEET")
PART_CUT = (-286.0, -226.0, -170.0, -112.0, -40.0, 60.0, 196.0, 300.0, 445.0)   # local y the body has formed down to
PART_TAG_Y = (-460.0, -260.0, -200.0, -140.0, -80.0, 10.0, 130.0, 250.0, 380.0)  # where its DAY tag points
HEART_AT = (36.0, -205.0)


def days(tl):
    """[(day time, part time)] for days 1-10 (cached)."""
    cache = getattr(tl, "_ya_days", None)
    if cache is None:
        c3, c4, c5 = cues(tl, "p3"), cues(tl, "p4"), cues(tl, "p5")
        cache = [(c3["D1"], c3["H1"]), (c3["D2"], c3["H2"]), (c3["D3"], c3["H3"]), (c4["D4"], c4["H4"]),
                 (c4["D5"], c4["H5"]), (c4["H6"] - 0.15, c4["H6"]), (c4["H7"] - 0.15, c4["H7"]),
                 (c4["H8"] - 0.15, c4["H8"]), (c4["H9"] - 0.15, c4["H9"]), (c5["D"], c5["D"])]
        tl._ya_days = cache
    return cache


def heart_path(cr, cx, cy, r):
    pts = []
    for i in range(40):
        q = 2 * math.pi * i / 40
        hx = 16 * math.sin(q) ** 3
        hy = -(13 * math.cos(q) - 5 * math.cos(2 * q) - 2 * math.cos(3 * q) - math.cos(4 * q))
        pts.append((cx + r * hx / 16, cy + r * hy / 16))
    pc.poly(cr, pts)


def body_build(cr, t, tl, mood="calm", front=(-0.32, -0.55), hand="open", glow_all=0.0):
    """The ghost of the new body and the part formed so far (a band growing down from the head), the leaf of rice-
    balls, the DAY counter. Returns (n days done, the current day index, the puppet points)."""
    ds = days(tl)
    n_day = sum(1 for d, _ in ds if t >= d)
    hip = FLOOR - Y.DH_FEET * BODYS
    cut = -640.0
    forming = None
    for i, (_, tp) in enumerate(ds[:9]):
        u = ease((t - tp + 0.1) / 0.55)
        if u <= 0:
            break
        prev = PART_CUT[i - 1] if i else -640.0
        cut = prev + (PART_CUT[i] - prev) * u
        if u < 1:
            forming = (i, u)
    ghost(cr, t, BODYX, BODYS, 1.0, bob=False)
    glow(cr, BODYX, hip - 100 * BODYS, 520, 0.25 + 0.5 * glow_all)
    pts = {}
    if cut > -639:
        cr.save()
        cr.rectangle(0, 0, W, hip + cut * BODYS)
        cr.clip()
        pts = dh(cr, t, BODYX, BODYS, mood, front=front, hand=hand, rods=False, bob=False)
        cr.restore()
        if t >= ds[2][1]:                                # the heart glows in the chest
            q = prog(t, ds[2][1], 0.4) * (1 - 0.5 * prog(t, ds[3][1], 0.4))
            cr.save()
            hx_, hy_ = BODYX + HEART_AT[0] * BODYS, hip + HEART_AT[1] * BODYS
            glow(cr, hx_, hy_, 120, 0.6 * q)
            heart_path(cr, hx_, hy_, 70 * BODYS * (1 + 0.06 * math.sin(t * 6)))
            cr.set_source_rgba(0.92, 0.22, 0.16, 0.85 * q)
            cr.fill_preserve()
            cr.set_source_rgba(0.45, 0.06, 0.04, q)
            cr.set_line_width(3)
            cr.stroke()
            cr.restore()
        if forming:
            i, u = forming
            y = hip + cut * BODYS
            glow(cr, BODYX, y, 300, 0.9 * math.sin(math.pi * u))
            sparkle(cr, BODYX + 40, y, 60 * math.sin(math.pi * u) + 6, 1.0, (1.0, 0.95, 0.75))
    if t < ds[8][1] + 0.4:                               # the little soul of light, inside, until the body is whole
        a = 1 - prog(t, ds[8][1], 0.4)
        Y.soul(cr, t, BODYX + 10, hip - 130 * BODYS, 90, "sheepish", alpha=a, glow=0.9)
    rx, ry, rs = ROW
    nb = 0.0
    for d, _ in ds:
        nb += clamp((t - d) / 0.4)
    from scenes_garuda_purana import rice_row
    rice_row(cr, t, rx, ry, rs, nb, gap=66.0, ball=0.62)
    return n_day, pts


def day_ui(cr, t, tl, part_i=None):
    ds = days(tl)
    n_day = sum(1 for d, _ in ds if t >= d)
    if n_day:
        counter_badge(cr, t, ds[n_day - 1][0], f"DAY {n_day}", ROW[0], 430, 104)
    hip = FLOOR - Y.DH_FEET * BODYS
    for i, (d, tp) in enumerate(ds[:9]):
        if t < tp:
            break
        live = i == min(8, n_day - 1) or (i == 8 and t < ds[9][0])
        if not live:
            continue
        y = hip + PART_TAG_Y[i] * BODYS
        x0 = BODYX + 190
        dotted(cr, [(x0 + 90, y), (BODYX + 60, y)], prog(t, tp, 0.3), 16, 4, RED, 0.9)
        plate(cr, t, tp, f"DAY {i + 1}: {PART_NAMES[i]}", x0 + 240, y, 34, RED)


def s_p3(cr, t, tl, t0, t1):
    ground(cr)
    tint(cr, (1.0, 0.82, 0.62), 0.15)
    body_build(cr, t, tl)
    ds = days(tl)
    c = cues(tl, "p3")

    def ui(cr):
        i = max(0, min(2, sum(1 for d, _ in ds[:3] if t >= d) - 1))
        d, tp = ds[i]
        head(cr, t, f"DAY {i + 1}:", d - 0.05, PART_NAMES[i], tp)
        day_ui(cr, t, tl)
    return dict(ui=ui, lift=0.4, night=0.06)


def s_p4(cr, t, tl, t0, t1):
    ground(cr)
    tint(cr, (1.0, 0.82, 0.62), 0.15)
    body_build(cr, t, tl)
    ds = days(tl)

    def ui(cr):
        i = max(3, min(8, sum(1 for d, _ in ds[:9] if t >= d) - 1))
        d, tp = ds[i]
        head(cr, t, f"DAY {i + 1}:", d - 0.05, PART_NAMES[i], tp)
        day_ui(cr, t, tl)
    return dict(ui=ui, lift=0.4, night=0.06)


def s_p5(cr, t, tl, t0, t1):
    c = cues(tl, "p5")
    tD, tHu, tTh = c["D"], c["Hu"], c["Th"]
    ground(cr)
    tint(cr, (1.0, 0.82, 0.62), 0.15)
    belly = keyed(t, [(t0, 0.0), (tHu - 0.1, 1.0), (tTh - 0.1, 2.0)], 0.3, 1.3)
    fr = mix((-0.32, -0.55), (-0.15, -1.6), min(1.0, belly))
    if belly > 1:
        fr = mix((-0.15, -1.6), (-0.55, -2.45), belly - 1)
    mood = "calm" if t < tHu else ("sheepish" if t < tTh else "talking")
    n, pts = body_build(cr, t, tl, mood, front=fr, glow_all=prog(t, tD, 0.5) * (1 - 0.6 * prog(t, tD + 1, 0.6)))
    if t > tD and 0 < t - tD < 0.8:
        burst(cr, t, BODYX, FLOOR - 330, tD, n=14, rmax=420, alpha=0.6)
    hip = FLOOR - Y.DH_FEET * BODYS
    if tHu < t < tTh + 0.2:                              # the belly rumbles
        bx, by = BODYX + 130 * BODYS, hip - 90 * BODYS
        for k in range(3):
            ph = (t * 3 + k * 0.33) % 1.0
            cr.save()
            cr.set_source_rgba(*RED, 0.8 * (1 - ph))
            cr.set_line_width(5)
            cr.arc(bx + 20, by, 30 + 50 * ph, -0.6, 0.6)
            cr.stroke()
            cr.restore()
    dev_b = cr.user_to_device(BODYX + 300, hip - 90 * BODYS)
    dev_t = cr.user_to_device(BODYX + 300, hip - 330 * BODYS)

    def ui(cr):
        head(cr, t, "DAY 10:", tD - 0.05, None, 0.0)
        parts_line(cr, t, [("HUNGER", tHu, RED), ("&", tTh, RED), ("THIRST", tTh + 0.1, RED)], 116, 118)
        counter_badge(cr, t, tD, "DAY 10", ROW[0], 430, 104)
        caption(cr, t, tHu + 0.1, "HUNGER", dev_b[0] + 80, dev_b[1], 48, RED)
        caption(cr, t, tTh + 0.1, "THIRST", dev_t[0] + 80, dev_t[1], 48, RED)
    return dict(ui=ui, lift=0.4, night=0.06)


# ------------------------------------------------------------------ p6 - p7  four portions: commission!


PIE = (760.0, 560.0, 150.0)          # the big rice-ball: centre, radius
DHP = (1520.0, 915.0, 500.0)         # little Dhaniram (his hand-sized body), feet and height
DUP = (360.0, 0.6)                   # the messenger who takes his share (facing right)
QUART = (("BODY", -0.75), ("BODY", -0.25), ("DHANIRAM", 0.25), ("YAMADUTAS", 0.75))   # label, mid-angle (x pi)


def wedge(cr, cx, cy, r, a0, a1, alpha=1.0, lit=0.0):
    """A quarter of a rice-ball: white rice, an ink edge, a few grains."""
    if alpha <= 0.01 or r < 2:
        return
    if lit > 0.01:
        glow(cr, cx + 0.4 * r * math.cos((a0 + a1) / 2), cy + 0.4 * r * math.sin((a0 + a1) / 2), 2.2 * r, 0.6 * lit)
    cr.save()
    cr.move_to(cx, cy)
    cr.arc(cx, cy, r, a0, a1)
    cr.close_path()
    cr.set_source_rgba(0.99, 0.97, 0.90, 0.97 * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, alpha)
    cr.set_line_width(5)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()
    rng = random.Random(int(a0 * 100))
    for _ in range(6):
        aa = rng.uniform(a0 + 0.15, a1 - 0.15)
        rr = rng.uniform(0.3, 0.85) * r
        x, y = cx + rr * math.cos(aa), cy + rr * math.sin(aa)
        cr.move_to(x - 0.05 * r, y - 0.02 * r)
        cr.line_to(x + 0.05 * r, y + 0.02 * r)
    cr.set_source_rgba(0.78, 0.74, 0.62, alpha)
    cr.set_line_width(3)
    cr.stroke()
    cr.restore()


def rice_ball(cr, cx, cy, r, alpha=1.0):
    """A whole rice-ball, drawn like its portions (white rice, an ink edge, grains, a pale highlight)."""
    cr.save()
    cr.arc(cx, cy, r, 0, 2 * math.pi)
    cr.set_source_rgba(0.99, 0.97, 0.90, 0.97 * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, alpha)
    cr.set_line_width(5)
    cr.stroke()
    pc.ell(cr, cx - 0.35 * r, cy - 0.35 * r, 0.3 * r, 0.18 * r, -0.6)
    cr.set_source_rgba(1, 1, 1, 0.9 * alpha)
    cr.fill()
    rng = random.Random(7)
    for _ in range(16):
        aa, rr = rng.uniform(0, 2 * math.pi), rng.uniform(0.2, 0.85) * r
        x, y = cx + rr * math.cos(aa), cy + rr * math.sin(aa)
        cr.move_to(x - 0.05 * r, y - 0.02 * r)
        cr.line_to(x + 0.05 * r, y + 0.02 * r)
    cr.set_source_rgba(0.78, 0.74, 0.62, alpha)
    cr.set_line_width(3)
    cr.stroke()
    cr.restore()


def pie_scene(cr, t, tl, line):
    """The big rice-ball cut in four: two portions for the body, one for Dhaniram (he eats it), one for the
    messengers (taken). Returns (Dhaniram's points, the messenger's points, the label anchors)."""
    c6 = cues(tl, "p6")
    tC, tB, tE, tQ, tY = c6["C"], c6["B"], c6["E"], c6["Q"], c6["Y"]
    tC7 = cues(tl, "p7")["C"]
    cx, cy, r = PIE
    prop(cr, "gp_leaf", cx, cy + r + 40, 0.95)
    split = ease((t - tC) / 0.5)
    # the messenger at the left, reaching for his share
    grab = keyed(t, [(0.0, 0.0), (tY - 0.15, 1.0), (tY + 0.6, 2.0)], 0.3, 1.2)
    dx_, ds = DUP
    hy = FLOOR - 434 * ds
    tgt = (cx - 0.9 * r, cy + 0.8 * r)
    reachf = reach_arm(dx_, hy, ds, 26 * 1.12, tgt, False)
    fr = mix((-0.4, -0.5), reachf, min(1.0, grab))
    if grab > 1:
        fr = mix(reachf, (-2.3, -1.6), grab - 1)
    dp = du(cr, t, dx_, ds, flip=False, hold="none", front=fr, backa=(0.25, -0.4), ph=0.5, head=-0.1 * (grab > 1.5))
    hand = to_user(cr, dp["handF"])
    # little Dhaniram (his hand-sized body) at the right
    x, f, h = DHP
    eat = keyed(t, [(0.0, 0.0), (tE - 0.1, 1.0), (tE + 1.0, 0.0)], 0.3, 1.2)
    angry = t > tC7 - 0.6 if line == "p7" else False
    mood = "smug" if t < tY - 0.1 else ("shocked" if not angry else "angry")
    sp = Y.soul(cr, t, x, f, h, mood, flip=True, solid=1.0, glow=0.5,
                front=(-2.6, -0.25) if angry else mix((-0.32, -0.55), (-1.3, -1.3), eat),
                hand="point" if angry else "open", hits=[(tY, 0.3)] if t > tY else ())
    mouth = to_user(cr, sp["head"]) if sp else (x, f - h * 0.8)
    anchors = []
    for i, (lab, mid) in enumerate(QUART):
        a0, a1 = (mid - 0.25) * math.pi, (mid + 0.25) * math.pi
        off = 34 * split
        qx, qy = cx + off * math.cos(mid * math.pi), cy + off * math.sin(mid * math.pi)
        rr, al, lit = r, 1.0, 0.0
        if i < 2 and t > tB:
            lit = prog(t, tB + 0.1 * i, 0.4)
        if i == 2 and t > tE - 0.1:                     # flies to Dhaniram and is eaten
            u = ease((t - tE + 0.1) / 0.7)
            qx, qy = qx + (mouth[0] - 40 - qx) * u, qy + (mouth[1] + 30 - qy) * u - 120 * math.sin(math.pi * u)
            rr = r * (1 - 0.75 * u) * (1 - prog(t, tE + 0.7, 0.6))
            al = 1 - prog(t, tE + 1.2, 0.3)
        if i == 3 and t > tY - 0.15:                     # taken by the messenger
            u = ease((t - tY + 0.15) / 0.5)
            qx, qy = qx + (hand[0] + 10 - qx) * u, qy + (hand[1] - 10 - qy) * u
            rr = r * (1 - 0.55 * u)
            if line == "p7":
                rr *= 1 - 0.5 * prog(t, tC7, 1.2)
        if split <= 0.01:
            continue
        wedge(cr, qx - cx + cx, qy, rr, a0, a1, al, lit)
        anchors.append((lab, cr.user_to_device(qx + 1.3 * r * math.cos(mid * math.pi),
                                               qy + 1.15 * r * math.sin(mid * math.pi))))
    if split <= 0.01:
        rice_ball(cr, cx, cy, r)
    return sp, dp, anchors


def s_p6(cr, t, tl, t0, t1):
    c = cues(tl, "p6")
    tM, tC, tB, tE, tQ, tY = c["M"], c["C"], c["B"], c["E"], c["Q"], c["Y"]
    ground(cr)
    tint(cr, (1.0, 0.84, 0.62), 0.15)
    sp, dp, anchors = pie_scene(cr, t, tl, "p6")
    dev_q = cr.user_to_device(PIE[0] - 1.3 * PIE[2] * math.cos(0.25 * math.pi), PIE[1] + 1.15 * PIE[2] * 0.7)
    shows = {0: tB, 1: tB + 0.15, 2: tE, 3: tY}

    def ui(cr):
        if t < tY - 0.15:
            head(cr, t, "A FUNNY THING: EACH RICE-BALL HAS", tM - 0.1, "4 PORTIONS", tC)
        else:
            head(cr, t, "AND THE LAST ONE GOES TO", tY - 0.15, "THE MESSENGERS!", tY + 0.05)
        for i, (lab, (ax, ay)) in enumerate(anchors):
            if i == 2 and t > tE + 1.3:
                continue
            plate(cr, t, shows[i], lab, ax, ay, 32, RED if i == 3 else INK)
        if tQ < t < tY:
            big_mark(cr, t, tQ, "?", dev_q[0] - 60, dev_q[1] + 20, 130)
    return dict(ui=ui, lift=0.4, night=0.05)


def s_p7(cr, t, tl, t0, t1):
    c = cues(tl, "p7")
    tB, tC = c["B"], c["C"]
    ground(cr)
    tint(cr, (1.0, 0.84, 0.62), 0.15)
    sp, dp, anchors = pie_scene(cr, t, tl, "p7")
    mouth = sp["head"] if sp else (1500, 600)

    def ui(cr):
        head(cr, t, "DHANIRAM SAID:", tB - 0.1, "EVEN HERE, COMMISSION?!", tC)
        say(cr, t, tB, mouth[0] - 360, max(450, mouth[1] - 60), [("YAHAN BHI", 58, INK, tB + 0.1),
                                                        ("COMMISSION?!", 66, RED, tC)],
            tail=(mouth[0] - 40, mouth[1] - 30))
        for i, (lab, (ax, ay)) in enumerate(anchors):
            if i == 3:
                plate(cr, t, -1.0, lab, ax, ay, 32, RED)
    return dict(ui=ui, lift=0.4, night=0.05, flash=flash_at(t, tC, 0.15))


# ------------------------------------------------------------------ p8  hand-sized; day 13: led away, bound


def s_p8(cr, t, tl, t0, t1):
    c = cues(tl, "p8")
    tH, tT, tB, tBa, tC = c["H"], c["T"], c["B"], c["Ba"], c["C"]
    road_a = prog(t, tT - 0.1, 0.5)
    hand_a = 1 - road_a
    if hand_a > 0.01:                                    # the hand-sized body beside a big open hand
        ground(cr, alpha=hand_a)
        tint(cr, (1.0, 0.84, 0.62), 0.15 * hand_a)
        sh = 400.0
        Y.soul(cr, t, 820, FLOOR, sh, "sheepish", solid=1.0, glow=0.5, alpha=hand_a)
        ps = sh / 760.0
        q = prog(t, t0 + 0.3, 0.45)
        if q > 0.01:
            glow(cr, 1230, FLOOR - sh / 2, 360, 0.3 * q * hand_a)
            prop(cr, "ya_palm", 1250, FLOOR + 80 * (1 - q), ps, alpha=q * hand_a)
            for yy in (FLOOR - sh, FLOOR):
                dotted(cr, [(700, yy), (1400, yy)], prog(t, tH + 0.2, 0.5), 22, 4.5, RED, 0.9 * hand_a)
    if road_a > 0.01:                                    # day 13: bound, led off along the burning road
        road_set(cr, t, road_a)
        walk0 = min(tC - 0.2, tBa + 0.35)
        sx0 = 820.0
        if t < walk0:
            sx, legs, rock = sx0, (0.0, 0.0), 0.0
        else:
            sx, bob, rock, ph = hop_walk(t, walk0, walk0 + 6.0, sx0, sx0 + 900, 0.5)
            legs = walk_legs(ph, 0.28)
        lead = sx + 330
        dp = du(cr, t, lead, 0.6, feet=930, flip=False, hold="none", front=(0.6, -0.3), backa=(0.3, -0.25),
                ph=0.4, legs=legs, rot=rock, alpha=road_a)
        du(cr, t, sx - 340, 0.6, feet=970, flip=False, hold="staff", legs=legs, rot=rock, ph=1.1, alpha=road_a)
        bound = prog(t, tBa - 0.2, 0.4)
        sp = Y.soul(cr, t, sx, 950, 230, "crying", solid=1.0, glow=0.4, alpha=road_a,
                    front=mix((-0.32, -0.55), (-0.75, -1.2), bound), backa=mix((0.3, -0.25), (-0.7, -1.25), bound),
                    legs=legs, rot=rock)
        if sp and bound > 0.01:
            hf = to_user(cr, sp["handF"])
            hand = to_user(cr, dp["handB"])
            for k in range(3):
                cr.save()
                cr.translate(hf[0] - 4, hf[1] - 6 + 7 * k)
                cr.rotate(-0.3)
                cr.scale(1, 0.4)
                cr.arc(0, 0, 16, 0, 2 * math.pi)
                cr.restore()
                cr.set_source_rgba(*GC.ROPE, bound * road_a)
                cr.set_line_width(5)
                cr.stroke()
            if bound > 0.9:
                GC.rope(cr, [(hf[0] + 6, hf[1]), ((hf[0] + hand[0]) / 2, max(hf[1], hand[1]) + 50), hand], 7)
    dev_m = (1700, 330)

    def ui(cr):
        if t < tT - 0.2:
            box = head(cr, t, "THIS NEW BODY WAS ONLY", t0 + 0.05, "HAND-SIZED", tH)
            if box:
                underline(cr, t, box[0], box[0] + box[2], box[1] + box[3] + 22, tH + 0.5)
        else:
            head(cr, t, "DAY 13: TIED UP AND LED AWAY,", tT - 0.15, "LIKE A CAPTURED MONKEY", tB)
            counter_badge(cr, t, tT, "DAY 13", 205, 375, 76)
            q = back(clamp((t - tB) / 0.35), 1.6)
            if q > 0.01 and t < tC + 1.2:
                prop(cr, "ya_monkey", dev_m[0], dev_m[1], 0.7 * (0.6 + 0.4 * q),
                     alpha=clamp(q) * (1 - prog(t, tC + 0.9, 0.3)))
    return dict(ui=ui, lift_abs=0.3 + 0.6 * prog(t, tT, 0.5), flash=flash_at(t, tT, 0.15))


# ------------------------------------------------------------------ the shot table, draw, sfx


SHOTS = {
    "i1": (s_i1, {"z": (1.0, 1.05), "focus": (900, 640)}),
    "i2": (s_i2, {"z": (1.05, 1.07), "focus": (900, 640), "cont": True}),
    "i3": (s_i3, {"z": (1.0, 1.03)}),
    "i4": (s_i4, {"z": (1.0, 1.02)}),
    "i5": (s_i5, {"z": (1.02, 1.04), "cont": True}),
    "i6": (s_i6, {"z": (1.04, 1.05), "cont": True}),
    "i7": (s_i7, {"z": (1.05, 1.06), "cont": True}),
    "i8": (s_i8, {"z": (1.0, 1.02)}),
    "d1": (s_d1, {"z": (1.0, 1.03)}),
    "d2": (s_d2, {"z": (1.03, 1.06), "cont": True}),
    "d3": (s_d3, {"z": (1.0, 1.03)}),
    "d4": (s_d4, {"z": (1.0, 1.03)}),
    "d5": (s_d5, {"z": (1.0, 1.03)}),
    "d6": (s_d6, {"z": (1.0, 1.04)}),
    "d7": (s_d7, {"z": (1.0, 1.03)}),
    "d8": (s_d8, {"z": (1.0, 1.04), "focus": (1000, 600)}),
    "d9": (s_d9, {"z": (1.0, 1.04), "focus": (800, 600)}),
    "d10": (s_d10, {"z": (1.1, 1.15), "focus": (800, 640)}),
    "d11": (s_d11, {"z": (1.15, 1.22), "focus": (800, 660), "cont": True}),
    "d12": (s_d12, {"z": (1.0, 1.02)}),
    "d13": (s_d13, {"z": (1.0, 1.03)}),
    "p1": (s_p1, {"z": (1.0, 1.02)}),
    "p2": (s_p2, {"z": (1.0, 1.03)}),
    "p3": (s_p3, {"z": (1.0, 1.01)}),
    "p4": (s_p4, {"z": (1.01, 1.02), "cont": True}),
    "p5": (s_p5, {"z": (1.02, 1.03), "cont": True}),
    "p6": (s_p6, {"z": (1.0, 1.02)}),
    "p7": (s_p7, {"z": (1.02, 1.04), "cont": True}),
    "p8": (s_p8, {"z": (1.0, 1.03)}),
}


def active(tl, t):
    """The active line at t (the last one that has started), its start and the next line's start."""
    st = getattr(tl, "_ya_starts", None)
    if st is None:
        st = tl._ya_starts = [b.start for b in tl.beats]
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
    from scenes_jarasandha import motes
    motes(cr, t)
    night = out.get("night", 0.0)
    lamp(cr, t, night=night, flash=out.get("flash", 0.0))
    title_lift(cr, out.get("lift_abs", out.get("lift", 0.0) * max(0.35, min(1.0, 2.5 * night))))
    if out.get("ui"):
        out["ui"](cr)
    if not opt.get("cont") and t0 > 0 and t - t0 < 0.22:      # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur) for the intro, the two lives and the rice-balls, sparse (at most three a part): a damaru on
    the hook's first frame, a conch on the title card; a conch on part 1's card, a shimmer as the soul is drawn out, a
    hit on NO POCKET!; a conch on part 2's card, a bell as the new body is whole (day 10), a hit on COMMISSION?!. Each
    at least SFX_MIN_GAP from every sound already kept (render_myth.calm_sfx also keeps them apart across the whole
    video); the bed dips before the big reveals."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["i3"]["G"], "conch", 0),
            (c["d1"]["t0"], "conch", 0), (c["d8"]["P"], "shimmer", 0), (c["d11"]["N"], "hit", 0),
            (c["p1"]["t0"], "conch", 0), (c["p5"]["D"], "bell", 0), (c["p7"]["C"], "hit", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["i8"]["S"] - 0.35, "dip", 0.45), (c["d8"]["P"] - 0.35, "dip", 0.5), (c["d11"]["N"] - 0.3, "dip", 0.45),
            (c["p7"]["C"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
