"""Scenes for mythology video 4 (King Bali and Vamana) in the owner's reference look (7 Nov 2026, "make it like this"):
painted cut-out characters (SDXL, cut out, one image per character so nobody changes) on painted sets, the reference's
paper devices (diorama.py) and two-tier headlines. Cues are line fractions so Hindi and Kannada stay in step."""
import math
import os

from channel import ASSETS_ROOT
from diorama import (GOLDC, calendar, checklist, cutout, dotted_path, finish, label_row, paper_clouds, slide, stage,
                     target, torn_note, torn_tag)
from poster import CORAL, CREAM, H, MONO_FONT, RED, W, back, clamp, draw_text, headline, prog, push, ring, yes_no_card
from shots import T, shot_at, starts

D = os.path.join(ASSETS_ROOT, "bali")
PICK = {"bali": 2031, "vamana": 2000, "shukra": 2000, "aditi": 2000, "foot": 2000}   # chosen seeds (set after review)


def C(name):
    return os.path.join(D, "chars", f"{name}_s{PICK[name]}.png")


def light_foot(cr, t, x, y, h, anchor="feet", flip=False, rot=0.0, alpha=1.0, glow=0.6, shadow=False):
    """Trivikrama's step as a foot and shin made of golden light (side view, toes forward), sole at (x, y), h px
    from sole to the top of the shin. Drawn in code: the generated feet looked like a woman's adorned feet."""
    import cairo
    if alpha <= 0 or h <= 2:
        return
    if glow > 0:
        g = cairo.RadialGradient(x, y - h * 0.45, 10, x, y - h * 0.45, h * 1.1)
        g.add_color_stop_rgba(0, 1, 0.9, 0.55, 0.5 * glow * alpha)
        g.add_color_stop_rgba(1, 1, 0.9, 0.55, 0)
        cr.set_source(g)
        cr.arc(x, y - h * 0.45, h * 1.1, 0, 2 * math.pi)
        cr.fill()
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(-h if flip else h, h)
    cr.translate(-0.5, 0)

    def foot_path():
        cr.move_to(0.02, 0)
        cr.curve_to(0.25, 0.025, 0.6, 0.03, 0.88, 0.0)           # sole
        cr.curve_to(0.97, -0.01, 1.06, -0.03, 1.05, -0.07)       # toe tip
        cr.curve_to(1.04, -0.12, 0.96, -0.14, 0.86, -0.14)       # top of the big toe
        cr.curve_to(0.72, -0.17, 0.6, -0.26, 0.5, -0.36)         # instep
        cr.curve_to(0.42, -0.45, 0.38, -0.6, 0.37, -1.0)         # ankle and shin
        cr.line_to(0.13, -1.0)
        cr.curve_to(0.13, -0.7, 0.12, -0.45, 0.1, -0.3)          # calf to the Achilles
        cr.curve_to(0.06, -0.2, -0.02, -0.12, 0.02, 0)           # heel
        cr.close_path()
    for k, (w, a_) in enumerate(((0.10, 0.10), (0.06, 0.16), (0.03, 0.25))):   # soft outer glow
        foot_path()
        cr.set_source_rgba(1, 0.85, 0.45, a_ * alpha)
        cr.set_line_width(w)
        cr.stroke()
    foot_path()
    g = cairo.LinearGradient(0, -1, 0.8, 0)
    g.add_color_stop_rgba(0, 1.0, 0.97, 0.85, 0.92 * alpha)
    g.add_color_stop_rgba(0.6, 1.0, 0.80, 0.35, alpha)
    g.add_color_stop_rgba(1, 0.92, 0.55, 0.15, alpha)
    cr.set_source(g)
    cr.fill_preserve()
    cr.set_source_rgba(1, 0.98, 0.85, 0.9 * alpha)
    cr.set_line_width(0.012)
    cr.stroke()
    for k in range(4):                                     # toe lines
        tx = 0.98 + 0.05 * k
        cr.move_to(tx, -0.04)
        cr.line_to(tx - 0.03, -0.13 + 0.015 * k)
    cr.set_source_rgba(0.85, 0.5, 0.15, 0.5 * alpha)
    cr.set_line_width(0.01)
    cr.stroke()
    cr.restore()
    for k in range(14):                                    # sparkles
        ph = (t * 0.7 + k / 14) % 1
        sx = x + (math.sin(k * 3.7) * 0.6) * h
        sy = y - h * (0.1 + 1.1 * ph)
        cr.arc(sx, sy, 3 + 2 * math.sin(k + t * 3), 0, 2 * math.pi)
        cr.set_source_rgba(1, 0.95, 0.7, 0.8 * alpha * (1 - ph))
        cr.fill()


