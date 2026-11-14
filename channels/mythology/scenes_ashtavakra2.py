"""Scenes for videos/ashtavakra2.py, the Ashtavakra remake built on the owner's reference reel (12 Nov 2026; lessons in
myth_out/LESSONS_FROM_REFERENCE_ASHTAVAKRA.md). Same Togalu Gombeyaata shadow-puppet cast and helpers as
scenes_ashtavakra, with these changes:

- Frame 0 is the stake happening: the father large and furious on the left, the boy on the right; at 0.45 s a red
  bolt from the father's finger hits the boy, he folds into his bent body and his eight joints light up red one by
  one. The callback (a15c) is the same framing in gold: the father smiling, the boy straight.
- Short Hindi labels (1-3 words, the word being said) on a parchment strip instead of the English two-tier
  headlines. The reused shots still draw their pictures; their English text calls are switched off in this process.
- A colour for each place (night blue for the curse, red for anger, the court's warm red, blue water, dawn for the
  return) and a closer camera on the reused wide shots (each SHOTS entry's zoom and focus).
- New shots: the hook, the baby listening to the mantras (a3), the mid-story question face to face (a10q), the
  callback and the two-sided question with Hindi cards.

Every frame is a pure function of t. Cues are words of the Hindi lines (CUES); the reused shots read
scenes_ashtavakra.CUES, which this module overrides for its own lines (the two videos never render in one process).
"""
import math

import cairo

import ashtavakra_cast as AV
import puppet_core as pc
import scenes_ashtavakra as A
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import clamp, draw_text, ease, prog
from puppet_core import H, W, depth, keyed, prop
from scenes_arjuna import HAS_INDIC, indic_surface
from scenes_jarasandha import INK, RED, glow, motes, red_ring, sound_rings, stars
from scenes_jayadratha import flash_at, tint, to_user
from scenes_kaikeyi import fig
from scenes_lakshman_rekha import sparkle
from scenes_mandhata import aura, burst, lights, warm
from scenes_ruru import sepia
from scenes_shani_ganesha import bolt, red_glow
from shots import T

G = A.G

