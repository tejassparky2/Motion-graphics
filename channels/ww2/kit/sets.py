"""WW2 kit: the recurring set backgrounds from SHOTLIST.md, full-frame (1920x1080) poster paintings.

Each set is a class built once and drawn every frame in the current coordinates, so a scene can wrap it in its
push-in. Options go to the constructor or to draw() for one frame:

    sky = Sky(mode="dusk")
    sky.draw(cr, t)                         # then props, figures, fx on top ... and print_finish(cr, t) last

Sky(mode="day"|"dusk"|"night"|"sunset", horizon=760, clouds=5, rays=False)
    flat banded sky (no gradients), drifting poster clouds; night has stars and a cream moon; sunset a low GOLD sun
    (never red, never with rays: STYLE.md's Rising Sun rule)
Ocean(horizon=760, mode="day"|"night", swell=1.0)     printed sea with hatching that slides and bobs; .depth(y)
TrenchLine(horizon=620, night=False)    no-man's land: craters, dead stumps, wire, and the trench parapet in front
Skyline(city="london"|"paris"|"moscow"|"berlin"|"pacific"|"generic", ground=820, tone=None, night=False, lit=0.3)
    a city silhouette on the ground line (one tone; lit windows at night). Moscow's tower carries a plain red star.
SigningRoom(kind="hall"|"office")       the Hall of Mirrors (arched mirrors, chandeliers) or a panelled office;
                                        put a things.LongTable / props.SigningTable in front
BletchleyHut()                          a wooden codebreakers' hut: plank walls, blackout window, swinging lamp,
                                        a blackboard of letter groups; add Bombe / Enigma / Papers in front
BunkerCorridor(close=1.0)               a concrete corridor in one-point perspective ending in the blast door
Courtroom()                             panelled courtroom: the judges' bench, the dock rail in front
ShipDeck()                              a battleship's teak deck (the Missouri), a big turret behind, sea beyond

`python -m channels.ww2.kit.sets` writes out/ww2/style/props_sheet_4_sets.png (every set, 4x4 thumbnails).
"""
import math
import random

from channels.ww2.kit.core import H, STENCIL, W, lerp, paper, rays, text
from channels.ww2.kit.fx import blob, cloud
from channels.ww2.kit.props import (TAU, BarbedWire, Destroyer, Sandbags, dots, ellipse, fill, fill_ink, glow, ink, line, mix,
                                    poly, rrect, shade, smoke, star)
from channels.ww2.kit.things import (BRASS, CONCRETE, GLASS, STEEL, STONE, WOOD, WOOD_DK, BunkerDoor, Island,
                                     LongTable, TurretCloseup)


class Set:
    defaults = {}

    def __init__(self, **kw):
        self.o = dict(self.defaults)
        self.o.update(kw)

    def draw(self, cr, t, **kw):
        o = dict(self.o)
        o.update(kw)
        cr.save()
        self._draw(cr, t, o)
        cr.restore()

    def _draw(self, cr, t, o):
        raise NotImplementedError


def bands(cr, y0, y1, colors):
    """Flat horizontal colour bands from y0 to y1 (poster banding instead of a gradient)."""
    n = len(colors)
    for i, c in enumerate(colors):
        cr.rectangle(-200, lerp(y0, y1, i / n), W + 400, (y1 - y0) / n + 1)
        fill(cr, c)


# ================================================================ SKY
SKIES = {
    "day": ("#c9c3a8", "#d6d0b6", "#e2dcc4"),
    "dusk": ("#8f8a78", "#b3a888", "#d2b77c", "#e2c27a"),
    "sunset": ("#6f6a5a", "#a08c63", "#cf9d4a", "#e7b65a"),
    "night": ("#1f2430", "#262c3a", "#2f3647"),
}


