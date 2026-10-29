"""tools/precheck.py EP...: Whisper medium on each voice take before the video is rendered (same scoring as check.py)."""
import difflib, importlib.util, os, re, sys
ROOT = "/home/user/Motion-graphics"
sys.path.insert(0, ROOT)
os.chdir(ROOT)
os.environ.setdefault("FPS", "24")
os.environ.setdefault("CLONE_RATE", "5.0")                    # as make_2d.py, so the takes land in the same cache
src = open("channels/horror/check.py").read()
exec(src[src.index("NUM = {"):src.index("\n\n\n", src.index("def norm"))])
import render
from motion import timeline
from faster_whisper import WhisperModel
import subprocess, imageio_ffmpeg
import numpy as np


def decode_audio(path, sampling_rate=16000):
    raw = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), '-v', 'quiet', '-i', path, '-ac', '1', '-ar', str(sampling_rate), '-f', 's16le', '-'], capture_output=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768
timeline.STOP_PAUSE, timeline.QUESTION_PAUSE, timeline.BEAT_GAP = 0.36, 0.45, 0.4
model = WhisperModel("medium.en", device="cpu", compute_type="int8")
for ep in sys.argv[1:]:
    home = 'stories' if os.path.exists(f'channels/stories/{ep}.py') else 'horror'
    spec = importlib.util.spec_from_file_location(f"videos.{ep}", f"channels/{home}/{ep}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[f"videos.{ep}"] = mod
    spec.loader.exec_module(mod)
    render.load(ep)
    tl = render.timeline()
    bad = 0
    print("==", ep, flush=True)
    for b in tl.beats:
        if isinstance(b.audio, np.ndarray):           # takes already in memory at voice.SR (44.1 kHz)
            from scipy.signal import resample_poly
            a = resample_poly(b.audio.astype(np.float32), 160, 441).astype(np.float32)
        else:
            a = decode_audio(b.audio, sampling_rate=16000)
        heard = " ".join(s.text for s in model.transcribe(a, language="en", beam_size=5)[0])
        ref, hyp = norm(b.text), norm(heard)
        r = difflib.SequenceMatcher(None, ref, hyp).ratio()
        bad += r < .9
        print(f"{'OK ' if r >= .9 else 'BAD'} {b.id:5s} {r:4.0%}  {heard.strip()}", flush=True)
    print(f"{len(tl.beats) - bad}/{len(tl.beats)} takes heard as written", flush=True)
