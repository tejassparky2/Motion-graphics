"""Scenes for videos/hanuman_curse.py: "Hanuman forgot his own powers" (Valmiki Ramayana, Uttara Kanda 35-36;
Kishkindha Kanda 66-67), in Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same
lamp-lit screen, two-tier headlines and rod-puppet motion as the earlier reels, with the cast from hanuman_cast. The
script was rewritten (12 Nov 2026) so a 5-year-old can follow it: every line has one shot that shows exactly what is
said, in the order it is said, with one big, short English headline per idea; the twist (Jambavan's reminder and
Hanuman remembering) gets a slow reveal: a spark in his chest that grows until the burst.

Respect: Hanuman, Indra, the gods, the sages and Jambavan with dignity. No injury is drawn: Indra and his white
elephant appear only in a flash, his weapon's strike is a white flash, the child tumbles onto a mountain and lies
there dazed with only a little star on his chin. The sages' anger is a flicker of light, never harm.

Every frame is a pure function of t. On-screen text is short English, except the h6 word card, where the spoken
word (हनु / हनुमान) shows in the viewer's script (shaped by matplotlib as in scenes_arjuna; without the Nirmala font it
falls back to Latin letters). Cues are words of the line ({"hi": ..., "kn": ...}) with a fraction fallback, in one
table (CUES) that the scenes and sfx() both read, with minimum gaps so a fast voice can't bunch the beats together.
Shot starts and cues are cached on the timeline under this module's own names (_hn_shot_starts, _hn_cues). Hindi is
the target; Kannada (a different art style later) only has to run.

Shot list (line: what is on the screen)
  h1   HOOK, frame 0: Hanuman alone and large, looking at the golden light in his two palms, a faint "?":
       HANUMAN FORGOT HIS OWN / POWERS; on "taaqatwar" the light surges; on "par" it flickers; on "nahin" the "?"
       pops red and the light drains out of his hands
  h2   a palm-leaf book opens: VALMIKI RAMAYANA, then A TRUE STORY (ringed): A STORY FROM THE / RAMAYANA, then AND
       IT'S A / TRUE STORY
  h3   dawn: baby Hanuman (tag BABY HANUMAN) hops on a hillside: WHEN HANUMAN WAS A / LITTLE BABY; the red sun rises
       behind the far hill and he points at it: HE SAW THE / RED SUN
  h4   a stem and leaf pop onto the sun, which is drawn like a ripe fruit: HE THOUGHT THE SUN WAS A / SWEET FRUIT!;
       he crouches (YUM!), a dotted arc shows the jump, and he flies at the sun: SO HE FLEW UP TO / EAT IT!
  h5   Indra on his white elephant flashes in on a storm cloud (tags INDRA / KING OF THE GODS): THE KING OF THE
       GODS, / INDRA; his weapon held up (ringed), then thrown: THREW HIS / WEAPON; a white flash at the child's chin
       (ringed, a little star): IT HIT HIS / CHIN!; he tumbles down onto a mountain top, dazed
  h6   the child on the mountain, the star on his chin ringed; a card CHIN = [हनु], an arrow, [हनुमान]: THE CHIN
       IS CALLED / HANU, then SO HIS NAME BECAME / HANUMAN
  h7   the gods (dark figures with halos, tag THE GODS) send streams of light into the child on a lotus: THE GODS
       GAVE HIM / POWERS; he raises his arms, a burst, a huge shadow of his strength: NOW NOBODY COULD / BEAT HIM!
  h8   the child bouncing, grinning: BUT LITTLE KIDS ARE / NAUGHTY!; the hermitage comes on and he hops in: HE RAN
       INTO THE / SAGES' HUT; ladles, pots and a bowl fly up as he flips: AND THREW THEIR THINGS / EVERYWHERE!
  h9   the mess about; two sages come in (tag THE SAGES), shocked, then angry with puffs of anger: THE SAGES GOT /
       ANGRY!; they point, crackling light: THEY SAID: and the card YOU WILL FORGET / ALL YOUR POWER!; the child's
       glow drains away
  h10  his last glow fades: AND HE REALLY / FORGOT; a palm-leaf calendar flips YEAR 1, 2, 3... while day and night
       flicker and the child becomes the grown Hanuman, no glow: FOR MANY / YEARS; two other vanaras walk in beside
       him and he scratches his head: HE LIVED LIKE AN / ORDINARY VANARA
  h11  the seashore, the vanara army, Lanka small on the horizon: THEN ONE / DAY...; a warm light over Lanka (tag
       SITA MATA IS HERE): TO FIND / SITA MATA; a dotted arc over the sea, SO FAR AWAY!: THEY HAD TO CROSS A / HUGE
       OCEAN
  h12  the vanaras shake their heads, a big red X over the arc: NOBODY COULD JUMP / THAT FAR; they hang their heads,
       Hanuman sits on a rock among them, the light dims: EVERYONE SAT / SAD
  h12q the question card HOW WILL HE / REMEMBER? under a big red "?", Hanuman small and waiting: SO NOW WHAT?
  h13  old Jambavan walks in with his staff (tags JAMBAVAN / KING OF THE BEARS): THE OLD KING OF THE BEARS, /
       JAMBAVAN; he speaks and a thought bubble shows the baby flying at the fruit-sun: HE SAID: YOU ONCE FLEW / TO
       THE SUN!
  h14  the twist, slowly: a spark in Hanuman's chest grows and grows, then his halo lights in a burst and he stands:
       AS SOON AS HE HEARD IT... / HE REMEMBERED!; he grows huge, towering over Jambavan and the shore: AND HE GREW
       AS BIG AS A / MOUNTAIN
  h15  the giant jump: from the shore a long arc of golden light over the ocean to Lanka: IN ONE / GIANT JUMP, then
       HE CROSSED THE WHOLE / OCEAN
  h15c the hook's picture again (Hanuman large, light in his palms, now shining steadily, his halo lit); where the
       "?" was, the fruit-sun appears: HE ONCE FLEW UP TO / THE SUN...; the whole ocean small at his feet, one dotted
       jump over it: SO THE OCEAN WAS JUST / ONE JUMP!
  h16  WHO WAS / THE REAL HERO?; cards HANUMAN? / JAMBAVAN?, a red ring alternating; both small below, facing each
       other
"""
import math

import cairo

import hanuman_cast as HC
import mandhata_cast as M
import puppet_core as pc
import ravana_cast as R
import ruru_cast as RU
import six_cast_a as SA
import six_cast_b  # noqa: F401  (registers the cow)
import six_cast_c  # noqa: F401  (registers the rock)
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, back, clamp, draw_text, ease, prog, text_size
from puppet_core import H, W, dangle, depth, keyed, prop, puppet, sway
from scenes_arjuna import HAS_INDIC, card2, down_arrow, indic_surface
from scenes_dharmavyadha import point_to
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, man_angles, motes, red_ring
from scenes_jayadratha import NIGHT, flash_at, silhouette, tag, tint, title_lift, to_user
from scenes_kaikeyi import card, fig
from scenes_lakshman_rekha import big_x, book, sparkle
from scenes_mandhata import aura, burst, held, lights, local, mix, reach_arm, warm, yajna_fire
from scenes_ravana import dotted, head2
from scenes_ruru import flow, held_grip, plate, sepia
from scenes_shani_ganesha import bolt, deva
from shots import CUT_LEAD, MIN_SHOT, T

