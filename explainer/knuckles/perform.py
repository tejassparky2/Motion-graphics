"""The character's performance and the room cameras."""
import math

import bpy
from mathutils import Matrix, Vector

from xb import anim, posing
from xb.anim import key_bone, key_fingers, key_hand, key_loc
import shots

FIST_W = Vector((-0.05, -0.30, 1.22))
FIST_F = Vector((0.3, -0.9, 0.15))
FIST_N = Vector((1.0, 0.3, 0.0))
SIDE_L = (Vector((0.25, -0.10, 0.93)), Vector((0.05, -0.25, -1.0)), Vector((-1.0, 0.0, 0.0)))
OPEN_R = (Vector((-0.05, -0.40, 1.27)), Vector((0.12, -0.99, -0.06)), Vector((0.05, 0.1, -1.0)))
LOW_R = (Vector((-0.24, -0.12, 0.95)), Vector((-0.05, -0.25, -1.0)), Vector((1.0, 0.0, 0.0)))


def _contact(press, dw=(0, 0, 0), extra_f=None):
    wR = FIST_W + Vector(dw)
    (wR, fR, nR), (wL, fL, nL) = posing.fist_in_palm(wR, extra_f or FIST_F, FIST_N, press=press)
    return (wR, fR, nR), (wL, fL, nL)


def hands(rig, tR, tL):
    R = lambda t, p: key_hand(rig, 'R', tR, t, *p)   # noqa: E731
    L = lambda t, p: key_hand(rig, 'L', tL, t, *p)   # noqa: E731

    def crack_sequence(t0, crack_t, success):
        """Left palm approaches, wraps the fist, winds up and pushes."""
        r, l = _contact(0.03)
        appr = (l[0] + Vector((0.06, -0.06, -0.04)), l[1], l[2])
        R(t0, r)
        L(t0, appr)
        key_fingers(rig, 'R', t0, 'fist')
        key_fingers(rig, 'L', t0, 'relaxed', spread=0.4)
        r, l = _contact(0.034)
        R(t0 + 0.5, r)
        L(t0 + 0.5, l)
        key_fingers(rig, 'L', t0 + 0.45, 'cup')
        r, l = _contact(0.028, dw=(0.0, 0.0, 0.005))
        R(t0 + 0.9, r)
        L(t0 + 0.9, l)
        # small re-grip while waiting
        r, l = _contact(0.027, dw=(0.004, 0.004, 0.0))
        R(crack_t - 0.75, r)
        L(crack_t - 0.75, l)
        # wind up: pull in toward the chest
        r, l = _contact(0.027, dw=(0.0, 0.02, 0.006))
        R(crack_t - 0.25, r)
        L(crack_t - 0.25, l)
        key_fingers(rig, 'R', crack_t - 0.25, 'fist')
        # push: the left palm drives into the knuckles
        r, l = _contact(0.012, dw=(0.0, 0.005, 0.0))
        R(crack_t, r)
        L(crack_t, l)
        key_fingers(rig, 'R', crack_t, 'tight')
        if success:
            r, l = _contact(0.012, dw=(0.0, -0.02, -0.012))   # jolt as the joints give
            R(crack_t + 0.06, r)
            L(crack_t + 0.06, l)
            r, l = _contact(0.02, dw=(0.0, -0.01, -0.004))
            R(crack_t + 0.22, r)
            L(crack_t + 0.22, l)
            key_fingers(rig, 'R', crack_t + 0.22, 'fist')
        else:
            for i, dt in enumerate((0.08, 0.16, 0.24, 0.32)):   # straining tremor, nothing gives
                r, l = _contact(0.010 + 0.002 * (i % 2), dw=(0.003 * (-1) ** i, 0.004, 0.0))
                R(crack_t + dt, r)
                L(crack_t + dt, l)
            r, l = _contact(0.03)
            R(crack_t + 0.6, r)
            L(crack_t + 0.6, l)
            key_fingers(rig, 'R', crack_t + 0.6, 'fist')

    # ---- shot 1: the first crack ----
    crack_sequence(0.0, shots.CRACK_T, True)
    r, l = _contact(0.02, dw=(0.0, -0.01, -0.004))
    R(3.0, r)
    L(3.0, l)
    key_fingers(rig, 'L', 3.0, 'cup')
    key_fingers(rig, 'R', 3.0, 'fist')
    L(3.45, SIDE_L)
    key_fingers(rig, 'L', 3.45, 'relaxed')
    R(3.5, OPEN_R)
    key_fingers(rig, 'R', 3.45, 'spread', spread=0.8)
    # ---- shot 2: open hand under x-ray, fingers flex gently ----
    w, f, n = OPEN_R
    R(4.4, (w + Vector((0.005, -0.005, 0.004)), f, n))
    key_fingers(rig, 'R', 4.45, 'spread', spread=0.8)
    key_fingers(rig, 'R', 5.0, 'relaxed', blend=('cup', 0.5), spread=0.5)
    key_fingers(rig, 'R', 5.75, 'spread', spread=0.7)
    R(5.75, (w + Vector((0.01, -0.01, 0.006)), f, n))
    L(5.75, SIDE_L)
    # ---- (joint cutaway: the character is off screen) ----
    R(10.4, LOW_R)
    key_fingers(rig, 'R', 10.4, 'relaxed')
    L(10.4, SIDE_L)
    # ---- shot 5: tries again, nothing ----
    crack_sequence(12.1, 13.35, False)
    r, l = _contact(0.05, dw=(0.0, -0.02, 0.0))
    R(14.25, r)
    L(14.25, (l[0] + Vector((0.03, -0.03, -0.02)), l[1], l[2]))
    key_fingers(rig, 'L', 14.25, 'relaxed')
    # turns the right hand palm-up to inspect it, then shakes it out
    insp = (Vector((-0.06, -0.36, 1.25)), Vector((0.25, -0.95, 0.15)), Vector((0.1, 0.1, 1.0)))
    R(14.8, insp)
    key_fingers(rig, 'R', 14.6, 'fist')
    key_fingers(rig, 'R', 14.95, 'relaxed', spread=0.3)
    L(14.8, SIDE_L)
    for i, dt in enumerate((15.1, 15.22, 15.34, 15.46, 15.58)):
        s = (-1) ** i
        R(dt, (insp[0] + Vector((0.012 * s, 0, 0.006)), insp[1] + Vector((0.12 * s, 0, 0)), insp[2]))
    R(16.0, insp)
    key_fingers(rig, 'R', 16.0, 'relaxed', spread=0.3)


