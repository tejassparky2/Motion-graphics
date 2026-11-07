"""Cute Things Kill Here, Episode 3: "They Rang Every Bell. The Moths Didn't Care" (2.5D diorama, like Episodes 1-2).

The viewers voted B on Episode 2 ("Most said b continue with it", owner, 7 Nov 2026): Kai shows Wren the glowing mark.
The owner approved this script on 7 Nov 2026 ("Ok"). Arc beat Ep 3-4 in out/monsters/story_v2.md: the village's
belief (bells) fails on screen while the real animal reason works (moths keep their backs to the light: the dorsal
light response), one sky-crack clue (Wren: "The sky cracked the night you fell."), the danger is solved, then a new
pull at the vote (the old lighthouse). Outcome: a clean win with a social cost (Ep 2 was a costly win).

    SYNTH=1 EP=ep03 /home/user/.venv-main/bin/python channels/monsters/ep01v2_timing.py
        -> channels/monsters/ep03/timing.json and TIMING.md (voices the lines, Turbo; Whisper medium.en after)
"""
from motion import voice

NARRATOR = dict(turbo=True, turbo_ref="am_liam")   # Kai: the same voice as Episodes 1-2
# Wren, the village bell-keeper: the same Turbo voice as Episode 2 (from a Kokoro clip; synthetic, nobody cloned).
voice.SPEAKERS["wren"] = dict(voice="af_sky", turbo_ref="af_sky+5")
TAIL = 0.35                                        # cut ~0.5 s after the last word
TWIST = "l14"                                      # the flip: the music drops under it

SCRIPT = [
    dict(id="l1", scene="S01", text="You said show her. So I did."),
    dict(id="l2", scene="S02", text="Marked. The sky cracked the night you fell.", gap=0.5,
         speaker="wren", speaker_from="Marked"),
    dict(id="l3", scene="S03", text="The whole village backed away from me.", gap=0.5),
    dict(id="l4", scene="S04", text="Then the sun went down.", gap=0.6),
    dict(id="l5", scene="S05", text="And my wrist was the only light for miles.", gap=0.4),
    dict(id="l6", scene="S06", text="That's when the fluffmoths came down the hill.", gap=0.7),
    dict(id="l7", scene="S07", text="Their wing dust stings like nettles.", gap=0.4),
    dict(id="l8", scene="S08", text="Ring the bells! Bells drive them off!", gap=0.4,
         speaker="wren", speaker_from="Ring"),
    dict(id="l9", scene="S09", text="The bells rang. The moths didn't even notice.", gap=0.9),   # the bells ring first
    dict(id="l10", scene="S10", text="They were circling my wrist. Round and round.", gap=0.5),
    dict(id="l11", scene="S11", text="Moths don't fly at a light. They keep their backs to it.", gap=0.6),
    dict(id="l12", scene="S12", text="So when the light is above them, they circle it.", gap=0.4),
    dict(id="l13", scene="S13", text="So I put the light below them.", gap=0.5),
    dict(id="l14", scene="S14", text="", hold=2.6, gap=0.5),        # THE FLIP: the swarm tumbles, no words
    dict(id="l15", scene="S15", text="Every single moth landed on its back.", gap=0.4),
    dict(id="l16", scene="S16", text="Wren lowered her bell.", gap=1.8),    # hold the field of upside-down moths (laugh)
    dict(id="l17", scene="S17", text="The village wants you gone by sunrise.", gap=0.7,
         speaker="wren", speaker_from="The"),
    dict(id="l18", scene="S18", text="But the last marked one left something at the old lighthouse.", gap=0.7,
         speaker="wren", speaker_from="But"),   # a whisper: quieter and closer in the mix (Turbo has no real whisper)
    dict(id="l19", scene="S19", text="Option A: go with Wren tonight. Option B: leave at sunrise, like they said. "
                                     "Comment A or B.", gap=0.8),
]

SPLITS = []        # (shot, line, the word the second shot opens on): none yet

# The upload sheet. Audience: NOT made for kids (comments stay on for the vote). Fully animated fantasy: no
# altered-content disclosure. Music and effects are original.
METADATA = dict(
    title="They Rang Every Bell. The Moths Didn't Care 🦋",
    alt_titles=["The Whole Village Ran From My Wrist 🦋",
                "Moths Don't Fly at Lights. I Used That 🦋"],
    description="""You voted B, so Kai showed Wren the glowing mark. The whole village backed away. Then night fell, and his
wrist was the only light for miles.

His only weapon is still what he knows.

Cute Things Kill Here, Episode 3.
Comment A to GO with Wren to the lighthouse tonight, or B to LEAVE at sunrise. The letter in more comments decides
Episode 4.

The real facts:
- Moths don't fly straight at a light. They tilt their backs toward it, which makes them circle a light above them
  and flip over and crash when the light is below them (Fabian et al., "Why flying insects gather at artificial
  light", Nature Communications 2024).
- The stinging wing dust is borrowed from real Hylesia moths, whose tiny body hairs cause itchy rashes.

Original story and animation. The creatures and the world are fictional.
Hero base model: Seed-san by VirtualCast, Inc. (VRM Public License 1.0)""",
    hashtags=["#anime", "#isekai", "#Shorts"],
    tags=["original anime", "isekai", "reincarnated", "anime short", "2.5d anime", "cute monsters", "moths",
          "moth to a flame", "why moths circle lights", "animal facts", "cute things kill here", "episode 3",
          "choose the ending"],
    pinned_comment="A or B? 🦋 A = go with Wren to the old lighthouse tonight. B = leave at sunrise, like the village "
                   "said. The letter in more comments within 48 hours of this video going up decides Episode 4.",
)
