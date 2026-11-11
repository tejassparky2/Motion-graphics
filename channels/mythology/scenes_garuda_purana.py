"""Scenes for videos/garuda_purana.py: "What happens after death, according to the Garuda Purana" (Preta Kalpa /
Saroddhara, chapters 1-3), in Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same
lamp-lit screen, two-tier headlines and rod-puppet motion as the Ruru and Dharmavyadha reels, with the cast from
garuda_cast. Eerie but calm, told so a child can follow: one plain label per step, and two devices that carry the idea:
THE SOUL, a tiny figure of warm-white light (first shown beside a big thumb: the same size), and THE NEW BODY, a figure
of light that fills in part by part, one part per rice-ball, over the ten days.

Respect and calm: Yama and Chitragupta are dignified; the messengers are tall dark silhouettes, fierce but never
monstrous (no fangs, no horns); the old man simply closes his eyes; his empty body is a dotted outline; the Vaitarani is
a wide dark-red river with whirlpools and nothing in it (no gore, no bodies); nobody is hurt on screen.

Every frame is a pure function of t. English on-screen text (shared by Hindi and Kannada) except the book's title on p2
and the soul's cry on p4, which also show in the viewer's script (गरुड़ पुराण / ಗರುಡ ಪುರಾಣ, हाय, हाय! / ಅಯ್ಯೋ, ಅಯ್ಯೋ!,
shaped by matplotlib as in scenes_arjuna; left out without the Nirmala font). Cues are words of the line in each
language ({"hi": ..., "kn": ...}) with a fraction fallback, kept in one table (CUES) that the scenes and sfx() both
read, with minimum gaps so a fast voice can't bunch the beats together.

Shot list (line: what is on the screen)
  p1  HOOK, frame 0: a big leather thumbs-up hand and, beside it, the soul: a tiny glowing figure exactly as tall as the
      thumb (dotted lines from the thumb's tip and base: SAME SIZE): AFTER DEATH THE SOUL BECOMES / THUMB-SIZED (big
      words in by 0.3 s, underlined on "angoothe", the thumb ringed); THE SOUL tag; a 10 DAYS badge; on "pindon" the
      hand goes, a banana leaf with ten rice-balls pops in: IN 10 DAYS, FROM RICE-BALLS: / A NEW BODY, and a body of
      light forms around the soul part by part
  p2  THIS IS NOT A / FILM STORY (crossed out); a palm-leaf book rises and opens: GARUDA PURANA, PART 2: PRETA KALPA
      (ringed), CHAPTERS 1-3, and the title in the viewer's script: IT'S WRITTEN IN THE / GARUDA PURANA
  p3  evening, a room: an old man on a rope cot, a small lamp; THE GARUDA PURANA SAYS: / AT DEATH...; the lamp dims, his
      eyes close; two tall dark messengers come out of the night in the doorway (staff, noose): THEN COME / YAMA'S
      MESSENGERS (tag)
  p4  closer: one messenger casts a noose of light; the tiny soul is drawn up out of the old man's chest: THEY CATCH THE
      / THUMB-SIZED SOUL, AND PULL IT / OUT OF THE BODY; his body fades to a dotted outline (HIS BODY); the soul's hands
      go to its head: cloud OH! OH! with हाय, हाय! / ಅಯ್ಯೋ, ಅಯ್ಯೋ!
  p5  Yama's hall: Yama on his throne (tag YAMA), a messenger holds the soul before him: THE MESSENGERS TAKE IT TO /
      YAMA; Yama raises his hand; the soul flies up along a dotted arc, the hall fades into the night and the house,
      and the soul comes down at the door: BY YAMA'S ORDER, IT FLIES / BACK HOME
  p6  the room again, the dotted body on the cot (HIS BODY); the soul dives at it and bounces off, twice: IT TRIED TO GO
      BACK / INTO ITS BODY, BUT IT / COULDN'T; it floats, arms down; the outline ringed: NOW IT HAS / NO BODY
  p7  the son kneels (tag HIS SON) by a small lamp and sets a rice-ball on a banana leaf: THEN, FOR 10 DAYS, / HIS SON
      / OFFERS / RICE-BALLS; card 10 DAYS, / 10 RICE-BALLS; a dotted body appears with the soul in its chest, light
      flows from the ball into it: EACH RICE-BALL MAKES / A NEW BODY PART
  p8  the dotted body large; each day a part fills with light (a glow as it forms), a rice-ball joins the row on the
      leaf, a DAY n tag points at it: DAY 1: / HEAD, DAY 2: / NECK & SHOULDERS, DAY 3: / HEART, DAY 4: / BACK
  p9  the same: DAY 5: / NAVEL, DAY 6: / HIPS, DAY 7: / THIGHS, DAY 8: / KNEES, DAY 9: / FEET
  p10 DAY 10: the whole body glows; one hand goes to its belly, the other to its throat (both ringed): DAY 10: / HUNGER
      & THIRST
  p11 night: a long road winds up to Yama's far door; the soul starts walking; sixteen tiny city gates pop in along it;
      badges 86,000 YOJANAS, 16 CITIES, ~1 YEAR: THEN BEGINS THE JOURNEY TO / YAMA'S CITY
  p12 a dry, cracked road, a dead tree, a hot sun; the soul trudges; an empty water pot and an empty bowl, crossed out:
      ON THE ROAD: / NO FOOD, NO WATER; a rice-ball comes down on a thread of light into its hands (tag EVERY MONTH),
      the soul brightens: ITS ONLY FOOD: / A RICE-BALL A MONTH
  p13 a wide dark-red river with slow whirlpools (no gore), the soul small on the near bank, Yama's door far across:
      AND HALF-WAY COMES THE RIVER / VAITARANI; a width arrow 100 YOJANAS: THE VAITARANI: / 100 YOJANAS WIDE; NOT WATER
  p14 a ferry with its boatman crosses to the bank: TO CROSS IT, / A BOAT COMES; two souls wait, one with a cow
      medallion, one with an empty one: BUT ONLY FOR THOSE WHO / GAVE A COW (ringed); the cow-giver steps into the boat
  p15 Yama's hall: Chitragupta (tag) unrolls a long scroll of deeds (ticks and crosses), the soul before them:
      CHITRAGUPTA READS EVERY DEED: / THE ACCOUNT; Yama (tag) raises his staff, a flash: AND YAMA GIVES HIS / JUDGEMENT
  p16 the soul small in the middle, the road to Yama's door faint behind: THE GARUDA PURANA SAYS: / THIS IS THE
      JOURNEY, then DO YOU / BELIEVE IT?; BELIEVE? / DON'T? cards, a red ring alternating (the question is the last
      line)
"""
import math

import cairo

import dharmavyadha_cast as DV
import garuda_cast as GC
import puppet_core as pc
import ruru_cast as RU
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, cross, draw_text, ease, prog, tick
from puppet_core import H, W, depth, keyed, prop, puppet, sway
from scenes_arjuna import card2, cloud_text
from scenes_dharmavyadha import point_to, script_strip
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, man_angles, motes, red_ring, stars
from scenes_jayadratha import NIGHT, flash_at, tag, tint, title_lift, to_user
from scenes_kaikeyi import ANJALI, card, fig
from scenes_lakshman_rekha import big_x, book, sparkle
from scenes_mandhata import aura, burst, held, lights, mix, reach_arm, warm
from scenes_ravana import dotted, head2
from scenes_ruru import flow, held_grip, nods, plate
from scenes_six_b import body_outline, counter_badge
from shots import T, shot_at

MISSES = set()                       # cue words not found in a line (falls back to fractions)
G = FEET + 120                       # the floor of most sets
TITLE = {"hi": "गरुड़ पुराण", "kn": "ಗರುಡ ಪುರಾಣ"}           # the book's title in the viewer's script (p2)
CRY = {"hi": "हाय, हाय!", "kn": "ಅಯ್ಯೋ, ಅಯ್ಯೋ!"}            # the soul's cry (p4)
SOUL_W = (1.0, 0.97, 0.86)           # the soul's light
SOUL_GOLD = (1.0, 0.76, 0.28)
SOUL_RIM = (0.50, 0.28, 0.06)
DOT_C = (0.40, 0.26, 0.12)           # dotted outlines


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, words)
    except (KeyError, ValueError):
        MISSES.add((bid, words[getattr(tl, "lang", "hi")] if isinstance(words, dict) else words))
        return T(tl, bid, frac)


