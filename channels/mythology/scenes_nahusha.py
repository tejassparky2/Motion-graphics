"""Scenes for videos/nahusha.py: King Nahusha, made king of heaven, cursed into a python for kicking a sage, and freed
by Yudhishthira's answers (Mahabharata, Udyoga Parva 11-17; Vana Parva 178-181), in Togalu Gombeyaata shadow
puppets drawn in code. Frame 0 is the stake itself: the king on his palanquin carried by sages, the kick, the python.
Short Hindi labels, a colour per place (heaven gold, earth warm, forest green, anger red), a callback in gold.

Respect: the sages are old and dignified, never comic; no blood; the python is the friendly old leather snake of the
Ruru reel with Nahusha's own crown, so a child always knows who it is; Bhima is held, never hurt.

Shot list (line: what is on the screen)
  nh1   HOOK: the palanquin on the sages' shoulders, Nahusha proud; his kick at the front sage; a flash: the python
  nh2   Nahusha standing before his city on earth
  nh3   heaven: the king of the gods walks off his throne into a cloud; the empty throne, a red "?"
  nh4   Nahusha rises from below on a cloud to the throne; two gods bow; a gold aura
  nh5   Nahusha on the throne laughing, red light; he points: the sages shall carry him
  nh6   the procession: four old sages under the poles, walking, clouds drift past
  nh7   closer: Nahusha jabbing his hand, shouting "sarpa! sarpa!"
  nh8   the palanquin stops; his foot shoots out and strikes the front sage's head
  nh9   the sage, big and angry, his hand raised in a curse; Nahusha small and shocked; "sarpa = snake"
  nh10  Nahusha falls through the sky, a flash, a python lands on the earth in a cloud of dust
  nh11  the python coiled under a tree as suns and moons race over it; leaves fall
  nh12  Bhima walks into the forest with his mace; the python watches from behind a tree
  nh13  the python winds round Bhima; he strains and cannot move
  nh14  close on Bhima in the coils, a red "?"
  nh15  the python speaks; a thought bubble: the sage's boon (gold light); Bhima's strength bar drains
  nh16  the python's head close up, Nahusha's ghost behind it; the jaws open
  nh17  Yudhishthira walks in; the python turns to him
  nh18  the question; three gold words (truth, kindness, forgiveness); "birth" struck out, "deeds" ringed
  nh19  a flash: the coils fall away, Nahusha's king form rises in gold to the sky, Bhima free
  nh20  CALLBACK: left, the king falling (red arrow down); right, rising (gold arrow up)
  nh21  two cards (ताक़त? / समझ?), Bhima and Yudhishthira under them, a red ring alternating
"""
import math

import cairo

import lrekha_cast  # noqa: F401  (registers the speech cloud, leaves)
import nahusha_cast as N
import ruru_cast as RU
import camera_beats
import puppet_core as pc
import scenes_ruru as RS
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import clamp, ease, prog
from puppet_core import H, W, hop_walk, keyed, prop, puppet
from scenes_andhe_ka_putra import bhima as bhima_fig
from scenes_arjuna import yudh
from scenes_ashtavakra2 import hcard, label
from scenes_bhrigu import sage
from scenes_hanuman_curse import arc_path, qmark
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, man_angles, motes, red_ring, walk_legs
from scenes_jayadratha import flash_at, tint, to_user
from scenes_kaikeyi import fig
from scenes_lakshman_rekha import forest
from scenes_mandhata import ashvin, aura, indra, lights, warm
from scenes_manthara import dots_path, ground, puffs
from scenes_six_c import agastya
from scenes_snake_tongue import heaven
from shots import T

G = FEET + 120
MISSES = set()
SN, SNB = RU.SN_OLD, RU.SN_OLD_B
PARCH = pc.PARCH

FIRST = {"nh1": "n01", "nh2": "n02", "nh3": "n03", "nh4": "n05", "nh5": "n07", "nh6": "n09", "nh7": "n10",
         "nh8": "n12", "nh9": "n13", "nh10": "n16", "nh11": "n17", "nh12": "n18", "nh13": "n20", "nh14": "n22",
         "nh15": "n23", "nh16": "n25", "nh17": "n27", "nh18": "n29", "nh19": "n32", "nh20": "n34", "nh21": "n35"}

# Every cue of every shot: (name, line, word, fraction fallback, ((after, min gap), ...)); "t0" = the shot's start.
CUES = {
    "nh1": (("D", "n01", "देवताओं", 0.25, (("t0", 0.3),)), ("L", "n01", "लात", 0.7, (("D", 0.8),)),
            ("A", "n01", "अजगर", 0.85, (("L", 0.5),))),
    "nh2": (("N", "n02", "नहुष", 0.4, (("t0", 0.2),)), ("M", "n02", "महान", 0.8, (("N", 0.5),))),
    "nh3": (("C", "n03", "छिप", 0.8, (("t0", 1.2),)), ("K", "n04", "राजा", 0.6, (("C", 0.6),))),
    "nh4": (("N", "n05", "नहुष", 0.45, (("t0", 0.6),)), ("S", "n05", "स्वर्ग", 0.75, (("N", 0.6),)),
            ("I", "n06", "इंसान", 0.2, (("S", 0.6),)), ("R", "n06", "राज", 0.75, (("I", 0.5),))),
    "nh5": (("T", "n07", "ताक़त", 0.25, (("t0", 0.3),)), ("G", "n07", "घमंड", 0.8, (("T", 0.5),)),
            ("P", "n08", "पालकी", 0.55, (("G", 0.6),)), ("R", "n08", "ऋषि", 0.8, (("P", 0.3),))),
    "nh6": (("B", "n09", "बूढ़े", 0.1, (("t0", 0.0),)), ("P", "n09", "पालकी", 0.35, (("B", 0.4),)),
            ("K", "n09", "कंधों", 0.55, (("P", 0.4),))),
    "nh7": (("J", "n10", "जल्दी", 0.3, (("t0", 0.2),)), ("S", "n10", "सर्प", 0.75, (("J", 0.5),)),
            ("M", "n11", "मतलब", 0.55, (("S", 0.8),)), ("C", "n11", "चलो", 0.9, (("M", 0.4),))),
    "nh8": (("G", "n12", "गुस्से", 0.15, (("t0", 0.1),)), ("L", "n12", "लात", 0.85, (("G", 1.0),))),
    "nh9": (("S", "n13", "श्राप", 0.45, (("t0", 0.3),)), ("B", "n13", "बद्दुआ", 0.8, (("S", 0.5),)),
            ("C", "n14", "चिल्लाता", 0.6, (("B", 0.6),)), ("K", "n15", "खुद", 0.35, (("C", 0.6),)),
            ("Y", "n15", "साँप", 0.9, (("K", 0.5),))),
    "nh10": (("P", "n16", "पल", 0.1, (("t0", 0.0),)), ("A", "n16", "अजगर", 0.45, (("P", 0.6),)),
             ("G", "n16", "गिर", 0.85, (("A", 0.6),))),
    "nh11": (("S", "n17", "सालों", 0.1, (("t0", 0.0),)), ("J", "n17", "जंगल", 0.5, (("S", 0.4),))),
    "nh12": (("B", "n18", "भीम", 0.8, (("t0", 0.8),)), ("T", "n19", "ताक़तवर", 0.6, (("B", 0.8),))),
    "nh13": (("A", "n20", "अचानक", 0.05, (("t0", 0.0),)), ("L", "n20", "लपेटकर", 0.65, (("A", 0.6),)),
             ("J", "n20", "जकड़", 0.85, (("L", 0.4),)), ("Z", "n21", "ज़ोर", 0.3, (("J", 0.6),)),
             ("H", "n21", "हिल", 0.75, (("Z", 0.5),))),
    "nh14": (("T", "n22", "ताक़तवर", 0.25, (("t0", 0.2),)), ("K", "n22", "कैसे", 0.8, (("T", 0.6),))),
    "nh15": (("R", "n23", "ऋषि", 0.3, (("t0", 0.3),)), ("V", "n23", "वरदान", 0.85, (("R", 0.5),)),
             ("P", "n24", "पकड़", 0.3, (("V", 0.6),)), ("T", "n24", "ताक़त", 0.75, (("P", 0.5),))),
    "nh16": (("N", "n25", "नहुष", 0.2, (("t0", 0.2),)), ("K", "n25", "खानदान", 0.6, (("N", 0.6),)),
             ("A", "n26", "आज", 0.2, (("K", 0.6),)), ("E", "n26", "खा", 0.7, (("A", 0.4),))),
    "nh17": (("Y", "n27", "युधिष्ठिर", 0.65, (("t0", 0.8),)), ("J", "n28", "जवाब", 0.45, (("Y", 0.6),)),
             ("C", "n28", "छोड़", 0.85, (("J", 0.5),))),
    "nh18": (("Q", "n29", "ऊँचा", 0.6, (("t0", 0.3),)), ("S", "n30", "सच", 0.55, (("Q", 0.8),)),
             ("D", "n30", "दया", 0.75, (("S", 0.35),)), ("M", "n30", "माफ़ी", 0.9, (("D", 0.35),)),
             ("J", "n31", "जन्म", 0.15, (("M", 0.6),)), ("K", "n31", "कामों", 0.6, (("J", 0.5),))),
    "nh19": (("T", "n32", "टूट", 0.8, (("t0", 0.6),)), ("B", "n33", "छोड़", 0.3, (("T", 0.6),)),
             ("S", "n33", "स्वर्ग", 0.85, (("B", 0.8),))),
    "nh20": (("G", "n34", "गिराया", 0.45, (("t0", 0.6),)), ("U", "n34", "उठाया", 0.9, (("G", 0.8),))),
    "nh21": (("T", "n35", "ताक़त", 0.25, (("t0", 0.6),)), ("S", "n35", "समझ", 0.45, (("T", 0.4),))),
}


