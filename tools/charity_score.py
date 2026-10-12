"""Original background score for charity appeals (synthesised here: no samples, no copyrighted music).

Research behind the choices (Oct 2026 notes, trust reel01):
- Mode, not tempo, moves helping: sad/minor music raised willingness to help over happy music or silence,
  tempo had no effect (Frontiers in Psychology 2024, "Tunes that move us", PMC11754231). So: tender minor
  key, slow and calm, with a lift to major only for the call to action (hope, not despair).
- Speech must stay clear: background at least ~20 dB under foreground speech (WCAG 1.4.7), ducked
  whenever someone speaks.
- Indian warmth for a Kannada audience: tanpura drone, soft harmonium-like pad, bansuri-like flute.
  The flute sits in the voice's range, so it only plays where nobody is making the appeal.

  bed = score(n, sr, flute_from, lift_at)      # mono float array, peak 1
"""
import numpy as np

D3 = 146.83


def _hz(semi, base=D3):
    return base * 2 ** (semi / 12)


def _adsr(n, sr, a, r):
    t = np.arange(n) / sr
    return np.minimum(1, t / a) * np.clip((n / sr - t) / r, 0, 1)


def _pad_note(f, dur, sr, bright=1.0):
    n = int(dur * sr)
    t = np.arange(n) / sr
    s = np.zeros(n)
    for k in range(1, 8):                                           # reed-like, harmonium flavour
        amp = (1 / k ** 1.4) * (bright if k > 3 else 1)
        for det in (-0.12, 0.12):                                  # gentle chorus
            s += amp * np.sin(2 * np.pi * f * k * (1 + det / 100) * t + k * 0.7)
    return s * _adsr(n, sr, 1.6, 2.0) * (1 + 0.05 * np.sin(2 * np.pi * 0.2 * t))


def _tanpura(f, sr, rng):
    n = int(3.6 * sr)
    t = np.arange(n) / sr
    s = np.zeros(n)
    for k in range(1, 14):                                          # jawari: bright, buzzing upper partials
        env = np.exp(-t / (2.6 / (1 + 0.08 * k)))
        bloom = 1 + 0.6 * np.sin(np.pi * np.clip(t / 2.0, 0, 1)) * (k > 4)
        s += env * bloom / k ** 1.1 * np.sin(2 * np.pi * f * k * t + rng.uniform(0, 6))
    return s * np.minimum(1, t / 0.004)


def _flute(f0, f1, dur, sr, rng):
    """One bansuri-like note, gliding (meend) from f0 to f1 over its first fifth."""
    n = int(dur * sr)
    t = np.arange(n) / sr
    glide = np.clip(t / max(0.15, dur * 0.2), 0, 1)
    f = f0 * (f1 / f0) ** (glide * glide * (3 - 2 * glide))
    vib = 1 + 0.006 * np.minimum(1, t / 0.6) * np.sin(2 * np.pi * 5.2 * t)
    ph = 2 * np.pi * np.cumsum(f * vib) / sr
    tone = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.05 * np.sin(3 * ph)
    breath = rng.standard_normal(n)
    from scipy.signal import butter, sosfilt
    breath = sosfilt(butter(2, [f1 * 0.8, f1 * 3], "bandpass", fs=sr, output="sos"), breath) * 0.25
    return (tone + breath) * _adsr(n, sr, 0.12, min(0.6, dur * 0.4))


