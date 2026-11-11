"""Scenes for videos/dharmavyadha.py: "A butcher taught dharma to a sage" (Kaushika and the Dharmavyadha, Mahabharata,
Vana Parva 205-214), in Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit
screen, two-tier headlines and rod-puppet motion as the Jarasandha, Kaikeyi, Lakshman Rekha, Mandhata, Jayadratha,
Arjuna and Ruru reels, with the cast from dharmavyadha_cast. A debate told so a child can follow: one plain label per
step, and the same three places come back (the tree, the housewife's door, the butcher's home) so every shot reads at
once.

Respect: the proud sage is humbled, never mocked (the drop on his head is the one light moment); the housewife is calm
and sure; the butcher is kind and dignified, his stall shows only plain hanging shapes and a chopping block; the old
parents keep their dignity. No gore at all: the crane falls softly with its eyes shut and lies as if asleep; the
"flash" of the sage's anger is a line of light.

Every frame is a pure function of t. English on-screen text (shared by Hindi and Kannada) except the butcher's own
words on d14, which show in the viewer's script (यही मेरे भगवान हैं / ಇವರೇ ನನ್ನ ದೇವರು, shaped by matplotlib as in
scenes_arjuna; without the Nirmala font they are left out). Cues are words of the line in each language ({"hi": ...,
"kn": ...}) with a fraction fallback, kept in one table (CUES) that the scenes and sfx() both read, with minimum gaps so
a fast voice can't bunch the beats together.

Shot list (line: what is on the screen)
  d1  HOOK, frame 0: Kaushika alone and large, glaring up; a line of light runs from his eye to a white crane already
      falling softly behind him (feathers drifting): A SAGE'S ONE ANGRY LOOK / KILLED A BIRD (big words in by 0.3 s,
      underlined as it lands, on "mar"); his eye flashes again on "nazar"; on "kasai" his face turns to shock and a
      card drops in: ...THEN A BUTCHER / TAUGHT HIM DHARMA (red on "dharm")
  d2  THIS IS NOT A / FILM STORY (crossed out); a palm-leaf book rises and opens: MAHABHARATA, BOOK 3: VANA PARVA
      (ringed), SECTIONS 205-214; IT'S WRITTEN IN THE / MAHABHARATA
  d3  a big tree comes in; Kaushika sits cross-legged under its bare branch reading a palm leaf, the Veda bundle beside
      him (tag SAGE KAUSHIKA): A SAGE NAMED / KAUSHIKA, then UNDER A TREE, READING THE / VEDAS (the leaf glows)
  d4  a white crane flies in and lands on the branch above him: ON THE BRANCH ABOVE: A / CRANE; a white drop falls on
      his bun, a little splat, his face jumps: AND THEN, ON HIS HEAD... / SPLAT!
  d5  he looks up in anger; a line of light from his eyes hits the crane: HE LOOKED UP IN ANGER: / ONE ANGRY LOOK; it
      falls softly (eyes shut) and lies on the ground: AND THE CRANE / FELL DEAD (in ink)
  d6  he kneels by the bird, a hand to his brow, a tear: THE SAGE FELT VERY / SAD; a cloud IN ANGER... / WHAT HAVE I
      DONE?
  d7  a village house; he walks up with his begging bowl: HE WENT TO A HOUSE TO ASK FOR / FOOD; the housewife appears
      in the doorway (tag THE HOUSEWIFE), a water pot by the door; she raises her hand: THE WOMAN OF THE HOUSE SAID: /
      PLEASE WAIT
  d8  the house cut open by its wall: outside the sage waits with his bowl; inside, her tired husband walks in with
      his hoe: THEN HER HUSBAND CAME HOME / HUNGRY; he sits, she sets his food before him: SHE FED HER / HUSBAND FIRST;
      a sun crosses a dotted arc like a clock; the sage taps his foot (tag STILL WAITING...): AND THE SAGE? / KEPT
      WAITING
  d9  at the door: THE SAGE GOT / ANGRY, a weak line of light from his eyes fizzles out half-way; she speaks calmly:
      speech cloud I AM NOT A / CRANE! / ...TO DIE FROM YOUR LOOK; his face turns to shock
  d10 close on him, frozen in shock: THE SAGE WAS / SHOCKED; a thought bubble with the crane lying under the tree; a
      big red "?": HOW DID SHE / KNOW?
  d11 she points far away; a dotted road draws itself to the skyline of a city (tag MITHILA): SHE SAID: YOU DON'T KNOW
      / DHARMA, GO TO / MITHILA..., then a tiny butcher at its gate (tag A BUTCHER): ...A BUTCHER WILL / TEACH YOU
  d12 the Mithila market: the stall (plain hanging shapes, a chopping block, a weighing scale), the butcher behind his
      counter (tag THE BUTCHER), the sage walks in: IN MITHILA'S MARKET: A / BUTCHER; the butcher looks up and smiles:
      HE SAW THE SAGE AND SMILED:, speech cloud SHE SENT YOU, / RIGHT?; the sage's jaw drops
  d13 the butcher's home: he walks in with the sage: HE TOOK THE SAGE / HOME; his old parents on a bench light up and
      smile (tags HIS FATHER, HIS MOTHER): THERE SAT HIS OLD / PARENTS
  d14 closer: THE BUTCHER SAID: / MY PARENTS = MY GODS with his words in the viewer's script under it; he kneels with
      folded hands while water falls gently over his parents, pours water over his father's feet into a basin, then
      holds up a plate of food; a note ticks I BATHE THEM / I WASH THEIR FEET / I FEED THEM
  d15 he turns to the sage and points gently: THE BUTCHER ASKED: / AND YOU?; YOU LEFT YOUR PARENTS / WITHOUT A WORD;
      the sage's head sinks; a thought bubble: his old parents alone outside a hut
  d16 FLASHBACK (sepia, FAR AWAY..., a pale moon and stars): the sage's own old parents alone on a rope cot by their
      hut, eyes closed, tears: THEY WENT BLIND WITH / GRIEF (their eyes ringed); the sepia lifts, a dotted road draws
      itself to them: GO, SERVE THEM / FIRST
  d17 the same hut at sunrise: the sage walks in with folded hands: AND THE SAGE REALLY / WENT HOME; he kneels, bows
      low and touches his father's feet; the father's hand on his head, the mother's raised in blessing, both smile:
      TO SERVE HIS PARENTS, / HE WENT HOME
  d18 WHO IS MORE / RIGHTEOUS?; cards THE SAGE? (READS THE VEDAS) / THE BUTCHER? (SERVES HIS PARENTS), a red ring
      alternating; the two of them small below, the sage reading, the butcher with a plate
"""
import math

import cairo

import dharmavyadha_cast as DV
import puppet_core as pc
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, MONO_FONT, back, clamp, draw_text, ease, prog, tick
from puppet_core import H, W, depth, keyed, prop, puppet, sway
from scenes_arjuna import HAS_INDIC, card2, cloud_text, indic_surface
from scenes_jarasandha import FADE, FEET, INK, RED, bob_rot, glow, man_angles, motes, red_ring, stars, woman_angles
from scenes_jayadratha import NIGHT, flash_at, tag, tint, title_lift, to_user
from scenes_kaikeyi import ANJALI, card, fig
from scenes_lakshman_rekha import big_q, big_x, book, sparkle, walk_at
from scenes_mandhata import held, lights, local, mix, reach_arm, warm
from scenes_ravana import dotted, head2
from scenes_ruru import plate, sepia
from shots import T, shot_at

