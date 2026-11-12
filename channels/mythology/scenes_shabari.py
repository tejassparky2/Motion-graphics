"""Scenes for videos/shabari.py: "Shabari's tasted berries are in neither Valmiki's Ramayana nor Tulsidas's
Ramcharitmanas" (Valmiki Ramayana, Aranya Kanda 74; Ramcharitmanas, Aranya Kand, doha 34), in Togalu Gombeyaata
(Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen, two-tier headlines and rod-puppet
motion as the earlier reels, a myth-bust in the manner of the Lakshman Rekha reel (its red stamp, its palm-leaf books),
with the cast from shabari_cast. Every line has one shot that shows exactly what is said, in the order it is said,
one big, short English headline per idea, so a 5-year-old can follow it without sound; the real miracle gets a slow
reveal (the lamp dims, the Valmiki book glows, then the flowers).

Respect: Shabari, Rama and the sages with dignity; the belief is treated gently (Rama's love for her is in both books).
No fire is shown at her end: she becomes a soft light that rises to her gurus' lights.

Every frame is a pure function of t. On-screen text is short English. Cues are words of the Hindi line with a fraction
fallback, in one table (CUES) that the scenes and sfx() both read, with minimum gaps so a fast voice can't bunch the
beats together. Shot starts and cues are cached on the timeline under this module's own names (_sb_shot_starts,
_sb_cues). Hindi only (Kannada is routed to scenes_shabari_yk).

Shot list (line: what is on the screen)
  sb1   HOOK, frame 0: Shabari large and alone, holding out a bitten berry, her basket of berries at her side:
        SHABARI'S TASTED BERRIES? and the red stamp NOT IN / VALMIKI slammed on at 0.3 s; her name plate; on "joothe"
        the bitten berry is ringed (TASTED FIRST?); on "Ram" she holds it out further, glowing; on "pyaar" little
        lights rise round it; on "kahani" a leaf names THE VALMIKI RAMAYANA; on "Valmiki" the stamp slams again; on
        "nahin" a red X over the berry
  sb2   two book covers drop in, each with a bunch of berries in its medallion: VALMIKI RAMAYANA (a red X over the
        berries), then TULSIDAS RAMCHARITMANAS (red X): TASTED BERRIES? / NOT IN VALMIKI, then NOT IN EITHER BOOK
  sb3   Shabari alone sweeping (dust puffs), plate SHABARI; the forest and the hermitage hut come up: A SIMPLE /
        FOREST WOMAN; two old sages appear, seated (THE SAGES); she brings them water: SHE SERVED SOME / OLD SAGES
  sb4   the sage speaks to her (she listens, hands joined); a thought bubble: Rama walking down a path: THE SAGES
        SAID: / RAMA WILL COME!, then WAIT FOR HIM!
  sb5   the sages become soft light and rise to the sky: THEN THE SAGES WENT TO / HEAVEN; Shabari alone, head
        bowed, the light dims: SHABARI WAS LEFT / ALL ALONE
  sb6   the path; Shabari with her stick shading her eyes, watching it; sun and moon racing over, YEAR 1, 2, ...
        flipping: FOR YEARS AND YEARS / SHE WAITED; berries pop into her basket one by one: SHE KEPT FRUITS / FOR
        RAMA
  sb7   dawn: THEN ONE / DAY...; Rama walks in along the path, searching (plate LOOKING FOR SITA MATA): RAMA REALLY /
        CAME!, a burst of light, Shabari's joy
  sb8   she kneels and bows to touch his feet (he blesses her): SHE TOUCHED HIS / FEET; offers a water pot: SHE GAVE
        HIM / WATER...; then the full basket she gathered: ...AND / FRUITS; Rama smiles and takes one
  sb8q  question card under a big red "?": DID SHE TASTE / THEM FIRST?; Shabari small, a berry in her hand, waiting
  sb9   the Valmiki palm-leaf book opens; a magnifying glass finds only "I GATHERED / FOREST FRUITS / FOR YOU" (ringed):
        VALMIKI SAYS: / SHE GATHERED FRUITS; the glass searches the leaves: VALMIKI: / NO TASTING
  sb10  the Ramcharitmanas book (leaf ARANYA KAND, DOHA 34); below, Rama eating sweet fruit from Shabari's basket,
        smiling (SO SWEET!, WONDERFUL!): RAMA ATE THE SWEET FRUITS / WITH LOVE; then TULSIDAS: / NO TASTING EITHER
  sb11  the tasted-berry picture in a cloud (little Shabari biting a berry, little Rama): THE TASTED BERRIES CAME /
        MUCH LATER; a bundle of later stories, a bhajan singer with a lamp singing (notes): FROM LATER / SONGS &
        STORIES
  sb12  REVEAL: the lamp dims, the Valmiki book glows, Shabari comes to look at it, the "?" in its medallion throbs
        on "asli" and bursts into fresh flowers on "chamatkaar": BUT VALMIKI HAS A / REAL MIRACLE
  sb13  the sages' altar with their offered flowers, fresh and swaying, Rama and Shabari either side; YEAR 1, 2, ...
        flips: THE SAGES HAD LEFT / YEARS AGO...; the flowers ringed: BUT THEIR FLOWERS WERE / STILL FRESH!; wilted
        flowers shown crossed out: THEY NEVER / WILTED!
  sb14  the sages' bark clothes hanging on a branch, dripping, Shabari pointing: THE SAGES' CLOTHES, / HUNG TO DRY,
        then (drips, glints): AFTER YEARS, STILL / WET!
  sb15  Shabari bows to Rama, who blesses her: MEETING RAMA, HER / WAIT WAS OVER; her gurus' lights in the sky; she
        becomes a soft light and rises to them: SHE WENT UP TO / HER GURUS
  sb15c CALLBACK: the hook's picture again (Shabari large, holding out a berry), the berry flickering bitten / whole
        with a "?": TASTED OR NOT...; two small book covers with gold ticks: HER WAIT / WAS TRUE
  sb16  two cards, TASTED BERRIES (a bitten bunch) and VALMIKI'S STORY (the Valmiki cover with fresh flowers), a red
        ring alternating: WHICH DO YOU / BELIEVE?; Shabari small between them, turning to the ringed one
"""
import math

import cairo

import andhe_cast  # noqa: F401  (registers the magnifying glass)
import arjuna_cast  # noqa: F401  (registers the thought bubble)
import dharmavyadha_cast  # noqa: F401  (registers the big tree, the drop)
import kaikeyi_cast  # noqa: F401  (registers the plaque, the leaf, the garland)
import lrekha_cast  # noqa: F401  (registers the hut and the palm-leaf books)
import mandhata_cast  # noqa: F401  (registers the water pot)
import puppet_core as pc
import shabari_cast as SB
import six_cast_c  # noqa: F401  (registers the clay hand lamp)
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, text_size
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_arjuna import card2
from scenes_hanuman_curse import arc_path, orb, qmark, trail, year_leaf
from scenes_jarasandha import FEET, INK, LIGHT, RED, bob_rot, glow, man_angles, motes, red_ring, walk_legs, woman_angles
from scenes_jayadratha import NIGHT, flash_at, tag, tint, title_lift, to_user
from scenes_kaikeyi import ANJALI, card, leaf_tag, rama, stamp2
from scenes_lakshman_rekha import big_x, book, sparkle
from scenes_mandhata import burst, held, lights, local, mix, reach_arm, warm
from scenes_ravana import dotted, head2
from scenes_ruru import held_grip, plate
from shots import CUT_LEAD, MIN_SHOT, T

MISSES = set()                       # cue words not found in a line (falls back to fractions)
G = FEET + 120                       # the ground line of most sets
GREEN_C = (0.20, 0.52, 0.18)


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, words)
    except (KeyError, ValueError):
        MISSES.add((bid, words[getattr(tl, "lang", "hi")] if isinstance(words, dict) else words))
        return T(tl, bid, frac)


