"""Long video 2 (videos/yamlok_yatra.py, 1920x1080): routes each moment to the scene module that owns its line.

  scenes_yy_a: intro (i*), the two lives and the night of death (d*), the ten rice-balls (p*)   [home, shop, street]
  scenes_yy_b: the road (w*), the sixteen cities (c*), the Vaitarani (v*), the cold city (s*)    [the journey]
  scenes_yy_c: Yama's court (y*), the eastern gate (t*), the ending (o*)                          [Yama's city]

The shared cast (Dhaniram, Bhola, the thumb-sized and hand-sized soul) lives in yy_cast.py. The active line at time t is
the last line that has started (a pause belongs to the line before it)."""
import bisect
import importlib

PARTS = {"i": "scenes_yy_a", "d": "scenes_yy_a", "p": "scenes_yy_a",
         "w": "scenes_yy_b", "c": "scenes_yy_b", "v": "scenes_yy_b", "s": "scenes_yy_b",
         "y": "scenes_yy_c", "t": "scenes_yy_c", "o": "scenes_yy_c"}


def _module(beat_id):
    return importlib.import_module(PARTS[beat_id[0]])


def active_beat(tl, t):
    starts = [b.start for b in tl.beats]
    i = max(0, bisect.bisect_right(starts, t) - 1)
    return tl.beats[i]


def draw(cr, t, tl):
    _module(active_beat(tl, t).id).draw(cr, t, tl)


def sfx(tl):
    events = []
    for mod in sorted(set(PARTS.values())):
        events += importlib.import_module(mod).sfx(tl)
    return sorted(events, key=lambda e: e[0] if isinstance(e, (tuple, list)) else e.get("t", 0))
