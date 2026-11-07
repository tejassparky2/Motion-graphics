"""Scenes for videos/ravana.py: Togalu Gombeyaata (Karnataka leather shadow-puppet theatre) drawn in code, the same
lamp-lit screen, headlines and rod-puppet motion as the Jarasandha reel (scenes_jarasandha), with the Ravana cast from
ravana_cast. Every frame is a pure function of t. English on-screen text only (shared by Hindi and Kannada); cues are
words of the line in each language ({"hi": ..., "kn": ...}) with a fraction fallback, so both languages stay in sync.

Shot list (line: what is on the screen)
  r1  HOOK: ten-headed Ravana alone, large; RAVANA, CARRIED BY A + red MONKEY (in by 0.5 s, underlined on "vanara");
      fist up and heads roaring on "gods"; a huge golden vanara arm scoops him under it ("armpit"); then a dotted
      loop round four ocean patches with Vali carrying him ("oceans")
  r2  NOT A FILM SCENE crossed out while the pair flies past; the palm-leaf book VALMIKI RAMAYANA rises; UTTARA KANDA
  r3  the tally board: RAMA, DEFEAT 1, DEFEAT 2 rows pop in; BEFORE RAMA, RAVANA LOST TWICE; his heads droop
  r4  AFTER A BOON FROM BRAHMA (glow, tag); HE SET OUT TO CONQUER THE WORLD: he marches across a cloth map, the kings
      on it topple and their crowns fly off
  r5  Kailasa; Nandi (vanara face, ash marks, trident) swings the trident across his path: NANDI; ring on his face:
      VANARA'S; Ravana's ten heads throw back and laugh: LAUGHED
  r6  NANDI'S CURSE on a torn note; vanara warriors rise along the bottom; MONKEYS WILL END YOUR CLAN stamp
  r7  DEFEAT 1, NARMADA: the river slides in under the bank, a Shiva linga appears, kneeling Ravana offers marigolds
  r8  KARTAVIRYA ARJUNA splashing in the river; his thousand arms fan open while N ARMS counts up to 1000
  r9  the arms swing forward into a wall of gold hands; upstream the water piles up: STOPPED THE RIVER
  r10 the river runs BACKWARDS (strips flow left, a red arrow); the FLOWERS float off the linga; Ravana turns angry
  r11 Ravana charges (FIGHT); the arms close on him; rope (TIED UP); dragged to MAHISHMATI; mini tally: DEFEAT 1 ticked
  r12 the sage Pulastya walks in with his staff (GRANDFATHER tag); Arjuna bows; the ropes fall away: FREE HIM
  r13 RE-HOOK: the screen darkens, a huge vanara shadow looms; DEFEAT 2 stamp slams in
  r14 KISHKINDHA; Vali steps from far away onto the cloth: VALI; flexes (VERY STRONG); Ravana marches off: FIGHT HIM
  r15 the southern ocean at sunset; Vali seated at SANDHYA, hands joined; Ravana tiptoes up FROM BEHIND
  r16 SNAP! Vali springs up and tucks Ravana under his arm (heads squashed, legs dangling): ARMPIT
  r17 round cloth map of the four oceans; dotted path S -> W -> N -> E with a tick at each; Vali flies with Ravana;
      ALL FOUR (the discs glow); a big pass of the dangling Ravana: ALL THE WAY
  r18 Kishkindha: Vali lands (YOJANAS, Ravana sees stars) and lets go (LET GO); a fire; their hands meet over it:
      FRIENDS; mini tally: DEFEAT 2 ticked
  r19 the curse note returns with Nandi and the laughing Ravana; Lanka's walls burn; Hanuman leaps over with his
      burning tail (BURNED LANKA); the vanara army marches to the gate (HIS GATES)
  r20 DID YOU KNOW? BEFORE RAMA, HE LOST TWICE; the tally (both ticked); the YES / NO card; Vali and Ravana small
"""
import math

import cairo

import puppet_core as pc
import ravana_cast as R
from poster import MONO_FONT, back, clamp, draw_text, ease, prog, text_size, tick
from puppet_core import H, W, depth, hop_walk, keyed, prop, puppet, sway
from scenes_jarasandha import FADE, FEET, INK, RED, big_word, bob_rot, fit, glow, ground, man_angles, man_y, motes
from scenes_jarasandha import head2 as _head2
from scenes_jarasandha import red_cross, red_ring, small_line, sound_rings, stamp, tag, walk_legs, walker
from shots import T, shot_at, starts

MISSES = set()                       # cue words not found in a line (checked by the build; falls back to fractions)
ROPE_C = (0.86, 0.66, 0.36)
MOODS = {"calm": "ravana_head", "laugh": "ravana_head_laugh", "angry": "ravana_head_angry"}


def cue(tl, bid, words, frac):
    """A word cue (real word timings when voiced) with a fraction fallback."""
    try:
        return T(tl, bid, words)
    except (KeyError, ValueError):
        MISSES.add((bid, words[getattr(tl, "lang", "hi")] if isinstance(words, dict) else words))
        return T(tl, bid, frac)


def F(tl, bid, f):
    return T(tl, bid, f)


def head2(cr, t, small, t_small, big, t_big, big_size=160, small_size=62, **kw):
    """scenes_jarasandha.head2 with both lines kept inside the side margins, even at the big word's pop-in
    overshoot (x1.18): the big word fits 800 px, the small line 940 px."""
    if big:
        big_size = min(big_size, fit(big, big_size, 800))
    if small:
        sw = sum(text_size(wd, small_size)[0] for wd in small.split()) + small_size * 0.34 * (len(small.split()) - 1)
        if sw > 940:
            small_size = int(small_size * 940 / sw)
    return _head2(cr, t, small, t_small, big, t_big, big_size=big_size, small_size=small_size, **kw)


# ------------------------------------------------------------------ puppets


def rv_angles(t, front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0), hits=(), ph=0.0):
    return man_angles("ravana", t, front, backa, head, legs, hits, ph)


def rv(cr, t, x, y, s, rot=0.0, flip=False, ang=None, mood="calm", jig=0.0, squash=0.0, look=0.0, alpha=1.0,
       blur=0.0, rods=True, kneel=False, only=None):
    """Ten-headed Ravana: hip at (x, y). ang = full angle dict (rv_angles); mood calm | laugh | angry; jig shakes the
    heads, squash presses them flat, kneel swaps the legs for the kneeling pair."""
    a = dict(ang if ang is not None else rv_angles(t))
    if jig:
        a["ravana_head"] = a.get("ravana_head", 0.0) + jig * 0.07 * math.sin(t * 15)
    hide = ()
    if kneel:
        prop(cr, "ravana_kneel", x, y, s, rot, alpha, blur, flip)
        hide = ("ravana_legF", "ravana_legB")
    extra = {"ravana_body": R.ravana_heads(t, mood, jig, squash, a.get("ravana_head", 0.0), alpha, blur, look)}
    swap = {"ravana_head": MOODS[mood]} if mood != "calm" else None
    return puppet(cr, R.RAVANA, x, y, s, rot, flip, a, alpha, blur, hide=hide, swap=swap, rods=rods, extra=extra,
                  only=only)


