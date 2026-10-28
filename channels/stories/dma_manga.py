"""DEAD MAN'S ALGORITHM, the manga videos: what every episode shares (the book, the cast's voices, the beat helpers and
the frame overlays). Episodes: dma_manga01.py, dma_manga02.py, ...

Pages, panel boxes and every character line come from the manga creation chat (tejassparky2/Manga, video/chNN/ +
story/chapterNN/script.yaml), copied to assets/manga/dma/chNN/. Character lines are spoken word for word as lettered;
the narrator's lines are ours and only describe what the panels show.
"""
import os

import yaml

from motion import audio, voice
from motion.engine import cue

from channels.horror import hud, hud2d, sound  # noqa: F401  (sound registers the effects)
from channels.stories import dma_kit as K, manga as M, serial

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NARRATOR = dict(turbo=True, turbo_ref="bm_george")            # the storyteller; Ren speaks in his own voice
MUSIC = "pad"                                                 # a soft ambient bed (owner: no buzzing hum)
SERIES = "DEAD MAN'S ALGORITHM · THE MANGA"


def setup():
    """The cast's voices: the eight students as before, plus the teacher and unnamed classmates (placeholders)."""
    voice.SPEAKERS.update(K.SPEAKERS)
    voice.SPEAKERS.update({
        "teacher": dict(voice="am_liam", turbo_ref="am_liam"),
        "student_a": dict(voice="af_nova", turbo_ref="af_nova"),
        "student_b": dict(voice="am_michael", turbo_ref="am_michael"),
        "student_c": dict(voice="bf_isabella", turbo_ref="bf_isabella"),
        "student_d": dict(voice="am_eric", turbo_ref="am_eric-1"),
        "student_e": dict(voice="af_sarah", turbo_ref="af_sarah"),
    })
    audio.GAINS.update(chime=0.6, click=0.6, sting=0.5)


def book(chapter=1, folder=None):
    folder = folder or os.environ.get("MANGA_PAGES") or f"assets/manga/dma/ch{chapter:02d}"
    spec = os.path.join(ROOT, f"assets/manga/dma/ch{chapter:02d}", "script.yaml")
    rows = {p["page"]: p["rows"] for p in yaml.safe_load(open(spec))["pages"]}
    return M.Manga(folder, rows)


def N(i, page, panel, text, p="m", **kw):
    """A narrator beat."""
    return dict(id=f"{p}{i}", page=page, panel=panel, text=text, **kw)


def S(i, page, panel, who, text, p="m", **kw):
    """A character beat (who = a voice.SPEAKERS key; name = the label shown, default WHO)."""
    if who.startswith("student") and "name" not in kw:
        kw["name"] = "CLASSMATE"
    return dict(id=f"{p}{i}", page=page, panel=panel, text=text, speaker=who, **kw)


def frame(cr, t, tl, R, ep, hook, last, nxt, key, hook_end=None):
    """Everything over the pages: finish, series label, the hook under the page, speaker chip + captions, the
    next-episode card, page-turn whooshes and each beat's sound effect."""
    B = tl.by_id
    hud.finish(cr, t, flash_at=[], vig=0.35, grain=0.03)
    M.series_chip(cr, f"{SERIES} · EP {ep}")
    hook_end = hook_end if hook_end is not None else B[R.beats[0]["id"]].end + 0.1
    hud2d.hook(cr, t, hook, end=hook_end, y=1095, size=78)
    if hook_end + 0.25 < t < B[last].end + 0.1:
        M.name_chip(cr, t, R.speaker(t, tl))
        hud2d.captions(cr, t, tl, key, y=1135)
    serial.next_card(cr, t, B[last].end + 0.1, SERIES, f"EPISODE {ep + 1}", nxt)
    for b in R.plan(tl):
        if b["turn"]:
            cue("whoosh", t, b["t0"] + 0.05)
        if b.get("sfx"):
            cue(b["sfx"], t, b["start"] - 0.08 + b.get("sfx_at", 0.0))
