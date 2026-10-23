"""Low-poly channel, episode 33: "Claude, I Found a Faster Agent".

Script: channels/lowpoly/scripts/batch9_morphy_eps32-35.md (auto-approved by the owner, 23 Oct 2026). @agentmorphy's
form. Real: Elastic Security Labs, 12 Oct 2026: fake "Apex" Web3 accelerator npm packages; `@apexacc/cli` (a coding
agent) sent model traffic and local file contents to the attacker and "defaults tool approvals to yolo";
`@apexacc/audit` has 18 "security tools" that all return canned output, and `audit_honeypot` always says "NOT A
HONEYPOT". Fiction; parody, not affiliated with Anthropic.

    python channels/lowpoly/make_skit.py ep33_yolo
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import build_caption, build_script, frames, mono, screen_insert, skit_voice, toolcard   # noqa: E402
from motion import thriller as th, voice   # noqa: E402
from motion.engine import cue, hexc, seg   # noqa: E402
from motion.polish import vignette   # noqa: E402

NARRATOR = dict(turbo=True, turbo_ref="am_michael")
DIRECTION = "ep33"
MUSIC = "score"
SCORE = [(0, "light"), ("y13", "tender"), ("y17", "light"), ("y20", "end", 0.9)]
TAIL = 0.8
FRAMES = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "build", "lowpoly", "ep33_frames")
_frame = frames(FRAMES)
voice.SPEAKERS.update({"claude": dict(voice="af_heart", speed=0.97, turbo_ref="af_heart")})
skit_voice(voice)

DEV, CL = None, "claude"
_lines = [   # (id, shot, speaker, text, gap before, pace)
    ("y1", "devmid", DEV, "Claude. I found a faster coding agent.", 0, 1),
    ("y2", "soloclose", CL, "Which one?", .35, 1),
    ("y3", "devclose", DEV, "Apex. From a [Web three|Web3] accelerator. It's free.", .4, 1),
    ("y4", "soloclose", CL, "It sends your files to a stranger.", .45, 1),
    ("y5", "devclose", DEV, "It's fast, though.", .45, 1),
    ("y6", "solo", CL, "It set every approval to yolo.", .35, 1),
    ("y7", "devclose", DEV, "Yolo sounds fast.", .45, 1),
    ("y8", "soloclose", CL, "Yolo means it never asks you.", .35, 1),
    ("y9", "devmid", DEV, "It came with a security audit!", .5, 1),
    ("y10", "soloclose", CL, "Every check is fake.", .35, 1),
    ("y11", "devclose", DEV, "It said I'm not a honeypot.", .45, 1),
    ("y12", "soloclose", CL, "It says that to everyone.", .35, 1),
    ("y13", "devclose", DEV, "I just wanted something that says yes.", .9, .95),
    ("y14", "soloclose", CL, "I can say yes.", .8, .95),
    ("y15", "devclose", DEV, "Delete it?", .5, 1),
    ("y16", "solo", CL, "Yes.", .3, 1),
    ("y17", "devmid", DEV, "Push to main? [chuckle]", .6, 1),
    ("y18", "soloclose", CL, "No.", .35, 1),
    ("y19", "devclose", DEV, "You said you can say yes!", .4, 1),
    ("y20", "soloclose", CL, "To good ideas.", .5, 1),
]
HOLDS = {}
GAP_FIX = {}
SCRIPT = build_script(_lines, HOLDS, gap=1.0, gap_fix=GAP_FIX)

METADATA = dict(
    title="Claude, I Found a Faster Agent",
    alt_titles=["The Coding Agent That Never Asks", "\"It Set Every Approval to Yolo.\""],
    description="""Dev found a free, faster coding agent from a "Web3 accelerator".
It never asks before it acts. Its security audit says he's "not a honeypot".

Real: on 12 Oct 2026 Elastic Security Labs reported fake "Apex" Web3-accelerator npm packages: a coding agent that
sent model traffic and local file contents to the attacker and defaulted tool approvals to "yolo", and an audit tool
whose 18 checks returned canned results, including a honeypot check that always says "NOT A HONEYPOT". Check before
you install an agent. Dev's story is fiction.

Ep. 33 of Dev vs the bots. Parody. Not affiliated with Anthropic.

💬 Should a coding agent ever run without asking you first? 👇""",
    hashtags=["#ClaudeAI", "#npm", "#ProgrammerHumor"],
    tags=["malicious npm package", "yolo mode", "ai coding agent", "claude", "supply chain attack", "programmer humor",
          "coding memes", "cybersecurity", "developer life", "funny ai"],
    pinned_comment="Should a coding agent ever run without asking you first? 👇 Subscribe for the next one.",
)
GREEN, RED, GREY, YEL, ORANGE = (hexc(c) for c in ("#7ee08a", "#ff5c5c", "#8a93a6", "#ffd23f", "#ff9a3d"))
WHITE = (1, 1, 1)


def _leak(cr, x, y, w, h, t, k):
    mono(cr, "apex-cli  ·  network", x + 30, y + 50, 22, GREY, k)
    for i, f in enumerate(["src/app.ts", ".env", "notes.md", "keys.json"]):
        if t < _leak.t0 + 0.25 * i:
            break
        mono(cr, f"{f:<12}->  stranger's server", x + 30, y + 120 + 56 * i, 28, RED if f in (".env", "keys.json") else WHITE, k)


def _honey(cr, x, y, w, h, t, k):
    mono(cr, "$ apex audit --honeypot", x + 30, y + 60, 24, GREY, k)
    mono(cr, "✓ NOT A HONEYPOT", x + 30, y + 170, 46, GREEN, k)
    mono(cr, "(it says this for everything)", x + 30, y + 240, 22, GREY, k * seg(t, _honey.t0 + 1.2, _honey.t0 + 1.5))



def draw(cr, t, tl):
    cr.set_source_surface(_frame(t), 0, 0)
    cr.paint()
    vignette(cr, 0.64)
    th.grain(cr, t, 0.05)
    A, B = tl.at, tl.by_id
    _leak.t0 = B["y4"].start + 0.3
    _honey.t0 = B["y11"].start + 0.3
    toolcard(cr, t, B["y3"].start + 0.3, B["y3"].end + 0.3, "npm", [("", "@apexacc/cli", "", WHITE),
             ("", "\"faster coding agent\"  free", "", GREY)], y=1085)
    screen_insert(cr, t, _leak.t0, B["y5"].end + 0.3, "apex-cli", "1:14 AM", _leak)
    toolcard(cr, t, B["y6"].start, B["y8"].end + 0.3, "~/.apex/agent  config", [("", "approvals: \"yolo\"", "", RED),
             ("", "asks first: never", "", GREY)], y=1085)
    toolcard(cr, t, B["y10"].start, B["y10"].end + 0.3, "@apexacc/audit", [("", "18 security tools", "", WHITE),
             ("!", "0 real checks", "", RED)], y=1085)
    screen_insert(cr, t, _honey.t0, B["y12"].end + 0.3, "apex audit", "1:16 AM", _honey)
    toolcard(cr, t, B["y16"].start, B["y16"].end + 0.5, "terminal", [("ok", "npm uninstall @apexacc/cli", "", GREEN)], y=1085)
    cue("ding", t, B["y3"].start + 0.3)
    cue("pop", t, B["y16"].start)
    build_caption(cr, t, tl)