def body(rig, look, cams):
    """Head, neck, breathing, gaze."""
    hands_c = FIST_W + Vector((0.06, -0.1, 0.0))
    K = lambda t, n, r: key_bone(rig, n, t, rot=r)   # noqa: E731
    # head: +X nods down, +Y turns to the character's left, +Z tilts
    for t, head, neck in (
            (0.0, (0.30, 0.02, 0.0), (0.10, 0, 0)),
            (2.3, (0.34, 0.0, -0.03), (0.12, 0, 0)),
            (2.55, (0.30, 0.0, -0.05), (0.10, 0, 0)),
            (2.7, (0.12, 0.0, 0.06), (0.05, 0, 0)),     # relief: head comes up
            (3.3, (0.18, -0.05, 0.05), (0.06, 0, 0)),
            (3.5, (0.30, -0.06, 0.0), (0.10, 0, 0)),
            (5.8, (0.30, -0.06, 0.0), (0.10, 0, 0)),
            (10.5, (-0.02, 0.0, 0.0), (0.0, 0, 0)),
            (10.9, (-0.06, 0.04, 0.10), (-0.02, 0, 0)),  # "That's the pop!"
            (11.6, (-0.02, 0.06, 0.06), (0.0, 0, 0)),
            (12.1, (0.30, 0.02, 0.0), (0.10, 0, 0)),
            (13.3, (0.34, 0.0, -0.03), (0.12, 0, 0)),
            (13.8, (0.30, 0.0, 0.0), (0.10, 0, 0)),
            (14.2, (0.22, 0.05, 0.12), (0.08, 0, 0)),   # puzzled tilt
            (14.9, (0.34, -0.10, 0.06), (0.10, 0, 0)),  # looks at his hand
            (15.6, (0.10, 0.0, 0.10), (0.04, 0, 0)),
            (16.0, (0.06, 0.02, 0.12), (0.03, 0, 0))):
        K(t, 'head', head)
        K(t, 'neck02', neck)
    # breathing on the chest
    for i in range(10):
        t = i * 1.7
        K(t, 'spine03', (0.015 if i % 2 else -0.01, 0, 0))
    # shoulders rise while pushing
    for t, v in ((0.0, 0.0), (2.25, 0.0), (2.5, 0.06), (2.8, 0.0), (13.1, 0.0), (13.35, 0.07), (13.9, 0.0)):
        for s, sg in (('L', 1), ('R', -1)):
            K(t, 'clavicle.' + s, (0.0, 0.0, sg * v))
    # gaze
    cam_pos = lambda name: cams[name].location.copy()   # noqa: E731
    for t, p in ((0.0, hands_c), (2.6, hands_c + Vector((0, 0, 0.05))), (2.85, cam_pos('crack')),
                 (3.3, cam_pos('crack')), (3.5, OPEN_R[0] + Vector((0, -0.08, 0))), (5.8, OPEN_R[0]),
                 (10.5, cam_pos('smile')), (12.0, cam_pos('smile')), (12.1, hands_c), (14.0, hands_c),
                 (14.2, hands_c + Vector((0.1, 0, 0.1))), (14.6, Vector((-0.06, -0.4, 1.25))),
                 (15.55, Vector((-0.06, -0.4, 1.25))), (15.75, cam_pos('again')), (16.0, cam_pos('again'))):
        key_loc(look, t, p)