# ------------------------------------------------------------------ cues (Hindi words of ashtavakra2's lines)
# (name, word, fraction fallback, ((after, min gap), ...)); "t0" = the line's start.
CUES = {
    "a1": (("E", "आठ", 0.3, (("t0", 0.5),)),
           ("P", "पिता", 0.8, (("E", 0.6),))),
    "a3": (("K", "कहोड़", 0.1, ()),
           ("M", "मंत्र", 0.45, (("K", 0.8),)),
           ("B", "पेट", 0.75, (("M", 0.6),)),
           ("S", "सुनता", 0.9, (("B", 0.4),))),
    "a4": (("B", "पेट", 0.2, (("t0", 0.3),)),
           ("V", "आवाज़", 0.3, (("B", 0.3),)),
           ("F", "पिताजी", 0.5, (("V", 0.5),)),
           ("Mt", "मंत्र", 0.7, (("F", 0.3),)),
           ("W", "गलत", 0.82, (("Mt", 0.3),))),
    "a6": (("Sk", "अपमान", 0.15, (("t0", 0.3),)),
           ("Gu", "ग़ुस्से", 0.3, (("Sk", 0.4),)),
           ("C", "जा", 0.5, (("Sk", 0.3),)),
           ("Y", "तेरा", 0.55, (("C", 0.2),)),
           ("Bd", "तेरा", 0.6, (("Y", 0.0),)),
           ("B", "शरीर", 0.65, (("C", 0.3),)),
           ("E", "आठ", 0.75, (("B", 0.3),)),
           ("K", "होगा", 0.92, (("E", 0.4),))),
    "a8": (("Py", "पैसे", 0.15, (("t0", 0.2),)),
           ("F", "पिता", 0.45, (("Py", 0.5),)),
           ("K", "राजा", 0.75, (("F", 0.3),)),
           ("P", "महल", 0.85, (("K", 0.3),)),
           ("Gh", "गए", 0.97, (("P", 0.4),)),
           ("Pd", "गए", 0.99, (("Gh", 0.2),))),
    "a9": (("Gp", "घमंडी", 0.15, (("t0", 0.2),)),
           ("Kh", "नियम", 0.4, (("Gp", 0.6),)),
           ("Q", "बहस", 0.55, (("Kh", 0.3),)),
           ("L", "हारे", 0.65, (("Q", 0.3),)),
           ("W", "पानी", 0.8, (("L", 0.4),)),
           ("Dr", "डुबो", 0.9, (("W", 0.3),))),
    "a10": (("L", "हार", 0.3, (("t0", 0.3),)),
            ("W", "पानी", 0.6, (("L", 0.9),)),
            ("D", "डुबो", 0.8, (("W", 0.3),))),
    "a7": (("Bn", "पैदा", 0.25, (("t0", 0.4),)),
           ("E", "टेढ़ा", 0.45, (("Bn", 0.4),)),
           ("N", "नाम", 0.65, (("E", 0.5),)),
           ("A", "अष्टावक्र", 0.85, (("N", 0.4),)),
           ("Mt", "अष्टावक्र", 0.95, (("A", 0.9),))),
    "a11": (("Y", "बारह", 0.03, ()),
            ("A", "माँ", 0.45, (("t0", 0.6),)),
            ("Mn", "माँ", 0.45, (("t0", 0.6),)),
            ("T", "सच", 0.75, (("A", 0.4),)),
            ("Bd", "दिया", 0.97, (("T", 0.3),)),
            ("P", "दिया", 0.99, (("Bd", 0.3),))),
    "a12": (("Pc", "महल", 0.05, (("t0", 0.1),)),
            ("S", "रोका", 0.25, (("Pc", 0.4),)),
            ("N", "बच्चे", 0.35, (("S", 0.3),)),
            ("A", "बोला", 0.6, (("N", 0.8),)),
            ("G", "उम्र", 0.72, (("A", 0.4),)),
            ("K", "अक्ल", 0.88, (("G", 0.8),))),
    "a10q": (("P", "पंडित", 0.15, (("t0", 0.3),)),
             ("D", "डुबोया", 0.45, (("P", 0.5),)),
             ("Q", "क्या", 0.6, (("D", 0.5),)),
             ("H", "हरा", 0.85, (("Q", 0.6),))),
    "a13": (("Ch", "बहस", 0.05, (("t0", 0.1),)),
            ("Q", "बहस", 0.1, (("Ch", 0.2),)),
            ("Pd", "पंडित", 0.75, (("Q", 0.8),)),
            ("Wn", "हरा", 0.88, (("Pd", 0.3),))),
    "a14": (("S", "खोला", 0.15, (("t0", 0.4),)),
            ("Dv", "देवता", 0.35, (("S", 0.4),)),
            ("M", "मरे", 0.6, (("Dv", 0.6),)),
            ("D", "मरे", 0.62, (("M", 0.0),)),
            ("Z", "पूजा", 0.88, (("D", 0.5),))),
    "a15": (("W", "पूरी", 0.12, (("t0", 0.3),)),
            ("L", "लौट", 0.3, (("W", 0.6),)),
            ("N", "नदी", 0.55, (("L", 1.2),)),
            ("S", "सीधा", 0.92, (("N", 1.6),))),
    "a15c": (("P", "सज़ा", 0.3, (("t0", 0.5),)),
             ("U", "उसी", 0.6, (("P", 0.8),)),
             ("V", "वापस", 0.85, (("U", 0.6),))),
    "a16": (("Q", "गलत", 0.15, (("t0", 0.2),)),
            ("S", "बेटा", 0.55, (("Q", 0.5),)),
            ("F", "पिता", 0.85, (("S", 0.6),))),
}


def _hi(entry):
    """This module's (name, word, frac, cons) -> scenes_ashtavakra's (name, {"hi": word, "kn": word}, frac, cons)."""
    return tuple((n, {"hi": w, "kn": w}, f, c) for n, w, f, c in entry)


A.CUES.update({bid: _hi(e) for bid, e in CUES.items()})
cues = A.cues


# The reused shots' English text, switched off (their pictures, rings, discs and bursts stay).
def _off(*_a, **_k):
    return None


for _name in ("head2", "tag", "plate", "card", "card2", "counter_badge", "rule_card", "script_strip", "voice_cloud",
              "cloud_text"):
    setattr(A, _name, _off)
_draw_text = A.draw_text
A.draw_text = lambda cr, text, *a, **k: None if text == "+" else _draw_text(cr, text, *a, **k)   # a7's plaque sum


# ------------------------------------------------------------------ Hindi labels


PARCH = (0.97, 0.87, 0.62)


