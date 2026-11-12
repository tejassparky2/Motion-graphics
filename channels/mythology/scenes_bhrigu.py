"""Scenes for videos/bhrigu.py: "A sage kicked Vishnu in the chest, and Vishnu pressed his feet" (Bhagavata Purana
10.89.1-19), in Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen,
two-tier headlines and rod-puppet motion as the earlier reels, with the cast from bhrigu_cast (Bhrigu, Lakshmi,
Adishesha, more faces for Vishnu, Brahma and Shiva) and the earlier casts (Vishnu and Parvati from shani_cast, Shiva
from shikhandi_cast, Brahma from six_cast_c, the other sages from ruru_cast, mandhata_cast and six_cast_a). Written so
a 5-year-old can follow it: every line has one shot that shows exactly what is said, in the order it is said, with one
big, short English headline per idea; the twist (Vishnu answering the kick with kindness) gets a slow build: he rises,
bows, speaks, then presses the sage's feet.

Respect: the gods, Lakshmi, Parvati and the sages with dignity. The kick is never slapstick: the sage turns into a
dark silhouette, the lamp dims, his foot touches the chest slowly in a soft white flash, and only a faint print is left
(the hook shows just that ghost of a sole on Vishnu's chest). Shiva's trident is only raised, straight up, never
pointed at anyone. Parvati kneels and calms him with dignity. Brahma's anger is a red flush that he swallows.

Every frame is a pure function of t. On-screen text is short English. Cues are words of the Hindi line with a fraction
fallback, in one table (CUES) that the scenes and sfx() both read, with minimum gaps so a fast voice can't bunch the
beats together; MISSES lists cue words not found (it stays empty for Hindi). Shot starts and cues are cached on the
timeline under this module's own names (_bg_shot_starts, _bg_cues). Hindi only: Kannada goes to scenes_bhrigu_yk.

Shot list (line: what is on the screen)
  bg1   HOOK, frame 0: Bhrigu seated on a rock, his foot held out; Vishnu, large and kneeling, presses it with his two
        front hands, the conch and chakra raised in the other two: A SAGE KICKED VISHNU... / HE PRESSED HIS FEET!
        (both on screen by 0.3 s); tags SAGE / VISHNU; on "laat" a soft white flash on his chest leaves the ghost
        of a sole there (ringed); on "ulta" a red arrow from the chest to the foot; on "dabaye" the pressing
        quickens, sparkles, the big line is underlined
  bg2   a palm-leaf book opens: A STORY FROM THE / BHAGAVATA PURANA, then AND IT'S A / TRUE STORY (ringed)
  bg3   sages arguing round a sacred fire (puffs of temper, pointing hands): ONE DAY, THE SAGES / ARGUED; three
        medallions pop up as each god is named (BRAHMA, VISHNU, SHIVA), each gets a red "?": THE THREE GODS: / WHO
        IS THE GREATEST?
  bg4   the others dim; Bhrigu steps forward, ringed and tagged: THE JOB WENT TO / BHRIGU RISHI; he turns, thinking;
        a card NO ANGER / = THE GREATEST: HIS TEST: / WHO STAYS CALM?
  bg5   Brahma on his lotus (tag BRAHMA); Bhrigu walks in and stands stiff, tags HIS FATHER / HIS SON: FIRST, TO
        BRAHMA: / HIS OWN FATHER; plaques BOW and WORDS pop up, each with a red X: NO BOW. / NO WORD.
  bg6   Brahma close, his three faces flush red, red glow, puffs of anger, a shake: BRAHMA GOT / ANGRY!; tag HIS SON
        on the sage; the red puffs fly back into his mouth, his faces calm, gold light: BUT HE SWALLOWED / HIS ANGER
  bg7   Kailash: Shiva (tag SHIVA), Parvati behind, the trident planted; the sage walks in: THEN, TO KAILASH: /
        SHIVA; Shiva smiles and comes forward, arms wide: SHIVA, HAPPY, CAME FOR / A WARM HUG
  bg8   the sage hops back, a hand up: BUT THE SAGE / STEPPED BACK; he shouts (a spiky cloud of red zig-zags),
        Shiva's arms drop: AND SHOUTED / INSULTS!
  bg9   red glow; Shiva raises his trident straight up: SHIVA GOT ANGRY, / TRIDENT RAISED!; Parvati (tag PARVATI MA)
        comes and kneels at his feet, holding them; the red turns to gold, the trident comes down: THEN PARVATI MA /
        CALMED HIM
  bg9q  QUESTION: NOW, ONLY ONE WAS LEFT: / VISHNU; three medallions, Brahma and Shiva crossed out, Vishnu's ringed;
        a big red "?" over the card WHAT WILL / HAPPEN THERE?; Bhrigu small, walking on
  bg10  Vaikuntha: Adishesha's coils and hood, Vishnu lying with his head in Lakshmi's lap, her hand on his shoulder
        (tag LAKSHMI MA), his chakra and conch floating over him, the head ringed on "god": VISHNU, HIS HEAD IN /
        LAKSHMI'S LAP, then VISHNU WAS / RESTING
  bg11  the sage walks in; the lamp dims and he becomes a silhouette; slowly his foot touches Vishnu's chest in a soft
        white flash: AND RIGHT ON HIS CHEST... / A KICK!; Lakshmi startled
  bg12  Vishnu rises and stands, calm, a soft gold light: VISHNU GOT UP... / NO ANGER!; he bows with joined hands,
        petals: INSTEAD, / HE BOWED
  bg13  Vishnu speaks (cloud I DIDN'T SEE / YOU COME): VISHNU SAID: / SORRY!; his hand toward the sage's foot
        (ringed), cloud YOUR FEET ARE / SO SOFT...: AND HE ASKED: / IS YOUR FOOT HURT?
  bg14  the hook's picture: Vishnu kneels and presses the sage's foot, gently, sparkles: WITH LOVE, / HE PRESSED HIS
        FEET
  bg15  the sage's face close, tears falling: THE SAGE'S EYES / FILLED WITH TEARS; back at the fire he tells the
        sages, a Vishnu medallion rises in gold: HE TOLD THE SAGES: / VISHNU IS THE GREATEST
  bg15c CALLBACK, the hook's picture again: the ghost sole flashes on his chest: KICKED IN THE CHEST... / HE PRESSED
        THE FEET
  bg16  THE SAGE'S TEST WAS... / RIGHT OR WRONG?; cards RIGHT TEST? / WRONG TEST?, a red ring alternating; Bhrigu
        and Vishnu small below, facing each other
"""
import math

import cairo

import bhrigu_cast as B
import mandhata_cast as M
import puppet_core as pc
import ruru_cast as RU
import shani_cast as S
import shikhandi_cast as SK
import six_cast_a as SA
import six_cast_c as C6
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, back, clamp, ease, prog
from puppet_core import W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_arjuna import card2, cloud_text
from scenes_hanuman_curse import anger_puffs, qmark
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, man_angles, motes, red_ring, walk_legs, woman_angles
from scenes_jayadratha import flash_at, tag, tint, to_user
from scenes_kaikeyi import ANJALI, card, fig
from scenes_lakshman_rekha import big_x, book, sparkle
from scenes_mandhata import aura, held, lights, local, mix, reach_arm, warm, yajna_fire
from scenes_ravana import head2
from scenes_ruru import held_grip, plate
from scenes_shani_ganesha import kailash, lady, red_glow
from shots import CUT_LEAD, MIN_SHOT, T

MISSES = set()                       # cue words not found in a line (falls back to fractions)
G = FEET + 120                       # the ground line of every set


def cue(tl, bid, word, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, word)
    except (KeyError, ValueError):
        MISSES.add((bid, word))
        return T(tl, bid, frac)


