"""Scenes for videos/kumbhakarna.py: "Kumbhakarna never asked for sleep: Saraswati sat on his tongue" (Valmiki
Ramayana, Uttara Kanda 10), in Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same
lamp-lit screen, two-tier headlines and rod-puppet motion as the Ruru, Dharmavyadha, Shani-Ganesha and Garuda Purana
reels, with the cast from kumbhakarna_cast. Rewritten 12 Nov 2026 so a 5-year-old can follow (owner: "so clear ... even
a 5 year old can understand"): one storyline, short headlines (2-5 words), Kumbhakarna, Brahma and Saraswati (Ravana
and Rama only as who's who), the hard word explained on a card (the goddess of speech), a mid-story question card
(k5q) and a callback to the hook (k13c), one idea on screen at a time, and one device that carries it all:
Kumbhakarna's giant jointed jaw with a tiny glowing Saraswati sitting on his tongue (the hook, her flight in, the
wish, her flight out, the twist, the callback).

Respect: Brahma, Saraswati and the gods with dignity and beauty; Kumbhakarna fierce but a little comic when sleepy. No
gore at all: his eating is fruit, sweets and a pot flying into his mouth, or a huge dark mouth-shadow over the world;
the drums and the elephants are comic: he simply keeps snoring; nobody is hurt on screen.

Every frame is a pure function of t. English on-screen text (Hindi only from now on; the Kannada reel gets its own
art, but the module still runs on a Kannada timeline) except where a card shows spoken words, which also show in the
viewer's script (shaped by matplotlib as in scenes_arjuna; left out without the Nirmala font): his wish (k8) and
Brahma's "so be it" (k9). Cues are words of the line in each language ({"hi": ..., "kn": ...}) with a fraction
fallback, kept in one table (CUES) that the scenes and sfx() both read, with minimum gaps so a fast voice can't bunch
the beats together. Timeline caches live under "_kb_" attributes.

Shot list (line: what is on the screen)
  k1  HOOK, frame 0: Kumbhakarna's giant face in profile, tilted back, mouth wide open, and on his tongue a tiny glowing
      Saraswati with her veena: KUMBHAKARNA NEVER ASKED FOR / SLEEP (big word in by 0.3 s, underlined on "sone"); his
      eyes pop open on "nahi"; ON HIS TONGUE (ringed); SARASWATI tag
  k2  a palm-leaf book rises and opens: THE RAMAYANA (ringed), BY SAGE VALMIKI: A TRUE STORY FROM / THE RAMAYANA
  k3  Kumbhakarna comes onto the cloth, then Ravana beside him (tags): KUMBHAKARNA WAS / RAVANA'S BROTHER; Ravana
      looks up at him, a red measuring line runs from the ground to his crown: A HUGE, HUGE / GIANT; mangoes, fruit,
      a plate of sweets and a whole pot fly into his chomping mouth: WHO ATE / ANYTHING!
  k4  a forest at night, a sacred fire, Kumbhakarna praying, hands joined: HE PRAYED TO / BRAHMA; Brahma comes down on
      his lotus in a shaft of light (tag): BRAHMA WAS / HAPPY; Brahma's cloud ASK FOR / ANYTHING!
  k5  three gods (dark figures with halos) hold their heads and tremble: THE OTHER GODS WERE / SCARED; the lamp dims, a
      huge dark mouth-shadow looms over the whole world (a leather globe): IF HE GETS POWER, / HE'LL EAT THE WORLD!
  k5q QUESTION: Brahma small, hand at his chin: BUT BRAHMA HAD / PROMISED; a big red "?" swings in over the card SO WHAT
      NOW?
  k6  a shaft of light and Saraswati appears with her veena, her swan gliding in, and a card with a speech bubble:
      GODDESS OF SPEECH; SO BRAHMA CALLED / SARASWATI; Brahma points: cloud GO, SIT ON / HIS TONGUE!
  k7  the giant face again, facing left; Saraswati floats beside it, shrinks in a ring of sparkles: SARASWATI BECAME /
      TINY; flies on a trail of light onto his tongue (ringed); his eyes go heavy: AND SAT ON / HIS TONGUE
  k8  Brahma on his lotus (left) and Kumbhakarna, huge (right), a glow at his mouth: cloud WHAT DO YOU WANT?; then his
      cloud I WANT TO SLEEP / FOR MANY YEARS! with the words in Hindi under it: BUT OUT OF HIS MOUTH CAME:
  k9  Brahma raises his hand in blessing: BRAHMA SAID: / SO BE IT!, a plaque with the words in Hindi; he fades away into
      a burst of light
  k10 Saraswati flies out of his mouth on a trail of light; he shakes his head, question marks pop up: SARASWATI FLEW
      OUT. THEN / HE UNDERSTOOD!; he clutches his head: cloud OH NO! / WHAT DID I ASK FOR?
  k11 THE TWIST, slowly: close on his face, the mouth opening; the tongue lights up and is ringed (HIS TONGUE): HIS OWN
      TONGUE / TRICKED HIM!
  k12 Rama and Ravana face each other, arrows flying: THEN CAME THE WAR: / RAMA vs RAVANA; Kumbhakarna asleep on the
      ground, snoring: AND KUMBHAKARNA WAS / FAST ASLEEP!
  k13 two drummers (dark figures) beat big drums at his ear, booming rings: TO WAKE HIM UP, / THEY BEAT DRUMS!; he
      snores on (STILL ASLEEP); two elephants walk right over his belly: THEY EVEN WALKED / ELEPHANTS ON HIM!, STILL
      SNORING!
  k13c CALLBACK to the hook: the same giant tilted-back face, mouth open, Saraswati glowing on his tongue, the whole
      world floating at his lips: HE COULD EAT / THE WHOLE WORLD...; his eyes close, z's rise, the world drifts away:
      BUT HIS OWN TONGUE / PUT HIM TO SLEEP
  k14 Kumbhakarna asleep on his bed, snoring gently (zzz, his belly rising): DID THE GODS / CHEAT HIM?; YES / NO cards,
      a red ring alternating
"""
import math

import cairo

import jayadratha_cast as J
import kumbhakarna_cast as KB
import puppet_core as pc
import six_cast_c as C6
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog
from puppet_core import H, W, depth, keyed, prop, puppet, sway
from scenes_arjuna import HAS_INDIC, cloud_text, indic_surface
from scenes_dharmavyadha import point_to
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, man_angles, motes, red_ring, sound_rings, woman_angles
from scenes_jayadratha import NIGHT, arrow_at, flash_at, silhouette, tag, tint, title_lift, to_user
from scenes_kaikeyi import ANJALI, card, fig, rama
from scenes_lakshman_rekha import book, sparkle
from scenes_mandhata import aura, beam, burst, held, lights, mix, reach_arm, warm, zzz
from scenes_ravana import head2, rv, rv_angles
from scenes_ruru import fire, flow, nods, plate, trees
from scenes_shani_ganesha import deva
from shots import T, starts

