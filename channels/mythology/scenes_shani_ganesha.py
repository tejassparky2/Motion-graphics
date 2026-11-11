"""Scenes for videos/shani_ganesha.py: "Ganesha's head fell to one look from Shani Dev" (Brahma Vaivarta Purana,
Ganapati Khanda), in Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit
screen, two-tier headlines and rod-puppet motion as the Jarasandha, Kaikeyi, Lakshman Rekha, Mandhata, Jayadratha,
Arjuna, Ruru and Dharmavyadha reels, with the cast from shani_cast. A myth-bust told so a child can follow: one plain
label per step, and the same few things come back (Shani's lowered eyes as a dotted line to the ground, the curse card,
the cradle) so every shot reads at once.

Respect: every deity with dignity and beauty. Shani is calm and sad, his eyes always lowered; he warns first and looks
only because he is pressed. Parvati's insistence is a mother's pride, never foolishness; she faints from grief and her
anger is a mother's. No gore at all: the head is never drawn; at the glance a white flash fills the screen and the head
goes up as a ball of light while the cradle shows only its cloth; the elephant simply fades into golden light at the
Sudarshana chakra's flash; Ganesha rises from the cradle glowing, with the elephant head.

Every frame is a pure function of t. English on-screen text only (shared by Hindi and Kannada). Cues are words of the
line in each language ({"hi": ..., "kn": ...}) with a fraction fallback, kept in one table (CUES) that the scenes and
sfx() both read, with minimum gaps so a fast voice can't bunch the beats together.

Shot list (line: what is on the screen)
  s1  HOOK, frame 0: Shani Dev alone and large, his crow on his staff, his eye glancing sideways from its lowered lid
      and glowing faintly: GANESHA'S HEAD WASN'T CUT BY SHIVA / IT WAS SHANI'S LOOK (big words in by 0.3 s); on
      "Shiva" a small trident drops in and is crossed out; on "look" his eye flares and a thin line of light glances
      sideways; on "fell" the big line is underlined and the crow flaps
  s2  THIS IS NOT A / FILM STORY (crossed out); a palm-leaf book rises and opens: BRAHMA VAIVARTA PURANA, PART 3:
      GANAPATI KHANDA (ringed); IT'S WRITTEN IN A / PURANA
  s3  two parchment panels: SHIVA PURANA (Shiva's silhouette with his trident, THE TRIDENT, ticked) and BRAHMA
      VAIVARTA (a big "?", then SHANI'S LOOK): WE ALL HEARD: / SHIVA'S TRIDENT, then SAME GANESHA, / TWO DIFFERENT
      STORIES
  s4  Shani seated cross-legged on a lotus, eyes shut, his crow beside him (tag SHANI DEV): FIRST, KNOW / SHANI'S
      SECRET; light gathers round him: ONE DAY, DEEP IN / MEDITATION
  s5  his wife walks in smiling (tags HIS WIFE / A GANDHARVA PRINCESS) and waits while a sun crosses the day: HIS
      WIFE CAME TO HIM, / SMILING; his shut eye is ringed, a dotted line from it to her is crossed out: BUT HE DIDN'T
      EVEN / LOOK
  s6  she grows angry and points; a crackling line of light from her finger: SHE BECAME VERY / ANGRY, then AND SHE
      CURSED HIM: with the card WHOEVER YOU LOOK AT / WILL LOSE HIS HEAD; his eyes open, lowered
  s7  Shani walks in, eyes lowered, a red dotted line from his eye to the ground, days passing (a sun crossing again
      and again): FROM THAT DAY ON: / EYES ALWAYS DOWN
  s8  Kailash: the court with its toran, the snow peaks behind; the cradle with the sweet baby, glowing; flowers fall:
      THEN GANESHA WAS / BORN; the devas come in with garlands: ALL THE DEVAS CAME TO / BLESS HIM; Shani at the back,
      eyes down (tag SHANI DEV): AND SHANI DEV / CAME TOO
  s9  Shani, the cradle, Parvati (tag PARVATI); his lowered sight-line ringed: BUT SHANI DIDN'T LOOK AT / THE BABY;
      PARVATI ASKED: with the cloud WHY WON'T YOU LOOK / AT MY SON?
  s10 Shani explains, the curse card shown small: HE TOLD HER ABOUT / THE CURSE; Parvati laughs (HA!): BUT SHE /
      LAUGHED IT OFF; she presents her son with a mother's pride: AND SHE INSISTED: / LOOK AT MY SON!
  s11 close on Shani's face, trembling: FEARFULLY, FROM THE / CORNER OF HIS EYE; his eye turns to its corner and glows,
      a thin line of light goes to the baby: JUST ONCE: / ONE GLANCE
  s12 the cradle, the line of light still on it, the lamp dims: AND IN THAT VERY / MOMENT...; a white flash fills the
      screen; only the cradle cloth is left and a ball of light flies up: IN A FLASH OF LIGHT, / THE HEAD FELL
  s13 Parvati faints into a dark-red glow: PARVATI / FAINTED; the devas hold their heads: AND ALL AROUND: / CHAOS
  s14 moonlit night: Vishnu on Garuda flies across the stars, a dotted trail and a NORTH tag (tag VISHNU): THEN
      VISHNU, ON GARUDA, / FLEW NORTH; below, an elephant asleep under the moon (zzz): THERE, AN ELEPHANT WAS /
      SLEEPING
  s15 Vishnu raises the Sudarshana chakra, a golden flash, the elephant fades into light and a golden light rises:
      WITH THE / SUDARSHANA CHAKRA; back on Kailash the light comes down into the cradle: AN ELEPHANT'S HEAD FOR /
      GANESHA; Ganesha rises glowing with the elephant head, flowers fall, the devas raise their hands: AND /
      GANESHA LIVED AGAIN!
  s16 Parvati, angry, points at Shani (eyes down), a crackling line of light: BUT PARVATI WAS STILL / ANGRY; SHE
      CURSED SHANI: with the card BECOME / LIMBLESS!
  s17 the devas plead with folded hands: THE DEVAS / PLEADED; the card is crossed out and changes to LAME / FOREVER:
      SO THE CURSE WAS / SOFTENED; Shani turns and limps away on his staff: AND THAT'S / WHY SHANI DEV LIMPS
  s18 Shani small and calm, his crow on his staff: SHANI DEV / HAD WARNED THEM; HIS PUNISHMENT WAS... and cards FAIR? /
      UNFAIR?, a red ring alternating
"""
import math

import cairo

import mandhata_cast as M
import puppet_core as pc
import shani_cast as S
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, text_size, tick
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_arjuna import card2, cloud_text, down_arrow, ha
from scenes_dharmavyadha import eye_of, point_to, sitter, sun_arc, tears
from scenes_jarasandha import FADE, FEET, INK, RED, bob_rot, glow, man_angles, motes, red_ring, stars, woman_angles
from scenes_jayadratha import NIGHT, flash_at, silhouette, tag, tint, title_lift, to_user
from scenes_kaikeyi import ANJALI, card, fig
from scenes_lakshman_rekha import big_x, book, sparkle
from scenes_mandhata import aura, burst, held, lights, local, mix, reach_arm, warm, zzz
from scenes_ravana import dotted, head2
from scenes_ruru import held_grip, petals, plate, sepia
from shots import T, shot_at

