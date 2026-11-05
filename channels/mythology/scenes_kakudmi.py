"""Scenes for mythology video 1 (Kakudmi): the code-drawn cast (myth_cast) on painted background plates
(myth_assets/kakudmi/*.png, made with SDXL; a code-painted sky stands in when a plate is missing), with divine light,
petals, counters and marks. Every change is keyed to the narration (fractions of a line keep Hindi and Kannada in
step). Frame 0: the king alone on a plain indigo ground with the two-tier headline."""
import functools
import math
import os

import cairo
import numpy as np

from channel import ASSETS_ROOT
from motion.polish import light_rays
from motion.polish import soft_disc as _soft_disc


def soft_disc(cr, x, y, r, col):
    if r > 2 and col[3] > 0.003:
        _soft_disc(cr, x, y, r, col)
from myth_cast import GOLD, LOOKS, brahma, figure, halo, hexc, hourglass, plough, veena, vedas
from poster import (CORAL, CREAM, FPS, H, MONO_FONT, RED, W, back, clamp, cross, draw_text, headline, prog, push,
                    ring, strike, text_size, to_surface, yes_no_card)
from shots import T, shot_at, starts

PLATES = os.path.join(ASSETS_ROOT, "kakudmi")
INDIGO = (0.10, 0.11, 0.25)
GOLDC = (0.91, 0.70, 0.23)


# ---------------------------------------------------------------- backgrounds
@functools.lru_cache(maxsize=8)
def _plate(name):
    path = os.path.join(PLATES, f"{name}.png")
    if not os.path.exists(path):
        return None
    from PIL import Image
    im = Image.open(path).convert("RGB")
    k = max(W * 1.12 / im.width, H * 1.12 / im.height)        # 12% overscan for drifts and push-ins
    im = im.resize((int(im.width * k), int(im.height * k)), Image.LANCZOS)
    return to_surface(im)


SKY = {   # code-painted stand-ins (top colour, bottom colour)
    "palace": ((0.35, 0.16, 0.10), (0.72, 0.42, 0.18)),
    "clouds": ((0.98, 0.80, 0.55), (0.55, 0.62, 0.86)),
    "brahmaloka": ((0.99, 0.86, 0.55), (0.93, 0.55, 0.42)),
    "dwaraka": ((0.98, 0.62, 0.36), (0.20, 0.36, 0.55)),
    "street": ((0.95, 0.82, 0.60), (0.60, 0.45, 0.30)),
}


def plate(cr, t, name, t0, drift=(0.0, -30.0), dim=0.0):
    s = _plate(name)
    if s is None:
        top, bot = SKY[name]
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, *top)
        g.add_color_stop_rgb(1, *bot)
        cr.set_source(g)
        cr.paint()
    else:
        k = clamp((t - t0) / 8.0)
        x = (W - s.get_width()) / 2 + drift[0] * k
        y = (H - s.get_height()) / 2 + drift[1] * k
        cr.set_source_surface(s, x, y)
        cr.paint()
    if dim:
        cr.set_source_rgba(0.05, 0.04, 0.10, dim)
        cr.paint()


def plain(cr, col=INDIGO):
    g = cairo.RadialGradient(W / 2, H * 0.42, 100, W / 2, H * 0.5, H * 0.75)
    g.add_color_stop_rgb(0, *(min(1, c * 1.7) for c in col))
    g.add_color_stop_rgb(1, *(c * 0.55 for c in col))
    cr.set_source(g)
    cr.paint()


def cosmos(cr, t):
    plain(cr, (0.06, 0.05, 0.16))
    rng = np.random.default_rng(3)
    xs, ys, rs, ph = rng.uniform(0, W, 220), rng.uniform(0, H, 220), rng.uniform(0.8, 3.2, 220), rng.uniform(0, 6, 220)
    for x, y, r, p in zip(xs, ys, rs, ph):
        a = 0.35 + 0.35 * math.sin(t * 1.3 + p)
        cr.arc(x, y, r, 0, 2 * math.pi)
        cr.set_source_rgba(1, 0.95, 0.85, a)
        cr.fill()


@functools.lru_cache(maxsize=4)
def _grain(k):
    rng = np.random.default_rng(100 + k)
    n = rng.normal(128, 40, (H // 2, W // 2)).clip(0, 255).astype(np.uint8)
    from PIL import Image
    im = Image.fromarray(n, "L").convert("RGBA")
    im.putalpha(14)
    return to_surface(im.resize((W, H)))


def grade(cr, t, warm=0.06):
    """One shared finish over every frame: a warm wash, a soft vignette and per-frame grain."""
    cr.set_source_rgba(1.0, 0.72, 0.38, warm)
    cr.paint()
    g = cairo.RadialGradient(W / 2, H * 0.47, H * 0.32, W / 2, H * 0.5, H * 0.78)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0.02, 0.01, 0.05, 0.55)
    cr.set_source(g)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_OVERLAY)
    cr.set_source_surface(_grain(int(t * FPS) % 4), 0, 0)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_OVER)