# Every cue of every line: (name, Hindi word, fraction fallback, ((after, min gap), ...)); "t0" = the line's start.
# Words are exact substrings of the Hindi lines (checked: MISSES stays empty).
CUES = {
    "bg1": (("R", "ऋषि", 0.12, (("t0", 0.3),)),
            ("V", "विष्णु", 0.3, (("R", 0.4),)),
            ("K", "लात", 0.45, (("V", 0.4),)),
            ("U", "उल्टा", 0.72, (("K", 0.8),)),
            ("P", "दबाए", 0.92, (("U", 0.5),))),
    "bg2": (("B", "भागवत", 0.15, (("t0", 0.2),)),
            ("S", "सच्ची", 0.6, (("B", 0.6),))),
    "bg3": (("A", "बहस", 0.25, (("t0", 0.3),)),
            ("B", "ब्रह्मा", 0.45, (("A", 0.6),)),
            ("V", "विष्णु", 0.55, (("B", 0.35),)),
            ("S", "शिव", 0.65, (("V", 0.35),)),
            ("G", "बड़ा", 0.85, (("S", 0.5),))),
    "bg4": (("B", "भृगु", 0.3, (("t0", 0.4),)),
            ("T", "सोचा", 0.5, (("B", 0.8),)),
            ("A", "ग़ुस्सा", 0.65, (("T", 0.4),)),
            ("G", "बड़ा", 0.92, (("A", 0.6),))),
    "bg5": (("B", "ब्रह्मा", 0.15, (("t0", 0.3),)),
            ("F", "पिता", 0.45, (("B", 0.6),)),
            ("N", "प्रणाम", 0.7, (("F", 0.8),)),
            ("W", "बोले", 0.92, (("N", 0.5),))),
    "bg6": (("A", "आया", 0.3, (("t0", 0.3),)),
            ("S", "बेटा", 0.5, (("A", 0.6),)),
            ("D", "पी", 0.85, (("S", 0.6),))),
    "bg7": (("S", "शिव", 0.2, (("t0", 0.3),)),
            ("H", "ख़ुश", 0.5, (("S", 0.8),)),
            ("L", "गले", 0.75, (("H", 0.5),))),
    "bg8": (("P", "पीछे", 0.2, (("t0", 0.2),)),
            ("B", "बुरा", 0.6, (("P", 0.7),))),
    "bg9": (("A", "ग़ुस्से", 0.12, (("t0", 0.2),)),
            ("T", "त्रिशूल", 0.25, (("A", 0.3),)),
            ("P", "पार्वती", 0.5, (("T", 1.0),)),
            ("F", "पकड़कर", 0.7, (("P", 0.6),)),
            ("C", "शांत", 0.9, (("F", 0.5),))),
    "bg9q": (("V", "विष्णु", 0.45, (("t0", 0.3),)),
             ("Q", "क्या", 0.75, (("V", 0.6),))),
    "bg10": (("L", "लक्ष्मी", 0.2, (("t0", 0.3),)),
             ("G", "गोद", 0.45, (("L", 0.5),)),
             ("R", "आराम", 0.75, (("G", 0.6),))),
    "bg11": (("S", "सीधे", 0.3, (("t0", 0.5),)),
             ("C", "छाती", 0.5, (("S", 0.4),)),
             ("K", "लात", 0.8, (("C", 0.5),))),
    "bg12": (("U", "उठे", 0.12, (("t0", 0.1),)),
             ("N", "नहीं", 0.4, (("U", 0.7),)),
             ("J", "झुककर", 0.65, (("N", 0.6),)),
             ("P", "प्रणाम", 0.85, (("J", 0.4),))),
    "bg13": (("M", "माफ़", 0.1, (("t0", 0.15),)),
             ("D", "देखा", 0.4, (("M", 0.6),)),
             ("P", "पैर", 0.55, (("D", 0.5),)),
             ("N", "नाज़ुक", 0.7, (("P", 0.4),)),
             ("C", "चोट", 0.85, (("N", 0.5),))),
    "bg14": (("L", "प्यार", 0.15, (("t0", 0.1),)),
             ("D", "दबाने", 0.7, (("L", 0.5),))),
    "bg15": (("A", "आँसू", 0.3, (("t0", 0.3),)),
             ("L", "लौटकर", 0.5, (("A", 0.8),)),
             ("K", "कहा", 0.7, (("L", 0.5),)),
             ("V", "विष्णु", 0.92, (("K", 0.5),))),
    "bg15c": (("C", "छाती", 0.1, (("t0", 0.15),)),
              ("K", "लात", 0.25, (("C", 0.3),)),
              ("B", "बदले", 0.6, (("K", 0.6),)),
              ("P", "दबाए", 0.9, (("B", 0.5),))),
    "bg16": (("I", "इम्तिहान", 0.3, (("t0", 0.3),)),
             ("R", "सही", 0.45, (("I", 0.3),)),
             ("W", "ग़लत", 0.65, (("R", 0.6),)),
             ("C", "कमेंट", 0.85, (("W", 0.5),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_bg_cues", None)
    if cache is None:
        cache = {}
        tl._bg_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, word, frac, cons in CUES[bid]:
            v = cue(tl, bid, word, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


# ------------------------------------------------------------------ small helpers


def ground(cr, y=G, alpha=1.0, blur=0.0):
    prop(cr, "ground", W / 2, y + 6, 0.82, alpha=alpha, blur=blur)


def soft_flash(cr, x, y, t, t_f, r=260, k=1.0):
    """A soft white flash of light at (x, y) (the touch of the kick): no rays, no sparks, just light."""
    u = t - t_f
    if u < 0 or u > 1.6:
        return
    a = k * math.exp(-2.6 * u) * clamp(u / 0.12)
    glow(cr, x, y, r * (1 + 0.5 * u), 0.9 * a)
    g = cairo.RadialGradient(x, y, 0, x, y, r * (0.6 + 0.4 * u))
    g.add_color_stop_rgba(0, 1.0, 1.0, 0.96, 0.85 * a)
    g.add_color_stop_rgba(1, 1.0, 1.0, 0.96, 0.0)
    cr.save()
    cr.set_source(g)
    cr.arc(x, y, r * (0.6 + 0.4 * u), 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def rim_silhouette(cr, fn, a, col=(0.07, 0.04, 0.03), rim=(1.0, 0.95, 0.84), w=5.0):
    """scenes_jayadratha.silhouette with a thin pale rim of lamp light round it, so a dark limb still reads where it
    crosses another puppet."""
    if a <= 0.01:
        return
    cr.push_group()
    fn(cr)
    pat = cr.pop_group()
    for k in range(8):
        ang = 2 * math.pi * k / 8
        cr.save()
        cr.translate(w * math.cos(ang), w * math.sin(ang))
        cr.set_source_rgba(*rim, 0.55 * a)
        cr.mask(pat)
        cr.restore()
    cr.save()
    cr.set_source_rgba(*col, a)
    cr.mask(pat)
    cr.restore()


def ghost_sole(cr, t, p, a, rot=-0.5, s=0.42):
    """The faint print of a sole on Vishnu's chest (the ghost of the kick)."""
    if a <= 0.01:
        return
    prop(cr, "bg_sole", p[0], p[1], s, rot=rot, alpha=0.32 * a)


def arrow(cr, p0, p1, p, alpha=1.0, w=12, bend=-80.0):
    """A red curved arrow from p0 toward p1, drawn to fraction p."""
    if p <= 0.01:
        return
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + bend
    pts = []
    for i in range(41):
        u = p * i / 40
        pts.append(((1 - u) ** 2 * p0[0] + 2 * u * (1 - u) * mx + u * u * p1[0],
                    (1 - u) ** 2 * p0[1] + 2 * u * (1 - u) * my + u * u * p1[1]))
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, col, k in ((w + 8, (1.0, 0.95, 0.82), 0.8), (w, RED, 0.95)):
        cr.move_to(*pts[0])
        for q in pts[1:]:
            cr.line_to(*q)
        cr.set_source_rgba(*col, k * alpha)
        cr.set_line_width(lw)
        cr.stroke()
    if p > 0.8:
        (ax, ay), (bx, by) = pts[-2], pts[-1]
        ang = math.atan2(by - ay, bx - ax)
        L = w * 2.6
        pc.poly(cr, [(bx + math.cos(ang) * L * 0.6, by + math.sin(ang) * L * 0.6),
                     (bx + math.cos(ang + 2.4) * L, by + math.sin(ang + 2.4) * L),
                     (bx + math.cos(ang - 2.4) * L, by + math.sin(ang - 2.4) * L)])
        cr.set_source_rgba(*RED, 0.95 * alpha)
        cr.fill()
    cr.restore()


def petals(cr, t, t0, x, y, w, n=10, a=1.0):
    """Gold and pink petals drifting down over (x, y) after t0."""
    if t < t0 or a <= 0.01:
        return
    for i in range(n):
        u = ((t - t0) * 0.35 + i / n) % 1.0
        px = x + w * (((i * 37) % 11) / 10 - 0.5) + 30 * math.sin(t * 1.6 + i)
        py = y - 300 + 600 * u
        col = (1.0, 0.62, 0.70) if i % 2 else (1.0, 0.80, 0.30)
        q = clamp((t - t0) / 0.5) * math.sin(math.pi * u) * a
        cr.save()
        cr.translate(px, py)
        cr.rotate(t * 2 + i)
        pc.ell(cr, 0, 0, 10, 5)
        cr.set_source_rgba(*col, 0.85 * q)
        cr.fill()
        cr.restore()


def zig_cloud(cr, t, t_in, x, y, s, flip=False, alpha=1.0):
    """The spiky shout cloud popping in at t_in, shaking a little."""
    q = back(clamp((t - t_in) / 0.25), 1.8)
    if q <= 0.01:
        return
    jx = 5 * math.sin(t * 37) * (t > t_in)
    prop(cr, "bg_shout", x + jx, y, s * (0.6 + 0.4 * q), rot=0.04 * math.sin(t * 23), alpha=clamp(q) * alpha,
         flip=flip)


def kick_angle(hip, target, s, flip, foot=(30.0, 400.0)):
    """legF angle that puts the foot (leg units) of a leg hinged at `hip` on `target` (screen)."""
    sg = -1 if flip else 1
    dx, dy = (target[0] - hip[0]) * sg / s, (target[1] - hip[1]) / s
    return math.atan2(dy, dx) - math.atan2(foot[1], foot[0])


# ------------------------------------------------------------------ medallions (the three gods)


MED_HEAD = {"brahma": ("c6_brahma_head", 0.62, 0.0, -150.0), "brahma_red": ("bg_brahma_head_red", 0.62, 0.0, -150.0),
            "vishnu": ("bg_vishnu_head_kind", 0.85, 20.0, -150.0), "shiva": ("bg_shiva_head_smile", 0.9, -4.0, -150.0)}


def medallion(cr, t, t_in, x, y, r, who, alpha=1.0, t_out=None):
    """A round parchment medallion with a god's head in it, popping in at t_in (r = its radius in px)."""
    q = back(clamp((t - t_in) / 0.35), 1.5)
    if t_out is not None:
        q *= 1 - prog(t, t_out, 0.25)
    a = clamp(q) * alpha
    if a <= 0.01:
        return
    s = r / 176 * q
    prop(cr, "bg_medal_face", x, y, s, alpha=a)
    name, hs, cx, cy = MED_HEAD[who]
    cr.save()
    cr.new_path()
    cr.arc(x, y, 150 * s, 0, 2 * math.pi)
    cr.clip()
    k = hs * s
    prop(cr, name, x - cx * k, y - cy * k + 18 * s, k, alpha=a)
    cr.restore()
    prop(cr, "bg_medal_rim", x, y, s, alpha=a)


# ------------------------------------------------------------------ puppets

BH_HEAD = {m: "bg_bhrigu_head" + ("" if m == "calm" else "_" + m) for m in B.BG_MOODS}
BH_BACK = (-0.45, -0.75)             # Bhrigu's back hand forward at his side, holding the staff upright


def bhrigu(cr, t, x, s, mood="calm", staff=True, feet=G, tilt=0.04, **kw):
    """Bhrigu standing (feet on `feet`), his bamboo staff upright in his back hand, its foot on the ground."""
    kw.setdefault("backa", BH_BACK)
    kw.setdefault("ph", 0.9)
    sw = dict(kw.pop("swap", None) or {})
    sw["bg_bhrigu_head"] = BH_HEAD[mood]
    if staff:
        probe = dict(kw, alpha=0.0, rods=False)
        pts = fig(cr, B.BHRIGU, "bg_bhrigu", t, x, s, swap=sw, feet=feet, **probe)
        hx, hy = to_user(cr, pts["handB"])
        sg = -1 if kw.get("flip") else 1
        prop(cr, "av_staff", hx + 4 * s * sg, feet + 4, s * 1.45, rot=tilt * sg, alpha=kw.get("alpha", 1.0),
             blur=kw.get("blur", 0.0))
    return fig(cr, B.BHRIGU, "bg_bhrigu", t, x, s, swap=sw, feet=feet, **kw)


def bhrigu_walk(cr, t, t0, t1, x0, x1, s, feet=G, t_in=None, **kw):
    """Bhrigu walking in rod-puppet steps (brought onto the cloth from away when t_in is given); returns (pts, x)."""
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, 0.45)
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    kw.setdefault("hits", [(t1, 1.0)])
    return bhrigu(cr, t, x, s * k, legs=walk_legs(ph, 0.26), rot=rock, y=feet - 434 * s * k + bob,
                  alpha=a * kw.pop("alpha", 1.0), blur=b + kw.pop("blur", 0.0), feet=feet, **kw), x


def bhrigu_seat(cr, t, x, hip, s, mood="shock", rock=True, alpha=1.0, blur=0.0, front=(-0.7, -0.9),
                backa=(-0.3, -0.6), head=0.0, hits=(), ph=0.9):
    """Bhrigu seated on a rock, his near leg stretched out (his foot held out); returns his points (device) plus
    'sole' and 'instep' (scene)."""
    if rock:
        prop(cr, "c6_rock", x - 110 * s, G + 8, 0.9, alpha=alpha, blur=blur)
    prop(cr, "bg_bhrigu_seat_ext", x, hip, s, alpha=alpha, blur=blur)
    ang = man_angles("bg_bhrigu", t, front, backa, head, (0.0, 0.0), hits, ph)
    pts = puppet(cr, B.BHRIGU, x, hip, s, bob_rot(t, ph, 0.004), False, ang, alpha, blur,
                 hide=("bg_bhrigu_legF", "bg_bhrigu_legB"), swap={"bg_bhrigu_head": BH_HEAD[mood]})
    pts = dict(pts)
    pts["sole"] = (x + B.EXT_SOLE[0] * s, hip + B.EXT_SOLE[1] * s)
    pts["instep"] = (x + B.EXT_INSTEP[0] * s, hip + B.EXT_INSTEP[1] * s)
    pts["toes"] = (x + B.EXT_TOES[0] * s, hip + B.EXT_TOES[1] * s)
    pts["heel"] = (x + B.EXT_HEEL[0] * s, hip + B.EXT_HEEL[1] * s)
    return pts


F2_UP = (-2.15, -0.75)                # Vishnu's upper arms: the chakra raised in front, the conch raised behind
B2_UP = (2.6, 0.5)


def emblem(sprite, arm, s, dy=170, lift=58.0, spin=0.0, alpha=1.0, blur=0.0):
    """extra= callback: the chakra / conch held upright just above a hand whose (upper, fore) angles are `arm`."""
    rot = -(arm[0] + arm[1])

    def fn(cr_):
        cr_.save()
        cr_.translate(4, dy)
        cr_.rotate(rot)
        cr_.translate(0, -lift)
        cr_.rotate(spin)
        cr_.scale(s, s)
        pc.paint_part(cr_, sprite, alpha, blur)
        cr_.restore()
    return fn


def vishnu(cr, t, x, s, mood="kind", front=(-0.32, -0.55), backa=(0.3, -0.25), f2=F2_UP, b2=B2_UP, head=0.0,
           legs=(0.0, 0.0), hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, feet=G, ph=0.7, y=None,
           kneel=False, emblems=True, upper=True, halo_a=0.0):
    """Vishnu (shani_cast's four-armed puppet) standing (feet on `feet`) or kneeling; f2 / b2 = the upper arms."""
    ang = man_angles("sg_vishnu", t, front, backa, head, legs, hits, ph)
    ang["sg_vishnu_armF2_up"] = f2[0] + 0.32 + sway(t, 0.02, 0.4, ph)
    ang["sg_vishnu_armF2_lo"] = f2[1] + 0.55
    ang["sg_vishnu_armB2_up"] = b2[0] - 0.30 + sway(t, 0.02, 0.45, ph + 1)
    ang["sg_vishnu_armB2_lo"] = b2[1] + 0.25
    hide = []
    r = rot + bob_rot(t, ph)
    if kneel:
        hy = feet - 250 * s if y is None else y
        prop(cr, "bg_vishnu_kneel", x, hy, s, r, alpha, blur, flip)
        hide += ["sg_vishnu_legF", "sg_vishnu_legB"]
    else:
        hy = feet - 434 * s if y is None else y
    if not upper:
        hide += ["sg_vishnu_armF2_up", "sg_vishnu_armF2_lo", "sg_vishnu_armB2_up", "sg_vishnu_armB2_lo"]
    if halo_a > 0.01:
        sg = -1 if flip else 1
        cx = x + sg * (-20 * s)
        cy = hy - 560 * s
        glow(cr, cx, cy, 520 * s + 120, 0.5 * halo_a * alpha)
        warm(cr, cx, cy, 420 * s, 0.45 * halo_a * alpha)
    ex = None
    if emblems and upper:
        ex = {"sg_vishnu_armF2_lo": emblem("sg_chakra", f2, 0.42, spin=t * 1.6, alpha=alpha, blur=blur),
              "sg_vishnu_armB2_lo": emblem("sg_conch", b2, 0.5, lift=40, alpha=alpha, blur=blur)}
    return puppet(cr, S.VISHNU, x, hy, s, r, flip, ang, alpha, blur, hide=hide,
                  swap={"sg_vishnu_head": "bg_vishnu_head_" + mood}, rods=rods, extra=ex)


LIE_ROT = -math.pi / 2 + 0.1         # Vishnu lying on his back, head to the left, a little raised


def lakshmi_sit(cr, t, x, hip, s, mood="open", front=(-0.6, -0.9), backa=(-0.3, -0.9), head=0.0, flip=False,
                alpha=1.0, blur=0.0, hits=(), ph=1.1):
    """Lakshmi seated (hip at `hip`), her lap forward."""
    r = bob_rot(t, ph, 0.006)
    prop(cr, "bg_lakshmi_body_sit", x, hip, s, r, alpha, blur, flip)
    ang = woman_angles("bg_lakshmi", t, front, backa, head, hits, ph)
    return puppet(cr, B.LAKSHMI, x, hip, s, r, flip, ang, alpha, blur, hide=("bg_lakshmi_body",),
                  swap={"bg_lakshmi_head": "bg_lakshmi_head" + ("" if mood == "open" else "_" + mood)}, rods=False)


def brahma(cr, t, x, ground_, s, mood="calm", front=(-0.7, -1.7), backa=(0.25, -1.0), flip=False, alpha=1.0,
           blur=0.0, glow_a=1.0, hits=(), rods=True, shake=0.0):
    """Brahma (six_cast_c) seated cross-legged on his lotus (the lotus on ground_), the Vedas in his back hand
    (scenes_kumbhakarna.brahma, with his flushed face for mood 'red')."""
    sg = -1 if flip else 1
    if glow_a > 0:
        glow(cr, x, ground_ - 420 * s, 620 * s + 160, 0.6 * glow_a * alpha)
        aura(cr, t, x, ground_ - 520 * s, 240 * s, 760 * s, 0.4 * glow_a * alpha, n=22, spin=0.05)
    prop(cr, "md_lotus", x + sg * 30 * s, ground_ - 165 * s, s * 1.5, rot=sway(t, 0.005, 0.3, 2.0), alpha=alpha,
         blur=blur, flip=flip)
    hy = ground_ - 165 * s - C6.SEAT_H * s + 10 * s
    jx = shake * 6 * math.sin(t * 41)
    prop(cr, "c6_brahma_seat", x + jx, hy, s, alpha=alpha, blur=blur, flip=flip)
    ang = man_angles("c6_brahma", t, front, backa, 0.0, (0.0, 0.0), hits, 0.8)
    sw = {"c6_brahma_body": "c6_brahma_body_sit"}
    if mood == "red":
        sw["c6_brahma_head"] = "bg_brahma_head_red"
    return puppet(cr, C6.BRAHMA, x + jx, hy, s, bob_rot(t, 0.8, 0.005) + shake * 0.02 * math.sin(t * 29), flip, ang,
                  alpha, blur, hide=("c6_brahma_legF", "c6_brahma_legB"), swap=sw,
                  extra={"c6_brahma_armB_lo": held("c6_veda", backa, 0.8, dy=160, alpha=alpha, blur=blur)}, rods=rods)


SH_FRONT = (-0.95, -0.85)            # Shiva's front hand before his chest, the trident upright in it
SH_RAISE = (-2.45, -0.5)             # the trident raised straight up


def shiva(cr, t, x, s, mood="smile", trident=False, **kw):
    """Shiva (shikhandi_cast) standing; mood calm | smile | shock | angry; trident = held in his front hand."""
    sw = {"sk_shiva_head": "sk_shiva_head" if mood == "calm" else "bg_shiva_head_" + mood}
    ex = None
    if trident:
        fr = kw.setdefault("front", SH_FRONT)
        ex = {"sk_shiva_armF_lo": held_grip("sg_trishul", fr, 1.2, 0.0, -115.0, kw.get("alpha", 1.0),
                                            kw.get("blur", 0.0))}
    kw.setdefault("feet", G)
    kw.setdefault("ph", 0.5)
    return fig(cr, SK.SHIVA, "sk_shiva", t, x, s, swap=sw, extra=ex, **kw)


def parvati(cr, t, x, s, mood="open", **kw):
    kw.setdefault("feet", G)
    return lady(cr, S.PARVATI, "sg_parvati", t, x, s, mood, **kw)


def parvati_kneel(cr, t, x, s, mood="open", front=(-1.0, -0.4), backa=(-0.8, -0.5), head=0.0, rot=0.0, flip=False,
                  alpha=1.0, blur=0.0, ph=0.4, hits=()):
    """Parvati kneeling (her knees on G), leaning forward by rot."""
    hip = G - B.KNEEL_H * s
    sg = -1 if flip else 1
    prop(cr, "bg_parvati_body_kneel", x, hip, s, rot * sg, alpha, blur, flip)
    ang = woman_angles("sg_parvati", t, front, backa, head, hits, ph)
    return puppet(cr, S.PARVATI, x, hip, s, rot * sg + bob_rot(t, ph, 0.006), flip, ang, alpha, blur,
                  hide=("sg_parvati_body",), swap={"sg_parvati_head": "sg_parvati_head" + ("" if mood == "open"
                                                                                           else "_" + mood)})


SAGES = {   # the other sages at the fire: rig, key, head per mood
    "khag": (RU.KHAG, "rr_khag", {"calm": "rr_khag_head_shock", "angry": "rr_khag_head_angry",
                                  "shock": "rr_khag_head_shock", "smile": "rr_khag_head_shock"}),
    "shukra": (SA.SHUKRA, "sx_shukra", {"calm": "sx_shukra_head", "angry": "sx_shukra_head_angry",
                                        "shock": "sx_shukra_head_shock", "smile": "sx_shukra_head_smile"}),
    "rishi": (RU.RISHI, "rr_rishi", {"calm": "rr_rishi_head", "angry": "rr_rishi_head_teach",
                                     "shock": "rr_rishi_head_shock", "smile": "rr_rishi_head_laugh"}),
    "md": (M.MDSAGE, "mdsage", {"calm": "mdsage_head", "angry": "mdsage_head", "shock": "mdsage_head",
                                "smile": "mdsage_head"}),
}


def sage(cr, t, who, x, s, mood="calm", **kw):
    rig, key, heads = SAGES[who]
    kw.setdefault("feet", G)
    return fig(cr, rig, key, t, x, s, swap={key + "_head": heads[mood]}, **kw)


# ------------------------------------------------------------------ the press (hook, bg14, callback)


PR_SAGE = (165, 1477, 0.68)          # Bhrigu seated: x, hip y, scale
PR_VIS = (548, 0.9)                  # Vishnu kneeling (facing left): x, scale


def press_set(cr, t, sage_mood="shock", vis_mood="kind", press=0.0, rate=2.2, hits=(), glow_a=0.6):
    """Bhrigu on his rock with his foot held out; Vishnu kneeling, pressing it between his two front hands (one at the
    toes, one at the heel, the sole between them; press 0..1 = how hard the hands knead); returns the ghost print's
    place on his chest and the foot (scene, and device for the ui)."""
    sx, shy, ss = PR_SAGE
    vx, vs = PR_VIS
    glow(cr, vx - 60, G - 640 * vs, 620, 0.42 * glow_a)
    warm(cr, vx - 40, G - 600 * vs, 520, 0.25 * glow_a)
    spts = bhrigu_seat(cr, t, sx, shy, ss, mood=sage_mood, front=(-1.1, -1.1), backa=(0.1, -0.25), ph=0.9)
    sole, toes, heel = spts["sole"], spts["toes"], spts["heel"]
    k = press * (0.5 + 0.5 * math.sin(t * rate * 2 * math.pi))
    k2 = press * (0.5 + 0.5 * math.sin(t * rate * 2 * math.pi + 2.2))
    vhip = G - 250 * vs
    fr = reach_arm(vx, vhip, vs, 26 * 1.1, (toes[0] + 16 + 5 * k, toes[1] + 4 + 8 * k), flip=True)
    ba = reach_arm(vx, vhip, vs, -14 * 1.1, (heel[0] + 18 + 5 * k2, heel[1] + 8 - 8 * k2), flip=True)
    vpts = vishnu(cr, t, vx, vs, mood=vis_mood, front=fr, backa=ba, f2=(-1.95, -0.95), flip=True, kneel=True,
                  head=0.12, hits=hits, ph=0.7, rods=True)
    ch = to_user(cr, vpts["chest"])
    sole_at = (ch[0] - 6, ch[1] + 20)                  # where the kick's ghost print sits on his chest
    return dict(sole_at=sole_at, foot=sole, sole_d=cr.user_to_device(*sole_at), foot_d=cr.user_to_device(*sole),
                sage_top_d=spts["top"], vis_top_d=vpts["top"])


# ------------------------------------------------------------------ bg1  hook


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "bg1")
    tR, tV, tK, tU, tP = c["R"], c["V"], c["K"], c["U"], c["P"]
    press = 0.45 + 0.55 * prog(t, tP - 0.1, 0.4)
    pts = press_set(cr, t, sage_mood="shock", vis_mood="kind", press=press, rate=1.4 + 0.8 * prog(t, tP, 0.3),
                    hits=[(tK, 0.25), (tP, 0.3)])
    sole_at, ft = pts["sole_at"], pts["foot"]
    ghost_sole(cr, t, sole_at, prog(t, tK, 0.25))
    soft_flash(cr, sole_at[0], sole_at[1], t, tK, 220)
    if t > tP - 0.1:
        lights(cr, t, ft[0] + 10, ft[1] - 30, 120, 7, 0.8 * prog(t, tP - 0.1, 0.4), (1.0, 0.8, 0.5), 0.6)
        sparkle(cr, ft[0] - 20, ft[1] - 70, 34 * (0.7 + 0.3 * math.sin(t * 6)), prog(t, tP, 0.3))
    sd, fd, st = pts["sole_d"], pts["foot_d"], pts["sage_top_d"]

    def ui(cr):
        head2(cr, t, "A SAGE KICKED VISHNU...", -1.0, "HE PRESSED HIS FEET!", 0.3, big_size=170, ghost=-1.0,
              under=tP)
        tag(cr, t, tR, "SAGE", max(st[0] - 20, 150), st[1] - 50, 34, t_out=tU)
        tag(cr, t, tV, "VISHNU", 910, 1130, 34, t_out=tU)
        if tK - 0.05 < t < tU + 0.4:
            red_ring(cr, sd[0], sd[1] - 10, 90, 110, prog(t, tK + 0.1, 0.35), 8, 1 - prog(t, tU + 0.1, 0.3))
        arrow(cr, (sd[0] - 30, sd[1] - 90), (fd[0] + 30, fd[1] - 100), prog(t, tU, 0.45),
              1 - prog(t, tP + 0.6, 0.4), bend=-130)
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.2) + flash_at(t, tK, 0.25) + flash_at(t, tP, 0.2))


# ------------------------------------------------------------------ bg2  a true story from the Bhagavata Purana


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "bg2")
    tB, tS = c["B"], c["S"]
    leaves = [(None, [("BHAGAVATA PURANA", 76, HEAD_FONT)], 0),
              (tS, [([("A TRUE STORY", RED)], 84, HEAD_FONT)], 0)]
    book(cr, t, 540, 980, 0.86, leaves, t_in=t0 + 0.05, t_open=tB, ring=(1, 0, 0, tS + 0.3))

    def ui(cr):
        if t < tS - 0.1:
            head2(cr, t, "A STORY FROM THE", t0 + 0.05, "BHAGAVATA PURANA", tB, big_size=200)
        else:
            head2(cr, t, "AND IT'S A", tS - 0.1, "TRUE STORY", tS + 0.05, big_size=240, under=tS + 0.4)
    return dict(ui=ui, flash=flash_at(t, tB, 0.25) + flash_at(t, tS, 0.2))


# ------------------------------------------------------------------ bg3 / bg4  the sages' fire; Bhrigu is chosen


FIRE_X = 540
CIRCLE = (("khag", 140, False, 0.3), ("shukra", 330, False, 1.4), ("bhrigu", 760, True, 0.9), ("md", 945, True, 2.1))
SAGE_S = 0.5
MEDS = ((230, "brahma", "BRAHMA"), (540, "vishnu", "VISHNU"), (850, "shiva", "SHIVA"))
MED_Y = 720


def argue(t, ph, a=1.0):
    """(front arm, head) of an arguing sage: the hand jabs forward now and then."""
    u = (t * 0.9 + ph) % 1.0
    jab = math.sin(math.pi * clamp(u / 0.35)) if u < 0.35 else 0.0
    return mix((-0.5, -0.8), (-1.55, -0.1), jab * a), 0.05 * jab * a


def fire_set(cr, t, t0, flare=0.0):
    prop(cr, "tree", 60, G + 10, 0.6, rot=sway(t, 0.006, 0.3), alpha=0.32, blur=10, flip=True)
    prop(cr, "tree", 1040, G + 10, 0.55, rot=sway(t, 0.006, 0.3, 1.0), alpha=0.3, blur=12)
    yajna_fire(cr, t, FIRE_X, G, 0.85, flare)
    ground(cr)


def circle(cr, t, t0, argue_a=1.0, dim=0.0, skip=(), moods=None, bh=None):
    """The sages round the fire (Bhrigu among them unless skipped); returns Bhrigu's points."""
    out = None
    for who, x, fl, ph in CIRCLE:
        if who in skip:
            continue
        fr, hd = argue(t, ph, argue_a)
        a, bl = 1 - 0.45 * dim, 3.0 * dim
        mood = (moods or {}).get(who, "angry" if argue_a > 0.5 else "calm")
        if who == "bhrigu":
            if bh is None:
                out = bhrigu(cr, t, x, SAGE_S, mood="stern" if argue_a > 0.5 else "calm", flip=fl, front=fr,
                             head=hd, ph=ph, alpha=a, blur=bl)
        else:
            sage(cr, t, who, x, SAGE_S, mood, flip=fl, front=fr, head=hd, ph=ph, alpha=a, blur=bl)
    return out


def s_debate(cr, t, tl, t0, t1):
    c = cues(tl, "bg3")
    tA, tB, tV, tS, tG = c["A"], c["B"], c["V"], c["S"], c["G"]
    fire_set(cr, t, t0, 0.3 * prog(t, tA, 0.3))
    circle(cr, t, t0, argue_a=0.4 + 0.6 * prog(t, tA - 0.2, 0.3))
    for who, x, fl, ph in CIRCLE:
        if t > tA:
            anger_puffs(cr, t + ph, x + (-1 if fl else 1) * 20, G - 690 * SAGE_S, prog(t, tA, 0.4) * 0.8)

    def ui(cr):
        if t < tB - 0.1:
            head2(cr, t, "ONE DAY, THE SAGES", t0 + 0.05, "ARGUED", tA, big_size=280)
        else:
            head2(cr, t, "THE THREE GODS:", tB - 0.1, "WHO IS THE GREATEST?", tG, big_size=190)
        for (x, who, label), tm in zip(MEDS, (tB, tV, tS)):
            medallion(cr, t, tm - 0.1, x, MED_Y, 118, who)
            plate(cr, t, tm, label, x, MED_Y + 150, 32)
            if t > tG:
                qmark(cr, t, tG + 0.1 * MEDS.index((x, who, label)), x + 92, MED_Y - 96, 120, RED)
    return dict(ui=ui, flash=flash_at(t, tB, 0.12) + flash_at(t, tV, 0.12) + flash_at(t, tS, 0.12) +
                flash_at(t, tG, 0.2))


BH_PICK = (600, 0.66)                # Bhrigu once chosen: x, scale


def s_pick(cr, t, tl, t0, t1):
    c = cues(tl, "bg4")
    tB, tT, tA, tG = c["B"], c["T"], c["A"], c["G"]
    fire_set(cr, t, t0)
    dim = prog(t, t0 + 0.1, 0.4)
    circle(cr, t, t0, argue_a=0.0, dim=dim, skip=("bhrigu",), moods={"khag": "calm", "shukra": "calm"})
    x0 = CIRCLE[2][1]
    u = ease(clamp((t - t0 - 0.1) / max(0.6, tB - t0 - 0.2)))
    x = x0 + (BH_PICK[0] - x0) * u
    s = SAGE_S + (BH_PICK[1] - SAGE_S) * u
    _, bob, rock, ph = hop_walk(t, t0 + 0.1, max(t0 + 0.7, tB - 0.1), 0, 1, 0.45)
    turn = t > tT - 0.1
    glow(cr, x, G - 600 * s, 520, 0.5 * prog(t, tB, 0.4))
    pts = bhrigu(cr, t, x, s, mood="stern" if turn else "calm", flip=not turn,
                 front=(-0.9, -2.4) if turn else (-0.4, -0.6), legs=walk_legs(ph, 0.26) if u < 1 else (0, 0),
                 rot=rock, y=G - 434 * s + bob, hits=[(tB, 0.4), (tT, 0.5)])
    top = pts["top"]
    rc = cr.user_to_device(x + 10, G - 470 * s)
    rk = cr.user_to_device(x + 200, G)[0] - cr.user_to_device(x, G)[0]

    def ui(cr):
        if t < tT - 0.1:
            head2(cr, t, "THE JOB WENT TO", t0 + 0.05, "BHRIGU RISHI", tB, big_size=240)
            if t > tB:
                red_ring(cr, rc[0], rc[1], rk * 0.95, rk * 2.1, prog(t, tB + 0.05, 0.4), 9)
        else:
            head2(cr, t, "HIS TEST:", tT - 0.1, "WHO STAYS CALM?", tA, big_size=220)
            card2(cr, t, tA - 0.15, 540, 820, 0.95, [("NO ANGER", 92, INK, -40, tA),
                                                      ("= THE GREATEST", 86, RED, 50, tG)])
        tag(cr, t, tB + 0.1, "BHRIGU RISHI", min(max(top[0], 260), 840), top[1] - 60, 38, t_out=tT - 0.2)
    return dict(ui=ui, flash=flash_at(t, tB, 0.2) + flash_at(t, tA, 0.15))


# ------------------------------------------------------------------ bg5 / bg6  Brahma, his own father


BR5 = (330, 0.8)                     # Brahma on his lotus: x, scale
BH5 = (850, 0.62)                    # Bhrigu before him


def brahma_set(cr, t):
    for i, (x, y, s) in enumerate(((150, 640, 0.7), (930, 560, 0.6), (820, 900, 0.45))):
        prop(cr, "cloud", x + 20 * math.sin(t * 0.3 + i), y, s, alpha=0.35, blur=6)
    glow(cr, 540, 1000, 700, 0.3)


def s_brahma(cr, t, tl, t0, t1):
    c = cues(tl, "bg5")
    tB, tF, tN, tW = c["B"], c["F"], c["N"], c["W"]
    brahma_set(cr, t)
    bx, bs = BR5
    bp = brahma(cr, t, bx, G, bs, flip=False, hits=[(tF, 0.3)])
    x, s = BH5
    t_stop = max(t0 + 0.8, tB + 0.2)
    pts, xx = bhrigu_walk(cr, t, t0 - 0.1, t_stop, 1150, x, s, t_in=t0 - 0.1, mood="stern", flip=True,
                          front=(-0.05, -0.1), ph=0.9)
    top = pts["top"]
    btag = cr.user_to_device(bx, 860)

    def ui(cr):
        if t < tN - 0.1:
            head2(cr, t, "FIRST, TO BRAHMA:", t0 + 0.05, "HIS OWN FATHER", tF, big_size=230)
        else:
            head2(cr, t, "NO BOW.", tN - 0.1, "NO WORD.", tW, big_size=260)
        tag(cr, t, tB + 0.1, "BRAHMA", btag[0], btag[1], 38, t_out=tF - 0.15)
        tag(cr, t, tF, "HIS FATHER", btag[0], btag[1], 38)
        tag(cr, t, tF + 0.3, "HIS SON", min(top[0], 900), top[1] - 70, 34)
        for k, (txt, tm, xx) in enumerate((("BOW", tN, 400), ("WORDS", tW, 700))):
            if t > tm - 0.1:
                plate(cr, t, tm - 0.1, txt, xx - 30, 700, 52)
                big_x(cr, xx + 18 * len(txt) + 30, 700, 64, 64, prog(t, tm + 0.1, 0.3), lw=11)
    return dict(ui=ui, flash=flash_at(t, tF, 0.15) + flash_at(t, tN, 0.15) + flash_at(t, tW, 0.15))


BR6 = (440, 0.98)
BH6 = (930, 0.5)


def s_angry(cr, t, tl, t0, t1):
    c = cues(tl, "bg6")
    tA, tS, tD = c["A"], c["S"], c["D"]
    red = prog(t, tA - 0.1, 0.3) * (1 - prog(t, tD + 0.5, 0.4))
    calm = prog(t, tD + 0.5, 0.5)
    bx, bs = BR6
    if red > 0.01:
        red_glow(cr, bx, G - 700 * bs, 700, 0.6 * red)
    glow(cr, bx, G - 700 * bs, 600, 0.5 * calm)
    shake = red * (1 - prog(t, tD, 0.3))
    bp = brahma(cr, t, bx, G, bs, mood="red" if (tA - 0.05 < t < tD + 0.55) else "calm", glow_a=0.4 + 0.6 * calm,
                shake=shake, front=mix((-0.7, -1.7), (-1.0, -2.2), calm), hits=[(tA, 0.3), (tD + 0.5, 0.3)])
    head = to_user(cr, bp["head"])
    mouth = (head[0], head[1] + 40)
    if tA < t < tD:
        anger_puffs(cr, t, head[0], head[1] - 290, prog(t, tA, 0.3))
        anger_puffs(cr, t + 0.4, head[0] - 120, head[1] - 230, 0.8 * prog(t, tA + 0.2, 0.3))
        anger_puffs(cr, t + 0.7, head[0] + 120, head[1] - 230, 0.8 * prog(t, tA + 0.3, 0.3))
    if tD - 0.05 < t < tD + 0.8:                         # the red puffs fly back into his mouth: swallowed
        for i in range(7):
            u = clamp((t - tD - 0.05 * i) / 0.45)
            if 0 < u < 1:
                a0 = 2 * math.pi * i / 7
                px = head[0] + 230 * math.cos(a0) * (1 - ease(u))
                py = head[1] - 200 + 230 * math.sin(a0) * 0.6 * (1 - ease(u)) + (mouth[1] - head[1] + 200) * ease(u)
                cr.new_path()
                cr.arc(px, py, 18 * (1 - u) + 6, 0, 2 * math.pi)
                cr.set_source_rgba(0.80, 0.10, 0.06, 0.8 * (1 - u))
                cr.fill()
    if t > tD + 0.5:
        lights(cr, t, head[0], head[1] - 100, 260, 8, 0.6 * calm)
    x, s = BH6
    pts = bhrigu(cr, t, x, s, mood="stern", flip=True, front=(-0.05, -0.1), ph=0.9)
    top = pts["top"]

    def ui(cr):
        if t < tD - 0.1:
            head2(cr, t, "BRAHMA GOT", t0 + 0.05, "ANGRY!", tA, big_size=300)
        else:
            head2(cr, t, "BUT HE SWALLOWED", tD - 0.1, "HIS ANGER", tD + 0.3, big_size=270)
        tag(cr, t, tS, "HIS SON", min(top[0], 920), top[1] - 70, 34)
    return dict(ui=ui, flash=flash_at(t, tA, 0.2) + flash_at(t, tD + 0.5, 0.2))


# ------------------------------------------------------------------ bg7 / bg8 / bg9  Kailash: Shiva and Parvati


SV7 = (360, 0.64)                    # Shiva: x, scale
PV7 = (120, 0.58)                    # Parvati behind him
BH7 = (870, 0.6)                     # the sage
TRI7 = 250                           # the trident planted in the ground


def kailash_set(cr, t, trident=True):
    kailash(cr, alpha=0.5, y=1330, s=0.66, blur=5.0)
    glow(cr, 540, 1150, 700, 0.25)
    ground(cr)
    if trident:
        prop(cr, "sg_trishul", TRI7, G - 420 * 0.62, 0.62, rot=sway(t, 0.004, 0.3))


HUG = ((-1.75, 0.15), (-1.35, -0.1))  # Shiva's arms open wide, forward and up (front, back)


def s_hug(cr, t, tl, t0, t1):
    c = cues(tl, "bg7")
    tS, tH, tL = c["S"], c["H"], c["L"]
    kailash_set(cr, t)
    px, ps = PV7
    parvati(cr, t, px, ps, mood="smile" if t > tH else "open", ph=0.4)
    sx, ss = SV7
    xx = keyed(t, [(t0, sx), (tL - 0.1, sx + 110)], 0.45, 1.2)
    walk = 0.3 * math.sin(math.pi * clamp((t - tL + 0.1) / 0.45)) * (t > tL - 0.1)
    op = keyed(t, [(t0, 0.0), (tL - 0.1, 1.0)], 0.35, 1.3)
    glow(cr, xx, G - 640 * ss, 520, 0.45 * prog(t, tH, 0.4))
    spts = shiva(cr, t, xx, ss, mood="smile" if t > tH - 0.1 else "calm", front=mix((-0.4, -0.6), HUG[0], op),
                 backa=mix((0.3, -0.3), HUG[1], op), legs=(-walk, walk), hits=[(tH, 0.3), (tL, 0.5)])
    stop = spts["top"]
    bx, bs = BH7
    bhrigu_walk(cr, t, t0 - 0.1, t0 + 1.1, 1180, bx, bs, t_in=t0 - 0.1, mood="stern", flip=True, front=(-0.1, -0.2))
    if t > tL:
        lights(cr, t, xx + 120, G - 520 * ss, 200, 7, 0.6 * prog(t, tL, 0.4), (1.0, 0.8, 0.5))

    def ui(cr):
        if t < tH - 0.1:
            head2(cr, t, "THEN, TO KAILASH:", t0 + 0.05, "SHIVA", tS, big_size=300)
        else:
            head2(cr, t, "SHIVA, HAPPY, CAME FOR", tH - 0.1, "A WARM HUG", tL, big_size=260, under=tL + 0.4)
        tag(cr, t, tS + 0.1, "SHIVA", max(stop[0], 240), stop[1] - 50, 38)
        tag(cr, t, tH + 0.2, "PARVATI MA", 200, 1060, 30)
    return dict(ui=ui, flash=flash_at(t, tS, 0.15) + flash_at(t, tL, 0.2))


def s_insult(cr, t, tl, t0, t1):
    c = cues(tl, "bg8")
    tP, tB = c["P"], c["B"]
    kailash_set(cr, t)
    px, ps = PV7
    parvati(cr, t, px, ps, mood="open" if t < tB else "speak", ph=0.4)
    sx, ss = SV7
    xx = sx + 110
    drop = prog(t, tB + 0.1, 0.35)
    shiva(cr, t, xx, ss, mood="smile" if t < tP else "shock", front=mix(HUG[0], (-0.4, -0.6), drop),
          backa=mix(HUG[1], (0.3, -0.3), drop), hits=[(tB + 0.1, 0.4)])
    bx, bs = BH7
    back_x = keyed(t, [(t0, bx), (tP, bx + 90)], 0.3, 1.4)
    jump = math.sin(math.pi * clamp((t - tP) / 0.3)) * (t > tP)
    shout = t > tB - 0.05
    talk = shout and int(t * 5) % 3 != 0
    pts = bhrigu(cr, t, back_x, bs, mood="shout" if talk else ("stern" if shout else "calm"), flip=True,
                 front=(-1.6, -0.6) if t > tP else (-0.1, -0.2), y=G - 434 * bs - 30 * jump, rot=0.1 * jump,
                 hits=[(tP, 0.6), (tB, 0.5)])
    hd = pts["head"]

    def ui(cr):
        if t < tB - 0.1:
            head2(cr, t, "BUT THE SAGE", t0 + 0.05, "STEPPED BACK", tP, big_size=250)
        else:
            head2(cr, t, "AND SHOUTED", tB - 0.1, "INSULTS!", tB + 0.05, big_size=300)
        zig_cloud(cr, t, tB, hd[0] - 230, hd[1] - 250, 0.75, flip=True)
    return dict(ui=ui, flash=flash_at(t, tP, 0.15) + flash_at(t, tB, 0.2))


SV9 = (370, 0.66)
PK9 = (590, 0.6)                     # Parvati kneeling before him, facing left


def s_trident(cr, t, tl, t0, t1):
    c = cues(tl, "bg9")
    tA, tT, tP, tF, tC = c["A"], c["T"], c["P"], c["F"], c["C"]
    calm = prog(t, tC - 0.1, 0.6)
    angry = prog(t, tA - 0.1, 0.3) * (1 - calm)
    kailash_set(cr, t, trident=False)
    sx, ss = SV9
    if angry > 0.01:
        red_glow(cr, sx, G - 700 * ss, 760, 0.55 * angry)
    glow(cr, sx, G - 640 * ss, 560, 0.5 * calm)
    up = keyed(t, [(t0, 0.0), (tT, 1.0), (tC, 0.0)], 0.35, 1.25)
    mood = "calm" if t > tC else ("angry" if t > tA - 0.1 else "shock")
    spts = shiva(cr, t, sx, ss, mood=mood, trident=True, front=mix(SH_FRONT, SH_RAISE, up), backa=(0.3, -0.3),
                 hits=[(tT, 0.5), (tC, 0.3)])
    hand = to_user(cr, spts["handF"])
    tip = (hand[0] + 8, hand[1] - 520 * ss * up - 40)
    if up > 0.6 and t < tC + 0.3:
        glow(cr, tip[0], tip[1], 260, 0.6 * angry)
        aura(cr, t, tip[0], tip[1], 40, 200, 0.5 * angry * clamp((up - 0.6) / 0.4), n=14, spin=0.6,
             col=(1.0, 0.45, 0.15))
    # Parvati: comes from behind him and kneels at his feet, holding them
    kx, ks = PK9
    if t < tP - 0.2:
        pass
    elif t < tF:
        x, bob, rock, _ = hop_walk(t, tP - 0.2, tF, -60, kx + 40, 0.42)
        b, k, a = depth(t, tP - 0.2, 0.4)
        parvati(cr, t, x, ks * k, mood="open", flip=False, y=G - 470 * ks + bob * 0.6 - (k - 1) * 300 * ks,
                rot=rock * 0.6, alpha=a, blur=b, front=(-0.6, -0.6))
    else:
        q = back(clamp((t - tF) / 0.3), 1.3)
        foot = (sx + 60 * ss, G - 20)
        fr = reach_arm(kx, G - B.KNEEL_H * ks, ks, 22, foot, flip=True)
        parvati_kneel(cr, t, kx, ks, mood="speak" if t < tC else "smile", front=fr, backa=(fr[0] + 0.2, fr[1]),
                      head=-0.15, rot=0.25 * clamp(q), flip=True, ph=0.4)
        if t > tF:
            lights(cr, t, sx + 80, G - 100, 120, 6, 0.6 * prog(t, tF, 0.4), (1.0, 0.85, 0.6))
    bx, bs = BH7
    lean = prog(t, tT, 0.3) * (1 - calm)
    pts = bhrigu(cr, t, bx + 60, bs, mood="shock" if t > tT else "stern", flip=True, rot=0.12 * lean,
                 front=(-1.2, -0.8) if lean > 0.3 else (-0.1, -0.2), hits=[(tT, 0.5)])
    ptop = cr.user_to_device(kx + 30, G - 640 * ks)

    def ui(cr):
        if t < tP - 0.1:
            head2(cr, t, "SHIVA GOT ANGRY,", t0 + 0.05, "TRIDENT RAISED!", tT, big_size=230)
        else:
            head2(cr, t, "THEN PARVATI MA", tP - 0.1, "CALMED HIM", tC, big_size=270, under=tC + 0.4)
        tag(cr, t, tF + 0.1, "PARVATI MA", min(ptop[0] + 40, 860), ptop[1] - 150, 34)
    return dict(ui=ui, flash=flash_at(t, tT, 0.25) + flash_at(t, tC, 0.2))


# ------------------------------------------------------------------ bg9q  and now: Vishnu?


def s_question(cr, t, tl, t0, t1):
    c = cues(tl, "bg9q")
    tV, tQ = c["V"], c["Q"]
    glow(cr, 540, 1150, 700, 0.3)
    ground(cr)
    pts, xx = bhrigu_walk(cr, t, t0 + 0.2, max(t0 + 1.4, tQ), 110, 380, 0.38, mood="stern")
    my = 1260
    medallion(cr, t, t0 + 0.05, 220, my, 100, "brahma_red")
    medallion(cr, t, t0 + 0.2, 860, my, 100, "shiva")
    medallion(cr, t, tV - 0.15, 540, my - 20, 130, "vishnu")

    def ui(cr):
        head2(cr, t, "NOW, ONLY ONE WAS LEFT:", t0 + 0.05, "VISHNU", tV, big_size=300)
        for x, tm in ((220, t0 + 0.4), (860, t0 + 0.55)):
            big_x(cr, x, my, 160, 160, prog(t, tm, 0.3), lw=14)
            plate(cr, t, tm + 0.1, "ANGRY", x, my + 130, 30)
        if t > tV:
            red_ring(cr, 540, my - 20, 148, 148, prog(t, tV + 0.1, 0.4), 9)
        qmark(cr, t, tQ - 0.1, 540, 720, 220, RED)
        card2(cr, t, tQ, 540, 950, 0.95, [("WHAT WILL", 80, INK, -44, tQ + 0.1), ("HAPPEN THERE?", 88, RED, 46,
                                                                                  tQ + 0.3)])
    return dict(ui=ui, flash=flash_at(t, tV, 0.15) + flash_at(t, tQ, 0.2), night=0.08)


# ------------------------------------------------------------------ bg10 / bg11  Vaikuntha: resting; the kick


SH10 = (660, 0.9)                   # Adishesha: x, scale (on the ground)
LK10 = 0.7                           # Lakshmi's scale
VS10 = 0.75                          # Vishnu's scale


def bed_top():
    x, s = SH10
    return G + B.SH_TOP * s


def vaikuntha(cr, t, dim=0.0):
    """The ocean of milk far behind, the glow of Vaikuntha, Adishesha's coils and hood."""
    glow(cr, 540, 1100, 760, 0.45 * (1 - dim))
    cr.save()
    for k in range(3):
        sh = 16 * math.sin(t * (0.5 + 0.12 * k) + k)
        prop(cr, "bg_milkA" if k % 2 == 0 else "bg_milkB", 540 + sh + (20 if k % 2 else -20), 1420 + 70 * k, 0.55,
             alpha=0.75 * (1 - 0.4 * dim), blur=3)
    cr.restore()
    x, s = SH10
    prop(cr, "bg_shesha", x, G + 4, s, rot=sway(t, 0.002, 0.25), alpha=1 - 0.35 * dim, blur=4 * dim)


def float_emblems(cr, t, x, y, a=1.0):
    """The chakra and the conch floating in a soft light over Vishnu as he rests."""
    if a <= 0.01:
        return
    for k, (sp, dx, sc) in enumerate((("sg_chakra", -70, 0.3), ("sg_conch", 90, 0.36))):
        yy = y + 10 * math.sin(t * 1.3 + k * 2)
        glow(cr, x + dx, yy, 150, 0.5 * a)
        prop(cr, sp, x + dx, yy, sc, rot=t * 1.2 if k == 0 else 0.15 * math.sin(t), alpha=a)


def lying(cr, t, mood="rest", lk_mood="down", hits=(), alpha=1.0, blur=0.0, lift=0.0, emblems=1.0, stroke=True):
    """Lakshmi seated at the head of the bed, Vishnu lying with his head in her lap, her hand on his head; returns
    (vishnu pts, lakshmi pts) (device)."""
    sx, ss = SH10
    top = bed_top()
    lx = sx - 340 * ss
    lhip = top - 34
    hx = lx + 120 * LK10 + 300 * VS10 + 20
    hy = top - 40 - 18 * lift
    rot = LIE_ROT + 0.012 * math.sin(t * 1.4) - 0.1 * lift
    head_at = local(hx, hy, VS10, rot, False, 60, -240)       # his shoulder, so his face stays clear
    st = 8 * math.sin(t * 2.2) if stroke else 0.0
    fr = reach_arm(lx, lhip, LK10, 22, (head_at[0] + st, head_at[1] - 24), flip=False)
    lp = lakshmi_sit(cr, t, lx, lhip, LK10, mood=lk_mood, front=fr, backa=(-0.4, -1.2), head=0.16,
                     alpha=alpha, blur=blur, hits=hits)
    ang = man_angles("sg_vishnu", t, (0.05, -0.1), (0.1, -0.1), -0.06, (0.04, -0.02), hits, 0.7)
    vp = puppet(cr, S.VISHNU, hx, hy, VS10, rot, False, ang, alpha, blur,
                hide=("sg_vishnu_armF2_up", "sg_vishnu_armF2_lo", "sg_vishnu_armB2_up", "sg_vishnu_armB2_lo"),
                swap={"sg_vishnu_head": "bg_vishnu_head_lie_" + mood}, rods=False)
    float_emblems(cr, t, hx, top - 260, emblems * alpha)
    return vp, lp


def s_rest(cr, t, tl, t0, t1):
    c = cues(tl, "bg10")
    tL, tG, tR = c["L"], c["G"], c["R"]
    vaikuntha(cr, t)
    vp, lp = lying(cr, t)
    head = vp["head"]
    ltop = lp["top"]
    petals(cr, t, t0 + 0.3, 600, 1200, 700, 10, 0.8)

    def ui(cr):
        if t < tR - 0.15:
            head2(cr, t, "VISHNU, HIS HEAD IN", t0 + 0.05, "LAKSHMI'S LAP", tG, big_size=230)
        else:
            head2(cr, t, "VISHNU WAS", tR - 0.15, "RESTING", tR, big_size=300)
        tag(cr, t, tL, "LAKSHMI MA", ltop[0] + 230, ltop[1] - 20, 32)
        if tG < t < tR + 0.6:
            red_ring(cr, head[0] - 10, head[1] - 10, 120, 90, prog(t, tG + 0.05, 0.4), 8, 1 - prog(t, tR + 0.3, 0.3))
    return dict(ui=ui, flash=flash_at(t, tG, 0.12) + flash_at(t, tR, 0.15))


def s_kick(cr, t, tl, t0, t1):
    c = cues(tl, "bg11")
    tS, tC, tK = c["S"], c["C"], c["K"]
    dimq = prog(t, tS, 0.4)
    vaikuntha(cr, t)
    awake = t > tK + 0.1
    vp, lp = lying(cr, t, mood="calm" if awake else "rest", lk_mood="speak" if awake else "down", hits=[(tK, 0.4)],
                   stroke=not awake)
    chest = to_user(cr, vp["chest"])
    s = 0.78
    xs = chest[0] + 270
    t_stop = max(t0 + 1.0, tS)
    x, bob, rock, ph = hop_walk(t, t0 - 0.1, t_stop, 1180, xs, 0.45)
    hip = (x + 16 * s * -1, G - 434 * s + bob)
    target = (chest[0] + 10, chest[1] - 6)
    kk = keyed(t, [(t0, 0.0), (tK - 0.45, 1.0), (tK + 0.6, 0.0)], 0.45, 1.05)
    lift = kick_angle(hip, target, s, True) * kk if t > tS else 0.0
    legs = (lift, 0.05 * kk) if t > t_stop else walk_legs(ph, 0.26)
    b, k, a = depth(t, t0 - 0.1, 0.5)
    sil = dimq

    def draw_sage(c_, alpha):
        return bhrigu(c_, t, x, s * k, mood="stern", flip=True, legs=legs, rot=rock - 0.08 * kk, alpha=alpha,
                      blur=b, y=G - 434 * s * k + bob, front=(0.2, -0.3), rods=sil < 0.5, staff=False,
                      backa=(0.25, -0.3))
    if sil < 1:
        draw_sage(cr, a * (1 - sil))
    if sil > 0:
        rim_silhouette(cr, lambda c_: draw_sage(c_, a), 0.92 * sil)
    soft_flash(cr, target[0], target[1], t, tK, 300, 1.3)
    if t > tK:
        ghost_sole(cr, t, (target[0], target[1] + 6), prog(t, tK, 0.3) * 1.4, rot=-0.9)
    tgt_d = cr.user_to_device(*target)

    def ui(cr):
        head2(cr, t, "AND RIGHT ON HIS CHEST...", t0 + 0.05, "A KICK!", tK, big_size=300)
        if tC < t < tK + 1.2:
            red_ring(cr, tgt_d[0], tgt_d[1], 110, 80, prog(t, tC, 0.4), 8, 1 - prog(t, tK + 0.8, 0.3))
    return dict(ui=ui, night=0.22 * dimq, lift=0.5, flash=flash_at(t, tK, 0.3))


# ------------------------------------------------------------------ bg12  he rose, no anger; he bowed


VX12 = (560, 0.7)
BX12 = (880, 0.6)


def s_rise(cr, t, tl, t0, t1):
    c = cues(tl, "bg12")
    tU, tN, tJ, tP = c["U"], c["N"], c["J"], c["P"]
    vaikuntha(cr, t, dim=prog(t, tU, 0.5))
    lakshmi_sit(cr, t, SH10[0] - 340 * SH10[1], bed_top() - 34, LK10, mood="open" if t < tN else "smile",
                front=(-1.0, -1.2), backa=(-0.4, -1.2), alpha=0.85, blur=2 * prog(t, tU, 0.5))
    vx, vs = VX12
    u = ease(clamp((t - tU) / 0.7))
    # from lying on the bed to standing on the ground before it
    x0, y0 = SH10[0] - 340 * SH10[1] + 120 * LK10 + 300 * VS10 + 20, bed_top() - 40
    x = x0 + (vx - x0) * u
    s = VS10 + (vs - VS10) * u
    y = y0 + (G - 434 * vs - y0) * u
    bow = keyed(t, [(t0, 0.0), (tJ, 1.0)], 0.4, 1.15)
    rot = LIE_ROT * (1 - u) + 0.2 * bow
    hands = mix((-0.5, -0.6), ANJALI["front"], bow)
    handb = mix((0.2, -0.3), ANJALI["backa"], bow)
    halo = prog(t, tN - 0.1, 0.5)
    vishnu(cr, t, x, s, mood="kind" if t > tU + 0.3 else "calm", front=hands, backa=handb, head=0.4 * bow,
           rot=rot, y=y, rods=u > 0.9, halo_a=halo, hits=[(tU + 0.7, 0.4), (tJ, 0.3)],
           legs=(0.0, 0.0))
    bx, bs = BX12
    bhrigu(cr, t, bx, bs, mood="shock" if t > tU + 0.3 else "stern", flip=True, front=(-0.2, -0.3))
    if t > tP - 0.1:
        petals(cr, t, tP - 0.1, 720, 1200, 600, 12, 1.0)
    if t > tN:
        lights(cr, t, x, G - 520 * vs, 300, 9, 0.5 * halo)

    def ui(cr):
        if t < tJ - 0.1:
            head2(cr, t, "VISHNU GOT UP...", t0 + 0.05, "NO ANGER!", tN, big_size=280)
        else:
            head2(cr, t, "INSTEAD,", tJ - 0.1, "HE BOWED", tJ + 0.05, big_size=300, under=tP)
    return dict(ui=ui, flash=flash_at(t, tN, 0.15) + flash_at(t, tJ, 0.15))


# ------------------------------------------------------------------ bg13  "sorry; is your foot hurt?"


VX13 = (330, 0.72)
BX13 = (840, 0.62)


def s_sorry(cr, t, tl, t0, t1):
    c = cues(tl, "bg13")
    tM, tD, tP, tN, tC = c["M"], c["D"], c["P"], c["N"], c["C"]
    glow(cr, 540, 1100, 700, 0.35)
    ground(cr)
    vx, vs = VX13
    talk = int(t * 4.5) % 3 != 0
    reach = keyed(t, [(t0, 0.0), (tP, 1.0)], 0.4, 1.2)
    bx, bs = BX13
    foot = (bx - 70 * bs, G - 20)
    fr = mix(ANJALI["front"], (-0.9, -0.3), reach)
    vishnu(cr, t, vx, vs, mood="speak" if talk else "kind", front=fr, backa=ANJALI["backa"] if reach < 0.5 else
           (0.2, -0.4), head=0.18 + 0.1 * reach, rot=0.06 + 0.05 * reach, halo_a=0.4, hits=[(tM, 0.3), (tP, 0.3)])
    pts = bhrigu(cr, t, bx, bs, mood="shock", flip=True, front=(-0.3, -0.5))
    foot = cr.user_to_device(*foot)

    def ui(cr):
        if t < tP - 0.1:
            head2(cr, t, "VISHNU SAID:", t0 + 0.05, "SORRY!", tM, big_size=300)
            cloud_text(cr, t, 640, 760, 0.78, [("I DIDN'T SEE", 64, INK, -34, tM + 0.3),
                                               ("YOU COME", 70, RED, 40, tD)], flip=False, t_in=tM + 0.2)
        else:
            head2(cr, t, "AND HE ASKED:", tP - 0.1, "IS YOUR FOOT HURT?", tC, big_size=200)
            cloud_text(cr, t, 640, 760, 0.78, [("YOUR FEET ARE", 62, INK, -34, tP),
                                               ("SO SOFT...", 74, RED, 40, tN)], flip=False, t_in=tP - 0.1)
            red_ring(cr, foot[0] + 10, foot[1] - 20, 90, 60, prog(t, tN, 0.4), 8)
    return dict(ui=ui, flash=flash_at(t, tM, 0.15) + flash_at(t, tC, 0.15))


# ------------------------------------------------------------------ bg14  he pressed the sage's feet


def s_press(cr, t, tl, t0, t1):
    c = cues(tl, "bg14")
    tL, tD = c["L"], c["D"]
    pts = press_set(cr, t, sage_mood="shock", vis_mood="kind", press=0.4 + 0.6 * prog(t, tD - 0.1, 0.4),
                    rate=1.6, hits=[(tD, 0.3)], glow_a=0.8)
    ft = pts["foot"]
    lights(cr, t, ft[0], ft[1] - 40, 160, 9, 0.8 * prog(t, tL, 0.4), (1.0, 0.75, 0.6), 0.6)
    petals(cr, t, tL, 420, 1300, 500, 8, 0.8)

    def ui(cr):
        head2(cr, t, "WITH LOVE,", t0 + 0.05, "HE PRESSED HIS FEET", tD, big_size=200, under=tD + 0.4)
    return dict(ui=ui, flash=flash_at(t, tD, 0.2))


# ------------------------------------------------------------------ bg15  tears; "Vishnu is the greatest"


def s_tears(cr, t, tl, t0, t1):
    c = cues(tl, "bg15")
    tA = c["A"]
    glow(cr, 760, 1100, 700, 0.5)
    warm(cr, 760, 1100, 520, 0.25, (0.55, 0.70, 1.0))
    s = 1.45
    hip_y = 1150 + 410 * s
    weep = t > tA - 0.1
    pts = bhrigu(cr, t, 470, s, mood="weep" if weep else "shock", staff=False, y=hip_y, feet=hip_y + 434 * s,
                 front=ANJALI["front"], backa=ANJALI["backa"], head=0.14, rods=False, ph=0.9)
    eye = to_user(cr, pts["head"])
    ex, ey = eye[0] + 36 * s, eye[1] - 4 * s
    if weep:
        for i in range(6):
            u = ((t - tA) / 1.1 + i / 6) % 1.0
            if t - tA - i * 0.18 > 0:
                prop(cr, "rr_tear", ex + 6 * math.sin(i), ey + 40 + 380 * u * u, 0.9, alpha=1 - u)

    def ui(cr):
        head2(cr, t, "THE SAGE'S EYES", t0 + 0.05, "FILLED WITH TEARS", tA, big_size=220)
    return dict(ui=ui, flash=flash_at(t, tA, 0.15))


def s_report(cr, t, tl, t0, t1):
    c = cues(tl, "bg15")
    tL, tK, tV = c["L"], c["K"], c["V"]
    fire_set(cr, t, t0, 0.3)
    rise = prog(t, tV - 0.1, 0.6)
    turn = prog(t, tK, 0.3)
    circle(cr, t, t0, argue_a=0.0, skip=("bhrigu",), moods={"khag": "shock" if t > tV else "calm",
                                                            "shukra": "smile" if t > tV else "calm",
                                                            "md": "calm"})
    x, s = 700, 0.62
    talk = tK < t and int(t * 4.5) % 3 != 0
    bhrigu(cr, t, x, s, mood="shout" if talk and t < tV else "joy", flip=True,
           front=mix((-0.4, -0.6), (-2.5, -0.4), turn), hits=[(tK, 0.4), (tV, 0.4)])
    my = 760 - 60 * rise
    if rise > 0.01:
        glow(cr, 540, my, 520, 0.7 * rise)
        aura(cr, t, 540, my, 150, 420, 0.6 * rise, n=20, spin=0.1)

    def ui(cr):
        head2(cr, t, "HE TOLD THE SAGES:", t0 + 0.05, "VISHNU IS THE GREATEST", tV, big_size=180, under=tV + 0.5)
        medallion(cr, t, tV - 0.1, 540, my, 150, "vishnu")
    return dict(ui=ui, flash=flash_at(t, tV, 0.3))


# ------------------------------------------------------------------ bg15c  the hook's picture again


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "bg15c")
    tC, tK, tB, tP = c["C"], c["K"], c["B"], c["P"]
    pts = press_set(cr, t, sage_mood="weep", vis_mood="kind", press=0.5 + 0.5 * prog(t, tP - 0.1, 0.4), rate=1.5,
                    hits=[(tK, 0.2), (tP, 0.3)], glow_a=0.8)
    sole_at, ft = pts["sole_at"], pts["foot"]
    ghost_sole(cr, t, sole_at, prog(t, tK, 0.25))
    soft_flash(cr, sole_at[0], sole_at[1], t, tK, 220)
    if t > tP - 0.1:
        lights(cr, t, ft[0] + 10, ft[1] - 30, 120, 7, 0.8 * prog(t, tP - 0.1, 0.4), (1.0, 0.8, 0.5), 0.6)
    sd, fd = pts["sole_d"], pts["foot_d"]

    def ui(cr):
        head2(cr, t, "KICKED IN THE CHEST...", t0 + 0.05, "HE PRESSED THE FEET", tP, big_size=200, under=tP + 0.4)
        if t > tC:
            red_ring(cr, sd[0], sd[1] - 10, 90, 110, prog(t, tC + 0.1, 0.35), 8, 1 - prog(t, tB, 0.3))
        arrow(cr, (sd[0] - 30, sd[1] - 90), (fd[0] + 30, fd[1] - 100), prog(t, tB, 0.45), 1.0, bend=-130)
    return dict(ui=ui, flash=flash_at(t, tK, 0.2) + flash_at(t, tP, 0.2))