def rv_walk(cr, t, t0, t1, x0, x1, s, flip=False, t_in=None, mood="calm", front=(-0.32, -0.55), backa=(0.3, -0.25),
            step=0.42, lift=0.0, lean=0.0, feet=FEET, **kw):
    """Ravana walking in jerky rod-puppet steps (lift = extra bob for tiptoeing, lean = forward tilt)."""
    x, bob, rock, ph = hop_walk(t, t0, t1, x0, x1, step)
    b, k, a = depth(t, t_in if t_in is not None else t0, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    ang = rv_angles(t, front, backa, legs=walk_legs(ph, 0.32 + 0.2 * lift), hits=[(t1, 1.0)], ph=x0 * 0.01)
    y = feet - 434 * s + bob * (1 + 2.5 * lift)
    return rv(cr, t, x, y - (k - 1) * 300 * s, s * k, rock + bob_rot(t, x0) + lean * (-1 if flip else 1), flip, ang,
              mood, alpha=a, blur=b, **kw), x


def vali_angles(t, front=(-0.32, -0.55), backa=(0.3, -0.25), head=0.0, legs=(0.0, 0.0), hits=(), ph=0.0):
    return man_angles("vali", t, front, backa, head, legs, hits, ph)


def reach(hip_x, hip_y, s, bulk, target, flip=False):
    """(upper arm, forearm) angles for man_angles(front=...) so the near hand of a man() figure (hip at hip_x, hip_y,
    scale s, unrotated) lands on target: a two-link solve with the elbow below the line."""
    sgn = -1 if flip else 1
    sx, sy = hip_x + sgn * 26 * bulk * s, hip_y - 262 * s
    dx, dy = (target[0] - sx) * sgn, target[1] - sy
    a, b = 150 * s, 160 * s
    d = max(1e-3, min(math.hypot(dx, dy), a + b - 1e-3))
    base = math.atan2(-dx, dy)
    ang_a = math.acos(clamp((a * a + d * d - b * b) / (2 * a * d), -1, 1))
    ang_e = math.acos(clamp((a * a + b * b - d * d) / (2 * a * b), -1, 1))
    return base + ang_a, -(math.pi - ang_e)


VALI_FRONT = {"vali_armF_up", "vali_armF_lo"}
VALI_BACK = {p[0] for p in R.VALI.parts} - VALI_FRONT


def TUCK_XY(s):
    """Where Ravana's hip sits, relative to Vali's hip, when tucked under his arm (heads poke out in front)."""
    return -90 * s, -165 * s


def vali_carry(cr, t, x, y, s, rot=0.0, squash=1.0, grip=1.0, fly=0.0, alpha=1.0, blur=0.0, rods=True,
               flail=1.0, mood="calm", rv_rot=None, rv_xy=None, rv_s=None, ph=0.0, vali_rot=0.0):
    """Vali (hip at x, y, facing right) with Ravana tucked under his near arm, face down, heads squashed, legs
    dangling. grip 0..1 = the arm closing over him; fly 0..1 = flying pose (legs trailing)."""
    va = vali_angles(t, front=(0.55 - 0.3 * grip, -0.5 - 1.1 * grip), backa=(-0.4 - 0.9 * fly, -0.6),
                     legs=(-0.5 * fly, 0.45 * fly), head=-0.1 * fly, ph=ph)
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    puppet(cr, R.VALI, 0, 0, s, vali_rot, angles=va, alpha=alpha, blur=blur, rods=rods, only=VALI_BACK)
    rs = rv_s if rv_s is not None else 0.62 * s
    rx, ry = rv_xy if rv_xy is not None else TUCK_XY(s)
    w = 0.05 * math.sin(t * 7 + ph) * flail
    ra = rv_angles(t, front=(-1.6 + 0.5 * flail * math.sin(t * 9 + ph), -0.6),
                   backa=(-0.9 + 0.5 * flail * math.sin(t * 8 + 1 + ph), -0.4),
                   legs=(-1.2 + 0.35 * flail * math.sin(t * 6.5 + ph), -1.45 + 0.35 * flail * math.sin(t * 7.3 + 1)),
                   head=0.12)
    rv(cr, t, rx, ry, rs, (rv_rot if rv_rot is not None else math.pi / 2) + w, ang=ra, mood=mood, squash=squash,
       jig=0.25 * flail, alpha=alpha, blur=blur, rods=False)
    puppet(cr, R.VALI, 0, 0, s, vali_rot, angles=va, alpha=alpha, blur=blur, rods=False, only=VALI_FRONT)
    cr.restore()


def _club_in_hand(cr_):
    in_hand("rv_club", 158, math.pi - 0.5, 0.85)(cr_)


def vanara(cr, t, x, feet, s, flip=False, step=0.0, raise_=0.0, alpha=1.0, blur=0.0, ph=0.0, rot=0.0):
    """A vanara warrior with a club (the curse's promise, the army at Lanka); step = walk phase -1..1."""
    ang = man_angles("vanara", t, front=(-0.5 - 1.7 * raise_, -1.0 + 0.4 * raise_), backa=(0.4, -0.5),
                     legs=walk_legs(step, 0.3), ph=ph)
    return puppet(cr, R.VANARA, x, feet - 434 * s, s, rot + bob_rot(t, ph), flip, ang, alpha, blur, rods=False,
                  extra={"vanara_armF_lo": _club_in_hand})


def ka_fan(cr, t, sx, sy, s, targets, t_open, stagger=0.012, alpha=1.0, blur=0.0, rest=0.0, flip=False):
    """Kartavirya's arms: one sprite per arm from the shoulder (sx, sy); targets = [(angle, scale)], each sweeping
    from `rest` to its angle (0 = hanging down, pi = up, pi/2 = pointing left) starting at t_open + i*stagger."""
    for i, (th, k) in enumerate(targets):
        q = back(clamp((t - t_open - i * stagger) / 0.32), 1.3) if t_open is not None else 1.0
        a = rest + (th - rest) * q + 0.03 * math.sin(t * 2.3 + i)
        if flip:
            a = -a
        prop(cr, "ka_arm", sx, sy, s * k, a, alpha, blur)


def fan_targets(n, a0, a1, k=1.0):
    return [(a0 + (a1 - a0) * i / max(1, n - 1), k) for i in range(n)]


FAN_OPEN = fan_targets(22, 0.55, 2 * math.pi - 0.55, 1.0) + fan_targets(17, 0.75, 2 * math.pi - 0.75, 0.82)


def big_arm(cr, sx, sy, s, th_up, th_lo, alpha=1.0, blur=0.0):
    """Vali's arm alone, huge (the hook's flash): shoulder at (sx, sy)."""
    cr.save()
    cr.translate(sx, sy)
    cr.rotate(th_up)
    cr.scale(s, s)
    pc.paint_part(cr, "vali_armF_up", alpha, blur)
    cr.translate(0, 150)
    cr.rotate(th_lo)
    pc.paint_part(cr, "vali_armF_lo", alpha, blur)
    cr.restore()


# ------------------------------------------------------------------ sets and marks


def river(cr, t, y0, n, dy=64, speed=70.0, s=0.8, alpha=1.0, phase=0.0):
    """n river strips from y0 downwards, scrolling (speed in design units/s; negative = flowing left)."""
    for k in range(n):
        off = (t * speed * (1 + 0.12 * k) + phase + 47 * k) % R.WAVE_P
        x = 540 + (off - R.WAVE_P / 2) * s
        prop(cr, "rv_waveA" if k % 2 == 0 else "rv_waveB", x, y0 + dy * k, s, alpha=alpha)


def tally(cr, t, x, y, s, shows, ticks=(None, None, None, None), alpha=1.0, labels=None):
    """The tally board: rows DEFEAT 1, DEFEAT 2, ..., RAMA; shows = time each row appears; ticks = tick times."""
    if alpha <= 0.01:
        return
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    pc.paint_part(cr, "rv_tally", alpha)
    cr.restore()
    labs = labels or ("DEFEAT 1", "DEFEAT 2", "...", "RAMA")
    for i, (lab, ts) in enumerate(zip(labs, shows)):
        if ts is None:
            continue
        q = prog(t, ts, 0.25) * alpha
        if q <= 0:
            continue
        ry = y + s * (-195 + 130 * i)
        if lab == "...":
            for k in range(3):
                cr.set_source_rgba(*INK, q)
                cr.arc(x + s * (-60 + 60 * k), ry, 9 * s, 0, 2 * math.pi)
                cr.fill()
            continue
        bx = x + s * (-300)
        cr.set_source_rgba(*INK, 0.9 * q)
        cr.set_line_width(max(2.5, 7 * s))
        cr.rectangle(bx, ry - 36 * s, 72 * s, 72 * s)
        cr.stroke()
        col = RED if lab == "RAMA" else INK
        draw_text(cr, lab, x + s * (-196), ry + 18 * s * (1 - q), int(88 * s), col, q, anchor="lm")
        if ticks[i] is not None:
            tick(cr, bx + 8 * s, ry - 2 * s, 76 * s, prog(t, ticks[i], 0.3), RED, alpha)


def note(cr, t, x, y, s, t_in, lines=(), stamp_t=None, alpha=1.0, rot=-0.03):
    """The curse note: title, lines (text, t_show), and the red stamp."""
    p = back(clamp((t - t_in) / 0.35), 1.4) if t_in is not None else 1.0
    a = clamp(p) * alpha
    if a <= 0.01:
        return
    yy = y + 60 * (1 - p)
    cr.save()
    cr.translate(x, yy)
    cr.rotate(rot)
    cr.scale(s, s)
    pc.paint_part(cr, "rv_note", a)
    draw_text(cr, "SPOKEN AT KAILASA", 0, -170, 40, INK, a, MONO_FONT, "ct", tracking=6)
    for i, (txt, ts) in enumerate(lines):
        q = prog(t, ts, 0.25) * a
        if q > 0:
            draw_text(cr, txt, 0, -86 + 86 * i + 14 * (1 - q), 76, INK, q, anchor="ct")
    cr.restore()
    if stamp_t is not None:
        stamp(cr, t, stamp_t, "MONKEYS WILL END YOUR CLAN", x, yy + 175 * s, int(44 * s / 0.95), rot=-0.05,
              alpha=alpha)


def dotted(cr, pts, p, gap=28.0, r=6.5, color=RED, alpha=1.0):
    """Dots along a polyline, revealed to fraction p of its length."""
    if p <= 0 or alpha <= 0.01:
        return
    lens = [math.dist(a, b) for a, b in zip(pts, pts[1:])]
    total = sum(lens) * clamp(p)
    d, i, acc = 0.0, 0, 0.0
    cr.set_source_rgba(*color, 0.9 * alpha)
    while d <= total and i < len(lens):
        while i < len(lens) and acc + lens[i] < d:
            acc += lens[i]
            i += 1
        if i >= len(lens):
            break
        f = (d - acc) / lens[i] if lens[i] else 0
        a, b = pts[i], pts[i + 1]
        cr.arc(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f, r, 0, 2 * math.pi)
        cr.fill()
        d += gap


def arc_pts(cx, cy, rx, ry, a0, a1, n=80):
    return [(cx + rx * math.cos(a0 + (a1 - a0) * i / n), cy + ry * math.sin(a0 + (a1 - a0) * i / n))
            for i in range(n + 1)]


def rope_line(cr, p0, p1, sag=50.0, alpha=1.0):
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2 + sag
    for w, col in ((12, INK), (7, ROPE_C)):
        cr.set_source_rgba(*col, alpha)
        cr.set_line_width(w)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.move_to(*p0)
        cr.curve_to(mx, my, mx, my, *p1)
        cr.stroke()


def flames(cr, t, pts, s=0.35, alpha=1.0):
    for i, (x, y) in enumerate(pts):
        f = int(t * 10 + i * 3) % 3
        prop(cr, f"flame{f}", x, y, s * (0.9 + 0.15 * math.sin(t * 7 + i)), alpha=alpha)


def compass(cr, t, x, y, letter, t_tick, alpha=1.0, size=58):
    """A leather disc with an ocean's letter; ticked when Vali does his sandhya there."""
    cr.save()
    cr.set_source_rgba(0.98, 0.88, 0.62, alpha)
    cr.arc(x, y, 46, 0, 2 * math.pi)
    cr.fill_preserve()
    cr.set_source_rgba(*INK, alpha)
    cr.set_line_width(5)
    cr.stroke()
    cr.restore()
    draw_text(cr, letter, x, y + 2, size, INK, alpha, anchor="cm")
    if t_tick is not None:
        q = prog(t, t_tick, 0.3)
        if q > 0:
            glow(cr, x, y, 120, 0.5 * math.exp(-2.5 * max(0, t - t_tick)))
            tick(cr, x + 18, y - 4, 64, q, RED, alpha)


# ------------------------------------------------------------------ scenes (cr, t, tl, t0, t1) -> dict


def s_hook(cr, t, tl, t0, t1):
    tG = cue(tl, "r1", {"hi": "देवता", "kn": "ದೇವತೆ"}, 0.15)
    tM = cue(tl, "r1", {"hi": "वानर", "kn": "ವಾನರ"}, 0.45)
    tB = cue(tl, "r1", {"hi": "बगल", "kn": "ಕಂಕುಳ"}, 0.55)
    tS = cue(tl, "r1", {"hi": "समुद्र", "kn": "ಸಮುದ್ರ"}, 0.8)
    tS = max(tS, tB + 1.0)
    fl = 0.0
    if t < tS:
        s = 0.94
        # the roar on "gods": the fist goes up, the heads throw back and shake
        up = keyed(t, [(0.0, 0.0), (tG - 0.1, 1.0)], 0.3, 1.5)
        roar = clamp((t - tG) / 0.2) * (1 - clamp((t - tG - 1.3) / 0.3)) if t > tG else 0.0
        mood = "laugh" if 0.05 < roar else "calm"
        grab = ease((t - tB) / 0.4) if t > tB else 0.0
        hx = 560 - 190 * grab
        hy = 1745 - 434 * s - 175 * grab
        rot = math.pi / 2 * back(clamp((t - tB) / 0.35), 1.3) if t > tB else 0.0
        if t > tB:
            ang = rv_angles(t, front=(-1.4 + 0.6 * math.sin(t * 9), -0.5), backa=(-0.8 + 0.5 * math.sin(t * 8), -0.4),
                            legs=(-1.2 * grab + 0.3 * math.sin(t * 6.5), -1.4 * grab + 0.3 * math.sin(t * 7.3)))
        else:
            ang = rv_angles(t, front=(-0.5 - 1.55 * up, -1.2 + 0.2 * up), backa=(0.3 - 0.9 * up, -1.6 + 0.6 * up),
                            head=-0.25 * roar, hits=[(tG, 1.0)])
        sq = ease((t - tB - 0.2) / 0.3) if t > tB else 0.0
        b = 6 * math.sin(math.pi * clamp((t - tB) / 0.35)) if t > tB else 0.0
        pts = rv(cr, t, hx, hy, s * (1 - 0.18 * grab), rot, ang=ang, mood="calm" if t > tB else mood,
                 jig=roar + 0.3 * grab, squash=sq, look=0.0, blur=b, rods=t < tB)
        if t > tB:
            q = back(clamp((t - tB + 0.08) / 0.35), 1.2)
            big_arm(cr, 1190, 890, 2.5, -2.4 + (2.4 + 0.86) * q, 0.78 * q + 0.04 * math.sin(t * 3),
                    blur=4 * (1 - clamp((t - tB) / 0.3)))
            fl = 0.45 * math.exp(-5 * max(0, t - tB))
        if 0 < roar:
            sound_rings(cr, pts["head"][0], pts["head"][1] - 120, t, tG, 4, 0.3, 480)
    else:
        # zoomed out: the dotted loop round the four oceans, Vali carrying Ravana round it
        cx, cy, rx, ry = 540, 1150, 380, 380
        p = clamp((t - tS) / max(0.8, t1 - tS - 0.2))
        a0 = math.pi / 2
        loop = arc_pts(cx, cy, rx, ry, a0, a0 + 2 * math.pi, 120)
        dotted(cr, loop, ease(p) * 0.999, 30, 7)
        for i, (wx, wy) in enumerate(((cx, cy + ry), (cx - rx, cy), (cx, cy - ry), (cx + rx, cy))):
            q = prog(t, tS + 0.15 * i, 0.3)
            cr.save()
            cr.rectangle(wx - 110, wy - 40, 220, 90)
            cr.clip()
            river(cr, t, wy - 6, 2, 26, 60, 0.75, alpha=q)
            cr.restore()
        a = a0 + 2 * math.pi * ease(p)
        vx, vy = cx + rx * math.cos(a), cy + ry * math.sin(a)
        vali_carry(cr, t, vx, vy + 60, 0.30, rot=0.12 * math.sin(t * 2), fly=1.0, rods=False)
        fl = 0.3 * math.exp(-5 * max(0, t - tS))

    def ui(cr):
        small_line(cr, t, [("RAVANA,", -1.0), ("CARRIED", -1.0), ("BY", -1.0), ("A", -1.0)], 245, 62)
        big_word(cr, t, "MONKEY", 0.45, 323, 190, ghost_from=-1.0, under=tM)
    return dict(ui=ui, flash=fl)


def s_source(cr, t, tl, t0, t1):
    tX = cue(tl, "r2", {"hi": "नहीं", "kn": "ಅಲ್ಲ"}, 0.3)
    tB = cue(tl, "r2", {"hi": "वाल्मीकि", "kn": "ವಾಲ್ಮೀಕಿ"}, 0.5)
    tU = cue(tl, "r2", {"hi": "उत्तर", "kn": "ಉತ್ತರ"}, 0.72)
    # the flying pair crosses the bottom while the title is crossed out, then the palm-leaf book rises
    fx = 1250 - 1500 * clamp((t - t0) / max(1.0, tB - t0))
    if t < tB + 0.2:
        vali_carry(cr, t, fx, 1500 + 30 * math.sin(t * 3), 0.42, rot=-0.08, fly=1.0, rods=False,
                   alpha=1 - prog(t, tB, 0.25))
    b, k, a = depth(t, tB - 0.2, 0.5)
    by = 1040 + 620 * (1 - ease((t - tB + 0.2) / 0.5))
    if t > tB - 0.25:
        cr.save()
        cr.translate(540, by)
        cr.rotate(-0.04 + sway(t, 0.02, 0.4))
        cr.scale(1.3 * k, 1.3 * k)
        pc.paint_part(cr, "book", a, b)
        if t > tB + 0.2:
            q = prog(t, tB + 0.2, 0.3) * a
            draw_text(cr, "VALMIKI", 0, -40, 66, INK, q, anchor="cm")
            draw_text(cr, "RAMAYANA", 0, 22, 66, INK, q, anchor="cm")
        cr.restore()
        pc.rod(cr, 540 - 280, by + 140, 400, H + 60, alpha=a)
        pc.rod(cr, 540 + 280, by + 140, 700, H + 60, alpha=a)

    def ui(cr):
        draw_text(cr, "NOT A", W / 2, 300, 66, INK, prog(t, t0 + 0.05, 0.2), anchor="ct")
        struck = t > tX + 0.3
        bx, byy, bw, bh = big_word(cr, t, "FILM SCENE", t0 + 0.15, 380, 170, color=FADE if struck else INK)
        if t > tX:
            red_cross(cr, W / 2, byy + bh / 2, min(bw, bh * 1.8), prog(t, tX, 0.3))
        stamp(cr, t, tU, "UTTARA KANDA", W / 2, by + 260, 80, rot=-0.06)
        if t > tU + 0.3:
            draw_text(cr, "THE LAST BOOK OF THE RAMAYANA", W / 2, by + 362, 30, INK, prog(t, tU + 0.3, 0.3),
                      MONO_FONT, "ct", tracking=3)
    return dict(ui=ui)


def s_tally(cr, t, tl, t0, t1):
    tRa = cue(tl, "r3", {"hi": "राम", "kn": "ರಾಮ"}, 0.08)
    t1st = cue(tl, "r3", {"hi": "एक", "kn": "ಒಂದ"}, 0.45)
    t2nd = cue(tl, "r3", {"hi": "दो", "kn": "ಎರಡು"}, 0.62)
    tL = cue(tl, "r3", {"hi": "हार", "kn": "ಸೋತಿದ್ದ"}, 0.8)
    tally(cr, t, 540, 880, 0.8, (t1st, t2nd, t2nd + 0.15, tRa + 0.1), alpha=prog(t, t0, 0.25))
    droop = keyed(t, [(t0, 0.0), (tL, 1.0)], 0.35, 1.5)
    shake = 0.12 * math.sin((t - t1st) * 16) * math.exp(-3 * max(0, t - t1st)) * (t > t1st)
    ang = rv_angles(t, front=(-0.2 + 0.1 * droop, -0.4), backa=(0.2, -0.3), head=0.28 * droop + shake,
                    hits=[(tL, 0.8)])
    rv(cr, t, 540, 1790 - 434 * 0.46, 0.46, bob_rot(t, 1) + 0.05 * droop, ang=ang, look=0.25 * droop + shake)

    def ui(cr):
        head2(cr, t, "BEFORE RAMA, RAVANA LOST", t0 + 0.05, "TWICE", t2nd, big_size=170, under=tL)
    return dict(ui=ui)


KINGS_MAP = ((-330, -150), (-150, 40), (30, -170), (190, 70), (340, -110))


def s_conquer(cr, t, tl, t0, t1):
    tV = cue(tl, "r4", {"hi": "वरदान", "kn": "ಸಿಕ್ಕ"}, 0.25)
    tW = cue(tl, "r4", {"hi": "दुनिया", "kn": "ಲೋಕ"}, 0.65)
    ms, mx, my = 0.86, 540, 930
    b, k, a = depth(t, t0, 0.45)
    prop(cr, "rv_map", mx, my, ms * k, rot=sway(t, 0.006, 0.3), alpha=a, blur=b)
    pc.rod(cr, mx - 380, my - 300 * ms, 300, H + 60, alpha=0.5 * a)
    pc.rod(cr, mx + 380, my - 300 * ms, 780, H + 60, alpha=0.5 * a)
    t_march0 = max(tW - 0.5, t0 + 0.6)
    t_march1 = t1 + 0.6
    x0, x1 = 240, 1300
    rx = x0 + (x1 - x0) * clamp((t - t_march0) / (t_march1 - t_march0))
    for i, (kx, ky) in enumerate(KINGS_MAP):
        X, Y = mx + kx * ms, my + ky * ms
        tf = t_march0 + (t_march1 - t_march0) * clamp((X - 40 - x0) / (x1 - x0))
        q = ease((t - tf) / 0.35) if t > tf else 0.0
        prop(cr, f"kingS{i}", X + 30 * q, Y + 10 * q, 1.25, rot=1.35 * q * (1 if i % 2 else -1) + sway(t, 0.03, 0.8, i),
             alpha=1 - 0.45 * q)
        if t > tf:
            u = clamp((t - tf) / 0.9)
            cx = X + 60 * u * (1 if i % 2 else -1)
            cy = Y - 130 - 160 * math.sin(math.pi * min(u, 0.5)) + 500 * max(0, u - 0.5) ** 2
            prop(cr, "rv_crown", cx, cy, 0.9, rot=6 * u * (1 if i % 2 else -1), alpha=1 - clamp((u - 0.75) / 0.25))
    ground(cr)
    boon = prog(t, tV, 0.4) * (1 - 0.6 * prog(t, t_march0 + 0.6, 0.6))
    if t < t_march0:
        glow(cr, x0, 1180, 330, 0.65 * boon * (0.85 + 0.15 * math.sin(t * 4)))
        ang = rv_angles(t, front=(-0.6 - 1.6 * boon, -0.6), backa=(-0.3 - 1.4 * boon, -0.5), head=-0.15 * boon)
        rv(cr, t, x0, man_y(0.6), 0.6, bob_rot(t, 2), ang=ang, jig=0.0)
    else:
        rv_walk(cr, t, t_march0, t_march1, x0, x1, 0.6, mood="angry", front=(-1.6, -0.5), backa=(0.4, -0.4),
                step=0.38)

    def ui(cr):
        if t < tW:
            head2(cr, t, "AFTER A BOON FROM", t0 + 0.05, "BRAHMA", tV - 0.1, big_size=170)
        else:
            head2(cr, t, "HE SET OUT TO", tW, "CONQUER THE WORLD", tW + 0.1, big_size=150)
        if tV < t < t_march0 + 0.3:
            tag(cr, t, tV + 0.2, "BRAHMA'S BOON", 300, 560 + 0, 36, t_out=t_march0)
    return dict(ui=ui, flash=0.3 * math.exp(-4 * max(0, t - tV)) * (t > tV))


def nandi(cr, t, x, s, block=0.0, raise_=0.0, alpha=1.0, blur=0.0, hits=()):
    """Nandi facing left, trident in hand; block 0..1 = the trident swung across the path."""
    ang = man_angles("nandi", t, front=(-1.0 - 0.5 * raise_, -1.1 + 0.4 * block), backa=(0.2 - 1.9 * raise_,
                     -0.4 - 0.3 * raise_), head=0.0, hits=hits, ph=2.0)
    pts = puppet(cr, R.NANDI, x, man_y(s), s, bob_rot(t, 3), flip=True, angles=ang, alpha=alpha, blur=blur)
    hx, hy = pts["handF"]
    prop(cr, "rv_trident", hx, hy, s * 0.95, rot=-0.1 - 0.75 * block, alpha=alpha, blur=blur, flip=True)
    return pts


def s_kailasa(cr, t, tl, t0, t1):
    tS = cue(tl, "r5", {"hi": "रोका", "kn": "ತಡೆದ"}, 0.22)
    tF = cue(tl, "r5", {"hi": "चेहरा", "kn": "ಮುಖ"}, 0.5)
    tL = cue(tl, "r5", {"hi": "हँस", "kn": "ನಕ್ಕು"}, 0.86)
    b, k, a = depth(t, t0, 0.5)
    prop(cr, "rv_kailasa", 540, FEET + 20, 0.86 * k, alpha=a, blur=b)
    ground(cr)
    block = keyed(t, [(t0, 0.0), (tS - 0.15, 1.0)], 0.25, 1.8)
    np_ = nandi(cr, t, 800, 0.66, block, hits=[(tS, 1.0)])
    laugh = clamp((t - tL) / 0.15) if t > tL else 0.0
    walk_end = min(tS, t0 + 1.6)
    if t < walk_end:
        rv_walk(cr, t, t0, walk_end, -160, 330, 0.62, front=(-0.9, -0.8))
    else:
        ang = rv_angles(t, front=(-0.6 - 0.9 * laugh, -1.4 + 0.6 * laugh), backa=(0.5 - 0.3 * laugh, -1.8),
                        head=-0.4 * laugh, hits=[(walk_end, 1.2), (tL, 1.0)])
        pts = rv(cr, t, 330, man_y(0.62), 0.62, bob_rot(t, 1) - 0.08 * laugh + 0.03 * laugh * math.sin(t * 20),
                 ang=ang, mood="laugh" if laugh > 0 else "calm", jig=1.2 * laugh)
        if laugh > 0:
            sound_rings(cr, pts["head"][0], pts["head"][1] - 100, t, tL, 5, 0.26, 360)
    fx, fy = np_["head"]

    def ui(cr):
        if t < tF:
            head2(cr, t, "AT KAILASA, STOPPED BY", t0 + 0.05, "NANDI", tS, big_size=190)
        elif t < tL:
            head2(cr, t, "HIS FACE: LIKE A", tF, "VANARA'S", tF + 0.1, big_size=180)
            red_ring(cr, fx - 4, fy - 6, 120, 130, prog(t, tF + 0.15, 0.4), 9)
        else:
            head2(cr, t, "AND RAVANA", tL, "LAUGHED", tL + 0.05, big_size=190)
    return dict(ui=ui)


def s_curse(cr, t, tl, t0, t1):
    tC = cue(tl, "r6", {"hi": "श्राप", "kn": "ಶಾಪ"}, 0.1)
    tV = cue(tl, "r6", {"hi": "वानर", "kn": "ವಾನರರು"}, 0.4)
    tN = cue(tl, "r6", {"hi": "नाश", "kn": "ನಾಶ"}, 0.85)
    glow(cr, 880, 1140, 330, 0.5 * prog(t, tC, 0.4) * (0.85 + 0.15 * math.sin(t * 3)))
    raise_ = keyed(t, [(t0, 0.0), (tC, 1.0)], 0.3, 1.6)
    nandi(cr, t, 880, 0.62, 1.0, raise_, hits=[(tC, 0.6)])
    frozen = 1 - clamp((t - t0) / 0.5)
    ang = rv_angles(t, front=(-0.9, -1.0), backa=(0.8, -1.4), head=-0.3 * frozen + 0.1 * prog(t, tN, 0.4))
    rv(cr, t, 190, man_y(0.55), 0.55, bob_rot(t, 1), ang=ang, mood="laugh" if frozen > 0.3 else "calm",
       jig=frozen, look=0.25 * prog(t, tN, 0.4))
    for i in range(6):
        ts = tV + 0.14 * i
        q = back(clamp((t - ts) / 0.4), 1.4)
        if q > 0:
            vanara(cr, t, 95 + 178 * i, 2060 - 170 * q, 0.34, flip=True, raise_=0.6 * (i % 2), ph=i * 1.3,
                   alpha=clamp(q))

    def ui(cr):
        head2(cr, t, "NANDI'S", t0 + 0.05, "CURSE", tC, big_size=190)
        note(cr, t, 540, 790, 0.92, tC + 0.1, [("VANARAS LIKE ME", tV), ("WILL BE BORN...", tV + 0.3)], tN)
    return dict(ui=ui, night=0.12)


BANK = FEET - 190                       # the Narmada scenes stand higher, so the river below reads clearly
LX, LS = 700, 0.88                       # the linga on the bank


def offer_flowers(cr, t, t_fl, n=4):
    """Times and resting places of the marigolds offered on the linga (scene coordinates)."""
    spots = ((662, BANK - 239), (716, BANK - 251), (690, BANK - 279), (744, BANK - 217))
    return [(t_fl + 0.28 * i, spots[i]) for i in range(n)]


def linga(cr, t, t_in=None, alpha=1.0):
    b, k, a = depth(t, t_in, 0.5) if t_in is not None else (0.0, 1.0, 1.0)
    glow(cr, LX, BANK - 140, 260, 0.35 * a)
    prop(cr, "rv_linga", LX, BANK + 4, LS * k, alpha=a * alpha, blur=b)


def s_narmada(cr, t, tl, t0, t1):
    tN = cue(tl, "r7", {"hi": "नर्मदा", "kn": "ನರ್ಮದಾ"}, 0.2)
    tLi = cue(tl, "r7", {"hi": "शिवलिंग", "kn": "ಶಿವಲಿಂಗ"}, 0.6)
    tFl = cue(tl, "r7", {"hi": "फूल", "kn": "ಹೂವು"}, 0.8)
    ground(cr, y=BANK + 6)
    if t > tLi - 0.1:
        linga(cr, t, tLi - 0.1)
    offers = offer_flowers(cr, t, tFl)
    reach = 0.0
    for i, (ti, (fx, fy)) in enumerate(offers):
        reach = max(reach, math.exp(-4 * max(0, t - ti)) * (t > ti - 0.3))
    ang = rv_angles(t, front=(-1.15 - 0.35 * reach, -0.45 + 0.2 * reach), backa=(-0.5, -1.6),
                    head=0.12, hits=[(ti, 0.4) for ti, _ in offers])
    s = 0.62
    pts = rv(cr, t, 330, BANK - 250 * s, s, 0.12 + bob_rot(t, 1), ang=ang, kneel=True)
    hx, hy = pts["handF"]
    for i, (ti, (fx, fy)) in enumerate(offers):
        if t < ti - 0.3:
            if i == 0 or t > offers[i - 1][0]:
                prop(cr, f"rv_mari{i % 2}", hx + 10, hy + 6, 0.9)
            continue
        q = ease((t - ti + 0.3) / 0.3)
        x = hx + (fx - hx) * q
        y = hy + (fy - hy) * q - 60 * math.sin(math.pi * q)
        prop(cr, f"rv_mari{i % 2}", x, y, 0.9, rot=0.5 * q)
    rise = ease((t - tN) / 0.5) if t > tN else 0.0
    river(cr, t, BANK + 150 + 450 * (1 - rise), 6, 58, 70, 0.8)

    def ui(cr):
        head2(cr, t, "DEFEAT 1: ON THE BANK OF THE", t0 + 0.05, "NARMADA", tN, big_size=180)
        if t > tLi:
            tag(cr, t, tLi + 0.15, "SHIVA LINGA", LX + 30, BANK - 520, 34)
    return dict(ui=ui)


AX, AS = 640, 0.86                       # Kartavirya Arjuna in the river


def s_arjuna(cr, t, tl, t0, t1):
    tK = cue(tl, "r8", {"hi": "कार्तवीर्य", "kn": "ಕಾರ್ತವೀರ್ಯ"}, 0.3)
    tA = cue(tl, "r8", {"hi": "हज़ार", "kn": "ಸಾವಿರ"}, 0.8)
    river(cr, t, 1290, 1, 60, 70, 0.8, alpha=0.8)
    b, k, a = depth(t, t0, 0.5)
    hy = man_y(AS)
    if t > tA - 0.1:
        ka_fan(cr, t, AX, hy - 262 * AS, AS, FAN_OPEN, tA, alpha=a)
    splash = [t0 + 0.4 + 0.7 * i for i in range(int(max(0, tA - t0) / 0.7) + 1)]
    play = sum(math.exp(-6 * max(0, t - s)) * (t > s) for s in splash)
    ang = man_angles("karta", t, front=(-1.0 - 0.6 * play, -0.6), backa=(-0.4 - 0.5 * play, -0.8), hits=[(s, 0.5)
                     for s in splash])
    puppet(cr, R.KARTA, AX, hy - (k - 1) * 260 * AS, AS * k, bob_rot(t, 4), flip=True, angles=ang, alpha=a, blur=b)
    for i, s0 in enumerate(splash):
        u = (t - s0) / 0.8
        if 0 < u < 1 and s0 < tA:
            for j in range(4):
                dx = (j - 1.5) * 60 - 160
                prop(cr, "rv_drop", AX + dx * (0.5 + u), 1290 - 300 * math.sin(math.pi * u) * (0.7 + 0.1 * j) + 40,
                     1.4, rot=0.4 * (j - 1.5), alpha=1 - u)
    river(cr, t, 1340, 9, 64, 70, 0.8)
    n = int(1000 * ease((t - tA - 0.1) / 1.3) ** 1.5) if t > tA else 0
    fl = 0.35 * math.exp(-4 * max(0, t - tA)) * (t > tA)

    def ui(cr):
        if t < tA:
            head2(cr, t, "KING OF MAHISHMATI", t0 + 0.05, "KARTAVIRYA ARJUNA", tK, big_size=140)
        else:
            head2(cr, t, "HE HAD", tA, f"{max(n, 2)} ARMS", tA + 0.05, big_size=190)
    return dict(ui=ui, flash=fl)


def s_dam(cr, t, tl, t0, t1):
    tA = cue(tl, "r9", {"hi": "हज़ार", "kn": "ಸಾವಿರ"}, 0.45)
    tS = cue(tl, "r9", {"hi": "रोक", "kn": "ತಡೆದು"}, 0.85)
    ax, s = 760, 0.82
    hy = man_y(s)
    sx, sy = ax - 20, hy - 262 * s
    reach = 300 * s
    wall_x = sx - reach
    fwd = keyed(t, [(t0, 0.0), (tA, 1.0)], 0.35, 1.3)
    wall = fan_targets(15, math.pi / 2 - 1.1, math.pi / 2 + 1.1, 1.0)
    targets = [(th + (wt - th) * fwd, kk) for (th, kk), (wt, _) in zip(sorted(FAN_OPEN[:22:3] + FAN_OPEN[1:22:3]), wall)]
    pile = ease((t - tS + 0.2) / 0.9) if t > tS - 0.2 else 0.0
    # upstream water (left of the arc of hands) piles up; downstream (right) runs low
    cr.save()
    cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    cr.rectangle(0, 0, sx, H)
    cr.new_sub_path()
    cr.arc(sx, sy, reach * 0.92, 0, 2 * math.pi)
    cr.clip()
    cr.set_fill_rule(cairo.FILL_RULE_WINDING)
    cr.rectangle(0, 0, sx, H)
    cr.clip()
    lvl = 1300 - 360 * pile
    n = 9 + int(6 * pile)
    for kk in range(n):
        off = (t * 70 * (1 - 0.85 * pile) + 47 * kk) % R.WAVE_P
        prop(cr, "rv_waveA" if kk % 2 == 0 else "rv_waveB", 540 + (off - R.WAVE_P / 2) * 0.8,
             lvl + 64 * kk * (1 - 0.15 * pile), 0.8)
    cr.restore()
    ka_fan(cr, t, sx, sy, s, targets, None)
    ang = man_angles("karta", t, front=(-1.6, -0.2), backa=(-1.4, -0.3), legs=(-0.25, 0.3), hits=[(tA, 0.6)])
    puppet(cr, R.KARTA, ax, hy, s, -0.06 + bob_rot(t, 4), flip=True, angles=ang)
    cr.save()
    cr.rectangle(sx, 0, W, H)
    cr.clip()
    river(cr, t, 1330 + 200 * pile, 9, 64, 70, 0.8)
    cr.restore()

    def ui(cr):
        head2(cr, t, "TO TEST HIS STRENGTH, HE", t0 + 0.05, "STOPPED THE RIVER", tS, big_size=160)
        if t > tS + 0.4:
            red_ring(cr, wall_x - 150, lvl + 160, 200, 210, prog(t, tS + 0.4, 0.45), 9)
    return dict(ui=ui, flash=0.25 * math.exp(-4 * max(0, t - tS)) * (t > tS))


def s_reverse(cr, t, tl, t0, t1):
    tU = cue(tl, "r10", {"hi": "उल्टा", "kn": "ಹಿಂದಕ್ಕೆ"}, 0.2)
    tF = cue(tl, "r10", {"hi": "फूल", "kn": "ಹೂವೆಲ್ಲಾ"}, 0.62)
    tAng = max(tF + 0.5, F(tl, "r10", 0.88))
    ground(cr, y=BANK + 6)
    linga(cr, t)
    up = keyed(t, [(t0, 0.0), (tF + 0.25, 1.0)], 0.35, 1.3)
    s = 0.62
    angry = t > tAng
    hy_k = BANK - 250 * s
    if up < 0.5:
        ang = rv_angles(t, front=(-1.0, -0.6), backa=(-0.5, -1.6), head=0.1 - 0.3 * up)
        rv(cr, t, 330, hy_k - 80 * up, s, 0.12 * (1 - up) + bob_rot(t, 1), ang=ang, kneel=True,
           look=-0.2 * clamp((t - tF) / 0.3))
    else:
        ang = rv_angles(t, front=(-1.4 if angry else -0.9, -1.2 if angry else -0.8), backa=(0.4, -1.4),
                        head=-0.05, hits=[(tF + 0.25, 1.0), (tAng, 0.8)])
        rv(cr, t, 330, BANK - 434 * s, s, bob_rot(t, 1), ang=ang, mood="angry" if angry else "calm",
           jig=0.4 * math.exp(-3 * max(0, t - tAng)) * angry, look=0.0)
    rise = ease((t - tU) / 0.6) if t > tU else 0.0
    surface = BANK + 150 - 90 * rise
    for i, (ti, (fx, fy)) in enumerate(offer_flowers(cr, t, -10)):
        st = tF + 0.18 * i
        u = clamp((t - st) / 1.6)
        if u <= 0:
            prop(cr, f"rv_mari{i % 2}", fx, fy, 0.9, rot=0.5)
            continue
        x = fx + 120 * ease(u * 4) - 900 * max(0.0, u - 0.25) ** 1.2
        y = fy + (surface - 16 - fy) * ease(u * 3) + 10 * math.sin(t * 6 + i)
        prop(cr, f"rv_mari{i % 2}", x, y, 0.9, rot=0.5 + 4 * u)
    river(cr, t, surface, 6, 58, 70 - 170 * rise, 0.8)

    def ui(cr):
        if t < tF:
            head2(cr, t, "THE RIVER FLOWED", t0 + 0.05, "BACKWARDS", tU, big_size=180)
            if t > tU + 0.2:
                pp = prog(t, tU + 0.2, 0.5)
                from poster import path as brush_path
                brush_path(cr, arc_pts(540, BANK + 250, 330, 50, -0.2, -math.pi + 0.2, 30), pp, 12, RED, arrow=True)
        else:
            head2(cr, t, "AND SWEPT AWAY HIS", tF, "FLOWERS", tF + 0.08, big_size=180)
    return dict(ui=ui)


def karta_pose(t, grab=0.0):
    return man_angles("karta", t, front=(-1.5, -0.3), backa=(-1.2 - 0.2 * grab, -0.4), hits=[])


def s_capture(cr, t, tl, t0, t1):
    tG = cue(tl, "r11", {"hi": "पकड़ा", "kn": "ಹಿಡಿದು"}, 0.55)
    tT = cue(tl, "r11", {"hi": "बाँधा", "kn": "ಕಟ್ಟಿ"}, 0.68)
    tC = cue(tl, "r11", {"hi": "राजधानी", "kn": "ರಾಜಧಾನಿ"}, 0.85)
    tT = max(tT, tG + 0.4)
    tC = max(tC, tT + 0.4)
    ground(cr)
    # Mahishmati's gate slides in on the capital cue
    gp = ease((t - tC + 0.1) / 0.5) if t > tC - 0.1 else 0.0
    if gp > 0:
        prop(cr, "wall", 1300 - 330 * gp, FEET + 10, 0.62, alpha=clamp(gp * 2))
    s = 0.8
    drag = clamp((t - tC - 0.2) / max(0.6, t1 - tC))
    ax = 780 + 150 * drag
    hy = man_y(s)
    grab = keyed(t, [(t0, 0.0), (tG - 0.05, 1.0), (tC + 0.2, 0.25)], 0.22, 1.4)
    # the back tier stays fanned out; the front arms swing forward and close on Ravana
    still = FAN_OPEN[22::2]
    grabbers = [(th + ((math.pi / 2 + 0.7 * (th - math.pi) / math.pi) - th) * grab, kk) for th, kk in FAN_OPEN[:22:2]]
    ka_fan(cr, t, ax, hy - 262 * s, s, still + grabbers, None)
    puppet(cr, R.KARTA, ax, hy, s, bob_rot(t, 4) - 0.05 * grab, flip=True,
           angles=man_angles("karta", t, front=(-1.4, -0.4), backa=(-1.1, -0.5), hits=[(tG, 0.6)]))
    rs = 0.6
    charge_end = min(tG - 0.05, t0 + 1.5)
    tied = t > tT
    if t < charge_end:
        rv_walk(cr, t, t0, charge_end, -180, 330, rs, mood="angry", front=(-2.3, -0.4), backa=(-1.2, -0.6),
                step=0.32)
        pts = None
    else:
        lift = 40 * ease((t - tG) / 0.25) * (t > tG) * (1 - drag)
        rx = 330 + 300 * ease((drag - 0.05) / 0.95) * (t > tC)
        hop = -abs(math.sin((t - tC) * 7)) * 22 * (t > tC + 0.2)
        if tied:
            ang = rv_angles(t, front=(-0.15, -0.2), backa=(0.15, -0.2), head=0.1, legs=(0.12, -0.12),
                            hits=[(tT, 0.6)])
        else:
            ang = rv_angles(t, front=(-2.3 + 0.4 * math.sin(t * 12), -0.4), backa=(-1.2 + 0.4 * math.sin(t * 11), -0.6),
                            legs=(-0.3 * math.sin(t * 10), 0.3 * math.sin(t * 10)), hits=[(tG, 1.4)])
        pts = rv(cr, t, rx, man_y(rs) - lift + hop, rs, 0.1 * math.sin(t * 9) * (t < tT) + bob_rot(t, 1) +
                 0.12 * (t > tC), ang=ang, mood="angry", jig=0.25 if not tied else 0.0)
        if tied:
            q = back(clamp((t - tT) / 0.3), 1.4)
            cx, cy = pts["chest"]
            prop(cr, "rv_rope", cx + 8, cy + 30, rs * q * 1.25, rot=0.05)
            if t > tC:
                hx, hy2 = 0, 0
                rope_line(cr, (cx + 90 * rs, cy + 30), (ax - 120 * s, hy - 200 * s), 70)
    fl = 0.4 * math.exp(-5 * max(0, t - tG)) * (t > tG)

    def ui(cr):
        if t < tG:
            head2(cr, t, "IN ANGER, RAVANA WENT TO", t0 + 0.05, "FIGHT", t0 + 0.3, big_size=190)
        elif t < tC:
            head2(cr, t, "CAUGHT AND", tG, "TIED UP", tT, big_size=190)
        else:
            head2(cr, t, "DRAGGED TO HIS CAPITAL", tC, "MAHISHMATI", tC + 0.1, big_size=170)
            tag(cr, t, tC + 0.3, "MAHISHMATI", 1300 - 330 * gp, 1290, 34)
        if t > tC:
            tally(cr, t, 900, 690, 0.34, (tC, tC, tC, tC), (tC + 0.6, None, None, None), alpha=prog(t, tC, 0.3))
    return dict(ui=ui, flash=fl)


def in_hand(sprite, dy=150, rot=0.0, s=1.0):
    """extra= callback drawing a held prop at a forearm's hand."""
    def fn(cr_):
        cr_.save()
        cr_.translate(4, dy)
        cr_.rotate(rot)
        cr_.scale(s, s)
        pc.paint_part(cr_, sprite)
        cr_.restore()
    return fn


def pulastya_walk(cr, t, t0, t1, x0, x1, s, t_in=None, bless=0.0):
    """The sage walks in with his staff; bless 0..1 raises his hand over Ravana."""
    ang = {"pulastya_armF_up": -0.6 - 1.2 * bless + 0.32, "pulastya_armF_lo": -0.4 + 0.55}
    return walker(cr, t, R.PULASTYA, "pulastya", t0, t1, x0, x1, s, angles=ang,
                  extra={"pulastya_armB_lo": in_hand("rv_staff", 150, 0.28)}, t_in=t_in)


def s_pulastya(cr, t, tl, t0, t1):
    tD = cue(tl, "r12", {"hi": "दादा", "kn": "ಅಜ್ಜ"}, 0.25)
    tP = cue(tl, "r12", {"hi": "पुलस्त्य", "kn": "ಪುಲಸ್ತ್ಯ"}, 0.4)
    tR = cue(tl, "r12", {"hi": "छुड़वाना", "kn": "ಬಿಡಿಸ್ಕೊಂಡು"}, 0.75)
    prop(cr, "wall", 760, FEET + 10, 0.62)
    ground(cr)
    s = 0.8
    bow = keyed(t, [(t0, 0.0), (tR - 0.2, 1.0)], 0.4, 1.2)
    puppet(cr, R.KARTA, 935, man_y(s), s, bob_rot(t, 4) + 0.15 * bow, flip=True,
           angles=man_angles("karta", t, front=(-0.8, -1.4), backa=(-0.7, -1.4), head=0.25 * bow), alpha=0.85,
           blur=4)
    free = t > tR
    rs = 0.6
    ang = rv_angles(t, front=(-0.15, -0.2) if not free else (-0.4, -0.5), backa=(0.15, -0.2) if not free else
                    (0.3, -0.3), head=0.2 * (1 - prog(t, tR, 0.4)), legs=(0.12, -0.12), hits=[(tR, 1.0)])
    pts = rv(cr, t, 640, man_y(rs), rs, bob_rot(t, 1), ang=ang, look=0.2 * (1 - prog(t, tR, 0.4)))
    cx, cy = pts["chest"]
    fall = clamp((t - tR) / 0.6)
    if fall < 1:
        prop(cr, "rv_rope", cx + 8, cy + 30 + 360 * fall ** 2, rs * 1.25, rot=0.05 + 0.6 * fall, alpha=1 - fall)
    bless = keyed(t, [(t0, 0.0), (tR - 0.25, 1.0)], 0.3, 1.4)
    glow(cr, 250, 1180, 300, 0.5 * prog(t, tD - 0.2, 0.5) * (0.85 + 0.15 * math.sin(t * 3)) + 0.35 * math.exp(
        -3 * max(0, t - tR)) * free)
    pulastya_walk(cr, t, t0 + 0.1, max(t0 + 1.0, tD), -170, 250, 0.78, t_in=t0, bless=bless)

    def ui(cr):
        if t < tR:
            head2(cr, t, "HIS GRANDFATHER, THE SAGE", t0 + 0.05, "PULASTYA", tP, big_size=190)
            tag(cr, t, tD + 0.1, "GRANDFATHER", 250, 640, 34)
        else:
            head2(cr, t, "HAD TO COME AND", tR, "FREE HIM", tR + 0.08, big_size=190)
    return dict(ui=ui, flash=0.3 * math.exp(-4 * max(0, t - tR)) * free)


def s_rehook(cr, t, tl, t0, t1):
    tB = cue(tl, "r13", {"hi": "बाकी", "kn": "ಬಾಕಿ"}, 0.7)
    puppet(cr, R.VALI, 760, man_y(1.45) + 160, 1.45, bob_rot(t, 2), flip=True,
           angles=vali_angles(t, front=(-1.2, -0.8), backa=(-0.6, -1.0)), alpha=0.5, blur=22, rods=False)
    ground(cr)
    ang = rv_angles(t, front=(-0.4, -0.9), backa=(0.5, -1.2), head=0.0)
    rv(cr, t, 330, man_y(0.6), 0.6, bob_rot(t, 1), ang=ang, look=0.18 * math.sin(t * 2.5))

    def ui(cr):
        head2(cr, t, "THE REAL HUMILIATION WAS", t0, "STILL TO COME", t0 + 0.12, big_size=160)
        stamp(cr, t, tB, "DEFEAT 2", W / 2, 720, 110, rot=-0.07)
    return dict(ui=ui, night=0.45 + 0.2 * prog(t, t0, 0.6), flash=0.3 * math.exp(-5 * max(0, t - tB)) * (t > tB))


def s_vali(cr, t, tl, t0, t1):
    tV = cue(tl, "r14", {"hi": "वाली", "kn": "ವಾಲಿ"}, 0.35)
    tS = cue(tl, "r14", {"hi": "ताक़तवर", "kn": "ಶಕ್ತಿಶಾಲಿ"}, 0.5)
    tG = cue(tl, "r14", {"hi": "सीधा", "kn": "ಸೀದಾ"}, 0.65)
    tK = cue(tl, "r14", {"hi": "किष्किंधा", "kn": "ಕಿಷ್ಕಿಂಧೆ"}, 0.2)
    tS = max(tS, tV + 0.6)
    bt, kt, at = depth(t, tK - 0.2, 0.5)
    prop(cr, "tree", 980, FEET + 10, 0.62 * kt, rot=sway(t, 0.006, 0.3), alpha=0.75 * at, blur=6 + bt)
    prop(cr, "tree", 60, FEET + 10, 0.5 * kt, rot=sway(t, 0.006, 0.3, 1), alpha=0.6 * at, blur=8 + bt, flip=True)
    ground(cr)
    if t < tV - 0.15:                       # far away first: a big soft shadow walking closer
        x_far = 900 - 120 * clamp((t - t0) / max(0.5, tV - t0))
        puppet(cr, R.VALI, x_far, man_y(1.2) + 150, 1.2, bob_rot(t, 2), flip=True,
               angles=vali_angles(t, front=(-0.6, -0.6)), alpha=0.35 * prog(t, t0 + 0.3, 0.5), blur=20, rods=False)
    if t > tV - 0.15:
        b, k, a = depth(t, tV - 0.15, 0.5)
        flex = keyed(t, [(t0, 0.0), (tS, 1.0)], 0.3, 1.6)
        ang = vali_angles(t, front=(-0.5 - 2.1 * flex, -0.4 - 1.4 * flex), backa=(0.2, -0.4),
                          hits=[(tS, 0.5)])
        glow(cr, 720, 1050, 360, 0.35 * a)
        pts = puppet(cr, R.VALI, 720, man_y(0.95) - (k - 1) * 280, 0.95 * k, bob_rot(t, 2), flip=True, angles=ang,
                     alpha=a, blur=b)
        if t > tS:
            sound_rings(cr, pts["handF"][0], pts["handF"][1], t, tS, 3, 0.28, 260)
    if t < tG:
        ang = rv_angles(t, front=(-0.4, -0.9), backa=(0.3, -1.6), head=-0.05)
        rv(cr, t, 250, man_y(0.6), 0.6, bob_rot(t, 1), ang=ang, look=0.2 * math.sin(t * 2.2) * (t < tV))
        if tK < t < tV + 0.3:
            sound_rings(cr, 330, 1000, t, tK, 3, 0.35, 220)
    else:
        rv_walk(cr, t, tG, tG + 1.4, 250, 410, 0.6, mood="angry", front=(-2.2, -0.4), backa=(0.4, -0.6), step=0.35)

    def ui(cr):
        if t < tG:
            head2(cr, t, "KING OF KISHKINDHA", t0 + 0.05, "VALI", tV, big_size=200)
            tag(cr, t, tK, "KISHKINDHA", 300, 640, 36)
            if t > tS:
                stamp(cr, t, tS + 0.1, "VERY STRONG", 760, 640, 56, rot=0.05)
        else:
            head2(cr, t, "RAVANA WENT STRAIGHT TO", tG, "FIGHT HIM", tG + 0.08, big_size=190)
    return dict(ui=ui)


VX, VS = 620, 0.86                      # Vali at the southern ocean (on the shore, the sea below)


def sea_set(cr, t):
    glow(cr, 955, 1335, 320, 0.45)
    prop(cr, "sun", 955, 1335, 0.48, rot=t * 0.05)
    ground(cr, y=BANK + 6)
    river(cr, t, BANK + 150, 6, 58, 40, 0.8)


def vali_seated(cr, t, alpha=1.0):
    hy = BANK - 112 * VS
    prop(cr, "vali_sit", VX, hy, VS, alpha=alpha)
    ang = vali_angles(t, front=(-0.75, -1.85), backa=(-0.8, -1.8), head=0.05)
    return puppet(cr, R.VALI, VX, hy, VS, bob_rot(t, 2) * 0.5, angles=ang, alpha=alpha,
                  hide=("vali_legF", "vali_legB"))


def s_sandhya(cr, t, tl, t0, t1):
    tY = cue(tl, "r15", {"hi": "संध्या", "kn": "ಸಂಧ್ಯಾ"}, 0.35)
    tC = cue(tl, "r15", {"hi": "चुपके", "kn": "ಸದ್ದಿಲ್ಲದೆ"}, 0.6)
    sea_set(cr, t)
    glow(cr, VX + 40, BANK - 330, 330, 0.45 * prog(t, tY - 0.2, 0.5) * (0.85 + 0.15 * math.sin(t * 2.5)))
    vali_seated(cr, t)
    if t > tC - 0.2:
        rv_walk(cr, t, tC - 0.2, t1 + 0.2, -170, 290, 0.62, front=(-1.1, -1.0), backa=(0.9, -0.8), step=0.6,
                lift=1.0, lean=0.12, feet=BANK)

    def ui(cr):
        if t < tC:
            head2(cr, t, "AT THE SOUTHERN OCEAN, VALI'S", t0 + 0.05, "SANDHYA", tY, big_size=190)
            if t > tY + 0.3:
                draw_text(cr, "TWILIGHT PRAYER", W / 2, 530, 34, INK, prog(t, tY + 0.3, 0.3), MONO_FONT, "ct",
                          tracking=4)
        else:
            head2(cr, t, "RAVANA CREPT UP", tC, "FROM BEHIND", tC + 0.08, big_size=180)
    return dict(ui=ui, night=0.06)


def s_snatch(cr, t, tl, t0, t1):
    tG = cue(tl, "r16", {"hi": "पकड़ा", "kn": "ಹಿಡಿದು"}, 0.55)
    tT = cue(tl, "r16", {"hi": "बगल", "kn": "ಕಂಕುಳ"}, 0.85)
    tT = max(tT, tG + 0.45)
    sea_set(cr, t)
    rs0 = 0.62                                         # Ravana's size while creeping (as in r15)
    if t < tG:
        vali_seated(cr, t)
        x = hop_walk(t, t0 - 0.2, tG, 290, 410, 0.6)[0]
        ang = rv_angles(t, front=(-1.5, -0.5), backa=(0.9, -0.8))
        rv(cr, t, x, BANK - 434 * rs0 - 10, rs0, 0.12 + bob_rot(t, 1), ang=ang)
        fl = 0.0
    else:
        q = back(clamp((t - tG) / 0.28), 1.3)
        sq = ease((t - tT) / 0.25) if t > tT else 0.0
        grip = 0.4 + 0.6 * sq
        hy = BANK - 434 * VS + 322 * VS * (1 - q)       # springs up from sitting to standing
        # Ravana is pulled from behind Vali's back to under his arm
        tx, ty = TUCK_XY(VS)
        rx = (410 - VX) * (1 - q) + tx * q
        ry = (BANK - 434 * rs0 - hy) * (1 - q) + ty * q
        bump = 1 + 0.04 * math.exp(-6 * max(0, t - tT)) * (t > tT)
        vali_carry(cr, t, VX, hy, VS * bump, squash=sq, grip=grip, rv_rot=math.pi / 2 * q, rv_xy=(rx, ry),
                   rv_s=rs0 + (0.62 * VS - rs0) * q, flail=0.4 + 0.6 * q,
                   blur=5 * math.sin(math.pi * clamp((t - tG) / 0.28)))
        fl = 0.5 * math.exp(-5 * max(0, t - tG)) + 0.3 * math.exp(-5 * max(0, t - tT)) * (t > tT)

    def ui(cr):
        if t < tT:
            head2(cr, t, "SNAP! VALI", tG, "GRABBED HIM", tG + 0.05, big_size=190)
        else:
            head2(cr, t, "AND TUCKED HIM UNDER HIS", tT, "ARMPIT", tT + 0.05, big_size=200)
    return dict(ui=ui, flash=fl, night=0.06)


OM = (540, 1110, 0.88)                  # the ocean map: centre and scale
OR = 300                                 # flight radius on screen


def s_oceans(cr, t, tl, t0, t1):
    tW = cue(tl, "r17", {"hi": "पश्चिम", "kn": "ಪಶ್ಚಿಮ"}, 0.2)
    tN = cue(tl, "r17", {"hi": "उत्तर", "kn": "ಉತ್ತರ"}, 0.3)
    tE = cue(tl, "r17", {"hi": "पूर्व", "kn": "ಪೂರ್ವ"}, 0.4)
    tSa = cue(tl, "r17", {"hi": "संध्या", "kn": "ಸಂಧ್ಯಾ"}, 0.6)
    tD = cue(tl, "r17", {"hi": "रावण", "kn": "ರಾವಣ"}, 0.78)
    tW, tN, tE = max(tW, t0 + 0.6), max(tN, tW + 0.6), max(tE, tN + 0.6)
    tSa = max(tSa, tE + 0.6)
    tD = max(tD, tSa + 0.8)
    cx, cy, ms = OM
    dim = 1 - 0.65 * prog(t, tD - 0.1, 0.35)
    b, k, a = depth(t, t0, 0.45)
    prop(cr, "rv_omap", cx, cy, ms * k, rot=sway(t, 0.004, 0.25), alpha=a * dim, blur=b)
    keys = [(t0 + 0.1, math.pi / 2), (tW, math.pi), (tN, 1.5 * math.pi), (tE, 2 * math.pi),
            (max(tSa, tE + 0.6), 2.5 * math.pi)]
    ang = keys[0][1]
    for (ta, aa), (tb, ab) in zip(keys, keys[1:]):
        if t >= ta:
            ang = aa + (ab - aa) * ease(clamp((t - ta) / (tb - ta)) ** 1.2) if t < tb else ab
    path = arc_pts(cx, cy, OR, OR, math.pi / 2, ang, 90) if ang > math.pi / 2 + 1e-3 else [(cx, cy + OR)] * 2
    dotted(cr, path, 1.0, 26, 6.5, alpha=dim)
    letters = (("S", math.pi / 2, t0 + 0.3), ("W", math.pi, tW), ("N", 1.5 * math.pi, tN), ("E", 0.0, tE))
    vx, vy = cx + OR * math.cos(ang), cy + OR * math.sin(ang)
    big = prog(t, tD - 0.1, 0.35)
    if big < 1:
        vali_carry(cr, t, vx, vy + 70, 0.32, rot=0.1 * math.sin(t * 2.2), fly=1.0, rods=False, alpha=dim)

    def ui(cr):
        for i, (lt, la, tt) in enumerate(letters):
            lx, ly = cx + (OR + 120) * math.cos(la), cy + (OR + 120) * math.sin(la)
            if t > tSa:                           # sandhya done at all four: each disc glows in turn
                glow(cr, lx, ly, 150, 0.6 * math.exp(-3 * max(0, t - tSa - 0.15 * i)) * (t > tSa + 0.15 * i))
            compass(cr, t, lx, ly, lt, tt, alpha=a * dim)
        if t < tW:
            head2(cr, t, "THEN VALI", t0 + 0.05, "FLEW OFF", t0 + 0.15, big_size=190)
        elif t < tSa:
            word = "WEST" if t < tN else "NORTH" if t < tE else "EAST"
            tw = tW if t < tN else tN if t < tE else tE
            head2(cr, t, "SANDHYA AT EVERY OCEAN:", tW, word, tw, big_size=200)
        elif t < tD:
            head2(cr, t, "SANDHYA AT EVERY OCEAN:", tW, "ALL FOUR", tSa, big_size=200)
            red_ring(cr, cx, cy, OR + 175, OR + 175, prog(t, tSa + 0.2, 0.6), 9)
        else:
            head2(cr, t, "RAVANA DANGLING", tD, "ALL THE WAY", tD + 0.08, big_size=190)
        if big > 0:
            u = (t - tD + 0.1) / max(1.0, t1 - tD + 0.6)
            x = 1350 - 1700 * clamp(u)
            vali_carry(cr, t, x, 1250 + 30 * math.sin(t * 3), 0.8, rot=-0.08, fly=1.0, rods=False, flail=1.4,
                       alpha=clamp(big * 2))
            for i in range(5):
                yy = 1050 + 90 * i
                cr.set_source_rgba(*INK, 0.35 * big)
                cr.set_line_width(5)
                cr.move_to(x + 260 + 40 * (i % 2), yy)
                cr.line_to(x + 520 + 60 * (i % 3), yy)
                cr.stroke()
    return dict(ui=ui)


def stars_spin(cr, t, x, y, r, t0, alpha=1.0):
    """Dizzy stars circling over Ravana's heads: small gold stars, inked, drawn over the cloth."""
    for i in range(4):
        a = t * 5 + i * math.pi / 2
        cx, cy = x + r * math.cos(a), y + 0.35 * r * math.sin(a)
        rr = 22 * (0.85 + 0.15 * math.sin(a))
        cr.new_path()
        for k in range(10):
            ang = t * 3 + k * math.pi / 5
            q = rr if k % 2 == 0 else rr * 0.45
            (cr.move_to if k == 0 else cr.line_to)(cx + q * math.cos(ang), cy + q * math.sin(ang))
        cr.close_path()
        cr.set_source_rgba(1.0, 0.80, 0.22, alpha)
        cr.fill_preserve()
        cr.set_source_rgba(*INK, alpha)
        cr.set_line_width(3)
        cr.stroke()


def s_friends(cr, t, tl, t0, t1):
    tY = cue(tl, "r18", {"hi": "योजन", "kn": "ಯೋಜನ"}, 0.1)
    tL = cue(tl, "r18", {"hi": "छोड़", "kn": "ಬಿಟ್ಟ"}, 0.45)
    tF = cue(tl, "r18", {"hi": "आग", "kn": "ಬೆಂಕಿ"}, 0.62)
    tD = cue(tl, "r18", {"hi": "दोस्ती", "kn": "ಸ್ನೇಹ"}, 0.85)
    tL = max(tL, t0 + 1.0)
    tF = max(tF, tL + 0.6)
    tD = max(tD, tF + 0.5)
    prop(cr, "tree", 120, FEET + 10, 0.62, rot=sway(t, 0.006, 0.3), alpha=0.7, blur=6)
    ground(cr)
    vs = 0.88
    if t > tF - 0.2:
        p = prog(t, tF - 0.2, 0.4)
        prop(cr, "altar", 540, FEET + 14, 0.62, alpha=p)
        prop(cr, f"flame{int(t * 10) % 3}", 540, FEET - 46, 0.5 * p, alpha=p)
        glow(cr, 540, FEET - 160, 300, 0.5 * p * (0.85 + 0.15 * math.sin(t * 9)))
    clasp = keyed(t, [(t0, 0.0), (tD - 0.15, 1.0)], 0.35, 1.3)
    rs, rx_f, vx_f = 0.6, 370, 760                # Ravana and Vali once they stand as friends
    meet = (556, 1170)                            # where their hands meet, over the fire
    if t < tL:
        land = back(clamp((t - t0) / 0.5), 1.4)
        vy = man_y(vs) - 900 * (1 - land)
        vali_carry(cr, t, 700, vy, vs, fly=1 - land, rods=land > 0.99, flail=0.4 + 0.6 * (t > tY))
        if land >= 1:                             # dust where he lands
            u = clamp((t - t0 - 0.5) / 0.6)
            for k in (-1, 1):
                prop(cr, "cloud", 700 + k * (120 + 200 * u), FEET - 30 - 40 * u, 0.25 + 0.2 * u, alpha=0.6 * (1 - u))
        if t > tY:                                # Ravana, still tucked, sees stars
            stars_spin(cr, t, 700 + 190 * vs, man_y(vs) - 260 * vs, 90, tY, alpha=prog(t, tY, 0.3))
        fl = 0.25 * math.exp(-6 * max(0, t - t0 - 0.5)) * (t > t0 + 0.5)
    else:
        fl = 0.35 * math.exp(-5 * max(0, t - tL))
        fv = reach(vx_f, man_y(vs), vs, 1.32, meet, flip=True)
        va = vali_angles(t, front=(-0.6 + (fv[0] + 0.6) * clasp, -0.5 + (fv[1] + 0.5) * clasp), backa=(0.3, -0.4),
                         hits=[(tL, 0.8)])
        puppet(cr, R.VALI, vx_f, man_y(vs), vs, 0.0, flip=True, angles=va)
        u = clamp((t - tL) / 0.45)
        up = keyed(t, [(t0, 0.0), (tF + 0.1, 1.0)], 0.35, 1.3)
        dizzy = 1 - up
        if up < 0.5:
            # dropped: tumbles down and sits, heads spinning
            rx = 700 - 150 * vs + (rx_f - (700 - 150 * vs)) * ease(u)
            ry = (man_y(vs) - 150 * vs) + (FEET - 250 * rs - (man_y(vs) - 150 * vs)) * u ** 2
            rot = math.pi / 2 * (1 - ease(u)) + 0.15 * math.sin(t * 5) * dizzy
            ang = rv_angles(t, front=(-0.8, -0.8), backa=(0.6, -1.0), head=0.2 * math.sin(t * 5))
            pts = rv(cr, t, rx, ry, rs, rot, ang=ang, kneel=u > 0.6, look=0.3 * math.sin(t * 6), squash=1 - u,
                     rods=False)
            if u >= 1:
                stars_spin(cr, t, pts["top"][0] - 20, pts["top"][1] - 120, 120, tL)
        else:
            fr = reach(rx_f, man_y(rs), rs, 1.18, meet)
            ang = rv_angles(t, front=(-0.4 + (fr[0] + 0.4) * clasp, -0.6 + (fr[1] + 0.6) * clasp), backa=(0.3, -0.5),
                            hits=[(tD, 0.3)])
            rv(cr, t, rx_f, man_y(rs), rs, 0.0, ang=ang)
        if t > tD:
            glow(cr, meet[0], meet[1], 200, 0.5 * math.exp(-2 * max(0, t - tD)) + 0.15)
    fl += 0.3 * math.exp(-4 * max(0, t - tD)) * (t > tD)

    def ui(cr):
        if t < tL:
            head2(cr, t, "AFTER THOUSANDS OF", t0 + 0.05, "YOJANAS", tY, big_size=200)
        elif t < tD:
            head2(cr, t, "BACK AT KISHKINDHA, VALI", tL, "LET GO", tL + 0.08, big_size=200)
        else:
            head2(cr, t, "BEFORE A FIRE, THEY BECAME", tD, "FRIENDS", tD + 0.06, big_size=200)
        if t > tD:
            tally(cr, t, 185, 660, 0.34, (tD, tD, tD, tD), (tD - 5, tD + 0.6, None, None), alpha=prog(t, tD, 0.3))
    return dict(ui=ui, flash=fl)


def hanuman_leap(cr, t, x, y, s, alpha=1.0):
    ang = man_angles("hanuman", t, front=(-2.4, -0.2), backa=(-2.0, -0.6), legs=(0.9, 0.3), head=-0.2)
    pts = puppet(cr, R.HANUMAN, x, y, s, -1.15, flip=True, angles=ang, alpha=alpha, rods=False,
                 extra={"hanuman_armB_lo": in_hand("mace", 160, math.pi, 0.7)})
    tx, ty = pts["tail"]
    for i in range(2):
        prop(cr, f"flame{(int(t * 12) + i) % 3}", tx + 6 * i, ty + 30, 0.28 - 0.08 * i, rot=0.3, alpha=alpha)
    glow(cr, tx, ty - 40, 160, 0.5 * alpha)
    return pts


def s_lanka(cr, t, tl, t0, t1):
    tC = cue(tl, "r19", {"hi": "श्राप", "kn": "ಶಾಪ"}, 0.05)
    tH = cue(tl, "r19", {"hi": "हँसा", "kn": "ನಕ್ಕ"}, 0.35)
    tB = cue(tl, "r19", {"hi": "जलाई", "kn": "ಸುಟ್ಟ"}, 0.6)
    tA = cue(tl, "r19", {"hi": "सेना", "kn": "ಸೇನೆ"}, 0.85)
    tV = cue(tl, "r19", {"hi": "वानर", "kn": "ವಾನರನ"}, 0.2)
    tB = max(tB, tH + 0.8)
    tA = max(tA, tB + 1.4)
    lp = ease((t - tB + 0.3) / 0.5) if t > tB - 0.3 else 0.0
    if t < tB:
        out = 1 - prog(t, tB - 0.3, 0.3)
        if t > tV - 0.1:                         # the vanara face he laughed at (Nandi, as at Kailasa)
            b, k, a = depth(t, tV - 0.1, 0.45)
            nandi(cr, t, 820, 0.6 * k, 1.0, 0.0, alpha=a * out, blur=b)
        if t > tH:
            ang = rv_angles(t, front=(-1.2, -1.2), backa=(0.6, -1.6), head=-0.35)
            rv(cr, t, 300, man_y(0.55), 0.55, bob_rot(t, 1) - 0.06, ang=ang, mood="laugh", jig=1.0,
               alpha=prog(t, tH, 0.25) * out)
    if lp > 0:
        glow(cr, 540, 1350, 520, 0.6 * lp * (0.8 + 0.2 * math.sin(t * 8)))
        prop(cr, "rv_lanka", 540, FEET + 10 + 300 * (1 - lp), 0.85, alpha=lp)
        fp = [(540 - 470 + 94 * i, FEET - 280 + (40 if i % 3 == 1 else 0)) for i in range(11)]
        fp += [(540 - 365, FEET - 400), (540 + 365, FEET - 400), (540, FEET - 545)]
        flames(cr, t, fp, 0.42, alpha=prog(t, tB, 0.5))
        u = clamp((t - tB) / 1.6)
        if 0 < u < 1:
            hx = 1250 - 1500 * u
            hy = 980 - 260 * math.sin(math.pi * u)
            hanuman_leap(cr, t, hx, hy, 0.62)
    if t > tA - 0.2:
        glow(cr, 300, 1500, 420, 0.4 * prog(t, tA, 0.5))
        for i in range(5):
            ts = tA - 0.2 + 0.12 * i
            x, bob, rock, ph = hop_walk(t, ts, ts + 1.5, -180 - 170 * i, 470 - 150 * i, 0.38)
            vanara(cr, t, x, 1890 + bob, 0.5, step=ph, raise_=0.9 * ((i + 1) % 2), ph=i * 1.1, rot=rock,
                   alpha=prog(t, ts, 0.2))
    ground(cr, y=FEET + 40)

    def ui(cr):
        if t < tB:
            head2(cr, t, "AND NANDI'S", t0 + 0.05, "CURSE?", tC + 0.1, big_size=200)
            note(cr, t, 540, 820, 0.85, t0 + 0.05, [("VANARAS LIKE ME", t0 - 1), ("WILL BE BORN...", t0 - 1)], t0 + 0.4,
                 alpha=1 - prog(t, tB - 0.25, 0.25))
        elif t < tA:
            head2(cr, t, "A VANARA", tB, "BURNED LANKA", tB + 0.06, big_size=180)
        else:
            head2(cr, t, "AND A VANARA ARMY AT", tA, "HIS GATES", tA + 0.06, big_size=190)
    return dict(ui=ui, night=0.4 - 0.15 * prog(t, tA, 0.6))


def s_end(cr, t, tl, t0, t1):
    tY = cue(tl, "r20", {"hi": "यस", "kn": "ಹೌದಾ"}, 0.7)
    tally(cr, t, 540, 820, 0.62, (t0 + 0.1, t0 + 0.2, t0 + 0.3, t0 + 0.4), (t0 + 0.5, t0 + 0.8, None, None),
          alpha=prog(t, t0, 0.25))
    p = back(clamp((t - tY + 0.6) / 0.4), 1.4)
    yb = 1320 + 80 * (1 - p)
    vali_carry(cr, t, 540, 1900 - 434 * 0.3, 0.3, flail=0.7)
    cr.save()
    cr.translate(540, yb)
    cr.scale(0.86, 0.86)
    pc.paint_part(cr, "card", alpha=clamp(p))
    cr.restore()
    pc.rod(cr, 420, yb + 170, 380, H + 60, alpha=clamp(p))
    pc.rod(cr, 660, yb + 170, 700, H + 60, alpha=clamp(p))

    def ui(cr):
        a = clamp(p)
        head2(cr, t, "DID YOU KNOW? BEFORE RAMA, HE", t0, "LOST TWICE", t0 + 0.12, big_size=190)
        for i, lab in enumerate(("YES", "NO")):
            bx = 540 - 160 + 320 * i
            cr.set_source_rgba(*INK, a)
            cr.set_line_width(7)
            cr.rectangle(bx - 112, yb - 36, 62, 62)
            cr.stroke()
            draw_text(cr, lab, bx - 30, yb - 5, 96, INK, a, anchor="lm")
        if t > tY:
            side = int((t - tY) / 0.9) % 2
            red_ring(cr, 540 - 160 + 320 * side + 20, yb - 5, 135, 80, prog(t, tY + 0.9 * int((t - tY) / 0.9), 0.35),
                     9)
    return dict(ui=ui)


SHOTS = [   # (line, cue: None = line start / fraction, draw function, options)
    ("r1", None, s_hook, {"z": (1.0, 1.04)}),
    ("r2", None, s_source, {}),
    ("r3", None, s_tally, {}),
    ("r4", None, s_conquer, {}),
    ("r5", None, s_kailasa, {}),
    ("r6", None, s_curse, {}),
    ("r7", None, s_narmada, {}),
    ("r8", None, s_arjuna, {}),
    ("r9", None, s_dam, {}),
    ("r10", None, s_reverse, {}),
    ("r11", None, s_capture, {}),
    ("r12", None, s_pulastya, {}),
    ("r13", None, s_rehook, {"z": (1.0, 1.1)}),
    ("r14", None, s_vali, {}),
    ("r15", None, s_sandhya, {}),
    ("r16", None, s_snatch, {"z": (1.02, 1.08)}),
    ("r17", None, s_oceans, {"z": (1.0, 1.03)}),
    ("r18", None, s_friends, {}),
    ("r19", None, s_lanka, {}),
    ("r20", None, s_end, {"z": (1.0, 1.03)}),
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
    """(time, name, dur): the Jarasandha vocabulary: a whoosh on every cut, damaru on hits, conch for the curse and
    each defeat, shimmer on magic and blessings, temple bell on sacred beats and the end card, pops as things land."""
    st = starts(tl, SHOTS)
    ev = [(s, "whoosh", 0.45) for s in st[1:]]
    g = lambda bid, f: T(tl, bid, f)
    c = lambda bid, w, f: cue(tl, bid, w, f)
    ev += [(0.0, "damaru", 0), (0.05, "bell", 0), (0.45, "pop", 0)]
    tG = c("r1", {"hi": "देवता", "kn": "ದೇವತೆ"}, 0.15)
    tM = c("r1", {"hi": "वानर", "kn": "ವಾನರ"}, 0.45)
    tB = c("r1", {"hi": "बगल", "kn": "ಕಂಕುಳ"}, 0.55)
    tS = max(c("r1", {"hi": "समुद्र", "kn": "ಸಮುದ್ರ"}, 0.8), tB + 1.0)
    ev += [(tG, "damaru", 0), (tG + 0.05, "hit", 0), (tM - 0.3, "dip", 0.4), (tM, "hit", 0),
           (tB - 0.1, "whoosh", 0.4), (tB + 0.25, "thud", 0), (tB + 0.3, "damaru", 0), (tS, "shimmer", 0),
           (tS, "whoosh", 0.8)]
    ev += [(c("r2", {"hi": "नहीं", "kn": "ಅಲ್ಲ"}, 0.3), "slam", 0),
           (c("r2", {"hi": "वाल्मीकि", "kn": "ವಾಲ್ಮೀಕಿ"}, 0.5), "conch", 0),
           (c("r2", {"hi": "उत्तर", "kn": "ಉತ್ತರ"}, 0.72), "thud", 0)]
    t1st = c("r3", {"hi": "एक", "kn": "ಒಂದ"}, 0.45)
    t2nd = c("r3", {"hi": "दो", "kn": "ಎರಡು"}, 0.62)
    ev += [(c("r3", {"hi": "राम", "kn": "ರಾಮ"}, 0.08) + 0.1, "pop", 0), (t1st, "pop", 0), (t2nd - 0.3, "dip", 0.4),
           (t2nd, "hit", 0), (t2nd + 0.05, "damaru", 0)]
    tV = c("r4", {"hi": "वरदान", "kn": "ಸಿಕ್ಕ"}, 0.25)
    tW = c("r4", {"hi": "दुनिया", "kn": "ಲೋಕ"}, 0.65)
    b4 = tl["r5"].start
    m0 = max(tW - 0.5, tl["r4"].start + 0.6)
    ev += [(tV, "shimmer", 0)]
    ev += [(m0 + 0.38 * i, "step", 0) for i in range(int(max(0, b4 - m0) / 0.38))]
    ev += [(tW + 0.3 + 0.5 * i, "pop", 0) for i in range(4) if tW + 0.3 + 0.5 * i < b4]
    tS5 = c("r5", {"hi": "रोका", "kn": "ತಡೆದ"}, 0.22)
    tL5 = c("r5", {"hi": "हँस", "kn": "ನಕ್ಕು"}, 0.86)
    ev += [(tl["r5"].start + 0.3 + 0.42 * i, "step", 0) for i in range(3)]
    ev += [(tS5, "thud", 0), (tS5 + 0.05, "damaru", 0), (c("r5", {"hi": "चेहरा", "kn": "ಮುಖ"}, 0.5), "tick", 0),
           (tL5, "damaru", 0), (tL5 + 0.35, "damaru", 0), (tL5 + 0.7, "damaru", 0)]
    tV6 = c("r6", {"hi": "वानर", "kn": "ವಾನರರು"}, 0.4)
    ev += [(c("r6", {"hi": "श्राप", "kn": "ಶಾಪ"}, 0.1), "conch", 0)]
    ev += [(tV6 + 0.12 * i, "pop", 0) for i in range(0, 7, 2)]
    tN6 = c("r6", {"hi": "नाश", "kn": "ನಾಶ"}, 0.85)
    ev += [(tN6 - 0.3, "dip", 0.4), (tN6, "slam", 0), (tN6 + 0.05, "hit", 0)]
    tLi = c("r7", {"hi": "शिवलिंग", "kn": "ಶಿವಲಿಂಗ"}, 0.6)
    tFl = c("r7", {"hi": "फूल", "kn": "ಹೂವು"}, 0.8)
    ev += [(c("r7", {"hi": "नर्मदा", "kn": "ನರ್ಮದಾ"}, 0.2), "whoosh", 0.6), (tLi, "bell", 0)]
    ev += [(tFl + 0.28 * i, "pop", 0) for i in range(4)]
    tA8 = c("r8", {"hi": "हज़ार", "kn": "ಸಾವಿರ"}, 0.8)
    ev += [(tl["r8"].start + 0.4 + 0.7 * i, "pop", 0) for i in range(int(max(0, tA8 - tl["r8"].start) / 0.7))]
    ev += [(tA8, "shimmer", 0), (tA8 + 0.1, "typing", 1.3), (tA8 + 1.45, "ding", 0)]
    tA9 = c("r9", {"hi": "हज़ार", "kn": "ಸಾವಿರ"}, 0.45)
    tS9 = c("r9", {"hi": "रोक", "kn": "ತಡೆದು"}, 0.85)
    ev += [(tA9, "whoosh", 0.5), (tS9 - 1.0, "riser", 1.0), (tS9, "thud", 0), (tS9 + 0.05, "damaru", 0)]
    tU = c("r10", {"hi": "उल्टा", "kn": "ಹಿಂದಕ್ಕೆ"}, 0.2)
    tF10 = c("r10", {"hi": "फूल", "kn": "ಹೂವೆಲ್ಲಾ"}, 0.62)
    ev += [(tU, "whoosh", 0.8), (tF10 - 0.3, "dip", 0.4), (tF10, "sting", 0)]
    tG11 = c("r11", {"hi": "पकड़ा", "kn": "ಹಿಡಿದು"}, 0.55)
    tT11 = max(c("r11", {"hi": "बाँधा", "kn": "ಕಟ್ಟಿ"}, 0.68), tG11 + 0.4)
    tC11 = max(c("r11", {"hi": "राजधानी", "kn": "ರಾಜಧಾನಿ"}, 0.85), tT11 + 0.4)
    ev += [(tl["r11"].start + 0.2 + 0.32 * i, "step", 0) for i in range(4)]
    ev += [(tG11, "hit", 0), (tG11 + 0.03, "damaru", 0), (tT11, "creak", 0), (tC11, "slam", 0),
           (tC11 + 0.6, "tick", 0), (tC11 + 0.65, "conch", 0)]
    tD12 = c("r12", {"hi": "दादा", "kn": "ಅಜ್ಜ"}, 0.25)
    tR12 = c("r12", {"hi": "छुड़वाना", "kn": "ಬಿಡಿಸ್ಕೊಂಡು"}, 0.75)
    ev += [(tl["r12"].start + 0.2 + 0.42 * i, "step", 0) for i in range(3)]
    ev += [(tD12, "bell", 0), (tR12, "shimmer", 0), (tR12 + 0.1, "thud", 0)]
    tB13 = c("r13", {"hi": "बाकी", "kn": "ಬಾಕಿ"}, 0.7)
    ev += [(tl["r13"].start - 0.35, "tick", 0), (tl["r13"].start - 0.3, "dip", 0.5), (tl["r13"].start, "sting", 0),
           (tl["r13"].start + 0.2, "heartbeat", 1.6), (tB13, "slam", 0), (tB13 + 0.02, "hit", 0)]
    tV14 = c("r14", {"hi": "वाली", "kn": "ವಾಲಿ"}, 0.35)
    tS14 = max(c("r14", {"hi": "ताक़तवर", "kn": "ಶಕ್ತಿಶಾಲಿ"}, 0.5), tV14 + 0.6)
    tG14 = c("r14", {"hi": "सीधा", "kn": "ಸೀದಾ"}, 0.65)
    tK14 = c("r14", {"hi": "किष्किंधा", "kn": "ಕಿಷ್ಕಿಂಧೆ"}, 0.2)
    ev += [(tK14, "pop", 0), (tV14, "damaru", 0), (tV14 + 0.05, "thud", 0), (tS14, "hit", 0), (tS14 + 0.1, "slam", 0)]
    ev += [(tG14 + 0.35 * i, "step", 0) for i in range(4)]
    tY15 = c("r15", {"hi": "संध्या", "kn": "ಸಂಧ್ಯಾ"}, 0.35)
    tC15 = c("r15", {"hi": "चुपके", "kn": "ಸದ್ದಿಲ್ಲದೆ"}, 0.6)
    ev += [(tY15, "bell", 0), (tY15 + 0.2, "shimmer", 0)]
    ev += [(tC15 + 0.6 * i, "tick", 0) for i in range(int(max(0, tl["r15"].end - tC15) / 0.6) + 1)]
    tG16 = c("r16", {"hi": "पकड़ा", "kn": "ಹಿಡಿದು"}, 0.55)
    tT16 = max(c("r16", {"hi": "बगल", "kn": "ಕಂಕುಳ"}, 0.85), tG16 + 0.45)
    ev += [(tG16 - 0.3, "dip", 0.4), (tG16, "hit", 0), (tG16 + 0.02, "damaru", 0), (tG16 + 0.05, "whoosh", 0.35),
           (tT16, "thud", 0), (tT16 + 0.05, "pop", 0)]
    tW17 = max(c("r17", {"hi": "पश्चिम", "kn": "ಪಶ್ಚಿಮ"}, 0.2), tl["r17"].start + 0.6)
    tN17 = max(c("r17", {"hi": "उत्तर", "kn": "ಉತ್ತರ"}, 0.3), tW17 + 0.6)
    tE17 = max(c("r17", {"hi": "पूर्व", "kn": "ಪೂರ್ವ"}, 0.4), tN17 + 0.6)
    tSa17 = max(c("r17", {"hi": "संध्या", "kn": "ಸಂಧ್ಯಾ"}, 0.6), tE17 + 0.6)
    tD17 = max(c("r17", {"hi": "रावण", "kn": "ರಾವಣ"}, 0.78), tSa17 + 0.8)
    ev += [(tl["r17"].start + 0.1, "whoosh", 0.8)]
    ev += [(x, "ding", 0) for x in (tl["r17"].start + 0.3, tW17, tN17, tE17)]
    ev += [(tSa17, "bell", 0), (tSa17 + 0.1, "shimmer", 0), (tD17 - 0.1, "whoosh", 1.2), (tD17 + 0.4, "damaru", 0)]
    tY18 = c("r18", {"hi": "योजन", "kn": "ಯೋಜನ"}, 0.1)
    tL18 = max(c("r18", {"hi": "छोड़", "kn": "ಬಿಟ್ಟ"}, 0.45), tl["r18"].start + 1.0)
    tF18 = max(c("r18", {"hi": "आग", "kn": "ಬೆಂಕಿ"}, 0.62), tL18 + 0.6)
    tD18 = max(c("r18", {"hi": "दोस्ती", "kn": "ಸ್ನೇಹ"}, 0.85), tF18 + 0.5)
    ev += [(tl["r18"].start + 0.45, "thud", 0), (tY18, "ding", 0), (tY18 + 0.25, "ding", 0), (tL18, "whoosh", 0.4),
           (tL18 + 0.45, "thud", 0), (tL18 + 0.5, "damaru", 0), (tF18 - 0.2, "shimmer", 0), (tD18, "bell", 0),
           (tD18 + 0.6, "tick", 0), (tD18 + 0.65, "conch", 0)]
    tH19 = c("r19", {"hi": "हँसा", "kn": "ನಕ್ಕ"}, 0.35)
    tB19 = max(c("r19", {"hi": "जलाई", "kn": "ಸುಟ್ಟ"}, 0.6), tH19 + 0.8)
    tA19 = max(c("r19", {"hi": "सेना", "kn": "ಸೇನೆ"}, 0.85), tB19 + 1.4)
    tV19 = c("r19", {"hi": "वानर", "kn": "ವಾನರನ"}, 0.2)
    ev += [(tl["r19"].start + 0.1, "conch", 0), (tl["r19"].start + 0.45, "thud", 0), (tV19, "shimmer", 0),
           (tH19, "damaru", 0), (tB19 - 0.3, "dip", 0.4), (tB19, "sting", 0),
           (tB19 + 0.1, "whoosh", 1.2)]
    ev += [(tA19 - 0.2 + 0.35 * i, "step", 0) for i in range(5)]
    ev += [(tA19, "damaru", 0), (tA19 + 0.5, "damaru", 0)]
    tY20 = c("r20", {"hi": "यस", "kn": "ಹೌದಾ"}, 0.7)
    ev += [(tl["r20"].start + 0.5, "tick", 0), (tl["r20"].start + 0.8, "tick", 0), (tY20 - 0.6, "pop", 0),
           (tY20, "bell", 0), (tY20 + 0.1, "ding", 0)]
    return [(round(max(0.0, a), 3), n, d) for a, n, d in ev]
