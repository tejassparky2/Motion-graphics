"""Episode 1 in diorama 2.5D (channels/monsters/DIORAMA_EP01.md), helper 9: S06, S08 (the lab dollhouse) and S12 (the
crawl to the pond on the island). Same frame counts and beats as the 3D shots (channels/monsters/ep01v2/helper9.py).

    S12 "I was so thirsty." (47 frames): Kai crawls on hands and knees up the trodden clearing toward the pond,
        panting, his tired face turned up to the high camera; the pond glints in the foreground ahead of him.
        Locked camera; Kai and the glint on 2s.

    blender -b -y -P channels/monsters/render_shot.py -- diorama S12 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import math

import bpy

from channels.monsters.ep01v2 import helper9 as h9              # the crawl, the face mixer and the glint
from channels.monsters.mk import diorama, hero

RENDER = h9.RENDER                                               # same render frames as the 3D shots
LENS, BLUR = 100.0, 12.0


def _cut_front(isl, cam, target, keep=0.8):
    """The dollhouse cutaway: hide the island trees standing between a low camera and its subject (closer to the
    camera, horizontally, than `keep` x the subject), so no canopy fills the foreground. Out of frame otherwise."""
    cx, cy = cam.location.x, cam.location.y
    reach = keep * math.hypot(target[0] - cx, target[1] - cy)
    for (x, y, *_), objs in zip(isl["spots"], isl["trees"]):
        if objs and math.hypot(x - cx, y - cy) < reach:
            for o in objs:
                o.hide_render = True


def s12():
    diorama.setup()
    isl = diorama.island(seed=31)
    n = RENDER["S12"]
    px, py = diorama.MAP["pond"]
    # up the clearing from the path (south) toward the pond: heading pi = facing +Y (north); look_up 3 tips his
    # face back toward the high camera so it reads under the cap's visor
    rig = h9._crawling_kai((px + 0.5, -12.0, 0.0), math.pi, 1, n, 3.0, period=16, look_up=3.0, step=2)
    hero.line_width(rig, 0.0025)
    for f in range(1, n + 3, 2):                                 # panting on 2s: open / half-open
        wide = (f // 2) % 2 == 0
        h9._face_mix(rig, {"face_sad": 0.7, "eye_zitome": 0.75, "mouse_open": 1.0 if wide else 0.5,
                           "lip_a": 0.6 if wide else 0.3}, f)
    # from the north, high and a little to the side: he crawls toward the lens, the pond between him and us
    cam = diorama.camera("cam_s12", (px + 0.5, -8.0, 2.5), dist=55.0, tilt=40.0, yaw=165.0, lens=LENS, blur=BLUR)
    cam.data.shift_x, cam.data.shift_y = 0.06, -0.08             # left of the Shorts rail (x < 560), above y 960
    _cut_front(isl, cam, (px + 0.5, -8.0))
    h9._glint((px + 1.2, py - 1.4, 0.12), cam, 2, n, size=0.6, every=10, hold=2)
    return dict(frames=n, step=2, subject=[rig["arm"]] + list(rig.get("cap", [])))


SHOTS = {"S12": s12}
