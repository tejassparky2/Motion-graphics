"""Scenes for videos/andhe_ka_putra.py: Draupadi never said "andhe ka putra andha" (it is not in the Mahabharata), in
Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen, two-tier headlines
and rod-puppet motion as the Lakshman Rekha, Jayadratha, Arjuna and Shani reels, with the cast from andhe_cast. Told so
a 5-year-old can follow (owner, 12 Nov 2026: "so clear ... even a 5 year old can understand"): one idea on the screen
at a time, the one acting big and clearly doing it, short big English headlines, no section numbers, a callback to
the hook's card before the closing question.

Respect: Draupadi with dignity always (the popular TV version is shown small, inside an old TV, and only as what "we
all saw"); her father-in-law calm, his eyes closed; the fall is comic and harmless (he only gets wet, waist-deep).

Every frame is a pure function of t. English on-screen text except where a card shows a spoken word: the quote itself
(अंधे का पुत्र अंधा) and the word for envy (जलन), in the viewer's own script, shaped through matplotlib with
Nirmala.ttc (scenes_arjuna.indic_surface; Latin letters without the font). Cues are words of the line in each language
({"hi": ..., "kn": ...}) with a fraction fallback, kept in one table (CUES) that the scenes and sfx() both read, with
minimum gaps so a fast voice can't bunch the beats together. Hindi only is checked (the Kannada reel gets its own art
style); Kannada still draws, with its own cue words. Timeline caches live on the timeline under _ak_ names.

Shot list (line: what is on the screen)
  m1   HOOK, frame 0: the quote card alone and large, the line in the viewer's script: DRAUPADI NEVER SAID / THIS LINE
       (big words in by 0.3 s); Draupadi and Duryodhana come on small below (tags); on "kabhi" a dotted line from her
       lips to the card is crossed out; on "ye baat" the quote is ringed; on "hai hi nahi" a red stamp NOT IN THE /
       MAHABHARATA slams on and the big words are underlined
  m2   an old TV switches on: WE ALL SAW IT / ON TV; on its screen, small, the popular scene: Duryodhana walks into a
       pond and falls in (splash), Draupadi on a balcony laughs; a speech cloud with the line, then a red "?" stamp
  m3   a palm-leaf book rises and opens: VYASA'S MAHABHARATA; a magnifying lens sweeps the leaves: IN VYASA'S
       MAHABHARATA: / NOWHERE!; stamp NOT FOUND
  m4   SO WHAT / REALLY HAPPENED? and a big "?"; the five Pandavas (tag THE 5 PANDAVAS) and Duryodhana (tag), a dotted
       arc joining them, plate ONE BIG FAMILY: PANDAVAS & DURYODHANA: / COUSINS; then the crystal palace sparkles: THE
       PANDAVAS HAD A / MAGIC PALACE
  m5   the palace, soft, behind two panels: FLOOR (water light running over tiles) = WATER? (FLOOR LOOKED LIKE /
       WATER), then WATER (a pond under a skin of tiles that lifts off) = FLOOR? (WATER LOOKED LIKE / FLOOR)
  m6   the palace; Duryodhana walks in looking round: DURYODHANA WAS / WALKING AROUND; he strides proudly onto "floor"
       that is the pond: HE THOUGHT WATER WAS / FLOOR; he drops in waist-deep, a splash, the pond shows itself:
       AND... / SPLASH! (plate IT WAS WATER!)
  m7   Duryodhana waist-deep, ashamed; along the back, one by one, each laughing (HA! HA!) with a tag: BHIMA,
       SERVANTS, ARJUNA, NAKULA, SAHADEVA: SEEING THIS, / THEY LAUGHED
  m8   the slow reveal: the list on a parchment panel, WHO LAUGHED (in Vyasa's Mahabharata), five names ticked, an
       empty dotted sixth row with DRAUPADI faded, struck through on "naam", stamp NOT / WRITTEN: AND / DRAUPADI?, then
       DRAUPADI: / NOT EVEN NAMED
  m9   the throne room: his father on the throne, eyes closed (tag HIS FATHER); Duryodhana with his mace complains
       (cloud THEY ALL / LAUGHED AT ME!): LATER, TO HIS FATHER, / HE COMPLAINED; a thought bubble of Draupadi and two
       women laughing (tag HIS OWN CLAIM): HE SAID: DRAUPADI / LAUGHED TOO; the bubble goes, the quote card drops in
       and is stamped NOBODY / SAID IT: BUT THIS LINE? / NOBODY SAID IT
  m10  Duryodhana, a hand on his heart: WHAT REALLY / HURT HIM?; heaps of gold and a chest of gems (tag THE PANDAVAS'
       MONEY), Yudhishthira glowing in a ring of golden rays: THE PANDAVAS' / MONEY & GLORY; his stare hardens, a green
       glow and green flames at his heart, the spoken word (जलन) on a plaque: HE FELT / ENVY
  m10c CALLBACK: the hook's quote card again, Draupadi small and laughing below: THE LAUGH / WE ALL BLAME...; the card
       rises, she goes, Duryodhana comes on with the green glow at his heart, ringed: ITS REAL ROOT: / HIS OWN HEART
  m11  SO WHAT WAS / THE REAL CAUSE?; two cards DRAUPADI'S / LAUGH? and DURYODHANA'S / ENVY? over small Draupadi and
       Duryodhana, a red ring alternating
"""
import math

import cairo

import andhe_cast as AK
import arjuna_cast as A
import jayadratha_cast as J
import puppet_cast as C
import puppet_core as pc
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, text_size, tick
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_arjuna import HAS_INDIC, indic_surface
from scenes_dharmavyadha import point_to
from scenes_jarasandha import FADE, INK, RED, bob_rot, glow, man_angles, motes, red_ring, walk_legs, \
    woman_angles
from scenes_jayadratha import fit_size, flash_at, tag, tint, to_user
from scenes_kaikeyi import card, fig, q_stamp, stamp2
from scenes_lakshman_rekha import big_q, big_x, book, sparkle
from scenes_mandhata import aura, held, lights, mix, warm
from scenes_ravana import dotted, head2
from scenes_ruru import plate, sepia
from scenes_shani_ganesha import panel
from shots import T, starts

MISSES = set()                       # cue words not found in a line (falls back to fractions)
QUOTE = {"hi": "अंधे का पुत्र अंधा", "kn": "ಕುರುಡನ ಮಗ ಕುರುಡನೇ"}          # the famous line, in the viewer's script
QUOTE_LAT = {"hi": "ANDHE KA PUTRA ANDHA", "kn": "KURUDANA MAGA KURUDANE"}
ENVY = {"hi": "जलन", "kn": "ಹೊಟ್ಟೆಕಿಚ್ಚು"}                              # the spoken word for envy
ENVY_LAT = {"hi": "JALAN", "kn": "HOTTEKICHCHU"}
FLOOR_Y = 1330                       # the palace: the glass floor's back edge (the pillars stand on it)
STAGE = 1712                         # where people stand on the palace floor
GREEN_C = (0.30, 0.86, 0.32)


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, words)
    except (KeyError, ValueError):
        MISSES.add((bid, words[getattr(tl, "lang", "hi")] if isinstance(words, dict) else words))
        return T(tl, bid, frac)