def S(name):
    return os.path.join(D, f"{name}.png")


def F(tl, bid, f):
    return T(tl, bid, f)


PAINTING = os.path.join(D, "cma_167578_bali_vamana.jpg")   # CC0, Cleveland Museum of Art
USED_ASSETS = ["cma_167578_bali_vamana.jpg"]        # the rest was generated on the laptop
CREDITS_FILES = [os.path.join(D, "credits.json")]
NIGHT = (0.08, 0.09, 0.20)


def plain(cr, col=NIGHT):
    import cairo
    g = cairo.RadialGradient(W / 2, H * 0.45, 100, W / 2, H * 0.5, H * 0.8)
    g.add_color_stop_rgb(0, *(min(1, c * 1.8) for c in col))
    g.add_color_stop_rgb(1, *(c * 0.6 for c in col))
    cr.set_source(g)
    cr.paint()


def floor(cr, y=1560, col=(0.22, 0.16, 0.13)):
    """A plain stage floor for the frame-0 shot."""
    import cairo
    g = cairo.LinearGradient(0, y, 0, H)
    g.add_color_stop_rgb(0, *col)
    g.add_color_stop_rgb(1, *(c * 0.5 for c in col))
    cr.rectangle(0, y, W, H - y)
    cr.set_source(g)
    cr.fill()


def hl(cr, t, small, big, t_small, t_big, y=230, big_color=CORAL, big_size=130, **kw):
    headline(cr, t, small, big, t_small, t_big, y=y, small_size=56, big_size=big_size, small_color=CREAM,
             big_color=big_color, **kw)


def top_band(cr, alpha=0.8, h=620):
    """A soft dark band behind the headline on bright sets (the gold heaven gates), so the text reads."""
    import cairo
    g = cairo.LinearGradient(0, 0, 0, h)
    g.add_color_stop_rgba(0, 0.04, 0.03, 0.06, alpha)
    g.add_color_stop_rgba(0.65, 0.04, 0.03, 0.06, alpha * 0.7)
    g.add_color_stop_rgba(1, 0.04, 0.03, 0.06, 0)
    cr.set_source(g)
    cr.rectangle(0, 0, W, h)
    cr.fill()


TAG = ("DIWALI · DAY 4 · ", "BALI PADYAMI")


# ---------------------------------------------------------------- shots
def s_hook(cr, t, tl, t0):                        # v1: God took everything... then promised: you'll be king of heaven
    plain(cr, (0.16, 0.10, 0.08))
    floor(cr)
    label_row(cr, "THE PROMISE · BHAGAVATA PURANA", "FIG. 1")
    cutout(cr, t, C("bali"), W / 2, 1640, 1180, glow=0.25 * prog(t, F(tl, "v1", 0.6), 0.6))
    hl(cr, t, "GOD TOOK EVERYTHING...", "THEN MADE A PROMISE", 0.05, min(1.8, F(tl, "v1", 0.4)), t_ghost=0.35,
       big_size=118)
    if t > F(tl, "v1", 0.75):
        torn_note(cr, t, F(tl, "v1", 0.75), "YOU'LL BE KING OF HEAVEN", W / 2, 1720, size=46)


def s_village(cr, t, tl, t0):                     # v2: believed: the day after Diwali he still visits his people
    stage(cr, t, S("village"), t0)
    label_row(cr, "THE VILLAGE · DIWALI NIGHT", "FIG. 2")
    torn_tag(cr, t, t0 + 0.2, *TAG, W - 300, 170)
    cutout(cr, t, C("bali"), W / 2, 1880, 760, alpha=prog(t, F(tl, "v2", 0.45), 0.6), glow=0.6)
    hl(cr, t, "EVERY YEAR, IT IS BELIEVED,", "HE COMES BACK", t0, F(tl, "v2", 0.5), y=260, big_size=120)


