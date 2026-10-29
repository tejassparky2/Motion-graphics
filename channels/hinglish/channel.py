"""Settings shared by every "Socho with Tejas" video: the narrator voice, the reveal pause and where assets live."""
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.dirname(REPO)                                   # <shorts research>, outside the public repo
ASSETS_ROOT = os.path.join(ROOT, "hinglish_assets")

# Owner, 29 Oct 2026: "Aman looks good" / "the words are not clear". Aman's voice comes from Indic Parler-TTS
# (named speaker, prompt 'named_aman_s3'); IndicF5 then speaks every line in that synthetic voice: WER 33% -> 22%,
# UTMOS 2.76 -> 3.66, same voice (ECAPA 0.81 to the prompt) in the 3-line test.
_VOICES = os.path.join(ROOT, "mayank", "voice")
NARRATOR = dict(engine="f5", studio="v3", tempo=1.15,   # one even speed-up for every line (owner: "speed up voice little",
                # then "speed up slightly like matching mayank speed"); 1.15 is the most atempo takes before rubberband
                ref_audio=os.path.join(_VOICES, "f5_refs", "named_aman_s3_ref.wav"),
                ref_text="सोचो, एक ऐसा पौधा जो कीड़ों को खा जाता है। और ये कोई फ़िल्म का सीन नहीं है, ये बिल्कुल सच है।")
VOICE_REF = os.path.join(_VOICES, "f5_refs", "named_aman_s3_ref.wav")
NARRATOR_LABEL = ("synthetic narrator: Indic Parler-TTS named speaker 'Aman' (Apache-2.0; datasets CC BY 4.0) as the "
                  "voice prompt, spoken by AI4Bharat IndicF5 (MIT), studio chain; nobody is cloned")   # records only
MUSIC = "pad"
TAIL = 0.9
# the longer pause Mayank leaves only before a reveal (the name, the precision beat, the closing line)
REVEAL_GAP = 0.6