class Sky(Set):
    defaults = dict(mode="day", horizon=760, clouds=5, rays=False, seed=3, drift=12.0)

    def _draw(self, cr, t, o):
        hz = o["horizon"]
        paper(cr)
        bands(cr, -200, hz, SKIES.get(o["mode"], SKIES["day"]))
        night = o["mode"] == "night"
        if o["rays"] and not night:
            rays(cr, t, W * 0.5, hz, n=28, color="khaki", alpha=0.25, spin=0.015)
        if night:
            r = random.Random(o["seed"])
            for i in range(120):
                x, y = r.uniform(0, W), r.uniform(0, hz * 0.85)
                tw = 0.6 + 0.4 * math.sin(t * r.uniform(1, 3) + i)
                cr.arc(x, y, r.uniform(1.2, 2.6), 0, TAU)
                fill(cr, "cream", 0.8 * tw)
            cr.arc(W * 0.78, hz * 0.22, 58, 0, TAU)
            fill_ink(cr, "cream", 4, tone=False)
            cr.arc(W * 0.78 + 20, hz * 0.22 - 10, 52, 0, TAU)
            fill(cr, SKIES["night"][0])
        if o["mode"] == "sunset":
            cr.arc(W * 0.62, hz - 10, 120, math.pi, TAU)                     # low gold sun, no rays
            fill_ink(cr, "gold", 5, tone=False)
            for i in range(4):
                y = hz - 30 - i * 26
                cr.rectangle(W * 0.62 - 130, y, 260, 6 + i)
                fill(cr, SKIES["sunset"][2])
        r = random.Random(o["seed"] + 1)
        for i in range(int(o["clouds"])):
            w = r.uniform(260, 520)
            y = r.uniform(hz * 0.15, hz * 0.7)
            x = (r.uniform(0, W + 600) + o["drift"] * t * (0.5 + y / hz)) % (W + 600) - 300
            c = "#3a4152" if night else mix("cream", SKIES.get(o["mode"], SKIES["day"])[0], 0.35 * (1 - y / hz))
            cloud(cr, x, y, w, seed=o["seed"] * 10 + i, color=c, dense=1)


# ================================================================ OCEAN
class Ocean(Set):
    defaults = dict(horizon=760, mode="day", swell=1.0, color=None)

    def depth(self, y):
        hz = self.o["horizon"]
        return max(0.0, (y - hz) / (H - hz))

    def _draw(self, cr, t, o):
        hz = o["horizon"]
        night = o["mode"] == "night"
        sea = o["color"] or ("#2c3a3e" if night else "sea")
        hatch = shade(sea, -0.25) if night else "sea_dk"
        cr.rectangle(-200, hz, W + 400, H - hz + 200)
        fill(cr, sea)
        y = hz + 4.0
        i = 0
        while y < H + 60:
            k = (y - hz) / (H - hz)
            off = (t * (8 + 30 * k) + i * 37) % 80
            bob = math.sin(t * 1.6 + i * 0.7) * 4 * k * o["swell"]
            cr.set_dash([40 + 160 * k, 14 + 40 * k], -off)
            line(cr, -100, y + bob, W + 100, y + bob, max(1.2, 3.4 * k + 0.8), hatch, 0.9)
            cr.set_dash([])
            y += 5 + 26 * k
            i += 1
        line(cr, -100, hz, W + 100, hz, 3, "ink")


# ================================================================ TRENCH LINE
class TrenchLine(Set):
    defaults = dict(horizon=620, night=False, seed=4, ground="#8b7a5c", mud="#6b5a40")

    def _draw(self, cr, t, o):
        hz = o["horizon"]
        Sky(mode="night" if o["night"] else "dusk", horizon=hz, clouds=3, seed=o["seed"]).draw(cr, t)
        cr.rectangle(-200, hz, W + 400, H - hz + 200)
        fill(cr, o["ground"])
        cr.rectangle(-200, hz, W + 400, H - hz + 200)
        dots(cr, shade(o["ground"], -0.3), 1, 0.8)
        cr.new_path()
        r = random.Random(o["seed"])
        for i in range(14):                                                    # shell craters
            y = hz + 30 + r.random() ** 1.4 * (H - hz - 260)
            k = 0.3 + (y - hz) / (H - hz)
            x = r.uniform(0, W)
            ellipse(cr, x, y, 110 * k, 22 * k)
            fill_ink(cr, o["mud"], 3, tone=False)
            ellipse(cr, x, y + 4 * k, 80 * k, 12 * k)
            fill(cr, "#8d9488")
        for i in range(6):                                                     # dead stumps
            x = r.uniform(40, W - 40)
            y = hz + r.uniform(10, 120)
            hgt = r.uniform(60, 160)
            poly(cr, [(x - 9, y), (x - 6, y - hgt), (x - 1, y - hgt * 0.85), (x + 4, y - hgt * 1.05), (x + 9, y)])
            fill(cr, "#3b3633")
            line(cr, x + 2, y - hgt * 0.6, x + 26, y - hgt * 0.8, 4, "#3b3633")
        for k, (y, sc) in enumerate(((hz + 60, 0.35), (hz + 170, 0.6))):       # two belts of wire
            for j in range(4):
                BarbedWire(length=620, seed=k * 4 + j, silhouette="#2b2724").draw(
                    cr, t, x=-200 + j * 640 + k * 180, y=y, scale=sc)
        y0 = H - 170                                                           # the parapet in front
        poly(cr, [(-200, y0 + 40), (W + 200, y0 + 20), (W + 200, H + 200), (-200, H + 200)])
        fill(cr, o["mud"])
        for j in range(9):
            Sandbags(length=300, rows=2, seed=j).draw(cr, t, x=-60 + j * 250, y=y0 + 40 - j * 2, scale=0.8)
        for x in range(0, W, 240):                                             # revetment posts
            line(cr, x + 40, y0 + 60, x + 34, H + 10, 14, WOOD_DK)


