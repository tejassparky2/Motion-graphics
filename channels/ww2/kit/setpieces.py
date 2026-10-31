"""WW2 channel kit: reusable action set-pieces with the poster figures (stick.py), SHOTLIST.md "Reusable set-pieces".

Each is one function that draws into world space (the caller sets the camera), driven by t, with parameters for
nation, place and size, so the same piece serves several shots. All non-graphic (STYLE.md): flashes, smoke, ducking
and dignified people; no injuries.

    from channels.ww2.kit import setpieces as sp
    sp.squad_advance(cr, t, nation="usa", x0=150, ground=900)          # leapfrog: run crouched, kneel and aim, fire
    sp.march_column(cr, t, nation="germany", ground=980, horizon=560)  # rows marching in step, receding into depth
    sp.duck_under_fire(cr, t, nation="britain", x=960, ground=900)     # behind sandbags: bursts land, they duck
    sp.cheering_crowd(cr, t, 0, 1920, 640, 1000)                       # V-E Day: arms up, hats flying, confetti
    sp.waiting_crowd(cr, t, 0, 1920, 600, 980, nation="britain")       # standing, heads down, a shuffle now and then
    sp.radio_family(cr, t, x=960, ground=930)                          # a family kneeling round a radio, heads bowed
    sp.shivering_soldiers(cr, t, nation="germany", x=960, ground=930)  # in snow, arms wrapped, breath puffs
    sp.prisoner_line(cr, t, nation="germany", ground=980, horizon=520) # a long line walking away into the snow

Sound cues are listed in each docstring.
"""
import math
import random

from channels.ww2.kit.core import H, W, cairo, col, lerp, smooth  # noqa: F401
from channels.ww2.kit import fx, props
from channels.ww2.kit import stick
from channels.ww2.kit.stick import Figure, crowd

# ---------------------------------------------------------------- extra poses for the set-pieces
_AIM = stick._AIM


def _crouch_run(t):
    """Running bent low under fire, rifle held across the body."""
    d = stick._run(t)
    d.update(lean=0.55, nod=-0.35, drop=28, sh_n=0.9, el_n=0.9, sh_f=0.6, el_f=1.2, hand_n="fist", hand_f="fist")
    return d


KNEEL_AIM = dict(_AIM, lean=0.18, hip_n=1.25, kn_n=1.25, hip_f=0.15, kn_f=2.6, drop=60, ground="feet",
                 face={"brow": "angry", "mouth": "grit"})
KNEEL_BOW = dict(lean=0.32, nod=0.6, hip_n=1.2, kn_n=2.6, hip_f=1.15, kn_f=2.6, sh_n=0.35, el_n=0.9, sh_f=0.3,
                 el_f=1.0, ground="feet", drop=70, turn=0.3, face={"brow": "sad", "mouth": "frown"})
HUG = dict(lean=0.2, nod=0.22, sh_n=0.5, el_n=2.15, sh_f=0.42, el_f=2.25, kn_n=0.18, kn_f=0.2, drop=6, turn=0.5,
           hand_n="fist", hand_f="fist", face={"brow": "worried", "mouth": "grit"})


def _shiver(t, seed=0):
    j = math.sin(t * 2 * math.pi * 9.0 + seed)
    return dict(HUG, sway=0.025 * j, bob=1.5 * j)


def _plod(t, period=1.3):
    """A slow, heavy walk, head down (prisoners, the snow)."""
    d = stick._walk(t, period=period, amp=0.3, arm=0.12, lean=0.12)
    d.update(nod=0.35, sh_n=0.05 + d["sh_n"] * 0.3, sh_f=-0.05 + d["sh_f"] * 0.3, el_n=0.15, el_f=0.15,
             face={"brow": "sad", "mouth": "line"})
    return d