def label(cr, t, t_in, text, x=540, y=330, size=84, col=INK, t_out=None, under=False):
    """A short Hindi label on a parchment strip (the word the voice is saying); rises in, fades out at t_out."""
    if not HAS_INDIC or t < t_in:
        return
    q = prog(t, t_in, 0.28)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.22)
    if q <= 0.01:
        return
    su = indic_surface(text, size, col)
    w_, h_ = su.get_width(), su.get_height()
    yy = y + 22 * (1 - ease(q))
    pad = 0.36 * size
    cr.save()
    cr.translate(x, yy)
    s = 0.92 + 0.08 * ease(q)
    cr.scale(s, s)
    pc.poly(cr, [(-w_ / 2 - pad, -h_ / 2 - 16), (w_ / 2 + pad, -h_ / 2 - 16), (w_ / 2 + pad + 14, 0),
                 (w_ / 2 + pad, h_ / 2 + 16), (-w_ / 2 - pad, h_ / 2 + 16), (-w_ / 2 - pad - 14, 0)])
    cr.set_source_rgba(0.0, 0.0, 0.0, 0.28 * q)
    cr.save()
    cr.translate(6, 8)
    cr.fill_preserve()
    cr.restore()
    cr.new_path()
    pc.poly(cr, [(-w_ / 2 - pad, -h_ / 2 - 16), (w_ / 2 + pad, -h_ / 2 - 16), (w_ / 2 + pad + 14, 0),
                 (w_ / 2 + pad, h_ / 2 + 16), (-w_ / 2 - pad, h_ / 2 + 16), (-w_ / 2 - pad - 14, 0)])
    cr.set_source_rgba(*PARCH, 0.97 * q)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, q)
    cr.set_line_width(4)
    cr.stroke()
    cr.set_source_surface(su, -w_ / 2, -h_ / 2)
    cr.paint_with_alpha(q)
    if under:
        u = prog(t, t_in + 0.3, 0.3)
        cr.move_to(-w_ / 2, h_ / 2 + 4)
        cr.line_to(-w_ / 2 + w_ * u, h_ / 2 + 4)
        cr.set_source_rgba(*RED, q)
        cr.set_line_width(7)
        cr.stroke()
    cr.restore()


# Labels per line: (cue name or seconds after the line's start, text, options). Each label stays until the next one of
# its line starts (or `out`), so one label shows at a time unless `keep` is set.
LABELS = {
    "a1": [(0.3, "आठ जगह से टेढ़ा", dict(x=760, y=560, size=80)),
           ("P", "पिता का श्राप", dict(x=760, y=560, size=90, col=RED, under=True))],
    "a3": [("K", "कहोड़ ऋषि", dict(y=380)),
           ("M", "हर रात: मंत्र", dict(y=380)),
           ("B", "पेट में बच्चा भी सुनता था", dict(y=380, size=70))],
    "a4": [("V", "पेट से आवाज़!", dict(y=380, size=92)),
           ("W", "आप गलत पढ़ रहे हो!", dict(y=380, size=84, col=RED))],
    "a6": [(0.05, "सबके सामने अपमान!", dict(y=360, size=84)),
           ("C", "श्राप!", dict(y=360, size=110, col=RED)),
           ("E", "आठ जगह से टेढ़ा", dict(y=360, size=88, col=RED, under=True))],
    "a8": [("Py", "घर में पैसे नहीं", dict(y=360)),
           ("P", "राजा का महल", dict(y=360))],
    "a9": [(0.05, "घमंडी पंडित", dict(y=360, size=90)),
           ("L", "हारे, तो पानी में!", dict(y=360, size=88, col=RED))],
    "a10": [("L", "पिता हार गए", dict(y=360, size=90)),
            ("W", "पानी में", dict(y=360, size=90))],
    "a7": [("E", "आठ जगह से टेढ़ा", dict(y=380)),
           ("A", "अष्टावक्र", dict(y=380, size=120, col=RED, under=True))],
    "a11": [("Y", "बारह साल बाद", dict(y=360, size=96)),
            ("Mn", "माँ ने सच बताया", dict(y=360, size=84))],
    "a12": [("S", "रोक दिया!", dict(y=360, size=100)),
            ("K", "उम्र नहीं, अक्ल!", dict(y=360, size=96, col=RED, under=True))],
    "a10q": [("P", "वही पंडित", dict(y=360, size=96)),
             ("Q", "क्या ये जीतेगा?", dict(y=360, size=92, col=RED))],
    "a13": [(0.05, "बहस", dict(y=360, size=110)),
            ("Wn", "बच्चा जीत गया!", dict(y=360, size=100, col=RED, under=True))],
    "a14": [("S", "राज़", dict(y=360, size=110)),
            ("Dv", "पानी के देवता का बेटा", dict(y=360, size=80)),
            ("M", "कोई मरा नहीं!", dict(y=360, size=100, col=RED))],
    "a15": [("L", "पिता ज़िंदा लौटे!", dict(y=360, size=92)),
            ("N", "नदी में", dict(y=360, size=96)),
            ("S", "शरीर सीधा!", dict(y=360, size=110, col=RED, under=True))],
    "a15c": [("P", "बोलने की सज़ा", dict(y=330)),
             ("V", "उसी ने पिता लौटाए", dict(y=330, size=80, col=RED))],
    "a16": [("Q", "गलत कौन?", dict(y=330, size=120, col=RED, under=True))],
}


