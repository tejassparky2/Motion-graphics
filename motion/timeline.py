"""Narration-driven timeline.

The script is a list of beats. Each beat's audio is synthesized, trimmed and laid end-to-end with a small gap,
so the video's timing *follows the voice* — there is no dead air to fill. Scenes ask the timeline when a beat
starts or when a particular word is spoken, and animate to that.

Script markup: `[spoken words|shown]` says one thing and shows another in the captions, e.g.
`[a hundred rupees|₹100]`. Punctuation right after the bracket is kept.
"""
import re
import sys
from dataclasses import dataclass, field

from . import voice

TOKEN = re.compile(r"\[([^|\]]+)\|([^\]]+)\]([^\s\[]*)|(\S+)")


@dataclass
class Unit:
    spoken: list          # spoken words
    shown: str            # caption text
    start: float = 0.0
    end: float = 0.0


@dataclass
class Beat:
    id: str
    scene: str
    text: str
    speaker: str = None   # character whose mouth moves (from the word `speaker_from` on)
    speaker_from: str = None
    gap: float = 0.18     # silence before this beat
    pace: float = 1.0     # speed multiplier for this line (<1 = slower, for emphasis)
    units: list = field(default_factory=list)
    start: float = 0.0
    end: float = 0.0
    audio: object = None

    @property
    def spoken_text(self):
        return " ".join(w for u in self.units for w in u.spoken)


def parse(text):
    units = []
    for m in TOKEN.finditer(text):
        if m.group(1):
            spoken = m.group(1).split()
            suffix = m.group(3) or ""
            spoken[-1] += suffix
            units.append(Unit(spoken, m.group(2) + suffix))
        else:
            units.append(Unit([m.group(4)], m.group(4)))
    return units


def _norm(s):
    return re.sub(r"[^a-z0-9₹.,]", "", s.lower())


class Timeline:
    def __init__(self, script, lead_in=0.12, tail=0.35):
        self.beats = []
        t = lead_in
        for i, spec in enumerate(script):
            b = Beat(**spec)
            b.units = parse(b.text)
            b.audio = voice.synth(b.spoken_text, b.pace)
            wt = voice.word_times(b.spoken_text, b.audio, b.pace)
            if i:
                t += b.gap
            b.start = t
            b.end = t + len(b.audio) / voice.SR
            k = 0
            for u in b.units:
                n = len(u.spoken)
                u.start = b.start + wt[k][0]
                u.end = b.start + wt[k + n - 1][1]
                k += n
            t = b.end
            self.beats.append(b)
        self.total = t + tail
        self.by_id = {b.id: b for b in self.beats}
        # scenes: contiguous runs of beats; a scene starts where its first beat's gap starts
        self.scenes = []
        for b in self.beats:
            if not self.scenes or self.scenes[-1][0] != b.scene:
                start = 0.0 if not self.scenes else b.start - b.gap
                if self.scenes:
                    self.scenes[-1][2] = start
                self.scenes.append([b.scene, start, None])
        self.scenes[-1][2] = self.total

    # ---- queries used by scenes
    def at(self, beat_id, key=None, end=False, nth=1):
        """Time a beat starts (or ends), or when the `nth` unit matching `key` starts (or ends)."""
        b = self.by_id[beat_id]
        if key is None:
            return b.end if end else b.start
        k = _norm(key)
        seen = 0
        for u in b.units:
            if k in _norm(u.shown) or k in _norm(" ".join(u.spoken)):
                seen += 1
                if seen == nth:
                    return u.end if end else u.start
        raise KeyError(f"{key!r} not found in beat {beat_id}: {b.text}")

    def scene_at(self, t):
        for name, s, e in self.scenes:
            if t < e:
                return name, s, e
        return self.scenes[-1]

    def speaking(self, who, t):
        """True while `who` is saying a word (for lip flap)."""
        for b in self.beats:
            if b.speaker != who or not (b.start <= t <= b.end):
                continue
            t0 = self.at(b.id, b.speaker_from) if b.speaker_from else b.start
            if t < t0:
                return False
            return any(u.start <= t <= u.end for u in b.units)
        return False

    def clips(self):
        return [(b.start, b.audio) for b in self.beats]

    def report(self):
        words = sum(len(u.spoken) for b in self.beats for u in b.units)
        speech = sum(b.end - b.start for b in self.beats)
        gaps = [b.start - a.end for a, b in zip(self.beats, self.beats[1:])]
        print(f"narration: {words} words, {speech:.1f}s of speech in {self.total:.1f}s "
              f"({100 * speech / self.total:.0f}% coverage), {60 * words / speech:.0f} wpm while speaking, "
              f"max gap between lines {max(gaps):.2f}s", file=sys.stderr)