MISSES = set()                       # cue words not found in a line (falls back to fractions)
G = FEET + 120                       # the ground line of most sets
WISH = {"hi": "मुझे बहुत सालों तक सोना है!", "kn": "ನನಗೆ ಎಷ್ಟೋ ವರ್ಷ ನಿದ್ದೆ ಮಾಡಬೇಕು!"}
SO_BE = {"hi": "ठीक है, ऐसा ही होगा!", "kn": "ಸರಿ, ಹಾಗೇ ಆಗಲಿ!"}
SR_GLOW = (1.0, 0.94, 0.70)          # Saraswati's light


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
    "k1": (("N", {"hi": "सोने", "kn": "ನಿದ್ದೆಯ"}, 0.25, (("t0", 0.9),)),
           ("X", {"hi": "नहीं", "kn": "ಇಲ್ಲ"}, 0.45, (("N", 0.6),)),
           ("T", {"hi": "ज़ुबान", "kn": "ನಾಲಿಗೆ"}, 0.62, (("X", 0.5),)),
           ("S", {"hi": "सरस्वती", "kn": "ಸರಸ್ವತಿ"}, 0.8, (("T", 0.45),))),
    "k2": (("R", {"hi": "रामायण", "kn": "ರಾಮಾಯಣದ"}, 0.25, (("t0", 0.25),)),
           ("S", {"hi": "सच्ची", "kn": "ನಿಜವಾದ"}, 0.6, (("R", 0.4),))),
    "k3": (("K", {"hi": "कुंभकर्ण", "kn": "ಕುಂಭಕರ್ಣ"}, 0.02, ()),
           ("R", {"hi": "रावण", "kn": "ರಾವಣನ"}, 0.15, (("K", 0.45),)),
           ("B", {"hi": "बड़ा", "kn": "ದೊಡ್ಡ"}, 0.5, (("R", 0.9),)),
           ("E", {"hi": "खा", "kn": "ತಿಂದುಬಿಡ್ತಿದ್ದ"}, 0.82, (("B", 0.8),))),
    "k4": (("B", {"hi": "ब्रह्मा", "kn": "ಬ್ರಹ್ಮನ"}, 0.12, (("t0", 0.3),)),
           ("H", {"hi": "ख़ुश", "kn": "ಖುಷಿಯಾಗಿ"}, 0.45, (("B", 0.9),)),
           ("M", {"hi": "माँगो", "kn": "ಕೇಳು"}, 0.75, (("H", 0.8),))),
    "k5": (("D", {"hi": "देवता", "kn": "ದೇವತೆಗಳು"}, 0.1, ()),
           ("F", {"hi": "डर", "kn": "ಹೆದರಿದ್ರು"}, 0.2, (("t0", 0.4),)),
           ("P", {"hi": "ताक़त", "kn": "ಶಕ್ತಿ"}, 0.5, (("F", 0.9),)),
           ("W", {"hi": "दुनिया", "kn": "ಜಗತ್ತನ್ನೇ"}, 0.78, (("P", 0.6),))),
    "k5q": (("P", {"hi": "वचन", "kn": "ಮಾತು"}, 0.3, (("t0", 0.4),)),
            ("Q", {"hi": "क्या", "kn": "ಏನು"}, 0.75, (("P", 0.9),))),
    "k6": (("SP", {"hi": "बोलने", "kn": "ಮಾತಿನ"}, 0.2, (("t0", 0.5),)),
           ("S", {"hi": "सरस्वती", "kn": "ಸರಸ್ವತಿಗೆ"}, 0.38, (("SP", 0.5),)),
           ("K", {"hi": "कहा", "kn": "ಹೇಳಿದ"}, 0.52, (("S", 0.6),)),
           ("T", {"hi": "ज़ुबान", "kn": "ನಾಲಿಗೆ"}, 0.8, (("K", 0.6),))),
    "k7": (("C", {"hi": "छोटी", "kn": "ಚಿಕ್ಕದಾಗಿ"}, 0.15, (("t0", 0.4),)),
           ("K", {"hi": "कुंभकर्ण", "kn": "ಕುಂಭಕರ್ಣನ"}, 0.45, (("C", 0.6),)),
           ("T", {"hi": "ज़ुबान", "kn": "ನಾಲಿಗೆ"}, 0.68, (("K", 0.4), ("C", 1.3))),
           ("B", {"hi": "बैठ", "kn": "ಕೂತ್ರು"}, 0.85, (("T", 0.35),))),
    "k8": (("Q", {"hi": "क्या", "kn": "ಏನು"}, 0.25, (("t0", 0.4),)),
           ("O", {"hi": "निकला", "kn": "ಬಂತು"}, 0.6, (("Q", 0.9),)),
           ("Y", {"hi": "सालों", "kn": "ವರ್ಷ"}, 0.78, (("O", 0.4),)),
           ("S", {"hi": "सोना", "kn": "ನಿದ್ದೆ"}, 0.9, (("Y", 0.3),))),
    "k9": (("T", {"hi": "ठीक", "kn": "ಸರಿ"}, 0.35, (("t0", 0.4),)),
           ("A", {"hi": "ऐसा", "kn": "ಹಾಗೇ"}, 0.6, (("T", 0.35),)),
           ("G", {"hi": "होगा", "kn": "ಆಗಲಿ"}, 0.85, (("A", 0.6),))),
    "k10": (("O", {"hi": "बाहर", "kn": "ಹೊರಗೆ"}, 0.1, (("t0", 0.2),)),
            ("H", {"hi": "होश", "kn": "ಪ್ರಜ್ಞೆ"}, 0.35, (("O", 0.8),)),
            ("K", {"hi": "अरे", "kn": "ಅಯ್ಯೋ"}, 0.6, (("H", 1.2),)),
            ("D", {"hi": "माँग", "kn": "ಕೇಳಿಬಿಟ್ಟೆ"}, 0.85, (("K", 0.5),))),
    "k11": (("T", {"hi": "ज़ुबान", "kn": "ನಾಲಿಗೆಯೇ"}, 0.3, (("t0", 0.7),)),
            ("F", {"hi": "धोखा", "kn": "ಮೋಸ"}, 0.7, (("T", 0.9),))),
    "k12": (("R", {"hi": "राम", "kn": "ರಾಮ"}, 0.15, (("t0", 0.3),)),
            ("L", {"hi": "लड़ाई", "kn": "ಯುದ್ಧ"}, 0.45, (("R", 0.5),)),
            ("S", {"hi": "सो", "kn": "ನಿದ್ದೆಯಲ್ಲಿದ್ದ"}, 0.8, (("L", 0.9),))),
    "k13": (("J", {"hi": "जगाने", "kn": "ಎಬ್ಬಿಸೋಕೆ"}, 0.1, (("t0", 0.2),)),
            ("D", {"hi": "ढोल", "kn": "ಡೋಲು"}, 0.3, (("J", 0.5),)),
            ("H", {"hi": "हाथी", "kn": "ಆನೆಗಳನ್ನೂ"}, 0.72, (("D", 1.2),))),
    "k13c": (("W", {"hi": "दुनिया", "kn": "ಜಗತ್ತನ್ನೇ"}, 0.2, (("t0", 0.3),)),
             ("T", {"hi": "ज़ुबान", "kn": "ನಾಲಿಗೆಯೇ"}, 0.62, (("W", 1.2),)),
             ("Z", {"hi": "सुला", "kn": "ಮಲಗಿಸಿಬಿಟ್ಟಿತು"}, 0.85, (("T", 0.6),))),
    "k14": (("Q", {"hi": "धोखा", "kn": "ಮೋಸ"}, 0.42, (("t0", 0.6),)),
            ("Y", {"hi": "हाँ", "kn": "ಹೌದಾ"}, 0.68, (("Q", 0.5),)),
            ("C", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.85, (("Y", 0.5),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under this module's own attribute)."""
    cache = getattr(tl, "_kb_cues", None)
    if cache is None:
        cache = {}
        tl._kb_cues = cache
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


def ground(cr, y=G, alpha=1.0):
    prop(cr, "ground", W / 2, y + 6, 0.82, alpha=alpha)




def word_plaque(cr, t, t_in, text, label, x, y, s, color=RED, alpha=1.0, size=130):
    """A leather plaque dropping in on its rod, a spoken word big on it in the viewer's script and a small English label
    under it (without the Nirmala font the label alone, big)."""
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
    if HAS_INDIC:
        draw_text(cr, label, 0, 72, 36, INK, a, MONO_FONT, "cm", tracking=3)
    else:
        draw_text(cr, label, 0, 0, 96, color, a, anchor="cm")
    cr.restore()
    pc.rod(cr, x, yy + 110 * s, x + 30, H + 60, alpha=0.5 * a)
    if HAS_INDIC:
        su = indic_surface(text, int(size * s), tuple(color))
        k = min(1.0, 540 * s / max(1, su.get_width()))
        cr.save()
        cr.translate(x, yy - 22 * s)
        cr.scale(k, k)
        cr.set_source_surface(su, -su.get_width() / 2, -su.get_height() / 2)
        cr.paint_with_alpha(a)
        cr.restore()


def strip(cr, t, t_in, text, x, y, size, maxw=600):
    """Spoken words in the viewer's script on a parchment strip, shrunk to fit maxw (left out without the Nirmala
    font)."""
    if not HAS_INDIC or t < t_in:
        return
    q = prog(t, t_in, 0.3)
    su = indic_surface(text, size, INK)
    k = min(1.0, (maxw - 80) / max(1, su.get_width()))
    w_, h_ = su.get_width() * k, su.get_height() * k
    yy = y + 16 * (1 - q)
    cr.save()
    pc.poly(cr, [(x - w_ / 2 - 28, yy - h_ / 2 - 14), (x + w_ / 2 + 28, yy - h_ / 2 - 14), (x + w_ / 2 + 40, yy),
                 (x + w_ / 2 + 28, yy + h_ / 2 + 14), (x - w_ / 2 - 28, yy + h_ / 2 + 14), (x - w_ / 2 - 40, yy)])
    cr.set_source_rgba(0.97, 0.87, 0.62, 0.96 * q)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, q)
    cr.set_line_width(3.5)
    cr.stroke()
    cr.translate(x - w_ / 2, yy - h_ / 2)
    cr.scale(k, k)
    cr.set_source_surface(su, 0, 0)
    cr.paint_with_alpha(q)
    cr.restore()




def blink(t, times, dur=0.22):
    return any(0 < t - tb < dur for tb in times)


# ------------------------------------------------------------------ Kumbhakarna


KK_MOOD = {m: "kb_kk_head" + ("" if m == "open" else "_" + m) for m in KB.KK_MOODS}


def kk(cr, t, x, s, mood="open", **kw):
    """Kumbhakarna standing (feet on `feet`, default G)."""
    kw.setdefault("feet", G)
    return fig(cr, KB.KUMBHA, "kb_kk", t, x, s, swap={"kb_kk_head": KK_MOOD[mood]}, **kw)


def kk_reach(x, s, target, front=True, feet=G, flip=False):
    """(upper, fore) angles so one of his hands lands on target."""
    return reach_arm(x, feet - 434 * s, s, (26 if front else -14) * KB.KK_B, target, flip)


LIE_HAND = reach_arm(0, 0, 1, 26 * KB.KK_B, (150, -110))     # lying: his hand resting on his belly


def kk_lying(cr, t, x, ground_, s, mood="snore", alpha=1.0, blur=0.0, rods=True):
    """Kumbhakarna asleep on his back (head to the left, belly up), breathing slowly. Returns his points."""
    br = math.sin(t * 1.4)
    hy = ground_ - 96 * s - 4 * br * s / 0.6
    ang = man_angles("kb_kk", t, LIE_HAND, (0.25, -0.2), 0.1 + 0.03 * br, (0.06, -0.04), (), 0.3)
    return puppet(cr, KB.KUMBHA, x, hy, s, -math.pi / 2 + 0.01 * br, False, ang, alpha, blur,
                  swap={"kb_kk_head": KK_MOOD[mood]}, rods=rods)


HINGE_CU = (KB.HINGE[0] * KB.CU, KB.HINGE[1] * KB.CU)


def face_cu(cr, t, nx, ny, sc, tilt, jaw, mood="open", inside=None, alpha=1.0, flip=False, cavity=True):
    """The giant close-up head: neck at (nx, ny), scale sc, tilted back by tilt; the jaw opened by `jaw` radians;
    inside(cr, seat) draws what sits on his tongue (scene coordinates). The pieces (neck, mouth, jaw, head, what sits
    on the tongue, tusks, ear ornament) are stacked like one leather puppet, then laid on the lit cloth together, so
    they don't darken each other where they overlap. Returns its points (scene)."""
    m0 = cr.get_matrix()
    ov = cairo.OPERATOR_OVER
    cr.push_group()
    cr.save()
    cr.translate(nx, ny)
    cr.rotate(tilt + sway(t, 0.008, 0.28))
    cr.scale(-sc if flip else sc, sc)
    pc.paint_part(cr, "kb_cu_neck", 1.0, op=ov)
    if cavity:
        cr.save()
        cr.scale(KB.CU, KB.CU)
        KB.mouth_cavity(cr, jaw)
        cr.restore()
    cr.save()
    cr.translate(*HINGE_CU)
    cr.rotate(jaw)
    cr.translate(-HINGE_CU[0], -HINGE_CU[1])
    pc.paint_part(cr, "kb_cu_jaw", 1.0, op=ov)
    seat = cr.user_to_device(KB.TONGUE_SEAT[0] * KB.CU, KB.TONGUE_SEAT[1] * KB.CU)
    chin = cr.user_to_device(100 * KB.CU, 10 * KB.CU)
    cr.restore()
    pc.paint_part(cr, "kb_cu_up" + ("" if mood == "open" else "_" + mood), 1.0, op=ov)
    eye = cr.user_to_device(48 * KB.CU, -124 * KB.CU)
    lip = cr.user_to_device(KB.LIP_UP[0] * KB.CU, KB.LIP_UP[1] * KB.CU)
    top = cr.user_to_device(0, -420 * KB.CU)
    if inside is not None:            # she is drawn over the lips: her own light, then her (never hidden by them)
        cr.save()
        cr.set_matrix(m0)
        inside(cr, cr.device_to_user(*seat))
        cr.restore()
    cr.save()
    cr.translate(*HINGE_CU)
    cr.rotate(jaw)
    cr.translate(-HINGE_CU[0], -HINGE_CU[1])
    pc.paint_part(cr, "kb_cu_tusk", 1.0, op=ov)
    cr.restore()
    pc.paint_part(cr, "kb_cu_ear", 1.0, op=ov)
    cr.restore()
    pat = cr.pop_group()
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source(pat)
    cr.paint_with_alpha(alpha)
    cr.restore()
    return {k: cr.device_to_user(*v) for k, v in (("seat", seat), ("eye", eye), ("lip", lip), ("chin", chin),
                                                   ("top", top))}


def cu_seat(t, nx, ny, sc, tilt, jaw, flip=False):
    """Where face_cu puts the seat on his tongue (scene coordinates), without drawing anything."""
    px, py = KB.jaw_pt(KB.TONGUE_SEAT, jaw)
    px = -px if flip else px
    a = tilt + sway(t, 0.008, 0.28)
    k = sc * KB.CU
    return nx + k * (px * math.cos(a) - py * math.sin(a)), ny + k * (px * math.sin(a) + py * math.cos(a))


def lamp_disc(cr, x, y, r, a):
    """A disc of Saraswati's light painted into the puppet group (it lights the dark mouth and the face round her)."""
    if a <= 0.01:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 1.0, 0.99, 0.94, 0.97 * clamp(a))
    g.add_color_stop_rgba(0.55, 1.0, 0.92, 0.66, 0.75 * clamp(a))
    g.add_color_stop_rgba(1, 1.0, 0.80, 0.40, 0.0)
    cr.save()
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


# ------------------------------------------------------------------ Saraswati


VEENA_FRONT = reach_arm(0, 0, 1, 22, (104, -96))        # standing with the veena: the plucking hand at the strings
VEENA_BACK = reach_arm(0, 0, 1, -12, (-112, -246))      # and the other hand on its neck
SIT_FRONT = reach_arm(0, 0, 1, 22, (118, -96))          # seated with the veena on her lap
SIT_BACK = reach_arm(0, 0, 1, -12, (-90, -232))


def veena_cb(alpha=1.0, blur=0.0, seated=False, pluck=0.0):
    """extra= callback for her body: the veena held across her (the great gourd low in front, the neck rising over her
    back shoulder); seated adds her lap first."""
    def fn(cr_):
        if seated:
            pc.paint_part(cr_, "kb_saras_seat", alpha, blur)
        cr_.save()
        if seated:
            cr_.translate(28, -150)
            cr_.rotate(0.55 + 0.01 * pluck)
            cr_.scale(0.6, 0.6)
        else:
            cr_.translate(-10, -170)
            cr_.rotate(0.62 + 0.01 * pluck)
            cr_.scale(0.62, 0.62)
        pc.paint_part(cr_, "kb_veena", alpha, blur)
        cr_.restore()
    return fn


def saras(cr, t, x, s, mood="smile", feet=G, flip=False, alpha=1.0, blur=0.0, rods=True, head=0.0, hits=(), y=None,
          rot=0.0, front=None, backa=None):
    """Saraswati standing with her veena (feet on `feet`); her plucking hand moves gently."""
    pl = math.sin(t * 7.0)
    fr = front or (VEENA_FRONT[0] + 0.05 * pl, VEENA_FRONT[1] + 0.04 * pl)
    ba = backa or VEENA_BACK
    hy = feet - 470 * s if y is None else y
    ang = woman_angles("kb_saras", t, fr, ba, head, hits, 0.4)
    sw = {"kb_saras_head": "kb_saras_head" + ("" if mood == "open" else "_" + mood)}
    return puppet(cr, KB.SARAS, x, hy, s, rot + bob_rot(t, 0.4), flip, ang, alpha, blur, swap=sw, rods=rods,
                  extra={"kb_saras_body": veena_cb(alpha, blur, False, pl)})


def saras_sit(cr, t, x, base_y, s, mood="smile", flip=False, alpha=1.0, blur=0.0, rods=False, rot=0.0):
    """Saraswati seated cross-legged with the veena on her lap, her lap resting on base_y (tiny on his tongue)."""
    pl = math.sin(t * 7.0)
    hy = base_y - KB.SR_SEAT_H * s
    ang = woman_angles("kb_saras", t, (SIT_FRONT[0] + 0.05 * pl, SIT_FRONT[1] + 0.04 * pl), SIT_BACK, 0.0, (), 0.4)
    sw = {"kb_saras_body": "kb_saras_body_sit",
          "kb_saras_head": "kb_saras_head" + ("" if mood == "open" else "_" + mood)}
    return puppet(cr, KB.SARAS, x, hy, s, rot + bob_rot(t, 0.4, 0.008), flip, ang, alpha, blur, swap=sw, rods=rods,
                  extra={"kb_saras_body": veena_cb(alpha, blur, True, pl)})


def tiny_saras(cr, t, x, y, s, a=1.0, glow_k=1.0, notes=0.0, rot=0.0, grp=False):
    """The tiny glowing Saraswati (her lap at x, y): a warm light round her first (it lights the dark mouth too), then
    the figure; notes > 0 sends little sparks of music up from the veena. grp: drawn inside face_cu's puppet group
    (her light is a painted disc there; the caller adds the glow on the cloth afterwards)."""
    if a <= 0.01:
        return
    pulse = 0.85 + 0.15 * math.sin(t * 3.1)
    if grp:
        lamp_disc(cr, x, y - 290 * s, 560 * s * (0.95 + 0.1 * pulse), a * min(1.0, glow_k))
    else:
        glow(cr, x, y - 300 * s, 1100 * s, 0.75 * a * glow_k * pulse)
        warm(cr, x, y - 280 * s, 760 * s, 0.85 * a * glow_k, SR_GLOW)
        warm(cr, x, y - 280 * s, 420 * s, 0.9 * a * glow_k, (1.0, 0.98, 0.90))
    saras_sit(cr, t, x, y, s, alpha=a, rot=rot)
    if notes > 0:
        for i in range(5):
            u = (t * 0.7 + i / 5) % 1.0
            gx = x + 160 * s + 140 * s * math.sin(i * 1.9 + t) * u
            gy = y - 120 * s - 900 * s * u
            sparkle(cr, gx, gy, 90 * s * math.sin(math.pi * u), notes * a, SR_GLOW)


def fly_path(t, t0, t1, p0, p1, lift=220.0):
    """A point flying from p0 to p1 between t0 and t1 along an arc (eased); returns (x, y, u)."""
    u = ease(clamp((t - t0) / max(0.2, t1 - t0)))
    return (p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u - lift * 4 * u * (1 - u), u)


# ------------------------------------------------------------------ Brahma


def brahma(cr, t, x, ground_, s, front=(-0.7, -1.7), backa=(0.25, -1.0), flip=False, alpha=1.0, blur=0.0, glow_a=1.0,
           hits=(), rods=True):
    """Brahma (six_cast_c) seated cross-legged on his lotus (the lotus on ground_), the Vedas in his back hand."""
    sg = -1 if flip else 1
    if glow_a > 0:
        glow(cr, x, ground_ - 420 * s, 620 * s + 160, 0.6 * glow_a * alpha)
        aura(cr, t, x, ground_ - 520 * s, 240 * s, 760 * s, 0.4 * glow_a * alpha, n=22, spin=0.05)
    prop(cr, "md_lotus", x + sg * 30 * s, ground_ - 165 * s, s * 1.5, rot=sway(t, 0.005, 0.3, 2.0), alpha=alpha,
         blur=blur, flip=flip)
    hy = ground_ - 165 * s - C6.SEAT_H * s + 10 * s
    prop(cr, "c6_brahma_seat", x, hy, s, alpha=alpha, blur=blur, flip=flip)
    ang = man_angles("c6_brahma", t, front, backa, 0.0, (0.0, 0.0), hits, 0.8)
    return puppet(cr, C6.BRAHMA, x, hy, s, bob_rot(t, 0.8, 0.005), flip, ang, alpha, blur,
                  hide=("c6_brahma_legF", "c6_brahma_legB"), swap={"c6_brahma_body": "c6_brahma_body_sit"},
                  extra={"c6_brahma_armB_lo": held("c6_veda", backa, 0.8, dy=160, alpha=alpha, blur=blur)}, rods=rods)


def brahma_hip(ground_, s):
    return ground_ - 165 * s - C6.SEAT_H * s + 10 * s


BLESS = (-2.5, -0.4)                 # Brahma's front hand raised in blessing
THINK = (-0.9, -2.55)                # his hand at his chin, thinking


# ------------------------------------------------------------------ others


def ravana(cr, t, x, s, feet=G, kneel=False, front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, hits=(), flip=False,
           alpha=1.0, blur=0.0, mood="calm", ph=0.6):
    hy = feet - (250 if kneel else 434) * s
    ang = rv_angles(t, front, backa, head, (0.0, 0.0), hits, ph)
    return rv(cr, t, x, hy, s, bob_rot(t, ph), flip, ang, mood, alpha=alpha, blur=blur, kneel=kneel)


def mouth_of(cr, pts):
    return to_user(cr, pts["mouth"])


def shadow_mouth(cr, t, x, y, s, jaw, a):
    """The huge dark mouth-shadow of k5: the close-up head drawn as one flat shadow, the jaw working slowly."""
    if a <= 0.01:
        return
    silhouette(cr, lambda c: face_cu(c, t, x, y, s, 0.3, jaw, "open", flip=True, cavity=False), 0.92 * a)


# ------------------------------------------------------------------ k1  hook


HK = (300, 1520, 1.2, -0.42)         # the face: neck x, y, scale, tilt
SR_S = 0.27                          # the tiny Saraswati on his tongue


def bloom(cr, t, seat, s, k=1.0):
    """Saraswati's light spilling over the cloth and his face (drawn before face_cu)."""
    glow(cr, seat[0], seat[1] - 290 * s, 1000 * s, 0.75 * k * (0.9 + 0.1 * math.sin(t * 3.1)))


def music(cr, t, seat, a):
    """Little sparks of music rising from her veena."""
    for i in range(5):
        u = (t * 0.7 + i / 5) % 1.0
        sparkle(cr, seat[0] + 50 + 40 * math.sin(i * 1.9 + t) * u, seat[1] - 40 - 260 * u,
                26 * math.sin(math.pi * u), a, SR_GLOW)


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "k1")
    tN, tX, tT, tS = c["N"], c["X"], c["T"], c["S"]
    nx, ny, sc, tilt = HK
    glow(cr, 640, 1250, 640, 0.35)
    jaw = 0.6 + 0.1 * keyed(t, [(t0, 0.0), (tX - 0.05, 1.0)], 0.35, 1.3) + 0.015 * math.sin(t * 2.2)
    mood = "open" if blink(t, (tX - 0.05,), 0.7) else "daze"
    gk = 1.0 + 0.5 * flash_at(t, tS, 1.0, 3.0)
    seat = cu_seat(t, nx, ny, sc, tilt, jaw)
    bloom(cr, t, seat, SR_S, gk)

    def inside(cr_, seat_):
        tiny_saras(cr_, t, seat_[0], seat_[1] + 4, SR_S, 1.0, gk, grp=True)

    face_cu(cr, t, nx, ny, sc, tilt, jaw, mood, inside)
    music(cr, t, seat, 0.4 + 0.6 * prog(t, tS, 0.4))

    def ui(cr):
        head2(cr, t, "KUMBHAKARNA NEVER ASKED FOR", -1.0, "SLEEP", 0.3, big_size=250, ghost=-1.0, under=tN)
        if t > tT:
            red_ring(cr, seat[0] + 4, seat[1] - 62, 110, 105, prog(t, tT, 0.45), 9)
        tag(cr, t, tT + 0.15, "ON HIS TONGUE", min(seat[0] + 260, 860), seat[1] + 150, 36)
        tag(cr, t, tS + 0.1, "SARASWATI", min(seat[0] + 200, 880), seat[1] - 250, 40)
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.2) + flash_at(t, tT, 0.2) + flash_at(t, tS, 0.25))