MISSES = set()                       # cue words not found in a line (falls back to fractions)
G = FEET + 120                       # the ground line of most sets
SIGHT = (0.70, 0.86, 1.0)            # the colour of Shani's glance (cool light)


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
    "s1": (("S", {"hi": "शिव", "kn": "ಶಿವ"}, 0.3, (("t0", 0.9),)),
           ("N", {"hi": "शनि", "kn": "ಶನಿ"}, 0.55, (("S", 0.8),)),
           ("L", {"hi": "एक", "kn": "ನೋಟಕ್ಕೆ"}, 0.75, (("N", 0.4),)),
           ("F", {"hi": "गिर", "kn": "ಬಿತ್ತು"}, 0.9, (("L", 0.4),))),
    "s2": (("X", {"hi": "नहीं", "kn": "ಅಲ್ಲ"}, 0.3, (("t0", 0.6),)),
           ("M", {"hi": "ब्रह्मवैवर्त", "kn": "ಬ್ರಹ್ಮವೈವರ್ತ"}, 0.55, (("X", 0.5),)),
           ("P", {"hi": "लिखा", "kn": "ಇದೆ"}, 0.85, (("M", 0.6),))),
    "s3": (("Sh", {"hi": "शिव", "kn": "ಶಿವ"}, 0.15, (("t0", 0.5),)),
           ("T", {"hi": "त्रिशूल", "kn": "ತ್ರಿಶೂಲದಿಂದ"}, 0.3, (("Sh", 0.8),)),
           ("SP", {"hi": "पुराण", "kn": "ಪುರಾಣದ"}, 0.5, (("T", 0.7),)),
           ("P", {"hi": "पर", "kn": "ಆದ್ರೆ"}, 0.68, (("SP", 0.6),)),
           ("D", {"hi": "अलग", "kn": "ಬೇರೆನೇ"}, 0.9, (("P", 0.6),))),
    "s4": (("S", {"hi": "राज़", "kn": "ರಹಸ್ಯ"}, 0.3, (("t0", 0.5),)),
           ("M", {"hi": "ध्यान", "kn": "ಧ್ಯಾನದಲ್ಲಿ"}, 0.75, (("S", 1.0),))),
    "s5": (("W", {"hi": "पत्नी", "kn": "ಹೆಂಡತಿ"}, 0.1, (("t0", 0.2),)),
           ("A", {"hi": "आईं", "kn": "ಬಂದ್ರು"}, 0.35, (("W", 0.6),)),
           ("L", {"hi": "देखा", "kn": "ನೋಡಲೇ"}, 0.82, (("A", 1.0),)),
           ("N", {"hi": "नहीं", "kn": "ಇಲ್ಲ"}, 0.92, (("L", 0.3),))),
    "s6": (("A", {"hi": "बहुत", "kn": "ಕೋಪ"}, 0.15, (("t0", 0.3),)),
           ("C", {"hi": "श्राप", "kn": "ಶಾಪ"}, 0.35, (("A", 0.8),)),
           ("L", {"hi": "देखोगे", "kn": "ನೋಡ್ತೀರೋ"}, 0.65, (("C", 0.7),)),
           ("H", {"hi": "सिर", "kn": "ತಲೆ"}, 0.82, (("L", 0.5),))),
    "s7": (("A", {"hi": "हमेशा", "kn": "ಯಾವಾಗಲೂ"}, 0.4, (("t0", 0.6),)),
           ("D", {"hi": "नीचे", "kn": "ಕೆಳಗೆ"}, 0.75, (("A", 0.5),))),
    "s8": (("B", {"hi": "जन्म", "kn": "ಜನನ"}, 0.2, (("t0", 0.4),)),
           ("D", {"hi": "देवता", "kn": "ದೇವತೆಗಳು"}, 0.4, (("B", 0.8),)),
           ("Bl", {"hi": "आशीर्वाद", "kn": "ಆಶೀರ್ವಾದ"}, 0.6, (("D", 0.5),)),
           ("S", {"hi": "भी", "kn": "ದೇವರೂ"}, 0.9, (("Bl", 0.8),))),
    "s9": (("N", {"hi": "नहीं", "kn": "ಇಲ್ಲ"}, 0.4, (("t0", 0.8),)),
           ("P", {"hi": "पार्वती", "kn": "ಪಾರ್ವತಿ"}, 0.5, (("N", 0.4),)),
           ("Q", {"hi": "क्यों", "kn": "ಯಾಕೆ"}, 0.8, (("P", 0.7),))),
    "s10": (("C", {"hi": "श्राप", "kn": "ಶಾಪದ"}, 0.15, (("t0", 0.3),)),
            ("L", {"hi": "हँसी", "kn": "ತಮಾಷೆ"}, 0.5, (("C", 0.9),)),
            ("I", {"hi": "ज़िद", "kn": "ಹಠ"}, 0.75, (("L", 0.6),)),
            ("S", {"hi": "देखिए", "kn": "ನೋಡಿ"}, 0.92, (("I", 0.4),))),
    "s11": (("F", {"hi": "डरते", "kn": "ಹೆದರ್ತಾ"}, 0.2, (("t0", 0.3),)),
            ("C", {"hi": "कोने", "kn": "ಕಣ್ಣಂಚಿನಿಂದ"}, 0.45, (("F", 0.6),)),
            ("L", {"hi": "देखा", "kn": "ನೋಡಿದ್ರು"}, 0.88, (("C", 0.8),))),
    "s12": (("M", {"hi": "उसी", "kn": "ಅದೇ"}, 0.15, (("t0", 0.2),)),
            ("H", {"hi": "सिर", "kn": "ತಲೆ"}, 0.55, (("M", 0.8),)),
            ("A", {"hi": "अलग", "kn": "ಬೇರೆ"}, 0.8, (("H", 0.5),))),
    "s13": (("F", {"hi": "बेहोश", "kn": "ಮೂರ್ಛೆ"}, 0.3, (("t0", 0.4),)),
            ("C", {"hi": "हाहाकार", "kn": "ಹಾಹಾಕಾರ"}, 0.75, (("F", 0.9),))),
    "s14": (("V", {"hi": "विष्णु", "kn": "ವಿಷ್ಣು"}, 0.08, ()),
            ("N", {"hi": "उत्तर", "kn": "ಉತ್ತರ"}, 0.45, (("V", 1.0),)),
            ("E", {"hi": "हाथी", "kn": "ಆನೆ"}, 0.8, (("N", 0.9),))),
    "s15": (("C", {"hi": "सुदर्शन", "kn": "ಸುದರ್ಶನ"}, 0.03, (("t0", 0.1),)),
            ("J", {"hi": "लगा", "kn": "ಜೋಡಿಸಿದ"}, 0.6, (("C", 2.0),)),
            ("L", {"hi": "फिर", "kn": "ಮತ್ತೆ"}, 0.88, (("J", 1.0),))),
    "s16": (("A", {"hi": "शांत", "kn": "ಕೋಪ"}, 0.25, (("t0", 0.4),)),
            ("C", {"hi": "श्राप", "kn": "ಶಾಪ"}, 0.6, (("A", 0.8),)),
            ("L", {"hi": "अपंग", "kn": "ಅಂಗಹೀನರಾಗಿ"}, 0.85, (("C", 0.5),))),
    "s17": (("P", {"hi": "मनाने", "kn": "ಬೇಡಿಕೊಂಡ"}, 0.1, (("t0", 0.3),)),
            ("S", {"hi": "हल्का", "kn": "ಕಡಿಮೆ"}, 0.35, (("P", 0.9),)),
            ("W", {"hi": "इसीलिए", "kn": "ಅದಕ್ಕೇ"}, 0.55, (("S", 0.8),)),
            ("L", {"hi": "लंगड़ाकर", "kn": "ಕುಂಟುತ್ತಾ"}, 0.85, (("W", 0.6),))),
    "s18": (("W", {"hi": "मना", "kn": "ಬೇಡ"}, 0.25, (("t0", 0.4),)),
            ("Q", {"hi": "सही", "kn": "ಸರಿನಾ"}, 0.6, (("W", 0.8),)),
            ("Y", {"hi": "हाँ", "kn": "ಹೌದಾ"}, 0.75, (("Q", 0.4),)),
            ("C", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.88, (("Y", 0.5),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_sg_cues", None)
    if cache is None:
        cache = {}
        tl._sg_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, words, frac, cons in CUES[bid]:
            v = cue(tl, bid, words, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


# ------------------------------------------------------------------ light


def ground(cr, y=G, alpha=1.0):
    prop(cr, "ground", W / 2, y + 6, 0.82, alpha=alpha)


def sightline(cr, p0, p1, a, reach=1.0, w=1.0):
    """Shani's glance: a thin line of cool light from his eye toward p1 (reach < 1 stops short)."""
    if a <= 0.01:
        return
    ex, ey = p0[0] + (p1[0] - p0[0]) * reach, p0[1] + (p1[1] - p0[1]) * reach
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, col, k in ((16 * w, (0.20, 0.36, 0.80), 0.35), (6 * w, (0.40, 0.60, 1.0), 0.8)):
        cr.move_to(*p0)
        cr.line_to(ex, ey)
        cr.set_source_rgba(*col, k * clamp(a))
        cr.set_line_width(lw)
        cr.stroke()
    cr.set_operator(cairo.OPERATOR_ADD)
    for lw, col, k in ((34 * w, (0.45, 0.65, 1.0), 0.16), (2.5 * w, (0.92, 0.97, 1.0), 0.95)):
        cr.move_to(*p0)
        cr.line_to(ex, ey)
        cr.set_source_rgba(*col, k * clamp(a))
        cr.set_line_width(lw)
        cr.stroke()
    cr.restore()
    if reach >= 0.98:
        sparkle(cr, ex, ey, 44 * w * a, a, SIGHT)


def eye_glow(cr, eye, a, r=1.0):
    """A faint glow in Shani's eye."""
    if a <= 0.01:
        return
    glow(cr, eye[0], eye[1], 120 * r, 0.6 * a)
    sparkle(cr, eye[0] + 4, eye[1], 30 * r * a, a, SIGHT)


def light_ball(cr, x, y, r, a, t=0.0):
    """A ball of light (the head going up, the life coming back): golden rays turning round it, a gold ring, a white
    core and a glint, so it reads on the bright middle of the cloth too."""
    if a <= 0.01:
        return
    glow(cr, x, y, r * 4.0, 0.8 * a)
    warm(cr, x, y, r * 3.0, 0.9 * a)
    aura(cr, t, x, y, r * 0.9, r * 2.6, 0.9 * a, n=14, spin=0.8)
    cr.save()
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 1.0, 1.0, 0.97, a)
    g.add_color_stop_rgba(0.65, 1.0, 0.94, 0.70, 0.95 * a)
    g.add_color_stop_rgba(1, 1.0, 0.74, 0.22, 0.9 * a)
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill_preserve()
    cr.set_source_rgba(0.80, 0.42, 0.06, 0.8 * a)
    cr.set_line_width(max(2.0, r * 0.07))
    cr.stroke()
    cr.restore()
    sparkle(cr, x, y, r * 1.6, a, (1.0, 0.95, 0.80))


def bolt(cr, t, t_in, p0, p1, dur=0.9, col=(1.0, 0.45, 0.15), seed=0):
    """A curse: a crackling, jagged line of light from p0 (a pointing finger) to p1, flickering, then gone."""
    u = t - t_in
    if not 0 <= u < dur:
        return
    a = (1 - u / dur) * (0.75 + 0.25 * math.sin(t * 40 + seed))
    reach = clamp(u / 0.18)
    n = 9
    pts = [p0]
    for i in range(1, n):
        f = i / n * reach
        j = 22 * math.sin(i * 2.7 + int(t * 18) * 1.3 + seed)
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L_ = math.hypot(dx, dy) or 1
        pts.append((p0[0] + dx * f - dy / L_ * j, p0[1] + dy * f + dx / L_ * j))
    pts.append((p0[0] + (p1[0] - p0[0]) * reach, p0[1] + (p1[1] - p0[1]) * reach))
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, c, k in ((16, col, 0.35), (6, col, 0.9)):
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
        cr.set_source_rgba(*c, k * a)
        cr.set_line_width(lw)
        cr.stroke()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.set_source_rgba(1.0, 0.95, 0.8, 0.9 * a)
    cr.set_line_width(2.5)
    cr.stroke()
    cr.restore()
    for i in range(4):
        sparkle(cr, p0[0] + 30 * math.cos(i * 1.6 + t * 9), p0[1] + 30 * math.sin(i * 1.6 + t * 9), 26 * a, a,
                (1.0, 0.7, 0.3))
    if reach >= 1:
        sparkle(cr, p1[0], p1[1], 60 * a, a, (1.0, 0.8, 0.4))


def red_glow(cr, x, y, r, a):
    """The dark-red glow of grief (and of anger)."""
    if a <= 0.01:
        return
    tint(cr, (1.0, 0.55, 0.50), 0.55 * a)
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 0.85, 0.10, 0.06, 0.38 * a)
    g.add_color_stop_rgba(1, 0.55, 0.04, 0.02, 0.0)
    cr.save()
    cr.set_source(g)
    cr.paint()
    cr.restore()


# ------------------------------------------------------------------ puppets


STAFF_S = 0.74                        # Shani's staff in his hand (arm units): a cane from the ground to his chest
STAFF_GRIP = -112.0
CROW_S = 0.44                         # the crow on the staff, relative to Shani's scale
SH_BACK = (-0.15, -0.35)              # his back hand a little forward, holding the staff upright
SH_MOOD = {m: "sg_shani_head" + ("" if m == "down" else "_" + m) for m in S.SH_MOODS}


def crow(cr, t, x, y, s, flip=False, flap=0.0, alpha=1.0, blur=0.0, ph=0.0):
    """The crow (feet at x, y): perched, bobbing its head now and then; flap 0..1 opens its wings."""
    if alpha <= 0.01:
        return
    bob = 0.06 * max(0.0, math.sin(t * 2.1 + ph)) ** 6
    name = "sg_crow_fly" if flap > 0.5 else "sg_crow"
    prop(cr, name, x, y - 10 * flap * s, s, rot=(bob + 0.04 * math.sin(t * 9) * flap) * (-1 if flip else 1),
         alpha=alpha, blur=blur, flip=flip)


def shani(cr, t, x, s, mood="down", staff=True, crow_on=False, flap=0.0, backa=SH_BACK, tilt=0.0, **kw):
    """Shani Dev standing (feet on `feet`), his iron staff upright in his back hand (crow_on perches his crow on its
    top; mostly the crow stands on the ground beside him instead, clear of his face)."""
    store = {}
    ex = dict(kw.pop("extra", None) or {})
    a, b = kw.get("alpha", 1.0), kw.get("blur", 0.0)
    if staff:
        ex["sg_shani_armB_lo"] = held_grip("sg_staff", backa, STAFF_S, tilt, STAFF_GRIP, a, b, store)
    kw.setdefault("feet", G)
    pts = fig(cr, S.SHANI, "sg_shani", t, x, s, backa=backa, swap={"sg_shani_head": SH_MOOD[mood]}, extra=ex, **kw)
    if staff and crow_on and "top" in store:
        tx, ty = to_user(cr, store["top"])
        crow(cr, t, tx, ty + 8 * s, CROW_S * s, flip=kw.get("flip", False), flap=flap, alpha=a, blur=b)
    if "bottom" in store:
        pts["staff_bottom"] = to_user(cr, store["bottom"])
    return pts


def shani_sit(cr, t, x, ground_, s, mood="shut", **kw):
    return sitter(cr, S.SHANI, "sg_shani", t, x, ground_, s, seat="sg_shani_seat", head_sprite=SH_MOOD[mood], **kw)


MED = dict(front=(-0.1, -1.05), backa=(0.0, -1.0))              # in meditation: the hands resting on his knees


def shani_limp(cr, t, t0, t1, x0, x1, s, feet=G, mood="sad", **kw):
    """Shani walking with a limp: the near leg swings, the far one drags stiffly; he dips onto his staff at every
    other step."""
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step=0.62)
    lame = ph < 0
    legs = (0.34 * ph, -0.06 * ph) if not lame else (0.05 * ph, 0.12 * ph)
    dip = 18 * abs(ph) * lame
    y = feet - 434 * s + bob * 0.5 + dip * s / 0.7
    return shani(cr, t, x, s, mood=mood, legs=legs, rot=rock * 1.6 + 0.03 * lame, y=y, tilt=-0.12 * abs(ph), **kw)


def shani_walk(cr, t, t0, t1, x0, x1, s, feet=G, mood="down", t_in=None, **kw):
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, 0.45)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    y = feet - 434 * s + bob - (k - 1) * 300 * s
    kw.setdefault("hits", [(t1, 1.0)])
    return shani(cr, t, x, s * k, mood=mood, legs=(0.32 * ph, -0.32 * ph), rot=rock, y=y, alpha=a, blur=b, **kw)


