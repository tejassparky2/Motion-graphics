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
    turn_pause: float = 0.32  # when a line starts as narration and a character takes over at `speaker_from`
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


# Full-stop pauses, measured from the reference narrators (see out/voice_rhythm.md)
SENTENCE_TAKES = True
STOP_PAUSE = 0.24
QUESTION_PAUSE = 0.30
BEAT_GAP = 0.24          # minimum silence between two script lines (each line ends a sentence)
_ABBREV = {"mr.", "mrs.", "ms.", "dr.", "st.", "p.s.", "vs.", "etc."}


def _sentence_end(w):
    lw = w.lower().strip('"\'”’)')
    if lw in _ABBREV or len(lw) <= 2 and lw.endswith("."):   # "Mr.", "A." and similar aren't sentence ends
        return False
    return lw.endswith((".", "?", "!", "...", ":"))


def clear_dialogue(script, ids=None, pace=0.9, turn_gap=0.42):
    """Riddles and their answers, read a little slower, with a clear pause whenever the voice changes hands.

    `ids` picks the beats to slow down (default: every line a character speaks)."""
    prev = None
    for spec in script:
        who = spec.get("speaker")
        if (ids is None and who) or (ids is not None and spec["id"] in ids):
            spec.setdefault("pace", pace)
        if prev is not None and (who != prev or (ids is not None and spec["id"] in ids)):
            spec["gap"] = max(spec.get("gap", 0.18), turn_gap)
        prev = who
    return script


def _norm(s):
    return re.sub(r"[^a-z0-9₹.,]", "", s.lower())


class Timeline:
    def __init__(self, script, lead_in=0.12, tail=0.35):
        self.beats = []
        t = lead_in
        for i, spec in enumerate(script):
            b = Beat(**spec)
            b.units = parse(b.text)
            b.audio, wt = self._speak(b)
            b.gap = max(b.gap, BEAT_GAP)
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

    @staticmethod
    def _takes(b):
        """The beat's spoken words cut into takes: one per sentence, plus a cut where a character takes over.
        Returns [(first word, last word + 1)] and the pause after each take but the last."""
        words = b.spoken_text.split()
        if b.spoken_text in voice._EXTERNAL or not SENTENCE_TAKES:
            return [(0, len(words))], []
        turn = -1
        if b.speaker_from:
            k, n = _norm(b.speaker_from), 0
            for u in b.units:
                if k in _norm(u.shown) or k in _norm(" ".join(u.spoken)):
                    turn = n
                    break
                n += len(u.spoken)
        cuts, pauses = [0], []
        for n, w in enumerate(words[:-1], 1):
            if n == turn:
                cuts.append(n)
                pauses.append(max(b.turn_pause, STOP_PAUSE))
            elif _sentence_end(w):
                cuts.append(n)
                pauses.append(QUESTION_PAUSE if w.endswith("?") else STOP_PAUSE)
        cuts.append(len(words))
        return list(zip(cuts, cuts[1:])), pauses

    @staticmethod
    def _speak(b):
        """Audio and per-word times for a beat, read the way a person would: every sentence is its own take, joined
        with a full-stop pause, so sentences never blur into each other. Where a line switches from narrator to
        character (`speaker_from`), the pause is a little longer."""
        import numpy as np
        words = b.spoken_text.split()
        spans, pauses = Timeline._takes(b)
        audio, times, off = [], [], 0.0
        for c, (a0, a1) in enumerate(spans):
            text = " ".join(words[a0:a1])
            who = Timeline._who(b, a0)
            clip = voice.synth(text, b.pace, who)
            times += [(s0 + off, e0 + off) for s0, e0 in voice.word_times(text, clip, b.pace, who)]
            audio.append(clip)
            off += len(clip) / voice.SR
            if c < len(pauses):
                audio.append(np.zeros(int(pauses[c] * voice.SR)))
                off += pauses[c]
        return np.concatenate(audio), times

    @staticmethod
    def _who(b, first_word):
        """Who speaks the take starting at `first_word`: the beat's speaker from `speaker_from` on (or the whole
        line if there's no `speaker_from`), otherwise the narrator (None)."""
        if not b.speaker:
            return None
        if not b.speaker_from:
            return b.speaker
        k, n = _norm(b.speaker_from), 0
        for u in b.units:
            if k in _norm(u.shown) or k in _norm(" ".join(u.spoken)):
                return b.speaker if first_word >= n else None
            n += len(u.spoken)
        return None

    @staticmethod
    def sentences(script):
        """Every take the script needs, so a slow voice engine can generate them all in one batch."""
        out = []
        for spec in script:
            b = Beat(**spec)
            b.units = parse(b.text)
            words = b.spoken_text.split()
            out += [(" ".join(words[a0:a1]), b.pace) for a0, a1 in Timeline._takes(b)[0]
                    if Timeline._who(b, a0) not in voice.CAST_VOICES]   # character voices aren't the clone
        return out

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
