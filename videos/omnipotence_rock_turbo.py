"""1 Rock, 2 Answers (Last Bencher), re-voiced with Chatterbox Turbo + voice tags like the crocodile video (owner,
15 Oct 2026). Same approved words and pictures as videos/omnipotence_rock.py. Narrator: Turbo stock voice with tags;
the kid and the teacher through Turbo with synthetic Kokoro reference voices, no tags.
"""
from videos.omnipotence_rock import *          # noqa: F401,F403
from videos.omnipotence_rock import SCRIPT as _PLAIN, NARRATOR as _N

NARRATOR = dict(_N, turbo=True)
voice.SPEAKERS.update({"kid": dict(voice.SPEAKERS["kid"], turbo_ref="am_puck+3"),
                       "sir": dict(voice.SPEAKERS["sir"], turbo_ref="am_michael")})
TAGGED = {
    "q2": "[gasp] The teacher freezes.",
    "q6": "But the teacher just smiles, and hands him the chalk. [chuckle]",
}
SCRIPT = [dict(spec, text=TAGGED.get(spec["id"], spec["text"])) for spec in _PLAIN]
