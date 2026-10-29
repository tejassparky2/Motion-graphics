"""Settings shared by every "Doc and the Organs" explainer reel (the English copy of the Hinglish channel's
mini-documentary pipeline, 29 Oct 2026): narrator, music, pauses and where the photos live."""
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Photo cut-outs and their credits.json (public domain / CC0 / CC BY only, so they can live in the public repo)
ASSETS_ROOT = os.path.join(REPO, "assets", "doctor_photos")

# Owner, 27 Oct 2026: "Change to clear and best voice" -> Chatterbox full model, its built-in stock voice (nobody is
# cloned), at its natural pace (research_notes/voice_match.md)
NARRATOR = dict(chatterbox=True, tempo_min=1.0, tempo_max=1.0)
MUSIC = "doc"      # motion.audio.doc: carried by phone speakers, ~16-20 dB under the voice, dips before reveals
TAIL = 0.9
GAP = 0.36         # silence between two lines (the reference reels' sentence pauses, 0.50-0.61 s with the takes' edges)
REVEAL_GAP = 0.6   # the longer pause only before a reveal: the name, a re-hook, the closing line
