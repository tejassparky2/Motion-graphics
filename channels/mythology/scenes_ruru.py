"""Scenes for videos/ruru.py: "He gave half his life to bring his dead bride back" (Ruru and Pramadvara, Mahabharata,
Adi Parva 8-12), in Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen,
two-tier headlines and rod-puppet motion as the Jarasandha, Kaikeyi, Lakshman Rekha, Mandhata, Jayadratha and Arjuna
reels, with the cast from ruru_cast. A love story told so a child can follow: one plain label per step, and one device
that carries the idea: Ruru's LIFE BAR (ten glowing windows), full when it first appears, cut in two by the messenger,
half of its light flowing into Pramadvara, and half of it dark for the rest of his life.

Respect and gentleness: the snakebite is a quick dart and a flash, never a wound; Pramadvara sinks down softly and lies
as if asleep, with flowers; Yama is a calm, dignified king who only nods; the staff is raised over the old snake and
stops far short of it; nobody is hurt on screen.

Every frame is a pure function of t. English on-screen text (shared by Hindi and Kannada) except the Sanskrit line under
the sage's teaching in r15, which shows in the viewer's script (अहिंसा परमो धर्मः / ಅಹಿಂಸಾ ಪರಮೋ ಧರ್ಮಃ, shaped by
matplotlib as in scenes_arjuna; without the Nirmala font it is left out). Cues are words of the line in each language
({"hi": ..., "kn": ...}) with a fraction fallback, kept in one table (CUES) that the scenes and sfx() both read, with
minimum gaps so a fast voice can't bunch the beats together.

Shot list (line: what is on the screen)
  r1  HOOK, frame 0: Ruru alone and large, holding out the glowing right half of his life bar toward his bride, who
      lies still on a mat below; above his head only the left half of his bar is left (a dotted outline where the other
      half was): HE GAVE HIS DEAD BRIDE / HALF HIS LIFE (big words in by 0.3 s, underlined on "aadhi"); on "dekar" the
      light streams from his hands to her; HIS BRIDE tag; on "zinda" a burst of light and her eyes open
  r2  THIS IS NOT A / FILM STORY (crossed out); a palm-leaf book rises and opens: MAHABHARATA, BOOK 1: ADI PARVA
      (ringed), SECTIONS 8-12; IT'S WRITTEN IN THE / MAHABHARATA
  r3  Ruru lit first (tag RURU): A SAGE'S SON: / RURU; Pramadvara comes onto the cloth (tag PRAMADVARA): HIS
      BRIDE-TO-BE: / PRAMADVARA; a marigold garland drops between them, petals: THE WEDDING WAS / FIXED
  r4  close on her foot in tall grass (sari hem, anklet, alta): DAYS BEFORE THE / WEDDING; the foot steps in, the grass
      rustles; a coiled snake hidden in the grass is ringed (A HIDDEN SNAKE); the foot comes down on its coil: SHE
      STEPPED ON A / SNAKE
  r5  wide: the snake darts at her ankle, a white flash (no wound): THE SNAKE / BIT HER; her hand goes to her heart, she
      sways and sinks down softly, flowers fall from her hair, the light dims: AND RIGHT THERE, / SHE DIED (in ink)
  r6  night forest; Ruru on his knees, face in his hands, tears falling: IN THE FOREST, RURU / WEPT; he joins his hands
      and looks up; a speech cloud IF I EVER DID GOOD... / BRING HER BACK!
  r7  a shaft of light; the winged messenger of the gods comes down on a cloud of light: A MESSENGER OF THE / GODS;
      above Pramadvara her life bar, every window dark (HER LIFE); he shakes his head: HE SAID: THE DEAD / DON'T COME
      BACK
  r8  he raises a hand: BUT THERE IS / ONE WAY; Ruru's bar (RURU'S LIFE, all ten lit) flies up into his hands, a line
      of light cuts it down the middle and the halves part (HALF / HALF): UNLESS... YOU GIVE / HALF YOUR LIFE
  r9  Ruru nods at once: RURU DIDN'T EVEN / THINK TWICE; he holds out his hands, the right half of his bar goes dark
      window by window and its light streams into Pramadvara, whose bar fills to half: RURU SAID: / MY HALF IS HERS
  r10 Yama (YAMA tag), calm and dignified, nods: YAMA, THE GOD OF DEATH, / SAID YES; light gathers on Pramadvara and
      she rises as if from sleep, eyes opening: AS IF FROM SLEEP, / SHE WOKE UP
  r11 the wedding mandap: garlands drop onto both, petals fall, a small sacred fire: RURU AND PRAMADVARA GOT / MARRIED;
      the lamp dims, Ruru's bar above him, five windows lit and five dark (ringed): BUT HIS OWN LIFE: / HALF
  r12 Ruru, angry, raises his staff; snakes flee from him: THEN RURU MADE A / VOW; card EVERY SNAKE I SEE: / DEAD
  r13 a big old grey-green snake rears up, friendly-eyed (AN OLD SNAKE); Ruru raises the staff over it and stops; it
      speaks: speech cloud WHAT DID I DO? / I HAVE NO VENOM!
  r14 FLASHBACK (sepia): a sage (THE SNAKE, LONG AGO) laughs and dangles a toy snake of grass at his friend, who sits by
      a small fire (HIS FRIEND): THAT SNAKE WAS ONCE A / SAGE, then AS A JOKE, HE SCARED HIS FRIEND / WITH A GRASS
      SNAKE; the friend jumps, then points: THE ANGRY FRIEND / CURSED HIM; card BE A SNAKE / WITHOUT VENOM!
  r15 light gathers on the old snake, a burst, and the white-bearded sage stands in its place: THE SNAKE BECAME A / SAGE
      AGAIN; Ruru lets the staff fall and joins his hands; the sage teaches: note NOT TAKING A LIFE / = / THE HIGHEST
      DHARMA, with अहिंसा परमो धर्मः (Hindi) / ಅಹಿಂಸಾ ಪರಮೋ ಧರ್ಮಃ (Kannada) under it
  r16 WOULD YOU GIVE SOMEONE / HALF YOUR LIFE?; YES / NO cards, a red ring alternating; Ruru and Pramadvara small
      together below, his half-lit bar over him
"""
import math

import cairo

import puppet_core as pc
import ruru_cast as RU
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, text_size
from puppet_core import H, W, depth, keyed, prop, puppet, sway
from scenes_arjuna import HAS_INDIC, card2, cloud_text, ha, indic_surface, point_at
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, man_angles, motes, red_ring, sound_rings, woman_angles
from scenes_jayadratha import NIGHT, flash_at, shroud, tag, tint, title_lift, to_user
from scenes_kaikeyi import ANJALI, card, fig
from scenes_lakshman_rekha import big_x, book, quote_note, sparkle
from scenes_mandhata import aura, beam, burst, lights, mix, warm
from scenes_ravana import dotted, head2
from shots import T, shot_at