# ---------------------------------------------------------------- 1. squad advancing
def squad_advance(cr, t, nation="usa", x0=150.0, ground=900.0, n=5, scale=0.55, spacing=230.0, facing=1,
                  speed=95.0, period=3.2, seed=4):
    """A squad advancing by leapfrog: each man runs bent low for part of the cycle, then drops to one knee and fires
    (muzzle flash only) while the next one runs; staggered depth (two ranks). Positions advance only while running.
    Sound: boots on dirt in bursts, single rifle shots at each flash."""
    r = random.Random(seed)
    men = []
    for i in range(n):
        off = (i / n) * period + r.uniform(-0.15, 0.15)
        depth = i % 2                                              # two ranks: the back one higher, smaller
        men.append((depth, i, off))
    for depth, i, off in sorted(men, key=lambda m: m[0], reverse=False):
        s = scale * (0.86 if depth else 1.0)
        y = ground - (40 if depth else 0)
        tt = t + off
        k, ph = divmod(tt, period)
        run_part = 0.55
        dist = k * speed * period * run_part + min(ph, period * run_part) * speed
        x = x0 + facing * (i * spacing + dist - off * speed * run_part * 0.5)
        f = Figure(nation=nation, x=x, y=y, scale=s, facing=facing, prop="rifle", seed=seed * 50 + i)
        if ph < period * run_part:
            pose = _crouch_run(tt)
        else:
            u = (ph - period * run_part) / (period * (1 - run_part))
            pose = dict(KNEEL_AIM, flash=1.0 if 0.35 < u < 0.42 else 0.0)
        f.draw_pose(cr, t, stick.pose_at(pose, tt, f.seed), x, y)


# ---------------------------------------------------------------- 2. marching column
def march_column(cr, t, nation="germany", ground=980.0, horizon=560.0, rows=7, cols=3, scale=0.62, x_center=W / 2,
                 speed=70.0, facing=1, spread=150.0, seed=2, rifles=True):
    """A column marching in step across the frame, rows receding toward the horizon (smaller, higher, paler: a
    printed depth). The front rows are full poster figures, the far rows silhouettes. Loops seamlessly.
    Sound: marching boots in unison, a drum."""
    out = []
    for r_ in range(rows):
        u = r_ / max(1, rows - 1)                                   # 0 front .. 1 back
        y = lerp(ground, horizon + 60, u ** 0.8)
        s = scale * lerp(1.0, 0.32, u ** 0.8)
        for c in range(cols):
            x = x_center + (c - (cols - 1) / 2) * spread * s / scale + ((t * speed * facing + r_ * 37) % 600) - 300
            x += (u * 260) * facing
            out.append((y, x, s, r_, c, u))
    for y, x, s, r_, c, u in sorted(out, key=lambda q: q[0]):
        flat = u > 0.45
        f = Figure(nation=nation, x=x, y=y, scale=s, facing=facing, prop="rifle" if rifles and not flat else None,
                   seed=seed * 100 + r_ * 7 + c, flat=flat)
        if flat:
            f.tone = stick._mix(stick._shade(col(stick.NATION_SIDE.get(nation, "axis")), 0.35), col("paper"),
                                0.45 * (u - 0.45) / 0.55)
        f.draw(cr, t, [(0.0, "march")])