def cue(tl, line, word, frac):
    try:
        return T(tl, line, {"hi": word})
    except (KeyError, ValueError):
        MISSES.add((line, word))
        return T(tl, line, frac)


def cues(tl, shot):
    cache = getattr(tl, "_nh_cues", None)
    if cache is None:
        cache = tl._nh_cues = {}
    if shot not in cache:
        out = {"t0": T(tl, FIRST[shot])}
        for name, line, word, frac, cons in CUES[shot]:
            v = cue(tl, line, word, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[shot] = out
    return cache[shot]


def speaking(tl, t, *lines, rate=2.6):
    """The python's jaw: open/shut while one of `lines` is being spoken."""
    for ln in lines:
        b = tl[ln]
        if b.start <= t <= b.end - 0.1:
            return math.sin((t - b.start) * 2 * math.pi * rate) > 0.1
    return False


# ------------------------------------------------------------------ Nahusha


def nh_head(mood):
    return "nh_nahusha_head" + ("" if mood == "calm" else "_" + mood)


def nahusha(cr, t, x, s, mood="calm", feet=G, **kw):
    return fig(cr, N.NAHUSHA, "nh_nahusha", t, x, s, swap={"nh_nahusha_head": nh_head(mood)}, feet=feet, **kw)


def nahusha_seated(cr, t, x, hip, s, mood="proud", seat="nh_nahusha_cross", front=(-0.5, -0.9), backa=(0.3, -1.0),
                   head=0.0, kick=0.0, hits=(), alpha=1.0, blur=0.0, rods=True):
    """Nahusha sitting (hip at x, hip): cross-legged on the palanquin, or legs down on the throne (nh_nahusha_seat).
    kick 0..1 swings his front leg out forward (to the right) from the hip; returns his points plus 'foot'."""
    prop(cr, seat, x, hip, s, alpha=alpha, blur=blur)
    ang = man_angles("nh_nahusha", t, front, backa, head, (0.0, 0.0), hits, 0.6)
    pts = puppet(cr, N.NAHUSHA, x, hip, s, bob_rot(t, 0.6, 0.006), False, ang, alpha, blur,
                 hide=("nh_nahusha_legF", "nh_nahusha_legB"), swap={"nh_nahusha_head": nh_head(mood)}, rods=rods)
    if kick > 0.01:
        a = -1.2 * kick                                     # forward and a little down: onto the sage's head
        lx, ly = x + 18 * s, hip + 8 * s
        prop(cr, "nh_nahusha_legF", lx, ly, s, rot=a, alpha=alpha, blur=blur)
        pts["foot"] = (lx - 440 * s * math.sin(a), ly + 440 * s * math.cos(a))
    return pts


# ------------------------------------------------------------------ the palanquin procession

SS = 0.58                             # the bearer sages' scale
PS = 0.62                             # the palanquin's scale
NS = 0.55                             # Nahusha's scale on it
POLE = G - 696 * SS                   # the poles rest on the bearers' shoulders
FLOOR = POLE - 70 * PS                # the palanquin's seat floor
HIP = FLOOR - 28 * PS - N.CROSS_H * NS


def bearer(cr, t, who, x, i, walk, alpha=1.0, blur=0.0, mood="calm", head=0.18, hit=None):
    ph = math.sin(2 * math.pi * 1.1 * t + 1.7 * i) if walk else 0.0
    bob = -6 * abs(ph)
    jolt = 0.0
    if hit is not None and t > hit:
        jolt = 0.45 * math.exp(-3.0 * (t - hit)) * math.cos(9 * (t - hit))
    kw = dict(front=(-1.9, -1.15), backa=(-1.7, -1.2), legs=walk_legs(ph, 0.22), feet=G, y=G - 434 * SS + bob,
              alpha=alpha, blur=blur, ph=i, head=head + jolt, rot=0.04 + 0.5 * jolt * 0.2)
    if who == "ag":
        return agastya(cr, t, x, SS, mood=mood, pot=False, **kw)
    return sage(cr, t, who, x, SS, mood=mood, **kw)


def procession(cr, t, cx, mood="proud", walk=True, kick=0.0, alpha=1.0, blur=0.0, nh_front=(-0.5, -0.9),
               nh_hits=(), ag_mood="calm", ag_hit=None):
    """Four sages carrying the palanquin (facing right), Nahusha on it. Returns Nahusha's points."""
    bearer(cr, t, "shukra", cx + 330, 0, walk, alpha, blur)
    bearer(cr, t, "khag", cx - 330, 1, walk, alpha, blur)
    bob = -4 * abs(math.sin(2 * math.pi * 1.1 * t)) if walk else 0.0
    prop(cr, "nh_palki", cx, FLOOR + bob, PS, rot=0.01 * math.sin(t * 2.2) if walk else 0.0, alpha=alpha, blur=blur)
    pts = nahusha_seated(cr, t, cx - 30, HIP + bob, NS, mood=mood, front=nh_front, kick=kick, hits=nh_hits,
                         alpha=alpha, blur=blur)
    bearer(cr, t, "rishi", cx - 215, 2, walk, alpha, blur)
    bearer(cr, t, "ag", cx + 215, 3, walk, alpha, blur, mood=ag_mood, hit=ag_hit)
    return pts


# ------------------------------------------------------------------ the python


def crown_on(cr, tip, cen, w0, face, alpha=1.0):
    a = math.atan2(tip[1] - cen[1], tip[0] - cen[0])
    hs = w0 / RU.HEAD_W
    if face > 0:
        nx, ny, rot, fl = math.sin(a), -math.cos(a), a, False
    else:
        nx, ny, rot, fl = -math.sin(a), math.cos(a), a - math.pi, True
    prop(cr, "nh_crown", cen[0] + nx * 58 * hs, cen[1] + ny * 58 * hs, 0.8 * hs, rot=rot, alpha=alpha, flip=fl)


def python_rest(cr, t, cx, cy, R, w0, head_xy, face=1, talk=False, alpha=1.0, turns=1.6, stack=50, arch=0.0,
                rods=True):
    """The python coiled on the ground, its head reared up at head_xy, Nahusha's crown on its head."""
    sn = RS.snake(cr, t, RS.spine_coil(cx, cy, R, face, head_xy, turns=turns, stack=stack, arch=arch), w0, "old",
                  face=face, head="rr_snake_old_talk" if talk else None, alpha=alpha, rods=rods)
    if sn:
        crown_on(cr, sn[0], sn[1], w0, face, alpha)
    return sn


def head_at(cr, x, y, ang, w0, face, talk=False, alpha=1.0, crown=True):
    """The python's head with its neck joint at (x, y), pointing along ang (radians, screen)."""
    hs = w0 / RU.HEAD_W
    name = "rr_snake_old_talk" if talk else "rr_snake_old"
    if face > 0:
        prop(cr, name, x, y, hs, rot=ang, alpha=alpha)
    else:
        prop(cr, name, x, y, hs, rot=ang - math.pi, alpha=alpha, flip=True)
    tip = (x + 205 * hs * math.cos(ang), y + 205 * hs * math.sin(ang))
    cen = (x + 100 * hs * math.cos(ang), y + 100 * hs * math.sin(ang))
    if crown:
        crown_on(cr, tip, cen, w0, face, alpha)
    return tip, cen


def tube(cr, pts, widths, alpha=1.0):
    """A leather snake body strip along pts (screen), widths per point: grey-green back, pale belly, ink edges,
    punched holes; multiplied onto the cloth like the other leather."""
    n = len(pts)
    if n < 2 or alpha <= 0.01:
        return
    nn = []
    for i in range(n):
        a, b = pts[max(0, i - 1)], pts[min(n - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        ln = math.hypot(dx, dy) or 1.0
        nn.append((dy / ln, -dx / ln))
    L = [(p[0] - q[0] * w / 2, p[1] - q[1] * w / 2) for p, q, w in zip(pts, nn, widths)]
    Rr = [(p[0] + q[0] * w / 2, p[1] + q[1] * w / 2) for p, q, w in zip(pts, nn, widths)]
    In = [(p[0] + q[0] * w * 0.12, p[1] + q[1] * w * 0.12) for p, q, w in zip(pts, nn, widths)]
    w0 = max(widths)
    cr.push_group()
    pc.poly(cr, L + Rr[::-1])
    cr.set_source_rgb(*SN)
    cr.fill()
    pc.poly(cr, Rr + In[::-1])
    cr.set_source_rgb(*SNB)
    cr.fill()
    for edge in (L, Rr):
        cr.move_to(*edge[0])
        for p in edge[1:]:
            cr.line_to(*p)
        cr.set_source_rgb(*INK)
        cr.set_line_width(max(2.2, 0.065 * w0))
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        cr.stroke()
    pc.punch(cr, [(p[0] - q[0] * w * 0.2, p[1] - q[1] * w * 0.2) for i, (p, q, w) in enumerate(zip(pts, nn, widths))
                  if i % 3 == 1 and w > 0.35 * w0], max(1.6, 0.06 * w0))
    pat = cr.pop_group()
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source(pat)
    cr.paint_with_alpha(alpha)
    cr.restore()


def helix(cx, y0, y1, rx, ry, turns, n=140):
    """Points of a coil round a standing figure, from y0 (top) down to y1; each with True where it passes in front."""
    out = []
    for i in range(n + 1):
        u = i / n
        a = math.pi / 2 + 2 * math.pi * turns * u
        out.append((cx + rx * math.cos(a), y0 + (y1 - y0) * u + ry * math.sin(a), math.sin(a) >= 0))
    return out


def runs(hx, front):
    out, cur = [], []
    for x, y, f in hx:
        if f == front:
            cur.append((x, y))
        elif cur:
            out.append(cur + [(x, y)])
            cur = []
    if cur:
        out.append(cur)
    return out


class Wrap:
    """The python wound round a standing figure: call back() before drawing the figure and front() after it."""

    def __init__(self, cx, y0, y1, rx, w, u=1.0, head=None, tail_to=(980, G - 20), alpha=1.0, t=0.0, talk=False):
        k = 1 + 1.3 * (1 - ease(clamp(u)))
        self.hx = helix(cx, y0, y1, rx * k, 34 * k, 2.4)
        self.w, self.alpha, self.t, self.talk = w, alpha * clamp(u * 3), t, talk
        self.head = head              # (x, y, ang, face) of the head's neck joint
        self.tail_to = tail_to

    def back(self, cr):
        for r in runs(self.hx, False):
            tube(cr, r, [self.w] * len(r), self.alpha)
        x1, y1, _ = self.hx[-1]                                   # the tail leaves the bottom loop to the ground
        tx, ty = self.tail_to
        pts = [(x1 + (tx - x1) * u, y1 + (ty - y1) * u - 60 * math.sin(math.pi * u) + 10 * math.sin(self.t * 2 + 6 * u))
               for u in (i / 30 for i in range(31))]
        tube(cr, pts, [self.w * (1 - 0.85 * (i / 30) ** 1.3) for i in range(31)], self.alpha)

    def front(self, cr):
        for r in runs(self.hx, True):
            tube(cr, r, [self.w] * len(r), self.alpha)
        if self.head:
            hx, hy, ang, face = self.head
            x0, y0, _ = self.hx[0]                                    # the neck rises from the top loop
            c = (x0 + 0.2 * (hx - x0), hy + 0.7 * (y0 - hy) - 40)
            neck = [((1 - u) ** 2 * x0 + 2 * (1 - u) * u * c[0] + u * u * hx,
                     (1 - u) ** 2 * y0 + 2 * (1 - u) * u * c[1] + u * u * hy) for u in (i / 20 for i in range(21))]
            tube(cr, neck, [self.w * (1 + 0.15 * i / 20) for i in range(21)], self.alpha)
            return head_at(cr, hx, hy, ang, self.w * 1.15, face, self.talk, self.alpha)
        return None


# ------------------------------------------------------------------ sets


def sky(cr, t):
    glow(cr, 540, 860, 760, 0.7)
    for x, y, s_ in ((170, 560, 0.8), (900, 470, 0.7), (560, 1500, 1.0), (120, 1560, 0.8), (980, 1640, 0.9)):
        puffs(cr, x + 30 * math.sin(t * 0.3 + x), y, s_, 0.55)


def throne_set(cr, t, a=1.0):
    heaven(cr, t, alpha=a, gate=False)
    prop(cr, "md_throne", 540, G, 0.8, alpha=a)
    return G - 246 * 0.8                                         # the seated hip on the throne


def woods(cr, t, trees=((80, 0.62, 6, 0.7, True), (1020, 0.7, 4, 0.8, False))):
    forest(cr, t, feet=G, hut_x=None, trees=trees)


def bhima(cr, t, x, s, mood="calm", **kw):
    kw.setdefault("feet", G)
    return bhima_fig(cr, t, x, s, mood=mood, **kw)


def bubble_disc(cr, x, y, r, a, draw_inside):
    if a <= 0.01:
        return
    cr.save()
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*PARCH, 0.96 * a)
    cr.fill_preserve()
    cr.clip()
    draw_inside(cr)
    cr.restore()
    cr.new_path()
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.set_source_rgba(*INK, a)
    cr.set_line_width(6)
    cr.stroke()
    for k, (dx, dy, rr) in enumerate(((r * 0.75, r * 1.05, 26), (r * 0.98, r * 1.32, 16))):
        cr.new_path()
        cr.arc(x + dx, y + dy, rr, 0, 2 * math.pi)
        cr.set_source_rgba(*PARCH, 0.96 * a)
        cr.fill_preserve()
        cr.set_source_rgba(*INK, a)
        cr.set_line_width(4)
        cr.stroke()


def arrow(cr, x, y0, y1, p, col, w=26):
    """A thick arrow from y0 to y1 (drawn up to p 0..1)."""
    if p <= 0.01:
        return
    ye = y0 + (y1 - y0) * ease(p)
    d = 1 if y1 > y0 else -1
    cr.save()
    cr.set_source_rgba(*col, 0.9)
    cr.set_line_width(w)
    cr.move_to(x, y0)
    cr.line_to(x, ye - d * 40)
    cr.stroke()
    pc.poly(cr, [(x - 50, ye - d * 50), (x + 50, ye - d * 50), (x, ye + d * 20)])
    cr.fill()
    cr.restore()


# ------------------------------------------------------------------ the shots


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "nh1")
    tL, tA = c["L"], c["A"]
    glow(cr, 540, 1000, 720, 0.55)
    ground(cr, G, a=0.6)
    fade = 1 - prog(t, tA - 0.05, 0.25)
    if fade > 0.01:
        kick = keyed(t, [(0, 0.0), (tL - 0.22, 1.0), (tL + 0.6, 0.55)], 0.16)
        procession(cr, t, 480, mood="scold" if t > tL - 0.5 else "proud", walk=t < tL - 0.4, kick=kick, alpha=fade,
                   ag_mood="angry" if t > tL + 0.15 else "calm", ag_hit=tL)
    q = prog(t, tA - 0.05, 0.35)
    if q > 0.01:
        glow(cr, 560, G - 300, 420, 0.6 * q)
        python_rest(cr, t, 520, G - 130, 330, 96, (760, G - 560 + 10 * math.sin(t * 2)), face=1, alpha=q, stack=70)
    return dict(flash=max(flash_at(t, tL, 0.35), flash_at(t, tA, 0.7, 3.0)), night=0.1)


def s_name(cr, t, tl, t0, t1):
    c = cues(tl, "nh2")
    ground(cr, G, a=0.7)
    prop(cr, "mt_city", 560, G - 60, 0.8, alpha=0.75, blur=2)
    glow(cr, 520, G - 420, 460, 0.6)
    warm(cr, 520, G - 620, 300, 0.4 * prog(t, c["N"] - 0.1, 0.4))
    nahusha(cr, t, 520, 0.85, mood="smile" if t > c["M"] - 0.2 else "calm",
            front=keyed(t, [(0, (-0.32, -0.55)), (c["N"], (-1.9, -0.6))]), hits=[(c["N"], 0.4)], ph=0.3)
    return {}


def s_hide(cr, t, tl, t0, t1):
    c = cues(tl, "nh3")
    hip = throne_set(cr, t)
    x, bob, rock, ph = hop_walk(t, t0 + 0.2, c["C"] + 0.2, 560, 960, 0.42)
    a = 1 - prog(t, c["C"] - 0.1, 0.6)
    if a > 0.01:
        indra(cr, t, x, 0.7, feet=G, legs=walk_legs(ph), rot=rock, y=G - 434 * 0.7 + bob, alpha=a, blur=8 * (1 - a),
              head=0.15)
    prop(cr, "rr_lcloud", 960, G - 300, 1.3, alpha=0.95)

    def ui(cr_):
        qmark(cr_, t, c["K"] - 0.1, 540, hip - 330, 230)
    return dict(ui=ui)


def s_crown(cr, t, tl, t0, t1):
    c = cues(tl, "nh4")
    hip = throne_set(cr, t)
    u = ease(clamp((t - t0) / max(0.8, c["S"] - t0)))
    y = hip + (1 - u) * 900
    seated = u > 0.98
    if not seated:
        prop(cr, "rr_lcloud", 540, y + 160, 1.0, alpha=0.9)
    nahusha_seated(cr, t, 530, y, 0.8, mood="smile" if t < c["R"] else "proud", seat="nh_nahusha_seat",
                   front=(-1.3, -0.5) if t > c["I"] else (-0.5, -0.9), hits=[(c["I"], 0.4)])
    g = prog(t, c["S"] - 0.1, 0.5)
    if g > 0.01:
        aura(cr, t, 540, hip - 300, 120, 640, 0.35 * g, n=20, spin=0.08)
        lights(cr, t, 540, hip - 300, 300, 14, g)
    for x, fl, who in ((180, False, "md"), (900, True, None)):
        q = prog(t, c["N"] - 0.3, 0.5)
        if who:
            sage(cr, t, who, x, 0.62, feet=G, head=0.35, flip=fl, front=(-0.75, -1.85), backa=(-0.8, -1.8),
                 alpha=q, ph=0.4)
        else:
            ashvin(cr, t, x, 0.62, tool="md_lotus", feet=G, flip=fl, head=0.3, alpha=q, ph=1.1)
    return dict(flash=flash_at(t, c["S"], 0.2))


def s_pride(cr, t, tl, t0, t1):
    c = cues(tl, "nh5")
    hip = throne_set(cr, t)
    rg = prog(t, c["G"] - 0.2, 0.5)
    glow(cr, 540, hip - 300, 420, 0.5)
    if rg > 0.01:
        warm(cr, 540, hip - 320, 460, 0.5 * rg, col=(0.95, 0.25, 0.12))
    point = t > c["P"] - 0.2
    nahusha_seated(cr, t, 530, hip, 0.8, mood="laugh" if c["G"] - 0.2 < t < c["P"] - 0.2 else
                   ("scold" if point else "proud"), seat="nh_nahusha_seat",
                   front=(-1.65, -0.1) if point else (-0.5, -0.9), hits=[(c["P"], 0.5)], head=-0.08 * rg)
    q = prog(t, c["R"] - 0.3, 0.4)
    for k, (x, who) in enumerate(((880, "rishi"), (1000, "khag"))):
        sage(cr, t, who, x, 0.5, feet=G, flip=True, head=0.3, mood="shock", alpha=q, ph=k)
    return {}


def s_carry(cr, t, tl, t0, t1):
    c = cues(tl, "nh6")
    sky(cr, t)
    for i in range(4):                                     # clouds drifting past (the procession moves on)
        x = (1300 - (t * 160 + i * 380)) % 1600 - 260
        prop(cr, "rr_lcloud", x, G + 40 - 30 * (i % 2), 0.9, alpha=0.8)
    procession(cr, t, 540, mood="proud", walk=True)
    g = prog(t, c["K"] - 0.2, 0.4)
    if g > 0.01:
        for x in (325, 755):                                # the weight on the old shoulders
            glow(cr, x, POLE, 90, 0.5 * g)
    return {}


def s_sarpa(cr, t, tl, t0, t1):
    c = cues(tl, "nh7")
    sky(cr, t)
    for i in range(4):
        x = (1300 - (t * 160 + i * 380)) % 1600 - 260
        prop(cr, "rr_lcloud", x, G + 40 - 30 * (i % 2), 0.9, alpha=0.8)
    jab = [(c["S"], 0.6), (c["S"] + 0.45, 0.6)]
    procession(cr, t, 500, mood="scold" if t > c["J"] - 0.2 else "proud", walk=True,
               nh_front=(-1.55, -0.2) if t > c["J"] - 0.2 else (-0.5, -0.9), nh_hits=jab)
    return dict(flash=flash_at(t, c["S"], 0.12))


def s_kick(cr, t, tl, t0, t1):
    c = cues(tl, "nh8")
    tL = c["L"]
    sky(cr, t)
    rg = prog(t, c["G"] - 0.1, 0.5)
    kick = keyed(t, [(0, 0.0), (tL - 0.25, 0.15), (tL - 0.05, 1.0), (tL + 0.7, 0.5)], 0.14)
    pts = procession(cr, t, 480, mood="angry" if t > c["G"] - 0.1 else "scold", walk=t < c["G"] - 0.2, kick=kick,
                     ag_mood="angry" if t > tL + 0.2 else "calm", ag_hit=tL)
    if t > tL - 0.05 and "foot" in pts:
        fx, fy = pts["foot"]                               # user coordinates (nahusha_seated computes it)
        glow(cr, fx, fy, 160, 0.8 * (1 - prog(t, tL + 0.3, 0.5)))
    if rg > 0.01:
        warm(cr, 400, HIP - 200, 300, 0.4 * rg, col=(0.95, 0.25, 0.12))
    return dict(flash=flash_at(t, tL, 0.5, 3.0), night=0.1)


def s_curse(cr, t, tl, t0, t1):
    c = cues(tl, "nh9")
    tS, tK, tY = c["S"], c["K"], c["Y"]
    ground(cr, G, a=0.7)
    rg = prog(t, tS - 0.2, 0.5)
    warm(cr, 360, G - 600, 520, 0.6 * rg * (0.85 + 0.15 * math.sin(t * 6)), col=(0.95, 0.22, 0.10))
    glow(cr, 360, G - 600, 460, 0.4)
    raise_ = keyed(t, [(0, 0.0), (tS - 0.1, 1.0)], 0.25)
    agastya(cr, t, 360, 0.9, mood="angry", pot=False, feet=G,
            front=(-0.32 - 2.3 * raise_, -0.55 + 0.3 * raise_), hits=[(tS, 0.5), (tK, 0.4)], ph=0.2)
    sh = t > c["C"] - 0.2
    nahusha(cr, t, 850, 0.6, mood="shock" if sh else "angry", flip=True, front=(-1.2, -1.4) if sh else (-0.3, -0.5),
            rot=-0.05 * sh, ph=0.9)

    def ui(cr_):
        hcard(cr_, t, tK - 0.1, 600, 900, "सर्प", "= साँप!")
        if t > tY - 0.1:
            red_ring(cr_, 600, 880, 180, 130, prog(t, tY - 0.1, 0.4), 9)
    return dict(ui=ui, flash=max(flash_at(t, tS, 0.25), flash_at(t, tK, 0.2)), night=0.15)


def s_fall(cr, t, tl, t0, t1):
    c = cues(tl, "nh10")
    tA, tG = c["A"], c["G"]
    sky(cr, t)
    ground(cr, G, a=0.8)
    if t < tA:
        u = clamp((t - t0) / max(0.5, tA - t0))
        nahusha(cr, t, 540 + 40 * math.sin(t * 3), 0.6, mood="shock", y=380 + 520 * u * u, rot=1.6 * (t - t0),
                front=(-2.8, -0.2), backa=(-2.6, 0.2), legs=(0.4, -0.3), rods=False)
    else:
        u = ease(clamp((t - tA) / max(0.5, tG - tA)))
        cy = 900 + (G - 130 - 900) * u
        python_rest(cr, t, 540, cy, 320, 96, (760, cy - 430 + 10 * math.sin(t * 2)), face=1, stack=70,
                    rods=u > 0.95)
    if t > tG - 0.1:
        k = t - tG + 0.1
        for dx in (-380, -180, 200, 400):
            puffs(cr, 540 + dx * (1 + 0.6 * k), G - 40 - 40 * k, 0.7 + 0.4 * k, 0.7 * clamp(1.6 - k))
    return dict(flash=max(flash_at(t, tA, 0.8, 3.0), flash_at(t, tG, 0.25)))


def s_years(cr, t, tl, t0, t1):
    c = cues(tl, "nh11")
    woods(cr, t, trees=((860, 0.8, 0, 0.95, False),))
    cyc = (t - t0) * 0.7                                   # suns and moons racing over
    for k in range(2):
        u = (cyc + 0.5 * k) % 1.0
        x, y = 100 + 880 * u, 760 - 380 * math.sin(math.pi * u)
        prop(cr, "sun" if k == 0 else "moon", x, y, 0.14, rot=t, alpha=0.9 * math.sin(math.pi * u))
    python_rest(cr, t, 440, G - 120, 300, 88, (640, G - 380 + 6 * math.sin(t * 1.2)), face=1, stack=40, arch=-30)
    for i in range(8):                                     # leaves falling, year after year
        u = ((t - t0) * 0.35 + i / 8) % 1.0
        prop(cr, "lr_pleaf", 760 + 260 * math.sin(i * 1.7) + 80 * math.sin(u * 6 + i), 500 + 1200 * u, 0.35,
             rot=u * 6 + i, alpha=0.8 * math.sin(math.pi * u))
    return dict(night=0.25 + 0.2 * math.sin(cyc * 2 * math.pi))


def s_bhima(cr, t, tl, t0, t1):
    c = cues(tl, "nh12")
    woods(cr, t, trees=((80, 0.62, 6, 0.7, True),))
    python_rest(cr, t, 930, G - 110, 230, 74, (800, G - 330 + 5 * math.sin(t * 1.5)), face=-1, stack=30, rods=False)
    prop(cr, "tree", 1000, G + 10, 0.72, alpha=0.95)
    x, bob, rock, ph = hop_walk(t, t0, t0 + 2.6, -120, 420, 0.42)
    flex = t > c["T"] - 0.2
    bhima(cr, t, x, 0.74, mood="smile" if flex else "calm", legs=walk_legs(ph), rot=rock, y=G - 434 * 0.74 + bob,
          front=(-2.4, -1.2) if flex else (-0.32, -0.55), hits=[(c["T"], 0.5)], ph=0.2)
    return {}


BX, BS = 470, 0.76                     # Bhima wrapped: x, scale
B_HIP = G - 434 * BS


def wrapped(cr, t, tl, u=1.0, mood="angry", strain=0.0, head=None, x=BX, s=BS, flip=False, talk=False, alpha=1.0,
            tail_to=(1000, G - 20), free=0.0):
    hip = G - 434 * s
    wr = Wrap(x + 10, hip - 250 * s, G - 120, 150 * s, 62 * s / 0.76, u=u, head=head, tail_to=tail_to,
              alpha=alpha * (1 - free), t=t, talk=talk)
    wr.back(cr)
    jit = strain * 0.03 * math.sin(t * 23)
    arms = ((0.15, -0.2), (0.1, -0.15)) if free < 0.5 else ((-2.6, -0.6), (-2.4, -0.5))
    prop(cr, "mace", x + 260, G - 20, 0.6, rot=1.45, alpha=1.0)
    bhima(cr, t, x, s, mood=mood, mace=False, flip=flip, front=arms[0], backa=arms[1], rot=jit, ph=0.4,
          head=0.04 * math.sin(t * 7) * strain)
    return wr.front(cr)


def s_wrap(cr, t, tl, t0, t1):
    c = cues(tl, "nh13")
    woods(cr, t)
    u = clamp((t - c["A"] + 0.2) / max(0.8, c["J"] - c["A"] + 0.2))
    strain = prog(t, c["Z"] - 0.2, 0.3)
    wrapped(cr, t, tl, u=u, mood="hurt" if t > c["H"] - 0.2 else ("angry" if t > c["J"] - 0.2 else "shock"),
            strain=strain, head=(640, B_HIP - 330, math.pi - 0.25, -1))
    return dict(flash=flash_at(t, c["J"], 0.2))


def s_how(cr, t, tl, t0, t1):
    c = cues(tl, "nh14")
    woods(cr, t)
    wrapped(cr, t, tl, mood="hurt", strain=0.6, head=(640, B_HIP - 330, math.pi - 0.25, -1))

    def ui(cr_):
        qmark(cr_, t, c["K"] - 0.15, 860, 760, 260)
    return dict(ui=ui, night=0.3)


def s_boon(cr, t, tl, t0, t1):
    c = cues(tl, "nh15")
    woods(cr, t)
    talk = speaking(tl, t, "n23", "n24")
    wrapped(cr, t, tl, mood="hurt", strain=0.3, head=(640, B_HIP - 330, math.pi - 0.25, -1), talk=talk)
    q = prog(t, c["R"] - 0.3, 0.4)

    def inside(cr_):
        glow(cr_, 300, 980, 220, 0.8)
        agastya(cr_, t, 280, 0.36, mood="calm", pot=True, feet=1140, front=(-1.6, -0.3), rods=False, ph=0.5)
        g = prog(t, c["V"] - 0.2, 0.4)
        warm(cr_, 380, 950, 140, 0.9 * g)
        lights(cr_, t, 380, 960, 120, 10, g)

    def ui(cr_):
        bubble_disc(cr_, 300, 1000, 220, q, inside)
        p = prog(t, c["P"] - 0.1, 0.3)
        if p > 0.01:                                       # Bhima's strength draining away
            lvl = 1 - 0.95 * ease(clamp((t - c["P"]) / max(0.6, c["T"] - c["P"] + 0.4)))
            x0, y0, w_, h_ = 620, 900, 300, 46
            cr_.save()
            cr_.set_source_rgba(*PARCH, 0.95 * p)
            cr_.rectangle(x0 - 8, y0 - 8, w_ + 16, h_ + 16)
            cr_.fill()
            cr_.set_source_rgba(0.15, 0.55, 0.20, p)
            cr_.rectangle(x0, y0, w_ * lvl, h_)
            cr_.fill()
            cr_.set_source_rgba(*INK, p)
            cr_.set_line_width(5)
            cr_.rectangle(x0 - 8, y0 - 8, w_ + 16, h_ + 16)
            cr_.stroke()
            cr_.restore()
    return dict(ui=ui)


def s_iam(cr, t, tl, t0, t1):
    c = cues(tl, "nh16")
    glow(cr, 540, 1000, 700, 0.5)
    ga = prog(t, c["N"] - 0.2, 0.5)
    if ga > 0.01:                                          # Nahusha's ghost behind the python
        warm(cr, 360, 900, 380, 0.4 * ga)
        nahusha(cr, t, 330, 0.95, mood="proud", feet=G + 120, alpha=0.4 * ga, blur=3, rods=False, ph=0.8)
    talk = speaking(tl, t, "n25", "n26") or t > c["E"] - 0.05
    nk = [(1080, G + 40), (980, 1500), (860, 1260), (780, 1080)]
    tube(cr, nk, [150, 150, 150, 150])
    head_at(cr, 780, 1080 + 10 * math.sin(t * 1.8), math.pi - 0.2, 170, -1, talk=talk)
    return dict(flash=flash_at(t, c["E"], 0.35), night=0.3 * prog(t, c["A"] - 0.2, 0.4))


def s_yudh(cr, t, tl, t0, t1):
    c = cues(tl, "nh17")
    woods(cr, t, trees=((1040, 0.7, 4, 0.8, False),))
    talk = speaking(tl, t, "n28")
    turned = t > c["Y"] - 0.2
    head = (560, B_HIP - 300, math.pi - (0.15 if turned else 0.25), -1)
    wrapped(cr, t, tl, mood="hurt", strain=0.2, head=head, x=720, flip=True, talk=talk, tail_to=(1060, G - 20))
    x, bob, rock, ph = hop_walk(t, t0, t0 + 2.4, -150, 230, 0.42)
    yudh(cr, t, x, 0.72, mood="calm", flip=False, feet=G, legs=walk_legs(ph), rot=rock, y=G - 434 * 0.72 + bob,
         ph=0.3)
    return {}


def s_qa(cr, t, tl, t0, t1):
    c = cues(tl, "nh18")
    woods(cr, t, trees=((1040, 0.7, 4, 0.8, False),))
    talk = speaking(tl, t, "n29")
    wrapped(cr, t, tl, mood="hurt", strain=0.1, head=(620, B_HIP - 250, math.pi - 0.15, -1), x=780, s=0.66,
            flip=True, talk=talk, tail_to=(1070, G - 20))
    ans = t > c["S"] - 0.3
    yudh(cr, t, 250, 0.74, mood="smile" if ans else "calm", flip=False, feet=G,
         front=(-1.5, -0.4) if ans else (-0.32, -0.55), hits=[(c["S"], 0.4), (c["K"], 0.4)], ph=0.3)

    def ui(cr_):
        out = c["J"] - 0.2
        for k, (key, word, x, y) in enumerate((("S", "सच", 260, 1000), ("D", "दया", 540, 940), ("M", "माफ़ी", 820, 1000))):
            if t > c[key] - 0.1:
                g = prog(t, c[key] - 0.1, 0.3) * (1 - prog(t, out, 0.3))
                warm(cr_, x, y, 150, 0.8 * g)
            label(cr_, t, c[key] - 0.1, word, x=x, y=y, size=96, col=RED, t_out=out)
        label(cr_, t, c["J"] - 0.1, "जन्म", x=300, y=1000, size=110, t_out=t1 - 0.1)
        if t > c["J"] + 0.3:
            p = prog(t, c["J"] + 0.3, 0.3)
            cr_.save()
            cr_.set_source_rgba(*RED, 0.95)
            cr_.set_line_width(14)
            cr_.move_to(170, 1010)
            cr_.line_to(170 + 260 * p, 990)
            cr_.stroke()
            cr_.restore()
        label(cr_, t, c["K"] - 0.1, "काम", x=780, y=1000, size=110, col=RED, t_out=t1 - 0.1)
        if t > c["K"]:
            red_ring(cr_, 780, 1000, 190, 110, prog(t, c["K"], 0.4), 9)
    return dict(ui=ui)


def s_free(cr, t, tl, t0, t1):
    c = cues(tl, "nh19")
    tT, tB, tS = c["T"], c["B"], c["S"]
    woods(cr, t, trees=((1040, 0.7, 4, 0.8, False),))
    free = prog(t, tT, 0.7)
    g = prog(t, tT - 0.1, 0.4)
    glow(cr, 780, G - 400, 520, 0.7 * g)
    wrapped(cr, t, tl, mood="laugh" if t > tB else "hurt", strain=0.0, head=None if free > 0.5 else
            (620, B_HIP - 250, math.pi - 0.15, -1), x=780, s=0.66, flip=True, tail_to=(1070, G - 20), free=free)
    yudh(cr, t, 250, 0.74, mood="smile", flip=False, feet=G, front=(-0.75, -1.85), backa=(-0.8, -1.8), ph=0.3)
    if t > tT - 0.1:                                       # Nahusha's king form rises in gold
        u = ease(clamp((t - tT) / max(1.2, tS - tT + 0.6)))
        y = G - 150 - 480 * u
        aura(cr, t, 600, y - 300, 80, 420, 0.4 * g, n=16, spin=0.1)
        lights(cr, t, 600, y - 250, 220, 14, g)
        nahusha(cr, t, 600, 0.62, mood="smile", y=y - 434 * 0.62, front=(-0.75, -1.85), backa=(-0.8, -1.8),
                alpha=0.85 * g, blur=2, rods=False, ph=0.6)
    return dict(flash=flash_at(t, tT, 0.6, 3.0))


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "nh20")
    tG, tU = c["G"], c["U"]
    ground(cr, G, a=0.5)
    for i in range(14):                                    # the fold between the two halves
        y0 = 560 + 90 * i
        cr.move_to(540, y0)
        cr.line_to(540, y0 + 48)
    cr.set_source_rgba(0.25, 0.14, 0.05, 0.5)
    cr.set_line_width(6)
    cr.stroke()
    u1 = ease(clamp((t - t0 - 0.2) / max(1.0, tG - t0)))
    warm(cr, 270, 900 + 600 * u1, 260, 0.35, col=(0.95, 0.25, 0.12))
    nahusha(cr, t, 270, 0.45, mood="shock", y=700 + 650 * u1, rot=0.8 * u1, front=(-2.8, -0.2), backa=(-2.6, 0.2),
            rods=False)
    u2 = ease(clamp((t - tG) / max(1.0, tU - tG + 0.5)))
    g = prog(t, tG, 0.4)
    glow(cr, 810, 1400 - 650 * u2, 300, 0.7 * g)
    lights(cr, t, 810, 1300 - 650 * u2, 200, 10, g)
    nahusha(cr, t, 810, 0.45, mood="smile", y=1350 - 650 * u2, front=(-0.75, -1.85), backa=(-0.8, -1.8),
            alpha=g, rods=False, ph=0.6)

    def ui(cr_):
        arrow(cr_, 120, 900, 1500, prog(t, t0 + 0.3, 0.8), RED)
        arrow(cr_, 960, 1600, 900, prog(t, tG + 0.2, 0.8), (0.95, 0.70, 0.15))
        label(cr_, t, t0 + 0.2, "घमंड", x=270, y=1690, size=96, col=RED, t_out=t1 - 0.1)
        label(cr_, t, tU - 0.2, "समझ", x=810, y=1690, size=96, t_out=t1 - 0.1)
    return {"ui": ui}


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "nh21")
    tT, tS = c["T"], c["S"]
    ground(cr, G, a=0.7)
    glow(cr, 540, G - 300, 380, 0.6)
    bhima(cr, t, 280, 0.6, mood="smile", mace=True, front=(-2.4, -1.2), ph=0.2)
    yudh(cr, t, 800, 0.6, mood="smile", flip=True, feet=G, front=(-0.75, -1.85), backa=(-0.8, -1.8), ph=0.5)
    cards = ((280, "ताक़त?", "भीम", tT - 0.1), (800, "समझ?", "युधिष्ठिर", tS - 0.1))

    def ui(cr_):
        for cx, big, small, tc in cards:
            hcard(cr_, t, tc - 0.2, cx, 640, big, small)
        if t > tS + 0.3:
            n = int((t - tS - 0.3) / 0.9)
            k = n % 2
            red_ring(cr_, cards[k][0], 644, 230, 150, prog(t, tS + 0.3 + 0.9 * n, 0.35), 9)
    return dict(ui=ui, night=0.2)


