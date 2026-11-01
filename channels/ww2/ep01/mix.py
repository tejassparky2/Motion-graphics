"""WW2 Episode 1: the final mix. Narration + the score (planned here from the episode clock) + the effects each package
lists in its cues(T) -> out/ww2/ep01/mix.wav at -14 LUFS, true peak <= -1 dBTP, 48 kHz 16-bit stereo, no metadata.

    python channels/ww2/ep01/mix.py              # the mix (stand-ins for whatever hasn't landed yet)
    python channels/ww2/ep01/mix.py --check      # + Whisper medium on every line of the mix
    python channels/ww2/ep01/mix.py --plan       # print the score plan and the effect list, no audio

Inputs:
- channels/ww2/ep01/timing.json (via timing.Timing): every score cue is anchored to a line, sentence or chapter card,
  so the voiced timing moves the whole score with it. Nothing here is in absolute seconds.
- out/ww2/ep01/narration.wav (any rate, mono or stereo; resampled to 48 kHz and set to -16 LUFS). Until it lands, a
  stand-in babble voice is laid on the sentence times so the ducking can be judged (no Whisper check then).
- channels/ww2/ep01/p1.py .. p8.py: cues(T) -> [(t, name, gain_db, pan)] or with a 5th item, the duration in seconds
  (or a dict of keyword arguments) for the effects that take one (tank, plane_drone, sea_waves, ...). Names come from
  sound.SFX; gain_db is relative to a full-scale effect (the demo used -26 for a faint one to -3 for the gun).
  Music names (fanfare, drum_hit, tension, ...) are the score's job: they're ignored here, except drum_hit, whose time
  then replaces the default. A package with no cues() yet gets the stand-in list in STUB_CUES.

The score (owner brief via the coordinator, 31 Oct 2026): the newsreel fanfare on every chapter card except the
Holocaust's; tension for the cold open and Chapter 1, with the drum hit on "the biggest shock"; marches for the
Blitzkrieg, the fall of France, Barbarossa, D-Day and Bagration; somber, then the low tone, then silence for the
Holocaust; triumph-but-sad for V-E Day; somber for the bombs and the aftermath, a quiet end, and a hard cut right
after the last word. Music ducks 10 dB and ambience 8 dB under the narration (20 ms / 300 ms).
"""
import argparse
import difflib
import importlib
import json
import os
import re
import sys

import numpy as np
from scipy import signal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from channels.ww2 import sound as S                     # noqa: E402
from channels.ww2.ep01.timing import PACKAGES, Timing   # noqa: E402

OUT_DIR = os.path.join(ROOT, "out", "ww2", "ep01")
NARRATION = os.path.join(OUT_DIR, "narration.wav")
MIX = os.path.join(OUT_DIR, "mix.wav")
REPORT = os.path.join(OUT_DIR, "mix_report.json")

DUCK = dict(music_duck_db=-10.0, amb_duck_db=-10.0, fx_duck_db=-6.0,   # under the narration, and the
            protect_db=10.0)                                                # bed held 10 dB under the words
VOICE_LUFS = -16.0        # the narration's level before the master (the master then lifts everything to -14)
MUSIC_LUFS = -22.0        # each music cue's level before its section offset: ~6 LU under the voice, ~16 when ducked
AMBIENT = {"sea_waves", "blizzard", "radio_static", "clock_tick", "crowd_cheer", "train", "artillery_barrage",
           "plane_drone", "tank", "voice_crackle"}                  # long beds go on the ducked ambience bus
DEFAULT_DUR = dict(tank=5.0, plane_drone=6.0, sea_waves=8.0, blizzard=8.0, radio_static=3.0, voice_crackle=3.0,
                   typewriter=3.0, crowd_cheer=6.0, clock_tick=5.0, train=8.0, artillery_barrage=6.0, dive_whine=2.6)


# ---------------------------------------------------------------- the score plan