def s_source(cr, t, tl, t0):                      # v3: the story of King Bali, Bhagavata Purana canto 8
    stage(cr, t, S("swarga"), t0, dim=0.35)
    top_band(cr)
    label_row(cr, "BHAGAVATA PURANA · CANTO 8", "FIG. 3")
    cutout(cr, t, C("bali"), slide(t, t0, -300, 540), 1800, 1050)
    torn_note(cr, t, F(tl, "v3", 0.45), "BHAGAVATA PURANA", W / 2, 420, size=56, lines=["BHAGAVATA PURANA",
                                                                                         "CANTO 8"])
    torn_tag(cr, t, t0 + 0.3, "KING ", "BALI", 240, 640, size=34)


def s_conquest(cr, t, tl, t0):                    # v4: king of the asuras, defeated Indra, won heaven
    stage(cr, t, S("swarga"), t0)
    top_band(cr)
    label_row(cr, "SWARGA · HEAVEN", "FIG. 4")
    cutout(cr, t, C("bali"), W / 2, 1820, 1000)
    hl(cr, t, "AN ASURA KING", "WON HEAVEN", t0, F(tl, "v4", 0.55), y=250)
    worlds = (("EARTH", 0.25), ("SKY", 0.45), ("HEAVEN", 0.65))
    for i, (name, f) in enumerate(worlds):
        x = 210 + i * 330
        q = prog(t, F(tl, "v4", f), 0.3)
        if q > 0:
            torn_tag(cr, t, F(tl, "v4", f), f"{name}: ", "BALI", x, 620 + 30 * (i % 2), size=24, seed=10 + i)


def s_vamana(cr, t, tl, t0):                      # v5: Aditi prays; Vishnu comes as her son, the little Vamana
    plain(cr, (0.12, 0.10, 0.22))
    paper_clouds(cr, t, y0=300)
    label_row(cr, "ADITI'S PRAYER", "FIG. 5")
    cutout(cr, t, C("aditi"), 330, 1700, 820, alpha=prog(t, t0, 0.4))
    tv = F(tl, "v5", 0.55)
    g = prog(t, tv - 0.3, 0.5)
    cutout(cr, t, C("vamana"), 780, 1720, 760 * (0.6 + 0.4 * g), alpha=g, glow=1.0 - 0.6 * prog(t, tv + 0.6, 0.8))
    hl(cr, t, "GOD CAME AS A SMALL BOY:", "VAMANA", t0, F(tl, "v5", 0.75), y=260, big_size=150)


def footprints(cr, t, t0, x, y, n=3, gap=120):
    for i in range(n):
        p = prog(t, t0 + 0.25 * i, 0.25)
        if p <= 0:
            continue
        cx = x + i * gap
        cr.save()
        cr.translate(cx, y - 20 * (i % 2))
        cr.rotate(-0.2)
        cr.set_source_rgba(*CORAL, p)
        cr.scale(1, 1.7)
        cr.arc(0, 0, 22, 0, 2 * math.pi)
        cr.fill()
        cr.restore()
        for k in range(5):
            cr.arc(cx - 20 + k * 10, y - 60 - 20 * (i % 2) - (k % 2) * 4, 7, 0, 2 * math.pi)
            cr.set_source_rgba(*CORAL, p)
            cr.fill()


def s_ask(cr, t, tl, t0):                         # v6: the yajna; Vamana asks for three steps, measured by his own feet
    stage(cr, t, S("yajna"), t0)
    label_row(cr, "BALI'S YAJNA", "FIG. 6")
    cutout(cr, t, C("bali"), 760, 1820, 1000)
    cutout(cr, t, C("vamana"), slide(t, t0, -200, 290), 1820, 640)
    tq = F(tl, "v6", 0.55)
    hl(cr, t, "HE ASKED FOR JUST", "3 STEPS", tq - 0.3, tq, y=250, big_size=170)
    footprints(cr, t, tq + 0.3, 340, 760)


def s_smile(cr, t, tl, t0):                       # v7: Bali smiles: just three steps? take what you need
    stage(cr, t, S("yajna"), t0, dim=0.1)
    label_row(cr, "BALI'S YAJNA", "FIG. 6")
    cutout(cr, t, C("bali"), 600, 1840, 1120)
    cutout(cr, t, C("vamana"), 220, 1840, 600)
    torn_note(cr, t, F(tl, "v7", 0.35), "JUST 3 STEPS? TAKE THEM.", W / 2, 420, size=50)