MISSES = set()                       # cue words not found in a line (falls back to fractions)
G = FEET + 120                       # the ground line of most sets
SEA_Y = 900                          # the horizon over the ocean
SHORE_Y = 1180                       # where the sea meets the beach
HANU_W = {"hi": "हनु", "kn": "ಹನು"}                       # the spoken words on the h6 cards
NAME_W = {"hi": "हनुमान", "kn": "ಹನುಮಂತ"}
HANU_L = {"hi": "HANU", "kn": "HANU"}                     # Latin fallbacks (no Nirmala font)
NAME_L = {"hi": "HANUMAN", "kn": "HANUMANTA"}


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
    "h1": (("S", {"hi": "ताक़तवर", "kn": "ಶಕ್ತಿಶಾಲಿ"}, 0.35, (("t0", 0.9),)),
           ("B", {"hi": "पर", "kn": "ಆದ್ರೆ"}, 0.55, (("S", 0.6),)),
           ("N", {"hi": "नहीं", "kn": "ನೆನಪಿರಲಿಲ್ಲ"}, 0.85, (("B", 0.8),))),
    "h2": (("R", {"hi": "रामायण", "kn": "ರಾಮಾಯಣದ"}, 0.2, (("t0", 0.3),)),
           ("T", {"hi": "सच्ची", "kn": "ನಿಜವಾದ"}, 0.55, (("R", 0.6),))),
    "h3": (("B", {"hi": "बच्चे", "kn": "ಮಗುವಾಗಿದ್ದಾಗ"}, 0.35, (("t0", 0.4),)),
           ("R", {"hi": "सूरज", "kn": "ಸೂರ್ಯನನ್ನ"}, 0.8, (("B", 1.0),))),
    "h4": (("M", {"hi": "मीठा", "kn": "ಸಿಹಿಯಾದ"}, 0.28, (("t0", 0.4),)),
           ("F", {"hi": "फल", "kn": "ಹಣ್ಣು"}, 0.35, (("M", 0.3),)),
           ("E", {"hi": "खाने", "kn": "ತಿನ್ನೋಕೆ"}, 0.65, (("F", 0.8),)),
           ("U", {"hi": "उड़", "kn": "ಹಾರಿದ"}, 0.88, (("E", 0.5),))),
    "h5": (("I", {"hi": "इंद्र", "kn": "ಇಂದ್ರ"}, 0.15, (("t0", 0.3),)),
           ("W", {"hi": "हथियार", "kn": "ಆಯುಧ"}, 0.4, (("I", 0.6),)),
           ("T", {"hi": "फेंका", "kn": "ಎಸೆದ"}, 0.5, (("W", 0.4),)),
           ("J", {"hi": "ठुड्डी", "kn": "ದವಡೆಗೆ"}, 0.8, (("T", 0.8),))),
    "h6": (("C", {"hi": "ठुड्डी", "kn": "ದವಡೆಗೆ"}, 0.05, (("t0", 0.15),)),
           ("H", {"hi": "हनु", "kn": "ಹನು"}, 0.25, (("C", 0.5),)),
           ("N", {"hi": "नाम", "kn": "ಹೆಸರು"}, 0.6, (("H", 0.8),)),
           ("M", {"hi": "हनुमान", "kn": "ಹನುಮಂತ"}, 0.9, (("N", 0.5),))),
    "h7": (("D", {"hi": "देवताओं", "kn": "ದೇವತೆಗಳು"}, 0.15, (("t0", 0.2),)),
           ("P", {"hi": "शक्तियाँ", "kn": "ಶಕ್ತಿಗಳನ್ನ"}, 0.45, (("D", 0.8),)),
           ("B", {"hi": "हरा", "kn": "ಸೋಲಿಸೋಕಾಗಲ್ಲ"}, 0.8, (("P", 1.0),))),
    "h8": (("N", {"hi": "शरारती", "kn": "ತುಂಟರು"}, 0.2, (("t0", 0.4),)),
           ("K", {"hi": "कुटिया", "kn": "ಗುಡಿಸಲಿಗೆ"}, 0.55, (("N", 0.9),)),
           ("T", {"hi": "फेंकने", "kn": "ಎಸೆಯೋಕೆ"}, 0.85, (("K", 0.9),))),
    "h9": (("A", {"hi": "ग़ुस्सा", "kn": "ಕೋಪ"}, 0.15, (("t0", 0.3),)),
           ("S", {"hi": "कहा", "kn": "ಹೇಳಿದ್ರು"}, 0.4, (("A", 0.8),)),
           ("F", {"hi": "भूल", "kn": "ಮರೆತುಬಿಡ್ತೀಯ"}, 0.85, (("S", 0.8),))),
    "h10": (("F", {"hi": "भूल", "kn": "ಮರೆತುಬಿಟ್ಟ"}, 0.3, (("t0", 0.4),)),
            ("Y", {"hi": "सालों", "kn": "ವರ್ಷ"}, 0.5, (("F", 0.7),)),
            ("V", {"hi": "वानरों", "kn": "ವಾನರರ"}, 0.68, (("Y", 0.8),)),
            ("O", {"hi": "साधारण", "kn": "ಸಾಮಾನ್ಯವಾಗಿ"}, 0.85, (("V", 0.5),))),
    "h11": (("D", {"hi": "दिन", "kn": "ದಿನ"}, 0.1, (("t0", 0.2),)),
            ("S", {"hi": "सीता", "kn": "ಸೀತಾ"}, 0.3, (("D", 0.6),)),
            ("O", {"hi": "समुद्र", "kn": "ಸಮುದ್ರ"}, 0.75, (("S", 0.9),))),
    "h12": (("J", {"hi": "कूद", "kn": "ಹಾರೋಕಾಗ್ತಿರಲಿಲ್ಲ"}, 0.3, (("t0", 0.3),)),
            ("U", {"hi": "उदास", "kn": "ಬೇಜಾರಾಗಿ"}, 0.75, (("J", 0.9),))),
    "h12q": (("W", {"hi": "क्या", "kn": "ಏನು"}, 0.15, (("t0", 0.15),)),
             ("R", {"hi": "याद", "kn": "ನೆನಪಾಗುತ್ತೆ"}, 0.65, (("W", 0.8),)),
             ("H", {"hi": "कैसे", "kn": "ಹೇಗೆ"}, 0.75, (("W", 0.7),))),
    "h13": (("K", {"hi": "भालुओं", "kn": "ಕರಡಿಗಳ"}, 0.08, ()),
            ("J", {"hi": "जामवंत", "kn": "ಜಾಂಬವಂತ"}, 0.25, (("K", 0.5),)),
            ("A", {"hi": "आए", "kn": "ಬಂದು"}, 0.45, (("J", 0.5),)),
            ("S", {"hi": "बोले", "kn": "ಹೇಳಿದ"}, 0.55, (("A", 0.3),)),
            ("U", {"hi": "सूरज", "kn": "ಸೂರ್ಯನವರೆಗೂ"}, 0.85, (("S", 0.9),))),
    "h14": (("R", {"hi": "याद", "kn": "ನೆನಪಾಯ್ತು"}, 0.45, (("t0", 1.2),)),
            ("G", {"hi": "पहाड़", "kn": "ಬೆಟ್ಟದಷ್ಟು"}, 0.75, (("R", 0.9),))),
    "h15": (("L", {"hi": "छलांग", "kn": "ಜಿಗಿತದಲ್ಲಿ"}, 0.3, (("t0", 0.4),)),
            ("O", {"hi": "समुद्र", "kn": "ಸಮುದ್ರ"}, 0.65, (("L", 0.8),))),
    "h15c": (("S", {"hi": "सूरज", "kn": "ಸೂರ್ಯನವರೆಗೂ"}, 0.25, (("t0", 0.3),)),
             ("O", {"hi": "समुद्र", "kn": "ಸಮುದ್ರ"}, 0.6, (("S", 0.9),)),
             ("L", {"hi": "छलांग", "kn": "ಜಿಗಿತ"}, 0.85, (("O", 0.5),))),
    "h16": (("H", {"hi": "हीरो", "kn": "ಹೀರೋ"}, 0.15, (("t0", 0.4),)),
            ("A", {"hi": "हनुमान", "kn": "ಹನುಮಂತನಾ"}, 0.4, (("H", 0.5),)),
            ("J", {"hi": "जामवंत", "kn": "ಜಾಂಬವಂತನಾ"}, 0.7, (("A", 0.7),)),
            ("C", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.88, (("J", 0.5),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_hn_cues", None)
    if cache is None:
        cache = {}
        tl._hn_cues = cache
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


def ground(cr, y=G, alpha=1.0, blur=0.0):
    prop(cr, "ground", W / 2, y + 6, 0.82, alpha=alpha, blur=blur)


def star_on(cr, t, p, s=0.5, alpha=1.0):
    """The little gold star on the child's chin (the only mark the thunderbolt leaves)."""
    if alpha <= 0.01:
        return
    glow(cr, p[0], p[1], 90, 0.45 * alpha)
    prop(cr, "star", p[0] + 14, p[1] + 4, s * (1 + 0.12 * math.sin(t * 6)), rot=0.3 * math.sin(t * 2), alpha=alpha)
    sparkle(cr, p[0] + 20, p[1] - 6, 30 * (0.7 + 0.3 * math.sin(t * 7)), 0.9 * alpha)


def qmark(cr, t, t_in, x, y, size, color=RED, alpha=1.0):
    """A big "?" popping in at t_in and wobbling."""
    q = back(clamp((t - t_in) / 0.3), 1.6)
    if q <= 0.01 or alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(0.12 + 0.06 * math.sin(t * 3))
    cr.scale(q, q)
    draw_text(cr, "?", 0, 0, size, color, clamp(q) * alpha, anchor="cm")
    cr.restore()


def trail(cr, pts, a, w=1.0):
    """A ribbon of golden light along pts (a leap's path so far)."""
    if a <= 0.01 or len(pts) < 2:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, col, k in ((40 * w, (1.0, 0.60, 0.15), 0.20), (16 * w, (1.0, 0.72, 0.25), 0.45),
                       (5 * w, (1.0, 0.95, 0.75), 0.9)):
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
        cr.set_source_rgba(*col, k * a)
        cr.set_line_width(lw)
        cr.stroke()
    cr.restore()


def arc_path(p0, p1, lift, n=60, u1=1.0):
    """Points on a parabola-like arc from p0 to p1 rising `lift` above the straight line, up to fraction u1."""
    out = []
    for i in range(n + 1):
        u = u1 * i / n
        out.append((p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u - lift * 4 * u * (1 - u)))
    return out


def anger_puffs(cr, t, x, y, a):
    """Puffs of anger over a head: little dark-red swirls popping up."""
    if a <= 0.01:
        return
    for i in range(3):
        u = (t * 1.3 + i / 3) % 1.0
        xx = x - 40 + 40 * i + 10 * math.sin(t * 5 + i)
        yy = y - 30 - 90 * u
        cr.new_path()
        cr.arc(xx, yy, 10 + 16 * u, 0, 2 * math.pi * 0.8)
        cr.set_source_rgba(0.70, 0.08, 0.05, 0.7 * (1 - u) * a)
        cr.set_line_width(5)
        cr.stroke()


# ------------------------------------------------------------------ puppets


def baby(cr, t, x, y, s, mood="calm", arms=(-0.25, 0.25), legs=(-0.06, 0.06), head=0.0, tail=0.0, rot=0.0,
         flip=False, alpha=1.0, blur=0.0, rods=True, hits=(), ph=0.0, aura_a=0.0):
    """Baby Hanuman with his hip at (x, y) (standing: y = feet - BABY_LEG * s). arms / legs are absolute angles
    (0 hangs down, -pi/2 points forward, -pi up); aura_a lights his glow of power."""
    if aura_a > 0.01:
        cx, cy = local(x, y, s, rot, flip, 20, -250)
        glow(cr, cx, cy, 460 * s + 80, 0.6 * aura_a * alpha)
        warm(cr, cx, cy, 420 * s, 0.6 * aura_a * alpha)
        aura(cr, t, cx, cy, 170 * s, 560 * s, 0.75 * aura_a * alpha, n=16, spin=0.3)
    d = dangle(t, hits, 0.28, 1.6, 2.4)
    ang = {"hn_baby_armF": arms[0] + 0.25 + d + sway(t, 0.05, 0.7, ph),
           "hn_baby_armB": arms[1] - 0.25 - 0.6 * d + sway(t, 0.04, 0.6, ph + 1),
           "hn_baby_legF": legs[0] + 0.06, "hn_baby_legB": legs[1] - 0.06,
           "hn_baby_head": head + sway(t, 0.025, 0.5, ph + 2),
           "hn_baby_tail": tail + 0.14 * math.sin(t * 2.4 + ph)}
    sw = {"hn_baby_head": "hn_baby_head" + ("" if mood == "calm" else "_" + mood)}
    return puppet(cr, HC.BABY, x, y, s, rot + bob_rot(t, ph, 0.015), flip, ang, alpha, blur, swap=sw, rods=rods)


def baby_y(feet, s):
    return feet - HC.BABY_LEG * s


HANU_HEAD = {m: "hn_hanu_head" + ("" if m == "calm" else "_" + m) for m in HC.HANU_MOODS}
GADA_S = 0.62


def halo(cr, t, x, y, r, a):
    """Hanuman's slight halo: a soft glow, slow golden rays and a thin gold ring behind his head."""
    if a <= 0.01:
        return
    glow(cr, x, y, r * 2.4, 0.55 * a)
    warm(cr, x, y, r * 1.8, 0.55 * a)
    aura(cr, t, x, y, r * 0.8, r * 1.9, 0.6 * a, n=20, spin=0.12)
    cr.save()
    cr.set_source_rgba(1.0, 0.78, 0.26, 0.85 * a)
    cr.set_line_width(max(3.0, r * 0.05))
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.stroke()
    cr.restore()


def hanu(cr, t, x, s, mood="calm", gada=True, open_back=False, halo_a=0.0, front=(-0.32, -0.55),
         backa=(0.3, -0.25), feet=G, y=None, rot=0.0, flip=False, alpha=1.0, blur=0.0, gada_tilt=0.0, gada_grip=0.0,
         **kw):
    """Grown Hanuman standing (feet on `feet`, or hip at y), his gada in his back hand; halo_a lights his halo."""
    hy = feet - 434 * s if y is None else y
    if halo_a > 0.01:
        hx_, hy_ = local(x, hy, s, rot, flip, 22, -440)
        halo(cr, t, hx_, hy_, 200 * s, halo_a * alpha)
    ex = {}
    if gada:
        ex["hn_hanu_armB_lo"] = held_grip("hn_gada", backa, GADA_S, gada_tilt, gada_grip, alpha, blur)
    sw = {"hn_hanu_head": HANU_HEAD[mood]}
    if open_back:
        sw["hn_hanu_armB_lo"] = "hn_hanu_armF_lo"
    return fig(cr, HC.HANU, "hn_hanu", t, x, s, front=front, backa=backa, feet=feet, y=y, rot=rot, flip=flip,
               alpha=alpha, blur=blur, swap=sw, extra=ex or None, **kw)


SIT = dict(front=(-0.55, -0.95), backa=(-0.2, -1.1))            # seated, hands resting on his knees


def hanu_sit(cr, t, x, ground_, s, mood="sad", head=0.0, front=SIT["front"], backa=SIT["backa"], alpha=1.0,
             blur=0.0, rock=True, hits=(), ph=0.6, halo_a=0.0):
    """Hanuman seated on a rock (soles on ground_), his gada leaning on the rock behind him."""
    hip = ground_ - HC.HANU_SIT_H * s
    if rock:
        prop(cr, "hn_gada", x - 150 * s, ground_ - 40 * s, GADA_S * s, rot=-0.32, alpha=alpha, blur=blur)
        prop(cr, "c6_rock", x - 10 * s, ground_ + 8, 0.82 * s, alpha=alpha, blur=blur)
    if halo_a > 0.01:
        hx_, hy_ = local(x, hip, s, 0.0, False, 22, -440)
        halo(cr, t, hx_, hy_, 200 * s, halo_a * alpha)
    prop(cr, "hn_hanu_sit", x, hip, s, alpha=alpha, blur=blur)
    ang = man_angles("hn_hanu", t, front, backa, head, (0.0, 0.0), hits, ph)
    return puppet(cr, HC.HANU, x, hip, s, bob_rot(t, ph, 0.006), False, ang, alpha, blur,
                  hide=("hn_hanu_legF", "hn_hanu_legB"), swap={"hn_hanu_head": HANU_HEAD[mood]})


JSTAFF_GRIP = -120.0
J_BACK = (0.15, -0.95)                # Jambavan's back hand forward at his side, holding the staff upright


def jamb(cr, t, x, s, mood="calm", staff=True, backa=J_BACK, **kw):
    """Jambavan standing (feet on `feet`), his staff upright in his back hand."""
    a, b = kw.get("alpha", 1.0), kw.get("blur", 0.0)
    ex = {"hn_jamb_armB_lo": held_grip("hn_jstaff", backa, 0.6, 0.0, JSTAFF_GRIP, a, b)} if staff else None
    sw = {"hn_jamb_head": "hn_jamb_head" + ("" if mood == "calm" else "_" + mood)}
    kw.setdefault("feet", G)
    return fig(cr, HC.JAMB, "hn_jamb", t, x, s, backa=backa, swap=sw, extra=ex, **kw)


def sage(cr, t, who, x, s, mood="angry", **kw):
    """One of the two hermitage sages: 'khag' (ruru_cast's dark-bearded sage) or 'old' (six_cast_a's white-bearded
    sage). mood: calm | shock | angry."""
    kw.setdefault("feet", G)
    if who == "khag":
        m = {"calm": "rr_khag_head_shock", "shock": "rr_khag_head_shock", "angry": "rr_khag_head_angry"}[mood]
        return fig(cr, RU.KHAG, "rr_khag", t, x, s, swap={"rr_khag_head": m}, **kw)
    m = {"calm": "sx_shukra_head", "shock": "sx_shukra_head_shock", "angry": "sx_shukra_head_angry"}[mood]
    return fig(cr, SA.SHUKRA, "sx_shukra", t, x, s, swap={"sx_shukra_head": m}, **kw)


def monkey(cr, t, x, feet, s, flip=False, shake=0.0, ph=0.0, front=(-0.4, -0.5), backa=(0.3, -0.4), alpha=1.0,
           blur=0.0, rods=False, rot=0.0, legs=(0.0, 0.0), bow=0.0):
    """A vanara of the army (ravana_cast's VANARA); shake 0..1 shakes his head: no; bow 0..1 hangs it low."""
    head = shake * 0.22 * math.sin(t * 13 + ph) + 0.32 * bow
    ang = man_angles("vanara", t, front, backa, head, legs, (), ph)
    return puppet(cr, R.VANARA, x, feet - 434 * s, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, rods=rods)


def indra_on_elephant(cr, t, x, ground_, s, raise_=0.0, vajra=True, alpha=1.0, hits=()):
    """Indra seated on Airavata (the elephant's feet on ground_), the vajra raised in his front hand."""
    prop(cr, "hn_airavata", x, ground_, s, rot=sway(t, 0.008, 0.4), alpha=alpha)
    ix, iy = x + HC.AIR_SEAT[0] * s, ground_ + HC.AIR_SEAT[1] * s
    si = s * 0.66
    front = mix((-0.9, -0.9), (-2.75, -0.15), raise_)
    ang = man_angles("indra", t, front, (0.35, -0.7), 0.0, (0.0, 0.0), hits, 0.5)
    ex = {"indra_armF_lo": held("md_vajra", front, 0.7, alpha=alpha)} if vajra else None
    return puppet(cr, M.INDRA, ix, iy, si, bob_rot(t, 0.5, 0.008), False, ang, alpha,
                  hide=("indra_legF", "indra_legB"), extra=ex, rods=False)


# ------------------------------------------------------------------ sets


def sun(cr, t, x, y, s, fruit=0.0, alpha=1.0, glow_a=1.0, rays=True):
    """The rising sun drawn like a ripe red fruit; fruit 0..1 pops the stem and leaf on top."""
    if alpha <= 0.01:
        return
    glow(cr, x, y, 560 * s + 120, 0.55 * glow_a * alpha)
    warm(cr, x, y, 420 * s, 0.6 * glow_a * alpha, (1.0, 0.55, 0.15))
    if rays:
        prop(cr, "hn_sun_rays", x, y, s, rot=t * 0.12, alpha=alpha)
    r = sway(t, 0.02, 0.3)
    prop(cr, "hn_sun", x, y, s, rot=r, alpha=alpha)
    if fruit > 0.01:
        q = back(clamp(fruit), 1.8)
        tx, ty = local(x, y, s, r, False, 0, -HC.SUN_RAD + 10)
        prop(cr, "hn_stem", tx, ty, s * q, rot=r + sway(t, 0.05, 0.5), alpha=alpha * clamp(fruit * 3))


def hermitage(cr, t, alpha=1.0, blur=0.0, fire=1.0, flare=0.0):
    """The sages' hermitage: a far tree, the hut, the bark-cloth heap, the yajna fire on its altar."""
    prop(cr, "tree", 70, G + 10, 0.62, rot=sway(t, 0.006, 0.3), alpha=0.55 * alpha, blur=8 + blur, flip=True)
    prop(cr, "lr_hut", HUT[0], G + 10, HUT[1], alpha=0.92 * alpha, blur=2 + blur)
    ground(cr, alpha=alpha, blur=blur)
    if fire > 0.01:
        yajna_fire(cr, t, FIRE_X, G, 0.7, flare, alpha * fire)
    else:
        prop(cr, "altar", FIRE_X, G + 14, 0.5, alpha=alpha, blur=blur)


HUT = (860, 0.6)
FIRE_X = 600
ITEMS = (   # (sprite, rest x, rest y offset, scale, rest rot, land x, land rot, land y offset): the things he tosses
    ("hn_ladle", 300, -18, 0.5, -0.12, 520, 0.4, -10),
    ("md_kalasha", 420, 4, 0.42, 0.0, 470, 1.62, -60),
    ("hn_ladle", 500, -44, 0.48, 0.8, 700, -0.3, -8),
    ("dv_bowl", 700, 2, 0.62, 0.0, 600, 2.9, -36),
    ("md_kalasha", 740, 4, 0.36, 0.0, 790, -1.55, -50),
)


def item_at(t, i, t_fly):
    """Where item i is: at rest until t_fly, then flying up spinning and coming down tipped at its landing spot."""
    sp, x0, dy0, s, r0, x1, r1, dy1 = ITEMS[i]
    y0, y1 = G + dy0, G + dy1
    if t < t_fly:
        return sp, x0, y0, s, r0
    u = clamp((t - t_fly) / 1.1)
    x = x0 + (x1 - x0) * u
    y = y0 + (y1 - y0) * u - 620 * 4 * u * (1 - u)
    spin = (r1 - r0) + 2 * math.pi * (1 if i % 2 else -1)
    rot = r0 + spin * ease(u) if u < 1 else r1
    return sp, x, y, s, rot


def sea(cr, t, alpha=1.0, lanka=1.0, lanka_s=0.3, lanka_x=860):
    """The vast ocean to the horizon, Lanka small and golden on it, rolling strips of sea (kept light, so the
    puppets in front of it still glow)."""
    if lanka > 0.01:
        glow(cr, lanka_x, SEA_Y - 60, 260, 0.35 * lanka * alpha)
        prop(cr, "rv_lanka", lanka_x, SEA_Y + 12, lanka_s, alpha=lanka * alpha, blur=1.5)
    cr.save()                                           # the sea stops at the shore (the sand is not tinted by it)
    cr.rectangle(-300, -300, W + 600, SHORE_Y + 22 + 300)
    cr.clip()
    for k in range(3):
        sh = 18 * math.sin(t * (0.6 + 0.15 * k) + k * 1.3)
        prop(cr, "sx_wave2" if k % 2 == 0 else "sx_wave", 540 + sh + (24 if k % 2 else -24), SEA_Y + 20 + 92 * k,
             0.5 + 0.02 * k, alpha=0.78 * alpha)
    cr.restore()


def shore(cr, t, alpha=1.0, lanka=1.0, palm=True, lanka_s=0.3, lanka_x=860):
    sea(cr, t, alpha, lanka, lanka_s, lanka_x)
    prop(cr, "hn_beach", 540, SHORE_Y, 0.75, alpha=alpha)
    if palm:
        prop(cr, "hn_palm", 64, SHORE_Y + 470, 0.62, rot=sway(t, 0.012, 0.4), alpha=alpha)


# ------------------------------------------------------------------ h1  hook


HK = (385, 1.06, 1895)               # Hanuman in the hook: x, scale, feet


def orb(cr, t, x, y, r, a):
    """A small ball of golden light (the power in his palm): turning rays, a gold rim, a white core."""
    if a <= 0.01:
        return
    glow(cr, x, y, r * 5, 0.8 * a)
    warm(cr, x, y, r * 3.6, 0.9 * a)
    aura(cr, t, x, y, r * 0.9, r * 3.0, 0.9 * a, n=14, spin=0.9)
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 1.0, 0.96, 0.70, a)
    g.add_color_stop_rgba(0.55, 1.0, 0.74, 0.22, 0.97 * a)
    g.add_color_stop_rgba(1, 0.95, 0.42, 0.06, 0.95 * a)
    cr.save()
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill_preserve()
    cr.set_source_rgba(0.45, 0.16, 0.02, 0.85 * a)
    cr.set_line_width(max(2.5, r * 0.09))
    cr.stroke()
    cr.restore()
    sparkle(cr, x, y, r * 1.8, a, (1.0, 0.95, 0.80))


def hand_glow(cr, t, p, a, r=1.0):
    """Light in his palm: an orb of power floating just above it, and sparks rising."""
    if a <= 0.01:
        return
    orb(cr, t, p[0] + 4, p[1] - 56 * r + 6 * math.sin(t * 3 + p[0]), 44 * r * (0.7 + 0.3 * a), a)
    lights(cr, t, p[0], p[1] - 60, 90 * r, 6, 0.9 * a, speed=0.7)


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "h1")
    tS, tB, tN = c["S"], c["B"], c["N"]
    x, s, feet = HK
    hip = feet - 434 * s
    glow(cr, x + 80, feet - 760 * s, 620, 0.42)
    fr = reach_arm(x, hip, s, 26 * 1.2, (x + 250 * s, hip - 300 * s))
    ba = reach_arm(x, hip, s, -14 * 1.2, (x + 175 * s, hip - 262 * s))
    mood = "puzzled" if t < tN + 0.2 else "sad"
    pts = hanu(cr, t, x, s, mood=mood, gada=False, open_back=True, feet=feet, front=fr, backa=ba,
               head=0.3 + 0.05 * prog(t, tN, 0.5), hits=[(tS, 0.25), (tN, 0.3)], ph=1.0)
    hf, hb = to_user(cr, pts["handF"]), to_user(cr, pts["handB"])
    base = 0.62 + 0.38 * prog(t, tS - 0.1, 0.3) * (1 - prog(t, tB, 0.5))
    flick = 1.0 if t < tB else 0.72 + 0.28 * math.sin(t * 23) * (1 - prog(t, tN, 0.4))
    a_h = base * flick * (1 - 0.82 * prog(t, tN, 0.9))
    for p, r in ((hb, 0.85), (hf, 1.0)):
        hand_glow(cr, t, (p[0] + 6, p[1] - 6), a_h, r)
    if tS < t < tS + 1.0:
        burst(cr, t, hf[0], hf[1], tS, n=14, rmax=300, alpha=0.6)
    if t > tN:                                          # the light drains out of his hands: he has forgotten
        for i in range(10):
            ti = tN + 0.11 * i
            u = (t - ti) / 1.1
            if 0 < u < 1:
                p = hf if i % 2 else hb
                sparkle(cr, p[0] + 24 * math.sin(i * 2.1), p[1] + 30 + 520 * u * u, 22 * (1 - u), 1 - u)

    def ui(cr):
        head2(cr, t, "HANUMAN FORGOT HIS OWN", -1.0, "POWERS", 0.3, big_size=250, ghost=-1.0, under=tN)
        if t < tN:
            qmark(cr, t, -1.0, 760, 900, 170, INK, 0.30 + 0.05 * math.sin(t * 3))
        else:
            qmark(cr, t, tN, 760, 900, 230, RED)
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.2) + flash_at(t, tS, 0.3) + flash_at(t, tN, 0.2))