def labels(cr, t, tl, bid, t1):
    specs = LABELS.get(bid, [])
    if not specs:
        return
    c = cues(tl, bid) if bid in CUES else {"t0": T(tl, bid)}
    starts = []
    for when, _, _ in specs:
        starts.append(c["t0"] + when if isinstance(when, (int, float)) else c[when] - 0.1)
    if bid == "a1":
        starts[0] = 0.3
    for i, (_, text, kw) in enumerate(specs):
        kw = dict(kw)
        t_out = kw.pop("out", None)
        if t_out is None:
            t_out = starts[i + 1] - 0.15 if i + 1 < len(starts) else t1 - 0.12
        label(cr, t, starts[i], text, t_out=t_out, **kw)


# ------------------------------------------------------------------ the boy with his eight joints

def _joints(rig):
    """The boy's rig with eight more named points: the joints the curse bends."""
    pts = dict(rig.points)
    pts.update({"j1": ("av_boy_head", (0, -10)), "j2": ("av_boy_body", (-70, -170)),
                "j3": ("av_boy_armF_up", (0, 150)), "j4": ("av_boy_armF_lo", (0, 150)),
                "j5": ("av_boy_armB_up", (0, 150)), "j6": ("av_boy_body", (0, -10)),
                "j7": ("av_boy_legF", (10, 215)), "j8": ("av_boy_legB", (10, 215))})
    return pc.Rig(rig.parts, pts, rig.rods)


BOY_J = _joints(AV.BOY)
BOY_BENT_J = _joints(AV.BOY_BENT)
JOINT_ORDER = ("j1", "j3", "j4", "j2", "j5", "j6", "j7", "j8")


def boy_j(cr, t, x, s, mood="calm", bent=True, staff=False, front=(-0.95, -0.35), backa=(0.35, -0.5), feet=G, **kw):
    """scenes_ashtavakra.boy with the joint points (straight or bent)."""
    rig = BOY_BENT_J if bent else BOY_J
    swap = dict(AV.BENT_SWAP) if bent else {}
    swap["av_boy_head"] = A.hname("av_boy_head", mood, "calm")
    if staff:
        probe = dict(kw, alpha=0.0, rods=False)
        pts = fig(cr, rig, "av_boy", t, x, s, front=front, backa=backa, swap=swap, feet=feet, **probe)
        hx, hy = to_user(cr, pts["handF"])
        sg = -1 if kw.get("flip") else 1
        prop(cr, "av_staff", hx + 6 * s * sg, max(hy + 20, feet), s * 1.3, rot=0.04 * sg,
             alpha=kw.get("alpha", 1.0), blur=kw.get("blur", 0.0))
    return fig(cr, rig, "av_boy", t, x, s, front=front, backa=backa, swap=swap, feet=feet, **kw)


def joint_dots(cr, t, pts, t_on, step=0.17, alpha=1.0, col=(1.0, 0.22, 0.12)):
    """The eight bent joints lighting up red one by one from t_on (a ring pops on each), with a small count."""
    n_on = 0
    for i, k in enumerate(JOINT_ORDER):
        ti = t_on + step * i
        if t < ti:
            break
        n_on = i + 1
        x, y = to_user(cr, pts[k])
        u = prog(t, ti, 0.25)
        pulse = 0.75 + 0.25 * math.sin(t * 7 + i)
        red_spot(cr, x, y, 80, 0.6 * u * alpha)
        cr.save()
        cr.arc(x, y, 22 * u * pulse + 5, 0, 2 * math.pi)
        cr.set_source_rgba(*col, 0.95 * u * alpha)
        cr.fill()
        r = (t - ti) / 0.5
        if 0 < r < 1:
            cr.arc(x, y, 20 + 70 * ease(r), 0, 2 * math.pi)
            cr.set_source_rgba(*col, 0.8 * (1 - r) * alpha)
            cr.set_line_width(6 * (1 - r) + 1)
            cr.stroke()
        cr.restore()
    return n_on


def count_disc(cr, t, n, x, y, a):
    """A round leather medallion with the running count of lit joints (1..8)."""
    if n <= 0 or a <= 0.01:
        return
    A.num_disc(cr, x, y, 62, str(n), a, 0.06 * math.sin(t * 2), RED, hot=1.0 if n == 8 else 0.4)


