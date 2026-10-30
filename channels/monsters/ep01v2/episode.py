"""Cute Things Kill Here, Episode 1 (v2, approved by the owner 30 Oct 2026): "I Died Because of a Shrimp".
The spoken script, exactly as in out/monsters/story_v2.md (column 2), voiced by the render helper as Turbo am_liam
(assets/voice_cache/monsters_ep01v2_takes.tar, Whisper medium heard all 23 lines as written).

`scene` is the shot the line opens on. Gaps are the silence before a line: they give the picture room where the shot
list holds a moment without words (the snap, the drying sun, the deadpan reaction). Exact times per shot:
    python3 channels/monsters/ep01v2_timing.py     -> channels/monsters/ep01v2/timing.json and TIMING.md
"""

NARRATOR = dict(turbo=True, turbo_ref="am_liam")   # Kai tells it; the cache keys need exactly this
TAIL = 0.35                                        # the take ends ~0.15 s after its last word: cut ~0.5 s after it
TWIST = "l15"

SCRIPT = [
    dict(id="l1", scene="S01", text="Don't move. That claw can boil water."),
    dict(id="l2", scene="S02", text="Ten minutes ago, I was alive.", gap=0.4),
    dict(id="l3", scene="S03a", text="Night shift at the marine lab. Just me and the pistol shrimp.", gap=0.6),
    dict(id="l4", scene="S04", text="Its claw snaps so fast, the water boils.", gap=0.5),
    dict(id="l5", scene="S05a", text="Almost as hot as the surface of the sun. But only in water.", gap=0.5),
    dict(id="l6", scene="S06", text="Then the storm hit.", gap=0.7),
    dict(id="l7", scene="S07", text="Snap.", gap=0.5),
    dict(id="l8", scene="S08", text="Water. Cables. Me.", gap=0.6),
    dict(id="l9", scene="S09", text="I woke up under a cracked sky.", gap=1.1),
    dict(id="l10", scene="S10a", text="Everything here was tiny. And cute.", gap=0.5),
    dict(id="l11", scene="S11a", text="And every one of them was wrong.", gap=0.4),
    dict(id="l12", scene="S12", text="I was so thirsty.", gap=0.7),
    dict(id="l13", scene="S13", text="Something else was already drinking.", gap=0.5),
    dict(id="l14", scene="S14", text="A shrimp. On land. Impossible.", gap=0.6),
    dict(id="l15", scene="S15", text="", hold=4.0, gap=0.4),          # THE SNAP: no words
    dict(id="l16", scene="S16", text="When I opened my eyes, it was on my chest.", gap=0.8),
    dict(id="l17", scene="S17", text="Then I saw the drops.", gap=0.5),
    dict(id="l18", scene="S18", text="Its claw only works wet.", gap=0.5),
    dict(id="l19", scene="S19", text="So I didn't move. I let the sun dry it.", gap=0.6),
    dict(id="l20", scene="S20", text="It tried anyway.", gap=1.7),       # the drop shrinks away in silence (SG14)
    dict(id="l21", scene="S21", text="Then it stomped back to the puddle.", gap=2.9),   # pff, the stare, deadpan 2 s
    dict(id="l22", scene="S22", text="That's when I saw the thorn tree.", gap=0.6),
    dict(id="l23", scene="S23", text="A butcher bird hangs its food on thorns.", gap=0.5),
    dict(id="l24", scene="S24", text="Save the shrimp that tried to kill me, or run while I can?", gap=0.8),
]

# Shots that split one line: (shot, line, the word the second shot opens on)
SPLITS = [("S03b", "l3", "Just"), ("S05b", "l5", "But"), ("S10b", "l10", "And"), ("S11b", "l11", "was")]