# ------------------------------------------------------------------ k2  a true story from the Ramayana


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "k2")
    tR, tS = c["R"], c["S"]
    leaves = [(None, [("THE RAMAYANA", 104, HEAD_FONT)], 0),
              (tS, [("BY SAGE VALMIKI", 54, MONO_FONT)], 0)]
    book(cr, t, 540, 980, 0.86, leaves, t_in=t0 - 0.05, t_open=tR - 0.15, ring=(0, 0, 0, tR + 0.25))

    def ui(cr):
        head2(cr, t, "A TRUE STORY FROM", t0 + 0.05, "THE RAMAYANA", tR, big_size=230, under=tS + 0.2)
    return dict(ui=ui, flash=flash_at(t, tR, 0.25) + flash_at(t, tS, 0.15))


# ------------------------------------------------------------------ k3  Ravana's brother, a giant who ate anything


RV3 = (215, 0.6)                     # Ravana: x, scale
KK3 = (720, 0.98)                    # Kumbhakarna (facing left)
FOOD = ("mango", "c6_fruit", "md_kalasha", "mango", "c6_plate", "c6_fruit", "mango")


def s_brothers(cr, t, tl, t0, t1):
    c = cues(tl, "k3")
    tK, tR, tB, tE = c["K"], c["R"], c["B"], c["E"]
    ground(cr)
    glow(cr, 560, 1250, 640, 0.35)
    kx, ks = KK3
    eat = t > tE - 0.1
    chomp = eat and math.sin((t - tE) * 2 * math.pi * 2.2) > 0
    b, k, a = depth(t, tK - 0.3, 0.5)
    kp = kk(cr, t, kx, ks * k, mood=("hungry" if chomp else "speak") if eat else "open", flip=True,
            front=(-1.2, -0.9) if eat else (-0.35, -0.5), backa=(0.35, -0.4), alpha=a, blur=b, ph=1.0,
            y=G - 434 * ks - (k - 1) * 300 * ks, hits=[(tK, 0.3), (tE, 0.4)])
    rx, rs = RV3
    b, k, a = depth(t, tR - 0.25, 0.45)
    look = keyed(t, [(t0, 0.0), (tB - 0.1, 1.0)], 0.35, 1.3)
    rp = ravana(cr, t, rx, rs * k, alpha=a, blur=b, head=-0.22 * look, hits=[(tR, 0.3)], ph=0.2)
    top_k = to_user(cr, kp["top"])
    mouth = mouth_of(cr, kp)
    if t > tB - 0.1:                   # how tall he is: a measuring line beside him, ground to crown
        q = prog(t, tB - 0.1, 0.5)
        mx = kx + 230
        y0, y1 = G - 10, top_k[1] - 40
        ye = y0 + (y1 - y0) * q
        cr.save()
        cr.set_source_rgba(*RED, 0.9)
        cr.set_line_width(10)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(mx, y0)
        cr.line_to(mx, ye)
        cr.stroke()
        for yy in (y0, ye):
            cr.move_to(mx - 34, yy)
            cr.line_to(mx + 34, yy)
            cr.stroke()
        cr.restore()
    if eat:                            # food of every kind flies into his mouth
        for i, name in enumerate(FOOD):
            ts = tE - 0.1 + 0.32 * i
            u = (t - ts) / 0.75
            if 0 < u < 1:
                x0, y0 = (60 + 130 * (i % 4), 1700 - 60 * (i % 3))
                x = x0 + (mouth[0] - x0) * u
                y = y0 + (mouth[1] - y0) * u - 520 * 4 * u * (1 - u)
                prop(cr, name, x, y, (0.75 if name == "mango" else 0.45) * (1 - 0.5 * u), rot=t * 5 + i,
                     alpha=min(1.0, 5 * (1 - u)))
    dev_r = rp["top"]

    def ui(cr):
        if t < tB - 0.1:
            head2(cr, t, "KUMBHAKARNA WAS", t0 + 0.05, "RAVANA'S BROTHER", tR, big_size=190)
        elif t < tE - 0.1:
            head2(cr, t, "A HUGE, HUGE", tB - 0.1, "GIANT", tB + 0.05, big_size=270)
        else:
            head2(cr, t, "WHO ATE", tE - 0.1, "ANYTHING!", tE + 0.05, big_size=270)
        tag(cr, t, tK + 0.15, "KUMBHAKARNA", min(top_k[0] + 20, 860), max(600, top_k[1] - 60), 38, t_out=tB + 0.3)
        tag(cr, t, tR + 0.2, "RAVANA", dev_r[0], dev_r[1] - 60, 38)
    return dict(ui=ui, flash=flash_at(t, tR, 0.15) + flash_at(t, tB, 0.2) + flash_at(t, tE, 0.2))