def red_spot(cr, x, y, r, a):
    """A local red light (unlike red_glow, it does not tint the whole frame)."""
    if a <= 0.01:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 1.0, 0.18, 0.08, 0.55 * a)
    g.add_color_stop_rgba(1, 0.8, 0.05, 0.02, 0.0)
    cr.save()
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def beam(cr, t, t0, t1, p0, p1, seed=0, col=(1.0, 0.22, 0.10)):
    """The curse held on the boy: a thick, crackling red beam from the finger to his chest from t0 to t1 (fading in
    and out), with a red glow along it."""
    a = prog(t, t0, 0.12) * (1 - prog(t, t1 - 0.25, 0.25))
    if a <= 0.01:
        return
    n = 10
    pts = [p0]
    for i in range(1, n):
        f = i / n
        j = 26 * math.sin(i * 2.3 + int(t * 16) * 1.7 + seed)
        dx, dy = p1[0] - p0[0], p1[1] - p0[1]
        L_ = math.hypot(dx, dy) or 1
        pts.append((p0[0] + dx * f - dy / L_ * j, p0[1] + dy * f + dx / L_ * j))
    pts.append(p1)
    for i in range(0, n + 1, 2):
        red_spot(cr, pts[i][0], pts[i][1], 110, 0.35 * a)
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    fl = 0.8 + 0.2 * math.sin(t * 37 + seed)
    for lw, c, k in ((30, col, 0.30), (14, col, 0.85)):
        cr.move_to(*pts[0])
        for p in pts[1:]:
            cr.line_to(*p)
        cr.set_source_rgba(*c, k * a * fl)
        cr.set_line_width(lw)
        cr.stroke()
    cr.set_operator(cairo.OPERATOR_ADD)
    cr.move_to(*pts[0])
    for p in pts[1:]:
        cr.line_to(*p)
    cr.set_source_rgba(1.0, 0.9, 0.7, 0.9 * a)
    cr.set_line_width(4)
    cr.stroke()
    cr.restore()
    sparkle(cr, p1[0], p1[1], 70 * a, a, (1.0, 0.55, 0.3))


# ------------------------------------------------------------------ a1  HOOK: the curse hits, eight joints bend

HK_F = (200, 1.4)                   # the father: x, scale (feet on G)
HK_B = (940, 0.92)                   # the boy: x, scale
T_HIT = 0.45                         # the first bolt


def a_hook(cr, t, tl, t0, t1):
    c = cues(tl, "a1")
    tE, tP = c["E"], c["P"]
    t_dots = max(T_HIT + 0.35, tE - 0.1)
    stars(cr, t, 0.9, ((120, 300), (300, 230), (620, 180), (900, 280), (1000, 520), (700, 420), (980, 900)))
    fx, fs = HK_F
    red_spot(cr, fx + 60, 760, 620, 0.55 + 0.1 * math.sin(t * 3))
    cursing = t > T_HIT - 0.15
    kp = A.kahoda(cr, t, fx, fs, mood="curse" if cursing else "angry", front=(-0.85, 0.05), backa=(0.35, -0.5),
                  hits=[(T_HIT, 0.5), (tP, 0.4)], ph=0.6, rot=0.004 * math.sin(t * 19))
    bx, bs = HK_B
    hit = t > T_HIT + 0.12
    A.cool(cr, bx, G - 420, 420, 0.5 * (1 - prog(t, T_HIT, 0.3)))
    glow(cr, bx, G - 420, 460, 0.45)
    shake = 0.05 * math.exp(-4 * max(0.0, t - T_HIT - 0.12)) * math.sin(t * 40) * hit
    bp = boy_j(cr, t, bx, bs, mood="shut" if hit else "wonder", bent=hit, flip=True, rot=shake,
               front=(-0.4, -0.5) if hit else (-0.2, -0.3), backa=(0.5, -0.9) if hit else (0.2, -0.2),
               hits=[(T_HIT + 0.12, 0.8)], ph=0.2)

    def ui(cr_):                          # above the night colour, so the red stays red
        hand = to_user(cr_, kp["handF"])
        chest = to_user(cr_, bp["chest"])
        hd = to_user(cr_, kp["head"])
        red_spot(cr_, hd[0] + 30, hd[1] - 10, 230, 0.45 + 0.2 * math.sin(t * 9))
        beam(cr_, t, T_HIT, t_dots + 8 * 0.17 + 0.5, hand, chest)
        beam(cr_, t, tP - 0.1, tP + 0.9, hand, chest, seed=5)
        n = joint_dots(cr_, t, bp, t_dots) if hit else 0
        top = to_user(cr_, bp["top"])
        count_disc(cr_, t, n, min(top[0] + 170, 990), top[1] + 40, prog(t, t_dots, 0.2))
    return dict(ui=ui, flash=flash_at(t, T_HIT + 0.1, 0.45) + flash_at(t, tP, 0.2))


# ------------------------------------------------------------------ a3  the father teaches; the baby listens