# Every cue of every line: (name, {"hi": word}, fraction fallback, ((after, min gap), ...)); "t0" = the line's start.
# Words are exact substrings of the Hindi lines, given as short stems where a recogniser might drop a nukta or a
# chandrabindu (checked: MISSES stays empty).
CUES = {
    "sb1": (("S", {"hi": "शबरी"}, 0.1, (("t0", 0.3),)),
            ("J", {"hi": "जूठे"}, 0.2, (("S", 0.6),)),
            ("R", {"hi": "राम"}, 0.35, (("J", 0.8),)),
            ("P", {"hi": "प्यार"}, 0.45, (("R", 0.5),)),
            ("K", {"hi": "कहानी"}, 0.6, (("P", 0.6),)),
            ("V", {"hi": "वाल्मीकि"}, 0.7, (("P", 0.9), ("K", 0.4))),
            ("N", {"hi": "नहीं"}, 0.92, (("V", 0.7),))),
    "sb2": (("V", {"hi": "वाल्मीकि"}, 0.1, (("t0", 0.2),)),
            ("T", {"hi": "तुलसीदास"}, 0.5, (("V", 1.0),)),
            ("M", {"hi": "रामचरितमानस"}, 0.7, (("T", 0.5),))),
    "sb3": (("S", {"hi": "शबरी"}, 0.02, ()),
            ("J", {"hi": "जंगल"}, 0.12, (("S", 0.4),)),
            ("B", {"hi": "भोली"}, 0.3, (("J", 0.5),)),
            ("R", {"hi": "ऋषियों"}, 0.62, (("B", 0.9),)),
            ("V", {"hi": "सेवा"}, 0.78, (("R", 0.6),))),
    "sb4": (("K", {"hi": "कहा"}, 0.2, (("t0", 0.3),)),
            ("R", {"hi": "राम"}, 0.4, (("K", 0.6),)),
            ("A", {"hi": "आए"}, 0.55, (("R", 0.3),)),
            ("I", {"hi": "इंत"}, 0.8, (("A", 0.8),))),
    "sb5": (("H", {"hi": "स्वर्ग"}, 0.25, (("t0", 0.3),)),
            ("A", {"hi": "अकेली"}, 0.75, (("H", 1.0),))),
    "sb6": (("Y", {"hi": "सालों"}, 0.03, ()),
            ("P", {"hi": "रास्ता"}, 0.3, (("Y", 0.7),)),
            ("R", {"hi": "राम"}, 0.55, (("P", 0.8),)),
            ("F", {"hi": "फल"}, 0.8, (("R", 0.5),))),
    "sb7": (("D", {"hi": "दिन"}, 0.1, (("t0", 0.2),)),
            ("S", {"hi": "सीता"}, 0.22, (("D", 0.4),)),
            ("R", {"hi": "राम"}, 0.62, (("S", 1.0),)),
            ("C", {"hi": "सच"}, 0.75, (("R", 0.3),))),
    "sb8": (("F", {"hi": "पैर"}, 0.2, (("t0", 0.4),)),
            ("W", {"hi": "पानी"}, 0.4, (("F", 1.0),)),
            ("I", {"hi": "इकट्ठा"}, 0.65, (("W", 0.9),)),
            ("R", {"hi": "फल"}, 0.85, (("I", 0.4),))),
    "sb8q": (("K", {"hi": "क्या"}, 0.1, (("t0", 0.1),)),
             ("B", {"hi": "बेर"}, 0.45, (("K", 0.4),)),
             ("C", {"hi": "चख"}, 0.6, (("B", 0.2),))),
    "sb9": (("V", {"hi": "वाल्मीकि"}, 0.02, ()),
            ("I", {"hi": "इतना"}, 0.2, (("V", 0.8),)),
            ("J", {"hi": "जंगल"}, 0.4, (("I", 0.7),)),
            ("F", {"hi": "फल"}, 0.55, (("J", 0.6),)),
            ("C", {"hi": "चखने"}, 0.75, (("F", 0.9),)),
            ("N", {"hi": "नहीं"}, 0.95, (("C", 0.6),))),
    "sb10": (("T", {"hi": "तुलसीदास"}, 0.02, ()),
             ("M", {"hi": "मीठे"}, 0.3, (("T", 1.0),)),
             ("P", {"hi": "प्यार"}, 0.4, (("M", 0.4),)),
             ("A", {"hi": "तारी"}, 0.5, (("P", 0.5),)),
             ("C", {"hi": "चखने"}, 0.75, (("A", 1.0),)),
             ("N", {"hi": "नहीं"}, 0.95, (("C", 0.6),))),
    "sb11": (("L", {"hi": "बाद"}, 0.3, (("t0", 0.6),)),
             ("K", {"hi": "कहानियों"}, 0.6, (("L", 0.8),)),
             ("B", {"hi": "भजनों"}, 0.8, (("K", 0.5),))),
    "sb12": (("V", {"hi": "वाल्मीकि"}, 0.1, (("t0", 0.2),)),
             ("S", {"hi": "शबरी"}, 0.4, (("V", 0.6),)),
             ("A", {"hi": "असली"}, 0.7, (("S", 0.6),)),
             ("C", {"hi": "चमत्कार"}, 0.82, (("A", 0.3), ("V", 1.4)))),
    "sb13": (("Y", {"hi": "सालों"}, 0.2, (("t0", 0.4),)),
             ("F", {"hi": "फूल"}, 0.5, (("Y", 1.0),)),
             ("T", {"hi": "ताज"}, 0.65, (("F", 0.6),)),
             ("M", {"hi": "मुरझा"}, 0.85, (("T", 0.8),))),
    "sb14": (("S", {"hi": "सुखा"}, 0.35, (("t0", 0.5),)),
             ("K", {"hi": "कप"}, 0.55, (("S", 0.3),)),
             ("W", {"hi": "गीले"}, 0.85, (("K", 0.6),))),
    "sb15": (("M", {"hi": "मिलकर"}, 0.15, (("t0", 0.3),)),
             ("P", {"hi": "पूरा"}, 0.42, (("M", 0.6),)),
             ("G", {"hi": "गुरुओं"}, 0.7, (("P", 0.9),)),
             ("H", {"hi": "स्वर्ग"}, 0.85, (("G", 0.6),))),
    "sb15c": (("J", {"hi": "जूठे"}, 0.1, (("t0", 0.2),)),
              ("I", {"hi": "इंत"}, 0.5, (("J", 0.9),)),
              ("D", {"hi": "दोनों"}, 0.7, (("I", 0.5),)),
              ("S", {"hi": "सच्चा"}, 0.9, (("D", 0.5),))),
    "sb16": (("K", {"hi": "कहानी"}, 0.2, (("t0", 0.3),)),
             ("J", {"hi": "जूठे"}, 0.45, (("K", 0.6),)),
             ("V", {"hi": "वाल्मीकि"}, 0.65, (("J", 0.6),)),
             ("C", {"hi": "कमेंट"}, 0.88, (("V", 0.6),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_sb_cues", None)
    if cache is None:
        cache = {}
        tl._sb_cues = cache
    if bid not in cache:
        out = {"t0": T(tl, bid)}
        for name, words, frac, cons in CUES[bid]:
            v = cue(tl, bid, words, frac)
            for after, gap in cons:
                v = max(v, out[after] + gap)
            out[name] = v
        cache[bid] = out
    return cache[bid]


# ------------------------------------------------------------------ small helpers


def ground(cr, y=G, alpha=1.0, blur=0.0):
    prop(cr, "ground", W / 2, y + 6, 0.82, alpha=alpha, blur=blur)


def forest(cr, t, alpha=1.0, blur=0.0, hut=True, hut_x=880, hut_s=0.6,
           trees=((60, 0.62, 8, 0.6, True), (1060, 0.6, 10, 0.5, False))):
    """The forest by Matanga's hermitage: soft trees, the leaf hut, the ground."""
    for i, (x, s, b, a, fl) in enumerate(trees):
        prop(cr, "tree", x, G + 10, s, rot=sway(t, 0.006, 0.3, i), alpha=a * alpha, blur=b + blur, flip=fl)
    if hut:
        prop(cr, "lr_hut", hut_x, G + 8, hut_s, alpha=0.92 * alpha, blur=2 + blur)
    ground(cr, alpha=alpha, blur=blur)


def path_set(cr, t, alpha=1.0, hut=True):
    """The path to the hermitage: a far tree, the hut at the right edge, the trodden path along the ground."""
    prop(cr, "tree", 120, G + 10, 0.66, rot=sway(t, 0.006, 0.3), alpha=0.6 * alpha, blur=7, flip=True)
    prop(cr, "tree", 420, G + 10, 0.5, rot=sway(t, 0.006, 0.3, 1.0), alpha=0.45 * alpha, blur=12)
    if hut:
        prop(cr, "lr_hut", 1040, G + 8, 0.6, alpha=0.9 * alpha, blur=2)
    ground(cr, alpha=alpha)
    prop(cr, "sb_path", 540, G - 6, 0.72, alpha=alpha)


def limb_end(anchor, up, fore, end=(4.0, 150.0), l1=150.0):
    """Where a two-part arm's hand point lands in the puppet's root coordinates (up: the upper arm's absolute angle,
    fore: the forearm's angle relative to it; 0 hangs down)."""
    c, s_ = math.cos(fore), math.sin(fore)
    px, py = end[0] * c - end[1] * s_, end[0] * s_ + end[1] * c + l1
    c, s_ = math.cos(up), math.sin(up)
    return anchor[0] + px * c - py * s_, anchor[1] + px * s_ + py * c


def heap_sprite(i):
    return "sb_ber_y" if i % 3 == 1 else "sb_ber"


def basket(cr, x, y, s, n, flip=False, alpha=1.0, blur=0.0, pop_t=None, t=0.0, rot=0.0):
    """The bamboo basket (its handle's top at (x, y)) holding the first n berries of SB.HEAP; pop_t[i] = when berry
    i popped in (it bounces as it lands)."""
    if alpha <= 0.01:
        return
    sg = -1 if flip else 1
    prop(cr, "sb_bask_back", x, y, s, rot=rot, alpha=alpha, blur=blur, flip=flip)
    for i in range(min(n, len(SB.HEAP))):
        bx, by = SB.HEAP[i]
        k = 1.0
        if pop_t is not None and i < len(pop_t):
            u = (t - pop_t[i]) / 0.3
            if u < 0:
                continue
            k = back(clamp(u), 2.0)
        px, py = local(x, y, s, rot, flip, bx, by)
        prop(cr, heap_sprite(i), px, py - 30 * s * (1 - k), s * k, rot=0.2 * sg * ((i * 7) % 5 - 2) / 2, alpha=alpha,
             blur=blur)
    prop(cr, "sb_bask", x, y, s, rot=rot, alpha=alpha, blur=blur, flip=flip)


SHA_HEAD = {m: "sb_sha_head" + ("" if m == "calm" else "_" + m) for m in SB.SHA_MOODS}


def sha(cr, t, x, s, mood="calm", front=(-0.08, -0.35), backa=(0.15, -0.2), feet=G, head=0.0, hits=(), flip=False,
        alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.4, stick=False, kneel=False, bow=0.0, fist=False, extra=None,
        y=None):
    """Shabari standing (feet on `feet`) or kneeling (kneel: the folded legs, bow tips her torso forward from the
    hip). front / backa are the arms' (upper, fore) angles: 0 hangs down, -pi/2 points forward, -pi points up; stick
    puts her walking stick in her back hand, its foot on the ground. Returns her points (device)."""
    hip = (feet - (SB.KNEEL_H if kneel else 470.0) * s) if y is None else y
    ang = woman_angles("sb_sha", t, front, backa, head, hits, ph)
    sw = {"sb_sha_head": SHA_HEAD[mood]}
    if fist:
        sw["sb_sha_armF_lo"] = "sb_sha_armF_lo_fist"
    ex = dict(extra or {})
    if stick and not kneel:
        hy = limb_end(SB.SHA_SHOULDER_B, backa[0], backa[1])[1]
        ex["sb_sha_armB_lo"] = held_grip("sb_stick", backa, 1.0, 0.0, 504.0 - (470.0 - hy), alpha, blur)
    r = rot + bob_rot(t, ph, 0.01)
    if kneel:
        r += bow * (-1 if flip else 1)
        prop(cr, "sb_sha_kneel", x, hip, s, alpha=alpha, blur=blur, flip=flip)
        sw["sb_sha_body"] = "sb_sha_torso"
    return puppet(cr, SB.SHABARI, x, hip, s, r, flip, ang, alpha, blur, swap=sw, rods=rods, extra=ex or None)


def sha_reach(x, s, target, feet=G, flip=False, kneel=False, rot=0.0):
    """Front-arm angles that put Shabari's hand on `target` (scene coordinates)."""
    hip = feet - (SB.KNEEL_H if kneel else 470.0) * s
    if rot:
        c, s_ = math.cos(-rot), math.sin(-rot)                 # undo the body's tilt about the hip
        dx, dy = target[0] - x, target[1] - hip
        target = (x + dx * c - dy * s_, hip + dx * s_ + dy * c)
    return reach_arm(x, hip, s, SB.SHA_SHOULDER_F[0], target, flip)


def rama_(cr, t, x, s, mood="calm", feet=G, **kw):
    """kaikeyi_cast's Rama with his bow (the Lakshman Rekha reel's Rama); mood calm | smile | eat."""
    sw = None if mood == "calm" else {"rama_head": "sb_rama_head_" + mood}
    return rama(cr, t, x, s, feet=feet, swap=sw, **kw)


def rama_walk(cr, t, t0, t1, x0, x1, s, feet=G, step=0.42, **kw):
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step)
    kw.setdefault("hits", [(t1, 0.8)])
    return rama_(cr, t, x, s, legs=walk_legs(ph), rot=rock, y=feet - 434 * s + bob, feet=feet, **kw), x


SAGE = {"A": (SB.SAGE_A, "sx_shukra", "sb_sgA", {"calm": "sx_shukra_head", "smile": "sx_shukra_head_smile",
                                                  "call": "sx_shukra_head_call", "shut": "sx_shukra_head_shut"}),
        "B": (SB.SAGE_B, "rr_rishi", "sb_sgB", {"calm": "rr_rishi_head", "smile": "rr_rishi_head_teach",
                                                "call": "rr_rishi_head_teach", "shut": "rr_rishi_head"})}


def sage_sit(cr, t, k, x, ground_, s, mood="calm", front=(-0.5, -1.1), backa=(0.1, -0.6), head=0.0, hits=(),
             flip=True, alpha=1.0, blur=0.0, rods=True, ph=0.0, dy=0.0):
    """One of Matanga's old sages ('A': six_cast_a's white-bearded sage in saffron, 'B': ruru_cast's in cream) seated
    cross-legged (soles on ground_). mood: calm | smile | call (speaking) | shut."""
    rig, key, pre, heads = SAGE[k]
    hy = ground_ - 96 * s + dy
    ang = man_angles(key, t, front, backa, head, (0.0, 0.0), hits, ph)
    sw = {key + "_body": pre + "_body_sit", key + "_head": heads[mood]}
    seat = pre + "_seat"
    ex = {key + "_body": lambda c_: pc.paint_part(c_, seat, alpha, blur)}
    return puppet(cr, rig, x, hy, s, bob_rot(t, ph, 0.006), flip, ang, alpha, blur, hide=(key + "_legF", key + "_legB"),
                  swap=sw, rods=rods, extra=ex)


def berry_at(cr, t, p, s, bit=True, alpha=1.0, glint=0.0):
    """A single berry held at hand point p (scene coordinates), glinting."""
    if alpha <= 0.01:
        return
    x, y = p[0] + 6 * s, p[1] - 12 * s
    if glint > 0.01:
        glow(cr, x, y, 160 * s + 40, 0.5 * glint * alpha)
    prop(cr, "sb_ber_bit" if bit else "sb_ber", x, y, 1.85 * s, rot=0.15 + sway(t, 0.05, 0.5), alpha=alpha)
    if glint > 0.01:
        sparkle(cr, x - 18 * s, y - 20 * s, (26 + 8 * math.sin(t * 6)) * s / 0.8, glint * alpha)


def check(cr, x, y, size, p, col=GREEN_C, alpha=1.0):
    """A tick mark drawn in (p = how much)."""
    if p <= 0:
        return
    pts = [(x - 0.45 * size, y), (x - 0.12 * size, y + 0.33 * size), (x + 0.5 * size, y - 0.4 * size)]
    l1 = math.dist(pts[0], pts[1])
    l2 = math.dist(pts[1], pts[2])
    d = (l1 + l2) * clamp(p)
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, col_, a in ((size * 0.2, LIGHT, 0.85), (size * 0.13, col, 0.95)):
        cr.move_to(*pts[0])
        if d <= l1:
            f = d / l1
            cr.line_to(pts[0][0] + (pts[1][0] - pts[0][0]) * f, pts[0][1] + (pts[1][1] - pts[0][1]) * f)
        else:
            cr.line_to(*pts[1])
            f = (d - l1) / l2
            cr.line_to(pts[1][0] + (pts[2][0] - pts[1][0]) * f, pts[1][1] + (pts[2][1] - pts[1][1]) * f)
        cr.set_source_rgba(*col_, a * alpha)
        cr.set_line_width(lw)
        cr.stroke()
    cr.restore()


COVER_TITLE = {"v": (("VALMIKI", 74), ("RAMAYANA", 62)), "t": (("TULSIDAS", 66), ("RAMCHARITMANAS", 50))}


def cover(cr, t, t_in, x, y, s, which, med="sb_ber3_bit", med_s=0.95, x_t=None, tick_t=None, alpha=1.0, rods=True,
          glow_a=0.0, med_fn=None):
    """A book's cloth cover dropping in on two rods (Valmiki 'v' saffron, Tulsidas 't' red), its title on the pale
    panel, a picture in its round medallion (a sprite, or med_fn(cr) drawing in cover units about the medallion's
    centre); x_t = when a red X slashes the picture, tick_t = when a green tick goes over it."""
    if t_in is not None:
        q = back(clamp((t - t_in) / 0.4), 1.3)
        a = clamp((t - t_in) / 0.2) * alpha
    else:
        q, a = 1.0, alpha
    if a <= 0.01:
        return
    yy = y + 240 * (1 - q)
    r = sway(t, 0.008, 0.4, x * 0.01)
    if glow_a > 0.01:
        glow(cr, x, yy, 520 * s + 120, glow_a * a)
        warm(cr, x, yy, 420 * s, 0.7 * glow_a * a)
    if rods:
        for sx in (-1, 1):
            pc.rod(cr, x + sx * 150 * s, yy + 290 * s, x + sx * 220, H + 60, alpha=0.5 * a)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(r)
    cr.scale(s, s)
    pc.paint_part(cr, "sb_cov_" + which, a)
    (l1, s1), (l2, s2) = COVER_TITLE[which]
    for txt, sz, dy in ((l1, s1, -206), (l2, s2, -138)):
        sz2 = min(sz, int(sz * 330 / max(1, text_size(txt, sz, HEAD_FONT)[0])))
        draw_text(cr, txt, 0, dy, sz2, INK, a, HEAD_FONT, "cm")
    if med_fn is not None:
        med_fn(cr, a)
    elif med:
        prop(cr, med, 0, 128, med_s, alpha=a)
    if x_t is not None and t > x_t:
        big_x(cr, 0, 110, 190, 190, prog(t, x_t, 0.3), alpha=a, lw=24)
    if tick_t is not None and t > tick_t:
        check(cr, 0, 110, 190, prog(t, tick_t, 0.35), alpha=a)
    cr.restore()


def slam_stamp(cr, t, t_in, lines, x, y, size, kicks=(), rot=-0.06):
    """scenes_kaikeyi.stamp2 slammed on at t_in, then thumped again (a quick swell) at each of `kicks`."""
    k = 1.0
    for tk in kicks:
        u = t - tk
        if 0 <= u < 0.35:
            k += 0.16 * math.sin(math.pi * u / 0.35)
    cr.save()
    cr.translate(x, y)
    cr.scale(k, k)
    stamp2(cr, t, t_in, lines, 0, 0, size, rot=rot)
    cr.restore()


def rise(cr, t, t_up, p0, p1, dur=1.6, r=30.0, alpha=1.0, trail_a=0.7):
    """A soft orb of light rising from p0 to p1 (an ascent, never a fire), a ribbon of light behind it; returns its
    position (or None before it leaves)."""
    u = clamp((t - t_up) / dur)
    if u <= 0 or alpha <= 0.01:
        return None
    e = ease(u)
    pts = [(p0[0] + (p1[0] - p0[0]) * ease(u * i / 30) + 30 * math.sin(math.pi * u * i / 30),
            p0[1] + (p1[1] - p0[1]) * ease(u * i / 30)) for i in range(31)]
    trail(cr, pts, trail_a * alpha * (1 - 0.5 * prog(t, t_up + dur, 0.8)), 0.55)
    x, y = pts[-1]
    glow(cr, x, y, 220 + 60 * e, 0.7 * alpha)
    orb(cr, t, x, y + 3 * math.sin(t * 3), r * (0.8 + 0.2 * e), alpha)
    return x, y


def notes(cr, t, t_on, x, y, alpha=1.0):
    """Music notes floating up and away from a singer's mouth at (x, y)."""
    if t < t_on or alpha <= 0.01:
        return
    for i in range(5):
        u = (t - t_on) * 0.55 + i / 5
        if u < 0 or (t - t_on) < i * 0.2:
            continue
        u %= 1.0
        a = math.sin(math.pi * u) * alpha * clamp((t - t_on) / 0.3)
        prop(cr, "sb_note", x + 40 + 200 * u + 30 * math.sin(t * 2 + i), y - 40 - 320 * u, 0.5 + 0.2 * (i % 2),
             rot=0.3 * math.sin(t * 3 + i), alpha=a)


# ------------------------------------------------------------------ sb1  hook


HK = (330, 1.0, 1890)                # Shabari in the hook: x, scale, feet
HK_BERRY = (690, 1070)               # where her hand holds the berry out
HK_BASKET = 0.8


def hook_figure(cr, t, reach=0.0, mood="smile", hits=(), glint=0.0, bit=True, berry_a=1.0):
    """The hook's picture (also the callback's): Shabari large, holding a berry out, her full basket at her side.
    Returns the berry's position."""
    x, s, feet = HK
    tgt = (HK_BERRY[0] + 50 * reach, HK_BERRY[1] - 30 * reach)
    fr = sha_reach(x, s, tgt, feet)
    pts = sha(cr, t, x, s, mood=mood, front=fr, backa=(-0.12, -0.3), feet=feet, head=0.06, hits=hits, ph=1.0)
    hb = to_user(cr, pts["handB"])
    basket(cr, hb[0] + 6, hb[1] - 10, HK_BASKET * s, 15)
    hf = to_user(cr, pts["handF"])
    berry_at(cr, t, hf, s, bit=bit, alpha=berry_a, glint=glint)
    return hf[0] + 6 * s, hf[1] - 10 * s


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "sb1")
    tS, tJ, tR, tP, tK, tV, tN = c["S"], c["J"], c["R"], c["P"], c["K"], c["V"], c["N"]
    x, s, feet = HK
    glow(cr, x + 140, feet - 760 * s, 660, 0.42)
    reach = keyed(t, [(t0, 0.0), (tR, 1.0)], 0.3, 1.4)
    glint = 0.5 + 0.5 * prog(t, tR, 0.4)
    bp = hook_figure(cr, t, reach, "smile", hits=[(tR, 0.3), (tV, 0.2)], glint=glint)
    if t > tP:
        for i in range(6):                                  # little lights of love round the berry
            u = ((t - tP) * 0.6 + i / 6) % 1.0
            sparkle(cr, bp[0] - 60 + 120 * ((i * 0.37) % 1), bp[1] - 40 - 160 * u, 18 * math.sin(math.pi * u),
                    0.8 * prog(t, tP, 0.4))

    def ui(cr):
        head2(cr, t, "SHABARI'S TASTED BERRIES?", -1.0, None, 0.0, small_size=70)
        slam_stamp(cr, t, 0.3, ["NOT IN", "VALMIKI"], 540, 530, 118, kicks=(tV,))
        leaf_tag(cr, t, tK, 700, 770, 0.72, [("THE VALMIKI RAMAYANA", 40, MONO_FONT)], rot=0.03, rod=False)
        plate(cr, t, tS, "SHABARI", x + 10, 865, 40)
        if t > tJ:
            red_ring(cr, bp[0], bp[1], 78, 70, prog(t, tJ, 0.35), 9)
            plate(cr, t, tJ + 0.2, "TASTED FIRST?", bp[0] + 70, bp[1] + 120, 36, color=RED)
        if t > tN:
            big_x(cr, bp[0], bp[1], 150, 140, prog(t, tN, 0.3), lw=18)
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.3) + flash_at(t, tV, 0.35) + flash_at(t, tN, 0.2))