# ------------------------------------------------------------------ k4  he prayed to Brahma; Brahma, happy: "ask!"


KK4 = (330, 0.9)
FIRE4 = (640, G + 6, 0.66)
BR4 = (850, 0.5)


def s_pray(cr, t, tl, t0, t1):
    c = cues(tl, "k4")
    tB, tH, tM = c["B"], c["H"], c["M"]
    t_in = tH - 0.4                    # Brahma comes down just before "khush"
    trees(cr, t, 0.9)
    ground(cr)
    flare = prog(t, tB - 0.1, 0.5)
    glow(cr, 480, G - 500, 700, 0.25 + 0.3 * flare)
    sk = prog(t, tB, 0.5) * (1 - prog(t, t_in, 0.3))      # Brahma's lotus of light, high up: whom he prays to
    if sk > 0.01:
        glow(cr, 830, 760, 300, 0.7 * sk)
        aura(cr, t, 830, 750, 60, 220, 0.6 * sk, n=16, spin=0.1)
        prop(cr, "md_lotus", 830, 800 - 30 * (1 - ease(sk)), 0.55, rot=sway(t, 0.01, 0.4), alpha=sk)
    kx, ks = KK4
    aura(cr, t, kx + 40, G - 700 * ks, 220 * ks, 760 * ks, 0.45 * flare, n=20, spin=0.05)
    kp = kk(cr, t, kx, ks, mood="open", front=ANJALI["front"], backa=ANJALI["backa"],
            head=0.14 * nods(t, (tB + 0.3,), 0.8), ph=1.0, hits=[(tB, 0.3)])
    fx, fg, fs = FIRE4
    fire(cr, t, fx, fg, fs * (1 + 0.3 * flare))
    lights(cr, t, fx, fg - 300, 160, 9, 0.5 + 0.4 * flare, (1.0, 0.72, 0.30), 0.9)
    if t > t_in:                       # Brahma comes down on his lotus in a shaft of light
        bx, bs = BR4
        beam(cr, bx, 260, 560, G, 0.8 * prog(t, t_in, 0.4))
        b, k, a = depth(t, t_in + 0.05, 0.6)
        yy = 240 * (1 - ease(clamp((t - t_in - 0.05) / 0.7)))
        cr.save()
        cr.translate(0, -yy)
        brahma(cr, t, bx, G, bs * k, flip=True, front=mix((-0.7, -1.7), BLESS, prog(t, tM - 0.2, 0.35)), alpha=a,
               blur=b, hits=[(tM, 0.3)])
        cr.restore()
    top_k = to_user(cr, kp["top"])

    def ui(cr):
        if t < t_in:
            head2(cr, t, "HE PRAYED TO", t0 + 0.05, "BRAHMA", tB, big_size=280)
        else:
            head2(cr, t, "BRAHMA WAS", t_in, "HAPPY", tH, big_size=280)
        tag(cr, t, t0 + 0.3, "KUMBHAKARNA", top_k[0] - 20, max(600, top_k[1] - 60), 36, t_out=t_in)
        tag(cr, t, tH + 0.1, "BRAHMA", BR4[0], 1080, 38, t_out=tM - 0.3)
        cloud_text(cr, t, 700, 800, 0.74, [("ASK FOR", 84, INK, -46, tM), ("ANYTHING!", 100, RED, 50, tM + 0.25)],
                   flip=True, t_in=tM - 0.25)
    return dict(ui=ui, night=0.18, lift=1.0, flash=flash_at(t, tB, 0.2) + flash_at(t, tH, 0.3))