def lady(cr, rig, key, t, x, s, mood="open", feet=G, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(),
         flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.4, y=None, lie=0.0, lie_dir=-1):
    """The wife or Parvati standing (feet on `feet`), or lying (lie 1: turned about her hip, which comes down to just
    above the ground, the head toward lie_dir)."""
    q = clamp(lie)
    th = lie_dir * math.pi / 2 * q
    hy = (feet - 470 * s if y is None else y) + (360 * s + 4) * q
    ang = woman_angles(key, t, front, backa, head, hits, ph)
    swap = {key + "_head": key + "_head" + ("" if mood == "open" else "_" + mood)}
    return puppet(cr, rig, x, hy, s, th + rot + bob_rot(t, ph) * (1 - q), flip, ang, alpha, blur, swap=swap,
                  rods=rods)


def wife(cr, t, x, s, mood="open", **kw):
    return lady(cr, S.WIFE, "sg_wife", t, x, s, mood, **kw)


def parvati(cr, t, x, s, mood="open", **kw):
    return lady(cr, S.PARVATI, "sg_parvati", t, x, s, mood, **kw)


def glide(cr, t, fn, t0, t1, x0, x1, s, feet=G, t_in=None, **kw):
    """A woman puppet carried across the cloth in rod-puppet steps (she has no legs: only bob and rock)."""
    x, bob, rock, _ = hop_walk(t, t0, t1, x0, x1, 0.45)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    kw.setdefault("hits", [(t1, 1.0)])
    return fn(cr, t, x, s * k, y=feet - 470 * s + bob * 0.6 - (k - 1) * 300 * s, rot=rock * 0.6, alpha=a, blur=b,
              **kw)


def woman_point(x, s, target, feet=G, flip=False):
    """front=(upper, fore) for a woman's straight front arm pointing at target."""
    return point_to(x, feet - 470 * s, s, target, flip=flip, bulk=22 / 26)


BS = 0.6                              # the baby's scale relative to the cradle's


def cradle(cr, t, x, ground_, s, mode="hu", glow_a=0.0, rise=0.0, arms=(0.0, 0.0), eyes="open", alpha=1.0,
           blur=0.0, hits=(), rock=True):
    """The cradle (back, the baby or its cloth, front). mode: hu (the sweet baby) | el (Ganesha with the elephant
    head) | cloth (only the cradle cloth) | empty. rise 0..1 lifts the baby up out of it (sitting up, glowing).
    Returns the baby's points (device) or {} and the head centre (scene)."""
    r = 0.025 * math.sin(t * 1.5) if rock else 0.0
    rim = ground_ + S.CRADLE_RIM * s
    bs = BS * s
    hip = rim + (96 - 230 * ease(clamp(rise))) * bs
    head_c = local(x, hip, bs, 0.0, False, 0, -440 if mode == "hu" else -470)
    if glow_a > 0 and mode in ("hu", "el"):
        glow(cr, head_c[0], head_c[1] + 60 * bs, 620 * bs + 60, glow_a * (0.88 + 0.12 * math.sin(t * 3.3)))
        aura(cr, t, head_c[0], head_c[1], 220 * bs, 720 * bs, 0.9 * glow_a * alpha)
        warm(cr, head_c[0], head_c[1], 520 * bs, 0.7 * glow_a * alpha)
    cr.save()
    cr.translate(x, ground_)
    cr.rotate(r)
    cr.translate(-x, -ground_)
    prop(cr, "sg_cradle_back", x, ground_, s, alpha=alpha, blur=blur)
    pts = {}
    if mode in ("hu", "el"):
        d = pc.dangle(t, hits, 0.3, 1.6, 2.4)
        ang = {"mb_armL": arms[0] + d, "mb_armR": -arms[1] - d}
        swap = {"mb_body": "sg_baby_hu" if mode == "hu" else "sg_baby_el"}
        hide = ("mb_legL", "mb_legR")
        if mode == "el":
            hide += ("mb_eyes",)
        elif eyes != "open":
            swap["mb_eyes"] = "mb_eyes_" + eyes
        cr.save()
        cr.rectangle(-500, -500, W + 1000, rim + 8 * s + 500)
        cr.clip()
        pts = puppet(cr, M.BABY, x, hip, bs, bob_rot(t, x * 0.01, 0.01), False, ang, alpha, blur, swap=swap, hide=hide,
                     rods=False)
        cr.restore()
    elif mode == "cloth":
        prop(cr, "sg_cloth", x, rim + 6 * s, s, alpha=alpha, blur=blur)
    prop(cr, "sg_cradle", x, ground_, s, alpha=alpha, blur=blur)
    cr.restore()
    pc.rod(cr, x + 200 * s, ground_ - 60 * s, x + 260 * s, H + 60, alpha=0.4 * alpha)
    return pts, head_c


VS = 0.6                              # Vishnu's scale relative to Garuda's
V_F2 = (-2.55, -0.35)                 # his raised front hand (the chakra)
V_B2 = (2.65, 0.45)                   # his raised back hand (the conch)


def garuda(cr, t, x, y, s, flap=1.0, alpha=1.0, blur=0.0, rot=0.0, chakra=0.0, hits=(), front=(-1.2, -0.7),
           chakra_on=True):
    """Garuda in flight (body centre at x, y) with Vishnu seated on his back, four-armed: the chakra raised in one
    hand (chakra 0..1 makes it blaze and grow), the conch in another. Returns (Vishnu's points, chakra centre)."""
    if alpha <= 0.01:
        return {}, (x, y)
    f = math.sin(t * 5.0)
    sh = local(x, y, s, rot, False, *S.GA_SHOULDER)
    prop(cr, "sg_gwing_far", sh[0] + 20 * s, sh[1] - 6 * s, s, rot=rot + 0.12 + 0.3 * f * flap, alpha=alpha,
         blur=blur + 1.5)
    prop(cr, "sg_garuda", x, y, s, rot=rot, alpha=alpha, blur=blur)
    prop(cr, "sg_gwing", sh[0], sh[1], s, rot=rot - 0.3 + 0.36 * f * flap, alpha=alpha, blur=blur)
    vs = VS * s
    vx, vy = local(x, y, s, rot, False, *S.GA_SEAT)
    prop(cr, "sg_vishnu_seat", vx, vy, vs, rot=rot, alpha=alpha, blur=blur)
    ang = man_angles("sg_vishnu", t, front, (0.5, -0.8), 0.0, (0.0, 0.0), hits, 0.7)
    ang["sg_vishnu_armF2_up"] = V_F2[0] + 0.32 + 0.04 * math.sin(t * 1.3)
    ang["sg_vishnu_armF2_lo"] = V_F2[1] + 0.55
    ang["sg_vishnu_armB2_up"] = V_B2[0] - 0.30
    ang["sg_vishnu_armB2_lo"] = V_B2[1] + 0.25
    ex = {"sg_vishnu_armB2_lo": held("sg_conch", V_B2, 0.55, dy=176, alpha=alpha, blur=blur)}
    pts = puppet(cr, S.VISHNU, vx, vy, vs, rot + bob_rot(t, 0.7, 0.008), False, ang, alpha, blur,
                 hide=("sg_vishnu_legF", "sg_vishnu_legB"), rods=False, extra=ex)
    hx, hy = to_user(cr, pts["handF2"])
    cx, cy = hx + 6 * vs, hy - 150 * vs * (1 + 0.6 * chakra)
    if chakra > 0 and chakra_on:
        glow(cr, cx, cy, 300 * vs * (1 + chakra), 0.9 * chakra * alpha)
        aura(cr, t, cx, cy, 120 * vs, 420 * vs * (1 + chakra), chakra * alpha, n=16, spin=0.6)
    if chakra_on:
        prop(cr, "sg_chakra", cx, cy, 0.55 * vs * (1 + 0.8 * chakra), rot=t * (2.0 + 6 * chakra), alpha=alpha)
    pc.rod(cr, x - 40 * s, y + 60 * s, x + 10, H + 60, alpha=0.5 * alpha, blur=blur)
    pc.rod(cr, vx, vy - 200 * vs, vx + 60, H + 60, alpha=0.35 * alpha, blur=blur)
    return pts, (cx, cy)