# Every cue of every line: (name, {"hi": word, "kn": word}, fraction fallback, ((after, min gap), ...)); "t0" = the
# line's start. Words are exact substrings of the script lines (checked: MISSES stays empty).
CUES = {
    "p1": (("A", {"hi": "आत्मा", "kn": "ಆತ್ಮ"}, 0.17, (("t0", 0.6),)),
           ("T", {"hi": "अंगूठे", "kn": "ಹೆಬ್ಬೆರಳಿನಷ್ಟು"}, 0.25, (("A", 0.4),)),
           ("S", {"hi": "छोटी", "kn": "ಚಿಕ್ಕದಾಗುತ್ತೆ"}, 0.38, (("T", 0.6),)),
           ("D", {"hi": "दस", "kn": "ಹತ್ತು"}, 0.55, (("S", 0.8),)),
           ("P", {"hi": "पिंडों", "kn": "ಪಿಂಡಗಳಿಂದ"}, 0.7, (("D", 0.6),)),
           ("N", {"hi": "नया", "kn": "ಹೊಸ"}, 0.85, (("P", 0.6),))),
    "p2": (("X", {"hi": "नहीं", "kn": "ಅಲ್ಲ"}, 0.3, (("t0", 0.6),)),
           ("G", {"hi": "गरुड़", "kn": "ಗರುಡ"}, 0.6, (("X", 0.5),)),
           ("L", {"hi": "लिखा", "kn": "ಇದೆ"}, 0.85, (("G", 0.5),))),
    "p3": (("M", {"hi": "मौत", "kn": "ಸಾವಿನ"}, 0.35, (("t0", 0.6),)),
           ("Y", {"hi": "यमराज", "kn": "ಯಮನ"}, 0.65, (("M", 0.5),)),
           ("D", {"hi": "दूत", "kn": "ದೂತರು"}, 0.78, (("Y", 0.3),)),
           ("A", {"hi": "आते", "kn": "ಬರ್ತಾರೆ"}, 0.9, (("D", 0.4),))),
    "p4": (("T", {"hi": "अंगूठे", "kn": "ಹೆಬ್ಬೆರಳಿನಷ್ಟು"}, 0.1, (("t0", 0.3),)),
           ("P", {"hi": "खींचकर", "kn": "ಎಳೆದು"}, 0.4, (("T", 0.7),)),
           ("O", {"hi": "निकालते", "kn": "ತೆಗೀತಾರೆ"}, 0.55, (("P", 0.6),)),
           ("C", {"hi": "चिल्लाती", "kn": "ಕೂಗುತ್ತೆ"}, 0.75, (("O", 0.6),)),
           ("H", {"hi": "हाय", "kn": "ಅಯ್ಯೋ"}, 0.85, (("C", 0.3),))),
    "p5": (("Y", {"hi": "यमराज", "kn": "ಯಮನ"}, 0.15, (("t0", 0.3),)),
           ("F", {"hi": "सामने", "kn": "ಮುಂದೆ"}, 0.3, (("Y", 0.4),)),
           ("C", {"hi": "हुक्म", "kn": "ಆಜ್ಞೆಯಿಂದ"}, 0.55, (("F", 0.8),)),
           ("A", {"hi": "हवा", "kn": "ಗಾಳಿಯಲ್ಲಿ"}, 0.68, (("C", 0.5),)),
           ("H", {"hi": "घर", "kn": "ಮನೆಗೆ"}, 0.85, (("A", 0.6),))),
    "p6": (("W", {"hi": "वापस", "kn": "ಒಳಗೆ"}, 0.25, (("t0", 0.4),)),
           ("B", {"hi": "पर", "kn": "ಆದ್ರೆ"}, 0.55, (("W", 0.9),)),
           ("N", {"hi": "अब", "kn": "ಈಗ"}, 0.75, (("B", 0.8),)),
           ("Z", {"hi": "कोई", "kn": "ಇಲ್ಲ"}, 0.88, (("N", 0.3),))),
    "p7": (("S", {"hi": "बेटा", "kn": "ಮಗ"}, 0.05, (("t0", 0.2),)),
           ("D", {"hi": "दस", "kn": "ಹತ್ತು"}, 0.15, (("S", 0.4),)),
           ("P", {"hi": "पिंड", "kn": "ಪಿಂಡ"}, 0.35, (("D", 0.6),)),
           ("E", {"hi": "हर", "kn": "ಪ್ರತಿ"}, 0.6, (("P", 0.8),)),
           ("N", {"hi": "हिस्सा", "kn": "ಭಾಗ"}, 0.85, (("E", 0.6),))),
    "p8": (("D1", {"hi": "पहले", "kn": "ಮೊದಲ"}, 0.02, ()),
           ("H1", {"hi": "सिर", "kn": "ತಲೆ"}, 0.12, (("D1", 0.4),)),
           ("D2", {"hi": "दूसरे", "kn": "ಎರಡನೇ"}, 0.2, (("H1", 0.5),)),
           ("H2", {"hi": "गर्दन", "kn": "ಕುತ್ತಿಗೆ"}, 0.32, (("D2", 0.4),)),
           ("D3", {"hi": "तीसरे", "kn": "ಮೂರನೇ"}, 0.55, (("H2", 0.8),)),
           ("H3", {"hi": "दिल", "kn": "ಹೃದಯ"}, 0.68, (("D3", 0.4),)),
           ("D4", {"hi": "चौथे", "kn": "ನಾಲ್ಕನೇ"}, 0.75, (("H3", 0.5),)),
           ("H4", {"hi": "पीठ", "kn": "ಬೆನ್ನು"}, 0.9, (("D4", 0.4),))),
    "p9": (("N", {"hi": "नाभि", "kn": "ಹೊಕ್ಕುಳು"}, 0.25, (("t0", 0.5),)),
           ("Hp", {"hi": "कमर", "kn": "ಸೊಂಟ"}, 0.5, (("N", 0.6),)),
           ("Th", {"hi": "जांघ", "kn": "ತೊಡೆ"}, 0.62, (("Hp", 0.5),)),
           ("K", {"hi": "घुटने", "kn": "ಮಂಡಿ"}, 0.75, (("Th", 0.5),)),
           ("F", {"hi": "पैर", "kn": "ಕಾಲು"}, 0.9, (("K", 0.5),))),
    "p10": (("D", {"hi": "दसव", "kn": "ಹತ್ತನೇ"}, 0.1, ()),
            ("Hu", {"hi": "भूख", "kn": "ಹಸಿವು"}, 0.6, (("D", 0.9),)),
            ("Th", {"hi": "प्यास", "kn": "ಬಾಯಾರಿಕೆ"}, 0.85, (("Hu", 0.5),))),
    "p11": (("Y", {"hi": "नगरी", "kn": "ಯಮಪುರಿಯ"}, 0.25, (("t0", 0.6),)),
            ("K", {"hi": "छियासी", "kn": "ಎಂಬತ್ತಾರು"}, 0.45, (("Y", 0.8),)),
            ("S", {"hi": "सोलह", "kn": "ಹದಿನಾರು"}, 0.7, (("K", 1.0),)),
            ("Yr", {"hi": "साल", "kn": "ವರ್ಷ"}, 0.92, (("S", 0.8),))),
    "p12": (("W", {"hi": "पानी", "kn": "ನೀರೂ"}, 0.12, (("t0", 0.3),)),
            ("F", {"hi": "खाना", "kn": "ಊಟನೂ"}, 0.22, (("W", 0.5),)),
            ("P", {"hi": "पिंडों", "kn": "ಪಿಂಡಗಳ"}, 0.55, (("F", 0.8),)),
            ("M", {"hi": "महीने", "kn": "ತಿಂಗಳು"}, 0.85, (("F", 0.8),))),
    "p13": (("V", {"hi": "वैतरणी", "kn": "ವೈತರಣಿ"}, 0.3, (("t0", 0.5),)),
            ("C", {"hi": "सौ", "kn": "ನೂರು"}, 0.48, (("V", 0.7),)),
            ("N", {"hi": "पानी", "kn": "ನೀರಲ್ಲ"}, 0.7, (("C", 0.8),)),
            ("B", {"hi": "बहता", "kn": "ಹರಿಯುತ್ತೆ"}, 0.92, (("N", 0.6),))),
    "p14": (("B", {"hi": "नाव", "kn": "ದೋಣಿ"}, 0.3, (("t0", 0.4),)),
            ("O", {"hi": "पर", "kn": "ಆದ್ರೆ"}, 0.48, (("B", 0.6),)),
            ("C", {"hi": "गाय", "kn": "ಹಸು"}, 0.82, (("O", 0.8),)),
            ("G", {"hi": "दान", "kn": "ದಾನ"}, 0.9, (("C", 0.3),))),
    "p15": (("C", {"hi": "चित्रगुप्त", "kn": "ಚಿತ್ರಗುಪ್ತ"}, 0.12, (("t0", 0.3),)),
            ("A", {"hi": "हिसाब", "kn": "ಲೆಕ್ಕ"}, 0.45, (("C", 0.8),)),
            ("Y", {"hi": "यमराज", "kn": "ಯಮ"}, 0.7, (("A", 0.8),)),
            ("J", {"hi": "सुनाते", "kn": "ತೀರ್ಪು"}, 0.88, (("Y", 0.5),))),
    "p16": (("J", {"hi": "यही", "kn": "ಇದೇ"}, 0.3, (("t0", 0.5),)),
            ("Q", {"hi": "मानते", "kn": "ನಂಬ್ತೀರಾ"}, 0.62, (("J", 0.8),)),
            ("Y", {"hi": "हाँ", "kn": "ಹೌದಾ"}, 0.75, (("Q", 0.5),)),
            ("C", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.88, (("Y", 0.4),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_gp_cues", None)
    if cache is None:
        cache = {}
        tl._gp_cues = cache
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


# ------------------------------------------------------------------ the soul


ARMS = {"rest": ((0.05, 0.17), (0.08, 0.33)), "up": ((0.11, 0.12), (0.05, -0.12)),
        "reach": ((0.15, -0.10), (0.22, -0.27)), "droop": ((0.03, 0.17), (0.02, 0.32)),
        "out": ((0.16, 0.06), (0.30, 0.0))}


def soul(cr, t, x, feet, h, a=1.0, arms="rest", walk=None, halo=1.0, shiver=0.0):
    """The soul as the Garuda Purana tells it: a tiny human figure of warm-white light (head, body, arms, legs, no
    face) with a gold rim, a soft halo and a gentle flicker. (x, feet) = where its feet are, h = its height; arms:
    rest | up (hands to its head: crying out) | reach | droop | out, or a mix (a pair of ((elbow), (hand)) offsets);
    walk = the stride phase (radians) when it walks."""
    if a <= 0.01 or h < 4:
        return
    u = h
    x += shiver * 0.03 * u * math.sin(t * 40)
    pul = 0.93 + 0.07 * math.sin(t * 3.3 + x * 0.013)
    if walk is not None:
        feet -= 0.025 * u * abs(math.sin(walk))
    if halo > 0:
        glow(cr, x, feet - 0.55 * u, 1.5 * u + 50, min(1.0, 0.8 * a * halo * pul))
        warm(cr, x, feet - 0.55 * u, 0.8 * u + 24, 0.55 * a * halo)
        aura(cr, t, x, feet - 0.55 * u, 0.42 * u, 0.95 * u + 20, 0.3 * a * halo, n=16, spin=0.05)
    el, hd = ARMS[arms] if isinstance(arms, str) else arms
    sh_y, hip_y = feet - 0.74 * u, feet - 0.43 * u
    hx, hy, hr = x, feet - 0.885 * u, 0.1 * u
    limbs = []
    for k, sg in enumerate((-1, 1)):
        sx_ = x + sg * 0.13 * u
        limbs.append([(sx_, sh_y + 0.02 * u), (sx_ + sg * el[0] * u, sh_y + el[1] * u),
                      (sx_ + sg * hd[0] * u, sh_y + hd[1] * u)])
        lift = max(0.0, math.sin(walk + k * math.pi)) if walk is not None else 0.0
        limbs.append([(x + sg * 0.055 * u, hip_y), (x + sg * 0.065 * u, hip_y + (0.22 - 0.07 * lift) * u),
                      (x + sg * 0.07 * u, feet - 0.09 * lift * u)])
    lw = 0.085 * u
    torso = [(x - 0.14 * u, sh_y), (x + 0.14 * u, sh_y), (x + 0.085 * u, hip_y + 0.03 * u),
             (x - 0.085 * u, hip_y + 0.03 * u)]
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    for extra, col, al in ((0.05 * u + 4, SOUL_RIM, 0.7), (0.024 * u + 2, SOUL_GOLD, 0.95), (0.0, SOUL_W, 1.0)):
        cr.set_source_rgba(*col, al * a * (pul if extra == 0 else 1.0))
        for limb in limbs:
            cr.move_to(*limb[0])
            for p in limb[1:]:
                cr.line_to(*p)
            cr.set_line_width(lw + extra)
            cr.stroke()
        cr.move_to(hx, hy)
        cr.line_to(x, sh_y + 0.05 * u)
        cr.set_line_width(0.07 * u + extra)
        cr.stroke()
        pc.poly(cr, torso)
        cr.set_line_width(0.06 * u + extra)
        cr.stroke_preserve()
        cr.fill()
        cr.arc(hx, hy, hr + extra / 2, 0, 2 * math.pi)
        cr.fill()
    g = cairo.RadialGradient(x, feet - 0.62 * u, 0, x, feet - 0.62 * u, 0.3 * u)
    g.add_color_stop_rgba(0, 1.0, 1.0, 0.95, 0.55 * a)
    g.add_color_stop_rgba(1, 1.0, 1.0, 0.95, 0.0)
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_source(g)
    cr.arc(x, feet - 0.62 * u, 0.3 * u, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def light_rope(cr, pts, a=1.0, w=1.0):
    """A rope of light (the messengers' noose, the rice-ball's thread) along pts."""
    if a <= 0.01 or len(pts) < 2:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, col, al in ((30, (0.42, 0.20, 0.04), 0.35), (16, (1.0, 0.60, 0.12), 0.85), (6, (1.0, 0.95, 0.72), 1.0)):
        cr.new_path()
        pc.spath(cr, pts, closed=False)
        cr.set_source_rgba(*col, al * a)
        cr.set_line_width(lw * w)
        cr.stroke()
    cr.restore()


def noose_loop(cr, t, x, y, rx, ry, a=1.0):
    """The noose of light closed round the soul's waist."""
    pts = [(x + rx * math.cos(q), y + ry * math.sin(q)) for q in (2 * math.pi * i / 24 for i in range(25))]
    light_rope(cr, pts, a, 0.8)


def bezier(p0, p1, p2, u):
    return ((1 - u) ** 2 * p0[0] + 2 * (1 - u) * u * p1[0] + u * u * p2[0],
            (1 - u) ** 2 * p0[1] + 2 * (1 - u) * u * p1[1] + u * u * p2[1])


# ------------------------------------------------------------------ the new body (front view, part by part)


BODY_PARTS = ("head", "neck", "heart", "back", "navel", "hips", "thighs", "knees", "feet")
DAY_LABEL = ("HEAD", "NECK & SHOULDERS", "HEART", "BACK", "NAVEL", "HIPS", "THIGHS", "KNEES", "FEET",
             "HUNGER & THIRST")


def _ik(s, tg, l1, l2, bend):
    dx, dy = tg[0] - s[0], tg[1] - s[1]
    d = max(1e-3, min(math.hypot(dx, dy), (l1 + l2) * 0.999))
    a = math.atan2(dy, dx)
    b = math.acos(clamp((l1 * l1 + d * d - l2 * l2) / (2 * l1 * d), -1.0, 1.0))
    el = (s[0] + l1 * math.cos(a + bend * b), s[1] + l1 * math.sin(a + bend * b))
    return el, (s[0] + d * math.cos(a), s[1] + d * math.sin(a))


def body_shapes(x, feet, h, hands=None):
    """{part: [shape]} for the new body standing at (x, feet), h tall (front view); hands = {"L"|"R": target}."""
    u = h

    def P(px, py):
        return x + px * u, feet + py * u
    neck = [("poly", [P(-0.032, -0.815), P(0.032, -0.815), P(0.038, -0.75), P(-0.038, -0.75)]),
            ("smooth", [P(-0.175, -0.722), P(-0.155, -0.758), P(-0.05, -0.78), P(0.05, -0.78), P(0.155, -0.758),
                        P(0.175, -0.722), P(0.0, -0.712)])]
    arms = []
    for sg, key in ((-1, "L"), (1, "R")):
        s_ = P(sg * 0.158, -0.738)
        tg = (hands or {}).get(key) or P(sg * 0.235, -0.43)
        el, hd = _ik(s_, tg, 0.17 * u, 0.165 * u, -sg)
        arms += [("seg", s_, el, 0.042 * u, 0.034 * u), ("seg", el, hd, 0.034 * u, 0.027 * u),
                 ("ell", hd, 0.022 * u, 0.028 * u)]
    return {
        "head": [("ell", P(0, -0.885), 0.064 * u, 0.08 * u)],
        "neck": neck,
        "arms": arms,
        "heart": [("heart", P(0.045, -0.66), 0.044 * u)],
        "back": [("smooth", [P(-0.16, -0.73), P(0.16, -0.73), P(0.148, -0.66), P(0.112, -0.575), P(-0.112, -0.575),
                             P(-0.148, -0.66)])],
        "navel": [("smooth", [P(-0.116, -0.585), P(0.116, -0.585), P(0.106, -0.525), P(0.118, -0.47), P(-0.118, -0.47),
                              P(-0.106, -0.525)]),
                  ("dot", P(0, -0.52), 0.013 * u)],
        "hips": [("smooth", [P(-0.12, -0.485), P(0.12, -0.485), P(0.138, -0.425), P(0.11, -0.378), P(0.0, -0.372),
                             P(-0.11, -0.378), P(-0.138, -0.425)])],
        "thighs": [("seg", P(sg * 0.072, -0.41), P(sg * 0.07, -0.25), 0.066 * u, 0.05 * u) for sg in (-1, 1)],
        "knees": [("seg", P(sg * 0.07, -0.252), P(sg * 0.068, -0.15), 0.054 * u, 0.044 * u) for sg in (-1, 1)],
        "feet": [("seg", P(sg * 0.068, -0.152), P(sg * 0.066, -0.04), 0.044 * u, 0.032 * u) for sg in (-1, 1)] +
                [("ell", P(sg * 0.086, -0.022), 0.048 * u, 0.022 * u) for sg in (-1, 1)],
    }


def _shape_path(cr, sh, caps=True):
    cr.new_path()
    kind = sh[0]
    if kind == "poly":
        pc.poly(cr, sh[1])
    elif kind == "smooth":
        pc.spath(cr, sh[1])
    elif kind == "ell":
        pc.ell(cr, sh[1][0], sh[1][1], sh[2], sh[3])
    elif kind == "dot":
        cr.arc(sh[1][0], sh[1][1], sh[2], 0, 2 * math.pi)
    elif kind == "heart":
        (cx, cy), r = sh[1], sh[2]
        pts = []
        for i in range(40):
            q = 2 * math.pi * i / 40
            hx = 16 * math.sin(q) ** 3
            hy = -(13 * math.cos(q) - 5 * math.cos(2 * q) - 2 * math.cos(3 * q) - math.cos(4 * q))
            pts.append((cx + r * hx / 16, cy + r * hy / 16))
        pc.poly(cr, pts)
    elif kind == "seg":
        p0, p1, w0, w1 = sh[1], sh[2], sh[3], sh[4]
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        ln = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / ln, dx / ln
        pc.poly(cr, [(p0[0] + nx * w0 / 2, p0[1] + ny * w0 / 2), (p1[0] + nx * w1 / 2, p1[1] + ny * w1 / 2),
                     (p1[0] - nx * w1 / 2, p1[1] - ny * w1 / 2), (p0[0] - nx * w0 / 2, p0[1] - ny * w0 / 2)])
        if caps:
            cr.new_sub_path()
            cr.arc(p0[0], p0[1], w0 / 2, 0, 2 * math.pi)
            cr.new_sub_path()
            cr.arc(p1[0], p1[1], w1 / 2, 0, 2 * math.pi)


def _centre(sh):
    if sh[0] in ("poly", "smooth"):
        return sum(p[0] for p in sh[1]) / len(sh[1]), sum(p[1] for p in sh[1]) / len(sh[1])
    if sh[0] == "seg":
        return (sh[1][0] + sh[2][0]) / 2, (sh[1][1] + sh[2][1]) / 2
    return sh[1]


def light_body(cr, t, x, feet, h, parts, alpha=1.0, hands=None, outline=1.0, oc=DOT_C, bright=0.0):
    """The new body the rice-balls build: each part a dotted outline until it forms (parts[name] 0..1), then a figure
    of warm light; a glow blooms where a part is forming. Returns {part: centre} plus 'throat' and 'belly'."""
    shapes = body_shapes(x, feet, h, hands)
    cen = {k: _centre(v[0]) for k, v in shapes.items()}
    cen["neck"] = _centre(shapes["neck"][1])
    cen["throat"] = (x, feet - 0.79 * h)
    cen["belly"] = (x, feet - 0.52 * h)
    if alpha <= 0.01:
        return cen
    pr = dict(parts)
    pr["arms"] = pr.get("neck", 0.0)                    # the arms come with the neck and shoulders (day 2)
    formed = sum(clamp(pr.get(k, 0.0)) for k in BODY_PARTS) / len(BODY_PARTS)
    if formed > 0:
        glow(cr, x, feet - 0.5 * h, 0.8 * h, (0.45 + 0.35 * bright) * alpha * formed)
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    if outline > 0.01:                                  # what is still to come: dotted
        cr.set_dash([0.1, max(9.0, 0.016 * h)])
        cr.set_line_width(max(4.0, 0.0075 * h))
        for k in BODY_PARTS + ("arms",):
            p = clamp(pr.get(k, 0.0))
            if p >= 1:
                continue
            cr.set_source_rgba(*oc, 0.85 * outline * alpha * (1 - p))
            for sh in shapes[k]:
                if sh[0] == "dot":
                    continue
                _shape_path(cr, sh, caps=False)
                cr.stroke()
        cr.set_dash([])
    rim = max(3.0, 0.011 * h)

    def lit(group):                                     # rim passes first, then the light: one seamless figure
        group = [k for k in group if pr.get(k, 0.0) > 0]
        for col, wid, al in (((0.62, 0.34, 0.08), 2.4 * rim, 0.75), ((1.0, 0.72, 0.22), 1.2 * rim, 0.95),
                             ((1.0, 0.91, 0.62), 0.0, 0.92 + 0.08 * bright)):
            for k in group:
                cr.set_source_rgba(*col, al * clamp(pr[k]) * alpha)
                for sh in shapes[k]:
                    if sh[0] == "dot":
                        continue
                    _shape_path(cr, sh)
                    if wid:
                        cr.set_line_width(wid)
                        cr.stroke()
                    else:
                        cr.fill()
    lit([k for k in BODY_PARTS if k != "heart"])
    if parts.get("navel", 0.0) > 0:
        sh = shapes["navel"][1]
        cr.arc(sh[1][0], sh[1][1], sh[2], 0, 2 * math.pi)
        cr.set_source_rgba(0.80, 0.48, 0.14, clamp(parts["navel"]) * alpha)
        cr.fill()
    ph = clamp(parts.get("heart", 0.0))
    if ph > 0:                                          # the heart glows red inside the chest
        _shape_path(cr, shapes["heart"][0])
        cr.set_source_rgba(0.92, 0.26, 0.18, (0.9 - 0.25 * clamp(parts.get("back", 0.0))) * ph * alpha)
        cr.fill_preserve()
        cr.set_source_rgba(0.55, 0.10, 0.05, 0.8 * ph * alpha)
        cr.set_line_width(max(2.0, 0.003 * h))
        cr.stroke()
    lit(["arms"])                                       # the arms over the body (hands on the belly, the throat)
    for k in BODY_PARTS:
        p = clamp(parts.get(k, 0.0))
        if 0 < p < 1:                                   # the part blooms as it forms
            cx, cy = cen[k]
            glow(cr, cx, cy, 0.22 * h + 40, 0.9 * math.sin(math.pi * p) * alpha)
            sparkle(cr, cx, cy, (0.05 * h + 14) * math.sin(math.pi * p), alpha, (1.0, 0.95, 0.75))
    cr.restore()
    return cen


def lying_outline(cr, cx, cy, length, alpha=1.0, p=1.0):
    """The old man's empty body: six_b's dotted body outline laid down on its back, head to the left."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.translate(cx, cy)
    cr.rotate(-math.pi / 2)
    body_outline(cr, 0, length / 2, length, p, alpha)
    cr.restore()


# ------------------------------------------------------------------ puppets


def old_man(cr, t, x, top, s, eyes="open", alpha=1.0, blur=0.0, reach=0.0):
    """The old man lying on his back on a cot whose top is at `top` (hip at x), head to the left; reach lifts his front
    hand a little (weakly)."""
    fr = mix((0.05, -0.15), (-0.9, -0.5), reach)
    ang = man_angles("gp_old", t, fr, (0.1, -0.1), 0.0, (0.0, 0.0), (), 0.0)
    hy = top - 80 * s + 2.5 * math.sin(t * 2.0) * (eyes == "open")
    sw = {"gp_old_head": "gp_old_head" + ("" if eyes == "open" else "_shut")}
    return puppet(cr, GC.OLD, x, hy, s, -math.pi / 2, False, ang, alpha, blur, swap=sw, rods=False)


def duta(cr, t, x, s, feet=G, flip=True, front=(-0.4, -0.5), backa=(0.3, -0.3), hold="staff", tilt=0.0, head=0.0,
         alpha=1.0, blur=0.0, hits=(), ph=0.0, rot=0.0):
    """A Yamaduta standing, facing left (flip), his staff (hold staff) or the rope noose (hold noose) in his front
    hand."""
    ex = {}
    if hold == "staff":
        ex["gp_duta_armF_lo"] = held_grip("gp_dstaff", front, 0.62, tilt, 40, alpha, blur)
    elif hold == "noose":
        ex["gp_duta_armF_lo"] = held("gp_noose", front, 0.62, 150, 0.0, alpha, blur)
    return fig(cr, GC.DUTA, "gp_duta", t, x, s, front=front, backa=backa, head=head, hits=hits, flip=flip,
               alpha=alpha, blur=blur, feet=feet, ph=ph, extra=ex, rot=rot)


def yama_seated(cr, t, x, ground, s, flip=True, front=(-0.55, -0.85), backa=(0.3, -0.3), nod=0.0, grip=120.0,
                head=0.0, alpha=1.0, blur=0.0, hits=(), store=None):
    """Yama (ruru_cast) seated on mandhata_cast's throne (pivot on the ground), his danda in his front hand."""
    prop(cr, "md_throne", x, ground, s, flip=flip, alpha=alpha, blur=blur)
    hip = ground - 246 * s
    prop(cr, "gp_yama_seat", x, hip, s, flip=flip, alpha=alpha, blur=blur)
    ang = man_angles("rr_yama", t, front, backa, head + 0.2 * nod, (0.0, 0.0), hits, 0.6)
    ex = {"rr_yama_armF_lo": held_grip("rr_danda", front, 0.68, 0.0, grip, alpha, blur, store)}
    return puppet(cr, RU.YAMA, x, hip, s, bob_rot(t, 0.6, 0.006), flip, ang, alpha, blur,
                  hide=("rr_yama_legF", "rr_yama_legB"), extra=ex)


def diya(cr, t, x, ground, s=1.0, alpha=1.0, lit=1.0):
    """The small clay lamp with its flickering flame."""
    prop(cr, "gp_diya", x, ground, s, alpha=alpha)
    wx, wy = x + GC.DIYA_WICK[0] * s, ground + GC.DIYA_WICK[1] * s
    if lit > 0.01:
        glow(cr, wx, wy - 50 * s, 240 * s + 40, (0.55 + 0.08 * math.sin(t * 9)) * alpha * lit)
        prop(cr, f"flame{int(t * 10) % 3}", wx, wy + 6 * s, 0.24 * s * (0.6 + 0.4 * lit), alpha=alpha * lit)


def ground(cr, y=G, alpha=1.0):
    prop(cr, "ground", W / 2, y + 6, 0.82, alpha=alpha)


def room_set(cr, t, alpha=1.0):
    """The old man's room: dharmavyadha_cast's back wall (soft), the floor."""
    prop(cr, "dv_room", 540, G + 6, 0.86, alpha=0.78 * alpha, blur=4)
    ground(cr, alpha=alpha)


def cot(cr, x, s, ground_=G, alpha=1.0):
    """The rope cot; returns its top (y)."""
    prop(cr, "dv_charpai", x, ground_, s, alpha=alpha)
    return ground_ - (DV.BENCH_H - 60) * s


def pinda(cr, x, y, s, alpha=1.0):
    """A rice-ball, painted over what is under it (white leather would vanish into a green leaf when multiplied)."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    pc.paint_part(cr, "gp_pinda", alpha, 0.0, cairo.OPERATOR_OVER)
    cr.restore()


def rice_row(cr, t, x, y, s, n, t_in=None, slots=10, gap=82.0, ball=0.72):
    """The banana leaf with the rice-balls offered so far (n, a float: the last one drops in), dotted rings for the
    days still to come."""
    a = prog(t, t_in, 0.35) if t_in is not None else 1.0
    if a <= 0.01:
        return
    prop(cr, "gp_leaf", x, y + 18 * (1 - a), s, alpha=a)
    for i in range(slots):
        bx = x + (i - (slots - 1) / 2) * gap
        q = clamp(n - i)
        if q < 1:
            cr.save()
            cr.set_dash([0.1, 11])
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.set_line_width(5)
            cr.arc(bx, y - 22, 46 * ball * 0.86, 0, 2 * math.pi)
            cr.set_source_rgba(*DOT_C, 0.55 * a * (1 - q))
            cr.stroke()
            cr.restore()
        if q > 0:
            pinda(cr, bx, y - 22 - 60 * (1 - back(q, 2.0)), ball * (0.6 + 0.4 * q), alpha=a * clamp(q * 2))


def cow_badge(cr, t, t_in, x, y, r, empty=False, alpha=1.0):
    """A round medallion with the gift cow in it (empty: a dotted ring only, nothing given)."""
    q = back(clamp((t - t_in) / 0.35), 1.6)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    rr = r * (0.6 + 0.4 * q)
    cr.save()
    if empty:
        cr.set_dash([0.1, 14])
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_width(7)
        cr.arc(x, y, rr, 0, 2 * math.pi)
        cr.set_source_rgba(1.0, 0.88, 0.6, 0.8 * a)
        cr.stroke()
    else:
        glow(cr, x, y, rr * 2.2, 0.5 * a)
        cr.arc(x, y, rr, 0, 2 * math.pi)
        cr.set_source_rgba(0.97, 0.87, 0.62, 0.96 * a)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, a)
        cr.set_line_width(5)
        cr.stroke()
        cr.arc(x, y, rr - 12, 0, 2 * math.pi)
        cr.set_source_rgba(0.85, 0.6, 0.15, a)
        cr.set_line_width(4)
        cr.stroke()
        prop(cr, "gp_cow", x - 0.08 * rr, y + 0.62 * rr, rr / 560, alpha=a)
    cr.restore()


def flight(cr, pts, p, a=1.0):
    """The soul's path through the air: pale-gold dots behind it."""
    dotted(cr, pts, p, 30, 6.5, (1.0, 0.86, 0.5), 0.9 * a)


def ripple(cr, t, t_hit, x, y, a=1.0):
    """The soul bouncing off: a pale ring spreading from where it touched, a glint."""
    u = (t - t_hit) / 0.6
    if not 0 < u < 1:
        return
    cr.save()
    cr.set_line_width(8 * (1 - u) + 2)
    cr.set_source_rgba(1.0, 0.92, 0.7, 0.85 * (1 - u) * a)
    pc.ell(cr, x, y, 40 + 200 * u, 14 + 60 * u)
    cr.stroke()
    cr.restore()
    sparkle(cr, x, y - 10, 60 * math.sin(math.pi * u) + 8, (1 - u) * a, (1.0, 0.97, 0.85))


def night_sky(cr, t, a, y1=1000):
    """A dark night over the cloth down to y1, with a few stars (the light still glows through in the middle)."""
    if a <= 0.01:
        return
    g = cairo.LinearGradient(0, 0, 0, y1)
    g.add_color_stop_rgba(0, 0.05, 0.05, 0.12, 0.0)
    g.add_color_stop_rgba(0.35, 0.10, 0.10, 0.22, 0.55 * a)
    g.add_color_stop_rgba(1, 0.10, 0.10, 0.22, 0.0)
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.rectangle(0, 0, W, y1)
    cr.set_source(g)
    cr.fill()
    cr.restore()
    stars(cr, t, 0.8 * a, ((140, 620), (330, 760), (900, 640), (760, 820), (980, 900), (220, 930)))


# ------------------------------------------------------------------ p1  hook: thumb-sized


TH1 = (770, 1590, 1.1)               # the thumb: x, wrist-bottom y, scale
SOUL1_X = 210
BODY1 = (540, 1690, 960)             # the new body in the hook: x, feet, height
ROW1 = (540, 1800, 1.45)             # the leaf of rice-balls: x, y, scale


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "p1")
    tA, tT, tS, tD, tP, tN = c["A"], c["T"], c["S"], c["D"], c["P"], c["N"]
    tx, ty, ts = TH1
    tip, base = ty - GC.THUMB_TIP * ts, ty - GC.THUMB_BASE * ts
    b, k, a = depth(t, -1.0, 0.1, t_out=tP, out_dur=0.5)
    if a > 0.01:
        glow(cr, tx - 60, (tip + ty) / 2, 520, 0.35 * a)
        bob = 0.07 * math.sin(math.pi * clamp((t - (tS + tD) / 2) / 0.5))       # a little thumbs-up nod
        prop(cr, "gp_thumb", tx, ty, ts * k, rot=sway(t, 0.008, 0.35) - bob, alpha=a, blur=b)
    left = tx - 170 * ts
    meas = prog(t, 0.45, 0.6) * a
    if meas > 0:
        for yy in (tip, base):
            dotted(cr, [(left - 10, yy), (SOUL1_X + 20, yy)], meas, 22, 5.0, RED, 0.9)
    # the soul: thumb-sized; when the new body forms it moves into its chest
    m = ease((t - tN) / 0.7) if t > tN else 0.0
    bx, bf, bh = BODY1
    sx = SOUL1_X + (bx - SOUL1_X) * m
    sh = (base - tip) * (1 - 0.66 * m)
    sf = base + (bf - 0.6 * bh + 0.5 * sh - base) * m
    shrink = 1 - 0.08 * math.sin(math.pi * clamp((t - tS) / 0.5))
    if t > tN - 0.05:
        parts = {kk: prog(t, tN + 0.09 * i, 0.35) for i, kk in enumerate(("feet", "knees", "thighs", "hips", "navel",
                                                                           "back", "heart", "neck", "head"))}
        light_body(cr, t, bx, bf, bh, parts, alpha=prog(t, tN - 0.05, 0.3))
    if tA < t < tA + 0.6:
        glow(cr, sx, sf - 0.55 * sh, 300, 0.6 * math.sin(math.pi * (t - tA) / 0.6))
    soul(cr, t, sx, sf, sh * shrink)
    if t > tS and t < tS + 0.6:
        lights(cr, t, sx, sf - 0.5 * sh, 120, 7, 0.8 * (1 - (t - tS) / 0.6))
    rx, ry, rs = ROW1
    rice_row(cr, t, rx, ry, rs, 10 * clamp((t - tP) / 0.8), t_in=tP - 0.1, ball=0.72)
    if t > tN:
        burst(cr, t, bx, bf - 0.55 * bh, tN + 0.5, n=16, rmax=520, alpha=0.6)
    dev_soul = cr.user_to_device(SOUL1_X, base + 48)
    dev_mid = cr.user_to_device((SOUL1_X + left) / 2 + 30, (tip + base) / 2)
    dev_th = cr.user_to_device(tx - 95 * ts, (tip + base) / 2)
    ring_a = a

    def ui(cr):
        if t < tP:
            head2(cr, t, "AFTER DEATH THE SOUL BECOMES", -1.0, "THUMB-SIZED", 0.3, big_size=230, ghost=-1.0, under=tT)
        else:
            head2(cr, t, "IN 10 DAYS, FROM RICE-BALLS:", tP - 0.1, "A NEW BODY", tN, big_size=250, under=tN + 0.5)
        plate(cr, t, tA, "THE SOUL", dev_soul[0], dev_soul[1], 30, t_out=tP)
        plate(cr, t, tT + 0.2, "SAME SIZE", dev_mid[0], dev_mid[1], 26, t_out=tP)
        if t > tT:
            red_ring(cr, dev_th[0], dev_th[1], 120, (base - tip) / 2 + 40, prog(t, tT + 0.05, 0.45), 9, ring_a)
        counter_badge(cr, t, tD, "10 DAYS", 250, 1330, 76, alpha=1 - prog(t, tP, 0.3))
    return dict(ui=ui, flash=flash_at(t, tT, 0.15) + flash_at(t, tN, 0.3))


# ------------------------------------------------------------------ p2  it's in the Garuda Purana


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "p2")
    tX, tG, tL = c["X"], c["G"], c["L"]
    leaves = [(None, [("GARUDA PURANA", 84, HEAD_FONT)], 0),
              (tL + 0.1, [([("PART 2:", INK), ("PRETA KALPA", RED)], 72, HEAD_FONT)], 0),
              (tL + 0.5, [("CHAPTERS 1-3", 44, MONO_FONT)], 0)]
    book(cr, t, 540, 940, 0.86, leaves, t_in=t0 + 0.05, t_open=tG, ring=(1, 0, 1, tL + 0.45))
    lng = lang(tl)

    def ui(cr):
        if t < tG:
            struck = t > tX + 0.25
            box = head2(cr, t, "THIS IS NOT A", t0 + 0.05, "FILM STORY", t0 + 0.35, big_size=210,
                        big_color=(0.42, 0.30, 0.20) if struck else INK)
            if box and t > tX:
                bx, by, bw, bh = box
                big_x(cr, W / 2, by + bh / 2, bw + 60, bh * 0.95, prog(t, tX, 0.3), lw=24)
        else:
            head2(cr, t, "IT'S WRITTEN IN THE", tG - 0.2, "GARUDA PURANA", tG + 0.06, big_size=200, under=tL + 0.3)
        script_strip(cr, t, tG + 0.35, TITLE[lng], 540, 1560, 64)
    return dict(ui=ui, flash=flash_at(t, tG, 0.25) + flash_at(t, tL, 0.2))


# ------------------------------------------------------------------ p3  the messengers at the door


COT3 = (420, 0.82)                   # the cot: x, scale
OLD3 = (470, 0.66)                   # the old man lying: hip x, scale
DOOR3 = (890, 0.8)                   # the doorway: x, scale
LAMP3 = (110, 0.95)                  # the clay lamp on the floor: x, scale


def doorway(cr, t, x, s, dark=1.0):
    """The doorway with the night outside it."""
    x0, x1 = x - 176 * s, x + 176 * s
    y0, y1 = G - 930 * s, G - 20 * s
    cr.save()
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.set_source_rgba(0.06, 0.06, 0.13, 0.82 * dark)
    cr.fill()
    cr.restore()
    for i, (px, py) in enumerate(((0.3, 0.15), (0.75, 0.3), (0.5, 0.5), (0.2, 0.62))):
        sparkle(cr, x0 + (x1 - x0) * px, y0 + (y1 - y0) * py, 9 + 3 * math.sin(t * 2 + i), 0.7 * dark,
                (0.95, 0.95, 1.0))
    prop(cr, "gp_doorway", x, G, s)


def s_door(cr, t, tl, t0, t1):
    c = cues(tl, "p3")
    tM, tY, tD, tA = c["M"], c["Y"], c["D"], c["A"]
    room_set(cr, t)
    dx_, ds = DOOR3
    doorway(cr, t, dx_, ds)
    dim = prog(t, tM, 0.8)
    # the messengers come out of the night: one in the doorway, one stepping in
    ba, ka, aa = depth(t, tY - 0.1, 0.9)
    if t > tY - 0.15:
        glow(cr, dx_, G - 520, 300, 0.25 * aa)
        duta(cr, t, dx_, 0.86 * ka, hold="noose", front=(-0.5, -0.6), alpha=aa, blur=ba, ph=0.3,
             hits=[(tA, 0.3)])
    if t > tD:
        bb, kb, ab = depth(t, tD, 0.6)
        step = ease((t - tD - 0.1) / max(0.8, tA - tD + 0.4))
        duta(cr, t, dx_ - 20 - 150 * step, 0.9 * kb, hold="staff", front=(-0.62, -0.55), alpha=ab, blur=bb,
             ph=0.9, hits=[(tA, 0.4)], rot=-0.03 * math.sin(math.pi * step))
    cx_, cs = COT3
    top = cot(cr, cx_, cs)
    lx, ls = LAMP3
    diya(cr, t, lx, G + 22, ls, lit=1 - 0.45 * dim)
    glow(cr, 260, top - 120, 360, 0.35 * (1 - 0.5 * dim))
    ox, os_ = OLD3
    old_man(cr, t, ox, top, os_, eyes="open" if t < tM + 0.35 else "shut",
            reach=keyed(t, [(t0, 0.6), (tM - 0.2, 0.0)], 0.6, 1.0))
    dev_tag = cr.user_to_device(700, 760)

    def ui(cr):
        if t < tD:
            head2(cr, t, "THE GARUDA PURANA SAYS:", t0 + 0.05, "AT DEATH...", tM, big_size=240)
        else:
            head2(cr, t, "THEN COME", tD - 0.15, "YAMA'S MESSENGERS", tD, big_size=200)
        plate(cr, t, tA, "YAMADUTAS", dev_tag[0], dev_tag[1], 30)
    return dict(ui=ui, night=0.14 + 0.16 * dim, lift=1.0, flash=flash_at(t, tD, 0.25))


# ------------------------------------------------------------------ p4  the soul is pulled out


COT4 = (520, 1.06)
OLD4 = (560, 0.8)
DU4 = (930, 0.84)                    # the messenger with the noose (facing left)
DA4 = (120, 0.84)                    # the other, with his staff (facing right)


def s_pull(cr, t, tl, t0, t1):
    c = cues(tl, "p4")
    tT, tP, tO, tC, tH = c["T"], c["P"], c["O"], c["C"], c["H"]
    room_set(cr, t)
    ax, as_ = DA4
    duta(cr, t, ax, as_, flip=False, hold="staff", front=(-0.6, -0.5), ph=0.2, alpha=0.95)
    cx_, cs = COT4
    top = cot(cr, cx_, cs, G + 30)
    diya(cr, t, 960, G + 40, 0.9)
    ox, os_ = OLD4
    empty = prog(t, tO, 0.9)
    op = old_man(cr, t, ox, top, os_, eyes="shut", alpha=1 - 0.85 * empty)
    chest = to_user(cr, op["chest"])
    lying_outline(cr, ox - 20, top - 120, 700, alpha=empty)
    # the soul drawn up out of the chest
    rise = ease((t - tP + 0.15) / max(0.9, tO - tP + 0.45))
    s0, s1 = (chest[0], chest[1] + 30), (560, 1180)
    sx = s0[0] + (s1[0] - s0[0]) * rise
    sf = s0[1] + (s1[1] - s0[1]) * rise - 90 * math.sin(math.pi * rise)
    sh = 70 + 120 * rise
    seen = prog(t, tT - 0.3, 0.5)
    glow(cr, chest[0], chest[1] - 20, 160, 0.6 * seen * (1 - rise))
    dx_, ds = DU4
    hy = G - 434 * ds
    aim = point_to(dx_, hy, ds, (sx, sf - 0.55 * sh), flip=True, bulk=1.12)
    pull = keyed(t, [(t0, 0.0), (tP, 1.0)], 0.35, 1.2)
    fr = mix((-0.4, -0.5), (aim[0] + 0.25 * rise, -0.25), pull)
    dp = duta(cr, t, dx_, ds, hold="none", front=fr, backa=(0.2, -0.6), ph=0.6, hits=[(tP, 0.3)])
    hand = to_user(cr, dp["handF"])
    if t > tT - 0.1:                                    # the noose of light
        la = prog(t, tT - 0.1, 0.4)
        wx, wy = sx, sf - 0.45 * sh
        mid = ((hand[0] + wx) / 2, min(hand[1], wy) - 60 + 40 * rise)
        light_rope(cr, [hand, mid, (wx + 0.18 * sh, wy)], la)
        noose_loop(cr, t, wx, wy, 0.2 * sh + 6, 0.07 * sh + 4, la)
    arms = "up" if t > tC else ("reach" if rise > 0.5 else "rest")
    soul(cr, t, sx, sf, sh * seen, a=seen, arms=arms, shiver=prog(t, tC, 0.2) * (1 - prog(t, tH + 1.2, 0.5)))
    lng = lang(tl)
    dev_body = cr.user_to_device(620, top - 285)

    def ui(cr):
        if t < tP:
            head2(cr, t, "THEY CATCH THE", t0 + 0.05, "THUMB-SIZED SOUL", tT, big_size=210)
        elif t < tC:
            head2(cr, t, "AND PULL IT", tP - 0.1, "OUT OF THE BODY", tP + 0.1, big_size=210, under=tO)
        else:
            head2(cr, t, "THE SOUL CRIES OUT:", tC - 0.1, None, 0.0)
        plate(cr, t, tO + 0.3, "HIS BODY", dev_body[0], dev_body[1], 30)
        cloud_text(cr, t, 330, 800, 0.72, [("OH! OH!", 120, RED, 0, tC + 0.15)], flip=True, t_in=tC - 0.15)
        script_strip(cr, t, min(tH, tC + 0.45), CRY[lng], 330, 575, 56)
    return dict(ui=ui, night=0.22, lift=1.0, flash=flash_at(t, tP, 0.2) + flash_at(t, tH, 0.15))


# ------------------------------------------------------------------ p5  before Yama, then back home


YM5 = (750, 0.84)                    # Yama's throne: x, scale
DU5 = (190, 0.84)                    # the messenger holding the soul (facing right)
SOUL5 = (450, 1330, 190)             # the soul before Yama: x, feet, height
HOUSE5 = (560, 0.82)                 # the house: x, scale


def s_yama(cr, t, tl, t0, t1):
    c = cues(tl, "p5")
    tY, tF, tC, tA, tH = c["Y"], c["F"], c["C"], c["A"], c["H"]
    aB = prog(t, tA + 0.15, 0.6)
    aA = 1 - aB
    door = (HOUSE5[0] + DV.DOOR_X * HOUSE5[1], G - 40)
    if aA > 0.01:                                       # Yama's hall
        prop(cr, "sb_yhall", 540, G + 8, 0.44, alpha=0.6 * aA, blur=5)
        ground(cr, alpha=aA)
        yx, ys = YM5
        glow(cr, yx, G - 560, 480, 0.4 * aA)
        aura(cr, t, yx - 20, G - 820, 120, 420, 0.22 * aA, n=16, spin=0.03, col=(0.95, 0.45, 0.25))
        order = keyed(t, [(t0, 0.0), (tC - 0.1, 1.0)], 0.3, 1.4)
        yp = yama_seated(cr, t, yx, G, ys, front=mix((-0.55, -0.85), (-2.2, -0.3), order), nod=nods(t, (tF,), 0.6),
                         alpha=aA, hits=[(tC, 0.4)])
        dx_, ds = DU5
        dp = duta(cr, t, dx_, ds, flip=False, hold="none", front=(-1.25, -0.2), alpha=aA, ph=0.4)
        hand = to_user(cr, dp["handF"])
        if t < tA:
            sx_, sf_, sh_ = SOUL5
            wx, wy = sx_, sf_ - 0.45 * sh_
            light_rope(cr, [hand, ((hand[0] + wx) / 2, wy + 30), (wx - 0.18 * sh_, wy)], aA * (1 - prog(t, tC, 0.4)))
            noose_loop(cr, t, wx, wy, 0.2 * sh_ + 6, 0.07 * sh_ + 4, aA * (1 - prog(t, tC, 0.4)))
        if t > tC:
            burst(cr, t, yx - 120, G - 900, tC, n=14, rmax=420, alpha=0.6 * aA)
        dev_y = yp["top"]
    else:
        dev_y = None
    if aB > 0.01:                                       # the house at night
        night_sky(cr, t, aB)
        hx, hs = HOUSE5
        prop(cr, "dv_house", hx, G + 6, hs, alpha=aB)
        ground(cr, alpha=aB)
        glow(cr, door[0], door[1] - 260, 300, 0.5 * aB)
    # the soul: before Yama, then up through the air and down at the door
    sx_, sf_, sh_ = SOUL5
    p0, p1, p2 = (sx_, sf_), (200, 380), (door[0], door[1] - 30)
    dur = max(1.3, tH - tA + 0.7)
    u = ease((t - tA + 0.1) / dur) if t > tA - 0.1 else 0.0
    pts = [bezier(p0, p1, p2, i / 60) for i in range(61)]
    if u > 0:
        flight(cr, pts, u, 1.0)
    px, py = bezier(p0, p1, p2, u)
    hgt = sh_ * (1 - 0.15 * math.sin(math.pi * u))
    soul(cr, t, px, py, hgt, arms="out" if 0 < u < 1 else "rest", shiver=0.0)
    if 0.98 < u and t < tH + dur:
        burst(cr, t, p2[0], p2[1] - 80, tA - 0.1 + dur, n=10, rmax=260, alpha=0.5)

    def ui(cr):
        if t < tC:
            head2(cr, t, "THE MESSENGERS TAKE IT TO", t0 + 0.05, "YAMA", tY, big_size=260)
        else:
            head2(cr, t, "BY YAMA'S ORDER, IT FLIES", tC - 0.1, "BACK HOME", tH, big_size=240, under=tH + 0.4)
        if dev_y is not None:
            tag(cr, t, tY + 0.2, "YAMA", dev_y[0] - 30, dev_y[1] - 150, 40, alpha=aA)
    return dict(ui=ui, night=0.08 + 0.26 * aB, lift=1.0, flash=flash_at(t, tY, 0.2) + flash_at(t, tC, 0.2))


# ------------------------------------------------------------------ p6  it can't go back in


COT6 = (500, 0.95)
BODY6 = (500, 700)                   # the empty body's centre x and length


def s_nobody(cr, t, tl, t0, t1):
    c = cues(tl, "p6")
    tW, tB, tN, tZ = c["W"], c["B"], c["N"], c["Z"]
    room_set(cr, t)
    cx_, cs = COT6
    top = cot(cr, cx_, cs)
    diya(cr, t, 900, G + 22, 0.95)
    bx, bl = BODY6
    by = top - 0.175 * bl - 6
    lying_outline(cr, bx, by, bl, alpha=1.0 - 0.3 * prog(t, tN, 0.6))
    target = (bx - 0.12 * bl, by)
    hover = (bx - 0.1 * bl, top - 420)
    dy = 0.0
    hits = []
    for td in (tW + 0.15, tB - 0.05):
        u = (t - td) / 0.85
        if 0 < u < 1:
            down = math.sin(math.pi * clamp(u / 0.55)) if u < 0.55 else 0.0
            up = -math.sin(math.pi * (u - 0.4) / 0.6) * 0.25 if u > 0.4 else 0.0
            dy = (target[1] - 60 - hover[1]) * max(0.0, down * (u < 0.42) + (u >= 0.42) * (1 - (u - 0.42) / 0.2)
                                                      * (u < 0.62)) + 160 * up
        hits.append(td + 0.42 * 0.85)
    sad = prog(t, tN, 0.5)
    sf = hover[1] + dy - 40 * sad + 8 * math.sin(t * 1.8)
    soul(cr, t, hover[0], sf, 175, arms="droop" if t > tN else ("reach" if dy > 20 else "rest"))
    for th in hits:
        ripple(cr, t, th, target[0], target[1] - 30)
    dev_b = cr.user_to_device(bx + 0.33 * bl, by - 170)
    dev_ring = cr.user_to_device(bx, by)

    def ui(cr):
        if t < tB:
            head2(cr, t, "IT TRIED TO GO BACK", t0 + 0.05, "INTO ITS BODY", tW, big_size=220)
        elif t < tN:
            head2(cr, t, "BUT IT", tB - 0.1, "COULDN'T", tB + 0.35, big_size=260)
        else:
            head2(cr, t, "NOW IT HAS", tN - 0.1, "NO BODY", tZ, big_size=260, under=tZ + 0.4)
        plate(cr, t, t0 + 0.2, "HIS BODY", dev_b[0], dev_b[1], 30)
        if t > tZ:
            red_ring(cr, dev_ring[0], dev_ring[1], 0.56 * bl, 170, prog(t, tZ + 0.05, 0.5), 9)
    return dict(ui=ui, night=0.2, lift=1.0, flash=sum(flash_at(t, th, 0.12) for th in hits))


# ------------------------------------------------------------------ p7  the son offers the rice-balls


SON7 = (190, 0.8)                    # the son kneeling: x, scale
LEAF7 = (505, G - 2, 0.72)           # the leaf: x, y, scale
LAMP7 = (700, 0.9)
BODY7 = (875, G - 40, 800)           # the new body (dotted for now): x, feet, height


def s_offer(cr, t, tl, t0, t1):
    c = cues(tl, "p7")
    tS, tD, tP, tE, tN = c["S"], c["D"], c["P"], c["E"], c["N"]
    room_set(cr, t, alpha=0.6)
    lx, ls = LAMP7
    diya(cr, t, lx, G + 18, ls)
    vx, vy, vs = LEAF7
    prop(cr, "gp_leaf", vx, vy, vs)
    sx_, ss = SON7
    hy = G - 250 * ss
    spot = (vx - 40, vy - 30)
    reach = reach_arm(sx_, hy, ss, 26 * 0.95, (spot[0], spot[1] - 20))
    give = keyed(t, [(t0, 0.0), (tP - 0.55, 1.0), (tP + 0.5, 0.0)], 0.4, 1.2)
    sp = fig(cr, GC.SON, "gp_son", t, sx_, ss, front=mix(ANJALI["front"], reach, give),
             backa=mix(ANJALI["backa"], (-0.2, -0.6), give), head=0.12 + 0.08 * give, feet=G,
             kneel="gp_son_kneel", swap={"gp_son_head": "gp_son_head"}, ph=0.5, hits=[(tS, 0.3)])
    hand = to_user(cr, sp["handF"])
    if t < tP:                                          # the rice-ball in his hand, then on the leaf
        if t > tS:
            pinda(cr, hand[0] + 8, hand[1] - 10, 0.62, alpha=prog(t, tS, 0.3))
    else:
        q = back(clamp((t - tP) / 0.3), 1.5)
        pinda(cr, spot[0], spot[1] - 6 * (1 - q), 0.62)
        glow(cr, spot[0], spot[1] - 20, 160, 0.5 * prog(t, tP, 0.3))
    bxx, bf, bh = BODY7
    ba = prog(t, tP + 0.3, 0.6)
    parts = {"head": 0.0}
    glow(cr, bxx, bf - 0.5 * bh, 460, 0.45 * ba)
    cen = light_body(cr, t, bxx, bf, bh, parts, alpha=ba)
    if t > tE:
        flow(cr, t, tE, tE + 1.2, (spot[0], spot[1] - 30), cen["back"], n=10, lift=260, dur=0.8)
    if t > tN - 0.2:
        q = prog(t, tN - 0.2, 0.6)
        soul(cr, t, bxx, bf - 0.6 * bh + 50, 95, a=q, halo=0.8)
    dev_son = sp["top"]
    dev_ball = cr.user_to_device(spot[0], spot[1] + 80)

    def ui(cr):
        if t < tP:
            head2(cr, t, "THEN, FOR 10 DAYS,", t0 + 0.05, "HIS SON", tS, big_size=250)
        elif t < tE:
            head2(cr, t, "OFFERS", tP - 0.1, "RICE-BALLS", tP, big_size=250)
        else:
            head2(cr, t, "EACH RICE-BALL MAKES", tE - 0.1, "A NEW BODY PART", tN, big_size=210, under=tN + 0.4)
        card2(cr, t, tD - 0.2, 540, 790, 0.6, [("10 DAYS,", 96, INK, -54, tD), ("10 RICE-BALLS", 92, RED, 52, tP)])
        tag(cr, t, tS + 0.2, "HIS SON", dev_son[0], dev_son[1] - 70, 34)
        plate(cr, t, tP + 0.3, "RICE-BALL", dev_ball[0], dev_ball[1], 26)
    return dict(ui=ui, night=0.1, lift=1.0, flash=flash_at(t, tP, 0.2) + flash_at(t, tN, 0.15))


# ------------------------------------------------------------------ p8 - p10  the new body, day by day


BODY8 = (610, 1650, 960)             # x, feet, height
ROW8 = (540, 1815, 1.45)
PART_CUES = (("p8", "H1"), ("p8", "H2"), ("p8", "H3"), ("p8", "H4"), ("p9", "N"), ("p9", "Hp"), ("p9", "Th"),
             ("p9", "K"), ("p9", "F"))
DAY_CUES = (("p8", "D1"), ("p8", "D2"), ("p8", "D3"), ("p8", "D4"), ("p9", "t0"), ("p9", "Hp"), ("p9", "Th"),
            ("p9", "K"), ("p9", "F"), ("p10", "D"))


def days(tl):
    """(day start times, part times) for the ten days (cached on the timeline)."""
    d = getattr(tl, "_gp_days", None)
    if d is None:
        d = ([cues(tl, b)[k] for b, k in DAY_CUES], [cues(tl, b)[k] for b, k in PART_CUES])
        tl._gp_days = d
    return d


def body_days(cr, t, tl, t0, t1, bright=0.0, hands=None):
    """The shared set of p8-p10: the body forming, the rice-balls on the leaf, the DAY n tag on the newest part."""
    dstart, ptime = days(tl)
    x, feet, h = BODY8
    glow(cr, x, feet - 0.5 * h, 640, 0.3)
    parts = {k: prog(t, tp, 0.55) for k, tp in zip(BODY_PARTS, ptime)}
    cen = light_body(cr, t, x, feet, h, parts, hands=hands, bright=bright)
    soul(cr, t, x - 0.05 * h, feet - 0.6 * h + 44, 84, halo=0.7)
    n = sum(1 for ts in dstart if t >= ts - 0.05)
    last = max([i for i, ts in enumerate(dstart) if t >= ts - 0.05], default=-1)
    rx, ry, rs = ROW8
    nb = last + clamp((t - dstart[last]) / 0.35) if last >= 0 else 0.0
    rice_row(cr, t, rx, ry, rs, nb, ball=0.72)
    return cen, n, last, dstart, ptime


def day_tag(cr, t, t_in, text, part_xy, t_out=None):
    """A DAY n plate at the left with a dotted pointer to the part that day makes."""
    if part_xy is None:
        return
    a = prog(t, t_in, 0.3) * (1 - (prog(t, t_out, 0.25) if t_out is not None else 0.0))
    if a <= 0.01:
        return
    px, py = part_xy
    y = clamp(py, 700, 1600)
    dotted(cr, [(250, y), (px - 40, py)], prog(t, t_in + 0.1, 0.4), 18, 4.5, RED, 0.9 * a)
    plate(cr, t, t_in, text, 170, y, 34, color=RED, alpha=a)


def body_ui(cr, t, cen, last, dstart, ptime, t_next):
    if last < 0:
        return
    day = last + 1
    tp = ptime[last] if last < len(ptime) else dstart[last] + 0.6
    big = DAY_LABEL[last]
    head2(cr, t, f"DAY {day}:", dstart[last] - 0.05, big, min(tp, dstart[last] + 0.3),
          big_size=230 if len(big) < 10 else 170)
    if last < len(BODY_PARTS):
        dev = cr.user_to_device(*cen[BODY_PARTS[last]])
        day_tag(cr, t, tp - 0.1, f"DAY {day}", dev, t_out=t_next)


def s_days(cr, t, tl, t0, t1):
    cen, n, last, dstart, ptime = body_days(cr, t, tl, t0, t1)
    t_next = dstart[last + 1] - 0.15 if 0 <= last < len(dstart) - 1 else None

    def ui(cr):
        body_ui(cr, t, cen, last, dstart, ptime, t_next)
    fl = sum(flash_at(t, tp, 0.12) for tp in ptime)
    return dict(ui=ui, night=0.06, flash=fl)


def s_day10(cr, t, tl, t0, t1):
    c = cues(tl, "p10")
    tD, tHu, tTh = c["D"], c["Hu"], c["Th"]
    x, feet, h = BODY8
    belly, throat = (x - 0.03 * h, feet - 0.53 * h), (x + 0.02 * h, feet - 0.795 * h)
    rest_l, rest_r = (x - 0.215 * h, feet - 0.41 * h), (x + 0.215 * h, feet - 0.41 * h)
    ql = keyed(t, [(t0, 0.0), (tHu - 0.1, 1.0)], 0.35, 1.3)
    qr = keyed(t, [(t0, 0.0), (tTh - 0.1, 1.0)], 0.35, 1.3)
    hands = {"L": mix(rest_l, belly, ql), "R": mix(rest_r, throat, qr)}
    cen, n, last, dstart, ptime = body_days(cr, t, tl, t0, t1, bright=prog(t, tD, 0.5), hands=hands)
    if t > tD:
        burst(cr, t, x, feet - 0.55 * h, tD + 0.1, n=18, rmax=640, alpha=0.6)
    dev_b = cr.user_to_device(*belly)
    dev_t = cr.user_to_device(*throat)

    def ui(cr):
        head2(cr, t, "DAY 10:", tD - 0.05, "HUNGER & THIRST", tHu, big_size=200, under=tTh + 0.3)
        if t > tHu + 0.2:
            red_ring(cr, dev_b[0], dev_b[1], 120, 80, prog(t, tHu + 0.2, 0.45), 8)
        if t > tTh + 0.2:
            red_ring(cr, dev_t[0], dev_t[1], 95, 70, prog(t, tTh + 0.2, 0.45), 8)
    return dict(ui=ui, night=0.06, flash=flash_at(t, tD, 0.25) + flash_at(t, tHu, 0.12))


# ------------------------------------------------------------------ p11  the long road


def road_pt(u):
    """The road to Yama's city: centre x, y and width at u (0 near .. 1 far)."""
    y = 700 + 1130 * (1 - u) ** 1.35
    x = 540 + 260 * math.sin(2.2 * math.pi * u + 0.4) * (1 - u) ** 0.8
    return x, y, 30 + 400 * (1 - u) ** 1.3


def road(cr, p=1.0, a=1.0, col=(0.74, 0.55, 0.32)):
    """The winding road drawn from the near end to fraction p of its length, dotted at the edges."""
    if a <= 0.01 or p <= 0:
        return
    us = [p * i / 80 for i in range(81)]
    L_ = [(road_pt(u)[0] - road_pt(u)[2] / 2, road_pt(u)[1]) for u in us]
    R_ = [(road_pt(u)[0] + road_pt(u)[2] / 2, road_pt(u)[1]) for u in us]
    cr.save()
    pc.poly(cr, L_ + R_[::-1])
    cr.set_source_rgba(*col, 0.85 * a)
    cr.fill()
    cr.restore()
    for edge in (L_, R_):
        dotted(cr, edge, 1.0, 20, 4.0, (0.36, 0.22, 0.10), 0.8 * a)


GATES = [0.12 + 0.052 * k for k in range(16)]


def gates(cr, t, t_in, a=1.0, step=0.07):
    """Sixteen small city gates along the road, alternating sides, popping in from near to far."""
    for k in reversed(range(16)):
        q = back(clamp((t - t_in - step * k) / 0.3), 1.8)
        if q <= 0.01:
            continue
        u = GATES[k]
        x, y, w = road_pt(u)
        s = 0.22 * (1 - u) ** 1.2 + 0.03
        sg = -1 if k % 2 == 0 else 1
        prop(cr, "gp_gate", x + sg * (w / 2 + 330 * s), y + 4, s * q, alpha=clamp(q) * a)


def s_road(cr, t, tl, t0, t1):
    c = cues(tl, "p11")
    tY, tK, tS, tYr = c["Y"], c["K"], c["S"], c["Yr"]
    night_sky(cr, t, 1.0, 1100)
    fx, fy, _ = road_pt(1.0)
    glow(cr, fx, fy - 60, 260, 0.6)
    aura(cr, t, fx, fy - 70, 50, 200, 0.3, n=14, spin=0.03, col=(0.95, 0.45, 0.25))
    prop(cr, "sb_door", fx, fy + 6, 0.13, alpha=prog(t, tY - 0.2, 0.5))
    road(cr, prog(t, t0, 1.4))
    gates(cr, t, tS - 0.2)
    u = 0.02 + 0.05 * clamp((t - t0) / max(1.0, t1 - t0))
    x, y, w = road_pt(u)
    soul(cr, t, x, y - 20, 160, arms="rest", walk=t * 5.0)

    def ui(cr):
        head2(cr, t, "THEN BEGINS THE JOURNEY TO", t0 + 0.05, "YAMA'S CITY", tY, big_size=240, under=tY + 0.5)
        counter_badge(cr, t, tK, "86,000 YOJANAS", 760, 1000, 62)
        counter_badge(cr, t, tS + 16 * 0.07, "16 CITIES", 790, 1180, 62)
        counter_badge(cr, t, tYr, "~1 YEAR", 250, 1380, 62)
    return dict(ui=ui, night=0.3, lift=1.0, flash=flash_at(t, tY, 0.2) + flash_at(t, tS + 1.1, 0.12))


# ------------------------------------------------------------------ p12  no food, no water; the monthly rice-ball


def cracks(cr, a=1.0):
    """Dry, cracked earth over the floor."""
    cr.save()
    cr.set_source_rgba(0.36, 0.22, 0.10, 0.7 * a)
    cr.set_line_width(3)
    for i in range(14):
        x0 = 40 + 75 * i
        y0 = G + 30 + 40 * ((i * 0.618) % 1.0)
        pts = [(x0, y0), (x0 + 30, y0 + 22), (x0 + 22, y0 + 60), (x0 + 50, y0 + 90)]
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
        cr.move_to(x0 + 30, y0 + 22)
        cr.line_to(x0 + 70, y0 + 16)
        cr.stroke()
    cr.restore()


def s_dry(cr, t, tl, t0, t1):
    c = cues(tl, "p12")
    tW, tF, tP, tM = c["W"], c["F"], c["P"], c["M"]
    tL = min(tP, tM) - 0.1
    warm(cr, 170, 760, 260, 0.6, (1.0, 0.6, 0.2))
    prop(cr, "sun", 170, 760, 0.28, rot=t * 0.2)
    prop(cr, "gp_deadtree", 935, G + 10, 0.95, rot=sway(t, 0.004, 0.3))
    ground(cr)
    cracks(cr)
    sx, sh = 540, 300
    drops = (tL, max(tM, tL + 2.2))                     # a rice-ball each month: two come down while we watch
    fed, catching = 0.0, False
    for td in drops:
        if t < td:
            continue
        arr = clamp((t - td) / 1.0)
        gone = prog(t, td + 1.4, 0.4)
        fed += gone
        catching = catching or (0.5 < arr and gone < 1)
        if gone >= 1:
            if t < td + 2.2:
                burst(cr, t, sx, G - 10 - 0.6 * sh, td + 1.4, n=14, rmax=380, alpha=0.7)
            continue
        by = 600 + (G - 10 - 1.05 * sh - 600) * ease(arr)
        light_rope(cr, [(sx, 540), (sx + 6, (540 + by) / 2), (sx, by - 34)], prog(t, td, 0.3) * (1 - gone))
        glow(cr, sx, by, 150, 0.6 * (1 - gone))
        pinda(cr, sx, by, 0.85 * (1 - 0.5 * gone), alpha=1 - gone)
    soul(cr, t, sx, G - 10, sh, arms="reach" if catching else ("rest" if fed > 0 else "droop"),
         walk=None if catching else t * 4.0, halo=0.6 + 0.4 * min(1.0, fed))
    for tt, name, x, y, s in ((tW, "md_kalasha", 330, 1060, 0.42), (tF, "dv_bowl", 750, 1020, 0.9)):
        q = back(clamp((t - tt + 0.15) / 0.35), 1.5)
        if q > 0:
            prop(cr, name, x, y + 40 * (1 - q), s * (0.7 + 0.3 * q), alpha=clamp(q) * (1 - 0.5 * prog(t, tL, 0.5)))
    dev_ball = cr.user_to_device(sx + 190, 780)

    def ui(cr):
        if t < tL:
            head2(cr, t, "ON THE ROAD:", t0 + 0.05, "NO FOOD, NO WATER", tW, big_size=200)
        else:
            head2(cr, t, "ITS ONLY FOOD:", tL - 0.1, "A RICE-BALL A MONTH", tL + 0.1, big_size=190, under=tM + 0.3)
        for tt, x, y, w_, h_ in ((tW, 330, 960, 220, 220), (tF, 750, 975, 240, 150)):
            if t > tt + 0.15:
                big_x(cr, x, y, w_, h_, prog(t, tt + 0.15, 0.3), alpha=1 - 0.5 * prog(t, tL, 0.5), lw=16)
        plate(cr, t, tM, "EVERY MONTH", dev_ball[0], dev_ball[1], 32)
    return dict(ui=ui, eve=0.22, flash=sum(flash_at(t, td + 1.4, 0.15) for td in drops))


# ------------------------------------------------------------------ p13  the Vaitarani


WHIRLS = ((300, 0.3, 120), (790, 0.15, 90), (600, 0.55, 150), (900, 0.75, 130), (180, 0.82, 120))


def river(cr, t, top, bottom, a=1.0, speed=1.0, whirl=1.0):
    """The Vaitarani: a wide river of dark-red water (never gore) from y=top (far bank) to y=bottom (near bank): a few
    rows of slow leather waves, smaller far away, and turning whirlpools."""
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    g = cairo.LinearGradient(0, top, 0, bottom)
    g.add_color_stop_rgba(0, 0.72, 0.34, 0.32, a)
    g.add_color_stop_rgba(1, 0.86, 0.40, 0.34, a)
    cr.rectangle(0, top, W, bottom - top)
    cr.set_source(g)
    cr.fill()
    cr.restore()
    n = 7
    for k in range(n):
        v = k / (n - 1)
        y = top + 30 + (bottom - top - 60) * v ** 1.2
        s = 0.34 + 0.4 * v
        per = 2080 * s
        off = (t * (20 + 36 * v) * speed * (1 if k % 2 else -1)) % (160 * s)
        for xx in (540 + off - per, 540 + off, 540 + off + per):
            prop(cr, "gp_rwaveA" if k % 2 == 0 else "gp_rwaveB", xx, y, s, alpha=0.75 * a)
    for i, (x, v, r) in enumerate(WHIRLS):
        y = top + 30 + (bottom - top - 60) * v ** 1.2 - 40
        sc = 0.5 + 0.6 * v
        spin = -t * (0.8 + 0.25 * i) * speed
        cr.save()
        cr.translate(x, y)
        cr.scale(1.0, 0.4)
        for lw, col, al in ((14, (0.25, 0.04, 0.04), 0.5), (7, (1.0, 0.62, 0.48), 0.9)):
            cr.new_path()
            for j in range(90):
                q = j / 89
                ang = spin + q * 3.6 * math.pi
                rr = r * sc * (0.1 + q)
                (cr.move_to if j == 0 else cr.line_to)(rr * math.cos(ang), rr * math.sin(ang))
            cr.set_source_rgba(*col, al * a * whirl)
            cr.set_line_width(lw)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.stroke()
        cr.restore()


def banks(cr, t, top, bottom, door_x=820, a=1.0):
    """The far bank (Yama's door small on it) and the near bank."""
    glow(cr, door_x, top - 40, 160, 0.4 * a)
    prop(cr, "sb_door", door_x, top + 4, 0.1, alpha=0.8 * a, blur=1.5)
    prop(cr, "ground", W / 2, top + 8, 0.82, alpha=0.7 * a, blur=1.5)
    cr.save()
    cr.rectangle(0, bottom, W, H - bottom)
    cr.set_source_rgba(0.62, 0.44, 0.26, 0.6 * a)
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.fill()
    cr.restore()
    prop(cr, "ground", W / 2, bottom + 4, 0.82, alpha=a)


def arrow_v(cr, x, y0, y1, p, a=1.0):
    """A pale double-headed measuring arrow from y0 to y1 (drawn out from the middle, p 0..1), inked."""
    if p <= 0:
        return
    ym = (y0 + y1) / 2
    ya, yb = ym + (y0 - ym) * p, ym + (y1 - ym) * p
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, col in ((16, pc.INK), (8, (1.0, 0.9, 0.62))):
        cr.set_source_rgba(*col, a)
        cr.set_line_width(lw)
        cr.move_to(x, ya + 20)
        cr.line_to(x, yb - 20)
        cr.stroke()
    for yy, sg in ((ya, -1), (yb, 1)):
        pc.poly(cr, [(x, yy + sg * 14), (x - 30, yy - sg * 30), (x + 30, yy - sg * 30)])
        cr.set_source_rgba(1.0, 0.9, 0.62, a)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, a)
        cr.set_line_width(4)
        cr.stroke()
    cr.restore()


RV13 = (820, 1700)                   # the river: far bank y, near bank y


def s_river(cr, t, tl, t0, t1):
    c = cues(tl, "p13")
    tV, tC, tN, tB = c["V"], c["C"], c["N"], c["B"]
    top, bottom = RV13
    night_sky(cr, t, 1.0, top + 40)
    river(cr, t, top, bottom, speed=1.0 + 0.8 * prog(t, tB, 0.6), whirl=0.6 + 0.4 * prog(t, tV, 0.5))
    banks(cr, t, top, bottom)
    soul(cr, t, 330, 1870, 200, arms="rest" if t < tN else "droop")
    arrow_v(cr, 860, top + 30, bottom - 10, prog(t, tC, 0.6))
    dev_m = cr.user_to_device(860, (top + bottom) / 2)

    def ui(cr):
        if t < tC:
            head2(cr, t, "AND HALF-WAY COMES THE RIVER", t0 + 0.05, "VAITARANI", tV, big_size=250)
        else:
            head2(cr, t, "THE VAITARANI:", tC - 0.1, "100 YOJANAS WIDE", tC + 0.05, big_size=200, under=tC + 0.5)
        plate(cr, t, tC + 0.4, "100 YOJANAS", dev_m[0] - 40, dev_m[1], 36)
        plate(cr, t, tN, "NOT WATER...", 380, 1130, 42)
    return dict(ui=ui, night=0.22, lift=1.0, flash=flash_at(t, tV, 0.3) + flash_at(t, tC, 0.15))


# ------------------------------------------------------------------ p14  the boat, only for the cow-givers


RV14 = (820, 1460)
SA14 = (230, 1850, 200)              # the soul who gave a cow: x, feet, height
SB14 = (870, 1850, 200)              # the soul who did not
DOCK14 = (550, 0.5)                  # where the ferry stops at the near bank: x, scale


def s_boat(cr, t, tl, t0, t1):
    c = cues(tl, "p14")
    tB, tO, tC, tG = c["B"], c["O"], c["C"], c["G"]
    top, bottom = RV14
    night_sky(cr, t, 1.0, top + 40)
    river(cr, t, top, bottom, whirl=0.7)
    banks(cr, t, top, bottom, door_x=760)
    # the ferry crosses from far left to the near bank, waits, and leaves with the cow-giver
    arrive = max(tB + 1.7, tC - 0.1)
    u = ease((t - tB + 0.2) / (arrive - tB + 0.2)) if t > tB - 0.2 else 0.0
    t_go = tG + 1.1
    w = ease((t - t_go) / 1.6) if t > t_go else 0.0
    kx, ks = DOCK14
    bx = -300 + (kx + 300) * u + 760 * w
    by = 960 + (bottom - 30 - 960) * u - 320 * w
    bs = 0.32 + (ks - 0.32) * u - 0.14 * w
    if t > tB - 0.25:
        bob = 6 * math.sin(t * 2.2)
        glow(cr, bx, by - 80 * bs, 520 * bs + 100, 0.5)
        warm(cr, bx + 470 * bs, by - 200 * bs, 160 * bs + 40, 0.7)
        prop(cr, "flame1" if math.sin(t * 9) > 0 else "flame2", bx + 470 * bs, by - 170 * bs, 0.3 * bs)
        ang = man_angles("dv_hus", t, (-1.6, -0.9), (-1.2, -1.2), 0.0, (0.0, 0.0), (), 0.8)
        ex = {"dv_hus_armF_lo": held_grip("gp_pole", (-1.6, -0.9), 1.0, 0.25 + 0.06 * math.sin(t * 1.6), 150)}
        puppet(cr, DV.HUS, bx - 200 * bs, by + bob - 120 * bs - 434 * bs * 0.9, bs * 0.9,
               bob_rot(t, 0.8), False, ang, swap={"dv_hus_head": "dv_hus_head_smile"}, extra=ex, rods=False)
        prop(cr, "gp_boat", bx, by + bob, bs, rot=0.02 * math.sin(t * 1.3))
    ax, af, ah = SA14
    board = ease((t - tG) / 0.8) if t > tG else 0.0
    sx = ax + (bx + 120 * bs - ax) * board
    sf = af + (by - 60 * bs - af) * board
    if w > 0:
        sx, sf = bx + 120 * bs, by - 60 * bs
    soul(cr, t, sx, sf, ah * (1 - 0.3 * board), arms="reach" if t > tC and board < 1 else "rest")
    ox, of, oh = SB14
    soul(cr, t, ox, of, oh, arms="droop" if t > tG else "rest", halo=0.7)
    dev_a = cr.user_to_device(ax, af - ah - 150)
    dev_b = cr.user_to_device(ox, of - oh - 150)

    def ui(cr):
        if t < tO:
            head2(cr, t, "TO CROSS IT,", t0 + 0.05, "A BOAT COMES", tB, big_size=240)
        else:
            head2(cr, t, "BUT ONLY FOR THOSE WHO", tO - 0.1, "GAVE A COW", tC, big_size=250, under=tG + 0.2)
        cow_badge(cr, t, tO + 0.2, dev_a[0], dev_a[1], 100, alpha=1 - 0.6 * board)
        cow_badge(cr, t, tO + 0.45, dev_b[0], dev_b[1], 100, empty=True)
        if t > tC:
            red_ring(cr, dev_a[0], dev_a[1], 150, 140, prog(t, tC + 0.05, 0.45), 9, 1 - 0.6 * board)
    return dict(ui=ui, night=0.22, lift=1.0, flash=flash_at(t, tB, 0.15) + flash_at(t, tC, 0.2))


# ------------------------------------------------------------------ p15  Chitragupta's account, Yama's judgement


YM15 = (862, 0.74)
CG15 = (165, 0.84)
ROWS15 = (True, True, False, True, False, True, True, False, True)


def scroll(cr, t, x, y, w, length, alpha=1.0):
    """Chitragupta's scroll of deeds hanging from its top roller at (x, y): DEEDS, then rows of a green tick (good) or
    a red cross (bad) with lines of writing, as far as it has unrolled; the bottom roller at its end."""
    cr.save()
    pc.poly(cr, [(x - w / 2, y), (x + w / 2, y), (x + w / 2, y + length), (x - w / 2, y + length)])
    cr.set_source_rgba(0.98, 0.90, 0.68, 0.97 * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, alpha)
    cr.set_line_width(4)
    cr.stroke()
    draw_text(cr, "DEEDS", x, y + 34, 34, INK, alpha * clamp((length - 60) / 40), MONO_FONT, "cm", tracking=4)
    for i, good in enumerate(ROWS15):
        ry = y + 92 + 56 * i
        if ry + 30 > y + length:
            break
        if good:
            tick(cr, x - w / 2 + 22, ry, 36, 1.0, color=(0.16, 0.50, 0.24), alpha=alpha)
        else:
            cross(cr, x - w / 2 + 40, ry, 30, 1.0, alpha=alpha)
        cr.set_source_rgba(*pc.INK, 0.55 * alpha)
        cr.set_line_width(3)
        cr.move_to(x - w / 2 + 76, ry)
        for j in range(12):
            cr.line_to(x - w / 2 + 76 + (w - 100) * (j + 1) / 12, ry + 5 * math.sin(j * 2.1 + i))
        cr.stroke()
    for yy in (y, y + length):                          # the rollers
        pc.poly(cr, [(x - w / 2 - 20, yy - 12), (x + w / 2 + 20, yy - 12), (x + w / 2 + 20, yy + 12),
                     (x - w / 2 - 20, yy + 12)])
        cr.set_source_rgba(0.56, 0.33, 0.15, alpha)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, alpha)
        cr.stroke()
        for sx in (-1, 1):
            cr.arc(x + sx * (w / 2 + 28), yy, 14, 0, 2 * math.pi)
            cr.set_source_rgba(1.0, 0.82, 0.3, alpha)
            cr.fill_preserve()
            cr.set_source_rgba(*pc.INK, alpha)
            cr.stroke()
    cr.restore()


def s_judge(cr, t, tl, t0, t1):
    c = cues(tl, "p15")
    tC, tA, tY, tJ = c["C"], c["A"], c["Y"], c["J"]
    prop(cr, "sb_yhall", 540, G + 8, 0.46, alpha=0.6, blur=5)
    ground(cr)
    yx, ys = YM15
    glow(cr, yx, G - 560, 460, 0.4)
    raise_ = keyed(t, [(t0, 0.0), (tY - 0.1, 1.0)], 0.35, 1.3)
    thump = keyed(t, [(t0, 0.0), (tJ - 0.05, 1.0)], 0.15, 1.8)
    store = {}
    yp = yama_seated(cr, t, yx, G, ys, front=mix((-0.55, -0.85), (-2.35, -0.25), raise_), grip=120 + 120 * raise_,
                     head=-0.05 * raise_ + 0.06 * thump, hits=[(tJ, 0.5)], store=store)
    cx_, cs = CG15
    hold = keyed(t, [(t0, 0.0), (tA - 0.6, 1.0)], 0.35, 1.2)
    cp = fig(cr, GC.CHITRA, "gp_chitra", t, cx_, cs, front=mix((-0.4, -0.5), (-1.1, -0.45), hold),
             backa=mix((0.3, -0.3), (-1.0, -0.6), hold), feet=G, head=0.06 * hold, ph=0.3, hits=[(tC, 0.3)])
    hand = to_user(cr, cp["handF"])
    unroll = ease((t - tA + 0.35) / 1.6) if t > tA - 0.35 else 0.0
    if hold > 0.05:
        scroll(cr, t, hand[0] + 30, hand[1] - 4, 240, 60 + 560 * unroll, alpha=clamp(hold * 1.5))
    soul(cr, t, 615, 1100 + 10 * math.sin(t * 1.6), 150, arms="rest" if t < tJ else "droop", halo=0.8)
    if t > tJ and "top" in store:
        top = to_user(cr, store["top"])
        burst(cr, t, top[0], top[1], tJ, n=16, rmax=420, alpha=0.7)
    dev_c, dev_y = cp["top"], yp["top"]

    def ui(cr):
        if t < tY:
            head2(cr, t, "CHITRAGUPTA READS EVERY DEED:", t0 + 0.05, "THE ACCOUNT", tA, big_size=240)
        else:
            head2(cr, t, "AND YAMA GIVES HIS", tY - 0.1, "JUDGEMENT", tJ, big_size=250, under=tJ + 0.4)
        tag(cr, t, tC + 0.15, "CHITRAGUPTA", dev_c[0], dev_c[1] - 60, 30)
        tag(cr, t, tY + 0.1, "YAMA", dev_y[0] - 30, dev_y[1] - 150, 40)
    return dict(ui=ui, night=0.1, lift=1.0, flash=flash_at(t, tA, 0.12) + flash_at(t, tJ, 0.35))


# ------------------------------------------------------------------ p16  do you believe it?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "p16")
    tJ, tQ, tY, tC = c["J"], c["Q"], c["Y"], c["C"]
    ground(cr, alpha=0.6)
    trail = [bezier((90, 1900), (200, 1480), (540, 1470), i / 50) for i in range(51)]
    flight(cr, trail, prog(t, t0, 1.2), 0.7)
    glow(cr, 540, 1300, 480, 0.4)
    soul(cr, t, 540, 1460 + 8 * math.sin(t * 1.5), 240, arms="rest", halo=1.2)
    cards = ((300, "BELIEVE?", tQ + 0.1), (780, "DON'T?", tQ + 0.3))

    def ui(cr):
        if t < tQ:
            head2(cr, t, "THE GARUDA PURANA SAYS:", t0 + 0.05, "THIS IS THE JOURNEY", tJ, big_size=200)
        else:
            head2(cr, t, "DO YOU", tQ - 0.1, "BELIEVE IT?", tQ + 0.05, big_size=250)
        for cx, txt, tc in cards:
            card(cr, t, tc - 0.25, cx, 780, 0.58, [(txt, 112, RED, 4)])
        if t > tY:
            n = int((t - tY) / 0.9)
            k = n % 2
            red_ring(cr, cards[k][0], 784, 236, 96, prog(t, tY + 0.9 * n, 0.35), 9)
    return dict(ui=ui, night=0.12, lift=1.0, flash=flash_at(t, tQ, 0.15))


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options); "cont" = same set, no lamp dip
    ("p1", None, s_hook, {"z": (1.0, 1.03)}),
    ("p2", None, s_book, {"z": (1.0, 1.03)}),
    ("p3", None, s_door, {"z": (1.0, 1.04)}),
    ("p4", None, s_pull, {"z": (1.0, 1.05), "focus": (540, 1300)}),
    ("p5", None, s_yama, {"z": (1.0, 1.03)}),
    ("p6", None, s_nobody, {"z": (1.0, 1.04), "focus": (540, 1400)}),
    ("p7", None, s_offer, {"z": (1.0, 1.03)}),
    ("p8", None, s_days, {"z": (1.0, 1.02)}),
    ("p9", None, s_days, {"z": (1.02, 1.04), "cont": True}),
    ("p10", None, s_day10, {"z": (1.04, 1.06), "cont": True}),
    ("p11", None, s_road, {"z": (1.0, 1.04), "focus": (540, 1500)}),
    ("p12", None, s_dry, {"z": (1.0, 1.03)}),
    ("p13", None, s_river, {"z": (1.0, 1.04)}),
    ("p14", None, s_boat, {"z": (1.0, 1.03)}),
    ("p15", None, s_judge, {"z": (1.0, 1.03)}),
    ("p16", None, s_end, {"z": (1.0, 1.03)}),
]


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl, SHOTS)
    _, _, fn, opt = SHOTS[k]
    z0, z1 = opt.get("z", (1.0, 1.05))                  # "cont" shots pick up the push where the last one ended
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
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22 and not opt.get("cont"):     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a conch
    as the messengers appear, a bell at the son's rice-ball, a single hit at the river, shimmer on the closing question,
    then (only where it fits) shimmer as the soul flies home. Chosen in THAT order of importance, each at least
    SFX_MIN_GAP from every sound already kept (as render_myth.calm_sfx keeps them), so the list returned is what plays
    (6 sounds); the bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["p3"]["D"], "conch", 0), (c["p7"]["P"], "bell", 0), (c["p13"]["V"], "hit", 0),
            (c["p16"]["Q"], "shimmer", 0), (c["p5"]["A"], "shimmer", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["p3"]["D"] - 0.3, "dip", 0.5), (c["p13"]["V"] - 0.3, "dip", 0.45), (c["p16"]["Q"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