def score_plan(T, drum_hit_at=None):
    """[(kind, start, end, db, kwargs)] with kind a sound.MUSIC name or "cut" (silence on everything but the voice).
    end is where the cue is cut (with a short fade); the cue itself is generated a little longer."""
    L = lambda i: T.line(str(i))                               # noqa: E731
    card = lambda c: T.chapter(c).card                          # noqa: E731
    shock = drum_hit_at if drum_hit_at is not None else L(29).end - 0.25
    P = []

    def m(kind, a, b, db=0.0, fade_in=0.6, fade_out=1.0, **kw):
        P.append(dict(kind=kind, start=round(a, 3), end=round(b, 3), db=db, fade_in=fade_in, fade_out=fade_out,
                      kw=kw))

    def fanfare(c):
        a = card(c)[0]
        m("fanfare", a, a + 3.6, 4.0, 0.0, 0.4)

    # cold open: tension; it stops dead on "And fires." (the gun is the package's effect), then the world and title
    m("tension", 0.0, L(3).start + 0.05, 0.0, 0.05, 0.03, seed=0)
    m("tension", L(4).start - 0.4, card("C1")[0] + 0.3, 0.0, 1.2, 0.6, seed=1, tick_on=False)
    # Chapter 1: the broken peace; the drum hit on "the biggest shock"; the pact under a quieter pulse
    fanfare("C1")
    m("tension", L(8).start - 0.3, L(16).end + 0.6, -1.0, 0.8, 1.2, seed=2, bpm=96)
    m("tension", L(17).start - 0.4, shock, 0.0, 1.0, 0.05, seed=3)
    m("drum_hit", shock, shock + 4.0, 5.0, 0.0, 0.5)
    m("tension", shock + 1.8, card("C2")[0] + 0.3, -2.0, 1.5, 0.6, seed=4, tick_on=False)
    # Chapter 2: Blitzkrieg march; the Phoney War idles; France falls to a march; Dunkirk and the armistice somber
    fanfare("C2")
    m("march", L(34).start - 0.5, L(38).end + 0.6, 0.0, 0.3, 1.2, seed=0, bpm=116)
    m("tension", L(39).start - 0.3, L(40).end + 0.4, -5.0, 1.0, 0.8, seed=5, tick_on=False)
    m("march", L(41).start - 0.3, L(45).end + 0.6, 0.0, 0.4, 1.2, seed=1, bpm=112)
    m("somber", L(46).start - 0.4, L(51).end + 0.8, 0.0, 1.0, 1.5, seed=0)
    m("tension", L(52).start - 0.3, card("C3")[0] + 0.3, -1.0, 1.0, 0.6, seed=6)
    # Chapter 3: the gamble; Barbarossa drives east; winter; Pearl Harbor and a world war
    fanfare("C3")
    m("tension", L(58).start - 0.3, L(59).end + 0.3, -1.0, 0.6, 0.6, seed=7)
    m("march", L(60).start - 0.3, L(63).end + 0.6, 0.0, 0.3, 1.5, seed=2, bpm=120)
    m("tension", L(64).start - 0.3, L(66).end + 0.4, -4.0, 1.2, 1.0, seed=8, tick_on=False)
    m("tension", L(67).start - 0.3, card("C4")[0] + 0.3, 0.0, 0.8, 0.6, seed=9)
    # Chapter 4: Midway; El Alamein; Stalingrad; the surrender somber; Kursk; the U-boats and the codebreakers
    fanfare("C4")
    m("tension", L(75).start - 0.3, L(79).end + 0.4, 0.0, 0.6, 0.8, seed=10)
    m("march", L(80).start - 0.3, L(80).end + 0.6, -1.0, 0.3, 1.0, seed=3, bpm=108)
    m("tension", L(81).start - 0.2, L(84).end + 0.3, 0.0, 0.8, 0.6, seed=11)
    m("somber", L(85).start - 0.4, L(87).end + 0.6, 0.0, 1.0, 1.2, seed=1)
    m("march", L(88).start - 0.3, L(88).end + 0.6, -1.0, 0.3, 1.0, seed=4, bpm=112)
    m("tension", L(89).start - 0.3, card("C5")[0] + 0.6, -1.0, 0.8, 1.5, seed=12)
    # Chapter 5, the Holocaust: no fanfare; somber into the low tone, then silence (line 97 and the gap after it)
    m("somber", card("C5")[0] + 0.3, L(92).end + 0.8, -2.0, 1.5, 1.5, seed=2, with_pad=False)
    m("low_tone", L(93).start - 0.5, L(96).end + 1.0, -1.0, 2.0, 2.0)
    P.append(dict(kind="cut", start=round(L(96).end + 1.0, 3), end=round(card("C6")[0], 3)))
    # Chapter 6: Sicily; D-Day through Bagration and Paris on one march; the Bulge; the Pacific
    fanfare("C6")
    m("tension", L(98).start - 0.3, L(100).end + 0.4, -1.0, 0.6, 0.8, seed=13)
    m("march", L(101).start - 0.4, L(106).end + 0.8, 0.0, 0.5, 1.5, seed=5, bpm=112)
    m("tension", L(107).start - 0.3, L(108).end + 0.5, 0.0, 0.5, 0.6, seed=14)
    m("tension", L(109).start - 0.3, card("C7")[0] + 0.3, -2.0, 1.0, 0.6, seed=15, tick_on=False)
    # Chapter 7: Berlin; the bunker door and silence; V-E Day; "But Japan fights on." quiet; the bombs, somber
    fanfare("C7")
    m("tension", L(111).start - 0.3, L(112).end + 0.15, 0.0, 0.6, 0.03, seed=16)
    P.append(dict(kind="cut", start=round(L(112).end + 0.15, 3), end=round(L(113).start - 0.2, 3)))
    m("triumph", L(113).start - 0.2, L(115).start - 0.1, 0.0, 0.3, 0.05, seed=0)
    m("somber", L(116).start - 0.3, card("C8")[0] + 0.4, -1.0, 1.5, 1.0, seed=3)
    # Chapter 8: after the war, somber; the question over a quiet low tone; a hard cut after the last word
    fanfare("C8")
    m("somber", L(122).start - 0.3, L(127).end + 0.6, 0.0, 1.0, 1.5, seed=4)
    m("low_tone", L(128).start - 0.5, L(131).end + 0.05, -6.0, 1.5, 0.02, seed=1)
    P.append(dict(kind="cut", start=round(L(131).end + 0.05, 3), end=round(T.total, 3)))
    return P