# ------------------------------------------------------------------ sb2  not in either book


def s_books(cr, t, tl, t0, t1):
    c = cues(tl, "sb2")
    tV, tT, tM = c["V"], c["T"], c["M"]
    glow(cr, 540, 1150, 660, 0.35)
    cover(cr, t, tV - 0.35, 290, 1130, 0.98, "v", x_t=tV + 0.5)
    cover(cr, t, tT - 0.35, 790, 1130, 0.98, "t", x_t=tM + 0.15)

    def ui(cr):
        if t < tM:
            head2(cr, t, "TASTED BERRIES?", t0 + 0.05, "NOT IN VALMIKI", tV + 0.35, big_size=200)
        else:
            head2(cr, t, "TASTED BERRIES?", -1.0, "NOT IN EITHER BOOK", tM + 0.2, big_size=200, under=tM + 0.6)
    return dict(ui=ui, flash=flash_at(t, tV + 0.5, 0.2) + flash_at(t, tM + 0.15, 0.25))


# ------------------------------------------------------------------ sb3  a simple forest woman; she served old sages


SW = (330, 0.74)                     # Shabari sweeping: x, scale
SAGES3 = (("A", 720, 0.58, 0.3), ("B", 920, 0.54, 1.3))


def s_serve(cr, t, tl, t0, t1):
    c = cues(tl, "sb3")
    tS, tJ, tB, tR, tV = c["S"], c["J"], c["B"], c["R"], c["V"]
    fb, _, fa = depth(t, tJ - 0.2, 0.6)
    if t > tJ - 0.2:
        forest(cr, t, alpha=fa, blur=fb * 0.6, hut_x=900, hut_s=0.58)
    else:
        ground(cr)
    for i, (k, xx, ss, ph) in enumerate(SAGES3):
        if t > tR - 0.3:
            b, kk, a = depth(t, tR - 0.3 + 0.15 * i, 0.5)
            mood = "smile" if t > tV + 0.3 else "calm"
            sage_sit(cr, t, k, xx, G, ss * kk, mood=mood, flip=True, alpha=a, blur=b, ph=ph,
                     front=(-0.6, -1.0) if i == 0 else (-0.5, -1.1))
    x, s = SW
    if t < tV - 0.15:                                       # sweeping the path, bent over her broom
        stoop = 0.3
        swp = math.sin(2 * math.pi * 1.1 * (t - t0))
        hip = G - 470 * s
        tgt = (x + 250 * s + 70 * s * swp, hip - 10 * s)
        fr = sha_reach(x, s, tgt, rot=stoop)
        pts = sha(cr, t, x, s, mood="calm", front=fr, backa=(-0.2, -0.6), rot=stoop, ph=0.4, fist=True,
                  head=0.08)
        hf = to_user(cr, pts["handF"])
        L = 345 * s * 1.25
        dy = G - 6 - hf[1]
        th = -math.acos(clamp(dy / L, -1, 1))
        prop(cr, "sb_broom", hf[0], hf[1], 1.25 * s, rot=th)
        bx = hf[0] - math.sin(th) * L
        for i in range(5):                                  # dust puffs where the broom brushes
            u = ((t - t0) * 1.1 + i / 5) % 1.0
            prop(cr, "cloud", bx + 30 + 120 * u * (1 if i % 2 else 0.6), G - 30 - 90 * u, 0.14 + 0.16 * u,
                 alpha=0.6 * (1 - u))
    else:                                                   # she brings them water
        w = keyed(t, [(tV - 0.15, 0.0), (tV + 0.2, 1.0)], 0.3, 1.3)
        xs = x + 150 * w
        tgt = (SAGES3[0][1] - 140, G - 330)
        fr = mix((-0.6, -0.6), sha_reach(xs, s, tgt), w)
        sha(cr, t, xs, s, mood="smile", front=fr, backa=(0.2, -0.4), ph=0.4, hits=[(tV, 0.4)],
            extra={"sb_sha_armF_lo": held("md_kalasha", fr, 0.42, 166)})
    dev = cr.user_to_device(x + 20, G - 1010 * s)

    def ui(cr):
        if t < tR - 0.1:
            head2(cr, t, "SHABARI: A SIMPLE", t0 + 0.05, "FOREST WOMAN", tB, big_size=230)
        else:
            head2(cr, t, "SHE SERVED SOME", tR - 0.1, "OLD SAGES", tV, big_size=250)
            tag(cr, t, tR + 0.3, "THE SAGES", 800, 1070, 38, t_out=tV + 1.2)
        plate(cr, t, tS + 0.1, "SHABARI", dev[0], dev[1], 38, t_out=tR - 0.2)
    return dict(ui=ui, flash=flash_at(t, tB, 0.15) + flash_at(t, tR, 0.15))


