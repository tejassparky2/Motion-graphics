"""Scenes for videos/ranchhod.py: "Krishna ran away from battle" (Bhagavata Purana 10.50-51; Vishnu Purana 5.23), in
Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code: the same lamp-lit screen, two-tier
headlines and rod-puppet motion as the Hanuman, Kumbhakarna and Jayadratha reels, with the cast from ranchhod_cast.
Built so a 5-year-old can follow it: every line has one shot that shows exactly what is said, in the order it is
said, with one big, short English headline per idea; the hard words (रण, रणछोड़) get a word card in Devanagari with
their plain meaning; the twist (the run was the plan) gets a slow reveal: the chase path drawn on a little map,
ending in a red ring at the cave.

Respect: Krishna calm and clever, never a coward cartoon; Muchukunda an old king with dignity; the gods as
silhouettes with halos. No gore at all: the kick is a silhouette and a flash; Kalayavana's end is his figure going
white in a white flash, then only a small heap of ash and grey flakes drifting away, never a burning body.

Every frame is a pure function of t. On-screen text is short English, except the word cards (रण, रणछोड़), shaped by
matplotlib with Nirmala.ttc as in scenes_arjuna (Latin letters without the font). Cues are words of the Hindi line
with a fraction fallback, in one table (CUES) that the scenes and sfx() both read, with minimum gaps so a fast voice
can't bunch the beats together. Shot starts and cues are cached on the timeline under this module's own names
(_rc_shot_starts, _rc_cues). Hindi only: the Kannada reel is drawn by scenes_ranchhod_yk.

Shot list (line: what is on the screen)
  rc1   HOOK, frame 0: Krishna alone and large, RUNNING (knee up, arms pumping), looking back over his shoulder:
        LORD KRISHNA / RAN AWAY! (big word in by 0.3 s); on "yuddh" the battle he leaves shows small behind him
        (soldiers in a dust cloud, plate THE BATTLE); on "bhaag" dust bursts at his feet, speed lines, the big word
        is underlined; on "naam" a leather plaque drops in and on "Ranchhod" the name appears on it in Devanagari:
        SO ONE OF HIS NAMES IS / RANCHHOD
  rc2   word cards: [रण = BATTLE] (crossed swords on a shield): THIS WORD MEANS / BATTLE; an arrow down to [रणछोड़],
        under it the picture: little Krishna running away from the crossed swords: AND RANCHHOD MEANS / RAN FROM
        BATTLE; then a palm-leaf book rises: BHAGAVATA PURANA, A TRUE STORY (ringed): A TRUE STORY FROM THE /
        BHAGAVATA PURANA
  rc3   Kalayavana comes onto the cloth, huge, sword up (tag KALAYAVANA): KALAYAVANA, / A CRUEL KING; three rows of
        soldiers march in behind him: WITH MILLIONS OF / SOLDIERS; Mathura's gate rises at the right (tag MATHURA):
        HE ATTACKED KRISHNA'S / CITY!
  rc4   the gate, close: its doors swing open, Krishna steps out alone; he shows his empty hands, a sword crossed out
        by them: KRISHNA CAME OUT WITH / NO WEAPON; the whole army far away on the left: NO WEAPON, / ALONE!
  rc5   Kalayavana, sword in hand, laughs; a thought bubble shows little Krishna with empty hands: KALAYAVANA
        LAUGHED: / ALONE?, then ALONE, AND / NO WEAPON?; he throws his sword down (it clatters on the ground) and
        reaches out with both hands: 'I'LL CATCH HIM / BY HAND!'
  rc6   Kalayavana lunges at Krishna, hands out: KALAYAVANA CAME / CLOSER...; Krishna turns his back and runs off
        to the right in a puff of dust, the hands grab air: AND KRISHNA / RAN!
  rc7   Kalayavana shouts, a fist up, sound rings from his mouth; small Krishna far ahead, running: HE SHOUTED: /
        COWARD!; a cloud WHERE ARE YOU / RUNNING?; then he runs after him: AND HE / CHASED HIM!
  rc8   the chase over the hills (the hills slide past): Kalayavana's hand always a little behind Krishna's back,
        the gap ringed (SO CLOSE!): KRISHNA KEPT RUNNING, / JUST OUT OF REACH; a hill with a cave slides in and
        Krishna runs into its dark mouth: INTO A / DARK CAVE
  rc8q  the QUESTION card: a big red "?" over WAS KRISHNA / SCARED?; Krishna small and waiting in the cave mouth
  rc9   inside the cave (rock walls, stalactites): an old king asleep on a stone bed (his head on the stone pillow
        at the right, as in all the cave shots), z's rising, cobwebs growing:
        IN THAT CAVE, FOR / MANY YEARS..., A KING WAS / ASLEEP; tag MUCHUKUNDA: HIS NAME WAS / MUCHUKUNDA
  rc10  FLASHBACK (sepia): Muchukunda with a sword guards the gods (silhouettes with halos) from demons (dark
        silhouettes) while suns and moons race by: HE FOUGHT FOR / THE GODS, FOR YEARS!; the demons are gone, light
        streams from the gods into him: THE GODS GAVE HIM A / GIFT; he closes his eyes and lies down, z's:
        THE GODS' GIFT: / SLEEP!
  rc11  the rule as a three-step strip (shut eye shaking: WAKE HIM UP -> the eye opens, glowing: ONE LOOK -> a little
        dark figure flashes white and is a heap of ash: ASH!): WHOEVER WAKES HIM UP... / TURNS TO ASH!
  rc12  the dark cave: Kalayavana walks in; the sleeper is a dark shape on the bed: KALAYAVANA CAME IN AND SAW / A
        SLEEPING MAN; a thought bubble: Krishna lying with his eyes shut, smiling: HE THOUGHT: / 'THAT'S KRISHNA!',
        then 'HE'S ONLY / PRETENDING!' (in the bubble he peeks with one eye, ringed)
  rc13  in silhouette: Kalayavana pulls his leg back (WITH ALL HIS / STRENGTH...) and kicks the sleeper's legs: a flash,
        KICK!: HE KICKED THE / SLEEPING KING!
  rc14  the twist, slowly: the king stirs and sits up, facing Kalayavana: THE KING / WOKE UP; his eyes open,
        glowing, light pours from them: HE OPENED HIS / ANGRY EYES...; Kalayavana (shocked) goes white, a white
        flash, and only a heap of ash is left, grey flakes drifting away: AND KALAYAVANA BECAME / ASHES!
  rc15  outside, Krishna calm and smiling at the cave mouth, ash drifting out of it: KRISHNA WAS / NOT SCARED!; a
        little map above: Mathura's gate, the hills, and the chase drawn as a dotted red path that ends in a red ring
        at this cave: HE LED THE ENEMY / RIGHT HERE!
  rc15c CALLBACK to the hook: the same running Krishna, looking back, now smiling: THE ONE THEY CALLED A / 'COWARD'...;
        the Ranchhod plaque drops in again; golden light: WON THE FIGHT / WITHOUT A WEAPON!
  rc16  WHY DID / KRISHNA RUN?; cards FEAR? / BRAINS?, a red ring alternating; Krishna small and calm below, turning
        to the ringed card
"""
import math

import cairo

import puppet_core as pc
import ranchhod_cast as RC
from channel import SFX_KEEP, SFX_MIN_GAP
from poster import HEAD_FONT, back, clamp, draw_text, ease, prog
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_arjuna import HAS_INDIC, card2, cloud_text, down_arrow
from scenes_hanuman_curse import qmark, word_plaque
from scenes_jarasandha import FEET, INK, RED, glow, man_angles, motes, red_ring, sound_rings
from scenes_jayadratha import NIGHT, flash_at, silhouette, tag, tint, title_lift, to_user
from scenes_kaikeyi import card, fig
from scenes_lakshman_rekha import big_x, book, sparkle
from scenes_mandhata import aura, burst, held, local, mix, reach_arm, warm, zzz
from scenes_ravana import dotted, head2
from scenes_ruru import flow, plate, sepia
from scenes_shani_ganesha import deva
from shots import CUT_LEAD, MIN_SHOT, T

MISSES = set()                       # Hindi cue words not found in their line (falls back to fractions)
G = FEET + 120                       # the ground line of the open-air sets
CG = 960 + RC.CAVE_FLOOR             # the floor inside the cave
RAN_W, RANCH_W = "रण", "रणछोड़"        # the spoken words on the cards
RAN_L, RANCH_L = "RAN", "RANCHHOD"   # Latin fallbacks (no Nirmala font)
DUST_C = (0.94, 0.84, 0.64)
ASH_C = (0.62, 0.60, 0.60)


def cue(tl, bid, word, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, word)
    except (KeyError, ValueError):
        if getattr(tl, "lang", "hi") == "hi":
            MISSES.add((bid, word))
        return T(tl, bid, frac)