# ---------------------------------------------------------------- 3. ducking under fire
def duck_under_fire(cr, t, nation="britain", x=960.0, ground=900.0, n=3, scale=0.62, facing=1, seed=6,
                    bursts=(0.6, 1.9, 3.1, 4.4), every=5.0):
    """Soldiers behind a sandbag wall; flat star bursts and dirt puffs land beyond it on `bursts` (repeating every
    `every` s) and the men duck, hands over helmets, then peek back up. Non-graphic: flashes and smoke only.
    Sound: a whistle then a crump at each burst, falling dirt."""
    tt = t % every
    last = max([b for b in bursts if b <= tt], default=-9)
    age = tt - last
    r = random.Random(seed + int(t // every))
    bx = x + facing * (n * 130 + 160 * r.random()) + r.uniform(-200, 200)
    by = ground - 60
    fx.puff(cr, bx, by, age, size=1.2, seed=int(last * 7))
    for i in range(n):
        ducking = 0.0 <= age < 1.1
        pose = "duck" if ducking else ("crouch" if age < 1.5 else KNEEL_AIM)
        f = Figure(nation=nation, x=x + (i - (n - 1) / 2) * 230 * scale / 0.62, y=ground - 10,
                   scale=scale * (1 - 0.05 * (i % 2)), facing=facing, prop="rifle", seed=seed * 10 + i)
        f.draw(cr, t, [(last + 0.05, pose)], face={"sweat": 1.0} if ducking else None)
    props.Sandbags(x=x, y=ground + 10, scale=scale * 1.6, length=n * 230 / 1.3 + 160, rows=3).draw(cr, t)
    fx.starburst(cr, bx, by - 60, age, size=1.1, seed=int(last * 3))


# ---------------------------------------------------------------- 4. cheering crowd
def cheering_crowd(cr, t, x0=0.0, x1=W, y0=640.0, y1=1000.0, n=46, scale=0.5, front=5, seed=3, hats=True,
                   confetti=True, nation=None):
    """V-E Day: a dense crowd cheering (silhouettes behind, a front row of full poster civilians and soldiers),
    hats tossed up and spinning, confetti drifting down. Sound: cheering, bells, a band in the distance."""
    crowd(cr, t, n, x0, x1, y0, y1 - 40, scale=scale * 0.8, pose="cheer", seed=seed,
          poses=["cheer", "cheer", "wave", "stand"], tone="ink_soft")
    r = random.Random(seed)
    kinds = [dict(civilian="flatcap"), dict(civilian="hat"), dict(nation="britain"), dict(civilian="scarf"),
             dict(nation="usa"), dict(nation="soviet")]
    for i in range(front):
        x = lerp(x0 + 120, x1 - 120, (i + 0.5) / front) + r.uniform(-40, 40)
        k = kinds[i % len(kinds)] if nation is None else dict(nation=nation)
        f = Figure(x=x, y=y1, scale=scale * 1.25, facing=r.choice((1, -1)), seed=seed * 20 + i, **k)
        f.draw(cr, t + r.uniform(0, 2), [(0.0, r.choice(["cheer", "wave", "cheer"]))])
    if hats:
        for i in range(10):
            rr = random.Random(seed * 99 + i)
            period = rr.uniform(1.4, 2.2)
            u = ((t + rr.uniform(0, period)) % period) / period
            hx = rr.uniform(x0 + 80, x1 - 80) + 40 * math.sin(u * 3)
            hy = y0 + 40 - math.sin(u * math.pi) * rr.uniform(220, 380)
            cr.save()
            cr.translate(hx, hy)
            cr.rotate(u * rr.uniform(4, 9))
            for path, c in stick._headgear_parts(rr.choice(["hat", "flatcap", "bowler"]), 28):
                stick._printed(cr, path, col(c) if c else col("ink_soft"), 6, col("ink"), 3.0, dots=False)
            cr.restore()
    if confetti:
        for i in range(90):
            rr = random.Random(seed * 7 + i)
            fall = rr.uniform(60, 140)
            x = rr.uniform(x0, x1) + 30 * math.sin(t * 2 + i)
            y = (rr.uniform(0, H) + t * fall) % (y1 + 40) - 20
            cr.save()
            cr.translate(x, y)
            cr.rotate(t * rr.uniform(2, 6) + i)
            cr.rectangle(-5, -3, 10, 6)
            cr.set_source_rgba(*col(rr.choice(["alert", "allies", "gold", "cream", "soviet"])))
            cr.fill()
            cr.restore()


# ---------------------------------------------------------------- 5. waiting crowd
def waiting_crowd(cr, t, x0=0.0, x1=W, y0=600.0, y1=980.0, n=44, scale=0.45, nation="britain", seed=5):
    """People (or soldiers) waiting: standing, heads down, a weight shift and a shuffle now and then
    (Dunkirk beach queues, the jobless queue). Sound: murmur, shuffling feet (wind and sea on a beach)."""
    crowd(cr, t, n, x0, x1, y0, y1, scale=scale, nation=nation, seed=seed,
          poses=["stand", "head_down", "head_down", "arms_crossed", "stand"])


# ---------------------------------------------------------------- 6. radio family
def radio_family(cr, t, x=960.0, ground=930.0, scale=0.7, seed=8, on=True):
    """A family kneeling round a radio on a low table, heads bowed (Japan, 15 Aug 1945: the broadcast), a warm
    lamp glow. Civilians in plain dress (no symbols). Sound: radio crackle, a voice under it (unintelligible)."""
    cr.save()
    g = cairo.RadialGradient(x, ground - 260 * scale, 20, x, ground - 260 * scale, 700 * scale)
    g.add_color_stop_rgba(0, *col("gold")[:3], 0.22)
    g.add_color_stop_rgba(1, *col("gold")[:3], 0.0)
    cr.set_source(g)
    cr.paint()
    cr.restore()
    # the low table and the radio on it
    tw, th = 360 * scale, 90 * scale
    cr.rectangle(x - tw / 2, ground - th, tw, th * 0.22)
    stick._printed(cr, lambda c: c.rectangle(x - tw / 2, ground - th, tw, th * 0.22), col("#6b4a2e"), 6,
                   col("ink"), 4)
    for sx in (-1, 1):
        stick._printed(cr, lambda c, sx=sx: c.rectangle(x + sx * tw * 0.42 - 8, ground - th, 16, th),
                       col("#5a3d26"), 0, col("ink"), 3)
    props.Radio(x=x, y=ground - th, scale=scale * 0.75).draw(cr, t, on=on)
    people = [(-470, 1, "scarf", 0.95), (-290, 1, "flatcap", 0.85), (300, -1, "scarf", 0.8), (480, -1, None, 1.0)]
    for i, (dx, face, civ, k) in enumerate(people):
        f = Figure(civilian=civ or "hat", x=x + dx * scale, y=ground, scale=scale * k, facing=face,
                   seed=seed * 10 + i)
        f.draw(cr, t + i * 0.7, [(0.0, KNEEL_BOW)])


# ---------------------------------------------------------------- 7. shivering soldiers
def shivering_soldiers(cr, t, nation="germany", x=960.0, ground=930.0, n=3, scale=0.66, spacing=230.0, seed=9,
                       snow=True, coats=False):
    """Soldiers in thin coats in deep snow, arms wrapped round themselves, shaking on 1s, breath puffing; snow
    falling and drifted at their boots (the winter of 1941). Sound: howling wind, chattering teeth."""
    cr.rectangle(0, ground - 14, W * 3, H)
    cr.save()
    cr.translate(-W, 0)
    cr.rectangle(0, ground - 14, W * 3, H)
    cr.set_source_rgba(*col("snow"))
    cr.fill()
    cr.restore()
    cr.new_path()
    for i in range(n):
        xx = x + (i - (n - 1) / 2) * spacing
        f = Figure(nation=nation, x=xx, y=ground, scale=scale * (1 - 0.05 * (i % 2)), facing=1 if i % 2 else -1,
                   seed=seed * 10 + i)
        if coats:
            f.dress.update(skirt=-0.45)
        f.draw_pose(cr, t, stick.pose_at(_shiver(t, i), t, f.seed), xx, ground)
        J = f.joints(t, [(0.0, HUG)])
        hx, hy = J["head"]
        k = ((t * 0.7 + i * 0.37) % 1.0)
        fx.puff(cr, hx + f.facing * 40 * scale + f.facing * 60 * k * scale, hy + 10 * scale - 30 * k, k * 1.4,
                size=0.18 * scale / 0.66, seed=i, life=1.4, color="#f4f0e6", rise=40)
        # snow drifted over the boots
        cr.save()
        cr.translate(xx, ground + 2)
        cr.scale(1, 0.34)
        cr.arc(0, 0, 74 * scale / 0.66, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(*col("snow"))
        cr.fill()
    if snow:
        props.snowfall(cr, t, density=220, wind=60)


# ---------------------------------------------------------------- 8. prisoner line
def prisoner_line(cr, t, nation="germany", ground=980.0, horizon=520.0, n=16, scale=0.6, x_front=1500.0,
                  x_back=300.0, speed=0.06, seed=11, snow=True):
    """A long line of prisoners walking slowly away into the snow (Stalingrad, Feb 1943): greatcoats, heads down,
    hands at their sides, receding to the horizon (smaller, paler, the far ones silhouettes). Dignified: no
    injuries, no guards' violence. The line flows along its path, looping. Sound: footsteps in snow, wind."""
    for i in reversed(range(n)):
        u = ((i / n) + t * speed) % 1.0                              # 0 = front (near), 1 = horizon
        x = lerp(x_front, x_back, u)
        y = lerp(ground, horizon, u ** 0.9)
        s = scale * lerp(1.0, 0.22, u ** 0.9)
        flat = u > 0.35
        f = Figure(nation=nation, x=x, y=y, scale=s, facing=-1, seed=seed * 30 + i, flat=flat)
        f.dress.update(skirt=-0.5)                                  # greatcoats
        if flat:
            f.tone = stick._mix(col("ink_soft"), col("snow"), 0.65 * (u - 0.35) / 0.65)
        f.draw(cr, t + i * 0.41, [(0.0, _plod)])
    if snow:
        props.snowfall(cr, t, density=200, wind=-30)