# ------------------------------------------------------------------ sb4  "Rama will come. Wait for him."


BUB4 = (560, 900, 0.62)


def bubble_rama(cr, t, bx, by, bs, t_in, alpha=1.0):
    """Inside the thought bubble: a little path, Rama walking along it (looping), the hut far off."""
    cr.save()
    cr.new_path()
    pc.ell(cr, bx, by, 280 * bs, 190 * bs)
    cr.clip()
    a = alpha * prog(t, t_in, 0.3)
    feet = by + 112 * bs
    prop(cr, "lr_hut", bx + 165 * bs, feet - 8 * bs, 0.16 * bs / 0.62, alpha=0.7 * a, blur=1)
    prop(cr, "sb_path", bx, feet - 6 * bs, 0.3 * bs / 0.62, alpha=a)
    u = ((t - t_in) / 2.4) % 1.0
    x, bob, rock, ph = hop_walk(u * 2.4, 0.0, 2.4, bx - 210 * bs, bx + 70 * bs, 0.4)
    rs = 0.14 * bs / 0.62
    rama_(cr, t, x, rs, mood="smile", feet=feet, y=feet - 434 * rs + bob * 0.3, legs=walk_legs(ph),
          rot=rock, rods=False, alpha=a)
    cr.restore()


def s_promise(cr, t, tl, t0, t1):
    c = cues(tl, "sb4")
    tK, tR, tA, tI = c["K"], c["R"], c["A"], c["I"]
    forest(cr, t, alpha=0.9, blur=3, hut_x=980, hut_s=0.5)
    talk = t > tK and int(t * 4.4) % 3 != 0 and t < tI + 1.0
    pt = keyed(t, [(t0, 0.0), (tR - 0.1, 1.0)], 0.3, 1.3)
    sage_sit(cr, t, "B", 960, G, 0.56, mood="smile", flip=True, ph=1.3, blur=2)
    sp = sage_sit(cr, t, "A", 770, G, 0.7, mood="call" if talk else "calm", flip=True,
                  front=mix((-0.5, -1.1), (-2.2, -0.5), pt), hits=[(tK, 0.4), (tI, 0.5)], ph=0.3)
    listen = prog(t, tA, 0.4)
    sha(cr, t, 270, 0.72, mood="look" if t > tA else "calm", head=0.04 - 0.08 * listen,
        hits=[(tI + 0.1, 0.3)], ph=0.4, **ANJALI)
    bx, by, bs = BUB4
    q = back(clamp((t - tR + 0.15) / 0.35), 1.5)
    if q > 0.01:
        prop(cr, "ar_think", bx, by, bs * (0.6 + 0.4 * q), rot=sway(t, 0.006, 0.4), alpha=clamp(q))
        if q > 0.8:
            bubble_rama(cr, t, bx, by - 10, bs, tR)
    mouth = sp["head"]

    def ui(cr):
        if t < tI - 0.1:
            head2(cr, t, "THE SAGES SAID:", t0 + 0.05, "'RAMA WILL COME!'", tA, big_size=220)
        else:
            head2(cr, t, "THE SAGES SAID:", -1.0, "'WAIT FOR HIM!'", tI, big_size=230, under=tI + 0.4)
        if tK < t < tR:
            dotted(cr, [(mouth[0] - 70, mouth[1] - 40), (bx + 150, by + 120)], prog(t, tK, 0.4), 26, 5, INK, 0.5)
    return dict(ui=ui, flash=flash_at(t, tR, 0.2) + flash_at(t, tI, 0.15))


# ------------------------------------------------------------------ sb5  the sages went to heaven; she was alone


SAGES5 = (("A", 720, 0.62, 0.3), ("B", 920, 0.56, 1.3))


