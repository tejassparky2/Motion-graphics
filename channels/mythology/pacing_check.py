"""Pacing check for a finished reel (owner, 14 Nov 2026: "the same shot is still for many seconds and video feels
slow"): finds every stretch where the picture barely changes, and the cuts.

  python -I -X utf8 channels/mythology/pacing_check.py <video.mp4> [--max-still 2.0]

The video is read at 6 frames a second, 108x192 grey. A "visible change" is a frame whose mean difference from the
frame half a second before is above CHANGE (a cut, a new figure, a label, a big move: the puppets' idle sway and the
lamp flicker stay below it); a cut is a jump between consecutive frames above CUT. It prints the longest stretches
with no visible change, the cut count and the average time between cuts, and exits with 1 if any stretch is longer
than --max-still seconds (default 2.0).
"""
import subprocess
import sys

import numpy as np

FPS = 6
W, H = 108, 192
CHANGE = 4.0          # mean |difference| (0-255) against the frame 0.5 s earlier
CUT = 7.0             # mean |difference| between consecutive frames: a cut or a camera punch-in (a new framing)
MAX_HOLD = 3.0        # longest a framing may be held (the camera_beats aim is 2.6 s)


def frames(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-vf", f"fps={FPS},scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W).astype(np.float32)


def main():
    path = sys.argv[1]
    max_still = float(sys.argv[sys.argv.index("--max-still") + 1]) if "--max-still" in sys.argv else 2.0
    f = frames(path)
    lag = FPS // 2
    change = np.zeros(len(f), bool)
    for i in range(lag, len(f)):
        change[i] = np.abs(f[i] - f[i - lag]).mean() > CHANGE
    step = np.r_[0, np.abs(np.diff(f, axis=0)).mean(axis=(1, 2))]
    cuts = np.where(step > CUT)[0] / FPS
    still, i = [], 0
    while i < len(f):
        if not change[i]:
            j = i
            while j < len(f) and not change[j]:
                j += 1
            still.append(((j - i) / FPS, i / FPS))
            i = j
        else:
            i += 1
    still.sort(reverse=True)
    dur = len(f) / FPS
    print(f"{path}: {dur:.1f} s, {len(cuts)} cuts (one every {dur / max(1, len(cuts)):.1f} s), "
          f"changing {change.mean() * 100:.0f}% of the time")
    print("longest still stretches (seconds, starting at):")
    for d, s in still[:8]:
        print(f"  {d:4.1f} s at {int(s // 60)}:{s % 60:04.1f}")
    bad = [x for x in still if x[0] > max_still]
    print(f"{len(bad)} still stretch(es) longer than {max_still} s")
    holds = np.diff(np.r_[0.0, cuts, dur])
    starts = np.r_[0.0, cuts]
    order = np.argsort(-holds)[:6]
    print("longest held framings: " + ", ".join(f"{holds[k]:.1f} s at {int(starts[k] // 60)}:{starts[k] % 60:04.1f}"
                                                for k in order))
    long_holds = int((holds > MAX_HOLD).sum())
    print(f"{long_holds} framing(s) held longer than {MAX_HOLD} s")
    sys.exit(1 if bad or long_holds else 0)


if __name__ == "__main__":
    main()