def painting(cr, t, t0, t1, f0, f1, z0, z1):
    """The CC0 Pahari painting, panned and zoomed from point f0 to f1 (fractions of the image) over the shot."""
    import cairo
    from diorama import _img
    img = _img(PAINTING, 3400)
    k = clamp((t - t0) / max(0.5, t1 - t0))
    k = k * k * (3 - 2 * k)
    fx, fy = f0[0] + (f1[0] - f0[0]) * k, f0[1] + (f1[1] - f0[1]) * k
    z = (z0 + (z1 - z0) * k) * H / img.get_height()
    cr.set_source_rgb(0.08, 0.05, 0.04)
    cr.paint()
    cr.save()
    cr.translate(W / 2, H / 2)
    cr.scale(z, z)
    cr.translate(-fx * img.get_width(), -fy * img.get_height())
    cr.set_source_surface(img, 0, 0)
    cr.paint()
    cr.restore()


def s_warn(cr, t, tl, t0):                        # v8: Shukracharya: this boy is Vishnu; he will take everything
    b = tl["v8"]
    painting(cr, t, t0, b.end, (0.20, 0.57), (0.40, 0.62), 2.2, 1.6)
    label_row(cr, "PAHARI PAINTING, 1700s · CLEVELAND MUSEUM OF ART", "FIG. 7")
    tn = F(tl, "v8", 0.3)
    import cairo
    q = prog(t, F(tl, "v8", 0.6), 0.3)
    if q > 0:                                                # a dark band so the red words read on the painting
        g = cairo.LinearGradient(0, 470, 0, 700)
        g.add_color_stop_rgba(0, 0.05, 0.03, 0.02, 0)
        g.add_color_stop_rgba(0.25, 0.05, 0.03, 0.02, 0.75 * q)
        g.add_color_stop_rgba(0.75, 0.05, 0.03, 0.02, 0.75 * q)
        g.add_color_stop_rgba(1, 0.05, 0.03, 0.02, 0)
        cr.set_source(g)
        cr.rectangle(0, 470, W, 230)
        cr.fill()
    torn_note(cr, t, tn, "THE BOY IS VISHNU", W / 2, 360, size=60)
    hl(cr, t, "", "HE'LL TAKE EVERYTHING", F(tl, "v8", 0.6), F(tl, "v8", 0.65), y=470, big_size=96)
    torn_tag(cr, t, t0 + 0.4, "GURU ", "SHUKRACHARYA", 330, 1500, size=30, seed=21)


def s_promise(cr, t, tl, t0):                     # v9: I gave my word; I will not step back
    stage(cr, t, S("yajna"), t0, dim=0.2)
    label_row(cr, "THE WORD", "FIG. 8")
    cutout(cr, t, C("bali"), W / 2, 1840, 1250, glow=0.4)
    ts = F(tl, "v9", 0.55)
    p = prog(t, ts, 0.25)
    if p > 0:
        s = 1.6 - 0.6 * back(clamp((t - ts) / 0.25))
        cr.save()
        cr.translate(W / 2, 460)
        cr.rotate(-0.12)
        cr.scale(s, s)
        cr.set_source_rgba(*RED, p)
        cr.set_line_width(10)
        cr.rectangle(-330, -70, 660, 140)
        cr.stroke()
        draw_text(cr, "PROMISE KEPT", 0, 0, 96, RED, p, anchor="cm")
        cr.restore()


def water(cr, t, t0, x, y, length, a=1.0):
    p = clamp((t - t0) / 0.6)
    if p <= 0:
        return
    for k in range(18):
        ph = (t * 2.2 + k / 18) % 1
        yy = y + ph * length * p
        cr.arc(x + 6 * math.sin(k * 3.1 + t * 5), yy, 6, 0, 2 * math.pi)
        cr.set_source_rgba(0.75, 0.9, 1.0, 0.8 * a)
        cr.fill()


def s_grow(cr, t, tl, t0):                        # v10: the gift-water falls; Vamana grows and keeps growing
    stage(cr, t, S("yajna"), t0, dim=0.15)
    label_row(cr, "THE GIFT", "FIG. 9")
    b = tl["v10"]
    tg = F(tl, "v10", 0.3)
    k = clamp((t - tg) / max(0.5, b.end - tg))
    cutout(cr, t, C("bali"), 820, 1840, 900)
    water(cr, t, t0 + 0.2, 640, 1150, 380)
    hgt = 640 * (1 + 4.5 * k ** 1.6)                        # Vamana outgrows the frame
    cutout(cr, t, C("vamana"), 300, 1840 + 0.15 * (hgt - 640), hgt, glow=min(1, k * 1.5))
    hl(cr, t, "HE GREW...", "AND GREW", t0, F(tl, "v10", 0.6), y=230, big_size=150)