# ------------------------------------------------------------------ labels


LABELS = {
    "nh1": [(0.25, "देवताओं का राजा", dict(y=330, size=90)),
            ("L", "एक लात!", dict(y=330, size=110, col=RED)),
            ("A", "अजगर!", dict(y=330, size=130, col=RED, under=True))],
    "nh2": [("N", "राजा नहुष", dict(y=330, size=120, col=RED)),
            ("M", "धरती का महान राजा", dict(y=330, size=84))],
    "nh3": [(0.1, "देवताओं का राजा छिप गया", dict(y=330, size=72)),
            ("K", "स्वर्ग: कोई राजा नहीं!", dict(y=330, size=84, col=RED))],
    "nh4": [("N", "नहुष: स्वर्ग का राजा", dict(y=330, size=84)),
            ("I", "इंसान, देवताओं पर राज!", dict(y=330, size=80, col=RED, under=True))],
    "nh5": [("G", "घमंड!", dict(y=330, size=120, col=RED)),
            ("P", "मेरी पालकी: ऋषि उठाएँगे", dict(y=330, size=76))],
    "nh6": [("B", "बूढ़े ऋषि, भारी पालकी", dict(y=330, size=84))],
    "nh7": [("S", "सर्प! सर्प!", dict(y=330, size=120, col=RED)),
            ("M", "सर्प = जल्दी चलो", dict(y=330, size=92, under=True))],
    "nh8": [("G", "गुस्से में...", dict(y=330, size=90)),
            ("L", "ऋषि के सिर पर लात!", dict(y=330, size=88, col=RED, under=True))],
    "nh9": [("S", "श्राप = बद्दुआ", dict(y=330, size=96, col=RED)),
            ("C", "सर्प सर्प चिल्लाता है?", dict(y=330, size=80)),
            ("K", "तो खुद सर्प बन जा!", dict(y=330, size=88, col=RED, under=True))],
    "nh10": [("A", "नहुष बना अजगर", dict(y=330, size=96, col=RED)),
             ("G", "धरती पर गिरा!", dict(y=330, size=100))],
    "nh11": [("S", "सालों तक, जंगल में...", dict(y=330, size=88))],
    "nh12": [("B", "भीम", dict(y=330, size=130, col=RED)),
             ("T", "सबसे ताक़तवर पांडव", dict(y=330, size=88, under=True))],
    "nh13": [("J", "जकड़ लिया!", dict(y=330, size=120, col=RED)),
             ("Z", "पूरा ज़ोर लगाया...", dict(y=330, size=90)),
             ("H", "हिल भी नहीं पाया!", dict(y=330, size=96, col=RED, under=True))],
    "nh14": [("T", "सबसे ताक़तवर पांडव...", dict(y=330, size=84)),
             ("K", "कैसे हार गया?", dict(y=330, size=110, col=RED))],
    "nh15": [("V", "ऋषि का वरदान", dict(y=330, size=96)),
             ("P", "पकड़ में आया = ताक़त गई", dict(y=330, size=76, col=RED, under=True))],
    "nh16": [("N", "मैं नहुष हूँ!", dict(y=330, size=120, col=RED)),
             ("K", "तुम्हारे खानदान का राजा", dict(y=330, size=80)),
             ("E", "खा जाऊँगा!", dict(y=330, size=120, col=RED, under=True))],
    "nh17": [("Y", "बड़ा भाई: युधिष्ठिर", dict(y=330, size=88)),
             ("J", "सही जवाब दो!", dict(y=330, size=110, col=RED))],
    "nh18": [("Q", "सबसे ऊँचा इंसान कौन?", dict(y=330, size=84, col=RED)),
             ("J", "जन्म से नहीं...", dict(y=330, size=90)),
             ("K", "अपने कामों से!", dict(y=330, size=100, col=RED, under=True))],
    "nh19": [("T", "श्राप टूट गया!", dict(y=330, size=110, col=RED)),
             ("S", "फिर से राजा, स्वर्ग की ओर", dict(y=330, size=76))],
    "nh20": [(0.1, "घमंड ने गिराया...", dict(y=330, size=92)),
             ("U", "समझ ने उठाया", dict(y=330, size=104, col=RED, under=True))],
    "nh21": [(0.05, "तो बताओ...", dict(y=300, size=90))],
}


