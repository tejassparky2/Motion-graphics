"""Compositor test (channels/monsters/comp.py): a 3-shot demo built from the snap test frames plus their subject pass.

    blender -b -P channels/monsters/test_comp_frames.py -- build/monsters/comp_test/frames 360 640 4 21 64
    FPS=24 python channels/monsters/test_comp.py

1. "intro": the creature idles (hook text, WILD tag, ambient sparkles).
2. "rewind": a blob wipe opens on shot 1's frames running backwards under the glitch.
3. "snap": a hard cut; the subject-pass impact frame on the snap (2 frames), then the creature freezes over a red
   burst while the burst keeps moving, then the shot carries on.
A status bar carries across all three (episode time) and takes a hit on the snap; a caption sits in its band.
Writes the frames to build/monsters/comp_test/out (not in git) and four stills to out/monsters/tests/comp_*.png;
checks the Source operations and that the layout check catches a menu placed in the caption band and right rail.
"""
import os
import sys

os.environ.setdefault("FPS", "24")
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)

import cv2  # noqa: E402

from motion.engine import W, cairo  # noqa: E402
from motion.polish import text_path  # noqa: E402
from channels.monsters import comp, fx2d, fx2d_extra  # noqa: E402

FRAMES = os.path.join(ROOT, "build/monsters/comp_test/frames")
OUT = os.path.join(ROOT, "build/monsters/comp_test/out")
TESTS = os.path.join(ROOT, "out/monsters/tests")
FIRST = 21                         # the first Blender frame rendered (frames 21-64 around the snap)
SNAP = (44 - FIRST) / 24           # the snap is Blender frame 44: its time in the folder


def caption(cr, t, text, start, end):
    """A stand-in caption in the caption band (the real ones come from the episode timeline)."""
    if not start <= t < end:
        return
    text_path(cr, text, W / 2, 905, 50, "Fredoka", "center")
    cr.set_source_rgba(0.07, 0.06, 0.12, 1)
    cr.set_line_width(9)
    cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.stroke()
    text_path(cr, text, W / 2, 905, 50, "Fredoka", "center")
    cr.set_source_rgb(1, 1, 1)
    cr.fill()


def check_source_ops(src):
    n = len(src.map)
    assert src.seq(0.5, 1.0).map == list(range(12, 24))
    assert src.reverse().map[0] == n - 1
    h = src.hold(0.5, 1.0)
    assert len(h.map) == n and set(h.map[12:24]) == {12}
    hi = src.hold(0.5, 1.0, insert=True)
    assert len(hi.map) == n + 12 and hi.map[24] == 12
    r = src.seq(0, 1.0).retime(3)
    assert len(r.map) == 72 and r.map[:6] == [0, 0, 0, 1, 1, 1]
    assert len(src.fit(1.66).map) == 40
    print("OK  Source operations (seq, reverse, hold, hold insert, retime, fit)")


def check_layout_catches_bad_menu(src):
    bad = comp.Shot(src.seq(0, 0.5), 0.5, [(fx2d.choice_menu, dict(start=0.0, y=748))], name="menu at y=748")
    good = comp.Shot(src.seq(0, 0.5), 0.5, [(fx2d.choice_menu, dict(start=0.0, y=560))], name="menu at y=560")
    rb = comp.render([bad], OUT + "_layout", write=False, verbose=False)["layout"]
    rg = comp.render([good], OUT + "_layout", write=False, verbose=False)["layout"]
    print(f"{'OK ' if rb else 'BAD'} layout check flags fx2d.choice_menu at its default y=748: {rb}")
    print(f"{'OK ' if not rg else 'BAD'} layout check passes the menu at y=560: {rg}")
    return bool(rb) and not rg


def main():
    if not os.path.isdir(os.path.join(FRAMES, "subject")):
        sys.exit("render the frames first: blender -b -P channels/monsters/test_comp_frames.py -- " + FRAMES)
    src = comp.Source(FRAMES)
    check_source_ops(src)
    ok = check_layout_catches_bad_menu(src)

    intro = comp.Shot(src.seq(0, 0.9), 0.9, [
        (fx2d_extra.ambient, dict(start=0.0, keep_clear=(330, 600, 160))),
        (fx2d.hook_text, dict(start=0.0, end=0.8, lines=("IT ERASED", "A FOREST"), red=("ERASED",), y=300)),
        (fx2d.creature_tag, dict(start=0.0, name="???", threat=5)),
    ], name="intro")
    rewind = comp.glitch_rewind(src.seq(0, 0.9), 1.0, trans=comp.Wipe("blob", 0.45))
    t_snap = SNAP - 0.75                                            # the snap in shot 3's local time
    hold0, hold1 = t_snap + 2 / 24, t_snap + 2 / 24 + 0.8
    snap = comp.Shot(src.seq(0.75).hold(hold0, hold1, insert=True), src.seq(0.75).duration + 0.8, [
        (comp.impact, dict(start=t_snap, frames=2)),
        (comp.backdrop, dict(start=hold0, end=hold1 - 1 / 24, fn=fx2d_extra.burst_bg,
                             args=dict(style="red", cy=600))),
        (fx2d.shockwave, dict(start=hold0, x=330, y=620, r=330)),
    ], name="snap")
    shots = [intro, rewind, snap]
    snap_global = intro.dur + rewind.dur + t_snap
    rep = comp.render(shots, OUT, overlays=[
        (fx2d.status_bar, dict(start=0.0, hits=[(snap_global, 0.15)])),
        (caption, dict(text="This cute little thing", start=0.0, end=0.9), "caption"),
        (caption, dict(text="Snap.", start=snap_global, end=snap_global + 1.0), "caption"),
    ])
    ok &= not rep["layout"]
    print(f"{'OK ' if not rep['layout'] else 'BAD'} layout of the demo: {rep['layout'] or 'clean'}")
    print("cues:", sorted({(round(a, 2), n) for a, n, _ in rep["events"]}))

    f_rewind = int(round(intro.dur * 24))
    f_snap = f_rewind + int(round(rewind.dur * 24)) + int(round(t_snap * 24))
    stills = {"wipe": f_rewind + 5, "glitch": f_rewind + 16, "impact": f_snap, "burst": f_snap + 10}
    os.makedirs(TESTS, exist_ok=True)
    for name, g in stills.items():
        img = cv2.imread(os.path.join(OUT, f"{g + 1:05d}.png"))
        path = os.path.join(TESTS, f"comp_{name}.png")
        cv2.imwrite(path, img, [cv2.IMWRITE_PNG_COMPRESSION, 9])
        print(f"wrote {path} (frame {g + 1}, {os.path.getsize(path) / 1e6:.2f} MB)")
    print(f"{rep['frames']} frames, {rep['ms_per_frame']:.0f} ms per frame")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