# ---------------------------------------------------------------- small animated pieces
def tag(cr, t, t0, text, x, y, size=40):
    """A name plate: dark lacquer with a gold rim, pops in."""
    p = prog(t, t0, 0.3)
    if p <= 0:
        return
    w, h = text_size(text, size, MONO_FONT, 3)[0] + 60, size * 1.9
    cr.save()
    cr.translate(x, y + 30 * (1 - back(clamp((t - t0) / 0.3))))
    cr.set_source_rgba(0.13, 0.06, 0.05, 0.85 * p)
    cr.rectangle(-w / 2, -h / 2, w, h)
    cr.fill()
    cr.set_source_rgba(*GOLDC, p)
    cr.set_line_width(4)
    cr.rectangle(-w / 2 + 6, -h / 2 + 6, w - 12, h - 12)
    cr.stroke()
    draw_text(cr, text, 0, 0, size, CREAM, p, MONO_FONT, "cm", tracking=3)
    cr.restore()


def petals(cr, t, n=26, seed=1, area=(0, 0, W, H), col=(0.98, 0.62, 0.72), speed=60):
    rng = np.random.default_rng(seed)
    x0, y0, w, h = area
    for k in range(n):
        px, py, ph, sz = rng.uniform(0, w), rng.uniform(0, h), rng.uniform(0, 6.3), rng.uniform(8, 18)
        y = y0 + (py + t * speed * rng.uniform(0.6, 1.2)) % h
        x = x0 + px + 30 * math.sin(t * 0.9 + ph)
        cr.save()
        cr.translate(x, y)
        cr.rotate(t * 1.5 + ph)
        cr.scale(1, 0.5)
        cr.arc(0, 0, sz, 0, 2 * math.pi)
        cr.restore()
        cr.set_source_rgba(*col, 0.75)
        cr.fill()


def notes(cr, t, x, y, n=5, seed=4):
    rng = np.random.default_rng(seed)
    for k in range(n):
        ph = (t * 0.45 + k / n) % 1.0
        nx = x + rng.uniform(-90, 90) + 40 * math.sin(ph * 6 + k)
        ny = y - ph * 420
        a = math.sin(ph * math.pi)
        draw_text(cr, "♪" if k % 2 else "♫", nx, ny, 64, GOLDC, a, "C:/Windows/Fonts/seguisym.ttf", "cm")


def year_counter(cr, t, t0, t1, x, y, final=116640000, size=96, color=GOLDC, label="YEARS"):
    """Digits rolling up with Indian grouping (11,66,40,000), easing to the final value at t1."""
    p = clamp((t - t0) / max(0.01, t1 - t0))
    v = int(final * (1 - (1 - p) ** 3))
    s = f"{v:,}"
    if v >= 100000:                                          # Indian digit grouping
        head_, tail = str(v)[:-3], str(v)[-3:]
        parts = []
        while len(head_) > 2:
            parts.insert(0, head_[-2:])
            head_ = head_[:-2]
        s = ",".join([head_] + parts) + "," + tail if head_ else ",".join(parts) + "," + tail
    a = prog(t, t0, 0.25)
    draw_text(cr, s, x, y, size, color, a, MONO_FONT, "cm")
    draw_text(cr, label, x, y + size * 0.85, size * 0.38, CREAM, a, MONO_FONT, "cm", tracking=4)


def crumble(cr, t, t0, draw_fn, cx, cy, w, h, seed=0):
    """Draw something, then let it fall apart into drifting dust from t0."""
    p = clamp((t - t0) / 1.1)
    if p < 1:
        cr.push_group()
        draw_fn(cr)
        cr.pop_group_to_source()
        cr.paint_with_alpha(1 - p)
    if p > 0:
        rng = np.random.default_rng(seed)
        for k in range(90):
            px, py = cx + rng.uniform(-w / 2, w / 2), cy + rng.uniform(-h / 2, h / 2)
            vx, vy = rng.uniform(40, 220), rng.uniform(-160, 40)
            q = clamp(p * 1.2 - rng.uniform(0, 0.3))
            cr.arc(px + vx * q, py + vy * q + 120 * q * q, 3 + 3 * rng.uniform(), 0, 2 * math.pi)
            cr.set_source_rgba(0.85, 0.75, 0.6, (1 - q) * 0.9)
            cr.fill()


def palace_icon(cr, x, y, s, col=(0.85, 0.75, 0.6)):
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    cr.move_to(-120, 0)
    for px, py in ((-120, -120), (-80, -120), (-80, -170), (-40, -170), (-40, -120), (0, -230), (40, -120),
                   (40, -170), (80, -170), (80, -120), (120, -120), (120, 0)):
        cr.line_to(px, py)
    cr.close_path()
    cr.set_source_rgba(*col, 1)
    cr.fill()
    cr.restore()


def light_from_above(cr, t, x, a=1.0):
    if a <= 0:
        return
    g = cairo.LinearGradient(x, 0, x, H * 0.8)
    g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.55 * a)
    g.add_color_stop_rgba(1, 1, 0.95, 0.75, 0)
    cr.move_to(x - 90, 0)
    cr.line_to(x + 90, 0)
    cr.line_to(x + 260, H * 0.8)
    cr.line_to(x - 260, H * 0.8)
    cr.close_path()
    cr.set_source(g)
    cr.fill()


