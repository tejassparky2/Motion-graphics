"""Scenes for videos/mrityu.py: "Death herself wept" (Mahabharata, Drona Parva: Narada's story to King Akampana), in
Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen, two-tier headlines
and rod-puppet motion as the earlier reels, with the cast from mrityu_cast. Built so a 5-year-old can follow it: every
line has one shot that shows exactly what is said, in the order it is said, one big short English headline per idea;
the twist (her tears become diseases) gets a slow reveal: the tears fall from Brahma's opened hands and darken, one by
one, into little clouds of sickness.

Respect: Brahma, Shiva, Mother Earth and Mrityu with dignity. Death is a gentle young woman in red, never a skull or a
monster; her tears are light. Brahma's anger is light and glow: flames rise BEHIND the round world and the little
silhouettes on it only throw up their arms, nobody burns. People dying of illness are little silhouettes lying down
as if asleep, a soft light rising from them; no harm is ever drawn.

Every frame is a pure function of t. On-screen text is short English, except the mr9 name card, where the spoken word
(मृत्यु) shows in Devanagari (shaped by matplotlib as in scenes_arjuna; without the Nirmala font it falls back to Latin
letters). Cues are words of the Hindi line with a fraction fallback, in one table (CUES) that the scenes and sfx() both
read, with minimum gaps so a fast voice can't bunch the beats together. Shot starts and cues are cached on the timeline
under this module's own names (_mr_shot_starts, _mr_cues). Kannada is routed to scenes_mrityu_yk (videos/mrityu.py).

Shot list (line: what is on the screen)
  mr1   HOOK, frame 0: Mrityu alone and large, a hand at her mouth, glowing tears running down her face, tag DEATH:
        DEATH HERSELF / CRIED; on "darti" little dark people at her feet shrink back from her, afraid; on "roi" she
        sobs (eyes squeezed shut), a surge of tears, CRIED underlined; on "kyonki" SHE DIDN'T WANT TO / TAKE ANY LIFE;
        on "maarna" she slowly shakes her head
  mr2   a palm-leaf book opens: MAHABHARATA, then A TRUE STORY (ringed): A TRUE STORY FROM THE / MAHABHARATA
  mr3   Brahma on his lotus (tag BRAHMA): LONG AGO, BRAHMA / MADE THE WORLD; the round world pops out of his light,
        sparks fly from his hand and little people and animals appear on it; a counter DEATHS: 0, its 0 ringed: AND
        BACK THEN, / NOBODY DIED
  mr4   the world, big: people (tag PEOPLE), then animals (tag ANIMALS) pop up all round it, faster and faster, a
        counter PEOPLE racing: THEY KEPT GROWING AND / GROWING; it is packed: one little man hovers over the crowd,
        ringed, NO ROOM!: ON EARTH THERE WAS / NO ROOM LEFT
  mr5   Mother Earth (tag MOTHER EARTH) bent under the crowded world on her back, trembling, Brahma small on his lotus:
        MOTHER EARTH WAS / TIRED; she reaches out to him: SHE SAID TO BRAHMA: + cloud I CAN'T CARRY / THIS ANY
        MORE!
  mr6   Brahma frowns, an orange glow round him, shaking: BRAHMA GOT SO / ANGRY; a stream of fire-light from him to
        the world: HIS ANGER BECAME / FIRE; flames of light rise behind the world, the little people throw up their
        arms, all goes orange: AND THE WORLD BEGAN TO / BURN
  mr7   Shiva walks in with his trident (tag SHIVA): THEN CAME / SHIVA; his hand up: HE SAID: / STOP!; cloud DON'T
        BURN / EVERYONE!
  mr8   the fire-light streams back from the world into Brahma, the flames sink: BRAHMA PULLED THE FIRE / BACK IN; a
        burst of light from him, and out of the light steps a girl (pale, blurred, then real): AND FROM HIS BODY CAME
        / A GIRL
  mr9   Brahma and the girl face to face; a plaque मृत्यु = DEATH: HE NAMED HER / MRITYU; he points away, out
        into the world: HE ORDERED HER: + card GO, TAKE / EVERY LIFE!
  mr10  the girl, big, a hand at her mouth, sobbing, tears pouring: HEARING THIS, SHE BURST INTO / TEARS; she holds out
        her hands: SHE ASKED: + cloud HOW CAN I / TAKE A LIFE?
  mr11  Brahma (right) holds out his cupped hands; her tears fly in a glowing stream into them: BRAHMA CAUGHT HER /
        TEARS; his palms full of light, ringed: IN HIS TWO / HANDS
  mr12  she shakes her head (no), then stands on ONE leg, hands joined over her head, eyes shut (her one foot
        ringed): TO SAY NO, SHE STOOD / ON ONE LEG; suns and moons race over her and a YEARS counter spins up to
        1,000,000,000: FOR / BILLIONS OF YEARS!
  mr13  Brahma shakes his head, a red X: BUT BRAHMA SAID / NO; his cupped palms still glowing, ringed: HER TEARS WERE
        STILL / IN HIS HANDS
  mr13q QUESTION: SO...; a big red "?" over the card WHAT HAPPENED TO / THE TEARS?, Brahma and the girl small below
  mr14  the twist, slowly: Brahma (HE SAID:) opens his hands; the glowing tears fall one by one and darken into little
        dark clouds (tag DISEASES): YOUR TEARS WILL BECOME / DISEASES; the clouds drift down onto the world, and here
        and there a little person lies down as if asleep, a soft light rising: AND PEOPLE WOULD DIE OF / DISEASES
  mr15  an hourglass runs out; a sleeping old man's soft light rises and the girl (gentle) takes its hand and leads
        it away: JUST TAKE THEM / WHEN IT'S TIME; a dark smudge tagged SIN drifts at her and breaks up on her light,
        a red X: AND IT WON'T BE / YOUR SIN
  mr16  she bows, hands joined, and nods: AT LAST, THE GIRL / AGREED; sunrise behind the world, the girl comes down
        to it in her soft red light (tag DEATH): AND DEATH CAME TO / THE WORLD
  mr16c CALLBACK: the hook's picture again (the girl large, a hand at her mouth, tears; the little afraid people at
        her feet): THE DEATH WE ALL / FEAR...; then BEFORE TAKING THE FIRST LIFE, / SHE CRIED (underlined)
  mr17  IS DEATH A PUNISHMENT, / OR A NEED?; cards PUNISHMENT? / NEED?, a red ring alternating; the girl and the
        world small below
"""
import functools
import math
import random

import cairo

import mrityu_cast as MC
import puppet_core as pc
import shikhandi_cast as SKC
import six_cast_c as C6
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, back, clamp, draw_text, ease, prog, text_size
from puppet_core import H, W, depth, keyed, prop, puppet, sway
from scenes_arjuna import HAS_INDIC, card2, cloud_text, indic_surface
from scenes_dharmavyadha import point_to
from scenes_jarasandha import FEET, INK, RED, bob_rot, glow, man_angles, motes, red_ring, woman_angles
from scenes_jayadratha import NIGHT, flash_at, tag, tint, title_lift, to_user
from scenes_kaikeyi import ANJALI, card, fig
from scenes_lakshman_rekha import big_x, book, sparkle
from scenes_mandhata import aura, burst, held, local, mix, reach_arm, warm
from scenes_ravana import head2
from scenes_ruru import flow, held_grip, plate
from shots import CUT_LEAD, MIN_SHOT, T

