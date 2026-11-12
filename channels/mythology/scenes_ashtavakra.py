"""Scenes for videos/ashtavakra.py: "An unborn baby corrected his father from the womb" (Mahabharata, Vana Parva
132-134), in Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen,
two-tier headlines and rod-puppet motion as the Shani, Garuda Purana, Dharmavyadha and Ruru reels, with the cast from
ashtavakra_cast. Made for the 5-year-old script (12 Nov 2026: "so clear ... even a 5 year old can understand"): every
line has a shot that shows exactly what is said, in order; one idea on screen at a time; the one acting is big; short
English headlines; names only where the narration says them (the father is FATHER, the mother MOTHER, the king THE
KING, the scholar the PROUD PANDIT, Varuna only "the water god"). Two devices carry the story: THE WOMB WINDOW (a soft
rose-gold oval of light over the mother's belly with the tiny child curled inside, who opens his eyes, speaks and
points) and THE WATER (the lake by the palace, blue light, where the loser goes and from which the father comes back).

Respect: the father is a learned guru whose pride is hurt, never a villain; the mother is calm and dignified; the boy's
crooked body is drawn plainly and with dignity (a rounded back, a bent knee, a turned wrist, a staff) and his face is
always bright and sure; the king is wise; the pandit is proud, then honest. No gore at all: the curse is a crackle of
light that stops at the window's rim; the father bows, folds his hands and sinks gently into blue light with his eyes
closed (no struggle, no suffering); he comes back glowing.

Every frame is a pure function of t. English on-screen text except three words the narration says, shown in the
viewer's script on a parchment strip: the book's title (a2), the hard word श्राप explained as "a bad wish" (a6) and the
boy's name (a7) (shaped by matplotlib as in scenes_arjuna; left out without the Nirmala font). Cues are words of the
line in each language ({"hi": ..., "kn": ...}) with a fraction fallback, kept in one table (CUES) that the scenes and
sfx() both read, with minimum gaps so a fast voice can't bunch the beats together. The Hindi reel is the one made in
this style (the Kannada reel gets its own art); the module still draws the Kannada lines without errors. The shot
starts and cues are cached on the timeline under this module's own names (_av_shots, _av_cues).

Shot list (line: what is on the screen)
  a1   HOOK, frame 0: the mother large and alone, seated, a big glowing womb window on her belly with the tiny child
       curled inside: AN UNBORN BABY CORRECTED / HIS FATHER (big words in by 0.3 s); heartbeat rings; on "paida" the
       tag NOT EVEN BORN YET; on "pet" the window pulses and the child opens his eyes; the father comes in on the right
       reading his palm leaf, and on "pitaji" the child's arm rises to point at him; a voice cloud (joined to the
       window by a trail of light) FATHER, YOU'RE / READING IT WRONG! (second line on "galat"); the big words underlined
  a2   a palm-leaf book rises and opens: MAHABHARATA (ringed on "sachchi"), the title in the viewer's script: A TRUE
       STORY FROM THE / MAHABHARATA
  a3   the father seated (tag FATHER), an oil lamp, two children listening with folded hands: HIS FATHER WAS / A BIG
       GURU; night falls, the moon rises, he reads the palm leaf and golden Om syllables float to the children (tag
       CHILDREN): EVERY NIGHT, HE TAUGHT / PRAYER MANTRAS
  a4   night: the father turned to the mother (tag MOTHER), the children behind him; the window glows, sound rings: ONE
       NIGHT, FROM THE BELLY: / A VOICE!; the child points; a voice cloud FATHER, / YOU'RE READING / IT WRONG!; the
       father and the children gasp ("!")
  a5   close on the father, his cheek flushed red, a bead of sweat; the children whisper behind: IN FRONT OF THE
       CHILDREN, / ASHAMED; the flush turns to anger in a red glow: AND VERY / ANGRY!
  a6   the father stands and points; a crackle of light stops at the window's rim, the window flickers red: THE ANGRY
       FATHER / CURSED HIM; the hard word: श्राप on a strip and the card CURSE = / A BAD WISH; then the card YOUR BODY
       WILL BE / CROOKED IN / 8 PLACES
  a7   the mother holds the newborn in a saffron cloth, a soft glow: THE BABY WAS BORN / CROOKED; HIS NAME: /
       ASHTAVAKRA with the name in the viewer's script; then ASHTAVAKRA MEANS: / CROOKED IN 8 PLACES with the plaques
       ASHTA = 8 + VAKRA = CROOKED
  a8   a king's palace, the king on his throne at the back (tag THE KING); the father walks in (tag FATHER): ONE DAY,
       FATHER WENT TO / A KING'S PALACE; the pandit, tall and proud, steps in, chin up: THERE LIVED A / PROUD PANDIT
  a9   the pandit large, one finger raised, a sly smile; a "?" and a "!" pop by his hand: THE PANDIT'S GAME: /
       QUESTIONS & ANSWERS; the lake beside the palace in blue light and the card LOSE THE GAME -> INTO THE WATER!: THE
       LOSER GOES / INTO THE WATER
  a10  by the lake: the father bows his head: FATHER / LOST; he folds his hands, closes his eyes and sinks gently into
       blue light, bubbles of light rising: AND WAS PUT INTO / THE WATER
  a10q the QUESTION: the mother small on the shore with the baby in her arms, the water before her; the card WILL HE
       EVER / SEE FATHER? and a big red "?" (ringed on "dekh")
  a11  a counter turns 1..12 YEARS while the sun spins: 12 YEARS / LATER; the boy (tag ASHTAVAKRA, AGE 12) with his
       staff: THE BABY GREW UP: / ASHTAVAKRA; a thought bubble of his father sinking: HE FOUND OUT / THE TRUTH; he
       walks off, bent, with his staff: WITH HIS CROOKED BODY, / TO THE PALACE!
  a12  the palace door; the gatekeeper slants his spear across it: AT THE DOOR: / STOPPED!; cloud NO CHILDREN!; the boy
       answers (ASHTAVAKRA SAID:): cloud AGE? NO! / BRAINS MAKE / YOU BIG!; the spear goes up, the guard steps aside
  a13  the palace: the boy and the pandit face to face, the king between them at the back: LITTLE BOY VS / PROUD
       PANDIT; "?" from the pandit, "!" from the boy, in turn; the pandit staggers back, stunned, a burst of light round
       the boy: THE LITTLE BOY / WON!
  a14  the TWIST, slowly: the pandit, honest now: THEN THE PANDIT TOLD / A SECRET; HE SAID: / NOBODY DIED!; a bubble
       opens under the water: the water god (a tall glowing figure, a crown, blue light) with the father (in colour) and
       the others before him, hands folded: ALL ALIVE, WITH / THE WATER GOD (tags ALIVE!, FATHER)
  a15  the lake: the father rises out of the water, glowing, the boy on the shore smiles: FROM THE WATER, FATHER / CAME
       BACK ALIVE!; then the river: the father pours water from a pot over the boy: FATHER BATHED HIM / IN THE RIVER; a
       burst of light, the boy rises straight, arms up: AND HIS BODY BECAME / STRAIGHT!
  a15c the CALLBACK: frame 0 again (the mother, the window, the child pointing); the father comes in, back and smiling,
       warm light: PUNISHED FOR SPEAKING... / HIS WORDS SAVED FATHER
  a16  SO, / WHOSE FAULT?; two cards THE SON? (the womb window, the child pointing) / THE FATHER? (the angry father
       pointing), a red ring alternating (the question is the last line)
"""
import math

import cairo

import ashtavakra_cast as AV
import dharmavyadha_cast as DV
import jayadratha_cast as J
import puppet_core as pc
import ravana_cast as R
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, back, clamp, draw_text, ease, prog
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_arjuna import HAS_INDIC, card2, cloud_text, indic_surface
from scenes_dharmavyadha import READ, sun_arc, tears
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, motes, red_ring, sound_rings, stars, walk_legs, \
    woman_angles
from scenes_jayadratha import NIGHT, flash_at, silhouette, tag, tint, title_lift, to_user
from scenes_kaikeyi import ANJALI, card, fig
from scenes_lakshman_rekha import book, sparkle
from scenes_mandhata import aura, burst, held, lights, local, mix, reach_arm, warm
from scenes_ravana import head2
from scenes_ruru import plate, sepia
from scenes_six_b import counter_badge
from scenes_shani_ganesha import bolt, deva, red_glow
from shots import T

MISSES = set()                       # cue words not found in a line (falls back to fractions)
G = FEET + 120                       # the ground line of most sets
BK = 0.8                             # the boy's scale relative to the grown men beside him
COOL = (0.42, 0.70, 1.0)             # the water's blue light
TITLE = {"hi": "महाभारत", "kn": "ಮಹಾಭಾರತ"}                          # the book's title in the viewer's script (a2)
NAME = {"hi": "अष्टावक्र", "kn": "ಅಷ್ಟಾವಕ್ರ"}                       # the boy's name in the viewer's script (a6)


def lang(tl):
    return getattr(tl, "lang", "hi")


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, words)
    except (KeyError, ValueError):
        MISSES.add((bid, words[lang(tl)] if isinstance(words, dict) else words))
        return T(tl, bid, frac)