# ------------------------------------------------------------------ k5  the other gods are scared: he'd eat the world


MOUTH5 = (930, 1600, 0.86)           # the mouth-shadow (facing left): neck x, y, scale
WORLD5 = (330, 1250, 0.95)


def s_gods(cr, t, tl, t0, t1):
    c = cues(tl, "k5")
    tD, tF, tP, tW = c["D"], c["F"], c["P"], c["W"]
    t_sh = tP - 0.3
    sh = prog(t, t_sh, 0.45)
    ground(cr)
    a1 = 1 - prog(t, t_sh - 0.1, 0.35)
    if a1 > 0.01:                     # the gods tremble, holding their heads
        for i, (dx, ds) in enumerate(((250, 0.6), (540, 0.66), (830, 0.6))):
            b_, k_, aa = depth(t, tD - 0.3 + 0.12 * i, 0.45)
            deva(cr, t, dx, ds * k_, pose="head" if t > tF - 0.1 else "stand", feet=G - 10, flip=i == 2,
                 alpha=a1 * aa, blur=b_, ph=i * 0.9, shake=prog(t, tF - 0.1, 0.2))
    if sh > 0.01:                     # a huge dark mouth-shadow looms over the whole world
        mx, my, ms = MOUTH5
        jaw = 0.25 + 0.25 * (0.5 + 0.5 * math.sin((t - t_sh) * 2.4))
        shadow_mouth(cr, t, mx + 160 * (1 - ease(sh)), my, ms, jaw, sh)
        wx, wy, ws = WORLD5
        q = back(clamp((t - t_sh) / 0.4), 1.5)
        prop(cr, "kb_world", wx, wy + 60 * (1 - q), ws * clamp(q), rot=0.05 * t, alpha=clamp(q))
        lights(cr, t, wx, wy, 260, 8, 0.4 * clamp(q))
        if t > tW:
            glow(cr, wx, wy, 300, 0.4 * prog(t, tW, 0.3) * (0.6 + 0.4 * math.sin(t * 6)))

    def ui(cr):
        if t < t_sh:
            head2(cr, t, "THE OTHER GODS WERE", t0 + 0.05, "SCARED", tF, big_size=280)
            tag(cr, t, tD + 0.3, "THE GODS", 540, 1060, 40, alpha=a1)
        else:
            head2(cr, t, "IF HE GETS POWER,", t_sh, "HE'LL EAT THE WORLD!", tW, big_size=190, under=tW + 0.5)
            plate(cr, t, t_sh + 0.4, "THE WHOLE WORLD", WORLD5[0], 1560, 32)
    return dict(ui=ui, night=0.3 * sh, lift=1.0, flash=flash_at(t, tF, 0.2) + flash_at(t, tW, 0.25))


# ------------------------------------------------------------------ k5q  QUESTION: Brahma had promised. What now?


BR5Q = (540, 0.6)


def big_qmark(cr, t, t_in, x, y, size):
    """A big red question mark swinging in on its rod."""
    q = back(clamp((t - t_in) / 0.4), 1.6)
    if q <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.rotate(0.1 * math.sin(t * 2.4) + 0.4 * (1 - q))
    cr.scale(q, q)
    draw_text(cr, "?", 0, 0, size, RED, clamp(q), anchor="cm")
    cr.restore()
    pc.rod(cr, x + 10, y + size * 0.42 * q, x + 60, H + 60, alpha=0.5 * clamp(q))


def s_question(cr, t, tl, t0, t1):
    c = cues(tl, "k5q")
    tP, tQ = c["P"], c["Q"]
    ground(cr)
    glow(cr, 540, 1400, 600, 0.4)
    bx, bs = BR5Q
    think = keyed(t, [(t0, 0.0), (tQ - 0.5, 1.0)], 0.3, 1.2)
    brahma(cr, t, bx, G, bs, front=mix(BLESS, THINK, think), hits=[(tP, 0.3)])
    if t < tQ - 0.5:                   # his promise: a glowing "word given" seal over his blessing hand
        q = prog(t, tP - 0.1, 0.35) * (1 - prog(t, tQ - 0.6, 0.3))
        lights(cr, t, bx + 90, G - 900 * bs, 120, 8, 0.8 * q)

    def ui(cr):
        if t < tQ - 0.45:
            head2(cr, t, "BUT BRAHMA HAD", t0 + 0.05, "PROMISED!", tP, big_size=270)
            card(cr, t, tP + 0.1, 540, 790, 0.78, [("HE SAID:", 52, INK, -50), ("ASK FOR ANYTHING!", 92, RED, 34)],
                 t_out=tQ - 0.7)
        else:
            head2(cr, t, "SO NOW", tQ - 0.45, "WHAT?", tQ - 0.2, big_size=300)
            big_qmark(cr, t, tQ - 0.35, 540, 820, 420)
    return dict(ui=ui, flash=flash_at(t, tP, 0.2) + flash_at(t, tQ, 0.25))


# ------------------------------------------------------------------ k6  Brahma calls Saraswati, the goddess of speech


BR6 = (250, 0.56)
SR6 = (770, 0.62)


def speech_card(cr, t, t_in, x, y, s, t_out=None):
    """The hard word, made simple: a plaque with a speech bubble and GODDESS OF SPEECH."""
    q = back(clamp((t - t_in) / 0.35), 1.4)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.25)
    a = clamp(q)
    if a <= 0.01:
        return
    yy = y + 60 * (1 - q)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(sway(t, 0.01, 0.4, x * 0.01))
    cr.scale(s, s)
    pc.paint_part(cr, "plaque", a)
    prop(cr, "lr_scloud", -262, -6, 0.2, alpha=a)
    for i in range(3):
        cr.new_path()
        cr.arc(-298 + 34 * i, -14, 8, 0, 2 * math.pi)
        cr.set_source_rgba(*INK, a)
        cr.fill()
    draw_text(cr, "GODDESS OF", 80, -36, 66, INK, a, anchor="cm")
    draw_text(cr, "SPEECH", 80, 42, 96, RED, a, anchor="cm")
    cr.restore()
    pc.rod(cr, x, yy + 110 * s, x + 30, H + 60, alpha=0.5 * a)