def a_listen(cr, t, tl, t0, t1):
    c = cues(tl, "a3")
    tK, tM, tB, tS = c["K"], c["M"], c["B"], c["S"]
    stars(cr, t, 0.6, ((150, 640), (420, 700), (900, 660), (1000, 900)))
    A.moon_arc(cr, t, t0 - 1.0, t1 + 3.0, 0.9)
    glow(cr, 560, 1400, 720, 0.4)
    A.ground(cr)
    lx = 560
    fl = 0.85 + 0.15 * math.sin(t * 9)
    glow(cr, lx, G - 150, 420, 0.7 * fl)
    warm(cr, lx, G - 150, 360, 0.5 * fl)
    prop(cr, "av_lamp", lx, G, 0.5)
    prop(cr, f"flame{int(t * 10) % 3}", lx + 3, G - 118, 0.17)
    for i, (dx, ds, bl) in enumerate(((30, 0.56, 2.0), (150, 0.52, 3.0))):
        A.dis_sit(cr, t, i + 1, dx, G - 10 * i, ds, mood="smile" if t > tM + 0.6 else "calm",
                  front=(-0.75, -1.85), backa=(-0.8, -1.8), blur=bl, ph=0.5 * i)
    kp = A.kahoda_sit(cr, t, 340, G, 0.9, mood="read", tilt=0.04 * math.sin(t * 2.4), hits=[(tK, 0.3)], ph=0.9)
    sp = A.suj(cr, t, 820, G, 1.0, mood="smile" if t > tS else "open", flip=True, front=(-0.8, -0.9),
               backa=(-0.2, -0.7), ph=0.4)
    bx, by = to_user(cr, sp["belly"])
    lit = prog(t, tB - 0.3, 0.5)
    A.womb(cr, t, bx - 4, by - 10, 140 + 40 * lit, 160 + 44 * lit, 0.55 + 0.45 * lit, False, 0.0,
           0.5 + 0.5 * math.sin(t * 2.6) + 1.0 * math.exp(-3 * max(0.0, t - tB)) * (t > tB), flip=True)
    mouth = to_user(cr, kp["head"])
    A.mantras(cr, t, tM - 0.3, (mouth[0] - 70, mouth[1] + 10), (110, G - 500))
    A.mantras(cr, t, tB - 0.2, (mouth[0] + 70, mouth[1] + 10), (bx - 20, by - 20))
    if t > tS - 0.2:
        sound_rings(cr, bx - 140, by - 20, t, tS - 0.2, n=3, rmax=160, alpha=0.5)
    return dict(night=0.22, lift=1.0, flash=flash_at(t, tK, 0.12) + flash_at(t, tB, 0.15))


# ------------------------------------------------------------------ a10q  the question: can a bent boy beat him?

def a_face(cr, t, tl, t0, t1):
    c = cues(tl, "a10q")
    tP, tD, tQ, tH = c["P"], c["D"], c["Q"], c["H"]
    A.court(cr, t, kmood="calm", hs=0.9)
    vx, vs = 880, 1.05
    red_glow(cr, vx, G - 520, 520, 0.35 * prog(t, tP, 0.4))
    vp = A.vandin(cr, t, vx, vs, mood="smirk", flip=True, front=(-0.3, -0.5), backa=(-0.3, -0.9),
                  head=-0.06, hits=[(tP, 0.4)], ph=1.1)
    if t > tD - 0.2:                                                             # the father he drowned: a blue memory
        A.cool(cr, vx, G - 300, 380, 0.5 * prog(t, tD - 0.2, 0.4) * (1 - prog(t, tQ, 0.5)))
        A.bubbles(cr, t, vx - 60, G - 200, 160, 7, 0.7 * prog(t, tD - 0.2, 0.4) * (1 - prog(t, tQ, 0.5)))
    bx, bs = 200, 0.98
    glow(cr, bx, G - 420, 420, 0.5)
    bp = A.boy(cr, t, bx, bs, mood="firm", front=(-0.45, -0.3), hits=[(tQ, 0.4)], ph=0.4)
    vm = to_user(cr, vp["head"])
    bm = to_user(cr, bp["head"])

    def ui(cr_):
        q = prog(t, tQ, 0.35)
        if q > 0.01:
            cr_.save()
            cr_.translate((vm[0] + bm[0]) / 2, min(vm[1], bm[1]) - 60)
            cr_.scale(0.6 + 0.4 * ease(q), 0.6 + 0.4 * ease(q))
            cr_.rotate(0.06 * math.sin(t * 2))
            draw_text(cr_, "?", 0, 0, 380, RED, clamp(q), anchor="cm")
            cr_.restore()
        if t > tH:
            red_ring(cr_, (vm[0] + bm[0]) / 2, min(vm[1], bm[1]) - 60, 170, 210, prog(t, tH, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tP, 0.15) + flash_at(t, tQ, 0.2))


# ------------------------------------------------------------------ a15c  CALLBACK: the hook's framing, in gold

