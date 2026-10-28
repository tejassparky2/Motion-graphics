"""DEAD MAN'S ALGORITHM, the manga, Episode 3 (9:16): Chapter 1 "12:17", pages 15-21. Ren counts twenty, the teacher is
gone, no signal and no clock, the door won't move, Aoi: "This room was built... for us.", the cameras, the screen
(20 SURVIVORS, STATUS OF EARTH: UNKNOWN), the student records, and Momo's first words. Ends on Riku's "What the hell
ARE you?!", which Momo doesn't answer (page 22 opens the Glass Auction).

Every character line is word for word as lettered on the manga chat's pages (unnamed classmates are its placeholders
STUDENT E-L, shown as CLASSMATE; Ren's thought bubbles are spoken in his voice); the narrator only describes what the
panels show. The phone shows no time and the teacher's fate is unresolved in the manga's ledger, so the narration
says neither.

    /home/user/.venv-main/bin/python channels/horror/make_2d.py dma_manga03   -> out/stories/dma_manga03.mp4
"""
from motion.engine import cue

from channels.stories import manga as M
from channels.stories.dma_manga import MUSIC, NARRATOR, N, S, book, frame, setup  # noqa: F401  (render reads both)

TAIL = 2.0
setup()
BOOK = book(1)


def n(i, page, panel, text, **kw):
    return N(i, page, panel, text, p="g", **kw)


def s(i, page, panel, who, text, **kw):
    return S(i, page, panel, who, text, p="g", **kw)


BEATS = [
    n(1, 15, 1, "Concrete walls. A huge metal door. A dark screen."),
    s(2, 15, 1, "ren", "Eighteen. Nineteen. Twenty.", gap=0.4),
    s(3, 15, 2, "ren", "[Where is Sensei?|Where's Sensei?]", gap=0.4),          # "Where's" was heard "We're"
    s(4, 15, 3, "student_e", "[Sensei's not here.|Sensei's not here...]", gap=0.35),
    n(5, 16, 1, "Everyone reached for their phones.", gap=0.4),
    s(6, 16, 1, "student_a", "[No signal.|No signal...]", gap=0.3),
    s(7, 16, 1, "student_b", "Mine too!", gap=0.25),
    n(8, 16, 2, "No service. And no clock. Nobody knew how long they'd been out.", gap=0.4),
    s(9, 16, 3, "student_b", "[Let us out!|Let us out!!]", gap=0.3, impact=True),   # bf_isabella's was heard "Letters out"
    s(10, 16, 3, "student_d", "[Is anyone there?|Is anyone there?!]", gap=0.2),
    n(11, 16, 4, "Go and Riku threw their shoulders into the door.", gap=0.35, sfx="thud"),
    s(12, 16, 4, "riku", "Open, damn it!", gap=0.3, impact=True),
    n(13, 17, 1, "Riku kicked it. It didn't move.", sfx="hit"),
    s(14, 17, 1, "riku", "[Damn it!|Damn it!!]", gap=0.25),
    n(15, 17, 2, "Fujimoto Aoi knelt by the door. She studied its edges.", gap=0.4),   # "Aoi knelt" was heard "I knelt"
    s(16, 17, 3, "aoi", "[This is not a school door someone modified.|This isn't a school door someone modified.]",
      gap=0.35),
    s(17, 17, 4, "aoi", "[This room was built for us.|This room was built... for us.]", gap=0.4),
    n(18, 17, 5, "Ren looked up. In the corner of the ceiling, a small lens.", gap=0.45),
    s(19, 17, 5, "ren", "Cameras.", gap=0.35),
    n(20, 18, 1, "Then the screen woke up.", gap=0.5, sfx="static"),
    n(21, 18, 2, "[Class three B.|Class 3-B.] [Twenty|20] students. [Twenty|20] survivors.",
      gap=0.4),
    n(22, 18, 2, "[Event zero zero.|Event 00:] Impact.", gap=0.35),
    n(23, 18, 2, "Status of Earth. Unknown.", gap=0.45),          # its sting comes after the line (cues)
    s(24, 18, 3, "haruto", "[Survivors?|Survivors...?]", gap=0.5),
    s(25, 18, 3, "student_d", "[Status of Earth. Unknown?|Status of Earth... unknown?]", gap=0.3),
    n(26, 19, 1, "Then a list. Names. Birthdays. Blood types.", gap=0.4),
    n(27, 19, 2, "Some fields were blurred. But none of them were empty.", gap=0.35),
    s(28, 19, 3, "student_a", "[That's my birthday.|That's my birthday...]", gap=0.35),
    s(29, 19, 3, "student_e", "[My blood type.|My blood type—]", gap=0.2),
    s(30, 19, 4, "ren", "Birthdays. Blood types. Medical records. Emergency contacts.", gap=0.4),
    s(31, 19, 4, "ren", "It knows all twenty of us.", gap=0.35),
    n(32, 20, 1, "Under the screen, a small hatch slid open.", gap=0.6, sfx="click"),
    n(33, 20, 2, "Something small and white. And a bell.", gap=0.35, sfx="chime"),
    s(34, 20, 3, "momo", "[Hello, hello, Class three B!|Hello, hello, Class 3-B!]", gap=0.35),
    n(35, 20, 4, "Nobody moved.", gap=0.4),
    s(36, 21, 1, "momo", "I am the administrator of Dead Man's Algorithm.", gap=0.6),
    n(37, 21, 2, "Silence.", gap=0.4),
    s(38, 21, 3, "momo", "This is usually the part where someone screams.", gap=0.5),
    s(39, 21, 4, "riku", "[What the hell are you?|What the hell ARE you?!]", gap=0.4, impact=True),
    n(40, 21, 0, "Momo didn't answer.", gap=0.6),
]
R = M.Reader(BOOK, BEATS)
SCRIPT = R.script()