# ------------------------------------------------------------------ h2  a true story from the Ramayana


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "h2")
    tR, tT = c["R"], c["T"]
    leaves = [(None, [("VALMIKI RAMAYANA", 90, HEAD_FONT)], 0),
              (tT, [([("A TRUE STORY", RED)], 84, HEAD_FONT)], 0)]
    book(cr, t, 540, 960, 0.86, leaves, t_in=t0 + 0.05, t_open=tR, ring=(1, 0, 0, tT + 0.3))

    def ui(cr):
        if t < tT:
            head2(cr, t, "A STORY FROM THE", t0 + 0.05, "RAMAYANA", tR, big_size=240)
        else:
            head2(cr, t, "AND IT'S A", tT - 0.1, "TRUE STORY", tT + 0.05, big_size=240, under=tT + 0.4)
    return dict(ui=ui, flash=flash_at(t, tR, 0.25) + flash_at(t, tT, 0.2))


# ------------------------------------------------------------------ h3 / h4  the red sun; "a sweet fruit!"; he flies


SUN3 = (790, 0.6)                    # the sun: x, scale (it rises to SUN3_Y)
SUN3_Y = 870
BX3, BS3 = 250, 0.72                 # the child: x, scale


def sun_set(cr, t, rise, fruit=0.0):
    """The dawn set: the sun (rise 0..1 brings it up from behind the far hill), the hills, the ground."""
    sx, ss = SUN3
    sy = 1420 - (1420 - SUN3_Y) * rise
    sun(cr, t, sx, sy, ss, fruit=fruit, glow_a=0.6 + 0.4 * rise)
    prop(cr, "hn_hill", 820, 1600, 0.62, alpha=0.75, blur=5)
    prop(cr, "hn_hill", 260, 1660, 0.45, alpha=0.6, blur=7, flip=True)
    ground(cr)
    lights(cr, t, sx, sy, 260, 8, 0.6 * rise, (1.0, 0.75, 0.35), 0.4)
    return sx, sy