MISSES = set()                       # cue words not found in a line (falls back to fractions)
G = FEET + 120                       # the ground line of most sets
FIRE_C = (1.0, 0.50, 0.12)           # Brahma's anger: orange light
TEAR_GLOW = (0.45, 0.72, 1.0)
DEATH_GLOW = (1.0, 0.55, 0.45)       # her soft red light
NAME_W = "मृत्यु"
UP = dict(front=(-2.45, -0.55), backa=(-2.35, -0.65))     # both arms raised in front of her face, palms joined
PLEAD = dict(front=(-1.25, -0.55), backa=(-1.05, -0.45))  # both hands held out, open


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback (also for a language with no cue words:
    this module only has to draw Hindi)."""
    w = words.get(getattr(tl, "lang", "hi")) if isinstance(words, dict) else words
    if w is None:
        return T(tl, bid, frac)
    try:
        return T(tl, bid, w)
    except (KeyError, ValueError):
        MISSES.add((bid, w))
        return T(tl, bid, frac)


# Every cue of every line: (name, {"hi": word}, fraction fallback, ((after, min gap), ...)); "t0" = the line's start.
# Words are exact substrings of the Hindi lines (checked: MISSES stays empty). Kannada is drawn by scenes_mrityu_yk.
CUES = {
    "mr1": (("M", {"hi": "मौत"}, 0.08, (("t0", 0.4),)),
            ("D", {"hi": "डरती"}, 0.3, (("M", 0.6),)),
            ("R", {"hi": "रोई"}, 0.47, (("D", 0.8),)),
            ("K", {"hi": "क्योंकि"}, 0.62, (("R", 0.8),)),
            ("N", {"hi": "मारना"}, 0.82, (("K", 0.6),))),
    "mr2": (("M", {"hi": "महाभारत"}, 0.15, (("t0", 0.2),)),
            ("S", {"hi": "सच्ची"}, 0.5, (("M", 0.6),))),
    "mr3": (("B", {"hi": "ब्रह्मा"}, 0.18, (("t0", 0.3),)),
            ("W", {"hi": "बनाई"}, 0.45, (("B", 0.6),)),
            ("N", {"hi": "मरता"}, 0.75, (("W", 0.8),))),
    "mr4": (("P", {"hi": "इंसान"}, 0.02, ()),
            ("A", {"hi": "जानवर"}, 0.14, (("P", 0.45),)),
            ("G", {"hi": "बढ़ते"}, 0.28, (("A", 0.45),)),
            ("F", {"hi": "धरती"}, 0.55, (("G", 1.0),)),
            ("J", {"hi": "जगह"}, 0.82, (("F", 0.6),))),
    "mr5": (("E", {"hi": "माँ"}, 0.08, (("t0", 0.15),)),
            ("T", {"hi": "थक"}, 0.25, (("E", 0.6),)),
            ("S", {"hi": "बोलीं"}, 0.5, (("T", 0.8),)),
            ("U", {"hi": "उठता"}, 0.92, (("S", 1.0),))),
    "mr6": (("A", {"hi": "ग़ुस्सा"}, 0.2, (("t0", 0.4),)),
            ("F", {"hi": "आग"}, 0.48, (("A", 0.9),)),
            ("J", {"hi": "जलने"}, 0.8, (("F", 0.9),))),
    "mr7": (("S", {"hi": "शिव"}, 0.1, (("t0", 0.15),)),
            ("R", {"hi": "रुकिए"}, 0.5, (("S", 0.8),)),
            ("M", {"hi": "जलाइए"}, 0.8, (("R", 0.5),))),
    "mr8": (("W", {"hi": "वापस"}, 0.2, (("t0", 0.3),)),
            ("K", {"hi": "खींच"}, 0.35, (("W", 0.3),)),
            ("P", {"hi": "पल"}, 0.58, (("K", 0.8),)),
            ("G", {"hi": "लड़की"}, 0.85, (("P", 0.6),))),
    "mr9": (("N", {"hi": "नाम"}, 0.15, (("t0", 0.3),)),
            ("M", {"hi": "मृत्यु"}, 0.28, (("N", 0.4),)),
            ("Y", {"hi": "मौत"}, 0.42, (("M", 0.5),)),
            ("H", {"hi": "हुक्म"}, 0.6, (("Y", 0.6),)),
            ("J", {"hi": "जाओ"}, 0.75, (("H", 0.4),)),
            ("L", {"hi": "जान"}, 0.88, (("J", 0.3),))),
    "mr10": (("F", {"hi": "फूट"}, 0.35, (("t0", 0.6),)),
             ("B", {"hi": "बोली"}, 0.6, (("F", 0.9),)),
             ("K", {"hi": "कैसे"}, 0.88, (("B", 0.6),))),
    "mr11": (("A", {"hi": "आँसू"}, 0.28, (("t0", 0.4),)),
             ("H", {"hi": "हथेलियों"}, 0.7, (("A", 0.8),))),
    "mr12": (("M", {"hi": "मना"}, 0.02, ()),
             ("P", {"hi": "पैर"}, 0.4, (("M", 0.6),)),
             ("A", {"hi": "अरबों"}, 0.78, (("P", 0.9),))),
    "mr13": (("N", {"hi": "माने"}, 0.3, (("t0", 0.4),)),
             ("H", {"hi": "हथेलियों"}, 0.62, (("N", 0.9),)),
             ("A", {"hi": "आँसू"}, 0.88, (("H", 0.3),))),
    "mr13q": (("A", {"hi": "आँसुओं"}, 0.3, (("t0", 0.2),)),
              ("Q", {"hi": "क्या"}, 0.72, (("A", 0.4),))),
    "mr14": (("S", {"hi": "बोले"}, 0.15, (("t0", 0.2),)),
             ("A", {"hi": "आँसू"}, 0.3, (("S", 0.4),)),
             ("B", {"hi": "बीमारियाँ"}, 0.42, (("A", 0.6),)),
             ("L", {"hi": "लोग"}, 0.62, (("B", 1.0),)),
             ("M", {"hi": "मरेंगे"}, 0.9, (("L", 0.6),))),
    "mr15": (("T", {"hi": "समय"}, 0.2, (("t0", 0.3),)),
             ("J", {"hi": "जाना"}, 0.45, (("T", 0.6),)),
             ("P", {"hi": "पाप"}, 0.65, (("J", 0.6),)),
             ("N", {"hi": "लगेगा"}, 0.9, (("P", 0.6),))),
    "mr16": (("M", {"hi": "मानी"}, 0.4, (("t0", 0.5),)),
             ("D", {"hi": "दुनिया"}, 0.62, (("M", 0.6),)),
             ("A", {"hi": "आई"}, 0.92, (("D", 0.5),))),
    "mr16c": (("D", {"hi": "डरते"}, 0.22, (("t0", 0.4),)),
              ("P", {"hi": "पहली"}, 0.48, (("D", 0.8),)),
              ("A", {"hi": "आँसू"}, 0.82, (("P", 0.6),))),
    "mr17": (("Z", {"hi": "सज़ा"}, 0.4, (("t0", 0.5),)),
             ("R", {"hi": "ज़रूरत"}, 0.62, (("Z", 0.5),)),
             ("C", {"hi": "कमेंट"}, 0.85, (("R", 0.5),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_mr_cues", None)
    if cache is None:
        cache = {}
        tl._mr_cues = cache
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


def ground(cr, y=G, alpha=1.0):
    prop(cr, "ground", W / 2, y + 6, 0.82, alpha=alpha)


def dev(cr, x, y):
    return cr.user_to_device(x, y)


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


def counter(cr, t, t_in, label, value, x, y, s, alpha=1.0, vcol=RED):
    """A leather plaque counter: a small label over a big number."""
    card(cr, t, t_in, x, y, s, [(label, 54, INK, -50), (value, 104, vcol, 38)], alpha=alpha)


def commas(n):
    return f"{int(n):,}"


def word_plaque(cr, t, t_in, x, y, s, words, alpha=1.0, maxw=600.0):
    """A leather plaque dropping in on its rod with one row of words, centred and shrunk to fit maxw (plaque units):
    words = [(kind, text, size, colour, t_show)] (kind 'indic' = the spoken word in Devanagari, shaped by matplotlib;
    'latin' = English). As scenes_hanuman_curse.word_plaque."""
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


# ------------------------------------------------------------------ light: tears, fire, souls


def tear(cr, x, y, r, a):
    """One glowing tear: a soft light round a pale-blue drop with a white heart."""
    if a <= 0.01 or r <= 0.5:
        return
    glow(cr, x, y, r * 7, 0.42 * a)
    warm(cr, x, y, r * 4.2, 0.95 * a, TEAR_GLOW)
    cr.save()
    cr.translate(x, y)
    cr.new_path()
    cr.move_to(0, -2.4 * r)
    cr.curve_to(0.45 * r, -1.3 * r, r, -0.6 * r, r, 0.1 * r)
    cr.arc(0, 0.1 * r, r, 0, math.pi)
    cr.curve_to(-r, -0.6 * r, -0.45 * r, -1.3 * r, 0, -2.4 * r)
    cr.close_path()
    g = cairo.RadialGradient(-0.3 * r, -0.1 * r, 0, 0, 0, 1.5 * r)
    g.add_color_stop_rgba(0, 1.0, 1.0, 1.0, a)
    g.add_color_stop_rgba(1, *MC.TEAR, 0.9 * a)
    cr.set_source(g)
    cr.fill_preserve()
    cr.set_source_rgba(0.22, 0.42, 0.70, 0.7 * a)
    cr.set_line_width(max(1.2, r * 0.14))
    cr.stroke()
    cr.restore()


def cheek(cr, eye, s, a, flip=False):
    """The wet, glowing line her tears leave down her cheek."""
    if a <= 0.01:
        return
    sg = -1 if flip else 1
    pts = [(eye[0], eye[1]), (eye[0] + sg * 6 * s, eye[1] + 30 * s), (eye[0] + sg * 12 * s, eye[1] + 62 * s)]
    glow(cr, eye[0], eye[1], 90 * s + 30, 0.35 * a)
    warm(cr, eye[0] + sg * 6 * s, eye[1] + 30 * s, 70 * s + 20, 0.8 * a, TEAR_GLOW)
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, col, al in ((14 * s + 4, TEAR_GLOW, 0.35), (6 * s + 2, MC.TEAR, 0.9), (2.2 * s + 1, (1, 1, 1), 0.9)):
        cr.move_to(*pts[0])
        cr.curve_to(*pts[1], *pts[1], *pts[2])
        cr.set_source_rgba(*col, al * a)
        cr.set_line_width(lw)
        cr.stroke()
    cr.restore()


def tears(cr, t, eye, s, a=1.0, rate=2.2, flip=False, big=1.0, seed=0.0, floor=None, life=1.7):
    """Her tears: drops gather under the eye, run down the cheek, then fall, glowing (a pure function of t)."""
    if a <= 0.01:
        return
    cheek(cr, eye, s, a, flip)
    sg = -1 if flip else 1
    n0 = int(t * rate)
    for k in range(n0 - int(life * rate) - 2, n0 + 1):
        ts = k / rate + 0.12 * math.sin(k * 1.7 + seed)
        u = t - ts
        if not 0 <= u < life:
            continue
        if u < 0.4:
            q = ease(u / 0.4)
            x, y = eye[0] + sg * 12 * s * q, eye[1] + 64 * s * q
        else:
            v = u - 0.4
            x = eye[0] + sg * (12 * s + 50 * s * v)
            y = eye[1] + 64 * s + 0.5 * 1100 * s * v * v
        if floor is not None and y > floor:
            continue
        fade = clamp((life - u) / 0.5) * clamp(u / 0.12)
        r = 11 * s * big * (0.85 + 0.25 * math.sin(k * 2.3 + seed))
        tear(cr, x, y, r, a * fade)
        if u > 0.4:
            sparkle(cr, x + 4 * s, y - 2 * r, 2.4 * r * (0.7 + 0.3 * math.sin(t * 9 + k)), 0.8 * a * fade,
                    (0.92, 0.98, 1.0))


def tear_arc(cr, t, t0, t1, p0, p1, s=1.0, lift=200.0, rate=4.0, dur=0.9, alpha=1.0):
    """Tears flying from p0 to p1 along an arc, one every 1/rate s between t0 and t1."""
    if t < t0 or alpha <= 0.01:
        return
    q = clamp((t - t0) / 0.4) * (1 - clamp((t - t1 - dur) / 0.4))
    if q > 0.01:                                        # a faint glowing path, so the stream reads as one
        path = [(p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u - lift * 4 * u * (1 - u))
                for u in (i / 40 for i in range(41))]
        cr.save()
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        for lw, col, al in ((26, TEAR_GLOW, 0.22), (8, MC.TEAR, 0.45)):
            cr.move_to(*path[0])
            for p in path[1:]:
                cr.line_to(*p)
            cr.set_source_rgba(*col, al * q * alpha)
            cr.set_line_width(lw)
            cr.stroke()
        cr.restore()
    k = 0
    while True:
        ts = t0 + k / rate
        if ts > t1 or ts > t:
            break
        k += 1
        u = (t - ts) / dur
        if not 0 < u < 1:
            continue
        e = u * u * (3 - 2 * u)
        x = p0[0] + (p1[0] - p0[0]) * e
        y = p0[1] + (p1[1] - p0[1]) * e - lift * 4 * e * (1 - e)
        tear(cr, x, y, 13 * s, alpha * clamp((1 - u) * 6))


def pool(cr, t, p, s, a):
    """The tears held in Brahma's cupped palms: a little lens of glowing blue water in his hands, drops glinting on
    it, a soft blue light round it."""
    if a <= 0.01:
        return
    x, y = p
    pulse = 0.85 + 0.15 * math.sin(t * 3.0)
    glow(cr, x, y, 260 * s + 60, 0.6 * a * pulse)
    warm(cr, x, y - 10 * s, 260 * s + 40, 0.95 * a * pulse, TEAR_GLOW)
    rx, ry = 88 * s, 26 * s
    cr.save()
    cr.translate(x, y)
    cr.new_path()
    cr.save()
    cr.scale(rx, ry)
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    g = cairo.LinearGradient(0, -ry, 0, ry)
    g.add_color_stop_rgba(0, 0.90, 0.97, 1.0, a)
    g.add_color_stop_rgba(1, 0.36, 0.66, 0.98, a)
    cr.set_source(g)
    cr.fill_preserve()
    cr.set_source_rgba(0.14, 0.32, 0.66, 0.9 * a)
    cr.set_line_width(max(2.0, 4 * s))
    cr.stroke()
    cr.new_path()
    cr.save()
    cr.translate(-rx * 0.3, -ry * 0.25)
    cr.scale(rx * 0.35, ry * 0.3)
    cr.arc(0, 0, 1, 0, 2 * math.pi)
    cr.restore()
    cr.set_source_rgba(1, 1, 1, 0.9 * a)
    cr.fill()
    cr.restore()
    for i in range(3):
        tear(cr, x - 34 * s + 34 * s * i, y - 26 * s - 8 * s * math.sin(i * 1.9 + t * 2), 12 * s, a)
    sparkle(cr, x + 10 * s, y - 60 * s, (46 + 12 * math.sin(t * 5)) * s, a, (0.92, 0.98, 1.0))


def fire_stream(cr, t, t0, t1, p0, p1, lift=180.0, alpha=1.0, n=16, dur=0.8, back_=False):
    """A stream of fire-light from p0 to p1 along an arc (back_: from p1 to p0, pulled back)."""
    if t < t0 or alpha <= 0.01:
        return
    q = clamp((t - t0) / 0.4) * (1 - clamp((t - t1 - dur) / 0.4))
    if back_:
        p0, p1 = p1, p0
    if q > 0.01:
        path = [(p0[0] + (p1[0] - p0[0]) * u, p0[1] + (p1[1] - p0[1]) * u - lift * 4 * u * (1 - u))
                for u in (i / 40 for i in range(41))]
        cr.save()
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        for lw, col, a in ((54, (1.0, 0.42, 0.08), 0.20), (22, (1.0, 0.56, 0.12), 0.42), (7, (1.0, 0.90, 0.55), 0.9)):
            cr.move_to(*path[0])
            for p in path[1:]:
                cr.line_to(*p)
            cr.set_source_rgba(*col, a * q * alpha)
            cr.set_line_width(lw)
            cr.stroke()
        cr.restore()
    step = max(0.04, (t1 - t0) / n)
    k = 0
    while True:
        ts = t0 + k * step
        if ts > t1 or ts > t:
            break
        k += 1
        u = (t - ts) / dur
        if not 0 < u < 1:
            continue
        e = u * u * (3 - 2 * u)
        x = p0[0] + (p1[0] - p0[0]) * e
        y = p0[1] + (p1[1] - p0[1]) * e - lift * 4 * e * (1 - e)
        glow(cr, x, y, 110, 0.5 * alpha)
        sparkle(cr, x, y, 34 * (0.75 + 0.35 * math.sin(math.pi * u)), 0.95 * alpha, (1.0, 0.70, 0.30))


def soul(cr, t, x, y, s, a):
    """A soul: a small, soft golden light (a flame-like orb with slow rays) centred on (x, y)."""
    if a <= 0.01:
        return
    r = 26 * s
    glow(cr, x, y, r * 7, 0.7 * a)
    warm(cr, x, y, r * 5, 0.9 * a)
    aura(cr, t, x, y, r * 1.1, r * 3.4, 0.8 * a, n=12, spin=0.5)
    g = cairo.RadialGradient(x - r * 0.25, y - r * 0.3, 0, x, y, r)
    g.add_color_stop_rgba(0, 1.0, 1.0, 0.94, a)
    g.add_color_stop_rgba(0.6, 1.0, 0.86, 0.45, a)
    g.add_color_stop_rgba(1, 1.0, 0.62, 0.20, 0.95 * a)
    cr.save()
    cr.new_path()
    cr.move_to(x, y - r * 1.9)                          # a little flame-shaped light
    cr.curve_to(x + r * 0.7, y - r * 1.0, x + r, y - r * 0.4, x + r, y + r * 0.1)
    cr.arc(x, y + r * 0.1, r, 0, math.pi)
    cr.curve_to(x - r, y - r * 0.4, x - r * 0.7, y - r * 1.0, x, y - r * 1.9)
    cr.close_path()
    cr.set_source(g)
    cr.fill_preserve()
    cr.set_source_rgba(0.55, 0.26, 0.04, 0.8 * a)
    cr.set_line_width(max(1.5, r * 0.1))
    cr.stroke()
    cr.restore()
    sparkle(cr, x, y - r * 0.4, r * 2.2 * (0.8 + 0.2 * math.sin(t * 4)), a)


# ------------------------------------------------------------------ the round world and its crowd


R0 = 236.0                           # kb_world's rim (its units)


@functools.lru_cache(maxsize=1)
def crowd_slots():
    """Places on the world's rim (angle from the top, row 0 = front / 1 = behind), each with its silhouette, in the
    order they appear: people first, a few at a time, spread round the world."""
    rng = random.Random(22)
    people = ["mr_p_man", "mr_p_woman", "mr_p_child", "mr_p_man", "mr_p_woman", "mr_p_old"]
    animals = ["mr_a_cow", "mr_a_deer", "mr_a_goat", "mr_a_dog", "mr_a_elephant", "mr_a_cow"]
    slots = []
    for row, (a0, a1, step) in enumerate(((-1.40, 1.40, 0.094), (-1.36, 1.36, 0.094))):
        a = a0 + (step / 2 if row else 0.0)
        i = 0
        while a <= a1 + 1e-6:
            kind = rng.choice(animals) if (i % 3 == 1) else rng.choice(people)
            slots.append((a, row, kind, rng.random() < 0.5, rng.random() * 6.28))
            a += step
            i += 1
    front = [x for x in slots if x[1] == 0]
    behind = [x for x in slots if x[1] == 1]
    rng.shuffle(front)
    rng.shuffle(behind)
    first = [x for x in front if x[2].startswith("mr_p")][:8] + [x for x in front if x[2].startswith("mr_a")][:4]
    rest = [x for x in front if x not in first]
    return first + rest + behind


N_SLOTS = len(crowd_slots())
UP_OF = {"mr_p_man": "mr_p_man_up", "mr_p_old": "mr_p_man_up", "mr_p_child": "mr_p_man_up",
         "mr_p_woman": "mr_p_woman_up"}


def flames_ring(cr, t, cx, cy, r, a):
    """Fire-light rising behind the world (drawn before it): flames of light round its rim, an orange glow."""
    if a <= 0.01:
        return
    glow(cr, cx, cy, r * 2.6, 0.8 * a)
    warm(cr, cx, cy, r * 2.2, 0.9 * a, FIRE_C)
    aura(cr, t, cx, cy, r * 0.9, r * 1.9, 0.9 * a, n=26, col=FIRE_C, spin=0.1)
    for i in range(14):
        ang = -2.2 + 4.4 * i / 13
        k = 0.75 + 0.25 * math.sin(t * 6 + i * 1.7)
        x, y = cx + r * 0.8 * math.sin(ang), cy - r * 0.8 * math.cos(ang)
        prop(cr, f"flame{(int(t * 10) + i) % 3}", x, y, r / 300 * 0.62 * k * a, rot=ang, alpha=0.85 * a)


def world(cr, t, cx, cy, r, count=0.0, alarm=0.0, fire=0.0, lying=(), alpha=1.0, spin=0.0, hover=0.0, souls=0.0,
          t_pop=0.0):
    """kb_world drawn with radius r px at (cx, cy), the first `count` crowd places filled (the next one popping in);
    alarm 0..1 throws their arms up; fire 0..1 lights flames behind the world; lying = slot indices lying down asleep
    (souls 0..1 lifts a soft light from each). Returns {"top": the crowd's top centre}."""
    if alpha <= 0.01:
        return {"top": (cx, cy - r)}
    flames_ring(cr, t, cx, cy, r, fire * alpha)
    k = r / R0
    fs = r / 300.0
    slots = crowd_slots()
    n = min(N_SLOTS, int(math.ceil(count)))

    def fig_at(i, behind):
        a, row, kind, fl, ph = slots[i]
        if (row == 1) != behind:
            return
        p = clamp(count - i) if i == n - 1 else 1.0
        q = back(clamp(p), 1.8)
        if q <= 0.01:
            return
        ang = a + spin
        sc = fs * (0.62 if kind.startswith("mr_a") else 1.0) * (0.86 if row else 1.0) * q
        name = kind
        jump = 0.0
        if alarm > 0.5 and kind in UP_OF:
            name = UP_OF[kind]
            jump = 10 * fs * abs(math.sin(t * 7 + ph)) * alarm
        rr = r - 6 * k
        if i in lying and kind.startswith("mr_p"):
            name = "mr_p_lying"
            sc = fs * 0.9
        bx = cx + (rr + jump) * math.sin(ang)
        by = cy - (rr + jump) * math.cos(ang)
        prop(cr, name, bx, by, sc, rot=ang + 0.04 * math.sin(t * 2.2 + ph), flip=fl, alpha=alpha * (0.8 if row else 1))
    for i in range(n):
        fig_at(i, True)
    prop(cr, "kb_world", cx, cy, k, rot=0.02 * math.sin(t * 0.7), alpha=alpha)
    for i in range(n):
        fig_at(i, False)
    if souls > 0.01:
        for j, i in enumerate(sorted(lying)):
            a = slots[i][0] + spin
            u = clamp(souls * 1.3 - 0.15 * j)
            if u > 0.01:
                bx = cx + (r + 30 * fs + 150 * fs * ease(u)) * math.sin(a)
                by = cy - (r + 30 * fs + 150 * fs * ease(u)) * math.cos(a)
                soul(cr, t, bx, by, 0.6 * fs, alpha * math.sin(math.pi * min(1.0, u)) ** 0.5)
    if hover > 0.01:                                    # one more little man, with no room to stand
        hy = cy - r - 150 * fs - 14 * fs * math.sin(t * 5)
        prop(cr, "mr_p_man_up", cx, hy, fs * back(clamp(hover), 1.6), rot=0.12 * math.sin(t * 6), alpha=alpha)
    return {"top": (cx, cy - r - 130 * fs)}


# ------------------------------------------------------------------ puppets


def death(cr, t, x, s, mood="open", feet=G, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(), flip=False,
          alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.4, y=None, leg=False):
    """Mrityu standing (feet on `feet`); leg = standing on one leg. Returns her points (device)."""
    hy = feet - 470 * s if y is None else y
    ang = woman_angles("mr_death", t, front, backa, head, hits, ph)
    sw = {"mr_death_head": "mr_death_head" + ("" if mood == "open" else "_" + mood)}
    if leg:
        sw["mr_death_body"] = "mr_death_body_leg"
    return puppet(cr, MC.DEATH, x, hy, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, swap=sw, rods=rods)


def w_reach(x, feet, s, target, front=True, flip=False, head_k=None):
    """(upper, fore) so a woman puppet's hand lands on target (her shoulders at (22 | -12, -262))."""
    return reach_arm(x, feet - 470 * s, s, 22 if front else -12, target, flip)


def mouth_target(x, feet, s, flip=False, head=0.0):
    """Where her hand goes to cover her mouth (scene coordinates), for a head turned by `head`."""
    sg = -1 if flip else 1
    hx, hy = x + sg * 2 * s, feet - 470 * s - 292 * s
    px, py = 70, -58
    c, si = math.cos(head), math.sin(head)
    return hx + sg * s * (px * c - py * si), hy + s * (px * si + py * c)


def weep_pose(x, feet, s, flip=False, head=0.12):
    """Her front hand at her mouth (a sob), the other arm hanging."""
    tg = mouth_target(x, feet, s, flip, head)
    return dict(front=w_reach(x, feet, s, (tg[0], tg[1] + 10 * s), True, flip), backa=(0.12, -0.3))


def earth(cr, t, x, s, mood="tired", feet=G, front=(-0.08, -0.35), backa=(0.15, -0.2), head=0.0, hits=(),
          flip=False, alpha=1.0, blur=0.0, rods=True, rot=0.0, ph=0.9, y=None):
    hy = feet - 470 * s if y is None else y
    ang = woman_angles("mr_earth", t, front, backa, head, hits, ph)
    sw = {"mr_earth_head": "mr_earth_head" + ("" if mood == "open" else "_" + mood)}
    return puppet(cr, MC.EARTH, x, hy, s, rot, flip, ang, alpha, blur, swap=sw, rods=rods)


BR_LEGS = ("c6_brahma_legF", "c6_brahma_legB")
BLESS = (-2.5, -0.4)                 # Brahma's front hand raised in blessing
CUP_ARMS = dict(front=(-1.45, -0.55), backa=(-1.3, -0.65))   # both cupped hands held out in front of him


def brahma_hip(ground_, s):
    return ground_ - 165 * s - C6.SEAT_H * s + 10 * s


def brahma(cr, t, x, ground_, s, front=(-0.7, -1.7), backa=(0.25, -1.0), flip=False, alpha=1.0, blur=0.0,
           glow_a=1.0, hits=(), rods=True, mood="calm", cup=False, head=0.0, anger=0.0):
    """Brahma (six_cast_c) seated on his lotus (the lotus on ground_): mood calm | angry; cup = both palms cupped
    (no Veda); anger 0..1 turns his light orange."""
    sg = -1 if flip else 1
    hy = brahma_hip(ground_, s)
    if glow_a > 0:
        gx, gy = x, ground_ - 520 * s
        glow(cr, x, ground_ - 420 * s, 620 * s + 160, 0.6 * glow_a * alpha)
        aura(cr, t, gx, gy, 240 * s, 760 * s, 0.4 * glow_a * alpha * (1 - anger), n=22, spin=0.05)
        if anger > 0.01:
            warm(cr, gx, gy, 700 * s, 0.9 * anger * alpha, FIRE_C)
            aura(cr, t, gx, gy, 240 * s, 900 * s, 0.85 * anger * alpha, n=26, col=FIRE_C, spin=0.2)
    prop(cr, "md_lotus", x + sg * 30 * s, ground_ - 165 * s, s * 1.5, rot=sway(t, 0.005, 0.3, 2.0), alpha=alpha,
         blur=blur, flip=flip)
    prop(cr, "c6_brahma_seat", x, hy, s, alpha=alpha, blur=blur, flip=flip)
    ang = man_angles("c6_brahma", t, front, backa, head, (0.0, 0.0), hits, 0.8)
    sw = {"c6_brahma_body": "c6_brahma_body_sit"}
    if mood == "angry":
        sw["c6_brahma_head"] = "mr_brahma_head_angry"
    ex = None
    if cup:
        sw["c6_brahma_armF_lo"] = sw["c6_brahma_armB_lo"] = "mr_brahma_lo_cup"
    else:
        ex = {"c6_brahma_armB_lo": held("c6_veda", backa, 0.8, dy=160, alpha=alpha, blur=blur)}
    return puppet(cr, C6.BRAHMA, x, hy, s, bob_rot(t, 0.8, 0.005), flip, ang, alpha, blur, hide=BR_LEGS, swap=sw,
                  extra=ex, rods=rods)


def cup_point(cr, pts, s, flip=False):
    """The bowl of his cupped palms (scene coordinates), from the front hand."""
    hx, hy = to_user(cr, pts["handF"])
    return hx + (-8 if flip else 8) * s, hy - 22 * s


def shiva(cr, t, x, s, mood="calm", stop=0.0, feet=G, flip=False, alpha=1.0, blur=0.0, hits=(), ph=1.0, rods=True,
          y=None, legs=(0.0, 0.0), rot=0.0):
    """Shiva (shikhandi_cast), his trident upright in his back hand; stop 0..1 raises his front hand, palm out."""
    ba = (0.5, 0.15)                                    # the trident upright behind him
    ex = {"sk_shiva_armB_lo": held_grip("sg_trishul", ba, 1.2, 0.0, -115.0, alpha, blur)}
    fr = mix((-0.32, -0.55), (-2.0, -0.9), stop)
    sw = {"sk_shiva_head": "sk_shiva_head" + ("" if mood == "calm" else "_" + mood)}
    return fig(cr, SKC.SHIVA, "sk_shiva", t, x, s, front=fr, backa=ba, feet=feet, flip=flip, alpha=alpha, blur=blur,
               swap=sw, extra=ex, hits=hits, ph=ph, rods=rods, y=y, legs=legs, rot=rot)


def fear_row(cr, t, x0, y, s, a, t_in, n=5, spread=70.0, shrink=0.0):
    """A little row of the world's people, far away and afraid (arms up), shrinking back."""
    if a <= 0.01:
        return
    kinds = ("mr_p_man_up", "mr_p_woman_up", "mr_p_child", "mr_p_man_up", "mr_p_woman", "mr_p_old")
    for i in range(n):
        q = back(clamp((t - t_in - 0.08 * i) / 0.3), 1.6)
        if q <= 0.01:
            continue
        x = x0 + spread * i + 12 * shrink * (i + 1)
        prop(cr, kinds[i % len(kinds)], x, y, s * q * (0.9 if i % 2 else 1.0),
             rot=0.16 * shrink + 0.03 * math.sin(t * 3 + i), alpha=a * 0.95, flip=i % 2 == 1)


# ------------------------------------------------------------------ mr1  hook


HK = (420, 1.3, 1985)                # the girl in the hook: x, scale, feet


def hook_girl(cr, t, mood, shake=0.0, sob=(), tear_k=1.0, surge=None):
    """The hook's picture (also the callback's): the girl large, a hand at her mouth, tears running."""
    x, s, feet = HK
    head = 0.12 + shake * 0.13 * math.sin(t * 5.5)
    glow(cr, x + 60, feet - 820 * s, 700, 0.42)
    pose = weep_pose(x, feet, s, head=head)
    pts = death(cr, t, x, s, mood=mood, feet=feet, head=head, hits=sob, ph=0.3, **pose)
    eye = to_user(cr, pts["eye"])
    big = 1.0 + (0.5 * flash_at(t, surge, 1.0, 2.0) if surge is not None else 0.0)
    tears(cr, t, eye, s, tear_k, rate=2.0 + (2.5 * flash_at(t, surge, 1.0, 1.5) if surge is not None else 0),
          big=big, floor=1930)
    return pts, eye


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "mr1")
    tM, tD, tR, tK, tN = c["M"], c["D"], c["R"], c["K"], c["N"]
    shrink = prog(t, tD + 0.3, 0.8)
    fear_row(cr, t, 650, 1870, 1.2, 1.0, tD - 0.05, n=5, spread=80, shrink=shrink)
    mood = "sad" if t < tR - 0.05 else ("cry" if t < tN + 0.6 else "sad")
    pts, eye = hook_girl(cr, t, mood, shake=prog(t, tN, 0.4) * (1 - prog(t, tN + 2.0, 0.5)),
                         sob=[(tR, 0.35)], surge=tR)
    tg = dev(cr, eye[0] + 300, eye[1] - 40)

    def ui(cr):
        if t < tK - 0.1:
            head2(cr, t, "DEATH HERSELF", -1.0, "CRIED", 0.3, big_size=300, ghost=-1.0, under=tR)
        else:
            head2(cr, t, "SHE DIDN'T WANT TO", tK - 0.1, "TAKE ANY LIFE", tK + 0.05, big_size=230)
        tag(cr, t, 0.5, "DEATH", min(tg[0], 900), tg[1], 46)
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.2) + flash_at(t, tR, 0.3) + flash_at(t, tK, 0.15))