_ENV = {}


def talk(tl, t, ids):
    """Mouth opening 0..1 from the narration loudness on these lines (Brahma's lines), 0 elsewhere."""
    for bid in ids:
        b = tl[bid]
        if not (b.start <= t <= b.end) or not b.wav or not os.path.exists(b.wav):
            continue
        if b.wav not in _ENV:
            import wave
            with wave.open(b.wav) as f:
                a = np.frombuffer(f.readframes(f.getnframes()), np.int16).astype(np.float32) / 32767
                sr = f.getframerate()
            win = int(sr * 0.03)
            rms = np.sqrt(np.convolve(a * a, np.ones(win) / win, mode="same"))
            _ENV[b.wav] = (sr, rms / max(1e-6, np.percentile(rms, 95)))
        sr, env = _ENV[b.wav]
        i = int((t - b.start) * sr)
        if 0 <= i < len(env):
            return float(min(1.0, env[i]))
    return 0.0


def mouth_for(v, rest="smile"):
    return "open" if v > 0.45 else ("o" if v > 0.2 else rest)


def C(hi, kn):
    return {"hi": hi, "kn": kn}


# ---------------------------------------------------------------- shots (fn(cr, t, tl, t0))
def s_hook(cr, t, tl, t0):                                   # b1: the king alone, an hourglass, the impossible number
    plain(cr)
    tb = T(tl, "b1", C("ग्यारह", "ಹನ್ನೊಂದು"))
    k = clamp((t - t0) / 3.0)
    figure(cr, t, W / 2 + 40, 1640, 1.75, "kakudmi", arms=("hold", "down"),
           hold=lambda c, x, y: hourglass(c, x, y, 1 - k), eyes="open", lookdir=(0.3, -0.2))
    headline(cr, t, "A FEW MOMENTS IN HEAVEN...", "11 CRORE YEARS", 0.05, min(1.8, tb - 0.15), y=280,
             small_size=58, big_size=150, small_color=CREAM, big_color=CORAL, t_ghost=0.35)
    if t > tb + 0.1:                                         # marked as the number is spoken
        ring(cr, W / 2, 280 + 58 * 1.18 + 80, 520, 105, prog(t, tb + 0.1, 0.4), color=CORAL)
    year_counter(cr, t, 0.6, tl["b1"].end, 860, 640, size=44, label="YEARS ON EARTH")


def s_gone(cr, t, tl, t0):                                   # b1b: family, city, era crumble to dust
    plain(cr, (0.12, 0.10, 0.20))
    b = tl["b1b"]
    items = [("FAMILY", lambda c: [figure(c, t, x, 900, 0.95, "villager", seed=i, shadow=False, bob=False)
                                   for i, x in enumerate((170, 330, 490))], 330, 640, 0.0),
             ("CITY", lambda c: palace_icon(c, 820, 900, 1.9), 820, 700, 0.34),
             ("ERA", lambda c: draw_text(c, "YOUR WHOLE ERA", 540, 1180, 130, CREAM, 1, anchor="cm"), 540, 1180,
              0.66)]
    for label, _, cx, cy, f in items[:2]:
        draw_text(cr, label, cx, 990, 44, CREAM, prog(t, b.start + b.dur * f, 0.3) * (1 - prog(t, b.start +
                  b.dur * f + 0.8, 0.5)), MONO_FONT, "cm", tracking=4)
    for label, fn, cx, cy, f in items:
        ts = b.start + b.dur * f
        if t < ts - 0.3:
            continue
        a = prog(t, ts - 0.3, 0.25)
        cr.push_group()
        crumble(cr, t, ts + 0.7, fn, cx, cy, 360, 300, seed=int(f * 10))
        cr.pop_group_to_source()
        cr.paint_with_alpha(a)
    headline(cr, t, "EVERYONE YOU KNEW:", "GONE", t0, b.start + b.dur * 0.75, y=1400, small_size=58, big_size=150,
             small_color=CREAM, big_color=CORAL)


def palm_leaf(cr, t, t0, x, y, w, lines):
    p = prog(t, t0, 0.6)
    ww = w * p
    cr.save()
    cr.translate(x - ww / 2, y)
    g = cairo.LinearGradient(0, -80, 0, 80)
    g.add_color_stop_rgb(0, 0.93, 0.80, 0.52)
    g.add_color_stop_rgb(1, 0.78, 0.60, 0.32)
    cr.rectangle(0, -80, ww, 160)
    cr.set_source(g)
    cr.fill()
    for hx in (ww * 0.18, ww * 0.82):
        cr.arc(hx, 0, 9, 0, 2 * math.pi)
        cr.set_source_rgba(0.35, 0.2, 0.1, p)
        cr.fill()
    cr.restore()
    for i, ln in enumerate(lines):
        draw_text(cr, ln, x, y - 30 + 60 * i, 44, (0.30, 0.16, 0.08), prog(t, t0 + 0.4 + 0.2 * i, 0.3), MONO_FONT,
                  "cm", tracking=3)