def s_alone(cr, t, tl, t0, t1):
    c = cues(tl, "sb5")
    tH, tA = c["H"], c["A"]
    forest(cr, t, alpha=0.9, blur=2, hut_x=960, hut_s=0.5)
    for i, (k, xx, ss, ph) in enumerate(SAGES5):        # the sages turn to soft light and rise
        tu = tH - 0.2 + 0.25 * i
        u = clamp((t - tu) / 1.0)
        hy = G - 96 * ss
        if u < 1:
            glow(cr, xx, hy - 250 * ss, 300, 0.6 * prog(t, tu - 0.3, 0.4) * (1 - u))
            sage_sit(cr, t, k, xx, G, ss, mood="shut" if t > tu - 0.3 else "smile", flip=True,
                     front=(-0.75, -1.85), backa=(-0.8, -1.8), alpha=1 - u, blur=14 * u, dy=-140 * ease(u),
                     rods=u < 0.3, ph=ph)
        rise(cr, t, tu + 0.3, (xx, hy - 300 * ss), (xx - 120 + 80 * i, 660 + 30 * i), 1.3, 26,
             alpha=1 - prog(t, tA + 0.3, 0.6))
    alone = prog(t, tA, 0.5)
    drop = keyed(t, [(t0, 0.0), (tA, 1.0)], 0.35, 1.2)
    sha(cr, t, 300, 0.74, mood="look" if t < tA else "calm", head=-0.16 * (1 - alone) + 0.16 * alone,
        front=mix(ANJALI["front"], (-0.15, -0.3), drop), backa=mix(ANJALI["backa"], (0.1, -0.2), drop),
        rot=0.06 * alone, ph=0.4)

    def ui(cr):
        if t < tA - 0.1:
            head2(cr, t, "THEN THE SAGES WENT TO", t0 + 0.05, "HEAVEN", tH, big_size=270)
        else:
            head2(cr, t, "SHABARI WAS LEFT", tA - 0.1, "ALL ALONE", tA + 0.05, big_size=260)
    return dict(ui=ui, flash=flash_at(t, tH, 0.25), night=0.2 * alone, lift=1.0)


# ------------------------------------------------------------------ sb6  for years she watched the path; fruits


SH6 = (830, 0.7)                     # Shabari watching: x, scale (facing left)
BK6 = (620, 0.62)                    # the basket on the ground: x, scale (its handle's top above the ground)


def basket_ground(x, s):
    """The handle's top for a basket standing on the ground at x."""
    return x, G - 4 - (SB.BASK_RIM + 152) * s


def watcher(cr, t, mood="look", alpha=1.0, hits=(), shade=1.0, stick=True):
    """Shabari at the hut's edge, facing down the path (to the left), her hand shading her eyes."""
    x, s = SH6
    hip = G - 470 * s
    brow = local(x, hip, s, 0.0, True, 74, -440)
    fr = mix((-0.3, -0.5), reach_arm(x, hip, s, SB.SHA_SHOULDER_F[0], brow, True), shade)
    return sha(cr, t, x, s, mood=mood, front=fr, backa=(0.25, -0.55), flip=True, stick=stick, ph=0.4, alpha=alpha,
               hits=hits, head=-0.04)


def sun_moon(cr, t, t_a, t_b, period=1.1):
    """The sun and the moon racing over the sky in turn (days passing); returns how dark it is (0..1)."""
    if t < t_a or t > t_b + period:
        return 0.0
    u = (t - t_a) / period
    k = int(u)
    f = u - k
    pts = arc_path((60, 1130), (1020, 1130), 300, 30, f)
    x, y = pts[-1]
    if k % 2 == 0:
        glow(cr, x, y, 200, 0.6)
        prop(cr, "sun", x, y, 0.22, rot=t)
    else:
        prop(cr, "moon", x, y, 0.3)
        for i in range(4):
            prop(cr, "star", 150 + 230 * i, 980 + 70 * (i % 2), 0.35, alpha=0.7 * math.sin(math.pi * f))
    return 0.32 * math.sin(math.pi * f) if k % 2 else 0.0


def s_years(cr, t, tl, t0, t1):
    c = cues(tl, "sb6")
    tY, tP, tR, tF = c["Y"], c["P"], c["R"], c["F"]
    t_end = tl["sb6"].end
    dark = sun_moon(cr, t, tY, t_end - 0.4)
    path_set(cr, t)
    n = 15
    pops = [tR + (t_end + 0.3 - tR) * i / n for i in range(n)]
    bx, bs = BK6
    hx, hy = basket_ground(bx, bs)
    basket(cr, hx, hy, bs, n, pop_t=pops, t=t)
    watcher(cr, t, shade=keyed(t, [(t0, 0.0), (tP - 0.1, 1.0), (tR - 0.1, 0.0)], 0.3, 1.3))

    def ui(cr):
        if t < tR - 0.1:
            head2(cr, t, "FOR YEARS AND YEARS,", t0 + 0.05, "SHE WAITED", tP, big_size=260)
        else:
            head2(cr, t, "SHE KEPT FRUITS", tR - 0.1, "FOR RAMA", tR + 0.05, big_size=270)
        if t > tY:
            year_leaf(cr, t, tY, max(tY + 1.5, t_end - 0.3), 540, 760, 1.0, n=20, alpha=prog(t, tY, 0.3))
        if t > tP and t < tR:                               # her gaze, down the path
            ex_, ey_ = local(SH6[0], G - 470 * SH6[1], SH6[1], 0.0, True, 70, -400)
            dotted(cr, [(ex_ - 40, ey_), (420, G - 260), (80, G - 50)], prog(t, tP, 0.6), 30, 6, RED, 0.75)
    return dict(ui=ui, night=dark, lift=1.0, flash=flash_at(t, tR, 0.15))


# ------------------------------------------------------------------ sb7  one day, Rama really came


def s_came(cr, t, tl, t0, t1):
    c = cues(tl, "sb7")
    tD, tS, tR, tC = c["D"], c["S"], c["R"], c["C"]
    dawn = prog(t, tD - 0.2, 0.8)
    glow(cr, 120, 1250, 640, 0.55 * dawn)
    prop(cr, "sun", 150, 1300 - 280 * dawn, 0.3, rot=t * 0.3, alpha=0.8 * dawn)
    path_set(cr, t)
    bx, bs = BK6
    hx, hy = basket_ground(bx, bs)
    basket(cr, hx, hy, bs, 15)
    t_in, t_stop = tS - 0.4, max(tR + 0.5, tS + 1.4)
    rx = 330
    if t > t_in:
        if t > tC:
            burst(cr, t, rx, G - 600, tC, n=18, rmax=640, alpha=0.6)
            glow(cr, rx, G - 600, 520, 0.4 * prog(t, tC, 0.4))
        search = keyed(t, [(t_in, 1.0), (t_stop, 0.0)], 0.3, 1.3)
        fr = mix((-0.6, -0.4), (-2.3, -1.3), search)
        _, rxx = rama_walk(cr, t, t_in, t_stop, -160, rx, 0.72, mood="smile" if t > tC else "calm", front=fr,
                           head=0.04 * search)
        rdev = cr.user_to_device(rxx, G - 1150 * 0.72)
    else:
        rdev = None
    joy = t > tC
    watcher(cr, t, mood="joy" if joy else "look", shade=1.0 - prog(t, tC, 0.3), hits=[(tC, 0.5)])

    def ui(cr):
        if t < tR - 0.1:
            head2(cr, t, "THEN ONE", t0 + 0.05, "DAY...", tD, big_size=280)
        else:
            head2(cr, t, "RAMA REALLY", tR - 0.1, "CAME!", tC, big_size=300, under=tC + 0.4)
        if rdev is not None:
            plate(cr, t, tS, "LOOKING FOR SITA MATA", max(300, rdev[0] + 40), rdev[1], 32, t_out=tC + 0.6)
    return dict(ui=ui, flash=flash_at(t, tC, 0.4), night=0.18 * (1 - dawn), lift=1.0)


# ------------------------------------------------------------------ sb8  his feet, water, fruits


RM8 = (340, 0.76)                    # Rama: x, scale (facing right)
SH8 = (730, 0.74)                    # Shabari: x, scale (facing left)


def s_offer(cr, t, tl, t0, t1):
    c = cues(tl, "sb8")
    tF, tW, tI, tR = c["F"], c["W"], c["I"], c["R"]
    forest(cr, t, alpha=0.85, blur=4, hut_x=960, hut_s=0.5)
    rx, rs = RM8
    take = keyed(t, [(t0, 0.0), (tR + 0.5, 1.0)], 0.3, 1.3)
    bless = keyed(t, [(t0, 0.0), (tF + 0.3, 1.0), (tW, 0.0)], 0.3, 1.3)
    rfr = mix(mix((-0.45, -0.5), (-1.9, -0.6), bless), (-1.25, -0.5), take)
    rpts = rama_(cr, t, rx, rs, mood="smile", front=rfr, head=0.1 * prog(t, tF, 0.4) * (1 - take), ph=0.5,
          hits=[(tF + 0.3, 0.4), (tR + 0.5, 0.4)])
    x, s = SH8
    knee = t > tF - 0.25
    if not knee:
        sha(cr, t, x, s, mood="joy", flip=True, ph=0.4, **ANJALI)
    else:
        bow = keyed(t, [(tF - 0.25, 0.0), (tF, 1.1), (tW - 0.1, 0.12)], 0.3, 1.2)
        if t < tW - 0.1:                                    # bowing, her hands at his feet
            foot = (rx + 100 * rs, G - 15)
            fr = sha_reach(x, s, foot, flip=True, kneel=True, rot=-bow)
            bk = mix((0.1, -0.3), (-1.2, -0.3), clamp(bow))
            sha(cr, t, x, s, mood="shut", flip=True, kneel=True, bow=bow, front=fr, backa=bk, ph=0.4)
        elif t < tI - 0.1:                                  # a pot of water held up to him
            fr = (-1.15, -0.95)
            sha(cr, t, x, s, mood="smile", flip=True, kneel=True, bow=0.12, front=fr, backa=(-0.9, -1.0), ph=0.4,
                hits=[(tW, 0.4)], extra={"sb_sha_armF_lo": held("md_kalasha", fr, 0.42, 166)})
        else:                                               # then the basket of fruits
            fr = (-1.15, -0.8)
            pts = sha(cr, t, x, s, mood="joy", flip=True, kneel=True, bow=0.1, front=fr, backa=(-1.0, -0.9),
                      ph=0.4, hits=[(tI, 0.4), (tR, 0.3)])
            hf = to_user(cr, pts["handF"])
            basket(cr, hf[0] - 10, hf[1] - 40, 0.55, 15 if t < tR + 0.7 else 14, flip=True)
            if t > tR + 0.7:                                # Rama takes one
                rh = to_user(cr, rpts["handF"])
                prop(cr, "sb_ber", rh[0] + 6, rh[1] - 8, 0.9)

    def ui(cr):
        if t < tW - 0.1:
            head2(cr, t, "SHE TOUCHED HIS", t0 + 0.05, "FEET", tF, big_size=300)
        elif t < tI - 0.1:
            head2(cr, t, "SHE GAVE HIM", tW - 0.1, "WATER...", tW, big_size=280)
        else:
            head2(cr, t, "SHE GAVE HIM WATER...", -1.0, "AND FRUITS", tR, big_size=270, under=tR + 0.5)
    return dict(ui=ui, flash=flash_at(t, tF, 0.15) + flash_at(t, tR, 0.2))


