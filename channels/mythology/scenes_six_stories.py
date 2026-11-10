"""Long video 1 (videos/six_stories.py, 1920x1080): routes each moment to the scene module that owns its line.

  scenes_six_a: intro (i*), story 1 Kacha (k*), story 6 Yayati (y*), outro (o*)   [Devayani, Shukra, Kacha]
  scenes_six_b: story 2 Mandavya (m*), story 5 Nachiketa (n*)                      [Yama in both]
  scenes_six_c: story 3 Agastya (g*), story 4 Rishyashringa (s*)                   [water, forest, rain]

The active line at time t is the last line that has started (a pause belongs to the line before it)."""
import bisect
import importlib

PARTS = {"i": "scenes_six_a", "k": "scenes_six_a", "y": "scenes_six_a", "o": "scenes_six_a",
         "m": "scenes_six_b", "n": "scenes_six_b",
         "g": "scenes_six_c", "s": "scenes_six_c"}


def _prefix(beat_id):
    return beat_id.rstrip("0123456789")


def _module(beat_id):
    return importlib.import_module(PARTS[_prefix(beat_id)])


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