# ------------------------------------------------------------------ mr2  a true story from the Mahabharata


def s_book(cr, t, tl, t0, t1):
    c = cues(tl, "mr2")
    tM, tS = c["M"], c["S"]
    leaves = [(None, [("MAHABHARATA", 92, HEAD_FONT)], 0),
              (tS, [([("A TRUE STORY", RED)], 84, HEAD_FONT)], 0)]
    book(cr, t, 540, 980, 0.86, leaves, t_in=t0 - 0.05, t_open=tM - 0.15, ring=(1, 0, 0, tS + 0.3))

    def ui(cr):
        head2(cr, t, "A TRUE STORY FROM THE", t0 + 0.05, "MAHABHARATA", tM, big_size=220, under=tS + 0.2)
    return dict(ui=ui, flash=flash_at(t, tM, 0.25) + flash_at(t, tS, 0.15))


# ------------------------------------------------------------------ mr3  Brahma makes the world; nobody died


BR3 = (270, 1520, 0.6)               # Brahma: x, lotus ground, scale
W3 = (770, 1240, 190)                # the world: centre, radius


def s_create(cr, t, tl, t0, t1):
    c = cues(tl, "mr3")
    tB, tW, tN = c["B"], c["W"], c["N"]
    bx, bg, bs = BR3
    raise_ = keyed(t, [(t0, 0.0), (tW - 0.4, 1.0)], 0.3, 1.3)
    b, k, a = depth(t, t0 - 0.2, 0.45)
    pts = brahma(cr, t, bx, bg, bs * k, front=mix((-0.7, -1.7), (-2.1, -0.5), raise_), alpha=a, blur=b,
                 hits=[(tW - 0.4, 0.4)])
    hand = to_user(cr, pts["handF"])
    wx, wy, wr = W3
    wq = back(clamp((t - tW) / 0.45), 1.5)
    if t > tW - 0.05:
        burst(cr, t, wx, wy, tW, n=18, rmax=520, alpha=0.7)
    count = 12 * clamp((t - tW - 0.4) / max(0.8, tN - tW - 0.2))
    if wq > 0.01:
        cr.save()
        cr.translate(wx, wy)
        cr.scale(wq, wq)
        cr.translate(-wx, -wy)
        world(cr, t, wx, wy, wr, count=count)
        cr.restore()
        flow(cr, t, tW + 0.3, tN, hand, (wx, wy - wr - 30), n=10, lift=200, alpha=0.9, r=22, dur=0.8)
    dv_b = dev(cr, bx + 10, bg - 950 * bs)
    dv_c = dev(cr, 540, 1785)

    def ui(cr):
        if t < tN - 0.1:
            head2(cr, t, "LONG AGO, BRAHMA", t0 + 0.05, "MADE THE WORLD", tW, big_size=230)
        else:
            head2(cr, t, "AND BACK THEN,", tN - 0.1, "NOBODY DIED", tN + 0.05, big_size=250)
        tag(cr, t, tB + 0.1, "BRAHMA", max(170, dv_b[0]), dv_b[1], 40, t_out=tN - 0.3)
        if t > tN - 0.2:
            counter(cr, t, tN - 0.2, "DEATHS", "0", dv_c[0], dv_c[1], 0.62)
            red_ring(cr, dv_c[0], dv_c[1] + 24, 76, 66, prog(t, tN + 0.35, 0.4), 8)
    return dict(ui=ui, flash=flash_at(t, tW, 0.3) + flash_at(t, tN, 0.2))


