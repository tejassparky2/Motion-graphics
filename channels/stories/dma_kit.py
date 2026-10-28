"""DEAD MAN'S ALGORITHM, Parts 3-6: the pieces the episodes share (approved script: channels/stories/
dma_arc_games_1_2.md v4). The cast's voices, the camera, rule and statement cards, the chamber of Game 1, the white
room of Game 2 with its PLAYERS screen, gold tokens, Momo's pile, the proof card, the ledger and the flashback look.
Every number on screen is drawn here from the story's numbers, never painted.
"""
import math

from motion.engine import W, H, cairo, clamp01, seg

from channels.horror import hud2d
from channels.horror.toon2d import glow, hexa, noise
from channels.stories import anime2d as AN
from channels.stories import dma_anime, dma_art

A = dma_anime


def use(mod):
    """The drawing module the episode picked (dma_anime, or dma_art for ANIME=0)."""
    global A
    A = mod


SPEAKERS = {
    "ren": dict(voice="am_echo", turbo_ref="am_echo"),         # Ren's own lines: the narrator's voice, mouth moving
    "haruto": dict(voice="am_puck", turbo_ref="am_puck"),
    "yui": dict(voice="af_heart", turbo_ref="af_heart"),
    "riku": dict(voice="am_fenrir", turbo_ref="am_fenrir"),
    "kota": dict(voice="am_eric", turbo_ref="am_eric+1"),
    "go": dict(voice="am_onyx", turbo_ref="am_onyx-1"),
    "aoi": dict(voice="af_kore", turbo_ref="af_kore"),
    "mio": dict(voice="af_bella", turbo_ref="af_bella"),
    "saki": dict(voice="af_nicole", turbo_ref="af_nicole"),
    "momo": dict(voice="af_sky", turbo_ref="af_sky+5"),
}
CYAN = (0.55, 1, 0.85, 1)
RED = hud2d.RED
GOLD, GOLD_D = hexa("#e8c04a"), hexa("#a8821c")
BY = 940                                                      # where a bust's neck sits in a talking shot


def camera(cr, t, s0, s1, z0=1.0, z1=1.06, cx=W / 2, cy=H / 2, shake=1.0, pan=(0.0, 0.0)):
    """A slow push-in with a little handheld drift (and an optional pan in px over the shot)."""
    k = seg(t, s0, s1)
    z = z0 + (z1 - z0) * k
    cr.translate(cx + 4 * shake * noise(t * 0.7, 1) - pan[0] * k, cy + 3 * shake * noise(t * 0.6, 4) - pan[1] * k)
    cr.rotate(0.004 * shake * noise(t * 0.5, 7))
    cr.scale(z, z)
    cr.translate(-cx, -cy)


def fmt(sec):
    return f"{int(sec // 60)}:{int(sec % 60):02d}"


def shot_index(tl, plan):
    """plan: [(beat id or time, name)] -> [(start, name)] sorted, ending with a sentinel."""
    out = []
    for at, name in plan:
        s = at if isinstance(at, (int, float)) else tl.by_id[at].start - 0.15
        out.append((max(0.0, s), name))
    out.sort(key=lambda p: p[0])
    return out + [(tl.total + 1, "end")]


def current(sh, t):
    k = max(i for i, (at, _) in enumerate(sh) if at <= t or i == 0)
    return sh[k][0], sh[k][1], sh[k + 1][0]


# ------------------------------------------------------------------ cards
def _wrap(cr, words, size, max_w, font):
    lines, cur = [], []
    for wd in words:
        if cur and A.text_width(cr, " ".join(cur + [wd]), size, font) > max_w:
            lines.append(cur)
            cur = [wd]
        else:
            cur.append(wd)
    return lines + [cur]


