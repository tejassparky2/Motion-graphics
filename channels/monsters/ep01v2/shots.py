"""Episode 1 (v2) shot registry: every builder's module adds its SHOTS here (see channels/monsters/EP01V2_SHOTS.md)."""
import importlib

SHOTS = {}
for _m in ("coordinator", "helper1", "helper2", "helper3", "helper4", "helper5", "helper6", "helper9", "helper10",
           "bgqrs", "xprl", "helper8"):
    try:
        SHOTS.update(importlib.import_module(f"channels.monsters.ep01v2.{_m}").SHOTS)
    except ModuleNotFoundError as e:
        if e.name != f"channels.monsters.ep01v2.{_m}":
            raise