# ------------------------------------------------------------------ bg16  the test: right or wrong?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "bg16")
    tI, tR, tW, tC = c["I"], c["R"], c["W"], c["C"]
    glow(cr, 540, 1420, 520, 0.45)
    ground(cr)
    bhrigu(cr, t, 300, 0.52, mood="stern", front=(-0.6, -0.9), hits=[(tR, 0.4)])
    vishnu(cr, t, 790, 0.52, mood="kind", flip=True, front=ANJALI["front"], backa=ANJALI["backa"], halo_a=0.4,
           hits=[(tW, 0.4)])
    cards = ((300, "RIGHT TEST?", tR), (780, "WRONG TEST?", tW))

    def ui(cr):
        head2(cr, t, "THE SAGE'S TEST WAS...", t0 + 0.05, "RIGHT OR WRONG?", tI, big_size=230)
        for cx, txt, tc in cards:
            card(cr, t, tc - 0.25, cx, 760, 0.6, [(txt, 96, RED, 4)])
        if t > tR:
            if t < tW:
                k, ts = 0, tR
            else:
                n = int((t - tW) / 0.9)
                k, ts = (1 + n) % 2, tW + 0.9 * n
            red_ring(cr, cards[k][0], 764, 250, 92, prog(t, ts, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tR, 0.15))