# ------------------------------------------------------------------ sb8q  did she taste them first?


def s_question(cr, t, tl, t0, t1):
    c = cues(tl, "sb8q")
    tK, tB, tC = c["K"], c["B"], c["C"]
    glow(cr, 540, 1500, 520, 0.4)
    ground(cr)
    x, s = 470, 0.56
    hip = G - 470 * s
    lift_ = keyed(t, [(t0, 0.0), (tB, 1.0)], 0.3, 1.3)
    tgt = local(x, hip, s, 0.0, False, 130, -330 - 40 * lift_)
    fr = sha_reach(x, s, tgt)
    pts = sha(cr, t, x, s, mood="look", front=fr, backa=(-0.12, -0.3), head=0.08 * math.sin(t * 1.3), ph=0.4)
    hb = to_user(cr, pts["handB"])
    basket(cr, hb[0] + 6, hb[1] - 10, 0.8 * s, 15)
    berry_at(cr, t, to_user(cr, pts["handF"]), s, bit=False, glint=0.6)

    def ui(cr):
        head2(cr, t, "THE BIG QUESTION:", t0 + 0.05, None, 0.0)
        qmark(cr, t, tK - 0.1, 540, 650, 330, RED)
        card2(cr, t, tK, 540, 960, 1.08, [("DID SHE TASTE", 80, INK, -54, tK + 0.3),
                                          ("THEM FIRST?", 104, RED, 34, tC)])
    return dict(ui=ui, flash=flash_at(t, tK, 0.15) + flash_at(t, tC, 0.2), night=0.1)


# ------------------------------------------------------------------ sb9  Valmiki: she gathered forest fruits


def s_valmiki(cr, t, tl, t0, t1):
    c = cues(tl, "sb9")
    tV, tI, tJ, tF, tC, tN = c["V"], c["I"], c["J"], c["F"], c["C"], c["N"]
    glow(cr, 540, 1150, 640, 0.35)
    leaves = [(None, [("VALMIKI RAMAYANA", 86, HEAD_FONT)], 0),
              (tJ, [("\"I GATHERED", 88, HEAD_FONT)], 0),
              (tF, [([("FOREST FRUITS", RED)], 92, HEAD_FONT)], 0),
              (tF + 0.45, [("FOR YOU.\"", 88, HEAD_FONT)], 0)]
    bx, by, bsc = 540, 870, 0.88
    cen = book(cr, t, bx, by, bsc, leaves, t_in=t0 + 0.05, t_open=t0 + 0.55, ring=(2, 0, 0, tF + 0.3))
    if len(cen) >= 4 and t > tI:                            # the magnifying glass looks for the words
        ln = 1 if t < tF else 2
        if t < tC:
            gx, gy = cen[ln][0] - 230 + 30 * math.sin(t * 2.2), cen[ln][1] - 6
        else:                                               # searching every leaf for "tasting"
            u = (t - tC) / 0.9
            k = int(u) % 3 + 1
            f = u - int(u)
            gx = cen[k][0] - 300 + 600 * f
            gy = cen[k][1] - 6
        a = prog(t, tI, 0.3)
        prop(cr, "ak_lens", gx, gy, 0.82, rot=0.1 * math.sin(t * 1.5), alpha=a)

    def ui(cr):
        if t < tC - 0.1:
            head2(cr, t, "VALMIKI SAYS:", t0 + 0.05, "SHE GATHERED FRUITS", tF, big_size=200)
        else:
            head2(cr, t, "VALMIKI:", tC - 0.1, "NO TASTING", tC + 0.1, big_size=260, under=tN)
        leaf_tag(cr, t, tI, 790, 690, 0.62, [("VALMIKI RAMAYANA", 34, MONO_FONT), ("ARANYA KANDA 74", 50, HEAD_FONT)],
                 rot=0.04, rod=False, t_out=tC - 0.2)
    return dict(ui=ui, flash=flash_at(t, tF, 0.15) + flash_at(t, tC + 0.1, 0.25))


# ------------------------------------------------------------------ sb10  Tulsidas: Rama ate them with love


RM10 = (330, 0.62)
SH10 = (690, 0.62)


def s_tulsi(cr, t, tl, t0, t1):
    c = cues(tl, "sb10")
    tT, tM, tP, tA, tC, tN = c["T"], c["M"], c["P"], c["A"], c["C"], c["N"]
    glow(cr, 540, 1400, 600, 0.35)
    leaves = [(None, [("RAMCHARITMANAS", 84, HEAD_FONT)], 0),
              (tM, [("\"SWEET FRUITS...\"", 84, HEAD_FONT)], 0)]
    book(cr, t, 540, 720, 0.66, leaves, t_in=t0 + 0.05, t_open=t0 + 0.5, rods=False)
    forest(cr, t, alpha=0.55, blur=6, hut=False)
    rx, rs = RM10
    # Rama eats: the berry goes from his hand to his mouth, again and again
    if t > tM - 0.2:
        cyc = ((t - tM + 0.2) / 1.2) % 1.0
        up = math.sin(math.pi * clamp(cyc / 0.6))
        eating = up > 0.6
    else:
        up, eating = 0.0, False
    hip = G - 434 * rs
    mouth = local(rx, hip, rs, 0.0, False, 70, -360)
    fr = mix((-1.2, -0.6), reach_arm(rx, hip, rs, 26 * 1.05, mouth), up)
    pts = rama_(cr, t, rx, rs, mood="eat" if eating else "smile", front=fr, ph=0.5,
                hits=[(tA, 0.3)])
    if t > tM - 0.2 and not eating:
        hf = to_user(cr, pts["handF"])
        prop(cr, "sb_ber", hf[0] + 4, hf[1] - 8, 0.8)
    x, s = SH10
    sp = sha(cr, t, x, s, mood="joy", flip=True, front=(-1.35, -0.55), backa=(-1.25, -0.5), ph=0.4)
    hf2 = to_user(cr, sp["handF"])
    basket(cr, hf2[0] - 10, hf2[1] - 40, 0.5, 13, flip=True)
    if t > tP:
        lights(cr, t, rx + 40, hip - 300 * rs, 160, 8, 0.8 * prog(t, tP, 0.4), (1.0, 0.55, 0.45), 0.6)
    top = cr.user_to_device(rx + 190, G - 980 * rs)

    def ui(cr):
        if t < tM - 0.1:
            head2(cr, t, "TULSIDAS WRITES:", t0 + 0.05, None, 0.0)
        elif t < tC - 0.1:
            head2(cr, t, "RAMA ATE THE SWEET FRUITS", tM - 0.1, "WITH LOVE", tP, big_size=260)
        else:
            head2(cr, t, "TULSIDAS:", tC - 0.1, "NO TASTING EITHER", tC + 0.1, big_size=200, under=tN)
        leaf_tag(cr, t, tT + 0.5, 820, 1000, 0.56, [("RAMCHARITMANAS", 34, MONO_FONT), ("ARANYA KAND, DOHA 34", 46,
                                                                                         HEAD_FONT)],
                 rot=0.04, rod=False, t_out=tM)
        plate(cr, t, tA, "SO SWEET!", top[0], top[1], 40, color=RED, t_out=tA + 0.8)
        plate(cr, t, tA + 0.8, "WONDERFUL!", top[0], top[1], 40, color=RED, t_out=tC - 0.1)
    return dict(ui=ui, flash=flash_at(t, tM, 0.15) + flash_at(t, tC + 0.1, 0.25))


# ------------------------------------------------------------------ sb11  added later: songs and stories


BUB11 = (610, 850, 0.86)
SG11 = (250, 0.72)


def bubble_tasting(cr, t, bx, by, bs, t_in, alpha=1.0):
    """Inside the cloud: the picture people know: little Shabari biting a berry, then holding it out to little Rama."""
    cr.save()
    cr.new_path()
    pc.ell(cr, bx, by, 280 * bs, 190 * bs)
    cr.clip()
    a = alpha * prog(t, t_in, 0.3)
    feet = by + 168 * bs
    ss = 0.3 * bs / 0.86
    sx = bx - 130 * bs
    cyc = ((t - t_in) / 2.2) % 1.0
    bite = cyc < 0.5
    hip = feet - 470 * ss
    tgt = local(sx, hip, ss, 0.0, False, 74, -362) if bite else (bx + 20 * bs, feet - 420 * ss)
    fr = reach_arm(sx, hip, ss, SB.SHA_SHOULDER_F[0], tgt)
    pts = sha(cr, t, sx, ss, mood="shut" if bite else "smile", front=fr, feet=feet, rods=False, alpha=a, ph=0.4)
    hf = to_user(cr, pts["handF"])
    prop(cr, "sb_ber_bit", hf[0] + 4, hf[1] - 8, 2.4 * ss, alpha=a)
    rs = 0.29 * bs / 0.86
    rama_(cr, t, bx + 160 * bs, rs, mood="smile", feet=feet, flip=True, rods=False, alpha=a,
          front=(-1.2, -0.5) if not bite else (-0.5, -0.4))
    cr.restore()