def labels(cr, t, tl, bid, t1):
    specs = LABELS.get(bid, [])
    if not specs:
        return
    c = cues(tl, bid)
    starts = [c["t0"] + w if isinstance(w, (int, float)) else c[w] - 0.1 for w, _, _ in specs]
    if bid == "nh1":
        starts[0] = 0.25
    for i, (_, text, kw) in enumerate(specs):
        kw = dict(kw)
        t_out = kw.pop("out", None)
        if t_out is None:
            t_out = starts[i + 1] - 0.15 if i + 1 < len(starts) else t1 - 0.12
        label(cr, t, starts[i], text, t_out=t_out, **kw)


# ------------------------------------------------------------------ the cut list and the frame


HEAVEN = (1.0, 0.88, 0.62)
EARTH = (1.0, 0.80, 0.58)
FOREST = (0.86, 1.0, 0.78)
ANGER = (1.0, 0.55, 0.45)
NIGHT_BLUE = (0.55, 0.66, 1.0)
GOLDC = (1.0, 0.86, 0.58)
DUSK = (1.0, 0.62, 0.42)

SHOTS = [
    ("nh1", s_hook, dict(z=(1.2, 1.24), focus=(540, 1720), place=(DUSK, 0.35))),
    ("nh2", s_name, dict(z=(1.3, 1.34), focus=(520, 1760), place=(EARTH, 0.3))),
    ("nh3", s_hide, dict(z=(1.2, 1.24), focus=(600, 1760), place=(HEAVEN, 0.35))),
    ("nh4", s_crown, dict(z=(1.15, 1.2), focus=(540, 1760), place=(HEAVEN, 0.35))),
    ("nh5", s_pride, dict(z=(1.25, 1.3), focus=(580, 1760), place=(ANGER, 0.3))),
    ("nh6", s_carry, dict(z=(1.2, 1.24), focus=(540, 1720), place=(DUSK, 0.3))),
    ("nh7", s_sarpa, dict(z=(1.45, 1.5), focus=(470, 1500), place=(DUSK, 0.35))),
    ("nh8", s_kick, dict(z=(1.35, 1.4), focus=(560, 1550), place=(ANGER, 0.35))),
    ("nh9", s_curse, dict(z=(1.2, 1.25), focus=(540, 1760), place=(ANGER, 0.45))),
    ("nh10", s_fall, dict(z=(1.0, 1.03), focus=(540, 1150), place=(DUSK, 0.4))),
    ("nh11", s_years, dict(z=(1.2, 1.24), focus=(520, 1760), place=(FOREST, 0.35))),
    ("nh12", s_bhima, dict(z=(1.2, 1.24), focus=(560, 1760), place=(FOREST, 0.3))),
    ("nh13", s_wrap, dict(z=(1.3, 1.35), focus=(500, 1760), place=(FOREST, 0.35))),
    ("nh14", s_how, dict(z=(1.7, 1.75), focus=(500, 1280), place=(NIGHT_BLUE, 0.35))),
    ("nh15", s_boon, dict(z=(1.15, 1.2), focus=(480, 1760), place=(FOREST, 0.3))),
    ("nh16", s_iam, dict(z=(1.0, 1.05), focus=(620, 1100), place=(NIGHT_BLUE, 0.35))),
    ("nh17", s_yudh, dict(z=(1.2, 1.24), focus=(540, 1760), place=(FOREST, 0.3))),
    ("nh18", s_qa, dict(z=(1.1, 1.13), focus=(540, 1760), place=(GOLDC, 0.3),
                        frames=[(1.1, (540, 1760)), (1.18, (400, 1760)), (1.18, (680, 1760))])),
    ("nh19", s_free, dict(z=(1.1, 1.14), focus=(560, 1760), place=(GOLDC, 0.4))),
    ("nh20", s_callback, dict(z=(1.0, 1.03), focus=(540, 1200), place=(GOLDC, 0.35),
                              frames=[(1.0, (540, 1200)), (1.06, (540, 1150))])),
    ("nh21", s_end, dict(z=(1.0, 1.03), focus=(540, 1200), frames=[(1.0, (540, 1200))])),   # cards: stay wide
]


