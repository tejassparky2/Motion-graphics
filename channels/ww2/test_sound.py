"""Checks for channels/ww2/sound.py: every generator is finite, non-silent and deterministic; music cues come out the
asked length; the mix ducks music under the narration, cuts to silence, and the limiter holds its ceiling.

    python -m pytest channels/ww2/test_sound.py -q
"""
import numpy as np

from channels.ww2 import sound as s

SHORT = dict(tension=(3.0,), march=(3.0,), somber=(3.0,), low_tone=(3.0,), triumph=(3.0,), drum_hit=(),
             gun_boom=(), artillery=(), artillery_barrage=(2.0,), tank=(2.0,), plane_drone=(2.0,), dive_whine=(1.5,),
             explosion=(), rifle_crack=(), sea_waves=(3.0,), blizzard=(3.0,), radio_static=(1.0,),
             voice_crackle=(1.5,), morse=("SOS",), typewriter=(1.5,), stamp=(), page_whoosh=(),
             crowd_cheer=(2.0,), clock_tick=(2.0,), train=(2.0,), door_slam=())


def test_every_generator():
    for name, fn in {**s.MUSIC, **s.SFX}.items():
        a, b = fn(*SHORT[name]), fn(*SHORT[name])
        assert np.all(np.isfinite(a)), name
        assert 0.5 < np.max(np.abs(a)) <= 0.9 + 1e-9, name
        assert np.array_equal(a, b), f"{name} is not deterministic"


def test_music_length():
    for name in ("tension", "march", "somber", "low_tone", "triumph"):
        assert len(s.MUSIC[name](4.3)) == s._n(4.3), name


def test_mix_ducks_and_cuts():
    m = s.Mix(4.0)
    m.music(s.low_tone(4.0), 0.0, -10)
    m.cut(3.0, 3.5)
    voice = np.zeros(s._n(4.0))
    voice[s._n(1.0):s._n(2.0)] = 0.3 * np.sin(2 * np.pi * 200 * s._t(s._n(1.0)))
    dry, wet = m.render(), m.render(voice)
    music = wet - voice[:, None]                                       # the bed under the voice

    def rms(x, a, b):
        return np.sqrt(np.mean(x[s._n(a):s._n(b)] ** 2))
    assert rms(music, 1.3, 1.9) < rms(dry, 1.3, 1.9) * s._db(-8)       # ~10 dB down while the voice speaks
    assert rms(music, 2.8, 2.95) > rms(dry, 2.8, 2.95) * s._db(-3)     # recovered before the cut
    assert np.max(np.abs(dry[s._n(3.01):s._n(3.49)])) == 0              # the hard cut is silent


def test_limiter_ceiling():
    x = np.stack([np.sin(2 * np.pi * 997 * s._t(s._n(1.0)))] * 2, 1) * 2.0
    y = s.limit(x, -1.5)
    assert np.max(np.abs(y[s._n(0.01):])) <= s._db(-1.5) * 1.01