def card(cr, t, start, end, kicker, text, hot=(), y=H * 0.5, size=34, col=CYAN):
    """A rule card slammed on screen: KICKER in red, the text in mono, words in `hot` (a phrase) in red."""
    if t < start or t > end + 0.25:
        return
    p = clamp01((t - start) / 0.15)
    a = 1 - clamp01((t - end) / 0.25)
    font = "Liberation Mono"
    w = W * 0.86
    words = text.upper().split()
    hot_words = set(" ".join(hot).upper().split())
    lines = _wrap(cr, words, size, w - 60, font)
    h = 150 + len(lines) * size * 1.35
    cr.save()
    cr.push_group()
    cr.translate(W / 2, y)
    s = 1.25 - 0.25 * p
    cr.scale(s, s)
    A.tk.tk_rrect(cr, -w / 2, -h / 2, w, h, 18)
    cr.set_source_rgba(0.03, 0.05, 0.06, 0.93)
    cr.fill_preserve()
    cr.set_source_rgba(*col[:3], 0.9)
    cr.set_line_width(4)
    cr.stroke()
    hud2d._text(cr, kicker, 0, -h / 2 + 68, 46, RED, hud2d.ROUND, "center")
    sp = A.text_width(cr, " ", size, font)
    for j, ln in enumerate(lines):
        lw = A.text_width(cr, " ".join(ln), size, font)
        x = -lw / 2
        yy = -h / 2 + 130 + j * size * 1.35
        for wd in ln:
            bare = wd.strip(".,!?")
            c = RED if bare in hot_words else col
            if bare in hot_words:
                glow(cr, x + A.text_width(cr, wd, size, font) / 2, yy - size * 0.3, size * 2, RED[:3],
                     0.25 * (0.6 + 0.4 * math.sin(t * 6)))
            hud2d._text(cr, wd, x, yy, size, c, font)
            x += A.text_width(cr, wd, size, font) + sp
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def slam(cr, t, start, end, lines, y=H * 0.3, size=76):
    """Big statement text slammed in (MY NUMBER: 1): [(text, red?)], each line fitted to the frame."""
    if t < start or t > end + 0.25:
        return
    p = clamp01((t - start) / 0.12)
    a = clamp01((t - start) / 0.06) * (1 - clamp01((t - end) / 0.25))
    cr.save()
    cr.push_group()
    cr.translate(W / 2, y)
    s = 1.4 - 0.4 * p
    cr.scale(s, s)
    for k, (txt, red) in enumerate(lines):
        sz = min(size, size * (W - 80) / max(1, A.text_width(cr, txt, size, hud2d.ROUND)))
        hud2d._text(cr, txt, 0, k * size * 1.08, sz, RED if red else (1, 1, 1, 1), hud2d.ROUND, "center",
                    outline=(0.05, 0.03, 0.06, 1), ow=sz * 0.14, shadow=0.5)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def rules_strip(cr, t, shown, hot=None, n=5):
    """Small chips R1..Rn under the status bar once each is read; the one in play turns red."""
    x = 18
    for k in range(1, min(shown, n) + 1):
        w = 64
        A.tk.tk_rrect(cr, x, 66, w, 36, 18)
        cr.set_source_rgba(*(RED[:3] if hot == k else (0.04, 0.06, 0.07)), 0.92)
        cr.fill_preserve()
        cr.set_source_rgba(*CYAN[:3], 0.6)
        cr.set_line_width(2)
        cr.stroke()
        hud2d._text(cr, f"R{k}", x + w / 2, 91, 22, (1, 1, 1, 1), hud2d.ROUND, "center")
        x += w + 8