def s_source(cr, t, tl, t0):                                 # b2: not a Hollywood film; it is in the Bhagavata Purana
    plain(cr, (0.16, 0.08, 0.06))
    b = tl["b2"]
    tb = b.start + b.dur * 0.5
    draw_text(cr, "HOLLYWOOD FILM?", W / 2, 520, 92, CREAM, prog(t, t0, 0.3), anchor="cm")
    cross(cr, W / 2, 520, 140, prog(t, b.start + b.dur * 0.25, 0.3), color=CORAL)
    palm_leaf(cr, t, tb, W / 2, 1000, 860, ["BHAGAVATA PURANA", "CANTO 9, CHAPTER 3"])
    soft_disc(cr, W / 2, 1000, 520 * prog(t, tb, 0.8), (1, 0.85, 0.5, 0.12))


def s_king(cr, t, tl, t0):                                   # b3: king Kakudmi and his daughter Revati
    plate(cr, t, "palace", t0)
    b = tl["b3"]
    tr = b.start + b.dur * 0.62
    kx = 330 + 200 * (1 - back(clamp((t - t0) / 0.5)))
    figure(cr, t, kx, 1600, 1.3, "kakudmi", arms=("hips", "down"))
    tag(cr, t, t0 + 0.3, "KING KAKUDMI", 330, 1690)
    if t > tr - 0.3:
        rx = 760 + 300 * (1 - back(clamp((t - tr + 0.3) / 0.5)))
        figure(cr, t, rx, 1600, 1.55, "revati", arms=("front", "down"), seed=2)
        tag(cr, t, tr, "PRINCESS REVATI", 760, 1690)


def s_suitors(cr, t, tl, t0):                                # b4: no groom on Earth was good enough
    plate(cr, t, "palace", t0, dim=0.25)
    b = tl["b4"]
    for i in range(5):                                       # two staggered rows, big enough to read on a phone
        ts = b.start + b.dur * (0.12 + 0.16 * i)
        x, fy, sc = [(250, 1500, 0.8), (540, 1500, 0.8), (830, 1500, 0.8), (390, 1800, 0.95), (700, 1800, 0.95)][i]
        if t < ts - 0.25:
            continue
        figure(cr, t, x, fy + 18 * (1 - back(clamp((t - ts + 0.25) / 0.3))), sc, "suitor", seed=i,
               turban=hexc(["#d8763a", "#3f9b6e", "#8a4fc9", "#c9402e", "#2f5fb3"][i]))
        cross(cr, x, fy - 420 * sc, 110 * sc, prog(t, ts + 0.25, 0.25), color=CORAL)
    headline(cr, t, "NO GROOM ON EARTH WAS", "GOOD ENOUGH", t0, b.start + b.dur * 0.7, y=330, small_size=56,
             big_size=130, small_color=CREAM, big_color=CORAL)


def s_ask(cr, t, tl, t0):                                    # b5: ask the creator himself
    plate(cr, t, "palace", t0, dim=0.35)
    b = tl["b5"]
    light_from_above(cr, t, 560, prog(t, b.start + b.dur * 0.35, 0.8))
    light_rays(cr, t, 560, -60, n=6, length=1500, a=0.08 * prog(t, b.start + b.dur * 0.35, 0.8))
    figure(cr, t, 540, 1650, 1.45, "kakudmi", arms=("up", "down"), lookdir=(0.0, -0.9), eyes="open")
    headline(cr, t, "THEN ASK THE ONE WHO", "CREATED ALL", t0, b.start + b.dur * 0.55, y=260, small_size=56,
             big_size=140, small_color=CREAM, big_color=CORAL)


def s_rise(cr, t, tl, t0):                                   # b6: they rise straight to Brahmaloka
    b = tl["b6"]
    k = clamp((t - t0) / max(0.5, b.end - t0))
    plate(cr, t, "clouds", t0, drift=(0, 260))
    petals(cr, t, 30, seed=5, speed=-90, col=(1, 0.9, 0.7))
    y = 1700 - 520 * k
    figure(cr, t, 420, y, 1.05, "kakudmi", arms=("front", "down"), shadow=False, lookdir=(0.2, -0.6))
    figure(cr, t, 640, y + 20, 1.2, "revati", arms=("front", "down"), shadow=False, seed=3, lookdir=(-0.1, -0.6))
    soft_disc(cr, 540, y - 400, 420, (1, 0.95, 0.75, 0.18))
    tag(cr, t, b.start + b.dur * 0.55, "BRAHMALOKA", 540, 300, 52)


def court(cr, t, t0, dim=0.0, brahma_kw=None, singers=True):
    plate(cr, t, "brahmaloka", t0, dim=dim)
    light_rays(cr, t, 540, 420, n=7, length=1300, a=0.07)
    brahma(cr, t, 540, 1180, 0.95, **(brahma_kw or {}))
    if singers:
        figure(cr, t, 170, 1700, 0.85, "gandharva1", arms=("hold", "front"), hold=veena, seed=1, eyes="happy")
        figure(cr, t, 910, 1700, 0.85, "gandharva2", arms=("front", "front"), seed=2, facing=-1, eyes="happy",
               mouth="o")