DEVA_POSE = {"stand": ((-0.32, -0.55), (0.3, -0.25)), "garland": ((-1.3, -0.3), (0.2, -0.4)),
             "plead": (ANJALI["front"], ANJALI["backa"]), "cheer": ((-2.75, -0.35), (-2.6, -0.45))}


def deva(cr, t, x, s, pose="stand", feet=G, flip=False, alpha=1.0, blur=0.0, ph=0.0, garland=False, shake=0.0,
         bow=0.0, y=None, legs=(0.0, 0.0), rot=0.0):
    """A deva: a dark silhouette with a halo of light (a gold ring and a glow); pose stand | garland | plead | cheer |
    head (both hands on his head, in dismay); garland adds a bright marigold garland in his front hand."""
    if alpha <= 0.01:
        return {}
    hy = feet - 434 * s if y is None else y
    hc = local(x, hy, s, rot, flip, 16, -420)
    glow(cr, hc[0], hc[1], 200 * s + 30, 0.55 * alpha)
    cr.save()
    cr.set_source_rgba(1.0, 0.78, 0.30, 0.85 * alpha)
    cr.set_line_width(max(3.0, 9 * s))
    cr.arc(hc[0] - (14 if not flip else -14) * s, hc[1] - 30 * s, 150 * s, 0, 2 * math.pi)
    cr.stroke()
    cr.restore()
    if pose == "head":
        sg = -1 if flip else 1
        fr = reach_arm(x, hy, s, 26 * 0.95, (hc[0] + sg * 40 * s, hc[1] - 60 * s), flip)
        ba = reach_arm(x, hy, s, -14 * 0.95, (hc[0] - sg * 50 * s, hc[1] - 70 * s), flip)
    else:
        fr, ba = DEVA_POSE[pose]
    jig = shake * 0.05 * math.sin(t * 14 + ph)
    pts = silhouette(cr, lambda c: fig(c, S.DEVA, "sg_deva", t, x, s, front=fr, backa=ba, head=0.25 * bow + jig,
                                       flip=flip, feet=feet, ph=ph, rods=True, rot=rot + 0.06 * bow, y=y, legs=legs,
                                       alpha=1.0, blur=blur), 0.82 * alpha)
    if garland and pts:
        gx, gy = to_user(cr, pts["handF"])
        prop(cr, "kk_garland", gx, gy - 10 * s, 1.1 * s / 0.55, rot=sway(t, 0.04, 0.6, ph), alpha=alpha)
    return pts


def deva_walk(cr, t, t0, t1, x0, x1, s, feet=G, **kw):
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, 0.45)
    return deva(cr, t, x, s, feet=feet, y=feet - 434 * s + bob, legs=(0.32 * ph, -0.32 * ph), rot=rock, **kw)


def elephant(cr, t, x, ground_, s, alpha=1.0, blur=0.0, snore=True):
    """The elephant asleep (breathing slowly), soft z's rising from its head."""
    if alpha <= 0.01:
        return
    br = 1 + 0.012 * math.sin(t * 1.6)
    cr.save()
    cr.translate(x, ground_)
    cr.scale(1, br)
    prop(cr, "sg_elephant", 0, 0, s, alpha=alpha, blur=blur)
    cr.restore()
    if snore:
        zzz(cr, t, x + S.EL_HEAD[0] * s + 40, ground_ + S.EL_HEAD[1] * s - 60, 1.3, alpha)


def kailash(cr, alpha=0.55, y=1260, s=0.62, blur=5.0):
    prop(cr, "sg_kailash", 540, y, s, alpha=alpha, blur=blur)


def hall(cr, t, alpha=1.0, blur=0.0, s=1.0):
    prop(cr, "sg_hall", 540, G + 6, s, rot=sway(t, 0.002, 0.3), alpha=alpha, blur=blur)


def panel(cr, t, t_in, x, y, w, h, alpha=1.0):
    """A tall parchment panel dropping in on its rod (the split card); returns its (top y, alpha)."""
    q = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(q) * alpha
    if a <= 0.01:
        return None, 0.0
    yy = y + 70 * (1 - q)
    pc.rod(cr, x, yy + h / 2, x + 30, H + 60, alpha=0.5 * a)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(sway(t, 0.006, 0.4, x * 0.01))
    pc.poly(cr, [(-w / 2, -h / 2 + 18), (-w / 2 + 18, -h / 2), (w / 2 - 18, -h / 2), (w / 2, -h / 2 + 18),
                 (w / 2, h / 2 - 18), (w / 2 - 18, h / 2), (-w / 2 + 18, h / 2), (-w / 2, h / 2 - 18)])
    cr.set_source_rgba(0.97, 0.86, 0.60, 0.97 * a)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, a)
    cr.set_line_width(5)
    cr.stroke()
    for k in range(int(w // 22)):
        for yd in (-h / 2 + 10, h / 2 - 10):
            cr.new_sub_path()
            cr.arc(-w / 2 + 16 + k * 22, yd, 2.6, 0, 2 * math.pi)
    cr.set_source_rgba(0.55, 0.32, 0.14, 0.8 * a)
    cr.fill()
    cr.restore()
    return yy, a


def fit(text, size, maxw):
    w, _ = text_size(text, size)
    return min(size, int(size * maxw / max(1, w)))


# ------------------------------------------------------------------ s1  hook


HK = (330, 1.12, 1900)               # Shani in the hook: x, scale, feet
TRI1 = (850, 1240)                   # the small trident that is crossed out


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "s1")
    tS, tN, tL, tF = c["S"], c["N"], c["L"], c["F"]
    x, s, feet = HK
    glow(cr, x + 40, feet - 760 * s, 600, 0.42)
    flap = clamp(1 - abs(t - tF - 0.3) / 0.35) if t > tF - 0.1 else 0.0
    crow(cr, t, 700, feet - 4, 0.5, flap=flap, ph=0.4)
    pts = shani(cr, t, x, s, mood="glance", feet=feet, front=(-0.45, -0.85), hits=[(tN, 0.3), (tL, 0.4)], ph=1.0,
                head=-0.03 * prog(t, tL - 0.1, 0.3))
    eye = eye_of(cr, pts, k=0.21)
    pulse = 0.5 + 0.5 * math.sin(t * 3.0)
    flare = math.exp(-2.2 * max(0.0, t - tL)) * (t > tL - 0.05)
    eye_glow(cr, eye, 0.45 + 0.2 * pulse + 0.6 * flare, 1.0 + 0.6 * flare)
    if t > tL - 0.05:
        sightline(cr, eye, (W + 40, eye[1] + 260), 0.9 * math.exp(-1.6 * max(0.0, t - tL - 0.3)),
                  reach=ease(clamp((t - tL + 0.05) / 0.35)), w=0.9)
    tq = back(clamp((t - tS) / 0.35), 1.5)
    if tq > 0.01:
        a = clamp(tq) * (1 - prog(t, tL - 0.1, 0.4))
        prop(cr, "sg_trishul", TRI1[0], TRI1[1] - 80 * (1 - tq), 0.42, rot=0.12 + sway(t, 0.02, 0.5), alpha=a)

    def ui(cr):
        head2(cr, t, "GANESHA'S HEAD WASN'T CUT BY SHIVA", -1.0, "IT WAS SHANI'S LOOK", 0.3, big_size=170, ghost=-1.0,
              under=tF)
        if tS < t < tL + 0.3:
            big_x(cr, TRI1[0], TRI1[1] - 20, 230, 300, prog(t, tS + 0.35, 0.35), alpha=1 - prog(t, tL - 0.1, 0.4))
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.2) + flash_at(t, tL, 0.3) + flash_at(t, tF, 0.15))


# ------------------------------------------------------------------ s2  it's written in a Purana


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "s2")
    tX, tM, tP = c["X"], c["M"], c["P"]
    leaves = [(None, [("BRAHMA VAIVARTA PURANA", 84, HEAD_FONT)], 0),
              (tP - 0.2, [([("PART 3:", INK), ("GANAPATI KHANDA", RED)], 70, HEAD_FONT)], 0),
              (tP + 0.3, [("SHANI'S GLANCE AT GANESHA", 40, MONO_FONT)], 0)]
    book(cr, t, 540, 940, 0.86, leaves, t_in=t0 + 0.05, t_open=tM, ring=(1, 0, 1, tP + 0.25))

    def ui(cr):
        if t < tM:
            struck = t > tX + 0.25
            box = head2(cr, t, "THIS IS NOT A", t0 + 0.05, "FILM STORY", t0 + 0.35, big_size=210,
                        big_color=(0.42, 0.30, 0.20) if struck else INK)
            if box and t > tX:
                bx, by, bw, bh = box
                big_x(cr, W / 2, by + bh / 2, bw + 60, bh * 0.95, prog(t, tX, 0.3), lw=24)
        else:
            head2(cr, t, "IT'S WRITTEN IN A", tM - 0.2, "PURANA", tM + 0.06, big_size=240, under=tP + 0.2)
    return dict(ui=ui, flash=flash_at(t, tM, 0.25) + flash_at(t, tP, 0.2))


# ------------------------------------------------------------------ s3  two different stories


PAN = ((290, "SHIVA PURANA"), (790, "BRAHMA VAIVARTA"))
PAN_Y, PAN_W, PAN_H = 1120, 460, 860