# Every cue of every line: (name, Hindi word, fraction fallback, ((after, min gap), ...)); "t0" = the line's start.
# Words are exact substrings of the Hindi lines (checked: MISSES stays empty).
CUES = {
    "rc1": (("Y", "युद्ध", 0.3, (("t0", 0.9),)),
            ("R", "भाग", 0.45, (("Y", 0.5),)),
            ("N", "नाम", 0.75, (("R", 1.0),)),
            ("C", "रणछोड़", 0.88, (("N", 0.4),))),
    "rc2": (("A", "रण", 0.02, (("t0", 0.1),)),
            ("Y", "युद्ध", 0.15, (("A", 0.5),)),
            ("B", "रणछोड़", 0.3, (("Y", 0.6),)),
            ("M", "भागने", 0.55, (("B", 0.6),)),
            ("P", "भागवत", 0.75, (("M", 0.9),)),
            ("T", "सच्ची", 0.88, (("P", 0.4),))),
    "rc3": (("K", "कालयवन", 0.12, (("t0", 0.3),)),
            ("Z", "ज़ालिम", 0.3, (("K", 0.6),)),
            ("S", "करोड़ों", 0.5, (("Z", 0.8),)),
            ("N", "नगरी", 0.82, (("S", 1.0),)),
            ("A", "चढ़", 0.9, (("N", 0.3),))),
    "rc4": (("W", "हथियार", 0.35, (("t0", 0.9),)),
            ("A", "अकेले", 0.65, (("W", 0.7),)),
            ("O", "निकले", 0.88, (("A", 0.5),))),
    "rc5": (("S", "सोचा", 0.15, (("t0", 0.4),)),
            ("L", "अकेला", 0.25, (("S", 0.3),)),
            ("W", "हथियार", 0.45, (("L", 0.6),)),
            ("H", "हाथों", 0.75, (("W", 0.9),)),
            ("P", "पकड़", 0.85, (("H", 0.3),))),
    "rc6": (("P", "पास", 0.25, (("t0", 0.5),)),
            ("K", "कृष्ण", 0.55, (("P", 0.5),)),
            ("B", "पीठ", 0.68, (("K", 0.2),)),
            ("R", "भाग", 0.85, (("B", 0.4),))),
    "rc7": (("C", "चिल्लाया", 0.15, (("t0", 0.3),)),
            ("D", "डरपोक", 0.3, (("C", 0.4),)),
            ("W", "कहाँ", 0.55, (("D", 0.6),)),
            ("F", "दौड़ा", 0.88, (("W", 0.8),))),
    "rc8": (("D", "दौड़ते", 0.1, (("t0", 0.2),)),
            ("P", "पकड़", 0.35, (("D", 0.6),)),
            ("G", "गुफा", 0.78, (("P", 1.2),)),
            ("E", "घुस", 0.88, (("G", 0.4),))),
    "rc8q": (("Q", "क्या", 0.1, (("t0", 0.15),)),
             ("D", "डर", 0.7, (("Q", 0.7),))),
    "rc9": (("C", "गुफा", 0.08, (("t0", 0.15),)),
            ("Y", "सालों", 0.25, (("C", 0.4),)),
            ("K", "राजा", 0.45, (("Y", 0.7),)),
            ("S", "सो", 0.55, (("K", 0.3),)),
            ("M", "मुचुकुंद", 0.85, (("S", 0.9),))),
    "rc10": (("D", "देवताओं", 0.08, (("t0", 0.2),)),
             ("F", "लड़ाई", 0.3, (("D", 0.8),)),
             ("B", "वरदान", 0.68, (("F", 1.5),)),
             ("S", "सो", 0.88, (("B", 0.8),))),
    "rc11": (("W", "जगाएगा", 0.25, (("t0", 0.5),)),
             ("E", "नज़र", 0.55, (("W", 0.8),)),
             ("A", "राख", 0.85, (("E", 0.8),))),
    "rc12": (("C", "गुफा", 0.1, (("t0", 0.2),)),
             ("S", "देखा", 0.42, (("C", 0.8),)),
             ("T", "सोचा", 0.55, (("S", 0.5),)),
             ("K", "कृष्ण", 0.65, (("T", 0.3),)),
             ("N", "नाटक", 0.85, (("K", 0.7),))),
    "rc13": (("P", "ताक़त", 0.2, (("t0", 0.3),)),
             ("R", "राजा", 0.55, (("P", 0.6),)),
             ("L", "लात", 0.85, (("R", 0.5),))),
    "rc14": (("W", "नींद", 0.12, (("t0", 0.2),)),
             ("O", "खोलीं", 0.45, (("W", 1.2),)),
             ("K", "कालयवन", 0.62, (("O", 0.6),)),
             ("X", "राख", 0.88, (("K", 0.7),))),
    "rc15": (("N", "नहीं", 0.25, (("t0", 0.4),)),
             ("E", "दुश्मन", 0.5, (("N", 0.7),)),
             ("M", "मौत", 0.75, (("E", 0.8),))),
    "rc15c": (("D", "डरपोक", 0.2, (("t0", 0.3),)),
              ("R", "रणछोड़", 0.42, (("D", 0.6),)),
              ("W", "हथियार", 0.6, (("R", 0.6),)),
              ("J", "जीत", 0.88, (("W", 0.6),))),
    "rc16": (("Q", "भागना", 0.2, (("t0", 0.3),)),
             ("F", "डर", 0.35, (("Q", 0.4),)),
             ("B", "दिमाग़", 0.6, (("F", 0.7),)),
             ("C", "कमेंट", 0.85, (("B", 0.5),))),
}


def cues(tl, bid):
    """{name: time} for a line (cached on the timeline under this module's own name)."""
    cache = getattr(tl, "_rc_cues", None)
    if cache is None:
        cache = {}
        tl._rc_cues = cache
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


def puff(cr, x, y, r, a, col=DUST_C):
    """A soft round puff (dust, ash smoke)."""
    if a <= 0.01 or r <= 1:
        return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, *col, 0.55 * a)
    g.add_color_stop_rgba(0.6, *col, 0.30 * a)
    g.add_color_stop_rgba(1, *col, 0.0)
    cr.save()
    cr.set_source(g)
    cr.arc(x, y, r, 0, 2 * math.pi)
    cr.fill()
    cr.restore()


def dust(cr, t, t0, t1, pos, rate=0.13, life=0.9, drift=-160.0, size=1.0, alpha=1.0):
    """Dust kicked up behind a runner: a puff every `rate` s between t0 and t1 at pos(ts) (scene xy), drifting
    back (drift px/s) and up, growing and fading."""
    if t < t0 or alpha <= 0.01:
        return
    k1 = int((min(t, t1) - t0) / rate)
    for k in range(max(0, k1 - int(life / rate) - 1), k1 + 1):
        ts = t0 + k * rate
        u = (t - ts) / life
        if not 0 <= u < 1:
            continue
        x, y = pos(ts)
        sg = 1 if k % 2 else -1
        puff(cr, x + drift * (t - ts) + sg * 10, y - 70 * u * size - 10, (30 + 70 * u) * size,
             alpha * (1 - u) * min(1.0, u * 6))


def speed_lines(cr, t, x, y, h, a, n=6):
    """Streaks of motion behind a runner (to the left of x), flickering."""
    if a <= 0.01:
        return
    cr.save()
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(n):
        yy = y - h / 2 + h * (i + 0.5) / n
        ph = (t * 2.3 + i * 0.37) % 1.0
        L = 110 + 70 * ((i * 7) % 3)
        x1 = x - 10 - 70 * ph - 30 * (i % 2)
        cr.move_to(x1, yy)
        cr.line_to(x1 - L, yy)
        cr.set_source_rgba(*INK, 0.75 * a * math.sin(math.pi * ph))
        cr.set_line_width(7)
        cr.stroke()
    cr.restore()


