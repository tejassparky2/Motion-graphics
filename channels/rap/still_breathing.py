"""Still Breathing: Short cut = Hook + Verse 1 (16 bars), loops cleanly back into the hook.

Beat grid measured from the owner's Gemini audio: 90 BPM, first beat at 0.078 s; the hook starts on beat 16.
"""
BPM = 90.0
PHASE = 0.0778
START_BEAT = 16          # 10.75 s, half a beat before "They buried my name"
BEATS = 64               # 16 bars = 42.7 s, ends after "climb it alone"

# (lyric line with marks, shots cycled every 2 beats while the line plays)
LINES = [
    ("They *buried my *name, but I'm still !breathing",
     [("slab", "fill"), ("slab", "red"), ("breath", "fill"), ("breath", "red")]),
    ("Every *scar on my *chest got a !reason",
     [("scar", "fill"), ("scar", "close"), ("scar", "red"), ("eye", "redline")]),
    ("Fell *down nine *times, got *up on !ten",
     [("fall", "fill"), ("fall", "red"), ("reach", "fill"), ("reach", "red")]),
    ("Still *breathing, still *breathing, and I'm !rising again",
     [("breath", "red"), ("breath", "close"), ("sunrise", "fill"), ("sunrise", "red")]),
    ("*Cold room, no *light, just me and my !doubt", [("bulb", "fill"), ("eye", "close")]),
    ("Mama keeps *asking why I *never go *out", [("door", "fill"), ("door", "close")]),
    ("*Phone so *quiet, got no one to *call", [("phone", "fill"), ("phone", "close")]),
    ("Wrote my *whole life down on a !cracked bedroom *wall", [("chalk", "fill"), ("chalk", "line")]),
    ("They *said I was *nothing, said I'd *never be", [("pointers", "fill"), ("pointers", "red")]),
    ("Funny how the !nothing kept on *staring at me", [("mirror", "fill"), ("mirror", "redline")]),
    ("Every *no that they *gave me, I kept it like !stone", [("fist", "fill"), ("fist", "close")]),
    ("Built me a *staircase, now I *climb it !alone", [("stairs", "fill"), ("stairs", "red")]),
]
ANCHORS = ["top", "mid", "top", "mid", "mid", "top", "mid", "top", "top", "mid", "top", "mid"]
LINES_LEFT = [True, False]
DIP_FROM = 5            # verse lines (after the first) open with a 3-frame dip to black

# where the "close" variant crops in, per scene
FOCUS = dict(eye=(540, 940), bulb=(540, 1050), door=(760, 860), phone=(540, 1000), chalk=(500, 700),
             pointers=(540, 800), mirror=(540, 800), fist=(540, 1050), stairs=(540, 1100), slab=(540, 1000),
             breath=(640, 1000), scar=(560, 980), fall=(540, 1250), reach=(470, 950), sunrise=(540, 1100))