def s_split(cr, t, tl, t0, t1):
    c = cues(tl, "s3")
    tSh, tT, tSP, tP, tD = c["Sh"], c["T"], c["SP"], c["P"], c["D"]
    glow(cr, 540, 1150, 660, 0.35)

    def ui(cr):
        if t < tP:
            head2(cr, t, "WE ALL HEARD:", t0 + 0.05, "SHIVA'S TRIDENT", tT, big_size=210)
        else:
            head2(cr, t, "SAME GANESHA,", tP - 0.1, "TWO DIFFERENT STORIES", tP + 0.45, big_size=180, under=tD)
        (lx, ltitle), (rx, rtitle) = PAN
        yy, a = panel(cr, t, t0 + 0.1, lx, PAN_Y, PAN_W, PAN_H)
        if a > 0:
            top = yy - PAN_H / 2
            draw_text(cr, ltitle, lx, top + 70, fit(ltitle, 64, PAN_W - 60), RED, a, anchor="cm")
            feet = top + 705
            front = mix((-0.4, -0.5), (-2.75, -0.15), prog(t, tT - 0.2, 0.35))
            silhouette(cr, lambda c_: fig(c_, S.SHIVA, "sg_shiva", t, lx - 40, 0.42, front=front, backa=(0.4, -0.3),
                                          feet=feet, rods=False, ph=0.5,
                                          extra={"sg_shiva_armF_lo": held("sg_trishul", front, 0.56)}),
                       0.85 * a * prog(t, tSh - 0.1, 0.35))
            if t > tT - 0.1:
                sparkle(cr, lx + 40, top + 170, 30 * prog(t, tT, 0.3), a * (0.6 + 0.4 * math.sin(t * 5)))
            q = prog(t, tT, 0.3) * a
            if q > 0:
                draw_text(cr, "THE TRIDENT", lx, top + 770 + 10 * (1 - q), 60, INK, q, anchor="cm")
            if t > tSP:
                tick(cr, lx + 120, top + 560, 120, prog(t, tSP, 0.35))
        yy, a = panel(cr, t, tP - 0.25, rx, PAN_Y, PAN_W, PAN_H)
        if a > 0:
            top = yy - PAN_H / 2
            draw_text(cr, rtitle, rx, top + 70, fit(rtitle, 64, PAN_W - 60), RED, a, anchor="cm")
            q = back(clamp((t - tP) / 0.35), 1.6)
            if q > 0:
                cr.save()
                cr.translate(rx, top + 420)
                cr.rotate(0.1 * math.sin(t * 2.6) + 0.3 * (1 - q))
                cr.scale(q, q)
                draw_text(cr, "?", 0, 0, 380, RED, clamp(q) * a, anchor="cm")
                cr.restore()
            q = prog(t, tD - 0.1, 0.3) * a
            if q > 0:
                draw_text(cr, "SHANI'S LOOK", rx, top + 770 + 10 * (1 - q), 60, INK, q, anchor="cm")
    return dict(ui=ui, flash=flash_at(t, tSP, 0.15) + flash_at(t, tD, 0.2))


# ------------------------------------------------------------------ s4  Shani's secret: deep in meditation


SH4 = (480, 0.95)                    # Shani seated on the lotus: x, scale


def s_med(cr, t, tl, t0, t1):
    c = cues(tl, "s4")
    tS, tM = c["S"], c["M"]
    x, s = SH4
    glow(cr, 540, 1350, 640, 0.35)
    ground(cr)
    lit = prog(t, tM - 0.1, 0.7)
    glow(cr, x + 60, G - 480, 520, 0.3 + 0.35 * lit)
    aura(cr, t, x + 30, G - 600 * s, 200 * s, 640 * s, 0.75 * lit, n=20, spin=0.08)
    pts = shani_sit(cr, t, x, G, s, mood="shut", head=0.06, hits=[(tS, 0.25)], ph=1.0, **MED)
    hop = max(0.0, math.sin(math.pi * clamp((t - (tS + tM) / 2) / 0.35)))
    crow(cr, t, 900 - 60 * prog(t, (tS + tM) / 2, 0.35), G + 4 - 40 * hop, 0.42, flip=True, ph=0.7, flap=hop)
    if t > tM:
        lights(cr, t, x + 60, G - 520, 320, 12, 0.7 * lit)
    top = to_user(cr, pts["top"])

    def ui(cr):
        if t < tM:
            head2(cr, t, "FIRST, KNOW", t0 + 0.05, "SHANI'S SECRET", tS, big_size=210)
        else:
            head2(cr, t, "ONE DAY, DEEP IN", tM - 0.15, "MEDITATION", tM + 0.05, big_size=230, under=tM + 0.5)
        tag(cr, t, t0 + 0.35, "SHANI DEV", min(max(top[0] + 40, 200), 880), top[1] - 200 * SH4[1] - 50, 36)
    return dict(ui=ui, flash=flash_at(t, tS, 0.15) + flash_at(t, tM, 0.2))


# ------------------------------------------------------------------ s5  his wife came; he didn't even look


SH5 = (300, 0.8)                     # Shani seated (eyes shut): x, scale
WF5 = (790, 0.66)                    # his wife: where she stops, scale (facing left)


def s_wife(cr, t, tl, t0, t1):
    c = cues(tl, "s5")
    tW, tA, tL, tN = c["W"], c["A"], c["L"], c["N"]
    glow(cr, 540, 1350, 640, 0.35)
    ground(cr)
    x, s = SH5
    glow(cr, x + 60, G - 400, 380, 0.3)
    aura(cr, t, x + 30, G - 600 * s, 180 * s, 560 * s, 0.45, n=18, spin=0.08)
    pts = shani_sit(cr, t, x, G, s, mood="shut", head=0.06, ph=1.0, **MED)
    eye = eye_of(cr, pts)
    wx, ws = WF5
    t_arr = min(tA + 0.2, t0 + 1.6)
    waiting = keyed(t, [(t0, 0.0), (t_arr + 0.3, 1.0)], 0.35, 1.2)
    mood = "smile" if t < tN + 0.2 else "open"
    if t < t_arr:
        wp = glide(cr, t, wife, tW - 0.5, t_arr, 1250, wx, ws, mood=mood, flip=True, front=(-0.6, -1.4))
    else:
        wp = wife(cr, t, wx, ws, mood=mood, flip=True, front=mix((-0.6, -1.4), ANJALI["front"], waiting),
                  backa=mix((0.15, -0.2), ANJALI["backa"], waiting), head=-0.04 + 0.08 * prog(t, tN, 0.4),
                  hits=[(tN, 0.3)])
    sun_arc(cr, t, 560, 800, 200, 0.1 + 0.8 * clamp((t - t_arr) / max(0.8, tL - t_arr)),
            prog(t, t_arr + 0.2, 0.3) * (1 - prog(t, tL, 0.3)))
    face = to_user(cr, wp["head"])
    wtop = to_user(cr, wp["top"])

    def ui(cr):
        if t < tL:
            head2(cr, t, "HIS WIFE CAME TO HIM,", t0 + 0.05, "SMILING", tA, big_size=240)
        else:
            head2(cr, t, "BUT HE DIDN'T EVEN", tL - 0.15, "LOOK", tN, big_size=280)
        tag(cr, t, tW + 0.2, "HIS WIFE", min(wtop[0], 900), wtop[1] - 150, 34, t_out=tL - 0.2)
        plate(cr, t, tW + 0.45, "A GANDHARVA PRINCESS", min(wtop[0], 860), wtop[1] - 82, 28, t_out=tL - 0.2)
        if t > tL - 0.1:
            line = [(eye[0] + (face[0] - eye[0]) * u, eye[1] + (face[1] - 30 - eye[1]) * u - 60 * math.sin(math.pi * u))
                    for u in (i / 30 for i in range(31))]
            dotted(cr, line, prog(t, tL - 0.1, 0.4), 28, 6.5, FADE, 0.9)
            mx, my = line[15]
            big_x(cr, mx, my, 120, 110, prog(t, tN, 0.3))
            red_ring(cr, eye[0], eye[1] - 4, 60, 40, prog(t, tN + 0.1, 0.4), 8)
    return dict(ui=ui, flash=flash_at(t, tN, 0.2))


# ------------------------------------------------------------------ s6  the curse


def s_curse(cr, t, tl, t0, t1):
    c = cues(tl, "s6")
    tA, tC, tL, tH = c["A"], c["C"], c["L"], c["H"]
    glow(cr, 540, 1350, 640, 0.35)
    ground(cr)
    x, s = SH5
    wake = t > tC + 0.6
    pts = shani_sit(cr, t, x, G, s, mood="down" if wake else "shut", head=0.06 + 0.06 * wake, ph=1.0,
                    hits=[(tC + 0.6, 0.4)], **MED)
    head_s = to_user(cr, pts["head"])
    wx, ws = WF5
    tgt = (head_s[0] + 20, head_s[1] + 10)
    aim = woman_point(wx, ws, tgt, flip=True)
    p = keyed(t, [(t0, 0.0), (tC - 0.15, 1.0)], 0.3, 1.5)
    mood = "curse" if tC - 0.1 < t < tH + 0.6 and math.sin((t - tC) * 15) > -0.2 else ("angry" if t > tA - 0.1
                                                                                          else "open")
    wp = wife(cr, t, wx, ws, mood=mood, flip=True, front=mix((-0.3, -0.6), aim, p), backa=(0.35, -0.6),
              head=-0.06 * p, hits=[(tA, 0.4), (tC, 0.5)])
    hand = to_user(cr, wp["handF"])
    if t > tA:
        red_glow(cr, wx, G - 500, 700, 0.35 * prog(t, tA, 0.5) * (1 - 0.5 * prog(t, tH + 0.6, 0.6)))
    bolt(cr, t, tC, hand, tgt, 1.1)
    bolt(cr, t, tH, hand, tgt, 0.8, seed=3)

    def ui(cr):
        if t < tC:
            head2(cr, t, "SHE BECAME VERY", t0 + 0.05, "ANGRY", tA, big_size=270)
        else:
            head2(cr, t, "AND SHE CURSED HIM:", tC - 0.1, None, 0.0)
        card2(cr, t, tL - 0.45, 540, 760, 0.82, [("WHOEVER YOU LOOK AT", 70, INK, -44, tL - 0.3),
                                          ("WILL LOSE HIS HEAD", 80, RED, 48, tH)])
    return dict(ui=ui, flash=flash_at(t, tC, 0.35) + flash_at(t, tH, 0.2))


# ------------------------------------------------------------------ s7  eyes always down


SH7 = (450, 0.8)


def s_down(cr, t, tl, t0, t1):
    c = cues(tl, "s7")
    tA, tD = c["A"], c["D"]
    glow(cr, 540, 1350, 640, 0.35)
    ground(cr)
    days = (t - tA) / 1.3 if t > tA - 0.2 else 0.0
    sun_arc(cr, t, 560, 790, 230, days % 1.0, prog(t, tA - 0.2, 0.3))
    x, s = SH7
    t_stop = min(tD - 0.2, t0 + 1.6)
    cx_, cbob, _, _ = hop_walk(t, t0 - 0.2, t_stop + 0.3, 40, 740, 0.3)
    crow(cr, t, cx_, G + 2 + 0.6 * cbob, 0.42, ph=0.9)
    if t < t_stop:
        pts = shani_walk(cr, t, t0 - 0.2, t_stop, -180, x, s, mood="down", ph=1.0)
    else:
        pts = shani(cr, t, x, s, mood="down", head=0.12 * prog(t, tD - 0.2, 0.3), hits=[(tD, 0.3)], ph=1.0)
    eye = eye_of(cr, pts)
    gp = (eye[0] + 210, G - 6)

    def ui(cr):
        head2(cr, t, "FROM THAT DAY ON:", t0 + 0.05, "EYES ALWAYS DOWN", tD, big_size=200)
        if t > tD - 0.15:
            line = [(eye[0] + (gp[0] - eye[0]) * u, eye[1] + (gp[1] - eye[1]) * u) for u in (i / 30 for i in range(31))]
            dotted(cr, line, prog(t, tD - 0.15, 0.4), 26, 6.5, RED, 0.95)
            down_arrow(cr, 880, 1050, 1420, prog(t, tD + 0.2, 0.4), 0.95, 18)
        plate(cr, t, tA + 0.1, "DAY AFTER DAY", 880, 980, 30)
    return dict(ui=ui, flash=flash_at(t, tD, 0.2))