MISSES = set()                       # cue words not found in a line (falls back to fractions)
QUOTE = {"hi": "यही मेरे भगवान हैं", "kn": "ಇವರೇ ನನ್ನ ದೇವರು"}     # the butcher's words (d14), in the viewer's script
G = FEET + 120                       # the ground line of most sets


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
    "d1": (("G", {"hi": "भरी", "kn": "ನೋಟಕ್ಕೆ"}, 0.3, (("t0", 0.6),)),
           ("D", {"hi": "मर", "kn": "ಸತ್ತುಹೋಯ್ತು"}, 0.5, (("G", 0.5),)),
           ("B", {"hi": "कसाई", "kn": "ಕಟುಕ"}, 0.78, (("D", 0.9),)),
           ("M", {"hi": "धर्म", "kn": "ಧರ್ಮ"}, 0.88, (("B", 0.35),))),
    "d2": (("X", {"hi": "नहीं", "kn": "ಅಲ್ಲ"}, 0.3, (("t0", 0.6),)),
           ("M", {"hi": "महाभारत", "kn": "ಮಹಾಭಾರತದ"}, 0.55, (("X", 0.5),)),
           ("P", {"hi": "वन", "kn": "ವನ"}, 0.75, (("M", 0.5),))),
    "d3": (("K", {"hi": "कौशिक", "kn": "ಕೌಶಿಕ"}, 0.02, ()),
           ("T", {"hi": "नीचे", "kn": "ಮರದ"}, 0.4, (("K", 0.9),)),
           ("V", {"hi": "वेद", "kn": "ವೇದ"}, 0.7, (("T", 0.6),))),
    "d4": (("C", {"hi": "बगुले", "kn": "ಕೊಕ್ಕರೆ"}, 0.3, (("t0", 0.35),)),
           ("S", {"hi": "बीट", "kn": "ಹಿಕ್ಕೆ"}, 0.75, (("C", 0.9),))),
    "d5": (("A", {"hi": "ऊपर", "kn": "ಕೋಪದಿಂದ"}, 0.15, (("t0", 0.3),)),
           ("L", {"hi": "देखा", "kn": "ನೋಡಿದ್ರು"}, 0.4, (("A", 0.4),)),
           ("D", {"hi": "बगुला", "kn": "ಕೊಕ್ಕರೆ"}, 0.6, (("L", 0.5),)),
           ("F", {"hi": "गिर", "kn": "ಬಿತ್ತು"}, 0.85, (("D", 0.5), ("L", 1.3)))),
    "d6": (("S", {"hi": "दुख", "kn": "ಬೇಜಾರಾಯ್ತು"}, 0.25, (("t0", 0.4),)),
           ("W", {"hi": "क्या", "kn": "ಏನು"}, 0.75, (("S", 1.0),))),
    "d7": (("A", {"hi": "भिक्षा", "kn": "ಭಿಕ್ಷೆ"}, 0.2, (("t0", 0.4),)),
           ("Wf", {"hi": "औरत", "kn": "ಹೆಂಗಸು"}, 0.62, (("A", 1.0),)),
           ("P", {"hi": "रुकिए", "kn": "ಸ್ವಲ್ಪ"}, 0.85, (("Wf", 0.5),))),
    "d8": (("Hb", {"hi": "पति", "kn": "ಗಂಡ"}, 0.1, (("t0", 0.2),)),
           ("Hu", {"hi": "भूखा", "kn": "ಹಸಿವಿಂದ"}, 0.2, (("Hb", 0.4),)),
           ("F", {"hi": "पहले", "kn": "ಮೊದಲು"}, 0.45, (("Hu", 1.2),)),
           ("E", {"hi": "खाना", "kn": "ಊಟ"}, 0.6, (("F", 0.6),)),
           ("Wt", {"hi": "करवाया", "kn": "ಕಾಯಿಸಿದ್ಳು"}, 0.85, (("E", 0.9),))),
    "d9": (("A", {"hi": "आया", "kn": "ಕೋಪ"}, 0.1, (("t0", 0.3),)),
           ("S", {"hi": "बोली", "kn": "ಹೇಳಿದ್ಳು"}, 0.35, (("A", 0.9),)),
           ("C", {"hi": "बगुला", "kn": "ಕೊಕ್ಕರೆ"}, 0.55, (("S", 0.6),)),
           ("L", {"hi": "मर", "kn": "ನೋಟಕ್ಕೆ"}, 0.8, (("C", 0.7),))),
    "d10": (("Sh", {"hi": "हैरान", "kn": "ಶಾಕ್"}, 0.1, (("t0", 0.2),)),
            ("J", {"hi": "जंगल", "kn": "ಕಾಡಲ್ಲಿ"}, 0.4, (("Sh", 0.7),)),
            ("K", {"hi": "कैसे", "kn": "ಹೇಗೆ"}, 0.8, (("J", 0.8),))),
    "d11": (("D", {"hi": "जानते", "kn": "ಗೊತ್ತಿಲ್ಲ"}, 0.2, (("t0", 0.5),)),
            ("M", {"hi": "मिथिला", "kn": "ಮಿಥಿಲೆಗೆ"}, 0.35, (("D", 0.7),)),
            ("B", {"hi": "कसाई", "kn": "ಕಟುಕ"}, 0.7, (("M", 1.2),)),
            ("T", {"hi": "सिखाएगा", "kn": "ಕಲಿಸ್ತಾನೆ"}, 0.92, (("B", 0.5),))),
    "d12": (("M", {"hi": "मिथिला", "kn": "ಮಿಥಿಲೆಗೆ"}, 0.05, ()),
            ("B", {"hi": "कसाई", "kn": "ಕಟುಕ"}, 0.2, (("t0", 0.8),)),
            ("L", {"hi": "देखते", "kn": "ನೋಡಿದ"}, 0.6, (("B", 1.4),)),
            ("Q", {"hi": "भेजा", "kn": "ಕಳಿಸಿದ್ಳು"}, 0.88, (("L", 0.9),))),
    "d13": (("H", {"hi": "घर", "kn": "ಮನೆಗೆ"}, 0.3, (("t0", 0.4),)),
            ("O", {"hi": "उसके", "kn": "ವಯಸ್ಸಾದ"}, 0.6, (("H", 0.8),)),
            ("P", {"hi": "बैठे", "kn": "ಅಪ್ಪ"}, 0.75, (("O", 0.4),))),
    "d14": (("G", {"hi": "भगवान", "kn": "ದೇವರು"}, 0.2, (("t0", 0.4),)),
            ("Ba", {"hi": "नहलाता", "kn": "ಸ್ನಾನ"}, 0.5, (("G", 1.0),)),
            ("F", {"hi": "पैर", "kn": "ಕಾಲು"}, 0.68, (("Ba", 0.8),)),
            ("E", {"hi": "खाना", "kn": "ಊಟ"}, 0.85, (("F", 0.8),))),
    "d15": (("Y", {"hi": "आप", "kn": "ನೀವು"}, 0.2, (("t0", 0.3),)),
            ("W", {"hi": "बिना", "kn": "ಹೇಳದೆ"}, 0.5, (("Y", 0.9),)),
            ("L", {"hi": "तपस्या", "kn": "ತಪಸ್ಸಿಗೆ"}, 0.82, (("W", 0.7),))),
    "d16": (("Bl", {"hi": "अंधे", "kn": "ಕುರುಡರಾಗಿದ್ದಾರೆ"}, 0.35, (("t0", 0.6),)),
            ("Go", {"hi": "जाइए", "kn": "ಹೋಗಿ"}, 0.6, (("Bl", 0.9),)),
            ("S", {"hi": "सेवा", "kn": "ಸೇವೆ"}, 0.85, (("Go", 0.5),))),
    "d17": (("R", {"hi": "सच", "kn": "ನಿಜವಾಗಲೂ"}, 0.15, (("t0", 0.3),)),
            ("S", {"hi": "सेवा", "kn": "ಸೇವೆ"}, 0.55, (("R", 1.1),)),
            ("H", {"hi": "लौट", "kn": "ವಾಪಸ್"}, 0.8, (("S", 0.6),))),
    "d18": (("Q", {"hi": "कौन", "kn": "ಯಾರು"}, 0.2, (("t0", 0.3),)),
            ("S", {"hi": "ऋषि", "kn": "ಋಷಿನಾ"}, 0.4, (("Q", 0.4),)),
            ("B", {"hi": "कसाई", "kn": "ಕಟುಕನಾ"}, 0.75, (("S", 0.8),)),
            ("C", {"hi": "कमेंट", "kn": "ಕಾಮೆಂಟ್"}, 0.88, (("B", 0.5),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline)."""
    cache = getattr(tl, "_dv_cues", None)
    if cache is None:
        cache = {}
        tl._dv_cues = cache
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


# ------------------------------------------------------------------ puppets


def kau(cr, t, x, s, mood="calm", bowl=None, leaf=None, kneel=False, front=(-0.32, -0.55), **kw):
    """Kaushika standing (feet on `feet`) or kneeling; bowl / leaf = the scale of the begging bowl / palm leaf in his
    front hand."""
    sw = {"dv_kau_head": "dv_kau_head" + ("" if mood == "calm" else "_" + mood)}
    a, b = kw.get("alpha", 1.0), kw.get("blur", 0.0)
    ex = {}
    if bowl:
        ex["dv_kau_armF_lo"] = held("dv_bowl", front, bowl, 176, 0.0, a, b)
    if leaf:
        ex["dv_kau_armF_lo"] = held("dv_pleaf", front, leaf, 168, 0.0, a, b)
    return fig(cr, DV.KAU, "dv_kau", t, x, s, front=front, swap=sw, extra=ex or None,
               kneel="dv_kau_kneel" if kneel else None, **kw)


def sitter(cr, rig, key, t, x, ground, s, seat=None, seat_h=DV.SEAT_H, head_sprite=None, lady=False,
           front=None, backa=None, head=0.0, hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, ph=0.0, rot=0.0,
           extra=None):
    """A puppet seated (cross-legged on the ground, or on a bench / cot: seat_h = BENCH_H): the body swapped for its
    seated sprite (legs hidden), the seat sprite painted over it. Returns its points (device)."""
    hy = ground - seat_h * s
    if lady:
        ang = woman_angles(key, t, front or (-0.5, -1.1), backa or (0.1, -0.6), head, hits, ph)
        hide = ()
    else:
        ang = man_angles(key, t, front or (-0.5, -1.1), backa or (0.1, -0.6), head, (0.0, 0.0), hits, ph)
        hide = (key + "_legF", key + "_legB")
    swap = {key + "_body": key + "_body_sit"}
    if head_sprite:
        swap[key + "_head"] = head_sprite
    ex = dict(extra or {})
    if seat:
        prev = ex.get(key + "_body")

        def fn(cr_, prev=prev):
            pc.paint_part(cr_, seat, alpha, blur)
            if prev:
                prev(cr_)
        ex[key + "_body"] = fn
    return puppet(cr, rig, x, hy, s, rot + bob_rot(t, ph, 0.008), flip, ang, alpha, blur, hide=hide, swap=swap,
                  rods=rods, extra=ex or None)


READ = dict(front=(-0.9, -0.8), backa=(-0.85, -0.85))            # both hands holding the palm leaf before him


def kau_sit(cr, t, x, ground, s, mood="calm", leaf=0.78, **kw):
    kw.setdefault("front", READ["front"])
    kw.setdefault("backa", READ["backa"])
    ex = {}
    if leaf:
        ex["dv_kau_armF_lo"] = held("dv_pleaf", kw["front"], leaf, 168, 0.0, kw.get("alpha", 1.0), kw.get("blur", 0.0))
    return sitter(cr, DV.KAU, "dv_kau", t, x, ground, s, seat="dv_kau_seat",
                  head_sprite="dv_kau_head" + ("" if mood == "calm" else "_" + mood), extra=ex, **kw)


def wife(cr, t, x, s, eyes="open", plate_=None, feet=G, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(),
         flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.4, y=None, legs=None):
    """The housewife (feet on `feet`); plate_ = the scale of a plate of food in her front hand."""
    ang = woman_angles("dv_wife", t, front, backa, head, hits, ph)
    hy = feet - 470 * s if y is None else y
    ex = {"dv_wife_armF_lo": held("dv_plate", front, plate_, 172, 0.0, alpha, blur)} if plate_ else None
    swap = {"dv_wife_head": "dv_wife_head" + ("" if eyes == "open" else "_" + eyes)}
    return puppet(cr, DV.WIFE, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, swap=swap, rods=rods, extra=ex)


def hus(cr, t, x, s, mood="tired", sit=0.0, feet=G, hoe=True, front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0,
        legs=(0.0, 0.0), hits=(), flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.8, y=None):
    """The husband: standing (sit 0) or sitting cross-legged (sit 1), with a quick rod-puppet drop between."""
    q = clamp(sit)
    hy_st, hy_sit = feet - 434 * s, feet - DV.SEAT_H * s
    hy = (hy_st + (hy_sit - hy_st) * ease(q)) if y is None else y
    ang = man_angles("dv_hus", t, front, backa, head, legs, hits, ph)
    swap = {"dv_hus_head": "dv_hus_head" + ("" if mood == "tired" else "_" + mood)}
    hide, ex = (), {}
    if q >= 0.5:
        swap["dv_hus_body"] = "dv_hus_body_sit"
        hide = ("dv_hus_legF", "dv_hus_legB")
        ex["dv_hus_body"] = lambda cr_: pc.paint_part(cr_, "dv_hus_seat", alpha, blur)
    if hoe:
        ex["dv_hus_armB_lo"] = held("dv_hoe", backa, 0.8, 150, -0.3, alpha, blur)
    bx = 6 * math.sin(math.pi * q) if 0 < q < 1 else 0.0
    return puppet(cr, DV.HUS, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur + bx, hide=hide, swap=swap,
                  rods=rods, extra=ex or None)


def vy(cr, t, x, s, mood="calm", kneel=False, lota=None, plate_=None, front=(-0.32, -0.55), **kw):
    """The butcher (feet on `feet`), standing or kneeling; lota = the tilt of the brass water pot in his front hand,
    plate_ = the scale of a plate of food."""
    sw = {"dv_vy_head": "dv_vy_head" + ("" if mood == "calm" else "_" + mood)}
    a, b = kw.get("alpha", 1.0), kw.get("blur", 0.0)
    ex = {}
    if lota is not None:
        ex["dv_vy_armF_lo"] = held("sx_lota", front, 0.6, 176, lota, a, b)
    if plate_:
        ex["dv_vy_armF_lo"] = held("dv_plate", front, plate_, 172, 0.0, a, b)
    return fig(cr, DV.VY, "dv_vy", t, x, s, front=front, swap=sw, extra=ex or None,
               kneel="dv_vy_kneel" if kneel else None, **kw)


def bfa(cr, t, x, ground, s, mood="smile", **kw):
    return sitter(cr, DV.BFA, "dv_bfa", t, x, ground, s, seat="dv_bfa_seat", seat_h=DV.BENCH_H,
                  head_sprite="dv_bfa_head" + ("" if mood == "smile" else "_" + mood), **kw)


def bmo(cr, t, x, ground, s, mood="smile", **kw):
    return sitter(cr, DV.BMO, "dv_bmo", t, x, ground, s, seat_h=DV.BENCH_H, lady=True,
                  head_sprite="dv_bmo_head" + ("" if mood == "smile" else "_" + mood), **kw)


def kfa(cr, t, x, ground, s, smile=False, **kw):
    return sitter(cr, DV.KFA, "dv_kfa", t, x, ground, s, seat="dv_kfa_seat", seat_h=DV.BENCH_H,
                  head_sprite="dv_kfa_head" + ("_smile" if smile else ""), **kw)


def kmo(cr, t, x, ground, s, smile=False, **kw):
    return sitter(cr, DV.KMO, "dv_kmo", t, x, ground, s, seat_h=DV.BENCH_H, lady=True,
                  head_sprite="dv_kmo_head" + ("_smile" if smile else ""), **kw)


def point_to(x, hy, s, target, flip=False, bulk=1.0):
    """front=(upper, fore) for a straight front arm pointing from the shoulder at target."""
    sg = -1 if flip else 1
    sx, sy = x + sg * 26 * bulk * s, hy - 262 * s
    a = math.atan2(target[1] - sy, (target[0] - sx) * sg)
    return (a - math.pi / 2, 0.0)


# ------------------------------------------------------------------ the crane


CS = 0.42                            # the crane's scale on the tree


def crane(cr, t, x, y, s, mode="stand", flip=False, rot=0.0, flap=0.0, wing=0.0, eye="open", alpha=1.0, blur=0.0,
          ph=0.0):
    """mode stand: perched, feet at (x, y); fly / fall: its body centre at (x, y), wings spread (flap = how much they
    beat, wing = their resting lift); lie: lying still on the ground at y."""
    if alpha <= 0.01:
        return
    if mode == "stand":
        prop(cr, "dv_crane" if eye == "open" else "dv_crane_shut", x, y, s, rot + sway(t, 0.012, 0.45, ph), alpha, blur,
             flip)
        return
    if mode == "lie":
        prop(cr, "dv_crane_lie", x, y, s, rot, alpha, blur, flip)
        return
    sg = -1 if flip else 1
    w = wing + flap * 0.5 * math.sin(t * 10 + ph)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(sg * s, s)
    cr.translate(-DV.CR_C[0], -DV.CR_C[1])
    sx, sy = DV.CR_SHOULDER
    cr.save()
    cr.translate(sx - 20, sy + 6)
    cr.rotate(w + 0.25)
    pc.paint_part(cr, "dv_crane_wing", alpha * 0.85, blur + 1.0)
    cr.restore()
    pc.paint_part(cr, "dv_crane_flyo" if eye == "open" else "dv_crane_fly", alpha, blur)
    cr.save()
    cr.translate(sx, sy)
    cr.rotate(w)
    pc.paint_part(cr, "dv_crane_wing", alpha, blur)
    cr.restore()
    cr.restore()


def fall_at(t, t0, t1, p0, p1, s, flip=False):
    """Where the softly falling crane is: (x, y, rot, landed); p0 = its body centre at t0, p1 = (x, ground) where it
    lies from t1."""
    if t >= t1:
        return p1[0], p1[1], 0.0, True
    u = clamp((t - t0) / max(0.3, t1 - t0))
    e = u * u * (3 - 2 * u)
    gy = p1[1] - 80 * s
    x = p0[0] + (p1[0] - p0[0]) * e + 46 * math.sin(u * math.pi * 2.2) * (1 - u)
    y = p0[1] + (gy - p0[1]) * e
    rot = (0.15 + 0.55 * math.sin(math.pi * e) + 0.12 * math.sin(u * 9) * (1 - u)) * (-1 if flip else 1)
    return x, y, rot, False


def crane_fall(cr, t, t0, t1, p0, p1, s, flip=False, alpha=1.0):
    x, y, rot, landed = fall_at(t, t0, t1, p0, p1, s, flip)
    if landed:
        crane(cr, t, x, y, s, "lie", flip, alpha=alpha)
    else:
        crane(cr, t, x, y, s, "fall", flip, rot, flap=0.3, wing=0.1, eye="shut", alpha=alpha)
    return x, y, landed


def feathers(cr, t, t0, t1, p0, p1, s, n=3, dur=3.2, alpha=1.0, flip=False):
    """White feathers that leave the falling crane one after another and drift down, swaying."""
    for i in range(n):
        ti = t0 + (t1 - t0) * (0.15 + 0.3 * i)
        u = (t - ti) / dur
        if not 0 < u < 1:
            continue
        x0, y0, _, _ = fall_at(ti, t0, t1, p0, p1, s, flip)
        xx = x0 + 70 * math.sin(u * 5 + i * 2.1) + 40 * (i - 1) * u
        yy = y0 + 520 * u
        a = alpha * min(1.0, 5 * u, 4 * (1 - u))
        prop(cr, "dv_feather", xx, yy, 0.75, rot=0.5 + 0.6 * math.sin(u * 5 + i * 1.7), alpha=a)


def glare(cr, p0, p1, a, reach=1.0):
    """A line of light from the sage's eye toward p1 (reach < 1 stops short: the anger that fizzles)."""
    if a <= 0.01:
        return
    ex, ey = p0[0] + (p1[0] - p0[0]) * reach, p0[1] + (p1[1] - p0[1]) * reach
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, col, k in ((24, (0.90, 0.22, 0.06), 0.35), (11, (1.0, 0.50, 0.10), 0.85)):   # shows on the bright cloth
        cr.move_to(*p0)
        cr.line_to(ex, ey)
        cr.set_source_rgba(*col, k * clamp(a))
        cr.set_line_width(lw)
        cr.stroke()
    cr.set_operator(cairo.OPERATOR_ADD)
    for lw, col, k in ((44, (1.0, 0.45, 0.15), 0.18), (4, (1.0, 0.95, 0.80), 0.95)):
        cr.move_to(*p0)
        cr.line_to(ex, ey)
        cr.set_source_rgba(*col, k * clamp(a))
        cr.set_line_width(lw)
        cr.stroke()
    cr.restore()
    glow(cr, p0[0], p0[1], 140, 0.55 * a)
    sparkle(cr, p0[0], p0[1], 46 * a, a, (1.0, 0.72, 0.4))
    if reach >= 1:
        sparkle(cr, ex, ey, 60 * a, a)


def eye_of(cr, pts, flip=False, k=0.13):
    """A puppet's eye (scene coordinates): a little in front of its 'head' point, along the face."""
    hx, hy = to_user(cr, pts["head"])
    tx, ty = to_user(cr, pts["top"])
    L = math.hypot(hx - tx, hy - ty) or 1.0
    ux, uy = (hx - tx) / L, (hy - ty) / L
    fx, fy = (uy, -ux) if not flip else (-uy, ux)
    return hx + fx * k * L - ux * 0.04 * L, hy + fy * k * L - uy * 0.04 * L


def tears(cr, t, t0, eye, n=6, period=0.6, alpha=1.0):
    for i in range(n):
        u = (t - t0 - period * i) / 0.9
        if 0 < u < 1:
            prop(cr, "rr_tear", eye[0] + 18 + 6 * (i % 2), eye[1] + 30 + 220 * u * u, 0.8, alpha=alpha * (1 - u * u))


def script_strip(cr, t, t_in, text, x, y, size):
    """The butcher's words in the viewer's own script on a parchment strip (left out without the Nirmala font)."""
    if not HAS_INDIC or t < t_in:
        return
    q = prog(t, t_in, 0.3)
    su = indic_surface(text, size, INK)
    w_, h_ = su.get_width(), su.get_height()
    yy = y + 16 * (1 - q)
    cr.save()
    pc.poly(cr, [(x - w_ / 2 - 28, yy - h_ / 2 - 14), (x + w_ / 2 + 28, yy - h_ / 2 - 14), (x + w_ / 2 + 40, yy),
                 (x + w_ / 2 + 28, yy + h_ / 2 + 14), (x - w_ / 2 - 28, yy + h_ / 2 + 14), (x - w_ / 2 - 40, yy)])
    cr.set_source_rgba(0.97, 0.87, 0.62, 0.96 * q)
    cr.fill_preserve()
    cr.set_source_rgba(*pc.INK, q)
    cr.set_line_width(3.5)
    cr.stroke()
    cr.set_source_surface(su, x - w_ / 2, yy - h_ / 2)
    cr.paint_with_alpha(q)
    cr.restore()


def ground(cr, y=G, alpha=1.0):
    prop(cr, "ground", W / 2, y + 6, 0.82, alpha=alpha)


# ------------------------------------------------------------------ the sets


TX, TS = 850, 0.78                   # the tree: x, scale (ground G)
BR_FOOT = (-560.0, -878.0)           # where the crane stands on its branch (tree units)
KX, KS = 380, 0.78                   # Kaushika seated under it: x, scale


def tree_set(cr, t, alpha=1.0, blur=0.0, x=TX, s=TS, ground_=True):
    r = sway(t, 0.004, 0.3)
    prop(cr, "dv_tree", x, G + 8, s, rot=r, alpha=alpha, blur=blur)
    if ground_:
        ground(cr, alpha=alpha)
    bx, by = BR_FOOT
    return (x + s * (bx * math.cos(r) - by * math.sin(r)), G + 8 + s * (bx * math.sin(r) + by * math.cos(r)))


def bundle(cr, x=KX - 210, alpha=1.0, y=G):
    prop(cr, "dv_bundle", x, y + 2, 0.55, alpha=alpha)


HX, HS = 760, 0.8                    # the house: x, scale (ground G); the sage stands outside it, on the left


def house_set(cr, x=HX, s=HS, alpha=1.0, blur=0.0, pot=True):
    prop(cr, "dv_house", x, G + 6, s, alpha=alpha, blur=blur)
    ground(cr, alpha=alpha)
    if pot:
        prop(cr, "md_kalasha", x - 360 * s, G + 4, 0.36 * s / 0.95, alpha=alpha)
    return x + DV.DOOR_X * s, G - 40 * s                                         # the doorway: x, its floor


RG = FEET + 150                      # the floor of the butcher's home
BENCH = (705, 0.62)                  # the bench: x, scale
PAR = (590, 820, 0.62)               # his father's and mother's x, scale (facing left)


def room(cr, x, g, s, alpha=1.0, blur=0.0, fade=280.0):
    """The room's back wall, its top fading into the cloth (no hard edge)."""
    cr.push_group()
    prop(cr, "dv_room", x, g + 6, s, alpha=alpha, blur=blur)
    pat = cr.pop_group()
    top = g - 1100 * s
    gr = cairo.LinearGradient(0, top, 0, top + fade)
    gr.add_color_stop_rgba(0, 0, 0, 0, 0.0)
    gr.add_color_stop_rgba(1, 0, 0, 0, 1.0)
    cr.save()
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    cr.set_source(pat)
    cr.mask(gr)
    cr.restore()


def home_set(cr, t, alpha=1.0, blur=0.0, parents=True, fa_mood="smile", mo_mood="smile", hits=(), lit=0.0,
             fa_front=None, fa_backa=None, par=PAR, bench=BENCH):
    room(cr, 540, RG, 0.9, alpha=0.85 * alpha, blur=3.0 + blur)
    ground(cr, RG, alpha)
    out = {}
    if parents:
        fx, mx, ps = par
        if lit > 0:
            glow(cr, (fx + mx) / 2, RG - 380, 420, 0.5 * lit)
            warm(cr, (fx + mx) / 2, RG - 380, 360, 0.5 * lit)
        prop(cr, "dv_bench", bench[0], RG + 4, bench[1], alpha=alpha, blur=blur)
        out["fa"] = bfa(cr, t, fx, RG, ps, mood=fa_mood, flip=True, alpha=alpha, blur=blur, hits=hits, ph=0.3,
                        front=fa_front, backa=fa_backa)
        out["mo"] = bmo(cr, t, mx, RG, ps * 0.97, mood=mo_mood, flip=True, alpha=alpha, blur=blur, hits=hits, ph=1.3)
    return out


HUT = (990, 0.7)                     # Kaushika's parents' hut: x, scale (ground G), set back
COT = (630, 0.66)                    # their rope cot: x, scale
KP = (520, 750, 0.66)                # his father's and mother's x, scale (facing left)


def hut_set(cr, t, fa_smile=False, mo_smile=False, alpha=1.0, fa_front=None, fa_backa=None, mo_front=None,
            hits=(), sky=None, sky_t=0.0):
    """Kaushika's parents alone on their rope cot by the hut. sky: "night" (a pale moon and stars: alone) or
    "dawn" (the sun rising behind the hut from sky_t: he has come home)."""
    if sky == "night":
        stars(cr, t, 0.8, ((160, 760), (330, 900), (620, 700), (950, 820), (480, 1010), (820, 1080)))
        glow(cr, 800, 900, 200, 0.35)
        prop(cr, "moon", 800, 900, 0.8, rot=-0.3)
    elif sky == "dawn":
        u = prog(t, sky_t, 2.5)
        glow(cr, 860, 1150 - 120 * u, 420, 0.55)
        prop(cr, "sun", 860, 1150 - 120 * u, 0.55, rot=t * 0.15)
    prop(cr, "tree", 1060, G + 10, 0.5, rot=sway(t, 0.005, 0.3), alpha=0.5 * alpha, blur=9)
    prop(cr, "lr_hut", HUT[0], G + 8, HUT[1], alpha=0.85 * alpha, blur=2.5)
    ground(cr, alpha=alpha)
    prop(cr, "dv_charpai", COT[0], G + 4, COT[1], alpha=alpha)
    fx, mx, ps = KP
    fa = kfa(cr, t, fx, G, ps, smile=fa_smile, flip=True, alpha=alpha, ph=0.2, front=fa_front, backa=fa_backa,
             hits=hits)
    mo = kmo(cr, t, mx, G, ps * 0.97, smile=mo_smile, flip=True, alpha=alpha, ph=1.1,
             front=mo_front or (-0.6, -1.3), backa=(-0.3, -1.2), hits=hits)
    return fa, mo


def kau_bow(cr, t, x, s, bow=0.0, mood="humble", front=ANJALI["front"], backa=ANJALI["backa"], head=0.0, hits=(),
            alpha=1.0, blur=0.0, ph=1.0, feet=G):
    """Kaushika kneeling, his upper body bowing forward from the hip (bow = radians); the legs stay on the ground."""
    hy = feet - 250 * s
    prop(cr, "dv_kau_kneel", x, hy, s, 0.0, alpha, blur)
    ang = man_angles("dv_kau", t, front, backa, head, (0.0, 0.0), hits, ph)
    sw = {"dv_kau_head": "dv_kau_head" + ("" if mood == "calm" else "_" + mood)}
    return puppet(cr, DV.KAU, x, hy, s, bow + bob_rot(t, ph, 0.006), False, ang, alpha, blur,
                  hide=("dv_kau_legF", "dv_kau_legB"), swap=sw)


# ------------------------------------------------------------------ d1  hook


HK = (320, 0.98, 1890)               # Kaushika in the hook: x, scale, feet
CR1 = ((790, 790), (720, 1884), 0.52)   # the crane: body centre when the reel starts, where it lies, scale


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "d1")
    tG, tD, tB, tM = c["G"], c["D"], c["B"], c["M"]
    x, s, feet = HK
    p0, p1, cs = CR1
    t_land = max(tD, 1.4)
    t_fall0 = -0.5
    glow(cr, x + 40, feet - 700 * s, 560, 0.42)
    cx, cy, _, landed = fall_at(t, t_fall0, t_land, p0, p1, cs)
    glow(cr, cx, cy - 40, 300, 0.45 * (1 - prog(t, t_land, 0.6)))
    feathers(cr, t, t_fall0, t_land, p0, p1, cs, n=3, dur=3.0)
    crane_fall(cr, t, t_fall0, t_land, p0, p1, cs)
    up = -0.22 + 0.12 * prog(t, t_land, 0.5)
    shock = keyed(t, [(0.0, 0.0), (tB, 1.0)], 0.3, 1.3)
    pts = kau(cr, t, x, s, mood="shock" if t > tB + 0.05 else "angry", feet=feet, head=up * (1 - shock),
              front=mix((-0.22, -0.35), (-1.75, -1.75), shock), backa=mix((0.12, -0.25), (-1.2, -1.6), shock),
              hits=[(tG, 0.35), (tB, 0.45)], ph=1.0)
    eye = eye_of(cr, pts)
    beam = 0.8 * (1 - prog(t, 0.8, 0.5)) + 0.95 * math.exp(-3.0 * max(0.0, t - tG)) * (t > tG) * (t < t_land)
    if not landed:
        glare(cr, eye, (cx - 40, cy - 10), beam)

    def ui(cr):
        head2(cr, t, "A SAGE'S ONE ANGRY LOOK", -1.0, "KILLED A BIRD", 0.3, big_size=220, ghost=-1.0, under=tD)
        card2(cr, t, tB - 0.2, 570, 690, 0.8, [("...THEN A BUTCHER", 72, INK, -44, tB),
                                              ("TAUGHT HIM DHARMA", 78, RED, 46, tM)])
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.2) + flash_at(t, tG, 0.3) + flash_at(t, tD, 0.15))