def story_books(cr, t, x, y, s, alpha=1.0, blur=0.0):
    """A small heap of later story books (plain cloth covers, the tasted-berry picture on each)."""
    for i, (dx, dy, r, nm) in enumerate(((-60, 40, -0.25, "sb_cov_t"), (50, 20, 0.18, "sb_cov_v"),
                                         (-5, -20, -0.04, "sb_cov_t"))):
        cr.save()
        cr.translate(x + dx * s, y + dy * s)
        cr.rotate(r)
        cr.scale(s, s)
        pc.paint_part(cr, nm, alpha, blur)
        cr.restore()
        prop(cr, "sb_ber3_bit", *local(x + dx * s, y + dy * s, s, r, False, 0, 128), s=0.95 * s, rot=r, alpha=alpha,
             blur=blur)


def s_later(cr, t, tl, t0, t1):
    c = cues(tl, "sb11")
    tL, tK, tB = c["L"], c["K"], c["B"]
    glow(cr, 540, 1300, 600, 0.4)
    ground(cr)
    bx, by, bs = BUB11
    q = back(clamp((t - t0 - 0.1) / 0.35), 1.5)
    if q > 0.01:
        prop(cr, "ar_think", bx, by, bs * (0.6 + 0.4 * q), rot=sway(t, 0.006, 0.4), alpha=clamp(q), flip=True)
        if q > 0.8:
            bubble_tasting(cr, t, bx, by - 10, bs, t0 + 0.3)
    if t > tK - 0.3:                                        # the later story books
        b, k, a = depth(t, tK - 0.3, 0.45)
        story_books(cr, t, 850, G - 170, 0.4 * k, a, b)
    x, s = SG11
    b, k, a = depth(t, tL - 0.3, 0.5)
    singing = t > tB - 0.1
    mood = ("sing" if int(t * 3.2) % 2 else "sing2") if singing else "calm"
    lamp_s = 0.62
    fr = (-1.35, -0.65)
    pts = puppet(cr, SB.SINGER, x, G - 434 * s * k, s * k, bob_rot(t, 0.7, 0.012), False,
                 man_angles("sb_sing", t, fr, (0.3, -0.9), -0.06 if singing else 0.0, (0.0, 0.0),
                            [(tB, 0.3)], 0.7), a, b, swap={"sb_sing_head": "sb_sing_head" + (
                                "" if mood == "calm" else "_" + mood)},
                 extra={"sb_sing_armF_lo": held("c6_handlamp", fr, lamp_s, 170, alpha=a, blur=b)})
    hf = to_user(cr, pts["handF"])
    if a > 0.3:
        glow(cr, hf[0] + 10, hf[1] - 60, 200, 0.6 * a * (0.85 + 0.15 * math.sin(t * 7)))
    hd = to_user(cr, pts["head"])
    notes(cr, t, tB, hd[0] + 40, hd[1] + 20)
    st_dev = cr.user_to_device(850, G - 340)
    sg_dev = cr.user_to_device(x + 20, G - 1130 * s)

    def ui(cr):
        if t < tK - 0.1:
            head2(cr, t, "THE TASTED BERRIES CAME", t0 + 0.05, "MUCH LATER", tL, big_size=260)
        else:
            head2(cr, t, "FROM LATER", tK - 0.1, "SONGS & STORIES", tB, big_size=230)
        plate(cr, t, tK, "STORIES", st_dev[0], st_dev[1], 36)
        plate(cr, t, tB, "BHAJANS", sg_dev[0], sg_dev[1], 36)
    return dict(ui=ui, flash=flash_at(t, tL, 0.15) + flash_at(t, tB, 0.15))


# ------------------------------------------------------------------ sb12  reveal: but Valmiki has a real miracle


def s_reveal(cr, t, tl, t0, t1):
    c = cues(tl, "sb12")
    tV, tS, tA, tC = c["V"], c["S"], c["A"], c["C"]
    dim = prog(t, t0, 0.8)
    bright = prog(t, tC - 0.1, 0.5)
    gl = 0.25 + 0.35 * prog(t, tV, 1.2) + 0.5 * bright
    if t > tS - 0.3:                                        # Shabari comes to look at the book
        b, k, a = depth(t, tS - 0.3, 0.5)
        sha(cr, t, 880, 0.5 * k, mood="look" if t < tC else "joy", flip=True, alpha=a, blur=b, ph=0.4,
            front=(-0.9, -0.7), head=-0.06)
    pulse = prog(t, tA, 0.3) * (1 - bright) * (0.5 + 0.5 * math.sin((t - tA) * 12))

    def med(cr_, a):
        if bright < 1:
            k = 1 + 0.15 * pulse
            draw_text(cr_, "?", 0, 116, int(190 * k), RED, a * (1 - bright), anchor="cm")
        if bright > 0:
            prop(cr_, "sb_bloom", 0, 160, 0.6 * (0.6 + 0.4 * back(clamp(bright), 1.6)), alpha=a * clamp(bright * 2))
    cover(cr, t, t0 + 0.05, 540, 1180, 1.1, "v", glow_a=gl, med_fn=med)
    if t > tC:
        burst(cr, t, 540, 1180 + 110 * 1.1, tC, n=20, rmax=700, alpha=0.7)
        lights(cr, t, 540, 1300, 300, 12, 0.8 * bright)

    def ui(cr):
        head2(cr, t, "BUT VALMIKI HAS A", t0 + 0.05, "REAL MIRACLE", tC, big_size=240, under=tC + 0.4)
    return dict(ui=ui, night=0.32 * dim * (1 - 0.6 * bright), lift=1.0, flash=flash_at(t, tC, 0.45))


# ------------------------------------------------------------------ sb13  the flowers were still fresh


VEDI = (540, 1.0)


def s_flowers(cr, t, tl, t0, t1):
    c = cues(tl, "sb13")
    tY, tF, tT, tM = c["Y"], c["F"], c["T"], c["M"]
    forest(cr, t, alpha=0.7, blur=5, hut_x=980, hut_s=0.48)
    vx, vs = VEDI
    top = G - 180 * vs
    fresh = prog(t, tT - 0.1, 0.4)
    glow(cr, vx, top - 80, 380, 0.3 + 0.4 * fresh)
    prop(cr, "sb_vedi", vx, G + 4, vs)
    prop(cr, "sb_bloom", vx, top + 8, vs * (1 + 0.04 * math.sin(t * 2)), rot=sway(t, 0.02, 0.5))
    if t > tT:
        lights(cr, t, vx, top - 60, 180, 9, 0.8 * fresh)
    rama_(cr, t, 150, 0.58, mood="smile", front=(-0.6, -0.5), head=0.08, ph=0.5)
    point = keyed(t, [(t0, 0.0), (tF - 0.1, 1.0)], 0.3, 1.3)
    sha(cr, t, 930, 0.6, mood="smile", flip=True, front=mix((-0.4, -0.4), (-1.5, -0.2), point),
        backa=(0.2, -0.4), ph=0.4, hits=[(tF, 0.3)])

    def ui(cr):
        if t < tF - 0.1:
            head2(cr, t, "THE SAGES HAD LEFT", t0 + 0.05, "YEARS AGO...", tY, big_size=250)
        elif t < tM - 0.1:
            head2(cr, t, "BUT THEIR FLOWERS WERE", tF - 0.1, "STILL FRESH!", tT, big_size=250, under=tT + 0.4)
        else:
            head2(cr, t, "THEY HAD", tM - 0.1, "NOT WILTED!", tM, big_size=270)
        if tY - 0.1 < t < tF:
            year_leaf(cr, t, tY, max(tY + 1.0, tF - 0.3), 540, 800, 1.0, n=15,
                      alpha=prog(t, tY - 0.1, 0.3) * (1 - prog(t, tF - 0.2, 0.2)))
        if t > tF:
            red_ring(cr, vx, top - 40, 230, 120, prog(t, tF, 0.4), 9)
        if t > tM - 0.2:                                    # what you'd expect after years: wilted (crossed out)
            q = back(clamp((t - tM + 0.2) / 0.35), 1.4)
            cx, cy = 560, 900
            dotted(cr, [(cx + 170 * math.cos(a_), cy + 120 * math.sin(a_)) for a_ in
                        (2 * math.pi * i / 40 for i in range(41))], clamp(q), 26, 5, INK, 0.6)
            prop(cr, "sb_bloom_dry", cx, cy + 40, 0.6 * q)
            big_x(cr, cx, cy, 220, 180, prog(t, tM + 0.2, 0.3), lw=18)
    return dict(ui=ui, flash=flash_at(t, tT, 0.3) + flash_at(t, tM, 0.15))


# ------------------------------------------------------------------ sb14  the clothes were still wet


TREE14 = (960, 0.8)
CLOTHS = ((-260, -824, 0.62), (-440, -850, 0.66), (-620, -858, 0.6))


def s_clothes(cr, t, tl, t0, t1):
    c = cues(tl, "sb14")
    tS, tK, tW = c["S"], c["K"], c["W"]
    tx, ts = TREE14
    prop(cr, "tree", 120, G + 10, 0.5, alpha=0.4, blur=10, flip=True)
    ground(cr)
    prop(cr, "dv_tree", tx, G + 6, ts, rot=sway(t, 0.003, 0.3))
    wet = prog(t, tW - 0.1, 0.4)
    hems = []
    for i, (dx, dy, cs) in enumerate(CLOTHS):
        b, k, a = depth(t, tS - 0.35 + 0.15 * i, 0.4)
        px, py = tx + dx * ts, G + 6 + dy * ts
        sw = sway(t, 0.03, 0.4, i)
        prop(cr, "sb_bark", px, py, cs * k, rot=sw, alpha=a, blur=b)
        hems.append((px - math.sin(sw) * 280 * cs, py + 285 * cs, a))
        if wet > 0:
            for j in range(3):
                sparkle(cr, px - 40 * cs + 40 * cs * j, py + (60 + 70 * j) * cs, 22 * (0.6 + 0.4 * math.sin(
                    t * 5 + i + j)), 0.8 * wet)
    for i, (hx, hy, a) in enumerate(hems):                  # drips falling to the ground
        rate = 0.35 + 1.2 * wet
        for j in range(3):
            u = ((t - t0) * rate * 1.4 + j / 3 + i * 0.29) % 1.0
            if a < 0.5:
                continue
            dx_ = (j - 1) * 30
            y = hy + (G - hy) * u * u
            prop(cr, "dv_drop", hx + dx_, y, 1.1, alpha=0.9 * (1 - 0.3 * u))
            if u > 0.92:                                    # a little splash ring where it lands
                cr.save()
                cr.set_source_rgba(0.45, 0.62, 0.85, 0.5)
                cr.set_line_width(3)
                cr.new_path()
                pc.ell(cr, hx + dx_, G - 4, 30 * (u - 0.9) * 20, 6)
                cr.stroke()
                cr.restore()
    point = keyed(t, [(t0, 0.0), (tK, 1.0)], 0.3, 1.3)
    sha(cr, t, 200, 0.6, mood="smile" if t < tW else "joy", front=mix((-0.3, -0.4), (-2.4, -0.3), point),
        backa=(0.2, -0.4), head=-0.12 * point, ph=0.4, hits=[(tW, 0.3)])

    def ui(cr):
        if t < tW - 0.1:
            head2(cr, t, "THE SAGES' CLOTHES,", t0 + 0.05, "HUNG TO DRY", tS, big_size=250)
        else:
            head2(cr, t, "AFTER YEARS, STILL", tW - 0.1, "WET!", tW, big_size=320, under=tW + 0.4)
        if t > tK:
            red_ring(cr, tx + CLOTHS[1][0] * ts, G + CLOTHS[1][1] * ts + 120, 300, 170, prog(t, tK, 0.4), 9)
    return dict(ui=ui, flash=flash_at(t, tW, 0.3))


