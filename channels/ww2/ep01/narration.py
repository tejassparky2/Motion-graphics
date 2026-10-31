"""WW2 Episode 1 narration: script -> spoken takes -> narration.wav + timing.json (the clock every package animates to).

    /home/user/.venv-main/bin/python channels/ww2/ep01/narration.py --estimate   # provisional timing.json from word counts
    /home/user/.venv-main/bin/python channels/ww2/ep01/narration.py --voice      # voice every sentence (Chatterbox Turbo,
                                                     # bm_george timbre, owner's pick 31 Oct 2026), Whisper-check, assemble

Narrator: Chatterbox Turbo with the synthetic Kokoro "bm_george" reference (male British; no real person is cloned).
Every sentence is its own take; real pauses between sentences, longer between lines, a chapter-card gap between
chapters, and slower, longer pauses in the Holocaust chapter. Numbers are written out in words for the voice.

timing.json schema (times in seconds from the episode start):
  {"fps": 24, "total": T, "chapters": [{"id": "C0", "title": ..., "start": s, "end": e, "card": [s0, s1] | null}],
   "lines": [{"id": "33", "chapter": "C1", "text": ..., "spoken": ..., "start": s, "end": e,
              "sentences": [{"text": ..., "start": s, "end": e}]}], "estimated": true|false}
Packages read it through channels/ww2/ep01/timing.py (Timing().line("33").start ...).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(ROOT, "channels", "ww2", "ep01_script.md")
TAKES = os.path.join(ROOT, "build", "ww2", "takes")
REF = os.path.join(ROOT, "build", "turbo_refs", "bm_george.wav")
OUT_WAV = os.path.join(ROOT, "out", "ww2", "ep01", "narration.wav")
TIMING = os.path.join(HERE, "timing.json")
SR = 24000

CHAPTERS = [  # (id, title, first line id); line ids follow the script's numbering, "109b"/"123b" included
    ("C0", "Cold open", "1"), ("C1", "The broken peace", "8"), ("C2", "Lightning war", "34"),
    ("C3", "The war goes global", "58"), ("C4", "The turning points", "75"), ("C5", "The Holocaust", "92"),
    ("C6", "Closing in", "98"), ("C7", "The end", "111"), ("C8", "After the war", "122")]
LEAD_IN = 0.6            # silence before the first word (the battleship scene is already moving)
SENT_PAUSE = 0.42        # between sentences inside a line
LINE_PAUSE = 0.62        # between lines
CARD_GAP = 2.9           # chapter card on screen between chapters (fanfare)
SOMBER = {"C5": 1.6}     # pause multiplier in the Holocaust chapter
SPECIAL_AFTER = {"2": 0.35, "3": 1.1, "6": 0.9, "7": 0.4, "10": 0.5, "15": 0.8, "28": 0.7, "32": 0.8, "35": 0.7,
                 "49": 0.8, "55": 0.6, "57": 0.8, "64": 0.6, "72": 0.9, "79": 0.7, "85": 0.6, "95": 2.0,
                 "97": 2.2, "102": 0.9, "108": 0.6, "112": 1.4, "118": 1.0, "119": 1.6, "121": 1.4, "124": 1.0,
                 "129": 0.6}      # extra beat (s) after these lines: punches, reveals, the somber moments
TAIL = 0.5               # cut within ~0.5 s of the last word (channel rule)

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen " \
       "seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
ORD = {"1st": "first", "2nd": "second", "3rd": "third", "4th": "fourth", "5th": "fifth", "6th": "sixth",
       "7th": "seventh", "8th": "eighth", "9th": "ninth", "10th": "tenth", "11th": "eleventh", "15th": "fifteenth",
       "17th": "seventeenth", "22nd": "twenty-second", "30th": "thirtieth"}


def two(n):
    if n < 20:
        return ONES[n]
    t, o = divmod(n, 10)
    return TENS[t] + ("-" + ONES[o] if o else "")


def year(y):
    a, b = divmod(int(y), 100)
    return two(a) + " " + ("hundred" if b == 0 else ("oh " + ONES[b] if b < 10 else two(b)))


def spoken(text):
    """The words the voice reads: numbers in words, a few names respelled for the voice."""
    s = text
    s = re.sub(r"\b4:45\b", "four forty-five", s)
    for k, v in ORD.items():
        s = re.sub(rf"\b{k}\b", v, s)
    s = re.sub(r"\b(19[0-4]\d)\b", lambda m: year(m.group(1)), s)
    s = s.replace("USS Missouri", "U-S-S Missouri")
    s = re.sub(r"([.?!]\s+)([a-z])", lambda m: m.group(1) + m.group(2).upper(), s)    # "...1939. Four forty-five"
    return s[:1].upper() + s[1:]


def parse():
    txt = open(SCRIPT).read().split("## Sources")[0]          # the numbered lists after it are not narration
    lines = []
    for m in re.finditer(r"^(\d+b?)\. \*\*(.+?)\*\*", txt, re.M):
        lines.append({"id": m.group(1), "text": m.group(2).strip()})
    order = [ln["id"] for ln in lines]
    chap_of, ci = {}, -1
    firsts = {c[2]: c for c in CHAPTERS}
    for lid in order:
        if lid in firsts:
            ci += 1
        chap_of[lid] = CHAPTERS[ci][0]
    for ln in lines:
        ln["chapter"] = chap_of[ln["id"]]
        ln["spoken"] = spoken(ln["text"])
        ln["sentences"] = [{"text": s} for s in split_sentences(ln["spoken"])]
    return lines


def split_sentences(s):
    parts = re.split(r"(?<=[.?!])\s+(?=[A-Z\"'])", s.strip())
    return [p.strip() for p in parts if p.strip()]


def take_path(text):
    h = hashlib.sha1(f"bm_george|turbo|{text}".encode()).hexdigest()[:14]
    return os.path.join(TAKES, f"{h}.wav")


def syllables(s):
    return max(1, len(re.findall(r"[aeiouy]+", s.lower())))


def build(lines, durations, estimated):
    t = LEAD_IN
    chapters = []
    prev_ch = None
    for i, ln in enumerate(lines):
        ch = ln["chapter"]
        mult = SOMBER.get(ch, 1.0)
        if ch != prev_ch:
            if prev_ch is not None:
                chapters[-1]["end"] = t
                card = [t, t + CARD_GAP]
                t += CARD_GAP
            else:
                card = None
            title = next(c[1] for c in CHAPTERS if c[0] == ch)
            chapters.append({"id": ch, "title": title, "start": card[0] if card else 0.0, "end": None, "card": card})
            prev_ch = ch
        ln["start"] = t
        for j, sent in enumerate(ln["sentences"]):
            d = durations[sent["text"]]
            sent["start"], sent["end"] = t, t + d
            t += d
            if j < len(ln["sentences"]) - 1:
                t += SENT_PAUSE * mult
        ln["end"] = t
        nxt = lines[i + 1] if i + 1 < len(lines) else None
        if nxt is not None:
            t += LINE_PAUSE * mult + SPECIAL_AFTER.get(ln["id"], 0.0)
    total = t + TAIL
    chapters[-1]["end"] = total
    return {"fps": 24, "total": round(total, 3), "estimated": estimated, "chapters": chapters, "lines": lines}


def estimate():
    lines = parse()
    dur = {}
    for ln in lines:
        for s in ln["sentences"]:
            dur[s["text"]] = syllables(s["text"]) / 4.3 + 0.15      # ~4.3 syllables/s documentary pace
    tm = build(lines, dur, estimated=True)
    json.dump(tm, open(TIMING, "w"), indent=1)
    print(f"estimated timing.json: {len(lines)} lines, {tm['total'] / 60:.2f} min")


def voice():
    import numpy as np
    import soundfile as sf
    lines = parse()
    os.makedirs(TAKES, exist_ok=True)
    todo = []
    for ln in lines:
        for s in ln["sentences"]:
            p = take_path(s["text"])
            if not os.path.exists(p):
                todo.append([s["text"], p, REF])
    if todo:
        jobs = os.path.join(TAKES, "jobs.json")
        json.dump(todo, open(jobs, "w"))
        print(f"voicing {len(todo)} takes ...", flush=True)
        env = dict(os.environ, CLONE_MODEL="turbo")
        subprocess.check_call(["/home/user/.venv-clone/bin/python", os.path.join(ROOT, "tools", "clone_tts.py"), jobs],
                              env=env)
    dur = {}
    for ln in lines:
        for s in ln["sentences"]:
            w, sr = sf.read(take_path(s["text"]))
            dur[s["text"]] = len(w) / sr
    tm = build(lines, dur, estimated=False)
    out = np.zeros(int((tm["total"] + 0.1) * SR), np.float32)
    for ln in lines:
        for s in ln["sentences"]:
            w, sr = sf.read(take_path(s["text"]), dtype="float32")
            a = int(s["start"] * SR)
            out[a:a + len(w)] += w[: len(out) - a]
    out *= 0.9 / max(1e-6, float(np.max(np.abs(out))))
    os.makedirs(os.path.dirname(OUT_WAV), exist_ok=True)
    sf.write(OUT_WAV, out, SR)
    json.dump(tm, open(TIMING, "w"), indent=1)
    print(f"narration.wav + timing.json: {len(lines)} lines, {tm['total'] / 60:.2f} min")


if __name__ == "__main__":
    if "--voice" in sys.argv:
        voice()
    else:
        estimate()