# ------------------------------------------------------------------ d2  it's in the Mahabharata


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "d2")
    tX, tM, tP = c["X"], c["M"], c["P"]
    leaves = [(None, [("MAHABHARATA", 92, HEAD_FONT)], 0),
              (tP + 0.1, [([("BOOK 3:", INK), ("VANA PARVA", RED)], 76, HEAD_FONT)], 0),
              (tP + 0.5, [("SECTIONS 205-214", 44, MONO_FONT)], 0)]
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


# ------------------------------------------------------------------ d3  the sage under the tree


def s_tree(cr, t, tl, t0, t1):
    c = cues(tl, "d3")
    tK, tT, tV = c["K"], c["T"], c["V"]
    b, k, a = depth(t, tT - 0.45, 0.6)
    glow(cr, 560, 1300, 600, 0.35)
    if t > tT - 0.45:
        r = sway(t, 0.004, 0.3)
        prop(cr, "dv_tree", TX, G + 8, TS * k, rot=r, alpha=a, blur=b)
    ground(cr)
    lit = prog(t, tK - 0.1, 0.4)
    glow(cr, KX + 60, G - 420, 400, 0.25 + 0.3 * lit)
    bundle(cr)
    pts = kau_sit(cr, t, KX, G, KS, head=0.1 - 0.12 * prog(t, tK, 0.3) + 0.12 * prog(t, tT, 0.4),
                  hits=[(tK, 0.3), (tV, 0.3)], ph=1.0)
    hand = to_user(cr, pts["handF"])
    if t > tV - 0.1:
        q = prog(t, tV - 0.1, 0.4)
        warm(cr, hand[0] + 20, hand[1], 200, 0.7 * q)
        lights(cr, t, hand[0] + 10, hand[1] - 60, 110, 8, 0.8 * q)
    dev_top = pts["top"]

    def ui(cr):
        if t < tT:
            head2(cr, t, "A SAGE NAMED", t0 + 0.05, "KAUSHIKA", tK + 0.05, big_size=240)
        else:
            head2(cr, t, "UNDER A TREE, READING THE", tT - 0.1, "VEDAS", tV, big_size=250, under=tV + 0.4)
        tag(cr, t, tK + 0.25, "SAGE KAUSHIKA", min(max(dev_top[0], 210), 870), dev_top[1] - 60, 34)
    return dict(ui=ui, flash=flash_at(t, tK, 0.15) + flash_at(t, tV, 0.2))


