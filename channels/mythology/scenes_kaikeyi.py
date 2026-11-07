"""Scenes for videos/kaikeyi.py: a fair debate on Kaikeyi, in Togalu Gombeyaata (Karnataka leather shadow-puppet theatre)
drawn in code: the same lamp-lit screen, two-tier headlines and rod-puppet motion as the Jarasandha and Ravana reels,
with the cast from kaikeyi_cast. The central device is a leather balance scale: one pan FOR KAIKEYI, one AGAINST
KAIKEYI, palm-leaf evidence tags with the verse numbers landing in the pans, the beam swinging as each point lands.
Every frame is a pure function of t. English on-screen text only (shared by Hindi and Kannada); cues are words of the
line in each language ({"hi": ..., "kn": ...}) with a fraction fallback, kept in one table (CUES) that the scenes and
sfx() both read, so the pictures and the sounds always land together.

Shot list (line: what is on the screen)
  k1  HOOK: Kaikeyi alone and large; EVERYONE CALLS HER / THE VILLAIN (big word in by 0.4 s); pointing hands slide in
      from the edges; a red "?" stamp lands after VILLAIN on "khalnayika"; on "Ayodhya" she steps aside and the crown
      comes down; on "bete" a small Bharata appears and the crown floats over his head: ... BELONGED TO / HER SON
  k2  Rama (blue, bow) speaking to Bharata: AND WHO SAID IT? / RAMA HIMSELF; TO BHARATA tag; the palm-leaf tag
      VALMIKI RAMAYANA / AYODHYA KANDA 107.3 drops in, 107.3 turns red and is ringed
  k3  the wedding fire; Dasharatha and Kaikeyi, garlands fly onto them, petals; her father the Kekaya king walks in
      (KEKAYA KING tag); the promise scroll arcs from Dasharatha to him: TO HER FATHER, / A PROMISE
  k4  the scale (FOR KAIKEYI lit, AGAINST dim); THE BRIDE-PRICE: / THE KINGDOM, the crown of Ayodhya comes down; on
      "beta" it flies into the FOR pan with the 107.3 leaf (KAIKEYI'S SON tag), the beam tips; ... WOULD BE / KING
  k5  palm-leaf calendar flipping: AND THEN, MANY / YEARS LATER; the palace, Dasharatha announces, Rama under a
      hovering crown, coronation drums; on "Bharata": BUT AT THAT TIME, / WHERE WAS BHARATA? + his faint shadow, "?"
  k6  cloth map: AYODHYA, then KEKAYA with Bharata, dotted line, FAR AWAY; a small Dasharatha speaks; his words on a
      torn note WHILE BHARATA IS AWAY, / NOW IS THE TIME. with the palm leaf 2.4.25; underlined on "time"
  k7  the invitation list written with a quill: OTHER KINGS (tick), KEKAYA KING (cross), JANAKA (cross), leaf 2.1.46;
      on "later" the list moves up, the scale returns and the 2.1.46 leaf flies into the FOR pan: it tips further
  k8  RE-HOOK: the screen darkens, the beam swings hard to FOR: SO WAS SHE / RIGHT?, a ring round the FOR pan
  k9  WAIT. slams in (the screen shakes); the AGAINST pan lights up: NOW, THE / OTHER SIDE
  k10 SHE ASKED THE THRONE FOR / BHARATA (ring on the crown); the card 14 YEARS / IN THE FOREST drops on the AGAINST
      pan, the beam swings back: BUT ALSO, FOR RAMA: / EXILE; stamp NOT IN THE / WEDDING PROMISE
  k11 Dasharatha before the empty throne; the lamp dims, his head bows, his crown slips and falls, he fades softly:
      IN GRIEF FOR HIS SON, KING DASHARATHA / PASSED AWAY (in ink, not red; only a soft bell)
  k12 Bharata returns; Kaikeyi offers him the crown; he turns away (AND BLAMED / HIS OWN MOTHER), turns back, pushes
      it away and it falls: AND HE / REFUSED THE THRONE
  k13 the forest; Rama and the kneeling Bharata; leaf 107.3 (THE OLD PROMISE); card THE KINGDOM / IS YOURS with a
      crown over Bharata; BUT TO KEEP HIS / FATHER'S WORD; trees close round Rama: RAMA STAYED IN THE / FOREST
  k14 Bharata carries Rama's sandals on his head to the empty throne and sets them on it: RAMA'S SANDALS; the YEARS
      counter ticks 1..14; Bharata kneels before the throne
  k15 the scale settles level with Kaikeyi in one pan and Dasharatha in the other; cards KAIKEYI? and DASHARATHA?;
      SO WHO WAS / WRONG?; a red ring alternates between the cards
"""
import math

import cairo

import kaikeyi_cast as K
import puppet_core as pc
from poster import HEAD_FONT, MONO_FONT, back, clamp, cross, draw_text, ease, prog, text_size, tick
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_jarasandha import (FADE, FEET, INK, LIGHT, RED, big_word, bob_rot, glow, ground, man_angles, motes,
                               red_ring, small_line, sound_rings, stamp, tag, walk_legs, woman_angles)
from scenes_ravana import dotted, head2, in_hand
from shots import T, shot_at, starts

MISSES = set()                       # cue words not found in a line (falls back to fractions)
D = K.PAN_DROP


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, words)
    except (KeyError, ValueError):
        MISSES.add((bid, words[getattr(tl, "lang", "hi")] if isinstance(words, dict) else words))
        return T(tl, bid, frac)


