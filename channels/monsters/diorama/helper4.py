"""Episode 1 in diorama 2.5D (channels/monsters/DIORAMA_EP01.md), helper 4: the jelly-snail's two shots, in the flower
meadow at diorama.MAP["snail"], on the one island (seed 31). The same lengths and beats as the 3D shots
(ep01v2/helper4.py), so the mix stays in sync:

    S10a (56 frames; 44 in the cut) "Everything here was tiny." A close toy-world beat from the south, the snail's face
          turned up to the lens: the cute held pose, one slow bob, one blink (shut on frame 23, as in 3D). Locked, so
          it renders on 2s (characters on 2s; the pollen motes too).
    S11a (39 frames; 27 in the cut) "And every one of..." From above and behind the snail (from the north): its trail
          of burnt, ember-rimmed holes runs down the frame toward the lens and leads up to the snail, the pale cel
          smoke (S11a v3) rising off every hole. The smoke and the ember flicker are effects, so on 1s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama S10a OUT_DIR [--still N --scale 0.5]
    python channels/monsters/diorama/helper4.py S10a OUT_DIR out/monsters/diorama/shots     (mp4 + sheet)
"""
import math
import os
import subprocess
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")))
try:
    import bpy
    from mathutils import Vector
except ImportError:                                            # encode() runs outside Blender
    bpy = None

HANDLE = 12
LENS, BLUR = 100.0, 12.0


def _scene(trail):
    """The island (seed 31), the diorama light, and the snail at MAP["snail"] facing -Y (toward the default camera),
    with the meadow flowers cleared where it sits and where its trail has burned the grass."""
    from channels.monsters.mk import diorama, jellysnail
    diorama.setup()
    diorama.island(seed=31)
    x, y = diorama.MAP["snail"]
    rig = jellysnail.build((x, y, 0.0), trail=trail)
    _clear_flowers(rig)
    return rig


def _clear_flowers(rig):
    """Delete the meadow-flower dots under the snail and along its trail (burned away, and they would poke through)."""
    x0, y0 = rig["root"].location.x, rig["root"].location.y
    tr = rig.get("trail")
    pts = [(x0, y0 + 0.15 * k) for k in range(-8, 12)] + (list(tr["path"]) if tr else [])
    for o in list(bpy.data.objects):
        if o.type != "MESH" or not o.data.materials or not o.data.materials[0].name.startswith("mflower"):
            continue
        p = o.location
        if any(math.hypot(p.x - px, p.y - py) < 1.6 for px, py in pts):
            bpy.data.objects.remove(o, do_unlink=True)


def s10a():
    from channels.monsters.ep01v2.helper4 import _motes
    from channels.monsters.mk import anim, diorama, jellysnail
    frames = 44 + HANDLE
    rig = _scene(trail=False)
    jellysnail.hold(rig, 1, frames, "cute", bob=0.025, period=36, step=2)
    anim.blink(rig, 23)                                        # the 3D shot's blink frame
    anim.on_twos(rig["eyes"], 2)
    x, y = diorama.MAP["snail"]
    head = (x, y - 0.9, 1.2)
    # the snail is ~2 units against Kai's 8.7, so its close beat sits nearer than the brief's Kai distances (45-90)
    cam = diorama.camera("dio_s10a", head, dist=17.0, tilt=42.0, yaw=8.0, lens=LENS, blur=BLUR)
    motes = _motes((x, y - 1.2, 1.2), 1, frames, spread=(1.8, 1.4, 1.0))
    for m in motes:
        anim.on_twos([m], 2)
    return dict(frames=frames, step=2, subject=[rig["root"], *motes], camera=cam)


def s11a():
    from channels.monsters.ep01v2.helper4 import _cel_smoke, _ember_flicker, _hole_glow, _motes
    from channels.monsters.mk import diorama, jellysnail
    frames = 27 + HANDLE
    rig = _scene(trail=True)
    tr = rig["trail"]
    _cel_smoke(tr)
    # seen from the north (looking -Y) screen-right is world -X, so the smoke leans to +X: up and to the left, away
    # from the shell, as in S11a v3. Bigger and taller than in 3D, so the columns read from above
    jellysnail.smoke(tr, 1, strength=1.5, size=1.15, rise=1.7, lean=(0.45, 0.0))
    jellysnail.idle(rig, 1, frames, step=2)
    _ember_flicker(1, frames, lo=1.8, hi=2.8)
    _hole_glow(tr)
    x, y = diorama.MAP["snail"]
    mid = tr["holes"][2]
    target = ((x + mid[0]) / 2, (y + mid[1]) / 2 + 0.6, 0.3)  # between the snail and the middle of the trail
    cam = diorama.camera("dio_s11a", target, dist=24.0, tilt=56.0, yaw=180.0, lens=LENS, blur=BLUR)
    motes = _motes((mid[0], mid[1], 0.8), 1, frames, spread=(1.6, 2.0, 0.6), n=8, seed=11)
    return dict(frames=frames, step=1, subject=[rig["root"], tr["root"], *motes], camera=cam)


SHOTS = {"S10a": s10a, "S11a": s11a}


def encode(shot, frames_dir, out_dir):
    """frames_dir/0001.png... -> out_dir/<shot>.mp4 (x264 crf 12, no metadata or encoder tag) and <shot>_sheet.jpg
    (every 6th frame)."""
    from PIL import Image
    os.makedirs(out_dir, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "24", "-i", os.path.join(frames_dir, "%04d.png"),
                    "-c:v", "libx264", "-crf", "12", "-preset", "slow", "-pix_fmt", "yuv420p", "-map_metadata", "-1",
                    "-fflags", "+bitexact", "-flags:v", "+bitexact", "-x264-params", "no-info=1",
                    os.path.join(out_dir, f"{shot}.mp4")], check=True)
    n = len([f for f in os.listdir(frames_dir) if f[:4].isdigit() and f.endswith(".png")])
    ims = [Image.open(os.path.join(frames_dir, f"{f:04d}.png")) for f in range(1, n + 1, 6)]
    w, h = ims[0].size[0] // 3, ims[0].size[1] // 3
    cols = min(len(ims), 4)
    sheet = Image.new("RGB", (w * cols, h * -(-len(ims) // cols)), "white")
    for i, im in enumerate(ims):
        sheet.paste(im.resize((w, h)), ((i % cols) * w, (i // cols) * h))
    sheet.save(os.path.join(out_dir, f"{shot}_sheet.jpg"), quality=90)


if __name__ == "__main__" and bpy is None:
    encode(*sys.argv[1:4])