# ------------------------------------------------------------------ d4  the crane; splat


def s_splat(cr, t, tl, t0, t1):
    c = cues(tl, "d4")
    tC, tS = c["C"], c["S"]
    glow(cr, 560, 1300, 600, 0.35)
    bx, by = tree_set(cr, t)
    bundle(cr)
    t_fly0, t_land = tC - 0.4, tC + 0.35
    if t < t_land:                                       # the crane flies in from the left and lands
        u = ease(clamp((t - t_fly0) / (t_land - t_fly0)))
        fx = bx - 600 * (1 - u)
        fy = by - CS * 300 - 240 * (1 - u) - 60 * math.sin(math.pi * u)
        if t > t_fly0:
            crane(cr, t, fx, fy, CS, "fly", flap=1.0, wing=0.1, rot=-0.1 * (1 - u))
    else:
        settle = math.exp(-5 * (t - t_land)) * math.sin((t - t_land) * 14) * 0.06
        crane(cr, t, bx, by, CS, "stand", rot=settle)
    tail = (bx + CS * DV.CR_TAIL[0], by + CS * DV.CR_TAIL[1])
    hit_t = tS + 0.22
    jump = math.exp(-6 * max(0.0, t - hit_t)) * math.sin(max(0.0, t - hit_t) * 20) * (t > hit_t)
    pts = kau_sit(cr, t, KX, G, KS, mood="shock" if t > hit_t else "calm", head=0.1 - 0.08 * prog(t, hit_t, 0.2),
                  rot=0.02 * jump, hits=[(hit_t, 0.6)], ph=1.0)
    bun = to_user(cr, pts["top"])
    bun = (bun[0] - 8, bun[1] + 52)
    if tS - 0.05 < t < hit_t:                            # the drop falls...
        u = clamp((t - tS + 0.05) / (hit_t - tS + 0.05))
        prop(cr, "dv_drop", tail[0] + (bun[0] - tail[0]) * u, tail[1] + 20 + (bun[1] - tail[1] - 20) * u * u, 0.9)
    if t >= hit_t:                                       # ...splat on his bun
        q = back(clamp((t - hit_t) / 0.18), 2.0)
        prop(cr, "dv_splat", bun[0], bun[1] - 4, 0.75 * q)
        for i in range(5):
            u = clamp((t - hit_t) / 0.45)
            if u < 1:
                a = i * 2 * math.pi / 5 - 1.4
                sparkle(cr, bun[0] + 70 * u * math.cos(a), bun[1] - 10 + 50 * u * math.sin(a), 12 * (1 - u), 1 - u,
                        (1.0, 1.0, 1.0))

    def ui(cr):
        if t < tS:
            head2(cr, t, "ON THE BRANCH ABOVE: A", t0 + 0.05, "CRANE", tC, big_size=260)
        else:
            head2(cr, t, "AND THEN, ON HIS HEAD...", tS - 0.1, "SPLAT!", hit_t, big_size=260)
    return dict(ui=ui, flash=flash_at(t, hit_t, 0.2))


