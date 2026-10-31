"""The A/B vote cards for the split-screen ending (Episode 1 v3, S24; Q5 of DIORAMA_EP01_V3.md): a big round letter
badge with a word tag beside it, popping in with an overshoot on the narrator's "Option A" / "Option B" and pulsing
together on "Comment A or B".

Same convention as fx2d: every element is fn(cr, t, start, ...) on a 720x1280 frame, t and start in shot seconds, and
it draws nothing before `start` (or after `end`). The pop runs on 1s like the other 2D effects; the idle bob steps on
2s like the characters. Sound is in the mix (ep01v3_sound.option_sting), so these cue nothing by default.

Layout (DIORAMA_EP01_V3.md readability): both cards sit left of x 560 (the Shorts buttons) and clear of the caption
band (845-930); A rides in the top panel under the Shorts top bar, B in the bottom panel above the captions.
Our own design (OFL fonts, plain shapes): no franchise look.

    fx2d_ab.ab_cards(cr, t, a_at=0.4, b_at=2.9, both_at=4.6)     # in the S24 overlay, with the line's word times
"""
import math

from motion.engine import FPS, H, W, back_out, cairo, clamp01, cue
from motion.polish import rrect, text_width

from channels.monsters import fx2d

A_COL = fx2d.hexa("#ff5a3c")          # SAVE: warm coral, the threat word colour of the hook and covers
B_COL = fx2d.hexa("#3aa8ff")          # RUN: cool blue
A_POS = (124, 236)                     # badge centres: under the top bar / above the caption band
B_POS = (124, 700)
R = 84                                 # badge radius (168 px across: about 37 px wide at 160 px phone-grid size)
POP = 0.32                             # seconds for the pop (0 -> overshoot -> 1)


def _bob(t, start):
    """A small idle bob after the pop, stepped on 2s."""
    f = int(math.floor((t - start) * FPS + 1e-6)) // 2 * 2
    return math.sin(f / FPS * 2 * math.pi * 0.9) * 4.0


def _pulse(t, at):
    """1 at `at`, easing back to 0 over 0.3 s (the both-cards bump on "Comment A or B")."""
    if at is None or t < at:
        return 0.0
    return max(0.0, 1 - (t - at) / 0.3)


def ab_card(cr, t, start, letter="A", label="SAVE", pos=None, col=None, end=None, pulse_at=None, sound=False):
    """One card: a coloured badge with a big white letter (thick ink outline, drop shadow, a gloss band) and a white
    word tag beside it. It pops from nothing to an overshoot and settles in POP seconds, with a white flash ring."""
    if t < start or (end is not None and t > end):
        return
    if sound:
        cue("m_ui_select", t, start)
    x, y = pos or (A_POS if letter == "A" else B_POS)
    col = col or (A_COL if letter == "A" else B_COL)
    u = (t - start) / POP
    s = back_out(u, 2.6) if u < 1 else 1.0
    s *= 1 + 0.12 * _pulse(t, pulse_at)
    y += _bob(t, start + POP) if u >= 1 else 0.0
    spin = (1 - clamp01(u)) * -0.35                               # it swings upright as it lands
    cr.save()
    cr.translate(x, y)
    cr.rotate(spin)
    cr.scale(max(s, 1e-3), max(s, 1e-3))
    # shadow, badge, ink rim, gloss
    cr.arc(6, 10, R, 0, 2 * math.pi)
    cr.set_source_rgba(0, 0, 0, 0.35)
    cr.fill()
    cr.arc(0, 0, R, 0, 2 * math.pi)
    cr.set_source_rgba(*col)
    cr.fill_preserve()
    cr.set_line_width(10)
    cr.set_source_rgba(*fx2d.INK)
    cr.stroke()
    cr.arc(0, 0, R - 14, math.pi * 1.1, math.pi * 1.9)
    cr.set_line_width(9)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_source_rgba(1, 1, 1, 0.45)
    cr.stroke()
    size = R * 1.55
    fx2d._text(cr, letter, 0, size * 0.36, size, fx2d.WHITE, fx2d.DISPLAY, "center", outline=fx2d.INK,
               ow=size * 0.14, shadow=0.4)
    cr.restore()
    # the word tag slides out from behind the badge once it has landed
    v = clamp01((t - start - POP * 0.6) / 0.18)
    if v > 0 and label:
        size = 64
        tw = text_width(cr, label, size, fx2d.DISPLAY)
        x0 = x + R * 0.75
        w = (tw + 52) * v
        cr.save()
        rrect(cr, x0, y - 40, w, 80, 40)
        cr.set_source_rgba(1, 1, 1, 0.96)
        cr.fill_preserve()
        cr.set_line_width(7)
        cr.set_source_rgba(*fx2d.INK)
        cr.stroke()
        cr.rectangle(x0, y - 44, w, 88)
        cr.clip()
        fx2d._text(cr, label, x0 + 22 + R * 0.25, y + size * 0.36, size, col, fx2d.DISPLAY, "left")
        cr.restore()
    # the flash ring on landing (1s)
    k = (t - start) / 0.25
    if 0 <= k < 1:
        cr.save()
        cr.arc(x, y, R * (1.05 + 0.45 * k), 0, 2 * math.pi)
        cr.set_line_width(10 * (1 - k))
        cr.set_source_rgba(1, 1, 1, 0.9 * (1 - k))
        cr.stroke()
        cr.restore()


def ab_cards(cr, t, a_at, b_at, both_at=None, end=None, labels=("SAVE", "RUN")):
    """Both cards for the S24 split: A pops on "Option A" (a_at), B on "Option B" (b_at), both pulse on
    "Comment A or B" (both_at). Times in shot seconds."""
    ab_card(cr, t, a_at, "A", labels[0], end=end, pulse_at=both_at)
    ab_card(cr, t, b_at, "B", labels[1], end=end, pulse_at=both_at)

