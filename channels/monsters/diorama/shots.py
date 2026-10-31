"""Diorama style-test shot registry (channels/monsters/DIORAMA_TEST.md): each builder module adds its SHOTS here.

    blender -b -y -P channels/monsters/render_shot.py -- diorama D15 OUT_DIR [--frames A-B] [--still N --scale 0.5]
"""
import importlib

SHOTS = {}
for _m in ("helper10", "bgqrs", "helper3", "helper2", "xprl", "helper6", "helper5"):
    try:
        SHOTS.update(importlib.import_module(f"channels.monsters.diorama.{_m}").SHOTS)
    except ModuleNotFoundError as e:
        if e.name != f"channels.monsters.diorama.{_m}":
            raise