# ================================================================ CITY SKYLINES
def _windows(cr, x, y, w, h, r, lit, night, step=34):
    for wy in range(int(h // step) - 1):
        for wx in range(int(w // 26)):
            px, py = x + 10 + wx * 26, y + 18 + wy * step
            if r.random() < 0.6:
                on = night and r.random() < lit
                rrect(cr, px, py, 10, 14, 1)
                fill(cr, "#f2c45a" if on else "ink", 1.0 if on else 0.35)


def _rows(cr, x0, x1, ground, r, tone, lit, night, hmin=90, hmax=200, roof="flat"):
    x = x0
    while x < x1:
        w = r.uniform(70, 150)
        h = r.uniform(hmin, hmax)
        top = ground - h
        if roof == "mansard":
            poly(cr, [(x, ground), (x, top + 30), (x + 12, top), (x + w - 12, top), (x + w, top + 30), (x + w, ground)])
        elif roof == "gable":
            poly(cr, [(x, ground), (x, top + 26), (x + w / 2, top - 10), (x + w, top + 26), (x + w, ground)])
        else:
            poly(cr, [(x, ground), (x, top), (x + w, top), (x + w, ground)])
        fill(cr, tone)
        if r.random() < 0.6:                                                  # chimneys
            for c in range(r.randint(1, 3)):
                cx = x + 14 + c * 22
                rrect(cr, cx, top - 22, 12, 30, 1)
                fill(cr, tone)
        _windows(cr, x, top + 30, w, h - 30, r, lit, night)
        x += w - 1


class Skyline(Set):
    defaults = dict(city="london", ground=820, tone=None, night=False, lit=0.3, seed=11, floor=True)

    def _draw(self, cr, t, o):
        g = o["ground"]
        night = o["night"]
        tone = o["tone"] or ("#2b2a2e" if night else "#5c564b")
        back = mix(tone, "sky" if not night else "#2f3647", 0.45)
        r = random.Random(o["seed"])
        _rows(cr, -100, W + 100, g - 40, r, back, o["lit"] * 0.5, night, 120, 260)     # a hazier back row
        getattr(self, "_" + o["city"], self._generic)(cr, t, g, tone, r, o)
        if o["floor"]:
            cr.rectangle(-200, g, W + 400, H - g + 200)
            fill(cr, shade(tone, -0.25))
        line(cr, -200, g, W + 200, g, 3, "ink")

    def _generic(self, cr, t, g, tone, r, o):
        _rows(cr, -100, W + 100, g, r, tone, o["lit"], o["night"])

    def _london(self, cr, t, g, tone, r, o):
        _rows(cr, -100, W + 100, g, r, tone, o["lit"], o["night"], 80, 160, roof="gable")
        bx = W * 0.3                                                          # the clock tower
        rrect(cr, bx - 45, g - 520, 90, 520, 0)
        fill(cr, tone)
        rrect(cr, bx - 58, g - 600, 116, 90, 0)
        fill(cr, tone)
        cr.arc(bx, g - 555, 34, 0, TAU)
        fill_ink(cr, "#f2c45a" if o["night"] else "cream", 4, tone=False)
        line(cr, bx, g - 555, bx + 14, g - 570, 4)
        line(cr, bx, g - 555, bx, g - 580, 4)
        poly(cr, [(bx - 58, g - 600), (bx, g - 740), (bx + 58, g - 600)])
        fill(cr, tone)
        line(cr, bx, g - 740, bx, g - 790, 5, tone)
        poly(cr, [(bx + 45, g), (bx + 45, g - 220), (W * 0.62, g - 220), (W * 0.62, g)])   # the long gothic front
        fill(cr, tone)
        for i in range(16):
            x = bx + 60 + i * ((W * 0.62 - bx - 60) / 16)
            poly(cr, [(x - 6, g - 220), (x, g - 270), (x + 6, g - 220)])
            fill(cr, tone)
        dx = W * 0.8                                                          # the cathedral dome
        rrect(cr, dx - 120, g - 260, 240, 260, 0)
        fill(cr, tone)
        rrect(cr, dx - 90, g - 330, 180, 70, 0)
        fill(cr, tone)
        cr.arc(dx, g - 330, 90, math.pi, TAU)
        fill(cr, tone)
        rrect(cr, dx - 14, g - 470, 28, 60, 4)
        fill(cr, tone)
        line(cr, dx, g - 470, dx, g - 500, 5, tone)

    def _paris(self, cr, t, g, tone, r, o):
        _rows(cr, -100, W + 100, g, r, tone, o["lit"], o["night"], 90, 150, roof="mansard")
        ex = W * 0.42                                                          # the iron tower (lattice silhouette)
        top = g - 760
        legs = [(-150, 0), (150, 0)]
        for sx, _ in legs:
            poly(cr, [(ex + sx - 30, g), (ex + sx + 30 * (1 if sx < 0 else -1) + (10 if sx < 0 else -10), g),
                      (ex + sx * 0.25, g - 300), (ex + sx * 0.18, g - 300)])
            fill(cr, tone)
        cr.move_to(ex - 150, g)
        cr.curve_to(ex - 100, g - 120, ex + 100, g - 120, ex + 150, g)
        cr.line_to(ex + 120, g)
        cr.curve_to(ex + 80, g - 90, ex - 80, g - 90, ex - 120, g)
        cr.close_path()
        fill(cr, tone)
        rrect(cr, ex - 70, g - 310, 140, 22, 2)
        fill(cr, tone)
        poly(cr, [(ex - 48, g - 300), (ex + 48, g - 300), (ex + 14, g - 560), (ex - 14, g - 560)])
        fill(cr, tone)
        rrect(cr, ex - 34, g - 570, 68, 16, 2)
        fill(cr, tone)
        poly(cr, [(ex - 14, g - 560), (ex + 14, g - 560), (ex + 3, top), (ex - 3, top)])
        fill(cr, tone)
        for k in range(12):                                                   # lattice gaps
            y = g - 320 - k * 20
            w = lerp(40, 10, k / 12)
            line(cr, ex - w, y, ex + w, y - 18, 2, mix(tone, "sky", 0.5))
            line(cr, ex + w, y, ex - w, y - 18, 2, mix(tone, "sky", 0.5))
        ax = W * 0.78                                                          # the triumphal arch
        rrect(cr, ax - 110, g - 250, 220, 250, 0)
        fill(cr, tone)
        cr.move_to(ax - 45, g)
        cr.line_to(ax - 45, g - 120)
        cr.curve_to(ax - 45, g - 175, ax + 45, g - 175, ax + 45, g - 120)
        cr.line_to(ax + 45, g)
        cr.close_path()
        fill(cr, mix(tone, "sky", 0.55) if not o["night"] else "#2f3647")
        for sx, h in ((W * 0.12, 300), (W * 0.18, 250)):                       # hilltop basilica domes
            cr.arc(sx, g - h, 50, math.pi, TAU)
            fill(cr, tone)
            rrect(cr, sx - 50, g - h, 100, h, 0)
            fill(cr, tone)
            line(cr, sx, g - h - 50, sx, g - h - 90, 5, tone)

    def _moscow(self, cr, t, g, tone, r, o):
        _rows(cr, -100, W + 100, g, r, tone, o["lit"], o["night"], 70, 140)
        poly(cr, [(-100, g), (-100, g - 120), (W + 100, g - 120), (W + 100, g)])   # the fortress wall
        fill(cr, tone)
        for x in range(-100, W + 100, 40):
            poly(cr, [(x, g - 120), (x + 6, g - 146), (x + 20, g - 136), (x + 34, g - 146), (x + 40, g - 120)])
            fill(cr, tone)
        tx = W * 0.35                                                          # the gate tower with its red star
        rrect(cr, tx - 70, g - 420, 140, 420, 0)
        fill(cr, tone)
        rrect(cr, tx - 54, g - 520, 108, 100, 0)
        fill(cr, tone)
        cr.arc(tx, g - 470, 30, 0, TAU)
        fill_ink(cr, "cream", 4, tone=False)
        for k, (w, h) in enumerate(((46, 40), (36, 34), (26, 30))):            # stepped tiers, then the tent roof
            y = g - 520 - sum(hh for _, hh in ((46, 40), (36, 34), (26, 30))[:k])
            poly(cr, [(tx - w, y), (tx - w, y - h + 8), (tx - w + 6, y - h), (tx + w - 6, y - h), (tx + w, y - h + 8),
                      (tx + w, y)])
            fill(cr, tone)
        poly(cr, [(tx - 26, g - 624), (tx, g - 760), (tx + 26, g - 624)])
        fill(cr, tone)
        star(cr, tx, g - 784, 28, "soviet", lw=4)
        bx = W * 0.72                                                          # the cathedral's onion domes
        rrect(cr, bx - 200, g - 300, 400, 300, 0)
        fill(cr, tone)
        stripes = ("alert", "gold", "allies", "olive", "cream")
        for i, (dx, h, s) in enumerate(((-140, 360, 0.8), (-60, 420, 0.9), (0, 560, 1.15), (70, 430, 0.9),
                                        (150, 370, 0.8))):
            x = bx + dx
            rrect(cr, x - 30 * s, g - h, 60 * s, h - 280, 0)
            fill(cr, tone)
            cr.move_to(x, g - h - 120 * s)
            cr.curve_to(x + 10 * s, g - h - 70 * s, x + 62 * s, g - h - 60 * s, x + 46 * s, g - h)
            cr.line_to(x - 46 * s, g - h)
            cr.curve_to(x - 62 * s, g - h - 60 * s, x - 10 * s, g - h - 70 * s, x, g - h - 120 * s)
            cr.close_path()
            if o["night"]:
                fill(cr, tone)
            else:
                fill_ink(cr, mix(stripes[i], tone, 0.35), 3, tone=False)
            line(cr, x, g - h - 120 * s, x, g - h - 160 * s, 4, tone)

    def _berlin(self, cr, t, g, tone, r, o):
        _rows(cr, -100, W + 100, g, r, tone, o["lit"], o["night"], 110, 200)
        gx = W * 0.4                                                           # the columned city gate
        rrect(cr, gx - 260, g - 60, 520, 60, 0)
        fill(cr, tone)
        rrect(cr, gx - 280, g - 330, 560, 70, 0)
        fill(cr, tone)
        rrect(cr, gx - 120, g - 400, 240, 70, 0)
        fill(cr, tone)
        for i in range(6):
            x = gx - 240 + i * 92
            rrect(cr, x, g - 260, 32, 200, 0)
            fill(cr, tone)
        rx = W * 0.75                                                          # the parliament dome
        rrect(cr, rx - 260, g - 260, 520, 260, 0)
        fill(cr, tone)
        for sx in (-260, 200):
            rrect(cr, rx + sx, g - 320, 60, 320, 0)
            fill(cr, tone)
        cr.move_to(rx - 120, g - 260)
        cr.curve_to(rx - 120, g - 380, rx + 120, g - 380, rx + 120, g - 260)
        cr.close_path()
        fill(cr, tone)
        cx = W * 0.1                                                           # the victory column
        rrect(cr, cx - 50, g - 90, 100, 90, 0)
        fill(cr, tone)
        rrect(cr, cx - 18, g - 460, 36, 380, 0)
        fill(cr, tone)
        ellipse(cr, cx, g - 470, 16, 26)
        fill(cr, tone)

    def _pacific(self, cr, t, g, tone, r, o):
        Island(width=1300, color=tone, seed=o["seed"]).draw(cr, t, x=W * 0.55, y=g, scale=1.0)
        for i in range(9):                                                    # palms along the beach
            x = W * (0.05 + i * 0.1) + r.uniform(-20, 20)
            hgt = r.uniform(160, 260)
            sway = math.sin(t * 1.2 + i) * 6
            cr.move_to(x, g)
            cr.curve_to(x + 10, g - hgt * 0.5, x + 20 + sway, g - hgt * 0.8, x + 26 + sway, g - hgt)
            ink(cr, 10, tone)
            for a in (-2.8, -2.2, -1.5, -0.8, -0.2):
                cr.move_to(x + 26 + sway, g - hgt)
                cr.curve_to(x + 26 + sway + math.cos(a) * 40, g - hgt + math.sin(a) * 40,
                            x + 26 + sway + math.cos(a) * 80, g - hgt + math.sin(a) * 30 + 20,
                            x + 26 + sway + math.cos(a) * 100, g - hgt + 40)
                ink(cr, 9, tone)
        for i in range(3):                                                    # stilt huts
            x = W * (0.12 + i * 0.09)
            rrect(cr, x - 40, g - 90, 80, 50, 0)
            fill(cr, tone)
            poly(cr, [(x - 56, g - 90), (x, g - 140), (x + 56, g - 90)])
            fill(cr, tone)
            for sx in (-30, 30):
                line(cr, x + sx, g - 40, x + sx, g, 5, tone)


# ================================================================ INTERIORS
def _floor(cr, y0, vx, color, n=14, wood=True):
    """A floor from y0 to the bottom in one-point perspective toward vanishing x (planks or tiles)."""
    cr.rectangle(-200, y0, W + 400, H - y0 + 200)
    fill(cr, color)
    for i in range(-n, n + 1):
        line(cr, vx + i * 30, y0, vx + i * 260, H + 40, 2.5, shade(color, -0.3))
    y = y0
    k = 8.0
    while y < H + 40:
        if not wood:
            line(cr, -200, y, W + 200, y, 2.5, shade(color, -0.3))
        y += k
        k *= 1.35
    line(cr, -200, y0, W + 200, y0, 4)


class SigningRoom(Set):
    defaults = dict(kind="hall", horizon=640, table=False)

    def _draw(self, cr, t, o):
        hz = o["horizon"]
        if o["kind"] == "hall":
            cr.rectangle(-200, -200, W + 400, hz + 200)
            fill(cr, "#d8c08a")
            for i in range(-1, 9):                                             # arched mirror bays
                x = i * 240 + 40
                rrect(cr, x - 14, -100, 28, hz + 100, 0)
                fill_ink(cr, BRASS, 3)
                cr.move_to(x + 30, hz - 40)
                cr.line_to(x + 30, 220)
                cr.curve_to(x + 30, 110, x + 210, 110, x + 210, 220)
                cr.line_to(x + 210, hz - 40)
                cr.close_path()
                fill_ink(cr, "#b9c2b7", 4, tone=False)
                for j in range(1, 4):
                    line(cr, x + 30, 220 + j * 90, x + 210, 220 + j * 90, 2, "#8f9a90")
                line(cr, x + 120, 140, x + 120, hz - 40, 2, "#8f9a90")
                line(cr, x + 60, hz - 60, x + 180, 170, 3, "cream", 0.7)          # mirror glint
            cr.rectangle(-200, -200, W + 400, 90)
            fill(cr, BRASS, keep=True)
            dots(cr, shade(BRASS, -0.35), 2)
            cr.new_path()
            for cx in (W * 0.25, W * 0.5, W * 0.75):                            # chandeliers
                sw = math.sin(t * 0.8 + cx) * 0.02
                cr.save()
                cr.translate(cx, -10)
                cr.rotate(sw)
                line(cr, 0, 0, 0, 120, 3)
                ellipse(cr, 0, 150, 90, 26)
                fill_ink(cr, BRASS, 3, tone=False)
                for k in range(7):
                    x = -80 + k * 26
                    line(cr, x, 150, x, 128, 3, "cream")
                    glow(cr, x, 122, 18, "gold", 0.6)
                cr.restore()
            _floor(cr, hz, W / 2, "#9a7448")
        else:
            cr.rectangle(-200, -200, W + 400, hz + 200)
            fill(cr, "#7a5638")
            for i in range(-1, 12):
                x = i * 180
                rrect(cr, x + 20, 120, 140, hz - 180, 4)
                fill_ink(cr, shade("#7a5638", 0.12), 3)
            rrect(cr, W * 0.38, 120, W * 0.24, 300, 6)                          # window
            fill_ink(cr, "#c9c3a8", 6, tone=False)
            line(cr, W * 0.5, 120, W * 0.5, 420, 6)
            line(cr, W * 0.38, 270, W * 0.62, 270, 6)
            _floor(cr, hz, W / 2, "#6a4b31")
        if o["table"]:
            LongTable(length=1500, chairs=8).draw(cr, t, x=W / 2, y=hz + 260, scale=1.0)


class BletchleyHut(Set):
    defaults = dict(horizon=700, seed=6)

    def _draw(self, cr, t, o):
        hz = o["horizon"]
        cr.rectangle(-200, -200, W + 400, hz + 200)
        fill(cr, "#8a6a48")
        for i in range(-20, 60):                                               # horizontal plank walls
            y = i * 30
            line(cr, -200, y, W + 200, y, 2, shade("#8a6a48", -0.3))
        for x in range(0, W + 1, 320):
            rrect(cr, x - 10, -100, 20, hz + 100, 0)
            fill_ink(cr, WOOD_DK, 3, tone=False)
        rrect(cr, 180, 160, 360, 260, 4)                                       # window with blackout curtain
        fill_ink(cr, "#2b3040", 6, tone=False)
        line(cr, 360, 160, 360, 420, 6)
        line(cr, 180, 290, 540, 290, 6)
        for s in (-1, 1):
            cx = 360 + s * 150
            poly(cr, [(cx - 60, 150), (cx + 60, 150), (cx + 50 + math.sin(t + s) * 4, 430), (cx - 50, 430)])
            fill_ink(cr, "#3b3633", 4)
        rrect(cr, 1180, 140, 560, 320, 6)                                       # blackboard of letter groups
        fill_ink(cr, "#2f3a33", 8, tone=False)
        r = random.Random(o["seed"])
        for i in range(5):
            for j in range(4):
                s = "".join(chr(65 + r.randrange(26)) for _ in range(5))
                text(cr, s, 1220 + j * 130, 200 + i * 56, 34, font=STENCIL, color="cream", align="left", alpha=0.85)
        sw = math.sin(t * 1.4) * 0.06                                           # the swinging lamp
        cr.save()
        cr.translate(W * 0.5, -20)
        cr.rotate(sw)
        line(cr, 0, 0, 0, 220, 3)
        poly(cr, [(-80, 280), (-30, 220), (30, 220), (80, 280)])
        fill_ink(cr, "#3f5a46", 4, tone=False)
        glow(cr, 0, 300, 220, "gold", 0.35)
        cr.restore()
        _floor(cr, hz, W / 2, "#6b5a46", wood=True)
        rrect(cr, -50, hz + 40, W + 100, 50, 4)                                 # bench/desk edge
        fill_ink(cr, WOOD, 5)


class BunkerCorridor(Set):
    defaults = dict(close=1.0)

    def _draw(self, cr, t, o):
        vx, vy = W / 2, H * 0.48
        cr.rectangle(-200, -200, W + 400, H + 400)
        fill(cr, shade(CONCRETE, -0.25))
        fx0, fy0, fx1, fy1 = vx - 300, vy - 330, vx + 300, vy + 300            # the far wall around the door
        poly(cr, [(-200, -200), (fx0, fy0), (fx0, fy1), (-200, H + 200)])       # left wall
        fill(cr, shade(CONCRETE, -0.1), keep=True)
        dots(cr, shade(CONCRETE, -0.4), 1, 0.6)
        cr.new_path()
        poly(cr, [(W + 200, -200), (fx1, fy0), (fx1, fy1), (W + 200, H + 200)])  # right wall
        fill(cr, shade(CONCRETE, -0.18))
        poly(cr, [(-200, -200), (W + 200, -200), (fx1, fy0), (fx0, fy0)])       # ceiling
        fill(cr, shade(CONCRETE, -0.35))
        poly(cr, [(-200, H + 200), (W + 200, H + 200), (fx1, fy1), (fx0, fy1)])  # floor
        fill(cr, shade(CONCRETE, -0.3), keep=True)
        dots(cr, shade(CONCRETE, -0.55), 2, 0.8)
        cr.new_path()
        for k in range(4):                                                     # receding wall joints and lamps
            u = 1 - (k + 1) / 5
            xl = lerp(fx0, -200, u)
            xr = lerp(fx1, W + 200, u)
            yt = lerp(fy0, -200, u)
            yb = lerp(fy1, H + 200, u)
            line(cr, xl, yt, xl, yb, 3, shade(CONCRETE, -0.5))
            line(cr, xr, yt, xr, yb, 3, shade(CONCRETE, -0.5))
            lx, ly = (xl + xr) / 2, yt + 24 * (1 - u * 0.6)
            flick = 0.85 + 0.15 * math.sin(t * 13 + k * 3)
            glow(cr, lx, ly + 10, 90 * (1.4 - u), "gold", 0.45 * flick)
            ellipse(cr, lx, ly, 30 * (1.4 - u), 12 * (1.4 - u))
            fill_ink(cr, "cream", 3, tone=False)
        line(cr, -200, 140, fx0, fy0 + 60, 12, STEEL)                          # pipes
        line(cr, -200, 190, fx0, fy0 + 80, 8, shade(STEEL, -0.2))
        poly(cr, [(fx0, fy0), (fx1, fy0), (fx1, fy1), (fx0, fy1)])
        fill_ink(cr, CONCRETE, 4)
        BunkerDoor(frame=CONCRETE).draw(cr, t, x=vx, y=fy1, scale=0.95, close=o["close"])


class Courtroom(Set):
    defaults = dict(horizon=600)

    def _draw(self, cr, t, o):
        hz = o["horizon"]
        cr.rectangle(-200, -200, W + 400, hz + 200)
        fill(cr, "#6e4f33")
        for i in range(-1, 12):
            x = i * 180
            rrect(cr, x + 16, 80, 148, hz - 120, 4)
            fill_ink(cr, shade("#6e4f33", 0.12), 3)
        rrect(cr, W * 0.2, 260, W * 0.6, 240, 6)                                 # the judges' bench
        fill_ink(cr, WOOD_DK, 6)
        rrect(cr, W * 0.18, 240, W * 0.64, 32, 6)
        fill_ink(cr, WOOD, 5)
        for i in range(4):                                                     # high-backed chairs
            x = W * (0.3 + i * 0.13)
            rrect(cr, x - 50, 120, 100, 140, 16)
            fill_ink(cr, "#5a2a22", 4)
        _floor(cr, hz, W / 2, "#7a6a50")
        rrect(cr, -100, H - 300, W * 0.62, 30, 6)                               # the dock rail (front left)
        fill_ink(cr, WOOD, 5)
        for x in range(-60, int(W * 0.6), 60):
            line(cr, x, H - 270, x, H + 20, 10, WOOD_DK)
        rrect(cr, -100, H - 160, W * 0.62, 200, 0)
        fill_ink(cr, WOOD_DK, 5)


class ShipDeck(Set):
    defaults = dict(horizon=560, mode="day")

    def _draw(self, cr, t, o):
        hz = o["horizon"]
        Sky(mode=o["mode"], horizon=hz, clouds=4).draw(cr, t)
        Ocean(horizon=hz, mode="night" if o["mode"] == "night" else "day").draw(cr, t)
        TurretCloseup(side="usa", silhouette=None).draw(cr, t, x=W * 0.2, y=hz + 160, scale=0.6, turret=150, elev=6)
        _floor(cr, hz + 160, W * 0.55, "#b58e5c")
        for x in range(-100, W + 100, 70):                                     # rail stanchions at the deck edge
            line(cr, x, hz + 160, x, hz + 60, 4)
        line(cr, -100, hz + 70, W + 100, hz + 70, 4)
        line(cr, -100, hz + 110, W + 100, hz + 110, 3)
        Destroyer(silhouette="#5c5f5c", side="usa", water=None).draw(cr, t, x=W * 0.82, y=hz + 6, scale=0.32,
                                                                       facing=-1, speed=20)


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("math", "random")]


def _sheet(t=1.3, out=None):
    """Every set as a 4x4 grid of thumbnails: out/ww2/style/props_sheet_4_sets.png."""
    import os
    from channels.ww2.kit.core import ROOT, print_finish, render_clip
    cells = [
        ("SKY day", Sky(mode="day", rays=True)), ("SKY dusk", Sky(mode="dusk")), ("SKY night", Sky(mode="night")),
        ("SKY sunset", Sky(mode="sunset")), ("OCEAN", None), ("TRENCH LINE", TrenchLine()),
        ("LONDON", Skyline(city="london")), ("PARIS", Skyline(city="paris")), ("MOSCOW", Skyline(city="moscow")),
        ("BERLIN", Skyline(city="berlin", night=True)), ("PACIFIC", Skyline(city="pacific")),
        ("SIGNING HALL", SigningRoom(kind="hall", table=True)), ("OFFICE", SigningRoom(kind="office", table=True)),
        ("BLETCHLEY HUT", BletchleyHut()), ("BUNKER", BunkerCorridor(close=0.7)), ("COURTROOM", Courtroom()),
    ]

    def draw(cr, tt):
        paper(cr)
        for i, (name, s) in enumerate(cells):
            cx, cy = (i % 4) * W / 4, (i // 4) * H / 4
            cr.save()
            cr.rectangle(cx + 4, cy + 4, W / 4 - 8, H / 4 - 8)
            cr.clip()
            cr.translate(cx + 4, cy + 4)
            cr.scale((W / 4 - 8) / W, (H / 4 - 8) / H)
            if s is None:
                Sky(mode="day").draw(cr, tt, horizon=500)
                Ocean(horizon=500).draw(cr, tt)
            else:
                if name.startswith(("LONDON", "PARIS", "MOSCOW", "BERLIN", "PACIFIC")):
                    Sky(mode="night" if name == "BERLIN" else "day").draw(cr, tt)
                s.draw(cr, tt)
            cr.restore()
            text(cr, name, cx + 14, cy + 34, 26, font=STENCIL, color="cream", align="left", outline="ink",
                 outline_w=5)
        print_finish(cr, tt)

    out = out or os.path.join(ROOT, "out", "ww2", "style", "props_sheet_4_sets.png")
    return render_clip(draw, 1, out, still=t)


def _sheet_deck(t=1.3, out=None):
    import os
    from channels.ww2.kit.core import ROOT, print_finish, render_clip

    def draw(cr, tt):
        ShipDeck().draw(cr, tt)
        print_finish(cr, tt)
    return render_clip(draw, 1, out or os.path.join(ROOT, "out", "ww2", "style", "set_shipdeck.png"), still=t)


if __name__ == "__main__":
    print(_sheet())
    print(_sheet_deck())