# ------------------------------------------------------------------ mr4  more and more: no room left


W4 = (540, 1200, 285)


def s_crowd(cr, t, tl, t0, t1):
    c = cues(tl, "mr4")
    tP, tA, tG, tF, tJ = c["P"], c["A"], c["G"], c["F"], c["J"]
    wx, wy, wr = W4
    glow(cr, wx, wy, 760, 0.35)
    u = clamp((t - tP + 0.1) / max(1.0, tJ - tP - 0.2))
    count = 12 + (N_SLOTS - 12) * (u ** 1.6)
    w = world(cr, t, wx, wy, wr, count=count, hover=prog(t, tJ + 0.1, 0.35), spin=0.0)
    top = w["top"]
    dv_top = dev(cr, top[0], top[1] - 70)
    dv_c = dev(cr, 540, 1795)
    dv_p, dv_a = dev(cr, 210, 960), dev(cr, 880, 1450)
    pop = 2 * 10 ** (9 * clamp((t - tG) / max(1.0, tJ - tG)) ** 1.3)

    def ui(cr):
        if t < tJ - 0.1:
            head2(cr, t, "THEY KEPT GROWING AND", t0 + 0.05, "GROWING", tG, big_size=270)
        else:
            head2(cr, t, "ON EARTH THERE WAS", tJ - 0.1, "NO ROOM LEFT", tJ + 0.05, big_size=240)
        plate(cr, t, tP + 0.1, "PEOPLE", dv_p[0], dv_p[1], 40, t_out=tF)
        plate(cr, t, tA + 0.1, "ANIMALS", dv_a[0], dv_a[1], 40, t_out=tF)
        counter(cr, t, tG - 0.2, "PEOPLE", commas(pop), dv_c[0], dv_c[1], 0.62)
        if t > tJ + 0.1:
            red_ring(cr, dv_top[0], dv_top[1] + 10, 90, 110, prog(t, tJ + 0.2, 0.35), 8)
            plate(cr, t, tJ + 0.4, "NO ROOM!", dv_top[0] + 200, dv_top[1] - 30, 40, color=RED)
    return dict(ui=ui, flash=flash_at(t, tG, 0.15) + flash_at(t, tJ, 0.2))