def s_sun(cr, t, tl, t0, t1):
    c = cues(tl, "h3")
    tB, tR = c["B"], c["R"]
    rise = ease((t - tR + 0.7) / 1.5)
    sun_set(cr, t, rise)
    hip0 = baby_y(G, BS3)
    hop = math.sin(math.pi * clamp((t - tB) / 0.45)) * (t > tB)
    look = keyed(t, [(t0, 0.0), (tR + 0.2, 1.0)], 0.35, 1.3)
    point = keyed(t, [(t0, 0.0), (tR + 0.3, 1.0)], 0.3, 1.3)
    b, k, a = depth(t, t0 - 0.3, 0.45)
    baby(cr, t, BX3, hip0 - 60 * hop, BS3 * k, mood="wonder" if t > tR else "happy",
         arms=mix((-0.25, 0.25), (-2.3, 0.3), point), head=-0.28 * look, hits=[(tB, 0.4), (tR, 0.4)], ph=0.3,
         alpha=a, blur=b)
    dev_b = cr.user_to_device(BX3 + 20, hip0 - 520 * BS3)

    def ui(cr):
        if t < tR - 0.1:
            head2(cr, t, "WHEN HANUMAN WAS A", t0 + 0.05, "LITTLE BABY", tB, big_size=230)
        else:
            head2(cr, t, "HE SAW THE", tR - 0.1, "RED SUN", tR + 0.05, big_size=270)
        tag(cr, t, tB + 0.2, "BABY HANUMAN", max(230, dev_b[0]), dev_b[1], 38, t_out=tR)
    return dict(ui=ui, eve=0.35 * (1 - rise * 0.6), flash=flash_at(t, tR, 0.2))


def s_fly(cr, t, tl, t0, t1):
    c = cues(tl, "h4")
    tM, tF, tE, tU = c["M"], c["F"], c["E"], c["U"]
    sx, sy = sun_set(cr, t, 1.0, fruit=(t - tF + 0.05) / 0.35)
    hip0 = baby_y(G, BS3)
    p1 = (sx - 250, sy + 120)
    crouch = keyed(t, [(t0, 0.0), (tE, 1.0), (tU, 0.0)], 0.22, 1.2)
    if t < tU:
        mood = "wonder" if t < tF + 0.2 else "happy"
        point = keyed(t, [(t0, 1.0), (tF + 0.4, 0.0)], 0.3, 1.3)
        arms = mix(mix((-0.25, 0.25), (-2.3, 0.3), point), (0.9, 1.1), crouch)
        baby(cr, t, BX3, hip0 + 34 * BS3 * crouch, BS3, mood=mood, arms=arms, head=-0.28,
             rot=-0.18 * crouch, hits=[(tF, 0.5)], ph=0.3)
    else:
        u = clamp((t - tU) / 0.95)
        path = arc_path((BX3, hip0), p1, 260, 50, u)
        bx, by = path[-1]
        if u >= 1:
            by += 10 * math.sin((t - tU) * 4)
        trail(cr, path, 0.85 * (1 - 0.4 * prog(t, tU + 1.4, 0.6)), 0.8)
        for i in range(6):                              # dust where he sprang up
            q = clamp((t - tU) / 0.8)
            prop(cr, "cloud", BX3 + (i - 2.5) * (40 + 120 * q), G - 20 - 50 * q, 0.16 + 0.12 * q,
                 alpha=0.45 * (1 - q))
        baby(cr, t, bx, by, BS3, mood="happy", arms=(-2.45, -2.15), legs=(0.55, 0.95), head=-0.15,
             rot=0.9 * ease(u * 2), tail=0.4, hits=[(tU, 0.6)], ph=0.3, aura_a=0.3)
    if tE - 0.1 < t < tU + 0.2:                          # the jump he is about to make
        a = prog(t, tE - 0.1, 0.25) * (1 - prog(t, tU, 0.2))
        dotted(cr, arc_path((BX3 + 60, hip0 - 120), (p1[0] - 20, p1[1] - 60), 240, 40), prog(t, tE - 0.1, 0.5),
               30, 6, RED, a)

    def ui(cr):
        if t < tU - 0.1:
            head2(cr, t, "HE THOUGHT THE SUN WAS A", t0 + 0.05, "SWEET FRUIT!", tM, big_size=230)
        else:
            head2(cr, t, "SO HE FLEW UP TO", tU - 0.1, "EAT IT!", tU + 0.05, big_size=280)
        if tE < t < tU:
            plate(cr, t, tE, "YUM!", BX3 + 210, hip0 - 470 * BS3, 40)
    return dict(ui=ui, eve=0.14, flash=flash_at(t, tF, 0.2) + flash_at(t, tU, 0.25))


# ------------------------------------------------------------------ h5  Indra throws his weapon; it hits his chin


SUN4 = (850, 760, 0.58)
HILL4 = (560, 1905, 0.74)
ELE4 = (265, 1235, 0.47)             # Airavata on his storm cloud: x, ground, scale
BB4 = (575, 975, 0.55)               # the child near the sun: hip x, y, scale
CHIN_W = {"hi": "CHIN", "kn": "JAW"}                       # what the line calls the spot (ठुड्डी / ದವಡೆ)


def hill_top(hill):
    hx, hy, hs = hill
    return hx, hy - 610 * hs


