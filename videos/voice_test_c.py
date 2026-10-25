"""Voice test c (owner chose between C and D, 25 Oct 2026): the first lines of the snakebite explainer, voiced by
Chatterbox Turbo with the timbre of Kokoro am_puck. Not for upload."""
from videos import snakebite as _sb

NARRATOR = dict(turbo=True, turbo_ref="am_puck", rate=4.7, tempo_min=0.88)
STYLE = _sb.STYLE
MUSIC = _sb.MUSIC
TAIL = 0.8
SCRIPT = [dict(s) for s in _sb.SCRIPT[:5]]
draw = _sb.draw