def proof(cr, t, start, end, steps, y0=H * 0.2, gap=None):
    """The answer as a chain of boxes, one per step, each arriving on its beat: [(text, at, red?)]."""
    if t < start or t > end + 0.25:
        return
    a = 1 - clamp01((t - end) / 0.25)
    gap = gap or H * 0.13
    cr.save()
    cr.push_group()
    cr.set_source_rgba(0.01, 0.02, 0.03, 0.55 * clamp01((t - start) / 0.2))
    cr.paint()
    w = W * 0.8
    for k, (txt, at, red) in enumerate(steps):
        if t < at:
            break
        p = clamp01((t - at) / 0.18)
        yc = y0 + k * gap
        cr.save()
        cr.translate(W / 2, yc)
        cr.scale(0.9 + 0.1 * p, 0.9 + 0.1 * p)
        A.tk.tk_rrect(cr, -w / 2, -48, w, 96, 16)
        cr.set_source_rgba(*((0.35, 0.03, 0.03) if red else (0.03, 0.06, 0.07)), 0.95 * p)
        cr.fill_preserve()
        cr.set_source_rgba(*(RED[:3] if red else CYAN[:3]), 0.95 * p)
        cr.set_line_width(4)
        cr.stroke()
        sz = min(40, 40 * (w - 50) / max(1, A.text_width(cr, txt, 40, hud2d.ROUND)))
        hud2d._text(cr, txt, 0, sz * 0.36, sz, (1, 1, 1, p), hud2d.ROUND, "center")
        cr.restore()
        if k + 1 < len(steps) and t >= steps[k + 1][1]:     # the arrow to the next step
            cr.set_source_rgba(*CYAN[:3], 0.9)
            cr.set_line_width(6)
            cr.move_to(W / 2, yc + 52)
            cr.line_to(W / 2, yc + gap - 56)
            cr.stroke()
            cr.move_to(W / 2 - 16, yc + gap - 70)
            cr.line_to(W / 2, yc + gap - 52)
            cr.line_to(W / 2 + 16, yc + gap - 70)
            cr.stroke()
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def ledger(cr, t, start, end, rows, y=H * 0.3):
    """Momo's result board: [(name, tokens)], the poorest row turning red and shaking."""
    if t < start or t > end + 0.25:
        return
    a = clamp01((t - start) / 0.15) * (1 - clamp01((t - end) / 0.25))
    poorest = min(v for _, v in rows)
    w, rh = W * 0.84, 92
    h = 110 + rh * len(rows)
    cr.save()
    cr.push_group()
    cr.translate(W / 2, y)
    A.tk.tk_rrect(cr, -w / 2, 0, w, h, 18)
    cr.set_source_rgba(0.02, 0.03, 0.04, 0.95)
    cr.fill_preserve()
    cr.set_source_rgba(*CYAN[:3], 0.8)
    cr.set_line_width(4)
    cr.stroke()
    hud2d._text(cr, "TIME'S UP · PLAYERS", 0, 62, 32, (*CYAN[:3], 1), "Liberation Mono", "center")
    for k, (name, v) in enumerate(rows):
        at = start + 0.5 + 0.9 * k
        if t < at:
            continue
        low = v == poorest and t > start + 0.5 + 0.9 * len(rows)
        yy = 110 + k * rh
        jit = 3 * math.sin(t * 40) if low else 0
        if low:
            cr.set_source_rgba(*RED[:3], 0.3 + 0.15 * math.sin(t * 8))
            cr.rectangle(-w / 2 + 12, yy + 8, w - 24, rh - 16)
            cr.fill()
        col = RED if low else (1, 1, 1, 1)
        hud2d._text(cr, name, -w / 2 + 40 + jit, yy + 60, 38, col, hud2d.ROUND)
        hud2d._text(cr, str(v), w / 2 - 40 + jit, yy + 60, 46, col, "Liberation Mono", "right")
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def flashback(cr, k=1.0):
    """Drain the colour and warm it (a remembered moment)."""
    if k <= 0:
        return
    cr.save()
    cr.set_operator(cairo.OPERATOR_HSL_SATURATION)
    cr.set_source_rgba(0.5, 0.5, 0.5, 0.85 * k)
    cr.paint()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.set_source_rgba(0.35, 0.25, 0.12, 0.18 * k)
    cr.paint()
    g = cairo.RadialGradient(W / 2, H / 2, H * 0.25, W / 2, H / 2, H * 0.7)
    g.add_color_stop_rgba(0, 0, 0, 0, 0)
    g.add_color_stop_rgba(1, 0, 0, 0, 0.6 * k)
    cr.set_source(g)
    cr.paint()
    cr.restore()