def s_strike(cr, t, tl, t0, t1):
    c = cues(tl, "h5")
    tI, tW, tT, tJ = c["I"], c["W"], c["T"], c["J"]
    sx, sy, ss = SUN4
    sun(cr, t, sx, sy, ss, fruit=1.0, glow_a=1 - 0.5 * prog(t, tJ, 0.5))
    hx, hy, hs = HILL4
    prop(cr, "hn_hill", hx, hy, hs)
    bx0, by0, bs = BB4
    tx, ty = hill_top(HILL4)
    lie_y = ty - 56 * bs + 6
    t_in = t0 + 0.1                                      # Indra on his elephant, seen only in the flash
    ia = prog(t, t_in, 0.2) * (1 - prog(t, tJ + 0.3, 0.35))
    hand = None
    if ia > 0.01:
        ex, eg, es = ELE4
        glow(cr, ex + 40, eg - 420 * es, 560, 0.7 * ia)
        burst(cr, t, ex + 40, eg - 420 * es, t_in, n=18, rmax=520, alpha=0.6 * ia)
        prop(cr, "cloud", ex - 60, eg + 40, 1.0, alpha=0.9 * ia)
        prop(cr, "cloud", ex + 200, eg + 60, 0.75, alpha=0.9 * ia)
        raise_ = keyed(t, [(t0, 0.0), (tW, 1.0)], 0.25, 1.4)
        ipts = indra_on_elephant(cr, t, ex, eg, es, raise_, vajra=t < tT, alpha=ia, hits=[(tT, 0.6)])
        hand = to_user(cr, ipts["handF"])
        prop(cr, "cloud", ex - 220, eg + 10, 0.55, alpha=0.8 * ia)
        if tW - 0.1 < t < tT:                            # his weapon, held up and ringed
            red_ring(cr, hand[0] + 4, hand[1] - 70, 80, 110, prog(t, tW - 0.1, 0.35), 8, ia)
    t_land = tJ + 0.9                                    # struck, he tumbles down onto the mountain
    if t < tJ:
        look = keyed(t, [(t0, 0.0), (tT - 0.1, 1.0)], 0.3, 1.3)
        pts = baby(cr, t, bx0, by0 + 10 * math.sin(t * 3.5), bs, mood="happy" if t < tT else "wonder",
                   arms=(-2.45, -2.15), legs=(0.55, 0.95), head=-0.15 + 0.25 * look, rot=0.9, tail=0.4, ph=0.3,
                   aura_a=0.25)
    elif t < t_land:
        u = clamp((t - tJ) / (t_land - tJ))
        e = u * u
        x = bx0 + (tx - 10 - bx0) * e + 60 * math.sin(math.pi * u)
        y = by0 + (lie_y - by0) * e - 140 * math.sin(math.pi * min(1.0, u * 1.6)) * (1 - u)
        spin = 0.9 - (0.9 + math.pi / 2 + 2 * math.pi) * ease(u)
        pts = baby(cr, t, x, y, bs, mood="daze", arms=(-1.2, -0.6), legs=(-0.4, 0.3), rot=spin, tail=0.3, ph=0.3,
                   rods=False)
    else:
        bump = 18 * math.exp(-7 * (t - t_land)) * abs(math.sin((t - t_land) * 14))
        pts = baby(cr, t, tx - 10, lie_y - bump, bs, mood="daze", arms=(-0.6, -0.2), legs=(-0.15, 0.1),
                   rot=-math.pi / 2, tail=0.5, ph=0.3, rods=False)
        for k in (-1, 1):                               # dust where he lands
            q = clamp((t - t_land) / 0.7)
            prop(cr, "cloud", tx + k * (70 + 120 * q), ty - 20 - 30 * q, 0.14 + 0.1 * q, alpha=0.5 * (1 - q))
    chin = to_user(cr, pts["chin"])
    if t > tJ:
        star_on(cr, t, chin, alpha=prog(t, tJ, 0.2))
        if t < tJ + 1.2:
            red_ring(cr, chin[0], chin[1], 66, 54, prog(t, tJ + 0.15, 0.35), 8)
    if hand is not None and tT <= t < tJ + 0.1:           # the weapon flies from his hand to the child's chin
        u = clamp((t - tT) / max(0.3, tJ - tT))
        vx, vy = hand[0] + (chin[0] - hand[0]) * ease(u), hand[1] + (chin[1] - hand[1]) * ease(u) - 120 * math.sin(
            math.pi * u)
        trail(cr, [(hand[0] + (chin[0] - hand[0]) * ease(k / 20 * u), hand[1] + (chin[1] - hand[1]) * ease(k / 20 * u)
                    - 120 * math.sin(math.pi * k / 20 * u)) for k in range(21)], 0.7 * (1 - prog(t, tJ, 0.15)), 0.6)
        glow(cr, vx, vy, 160, 0.8)
        prop(cr, "md_vajra", vx, vy, 0.4, rot=t * 9, alpha=1 - prog(t, tJ, 0.1))
    if t > tJ - 0.05:
        bolt(cr, t, tJ - 0.05, (chin[0] - 260, chin[1] - 300), chin, 0.5, (0.65, 0.78, 1.0), 3)
    dev_i = cr.user_to_device(ELE4[0] - 20, ELE4[1] + 150)                # under his storm cloud
    white = 0.85 * math.exp(-6 * max(0.0, t - tJ)) * (t > tJ)
    lg = lang(tl)

    def ui(cr):
        if t < tT - 0.1:
            head2(cr, t, "THE KING OF THE GODS,", t0 + 0.05, "INDRA", tI, big_size=270)
        elif t < tJ - 0.05:
            head2(cr, t, "THREW HIS", tT - 0.1, "WEAPON", tT + 0.05, big_size=270)
        else:
            head2(cr, t, "IT HIT HIS", tJ - 0.05, CHIN_W[lg] + "!", tJ + 0.05, big_size=280)
        tag(cr, t, tI + 0.1, "INDRA", dev_i[0], dev_i[1], 40, alpha=ia)
        plate(cr, t, tI + 0.4, "KING OF THE GODS", dev_i[0] + 20, dev_i[1] + 64, 28, alpha=ia)
    return dict(ui=ui, white=white, flash=flash_at(t, t_in, 0.35) + flash_at(t, tT, 0.25) + flash_at(t, t_land, 0.15))


# ------------------------------------------------------------------ h6  chin = hanu, so: Hanuman


HILL5 = (540, 1960, 0.66)
CARD5A = (540, 760, 0.78)
CARD5B = (540, 1050, 0.82)


def word_plaque(cr, t, t_in, x, y, s, words, alpha=1.0, maxw=600.0):
    """A leather plaque dropping in on its rod with one row of words, centred and shrunk to fit maxw (plaque units):
    words = [(kind, text, size, colour, t_show)] (kind 'indic' = the spoken word in the viewer's script, shaped by
    matplotlib; 'latin' = English)."""
    q = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    yy = y + 60 * (1 - q)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(sway(t, 0.008, 0.4, x * 0.01))
    cr.scale(s, s)
    pc.paint_part(cr, "plaque", a)
    cr.restore()
    pc.rod(cr, x, yy + 110 * s, x + 30, H + 60, alpha=0.5 * a)

    def width(kind, text, size):
        if kind == "indic":
            return indic_surface(text, int(size), tuple(INK)).get_width()
        return text_size(text, int(size))[0]
    gap = 34
    total = sum(width(k_, tx, sz) for k_, tx, sz, _, _ in words) + gap * (len(words) - 1)
    f = s * min(1.0, maxw / max(1.0, total))
    cx = x - total * f / 2
    for kind, text, size, col, ts in words:
        w = width(kind, text, size) * f
        p = prog(t, ts, 0.25) * a
        if p > 0.01:
            k = 1.15 - 0.15 * back(clamp((t - ts) / 0.3))
            cr.save()
            cr.translate(cx + w / 2, yy)
            cr.scale(k, k)
            if kind == "indic":
                su = indic_surface(text, int(size * f), tuple(col))
                cr.set_source_surface(su, -su.get_width() / 2, -su.get_height() / 2 - 4 * f)
                cr.paint_with_alpha(p)
            else:
                draw_text(cr, text, 0, 0, int(size * f), col, p, anchor="cm")
            cr.restore()
        cx += w + gap * f


def s_hanu(cr, t, tl, t0, t1):
    c = cues(tl, "h6")
    tC, tH, tN, tM = c["C"], c["H"], c["N"], c["M"]
    lg = lang(tl)
    hx, hy, hs = HILL5
    glow(cr, hx, hy - 700 * hs, 520, 0.35)
    prop(cr, "hn_hill", hx, hy, hs)
    tx, ty = hill_top(HILL5)
    bs = 0.5
    pts = baby(cr, t, tx - 10, ty - 56 * bs + 6, bs, mood="daze", arms=(-0.6, -0.2), legs=(-0.15, 0.1),
               rot=-math.pi / 2, tail=0.5, ph=0.3, rods=False)
    chin = to_user(cr, pts["chin"])
    star_on(cr, t, chin)
    ax, ay, a_s = CARD5A
    bx, by, b_s = CARD5B
    kind, hw, nw = ("indic", HANU_W[lg], NAME_W[lg]) if HAS_INDIC else ("latin", HANU_L[lg], NAME_L[lg])
    wa = [("latin", CHIN_W[lg], 120, INK, tC), ("latin", "=", 120, INK, tH - 0.1), (kind, hw, 150, RED, tH)]
    wb = [(kind, nw, 170, RED, tM)]
    chin_ring = prog(t, tC + 0.1, 0.4)

    def ui(cr):
        if t < tN - 0.1:
            head2(cr, t, "THE " + CHIN_W[lg] + " IS CALLED", t0 + 0.05, "HANU", tH, big_size=270)
        else:
            head2(cr, t, "SO HIS NAME BECAME", tN - 0.1, "HANUMAN", tM, big_size=250, under=tM + 0.4)
        word_plaque(cr, t, tC - 0.25, ax, ay, a_s, wa)
        if chin_ring > 0:
            red_ring(cr, chin[0] + 6, chin[1] - 4, 70, 56, chin_ring, 8)
            dotted(cr, [(ax - 200, ay + 90), (ax - 230, (ay + chin[1]) / 2), (chin[0] - 30, chin[1] - 70)],
                   prog(t, tC + 0.1, 0.5), 26, 6, RED, 0.85 * (1 - prog(t, tN - 0.1, 0.3)))
        if t > tN - 0.1:
            down_arrow(cr, ax, ay + 110, by - 110, prog(t, tN - 0.1, 0.35))
        word_plaque(cr, t, tM - 0.3, bx, by, b_s, wb)
    return dict(ui=ui, flash=flash_at(t, tH, 0.2) + flash_at(t, tM, 0.3))


# ------------------------------------------------------------------ h7  the gods give him powers; nobody can beat him


DEVAS7 = ((150, 0.5, False, 0.0), (330, 0.42, False, 1.1), (930, 0.5, True, 2.0), (750, 0.42, True, 0.6))
LOTUS7 = (540, G - 20)


def s_boons(cr, t, tl, t0, t1):
    c = cues(tl, "h7")
    tD, tP, tB = c["D"], c["P"], c["B"]
    glow(cr, 540, 1300, 640, 0.4)
    ground(cr)
    lx, ly = LOTUS7
    bs = 0.6
    feet = ly - 90 * 0.5
    hands = []
    for i, (x, s, fl, ph) in enumerate(DEVAS7):
        b, k, a = depth(t, tD - 0.25 + 0.12 * i, 0.5)
        give = keyed(t, [(t0, 0.0), (tP - 0.2 + 0.1 * i, 1.0)], 0.3, 1.3)
        pts = deva(cr, t, x, s * k, pose="garland" if give > 0.5 else "stand", feet=G + (20 if s < 0.45 else 0),
                   flip=fl, alpha=a, blur=b + (4 if s < 0.45 else 0), ph=ph)
        if pts:
            hands.append(to_user(cr, pts["handF"]))
    aura_a = 0.25 + 0.75 * prog(t, tP, 1.4)
    if t > tB - 0.1:                                    # nobody can beat him: a huge shadow of his strength
        q = clamp((t - tB + 0.1) / 0.3)
        silhouette(cr, lambda c_: hanu(c_, t, lx + 20, 0.95, mood="calm", feet=G + 40, rods=False, ph=0.2,
                                       gada=False, front=(-2.7, -0.3), backa=(-2.5, -0.4)), 0.3 * q,
                   (0.35, 0.16, 0.06))
    prop(cr, "md_lotus", lx, ly, 0.5, rot=sway(t, 0.008, 0.4))
    flex = keyed(t, [(t0, 0.0), (tP + 0.6, 1.0), (tB, 2.0)], 0.3, 1.3)
    arms = mix((-0.3, 0.3), (-2.6, 2.6), min(1.0, flex)) if flex <= 1 else mix((-2.6, 2.6), (-2.9, -2.7), flex - 1)
    bpts = baby(cr, t, lx, baby_y(feet, bs), bs, mood="happy" if t > tP + 0.4 else "wonder", arms=arms, ph=0.5,
                aura_a=aura_a, hits=[(tP + 0.6, 0.5), (tB, 0.6)])
    chest = to_user(cr, bpts["chest"])
    for i, h in enumerate(hands):
        flow(cr, t, tP + 0.1 * i, tB, h, chest, n=8, lift=170, alpha=0.9, r=24, dur=0.9)
    if t > tB:
        burst(cr, t, chest[0], chest[1] - 60, tB, n=18, rmax=520, alpha=0.7)

    def ui(cr):
        if t < tB - 0.1:
            head2(cr, t, "THE GODS GAVE HIM", t0 + 0.05, "POWERS", tP, big_size=280)
        else:
            head2(cr, t, "NOW NOBODY COULD", tB - 0.1, "BEAT HIM!", tB + 0.05, big_size=270)
        tag(cr, t, tD + 0.2, "THE GODS", 540, 1010, 38, t_out=tB - 0.2)
    return dict(ui=ui, flash=flash_at(t, tP, 0.25) + flash_at(t, tB, 0.3))


# ------------------------------------------------------------------ h8  naughty! the sages' hut; he throws things


