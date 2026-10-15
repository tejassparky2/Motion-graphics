"""The Immortal Jellyfish, re-voiced with Chatterbox Turbo + voice tags like the crocodile video (owner, 15 Oct 2026).
Same approved words and pictures as videos/immortal_jellyfish.py; narrator only (Turbo stock voice).
"""
from videos.immortal_jellyfish import *          # noqa: F401,F403
from videos.immortal_jellyfish import SCRIPT as _PLAIN

NARRATOR = dict(globals().get("NARRATOR", {}), turbo=True)
TAGGED = {
    "j5": "This one cheats. [chuckle]",
    "j12": "So is it truly immortal? [sigh] Not quite.",
}
SCRIPT = [dict(spec, text=TAGGED.get(spec["id"], spec["text"])) for spec in _PLAIN]