def s_steps(cr, t, tl, t0):                       # v11: first step the earth, second the whole sky up to heaven
    stage(cr, t, S("cosmos"), t0, drift=(0, 30))
    label_row(cr, "TRIVIKRAMA · THE THREE STEPS", "FIG. 10")
    t1, t2 = F(tl, "v11", 0.05), F(tl, "v11", 0.5)
    # the same Vamana, now so tall that only his legs are in frame; he strides across, then rises out of the top
    k1 = back(clamp((t - t1) / 0.7)) if t >= t1 else 0.0
    k2 = clamp((t - t2) / 1.2) if t >= t2 else 0.0
    feet_y = 1500 - 1700 * k2 * k2
    x = -300 + 760 * k1 + 240 * k2
    cutout(cr, t, C("vamana"), x, feet_y, 7200 + 9000 * k2, glow=0.9, bob=0.0)
    for i, (tf, fx, fy) in enumerate(((t1 + 0.5, 520, 1430), (t2 + 0.4, 700, 300))):   # glowing footprints
        q = prog(t, tf, 0.4)
        if q > 0:
            import cairo
            g = cairo.RadialGradient(fx, fy, 5, fx, fy, 140)
            g.add_color_stop_rgba(0, 1, 0.92, 0.6, 0.85 * q)
            g.add_color_stop_rgba(1, 1, 0.92, 0.6, 0)
            cr.set_source(g)
            cr.arc(fx, fy, 140, 0, 2 * math.pi)
            cr.fill()
    checklist(cr, t, 70, 1320, 640, "TRIVIKRAMA · STEPS", [("STEP 1: EARTH", t1 + 0.4), ("STEP 2: SKY", t2 + 0.4)])


def crack(cr, t, t0, x, y):
    p = clamp((t - t0) / 0.6)
    if p <= 0:
        return
    import random
    rnd = random.Random(5)
    cr.set_source_rgba(1, 0.92, 0.6, p)
    cr.set_line_width(5)
    for k in range(7):
        ang = -math.pi / 2 + (k - 3) * 0.32
        L = 260 * p * rnd.uniform(0.6, 1.0)
        cr.move_to(x, y)
        cx, cy = x, y
        for s in range(4):
            cx += math.cos(ang + rnd.uniform(-0.4, 0.4)) * L / 4
            cy += math.sin(ang + rnd.uniform(-0.4, 0.4)) * L / 4
            cr.line_to(cx, cy)
        cr.stroke()


def ganga(cr, t, t0, x, y, length):
    import cairo
    p = clamp((t - t0) / 1.2)
    if p <= 0:
        return
    for k in range(3):
        w = 70 - 20 * k
        g = cairo.LinearGradient(x, y, x, y + length * p)
        g.add_color_stop_rgba(0, 0.85, 0.97, 1.0, 0.9 - 0.2 * k)
        g.add_color_stop_rgba(1, 0.55, 0.85, 1.0, 0.2)
        cr.set_source(g)
        cr.move_to(x - w / 2, y)
        for i in range(21):
            f = i / 20
            cr.line_to(x - w / 2 + 18 * math.sin(f * 9 + t * 4 + k), y + length * p * f)
        for i in range(20, -1, -1):
            f = i / 20
            cr.line_to(x + w / 2 + 18 * math.sin(f * 9 + t * 4 + k + 1), y + length * p * f)
        cr.close_path()
        cr.fill()
    for k in range(30):
        ph = (t * 1.5 + k / 30) % 1
        cr.arc(x + 40 * math.sin(k * 2.3), y + length * p * ph, 4, 0, 2 * math.pi)
        cr.set_source_rgba(1, 1, 1, 0.8 * (1 - ph))
        cr.fill()