# Every cue of every line: (name, {"hi": word, "kn": word}, fraction fallback, ((after, min gap), ...)); "t0" = the
# line's start. Words are exact substrings of the script lines (checked: MISSES stays empty).
CUES = {
    "a1": (("U", {"hi": "पैदा", "kn": "ಹುಟ್ಟೇ"}, 0.2, (("t0", 0.9),)),
           ("B", {"hi": "पेट", "kn": "ಹೊಟ್ಟೆಯೊಳಗಿಂದ"}, 0.5, (("U", 0.7),)),
           ("F", {"hi": "पिताजी", "kn": "ಅಪ್ಪಾ"}, 0.68, (("B", 0.7),)),
           ("W", {"hi": "गलत", "kn": "ತಪ್ಪಾಗಿ"}, 0.82, (("F", 0.4),))),
    "a2": (("M", {"hi": "महाभारत", "kn": "ಮಹಾಭಾರತದ"}, 0.2, (("t0", 0.3),)),
           ("T", {"hi": "सच्ची", "kn": "ನಿಜವಾದ"}, 0.6, (("M", 0.4),))),
    "a3": (("Ft", {"hi": "पिता", "kn": "ಅಪ್ಪ"}, 0.12, ()),
           ("G", {"hi": "गुरु", "kn": "ಗುರು"}, 0.35, (("t0", 0.6),)),
           ("R", {"hi": "रात", "kn": "ರಾತ್ರಿ"}, 0.52, (("G", 0.6),)),
           ("M", {"hi": "मंत्र", "kn": "ಮಂತ್ರ"}, 0.8, (("R", 0.6),))),
    "a4": (("B", {"hi": "पेट", "kn": "ಹೊಟ್ಟೆಯಿಂದ"}, 0.2, (("t0", 0.3),)),
           ("V", {"hi": "बच्चे", "kn": "ಧ್ವನಿ"}, 0.32, (("B", 0.3),)),
           ("F", {"hi": "पिताजी", "kn": "ಅಪ್ಪಾ"}, 0.5, (("V", 0.5),)),
           ("Mt", {"hi": "मंत्र", "kn": "ಮಂತ್ರ"}, 0.62, (("F", 0.3),)),
           ("W", {"hi": "गलत", "kn": "ತಪ್ಪಾಗಿ"}, 0.82, (("Mt", 0.4),))),
    "a5": (("S", {"hi": "सामने", "kn": "ಮುಂದೆ"}, 0.25, (("t0", 0.3),)),
           ("Sh", {"hi": "शर्म", "kn": "ನಾಚಿಕೆ"}, 0.5, (("S", 0.4),)),
           ("A", {"hi": "और", "kn": "ಕೋಪನೂ"}, 0.75, (("Sh", 0.8),))),
    "a6": (("C", {"hi": "श्राप", "kn": "ಶಾಪ"}, 0.25, (("t0", 0.4),)),
           ("Y", {"hi": "यानी", "kn": "ಕೊಟ್ರು"}, 0.36, (("C", 0.3),)),
           ("Bd", {"hi": "बद्दुआ", "kn": "ಕೊಟ್ರು"}, 0.45, (("Y", 0.3),)),
           ("B", {"hi": "शरीर", "kn": "ದೇಹ"}, 0.65, (("Bd", 1.3),)),
           ("E", {"hi": "आठ", "kn": "ಎಂಟು"}, 0.75, (("B", 0.4),)),
           ("K", {"hi": "जाएगा", "kn": "ಸೊಟ್ಟಗಾಗುತ್ತೆ"}, 0.92, (("E", 0.4),))),
    "a7": (("Bn", {"hi": "पैदा", "kn": "ಹುಟ್ಟಿತು"}, 0.3, (("t0", 0.6),)),
           ("N", {"hi": "नाम", "kn": "ಹೆಸರು"}, 0.45, (("Bn", 0.7),)),
           ("A", {"hi": "अष्टावक्र", "kn": "ಅಷ್ಟಾವಕ್ರ"}, 0.55, (("N", 0.4),)),
           ("Mt", {"hi": "मतलब", "kn": "ಅಂದ್ರೆ"}, 0.75, (("A", 1.1),)),
           ("E", {"hi": "आठ", "kn": "ಎಂಟು"}, 0.85, (("Mt", 0.4),))),
    "a8": (("F", {"hi": "पिता", "kn": "ಅಪ್ಪ"}, 0.15, (("t0", 0.2),)),
           ("K", {"hi": "राजा", "kn": "ರಾಜನ"}, 0.3, (("F", 0.3),)),
           ("P", {"hi": "महल", "kn": "ಅರಮನೆಗೆ"}, 0.42, (("K", 0.3),)),
           ("Gh", {"hi": "घमंडी", "kn": "ಜಂಭದ"}, 0.75, (("P", 0.9),)),
           ("Pd", {"hi": "पंडित", "kn": "ಪಂಡಿತ"}, 0.88, (("Gh", 0.3),))),
    "a9": (("Kh", {"hi": "खेल", "kn": "ಆಟ"}, 0.25, (("t0", 0.4),)),
           ("Q", {"hi": "सवाल", "kn": "ಪ್ರಶ್ನೆ"}, 0.38, (("Kh", 0.3),)),
           ("L", {"hi": "हारेगा", "kn": "ಸೋಲ್ತಾರೋ"}, 0.55, (("Q", 0.9),)),
           ("W", {"hi": "पानी", "kn": "ನೀರಲ್ಲಿ"}, 0.72, (("L", 0.5),)),
           ("Dr", {"hi": "डुबो", "kn": "ಮುಳುಗಿಸ್ತಾರೆ"}, 0.85, (("W", 0.3),))),
    "a10": (("L", {"hi": "हार", "kn": "ಸೋತರು"}, 0.3, (("t0", 0.4),)),
            ("W", {"hi": "पानी", "kn": "ನೀರಲ್ಲಿ"}, 0.6, (("L", 0.9),)),
            ("D", {"hi": "डुबो", "kn": "ಮುಳುಗಿಸಿದ್ರು"}, 0.8, (("W", 0.3),))),
    "a10q": (("Ch", {"hi": "बच्चा", "kn": "ಮಗು"}, 0.25, (("t0", 0.4),)),
             ("P", {"hi": "पिता", "kn": "ಅಪ್ಪನನ್ನ"}, 0.5, (("Ch", 0.4),)),
             ("D", {"hi": "देख", "kn": "ನೋಡುತ್ತಾ"}, 0.8, (("P", 0.4),))),
    "a11": (("Y", {"hi": "बारह", "kn": "ಹನ್ನೆರಡು"}, 0.03, ()),
            ("A", {"hi": "अष्टावक्र", "kn": "ಅಷ್ಟಾವಕ್ರನಿಗೆ"}, 0.2, (("t0", 1.0),)),
            ("T", {"hi": "बात", "kn": "ವಿಷಯ"}, 0.36, (("A", 0.6),)),
            ("Bd", {"hi": "शरीर", "kn": "ದೇಹದ"}, 0.65, (("T", 0.9),)),
            ("P", {"hi": "महल", "kn": "ಅರಮನೆಗೆ"}, 0.85, (("Bd", 0.4),))),
    "a12": (("S", {"hi": "रोका", "kn": "ತಡೆದ್ರು"}, 0.12, (("t0", 0.3),)),
            ("N", {"hi": "बच्चे", "kn": "ಮಕ್ಕಳನ್ನ"}, 0.22, (("S", 0.4),)),
            ("A", {"hi": "बोला", "kn": "ಹೇಳಿದ"}, 0.45, (("N", 0.9),)),
            ("G", {"hi": "उम्र", "kn": "ವಯಸ್ಸಿಂದ"}, 0.58, (("A", 0.4),)),
            ("K", {"hi": "अक्ल", "kn": "ಬುದ್ಧಿಯಿಂದ"}, 0.82, (("G", 0.8),))),
    "a13": (("Ch", {"hi": "छोटे", "kn": "ಪುಟ್ಟ"}, 0.2, (("t0", 0.3),)),
            ("Pd", {"hi": "पंडित", "kn": "ಪಂಡಿತನನ್ನ"}, 0.45, (("Ch", 0.4),)),
            ("Q", {"hi": "सवाल", "kn": "ಪ್ರಶ್ನೆ"}, 0.65, (("Pd", 0.3),)),
            ("Wn", {"hi": "हरा", "kn": "ಸೋಲಿಸಿದ"}, 0.88, (("Q", 1.2),))),
    "a14": (("S", {"hi": "खोला", "kn": "ರಹಸ್ಯ"}, 0.2, (("t0", 0.4),)),
            ("M", {"hi": "मारा", "kn": "ಕೊಂದಿಲ್ಲ"}, 0.42, (("S", 0.8),)),
            ("D", {"hi": "देवता", "kn": "ದೇವರ"}, 0.7, (("M", 1.0),)),
            ("Z", {"hi": "पास", "kn": "ಜೀವಂತವಾಗಿದ್ದಾರೆ"}, 0.85, (("D", 0.5),))),
    "a15": (("W", {"hi": "पानी", "kn": "ನೀರಿಂದ"}, 0.08, (("t0", 0.15),)),
            ("L", {"hi": "लौट", "kn": "ವಾಪಸ್"}, 0.35, (("W", 0.9),)),
            ("N", {"hi": "नदी", "kn": "ನದಿಯಲ್ಲಿ"}, 0.62, (("L", 1.2),)),
            ("S", {"hi": "सीधा", "kn": "ನೇರ"}, 0.9, (("N", 1.6),))),
    "a15c": (("P", {"hi": "पेट", "kn": "ಹೊಟ್ಟೆಯಲ್ಲಿ"}, 0.2, (("t0", 0.4),)),
             ("U", {"hi": "उसी", "kn": "ಅದೇ"}, 0.6, (("P", 0.9),)),
             ("V", {"hi": "वापस", "kn": "ವಾಪಸ್"}, 0.85, (("U", 0.6),))),
    "a16": (("Q", {"hi": "किसकी", "kn": "ಯಾರದ್ದು"}, 0.2, (("t0", 0.3),)),
            ("S", {"hi": "बेटे", "kn": "ಮಗನದ್ದಾ"}, 0.45, (("Q", 0.6),)),
            ("F", {"hi": "पिता", "kn": "ಅಪ್ಪನದ್ದಾ"}, 0.72, (("S", 0.8),)),
            ("C", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.88, (("F", 0.5),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under _av_cues)."""
    cache = getattr(tl, "_av_cues", None)
    if cache is None:
        cache = {}
        tl._av_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, words, frac, cons in CUES[bid]:
            v = cue(tl, bid, words, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


# ------------------------------------------------------------------ light and water


def ground(cr, y=G, alpha=1.0):
    prop(cr, "ground", W / 2, y + 6, 0.82, alpha=alpha)


def cool(cr, x, y, r, a, col=COOL):
    """warm() in the water's blue."""
    warm(cr, x, y, r, a, col)


def water(cr, t, y0, rows=4, s=0.82, step=54, alpha=1.0, river=False, x0=0, x1=W, speed=34.0):
    """Rows of scrolling wave strips from y0 down (the lake: ravana_cast's blue; the river Samanga: a clear green-
    blue), clipped to x0..x1."""
    if alpha <= 0.01:
        return
    names = ("av_rwaveA", "av_rwaveB") if river else ("rv_waveA", "rv_waveB")
    per = R.WAVE_P * s
    cr.save()
    cr.rectangle(x0, -100, x1 - x0, H + 200)
    cr.clip()
    for i in range(rows):
        off = (t * speed * (1.0 if i % 2 else -0.75) + 37 * i) % per
        prop(cr, names[i % 2], 540 + off - per / 2, y0 + i * step, s, alpha=alpha)
    cr.restore()


def ripple(cr, x, y, t, t0, n=3, period=0.45, rmax=260, alpha=1.0):
    """Rings spreading on the water from (x, y)."""
    for i in range(n):
        p = (t - t0 - i * period) / 1.4
        if 0 < p < 1:
            r = 30 + rmax * ease(p)
            cr.save()
            cr.translate(x, y)
            cr.scale(1.0, 0.22)
            cr.arc(0, 0, r, 0, 2 * math.pi)
            cr.restore()
            cr.set_source_rgba(0.90, 0.97, 1.0, 0.7 * (1 - p) * alpha)
            cr.set_line_width(5 * (1 - p) + 2)
            cr.stroke()


def bubbles(cr, t, x, y, r, n, a, ph=0.0):
    """Little bubbles of light rising through the water."""
    lights(cr, t, x, y, r, n, a, (0.80, 0.92, 1.0), 0.45, ph)


def ledge(cr, x0, x1, y, alpha=1.0):
    """The stone edge of the lake by the court: a row of dressed stones."""
    if alpha <= 0.01:
        return
    cr.save()
    pc.poly(cr, [(x0, y - 26), (x1, y - 26), (x1, y + 34), (x0, y + 34)])
    cr.set_source_rgba(0.62, 0.50, 0.38, alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, alpha)
    cr.set_line_width(5)
    cr.stroke()
    for k in range(int((x1 - x0) // 90) + 1):
        xx = x0 + 90 * k + (45 if k % 2 else 0)
        cr.move_to(xx, y - 26)
        cr.line_to(xx, y + 34)
    cr.set_line_width(3)
    cr.stroke()
    cr.restore()


# ------------------------------------------------------------------ the womb window


WOMB_IN = (1.0, 0.97, 0.90)
WOMB_OUT = (1.0, 0.78, 0.60)
WOMB_RIM = (1.0, 0.80, 0.42)


def womb(cr, t, cx, cy, rx, ry, a, talk=False, point=0.0, pulse=0.0, red=0.0, flip=False, glow_a=1.0):
    """The womb window: a soft rose-gold oval of light over the mother's belly with the unborn child curled inside,
    gently breathing (talk: eyes open, mouth open); point 0..1 raises his little arm to point out (toward the side he
    faces); red 0..1 flushes it red (the curse). Returns the fingertip (scene coordinates)."""
    if a <= 0.01:
        return (cx, cy)
    k = 1 + 0.035 * pulse
    rx, ry = rx * k, ry * k
    cr.save()
    cr.translate(cx, cy)
    cr.scale(rx, ry)
    cr.new_path()
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    path = cr.copy_path()
    cr.new_path()
    glow(cr, cx, cy, max(rx, ry) * 2.2, (0.45 + 0.35 * pulse) * a * glow_a)
    warm(cr, cx, cy, max(rx, ry) * 1.9, (0.35 + 0.3 * pulse) * a * glow_a, (1.0, 0.70, 0.50))
    g = cairo.RadialGradient(cx, cy - 0.2 * ry, 0, cx, cy, max(rx, ry))
    g.add_color_stop_rgba(0, *WOMB_IN, 0.92 * a)
    g.add_color_stop_rgba(0.75, *WOMB_OUT, 0.88 * a)
    g.add_color_stop_rgba(1, 0.96, 0.62, 0.46, 0.9 * a)
    cr.append_path(path)
    cr.set_source(g)
    cr.fill()
    fs = ry * 1.45 / 380.0
    sg = -1 if flip else 1
    rot = 0.035 * math.sin(t * 1.3) * sg
    fx, fy = cx - 6 * fs * sg, cy + 52 * fs
    cr.save()
    cr.append_path(path)
    cr.clip()
    prop(cr, "av_fetus_talk" if talk else "av_fetus", fx, fy, fs, rot=rot, alpha=a, flip=flip)
    sx, sy = local(fx, fy, fs, rot, flip, *AV.FETUS_SHOULDER)
    ang = (-0.55 - 1.55 * ease(clamp(point)) + 0.06 * math.sin(t * 5.0) * clamp(point)) * sg + rot
    prop(cr, "av_fetus_arm", sx, sy, fs, rot=ang, alpha=a, flip=flip)
    tip = local(sx, sy, fs, ang, flip, 3, 160)
    lights(cr, t, cx, cy, rx * 0.8, 6, 0.45 * a, (1.0, 0.92, 0.70), 0.35)
    if red > 0.01:
        cr.set_source_rgba(0.95, 0.20, 0.10, 0.45 * clamp(red) * a)
        cr.paint()
    cr.restore()
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for lw, al in ((30, 0.16), (13, 0.32)):
        cr.new_path()
        cr.append_path(path)
        cr.set_source_rgba(*WOMB_RIM, al * a * glow_a)
        cr.set_line_width(lw)
        cr.stroke()
    cr.restore()
    for lw, col in ((6.5, (0.62, 0.30, 0.10)), (2.6, (1.0, 0.94, 0.80))):
        cr.new_path()
        cr.append_path(path)
        cr.set_source_rgba(*col, 0.95 * a)
        cr.set_line_width(lw)
        cr.stroke()
    cr.new_path()
    return tip


# ------------------------------------------------------------------ puppets


def hname(base, mood, default):
    return base if mood == default else base + "_" + mood


def kahoda(cr, t, x, s, mood="calm", leaf=False, **kw):
    """Kahoda standing (feet on `feet`, default G); leaf = the palm leaf held before him in his front hand."""
    kw.setdefault("feet", G)
    ex = dict(kw.pop("extra", None) or {})
    if leaf:
        ex["av_kahoda_armF_lo"] = held("dv_pleaf", kw.get("front", (-0.32, -0.55)), 0.7, 168, 0.0,
                                       kw.get("alpha", 1.0), kw.get("blur", 0.0))
    return fig(cr, AV.KAHODA, "av_kahoda", t, x, s, swap={"av_kahoda_head": hname("av_kahoda_head", mood, "calm")},
               extra=ex or None, **kw)


def kahoda_walk(cr, t, t0, t1, x0, x1, s, feet=G, t_in=None, **kw):
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, 0.45)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    kw.setdefault("hits", [(t1, 1.0)])
    return kahoda(cr, t, x, s * k, legs=walk_legs(ph), rot=rock, y=feet - 434 * s + bob - (k - 1) * 300 * s,
                  alpha=a * kw.pop("alpha", 1.0), blur=b + kw.pop("blur", 0.0), feet=feet, **kw)


def sit(cr, rig, key, t, x, ground_, s, body, seat=None, seat_h=DV.SEAT_H, head=None, lady=False, front=None,
        backa=None, tilt=0.0, hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, ph=0.0, extra=None):
    """scenes_dharmavyadha.sitter with the seated body sprite named (body), so one figure can sit two ways."""
    hy = ground_ - seat_h * s
    if lady:
        ang = woman_angles(key, t, front or (-0.5, -1.1), backa or (0.1, -0.6), tilt, hits, ph)
        hide = ()
    else:
        from scenes_jarasandha import man_angles
        ang = man_angles(key, t, front or (-0.5, -1.1), backa or (0.1, -0.6), tilt, (0.0, 0.0), hits, ph)
        hide = (key + "_legF", key + "_legB")
    swap = {key + "_body": body}
    if head:
        swap[key + "_head"] = head
    ex = dict(extra or {})
    if seat:
        prev = ex.get(key + "_body")

        def fn(cr_, prev=prev):
            pc.paint_part(cr_, seat, alpha, blur)
            if prev:
                prev(cr_)
        ex[key + "_body"] = fn
    return puppet(cr, rig, x, hy, s, bob_rot(t, ph, 0.008), flip, ang, alpha, blur, hide=hide, swap=swap, rods=rods,
                  extra=ex or None)


def kahoda_sit(cr, t, x, ground_, s, mood="read", leaf=True, front=None, backa=None, **kw):
    front = front or READ["front"]
    backa = backa or READ["backa"]
    ex = {}
    if leaf:
        ex["av_kahoda_armF_lo"] = held("dv_pleaf", front, 0.78, 168, 0.0, kw.get("alpha", 1.0), kw.get("blur", 0.0))
    return sit(cr, AV.KAHODA, "av_kahoda", t, x, ground_, s, "av_kahoda_body_sit", seat="av_kahoda_seat",
               head=hname("av_kahoda_head", mood, "calm"), front=front, backa=backa, extra=ex, **kw)


def dis_sit(cr, t, k, x, ground_, s, mood="calm", **kw):
    key = f"av_dis{k}"
    return sit(cr, AV.DIS1 if k == 1 else AV.DIS2, key, t, x, ground_, s, key + "_body_sit", seat=key + "_seat",
               head=hname(key + "_head", mood, "calm"), **kw)


def suj(cr, t, x, ground_, s, mood="open", belly=True, stool=True, flip=False, alpha=1.0, blur=0.0, **kw):
    """Sujata seated on her low stool (soles on ground_); returns her points (device) with 'belly'."""
    if stool:
        prop(cr, "av_peeta", x + (-30 if flip else 30) * s, ground_, s, alpha=alpha, blur=blur)
    kw.setdefault("front", (-0.55, -0.9))
    kw.setdefault("backa", (-0.1, -0.7))
    return sit(cr, AV.SUJ, "av_suj", t, x, ground_, s, "av_suj_body_sit" if belly else "av_suj_body_sit0",
               seat_h=DV.BENCH_H, head=hname("av_suj_head", mood, "open"), lady=True, flip=flip, alpha=alpha,
               blur=blur, **kw)


def boy(cr, t, x, s, mood="calm", bent=True, staff=True, front=(-0.95, -0.35), backa=(0.35, -0.5), feet=G,
        tilt=0.04, **kw):
    """Ashtavakra standing (feet on `feet`): bent (BOY_BENT) or straight (BOY); his bamboo staff in his front hand,
    its foot on the ground."""
    rig = AV.BOY_BENT if bent else AV.BOY
    swap = dict(AV.BENT_SWAP) if bent else {}
    swap["av_boy_head"] = hname("av_boy_head", mood, "calm")
    if staff:
        probe = dict(kw, alpha=0.0, rods=False)
        pts = fig(cr, rig, "av_boy", t, x, s, front=front, backa=backa, swap=swap, feet=feet, **probe)
        hx, hy = to_user(cr, pts["handF"])
        sg = -1 if kw.get("flip") else 1
        prop(cr, "av_staff", hx + 6 * s * sg, max(hy + 20, feet), s * 1.3, rot=tilt * sg, alpha=kw.get("alpha", 1.0),
             blur=kw.get("blur", 0.0))
    return fig(cr, rig, "av_boy", t, x, s, front=front, backa=backa, swap=swap, feet=feet, **kw)


def boy_walk(cr, t, t0, t1, x0, x1, s, feet=G, t_in=None, **kw):
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, 0.5)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    kw.setdefault("hits", [(t1, 1.0)])
    return boy(cr, t, x, s * k, legs=walk_legs(ph, 0.26), rot=rock, y=feet - 434 * s * k + bob,
               alpha=a * kw.pop("alpha", 1.0), blur=b + kw.pop("blur", 0.0), feet=feet, **kw), x


def janaka(cr, t, x, ground_, s, mood="calm", throne=True, alpha=1.0, blur=0.0, **kw):
    """King Janaka seated on his throne (facing right; the throne's foot on ground_)."""
    if throne:
        prop(cr, "md_throne", x + 50 * s, ground_, s * 1.04, alpha=alpha, blur=blur)
    kw.setdefault("front", (-0.6, -0.9))
    kw.setdefault("backa", (-0.2, -0.8))
    return sit(cr, AV.JANAKA, "av_janaka", t, x, ground_, s, "av_janaka_body_sit", seat="av_janaka_seat",
               seat_h=DV.BENCH_H, head=hname("av_janaka_head", mood, "calm"), alpha=alpha, blur=blur, **kw)


def vandin(cr, t, x, s, mood="calm", **kw):
    kw.setdefault("feet", G)
    return fig(cr, AV.VANDIN, "av_vandin", t, x, s, swap={"av_vandin_head": hname("av_vandin_head", mood, "calm")},
               **kw)


def guard(cr, t, x, s, spear=0.0, **kw):
    """The gatekeeper (jayadratha_cast's soldier) with his spear: spear 0 = upright at his side, 1 = slanted across
    the doorway (its tip high, well above the boy) while his other hand is raised, palm out: stop."""
    front = mix((-0.5, -0.6), (-1.1, -0.35), spear)
    backa = mix((0.3, -0.25), (-1.75, -0.35), spear)
    tilt = 0.72 * spear
    kw.setdefault("feet", G)
    ex = {"jd_soldier_armF_lo": held("jd_spear", front, 0.66, 150, tilt, kw.get("alpha", 1.0), kw.get("blur", 0.0))}
    return fig(cr, J.SOLDIER, "jd_soldier", t, x, s, front=front, backa=backa, extra=ex, **kw)


def brahmin_sil(cr, t, k, x, y, s, a, flip=False, ph=0.0):
    """A Brahmin rising from the water: a dark silhouette (a disciple puppet) with a soft halo, hands folded."""
    if a <= 0.01:
        return
    key = f"av_dis{k}"
    rig = AV.DIS1 if k == 1 else AV.DIS2
    hc = local(x, y, s, 0.0, flip, 16, -420)
    glow(cr, hc[0], hc[1] + 120 * s, 360 * s + 40, 0.6 * a)
    cool(cr, hc[0], hc[1] + 200 * s, 420 * s, 0.5 * a, (0.75, 0.88, 1.0))
    cr.save()
    cr.set_source_rgba(1.0, 0.86, 0.50, 0.8 * a)
    cr.set_line_width(max(3.0, 8 * s))
    cr.arc(hc[0] - (12 if not flip else -12) * s, hc[1] - 30 * s, 140 * s, 0, 2 * math.pi)
    cr.stroke()
    cr.restore()
    silhouette(cr, lambda c: fig(c, rig, key, t, x, s, front=ANJALI["front"], backa=ANJALI["backa"], flip=flip,
                                 y=y, ph=ph, rods=False), 0.85 * a)


# ------------------------------------------------------------------ text pieces


def num_disc(cr, x, y, r, text, a, rot=0.0, col=RED, hot=0.0):
    """A small round leather medallion with a number (the debate's riddles)."""
    if a <= 0.01:
        return
    if hot > 0.01:
        glow(cr, x, y, r * 3.4, 0.7 * hot * a)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.set_source_rgba(0.97, 0.87, 0.62, 0.97 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(4)
    cr.stroke()
    for i in range(14):
        ang = 2 * math.pi * i / 14
        cr.new_sub_path()
        cr.arc((r - 8) * math.cos(ang), (r - 8) * math.sin(ang), 1.8, 0, 2 * math.pi)
    cr.set_source_rgba(0.55, 0.32, 0.14, 0.8 * a)
    cr.fill()
    draw_text(cr, text, 0, 2, int(r * 1.15), col, a, anchor="cm")
    cr.restore()


def script_strip(cr, t, t_in, text, x, y, size, t_out=None):
    """Words in the viewer's own script on a parchment strip (left out without the Nirmala font)."""
    if not HAS_INDIC or t < t_in:
        return
    q = prog(t, t_in, 0.3)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.25)
    if q <= 0.01:
        return
    su = indic_surface(text, size, INK)
    w_, h_ = su.get_width(), su.get_height()
    yy = y + 16 * (1 - q)
    cr.save()
    pc.poly(cr, [(x - w_ / 2 - 28, yy - h_ / 2 - 14), (x + w_ / 2 + 28, yy - h_ / 2 - 14), (x + w_ / 2 + 40, yy),
                 (x + w_ / 2 + 28, yy + h_ / 2 + 14), (x - w_ / 2 - 28, yy + h_ / 2 + 14), (x - w_ / 2 - 40, yy)])
    cr.set_source_rgba(0.97, 0.87, 0.62, 0.96 * q)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, q)
    cr.set_line_width(3.5)
    cr.stroke()
    cr.set_source_surface(su, x - w_ / 2, yy - h_ / 2)
    cr.paint_with_alpha(q)
    cr.restore()


def bubble(cr, t, t_in, x, y, r, content, src=None, alpha=1.0, col=(0.78, 0.90, 1.0), t_out=None):
    """A round vision bubble (a thought, or a glimpse under the water) popping in at t_in, with three small circles
    trailing to src; content(cr) draws inside it (scene coordinates, clipped)."""
    q = back(clamp((t - t_in) / 0.35), 1.5)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.3)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    rr = r * (0.6 + 0.4 * q)
    if src is not None:
        for i, f in enumerate((0.25, 0.5, 0.72)):
            px, py = src[0] + (x - src[0]) * f, src[1] + (y - src[1]) * f
            cr.arc(px, py, 10 + 9 * i, 0, 2 * math.pi)
            cr.set_source_rgba(0.97, 0.90, 0.72, 0.95 * a)
            cr.fill_preserve()
            cr.set_source_rgba(*pc.INK, a)
            cr.set_line_width(3)
            cr.stroke()
    cr.save()
    cr.arc(x, y, rr, 0, 2 * math.pi)
    g = cairo.RadialGradient(x, y - rr * 0.3, 0, x, y, rr)
    g.add_color_stop_rgba(0, 1.0, 0.98, 0.94, 0.97 * a)
    g.add_color_stop_rgba(1, *col, 0.97 * a)
    cr.set_source(g)
    cr.fill_preserve()
    cr.clip()
    if a > 0.3:
        content(cr)
    cr.restore()
    cr.arc(x, y, rr, 0, 2 * math.pi)
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(6)
    cr.stroke()
    cr.arc(x, y, rr - 12, 0, 2 * math.pi)
    cr.set_source_rgba(0.55, 0.32, 0.14, 0.6 * a)
    cr.set_dash([3, 12])
    cr.set_line_width(4)
    cr.stroke()
    cr.set_dash([])


def voice_cloud(cr, t, t_in, x, y, w, h, lines, src, alpha=1.0):
    """The unborn child's voice: a scalloped parchment cloud with no tail, joined to the womb window (src) by a trail
    of small glowing circles, popping in at t_in; lines = [(text, size, colour, dy, t_show)] in screen pixels."""
    q = back(clamp((t - t_in) / 0.3), 1.6)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    k = 0.6 + 0.4 * q
    for i, f in enumerate((0.18, 0.42, 0.66)):
        u = clamp((t - t_in) / 0.25 - 0.4 * i)
        if u <= 0:
            continue
        px, py = src[0] + (x - src[0]) * f, src[1] + (y + h * 0.42 - src[1]) * f
        r = 9 + 7 * i
        glow(cr, px, py, r * 4, 0.35 * a * u)
        cr.arc(px, py, r * u, 0, 2 * math.pi)
        cr.set_source_rgba(0.98, 0.90, 0.70, a * u)
        cr.fill_preserve()
        cr.set_source_rgba(*pc.INK, a * u)
        cr.set_line_width(3)
        cr.stroke()
    cr.save()
    cr.translate(x, y)
    cr.rotate(sway(t, 0.008, 0.5))
    cr.scale(k, k)
    n = 16
    bumps = [(w / 2 * math.cos(2 * math.pi * i / n), h / 2 * math.sin(2 * math.pi * i / n)) for i in range(n)]
    br = 0.17 * (w + h) / 2
    for bx_, by_ in bumps:                                                       # outline first ...
        cr.arc(bx_, by_, br, 0, 2 * math.pi)
        cr.set_source_rgba(*pc.INK, a)
        cr.set_line_width(12)
        cr.stroke()
    for bx_, by_ in bumps:                                                       # ... then the fill over it
        cr.new_sub_path()
        cr.arc(bx_, by_, br, 0, 2 * math.pi)
    cr.new_sub_path()
    cr.save()
    cr.scale(w / 2, h / 2)
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(0.98, 0.90, 0.70, a)
    cr.fill()
    for i in range(n):
        ang = 2 * math.pi * (i + 0.5) / n
        cr.new_sub_path()
        cr.arc((w / 2 - 6) * math.cos(ang), (h / 2 - 6) * math.sin(ang), 2.6, 0, 2 * math.pi)
    cr.set_source_rgba(0.55, 0.32, 0.14, 0.8 * a)
    cr.fill()
    cr.restore()
    for txt, sz, col, dy, ts in lines:
        p = prog(t, ts, 0.25) * a
        if p > 0:
            kk = 1.15 - 0.15 * back(clamp((t - ts) / 0.3))
            cr.save()
            cr.translate(x, y + dy * k)
            cr.scale(kk * k, kk * k)
            draw_text(cr, txt, 0, 0, sz, col, p, anchor="cm")
            cr.restore()


def bang(cr, t, t_in, x, y, size=80, alpha=1.0):
    """A red "!" popping up over a gasping head."""
    q = back(clamp((t - t_in) / 0.25), 2.0)
    a = clamp(q) * alpha * (1 - prog(t, t_in + 1.6, 0.4))
    if a <= 0.01:
        return
    cr.save()
    cr.translate(x, y - 20 * q)
    cr.rotate(0.12 * math.sin(t * 7))
    cr.scale(q, q)
    draw_text(cr, "!", 0, 0, size, RED, a, anchor="cm")
    cr.restore()


def rule_card(cr, t, t_in, x, y, s, t_a, t_b, alpha=1.0, top="LOSE THE GAME", bottom="INTO THE WATER!"):
    """The rule plaque: `top` / (a red arrow) `bottom`, each half on its own word."""
    q = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    yy = y + 60 * (1 - q)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(sway(t, 0.01, 0.4, x * 0.01))
    cr.scale(s, s)
    pc.paint_part(cr, "plaque", a)
    p = prog(t, t_a, 0.25) * a
    if p > 0:
        draw_text(cr, top, 0, -52, 76, INK, p, anchor="cm")
    p = prog(t, t_b, 0.25) * a
    if p > 0:
        k = 1.15 - 0.15 * back(clamp((t - t_b) / 0.3))
        cr.save()
        cr.translate(70, 50)
        cr.scale(k, k)
        draw_text(cr, bottom, 0, 0, min(100, int(1150 / max(1, len(bottom)))), RED, p, anchor="cm")
        cr.restore()
        cr.set_source_rgba(*RED, p)
        cr.set_line_width(14)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(-290, 50)
        cr.line_to(-210, 50)
        cr.stroke()
        pc.poly(cr, [(-214, 30), (-180, 50), (-214, 70)])
        cr.fill()
    cr.restore()
    pc.rod(cr, x, yy + 110 * s, x + 30, H + 60, alpha=0.5 * a)


# ------------------------------------------------------------------ a1  hook (and its echo on a15c)


HK = (320, 1880, 1.34)               # the mother in the hook: x, ground (soles), scale
HK_F = (910, 0.92)                   # the father coming in on the right: x, scale
WR = (224, 254)                      # the womb window's radii in the hook


def hook_mother(cr, t, point, talk, pulse, beats=(), mood="open", hits=(), red=0.0):
    """The frame-0 image: the mother large and seated, the big womb window on her belly, heartbeat rings at `beats`.
    Returns the window's centre and the child's fingertip."""
    x, gr, s = HK
    glow(cr, 420, 1400, 760, 0.45)
    pts = suj(cr, t, x, gr, s, mood=mood, front=(-0.75, -0.3), backa=(-0.25, -0.75), hits=hits, ph=0.3)
    bx, by = to_user(cr, pts["belly"])
    cx, cy = bx + 8, by - 16
    for tb in beats:                                                             # heartbeats: rings off the window
        u = (t - tb) / 0.9
        if 0 < u < 1:
            cr.save()
            cr.translate(cx, cy)
            cr.scale(WR[0] * (1 + 0.45 * ease(u)), WR[1] * (1 + 0.45 * ease(u)))
            cr.arc(0, 0, 1, 0, 2 * math.pi)
            cr.restore()
            cr.set_source_rgba(0.85, 0.36, 0.20, 0.55 * (1 - u))
            cr.set_line_width(10 * (1 - u) + 2)
            cr.stroke()
    tip = womb(cr, t, cx, cy, WR[0], WR[1], 1.0, talk, point, pulse, red)
    if point > 0.6:
        sparkle(cr, tip[0] + 8, tip[1], 26 * (0.7 + 0.3 * math.sin(t * 6)), 0.9, (1.0, 0.95, 0.80))
    return (cx, cy), tip


def a_hook(cr, t, tl, t0, t1):
    c = cues(tl, "a1")
    tU, tB, tF, tW = c["U"], c["B"], c["F"], c["W"]
    pulse = 0.5 + 0.5 * math.sin(t * 2.6) + 1.4 * math.exp(-3 * max(0.0, t - tB)) * (t > tB)
    talk = t > tB and not (tW + 1.2 < t and math.sin(t * 13) < 0)
    (cx, cy), _ = hook_mother(cr, t, prog(t, tF + 0.05, 0.45), talk, pulse, beats=(0.8, 1.5, tB),
                              mood="shock" if t > tW - 0.05 else "open", hits=[(tW, 0.3)])
    fx, fs = HK_F
    t_in = min(tF - 0.5, tB + 0.3)
    if t > t_in:                                                                 # the father, reading his palm leaf
        b, k, a = depth(t, t_in, 0.5)
        kahoda(cr, t, fx, fs * k, mood="shock" if t > tW - 0.05 else "read", flip=True, leaf=True,
               front=READ["front"], backa=(0.3, -0.4), y=HK[1] - 434 * fs * k - (k - 1) * 200, alpha=a, blur=b,
               hits=[(tW, 0.3)], ph=0.6)

    def ui(cr):
        head2(cr, t, "AN UNBORN BABY CORRECTED", -1.0, "HIS FATHER", 0.3, big_size=250, ghost=-1.0,
              under=tW + 0.15)
        tag(cr, t, tU, "NOT EVEN BORN YET", cx + 280, cy - 280, 30, t_out=t_in + 0.1)
        voice_cloud(cr, t, tF - 0.2, 640, 745, 520, 230, [("FATHER, YOU'RE", 70, INK, -42, tF),
                                                          ("READING IT WRONG!", 84, RED, 44, tW)],
                    (cx + 140, cy - 195))
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.2) + flash_at(t, tB, 0.2) + flash_at(t, tW, 0.2))


