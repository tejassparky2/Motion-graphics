"""Procedural animation, baked to keyframes on every frame.

All motion is a function of time; the bike's kinematics are consistent
(wheel spin = distance / radius, chain & cog driven by the crank through the
real gear ratio, freewheel while coasting).
"""
import math

import bpy
import numpy as np

from . import bicycle as B
from .util import smoothstep

FPS = 24


def bake(id_owner, path, index, frames, values, group=None):
    index = max(index, 0)
    ad = id_owner.animation_data or id_owner.animation_data_create()
    if ad.action is None:
        ad.action = bpy.data.actions.new(f"{id_owner.name}Action")
    fc = ad.action.fcurves.find(path, index=index)
    if fc is None:
        fc = ad.action.fcurves.new(path, index=index, action_group=group or "")
    fc.keyframe_points.clear()
    n = len(frames)
    fc.keyframe_points.add(n)
    co = np.empty(2 * n, dtype=np.float32)
    co[0::2] = frames
    co[1::2] = values
    fc.keyframe_points.foreach_set("co", co)
    fc.keyframe_points.foreach_set("interpolation", np.full(n, 1, dtype=np.int32))  # LINEAR
    fc.update()
    # Blender 4.4+ slotted actions: make sure the action's slot is assigned
    if hasattr(ad, 'action_slot') and ad.action_slot is None and len(ad.action.slots):
        ad.action_slot = ad.action.slots[0]
    return fc


def integrate(rate, dt):
    out = np.zeros_like(rate)
    out[1:] = np.cumsum(0.5 * (rate[1:] + rate[:-1]) * dt)
    return out


class Timeline:
    """Sampled at sub-frame resolution for smooth integration."""

    def __init__(self, seconds, fps=FPS, start_frame=1, sub=4):
        self.fps = fps
        self.start = start_frame
        self.nframes = int(round(seconds * fps)) + 1
        self.sub = sub
        n = (self.nframes - 1) * sub + 1
        self.t = np.linspace(0, seconds, n)
        self.dt = self.t[1] - self.t[0]
        self.frames = self.start + np.arange(self.nframes)

    def at_frames(self, arr):
        return np.asarray(arr)[::self.sub]


def bike_motion(T, coast=(9.2, 13.4), v0=3.05, x0=0.0, y0=0.55):
    t = T.t
    c0, c1 = coast
    # cadence (rev/s): pedalling, ease out into a coast, ease back in
    pedal_on = 1 - smoothstep(c0 - 0.7, c0, t) + smoothstep(c1, c1 + 0.8, t)
    pedal_on = np.clip(pedal_on, 0, 1)
    v = v0 * (1 - 0.10 * smoothstep(c0, c1, t) * (1 - smoothstep(c1, c1 + 1.5, t)))
    # gentle start: already rolling at frame 1
    cad = v / (B.GEAR * 2 * math.pi * B.R) * pedal_on
    crank = integrate(cad * 2 * math.pi, T.dt)
    # park the cranks level while coasting: shift so crank angle at c0 is k*pi
    i0 = np.searchsorted(t, c0)
    shift = round(crank[i0] / math.pi) * math.pi - crank[i0]
    crank = crank + shift
    dist = integrate(v, T.dt)
    # gentle S-curve weave across the planks
    y = y0 + 0.10 * np.sin(t * 0.42 + 0.6) + 0.035 * np.sin(t * 1.3)
    x = x0 + dist
    dx = np.gradient(x, T.dt)
    dy = np.gradient(y, T.dt)
    yaw = np.arctan2(dy, dx)
    curv = np.gradient(yaw, T.dt) / np.maximum(v, 0.1)
    lean_turn = np.arctan(v * v * curv / 9.81)
    # pedalling sway (rider rocks the bike a little each stroke)
    sway = 0.012 * np.sin(crank) * pedal_on
    steer_balance = 0.010 * np.sin(crank + 0.6) * pedal_on + 0.006 * np.sin(t * 2.1)
    steer = B.WHEELBASE * curv + steer_balance
    # deck texture: small bumps from the plank seams (low-passed)
    rng = np.random.default_rng(7)
    bump = np.convolve(rng.normal(0, 1, len(t)), np.ones(9) / 9, mode='same') * 0.0012
    chain = (crank - crank[0]) * B.RING_R
    return dict(t=t, x=x, y=y, yaw=yaw, lean=lean_turn + sway, steer=steer, crank=crank,
                wheel=dist / B.R, cog=chain / B.COG_R, chain=chain, v=v, bump=bump,
                pedal_on=pedal_on, cad=cad)