# Every cue of every line: (name, {"hi": word, "kn": word}, fraction fallback, ((after, min gap), ...)); "t0" = the
# line's start. Words are exact substrings of the script lines (checked: MISSES stays empty); a word that comes twice
# in a line is given with its neighbour so the right one is found.
CUES = {
    "m1": (("D", {"hi": "द्रौपदी", "kn": "ದ್ರೌಪದಿ"}, 0.1, (("t0", 0.6),)),
           ("Y", {"hi": "दुर्योधन", "kn": "ದುರ್ಯೋಧನನಿಗೆ"}, 0.2, (("D", 0.6),)),
           ("K", {"hi": "कभी", "kn": "ಯಾವತ್ತೂ"}, 0.3, (("Y", 0.5),)),
           ("L", {"hi": "ये बात", "kn": "ಈ ಮಾತು"}, 0.7, (("K", 0.8),)),
           ("N", {"hi": "ही नहीं", "kn": "ದಲ್ಲೇ ಇಲ್ಲ"}, 0.92, (("L", 0.7),))),
    "m2": (("T", {"hi": "टीवी", "kn": "ಟಿವಿಯಲ್ಲಿ"}, 0.15, (("t0", 0.3),)),
           ("F", {"hi": "गिरा", "kn": "ಬಿದ್ದ"}, 0.45, (("T", 1.0),)),
           ("H", {"hi": "हँसकर", "kn": "ನಗ್ತಾ"}, 0.65, (("F", 0.6),)),
           ("Q", {"hi": "अंधे", "kn": "ಕುರುಡನ"}, 0.78, (("H", 0.5),))),
    "m3": (("V", {"hi": "व्यास", "kn": "ವ್ಯಾಸರು"}, 0.1, (("t0", 0.3),)),
           ("N", {"hi": "कहीं", "kn": "ಎಲ್ಲೂ"}, 0.75, (("V", 1.0),))),
    "m4": (("B", {"hi": "पांडव और", "kn": "ಪಾಂಡವರು"}, 0.3, (("t0", 1.0),)),
           ("C", {"hi": "चचेरे", "kn": "ಅಣ್ಣತಮ್ಮಂದಿರ"}, 0.5, (("B", 0.9),)),
           ("P", {"hi": "पांडवों का", "kn": "ಪಾಂಡವರಿಗೆ"}, 0.7, (("C", 1.0),)),
           ("J", {"hi": "जादुई", "kn": "ಮಾಯೆಯ"}, 0.82, (("P", 0.4),))),
    "m5": (("F", {"hi": "पानी जैसी", "kn": "ನೀರಿನ ಹಾಗೆ"}, 0.3, (("t0", 0.5),)),
           ("W", {"hi": "और पानी", "kn": "ನೀರು ನೆಲದ"}, 0.6, (("F", 0.9),)),
           ("L", {"hi": "जैसा", "kn": "ನೆಲದ ಹಾಗೆ"}, 0.9, (("W", 0.5),))),
    "m6": (("D", {"hi": "घूम", "kn": "ತಿರುಗಾಡ್ತಿದ್ದ"}, 0.15, (("t0", 0.3),)),
           ("S", {"hi": "लगा", "kn": "ಅಂದ್ಕೊಂಡು"}, 0.4, (("D", 0.8),)),
           ("A", {"hi": "आगे", "kn": "ಮುಂದೆ"}, 0.55, (("S", 0.5),)),
           ("B", {"hi": "छपाक", "kn": "ದಢಾರ್"}, 0.78, (("A", 0.9),))),
    "m7": (("B", {"hi": "भीम", "kn": "ಭೀಮ"}, 0.2, (("t0", 0.4),)),
           ("S", {"hi": "नौकर", "kn": "ಸೇವಕರು"}, 0.38, (("B", 0.6),)),
           ("A", {"hi": "अर्जुन", "kn": "ಅರ್ಜುನ"}, 0.6, (("S", 0.6),)),
           ("N", {"hi": "नकुल", "kn": "ನಕುಲ"}, 0.7, (("A", 0.4),)),
           ("D", {"hi": "सहदेव", "kn": "ಸಹದೇವನೂ"}, 0.8, (("N", 0.4),))),
    "m8": (("D", {"hi": "द्रौपदी", "kn": "ದ್ರೌಪದಿಯ"}, 0.35, (("t0", 0.6),)),
           ("N", {"hi": "नाम", "kn": "ಹೆಸರೇ"}, 0.6, (("D", 0.5),)),
           ("X", {"hi": "नहीं", "kn": "ಬರೆದಿಲ್ಲ"}, 0.82, (("N", 0.4),))),
    "m9": (("F", {"hi": "पिता", "kn": "ಅಪ್ಪನ"}, 0.15, (("t0", 0.4),)),
           ("C", {"hi": "शिकायत", "kn": "ದೂರು"}, 0.25, (("F", 0.4),)),
           ("D", {"hi": "द्रौपदी", "kn": "ದ್ರೌಪದಿನೂ"}, 0.35, (("C", 0.7),)),
           ("H", {"hi": "हँसी", "kn": "ನಕ್ಕಳು"}, 0.45, (("D", 0.4),)),
           ("Q", {"hi": "पर अंधे", "kn": "ಕುರುಡನ"}, 0.58, (("H", 0.8),)),
           ("K", {"hi": "किसी", "kn": "ಯಾರೂ"}, 0.85, (("Q", 0.9),))),
    "m10": (("R", {"hi": "चुभ", "kn": "ನೋವು"}, 0.3, (("t0", 0.7),)),
            ("W", {"hi": "पैसा", "kn": "ದುಡ್ಡು"}, 0.48, (("R", 0.8),)),
            ("G", {"hi": "शान", "kn": "ಗೌರವ"}, 0.6, (("W", 0.5),)),
            ("E", {"hi": "जलन", "kn": "ಹೊಟ್ಟೆಕಿಚ್ಚು"}, 0.88, (("G", 0.8),))),
    "m10c": (("L", {"hi": "हँसी", "kn": "ನಗು"}, 0.12, (("t0", 0.3),)),
             ("R", {"hi": "असली", "kn": "ಬೇರು"}, 0.55, (("L", 1.0),)),
             ("H", {"hi": "दिल", "kn": "ಮನಸ್ಸಲ್ಲಿತ್ತು"}, 0.88, (("R", 0.5),))),
    "m11": (("Q", {"hi": "असली", "kn": "ನಿಜವಾದ"}, 0.25, (("t0", 0.4),)),
            ("D", {"hi": "द्रौपदी", "kn": "ದ್ರೌಪದಿಯ"}, 0.45, (("Q", 0.5),)),
            ("Y", {"hi": "दुर्योधन", "kn": "ದುರ್ಯೋಧನನ"}, 0.65, (("D", 0.7),)),
            ("C", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.88, (("Y", 0.6),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_ak_cues", None)
    if cache is None:
        cache = {}
        tl._ak_cues = cache
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


# ------------------------------------------------------------------ text in the viewer's script


def native(cr, tl, words, latin, x, y, size, color=INK, alpha=1.0, maxw=None):
    """A spoken word or line in the viewer's own script (Devanagari / Kannada), centred on (x, y) and fitted to maxw;
    Latin letters without the Nirmala font. Returns its width."""
    if alpha <= 0.01:
        return 0.0
    lg = lang(tl)
    if HAS_INDIC:
        s = indic_surface(words[lg], int(size), tuple(color))
        w, h = s.get_width(), s.get_height()
        k = min(1.0, maxw / w) if maxw else 1.0
        cr.save()
        cr.translate(x, y)
        cr.scale(k, k)
        cr.set_source_surface(s, -w / 2, -h / 2)
        cr.paint_with_alpha(alpha)
        cr.restore()
        return w * k
    sz = fit_size(latin[lg], int(size * 0.8), maxw) if maxw else int(size * 0.8)
    draw_text(cr, latin[lg], x, y, sz, color, alpha, anchor="cm")
    return text_size(latin[lg], sz)[0]


def qcard(cr, t, tl, t_in, x, y, s, alpha=1.0, rod=True, shake=0.0):
    """The quote card (andhe_cast ak_qcard) with the line on it, dropping in on two rods at t_in (None = already
    there). Returns its centre."""
    q = back(clamp((t - t_in) / 0.35), 1.4) if t_in is not None else 1.0
    a = clamp(q) * alpha
    if a <= 0.01:
        return None
    yy = y + 70 * (1 - q)
    r = sway(t, 0.006, 0.4) + shake
    if rod:
        for sx in (-1, 1):
            pc.rod(cr, x + sx * 300 * s, yy + 175 * s, x + sx * 240, H + 60, alpha=0.5 * a)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(r)
    cr.scale(s, s)
    pc.paint_part(cr, "ak_qcard", a)
    native(cr, tl, QUOTE, QUOTE_LAT, 0, 6, 120, INK, a, maxw=740)
    cr.restore()
    return x, yy


# ------------------------------------------------------------------ puppets


def head_of(key, mood, default):
    return key + "_head" + ("" if mood == default else "_" + mood)


def duryo(cr, t, x, s, mood="calm", gada=False, up=False, front=(-0.32, -0.55), backa=(0.3, -0.25), **kw):
    """Duryodhana (andhe_cast): mood swaps his face; gada = his mace upright in his back hand; up = the robe held up
    to the knee."""
    swap = {"ak_duryo_head": head_of("ak_duryo", mood, "calm")}
    if up:
        swap.update({"ak_duryo_body": "ak_duryo_body_up", "ak_duryo_legF": "ak_duryo_legF_up",
                     "ak_duryo_legB": "ak_duryo_legB_up"})
    extra = None
    if gada:
        extra = {"ak_duryo_armB_lo": held("ak_gada", backa, 0.55, alpha=kw.get("alpha", 1.0), blur=kw.get("blur", 0.0))}
    return fig(cr, AK.DURYO, "ak_duryo", t, x, s, front=front, backa=backa, swap=swap, extra=extra, **kw)


def lady(cr, rig, key, head, t, x, s, feet, front=(-0.08, -0.35), backa=(0.15, -0.2), hd=0.0, hits=(), flip=False,
         alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.4, y=None):
    """A woman() puppet standing with her feet on `feet`, her head swapped for `head`."""
    ang = woman_angles(key, t, front, backa, hd, hits, ph)
    hy = feet - 470 * s if y is None else y
    return puppet(cr, rig, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, swap={key + "_head": head},
                  rods=rods)


def draupadi(cr, t, x, s, feet, mood="open", **kw):
    return lady(cr, AK.DRAUPADI, "ak_draupadi", head_of("ak_draupadi", mood, "open"), t, x, s, feet, **kw)


def bhima(cr, t, x, s, mood="calm", mace=True, backa=(0.3, -0.25), **kw):
    extra = {"bhima_armB_lo": held("mace", backa, 0.62, alpha=kw.get("alpha", 1.0))} if mace else None
    return fig(cr, C.BHIMA, "bhima", t, x, s, backa=backa, swap={"bhima_head": head_of("ak_bhima", mood, "calm")},
               extra=extra, **kw)


def arjuna(cr, t, x, s, mood="laugh", **kw):
    return fig(cr, J.ARJUNA, "jd_arjuna", t, x, s,
               swap={"jd_arjuna_head": "ak_arjuna_head_laugh" if mood == "laugh" else "jd_arjuna_head"}, **kw)


def twin(cr, rig, key, t, x, s, mood="laugh", **kw):
    return fig(cr, rig, key, t, x, s, swap={key + "_head": head_of(key, mood, "calm")}, **kw)


def servant(cr, t, x, s, b=False, mood="laugh", chamara=False, front=(-0.32, -0.55), **kw):
    extra = {"ak_servant_armF_lo": held("ak_chamara", front, 0.6, tilt=0.25)} if chamara else None
    hk = "ak_servantB" if b else "ak_servant"
    return fig(cr, AK.SERVANT, "ak_servant", t, x, s, front=front, swap={"ak_servant_head": head_of(hk, mood, "calm")},
               extra=extra, **kw)


def dhrita(cr, t, x, hip_y, s, front=(-0.9, -0.6), backa=(0.25, -0.9), head=0.0, hits=(), alpha=1.0, blur=0.0):
    """Dhritarashtra seated on his throne (hip at x, hip_y), his eyes closed."""
    r = bob_rot(t, 0.8, 0.006)
    prop(cr, "ak_dhrita_seat", x, hip_y, s, r, alpha, blur)
    ang = man_angles("ak_dhrita", t, front, backa, head, (0.0, 0.0), hits, 0.8)
    return puppet(cr, AK.DHRITA, x, hip_y, s, r, False, ang, alpha, blur, hide=("ak_dhrita_legF", "ak_dhrita_legB"))


def walk_fig(cr, t, fn, t0, t1, x0, x1, s, feet, step=0.42, t_in=None, **kw):
    """A man() puppet (fn = duryo / ...) walking in jerky rod-puppet steps on any ground line."""
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    kw.setdefault("hits", [(t1, 1.0)])
    y = feet - 434 * s + bob - (k - 1) * 300 * s
    return fn(cr, t, x, s * k, legs=walk_legs(ph), rot=rock, alpha=a, blur=b, y=y, feet=feet, **kw)


def laughing(t, t_l, ph=0.0):
    """A rod puppet laughing from t_l: the body shakes, the head tips back and bobs. Returns (rot, head)."""
    on = prog(t, t_l, 0.2)
    u = t - t_l
    return (on * 0.03 * math.sin(2 * math.pi * 4.6 * u + ph),
            on * (-0.14 + 0.07 * math.sin(2 * math.pi * 3.1 * u + ph)))


def green_glow(cr, x, y, r, a):
    """The green light of envy round a heart."""
    if a <= 0.01:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 0.40, 0.95, 0.30, 0.55 * a)
    g.add_color_stop_rgba(0.45, 0.20, 0.70, 0.18, 0.28 * a)
    g.add_color_stop_rgba(1, 0.10, 0.40, 0.10, 0.0)
    cr.save()
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def gflames(cr, t, x, y, s, a, n=3, spread=70.0):
    """Little green flames flickering round (x, y)."""
    if a <= 0.01:
        return
    for i in range(n):
        k = int(t * 9 + i * 1.7) % 3
        dx = (i - (n - 1) / 2) * spread
        f = 0.85 + 0.15 * math.sin(t * 13 + i * 2.1)
        prop(cr, f"ak_gflame{k}", x + dx, y + 10 * abs(dx) / max(1.0, spread), s * f * (1.0 - 0.12 * abs(i - 1)),
             rot=0.08 * math.sin(t * 7 + i), alpha=a)


# ------------------------------------------------------------------ the palace, the floor, the pond


def ell_path(cr, cx, cy, rx, ry):
    cr.save()
    cr.translate(cx, cy)
    cr.scale(rx, ry)
    cr.new_sub_path()
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()


def floor_shimmer(cr, t, a, x0=0.0, x1=W, y0=FLOOR_Y + 16, y1=H, base=FLOOR_Y):
    """Bands of light running slowly over the glass floor, so it looks like water."""
    if a <= 0.01:
        return
    cr.save()
    cr.rectangle(x0, y0, x1 - x0, y1 - y0)
    cr.clip()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    span = y1 - y0 + 80
    for k in range(9):
        y = y0 - 40 + (k * span / 9 + t * 22) % span
        d = clamp((y - base) / 600.0)
        cr.new_path()
        xx = x0
        while xx <= x1:
            yy = y + (3 + 9 * d) * math.sin(xx / (40 + 70 * d) + t * 1.7 + k * 1.3)
            (cr.move_to if xx == x0 else cr.line_to)(xx, yy)
            xx += 18
        cr.set_source_rgba(0.80, 0.94, 1.0, a * (0.10 + 0.12 * d))
        cr.set_line_width(2.5 + 4 * d)
        cr.stroke()
    cr.restore()


def floor(cr, t, pond_=None, illusion=1.0, rim=0.0, ripple_t=None, y=FLOOR_Y, alpha=1.0):
    """The glass floor; pond_ = (cx, cy, rx, ry) is where the pond is: while illusion = 1 it is drawn as more floor
    (only a faint blue tint), at 0 as the real water with its rim and ripples."""
    cr.save()
    if pond_:
        cr.rectangle(-300, -300, W + 600, H + 600)
        ell_path(cr, *pond_)
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.clip()
    prop(cr, "ak_floor", 540, y, 1.0, alpha=alpha)
    cr.restore()
    floor_shimmer(cr, t, 0.9 * alpha, y0=y + 16, base=y)
    if not pond_:
        return
    cx, cy, rx, ry = pond_
    cr.save()
    ell_path(cr, cx, cy, rx, ry)
    cr.clip()
    prop(cr, "ak_floor", 540, y, 1.0, alpha=alpha * illusion)
    prop(cr, "ak_water", cx + 12 * math.sin(t * 0.7), cy, rx / 400.0 * 1.05, alpha=alpha * (1 - 0.85 * illusion))
    w = 1 - illusion
    if w > 0.01:
        cr.set_operator(cairo.OPERATOR_ADD)
        for k in range(3):
            u = (t * 0.35 + k / 3) % 1.0
            ell_path(cr, cx + 30 * math.sin(k * 2.0), cy + 6, rx * (0.2 + 0.7 * u), ry * (0.2 + 0.7 * u))
            cr.set_source_rgba(0.85, 0.96, 1.0, 0.25 * w * (1 - u))
            cr.set_line_width(3)
            cr.stroke()
    cr.restore()
    if rim > 0.01:
        cr.save()
        ell_path(cr, cx, cy, rx, ry)
        cr.set_source_rgba(*INK, 0.55 * rim * alpha)
        cr.set_line_width(5)
        cr.stroke()
        ell_path(cr, cx, cy, rx - 6, ry - 3)
        cr.set_source_rgba(1.0, 0.86, 0.45, 0.5 * rim * alpha)
        cr.set_line_width(2.5)
        cr.stroke()
        cr.restore()


TWINKLE = ((80, 700), (80, 1000), (1000, 820), (1000, 1150), (300, 780), (540, 840), (760, 790), (440, 1050),
           (650, 1000), (860, 1100))


def palace(cr, t, alpha=1.0, blur=0.0, pond_=None, illusion=1.0, rim=0.0, twinkle=0.6, arch=True):
    """The magic crystal palace: a lattice wall, two crystal pillars, a cusped arch, the glass floor (and the pond)."""
    prop(cr, "ak_jali", 540, FLOOR_Y + 6, 0.92, alpha=0.55 * alpha, blur=3 + blur)
    glow(cr, 540, 1000, 700, 0.25 * alpha)
    for x in (80, 1000):
        prop(cr, "ak_pillar", x, FLOOR_Y + 8, 0.74, alpha=alpha, blur=blur)
    if arch:                                            # arch: True / False, or how strongly it shows
        prop(cr, "ak_arch", 540, 700, 0.86, rot=sway(t, 0.002, 0.3), alpha=alpha * float(arch), blur=blur)
    floor(cr, t, pond_, illusion, rim, alpha=alpha)
    for i, (x, y) in enumerate(TWINKLE):
        u = (t * 0.45 + i * 0.37) % 1.0
        sparkle(cr, x, y, 26 * math.sin(math.pi * u) ** 2, twinkle * alpha, (0.80, 0.94, 1.0))


def splash(cr, t, t_s, x, y, s=1.0):
    """Duryodhana going in: a crown of water, drops flying out and falling back, rings spreading."""
    u = t - t_s
    if u < 0 or u > 2.4:
        return
    a = 1 - prog(t, t_s + 0.45, 0.6)
    if a > 0.01:
        prop(cr, "ak_splash", x, y + 6, s * (0.3 + 0.8 * ease(u / 0.32)), alpha=a)
    for i in range(14):
        ang = math.pi * (0.12 + 0.76 * ((i * 0.618) % 1.0))
        v = (420 + 260 * ((i * 0.37) % 1.0)) * s
        dx, dy = -math.cos(ang) * v * u, -math.sin(ang) * v * u + 1300 * s * u * u
        if dy > 40 * s:
            continue
        prop(cr, "rv_drop", x + dx, y + dy, 1.3 * s, rot=-math.cos(ang) * 0.8, alpha=clamp(1.6 - u))
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    for k in range(3):
        p = (u - 0.2 * k) / 1.4
        if 0 < p < 1:
            ell_path(cr, x, y + 8, (90 + 260 * ease(p)) * s, (24 + 70 * ease(p)) * s)
            cr.set_source_rgba(0.85, 0.96, 1.0, 0.55 * (1 - p))
            cr.set_line_width(4)
            cr.stroke()
    cr.restore()


def drips(cr, t, x, y, w, a=1.0, n=4):
    """Water dripping off someone (falling drops along a width w)."""
    for i in range(n):
        u = (t * 0.9 + i / n) % 1.0
        prop(cr, "rv_drop", x - w / 2 + w * ((i * 0.618) % 1.0), y + 120 * u * u, 0.9, alpha=a * (1 - u))


# ------------------------------------------------------------------ m1  hook: Draupadi never said it


CARD1 = (540, 1000, 0.98)
DR1 = (200, 0.5, 1800)               # Draupadi, small, lower left: x, scale, feet
DU1 = (880, 0.5, 1800)               # Duryodhana, small, lower right


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "m1")
    tD, tY, tK, tL, tN = c["D"], c["Y"], c["K"], c["L"], c["N"]
    x, y, s = CARD1
    glow(cr, x, y, 760, 0.4)
    shake = 0.05 * math.exp(-6 * max(0.0, t - tN)) * math.sin(48 * (t - tN)) if t > tN else 0.0
    qcard(cr, t, tl, None, x, y, s, shake=shake)
    prop(cr, "ground", W / 2, 1806, 0.82)
    dp = None
    if t > tD - 0.3:
        b, k, a = depth(t, tD - 0.3, 0.4)
        dx, ds, df = DR1
        dp = draupadi(cr, t, dx, ds * k, df, mood="open", alpha=a, blur=b, hd=-0.08, ph=0.4)
    if t > tY - 0.3:
        b, k, a = depth(t, tY - 0.3, 0.4)
        ux, us, uf = DU1
        duryo(cr, t, ux, us * k, feet=uf, flip=True, alpha=a, blur=b, head=-0.1, ph=0.9, y=uf - 434 * us * k)
    if dp and t > tK - 0.1:                             # "never": from her lips to the line, crossed out
        hx, hy = to_user(cr, dp["head"])
        p0, p1 = (hx + 60, hy + 10), (x - 110, y + 190)
        pts = [(p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u - 60 * math.sin(math.pi * u))
               for u in (i / 30 for i in range(31))]
        fade = 1 - prog(t, tN - 0.1, 0.3)
        dotted(cr, pts, prog(t, tK - 0.1, 0.35), 24, 6, RED, fade)
        mx, my = pts[15]
        big_x(cr, mx, my, 120, 110, prog(t, tK + 0.2, 0.3), alpha=fade)
    if t > tL - 0.05:
        red_ring(cr, x, y + 6, 430, 112, prog(t, tL - 0.05, 0.45), 10, 1 - 0.5 * prog(t, tN, 0.3))

    def ui(cr):
        head2(cr, t, "DRAUPADI NEVER SAID", -1.0, "THIS LINE", 0.3, big_size=240, ghost=-1.0, under=tN + 0.25)
        tag(cr, t, tD, "DRAUPADI", 360, 1400, 32, t_out=tN - 0.15)
        tag(cr, t, tY, "DURYODHANA", 720, 1330, 32, t_out=tN - 0.15)
        stamp2(cr, t, tN, ["NOT IN THE", "MAHABHARATA"], 560, y + 270, 92, rot=-0.07)
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.2) + flash_at(t, tK + 0.2, 0.15) + flash_at(t, tN, 0.45, 5.0))


