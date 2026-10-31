"""WW2 kit: structures, scenery and small props from SHOTLIST.md (poster look, same API as props.py).

    from channels.ww2.kit.props import *       # props.py re-exports everything here too
    Clock(x=960, y=500, scale=1.2).draw(cr, t, hours=4 + 45 / 60)

Every class is a props.Prop: Thing(x, y, scale, facing, side, alpha, seed, silhouette=None, **options).draw(cr, t, ...)
(x, y) is the ground point under the thing unless the docstring says "centre". silhouette="ink" (any colour) draws it
as one flat poster silhouette. Sizes are at scale 1.

Vehicles+:   Airliner (door 0..1 opens, door_xy()), TurretCloseup (turret, elev, fire), Hedgehog (beach obstacle)
Structures:  FortWall(length), FortIcon (centre; glow 0..1), Podium (top_y), Parliament, Padlock (centre; snap_at),
             RuinedSkyline(width), BuildingSection (floors list), BunkerDoor (close 0..1), LongTable(length, chairs),
             Tree(kind="pine"|"oak"|"birch"), forest(), Island(width, bursts), Flag(color, stripe), Pedestal
Small:       Clock (centre; hours or spin), Newspaper (centre; masthead, headline, spin 0..1), Bombe (drums turn),
             Microphone, WhiteFlag, ParachuteIcon (centre), Chart (centre; progress 0..1, crash), Coin (centre),
             coin_stream(), Die (centre; roll 0..1, value), Thermometer (bulb centre; temp C), Headphones (centre),
             Papers (centre; circle 0..1), Pact (centre; tear 0..1), Paper (centre; crumple 0..1, lines)
"""
import math
import random

from channels.ww2.kit.core import LABEL, SLAB, STENCIL, TITLE, back_out, clamp01, ease_in, ease_out, lerp, seg, \
    smooth, text
from channels.ww2.kit.props import (TAU, BarbedWire, Prop, barrels, dots, ellipse, explosion, fill, fill_ink, glow,  # noqa: F401
                                    ink, line, mix, muzzle_flash, noise, poly, propeller, recoil, rng, rrect, shade,
                                    since, smoke, wheel)

STONE = "#b9ae92"
STONE_DK = "#8f846b"
CONCRETE = "#a7a08d"
WOOD = "#7a5638"
WOOD_DK = "#5a3e28"
BRASS = "#c39a3e"
STEEL = "#6d6a66"
GLASS = "#cfd3c4"


# ================================================================ vehicles and big gun
class Airliner(Prop):
    """A 1938 twin-engine airliner parked on the ground, ~640 long, facing right; door 0..1 opens the rear door and
    lowers the steps. door_xy() gives the doorway sill (local, at scale 1) for standing a figure in it."""
    defaults = dict(door=1.0, rpm=0.0, color="#c4bfae", stripe="allies")

    @staticmethod
    def door_xy():
        return (-150, -150)

    def _draw(self, cr, t, o):
        lw = self.lw
        c = o["color"]
        line(cr, 140, -40, 150, 0, lw * 1.2)                                    # main gear
        wheel(cr, 150, -26, 26, 0, lw * 0.7)
        line(cr, -270, -96, -276, -14, lw)
        wheel(cr, -276, -10, 10, 0, lw * 0.5)
        poly(cr, [(-300, -150), (-330, -270), (-280, -268), (-230, -150)])     # fin
        fill_ink(cr, c, lw)
        cr.move_to(320, -150)                                                   # fuselage
        cr.curve_to(318, -200, 270, -214, 200, -214)
        cr.line_to(-220, -190)
        cr.curve_to(-280, -186, -320, -170, -340, -152)
        cr.line_to(-340, -136)
        cr.curve_to(-300, -112, -240, -104, -180, -100)
        cr.line_to(220, -98)
        cr.curve_to(280, -98, 318, -116, 320, -150)
        cr.close_path()
        fill_ink(cr, c, lw)
        line(cr, 310, -150, -330, -146, lw * 1.6, o["stripe"])                   # cheat line
        cr.move_to(316, -170)                                                   # cockpit glazing
        cr.curve_to(300, -200, 270, -206, 250, -204)
        cr.line_to(252, -172)
        cr.close_path()
        fill_ink(cr, GLASS, lw * 0.6, tone=False)
        for i in range(8):
            rrect(cr, 180 - i * 42, -184, 22, 22, 6)
            fill_ink(cr, GLASS, lw * 0.4, tone=False)
        poly(cr, [(-330, -150), (-260, -150), (-250, -140), (-330, -138)])
        fill_ink(cr, c, lw * 0.8)
        rrect(cr, -60, -112, 260, 18, 9)                                        # wing (edge on)
        fill_ink(cr, c, lw * 0.8)
        rrect(cr, 60, -140, 120, 40, 18)                                        # engine nacelle
        fill_ink(cr, shade(c, -0.15), lw * 0.8)
        propeller(cr, 186, -120, 64, t * o["rpm"] * TAU, lw)
        dx, dy = self.door_xy()
        u = smooth(clamp01(o["door"]))
        rrect(cr, dx - 30, dy - 70, 60, 78, 6)                                  # doorway
        fill_ink(cr, "ink" if u > 0.05 else c, lw * 0.7, tone=False)
        if u > 0.05:
            cr.save()                                                           # door panel swings out toward us
            cr.translate(dx + 30, dy - 70)
            cr.scale(1 - 0.75 * u, 1)
            rrect(cr, -60, 0, 60, 78, 6)
            fill_ink(cr, shade(c, 0.1), lw * 0.7, tone=False)
            cr.restore()
            for k in range(5):                                                  # steps unfold to the ground
                f = clamp01(u * 5 - k)
                if f <= 0:
                    break
                sx = dx - 10 - k * 26
                sy = dy + 8 + k * 28
                rrect(cr, sx - 34, sy, 60 * f, 10, 3)
                fill_ink(cr, STEEL, lw * 0.5, tone=False)
            line(cr, dx - 36, dy + 6, dx - 10 - 4 * 26 - 30, dy + 8 + 5 * 28, lw * 0.6)