MISSES = set()                       # cue words not found in a line (falls back to fractions)
HEART = dict(front=(-0.3, -2.45), backa=(0.12, -0.25))          # a hand at the heart
OFFER = dict(front=(-1.3, -0.3), backa=(-1.2, -0.45))           # both hands held out in front
SANSKRIT = {"hi": "अहिंसा परमो धर्मः", "kn": "ಅಹಿಂಸಾ ಪರಮೋ ಧರ್ಮಃ"}
FLOWERS = ("rr_fl_red", "rr_fl_white", "rr_fl_pink", "rr_fl_gold")


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
    "r1": (("H", {"hi": "आधी", "kn": "ಅರ್ಧ"}, 0.3, (("t0", 0.6),)),
           ("G", {"hi": "देकर", "kn": "ಕೊಟ್ಟು"}, 0.45, (("H", 0.5),)),
           ("D", {"hi": "मरी", "kn": "ಸತ್ತುಹೋದ"}, 0.6, (("G", 0.5),)),
           ("B", {"hi": "दुल्हन", "kn": "ಮದುಮಗಳನ್ನ"}, 0.75, (("D", 0.4),)),
           ("A", {"hi": "ज़िंदा", "kn": "ಬದುಕಿಸಿದ"}, 0.88, (("B", 0.5),))),
    "r2": (("X", {"hi": "नहीं", "kn": "ಅಲ್ಲ"}, 0.3, (("t0", 0.6),)),
           ("M", {"hi": "महाभारत", "kn": "ಮಹಾಭಾರತದ"}, 0.55, (("X", 0.5),)),
           ("P", {"hi": "आदि", "kn": "ಆದಿ"}, 0.75, (("M", 0.5),))),
    "r3": (("R", {"hi": "रुरु", "kn": "ರುರು"}, 0.02, ()),
           ("S", {"hi": "ऋषि", "kn": "ಋಷಿಯ"}, 0.13, (("R", 0.4),)),
           ("W", {"hi": "शादी", "kn": "ಮದುವೆ"}, 0.4, (("S", 0.9),)),
           ("P", {"hi": "प्रमद्वरा", "kn": "ಪ್ರಮದ್ವರಾ"}, 0.55, (("W", 0.5),)),
           ("F", {"hi": "तय", "kn": "ನಿಶ್ಚಯ"}, 0.88, (("P", 0.9),))),
    "r4": (("D", {"hi": "दिन", "kn": "ದಿನ"}, 0.25, (("t0", 0.5),)),
           ("F", {"hi": "पैर", "kn": "ಕಾಲು"}, 0.45, (("D", 0.8),)),
           ("G", {"hi": "घास", "kn": "ಹುಲ್ಲಲ್ಲಿ"}, 0.55, (("F", 0.4),)),
           ("S", {"hi": "साँप", "kn": "ಹಾವಿನ"}, 0.75, (("G", 0.5),)),
           ("T", {"hi": "गया", "kn": "ಬಿತ್ತು"}, 0.92, (("S", 0.5),))),
    "r5": (("B", {"hi": "डस", "kn": "ಕಚ್ಚಿತು"}, 0.2, (("t0", 0.35),)),
           ("P", {"hi": "प्रमद्वरा", "kn": "ಪ್ರಮದ್ವರಾ"}, 0.55, (("B", 0.8),)),
           ("D", {"hi": "मर", "kn": "ಸತ್ತುಹೋದಳು"}, 0.85, (("P", 0.8),))),
    "r6": (("J", {"hi": "जंगल", "kn": "ಕಾಡಿಗೆ"}, 0.1, (("t0", 0.2),)),
           ("C", {"hi": "रोया", "kn": "ಅತ್ತ"}, 0.25, (("J", 0.5),)),
           ("G", {"hi": "पुण्य", "kn": "ಪುಣ್ಯ"}, 0.6, (("C", 0.9),)),
           ("W", {"hi": "वापस", "kn": "ವಾಪಸ್"}, 0.85, (("G", 0.7),))),
    "r7": (("M", {"hi": "दूत", "kn": "ದೂತ"}, 0.2, (("t0", 0.4),)),
           ("L", {"hi": "उम्र", "kn": "ಆಯಸ್ಸು"}, 0.55, (("M", 1.0),)),
           ("N", {"hi": "नहीं", "kn": "ಬರೋದಿಲ್ಲ"}, 0.88, (("L", 0.7),))),
    "r8": (("W", {"hi": "रास्ता", "kn": "ದಾರಿ"}, 0.2, (("t0", 0.3),)),
           ("H", {"hi": "आधी", "kn": "ಅರ್ಧ"}, 0.55, (("W", 0.8),)),
           ("G", {"hi": "दो", "kn": "ಕೊಡು"}, 0.9, (("H", 0.8),))),
    "r9": (("N", {"hi": "सोचा", "kn": "ಯೋಚಿಸಲಿಲ್ಲ"}, 0.35, (("t0", 0.5),)),
           ("M", {"hi": "मेरी", "kn": "ನನ್ನ"}, 0.6, (("N", 0.7),)),
           ("H", {"hi": "उसकी", "kn": "ಅವಳದ್ದು"}, 0.9, (("M", 0.8),))),
    "r10": (("Y", {"hi": "यमराज", "kn": "ಯಮಧರ್ಮ"}, 0.03, ()),
            ("K", {"hi": "हाँ", "kn": "ಒಪ್ಪಿದ"}, 0.2, (("t0", 0.5),)),
            ("P", {"hi": "प्रमद्वरा", "kn": "ಪ್ರಮದ್ವರಾ"}, 0.45, (("K", 0.7),)),
            ("S", {"hi": "नींद", "kn": "ನಿದ್ದೆಯಿಂದ"}, 0.75, (("P", 0.5),)),
            ("U", {"hi": "जागी", "kn": "ಎದ್ದಳು"}, 0.9, (("S", 0.5),))),
    "r11": (("W", {"hi": "शादी", "kn": "ಮದುವೆ"}, 0.15, (("t0", 0.3),)),
            ("B", {"hi": "पर", "kn": "ಆದ್ರೆ"}, 0.45, (("W", 1.0),)),
            ("H", {"hi": "आधी", "kn": "ಅರ್ಧ"}, 0.85, (("B", 0.8),))),
    "r12": (("V", {"hi": "खाई", "kn": "ಪ್ರತಿಜ್ಞೆ"}, 0.25, (("t0", 0.5),)),
            ("S", {"hi": "दिखेगा", "kn": "ಹಾವನ್ನೆಲ್ಲ"}, 0.55, (("V", 0.8),)),
            ("K", {"hi": "मार", "kn": "ಕೊಲ್ತೀನಿ"}, 0.85, (("S", 0.6),))),
    "r13": (("O", {"hi": "बू", "kn": "ಮುದಿ"}, 0.15, (("t0", 0.4),)),
            ("R", {"hi": "डंडा", "kn": "ಕೋಲು"}, 0.3, (("O", 0.5),)),
            ("T", {"hi": "बोला", "kn": "ಹೇಳ್ತು"}, 0.5, (("R", 0.7),)),
            ("W", {"hi": "क्या", "kn": "ನಾನೇನು"}, 0.62, (("T", 0.3),)),
            ("V", {"hi": "मुझमें", "kn": "ವಿಷನೂ"}, 0.82, (("W", 0.8),))),
    "r14": (("S", {"hi": "ऋषि", "kn": "ಋಷಿ"}, 0.15, (("t0", 0.4),)),
            ("J", {"hi": "मज़ाक", "kn": "ತಮಾಷೆಗೆ"}, 0.25, (("S", 0.8),)),
            ("G", {"hi": "घास", "kn": "ಹುಲ್ಲಿನ"}, 0.4, (("J", 0.7),)),
            ("F", {"hi": "डराया", "kn": "ಹೆದರಿಸಿದ್ದ"}, 0.6, (("G", 0.9),)),
            ("C", {"hi": "श्राप", "kn": "ಶಾಪ"}, 0.72, (("F", 0.9),)),
            ("B", {"hi": "बिना", "kn": "ವಿಷ"}, 0.88, (("C", 0.7),))),
    "r15": (("M", {"hi": "मिलते", "kn": "ಭೇಟಿಯಾದ"}, 0.1, (("t0", 0.2),)),
            ("S", {"hi": "ऋषि", "kn": "ಋಷಿ"}, 0.3, (("M", 0.8),)),
            ("L", {"hi": "जान", "kn": "ಜೀವನೂ"}, 0.6, (("S", 1.0),)),
            ("D", {"hi": "धर्म", "kn": "ಧರ್ಮ"}, 0.92, (("L", 0.9),))),
    "r16": (("H", {"hi": "आधी", "kn": "ಅರ್ಧ"}, 0.3, (("t0", 0.5),)),
            ("Y", {"hi": "ना", "kn": "ಹೌದಾ"}, 0.7, (("H", 0.8),)),
            ("C", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.85, (("Y", 0.5),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_ru_cues", None)
    if cache is None:
        cache = {}
        tl._ru_cues = cache
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


# ------------------------------------------------------------------ small helpers


def held_grip(sprite, arm, s, tilt=0.0, grip=0.0, alpha=1.0, blur=0.0, store=None):
    """extra= callback: a staff held upright (+ tilt toward the puppet's front) in a hand whose (upper, fore) angles are
    `arm`; grip moves the staff up through the hand (design units). store gets its 'top' and 'bottom' (device)."""
    rot = -(arm[0] + arm[1]) + tilt

    def fn(cr_):
        cr_.save()
        cr_.translate(4, 150)
        cr_.rotate(rot)
        cr_.scale(s, s)
        cr_.translate(0, -grip)
        pc.paint_part(cr_, sprite, alpha, blur)
        if store is not None:
            store["top"] = cr_.user_to_device(0, -480)
            store["bottom"] = cr_.user_to_device(0, 430)
        cr_.restore()
    return fn


def plate(cr, t, t_in, text, x, y, size=32, color=INK, alpha=1.0, t_out=None):
    """A small parchment label with no rod (for the life bars), centred on (x, y)."""
    p = prog(t, t_in, 0.25)
    if t_out is not None:
        p = min(p, 1 - prog(t, t_out, 0.25))
    a = p * alpha
    if a <= 0.01:
        return
    w, h = text_size(text, size, MONO_FONT, 2)
    bw, bh = w + 40, h + 22
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


def nods(t, times, dur=0.34):
    """A head nodding (0..1 bumps) at each of `times`."""
    v = 0.0
    for tn in times:
        u = (t - tn) / dur
        if 0 < u < 1:
            v += math.sin(math.pi * u)
    return v


def flow(cr, t, t0, t1, p0, p1, n=12, lift=180.0, alpha=1.0, r=26.0, dur=0.9):
    """Sparks of light streaming from p0 to p1 (scene coordinates) along an arc: one leaves every (t1 - t0) / n s
    between t0 and t1, each taking `dur` s."""
    if t < t0 or alpha <= 0.01:
        return
    trail = clamp((t - t0) / 0.5) * (1 - clamp((t - t1 - dur) / 0.4))
    if trail > 0.01:                                    # a warm ribbon of light along the path
        path = [(p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u - lift * 4 * u * (1 - u))
                for u in (i / 40 for i in range(41))]
        cr.save()
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        for lw, col, a in ((30, (1.0, 0.62, 0.15), 0.22), (12, (1.0, 0.72, 0.25), 0.45), (4, (1.0, 0.95, 0.75), 0.9)):
            cr.move_to(*path[0])
            for p in path[1:int(1 + 40 * clamp((t - t0) / 0.5))]:
                cr.line_to(*p)
            cr.set_source_rgba(*col, a * trail * alpha)
            cr.set_line_width(lw)
            cr.stroke()
        cr.restore()
    step = max(0.04, (t1 - t0) / n)
    k = 0
    while True:
        ts = t0 + k * step
        if ts > t1 or ts > t:
            break
        u = (t - ts) / dur
        k += 1
        if not 0 < u < 1:
            continue
        e = u * u * (3 - 2 * u)
        x = p0[0] + (p1[0] - p0[0]) * e + 14 * math.sin(t * 5 + k)
        y = p0[1] + (p1[1] - p0[1]) * e - lift * 4 * e * (1 - e)
        glow(cr, x, y, 80, 0.45 * alpha)
        sparkle(cr, x, y, r * (0.75 + 0.35 * math.sin(math.pi * u)), 0.95 * alpha)


def petals(cr, t, t0, x, y, n=10, spread=600.0, fall=1100.0, dur=3.0, alpha=1.0, seed=0.0, s=0.6, loop=False):
    """Flowers drifting down from around (x, y), one after another from t0 (loop: a steady fall)."""
    for i in range(n):
        ti = t0 + 0.17 * i
        if t < ti:
            continue
        u = (t - ti) / dur
        if loop:
            u %= 1.0
        elif u > 1:
            continue
        xx = x + spread * (((i * 0.618 + seed) % 1.0) - 0.5) + 36 * math.sin(t * 1.7 + i * 2.1)
        yy = y + fall * u
        a = alpha * min(1.0, 4 * u, 4 * (1 - u))
        prop(cr, FLOWERS[i % 4], xx, yy, s, rot=t * 1.3 + i, alpha=a)


# ------------------------------------------------------------------ the life bar


def life_bar(cr, t, x, y, s, lit=10.0, alpha=1.0, halves=(True, True), dl=(0.0, 0.0), dr=(0.0, 0.0, 0.0), seam=0.0,
             glow_a=1.0, ghost=False):
    """The LIFE BAR (ruru_cast rr_bar) centred at (x, y) at scale s: the first `lit` windows glow gold (a fraction
    lights part of a window), the rest are dark. halves = draw the left half (heart + windows 1-5) / the right half;
    dl, dr move the halves apart (dr may turn too); seam 0..1 draws the line of light that cuts it; ghost = a dotted
    outline where a missing right half was. Returns {window: (x, y) on screen, device}."""
    out = {}
    if alpha <= 0.01:
        return out
    r = sway(t, 0.006, 0.35, x * 0.01)
    if glow_a > 0 and lit > 0:
        lx = x + s * (RU.BAR_CELL0 + RU.BAR_STEP * (min(lit, 10) - 1) / 2)
        glow(cr, lx, y, 120 + 300 * s * min(lit, 10) / 10, 0.45 * glow_a * alpha * (0.9 + 0.1 * math.sin(t * 4)))
    for side in (0, 1):
        if not halves[side]:
            continue
        dx, dy = dl if side == 0 else dr[:2]
        cr.save()
        cr.translate(x + dx, y + dy)
        cr.rotate(r + (0.0 if side == 0 else dr[2]))
        cr.scale(s, s)
        if side == 0:
            cr.rectangle(-600, -200, 600 + RU.BAR_SEAM, 400)
        else:
            cr.rectangle(RU.BAR_SEAM, -200, 600, 400)
        cr.clip()
        pc.paint_part(cr, "rr_bar", alpha)
        for i in (range(5) if side == 0 else range(5, 10)):
            cx = RU.BAR_CELL0 + RU.BAR_STEP * i
            lv = clamp(lit - i)
            x0, w = cx - RU.BAR_CW / 2 + 3, RU.BAR_CW - 6
            y0, h = -RU.BAR_CH / 2 + 3, RU.BAR_CH - 6
            if lv < 1:
                cr.rectangle(x0 + w * lv, y0, w * (1 - lv), h)
                cr.set_source_rgba(0.11, 0.06, 0.03, 0.85 * alpha)
                cr.fill()
            if lv > 0:
                g = cairo.LinearGradient(0, y0, 0, y0 + h)
                g.add_color_stop_rgba(0, 1.0, 0.93, 0.62, 0.97 * alpha)
                g.add_color_stop_rgba(1, 1.0, 0.68, 0.18, 0.97 * alpha)
                cr.rectangle(x0, y0, w * lv, h)
                cr.set_source(g)
                cr.fill()
                cr.save()
                cr.set_operator(cairo.OPERATOR_ADD)
                cr.rectangle(x0 + 6, y0 + 6, max(0.0, w * lv - 12), 14)
                cr.set_source_rgba(1.0, 0.95, 0.8, 0.35 * alpha)
                cr.fill()
                cr.restore()
            out[i] = cr.user_to_device(cx, 0)
        cr.restore()
    if ghost:
        pts = [(RU.BAR_SEAM + 6, -80), (440, -80), (470, -60), (470, 60), (440, 80), (RU.BAR_SEAM + 6, 80)]
        u = [(x + s * px * math.cos(r) - s * py * math.sin(r), y + s * px * math.sin(r) + s * py * math.cos(r))
             for px, py in pts]
        dotted(cr, u + [u[0]], 1.0, 15, 4.2, (0.42, 0.26, 0.12), 0.75 * alpha)
    if seam > 0:
        sx = x + s * RU.BAR_SEAM + (dl[0] + dr[0]) / 2
        y0, y1 = y - 115 * s, y + 115 * s
        ye = y0 + (y1 - y0) * clamp(seam)
        cr.save()
        cr.set_operator(cairo.OPERATOR_ADD)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        for lw, a in ((26, 0.18), (12, 0.4), (5, 0.9)):
            cr.move_to(sx, y0)
            cr.line_to(sx, ye)
            cr.set_source_rgba(1.0, 0.9, 0.6, a * alpha)
            cr.set_line_width(lw)
            cr.stroke()
        cr.restore()
        if seam < 1:
            sparkle(cr, sx, ye, 40, alpha)
    return out


# ------------------------------------------------------------------ puppets


def ruru(cr, t, x, s, mood="calm", staff=None, kneel=False, extra=None, store=None, **kw):
    """Ruru (feet on `feet`); staff = (tilt, grip) puts his staff in his front hand; kneel = on one knee."""
    sw = {"rr_ruru_head": "rr_ruru_head" + ("" if mood == "calm" else "_" + mood)}
    ex = dict(extra or {})
    if staff is not None:
        ex["rr_ruru_armF_lo"] = held_grip("rv_staff", kw.get("front", (-0.32, -0.55)), STAFF_S, staff[0], staff[1],
                                          kw.get("alpha", 1.0), kw.get("blur", 0.0), store)
    return fig(cr, RU.RURU, "rr_ruru", t, x, s, swap=sw, extra=ex or None, kneel="rr_ruru_kneel" if kneel else None,
               **kw)


def pram(cr, t, x, s, eyes="open", lie=0.0, lie_dir=-1, feet=FEET, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0,
         hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, ph=0.0, rot=0.0):
    """Pramadvara standing (feet on `feet`), or lying on her back (lie 1): she turns about her hip, which comes down
    to just above the ground, her head toward lie_dir (-1 left: face her right, flip False; 1 right: flip True).
    Returns her points (device)."""
    q = clamp(lie)
    th = lie_dir * math.pi / 2 * q
    hy = (feet - 470 * s) + (360 * s + 4) * q
    ang = woman_angles("rr_pram", t, front, backa, head, hits, ph)
    swap = {"rr_pram_head": "rr_pram_head" + ("" if eyes == "open" else "_" + eyes)}
    return puppet(cr, RU.PRAM, x, hy, s, th + rot + bob_rot(t, ph) * (1 - q), flip, ang, alpha, blur, swap=swap,
                  rods=rods)


LIE = dict(front=(-0.3, -2.3), backa=(0.12, -0.3))              # lying still: a hand on her chest
STAFF_S = 0.62                       # Ruru's staff in his hand (arm units)
STAFF_UP = (-2.2, -0.6)              # his staff arm raised (the hand above his brow, the staff above the hand)
STAFF_DOWN = (-0.4, -0.6)            # carried at his side
GRIP_UP, GRIP_DOWN = 430.0, -250.0   # where the hand holds it: its foot (raised) / its middle-top (carried)


def lying_bride(cr, t, x, ground, s, eyes="shut", alpha=1.0, mat=True, flowers=True, hits=()):
    """Pramadvara lying still on a straw mat, head to the left, a few flowers beside her."""
    if mat:
        prop(cr, "md_mat", x + 20 * s, ground + 2, s * 1.05, alpha=alpha)
    if flowers:
        for i, (dx, dy) in enumerate(((-560, -10), (-430, 6), (520, 0), (600, -14), (-640, 4))):
            prop(cr, FLOWERS[i % 4], x + dx * s, ground + dy * s - 6, 0.9 * s / 0.5, rot=i * 0.9, alpha=alpha)
    return pram(cr, t, x, s, eyes=eyes, lie=1.0, lie_dir=-1, feet=ground, alpha=alpha, hits=hits, **LIE)


def duta(cr, t, x, hip_y, s, front=(-0.6, -0.6), backa=(0.3, -0.35), head=0.0, hits=(), flip=True, alpha=1.0,
         blur=0.0, rods=True, flap=1.0):
    """The messenger of the gods floating on a cloud of light (hip at hip_y, bobbing), wings beating slowly."""
    y = hip_y + 12 * math.sin(t * 1.7)
    if alpha > 0.01:
        glow(cr, x, y - 120 * s, 520 * s + 120, 0.55 * alpha)
        aura(cr, t, x, y - 330 * s, 160 * s, 560 * s, 0.45 * alpha, n=20, spin=0.06)
    ang = man_angles("rr_duta", t, front, backa, head, (0.22, 0.38), hits, 0.7)
    ang["rr_wingF"] = -0.1 + 0.16 * math.sin(t * 2.6) * flap
    ang["rr_wingB"] = -0.02 + 0.12 * math.sin(t * 2.6 - 0.5) * flap
    pts = puppet(cr, RU.DUTA, x, y, s, bob_rot(t, 0.7, 0.01), flip, ang, alpha, blur, rods=rods)
    prop(cr, "rr_lcloud", x, y + 430 * s, s * 0.95, rot=sway(t, 0.01, 0.4, 2.0), alpha=alpha, blur=blur)
    return pts


def yama(cr, t, x, s, nod=0.0, front=(-0.55, -0.85), backa=(0.3, -0.3), head=0.0, alpha=1.0, blur=0.0, **kw):
    """Yama Dharmaraja holding his danda upright; nod 0..1 bows his head."""
    ex = {"rr_yama_armF_lo": held_grip("rr_danda", front, 0.68, 0.0, 120, alpha, blur)}
    return fig(cr, RU.YAMA, "rr_yama", t, x, s, front=front, backa=backa, head=head + 0.2 * nod, extra=ex, alpha=alpha,
               blur=blur, **kw)


def rishi(cr, t, x, s, mood="calm", **kw):
    sw = {"rr_rishi_head": "rr_rishi_head" + ("" if mood == "calm" else "_" + mood)}
    return fig(cr, RU.RISHI, "rr_rishi", t, x, s, swap=sw, **kw)


def khagama(cr, t, x, ground, s, mood="sleep", hop=0.0, front=None, backa=None, head=0.0, hits=(), alpha=1.0,
            blur=0.0, rods=True, ph=0.3):
    """Khagama seated cross-legged (hip SEAT_H above the ground); hop lifts him (a startled jump)."""
    hy = ground - RU.SEAT_H * s - hop
    sw = {"rr_khag_head": "rr_khag_head" + ("" if mood == "sleep" else "_" + mood), "rr_khag_body": "rr_khag_body_sit"}
    ang = man_angles("rr_khag", t, front or ANJALI["front"], backa or ANJALI["backa"], head, (0.0, 0.0), hits, ph)
    return puppet(cr, RU.KHAG, x, hy, s, bob_rot(t, ph, 0.008), False, ang, alpha, blur,
                  hide=("rr_khag_legF", "rr_khag_legB"), swap=sw, rods=rods,
                  extra={"rr_khag_body": lambda cr_: pc.paint_part(cr_, "rr_khag_seat", alpha, blur)})


def fire(cr, t, x, ground, s=1.0, alpha=1.0):
    """A small sacred fire on its altar."""
    glow(cr, x, ground - 190 * s, 300 * s + 60, (0.5 + 0.1 * math.sin(t * 7)) * alpha)
    prop(cr, "altar", x, ground + 14 * s, 0.72 * s, alpha=alpha)
    prop(cr, f"flame{int(t * 10) % 3}", x, ground - 44 * s, 0.5 * s, alpha=alpha)
    lights(cr, t, x, ground - 260 * s, 110 * s, 7, 0.6 * alpha, (1.0, 0.7, 0.3), 0.8)


def trees(cr, t, a, night=True):
    """The forest behind: soft, far trees."""
    if a <= 0.01:
        return
    prop(cr, "tree", 960, FEET + 30, 0.78, rot=sway(t, 0.006, 0.3), alpha=0.6 * a, blur=8)
    prop(cr, "tree", 110, FEET + 30, 0.7, rot=sway(t, 0.006, 0.3, 1.0), alpha=0.55 * a, blur=10, flip=True)
    prop(cr, "tree", 560, FEET + 40, 0.48, rot=sway(t, 0.005, 0.3, 2.0), alpha=0.35 * a, blur=16)


def fireflies(cr, t, a):
    lights(cr, t, 540, 1350, 420, 9, 0.5 * a, (0.85, 1.0, 0.6), 0.18)


def grass(cr, t, x, ground, s, k=0, alpha=1.0, blur=0.0, rustle=0.0, part=0.0):
    """A clump of tall grass swaying (rustle: stronger; part: bends aside, + to the right)."""
    rot = sway(t, 0.02 + 0.05 * rustle, 0.5 + 0.6 * rustle, x * 0.013) + part
    prop(cr, f"rr_grass{k % 3}", x, ground + 8, s, rot=rot, alpha=alpha, blur=blur)


# ------------------------------------------------------------------ snakes


SNAKES = {"old": (RU.SN_OLD, RU.SN_OLD_B, None), "bite": (RU.SN_BITE, RU.SN_BITE_B, RU.SN_BITE_B)}


def _resample(pts, n):
    d = [0.0]
    for a, b in zip(pts, pts[1:]):
        d.append(d[-1] + math.dist(a, b))
    L = d[-1] or 1.0
    out, j = [], 0
    for i in range(n):
        s = L * i / (n - 1)
        while j < len(d) - 2 and d[j + 1] < s:
            j += 1
        seg = (d[j + 1] - d[j]) or 1.0
        f = clamp((s - d[j]) / seg)
        a, b = pts[j], pts[j + 1]
        out.append((a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f))
    return out, L


def snake(cr, t, spine, w0, kind="old", face=1, head=None, alpha=1.0, rods=True, n=72, head_rot=0.0):
    """A leather snake: spine = points on screen from the neck (where the head joins) to the tail tip; w0 = the body's
    width at the neck. The body is one tapered strip, drawn tail first in pieces so its coils lie over each other: a
    pale belly on the ground side, cream bands (the bite snake), holes punched along the back. Then the head sprite at
    the neck, turned along the spine, facing right (face 1) or left (-1). Returns the head's tip and centre."""
    if alpha <= 0.01 or len(spine) < 2:
        return None
    P, L = _resample(spine, n)
    col, belly, bandc = SNAKES[kind]
    Nn, Ww = [], []
    for i in range(n):
        a, b = P[max(0, i - 1)], P[min(n - 1, i + 1)]
        tx, ty = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(tx, ty) or 1.0
        Nn.append((ty / ln * face, -tx / ln * face))
        u = i / (n - 1)
        Ww.append(w0 * (1 + 0.15 * math.sin(math.pi * clamp(u / 0.5))) * (1 - 0.92 * clamp((u - 0.4) / 0.6) ** 1.4))
    bk = [(p[0] - nn[0] * w / 2, p[1] - nn[1] * w / 2) for p, nn, w in zip(P, Nn, Ww)]
    be = [(p[0] + nn[0] * w / 2, p[1] + nn[1] * w / 2) for p, nn, w in zip(P, Nn, Ww)]
    inner = [(p[0] + nn[0] * w * 0.14, p[1] + nn[1] * w * 0.14) for p, nn, w in zip(P, Nn, Ww)]
    period = 1.15 * w0
    lw = max(2.2, 0.065 * w0)
    cr.push_group()
    m = 8
    s = n - 1
    while s > 0:
        a = max(0, s - m - 1)
        idx = range(a, s + 1)
        pc.poly(cr, [bk[i] for i in idx] + [be[i] for i in reversed(idx)])
        cr.set_source_rgb(*col)
        cr.fill()
        if bandc is not None:
            for i in range(a, s):
                if ((L * i / (n - 1)) / period) % 1.0 < 0.3 and i > 2:
                    pc.poly(cr, [bk[i], bk[i + 1], be[i + 1], be[i]])
                    cr.set_source_rgb(*bandc)
                    cr.fill()
        pc.poly(cr, [be[i] for i in idx] + [inner[i] for i in reversed(idx)])
        cr.set_source_rgb(*belly)
        cr.fill()
        for edge in (bk, be):
            cr.move_to(*edge[a])
            for i in range(a + 1, s + 1):
                cr.line_to(*edge[i])
            cr.set_source_rgb(*pc.INK)
            cr.set_line_width(lw)
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            cr.set_line_join(cairo.LINE_JOIN_ROUND)
            cr.stroke()
        holes = [(P[i][0] - Nn[i][0] * Ww[i] * 0.2, P[i][1] - Nn[i][1] * Ww[i] * 0.2) for i in idx
                 if i % 3 == 0 and Ww[i] > 0.35 * w0 and i > 2]
        pc.punch(cr, holes, max(1.6, 0.06 * w0))
        s = a
    if n > 1:                                                     # the tail tip
        cr.new_path()
        cr.arc(P[-1][0], P[-1][1], max(1.5, Ww[-1] / 2), 0, 2 * math.pi)
        cr.set_source_rgb(*col)
        cr.fill()
    pat = cr.pop_group()
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source(pat)
    cr.paint_with_alpha(alpha)
    cr.restore()
    hp = P[0]
    q = P[min(4, n - 1)]
    ang = math.atan2(hp[1] - q[1], hp[0] - q[0])
    hs = w0 / RU.HEAD_W
    name = head or ("rr_snake_" + kind)
    if face > 0:
        prop(cr, name, hp[0], hp[1], hs, rot=ang + head_rot, alpha=alpha)
        ha_ = ang + head_rot
    else:
        prop(cr, name, hp[0], hp[1], hs, rot=ang - math.pi + head_rot, alpha=alpha, flip=True)
        ha_ = ang - head_rot
    if rods:
        mid = P[n // 3]
        pc.rod(cr, mid[0], mid[1], mid[0] + 40, H + 60, alpha=0.45 * alpha)
        pc.rod(cr, hp[0], hp[1] + 20 * hs, hp[0] + 60, H + 60, alpha=0.45 * alpha)
    tip = (hp[0] + 205 * hs * math.cos(ha_), hp[1] + 205 * hs * math.sin(ha_))
    cen = (hp[0] + 100 * hs * math.cos(ha_), hp[1] + 100 * hs * math.sin(ha_))
    return tip, cen


def spine_coil(cx, cy, R, face, head_xy, turns=1.5, flat=0.42, stack=0.0, m=90, arch=0.0):
    """A coiled snake's spine: from the neck at head_xy (it leaves the head going backward, then curves down) onto a
    flattened spiral round (cx, cy) whose inner turns sit `stack` px higher; the tail ends on the outside. arch lifts
    the neck into a hump (a strike)."""
    r0 = 0.42 * R
    a0 = -math.pi / 2 - face * 0.7
    spiral = []
    for i in range(m + 1):
        u = i / m
        a = a0 + face * 2 * math.pi * turns * u
        r = r0 + (R - r0) * u
        spiral.append((cx + r * math.cos(a), cy + flat * r * math.sin(a) - stack * (1 - u)))
    hx, hy = head_xy
    sx, sy = spiral[0]
    c = (hx - face * 0.6 * R, hy + 0.15 * (sy - hy) - arch)
    neck = [((1 - u) ** 2 * hx + 2 * (1 - u) * u * c[0] + u * u * sx,
             (1 - u) ** 2 * hy + 2 * (1 - u) * u * c[1] + u * u * sy) for u in (k / 24 for k in range(24))]
    return neck + spiral


def spine_wave(t, hx, hy, face, length, w0, speed=1.0, lift=0.0, n=48):
    """A snake stretched out behind its head at (hx, hy) (facing `face`), its body waving as it slithers."""
    wl = 6.5 * w0
    amp = 0.8 * w0
    pts = []
    for i in range(n):
        s = length * i / (n - 1)
        a = amp * min(1.0, s / (0.6 * wl))
        y = hy + a * math.sin(2 * math.pi * (s / wl - speed * t * 1.4))
        y -= lift * max(0.0, 1 - s / (0.35 * length)) ** 2
        pts.append((hx - face * s, y))
    return pts


# ------------------------------------------------------------------ r1  hook


HOOK = (290, 0.95, 1890)             # Ruru in the hook: x, scale, feet
BRIDE1 = (770, 1838, 0.58)           # the bride lying below: hip x, ground, scale
HB = 0.5                             # the life bars' scale in the hook


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "r1")
    tH, tG, tD, tB, tA = c["H"], c["G"], c["D"], c["B"], c["A"]
    x, s, feet = HOOK
    bx, by, bs = BRIDE1
    alive = prog(t, tA, 0.5)
    glow(cr, x + 60, feet - 700 * s, 560, 0.42)
    glow(cr, bx - 60, by - 60, 360, 0.3 + 0.45 * alive)
    bp = lying_bride(cr, t, bx, by, bs, eyes="open" if t > tA + 0.2 else "shut", hits=[(tA, 0.4)])
    chest = to_user(cr, bp["chest"])
    pts = ruru(cr, t, x, s, feet=feet, head=0.14, hits=[(tG, 0.3)], ph=1.0, **OFFER)
    hand = to_user(cr, pts["handF"])
    hx, hy = hand[0] + 80, hand[1] - 52
    warm(cr, hx, hy, 300, 0.6)
    life_bar(cr, t, hx - 263 * HB, hy, HB, lit=10, halves=(False, True))
    top = to_user(cr, pts["top"])
    bar_y = top[1] - 95
    life_bar(cr, t, top[0] + 196 * HB, bar_y, HB, lit=5, halves=(True, False), ghost=True)
    flow(cr, t, tG, t1, (hx + 70, hy + 10), (chest[0], chest[1] - 20), n=16, lift=160)
    if t > tA:
        burst(cr, t, chest[0], chest[1] - 30, tA, n=16, rmax=380, alpha=0.8)
        lights(cr, t, chest[0], chest[1] - 60, 160, 9, 0.8 * alive)
    dev_b = cr.user_to_device(bx + 60, by - 170)
    dev_bar = cr.user_to_device(top[0] + 60, bar_y - 74)

    def ui(cr):
        head2(cr, t, "HE GAVE HIS DEAD BRIDE", -1.0, "HALF HIS LIFE", 0.3, big_size=230, ghost=-1.0, under=tH)
        plate(cr, t, tH, "RURU'S LIFE", dev_bar[0], dev_bar[1], 30)
        tag(cr, t, tB, "HIS BRIDE", dev_b[0], dev_b[1], 34)
    return dict(ui=ui, flash=flash_at(t, tH, 0.2) + flash_at(t, tA, 0.35))


# ------------------------------------------------------------------ r2  it's in the Mahabharata


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "r2")
    tX, tM, tP = c["X"], c["M"], c["P"]
    leaves = [(None, [("MAHABHARATA", 92, HEAD_FONT)], 0),
              (tP + 0.1, [([("BOOK 1:", INK), ("ADI PARVA", RED)], 76, HEAD_FONT)], 0),
              (tP + 0.5, [("SECTIONS 8-12", 44, MONO_FONT)], 0)]
    book(cr, t, 540, 940, 0.86, leaves, t_in=t0 + 0.05, t_open=tM, ring=(1, 0, 1, tP + 0.45))

    def ui(cr):
        if t < tM:
            struck = t > tX + 0.25
            box = head2(cr, t, "THIS IS NOT A", t0 + 0.05, "FILM STORY", t0 + 0.35, big_size=210,
                        big_color=(0.42, 0.30, 0.20) if struck else INK)
            if box and t > tX:
                bx, by, bw, bh = box
                big_x(cr, W / 2, by + bh / 2, bw + 60, bh * 0.95, prog(t, tX, 0.3), lw=24)
        else:
            head2(cr, t, "IT'S WRITTEN IN THE", tM - 0.2, "MAHABHARATA", tM + 0.06, big_size=200, under=tP + 0.3)
    return dict(ui=ui, flash=flash_at(t, tM, 0.25) + flash_at(t, tP, 0.2))


# ------------------------------------------------------------------ r3  Ruru and Pramadvara


CP = (290, 800, 0.76, FEET + 140)    # Ruru x, Pramadvara x, scale, feet


def s_couple(cr, t, tl, t0, t1):
    c = cues(tl, "r3")
    tR, tS, tW, tP, tF = c["R"], c["S"], c["W"], c["P"], c["F"]
    rx, px, s, feet = CP
    glow(cr, rx, feet - 700 * s, 430, 0.25 + 0.35 * prog(t, tR, 0.3))
    glow(cr, px, feet - 700 * s, 430, 0.55 * prog(t, tP, 0.3))
    warm(cr, 540, 1180, 380, 0.4 * prog(t, tF, 0.5))
    prop(cr, "ground", W / 2, feet + 6, 0.82)
    b, k, a = depth(t, t0 - 0.2, 0.45)
    joined = keyed(t, [(t0, 0.0), (tF - 0.1, 1.0)], 0.3, 1.3)
    rp = ruru(cr, t, rx, s * k, mood="smile" if t > tF else "calm", feet=feet, alpha=a, blur=b, hits=[(tR, 0.5)],
              front=mix((-0.4, -0.5), (-0.95, -0.5), joined), head=-0.03 * joined, ph=1.0)
    b2, k2, a2 = depth(t, tP - 0.35, 0.45)
    pp = pram(cr, t, px, s * k2 * 0.97, eyes="smile" if t > tF else "open", feet=feet, flip=True, alpha=a2, blur=b2,
              hits=[(tP, 0.5)], front=mix((-0.08, -0.35), (-0.9, -0.5), joined))
    if t > tF - 0.35:                                   # a marigold garland drops between them
        q = back(clamp((t - tF + 0.35) / 0.45), 1.4)
        prop(cr, "kk_garland", 545, 1040 - 420 * (1 - q), 1.25, rot=0.07 * math.sin(t * 2.3) * clamp(q), alpha=clamp(q))
        lights(cr, t, 545, 1200, 150, 8, 0.7 * prog(t, tF, 0.4))
        petals(cr, t, tF, 540, 600, n=12, spread=760, fall=1150, dur=2.6, s=1.0)
    dev_r, dev_p = rp["top"], pp["top"]

    def ui(cr):
        if t < tW:
            head2(cr, t, "A SAGE'S SON:", t0 + 0.05, "RURU", tR + 0.05, big_size=250)
        elif t < tF:
            head2(cr, t, "HIS BRIDE-TO-BE:", tW - 0.15, "PRAMADVARA", tP, big_size=210)
        else:
            head2(cr, t, "THE WEDDING WAS", tF - 0.2, "FIXED", tF, big_size=250, under=tF + 0.4)
        ty_ = min(dev_r[1], dev_p[1]) - 150
        tag(cr, t, tR + 0.15, "RURU", dev_r[0] - 10, ty_, 40)
        tag(cr, t, tP + 0.15, "PRAMADVARA", min(dev_p[0] + 10, 880), ty_, 36)
    return dict(ui=ui, flash=flash_at(t, tR, 0.15) + flash_at(t, tP, 0.2) + flash_at(t, tF, 0.25))


# ------------------------------------------------------------------ r4  her foot in the grass; the hidden snake


G4 = 1650                            # the ground line in the close-up
SN4 = (720, G4 - 28, 160, 64)        # the snake's coil: centre x, y, outer radius, neck width


def s_foot(cr, t, tl, t0, t1):
    c = cues(tl, "r4")
    tD, tF, tG, tS, tT = c["D"], c["F"], c["G"], c["S"], c["T"]
    rustle = prog(t, tG - 0.2, 0.3) * (1 - 0.6 * prog(t, tT + 0.6, 0.6))
    reveal = prog(t, tS - 0.15, 0.35)
    glow(cr, 540, 1250, 620, 0.35)
    for i, (gx, sc) in enumerate(((60, 1.15), (300, 1.05), (560, 1.2), (900, 1.1), (1060, 1.2))):
        grass(cr, t, gx, G4 - 6, sc, i, alpha=0.55, blur=7, rustle=rustle)
    prop(cr, "ground", W / 2, G4, 1.0)
    cx, cy, R, w0 = SN4
    jolt = math.exp(-5 * max(0.0, t - tT)) * (t > tT)
    hx, hy = cx + 10, cy - 190 - 50 * jolt + 6 * math.sin(t * 2.2)
    sn = snake(cr, t, spine_coil(cx, cy, R, -1, (hx, hy), turns=1.6, stack=46), w0, "bite", face=-1,
               head="rr_snake_bite_open" if 0 < t - tT < 0.5 else None, head_rot=-0.1, rods=False)
    if t > tS - 0.2:
        sparkle(cr, sn[1][0] - 20, sn[1][1] - 18, 26 * (0.7 + 0.3 * math.sin(t * 9)), 0.9 * reveal)
    for i, (gx, sc, part) in enumerate(((770, 0.72, 0.4), (960, 0.86, 0.25), (1080, 0.8, 0.2))):
        grass(cr, t, gx, G4 + 4, sc, i + 1, rustle=rustle, part=part * reveal)
    # her foot: steps in from the left, raised, and comes down on the coil
    t_in, t_dn = tF - 0.15, tT - 0.12
    if t > t_in:
        u = clamp((t - t_in) / max(0.5, t_dn - t_in))
        fx = -420 + (250 + 420) * ease(u)
        lift = 110 * (1 - ease(clamp((t - t_dn) / 0.18))) + 30 * math.sin(math.pi * u) * (u < 1)
        fr = -0.08 * (1 - ease(clamp((t - t_dn) / 0.18)))
        cr.push_group()                                 # the sari fades up into the light (no hard top edge)
        prop(cr, "rr_foot", fx, G4 - lift, 1.0, rot=fr)
        pat = cr.pop_group()
        yt = G4 - lift - 690
        g = cairo.LinearGradient(0, yt, 0, yt + 260)
        g.add_color_stop_rgba(0, 0, 0, 0, 0.0)
        g.add_color_stop_rgba(1, 0, 0, 0, 1.0)
        cr.save()
        cr.set_operator(cairo.OPERATOR_MULTIPLY)
        cr.set_source(pat)
        cr.mask(g)
        cr.restore()
        pc.rod(cr, fx + 90, G4 - lift - 400, fx + 140, H + 60, alpha=0.4)
    grass(cr, t, -30, G4 + 12, 0.7, 2, rustle=rustle)
    dev_s = cr.user_to_device(cx, cy - 70)

    def ui(cr):
        if t < tT:
            head2(cr, t, "DAYS BEFORE THE", t0 + 0.05, "WEDDING", tD, big_size=250)
        else:
            head2(cr, t, "SHE STEPPED ON A", tT - 0.1, "SNAKE", tT + 0.05, big_size=250, under=tT + 0.4)
        if t > tS:
            red_ring(cr, dev_s[0], dev_s[1], 230, 175, prog(t, tS + 0.05, 0.45), 9)
        tag(cr, t, tS + 0.2, "A HIDDEN SNAKE", min(dev_s[0] + 40, 860), dev_s[1] - 300, 34, t_out=tT + 0.3)
    return dict(ui=ui, flash=flash_at(t, tS, 0.15) + flash_at(t, tT, 0.3))


# ------------------------------------------------------------------ r5  the bite; she sinks down


PR5 = (600, 0.74, FEET + 100)        # Pramadvara: hip x, scale, ground
SN5 = (300, FEET + 100 - 20, 118, 50)  # the snake's coil: centre x, y, outer radius, neck width


def bun_xy(x, ground, s, q, lie_dir, flip):
    """Where Pramadvara's hair bun is (scene) for pram(..., lie=q)."""
    th = lie_dir * math.pi / 2 * q
    hy = (ground - 470 * s) + (360 * s + 4) * q
    lx, ly = (60 if flip else -60), -410
    return x + s * (lx * math.cos(th) - ly * math.sin(th)), hy + s * (lx * math.sin(th) + ly * math.cos(th))


def s_bite(cr, t, tl, t0, t1):
    c = cues(tl, "r5")
    tB, tP, tD = c["B"], c["P"], c["D"]
    px, ps, pg = PR5
    sink = ease(clamp((t - tP - 0.05) / max(0.9, tD - tP + 0.15)))
    dim = prog(t, tD - 0.3, 1.0)
    glow(cr, px - 80, pg - 500, 600, 0.45 - 0.2 * dim)
    for i, (gx, sc) in enumerate(((80, 0.8), (330, 0.75), (860, 0.85), (1040, 0.8))):
        grass(cr, t, gx, pg - 4, sc, i, alpha=0.5, blur=8)
    prop(cr, "ground", W / 2, pg + 6, 0.82)
    cx, cy, R, w0 = SN5
    tgt = (px - 120 * ps, pg - 120)
    hit = t > tB
    reel = keyed(t, [(t0, 0.0), (tB + 0.1, 1.0)], 0.25, 1.6)
    fr = mix((-0.08, -0.35), HEART["front"], reel)
    sway_ = 0.05 * math.sin((t - tB) * 4.5) * prog(t, tB, 0.3) * (1 - sink)
    pp = pram(cr, t, px, ps, eyes="shut" if sink > 0.35 else "open", lie=sink, lie_dir=1, feet=pg, flip=True,
              front=fr, backa=(0.2, -0.3), head=-0.12 * reel * (1 - sink), hits=[(tB, 0.8)], rot=sway_)
    rest = (cx + 70, cy - 210 + 6 * math.sin(t * 2.4))  # reared up, looking at her foot; then the dart
    go = ease(clamp((t - tB + 0.14) / 0.12)) * (1 - ease(clamp((t - tB - 0.12) / 0.32)))
    hx, hy = rest[0] + (tgt[0] - rest[0]) * go, rest[1] + (tgt[1] - rest[1]) * go
    leave = prog(t, tB + 0.8, 0.6)
    if leave < 1:
        snake(cr, t, spine_coil(cx - 160 * leave, cy, R, 1, (hx - 160 * leave, hy), turns=1.5, stack=40,
                                arch=170 * go), w0, "bite", face=1,
              head="rr_snake_bite_open" if tB - 0.2 < t < tB + 0.35 else None, alpha=1 - leave, rods=False,
              head_rot=0.25 * (1 - go) + 0.35 * go)
    for i in range(6):                                  # flowers slip from her hair as she sinks
        ti = tP + 0.25 + 0.22 * i
        if t < ti:
            continue
        q = clamp((ti - tP - 0.05) / max(0.9, tD - tP + 0.15))
        sx, sy = bun_xy(px, pg, ps, ease(q), 1, True)
        u = clamp((t - ti) / 1.1)
        yy = sy + (pg - 8 - sy) * (u * u)
        xx = sx + 60 * (i % 3 - 1) * u + 18 * math.sin(t * 2 + i) * (1 - u)
        prop(cr, FLOWERS[i % 4], xx, yy, 0.85, rot=i + 2.5 * u)
    if hit and t < tB + 0.6:                            # a white flash where it struck (no wound)
        u = (t - tB) / 0.6
        sparkle(cr, tgt[0], tgt[1] - 10, 90 * math.sin(math.pi * u) + 10, 1 - u, (1.0, 0.97, 0.88))
        glow(cr, tgt[0], tgt[1], 180, 0.7 * (1 - u))
    if t > tD:
        glow(cr, px + 120, pg - 60, 300, 0.25 * dim)

    def ui(cr):
        if t < tD:
            head2(cr, t, "THE SNAKE", t0 + 0.05, "BIT HER", tB + 0.02, big_size=250)
        else:
            head2(cr, t, "AND RIGHT THERE,", tD - 0.2, "SHE DIED", tD, big_size=250, big_color=INK)
    return dict(ui=ui, eve=0.25 * dim, night=0.12 * dim, lift=1.0, flash=flash_at(t, tB, 0.4))


# ------------------------------------------------------------------ r6  he weeps in the forest and prays


WEEP = (500, 0.86, FEET + 110)


def s_weep(cr, t, tl, t0, t1):
    c = cues(tl, "r6")
    tJ, tC, tG, tW = c["J"], c["C"], c["G"], c["W"]
    dark = prog(t, t0, 0.6)
    trees(cr, t, prog(t, tJ - 0.3, 0.6))
    fireflies(cr, t, prog(t, tJ, 0.8))
    prop(cr, "ground", W / 2, FEET + 116, 0.82)
    x, s, feet = WEEP
    glow(cr, x, feet - 500 * s, 420, 0.4)
    cry = keyed(t, [(t0, 0.0), (tC - 0.15, 1.0)], 0.3, 1.3)
    pray = keyed(t, [(t0, 0.0), (tG - 0.15, 1.0)], 0.35, 1.3)
    fr = mix(mix((-0.25, -0.4), (-0.62, -2.55), cry), ANJALI["front"], pray)
    ba = mix(mix((0.2, -0.3), (-0.5, -2.35), cry), ANJALI["backa"], pray)
    sob = 0.012 * math.sin(t * 9) * cry * (1 - 0.6 * pray)
    rp = ruru(cr, t, x, s, mood="weep" if t > tC - 0.2 else "calm", kneel=True, feet=feet, front=fr, backa=ba,
              head=0.26 * cry * (1 - pray) - 0.2 * pray, rot=sob, hits=[(tC, 0.4), (tG, 0.3)], ph=1.0)
    eye = to_user(cr, rp["head"])
    if t > tC:                                          # tears falling
        for i in range(8):
            ti = tC + 0.1 + 0.62 * i
            u = (t - ti) / 0.9
            if 0 < u < 1:
                prop(cr, "rr_tear", eye[0] + 30 + 8 * (i % 2), eye[1] + 40 + 260 * u * u, 0.9, alpha=1 - u * u)

    def ui(cr):
        head2(cr, t, "IN THE FOREST, RURU", t0 + 0.05, "WEPT", tC, big_size=260)
        cloud_text(cr, t, 730, 840, 0.82, [("IF I EVER DID GOOD...", 64, INK, -52, tG),
                                           ("BRING HER BACK!", 92, RED, 44, tW)], t_in=tG - 0.25)
    return dict(ui=ui, night=0.32 * dark, lift=1.0, flash=flash_at(t, tW, 0.2))


# ------------------------------------------------------------------ r7  the messenger of the gods


DU7 = (590, 0.62, 1010)              # the messenger: x, scale, hip y when he has come down
RU7 = (200, 0.6, FEET + 110)         # Ruru kneeling
PR7 = (800, FEET + 125, 0.5)         # Pramadvara lying: hip x, ground, scale


def s_duta(cr, t, tl, t0, t1):
    c = cues(tl, "r7")
    tM, tL, tN = c["M"], c["L"], c["N"]
    trees(cr, t, 1.0)
    light = prog(t, tM - 0.4, 0.6)
    dx_, ds, dy = DU7
    beam(cr, dx_, 260, 560, FEET, light * 0.85)
    prop(cr, "ground", W / 2, FEET + 131, 0.82)
    bx, bg, bs = PR7
    bp = lying_bride(cr, t, bx, bg, bs)
    rx, rs, rf = RU7
    look = keyed(t, [(t0, 0.0), (tM, 1.0)], 0.35, 1.3)
    ruru(cr, t, rx, rs, mood="weep" if t < tM else "calm", kneel=True, feet=rf, front=ANJALI["front"],
         backa=ANJALI["backa"], head=0.22 * (1 - look) - 0.24 * look, hits=[(tM, 0.3)], ph=1.0)
    arrive = ease((t - tM + 0.35) / 0.9)
    b, k, a = depth(t, tM - 0.35, 0.9)
    shake = 0.13 * math.sin(2 * math.pi * 2.6 * (t - tN)) * math.exp(-1.6 * (t - tN)) if t > tN else 0.0
    if t > tM - 0.4:
        duta(cr, t, dx_, dy - 700 * (1 - arrive), ds * k, front=mix((-0.6, -0.6), (-1.0, -0.9), prog(t, tL, 0.4)),
             head=0.08 + shake, alpha=a, blur=b, hits=[(tL, 0.3)])
    chest = to_user(cr, bp["chest"])
    bar_x, bar_y = chest[0] + 60, chest[1] - 170
    if t > tL - 0.1:
        life_bar(cr, t, bar_x, bar_y, 0.3, lit=0, alpha=prog(t, tL - 0.1, 0.3))
    dev_bar = cr.user_to_device(bar_x, bar_y - 48)

    def ui(cr):
        if t < tL:
            head2(cr, t, "A MESSENGER OF THE", t0 + 0.05, "GODS", tM, big_size=260)
        else:
            head2(cr, t, "HE SAID: THE DEAD", tL - 0.2, "DON'T COME BACK", tN, big_size=200, under=tN + 0.4)
        plate(cr, t, tL, "HER LIFE", dev_bar[0], dev_bar[1], 26)
    return dict(ui=ui, night=0.26, lift=1.0, flash=flash_at(t, tM, 0.35) + flash_at(t, tN, 0.15))


# ------------------------------------------------------------------ r8  "give half your life": the bar is cut


DU8 = (840, 0.74, 1230)              # the messenger, facing left: x, scale, hip y
BAR8 = (440, 1000, 0.56)             # the bar held out in front of him: centre x, y, scale


def s_split(cr, t, tl, t0, t1):
    c = cues(tl, "r8")
    tW, tH, tG = c["W"], c["H"], c["G"]
    trees(cr, t, 0.7)
    glow(cr, 560, 900, 620, 0.45)
    prop(cr, "ground", W / 2, FEET + 131, 0.82)
    rp = ruru(cr, t, 170, 0.5, kneel=True, feet=FEET + 120, front=ANJALI["front"], backa=ANJALI["backa"], head=-0.22,
              ph=1.0)
    t_fly = tH - 0.4
    hold = keyed(t, [(t0, 0.0), (t_fly, 1.0)], 0.35, 1.2)
    one = keyed(t, [(t0, 0.0), (tW - 0.1, 1.0)], 0.3, 1.4) * (1 - hold)
    dx_, ds, dy = DU8
    fr = mix(mix((-0.6, -0.6), (-2.7, -0.35), one), (-1.85, -0.1), hold)
    ba = mix((0.3, -0.35), (-1.7, -0.25), hold)
    duta(cr, t, dx_, dy, ds, front=fr, backa=ba, head=0.04 * hold, hits=[(tW, 0.4)])
    if t > t_fly - 0.05:
        u = ease(clamp((t - t_fly) / 0.55))
        top = to_user(cr, rp["top"])
        x0, y0, s0 = top[0] + 20, top[1] - 90, 0.26
        bx, by, bsc = BAR8
        x = x0 + (bx - x0) * u
        y = y0 + (by - y0) * u - 120 * math.sin(math.pi * u)
        sc = s0 + (bsc - s0) * u
        part = ease(clamp((t - tG) / 0.45))
        seam = clamp((t - tH - 0.25) / 0.45)
        life_bar(cr, t, x, y, sc, lit=10, dl=(-34 * part, 0.0), dr=(34 * part, 6 * part, 0.04 * part), seam=seam)
        if u < 1:
            lights(cr, t, x, y, 160, 8, 0.8)
        if 0 < t - tG < 0.6:
            burst(cr, t, x + sc * RU.BAR_SEAM, y, tG, n=12, rmax=260, alpha=0.6)
        dev_bar = cr.user_to_device(x - 60 * sc, y - 100 * sc - 30)
        dev_l = cr.user_to_device(x + sc * (-170) - 34 * part, y + 100 * sc + 30)
        dev_r = cr.user_to_device(x + sc * 263 + 34 * part, y + 100 * sc + 36)
    else:
        dev_bar = dev_l = dev_r = None

    def ui(cr):
        if t < tH:
            head2(cr, t, "BUT THERE IS", t0 + 0.05, "ONE WAY", tW, big_size=250)
        else:
            head2(cr, t, "UNLESS... YOU GIVE", tH - 0.2, "HALF YOUR LIFE", tH + 0.25, big_size=210, under=tG + 0.2)
        if dev_bar is not None:
            plate(cr, t, t_fly + 0.4, "RURU'S LIFE", dev_bar[0], dev_bar[1], 30)
            plate(cr, t, tG + 0.15, "HALF", dev_l[0], dev_l[1], 30)
            plate(cr, t, tG + 0.25, "HALF", dev_r[0], dev_r[1], 30)
    return dict(ui=ui, night=0.16, lift=1.0, flash=flash_at(t, tH + 0.25, 0.25) + flash_at(t, tG, 0.25))


# ------------------------------------------------------------------ r9  "my half is hers": the light flows to her


RU9 = (250, 0.72, FEET + 120)
PR9 = (780, FEET + 135, 0.55)
BAR9 = (310, 0.44)                   # Ruru's bar: x, scale (y from his head)


def s_give(cr, t, tl, t0, t1):
    c = cues(tl, "r9")
    tN, tM, tH = c["N"], c["M"], c["H"]
    glow(cr, 540, 1100, 640, 0.42)
    prop(cr, "ground", W / 2, FEET + 141, 0.82)
    bx, bg, bs = PR9
    dur = max(0.7, tH - tM)
    drain = clamp((t - tM) / dur)
    fill = clamp((t - tM - 0.3) / dur)
    glow(cr, bx - 80, bg - 60, 320, 0.2 + 0.5 * fill)
    bp = lying_bride(cr, t, bx, bg, bs)
    give = keyed(t, [(t0, 0.0), (tM - 0.1, 1.0)], 0.35, 1.3)
    x, s, feet = RU9
    rp = ruru(cr, t, x, s, mood="calm", feet=feet, front=mix((-0.35, -0.5), OFFER["front"], give),
              backa=mix((0.25, -0.3), OFFER["backa"], give), head=0.16 * nods(t, (tN, tN + 0.4)) + 0.06 * give,
              hits=[(tN, 0.3), (tM, 0.3)], ph=1.0)
    top = to_user(cr, rp["top"])
    bxr, bsr = BAR9
    bar_y = top[1] - 170
    cells = life_bar(cr, t, bxr, bar_y, bsr, lit=10 - 5 * drain, dl=(-10.0, 0.0), dr=(10.0, 0.0, 0.0), seam=1.0)
    chest = to_user(cr, bp["chest"])
    hb_x, hb_y = chest[0] + 70, chest[1] - 180
    life_bar(cr, t, hb_x, hb_y, 0.34, lit=5 * fill)
    if 7 in cells:
        src = to_user(cr, cells[7])
        flow(cr, t, tM, tM + dur, src, (chest[0], chest[1] - 30), n=18, lift=260, dur=0.6)
    if fill > 0:
        lights(cr, t, chest[0], chest[1] - 40, 140, 8, 0.7 * fill)
    dev_rb = cr.user_to_device(bxr, bar_y - 60)
    dev_hb = cr.user_to_device(hb_x, hb_y - 48)

    def ui(cr):
        if t < tM:
            head2(cr, t, "RURU DIDN'T EVEN", t0 + 0.05, "THINK TWICE", tN, big_size=230)
        else:
            head2(cr, t, "RURU SAID:", tM - 0.2, "MY HALF IS HERS", tM + 0.1, big_size=210, under=tH)
        plate(cr, t, t0 + 0.1, "RURU'S LIFE", dev_rb[0], dev_rb[1], 28)
        plate(cr, t, t0 + 0.3, "HER LIFE", dev_hb[0], dev_hb[1], 26)
    return dict(ui=ui, night=0.1, lift=1.0, flash=flash_at(t, tM, 0.2) + flash_at(t, tH, 0.3))


# ------------------------------------------------------------------ r10  Yama says yes; she wakes


YM10 = (270, 0.8, FEET + 150)
PR10 = (760, FEET + 150, 0.62)


def s_wake(cr, t, tl, t0, t1):
    c = cues(tl, "r10")
    tY, tK, tP, tS, tU = c["Y"], c["K"], c["P"], c["S"], c["U"]
    x, s, feet = YM10
    glow(cr, x, feet - 760 * s, 520, 0.42)
    aura(cr, t, x - 10, feet - 434 * s - 330 * s, 150, 470, 0.25, n=16, spin=0.03, col=(0.95, 0.45, 0.25))
    prop(cr, "ground", W / 2, feet + 6, 0.82)
    b, k, a = depth(t, t0 - 0.15, 0.5)
    yp = yama(cr, t, x, s * k, nod=nods(t, (tK,), 0.6), feet=feet, alpha=a, blur=b, ph=0.6)
    bx, bg, bs = PR10
    rise = ease(clamp((t - tS) / max(0.9, tU - tS + 0.45)))
    lit = prog(t, tP - 0.1, 0.6)
    glow(cr, bx, bg - 300 - 300 * rise, 380, 0.3 + 0.45 * lit)
    warm(cr, bx, bg - 250 - 300 * rise, 330, 0.5 * lit)
    prop(cr, "md_mat", bx + 10, bg + 2, bs * 1.05, alpha=1 - 0.6 * rise)
    pram(cr, t, bx, bs, eyes="shut" if rise < 0.75 else ("smile" if t > tU + 0.4 else "open"), lie=1 - rise,
         lie_dir=1, flip=True, feet=bg, front=mix(LIE["front"], (-0.35, -0.5), rise), backa=LIE["backa"],
         hits=[(tU, 0.4)])
    lights(cr, t, bx, bg - 200 - 300 * rise, 230, 12, 0.8 * lit)
    dev_y = yp["top"]

    def ui(cr):
        if t < tP:
            head2(cr, t, "YAMA, THE GOD OF DEATH,", t0 + 0.05, "SAID YES", tK, big_size=240)
        else:
            head2(cr, t, "AS IF FROM SLEEP,", tP - 0.15, "SHE WOKE UP", tU, big_size=230, under=tU + 0.4)
        tag(cr, t, tY + 0.3, "YAMA", dev_y[0], dev_y[1] - 110, 40)
    return dict(ui=ui, flash=flash_at(t, tK, 0.15) + flash_at(t, tU, 0.35))


# ------------------------------------------------------------------ r11  the wedding; his life stays at half


MANDAP = (540, FEET + 140, 0.72)


def s_wedding(cr, t, tl, t0, t1):
    c = cues(tl, "r11")
    tW, tB, tH = c["W"], c["B"], c["H"]
    mx, mf, ms = MANDAP
    dim = prog(t, tB - 0.1, 0.5)
    glow(cr, 540, 1250, 600, 0.45)
    prop(cr, "rr_mandap", mx, mf, ms, rot=sway(t, 0.003, 0.3), alpha=1 - 0.5 * dim, blur=6 * dim)
    prop(cr, "ground", W / 2, mf + 6, 0.82)
    fire(cr, t, 540, mf, 0.42, alpha=1 - 0.4 * dim)
    s = 0.62
    g = keyed(t, [(t0, 0.0), (tW - 0.1, 1.0)], 0.3, 1.2)
    rp = ruru(cr, t, 370, s, mood="smile" if t < tB else "calm", feet=mf, front=mix((-0.4, -0.5), ANJALI["front"], g),
              backa=mix((0.25, -0.3), ANJALI["backa"], g), ph=1.0, hits=[(tW, 0.3)])
    pp = pram(cr, t, 712, s * 0.97, eyes="smile", feet=mf, flip=True, front=mix((-0.08, -0.35), (-0.75, -1.8), g),
              backa=mix((0.15, -0.2), (-0.8, -1.75), g), hits=[(tW, 0.3)], blur=4 * dim, alpha=1 - 0.25 * dim)
    for pts_, dx in ((rp, 4), (pp, -4)):               # garlands drop round their necks
        ch = to_user(cr, pts_["chest"])
        q = back(clamp((t - tW + 0.2) / 0.4), 1.3)
        if q > 0:
            prop(cr, "kk_garland", ch[0] + dx, ch[1] - 92 * s - 260 * (1 - q), 0.55, alpha=clamp(q * 2))
    petals(cr, t, tW, 540, 640, n=14, spread=820, fall=1150, dur=3.2, s=1.0)
    top = to_user(cr, rp["top"])
    bs_ = 0.46
    bar_x, bar_y = 410, top[1] - 150
    cells = {}
    if t > tB - 0.2:
        cells = life_bar(cr, t, bar_x, bar_y, bs_, lit=5, alpha=prog(t, tB - 0.2, 0.35))
    dev_bar = cr.user_to_device(bar_x - 60 * bs_, bar_y - 100 * bs_ - 28)
    dev_half = cr.user_to_device(bar_x + bs_ * 263, bar_y)

    def ui(cr):
        if t < tB:
            head2(cr, t, "RURU AND PRAMADVARA GOT", t0 + 0.05, "MARRIED", tW + 0.05, big_size=250)
        else:
            head2(cr, t, "BUT HIS OWN LIFE:", tB - 0.15, "HALF", tH, big_size=260, under=tH + 0.4)
        if cells:
            plate(cr, t, tB, "RURU'S LIFE", dev_bar[0], dev_bar[1], 30)
            if t > tH:
                red_ring(cr, dev_half[0], dev_half[1], 140, 56, prog(t, tH + 0.05, 0.45), 8)
    return dict(ui=ui, eve=0.2 * dim, flash=flash_at(t, tW, 0.25) + flash_at(t, tH, 0.2))


# ------------------------------------------------------------------ r12  the vow; snakes flee


RU12 = (330, 0.84, FEET + 130)
FLEE = ((520, FEET + 115, 40, 330, 0.0), (460, FEET + 50, 32, 290, 0.25), (580, FEET + 175, 46, 370, 0.12))


def s_vow(cr, t, tl, t0, t1):
    c = cues(tl, "r12")
    tV, tS, tK = c["V"], c["S"], c["K"]
    glow(cr, 420, 1200, 600, 0.4)
    prop(cr, "ground", W / 2, FEET + 136, 0.82)
    x, s, feet = RU12
    up = keyed(t, [(t0, 0.0), (tV - 0.1, 1.0)], 0.3, 1.4)
    shake_ = keyed(t, [(t0, 0.0), (tK - 0.05, 1.0), (tK + 0.35, 0.0)], 0.18, 1.6)
    fr = mix(STAFF_DOWN, STAFF_UP, up)
    ruru(cr, t, x, s, mood="angry" if t > tV - 0.15 else "calm", feet=feet, front=fr, backa=(0.3, -0.5),
         staff=(-0.45 * up + 0.15 * shake_, GRIP_DOWN + (GRIP_UP - 150 - GRIP_DOWN) * up), hits=[(tV, 0.6), (tK, 0.5)],
         ph=1.0, head=-0.05 * up)
    for i, (x0, y0, w0, v, dl) in enumerate(FLEE):     # snakes slither away from him
        ts = tS - 0.25 + dl
        if t < ts:
            continue
        hx = x0 + v * (t - ts) + 60
        snake(cr, t, spine_wave(t * 1.4 + i, hx, y0, 1, 9.5 * w0, w0, speed=1.6), w0, "bite", face=1,
              alpha=prog(t, ts, 0.25), rods=False)

    def ui(cr):
        head2(cr, t, "THEN RURU MADE A", t0 + 0.05, "VOW", tV, big_size=260)
        card2(cr, t, tS - 0.25, 770, 900, 0.62, [("EVERY SNAKE I SEE:", 66, INK, -56, tS),
                                                ("DEAD", 118, RED, 38, tK)])
    return dict(ui=ui, flash=flash_at(t, tV, 0.3) + flash_at(t, tK, 0.25))


# ------------------------------------------------------------------ r13  the old snake speaks


SN13 = (250, FEET + 70, 160, 78)     # the old snake's coil: centre x, y, outer radius, neck width
SN13_HEAD = (390, FEET - 340)        # where its head rears up to
RU13 = (800, 0.8, FEET + 150)        # Ruru, facing left


def old_snake(cr, t, tl, talk_from=None, alpha=1.0, glow_a=0.0, rods=True):
    """The old Dundubha coiled on the left, its head reared up toward Ruru; it speaks from talk_from."""
    cx, cy, R, w0 = SN13
    hx, hy = SN13_HEAD
    hy += 8 * math.sin(t * 1.9)
    talk = talk_from is not None and t > talk_from and (math.sin((t - talk_from) * 2 * math.pi * 2.6) > 0.1)
    if glow_a > 0:
        glow(cr, cx + 40, cy - 160, 420, glow_a)
        aura(cr, t, cx + 40, cy - 180, 120, 420, 0.6 * glow_a, n=18, spin=0.1)
    return snake(cr, t, spine_coil(cx, cy, R, 1, (hx, hy), turns=1.55, stack=60), w0, "old", face=1,
                 head="rr_snake_old_talk" if talk else None, head_rot=-0.12, alpha=alpha, rods=rods)


def s_old(cr, t, tl, t0, t1):
    c = cues(tl, "r13")
    tO, tR, tT, tW, tV = c["O"], c["R"], c["T"], c["W"], c["V"]
    glow(cr, 540, 1250, 620, 0.42)
    prop(cr, "ground", W / 2, FEET + 156, 0.82)
    a = prog(t, tO - 0.4, 0.4)
    sn = old_snake(cr, t, tl, talk_from=tT, alpha=a)
    x, s, feet = RU13
    up = keyed(t, [(t0, 0.0), (tR - 0.1, 1.0)], 0.3, 1.4)
    freeze = keyed(t, [(t0, 0.0), (tT, 1.0)], 0.25, 1.6)
    fr = mix(STAFF_DOWN, STAFF_UP, up)
    ruru(cr, t, x, s, mood="shock" if t > tT + 0.05 else ("angry" if t > tR - 0.2 else "calm"), feet=feet, flip=True,
         front=fr, backa=(0.3, -0.5), staff=(-0.42 * up - 0.06 * freeze, GRIP_DOWN + (GRIP_UP - GRIP_DOWN) * up),
         head=-0.05 * up - 0.06 * freeze, rot=-0.03 * freeze, hits=[(tR, 0.5), (tT, 0.4)], ph=1.0)
    dev_s = cr.user_to_device(*(sn[1] if sn else (300, 1300)))

    def ui(cr):
        if t < tT:
            head2(cr, t, "ONE DAY HE RAISED HIS STAFF AT AN", t0 + 0.05, "OLD SNAKE", tO, big_size=230)
        else:
            head2(cr, t, "THE OLD SNAKE SPOKE:", tT - 0.1, None, 0.0)
        tag(cr, t, tO + 0.15, "AN OLD SNAKE", max(200, dev_s[0] - 80), dev_s[1] - 170, 34, t_out=tW - 0.2)
        cloud_text(cr, t, 440, 880, 0.74, [("WHAT DID I DO?", 86, INK, -48, tW),
                                           ("I HAVE NO VENOM!", 76, RED, 46, tV)], t_in=tW - 0.25)
    return dict(ui=ui, flash=flash_at(t, tR, 0.15) + flash_at(t, tV, 0.25))


# ------------------------------------------------------------------ r14  flashback: the joke and the curse


KG14 = (370, 0.8, FEET + 120)        # Khagama seated: x, scale, ground
RS14 = (820, 0.8, FEET + 120)        # the joking sage, facing left


def sepia(cr, a):
    """The flashback look: the colours drained to a warm brown, darker edges, a thin frame."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_HSL_SATURATION)
    cr.set_source_rgba(0.5, 0.5, 0.5, 0.55 * a)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source_rgba(1.0, 0.90, 0.72, 0.5 * a)
    cr.paint()
    cr.restore()
    shroud(cr, 540, 1000, 1500, 0.22 * a)
    cr.save()
    cr.set_source_rgba(0.25, 0.14, 0.06, 0.55 * a)
    cr.set_line_width(5)
    cr.rectangle(28, 28, W - 56, H - 56)
    cr.stroke()
    cr.set_line_width(2)
    cr.rectangle(42, 42, W - 84, H - 84)
    cr.stroke()
    cr.restore()


def s_flash(cr, t, tl, t0, t1):
    c = cues(tl, "r14")
    tS, tJ, tG, tF, tC, tB = c["S"], c["J"], c["G"], c["F"], c["C"], c["B"]
    glow(cr, 540, 1250, 640, 0.4)
    prop(cr, "ground", W / 2, FEET + 126, 0.82)
    fire(cr, t, 135, FEET + 120, 0.5)
    kx, ks, kg = KG14
    sx, ss, sf = RS14
    jump = math.sin(math.pi * clamp((t - tF) / 0.55)) * 160 if t > tF else 0.0
    startled = keyed(t, [(t0, 0.0), (tF - 0.05, 1.0), (tC - 0.2, 0.0)], 0.2, 1.5)
    curse = keyed(t, [(t0, 0.0), (tC - 0.1, 1.0)], 0.25, 1.5)
    k_mood = "angry" if t > tC - 0.15 else ("shock" if t > tF - 0.05 else "sleep")
    hy_k = kg - RU.SEAT_H * ks
    aim = point_at(kx, hy_k, ks, (sx - 40, sf - 760 * ss), 0.95)
    kfr = mix(mix(ANJALI["front"], (-2.7, -0.5), startled), aim, curse)
    kba = mix(mix(ANJALI["backa"], (-2.5, -0.8), startled), (0.2, -0.3), curse)
    kp = khagama(cr, t, kx, kg, ks, mood=k_mood, hop=jump, front=kfr, backa=kba, head=-0.05 * startled,
                 hits=[(tF, 0.6), (tC, 0.5)])
    laugh = tJ - 0.1 < t < tC - 0.1
    reach = keyed(t, [(t0, 0.0), (tG - 0.35, 1.0), (tC - 0.15, 0.0)], 0.3, 1.3)
    back_ = keyed(t, [(t0, 0.0), (tC - 0.1, 1.0)], 0.3, 1.3)
    sp = rishi(cr, t, sx + 40 * back_, ss, mood="laugh" if laugh else ("shock" if t > tC - 0.1 else "calm"), feet=sf,
               flip=True, front=mix(mix((-0.4, -0.5), (-1.45, -0.2), reach), (-0.6, -2.3), back_),
               backa=(0.35, -0.5) if not laugh else (-0.3, -1.9),
               head=-0.08 * (1 if laugh else 0) + 0.06 * curse, rot=0.02 * math.sin(t * 14) * laugh,
               hits=[(tJ, 0.4), (tC, 0.5)], ph=0.5)
    if t > tG - 0.45:                                   # the grass toy snake dangling from his hand
        hand = to_user(cr, sp["handF"])
        q = prog(t, tG - 0.45, 0.3) * (1 - prog(t, tC - 0.25, 0.3))
        prop(cr, "rr_gsnake", hand[0] + 4, hand[1] + 6, 0.66, rot=0.22 * math.sin(t * 3.4) + 0.1, alpha=q)
    dev_k, dev_s = kp["top"], sp["top"]
    dev_head_s = sp["head"]

    def ui(cr):
        if t < tJ:
            head2(cr, t, "THAT SNAKE WAS ONCE A", t0 + 0.05, "SAGE", tS, big_size=260)
        elif t < tC:
            head2(cr, t, "AS A JOKE, HE SCARED HIS FRIEND", tJ - 0.1, "WITH A GRASS SNAKE", tG, big_size=200)
        else:
            head2(cr, t, "THE ANGRY FRIEND", tC - 0.2, "CURSED HIM", tC + 0.05, big_size=240)
        plate(cr, t, t0 + 0.1, "LONG AGO...", 200, 600, 34)
        tag(cr, t, tS + 0.15, "THE SNAKE, LONG AGO", min(dev_s[0] + 10, 830), dev_s[1] - 120, 28, t_out=tJ + 0.1)
        tag(cr, t, tJ + 0.2, "HIS FRIEND", max(200, dev_k[0] - 20), dev_k[1] - 130 - jump, 30, t_out=tC + 0.2)
        if laugh:
            ha(cr, t, tJ + 0.05, dev_head_s[0] - 150, dev_head_s[1] - 110, 64)
        if t > tF and t < tF + 1.0:
            sound_rings(cr, dev_k[0], dev_k[1] + 80, t, tF, 3, 0.25, 220, alpha=0.4)
        card2(cr, t, tC - 0.15, 560, 900, 0.64, [("BE A SNAKE", 92, INK, -52, tC),
                                                 ("WITHOUT VENOM!", 84, RED, 44, tB)])
    return dict(ui=ui, sepia=1.0, flash=flash_at(t, tF, 0.2) + flash_at(t, tC, 0.25))


# ------------------------------------------------------------------ r15  the snake becomes the sage again


RS15 = (300, 0.74, FEET + 150)


def s_sage(cr, t, tl, t0, t1):
    c = cues(tl, "r15")
    tM, tS, tL, tD = c["M"], c["S"], c["L"], c["D"]
    glow(cr, 540, 1250, 620, 0.45)
    prop(cr, "ground", W / 2, FEET + 156, 0.82)
    lit = prog(t, tM, 0.6)
    gone = prog(t, tS, 0.3)
    if gone < 1:
        old_snake(cr, t, tl, alpha=1 - gone, glow_a=0.7 * lit, rods=gone < 0.5)
        lights(cr, t, 330, FEET - 200, 260, 12, 0.8 * lit)
    sx, ss, sf = RS15
    if t > tS - 0.1:
        b, k, a = depth(t, tS - 0.1, 0.5)
        glow(cr, sx, sf - 600 * ss, 480, 0.6 * a)
        aura(cr, t, sx, sf - 700 * ss, 140, 520, 0.4 * a * (1 - 0.5 * prog(t, tS + 1.5, 1.0)), n=18, spin=0.06)
        teach = keyed(t, [(t0, 0.0), (tL - 0.1, 1.0)], 0.3, 1.3)
        rishi(cr, t, sx, ss * k, mood="teach", feet=sf, front=mix((-0.5, -0.6), (-2.25, -0.55), teach),
              backa=(0.3, -0.3), alpha=a, blur=b, hits=[(tL, 0.3)], ph=0.4)
    if t > tS:
        burst(cr, t, 330, FEET - 250, tS, n=20, rmax=620, alpha=0.9)
    x, s, feet = RU13
    low = keyed(t, [(t0, 0.0), (tM + 0.2, 1.0)], 0.35, 1.2)
    bow = keyed(t, [(t0, 0.0), (tL - 0.1, 1.0)], 0.3, 1.3)
    drop_t = tL - 0.1
    fr = mix(mix(STAFF_UP, STAFF_DOWN, low), ANJALI["front"], bow)
    ba = mix((0.3, -0.5), ANJALI["backa"], bow)
    ruru(cr, t, x, s, mood="shock" if t < tS + 0.6 else "calm", feet=feet, flip=True, front=fr, backa=ba,
         staff=None if t > drop_t else (-0.42 * (1 - low), GRIP_UP + (GRIP_DOWN - GRIP_UP) * low), head=0.12 * bow,
         ph=1.0, hits=[(tS, 0.4), (tL, 0.3)])
    if t > drop_t:                                      # the staff falls to the ground
        u = clamp((t - drop_t) / 0.55)
        e = u * u
        ss_ = STAFF_S * s
        prop(cr, "rv_staff", 700 - 150 * e, feet - 430 * ss_ * (1 - e) - 12 * e, ss_, rot=-1.48 * e, alpha=1.0)
    lng = lang(tl)

    def ui(cr):
        if t < tL - 0.2:
            head2(cr, t, "THE SNAKE BECAME A", t0 + 0.05, "SAGE AGAIN", tS, big_size=240)
        else:
            head2(cr, t, "THE SAGE TAUGHT:", tL - 0.2, None, 0.0)
        if t > tL - 0.2:
            quote_note(cr, t, tL - 0.2, 540, 720, 0.6,
                       [("NOT TAKING A LIFE", 104, INK, HEAD_FONT, -118, tL),
                        ("=", 110, INK, HEAD_FONT, 6, tL + 0.35),
                        ("THE HIGHEST DHARMA", 104, RED, HEAD_FONT, 124, tD)])
        if HAS_INDIC and t > tD + 0.15:
            q = prog(t, tD + 0.15, 0.3)
            su = indic_surface(SANSKRIT[lng], 50, INK)
            w_, h_ = su.get_width(), su.get_height()
            yy = 950 + 16 * (1 - q)
            cr.save()
            pc.poly(cr, [(540 - w_ / 2 - 28, yy - h_ / 2 - 14), (540 + w_ / 2 + 28, yy - h_ / 2 - 14),
                         (540 + w_ / 2 + 40, yy), (540 + w_ / 2 + 28, yy + h_ / 2 + 14),
                         (540 - w_ / 2 - 28, yy + h_ / 2 + 14), (540 - w_ / 2 - 40, yy)])
            cr.set_source_rgba(0.97, 0.87, 0.62, 0.96 * q)
            cr.fill_preserve()
            cr.set_source_rgba(*pc.INK, q)
            cr.set_line_width(3.5)
            cr.stroke()
            cr.set_source_surface(su, 540 - w_ / 2, yy - h_ / 2)
            cr.paint_with_alpha(q)
            cr.restore()
    return dict(ui=ui, flash=flash_at(t, tS, 0.45) + flash_at(t, tD, 0.2))


# ------------------------------------------------------------------ r16  would you?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "r16")
    tH, tY, tC = c["H"], c["Y"], c["C"]
    prop(cr, "ground", W / 2, FEET + 96, 0.82)
    glow(cr, 540, 1420, 460, 0.45)
    rp = ruru(cr, t, 440, 0.52, mood="smile", feet=FEET + 90, front=(-0.6, -0.8), ph=1.0)
    pram(cr, t, 650, 0.5, eyes="smile", feet=FEET + 90, flip=True, front=(-0.6, -0.8))
    top = to_user(cr, rp["top"])
    life_bar(cr, t, 440, top[1] - 80, 0.26, lit=5)
    cards = ((300, "YES", tH + 0.1), (780, "NO", tH + 0.3))

    def ui(cr):
        head2(cr, t, "WOULD YOU GIVE SOMEONE", t0 + 0.05, "HALF YOUR LIFE?", tH, big_size=210)
        for cx, txt, tc in cards:
            card(cr, t, tc - 0.25, cx, 720, 0.58, [(txt, 150, RED, 4)])
        if t > tY:
            n = int((t - tY) / 0.9)
            k = n % 2
            red_ring(cr, cards[k][0], 724, 232, 96, prog(t, tY + 0.9 * n, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tY, 0.15))


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("r1", None, s_hook, {"z": (1.0, 1.04)}),
    ("r2", None, s_book, {"z": (1.0, 1.03)}),
    ("r3", None, s_couple, {"z": (1.0, 1.03)}),
    ("r4", None, s_foot, {"z": (1.0, 1.05), "focus": (560, 1500)}),
    ("r5", None, s_bite, {"z": (1.0, 1.04)}),
    ("r6", None, s_weep, {"z": (1.0, 1.04)}),
    ("r7", None, s_duta, {"z": (1.0, 1.03)}),
    ("r8", None, s_split, {"z": (1.0, 1.04)}),
    ("r9", None, s_give, {"z": (1.0, 1.03)}),
    ("r10", None, s_wake, {"z": (1.0, 1.03)}),
    ("r11", None, s_wedding, {"z": (1.0, 1.03)}),
    ("r12", None, s_vow, {"z": (1.0, 1.04)}),
    ("r13", None, s_old, {"z": (1.0, 1.04)}),
    ("r14", None, s_flash, {"z": (1.0, 1.03)}),
    ("r15", None, s_sage, {"z": (1.0, 1.03)}),
    ("r16", None, s_end, {"z": (1.0, 1.03)}),
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
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a single
    hit on the snakebite, shimmer as the messenger appears, a bell at the wedding, a conch on the sage's teaching, then
    (only where they fit) shimmer as she wakes, a damaru as the old snake speaks, shimmer as the light flows to her, a
    conch on the vow, a damaru on the curse, a bell on the closing question. Chosen in THAT order of importance, each at
    least SFX_MIN_GAP from every sound already kept (as render_myth.calm_sfx keeps them), so the list returned is what
    plays (6-7 sounds); the bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["r5"]["B"], "hit", 0), (c["r7"]["M"], "shimmer", 0), (c["r11"]["W"], "bell", 0),
            (c["r15"]["L"], "conch", 0), (c["r10"]["U"], "shimmer", 0), (c["r13"]["T"], "damaru", 0),
            (c["r9"]["M"], "shimmer", 0), (c["r12"]["V"], "conch", 0), (c["r14"]["C"], "damaru", 0),
            (c["r16"]["Y"], "bell", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["r5"]["B"] - 0.35, "dip", 0.5), (c["r10"]["U"] - 0.3, "dip", 0.45), (c["r15"]["S"] - 0.3, "dip", 0.5)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