# ------------------------------------------------------------------ d5  one angry look


CR5_LAND = (690, G)                  # where the crane comes to lie (x, ground)


def s_glare(cr, t, tl, t0, t1):
    c = cues(tl, "d5")
    tA, tL, tD, tF = c["A"], c["L"], c["D"], c["F"]
    glow(cr, 560, 1300, 600, 0.35)
    bx, by = tree_set(cr, t)
    bundle(cr)
    t_fall0 = tL + 0.3
    if t < t_fall0:
        startle = math.exp(-6 * max(0.0, t - tL)) * (t > tL)
        crane(cr, t, bx, by, CS, "stand", rot=-0.15 * startle)
    p0 = (bx - CS * DV.CR_C[0], by + CS * DV.CR_C[1])
    if t >= t_fall0:
        glow(cr, CR5_LAND[0] + 60, CR5_LAND[1] - 50, 240, 0.5 * prog(t, tF, 0.4))
        feathers(cr, t, t_fall0, tF, p0, CR5_LAND, CS)
        crane_fall(cr, t, t_fall0, tF, p0, CR5_LAND, CS)
    look = keyed(t, [(t0, 0.0), (tA - 0.1, 1.0)], 0.3, 1.4)
    pts = kau_sit(cr, t, KX, G, KS, mood="angry" if t > tA - 0.15 else "calm", head=0.0 - 0.34 * look,
                  front=mix(READ["front"], (-0.5, -0.9), look), hits=[(tA, 0.5), (tL, 0.3)], ph=1.0)
    eye = eye_of(cr, pts)
    beam = math.exp(-2.6 * max(0.0, t - tL)) * (t > tL - 0.05) * (t < t_fall0 + 0.5)
    glare(cr, eye, (p0[0] - 10, p0[1]), beam)

    def ui(cr):
        if t < tF:
            head2(cr, t, "HE LOOKED UP IN ANGER:", t0 + 0.05, "ONE ANGRY LOOK", tL, big_size=200, under=tL + 0.3)
        else:
            head2(cr, t, "AND THE CRANE", tF - 0.15, "FELL DEAD", tF, big_size=240, big_color=INK)
    return dict(ui=ui, flash=flash_at(t, tL, 0.35) + flash_at(t, tF, 0.12))


# ------------------------------------------------------------------ d6  what have I done?


CR6 = (640, G, 0.5)                  # the crane lying: x, ground, scale
K6 = (330, 0.84)                     # Kaushika kneeling: x, scale


def s_regret(cr, t, tl, t0, t1):
    c = cues(tl, "d6")
    tS, tW = c["S"], c["W"]
    glow(cr, 540, 1350, 600, 0.38)
    prop(cr, "dv_tree", TX + 160, G + 8, TS * 0.9, rot=sway(t, 0.004, 0.3), alpha=0.38, blur=12)
    ground(cr)
    cx, cg, cs = CR6
    glow(cr, cx + 60, cg - 60, 260, 0.5)
    crane(cr, t, cx, cg, cs, "lie")
    prop(cr, "dv_feather", cx + 260, cg - 6, 0.6, rot=1.45)
    x, s = K6
    hy = G - 250 * s
    brow = local(x, hy, s, 0.0, False, 84, -452)
    to_brow = reach_arm(x, hy, s, 26 * 0.94, brow)
    reach = local(x, hy, s, 0.0, False, 340, -60)
    to_bird = reach_arm(x, hy, s, 26 * 0.94, reach)
    p1 = keyed(t, [(t0, 0.0), (tS - 0.1, 1.0)], 0.3, 1.3)
    p2 = keyed(t, [(t0, 0.0), (tW - 0.35, 1.0)], 0.35, 1.2)
    fr = mix(mix((-0.6, -0.6), to_brow, p1), to_bird, p2)
    pts = kau(cr, t, x, s, mood="sad" if t > tS - 0.2 else "shock", kneel=True, feet=G, front=fr,
              backa=(-0.2, -0.6), head=0.18 + 0.1 * p1 - 0.05 * p2, hits=[(tS, 0.4), (tW, 0.3)], ph=1.0)
    eye = eye_of(cr, pts)
    if t > tS:
        tears(cr, t, tS + 0.1, eye, n=6, period=0.55)

    def ui(cr):
        head2(cr, t, "THE SAGE FELT VERY", t0 + 0.05, "SAD", tS, big_size=260)
        cloud_text(cr, t, 600, 820, 0.84, [("IN ANGER...", 64, INK, -56, tW - 0.3),
                                           ("WHAT HAVE I DONE?", 84, RED, 42, tW)], t_in=tW - 0.5)
    return dict(ui=ui, eve=0.12, flash=flash_at(t, tW, 0.15))


# ------------------------------------------------------------------ d7  at the door: please wait


def s_door(cr, t, tl, t0, t1):
    c = cues(tl, "d7")
    tA, tWf, tP = c["A"], c["Wf"], c["P"]
    glow(cr, 540, 1350, 640, 0.35)
    dx, dfloor = house_set(cr)
    glow(cr, dx, dfloor - 280, 260, 0.45 * prog(t, tWf - 0.2, 0.4))
    b, k, a = depth(t, tWf - 0.25, 0.45)
    raise_ = keyed(t, [(t0, 0.0), (tP - 0.1, 1.0)], 0.3, 1.4)
    wp = None
    if t > tWf - 0.25:
        wp = wife(cr, t, dx, 0.5 * k, eyes="calm" if t > tP - 0.1 else "open", feet=dfloor, flip=True, alpha=a,
                  blur=b, front=mix((-0.08, -0.35), (-1.7, -0.75), raise_), head=-0.04 * raise_,
                  hits=[(tP, 0.4)])
    offer = keyed(t, [(t0, 0.0), (tA - 0.1, 1.0)], 0.3, 1.4)
    walk_at(cr, t, kau, t0 - 0.2, min(tA - 0.15, t0 + 1.4), -200, 170, 0.66, feet=G, mood="calm", bowl=0.95,
            front=mix((-0.4, -0.6), (-1.15, -0.45), offer), ph=1.0)
    dev_w = wp["top"] if wp else None

    def ui(cr):
        if t < tP:
            head2(cr, t, "HE WENT TO A HOUSE TO ASK FOR", t0 + 0.05, "FOOD", tA, big_size=260)
        else:
            head2(cr, t, "THE WOMAN OF THE HOUSE SAID:", tP - 0.2, "PLEASE WAIT", tP, big_size=220, under=tP + 0.4)
        if dev_w:
            tag(cr, t, tWf + 0.2, "THE HOUSEWIFE", min(dev_w[0], 840), dev_w[1] - 70, 30)
    return dict(ui=ui, flash=flash_at(t, tP, 0.2))


# ------------------------------------------------------------------ d8  husband first; the sage waits


WALL_X = 330                         # the house wall between outside (left) and inside (right)
HUS8 = (850, 0.6)                    # the husband: where he sits, scale
WIFE8 = (520, 0.58)                  # the housewife serving
FOOD8 = (650, G - 4)                 # where the plate is set down


def sun_arc(cr, t, cx, cy, rx, p, alpha=1.0):
    """The day as a dotted arc with hour ticks; the sun travels along it (p 0..1): time passing, like a clock."""
    if alpha <= 0.01:
        return
    ry = 0.5 * rx
    pts = [(cx - rx * math.cos(math.pi * v), cy - ry * math.sin(math.pi * v)) for v in (i / 50 for i in range(51))]
    dotted(cr, pts, 1.0, 22, 4.5, FADE, 0.8 * alpha)
    cr.save()
    cr.set_source_rgba(*INK, 0.8 * alpha)
    cr.set_line_width(4)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(7):
        v = i / 6
        a = math.pi * v
        x0, y0 = cx - rx * math.cos(a), cy - ry * math.sin(a)
        nx, ny = -math.cos(a), -math.sin(a) * 0.5 / 0.5
        cr.move_to(x0 + 10 * nx, y0 + 10 * ny)
        cr.line_to(x0 + 26 * nx, y0 + 26 * ny)
        cr.stroke()
    cr.restore()
    u = clamp(p)
    sx, sy = cx - rx * math.cos(math.pi * u), cy - ry * math.sin(math.pi * u)
    glow(cr, sx, sy, 150, 0.5 * alpha)
    prop(cr, "sun", sx, sy, 0.2, rot=t * 0.4, alpha=alpha)