def face(F):
    """Facial expressions (ARKit face units) and blinks."""
    F.key(0.0, browDownLeft=0.25, browDownRight=0.25, mouthPressLeft=0.2, mouthPressRight=0.2)
    F.key(2.25, browDownLeft=0.5, browDownRight=0.5, mouthPressLeft=0.5, mouthPressRight=0.5,
          eyeSquintLeft=0.3, eyeSquintRight=0.3, noseSneerLeft=0.15, noseSneerRight=0.15)
    F.key(2.6, eyeBlinkLeft=0.7, eyeBlinkRight=0.7, mouthSmileLeft=0.35, mouthSmileRight=0.35,
          browInnerUp=0.3, mouthRollLower=0.2)
    F.key(3.1, eyeBlinkLeft=0.15, eyeBlinkRight=0.15, mouthSmileLeft=0.55, mouthSmileRight=0.55,
          cheekSquintLeft=0.3, cheekSquintRight=0.3)
    F.key(3.5, mouthSmileLeft=0.3, mouthSmileRight=0.3)
    F.key(5.8, mouthSmileLeft=0.25, mouthSmileRight=0.25)
    F.key(10.5, mouthSmileLeft=0.3, mouthSmileRight=0.3)
    F.key(10.85, mouthSmileLeft=0.8, mouthSmileRight=0.8, cheekSquintLeft=0.55, cheekSquintRight=0.55,
          eyeSquintLeft=0.35, eyeSquintRight=0.35, browOuterUpLeft=0.35, browOuterUpRight=0.35,
          mouthDimpleLeft=0.3, mouthDimpleRight=0.3)
    F.key(11.9, mouthSmileLeft=0.7, mouthSmileRight=0.75, cheekSquintLeft=0.45, cheekSquintRight=0.5,
          eyeSquintLeft=0.3, eyeSquintRight=0.3, browOuterUpLeft=0.2, browOuterUpRight=0.25)
    F.key(12.2, mouthSmileLeft=0.2, mouthSmileRight=0.2, browDownLeft=0.2, browDownRight=0.2)
    F.key(13.3, browDownLeft=0.6, browDownRight=0.6, mouthPressLeft=0.6, mouthPressRight=0.6,
          eyeSquintLeft=0.45, eyeSquintRight=0.45, noseSneerLeft=0.3, noseSneerRight=0.3,
          mouthRollLower=0.3)
    F.key(13.75, browDownLeft=0.55, browDownRight=0.55, mouthPressLeft=0.55, mouthPressRight=0.55,
          eyeSquintLeft=0.4, eyeSquintRight=0.4, noseSneerLeft=0.25, noseSneerRight=0.25)
    F.key(14.15, browInnerUp=0.65, browDownLeft=0.35, mouthFrownLeft=0.35, mouthFrownRight=0.35,
          mouthLeft=0.35, mouthPucker=0.15, eyeWideLeft=0.15, eyeWideRight=0.15)
    F.key(15.6, browInnerUp=0.55, browOuterUpRight=0.4, mouthFrownLeft=0.3, mouthFrownRight=0.3,
          mouthLeft=0.3, mouthShrugLower=0.35)
    F.key(16.0, browInnerUp=0.55, browOuterUpRight=0.45, mouthFrownLeft=0.3, mouthFrownRight=0.3,
          mouthLeft=0.3, mouthShrugLower=0.4)
    for t in (0.9, 3.4, 4.9, 11.3, 12.6, 14.45, 15.7):
        F.blink(t)