# ------------------------------------------------------------------ s8  Kailash: Ganesha is born


CR8 = (540, 0.82)                    # the cradle: x, scale (ground G)


def s_birth(cr, t, tl, t0, t1):
    c = cues(tl, "s8")
    tB, tD, tBl, tS = c["B"], c["D"], c["Bl"], c["S"]
    kailash(cr)
    glow(cr, 540, 1300, 680, 0.4)
    hall(cr, t, alpha=0.95, blur=1.5)
    sh_a = prog(t, tS - 0.3, 0.5)
    if sh_a > 0:                                                                  # Shani, small, at the back
        b, k, a = depth(t, tS - 0.3, 0.6)
        shani(cr, t, SH8X, 0.46 * k, mood="down", feet=G - 60, alpha=a, blur=b + 1.5, rods=False, ph=1.3, head=0.1)
    ground(cr)
    lit = prog(t, tB - 0.1, 0.6)
    _, head_c = cradle(cr, t, CR8[0], G, CR8[1], "hu", glow_a=0.25 + 0.55 * lit, arms=(0.35 * math.sin(t * 2.4),
                                                                                       0.3 * math.sin(t * 2.0 + 1)))
    if t > tB:
        petals(cr, t, tB, 540, 520, n=14, spread=900, fall=1300, dur=3.4, loop=True, s=0.55)
    for i, (x0, x1, fl, sc) in enumerate(((-160, 170, False, 0.62), (1240, 960, True, 0.62))):
        t_in = tD - 0.3 + 0.25 * i
        if t > t_in - 0.6:
            hold = keyed(t, [(t0, 0.0), (tBl, 1.0)], 0.3, 1.3)
            if t < t_in + 1.0:
                deva_walk(cr, t, t_in - 0.6, t_in + 1.0, x0, x1, sc, flip=fl, pose="garland", garland=True,
                          ph=0.6 * i)
            else:
                deva(cr, t, x1, sc, pose="garland", garland=True, flip=fl, ph=0.6 * i, bow=0.6 * hold)

    def ui(cr):
        if t < tD:
            head2(cr, t, "THEN GANESHA WAS", t0 + 0.05, "BORN", tB, big_size=290)
        elif t < tS:
            head2(cr, t, "ALL THE DEVAS CAME TO", tD - 0.1, "BLESS HIM", tBl, big_size=250)
        else:
            head2(cr, t, "AND SHANI DEV", tS - 0.15, "CAME TOO", tS + 0.05, big_size=250)
        tag(cr, t, tB + 0.4, "BABY GANESHA", head_c[0], 1090, 32, t_out=tS - 0.4)
        tag(cr, t, tS + 0.2, "SHANI DEV", SH8X, 1060, 30)
    return dict(ui=ui, flash=flash_at(t, tB, 0.2))


SH8X = 770                           # Shani at the back of the court (s8)


# ------------------------------------------------------------------ s9  Parvati asks


SH9 = (200, 0.7)                     # Shani (eyes down)
CR9 = (590, 0.66)                    # the cradle
PV9 = (900, 0.7)                     # Parvati (facing left)


def court(cr, t, alpha=0.75):
    glow(cr, 540, 1300, 680, 0.4)
    hall(cr, t, alpha=alpha, blur=4.0)
    ground(cr)


def s_ask(cr, t, tl, t0, t1):
    c = cues(tl, "s9")
    tN, tP, tQ = c["N"], c["P"], c["Q"]
    court(cr, t)
    pts = shani(cr, t, SH9[0], SH9[1], mood="down", head=0.12, ph=1.0)
    eye = eye_of(cr, pts)
    cradle(cr, t, CR9[0], G, CR9[1], "hu", glow_a=0.45, arms=(0.3 * math.sin(t * 2.4), 0.25 * math.sin(t * 2 + 1)))
    turn = keyed(t, [(t0, 0.0), (tP, 1.0)], 0.3, 1.3)
    speak = tQ - 0.4 < t < t1 - 0.2 and math.sin(t * 15) > 0
    pp = parvati(cr, t, PV9[0], PV9[1], mood="speak" if speak else "smile", flip=True,
                 front=mix((-0.7, -0.9), (-1.35, -0.4), turn), head=-0.05 * turn, hits=[(tP, 0.3)])
    ptop = to_user(cr, pp["top"])

    def ui(cr):
        if t < tP:
            head2(cr, t, "BUT SHANI DIDN'T LOOK AT", t0 + 0.05, "THE BABY", tN, big_size=240)
        else:
            head2(cr, t, "PARVATI ASKED:", tP - 0.1, None, 0.0)
        if t > tN - 0.2:
            gp = (eye[0] + 150, G - 6)
            line = [(eye[0] + (gp[0] - eye[0]) * u, eye[1] + (gp[1] - eye[1]) * u) for u in (i / 24 for i in range(25))]
            dotted(cr, line, prog(t, tN - 0.2, 0.4), 26, 6, RED, 0.9 * (1 - prog(t, tQ, 0.4)))
            red_ring(cr, eye[0], eye[1] - 2, 50, 34, prog(t, tN, 0.4), 7, 1 - prog(t, tQ, 0.4))
        tag(cr, t, tP + 0.1, "PARVATI", min(ptop[0] - 30, 900), ptop[1] - 190, 32, t_out=tQ - 0.55)
        cloud_text(cr, t, 520, 720, 0.86, [("WHY WON'T YOU LOOK", 64, INK, -46, tQ - 0.35),
                                           ("AT MY SON?", 116, RED, 52, tQ)], flip=True, t_in=tQ - 0.5)
    return dict(ui=ui, flash=flash_at(t, tQ, 0.2))


# ------------------------------------------------------------------ s10  he warns; she laughs and insists


def s_insist(cr, t, tl, t0, t1):
    c = cues(tl, "s10")
    tC, tL, tI, tS = c["C"], c["L"], c["I"], c["S"]
    court(cr, t)
    talk = tC - 0.1 < t < tL - 0.2
    explain = keyed(t, [(t0, 0.0), (tC, 1.0), (tL, 0.0)], 0.3, 1.3)
    shani(cr, t, SH9[0], SH9[1], mood="speak" if (talk and math.sin(t * 14) > 0) else "down", head=0.12, ph=1.0,
          front=mix((-0.32, -0.55), (-1.1, -1.2), explain), hits=[(tC, 0.3)])
    cx, cs = CR9
    cradle(cr, t, cx, G, cs, "hu", glow_a=0.45 + 0.35 * prog(t, tI, 0.4),
           arms=(0.3 * math.sin(t * 2.4), 0.25 * math.sin(t * 2 + 1)))
    present = keyed(t, [(t0, 0.0), (tI - 0.1, 1.0)], 0.3, 1.4)
    aim = woman_point(PV9[0], PV9[1], (cx + 40, G - 420 * cs), flip=True)
    laughing = tL - 0.1 < t < tI
    mood = "laugh" if laughing else ("speak" if (t > tI and math.sin(t * 15) > 0) else "smile")
    pp = parvati(cr, t, PV9[0], PV9[1], mood=mood, flip=True, front=mix((-0.7, -0.9), aim, present),
                 head=-0.12 * laughing - 0.05 * present + 0.04 * math.sin(t * 9) * laughing,
                 hits=[(tL, 0.3), (tI, 0.4)])
    ph_ = to_user(cr, pp["head"])

    def ui(cr):
        if t < tL:
            head2(cr, t, "HE TOLD HER ABOUT", t0 + 0.05, "THE CURSE", tC, big_size=250)
        elif t < tI:
            head2(cr, t, "BUT SHE", tL - 0.1, "LAUGHED IT OFF", tL + 0.05, big_size=220)
        else:
            head2(cr, t, "AND SHE INSISTED:", tI - 0.1, "LOOK AT MY SON!", tS, big_size=200, under=tS + 0.35)
        card(cr, t, tC + 0.1, 330, 760, 0.56, [("WHOEVER YOU LOOK AT", 64, INK, -44),
                                               ("WILL LOSE HIS HEAD", 72, RED, 46)], t_out=tL - 0.1)
        ha(cr, t, tL, ph_[0] - 40, ph_[1] - 120, 64)
    return dict(ui=ui, flash=flash_at(t, tI, 0.2) + flash_at(t, tS, 0.15))


# ------------------------------------------------------------------ s11  close: one glance


CLOSE = (470, 1.75, 2060)            # Shani in close-up: x, scale, hip y
CR11 = (905, 1770, 0.36)             # the cradle far right: x, ground, scale


def s_glance(cr, t, tl, t0, t1):
    c = cues(tl, "s11")
    tF, tC, tL = c["F"], c["C"], c["L"]
    glow(cr, 420, 1150, 700, 0.4)
    cx, cg, cs = CR11
    _, head_c = cradle(cr, t, cx, cg, cs, "hu", glow_a=0.5, arms=(0.3 * math.sin(t * 2.4), 0.25 * math.sin(t * 2 + 1)))
    x, s, hy = CLOSE
    tremble = 0.006 * math.sin(t * 23) * prog(t, tF, 0.3) * (1 - prog(t, tL + 0.6, 0.4))
    mood = "glance" if t > tC - 0.05 else ("sad" if t > tF else "down")
    pts = shani(cr, t, x, s, mood=mood, y=hy, rot=tremble, head=0.1 - 0.06 * prog(t, tC, 0.3), front=(-0.25, -0.5),
                crow_on=False, hits=[(tF, 0.2)], ph=1.0)
    eye = eye_of(cr, pts, k=0.21 if mood == "glance" else 0.13)
    if t > tF:                                                                    # fear: a bead of sweat
        tears(cr, t, tF + 0.1, (eye[0] - 70, eye[1] - 120), n=3, period=0.9, alpha=0.8)
    ga = prog(t, tC - 0.05, 0.3)
    eye_glow(cr, eye, 0.5 * ga + 0.6 * math.exp(-2 * max(0.0, t - tL)) * (t > tL), 1.6)
    if t > tL - 0.05:
        sightline(cr, eye, (head_c[0], head_c[1] + 20), 0.95, reach=ease(clamp((t - tL + 0.05) / 0.3)), w=1.0)

    def ui(cr):
        if t < tL:
            head2(cr, t, "FEARFULLY, FROM THE", t0 + 0.05, "CORNER OF HIS EYE", tC, big_size=180)
        else:
            head2(cr, t, "JUST ONCE:", tL - 0.1, "ONE GLANCE", tL + 0.05, big_size=250, under=tL + 0.4)
    return dict(ui=ui, eve=0.08 * prog(t, tC, 0.5), flash=flash_at(t, tL, 0.3))