# ------------------------------------------------------------------ mr5  Mother Earth: "I can't carry this!"


ER5 = (650, 0.84)                    # Mother Earth: x, scale (facing left, bent)
BR5 = (215, 1780, 0.5)               # Brahma, small
LEAN = -0.34                         # how far she bends under the load
WL5 = (-290, -330, 205)              # the world on her back: centre and radius (her root units, unflipped)


def earth_load(cr, t, x, s, feet, mood, lean, tremble, alpha=1.0, blur=0.0, plead=0.0, head=0.25, hits=()):
    """Mother Earth bent forward (facing left) under the crowded world on her back: her back hand holds it from
    below, her front hand rests on her thigh (tired), then reaches out to Brahma (plead 0..1)."""
    flip = True
    rot = lean + tremble * 0.015 * math.sin(t * 17)
    hy = feet - 470 * s
    lx, ly, lr = WL5
    wc = local(x, hy, s, rot, flip, lx, ly)
    wc = (wc[0], wc[1] + 4 * tremble * math.sin(t * 17))
    wr = lr * s
    hold_b = reach_arm(x, hy, s, -12, local(x, hy, s, 0.0, flip, -150, -150), flip)
    fr = mix((-0.45, -0.1), (-1.35, -0.75), plead)
    world(cr, t, wc[0], wc[1], wr, count=N_SLOTS, alpha=alpha)
    pts = earth(cr, t, x, s, mood=mood, feet=feet, front=fr, backa=hold_b, head=head, flip=flip, rot=rot,
                alpha=alpha, blur=blur, hits=hits)
    return pts, wc, wr


def s_earth(cr, t, tl, t0, t1):
    c = cues(tl, "mr5")
    tE, tT, tS, tU = c["E"], c["T"], c["S"], c["U"]
    ground(cr)
    glow(cr, 560, 1300, 640, 0.35)
    bx, bg, bs = BR5
    brahma(cr, t, bx, bg, bs, glow_a=0.6, hits=[(tS, 0.2)])
    x, s = ER5
    walk_x, bob, rock, _ = pc.hop_walk(t, t0 - 0.2, tE + 0.3, 1100, x, 0.55)
    b, k, a = depth(t, t0 - 0.3, 0.5)
    tired = prog(t, tT, 0.4)
    plead = prog(t, tS, 0.4)
    pts, wc, wr = earth_load(cr, t, walk_x, s * k, G + bob * 0.5, "plead" if t > tS else ("tired" if t > tT - 0.2
                             else "open"), LEAN * (0.6 + 0.4 * tired) + rock * 0.5, 0.3 + 0.7 * tired,
                             alpha=a, blur=b, plead=plead, head=0.25 - 0.3 * plead, hits=[(tU, 0.4)])
    if t > tT:                                          # drops of sweat: she is so tired
        top = to_user(cr, pts["head"])
        for i in range(3):
            u = ((t - tT) * 0.9 + i / 3) % 1.0
            tear(cr, top[0] + 30 - 30 * i, top[1] - 20 + 120 * u * u, 7, 0.7 * math.sin(math.pi * u))
    dv_e = dev(cr, wc[0] + 20, wc[1] - wr - 150)
    dv_cl = dev(cr, 380, 570)

    def ui(cr):
        if t < tS - 0.1:
            head2(cr, t, "MOTHER EARTH WAS SO", t0 + 0.05, "TIRED", tT, big_size=290)
            tag(cr, t, tE + 0.1, "MOTHER EARTH", dv_e[0], dv_e[1], 36, t_out=tS - 0.3)
        else:
            head2(cr, t, "SHE SAID TO BRAHMA:", tS - 0.1, None, 0.0)
            cloud_text(cr, t, dv_cl[0], dv_cl[1], 0.7, [("I CAN'T CARRY", 70, INK, -40, tS + 0.15),
                                                        ("THIS ANY MORE!", 84, RED, 50, tU)], flip=True, t_in=tS)
    return dict(ui=ui, flash=flash_at(t, tT, 0.15) + flash_at(t, tU, 0.2))


# ------------------------------------------------------------------ mr6  Brahma's anger: fire; the world burns


BR6 = (290, 1330, 0.62)
W6 = (690, 1490, 215)


def s_fire(cr, t, tl, t0, t1):
    c = cues(tl, "mr6")
    tA, tF, tJ = c["A"], c["F"], c["J"]
    anger = prog(t, tA - 0.1, 0.4)
    burn = prog(t, tJ - 0.1, 0.6)
    wx, wy, wr = W6
    bx, bg, bs = BR6
    shake = anger * 0.02 * math.sin(t * 28)
    pts = brahma(cr, t, bx, bg, bs, mood="angry" if t > tA - 0.1 else "calm", anger=anger,
                 front=mix((-0.7, -1.7), (-1.9, -0.4), prog(t, tF - 0.3, 0.3)), head=shake, hits=[(tA, 0.4)])
    hand = to_user(cr, pts["handF"])
    world(cr, t, wx, wy, wr, count=N_SLOTS, alarm=burn, fire=burn)
    fire_stream(cr, t, tF, t1, hand, (wx, wy - wr * 0.4), lift=160, alpha=1.0)
    dv_b = dev(cr, bx, bg - 900 * bs)

    def ui(cr):
        if t < tF - 0.1:
            head2(cr, t, "BRAHMA GOT SO", t0 + 0.05, "ANGRY", tA, big_size=300)
        elif t < tJ - 0.1:
            head2(cr, t, "HIS ANGER BECAME", tF - 0.1, "FIRE", tF + 0.05, big_size=300)
        else:
            head2(cr, t, "AND THE WORLD BEGAN TO", tJ - 0.1, "BURN", tJ + 0.05, big_size=300)
        if t < tF:
            for i in range(3):                           # puffs of anger over his head
                u = (t * 1.3 + i / 3) % 1.0
                a_ = anger * (1 - u)
                if a_ > 0.01:
                    cr.new_path()
                    cr.arc(dv_b[0] - 50 + 50 * i, dv_b[1] - 60 - 90 * u, 10 + 16 * u, 0, 2 * math.pi * 0.8)
                    cr.set_source_rgba(0.75, 0.10, 0.05, 0.75 * a_)
                    cr.set_line_width(6)
                    cr.stroke()
    return dict(ui=ui, flash=flash_at(t, tA, 0.15) + flash_at(t, tF, 0.3) + flash_at(t, tJ, 0.2),
                eve=0.42 * burn + 0.15 * anger)


# ------------------------------------------------------------------ mr7  Shiva: "stop!"


BR7 = (250, 1780, 0.55)
SH7 = (820, 0.74)
W7 = (530, 1650, 88)


def s_shiva(cr, t, tl, t0, t1):
    c = cues(tl, "mr7")
    tS, tR, tM = c["S"], c["R"], c["M"]
    ground(cr)
    calm = prog(t, tR + 0.2, 0.5)
    bx, bg, bs = BR7
    brahma(cr, t, bx, bg, bs, mood="angry" if calm < 0.5 else "calm", anger=0.8 * (1 - calm),
           front=mix((-1.9, -0.4), (-0.7, -1.7), calm), hits=[(tR, 0.4)])
    wx, wy, wr = W7
    world(cr, t, wx, wy, wr, count=N_SLOTS, alarm=1.0 - 0.6 * calm, fire=1.0 - 0.5 * calm)
    sx, ss = SH7
    t_in = t0 - 0.1
    x, bob, rock, legp = pc.hop_walk(t, t_in, max(tS + 0.3, t0 + 0.9), 1250, sx, 0.5)
    b, k, a = depth(t, t_in, 0.45)
    stop = keyed(t, [(t0, 0.0), (tR - 0.15, 1.0)], 0.22, 1.5)
    glow(cr, x - 20, G - 600 * ss, 620, 0.5 * a)
    talk = (tR - 0.1 < t < tR + 0.4) or (tM - 0.1 < t < tM + 0.6 and int(t * 6) % 2 == 0)
    sp = shiva(cr, t, x, ss * k, mood="speak" if talk else "calm", stop=stop, flip=True, alpha=a, blur=b,
               y=G - 434 * ss + bob - (k - 1) * 300 * ss, legs=(0.3 * legp, -0.3 * legp), rot=rock,
               hits=[(tR - 0.15, 0.6)])
    hnd = to_user(cr, sp["handF"])
    if t > tR - 0.15:                                   # light from his raised palm
        q = prog(t, tR - 0.15, 0.3)
        glow(cr, hnd[0], hnd[1] - 40, 260, 0.7 * q)
        aura(cr, t, hnd[0], hnd[1] - 40, 40, 200, 0.6 * q, n=14, spin=0.4)
    dv_s = dev(cr, sx + 20, 900)
    dv_h = dev(cr, hnd[0], hnd[1] - 40)
    dv_cl = dev(cr, 400, 770)

    def ui(cr):
        if t < tR - 0.15:
            head2(cr, t, "THEN CAME", t0 + 0.05, "SHIVA", tS, big_size=300)
            tag(cr, t, tS + 0.1, "SHIVA", min(dv_s[0], 900), dv_s[1], 40)
        else:
            head2(cr, t, "HE SAID:", tR - 0.15, "STOP!", tR, big_size=320)
            red_ring(cr, dv_h[0], dv_h[1], 95, 120, prog(t, tR + 0.1, 0.35), 8)
            cloud_text(cr, t, dv_cl[0], dv_cl[1], 0.62, [("DON'T BURN", 78, INK, -40, tM),
                                                         ("EVERYONE!", 88, RED, 50, tM + 0.25)], flip=True,
                       t_in=tM - 0.1)
    return dict(ui=ui, flash=flash_at(t, tS, 0.2) + flash_at(t, tR, 0.35), eve=0.25 * (1 - calm))


