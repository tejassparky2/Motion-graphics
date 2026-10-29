"""Choreography: the bike path, the rider's acting, and five camera shots."""
import math

import bpy
import numpy as np
from mathutils import Vector

from . import environment
from .anim import bake, key_track
from .util import empty, smoothstep

DURATION = 20.0
FPS = 24

BIKE_PATH = dict(coast=(9.2, 13.4), v0=3.05, x0=0.0, y0=0.50)
SUN = dict(sun_elev_deg=3.6, sun_az_deg=-40.0)

# (time, (yaw, pitch, tilt)) yaw + = look left, pitch + = nose down, tilt + = cock head right
HEAD_KEYS = [
    (0.0, (0.00, 0.00, 0.00)), (1.6, (0.06, 0.02, 0.00)), (3.2, (-0.05, -0.02, 0.02)),
    (5.6, (0.00, 0.00, 0.00)), (6.3, (0.06, 0.30, -0.04)), (7.1, (0.06, 0.30, -0.04)),
    (7.8, (-0.05, 0.00, 0.00)), (8.9, (-0.10, 0.02, 0.00)), (9.6, (-0.42, 0.06, 0.16)),
    (10.9, (-0.40, 0.04, 0.20)), (11.4, (-0.36, 0.08, 0.10)), (12.3, (-0.05, 0.00, 0.00)),
    (14.0, (0.02, -0.02, 0.00)), (14.7, (-0.22, 0.04, 0.10)), (15.6, (-0.20, 0.03, 0.08)), (16.3, (0.0, 0.0, 0.0)),
    (17.5, (0.00, -0.04, 0.00)), (20.0, (0.00, -0.02, 0.00)),
]
JAW_KEYS = [(0.0, 0.0), (10.05, 0.0), (10.4, 0.11), (10.75, 0.02), (11.0, 0.0), (14.6, 0.0),
            (14.85, 0.05), (15.1, 0.0), (20.0, 0.0)]

PERCHED_GULLS = [((21.0, 2.46, 3.57), 2.4), ((57.6, -2.46, 3.57), -1.2), ((86.4, 2.46, 1.15), 1.8)]
FAR_PELICANS = dict(n=5, start=(150.0, -128.0, 4.5), vel=(0.0, 7.2, 0.0))
SIGN = dict(loc=(8.0, -1.72, 0.0), rot_z=0.0)

SHOTS = [  # name, start s, end s
    ('approach', 0.0, 4.0),
    ('side', 4.0, 8.0),
    ('front', 8.0, 12.0),
    ('profile', 12.0, 16.0),
    ('sunset', 16.0, 20.0),
]
# sun cheats per shot (elevation, azimuth)
SUN_PER_SHOT = {'approach': (3.6, -40.0), 'side': (3.6, -40.0), 'front': (3.4, -95.0),
                'profile': (4.0, -108.0), 'sunset': (2.4, -7.0)}


def _frames(T, a, b):
    return (T.t >= a - 1e-9) & (T.t <= b + 1e-9)


def _cam(name, coll, lens, fstop, focus_obj):
    cd = bpy.data.cameras.new(name)
    cd.lens = lens
    cd.sensor_width = 36.0
    cd.dof.use_dof = True
    cd.dof.aperture_fstop = fstop
    cd.dof.focus_object = focus_obj
    cd.dof.aperture_blades = 7
    cd.dof.aperture_rotation = math.radians(12)
    cd.clip_start = 0.05
    cd.clip_end = 30000
    cam = bpy.data.objects.new(name, cd)
    coll.objects.link(cam)
    tgt = empty(f"{name}.target", coll, size=0.1)
    tc = cam.constraints.new('TRACK_TO')
    tc.target = tgt
    tc.track_axis = 'TRACK_NEGATIVE_Z'
    tc.up_axis = 'UP_Y'
    return cam, tgt