# ------------------------------------------------------------------ s12  a flash: the head fell


CR12 = (540, 0.86)


def s_flash(cr, t, tl, t0, t1):
    c = cues(tl, "s12")
    tM, tH, tA = c["M"], c["H"], c["A"]
    glow(cr, 540, 1300, 640, 0.38)
    hall(cr, t, alpha=0.55, blur=6.0)
    ground(cr)
    cx, cs = CR12
    gone = t >= tH
    _, head_c = cradle(cr, t, cx, G, cs, "cloth" if gone else "hu", glow_a=0.5,
                       arms=(0.3 * math.sin(t * 2.4), 0.25 * math.sin(t * 2 + 1)))
    if not gone:
        sightline(cr, (-40, 860), (head_c[0], head_c[1] + 20), 0.8 + 0.15 * math.sin(t * 9))
    else:
        def ball_y(dt):
            u = clamp(dt / 2.4)
            return head_c[1] - (head_c[1] - 560) * (u * u * (3 - 2 * u)), u
        by, u = ball_y(t - tH)
        bx = head_c[0] + 40 * math.sin(u * 5)
        light_ball(cr, bx, by, 60 * (1 - 0.25 * u), 1 - 0.5 * prog(t, tH + 2.0, 0.6), t)
        for i in range(7):
            yy, uu = ball_y(t - tH - 0.12 * (i + 1))
            if 0 < uu < 1:
                sparkle(cr, head_c[0] + 40 * math.sin(uu * 5) + 26 * math.sin(i * 2.3), yy + 20,
                        16 * (1 - 0.1 * i), 0.9 - 0.1 * i)
        glow(cr, cx, G - 360 * cs, 360, 0.4 * (1 - prog(t, tH + 1.0, 1.0)))
    white = clamp(1.3 * math.exp(-3.2 * (t - tH))) if gone else 0.0

    def ui(cr):
        if t < tH:
            head2(cr, t, "AND IN THAT VERY", t0 + 0.05, "MOMENT...", tM, big_size=250)
        else:
            head2(cr, t, "IN A FLASH OF LIGHT,", tH + 0.25, "THE HEAD FELL", tA, big_size=230, big_color=INK)
    return dict(ui=ui, eve=0.18 * prog(t, tM, 0.6) * (1 - gone), white=white)


# ------------------------------------------------------------------ s13  Parvati fainted; chaos


PV13 = (540, 0.66)


def s_chaos(cr, t, tl, t0, t1):
    c = cues(tl, "s13")
    tF, tC = c["F"], c["C"]
    court(cr, t, 0.6)
    grief = prog(t, tF - 0.2, 0.8)
    red_glow(cr, PV13[0], G - 300, 800, 0.85 * grief)
    for x, s, fl, ph, bl in ((800, 0.46, True, 2.1, 3.0), (300, 0.44, False, 0.7, 3.0), (130, 0.6, False, 0.0, 0.0),
                             (980, 0.6, True, 1.2, 0.0)):
        q = prog(t, tC - 0.4, 0.4)
        deva(cr, t, x, s, pose="head" if t > tC - 0.3 else "stand", flip=fl, ph=ph, blur=bl,
             shake=q, feet=G - (40 if bl else 0), alpha=0.5 + 0.5 * prog(t, t0, 0.3))
    fall = clamp((t - tF - 0.1) / 1.2)
    fe = ease(fall)
    pp = parvati(cr, t, PV13[0], PV13[1], mood="faint" if t > tF else "open", front=mix((-0.4, -2.0), (-0.3, -2.3), fe),
                 backa=(0.25, -0.4), lie=fe, lie_dir=-1, hits=[(tF, 0.5)], rods=True)
    if t > tF + 0.9:
        h = to_user(cr, pp["head"])
        tears(cr, t, tF + 1.0, (h[0] + 10, h[1] - 10), n=3, period=0.9, alpha=0.8)

    def ui(cr):
        if t < tC:
            head2(cr, t, "PARVATI", t0 + 0.05, "FAINTED", tF, big_size=280)
        else:
            head2(cr, t, "AND ALL AROUND:", tC - 0.15, "CHAOS", tC, big_size=320)
    return dict(ui=ui, flash=flash_at(t, tC, 0.2))


# ------------------------------------------------------------------ s14  Vishnu flew north


EL14 = (540, G - 30, 0.5)            # the elephant: x, ground, scale
MOON = (180, 660)
NIGHT2 = 0.6                         # the moonlit night is darker than the other night shots
GS = 0.5                             # Garuda's scale in the night shots
HOVER = (560, 1090)                  # where Garuda hovers above the sleeping elephant


def night_set(cr, t, trees=True):
    stars(cr, t, 0.9, ((330, 760), (620, 640), (900, 900), (470, 1150), (840, 1120), (1000, 1290), (120, 1000)))
    glow(cr, MOON[0], MOON[1], 240, 0.5)
    prop(cr, "moon", MOON[0], MOON[1], 0.9, rot=-0.3)
    if trees:
        prop(cr, "tree", 60, G + 10, 0.55, rot=sway(t, 0.005, 0.3), alpha=0.75, blur=4)
        prop(cr, "tree", 1060, G + 10, 0.6, rot=sway(t, 0.005, 0.3, 1.0), alpha=0.75, blur=4)
    ground(cr)


def flight(t, t0, t_arr, path):
    """Position along a polyline path between t0 and t_arr (eased), then hovering at its end."""
    v = clamp((t - t0) / max(0.5, t_arr - t0))
    u = v * v * (3 - 2 * v) * 0.6 + v * 0.4
    k = u * (len(path) - 1)
    i = min(int(k), len(path) - 2)
    f = k - i
    return (path[i][0] + (path[i + 1][0] - path[i][0]) * f,
            path[i][1] + (path[i + 1][1] - path[i][1]) * f + 12 * math.sin(t * 2.0) * u)


def s_north(cr, t, tl, t0, t1):
    c = cues(tl, "s14")
    tV, tN, tE = c["V"], c["N"], c["E"]
    night_set(cr, t)
    ex, eg, es = EL14
    ea = prog(t, tE - 0.3, 0.5)
    if ea > 0:
        glow(cr, ex + 100, eg - 200, 460, 0.6 * ea)
        elephant(cr, t, ex, eg, es, alpha=ea)
    path = [(-60, 1330), (160, 1240), (380, 1150), HOVER]
    t_arr = tE - 0.2
    gx, gy = flight(t, t0 - 0.3, t_arr, path)
    rot = -0.14 + 0.18 * prog(t, t_arr - 0.4, 0.8)
    trail = [(p[0] - 160, p[1] + 90) for p in path]
    dotted(cr, trail, clamp((t - t0 + 0.3) / max(0.5, t_arr - t0)), 30, 7, RED, 0.75 * prog(t, tN - 0.3, 0.4))
    garuda(cr, t, gx, gy, GS, rot=rot)

    def ui(cr):
        if t < tE:
            head2(cr, t, "THEN VISHNU, ON GARUDA,", t0 + 0.05, "FLEW NORTH", tN, big_size=240)
        else:
            head2(cr, t, "THERE, AN ELEPHANT WAS", tE - 0.1, "SLEEPING", tE + 0.15, big_size=250)
        tag(cr, t, tV + 0.2, "VISHNU ON GARUDA", min(max(gx - 30, 220), 860), gy + 200, 28, t_out=tE - 0.3)
        if t > tN - 0.2:
            q = prog(t, tN - 0.2, 0.4)
            nx, ny = 950, 600
            cr.save()
            cr.set_source_rgba(*RED, 0.9 * q)
            cr.set_line_width(12)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.move_to(nx, ny + 170)
            cr.line_to(nx, ny + 170 - 150 * q)
            cr.stroke()
            pc.poly(cr, [(nx - 30, ny + 30), (nx + 30, ny + 30), (nx, ny - 14)])
            cr.fill()
            cr.restore()
            plate(cr, t, tN, "NORTH", nx, ny + 216, 30, alpha=q)
        tag(cr, t, tE + 0.3, "A SLEEPING ELEPHANT", 340, eg - 330, 26)
    return dict(ui=ui, night=NIGHT2, lift=1.0, flash=flash_at(t, tN, 0.15))


# ------------------------------------------------------------------ s15  the chakra; Ganesha lives again


CR15 = (540, 0.86)