SHOTS = [   # (line, cue: None = line start, else a CUES name; draw function, options)
    ("bg1", None, s_hook, {"z": (1.14, 1.18), "focus": (400, 1770)}),
    ("bg2", None, s_book, {"z": (1.0, 1.03)}),
    ("bg3", None, s_debate, {"z": (1.0, 1.03)}),
    ("bg4", None, s_pick, {"z": (1.0, 1.03)}),
    ("bg5", None, s_brahma, {"z": (1.0, 1.03)}),
    ("bg6", None, s_angry, {"z": (1.0, 1.04)}),
    ("bg7", None, s_hug, {"z": (1.0, 1.03)}),
    ("bg8", None, s_insult, {"z": (1.0, 1.04)}),
    ("bg9", None, s_trident, {"z": (1.0, 1.03)}),
    ("bg9q", None, s_question, {"z": (1.0, 1.03)}),
    ("bg10", None, s_rest, {"z": (1.0, 1.03)}),
    ("bg11", None, s_kick, {"z": (1.0, 1.04)}),
    ("bg12", None, s_rise, {"z": (1.0, 1.03)}),
    ("bg13", None, s_sorry, {"z": (1.0, 1.03)}),
    ("bg14", None, s_press, {"z": (1.06, 1.12), "focus": (400, 1770)}),
    ("bg15", None, s_tears, {"z": (1.0, 1.04), "focus": (540, 1150)}),
    ("bg15", "L", s_report, {"z": (1.0, 1.03)}),
    ("bg15c", None, s_callback, {"z": (1.14, 1.18), "focus": (400, 1770)}),
    ("bg16", None, s_end, {"z": (1.0, 1.03)}),
]


