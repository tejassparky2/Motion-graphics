"""WW2 Episode 1 style frame: the map engine on script lines 30-38 (8 s). Europe, August to September 1939: the
camera pushes in on Poland, the secret line splits it under a SECRET stamp, grey arrows sweep in from Germany and
East Prussia, then red arrows from the east, and Poland floods grey and red. The date tag goes AUG 1939 -> SEPT 1939.

    /home/user/.venv-main/bin/python channels/ww2/style/map_1939.py [--still 5.6 out.png]

Sound cues: secret line scratch 1.0; stamp thunk 2.3; date flip 3.1; guns at Danzig 3.3; tank rumble 3.4-5.6;
red arrows 5.4; flood swells 4.5 and 6.2.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from channels.ww2.kit.core import ROOT, date_stamp, paper, render_clip  # noqa: E402
from channels.ww2.kit.maps import SPLIT_1939, Map  # noqa: E402

DUR = 8.0
m = Map("europe")
m.camera_key(0.0, (16.5, 51.0), 1.15)
m.camera_key(3.4, (20.6, 52.1), 2.55)
m.camera_key(DUR, (21.2, 52.1), 2.75)                     # the slow push-in keeps going
m.label("GERMANY", 0.2, lonlat=(10.6, 51.2), size=46)
m.label("SOVIET UNION", 0.2, lonlat=(30.5, 54.6), size=46)
m.label("POLAND", 0.5, lonlat=(18.7, 51.35), size=50)
m.label("EAST PRUSSIA", 0.8, lonlat=(20.9, 54.35), size=30, t_out=3.0)
m.secret_line(SPLIT_1939, 1.0, 2.4)                      # stays: the new dividing line
m.stamp("SECRET", (23.6, 53.05), 2.3, t_out=4.0, size=64)
m.city("Warsaw", 3.0)
m.city("Danzig", 3.3, dy=-16)
GREY = "germany"
m.arrow([(14.9, 53.3), (17.0, 53.0), (19.4, 52.6)], GREY, 3.4, 4.9, hold=6.6)              # from Pomerania
m.arrow([(20.6, 54.0), (20.9, 53.3), (21.0, 52.5)], GREY, 3.6, 5.0, hold=6.6)              # from East Prussia
m.arrow([(17.6, 50.6), (19.0, 50.6), (20.6, 51.3)], GREY, 3.8, 5.2, hold=6.6)              # from Silesia
m.side("poland_w", 4.4, GREY, origin=(16.4, 52.0), dur=1.6)
m.arrow([(28.4, 53.4), (26.6, 53.1), (24.5, 52.9)], "soviet", 5.3, 6.4, hold=7.6)          # from the east
m.arrow([(27.8, 50.6), (25.9, 50.0), (24.3, 49.9)], "soviet", 5.5, 6.6, hold=7.6)
m.side("poland_e", 6.0, "soviet", origin=(27.0, 51.6), dur=1.5)


def draw(cr, t):
    paper(cr)
    m.draw(cr, t)
    if t < 3.1:
        date_stamp(cr, t, "AUG 1939", start=0.0)
    else:
        date_stamp(cr, t, "SEPT 1939", start=3.1)


if __name__ == "__main__":
    out = os.path.join(ROOT, "out", "ww2", "style", "map_1939.mp4")
    if "--still" in sys.argv:
        i = sys.argv.index("--still")
        render_clip(draw, DUR, sys.argv[i + 2], still=float(sys.argv[i + 1]))
    else:
        render_clip(draw, DUR, out)