def apply_bike(T, bike, m, z_deck=0.0):
    fr = T.frames
    A = T.at_frames
    root = bike['root']
    root.rotation_mode = 'XYZ'
    bake(root, 'location', 0, fr, A(m['x']))
    bake(root, 'location', 1, fr, A(m['y']))
    bake(root, 'location', 2, fr, A(z_deck + m['bump']))
    bake(root, 'rotation_euler', 2, fr, A(m['yaw']))
    bake(bike['lean'], 'rotation_euler', 0, fr, A(m['lean']))
    bake(bike['steer'], 'rotation_euler', 2, fr, A(m['steer']))
    bike['steer'].rotation_mode = 'XYZ'
    bake(bike['crank'], 'rotation_euler', 1, fr, A(m['crank']))
    bake(bike['rear_spin'], 'rotation_euler', 1, fr, A(m['wheel']))
    bake(bike['front_spin'], 'rotation_euler', 1, fr, A(m['wheel']))
    bake(bike['cog'], 'rotation_euler', 1, fr, A(m['cog']))
    # pedals stay roughly level with a little ankling
    ankle = 0.22 * np.sin(m['crank'] + 0.9) * m['pedal_on']
    for nm, ph in (('R', 0.0), ('L', math.pi)):
        an = 0.22 * np.sin(m['crank'] + ph + 0.9) * m['pedal_on']
        bake(bike['pedals'][nm], 'rotation_euler', 1, fr, A(-m['crank'] + an))
    mod = bike['chain'].modifiers['Links']
    sock = bike['chain_socket']
    bake(bike['chain'], f'modifiers["Links"]["{sock}"]', -1, fr, A(m['chain']))


# ---------------------------------------------------------------------------
# Rider
# ---------------------------------------------------------------------------

def key_track(t, keys):
    """Piecewise smooth interpolation through (time, value) keys (value may be tuple)."""
    ts = np.array([k[0] for k in keys])
    vs = np.array([k[1] for k in keys], dtype=float)
    out = np.zeros((len(t),) + vs.shape[1:])
    for i in range(len(keys) - 1):
        a, b = ts[i], ts[i + 1]
        m = (t >= a) & (t <= b)
        s = smoothstep(a, b, t[m])
        out[m] = vs[i] * (1 - s)[..., None] + vs[i + 1] * s[..., None] if vs.ndim > 1 else vs[i] * (1 - s) + vs[i + 1] * s
    out[t < ts[0]] = vs[0]
    out[t > ts[-1]] = vs[-1]
    return out


def spring(input_acc, dt, freq=3.2, damp=0.18):
    """Damped oscillator x'' = -w^2 x - 2 z w x' + a(t)."""
    w = 2 * math.pi * freq
    x = np.zeros_like(input_acc)
    v = 0.0
    xi = 0.0
    for i in range(1, len(input_acc)):
        a = -w * w * xi - 2 * damp * w * v + input_acc[i]
        v += a * dt
        xi += v * dt
        x[i] = xi
    return x


def _arm_to_local(rig, bone, vec):
    """Small-angle rotation vectors / offsets from armature space to bone space."""
    Bm = np.array(rig.data.bones[bone].matrix_local.to_3x3())
    return np.asarray(vec) @ Bm


def _bake_rot(rig, bone, fr, rx, ry, rz):
    loc = _arm_to_local(rig, bone, np.stack([rx, ry, rz], 1))
    for i in range(3):
        bake(rig, f'pose.bones["{bone}"].rotation_euler', i, fr, loc[:, i])


