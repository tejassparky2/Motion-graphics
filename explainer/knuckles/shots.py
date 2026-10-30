"""Shot list and timing for "What happens when you crack your knuckles?" (seconds).

Narration timings come from voice.py (Kokoro TTS, words.json).
"""
FPS = 24
DURATION = 16.0

SHOTS = [
    # name, start, end, what we see
    ('crack', 0.0, 3.55),     # medium shot: fist into palm, CRACK on "knuckles"
    ('xray', 3.55, 5.75),     # close-up on the open hand, fades to x-ray, joints glow on "fluid"
    ('joint', 5.75, 10.55),   # cutaway of a knuckle: bones pull apart, gas bubble pops into being
    ('smile', 10.55, 12.1),   # close-up: satisfied grin on "That's the pop!"
    ('again', 12.1, 16.0),    # medium shot: tries again, nothing happens, "20 minutes"
]

CRACK_T = 2.55        # first knuckle crack (sound + jolt)
XRAY_T = (3.85, 4.35)  # skin fades to x-ray
FLUID_T = 5.05        # joints glow on "fluid"
PULL_T = (5.95, 6.9)  # "pull them apart"
PRESSURE_T = (7.6, 9.2)
BUBBLE_T = 9.85       # "suddenly" -> bubble forms
TIMER_T = 13.95       # "twenty minutes"


def frame(t):
    return 1 + round(t * FPS)
