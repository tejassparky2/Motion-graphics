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
