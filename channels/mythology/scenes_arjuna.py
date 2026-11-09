"""Scenes for videos/arjuna.py: "Arjuna raises his sword on his own elder brother" (Krishna's two tricks), in Togalu
Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen, two-tier headlines and
rod-puppet motion as the Jarasandha, Kaikeyi, Lakshman Rekha, Mandhata and Jayadratha reels, with the cast from
arjuna_cast. Told so a child can follow (owner, 9 Nov 2026: "explain correctly so even who never saw Mahabaratha or even
kid can understand clearly"): who is who first, then every cause-and-effect step as one plain label: the bow's name,
the secret vow as a card (the exact words that break it), Karna beating Yudhishthira, the wound, the forbidden words
said in anger, the trap (a scale: LIAR / SINNER), Krishna's way out (the respectful and the rude word, on cards, in the
viewer's own language), the second trap and the second way out, the forgiveness.

Respect: Yudhishthira, Arjuna and Krishna keep their dignity; the sword is only raised and stopped (its tip always well
short of anyone), nobody is hurt, no blood (Yudhishthira's wounds are white cloth bandages); Krishna is calm and wise.

Every frame is a pure function of t. English on-screen text (shared by Hindi and Kannada) except the two word cards of
a12/a13, which show the viewer's language: आप / तू (Hindi), ನೀವು / ನೀನು (Kannada), shaped by matplotlib's text engine
(PIL here has no complex-script shaping); without the Nirmala font they fall back to AAP / TU and NEEVU / NEENU. Cues
are words of the line in each language ({"hi": ..., "kn": ...}) with a fraction fallback, kept in one table (CUES)
that the scenes and sfx() both read, with minimum gaps so a fast voice can't bunch the beats together.

Shot list (line: what is on the screen)
  a1  HOOK, frame 0: Arjuna alone and large, sword raised, fierce; ARJUNA'S SWORD / ON HIS OWN / BROTHER (big word in by
      0.3 s, underlined on "bhai"); a glint runs up the blade on "talwar"; on "Krishna" Krishna's blue hand rises in
      from the right edge; a card KILL HIM... / WITHOUT KILLING? (second line red, on "bina maare")
  a2  THIS IS NOT A / FILM STORY (crossed out); a palm-leaf book rises and opens: MAHABHARATA, BOOK 8: KARNA PARVA
      (ringed), SECTIONS 68-71
  a3  the two brothers face to face: Yudhishthira (tag ELDEST) lit first: THE ELDEST PANDAVA: / YUDHISHTHIRA; then
      Arjuna (tag GREATEST ARCHER), his bow lifted: HIS YOUNGER BROTHER: / ARJUNA
  a4  the bow alone, glowing, rays turning: ARJUNA'S BOW: / GANDIVA (tag GANDIVA); it moves aside, a folded note drops
      in and a red wax seal stamps it: AND A / SECRET VOW
  a5  a torn note: ANYONE WHO SAYS: / "GIVE YOUR BOW AWAY" / (a red arrow) / LOSES HIS HEAD (red); Arjuna's dark
      silhouette behind, bow raised
  a6  Karna (big, sun halo, golden armour) draws his bow: THE KAURAVAS' GREATEST WARRIOR: / KARNA; small Yudhishthira
      with his bow; the arrow knocks the bow out of his hands, he reels: KARNA DEFEATED / YUDHISHTHIRA; Karna laughs
      (HA! HA!): KARNA / MOCKED HIM
  a7  dusk, the camp tent; Yudhishthira inside, slumped on a cot, bandaged (tag WOUNDED): YUDHISHTHIRA CAME BACK /
      WOUNDED; Arjuna and Krishna walk in: ARJUNA AND KRISHNA / CAME TO SEE HIM
  a8  inside the tent: Yudhishthira smiles; a thought bubble with Karna's head, crossed out: HE THOUGHT: / KARNA IS
      DEAD!; on "par" the cross fades, his smile goes: BUT KARNA WAS / STILL ALIVE (tag KARNA: STILL ALIVE)
  a9  Yudhishthira rises, angry, and points at the bow; a speech cloud FIE ON YOUR GANDIVA! / GIVE IT AWAY! (red), the
      bow ringed
  a10 the vow card flashes back for a beat (red flash); Arjuna draws his sword and points it at his brother, stopping
      far short: THE VOW CAME BACK..., then HE DREW HIS SWORD ON / HIS OWN BROTHER
  a11 Krishna steps in and holds Arjuna's wrist: KRISHNA / HELD HIS HAND; then the scale: BREAK THE VOW? / LIAR (the
      LIAR card drops into the left pan, it tips), KILL HIS BROTHER? / SINNER (the right pan), then level and wobbling
      with a big "?": ARJUNA: / WHAT DO I DO?
  a12 Krishna teaching; FOR AN ELDER, / RESPECT = LIFE; two word cards: the respectful word (आप / ನೀವು, RESPECTFUL
      "YOU") and, below a red arrow, the rude word in red (तू / ನೀನು, RUDE "YOU"), the first one struck through: CALL
      HIM THE / RUDE "YOU"; then = KILLED, / WITHOUT KILLING and a caption NO RESPECT = DEATH, WITHOUT DYING
  a13 the tent: Arjuna points and scolds (the rude word pops up in red by his mouth); dice tumble down behind him and
      land; a speech cloud YOU GAMBLED / OUR KINGDOM AWAY!: ARJUNA SCOLDED HIS BROTHER / RUDELY
  a14 a note with two ticks: VOW (tick) and BROTHER ALIVE (tick); the brothers below, the sword back in its sheath
  a15 RE-HOOK: the lamp dims; Arjuna, head bowed in shame: ARJUNA FELT / ASHAMED; he draws the sword again and its blade
      swings back upright, a dotted red U-turn arrow showing it turn toward himself (it stops far short, the blade
      never near him); Krishna's hand rises from the right: AND NOW, ON / HIMSELF?!
  a16 Krishna calm, glowing: KRISHNA FOUND / ANOTHER WAY; a card PRAISE YOURSELF / = / KILL YOURSELF; small Arjuna
      lowers his sword: SO KRISHNA SAID: / PRAISE YOURSELF!
  a17 Arjuna boasts, fist on his chest, chin up, sparkles: ARJUNA PRAISED / HIMSELF; then kneels at Yudhishthira's feet:
      THEN BOWED AT HIS / BROTHER'S FEET; Yudhishthira lifts him up, a warm light: YUDHISHTHIRA / FORGAVE HIM (FORGIVEN)
  a18 SO, KRISHNA'S TRICK WAS...: two cards CLEVER? / CHEATING THE VOW?, a red ring alternating; Krishna small and calm
      below; a big "?"
"""
import functools
import math
import os

import cairo
import numpy as np

import arjuna_cast as A
import jayadratha_cast as J
import puppet_cast as C
import puppet_core as pc
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, tick, to_surface
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_jarasandha import FADE, FEET, INK, RED, bob_rot, glow, man_angles, motes, red_ring, small_line, \
    sound_rings, big_word, walk_legs
from scenes_jayadratha import NIGHT, arrow_at, fit_size, flash_at, shroud, silhouette, tag, tint, title_lift, to_user
from scenes_kaikeyi import ANJALI, card, fig, settle
from scenes_lakshman_rekha import big_q, big_x, book, quote_note, sparkle
from scenes_mandhata import aura, burst, lights, mix, reach_arm, warm
from scenes_ravana import dotted, head2
from shots import T, shot_at