def shot_at(t, tl):
    cache = getattr(tl, "_nh_shots", None)
    if cache is None:
        starts = [0.0]
        for bid, _, _ in SHOTS[1:]:
            starts.append(max(T(tl, FIRST[bid]) - 0.12, starts[-1] + 0.5))
        cache = tl._nh_shots = starts
    k = 0
    for i, s in enumerate(cache):
        if t >= s:
            k = i
    return k, cache[k], cache[k + 1] if k + 1 < len(cache) else tl.total


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl)
    bid, fn, opt = SHOTS[k]
    z, (fx, fy) = camera_beats.camera(tl, t, t0, t1, opt)     # a new framing every line, no hold > 2.6 s
    cr.save()
    cr.translate(fx, fy)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    pc.screen(cr)
    out = fn(cr, t, tl, t0, t1) or {}
    if opt.get("place"):
        col, a = opt["place"]
        tint(cr, col, a)
    if out.get("ui"):
        out["ui"](cr)
    cr.restore()
    motes(cr, t)
    pc.lamp(cr, t, night=max(out.get("night", 0.0), opt.get("night", 0.0)), flash=out.get("flash", 0.0))
    labels(cr, t, tl, bid, t1)
    if k > 0 and t - t0 < 0.22:
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """Sparse sounds, most important first, at least SFX_MIN_GAP apart: a damaru as the king becomes a python in the
    hook, a hit on the kick, a conch on the curse, a hit as the coils close on Bhima, shimmer as the curse breaks, a
    bell on the closing question; dips before the kick and the fall."""
    c = {b: cues(tl, b) for b in CUES}
    t_end = min(c["nh21"]["S"], tl["n35"].end - 0.05)
    want = [(c["nh1"]["A"], "damaru", 0), (c["nh8"]["L"], "hit", 0), (c["nh19"]["T"], "shimmer", 0),
            (t_end, "bell", 0), (c["nh9"]["S"], "conch", 0), (c["nh13"]["J"], "hit", 0),
            (c["nh10"]["G"], "hit", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["nh8"]["L"] - 0.3, "dip", 0.5), (c["nh10"]["A"] - 0.3, "dip", 0.45)]
    kept = [(after_voice(tl, a), n, d) for a, n, d in kept]          # never over a spoken word
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]


def after_voice(tl, a):
    """A sound effect time moved out of any spoken line into the pause right after it, so no effect covers a word."""
    for b in tl.beats:
        if b.start - 0.15 <= a < b.end:
            return b.end + 0.06 if b.end + 1.0 < tl.total else max(0.0, b.start - 0.3)   # last line: just before it
    return a