# ------------------------------------------------------------------ a2  a true story from the Mahabharata


def a_book(cr, t, tl, t0, t1):
    c = cues(tl, "a2")
    tM, tT = c["M"], c["T"]
    leaves = [(None, [("MAHABHARATA", 104, HEAD_FONT)], 0)]
    book(cr, t, 540, 960, 0.9, leaves, t_in=t0 - 0.15, t_open=min(tM, t0 + 0.5), ring=(0, 0, 0, tT))

    def ui(cr):
        head2(cr, t, "A TRUE STORY FROM THE", t0 + 0.05, "MAHABHARATA", tM, big_size=210, under=tT + 0.15)
        script_strip(cr, t, tM + 0.3, TITLE[lang(tl)], 540, 1330, 72)
    return dict(ui=ui, flash=flash_at(t, tM, 0.25) + flash_at(t, tT, 0.2))


# ------------------------------------------------------------------ a3  a big guru; every night, prayer mantras


D3 = ((120, 0.56), (300, 0.52))       # the children: x, scale (facing right)
LAMP3 = (515, 0.6)
KH3 = (790, 0.88)                    # the father seated, facing the children (left)
OM_C = (0.62, 0.30, 0.06)


def moon_arc(cr, t, t0, t1, alpha=1.0):
    """The moon crossing the night sky along a slow arc (all night)."""
    u = clamp((t - t0) / max(1.0, t1 - t0))
    x = 150 + 780 * u
    y = 760 - 150 * math.sin(math.pi * u)
    glow(cr, x, y, 220, 0.45 * alpha)
    prop(cr, "moon", x, y, 0.62, rot=-0.3 + 0.4 * u, alpha=alpha)


