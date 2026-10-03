import sys, re, difflib; sys.path.insert(0, ".")
import numpy as np, render
from motion import voice
from faster_whisper import WhisperModel
m = WhisperModel("medium.en", device="cpu", compute_type="int8")
NUM = set("zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy eighty ninety hundred thousand million percent point".split())
def toks(s): return re.sub(r"[^a-z0-9' ]", " ", s.lower().replace("-", " ")).split()
for v in sys.argv[1:]:
    render._tl.clear(); render.load(v); tl = render.timeline()
    bad = 0
    for b in tl.beats:
        a = np.concatenate([np.zeros(int(0.6 * voice.SR)), b.audio, np.zeros(int(0.6 * voice.SR))])
        a16 = np.interp(np.arange(int(len(a)*16000/voice.SR))*voice.SR/16000, np.arange(len(a)), a).astype(np.float32)
        heard = " ".join(s.text.strip() for s in m.transcribe(a16, language="en", beam_size=5)[0])
        A, H = toks(b.spoken_text), toks(heard)
        issues = []
        for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, H).get_opcodes():
            if op == "equal": continue
            said, got = A[i1:i2], H[j1:j2]
            if all(w in NUM or w in ("and", "a") for w in said) and all(re.fullmatch(r"[0-9%.,]+|and|a", w) for w in got): continue
            issues.append(f"{' '.join(said)!r}->{' '.join(got)!r}")
        if issues:
            bad += 1
            print(f"  {v}:{b.id}: {'; '.join(issues)}   [{heard}]", flush=True)
    print(f"{v}: {len(tl.beats)} lines, {bad} flagged, {tl.total:.1f}s", flush=True)