def s_wait(cr, t, tl, t0, t1):
    c = cues(tl, "d8")
    tHb, tHu, tF, tE, tWt = c["Hb"], c["Hu"], c["F"], c["E"], c["Wt"]
    cr.save()                                            # inside: the room, behind the wall
    cr.rectangle(WALL_X, 0, W, H)
    cr.clip()
    prop(cr, "dv_room", 760, G + 6, 0.78, alpha=0.82, blur=3.0)
    glow(cr, 700, G - 420, 460, 0.3)
    cr.restore()
    ground(cr)
    impatient = prog(t, tWt - 0.3, 0.3)
    tap = -0.16 * abs(math.sin(t * 7.5)) * prog(t, tF, 0.3)
    shake = 0.06 * math.sin(t * 9) * impatient
    kau(cr, t, 165, 0.6, mood="angry" if t > tWt - 0.3 else "calm", bowl=0.95, feet=G, front=(-1.1, -0.5),
        legs=(tap, 0.0), head=shake, ph=1.0)
    prop(cr, "dv_wall", WALL_X, G + 6, 0.9)
    hx, hs = HUS8
    t_in, t_arr = tHb - 0.35, tHb + 0.9
    t_sit = max(t_arr + 0.1, tF - 0.45)
    sit = clamp((t - t_sit) / 0.35)
    eat = t > tE + 0.15
    cyc = 0.5 - 0.5 * math.cos((t - tE - 0.15) * 2 * math.pi / 0.9) if eat else 0.0
    if t < t_arr:
        walk_at(cr, t, hus, t_in, t_arr, 1220, hx, hs, feet=G, flip=True, mood="tired", head=0.12, ph=0.8)
    else:
        hus(cr, t, hx, hs, mood="smile" if eat else "tired", sit=sit, feet=G, flip=True, hoe=sit < 0.5,
            head=0.12 * (1 - sit) + 0.05 * cyc, front=mix((-0.6, -0.9), (-0.5, -2.4), cyc) if eat else (-0.32, -0.55),
            backa=(-0.3, -0.8) if sit >= 0.5 else (0.3, -0.25), hits=[(t_sit + 0.3, 0.4)])
    if sit >= 0.5:
        prop(cr, "dv_hoe", hx + 150, G + 4, 0.48, rot=1.45)
    wx, ws = WIFE8
    serve = keyed(t, [(t0, 0.0), (tF - 0.25, 1.0)], 0.3, 1.2)
    set_down = clamp((t - tF - 0.2) / 0.45)
    done = keyed(t, [(t0, 0.0), (tF + 0.7, 1.0)], 0.35, 1.2)
    wp = wife(cr, t, wx, ws, eyes="smile" if t > tF else "open", feet=G, plate_=0.82 if set_down <= 0 else None,
              front=mix(mix((-0.7, -0.9), (-1.35, -0.35), serve), (-0.45, -1.3), done),
              rot=0.1 * serve * (1 - done), ph=0.4)
    if set_down > 0:
        hp = to_user(cr, wp["handF"])
        e = ease(set_down)
        px, py = hp[0] + (FOOD8[0] - hp[0]) * e, hp[1] + 12 + (FOOD8[1] - hp[1] - 12) * e
        prop(cr, "dv_plate", px, py, 0.82 * ws)
    sun_arc(cr, t, 720, 760, 230, 0.12 + 0.76 * clamp((t - tF + 0.2) / max(0.8, t1 - tF)), prog(t, tF - 0.3, 0.3))

    def ui(cr):
        if t < tF:
            head2(cr, t, "THEN HER HUSBAND CAME HOME", t0 + 0.05, "HUNGRY", tHu, big_size=260)
        elif t < tWt:
            head2(cr, t, "SHE FED HER", tF - 0.15, "HUSBAND FIRST", tF + 0.05, big_size=210, under=tE)
        else:
            head2(cr, t, "AND THE SAGE?", tWt - 0.2, "KEPT WAITING", tWt, big_size=220)
        tag(cr, t, tWt + 0.1, "STILL WAITING...", 240, 1110, 26)
    return dict(ui=ui, eve=0.1 * prog(t, tWt, 1.0), flash=flash_at(t, tF, 0.15))


# ------------------------------------------------------------------ d9  "I am not a crane!"


def s_notcrane(cr, t, tl, t0, t1):
    c = cues(tl, "d9")
    tA, tS, tC, tL = c["A"], c["S"], c["C"], c["L"]
    glow(cr, 540, 1350, 640, 0.35)
    dx, dfloor = house_set(cr)
    glow(cr, dx, dfloor - 260, 260, 0.45)
    speaking = tS - 0.05 < t < t1 - 0.2 and math.sin((t - tS) * 2 * math.pi * 2.4) > 0
    wp = wife(cr, t, dx, 0.5, eyes="speak" if speaking else "calm", feet=dfloor, flip=True,
              front=mix((-0.08, -0.35), (-0.9, -1.2), prog(t, tC, 0.3)), hits=[(tS, 0.3), (tC, 0.3)])
    ang = t > tA - 0.15
    pts = kau(cr, t, 175, 0.66, mood="shock" if t > tC + 0.1 else ("angry" if ang else "calm"), feet=G,
              bowl=0.95, front=(-0.6, -0.6), head=-0.06 * prog(t, tA, 0.3) + 0.08 * prog(t, tC, 0.3),
              hits=[(tA, 0.5), (tC, 0.4)], ph=1.0)
    eye = eye_of(cr, pts)
    tgt = to_user(cr, wp["head"])
    if tA < t < tA + 1.2:                               # his angry look: it fizzles out half-way
        u = (t - tA) / 1.2
        glare(cr, eye, tgt, 0.8 * (1 - u), reach=0.25 + 0.35 * ease(u / 0.5) * (1 - 0.4 * u))

    def ui(cr):
        if t < tS:
            head2(cr, t, "THE SAGE GOT", t0 + 0.05, "ANGRY", tA, big_size=260)
        else:
            head2(cr, t, "SHE SAID CALMLY:", tS - 0.2, None, 0.0)
        cloud_text(cr, t, 520, 650, 0.86, [("I AM NOT A", 88, INK, -92, tS + 0.05),
                                           ("CRANE!", 150, RED, 6, tC),
                                           ("...TO DIE FROM YOUR LOOK", 44, INK, 104, tL)], flip=True, t_in=tS - 0.15)
    return dict(ui=ui, flash=flash_at(t, tC, 0.3))


# ------------------------------------------------------------------ d10  how did she know?


THINK10 = (690, 830, 0.62)


def s_know(cr, t, tl, t0, t1):
    c = cues(tl, "d10")
    tSh, tJ, tK = c["Sh"], c["J"], c["K"]
    glow(cr, 330, 1300, 560, 0.4)
    jolt = math.exp(-5 * max(0.0, t - tSh)) * math.sin(max(0.0, t - tSh) * 26) * (t > tSh)
    up = keyed(t, [(t0, 0.0), (tSh, 1.0)], 0.25, 1.4)
    pts = kau(cr, t, 300, 0.95, mood="shock", feet=1890, head=-0.04, front=mix((-0.4, -0.6), (-1.75, -1.75), up),
              backa=mix((0.25, -0.4), (-1.2, -1.6), up), rot=0.02 * jolt,
              hits=[(tSh, 0.5)], ph=1.0)
    head = to_user(cr, pts["head"])
    if t > tSh:                                          # shock lines round his head
        q = prog(t, tSh, 0.25) * (1 - 0.5 * prog(t, tSh + 1.2, 0.5))
        cr.save()
        cr.set_source_rgba(*INK, 0.8 * q)
        cr.set_line_width(7)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        for a in (-2.5, -2.0, -1.5, -1.0):
            r0, r1 = 170, 170 + 60 * q
            cr.move_to(head[0] + r0 * math.cos(a), head[1] - 40 + r0 * math.sin(a))
            cr.line_to(head[0] + r1 * math.cos(a), head[1] - 40 + r1 * math.sin(a))
            cr.stroke()
        cr.restore()
    bx, by, bs = THINK10
    q = back(clamp((t - tJ + 0.2) / 0.35), 1.5)
    if q > 0.01:
        prop(cr, "ar_think", bx, by, bs * (0.6 + 0.4 * q), rot=sway(t, 0.008, 0.5), alpha=clamp(q), flip=True)
        cr.save()                                        # inside it: the crane lying under the tree
        cr.new_path()
        pc.ell(cr, bx - 10, by - 30, 200 * q, 130 * q)
        cr.clip()
        mg = by + 70
        cr.set_source_rgba(0.45, 0.30, 0.14, 0.5 * clamp(q))
        cr.rectangle(bx - 260, mg, 520, 8)
        cr.fill()
        prop(cr, "dv_tree", bx + 110, mg + 4, 0.15, alpha=clamp(q))
        glow(cr, bx - 40, mg - 30, 120, 0.4 * clamp(q))
        crane(cr, t, bx - 80, mg + 2, 0.22, "lie", alpha=clamp(q))
        cr.restore()

    def ui(cr):
        if t < tK:
            head2(cr, t, "THE SAGE WAS", t0 + 0.05, "SHOCKED", tSh, big_size=260)
        else:
            head2(cr, t, "HOW DID SHE", tK - 0.2, "KNOW?", tK, big_size=280)
        if t > tK:
            big_q(cr, t, tK + 0.1, 900, 1230, 280)
    return dict(ui=ui, flash=flash_at(t, tSh, 0.2) + flash_at(t, tK, 0.2))


# ------------------------------------------------------------------ d11  go to Mithila


CITY11 = (820, 1070, 0.3)            # Mithila far away: x, ground, scale


def s_go(cr, t, tl, t0, t1):
    c = cues(tl, "d11")
    tD, tM, tB, tT = c["D"], c["M"], c["B"], c["T"]
    glow(cr, 540, 1350, 620, 0.35)
    cx, cg, cs = CITY11
    city_a = prog(t, tM - 0.2, 0.5)
    if city_a > 0:
        glow(cr, cx, cg - 120, 320, 0.5 * city_a)
        prop(cr, "dv_city", cx, cg, cs, alpha=city_a, blur=1.5)
    road = [(470 + (cx - 470) * u + 160 * math.sin(math.pi * u) * (1 - u) * 2, G - 30 - (G - 30 - cg - 8) * u)
            for u in (i / 60 for i in range(61))]
    dotted(cr, road, prog(t, tM, 0.9), 30, 7.5, RED, 0.95)
    if t > tB - 0.2:
        b, k, a = depth(t, tB - 0.2, 0.4)
        vy(cr, t, cx, 0.17 * k, mood="smile", feet=cg + 2, alpha=a, blur=b * 0.3, rods=False, flip=True)
    ground(cr)
    point = keyed(t, [(t0, 0.0), (tM - 0.15, 1.0)], 0.3, 1.4)
    wx, ws = 390, 0.62
    hy = G - 470 * ws
    aim = point_to(wx, hy, ws, (cx, cg - 160), bulk=0.85)
    wife(cr, t, wx, ws, eyes="speak" if (t < tM and math.sin(t * 15) > 0) else "calm", feet=G,
         front=mix((-0.5, -1.0), aim, point), hits=[(tM, 0.4), (tB, 0.3)])
    kau(cr, t, 140, 0.6, mood="shock" if t < tM else "calm", feet=G, bowl=0.95, front=(-0.6, -0.6),
        head=-0.12 * point, ph=1.0)

    def ui(cr):
        if t < tM:
            head2(cr, t, "SHE SAID: YOU DON'T KNOW", t0 + 0.05, "DHARMA", tD, big_size=260)
        elif t < tB:
            head2(cr, t, "GO TO", tM - 0.15, "MITHILA...", tM, big_size=260)
        else:
            head2(cr, t, "...A BUTCHER WILL", tB - 0.15, "TEACH YOU", tT, big_size=240, under=tT + 0.3)
        tag(cr, t, tM + 0.4, "MITHILA", cx, cg - 260, 34)
        tag(cr, t, tB + 0.2, "A BUTCHER", cx + 10, cg + 110, 28)
    return dict(ui=ui, flash=flash_at(t, tM, 0.2))