def dark(cr, a):
    if a > 0:
        cr.set_source_rgba(0, 0, 0.01, a)
        cr.paint()


# ------------------------------------------------------------------ Game 1: the chamber
def chamber(cr, t, lines, momo_at=None, case=True):
    """The chamber of Game 1 with the glass case and the wall screen showing `lines`."""
    A.chamber(cr, t, screen=A.screen_text(lines, col=CYAN, momo_at=momo_at, t=t))
    if case:
        A.glass_case(cr, t, W / 2, H * 0.62, 0.9)


def key(cr, x, y, s, rot=-0.4, glow_k=1.0):
    """The gold exit key."""
    cr.save()
    cr.translate(x, y)
    cr.rotate(rot)
    cr.scale(s, s)
    glow(cr, 0, 0, 160, (1, 0.85, 0.45), 0.35 * glow_k)
    A.toon(cr, lambda c: c.arc(-40, 0, 22, 0, 2 * math.pi), GOLD, GOLD_D, (-3, -3), (1, 1, 0.8, 0.6), (-4, -4), lw=3)
    cr.set_source_rgba(0.06, 0.05, 0.03, 1)
    cr.arc(-40, 0, 9, 0, 2 * math.pi)
    cr.fill()
    A.toon(cr, lambda c: c.rectangle(-20, -6, 80, 12), GOLD, GOLD_D, (-2, -2), None, lw=3)
    A.toon(cr, lambda c: A.poly(c, [(40, 6), (40, 22), (50, 22), (50, 14), (58, 14), (58, 6)]), GOLD, GOLD_D,
           (-2, -2), None, lw=2.5)
    cr.restore()


def door(cr, t, k):
    """The sealed chamber door opening on white light (k 0..1)."""
    cr.set_source_rgba(0.03, 0.035, 0.04, 1)
    cr.paint()
    dw, dh = W * 0.62, H * 0.62
    x0, y0 = (W - dw) / 2, H * 0.2
    A.toon(cr, lambda c: c.rectangle(x0 - 20, y0 - 20, dw + 40, dh + 20), hexa("#2a2d31"), hexa("#16181b"), (0, -6),
           None, lw=5)
    gap = dw * 0.5 * k
    if gap > 0:
        cr.set_source_rgba(1, 1, 1, 1)
        cr.rectangle(W / 2 - gap, y0, gap * 2, dh)
        cr.fill()
        glow(cr, W / 2, y0 + dh / 2, 300 + 900 * k, (1, 1, 1), 0.5 + 0.4 * k)
    for sx in (-1, 1):                                         # the two door leaves sliding apart
        cr.save()
        cr.rectangle(*((x0, y0, dw / 2 - gap, dh) if sx < 0 else (W / 2 + gap, y0, dw / 2 - gap, dh)))
        cr.set_source_rgba(0.16, 0.17, 0.19, 1)
        cr.fill()
        cr.restore()
    if k > 0.3:
        cr.set_source_rgba(1, 1, 1, (k - 0.3) / 0.7 * 0.85)
        cr.paint()


# ------------------------------------------------------------------ Game 2: the white room
def wall_screen(cr, t, lines, flash=0.0, red=False):
    """The big screen on the white room's far wall."""
    sw, sh = W * 0.62, H * 0.15
    x0, y0 = W * 0.08, H * 0.13
    A.toon(cr, lambda c: A.tk.tk_rrect(c, x0 - 12, y0 - 12, sw + 24, sh + 24, 10), hexa("#1d1f22"), None, (0, 0),
           None, lw=3)
    cr.save()
    cr.rectangle(x0, y0, sw, sh)
    cr.clip()
    cr.set_source_rgba(0.02, 0.04, 0.05, 1)
    cr.paint()
    A.screen_text(lines, col=RED if red else CYAN)(cr, x0, y0, sw, sh)
    for yy in range(int(y0), int(y0 + sh), 4):
        cr.set_source_rgba(0, 0, 0, 0.18)
        cr.rectangle(x0, yy, sw, 1.5)
        cr.fill()
    if flash > 0:
        cr.set_source_rgba(1, 1, 1, 0.6 * flash)
        cr.paint()
    cr.restore()
    glow(cr, x0 + sw / 2, y0 + sh / 2, sw * 0.7, RED[:3] if red else (0.4, 0.9, 1), 0.18)