# ---------------------------------------------------------------- the effects

def STUB_CUES(T, pkg):
    """Stand-in effects for a package that has no cues() yet (from the script's stage directions)."""
    L = lambda i: T.line(str(i))                               # noqa: E731
    c = {
        "P1": [(0.0, "clock_tick", -24, 0.0, L(2).start), (0.2, "sea_waves", -26, 0.0, L(3).end),
               (L(3).end - 0.1, "gun_boom", -3, 0.0), (L(10).start + 1.0, "typewriter", -22, 0.2, 3.0),
               (L(16).end - 1.5, "stamp", -12, 0.0)],
        "P2": [(L(18).start + 2.0, "page_whoosh", -16, -0.2), (L(19).start + 2.0, "page_whoosh", -16, 0.2),
               (L(27).start + 1.0, "plane_drone", -24, 0.3, 4.0), (L(31).end - 0.5, "stamp", -10, 0.0),
               (L(33).end - 0.4, "gun_boom", -5, 0.0), (L(34).start, "tank", -20, -0.3, 5.0),
               (L(34).start + 1.0, "plane_drone", -22, 0.2, 5.0)],
        "P3": [(L(36).start + 0.5, "morse", -24, 0.3, {"text": "WAR DE G"}), (L(39).start, "clock_tick", -26, 0, 5.0),
               (L(47).start, "sea_waves", -24, 0.0, 9.0)],
        "P4": [(L(54).start, "plane_drone", -20, 0.0, {"dur": 7.0, "count": 4}),
               (L(60).start, "artillery_barrage", -22, 0.0, 6.0), (L(64).start, "blizzard", -24, 0.0, 9.0),
               (L(67).start + 2.0, "dive_whine", -18, 0.2, 2.4), (L(67).start + 4.4, "explosion", -10, 0.1)],
        "P5": [(L(70).start + 0.5, "radio_static", -26, -0.3, 3.0), (L(78).start + 3.0, "dive_whine", -18, 0.2),
               (L(78).start + 5.6, "explosion", -9, 0.0), (L(80).start, "tank", -22, -0.2, 6.0),
               (L(84).start + 0.4, "stamp", -10, 0.0)],
        "P6": [(L(88).start, "tank", -22, 0.2, 5.0), (L(90).start + 1.0, "typewriter", -22, 0.0, 4.0),
               (L(94).start + 1.0, "train", -28, 0.0, {"dur": 6.0, "distance": 2.5, "whistle": False})],
        "P7": [(L(102).start, "sea_waves", -22, 0.0, 9.0), (L(103).start, "plane_drone", -22, 0.0,
                                                            {"dur": 7.0, "count": 3}),
               (L(104).start, "rifle_crack", -20, 0.4), (L(105).start, "artillery_barrage", -22, 0.0, 6.0),
               (L(106).start, "crowd_cheer", -22, 0.0, 3.5), (L(112).end + 0.05, "door_slam", -6, 0.0),
               (L(114).start, "crowd_cheer", -18, 0.0, 6.0),
               (L(116).start + 3.5, "explosion", -12, 0.0, {"size": 2.0, "distance": 3.0})],
        "P8": [(L(118).start + 2.0, "explosion", -14, 0.0, {"size": 2.0, "distance": 3.5}),
               (L(120).start, "radio_static", -24, -0.2, 4.0)],
    }
    return c.get(pkg, [])