# ------------------------------------------------------------------ d12  the Mithila market


STALL = (700, 0.7)                   # the stall: x, scale (floor RG)


def s_market(cr, t, tl, t0, t1):
    c = cues(tl, "d12")
    tM, tB, tL, tQ = c["M"], c["B"], c["L"], c["Q"]
    prop(cr, "dv_city", 520, RG - 330, 0.7, alpha=0.45, blur=10)
    prop(cr, "dv_basket", 110, RG - 210, 0.45, alpha=0.6, blur=6)
    glow(cr, 560, 1350, 640, 0.35)
    ground(cr, RG)
    sx, ss = STALL
    lit = prog(t, tB - 0.2, 0.4)
    glow(cr, sx, RG - 560, 420, 0.25 + 0.3 * lit)
    prop(cr, "dv_stall_back", sx, RG + 6, ss)
    up = keyed(t, [(t0, 0.0), (tL - 0.1, 1.0)], 0.3, 1.4)
    wave = keyed(t, [(t0, 0.0), (tQ - 0.25, 1.0)], 0.3, 1.4)
    work = 0.08 * math.sin(t * 6) * (1 - up)
    cr.save()                                            # he stands behind his counter: only above it shows
    cr.rectangle(-200, -200, W + 400, RG + 6 - 400 * ss + 200)
    cr.clip()
    vp = vy(cr, t, sx + 10, 0.66, mood="speak" if (t > tQ - 0.2 and math.sin(t * 15) > 0) else
            ("smile" if t > tL - 0.1 else "calm"), feet=RG, flip=True,
            front=mix((-1.0 + work, -0.7), (-1.9, -0.6), wave), backa=(-0.6, -0.9),
            head=0.22 * (1 - up) - 0.04 * up, hits=[(tL, 0.4), (tQ, 0.3)], ph=0.5)
    cr.restore()
    prop(cr, "dv_counter", sx, RG + 6, ss)
    prop(cr, "dv_basket", 1010, RG + 4, 0.42)
    shock = t > tQ + 0.15
    walk_at(cr, t, kau, t0 - 0.1, min(tB + 0.3, t0 + 1.6), -170, 220, 0.66, feet=RG,
            mood="shock" if shock else "calm", bowl=0.95, front=(-0.6, -0.6), head=-0.06 * shock,
            hits=[(tQ + 0.15, 0.6)], ph=1.0)
    dev_v = vp["top"]

    def ui(cr):
        if t < tL:
            head2(cr, t, "IN MITHILA'S MARKET: A", t0 + 0.05, "BUTCHER", tB, big_size=250)
        else:
            head2(cr, t, "HE SAW THE SAGE AND SMILED:", tL - 0.1, None, 0.0)
        tag(cr, t, tB + 0.2, "THE BUTCHER", min(dev_v[0], 880), dev_v[1] - 70, 30, t_out=tQ - 0.4)
        cloud_text(cr, t, 480, 800, 0.88, [("SHE SENT YOU,", 100, INK, -50, tQ - 0.15),
                                           ("RIGHT?", 140, RED, 64, tQ + 0.2)], flip=True, t_in=tQ - 0.35)
    return dict(ui=ui, flash=flash_at(t, tQ, 0.2))


# ------------------------------------------------------------------ d13  his home; his old parents


def s_home(cr, t, tl, t0, t1):
    c = cues(tl, "d13")
    tH, tO, tP = c["H"], c["O"], c["P"]
    lit = prog(t, tO - 0.1, 0.5)
    par = home_set(cr, t, fa_mood="smile" if t > tO else "calm", mo_mood="smile" if t > tO else "open",
                   hits=[(tO, 0.3)], lit=lit)
    if t > tP:
        lights(cr, t, (PAR[0] + PAR[1]) / 2, RG - 500, 260, 10, 0.6 * prog(t, tP, 0.5))
    fold = keyed(t, [(t0, 0.0), (tO, 1.0)], 0.35, 1.2)
    walk_at(cr, t, vy, t0 - 0.2, t0 + 1.3, -150, 340, 0.66, feet=RG, mood="smile",
            front=mix((-0.32, -0.55), ANJALI["front"], fold), backa=mix((0.3, -0.25), ANJALI["backa"], fold), ph=0.5)
    walk_at(cr, t, kau, t0 + 0.1, t0 + 1.6, -330, 120, 0.6, feet=RG, mood="calm", bowl=0.95, front=(-0.6, -0.6),
            ph=1.0)
    dev_f, dev_m = par["fa"]["top"], par["mo"]["top"]

    def ui(cr):
        if t < tO:
            head2(cr, t, "HE TOOK THE SAGE", t0 + 0.05, "HOME", tH, big_size=260)
        else:
            head2(cr, t, "THERE SAT HIS OLD", tO - 0.15, "PARENTS", tP, big_size=260, under=tP + 0.35)
        ty = min(dev_f[1], dev_m[1]) - 70
        tag(cr, t, tP + 0.05, "HIS FATHER", dev_f[0] - 30, ty, 28)
        tag(cr, t, tP + 0.3, "HIS MOTHER", min(dev_m[0] + 20, 900), ty - 66, 28)
    return dict(ui=ui, flash=flash_at(t, tO, 0.2))


# ------------------------------------------------------------------ d14  my parents = my gods


ROWS14 = ("I BATHE THEM", "I WASH THEIR FEET", "I FEED THEM")


def chores(cr, t, t_in, x, y, s, row_t):
    """A torn note with the three things he does, each ticked as he says it."""
    p = back(clamp((t - t_in) / 0.35), 1.4)
    a = clamp(p)
    if a <= 0.01:
        return
    yy = y + 60 * (1 - p)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(-0.02 + sway(t, 0.006, 0.4))
    cr.scale(s, s)
    pc.paint_part(cr, "rv_note", a)
    for i, (txt, tr) in enumerate(zip(ROWS14, row_t)):
        q = prog(t, tr, 0.25) * a
        ry = -150 + 150 * i
        if q > 0:
            cr.set_source_rgba(*INK, 0.85 * q)
            cr.set_line_width(7)
            cr.rectangle(-330, ry - 40, 80, 80)
            cr.stroke()
            draw_text(cr, txt, -220, ry + 12 * (1 - q), 84, INK, q, anchor="lm")
            tick(cr, -322, ry - 6, 76, prog(t, tr + 0.2, 0.3))
    cr.restore()


def drops(cr, t, x0, y0, x1, y1, n=9, alpha=1.0, rate=2.4):
    """A thin stream of water drops from (x0, y0) falling to (x1, y1), blue so it shows on the bright cloth."""
    if alpha <= 0.01:
        return
    cr.save()
    for i in range(n):
        u = (t * rate + i / n) % 1.0
        x, y = x0 + (x1 - x0) * u, y0 + (y1 - y0) * u * u
        cr.new_path()
        pc.ell(cr, x, y, 5, 9)
        cr.set_source_rgba(0.30, 0.56, 0.92, 0.85 * alpha * (1 - 0.4 * u))
        cr.fill()
    cr.restore()


PAR14 = (650, 900, 0.74)             # closer: his father's and mother's x, scale
BENCH14 = (800, 0.74)
K14 = (245, 0.74)                    # the butcher kneeling at his father's feet: x, scale


def s_serve(cr, t, tl, t0, t1):
    c = cues(tl, "d14")
    tG, tBa, tF, tE = c["G"], c["Ba"], c["F"], c["E"]
    fx, mx, ps = PAR14
    hy_f = RG - DV.BENCH_H * ps
    home_set(cr, t, lit=0.5, hits=[(tF, 0.2)], par=PAR14, bench=BENCH14)
    feet_x = fx - 235 * ps
    x, s = K14
    hy = RG - 250 * s
    wash = keyed(t, [(t0, 0.0), (tF - 0.15, 1.0), (tE - 0.15, 0.0)], 0.3, 1.2)
    feed = keyed(t, [(t0, 0.0), (tE - 0.15, 1.0)], 0.3, 1.2)
    to_feet = reach_arm(x, hy, s, 26 * 1.04, (feet_x - 30, RG - 200))
    to_face = point_to(x, hy, s, (fx - 80, hy_f - 260), bulk=1.04)
    fr = mix(mix(ANJALI["front"], to_feet, wash), (to_face[0] + 0.2, -0.5), feed)
    ba = mix(ANJALI["backa"], (-0.4, -0.9), max(wash, feed))
    pts = vy(cr, t, x, s, mood="smile", kneel=True, feet=RG, front=fr, backa=ba,
             lota=0.9 if (wash > 0.5 and t < tE - 0.15) else None, plate_=0.62 if feed > 0.5 else None,
             head=0.15 * wash - 0.05 * feed, hits=[(tF, 0.3), (tE, 0.3)], ph=0.5)
    prop(cr, "dv_basin", feet_x + 10, RG + 4, 0.62, alpha=prog(t, tBa, 0.3))
    if tF < t < tE - 0.1:                                # water poured over his father's feet
        hand = to_user(cr, pts["handF"])
        drops(cr, t, hand[0] + 50, hand[1] + 10, feet_x + 20, RG - 60, n=10, alpha=prog(t, tF, 0.2))
    if tBa < t < tF + 0.2:                               # bathing: a gentle shower over his parents
        q = prog(t, tBa, 0.3) * (1 - prog(t, tF, 0.3))
        for k, px in enumerate((fx, mx)):
            for j in range(3):
                drops(cr, t + 0.37 * j + k, px - 40 + 40 * j, RG - 860, px - 30 + 40 * j, RG - 560, n=4, alpha=q,
                      rate=1.6)
    lng = lang(tl)

    def ui(cr):
        head2(cr, t, "THE BUTCHER SAID:", t0 + 0.05, "MY PARENTS = MY GODS", tG, big_size=170, under=tG + 0.5)
        script_strip(cr, t, tG + 0.35, QUOTE[lng], 540, 600, 52)
        chores(cr, t, tBa - 0.3, 560, 860, 0.66, (tBa, tF, tE))
    return dict(ui=ui, flash=flash_at(t, tG, 0.2))


# ------------------------------------------------------------------ d15  and you?


THINK15 = (330, 820, 0.52)