def cameras(coll, scene):
    def cam(name, lens, loc, aim, fstop=2.2, up=None):
        d = bpy.data.cameras.new(name)
        d.lens = lens
        d.sensor_fit = 'VERTICAL'
        d.sensor_height = 24.0
        d.dof.use_dof = True
        d.dof.aperture_fstop = fstop
        d.clip_start = 0.02
        o = bpy.data.objects.new(name, d)
        coll.objects.link(o)
        o.location = loc
        d_ = (Vector(aim) - Vector(loc)).normalized()
        if up is None:
            o.rotation_euler = d_.to_track_quat('-Z', 'Y').to_euler()
        else:   # explicit up vector (for top-down views)
            u = Vector(up)
            u = (u - u.dot(d_) * d_).normalized()
            o.rotation_euler = Matrix((d_.cross(u), u, -d_)).transposed().to_euler()
        return o
    cams = {}
    cams['crack'] = cam('Cam1_Crack', 36, (-0.55, -1.6, 1.52), (0.0, -0.18, 1.43))
    cams['xray'] = cam('Cam2_Xray', 35, (-0.01, -0.60, 1.70), (-0.04, -0.46, 1.27), fstop=4.0, up=(0, 1, 0))
    cams['smile'] = cam('Cam4_Smile', 48, (0.16, -0.80, 1.68), (0.0, -0.08, 1.66), fstop=2.8)
    cams['again'] = cam('Cam5_Again', 36, (0.55, -1.6, 1.52), (0.0, -0.18, 1.43))
    # slow push-ins
    for name, dt, push in (('crack', (0.0, 3.55), 0.14), ('xray', (3.55, 5.75), 0.07),
                           ('smile', (10.55, 12.1), 0.05), ('again', (12.1, 16.0), 0.12)):
        o = cams[name]
        fwd = o.matrix_world.to_3x3() @ Vector((0, 0, -1))
        p0 = o.location.copy()
        key_loc(o, dt[0], p0)
        key_loc(o, dt[1], p0 + fwd * push)
        anim.set_ease(o, 'LINEAR')
        for i in range(3):
            anim.wiggle(o, 'location', i, 0.003, 22.0, seed=11 * i + len(name))
    return cams


def focus(cams, rig):
    """Focus pulls: each camera tracks the right part of the character."""
    for name, bone in (('crack', 'wrist.R'), ('again', 'wrist.R'), ('smile', 'head'), ('xray', 'metacarpal2.R')):
        e = bpy.data.objects.new('Focus_' + name, None)
        cams[name].users_collection[0].objects.link(e)
        e.parent = rig
        e.parent_type = 'BONE'
        e.parent_bone = bone
        e.location = (0, -0.11, 0.08) if bone == 'head' else (0, 0, 0)   # head: bone tail -> eyes
        cams[name].data.dof.focus_object = e