def package_cues(T):
    """Every package's cues: (pkg, t, name, db, pan, extra, stub?). Music names are dropped (drum_hit -> its time)."""
    out, drum = [], None
    for pkg, _, _ in PACKAGES:
        stub = False
        try:
            mod = importlib.import_module(f"channels.ww2.ep01.{pkg.lower()}")
            cues = list(mod.cues(T)) if hasattr(mod, "cues") else None
        except ModuleNotFoundError:
            cues = None
        if cues is None:
            cues, stub = STUB_CUES(T, pkg), True
        for c in cues:
            t, name, db, pan = c[:4]
            extra = c[4] if len(c) > 4 else None
            if name == "drum_hit":
                drum = float(t)
            elif name in S.MUSIC:
                continue
            elif name not in S.SFX:
                print(f"warning: {pkg} cue {name!r} at {t:.2f} is not in sound.SFX; skipped")
            else:
                out.append((pkg, float(t), name, float(db), float(pan), extra, stub))
    return out, drum


def make_sfx(name, extra, seed):
    fn = S.SFX[name]
    kw = dict(extra) if isinstance(extra, dict) else {}
    if isinstance(extra, (int, float)):
        kw["dur"] = float(extra)
    if name in DEFAULT_DUR and "dur" not in kw:
        kw["dur"] = DEFAULT_DUR[name]
    if "seed" in fn.__code__.co_varnames[:fn.__code__.co_argcount] and "seed" not in kw:
        kw["seed"] = seed
    return fn(**kw)


# ---------------------------------------------------------------- the voice