def mantras(cr, t, t_on, src, dst, alpha=1.0):
    """Sacred syllables (the Om) floating from the teacher's lips toward the children, one every 0.5 s."""
    if t < t_on or alpha <= 0.01:
        return
    for i in range(8):
        u = (t - t_on - 0.5 * i) / 1.8
        if not 0 < u < 1:
            continue
        x = src[0] + (dst[0] - src[0]) * u
        y = src[1] + (dst[1] - src[1]) * u - 90 * math.sin(math.pi * u) + 12 * math.sin(t * 3 + i)
        a = alpha * min(1.0, 4 * u) * (1 - u * u)
        glow(cr, x, y, 90, 0.5 * a)
        if HAS_INDIC:
            su = indic_surface("ॐ", 58, OM_C)
            cr.set_source_surface(su, x - su.get_width() / 2, y - su.get_height() / 2)
            cr.paint_with_alpha(a)
        else:
            sparkle(cr, x, y, 26, a)


def a_guru(cr, t, tl, t0, t1):
    c = cues(tl, "a3")
    tFt, tG, tR, tM = c["Ft"], c["G"], c["R"], c["M"]
    night = prog(t, tR - 0.3, 0.5)
    stars(cr, t, 0.8 * night, ((120, 640), (330, 700), (610, 620), (880, 690), (1000, 860), (420, 900), (760, 880)))
    moon_arc(cr, t, tR - 1.0, t1 + 3.0, night)
    ground(cr)
    lx, ls = LAMP3
    fl = 0.85 + 0.15 * math.sin(t * 9) + 0.08 * math.sin(t * 23)
    glow(cr, lx, G - 250 * ls, 560, 0.8 * fl)
    warm(cr, lx, G - 250 * ls, 460, 0.65 * fl)
    prop(cr, "av_lamp", lx, G, ls)
    prop(cr, f"flame{int(t * 10) % 3}", lx + 4, G - 236 * ls, 0.2)
    for i, (dx, ds) in enumerate(D3):
        dis_sit(cr, t, i + 1, dx, G, ds, mood="smile" if t > tM + 0.5 else "calm", front=(-0.75, -1.85),
                backa=(-0.8, -1.8), tilt=0.04 * math.sin(t * 1.1 + i), ph=0.5 * i)
    kx, ks = KH3
    nod = 0.05 * math.sin(t * 2.4)
    kp = kahoda_sit(cr, t, kx, G, ks, mood="read" if t > tR - 0.2 else "calm", flip=True, tilt=0.04 + nod,
                    hits=[(tG, 0.3), (tM, 0.3)], ph=0.9)
    mouth = to_user(cr, kp["head"])
    mantras(cr, t, tM - 0.3, (mouth[0] - 80, mouth[1] + 10), (260, G - 470))
    ktop = kp["top"]

    def ui(cr):
        if t < tR:
            head2(cr, t, "HIS FATHER WAS", t0 + 0.05, "A BIG GURU", tG, big_size=270)
        else:
            head2(cr, t, "EVERY NIGHT, HE TAUGHT", tR - 0.1, "PRAYER MANTRAS", tM, big_size=210)
        tag(cr, t, tFt + 0.1, "FATHER", ktop[0], ktop[1] - 80, 36)
        tag(cr, t, tR + 0.2, "CHILDREN", 230, 1240, 32)
    return dict(ui=ui, night=0.34 * night, lift=1.0, flash=flash_at(t, tG, 0.15) + flash_at(t, tM, 0.15))


