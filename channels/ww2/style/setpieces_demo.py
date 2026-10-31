import os, sys; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from channels.ww2.kit.core import *
from channels.ww2.kit import setpieces as sp
T = float(sys.argv[2]) if len(sys.argv) > 2 else 1.3
SCENES = [
    ("squad_advance", lambda cr, t: (rays(cr, t, W/2, 900, color="khaki", alpha=0.3), sp.squad_advance(cr, t, nation="usa", x0=150, ground=900))),
    ("march_column", lambda cr, t: sp.march_column(cr, t, nation="germany", ground=1000, horizon=560)),
    ("duck_under_fire", lambda cr, t: sp.duck_under_fire(cr, t, nation="britain", x=1000, ground=900)),
    ("cheering_crowd", lambda cr, t: sp.cheering_crowd(cr, t, 0, W, 600, 1010)),
    ("waiting_crowd", lambda cr, t: sp.waiting_crowd(cr, t, 0, W, 560, 1000, nation="britain")),
    ("radio_family", lambda cr, t: sp.radio_family(cr, t, x=960, ground=940, scale=0.9)),
    ("shivering_soldiers", lambda cr, t: sp.shivering_soldiers(cr, t, nation="germany", x=960, ground=940)),
    ("prisoner_line", lambda cr, t: (cr.rectangle(0, 480, W, H), cr.set_source_rgba(*col("snow")), cr.fill(), sp.prisoner_line(cr, t, nation="germany", ground=1010, horizon=500))),
]
def frame(fn):
    def draw(cr, t):
        paper(cr)
        fn(cr, t)
        print_finish(cr, t)
    return draw
from PIL import Image
out = []
for name, fn in SCENES:
    p = os.path.join(sys.argv[1], name + ".png")
    render_clip(frame(fn), 1, p, still=T)
    out.append(Image.open(p).convert("RGB").resize((960, 540)))
sheet = Image.new("RGB", (1920, 2160))
for i, im in enumerate(out):
    sheet.paste(im, ((i % 2) * 960, (i // 2) * 540))
sheet.save(os.path.join(sys.argv[1], "setpieces_sheet.jpg"), quality=88)