def ash_flakes(cr, t, t0, x, y, n=26, spread=120.0, rise=520.0, drift=160.0, dur=2.6, alpha=1.0):
    """Grey flakes of ash lifting from (x, y) from t0 and drifting away on the air, fading."""
    if t < t0 or alpha <= 0.01:
        return
    cr.save()
    for i in range(n):
        ts = t0 + 0.04 * i
        u = (t - ts) / dur
        if not 0 < u < 1:
            continue
        px = x + spread * math.sin(i * 2.39) + drift * u + 26 * math.sin(t * 2.2 + i)
        py = y - 30 * (i % 3) - rise * (1 - (1 - u) ** 2)
        r = 4 + (i % 4) * 2.2
        cr.save()
        cr.translate(px, py)
        cr.rotate(t * 2 + i)
        cr.scale(1.0, 0.55)
        cr.arc(0, 0, r, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(*(ASH_C if i % 3 else (0.40, 0.38, 0.38)), 0.85 * alpha * (1 - u) * min(1.0, u * 8))
        cr.fill()
    cr.restore()


def white_out(cr, fn, a):
    """Whatever fn(cr) draws, lit white (a figure caught in the blinding light)."""
    if a <= 0.01:
        return None
    return silhouette(cr, fn, a, (1.0, 0.98, 0.92))


def ash_heap(cr, x, y, s, alpha=1.0):
    """The heap of ash, painted over (not multiplied), so its pale grey shows on the dark cave floor too."""
    if s <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    pc.paint_part(cr, "rc_ash", alpha, op=cairo.OPERATOR_OVER)
    cr.restore()


def door(cr, x, y, gs, open_, flip=False, alpha=1.0):
    """One gate door on its hinge at (x, y): open_ 0 = shut, 1 = swung right back (seen edge-on, narrow)."""
    k = max(0.08, 1 - 0.9 * ease(open_))
    cr.save()
    cr.translate(x, y)
    cr.scale((-gs if flip else gs) * k, gs)
    pc.paint_part(cr, "rc_door", alpha)
    cr.restore()


def army_row(cr, t, y, s, t_march, speed=60.0, alpha=1.0, blur=0.0, x0=0.0, rise=1.0, step=0.5):
    """A row of marching soldiers (rc_army pieces end to end) across the screen, moving right, bobbing in step;
    rise 0..1 brings it up from below the screen."""
    if alpha <= 0.01 or rise <= 0.0:
        return
    wid = 1320 * s
    m = x0 + speed * max(0.0, t - t_march)
    bob = 8 * s / 0.5 * abs(math.sin(math.pi * t / step))
    yy = y + (H + 40 - (y - 900 * s)) * (1 - ease(rise)) - bob
    for k in range(-2, 3):
        x = W / 2 + ((m % wid) + k * wid)
        if -wid < x < W + wid:
            prop(cr, "rc_army", x, yy, s, alpha=alpha, blur=blur)


# ------------------------------------------------------------------ puppets


KR_HEAD = {"calm": "krishna_head", "smile": "rc_kr_head_smile", "back": "rc_kr_head_back",
           "back_smile": "rc_kr_head_back_smile", "sleep": "rc_kr_head_sleep"}
KL_HEAD = {m: "rc_kala_head" + ("" if m == "fierce" else "_" + m) for m in RC.KL_MOODS}
MK_HEAD = {m: "rc_mk_head" + ("" if m == "calm" else "_" + m) for m in RC.MK_MOODS}
OPEN = dict(front=(-1.25, -0.55), backa=(-1.05, -0.75))          # both hands held out, palms open
RUN_P = 0.30                                                     # a running stride (s)


def krishna(cr, t, x, s, mood="calm", **kw):
    """Krishna standing (feet on `feet`, default G)."""
    kw.setdefault("feet", G)
    return fig(cr, RC.KRISHNA, "krishna", t, x, s, swap={"krishna_head": KR_HEAD[mood]}, **kw)


def runner(cr, t, rig, key, head, x, ground_, s, flip=False, alpha=1.0, blur=0.0, rods=True, ph=0.0, P=RUN_P,
           front=None, backa=None, lean=0.16, hits=(), extra=None):
    """A figure RUNNING (feet on ground_): bent running legs swapped in, alternating each stride, the body bobbing and
    leaning forward, the near arm pumping in front and the far arm swinging back. Returns its points (device)."""
    q = (t + ph) / P
    v, u = int(math.floor(q)) % 2, q - math.floor(q)
    hy = ground_ - RC.HIP_RUN * s - 26 * s * math.sin(math.pi * u)
    sw_ = 0.22 * math.sin(math.pi * u) * (1 if v else -1)
    fr = front or (-0.95 + sw_, -1.25)
    ba = backa or (0.85 - sw_, -1.15)
    ang = man_angles(key, t, fr, ba, -0.04, (0.0, 0.0), hits, ph)
    la = 0.16 * (u - 0.5)
    sw = {key + "_head": head}
    if v == 0:
        sw[key + "_legF"], sw[key + "_legB"] = key_leg(key, "fwd"), key_leg(key, "back")
        ang[key + "_legF"], ang[key + "_legB"] = -la, la
    else:
        sw[key + "_legF"], sw[key + "_legB"] = key_leg(key, "back"), key_leg(key, "fwd")
        ang[key + "_legF"], ang[key + "_legB"] = la, -la
    return puppet(cr, rig, x, hy, s, lean + 0.025 * math.sin(2 * math.pi * u), flip, ang, alpha, blur, swap=sw,
                  rods=rods, extra=extra)


def key_leg(key, mode):
    return ("rc_kr_leg_" if key == "krishna" else "rc_kala_leg_") + mode


def kr_run(cr, t, x, ground_, s, mood="back", **kw):
    return runner(cr, t, RC.KRISHNA, "krishna", KR_HEAD[mood], x, ground_, s, **kw)


def kala(cr, t, x, s, mood="fierce", sword=False, tilt=0.0, **kw):
    """Kalayavana standing (feet on `feet`, default G); sword = his sword upright in his front hand."""
    kw.setdefault("feet", G)
    if sword:
        fr = kw.get("front", (-0.32, -0.55))
        kw["extra"] = {"rc_kala_armF_lo": held("rc_sword", fr, 0.78, dy=150, tilt=tilt, alpha=kw.get("alpha", 1.0),
                                               blur=kw.get("blur", 0.0))}
    return fig(cr, RC.KALA, "rc_kala", t, x, s, swap={"rc_kala_head": KL_HEAD[mood]}, **kw)


def kala_run(cr, t, x, ground_, s, mood="shout", **kw):
    return runner(cr, t, RC.KALA, "rc_kala", KL_HEAD[mood], x, ground_, s, **kw)


def mk(cr, t, x, s, mood="calm", sword=False, **kw):
    """Muchukunda standing (feet on `feet`, default G); sword = a talwar raised in his front hand."""
    kw.setdefault("feet", G)
    if sword:
        fr = kw.get("front", (-0.32, -0.55))
        kw["extra"] = {"rc_mk_armF_lo": held("ar_sword", fr, 0.72, dy=150, tilt=0.15, alpha=kw.get("alpha", 1.0),
                                             blur=kw.get("blur", 0.0))}
    return fig(cr, RC.MUCHU, "rc_mk", t, x, s, swap={"rc_mk_head": MK_HEAD[mood]}, **kw)


def mk_lying(cr, t, x, top, s, mood="sleep", sit=0.0, alpha=1.0, blur=0.0, rods=True, bump=0.0, shake=0.0):
    """Muchukunda asleep on his back on a surface at height `top` (head to the left), breathing slowly; sit 0..1
    raises him to sitting (the legs stay along the bed). Returns his points (device)."""
    br = math.sin(t * 1.3)
    q = ease(clamp(sit))
    rot = -math.pi / 2 + (math.pi / 2 - 0.22) * q + 0.01 * br * (1 - q) + shake * 0.03 * math.sin(t * 31)
    hy = top - (66 + 3 * br * (1 - q)) * s + (26 * s) * q - bump
    la = -math.pi / 2 - rot
    front = mix((0.3, -0.25), (-0.5, -0.6), q)
    ang = man_angles("rc_mk", t, front, (0.25, -0.15), 0.04 * (1 - q), (0.0, 0.0), (), 0.3)
    ang["rc_mk_legF"] = la - 0.06 * (1 - q)
    ang["rc_mk_legB"] = la + 0.02
    return puppet(cr, RC.MUCHU, x, hy, s, rot, False, ang, alpha, blur, swap={"rc_mk_head": MK_HEAD[mood]},
                  rods=rods)


def bed_top(bx, bs, floor=CG):
    return floor - RC.BED_H * bs


def sleeper(cr, t, bx, bs, hip, s, mood="sleep", sit=0.0, bump=0.0, shake=0.0, dark=0.0, rods=True):
    """The stone bed and the old king on it, his head on the stone pillow at the RIGHT (the bed and king are drawn
    mirrored about the bed's middle, so his feet point left and, sitting up, he faces left); hip = his hip's x on the
    screen; dark = a dark shadow over him (in the dark cave). Anything below the bed top (his hair, the dhoti pleats
    when he sits) is hidden by the bed. Returns his points (device)."""
    cr.save()
    cr.translate(2 * bx, 0)
    cr.scale(-1, 1)
    prop(cr, "rc_bed", bx, CG, bs)
    top = bed_top(bx, bs)
    cr.rectangle(-600, -600, W + 1200, top + 8 + 600)
    cr.clip()
    hx = 2 * bx - hip
    pts = mk_lying(cr, t, hx, top, s, mood, sit=sit, bump=bump, shake=shake, rods=rods)
    if dark > 0.01:
        silhouette(cr, lambda cr_: mk_lying(cr_, t, hx, top, s, mood, sit=sit, bump=bump, shake=shake, rods=False),
                   dark)
    cr.restore()
    return pts


# ------------------------------------------------------------------ rc1  hook


HK = (460, 1.1, 1890)                # Krishna in the hook: x, scale, ground
PLQ = (800, 650, 0.6)                # the name plaque: x, y, scale


def battle_far(cr, t, a, x=150, y=1700):
    """The battle he leaves, small and far behind him: soldiers in a dust cloud."""
    if a <= 0.01:
        return
    for i, (dx, r) in enumerate(((-60, 150), (60, 170), (170, 120), (-150, 120))):
        puff(cr, x + dx + 12 * math.sin(t * 1.3 + i), y - 120 - 30 * (i % 2), r, 0.9 * a)
    for i, (dx, dy, s) in enumerate(((-40, -30, 0.24), (40, 0, 0.3))):
        prop(cr, "rc_army", x + dx, y + dy - 6 * abs(math.sin(t * 6 + i)), s, alpha=0.8 * a, blur=3.0 - i)


def name_plaque(cr, t, t_in, t_word, x=PLQ[0], y=PLQ[1], s=PLQ[2], ring_t=None):
    """The leather plaque with Krishna's name रणछोड़ (the word appears when it is spoken)."""
    kind, w = ("indic", RANCH_W) if HAS_INDIC else ("latin", RANCH_L)
    word_plaque(cr, t, t_in, x, y, s, [(kind, w, 175, RED, t_word)])
    if ring_t is not None and t > ring_t:
        red_ring(cr, x, y - 4, 270 * s / 0.6, 92 * s / 0.6, prog(t, ring_t, 0.35), 8)


def s_hook(cr, t, tl, t0, t1):
    c = cues(tl, "rc1")
    tY, tR, tN, tC = c["Y"], c["R"], c["N"], c["C"]
    x, s, gnd = HK
    battle_far(cr, t, prog(t, tY - 0.1, 0.4))
    glow(cr, x + 40, gnd - 700 * s, 640, 0.35)
    ground(cr, gnd - 4)
    dust(cr, t, -0.6, 99.0, lambda ts: (x - 170 * s, gnd - 20), 0.12, 0.9, -220, 1.0 + 0.5 * prog(t, tR, 0.3))
    if t > tR:
        q = math.exp(-2.0 * (t - tR))
        for k in range(5):
            puff(cr, x - 60 - 70 * k * (1 - q * 0.3), gnd - 40 - 30 * (k % 2), 90 + 30 * k, 0.9 * q)
    speed_lines(cr, t, x - 120 * s, gnd - 650 * s, 480 * s, 0.4 + 0.5 * prog(t, tR, 0.3))
    kr_run(cr, t, x, gnd, s, "back", hits=[(tR, 0.3)], ph=0.15)

    def ui(cr):
        if t < tN - 0.1:
            head2(cr, t, "LORD KRISHNA", -1.0, "RAN AWAY!", 0.3, big_size=270, ghost=-1.0, under=tR)
        else:
            head2(cr, t, "SO ONE OF HIS NAMES IS", tN - 0.1, "RANCHHOD", tC, big_size=250)
        if t > tY - 0.1 and t < tN:
            plate(cr, t, tY, "THE BATTLE", 150, 1390, 34)
        name_plaque(cr, t, tN - 0.2, tC, ring_t=tC + 0.35)
    return dict(ui=ui, flash=flash_at(t, 0.3, 0.2) + flash_at(t, tR, 0.3) + flash_at(t, tC, 0.25))


# ------------------------------------------------------------------ rc2  the word cards


CA = (540, 700, 0.72)                # card रण = BATTLE
CB = (540, 1010, 0.72)               # card रणछोड़


def s_words(cr, t, tl, t0, t1):
    c = cues(tl, "rc2")
    tA, tY, tB, tM, tP, tT = c["A"], c["Y"], c["B"], c["M"], c["P"], c["T"]
    glow(cr, 540, 1350, 600, 0.35)
    pic = prog(t, tM - 0.1, 0.4) * (1 - prog(t, tP - 0.1, 0.35))
    if pic > 0.01:                                       # the meaning, drawn: running away from the battle
        bx, by = 260, 1460
        prop(cr, "rc_battle", bx, by, 0.7, rot=sway(t, 0.02, 0.5), alpha=pic)
        u = clamp((t - tM) / 1.6)
        rx = 470 + 380 * ease(u)
        dotted(cr, [(bx + 120, by + 40), (rx - 60, by + 60)], 1.0, 26, 6, RED, 0.8 * pic * clamp(u * 4))
        kr_run(cr, t, rx, by + 230, 0.36, "back", alpha=pic, rods=False)
        dust(cr, t, tM, 99.0, lambda ts: (470 + 380 * ease(clamp((ts - tM) / 1.6)) - 60, by + 220), 0.14, 0.8,
             -120, 0.5, pic)
    if t > tP - 0.2:                                     # a true story from the Bhagavata Purana
        leaves = [(None, [("BHAGAVATA PURANA", 76, HEAD_FONT)], 0),
                  (tT, [([("A TRUE STORY", RED)], 84, HEAD_FONT)], 0)]
        book(cr, t, 540, 1360, 0.72, leaves, t_in=tP - 0.15, t_open=tP + 0.3, ring=(1, 0, 0, tT + 0.35))

    def ui(cr):
        if t < tB - 0.1:
            head2(cr, t, "THIS WORD MEANS", t0 + 0.05, "BATTLE", tY, big_size=280)
        elif t < tP - 0.1:
            head2(cr, t, "AND RANCHHOD MEANS", tB - 0.1, "RAN FROM BATTLE", tM, big_size=200)
        else:
            head2(cr, t, "A TRUE STORY FROM THE", tP - 0.1, "BHAGAVATA PURANA", tP + 0.05, big_size=200)
        kind = "indic" if HAS_INDIC else "latin"
        ax, ay, a_s = CA
        word_plaque(cr, t, tA - 0.3, ax, ay, a_s, [(kind, RAN_W if HAS_INDIC else RAN_L, 160, RED, tA),
                                                   ("latin", "=", 110, INK, tY - 0.1),
                                                   ("latin", "BATTLE", 110, INK, tY)])
        if t > tB - 0.3:
            down_arrow(cr, ax, ay + 100, CB[1] - 100, prog(t, tB - 0.3, 0.3))
        bx, by, b_s = CB
        word_plaque(cr, t, tB - 0.2, bx, by, b_s, [(kind, RANCH_W if HAS_INDIC else RANCH_L, 170, RED, tB)])
        if pic > 0.01:
            plate(cr, t, tM + 0.1, "BATTLE", 260, 1650, 32, alpha=pic)
    return dict(ui=ui, flash=flash_at(t, tY, 0.2) + flash_at(t, tM, 0.2) + flash_at(t, tP, 0.2))


# ------------------------------------------------------------------ rc3  a cruel king, millions of soldiers, the city


KL3 = (290, 0.78)                    # Kalayavana: x, scale
GATE3 = (870, 1560, 0.5)             # the far gate: x, ground, scale


def s_attack(cr, t, tl, t0, t1):
    c = cues(tl, "rc3")
    tK, tZ, tS, tN = c["K"], c["Z"], c["S"], c["N"]
    glow(cr, 540, 1300, 640, 0.35)
    if t > tN - 0.3:                                     # Mathura's gate, far off at the right
        b, k, a = depth(t, tN - 0.3, 0.5)
        gx, gg, gs = GATE3
        glow(cr, gx, gg - 300, 360, 0.4 * a)
        prop(cr, "rc_gate", gx, gg, gs * k, alpha=a, blur=b + 1.5)
    ground(cr, alpha=0.9)
    for i, (y, s, bl, sp) in enumerate(((1640, 0.30, 4.0, 40.0), (1760, 0.40, 2.0, 50.0))):
        r = prog(t, tS - 0.15 + 0.15 * i, 0.5)
        army_row(cr, t, y, s, tS, sp, alpha=0.85, blur=bl, x0=-300 + 160 * i, rise=r)
    x, s = KL3
    b, k, a = depth(t, t0 - 0.25, 0.5)
    up = keyed(t, [(t0, 0.0), (tZ, 1.0)], 0.3, 1.4)
    fr = mix((-0.6, -0.7), (-2.3, -0.35), up)
    pts = kala(cr, t, x, s * k, mood="fierce" if t < tZ else "shout", sword=True, tilt=0.45 * up, front=fr,
               backa=(0.4, -0.6), head=-0.05 * up, hits=[(tZ, 0.5)], alpha=a, blur=b, ph=0.4)
    r = prog(t, tS - 0.05, 0.5)
    army_row(cr, t, 2060, 0.55, tS, 70.0, alpha=0.95, blur=0.0, x0=200, rise=r)
    top = to_user(cr, pts["top"])

    def ui(cr):
        if t < tS - 0.1:
            head2(cr, t, "KALAYAVANA,", t0 + 0.05, "A CRUEL KING", tZ, big_size=240)
        elif t < tN - 0.1:
            head2(cr, t, "WITH MILLIONS OF", tS - 0.1, "SOLDIERS", tS + 0.05, big_size=280)
        else:
            head2(cr, t, "HE ATTACKED KRISHNA'S", tN - 0.1, "CITY!", tN + 0.05, big_size=300)
        tag(cr, t, tK, "KALAYAVANA", max(250, min(top[0], 830)), top[1] - 40, 40, t_out=tS)
        if t > tN:
            tag(cr, t, tN + 0.15, "MATHURA", GATE3[0], GATE3[1] - 680 * GATE3[2] - 40, 36)
    return dict(ui=ui, flash=flash_at(t, tK, 0.2) + flash_at(t, tZ, 0.2) + flash_at(t, tS, 0.25) + flash_at(t, tN, 0.2))


# ------------------------------------------------------------------ rc4  the gate opens: Krishna comes out alone


GATE4 = (720, 0.95)                  # the gate: x, scale (ground G)
KR4 = 0.42


def s_out(cr, t, tl, t0, t1):
    c = cues(tl, "rc4")
    tW, tA, tO = c["W"], c["A"], c["O"]
    gx, gs = GATE4
    glow(cr, gx, G - 260, 420, 0.5)
    if t > tA - 0.2:                                     # the whole army, far away on the left
        a = prog(t, tA - 0.2, 0.5)
        for i, (ax, ay, s_) in enumerate(((110, 1560, 0.24), (190, 1600, 0.28))):
            prop(cr, "rc_army", ax, ay - 5 * abs(math.sin(t * 6 + i)), s_, alpha=0.75 * a, blur=4.0 - i)
    prop(cr, "rc_gate", gx, G, gs)
    ground(cr)
    op = clamp((t - t0 - 0.05) / 0.55)
    hw = RC.GATE_ARCH[0] / 2 * gs
    t_out0, t_out1 = t0 + 0.6, max(t0 + 1.4, tW - 0.15)
    xx, bob, rock, legp = hop_walk(t, t_out0, t_out1, gx, 470, 0.4)
    near = ease(clamp((t - t_out0) / (t_out1 - t_out0)))  # coming out toward us: his shadow grows
    ks, kf = KR4 + (0.6 - KR4) * near, G + 40 * near
    if t > tO - 0.1:
        xx, bob, rock, legp = hop_walk(t, tO - 0.1, tO + 0.6, 470, 400, 0.35)
    show = prog(t, tW - 0.1, 0.3)
    fr = mix((-0.32, -0.55), OPEN["front"], show)
    ba = mix((0.3, -0.25), OPEN["backa"], show)

    def kr(cr_):
        return krishna(cr_, t, xx, ks, mood="calm", flip=True, front=fr, backa=ba, y=kf - 434 * ks + bob,
                       legs=(0.3 * legp, -0.3 * legp), rot=rock, ph=0.3, hits=[(tW, 0.4)])
    if op < 1:
        pts = kr(cr)
        door(cr, gx - hw, G, gs, op)
        door(cr, gx + hw, G, gs, op, flip=True)
    else:
        door(cr, gx - hw, G, gs, 1.0)
        door(cr, gx + hw, G, gs, 1.0, flip=True)
        pts = kr(cr)
    hf, hb = to_user(cr, pts["handF"]), to_user(cr, pts["handB"])

    def ui(cr):
        if t < tA - 0.1:
            head2(cr, t, "KRISHNA CAME OUT WITH", t0 + 0.05, "NO WEAPON", tW, big_size=270)
        else:
            head2(cr, t, "NO WEAPON,", tA - 0.1, "ALONE!", tA + 0.05, big_size=300, under=tO)
        fade = 1 - prog(t, tA, 0.3)                      # "no weapon" told: it clears for "alone"
        if t > tW - 0.05 and fade > 0.01:                # the empty hands: a sword crossed out
            q = prog(t, tW - 0.05, 0.3) * fade
            sx, sy = (hf[0] + hb[0]) / 2 - 60, min(hf[1], hb[1]) - 170
            prop(cr, "ar_sword", sx, sy + 120, 0.36 * q, rot=-0.5, alpha=q)
            big_x(cr, sx - 30, sy - 10, 170, 190, prog(t, tW + 0.15, 0.3), alpha=fade, lw=16)
            red_ring(cr, hf[0] - 8, hf[1] + 14, 120, 80, prog(t, tW + 0.1, 0.35), 7, alpha=fade)
        if t > tA:
            plate(cr, t, tA + 0.1, "THE WHOLE ARMY", 170, 1320, 30)
    return dict(ui=ui, flash=flash_at(t, tW, 0.2) + flash_at(t, tA, 0.2))


# ------------------------------------------------------------------ rc5  he laughs: "I'll catch him by hand!"


KL5 = (360, 0.9)
BUB5 = (760, 820, 0.62)


def s_laugh(cr, t, tl, t0, t1):
    c = cues(tl, "rc5")
    tS, tL, tW, tH, tP = c["S"], c["L"], c["W"], c["H"], c["P"]
    glow(cr, 540, 1300, 620, 0.38)
    ground(cr)
    x, s = KL5
    laugh = tS - 0.1 < t < tH
    jig = 0.04 * math.sin(t * 19) if laugh else 0.0
    grab = keyed(t, [(t0, 0.0), (tH, 1.0), (tP, 2.0)], 0.25, 1.3)
    if grab < 1:
        fr = mix((-0.6, -0.8), (-1.6, -0.6), grab)
    else:
        fr = mix((-1.6, -0.6), (-1.35, -1.1), grab - 1)
    ba = (0.4, -0.5) if grab < 0.5 else mix((0.4, -0.5), (-1.1, -0.9), min(1.0, grab))
    mood = "fierce" if t < tS - 0.1 else ("laugh" if t < tH else "sly")
    pts = kala(cr, t, x, s, mood=mood, sword=t < tH, front=fr, backa=ba, head=-0.18 * laugh + jig,
               rot=jig * 0.4, hits=[(tH, 0.5), (tP, 0.4)], ph=0.4)
    if t > tH:                                           # the sword thrown down: it clatters onto the ground
        u = clamp((t - tH) / 0.45)
        hx, hy = to_user(cr, pts["handF"])
        p0, p1 = (x + 250, G - 480), (x - 60, G - 18)
        sx = p0[0] + (p1[0] - p0[0]) * u
        sy = p0[1] + (p1[1] - p0[1]) * u * u - 120 * math.sin(math.pi * u)
        rot = 0.5 - (0.5 + math.pi / 2 + 0.1) * ease(u)
        if u >= 1:
            dt = t - tH - 0.45
            sy -= 30 * abs(math.sin(9 * dt)) * math.exp(-5 * dt)
        prop(cr, "rc_sword", sx, sy, 0.66, rot=rot)
        if 0.95 < u and t < tH + 1.2:
            for k in (-1, 1):
                q = clamp((t - tH - 0.45) / 0.6)
                puff(cr, sx + k * (40 + 80 * q), G - 20 - 20 * q, 40 + 30 * q, 0.7 * (1 - q))
    bx, by, bs = BUB5
    q = back(clamp((t - tS) / 0.35), 1.5) * (1 - prog(t, tH - 0.15, 0.25))
    if q > 0.01:                                         # what he thinks: little Krishna, alone, empty-handed
        prop(cr, "ar_think", bx, by, bs * (0.6 + 0.4 * clamp(q)), rot=sway(t, 0.006, 0.4), alpha=clamp(q),
             flip=True)
        if q > 0.7:
            krishna(cr, t, bx + 10, 0.24, mood="calm", flip=True, front=OPEN["front"], backa=OPEN["backa"],
                    feet=by + 130, rods=False, alpha=clamp(q))
    top = to_user(cr, pts["top"])

    def ui(cr):
        if t < tW - 0.1:
            head2(cr, t, "KALAYAVANA LAUGHED:", t0 + 0.05, "ALONE?", tL, big_size=300)
        elif t < tH - 0.1:
            head2(cr, t, "ALONE, AND", tW - 0.1, "NO WEAPON?", tW + 0.05, big_size=260)
        else:
            head2(cr, t, "'I'LL CATCH HIM", tH - 0.1, "BY HAND!'", tH + 0.05, big_size=280, under=tP)
        if laugh and t > tS + 0.2:
            for i, (dx, dy) in enumerate(((70, -60), (130, -10), (40, -120))):
                a = 0.5 + 0.5 * math.sin(t * 9 + i * 2)
                draw_text(cr, "HA!", top[0] + dx + 40, top[1] + dy + 60, 44, INK, 0.85 * a, anchor="cm")
        if q > 0.7:
            plate(cr, t, tL, "ALONE", bx - 140, by - 120, 30, alpha=clamp(q))
            plate(cr, t, tW, "NO WEAPON", bx + 130, by - 40, 30, alpha=clamp(q))
    return dict(ui=ui, flash=flash_at(t, tH, 0.25) + flash_at(t, tL, 0.15))


# ------------------------------------------------------------------ rc6  he comes closer: Krishna turns and runs


KR6 = (740, 0.6)


def s_turn(cr, t, tl, t0, t1):
    c = cues(tl, "rc6")
    tP, tK, tB, tR = c["P"], c["K"], c["B"], c["R"]
    glow(cr, 560, 1300, 640, 0.36)
    ground(cr)
    kx, ks = KR6
    if t < tR:                                           # Krishna, calm; he turns his back
        turned = t > tB
        hop = math.sin(math.pi * clamp((t - tB) / 0.25)) * (t > tB)
        krishna(cr, t, kx, ks, mood="calm" if not turned else "back", flip=not turned, y=G - 434 * ks - 40 * hop,
                front=(-0.5, -0.5) if not turned else (-0.9, -1.2), backa=(0.3, -0.3) if not turned else (0.7, -1.0),
                ph=0.3, hits=[(tK, 0.3), (tB, 0.5)])
    else:                                                # and runs off to the right
        u = clamp((t - tR) / 1.1)
        rx = kx + 620 * ease(u)
        dust(cr, t, tR, tR + 1.1, lambda ts: (kx + 620 * ease(clamp((ts - tR) / 1.1)) - 90, G - 20), 0.1, 0.9,
             -140, 0.9)
        kr_run(cr, t, rx, G, ks, "back")
        speed_lines(cr, t, rx - 120, G - 600 * ks, 380 * ks, 0.8 * (1 - prog(t, tR + 1.0, 0.3)))
    lunge = keyed(t, [(t0, 0.0), (tP, 1.0), (tR + 0.1, 2.0)], 0.3, 1.3)
    if lunge <= 1:
        lx, bob, rock, legp = hop_walk(t, t0 - 0.1, tP + 0.2, 60, 330, 0.36)
        lean = 0.0
    else:
        lx, bob, rock, legp = 330 + 110 * (lunge - 1), 0.0, 0.0, 0.0
        lean = 0.14 * (lunge - 1)
    grab = clamp(lunge)
    fr = mix((-0.5, -0.6), (-1.55, -0.3), grab)
    ba = mix((0.3, -0.4), (-1.35, -0.45), grab)
    kala(cr, t, lx, 0.78, mood="sly" if t < tR else "shock", front=fr, backa=ba, y=G - 434 * 0.78 + bob,
         legs=(0.3 * legp - 0.3 * (lunge > 1), -0.3 * legp + 0.25 * (lunge > 1)), rot=rock + lean, ph=0.5,
         hits=[(tR + 0.1, 0.6)])

    def ui(cr):
        if t < tB - 0.1:
            head2(cr, t, "KALAYAVANA CAME", t0 + 0.05, "CLOSER...", tP, big_size=290)
        else:
            head2(cr, t, "AND KRISHNA", tB - 0.1, "RAN!", tR, big_size=320, under=tR + 0.3)
        if t > tR + 0.15 and t < tR + 1.3:
            plate(cr, t, tR + 0.15, "MISSED!", 700, 1060, 40, t_out=tR + 1.05)
    return dict(ui=ui, flash=flash_at(t, tP, 0.15) + flash_at(t, tR, 0.3))


# ------------------------------------------------------------------ rc7  "coward!" and the chase


def hills_far(cr, t, speed, alpha=1.0, y=1640, s=0.42, blur=4.0):
    """Far hills sliding past to the left (the chase moving right)."""
    span = 1600.0
    m = (speed * t) % span
    for k in range(-1, 3):
        x = 300 + k * 800 - m
        prop(cr, "hn_hill", x, y, s * (1.0 if k % 2 else 0.8), alpha=0.7 * alpha, blur=blur, flip=bool(k % 2))


def s_shout(cr, t, tl, t0, t1):
    c = cues(tl, "rc7")
    tC, tD, tW, tF = c["C"], c["D"], c["W"], c["F"]
    run = t > tF
    hills_far(cr, t, 60.0 if not run else 60.0 + 200 * prog(t, tF, 0.4), y=1700)
    glow(cr, 540, 1300, 620, 0.35)
    ground(cr)
    kx = 900 + 20 * math.sin(t * 1.3)                    # Krishna far ahead, running
    kr_run(cr, t, kx, G - 140, 0.34, "back", blur=2.0, rods=False)
    dust(cr, t, t0 - 1, 99.0, lambda ts: (900 + 20 * math.sin(ts * 1.3) - 50, G - 150), 0.13, 0.8, -150, 0.4, 0.8)
    if not run:
        fist = keyed(t, [(t0, 0.0), (tC, 1.0)], 0.25, 1.4)
        fr = mix((-0.6, -0.7), (-2.6, -0.6), fist)
        pts = kala(cr, t, 330, 0.84, mood="shout" if t > tC - 0.1 else "fierce", front=fr, backa=(0.5, -0.8),
                   head=-0.08 * fist, hits=[(tC, 0.4), (tD, 0.5), (tW, 0.3)], ph=0.4,
                   rot=0.02 * math.sin(t * 20) * (t > tC))
    else:
        u = clamp((t - tF) / 1.2)
        pts = kala_run(cr, t, 330 + 160 * ease(u), G, 0.84, "shout", ph=0.1, front=(-2.4, -0.4))
        dust(cr, t, tF, 99.0, lambda ts: (330 + 160 * ease(clamp((ts - tF) / 1.2)) - 160, G - 20), 0.12, 0.9, -200,
             1.0)
    mouth = to_user(cr, pts["mouth"])
    if not run:
        sound_rings(cr, mouth[0] + 20, mouth[1], t, tC - 0.05, n=5, period=0.3, rmax=360, alpha=0.6)

    def ui(cr):
        if t < tF - 0.1:
            head2(cr, t, "HE SHOUTED:", t0 + 0.05, "COWARD!", tD, big_size=320)
        else:
            head2(cr, t, "AND HE", tF - 0.1, "CHASED HIM!", tF + 0.05, big_size=280)
        if tW - 0.15 < t < tF + 0.3:
            cloud_text(cr, t, min(mouth[0] + 330, 760), mouth[1] - 250, 0.72,
                       [("WHERE ARE YOU", 58, INK, -40, tW), ("RUNNING?", 84, RED, 40, tW + 0.15)], t_in=tW - 0.15,
                       alpha=1 - prog(t, tF + 0.05, 0.25))
    return dict(ui=ui, flash=flash_at(t, tD, 0.25) + flash_at(t, tF, 0.2))


# ------------------------------------------------------------------ rc8  just out of reach ... into a dark cave


CAVE8 = 1.3                          # the cave's scale here
KR8, KL8 = (690, 0.56), (300, 0.74)


def s_chase(cr, t, tl, t0, t1):
    c = cues(tl, "rc8")
    tD, tP, tG, tE = c["D"], c["P"], c["G"], c["E"]
    tin = tG - 0.6                                       # the cave hill slides in from the right
    slide = ease(clamp((t - tin) / 1.0))
    cx = 1700 - (1700 - 900) * slide
    hills_far(cr, t, 240 * (1 - 0.8 * slide), y=1700)
    glow(cr, 540, 1300, 620, 0.35)
    mx = cx + RC.CAVE_MOUTH[0] * CAVE8                   # the mouth's centre
    if t > tin - 0.1:
        prop(cr, "rc_cave_back", cx, G, CAVE8)
    ground(cr)
    kx0, ks = KR8
    enter0 = tG + 0.1
    if t < enter0:
        kx = kx0 + 10 * math.sin(t * 2.1)
    else:
        kx = kx0 + 10 * math.sin(enter0 * 2.1) + (mx - kx0 + 20) * ease(clamp((t - enter0) / 0.9))
    inside = t > enter0 and kx > mx - RC.CAVE_MOUTH[2] * CAVE8 * 0.5 + 70
    depth_k = clamp((kx - (mx - 60)) / 120) if inside else 0.0
    kdraw = (lambda cr_: kr_run(cr_, t, kx, G, ks * (1 - 0.3 * depth_k), "back", alpha=1 - 0.75 * depth_k,
                                blur=4 * depth_k, rods=not inside, ph=0.05))
    if inside:
        kp = kdraw(cr)
        if t > tin - 0.1:
            prop(cr, "rc_cave", cx, G, CAVE8)
    else:
        if t > tin - 0.1:
            prop(cr, "rc_cave", cx, G, CAVE8)
        dust(cr, t, t0 - 1, enter0, lambda ts: (kx0 - 80, G - 20), 0.11, 0.8, -220, 0.8)
        kp = kdraw(cr)
    lx0, ls = KL8
    lx = lx0 + 14 * math.sin(t * 2.1 + 0.6) + (150 * ease(clamp((t - tE) / 1.0)) if t > tE else 0.0)
    reach = keyed(t, [(t0, 0.0), (tP - 0.2, 1.0)], 0.3, 1.2)
    lp = kala_run(cr, t, lx, G, ls, "shout", front=mix((-1.0, -1.2), (-1.62, -0.12), reach), ph=0.12)
    dust(cr, t, t0 - 1, 99.0, lambda ts: (lx0 - 100, G - 20), 0.12, 0.9, -240, 1.0)
    hand = to_user(cr, lp["handF"])
    back_ = to_user(cr, kp["chest"]) if kp else (kx, G - 600 * ks)

    def ui(cr):
        if t < tG - 0.1:
            head2(cr, t, "KRISHNA KEPT RUNNING,", t0 + 0.05, "JUST OUT OF REACH", tP, big_size=220)
        else:
            head2(cr, t, "INTO A", tG - 0.1, "DARK CAVE", tG + 0.05, big_size=300, under=tE + 0.2)
        if tP - 0.1 < t < tG:                            # the gap between his hand and Krishna's back
            q = prog(t, tP - 0.1, 0.3) * (1 - prog(t, tG - 0.3, 0.25))
            gx = (hand[0] + back_[0] - 40) / 2
            red_ring(cr, gx, hand[1] + 10, max(70, (back_[0] - 40 - hand[0]) / 2 + 40), 70, q, 8)
            plate(cr, t, tP + 0.1, "SO CLOSE!", gx, hand[1] - 110, 40, alpha=q)
    return dict(ui=ui, flash=flash_at(t, tP, 0.15) + flash_at(t, tG, 0.2))


# ------------------------------------------------------------------ rc8q  was Krishna scared?


def s_question(cr, t, tl, t0, t1):
    c = cues(tl, "rc8q")
    tQ, tD = c["Q"], c["D"]
    glow(cr, 540, 1400, 600, 0.35)
    cs, cxq = 0.85, 760
    prop(cr, "rc_cave_back", cxq, G, cs)
    mx = cxq + RC.CAVE_MOUTH[0] * cs
    prop(cr, "rc_cave", cxq, G, cs)
    ground(cr)
    glow(cr, mx, G - 200, 240, 0.6)                      # Krishna waits in the cave mouth, small
    krishna(cr, t, mx + 10, 0.34, mood="calm", flip=True, ph=0.3, head=0.04 * math.sin(t * 1.4))

    def ui(cr):
        head2(cr, t, "SO TELL ME...", t0 + 0.05, None, 0.0)
        qmark(cr, t, tQ - 0.1, 540, 640, 330, RED)
        card2(cr, t, tQ, 540, 960, 1.05, [("WAS KRISHNA", 84, INK, -54, tQ + 0.3), ("SCARED?", 116, RED, 40, tD)])
    return dict(ui=ui, flash=flash_at(t, tQ, 0.15) + flash_at(t, tD, 0.2), night=0.06)


# ------------------------------------------------------------------ inside the cave


def cave_in(cr, t, webs=1.0, light=1.0, bx=540):
    """Inside the cave: the rock frame, a soft light on the bed, cobwebs grown by `webs`."""
    glow(cr, bx, CG - 380, 620, 0.5 * light)
    prop(cr, "rc_cave_in", 540, 960, 1.0)
    for (x, y, rot, s, d) in ((80, 140, 0.0, 0.95, 0.0), (1000, 150, math.pi / 2, 0.8, 0.25),
                              (120, 1450, -0.3, 0.5, 0.5)):
        q = ease(clamp(webs * 1.6 - d))
        if q > 0.01:
            prop(cr, "rc_web", x, y, s * q, rot=rot, alpha=0.9 * q)


BED9 = (500, 1.05)                   # the bed: x, scale
MK9 = (560, 0.74)                    # the sleeper: hip x, scale


def s_king(cr, t, tl, t0, t1):
    c = cues(tl, "rc9")
    tC, tY, tK, tS, tM = c["C"], c["Y"], c["K"], c["S"], c["M"]
    webs = prog(t, tY - 0.1, 1.4)
    cave_in(cr, t, webs, 0.6 + 0.4 * prog(t, t0, 0.6))
    bx, bs = BED9
    x, s = MK9
    pts = sleeper(cr, t, bx, bs, x, s, "sleep")
    q = ease(clamp((webs - 0.4) * 2))
    if q > 0.01:                                         # webs on the bed too: he has slept for years
        prop(cr, "rc_web", bx - RC.BED_W / 2 * bs + 10, bed_top(bx, bs) + 20, 0.45 * q, alpha=0.9 * q)
    head = to_user(cr, pts["head"])
    zzz(cr, t, head[0] - 10, head[1] - 40, 2.4, alpha=prog(t, tS - 0.2, 0.4))

    def ui(cr):
        if t < tK - 0.1:
            head2(cr, t, "IN THAT CAVE, FOR", t0 + 0.05, "MANY YEARS...", tY, big_size=260)
        elif t < tM - 0.1:
            head2(cr, t, "A KING WAS", tK - 0.1, "ASLEEP", tS, big_size=320)
        else:
            head2(cr, t, "HIS NAME WAS", tM - 0.1, "MUCHUKUNDA", tM + 0.05, big_size=230)
        if t > tM:
            tag(cr, t, tM + 0.1, "MUCHUKUNDA", 470, 1140, 42)
            plate(cr, t, tM + 0.4, "A GREAT OLD KING", 470, 1215, 30)
    return dict(ui=ui, flash=flash_at(t, tC, 0.15) + flash_at(t, tM, 0.2), night=0.16)


# ------------------------------------------------------------------ rc10  flashback: he fought for the gods; the gift


ASURAS = ((890, 0.6, 0.0), (1030, 0.54, 0.5))


def sky_cycle(cr, t, t0, t1, alpha=1.0):
    """Suns and moons racing across the sky: a long, long time."""
    if alpha <= 0.01 or t < t0:
        return 0.0
    n = 1.1
    ph = ((t - t0) * n) % 1.0
    day = int((t - t0) * n) % 2 == 0
    x = 1080 - 1080 * ph
    y = 900 - 170 * math.sin(math.pi * ph)
    a = alpha * math.sin(math.pi * ph) * (1 - prog(t, t1, 0.3))
    prop(cr, "sun" if day else "moon", x, y, 0.4 if day else 0.6, rot=t * 0.4, alpha=a)
    return (0 if day else 1) * a


def s_flashback(cr, t, tl, t0, t1):
    c = cues(tl, "rc10")
    tD, tF, tB, tS = c["D"], c["F"], c["B"], c["S"]
    glow(cr, 540, 1300, 620, 0.4)
    night = 0.22 * sky_cycle(cr, t, tF - 0.2, tB - 0.2)
    ground(cr)
    hands = []
    for i, (x, s, ph) in enumerate(((110, 0.56, 0.0), (270, 0.5, 1.1))):
        b, k, a = depth(t, tD - 0.25 + 0.12 * i, 0.5)
        give = t > tB - 0.1
        xx = x + 50 * ease(clamp((t - tB) / 0.6)) * give
        a *= 1 - 0.45 * prog(t, tS, 0.5)                 # the gift given, the gods step back
        pts = deva(cr, t, xx, s * k, pose="garland" if give else "stand", feet=G + 10 * i, alpha=a, blur=b + 2 * i,
                   ph=ph)
        if pts:
            hands.append(to_user(cr, pts["handF"]))
    mx, ms = 580, 0.7
    asleep = t > tS - 0.05
    fight = tD - 0.2 < t < tB
    swing = 0.5 + 0.5 * math.sin((t - tF) * 7.0) if fight and t > tF else 0.0
    if not asleep:
        fr = mix((-1.0, -0.4), (-2.7, -0.2), swing) if t < tB else (-0.5, -0.6)
        mpts = mk(cr, t, mx, ms, mood="fight" if t < tB else "calm", sword=t < tB, front=fr, backa=(0.3, -0.5),
                  ph=0.2, hits=[(tB, 0.4)])
        chest = to_user(cr, mpts["chest"])
    else:                                                # he lies down to sleep
        u = ease(clamp((t - tS + 0.05) / 0.7))
        rot = -math.pi / 2 * u
        hy = G - 434 * ms + (434 - 66) * ms * u
        ang = man_angles("rc_mk", t, (0.3, -0.25), (0.25, -0.15), 0.0)
        mpts = puppet(cr, RC.MUCHU, mx + 200 * u, hy, ms, rot, False, ang, swap={"rc_mk_head": MK_HEAD["sleep"]})
        chest = to_user(cr, mpts["chest"])
        hd = to_user(cr, mpts["head"])
        zzz(cr, t, hd[0] + 20, hd[1] - 70, 2.0, alpha=prog(t, tS + 0.4, 0.4))
    for i, (ax, s, ph) in enumerate(ASURAS):             # the demons, pushed back at every swing
        a = prog(t, tD + 0.1 + 0.15 * i, 0.4) * (1 - prog(t, tB - 0.4, 0.4))
        if a > 0.01:
            push = 50 * swing + 30 * math.sin(t * 3 + ph)
            prop(cr, "rc_asura", ax + push, G + 10, s, rot=0.05 * math.sin(t * 6 + ph), alpha=a, flip=True)
    if fight and t > tF:
        for k in range(3):                               # clashes: sparks where sword meets club
            tk = tF + 0.45 * k
            if tk < t < tk + 0.3:
                burst(cr, t, 800 + 30 * k, 1150 - 40 * k, tk, n=10, rmax=160, alpha=0.6)
    for i, h in enumerate(hands):
        flow(cr, t, tB + 0.1 * i, tS - 0.2, h, chest, n=8, lift=160, alpha=0.9, r=22, dur=0.8)

    def ui(cr):
        if t < tB - 0.1:
            head2(cr, t, "HE FOUGHT FOR", t0 + 0.05, "THE GODS", tD, big_size=300)
            if t > tF:
                plate(cr, t, tF + 0.1, "FOR YEARS AND YEARS!", 540, 640, 40)
        elif t < tS - 0.1:
            head2(cr, t, "THE GODS GAVE HIM A", tB - 0.1, "GIFT", tB + 0.05, big_size=320)
        else:
            head2(cr, t, "THE GODS' GIFT:", tS - 0.1, "SLEEP!", tS + 0.05, big_size=320, under=tS + 0.5)
        tag(cr, t, tD + 0.3, "THE GODS", 190, 1080, 36, t_out=tB - 0.2)
        if t > tB - 0.1 and t < tS:
            tag(cr, t, tB + 0.1, "MUCHUKUNDA", 600, 1020, 36)
    return dict(ui=ui, sepia=0.6, night=night, flash=flash_at(t, tD, 0.15) + flash_at(t, tB, 0.25))


# ------------------------------------------------------------------ rc11  the rule: wake him -> his eyes -> ash


ROWS11 = (720, 1110, 1520)


def s_rule(cr, t, tl, t0, t1):
    c = cues(tl, "rc11")
    tW, tE, tA = c["W"], c["E"], c["A"]
    glow(cr, 540, 1150, 700, 0.38)
    y1, y2, y3 = ROWS11
    a1 = prog(t, tW - 0.3, 0.3)
    if a1 > 0.01:                                        # 1: the shut eye, shaken awake
        sh = 10 * math.sin(t * 28) * prog(t, tW, 0.2) * (1 - prog(t, tE - 0.2, 0.3))
        prop(cr, "rc_eye_shut", 540 + sh, y1, 0.85, alpha=a1)
        for k in (-1, 1):
            if t > tW:
                cr.save()
                cr.set_source_rgba(*INK, 0.7 * a1)
                cr.set_line_width(6)
                for j in range(3):
                    xx = 540 + k * (200 + 22 * j)
                    cr.move_to(xx, y1 - 40 + 20 * j)
                    cr.line_to(xx + k * 30, y1 - 50 + 20 * j)
                cr.stroke()
                cr.restore()
    a2 = prog(t, tE - 0.2, 0.3)
    if a2 > 0.01:                                        # 2: the eye opens, glowing
        op = ease(clamp((t - tE + 0.05) / 0.35))
        glow(cr, 540, y2, 260, 0.7 * op * a2)
        warm(cr, 540, y2, 260, 0.6 * op * a2)
        aura(cr, t, 540, y2, 150, 330, 0.8 * op * a2, n=18, spin=0.3)
        cr.save()
        cr.translate(540, y2)
        cr.scale(0.85, 0.85 * max(0.08, op))
        pc.paint_part(cr, "rc_eye", a2)
        cr.restore()
        if op < 0.6:
            prop(cr, "rc_eye_shut", 540, y2, 0.85, alpha=a2 * (1 - op / 0.6))
    a3 = prog(t, tE + 0.3, 0.3)
    if a3 > 0.01:                                        # 3: whoever is there flashes white: only ash is left
        fx, fs = 540, 0.3
        gone = clamp((t - tA) / 0.25)
        if gone < 1:
            fn = (lambda cr_: puppet(cr_, RC.KALA, fx, y3 + 140 - 434 * fs, fs, 0.0, False,
                                     man_angles("rc_kala", t, (-1.6, -0.3), (-1.2, -0.6)), rods=False))
            silhouette(cr, fn, 0.9 * a3 * (1 - gone))
            white_out(cr, fn, gone * 1.2 * a3 + 0.6 * prog(t, tA - 0.3, 0.3))
        if t > tA:
            glow(cr, fx, y3, 300, 0.8 * math.exp(-2 * (t - tA)))
            prop(cr, "rc_ash", fx, y3 + 150, 0.55 * clamp((t - tA) / 0.3 + 0.3))
            ash_flakes(cr, t, tA, fx, y3 + 100, n=20, spread=60, rise=300, drift=120, dur=2.2)

    def ui(cr):
        head2(cr, t, "WHOEVER WAKES HIM UP...", t0 + 0.05, "TURNS TO ASH!", tA, big_size=270)
        plate(cr, t, tW, "WAKE HIM UP", 540, y1 + 110, 36)
        if t > tE - 0.2:
            down_arrow(cr, 540, y1 + 150, y2 - 140, prog(t, tE - 0.25, 0.25), w=12)
            plate(cr, t, tE + 0.1, "ONE LOOK", 830, y2, 36)
        if t > tE + 0.2:
            down_arrow(cr, 540, y2 + 120, y3 - 170, prog(t, tE + 0.25, 0.25), w=12)
        if t > tA:
            plate(cr, t, tA + 0.15, "ASH!", 760, y3 + 120, 48, color=RED)
    return dict(ui=ui, flash=flash_at(t, tE, 0.25) + flash_at(t, tA, 0.35))


# ------------------------------------------------------------------ rc12  in the dark: "that's Krishna!"


BED12 = (680, 0.86)
MK12 = (640, 0.66)                   # the sleeper's hip on the screen (his feet to the left, toward Kalayavana)
KL12 = (230, 0.7)
BUB12 = (660, 860, 0.8)


def sleeper_dark(cr, t, dark=0.65, bump=0.0, shake=0.0, sit=0.0, mood="sleep"):
    """The bed and the sleeping king in the dark (a dark shape with faint detail); returns his points."""
    bx, bs = BED12
    x, s = MK12
    return sleeper(cr, t, bx, bs, x, s, mood, sit=sit, bump=bump, shake=shake, dark=dark)


def s_mistake(cr, t, tl, t0, t1):
    c = cues(tl, "rc12")
    tC, tS, tT, tK, tN = c["C"], c["S"], c["T"], c["K"], c["N"]
    cave_in(cr, t, 1.0, 0.55, bx=BED12[0])
    sleeper_dark(cr, t, 0.6)
    lx, ls = KL12
    xx, bob, rock, legp = hop_walk(t, t0 - 0.1, max(t0 + 1.0, tS - 0.2), -160, lx, 0.42)
    point = keyed(t, [(t0, 0.0), (tS, 1.0)], 0.3, 1.3)
    fr = mix((-0.5, -0.6), reach_arm(xx, CG - 434 * ls, ls, 26 * RC.KL_B, (640, CG - 380)), point)
    pts = kala(cr, t, xx, ls, mood="sly" if t > tT - 0.1 else "fierce", front=fr, backa=(0.4, -0.6), feet=CG,
               y=CG - 434 * ls + bob, legs=(0.3 * legp, -0.3 * legp), rot=rock, ph=0.4, hits=[(tS, 0.4), (tK, 0.4)])
    bx, by, bs = BUB12
    q = back(clamp((t - tT) / 0.35), 1.5)
    if q > 0.01:                                         # what he thinks: Krishna, pretending to sleep
        prop(cr, "ar_think", bx, by, bs * (0.6 + 0.4 * clamp(q)), rot=sway(t, 0.006, 0.4), alpha=clamp(q),
             flip=True)
        if q > 0.7:                                      # "pretending": now and then he peeks with one eye
            peek = t > tN and (t - tN) % 1.0 < 0.45
            kpts = puppet(cr, RC.KRISHNA, bx + 10, by + 70, 0.32, -math.pi / 2 + 0.01 * math.sin(t * 1.3), False,
                          man_angles("krishna", t, (0.3, -0.25), (0.25, -0.15)),
                          swap={"krishna_head": KR_HEAD["smile" if peek else "sleep"]}, rods=False, alpha=clamp(q))
            kh = to_user(cr, kpts["head"])
            zzz(cr, t, kh[0] + 10, kh[1] - 50, 1.4, alpha=clamp(q))
            if peek:
                ke = local(bx + 10, by + 70, 0.32, -math.pi / 2, False, 6 + 34, -300 - 118)
                red_ring(cr, ke[0], ke[1], 34, 30, prog(t, tN + int(t - tN), 0.2), 5)
    top = to_user(cr, pts["top"])

    def ui(cr):
        if t < tT - 0.1:
            head2(cr, t, "KALAYAVANA CAME IN AND SAW", t0 + 0.05, "A SLEEPING MAN", tS, big_size=220)
        elif t < tN - 0.1:
            head2(cr, t, "HE THOUGHT:", tT - 0.1, "'THAT'S KRISHNA!'", tK, big_size=220)
        else:
            head2(cr, t, "'HE'S ONLY", tN - 0.1, "PRETENDING!'", tN + 0.05, big_size=260)
        if t < tT:
            tag(cr, t, tC, "KALAYAVANA", max(200, top[0]), top[1] - 40, 36, t_out=tT - 0.2)
        if q > 0.7:
            plate(cr, t, tK, "KRISHNA!", bx + 170, by - 170, 36)
    return dict(ui=ui, night=0.22, lift=1.0, flash=flash_at(t, tS, 0.12) + flash_at(t, tK, 0.2))


# ------------------------------------------------------------------ rc13  the kick (in silhouette)


KL13 = (250, 0.72)


def s_kick(cr, t, tl, t0, t1):
    c = cues(tl, "rc13")
    tP, tR, tL = c["P"], c["R"], c["L"]
    cave_in(cr, t, 1.0, 0.65, bx=BED12[0])
    bump = 14 * math.exp(-6 * max(0.0, t - tL)) * abs(math.sin((t - tL) * 20)) * (t > tL)
    sleeper_dark(cr, t, 0.55, bump=bump)
    x, s = KL13
    wind = keyed(t, [(t0, 0.0), (tP, 1.0), (tL - 0.05, 2.0)], 0.22, 1.5)
    if wind <= 1:
        legs = (0.55 * wind, -0.05)
        lean = 0.12 * wind
    else:
        k = wind - 1
        legs = (0.55 - 1.95 * k, -0.05 + 0.15 * k)
        lean = 0.12 - 0.30 * k
    fr = (-0.6 - 0.8 * clamp(wind - 1), -0.7)
    ba = (0.6 + 0.6 * clamp(wind - 1), -0.5)
    hy = CG - 434 * s - 30 * clamp(wind - 1)

    def kfig(cr_):
        return kala(cr_, t, x, s, mood="shout", front=fr, backa=ba, y=hy, feet=CG, legs=legs, rot=lean, ph=0.4,
                    rods=False)
    glow(cr, x + 40, CG - 420, 420, 0.45)
    kp = silhouette(cr, kfig, 0.92)
    pc.rod(cr, x, hy - 200 * s, x + 30, H + 60, alpha=0.5)
    foot = to_user(cr, kp["hip"]) if kp else (x, hy)
    hit = (foot[0] + 300 * s, foot[1] + 80 * s)
    if t > tL:
        burst(cr, t, hit[0], hit[1], tL, n=14, rmax=320, alpha=0.8)

    def ui(cr):
        if t < tL - 0.1:
            head2(cr, t, "WITH ALL HIS", t0 + 0.05, "STRENGTH...", tP, big_size=290)
        else:
            head2(cr, t, "HE KICKED THE", tL - 0.1, "SLEEPING KING!", tL + 0.05, big_size=230)
        if t > tL:
            q = back(clamp((t - tL) / 0.25), 2.0)
            cr.save()
            cr.translate(hit[0] + 60, hit[1] - 170)
            cr.rotate(-0.12)
            cr.scale(q, q)
            draw_text(cr, "KICK!", 0, 0, 110, RED, clamp(q), anchor="cm")
            cr.restore()
    return dict(ui=ui, night=0.22, lift=1.0, flash=flash_at(t, tL, 0.45))


# ------------------------------------------------------------------ rc14  the twist: his eyes open; ashes


def s_ashes(cr, t, tl, t0, t1):
    c = cues(tl, "rc14")
    tW, tO, tK, tX = c["W"], c["O"], c["K"], c["X"]
    lit = prog(t, tO, 0.6)
    cave_in(cr, t, 1.0, 0.6 + 0.4 * lit, bx=BED12[0])
    sit = ease(clamp((t - tW - 0.2) / 0.8))
    stir = 0.6 * prog(t, tW - 0.1, 0.2) * (1 - prog(t, tW + 0.3, 0.3))
    mood = "sleep" if t < tO else "wake"
    pts = sleeper_dark(cr, t, 0.5 * (1 - lit), shake=stir, sit=sit, mood=mood)
    eye = to_user(cr, pts["eye"])
    if t > tO - 0.05:                                    # a pale fire in his open eyes, pouring at Kalayavana
        q = prog(t, tO - 0.05, 0.5)
        glow(cr, eye[0], eye[1], 200 + 120 * q, 0.9 * q)
        warm(cr, eye[0], eye[1], 260, 0.8 * q, (1.0, 0.86, 0.45))
        aura(cr, t, eye[0], eye[1], 30, 240 * q, 0.9 * q, n=14, spin=0.6)
        sparkle(cr, eye[0], eye[1], 50 * q * (0.8 + 0.2 * math.sin(t * 9)), q, (1.0, 0.98, 0.85))
    x, s = KL12
    gone = t > tX + 0.15
    if not gone:
        fear = prog(t, tO, 0.3)

        def kfig(cr_):
            return kala(cr_, t, x - 40 * fear, s, mood="shock" if t > tO else "sly",
                        front=mix((-0.6, -0.7), (-1.9, -0.9), fear), backa=mix((0.4, -0.6), (-1.6, -1.2), fear),
                        feet=CG, head=0.1 * fear, rot=-0.08 * fear, ph=0.4, hits=[(tO, 0.5)], rods=t < tK)
        kp = kfig(cr)
        chest = to_user(cr, kp["chest"])
        if t > tK - 0.1:                                 # the light reaches him: he goes white
            wq = prog(t, tK - 0.1, max(0.3, tX - tK + 0.1))
            white_out(cr, kfig, wq)
            glow(cr, chest[0], chest[1], 300, 0.7 * wq)
            beam_a = prog(t, tK - 0.2, 0.3)
            cr.save()
            cr.set_operator(cairo.OPERATOR_ADD)
            g = cairo.LinearGradient(eye[0], eye[1], chest[0], chest[1])
            g.add_color_stop_rgba(0, 1.0, 0.94, 0.70, 0.55 * beam_a)
            g.add_color_stop_rgba(1, 1.0, 0.94, 0.70, 0.15 * beam_a)
            cr.set_source(g)
            pc.poly(cr, [(eye[0], eye[1] - 10), (chest[0], chest[1] - 160), (chest[0], chest[1] + 160),
                         (eye[0], eye[1] + 10)])
            cr.fill()
            cr.restore()
    ash_x = x - 30
    if t > tX:                                           # only ash is left, drifting away
        glow(cr, ash_x, CG - 80, 260, 0.5)
        ash_heap(cr, ash_x, CG + 2, 0.95 * clamp((t - tX) / 0.3 + 0.2))
        ash_flakes(cr, t, tX, ash_x, CG - 160, n=34, spread=110, rise=700, drift=260, dur=3.0)
        for k in range(4):
            q = clamp((t - tX - 0.05 * k) / 1.6)
            puff(cr, ash_x + 30 * k - 40, CG - 200 - 260 * q, 90 + 80 * q, 0.6 * (1 - q), ASH_C)
    white = 0.9 * math.exp(-5 * max(0.0, t - tX)) * (t > tX)

    def ui(cr):
        if t < tO - 0.1:
            head2(cr, t, "THE KING", t0 + 0.05, "WOKE UP", tW, big_size=300)
        elif t < tX - 0.1:
            head2(cr, t, "HE OPENED HIS", tO - 0.1, "ANGRY EYES...", tO + 0.05, big_size=250)
        else:
            head2(cr, t, "AND KALAYAVANA BECAME", tX - 0.1, "ASHES!", tX + 0.05, big_size=320, under=tX + 0.5)
    return dict(ui=ui, night=0.22 * (1 - lit) + 0.06, lift=1.0, white=white,
                flash=flash_at(t, tW, 0.15) + flash_at(t, tO, 0.4))


# ------------------------------------------------------------------ rc15  the reveal: he led him there


CAVE15 = (790, 0.95)
GATE_M = (150, 1010, 0.17)           # the little map: Mathura's gate


def s_plan(cr, t, tl, t0, t1):
    c = cues(tl, "rc15")
    tN, tE, tM = c["N"], c["E"], c["M"]
    glow(cr, 540, 1300, 620, 0.4)
    cx, cs = CAVE15
    mx = cx + RC.CAVE_MOUTH[0] * cs
    prop(cr, "rc_cave_back", cx, G, cs)
    prop(cr, "rc_cave", cx, G, cs)
    ash_flakes(cr, t, t0 - 1.5, mx + 30, G - 260, n=22, spread=60, rise=560, drift=220, dur=3.4)
    ground(cr)
    krishna(cr, t, mx - 230, 0.56, mood="smile", front=(-0.5, -0.9), backa=(0.25, -0.5), ph=0.3,
            hits=[(tN, 0.3), (tM, 0.3)])
    mp = prog(t, tE - 0.2, 0.4)                          # the little map: the gate, the hills, the path to here
    if mp > 0.01:
        gx, gy, gs = GATE_M
        prop(cr, "rc_gate", gx, gy, gs, alpha=mp)
        for hx, hs in ((400, 0.22), (620, 0.18)):
            prop(cr, "hn_hill", hx, gy, hs, alpha=0.9 * mp, flip=hx > 500)
        path = ([(gx + 60, gy - 20), (300, gy - 120), (400, gy - 150), (500, gy - 110)] +
                [(560, gy - 100), (640, gy - 140), (720, gy - 90)] +
                [(mx + 40, gy + 140), (mx, G - 280)])
        dotted(cr, path, prog(t, tE, max(0.6, tM - tE - 0.1)), 26, 7, RED, mp)
        if t > tM:
            red_ring(cr, mx, G - 200, 170, 220, prog(t, tM, 0.4), 9)

    def ui(cr):
        if t < tE - 0.1:
            head2(cr, t, "KRISHNA WAS", t0 + 0.05, "NOT SCARED!", tN, big_size=270)
        else:
            head2(cr, t, "HE LED THE ENEMY", tE - 0.1, "RIGHT HERE!", tM, big_size=280, under=tM + 0.4)
        if mp > 0.01:
            plate(cr, t, tE, "MATHURA", GATE_M[0], GATE_M[1] + 40, 28, alpha=mp)
            plate(cr, t, tM + 0.2, "THE CAVE", mx + 160, G - 470, 30)
    return dict(ui=ui, flash=flash_at(t, tN, 0.15) + flash_at(t, tM, 0.3))


# ------------------------------------------------------------------ rc15c  the callback: the "coward" won


def s_callback(cr, t, tl, t0, t1):
    c = cues(tl, "rc15c")
    tD, tR, tW, tJ = c["D"], c["R"], c["W"], c["J"]
    x, s, gnd = HK
    win = prog(t, tJ - 0.1, 0.6)
    glow(cr, x + 40, gnd - 700 * s, 640, 0.35 + 0.3 * win)
    if win > 0.01:
        aura(cr, t, x + 20, gnd - 760 * s, 200, 640, 0.6 * win, n=22, spin=0.15)
        warm(cr, x + 20, gnd - 760 * s, 520, 0.3 * win)
    ground(cr, gnd - 4)
    dust(cr, t, t0 - 1.0, 99.0, lambda ts: (x - 170 * s, gnd - 20), 0.12, 0.9, -220, 1.0)
    speed_lines(cr, t, x - 120 * s, gnd - 650 * s, 480 * s, 0.6)
    kr_run(cr, t, x, gnd, s, "back_smile", ph=0.15, hits=[(tW, 0.3)])
    if t > tJ:
        burst(cr, t, x + 40, gnd - 900 * s, tJ, n=18, rmax=620, alpha=0.6)

    def ui(cr):
        if t < tW - 0.1:
            head2(cr, t, "THE ONE THEY CALLED A", t0 + 0.05, "'COWARD'...", tD, big_size=270)
        else:
            head2(cr, t, "WON THE FIGHT", tW - 0.1, "WITHOUT A WEAPON!", tW + 0.05, big_size=200, under=tJ)
        name_plaque(cr, t, tR - 0.25, tR)
    return dict(ui=ui, flash=flash_at(t, tR, 0.2) + flash_at(t, tJ, 0.3))


# ------------------------------------------------------------------ rc16  fear, or brains?


def s_end(cr, t, tl, t0, t1):
    c = cues(tl, "rc16")
    tQ, tF, tB = c["Q"], c["F"], c["B"]
    glow(cr, 540, 1400, 600, 0.42)
    ground(cr)
    cards = ((278, "FEAR?", tQ + 0.05), (802, "BRAINS?", tQ + 0.25))
    k = None
    if t > tF:
        if t < tB:
            k = 0
        else:
            k = (1 + int((t - tB) / 0.9)) % 2
    krishna(cr, t, 540, 0.62, mood="smile", flip=(k == 0), front=(-0.6, -0.9), backa=(0.25, -0.5), ph=0.3,
            hits=[(tF, 0.3), (tB, 0.3)])

    def ui(cr):
        head2(cr, t, "WHY DID", t0 + 0.05, "KRISHNA RUN?", tQ, big_size=250)
        for cx, txt, tc in cards:
            card(cr, t, tc - 0.25, cx, 770, 0.6, [(txt, 124, RED, 4)])
        if k is not None:
            ts = tF if t < tB else tB + 0.9 * int((t - tB) / 0.9)
            red_ring(cr, cards[k][0], 774, 248, 100, prog(t, ts, 0.35), 10)
    return dict(ui=ui, flash=flash_at(t, tF, 0.15) + flash_at(t, tB, 0.15))


SHOTS = [   # (line, cue: None = line start, draw function, options)
    ("rc1", None, s_hook, {"z": (1.0, 1.04)}),
    ("rc2", None, s_words, {"z": (1.0, 1.03)}),
    ("rc3", None, s_attack, {"z": (1.0, 1.04)}),
    ("rc4", None, s_out, {"z": (1.0, 1.03)}),
    ("rc5", None, s_laugh, {"z": (1.0, 1.04)}),
    ("rc6", None, s_turn, {"z": (1.0, 1.03)}),
    ("rc7", None, s_shout, {"z": (1.0, 1.03)}),
    ("rc8", None, s_chase, {"z": (1.0, 1.03)}),
    ("rc8q", None, s_question, {"z": (1.0, 1.03)}),
    ("rc9", None, s_king, {"z": (1.0, 1.04), "focus": (560, 1400)}),
    ("rc10", None, s_flashback, {"z": (1.0, 1.03)}),
    ("rc11", None, s_rule, {"z": (1.0, 1.03)}),
    ("rc12", None, s_mistake, {"z": (1.0, 1.03)}),
    ("rc13", None, s_kick, {"z": (1.0, 1.05), "focus": (420, 1450)}),
    ("rc14", None, s_ashes, {"z": (1.0, 1.04), "focus": (480, 1400)}),
    ("rc15", None, s_plan, {"z": (1.0, 1.03)}),
    ("rc15c", None, s_callback, {"z": (1.0, 1.04)}),
    ("rc16", None, s_end, {"z": (1.0, 1.03)}),
]


def _starts(tl):
    """Each shot's start (cached on the timeline under this module's own name, not shots.shot_at's)."""
    st = getattr(tl, "_rc_shot_starts", None)
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
        tl._rc_shot_starts = st
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
    """(time, name, dur), sparse (owner, 8 Nov 2026: "only use sounds where necessary"): a damaru on the hook, a hit
    on the kick, a conch as the old king's eyes open, shimmer on the reveal (he led him there), a bell on the closing
    question, then (only where they fit) shimmer on the gods' gift, a damaru as Krishna runs and a conch as the army
    comes. Chosen in THAT order of importance, each at least SFX_MIN_GAP from every sound already kept (as
    render_myth.calm_sfx keeps them), so the list returned is what plays (about 6 sounds); the bed dips before the
    reveals stay."""
    c = {b: cues(tl, b) for b in CUES}
    want = [(0.0, "damaru", 0), (c["rc13"]["L"], "hit", 0), (c["rc14"]["O"], "conch", 0),
            (c["rc15"]["M"], "shimmer", 0), (c["rc16"]["F"], "bell", 0), (c["rc10"]["B"], "shimmer", 0),
            (c["rc6"]["R"], "damaru", 0), (c["rc3"]["S"], "conch", 0)]
    kept = []
    for e in want:
        if e[1] in SFX_KEEP and all(abs(e[0] - k[0]) >= SFX_MIN_GAP for k in kept):
            kept.append(e)
    dips = [(c["rc13"]["L"] - 0.35, "dip", 0.5), (c["rc14"]["O"] - 0.3, "dip", 0.5),
            (c["rc15"]["E"] - 0.3, "dip", 0.45)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in sorted(kept + dips)]
