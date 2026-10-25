"""Voice test O (owner, 25 Oct 2026: "this seems like pure AI voice, no human touch"): the first lines of the
snakebite explainer voiced by Orpheus TTS, stock voice "leo", at its own natural pace. Not for upload."""
from videos import snakebite as _sb

NARRATOR = dict(orpheus="leo", tempo_min=1.0, tempo_max=1.0)
STYLE = _sb.STYLE
MUSIC = _sb.MUSIC
TAIL = 0.8
SCRIPT = [dict(s, text=s["text"].replace("[dramatic] ", "")) for s in _sb.SCRIPT[:5]]
draw = _sb.draw