def s_court(cr, t, tl, t0):                                  # b7: Brahma listening to the Gandharvas Haha and Huha
    b = tl["b7"]
    court(cr, t, t0, brahma_kw=dict(eyes="happy"))
    tg = b.start + b.dur * 0.55
    if t > tg - 0.3:
        notes(cr, t, 200, 1250)
        notes(cr, t, 900, 1250, seed=7)
        tag(cr, t, tg, "HAHA", 170, 1800, 40)
        tag(cr, t, tg + 0.25, "HUHU", 910, 1800, 40)
    tag(cr, t, t0 + 0.2, "BRAHMA", 540, 300, 52)


def s_wait(cr, t, tl, t0):                                   # b8: the king waits; on Earth, ages race by
    b = tl["b8"]
    court(cr, t, t0, dim=0.15, brahma_kw=dict(eyes="happy"), singers=False)
    notes(cr, t, 300, 1000, seed=9)
    notes(cr, t, 780, 1000, seed=12)
    figure(cr, t, 300, 1850, 1.1, "kakudmi", arms=("front", "front"), eyes="closed", mouth="smile", shadow=False)
    # an Earth window: ages flashing by
    te = b.start + b.dur * 0.35
    p = prog(t, te, 0.35)
    if p > 0:
        cx, cy, r = 810, 1450, 190 * p
        cr.save()
        cr.arc(cx, cy, r, 0, 2 * math.pi)
        cr.clip()
        ph = (t - te) * 2.2
        cols = [(0.25, 0.55, 0.30), (0.65, 0.55, 0.35), (0.45, 0.42, 0.40), (0.20, 0.45, 0.35)]
        a, bcol = cols[int(ph) % 4], cols[(int(ph) + 1) % 4]
        f = ph % 1
        cr.set_source_rgb(*[a[i] * (1 - f) + bcol[i] * f for i in range(3)])
        cr.paint()
        for i in range(6):
            palace_icon(cr, cx - 160 + i * 64, cy + 120, 0.25 + 0.15 * math.sin(ph * 3 + i) ** 2, (0.2, 0.15, 0.12))
        cr.restore()
        cr.arc(cx, cy, r, 0, 2 * math.pi)
        cr.set_source_rgba(*GOLDC, 1)
        cr.set_line_width(8)
        cr.stroke()
        year_counter(cr, t, te, te + 20, cx, cy - r - 70, size=46, label="EARTH")
    headline(cr, t, "HE WAITED", "POLITELY", t0, b.start + b.dur * 0.6, y=240, small_size=56, big_size=120,
             small_color=CREAM, big_color=CORAL)


def name_scroll(cr, t, x, y, fade=0.0):
    g = cairo.LinearGradient(0, y - 200, 0, y + 200)
    g.add_color_stop_rgb(0, 0.96, 0.88, 0.70)
    g.add_color_stop_rgb(1, 0.85, 0.72, 0.50)
    cr.rectangle(x - 200, y - 230, 400, 460)
    cr.set_source(g)
    cr.fill()
    for i in range(6):
        ln = clamp(fade * 1.6 - i * 0.12)
        cr.rectangle(x - 150, y - 170 + i * 66, 300 * (1 - ln), 14)
        cr.set_source_rgba(0.35, 0.18, 0.08, 0.85)
        cr.fill()


def s_list(cr, t, tl, t0):                                   # b9: song over; the king names his chosen grooms
    b = tl["b9"]
    court(cr, t, t0, dim=0.1, singers=False)
    figure(cr, t, 330, 1850, 1.1, "kakudmi", arms=("front", "front"), shadow=False)
    p = prog(t, b.start + b.dur * 0.45, 0.4)
    if p > 0:
        cr.save()
        cr.translate(0, 80 * (1 - p))
        name_scroll(cr, t, 770, 1450)
        cr.restore()


def s_laugh(cr, t, tl, t0):                                  # b10: Brahma laughs
    court(cr, t, t0, singers=False, brahma_kw=dict(eyes="happy", mouth="grin", laugh=0.6))
    soft_disc(cr, 540, 700, 600 * prog(t, t0, 0.5), (1, 0.9, 0.6, 0.18))


def s_gone_names(cr, t, tl, t0):                             # b11: "the ones you name are long gone"
    b = tl["b11"]
    v = talk(tl, t, ("b11",))
    court(cr, t, t0, singers=False, brahma_kw=dict(mouth=mouth_for(v)))
    name_scroll(cr, t, 800, 1500, fade=clamp((t - b.start) / max(0.5, b.dur * 0.8)))
    headline(cr, t, "THE GROOMS HE CHOSE?", "LONG GONE", b.start + b.dur * 0.2, b.start + b.dur * 0.5, y=230,
             small_size=56, big_size=140, small_color=CREAM, big_color=CORAL)


