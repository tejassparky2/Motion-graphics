"""Episode 1 v3, Hinglish dub: the same picture, English captions, music and effects; only the narration changes.

Owner, 1 Nov 2026: "make the same in hindi now just change voice to hindi hinglish the voice is already created in
shorts chat take from it", then "let the caption be in English only just voice hinglish".

The voice is the Socho with Tejas channel's "Aman": Indic Parler-TTS's named speaker as the prompt, AI4Bharat IndicF5
reading every line, tempo x1.15 and that chat's studio chain (synthetic; nobody is cloned). The shorts chat voices the
lines and pushes them to branch ccr-56282fe5-evehq4-hinglish, out/monsters_hi/ep01_takes/ (l01.wav ... l30.wav, no l18,
plus lines.json).

    python channels/monsters/ep01v3_hi_sound.py TAKES_DIR          # -> out/monsters/ep01v3_hi/mix.wav + stems + layout.json
    python channels/monsters/ep01v3_hi_sound.py TAKES_DIR --mux [--picture ep01v3_diorama.mp4]   # + the final mp4

The shorts chat records AND Whisper-checks every take with its Hindi Whisper before pushing (owner, 1 Nov 2026: "It
uses whisper made for hindi so let it do it don't download specifically for hindi here"). --check (multilingual
medium on the mix) stays only for a container that already has that model; don't download one for it.

Layout: every take starts where its English line started, so the English captions and every picture cue stay put.
A take longer than its slot (up to GAP before the next line starts) is sped up with ffmpeg atempo, x1.12 at most;
anything still left over pushes the next line later. The music, the effects and their levels come from
ep01v3_sound.build() on the unchanged timing.json, so every cue lands on the same frame as in the English cut; the
sidechain duck follows the Hindi voice.
"""
import json
import os
import subprocess
import sys
import types

import numpy as np
import soundfile as sf
from scipy import signal

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from channels.monsters import ep01v3_sound as v3                         # noqa: E402  (sets base.EPISODE = ep01v3)
from channels.monsters.sfx import SR                                     # noqa: E402

base = v3.base
ROOT = base.ROOT
OUT = os.path.join(ROOT, "out", "monsters", "ep01v3_hi")
GAP = 0.2                 # the least silence between two lines
MAX_RATE = 1.12           # the most a take is sped up to fit its slot
MAX_RATE_LAST = 1.2       # the A/B question may go a little faster so it still lands before the cut
EARLY = 0.15              # a long take may start this much before its English line (into the silence before it)
VOICE_GAIN = {"l6": 3.0}  # dB: "Phir toofan aaya" sits on the thunder (only 3.9 dB over the bed at 0 dB)
END_PAD = 0.5             # the last word ends at least this long before the cut (channel rule TAIL = 0.5)


def atempo(x, sr, rate):
    """Speed a mono take up by `rate` without changing its pitch (ffmpeg atempo)."""
    if abs(rate - 1.0) < 1e-3:
        return x
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "pipe:0",
                        "-af", f"atempo={rate:.4f}", "-f", "f32le", "-ar", str(sr), "-ac", "1", "pipe:1"],
                       input=np.asarray(x, np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32).astype(np.float64)