# ------------------------------------------------------------------ mr8  the fire goes back; a girl steps out


BR8 = (300, 1700, 0.66)
W8 = (800, 1660, 150)
GL8 = (740, 0.78)


def s_girl(cr, t, tl, t0, t1):
    c = cues(tl, "mr8")
    tW, tK, tP, tG = c["W"], c["K"], c["P"], c["G"]
    ground(cr)
    bx, bg, bs = BR8
    pull = prog(t, tW, max(0.8, tP - tW))
    gone = prog(t, tP - 0.3, 0.5)
    wx, wy, wr = W8
    world(cr, t, wx, wy + 300 * gone, wr, count=N_SLOTS, alarm=1.0 - pull, fire=0.9 * (1 - pull),
          alpha=1 - gone)
    pts = brahma(cr, t, bx, bg, bs, front=mix((-1.9, -0.6), (-0.7, -1.7), pull), hits=[(tK, 0.3)])
    chest = to_user(cr, pts["chest"])
    if t < tP:
        fire_stream(cr, t, tW, max(tW + 0.4, tP - 0.6), chest, (wx, wy - wr * 0.3), lift=150, alpha=1 - gone,
                    back_=True, n=12, dur=0.7)
    if t > tP - 0.05:
        burst(cr, t, chest[0], chest[1], tP, n=22, rmax=760, alpha=0.9)
        warm(cr, chest[0], chest[1], 420, 0.8 * flash_at(t, tP, 1.0, 1.2))
    gx, gs = GL8
    if t > tG - 0.5:                                    # out of his light steps a girl
        u = ease(clamp((t - tG + 0.5) / 0.9))
        x = chest[0] + (gx - chest[0]) * u
        b, k, a = depth(t, tG - 0.5, 0.9)
        glow(cr, x + 20, G - 560 * gs, 520, 0.6 * a)
        warm(cr, x + 20, G - 560 * gs, 360, 0.6 * a, DEATH_GLOW)
        death(cr, t, x, gs * k, mood="open", flip=True, alpha=a, blur=b, front=(-0.2, -0.4),
              y=G - 470 * gs - (k - 1) * 300 * gs, hits=[(tG + 0.4, 0.5)], rods=u > 0.7)
    dv_g = dev(cr, gx, 980)

    def ui(cr):
        if t < tP - 0.1:
            head2(cr, t, "BRAHMA PULLED THE FIRE", t0 + 0.05, "BACK IN", tK, big_size=280)
        else:
            head2(cr, t, "AND FROM HIS BODY CAME", tP - 0.1, "A GIRL", tG, big_size=290, under=tG + 0.5)
    return dict(ui=ui, flash=flash_at(t, tP, 0.4) + flash_at(t, tG, 0.2), eve=0.2 * (1 - pull))


# ------------------------------------------------------------------ mr9  "Mrityu: Death." "Go, take every life."


BR9 = (250, 1785, 0.6)
GL9 = (800, 0.8)
CARD9 = (540, 790, 0.82)


def s_name(cr, t, tl, t0, t1):
    c = cues(tl, "mr9")
    tN, tM, tY, tH, tJ, tL = c["N"], c["M"], c["Y"], c["H"], c["J"], c["L"]
    ground(cr)
    glow(cr, 540, 1350, 640, 0.35)
    bx, bg, bs = BR9
    hy = brahma_hip(bg, bs)
    order = prog(t, tJ - 0.2, 0.3)
    tgt = (1150, 760)
    fr = mix(mix((-0.7, -1.7), BLESS, prog(t, tN, 0.3) * (1 - order)), point_to(bx, hy, bs, tgt, bulk=1.12), order)
    brahma(cr, t, bx, bg, bs, front=fr, hits=[(tM, 0.3), (tJ, 0.4)])
    gx, gs = GL9
    shock = t > tL
    death(cr, t, gx, gs, mood="sad" if shock else "open", flip=True, head=0.05 * prog(t, tL, 0.4),
          front=mix((-0.2, -0.4), (-0.9, -1.9), prog(t, tL + 0.1, 0.3)), hits=[(tL, 0.5)], ph=0.4)
    cx, cy, cs = CARD9
    dc = dev(cr, cx, cy)
    word = ("indic", NAME_W, 150, RED, tM) if HAS_INDIC else ("latin", "MRITYU", 120, RED, tM)

    def ui(cr):
        if t < tH - 0.1:
            head2(cr, t, "BRAHMA NAMED HER", t0 + 0.05, "MRITYU", tM, big_size=290)
            word_plaque(cr, t, tM - 0.3, dc[0], dc[1], cs, [word, ("latin", "=", 110, INK, tY - 0.1),
                                                           ("latin", "DEATH", 120, INK, tY)])
        else:
            head2(cr, t, "AND HE ORDERED HER:", tH - 0.1, None, 0.0)
            card2(cr, t, tH + 0.05, dc[0], dc[1], 0.9, [("GO, TAKE", 84, INK, -46, min(tJ, tH + 0.2)),
                                                         ("EVERY LIFE!", 104, RED, 44, tL)])
    return dict(ui=ui, flash=flash_at(t, tM, 0.2) + flash_at(t, tY, 0.15) + flash_at(t, tL, 0.2))


# ------------------------------------------------------------------ mr10  she burst into tears: "how can I?"


GL10 = (400, 1.12, 1880)


def s_weep(cr, t, tl, t0, t1):
    c = cues(tl, "mr10")
    tF, tB, tK = c["F"], c["B"], c["K"]
    x, s, feet = GL10
    glow(cr, x + 60, feet - 820 * s, 680, 0.45)
    ask = prog(t, tB - 0.1, 0.35)
    head = 0.14 * (1 - ask) - 0.1 * ask
    pose = weep_pose(x, feet, s, head=head)
    fr = mix(pose["front"], PLEAD["front"], ask)
    ba = mix(pose["backa"], PLEAD["backa"], ask)
    mood = ("sad" if t < tF - 0.1 else "cry") if t < tB - 0.1 else "speak"
    pts = death(cr, t, x, s, mood=mood, feet=feet, head=head, front=fr, backa=ba, hits=[(tF, 0.4), (tB, 0.3)])
    eye = to_user(cr, pts["eye"])
    surge = flash_at(t, tF, 1.0, 1.0)
    tears(cr, t, eye, s, 1.0, rate=2.4 + 3.0 * surge, big=1.0 + 0.4 * surge, floor=1900)
    dv_cl = dev(cr, 790, 760)

    def ui(cr):
        if t < tB - 0.1:
            head2(cr, t, "HEARING THIS, SHE BURST INTO", t0 + 0.05, "TEARS", tF, big_size=300)
        else:
            head2(cr, t, "SHE ASKED:", tB - 0.1, None, 0.0)
            cloud_text(cr, t, dv_cl[0], dv_cl[1], 0.6, [("HOW CAN I", 80, INK, -40, tB + 0.1),
                                                        ("TAKE A LIFE?", 84, RED, 50, tK)], t_in=tB)
    return dict(ui=ui, flash=flash_at(t, tF, 0.25) + flash_at(t, tK, 0.15))


# ------------------------------------------------------------------ mr11  Brahma catches her tears in his palms


GL11 = (240, 0.84)
BR11 = (770, 1785, 0.68)


def s_catch(cr, t, tl, t0, t1):
    c = cues(tl, "mr11")
    tA, tH = c["A"], c["H"]
    ground(cr)
    glow(cr, 540, 1350, 640, 0.35)
    gx, gs = GL11
    pose = weep_pose(gx, G, gs, head=0.1)
    gp = death(cr, t, gx, gs, mood="cry", front=pose["front"], backa=pose["backa"], head=0.1, ph=0.3)
    eye = to_user(cr, gp["eye"])
    tears(cr, t, eye, gs, 0.9, rate=2.0, floor=G - 20)
    bx, bg, bs = BR11
    reach = keyed(t, [(t0, 0.0), (tA - 0.4, 1.0)], 0.3, 1.2)
    fr = mix((-0.7, -1.7), CUP_ARMS["front"], reach)
    ba = mix((0.25, -1.0), CUP_ARMS["backa"], reach)
    bp = brahma(cr, t, bx, bg, bs, flip=True, cup=True, front=fr, backa=ba, hits=[(tA - 0.4, 0.3)])
    cp = cup_point(cr, bp, bs, flip=True)
    fill = prog(t, tA, max(0.8, tH - tA))
    tear_arc(cr, t, tA - 0.1, t1, (eye[0] + 20, eye[1] + 30), cp, s=0.9, lift=180, rate=4.0, dur=0.85)
    pool(cr, t, cp, bs, 0.25 + 0.75 * fill)
    dv_c = dev(cr, *cp)

    def ui(cr):
        if t < tH - 0.1:
            head2(cr, t, "BRAHMA CAUGHT HER", t0 + 0.05, "TEARS", tA, big_size=300)
        else:
            head2(cr, t, "IN HIS TWO", tH - 0.1, "HANDS", tH + 0.05, big_size=300)
            red_ring(cr, dv_c[0], dv_c[1] - 10, 120, 95, prog(t, tH + 0.1, 0.35), 8)
    return dict(ui=ui, flash=flash_at(t, tA, 0.2) + flash_at(t, tH, 0.15))


# ------------------------------------------------------------------ mr12  on one leg, for billions of years


GL12 = (470, 0.95)


