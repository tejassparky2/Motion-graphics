"""export_takes.py EP OUT.tar: build EP's timeline (all takes must already be cached) and pack every file it reads
under build/ (voice takes, turbo refs, processed clips) into OUT.tar, paths relative to the repo root."""
import importlib.util
import os
import sys
import tarfile

ROOT = "/home/user/Motion-graphics"
sys.path.insert(0, ROOT)
os.chdir(ROOT)
os.environ.setdefault("CLONE_RATE", "5.0")
os.environ.setdefault("FPS", "24")
ep, out = sys.argv[1], sys.argv[2]
if ep.endswith("_long"):
    os.environ["CANVAS"] = "landscape"
used = set()
build = os.path.join(ROOT, "build") + os.sep


def hook(event, args):
    if event == "open" and args and isinstance(args[0], str):
        p = os.path.abspath(args[0])
        if p.startswith(build) and os.path.isfile(p):
            used.add(p)


from motion import timeline  # noqa: E402
import render  # noqa: E402
timeline.STOP_PAUSE, timeline.QUESTION_PAUSE, timeline.BEAT_GAP = 0.36, 0.45, 0.4
home = "stories" if os.path.exists(f"channels/stories/{ep}.py") else "horror"
spec = importlib.util.spec_from_file_location(f"videos.{ep}", f"channels/{home}/{ep}.py")
mod = importlib.util.module_from_spec(spec)
sys.modules[f"videos.{ep}"] = mod
spec.loader.exec_module(mod)
render.load(ep)
sys.addaudithook(hook)
_exists = os.path.exists


def exists(p):                                                # cached files are found with os.path.exists...
    ok = _exists(p)
    if ok and isinstance(p, str):
        hook("open", (p,))
    return ok


os.path.exists = exists
import soundfile  # noqa: E402
_read = soundfile.read


def read(p, *a, **k):                                         # ...and read with soundfile (C-level, not audited)
    if isinstance(p, str):
        hook("open", (p,))
    return _read(p, *a, **k)


soundfile.read = read
tl = render.timeline()
for p in list(used):                                          # each take's ".ok" marker travels with it
    if os.path.exists(p + ".ok"):
        used.add(p + ".ok")
with tarfile.open(out, "w") as tar:
    for p in sorted(used):
        if "/jobs_" in p:
            continue
        tar.add(p, arcname=os.path.relpath(p, ROOT))
print(f"{len(tl.beats)} beats, {tl.total:.1f} s; packed {len(used)} files -> {out}", flush=True)