METADATA = dict(
    title="20 Survivors. Status of Earth: Unknown | Dead Man's Algorithm Manga Ep 3 ☄️",
    alt_titles=["They Woke Up in a Sealed Room. Then It Said Hello 🐭",
                "Dead Man's Algorithm: The Manga, Episode 3 ☄️"],
    description="""Twenty students in a concrete room. No teacher. No signal. No clock.
Then a screen: 20 SURVIVORS. STATUS OF EARTH: UNKNOWN.
It knows every birthday and blood type in the class. And then something small and white says hello.

Dead Man's Algorithm, the manga, Chapter 1 "12:17", pages 15 to 21.
Episode 4 is next: the first game.

(Original story. Original manga, read with voices.)""",
    hashtags=["#DeadMansAlgorithm", "#Manga", "#Shorts"],
    tags=["dead mans algorithm", "manga", "manga recap", "manga dub", "survival game", "death game",
          "psychological thriller", "original manga", "momo", "episode 3"],
    pinned_comment="No teacher, no clock, and a screen that knows everyone's blood type. Where do you think "
                   "Sensei went? 👇",
)

KEY = {"twenty", "sensei", "signal", "clock", "door", "damn", "moved", "aoi", "built", "cameras", "screen",
       "survivors", "impact", "earth", "unknown", "birthdays", "birthday", "blood", "empty", "medical", "emergency",
       "knows", "hatch", "white", "bell", "hello", "administrator", "algorithm", "silence", "screams", "hell",
       "answer"}


def cues(t, tl):
    """This episode's sound cues (shared with the Chapter 1 long video)."""
    B = tl.by_id
    cue("heartbeat", t, B["g18"].start, B["g20"].start - B["g18"].start)
    cue("riser", t, B["g20"].start, B["g23"].start - B["g20"].start)
    cue("sting", t, B["g23"].end + 0.05)                      # under the sting it was heard "The status of Earth"
    cue("heartbeat", t, B["g30"].start, B["g32"].start - B["g30"].start)
    cue("hush", t, B["g35"].start - 0.2, B["g36"].start - B["g35"].start + 0.1)       # nobody moved
    cue("hush", t, B["g37"].start - 0.2, B["g38"].start - B["g37"].start + 0.1)       # silence
    cue("riser", t, B["g38"].start, B["g39"].start - B["g38"].start)


def draw(cr, t, tl):
    B = tl.by_id
    R.draw(cr, t, tl)
    frame(cr, t, tl, R, 3, [("20 SURVIVORS.", False), ("OF WHAT?", True)], "g40", "THE GLASS AUCTION", KEY)
    cues(t, tl)
