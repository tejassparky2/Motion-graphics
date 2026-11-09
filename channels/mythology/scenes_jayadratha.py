"""Scenes for videos/jayadratha.py: "One arrow, two heads": Krishna hides the sun so that Arjuna can keep his vow, in
Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen, two-tier headlines
and rod-puppet motion as the Jarasandha, Kaikeyi, Lakshman Rekha and Mandhata reels, with the cast from
jayadratha_cast. Told by a narrator for someone who has never heard the Mahabharata (owner, 9 Nov 2026: "explain
correctly so even who never saw Mahabaratha or even kid can understand clearly"): ONE point per shot, and the logic on
screen in plain labels: who is who, the vow's sunset deadline (a sun travelling along a day-arc to a red SUNSET mark),
the Kauravas' plan as a card with an arrow, the rule that the day's battle stopped at sunset, and why Jayadratha came
out (to watch Arjuna go into the fire).

Respect: Krishna is calm and wise, never a trickster cartoon; Arjuna keeps his dignity. No gore at all: the head is
only ever a small dark round silhouette (a pale rim so it reads on the dark sky), the father's death is a burst of
light and a white flash on his silhouette, after which he is gone and only drifting lights remain.

Every frame is a pure function of t. English on-screen text only (shared by Hindi and Kannada); cues are words of the
line in each language ({"hi": ..., "kn": ...}) with a fraction fallback, kept in one table (CUES) that the scenes and
sfx() both read, with minimum gaps so a fast voice can't bunch the beats together.

Shot list (line: what is on the screen)
  y1  HOOK, frame 0: Krishna alone and large, his hand raised to a sun already half behind the dark disc; ONE ARROW, /
      TWO HEADS (big word in by 0.3 s); the disc closes on "suraj"; an arrow flies in under the headline on "teer";
      two small crowns fall and land on "do sir"
  y2  THIS IS NOT A / FILM SCENE (crossed out); a palm-leaf book opens: MAHABHARATA / BOOK 7: DRONA PARVA (ringed)
  y3  WHO IS WHO: the chariot: Arjuna with his bow (tag ARJUNA: GREATEST ARCHER (PANDAVAS)), Krishna at the reins with
      a whip (tag KRISHNA: HIS CHARIOTEER); each lit as he is named
  y4  ON THE KAURAVA SIDE: / JAYADRATHA (palm leaf JAYADRATHA / A KING ON THE KAURAVA SIDE); the chakravyuha builds
      behind him, he blocks its door, the Pandavas' shadows are pushed back: HE BLOCKED THE DOOR; inside, small
      Abhimanyu (tag ARJUNA'S SON ABHIMANYU) falls gently and fades: ABHIMANYU DIED (in ink)
  y5  Arjuna raises his bow beside a pyre: ARJUNA'S / VOW; a torn note: BEFORE SUNSET: / KILL JAYADRATHA / IF NOT: /
      ARJUNA ENTERS THE FIRE; the day-arc with the sun and a red SUNSET deadline (ringed); the pyre flares on "aag"
  y6  THE KAURAVAS HAD / A PLAN: a card KAURAVA PLAN: / HIDE HIM TILL SUNSET / (a red arrow drawn down) / ARJUNA DIES;
      soldiers close in round Jayadratha below
  y7  THEY HID JAYADRATHA INSIDE / THE WHOLE ARMY: two rows of soldiers march in; he sinks out of sight behind raised
      shields (ringed)
  y8  ARJUNA FOUGHT / ALL DAY: Arjuna shoots again and again into a wall of shields; the sun slides down the day-arc
      towards SUNSET, the light warms; EVENING... / STILL FAR: a dotted line to a tiny Jayadratha on a far hill
  y9  THEN KRISHNA / HID THE SUN: Krishna lifts his hand, the dark disc (tag YOGA-MAYA) slides over the sun, darkness
      spreads from it
  y10 THE KEY RULE: EVERYONE THOUGHT: / SUNSET!, soldiers look up; then THE RULE OF THIS WAR: / SUNSET = STOP and a card
      AT SUNSET, THE DAY'S / BATTLE STOPPED, the soldiers lower their spears and shields
  y11 the Kauravas cheer, spears high (sound rings), the pyre flares behind them: THE KAURAVAS CHEERED: / ARJUNA FAILED!
      then ARJUNA FAILED! / NOW HE MUST BURN!
  y12 the soldiers part; Jayadratha strolls out, relaxed, and turns to the pyre where Arjuna stands (a dotted line of
      sight): JAYADRATHA RELAXED AND / CAME OUT, then HE CAME OUT TO WATCH / ARJUNA BURN
  y13 the chariot again (callback to the hook), the sun still behind the disc with light round its rim: THE SUN HAS /
      NOT SET! (ring on the sun); Krishna swings his arm to Jayadratha standing in the open, Arjuna draws: THERE HE IS!
  y14 BUT THERE WAS ONE / DANGER; the old father (tag JAYADRATHA'S FATHER) raises a warning hand; a torn note HIS
      FATHER'S BOON: / WHOEVER DROPS MY SON'S HEAD / TO THE GROUND, / THEIR OWN HEAD BURSTS / IN 100 PIECES
  y15 Krishna explains, pointing: DON'T LET IT TOUCH THE / GROUND (a red X on the ground under Jayadratha), then SEND IT
      TO HIS / FATHER'S LAP: a dotted arc draws itself to the far hermitage where the father prays; his lap is ringed
  y16 Arjuna shoots; Jayadratha is gone in a flash of light; a small dark round silhouette rides the arrow along the
      dotted arc and lands in the praying father's lap: ARJUNA'S ARROW CARRIED IT / FAR AWAY ... INTO HIS FATHER'S / LAP
  y17 close on the hermitage: the father finishes his prayer and stands (THE FATHER / STOOD UP); the dark shape falls
      to the ground (IT FELL TO THE / GROUND); a dark ring gathers round his head, then a burst of light, his figure
      goes to silhouette, a white flash, and he is gone: HIS OWN BOON / KILLED HIM
  y18 Krishna lowers his hand; the disc slides away, the darkness lifts, the sun shines; the day-arc shows it short of
      SUNSET: THEN KRISHNA REMOVED / THE DARKNESS, then THE SUN WAS / STILL UP (ringed)
  y19 SO, KRISHNA'S MOVE WAS...: two cards CLEVER? / CHEATING?, a red ring alternating; Krishna small and calm below
"""
import math

import cairo

import jayadratha_cast as J
import puppet_cast as C
import puppet_core as pc
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, text_size
from puppet_core import H, W, depth, keyed, prop, puppet, sway
from scenes_jarasandha import (FADE, FEET, INK, RED, bob_rot, glow, ground, man_angles, motes, red_ring, sound_rings)
from scenes_kaikeyi import ANJALI, card, fig, leaf_tag
from scenes_lakshman_rekha import big_q, big_x, book, quote_note, sparkle
from scenes_mandhata import aura, burst, held, lights, local, mix, reach_arm, warm, yajna_fire
from scenes_ravana import dotted, head2
from shots import T, shot_at

MISSES = set()                       # cue words not found in a line (falls back to fractions)
NIGHT = 0.42
SIL = (0.07, 0.04, 0.03)             # silhouettes


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
    "y1": (("S", {"hi": "सूरज", "kn": "ಸೂರ್ಯನನ್ನ"}, 0.3, (("t0", 0.5),)),
           ("A", {"hi": "तीर", "kn": "ಬಾಣದಿಂದ"}, 0.68, (("S", 0.8),)),
           ("H", {"hi": "दो", "kn": "ಎರಡು"}, 0.8, (("A", 0.4),))),
    "y2": (("X", {"hi": "नहीं", "kn": "ಅಲ್ಲ"}, 0.35, (("t0", 0.6),)),
           ("M", {"hi": "महाभारत", "kn": "ಮಹಾಭಾರತದ"}, 0.55, (("X", 0.5),)),
           ("D", {"hi": "द्रोण", "kn": "ದ್ರೋಣ"}, 0.72, (("M", 0.5),))),
    "y3": (("A", {"hi": "अर्जुन", "kn": "ಅರ್ಜುನ"}, 0.2, (("t0", 0.3),)),
           ("B", {"hi": "धनुर्धारी", "kn": "ಬಿಲ್ಲುಗಾರ"}, 0.5, (("A", 0.6),)),
           ("K", {"hi": "कृष्ण", "kn": "ಕೃಷ್ಣ"}, 0.72, (("B", 0.6),)),
           ("R", {"hi": "सारथी", "kn": "ಸಾರಥಿ"}, 0.9, (("K", 0.3),))),
    "y4": (("J", {"hi": "जयद्रथ", "kn": "ಜಯದ್ರಥ"}, 0.03, ()),
           ("K", {"hi": "कौरवों", "kn": "ಕೌರವರ"}, 0.15, (("J", 0.3),)),
           ("B", {"hi": "रोका", "kn": "ತಡೆದ"}, 0.55, (("K", 1.0),)),
           ("A", {"hi": "अभिमन्यु", "kn": "ಅಭಿಮನ್ಯು"}, 0.78, (("B", 0.9),)),
           ("M", {"hi": "मारा", "kn": "ಸತ್ತುಹೋದ"}, 0.9, (("A", 0.4),))),
    "y5": (("V", {"hi": "क़सम", "kn": "ಪ್ರತಿಜ್ಞೆ"}, 0.12, (("t0", 0.3),)),
           ("S", {"hi": "सूरज", "kn": "ಸೂರ್ಯ"}, 0.3, (("V", 0.5),)),
           ("J", {"hi": "जयद्रथ", "kn": "ಜಯದ್ರಥನನ್ನ"}, 0.45, (("S", 0.5),)),
           ("N", {"hi": "नहीं", "kn": "ಆಗಲಿಲ್ಲ"}, 0.62, (("J", 0.7),)),
           ("F", {"hi": "आग", "kn": "ಬೆಂಕಿಗೆ"}, 0.85, (("N", 0.6),))),
    "y6": (("K", {"hi": "कौरवों", "kn": "ಕೌರವರು"}, 0.05, ()),
           ("H", {"hi": "शाम", "kn": "ಸಂಜೆವರೆಗೆ"}, 0.25, (("t0", 0.5),)),
           ("S", {"hi": "सूरज", "kn": "ಸೂರ್ಯ"}, 0.6, (("H", 1.0),)),
           ("D", {"hi": "मर", "kn": "ಸಾಯ್ತಾನೆ"}, 0.88, (("S", 0.6),))),
    "y7": (("J", {"hi": "जयद्रथ", "kn": "ಜಯದ್ರಥನನ್ನ"}, 0.2, (("t0", 0.2),)),
           ("A", {"hi": "सेना", "kn": "ಸೈನ್ಯದ"}, 0.6, (("J", 0.4),)),
           ("H", {"hi": "छिपा", "kn": "ಬಚ್ಚಿಟ್ರು"}, 0.85, (("A", 0.4),))),
    "y8": (("F", {"hi": "लड़ता", "kn": "ಹೋರಾಡಿದ"}, 0.15, (("t0", 0.2),)),
           ("E", {"hi": "शाम", "kn": "ಸಂಜೆ"}, 0.45, (("F", 0.9),)),
           ("R", {"hi": "दूर", "kn": "ದೂರದಲ್ಲಿದ್ದ"}, 0.85, (("E", 0.8),))),
    "y9": (("K", {"hi": "कृष्ण", "kn": "ಕೃಷ್ಣ"}, 0.08, (("t0", 0.1),)),
           ("Y", {"hi": "योग", "kn": "ಯೋಗಮಾಯೆಯಿಂದ"}, 0.3, (("K", 0.4),)),
           ("C", {"hi": "ढक", "kn": "ಮುಚ್ಚಿಬಿಟ್ಟ"}, 0.55, (("Y", 0.5),)),
           ("D", {"hi": "अंधेरा", "kn": "ಕತ್ತಲು"}, 0.8, (("C", 0.5),))),
    "y10": (("T", {"hi": "सूरज", "kn": "ಸೂರ್ಯ"}, 0.15, (("t0", 0.2),)),
            ("R", {"hi": "रोज़", "kn": "ದಿನಾ"}, 0.5, (("T", 1.0),)),
            ("B", {"hi": "लड़ाई", "kn": "ಯುದ್ಧ"}, 0.8, (("R", 0.5),)),
            ("X", {"hi": "रुक", "kn": "ನಿಲ್ತಿತ್ತು"}, 0.9, (("B", 0.3),))),
    "y11": (("C", {"hi": "चिल्लाए", "kn": "ಕೂಗಿದ್ರು"}, 0.3, (("t0", 0.3),)),
            ("L", {"hi": "हार", "kn": "ಸೋತ"}, 0.5, (("C", 0.4),)),
            ("F", {"hi": "आग", "kn": "ಬೆಂಕಿಗೆ"}, 0.82, (("L", 0.6),))),
    "y12": (("J", {"hi": "जयद्रथ", "kn": "ಜಯದ್ರಥ"}, 0.03, ()),
            ("O", {"hi": "बाहर", "kn": "ಹೊರಗೆ"}, 0.5, (("t0", 0.9),)),
            ("W", {"hi": "देखने", "kn": "ನೋಡೋಕೆ"}, 0.9, (("O", 0.9),))),
    "y13": (("K", {"hi": "कृष्ण", "kn": "ಕೃಷ್ಣ"}, 0.08, (("t0", 0.1),)),
            ("S", {"hi": "सूरज", "kn": "ಸೂರ್ಯ"}, 0.3, (("K", 0.4),)),
            ("N", {"hi": "नहीं", "kn": "ಮುಳುಗಿಲ್ಲ"}, 0.45, (("S", 0.35),)),
            ("J", {"hi": "जयद्रथ", "kn": "ಜಯದ್ರಥ"}, 0.75, (("N", 0.6),))),
    "y14": (("D", {"hi": "ख़तरा", "kn": "ಅಪಾಯ"}, 0.1, (("t0", 0.3),)),
            ("F", {"hi": "पिता", "kn": "ತಂದೆಯ"}, 0.28, (("D", 0.6),)),
            ("G", {"hi": "ज़मीन", "kn": "ನೆಲಕ್ಕೆ"}, 0.6, (("F", 1.2),)),
            ("B", {"hi": "सौ", "kn": "ನೂರು"}, 0.85, (("G", 0.8),))),
    "y15": (("K", {"hi": "कृष्ण", "kn": "ಕೃಷ್ಣ"}, 0.1, (("t0", 0.1),)),
            ("G", {"hi": "ज़मीन", "kn": "ನೆಲಕ್ಕೆ"}, 0.35, (("K", 0.5),)),
            ("L", {"hi": "गोद", "kn": "ತೊಡೆ"}, 0.85, (("G", 1.0),))),
    "y16": (("A", {"hi": "तीर", "kn": "ಬಾಣ"}, 0.1, (("t0", 0.7),)),
            ("P", {"hi": "पूजा", "kn": "ಪೂಜೆ"}, 0.55, (("A", 1.0),)),
            ("L", {"hi": "गोद", "kn": "ತೊಡೆ"}, 0.8, (("P", 0.8),))),
    "y17": (("U", {"hi": "उठे", "kn": "ಎದ್ರು"}, 0.2, (("t0", 0.3),)),
            ("G", {"hi": "ज़मीन", "kn": "ನೆಲಕ್ಕೆ"}, 0.45, (("U", 0.75),)),
            ("B", {"hi": "सौ", "kn": "ನೂರು"}, 0.82, (("G", 0.9),))),
    "y18": (("K", {"hi": "कृष्ण", "kn": "ಕೃಷ್ಣ"}, 0.05, ()),
            ("R", {"hi": "हटा", "kn": "ತೆಗೆದ"}, 0.3, (("t0", 0.6),)),
            ("S", {"hi": "सूरज", "kn": "ಸೂರ್ಯ"}, 0.55, (("R", 0.5),))),
    "y19": (("C", {"hi": "बुद्धिमानी", "kn": "ಬುದ್ಧಿವಂತಿಕೆನಾ"}, 0.3, (("t0", 0.5),)),
            ("X", {"hi": "धोखा", "kn": "ಮೋಸನಾ"}, 0.55, (("C", 0.5),)),
            ("M", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.8, (("X", 0.4),))),
}