def a_callback(cr, t, tl, t0, t1):
    c = cues(tl, "a15c")
    tP, tU, tV = c["P"], c["U"], c["V"]
    gold = prog(t, tU - 0.2, 0.6)
    glow(cr, 540, 900, 760, 0.35 + 0.35 * gold)
    warm(cr, 520, 1000, 640, 0.6 * gold)
    aura(cr, t, 540, 900, 140, 760, 0.55 * gold, n=22, spin=0.08)
    fx, fs = HK_F
    kp = A.kahoda(cr, t, fx, fs, mood="smile" if t > tU else "shame", front=(-1.0, -0.3), backa=(0.35, -0.5),
                  hits=[(tU, 0.4)], ph=0.6)
    bx, bs = HK_B
    bp = boy_j(cr, t, bx, bs, mood="smile", bent=False, flip=True, front=(-1.0, -0.4), backa=(0.3, -0.4),
               hits=[(tV, 0.4)], ph=0.2)
    hand = to_user(cr, kp["handF"])
    chest = to_user(cr, bp["chest"])
    bolt(cr, t, tP, hand, chest, 0.8, col=(1.0, 0.25, 0.12), seed=2)              # the old punishment, once
    if t > tU:                                                                   # now a thread of gold light
        cr.save()
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        u = prog(t, tU, 0.5)
        mx, my = (hand[0] + chest[0]) / 2, min(hand[1], chest[1]) - 120
        cr.move_to(*hand)
        cr.curve_to(mx, my, mx, my, hand[0] + (chest[0] - hand[0]) * u, hand[1] + (chest[1] - hand[1]) * u)
        cr.set_source_rgba(1.0, 0.85, 0.40, 0.8 * u)
        cr.set_line_width(10)
        cr.stroke()
        cr.restore()
        lights(cr, t, mx, my + 60, 260, 12, 0.7 * u)
    return dict(flash=flash_at(t, tU, 0.15) + flash_at(t, tV, 0.25))


# ------------------------------------------------------------------ a16  who was wrong? two Hindi cards

def hcard(cr, t, t_in, x, y, big, small, a=1.0):
    """A leather plaque with a big Hindi word (red) and a small one under it (ink)."""
    q = prog(t, t_in, 0.3)
    if q <= 0.01 or not HAS_INDIC:
        return
    sb = indic_surface(big, 104, RED)
    ss = indic_surface(small, 64, INK)
    w_ = max(sb.get_width(), ss.get_width()) + 90
    h_ = sb.get_height() + ss.get_height() + 70
    yy = y + 40 * (1 - ease(q))
    cr.save()
    cr.translate(x, yy)
    cr.rotate(0.02 * math.sin(t * 1.3 + x))
    pc.poly(cr, [(-w_ / 2, -h_ / 2), (w_ / 2, -h_ / 2), (w_ / 2, h_ / 2), (-w_ / 2, h_ / 2)])
    cr.set_source_rgba(*PARCH, 0.97 * q * a)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, q * a)
    cr.set_line_width(5)
    cr.stroke()
    cr.set_source_surface(sb, -sb.get_width() / 2, -h_ / 2 + 22)
    cr.paint_with_alpha(q * a)
    cr.set_source_surface(ss, -ss.get_width() / 2, h_ / 2 - ss.get_height() - 22)
    cr.paint_with_alpha(q * a)
    cr.restore()


def a_end(cr, t, tl, t0, t1):
    c = cues(tl, "a16")
    tQ, tS, tF = c["Q"], c["S"], c["F"]
    glow(cr, 270, G - 450, 420, 0.5)
    red_glow(cr, 810, G - 450, 420, 0.35 * prog(t, tF - 0.2, 0.4))
    A.ground(cr)
    A.boy(cr, t, 270, 1.08, mood="firm", bent=False, staff=False, front=(-0.6, -0.4), hits=[(tS, 0.4)], ph=0.3)
    A.kahoda(cr, t, 820, 1.0, mood="curse" if t > tF else "angry", flip=True,
             front=(-1.55, -0.05) if t > tF - 0.2 else (-0.5, -0.6), backa=(0.3, -0.4), hits=[(tF, 0.4)], ph=0.6)
    cards = ((270, "बेटा?", "सच बोला", tS - 0.1), (820, "पिता?", "ग़ुस्सा किया", tF - 0.1))

    def ui(cr_):
        for cx, big, small, tc in cards:
            hcard(cr_, t, tc - 0.2, cx, 560, big, small)
        if t > tF + 0.3:
            n = int((t - tF - 0.3) / 0.9)
            k = n % 2
            red_ring(cr_, cards[k][0], 564, 230, 150, prog(t, tF + 0.3 + 0.9 * n, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tQ, 0.15))


# ------------------------------------------------------------------ the cut list and the frame

NIGHT_BLUE = (0.50, 0.62, 1.0)
ANGER = (1.0, 0.55, 0.45)
COURT = (1.0, 0.74, 0.58)
WATER = (0.55, 0.72, 1.0)
DAWN = (1.0, 0.72, 0.50)
DAY = (0.92, 1.0, 0.82)
GOLD = (1.0, 0.88, 0.62)