# ------------------------------------------------------------------ a4  one night: a voice from the belly


SJ4 = (770, 0.8)                     # the mother, facing left
KH4 = (360, 0.66)                    # the father seated, turned to her
D4 = ((70, 0.46, 2.0), (205, 0.42, 3.0))


def a_voice(cr, t, tl, t0, t1):
    c = cues(tl, "a4")
    tB, tV, tF, tMt, tW = c["B"], c["V"], c["F"], c["Mt"], c["W"]
    stars(cr, t, 0.6, ((150, 640), (420, 700), (900, 660), (1000, 900)))
    glow(cr, 560, 1400, 720, 0.4)
    ground(cr)
    for i, (dx, ds, bl) in enumerate(D4):
        dis_sit(cr, t, i + 1, dx, G - 10 * i, ds, mood="shock" if t > tW + 0.05 + 0.12 * i else "calm",
                front=(-0.75, -1.85) if t < tW else (-1.5, -1.6), backa=(-0.8, -1.8), blur=bl,
                hits=[(tW + 0.1, 0.5)], ph=0.5 * i)
    kx, ks = KH4
    kp = kahoda_sit(cr, t, kx, G, ks, mood="shock" if t > tW else ("calm" if t > tV else "read"),
                    tilt=-0.04 * prog(t, tV, 0.4), hits=[(tV, 0.3), (tW, 0.5)], ph=0.9)
    sx, ss = SJ4
    sp = suj(cr, t, sx, G, ss, mood="shock" if t > tV + 0.3 else "open", flip=True, front=(-0.8, -0.9),
             backa=(-0.2, -0.7), ph=0.4)
    bx, by = to_user(cr, sp["belly"])
    lit = prog(t, tB - 0.2, 0.5)
    pulse = 0.5 + 0.5 * math.sin(t * 2.8) + 1.2 * math.exp(-3 * max(0.0, t - tB)) * (t > tB)
    talk = t > tV and math.sin(t * 13) > -0.3
    wx, wy = bx - 4, by - 10
    womb(cr, t, wx, wy, 120 + 30 * lit, 136 + 34 * lit, 0.6 + 0.4 * lit, talk, prog(t, tF, 0.4), pulse,
         flip=True)
    if t > tV:
        sound_rings(cr, wx - 150, wy, t, tV, n=3, rmax=200, alpha=0.6)
    ktop, stop = to_user(cr, kp["top"]), sp["top"]

    def ui(cr):
        head2(cr, t, "ONE NIGHT, FROM THE BELLY:", t0 + 0.05, "A VOICE!", tV, big_size=280)
        tag(cr, t, tB, "MOTHER", min(stop[0] - 10, 950), stop[1] - 80, 32, t_out=tF - 0.3)
        voice_cloud(cr, t, tF - 0.2, 500, 860, 600, 330, [("FATHER,", 66, INK, -100, tF),
                                                          ("YOU'RE READING", 76, INK, -14, tMt),
                                                          ("IT WRONG!", 112, RED, 82, tW)], (wx - 110, wy - 140))
        for i, (dx, ds, _) in enumerate(D4):
            bang(cr, t, tW + 0.1 + 0.12 * i, dx + 30, G - 700 * ds, 90)
        bang(cr, t, tW + 0.05, ktop[0] + 20, ktop[1] - 40, 100)
    return dict(ui=ui, night=0.18, lift=1.0, flash=flash_at(t, tB, 0.2) + flash_at(t, tW, 0.25))


# ------------------------------------------------------------------ a5  ashamed; angry


KH5 = (430, 1.42, 1660)              # the father close: x, scale, hip y


def a_insult(cr, t, tl, t0, t1):
    c = cues(tl, "a5")
    tS, tSh, tA = c["S"], c["Sh"], c["A"]
    glow(cr, 480, 1150, 720, 0.42)
    for i, (dx, ds) in enumerate(((830, 0.5), (990, 0.46))):             # the children whispering behind
        silhouette(cr, lambda c_, dx=dx, ds=ds, i=i: fig(c_, AV.DIS1 if i == 0 else AV.DIS2, f"av_dis{i + 1}", t,
                                                         dx, ds, front=(-1.9, -1.4) if i == 0 else (-0.4, -0.6),
                                                         flip=True, feet=G - 40, ph=0.7 * i, rods=False, blur=3.0),
                   0.55 * prog(t, t0, 0.4))
        if t > tS - 0.2:
            sound_rings(cr, dx - 50, G - 40 - 640 * ds, t, tS - 0.2 + 0.4 * i, n=3, rmax=110, alpha=0.45)
    angry = t > tA - 0.1
    red_glow(cr, 430, 1100, 760, (0.25 * prog(t, tSh, 0.5) + 0.55 * prog(t, tA - 0.1, 0.4)))
    x, s, hy = KH5
    shake = 0.006 * math.sin(t * 21) * prog(t, tA, 0.3)
    kp = kahoda(cr, t, x, s, mood="angry" if angry else "shame", y=hy, rot=shake, front=(-0.3, -0.6) if not angry
                else (-0.5, -1.2), backa=(0.25, -0.3), head=0.1 * (1 - prog(t, tA - 0.1, 0.3)), hits=[(tA, 0.5)],
                ph=0.6)
    hd = to_user(cr, kp["head"])
    if not angry:
        tears(cr, t, tSh + 0.1, (hd[0] - 90, hd[1] - 120), n=3, period=0.9, alpha=0.8)

    def ui(cr):
        if t < tA:
            head2(cr, t, "IN FRONT OF THE CHILDREN,", t0 + 0.05, "ASHAMED", tSh, big_size=270)
        else:
            head2(cr, t, "AND VERY", tA - 0.1, "ANGRY!", tA, big_size=300)
    return dict(ui=ui, flash=flash_at(t, tSh, 0.15) + flash_at(t, tA, 0.3))


# ------------------------------------------------------------------ a6  the curse ("shraap", a bad wish)


KH6 = (250, 0.84)                    # the father standing, pointing
SJ6 = (840, 0.64)                    # the mother, facing left
CURSE_WORD = {"hi": "श्राप", "kn": "ಶಾಪ"}


def a_curse(cr, t, tl, t0, t1):
    c = cues(tl, "a6")
    tC, tY, tBd, tB, tE, tK = c["C"], c["Y"], c["Bd"], c["B"], c["E"], c["K"]
    glow(cr, 540, 1400, 680, 0.38)
    ground(cr)
    sx, ss = SJ6
    sp = suj(cr, t, sx, G, ss, mood="shock" if t > tC else "open", flip=True, front=(-0.8, -0.9), backa=(-0.2, -0.7),
             ph=0.4)
    bx, by = to_user(cr, sp["belly"])
    red = 0.8 * (math.exp(-2.5 * (t - tC)) * (t > tC) + math.exp(-2.5 * (t - tK)) * (t > tK))
    womb(cr, t, bx - 4, by - 8, 104, 118, 1.0, False, 0.0, 0.5 + 0.5 * math.sin(t * 2.6), red, flip=True)
    kx, ks = KH6
    rim = (bx - 104 - 6, by - 30)
    aim = keyed(t, [(t0, (-0.5, -0.6)), (tC - 0.15, (-1.62, 0.0))], 0.3, 1.5)
    cursing = tC - 0.1 < t
    kp = kahoda(cr, t, kx, ks, mood="curse" if cursing and math.sin((t - tC) * 13) > -0.3 else "angry", front=aim,
                backa=(0.35, -0.5), hits=[(tC, 0.5), (tK, 0.4)], ph=0.6)
    if t > tC - 0.1:
        red_glow(cr, kx, G - 500, 640, 0.3 * prog(t, tC - 0.1, 0.4) * (1 - 0.4 * prog(t, tK + 0.6, 0.6)))
    hand = to_user(cr, kp["handF"])
    bolt(cr, t, tC, hand, rim, 1.0)
    bolt(cr, t, tK, hand, rim, 0.8, seed=3)

    def ui(cr):
        head2(cr, t, "THE ANGRY FATHER", t0 + 0.05, "CURSED HIM", tC, big_size=260)
        t_out = tB - 0.3                                                         # the hard word, explained
        script_strip(cr, t, tY - 0.1, CURSE_WORD[lang(tl)], 540, 690, 92, t_out=t_out)
        card2(cr, t, tBd - 0.25, 540, 840, 0.86, [("CURSE =", 70, INK, -50, tBd - 0.1),
                                                  ("A BAD WISH", 110, RED, 46, tBd)], alpha=1 - prog(t, t_out, 0.25))
        card2(cr, t, tB - 0.2, 540, 790, 0.98, [("YOUR BODY WILL BE", 56, INK, -70, tB),
                                                ("CROOKED IN", 56, INK, -14, tE - 0.15),
                                                ("8 PLACES", 86, RED, 58, tE)])
    return dict(ui=ui, flash=flash_at(t, tC, 0.35) + flash_at(t, tE, 0.2) + flash_at(t, tK, 0.15))


# ------------------------------------------------------------------ a7  born crooked; named Ashtavakra: 8 + crooked


SJ7 = (330, 0.86)


def a_named(cr, t, tl, t0, t1):
    c = cues(tl, "a7")
    tBn, tN, tA, tMt, tE = c["Bn"], c["N"], c["A"], c["Mt"], c["E"]
    glow(cr, 420, 1400, 700, 0.45)
    ground(cr)
    sx, ss = SJ7
    hy = G - DV.BENCH_H * ss
    lap = (112.0, -96.0)                                                         # the baby on her lap (body units)
    cx, cy = local(sx, hy, ss, 0.0, False, *lap)
    lit = 0.55 + 0.45 * prog(t, tBn - 0.2, 0.5)
    glow(cr, cx, cy, 400, 0.7 * lit)
    warm(cr, cx, cy, 340, 0.6 * lit)
    aura(cr, t, cx, cy, 100, 320, 0.5 * lit, n=16, spin=0.1)
    rock = 0.04 * math.sin(t * 1.6)

    def baby(cr_):
        cr_.save()
        cr_.translate(*lap)
        cr_.rotate(-0.16 + rock)
        cr_.scale(0.8, 0.8)
        pc.paint_part(cr_, "av_swaddle")
        cr_.restore()
    front = reach_arm(sx, hy, ss, 22, (cx + 70 * ss, cy + 34 * ss))
    backa = reach_arm(sx, hy, ss, -12, (cx - 70 * ss, cy + 30 * ss))
    suj(cr, t, sx, G, ss, mood="smile", belly=False, front=front, backa=backa, tilt=0.08, extra={"av_suj_body": baby},
        ph=0.3)
    lights(cr, t, cx, cy - 40, 220, 8, 0.6 * lit)

    def ui(cr):
        if t < tN:
            head2(cr, t, "THE BABY WAS BORN", t0 + 0.05, "CROOKED", tBn, big_size=290)
        elif t < tMt:
            head2(cr, t, "HIS NAME:", tN - 0.1, "ASHTAVAKRA", tA, big_size=230, under=tA + 0.35)
            script_strip(cr, t, tA + 0.15, NAME[lang(tl)], 540, 780, 90)
        else:
            head2(cr, t, "ASHTAVAKRA MEANS:", tMt - 0.1, "CROOKED IN 8 PLACES", tE, big_size=170)
        for px, word, small, tt in ((262, "ASHTA", "= 8", tMt + 0.2), (818, "VAKRA", "= CROOKED", tE)):
            card(cr, t, max(tt - 0.25, tMt), px, 800, 0.62, [(word, 120, RED, -26), (small, 76, INK, 68)])
        if t > tMt + 0.4:
            draw_text(cr, "+", 540, 800, 120, INK, prog(t, tMt + 0.4, 0.25), anchor="cm")
    return dict(ui=ui, flash=flash_at(t, tBn, 0.15) + flash_at(t, tA, 0.25) + flash_at(t, tE, 0.15))


# ------------------------------------------------------------------ a8  a king's palace; a proud pandit


JN_BACK = (520, G - 40, 0.42)        # the king at the back of his court: x, ground, scale