# ------------------------------------------------------------------ sb15  her wait was over; she went to her gurus


RM15 = (330, 0.68)
SH15 = (730, 0.68)
GURU = ((370, 860), (710, 860))


def s_end_wait(cr, t, tl, t0, t1):
    c = cues(tl, "sb15")
    tM, tP, tG, tH = c["M"], c["P"], c["G"], c["H"]
    forest(cr, t, alpha=0.8, blur=4, hut_x=980, hut_s=0.5)
    gq = prog(t, tG - 0.3, 0.7)
    for i, (gx, gy) in enumerate(GURU):                     # her gurus' lights in the sky
        if gq > 0.01:
            glow(cr, gx, gy, 260, 0.75 * gq)
            warm(cr, gx, gy, 200, 0.7 * gq)
            sage_sit(cr, t, "AB"[i], gx, gy + 120, 0.36, mood="smile", flip=i == 1, alpha=0.45 * gq, blur=5,
                     rods=False, front=(-1.4, -0.4) if i == 0 else (-1.4, -0.4), ph=i)
    rx, rs = RM15
    bless = keyed(t, [(t0, 0.0), (tP - 0.2, 1.0)], 0.3, 1.3)
    look = prog(t, tG, 0.6)
    rama_(cr, t, rx, rs, mood="smile", front=mix((-0.45, -0.5), (-1.9, -0.6), bless), head=-0.14 * look, ph=0.5,
          hits=[(tP - 0.2, 0.4)])
    x, s = SH15
    bow = keyed(t, [(t0, 0.0), (tM, 0.38), (tP + 0.3, 0.08)], 0.35, 1.2)
    fade = clamp((t - tG) / 1.1)
    hip = G - 470 * s
    if fade < 1:
        glow(cr, x, hip - 300 * s, 380, 0.6 * fade)
        sha(cr, t, x, s, mood="joy", flip=True, rot=-bow, ph=0.4, alpha=1 - fade, blur=10 * fade, rods=fade < 0.3,
            **ANJALI)
    rise(cr, t, tG + 0.3, (x, hip - 300 * s), (540, 820), 1.6, 44)

    def ui(cr):
        if t < tG - 0.1:
            head2(cr, t, "MEETING RAMA, HER", t0 + 0.05, "WAIT WAS OVER", tP, big_size=240)
        else:
            head2(cr, t, "SHE WENT UP TO", tG - 0.1, "HER GURUS", tG + 0.1, big_size=260)
    return dict(ui=ui, flash=flash_at(t, tP, 0.15) + flash_at(t, tH, 0.3), night=0.12 * gq, lift=1.0)


# ------------------------------------------------------------------ sb15c  callback: tasted or not, her wait was true


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "sb15c")
    tJ, tI, tD, tS = c["J"], c["I"], c["D"], c["S"]
    x, s, feet = HK
    glow(cr, x + 140, feet - 760 * s, 660, 0.42 + 0.25 * prog(t, tS, 0.5))
    flick = tJ < t < tI
    bit = (int((t - tJ) / 0.4) % 2 == 0) if flick else (t <= tJ)
    bp = hook_figure(cr, t, 1.0, "joy" if t > tS else "smile", hits=[(tS, 0.3)], glint=0.6, bit=bit)
    if t > tS:
        warm(cr, x + 60, feet - 700 * s, 520, 0.4 * prog(t, tS, 0.5))
        lights(cr, t, x + 40, feet - 800 * s, 300, 10, 0.7 * prog(t, tS, 0.5))

    def ui(cr):
        head2(cr, t, "TASTED OR NOT...", t0 + 0.05, "HER WAIT WAS TRUE", tI + 0.1, big_size=210, under=tS)
        if flick:
            qmark(cr, t, tJ, bp[0] + 90, bp[1] - 90, 120, RED)
        for i, wh in enumerate(("v", "t")):
            cover(cr, t, tD - 0.2 + 0.15 * i, 360 + 380 * i, 745, 0.42, wh, med="sb_sha_head_joy", med_s=0.95,
                  tick_t=tD + 0.25 + 0.15 * i)
    return dict(ui=ui, flash=flash_at(t, tI, 0.2) + flash_at(t, tD, 0.15))


# ------------------------------------------------------------------ sb16  which do you believe?


CARDS16 = ((290, "TASTED", "BERRIES"), (790, "VALMIKI'S", "STORY"))


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "sb16")
    tK, tJ, tV, tC = c["K"], c["J"], c["V"], c["C"]
    glow(cr, 540, 1400, 560, 0.42)
    ground(cr)
    if tJ < t < tV:                                         # she turns to whichever card is ringed
        face_left = True
    elif t >= tV:
        face_left = int((t - tV) / 0.9) % 2 == 1
    else:
        face_left = False
    sha(cr, t, 540, 0.5, mood="look", head=-0.1, ph=0.4, front=(-0.6, -0.6), flip=face_left,
        hits=[(tJ, 0.3), (tV, 0.3)])

    def ui(cr):
        head2(cr, t, "WHICH DO YOU", t0 + 0.05, "BELIEVE?", tK, big_size=280)
        for i, (cx, l1, l2) in enumerate(CARDS16):
            tin = t0 + 0.25 + 0.15 * i
            q = back(clamp((t - tin) / 0.35), 1.4)
            if q > 0.01:
                if i == 0:
                    prop(cr, "sb_ber3_bit", cx, 790 + 60 * (1 - q), 1.25 * q, rot=sway(t, 0.03, 0.4))
                else:
                    cover(cr, t, None, cx, 770 + 60 * (1 - q), 0.4 * q, "v", med="sb_bloom", med_s=0.5, rods=False)
            card(cr, t, tin, cx, 1060, 0.56, [(l1, 96, INK, -44), (l2, 104, RED, 52)])
        if t > tJ:
            if t < tV:
                k, ts = 0, tJ
            else:
                n = int((t - tV) / 0.9)
                k, ts = (1 + n) % 2, tV + 0.9 * n
            red_ring(cr, CARDS16[k][0], 930, 240, 250, prog(t, ts, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tK, 0.15))


SHOTS = [   # (line, cue: None = line start, draw function, options)
    ("sb1", None, s_hook, {"z": (1.0, 1.04)}),
    ("sb2", None, s_books, {"z": (1.0, 1.03)}),
    ("sb3", None, s_serve, {"z": (1.0, 1.03)}),
    ("sb4", None, s_promise, {"z": (1.0, 1.03)}),
    ("sb5", None, s_alone, {"z": (1.0, 1.04)}),
    ("sb6", None, s_years, {"z": (1.0, 1.03)}),
    ("sb7", None, s_came, {"z": (1.0, 1.04)}),
    ("sb8", None, s_offer, {"z": (1.0, 1.03)}),
    ("sb8q", None, s_question, {"z": (1.0, 1.03)}),
    ("sb9", None, s_valmiki, {"z": (1.0, 1.03)}),
    ("sb10", None, s_tulsi, {"z": (1.0, 1.03)}),
    ("sb11", None, s_later, {"z": (1.0, 1.03)}),
    ("sb12", None, s_reveal, {"z": (1.0, 1.06)}),
    ("sb13", None, s_flowers, {"z": (1.0, 1.03)}),
    ("sb14", None, s_clothes, {"z": (1.0, 1.04)}),
    ("sb15", None, s_end_wait, {"z": (1.0, 1.03)}),
    ("sb15c", None, s_callback, {"z": (1.0, 1.04)}),
    ("sb16", None, s_end, {"z": (1.0, 1.03)}),
]


def _starts(tl):
    """Each shot's start (cached on the timeline under this module's own name, not shots.shot_at's)."""
    st = getattr(tl, "_sb_shot_starts", None)
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
        tl._sb_shot_starts = st
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
    title_lift(cr, out.get("lift", 0.0) * out.get("night", 0.0) / NIGHT)
    if out.get("ui"):
        out["ui"](cr)
    if k > 0 and t - t0 < 0.22:                     # the lamp dips for a moment on a scene change
        cr.set_source_rgba(0.02, 0.01, 0.0, 0.35 * (1 - (t - t0) / 0.22))
        cr.paint()
    pc.finish(cr, t)


def sfx(tl):
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, shimmer
    on the real miracle, a conch as Rama arrives, a bell on the closing question, then (only where they fit) a hit on
    "not in either book", a bell on the fresh flowers, shimmer as she rises to her gurus and a hit on "no tasting".
    Chosen in THAT order of importance, each at least SFX_MIN_GAP from every sound already kept (as
    render_myth.calm_sfx keeps them), so the list returned is what plays (about 6 sounds); the bed dips before the
    reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["sb12"]["C"], "shimmer", 0), (c["sb7"]["C"], "conch", 0),
            (c["sb16"]["K"], "bell", 0), (c["sb2"]["M"] + 0.15, "hit", 0), (c["sb13"]["T"], "bell", 0),
            (c["sb15"]["G"], "shimmer", 0), (c["sb9"]["C"] + 0.1, "hit", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["sb8q"]["t0"] - 0.3, "dip", 0.4), (c["sb9"]["C"] - 0.3, "dip", 0.45),
            (c["sb12"]["C"] - 0.35, "dip", 0.5)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