# Every cue of every line: (name, {"hi": word, "kn": word}, fraction fallback, ((after, min gap), ...)); "t0" = the
# line's start. The guards keep the beats in order and far enough apart when a voice reads fast.
CUES = {
    "k1": (("V", {"hi": "खलनायिका", "kn": "ಖಳನಾಯಕಿ"}, 0.38, (("t0", 1.6),)),
           ("A", {"hi": "अयोध्या", "kn": "ಅಯೋಧ್ಯೆಯ"}, 0.6, (("V", 1.0),)),
           ("S", {"hi": "बेटे", "kn": "ಮಗನಿಗೇ"}, 0.82, (("A", 0.8),))),
    "k2": (("R", {"hi": "राम", "kn": "ರಾಮನೇ"}, 0.3, (("t0", 0.5),)),
           ("B", {"hi": "भरत", "kn": "ಭರತನಿಗೆ"}, 0.42, (("R", 0.5),)),
           ("V", {"hi": "वाल्मीकि", "kn": "ವಾಲ್ಮೀಕಿ"}, 0.68, (("B", 0.8),)),
           ("K", {"hi": "अयोध्या", "kn": "ಅಯೋಧ್ಯಾ"}, 0.85, (("V", 0.5),))),
    "k3": (("D", {"hi": "दशरथ", "kn": "ದಶರಥ"}, 0.05, ()),
           ("W", {"hi": "शादी", "kn": "ಮದುವೆ"}, 0.3, (("t0", 0.6),)),
           ("F", {"hi": "पिता", "kn": "ತಂದೆ"}, 0.48, (("W", 0.6),)),
           ("K", {"hi": "केकय", "kn": "ಕೇಕಯ"}, 0.6, (("F", 0.3),)),
           ("P", {"hi": "वादा", "kn": "ಮಾತು"}, 0.86, (("K", 0.5),))),
    "k4": (("R", {"hi": "राज्य", "kn": "ರಾಜ್ಯ"}, 0.25, (("t0", 0.4),)),
           ("S", {"hi": "बेटा", "kn": "ಮಗನೇ"}, 0.6, (("R", 0.9),)),
           ("K", {"hi": "राजा", "kn": "ಆಗ್ತಾನೆ"}, 0.85, (("S", 0.6),))),
    "k5": (("C", {"hi": "राज्याभिषेक", "kn": "ಪಟ್ಟಾಭಿಷೇಕ"}, 0.4, (("t0", 1.0),)),
           ("B", {"hi": "भरत", "kn": "ಭರತ"}, 0.82, (("C", 1.0),))),
    "k6": (("M", {"hi": "मामा", "kn": "ಸೋದರಮಾವನ"}, 0.06, (("t0", 0.3),)),
           ("K", {"hi": "केकय", "kn": "ಕೇಕಯದಲ್ಲಿ"}, 0.2, (("M", 0.4),)),
           ("D", {"hi": "दशरथ", "kn": "ದಶರಥನೇ"}, 0.38, (("K", 1.0),)),
           ("W", {"hi": "बाहर", "kn": "ಇಲ್ಲದಿರುವಾಗಲೇ"}, 0.68, (("D", 0.5),)),
           ("T", {"hi": "समय", "kn": "ಸಮಯ"}, 0.9, (("W", 0.6),))),
    "k7": (("H", {"hi": "जल्दी", "kn": "ಅವಸರದಲ್ಲಿ"}, 0.05, ()),
           ("K", {"hi": "केकय", "kn": "ಕೇಕಯ"}, 0.2, (("t0", 0.9),)),
           ("J", {"hi": "जनक", "kn": "ಜನಕನನ್ನೂ"}, 0.45, (("K", 0.8),)),
           ("L", {"hi": "बाद", "kn": "ಆಮೇಲೆ"}, 0.72, (("J", 0.8),))),
    "k8": (("H", {"hi": "हक़", "kn": "ಹಕ್ಕನ್ನ"}, 0.65, (("t0", 0.5),)),),
    "k9": (("O", {"hi": "दूसरी", "kn": "ಇನ್ನೊಂದು"}, 0.4, (("t0", 0.6),)),),
    "k10": (("B", {"hi": "भरत", "kn": "ಭರತನಿಗೆ"}, 0.08, (("t0", 0.3),)),
            ("A", {"hi": "माँगा", "kn": "ಕೇಳಿದ್ಲು"}, 0.22, (("B", 0.5),)),
            ("F", {"hi": "चौदह", "kn": "ಹದಿನಾಲ್ಕು"}, 0.48, (("A", 0.8),)),
            ("E", {"hi": "वनवास", "kn": "ವನವಾಸ"}, 0.6, (("F", 0.4),)),
            ("W", {"hi": "शादी", "kn": "ಮದುವೆಯ"}, 0.85, (("E", 0.8),))),
    "k11": (("G", {"hi": "ग़म", "kn": "ದುಃಖದಲ್ಲಿ"}, 0.25, ()),
            ("X", {"hi": "चल बसे", "kn": "ಪ್ರಾಣ"}, 0.72, (("t0", 0.9),))),
    "k12": (("M", {"hi": "माँ", "kn": "ಅಮ್ಮನನ್ನೇ"}, 0.35, (("t0", 0.9),)),
            ("R", {"hi": "धिक्कारा", "kn": "ಬೈದ"}, 0.5, (("M", 0.4),)),
            ("N", {"hi": "मना", "kn": "ಬೇಡ"}, 0.82, (("R", 0.8),))),
    "k13": (("O", {"hi": "पुराना", "kn": "ಹಳೇ"}, 0.1, (("t0", 0.3),)),
            ("Y", {"hi": "तुम्हारा", "kn": "ನಿನ್ನದೇ"}, 0.35, (("O", 0.8),)),
            ("P", {"hi": "पिता", "kn": "ತಂದೆಯ"}, 0.55, (("Y", 0.8),)),
            ("S", {"hi": "वन में", "kn": "ಕಾಡಲ್ಲೇ"}, 0.85, (("P", 0.8),))),
    "k14": (("P", {"hi": "खड़ाऊँ", "kn": "ಪಾದುಕೆಗಳನ್ನ"}, 0.15, (("t0", 0.3),)),
            ("T", {"hi": "सिंहासन", "kn": "ಸಿಂಹಾಸನದ"}, 0.3, (("P", 0.6), ("t0", 1.2))),
            ("F", {"hi": "चौदह", "kn": "ಹದಿನಾಲ್ಕು"}, 0.5, (("T", 0.8),)),
            ("N", {"hi": "नाम", "kn": "ಹೆಸರಲ್ಲೇ"}, 0.75, (("F", 0.6),))),
    "k15": (("K", {"hi": "कैकेयी", "kn": "ಕೈಕೇಯಿದಾ"}, 0.3, (("t0", 0.5),)),
            ("D", {"hi": "दशरथ", "kn": "ದಶರಥನದ್ದಾ"}, 0.55, (("K", 0.6),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_kk_cues", None)
    if cache is None:
        cache = {}
        tl._kk_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, words, frac, cons in CUES[bid]:
            v = cue(tl, bid, words, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


# ------------------------------------------------------------------ puppets


def fig(cr, rig, key, t, x, s, front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0), hits=(),
        flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, feet=FEET, ph=0.0, extra=None, swap=None, kneel=None,
        y=None):
    """A man() puppet standing (hip at feet - 434 s) or kneeling (kneel = the kneeling-legs sprite); front / backa are
    the arms' (upper, fore) angles: 0 hangs down, -pi/2 points forward, -pi points up."""
    ang = man_angles(key, t, front, backa, head, legs, hits, ph)
    hide = ()
    r = rot + bob_rot(t, ph)
    if kneel:
        hy = feet - 250 * s if y is None else y
        prop(cr, kneel, x, hy, s, r, alpha, blur, flip)
        hide = (key + "_legF", key + "_legB")
    else:
        hy = feet - 434 * s if y is None else y
    return puppet(cr, rig, x, hy, s, r, flip, ang, alpha, blur, hide=hide, swap=swap, rods=rods, extra=extra)


def walk(cr, t, fn, t0, t1, x0, x1, s, t_in=None, step=0.42, **kw):
    """A man() puppet (fn = rama / bharata / ...) walking in jerky rod-puppet steps, brought onto the cloth."""
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    kw.setdefault("hits", [(t1, 1.0)])
    y = FEET - 434 * s + bob - (k - 1) * 300 * s
    return fn(cr, t, x, s * k, legs=walk_legs(ph), rot=rock, alpha=a, blur=b, y=y, **kw)


def kai(cr, t, x, s, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(), flip=False, alpha=1.0, blur=0.0,
        rods=True, rot=0.0, feet=FEET, ph=0.0, y=None):
    """Kaikeyi (feet on `feet`)."""
    ang = woman_angles("kaikeyi", t, front, backa, head, hits, ph)
    hy = feet - 470 * s if y is None else y
    return puppet(cr, K.KAIKEYI, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, rods=rods)


BOW = {"rama_armB_lo": in_hand("bow", 160, 0.0, 0.62)}
ANJALI = dict(front=(-0.75, -1.85), backa=(-0.8, -1.8))          # hands joined in front of the chest


def rama(cr, t, x, s, **kw):
    kw.setdefault("extra", BOW)
    return fig(cr, K.RAMA, "rama", t, x, s, **kw)


def bharata(cr, t, x, s, **kw):
    return fig(cr, K.BHARATA, "bharata", t, x, s, **kw)


def dasha(cr, t, x, s, **kw):
    return fig(cr, K.DASHARATHA, "dasharatha", t, x, s, **kw)


def kekaya(cr, t, x, s, **kw):
    return fig(cr, K.KEKAYA, "kekaya", t, x, s, **kw)


# ------------------------------------------------------------------ text pieces


def plaque(cr, text, x, y, size, color=INK, alpha=1.0, font=HEAD_FONT, fill=None, pad=(40, 26)):
    """A small leather plaque with one line of text, centred on (x, y) in the current coordinates."""
    if alpha <= 0.01:
        return
    w, h = text_size(text, size, font)
    bw, bh = w + pad[0], h + pad[1]
    cr.save()
    cr.translate(x, y)
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    c = 10
    pc.poly(cr, [(-bw / 2, -bh / 2 + c), (-bw / 2 + c, -bh / 2), (bw / 2 - c, -bh / 2), (bw / 2, -bh / 2 + c),
                 (bw / 2, bh / 2 - c), (bw / 2 - c, bh / 2), (-bw / 2 + c, bh / 2), (-bw / 2, bh / 2 - c)])
    cr.set_source_rgba(*(fill or pc.PARCH), alpha)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, alpha)
    cr.set_line_width(4)
    cr.stroke()
    cr.set_operator(cairo.OPERATOR_OVER)
    for k in range(int(bw // 18)):
        cr.arc(-bw / 2 + 12 + k * 18, -bh / 2 + 7, 2.2, 0, 2 * math.pi)
        cr.arc(-bw / 2 + 12 + k * 18, bh / 2 - 7, 2.2, 0, 2 * math.pi)
    cr.set_source_rgba(*LIGHT, 0.85 * alpha)
    cr.fill()
    draw_text(cr, text, 0, 1, size, color, alpha, font, "cm")
    cr.restore()


def segs_line(cr, segs, x, y, size, font, alpha, tracking=0):
    """One centred line built from coloured segments [(text, colour)]; returns [(x0, w)] per segment."""
    ws = [text_size(s, size, font, tracking)[0] for s, _ in segs]
    sp = size * 0.4
    tot = sum(ws) + sp * (len(segs) - 1)
    xx = x - tot / 2
    boxes = []
    for (s, col), w in zip(segs, ws):
        draw_text(cr, s, xx, y, size, col, alpha, font, "lm", tracking)
        boxes.append((xx, w))
        xx += w + sp
    return boxes


def leaf_tag(cr, t, t_in, x, y, s, lines, rot=-0.04, alpha=1.0, t_out=None, rod=True):
    """A palm-leaf evidence tag dropping in on its rod. lines = [(text or [(text, colour)], size, font)] in leaf
    units (the leaf is 540 x 88). Returns ({line: ([(x0, w)], centre y)}, (x, y, s, rot)) in leaf units."""
    p = back(clamp((t - t_in) / 0.35), 1.3) if t_in is not None else 1.0
    a = clamp((t - t_in) / 0.18) * alpha if t_in is not None else alpha
    if t_out is not None:
        a *= 1 - clamp((t - t_out) / 0.25)
    if a <= 0.01:
        return {}, None
    yy = y - 70 * (1 - p)
    r = rot + sway(t, 0.012, 0.45, x * 0.01)
    if rod:
        pc.rod(cr, x + 60 * s, yy + 40 * s, x + 90, H + 50, alpha=0.5 * a)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(r)
    cr.scale(s, s)
    pc.paint_part(cr, "kk_leaf", a)
    hs = [sz * 1.12 for _, sz, _ in lines]
    y0 = -sum(hs) / 2
    out = {}
    for i, ((txt, sz, font), hh) in enumerate(zip(lines, hs)):
        cy = y0 + hh / 2
        segs = [(txt, INK)] if isinstance(txt, str) else txt
        out[i] = (segs_line(cr, segs, 0, cy, sz, font, a, 3 if font == MONO_FONT else 0), cy)
        y0 += hh
    cr.restore()
    return out, (x, yy, s, r)


EV_2425 = [("AYODHYA KANDA", 34, MONO_FONT), ("2.4.25", 52, HEAD_FONT)]
EV_2146 = [("AYODHYA KANDA", 34, MONO_FONT), ("2.1.46", 52, HEAD_FONT)]
EV_1073 = [("AYODHYA KANDA", 34, MONO_FONT), ("107.3", 52, HEAD_FONT)]


def stamp2(cr, t, t_in, lines, x, y, size, rot=-0.06, color=RED, alpha=1.0):
    """A red rubber stamp with two or more lines."""
    p = clamp((t - t_in) / 0.2)
    if p <= 0:
        return
    s = 1.7 - 0.7 * back(p, 2.0)
    ws = [text_size(ln, size, tracking=4) for ln in lines]
    w = max(a for a, _ in ws)
    h = sum(b for _, b in ws) + 14 * (len(lines) - 1)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.set_source_rgba(*color, 0.88 * p * alpha)
    cr.set_line_width(7)
    cr.rectangle(-w / 2 - 26, -h / 2 - 18, w + 52, h + 36)
    cr.stroke()
    yy = -h / 2
    for ln, (_, hh) in zip(lines, ws):
        draw_text(cr, ln, 0, yy, size, color, 0.92 * p * alpha, anchor="ct", tracking=4)
        yy += hh + 14
    cr.restore()


def q_stamp(cr, t, t_in, x, y, r, rot=0.14, alpha=1.0):
    """The red "?" stamp of the hook: a ring with a question mark, slammed on."""
    p = clamp((t - t_in) / 0.2)
    if p <= 0:
        return
    s = 1.8 - 0.8 * back(p, 2.0)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    cr.set_source_rgba(*RED, 0.9 * p * alpha)
    cr.set_line_width(10)
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.stroke()
    draw_text(cr, "?", 2, 4, int(r * 1.6), RED, p * alpha, anchor="cm")
    cr.restore()


def card(cr, t, t_in, x, y, s, lines, alpha=1.0, rod=True, t_out=None):
    """A leather plaque card dropping in on its rod; lines = [(text, size, colour, dy)] in plaque units."""
    q = back(clamp((t - t_in) / 0.35), 1.4)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.25)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    yy = y + 60 * (1 - q)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(sway(t, 0.01, 0.4, x * 0.01))
    cr.scale(s, s)
    pc.paint_part(cr, "plaque", a)
    for txt, sz, col, dy in lines:
        draw_text(cr, txt, 0, dy, sz, col, a, anchor="cm")
    cr.restore()
    if rod:
        pc.rod(cr, x, yy + 110 * s, x + 30, H + 60, alpha=0.5 * a)


# ------------------------------------------------------------------ the balance scale


def settle(t, keys, freq=0.85, decay=2.1):
    """The beam's tilt: from each key (time, value) it swings to the new value like a pendulum and settles."""
    def val(i, tt):
        if i == 0:
            return keys[0][1]
        tb, vb = keys[i]
        if tt < tb:
            return val(i - 1, tt)
        v0 = val(i - 1, tb)
        dt = tt - tb
        return vb + (v0 - vb) * math.exp(-decay * dt) * math.cos(2 * math.pi * freq * dt)
    return val(len(keys) - 1, t)


def drop_q(t, t_land, dur=0.45):
    """0 (still above, out of sight) .. 1 (landed) for something dropped to land at t_land; None = always there."""
    if t_land is None:
        return 1.0
    return clamp((t - t_land + dur) / dur)


CROWN_IN_PAN = (-80, D + 22, 0.52)       # where the crown sits in the FOR pan (pan units)


def _pan_items(cr, t, items):
    """Things in a pan (pan units: the hook at 0, 0, the rim at y = D). Leaves first, then the crown, then cards and
    figures."""
    order = {"leaf": 0, "crown": 1, "card": 2, "fig": 3}
    nleaf = 0
    for it in sorted(items, key=lambda i: order[i["kind"]]):
        q = drop_q(t, it.get("t"))
        k = it["kind"]
        if k == "leaf":
            slot = nleaf
            nleaf += 1
        if q <= 0:
            continue
        dy = -620 * (1 - q) ** 2
        a = clamp(q * 3) * it.get("alpha", 1.0)
        if k == "leaf":                                 # stacked to the right of the crown, numbers showing
            x, y = 48 + 4 * (slot % 2), D - 8 - 37 * slot
            r = (-0.03, 0.025, -0.015, 0.03)[slot % 4]
            cr.save()
            cr.translate(x, y + dy)
            cr.rotate(r)
            cr.scale(0.42, 0.42)
            pc.paint_part(cr, "kk_leaf", a)
            draw_text(cr, it["text"], 78, 3, 100, INK, a, anchor="cm")
            cr.restore()
        elif k == "crown":
            cx, cy, cs = CROWN_IN_PAN
            prop(cr, "kk_crown", cx, cy + dy, cs, alpha=a)
        elif k == "card":
            cr.save()
            cr.translate(0, D - 46 + dy)
            cr.rotate(0.02)
            cr.scale(0.42, 0.42)
            pc.paint_part(cr, "plaque", a)
            draw_text(cr, it["lines"][0], 0, -24, 118, RED, a, anchor="cm")
            draw_text(cr, it["lines"][1], 0, 60, 58, INK, a, MONO_FONT, "cm", tracking=2)
            cr.restore()
        elif k == "fig":
            it["fn"](cr, t, D + 34 + dy, a)


def balance(cr, t, x, foot, s, tilt_fn, left=(), right=(), alpha=1.0, blur=0.0, labels=1.0, lit=0.0, for_lit=1.0):
    """The leather balance scale standing at (x, foot). tilt_fn(t) > 0: the FOR KAIKEYI (left) pan is down.
    left / right: pan items (dicts: kind crown | leaf (text) | card (lines) | fig (fn), t = landing time).
    lit 0..1 lights the AGAINST pan; labels = alpha of the pan labels. Returns [(hook x, y, swing)] per pan."""
    tilt = tilt_fn(t)
    vel = (tilt - tilt_fn(t - 0.06)) / 0.06
    sw = clamp(0.32 * vel, -0.3, 0.3) + 0.018 * math.sin(t * 1.9)
    prop(cr, "kk_post", x, foot, s, alpha=alpha, blur=blur)
    px, py = x, foot - K.POST_H * s
    out = []
    for side in (-1, 1):
        ex = px + side * K.BEAM_L * s * math.cos(tilt)
        ey = py - side * K.BEAM_L * s * math.sin(tilt)
        out.append((ex, ey, sw * (1.0 if side < 0 else 0.85)))
    prop(cr, "kk_beam", px, py, s, rot=-tilt, alpha=alpha, blur=blur)
    for (ex, ey, swp), side, items in zip(out, (-1, 1), (left, right)):
        lt = lit if side > 0 else 0.0
        if lt > 0:
            glow(cr, ex, ey + (D + 20) * s, 330 * s, 0.7 * lt * (0.85 + 0.15 * math.sin(t * 5)))
        cr.save()
        cr.translate(ex, ey)
        cr.rotate(swp)
        cr.scale(s, s)
        _pan_items(cr, t, items)
        pc.paint_part(cr, "kk_pan", alpha, blur)
        if labels > 0:
            ink_a = labels * alpha
            cr.set_source_rgba(*INK, 0.8 * ink_a)
            cr.set_line_width(3)
            cr.move_to(0, D + 54)
            cr.line_to(0, D + 92)
            cr.stroke()
            if side < 0:
                plaque(cr, "FOR KAIKEYI", 0, D + 124, 48, INK, ink_a * (0.55 + 0.45 * for_lit))
            else:
                col = tuple(FADE[i] + (RED[i] - FADE[i]) * lt for i in range(3))
                plaque(cr, "AGAINST KAIKEYI", 0, D + 124, 48, col, ink_a * (0.5 + 0.5 * lt))
        cr.restore()
    return out


def pan_xy(pan, s, lx, ly):
    """Screen position of a point (lx, ly) in a pan's units."""
    ex, ey, swp = pan
    c, si = math.cos(swp), math.sin(swp)
    return ex + s * (lx * c - ly * si), ey + s * (lx * si + ly * c)


# tilt of the beam through the reel (rad, + = FOR KAIKEYI heavier)
TILT_K4, TILT_K6, TILT_K7, TILT_K8, TILT_K10 = 0.13, 0.19, 0.26, 0.36, -0.2


def for_items(t_crown=None, t_107=None, t_2425=None, t_2146=None):
    """What lies in the FOR pan: the crown and the evidence leaves (None = already there; False = not yet)."""
    out = []
    for kind, tt, text in (("leaf", t_107, "107.3"), ("leaf", t_2425, "2.4.25"), ("leaf", t_2146, "2.1.46"),
                           ("crown", t_crown, None)):
        if tt is False:
            continue
        out.append(dict(kind=kind, t=tt, text=text))
    return out


# ------------------------------------------------------------------ k1  hook


HANDS = (   # (side, y, tip x, rot, delay, sprite)
    (-1, 820, 330, 0.30, 0.0, 0), (1, 1020, 800, 0.22, 0.25, 1), (-1, 1330, 350, -0.22, 0.5, 2),
    (1, 1480, 770, -0.30, 0.7, 0))
HAND_T0 = 0.95


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "k1")
    tV, tA, tS = c["V"], c["A"], c["S"]
    feet = 1790
    # Kaikeyi: large and alone, then she steps aside for the crown
    side = keyed(t, [(0.0, 0.0), (tA - 0.1, 1.0)], 0.45, 1.3)
    s = 1.15 - 0.17 * side
    x = 530 - 200 * side
    look = keyed(t, [(0.0, 0.0), (tV, 1.0), (tA, 0.0)], 0.3, 1.5)
    kai(cr, t, x, s, front=(-0.25 - 0.3 * look, -0.9 - 1.1 * look), backa=(0.12, -0.25), head=-0.06 * look,
        hits=[(tV, 0.8), (tA, 0.6)], feet=feet)
    # the pointing hands of "everyone"
    out = prog(t, tA - 0.45, 0.35)
    for sd, hy, tip, rot, dl, k in HANDS:
        q = back(clamp((t - HAND_T0 - dl) / 0.3), 1.4) * (1 - out)
        if q <= 0:
            continue
        jab = 22 * math.exp(-7 * max(0, t - tV)) * math.sin(14 * max(0, t - tV)) if t > tV else 0.0
        jab += 8 * math.sin(t * 6 + dl * 5)
        hs = 0.9
        L = 384 * hs
        ox = -sd * (L + 60) * (1 - q)
        if sd < 0:
            px = tip - L * math.cos(rot) + ox + jab * math.cos(rot)
            py = hy + L * math.sin(rot) - jab * math.sin(rot)
            prop(cr, f"kk_point{k}", px, py, hs, rot=-rot, alpha=clamp(q * 2))
        else:
            px = tip + L * math.cos(rot) + ox - jab * math.cos(rot)
            py = hy + L * math.sin(rot) - jab * math.sin(rot)
            prop(cr, f"kk_point{k}", px, py, hs, rot=rot, alpha=clamp(q * 2), flip=True)
    # the crown of Ayodhya comes down; on "son" it floats over the small Bharata
    bx, bs, bfeet = 800, 0.5, 1780
    if t > tA - 0.15:
        dq = back(clamp((t - tA + 0.15) / 0.4), 1.3)
        fq = ease((t - tS - 0.1) / 0.7) if t > tS - 0.1 else 0.0
        cx, cy = 800, 800
        top_y = bfeet - 434 * bs - 600 * bs
        x_ = cx + (bx + 10 - cx) * fq
        y_ = (cy - 500 * (1 - dq)) + (top_y - 20 - cy) * fq - 120 * math.sin(math.pi * fq)
        sc = 1.0 + (0.5 - 1.0) * fq
        glow(cr, x_, y_ - 100 * sc, 260 * sc + 60, 0.55 * clamp(dq) * (0.85 + 0.15 * math.sin(t * 4)))
        if fq < 0.05:
            pc.rod(cr, x_, y_ - 120, x_ + 40, H + 60, alpha=0.55 * clamp(dq))
        prop(cr, "kk_crown", x_, y_, sc, rot=sway(t, 0.03, 0.5), alpha=clamp(dq * 2))
        if t > tS - 0.25:
            b, k, a = depth(t, tS - 0.25, 0.4)
            bharata(cr, t, bx, bs * k, front=(-0.6, -0.9), backa=(0.25, -0.3), alpha=a, blur=b, feet=bfeet, ph=1.0)
    fl = 0.4 * math.exp(-5 * max(0, t - tV)) * (t > tV) + 0.3 * math.exp(-4 * max(0, t - tS)) * (t > tS)

    def ui(cr):
        if t < tS:
            small_line(cr, t, [("EVERYONE", -1.0), ("CALLS", -1.0), ("HER", -1.0)], 245, 62)
            size = min(190, int(190 * 740 / text_size("THE VILLAIN", 190)[0]))
            bw = text_size("THE VILLAIN", size)[0]
            r = 66
            dx = (r * 2 + 18) / 2 * ease((t - tV) / 0.25) if t > tV else 0.0
            cr.save()
            cr.translate(-dx, 0)
            _, _, _, bh = big_word(cr, t, "THE VILLAIN", 0.4, 323, size, ghost_from=-1.0)
            cr.restore()
            if t > tV:
                q_stamp(cr, t, tV, W / 2 - dx + bw / 2 + 18 + r, 323 + bh / 2 + 4, r)
            if t > tA + 0.45:
                tag(cr, t, tA + 0.45, "AYODHYA'S CROWN", 800, 900, 32, t_out=tS - 0.2)
        else:
            head2(cr, t, "AYODHYA'S THRONE BELONGED TO", tS, "HER SON", tS + 0.08, big_size=190, under=tS + 0.5)
            tag(cr, t, tS + 0.3, "BHARATA", bx, 1080, 38)
    return dict(ui=ui, flash=fl)


# ------------------------------------------------------------------ k2  Rama said it


def s_rama(cr, t, tl, t0, t1):
    c = cues(tl, "k2")
    tR, tB, tV, tK = c["R"], c["B"], c["V"], c["K"]
    b, k, a = depth(t, t0, 0.5)
    prop(cr, "tree", 1010, FEET + 10, 0.6, rot=sway(t, 0.006, 0.3), alpha=0.6, blur=10)
    prop(cr, "tree", 40, FEET + 10, 0.5, rot=sway(t, 0.006, 0.3, 1), alpha=0.5, blur=12, flip=True)
    ground(cr)
    talk = keyed(t, [(t0, 0.0), (tR - 0.1, 1.0), (tV, 0.4)], 0.3, 1.5)
    w_end = min(t0 + 1.0, tR - 0.2)
    if t < w_end:                                       # Rama walks in to Bharata
        pts = walk(cr, t, rama, t0, w_end, -120, 300, 0.76, t_in=t0, ph=0.5)
    else:
        pts = rama(cr, t, 300, 0.76, front=(-0.5 - 0.9 * talk, -0.6 + 0.2 * talk), hits=[(tR, 0.8), (w_end, 0.6)],
                   ph=0.5)
    if t > tR:
        hx, hy = pts["head"]
        sound_rings(cr, hx + 70, hy + 20, t, tR, 3, 0.3, 150, alpha=0.8)
    listen = prog(t, tB, 0.5)
    bharata(cr, t, 790, 0.7, flip=True, front=(-0.4, -0.5), head=0.12 * listen, hits=[(tB, 0.5)], ph=2.0,
            alpha=a, blur=b)

    def ui(cr):
        head2(cr, t, "AND WHO SAID IT?", t0 + 0.05, "RAMA HIMSELF", tR, big_size=180, under=tR + 0.4)
        tag(cr, t, tB, "TO BHARATA", 790, 770, 36)
        lines = [("VALMIKI RAMAYANA", 44, HEAD_FONT),
                 ([("AYODHYA KANDA", INK), ("107.3", RED if t > tK else INK)], 30, MONO_FONT)]
        boxes, tr = leaf_tag(cr, t, tV, 540, 620, 1.3, lines, rot=-0.03)
        if tr is not None and t > tK:
            segs, cy = boxes[1]
            x0, w = segs[1]
            lx, ly, ls, lr = tr
            cxl = x0 + w / 2
            gx = lx + ls * (cxl * math.cos(lr) - cy * math.sin(lr))
            gy = ly + ls * (cxl * math.sin(lr) + cy * math.cos(lr))
            red_ring(cr, gx, gy, w * ls / 2 + 18, 30, prog(t, tK + 0.1, 0.4), 7)
    return dict(ui=ui, flash=0.25 * math.exp(-4 * max(0, t - tV)) * (t > tV))


# ------------------------------------------------------------------ k3  the wedding and the promise


def s_wedding(cr, t, tl, t0, t1):
    c = cues(tl, "k3")
    tD, tW, tF, tK, tP = c["D"], c["W"], c["F"], c["K"], c["P"]
    glow(cr, 440, FEET - 170, 300, 0.55 * (0.85 + 0.15 * math.sin(t * 7)))
    prop(cr, "altar", 440, FEET + 14, 0.55)
    prop(cr, f"flame{int(t * 10) % 3}", 440, FEET - 30, 0.42)
    ground(cr)
    vow_t = max(tP - 0.15, t0)
    give = keyed(t, [(t0, 0.0), (vow_t, 1.0)], 0.3, 1.4)
    dp = dasha(cr, t, 190, 0.74, front=(-0.5 - 0.7 * give, -0.6 + 0.2 * give), hits=[(tW, 0.5), (vow_t, 0.6)],
               ph=0.3)
    kp = kai(cr, t, 640, 0.74, flip=True, front=(-0.3, -0.8), backa=(0.2, -0.3), hits=[(tW, 0.5)], ph=1.4)
    kk = None
    if t > tF - 0.1:                                    # her father walks in; he reaches up for the promise
        recv = keyed(t, [(t0, 0.0), (tP + 0.1, 1.0)], 0.3, 1.4)
        kk = walk(cr, t, kekaya, tF - 0.1, tF + 0.9, 1250, 950, 0.68, t_in=tF - 0.1, step=0.33, flip=True,
                  front=(-0.4 - 1.7 * recv, -0.6 + 0.2 * recv), ph=2.2)
    # garlands fly onto the couple
    for pts, ph, sc in ((dp, 0, 0.74), (kp, 1, 0.66)):
        q = back(clamp((t - tW - 0.1 * ph) / 0.45), 1.3)
        if q > 0:
            cx, cy = pts["chest"]
            prop(cr, "kk_garland", cx + (8 if ph == 0 else -8), cy - 90 * sc - 420 * (1 - q), sc,
                 rot=sway(t, 0.03, 0.7, ph), alpha=clamp(q * 2))
    if t > tW:                                          # petals drifting down
        for i in range(16):
            dl = (i * 0.137) % 0.7
            u = (t - tW - dl) / (2.2 + 0.4 * ((i * 7) % 3))
            if 0 < u < 1:
                px = 110 + (i * 263) % 860 + 40 * math.sin(t * 2.2 + i)
                py = 470 + (i * 97) % 260 + 1000 * u
                prop(cr, f"rv_mari{i % 2}", px, py, 0.5 + 0.1 * (i % 3), rot=3 * u + i, alpha=1 - u ** 3)
    vow = None
    if t > vow_t - 0.1 and kk is not None:              # the promise: Dasharatha's hand -> the Kekaya king's
        q = ease((t - vow_t) / 0.65)
        hx, hy = dp["handF"]
        kx, ky = kk["handF"]
        vx = hx + (kx - hx) * q
        vy = hy + (ky - hy) * q - 330 * math.sin(math.pi * q)
        glow(cr, vx, vy, 200, 0.5 * prog(t, vow_t - 0.1, 0.3))
        prop(cr, "kk_vow", vx, vy - 20, 0.75, rot=0.4 * math.sin(math.pi * q), alpha=prog(t, vow_t - 0.1, 0.2))
        vow = (vx, vy - 20)

    def ui(cr):
        if t < tP:
            head2(cr, t, "WHEN DASHARATHA MARRIED", t0 + 0.05, "KAIKEYI", tW, big_size=190)
            tag(cr, t, tD + 0.15, "DASHARATHA", 210, 700, 34, t_out=tP - 0.1)
        else:
            head2(cr, t, "TO HER FATHER,", tP, "A PROMISE", tP + 0.05, big_size=200)
            if vow is not None and t > tP + 0.55:
                red_ring(cr, vow[0], vow[1], 140, 70, prog(t, tP + 0.55, 0.4), 8)
        tag(cr, t, tK, "KEKAYA KING", 880, 700, 34)
    return dict(ui=ui, flash=0.25 * math.exp(-4 * max(0, t - tW)) * (t > tW))


# ------------------------------------------------------------------ k4  the bride-price on the scale


def s_price(cr, t, tl, t0, t1):
    c = cues(tl, "k4")
    tR, tS, tKg = c["R"], c["S"], c["K"]
    land = tS + 0.05
    tilt = lambda tt: settle(tt, [(t0 - 9, 0.0), (land, TILT_K4)], 0.8, 1.6)
    b, k, a = depth(t, t0, 0.45)
    ground(cr)
    s = 0.92 * k
    left = for_items(t_crown=None if t >= land else False, t_107=land + 0.15, t_2425=False, t_2146=False)
    pans = balance(cr, t, 540, FEET, s, tilt, left=left, alpha=a, blur=b)
    # the crown: first hanging over the beam as "the kingdom", then flown into the FOR pan
    if tR - 0.2 < t < land:
        q = back(clamp((t - tR + 0.2) / 0.4), 1.3)
        y0 = 690 - 400 * (1 - q)
        u = ease((t - land + 0.45) / 0.45) if t > land - 0.45 else 0.0
        cx_, cy_, cs_ = CROWN_IN_PAN
        px_, py_ = pan_xy(pans[0], s, cx_, cy_)
        x_ = 540 + (px_ - 540) * u
        y_ = y0 + (py_ - y0) * u - 120 * math.sin(math.pi * u)
        sc = 1.0 + (cs_ * s - 1.0) * u
        glow(cr, x_, y_ - 110 * sc, 300 * sc, 0.55 * clamp(q) * (1 - u))
        if u < 0.05:
            pc.rod(cr, 540, y0 - 110, 580, H + 60, alpha=0.4 * clamp(q))
        prop(cr, "kk_crown", x_, y_, sc, rot=sway(t, 0.03, 0.5) * (1 - u), alpha=clamp(q * 2))

    def ui(cr):
        if t < tKg:
            head2(cr, t, "THE BRIDE-PRICE:", t0 + 0.05, "THE KINGDOM", tR, big_size=190)
        else:
            head2(cr, t, "KAIKEYI'S SON WOULD BE", tKg, "KING", tKg + 0.06, big_size=210, under=tKg + 0.35)
        if tR < t < land:
            tag(cr, t, tR + 0.25, "THE CROWN OF AYODHYA", 540, 770, 32, t_out=land - 0.45)
        if t > land:
            ex, ey, _ = pans[0]
            tag(cr, t, land + 0.2, "KAIKEYI'S SON", ex + 10, ey - 110, 34)
    return dict(ui=ui, flash=0.25 * math.exp(-4 * max(0, t - land)) * (t > land))


# ------------------------------------------------------------------ k5  years later, the coronation


SEASONS = ("SPRING", "SUMMER", "MONSOON", "AUTUMN", "WINTER")


def drums(cr, t, t_on, alpha=1.0):
    """Two nagara drums in the bottom corners, beaten from t_on."""
    for i, x in enumerate((150, 930)):
        prop(cr, "kk_drum", x, FEET + 12, 0.72, alpha=alpha)
        for k, sx in enumerate((-1, 1)):
            ph = (t - t_on) / 0.26 + 0.5 * k + 0.25 * i
            lift = abs(math.sin(math.pi * (ph % 1.0))) if t > t_on else 0.6
            hx = x + sx * 40
            hy = FEET + 12 - 150 * 0.72 - 8 - 70 * lift
            for w, col in ((13, INK), (7, pc.BROWN)):
                cr.set_source_rgba(*col, alpha)
                cr.set_line_width(w)
                cr.set_line_cap(cairo.LINE_CAP_ROUND)
                cr.move_to(hx + sx * 40, hy - 78)
                cr.line_to(hx, hy)
                cr.stroke()
            cr.arc(hx, hy, 13, 0, 2 * math.pi)
            cr.set_source_rgba(*INK, alpha)
            cr.fill()
            cr.arc(hx, hy, 8, 0, 2 * math.pi)
            cr.set_source_rgba(*pc.GOLD, alpha)
            cr.fill()
        if t > t_on:
            sound_rings(cr, x, FEET - 140, t, t_on + 0.13 * i, 6, 0.26, 110, alpha=0.4 * alpha)


def calendar(cr, t, t0, t1, n=9):
    """A palm-leaf calendar flipping fast (years go by): the leaf turns on its two rings, edge-on, and comes back
    as the next season; a few leaf edges hang below it (drawn as lines, so the leather does not darken)."""
    flips = clamp((t - t0) / max(0.6, t1 - t0)) * n
    top, s = 760, 1.6
    pc.rod(cr, 540 - 226 * s, top, 240, H + 60, alpha=0.5)
    pc.rod(cr, 540 + 226 * s, top, 840, H + 60, alpha=0.5)
    cur = int(flips)
    ph = flips - cur
    sy = abs(math.cos(math.pi * ph))
    for k in range(4):                                  # the pile's edges under the leaf
        yy = top + 2 * 46 * s + 10 + 9 * k
        cr.set_source_rgba(*INK, 0.7)
        cr.set_line_width(3)
        cr.move_to(540 - 250 * s + 8 * k, yy)
        cr.line_to(540 + 250 * s - 8 * k, yy)
        cr.stroke()
    cr.save()
    cr.translate(540, top)
    cr.scale(s, max(0.03, sy) * s)
    cr.translate(0, 46)
    pc.paint_part(cr, "kk_leaf", 1.0)
    if sy > 0.15:
        draw_text(cr, SEASONS[(cur + (ph > 0.5)) % 5], 0, 2, 50, INK, 0.9, MONO_FONT, "cm", tracking=10)
    cr.restore()
    for sx in (-1, 1):
        cr.new_path()
        cr.arc(540 + sx * 226 * s, top + 4, 15, 0, 2 * math.pi)
        cr.set_source_rgba(*RED, 1)
        cr.set_line_width(7)
        cr.stroke()


def s_years(cr, t, tl, t0, t1):
    c = cues(tl, "k5")
    tC, tB = c["C"], c["B"]
    tP = tC - 0.25                                       # the palace set comes on
    if t < tP:
        calendar(cr, t, t0 + 0.1, tP - 0.1)
        a = 0.8
        prop(cr, "sun", 540 + 330 * math.cos(t * 3), 1250 + 140 * math.sin(t * 3), 0.42, rot=t, alpha=a)
        prop(cr, "moon", 540 - 330 * math.cos(t * 3), 1250 - 140 * math.sin(t * 3), 0.7, alpha=a)

        def ui(cr):
            head2(cr, t, "AND THEN, MANY", t0 + 0.05, "YEARS LATER", t0 + 0.2, big_size=190)
        return dict(ui=ui)
    b, k, a = depth(t, tP, 0.45)
    prop(cr, "arch", 540, FEET + 10, 0.8 * k, alpha=0.8 * a, blur=b + 3)
    ground(cr)
    where = prog(t, tB - 0.1, 0.4)
    announce = keyed(t, [(tP, 0.0), (tC, 1.0)], 0.3, 1.5)
    dasha(cr, t, 300, 0.74, front=(-0.6 - 1.4 * announce, -0.8 + 0.5 * announce), hits=[(tC, 0.8)], alpha=a, blur=b,
          ph=0.4)
    rama(cr, t, 720, 0.74, flip=True, front=(-0.4, -0.6), head=0.05, alpha=a, blur=b, ph=1.3)
    cq = back(clamp((t - tC) / 0.45), 1.3)
    if cq > 0:
        cy = 760 - 300 * (1 - cq)
        glow(cr, 720, cy - 100, 260, 0.6 * clamp(cq) * (1 - 0.5 * where))
        prop(cr, "kk_crown", 720, cy, 0.7, rot=sway(t, 0.03, 0.5), alpha=clamp(cq * 2) * (1 - 0.4 * where))
    drums(cr, t, tC, alpha=a)
    if where > 0:                                      # Bharata is not here: a faint, far shadow and a "?"
        bharata(cr, t, 960, 0.9, flip=True, alpha=0.32 * where, blur=18, rods=False, ph=2.0, feet=FEET + 80)
    fl = 0.3 * math.exp(-4 * max(0, t - tC)) * (t > tC)

    def ui(cr):
        if t < tB:
            head2(cr, t, "DASHARATHA FIXED RAMA'S", tP + 0.05, "CORONATION", tC, big_size=190)
        else:
            head2(cr, t, "BUT AT THAT TIME,", tB, "WHERE WAS BHARATA?", tB + 0.06, big_size=170)
            q = back(clamp((t - tB - 0.25) / 0.3), 1.6)
            if q > 0:
                cr.save()
                cr.translate(950, 980)
                cr.rotate(0.1 + 0.04 * math.sin(t * 3))
                cr.scale(q, q)
                draw_text(cr, "?", 0, 0, 260, RED, clamp(q), anchor="cm")
                cr.restore()
    return dict(ui=ui, flash=fl)


# ------------------------------------------------------------------ k6  Bharata far away; "now is the time"


MAP = (540, 1250, 0.92)
CITY_K, CITY_A = (-270, -40), (260, 200)


def map_xy(p):
    return MAP[0] + p[0] * MAP[2], MAP[1] + p[1] * MAP[2]


def quote_note(cr, t, t_in, x, y, s, t_mark=None, alpha=1.0):
    """Dasharatha's words on a torn note (2.4.25)."""
    p = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(p) * alpha
    if a <= 0.01:
        return None
    yy = y + 70 * (1 - p)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(-0.025)
    cr.scale(s, s)
    pc.paint_part(cr, "rv_note", a)
    draw_text(cr, "DASHARATHA, TO RAMA:", 0, -170, 40, INK, a, MONO_FONT, "ct", tracking=5)
    l1, l2 = "WHILE BHARATA IS AWAY,", "NOW IS THE TIME."
    sz1 = min(78, int(78 * 680 / text_size(l1, 78)[0]))
    draw_text(cr, l1, 0, -60, sz1, INK, a, anchor="cm")
    q2 = prog(t, t_in + 0.35, 0.3)
    draw_text(cr, l2, 0, 50, 96, RED, a * q2, anchor="cm")
    w2 = text_size(l2, 96)[0]
    if t_mark is not None and t > t_mark:
        q = ease((t - t_mark) / 0.4)
        cr.set_source_rgba(*RED, 0.9 * a)
        cr.set_line_width(12)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(-w2 / 2 - 10, 116)
        cr.curve_to(-w2 / 4, 106, w2 / 4, 124, -w2 / 2 - 10 + (w2 + 20) * q, 110)
        cr.stroke()
    cr.restore()
    return yy


def s_map(cr, t, tl, t0, t1):
    c = cues(tl, "k6")
    tM, tK, tD, tW, tT = c["M"], c["K"], c["D"], c["W"], c["T"]
    mx, my, ms = MAP
    b, k, a = depth(t, t0, 0.45)
    prop(cr, "kk_map", mx, my, ms * k, rot=sway(t, 0.004, 0.25), alpha=a, blur=b)
    pc.rod(cr, mx - 380, my - 300 * ms, 300, H + 60, alpha=0.5 * a)
    pc.rod(cr, mx + 380, my - 300 * ms, 780, H + 60, alpha=0.5 * a)
    ax, ay = map_xy(CITY_A)
    kx, ky = map_xy(CITY_K)
    prop(cr, "kk_cityA", ax, ay, 0.8 * k, alpha=a)
    qk = back(clamp((t - tK + 0.15) / 0.35), 1.4)
    if qk > 0:
        prop(cr, "kk_cityK", kx, ky, 0.8 * qk, alpha=clamp(qk * 2))
    pts = [(ax - 40 + (kx + 60 - ax + 40) * u, ay - 60 + (ky - 30 - ay + 60) * u - 120 * math.sin(math.pi * u))
           for u in [i / 40 for i in range(41)]]
    dotted(cr, pts, prog(t, tK, 0.9), 26, 6.5)
    qb = back(clamp((t - tM) / 0.35), 1.5)             # Bharata, small, at his uncle's home
    if qb > 0:
        bharata(cr, t, kx + 92, 0.27 * qb, flip=True, feet=ky + 6, rods=False, ph=2.0)
    if t > tD - 0.2:                                   # Dasharatha, small, at Ayodhya, speaking
        q = back(clamp((t - tD + 0.2) / 0.35), 1.5)
        dp = dasha(cr, t, ax + 110, 0.27 * q, flip=True, feet=ay + 6, rods=False, front=(-1.4, -0.5), ph=0.7)
        if t > tD:
            sound_rings(cr, dp["head"][0] - 20, dp["head"][1], t, tD, 3, 0.3, 90, alpha=0.7)

    def ui(cr):
        if t < tD:
            head2(cr, t, "BHARATA WAS AT HIS UNCLE'S HOME, IN", t0 + 0.05, "KEKAYA", tK, big_size=200)
            tag(cr, t, t0 + 0.3, "AYODHYA", ax, ay + 72, 34)
            tag(cr, t, tK + 0.1, "KEKAYA", kx, ky + 72, 34)
            if t > tK + 0.6:
                stamp(cr, t, tK + 0.6, "FAR AWAY", 610, 1330, 46, rot=-0.12)
        else:
            small_line(cr, t, [(w, tD + 0.08 * i) for i, w in enumerate("AND DASHARATHA HIMSELF SAID:".split())],
                       245, 62)
            yy = quote_note(cr, t, tW - 0.3, 540, 600, 0.8, t_mark=tT)
            if yy is not None:
                leaf_tag(cr, t, tW + 0.25, 780, yy + 268, 0.8, EV_2425, rot=0.04, rod=False)
    return dict(ui=ui)


# ------------------------------------------------------------------ k7  the invitation list


ROWS = (("OTHER KINGS", "tick"), ("KEKAYA KING", "cross"), ("JANAKA", "cross"))


def invite_list(cr, t, x, y, s, row_t, mark_t, alpha=1.0):
    """The scroll; row_t = when each name starts being written, mark_t = when its tick / cross is drawn."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(sway(t, 0.006, 0.3))
    cr.scale(s, s)
    pc.paint_part(cr, "kk_scroll", alpha)
    draw_text(cr, "CORONATION GUESTS", 0, -318, 44, INK, alpha, MONO_FONT, "cm", tracking=6)
    quill = None
    for i, ((name, mark), tw, tm) in enumerate(zip(ROWS, row_t, mark_t)):
        if t < tw:
            continue
        ry = -170 + 150 * i
        q = clamp((t - tw) / 0.55)
        w, _ = text_size(name, 78)
        cr.set_source_rgba(*INK, 0.9 * alpha)
        cr.set_line_width(6)
        cr.rectangle(-290, ry - 34, 68, 68)
        cr.stroke()
        cr.save()
        cr.rectangle(-200, ry - 70, (w + 20) * q, 140)
        cr.clip()
        faded = mark == "cross" and t > tm
        draw_text(cr, name, -190, ry, 78, FADE if faded else INK, alpha, anchor="lm")
        cr.restore()
        if q < 1:
            quill = (-190 + w * q, ry + 26)
        if t > tm:
            p = prog(t, tm, 0.3)
            if mark == "tick":
                tick(cr, -282, ry - 4, 70, p, RED, alpha)
            else:
                cross(cr, -256, ry, 60, p, RED, alpha)
    if quill is not None:
        prop(cr, "kk_quill", quill[0], quill[1], 0.6, rot=0.1 * math.sin(t * 25), alpha=alpha)
    cr.restore()


def s_invite(cr, t, tl, t0, t1):
    c = cues(tl, "k7")
    tK, tJ, tL = c["K"], c["J"], c["L"]
    row_t = (t0 + 0.05, tK - 0.45, tJ - 0.4)
    mark_t = (t0 + 0.65, tK + 0.15, tJ + 0.2)
    t_up = max(tL - 0.45, tJ + 0.3)                     # the list moves up first, then the scale comes in
    up = keyed(t, [(t0, 0.0), (t_up, 1.0)], 0.4, 1.2)
    sx, sy, ss = 620 - 80 * up, 940 - 195 * up, 0.88 - 0.36 * up
    # Dasharatha dictates the list, then steps away when the scale comes back
    ground(cr)
    if t < t_up + 0.5:
        b, k, a = depth(t, t0, 0.45, t_out=t_up, out_dur=0.4)
        point = keyed(t, [(t0, 0.3), (tK - 0.2, 1.0)], 0.3, 1.4)
        dp = dasha(cr, t, 165, 0.66 * k, front=(-0.6 - 1.0 * point, -0.6 + 0.2 * point), hits=[(tK, 0.6), (tJ, 0.6)],
                   alpha=a, blur=b, ph=0.6)
        if tK < t < tL:
            sound_rings(cr, dp["head"][0] + 50, dp["head"][1] + 10, t, tK - 0.3, 4, 0.5, 110, alpha=0.6 * a)
    invite_list(cr, t, sx, sy, ss, row_t, mark_t)
    land = tL + 0.55
    bs = 0.8
    pans = None
    if t > t_up + 0.35:
        b, k, a = depth(t, t_up + 0.35, 0.45)
        tilt = lambda tt: settle(tt, [(t0 - 9, TILT_K6), (land, TILT_K7)], 0.85, 1.8)
        pans = balance(cr, t, 540, FEET, bs * k, tilt, left=for_items(t_2146=None if t >= land else False),
                       alpha=a, blur=b)
    lx, ly = sx + 170 * ss, sy + 300 * ss

    def ui(cr):
        if t < tL:
            head2(cr, t, "IN A HURRY, DASHARATHA", t0 + 0.05, "DIDN'T INVITE", tK, big_size=180)
            leaf_tag(cr, t, tJ + 0.25, lx, ly, 0.62, EV_2146, rot=0.06, rod=False)
        else:
            head2(cr, t, "THEY'LL HEAR IT LATER,", tL, "HE THOUGHT", tL + 0.06, big_size=180)
            u = clamp((t - tL) / 0.55)                 # the leaf flies from the list into the FOR pan
            if u < 1 and pans is not None:
                ex, ey = pan_xy(pans[0], bs, 48, D - 82)
                leaf_tag(cr, t, None, lx + (ex - lx) * ease(u), ly + (ey - ly) * ease(u) - 160 * math.sin(math.pi * u),
                         0.62 - 0.28 * ease(u), EV_2146, rot=0.06 - 0.1 * u, rod=False)
    return dict(ui=ui, flash=0.2 * math.exp(-4 * max(0, t - land)) * (t > land))


# ------------------------------------------------------------------ k8 / k9  re-hook: the hard swing, then WAIT


SC = (540, FEET, 1.0)                   # the scale in the debate shots


def s_rehook(cr, t, tl, t0, t1):
    tH = cues(tl, "k8")["H"]
    tilt = lambda tt: settle(tt, [(t0 - 9, TILT_K7), (t0 + 0.1, TILT_K8 + 0.12), (t0 + 0.9, TILT_K8)], 0.9, 1.6)
    ground(cr)
    pans = balance(cr, t, *SC, tilt, left=for_items())
    rx, ry = pan_xy(pans[0], SC[2], 0, D - 20)
    glow(cr, rx, ry, 330, 0.45 * prog(t, t0 + 0.2, 0.4))

    def ui(cr):
        head2(cr, t, "SO WAS SHE", t0 + 0.05, "RIGHT?", tH, big_size=240)
        red_ring(cr, rx, ry, 190, 150, prog(t, tH + 0.35, 0.45), 9)
    return dict(ui=ui, night=0.25 + 0.15 * prog(t, t0, 0.5), flash=0.3 * math.exp(-5 * max(0, t - tH)) * (t > tH))


def s_wait(cr, t, tl, t0, t1):
    tO = cues(tl, "k9")["O"]
    sh = 14 * math.exp(-9 * max(0, t - t0 - 0.05)) * math.sin(60 * (t - t0))
    cr.translate(sh, 0.6 * sh)
    tilt = lambda tt: settle(tt, [(t0 - 9, TILT_K8)], 0.9, 1.6)
    ground(cr)
    lit = prog(t, tO, 0.35)
    balance(cr, t, *SC, tilt, left=for_items(), lit=lit, for_lit=1 - 0.4 * lit)

    def ui(cr):
        if t < tO:
            big_word(cr, t, "WAIT.", t0 + 0.02, 300, 280, color=INK)
        else:
            head2(cr, t, "NOW, THE", tO, "OTHER SIDE", tO + 0.06, big_size=220)
    return dict(ui=ui, night=0.3 * (1 - prog(t, tO, 0.5)), flash=0.45 * math.exp(-6 * max(0, t - t0)) +
                0.3 * math.exp(-4 * max(0, t - tO)) * (t > tO))


# ------------------------------------------------------------------ k10  the other side: 14 years


def s_exile(cr, t, tl, t0, t1):
    c = cues(tl, "k10")
    tB, tA, tF, tE, tW = c["B"], c["A"], c["F"], c["E"], c["W"]
    land = tF + 0.2
    tilt = lambda tt: settle(tt, [(t0 - 9, TILT_K8), (land, TILT_K10)], 0.8, 1.5)
    ground(cr)
    right = [dict(kind="card", t=land, lines=("14 YEARS", "IN THE FOREST"))]
    pans = balance(cr, t, *SC, tilt, left=for_items(), right=right, lit=1.0 - 0.3 * prog(t, tW, 0.5), for_lit=0.6)
    gx, gy = pan_xy(pans[0], SC[2], CROWN_IN_PAN[0], CROWN_IN_PAN[1] - 60)
    if tB < t < land:
        glow(cr, gx, gy, 200, 0.5 * prog(t, tB, 0.3))

    def ui(cr):
        if t < tF:
            head2(cr, t, "SHE ASKED THE THRONE FOR", t0 + 0.05, "BHARATA", tB, big_size=200)
            if t > tA:
                red_ring(cr, gx, gy, 100, 90, prog(t, tA, 0.4), 8)
        else:
            head2(cr, t, "BUT ALSO, FOR RAMA:", tF, "EXILE", tE, big_size=230)
        stamp2(cr, t, tW, ["NOT IN THE", "WEDDING PROMISE"], 560, 700, 50, rot=-0.06)
    return dict(ui=ui, flash=0.35 * math.exp(-4 * max(0, t - land)) * (t > land))


# ------------------------------------------------------------------ k11  Dasharatha's death, gently


def s_death(cr, t, tl, t0, t1):
    c = cues(tl, "k11")
    tG, tX = c["G"], c["X"]
    prop(cr, "kk_throne", 640, FEET + 10, 0.74, alpha=0.75, blur=6)
    ground(cr)
    s, x = 0.84, 450
    bow = keyed(t, [(t0, 0.15), (tG, 0.5), (tX - 0.2, 0.85)], 0.6, 1.1)
    slip = clamp((t - tX) / 0.25)
    fall = clamp((t - tX - 0.25) / 0.4)
    fade = ease((t - tX - 0.45) / 0.65) if t > tX + 0.45 else 0.0

    def crown_fn(cr_):
        """The crown in head coordinates: it slips back, then falls straight down (screen down) to the floor and lies
        on its side; it keeps its own full alpha while the king fades."""
        m = cr_.get_matrix()
        sc = math.hypot(m.xx, m.yx)
        ang = math.atan2(m.yx, m.xx)
        cr_.save()
        cr_.translate(-40 * ease(slip), 30 * slip ** 2)
        if fall > 0:
            _, cy_dev = cr_.user_to_device(0, -250)
            drop = max(0.0, (FEET - 70 - cy_dev) / sc) * fall ** 2
            cr_.translate(math.sin(ang) * drop - 80 * fall, math.cos(ang) * drop)
        cr_.translate(0, -250)
        cr_.rotate(-0.35 * ease(slip) - 1.15 * ease(fall * 1.3) - ang * fall)
        cr_.translate(0, 250)
        pc.paint_part(cr_, "ds_crown")
        cr_.restore()

    glow(cr, x, 1100, 360, 0.4 * (1 - fade))
    dasha(cr, t, x, s, front=(-0.2 - 0.3 * bow, -0.9), backa=(0.1, -0.3), head=0.12 + 0.35 * bow, rot=0.05 * bow,
          alpha=1 - fade, blur=10 * fade, rods=fade < 0.5, swap={"dasharatha_head": "dasharatha_head_bare"},
          extra={"dasharatha_head": crown_fn}, ph=0.4)

    def ui(cr):
        head2(cr, t, "IN GRIEF FOR HIS SON, KING DASHARATHA", t0 + 0.05, "PASSED AWAY", tX, big_size=180,
              big_color=INK)
    return dict(ui=ui, night=0.12 + 0.4 * prog(t, tG, 1.2))


# ------------------------------------------------------------------ k12  Bharata refuses the throne


def s_refuse(cr, t, tl, t0, t1):
    c = cues(tl, "k12")
    tM, tR, tN = c["M"], c["R"], c["N"]
    prop(cr, "arch", 540, FEET + 10, 0.8, alpha=0.7, blur=5)
    ground(cr)
    offer = keyed(t, [(t0, 0.3), (tM - 0.1, 1.0), (tN + 0.1, 0.2)], 0.35, 1.3)
    sad = prog(t, tR + 0.2, 0.6)
    kp = kai(cr, t, 800, 0.76, flip=True, front=(-0.3 - 1.1 * offer, -0.6 + 0.4 * offer), head=0.12 * sad,
             hits=[(tN, 0.8)], ph=1.2)
    hx, hy = kp["handF"]
    fly = clamp((t - tN - 0.1) / 0.6)
    if fly <= 0:
        prop(cr, "kk_crown", hx - 10, hy - 6, 0.5, rot=sway(t, 0.03, 0.6))
    else:                                               # pushed away: it tumbles down and lies on its side
        cx = hx - 10 + (660 - hx + 10) * fly
        cy = hy - 6 + (FEET - 64 - hy + 6) * fly ** 2 - 140 * math.sin(math.pi * fly) * (1 - fly)
        prop(cr, "kk_crown", cx, cy, 0.5, rot=-math.pi / 2 * ease(fly) + 0.7 * math.sin(math.pi * fly))
    walk_end = min(t0 + 1.0, tM)
    if t < walk_end:
        walk(cr, t, bharata, t0, walk_end, -150, 330, 0.74, t_in=t0, ph=2.0)
    elif t < tN - 0.05:
        if t > tR:                                      # turned away from his mother, a hand to his brow
            bharata(cr, t, 300, 0.74, flip=True, front=(-2.4, -2.1), backa=(0.15, -0.2), head=0.14,
                    hits=[(tR, 1.0)], ph=2.0)
        else:
            bharata(cr, t, 330, 0.74, front=(-0.5, -0.6), hits=[(walk_end, 0.6)], ph=2.0)
    else:                                               # turns back and pushes the crown away
        push = keyed(t, [(tN - 0.05, 0.0), (tN + 0.05, 1.0)], 0.25, 1.4)
        bharata(cr, t, 330 + 40 * push, 0.74, front=(-0.6 - 0.9 * push, -0.8 + 0.7 * push), backa=(0.3, -0.3),
                hits=[(tN + 0.1, 0.8)], ph=2.0)

    def ui(cr):
        if t < tR:
            head2(cr, t, "THEN BHARATA", t0 + 0.05, "RETURNED", t0 + 0.2, big_size=200)
        elif t < tN:
            head2(cr, t, "AND BLAMED", tR, "HIS OWN MOTHER", tR + 0.06, big_size=190)
        else:
            head2(cr, t, "AND HE", tN, "REFUSED THE THRONE", tN + 0.06, big_size=170, under=tN + 0.5)
    return dict(ui=ui, flash=0.25 * math.exp(-5 * max(0, t - tN)) * (t > tN))


# ------------------------------------------------------------------ k13  the forest: the kingdom is yours


def s_forest(cr, t, tl, t0, t1):
    c = cues(tl, "k13")
    tO, tY, tP, tS = c["O"], c["Y"], c["P"], c["S"]
    close = keyed(t, [(t0, 0.0), (tS - 0.1, 1.0)], 0.5, 1.2)
    prop(cr, "tree", 1000, FEET + 10, 0.62, rot=sway(t, 0.006, 0.3), alpha=0.7, blur=6)
    prop(cr, "tree", -220 + 260 * close, FEET + 10, 0.66, rot=sway(t, 0.006, 0.3, 1), alpha=0.85, blur=3,
         flip=True)
    if close > 0:
        prop(cr, "tree", 470, FEET + 10, 0.5, alpha=0.55 * clamp(close), blur=10)
    ground(cr)
    talk = keyed(t, [(t0, 0.3), (tO, 1.0), (tP, 0.5), (tS, 1.2)], 0.35, 1.4)
    rx = 320 - 70 * close
    rp = rama(cr, t, rx, 0.76, front=(-0.6 - 0.8 * talk, -0.7 + 0.3 * talk), hits=[(tO, 0.6), (tY, 0.6)], ph=0.5)
    if tO < t < tP:
        sound_rings(cr, rp["head"][0] + 70, rp["head"][1] + 20, t, tO, 4, 0.32, 140, alpha=0.7)
    if t > tS:
        glow(cr, rx, 1150, 330, 0.4 * prog(t, tS, 0.5))
    bp = bharata(cr, t, 800, 0.72, flip=True, kneel="bharata_kneel", head=0.1, ph=2.0, **ANJALI)
    yq = prog(t, tY, 0.4) * (1 - prog(t, tP + 0.3, 0.4))
    if yq > 0:
        tx, ty = bp["top"]
        glow(cr, tx, ty - 80, 200, 0.5 * yq)
        prop(cr, "kk_crown", tx + 6, ty - 30 - 30 * (1 - yq), 0.42, rot=sway(t, 0.03, 0.6), alpha=yq)

    def ui(cr):
        if t < tP:
            head2(cr, t, "RAMA REMINDED HIM OF", t0 + 0.05, "THE OLD PROMISE", tO, big_size=180)
            leaf_tag(cr, t, tO + 0.2, 540, 610, 0.95, EV_1073, rot=-0.04, t_out=tY - 0.1)
            card(cr, t, tY, 560, 700, 0.82, [("THE KINGDOM", 80, INK, -34), ("IS YOURS", 100, RED, 50)],
                 t_out=tP - 0.1)
        elif t < tS:
            head2(cr, t, "BUT TO KEEP HIS", tP, "FATHER'S WORD", tP + 0.06, big_size=190)
        else:
            head2(cr, t, "RAMA STAYED IN THE", tS, "FOREST", tS + 0.06, big_size=220)
    return dict(ui=ui, flash=0.25 * math.exp(-4 * max(0, t - tY)) * (t > tY))


# ------------------------------------------------------------------ k14  the sandals on the throne


YEARS_DUR = 1.8


def years_at(t, tF):
    return 1 + int(13 * ease((t - tF) / YEARS_DUR)) if t > tF else 1


def s_padukas(cr, t, tl, t0, t1):
    c = cues(tl, "k14")
    tP, tT, tF, tN = c["P"], c["T"], c["F"], c["N"]
    thx = 660
    glow(cr, thx, 1330, 380, 0.3 + 0.35 * prog(t, tT + 0.4, 0.5))
    prop(cr, "kk_throne", thx, FEET + 10, 0.78)
    ground(cr)
    seat_y = FEET + 10 - 252 * 0.78
    walk_end = min(t0 + 1.1, tT - 0.1)
    carry = dict(front=(-2.5, -1.2), backa=(-2.4, -1.2))       # both hands up, holding the sandals on his head
    if t < walk_end:
        bp = walk(cr, t, bharata, t0, walk_end, -150, 250, 0.74, t_in=t0, ph=2.0, **carry)
    elif t < tN:
        lift = keyed(t, [(walk_end, 1.0), (tT + 0.1, 0.0)], 0.4, 1.2)
        bp = bharata(cr, t, 250, 0.74, front=(-0.6 - 1.9 * lift, -0.7 - 0.5 * lift),
                     backa=(0.2 - 2.6 * lift, -0.3 - 0.9 * lift), hits=[(tT, 0.6)], ph=2.0)
    else:
        q = prog(t, tN, 0.5)
        bp = bharata(cr, t, 230, 0.74, kneel="bharata_kneel", head=0.32 * q, rot=0.18 * q, ph=2.0, **ANJALI)
    u = clamp((t - tT) / 0.6)                           # the sandals: on his head, then set on the throne
    tx, ty = bp["top"]
    if u <= 0:
        prop(cr, "kk_paduka", tx + 10, ty + 40, 0.5, rot=sway(t, 0.02, 0.6))
    else:
        sx0, sy0 = 260, FEET - 434 * 0.74 - 594 * 0.74 + 40
        px = sx0 + (thx - sx0) * ease(u)
        py = sy0 + (seat_y - sy0) * ease(u) - 180 * math.sin(math.pi * u)
        if u >= 1:
            glow(cr, thx, seat_y - 90, 260, 0.55 * (0.85 + 0.15 * math.sin(t * 3)))
        prop(cr, "kk_paduka", px, py, 0.5 + 0.36 * ease(u))
    n = years_at(t, tF)

    def ui(cr):
        if t < tF:
            head2(cr, t, "ON THE EMPTY THRONE,", t0 + 0.05, "RAMA'S SANDALS", tP, big_size=180)
        else:
            head2(cr, t, "BHARATA RULED IN RAMA'S NAME FOR", tF, f"{n} YEAR" + ("S" if n > 1 else ""), tF + 0.05,
                  big_size=220, under=tF + YEARS_DUR + 0.1)
    return dict(ui=ui, flash=0.3 * math.exp(-4 * max(0, t - tT - 0.6)) * (t > tT + 0.6))


def year_ticks(tl):
    tF = cues(tl, "k14")["F"]
    out, prev = [], 1
    for i in range(1, 400):
        tt = tF + i * 0.01
        n = years_at(tt, tF)
        if n != prev:
            out.append(tt)
            prev = n
        if n >= 14:
            break
    return out


# ------------------------------------------------------------------ k15  who was wrong?


def _fig_kai(cr, t, y, a):
    kai(cr, t, 0, 0.27, rods=False, alpha=a, y=y - 470 * 0.27, front=(-0.3, -0.6), ph=1.0)


def _fig_ds(cr, t, y, a):
    dasha(cr, t, 0, 0.27, rods=False, alpha=a, y=y - 434 * 0.27, flip=True, front=(-0.4, -0.6), ph=0.3)


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "k15")
    tK, tD = c["K"], c["D"]
    tilt = lambda tt: settle(tt, [(t0 - 9, TILT_K10), (t0 + 0.2, 0.0)], 0.7, 1.4)
    ground(cr)
    left = [dict(kind="fig", t=t0 + 0.3, fn=_fig_kai)]
    right = [dict(kind="fig", t=t0 + 0.45, fn=_fig_ds)]
    balance(cr, t, 540, FEET, 0.92, tilt, left=left, right=right, labels=0.0)
    cards = ((300, "KAIKEYI?", tK), (780, "DASHARATHA?", tD))      # the plaques are 426 px wide at cs = 0.56

    def ui(cr):
        head2(cr, t, "SO WHO WAS", t0 + 0.05, "WRONG?", t0 + 0.2, big_size=240)
        cs = 0.56
        size = min(96, *[int(96 * 370 / text_size(txt, 96)[0]) for _, txt, _ in cards])
        for cx, txt, tc in cards:
            card(cr, t, tc - 0.25, cx, 740, cs, [(txt, int(size / cs), RED, 4)])
        if t > tK:
            if t < tD:
                k, ts = 0, tK
            else:
                n = int((t - tD) / 0.9)
                k, ts = (1 if n % 2 == 0 else 0), tD + 0.9 * n
            red_ring(cr, cards[k][0], 744, 236, 92, prog(t, ts, 0.35), 9)
    return dict(ui=ui)


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("k1", None, s_hook, {"z": (1.0, 1.04)}),
    ("k2", None, s_rama, {}),
    ("k3", None, s_wedding, {}),
    ("k4", None, s_price, {"z": (1.0, 1.03)}),
    ("k5", None, s_years, {}),
    ("k6", None, s_map, {"z": (1.0, 1.03)}),
    ("k7", None, s_invite, {"z": (1.0, 1.03)}),
    ("k8", None, s_rehook, {"z": (1.0, 1.1)}),
    ("k9", None, s_wait, {"z": (1.1, 1.06)}),
    ("k10", None, s_exile, {"z": (1.0, 1.04)}),
    ("k11", None, s_death, {"z": (1.0, 1.06)}),
    ("k12", None, s_refuse, {}),
    ("k13", None, s_forest, {}),
    ("k14", None, s_padukas, {"z": (1.0, 1.04)}),
    ("k15", None, s_end, {"z": (1.0, 1.03)}),
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
    cr.restore()
    motes(cr, t)
    pc.lamp(cr, t, night=out.get("night", 0.0), flash=out.get("flash", 0.0))
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur): the Jarasandha / Ravana vocabulary: a whoosh on every cut, damaru on hits, conch on the big
    reveals, bell on sacred beats and the end, shimmer on the crown and blessings, creak when the scale swings, ticks
    for the counters, scribble for the writing, pops as things land. The death of Dasharatha gets only a soft bell."""
    st = starts(tl, SHOTS)
    ev = [(s, "whoosh", 0.45) for s in st[1:]]
    c = {b: cues(tl, b) for b in CUES}
    # k1
    k = c["k1"]
    ev += [(0.0, "damaru", 0), (0.05, "bell", 0), (0.4, "pop", 0)]
    ev += [(HAND_T0 + h[4], "pop", 0) for h in HANDS]
    ev += [(k["V"] - 0.3, "dip", 0.35), (k["V"], "slam", 0), (k["V"] + 0.02, "hit", 0), (k["A"] - 0.1, "whoosh", 0.5),
           (k["A"] + 0.1, "shimmer", 0), (k["A"] + 0.45, "pop", 0), (k["S"], "whoosh", 0.6), (k["S"] + 0.3, "damaru", 0), (k["S"] + 0.6, "pop", 0)]
    # k2
    k = c["k2"]
    w_end = min(k["t0"] + 1.0, k["R"] - 0.2)
    ev += [(k["t0"] + 0.1 + 0.33 * i, "step", 0) for i in range(3) if k["t0"] + 0.1 + 0.33 * i < w_end]
    ev += [(k["R"], "bell", 0), (k["B"], "pop", 0), (k["V"], "conch", 0), (k["V"] + 0.3, "thud", 0),
           (k["K"] + 0.1, "tick", 0)]
    # k3
    k = c["k3"]
    ev += [(k["t0"] + 0.1, "shimmer", 0), (k["W"], "bell", 0), (k["W"] + 0.1, "pop", 0), (k["W"] + 0.2, "pop", 0)]
    ev += [(k["F"] + 0.33 * i, "step", 0) for i in range(3)]
    ev += [(k["K"], "pop", 0), (k["P"] - 0.1, "whoosh", 0.6), (k["P"] + 0.5, "damaru", 0), (k["P"] + 0.55, "tick", 0)]
    # k4
    k = c["k4"]
    land = k["S"] + 0.05
    ev += [(k["R"] - 0.3, "dip", 0.35), (k["R"], "conch", 0), (k["R"] + 0.05, "shimmer", 0),
           (land - 0.45, "whoosh", 0.45), (land, "thud", 0), (land + 0.05, "creak", 0.9), (land + 0.15, "pop", 0),
           (k["K"], "hit", 0)]
    # k5
    k = c["k5"]
    tP = k["C"] - 0.25
    n = int(max(0, tP - k["t0"] - 0.2) / 0.16)
    ev += [(k["t0"] + 0.15 + 0.16 * i, "tick", 0) for i in range(min(n, 9))]
    ev += [(tP, "whoosh", 0.4), (k["C"], "conch", 0)]
    ev += [(k["C"] + 0.26 * i, "damaru", 0) for i in range(int(max(0, k["B"] - k["C"] - 0.3) / 0.52) + 1)]
    ev += [(k["B"] - 0.3, "dip", 0.4), (k["B"], "sting", 0), (k["B"] + 0.3, "pop", 0)]
    # k6
    k = c["k6"]
    ev += [(k["t0"] + 0.3, "pop", 0), (k["M"], "pop", 0), (k["K"], "pop", 0), (k["K"] + 0.6, "slam", 0),
           (k["D"] - 0.2, "pop", 0), (k["W"] - 0.3, "whoosh", 0.4), (k["W"] + 0.25, "thud", 0),
           (k["T"], "scribble", 0.4), (k["T"] + 0.05, "damaru", 0)]
    # k7
    k = c["k7"]
    land = k["L"] + 0.55
    ev += [(k["t0"] + 0.05, "scribble", 0.55), (k["t0"] + 0.65, "tick", 0), (k["K"] - 0.45, "scribble", 0.55),
           (k["K"] + 0.15, "slam", 0), (k["J"] - 0.4, "scribble", 0.5), (k["J"] + 0.2, "slam", 0),
           (k["J"] + 0.25, "pop", 0), (k["L"] - 0.1, "whoosh", 0.5), (land, "thud", 0), (land + 0.05, "creak", 0.9)]
    # k8: re-hook
    k = c["k8"]
    ev += [(k["t0"] - 0.35, "tick", 0), (k["t0"] - 0.3, "dip", 0.5), (k["t0"] + 0.05, "creak", 1.4),
           (k["t0"] + 0.1, "hit", 0), (k["t0"] + 0.2, "heartbeat", 1.6), (k["H"], "damaru", 0),
           (k["H"] + 0.35, "tick", 0)]
    # k9
    k = c["k9"]
    ev += [(k["t0"], "slam", 0), (k["t0"] + 0.02, "hit", 0), (k["O"], "conch", 0), (k["O"] + 0.05, "shimmer", 0)]
    # k10
    k = c["k10"]
    land = k["F"] + 0.2
    ev += [(k["B"], "pop", 0), (k["A"], "tick", 0), (land - 0.5, "dip", 0.4), (land - 0.4, "whoosh", 0.4),
           (land, "hit", 0), (land + 0.05, "creak", 1.4), (k["E"], "conch", 0), (k["W"], "slam", 0)]
    # k11: gentle, no hits
    k = c["k11"]
    ev += [(k["t0"] - 0.2, "dip", 0.3), (k["G"], "bell", 0), (k["X"] + 0.85, "thud", 0)]
    # k12
    k = c["k12"]
    ev += [(k["t0"] + 0.25 * i, "step", 0) for i in range(4)]
    ev += [(k["M"], "shimmer", 0), (k["R"], "damaru", 0), (k["N"], "hit", 0), (k["N"] + 0.65, "thud", 0)]
    # k13
    k = c["k13"]
    ev += [(k["O"] + 0.2, "pop", 0), (k["Y"], "shimmer", 0), (k["Y"] + 0.05, "pop", 0), (k["P"], "bell", 0),
           (k["S"] - 0.1, "whoosh", 0.6)]
    # k14
    k = c["k14"]
    ev += [(k["t0"] + 0.28 * i, "step", 0) for i in range(4)]
    ev += [(k["T"], "whoosh", 0.5), (k["T"] + 0.6, "bell", 0), (k["T"] + 0.65, "shimmer", 0)]
    ev += [(x, "tick", 0) for x in year_ticks(tl)]
    ev += [(k["N"], "conch", 0)]
    # k15
    k = c["k15"]
    ev += [(k["t0"] + 0.2, "creak", 1.2), (k["t0"] + 0.3, "pop", 0), (k["t0"] + 0.45, "pop", 0),
           (k["K"] - 0.25, "pop", 0), (k["K"], "tick", 0), (k["D"] - 0.25, "pop", 0), (k["D"], "tick", 0),
           (k["D"] + 0.4, "bell", 0)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in ev]