def s_split(cr, t, tl, t0):                                  # b12: here a few moments; on Earth 27 chatur-yugas
    b = tl["b12"]
    v = talk(tl, t, ("b12",))
    court(cr, t, t0, singers=False, dim=0.2, brahma_kw=dict(mouth=mouth_for(v)))
    p = prog(t, t0, 0.35)
    cr.set_source_rgba(0.05, 0.04, 0.12, 0.75 * p)
    cr.rectangle(0, 1250, W, 670)
    cr.fill()
    draw_text(cr, "HERE: A FEW MOMENTS", W / 2, 1330, 54, CREAM, p, MONO_FONT, "cm", tracking=2)
    hourglass(cr, W / 2 - 330, 1530, 0.55, t)
    te = b.start + b.dur * 0.55
    draw_text(cr, "EARTH:", W / 2 + 60, 1470, 54, CREAM, prog(t, te - 0.3, 0.3), MONO_FONT, "cm")
    draw_text(cr, "27 CHATUR-YUGAS", W / 2 + 60, 1570, 92, CORAL, prog(t, te, 0.3), anchor="cm")
    ring(cr, W / 2 + 60, 1570, 380, 80, prog(t, te + 0.3, 0.4), color=CORAL)


def s_balarama(cr, t, tl, t0):                               # b12b: give her to Balarama, who is on Earth now
    b = tl["b12b"]
    v = talk(tl, t, ("b12b",))
    court(cr, t, t0, singers=False, dim=0.25, brahma_kw=dict(mouth=mouth_for(v), abhaya=0.0))
    tb = b.start + b.dur * 0.35
    p = prog(t, tb, 0.5)
    if p > 0:
        soft_disc(cr, 540, 1560, 420, (0.6, 0.75, 1.0, 0.35 * p))
        figure(cr, t, 540, 1880, 0.95 * (0.6 + 0.4 * p), "balarama", arms=("hold", "down"), hold=plough, alpha_=p,
               seed=4)
        tag(cr, t, tb + 0.3, "BALARAMA", 540, 1240, 52)


def s_math(cr, t, tl, t0):                                   # b13: 1 chatur-yuga = 43,20,000 years; x27
    cosmos(cr, t)
    b = tl["b13"]
    draw_text(cr, "1 CHATUR-YUGA", W / 2, 640, 80, CREAM, prog(t, t0, 0.3), anchor="cm")
    draw_text(cr, "=", W / 2, 760, 80, CREAM, prog(t, t0 + 0.3, 0.3), MONO_FONT, "cm")
    draw_text(cr, "43,20,000 YEARS", W / 2, 880, 100, GOLDC, prog(t, b.start + b.dur * 0.25, 0.3), anchor="cm")
    tx = b.start + b.dur * 0.75
    p = prog(t, tx, 0.3)
    draw_text(cr, "× 27", W / 2, 1120, 200 * (1.2 - 0.2 * back(clamp((t - tx) / 0.3))) if p > 0 else 200, CORAL, p,
              MONO_FONT, "cm")


def s_total(cr, t, tl, t0):                                  # b14: over 11 crore years
    cosmos(cr, t)
    b = tl["b14"]
    year_counter(cr, t, t0, b.end - 0.2, W / 2, 900, size=120)
    headline(cr, t, "THAT IS MORE THAN", "11 CRORE YEARS", t0, b.start + b.dur * 0.5, y=330, small_size=56,
             big_size=130, small_color=CREAM, big_color=CORAL)
    soft_disc(cr, W / 2, 900, 600, (1, 0.8, 0.4, 0.08))


def s_rehook(cr, t, tl, t0):                                 # b15: the real shock: what did he see back on Earth?
    b = tl["b15"]
    k = clamp((t - t0) / max(0.5, b.dur))
    plate(cr, t, "clouds", t0, drift=(0, -260))
    figure(cr, t, 540, 900 + 600 * k, 1.2, "kakudmi", arms=("out", "out"), eyes="open", shadow=False,
           lookdir=(0, 0.8))
    tq = b.start + b.dur * 0.6
    p = prog(t, tq, 0.35)
    draw_text(cr, "?", W / 2, 520, 360 * (0.8 + 0.2 * back(clamp((t - tq) / 0.35))) if p > 0 else 300, CORAL, p,
              anchor="cm")
    headline(cr, t, "THE REAL SHOCK:", "WHAT DID HE SEE?", t0, tq, y=1450, small_size=56, big_size=110,
             small_color=CREAM, big_color=CORAL)


def bars(cr, t, t0, x, y, labels):
    for i, lab in enumerate(labels):
        ts = t0 + 0.45 * i
        p = prog(t, ts, 0.3)
        if p <= 0:
            continue
        yy = y + i * 120
        draw_text(cr, lab, x, yy, 44, CREAM, p, MONO_FONT, "lm", tracking=2)
        full, low = 360, 360 * (1 - 0.55 * prog(t, ts + 0.35, 0.5))
        cr.rectangle(x + 320, yy - 22, full, 44)
        cr.set_source_rgba(1, 1, 1, 0.15 * p)
        cr.fill()
        cr.rectangle(x + 320, yy - 22, low, 44)
        cr.set_source_rgba(*CORAL, p)
        cr.fill()
        draw_text(cr, "↓", x + 320 + full + 40, yy, 60, CORAL, prog(t, ts + 0.5, 0.3), "C:/Windows/Fonts/seguisym.ttf",
                  "cm")