def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_jd_cues", None)
    if cache is None:
        cache = {}
        tl._jd_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, words, frac, cons in CUES[bid]:
            v = cue(tl, bid, words, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


def to_user(cr, p):
    return cr.device_to_user(*p)


def tag(cr, t, t_in, text, x, y, size=44, alpha=1.0, color=INK, t_out=None):
    """scenes_jarasandha.tag (a small leather name plaque dropping in on its rod), with the edge dots drawn as dots
    and the parchment opaque, so it also reads on the dark shots."""
    p = clamp((t - t_in) / 0.3)
    if t_out is not None:
        p = min(p, 1 - clamp((t - t_out) / 0.25))
    if p <= 0:
        return
    w, h = text_size(text, size, MONO_FONT, 2)
    bw, bh = w + 54, h + 34
    yy = y - 40 * (1 - back(p))
    pc.rod(cr, x, yy + bh / 2, x + 30, H + 50, alpha=0.5 * p * alpha)
    cr.save()
    cr.translate(x, yy)
    pc.poly(cr, [(-bw / 2, -bh / 2 + 10), (-bw / 2 + 10, -bh / 2), (bw / 2 - 10, -bh / 2), (bw / 2, -bh / 2 + 10),
                 (bw / 2, bh / 2 - 10), (bw / 2 - 10, bh / 2), (-bw / 2 + 10, bh / 2), (-bw / 2, bh / 2 - 10)])
    cr.set_source_rgba(0.96, 0.84, 0.58, 0.96 * p * alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, p * alpha)
    cr.set_line_width(4)
    cr.stroke()
    for k in range(int(bw // 18)):
        for yd in (-bh / 2 + 7, bh / 2 - 7):
            cr.new_sub_path()
            cr.arc(-bw / 2 + 12 + k * 18, yd, 2.2, 0, 2 * math.pi)
    cr.set_source_rgba(0.55, 0.32, 0.14, 0.8 * p * alpha)
    cr.fill()
    draw_text(cr, text, 0, 1, size, color, p * alpha, MONO_FONT, "cm", tracking=2)
    cr.restore()


def flash_at(t, t_f, k=0.3, rate=4.0):
    return k * math.exp(-rate * max(0.0, t - t_f)) * (t > t_f)


# ------------------------------------------------------------------ light, dark and silhouettes


def shroud(cr, x, y, r, a):
    """Darkness spreading from (x, y): full `a` inside 0.55 r, fading out at r."""
    if a <= 0.01 or r <= 1:
        return
    g = cairo.RadialGradient(x, y, r * 0.55, x, y, r)
    g.add_color_stop_rgba(0, 0.03, 0.02, 0.06, a)
    g.add_color_stop_rgba(1, 0.03, 0.02, 0.06, 0.0)
    cr.save()
    cr.set_source(g)
    cr.paint()
    cr.restore()


def tint(cr, col, a):
    """A coloured light over the whole cloth (evening)."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(*col, a)
    cr.paint()
    cr.restore()


def silhouette(cr, fn, a, col=SIL):
    """Whatever fn(cr) draws, as one flat dark shadow (punched holes stay light)."""
    if a <= 0.01:
        return None
    cr.push_group()
    res = fn(cr)
    pat = cr.pop_group()
    cr.save()
    cr.set_source_rgba(*col, a)
    cr.mask(pat)
    cr.restore()
    return res


def head_sil(cr, x, y, r, rot=0.0, alpha=1.0, rim=1.0):
    """The head: only ever a small dark round silhouette with a tiny crown outline, a pale rim so it reads on dark."""
    if alpha <= 0.01:
        return
    if rim > 0:
        glow(cr, x, y, r * 3.0, 0.35 * rim * alpha)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.new_path()
    pc.ell(cr, 0, 0, r, r * 1.08)
    pts = [(-0.62 * r, -0.72 * r), (-0.55 * r, -1.25 * r), (-0.28 * r, -0.95 * r), (0, -1.42 * r),
           (0.28 * r, -0.95 * r), (0.55 * r, -1.25 * r), (0.62 * r, -0.72 * r)]
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.close_path()
    path = cr.copy_path()
    if rim > 0:
        cr.set_source_rgba(1.0, 0.9, 0.66, 0.75 * rim * alpha)
        cr.set_line_width(5)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
        cr.append_path(path)
    cr.set_source_rgba(*SIL, 0.96 * alpha)
    cr.fill()
    cr.restore()


def sun_disc(cr, t, x, y, s, cover=0.0, side=1.0, glow_a=1.0, alpha=1.0, red=0.0):
    """The sun (radius 200 s) and the dark disc of yoga-maya sliding over it from `side` (cover 0 = away, 1 = right
    over it); while it covers the sun, a corona of light still shows round its rim: the sun is still up."""
    glow(cr, x, y, 420 * s + 120, glow_a * alpha * (0.55 * (1 - 0.75 * cover) + 0.12))
    warm(cr, x, y, 300 * s, 0.5 * (1 - cover) * glow_a * alpha, (1.0, 0.72 - 0.3 * red, 0.18))
    prop(cr, "sun", x, y, s, rot=t * 0.2, alpha=alpha)
    if red > 0:
        tint_disc(cr, x, y, 200 * s, red * alpha)
    if cover > 0.01:
        ca = clamp((cover - 0.55) / 0.45)
        aura(cr, t, x, y, 200 * s, 380 * s, 0.95 * ca * alpha, n=26, spin=0.08)
        d = (1 - cover) * 470 * s
        prop(cr, "jd_maya", x + d * side, y - 0.3 * d, s, rot=-0.25 * t, alpha=alpha)


def tint_disc(cr, x, y, r, a):
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(1.0, 0.45, 0.30, 0.6 * a)
    cr.fill()
    cr.restore()


def drift_lights(cr, t, x, y, w, h, n, a, col=(1.0, 0.86, 0.45), speed=0.35, ph=0.0):
    for i in range(n):
        u = (t * speed + i / n + ph) % 1.0
        gx = x + w * (((i * 0.618) % 1.0) - 0.5) + 16 * math.sin(t * 1.7 + i)
        gy = y - h * u
        sparkle(cr, gx, gy, (10 + 7 * (i % 3)) * math.sin(math.pi * u), a, col)


# ------------------------------------------------------------------ puppets


AR_B = 1.05


def bow_cb(store, arm, bs, tilt, sprite, alpha, blur):
    """extra= callback: the bow held in a hand (upright + tilt), recording its string tips and grip (device)."""
    rot = -(arm[0] + arm[1]) + tilt

    def fn(cr_):
        cr_.save()
        cr_.translate(4, 150)
        cr_.rotate(rot)
        cr_.scale(bs, bs)
        pc.paint_part(cr_, sprite, alpha, blur)
        store["tips"] = (cr_.user_to_device(-88, -338), cr_.user_to_device(-88, 338))
        store["grip"] = cr_.user_to_device(0, 0)
        cr_.restore()
    return fn


def arrow_at(cr, x0, y0, ang, length, alpha=1.0, blur=0.0):
    """The arrow sprite from its nock at (x0, y0) pointing along ang, `length` px long."""
    prop(cr, "jd_arrow", x0, y0, length / 356.0, rot=ang, alpha=alpha, blur=blur)


def arjuna(cr, t, x, s, bow="carry", aim=-0.6, draw=0.0, arrow=True, feet=FEET, y=None, front=None, backa=None,
           alpha=1.0, blur=0.0, rods=True, head=0.0, hits=(), ph=0.0, rot=0.0):
    """Arjuna (facing right). bow: 'carry' (strung bow upright in the back hand), 'raise' (held high in the front
    hand: the vow), 'aim' (the bow arm straight out along the screen angle `aim`, draw 0..1 pulls the string back
    with an arrow nocked). Returns his points (device) plus 'grip' / 'nock' (user) when aiming."""
    hy = feet - 434 * s if y is None else y
    store = {}
    if bow == "aim":
        fr = (aim - math.pi / 2, 0.0)
        dx, dy = math.cos(aim), math.sin(aim)
        sx, sy = x + 26 * AR_B * s, hy - 262 * s
        k = (300 - 70 - 170 * draw) * s
        ba = reach_arm(x, hy, s, -14 * AR_B, (sx + k * dx, sy + k * dy))
        extra = {"jd_arjuna_armF_lo": bow_cb(store, fr, 0.8, aim, "jd_gandiva_bare" if draw > 0.02 else "jd_gandiva",
                                             alpha, blur)}
    elif bow == "raise":
        fr = front or (-2.95, -0.12)
        ba = backa or (0.3, -0.25)
        extra = {"jd_arjuna_armF_lo": bow_cb(store, fr, 0.8, 0.0, "jd_gandiva", alpha, blur)}
    else:
        fr = front or (-0.32, -0.55)
        ba = backa or (0.3, -0.25)
        extra = {"jd_arjuna_armB_lo": bow_cb(store, ba, 0.72, 0.0, "jd_gandiva", alpha, blur)}
    pts = fig(cr, J.ARJUNA, "jd_arjuna", t, x, s, front=fr, backa=ba, head=head, hits=hits, alpha=alpha, blur=blur,
              rods=rods, rot=rot, feet=feet, ph=ph, extra=extra, y=y)
    if bow == "aim" and "tips" in store:
        g = to_user(cr, store["grip"])
        hb = to_user(cr, pts["handB"])
        pts["grip"] = g
        pts["nock"] = hb
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
                ang = math.atan2(g[1] - hb[1], g[0] - hb[0])
                arrow_at(cr, hb[0], hb[1], ang, math.dist(g, hb) + 80 * s, alpha, blur)
    return pts


def krishna(cr, t, x, s, whip=False, **kw):
    if whip:
        ba = kw.get("backa", (0.3, -0.25))
        kw.setdefault("extra", {"krishna_armB_lo": held("jd_whip", ba, 0.75, tilt=-0.3, alpha=kw.get("alpha", 1.0),
                                                        blur=kw.get("blur", 0.0))})
    return fig(cr, C.KRISHNA, "krishna", t, x, s, **kw)


def jaya(cr, t, x, s, **kw):
    return fig(cr, J.JAYA, "jd_jaya", t, x, s, **kw)


JD_PROUD = dict(front=(-0.25, -2.35), backa=(0.75, -1.6))          # fist on the chest, the other hand on the hip


def soldier(cr, t, x, feet, s, raise_=0.0, flip=False, ph=0.0, alpha=1.0, blur=0.0, legs=(0.0, 0.0), cheer=0.0,
            guard=0.0, rods=False, rot=0.0):
    """A Kaurava soldier, a spear in the front hand (raise_ lifts it overhead), a round shield on the back arm
    (guard 0..1 raises it in front of him); cheer 0..1 makes him jump."""
    jump = cheer * abs(math.sin(t * 7.0 + ph * 3.1)) * 42 * s
    fr = (-0.45 - 2.1 * raise_, -1.15 + 1.0 * raise_)
    ba = mix((-0.25, -1.25), (-1.55, -0.75), guard)
    sh = {"jd_soldier_armB_lo": lambda cr_: _shield_in(cr_, alpha, blur),
          "jd_soldier_armF_lo": held("jd_spear", fr, 0.75, tilt=0.15 * raise_, alpha=alpha, blur=blur)}
    return fig(cr, J.SOLDIER, "jd_soldier", t, x, s, front=fr, backa=ba, legs=legs, flip=flip, alpha=alpha, blur=blur,
               rods=rods, rot=rot + 0.04 * cheer * math.sin(t * 7.0 + ph * 3.1), feet=feet - jump, ph=ph, extra=sh)


def _shield_in(cr_, alpha, blur):
    cr_.save()
    cr_.translate(6, 90)
    cr_.scale(0.95, 0.95)
    pc.paint_part(cr_, "jd_shield", alpha, blur)
    cr_.restore()


def father(cr, t, x, feet, s, rise=0.0, alpha=1.0, blur=0.0, flip=False, ph=0.0, rods=True, eyes=None, front=None,
           backa=None, head=0.0):
    """Vriddhakshatra. rise 0 = seated cross-legged in prayer (hands joined, eyes shut), 1 = standing; in between a
    quick rod-puppet lift. Returns his points (device) plus 'lap' and 'head_u' (user)."""
    q = clamp(rise)
    seated = q < 0.5
    hy_sit = feet - J.SEAT_H * s
    hy_st = feet - 434 * s
    hy = hy_sit + (hy_st - hy_sit) * ease(q)
    shut = (q < 0.3) if eyes is None else (eyes == "shut")
    fr = front or mix(ANJALI["front"], (-0.35, -0.45), ease(q))
    ba = backa or mix(ANJALI["backa"], (0.25, -0.3), ease(q))
    swap = {"jd_vk_head": "jd_vk_head_pray"} if shut else {}
    hide = ()
    extra = None
    if seated:
        swap["jd_vk_body"] = "jd_vk_body_sit"
        hide = ("jd_vk_legF", "jd_vk_legB")
        extra = {"jd_vk_body": lambda cr_: pc.paint_part(cr_, "jd_vk_seat", alpha, blur)}
    b_extra = 6 * math.sin(math.pi * q) if 0 < q < 1 else 0.0
    ang = man_angles("jd_vk", t, fr, ba, head, (0.0, 0.0), (), ph)
    r = bob_rot(t, ph, 0.008)
    pts = puppet(cr, J.VK, x, hy, s, r, flip, ang, alpha, blur + b_extra, hide=hide, swap=swap, rods=rods, extra=extra)
    pts["lap"] = local(x, hy, s, r, flip, *J.LAP)
    pts["head_u"] = to_user(cr, pts["head"])
    return pts


# ------------------------------------------------------------------ the chariot


AR_DX, KR_DX = -262.0, 228.0          # where Arjuna and Krishna stand on the deck (chariot units)


def chariot(cr, t, x, feet, s, ar=None, kr=None, alpha=1.0, blur=0.0, horses=True, rods=True, ph=0.0):
    """The chariot (pivot on the ground under the axle), Arjuna at the back, Krishna at the front; ar / kr = keyword
    dicts for arjuna() / krishna() or None. Returns {'arjuna': pts, 'krishna': pts, 'mouth': (x, y)}."""
    out = {}
    hx = x + J.HORSE_DX * s
    if horses:
        prop(cr, "jd_horse_far", hx + 80 * s, feet - 16 * s, s * 0.98, rot=sway(t, 0.006, 0.8, 1.0 + ph), alpha=alpha,
             blur=blur + 1.5)
    prop(cr, "jd_chariot_back", x, feet, s, alpha=alpha, blur=blur)
    deck = feet - J.DECK * s
    cr.save()                                           # the riders stand behind the car's side panel
    cr.new_path()
    cr.rectangle(-2000, -2000, W + 4000, H + 4000)
    pc.spath(cr, [(x + px * s, feet + py * s) for px, py in J.PANEL])
    cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    cr.clip()
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    cr.rectangle(-2000, -2000, W + 4000, deck + 2000 - 60 * s)
    cr.clip()
    if ar is not None:
        out["arjuna"] = arjuna(cr, t, x + AR_DX * s, s, feet=deck, alpha=alpha, blur=blur, rods=False, **ar)
    if kr is not None:
        out["krishna"] = krishna(cr, t, x + KR_DX * s, s, feet=deck, alpha=alpha, blur=blur, rods=False, **kr)
    cr.restore()
    prop(cr, "jd_chariot", x, feet, s, alpha=alpha, blur=blur)
    if horses:
        prop(cr, "jd_horse", hx, feet, s, rot=sway(t, 0.006, 0.8, ph), alpha=alpha, blur=blur)
    prop(cr, "jd_wheel", x + J.WHEEL_XY[0] * s, feet + J.WHEEL_XY[1] * s, s, rot=0.04 * math.sin(t * 0.8),
         alpha=alpha, blur=blur)
    if rods:
        pc.rod(cr, x - 60 * s, feet - 420 * s, x - 110 * s, H + 60, alpha=0.6 * alpha, blur=blur)
        if horses:
            pc.rod(cr, hx, feet - 600 * s, hx + 40 * s, H + 60, alpha=0.6 * alpha, blur=blur)
    out["mouth"] = (hx + 570 * s, feet - 770 * s)
    return out


def point_at(x, hy, s, target, bulk=1.0):
    """front=(upper, fore) for a straight front arm pointing from the shoulder at target (facing right)."""
    sx, sy = x + 26 * bulk * s, hy - 262 * s
    a = math.atan2(target[1] - sy, target[0] - sx)
    return (a - math.pi / 2, 0.0)


# ------------------------------------------------------------------ the chariot shot (kept from the first cut)


SHOUT = dict(x=262, feet=1790, s=0.53)        # the chariot in the shout shots
SUN_SHOUT = (770, 830, 0.68)


def shout_scene(cr, t, t0, tS, tN, t_draw0, t_draw1, cover, night=0.0):
    sx, sy, ss = SUN_SHOUT
    sun_disc(cr, t, sx, sy, ss, cover=cover)
    ground(cr, y=SHOUT["feet"] + 6)
    x, feet, s = SHOUT["x"], SHOUT["feet"], SHOUT["s"]
    deck = feet - J.DECK * s
    kx = x + KR_DX * s
    hy = deck - 434 * s
    fr = point_at(kx, hy, s, (sx - 40, sy + 30))
    lift = keyed(t, [(t0 - 0.5, 0.75), (t0 + 0.15, 1.0)], 0.3, 1.4)
    fr = mix((-1.0, -0.6), fr, lift)
    draw = clamp((t - t_draw0) / max(0.3, t_draw1 - t_draw0))
    out = chariot(cr, t, x, feet, s,
                  ar=dict(bow="aim", aim=-0.72, draw=0.35 + 0.65 * ease(draw), head=-0.06, ph=1.0),
                  kr=dict(front=fr, backa=(0.35, -0.3), head=-0.14, hits=[(tS, 0.4)], ph=0.4))
    return out



# ------------------------------------------------------------------ y4  Jayadratha blocks the chakravyuha


VY_C = (560.0, 985.0)                # the spiral's centre
VY_SQ = 0.8                          # vertical squash (seen a little from above)
VY_T = 2.2 * 2 * math.pi             # how far the spiral winds
VY_R0, VY_R1 = 60.0, 420.0


def vy_pt(u):
    """A point on the spiral, u = 0 (the centre) .. 1 (the mouth, at the bottom)."""
    th = VY_T * u
    r = VY_R0 + (VY_R1 - VY_R0) * u
    a = th + (math.pi / 2 - VY_T)
    return VY_C[0] + r * math.cos(a), VY_C[1] + VY_SQ * r * math.sin(a)


VY_N = 27
VY_SOLDIERS = [0.14 + i / (VY_N - 1) * 0.83 for i in range(VY_N)]


def s_vyuha(cr, t, tl, t0, t1):
    c = cues(tl, "y4")
    tC, tB, tA, tM = c["J"], c["B"], c["A"], c["M"]
    tP = tB - 0.35
    build = clamp((t - tB + 0.9) / 0.8)
    path = [vy_pt(i / 200) for i in range(201)]
    dotted(cr, path, build, 19, 7.5, (0.50, 0.24, 0.12), 0.8)
    ax, ay = VY_C
    if t > tA - 0.3:                                    # Abhimanyu inside, small, in a soft light; he falls, fades
        fall = ease((t - tM) / 0.9) if t > tM else 0.0
        a = prog(t, tA - 0.3, 0.4) * (1 - 0.65 * fall)
        glow(cr, ax, ay - 40, 200, 0.5 * a)
        fig(cr, J.ABHI, "jd_abhi", t, ax + 30 * fall, 0.2, front=(-1.2, -0.4), backa=(0.6, -0.2), feet=ay + 50,
            rot=-1.35 * fall, alpha=a, blur=2.5 * fall, rods=False, ph=2.0)
    pts = sorted(((vy_pt(u), u, i) for i, u in enumerate(VY_SOLDIERS)), key=lambda p: p[0][1])
    for (px, py), u, i in pts:                          # the soldiers stand along it, in from the mouth inwards
        ti = tB - 0.7 + 0.6 * (1 - u)
        q = back(clamp((t - ti) / 0.3), 1.5)
        if q <= 0:
            continue
        sc = 0.105 + 0.05 * u
        soldier(cr, t, px, py + 4 - 30 * (1 - q), sc, flip=px > ax, ph=i * 0.7, alpha=clamp(q * 1.5))
    ground(cr, y=FEET + 6 + 60)
    push = keyed(t, [(t0, 0.0), (tP, 1.0), (tB, 0.0), (tB + 0.5, 0.5), (tB + 0.9, 0.0)], 0.3, 1.5)
    if t > tP - 0.4:                                    # the Pandavas: shadows pushing in from the left
        b, k, a = depth(t, tP - 0.4, 0.5)
        for i, (rig, key, xx, sc) in enumerate(((C.BHIMA, "bhima", 120, 0.56), (C.KING, "king", 250, 0.5),
                                                (J.SOLDIER, "jd_soldier", 0, 0.5))):
            def sh(cr_, rig=rig, key=key, xx=xx, sc=sc, i=i):
                fig(cr_, rig, key, t, xx + 60 * push - 30 * i, sc * k, front=(-1.5, -0.3), backa=(-1.2, -0.4),
                    feet=FEET + 70, rods=False, ph=i, hits=[(tB, 1.0)])
            silhouette(cr, sh, 0.72 * a * (0.85 if i else 1.0))
    jx, js, jf = 520, 0.5, FEET + 70
    arms = keyed(t, [(t0, 0.0), (tP - 0.2, 1.0)], 0.3, 1.5)
    b, k, a = depth(t, t0 - 0.1, 0.45)
    jaya(cr, t, jx, js * k, flip=True, front=(-0.3 - 1.45 * arms, -0.55 + 0.55 * arms),
         backa=(0.3 + 1.35 * arms, -0.25 + 0.25 * arms), feet=jf, alpha=a, blur=b, hits=[(tB, 0.8)], ph=0.5)
    dev_a = cr.user_to_device(ax, ay - 140)

    def ui(cr):
        if t < tB:
            head2(cr, t, "ON THE KAURAVA SIDE:", t0 + 0.05, "JAYADRATHA", tC, big_size=230)
        elif t < tA:
            head2(cr, t, "HE BLOCKED THE DOOR OF THE", tB, "CHAKRAVYUHA", tB + 0.06, big_size=200, under=tB + 0.4)
            tag(cr, t, tP, "THE PANDAVAS", 200, 1150, 32, t_out=tA - 0.2)
        else:
            head2(cr, t, "INSIDE, ARJUNA'S SON", tA, "ABHIMANYU DIED", tM, big_size=200, big_color=INK)
            tag(cr, t, tA + 0.1, "ARJUNA'S SON ABHIMANYU", 560, dev_a[1] - 110, 30)
        leaf_tag(cr, t, t0 + 0.3, 840, 1560, 0.72, [("JAYADRATHA", 58, HEAD_FONT),
                                                     ("A KING ON THE KAURAVA SIDE", 26, MONO_FONT)], rot=0.03,
                 t_out=tA - 0.2)
    return dict(ui=ui, flash=flash_at(t, tB, 0.3), night=0.15 * prog(t, tM, 0.8))



# ------------------------------------------------------------------ the funeral pyre (the vow)


PYRE = (820, FEET + 40, 0.82)


def pyre(cr, t, x, feet, s, fire=0.0, alpha=1.0):
    if fire > 0:
        glow(cr, x, feet - 330 * s, (420 + 160 * fire) * s, (0.4 + 0.5 * fire) * (0.85 + 0.15 * math.sin(t * 7)))
    prop(cr, "jd_pyre", x, feet, s, alpha=alpha)
    if fire > 0:
        for i, dx in enumerate((-150, 0, 150)):
            f = int(t * 10 + i) % 3
            fs = (0.55 + 0.55 * fire) * s * (0.9 if i != 1 else 1.15)
            prop(cr, f"flame{f}", x + dx * s, feet - 250 * s, fs * (0.92 + 0.1 * math.sin(t * 6 + i)), alpha=alpha)
        lights(cr, t, x, feet - 520 * s, 160 * s, 10, fire * alpha, (1.0, 0.7, 0.3), 0.8)




# ------------------------------------------------------------------ the soldiers: two rows, cheering or standing down


DARK_SUN = (820, 790, 0.5)


def cheering_row(cr, t, cheer, raise_, alpha=1.0, part=0.0):
    for i, (x, sc, fl, b) in enumerate(((150, 0.44, False, 3.0), (380, 0.44, True, 3.0), (640, 0.44, False, 3.0),
                                        (900, 0.44, True, 3.0))):
        soldier(cr, t, x + (1 if x > 540 else -1) * 200 * part, FEET - 40, sc, flip=fl, ph=i * 1.3 + 5,
                alpha=0.85 * alpha, blur=b, raise_=raise_, cheer=cheer)
    ground(cr, y=FEET + 6 + 70)
    for i, (x, sc, fl) in enumerate(((110, 0.62, False), (330, 0.62, True), (560, 0.62, False), (780, 0.62, True),
                                     (990, 0.62, True))):
        soldier(cr, t, x + (1 if x > 540 else -1) * 260 * part, FEET + 80, sc, flip=fl, ph=i * 0.9,
                alpha=alpha, raise_=raise_, cheer=cheer)




# ------------------------------------------------------------------ y14  the father's boon


def s_shield(cr, t, tl, t0, t1):
    c = cues(tl, "y14")
    tD, tF, tG, tB = c["D"], c["F"], c["G"], c["B"]
    ground(cr, y=FEET + 46)
    warn = keyed(t, [(t0, 0.0), (tF, 1.0)], 0.35, 1.3)
    b, k, a = depth(t, t0 - 0.1, 0.45)
    glow(cr, 200, 1420, 420, 0.3 * a)
    father(cr, t, 185, FEET + 40, 0.68 * k, rise=1.0, eyes="open", alpha=a, blur=b,
           front=mix((-0.35, -0.45), (-2.05, -0.85), warn), backa=(0.25, -0.3), head=-0.06, ph=0.6)

    def ui(cr):
        head2(cr, t, "BUT THERE WAS ONE", t0 + 0.05, "DANGER", tD, big_size=250, under=tD + 0.4)
        tag(cr, t, tF + 0.1, "JAYADRATHA'S FATHER", 540, 1330, 34)
        if t > tF - 0.1:
            quote_note(cr, t, tF - 0.1, 610, 880, 0.88,
                       [("HIS FATHER'S BOON:", 46, INK, MONO_FONT, -178, tF + 0.1),
                        ("WHOEVER DROPS MY SON'S HEAD", 70, INK, HEAD_FONT, -92, tF + 0.45),
                        ("TO THE GROUND,", 70, INK, HEAD_FONT, -8, tG),
                        ("THEIR OWN HEAD BURSTS", 70, INK, HEAD_FONT, 76, tG + 0.6),
                        ("IN 100 PIECES", 104, RED, HEAD_FONT, 172, tB)])
    return dict(ui=ui, flash=flash_at(t, tD, 0.25) + flash_at(t, tB, 0.3))



# ------------------------------------------------------------------ y16  the arrow carries it to the father's lap


AR11 = (130, FEET + 90, 0.44)        # Arjuna (x, feet, scale)
JD11 = (455, FEET + 90, 0.4)         # Jayadratha
HERM = (850, 1440, 0.36)             # the far hermitage: the father's x, ground y, scale


def hill(cr, cx, top, w, base, col=(0.86, 0.74, 0.50), alpha=1.0):
    """A far hill of leather (a soft mound from base up to top)."""
    pts = [(cx - w, base + 40), (cx - 0.82 * w, top + 120), (cx - 0.5 * w, top + 14), (cx, top),
           (cx + 0.5 * w, top + 10), (cx + 0.9 * w, top + 70), (cx + 1.2 * w, base + 40)]
    cr.save()
    cr.new_path()
    pc.spath(cr, pts)
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(*col, alpha)
    cr.fill_preserve()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.set_source_rgba(*pc.INK, 0.85 * alpha)
    cr.set_line_width(5)
    cr.stroke()
    cr.restore()


def hermitage_far(cr, t, alpha=1.0, glow_a=0.0):
    fx, gy, fs = HERM
    prop(cr, "tree", fx + 200, gy + 8, 0.4, rot=sway(t, 0.006, 0.3, 2), alpha=0.6 * alpha, blur=5)
    hill(cr, fx + 30, gy, 330, FEET + 52, alpha=alpha)
    prop(cr, "lr_hut", fx + 125, gy + 6, 0.32, alpha=0.8 * alpha, blur=2.0)
    yajna_fire(cr, t, fx - 135, gy, 0.42, 0.2, alpha)
    prop(cr, "md_mat", fx + 30, gy - 2, 0.3, alpha=alpha)
    if glow_a > 0:
        glow(cr, fx + 20, gy - 120, 260, glow_a)
    return father(cr, t, fx, gy, fs, rise=0.0, alpha=alpha, rods=False, ph=0.6)


def arc_pts(p0, p1, peak, n=80):
    """A parabola-like arc from p0 to p1 rising to y = peak."""
    out = []
    for i in range(n + 1):
        u = i / n
        base = p0[1] + (p1[1] - p0[1]) * u
        out.append((p0[0] + (p1[0] - p0[0]) * u, base - (min(p0[1], p1[1]) - peak) * 4 * u * (1 - u)))
    return out


def along(pts, p):
    """The point at fraction p of a polyline's length, and the direction there."""
    lens = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(lens) * clamp(p)
    acc = 0.0
    for (a, b), ln in zip(zip(pts, pts[1:]), lens):
        if acc + ln >= total:
            f = (total - acc) / ln if ln else 0.0
            return (a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f), math.atan2(b[1] - a[1], b[0] - a[0])
        acc += ln
    a, b = pts[-2], pts[-1]
    return b, math.atan2(b[1] - a[1], b[0] - a[0])


def s_arrow(cr, t, tl, t0, t1):
    c = cues(tl, "y16")
    tA, tP, tL = c["A"], c["P"], c["L"]
    sx, sy, ss = 160, 780, 0.34
    shroud(cr, sx, sy, 2600, 0.32)
    aura(cr, t, sx, sy, 200 * ss, 380 * ss, 0.75, n=26, spin=0.08)
    prop(cr, "sun", sx, sy, ss, rot=t * 0.2)
    prop(cr, "jd_maya", sx, sy, ss, rot=-0.25 * t)
    lap_glow = 0.5 * prog(t, tL, 0.3) * math.exp(-1.2 * max(0.0, t - tL - 0.3)) + 0.3 * prog(t, tP, 0.4)
    fp = hermitage_far(cr, t, glow_a=lap_glow)
    lap = fp["lap"]
    ground(cr, y=FEET + 96)
    ax, af, as_ = AR11
    jx, jf, js = JD11
    t_hit = tA + 0.28
    head0 = (jx - 20 * js, jf - 434 * js - 410 * js)
    arc = arc_pts(head0, (lap[0], lap[1] - 22), 720)
    fly = clamp((t - t_hit) / max(0.5, tL - t_hit))
    if t > t_hit:                                       # the path (a dotted arc), drawn ahead of the flight
        dotted(cr, arc, min(1.0, fly + 0.18), 30, 6.5, RED, 0.85)
    if t < t_hit + 0.4:                                 # Jayadratha, looking up; struck, he is gone in the flash
        gone = ease((t - t_hit) / 0.3) if t > t_hit else 0.0
        jaya(cr, t, jx, js, flip=True, feet=jf, head=-0.32, front=(-1.6, -0.3), backa=(0.5, -0.5),
             alpha=1 - gone, blur=10 * gone, rods=t < t_hit, ph=0.3)
    draw = clamp((t - t0 - 0.1) / max(0.3, tA - t0 - 0.2))
    released = t >= tA
    pts = arjuna(cr, t, ax, as_, bow="aim", aim=-0.08, draw=0.0 if released else 0.2 + 0.8 * ease(draw),
                 arrow=not released, feet=af, hits=[(tA, 0.5)], ph=1.0)
    if released and t < t_hit:                          # the arrow to him
        nk = pts.get("nock", (ax + 120, af - 300 * as_))
        u = (t - tA) / (t_hit - tA)
        x0, y0 = nk[0] + (head0[0] - 60 - nk[0]) * u, nk[1] + (head0[1] - nk[1]) * u
        arrow_at(cr, x0, y0, math.atan2(head0[1] - nk[1], head0[0] - 60 - nk[0]), 150)
    if t > t_hit:
        burst(cr, t, head0[0], head0[1] + 80, t_hit, n=18, rmax=420, alpha=1.0)
    if t_hit < t:                                       # the head: a small dark silhouette riding the arrow, seen
        (hx, hy), ang = along(arc, fly)                 # only once it is well away from him, out of the light
        if fly < 1:
            show = clamp((fly - 0.07) / 0.06)
            arrow_at(cr, hx - 125 * math.cos(ang), hy - 125 * math.sin(ang), ang, 118,
                     alpha=show * (1.0 - prog(t, tL - 0.4, 0.3)))
            for k in range(6):                          # a faint trail of light
                (qx, qy), _ = along(arc, max(0.0, fly - 0.02 * (k + 1)))
                sparkle(cr, qx, qy, 14 - 2 * k, (0.5 - 0.07 * k) * show)
            head_sil(cr, hx, hy, 24, rot=0.6 * math.sin(6 * fly), alpha=show)
        else:
            head_sil(cr, lap[0], lap[1] - 22, 22, rot=0.3, alpha=1.0, rim=0.8)
    dev_lap = cr.user_to_device(*lap)
    dev_h = cr.user_to_device(HERM[0], HERM[1] - 330 * HERM[2])

    def ui(cr):
        if t < tL:
            head2(cr, t, "ARJUNA'S ARROW CARRIED IT", t0 + 0.05, "FAR AWAY", tP, big_size=220)
        else:
            head2(cr, t, "INTO HIS FATHER'S", tL, "LAP", tL + 0.06, big_size=260, under=tL + 0.35)
            red_ring(cr, dev_lap[0], dev_lap[1] - 10, 90, 70, prog(t, tL + 0.25, 0.4), 8)
        tag(cr, t, tP, "HIS FATHER, AT PRAYER", min(dev_h[0], 800), dev_h[1] + 330, 30)
    return dict(ui=ui, night=0.3, lift=1.0, flash=flash_at(t, t_hit, 0.6, 3.0))



# ------------------------------------------------------------------ the hermitage close: he stands, it falls, the burst


HC = (470, FEET + 60, 0.84)          # the father in the close shots: x, ground, scale


def herm_close(cr, t, tU, tG, tC=None, tF=None):
    """The hermitage close: the fire, the hut and a tree behind; the father seated with the dark shape in his lap,
    rising at tU (it slips and lands on the ground at tG); tC / tF: the curse and the burst (y13)."""
    x, gy, s = HC
    prop(cr, "tree", 60, gy + 10, 0.66, rot=sway(t, 0.006, 0.3, 1), alpha=0.55, blur=10, flip=True)
    prop(cr, "lr_hut", 960, gy + 8, 0.7, alpha=0.6, blur=7)
    ground(cr, y=gy + 6)
    yajna_fire(cr, t, 920, gy, 0.9, 0.15)
    prop(cr, "md_mat", x + 60, gy - 2, 0.58)
    rise = ease((t - tU) / 0.4) if t > tU else 0.0
    burst_t = tF
    gone = 0.0
    if burst_t is not None and t > burst_t:
        gone = ease((t - burst_t - 0.35) / 0.9)
    sil = clamp((t - burst_t + 0.15) / 0.15) if burst_t is not None else 0.0

    def draw_f(cr_):
        return father(cr_, t, x, gy, s, rise=rise, ph=0.6, rods=False, head=-0.08 * rise)
    if sil > 0:
        silhouette(cr, draw_f, sil * (1 - gone))
    else:
        draw_f(cr)
    hy = gy - J.SEAT_H * s + (J.SEAT_H - 434) * s * rise
    head = (x + 22 * s, hy - 412 * s)
    lap_sit = local(x, gy - J.SEAT_H * s, s, 0, False, *J.LAP)
    # the dark shape: in his lap, then slipping off as he stands and dropping to the ground
    r_h = 46
    if t < tU + 0.12:
        hp, rot = (lap_sit[0], lap_sit[1] - r_h * 0.9), 0.3
    else:
        u = clamp((t - tU - 0.12) / max(0.3, tG - tU - 0.12))
        x0, y0 = lap_sit[0] + 30, lap_sit[1] - r_h * 0.9
        x1, y1 = lap_sit[0] + 125, gy - r_h * 1.05
        hp = (x0 + (x1 - x0) * u, y0 + (y1 - y0) * u * u)
        rot = 0.3 + 0.5 * u
        if t > tG:
            dt = t - tG
            hp = (x1, y1 - 30 * abs(math.sin(9 * dt)) * math.exp(-5 * dt))
            rot = 0.8 - 0.3 * math.exp(-4 * dt)
    head_sil(cr, hp[0], hp[1], r_h, rot=rot, alpha=1.0, rim=0.6)
    if t > tG:
        d = cr.user_to_device(hp[0], gy)
        sound_rings(cr, d[0], d[1] - 10, t, tG, 3, 0.18, 160, alpha=0.4)
    if tC is not None and t > tC and (burst_t is None or t < burst_t + 0.2):
        k = prog(t, tC, 0.5)                            # the curse gathers round his head: a dark ring
        cr.save()
        cr.set_source_rgba(0.12, 0.05, 0.1, 0.5 * k)
        cr.set_line_width(14)
        for i in range(3):
            rr = 120 - 25 * i + 10 * math.sin(t * 5 + i)
            cr.arc(head[0], head[1], rr * (1.3 - 0.3 * k), 0, 2 * math.pi)
            cr.stroke()
        cr.restore()
    if burst_t is not None and t > burst_t:
        burst(cr, t, head[0], head[1], burst_t, n=26, rmax=900, alpha=1.0)
        for i in range(14):                             # shards of light flying out
            a = 2 * math.pi * i / 14 + 0.3
            u = (t - burst_t)
            rr = 40 + 900 * (1 - math.exp(-2.2 * u))
            aa = math.exp(-1.6 * u)
            sparkle(cr, head[0] + rr * math.cos(a), head[1] + rr * math.sin(a), 26 * aa + 4, aa)
        drift_lights(cr, t, x, gy - 200, 260, 700, 10, 0.8 * gone * math.exp(-0.3 * max(0.0, t - burst_t - 1.2)))
    return head, hp



# ------------------------------------------------------------------ the day-arc: the vow's sunset deadline


def sun_clock(cr, t, cx, cy, rx, p, alpha=1.0, cover=0.0, t_in=None):
    """The day as an arc above a horizon: the sun travels from sunrise (left) to SUNSET (right end, a red mark: the
    deadline); p = where the sun is now (0..1); cover hides it behind the dark disc. Returns the sun's position."""
    a = alpha * (prog(t, t_in, 0.35) if t_in is not None else 1.0)
    ry = 0.72 * rx
    u = clamp(p)
    sx, sy = cx - rx * math.cos(math.pi * u), cy - ry * math.sin(math.pi * u)
    if a <= 0.01:
        return sx, sy
    pts = [(cx - rx * math.cos(math.pi * v), cy - ry * math.sin(math.pi * v)) for v in (i / 60 for i in range(61))]
    dotted(cr, pts, 1.0, 24, 5.0, FADE, 0.8 * a)
    cr.save()
    cr.set_source_rgba(*INK, 0.85 * a)
    cr.set_line_width(5)
    cr.move_to(cx - rx - 40, cy)
    cr.line_to(cx + rx + 40, cy)
    cr.stroke()
    cr.set_source_rgba(*RED, 0.95 * a)
    cr.set_line_width(10)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(cx + rx, cy - 44)
    cr.line_to(cx + rx, cy + 22)
    cr.stroke()
    cr.restore()
    draw_text(cr, "SUNSET", cx + rx, cy + 36, 34, RED, a, MONO_FONT, "ct", tracking=2)
    glow(cr, sx, sy, 170, 0.5 * a * (1 - cover))
    prop(cr, "sun", sx, sy, 0.2, rot=t * 0.3, alpha=a)
    if cover > 0.01:
        d = (1 - cover) * 110
        prop(cr, "jd_maya", sx + d, sy - 0.3 * d, 0.2, rot=-0.25 * t, alpha=a)
    return sx, sy


def fit_size(text, size, maxw, font=HEAD_FONT):
    return min(size, int(size * maxw / max(1, text_size(text, size, font)[0])))


# ------------------------------------------------------------------ y1  hook


HOOK_K = (360, 1.0, 1890)            # Krishna in the hook: x, scale, feet
HOOK_SUN = (800, 820, 0.55)


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "y1")
    tS, tA, tH = c["S"], c["A"], c["H"]
    sx, sy, ss = HOOK_SUN
    cov = 0.6 + 0.4 * ease((t - tS + 0.1) / 0.6)
    dark = prog(t, tS, 0.8)
    shroud(cr, sx, sy, 300 + 1500 * dark, 0.28 * dark)
    sun_disc(cr, t, sx, sy, ss, cover=cov)
    x, s, feet = HOOK_K
    hy = feet - 434 * s
    up = keyed(t, [(-1.0, 0.85), (tS - 0.1, 1.0)], 0.3, 1.3)
    fr = mix((-1.6, -0.5), point_at(x, hy, s, (sx - 70, sy + 40)), up)
    glow(cr, x + 40, hy - 330 * s, 520, 0.35)
    krishna(cr, t, x, s, feet=feet, front=fr, backa=(0.3, -0.3), head=-0.16, hits=[(tS, 0.4)], ph=0.4)
    for i, (cx, name, dt) in enumerate(((700, "jd_crown_a", 0.0), (900, "jd_crown_b", 0.22))):
        tf = tH + dt                                    # two small crowns fall and land
        if t > tf - 0.05:
            q = clamp((t - tf + 0.05) / 0.55)
            land = feet - 90
            y = -150 + (land + 150) * q * q
            rot = (0.5 if i else -0.4) * q
            if q >= 1:
                dtt = t - tf - 0.5
                y = land - 40 * abs(math.sin(8 * dtt)) * math.exp(-4 * dtt)
            prop(cr, name, cx, y, 0.7, rot=rot)

    def ui(cr):
        head2(cr, t, "ONE ARROW,", -1.0, "TWO HEADS", 0.3, big_size=250, ghost=-1.0, under=tH + 0.3)
        if t > tA - 0.05:                               # one arrow flies in under the headline
            u = ease((t - tA + 0.05) / 0.45)
            arrow_at(cr, -420 + (W / 2 - 200 + 420) * u, 610, 0.0, 400)
    return dict(ui=ui, flash=flash_at(t, tS, 0.25) + flash_at(t, tH, 0.3))


# ------------------------------------------------------------------ y2  written in the Mahabharata


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "y2")
    tX, tM, tD = c["X"], c["M"], c["D"]
    leaves = [(None, [("MAHABHARATA", 92, HEAD_FONT)], 0),
              (tD + 0.1, [([("BOOK 7:", INK), ("DRONA PARVA", RED)], 76, HEAD_FONT)], 0)]
    book(cr, t, 540, 960, 0.86, leaves, t_in=t0 + 0.05, t_open=tM, ring=(1, 0, 1, tD + 0.45))

    def ui(cr):
        if t < tM:
            struck = t > tX + 0.25
            box = head2(cr, t, "THIS IS NOT A", t0 + 0.05, "FILM SCENE", t0 + 0.35, big_size=210,
                        big_color=FADE if struck else INK)
            if box and t > tX:
                bx, by, bw, bh = box
                big_x(cr, W / 2, by + bh / 2, bw + 60, bh * 0.95, prog(t, tX, 0.3), lw=24)
        else:
            head2(cr, t, "IT'S WRITTEN IN THE", tM, "MAHABHARATA", tM + 0.06, big_size=200, under=tD + 0.3)
    return dict(ui=ui, flash=flash_at(t, tM, 0.25) + flash_at(t, tD, 0.2))


# ------------------------------------------------------------------ y3  who is who


WHO = (262, 1790, 0.53)              # the chariot: x, ground, scale


def s_who(cr, t, tl, t0, t1):
    c = cues(tl, "y3")
    tA, tB, tK, tR = c["A"], c["B"], c["K"], c["R"]
    x, feet, s = WHO
    la, lk = prog(t, tA, 0.3), prog(t, tK, 0.3)
    glow(cr, x + AR_DX * s, feet - 900 * s, 420, 0.5 * la * (1 - 0.6 * lk))
    glow(cr, x + KR_DX * s, feet - 900 * s, 420, 0.5 * lk)
    ground(cr, y=feet + 6)
    lift = keyed(t, [(t0, 0.0), (tB, 1.0)], 0.3, 1.4)
    out = chariot(cr, t, x, feet, s,
                  ar=dict(bow="carry", backa=(0.3 - 0.9 * lift, -0.25 - 0.4 * lift), head=0.0, hits=[(tA, 0.6)],
                          ph=1.0),
                  kr=dict(whip=True, front=(-1.2, -0.6), backa=(-0.5 - 0.5 * lk, -0.9), hits=[(tK, 0.6)], ph=0.4))
    ah, kh = out["arjuna"]["top"], out["krishna"]["top"]

    def ui(cr):
        if t < tK:
            head2(cr, t, "THE PANDAVAS' GREATEST ARCHER:", t0 + 0.05, "ARJUNA", tA, big_size=240)
        else:
            head2(cr, t, "HIS CHARIOTEER:", tK, "KRISHNA", tK + 0.06, big_size=240, under=tR + 0.2)
        for txt, ti, (hx, hy), tx, ty in (("ARJUNA: GREATEST ARCHER (PANDAVAS)", tA + 0.25, ah, 420, 650),
                                          ("KRISHNA: HIS CHARIOTEER", tK + 0.15, kh, 520, 790)):
            if t > ti:
                dotted(cr, [(hx + 10, ty + 30), (hx, hy - 30)], prog(t, ti + 0.2, 0.3), 16, 4.5, INK, 0.55)
                tag(cr, t, ti, txt, tx, ty, 28)
    return dict(ui=ui, flash=flash_at(t, tA, 0.2) + flash_at(t, tK, 0.25))


# ------------------------------------------------------------------ y5  the vow and its deadline


def s_vow(cr, t, tl, t0, t1):
    c = cues(tl, "y5")
    tV, tS, tJ, tN, tF = c["V"], c["S"], c["J"], c["N"], c["F"]
    ground(cr, y=FEET + 46)
    fire = 0.2 * prog(t, t0, 0.5) + 0.8 * prog(t, tF, 0.5)
    pyre(cr, t, 850, FEET + 40, 0.62, fire=fire)
    up = keyed(t, [(t0, 0.0), (tV - 0.1, 1.0)], 0.35, 1.3)
    arjuna(cr, t, 165, 0.72, bow="raise", front=mix((-0.9, -0.7), (-2.4, -0.25), up), backa=(0.35 - 0.2 * up, -0.4),
           head=-0.1 * up, feet=FEET + 40, hits=[(tV, 0.6)], ph=1.0)
    cx, cy, rx = 520, 1400, 165
    sun_clock(cr, t, cx, cy, rx, 0.28, t_in=tS - 0.2)
    end = cr.user_to_device(cx + rx, cy)

    def ui(cr):
        head2(cr, t, "ARJUNA'S", t0 + 0.05, "VOW", tV, big_size=250, under=tV + 0.4)
        if t > tS - 0.1:
            quote_note(cr, t, tS - 0.1, 640, 920, 0.8,
                       [("BEFORE SUNSET:", 56, INK, MONO_FONT, -168, tS),
                        ("KILL JAYADRATHA", 116, INK, HEAD_FONT, -72, tJ),
                        ("IF NOT:", 56, INK, MONO_FONT, 44, tN),
                        ("ARJUNA ENTERS THE FIRE", 104, RED, HEAD_FONT, 148, tF)])
        if t > tS + 0.4:
            red_ring(cr, end[0], end[1] + 10, 100, 72, prog(t, tS + 0.4, 0.4), 8)
    return dict(ui=ui, flash=flash_at(t, tV, 0.35) + flash_at(t, tF, 0.45))


# ------------------------------------------------------------------ y6  the Kauravas' plan


def plan_card(cr, t, t_in, x, y, s, t2, t3):
    """The plan on a torn note: KAURAVA PLAN: / HIDE HIM TILL SUNSET / a red arrow drawn down / ARJUNA DIES."""
    p = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(p)
    if a <= 0.01:
        return
    yy = y + 70 * (1 - p)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(-0.02 + sway(t, 0.006, 0.4))
    cr.scale(s, s)
    pc.paint_part(cr, "rv_note", a)
    draw_text(cr, "KAURAVA PLAN:", 0, -172, 50, INK, a, MONO_FONT, "cm", tracking=4)
    q2 = prog(t, t2, 0.3) * a
    if q2 > 0:
        draw_text(cr, "HIDE HIM TILL SUNSET", 0, -80 + 12 * (1 - q2), fit_size("HIDE HIM TILL SUNSET", 100, 680), INK,
                  q2, HEAD_FONT, "cm")
    qa = ease((t - t3 + 0.45) / 0.4) if t > t3 - 0.45 else 0.0
    if qa > 0:                                          # the arrow, drawn downwards
        y0, y1 = -14, -14 + 92 * qa
        cr.set_source_rgba(*RED, 0.95 * a)
        cr.set_line_width(16)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(0, y0)
        cr.line_to(0, y1)
        cr.stroke()
        if qa > 0.6:
            pc.poly(cr, [(-36, y1 - 20), (36, y1 - 20), (0, y1 + 26)])
            cr.fill()
    q3 = prog(t, t3, 0.3) * a
    if q3 > 0:
        draw_text(cr, "ARJUNA DIES", 0, 160 + 12 * (1 - q3), 124, RED, q3, HEAD_FONT, "cm")
    cr.restore()


def s_plan(cr, t, tl, t0, t1):
    c = cues(tl, "y6")
    tK, tH, tS, tD = c["K"], c["H"], c["S"], c["D"]
    ground(cr, y=FEET + 46)
    jaya(cr, t, 540, 0.46, feet=FEET + 40, front=(-0.4, -0.6), backa=(0.4, -0.4), head=0.04, ph=0.3)
    for i, (x0, x1, fl) in enumerate(((-140, 330, False), (1220, 750, True))):
        q = ease((t - tH - 0.1 * i) / 0.6)
        soldier(cr, t, x0 + (x1 - x0) * q, FEET + 40, 0.46, flip=fl, ph=i * 1.7, alpha=clamp(q * 2), guard=q)

    def ui(cr):
        head2(cr, t, "THE KAURAVAS HAD", t0 + 0.05, "A PLAN", tK + 0.1, big_size=250)
        plan_card(cr, t, t0 + 0.3, 540, 930, 0.88, tH, tD)
    return dict(ui=ui, flash=flash_at(t, tD, 0.3))


# ------------------------------------------------------------------ y7  hidden inside the army


BACK_ROW = (150, 345, 735, 930)       # the soldiers behind him (x), feet at HID_BACK
FRONT_ROW = (100, 280, 460, 620, 800, 980)
HID_BACK, HID_J, HID_FRONT = 1480, 1560, 1700


def s_hidden(cr, t, tl, t0, t1):
    c = cues(tl, "y7")
    tJ, tA, tH = c["J"], c["A"], c["H"]
    sun_disc(cr, t, 905, 700, 0.42)
    ground(cr, y=HID_FRONT + 6)
    close = keyed(t, [(t0, 0.0), (tH, 1.0)], 0.3, 1.2)
    for i, x in enumerate(BACK_ROW):                    # the back of the ring
        q = ease((t - t0 - 0.1 * i) / 0.7)
        x0 = -150 if x < 540 else W + 150
        soldier(cr, t, x0 + (x - x0) * q, HID_BACK, 0.42, flip=x > 540, ph=i * 0.8 + 3, alpha=0.9 * clamp(q * 2))
    jf = HID_J + 130 * close
    jaya(cr, t, 540, 0.5, feet=jf, front=(-0.4, -0.6), backa=(0.4, -0.4), head=0.14 * close, ph=0.3, rods=False,
         alpha=1.0 - 0.35 * close, blur=3.0 * close)
    for i, x in enumerate(FRONT_ROW):                   # the front of the ring closes in, shields up
        q = ease((t - tA + 0.2 - 0.1 * i) / 0.7)
        x0 = -200 if x < 540 else W + 200
        xx = x0 + (x - x0) * q + (1 if x < 540 else -1) * 45 * close * (abs(x - 540) < 150)
        soldier(cr, t, xx, HID_FRONT, 0.5, flip=x > 540, ph=i * 0.9, alpha=clamp(q * 2), guard=close)
    jx, jy = cr.user_to_device(540, jf - 0.5 * 690)

    def ui(cr):
        head2(cr, t, "THEY HID JAYADRATHA INSIDE", t0 + 0.05, "THE WHOLE ARMY", tA, big_size=200)
        tag(cr, t, tJ, "JAYADRATHA", 540, 1150, 32, t_out=tH)
        if t > tH:
            red_ring(cr, jx, jy, 130, 105, prog(t, tH + 0.2, 0.45), 9)
    return dict(ui=ui, flash=flash_at(t, tH, 0.25))


# ------------------------------------------------------------------ y8  fighting all day; evening, still far


FAR_J = (935, 1335, 0.16)            # the far-off Jayadratha: x, feet, scale


def s_far(cr, t, tl, t0, t1):
    c = cues(tl, "y8")
    tF, tE, tR = c["F"], c["E"], c["R"]
    eve = prog(t, tE - 0.3, 1.2)
    p = 0.55 + 0.25 * clamp((t - t0) / max(0.5, tE - t0)) + 0.13 * eve
    cx, cy, rx = 760, 760, 190
    sun_clock(cr, t, cx, cy, rx, p)
    fx, ff, fs = FAR_J
    hill(cr, fx, ff, 200, FEET + 40, alpha=0.9)
    for i, dx in enumerate((-70, -38, 40, 72)):         # the far army round him
        soldier(cr, t, fx + dx, ff + 4 * (i % 2), 0.11, flip=dx > 0, ph=i, alpha=0.85, blur=1.5)
    jaya(cr, t, fx, fs, feet=ff, flip=True, rods=False, ph=0.3, blur=1.0)
    ground(cr, y=FEET + 86)
    P = 0.9                                             # Arjuna shoots again and again into the shields
    ph = (t - t0) % P
    draw = ease(ph / 0.55) if ph < 0.6 else 0.0
    ax, as_, af = 140, 0.6, FEET + 84
    pts = arjuna(cr, t, ax, as_, bow="aim", aim=-0.04, draw=draw, arrow=ph < 0.6, feet=af, ph=1.0)
    hit = ph >= 0.6
    for i, x in enumerate((390, 540, 690)):
        wob = 0.05 * math.exp(-6 * (ph - 0.75)) * math.sin(30 * (ph - 0.75)) if (ph > 0.75 and i == 0) else 0.0
        soldier(cr, t, x, FEET + 84, 0.5, flip=True, ph=i * 1.3, guard=1.0, rot=wob)
    if hit and "nock" in pts:
        u = (ph - 0.6) / 0.15
        if u < 1:
            nx, ny = pts["nock"]
            arrow_at(cr, nx + (330 - nx) * u, ny, 0.0, 120)
    dev_a = cr.user_to_device(ax + 40, af - 600 * as_)
    dev_j = cr.user_to_device(fx, ff - 140)

    def ui(cr):
        if t < tE:
            head2(cr, t, "ARJUNA FOUGHT", t0 + 0.05, "ALL DAY", tF, big_size=250)
        else:
            head2(cr, t, "EVENING...", tE, "STILL FAR", tR, big_size=250)
        if t > tR - 0.2:
            pts_ = [(dev_a[0] + (dev_j[0] - dev_a[0]) * u, dev_a[1] + (dev_j[1] - dev_a[1]) * u - 160 * math.sin(
                math.pi * u)) for u in (i / 40 for i in range(41))]
            dotted(cr, pts_, prog(t, tR - 0.2, 0.6), 26, 6.0, RED, 0.85)
            tag(cr, t, tR + 0.2, "JAYADRATHA", dev_j[0] - 40, dev_j[1] - 120, 28)
    return dict(ui=ui, eve=0.34 * eve, flash=flash_at(t, tE, 0.2))


# ------------------------------------------------------------------ y9  Krishna hides the sun


def s_hide(cr, t, tl, t0, t1):
    c = cues(tl, "y9")
    tK, tY, tC, tD = c["K"], c["Y"], c["C"], c["D"]
    sx, sy, ss = 790, 840, 0.6
    dark = prog(t, tD - 0.3, 1.0)
    shroud(cr, sx, sy, 250 + 2400 * dark, 0.45 * dark)
    cov = ease((t - tC + 0.3) / 0.6)
    sun_disc(cr, t, sx, sy, ss, cover=cov, red=0.5)
    x, s, feet = 290, 0.86, FEET + 70
    hy = feet - 434 * s
    up = keyed(t, [(t0, 0.0), (tK + 0.2, 1.0)], 0.35, 1.3)
    fr = mix((-0.35, -0.5), point_at(x, hy, s, (sx - 80, sy + 60)), up)
    hx, hyy = x + 30 * s, hy - 410 * s
    glow(cr, hx, hyy, 520, 0.4 + 0.3 * prog(t, tY, 0.5))
    aura(cr, t, hx - 20, hyy - 40, 140, 420, 0.5 * prog(t, tY, 0.5), n=20, spin=0.06)
    krishna(cr, t, x, s, feet=feet, front=fr, backa=(0.3, -0.3), head=-0.12 * up, hits=[(tC, 0.4)], ph=0.4)
    ground(cr, y=FEET + 76)
    dev = cr.user_to_device(sx, sy)

    def ui(cr):
        head2(cr, t, "THEN KRISHNA", t0 + 0.05, "HID THE SUN", tC, big_size=230, under=tD + 0.2)
        tag(cr, t, tY, "YOGA-MAYA", dev[0], dev[1] + 200, 34)
    return dict(ui=ui, night=NIGHT * dark, lift=dark, flash=flash_at(t, tC, 0.3))


# ------------------------------------------------------------------ y10  the key rule: at sunset, the battle stopped


def s_rule(cr, t, tl, t0, t1):
    c = cues(tl, "y10")
    tT, tR, tB, tX = c["T"], c["R"], c["B"], c["X"]
    shroud(cr, 900, 610, 2600, 0.45)
    aura(cr, t, 900, 610, 70, 133, 0.75, n=26, spin=0.08)
    prop(cr, "sun", 900, 610, 0.35, rot=t * 0.2)
    prop(cr, "jd_maya", 900, 610, 0.35, rot=-0.25 * t)
    stop = keyed(t, [(t0, 0.0), (tX, 1.0)], 0.35, 1.3)
    cheering_row(cr, t, 0.0, 1.0 - stop)
    look = prog(t, tT - 0.1, 0.4)
    for x in ((330, 780) if t < tR else ()):
        d = cr.user_to_device(x, 1260)
        draw_text(cr, "?", d[0], d[1] - 40 * look, 90, (1.0, 0.92, 0.7), 0.8 * look * (1 - prog(t, tR - 0.3, 0.3)),
                  anchor="cm")

    def ui(cr):
        if t < tR:
            head2(cr, t, "EVERYONE THOUGHT:", t0 + 0.05, "SUNSET!", tT, big_size=260)
        else:
            head2(cr, t, "THE RULE OF THIS WAR:", tR, "SUNSET = STOP", tR + 0.06, big_size=210, under=tX + 0.2)
            sz = min(fit_size("AT SUNSET, THE DAY'S", 84, 660), fit_size("BATTLE STOPPED", 120, 660))
            card(cr, t, tB - 0.3, 540, 860, 1.0, [("AT SUNSET, THE DAY'S", sz, INK, -46),
                                                   ("BATTLE STOPPED", int(sz * 1.25), RED, 50)])
    return dict(ui=ui, night=NIGHT, lift=1.0, flash=flash_at(t, tR, 0.2))


# ------------------------------------------------------------------ y11  "Arjuna failed! now he must burn!"


def s_cheer(cr, t, tl, t0, t1):
    c = cues(tl, "y11")
    tC, tL, tF = c["C"], c["L"], c["F"]
    shroud(cr, 900, 610, 2600, 0.45)
    aura(cr, t, 900, 610, 70, 133, 0.75, n=26, spin=0.08)
    prop(cr, "sun", 900, 610, 0.35, rot=t * 0.2)
    prop(cr, "jd_maya", 900, 610, 0.35, rot=-0.25 * t)
    pyre(cr, t, 520, FEET - 60, 0.46, fire=0.35 + 0.65 * prog(t, tF, 0.5))
    cheer = prog(t, tC - 0.1, 0.3)
    raise_ = keyed(t, [(t0, 0.2), (tC - 0.05, 1.0)], 0.25, 1.5)
    cheering_row(cr, t, cheer, raise_)

    def ui(cr):
        if t < tF:
            head2(cr, t, "THE KAURAVAS CHEERED:", t0 + 0.05, "ARJUNA FAILED!", tL, big_size=210)
        else:
            head2(cr, t, "ARJUNA FAILED!", tF - 0.3, "NOW HE MUST BURN!", tF, big_size=170, under=tF + 0.4)
        if t > tC:
            for x in (330, 780):
                d = cr.user_to_device(x, 1250)
                sound_rings(cr, d[0], d[1], t, tC, 6, 0.3, 300, alpha=0.5)
    return dict(ui=ui, night=NIGHT, lift=1.0, flash=flash_at(t, tC, 0.2) + flash_at(t, tF, 0.25))


# ------------------------------------------------------------------ y12  he came out to watch Arjuna burn


def s_watch(cr, t, tl, t0, t1):
    c = cues(tl, "y12")
    tJ, tO, tW = c["J"], c["O"], c["W"]
    shroud(cr, 900, 610, 2600, 0.42)
    prop(cr, "jd_maya", 900, 610, 0.35, rot=-0.25 * t)
    px, pf, ps = 150, FEET + 40, 0.45
    pyre(cr, t, px, pf, ps, fire=0.7)
    arjuna(cr, t, 350, 0.46, bow="carry", head=0.18, feet=FEET + 40, ph=1.0)
    part = ease((t - tO + 0.5) / 0.6)
    out_ = clamp((t - tO) / 1.0)
    for i, x in enumerate((540, 700, 860, 1020)):
        soldier(cr, t, x + (1 if x > 780 else -1) * 90 * part, FEET - 40, 0.44, flip=True, ph=i * 1.3, alpha=0.85,
                blur=3.0)
    behind = out_ < 0.5
    look = keyed(t, [(t0, 0.0), (tO + 0.6, -0.05), (tW, 0.05)], 0.4, 1.3)

    def jd(cr_):
        x = 760 - 80 * ease(out_)
        s = 0.48 + 0.16 * ease(out_)
        feet = FEET - 30 + 112 * ease(out_)
        relax = prog(t, tO + 0.6, 0.4)
        jaya(cr_, t, x, s, flip=True, feet=feet, head=look, front=mix((-0.4, -0.5), (0.75, -1.6), relax),
             backa=(0.75, -1.6), ph=0.3, blur=2.0 * (1 - out_) if behind else 0.0, hits=[(tO + 0.5, 0.6)])
        return x, s, feet
    if behind:
        jd(cr)
    ground(cr, y=FEET + 86)
    for i, (x, sc, fl) in enumerate(((610, 0.6, False), (800, 0.6, True), (990, 0.6, True))):
        soldier(cr, t, x + (1 if x > 700 else -1) * (70 if x < 700 else 150) * part, FEET + 84, sc, flip=fl, ph=i * 0.9)
    eye = None
    if not behind:
        jx, js, jf = jd(cr)
        eye = (jx - 40 * js, jf - 434 * js - 410 * js)
    fire_pt = (px, pf - 330 * ps)

    def ui(cr):
        if t < tO:
            head2(cr, t, "NOW JAYADRATHA FELT", t0 + 0.05, "SAFE", tJ + 0.4, big_size=260)
        elif t < tW:
            head2(cr, t, "SO HE CAME", tO, "OUT", tO + 0.06, big_size=260)
        else:
            head2(cr, t, "HE CAME OUT TO WATCH", tW, "ARJUNA BURN", tW + 0.06, big_size=230, under=tW + 0.4)
        if eye is not None and t > tO + 0.8:            # his line of sight to the pyre
            e, f = cr.user_to_device(*eye), cr.user_to_device(*fire_pt)
            pts = [(e[0] + (f[0] - e[0]) * u, e[1] + (f[1] - e[1]) * u) for u in (i / 40 for i in range(41))]
            dotted(cr, pts, prog(t, tO + 0.8, 0.5), 30, 6.0, (1.0, 0.86, 0.5), 0.85)
    return dict(ui=ui, night=NIGHT, lift=1.0, flash=flash_at(t, tO, 0.15))


# ------------------------------------------------------------------ y13  "the sun has not set! there he is!"


THERE = (235, 1790, 0.46)
THERE_SUN = (700, 800, 0.6)
THERE_J = (935, 1790, 0.34)


def s_there(cr, t, tl, t0, t1):
    c = cues(tl, "y13")
    tK, tS, tN, tJ = c["K"], c["S"], c["N"], c["J"]
    sx, sy, ss = THERE_SUN
    shroud(cr, sx, sy, 2600, 0.3)
    sun_disc(cr, t, sx, sy, ss, cover=1.0)
    x, feet, s = THERE
    ground(cr, y=feet + 6)
    jx, jf, js = THERE_J
    jaya(cr, t, jx, js, flip=True, feet=feet, head=0.05, front=(0.75, -1.6), backa=(0.75, -1.6), ph=0.3,
         rods=False)
    deck = feet - J.DECK * s
    kx = x + KR_DX * s
    hy = deck - 434 * s
    to_j = keyed(t, [(t0, 0.0), (tJ - 0.1, 1.0)], 0.3, 1.4)
    fr = mix(point_at(kx, hy, s, (sx - 60, sy + 40)), point_at(kx, hy, s, (jx, jf - 330 * js)), to_j)
    draw = clamp((t - tK) / max(0.4, tJ - tK + 0.6))
    chariot(cr, t, x, feet, s,
            ar=dict(bow="aim", aim=-0.72 + 0.64 * to_j, draw=0.3 + 0.7 * ease(draw), head=-0.06 + 0.06 * to_j, ph=1.0),
            kr=dict(front=fr, backa=(0.35, -0.3), head=-0.14 + 0.14 * to_j, hits=[(tK, 0.4), (tJ, 0.5)], ph=0.4))
    dev = cr.user_to_device(sx, sy)
    dj = cr.user_to_device(jx, jf - 470 * js)

    def ui(cr):
        if t < tJ:
            head2(cr, t, "THE SUN HAS", t0 + 0.05, "NOT SET!", tS, big_size=250, under=tN + 0.1)
            if t > tS:
                red_ring(cr, dev[0], dev[1], 250, 240, prog(t, tS + 0.1, 0.45), 10)
        else:
            head2(cr, t, "THE SUN HAS NOT SET!", t0 + 0.05, "THERE HE IS!", tJ, big_size=230)
            red_ring(cr, dj[0], dj[1], 100, 205, prog(t, tJ + 0.15, 0.45), 9)
        if t > tK:
            kh = cr.user_to_device(kx + 50 * s, hy - 300 * s)
            sound_rings(cr, kh[0], kh[1], t, tK, 3, 0.3, 150, alpha=0.4)
    return dict(ui=ui, night=0.3 * (1 - 0.35 * prog(t, tS, 0.6)), lift=0.8,
                flash=flash_at(t, tS, 0.35) + flash_at(t, tJ, 0.3))


# ------------------------------------------------------------------ y15  Krishna's instruction: not on the ground


JD15 = (520, FEET + 90, 0.36)


def s_instruct(cr, t, tl, t0, t1):
    c = cues(tl, "y15")
    tK, tG, tL = c["K"], c["G"], c["L"]
    shroud(cr, 250, 700, 2600, 0.3)
    prop(cr, "sun", 250, 700, 0.3, rot=t * 0.2)
    prop(cr, "jd_maya", 250, 700, 0.3, rot=-0.25 * t)
    fp = hermitage_far(cr, t, glow_a=0.4 * prog(t, tL, 0.4))
    lap = fp["lap"]
    ground(cr, y=FEET + 96)
    jx, jf, js = JD15
    jaya(cr, t, jx, js, flip=True, feet=jf, head=-0.2, front=(0.75, -1.6), backa=(0.75, -1.6), ph=0.3, rods=False)
    point = keyed(t, [(t0, 0.0), (tK + 0.2, 1.0), (tL - 0.2, 2.0)], 0.35, 1.3)
    x, s, feet = 170, 0.62, FEET + 90
    hy = feet - 434 * s
    t1_ = point_at(x, hy, s, (jx, jf - 40))
    t2_ = point_at(x, hy, s, (lap[0], lap[1] - 300))
    fr = mix((-0.35, -0.5), t1_, clamp(point)) if point <= 1 else mix(t1_, t2_, point - 1)
    krishna(cr, t, x, s, feet=feet, front=fr, backa=(0.3, -0.3), head=-0.04, hits=[(tG, 0.4), (tL, 0.4)], ph=0.4)
    head0 = (jx - 20 * js, jf - 434 * js - 410 * js)
    arc = arc_pts(head0, (lap[0], lap[1] - 22), 720)
    if t > tL - 0.2:
        dotted(cr, arc, prog(t, tL - 0.2, 0.9), 30, 6.5, RED, 0.85)
    dev_x = cr.user_to_device(jx, jf + 10)
    dev_lap = cr.user_to_device(*lap)

    def ui(cr):
        if t < tG:
            head2(cr, t, "SO KRISHNA SAID:", t0 + 0.05, None, 0.0)
        elif t < tL:
            head2(cr, t, "DON'T LET IT TOUCH THE", tG, "GROUND", tG + 0.06, big_size=250)
        else:
            head2(cr, t, "SEND IT TO HIS", tL, "FATHER'S LAP", tL + 0.06, big_size=230, under=tL + 0.5)
            red_ring(cr, dev_lap[0], dev_lap[1] - 10, 90, 70, prog(t, tL + 0.7, 0.4), 8)
        if t > tG:
            big_x(cr, dev_x[0], dev_x[1], 200, 90, prog(t, tG + 0.1, 0.3), lw=18)
        tag(cr, t, tL, "HIS FATHER", min(dev_lap[0], 900), dev_lap[1] + 250, 30)
    return dict(ui=ui, night=0.3, lift=1.0, flash=flash_at(t, tG, 0.2) + flash_at(t, tL, 0.2))


# ------------------------------------------------------------------ y17  he stands; it falls; his own boon


def s_burst(cr, t, tl, t0, t1):
    c = cues(tl, "y17")
    tU, tG, tB = c["U"], c["G"], c["B"]
    tC = min(tG + 0.4, tB - 0.3)
    herm_close(cr, t, tU, tG, tC, tB)
    white = 0.85 * math.exp(-3.2 * max(0.0, t - tB - 0.05)) * clamp((t - tB + 0.05) / 0.08) if t > tB - 0.05 else 0.0

    def ui(cr):
        if t < tG:
            head2(cr, t, "THE FATHER", t0 + 0.05, "STOOD UP", tU, big_size=250)
        elif t < tB:
            head2(cr, t, "IT FELL TO THE", tG, "GROUND", tG + 0.06, big_size=250)
        else:
            head2(cr, t, "HIS OWN BOON", tB, "KILLED HIM", tB + 0.06, big_size=250, under=tB + 0.6)
    return dict(ui=ui, night=0.22, lift=0.6, flash=flash_at(t, tG, 0.25) + flash_at(t, tB, 0.9, 2.5), white=white)


# ------------------------------------------------------------------ y18  the darkness lifts: the sun was still up


def s_sunback(cr, t, tl, t0, t1):
    c = cues(tl, "y18")
    tK, tR, tS = c["K"], c["R"], c["S"]
    lift_ = prog(t, tR - 0.1, 0.9)
    sx, sy, ss = 730, 820, 0.62
    shroud(cr, sx, sy, 2600, 0.42 * (1 - lift_))
    sun_disc(cr, t, sx, sy, ss, cover=1.0 - ease((t - tR + 0.1) / 0.8), glow_a=1.0 + 0.5 * lift_)
    if lift_ > 0:
        aura(cr, t, sx, sy, 140, 330, 0.6 * lift_, n=20)
    cx, cy, rx = 760, 1450, 190
    cs = sun_clock(cr, t, cx, cy, rx, 0.86, t_in=tS - 0.3)
    x, s, feet = 260, 0.86, FEET + 70
    hy = feet - 434 * s
    down = keyed(t, [(t0, 0.0), (tR - 0.1, 1.0)], 0.4, 1.2)
    fr = mix(point_at(x, hy, s, (sx - 80, sy + 60)), (-0.35, -0.5), down)
    glow(cr, x + 30 * s, hy - 410 * s, 480, 0.35)
    krishna(cr, t, x, s, feet=feet, front=fr, backa=(0.3, -0.3), head=-0.1 * (1 - down), hits=[(tR, 0.4)], ph=0.4)
    ground(cr, y=FEET + 76)
    dev_cs = cr.user_to_device(*cs)
    dev_sun = cr.user_to_device(sx, sy)

    def ui(cr):
        if t < tS:
            head2(cr, t, "THEN KRISHNA REMOVED", t0 + 0.05, "THE DARKNESS", tR, big_size=210)
        else:
            head2(cr, t, "THE SUN WAS", tS, "STILL UP", tS + 0.06, big_size=260, under=tS + 0.4)
            red_ring(cr, dev_sun[0], dev_sun[1], 170, 160, prog(t, tS + 0.2, 0.45), 9)
            red_ring(cr, dev_cs[0], dev_cs[1], 46, 42, prog(t, tS + 0.5, 0.35), 6)
    return dict(ui=ui, night=NIGHT * (1 - lift_), lift=1.0 - lift_, flash=flash_at(t, tR, 0.35))


# ------------------------------------------------------------------ y19  clever or cheating?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "y19")
    tC, tX, tM = c["C"], c["X"], c["M"]
    ground(cr, y=FEET + 46)
    glow(cr, 540, 1420, 380, 0.4)
    krishna(cr, t, 540, 0.6, feet=FEET + 40, front=(-0.55, -1.75), backa=(0.25, -0.3), ph=0.5)
    cards = ((290, "CLEVER?", tC), (790, "CHEATING?", tX))

    def ui(cr):
        head2(cr, t, "SO, KRISHNA'S MOVE WAS...", t0 + 0.05, None, 0.0)
        cs = 0.56
        size = min(150, *[int(96 * 370 / text_size(txt, 96)[0] / cs) for _, txt, _ in cards])
        for cx, txt, tc in cards:
            card(cr, t, tc - 0.25, cx, 640, cs, [(txt, size, RED, 4)])
        if t > tC:
            if t < tX:
                k, ts = 0, tC
            else:
                n = int((t - tX) / 0.9)
                k, ts = (1 if n % 2 == 0 else 0), tX + 0.9 * n
            red_ring(cr, cards[k][0], 644, 236, 92, prog(t, ts, 0.35), 9)
        big_q(cr, t, tM, 860, 1180, 220)
    return dict(ui=ui, flash=flash_at(t, tX, 0.2))


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("y1", None, s_hook, {"z": (1.0, 1.04)}),
    ("y2", None, s_book, {"z": (1.0, 1.03)}),
    ("y3", None, s_who, {"z": (1.0, 1.03)}),
    ("y4", None, s_vyuha, {"z": (1.0, 1.03)}),
    ("y5", None, s_vow, {}),
    ("y6", None, s_plan, {"z": (1.0, 1.03)}),
    ("y7", None, s_hidden, {"z": (1.0, 1.03)}),
    ("y8", None, s_far, {}),
    ("y9", None, s_hide, {"z": (1.0, 1.05)}),
    ("y10", None, s_rule, {"z": (1.0, 1.03)}),
    ("y11", None, s_cheer, {"z": (1.0, 1.04)}),
    ("y12", None, s_watch, {"z": (1.0, 1.04)}),
    ("y13", None, s_there, {"z": (1.02, 1.06)}),
    ("y14", None, s_shield, {"z": (1.0, 1.03)}),
    ("y15", None, s_instruct, {"z": (1.0, 1.02)}),
    ("y16", None, s_arrow, {"z": (1.0, 1.02)}),
    ("y17", None, s_burst, {"z": (1.02, 1.07)}),
    ("y18", None, s_sunback, {"z": (1.0, 1.04)}),
    ("y19", None, s_end, {"z": (1.0, 1.03)}),
]


