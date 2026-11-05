"""Whisper-free sanity check of each line's voice take (6 Nov 2026: Whisper medium is too weak in Kannada to judge
clarity on its own). For every line: duration, letters per second (Kannada/Devanagari letters only), loudness and the
longest inner pause. Flags takes that are too fast or slow for their text, near-silent, or with a long dead gap,
which is what a garbled or stalled IndicF5 take looks like.
Usage: python -I -X utf8 channels/mythology/audio_sanity.py <video> <lang>"""
import importlib.util, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import narrate  # noqa: E402
from channel import NARRATORS  # noqa: E402

name, lang = sys.argv[1], sys.argv[2]
spec = importlib.util.spec_from_file_location("v", os.path.join(HERE, "videos", f"{name}.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
cfg = NARRATORS[lang]
rows = []
for line in mod.SCRIPTS[lang]:
    a, _, wav = narrate.take(line["text"], cfg)
    letters = sum(1 for c in line["text"] if "ऀ" <= c <= "ॿ" or "ಀ" <= c <= "೿")
    dur = len(a) / narrate.SR
    hop = int(0.02 * narrate.SR)
    env = np.sqrt(np.convolve(a ** 2, np.ones(hop) / hop, mode="same"))[::hop]
    quiet = env < env.max() * 0.03
    gap, run = 0, 0
    for q in quiet:
        run = run + 1 if q else 0
        gap = max(gap, run)
    rows.append((line["id"], dur, letters / dur, float(np.sqrt((a ** 2).mean())), gap * 0.02))
cps = np.median([r[2] for r in rows])
for bid, dur, c, rms, gap in rows:
    flags = []
    if c < cps * 0.7:
        flags.append("SLOW (stretched or stalled?)")
    if c > cps * 1.35:
        flags.append("FAST (skipped words?)")
    if gap > 1.1:
        flags.append(f"GAP {gap:.1f}s")
    if rms < 0.03:
        flags.append("QUIET")
    print(f"{'!!' if flags else 'ok'} {bid:>5} {dur:5.1f}s {c:5.1f} letters/s rms {rms:.3f} gap {gap:.2f}s  "
          f"{' '.join(flags)}")
print(f"median {cps:.1f} letters/s")
