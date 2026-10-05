"""The host-and-Globe news format, shared by every news video: script helper (two voices, pauses at each hand-over),
background, camera that cuts to whoever speaks, the two characters, and the end screen with YES / NO buttons.

A video only writes its lines, its upload sheet and its pop-up panels (see videos/diesel_g7_release.py)."""
import math

from .captions import captions
from .characters import person
from .engine import RED, blob, hexc, line, shape
from .kit import camera, hl, whip
from .news import GREEN, PAPER, SKY, globe
from .story import buttons

H, G = "reporter", "globe"
HOST_X, GLOBE_X, GROUND = 170, 530, 960
TWO = (0.95, 360, 700)
HOST_CLOSE = (1.75, 190, 770)
GLOBE_CLOSE = (1.2, 530, 640)
GLOBE_VOICE = "bm_george"   # the Globe's own Kokoro voice; the host keeps the channel narrator (am_fenrir)


def dialogue(lines, globe_voice=GLOBE_VOICE, globe_pace=1.12, turn_gap=0.36):
    """SCRIPT from [(id, scene, "H" or "G", text)]: the Globe gets its own voice, and there is a clear pause
    whenever the other one starts talking."""
    script = []
    for i, (bid, scene, who, text) in enumerate(lines):
        spec = dict(id=bid, scene=scene, text=text, speaker=H if who == "H" else G)
        if i and who != lines[i - 1][2]:
            spec["gap"] = turn_gap
        if who == "G":
            spec.update(voice=globe_voice, pace=globe_pace)   # George reads slower than the host; match their pace
        script.append(spec)
    return script


def background(cr, t, keys):
    cr.set_source_rgba(*SKY)
    cr.paint()
    z, fx, fy = camera(t, keys, dur=0.22)
    cr.translate(360, 640)
    cr.scale(z, z)
    cr.translate(-fx, -fy)
    for k in range(5):
        blob(cr, 360, 560, 520 - k * 110, 330, None, 9000 + k, amp=0.6, lw=2.5, stroke=hexc("#ffffff", 0.55))
    for k in range(-2, 3):
        line(cr, [(-200, 560 + k * 120), (920, 560 + k * 120)], 2.5, hexc("#ffffff", 0.45), 9010 + k, amp=0.8)
    shape(cr, [(-700, GROUND), (1500, GROUND), (1500, 2600), (-700, 2600)], PAPER, seed=9020, amp=0.5, lw=4)


def cam_keys(tl, extra=()):
    keys = [(0, TWO)]
    for b in tl.beats:
        if b.scene == "talk":
            keys.append((b.start - 0.05, HOST_CLOSE if b.speaker == H else GLOBE_CLOSE))
    return keys + list(extra)


def host(cr, t, tl, **kw):
    k = dict(facing=1, arms=("hip", "hip"), eyes="dot", mouth="smile")
    k.update(kw)
    if tl.speaking(H, t):
        k["mouth"] = "o" if int(t * 12) % 2 else k["mouth"]
    person(cr, H, HOST_X, GROUND, t, **k)


def talking_globe(cr, t, tl, code, eyes="dot", idle="smile"):
    talking = tl.speaking(G, t)
    mouth = ("o" if int(t * 12) % 2 else idle) if talking else idle
    globe(cr, code, GLOBE_X, GROUND, t, eyes=eyes, mouth=mouth, look=-1,
          bounce=abs(math.sin(t * 9)) * 3 if talking else 0)


def mood(t, tl, moods, default):
    """Pick a face from [(beat_id, value)] by the latest beat that has started."""
    v = default
    for bid, val in moods:
        if t >= tl.at(bid):
            v = val
    return v


def end_scene(cr, t, tl, code, last_id, headline, prop=None, labels=(("YES", GREEN), ("NO", RED))):
    """The last line: both characters in shot, the question as a headline, an optional prop, YES / NO buttons."""
    from .news import panel
    A = tl.at
    background(cr, t, [(A(last_id) - 0.4, TWO)])
    host(cr, t, tl, arms=("point", "hip"), eyes="happy")
    talking_globe(cr, t, tl, code, "wide", "smile")
    cr.identity_matrix()
    hl(cr, t, headline, 215, 58, A(last_id), bold=True, underline=True)
    if prop:
        panel(cr, t, A(last_id) + 0.3, 999, 360, 380, 360, 190, prop, seed=9600)
    buttons(cr, t, A(last_id, "comments"), labels, y=530, s=0.75)


def make_draw(scenes):
    def draw(cr, t, tl):
        name, start, _ = tl.scene_at(t)
        cr.save()
        whip(cr, t, start)
        scenes[name](cr, t, tl)
        cr.restore()
        captions(cr, t, tl)
    return draw
