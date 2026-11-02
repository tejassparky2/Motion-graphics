"""Cute Things Kill Here, Episode 2: "I Saved the Shrimp That Tried to Kill Me" (2.5D diorama, like Episode 1 v3).

The viewers voted A on Episode 1 ("Most said to save the shrimp", owner, 1 Nov 2026). The owner approved this script
on 1 Nov 2026 ("OK go ahead"). It follows the 2A "SAVE" outline in out/monsters/story_v2.md: Kai saves the shrimp
with one real fact (a pistol shrimp's snap fires straight ahead), pays a small cost (the talons scratch his arm), the
first bond forms (the nose-tap and the glowing wrist mark), the sky-crack clue, then Wren and the bells, and the A/B.

    SYNTH=1 EP=ep02 /home/user/.venv-main/bin/python channels/monsters/ep01v2_timing.py
        -> channels/monsters/ep02/timing.json and TIMING.md (voices the lines, Turbo; Whisper medium.en after)
"""
from motion import voice

NARRATOR = dict(turbo=True, turbo_ref="am_liam")   # Kai: the same voice as Episode 1
# Wren, the village bell-keeper: her own Turbo voice from a Kokoro clip (synthetic; nobody real is cloned).
voice.SPEAKERS["wren"] = dict(voice="af_sky", turbo_ref="af_sky+5")
TAIL = 0.35                                        # cut ~0.5 s after the last word
TWIST = "l9"                                       # the snap: the music drops under it

SCRIPT = [
    dict(id="l1", scene="S01", text="You said save it. So I ran at the butcher bird."),
    dict(id="l2", scene="S02", text="The bird struck first.", gap=0.4),   # was "It dove first." / "The bird dived first." (heard "doe", then "died" in the mix)
    dict(id="l3", scene="S03", text="I got there half a second sooner.", gap=0.4),
    dict(id="l4", scene="S04", text="Its talons got my arm instead.", gap=0.5),
    dict(id="l5", scene="S05", text="Now I was holding a wet pistol shrimp. In my bare hands.", gap=0.7),
    dict(id="l6", scene="S06", text="But a pistol shrimp only fires one way. Straight ahead.", gap=0.6),
    dict(id="l7", scene="S07", text="So I turned it around.", gap=0.5),
    dict(id="l8", scene="S08", text="They don't call it a pistol shrimp for nothing.", gap=0.5),
    dict(id="l9", scene="S09", text="", hold=3.0, gap=0.6),          # THE SNAP: a held wind-up, impact frames, no words
    dict(id="l10", scene="S10", text="The bird landed in the thorn bush.", gap=0.4),
    dict(id="l11", scene="S11", text="Alive. Just very, very fluffed.", gap=0.6),
    dict(id="l12", scene="S12", text="Then the shrimp looked at me.", gap=2.0),       # the puffball stomps off (laugh)
    dict(id="l13", scene="S13", text="And tapped my nose.", gap=1.0),                # a second of silence: will it?
    dict(id="l14", scene="S14", text="Something on my wrist started to glow.", gap=1.0),   # Kai's stunned dot eyes
    dict(id="l15", scene="S15", text="The same shape as the crack in the sky.", gap=0.5),
    dict(id="l16", scene="S16", text="Then came the bells.", gap=0.9),   # was "Then the bells started." (Whisper heard "the bell started")
    dict(id="l17", scene="S17", text="A girl with a bell marched right up to me.", gap=0.5),   # was "walked straight" (heard "walks")
    dict(id="l18", scene="S18", text="Step away from the snapper. It goes in the lake.", gap=0.5,
         speaker="wren", speaker_from="Step"),
    dict(id="l19", scene="S19", text="The lake. Deep water. Where a pistol shrimp never runs dry.", gap=0.7),
    dict(id="l20", scene="S20", text="Option A: hand it over. Option B: show her the glowing mark. Comment A or B.",
         gap=0.8),   # owner, 2 Nov: B was "hide it in my shirt" (impossible with Wren face to face)
]

SPLITS = []        # (shot, line, the word the second shot opens on): none yet

# The upload sheet. Audience: NOT made for kids (comments stay on for the vote). Fully animated fantasy: no
# altered-content disclosure. Music and effects are original.
METADATA = dict(
    title="I Saved the Shrimp That Tried to Kill Me 🦐",
    alt_titles=["You Voted SAVE. So I Ran at the Butcher Bird 🦐",
                "I Turned a Pistol Shrimp Into an Actual Pistol 🦐"],
    description="""You voted A, so Kai saved the shrimp that tried to kill him. With his bare hands, against a butcher bird.

His only weapon is still what he knows.

Cute Things Kill Here, Episode 2.
Comment A to HAND the shrimp over, or B to SHOW her the glowing mark. The letter in more comments decides Episode 3.

The real fact:
- A pistol shrimp's claw shoots a fast jet of water straight forward, and that jet makes the bubble that snaps
  (Versluis et al., Science 2000). It only fires one way: straight ahead.

Original story and animation. The creatures and the world are fictional.
Hero base model: Seed-san by VirtualCast, Inc. (VRM Public License 1.0)""",
    hashtags=["#anime", "#isekai", "#Shorts"],
    tags=["original anime", "isekai", "reincarnated", "anime short", "2.5d anime", "cute monsters", "pistol shrimp",
          "butcher bird", "shrike", "animal facts", "cute things kill here", "episode 2", "choose the ending"],
    pinned_comment="A or B? 🦐 A = hand the shrimp over to Wren. B = show her the glowing mark. The letter in more comments "
                   "within 48 hours of this video going up decides Episode 3.",
)
