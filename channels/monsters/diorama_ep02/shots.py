"""Episode 2 (2.5D diorama) shot registry (channels/monsters/DIORAMA_EP02.md): each helper's diorama_ep02/<you>.py
adds its SHOTS here. Frame counts come from channels/monsters/ep02/timing.json (see ep02_frames()).

    blender -b -y -P channels/monsters/render_shot.py -- diorama_ep02 S05 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import importlib
import json
import os

_T = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "ep02", "timing.json")


def ep02_frames(shot):
    """render_frames (frames + the 12-frame tail handle) of an Episode 2 shot, from ep02/timing.json."""
    with open(_T) as f:
        return {s["shot"]: s["render_frames"] for s in json.load(f)["shots"]}[shot]


SHOTS = {}
for _m in ("bgqrs", "xprl", "helper1", "helper4", "helper5", "helper9", "helper10"):
    try:
        SHOTS.update(importlib.import_module(f"channels.monsters.diorama_ep02.{_m}").SHOTS)
    except ModuleNotFoundError as e:
        if e.name != f"channels.monsters.diorama_ep02.{_m}":
            raise