def s_call(cr, t, tl, t0, t1):
    c = cues(tl, "k6")
    tSP, tS, tK, tT = c["SP"], c["S"], c["K"], c["T"]
    ground(cr)
    bx, bs = BR6
    t_in = tSP - 0.3
    think = keyed(t, [(t0, 1.0), (tK - 0.2, 0.0)], 0.3, 1.2)
    speak = keyed(t, [(t0, 0.0), (tK - 0.15, 1.0)], 0.3, 1.3)
    sx, ss = SR6
    tgt = (sx - 40, G - 900 * ss)
    point = point_to(bx, brahma_hip(G, bs), bs, tgt, bulk=1.12)
    brahma(cr, t, bx, G, bs, front=mix(mix((-0.7, -1.7), THINK, think), point, speak), hits=[(tK, 0.3)])
    beam(cr, sx, 260, 600, G, 0.8 * prog(t, t_in - 0.1, 0.5))
    top = (sx, G - 900)
    if t > t_in - 0.1:
        b, k, a = depth(t, t_in, 0.6)
        glow(cr, sx, G - 600 * ss, 560, 0.6 * a)
        aura(cr, t, sx, G - 760 * ss, 160 * ss, 640 * ss, 0.45 * a, n=20, spin=0.06, col=(1.0, 0.88, 0.55))
        bs_, ks_, as_ = depth(t, tS, 0.5)
        sw_x = 600 + 120 * (1 - ease(clamp((t - tS) / 0.7)))
        prop(cr, "kb_swan", sw_x, G + 4, 0.5 * ks_, alpha=as_ * a, blur=bs_, rot=sway(t, 0.012, 0.5, 1.0),
             flip=True)
        sp = saras(cr, t, sx - 30, ss * k, mood="speak" if blink(t, (tSP + 0.1,), 0.6) else "smile", flip=True,
                   alpha=a, blur=b, y=G - 470 * ss - (k - 1) * 300 * ss, head=0.12 * nods(t, (tT + 0.4,), 0.6))
        lights(cr, t, sx, G - 520, 300, 10, 0.6 * a, (1.0, 0.95, 0.75))
        top = to_user(cr, sp["top"])
    if t < t_in:                       # Brahma thinks: a few sparks of light over his head
        q = prog(t, t0 + 0.1, 0.3) * (1 - prog(t, t_in - 0.2, 0.3))
        if q > 0:
            for i, r in enumerate((14, 22, 30)):
                sparkle(cr, bx + 70 + 40 * i, G - 1000 * bs - 60 * i, r, q, (1.0, 0.9, 0.6))

    def ui(cr):
        if t < tK - 0.15:
            head2(cr, t, "SO BRAHMA CALLED", t0 + 0.05, "SARASWATI", tS, big_size=250, under=tS + 0.4)
            speech_card(cr, t, tSP, 540, 770, 0.9, t_out=tK - 0.3)
        else:
            head2(cr, t, "BRAHMA TOLD HER:", tK - 0.15, None, 0.0)
        tag(cr, t, tS + 0.1, "SARASWATI", min(top[0] + 10, 880), top[1] - 70, 36, t_out=tK - 0.1)
        cloud_text(cr, t, 560, 770, 0.9, [("GO, SIT ON", 92, INK, -50, tK), ("HIS TONGUE!", 100, RED, 52, tT)],
                   t_in=tK - 0.25)
    return dict(ui=ui, flash=flash_at(t, tSP, 0.3) + flash_at(t, tT, 0.15))


# ------------------------------------------------------------------ k7  she becomes tiny and sits on his tongue


HK7 = (800, 1540, 1.3, 0.4)          # the face, facing left this time: neck x, y, scale, tilt
SR7 = 0.29
SR7_START = (250, 1100, 0.64)        # where she floats, still big, before she shrinks: lap x, y, scale


def s_enter(cr, t, tl, t0, t1):
    c = cues(tl, "k7")
    tC, tK, tT, tB = c["C"], c["K"], c["T"], c["B"]
    nx, ny, sc, tilt = HK7
    glow(cr, 440, 1250, 640, 0.35)
    land = tT
    jaw = 0.5 + 0.14 * prog(t, t0, 0.5) + 0.012 * math.sin(t * 2.2)
    mood = "daze" if t > tB - 0.1 else "open"
    seat = cu_seat(t, nx, ny, sc, tilt, jaw, flip=True)
    on = t >= land
    gk = 1.0 + flash_at(t, tB, 0.8, 3.0)
    if on:
        bloom(cr, t, seat, SR7, gk)

    def inside(cr_, seat_):
        if on:
            s_ = SR7 * (1 + 0.12 * math.exp(-5 * (t - land)) * math.sin((t - land) * 18))
            tiny_saras(cr_, t, seat_[0], seat_[1] + 4, s_, 1.0, gk, grp=True)

    pts = face_cu(cr, t, nx, ny, sc, tilt, jaw, mood, inside, flip=True)
    if not on:                         # she floats in, shrinks on "chhoti si", then flies onto his tongue
        x0, y0, s0 = SR7_START
        shrink = ease(clamp((t - tC + 0.05) / 0.6))
        s_now = s0 - (s0 - 0.36) * shrink
        t_fly = max(tC + 0.6, land - 1.0)
        x, y, u = fly_path(t, t_fly, land, (x0, y0), (seat[0], seat[1] + 4), lift=-140)
        if t > t_fly:
            s_now = 0.36 - (0.36 - SR7) * u
            flow(cr, t, t_fly, land, (x0, y0), (seat[0], seat[1] - 40), n=10, lift=-140, alpha=0.8, dur=0.7)
        if 0 < t - tC < 0.8:
            for i in range(8):         # sparkles round her as she shrinks
                a_ = 2 * math.pi * i / 8 + t * 3
                sparkle(cr, x + 200 * s_now * math.cos(a_), y - 300 * s_now + 260 * s_now * math.sin(a_), 22,
                        1 - (t - tC) / 0.8)
        tiny_saras(cr, t, x, y + 6 * math.sin(t * 2.4), s_now, prog(t, t0, 0.3), 0.8)
    if t > tB:
        burst(cr, t, seat[0], seat[1] - 80, tB, n=14, rmax=280, alpha=0.6)
    eye = pts["eye"]

    def ui(cr):
        if t < land - 0.1:
            head2(cr, t, "SARASWATI BECAME", t0 + 0.05, "TINY", tC, big_size=290)
        else:
            head2(cr, t, "AND SAT ON", land - 0.1, "HIS TONGUE", land, big_size=260, under=tB + 0.2)
        if t > tB:
            red_ring(cr, seat[0] - 4, seat[1] - 70, 120, 116, prog(t, tB, 0.45), 9)
        tag(cr, t, tK + 0.1, "KUMBHAKARNA", min(eye[0] + 40, 860), eye[1] - 260, 36, t_out=tB + 0.3)
    return dict(ui=ui, flash=flash_at(t, tC, 0.2) + flash_at(t, land, 0.25) + flash_at(t, tB, 0.2))


# ------------------------------------------------------------------ k8  "what do you want?" / "I want to sleep..."


BR8 = (200, 0.48)
KK8 = (830, 0.8)


def s_wish(cr, t, tl, t0, t1):
    c = cues(tl, "k8")
    tQ, tO, tY, tS = c["Q"], c["O"], c["Y"], c["S"]
    ground(cr)
    glow(cr, 540, 1300, 640, 0.35)
    bx, bs = BR8
    ask = keyed(t, [(t0, 0.0), (tQ - 0.15, 1.0), (tO, 0.0)], 0.3, 1.3)
    brahma(cr, t, bx, G, bs, front=mix((-0.7, -1.7), (-1.6, -0.3), ask), hits=[(tQ, 0.3)])
    kx, ks = KK8
    talk = t > tO and math.sin((t - tO) * 2 * math.pi * 2.4) > -0.3
    mood = "speak" if talk and t < tS + 0.9 else "daze"
    kp = kk(cr, t, kx, ks, mood=mood, flip=True, front=(-0.35, -0.5), backa=(0.3, -0.35), ph=1.0,
            head=0.04 * nods(t, (tO,), 0.4), hits=[(tO, 0.3)])
    m = mouth_of(cr, kp)
    gl = 0.6 + 0.3 * math.sin(t * 3.4) + 0.6 * flash_at(t, tO, 1.0, 3.0)
    glow(cr, m[0], m[1], 170, 0.8 * gl)
    warm(cr, m[0], m[1], 110, 0.8 * gl, SR_GLOW)
    sparkle(cr, m[0] - 6, m[1] - 4, 34 * gl, 0.9, SR_GLOW)

    def ui(cr):
        if t < tO:
            head2(cr, t, "BRAHMA ASKED:", t0 + 0.05, None, 0.0)
            cloud_text(cr, t, 420, 820, 0.78, [("WHAT DO YOU", 84, INK, -46, tQ), ("WANT?", 110, RED, 50, tQ + 0.2)],
                       t_in=tQ - 0.25)
        else:
            head2(cr, t, "AND OUT OF HIS MOUTH CAME:", tO - 0.1, None, 0.0)
            cloud_text(cr, t, 370, 800, 0.8, [("I WANT TO SLEEP", 86, INK, -48, tO + 0.1),
                                              ("FOR MANY YEARS!", 92, RED, 50, tY)], t_in=tO - 0.15, flip=True)
            strip(cr, t, tS + 0.15, WISH[lang(tl)], 375, 1090, 48, 600)
        tag(cr, t, t0 + 0.3, "BRAHMA", 200, 1200, 34, t_out=tO - 0.2)
    return dict(ui=ui, flash=flash_at(t, tO, 0.3) + flash_at(t, tS, 0.15))


# ------------------------------------------------------------------ k9  "so be it"


BR9 = (540, 0.66)


def s_sobeit(cr, t, tl, t0, t1):
    c = cues(tl, "k9")
    tT, tA, tG = c["T"], c["A"], c["G"]
    t_go = tG + 0.35
    ground(cr)
    x, s = BR9
    gone = prog(t, t_go, 0.6)
    raise_ = keyed(t, [(t0, 0.0), (tT - 0.2, 1.0)], 0.3, 1.4)
    if gone < 1:
        brahma(cr, t, x, G, s, front=mix((-0.7, -1.7), BLESS, raise_), alpha=1 - gone, blur=14 * gone,
               glow_a=1.0 + 0.6 * flash_at(t, tA, 1.0, 2.0), hits=[(tT, 0.4)])
    if t > tA:
        lights(cr, t, x, G - 520, 380, 14, 0.8 * (1 - 0.5 * gone))
    if t > t_go:
        burst(cr, t, x, G - 520, t_go, n=22, rmax=700, alpha=0.9)
        lights(cr, t, x, G - 700, 420, 16, 0.9 * (1 - prog(t, t_go + 1.0, 0.8)), (1.0, 0.92, 0.6), 0.8)

    def ui(cr):
        head2(cr, t, "BRAHMA SAID:", t0 + 0.05, "SO BE IT!", tA, big_size=270, under=tA + 0.4)
        word_plaque(cr, t, tT, SO_BE[lang(tl)], "OK, SO BE IT", 540, 760, 0.7, RED, size=110)
    return dict(ui=ui, flash=flash_at(t, tA, 0.45) + flash_at(t, t_go, 0.3))


