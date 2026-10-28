"""After a render: hear every line of the finished video with Whisper medium and list any line whose words don't
match the script (merged or misheard words get reworded and re-rendered), then check the files carry no encoder or
metadata tags.

    /home/user/.venv-main/bin/python channels/horror/check.py EPISODE
"""
import difflib
import json
import os
import re
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
import imageio_ffmpeg   # noqa: E402
from faster_whisper import WhisperModel   # noqa: E402

ep = sys.argv[1]
home = next(d for d in ("horror", "stories") if os.path.exists(os.path.join(ROOT, "channels", d, f"{ep}.py")))
video = os.path.join(ROOT, "out", home, f"{ep}.mp4")
timing = json.load(open(os.path.join(ROOT, "build", home, f"timing_{ep}.json")))
twin = os.path.join(ROOT, "channels", home, f"{ep.removesuffix('_2d')}.py")       # 2D cuts reuse the 3D script
src = open(twin if os.path.exists(twin) else os.path.join(ROOT, "channels", home, f"{ep}.py")).read()
texts = dict(re.findall(r'dict\(id="(\w+)", scene="\w+", text="((?:[^"]|"\s*\n\s*")*)"', src))
if not texts:                                    # scripts built in code (the manga episodes): import the episode
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"videos.{ep}", os.path.join(ROOT, "channels", home, f"{ep}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    texts = {b["id"]: b["text"] for b in mod.SCRIPT}
NUM = {"2": "two", "9": "nine", "13": "thirteen", "3": "three", "14": "fourteen", "6": "six", "4": "four",
       "40": "forty", "44": "forty four", "414": "four fourteen", "440": "four forty", "444": "four forty four", "30": "thirty", "41": "forty one",
       "10": "ten", "210": "two ten", "1": "one", "5": "five", "7": "seven", "900": "nine",
       "1217": "twelve seventeen", "3b": "three b", "0": "zero", "20": "twenty", "100": "a hundred", "912": "nine twelve", "12": "twelve",
       "16": "sixteen", "59": "fifty nine", "18": "eighteen", "19": "nineteen", "31": "thirty one", "69": "sixty nine",
       "70": "seventy", "17": "seventeen", "459": "four fifty nine", "458": "four fifty eight", "00": "zero zero"}
SAME = {"grey": "gray", "meter": "metre", "meters": "metres", "mrs": "mrs", "keyring": "key ring",
        "wylie": "wiley", "wily": "wiley", "wanna": "want to", "eyeholes": "eye holes", "too": "two",
        "harito": "haruto", "koda": "kota", "coda": "kota",             # Whisper's spellings of the DMA names
        "wren": "ren", "tiktok": "tick tock", "realize": "realise", "curb": "kerb", "mr": "mister", "ohh": "oh",
        "logbook": "log book", "it's": "its"}


def norm(s):
    s = re.sub(r'"\s*\n\s*"', "", s)
    s = re.sub(r"\[([^|\]]*)\|[^\]]*\]", r"\1", s)
    s = re.sub(r"\[[a-z ]+\]", " ", s).lower().replace("-", " ")
    return [x for w in re.findall(r"[a-z0-9']+", s) for x in SAME.get(NUM.get(w, w), NUM.get(w, w)).split()]


pcm = subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(), "-v", "error", "-i", video, "-ac", "1", "-ar", "16000", "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
audio = np.frombuffer(pcm, np.int16).astype(np.float32) / 32768
model = WhisperModel("medium.en", device="cpu", compute_type="int8")
bad = 0
for b in timing["beats"]:
    a = audio[max(0, int((b["start"] - .3) * 16000)): int((b["end"] + .15) * 16000)]
    heard = " ".join(s.text for s in model.transcribe(a, language="en", beam_size=5)[0])
    ref, hyp = norm(texts.get(b["id"], "")), norm(heard)
    r = difflib.SequenceMatcher(None, ref, hyp).ratio()
    flag = "OK " if r >= .9 else "BAD"
    bad += r < .9
    print(f"{flag} {b['id']:5s} {r:4.0%}  {heard.strip()}")
print(f"\n{len(timing['beats']) - bad}/{len(timing['beats'])} lines heard as written (Whisper medium)")
data = open(video, "rb").read() + open(video[:-4] + "_preview.mp4", "rb").read()
print("tags:", {s: data.count(s.encode()) for s in ["x264", "Lavf", "Lavc", "encoder", "c2pa", "jumb"]})
