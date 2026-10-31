"""Read the episode clock (timing.json, written by narration.py) from any package.

    from channels.ww2.ep01.timing import Timing
    T = Timing()
    T.line("33").start, T.line("33").end        # seconds from the episode start
    T.sentence("35", 1).start                   # the 2nd sentence of line 35 ("Lightning war.")
    T.chapter("C2").card                        # (start, end) of the chapter card, or None for the cold open
    T.total

timing.json is provisional (estimated from word counts) until the voiced narration lands; re-read it, never copy
numbers into code. Everything in a package should be placed relative to line/sentence times.
"""
import json
import os
from types import SimpleNamespace

HERE = os.path.dirname(os.path.abspath(__file__))


class Timing:
    def __init__(self, path=os.path.join(HERE, "timing.json")):
        d = json.load(open(path))
        self.fps, self.total, self.estimated = d["fps"], d["total"], d.get("estimated", True)
        self._lines = {ln["id"]: ln for ln in d["lines"]}
        self._chapters = {c["id"]: c for c in d["chapters"]}
        self.order = [ln["id"] for ln in d["lines"]]

    def line(self, lid):
        ln = self._lines[str(lid)]
        return SimpleNamespace(id=ln["id"], start=ln["start"], end=ln["end"], text=ln["text"],
                               chapter=ln["chapter"], dur=ln["end"] - ln["start"])

    def sentence(self, lid, k):
        s = self._lines[str(lid)]["sentences"][k]
        return SimpleNamespace(start=s["start"], end=s["end"], text=s["text"])

    def chapter(self, cid):
        c = self._chapters[cid]
        return SimpleNamespace(id=cid, title=c["title"], start=c["start"], end=c["end"],
                               card=tuple(c["card"]) if c["card"] else None)

    def lines_between(self, first, last):
        a, b = self.order.index(str(first)), self.order.index(str(last))
        return [self.line(x) for x in self.order[a:b + 1]]


# The 8 work packages (SHOTLIST.md): (name, first line, last line). Each renders one contiguous clip.
PACKAGES = [("P1", "1", "16"), ("P2", "17", "35"), ("P3", "36", "53"), ("P4", "54", "69"),
            ("P5", "70", "86"), ("P6", "87", "101"), ("P7", "102", "116"), ("P8", "117", "131")]


def _boundary(T, lid):
    """Where a package starting at line `lid` begins: its chapter card's start if the line opens a chapter (the
    card belongs to the package), else halfway through the pause before the line (never mid-word)."""
    i = T.order.index(lid)
    if i == 0:
        return 0.0
    ln, prev = T.line(lid), T.line(T.order[i - 1])
    if ln.chapter != prev.chapter:
        return T.chapter(ln.chapter).card[0]
    return (prev.end + ln.start) / 2


def package_span(name, T=None):
    """(start, end) in episode seconds of package `name`, frame-aligned; the last package ends at T.total."""
    T = T or Timing()
    names = [p[0] for p in PACKAGES]
    k = names.index(name)
    a = _boundary(T, PACKAGES[k][1])
    b = _boundary(T, PACKAGES[k + 1][1]) if k + 1 < len(PACKAGES) else T.total
    fa, fb = round(a * T.fps), round(b * T.fps)
    return fa / T.fps, fb / T.fps