# ------------------------------------------------------------------ k10  she flies out; "oh no! what did I ask for?"


KK10 = (330, 0.8)


def s_wake(cr, t, tl, t0, t1):
    c = cues(tl, "k10")
    tO, tH, tK, tD = c["O"], c["H"], c["K"], c["D"]
    ground(cr)
    glow(cr, 420, 1300, 600, 0.35)
    x, s = KK10
    hy = G - 434 * s
    shake = 0.16 * math.sin((t - tH) * 16) * math.exp(-2.6 * (t - tH)) if t > tH else 0.0
    clutch = keyed(t, [(t0, 0.0), (tK - 0.2, 1.0)], 0.3, 1.4)
    head_c = (x + 30 * s, hy - 300 * s - 150 * KB.HEAD_K * s)
    fr = mix((-0.35, -0.5), kk_reach(x, s, (head_c[0] + 70 * s, head_c[1] - 10 * s)), clutch)
    ba = mix((0.3, -0.35), kk_reach(x, s, (head_c[0] - 90 * s, head_c[1] - 20 * s), front=False), clutch)
    mood = "daze" if t < tH else "shock"
    rock = 0.05 * math.sin((t - tK) * 5) * clutch
    kp = kk(cr, t, x, s, mood=mood, front=fr, backa=ba, head=shake + 0.06 * clutch, rot=rock,
            hits=[(tH, 0.3), (tK, 0.4)], ph=1.0)
    m = mouth_of(cr, kp)
    if t < tO + 0.1:
        g = 0.6 + 0.3 * math.sin(t * 3.4)
        glow(cr, m[0], m[1], 170, 0.8 * g)
        warm(cr, m[0], m[1], 110, 0.8 * g, SR_GLOW)
    p1 = (1010, 560)
    if t > tO - 0.05:
        xx, yy, u = fly_path(t, tO - 0.05, tO + 1.4, (m[0] + 20, m[1] + 10), p1, lift=120)
        flow(cr, t, tO - 0.05, tO + 1.0, (m[0], m[1]), p1, n=10, lift=120, alpha=0.8, dur=0.7)
        if u < 1:
            tiny_saras(cr, t, xx, yy, 0.12 + 0.12 * u, 1 - prog(t, tO + 1.1, 0.3), 1.0)
    top = to_user(cr, kp["top"])

    def ui(cr):
        if t < tK:
            head2(cr, t, "SARASWATI FLEW OUT. THEN", t0 + 0.05, "HE UNDERSTOOD!", tH, big_size=220)
        fade = 1 - prog(t, tK - 0.35, 0.25)
        for i, (dx, dy, sz) in enumerate(((210, -10, 120), (330, 90, 96), (300, -140, 80))):
            ti = tH + 0.15 + 0.35 * i       # puzzled question marks pop up beside his head
            q = back(clamp((t - ti) / 0.3), 1.8)
            if q > 0.01 and fade > 0.01:
                cr.save()
                cr.translate(top[0] + dx, top[1] + 120 + dy + 8 * math.sin(t * 3 + i))
                cr.rotate(0.2 * math.sin(t * 2.2 + i))
                cr.scale(q, q)
                draw_text(cr, "?", 0, 0, sz, RED, clamp(q) * fade, anchor="cm")
                cr.restore()
        if t >= tK:
            head2(cr, t, "KUMBHAKARNA CRIED:", tK - 0.15, None, 0.0)
            cloud_text(cr, t, 770, 830, 0.8, [("OH NO!", 120, RED, -52, tK),
                                              ("WHAT DID I ASK FOR?", 74, INK, 58, tD)], t_in=tK - 0.2)
    return dict(ui=ui, flash=flash_at(t, tO, 0.2) + flash_at(t, tH, 0.2) + flash_at(t, tK, 0.15))


# ------------------------------------------------------------------ k11  THE TWIST: his own tongue tricked him


HK11 = (800, 1540, 1.3, 0.36)


def s_twist(cr, t, tl, t0, t1):
    c = cues(tl, "k11")
    tT, tF = c["T"], c["F"]
    glow(cr, 540, 1250, 640, 0.3)
    nx, ny, sc, tilt = HK11
    jaw = 0.12 + 0.52 * ease(clamp((t - tT + 0.4) / 0.8)) + 0.02 * math.sin(t * 2.2)
    seat = cu_seat(t, nx, ny, sc, tilt, jaw, flip=True)
    lit = prog(t, tT, 0.5)
    glow(cr, seat[0], seat[1] - 30, 300, 0.7 * lit * (0.85 + 0.15 * math.sin(t * 4)))
    face_cu(cr, t, nx, ny, sc, tilt, jaw, "angry" if t > tF - 0.1 else "daze", None, flip=True)
    if t > tF:
        burst(cr, t, seat[0], seat[1] - 20, tF, n=14, rmax=300, alpha=0.5)

    def ui(cr):
        head2(cr, t, "HIS OWN TONGUE", t0 + 0.05, "TRICKED HIM!", tF, big_size=270, under=tF + 0.5)
        if t > tT:
            red_ring(cr, seat[0] - 10, seat[1] - 10, 150, 90, prog(t, tT + 0.1, 0.5), 9)
        tag(cr, t, tT + 0.3, "HIS TONGUE", max(200, seat[0] - 240), seat[1] + 200, 40)
    return dict(ui=ui, flash=flash_at(t, tT, 0.15) + flash_at(t, tF, 0.35))


# ------------------------------------------------------------------ k12  the war began; he was asleep


RM12 = (230, 0.62)
RV12 = (850, 0.62)
KK12 = (680, 0.86)                   # asleep on the ground: hip x, scale


def body_top(x, kx, s):
    """The height of his sleeping body's top (belly up) above the ground at x, a smooth hill from head to feet."""
    return 250 * s * math.exp(-((x - (kx - 60 * s)) / (420 * s)) ** 2)


def sleeper_kk(cr, t, bump=0.0):
    """Kumbhakarna asleep on the ground (k12, k13), snoring; returns his head (scene)."""
    kx, ks = KK12
    kp = kk_lying(cr, t, kx, G + 4 * bump / 6, ks, mood="snore")
    head = to_user(cr, kp["head"])
    zzz(cr, t, head[0] + 20, head[1] - 110, 2.6)
    return head


def s_war(cr, t, tl, t0, t1):
    c = cues(tl, "k12")
    tR, tL, tS = c["R"], c["L"], c["S"]
    t_sl = tS - 0.25
    ground(cr)
    if t < t_sl:                       # the war: Rama and Ravana, arrows flying
        glow(cr, 540, 1250, 640, 0.3)
        b, k, a = depth(t, t0 - 0.1, 0.45)
        rx, rs = RM12
        rama(cr, t, rx, rs * k, ph=1.2, feet=G, front=(-1.5, -0.1), alpha=a, blur=b, hits=[(tL, 0.4)])
        b, k, a = depth(t, t0 + 0.15, 0.45)
        vx, vs = RV12
        ravana(cr, t, vx, vs * k, flip=True, mood="angry", front=(-1.4, -0.3), alpha=a, blur=b, hits=[(tL, 0.4)],
               ph=0.4)
        if t > tL - 0.2:
            for i in range(8):
                ts = tL - 0.2 + 0.26 * i
                u = (t - ts) / 0.6
                if 0 < u < 1:
                    if i % 2 == 0:
                        x0, x1, y0 = 330, 760, 1260 + 30 * (i % 3)
                        ang = 0.0
                    else:
                        x0, x1, y0 = 760, 330, 1230 + 30 * (i % 3)
                        ang = math.pi
                    arrow_at(cr, x0 + (x1 - x0) * u, y0 - 60 * math.sin(math.pi * u), ang, 150, 1 - u * u)
    else:                              # and Kumbhakarna? fast asleep
        glow(cr, 560, 1350, 640, 0.35)
        sleeper_kk(cr, t)

    def ui(cr):
        if t < t_sl:
            head2(cr, t, "THEN CAME THE WAR:", t0 + 0.05, "RAMA vs RAVANA", tL, big_size=210)
            tag(cr, t, tR + 0.1, "RAMA", RM12[0], 1030, 38)
            tag(cr, t, tR + 0.4, "RAVANA", RV12[0], 1030, 38)
        else:
            head2(cr, t, "AND KUMBHAKARNA WAS", t_sl, "FAST ASLEEP!", tS, big_size=250)
    return dict(ui=ui, eve=0.18 * (1 - prog(t, t_sl, 0.3)), flash=flash_at(t, tL, 0.2) + flash_at(t, t_sl, 0.2))


# ------------------------------------------------------------------ k13  drums, then elephants: still asleep


DRUMS = ((190, 0.6), (420, 0.58))    # the drummers behind his head and chest: x, scale


