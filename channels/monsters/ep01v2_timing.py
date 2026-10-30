"""Exact timing for Episode 1 v2 from the voice takes (assets/voice_cache/monsters_ep01v2_takes.tar).

    tar xf assets/voice_cache/monsters_ep01v2_takes.tar
    /home/user/.venv-main/bin/python channels/monsters/ep01v2_timing.py

Lays out channels/monsters/ep01v2/episode.py with the stories pipeline's pauses (sentence 0.36 s, question 0.45 s,
line gap 0.4 s minimum, the same as channels/horror/make_2d.py) and writes
    channels/monsters/ep01v2/timing.json   every line's start/end, every shot's first frame and length (24 fps)
    channels/monsters/ep01v2/TIMING.md     the same as a table for the builders
A shot cuts in LEAD (0.3 s, 7 frames) before its line; the rest of the silence before a line stays on the shot
before it (so S19 keeps the quiet drying, S20 the pff and the 2 s deadpan, S08 the black). A split shot (S03b, S05b, S10b, S11b) starts halfway through
the pause before the word it opens on. Refuses to synthesise: a missing take is an error, not a new voice."""
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.chdir(ROOT)
os.environ.setdefault("CLONE_RATE", "5.0")
FPS = 24
HANDLE = 12
LEAD = 0.3

from motion import timeline, voice   # noqa: E402

timeline.STOP_PAUSE, timeline.QUESTION_PAUSE, timeline.BEAT_GAP = 0.36, 0.45, 0.4


def _no_synth(*a, **k):
    raise SystemExit(f"missing voice take (would synthesise): {a[:1]}")


voice._clone_generate = _no_synth if hasattr(voice, "_clone_generate") else None
spec = importlib.util.spec_from_file_location("ep01v2_episode", os.path.join(ROOT, "channels", "monsters", "ep01v2",
                                                                              "episode.py"))
ep = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ep)
voice.configure(**ep.NARRATOR)
real_run = voice.subprocess.run


def guarded(cmd, *a, **k):
    if any("clone_tts.py" in str(c) for c in cmd):
        raise SystemExit("missing voice take: clone_tts.py would run. Unpack the takes tar first.")
    return real_run(cmd, *a, **k)


voice.subprocess.run = guarded
tl = timeline.Timeline(ep.SCRIPT, tail=ep.TAIL)


def word_start(b, word):
    """Start of the first unit in beat b whose shown text begins with `word`, and the end of the unit before it."""
    for i, u in enumerate(b.units):
        if u.shown.strip("\"'").lower().startswith(word.lower()):
            return u.start, (b.units[i - 1].end if i else b.start)
    raise KeyError(word)


cuts = []                                        # (shot, start s)
for i, b in enumerate(tl.beats):
    cuts.append((b.scene, 0.0 if i == 0 else b.start - min(b.gap, LEAD)))
for shot, line, word in ep.SPLITS:
    b = tl.by_id[line]
    s, prev_end = word_start(b, word)
    cuts.append((shot, (prev_end + s) / 2))
cuts.sort(key=lambda c: c[1])

shots = []
f_total = round(tl.total * FPS)
for k, (shot, s) in enumerate(cuts):
    f0 = round(s * FPS)
    f1 = round(cuts[k + 1][1] * FPS) if k + 1 < len(cuts) else f_total
    shots.append(dict(shot=shot, start=round(s, 3), first_frame=f0, frames=f1 - f0, seconds=round((f1 - f0) / FPS, 3),
                      render_frames=f1 - f0 + HANDLE))
lines = [dict(id=b.id, scene=b.scene, text=b.text, start=round(b.start, 3), end=round(b.end, 3),
              words=[dict(w=u.shown, start=round(u.start, 3), end=round(u.end, 3)) for u in b.units])
         for b in tl.beats]
out = dict(fps=FPS, total=round(tl.total, 3), total_frames=f_total, handle=HANDLE, lines=lines, shots=shots)
with open(os.path.join(ROOT, "channels", "monsters", "ep01v2", "timing.json"), "w") as f:
    json.dump(out, f, indent=1)

line_of = {}
for b in tl.beats:
    line_of.setdefault(b.scene, b)
for shot, line, word in ep.SPLITS:
    line_of[shot] = tl.by_id[line]
md = ["# Episode 1 v2: exact timing (from the voice takes)", "",
      f"Total **{tl.total:.2f} s = {f_total} frames** at {FPS} fps. Made by `channels/monsters/ep01v2_timing.py`;",
      "the numbers here win over the estimates in EP01V2_SHOTS.md.", "",
      f"- **frames** is the shot's length in the cut. Render **frames + {HANDLE}** (the tail handle).",
      "- **voice in / out** are seconds from the shot's first frame: where the line (or the shot's part of it) is",
      "  heard. Mouth flaps, eye blinks and hits land on these.", "",
      "| Shot | First frame | Frames | Seconds | Render frames | Voice in (s) | Voice out (s) | Line |",
      "|---|---|---|---|---|---|---|---|"]
for k, s in enumerate(shots):
    b = line_of.get(s["shot"])
    t0, t1 = s["start"], s["start"] + s["seconds"]
    if b is not None and b.units:
        ws = [u for u in b.units if u.start >= t0 - 1e-3 and u.end <= t1 + 1e-3]
        vin = f"{ws[0].start - t0:.2f}" if ws else "-"
        vout = f"{ws[-1].end - t0:.2f}" if ws else "-"
        said = " ".join(u.shown for u in ws)
    else:
        vin = vout = "-"
        said = "(no words)" if b is not None else ""
    md.append(f"| {s['shot']} | {s['first_frame']} | {s['frames']} | {s['seconds']:.2f} | {s['render_frames']} | "
              f"{vin} | {vout} | {said} |")
with open(os.path.join(ROOT, "channels", "monsters", "ep01v2", "TIMING.md"), "w") as f:
    f.write("\n".join(md) + "\n")
print("\n".join(md))
