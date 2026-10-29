"""Measure the tonal balance of a reference narration and of our voice, and save the EQ that moves ours toward it.

Long-term average spectrum over speech frames only (frames where the voice band dominates, so the reference's
quiet music bed counts for little), in 1/3-octave bands from 150 Hz to 12 kHz, each normalised to its own 1 kHz
level. The difference (reference - ours), smoothed and clamped to +-8 dB, is written as ffmpeg firequalizer
entries for narrate.py's studio chain. Below 150 Hz the reference is mixed with the music bed, so no matching is
attempted there (the chain uses a fixed high-pass instead).

Usage: python -I -X utf8 channels/hinglish/voice_match.py <out_json> --ref ref1.mp4 ref2.mp4 ... --ours a.wav b.wav ...
"""
import json, subprocess, sys
import numpy as np

SR = 44100
BANDS = [150 * 2 ** (k / 3) for k in range(int(3 * np.log2(12000 / 150)) + 1)]


def load(path, start=0, dur=None):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start)] + (["-t", str(dur)] if dur else []) + ["-i", path, "-ac", "1",
                                                                                             "-ar", str(SR), "-f", "f32le", "-"]
    return np.frombuffer(subprocess.run(cmd, capture_output=True, check=True).stdout, np.float32).astype(np.float64)


def ltas(signals):
    n = 4096
    win = np.hanning(n)
    freqs = np.fft.rfftfreq(n, 1 / SR)
    acc, count = np.zeros(len(freqs)), 0
    for y in signals:
        frames = np.lib.stride_tricks.sliding_window_view(y, n)[::n // 2]
        spec = np.abs(np.fft.rfft(frames * win, axis=1)) ** 2
        voice = spec[:, (freqs > 300) & (freqs < 3400)].sum(axis=1)
        low = spec[:, (freqs > 40) & (freqs < 150)].sum(axis=1) + 1e-12
        rms = np.sqrt(spec.sum(axis=1))
        keep = (rms > np.percentile(rms, 40)) & (voice / low > 8)       # speech frames, bed-dominated ones dropped
        acc += spec[keep].sum(axis=0)
        count += keep.sum()
    p = acc / max(1, count)
    levels = []
    for f in BANDS:
        lo, hi = f / 2 ** (1 / 6), f * 2 ** (1 / 6)
        levels.append(10 * np.log10(p[(freqs >= lo) & (freqs < hi)].mean() + 1e-20))
    levels = np.array(levels)
    return levels - np.interp(1000, BANDS, levels)


def main():
    a = sys.argv[1:]
    out = a[0]
    refs = a[a.index("--ref") + 1:a.index("--ours")]
    ours = a[a.index("--ours") + 1:]
    ref = ltas([load(r, 3, 150) for r in refs])
    own = ltas([load(o) for o in ours])
    diff = np.convolve(ref - own, np.ones(3) / 3, mode="same")
    diff = np.clip(diff - np.interp(1000, BANDS, diff), -8, 8)
    for f, r, o, d in zip(BANDS, ref, own, diff):
        print(f"{f:7.0f} Hz  ref {r:6.1f}  ours {o:6.1f}  EQ {d:+5.1f} dB")
    json.dump({"bands_hz": [round(f, 1) for f in BANDS], "gain_db": [round(float(d), 2) for d in diff],
               "note": "EQ moving the designed narrator toward the reference narration's tonal balance"},
              open(out, "w"), indent=1)
    print("wrote", out)


main()
