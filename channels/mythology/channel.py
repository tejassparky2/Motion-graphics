"""Settings shared by every mythology video: one narrator per language, the reveal pause and where files live.

One video module serves both languages: SCRIPTS = {"hi": [...], "kn": [...]} with the same line ids, so the shots and
on-screen pictures are shared and only the voice and its timing change."""
import os

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ROOT = os.path.dirname(REPO)                                   # <shorts research>, outside the public repo
ASSETS_ROOT = os.path.join(ROOT, "myth_assets")
OUT_ROOT = os.path.join(ROOT, "myth_out")
LANGS = ("hi", "kn")
WHISPER_LANG = {"hi": "hi", "kn": "kn"}

# Hindi: the existing "Aman" narrator of Socho with Tejas (owner, 6 Nov 2026: "for hindi the voice you already have").
# Indic Parler-TTS's named speaker 'Aman' made the prompt; AI4Bharat IndicF5 speaks every line in that synthetic voice.
_HI_VOICES = os.path.join(ROOT, "mayank", "voice", "f5_refs")
# Kannada: the same recipe with an Indic Parler-TTS Kannada speaker (kn_voice_search.py, kn_voice_pick.py).
_KN_VOICES = os.path.join(ASSETS_ROOT, "voice", "kn_refs")
KN_REF_TEXT = ("ಯೋಚಿಸಿ, ಸಾವಿರಾರು ವರ್ಷಗಳಿಂದ ಜನ ಹೇಳುತ್ತಾ ಬಂದಿರುವ ಒಂದು ಕಥೆ. "
               "ಆದರೆ ಅದರ ಒಂದು ಭಾಗ, ಹೆಚ್ಚಿನವರಿಗೆ ಗೊತ್ತೇ ಇಲ್ಲ.")
# Owner's pick, 7 Nov 2026 ("A"): designed voice A, Indic Parler's speaker Aman reading Kannada with the Hindi
# narrator's own description, seed 11 (kn_voice_design.py), as the IndicF5 prompt. Was Suresh s42 on 6 Nov.
# Owner, 7 Nov 2026: "Style 2": OmniVoice speaking in Hemanth's cloned voice (consented), lines read in groups of three
# with his own short pauses ("copy same style continuity narration"). Voice A (design_aman_orig_s11, IndicF5) stays
# available with MYTH_KN_VOICE=design_aman_orig_s11 MYTH_KN_ENGINE=f5.
KN_VOICE = os.environ.get("MYTH_KN_VOICE", "hemanth_v1")    # file stem in _KN_VOICES
KN_ENGINE = os.environ.get("MYTH_KN_ENGINE", "omni")
# consented clones: the owner, the owner's brother, and (7 Nov 2026, "Clone this voice it's my friend's and he
# agrees") the owner's friend Darshan; his reference keeps his own delivery ("Copy the same narration style")
# and (7 Nov 2026, "Try cloning this" / "Yes hemanth said yes") the owner's friend Hemanth
CLONED = {"tejas_v2", "brother_v1", "darshan_v1", "hemanth_v1"}
# 7 Nov 2026 the owner rejected both synthetic Kannada voices ("The both kannada voice is not good") and asked for
# clones of two real voices with consent: their own ("this is mine") and their brother's ("he agress"). Those
# references live only in _KN_VOICES (never in the repo), each with its exact words in <stem>.txt beside it:
# tejas_v2 (the owner) and brother_v1 (the brother). Pick one with MYTH_KN_VOICE until the owner chooses.
_KN_TXT = os.path.join(_KN_VOICES, f"{KN_VOICE}.txt")
if os.path.exists(_KN_TXT):
    with open(_KN_TXT, encoding="utf-8") as f:
        KN_REF_TEXT = f.read().strip()

NARRATORS = {
    # owner, 6 Nov 2026: "i want voice to be clear calm and we'll understandable": a gentler speed-up than Socho's 1.15
    "hi": dict(engine="f5", studio="v3", tempo=1.05,
               ref_audio=os.path.join(_HI_VOICES, "named_aman_s3_ref.wav"),
               ref_text="सोचो, एक ऐसा पौधा जो कीड़ों को खा जाता है। और ये कोई फ़िल्म का सीन नहीं है, ये बिल्कुल सच है।"),
    # owner, 8 Nov 2026: "Can you speed up voice": 1.12x for a while; then 9 Nov 2026: "The kannada voice is not clear"
    # and, from four samples of the same lines, "Clear b" = Hemanth's own speed, no stretch (the stretch blurred him)
    "kn": dict(engine=KN_ENGINE, studio="v3", tempo=1.0,
               ref_audio=os.path.join(_KN_VOICES, f"{KN_VOICE}.wav"), ref_text=KN_REF_TEXT,
               **(dict(group=3, gap=0.20, qgap=0.28) if KN_ENGINE == "omni" else {})),
}
VOICE_REFS = {k: v["ref_audio"] for k, v in NARRATORS.items()}
NARRATOR_LABEL = ("synthetic narrators: Indic Parler-TTS named speakers (Apache-2.0; datasets CC BY 4.0) as voice "
                  "prompts, spoken by AI4Bharat IndicF5 (MIT), studio chain" + ("; Kannada spoken by OmniVoice (k2-fsa, Apache-2.0)" if KN_ENGINE == "omni" else "") +
                  (f"; Kannada: a consented clone of a real voice ({KN_VOICE})"
                   if KN_VOICE in CLONED else "; nobody is cloned"))   # records only
MUSIC = "tanpura"   # calm drone for story narration (motion/audio.py tanpura), ~21 dB under the voice
# Owner, 8 Nov 2026: "Reduce the number of background sounds it's irritating and won't let hear story calmy only use
# sounds where necessary". The scenes still list every cue (the Lakshman Rekha reel had 144 in 65 s); render_myth
# keeps only these, in this order of importance, at least SFX_MIN_GAP s apart, SFX_GAIN softer.
SFX_KEEP = ["conch", "bell", "shimmer", "damaru", "hit"]   # big reveal, sacred beat/ending, magic, the hook's beat
SFX_MIN_GAP = 8.0
SFX_GAIN = 0.6                                                # about 4 dB quieter than before
TAIL = 0.9
REVEAL_GAP = 0.6       # the longer pause before a reveal