def s_play(cr, t, tl, t0, t1):
    c = cues(tl, "h8")
    tN, tK, tT = c["N"], c["K"], c["T"]
    on = tK - 0.25
    if t > on:
        b, k, a = depth(t, on, 0.5)
        hermitage(cr, t, alpha=a, blur=b, flare=0.8 * math.exp(-2 * max(0.0, t - tT)) * (t > tT))
        for i in range(len(ITEMS)):
            sp, x, y, s, rot = item_at(t, i, tT + 0.12 * i)
            prop(cr, sp, x, y, s, rot=rot, alpha=a, blur=b)
    else:
        glow(cr, 540, 1350, 560, 0.45)
        ground(cr)
    if t < on:                                          # bouncing about, up to mischief
        hop = abs(math.sin(math.pi * (t - t0) / 0.55))
        bs = 0.8
        baby(cr, t, 540, baby_y(G, bs) - 170 * hop, bs, mood="cheeky" if t > tN else "happy",
             arms=(-1.9 + 0.3 * hop, 1.3 - 0.3 * hop), legs=(-0.5 * hop, 0.4 * hop), tail=0.4 * hop,
             rot=0.08 * math.sin(t * 5), ph=0.2, aura_a=0.45, hits=[(tN, 0.6)])
    else:                                               # hopping into the hut's yard: three hops, then a flip
        bs = 0.62
        n = 3
        u = clamp((t - on) / max(0.9, tT - on))
        k_ = min(n - 1, int(u * n))
        f = u * n - k_
        x = -60 + (400 + 60) * (k_ + ease(f)) / n
        hop = math.sin(math.pi * f) * (1 if u < 1 else 0)
        flip_r = 2 * math.pi * ease(clamp((t - tT) / 0.6))
        up = math.sin(math.pi * clamp((t - tT) / 0.6)) * 260
        baby(cr, t, x, baby_y(G, bs) - 220 * hop - up, bs, mood="cheeky", arms=(-2.4, -2.0),
             legs=(-0.6 * hop, 0.5 * hop), tail=0.5, rot=0.25 * hop + flip_r, ph=0.2, aura_a=0.35,
             rods=t < tT)

    def ui(cr):
        if t < tK - 0.1:
            head2(cr, t, "BUT LITTLE KIDS ARE", t0 + 0.05, "NAUGHTY!", tN, big_size=280)
        elif t < tT - 0.1:
            head2(cr, t, "HE RAN INTO THE", tK - 0.1, "SAGES' HUT", tK + 0.05, big_size=250)
        else:
            head2(cr, t, "AND THREW THEIR THINGS", tT - 0.1, "EVERYWHERE!", tT + 0.05, big_size=240)
    return dict(ui=ui, flash=flash_at(t, tN, 0.2) + flash_at(t, tT, 0.25))


# ------------------------------------------------------------------ h9  the sages get angry: "you will forget it all"


BB9 = (230, 0.62)


def s_curse(cr, t, tl, t0, t1):
    c = cues(tl, "h9")
    tA, tS, tF = c["A"], c["S"], c["F"]
    hermitage(cr, t, alpha=0.6, blur=5, fire=0.3)
    for i in range(len(ITEMS)):                         # everything he threw, lying about
        sp, x, y, s, rot = item_at(t, i, t0 - 0.85 + 0.12 * i)
        prop(cr, sp, x - 80, y, s, rot=rot, alpha=0.85, blur=2)
    bx, bs = BB9
    drain = prog(t, tF + 0.1, 1.0)
    bpts = baby(cr, t, bx, baby_y(G, bs), bs, mood="cheeky" if t < tA else ("wonder" if t < tF + 0.6 else "calm"),
                arms=mix((-0.3, 0.3), (-1.0, -0.9), prog(t, tS, 0.3)), head=0.06, ph=0.2,
                aura_a=0.55 * (1 - drain), hits=[(tS, 0.6)])
    target = to_user(cr, bpts["chest"])
    fury = prog(t, tA - 0.1, 0.35)
    shake = fury * 0.03 * math.sin(t * 30)
    hands, tops = [], []
    for who, x, s, ph, tin in (("khag", 700, 0.64, 0.3, t0 - 0.2), ("old", 900, 0.6, 1.1, t0)):
        b, k, a = depth(t, tin, 0.45)
        hy = G - 434 * s
        fr = point_to(x, hy, s, target, flip=True, bulk=0.95)
        point = keyed(t, [(t0, 0.0), (tS - 0.15, 1.0)], 0.25, 1.4)
        p = sage(cr, t, who, x, s * k, "shock" if t < tA - 0.1 else "angry", flip=True,
                 front=mix(mix((-0.6, -0.9), (-2.5, -0.4), fury * (1 - point)), fr, point), ph=ph, rot=shake,
                 alpha=a, blur=b, hits=[(tA, 0.5), (tS, 0.5)])
        hands.append(to_user(cr, p["handF"]))
        tops.append(to_user(cr, p["top"]))
    for tp in tops:
        anger_puffs(cr, t, tp[0] - 10, tp[1] + 40, fury * (1 - prog(t, tF + 0.5, 0.5)))
    for i, h in enumerate(hands):
        bolt(cr, t, tS + 0.05 * i, h, target, 0.9, (1.0, 0.45, 0.15), i)
        bolt(cr, t, tF + 0.05 * i, h, target, 0.7, (1.0, 0.45, 0.15), i + 4)
    if t > tF:                                          # his strength drains away
        for i in range(10):
            ti = tF + 0.1 * i
            u = (t - ti) / 1.0
            if 0 < u < 1:
                sparkle(cr, target[0] + 60 * math.sin(i * 2.3), target[1] - 80 + 260 * u * u, 22 * (1 - u), 1 - u)
    dev_s = cr.user_to_device(800, G - 1000 * 0.64)

    def ui(cr):
        if t < tS - 0.1:
            head2(cr, t, "THE SAGES GOT", t0 + 0.05, "ANGRY!", tA, big_size=290)
        else:
            head2(cr, t, "THEY SAID:", tS - 0.1, None, 0.0)
        tag(cr, t, t0 + 0.25, "THE SAGES", dev_s[0], dev_s[1], 38, t_out=tS)
        card2(cr, t, tS + 0.1, 540, 790, 0.95, [("YOU WILL FORGET", 70, INK, -50, tS + 0.3),
                                                ("ALL YOUR POWER!", 92, RED, 40, tF)])
    return dict(ui=ui, flash=flash_at(t, tA, 0.2) + flash_at(t, tS, 0.25) + flash_at(t, tF, 0.25),
                eve=0.3 * fury)


# ------------------------------------------------------------------ h10  he forgot: for years, an ordinary vanara


def year_leaf(cr, t, t0, t1, x, y, s, n=12, alpha=1.0):
    """A palm-leaf calendar flipping fast: YEAR 1, YEAR 2, ... (the leaf turns on its rings, edge-on)."""
    if alpha <= 0.01:
        return
    flips = clamp((t - t0) / max(0.6, t1 - t0)) * (n - 1)
    cur = int(flips)
    ph = flips - cur
    sy = abs(math.cos(math.pi * ph)) if cur < n - 1 else 1.0
    pc.rod(cr, x - 226 * s, y, x - 300, H + 60, alpha=0.5 * alpha)
    pc.rod(cr, x + 226 * s, y, x + 300, H + 60, alpha=0.5 * alpha)
    for k in range(4):
        yy = y + 2 * 46 * s + 10 + 9 * k
        cr.set_source_rgba(*INK, 0.7 * alpha)
        cr.set_line_width(3)
        cr.move_to(x - 250 * s + 8 * k, yy)
        cr.line_to(x + 250 * s - 8 * k, yy)
        cr.stroke()
    cr.save()
    cr.translate(x, y)
    cr.scale(s, max(0.03, sy) * s)
    cr.translate(0, 46)
    pc.paint_part(cr, "kk_leaf", alpha)
    if sy > 0.15:
        num = cur + 1 + (1 if ph > 0.5 and cur < n - 1 else 0)
        draw_text(cr, f"YEAR {num}", 0, 4, 64, RED if num == n else INK, 0.95 * alpha, HEAD_FONT, "cm", tracking=6)
    cr.restore()
    for sx in (-1, 1):
        cr.new_path()
        cr.arc(x + sx * 226 * s, y + 4, 15, 0, 2 * math.pi)
        cr.set_source_rgba(*RED, alpha)
        cr.set_line_width(7)
        cr.stroke()


def s_years(cr, t, tl, t0, t1):
    c = cues(tl, "h10")
    tF, tY, tV, tO = c["F"], c["Y"], c["V"], c["O"]
    glow(cr, 540, 1350, 560, 0.4)
    ground(cr)
    grow = clamp((t - tY - 0.2) / 1.4)
    fade = 1 - prog(t, tF, 1.0)
    for i, (x0, x1, fl, ph) in enumerate(((-150, 230, False, 0.4), (1230, 850, True, 1.6))):
        if t > tV - 0.3:                                # the other vanaras, just like him
            xx, bob, rock, legp = pc.hop_walk(t, tV - 0.3 + 0.15 * i, tV + 0.9 + 0.15 * i, x0, x1, 0.4)
            monkey(cr, t, xx, G + bob, 0.56, flip=fl, ph=ph, rot=rock, legs=(0.3 * legp, -0.3 * legp),
                   front=(-0.4, -0.5), rods=True)
    if grow < 1:
        bs = 0.68
        baby(cr, t, 540, baby_y(G, bs), bs, mood="calm", arms=(-0.2, 0.2), head=0.08 * (1 - fade), ph=0.4,
             aura_a=0.6 * fade, alpha=1 - grow, blur=10 * grow, rods=grow < 0.5)
        if tF < t < tF + 1.4:                           # the last of his light falls away
            for i in range(8):
                u = (t - tF - 0.12 * i) / 1.0
                if 0 < u < 1:
                    sparkle(cr, 540 + 70 * math.sin(i * 2.5), 1400 + 300 * u * u, 20 * (1 - u), 1 - u)
    if grow > 0:
        s = 0.5 + 0.12 * ease(grow)
        scratch = keyed(t, [(t0, 0.0), (tO + 0.1, 1.0)], 0.3, 1.3)
        hanu(cr, t, 540, s, mood="calm", alpha=grow, blur=10 * (1 - grow), backa=(0.25, -0.5), rods=grow > 0.5,
             front=mix((-0.32, -0.55), (-2.6, -1.3), scratch), head=0.06 * scratch, ph=0.6)

    def ui(cr):
        if t < tY - 0.1:
            head2(cr, t, "AND HE REALLY", t0 + 0.05, "FORGOT", tF, big_size=280)
        elif t < tO - 0.1:
            head2(cr, t, "FOR MANY", tY - 0.1, "YEARS", tY + 0.05, big_size=280)
        else:
            head2(cr, t, "HE LIVED LIKE AN", tO - 0.1, "ORDINARY VANARA", tO + 0.05, big_size=220)
        if t > tY - 0.1:
            year_leaf(cr, t, tY, max(tY + 1.0, tO - 0.2), 540, 720, 1.25, n=12, alpha=prog(t, tY - 0.1, 0.3))
    days = 0.0
    if tY < t < tO:                                     # days and nights flicker past: years going by
        days = 0.22 * (0.5 + 0.5 * math.sin((t - tY) * 9.0)) * (1 - prog(t, tO - 0.4, 0.4))
    return dict(ui=ui, flash=flash_at(t, tY, 0.15) + flash_at(t, tO, 0.15), night=days, lift=1.0)


# ------------------------------------------------------------------ h11  one day: to find Sita, a huge ocean


ARMY = ((115, 0.42, False, 0.0), (300, 0.46, False, 1.2), (480, 0.4, True, 2.1), (660, 0.45, False, 0.7),
        (870, 0.42, True, 1.7))
ARC11 = ((420, 1270), (830, 905), 170)