def _starts(tl):
    """Each shot's start (cached on the timeline under this module's own name, not shots.shot_at's)."""
    st = getattr(tl, "_bg_shot_starts", None)
    if st is None:
        st = []
        for k, (bid, cu, _, _) in enumerate(SHOTS):
            if k == 0:
                st.append(0.0)
                continue
            if cu is None:
                s = T(tl, bid)
            else:
                s = cues(tl, bid)[cu] - CUT_LEAD
            st.append(max(s, st[-1] + MIN_SHOT))
        tl._bg_shot_starts = st
    return st


def shot_at(t, tl):
    st = _starts(tl)
    k = max(i for i, s in enumerate(st) if t >= s)
    return k, st[k], st[k + 1] if k + 1 < len(st) else tl.total


def title_glow(cr, a):
    """In the dimmed shots, the small lamp over the title stays lit so the headline reads."""
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
    title_glow(cr, out.get("lift", 0.0) * out.get("night", 0.0) / 0.42)
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a soft
    hit as the foot touches Vishnu's chest, shimmer as Vishnu presses the sage's feet, a bell on the closing question,
    then (only where they fit) a conch as Shiva raises his trident, a conch on "Vishnu is the greatest" and shimmer
    as Brahma swallows his anger. Chosen in THAT order of importance, each at least SFX_MIN_GAP from every sound
    already kept (as render_myth.calm_sfx keeps them), so the list returned is what plays (about 6 sounds); the bed
    dips before the kick, the trident and the pressing of the feet."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["bg11"]["K"], "hit", 0), (c["bg14"]["D"], "shimmer", 0),
            (c["bg16"]["I"], "bell", 0), (c["bg9"]["T"], "conch", 0), (c["bg15"]["V"], "conch", 0),
            (c["bg6"]["D"], "shimmer", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["bg11"]["K"] - 0.35, "dip", 0.5), (c["bg9"]["T"] - 0.3, "dip", 0.45),
            (c["bg14"]["D"] - 0.3, "dip", 0.5)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