def white_room(cr, t, lines=None, flash=0.0, red=False, momo=True, pile=0, lights=1.0, side=False):
    """Game 2's white room: the painted plate, the wall screen, Momo sitting in the middle with its pile of tokens.
    side=True (behind a close-up): Momo sits off to the right, smaller, so it never pokes up behind a head."""
    if A is dma_anime and A._bg("white_room"):
        AN.paint_bg(cr, A._bg("white_room"), ax=0.45)
    else:
        g = cairo.LinearGradient(0, 0, 0, H)
        g.add_color_stop_rgb(0, 0.86, 0.88, 0.9)
        g.add_color_stop_rgb(0.62, 0.94, 0.95, 0.96)
        g.add_color_stop_rgb(1, 0.8, 0.82, 0.85)
        cr.set_source(g)
        cr.paint()
    if lines:
        wall_screen(cr, t, lines, flash, red)
    mx, my, ms = (W * 0.9, H * 0.7, 0.75) if side else (W * 0.5, H * 0.76, 1.15)
    if pile:
        token_pile(cr, mx + (-110 if side else 150), my - 5, pile)
    if momo:
        A.momo(cr, mx, my, ms, t, mood="happy")
    if lights < 1:
        dark(cr, 1 - lights)


def token(cr, x, y, r, a=1.0, glint=0.0):
    """One gold token: a coin with a ring and an engraved M."""
    cr.save()
    cr.translate(x, y)
    cr.push_group()
    g = cairo.RadialGradient(-r * 0.3, -r * 0.3, r * 0.1, 0, 0, r)
    g.add_color_stop_rgb(0, 1.0, 0.92, 0.6)
    g.add_color_stop_rgb(0.7, *GOLD[:3])
    g.add_color_stop_rgb(1, *GOLD_D[:3])
    cr.arc(0, 0, r, 0, 2 * math.pi)
    cr.set_source(g)
    cr.fill_preserve()
    cr.set_source_rgba(0.35, 0.25, 0.05, 1)
    cr.set_line_width(max(1.5, r * 0.08))
    cr.stroke()
    cr.arc(0, 0, r * 0.72, 0, 2 * math.pi)
    cr.set_source_rgba(0.55, 0.4, 0.08, 0.8)
    cr.set_line_width(max(1, r * 0.05))
    cr.stroke()
    hud2d._text(cr, "M", 0, r * 0.32, r * 0.9, (0.5, 0.36, 0.06, 0.9), hud2d.ROUND, "center")
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    if glint > 0:
        glow(cr, r * 0.4, -r * 0.4, r * 1.6, (1, 1, 0.9), 0.6 * glint)
    cr.restore()


def stack(cr, x, y, n, r=26, label=True, red=False):
    """A short stack of tokens with its count underneath (n = the number the player holds)."""
    h = min(12, max(1, int(math.ceil(n / 10)))) if n else 0
    for k in range(h):
        cr.save()
        cr.translate(x, y - k * r * 0.28)
        cr.scale(1, 0.42)
        token(cr, 0, 0, r)
        cr.restore()
    if label:
        hud2d._text(cr, str(n), x, y + r * 1.4, r * 1.2, RED if red else (1, 1, 1, 1), "Liberation Mono", "center",
                    outline=(0, 0, 0, 1), ow=4)