class TurretCloseup(Prop):
    """A battleship's main turret seen big from a low heroic angle (~900 wide); origin = deck point under its centre.
    draw(t, turret=0 deg (0 = barrels toward the right of frame, 90 = at the camera), elev=12, fire=[t...])."""
    defaults = dict(turret=0.0, elev=12.0, fire=(), side="germany")

    def _draw(self, cr, t, o):
        lw, body = self.lw * 1.2, o["body"]
        poly(cr, [(-700, 0), (700, 0), (760, 60), (-760, 60)])                 # deck edge
        fill_ink(cr, shade(body, -0.25), lw)
        for i in range(-6, 7):
            line(cr, i * 110, 4, i * 124, 56, lw * 0.4, shade(body, -0.45))
        rrect(cr, -330, -60, 660, 66, 20)                                       # barbette ring
        fill_ink(cr, shade(body, -0.1), lw)
        age = since(t, o["fire"])
        kick = recoil(age)
        a = math.radians(o["turret"])
        ca, sa = math.cos(a), math.sin(a)
        tw = 300 * abs(ca) + 240 * abs(sa)
        behind = sa < -0.05
        piv = (tw * 0.45 * ca, -150)

        def guns():
            return barrels(cr, piv[0], piv[1], o["turret"], o["elev"], 720, 52, 2, kick, body, lw, spacing=110)
        res = guns() if behind else None
        fx = 1 if ca >= 0 else -1
        pts = [(-tw, -50), (-tw + 30, -250), (tw - 90, -262), (tw + 20, -150), (tw, -50)]
        if fx < 0:
            pts = [(-x, y) for x, y in pts]
        poly(cr, pts)
        fill_ink(cr, body, lw)
        poly(cr, [(-tw * 0.7, -262), (tw * 0.5, -270), (tw * 0.5, -300), (-tw * 0.6, -292)])   # rangefinder hood
        fill_ink(cr, shade(body, 0.12), lw * 0.8)
        for k in range(-3, 4):                                                  # rivet rows
            cr.arc(k * tw * 0.25, -80, 6, 0, TAU)
            fill(cr, shade(body, -0.4))
        if not behind:
            res = guns()
        tips, vec = res
        if age is not None and age < 1.4:
            ang = math.atan2(vec[1], vec[0]) if abs(vec[0]) > 0.15 else -math.pi / 2
            for x, y in tips:
                muzzle_flash(cr, x, y, age, 320, ang, seed=o["seed"])


class Hedgehog(Prop):
    """A steel beach obstacle (three crossed girders), ~150 tall."""
    defaults = dict(color=STEEL)

    def _draw(self, cr, t, o):
        lw = self.lw
        for a0, a1 in ((-0.9, 0.0), (0.9, 0.0), (0.0, 1.0)):
            cr.save()
            cr.translate(0, -70)
            cr.rotate(a0)
            cr.scale(1, 1 if a1 == 0 else 0.45)
            rrect(cr, -12, -95, 24, 190, 3)
            fill_ink(cr, o["color"] if a1 == 0 else shade(o["color"], -0.2), lw * 0.8)
            cr.restore()


