"""heads.py demos (helper 10): the contact sheet and the Churchill portrait clip.

    python channels/ww2/kit/heads_demo.py sheet      -> out/ww2/style/heads_sheet.png
    python channels/ww2/kit/heads_demo.py churchill  -> out/ww2/style/portrait_churchill.mp4 (6 s, line 53)
"""
import math
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
from channels.ww2.kit import core, heads  # noqa: E402
from channels.ww2.kit.core import (FPS, H, W, LABEL, SLAB, STENCIL, cairo, col, date_stamp, paper,  # noqa: E402
                                   print_finish, push_in, rays, text)

OUT = os.path.join(core.ROOT, "out", "ww2", "style")


def _ffmpeg_here():
    try:
        return core.ffmpeg()
    except Exception:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()


core.ffmpeg = _ffmpeg_here if not os.path.exists("/home/user/.venv-main/bin/python") else core.ffmpeg


def sheet(path=os.path.join(OUT, "heads_sheet.png")):
    SW, SH = 2600, 1800
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, SW, SH)
    cr = cairo.Context(surf)
    cr.set_source_rgba(*col("paper"))
    cr.paint()
    text(cr, "HEADS & LEADER PORTRAITS  (heads.py)", 60, 80, 54, font=SLAB, align="left")
    # row 1: the nine leaders as chest-up portraits on rays / plain fields
    n = len(heads.LEADERS)
    cw = (SW - 80) / n
    for i, who in enumerate(heads.LEADERS):
        x = 40 + cw * (i + 0.5)
        cr.save()
        cr.rectangle(40 + cw * i + 6, 110, cw - 12, 560)
        cr.clip()
        rays_col = "khaki" if heads.OUTFIT[who][0] in ("axis", "axis_it", "axis_jp") else "gold"
        heads.portrait(cr, 1.3 + i * 0.37, who, x, 690, height=520, expr="determined", turn=0.45, bg="rays",
                       ray_col=rays_col, idle=True, seed=i + 2)
        cr.restore()
        cr.rectangle(40 + cw * i + 6, 110, cw - 12, 560)
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(4)
        cr.stroke()
        text(cr, heads.NAMES[who], x, 708, 22, font=LABEL)
    # row 2: each leader small (figure size, R 31) in profile, three-quarter and front
    text(cr, "SMALL (figure size): profile / three-quarter / front", 60, 790, 30, font=STENCIL, align="left")
    for i, who in enumerate(heads.LEADERS):
        x0 = 40 + cw * i + cw * 0.18
        for j, turn in enumerate((0.0, 0.6, 1.0)):
            cr.save()
            cr.translate(x0 + j * cw * 0.32, 880)
            spec = dict(R=31.0, leader=who, nation=None, civilian=None, headgear=None, side=None, turn=turn,
                        flat=False, tone=None, seed=i, mouth_prop=None, key_w=5.0)
            heads.draw_head(cr, spec, {"name": "neutral"}, 1.0 + j)
            cr.restore()
    # row 3: the expression range (a generic head, three-quarter, big)
    text(cr, "EXPRESSIONS", 60, 1015, 30, font=STENCIL, align="left")
    names = list(heads.EXPRESSIONS)
    ew = (SW - 80) / len(names)
    for i, nm in enumerate(names):
        x = 40 + ew * (i + 0.5)
        cr.save()
        cr.translate(x - 10, 1170)
        spec = dict(R=82.0, leader=None, nation=None, civilian=None, headgear=None, side=None, turn=0.55, flat=False,
                    tone=None, seed=4, mouth_prop=None, key_w=6.0)
        heads.draw_head(cr, spec, {"name": nm}, 2.0)
        cr.restore()
        text(cr, nm.upper(), x, 1072, 26, font=LABEL)
    # row 4: soldiers and civilians under helper 1's helmets and caps, plus a blink and a crowd silhouette
    text(cr, "SOLDIERS & CIVILIANS (helper 1's headgear)", 60, 1420, 30, font=STENCIL, align="left")
    kinds = [("germany", None), ("britain", None), ("usa", None), ("soviet", None), ("france", None),
             ("japan", None), ("italy", None), (None, "flatcap"), (None, "hat"), (None, "scarf")]
    kw_ = (SW - 80) / (len(kinds) + 1)
    for i, (nat, civ) in enumerate(kinds):
        x = 40 + kw_ * (i + 0.5)
        cr.save()
        cr.translate(x, 1590)
        spec = dict(R=56.0, leader=None, nation=nat, civilian=civ, headgear=nat or civ, side=None,
                    turn=(0.0, 0.6, 0.3, 0.8, 0.0, 0.6, 0.4, 0.7, 0.2, 0.9)[i], flat=False, tone=None, seed=10 + i,
                    mouth_prop=None, key_w=5.0)
        heads.draw_head(cr, spec, {"name": ("determined", "worried", "neutral", "angry", "shocked", "determined",
                                            "smug", "smiling", "sad", "neutral")[i]}, 3.0)
        cr.restore()
        text(cr, (nat or civ).upper(), x, 1730, 22, font=LABEL)
    cr.save()
    cr.translate(40 + kw_ * (len(kinds) + 0.5), 1590)
    spec = dict(R=56.0, leader=None, nation="britain", civilian=None, headgear="britain", side=None, turn=0.0,
                flat=True, tone=col("ink_soft"), seed=1, mouth_prop=None, key_w=5.0)
    heads.draw_head(cr, spec, {}, 0.0)
    cr.restore()
    text(cr, "CROWD (FLAT)", 40 + kw_ * (len(kinds) + 0.5), 1730, 22, font=LABEL)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    surf.write_to_png(path)
    return path


def churchill(path=os.path.join(OUT, "portrait_churchill.mp4"), dur=6.0, still=None):
    """Line 53, '...refuses to make peace': Churchill on blue-grey rays, a slow push-in, then a firm head shake."""
    def draw(cr, t):
        paper(cr)
        z = push_in(t, 0.0, dur, 1.0, 1.12)
        cr.save()
        core.camera(cr, z, W / 2, H * 0.52)
        rays(cr, t, W / 2, H * 0.36, n=28, color="allies", alpha=0.16)
        sh = 0.0
        if 3.2 <= t <= 4.9:                                      # a firm shake: three swings, settling
            u = (t - 3.2) / 1.7
            sh = 0.32 * math.sin(u * 3 * 2 * math.pi) * (1 - u) ** 0.8
        heads.portrait(cr, t, "churchill", W / 2, H + 40, height=980, expr="determined", turn=0.42, shake=sh,
                       seed=5, nod=0.0)
        cr.restore()
        date_stamp(cr, t, "JUNE 1940")
        print_finish(cr, t)
    if still is not None:
        return core.render_clip(draw, dur, path.replace(".mp4", f"_t{still:.1f}.png"), still=still)
    return core.render_clip(draw, dur, path)


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "sheet"
    if what == "sheet":
        print(sheet())
    elif what == "churchill":
        print(churchill())
    elif what == "still":
        print(churchill(still=float(sys.argv[2])))