def court(cr, t, alpha=0.85, blur=2.0, king=True, kmood="calm", kalpha=1.0, hs=1.0):
    glow(cr, 540, 1300, 700, 0.4)
    prop(cr, "sg_hall", 540, G + 6, hs, rot=sway(t, 0.002, 0.3), alpha=alpha, blur=blur)
    pts = {}
    if king:
        jx, jg, js = JN_BACK
        pts = janaka(cr, t, jx, jg, js, mood=kmood, alpha=kalpha, blur=1.5, rods=False, ph=0.8)
    ground(cr)
    return pts


VD8 = (830, 0.78)


def a_palace(cr, t, tl, t0, t1):
    c = cues(tl, "a8")
    tF, tK, tP, tGh, tPd = c["F"], c["K"], c["P"], c["Gh"], c["Pd"]
    jp = court(cr, t, kmood="calm")
    t_stop = min(tP + 0.3, t0 + 1.8)
    if t < t_stop:
        kahoda_walk(cr, t, t0 - 0.2, t_stop, -160, 230, 0.64, mood="calm", ph=0.6)
    else:
        kahoda(cr, t, 230, 0.64, mood="calm", head=-0.04 * prog(t, tGh, 0.3), hits=[(tGh, 0.3)], ph=0.6)
    vx, vs = VD8
    if t > tGh - 0.45:
        b, k, a = depth(t, tGh - 0.45, 0.5)
        vandin(cr, t, vx, vs * k, mood="smirk", flip=True, front=(-0.75, -1.75), backa=(-0.6, -1.7),
               head=-0.12, y=G - 434 * vs * k - (k - 1) * 200, alpha=a, blur=b, hits=[(tGh, 0.4)], ph=1.1)
    jtop = to_user(cr, jp["top"]) if jp else (520, 1200)

    def ui(cr):
        if t < tGh:
            head2(cr, t, "ONE DAY, FATHER WENT TO", t0 + 0.05, "A KING'S PALACE", tP, big_size=210)
        else:
            head2(cr, t, "THERE LIVED A", tGh - 0.15, "PROUD PANDIT", tPd, big_size=250, under=tPd + 0.3)
        tag(cr, t, tF + 0.1, "FATHER", 230, 1010, 34, t_out=tGh - 0.2)
        tag(cr, t, tK + 0.15, "THE KING", jtop[0], jtop[1] - 60, 32, t_out=tGh - 0.2)
    return dict(ui=ui, flash=flash_at(t, tP, 0.15) + flash_at(t, tPd, 0.2))


# ------------------------------------------------------------------ a9  his game: lose and go into the water


VD9 = (300, 0.98)
LAKE9 = 1560                         # the lake's edge (by the court)


def a_rule(cr, t, tl, t0, t1):
    c = cues(tl, "a9")
    tKh, tQ, tL, tW, tDr = c["Kh"], c["Q"], c["L"], c["W"], c["Dr"]
    glow(cr, 540, 1300, 700, 0.38)
    prop(cr, "sg_hall", 540, G + 6, 1.0, alpha=0.45, blur=6.0)
    ground(cr)
    lit = 0.35 + 0.5 * prog(t, tW - 0.1, 0.5)
    cool(cr, 860, LAKE9 + 160, 520, lit)
    glow(cr, 860, LAKE9 + 120, 420, 0.4 * lit)
    water(cr, t, LAKE9 + 40, rows=6, s=0.8, x0=560)
    ledge(cr, 560, W + 20, LAKE9)
    if t > tW:
        ripple(cr, 840, LAKE9 + 70, t, tW, 3, 0.5, 220)
        bubbles(cr, t, 860, LAKE9 + 180, 160, 6, 0.6 * prog(t, tW, 0.4))
    x, s = VD9
    up = keyed(t, [(t0, 0.0), (tKh - 0.1, 1.0)], 0.3, 1.5)
    vp = vandin(cr, t, x, s, mood="speak" if (tKh < t < tDr + 0.5 and math.sin(t * 14) > 0) else "smirk",
                front=mix((-0.4, -0.6), (-2.7, -0.25), up), backa=(0.2, -0.35), head=-0.08,
                hits=[(tKh, 0.3), (tL, 0.3)], ph=1.1)
    hand = to_user(cr, vp["handF"])

    def ui(cr):
        if t < tL - 0.15:
            head2(cr, t, "THE PANDIT'S GAME:", t0 + 0.05, "QUESTIONS & ANSWERS", tQ, big_size=150)
            if t > tQ:                                                           # a question, then an answer
                num_disc(cr, hand[0] + 150, hand[1] + 40, 54, "?", prog(t, tQ, 0.25), 0.1 * math.sin(t * 3), RED)
                num_disc(cr, hand[0] + 290, hand[1] + 90, 54, "!", prog(t, tQ + 0.35, 0.25), -0.1, INK)
        else:
            head2(cr, t, "THE LOSER GOES", tL - 0.15, "INTO THE WATER", tDr, big_size=220)
        rule_card(cr, t, tL - 0.3, 700, 880, 0.74, tL - 0.1, tDr)
    return dict(ui=ui, flash=flash_at(t, tQ, 0.15) + flash_at(t, tDr, 0.25))


# ------------------------------------------------------------------ a10  the father lost; into the water


KH10 = (540, 0.86)
LAKE10 = 1500


def a_lost(cr, t, tl, t0, t1):
    c = cues(tl, "a10")
    tL, tW, tD = c["L"], c["W"], c["D"]
    prop(cr, "sg_hall", 540, G - 80, 0.9, alpha=0.35, blur=8.0)
    sink = ease(clamp((t - tW) / max(1.2, t1 - tW + 0.3)))
    blue = prog(t, tW - 0.2, 0.8)
    cool(cr, 540, LAKE10 + 120, 760, 0.45 + 0.45 * blue)
    glow(cr, 540, LAKE10 - 120, 560, 0.5)
    x, s = KH10
    bowed = t > tL - 0.1
    fold = prog(t, tW - 0.4, 0.4)
    kp = kahoda(cr, t, x, s, mood="bow" if bowed else "calm", feet=LAKE10 + 330 + 700 * sink,
                front=mix((-0.32, -0.55), ANJALI["front"], fold), backa=mix((0.3, -0.25), ANJALI["backa"], fold),
                head=0.14 * prog(t, tL - 0.1, 0.4), hits=[(tL, 0.4)], ph=0.6, rods=sink < 0.9,
                alpha=1 - 0.5 * prog(t, tD + 1.0, 1.0))
    water(cr, t, LAKE10, rows=9, s=0.84, step=52)
    if t > tW:
        ripple(cr, x, LAKE10 + 10, t, tW + 0.2, 3, 0.55, 300)
        bubbles(cr, t, x, LAKE10 + 120, 200, 9, 0.8 * prog(t, tW, 0.5))
        top = to_user(cr, kp["top"])
        if top[1] > LAKE10 - 40:
            glow(cr, x, LAKE10 + 160, 360, 0.6 * prog(t, tD, 0.6))

    def ui(cr):
        if t < tW:
            head2(cr, t, "FATHER", t0 + 0.05, "LOST", tL, big_size=300)
        else:
            head2(cr, t, "AND WAS PUT INTO", tW - 0.1, "THE WATER", tD, big_size=260)
    return dict(ui=ui, flash=flash_at(t, tL, 0.15), blue=0.25 * blue)


# ------------------------------------------------------------------ a10q  the question: will he ever see his father?


LAKEQ = 1640


def a_question(cr, t, tl, t0, t1):
    c = cues(tl, "a10q")
    tCh, tP, tD = c["Ch"], c["P"], c["D"]
    cool(cr, 540, LAKEQ + 100, 760, 0.6)
    water(cr, t, LAKEQ, rows=5, s=0.84)
    bubbles(cr, t, 760, LAKEQ + 60, 260, 6, 0.6)
    sx, ss = (230, 0.66)
    gq = LAKEQ - 34 + 48                                                         # the top of the bank she sits on
    bank(cr, LAKEQ - 34, x1=360)
    hy = gq - DV.BENCH_H * ss
    lap = (112.0, -96.0)
    cx, cy = local(sx, hy, ss, 0.0, False, *lap)
    glow(cr, cx, cy, 300, 0.6)

    def baby(cr_):
        cr_.save()
        cr_.translate(*lap)
        cr_.rotate(-0.16 + 0.04 * math.sin(t * 1.6))
        cr_.scale(0.8, 0.8)
        pc.paint_part(cr_, "av_swaddle")
        cr_.restore()
    front = reach_arm(sx, hy, ss, 22, (cx + 70 * ss, cy + 34 * ss))
    backa = reach_arm(sx, hy, ss, -12, (cx - 70 * ss, cy + 30 * ss))
    suj(cr, t, sx, gq, ss, mood="open", belly=False, front=front, backa=backa, tilt=0.1, extra={"av_suj_body": baby},
        ph=0.3)

    def ui(cr):
        card2(cr, t, t0 + 0.05, 540, 520, 1.0, [("WILL HE EVER", 84, INK, -46, t0 + 0.15),
                                                ("SEE FATHER?", 110, RED, 50, tP)])
        q = back(clamp((t - tCh) / 0.4), 1.6)                                     # the big red question mark
        if q > 0.01:
            cr.save()
            cr.translate(720, 1130)
            cr.rotate(0.1 * math.sin(t * 2.2) + 0.3 * (1 - q))
            cr.scale(q, q)
            glow(cr, 0, 0, 380, 0.5 * clamp(q))
            draw_text(cr, "?", 0, 0, 560, RED, clamp(q), anchor="cm")
            cr.restore()
        if t > tD:
            red_ring(cr, 720, 1150, 220, 300, prog(t, tD, 0.4), 10)
    return dict(ui=ui, flash=flash_at(t, tCh, 0.2), blue=0.15)


# ------------------------------------------------------------------ a11  12 years later; he found out; to the palace


BOY11 = (560, 0.62)


def a_years(cr, t, tl, t0, t1):
    c = cues(tl, "a11")
    tY, tA, tT, tBd, tP = c["Y"], c["A"], c["T"], c["Bd"], c["P"]
    glow(cr, 540, 1350, 700, 0.4)
    prop(cr, "lr_hut", 210, G + 10, 0.62, alpha=0.8, blur=3.0)
    prop(cr, "tree", 960, G + 10, 0.66, rot=sway(t, 0.005, 0.3), alpha=0.75, blur=4.0)
    ground(cr)
    spin = clamp((t - t0) / max(0.8, tA - t0))
    if t < tA + 0.3:
        sun_arc(cr, t, 540, 960, 300, (spin * 6.0) % 1.0, prog(t, t0, 0.2) * (1 - prog(t, tA, 0.3)))
    bx, bs = BOY11
    bp = {}
    if t > tA - 0.4:
        if t < tBd:
            b, k, a = depth(t, tA - 0.4, 0.5)
            bp = boy(cr, t, bx, bs * k, mood="firm" if t > tT + 0.3 else "calm", y=G - 434 * bs * k - (k - 1) * 200,
                     alpha=a, blur=b, head=0.04 * prog(t, tT, 0.4) - 0.04 * prog(t, tT + 0.8, 0.4),
                     hits=[(tT, 0.4)], ph=0.4)
        else:
            bp, _ = boy_walk(cr, t, tBd, tBd + 3.6, bx, 1180, bs, mood="firm", ph=0.4)

    def vision(cr_):
        cool(cr_, 790, 940, 260, 0.7)
        fake = ease(clamp((t - tT - 0.3) / 1.4))
        silhouette(cr_, lambda c_: fig(c_, AV.KAHODA, "av_kahoda", t, 790, 0.26, front=ANJALI["front"],
                                       backa=ANJALI["backa"], y=900 + 120 * fake, rods=False, ph=0.5), 0.8)
        for i in range(3):
            off = (t * 30 * (1 if i % 2 else -0.8)) % (R.WAVE_P * 0.3)
            prop(cr_, "rv_waveA" if i % 2 == 0 else "rv_waveB", 790 + off - 24, 980 + 26 * i, 0.3)

    def ui(cr):
        if t < tA:
            head2(cr, t, "12 YEARS", t0 + 0.05, "LATER", tY + 0.2, big_size=290)
        elif t < tT:
            head2(cr, t, "THE BABY GREW UP:", tA - 0.15, "ASHTAVAKRA", tA + 0.05, big_size=220)
        elif t < tBd:
            head2(cr, t, "HE FOUND OUT", tT - 0.15, "THE TRUTH", tT, big_size=270)
        else:
            head2(cr, t, "WITH HIS CROOKED BODY,", tBd - 0.1, "TO THE PALACE!", tP, big_size=220)
        n = 1 + int(11 * clamp((t - t0 - 0.1) / max(0.6, tA - t0 - 0.5)))
        counter_badge(cr, t, t0 + 0.05, f"{n} YEAR{'S' if n > 1 else ''}", 540, 820, 96, RED,
                      alpha=1 - prog(t, tA + 0.1, 0.25))
        if bp:
            top = to_user(cr, bp["top"])
            if t < tT:
                tag(cr, t, tA + 0.2, "ASHTAVAKRA, AGE 12", min(max(top[0], 260), 820), top[1] - 70, 28)
            bubble(cr, t, tT - 0.1, 790, 960, 150, vision, src=(top[0] + 40, top[1] - 10), t_out=tBd - 0.1)
    return dict(ui=ui, flash=flash_at(t, tA, 0.15) + flash_at(t, tT, 0.2))


