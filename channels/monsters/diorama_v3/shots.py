"""Episode 1 v3 (2.5D) shot registry (channels/monsters/DIORAMA_EP01_V3.md): each helper's diorama_v3/<you>.py adds
its SHOTS here. Frame counts come from channels/monsters/ep01v3/timing.json (see v3_frames()).

    blender -b -y -P channels/monsters/render_shot.py -- diorama_v3 S08a OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import importlib
import json
import os

_T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ep01v3", "timing.json")


def v3_frames(shot):
    """render_frames (frames + the 12-frame tail handle) of a v3 shot, from ep01v3/timing.json."""
    with open(_T) as f:
        return {s["shot"]: s["render_frames"] for s in json.load(f)["shots"]}[shot]


SHOTS = {}
for _m in ("bgqrs", "xprl", "helper1", "helper2", "helper3", "helper4", "helper5", "helper6", "helper9", "helper10"):
    try:
        SHOTS.update(importlib.import_module(f"channels.monsters.diorama_v3.{_m}").SHOTS)
    except ModuleNotFoundError as e:
        if e.name != f"channels.monsters.diorama_v3.{_m}":
            raise
