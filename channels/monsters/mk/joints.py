"""Kai's joints projected to the frame, for 2D effects that must sit on his body (fx2d.xray_flash's skeleton).

    from channels.monsters.mk import joints
    joints.export(rig, cam, range(f0, f1 + 1), "build/monsters/S08b_joints.json")   # in the shot builder

then in the comp:  J = joints.load(path);  (fx2d.xray_flash, dict(start=..., joints=joints.at(J, f0)))
Positions are full-resolution pixels (render.resolution_x/y, ignoring resolution_percentage), y down, keyed by
fx2d.JOINTS names."""
import json

# fx2d.JOINTS name -> (VRM bone name, where along the bone: 0 = its head, 1 = its tail)
MAP = {"head": ("head", 0.55), "neck": ("neck", 0.0), "chest": ("chest", 0.0), "pelvis": ("hips", 0.0),
       "l_shoulder": ("left_upper_arm", 0.0), "r_shoulder": ("right_upper_arm", 0.0),
       "l_elbow": ("left_lower_arm", 0.0), "r_elbow": ("right_lower_arm", 0.0),
       "l_hand": ("left_hand", 0.0), "r_hand": ("right_hand", 0.0),
       "l_hip": ("left_upper_leg", 0.0), "r_hip": ("right_upper_leg", 0.0),
       "l_knee": ("left_lower_leg", 0.0), "r_knee": ("right_lower_leg", 0.0),
       "l_foot": ("left_foot", 0.0), "r_foot": ("right_foot", 0.0)}


def project(rig, cam, scene=None, head_up=0.0):
    """{joint: (x, y)} for the current frame. head_up raises the skull centre (Blender units, world Z) if the
    head bone sits low in a big anime head."""
    import bpy
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    scene = scene or bpy.context.scene
    arm = rig["arm"]
    rx, ry = scene.render.resolution_x, scene.render.resolution_y
    out = {}
    for name, (bone, k) in MAP.items():
        pb = rig["bone"](bone)
        co = arm.matrix_world @ (pb.head + (pb.tail - pb.head) * k)
        if name == "head":
            co = co + Vector((0, 0, head_up))
        v = world_to_camera_view(scene, cam, co)
        out[name] = (round(v.x * rx, 1), round((1 - v.y) * ry, 1))
    return out


def export(rig, cam, frames, path, head_up=0.0):
    """Write {frame: joints} for the frames (sets each frame, so call it before the render loop)."""
    import bpy
    sc = bpy.context.scene
    keep = sc.frame_current
    data = {}
    for f in frames:
        sc.frame_set(f)
        data[str(f)] = project(rig, cam, sc, head_up)
    sc.frame_set(keep)
    with open(path, "w") as fh:
        json.dump(data, fh)
    return data


def load(path):
    with open(path) as fh:
        return {int(k): v for k, v in json.load(fh).items()}


def at(data, first_frame, fps=24):
    """A joints function for fx2d.xray_flash(joints=...): shot time t -> that frame's joints (frame first_frame at
    t = 0; the nearest exported frame if t falls outside)."""
    keys = sorted(data)

    def fn(t):
        f = first_frame + int(round(t * fps))
        f = min(keys, key=lambda k: abs(k - f)) if f not in data else f
        return {k: tuple(v) for k, v in data[f].items()}
    return fn