def token_pile(cr, x, y, k):
    """Momo's growing heap (k 0..1)."""
    n = int(6 + 60 * k)
    for j in range(n):
        u = (j * 0.618) % 1
        v = (j * 0.381) % 1
        rr = 120 * k ** 0.5 * (0.3 + 0.7 * v)
        ang = math.pi * (1.05 + 0.9 * u)
        px, py = x + rr * math.cos(ang) * 1.2, y + rr * math.sin(ang) * 0.45 - (1 - v) * 40 * k
        cr.save()
        cr.translate(px, py)
        cr.scale(1, 0.5)
        token(cr, 0, 0, 20)
        cr.restore()


def flying_tokens(cr, t, start, end, x0, y0, x1, y1, n=6):
    """Tokens arcing from (x0, y0) into Momo's pile at (x1, y1) between start and end."""
    if not (start <= t <= end):
        return
    for j in range(n):
        p = ((t - start) * 1.4 + j / n) % 1
        x = x0 + (x1 - x0) * p
        y = y0 + (y1 - y0) * p - math.sin(p * math.pi) * 240
        token(cr, x, y, 22, glint=0.5 * (1 - p))


def players(n):
    return ["PLAYERS", str(n)]


def palm(cr, t, x, y, s, has_token=0.0, close=0.0):
    """An open hand from below (Saki's), a token landing in it."""
    skin, shade = dma_art.SKIN[0], (0.86, 0.68, 0.6, 1)
    cr.save()
    cr.translate(x, y)
    cr.scale(s, s)
    A.toon(cr, lambda c: (c.save(), c.scale(1.0, 0.82), c.arc(0, 0, 150, 0, 2 * math.pi), c.restore()), skin, shade,
           (-8, -10), None, lw=5)                              # the palm
    for k, (ang, ln) in enumerate(((-2.45, 150), (-1.95, 190), (-1.57, 200), (-1.2, 185), (-0.45, 150))):
        bend = close * (0.5 if k < 4 else 0.3)
        cr.save()
        cr.rotate(ang + math.pi / 2 + (bend if k < 4 else -bend))
        A.toon(cr, lambda c, ln=ln: A.tk.tk_rrect(c, -26, -110 - ln * (1 - 0.35 * close), 52, ln, 26), skin, shade,
               (-4, -6), None, lw=4.5)
        cr.restore()
    cr.set_source_rgba(0.6, 0.4, 0.35, 0.5)                    # palm lines
    cr.set_line_width(3)
    cr.move_to(-90, -20)
    cr.curve_to(-40, 10, 30, 0, 90, -40)
    cr.move_to(-80, 30)
    cr.curve_to(-20, 40, 40, 30, 80, 10)
    cr.stroke()
    if has_token > 0:
        drop = (1 - has_token) * -260
        token(cr, 0, -10 + drop, 46, glint=1.0 if has_token >= 1 else 0.0)
    cr.restore()


def flash_white(cr, t, at, dur=0.4):
    if at <= t < at + dur:
        cr.set_source_rgba(1, 1, 1, 0.85 * (1 - (t - at) / dur))
        cr.paint()


# ------------------------------------------------------------------ motion-comic shots and effects
def has_shot(name):
    import os
    return A is dma_anime and os.path.exists(os.path.join(AN.ROOT, "assets/anime/dma/bg", name + ".png"))


def still(cr, t, s0, s1, name, z=(1.0, 1.1), a=(0.5, 0.5), drift=(0.0, 0.0), par=0.05, blur=0, fallback=None):
    """A painted shot (dma_shots.py) with a slow push; with figure layers, the figures push a little faster than the
    room behind them (parallax). Falls back to `fallback(cr)` when the painting doesn't exist."""
    import os
    if not has_shot(name):
        if fallback:
            fallback(cr)
        return
    k = seg(t, s0, s1)
    e = k * k * (3 - 2 * k) * 0.6 + k * 0.4
    zoom = z[0] + (z[1] - z[0]) * e
    ax, ay = a[0] + drift[0] * e, a[1] + drift[1] * e
    d = "assets/anime/dma/bg/"
    fg, fill = d + name + "_fg.png", d + name + "_fill.png"
    if par and not blur and os.path.exists(os.path.join(AN.ROOT, fg)):
        AN.paint_bg(cr, fill, ax=ax, ay=ay, zoom=zoom)
        AN.paint_bg(cr, fg, ax=ax, ay=ay, zoom=zoom * (1 + par * e))
    else:
        AN.paint_bg(cr, d + name + ".png", blur=blur, ax=ax, ay=ay, zoom=zoom)


