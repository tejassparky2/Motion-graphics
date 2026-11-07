"""Helper 9's Episode 3 (DIORAMA_EP03.md): the shared night (mk/night.py) entry points, and the shots S04 (the sun
goes down), S05 (the dark island, one coral dot) and S18 (Wren whispers and points; the lighthouse).

For everyone's night shots:

    from channels.monsters.diorama_ep03 import helper9 as N9
    N9.night(n)                  # after X._world(n): the night grade (moon, sky, haze, the mark's warm light)
    N9.dusk(n)                   # the dusk version (S04's end state)
    lt = N9.mark(k)              # Kai's wrist mark: the coral key light, on his left forearm bone (follows every pose)
    lh = N9.lighthouse()         # the ruined lighthouse across the lake (once per scene)

night() can come before the characters are built: materials are tagged for the mark's light again when the render
starts.
"""
import math

from channels.monsters.mk import night as NG

MARK_W = 6000.0                      # the mark light at night (no shadows; its light comes back through the grade)


def night(n=None, azim=None):
    """The night grade on the current scene (call after X._world / diorama.setup)."""
    return NG.apply("night", azim=azim)


def dusk(n=None, azim=None):
    return NG.apply("dusk", azim=azim)


def mark(k, energy=MARK_W, key=None, u=0.3):
    """Kai's mark as the coral key light: `key` = [(frame, energy)] for a flare or a dim."""
    return NG.mark_light(k, energy=energy, key=key, u=u)


def lighthouse(**kw):
    return NG.lighthouse(**kw)


SHOTS = {}