MISSES = set()                       # cue words not found in a line (falls back to fractions)
TF = FEET + 110                      # the floor inside the tent


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
    "a1": (("B", {"hi": "भाई", "kn": "ಅಣ್ಣನ"}, 0.3, (("t0", 0.6),)),
           ("S", {"hi": "तलवार", "kn": "ಕತ್ತಿ"}, 0.42, (("B", 0.3),)),
           ("K", {"hi": "कृष्ण", "kn": "ಕೃಷ್ಣ"}, 0.55, (("S", 0.6),)),
           ("M", {"hi": "मार", "kn": "ಕೊಲ್ಲು"}, 0.78, (("K", 0.6),)),
           ("W", {"hi": "बिना", "kn": "ಕೊಲ್ಲದೆ"}, 0.9, (("M", 0.5),))),
    "a2": (("X", {"hi": "नहीं", "kn": "ಅಲ್ಲ"}, 0.3, (("t0", 0.6),)),
           ("M", {"hi": "महाभारत", "kn": "ಮಹಾಭಾರತದ"}, 0.55, (("X", 0.5),)),
           ("P", {"hi": "कर्ण", "kn": "ಕರ್ಣ"}, 0.72, (("M", 0.5),))),
    "a3": (("Y", {"hi": "युधिष्ठिर", "kn": "ಯುಧಿಷ್ಠಿರ"}, 0.02, ()),
           ("E", {"hi": "बड़े", "kn": "ದೊಡ್ಡ"}, 0.25, (("t0", 0.6),)),
           ("A", {"hi": "अर्जुन", "kn": "ಅರ್ಜುನ"}, 0.5, (("E", 0.6),)),
           ("G", {"hi": "धनुर्धारी", "kn": "ಬಿಲ್ಲುಗಾರ"}, 0.85, (("A", 0.7),))),
    "a4": (("D", {"hi": "धनुष", "kn": "ಬಿಲ್ಲಿನ"}, 0.1, (("t0", 0.2),)),
           ("G", {"hi": "गांडीव", "kn": "ಗಾಂಡೀವ"}, 0.35, (("D", 0.5),)),
           ("Q", {"hi": "चुपचाप", "kn": "ಹೇಳದೆ"}, 0.65, (("G", 0.8),)),
           ("V", {"hi": "क़सम", "kn": "ಪ್ರತಿಜ್ಞೆ"}, 0.85, (("Q", 0.4),))),
    "a5": (("W", {"hi": "मुझसे", "kn": "ನನಗೆ"}, 0.1, (("t0", 0.2),)),
           ("G", {"hi": "गांडीव", "kn": "ಗಾಂಡೀವನ"}, 0.35, (("W", 0.5),)),
           ("H", {"hi": "सिर", "kn": "ತಲೆ"}, 0.8, (("G", 0.9),))),
    "a6": (("K", {"hi": "कर्ण", "kn": "ಕರ್ಣ"}, 0.2, (("t0", 0.6),)),
           ("D", {"hi": "हराया", "kn": "ಸೋಲಿಸಿ"}, 0.55, (("K", 1.2),)),
           ("M", {"hi": "मज़ाक", "kn": "ಅವಮಾನ"}, 0.8, (("D", 0.9),))),
    "a7": (("W", {"hi": "घायल", "kn": "ಗಾಯಗೊಂಡ"}, 0.03, ()),
           ("T", {"hi": "तंबू", "kn": "ಟೆಂಟ್"}, 0.3, (("t0", 0.6),)),
           ("A", {"hi": "अर्जुन", "kn": "ಅರ್ಜುನ"}, 0.5, (("T", 0.6),)),
           ("K", {"hi": "कृष्ण", "kn": "ಕೃಷ್ಣನ"}, 0.62, (("A", 0.3),))),
    "a8": (("L", {"hi": "लगा", "kn": "ಅನ್ನಿಸ್ತು"}, 0.15, (("t0", 0.4),)),
           ("M", {"hi": "मारकर", "kn": "ಕೊಂದು"}, 0.42, (("L", 0.6),)),
           ("B", {"hi": "पर", "kn": "ಆದ್ರೆ"}, 0.62, (("M", 0.8),)),
           ("Z", {"hi": "अभी", "kn": "ಬದುಕಿದ್ದ"}, 0.85, (("B", 0.5),))),
    "a9": (("A", {"hi": "युधिष्ठिर", "kn": "ಯುಧಿಷ್ಠಿರ"}, 0.15, ()),
           ("F", {"hi": "धिक्कार", "kn": "ಧಿಕ್ಕಾರ"}, 0.35, (("t0", 0.8),)),
           ("D", {"hi": "किसी", "kn": "ಕೊಟ್ಟುಬಿಡು"}, 0.75, (("F", 0.9),))),
    "a10": (("V", {"hi": "क़सम", "kn": "ಪ್ರತಿಜ್ಞೆ"}, 0.2, (("t0", 0.2),)),
            ("S", {"hi": "तलवार", "kn": "ಕತ್ತಿ"}, 0.5, (("V", 0.9), ("t0", 1.3))),
            ("B", {"hi": "भाई", "kn": "ಅಣ್ಣನನ್ನೇ"}, 0.8, (("S", 0.9),))),
    "a11": (("H", {"hi": "रोका", "kn": "ತಡೆದ"}, 0.15, (("t0", 0.3),)),
            ("L", {"hi": "झूठा", "kn": "ಸುಳ್ಳುಗಾರ"}, 0.45, (("H", 1.1),)),
            ("P", {"hi": "पापी", "kn": "ಪಾಪಿ"}, 0.7, (("L", 0.8),)),
            ("Q", {"hi": "क्या", "kn": "ಏನು"}, 0.9, (("P", 0.5),))),
    "a12": (("R", {"hi": "बड़ों", "kn": "ಮರ್ಯಾದೆನೇ"}, 0.15, (("t0", 0.3),)),
            ("L", {"hi": "जान", "kn": "ಜೀವ"}, 0.25, (("R", 0.3),)),
            ("A", {"hi": "आप", "kn": "ನೀವು"}, 0.45, (("L", 0.7),)),
            ("T", {"hi": "तू", "kn": "ನೀನು"}, 0.55, (("A", 0.6),)),
            ("W", {"hi": "बिना", "kn": "ಕೊಲ್ಲದೆ"}, 0.92, (("T", 1.0),))),
    "a13": (("D", {"hi": "वही", "kn": "ಹಾಗೇ"}, 0.1, (("t0", 0.2),)),
            ("T", {"hi": "तू", "kn": "ಏಕವಚನದಲ್ಲಿ"}, 0.3, (("D", 0.5),)),
            ("G", {"hi": "जुआ", "kn": "ಜೂಜಾಡಿದೆ"}, 0.6, (("T", 0.6),)),
            ("K", {"hi": "राज्य", "kn": "ರಾಜ್ಯ"}, 0.85, (("G", 0.6),))),
    "a14": (("V", {"hi": "पूरी", "kn": "ಉಳೀತು"}, 0.3, (("t0", 0.3),)),
            ("B", {"hi": "भाई", "kn": "ಅಣ್ಣನೂ"}, 0.55, (("V", 0.4),)),
            ("Z", {"hi": "रहे", "kn": "ಬದುಕಿದ್ರು"}, 0.85, (("B", 0.3),))),
    "a15": (("S", {"hi": "शर्म", "kn": "ನಾಚಿಕೆ"}, 0.2, (("t0", 0.4),)),
            ("D", {"hi": "तलवार", "kn": "ಕತ್ತಿ"}, 0.5, (("S", 0.8),)),
            ("N", {"hi": "बार", "kn": "ಸಲ"}, 0.7, (("D", 0.7),)),
            ("M", {"hi": "आप", "kn": "ತಾನೇ"}, 0.85, (("N", 0.4),))),
    "a16": (("K", {"hi": "कृष्ण", "kn": "ಕೃಷ್ಣ"}, 0.03, ()),
            ("P", {"hi": "अपनी", "kn": "ಹೊಗಳಿಕೊಳ್ಳೋದು"}, 0.3, (("t0", 0.8),)),
            ("E", {"hi": "जैसा", "kn": "ಹಾಗೇ"}, 0.65, (("P", 0.8),)),
            ("D", {"hi": "करो", "kn": "ಹೊಗಳಿಕೋ"}, 0.9, (("E", 0.6),))),
    "a17": (("B", {"hi": "बड़ाई", "kn": "ಹೊಗಳಿಕೊಂಡ"}, 0.2, (("t0", 0.3),)),
            ("F", {"hi": "पैरों", "kn": "ಕಾಲಿಗೆ"}, 0.5, (("B", 1.1),)),
            ("P", {"hi": "उसे", "kn": "ಕ್ಷಮಿಸಿದ್ರು"}, 0.85, (("F", 1.0),))),
    "a18": (("C", {"hi": "समझदारी", "kn": "ಬುದ್ಧಿವಂತಿಕೆನಾ"}, 0.3, (("t0", 0.5),)),
            ("X", {"hi": "धोखा", "kn": "ಮೋಸನಾ"}, 0.55, (("C", 0.5),)),
            ("M", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.8, (("X", 0.4),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_ar_cues", None)
    if cache is None:
        cache = {}
        tl._ar_cues = cache
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


# ------------------------------------------------------------------ the two words in the viewer's own script


INDIC_FONT = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts", "Nirmala.ttc")
HAS_INDIC = os.path.exists(INDIC_FONT)
WORDS = {"hi": ("आप", "तू"), "kn": ("ನೀವು", "ನೀನು")}             # the respectful and the rude "you"
WORDS_LATIN = {"hi": ("AAP", "TU"), "kn": ("NEEVU", "NEENU")}


@functools.lru_cache(maxsize=32)
def indic_surface(text, size, color):
    """Devanagari / Kannada text, shaped (matplotlib's text engine joins Kannada vowel signs, which PIL's basic
    layout here cannot), slightly emboldened, cropped to the ink: a cairo surface."""
    from matplotlib import font_manager, patheffects
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.figure import Figure
    from PIL import Image
    fig_ = Figure(figsize=(size * (len(text) + 2) * 1.1 / 72.0, size * 2.4 / 72.0), dpi=72)
    fig_.patch.set_alpha(0.0)
    canvas = FigureCanvasAgg(fig_)
    fp = font_manager.FontProperties(fname=INDIC_FONT, size=size)
    fig_.text(0.5, 0.5, text, fontproperties=fp, color=color, ha="center", va="center",
              path_effects=[patheffects.withStroke(linewidth=max(1.0, size * 0.045), foreground=color)])
    canvas.draw()
    a = np.asarray(canvas.buffer_rgba()).copy()
    ys, xs = np.nonzero(a[..., 3] > 8)
    a = a[max(0, ys.min() - 4):ys.max() + 5, max(0, xs.min() - 4):xs.max() + 5]
    return to_surface(Image.fromarray(np.ascontiguousarray(a), "RGBA"))


def word_text(cr, tl, k, x, y, size, color, alpha=1.0):
    """The respectful (k = 0) or rude (k = 1) word, centred on (x, y) in screen pixels."""
    if alpha <= 0.01:
        return
    if HAS_INDIC:
        s = indic_surface(WORDS[lang(tl)][k], int(size), tuple(color))
        cr.set_source_surface(s, x - s.get_width() / 2, y - s.get_height() / 2)
        cr.paint_with_alpha(alpha)
    else:
        draw_text(cr, WORDS_LATIN[lang(tl)][k], x, y, int(size * 0.9), color, alpha, anchor="cm")


def word_card(cr, t, tl, t_in, k, x, y, s, label, color, alpha=1.0, strike=None):
    """A leather plaque with one of the two words big on it and a small English label under it; strike = the time a
    red line strikes the word through."""
    q = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    yy = y + 60 * (1 - q)
    r = sway(t, 0.008, 0.4, x * 0.01)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(r)
    cr.scale(s, s)
    pc.paint_part(cr, "plaque", a)
    draw_text(cr, label, 0, 74, 34, INK, a, MONO_FONT, "cm", tracking=3)
    cr.restore()
    pc.rod(cr, x, yy + 110 * s, x + 30, H + 60, alpha=0.5 * a)
    word_text(cr, tl, k, x, yy - 22 * s, 150 * s, color, a)
    if strike is not None and t > strike:
        p = ease((t - strike) / 0.3)
        cr.save()
        cr.set_source_rgba(*RED, 0.92 * a)
        cr.set_line_width(16)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        half = 30 + 0.5 * (indic_surface(WORDS[lang(tl)][k], int(150 * s), tuple(color)).get_width()
                           if HAS_INDIC else 150 * s)
        x0, x1 = x - half, x + half
        cr.move_to(x0, yy - 24 * s)
        cr.line_to(x0 + (x1 - x0) * p, yy - 24 * s - 12 * p)
        cr.stroke()
        cr.restore()


# ------------------------------------------------------------------ small helpers


def paint(sprite, alpha=1.0, blur=0.0):
    return lambda cr_: pc.paint_part(cr_, sprite, alpha, blur)


def two(*fns):
    def fn(cr_):
        for f in fns:
            f(cr_)
    return fn


def down_arrow(cr, x, y0, y1, p, alpha=1.0, w=16):
    """A red arrow drawn downward from y0 to y1 (p = how much is drawn)."""
    if p <= 0:
        return
    ye = y0 + (y1 - y0) * p
    cr.save()
    cr.set_source_rgba(*RED, 0.95 * alpha)
    cr.set_line_width(w)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(x, y0)
    cr.line_to(x, ye - 20)
    cr.stroke()
    if p > 0.6:
        pc.poly(cr, [(x - 2.4 * w, ye - 30), (x + 2.4 * w, ye - 30), (x, ye + 16)])
        cr.fill()
    cr.restore()


def card2(cr, t, t_in, x, y, s, lines, alpha=1.0):
    """scenes_kaikeyi.card (a leather plaque dropping in on its rod) whose lines appear one by one, each on its own
    word: lines = [(text, size, colour, dy, t_show)] in plaque units."""
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
    for txt, sz, col, dy, ts in lines:
        p = prog(t, ts, 0.25) * a
        if p > 0:
            k = 1.15 - 0.15 * back(clamp((t - ts) / 0.3))
            cr.save()
            cr.translate(0, dy)
            cr.scale(k, k)
            draw_text(cr, txt, 0, 0, sz, col, p, anchor="cm")
            cr.restore()
    cr.restore()
    pc.rod(cr, x, yy + 110 * s, x + 30, H + 60, alpha=0.5 * a)


def cloud_text(cr, t, x, y, s, lines, flip=False, alpha=1.0, t_in=None):
    """lrekha_cast's speech cloud (tail lower left; flip = lower right) popping in at t_in, lines = [(text, size,
    colour, dy, t_show)] in screen pixels from its centre."""
    q = back(clamp((t - t_in) / 0.3), 1.6) if t_in is not None else 1.0
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    sc = s * (0.6 + 0.4 * q)
    prop(cr, "lr_scloud", x, y, sc, rot=sway(t, 0.008, 0.5), alpha=a, flip=flip)
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


# ------------------------------------------------------------------ puppets


SW_S = 0.66                          # the sword's scale in Arjuna's hand (arm units)


def sword_cb(store, arm, ss, tilt, alpha, blur):
    """extra= callback: the sword in a hand whose (upper, fore) angles are `arm` (upright + tilt); records the tip."""
    rot = -(arm[0] + arm[1]) + tilt

    def fn(cr_):
        cr_.save()
        cr_.translate(4, 150)
        cr_.rotate(rot)
        cr_.scale(ss, ss)
        pc.paint_part(cr_, "ar_sword", alpha, blur)
        store["tip"] = cr_.user_to_device(36, -560)
        store["mid"] = cr_.user_to_device(10, -300)
        cr_.restore()
    return fn


def gbow_cb(store, arm, bs, tilt, sprite, alpha, blur, key="grip"):
    """extra= callback: a bow held upright (+ tilt) in a hand; records its grip (device)."""
    rot = -(arm[0] + arm[1]) + tilt

    def fn(cr_):
        cr_.save()
        cr_.translate(4, 150)
        cr_.rotate(rot)
        cr_.scale(bs, bs)
        pc.paint_part(cr_, sprite, alpha, blur)
        store[key] = cr_.user_to_device(0, 0)
        cr_.restore()
    return fn


def arjuna(cr, t, x, s, mood=None, bow=True, sword=False, tilt=0.0, front=(-0.32, -0.55), backa=(0.3, -0.25),
           head=0.0, legs=(0.0, 0.0), hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, feet=FEET,
           ph=1.0, kneel=False, y=None, scabbard=True):
    """Arjuna (jayadratha_cast), facing right: the bow Gandiva in his back hand (bow=True), the sword in his front hand
    (sword=True, upright + tilt) or in its scabbard at his hip; mood swaps his face (angry | scold | shame | proud);
    kneel = on one knee. Returns his points (device) plus 'tip' (the sword's tip) and 'bow' (the bow's grip)."""
    store = {}
    extra = {}
    if bow == "front":                                  # the bow held up in his front hand (shown, pointed at)
        extra["jd_arjuna_armF_lo"] = gbow_cb(store, front, 0.78, 0.0, "jd_gandiva", alpha, blur, "bow")
    elif bow:
        extra["jd_arjuna_armB_lo"] = gbow_cb(store, backa, 0.72, 0.0, "jd_gandiva", alpha, blur, "bow")
    if sword:
        extra["jd_arjuna_armF_lo"] = sword_cb(store, front, SW_S, tilt, alpha, blur)
    if scabbard and not kneel:
        extra["jd_arjuna_body"] = paint("ar_scabbard" if sword else "ar_scabbard_full", alpha, blur)
    swap = {"jd_arjuna_head": f"ar_arjuna_head_{mood}"} if mood else None
    pts = fig(cr, J.ARJUNA, "jd_arjuna", t, x, s, front=front, backa=backa, head=head, legs=legs, hits=hits, flip=flip,
              alpha=alpha, blur=blur, rods=rods, rot=rot, feet=feet, ph=ph, extra=extra, swap=swap,
              kneel="ar_arjuna_kneel" if kneel else None, y=y)
    pts.update(store)
    return pts


def krishna(cr, t, x, s, **kw):
    return fig(cr, C.KRISHNA, "krishna", t, x, s, **kw)


def krishna_arm(cr, t, x, sh_y, s, front, alpha=1.0, flip=True):
    """Only Krishna's front arm, its shoulder at (x -+ 26 s, sh_y): his hand reaching in from a screen edge."""
    if alpha <= 0.01:
        return {}
    ang = man_angles("krishna", t, front, (0.3, -0.25), 0.0, (0.0, 0.0), (), 0.4)
    return puppet(cr, C.KRISHNA, x, sh_y + 262 * s, s, 0.0, flip, ang, alpha, 0.0,
                  only={"krishna_armF_up", "krishna_armF_lo"}, rods=True)


YU_B = 1.08


def yudh(cr, t, x, s, mood="calm", seat=0.0, hurt=False, bow=False, flip=True, front=(-0.32, -0.55),
         backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0), hits=(), feet=TF, alpha=1.0, blur=0.0, rods=True, rot=0.0,
         lean=0.0, ph=0.7, y=None):
    """Yudhishthira (facing left by default). seat 1 = seated (the seated legs, hip at feet - SEAT_H s; draw the cot
    yourself), 0 = standing, in between a quick rod-puppet rise; hurt = the white bandages; bow = his own bow in his
    front hand; lean > 0 slumps him forward. Returns his points (device) plus 'bow' (the bow's grip)."""
    q = clamp(seat)
    hy_sit = feet - A.SEAT_H * s
    hy_st = feet - 434 * s
    hy = (hy_st + (hy_sit - hy_st) * ease(q)) if y is None else y
    store = {}
    extra = {}
    if hurt:
        extra["ar_yudh_body"] = paint("ar_band_chest", alpha, blur)
        extra["ar_yudh_armB_up"] = paint("ar_band_arm", alpha, blur)
    if bow:
        extra["ar_yudh_armF_lo"] = gbow_cb(store, front, 0.8, 0.0, "ar_ybow", alpha, blur, "bow")
    swap = {"ar_yudh_head": "ar_yudh_head" + ("" if mood == "calm" else "_" + mood)}
    sg = -1 if flip else 1
    r = rot + bob_rot(t, ph) + sg * lean
    hide = ()
    if q >= 0.5:
        prop(cr, "ar_yudh_seat", x, hy, s, r, alpha, blur, flip)
        hide = ("ar_yudh_legF", "ar_yudh_legB")
    ang = man_angles("ar_yudh", t, front, backa, head, legs, hits, ph)
    pts = puppet(cr, A.YUDH, x, hy, s, r, flip, ang, alpha, blur, hide=hide, swap=swap, rods=rods, extra=extra)
    pts.update(store)
    return pts


KA_B = 1.18


def karna(cr, t, x, s, mood="calm", aim=None, draw=0.0, arrow=True, flip=True, front=(-0.32, -0.55),
          backa=(0.3, -0.25), head=0.0, feet=FEET, hits=(), alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.2):
    """Karna (facing left by default) with his great bow: carried in his back hand (aim=None), or held out along the
    screen angle `aim` (measured as if he faced right) with the string drawn back by `draw` 0..1 and an arrow nocked.
    Returns his points (device) plus 'nock' / 'grip' (user) when aiming."""
    hy = feet - 434 * s
    store = {}
    sg = -1 if flip else 1
    if aim is not None:
        front = (aim - math.pi / 2, 0.0)
        dx, dy = math.cos(aim), math.sin(aim)
        sx, sy = x + sg * 26 * KA_B * s, hy - 262 * s
        k = (300 - 70 - 170 * draw) * s
        backa = reach_arm(x, hy, s, -14 * KA_B, (sx + sg * k * dx, sy + k * dy), flip)
        rot_b = -(front[0] + front[1]) + aim
        sprite = "ar_kbow_bare" if draw > 0.02 else "ar_kbow"

        def bow_fn(cr_):
            cr_.save()
            cr_.translate(4, 150)
            cr_.rotate(rot_b)
            cr_.scale(0.8, 0.8)
            pc.paint_part(cr_, sprite, alpha, blur)
            store["tips"] = (cr_.user_to_device(-98, -378), cr_.user_to_device(-98, 378))
            store["grip"] = cr_.user_to_device(0, 0)
            cr_.restore()
        extra = {"ar_karna_armF_lo": bow_fn}
    else:
        extra = {"ar_karna_armB_lo": gbow_cb(store, backa, 0.72, 0.0, "ar_kbow", alpha, blur)}
    swap = {"ar_karna_head": "ar_karna_head_laugh"} if mood == "laugh" else None
    ang = man_angles("ar_karna", t, front, backa, head, (0.0, 0.0), hits, ph)
    pts = puppet(cr, A.KARNA, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, swap=swap, rods=rods,
                 extra=extra)
    if aim is not None and "tips" in store:
        g = to_user(cr, store["grip"])
        hb = to_user(cr, pts["handB"])
        pts["grip"], pts["nock"] = g, hb
        if draw > 0.02:
            ta, tb = to_user(cr, store["tips"][0]), to_user(cr, store["tips"][1])
            cr.save()
            cr.set_source_rgba(*pc.INK, 0.9 * alpha)
            cr.set_line_width(max(1.6, 2.6 * s))
            cr.move_to(*ta)
            cr.line_to(*hb)
            cr.line_to(*tb)
            cr.stroke()
            cr.restore()
            if arrow:
                ang_ = math.atan2(g[1] - hb[1], g[0] - hb[0])
                arrow_at(cr, hb[0], hb[1], ang_, math.dist(g, hb) + 80 * s, alpha, blur)
    return pts


def ha(cr, t, t_in, x, y, size=70, alpha=1.0):
    """Karna's laugh: HA! HA! letters popping up and drifting."""
    for i in range(4):
        ti = t_in + 0.32 * i
        if t < ti:
            continue
        u = t - ti
        q = back(clamp(u / 0.25), 2.0)
        a = clamp(q) * alpha * (1 - clamp((u - 1.4) / 0.5))
        if a <= 0.01:
            continue
        xx = x + (-60 if i % 2 else 50) - 20 * u
        yy = y - 70 * i - 50 * u
        cr.save()
        cr.translate(xx, yy)
        cr.rotate(-0.25 if i % 2 else 0.18)
        cr.scale(q, q)
        draw_text(cr, "HA!", 0, 0, size, (0.55, 0.12, 0.05), a, anchor="cm")
        cr.restore()


# ------------------------------------------------------------------ the camp


def tent_inside(cr, t, lamp=True, alpha=1.0):
    """Inside the tent: the striped back wall (soft, behind the puppets), the floor, a standing oil lamp."""
    prop(cr, "ar_wall", 540, TF + 10, 0.92, alpha=0.72 * alpha, blur=5.0)
    if lamp:
        lx, ly = 560, TF - 420 * 0.62
        glow(cr, lx, ly - 30, 300, (0.55 + 0.1 * math.sin(t * 7.3)) * alpha)
        prop(cr, "ar_diya", lx, TF + 4, 0.62, alpha=alpha, blur=2.0)
        f = int(t * 10) % 3
        prop(cr, f"flame{f}", lx + 40 * 0.62, ly + 6, 0.16 * (0.95 + 0.08 * math.sin(t * 9)), alpha=alpha)
    prop(cr, "ground", W / 2, TF + 6, 0.82, alpha=alpha)


def cot(cr, x, s, feet=TF, alpha=1.0, blur=0.0, flip=True):
    """The camp cot under a seated Yudhishthira at x (his thighs reach forward, so the cot sits under them)."""
    prop(cr, "ar_cot", x + (-1 if flip else 1) * 70 * s, feet, s, alpha=alpha, blur=blur)


# ------------------------------------------------------------------ the notes and cards


def vow_note(cr, t, t_in, x, y, s, tW, tG, tH, alpha=1.0):
    """The vow, on a torn note: ANYONE WHO SAYS: / "GIVE YOUR BOW AWAY" / a red arrow / LOSES HIS HEAD."""
    p = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(p) * alpha
    if a <= 0.01:
        return
    yy = y + 70 * (1 - p)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(-0.02 + sway(t, 0.006, 0.4))
    cr.scale(s, s)
    pc.paint_part(cr, "rv_note", a)
    draw_text(cr, "ANYONE WHO SAYS:", 0, -176, 46, INK, a * prog(t, tW, 0.3), MONO_FONT, "cm", tracking=4)
    q = prog(t, tG, 0.3) * a
    if q > 0:
        txt = '"GIVE YOUR BOW AWAY"'
        draw_text(cr, txt, 0, -86 + 12 * (1 - q), fit_size(txt, 104, 690), INK, q, HEAD_FONT, "cm")
    qa = ease((t - tH + 0.45) / 0.4) if t > tH - 0.45 else 0.0
    if qa > 0:
        down_arrow(cr, 0, -14, 70, qa, a, 15)
    q3 = prog(t, tH, 0.3) * a
    if q3 > 0:
        draw_text(cr, "LOSES HIS HEAD", 0, 158 + 12 * (1 - q3), fit_size("LOSES HIS HEAD", 128, 690), RED, q3,
                  HEAD_FONT, "cm")
    cr.restore()


def secret_note(cr, t, t_in, x, y, s, t_seal, alpha=1.0):
    """A folded note SECRET VOW and a red wax seal stamped on it at t_seal."""
    p = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(p) * alpha
    if a <= 0.01:
        return
    yy = y + 80 * (1 - p)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(0.03 + sway(t, 0.006, 0.4, 1.0))
    cr.scale(s, s)
    pc.paint_part(cr, "rv_note", a)
    draw_text(cr, "ARJUNA'S", 0, -150, 52, INK, a, MONO_FONT, "cm", tracking=6)
    draw_text(cr, "SECRET VOW", 0, -50, 150, RED, a, HEAD_FONT, "cm")
    cr.restore()
    if t > t_seal - 0.25:
        q = clamp((t - t_seal + 0.25) / 0.25)
        k = 1.8 - 0.8 * back(q, 2.0)
        prop(cr, "ar_seal", x + 10, yy + 120 * s, 0.75 * s * k, rot=-0.2 + 0.2 * q, alpha=clamp(q * 2) * a)


# ------------------------------------------------------------------ the scale (LIAR / SINNER)


def plank(cr, text, x, y, s, size, color, alpha=1.0):
    """A leather plaque with one word, centred on (x, y) in the current coordinates."""
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    pc.paint_part(cr, "plaque", alpha)
    draw_text(cr, text, 0, 0, fit_size(text, size, 640), color, alpha, anchor="cm")
    cr.restore()


def scale2(cr, t, x, foot, s, tilt, left_t, right_t, alpha=1.0, blur=0.0):
    """kaikeyi_cast's leather balance with a LIAR card dropping into the left pan at left_t and a SINNER card into
    the right one at right_t. tilt > 0: the left pan is down. Returns the pans' hooks [(x, y, swing)]."""
    vel = 0.0
    sw = 0.018 * math.sin(t * 1.9) + vel
    prop(cr, "kk_post", x, foot, s, alpha=alpha, blur=blur)
    px, py = x, foot - K_POST_H * s
    out = []
    for side in (-1, 1):
        ex = px + side * K_BEAM_L * s * math.cos(tilt)
        ey = py - side * K_BEAM_L * s * math.sin(tilt)
        out.append((ex, ey, sw))
    prop(cr, "kk_beam", px, py, s, rot=-tilt, alpha=alpha, blur=blur)
    for (ex, ey, swp), side, (txt, tt) in zip(out, (-1, 1), (("LIAR", left_t), ("SINNER", right_t))):
        cr.save()
        cr.translate(ex, ey)
        cr.rotate(swp)
        cr.scale(s, s)
        q = clamp((t - tt + 0.45) / 0.45) if tt is not None else 0.0
        if q > 0:
            plank(cr, txt, 0, K_DROP - 50 - 620 * (1 - q) ** 2, 0.42, 190, RED, alpha * clamp(q * 3))
        pc.paint_part(cr, "kk_pan", alpha, blur)
        cr.restore()
    return out


K_POST_H, K_BEAM_L, K_DROP = 720.0, 330.0, 300.0      # kaikeyi_cast.POST_H, BEAM_L, PAN_DROP


# ------------------------------------------------------------------ a1  hook


HOOK = (410, 0.98, 1890)             # Arjuna in the hook: x, scale, feet
HOOK_UP = (-2.55, -0.35)             # his sword arm, raised
KR_HAND = (-2.0, -0.45)              # Krishna's hand reaching in from the right edge, calm, palm up


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "a1")
    tB, tS, tK, tM, tW = c["B"], c["S"], c["K"], c["M"], c["W"]
    x, s, feet = HOOK
    glow(cr, x + 80, feet - 700 * s, 560, 0.4)
    warm(cr, x + 220, 900, 260, 0.3 * prog(t, tS, 0.3))
    fr = keyed(t, [(-1.0, HOOK_UP), (tS - 0.05, (-2.7, -0.2))], 0.25, 1.6)
    pts = arjuna(cr, t, x, s, mood="angry", sword=True, tilt=0.3, front=fr, backa=(0.3, -0.25), feet=feet,
                 head=-0.04, hits=[(tS, 0.5)], ph=1.0, bow=False)
    if t > tS - 0.05 and "tip" in pts:                  # a glint runs up the blade
        tip, mid = to_user(cr, pts["tip"]), to_user(cr, pts["mid"])
        u = clamp((t - tS + 0.05) / 0.35)
        gx, gy = mid[0] + (tip[0] - mid[0]) * u, mid[1] + (tip[1] - mid[1]) * u
        sparkle(cr, gx, gy, 46 * math.sin(math.pi * u) + 4, 0.9 * (1 - clamp((t - tS - 0.6) / 0.4)))
    kin = ease((t - tK) / 0.45) if t > tK else 0.0       # Krishna's hand rises in from the right edge
    if kin > 0:
        glow(cr, 880, 1120, 320, 0.4 * kin)
        krishna_arm(cr, t, 1130 + 260 * (1 - kin), 1210 + 200 * (1 - kin), 1.1,
                    keyed(t, [(tK, (-1.5, -0.2)), (tK + 0.3, KR_HAND)], 0.3, 1.4), alpha=clamp(kin * 2))

    def ui(cr):
        small_line(cr, t, [(wd, -1.0) for wd in "ARJUNA'S SWORD".split()], 190, 64)
        small_line(cr, t, [(wd, -1.0) for wd in "ON HIS OWN".split()], 268, 64)
        big_word(cr, t, "BROTHER", 0.3, 350, min(250, fit_size("BROTHER", 250, 800)), RED, ghost_from=-1.0,
                 under=tB)
        if t > tM - 0.3:
            card2(cr, t, tM - 0.3, 795, 1480, 0.6, [("KILL HIM...", fit_size("KILL HIM...", 96, 560), INK, -50, tM),
                                                   ("WITHOUT KILLING?", fit_size("WITHOUT KILLING?", 104, 560), RED,
                                                    48, tW)])
    return dict(ui=ui, flash=flash_at(t, tS, 0.25) + flash_at(t, tW, 0.25))


# ------------------------------------------------------------------ a2  it's in the Mahabharata


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "a2")
    tX, tM, tP = c["X"], c["M"], c["P"]
    leaves = [(None, [("MAHABHARATA", 92, HEAD_FONT)], 0),
              (tP + 0.1, [([("BOOK 8:", INK), ("KARNA PARVA", RED)], 76, HEAD_FONT)], 0),
              (tP + 0.5, [("SECTIONS 68-71", 44, MONO_FONT)], 0)]
    book(cr, t, 540, 940, 0.86, leaves, t_in=t0 + 0.05, t_open=tM, ring=(1, 0, 1, tP + 0.45))

    def ui(cr):
        if t < tM:
            struck = t > tX + 0.25
            box = head2(cr, t, "THIS IS NOT A", t0 + 0.05, "FILM STORY", t0 + 0.35, big_size=210,
                        big_color=FADE if struck else INK)
            if box and t > tX:
                bx, by, bw, bh = box
                big_x(cr, W / 2, by + bh / 2, bw + 60, bh * 0.95, prog(t, tX, 0.3), lw=24)
        else:
            head2(cr, t, "IT'S WRITTEN IN THE", tM - 0.2, "MAHABHARATA", tM + 0.06, big_size=200, under=tP + 0.3)
    return dict(ui=ui, flash=flash_at(t, tM, 0.25) + flash_at(t, tP, 0.2))