def s_small(cr, t, tl, t0):                                  # b16: people had become smaller, weaker, duller
    b = tl["b16"]
    plate(cr, t, "street", t0)
    figure(cr, t, 380, 1700, 1.25, "kakudmi", arms=("hips", "down"), eyes="open", lookdir=(0.6, 0.6))
    for i, x in enumerate((640, 760, 880, 990)):
        figure(cr, t, x, 1700, 0.48, "villager", seed=i + 5, lookdir=(-0.8, -0.6))
    cr.set_source_rgba(0.05, 0.04, 0.1, 0.55 * prog(t, b.start + b.dur * 0.3, 0.3))
    cr.rectangle(40, 260, W - 80, 450)
    cr.fill()
    bars(cr, t, b.start + b.dur * 0.3, 90, 340, ["HEIGHT", "STRENGTH", "MIND"])
    tag(cr, t, b.start + b.dur * 0.2, "VISHNU PURANA 4.1", 540, 760, 34)


def terrace(cr, y=1640):
    """A carved sandstone terrace across the bottom of the Dwaraka shots, so characters stand on stone, not water."""
    g = cairo.LinearGradient(0, y, 0, H)
    g.add_color_stop_rgb(0, 0.86, 0.68, 0.46)
    g.add_color_stop_rgb(1, 0.55, 0.38, 0.24)
    cr.rectangle(0, y, W, H - y)
    cr.set_source(g)
    cr.fill()
    cr.rectangle(0, y, W, 14)
    cr.set_source_rgba(0.98, 0.86, 0.62, 1)
    cr.fill()
    for k in range(12):                                       # carved lotus band
        x = 45 + k * 90
        cr.arc(x, y + 60, 22, 0, 2 * math.pi)
        cr.set_source_rgba(0.45, 0.30, 0.18, 0.55)
        cr.set_line_width(4)
        cr.stroke()
        cr.arc(x, y + 60, 8, 0, 2 * math.pi)
        cr.fill()
    cr.rectangle(0, y + 100, W, 6)
    cr.set_source_rgba(0.40, 0.26, 0.16, 0.5)
    cr.fill()
    for x in (20, W - 20):                                    # railing posts at the edges
        cr.rectangle(x - 18, y - 120, 36, 120)
        cr.set_source_rgba(0.80, 0.62, 0.42, 1)
        cr.fill()
        cr.arc(x, y - 128, 22, 0, 2 * math.pi)
        cr.fill()


def s_dwaraka(cr, t, tl, t0):                                # b17: Kushasthali was now Dwaraka
    b = tl["b17"]
    plate(cr, t, "dwaraka", t0)
    terrace(cr)
    p = prog(t, t0, 0.35)
    cr.save()
    cr.translate(540, 520)
    cr.rotate(-0.03)
    cr.set_source_rgba(0.40, 0.24, 0.12, p)
    cr.rectangle(-360, -110, 720, 220)
    cr.fill()
    cr.set_source_rgba(*GOLDC, p)
    cr.set_line_width(6)
    cr.rectangle(-345, -95, 690, 190)
    cr.stroke()
    draw_text(cr, "KUSHASTHALI", 0, 0, 96, CREAM, p, anchor="cm")
    ts = b.start + b.dur * 0.5
    strike(cr, -320, 6, 320, -6, prog(t, ts, 0.35), color=CORAL)
    cr.restore()
    q = prog(t, ts + 0.35, 0.35)
    draw_text(cr, "DWARAKA", 540, 760, 150 * (1.1 - 0.1 * back(clamp((t - ts - 0.35) / 0.35))) if q > 0 else 150,
              CORAL, q, anchor="cm")
    figure(cr, t, 300, 1820, 1.1, "kakudmi", arms=("chin", "down"), eyes="open", lookdir=(0.7, -0.5))


def ruler(cr, x, y0, y1, a=1.0):
    cr.rectangle(x - 18, y1, 36, y0 - y1)
    cr.set_source_rgba(0.95, 0.85, 0.55, a)
    cr.fill()
    for k in range(int((y0 - y1) / 30)):
        yy = y0 - k * 30
        cr.move_to(x - 18, yy)
        cr.line_to(x - (4 if k % 5 else -8), yy)
    cr.set_source_rgba(0.3, 0.2, 0.1, a)
    cr.set_line_width(3)
    cr.stroke()


def s_tall(cr, t, tl, t0):                                   # b18: old-age Revati is much taller than Balarama
    b = tl["b18"]
    plate(cr, t, "dwaraka", t0, dim=0.15)
    terrace(cr)
    tr = b.start + b.dur * 0.55
    k = prog(t, tr, 0.6)
    figure(cr, t, 330, 1760, 1.05, "balarama", arms=("hold", "down"), hold=plough, seed=4, lookdir=(0.5, -0.6))
    figure(cr, t, 760, 1760, 1.05 + 0.55 * k, "revati", arms=("front", "down"), seed=2, lookdir=(-0.5, 0.4))
    ruler(cr, 545, 1760, 1760 - 980, prog(t, tr, 0.3))
    headline(cr, t, "FROM AN OLDER AGE:", "TOO TALL", t0, tr + 0.2, y=250, small_size=56, big_size=150,
             small_color=CREAM, big_color=CORAL)