def load_narration(total):
    """The narration at 48 kHz mono, set to VOICE_LUFS; None if it hasn't landed."""
    if not os.path.exists(NARRATION):
        return None
    import pyloudnorm
    import soundfile as sf
    x, sr = sf.read(NARRATION, always_2d=True)
    x = x.mean(1)
    if sr != S.SR:
        g = np.gcd(sr, S.SR)
        x = signal.resample_poly(x, S.SR // g, sr // g)
    x = x[: S._n(total)]
    return x * S._db(VOICE_LUFS - pyloudnorm.Meter(S.SR).integrated_loudness(x))


def stub_voice(T):
    """A stand-in voice on the sentence times (formant babble, clean), only to judge the ducking before the real one."""
    import pyloudnorm
    v = np.zeros(S._n(T.total))
    k = 0
    for lid in T.order:
        ln = T._lines[lid]
        for s in ln["sentences"]:
            d = s["end"] - s["start"]
            babble = S.voice_crackle(d, 1000 + k, f0=105, radio=False)
            S._place(v, babble * S._ramp(len(babble), 0.02, 0.05), s["start"])
            k += 1
    return v * S._db(VOICE_LUFS - pyloudnorm.Meter(S.SR).integrated_loudness(v))


# ---------------------------------------------------------------- build

def _music(kind, dur, kw):
    fn = S.MUSIC[kind]
    if kind in ("fanfare", "drum_hit"):
        return fn(**kw)
    return fn(dur, **kw)


def build(T, verbose=True):
    import pyloudnorm
    meter = pyloudnorm.Meter(S.SR)
    cues, drum = package_cues(T)
    plan = score_plan(T, drum)
    mix = S.Mix(T.total)
    for p in plan:
        if p["kind"] == "cut":
            mix.cut(p["start"], p["end"])
            continue
        dur = p["end"] - p["start"]
        x = _music(p["kind"], dur + 1.5, p["kw"])[: S._n(dur)]
        x = x * S._db(MUSIC_LUFS - meter.integrated_loudness(x if len(x) > S._n(0.5) else np.pad(x, ((0, S._n(0.5)),
                                                                                                    (0, 0)))))
        mix.music(x, p["start"], p["db"], fade_in=p["fade_in"], fade_out=p["fade_out"])
        if verbose:
            print(f"  {p['start']:7.2f}-{p['end']:7.2f}  {p['kind']:9s} {p['db']:+.0f} dB  {p['kw'] or ''}")
    for k, (pkg, t, name, db, pan, extra, stub) in enumerate(cues):
        x = make_sfx(name, extra, k)
        (mix.amb if name in AMBIENT else mix.sfx)(x, t, db, pan=pan, fade_in=0.0 if name not in AMBIENT else 0.3,
                                                  fade_out=0.0 if name not in AMBIENT else 0.5)
    voice = load_narration(T.total)
    real = voice is not None
    if not real:
        voice = stub_voice(T)
    return mix, voice, real, plan, cues


SNR_MIN = 10.0


def line_snr(T, mix, voice):
    """Per line: the narration's level over everything else under it (music, effects, ambience after the ducks),
    in dB. Under ~10 dB a word can be lost under an effect; the Whisper check then decides."""
    bed = mix.render(voice, **DUCK).mean(1)
    v = np.zeros(len(bed))
    v[: min(len(v), len(voice))] = voice[: len(v)]
    bed -= v
    out = []
    for lid in T.order:
        ln = T._lines[lid]
        a, b = S._n(ln["start"]), S._n(ln["end"])
        rv, rb = np.sqrt(np.mean(v[a:b] ** 2)), np.sqrt(np.mean(bed[a:b] ** 2)) + 1e-9
        out.append((lid, round(float(20 * np.log10(rv / rb)), 1)))
    return out


def whisper_check(T, path=MIX, model="medium.en"):
    """Whisper on every line of the mix (cut at the line's times): how close the heard words are to the spoken text.
    Returns [(line id, ratio, heard)]; ratio < 0.85 is flagged."""
    import soundfile as sf
    import whisper
    w = whisper.load_model(model)
    x, sr = sf.read(path, always_2d=True)
    x = signal.resample_poly(x.mean(1), 1, sr // 16000).astype(np.float32) if sr % 16000 == 0 else \
        signal.resample_poly(x.mean(1), 16000, sr).astype(np.float32)
    norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower().replace("-", " "))            # noqa: E731
    out = []
    for lid in T.order:
        ln = T._lines[lid]
        a, b = int(max(0, ln["start"] - 0.25) * 16000), int((ln["end"] + 0.35) * 16000)
        heard = w.transcribe(x[a:b], language="en", fp16=False, temperature=0.0,
                             initial_prompt="A World War Two documentary.")["text"].strip()
        r = difflib.SequenceMatcher(None, norm(ln.get("spoken", ln["text"])).split(), norm(heard).split()).ratio()
        out.append((lid, round(r, 3), heard))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true", help="Whisper medium on every line of the finished mix")
    ap.add_argument("--plan", action="store_true", help="print the score plan and the effects, then stop")
    a = ap.parse_args()
    T = Timing()
    if a.plan:
        cues, drum = package_cues(T)
        for p in score_plan(T, drum):
            print(f"{p['start']:7.2f}-{p['end']:7.2f}  {p['kind']}")
        for c in cues:
            print(f"{c[1]:7.2f}  {c[0]} {c[2]} {c[3]:+.0f} dB{'  (stub)' if c[6] else ''}")
        return
    print(f"timing: total {T.total:.2f} s, {'provisional' if T.estimated else 'voiced'}")
    mix, voice, real, plan, cues = build(T)
    meas = mix.master(MIX, voice=voice, **DUCK)
    snr = line_snr(T, mix, voice)
    low = [r for r in snr if r[1] < SNR_MIN]
    print(f"voice over background, per line: median {np.median([r[1] for r in snr]):.1f} dB, lowest "
          + ", ".join(f"{lid} {v:.1f}" for lid, v in sorted(snr, key=lambda r: r[1])[:5])
          + (f"; {len(low)} line(s) under {SNR_MIN:.0f} dB" if low else ""))
    stubs = sorted({c[0] for c in cues if c[6]})
    print(f"{os.path.relpath(MIX, ROOT)}: I {meas['I']:.2f} LUFS, TP {meas['TP']:.2f} dBTP, LRA {meas['LRA']:.1f}; "
          f"voice {'narration.wav' if real else 'STAND-IN'}; {len(cues)} effects"
          f"{'; stub cues for ' + ', '.join(stubs) if stubs else ''}")
    report = dict(timing_estimated=T.estimated, voice="narration" if real else "stand-in", master=meas,
                  stub_packages=stubs, score=plan, effects=[c[:5] for c in cues], voice_over_background_db=snr)
    if a.check:
        if not real:
            print("Whisper check skipped: the narration hasn't landed (stand-in voice)")
        else:
            res = whisper_check(T)
            bad = [r for r in res if r[1] < 0.85]
            for lid, r, heard in bad:
                print(f"  line {lid}: {r:.2f} heard: {heard}")
            print(f"Whisper medium: {len(res) - len(bad)}/{len(res)} lines heard as written (ratio >= 0.85)")
            report["whisper"] = res
    os.makedirs(OUT_DIR, exist_ok=True)
    json.dump(report, open(REPORT, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
