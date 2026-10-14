"""The Crocodile Dilemma, re-voiced with Chatterbox Turbo and its voice tags (owner, 14 Oct 2026: "make another video
with turbo tags ... use correct emotion tags in the right place, make it human"). Same approved words and pictures as
videos/crocodile_dilemma.py; only the voice changes:

- narrator: Turbo's stock voice; crocodile and mother: Turbo too, taking the timbre of a synthetic Kokoro voice
  (am_onyx / af_heart), so they get tags and emotion as well (the court test kept Kokoro characters).
- tags, kept few and only where a person telling the story would make the sound (out/turbo_tags_research.md):
  the crocodile [laugh]s after making its trap of a deal; the mother [sniff]s before her brave answer; the narrator
  [chuckle]s when the trap turns on the crocodile; [dramatic] leans on the conclusion; [happy] lifts the try-it-at-home
  bit. The logic lines stay plain, so they stay clear.

  NARRATOR_ENGINE=clone CLONE_MODEL=turbo python render.py --video crocodile_dilemma_turbo
"""
from videos.crocodile_dilemma import *          # noqa: F401,F403  (scenes, metadata, NARRATOR, TAIL)
from videos.crocodile_dilemma import SCRIPT as _PLAIN

voice.SPEAKERS.update({"croc": dict(voice="am_onyx", speed=0.92, pitch=-2.0, turbo_ref="am_onyx"),
                       "mom": dict(voice="af_heart", speed=1.05, turbo_ref="af_heart")})

TAGGED = {
    "k2": "Guess what I'm going to do. Guess right, and you get your child back. [laugh]",
    "k3": "The mother thinks. Then she says. [sniff] You will not give my child back!",
    "k4": "Now the crocodile is stuck. [chuckle]",
    "k7": "[dramatic] Whatever it does, it breaks its own promise.",
    "k8": "[happy] Try it at home. Mom says: guess what I'll decide. Guess right, and you can go out. You say: you "
          "won't let me go.",
}
SCRIPT = [dict(spec, text=TAGGED.get(spec["id"], spec["text"])) for spec in _PLAIN]