# ================================================================ structures
class FortWall(Prop):
    """A low concrete garrison wall with a guardhouse (Westerplatte), `length` long, ~170 tall at the house."""
    defaults = dict(length=900.0, lit=True, color=CONCRETE)

    def _draw(self, cr, t, o):
        lw, L, c = self.lw, o["length"], o["color"]
        rrect(cr, -L / 2, -90, L, 90, 4)
        fill_ink(cr, c, lw)
        for i in range(int(L // 60)):
            x = -L / 2 + 30 + i * 60
            line(cr, x, -86, x, -4, lw * 0.3, shade(c, -0.3))
        rrect(cr, -L / 2 - 8, -102, L + 16, 16, 3)
        fill_ink(cr, shade(c, 0.12), lw * 0.8)
        hx = L * 0.18
        rrect(cr, hx - 110, -230, 220, 140, 4)                                  # guardhouse
        fill_ink(cr, shade(c, 0.05), lw)
        poly(cr, [(hx - 130, -230), (hx, -300), (hx + 130, -230)])
        fill_ink(cr, "#7d5a3f", lw)
        rrect(cr, hx - 30, -196, 60, 46, 3)
        fill_ink(cr, "#f2c45a" if o["lit"] else GLASS, lw * 0.6, tone=False)
        if o["lit"]:
            glow(cr, hx, -173, 70, "#f2c45a", 0.5)
        for gx in (-L * 0.32, L * 0.38):                                        # firing slits
            rrect(cr, gx - 30, -60, 60, 12, 3)
            fill(cr, "ink")


class FortIcon(Prop):
    """A map icon of a concrete casemate (~70 wide, centre); glow 0..1 lights it gold (Maginot line chain)."""
    defaults = dict(glow=0.0, color=CONCRETE)

    def _draw(self, cr, t, o):
        lw = self.lw * 0.7
        g = clamp01(o["glow"])
        if g > 0:
            glow(cr, 0, 0, 80 * g, "gold", 0.8 * g)
        cr.move_to(-36, 18)
        cr.line_to(-36, -6)
        cr.curve_to(-36, -30, 36, -30, 36, -6)
        cr.line_to(36, 18)
        cr.close_path()
        fill_ink(cr, mix(o["color"], "gold", g * 0.6), lw, tone=False)
        rrect(cr, -18, -8, 36, 8, 2)
        fill(cr, "ink")


class Podium(Prop):
    """A rally rostrum (~340 wide, ~300 tall) with plain dark drapes (no symbols), microphones on top and steps.
    A speaker stands at y = top_y (local)."""
    defaults = dict(drape="axis", color=STONE)
    top_y = -300

    def _draw(self, cr, t, o):
        lw = self.lw
        poly(cr, [(-220, 0), (220, 0), (200, -40), (-200, -40)])
        fill_ink(cr, shade(o["color"], -0.1), lw)
        rrect(cr, -170, -300, 340, 262, 6)
        fill_ink(cr, o["color"], lw)
        sway = math.sin(t * 1.3 + o["seed"]) * 4
        for s in (-1, 1):                                                       # two hanging drapes
            x0 = s * 110
            cr.move_to(x0 - 50, -296)
            cr.line_to(x0 + 50, -296)
            cr.line_to(x0 + 46 + sway, -70)
            cr.line_to(x0, -48 + sway * 0.5)
            cr.line_to(x0 - 46 + sway, -70)
            cr.close_path()
            fill_ink(cr, o["drape"], lw * 0.8)
        rrect(cr, -190, -320, 380, 24, 6)
        fill_ink(cr, shade(o["color"], 0.12), lw)
        for mx in (-40, 40):                                                    # microphones
            line(cr, mx, -320, mx * 0.6, -380, lw * 0.6)
            rrect(cr, mx * 0.6 - 9, -404, 18, 28, 8)
            fill_ink(cr, STEEL, lw * 0.5, tone=False)


class Parliament(Prop):
    """A grand parliament building in silhouette-ready poster shapes (~1100 wide, ~560 to the dome top): four corner
    towers, a columned portico and a glass dome. No flags or emblems."""
    defaults = dict(color=STONE, dome=GLASS, lit=False)

    def _draw(self, cr, t, o):
        lw, c = self.lw, o["color"]
        rrect(cr, -500, -300, 1000, 300, 0)
        fill_ink(cr, c, lw)
        for tx in (-520, 420):                                                  # corner towers
            rrect(cr, tx, -380, 100, 380, 0)
            fill_ink(cr, shade(c, 0.06), lw)
            rrect(cr, tx - 8, -396, 116, 20, 2)
            fill_ink(cr, shade(c, -0.1), lw * 0.7)
        for i in range(14):                                                     # windows
            x = -470 + i * 70
            if -170 < x < 150:
                continue
            rrect(cr, x, -250, 30, 60, 3)
            fill_ink(cr, "#f2c45a" if o["lit"] else shade(c, -0.45), lw * 0.4, tone=False)
            rrect(cr, x, -140, 30, 60, 3)
            fill_ink(cr, "#f2c45a" if o["lit"] else shade(c, -0.45), lw * 0.4, tone=False)
        poly(cr, [(-200, -330), (200, -330), (0, -420)])                         # pediment
        fill_ink(cr, shade(c, 0.1), lw)
        rrect(cr, -200, -340, 400, 18, 0)
        fill_ink(cr, shade(c, -0.05), lw * 0.7)
        for i in range(6):                                                      # portico columns
            x = -170 + i * 68
            rrect(cr, x, -322, 22, 322, 4)
            fill_ink(cr, shade(c, 0.15), lw * 0.6)
        rrect(cr, -240, -460, 480, 40, 0)                                       # dome drum
        fill_ink(cr, shade(c, -0.05), lw)
        cr.move_to(-210, -460)
        cr.curve_to(-210, -560, 210, -560, 210, -460)
        cr.close_path()
        fill_ink(cr, o["dome"], lw)
        for i in range(1, 6):
            x = -210 + i * 70
            cr.move_to(x, -460)
            cr.curve_to(x * 0.9, -520, x * 0.4, -545, 0, -545)
            ink(cr, lw * 0.4, shade(o["dome"], -0.4))
        rrect(cr, -16, -580, 32, 26, 4)
        fill_ink(cr, shade(c, -0.1), lw * 0.6)


class Padlock(Prop):
    """A giant padlock (centre of the body, ~260 wide). snap_at = when the shackle slams down (closed before that if
    None); drop 0..1 is how far it has fallen into frame (call with y yourself for a drop)."""
    defaults = dict(snap_at=None, color=BRASS)

    def _draw(self, cr, t, o):
        lw = self.lw * 1.3
        if o["snap_at"] is None:
            u = 1.0
        else:
            u = back_out(seg(t, o["snap_at"], o["snap_at"] + 0.12), 3.0)
        lift = (1 - u) * 90
        cr.save()
        cr.translate(0, -lift)
        cr.move_to(-80, -60)                                                    # shackle
        cr.line_to(-80, -150)
        cr.curve_to(-80, -270, 80, -270, 80, -150)
        cr.line_to(80, -60 + lift)
        ink(cr, 54 + lw * 2)
        cr.move_to(-80, -60)
        cr.line_to(-80, -150)
        cr.curve_to(-80, -270, 80, -270, 80, -150)
        cr.line_to(80, -60 + lift)
        ink(cr, 54, STEEL)
        cr.restore()
        rrect(cr, -130, -80, 260, 210, 26)
        fill_ink(cr, o["color"], lw)
        cr.arc(0, 10, 20, 0, TAU)
        fill(cr, "ink")
        poly(cr, [(-9, 20), (9, 20), (14, 70), (-14, 70)])
        fill(cr, "ink")


class RuinedSkyline(Prop):
    """A ruined city skyline (`width` wide, up to ~420 tall): broken walls, empty windows, a leaning chimney and
    smoke. Static except the smoke (smoke=False to skip)."""
    defaults = dict(width=1900.0, color="#5c564b", smoke=True)

    def _draw(self, cr, t, o):
        lw, Wd, c = self.lw, o["width"], o["color"]
        r = random.Random(o["seed"] + 77)
        x = -Wd / 2
        k = 0
        while x < Wd / 2:
            w = r.uniform(90, 200)
            h = r.uniform(140, 420)
            pts = [(x, 0), (x, -h * r.uniform(0.6, 1.0))]
            n = r.randint(3, 6)
            for i in range(1, n):                                               # broken jagged top
                pts.append((x + w * i / n, -h * r.uniform(0.35, 1.0)))
            pts += [(x + w, -h * r.uniform(0.3, 0.9)), (x + w, 0)]
            poly(cr, pts)
            fill_ink(cr, shade(c, r.uniform(-0.1, 0.1)), lw)
            for wy in range(1, int(h // 70)):                                   # empty window holes
                for wx in range(int(w // 50)):
                    px, py = x + 18 + wx * 50, -wy * 70
                    if r.random() < 0.55 and py > -h * 0.55:
                        rrect(cr, px, py - 30, 20, 30, 2)
                        fill(cr, "#e9c66a" if r.random() < 0.12 else "ink")
            if o["smoke"] and k % 3 == 1:
                smoke(cr, x + w / 2, -h * 0.6, t, height=380, width=40, dark=True, wind=0.5, rate=4, life=4.0,
                      seed=o["seed"] + k)
            x += w - 6
            k += 1
        poly(cr, [(-Wd / 2, 0), (Wd / 2, 0), (Wd / 2, 30), (-Wd / 2, 30)])
        fill(cr, shade(c, -0.2))


class BuildingSection(Prop):
    """A bombed apartment block in cross-section (~720 wide, 4 floors of 150): slabs, broken walls, rubble.
    .floors gives each floor's standing y (local) for placing figures."""
    defaults = dict(color=STONE, inside="#e4d6b4", nfloors=4)
    FLOOR = 150

    @property
    def floors(self):
        return [-i * self.FLOOR - 24 for i in range(self.o["nfloors"])]

    def _draw(self, cr, t, o):
        lw, c, n = self.lw, o["color"], o["nfloors"]
        H_ = n * self.FLOOR
        r = random.Random(o["seed"] + 5)
        rrect(cr, -340, -H_, 680, H_, 0)                                         # room interiors
        fill(cr, o["inside"])
        for i in range(n):                                                      # wallpaper halftone per floor
            rrect(cr, -340, -(i + 1) * self.FLOOR, 680, self.FLOOR, 0)
            dots(cr, shade(o["inside"], -0.18), 1, 1.0)
            cr.new_path()
        for i in range(n + 1):                                                  # floor slabs (broken at the end)
            y = -i * self.FLOOR
            end = 360 if i < n - 1 else r.uniform(80, 240)
            poly(cr, [(-360, y - 24), (end, y - 24 + r.uniform(-6, 10)), (end - 20, y), (-360, y)])
            fill_ink(cr, shade(c, -0.1), lw)
        pts = [(-360, 0), (-360, -H_ - 30), (-300, -H_ - 30), (-280, -H_ + 40), (-320, -H_ + 160), (-320, 0)]
        poly(cr, pts)                                                           # left outer wall (standing)
        fill_ink(cr, c, lw)
        pts = [(360, 0), (360, -H_ * 0.45), (330, -H_ * 0.5), (320, -H_ * 0.3), (330, 0)]
        poly(cr, pts)                                                           # right wall (shattered)
        fill_ink(cr, c, lw)
        for i in range(18):                                                     # rubble at the foot
            x = r.uniform(-380, 420)
            s = r.uniform(14, 40)
            poly(cr, [(x - s, 0), (x - s * 0.4, -s * r.uniform(0.6, 1.2)), (x + s * 0.6, -s * 0.8), (x + s, 0)])
            fill_ink(cr, shade(c, r.uniform(-0.3, 0.1)), lw * 0.5, tone=False)
        for i in range(n):                                                      # hanging wires/lamps
            y = -(i + 1) * self.FLOOR + 24
            line(cr, 60, y, 60 + 6 * math.sin(t * 1.5 + i), y + 34, lw * 0.4)


class BunkerDoor(Prop):
    """A heavy steel blast door in a concrete frame (~380 x 540); close 0..1 swings it shut (call with a shake
    on the slam). Origin = floor centre."""
    defaults = dict(close=1.0, color=STEEL, frame=CONCRETE)

    def _draw(self, cr, t, o):
        lw = self.lw
        rrect(cr, -260, -620, 520, 620, 6)
        fill_ink(cr, o["frame"], lw)
        rrect(cr, -190, -540, 380, 540, 4)
        fill_ink(cr, "ink", lw, tone=False)
        u = smooth(clamp01(o["close"]))
        cr.save()
        cr.translate(-190, 0)
        k = lerp(0.12, 1.0, u)
        cr.scale(k, 1)
        rrect(cr, 0, -540, 380, 540, 4)
        fill_ink(cr, o["color"], lw / max(k, 0.3))
        for yy in (-500, -270, -40):
            rrect(cr, 20, yy, 340, 20, 3)
            fill_ink(cr, shade(o["color"], -0.15), lw * 0.5 / max(k, 0.3), tone=False)
        for i in range(8):
            for yy in (-520, -20):
                cr.arc(30 + i * 45, yy, 6, 0, TAU)
                fill(cr, shade(o["color"], -0.4))
        cr.arc(280, -280, 50, 0, TAU)                                          # wheel handle
        ink(cr, 12, shade(o["color"], 0.25))
        for a in range(4):
            aa = a * math.pi / 2 + u * 1.2
            line(cr, 280, -280, 280 + math.cos(aa) * 50, -280 + math.sin(aa) * 50, 8, shade(o["color"], 0.25))
        cr.restore()


class LongTable(Prop):
    """A long signing table with a cloth, papers, inkwells and chairs behind, `length` long (Versailles, Reims,
    the UN, the Missouri). (x, y) = floor under its centre; the table top is at y-150."""
    defaults = dict(length=1400.0, chairs=8, cloth="#5f6a4a", papers=True)

    def _draw(self, cr, t, o):
        lw, L = self.lw, o["length"]
        n = int(o["chairs"])
        for i in range(n):                                                      # chair backs behind the table
            x = -L / 2 + (i + 0.5) * L / n
            rrect(cr, x - 40, -290, 80, 150, 14)
            fill_ink(cr, WOOD_DK, lw * 0.8)
            rrect(cr, x - 28, -276, 56, 90, 10)
            fill(cr, "#7a2f25")
        poly(cr, [(-L / 2 - 30, -150), (L / 2 + 30, -150), (L / 2 + 50, -40), (-L / 2 - 50, -40)])
        fill_ink(cr, o["cloth"], lw)
        poly(cr, [(-L / 2 - 30, -150), (L / 2 + 30, -150), (L / 2 + 10, -170), (-L / 2 - 10, -170)])
        fill_ink(cr, shade(o["cloth"], 0.15), lw)
        for lx in (-L / 2, L / 2):
            line(cr, lx, -40, lx, 0, lw * 1.4, WOOD_DK)
        if o["papers"]:
            for i in range(n):
                x = -L / 2 + (i + 0.5) * L / n
                poly(cr, [(x - 40, -153), (x + 40, -153), (x + 32, -165), (x - 34, -165)])
                fill_ink(cr, "cream", lw * 0.4, tone=False)
                if i % 2 == 0:
                    rrect(cr, x + 46, -184, 18, 16, 4)
                    fill_ink(cr, "ink", lw * 0.3, tone=False)


class Tree(Prop):
    """A poster tree (~360 tall): kind "pine" (stacked flat tiers), "oak" (lumpy crown) or "birch"; sways gently."""
    defaults = dict(kind="pine", color="#4f5a34", trunk=WOOD_DK, height=360.0)

    def _draw(self, cr, t, o):
        lw, hgt = self.lw, o["height"]
        sway = math.sin(t * 0.9 + o["seed"]) * 0.015
        line(cr, 0, 0, 0, -hgt * 0.35, lw * 3 if o["kind"] != "birch" else lw * 2, o["trunk"]
             if o["kind"] != "birch" else "cream")
        cr.rotate(sway)
        r = random.Random(o["seed"])
        if o["kind"] == "pine":
            for i in range(4):
                y0 = -hgt * (0.22 + i * 0.19)
                w = hgt * (0.36 - i * 0.07)
                poly(cr, [(-w, y0), (0, y0 - hgt * 0.32), (w, y0)])
                fill_ink(cr, shade(o["color"], 0.05 * i), lw)
        else:
            puffs = [(r.uniform(-0.25, 0.25) * hgt, -hgt * r.uniform(0.5, 0.85), hgt * r.uniform(0.16, 0.24))
                     for _ in range(6)]
            for x, y, rad in puffs:
                cr.new_sub_path()
                cr.arc(x, y, rad, 0, TAU)
            ink(cr, lw * 2)
            for x, y, rad in puffs:
                cr.new_sub_path()
                cr.arc(x, y, rad, 0, TAU)
            col_ = o["color"] if o["kind"] == "oak" else "#7c8a45"
            fill(cr, shade(col_, -0.2), keep=True)
            dots(cr, shade(col_, -0.45), 2)
            cr.new_path()
            for x, y, rad in puffs:
                cr.new_sub_path()
                cr.arc(x - rad * 0.12, y - rad * 0.15, rad * 0.86, 0, TAU)
            fill(cr, col_)
            if o["kind"] == "birch":
                for i in range(4):
                    line(cr, -4, -hgt * (0.08 + i * 0.07), 4, -hgt * (0.08 + i * 0.07), lw * 0.6)


def forest(cr, t, x0, x1, y, n=12, scale=0.8, seed=1, kind="pine", tone=None, rows=3):
    """Rows of poster trees between x0 and x1 standing on y; back rows smaller and paler (tone = silhouette base)."""
    r = random.Random(seed)
    for row in range(rows - 1, -1, -1):
        k = 1 - row * 0.22
        for i in range(n):
            x = lerp(x0, x1, (i + r.random() * 0.8) / n)
            c = mix(tone or "#4f5a34", "sky", row * 0.28)
            Tree(kind=kind if r.random() < 0.8 else "oak", color=c, seed=seed * 100 + row * 31 + i).draw(
                cr, t, x=x, y=y - row * 40 * scale, scale=scale * k * r.uniform(0.85, 1.15))


class Island(Prop):
    """A volcanic island silhouette on the waterline (`width` wide, ~380 tall): a cone, ridges and palms.
    bursts=[t...] puts flat star bursts on it."""
    defaults = dict(width=1000.0, color="#4b4a3c", bursts=())

    def _draw(self, cr, t, o):
        lw, Wd, c = self.lw, o["width"], o["color"]
        cr.move_to(-Wd / 2, 0)
        cr.curve_to(-Wd * 0.35, -60, -Wd * 0.3, -90, -Wd * 0.2, -120)
        cr.line_to(-Wd * 0.08, -380)
        cr.line_to(Wd * 0.02, -372)
        cr.curve_to(Wd * 0.12, -200, Wd * 0.3, -90, Wd / 2, 0)
        cr.close_path()
        fill_ink(cr, c, lw)
        for i in range(6):                                                      # palms on the shoulder
            x = Wd * (0.18 + i * 0.05)
            y = -90 + i * 12
            line(cr, x, y, x + 8, y - 70, lw * 0.8, shade(c, -0.2))
            for a in (-2.6, -2.0, -1.2, -0.5):
                line(cr, x + 8, y - 70, x + 8 + math.cos(a) * 36, y - 70 + math.sin(a) * 22 + 10, lw * 0.9,
                     shade(c, -0.2))
        for k, s in enumerate(o["bursts"] or ()):
            r = rng(o["seed"], "b", k)
            explosion(cr, r.uniform(-0.3, 0.3) * Wd, -r.uniform(40, 240), t - s, 0.7, seed=k)


class Flag(Prop):
    """A plain waving pennant on a pole (~260 tall): color, optional stripe colour. No emblems."""
    defaults = dict(color="allies", stripe=None, height=260.0)

    def _draw(self, cr, t, o):
        lw, h = self.lw, o["height"]
        line(cr, 0, 0, 0, -h, lw)
        pts_top, pts_bot = [], []
        for i in range(11):
            u = i / 10
            wv = math.sin(t * 5 - u * 4 + o["seed"]) * 10 * u
            pts_top.append((u * 150, -h + 4 + wv))
            pts_bot.append((u * 150, -h + 84 - u * 10 + wv))
        poly(cr, pts_top + pts_bot[::-1])
        fill_ink(cr, o["color"], lw * 0.7, tone=False)
        if o["stripe"]:
            mid = [(x, (y1 + y2) / 2) for (x, y1), (_, y2) in zip(pts_top, pts_bot)]
            poly(cr, mid, close=False)
            ink(cr, 18, o["stripe"])


class Pedestal(Prop):
    """A classical stone plinth (~260 wide, ~300 tall) for a statue/figure; crack 0..1 splits it."""
    defaults = dict(color=STONE, crack=0.0)

    def _draw(self, cr, t, o):
        lw, c = self.lw, o["color"]
        rrect(cr, -150, -40, 300, 40, 2)
        fill_ink(cr, shade(c, -0.1), lw)
        rrect(cr, -110, -270, 220, 230, 2)
        fill_ink(cr, c, lw)
        rrect(cr, -140, -300, 280, 34, 2)
        fill_ink(cr, shade(c, 0.1), lw)
        if o["crack"] > 0:
            u = clamp01(o["crack"])
            pts = [(10, -270), (-12, -220), (14, -170), (-8, -110), (12, -40)]
            n = max(2, int(1 + u * 4))
            poly(cr, pts[:n], close=False)
            ink(cr, lw * 0.8)


# ================================================================ small props
class Clock(Prop):
    """A station/dock clock face (centre, radius 150). hours = 4.75 shows 4:45; spin = hours per second (spinning
    months/years) added on top."""
    defaults = dict(hours=4.75, spin=0.0, color="cream", rim=BRASS, tick=True)

    def _draw(self, cr, t, o):
        lw = self.lw
        cr.arc(0, 0, 160, 0, TAU)
        fill_ink(cr, o["rim"], lw)
        cr.arc(0, 0, 136, 0, TAU)
        fill_ink(cr, o["color"], lw * 0.8, tone=False)
        for i in range(60):
            a = i * TAU / 60
            r0 = 112 if i % 5 == 0 else 122
            line(cr, math.sin(a) * r0, -math.cos(a) * r0, math.sin(a) * 128, -math.cos(a) * 128,
                 lw * (0.8 if i % 5 == 0 else 0.3))
        for i in (12, 3, 6, 9):
            a = i * TAU / 12
            text(cr, str(i), math.sin(a) * 92, -math.cos(a) * 92 + 13, 36, font=TITLE, color="ink", bold=False)
        hrs = o["hours"] + o["spin"] * t
        if o["tick"] and not o["spin"]:
            hrs += math.floor(t) / 3600.0
        ha = (hrs % 12) / 12 * TAU
        ma = (hrs % 1) * TAU
        sa = math.floor(t) * TAU / 60 if not o["spin"] else 0
        line(cr, 0, 0, math.sin(ha) * 70, -math.cos(ha) * 70, lw * 2.2)
        line(cr, 0, 0, math.sin(ma) * 108, -math.cos(ma) * 108, lw * 1.4)
        if o["tick"] and not o["spin"]:
            line(cr, -math.sin(sa) * 20, math.cos(sa) * 20, math.sin(sa) * 118, -math.cos(sa) * 118, lw * 0.5, "alert")
        cr.arc(0, 0, 10, 0, TAU)
        fill(cr, "ink")


class Newspaper(Prop):
    """A broadsheet front page (centre, ~420 x 560): masthead (default a generic red EXTRA! banner; never put an
    invented headline under a real paper's name), headline, columns, a halftone photo.
    spin 0..1 = the classic spinning-in newspaper (turns and grows to full size)."""
    defaults = dict(masthead="EXTRA!", headline="WAR!", sub="", spin=1.0, date="")

    def _draw(self, cr, t, o):
        lw = self.lw * 0.7
        u = clamp01(o["spin"])
        if u < 1:
            cr.rotate((1 - ease_out(u)) * TAU * 2.2)
            k = max(0.02, ease_out(u))
            cr.scale(k, k)
        rrect(cr, -210, -280, 420, 560, 2)
        fill_ink(cr, "#efe5cb", lw, tone=False)
        if o["masthead"] == "EXTRA!":                          # generic banner: never a real paper's name
            poly(cr, [(-200, -270), (200, -270), (194, -214), (-194, -210)])
            fill_ink(cr, "alert", lw, tone=False)
            text(cr, "EXTRA!", 0, -224, 48, font=SLAB, color="cream", bold=False, outline="ink", outline_w=5)
        else:
            text(cr, o["masthead"], 0, -226, 38, font=SLAB, color="ink", bold=False)
        line(cr, -190, -212, 190, -212, lw * 0.6)
        line(cr, -190, -204, 190, -204, lw * 0.3)
        if o["date"]:
            text(cr, o["date"], 0, -188, 16, font=LABEL, color="ink_soft")
        size = 104 if len(o["headline"]) < 8 else 64 if len(o["headline"]) < 14 else 44
        text(cr, o["headline"], 0, -96, size, font=TITLE, color="ink", bold=False)
        if o["sub"]:
            text(cr, o["sub"], 0, -54, 24, font=LABEL, color="ink")
        rrect(cr, -190, -36, 200, 150, 0)
        fill(cr, "#d8cdb2", keep=True)
        dots(cr, "ink_soft", 3)
        cr.new_path()
        r = random.Random(o["seed"])
        for col_ in range(2):
            x0 = 30 + col_ * 85 if col_ == 0 else 120
            for i in range(10):
                line(cr, x0 - 0, -30 + i * 15, x0 + r.uniform(50, 70), -30 + i * 15, lw * 0.5, "ink_soft")
        for col_ in range(3):
            for i in range(8):
                x0 = -190 + col_ * 132
                line(cr, x0, 136 + i * 16, x0 + r.uniform(90, 118), 136 + i * 16, lw * 0.5, "ink_soft")


class Bombe(Prop):
    """A codebreaking 'bombe' machine (~560 wide, ~640 tall): a cabinet of coloured drums that turn as it runs.
    run 0..1 = speed (0 stopped); stop_at = all drums settle (the 'click')."""
    defaults = dict(run=1.0, stop_at=None, color="#3f3a36")
    DRUM_COLS = ("#2f2b28", "#b5322a", "#d9a63a")

    def _draw(self, cr, t, o):
        lw = self.lw
        rrect(cr, -280, -640, 560, 640, 10)
        fill_ink(cr, o["color"], lw)
        rrect(cr, -250, -610, 500, 520, 6)
        fill(cr, shade(o["color"], -0.25))
        settle = o["stop_at"] is not None and t >= o["stop_at"]
        for row in range(3):
            for colm in range(12):
                for sub in range(3):
                    x = -220 + colm * 40
                    y = -560 + row * 170 + sub * 46
                    spd = 0 if settle else o["run"] * (1 + sub * 0.7 + colm * 0.13)
                    a = t * spd * 3 + colm + row
                    cr.arc(x, y, 17, 0, TAU)
                    fill_ink(cr, self.DRUM_COLS[sub], lw * 0.35, tone=False)
                    line(cr, x, y, x + math.cos(a) * 13, y + math.sin(a) * 13, lw * 0.5, "cream")
        rrect(cr, -280, -80, 560, 80, 6)
        fill_ink(cr, shade(o["color"], 0.1), lw)
        for i in range(10):
            cr.arc(-220 + i * 48, -40, 9, 0, TAU)
            fill_ink(cr, "gold" if (settle or int(t * 6 + i) % 3 == 0) else "#5b544c", lw * 0.3, tone=False)


class Microphone(Prop):
    """A 1940s broadcast microphone on a desk stand (~280 tall); on=True sends faint sound arcs."""
    defaults = dict(on=True, color=STEEL)

    def _draw(self, cr, t, o):
        lw = self.lw
        if o["on"]:
            for k in range(3):
                u = (t * 0.8 + k / 3) % 1.0
                for s in (-1, 1):
                    a0 = 0 if s > 0 else math.pi
                    cr.new_sub_path()
                    cr.arc(0, -230, 90 + 120 * u, a0 - 0.4, a0 + 0.4)
                    ink(cr, lw * 0.6, "ink_soft", 0.7 * (1 - u))
        ellipse(cr, 0, -6, 90, 14)
        fill_ink(cr, shade(o["color"], -0.2), lw)
        line(cr, 0, -10, 0, -160, lw * 1.4)
        cr.arc(0, -172, 26, math.pi, TAU)
        ink(cr, lw * 1.3)
        rrect(cr, -44, -300, 88, 110, 30)
        fill_ink(cr, o["color"], lw)
        for i in range(6):
            line(cr, -30, -278 + i * 15, 30, -278 + i * 15, lw * 0.4, shade(o["color"], -0.4))
        rrect(cr, -36, -176, 72, 30, 4)
        fill_ink(cr, "cream", lw * 0.5, tone=False)


class WhiteFlag(Prop):
    """A white flag on a stick planted in the ground (~300 tall), waving."""
    defaults = dict(height=300.0, wind=1.0)

    def _draw(self, cr, t, o):
        lw, h = self.lw, o["height"]
        line(cr, 0, 0, 6, -h, lw * 1.2, WOOD)
        top, bot = [], []
        for i in range(11):
            u = i / 10
            wv = math.sin(t * 4 * o["wind"] - u * 4 + o["seed"]) * 12 * u
            top.append((6 + u * 170, -h + 6 + wv + u * 18))
            bot.append((6 + u * 170, -h + 110 + wv * 1.2 + u * 30))
        poly(cr, top + bot[::-1])
        fill_ink(cr, "white", lw * 0.7, tone=False)
        poly(cr, [(6 + u * 170, (a[1] + b[1]) / 2 + 20) for u, a, b in zip([i / 10 for i in range(11)], top, bot)],
             close=False)
        ink(cr, lw * 0.4, "sky")


class ParachuteIcon(Prop):
    """A small map icon of a parachute (centre, ~60 wide), swaying."""
    defaults = dict(color="cream", line_c="allies")

    def _draw(self, cr, t, o):
        lw = self.lw * 0.6
        cr.rotate(math.sin(t * 2 + o["seed"]) * 0.15)
        cr.arc(0, -16, 30, math.pi, TAU)
        cr.close_path()
        fill_ink(cr, o["color"], lw, line=o["line_c"], tone=False)
        for s in (-30, -10, 10, 30):
            line(cr, s, -16, 0, 24, lw * 0.5, o["line_c"])
        cr.arc(0, 28, 6, 0, TAU)
        fill(cr, o["line_c"])


class Chart(Prop):
    """A poster stock chart (centre, ~900 x 520): axes, grid, a line drawn up to `progress` that climbs then
    plunges off the bottom after `crash` (fraction across). label = the year tag."""
    defaults = dict(progress=1.0, crash=0.62, label="1929", color="alert")

    def _draw(self, cr, t, o):
        lw = self.lw
        rrect(cr, -450, -260, 900, 520, 6)
        fill_ink(cr, "cream", lw, tone=False)
        for i in range(1, 5):
            line(cr, -400, -230 + i * 100, 420, -230 + i * 100, lw * 0.3, "ink_soft", 0.6)
        line(cr, -400, -230, -400, 220, lw)
        line(cr, -400, 220, 420, 220, lw)
        r = random.Random(o["seed"] + 3)
        pts = []
        n = 60
        for i in range(n + 1):
            u = i / n
            if u <= o["crash"]:
                y = 160 - 300 * (u / o["crash"]) ** 1.3 + r.uniform(-14, 14)
            else:
                v = (u - o["crash"]) / (1 - o["crash"])
                y = -140 + 700 * v ** 0.8 + r.uniform(-10, 10)
            pts.append((-400 + 820 * u, y))
        k = int(clamp01(o["progress"]) * n)
        if k >= 1:
            cr.save()
            rrect(cr, -450, -260, 900, 520, 6)
            cr.clip()
            poly(cr, pts[:k + 1], close=False)
            ink(cr, lw * 2.6)
            poly(cr, pts[:k + 1], close=False)
            ink(cr, lw * 1.4, o["color"])
            cr.restore()
        if o["label"]:
            text(cr, o["label"], 340, -190, 54, font=STENCIL, color="ink", bold=True)


def coin(cr, x, y, r, spin, lw=3.0, color=BRASS):
    """One coin at (x, y), radius r, flipping (spin in radians)."""
    k = math.cos(spin)
    ellipse(cr, x, y, r * max(abs(k), 0.12), r)
    fill_ink(cr, color if k > 0 else shade(color, -0.2), lw, tone=False)
    if abs(k) > 0.4:
        ellipse(cr, x, y, r * abs(k) * 0.6, r * 0.6)
        ink(cr, lw * 0.5, shade(color, -0.35))


class Coin(Prop):
    """A gold coin (centre, radius 40), flipping at `flip` turns/s."""
    defaults = dict(flip=1.0, color=BRASS)

    def _draw(self, cr, t, o):
        coin(cr, 0, 0, 40, t * o["flip"] * TAU + o["seed"], self.lw * 0.6, o["color"])


def coin_stream(cr, t, x0, y0, w, h, tx, ty, n=40, start=0.0, dur=2.5, r=14.0, seed=4):
    """n coins scattered over the box (x0, y0, w, h) drain toward (tx, ty) from `start`, shrinking as they go."""
    rr = random.Random(seed)
    for i in range(n):
        sx, sy = x0 + rr.random() * w, y0 + rr.random() * h
        delay = rr.random() * dur * 0.5
        u = ease_in(seg(t, start + delay, start + delay + dur * 0.5))
        if u >= 1:
            continue
        x = lerp(sx, tx, u) + math.sin(u * 9 + i) * 20 * (1 - u)
        y = lerp(sy, ty, u)
        coin(cr, x, y, r * (1 - 0.8 * u), t * 7 + i, max(1.5, r * 0.15))


class Die(Prop):
    """A rolling die (centre, ~120 cube): roll 0..1 tumbles it (bouncing, faces changing) and lands on `value`."""
    defaults = dict(roll=1.0, value=6, color="cream")
    PIPS = {1: [(0, 0)], 2: [(-1, -1), (1, 1)], 3: [(-1, -1), (0, 0), (1, 1)], 4: [(-1, -1), (1, -1), (-1, 1), (1, 1)],
            5: [(-1, -1), (1, -1), (0, 0), (-1, 1), (1, 1)], 6: [(-1, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (1, 1)]}

    def _face(self, cr, pts, val, lw, c):
        poly(cr, pts)
        fill_ink(cr, c, lw, tone=False)
        cx = sum(p[0] for p in pts) / 4
        cy = sum(p[1] for p in pts) / 4
        ax = ((pts[1][0] - pts[0][0]) / 2, (pts[1][1] - pts[0][1]) / 2)
        ay = ((pts[3][0] - pts[0][0]) / 2, (pts[3][1] - pts[0][1]) / 2)
        for px, py in self.PIPS[val]:
            x = cx + (ax[0] * px + ay[0] * py) * 0.55
            y = cy + (ax[1] * px + ay[1] * py) * 0.55
            cr.arc(x, y, 8, 0, TAU)
            fill(cr, "ink")

    def _draw(self, cr, t, o):
        lw = self.lw * 0.8
        u = clamp01(o["roll"])
        bounce = abs(math.sin(u * math.pi * 3)) * (1 - u) * 140
        cr.translate((u - 1) * 300, -bounce)
        cr.rotate((1 - ease_out(u)) * TAU * 1.5)
        k = int((1 - u) * 12)
        v = o["value"] if u >= 1 else 1 + (o["value"] + k) % 6
        s = 60
        top = [(-s, -s * 0.5), (0, -s), (s, -s * 0.5), (0, 0)]
        left = [(-s, -s * 0.5), (0, 0), (0, s * 1.1), (-s, s * 0.6)]
        right = [(0, 0), (s, -s * 0.5), (s, s * 0.6), (0, s * 1.1)]
        self._face(cr, top, v, lw, o["color"])
        self._face(cr, left, 1 + (v + 1) % 6, lw, shade(o["color"], -0.12))
        self._face(cr, right, 1 + (v + 3) % 6, lw, shade(o["color"], -0.24))


class Thermometer(Prop):
    """A tall frosty thermometer (bulb centre at the origin, ~520 tall), scale 0 to -40 C; temp = current reading."""
    defaults = dict(temp=0.0, lo=-40.0, hi=10.0)

    def _draw(self, cr, t, o):
        lw = self.lw
        rrect(cr, -70, -560, 140, 620, 30)
        fill_ink(cr, "#d6d2c2", lw)
        rrect(cr, -18, -520, 36, 500, 18)
        fill_ink(cr, "cream", lw * 0.7, tone=False)
        for v in range(int(o["lo"]), int(o["hi"]) + 1, 10):
            y = lerp(-40, -500, (v - o["lo"]) / (o["hi"] - o["lo"]))
            line(cr, 22, y, 40, y, lw * 0.6)
            text(cr, f"{v}", 44, y + 8, 22, font=LABEL, color="ink", align="left")
        y = lerp(-40, -500, (clamp01((o["temp"] - o["lo"]) / (o["hi"] - o["lo"]))))
        rrect(cr, -9, y, 18, -y, 9)
        fill(cr, "alert")
        cr.arc(0, 0, 40, 0, TAU)
        fill_ink(cr, "alert", lw, tone=False)
        for i in range(5):                                                      # frost crystals
            x, yy = -50 + i * 6, -480 + i * 60
            for a in range(3):
                aa = a * math.pi / 3
                line(cr, x - math.cos(aa) * 10, yy - math.sin(aa) * 10, x + math.cos(aa) * 10,
                     yy + math.sin(aa) * 10, lw * 0.3, "white")


class Headphones(Prop):
    """A 1940s radio operator's headset (centre, ~240 wide)."""
    defaults = dict(color="#3b3633")

    def _draw(self, cr, t, o):
        lw = self.lw
        cr.arc(0, 10, 110, math.pi * 1.05, math.pi * 1.95)
        ink(cr, 22 + lw * 2)
        cr.arc(0, 10, 110, math.pi * 1.05, math.pi * 1.95)
        ink(cr, 22, STEEL)
        for s in (-1, 1):
            ellipse(cr, s * 112, 20, 34, 48)
            fill_ink(cr, o["color"], lw, tone=False)
            ellipse(cr, s * 112, 20, 18, 28)
            fill(cr, shade(o["color"], 0.25))
        cr.move_to(112, 64)
        cr.curve_to(140, 140, 40, 160, 20, 220)
        ink(cr, lw * 0.6)


class Papers(Prop):
    """A stack of intercepted code sheets (centre, ~380 x 260) in five-letter groups; circle 0..1 draws a red ring
    round one word (word=index)."""
    defaults = dict(circle=0.0, word=7, lines=6)

    def _draw(self, cr, t, o):
        lw = self.lw * 0.6
        for k, (dx, a) in enumerate(((14, 0.06), (-8, -0.04), (0, 0.0))):
            cr.save()
            cr.translate(dx, k * 4)
            cr.rotate(a)
            rrect(cr, -190, -130, 380, 260, 2)
            fill_ink(cr, "#efe5cb" if k == 2 else "#e0d4b6", lw, tone=False)
            cr.restore()
        r = random.Random(o["seed"] + 9)
        target = None
        idx = 0
        for i in range(o["lines"]):
            for j in range(4):
                s = "".join(chr(65 + r.randrange(26)) for _ in range(5))
                x, y = -150 + j * 92, -86 + i * 36
                text(cr, s, x, y, 24, font=STENCIL, color="ink", align="left", bold=True)
                if idx == o["word"]:
                    target = (x + 34, y - 8)
                idx += 1
        u = clamp01(o["circle"])
        if u > 0 and target:
            cr.save()
            cr.translate(*target)
            cr.scale(1.0, 0.5)
            cr.arc(0, 0, 70, -1.6, -1.6 + TAU * u * 1.05)
            cr.restore()
            ink(cr, lw * 1.2, "alert")


class Pact(Prop):
    """A treaty sheet (centre, ~320 x 440) with two signatures; tear 0..1 rips it down the middle and the halves
    fly apart."""
    defaults = dict(tear=0.0, title="TREATY")

    def _half(self, cr, side, lw, o, jag):
        pts = [(0, -220)] + list(jag) + [(0, 220)]
        if side < 0:
            outline = [(-160, -220)] + pts + [(-160, 220)]
        else:
            outline = [(160, -220)] + pts + [(160, 220)]
        poly(cr, outline)
        fill_ink(cr, "#efe5cb", lw, tone=False)
        cr.save()
        poly(cr, outline)
        cr.clip()
        self._marks(cr, lw, o)
        cr.restore()

    def _marks(self, cr, lw, o):
        text(cr, o["title"], 0, -160, 44, font=SLAB, color="ink", bold=False)
        for i in range(8):
            line(cr, -120, -110 + i * 26, 120, -110 + i * 26, lw * 0.5, "ink_soft")
        for sx in (-80, 80):
            cr.move_to(sx - 50, 150)
            for k in range(8):
                cr.line_to(sx - 50 + k * 14, 150 + math.sin(k * 1.7 + sx) * 8)
            ink(cr, lw * 0.6, "#1f3c7a")

    def _draw(self, cr, t, o):
        lw = self.lw * 0.7
        u = clamp01(o["tear"])
        r = random.Random(o["seed"] + 2)
        jag = [(r.uniform(-10, 10), -220 + i * 40) for i in range(1, 11)]
        if u <= 0:
            rrect(cr, -160, -220, 320, 440, 2)
            fill_ink(cr, "#efe5cb", lw, tone=False)
            self._marks(cr, lw, o)
            return
        for side in (-1, 1):
            cr.save()
            cr.translate(side * 160 * ease_out(u), 30 * u * u)
            cr.rotate(side * 0.35 * ease_out(u))
            self._half(cr, side, lw, o, jag)
            cr.restore()


class Paper(Prop):
    """A sheet of paper (centre, ~300 x 400) with typed lines (lines=(...) or grey rules); crumple 0..1 squeezes it
    into a ball."""
    defaults = dict(crumple=0.0, lines=(), signed=True)

    def _draw(self, cr, t, o):
        lw = self.lw * 0.7
        u = smooth(clamp01(o["crumple"]))
        r = random.Random(o["seed"] + 1)
        flat = [(-150, -200), (0, -204), (150, -200), (154, 0), (150, 200), (0, 204), (-150, 200), (-154, 0)]
        ball = []
        for i in range(16):
            a = TAU * i / 16
            rad = 90 * r.uniform(0.8, 1.15)
            ball.append((math.cos(a) * rad, math.sin(a) * rad))
        fl16 = []
        for i in range(16):
            a, b = flat[i // 2], flat[(i // 2 + 1) % 8]
            f = (i % 2) * 0.5
            fl16.append((lerp(a[0], b[0], f), lerp(a[1], b[1], f)))
        pts = [(lerp(p[0], q[0], u), lerp(p[1], q[1], u)) for p, q in zip(fl16, ball)]
        poly(cr, pts)
        fill_ink(cr, "#efe5cb", lw, tone=False)
        if u < 0.5:
            a = 1 - u * 2
            if o["lines"]:
                for i, s in enumerate(o["lines"][:6]):
                    text(cr, s, 0, -130 + i * 44, 30, font=LABEL, color="ink", alpha=a)
            else:
                for i in range(9):
                    line(cr, -110, -150 + i * 32, 110, -150 + i * 32, lw * 0.5, "ink_soft", a)
            if o["signed"]:
                cr.move_to(-40, 160)
                for k in range(8):
                    cr.line_to(-40 + k * 14, 160 + math.sin(k * 1.7) * 8)
                ink(cr, lw * 0.6, "#1f3c7a", a)
        else:
            for i in range(7):
                p, q = r.randrange(16), r.randrange(16)
                line(cr, pts[p][0] * 0.6, pts[p][1] * 0.6, pts[q][0] * 0.3, pts[q][1] * 0.3, lw * 0.4, "ink_soft")


__all__ = [n for n in dir() if not n.startswith("_") and n not in ("math", "random")]


def _sheet(t=1.3, out=None):
    """Contact sheet of everything in this module: out/ww2/style/props_sheet_2.png."""
    import os
    from channels.ww2.kit.core import ROOT, paper, print_finish, render_clip
    from channels.ww2.kit.props import Tank

    def draw(cr, tt):
        paper(cr)
        items = [
            (Airliner(x=260, y=300, scale=0.36), dict(door=1.0)),
            (TurretCloseup(x=640, y=290, scale=0.2), dict(turret=35, fire=[tt - 0.05])),
            (Hedgehog(x=860, y=300, scale=0.6), {}),
            (FortWall(x=1100, y=300, scale=0.3), {}),
            (FortIcon(x=1300, y=250, scale=0.8), dict(glow=0.8)),
            (Podium(x=1440, y=300, scale=0.5), {}),
            (Parliament(x=1740, y=300, scale=0.26), {}),
            (Padlock(x=110, y=520, scale=0.42), dict(snap_at=tt - 0.5)),
            (RuinedSkyline(x=440, y=590, scale=0.22, width=1500), {}),
            (BuildingSection(x=770, y=600, scale=0.38), {}),
            (BunkerDoor(x=1000, y=600, scale=0.4), dict(close=0.6)),
            (LongTable(x=1330, y=600, scale=0.3), {}),
            (Island(x=1720, y=600, scale=0.3), dict(bursts=[tt - 0.2])),
            (Tree(x=60, y=880, scale=0.55, kind="pine"), {}),
            (Tree(x=160, y=880, scale=0.55, kind="oak"), {}),
            (Tree(x=250, y=880, scale=0.55, kind="birch"), {}),
            (Flag(x=320, y=880, scale=0.6), dict(stripe="cream")),
            (Pedestal(x=500, y=880, scale=0.55), dict(crack=0.6)),
            (Clock(x=690, y=760, scale=0.6), {}),
            (Newspaper(x=880, y=780, scale=0.38), dict(headline="WAR!", date="3 SEPTEMBER 1939")),
            (Bombe(x=1080, y=880, scale=0.3), {}),
            (Microphone(x=1230, y=880, scale=0.5), {}),
            (WhiteFlag(x=1310, y=880, scale=0.55), {}),
            (ParachuteIcon(x=1520, y=740, scale=1.0), {}),
            (Chart(x=1730, y=760, scale=0.3), dict(progress=0.9)),
            (Die(x=1530, y=860, scale=0.5), dict(roll=1.0, value=5)),
            (Thermometer(x=60, y=1020, scale=0.28), dict(temp=-30)),
            (Headphones(x=200, y=1010, scale=0.45), {}),
            (Papers(x=400, y=1000, scale=0.38), dict(circle=1.0)),
            (Pact(x=620, y=990, scale=0.2), dict(tear=0.0)),
            (Pact(x=760, y=990, scale=0.2), dict(tear=0.5)),
            (Paper(x=930, y=990, scale=0.2), dict(lines=("PEACE", "FOR OUR", "TIME"))),
            (Paper(x=1050, y=1000, scale=0.3), dict(crumple=1.0)),
            (Coin(x=1180, y=1000, scale=0.8), {}),
        ]
        for p, kw in items:
            p.draw(cr, tt, **kw)
        coin_stream(cr, tt, 1250, 950, 200, 80, 1500, 1040, n=14, start=tt - 1.0, dur=3.0)
        forest(cr, tt, 1560, 1900, 1060, n=6, scale=0.3, seed=2)
        Tank(x=1700, y=1066, scale=0.3, side="germany", silhouette="ink").draw(cr, tt, speed=80)
        print_finish(cr, tt)

    out = out or os.path.join(ROOT, "out", "ww2", "style", "props_sheet_2.png")
    return render_clip(draw, 1, out, still=t)


if __name__ == "__main__":
    print(_sheet())