def s_oneleg(cr, t, tl, t0, t1):
    c = cues(tl, "mr12")
    tM, tP, tA = c["M"], c["P"], c["A"]
    yrs = clamp((t - tA + 0.3) / max(1.2, t1 - tA - 0.2))
    cyc = (t - tP) * (0.5 + 2.6 * yrs) if t > tP else 0.0       # days and nights racing past, faster and faster
    if t > tP:
        sa = math.sin(cyc * math.pi * 2)
        sx = 540 + 420 * math.cos(cyc * math.pi * 2)
        prop(cr, "sun" if sa > 0 else "moon", sx, 1000 - 360 * abs(sa), 0.45, alpha=prog(t, tP, 0.5) * abs(sa) ** 0.5)
    ground(cr)
    glow(cr, 520, 1300, 620, 0.4)
    gx, gs = GL12
    leg = t > tP - 0.15
    hop = math.sin(math.pi * clamp((t - tP + 0.15) / 0.35)) * (t > tP - 0.15)
    if leg:
        up = keyed(t, [(tP - 0.15, 0.0), (tP + 0.1, 1.0)], 0.25, 1.2)
        pts = death(cr, t, gx, gs, mood="shut", leg=True, y=G - 470 * gs - 40 * hop,
                    front=mix((-0.2, -0.4), UP["front"], up), backa=mix((0.1, -0.2), UP["backa"], up), ph=0.2,
                    hits=[(tP + 0.1, 0.3)])
        aura(cr, t, gx + 10, G - 780 * gs, 160, 520, 0.35 * prog(t, tP + 0.3, 0.8), n=18, spin=0.04)
    else:
        no = prog(t, tM, 0.2) * (1 - prog(t, tP - 0.4, 0.2))
        pts = death(cr, t, gx, gs, mood="sad", head=no * 0.14 * math.sin(t * 9), ph=0.2)
    foot = dev(cr, gx + 40 * gs, G - 6)
    dv_c = dev(cr, 870, 1080)
    n = 10 ** (9 * yrs ** 1.4)
    days = 0.25 * (0.5 + 0.5 * math.sin(cyc * math.pi * 2)) * clamp((t - tP) / 0.5) if t > tP else 0.0

    def ui(cr):
        if t < tA - 0.1:
            head2(cr, t, "TO SAY NO, SHE STOOD", t0 + 0.05, "ON ONE LEG", tP, big_size=260)
            if t > tP + 0.1:
                red_ring(cr, foot[0], foot[1] - 20, 110, 60, prog(t, tP + 0.2, 0.35), 8)
        else:
            head2(cr, t, "FOR", tA - 0.1, "BILLIONS OF YEARS!", tA + 0.05, big_size=200, under=tA + 0.8)
        if t > tP + 0.2:
            counter(cr, t, tP + 0.2, "YEARS", commas(max(1, n)), dv_c[0], dv_c[1], 0.5)
    return dict(ui=ui, flash=flash_at(t, tP, 0.2) + flash_at(t, tA, 0.2), night=days, lift=1.0)


# ------------------------------------------------------------------ mr13  he said no; the tears still in his palms


BR13 = (650, 1785, 0.74)
GL13 = (200, 0.5)


def s_no(cr, t, tl, t0, t1):
    c = cues(tl, "mr13")
    tN, tH, tA = c["N"], c["H"], c["A"]
    ground(cr)
    glow(cr, 560, 1300, 640, 0.4)
    gx, gs = GL13
    death(cr, t, gx, gs, mood="shut", leg=True, **UP, ph=0.2)
    bx, bg, bs = BR13
    shake = prog(t, tN - 0.1, 0.2) * (1 - prog(t, tN + 1.3, 0.3))
    bp = brahma(cr, t, bx, bg, bs, flip=True, cup=True, **CUP_ARMS, head=shake * 0.2 * math.sin(t * 11))
    cp = cup_point(cr, bp, bs, flip=True)
    pool(cr, t, cp, bs, 1.0)
    dv_c = dev(cr, *cp)
    dv_h = dev(cr, bx, bg - 1020 * bs)

    def ui(cr):
        if t < tH - 0.1:
            head2(cr, t, "BUT BRAHMA SAID", t0 + 0.05, "NO", tN, big_size=340)
            if t > tN + 0.1:
                big_x(cr, min(dv_h[0] + 330, 960), dv_h[1] + 200, 170, 140, prog(t, tN + 0.15, 0.3), alpha=0.9, lw=16)
        else:
            head2(cr, t, "HER TEARS WERE STILL", tH - 0.1, "IN HIS HANDS", tA, big_size=250)
            red_ring(cr, dv_c[0], dv_c[1] - 10, 130, 100, prog(t, tH + 0.1, 0.35), 8)
    return dict(ui=ui, flash=flash_at(t, tN, 0.2) + flash_at(t, tH, 0.15))


# ------------------------------------------------------------------ mr13q  QUESTION: what happened to the tears?


def s_question(cr, t, tl, t0, t1):
    c = cues(tl, "mr13q")
    tA, tQ = c["A"], c["Q"]
    ground(cr)
    glow(cr, 540, 1500, 600, 0.4)
    bp = brahma(cr, t, 420, G, 0.46, flip=True, cup=True, **CUP_ARMS)
    cp = cup_point(cr, bp, 0.46, flip=True)
    pool(cr, t, cp, 0.46, 1.0)
    death(cr, t, 760, 0.48, mood="sad", flip=True, ph=0.3)

    def ui(cr):
        head2(cr, t, "SO...", t0 + 0.05, None, 0.0)
        big_qmark(cr, t, t0 + 0.1, 540, 640, 330)
        card2(cr, t, tA - 0.2, 540, 1010, 1.0, [("WHAT HAPPENED TO", 74, INK, -50, tA),
                                                ("THE TEARS?", 104, RED, 40, tQ)])
    return dict(ui=ui, flash=flash_at(t, tA, 0.15) + flash_at(t, tQ, 0.2), night=0.08)


# ------------------------------------------------------------------ mr14  the twist: her tears become diseases


BR14 = (330, 1290, 0.6)
W14 = (640, 1580, 190)
N_DROPS = 5
LIE14 = (0, 2, 5, 9, 13)              # crowd places that lie down, asleep


def drop_path(i, cp, t, t_b):
    """Tear i: leaves his hands at t_b + 0.5 i, falls slowly, darkens into a little cloud and drifts down to the
    world. Returns (x, y, u) or None."""
    ts = t_b + 0.45 * i
    u = (t - ts) / 2.2
    if u <= 0:
        return None
    u = min(u, 1.0)
    tx = [470, 560, 650, 740, 820][i]
    x = cp[0] + (tx - cp[0]) * ease(u) + 20 * math.sin(t * 1.5 + i)
    y = cp[1] + 20 + (1310 - cp[1] - 20) * (u ** 1.3) - 40 * math.sin(math.pi * u)
    return x, y, u


def s_disease(cr, t, tl, t0, t1):
    c = cues(tl, "mr14")
    tS, tA, tB, tL, tM = c["S"], c["A"], c["B"], c["L"], c["M"]
    glow(cr, 640, 1580, 520, 0.3)
    glow(cr, 540, 1300, 640, 0.35)
    wx, wy, wr = W14
    wa = 0.55 + 0.45 * prog(t, tB - 0.3, 0.6)
    lie = LIE14 if t > tM else ()
    world(cr, t, wx, wy, wr, count=N_SLOTS, alpha=wa, lying=lie, souls=prog(t, tM + 0.2, 1.6))
    bx, bg, bs = BR14
    tilt = prog(t, tB - 0.2, 0.6)
    fr = mix(CUP_ARMS["front"], (-1.0, -0.9), tilt)
    ba = mix(CUP_ARMS["backa"], (-0.9, -1.0), tilt)
    bp = brahma(cr, t, bx, bg, bs, cup=True, front=fr, backa=ba, hits=[(tS, 0.2)])
    cp = cup_point(cr, bp, bs)
    left = 1.0 - prog(t, tB - 0.2, 0.45 * N_DROPS + 0.6)
    pool(cr, t, cp, bs, 0.3 + 0.7 * left)
    clouds = []
    for i in range(N_DROPS):
        p = drop_path(i, cp, t, tB - 0.2)
        if p is None:
            continue
        x, y, u = p
        dark = clamp((u - 0.18) / 0.3)
        tear(cr, x, y, 13 * (1 - dark), 1 - dark)
        if dark > 0.01:
            q = back(dark, 1.4)
            prop(cr, "mr_disease", x, y, 0.55 * q * (1 + 0.04 * math.sin(t * 3 + i)), rot=0.08 * math.sin(t + i),
                 alpha=clamp(dark * 1.5) * (1 - 0.6 * prog(t, tM + 0.8, 0.8)))
            clouds.append((x, y))
    dv_cp = dev(cr, *cp)
    dv_cl = [dev(cr, x, y) for x, y in clouds]

    def ui(cr):
        if t < tL - 0.1:
            head2(cr, t, "HE SAID: YOUR TEARS WILL BECOME", t0 + 0.05, "DISEASES", tB, big_size=250, under=tB + 0.6)
            if t < tB:
                red_ring(cr, dv_cp[0], dv_cp[1] - 10, 120, 90, prog(t, tA, 0.35), 8)
        else:
            head2(cr, t, "AND PEOPLE WOULD DIE OF", tL - 0.1, "DISEASES", tL + 0.05, big_size=250)
        if len(dv_cl) >= 2:
            k = min(len(dv_cl) - 1, 2)
            tag(cr, t, tB + 1.0, "DISEASES", dv_cl[k][0], dv_cl[k][1] - 110, 36, t_out=tM + 0.6)
    return dict(ui=ui, flash=flash_at(t, tB, 0.3) + flash_at(t, tM, 0.15), night=0.1 * prog(t, tB, 1.0))


# ------------------------------------------------------------------ mr15  only when it's time; no sin on her


HG15 = (230, 1180, 0.72)
GL15 = (720, 0.78)
OLD15 = (420, G + 4)


def hourglass(cr, t, x, y, s, run):
    """The hourglass, its sand falling from the top bulb to the bottom (run 0..1)."""
    prop(cr, "mr_hourglass", x, y, s)
    hh = MC.HG_H - 20
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.set_operator(cairo.OPERATOR_MULTIPLY)
    sand = (0.98, 0.70, 0.30)
    for upper, lvl in ((True, 1 - run), (False, run)):
        if lvl <= 0.005:
            continue
        cr.save()
        MC.hourglass_bulb(cr, upper, 8)
        cr.clip()
        if upper:
            top = -hh * lvl
            cr.rectangle(-120, top, 240, -top)
        else:
            cr.rectangle(-120, hh * (1 - lvl), 240, hh * lvl + 2)
        cr.set_source_rgb(*sand)
        cr.fill()
        cr.restore()
    if 0.0 < run < 1.0:
        cr.rectangle(-3, 0, 6, hh)
        cr.set_source_rgb(*sand)
        cr.fill()
    cr.restore()