def title_lift(cr, a):
    """In the dark shots, the small lamp over the title stays lit so the headline reads."""
    if a <= 0.01:
        return
    g = cairo.RadialGradient(540, 420, 60, 540, 420, 620)
    g.add_color_stop_rgba(0, 1.0, 0.93, 0.76, 0.5 * a)
    g.add_color_stop_rgba(0.6, 1.0, 0.90, 0.70, 0.28 * a)
    g.add_color_stop_rgba(1, 1.0, 0.88, 0.66, 0.0)
    cr.save()
    cr.set_source(g)
    cr.paint()
    cr.restore()


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
    if out.get("white", 0.0) > 0.01:
        cr.set_source_rgba(1.0, 0.98, 0.93, clamp(out["white"]))
        cr.paint()
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)




def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a conch
    on Arjuna's vow, a conch as Krishna hides the sun, a single hit when the head falls to the ground, a bell on the
    closing question, then (only where they fit) a damaru on "the sun has not set!", shimmer as the sun comes back and
    on the burst of light. Chosen in THAT order of importance, each at least SFX_MIN_GAP from every sound already kept
    (as render_myth.calm_sfx keeps them), so the list returned is what plays; the bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["y5"]["V"], "conch", 0), (c["y9"]["C"], "conch", 0), (c["y17"]["G"], "hit", 0),
            (c["y19"]["C"], "bell", 0), (c["y13"]["N"], "damaru", 0), (c["y18"]["S"], "shimmer", 0),
            (c["y17"]["B"], "shimmer", 0), (c["y10"]["X"], "damaru", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["y9"]["t0"] - 0.3, "dip", 0.5), (c["y13"]["t0"] - 0.3, "dip", 0.5), (c["y17"]["B"] - 0.35, "dip", 0.5)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