def far_arc(cr, t, t_in):
    """A dotted arc over the sea from the shore to Lanka, with an arrowhead."""
    p0, p1, lift = ARC11
    p = prog(t, t_in, 0.8)
    if p <= 0:
        return
    pts = arc_path(p0, p1, lift, 50)
    dotted(cr, pts, p, 30, 7, RED, 0.9)
    if p >= 1:
        cr.save()
        cr.set_source_rgba(*RED, 0.9)
        ex, ey = pts[-1]
        pc.poly(cr, [(ex + 18, ey + 8), (ex - 30, ey - 16), (ex - 18, ey + 30)])
        cr.fill()
        cr.restore()


def s_ocean(cr, t, tl, t0, t1):
    c = cues(tl, "h11")
    tD, tS, tO = c["D"], c["S"], c["O"]
    shore(cr, t, lanka=prog(t, tS - 0.2, 0.5) * 0.7 + 0.3)
    if t > tS - 0.1:                                    # Sita Mata is there, far away: a small warm light
        q = prog(t, tS - 0.1, 0.4)
        glow(cr, 860, SEA_Y - 70, 200, 0.6 * q * (0.85 + 0.15 * math.sin(t * 3)))
        sparkle(cr, 860, SEA_Y - 80, 40 * q, q)
    for i, (x, s, fl, ph) in enumerate(ARMY):
        b, k, a = depth(t, t0 - 0.3 + 0.1 * i, 0.5)
        look = prog(t, tO, 0.4)
        monkey(cr, t, x, 1790 + 24 * (i % 2), s * k, flip=fl if look < 0.5 else False, ph=ph, alpha=a, blur=b,
               front=mix((-0.4, -0.5), (-1.6, -0.2), look * (i % 2)))
    far_arc(cr, t, tO + 0.1)

    def ui(cr):
        if t < tS - 0.1:
            head2(cr, t, "THEN ONE", t0 + 0.05, "DAY...", tD, big_size=280)
        elif t < tO - 0.1:
            head2(cr, t, "TO FIND", tS - 0.1, "SITA MATA", tS + 0.05, big_size=270)
        else:
            head2(cr, t, "THEY HAD TO CROSS A", tO - 0.1, "HUGE OCEAN", tO + 0.05, big_size=260)
        tag(cr, t, tS + 0.1, "SITA MATA IS HERE", 820, 655, 34)
        plate(cr, t, tO + 0.6, "SO FAR AWAY!", 560, 1085, 44)
    return dict(ui=ui, flash=flash_at(t, tS, 0.15) + flash_at(t, tO, 0.15))


# ------------------------------------------------------------------ h12  nobody could jump that far; all sad


HS13 = (270, 0.6)                    # Hanuman seated: x, scale (soles on SIT_G)
JB13 = (760, 0.62)                   # Jambavan where he stops
SIT_G = 1800
SAD12 = ((590, 0.44, False, 0.3), (770, 0.42, True, 1.2), (950, 0.44, True, 2.0))


def s_sad(cr, t, tl, t0, t1):
    c = cues(tl, "h12")
    tJ, tU = c["J"], c["U"]
    shore(cr, t)
    far_arc(cr, t, t0 - 2.0)
    shake = prog(t, tJ, 0.25) * (1 - prog(t, tU - 0.2, 0.3))
    sad = prog(t, tU - 0.1, 0.5)
    for i, (x, s, fl, ph) in enumerate(SAD12):          # they shake their heads, then hang them low
        monkey(cr, t, x, 1790 + 24 * (i % 2) + 20 * sad, s, flip=fl, shake=shake, ph=ph, bow=sad,
               front=mix((-0.4, -0.5), (0.1, -0.2), sad), backa=mix((0.3, -0.4), (0.1, -0.2), sad),
               rot=0.06 * sad)
    x, s = HS13
    hanu_sit(cr, t, x, SIT_G, s, mood="sad", head=0.1 + 0.08 * sad, ph=0.6)

    def ui(cr):
        if t < tU - 0.1:
            head2(cr, t, "NOBODY COULD JUMP", t0 + 0.05, "THAT FAR", tJ, big_size=280)
        else:
            head2(cr, t, "EVERYONE SAT", tU - 0.1, "SAD", tU + 0.05, big_size=300)
        plate(cr, t, -1.0, "SO FAR AWAY!", 560, 1085, 44)
        if t > tJ:
            big_x(cr, 620, 1060, 520, 300, prog(t, tJ + 0.2, 0.35), alpha=0.9, lw=18)
    return dict(ui=ui, flash=flash_at(t, tJ, 0.15), night=0.12 * sad)


# ------------------------------------------------------------------ h12q  so now what? how will he remember?


def s_question(cr, t, tl, t0, t1):
    c = cues(tl, "h12q")
    tW, tR, tH = c["W"], c["R"], c["H"]
    tR = min(tR, tH - 0.1)
    shore(cr, t, lanka=0.5)
    x, s = HS13
    hanu_sit(cr, t, x, SIT_G, s, mood="sad", head=0.12 + 0.03 * math.sin(t * 0.9), ph=0.6, alpha=0.9)

    def ui(cr):                                         # the question card, a big red "?" over it
        head2(cr, t, "SO NOW WHAT?", t0 + 0.05, None, 0.0)
        qmark(cr, t, tW - 0.1, 540, 600, 320, RED)
        card2(cr, t, tW, 540, 900, 1.08, [("HOW WILL HE", 80, INK, -54, tW + 0.4),
                                          ("REMEMBER?", 104, RED, 34, tR)])
    return dict(ui=ui, flash=flash_at(t, tW, 0.15) + flash_at(t, tR, 0.2), night=0.1)


# ------------------------------------------------------------------ h13  Jambavan: "you once flew to the sun!"


BUB = (540, 780, 0.78)               # the thought bubble: x, y, scale (its trail to the lower left)


def bubble_inside(cr, t, bx, by, s, t_mode, alpha=1.0):
    """The memory in the bubble: the child leaping at the fruit-sun, again and again."""
    cr.save()
    cr.new_path()
    pc.ell(cr, bx, by, 290 * s, 200 * s)
    cr.clip()
    a = alpha * prog(t, t_mode, 0.3)
    sx, sy = bx + 150 * s, by - 60 * s
    sun(cr, t, sx, sy, 0.24, fruit=1.0, alpha=a)
    u = ((t - t_mode) / 1.4) % 1.0
    p0, p1 = (bx - 230 * s, by + 130 * s), (sx - 90 * s, sy + 40 * s)
    path = arc_path(p0, p1, 120 * s, 30, ease(clamp(u / 0.8)))
    trail(cr, path, 0.7 * a, 0.4)
    hx, hy = path[-1]
    baby(cr, t, hx, hy, 0.22, mood="happy", arms=(-2.45, -2.15), legs=(0.55, 0.95), rot=0.9, rods=False,
         alpha=a, ph=0.3)
    cr.restore()


def s_jamb(cr, t, tl, t0, t1):
    c = cues(tl, "h13")
    tK, tJ, tA, tS, tU = c["K"], c["J"], c["A"], c["S"], c["U"]
    shore(cr, t, lanka_s=0.22, lanka_x=955)
    x, s = HS13
    lift = prog(t, tU, 0.6)
    hanu_sit(cr, t, x, SIT_G, s, mood="sad" if t < tS else ("calm" if t < tU else "puzzled"),
             head=0.14 * (1 - lift) - 0.06 * lift, ph=0.6, hits=[(tU, 0.3)])
    jx, js = JB13
    t_in, t_stop = t0 - 0.1, max(tA, t0 + 1.2)
    xx, bob, rock, legp = pc.hop_walk(t, t_in, t_stop, 1200, jx, 0.62)
    b, k, a = depth(t, t_in, 0.5)
    talk = t > tS and int(t * 4.2) % 3 != 0
    gest = keyed(t, [(t0, 0.0), (tS, 1.0), (tU - 0.2, 2.0)], 0.3, 1.3)
    fr = (-0.6, -0.6) if gest < 0.5 else ((-1.3, -0.4) if gest < 1.5 else (-2.3, -0.5))
    jp = jamb(cr, t, xx, js * k, mood="speak" if talk else "calm", flip=True, feet=SIT_G + 10,
              y=SIT_G + 10 - 434 * js + bob, legs=(0.3 * legp, -0.3 * legp), rot=rock, alpha=a, blur=b, front=fr,
              ph=1.2, hits=[(t_stop, 0.8), (tS, 0.4)])
    top = jp["top"]
    bx, by, bs = BUB
    q = back(clamp((t - tS + 0.1) / 0.35), 1.5)
    if q > 0.01:
        prop(cr, "ar_think", bx, by, bs * (0.6 + 0.4 * q), rot=sway(t, 0.006, 0.4), alpha=clamp(q), flip=True)
        if q > 0.8:
            bubble_inside(cr, t, bx, by - 10, bs, tS + 0.1)

    def ui(cr):
        if t < tS - 0.1:
            head2(cr, t, "THE OLD KING OF THE BEARS,", t0 + 0.05, "JAMBAVAN", tJ, big_size=260)
            tag(cr, t, tJ + 0.1, "JAMBAVAN", min(top[0], 900), top[1] - 30, 40)
            plate(cr, t, tJ + 0.4, "KING OF THE BEARS", min(top[0], 860), top[1] + 40, 30)
        else:
            head2(cr, t, "HE SAID: YOU ONCE FLEW", tS - 0.1, "TO THE SUN!", tU, big_size=260)
    return dict(ui=ui, flash=flash_at(t, tJ, 0.15) + flash_at(t, tU, 0.2))


# ------------------------------------------------------------------ h14  the twist, slowly: he remembers; he grows


def s_grow(cr, t, tl, t0, t1):
    c = cues(tl, "h14")
    tR, tG = c["R"], c["G"]
    g = ease(clamp((t - tG + 0.1) / max(1.0, t1 - tG - 0.3)))
    shore(cr, t, palm=False)
    lit = prog(t, tR - 0.1, 0.5)
    k = 1 - 0.5 * g                                     # everything else small: they shrink back as he grows
    jx = JB13[0] + 140 * g
    jamb(cr, t, jx, JB13[1] * k, mood="smile" if t > tR else "calm", flip=True, feet=SIT_G + 10 + 60 * g,
         front=mix((-1.3, -0.4), (-2.6, -0.3), prog(t, tG, 0.5)), head=-0.15 * g, ph=1.2)
    for i, (x, fl, ph) in enumerate(((950, True, 0.3), (110, False, 1.4), (1010, True, 2.0))):
        if g > 0.05:
            monkey(cr, t, x, SIT_G + 60, 0.28 * k, flip=fl, ph=ph, alpha=clamp(g * 3),
                   front=(-2.7, -0.3), backa=(-2.5, -0.4), rot=0.05 * math.sin(t * 9 + ph))
    x0, s0 = HS13
    if t < tR + 0.35:
        stir = prog(t, t0 + 0.3, max(0.6, tR - t0 - 0.4)) * (1 - lit)   # a spark in his chest, slowly growing
        hp = hanu_sit(cr, t, x0, SIT_G, s0, mood="puzzled" if t < tR else "joy", head=-0.05 - 0.08 * stir, ph=0.6,
                      halo_a=lit)
        if stir > 0.01:
            ch = to_user(cr, hp["chest"])
            orb(cr, t, ch[0] + 10, ch[1] + 10, 12 + 26 * stir + 4 * math.sin(t * 7), 0.4 + 0.5 * stir)
            lights(cr, t, ch[0], ch[1], 140 * stir, 6, 0.8 * stir)
    else:
        x = x0 + (470 - x0) * g
        s = s0 + (0.98 - s0) * g
        feet = SIT_G + 10 + 70 * g
        glow(cr, x + 20, feet - 640 * s, 700 * s + 200, 0.5 * lit)
        up = keyed(t, [(tR, 0.0), (tR + 0.45, 1.0)], 0.3, 1.3)
        hanu(cr, t, x, s, mood="joy", halo_a=lit, feet=feet, front=mix((-0.5, -0.9), (-2.7, -0.25), up),
             backa=(0.25, -0.6), head=-0.08 * up, hits=[(tR + 0.35, 0.6), (tG, 0.4)], ph=0.6, rods=g < 0.7)
    if t > tR:
        hx_, hy_ = (x0 + 30, SIT_G - 500 * s0) if t < tG else (470, G - 600)
        burst(cr, t, hx_, hy_, tR, n=22, rmax=760, alpha=0.9)
        lights(cr, t, 470, 1300, 380, 14, 0.8 * lit)

    def ui(cr):
        if t < tG - 0.1:
            head2(cr, t, "AS SOON AS HE HEARD IT...", t0 + 0.05, "HE REMEMBERED!", tR, big_size=240,
                  under=tR + 0.5)
        else:
            head2(cr, t, "AND HE GREW AS BIG AS A", tG - 0.1, "MOUNTAIN", tG + 0.05, big_size=260)
    return dict(ui=ui, flash=flash_at(t, tR, 0.45) + flash_at(t, tG, 0.2))