def load_take(path):
    x, sr = sf.read(path, dtype="float64", always_2d=True)
    x = x.mean(axis=1)
    if sr != SR:
        g = np.gcd(sr, SR)
        x = signal.resample_poly(x, SR // g, sr // g)
    return x


def layout(timing, takes_dir):
    """Place every Hindi take on the English clock; returns the beats and a report."""
    eng = [l for l in timing["lines"] if l.get("text")]
    beats, report, cursor = [], [], 0.0
    for i, l in enumerate(eng):
        num = int(l["id"][1:])
        path = os.path.join(takes_dir, f"l{num:02d}.wav")
        if not os.path.exists(path):
            raise SystemExit(f"missing take {path}")
        x = load_take(path) * 10 ** (VOICE_GAIN.get(l["id"], 0.0) / 20)
        last = i + 1 == len(eng)
        nxt = timing["total"] - END_PAD + GAP if last else eng[i + 1]["start"]
        dur = len(x) / SR
        start = max(l["start"], cursor)
        if dur > nxt - GAP - start:                       # a long take may start a little early into the silence
            start = max(l["start"] - EARLY, cursor)
        room = nxt - GAP - start
        rate = 1.0
        if dur > room and room > 0:
            rate = min(MAX_RATE_LAST if last else MAX_RATE, dur / max(0.05, room - 0.03))   # atempo rounds up a little
            x = atempo(x, SR, rate)
        end = start + len(x) / SR
        cursor = end + GAP
        beats.append(types.SimpleNamespace(id=l["id"], audio=x, start=start, end=end))
        report.append(dict(id=l["id"], eng_start=round(l["start"], 3), eng_end=round(l["end"], 3),
                           start=round(start, 3), end=round(end, 3), take_s=round(dur, 3), rate=round(rate, 3),
                           late=round(start - l["start"], 3)))
    for r in report:
        print(f"{r['id']:>4} take {r['take_s']:5.2f} s  x{r['rate']:.2f}  {r['start']:6.2f}-{r['end']:6.2f}  "
              f"(English {r['eng_start']:6.2f}-{r['eng_end']:6.2f})" + ("  <- late" if r["late"] > 0.05 else ""))
    if beats[-1].end > timing["total"] - END_PAD + 1e-3:
        raise SystemExit(f"the last line ends at {beats[-1].end:.2f} s, past the cut at {timing['total']:.2f} s "
                         f"minus {END_PAD} s: shorten a take")
    return beats, report


LINES = {   # the approved Hinglish lines (owner, 1 Nov 2026), as the voice reads them
    "l1": "हिलना मत। इसका पंजा पानी उबाल देता है।", "l2": "दस मिनट पहले, मैं ज़िंदा था।",
    "l3": "मरीन लैब में नाइट शिफ्ट। बस मैं, और पिस्टल श्रिम्प।", "l4": "पंजा इतना तेज़, कि पानी उबल जाए।",
    "l5": "क़रीब सूरज की सतह जितना गरम। पर सिर्फ पानी में।", "l6": "फिर तूफ़ान आया।",
    "l7": "श्रिम्प घबरा गया। उसके स्नैप से टैंक टूट गया।", "l8": "पानी डेस्क से गिरा, सीधा पावर केबल्स में।",
    "l9": "और मैं उसी में खड़ा था।", "l10": "ऐसे मैं मरा।", "l11": "फिर मैं जागा। एक दूसरी दुनिया में।",
    "l12": "यहाँ सब कुछ छोटा था। और क्यूट।", "l13": "और हर एक में कुछ गड़बड़ थी।", "l14": "मुझे बहुत प्यास लगी थी।",
    "l15": "कोई और पहले से पी रहा था।", "l16": "एक श्रिम्प। ज़मीन पर। नामुमकिन।", "l17": "फिर उसने सीधा मुझे देखा।",
    "l19": "बस एक इंच से बचा।", "l20": "आँख खुली, तो वो मेरी छाती पर बैठा था।", "l21": "फिर मैंने बूँदें देखीं।",
    "l22": "पंजा सिर्फ गीले में चलता है।", "l23": "तो मैं हिला नहीं। धूप ने उसे सुखा दिया।", "l24": "फिर भी, उसने वार किया।",
    "l25": "फिर गुस्से में, वापस पानी की तरफ़।", "l26": "तभी मैंने काँटों वाला पेड़ देखा।",
    "l27": "बुचर बर्ड अपना खाना काँटों पर टाँग देती है।", "l28": "और वो श्रिम्प को देख रही थी।",
    "l29": "श्रिम्प को कुछ पता नहीं था।",
    "l30": "ऑप्शन ए: उस श्रिम्प को बचाऊँ, जिसने मुझे मारना चाहा। ऑप्शन बी: भाग जाऊँ, जब तक मौका है। कमेंट करो, ए या बी।",
}


def _norm_hi(s):
    """Letters only, nukta and chandrabindu folded (Whisper spells them either way)."""
    import re
    import unicodedata
    s = unicodedata.normalize("NFD", s).replace("\u093c", "").replace("\u0901", "\u0902")
    return re.sub(r"[^\u0900-\u097fa-z]+", "", s.lower().replace("।", ""))


def check_hi(model_name="medium"):
    """Whisper (multilingual medium, Hindi) on every line of mix.wav as heard, against LINES. A line passes at a
    character similarity of 0.85 or more; the rest are printed for a listen and a retake."""
    import difflib
    from faster_whisper import WhisperModel
    rep = json.load(open(os.path.join(OUT, "layout.json")))
    y, sr = sf.read(os.path.join(OUT, "mix.wav"), dtype="float32", always_2d=True)
    y = signal.resample_poly(y.mean(axis=1), 1, 3) if sr == 48000 else y.mean(axis=1)
    model = WhisperModel(model_name, device="cpu", compute_type="int8")
    bad = []
    for r in rep:
        clip = y[int(max(0, r["start"] - 0.15) * 16000): int((r["end"] + 0.25) * 16000)]
        segs, _ = model.transcribe(clip, language="hi", beam_size=5, temperature=0.0, condition_on_previous_text=False)
        heard = " ".join(s.text.strip() for s in segs)
        sim = difflib.SequenceMatcher(None, _norm_hi(LINES[r["id"]]), _norm_hi(heard)).ratio()
        ok = sim >= 0.85
        print(f"{r['id']:>4} {'OK ' if ok else 'BAD'} {sim:.2f} | {LINES[r['id']]} | heard: {heard}", flush=True)
        if not ok:
            bad.append((r["id"], round(sim, 2), heard))
    print(f"{len(bad)} line(s) below 0.85")
    return bad


def main():
    takes_dir = sys.argv[1]
    with open(os.path.join(ROOT, "channels", "monsters", "ep01v3", "timing.json")) as f:
        timing = json.load(f)
    beats, report = layout(timing, takes_dir)
    os.makedirs(OUT, exist_ok=True)
    base.OUT = OUT
    base.load_voice = lambda: (None, types.SimpleNamespace(beats=beats, total=timing["total"]))
    base.main()
    with open(os.path.join(OUT, "layout.json"), "w") as f:
        json.dump(report, f, indent=1)
    if "--mux" in sys.argv:
        mux()
    if "--check" in sys.argv:
        check_hi()


def mux():
    """The unchanged v3 picture (stream copy, all 1929 frames) + the Hinglish mix -> out/monsters/ep01v3_hi.mp4, no tags."""
    picture = (sys.argv[sys.argv.index("--picture") + 1] if "--picture" in sys.argv
               else os.path.join(ROOT, "out", "monsters", "ep01v3_diorama.mp4"))   # the English cut: its video stream
    out = os.path.join(ROOT, "out", "monsters", "ep01v3_hi.mp4")
    tmp = out + ".tmp.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", picture, "-i", os.path.join(OUT, "mix.wav"),
                    "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-ar", "48000",
                    "-map_metadata", "-1", "-map_chapters", "-1", "-fflags", "+bitexact",
                    "-flags:a", "+bitexact", "-movflags", "+faststart", tmp], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-map", "0", "-c", "copy", "-map_metadata", "-1",
                    "-fflags", "+bitexact", "-flags:v", "+bitexact", "-flags:a", "+bitexact",
                    "-metadata:s:v", "handler_name=", "-metadata:s:a", "handler_name=", "-movflags", "+faststart", out],
                   check=True)
    os.remove(tmp)
    print(f"{os.path.relpath(out, ROOT)}: {os.path.getsize(out) / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