def s_time(cr, t, tl, t0, t1):
    c = cues(tl, "mr15")
    tT, tJ, tP, tN = c["T"], c["J"], c["P"], c["N"]
    ground(cr)
    glow(cr, 540, 1300, 640, 0.35)
    hx, hy, hs = HG15
    run = clamp((t - t0 + 2.6) / max(0.5, tT - t0 + 2.7))
    hourglass(cr, t, hx, hy, hs, run)
    if t > tT - 0.1:
        sparkle(cr, hx, hy + MC.HG_H * hs, 40, prog(t, tT - 0.1, 0.2) * (1 - prog(t, tT + 0.6, 0.3)))
    ox, oy = OLD15
    prop(cr, "mr_p_lying", ox, oy, 2.3, alpha=1 - prog(t, tP, 0.6))
    gx, gs = GL15
    lead = prog(t, tJ, 0.6)
    walk = clamp((t - tJ - 0.3) / max(1.0, tP - tJ))
    # the old man's light rises, floats to her open hand, and she leads it gently away (a few steps)
    rise = prog(t, tT, 0.8)
    x_g = gx + 110 * ease(walk)
    pts = death(cr, t, x_g, gs, mood="gentle", flip=True, front=mix((-0.2, -0.4), (-1.05, -0.35), lead),
                hits=[(tJ, 0.3)], ph=0.4)
    hand = to_user(cr, pts["handF"])
    glow(cr, x_g, G - 500 * gs, 420, 0.5)
    warm(cr, x_g, G - 520 * gs, 380, 0.45 * prog(t, tP, 0.4), DEATH_GLOW)
    if rise > 0.01:
        sx, sy = ox, oy - 60 - 200 * ease(rise)
        sx, sy = sx + (hand[0] - 34 - sx) * ease(lead), sy + (hand[1] - 30 - sy) * ease(lead)
        soul(cr, t, sx, sy + 8 * math.sin(t * 2.5), 1.0, rise)
    sin_a = prog(t, tP - 0.1, 0.4) * (1 - prog(t, tN + 0.2, 0.5))
    u = clamp((t - tP + 0.1) / max(0.6, tN - tP + 0.1))
    smx = 300 + (x_g - 260 - 300) * ease(u)
    smy = 820 + (1060 - 820) * ease(u) + 30 * math.sin(t * 2)
    if sin_a > 0.01:                                    # a dark smudge of sin, breaking up on her light
        prop(cr, "mr_disease", smx, smy, 0.6 * (1 + 0.6 * prog(t, tN, 0.5)), alpha=sin_a, rot=0.1 * math.sin(t))
    if t > tN:
        burst(cr, t, smx, smy, tN, n=12, rmax=260, alpha=0.6)
    dv_sm = dev(cr, smx, smy)

    def ui(cr):
        if t < tP - 0.1:
            head2(cr, t, "JUST TAKE THEM", t0 + 0.05, "WHEN IT'S TIME", tT, big_size=250)
        else:
            head2(cr, t, "AND IT WON'T BE", tP - 0.1, "YOUR SIN", tP + 0.05, big_size=290)
            tag(cr, t, tP + 0.1, "SIN", dv_sm[0], dv_sm[1] - 100, 38, alpha=sin_a)
            if t > tN - 0.1:
                big_x(cr, dv_sm[0], dv_sm[1], 220, 170, prog(t, tN - 0.1, 0.3), alpha=0.9 * (1 - prog(t, tN + 1.0,
                                                                                                    0.4)), lw=16)
    return dict(ui=ui, flash=flash_at(t, tT, 0.15) + flash_at(t, tN, 0.2))


# ------------------------------------------------------------------ mr16  she agreed; death came to the world


W16 = (540, 1580, 250)


def s_agree(cr, t, tl, t0, t1):
    c = cues(tl, "mr16")
    tM, tD, tA = c["M"], c["D"], c["A"]
    if t < tD - 0.15:
        ground(cr)
        glow(cr, 540, 1300, 640, 0.4)
        brahma(cr, t, 250, G, 0.58, front=mix((-0.7, -1.7), BLESS, prog(t, tM + 0.3, 0.4)), hits=[(tM, 0.3)])
        nod = sum(math.sin(math.pi * clamp((t - tn) / 0.4)) for tn in (tM, tM + 0.5) if t > tn)
        death(cr, t, 720, 0.86, mood="bow", flip=True, head=0.08 + 0.18 * nod, **ANJALI, ph=0.3)
        dv = None
    else:
        rise = prog(t, tD - 0.15, 1.6)
        wx, wy, wr = W16
        sy = 1500 - 460 * ease(rise)
        glow(cr, wx + 190, sy, 900, 0.6 * rise)
        prop(cr, "sun", wx + 190, sy, 0.75, rot=t * 0.05, alpha=clamp(rise * 1.5))
        aura(cr, t, wx + 190, sy, 160, 700, 0.6 * rise, n=24, spin=0.05)
        lie = (2, 9) if t > tA else ()
        world(cr, t, wx, wy, wr, count=N_SLOTS, lying=lie, souls=prog(t, tA + 0.2, 1.4))
        u = ease(clamp((t - tD) / max(1.0, tA - tD + 0.4)))
        gx, gy = 170 + (290 - 170) * u, 1010 + (1190 - 1010) * u
        warm(cr, gx, gy - 200, 300, 0.7, DEATH_GLOW)
        glow(cr, gx, gy - 200, 380, 0.5)
        death(cr, t, gx, 0.42, mood="gentle", y=gy - 470 * 0.42, front=(-0.6, -0.5), ph=0.3, rods=False)
        dv = dev(cr, gx - 10, gy - 470)

    def ui(cr):
        if t < tD - 0.15:
            head2(cr, t, "AT LAST, THE GIRL", t0 + 0.05, "AGREED", tM, big_size=300)
        else:
            head2(cr, t, "AND DEATH CAME TO", tD - 0.15, "THE WORLD", tA, big_size=270)
            tag(cr, t, tD + 0.3, "DEATH", dv[0], dv[1], 36)
    return dict(ui=ui, flash=flash_at(t, tM, 0.15) + flash_at(t, tD - 0.15, 0.2) + flash_at(t, tA, 0.2))


# ------------------------------------------------------------------ mr16c  CALLBACK: the death we fear cried first


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "mr16c")
    tD, tP, tA = c["D"], c["P"], c["A"]
    fear_row(cr, t, 650, 1870, 1.2, 1.0, t0 - 1.0, n=5, spread=80, shrink=prog(t, tD, 0.8))
    mood = "cry" if t > tA - 0.1 else "sad"
    pts, eye = hook_girl(cr, t, mood, sob=[(tA, 0.35)], surge=tA)
    tg = dev(cr, eye[0] + 300, eye[1] - 40)

    def ui(cr):
        if t < tP - 0.1:
            head2(cr, t, "THE DEATH WE ALL", t0 + 0.05, "FEAR...", tD, big_size=300)
        else:
            head2(cr, t, "BEFORE TAKING THE FIRST LIFE,", tP - 0.1, "SHE CRIED", tA, big_size=280, under=tA + 0.5)
        tag(cr, t, t0 + 0.3, "DEATH", min(tg[0], 900), tg[1], 46)
    return dict(ui=ui, flash=flash_at(t, tD, 0.15) + flash_at(t, tA, 0.3))


# ------------------------------------------------------------------ mr17  punishment, or a need?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "mr17")
    tZ, tR, tC = c["Z"], c["R"], c["C"]
    ground(cr)
    glow(cr, 540, 1450, 600, 0.45)
    world(cr, t, 700, 1620, 150, count=N_SLOTS)
    death(cr, t, 330, 0.62, mood="gentle", ph=0.3)
    cards = ((300, "PUNISHMENT?", tZ - 0.1), (790, "NEED?", tR - 0.1))

    def ui(cr):
        head2(cr, t, "IS DEATH A PUNISHMENT,", t0 + 0.05, "OR A NEED?", tR, big_size=270)
        for cx, txt, tc in cards:
            card(cr, t, tc - 0.25, cx, 790, 0.6, [(txt, 104 if len(txt) > 6 else 140, RED, 4)])
        if t > tZ:
            if t < tR:
                k, ts = 0, tZ
            else:
                n = int((t - tR) / 0.9)
                k, ts = (1 + n) % 2, tR + 0.9 * n
            red_ring(cr, cards[k][0], 794, 236, 96, prog(t, ts, 0.35), 9)
    return dict(ui=ui, flash=flash_at(t, tZ, 0.15) + flash_at(t, tR, 0.15))


SHOTS = [   # (line, cue: None = line start, draw function, options)
    ("mr1", None, s_hook, {"z": (1.0, 1.04)}),
    ("mr2", None, s_book, {"z": (1.0, 1.03)}),
    ("mr3", None, s_create, {"z": (1.0, 1.03)}),
    ("mr4", None, s_crowd, {"z": (1.0, 1.04), "focus": (540, 1200)}),
    ("mr5", None, s_earth, {"z": (1.0, 1.03)}),
    ("mr6", None, s_fire, {"z": (1.0, 1.04)}),
    ("mr7", None, s_shiva, {"z": (1.0, 1.03)}),
    ("mr8", None, s_girl, {"z": (1.0, 1.03)}),
    ("mr9", None, s_name, {"z": (1.0, 1.03)}),
    ("mr10", None, s_weep, {"z": (1.0, 1.04)}),
    ("mr11", None, s_catch, {"z": (1.0, 1.03)}),
    ("mr12", None, s_oneleg, {"z": (1.0, 1.03)}),
    ("mr13", None, s_no, {"z": (1.0, 1.03)}),
    ("mr13q", None, s_question, {"z": (1.0, 1.03)}),
    ("mr14", None, s_disease, {"z": (1.0, 1.03)}),
    ("mr15", None, s_time, {"z": (1.0, 1.03)}),
    ("mr16", None, s_agree, {"z": (1.0, 1.03)}),
    ("mr16c", None, s_callback, {"z": (1.0, 1.04)}),
    ("mr17", None, s_end, {"z": (1.0, 1.03)}),
]


def _starts(tl):
    """Each shot's start (cached on the timeline under this module's own name, not shots.shot_at's)."""
    st = getattr(tl, "_mr_shot_starts", None)
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
        tl._mr_shot_starts = st
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
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook,
    shimmer as the girl steps out of Brahma's light, a conch as her tears become diseases (the twist), a hit as his
    anger becomes fire, a bell on the closing question, then (only where they fit) a conch on Shiva's "stop!", a damaru
    as the years race past. Chosen in THAT order of importance, each at least SFX_MIN_GAP from
    every sound already kept (as render_myth.calm_sfx keeps them), so the list returned is what plays (about six
    sounds); the bed dips before the reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["mr8"]["G"], "shimmer", 0), (c["mr14"]["B"], "conch", 0),
            (c["mr6"]["F"], "hit", 0), (c["mr17"]["Z"], "bell", 0), (c["mr7"]["R"], "conch", 0),
            (c["mr12"]["A"], "damaru", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["mr6"]["F"] - 0.3, "dip", 0.45), (c["mr8"]["G"] - 0.35, "dip", 0.5),
            (c["mr14"]["B"] - 0.35, "dip", 0.5)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