# ------------------------------------------------------------------ h15  one giant jump across the ocean


LEAP = ((210, 1500), (860, 905), 420)    # from (his hip on the beach), to, how high the arc rises


def s_leap(cr, t, tl, t0, t1):
    c = cues(tl, "h15")
    tL, tO = c["L"], c["O"]
    shore(cr, t, lanka_s=0.42, lanka_x=870)
    for i, (x, ph) in enumerate(((330, 0.3), (450, 1.4), (90, 2.0))):
        cheer = prog(t, tL + 0.3, 0.3)
        monkey(cr, t, x, 1880, 0.3, ph=ph, front=mix((-0.4, -0.5), (-2.7, -0.3), cheer),
               backa=mix((0.3, -0.4), (-2.5, -0.4), cheer), rot=0.05 * cheer * math.sin(t * 9 + ph))
    p0, p1, lift = LEAP
    u = clamp((t - tL) / max(1.4, t1 - tL - 0.2))
    e = ease(u) if u < 1 else 1.0
    path = arc_path(p0, p1, lift, 70, max(0.001, e))
    if t > tL:
        trail(cr, path, 0.95, 1.2)
        for i in range(6):
            q = clamp((t - tL) / 0.8)
            prop(cr, "cloud", p0[0] + (i - 2.5) * (40 + 120 * q), p0[1] + 300 - 50 * q, 0.16 + 0.12 * q,
                 alpha=0.45 * (1 - q))
    if t < tL:
        crouch = keyed(t, [(t0, 0.0), (tL - 0.35, 1.0)], 0.25, 1.2)
        hanu(cr, t, p0[0], 0.62, mood="joy", halo_a=0.8, feet=p0[1] + 434 * 0.62 + 30 * crouch,
             front=mix((-1.2, -0.6), (0.6, -0.4), crouch), backa=(0.5, -0.3), rot=0.15 * crouch, ph=0.6)
    else:
        hx, hy = path[-1]
        s = 0.62 - 0.32 * e
        prev = path[-3] if len(path) > 3 else p0
        ang = math.atan2(hy - prev[1], hx - prev[0])
        glow(cr, hx, hy, 380 * s + 120, 0.6)
        hanu(cr, t, hx, s, mood="joy", halo_a=0.6, y=hy, rot=clamp(ang + math.pi / 2 - 0.2, 1.0, 1.85),
             front=(-2.75, -0.15), backa=(0.9, -0.3), legs=(0.6, 0.15), rods=False, ph=0.6, gada_tilt=1.0)

    def ui(cr):
        if t < tO - 0.1:
            head2(cr, t, "IN ONE", t0 + 0.05, "GIANT JUMP", tL, big_size=270)
        else:
            head2(cr, t, "HE CROSSED THE WHOLE", tO - 0.1, "OCEAN", tO + 0.05, big_size=280, under=tO + 0.5)
    return dict(ui=ui, flash=flash_at(t, tL, 0.3))


# ------------------------------------------------------------------ h15c  the hook's picture again: the sun-jumper


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "h15c")
    tS, tO, tL = c["S"], c["O"], c["L"]
    x, s, feet = HK
    hip = feet - 434 * s
    glow(cr, x + 80, feet - 760 * s, 620, 0.5)
    if t > tO - 0.1:                                     # the whole ocean, small at his feet
        q = prog(t, tO - 0.1, 0.5)
        cr.save()
        cr.rectangle(-200, 1700, W + 400, 400)
        cr.clip()
        prop(cr, "sx_wave2", 540 + 12 * math.sin(t), 1760 + 160 * (1 - q), 0.5, alpha=q)
        cr.restore()
        prop(cr, "rv_lanka", 930, 1772 + 160 * (1 - q), 0.14, alpha=q)
    fr = reach_arm(x, hip, s, 26 * 1.2, (x + 250 * s, hip - 300 * s))
    ba = reach_arm(x, hip, s, -14 * 1.2, (x + 175 * s, hip - 262 * s))
    pts = hanu(cr, t, x, s, mood="smile", gada=False, open_back=True, feet=feet, front=fr, backa=ba, head=0.22,
               halo_a=0.7, hits=[(tS, 0.25), (tL, 0.3)], ph=1.0)
    hf, hb = to_user(cr, pts["handF"]), to_user(cr, pts["handB"])
    for p, r in ((hb, 0.85), (hf, 1.0)):                 # the same palms as the first picture, now shining steadily
        hand_glow(cr, t, (p[0] + 6, p[1] - 6), 1.0, r)
    sq = back(clamp((t - tS) / 0.4), 1.5)                # where the "?" was: the sun he once flew to
    if sq > 0.01:
        sun(cr, t, 760, 900, 0.3 * sq, fruit=1.0, alpha=clamp(sq))
        dotted(cr, arc_path((hf[0] + 20, hf[1] - 60), (700, 960), 140, 40), prog(t, tS + 0.2, 0.6), 26, 6, RED,
               0.8 * clamp(sq))
    if t > tL - 0.1:                                     # one jump over the little ocean
        dotted(cr, arc_path((380, 1745), (900, 1745), 170, 40), prog(t, tL - 0.1, 0.5), 24, 6, RED, 0.9)

    def ui(cr):
        if t < tO - 0.1:
            head2(cr, t, "HE ONCE FLEW UP TO", t0 + 0.05, "THE SUN...", tS, big_size=270)
        else:
            head2(cr, t, "SO THE OCEAN WAS JUST", tO - 0.1, "ONE JUMP!", tL, big_size=280, under=tL + 0.4)
    return dict(ui=ui, flash=flash_at(t, tS, 0.2) + flash_at(t, tL, 0.25))


# ------------------------------------------------------------------ h16  the real hero?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "h16")
    tH, tA, tJ, tC = c["H"], c["A"], c["J"], c["C"]
    glow(cr, 540, 1420, 520, 0.45)
    ground(cr)
    hanu(cr, t, 330, 0.5, mood="smile", halo_a=0.6, feet=G, front=(-0.6, -0.9), backa=(0.25, -0.5), ph=0.6,
         hits=[(tA, 0.4)])
    jamb(cr, t, 760, 0.5, mood="smile", flip=True, feet=G, front=(-0.6, -0.9), ph=1.2, hits=[(tJ, 0.4)])
    cards = ((300, "HANUMAN?", tH + 0.1), (780, "JAMBAVAN?", tH + 0.3))

    def ui(cr):
        head2(cr, t, "WHO WAS", t0 + 0.05, "THE REAL HERO?", tH, big_size=220)
        for cx, txt, tc in cards:
            card(cr, t, tc - 0.25, cx, 760, 0.6, [(txt, 104, RED, 4)])
        if t > tA:
            if t < tJ:
                k, ts = 0, tA
            else:
                n = int((t - tJ) / 0.9)
                k, ts = (1 + n) % 2, tJ + 0.9 * n
            red_ring(cr, cards[k][0], 764, 240, 92, prog(t, ts, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tH, 0.15))


SHOTS = [   # (line, cue: None = line start, draw function, options)
    ("h1", None, s_hook, {"z": (1.0, 1.04)}),
    ("h2", None, s_book, {"z": (1.0, 1.03)}),
    ("h3", None, s_sun, {"z": (1.0, 1.04)}),
    ("h4", None, s_fly, {"z": (1.0, 1.03)}),
    ("h5", None, s_strike, {"z": (1.0, 1.03)}),
    ("h6", None, s_hanu, {"z": (1.0, 1.03)}),
    ("h7", None, s_boons, {"z": (1.0, 1.03)}),
    ("h8", None, s_play, {"z": (1.0, 1.03)}),
    ("h9", None, s_curse, {"z": (1.0, 1.04)}),
    ("h10", None, s_years, {"z": (1.0, 1.03)}),
    ("h11", None, s_ocean, {"z": (1.0, 1.03)}),
    ("h12", None, s_sad, {"z": (1.0, 1.04), "focus": (420, 1300)}),
    ("h12q", None, s_question, {"z": (1.0, 1.03)}),
    ("h13", None, s_jamb, {"z": (1.0, 1.03)}),
    ("h14", None, s_grow, {"z": (1.03, 1.0)}),
    ("h15", None, s_leap, {"z": (1.0, 1.03)}),
    ("h15c", None, s_callback, {"z": (1.0, 1.04)}),
    ("h16", None, s_end, {"z": (1.0, 1.03)}),
]


def _starts(tl):
    """Each shot's start (cached on the timeline under this module's own name, not shots.shot_at's)."""
    st = getattr(tl, "_hn_shot_starts", None)
    if st is None:
        st = []
        for k, (bid, cu, _, _) in enumerate(SHOTS):
            if k == 0:
                st.append(0.0)
                continue
            s = T(tl, bid, cu)
            if cu is not None:
                s -= CUT_LEAD
            st.append(max(s, st[-1] + MIN_SHOT))
        tl._hn_shot_starts = st
    return st


def shot_at(t, tl):
    st = _starts(tl)
    k = max(i for i, s in enumerate(st) if t >= s)
    return k, st[k], st[k + 1] if k + 1 < len(st) else tl.total


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl)
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
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a single
    hit as Indra's weapon strikes, a conch as the sages say "you will forget", shimmer as Hanuman remembers, a bell on
    the closing question, then (only where they fit) shimmer on the gods' powers, a conch on the giant jump and a
    damaru as the child flies at the sun. Chosen in THAT order of importance, each at least SFX_MIN_GAP from every
    sound already kept (as render_myth.calm_sfx keeps them), so the list returned is what plays (about 6 sounds); the
    bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["h5"]["J"], "hit", 0), (c["h9"]["F"], "conch", 0), (c["h14"]["R"], "shimmer", 0),
            (c["h16"]["H"], "bell", 0), (c["h7"]["P"], "shimmer", 0), (c["h15"]["L"], "conch", 0),
            (c["h4"]["U"], "damaru", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["h5"]["J"] - 0.35, "dip", 0.5), (c["h9"]["F"] - 0.3, "dip", 0.45), (c["h14"]["R"] - 0.3, "dip", 0.5)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
