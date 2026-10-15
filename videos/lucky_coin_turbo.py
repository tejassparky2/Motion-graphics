"""The Lucky Coin, re-voiced with Chatterbox Turbo + voice tags, like the crocodile video the owner preferred
(owner, 15 Oct 2026: "apply the new voice to these videos, the turbo one with tags, not my voice"). Same approved
words and pictures as videos/lucky_coin.py. Narrator: Turbo's stock voice (nobody cloned) with the tags; the kid and
Grandpa speak through Turbo with synthetic Kokoro reference voices, without tags (tags misfire in reference voices).
"""
from videos.lucky_coin import *          # noqa: F401,F403
from videos.lucky_coin import SCRIPT as _PLAIN, NARRATOR as _N

NARRATOR = dict(_N, turbo=True)
voice.SPEAKERS.update({"kid": dict(voice.SPEAKERS["kid"], turbo_ref="am_puck+3"),
                       "grandpa": dict(voice.SPEAKERS["grandpa"], turbo_ref="bm_george-1.5")})
TAGGED = {
    "c6": "Ask her out? Heads. They were married for fifty years. [chuckle]",
    "c8": "Now the grandson flipped it over. [gasp] And froze.",
}
SCRIPT = [dict(spec, text=TAGGED.get(spec["id"], spec["text"])) for spec in _PLAIN]