# ------------------------------------------------------------------ a3  the two brothers


BRO = dict(ax=290, yx=800, s=0.8, feet=FEET + 150)


def s_brothers(cr, t, tl, t0, t1):
    c = cues(tl, "a3")
    tY, tE, tA, tG = c["Y"], c["E"], c["A"], c["G"]
    ax, yx, s, feet = BRO["ax"], BRO["yx"], BRO["s"], BRO["feet"]
    ly, la = prog(t, tY, 0.3), prog(t, tA, 0.3)
    glow(cr, yx, feet - 700 * s, 430, 0.55 * ly * (1 - 0.5 * la))
    glow(cr, ax, feet - 700 * s, 430, 0.55 * la)
    prop(cr, "ground", W / 2, feet + 6, 0.82)
    b, k, a = depth(t, t0 - 0.2, 0.45)
    yp = yudh(cr, t, yx, s * k, feet=feet, front=(-0.6, -0.9), backa=(0.25, -0.3), hits=[(tY, 0.5)], alpha=a, blur=b)
    lift = keyed(t, [(t0, 0.0), (tG - 0.05, 1.0)], 0.3, 1.4)
    b2, k2, a2 = depth(t, tA - 0.35, 0.45)
    ap = arjuna(cr, t, ax, s * k2, backa=(0.3 - 0.9 * lift, -0.25 - 0.4 * lift), feet=feet, hits=[(tA, 0.6)],
                alpha=a2, blur=b2)

    def ui(cr):
        if t < tA:
            head2(cr, t, "THE ELDEST PANDAVA:", t0 + 0.05, "YUDHISHTHIRA", tY + 0.1, big_size=200)
        else:
            head2(cr, t, "HIS YOUNGER BROTHER:", tA - 0.2, "ARJUNA", tA + 0.06, big_size=240, under=tG + 0.2)
        yt, at = yp["top"], ap["top"]
        ty_ = min(yt[1] - 170, at[1] - 130)
        tag(cr, t, tE, "ELDEST", yt[0] - 10, ty_, 40)
        tag(cr, t, tG, "GREATEST ARCHER", max(220, at[0]), ty_, 34)
        if t > tA + 0.3:                                 # a dotted arc between them: brothers
            p0, p1 = (ap["chest"][0] + 70, ap["chest"][1] + 20), (yp["chest"][0] - 70, yp["chest"][1] + 20)
            pts_ = [(p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u - 70 * math.sin(math.pi * u))
                    for u in (i / 30 for i in range(31))]
            dotted(cr, pts_, prog(t, tA + 0.3, 0.5), 24, 5.5, RED, 0.75)
            q = prog(t, tA + 0.7, 0.3)
            if q > 0:
                draw_text(cr, "BROTHERS", (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 - 110, 34, INK, q, MONO_FONT,
                          "cm", tracking=4)
    return dict(ui=ui, flash=flash_at(t, tY, 0.15) + flash_at(t, tA, 0.2))


# ------------------------------------------------------------------ a4  the bow Gandiva; a secret vow


def s_gandiva(cr, t, tl, t0, t1):
    c = cues(tl, "a4")
    tD, tG, tQ, tV = c["D"], c["G"], c["Q"], c["V"]
    aside = ease((t - tQ + 0.1) / 0.6) if t > tQ - 0.1 else 0.0
    bx, by = 540 - 290 * aside, 1180 + 60 * aside
    bs = 1.25 - 0.45 * aside
    lit = prog(t, tG, 0.4)
    glow(cr, bx, by, 520 * bs, (0.35 + 0.45 * lit) * (0.9 + 0.1 * math.sin(t * 4)))
    warm(cr, bx, by, 420 * bs, 0.35 + 0.5 * lit)
    aura(cr, t, bx, by, 120 * bs, 520 * bs, 0.25 + 0.6 * lit, n=22, spin=0.1)
    b, k, a = depth(t, t0 - 0.15, 0.5)
    prop(cr, "jd_gandiva", bx, by + 30 * math.sin(t * 1.3), bs * k, rot=0.06 * math.sin(t * 0.9), alpha=a, blur=b)
    lights(cr, t, bx, by, 300 * bs, 10, 0.6 * lit * (1 - 0.5 * aside))
    pc.rod(cr, bx + 20, by + 330 * bs, bx + 70, H + 60, alpha=0.5 * a)
    dev = cr.user_to_device(bx + 200 * bs, by)

    def ui(cr):
        if t < tQ:
            head2(cr, t, "ARJUNA'S BOW:", t0 + 0.05, "GANDIVA", tG, big_size=250, under=tG + 0.4)
            tag(cr, t, tG + 0.2, "GANDIVA", min(dev[0] + 90, 920), dev[1] - 60, 40, t_out=tQ)
        else:
            head2(cr, t, "AND ARJUNA HAD A", tQ - 0.2, "SECRET VOW", tV, big_size=230)
            secret_note(cr, t, tQ, 690, 960, 0.72, tV)
    return dict(ui=ui, flash=flash_at(t, tG, 0.25) + flash_at(t, tV, 0.35))


# ------------------------------------------------------------------ a5  the vow card


def s_vow(cr, t, tl, t0, t1):
    c = cues(tl, "a5")
    tW, tG, tH = c["W"], c["G"], c["H"]
    glow(cr, 540, 1250, 520, 0.3 + 0.3 * prog(t, tH, 0.4))
    warm(cr, 540, 1400, 480, 0.25 * prog(t, tH, 0.5), (1.0, 0.35, 0.15))
    silhouette(cr, lambda cr_: _sil_arjuna(cr_, t), 0.62 * prog(t, t0, 0.4))

    def ui(cr):
        small_line(cr, t, [(wd, t0 + 0.05 + 0.08 * k) for k, wd in enumerate("ARJUNA'S SECRET VOW:".split())],
                   245, 64)
        vow_note(cr, t, t0 + 0.15, 540, 740, 0.92, tW, tG, tH)
    return dict(ui=ui, flash=flash_at(t, tH, 0.4))


def _sil_arjuna(cr_, t):
    """Arjuna swearing (fist on his chest, the bow in his other hand), one dark shadow under the note."""
    return arjuna(cr_, t, 540, 0.95, mood="angry", front=(-0.25, -2.35), backa=(0.3, -0.25), feet=2010, rods=False,
                  ph=1.0)


# ------------------------------------------------------------------ a6  Karna beats and mocks Yudhishthira


KA6 = (800, 0.9, FEET + 150)         # Karna: x, scale, feet
YU6 = (230, 0.5, FEET + 110)         # Yudhishthira, small


def s_karna(cr, t, tl, t0, t1):
    c = cues(tl, "a6")
    tK, tD, tM = c["K"], c["D"], c["M"]
    kx, ks, kf = KA6
    yx, ys, yf = YU6
    glow(cr, kx - 40, kf - 760 * ks, 560, 0.45)
    prop(cr, "ground", W / 2, FEET + 156, 0.82)
    t_hit = tD + 0.28
    hit = t > t_hit

    def yu6(tt, alpha, blur, bow, k=1.0):
        """Yudhishthira at time tt: holding his bow up; struck, he reels back, arms up."""
        reel = keyed(tt, [(t0, 0.0), (t_hit, 1.0)], 0.25, 1.8)
        return yudh(cr, tt, yx - 30 * reel, ys * k, flip=False, bow=bow, front=mix((-1.25, -0.4), (-2.3, -0.6), reel),
                    backa=mix((0.3, -0.25), (-1.0, -1.2), reel), head=-0.12 * reel, rot=-0.12 * reel, feet=yf,
                    hits=[(t_hit, 1.0)], alpha=alpha, blur=blur, mood="hurt" if tt > t_hit else "calm", ph=0.9,
                    rods=alpha > 0.01)
    gx0, gy0 = to_user(cr, yu6(t_hit, 0.0, 0.0, True)["bow"])     # where the bow is when the arrow strikes it
    b, k, a = depth(t, t0 + 0.2, 0.45)
    yp = yu6(t, a, b, not hit, k)
    if hit:                                             # the knocked bow: up, spinning, and down behind him
        dt = t - t_hit
        land = 0.78
        if dt < land:
            bx, by = gx0 - 200 * dt, gy0 - 700 * dt + 1400 * dt * dt
            rot = -7.5 * dt
        else:
            bx, by = gx0 - 200 * land, yf - 26
            rot = -math.pi / 2 - 0.06 * math.exp(-6 * (dt - land)) * math.sin(30 * (dt - land))
        prop(cr, "ar_ybow", bx, by, 0.8 * ys, rot=rot)
    # Karna draws and shoots; then laughs
    aimq = keyed(t, [(t0, 0.0), (tK + 0.2, 1.0)], 0.35, 1.3)
    released = t >= tD
    draw = 0.0 if released else clamp((t - tK - 0.3) / max(0.4, tD - tK - 0.4))
    laugh = t > tM
    shake = 0.03 * math.sin(t * 19) * (1 if laugh else 0) * (0.5 + 0.5 * math.exp(-1.5 * max(0.0, t - tM)))
    if aimq > 0.5:
        kp = karna(cr, t, kx, ks, mood="laugh" if laugh else "calm", aim=0.34, draw=ease(draw),
                   arrow=not released, feet=kf, rot=shake, head=-0.1 if laugh else 0.0, hits=[(tD, 0.6)])
    else:
        kp = karna(cr, t, kx, ks, feet=kf, front=(-0.5, -0.6), hits=[(tK, 0.5)])
    if released and t < t_hit and "nock" in kp:         # the arrow, to his bow
        nk = kp["nock"]
        u = (t - tD) / (t_hit - tD)
        ang = math.atan2(gy0 - nk[1], gx0 - nk[0])
        arrow_at(cr, nk[0] + (gx0 - nk[0]) * u - 150 * math.cos(ang) * u, nk[1] + (gy0 - nk[1]) * u
                 - 150 * math.sin(ang) * u, ang, 150)
    if hit:
        burst(cr, t, gx0, gy0, t_hit, n=14, rmax=260, alpha=0.8)
    dev_y = yp["top"]
    dev_k = kp["head"]

    def ui(cr):
        if t < tD:
            head2(cr, t, "THE KAURAVAS' GREATEST WARRIOR:", t0 + 0.05, "KARNA", tK, big_size=260)
        elif t < tM:
            head2(cr, t, "KARNA DEFEATED", tD - 0.2, "YUDHISHTHIRA", tD + 0.06, big_size=200)
        else:
            head2(cr, t, "KARNA", tM - 0.25, "MOCKED HIM", tM, big_size=240, under=tM + 0.4)
        tag(cr, t, tK + 0.15, "KARNA", min(dev_k[0] + 40, 960), dev_k[1] - 330, 38)
        tag(cr, t, t0 + 0.6, "YUDHISHTHIRA", max(190, dev_y[0]), dev_y[1] - 80, 30)
        if laugh:
            ha(cr, t, tM + 0.05, dev_k[0] - 330, dev_k[1] - 130, 72)
            sound_rings(cr, dev_k[0] - 80, dev_k[1] + 40, t, tM, 4, 0.35, 260, alpha=0.4)
    return dict(ui=ui, flash=flash_at(t, t_hit, 0.35) + flash_at(t, tM, 0.15))


# ------------------------------------------------------------------ a7  the tent at dusk


TENT = (580, FEET + 150, 0.74)


def s_tent(cr, t, tl, t0, t1):
    c = cues(tl, "a7")
    tW, tT, tA, tK = c["W"], c["T"], c["A"], c["K"]
    tx, tf, ts = TENT
    prop(cr, "ground", W / 2, tf + 6, 0.82)
    prop(cr, "ar_tent", tx, tf, ts)
    yx, ys = tx + 170, 0.62
    glow(cr, yx, tf - 330, 300, 0.5 + 0.08 * math.sin(t * 7))
    cot(cr, yx, ys, tf - 2)
    yp = yudh(cr, t, yx, ys, mood="hurt", seat=1.0, hurt=True, feet=tf - 2, lean=0.14, head=0.18,
              front=(-0.45, -1.6), backa=(0.1, -0.2), rods=False)
    prop(cr, "ar_tent_front", tx, tf, ts)
    t_walk1 = max(tA + 1.3, tK + 0.9)
    walk_a = hop_walk(t, tA - 0.1, t_walk1, -180, 330)
    walk_k = hop_walk(t, tK - 0.1, t_walk1 + 0.2, -260, 150)
    b, k, a = depth(t, tK - 0.1, 0.45)
    krishna(cr, t, walk_k[0], 0.6 * k, feet=tf + 10 + walk_k[1], legs=walk_legs(walk_k[3]), rot=walk_k[2], alpha=a,
            blur=b, ph=0.4, front=(-0.4, -0.5))
    b, k, a = depth(t, tA - 0.1, 0.45)
    arjuna(cr, t, walk_a[0], 0.62 * k, feet=tf + 14 + walk_a[1], legs=walk_legs(walk_a[3]), rot=walk_a[2], alpha=a,
           blur=b)
    dev_y = yp["top"]

    def ui(cr):
        if t < tA:
            head2(cr, t, "YUDHISHTHIRA CAME BACK", t0 + 0.05, "WOUNDED", tW + 0.25, big_size=250)
            tag(cr, t, tT, "HIS TENT", tx, 800, 34, t_out=tA)
        else:
            head2(cr, t, "ARJUNA AND KRISHNA", tA - 0.2, "CAME TO SEE HIM", tK, big_size=190)
        tag(cr, t, tW + 0.5, "WOUNDED", min(dev_y[0] + 20, 900), dev_y[1] - 150, 34)
    return dict(ui=ui, eve=0.34, night=0.12, flash=flash_at(t, tW, 0.15))


# ------------------------------------------------------------------ a8  he thinks Karna is dead; Karna lives


YX, YS = 830, 0.68                   # Yudhishthira in the tent
AX, AS = 285, 0.7                    # Arjuna
KX, KS = 95, 0.64                    # Krishna, a step behind


def s_alive(cr, t, tl, t0, t1):
    c = cues(tl, "a8")
    tL, tM, tB, tZ = c["L"], c["M"], c["B"], c["Z"]
    tent_inside(cr, t)
    krishna(cr, t, KX, KS, feet=TF, blur=3.0, alpha=0.9, front=(-0.4, -0.5), ph=0.4, rods=False)
    arjuna(cr, t, AX, AS, feet=TF, head=0.02, ph=1.0)
    cot(cr, YX, YS)
    smile = tL - 0.1 < t < tB + 0.2
    yp = yudh(cr, t, YX, YS, mood="smile" if smile else "hurt", seat=1.0, hurt=True, lean=0.05 if smile else 0.12,
              head=-0.05 if smile else 0.12, front=(-0.6, -1.3) if smile else (-0.45, -1.6), backa=(0.1, -0.2),
              hits=[(tL, 0.4), (tB, 0.5)])
    dev_y = yp["top"]

    def ui(cr):
        bub = prog(t, tL - 0.1, 0.35)
        bx, by = 520, 830
        if bub > 0:
            q = back(clamp((t - tL + 0.1) / 0.35), 1.6)
            prop(cr, "ar_think", bx, by, 0.62 * (0.6 + 0.4 * q), rot=sway(t, 0.006, 0.4), alpha=clamp(q))
            prop(cr, "ar_karna_head", bx + 20, by + 110, 0.62 * clamp(q), rot=0.0, alpha=clamp(q))
            xq = prog(t, tM + 0.1, 0.35) * (1 - prog(t, tB, 0.5))
            if xq > 0:
                big_x(cr, bx + 10, by - 20, 300, 260, 1.0 if t > tM + 0.45 else prog(t, tM + 0.1, 0.35),
                      alpha=xq, lw=26)
        if t < tB:
            head2(cr, t, "YUDHISHTHIRA THOUGHT:", t0 + 0.05, "KARNA IS DEAD!", tM, big_size=200)
        else:
            head2(cr, t, "BUT KARNA WAS", tB - 0.2, "STILL ALIVE", tZ, big_size=240, under=tZ + 0.4)
            tag(cr, t, tZ + 0.2, "KARNA: STILL ALIVE", bx - 20, by + 245, 36)
        if smile and t > tL + 0.2:
            sparkle(cr, dev_y[0] - 60, dev_y[1] + 150, 22 + 6 * math.sin(t * 6), 0.6)
    return dict(ui=ui, eve=0.22, flash=flash_at(t, tM, 0.2) + flash_at(t, tZ, 0.25))


# ------------------------------------------------------------------ a9  "fie on your Gandiva! give it away!"


def s_angry(cr, t, tl, t0, t1):
    c = cues(tl, "a9")
    tA, tF, tD = c["A"], c["F"], c["D"]
    tent_inside(cr, t)
    krishna(cr, t, KX, KS, feet=TF, blur=3.0, alpha=0.9, front=(-0.4, -0.5), ph=0.4, rods=False)
    rise = clamp((t - t0 - 0.35) / 0.45)
    ap = arjuna(cr, t, AX, AS, feet=TF, head=0.03 + 0.05 * prog(t, tD, 0.3), hits=[(tD, 0.4)], ph=1.0,
                bow="front", front=(-0.75, -0.85), backa=(0.25, -0.3))
    bow_u = to_user(cr, ap["bow"]) if "bow" in ap else (AX - 40, TF - 600)
    cot(cr, YX, YS, alpha=1.0)
    sit = 1.0 - ease(rise)
    hy = TF - 434 * YS
    pt = point_at_flip(YX, hy, YS, (bow_u[0], bow_u[1] - 40))
    fr = keyed(t, [(t0, (-0.45, -1.6)), (tF - 0.1, pt)], 0.3, 1.5)
    yudh(cr, t, YX, YS, mood="angry", seat=sit, hurt=True, front=fr, backa=(0.35, -0.6), head=-0.04,
         hits=[(tF, 0.6), (tD, 0.6)], rot=0.03 * math.sin(t * 13) * prog(t, tD, 0.2) * math.exp(-2 * max(0, t - tD)))
    dev_bow = cr.user_to_device(*bow_u)
    if t > tF:
        glow(cr, bow_u[0], bow_u[1], 260, 0.4 * prog(t, tF, 0.3))

    def ui(cr):
        head2(cr, t, "IN ANGER, YUDHISHTHIRA SAID:", t0 + 0.05, None, 0.0)
        cloud_text(cr, t, 520, 820, 0.8, [("FIE ON YOUR GANDIVA!", 54, INK, -58, tF),
                                          ("GIVE IT AWAY!", 112, RED, 34, tD)], flip=True, t_in=tF - 0.25)
        if t > tF:
            tag(cr, t, tF + 0.2, "GANDIVA", dev_bow[0] + 40, dev_bow[1] - 260, 30)
        if t > tD + 0.3:
            red_ring(cr, dev_bow[0] + 10, dev_bow[1], 95, 230, prog(t, tD + 0.3, 0.45), 9)
    return dict(ui=ui, eve=0.22, flash=flash_at(t, tF, 0.2) + flash_at(t, tD, 0.3))


def point_at_flip(x, hy, s, target, bulk=YU_B):
    """front=(upper, fore) for a straight front arm pointing at target, for a puppet facing LEFT."""
    sx, sy = x - 26 * bulk * s, hy - 262 * s
    a = math.atan2(target[1] - sy, -(target[0] - sx))
    return (a - math.pi / 2, 0.0)


# ------------------------------------------------------------------ a10  the vow comes back; the sword is drawn


A10_POINT = (-1.75, 0.05)            # Arjuna's sword arm, out toward his brother
A10_TILT = 1.25                      # the blade forward and a little up
HILT = (-0.55, -1.75)                # his hand at the hilt on his hip


def s_draw(cr, t, tl, t0, t1):
    c = cues(tl, "a10")
    tV, tS, tB = c["V"], c["S"], c["B"]
    tent_inside(cr, t)
    cot(cr, YX + 60, YS, alpha=0.9, blur=2.0)
    krishna(cr, t, KX, KS, feet=TF, blur=3.0, alpha=0.9, front=(-0.4, -0.5), head=0.05, ph=0.4, rods=False)
    drawn = t > tS
    reach = keyed(t, [(t0, 0.0), (tS - 0.4, 1.0), (tS, 2.0)], 0.3, 1.3)
    if reach <= 1:
        fr = mix((-0.25, -0.9), HILT, reach)            # the hand goes to the hilt at his hip
        tilt = 3.0
    else:
        u = min(1.0, reach - 1) + max(0.0, reach - 2) * 0.3
        fr = mix(HILT, A10_POINT, u)                    # out of the sheath, round and out toward his brother
        tilt = 2.6 + (A10_TILT - 2.6) * u
    ap = arjuna(cr, t, AX - 30, AS, mood="angry", sword=drawn, tilt=tilt, front=fr, backa=(0.15, -0.35), feet=TF,
                hits=[(tS, 0.4)], ph=1.0)
    back_ = keyed(t, [(t0, 0.0), (tS + 0.3, 1.0)], 0.3, 1.3)
    yudh(cr, t, YX + 40 + 20 * back_, YS, mood="hurt", seat=0.0, hurt=True, front=mix((-0.6, -0.9), (-0.2, -0.3),
                                                                                      back_),
         backa=(0.3, -0.4), head=0.06 - 0.1 * back_, rot=0.05 * back_, hits=[(tS + 0.3, 0.5)])
    tip = ap.get("tip")
    if drawn and tip is not None and t > tS + 0.2:
        tu = to_user(cr, tip)
        sparkle(cr, tu[0], tu[1], 30, 0.7 * (1 - prog(t, tS + 0.9, 0.4)))

    def ui(cr):
        vq = prog(t, t0 + 0.05, 0.25) * (1 - prog(t, tS - 0.25, 0.3))
        if vq > 0.01:                                   # the vow card flashes back
            cr.save()
            cr.set_source_rgba(0.35, 0.02, 0.0, 0.35 * vq)
            cr.paint()
            cr.restore()
            vow_note(cr, t, t0 - 1.0, 540, 740, 0.86, t0 - 1, t0 - 1, t0 - 0.5, alpha=vq)
        if t < tS:
            head2(cr, t, "ARJUNA REMEMBERED HIS VOW:", t0 + 0.05, None, 0.0)
        elif t < tB:
            head2(cr, t, "AND HE DREW", tS - 0.2, "HIS SWORD", tS, big_size=250)
        else:
            head2(cr, t, "HE DREW HIS SWORD ON", tB - 0.2, "HIS OWN BROTHER", tB + 0.06, big_size=200,
                  under=tB + 0.4)
    return dict(ui=ui, eve=0.2, flash=flash_at(t, t0 + 0.05, 0.5) + flash_at(t, tS, 0.35))


# ------------------------------------------------------------------ a11  Krishna holds his hand; LIAR or SINNER


A11_A = (290, 0.74, TF + 40)         # Arjuna (x, scale, feet), close
A11_K = (575, 0.74)                  # Krishna


def s_trap(cr, t, tl, t0, t1):
    c = cues(tl, "a11")
    tH, tL, tP, tQ = c["H"], c["L"], c["P"], c["Q"]
    tX = tL - 0.35                                      # the scale comes in
    part_b = t > tX
    if not part_b:
        ax, as_, af = A11_A
        tent_inside(cr, t, alpha=0.85)
        fr = (-2.35, -0.3)
        ap = arjuna(cr, t, ax, as_, mood="angry", sword=True, tilt=-0.3, front=fr, backa=(0.15, -0.35), feet=af,
                    hits=[(tH, 0.3)], ph=1.0, rot=-0.02)
        hand = to_user(cr, ap["handF"])
        kx, ks = A11_K
        khy = af - 434 * ks
        step = ease((t - t0 - 0.05) / 0.4)
        kxx = kx + 200 * (1 - step)
        grip = keyed(t, [(t0, 0.0), (tH - 0.15, 1.0)], 0.25, 1.3)
        target = (hand[0] + 6, hand[1] + 8)
        kfr = mix((-0.4, -0.5), reach_arm(kxx, khy, ks, 26, target, True), grip)
        glow(cr, kxx, khy - 300 * ks, 360, 0.4)
        krishna(cr, t, kxx, ks, flip=True, feet=af, front=kfr, backa=(0.3, -0.3), head=0.04, ph=0.4,
                hits=[(tH, 0.3)], alpha=clamp(step * 2))
        dev_h = cr.user_to_device(*target)
    else:
        b, k, a = depth(t, tX, 0.5)
        glow(cr, 540, 1150, 520, 0.35)

        def sh(cr_):                                    # Arjuna behind the scale, torn, his hands at his head
            return arjuna(cr_, t, 470, 1.05, feet=FEET + 330, front=(-2.75, -1.75), backa=(-2.6, -1.95), head=0.18,
                          rods=False, bow=False, scabbard=False)
        silhouette(cr, sh, 0.32 * prog(t, tX, 0.5))
        tilt = settle(t, [(t0, 0.0), (tL, 0.2), (tP, -0.2), (tQ, 0.0)])
        out = scale2(cr, t, 540, FEET + 110, 0.98 * k, tilt, tL, tP, alpha=a, blur=b)
        dev_l, dev_r = cr.user_to_device(out[0][0], out[0][1]), cr.user_to_device(out[1][0], out[1][1])

    def ui(cr):
        if not part_b:
            head2(cr, t, "KRISHNA", t0 + 0.05, "HELD HIS HAND", tH, big_size=220)
            if t > tH:
                red_ring(cr, dev_h[0], dev_h[1], 95, 80, prog(t, tH + 0.1, 0.4), 8)
        else:
            if t < tP:
                head2(cr, t, "BREAK THE VOW?", tX - 0.15, "LIAR", tL, big_size=260)
            elif t < tQ:
                head2(cr, t, "KILL HIS BROTHER?", tP - 0.2, "SINNER", tP, big_size=260)
            else:
                head2(cr, t, "ARJUNA:", tQ - 0.2, "WHAT DO I DO?", tQ, big_size=210)
            tag(cr, t, tL - 0.25, "BREAK THE VOW", dev_l[0], dev_l[1] - 110, 30)
            tag(cr, t, tP - 0.25, "KILL HIS BROTHER", dev_r[0], dev_r[1] - 110, 30)
            if t > tQ:
                big_q(cr, t, tQ + 0.1, 540, 730, 160)
    return dict(ui=ui, eve=0.15 if not part_b else 0.0, flash=flash_at(t, tH, 0.2) + flash_at(t, tL, 0.25) +
                flash_at(t, tP, 0.25))


# ------------------------------------------------------------------ a12  the respectful word and the rude word


TEACH = (-2.25, -0.55)               # Krishna's teaching hand, raised


def s_words(cr, t, tl, t0, t1):
    c = cues(tl, "a12")
    tR, tL, tA, tT, tW = c["R"], c["L"], c["A"], c["T"], c["W"]
    x, s, feet = 175, 0.86, FEET + 160
    glow(cr, x + 40, feet - 760 * s, 520, 0.45)
    aura(cr, t, x + 30, feet - 434 * s - 410 * s, 130, 400, 0.35, n=18, spin=0.05)
    prop(cr, "ground", W / 2, feet + 6, 0.82)
    hy = feet - 434 * s
    at1 = point_at(x, hy, s, (500, 830), 1.0)
    at2 = point_at(x, hy, s, (500, 1150), 1.0)
    fr = keyed(t, [(t0, (-0.4, -0.5)), (tR - 0.2, TEACH), (tA - 0.1, at1), (tT, at2), (tW, TEACH)], 0.3, 1.4)
    krishna(cr, t, x, s, feet=feet, front=fr, backa=(0.3, -0.3), head=-0.03, hits=[(tA, 0.3), (tT, 0.3)], ph=0.4)

    def ui(cr):
        if t < tA:
            head2(cr, t, "FOR AN ELDER,", t0 + 0.05, "RESPECT = LIFE", tL, big_size=210, under=tL + 0.4)
        elif t < tW:
            head2(cr, t, "INSTEAD OF RESPECT,", tA - 0.2, 'THE RUDE "YOU"', tT, big_size=180)
        else:
            head2(cr, t, "THAT KILLS HIM...", tW - 0.2, "WITHOUT KILLING", tW, big_size=180, under=tW + 0.4)
        word_card(cr, t, tl, tA - 0.2, 0, 680, 830, 0.74, 'RESPECTFUL "YOU"', INK, strike=tT + 0.15)
        if t > tT - 0.4:
            down_arrow(cr, 680, 945, 1035, ease((t - tT + 0.4) / 0.35))
        word_card(cr, t, tl, tT - 0.15, 1, 680, 1150, 0.74, 'RUDE "YOU"', RED)
        if t > tT + 0.1:
            red_ring(cr, 680, 1128, 300, 115, prog(t, tT + 0.2, 0.45), 9)
        tag(cr, t, tW + 0.3, "NO RESPECT = DEATH, WITHOUT DYING", 640, 1370, 27)
    return dict(ui=ui, flash=flash_at(t, tT, 0.3) + flash_at(t, tW, 0.2))


# ------------------------------------------------------------------ a13  "you gambled our kingdom away!"


DICE = ((150, 6, 0.0, -0.6), (330, 5, 0.18, 0.5), (470, 3, 0.34, -0.3))   # (x, face, delay, spin)


def dice(cr, t, t_in, ground_y, alpha=1.0, blur=0.0):
    """Three dice tumbling down from above and bouncing to rest."""
    for x, n, dl, sp in DICE:
        ti = t_in + dl
        if t < ti:
            continue
        u = t - ti
        fall = 0.55
        if u < fall:
            y = -150 + (ground_y + 150) * (u / fall) ** 2
            rot = sp * 9 * u
        else:
            d = u - fall
            y = ground_y - 140 * abs(math.sin(7 * d)) * math.exp(-4.5 * d)
            rot = sp * 9 * fall + sp * 2.0 * (1 - math.exp(-4 * d))
        prop(cr, f"ar_die{n}", x, y, 0.55, rot=rot, alpha=alpha, blur=blur)


def s_scold(cr, t, tl, t0, t1):
    c = cues(tl, "a13")
    tD, tT, tG, tK = c["D"], c["T"], c["G"], c["K"]
    tent_inside(cr, t)
    cot(cr, YX + 60, YS, alpha=0.9, blur=2.0)
    dice(cr, t, tG - 0.15, TF - 120, alpha=0.95, blur=2.0)
    krishna(cr, t, KX - 20, KS, feet=TF, blur=3.0, alpha=0.9, front=(-0.4, -0.5), ph=0.4, rods=False)
    hy = TF - 434 * AS
    pt = point_at(AX, hy, AS, (YX - 60, TF - 520 * YS))
    fr = keyed(t, [(t0, (-0.32, -0.55)), (tD + 0.1, pt)], 0.3, 1.5)
    ap = arjuna(cr, t, AX, AS, mood="scold" if t > tT - 0.1 else "angry", front=fr, backa=(0.15, -0.35), feet=TF,
                hits=[(tT, 0.5), (tG, 0.5), (tK, 0.5)], ph=1.0)
    yudh(cr, t, YX + 20, YS, mood="hurt", seat=0.0, hurt=True, front=(-0.6, -0.8), backa=(0.35, -0.5),
         head=0.16 * prog(t, tT, 0.4), lean=0.06 * prog(t, tG, 0.4), hits=[(tT, 0.4), (tK, 0.4)])
    dev_m = ap["head"]

    def ui(cr):
        head2(cr, t, "ARJUNA SCOLDED HIS BROTHER", t0 + 0.05, "RUDELY", tT, big_size=240)
        cloud_text(cr, t, 560, 860, 0.8, [("YOU GAMBLED", 92, INK, -46, tG),
                                          ("OUR KINGDOM AWAY!", 76, RED, 44, tK)], t_in=tG - 0.25)
        if tT - 0.1 < t:                                # the rude word pops by his mouth
            q = back(clamp((t - tT + 0.1) / 0.3), 1.8)
            a = clamp(q) * (1 - prog(t, tG - 0.3, 0.3))
            if a > 0.01:
                cx, cy = dev_m[0] + 215, dev_m[1] - 70
                prop(cr, "plaque", cx, cy, 0.3 * q, rot=-0.06, alpha=a)
                word_text(cr, tl, 1, cx, cy - 4, 64 * q, RED, a)
    return dict(ui=ui, eve=0.22, flash=flash_at(t, tT, 0.25) + flash_at(t, tG, 0.2))


def point_at(x, hy, s, target, bulk=1.05):
    """front=(upper, fore) for a straight front arm pointing from the shoulder at target (facing right)."""
    sx, sy = x + 26 * bulk * s, hy - 262 * s
    a = math.atan2(target[1] - sy, target[0] - sx)
    return (a - math.pi / 2, 0.0)


# ------------------------------------------------------------------ a14  vow kept, brother alive


def s_ticks(cr, t, tl, t0, t1):
    c = cues(tl, "a14")
    tV, tB, tZ = c["V"], c["B"], c["Z"]
    glow(cr, 540, 1500, 520, 0.4)
    prop(cr, "ground", W / 2, TF + 6, 0.82)
    arjuna(cr, t, 330, 0.5, feet=TF, ph=1.0, head=0.05)
    yudh(cr, t, 760, 0.48, mood="calm", hurt=True, feet=TF, front=(-0.6, -0.9), hits=[(tZ, 0.5)])
    if t > tZ:
        lights(cr, t, 760, TF - 380, 140, 8, 0.7 * prog(t, tZ, 0.4))

    def ui(cr):
        head2(cr, t, "KRISHNA'S TRICK", t0 + 0.05, "WORKED", tZ + 0.1, big_size=230)
        p = back(clamp((t - t0 - 0.1) / 0.35), 1.4)
        a = clamp(p)
        if a > 0.01:
            yy = 890 + 70 * (1 - p)
            cr.save()
            cr.translate(540, yy)
            cr.rotate(-0.015 + sway(t, 0.006, 0.4))
            cr.scale(0.95, 0.95)
            pc.paint_part(cr, "rv_note", a)
            for i, (txt, tt) in enumerate((("VOW", tV), ("BROTHER ALIVE", tZ))):
                ry = -80 + 175 * i
                q = prog(t, tt - 0.35, 0.25) * a
                cr.set_source_rgba(*INK, 0.85 * a)
                cr.set_line_width(6)
                cr.rectangle(-330, ry - 46, 92, 92)
                cr.stroke()
                draw_text(cr, txt, -200, ry, fit_size(txt, 120, 500), INK, max(q, 0.0), HEAD_FONT, "lm")
                tick(cr, -320, ry - 4, 96, prog(t, tt, 0.35), RED, a)
            cr.restore()
    return dict(ui=ui, flash=flash_at(t, tV, 0.2) + flash_at(t, tZ, 0.3))


# ------------------------------------------------------------------ a15  re-hook: now himself?!


A15 = (340, 0.86, FEET + 150)


def s_shame(cr, t, tl, t0, t1):
    c = cues(tl, "a15")
    tS, tD, tN, tM = c["S"], c["D"], c["N"], c["M"]
    x, s, feet = A15
    dark = prog(t, t0, 0.8)
    shroud(cr, x + 60, feet - 700 * s, 2400, 0.3 * dark)
    glow(cr, x + 40, feet - 760 * s, 420, 0.45)
    drawn = t > tD
    reach = keyed(t, [(t0, 0.0), (tD - 0.4, 1.0), (tD, 2.0), (tN, 3.0)], 0.3, 1.3)
    if reach <= 1:
        fr, tilt = mix((-0.32, -0.55), HILT, reach), 3.0
    elif reach <= 2:                                    # drawn, held out in front of him, the blade outward
        u = min(1.0, reach - 1)
        fr, tilt = mix(HILT, (-1.85, -0.15), u), 2.6 - 1.25 * u
    else:                                               # the blade turns back upright, leaning toward him; the hand
        u = reach - 2                                   # stays far out, so the blade is never near him
        fr, tilt = mix((-1.85, -0.15), (-2.05, -0.1), u), 1.35 - 1.6 * u
    pts = arjuna(cr, t, x, s, mood="shame", sword=drawn, tilt=tilt, front=fr, backa=(0.2, -0.3), feet=feet,
                 head=0.22 - 0.1 * prog(t, tN, 0.4), hits=[(tD, 0.3), (tN, 0.4)], ph=1.0, bow=False)
    kin = ease((t - tM + 0.1) / 0.45) if t > tM - 0.1 else 0.0
    if kin > 0:
        glow(cr, 880, 1120, 320, 0.45 * kin)
        krishna_arm(cr, t, 1130 + 260 * (1 - kin), 1230 + 200 * (1 - kin), 1.1,
                    keyed(t, [(tM, (-1.5, -0.2)), (tM + 0.3, KR_HAND)], 0.3, 1.4), alpha=clamp(kin * 2))
    tip = pts.get("tip")
    chest = pts["chest"]

    def ui(cr):
        if t < tN:
            head2(cr, t, "ARJUNA FELT", t0 + 0.05, "ASHAMED", tS, big_size=250)
        else:
            head2(cr, t, "AND NOW, ON", tN - 0.2, "HIMSELF?!", tN, big_size=260, under=tM)
        if tip is not None and t > tN + 0.1:            # the turn: a dotted U-turn from the blade back toward him,
            a = 1 - prog(t, tM + 0.6, 0.4)              # stopping well short; gone once Krishna's hand is up
            if a > 0.01:
                p0 = (tip[0] + 18, tip[1] - 6)
                p3 = (chest[0] + 170, chest[1] + 10)
                c1, c2 = (p0[0] + 220, p0[1] - 60), (p3[0] + 260, p3[1] - 30)
                path = [tuple((1 - u) ** 3 * p0[k] + 3 * (1 - u) ** 2 * u * c1[k] + 3 * (1 - u) * u * u * c2[k]
                              + u ** 3 * p3[k] for k in (0, 1)) for u in (i / 40 for i in range(41))]
                p = prog(t, tN + 0.1, 0.4)
                dotted(cr, path, p, 26, 6.5, RED, 0.9 * a)
                if p >= 1:
                    ang = math.atan2(p3[1] - c2[1], p3[0] - c2[0])
                    cr.save()
                    cr.translate(*p3)
                    cr.rotate(ang)
                    cr.set_source_rgba(*RED, 0.9 * a)
                    pc.poly(cr, [(16, 0), (-22, -19), (-22, 19)])
                    cr.fill()
                    cr.restore()
    return dict(ui=ui, night=0.32 * dark, lift=1.0, flash=flash_at(t, tD, 0.25) + flash_at(t, tN, 0.3))


# ------------------------------------------------------------------ a16  praise yourself = kill yourself


def s_praise(cr, t, tl, t0, t1):
    c = cues(tl, "a16")
    tK, tP, tE, tD = c["K"], c["P"], c["E"], c["D"]
    x, s, feet = 220, 0.8, FEET + 120
    glow(cr, x + 30, feet - 760 * s, 520, 0.5)
    aura(cr, t, x + 30, feet - 434 * s - 410 * s, 130, 420, 0.45, n=20, spin=0.05)
    warm(cr, x + 30, feet - 850 * s, 320, 0.4)
    prop(cr, "ground", W / 2, FEET + 96, 0.82)
    fr = keyed(t, [(t0, (-0.4, -0.5)), (tK + 0.1, TEACH), (tD - 0.1, (-1.7, -0.3))], 0.3, 1.4)
    krishna(cr, t, x, s, feet=feet, front=fr, backa=(0.3, -0.3), head=-0.03, hits=[(tP, 0.3)], ph=0.4)
    low = keyed(t, [(t0, 0.0), (tD + 0.2, 1.0)], 0.4, 1.2)
    b, k, a = depth(t, tE - 0.1, 0.45)
    if t > tE - 0.1:
        arjuna(cr, t, 880, 0.5 * k, mood="shame", sword=True, flip=True, front=mix((-2.4, -0.3), (-0.2, -0.1), low),
               tilt=1.0 + 1.9 * low, backa=(0.2, -0.3), feet=FEET + 90, head=0.2 - 0.2 * low, alpha=a, blur=b)

    def ui(cr):
        if t < tD:
            head2(cr, t, "KRISHNA FOUND", t0 + 0.05, "ANOTHER WAY", tK + 0.3, big_size=230)
        else:
            head2(cr, t, "SO KRISHNA SAID:", tD - 0.2, "PRAISE YOURSELF!", tD, big_size=190, under=tD + 0.4)
        if t > tP - 0.3:
            quote_note(cr, t, tP - 0.3, 690, 890, 0.7,
                       [("PRAISE YOURSELF", 118, INK, HEAD_FONT, -128, tP),
                        ("=", 120, INK, HEAD_FONT, 4, tE - 0.2),
                        ("KILL YOURSELF", 128, RED, HEAD_FONT, 132, tE)])
    return dict(ui=ui, flash=flash_at(t, tP, 0.2) + flash_at(t, tE, 0.25))


# ------------------------------------------------------------------ a17  he boasts, bows, is forgiven


A17 = dict(ax=280, kx=560, yx=840, s=0.66, feet=FEET + 90)
PROUD = dict(front=(-0.25, -2.35), backa=(0.75, -1.6))          # fist on the chest, the other hand on the hip


def s_forgive(cr, t, tl, t0, t1):
    c = cues(tl, "a17")
    tB, tF, tP = c["B"], c["F"], c["P"]
    ax0, kx, yx, s, feet = A17["ax"], A17["kx"], A17["yx"], A17["s"], A17["feet"]
    glow(cr, yx - 150, feet - 650 * s, 520, 0.35 + 0.35 * prog(t, tP, 0.5))
    prop(cr, "ground", W / 2, feet + 6, 0.82)
    t_go, t_kneel = tF - 0.55, tF + 0.05
    t_up = tP + 0.45
    wx, bob, rock, wph = hop_walk(t, t_go, t_kneel, ax0, kx)
    kneeling = t_kneel <= t < t_up
    yfr = keyed(t, [(t0, (-0.6, -0.9)), (tP - 0.1, (-1.15, -0.25)), (t_up + 0.1, (-1.9, -0.6))], 0.3, 1.3)
    yp = yudh(cr, t, yx, s, mood="smile" if t > tP else "calm", feet=feet, front=yfr, backa=(0.3, -0.4),
              head=0.18 if t_kneel < t < t_up + 0.3 else 0.0, hits=[(tP, 0.4)], ph=0.7)
    if t < t_go:                                         # the boast
        pr = prog(t, tB - 0.2, 0.3)
        arjuna(cr, t, ax0, s, mood="proud", front=mix((-0.32, -0.55), PROUD["front"], pr),
               backa=mix((0.3, -0.25), PROUD["backa"], pr), head=-0.1 * pr, rot=-0.06 * pr, feet=feet,
               hits=[(tB, 0.6)], ph=1.0, bow=False)
        if pr > 0:
            lights(cr, t, ax0 + 30, feet - 640 * s, 220, 10, 0.8 * pr, speed=0.7)
    elif kneeling:
        arjuna(cr, t, kx + 20, s, kneel=True, front=ANJALI["front"], backa=ANJALI["backa"], head=0.3, feet=feet,
               ph=1.0, bow=False, rot=0.05)
    elif t < t_kneel:
        arjuna(cr, t, wx, s, feet=feet + bob, legs=walk_legs(wph), rot=rock, ph=1.0, bow=False)
    else:                                               # lifted up, face to face
        arjuna(cr, t, kx - 10, s, front=ANJALI["front"], backa=ANJALI["backa"], head=0.05, feet=feet, ph=1.0,
               bow=False, hits=[(t_up, 0.6)])
        lights(cr, t, (kx + yx) / 2 - 40, feet - 560 * s, 220, 10, 0.8 * prog(t, t_up, 0.5), speed=0.5)
    dev_y = yp["top"]

    def ui(cr):
        if t < tF - 0.2:
            head2(cr, t, "ARJUNA PRAISED", t0 + 0.05, "HIMSELF", tB, big_size=250)
        elif t < tP:
            head2(cr, t, "THEN BOWED AT HIS", tF - 0.4, "BROTHER'S FEET", tF, big_size=200)
        else:
            head2(cr, t, "YUDHISHTHIRA LIFTED HIM UP:", tP - 0.2, "FORGIVEN", tP + 0.1, big_size=260,
                  under=tP + 0.6)
        if tB < t < tF - 0.2:                           # his boasts pop up one by one
            for i, (txt, x_, y_, r_) in enumerate((("GREATEST ARCHER!", 420, 740, -0.05),
                                                   ("NO ONE IS MY EQUAL!", 560, 830, 0.04),
                                                   ("I CONQUERED ALL LANDS!", 470, 920, -0.03))):
                ti = tB + 0.2 + 0.45 * i
                q = back(clamp((t - ti) / 0.25), 1.8)
                if q > 0:
                    cr.save()
                    cr.translate(x_, y_)
                    cr.rotate(r_)
                    cr.scale(q, q)
                    draw_text(cr, txt, 0, 0, 52, INK, clamp(q), HEAD_FONT, "cm")
                    cr.restore()
    return dict(ui=ui, flash=flash_at(t, tF, 0.2) + flash_at(t, tP, 0.3))


# ------------------------------------------------------------------ a18  clever, or cheating the vow?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "a18")
    tC, tX, tM = c["C"], c["X"], c["M"]
    prop(cr, "ground", W / 2, FEET + 96, 0.82)
    glow(cr, 540, 1380, 420, 0.4)
    krishna(cr, t, 520, 0.72, feet=FEET + 90, front=(-0.55, -1.75), backa=(0.25, -0.3), ph=0.5)
    cards = ((300, [("CLEVER?", 150, RED, 4)], tC), (780, [("CHEATING", 94, RED, -48), ("THE VOW?", 94, RED, 50)],
                                                         tX))

    def ui(cr):
        head2(cr, t, "SO, KRISHNA'S TRICK WAS...", t0 + 0.05, None, 0.0)
        cs = 0.58
        for cx, lines, tc in cards:
            card(cr, t, tc - 0.25, cx, 620, cs, [(txt, min(sz, fit_size(txt, sz, 660)), col, dy)
                                                 for txt, sz, col, dy in lines])
        if t > tC:
            if t < tX:
                k, ts = 0, tC
            else:
                n = int((t - tX) / 0.9)
                k, ts = (1 if n % 2 == 0 else 0), tX + 0.9 * n
            red_ring(cr, cards[k][0], 624, 232, 96, prog(t, ts, 0.35), 9)
        big_q(cr, t, tM, 860, 1110, 220)
    return dict(ui=ui, flash=flash_at(t, tX, 0.2))


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("a1", None, s_hook, {"z": (1.0, 1.04)}),
    ("a2", None, s_book, {"z": (1.0, 1.03)}),
    ("a3", None, s_brothers, {"z": (1.0, 1.03)}),
    ("a4", None, s_gandiva, {"z": (1.0, 1.04)}),
    ("a5", None, s_vow, {"z": (1.0, 1.03)}),
    ("a6", None, s_karna, {"z": (1.0, 1.03)}),
    ("a7", None, s_tent, {"z": (1.0, 1.04)}),
    ("a8", None, s_alive, {"z": (1.0, 1.03)}),
    ("a9", None, s_angry, {"z": (1.0, 1.04)}),
    ("a10", None, s_draw, {"z": (1.02, 1.07)}),
    ("a11", None, s_trap, {"z": (1.0, 1.03)}),
    ("a12", None, s_words, {"z": (1.0, 1.02)}),
    ("a13", None, s_scold, {"z": (1.0, 1.03)}),
    ("a14", None, s_ticks, {"z": (1.0, 1.03)}),
    ("a15", None, s_shame, {"z": (1.02, 1.07)}),
    ("a16", None, s_praise, {"z": (1.0, 1.03)}),
    ("a17", None, s_forgive, {"z": (1.0, 1.03)}),
    ("a18", None, s_end, {"z": (1.0, 1.03)}),
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
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a conch
    on the secret vow, a single hit as the sword is drawn on the brother, shimmer on VOW / BROTHER ALIVE, a bell on the
    forgiveness, then (only where they fit) a damaru on the re-hook and a bell on the closing question. Chosen in THAT
    order of importance, each at least SFX_MIN_GAP from every sound already kept (as render_myth.calm_sfx keeps them),
    so the list returned is what plays; the bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["a4"]["V"], "conch", 0), (c["a10"]["S"], "hit", 0), (c["a14"]["Z"], "shimmer", 0),
            (c["a17"]["P"], "bell", 0), (c["a15"]["N"], "damaru", 0), (c["a18"]["C"], "bell", 0),
            (c["a12"]["T"], "damaru", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["a10"]["S"] - 0.35, "dip", 0.5), (c["a15"]["N"] - 0.3, "dip", 0.5), (c["a12"]["T"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