# ------------------------------------------------------------------ m2  what we all saw on TV


TV2 = (540, 1770, 1.45)               # the TV: x, foot, scale


def s_tv(cr, t, tl, t0, t1):
    c = cues(tl, "m2")
    tT, tF, tH, tQ = c["T"], c["F"], c["H"], c["Q"]
    x, foot, s = TV2
    glow(cr, x, 1250, 760, 0.35)
    q = back(clamp((t - t0 + 0.05) / 0.35), 1.4)
    ty = foot + 90 * (1 - q)
    prop(cr, "ak_tv", x, ty, s, alpha=clamp(q))
    x0, y0, w, h = AK.TV_SCREEN
    sx, sy, sw, sh = x + (x0 + w / 2) * s, ty + (y0 + h / 2) * s, w * s, h * s
    on = prog(t, tT - 0.15, 0.35)
    if on > 0:
        vy, vx = max(0.03, clamp(on * 2 - 1)), clamp(on * 2)
        cr.save()                                       # the screen's clip
        cr.save()
        cr.translate(sx, sy)
        cr.scale(vx, vy)
        AK._rrect(cr, -sw / 2, -sh / 2, sw / 2, sh / 2, 40)
        cr.restore()
        cr.clip()
        cr.set_source_rgba(0.95, 0.93, 0.86, 1.0)
        cr.paint()
        top, left = sy - sh / 2, sx - sw / 2
        prop(cr, "ak_floor", sx, top + sh * 0.56, 0.42)       # the popular scene, small, on the screen
        bx, by = left + sw * 0.73, top + sh * 0.58
        prop(cr, "ak_balc_back", bx, by, 0.3)
        laugh = t > tH - 0.1
        rot, hd = laughing(t, tH - 0.1, 0.4) if laugh else (0.0, 0.0)
        dp = draupadi(cr, t, bx + 8, 0.25, by + 4, mood="laugh" if laugh else "open", flip=True, rods=False, rot=rot,
                      hd=hd + 0.12, front=(-0.9, -1.0) if t > tQ - 0.2 else (-0.1, -0.4))
        prop(cr, "ak_balc_rail", bx, by, 0.3)
        pond_ = (left + sw * 0.3, top + sh * 0.86, sw * 0.24, sh * 0.06)
        cr.save()
        ell_path(cr, *pond_)
        cr.clip()
        prop(cr, "ak_water", pond_[0], pond_[1], 0.3)
        cr.restore()
        px, py = pond_[0], pond_[1]
        ds = 0.27
        if t < tF:
            walk_fig(cr, t, duryo, t0 + 0.2, tF - 0.05, left - 60, px, ds, py, rods=False, ph=0.9)
        else:
            f = ease((t - tF) / 0.25)
            cr.save()
            cr.rectangle(-400, -400, W + 800, py + 400)
            cr.clip()
            duryo(cr, t, px, ds, mood="shock", feet=py, y=py - 434 * ds + f * (434 * ds + 10), rods=False, ph=0.9,
                  front=(-2.6, -0.3), backa=(-2.4, -0.2), hits=[(tF, 1.0)])
            cr.restore()
            splash(cr, t, tF, px, py, 0.32)
        if laugh:
            hx, hy = to_user(cr, dp["head"])
            ha2(cr, t, tH, hx, hy - 20, -1, 26)
        cr.set_source_rgba(1.0, 0.86, 0.62, 0.18)              # an old film's warm cast
        cr.paint()
        for k in range(int(sh // 9)):                          # scan lines, rolling
            cr.rectangle(left, top + ((k * 9 + t * 40) % sh), sw, 2.5)
        cr.set_source_rgba(0.1, 0.15, 0.1, 0.08)
        cr.fill()
        cr.restore()
        glow(cr, sx, sy, 380, 0.25 * on)

    def ui(cr):
        head2(cr, t, "WE ALL SAW IT", t0 + 0.05, "ON TV", tT, big_size=250)
        cq = back(clamp((t - tQ) / 0.3), 1.6)
        cx, cy = 400, 760
        if cq > 0.01:
            prop(cr, "lr_scloud", cx, cy, 0.66 * (0.6 + 0.4 * cq), rot=sway(t, 0.008, 0.5), alpha=clamp(cq), flip=True)
            native(cr, tl, QUOTE, QUOTE_LAT, cx, cy - 8, 66, INK, clamp(cq * 2 - 0.6), maxw=360)
        q_stamp(cr, t, tQ + 0.6, 900, 760, 60, rot=0.12)
    return dict(ui=ui, flash=flash_at(t, tT, 0.2) + flash_at(t, tF, 0.2) + flash_at(t, tQ + 0.6, 0.15))


# ------------------------------------------------------------------ m3  not in Vyasa's text


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "m3")
    tV, tN = c["V"], c["N"]
    leaves = [(None, [("VYASA'S MAHABHARATA", 84, HEAD_FONT)], 0)]
    pts = book(cr, t, 540, 840, 0.9, leaves, t_in=t0 + 0.02, t_open=tV, blank=3)
    if pts and t > tV + 0.4:                            # the lens sweeps the leaves: nothing
        u = clamp((t - tV - 0.4) / max(0.6, tN + 0.5 - tV - 0.4))
        f = 1 + u * (len(pts) - 2)
        i0 = min(int(f), len(pts) - 2)
        fy = pts[i0][1] + (pts[i0 + 1][1] - pts[i0][1]) * (f - i0)
        lx = 540 + 250 * math.sin(u * math.pi * 3.0 - math.pi / 2)
        prop(cr, "ak_lens", lx, fy - 10, 0.85, rot=0.15 * math.sin(t * 2.2))

    def ui(cr):
        head2(cr, t, "IN VYASA'S MAHABHARATA:", t0 + 0.05, "NOWHERE!", tN, big_size=250)
        stamp2(cr, t, tN + 0.3, ["NOT FOUND"], 560, 1470, 84, rot=-0.07)
    return dict(ui=ui, flash=flash_at(t, tV, 0.2) + flash_at(t, tN + 0.3, 0.25))


# ------------------------------------------------------------------ m4  the magic palace: floor = water, water = floor


PANELS = ((290, 1150), (790, 1150))
PANEL_W, PANEL_H = 460, 840


def mini_floor(cr, t, x, top, w, illusion=None, peek=0.0):
    """Inside a panel: a patch of the glass floor (with water light running over it), or (illusion given) the pond
    hidden under a skin of tiles that lifts by `peek`."""
    fs = 0.86                                           # the floor patch's scale (its back edge at top + 150)
    cr.save()
    cr.rectangle(x - w / 2 + 14, top + 150, w - 28, 470)
    cr.clip()
    if illusion is None:
        prop(cr, "ak_floor", x, top + 150, fs)
        floor_shimmer(cr, t, 2.2, x - w / 2, x + w / 2, top + 150, top + 620, base=top + 150)
    else:
        pond_ = (x, top + 410, 170, 116)
        cr.save()
        cr.rectangle(-300, -300, W + 600, H + 600)
        ell_path(cr, *pond_)
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.clip()
        prop(cr, "ak_floor", x, top + 150, fs)
        cr.restore()
        lift = ease(peek)
        cr.save()
        ell_path(cr, *pond_)
        cr.clip()
        prop(cr, "ak_water", x + 10 * math.sin(t * 0.8), top + 410, 0.8, alpha=0.15 + 0.85 * lift)
        if lift < 0.99:                                 # the tile skin over the water, lifting off
            cr.translate(0, -260 * lift)
            prop(cr, "ak_floor", x, top + 150, fs, alpha=illusion * (1 - lift))
        cr.restore()
        if peek > 0.01:
            dotted(cr, [(x + 170 * math.cos(a), top + 410 + 116 * math.sin(a)) for a in
                        (2 * math.pi * i / 60 for i in range(61))], peek, 26, 6, RED, 0.9)
    cr.restore()


PANDAVAS4 = ((100, "yudh"), (225, "bhima"), (350, "arjuna"), (470, "nakula"), (588, "sahadeva"))
CF = 1760                            # where the cousins stand


def pandava(cr, t, kind, x, s, mood="calm", **kw):
    """One of the five brothers (calm), facing right."""
    if kind == "yudh":
        return fig(cr, A.YUDH, "ar_yudh", t, x, s, swap={"ar_yudh_head": "ar_yudh_head" + ("_smile" if mood == "smile"
                                                                                           else "")}, **kw)
    if kind == "bhima":
        return bhima(cr, t, x, s * 1.02, mood="laugh" if mood == "laugh" else "calm", **kw)
    if kind == "arjuna":
        return arjuna(cr, t, x, s, mood="laugh" if mood == "laugh" else "calm", **kw)
    rig, key = (AK.NAKULA, "ak_nakula") if kind == "nakula" else (AK.SAHADEVA, "ak_sahadeva")
    return twin(cr, rig, key, t, x, s, mood="laugh" if mood == "laugh" else "calm", **kw)


def s_cousins(cr, t, tl, t0, t1):
    c = cues(tl, "m4")
    tB, tC, tP, tJ = c["B"], c["C"], c["P"], c["J"]
    pal = prog(t, tP - 0.2, 0.5)
    fam = 1 - pal
    if pal > 0.01:                                      # the magic palace
        magic = prog(t, tJ, 0.5)
        palace(cr, t, alpha=pal, twinkle=0.4 + 0.6 * magic, arch=pal)
        if t > tJ:
            lights(cr, t, 540, 1000, 480, 18, 0.8 * magic, col=(0.80, 0.94, 1.0))
    else:
        glow(cr, 540, 1350, 700, 0.35)
    if fam > 0.01 and t > tB - 0.3:                     # the cousins: the five brothers, and Duryodhana
        prop(cr, "ground", W / 2, CF + 6, 0.82, alpha=fam)
        for i, (x, kind) in enumerate(PANDAVAS4):
            b, k, a = depth(t, tB - 0.3 + 0.08 * i, 0.4)
            pandava(cr, t, kind, x, 0.5 * k, feet=CF, alpha=a * fam, blur=b, ph=0.6 * i, y=CF - 434 * 0.5 * k,
                    hits=[(tC, 0.3)])
        b, k, a = depth(t, tB + 0.35, 0.4)
        duryo(cr, t, 880, 0.6 * k, gada=True, feet=CF, flip=True, alpha=a * fam, blur=b, ph=0.9,
              y=CF - 434 * 0.6 * k, hits=[(tC, 0.3)])
        if t > tC - 0.1:                                # one family: an arc from the brothers to him
            pts = [(345 + 535 * u, 1010 - 60 * u - 170 * math.sin(math.pi * u)) for u in (i / 40 for i in range(41))]
            dotted(cr, pts, prog(t, tC - 0.1, 0.5), 26, 7, RED, fam)

    def ui(cr):
        if t < tB:
            head2(cr, t, "SO WHAT", t0 + 0.05, "REALLY HAPPENED?", t0 + 0.35, big_size=210)
            big_q(cr, t, t0 + 0.5, 540, 1150, 320, alpha=1 - prog(t, tB - 0.3, 0.25))
        elif t < tP:
            head2(cr, t, "PANDAVAS & DURYODHANA:", tB - 0.1, "COUSINS", tC, big_size=270)
            tag(cr, t, tB + 0.1, "THE 5 PANDAVAS", 345, 1060, 32, alpha=fam)
            tag(cr, t, tB + 0.45, "DURYODHANA", 870, 965, 32, alpha=fam)
            plate(cr, t, tC + 0.35, "ONE BIG FAMILY", 612, 740, 36, alpha=fam)
        else:
            head2(cr, t, "THE PANDAVAS HAD A", tP - 0.1, "MAGIC PALACE", tJ, big_size=220, under=tJ + 0.4)
    return dict(ui=ui, flash=flash_at(t, tC, 0.15) + flash_at(t, tJ, 0.25))


# ------------------------------------------------------------------ m5  floor = water? water = floor?


def s_panels(cr, t, tl, t0, t1):
    c = cues(tl, "m5")
    tF, tW, tL = c["F"], c["W"], c["L"]
    palace(cr, t, alpha=0.75, blur=6, twinkle=0.8, arch=False)
    lights(cr, t, 540, 1000, 480, 14, 0.4, col=(0.80, 0.94, 1.0))

    def ui(cr):
        if t < tW:
            head2(cr, t, "FLOOR LOOKED LIKE", t0 + 0.05, "WATER", tF, big_size=260)
        else:
            head2(cr, t, "WATER LOOKED LIKE", tW - 0.1, "FLOOR", tL, big_size=260)
        for k, ((x, y), t_in) in enumerate(zip(PANELS, (t0 + 0.05, tW - 0.25))):
            yy, a = panel(cr, t, t_in, x, y, PANEL_W, PANEL_H)
            if a <= 0:
                continue
            top = yy - PANEL_H / 2
            if k == 0:
                mini_floor(cr, t, x, top, PANEL_W)
                draw_text(cr, "FLOOR", x, top + 82, 88, INK, a, anchor="cm")
                q = prog(t, tF, 0.3) * a
                if q > 0:
                    draw_text(cr, "= WATER?", x, top + 720 + 10 * (1 - q), 88, RED, q, anchor="cm")
            else:
                mini_floor(cr, t, x, top, PANEL_W, illusion=1.0, peek=prog(t, tL + 0.25, 0.5))
                draw_text(cr, "WATER", x, top + 82, 88, INK, a, anchor="cm")
                q = prog(t, tL, 0.3) * a
                if q > 0:
                    draw_text(cr, "= FLOOR?", x, top + 720 + 10 * (1 - q), 88, RED, q, anchor="cm")
    return dict(ui=ui, flash=flash_at(t, tF, 0.15) + flash_at(t, tL, 0.15))


# ------------------------------------------------------------------ m6  walking... splash!


POND6 = (790, STAGE, 250, 88)


def s_splash(cr, t, tl, t0, t1):
    c = cues(tl, "m6")
    tD, tS, tA, tB = c["D"], c["S"], c["A"], c["B"]
    illusion = 1 - prog(t, tB + 0.05, 0.5)
    palace(cr, t, pond_=POND6, illusion=illusion, rim=prog(t, tB + 0.3, 0.5))
    s = 0.7
    t_stop = max(t0 + 0.6, tA - 0.1)
    if t < t_stop:                                      # walking round the palace, looking at it all
        turn = 0.1 * math.sin(2 * math.pi * 0.5 * (t - tD)) * prog(t, tD, 0.3)
        walk_fig(cr, t, duryo, t0 - 0.25, t_stop, -60, 380, s, STAGE, head=turn, ph=0.9)
    elif t < tB:                                        # sure it is floor, he strides on proudly
        walk_fig(cr, t, duryo, t_stop, tB - 0.02, 380, 760, s, STAGE, step=0.4, head=-0.08, front=(-0.5, -0.4),
                 mood="proud", ph=0.9)
    yw = STAGE + 4
    if t >= tB:                                         # in he goes: waist-deep, arms up, then ashamed
        f = ease((t - tB) / 0.26)
        bob = 7 * math.sin((t - tB) * 5.5) * math.exp(-1.2 * (t - tB))
        hip = STAGE - 434 * s + f * (434 * s + 26) + bob
        arms = keyed(t, [(tB, 0.0), (tB + 0.05, 1.0), (tB + 1.4, 0.0)], 0.25, 1.6)
        cr.save()
        cr.rectangle(-400, -400, W + 800, yw + 400)
        cr.clip()
        duryo(cr, t, 760, s, mood="shock" if t < tB + 1.3 else "shame", feet=STAGE, y=hip,
              rot=0.1 * math.exp(-2 * (t - tB)) * math.sin((t - tB) * 9),
              front=mix((-0.5, -0.9), (-2.7, -0.3), arms), backa=mix((0.3, -0.6), (-2.5, -0.2), arms),
              head=0.2 * (1 - arms), hits=[(tB + 0.05, 1.0)], ph=0.9, rods=False)
        cr.restore()
        cr.save()
        cr.set_operator(cairo.OPERATOR_ADD)
        ell_path(cr, 760, yw + 4, 120, 22)
        cr.set_source_rgba(0.85, 0.96, 1.0, 0.45)
        cr.set_line_width(4)
        cr.stroke()
        cr.restore()
        splash(cr, t, tB, 760, yw, 1.0)
        if t > tB + 1.0:
            drips(cr, t, 760, yw - 200, 160, prog(t, tB + 1.0, 0.4))

    def ui(cr):
        if t < tS:
            head2(cr, t, "DURYODHANA WAS", t0 + 0.05, "WALKING AROUND", tD, big_size=210)
        elif t < tB:
            head2(cr, t, "HE THOUGHT WATER WAS", tS - 0.1, "FLOOR", tS + 0.1, big_size=225)
        else:
            head2(cr, t, "AND...", tB - 0.15, "SPLASH!", tB, big_size=225)
            plate(cr, t, tB + 0.8, "IT WAS WATER!", 760, 1150, 34)
    return dict(ui=ui, flash=flash_at(t, tS + 0.1, 0.12) + flash_at(t, tB, 0.45, 5.0))


# ------------------------------------------------------------------ m7  who laughed


POND7 = (540, 1772, 300, 92)
LAUGHERS = (   # (cue, x, flip, kind, tag, tag x, tag y)
    ("B", 120, False, "bhima", "BHIMA", 130, 860),
    ("S", 262, False, "servant", None, 0, 0),
    ("S", 372, False, "servantB", "SERVANTS", 320, 790),
    ("A", 712, True, "arjuna", "ARJUNA", 712, 860),
    ("N", 838, True, "nakula", "NAKULA", 838, 790),
    ("D", 962, True, "sahadeva", "SAHADEVA", 922, 860),
)
LF = 1470                            # where the laughers stand
LS = 0.46
BELLY = (-0.15, -1.35)               # a hand on the belly (laughing)
DURY7 = (540, 1700)                  # what they point at


def laugher(cr, t, kind, x, flip, t_in, ph):
    """One of the laughers: comes onto the cloth at t_in already laughing, one hand on his belly, the other pointing
    down at Duryodhana in the pond (or a chamara held up)."""
    b, k, a = depth(t, t_in - 0.25, 0.4)
    rot, hd = laughing(t, t_in - 0.1, ph)
    s = LS * k
    kw = dict(feet=LF, flip=flip, rot=rot, head=hd, alpha=a, blur=b, ph=ph, y=LF - 434 * s, rods=False)
    point = point_to(x, LF - 434 * s, s, DURY7, flip=flip)
    if kind == "bhima":
        return bhima(cr, t, x, s * 1.02, mood="laugh", front=point, backa=BELLY, mace=False, **kw)
    if kind in ("servant", "servantB"):
        return servant(cr, t, x, s * 0.98, b=kind == "servantB", chamara=kind == "servant",
                       front=(-0.5, -0.7) if kind == "servant" else point, backa=BELLY, **kw)
    if kind == "arjuna":
        return arjuna(cr, t, x, s, front=point, backa=BELLY, **kw)
    rig, key = (AK.NAKULA, "ak_nakula") if kind == "nakula" else (AK.SAHADEVA, "ak_sahadeva")
    if kind == "nakula":
        return twin(cr, rig, key, t, x, s, front=BELLY, backa=(-0.2, -1.2), **kw)
    return twin(cr, rig, key, t, x, s, front=point, backa=BELLY, **kw)


def ha2(cr, t, t_in, x, y, side=1, size=34, alpha=1.0):
    """Small HA! letters puffing up beside a laughing head, again and again while he laughs."""
    if t < t_in:
        return
    for i in range(2):
        u = ((t - t_in) / 1.3 + i * 0.5) % 1.0
        if (t - t_in) < i * 0.65:
            continue
        q = back(clamp(u / 0.18), 2.0)
        a = clamp(q) * alpha * (1 - clamp((u - 0.7) / 0.3))
        if a <= 0.01:
            continue
        cr.save()
        cr.translate(x + side * (34 + 26 * u), y - 70 * u)
        cr.rotate(side * 0.18 + 0.1 * math.sin(i * 2 + t))
        cr.scale(q, q)
        draw_text(cr, "HA!", 0, 0, size, (0.55, 0.12, 0.05), a, anchor="cm")
        cr.restore()


def s_laugh(cr, t, tl, t0, t1):
    c = cues(tl, "m7")
    palace(cr, t, pond_=POND7, illusion=0.0, rim=1.0, twinkle=0.4, arch=False)
    heads = []
    for i, (ck, x, flip, kind, label, tx, ty) in enumerate(LAUGHERS):
        t_in = c[ck] + (0.12 if kind == "servantB" else 0.0)
        if t > t_in - 0.25:
            p = laugher(cr, t, kind, x, flip, t_in, ph=0.7 * i)
            heads.append((t_in, p["head"], flip))
    yw = POND7[1] - 4
    cr.save()
    cr.rectangle(-400, -400, W + 800, yw + 400)
    cr.clip()
    duryo(cr, t, 540, 0.62, mood="shame", feet=STAGE, y=yw - 26 + 5 * math.sin(t * 2.2), front=(-0.35, -1.9),
          backa=(0.25, -0.7), head=0.22, ph=0.9, rods=False, flip=True)
    cr.restore()
    cr.save()
    cr.set_operator(cairo.OPERATOR_ADD)
    ell_path(cr, 540, yw + 4, 110, 20)
    cr.set_source_rgba(0.85, 0.96, 1.0, 0.4)
    cr.set_line_width(4)
    cr.stroke()
    cr.restore()
    drips(cr, t, 540, yw - 190, 140, 0.8, 3)

    def ui(cr):
        head2(cr, t, "SEEING THIS,", t0 + 0.05, "THEY LAUGHED", c["B"], big_size=230)
        for (ck, x, flip, kind, label, tx, ty) in LAUGHERS:
            t_in = c[ck] + (0.12 if kind == "servantB" else 0.0)
            if label:
                tag(cr, t, t_in + 0.1, label, tx, ty, 30)
        for t_in, hp, flip in heads:
            hx, hy = to_user(cr, hp)
            ha2(cr, t, t_in + 0.05, hx, hy - 30, -1 if flip else 1)
    return dict(ui=ui, flash=sum(flash_at(t, c[k], 0.12) for k in ("B", "S", "A", "N", "D")))


# ------------------------------------------------------------------ m8  Draupadi: not even named


LIST_ROWS = ("BHIMA", "SERVANTS", "ARJUNA", "NAKULA", "SAHADEVA")
LIST = (540, 1170, 780, 980)          # the list panel: x, y, w, h


def s_list(cr, t, tl, t0, t1):
    c = cues(tl, "m8")
    tD, tN, tX = c["D"], c["N"], c["X"]
    glow(cr, 540, 1150, 720, 0.4)

    def ui(cr):
        if t < tN:
            head2(cr, t, "AND", t0 + 0.05, "DRAUPADI?", tD, big_size=260)
        else:
            head2(cr, t, "DRAUPADI:", tN - 0.15, "NOT EVEN NAMED", tN, big_size=220, under=tX + 0.2)
        x, y, w, h = LIST
        yy, a = panel(cr, t, t0 - 0.15, x, y, w, h)
        if a <= 0:
            return
        top = yy - h / 2
        draw_text(cr, "WHO LAUGHED", x, top + 76, 80, RED, a, anchor="cm")
        draw_text(cr, "IN VYASA'S MAHABHARATA", x, top + 142, 32, INK, a, MONO_FONT, "cm", tracking=4)
        for i, name in enumerate(LIST_ROWS):
            ry = top + 240 + 105 * i
            q = prog(t, t0 + 0.1 + 0.12 * i, 0.25) * a
            if q > 0:
                draw_text(cr, name, x - 300, ry + 8 * (1 - q), 70, INK, q, anchor="lm")
                tick(cr, x + 230, ry, 70, prog(t, t0 + 0.3 + 0.12 * i, 0.3), alpha=q)
        ry = top + 240 + 105 * 5
        q = prog(t, tD, 0.3) * a
        if q > 0:                                       # the empty sixth row
            bw, bh = 620, 96
            pts = [(x - bw / 2, ry - bh / 2), (x + bw / 2, ry - bh / 2), (x + bw / 2, ry + bh / 2),
                   (x - bw / 2, ry + bh / 2), (x - bw / 2, ry - bh / 2)]
            dotted(cr, pts, q, 22, 4.5, FADE, 0.9)
            draw_text(cr, "DRAUPADI", x - 300, ry, 70, FADE, 0.55 * q, anchor="lm")
            if t > tN:
                p = ease((t - tN) / 0.3)
                cr.save()
                cr.set_source_rgba(*RED, 0.92 * a)
                cr.set_line_width(14)
                cr.set_line_cap(cairo.LINE_CAP_ROUND)
                cr.move_to(x - 316, ry + 4)
                cr.line_to(x - 316 + 330 * p, ry - 6 * p)
                cr.stroke()
                cr.restore()
                draw_text(cr, "?", x + 230, ry, 90, RED, prog(t, tN + 0.2, 0.25) * a, anchor="cm")
        stamp2(cr, t, tX, ["NOT", "WRITTEN"], x + 20, ry + 128, 64, rot=-0.06)
    return dict(ui=ui, flash=flash_at(t, tD, 0.15) + flash_at(t, tX, 0.3))


# ------------------------------------------------------------------ m9  his own claim; but nobody said the line


THRONE8 = (240, 1770, 0.72)          # the throne: x, floor, scale (cushion top at -246)
DU8 = (800, 1770, 0.68)
BUBBLE8 = (470, 820, 0.74)
CARD8 = (540, 790, 0.8)


def s_claim(cr, t, tl, t0, t1):
    c = cues(tl, "m9")
    tF, tC, tD, tH, tQ, tK = c["F"], c["C"], c["D"], c["H"], c["Q"], c["K"]
    glow(cr, 540, 1300, 720, 0.35)
    tx, tf, ts = THRONE8
    prop(cr, "md_throne", tx, tf, ts)
    prop(cr, "ground", W / 2, tf + 6, 0.82)
    listen = keyed(t, [(t0, 0.0), (tC, 1.0)], 0.35, 1.3)
    dhrita(cr, t, tx - 22, tf - 246 * ts, 0.66, front=mix((-0.6, -0.9), (-1.2, -0.5), listen), head=-0.08 * listen,
           hits=[(tF, 0.4)])
    x, f, s = DU8
    talk = keyed(t, [(t0, 0.0), (tC - 0.1, 1.0), (tD - 0.1, 2.0), (tQ, 3.0)], 0.3, 1.4)
    if talk < 1.5:
        front = mix((-0.4, -0.5), (-1.5, -0.6), min(1.0, talk))
    elif talk < 2.5:
        front = mix((-1.5, -0.6), (-2.5, -0.5), talk - 1.0)
    else:
        front = mix((-2.5, -0.5), (-0.4, -0.5), talk - 2.0)
    duryo(cr, t, x, s, mood="scold" if tC < t < tQ else "angry", gada=True, feet=f, flip=True, front=front,
          head=0.04 * math.sin(t * 7) * prog(t, tC, 0.2) * (1 - prog(t, tQ, 0.2)),
          hits=[(tC, 0.6), (tD, 0.6), (tH, 0.5)], ph=0.9)

    def ui(cr):
        if t < tD:
            head2(cr, t, "LATER, TO HIS FATHER,", t0 + 0.05, "HE COMPLAINED", tC, big_size=220)
        elif t < tQ:
            head2(cr, t, "HE SAID: DRAUPADI", tD - 0.1, "LAUGHED TOO", tH, big_size=230)
        else:
            head2(cr, t, "BUT THIS LINE?", tQ - 0.1, "NOBODY SAID IT", tK, big_size=220, under=tK + 0.3)
        tag(cr, t, tF, "HIS FATHER", 250, 1100, 32, t_out=tQ - 0.2)
        cq = back(clamp((t - tC - 0.1) / 0.3), 1.6) * (1 - prog(t, tD - 0.3, 0.25))
        if cq > 0.01:
            cx, cy = 560, 860
            prop(cr, "lr_scloud", cx, cy, 0.62 * (0.6 + 0.4 * cq), rot=sway(t, 0.008, 0.5), alpha=clamp(cq),
                 flip=True)
            draw_text(cr, "THEY ALL", cx, cy - 46, 54, INK, clamp(cq), anchor="cm")
            draw_text(cr, "LAUGHED AT ME!", cx, cy + 22, 64, RED, clamp(cq), anchor="cm")
        bx, by, bs = BUBBLE8
        q = back(clamp((t - tD + 0.2) / 0.35), 1.5) * (1 - prog(t, tQ - 0.25, 0.25))
        if q > 0.01:
            prop(cr, "ar_think", bx, by, bs * (0.5 + 0.5 * q), rot=sway(t, 0.008, 0.4), alpha=clamp(q))
            a = clamp(q * 2 - 1)
            if a > 0.01:
                cr.save()
                ell_path(cr, bx, by, 232, 158)
                cr.clip()
                gf = by + 150
                laugh_t = tH - 0.1
                for lx, rig, key, head, flip, ph in ((360, C.QUEEN1, "queen1", "ak_lady1_head_laugh", False, 0.2),
                                                     (600, C.QUEEN2, "queen2", "ak_lady2_head_laugh", True, 1.1)):
                    rot, hd = laughing(t, tD + 0.3, ph)
                    lady(cr, rig, key, head, t, lx, 0.26, gf, flip=flip, rot=rot, hd=hd, alpha=a, rods=False,
                         front=(-0.6, -1.4), backa=(-0.3, -1.5))
                rot, hd = laughing(t, laugh_t, 0.6)
                draupadi(cr, t, bx + 10, 0.28, gf, mood="laugh" if t > laugh_t else "smile", rot=rot, hd=hd, alpha=a,
                         rods=False, front=(-0.4, -1.9), backa=(-0.2, -1.4))
                cr.restore()
            tag(cr, t, tH + 0.15, "HIS OWN CLAIM", bx, 588, 34, t_out=tQ - 0.3)
        if t > tQ - 0.3:
            cx, cy, cs = CARD8
            qcard(cr, t, tl, tQ - 0.3, cx, cy, cs, rod=False)
            stamp2(cr, t, tK, ["NOBODY", "SAID IT"], cx - 50, cy + 200, 76, rot=-0.07)
    return dict(ui=ui, eve=0.25, flash=flash_at(t, tD, 0.15) + flash_at(t, tH + 0.15, 0.2) + flash_at(t, tK, 0.3))


# ------------------------------------------------------------------ m10  what really hurt him: envy


DU9 = (230, 1790, 0.74)
HEART = (-0.3, -2.45)                # a hand at the heart


def s_envy(cr, t, tl, t0, t1):
    c = cues(tl, "m10")
    tR, tW, tG, tE = c["R"], c["W"], c["G"], c["E"]
    tH, tB = tE - 0.15, tE + 0.25
    glow(cr, 540, 1300, 720, 0.3)
    prop(cr, "ground", W / 2, 1796, 0.82)
    gl = prog(t, tG - 0.1, 0.5)
    if t > tG - 0.3:                                    # Yudhishthira in glory: a golden light, rays turning
        b, k, a = depth(t, tG - 0.3, 0.45)
        glow(cr, 800, 1150, 560, 0.7 * gl)
        warm(cr, 800, 1080, 420, 0.6 * gl)
        aura(cr, t, 795, 1010, 110, 470, 0.8 * gl, n=22, spin=0.08)
        fig(cr, A.YUDH, "ar_yudh", t, 800, 0.56 * k, flip=True, swap={"ar_yudh_head": "ar_yudh_head_smile"},
            feet=1660, front=(-1.4, -0.5), alpha=a, blur=b, ph=0.7, y=1660 - 434 * 0.56 * k)
    wq = back(clamp((t - tW) / 0.4), 1.4)
    if wq > 0.01:                                       # the wealth, heaped in front of him
        for (sp, x, y, s, dl) in (("ak_heap", 610, 1812, 0.78, 0.0), ("ak_chest", 905, 1806, 0.56, 0.15),
                                  ("sb_gold", 790, 1846, 0.46, 0.3)):
            q = back(clamp((t - tW - dl) / 0.4), 1.4)
            if q > 0.01:
                prop(cr, sp, x, y + 60 * (1 - q), s, alpha=clamp(q))
        for i in range(9):
            u = (t * 0.5 + i / 9) % 1.0
            sparkle(cr, 440 + 66 * i, 1740 - 200 * u, 26 * math.sin(math.pi * u), clamp(wq))
    x, f, s = DU9
    pain = keyed(t, [(t0, 0.0), (tR - 0.1, 1.0), (tW, 0.0)], 0.3, 1.4)
    envy = prog(t, tH - 0.2, 0.4)
    mood = "envy" if t > tE - 0.2 else ("angry" if t > tW + 0.2 else ("hurt" if t > tR - 0.1 else "calm"))
    front = mix(mix((-0.5, -0.5), HEART, pain), (-0.25, -2.0), envy)
    pts = duryo(cr, t, x, s, mood=mood, gada=True, feet=f, front=front, head=-0.06 * envy + 0.1 * pain,
                hits=[(tR, 0.4), (tH, 0.5)], ph=0.9, rot=0.012 * envy * math.sin(t * 17))
    chest = to_user(cr, pts["chest"])
    warm(cr, chest[0] + 20, chest[1] + 30, 170, 0.75 * pain, (1.0, 0.25, 0.15))   # the hurt at his heart
    burn = prog(t, tH, 0.5) * (0.75 + 0.25 * prog(t, tB, 0.4))
    if burn > 0.01:
        green_glow(cr, chest[0] + 20, chest[1] + 30, 260 + 60 * math.sin(t * 5), burn)
        gflames(cr, t, chest[0] + 22, chest[1] + 64, 0.16 + 0.05 * prog(t, tB, 0.4), 0.85 * burn, 3, 34)

    def ui(cr):
        if t < tW:
            head2(cr, t, "WHAT REALLY", t0 + 0.05, "HURT HIM?", t0 + 0.5, big_size=240)
        elif t < tE:
            head2(cr, t, "THE PANDAVAS'", tW - 0.05, "MONEY & GLORY", tG, big_size=220)
        else:
            head2(cr, t, "HE FELT", tE - 0.1, "ENVY", tE, big_size=280, under=tE + 0.4)
            q = back(clamp((t - tE - 0.2) / 0.35), 1.4)
            if q > 0.01:                                # the spoken word, on a plaque
                prop(cr, "plaque", 540, 700 + 40 * (1 - q), 0.6, alpha=clamp(q))
                native(cr, tl, ENVY, ENVY_LAT, 540, 700 + 40 * (1 - q), 92, INK, clamp(q), maxw=380)
        tag(cr, t, tW + 0.3, "THE PANDAVAS' MONEY", 720, 1560, 30, t_out=tE)
    return dict(ui=ui, flash=flash_at(t, tR, 0.12) + flash_at(t, tW, 0.2) + flash_at(t, tE, 0.4, 5.0))


# ------------------------------------------------------------------ m10c  callback: the laugh we blame; its root


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "m10c")
    tL, tR, tH = c["L"], c["R"], c["H"]
    up = ease((t - tR + 0.1) / 0.6) if t > tR - 0.1 else 0.0
    x, y, s = CARD1
    glow(cr, x, y - 240 * up, 760, 0.4)
    qcard(cr, t, tl, None, x, y - 250 * up, s * (1 - 0.22 * up), alpha=1 - 0.25 * up)
    prop(cr, "ground", W / 2, 1806, 0.82)
    if t > tL - 0.2 and t < tR + 0.3:                   # the laugh we all blame: her, small, laughing (as on TV)
        b, k, a = depth(t, tL - 0.2, 0.4)
        rot, hd = laughing(t, tL, 0.4)
        dr = draupadi(cr, t, 270, 0.56 * k, 1800, mood="laugh", alpha=a * (1 - prog(t, tR - 0.1, 0.35)), blur=b,
                      rot=rot, hd=hd, ph=0.4)
        hx, hy = to_user(cr, dr["head"])
        ha2(cr, t, tL + 0.05, hx, hy - 30, 1, 34, 1 - prog(t, tR - 0.1, 0.35))
    if t > tR - 0.3:                                    # its root: in someone else's heart
        b, k, a = depth(t, tR - 0.3, 0.45)
        pts = duryo(cr, t, 540, 0.62 * k, mood="envy", gada=True, feet=1800, alpha=a, blur=b, front=(-0.25, -2.0),
                    ph=0.9, y=1800 - 434 * 0.62 * k, hits=[(tH, 0.4)])
        ch = to_user(cr, pts["chest"])
        burn = prog(t, tH - 0.1, 0.4)
        green_glow(cr, ch[0] + 20, ch[1] + 30, 240 + 50 * math.sin(t * 5), burn)
        gflames(cr, t, ch[0] + 22, ch[1] + 64, 0.17, 0.85 * burn, 3, 34)
        if burn > 0.01:
            red_ring(cr, ch[0] + 20, ch[1] + 40, 120, 120, prog(t, tH + 0.2, 0.45), 9)

    def ui(cr):
        if t < tR:
            head2(cr, t, "THE LAUGH", t0 + 0.05, "WE ALL BLAME...", tL, big_size=210)
        else:
            head2(cr, t, "ITS REAL ROOT:", tR - 0.1, "HIS OWN HEART", tH, big_size=220, under=tH + 0.4)
    return dict(ui=ui, flash=flash_at(t, tR, 0.15) + flash_at(t, tH, 0.3))