def score(n, sr, flute_from, lift_at, seed=7):
    from scipy.signal import butter, fftconvolve, sosfilt
    rng = np.random.default_rng(seed)
    total = n / sr
    pad = np.zeros(n + sr * 6)
    drone = np.zeros_like(pad)
    flute = np.zeros_like(pad)

    def put(sig, at, buf, g=1.0):
        s0 = int(at * sr)
        if 0 <= s0 < len(buf):
            buf[s0:s0 + len(sig)] += g * sig[: len(buf) - s0]

    # tender D minor: i - VI - III - VII (Dm Bb F C), 6 s each; at the lift: Bb - C - D major, held
    minor = [[0, 3, 7], [-4, 0, 3], [3, 7, 10], [-2, 2, 5]]
    lift = [[-4, 0, 3], [-2, 2, 5], [0, 4, 7]]
    t, i = 0.0, 0
    while t < lift_at - 0.01:
        dur = min(6.0, lift_at - t)
        for s in minor[i % 4]:
            put(_pad_note(_hz(s), dur + 2.0, sr, bright=0.6), t, pad, 0.22)
        put(_pad_note(_hz(minor[i % 4][0] - 12), dur + 2.0, sr, 0.4), t, pad, 0.18)
        t += dur
        i += 1
    spans = [2.6, 2.6, max(2.0, total - lift_at - 5.2)]
    for ch, dur in zip(lift, spans):
        for s in ch + [ch[0] + 12]:
            put(_pad_note(_hz(s), dur + 2.5, sr, bright=1.0), t, pad, 0.22)
        put(_pad_note(_hz(ch[0] - 12), dur + 2.5, sr, 0.5), t, pad, 0.2)
        t += dur

    # tanpura cycle Pa - Sa' - Sa' - Sa, one pluck a second
    for k in range(int(total) + 1):
        f = [_hz(-5), _hz(0), _hz(0), _hz(-12)][k % 4]
        put(_tanpura(f, sr, rng), k * 1.0 + rng.uniform(0, 0.03), drone, 0.09)

    # bansuri phrases (D Kafi-ish: D E F G A B C), only from flute_from on; brighter phrase at the lift
    phrase_minor = [(7, 1.4), (5, 0.8), (3, 0.8), (5, 1.6), (0, 2.4), (None, 1.2),
                    (3, 0.8), (5, 0.8), (7, 1.2), (10, 1.0), (7, 2.6), (None, 1.6)]
    phrase_lift = [(7, 1.0), (9, 1.0), (12, 1.6), (14, 1.0), (12, 0.8), (9, 0.8), (12, 3.6)]
    t, prev = flute_from, 7
    while t < lift_at - 1.0:
        for semi, dur in phrase_minor:
            if t + dur > lift_at - 0.5:
                break
            if semi is not None:
                put(_flute(_hz(prev + 12), _hz(semi + 12), dur + 0.15, sr, rng), t, flute, 0.16)
                prev = semi
            t += dur
        else:
            continue
        break
    t = lift_at + 0.4
    for semi, dur in phrase_lift:
        if t + 0.8 > total:
            break
        put(_flute(_hz(prev + 12), _hz(semi + 12), min(dur + 0.15, total - t), sr, rng), t, flute, 0.18)
        prev, t = semi, t + dur

    # keep the bed out of the speech band (pad/drone), small warm room on everything
    pad = sosfilt(butter(2, 1800, "lowpass", fs=sr, output="sos"), pad)
    drone = sosfilt(butter(2, 2600, "lowpass", fs=sr, output="sos"), drone)
    dry = pad + drone + flute
    ir_t = np.arange(int(2.2 * sr)) / sr
    ir = rng.standard_normal(len(ir_t)) * np.exp(-ir_t / 0.6)
    ir[0] = 8.0
    wet = fftconvolve(dry, ir)[: len(dry)] / 14
    mix = (dry * 0.75 + wet * 0.45)[:n]
    mix = sosfilt(butter(2, 70, "highpass", fs=sr, output="sos"), mix)
    fade_in = np.clip(np.arange(n) / (2.0 * sr), 0, 1)
    fade_out = np.clip((n - np.arange(n)) / (2.5 * sr), 0, 1)
    mix = mix * fade_in * fade_out
    return mix / max(1e-6, np.abs(mix).max())


def duck_mix(voice, music, sr, plan, under_speech_db=-20.0, attack=0.15, release=0.8):
    """Mix music under a (stereo or mono) voice track.

    plan: list of (start_s, music_rms_db[, under_db]) giving, per section, the music's level when nobody
    speaks and how far under the speech it sits while someone does (default `under_speech_db`); the music
    never goes above the section level. Returns the mix and the music gain curve (dB)."""
    v = voice if voice.ndim == 1 else voice.mean(axis=1)
    hop = int(0.05 * sr)
    frames = len(v) // hop
    rms = np.sqrt(np.mean(v[: frames * hop].reshape(frames, hop) ** 2, axis=1) + 1e-12)
    vdb = 20 * np.log10(rms)
    # a short look-ahead max so the duck lands before a word starts
    look = np.maximum.reduce([np.roll(vdb, -k) for k in range(0, 4)])
    speaking = look > -38
    m = music[: len(v)]
    m_ref = 20 * np.log10(np.sqrt(np.mean(m ** 2)) + 1e-12)       # whole-track music RMS
    t = np.arange(frames) * hop / sr
    section = np.full(frames, plan[0][1])
    under = np.full(frames, under_speech_db)
    for start, lvl, *u in plan:
        section[t >= start] = lvl
        under[t >= start] = u[0] if u else under_speech_db
    # running speech level (smoothed) sets the ceiling for the music while someone talks
    speech_lvl = np.convolve(np.where(speaking, vdb, -90), np.ones(20) / 20, "same")
    target = np.where(speaking, np.minimum(section, np.maximum(speech_lvl, -30) + under), section)
    g = np.empty(frames)
    cur = target[0]
    a_c, r_c = np.exp(-0.05 / attack), np.exp(-0.05 / release)
    for k in range(frames):
        c = a_c if target[k] < cur else r_c
        cur = c * cur + (1 - c) * target[k]
        g[k] = cur
    gain_db = g - m_ref
    gain = np.interp(np.arange(len(v)), np.arange(frames) * hop + hop / 2, 10 ** (gain_db / 20))
    mm = m * gain
    out = voice + (mm[:, None] if voice.ndim == 2 else mm)
    return out, g