def setup(scene, T, bike, pel, rg, m, sun, sky):
    from .util import collection
    coll = collection("Cameras")
    t = T.at_frames(T.t)
    fr = T.frames
    bx = T.at_frames(m['x'])
    by = T.at_frames(m['y'])
    # a focus helper riding with the pelican's head
    head_focus = empty("FocusHead", coll, size=0.05)
    head_focus.parent = bike['frame']
    head_focus.location = (0.697, 0.0, 1.09)
    scene.frame_set(scene.frame_start)
    from .rig import _bone_parent
    _bone_parent(head_focus, rg['rig'], 'head')
    body_focus = empty("FocusBody", coll, size=0.05)
    body_focus.parent = bike['frame']
    body_focus.location = (0.45, 0.0, 0.70)

    cams = {}

    def shot_camera(name, lens, fstop, focus, pos_fn, tgt_fn, a, b):
        cam, tgt = _cam(f"Cam.{name}", coll, lens, fstop, focus)
        sel = (t >= a - 0.5) & (t <= b + 0.5)
        tt = np.clip(t, a - 0.5, b + 0.5)
        P = np.array([pos_fn(x) for x in tt])
        Q = np.array([tgt_fn(x) for x in tt])
        for k in range(3):
            bake(cam, 'location', k, fr, P[:, k])
            bake(tgt, 'location', k, fr, Q[:, k])
        cams[name] = cam
        return cam

    def bike_at(x):
        return np.interp(x, t, bx), np.interp(x, t, by)

    # 1. approach: long lens, low on the deck ahead of the bike
    def p1(x):
        u = smoothstep(0, 4, x)
        return (24.5 - 1.2 * u, 0.75 + 0.10 * u, 0.42 + 0.12 * u)

    def q1(x):
        X, Y = bike_at(x)
        return (X + 0.45, Y, 0.80)
    shot_camera('approach', 105, 2.2, body_focus, p1, q1, 0.0, 4.0)

    # 2. side tracking on the drive side, drifting up from the drivetrain to the rider
    def p2(x):
        X, Y = bike_at(x)
        u = smoothstep(4.0, 8.0, x)
        return (X + 0.42 + 0.06 * u, Y - 2.25, 0.50 + 0.30 * u)

    def q2(x):
        X, Y = bike_at(x)
        u = smoothstep(4.0, 8.0, x)
        return (X + 0.44, Y, 0.56 + 0.16 * u)
    shot_camera('side', 32, 4.0, body_focus, p2, q2, 4.0, 8.0)

    # 3. front three-quarter, camera retreating ahead of the bike; the bird looks at us
    def p3(x):
        X, Y = bike_at(x)
        u = smoothstep(8.0, 12.0, x)
        return (X + 2.35 - 0.35 * u, Y - 1.05 - 0.10 * u, 1.02 + 0.06 * u)

    def q3(x):
        X, Y = bike_at(x)
        u = smoothstep(8.0, 12.0, x)
        return (X + 0.55 + 0.1 * u, Y + 0.02, 0.86 + 0.10 * u)
    shot_camera('front', 50, 2.2, head_focus, p3, q3, 8.0, 12.0)

    # 4. close-up of the head, front-right three-quarter, warm side key light
    def p4(x):
        X, Y = bike_at(x)
        u = smoothstep(12.0, 16.0, x)
        return (X + 1.62 - 0.10 * u, Y - 0.80 - 0.04 * u, 1.14 + 0.02 * u)

    def q4(x):
        X, Y = bike_at(x)
        return (X + 0.80, Y + 0.02, 1.04)
    shot_camera('profile', 70, 2.4, head_focus, p4, q4, 12.0, 16.0)

    # 5. into the sunset: low behind, slow crane up as it rides away
    def p5(x):
        u = smoothstep(16.0, 20.0, x)
        return (39.5 + 1.5 * u, 0.25 + 0.1 * u, 0.40 + 1.2 * u)

    def q5(x):
        X, Y = bike_at(x)
        u = smoothstep(16.0, 20.0, x)
        return (X + 6.0 + 20 * u, Y * 0.6, 0.85 + 0.6 * u)
    shot_camera('sunset', 45, 4.0, body_focus, p5, q5, 16.0, 20.0)

    # timeline markers switch cameras; sun cheats are stepped per shot
    scene.timeline_markers.clear()
    sl = sun.data
    for name, a, b in SHOTS:
        f0 = int(round(a * T.fps)) + T.start
        mk = scene.timeline_markers.new(name, frame=f0)
        mk.camera = cams[name]
        el, az = SUN_PER_SHOT[name]
        environment.set_sun(sun, sky, el, az)
        sun.keyframe_insert('rotation_euler', frame=f0)
        sky.keyframe_insert('sun_elevation', frame=f0)
        sky.keyframe_insert('sun_rotation', frame=f0)
    for obj in (sun,):
        for fc in obj.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = 'CONSTANT'
    wt = scene.world.node_tree
    if wt.animation_data and wt.animation_data.action:
        for fc in wt.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = 'CONSTANT'
    scene.camera = cams['approach']
    # update the cloud/sun-disc direction used by the world shader per shot
    _key_world_sun(scene, T)
    return cams


def _key_world_sun(scene, T):
    """The world shader's sun-direction vector (dot product node) is keyed per shot."""
    nt = scene.world.node_tree
    dots = [n for n in nt.nodes if n.bl_idname == 'ShaderNodeVectorMath' and n.operation == 'DOT_PRODUCT']
    if not dots:
        return
    dot = dots[0]
    for name, a, b in SHOTS:
        el, az = SUN_PER_SHOT[name]
        d = (math.cos(math.radians(el)) * math.cos(math.radians(az)),
             math.cos(math.radians(el)) * math.sin(math.radians(az)),
             math.sin(math.radians(el)))
        f0 = int(round(a * T.fps)) + T.start
        dot.inputs[1].default_value = d
        dot.inputs[1].keyframe_insert('default_value', frame=f0)
    if nt.animation_data and nt.animation_data.action:
        for fc in nt.animation_data.action.fcurves:
            for kp in fc.keyframe_points:
                kp.interpolation = 'CONSTANT'
