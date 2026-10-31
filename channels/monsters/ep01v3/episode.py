"""Cute Things Kill Here, Episode 1 v3 (2.5D diorama; owner approved the v3 script on 31 Oct 2026: "OK go ahead").
The spoken script, exactly as in out/monsters/story_v3_diorama.md, voiced as Turbo am_liam like v2: the lines kept
from v2 reuse its takes (assets/voice_cache/monsters_ep01v2_takes.tar), the new ones are voiced and Whisper-checked.

What v3 adds (the owner's notes on the v2 comparison):
- the lab accident told step by step: the panicked shrimp's snap cracks the tank, the water reaches the power cables,
  Kai is standing in it, "That's how I died.", and he wakes "In another world.";
- the shrimp aims at Kai and misses him by an inch, then tries to finish him;
- the butcher bird is looking at the shrimp, which has no idea;
- the A/B vote: "Option A ... Option B ... Comment A or B."

    SYNTH=1 EP=ep01v3 /home/user/.venv-main/bin/python channels/monsters/ep01v2_timing.py
        -> channels/monsters/ep01v3/timing.json and TIMING.md
"""

NARRATOR = dict(turbo=True, turbo_ref="am_liam")   # the same voice as v2: its cache keys need exactly this
TAIL = 0.35                                        # cut ~0.5 s after the last word
TWIST = "l18"                                      # the snap

SCRIPT = [
    dict(id="l1", scene="S01", text="Don't move. That claw can boil water."),
    dict(id="l2", scene="S02", text="Ten minutes ago, I was alive.", gap=0.4),
    dict(id="l3", scene="S03a", text="Night shift at the marine lab. Just me and the pistol shrimp.", gap=0.6),
    dict(id="l4", scene="S04", text="Its claw snaps so fast, the water boils.", gap=0.5),
    dict(id="l5", scene="S05a", text="Almost as hot as the surface of the sun. But only in water.", gap=0.5),
    dict(id="l6", scene="S06", text="Then the storm hit.", gap=0.7),
    dict(id="l7", scene="S07", text="The shrimp panicked. Its snap cracked the tank.", gap=0.5),
    dict(id="l8", scene="S08", text="Water poured off the desk, straight into the power cables.", gap=0.5),
    dict(id="l9", scene="S08a", text="And I was standing in it.", gap=0.5),
    dict(id="l10", scene="S08b", text="That's how I died.", gap=0.6),
    dict(id="l11", scene="S09", text="Then I woke up. In another world.", gap=1.4),   # black, flatline, the soul falls
    dict(id="l12", scene="S10a", text="Everything here was tiny. And cute.", gap=0.5),
    dict(id="l13", scene="S11a", text="And every one of them was wrong.", gap=0.4),
    dict(id="l14", scene="S12", text="I was so thirsty.", gap=0.7),
    dict(id="l15", scene="S13", text="Something else was already drinking.", gap=0.5),
    dict(id="l16", scene="S14", text="A shrimp. On land. Impossible.", gap=0.6),
    dict(id="l17", scene="S15a", text="Then it looked right at me.", gap=0.5),
    dict(id="l18", scene="S15", text="", hold=4.0, gap=0.4),          # THE SNAP: no words
    dict(id="l19", scene="S15b", text="It missed me by an inch.", gap=0.4),
    dict(id="l20", scene="S16", text="When I opened my eyes, it was on my chest.", gap=0.8),
    dict(id="l21", scene="S17", text="Then I saw the drops.", gap=0.5),
    dict(id="l22", scene="S18", text="Its claw only works wet.", gap=0.5),
    dict(id="l23", scene="S19", text="So I didn't move. I let the sun dry it.", gap=0.6),
    dict(id="l24", scene="S20", text="It tried to finish me anyway.", gap=1.7),    # the drop shrinks away in silence
    dict(id="l25", scene="S21", text="Then it stomped back to the puddle.", gap=2.9),   # pff, the stare, deadpan
    dict(id="l26", scene="S22", text="That's when I saw the thorn tree.", gap=0.6),
    dict(id="l27", scene="S23", text="A butcher bird hangs its food on thorns.", gap=0.5),
    dict(id="l28", scene="S23b", text="And it was looking at the shrimp.", gap=0.5),
    dict(id="l29", scene="S23c", text="The shrimp had no idea.", gap=0.5),
    dict(id="l30", scene="S24", text="Option A: save the shrimp that tried to kill me. Option B: run while I can. "
                                     "Comment A or B.", gap=0.8),
]

# Shots that split one line: (shot, line, the word the second shot opens on)
SPLITS = [("S03b", "l3", "Just"), ("S05b", "l5", "But"), ("S10b", "l12", "And"), ("S11b", "l13", "was")]

# The upload sheet (story_v2.md "Packaging"; report TP16: no Pokémon terms in the title, thumbnail or tags).
# Audience: NOT made for kids (comments stay on for the vote). Fully animated fantasy: no altered-content disclosure
# (report TP15). Music and effects are original (SS9).
METADATA = dict(
    title="I Died Because of a Shrimp. Then I Woke Up Here 🦐",
    alt_titles=["This Shrimp Erased a Forest. It Was Sitting on My Chest 🦐",
                "Reborn in a World Where Cute Things Kill 🦐"],
    description="""A marine-biology student dies in a lab accident during a storm, and wakes up under a cracked sky in
a world of tiny, adorable creatures. Every one of them has a real animal's power.

His only weapon is what he knows.

Cute Things Kill Here, Episode 1.
Comment A to SAVE the shrimp that tried to kill him, or B to RUN. The letter in more comments decides Episode 2.

The real facts:
- A pistol shrimp snaps its claw so fast it makes a collapsing bubble that briefly reaches about 4,700 °C, against
  about 5,500 °C at the surface of the sun, and it only forms in water (Lohse et al., Nature 2001; Versluis et al.,
  Science 2000).
- Shrikes, the "butcher birds", impale their prey on thorns to store it.

Original story and animation. The creatures and the world are fictional.
Hero base model: Seed-san by VirtualCast, Inc. (VRM Public License 1.0)""",
    hashtags=["#anime", "#isekai", "#Shorts"],
    tags=["original anime", "isekai", "reincarnated", "anime short", "2.5d anime", "cute monsters", "pistol shrimp",
          "butcher bird", "shrike", "animal facts", "cute things kill here", "episode 1", "choose the ending"],
    pinned_comment="A or B? 🦐 A = save the shrimp that tried to kill him. B = run while he can. The letter in more "
                   "comments within 48 hours of this video going up decides Episode 2.",
)