SHOTS = [   # (line, draw function, options: zoom range, focus, place colour (rgb, strength), night)
    # zoom about the focus: fy = (1840 - 1775 z) / (1 - z) keeps the ground line just above the bottom edge
    ("a1", a_hook, dict(z=(1.0, 1.04), focus=(540, 1000), place=(NIGHT_BLUE, 0.7), night=0.3)),
    ("a3", a_listen, dict(z=(1.15, 1.2), focus=(560, 1342), place=(NIGHT_BLUE, 0.35), night=0.2)),
    ("a4", A.a_voice, dict(z=(1.4, 1.46), focus=(560, 1612), place=(NIGHT_BLUE, 0.35), night=0.2)),
    ("a6", A.a_curse, dict(z=(1.3, 1.36), focus=(545, 1558), place=(ANGER, 0.45))),
    ("a8", A.a_palace, dict(z=(1.25, 1.3), focus=(540, 1515), place=(COURT, 0.25))),
    ("a9", A.a_rule, dict(z=(1.1, 1.15), focus=(540, 1125), place=(COURT, 0.3))),
    ("a10", A.a_lost, dict(z=(1.25, 1.3), focus=(540, 1515), place=(WATER, 0.4))),
    ("a7", A.a_named, dict(z=(1.4, 1.45), focus=(420, 1612), place=(GOLD, 0.3))),
    ("a11", A.a_years, dict(z=(1.25, 1.3), focus=(600, 1515), place=(DAY, 0.35))),
    ("a12", A.a_gate, dict(z=(1.2, 1.25), focus=(600, 1450), place=(DAY, 0.25))),
    ("a10q", a_face, dict(z=(1.1, 1.15), focus=(540, 1125), place=(COURT, 0.35))),
    ("a13", A.a_debate, dict(z=(1.15, 1.2), focus=(540, 1342), place=(COURT, 0.35))),
    ("a14", A.a_secret, dict(z=(1.08, 1.12), focus=(560, 962), place=(WATER, 0.45))),
    ("a15", A.a_back, dict(z=(1.12, 1.17), focus=(540, 1233), place=(DAWN, 0.4))),
    ("a15c", a_callback, dict(z=(1.0, 1.04), focus=(540, 1000), place=(GOLD, 0.3))),
    ("a16", a_end, dict(z=(1.0, 1.03), focus=(540, 1200), night=0.3)),
]


def shot_at(t, tl):
    """(index, start, end) of the shot showing at t (cached on the timeline under _av2_shots)."""
    cache = getattr(tl, "_av2_shots", None)
    if cache is None:
        starts = [0.0]
        for bid, _, _ in SHOTS[1:]:
            starts.append(max(T(tl, bid) - 0.12, starts[-1] + 0.5))
        cache = tl._av2_shots = starts
    k = 0
    for i, s in enumerate(cache):
        if t >= s:
            k = i
    return k, cache[k], cache[k + 1] if k + 1 < len(cache) else tl.total


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl)
    bid, fn, opt = SHOTS[k]
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
    if opt.get("place"):
        col, a = opt["place"]
        tint(cr, col, a)
    if out.get("ui"):
        out["ui"](cr)                     # rings, discs, bursts (their English text is switched off above)
    cr.restore()
    motes(cr, t)
    pc.lamp(cr, t, night=max(out.get("night", 0.0), opt.get("night", 0.0)), flash=out.get("flash", 0.0))
    sepia(cr, out.get("sepia", 0.0))
    labels(cr, t, tl, bid, t1)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """Sparse sounds (owner, 8 Nov 2026: "only use sounds where necessary"), most important first, each at least
    SFX_MIN_GAP apart: a damaru on the hook's bolt, a conch at the curse, a hit as the boy wins, shimmer as his body
    becomes straight, a bell on the closing question, then shimmer at "all alive" if it fits; dips before reveals."""
    c = {b: cues(tl, b) for b in CUES}
    t_str = c["a15"]["S"] - 0.15
    t_end = min(max(c["a16"]["S"], t_str + SFX_MIN_GAP + 0.05), tl["a16"].end - 0.05)
    want = [(T_HIT, "damaru", 0), (c["a6"]["C"], "conch", 0), (c["a13"]["Wn"], "hit", 0), (t_str, "shimmer", 0),
            (t_end, "bell", 0), (c["a14"]["Z"], "shimmer", 0), (c["a7"]["A"], "bell", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["a6"]["C"] - 0.3, "dip", 0.45), (c["a13"]["Wn"] - 0.35, "dip", 0.5), (c["a14"]["Z"] - 0.3, "dip", 0.45),
            (t_str - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