# ------------------------------------------------------------------ m11  the real cause?


CARDS11 = ((300, ("DRAUPADI'S", "LAUGH?")), (780, ("DURYODHANA'S", "ENVY?")))
CARD11_Y = 960


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "m11")
    tQ, tD, tY = c["Q"], c["D"], c["Y"]
    glow(cr, 540, 1400, 640, 0.4)
    prop(cr, "ground", W / 2, 1796, 0.82)
    b, k, a = depth(t, t0 + 0.2, 0.45)
    draupadi(cr, t, 300, 0.5 * k, 1790, mood="smile", ph=0.4, hits=[(tD, 0.4)], alpha=a, blur=b)
    b, k, a = depth(t, t0 + 0.6, 0.45)
    pts = duryo(cr, t, 790, 0.56 * k, mood="envy", gada=True, feet=1790, flip=True, ph=0.9, hits=[(tY, 0.4)],
                alpha=a, blur=b, y=1790 - 434 * 0.56 * k)
    ch = to_user(cr, pts["chest"])
    green_glow(cr, ch[0], ch[1] + 30, 180, 0.6 * prog(t, tY, 0.4))

    def ui(cr):
        head2(cr, t, "SO WHAT WAS", t0 + 0.05, "THE REAL CAUSE?", tQ, big_size=210)
        for i, (x, (l1, l2)) in enumerate(CARDS11):
            card(cr, t, t0 + 0.3 + 0.15 * i, x, CARD11_Y, 0.58, [(l1, 84, INK, -46), (l2, 120, RED, 52)], rod=False)
        if t > tD:
            if t < tY:
                k_, ts = 0, tD
            else:
                n = int((t - tY) / 0.9)
                k_, ts = (1 if n % 2 == 0 else 0), tY + 0.9 * n
            red_ring(cr, CARDS11[k_][0], CARD11_Y + 4, 250, 110, prog(t, ts, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tD, 0.12) + flash_at(t, tY, 0.12))


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("m1", None, s_hook, {"z": (1.0, 1.04)}),
    ("m2", None, s_tv, {"z": (1.0, 1.03)}),
    ("m3", None, s_book, {"z": (1.0, 1.03)}),
    ("m4", None, s_cousins, {"z": (1.0, 1.03)}),
    ("m5", None, s_panels, {"z": (1.0, 1.02)}),
    ("m6", None, s_splash, {"z": (1.0, 1.04), "focus": (600, 1500)}),
    ("m7", None, s_laugh, {"z": (1.0, 1.03)}),
    ("m8", None, s_list, {"z": (1.0, 1.02)}),
    ("m9", None, s_claim, {"z": (1.0, 1.03)}),
    ("m10", None, s_envy, {"z": (1.0, 1.03)}),
    ("m10c", None, s_callback, {"z": (1.0, 1.03)}),
    ("m11", None, s_end, {"z": (1.0, 1.03)}),
]


def shot_at(t, tl):
    """(index, start, end) of the shot at t; the starts are cached on the timeline under this reel's own name."""
    st = getattr(tl, "_ak_starts", None)
    if st is None:
        st = tl._ak_starts = starts(tl, SHOTS)
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
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a hit at
    the splash, a conch as NOBODY SAID IT is stamped, shimmer as the magic palace appears, a bell on the closing
    question, then (only where they fit) a hit as the first stamp lands and a damaru at ENVY. Chosen in THAT order of
    importance, each at least SFX_MIN_GAP from every sound already kept (as render_myth.calm_sfx keeps them), so the
    list returned is what plays (about 6 sounds); the bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["m6"]["B"], "hit", 0), (c["m9"]["K"], "conch", 0), (c["m4"]["J"], "shimmer", 0),
            (c["m11"]["Q"], "bell", 0), (c["m1"]["N"], "hit", 0), (c["m10"]["E"], "damaru", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["m1"]["N"] - 0.3, "dip", 0.4), (c["m6"]["B"] - 0.3, "dip", 0.45), (c["m9"]["K"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