# ------------------------------------------------------------------ a12  the door: not age, brains


GATE = (760, 0.98)
GD12 = (740, 0.66)
BOY12 = (330, 0.66 * BK)


def a_gate(cr, t, tl, t0, t1):
    c = cues(tl, "a12")
    tS, tN, tA, tG, tK = c["S"], c["N"], c["A"], c["G"], c["K"]
    glow(cr, 540, 1350, 700, 0.42)
    prop(cr, "sg_hall", 540, G - 60, 0.86, alpha=0.4, blur=7.0)
    gx, gs = GATE
    prop(cr, "sx_door_frame", gx, G + 6, gs)
    ground(cr)
    t_ok = tK + 0.6
    spear = keyed(t, [(t0, 0.0), (tS - 0.1, 1.0), (t_ok, 0.0)], 0.3, 1.4)
    gdx = keyed(t, [(t0, 0.0), (t_ok + 0.2, 1.0)], 0.5, 1.1)
    gx2, gsc = GD12
    guard(cr, t, gx2 + 150 * gdx, gsc, spear=spear, flip=True, hits=[(tS, 0.4)], ph=0.9)
    bx, bs = BOY12
    if t < t0 + 1.2:
        boy_walk(cr, t, t0 - 0.4, t0 + 1.2, 80, bx, bs, mood="calm", ph=0.4)
    elif t < t_ok + 0.4:
        speak = tA < t < tK + 0.5 and math.sin(t * 14) > -0.2
        boy(cr, t, bx, bs, mood="speak" if speak else "firm", front=(-0.95, -0.35) if t < tA else (-1.3, -0.45),
            head=-0.06 * prog(t, tA, 0.3), hits=[(tA, 0.4), (tK, 0.3)], ph=0.4)
    else:
        boy_walk(cr, t, t_ok + 0.4, t_ok + 2.4, bx, 620, bs, mood="smile", ph=0.4)

    def ui(cr):
        if t < tA:
            head2(cr, t, "AT THE DOOR:", t0 + 0.05, "STOPPED!", tS, big_size=290)
        else:
            head2(cr, t, "ASHTAVAKRA SAID:", tA - 0.1, None, 0.0)
        cloud_text(cr, t, 640, 830, 0.66, [("NO CHILDREN!", 100, RED, 4, tN)], flip=True, t_in=tN - 0.2,
                   alpha=1 - prog(t, tA - 0.15, 0.25))
        cloud_text(cr, t, 500, 790, 1.0, [("AGE? NO!", 84, INK, -104, tG), ("BRAINS MAKE", 104, RED, 2, tK),
                                          ("YOU BIG!", 104, RED, 104, tK + 0.2)], t_in=tG - 0.25,
                   alpha=1 - prog(t, t_ok + 1.0, 0.3))
    return dict(ui=ui, flash=flash_at(t, tS, 0.15) + flash_at(t, tK, 0.25))


# ------------------------------------------------------------------ a13  the little boy beat the proud pandit


BOY13 = (240, 0.72 * BK)
VD13 = (860, 0.74)


def a_debate(cr, t, tl, t0, t1):
    c = cues(tl, "a13")
    tCh, tPd, tQ, tWn = c["Ch"], c["Pd"], c["Q"], c["Wn"]
    court(cr, t, kmood="wonder" if t > tWn + 0.2 else "calm", hs=0.9)
    won = t > tWn
    bx, bs = BOY13
    if won:
        glow(cr, bx + 40, G - 420, 520, 0.6 * prog(t, tWn, 0.4))
        aura(cr, t, bx + 30, G - 520 * bs - 120, 120, 420, 0.7 * prog(t, tWn, 0.4), n=18, spin=0.1)
    t_qa0, t_qa1 = min(tQ, tCh + 0.3), tWn - 0.2                                  # questions and answers fly
    n_qa = max(2, int((t_qa1 - t_qa0) / 0.55))
    step = (t_qa1 - t_qa0) / n_qa
    k_qa = int((t - t_qa0) / step) if t_qa0 < t < t_qa1 else -1
    talk_v = k_qa >= 0 and k_qa % 2 == 0
    talk_b = k_qa >= 0 and k_qa % 2 == 1
    bp = boy(cr, t, bx, bs, mood="smile" if won else ("speak" if talk_b and math.sin(t * 14) > 0 else "firm"),
             front=(-1.3, -0.45) if talk_b or won else (-0.95, -0.35), hits=[(tWn, 0.5)], ph=0.4)
    vx, vs = VD13
    stag = keyed(t, [(t0, 0.0), (tWn, 1.0)], 0.35, 1.8)
    vmood = "shock" if won else ("speak" if talk_v and math.sin(t * 14) > 0 else "smirk")
    vp = vandin(cr, t, vx + 70 * stag, vs, mood=vmood, flip=True, rot=0.06 * stag,
                front=(-1.8, -0.4) if talk_v else ((-1.0, -2.0) if won else (-0.6, -1.0)), backa=(-0.3, -0.9),
                head=0.06 * stag - 0.08 * (1 - stag), hits=[(tWn, 0.6)], ph=1.1)
    bm = to_user(cr, bp["head"])
    vm = to_user(cr, vp["head"])
    burst(cr, t, bx + 30, G - 520 * bs, tWn, n=20, rmax=620)

    def ui(cr):
        if t < tWn:
            head2(cr, t, "LITTLE BOY VS", t0 + 0.05, "PROUD PANDIT", tPd, big_size=250)
        else:
            head2(cr, t, "THE LITTLE BOY", tWn - 0.1, "WON!", tWn, big_size=320, under=tWn + 0.35)
        for i in range(n_qa):
            ti = t_qa0 + step * i
            if t < ti:
                break
            u = (t - ti) / 0.7
            if u > 1:
                continue
            src, dst = (vm, bm) if i % 2 == 0 else (bm, vm)
            px = src[0] + (dst[0] - src[0]) * 0.5 * ease(clamp(u))
            py = src[1] - 140 - 160 * math.sin(math.pi * clamp(u) * 0.5)
            num_disc(cr, px, py, 50, "?" if i % 2 == 0 else "!", clamp(u * 4) * (1 - clamp((u - 0.7) / 0.3)),
                     0.1 * math.sin(t * 3 + i), RED if i % 2 == 0 else INK)
        if won:
            plate(cr, t, tWn + 0.3, "PANDIT: STUNNED", min(vm[0] - 20, 860), vm[1] - 300, 28)
    return dict(ui=ui, flash=flash_at(t, tPd, 0.15) + flash_at(t, tWn, 0.4))


# ------------------------------------------------------------------ a14  the twist: nobody died; with the water god


VD14 = (250, 0.86)
LAKE14 = 1560
BUB14 = (690, 1120, 290)             # the glimpse under the water: x, y, radius


def a_secret(cr, t, tl, t0, t1):
    c = cues(tl, "a14")
    tS, tM, tD, tZ = c["S"], c["M"], c["D"], c["Z"]
    prop(cr, "sg_hall", 540, G - 70, 0.9, alpha=0.35, blur=7.0)
    blue = prog(t, tD - 0.3, 0.8)
    cool(cr, 540, LAKE14 + 100, 760, 0.4 + 0.4 * blue)
    water(cr, t, LAKE14, rows=5, s=0.84)                                         # the lake behind him
    bubbles(cr, t, 700, LAKE14 + 60, 380, 10, 0.6 * blue)
    ground(cr)
    x, s = VD14
    speak = tS < t < tZ + 0.6 and math.sin(t * 14) > 0
    vp = vandin(cr, t, x, s, mood="speak" if speak else "calm", front=(-1.1, -0.9) if t < tD else (-1.6, -0.2),
                backa=(0.2, -0.4), head=0.04, hits=[(tM, 0.4), (tD, 0.3)], ph=1.1)
    vm = to_user(cr, vp["head"])
    bx, by, br = BUB14

    def below(cr_):
        """Under the water: the water god (a tall glowing figure with a crown and a blue light) with the drowned
        before him, hands folded, alive; the father in front."""
        cool(cr_, bx, by, br * 1.2, 0.9)
        aura(cr_, t, bx, by - 110, 90, 300, 0.8, n=18, col=(0.30, 0.62, 1.0), spin=0.1)
        deva(cr_, t, bx, 0.44, pose="stand", feet=by + 200, ph=0.4)
        people = prog(t, tD + 0.35, 0.5)
        for k, (dx, fl) in enumerate(((-170, False), (170, True))):
            silhouette(cr_, lambda c_, dx=dx, fl=fl, k=k: fig(c_, AV.DIS1 if k == 0 else AV.DIS2, f"av_dis{k + 1}", t,
                                                               bx + dx, 0.27, front=ANJALI["front"],
                                                               backa=ANJALI["backa"], flip=fl, feet=by + 230,
                                                               rods=False, ph=k), 0.8 * people)
        kahoda(cr_, t, bx - 60, 0.3, mood="smile", front=ANJALI["front"], backa=ANJALI["backa"], feet=by + 250,
               rods=False, alpha=people, ph=0.6)
        for i in range(3):
            off = (t * 26 * (1 if i % 2 else -0.8)) % (R.WAVE_P * 0.4)
            prop(cr_, "rv_waveA" if i % 2 == 0 else "rv_waveB", bx + off - 32, by - br + 30 + 20 * i, 0.4, alpha=0.5)
        bubbles(cr_, t, bx, by, br * 0.8, 8, 0.8)

    def ui(cr):
        if t < tM:
            head2(cr, t, "THEN THE PANDIT TOLD", t0 + 0.05, "A SECRET", tS, big_size=280)
        elif t < tD:
            head2(cr, t, "HE SAID:", tM - 0.1, "NOBODY DIED!", tM + 0.05, big_size=250)
        else:
            head2(cr, t, "ALL ALIVE, WITH", tD - 0.1, "THE WATER GOD", tD + 0.1, big_size=220)
        q = ease(clamp((t - tD + 0.1) / 0.7))                                    # the slow reveal
        if q > 0.01:
            bubble(cr, t, tD - 0.1, bx, by, br * (0.55 + 0.45 * q), below, src=(vm[0] + 70, vm[1] - 30))
        tag(cr, t, tZ, "ALIVE!", bx + 120, by - br - 20, 40)
        tag(cr, t, tZ + 0.35, "FATHER", bx - 70, by + 270, 28)
    return dict(ui=ui, flash=flash_at(t, tM, 0.2) + flash_at(t, tD, 0.3), blue=0.12 * blue)


# ------------------------------------------------------------------ a15  father back alive; the river: straight


LAKE15 = 1520
RIV = 1540
BOY16 = (560, 0.84 * BK)
KH16 = (800, 0.62)


def bank(cr, y, x1=232):
    """The near bank on the left: earth and grass with a slanted edge into the water."""
    cr.save()
    pts = [(-60, y + 36), (x1, y + 36), (x1 + 68, y + 160), (x1 + 118, H + 60), (-60, H + 60)]
    pc.poly(cr, pts)
    cr.clip()
    prop(cr, "ground", 0, y + 42, 0.82)
    pc.poly(cr, [(-60, y + 150), (x1 + 170, y + 150), (x1 + 170, H + 60), (-60, H + 60)])
    cr.set_source_rgb(0.40, 0.27, 0.13)
    cr.fill()
    cr.restore()
    pc.poly(cr, pts[1:4], closed=False)
    cr.set_source_rgb(*pc.INK)
    cr.set_line_width(5)
    cr.stroke()


