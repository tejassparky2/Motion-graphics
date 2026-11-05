"""Voice every line of the given videos in both languages, then run the clarity retakes, one GPU job at a time.
Waits while another program holds more than MAX_BUSY MiB of GPU memory (owner, 6 Nov 2026: another session also
uses the GPU; run only when it is free).
Usage: python -I -X utf8 channels/mythology/voice_all.py kakudmi brahma_calves jarasandha"""
import importlib.util, os, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
import narrate  # noqa: E402
from channel import LANGS, NARRATORS  # noqa: E402

PY = sys.executable
MAX_BUSY = 600


def gpu_used():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
                             capture_output=True, text=True).stdout
        return int(out.strip().splitlines()[0])
    except Exception:
        return 0


def wait_gpu():
    while (u := gpu_used()) > MAX_BUSY:
        print(f"GPU busy ({u} MiB), waiting", flush=True)
        time.sleep(60)


def load(name):
    spec = importlib.util.spec_from_file_location(f"v_{name}", os.path.join(HERE, "videos", f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


for lang in LANGS:                     # one IndicF5 load per language: all lines of all videos in one batch
    jobs = []
    for name in sys.argv[1:]:
        jobs += [l for l in load(name).SCRIPTS[lang]]
    wait_gpu()
    print(f"voicing {len(jobs)} {lang} lines", flush=True)
    narrate.prefetch(jobs, NARRATORS[lang])
for name in sys.argv[1:]:
    for lang in LANGS:
        wait_gpu()
        print(f"retakes {name} {lang}", flush=True)
        subprocess.run([PY, "-I", "-X", "utf8", os.path.join(HERE, "retake.py"), name, lang])
print("VOICES DONE", flush=True)