def s_ganga(cr, t, tl, t0):                       # v12: the toe-nail pierces the shell of the universe; the Ganga flows in
    stage(cr, t, S("cosmos"), t0, zoom=1.15)
    label_row(cr, "THE SHELL OF THE UNIVERSE · 5.17.1", "FIG. 11")
    tc = F(tl, "v12", 0.4)
    import cairo
    g = cairo.RadialGradient(640, 230, 5, 640, 230, 420)
    g.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.9 * prog(t, tc - 0.6, 0.6))
    g.add_color_stop_rgba(1, 1, 0.95, 0.75, 0)
    cr.set_source(g)
    cr.arc(640, 230, 420, 0, 2 * math.pi)
    cr.fill()
    crack(cr, t, tc, 640, 230)
    ganga(cr, t, F(tl, "v12", 0.7), 640, 230, 1450)
    if t > F(tl, "v12", 0.72):
        torn_note(cr, t, F(tl, "v12", 0.78), "GANGA", 820, 1500, size=80, rot=0.04)
    hl(cr, t, "THE UNIVERSE CRACKED,", "GANGA FLOWED IN", t0, tc + 0.2, y=230, big_size=110)


def s_third(cr, t, tl, t0):                       # v13 (re-hook): where to put the third step? nothing was left
    plain(cr, (0.07, 0.07, 0.15))
    paper_clouds(cr, t, y0=600, alpha=0.5)
    label_row(cr, "STEP 3", "FIG. 12")
    footprints(cr, t, t0 + 0.2, 380, 900, n=2, gap=180)
    tq = F(tl, "v13", 0.25)
    p = prog(t, tq, 0.35)
    draw_text(cr, "?", 740, 880, 340 * (0.8 + 0.2 * back(clamp((t - tq) / 0.35))) if p > 0 else 300, CORAL, p,
              anchor="cm")
    hl(cr, t, "STEP 3:", "NOTHING LEFT", t0, F(tl, "v13", 0.6), y=300, big_size=150)


def s_head(cr, t, tl, t0):                        # v14: Bali bows: place the third step on my head
    stage(cr, t, S("yajna"), t0, dim=0.45)
    label_row(cr, "THE THIRD STEP · 8.22.2", "FIG. 13")
    tb = F(tl, "v14", 0.2)
    bow = 0.22 * prog(t, tb, 0.8)
    cutout(cr, t, C("bali"), W / 2, 1880, 1100, rot=bow * 0.5, glow=0.3)
    tf = F(tl, "v14", 0.6)
    if t > tf - 0.6:                                         # a gentle golden light comes down onto his head
        import cairo
        y = -200 + 900 * prog(t, tf - 0.6, 1.2)
        g = cairo.RadialGradient(W / 2, y, 10, W / 2, y, 360)
        g.add_color_stop_rgba(0, 1, 0.93, 0.65, 0.9)
        g.add_color_stop_rgba(1, 1, 0.93, 0.65, 0)
        cr.set_source(g)
        cr.arc(W / 2, y, 360, 0, 2 * math.pi)
        cr.fill()
    torn_note(cr, t, F(tl, "v14", 0.5), "ON MY HEAD", W / 2, 1720, size=72)


def s_sutala(cr, t, tl, t0):                      # v15: the twist: Sutala, a world even the gods want
    stage(cr, t, S("sutala"), t0)
    label_row(cr, "SUTALA · 8.22.33", "FIG. 14")
    cutout(cr, t, C("bali"), W / 2, 1860, 980, glow=0.5)
    hl(cr, t, "THE TWIST:", "SUTALA", t0, F(tl, "v15", 0.35), y=240, big_size=170)
    torn_note(cr, t, F(tl, "v15", 0.7), "EVEN THE GODS WANT IT", W / 2, 640, size=52)


def s_with_you(cr, t, tl, t0):                    # v16: I shall always be with you and protect you
    stage(cr, t, S("sutala"), t0, dim=0.2)
    label_row(cr, "THE PROMISE · 8.22.35", "FIG. 15")
    cutout(cr, t, C("bali"), 380, 1860, 900)
    cutout(cr, t, C("vamana"), 800, 1860, 640, glow=0.9)
    torn_note(cr, t, F(tl, "v16", 0.25), "I SHALL ALWAYS BE WITH YOU", W / 2, 430, size=50)
    torn_note(cr, t, F(tl, "v16", 0.65), "AND PROTECT YOU", W / 2, 560, size=50, seed=11, rot=0.02)


def s_future(cr, t, tl, t0):                      # v17: in Savarni Manu's age, you will be king of heaven
    stage(cr, t, S("swarga"), t0)
    top_band(cr)
    label_row(cr, "THE FUTURE · SAVARNI MANU · 8.22.31", "FIG. 16")
    cutout(cr, t, C("bali"), W / 2, 1840, 1080, glow=0.8)
    hl(cr, t, "ONE DAY, KING OF", "HEAVEN", t0, F(tl, "v17", 0.6), y=240, big_size=180, big_color=GOLDC)


