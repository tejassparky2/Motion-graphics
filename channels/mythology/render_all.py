"""Render, check and finish videos in both languages, one after another (the night's batch, 6 Nov 2026).

  python -I -X utf8 channels/mythology/render_all.py kakudmi:1 brahma_calves:2 jarasandha:3 [--langs hi,kn]

For each video and language: render_myth (master), render_myth --check (Whisper medium per line, logged), then
finish.py (cover, phone copy, upload pack, Drive). Logs go to myth_out/render_all.log."""
import os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
from channel import OUT_ROOT  # noqa: E402

PY = sys.executable
langs = sys.argv[sys.argv.index("--langs") + 1].split(",") if "--langs" in sys.argv else ["hi", "kn"]
env = dict(os.environ)
env.pop("MYTH_DRY", None)


def run(args, log):
    t = time.time()
    log.write(f"\n$ {' '.join(args)}\n")
    log.flush()
    r = subprocess.run([PY, "-I", "-X", "utf8", *args], stdout=log, stderr=subprocess.STDOUT, env=env)
    log.write(f"-> exit {r.returncode} in {time.time() - t:.0f} s\n")
    log.flush()
    return r.returncode


def video_format(name):
    """'landscape' for a long video whose module says FORMAT = "landscape" (poster.py reads MYTH_FORMAT)."""
    src = open(os.path.join(HERE, "videos", f"{name}.py"), encoding="utf-8").read()
    return "landscape" if 'FORMAT = "landscape"' in src else "portrait"


with open(os.path.join(OUT_ROOT, "render_all.log"), "a", encoding="utf-8") as log:
    for item in [a for a in sys.argv[1:] if ":" in a]:
        name, n = item.split(":")
        env["MYTH_FORMAT"] = video_format(name)
        for lang in langs:
            print(f"render {name} {lang}", flush=True)
            if run([os.path.join(HERE, "render_myth.py"), "--video", name, "--lang", lang], log):
                print(f"FAILED render {name} {lang}", flush=True)
                continue
            if lang != "kn":   # Whisper medium can't judge Kannada (kn_asr_check.py with turbo does) and it hogs the GPU
                run([os.path.join(HERE, "render_myth.py"), "--video", name, "--lang", lang, "--check"], log)
            if run([os.path.join(HERE, "finish.py"), name, lang, n], log):
                print(f"FAILED finish {name} {lang}", flush=True)
            else:
                print(f"done {name} {lang}", flush=True)
print("ALL DONE", flush=True)