def s_shrink(cr, t, tl, t0):                                 # b19: Balarama shortens her with the tip of his plough
    b = tl["b19"]
    plate(cr, t, "dwaraka", t0, dim=0.15)
    terrace(cr)
    tt = b.start + b.dur * 0.45
    k = prog(t, tt, 0.9)
    figure(cr, t, 330, 1760, 1.05, "balarama", arms=("point", "down"), hold=plough, seed=4, lookdir=(0.5, -0.6),
           halo_a=0.4 + 0.6 * prog(t, tt - 0.4, 0.4))
    figure(cr, t, 760, 1760, 1.6 - 0.55 * k, "revati", arms=("front", "down"), seed=2, lookdir=(-0.5, 0.0),
           eyes="happy" if k > 0.9 else "open")
    g = math.exp(-((t - tt - 0.4) / 0.4) ** 2)
    soft_disc(cr, 760, 1100, 500, (1, 0.9, 0.6, 0.45 * g))
    tag(cr, t, t0 + 0.3, "VISHNU PURANA 4.1", 540, 300, 36)


def s_awe(cr, t, tl, t0):                                    # b20: a few moments of waiting, crores of years apart
    cosmos(cr, t)
    b = tl["b20"]
    cr.save()
    cr.translate(540, 1000)
    cr.scale(3.2, 3.2)
    hourglass(cr, 0, 0, clamp((t - t0) / max(1.0, b.dur)), t)
    cr.restore()
    for k in range(40):                                       # star-sand falling through the neck
        ph = (t * 0.8 + k / 40) % 1
        cr.arc(540 + 6 * math.sin(k * 7.3), 935 + ph * 200, 3, 0, 2 * math.pi)
        cr.set_source_rgba(1, 0.95, 0.8, 0.9)
        cr.fill()
    headline(cr, t, "A FEW MOMENTS OF WAITING.", "CRORES OF YEARS", t0, b.start + b.dur * 0.5, y=260, small_size=52,
             big_size=120, small_color=CREAM, big_color=CORAL)


def s_end(cr, t, tl, t0):                                    # b21: would you go to Brahmaloka? yes or no
    b = tl["b21"]
    plate(cr, t, "brahmaloka", t0, dim=0.35)
    figure(cr, t, 540, 1250, 1.0, "kakudmi", arms=("front", "front"), lookdir=(0, -0.6))
    headline(cr, t, "WOULD YOU GO, KNOWING", "NO ONE WAITS?", t0, b.start + b.dur * 0.3, y=240, small_size=52,
             big_size=120, small_color=CREAM, big_color=CORAL)
    yes_no_card(cr, t, b.start + b.dur * 0.62, W / 2, 1480, w=600, h=300, question="COMMENT: YES OR NO")


SHOTS = [
    ("b1", None, s_hook), ("b1b", None, s_gone), ("b2", None, s_source), ("b3", None, s_king),
    ("b4", None, s_suitors), ("b5", None, s_ask), ("b6", None, s_rise), ("b7", None, s_court), ("b8", None, s_wait),
    ("b9", None, s_list), ("b10", None, s_laugh), ("b11", None, s_gone_names), ("b12", None, s_split),
    ("b12b", None, s_balarama), ("b13", None, s_math), ("b14", None, s_total), ("b15", None, s_rehook),
    ("b16", None, s_small), ("b17", None, s_dwaraka), ("b18", None, s_tall), ("b19", None, s_shrink),
    ("b20", None, s_awe), ("b21", None, s_end),
]
_SH = [(b, c, fn, "x") for b, c, fn in SHOTS]


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl, _SH)
    fn = _SH[k][2]
    cr.save()
    push(cr, t, t0, t1, 1.0, 1.045, cy=H * 0.5)
    fn(cr, t, tl, t0)
    cr.restore()
    flash = math.exp(-((t - t0) / 0.06) ** 2) if k > 0 else 0.0     # a soft white flash on each cut
    if flash > 0.02:
        cr.set_source_rgba(1, 0.97, 0.9, 0.18 * flash)
        cr.paint()
    grade(cr, t)


def sfx(tl):
    st = starts(tl, _SH)
    ev = [(s, "whoosh", 0.25) for s in st[1:]]
    ev += [(0.05, "bell", 0.0), (tl["b6"].start + 0.2, "shimmer", 0.0), (tl["b7"].start, "bell", 0.0),
           (tl["b10"].start, "shimmer", 0.0), (tl["b12b"].start + tl["b12b"].dur * 0.35, "conch", 0.0),
           (tl["b14"].start, "riser", 1.0), (tl["b19"].start + tl["b19"].dur * 0.45, "shimmer", 0.0),
           (tl["b20"].start, "bell", 0.0)]
    for bid in ("b4",):
        b = tl[bid]
        ev += [(b.start + b.dur * (0.12 + 0.16 * i) + 0.25, "pop", 0.0) for i in range(5)]
    ev += [(tl["b17"].start + tl["b17"].dur * 0.5, "scribble", 0.4), (tl["b16"].start + tl["b16"].dur * 0.3, "tick", 0)]
    for bid in ("b1b", "b12", "b14", "b15", "b20"):
        ev += [(tl[bid].start - 0.35, "tick", 0.0), (tl[bid].start - 0.35, "dip", 0.5)]
    return ev