def s_padyami(cr, t, tl, t0):                     # v18: Bali Pratipada / Bali Padyami: he returns to his people
    stage(cr, t, S("village"), t0)
    label_row(cr, "THE DAY AFTER DIWALI", "FIG. 17")
    torn_tag(cr, t, t0 + 0.1, *TAG, W - 300, 170)
    calendar(cr, t, F(tl, "v18", 0.25), W / 2, 330, "NOVEMBER", 2026, 0, 30, marks={8}, highlight=10)
    cutout(cr, t, C("bali"), W / 2, 1880, 640, alpha=prog(t, F(tl, "v18", 0.65), 0.6), glow=1.0)
    dotted_path(cr, t, F(tl, "v18", 0.6), [(120, 1650), (360, 1560), (540, 1620), (720, 1540), (960, 1640)])


def s_awe(cr, t, tl, t0):                         # v19: gave everything for his word; got what even the gods don't
    plain(cr, (0.14, 0.09, 0.05))
    floor(cr, 1600, (0.25, 0.17, 0.10))
    label_row(cr, "THE PROMISE · BHAGAVATA PURANA", "FIG. 18")
    cutout(cr, t, C("bali"), W / 2, 1700, 1180, glow=0.9)
    hl(cr, t, "HE GAVE EVERYTHING.", "HE GOT MORE", t0, F(tl, "v19", 0.55), y=240, big_size=150, big_color=GOLDC)


def s_end(cr, t, tl, t0):                         # v20: would you keep your word? yes or no
    stage(cr, t, S("village"), t0, dim=0.35)
    label_row(cr, "YOUR TURN", "FIG. 19")
    cutout(cr, t, C("bali"), W / 2, 1300, 760)
    hl(cr, t, "IN BALI'S PLACE,", "WOULD YOU KEEP IT?", t0, F(tl, "v20", 0.3), y=240, big_size=110)
    yes_no_card(cr, t, F(tl, "v20", 0.55), W / 2, 1520, w=600, h=300, question="COMMENT: YES OR NO")


SHOTS = [("v1", s_hook), ("v2", s_village), ("v3", s_source), ("v4", s_conquest), ("v5", s_vamana), ("v6", s_ask),
         ("v7", s_smile), ("v8", s_warn), ("v9", s_promise), ("v10", s_grow), ("v11", s_steps), ("v12", s_ganga),
         ("v13", s_third), ("v14", s_head), ("v15", s_sutala), ("v16", s_with_you), ("v17", s_future),
         ("v18", s_padyami), ("v19", s_awe), ("v20", s_end)]
_SH = [(b, None, fn, "x") for b, fn in SHOTS]


def draw(cr, t, tl):
    k, t0, t1 = shot_at(t, tl, _SH)
    cr.save()
    push(cr, t, t0, t1, 1.0, 1.04, cy=H * 0.5)
    _SH[k][2](cr, t, tl, t0)
    cr.restore()
    finish(cr, t)


def sfx(tl):
    st = starts(tl, _SH)
    ev = [(s, "whoosh", 0.25) for s in st[1:]]
    ev += [(0.05, "bell", 0.0), (tl["v5"].start + tl["v5"].dur * 0.5, "shimmer", 0.0),
           (tl["v9"].start + tl["v9"].dur * 0.55, "thud", 0.0), (tl["v10"].start, "riser", 1.5),
           (tl["v11"].start + tl["v11"].dur * 0.05, "hit", 0.0), (tl["v11"].start + tl["v11"].dur * 0.5, "hit", 0.0),
           (tl["v12"].start + tl["v12"].dur * 0.4, "slam", 0.0), (tl["v12"].start + tl["v12"].dur * 0.7, "shimmer", 0.0),
           (tl["v14"].start + tl["v14"].dur * 0.6, "bell", 0.0), (tl["v16"].start, "conch", 0.0),
           (tl["v18"].start, "bell", 0.0)]
    for bid in ("v8", "v12", "v13", "v15", "v19"):
        ev += [(tl[bid].start - 0.35, "tick", 0.0), (tl[bid].start - 0.35, "dip", 0.5)]
    return ev