def speed_lines(cr, t, k, cx=W / 2, cy=H * 0.42, col=(1, 1, 1), n=80, r0=None):
    """Anime focus lines (shuchusen) closing in on (cx, cy); redrawn on 2s like hand-drawn lines."""
    if k <= 0:
        return
    import random
    rnd = random.Random(int(AN.held(t) * 12))
    r0 = r0 or min(W, H) * 0.36
    R = math.hypot(W, H)
    cr.save()
    cr.set_source_rgba(*col[:3], 0.55 * k)
    for _ in range(n):
        a = rnd.uniform(0, 2 * math.pi)
        wd = rnd.uniform(0.003, 0.014)
        r = r0 * rnd.uniform(0.85, 1.5)
        cr.move_to(cx + math.cos(a) * r, cy + math.sin(a) * r)
        cr.line_to(cx + math.cos(a - wd) * R, cy + math.sin(a - wd) * R)
        cr.line_to(cx + math.cos(a + wd) * R, cy + math.sin(a + wd) * R)
        cr.close_path()
    cr.fill()
    cr.restore()


def impact(cr, t, at, dur=0.25, red=True):
    """An anime impact frame: for a few drawings the picture turns to hard black / white (and red), alternating."""
    if not (at <= t < at + dur):
        return
    import numpy as np
    s = cr.get_target()
    s.flush()
    w, h = s.get_width(), s.get_height()
    buf = np.ndarray((h, s.get_stride() // 4, 4), np.uint8, s.get_data())[:, :w]
    lum = buf[..., :3].astype(np.float32).mean(axis=2)
    ink = lum < np.percentile(lum, 55)
    phase = int((t - at) * 12) % 2
    if phase == 0:                                            # white paper, black ink
        v = np.where(ink, 0, 255).astype(np.uint8)
        buf[..., 0], buf[..., 1], buf[..., 2] = v, v, v
    else:                                                     # inverted, the ink red
        buf[..., 0] = np.where(ink, 40 if red else 255, 0)
        buf[..., 1] = np.where(ink, 30 if red else 255, 0)
        buf[..., 2] = np.where(ink, 255, 0)
    s.mark_dirty()


def dust(cr, t, k=1.0, col=(1, 1, 1)):
    """Specks floating in the light (held on 2s)."""
    if k <= 0:
        return
    tq = AN.held(t)
    for j in range(36):
        u = (j * 0.6180339 + 0.13) % 1
        v = (j * 0.4142135 + tq * (0.01 + 0.012 * (j % 3))) % 1
        x = W * u + 18 * math.sin(tq * 0.7 + j)
        y = H * (1 - v)
        cr.set_source_rgba(*col[:3], k * (0.2 + 0.3 * ((j * 7) % 5) / 5))
        cr.arc(x, y, 1.5 + (j % 3), 0, 2 * math.pi)
        cr.fill()


def chip_players(cr, t, n, red=False):
    """A small PLAYERS n chip under the status bar (for shots where the wall screen isn't in view)."""
    txt = f"PLAYERS {n}"
    w = A.text_width(cr, txt, 26, "Liberation Mono") + 36
    x, y = W - w - 16, 66
    A.tk.tk_rrect(cr, x, y, w, 40, 20)
    cr.set_source_rgba(*(RED[:3] if red else (0.03, 0.05, 0.06)), 0.92)
    cr.fill_preserve()
    cr.set_source_rgba(*CYAN[:3], 0.7)
    cr.set_line_width(2)
    cr.stroke()
    hud2d._text(cr, txt, x + w / 2, y + 28, 26, (1, 1, 1, 1), "Liberation Mono", "center")
