import re, sys, difflib, subprocess, importlib, imageio_ffmpeg
from faster_whisper import WhisperModel
name = sys.argv[1]
mod = importlib.import_module(f"videos.{name}")
f = f"out/{name}.mp4"
def norm(s):
    s = re.sub(r"\[([^|\]]*)\|[^\]]*\]", r"\1", s).lower().replace("-", " ")
    return re.findall(r"[a-z0-9']+", s)
ref = norm(" ".join(b["text"] for b in mod.SCRIPT))
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(f, language="en")
hyp = norm(" ".join(s.text for s in segs))
num = {"1":"one","2":"two","3":"three","4":"four","6":"six","10":"ten","38":"thirty eight","1896":"eighteen ninety six",
       "9":"nine","40":"forty","100":"a hundred","1957":"nineteen fifty seven","29":"twenty nine","30":"thirty"}
hyp = " ".join(num.get(w, w) for w in hyp).split()
sm = difflib.SequenceMatcher(None, ref, hyp)
print("ASR match %.1f%%" % (100 * sm.ratio()))
for op, a, b, c, d in sm.get_opcodes():
    if op != "equal": print(" ", op, ref[a:b], hyp[c:d])
ff = imageio_ffmpeg.get_ffmpeg_exe()
_h, _m, _s = re.search(r"Duration: (\d+):(\d+):([\d.]+)", subprocess.run([ff, "-i", f], capture_output=True, text=True).stderr).groups()
dur = int(_h) * 3600 + int(_m) * 60 + float(_s)
o = subprocess.run([ff, "-i", f, "-vf", "select='gt(scene,0.08)',showinfo", "-f", "null", "-"], capture_output=True, text=True).stderr
ts = [0.0] + [float(x) for x in re.findall(r"pts_time:([\d.]+)", o)] + [dur]
gaps = [b - a for a, b in zip(ts, ts[1:])]
print("visual changes %d, avg every %.2fs, longest %.2fs" % (len(ts) - 2, sum(gaps) / len(gaps), max(gaps)))
print("  >2s:", [(round(a, 1), round(b - a, 1)) for a, b in zip(ts, ts[1:]) if b - a > 2])
data = open(f, "rb").read() + open(f"out/{name}_preview.mp4", "rb").read()
print("strings:", {s: data.count(s.encode()) for s in ["x264", "Lavf", "Lavc", "c2pa", "jumb", "synthid", "SynthID", "watermark"]})
