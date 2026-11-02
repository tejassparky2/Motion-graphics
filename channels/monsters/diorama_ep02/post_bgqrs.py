"""Encode bGqrs's Episode 2 shots (S01, S03; DIORAMA_EP02.md) like every diorama shot: the Blender frames
build/monsters/diorama_ep02/<SHOT>/0001.png ... -> out/monsters/diorama_ep02/shots/<SHOT>.mp4 + <SHOT>_sheet.jpg
(crf 10, stream-copy remux, no encoder tags), checking the frame count against ep02/timing.json. No 2D pass: the
splash, dust and the bird's shadow are all in the 3D render.

    python channels/monsters/diorama_ep02/post_bgqrs.py S01 [S03]
"""
import os
import sys

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
sys.path.insert(0, ROOT)

from channels.monsters.diorama_ep02.helper10 import encode  # noqa: E402

if __name__ == "__main__":
    for shot in sys.argv[1:]:
        encode(shot, os.path.join(ROOT, "build", "monsters", "diorama_ep02", shot))