def s_alive(cr, t, tl, t0, t1):
    c = cues(tl, "s15")
    tC, tJ, tL = c["C"], c["J"], c["L"]
    cut = tJ - 0.25
    t_go = tC + 0.45                                                             # the chakra leaves his hand
    t_hit = t_go + 0.7                                                           # ...and flashes at the elephant
    ex, eg, es = EL14
    hx, hy = ex + S.EL_HEAD[0] * es, eg + S.EL_HEAD[1] * es
    if t < cut:
        night_set(cr, t)
        fade = clamp((t - t_hit) / 0.9)
        glow(cr, ex + 100, eg - 200, 460, 0.6 + 0.6 * fade * (1 - fade) * 4)
        if fade < 1:
            elephant(cr, t, ex, eg, es, alpha=1 - ease(fade), snore=t < t_go)
        if t > t_hit:
            warm(cr, ex + 80, eg - 160, 520, 0.9 * (1 - prog(t, t_hit + 1.2, 0.8)))
            lights(cr, t, ex + 100, eg - 150, 320, 16, 0.9 * (1 - prog(t, cut - 0.3, 0.3)))
            u = clamp((t - t_hit - 0.5) / 1.2)
            light_ball(cr, hx - 30 - 200 * u, hy - 60 - 700 * ease(u), 42 + 12 * fade, clamp(fade * 2), t)
        ch = clamp((t - tC + 0.1) / 0.4)
        flying = t_go < t < t_hit + 0.6
        _, (cx, cy) = garuda(cr, t, HOVER[0], HOVER[1] + 12 * math.sin(t * 2.0), GS, chakra=ch, rot=0.04, flap=0.6,
                             chakra_on=not flying)
        if flying:                                                               # the chakra flies to the elephant
            u = clamp((t - t_go) / (t_hit - t_go))
            px = cx + (hx - cx) * u
            py = cy + (hy - 60 - cy) * u - 180 * math.sin(math.pi * u)
            a = 1 - prog(t, t_hit + 0.2, 0.3)
            glow(cr, px, py, 220, 0.8 * a)
            for k in range(5):
                uu = max(0.0, u - 0.06 * (k + 1))
                sparkle(cr, cx + (hx - cx) * uu, cy + (hy - 60 - cy) * uu - 180 * math.sin(math.pi * uu),
                        24 - 3 * k, a * (1 - 0.15 * k))
            prop(cr, "sg_chakra", px, py, 0.32 * (1 + 0.4 * u), rot=t * 14, alpha=a)
        burst(cr, t, hx - 20, hy - 40, t_hit, n=22, rmax=640)
        out = dict(night=NIGHT2 * (1 - 0.3 * fade), lift=1.0, flash=flash_at(t, t_hit, 0.7))
    else:
        court(cr, t, 0.7)
        rise = ease(clamp((t - tL + 0.2) / 0.7))
        u = clamp((t - cut) / 0.8)
        cx, cs = CR15
        rim = G + S.CRADLE_RIM * cs
        joy = prog(t, tL, 0.4)
        for x, s, fl, ph in ((150, 0.58, False, 0.0), (930, 0.58, True, 1.1)):
            deva(cr, t, x, s, pose="cheer" if t > tL else "plead", flip=fl, ph=ph, alpha=prog(t, cut, 0.4))
        if u < 1:
            cradle(cr, t, cx, G, cs, "cloth", rock=False)
            light_ball(cr, cx, 560 + (rim - 140 - 560) * ease(u), 56, 1.0, t)
        else:
            cradle(cr, t, cx, G, cs, "el", glow_a=0.5 + 0.5 * joy, rise=rise,
                   arms=(0.5 * joy + 0.25 * math.sin(t * 3) * joy, 0.5 * joy + 0.25 * math.sin(t * 3.4 + 1) * joy),
                   hits=[(tL, 0.6)], rock=False)
            burst(cr, t, cx, rim - 200, cut + 0.8, n=18, rmax=560)
        if t > tL:
            petals(cr, t, tL, 540, 480, n=16, spread=960, fall=1300, dur=3.0, loop=True, s=0.6)
            lights(cr, t, cx, rim - 300, 360, 14, 0.8 * joy)
        out = dict(flash=flash_at(t, cut, 0.45) + flash_at(t, tL, 0.3))

    def ui(cr):
        if t_hit < t < cut:                                                      # the golden flash (over the night)
            k = math.exp(-1.6 * (t - t_hit))
            warm(cr, hx - 20, hy - 60, 820, 1.1 * k, (1.0, 0.76, 0.22))
            sparkle(cr, hx - 20, hy - 60, 160 * k, k, (1.0, 0.85, 0.4))
        if t < cut:
            head2(cr, t, "WITH THE", t0 + 0.05, "SUDARSHANA CHAKRA", tC + 0.1, big_size=200)
        elif t < tL:
            head2(cr, t, "AN ELEPHANT'S HEAD FOR", cut + 0.05, "GANESHA", tJ, big_size=270)
        else:
            head2(cr, t, "AND", tL - 0.1, "GANESHA LIVED AGAIN!", tL, big_size=190, under=tL + 0.4)
    out["ui"] = ui
    return out


# ------------------------------------------------------------------ s16  Parvati's curse


PV16 = (330, 0.74)
SH16 = (800, 0.72)


def s_pcurse(cr, t, tl, t0, t1):
    c = cues(tl, "s16")
    tA, tC, tL = c["A"], c["C"], c["L"]
    court(cr, t, 0.6)
    sp = shani(cr, t, SH16[0], SH16[1], mood="sad" if t > tC else "down", flip=True,
               head=0.14 + 0.06 * prog(t, tL, 0.4),
               hits=[(tC + 0.2, 0.4), (tL + 0.2, 0.3)], ph=1.0)
    tgt = to_user(cr, sp["chest"])
    px, ps = PV16
    aim = woman_point(px, ps, tgt)
    p = keyed(t, [(t0, 0.0), (tC - 0.15, 1.0)], 0.3, 1.5)
    mood = "angry" if t > tA - 0.2 else "open"
    if tC - 0.1 < t < tL + 0.6 and math.sin((t - tC) * 15) > 0:
        mood = "speak"
    pp = parvati(cr, t, px, ps, mood=mood, front=mix((-0.3, -0.6), aim, p), backa=(0.35, -0.6), head=-0.05 * p,
                 hits=[(tA, 0.3), (tC, 0.5)])
    if t > tA - 0.2:
        red_glow(cr, px, G - 500, 760, 0.3 * prog(t, tA - 0.2, 0.5))
    hand = to_user(cr, pp["handF"])
    bolt(cr, t, tC, hand, tgt, 1.0, (1.0, 0.35, 0.2))
    bolt(cr, t, tL, hand, tgt, 0.9, (1.0, 0.35, 0.2), seed=5)

    def ui(cr):
        if t < tC:
            head2(cr, t, "BUT PARVATI WAS STILL", t0 + 0.05, "ANGRY", tA, big_size=270)
        else:
            head2(cr, t, "SHE CURSED SHANI:", tC - 0.1, None, 0.0)
        card2(cr, t, tC + 0.1, 540, 760, 0.8, [("BECOME", 84, INK, -50, tL - 0.25), ("LIMBLESS!", 124, RED, 46, tL)])
    return dict(ui=ui, flash=flash_at(t, tC, 0.3) + flash_at(t, tL, 0.25))


# ------------------------------------------------------------------ s17  the devas plead; why he limps


SH17 = (780, 0.72)


def s_limp(cr, t, tl, t0, t1):
    c = cues(tl, "s17")
    tP, tS, tW, tL = c["P"], c["S"], c["W"], c["L"]
    court(cr, t, 0.6)
    for x, s, ph in ((120, 0.6, 0.0), (330, 0.6, 0.9)):
        deva(cr, t, x, s, pose="plead", ph=ph, bow=keyed(t, [(t0, 0.0), (tP, 1.0)], 0.3, 1.2),
             alpha=prog(t, t0 - 0.1, 0.3))
    if t < tW:
        shani(cr, t, SH17[0], SH17[1], mood="sad", flip=True, head=0.16, hits=[(tS, 0.3)], ph=1.0)
    else:
        shani_limp(cr, t, tW + 0.1, t1 + 0.4, SH17[0] - 40, 990, SH17[1], mood="sad", ph=1.0, head=0.1)

    def ui(cr):
        if t < tS:
            head2(cr, t, "THE DEVAS", t0 + 0.05, "PLEADED", tP, big_size=270)
        elif t < tW:
            head2(cr, t, "SO THE CURSE WAS", tS - 0.1, "SOFTENED", tS + 0.15, big_size=260)
        else:
            head2(cr, t, "AND THAT'S", tW - 0.1, "WHY SHANI DEV LIMPS", tL, big_size=180, under=tL + 0.4)
        old_out = tS + 0.45
        card(cr, t, t0 - 0.2, 540, 760, 0.8, [("BECOME", 84, INK, -50), ("LIMBLESS!", 124, RED, 46)], t_out=old_out)
        if tS < t < old_out + 0.3:
            big_x(cr, 540, 760, 520, 220, prog(t, tS, 0.25), alpha=1 - prog(t, old_out, 0.25))
        card2(cr, t, old_out + 0.1, 540, 760, 0.8, [("LAME", 96, RED, -46, old_out + 0.15),
                                                     ("FOREVER", 110, RED, 52, old_out + 0.35)])
    return dict(ui=ui, flash=flash_at(t, tS, 0.2) + flash_at(t, tL, 0.15))


# ------------------------------------------------------------------ s18  fair or unfair?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "s18")
    tW, tQ, tY, tC = c["W"], c["Q"], c["Y"], c["C"]
    glow(cr, 540, 1450, 520, 0.45)
    ground(cr)
    crow(cr, t, 760, G + 2, 0.4, ph=0.3)
    shani(cr, t, 500, 0.58, mood="down", head=0.12, front=(-0.6, -1.0), hits=[(tW, 0.3)], ph=1.0)
    cards = ((300, "FAIR?", tQ - 0.1), (780, "UNFAIR?", tQ + 0.15))

    def ui(cr):
        head2(cr, t, "SHANI DEV", t0 + 0.05, "HAD WARNED THEM", tW, big_size=210)
        plate(cr, t, tQ - 0.3, "HIS PUNISHMENT WAS...", 540, 650, 34)
        for cx, txt, tc in cards:
            card(cr, t, tc - 0.25, cx, 790, 0.58, [(txt, 140 if len(txt) < 6 else 120, RED, 4)])
        if t > tY:
            n = int((t - tY) / 0.9)
            k = n % 2
            red_ring(cr, cards[k][0], 794, 232, 96, prog(t, tY + 0.9 * n, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tC, 0.15))


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("s1", None, s_hook, {"z": (1.0, 1.04)}),
    ("s2", None, s_book, {"z": (1.0, 1.03)}),
    ("s3", None, s_split, {"z": (1.0, 1.02)}),
    ("s4", None, s_med, {"z": (1.0, 1.04)}),
    ("s5", None, s_wife, {"z": (1.0, 1.03)}),
    ("s6", None, s_curse, {"z": (1.0, 1.04)}),
    ("s7", None, s_down, {"z": (1.0, 1.03)}),
    ("s8", None, s_birth, {"z": (1.0, 1.03)}),
    ("s9", None, s_ask, {"z": (1.0, 1.03)}),
    ("s10", None, s_insist, {"z": (1.0, 1.03)}),
    ("s11", None, s_glance, {"z": (1.0, 1.05), "focus": (420, 1150)}),
    ("s12", None, s_flash, {"z": (1.0, 1.04)}),
    ("s13", None, s_chaos, {"z": (1.0, 1.03)}),
    ("s14", None, s_north, {"z": (1.0, 1.03)}),
    ("s15", None, s_alive, {"z": (1.0, 1.03)}),
    ("s16", None, s_pcurse, {"z": (1.0, 1.03)}),
    ("s17", None, s_limp, {"z": (1.0, 1.02)}),
    ("s18", None, s_end, {"z": (1.0, 1.03)}),
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
    sepia(cr, out.get("sepia", 0.0))
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
    at the wife's curse, a single hit at the white flash, shimmer as Ganesha lives again, a bell on the closing
    question, then (only where they fit) a bell at Ganesha's birth and a conch at Parvati's curse. Chosen in THAT
    order of importance, each at least SFX_MIN_GAP from every sound already kept (as render_myth.calm_sfx keeps
    them), so the list returned is what plays (about 6 sounds); the bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["s6"]["C"], "conch", 0), (c["s12"]["H"], "hit", 0), (c["s15"]["L"], "shimmer", 0),
            (c["s18"]["C"], "bell", 0), (c["s8"]["B"], "bell", 0), (c["s16"]["C"], "conch", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["s6"]["C"] - 0.3, "dip", 0.45), (c["s12"]["H"] - 0.35, "dip", 0.5), (c["s15"]["L"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