def a_back(cr, t, tl, t0, t1):
    c = cues(tl, "a15")
    tW, tL, tN, tS = c["W"], c["L"], c["N"], c["S"]
    cut = tN - 0.3
    if t < cut:                                                                  # the father rises from the water
        prop(cr, "sg_hall", 540, G - 60, 0.86, alpha=0.35, blur=7.0)
        cool(cr, 600, LAKE15 + 100, 820, 0.8)
        glow(cr, 640, LAKE15 - 100, 640, 0.45 + 0.15 * math.sin(t * 3.0))
        bubbles(cr, t, 640, LAKE15 + 40, 360, 10, 0.8 * prog(t, t0, 0.3), ph=0.3)
        tr = min(tW, t0 + 0.2)
        span = max(1.0, tL + 0.4 - tr)
        u = ease(clamp((t - tr) / span))
        hy = LAKE15 + 640 + (110 - 434 * 0.7 - 640) * u
        glow(cr, 650, hy - 260, 480, 0.8 * u)
        aura(cr, t, 650, hy - 400, 120, 420, 0.7 * u, n=18, spin=0.1)
        kahoda(cr, t, 650, 0.7, mood="smile" if u > 0.8 else "bow", y=hy, flip=True,
               front=ANJALI["front"] if t < tL + 0.3 else mix(ANJALI["front"], (-1.4, -0.3), prog(t, tL + 0.3, 0.4)),
               backa=ANJALI["backa"] if t < tL + 0.3 else (-1.2, -0.4), rods=u > 0.5, ph=0.6)
        water(cr, t, LAKE15, rows=9, s=0.84, step=52)
        ripple(cr, 650, LAKE15 + 10, t, tr, 3, 0.6, 260, 0.8)
        bank(cr, LAKE15 - 30)
        boy(cr, t, 160, 0.66 * BK, mood="smile" if t > tL else "wonder", feet=LAKE15 + 6, hits=[(tL, 0.4)], ph=0.4)
        out = dict(flash=flash_at(t, tL, 0.3), blue=0.1)
    else:                                                                        # the river: he pours, the boy rises
        glow(cr, 540, 1350, 720, 0.42)
        prop(cr, "tree", 70, RIV + 40, 0.58, rot=sway(t, 0.005, 0.3), alpha=0.7, blur=4.0)
        prop(cr, "tree", 1040, RIV + 40, 0.62, rot=sway(t, 0.005, 0.3, 1.0), alpha=0.7, blur=4.0)
        bx, bs = BOY16
        t_up = tS - 0.15
        up = ease(clamp((t - t_up) / 0.8))
        straight = t > t_up
        joy = prog(t, tS + 0.1, 0.4)
        feet = RIV + 250 - 190 * up
        if straight:
            glow(cr, bx, feet - 520 * bs, 520, 0.75 * up)
            warm(cr, bx, feet - 520 * bs, 420, 0.7 * up)
            aura(cr, t, bx, feet - 560 * bs, 120, 460, 0.8 * up, n=20, spin=0.12)
        boy(cr, t, bx, bs, mood=("smile" if joy > 0.5 else "shut") if straight else "shut", bent=not straight,
            staff=False, feet=feet, front=(-0.3, -0.5) if not straight else mix((-0.3, -0.5), (-2.6, -0.3), joy),
            backa=(0.3, -0.4) if not straight else mix((0.3, -0.4), (-2.5, -0.4), joy), head=0.08 * (not straight),
            hits=[(t_up, 0.5), (tS, 0.4)], ph=0.4, rods=False)
        kx, ks = KH16                                                            # the father pours the water
        pour = (-2.3, -0.5)
        kp = kahoda(cr, t, kx, ks, mood="smile", flip=True, front=pour, backa=(-0.6, -0.9), feet=RIV + 300,
                    extra={"av_kahoda_armF_lo": held("md_kalasha", pour, 0.32, 168, 1.35)}, rods=False, ph=0.6)
        hand = to_user(cr, kp["handF"])
        if cut + 0.2 < t < t_up + 0.3:                                           # the water falling on his head
            for i in range(9):
                u = ((t - cut) * 1.6 + i / 9) % 1.0
                px = hand[0] - 80 + (bx + 30 - hand[0] + 80) * u * 0.5
                py = hand[1] - 40 + (feet - 640 * bs - hand[1] + 40) * u
                prop(cr, "rv_drop", px + 6 * math.sin(i * 2.1), py, 1.3, alpha=0.9)
        water(cr, t, RIV, rows=8, s=0.84, step=54, river=True)
        ripple(cr, bx, RIV + 20, t, cut + 0.3, 3, 0.5, 260)
        if t > t_up:
            ripple(cr, bx, RIV + 20, t, t_up, 3, 0.45, 320)
            lights(cr, t, bx, feet - 600 * bs, 260, 14, 0.8 * up)
        burst(cr, t, bx, feet - 560 * bs, t_up, n=22, rmax=700)
        out = dict(flash=flash_at(t, cut, 0.3) + flash_at(t, t_up, 0.45))

    def ui(cr):
        if t < cut:
            head2(cr, t, "FROM THE WATER, FATHER", t0 + 0.05, "CAME BACK ALIVE!", tL, big_size=200)
        elif t < tS - 0.2:
            head2(cr, t, "FATHER BATHED HIM", cut + 0.05, "IN THE RIVER", tN, big_size=240)
        else:
            head2(cr, t, "AND HIS BODY BECAME", tS - 0.2, "STRAIGHT!", tS, big_size=300, under=tS + 0.35)
    out["ui"] = ui
    return out


# ------------------------------------------------------------------ a15c  the callback: his words saved his father


def a_callback(cr, t, tl, t0, t1):
    c = cues(tl, "a15c")
    tP, tU, tV = c["P"], c["U"], c["V"]
    pulse = 0.5 + 0.5 * math.sin(t * 2.6) + 1.2 * math.exp(-3 * max(0.0, t - tU)) * (t > tU)
    talk = tU < t and math.sin(t * 13) > -0.3
    red = 0.7 * math.exp(-2.5 * (t - tP)) * (t > tP)                            # the old punishment, a red flicker
    (cx, cy), _ = hook_mother(cr, t, 1.0, talk, pulse, beats=(t0 + 0.3, tP), mood="smile" if t > tV else "open",
                              red=red)
    fx, fs = HK_F
    if t > tU - 0.3:                                                             # the father, back and smiling
        b, k, a = depth(t, tU - 0.3, 0.5)
        warm(cr, fx, HK[1] - 600 * fs, 420, 0.6 * prog(t, tV, 0.4))
        aura(cr, t, fx - 20, HK[1] - 830 * fs, 100, 360, 0.6 * prog(t, tV, 0.4), n=16, spin=0.1)
        kahoda(cr, t, fx, fs * k, mood="smile", flip=True, front=(-1.4, -0.4), backa=(-1.2, -0.5),
               y=HK[1] - 434 * fs * k - (k - 1) * 200, alpha=a, blur=b, hits=[(tV, 0.3)], ph=0.6)
        lights(cr, t, (cx + fx) / 2, cy - 200, 240, 10, 0.7 * prog(t, tV, 0.4))

    def ui(cr):
        if t < tU - 0.1:
            head2(cr, t, "PUNISHED FOR", t0 + 0.05, "SPEAKING...", tP, big_size=260)
        else:
            head2(cr, t, "BUT HIS WORDS", tU - 0.1, "SAVED FATHER!", tV - 0.1, big_size=230, under=tV + 0.35)
        if t > tU - 0.1:
            sound_rings(cr, cx + 200, cy - 120, t, tU - 0.1, n=4, rmax=260, alpha=0.6)
    return dict(ui=ui, flash=flash_at(t, tU, 0.15) + flash_at(t, tV, 0.25))


# ------------------------------------------------------------------ a16  whose fault?


def a_end(cr, t, tl, t0, t1):
    c = cues(tl, "a16")
    tQ, tS, tF, tC = c["Q"], c["S"], c["F"], c["C"]
    glow(cr, 540, 1450, 640, 0.45)
    ground(cr)
    sp = suj(cr, t, 190, G, 0.7, mood="open", front=(-0.6, -0.9), backa=(-0.2, -0.7), ph=0.3)
    bx, by = to_user(cr, sp["belly"])
    womb(cr, t, bx + 4, by - 8, 112, 126, 1.0, prog(t, tS, 0.2) > 0.5, 0.6 + 0.4 * prog(t, tS, 0.4),
         0.5 + 0.5 * math.sin(t * 2.6) + 0.8 * math.exp(-3 * max(0.0, t - tS)) * (t > tS))
    kahoda(cr, t, 850, 0.74, mood="curse" if t > tF else "angry", flip=True,
           front=(-1.55, -0.05) if t > tF - 0.2 else (-0.5, -0.6), backa=(0.3, -0.4), hits=[(tF, 0.4)], ph=0.6)
    cards = ((285, "THE SON?", tS - 0.1), (795, "THE FATHER?", tF - 0.1))

    def ui(cr):
        head2(cr, t, "SO,", t0 + 0.05, "WHOSE FAULT?", tQ, big_size=250)
        for cx, txt, tc in cards:
            card(cr, t, tc - 0.25, cx, 780, 0.64, [(txt, 124 if len(txt) < 9 else 100, RED, 4)])
        if t > tF + 0.3:
            n = int((t - tF - 0.3) / 0.9)
            k = n % 2
            red_ring(cr, cards[k][0], 784, 256, 104, prog(t, tF + 0.3 + 0.9 * n, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tC, 0.15))


# ------------------------------------------------------------------ the cut list and the frame


SHOTS = [   # (line, draw function, options)
    ("a1", a_hook, {"z": (1.0, 1.04), "focus": (480, 1250)}),
    ("a2", a_book, {"z": (1.0, 1.03)}),
    ("a3", a_guru, {"z": (1.0, 1.03)}),
    ("a4", a_voice, {"z": (1.0, 1.04), "focus": (600, 1300)}),
    ("a5", a_insult, {"z": (1.0, 1.05), "focus": (430, 1100)}),
    ("a6", a_curse, {"z": (1.0, 1.03)}),
    ("a7", a_named, {"z": (1.0, 1.03)}),
    ("a8", a_palace, {"z": (1.0, 1.03)}),
    ("a9", a_rule, {"z": (1.0, 1.04)}),
    ("a10", a_lost, {"z": (1.0, 1.04)}),
    ("a10q", a_question, {"z": (1.0, 1.05), "focus": (540, 900)}),
    ("a11", a_years, {"z": (1.0, 1.03)}),
    ("a12", a_gate, {"z": (1.0, 1.03)}),
    ("a13", a_debate, {"z": (1.0, 1.03)}),
    ("a14", a_secret, {"z": (1.0, 1.03)}),
    ("a15", a_back, {"z": (1.0, 1.03)}),
    ("a15c", a_callback, {"z": (1.0, 1.04), "focus": (480, 1250)}),
    ("a16", a_end, {"z": (1.0, 1.03)}),
]


def shot_at(t, tl):
    """(index, start, end) of the shot showing at t: each shot runs from its line's start to the next line's start
    (cached on the timeline under _av_shots)."""
    cache = getattr(tl, "_av_shots", None)
    if cache is None:
        starts = [0.0]
        for bid, _, _ in SHOTS[1:]:
            starts.append(max(T(tl, bid) - 0.12, starts[-1] + 0.5))
        cache = tl._av_shots = starts
    k = 0
    for i, s in enumerate(cache):
        if t >= s:
            k = i
    return k, cache[k], cache[k + 1] if k + 1 < len(cache) else tl.total


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl)
    _, fn, opt = SHOTS[k]
    z0, z1 = opt.get("z", (1.0, 1.03))
    z = z0 + (z1 - z0) * clamp((t - t0) / max(0.5, t1 - t0))
    fx, fy = opt.get("focus", (540, 1060))
    cr.save()
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    pc.screen(cr)
    out = fn(cr, t, tl, t0, t1) or {}
    tint(cr, (1.0, 0.66, 0.42), out.get("eve", 0.0))
    tint(cr, (0.55, 0.72, 1.0), out.get("blue", 0.0))
    cr.restore()
    motes(cr, t)
    pc.lamp(cr, t, night=out.get("night", 0.0), flash=out.get("flash", 0.0))
    sepia(cr, out.get("sepia", 0.0))
    title_lift(cr, out.get("lift", 0.0) * out.get("night", 0.0) / NIGHT)
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a conch
    at the father's curse, a single hit as the little boy wins, shimmer as his body becomes straight, a bell on the
    closing question, then (only where they fit) shimmer at the twist (all alive, with the water god) and a bell at the
    name. Chosen in THAT order of importance, each at least SFX_MIN_GAP from every sound already kept (as
    render_myth.calm_sfx keeps them), so the list returned is what plays (about 6 sounds); the bed dips before the
    reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    t_str = c["a15"]["S"] - 0.15                                     # the body becomes straight
    t_end = min(max(c["a16"]["F"], t_str + SFX_MIN_GAP + 0.05), tl["a16"].end - 0.05)   # the question's bell
    t_name = min(max(c["a7"]["A"], c["a6"]["C"] + SFX_MIN_GAP + 0.05), tl["a7"].end)     # the name's bell
    want = [(0.0, "damaru", 0), (c["a6"]["C"], "conch", 0), (c["a13"]["Wn"], "hit", 0), (t_str, "shimmer", 0),
            (t_end, "bell", 0), (c["a14"]["D"], "shimmer", 0), (t_name, "bell", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["a6"]["C"] - 0.3, "dip", 0.45), (c["a13"]["Wn"] - 0.35, "dip", 0.5), (c["a14"]["D"] - 0.3, "dip", 0.45),
            (t_str - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
