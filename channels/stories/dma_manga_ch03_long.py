"""DEAD MAN'S ALGORITHM, the manga, Chapter 3 "The Charity" as one long video (16:9) for the YouTube channel's long-form
tab (owner, 28 Oct 2026: "Make chapter 3 long video too").

The three Shorts' beats in reading order (Episode 7 pages 1-6, Episode 8 pages 7-12, Episode 9 pages 13-19), with the
same voices and takes, so every line has already passed Whisper medium in its Short. A short silent chapter title
over the white room opens it; the Shorts' hooks and "next episode" cards are left out; the chapter ends on "CHAPTER
4 · FIND YOURSELF".

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga_ch03_long   -> out/stories/dma_manga_ch03_long.mp4
"""
from motion.engine import W, H, clamp01, cue

from channels.horror import hud, hud2d
from channels.stories import manga as M, serial
from channels.stories.dma_manga import MUSIC, NARRATOR, book, setup  # noqa: F401  (render reads both)
from channels.stories.dma_manga import SERIES as NAME     # not SERIES: the pipeline would add a second chip
from channels.stories import dma_manga07 as E7, dma_manga08 as E8, dma_manga09 as E9

TAIL = 4.0
setup()
BOOK = book(3)
EPISODES = (E7, E8, E9)
TITLE = dict(id="t0", page=1, panel=0, text="", hold=2.4)
BEATS = [TITLE] + [b for e in EPISODES for b in e.BEATS]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()
KEY = set().union(*(e.KEY for e in EPISODES))

METADATA = dict(
    title="Dead Man's Algorithm, Chapter 3: The Charity | Original Manga Read With Voices 🪙",
    alt_titles=["The Poorest Player Dies. So They Gave Everything Away | Dead Man's Algorithm Ch. 3",
                "I Found the Loophole. He Found the Loophole in My Loophole | Dead Man's Algorithm Ch. 3"],
    description="""Game two: the Charity. Nobody can take your tokens. You may give tokens to anyone in this room. When
time runs out, the poorest player dies, and a tie for poorest kills them all. Zero tokens, and you're not a player.
Ren finds the loophole: Momo is in the room, and Momo isn't a player. Give Momo everything, and nobody dies.
Then, with three seconds left, Riku puts one token in Saki's hand.

Dead Man's Algorithm, Chapter 3 "The Charity": the whole chapter, every page, with a narrator and a voice for every
character.

Chapter 4, "Find Yourself", is next.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#DeathGame"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "full chapter", "survival game", "death game",
          "psychological thriller", "original manga", "charity", "loophole", "chapter 3"],
    pinned_comment="Should Saki have given the token to Momo? Riku would have died, and she would have lived. What "
                   "would you have done? 👇",
)


def chapter_title(cr, t, end):
    """CHAPTER 3 · THE CHARITY over the white room, before the first line."""
    if t > end + 0.4:
        return
    a = clamp01(t / 0.3) * (1 - clamp01((t - end) / 0.4))
    cr.save()
    cr.push_group()
    cr.set_source_rgba(0.01, 0.01, 0.02, 0.78)
    cr.paint()
    hud2d._text(cr, "DEAD MAN'S ALGORITHM", W / 2, H * 0.36, 30, (1, 0.85, 0.4, 1), hud2d.ROUND, "center")
    hud2d._text(cr, "CHAPTER 3", W / 2, H * 0.53, 96, (1, 1, 1, 1), hud2d.ROUND, "center", shadow=0.6)
    hud2d._text(cr, "THE CHARITY", W / 2, H * 0.66, 54, hud2d.RED, hud2d.ROUND, "center", shadow=0.5)
    cr.pop_group_to_source()
    cr.paint_with_alpha(a)
    cr.restore()


def draw(cr, t, tl):
    B = tl.by_id
    R.draw(cr, t, tl)
    last = BEATS[-1]["id"]
    hud.finish(cr, t, flash_at=[], vig=0.3, grain=0.03)
    M.series_chip(cr, f"{NAME} · CHAPTER 3")
    chapter_title(cr, t, B["t0"].end)
    if B["t0"].end + 0.3 < t < B[last].end + 0.1:
        M.name_chip(cr, t, R.speaker(t, tl))
        hud2d.captions(cr, t, tl, KEY, y=H - 34, size=40, max_w=1000)
    serial.next_card(cr, t, B[last].end + 0.6, NAME, "CHAPTER 4", "FIND YOURSELF")
    for b in R.plan(tl):
        if b["turn"]:
            cue("whoosh", t, b["t0"] + 0.05)
        if b.get("sfx"):
            cue(b["sfx"], t, b["start"] - 0.08 + b.get("sfx_at", 0.0))
    for e in EPISODES:
        e.cues(t, tl)