def apply_rider(T, rig, m, head_keys, jaw_keys):
    """Armature space = bike space: X forward, Y left, Z up.
    Rotations: about X = roll/tilt, about Y = pitch (nose down +), about Z = yaw (left +)."""
    t = T.t
    fr = T.frames
    A = T.at_frames
    pb = rig.pose.bones
    for b in pb:
        b.rotation_mode = 'XYZ'
    crank = m['crank']
    on = m['pedal_on']
    z0 = np.zeros(len(fr))
    # torso: bob twice per revolution, roll toward the pushing leg
    bob = 0.0045 * np.cos(2 * crank) * on
    roll = 0.035 * np.sin(crank) * on
    pitch = -0.012 * np.cos(2 * crank) * on + 0.015 * (1 - on)
    yaw = 0.018 * np.sin(crank + 0.4) * on
    loc = _arm_to_local(rig, 'torso', np.stack([0 * bob, 0 * bob, bob], 1))
    for i in range(3):
        bake(rig, 'pose.bones["torso"].location', i, fr, A(loc[:, i]))
    _bake_rot(rig, 'torso', fr, A(roll), A(pitch), A(yaw))
    # head look keys: (yaw, pitch, tilt); stabilise against torso and bike roll
    look = key_track(t, head_keys)
    stab_roll = -(roll + m['lean']) * 0.85
    stab_pitch = -pitch
    stab_yaw = -yaw
    share = {'neck.1': 0.08, 'neck.2': 0.14, 'neck.3': 0.20, 'neck.4': 0.24, 'neck.5': 0.18, 'head': 0.16}
    for name, w in share.items():
        _bake_rot(rig, name, fr, A((look[:, 2] + stab_roll) * w), A((look[:, 1] + stab_pitch) * w),
                  A((look[:, 0] + stab_yaw) * w))
    jaw = key_track(t, jaw_keys)
    _bake_rot(rig, 'jaw', fr, A(0 * jaw), A(jaw), A(0 * jaw))
    # pouch jiggle: driven by vertical acceleration and head motion
    acc = np.gradient(np.gradient(bob + m['bump'], T.dt), T.dt) * 6.0
    acc += np.gradient(np.gradient(look[:, 1], T.dt), T.dt) * 0.6
    acc += np.gradient(np.gradient(jaw, T.dt), T.dt) * 0.8
    pj = np.clip(spring(acc, T.dt, freq=2.6, damp=0.16), -0.25, 0.25)
    side = np.clip(spring(np.gradient(np.gradient(roll + look[:, 0], T.dt), T.dt), T.dt, freq=1.8, damp=0.2) * 2.0,
                   -0.2, 0.2)
    _bake_rot(rig, 'pouch', fr, A(side), A(pj), A(0 * pj))
    # tail: a little counter-wag
    _bake_rot(rig, 'tail', fr, A(0 * t), A(0.02 * np.sin(t * 2.3)), A(-0.6 * yaw + 0.03 * np.sin(t * 1.7)))
    return look


def feather_wind(plumage, arr, T, speed=3.0, strength=0.0035):
    """Displace feather tips with a noise field streaming past the bird."""
    tex = bpy.data.textures.new("FeatherWind", 'CLOUDS')
    tex.noise_scale = 0.05
    tex.noise_depth = 2
    flex = np.clip(arr['flex'], 0, 1) ** 1.6
    reg = arr['region']
    gain = np.select([reg == 3, reg == 2, reg == 0], [3.0, 0.9, 0.7], 0.5)
    w = np.clip(flex * gain / 3.0, 0, 1)
    vg = plumage.vertex_groups.new(name="wind")
    q = np.round(w, 2)
    for val in np.unique(q):
        if val <= 0:
            continue
        vg.add(np.nonzero(q == val)[0].tolist(), float(val), 'REPLACE')
    drv = bpy.data.objects.new("WindField", None)
    bpy.context.scene.collection.objects.link(drv)
    drv.parent = plumage
    mod = plumage.modifiers.new("Wind", 'DISPLACE')
    mod.texture = tex
    mod.texture_coords = 'OBJECT'
    mod.texture_coords_object = drv
    mod.direction = 'NORMAL'
    mod.vertex_group = "wind"
    mod.strength = strength * 3.0
    mod.mid_level = 0.5
    # keep after the armature, before the normal transfer
    idx = list(plumage.modifiers).index(mod)
    plumage.modifiers.move(idx, 1)
    bake(drv, 'location', 0, T.frames, -speed * T.at_frames(T.t))
    bake(drv, 'location', 2, T.frames, 0.3 * np.sin(T.at_frames(T.t) * 0.7))
    return mod