def drummer(cr, t, x, s, beat, ph=0.0, alpha=1.0, blur=0.0):
    """A drummer (a dark figure) with a dhol hung at his waist, beating it with a stick."""
    up = 0.5 + 0.5 * math.sin((t + ph) * 2 * math.pi * 3.0) if beat else 0.0
    fr = (-0.9 - 1.3 * up, -1.0 + 0.6 * up)
    hy = G - 434 * s
    silhouette(cr, lambda c_: fig(c_, J.SOLDIER, "jd_soldier", t, x, s, front=fr, backa=(-1.2, -0.8), feet=G,
                                  rods=False, ph=ph, extra={"jd_soldier_armF_lo": held("kb_stick", fr, 0.8,
                                                                                         dy=150)}), 0.85 * alpha)
    prop(cr, "kb_dhol", x + 120 * s, hy + 60 * s, 0.5 * s / 0.6, rot=0.05 * math.sin(t * 19 + ph) * beat,
         alpha=alpha, blur=blur)


def s_wakeup(cr, t, tl, t0, t1):
    c = cues(tl, "k13")
    tJ, tD, tH = c["J"], c["D"], c["H"]
    ground(cr)
    glow(cr, 560, 1350, 640, 0.35)
    kx, ks = KK12
    bump = 0.0
    els = ((tH - 0.2, 0.36), (tH + 0.55, 0.32))
    for ts, es in els:
        ex = -160 + (1300 + 160) * clamp((t - ts) / 2.8)
        for foot in (ex - 90 * es / 0.36, ex + 70 * es / 0.36):
            bump += 6 * math.exp(-((foot - kx) / 120) ** 2) * (t > ts)
    drums = 1 - prog(t, tH - 0.4, 0.4)
    if drums > 0.01:                   # drummers beat big drums right by his head
        for i, (dx, ds) in enumerate(DRUMS):
            b_, k_, a_ = depth(t, tJ - 0.2 + 0.15 * i, 0.4)
            drummer(cr, t, dx, ds * k_, t > tD - 0.1, ph=i * 0.17, alpha=drums * a_, blur=b_)
    head = sleeper_kk(cr, t, bump)
    if tD - 0.1 < t < tH:
        sound_rings(cr, 330, G - 260, t, tD - 0.1, 4, 0.26, 380, alpha=0.5 * drums)
    for ts, es in els:                 # two elephants walk right over him; he snores on
        if t < ts:
            continue
        u = clamp((t - ts) / 2.8)
        ex = -160 + (1300 + 160) * u
        ph = (t - ts) * 2.6
        fx0, fx1 = ex - 120 * es / 0.36, ex + 120 * es / 0.36
        h0, h1 = body_top(fx0, kx, ks), body_top(fx1, kx, ks)
        rot = math.atan2(-(h1 - h0), fx1 - fx0)
        y = G - 10 - (h0 + h1) / 2 - 10 * abs(math.sin(ph * math.pi))
        prop(cr, "sb_elephant", ex, y, es, rot=rot + 0.03 * math.sin(ph * math.pi))
        pc.rod(cr, ex, y - 300 * es, ex + 40, H + 60, alpha=0.4)

    def ui(cr):
        if t < tH - 0.15:
            head2(cr, t, "TO WAKE HIM UP,", t0 + 0.05, "THEY BEAT DRUMS!", tD, big_size=240)
            if t > tD + 0.5:
                tag(cr, t, tD + 0.5, "STILL ASLEEP", 790, 1380, 38, t_out=tH - 0.3)
        else:
            head2(cr, t, "THEY EVEN WALKED", tH - 0.15, "ELEPHANTS ON HIM!", tH, big_size=200)
            plate(cr, t, tH + 1.0, "STILL SNORING!", 540, 1150, 40)
    return dict(ui=ui, flash=flash_at(t, tD, 0.2) + flash_at(t, tH, 0.25))


# ------------------------------------------------------------------ k13c  CALLBACK: the world-eater, put to sleep


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "k13c")
    tW, tT, tZ = c["W"], c["T"], c["Z"]
    nx, ny, sc, tilt = HK
    glow(cr, 640, 1250, 640, 0.35)
    asleep = t > tZ
    jaw = 0.6 - 0.08 * prog(t, tZ, 0.6) + 0.015 * math.sin(t * 2.2)
    seat = cu_seat(t, nx, ny, sc, tilt, jaw)
    gk = 1.0 + 0.6 * flash_at(t, tT, 1.0, 3.0)
    sa = 1.0
    bloom(cr, t, seat, SR_S, gk * sa)
    wq = back(clamp((t - tW + 0.2) / 0.4), 1.5) * (1 - prog(t, tZ, 0.6))
    if wq > 0.01:                      # the whole world floating at his lips
        prop(cr, "kb_world", seat[0] + 330, seat[1] - 160 - 120 * prog(t, tZ, 0.6), 0.62 * clamp(wq),
             rot=0.05 * t, alpha=clamp(wq))

    def inside(cr_, seat_):
        tiny_saras(cr_, t, seat_[0], seat_[1] + 4, SR_S, sa, gk, grp=True)

    face_cu(cr, t, nx, ny, sc, tilt, jaw, "sleep" if asleep else "open", inside)
    music(cr, t, seat, 0.7 * sa)
    if asleep:
        zzz(cr, t, seat[0] + 120, seat[1] - 200, 2.6, prog(t, tZ, 0.4))

    def ui(cr):
        if t < tT - 0.1:
            head2(cr, t, "HE COULD EAT", t0 + 0.05, "THE WHOLE WORLD...", tW, big_size=200)
        else:
            head2(cr, t, "BUT HIS OWN TONGUE", tT - 0.1, "PUT HIM TO SLEEP", tZ, big_size=200, under=tZ + 0.5)
        if t > tT:
            red_ring(cr, seat[0] + 4, seat[1] - 62, 110, 105, prog(t, tT, 0.45), 9, sa)
    return dict(ui=ui, flash=flash_at(t, tW, 0.15) + flash_at(t, tT, 0.2) + flash_at(t, tZ, 0.2))


# ------------------------------------------------------------------ k14  did the gods cheat him?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "k14")
    tQ, tY, tC = c["Q"], c["Y"], c["C"]
    glow(cr, 540, 1400, 600, 0.42)
    ground(cr)
    bed_s = 1.55
    seat = G - 206 * bed_s
    prop(cr, "ar_cot", 540, G + 4, bed_s, rot=sway(t, 0.002, 0.3))
    prop(cr, "kb_pillow", 540 - 210 * bed_s, seat + 6, 0.95)
    kp = kk_lying(cr, t, 690, seat + 14, 0.7, mood="snore")
    head = to_user(cr, kp["head"])
    belly = to_user(cr, kp["belly"])
    zzz(cr, t, head[0] + 30, head[1] - 120, 2.4)
    zzz(cr, t, belly[0] - 40, belly[1] - 80, 1.6, 0.6, 0.5)
    cards = ((300, "YES", tQ + 0.05), (780, "NO", tQ + 0.25))

    def ui(cr):
        head2(cr, t, "DID THE GODS", t0 + 0.05, "CHEAT HIM?", tQ, big_size=250)
        for cx, txt, tc in cards:
            card(cr, t, tc - 0.25, cx, 760, 0.58, [(txt, 150, RED, 4)])
        if t > tY:
            n = int((t - tY) / 0.9)
            k = n % 2
            red_ring(cr, cards[k][0], 764, 232, 96, prog(t, tY + 0.9 * n, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tY, 0.15))


SHOTS = [   # (line, cue: None = line start, draw function, options)
    ("k1", None, s_hook, {"z": (1.0, 1.04)}),
    ("k2", None, s_book, {"z": (1.0, 1.03)}),
    ("k3", None, s_brothers, {"z": (1.0, 1.03)}),
    ("k4", None, s_pray, {"z": (1.0, 1.04)}),
    ("k5", None, s_gods, {"z": (1.0, 1.03)}),
    ("k5q", None, s_question, {"z": (1.0, 1.03)}),
    ("k6", None, s_call, {"z": (1.0, 1.03)}),
    ("k7", None, s_enter, {"z": (1.0, 1.05), "focus": (560, 1500)}),
    ("k8", None, s_wish, {"z": (1.0, 1.03)}),
    ("k9", None, s_sobeit, {"z": (1.0, 1.04)}),
    ("k10", None, s_wake, {"z": (1.0, 1.03)}),
    ("k11", None, s_twist, {"z": (1.0, 1.06), "focus": (560, 1450)}),
    ("k12", None, s_war, {"z": (1.0, 1.03)}),
    ("k13", None, s_wakeup, {"z": (1.0, 1.03)}),
    ("k13c", None, s_callback, {"z": (1.0, 1.04)}),
    ("k14", None, s_end, {"z": (1.0, 1.03)}),
]


def shot_at(t, tl):
    """(index, start, end) of the shot at t; the shot starts are cached on the timeline as _kb_starts."""
    st = getattr(tl, "_kb_starts", None)
    if st is None:
        st = tl._kb_starts = starts(tl, SHOTS)
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
    title_lift(cr, out.get("lift", 0.0) * out.get("night", 0.0) / NIGHT)
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a bell on
    "so be it", shimmer as Saraswati appears, a hit as the elephants step on him, a conch as Brahma comes, then (only
    where they fit) shimmer as she settles on his tongue, a damaru on his "oh no!", a bell on the closing question.
    Chosen in THAT order of importance, each at least SFX_MIN_GAP from every sound already kept (as
    render_myth.calm_sfx keeps them), so the list returned is what plays (about six sounds); the bed dips before the
    reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["k9"]["A"], "bell", 0), (c["k6"]["S"], "shimmer", 0), (c["k13"]["H"], "hit", 0),
            (c["k4"]["H"], "conch", 0), (c["k7"]["B"], "shimmer", 0), (c["k10"]["K"], "damaru", 0),
            (c["k14"]["Y"], "bell", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["k9"]["A"] - 0.3, "dip", 0.45), (c["k11"]["F"] - 0.3, "dip", 0.5), (c["k13"]["H"] - 0.3, "dip", 0.5)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