def s_you(cr, t, tl, t0, t1):
    c = cues(tl, "d15")
    tY, tW, tL = c["Y"], c["W"], c["L"]
    home_set(cr, t, alpha=0.75, blur=6.0)
    vx, vs = 690, 0.72
    hy = RG - 434 * vs
    kx, ks = 300, 0.72
    aim = point_to(vx, hy, vs, (kx + 40, RG - 600 * ks), flip=True, bulk=1.04)
    p = keyed(t, [(t0, 0.0), (tY - 0.1, 1.0)], 0.3, 1.4)
    vy(cr, t, vx, vs, mood="speak" if math.sin(t * 15) > 0 else "calm", feet=RG, flip=True,
       front=mix((-0.32, -0.55), aim, p), hits=[(tY, 0.4)], ph=0.5)
    bow = keyed(t, [(t0, 0.0), (tL - 0.1, 1.0)], 0.35, 1.2)
    pts = kau(cr, t, kx, ks, mood="sad" if t > tW else "shock", feet=RG, bowl=0.95, front=(-0.6, -0.6),
              head=0.3 * bow, rot=0.03 * bow, hits=[(tY, 0.4), (tL, 0.3)], ph=1.0)
    if t > tL:
        tears(cr, t, tL + 0.1, eye_of(cr, pts), n=4, period=0.6)
    bx, by, bs = THINK15
    q = back(clamp((t - tW - 0.1) / 0.35), 1.5)
    if q > 0.01:
        prop(cr, "ar_think", bx, by, bs * (0.6 + 0.4 * q), rot=sway(t, 0.008, 0.5), alpha=clamp(q))
        cr.save()                                        # inside it: his old parents alone by their hut
        cr.new_path()
        pc.ell(cr, bx - 10, by - 30, 170 * q, 110 * q)
        cr.clip()
        mg = by + 55
        prop(cr, "lr_hut", bx + 90, mg, 0.2, alpha=clamp(q))
        kfa(cr, t, bx - 60, mg, 0.18, flip=True, rods=False, alpha=clamp(q))
        kmo(cr, t, bx + 10, mg, 0.175, flip=True, rods=False, alpha=clamp(q))
        cr.restore()

    def ui(cr):
        if t < tW:
            head2(cr, t, "THE BUTCHER ASKED:", t0 + 0.05, "AND YOU?", tY, big_size=280)
        else:
            head2(cr, t, "YOU LEFT YOUR PARENTS", tW - 0.15, "WITHOUT A WORD", tW + 0.2, big_size=200)
    return dict(ui=ui, flash=flash_at(t, tY, 0.2))


# ------------------------------------------------------------------ d16  flashback: blind with grief; go, serve them


def s_blind(cr, t, tl, t0, t1):
    c = cues(tl, "d16")
    tBl, tGo, tS = c["Bl"], c["Go"], c["S"]
    sep = 1.0 - prog(t, tGo - 0.1, 0.7)
    glow(cr, 480, 1400, 640, 0.45 + 0.1 * (1 - sep))
    fa, mo = hut_set(cr, t, mo_front=(-0.5, -1.1), sky="night")
    eyes = [eye_of(cr, fa, True), eye_of(cr, mo, True, 0.2)]
    if t > tBl:
        for k, e in enumerate(eyes):
            tears(cr, t, tBl + 0.2 + 0.3 * k, e, n=5, period=0.7, alpha=0.9)
    road = [(-40 + 390 * u, G - 40 - 70 * math.sin(math.pi * u)) for u in (i / 40 for i in range(41))]
    dotted(cr, road, prog(t, tGo + 0.1, 0.8), 30, 7.5, RED, 0.95)
    if t > tGo:
        warm(cr, 520, G - 300, 420, 0.4 * prog(t, tGo, 0.6))

    def ui(cr):
        if t < tGo:
            head2(cr, t, "THEY WENT BLIND WITH", tBl - 0.2, "GRIEF", tBl + 0.1, big_size=260)
            if t < tBl - 0.2:
                head2(cr, t, "HIS OWN PARENTS, ALONE...", t0 + 0.1, None, 0.0)
            for k, e in enumerate(eyes):
                red_ring(cr, e[0] - 6, e[1] - 4, 52, 36, prog(t, tBl + 0.25 + 0.2 * k, 0.4), 7)
            plate(cr, t, t0 + 0.1, "FAR AWAY...", 200, 620, 34, t_out=tGo - 0.2)
        else:
            head2(cr, t, "GO, SERVE THEM", tGo - 0.1, "FIRST", tS, big_size=280, under=tS + 0.35)
        tag(cr, t, t0 + 0.3, "THE SAGE'S PARENTS", 630, 1180, 28, t_out=tBl)
    return dict(ui=ui, sepia=sep, flash=flash_at(t, tGo, 0.3))


# ------------------------------------------------------------------ d17  he went home


K17 = (112, 0.62)                    # Kaushika kneeling at his father's feet: x, scale
BOW17 = 1.1                          # how far he bows (radians): his head down by his father's knees


def s_return(cr, t, tl, t0, t1):
    c = cues(tl, "d17")
    tR, tS, tH = c["R"], c["S"], c["H"]
    glow(cr, 480, 1400, 660, 0.45)
    warm(cr, 480, G - 360, 520, 0.35 * prog(t, tH, 0.6))
    kx, ks = K17
    fx, mx, ps = KP
    t_kneel = tS - 0.25
    touch = keyed(t, [(t_kneel, 0.0), (tS, 1.0)], 0.3, 1.2)
    bow = BOW17 * touch
    bless = keyed(t, [(t0, 0.0), (tS + 0.3, 1.0)], 0.35, 1.2)
    hy_f = G - DV.BENCH_H * ps
    hy_k = G - 250 * ks
    head_k = local(kx, hy_k, ks, BOW17, False, 0, -500)               # his head, bowed (where the hand will rest)
    to_head = reach_arm(fx, hy_f, ps, 26 * 0.88, head_k, flip=True)
    fa, mo = hut_set(cr, t, fa_smile=t > tS + 0.1, mo_smile=t > tS + 0.3, sky="dawn", sky_t=t0,
                     fa_front=mix((-0.5, -1.1), to_head, bless),
                     mo_front=mix((-0.5, -1.1), (-1.85, -1.0), bless), hits=[(tS + 0.3, 0.3)])
    if t < t_kneel:
        walk_at(cr, t, kau, t0 - 0.2, t_kneel - 0.1, -260, kx, ks, feet=G, mood="humble",
                front=ANJALI["front"], backa=ANJALI["backa"], ph=1.0)
    else:
        sh = local(kx, hy_k, ks, bow, False, 26 * 0.94, -262)
        tgt = (fx - 230 * ps, G - 30)
        a = math.atan2(tgt[1] - sh[1], tgt[0] - sh[0]) - bow
        to_feet = (a - math.pi / 2, -0.15)
        kau_bow(cr, t, kx, ks, bow, front=mix(ANJALI["front"], to_feet, touch),
                backa=mix(ANJALI["backa"], (to_feet[0] + 0.15, -0.2), touch), head=0.1 * touch,
                hits=[(t_kneel, 0.4)])
    if t > tH:
        lights(cr, t, (fx + mx) / 2 - 60, G - 420, 300, 12, 0.7 * prog(t, tH, 0.5))

    def ui(cr):
        if t < tS:
            head2(cr, t, "AND THE SAGE REALLY", t0 + 0.05, "WENT HOME", tR, big_size=260)
        else:
            head2(cr, t, "TO SERVE HIS PARENTS,", tS - 0.1, "HE WENT HOME", tS + 0.1, big_size=230, under=tH)
    return dict(ui=ui, flash=flash_at(t, tS, 0.2) + flash_at(t, tH, 0.15))


# ------------------------------------------------------------------ d18  who is more righteous?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "d18")
    tQ, tS, tB, tC = c["Q"], c["S"], c["B"], c["C"]
    glow(cr, 290, 1450, 420, 0.3 + 0.3 * prog(t, tS, 0.3))
    glow(cr, 790, 1400, 420, 0.3 + 0.3 * prog(t, tB, 0.3))
    ground(cr, RG)
    bundle(cr, 110, y=RG)
    kau_sit(cr, t, 270, RG, 0.66, head=0.08, ph=1.0, hits=[(tS, 0.3)])
    vy(cr, t, 800, 0.6, mood="smile", feet=RG, flip=True, front=(-1.25, -0.5), plate_=0.62, ph=0.5,
       hits=[(tB, 0.3)])
    cards = ((295, "THE SAGE?", "READS THE VEDAS", tS), (785, "THE BUTCHER?", "SERVES HIS PARENTS", tB))

    def ui(cr):
        head2(cr, t, "WHO IS MORE", t0 + 0.05, "RIGHTEOUS?", tQ, big_size=230)
        for cx, txt, sub, tc in cards:
            card(cr, t, tc - 0.25, cx, 760, 0.6, [(txt, 112 if len(txt) < 11 else 100, RED, 4)])
            tag(cr, t, tc + 0.15, sub, cx, 930, 30)
        if t > tC:
            n = int((t - tC) / 0.9)
            k = n % 2
            red_ring(cr, cards[k][0], 764, 234, 98, prog(t, tC + 0.9 * n, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tC, 0.15))


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("d1", None, s_hook, {"z": (1.0, 1.04)}),
    ("d2", None, s_book, {"z": (1.0, 1.03)}),
    ("d3", None, s_tree, {"z": (1.0, 1.03)}),
    ("d4", None, s_splat, {"z": (1.0, 1.04), "focus": (420, 1300)}),
    ("d5", None, s_glare, {"z": (1.02, 1.07), "focus": (440, 1250)}),
    ("d6", None, s_regret, {"z": (1.0, 1.04)}),
    ("d7", None, s_door, {"z": (1.0, 1.03)}),
    ("d8", None, s_wait, {"z": (1.0, 1.03)}),
    ("d9", None, s_notcrane, {"z": (1.0, 1.04)}),
    ("d10", None, s_know, {"z": (1.0, 1.05), "focus": (420, 1200)}),
    ("d11", None, s_go, {"z": (1.0, 1.03)}),
    ("d12", None, s_market, {"z": (1.0, 1.03)}),
    ("d13", None, s_home, {"z": (1.0, 1.03)}),
    ("d14", None, s_serve, {"z": (1.0, 1.03)}),
    ("d15", None, s_you, {"z": (1.0, 1.04)}),
    ("d16", None, s_blind, {"z": (1.0, 1.04)}),
    ("d17", None, s_return, {"z": (1.0, 1.03)}),
    ("d18", None, s_end, {"z": (1.0, 1.03)}),
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
    hit as the crane falls, shimmer on "I am not a crane!", a bell at the butcher's parents, a conch on "go, serve
    them first", a bell on the closing question, then (only where it fits) shimmer as he touches his parents' feet.
    Chosen in THAT order of importance, each at least SFX_MIN_GAP from every sound already kept (as
    render_myth.calm_sfx keeps them), so the list returned is what plays (about 6 sounds); the bed dips before the
    reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["d5"]["F"], "hit", 0), (c["d9"]["C"], "shimmer", 0), (c["d13"]["P"], "bell", 0),
            (c["d16"]["Go"], "conch", 0), (c["d18"]["C"], "bell", 0), (c["d17"]["S"], "shimmer", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["d5"]["F"] - 0.35, "dip", 0.5), (c["d9"]["C"] - 0.3, "dip", 0.45), (c["d16"]["Go"] - 0.3, "dip", 0.5)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
