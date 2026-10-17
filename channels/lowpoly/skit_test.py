"""Low-poly channel (separate from Interestingly Strange): skit style test with voices, about Claude and Codex.

Owner, 17 Oct 2026: "Make the characters more expressive and add voices ... we will be making video around claude
codex" (two reference skits from @agentpoly). Original dialogue and original character designs: Dev (a tired
developer in a hoodie), Claude (an orange helper) and Codex (a blue floating robot). Parody of how the tools feel
to use; no logos, not affiliated with Anthropic or OpenAI.

The 3D picture comes from scene_skit.html (frames rendered first by make_skit.py); this module adds the voices,
captions, speaker tags and the screen cards on top, through the normal render.py pipeline.
"""
import os

from motion import engine, voice
from motion.engine import FPS, H, W, cairo, cue, hexc, seg
from motion.polish import OUTLINE, WHITE, appear, bold_text, captions, paint, rrect

NARRATOR = dict(turbo=True)          # the narrator voice is Dev: Turbo's stock voice (tags work best there)
TAIL = 1.2
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build",
                      "lowpoly", "skit_frames")

voice.SPEAKERS.update({
    "claude": dict(voice="af_heart", speed=1.0, turbo_ref="af_heart"),
    "codex": dict(voice="am_puck", speed=1.05, turbo_ref="am_puck+2"),
})

SCRIPT = [
    dict(id="s1", scene="dev", text="Claude. Fix one typo. Just one."),
    dict(id="s2", scene="claude", speaker="claude", text="On it!"),
    dict(id="s3", scene="claude", speaker="claude", text="Done! Typo fixed."),
    dict(id="s4", scene="dev", text="Why does it say four thousand lines changed?", gap=0.5),
    dict(id="s5", scene="claude", speaker="claude", text="It was a very big typo.", gap=0.45),
    dict(id="s6", scene="codex", speaker="codex", text="I can undo that!"),
    dict(id="s7", scene="dev", text="Please."),
    dict(id="s8", scene="codex", speaker="codex", text="Undone! I also undid the typo fix.", gap=0.4),
    dict(id="s9", scene="wide", text="[sigh] I'll do it myself.", gap=0.5),
]

METADATA = dict(
    title="I Asked AI to Fix One Typo 😐",
    alt_titles=["Claude vs One Typo", "When the AI Fixes Your Typo (and Everything Else)"],
    description="Style test. Parody; not affiliated with Anthropic or OpenAI.",
    hashtags=["#Claude", "#Codex", "#Shorts"],
    tags=["claude", "codex", "ai coding", "programmer humor", "developer life"],
    pinned_comment="",
)

COLORS = {None: (WHITE, hexc("#ffffff")), "claude": (hexc("#f0a070"), hexc("#ff8a3d")),
          "codex": (hexc("#a9b8ff"), hexc("#7f9bff"))}


def _frame(t):
    i = min(int(round(t * FPS)), len(os.listdir(FRAMES)) - 1)
    return cairo.ImageSurface.create_from_png(os.path.join(FRAMES, f"f{i:05d}.png"))


def card(cr, t, start, end, lines, accent):
    """A dark rounded screen card (the editor's status), popping in over the picture."""
    if not (start <= t < end):
        return
    k = appear(t, start, 0.25) * (1 - seg(t, end - 0.15, end))
    cr.save()
    cr.translate(W / 2, 360)
    cr.scale(0.9 + 0.1 * k, 0.9 + 0.1 * k)
    rrect(cr, -290, -110, 580, 220, 26)
    cr.set_source_rgba(0.07, 0.08, 0.11, 0.92 * k)
    cr.fill_preserve()
    cr.set_source_rgba(*accent[:3], k)
    cr.set_line_width(4)
    cr.stroke()
    for i, (txt, col, size) in enumerate(lines):
        bold_text(cr, txt, 0, -38 + i * 78, size, (*col[:3], k), outline=None, shadow=0)
    cr.restore()


def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    A = tl.at
    card(cr, t, A("s2", "On"), A("s3"), [("Editing files…", hexc("#e8834a"), 44), ("● ● ●", WHITE, 36)],
         hexc("#e8834a"))
    card(cr, t, A("s4"), A("s4", end=True) + 0.3, [("✓ 1 typo fixed", hexc("#7ee08a"), 46),
                                                    ("4,203 lines changed", hexc("#ff6b6b"), 50)], hexc("#ff6b6b"))
    card(cr, t, A("s8", "also"), A("s8", end=True) + 0.4, [("↩ Undone", hexc("#6f8cff"), 46),
                                                         ("typo: still there", hexc("#ffd23f"), 46)], hexc("#6f8cff"))
    if A("s4") <= t < A("s4") + 0.05:
        cue("hit", t, A("s4"))
    who = None                                        # captions take the speaker's colour (Claude orange)
    for b in tl.beats:
        if b.start - 0.1 <= t:
            who = b.speaker
    captions(cr, t, tl, y=980, colors=COLORS.get(who, COLORS[None]))
