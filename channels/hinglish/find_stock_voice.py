"""Find the stock voice behind a reference narration in ElevenLabs' public Voice Library.

Lists male Hindi library voices (narration / educational / storytelling use cases first), downloads each voice's
public preview clip (the Hindi preview where the library has one), and ranks them by speaker-embedding similarity to
the reference clips. Previews are public sample files: this spends no ElevenLabs characters. Nothing is cloned; the
match is then used through ElevenLabs under its normal licence.

Needs ELEVENLABS_API_KEY (the library only allows filtering when logged in).
Usage: python -I -X utf8 channels/hinglish/find_stock_voice.py "<shorts research>\\mayank\\voice" [max_voices]
"""
import glob, json, os, sys, urllib.parse, urllib.request
import numpy as np
from resemblyzer import VoiceEncoder, preprocess_wav
import librosa

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from narrate import _key  # noqa: E402

USE_CASES = ["narrative_story", "informative_educational", "entertainment_tv", "social_media", None]


def get(url, k):
    req = urllib.request.Request(url, headers={"xi-api-key": k, "User-Agent": "HinglishVoiceSearch/0.1"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def library(k, limit):
    seen, out = set(), []
    for uc in USE_CASES:
        page = 0
        while len(out) < limit:
            q = {"page_size": 100, "page": page, "language": "hi", "gender": "male", "sort": "usage_character_count_1y"}
            if uc:
                q["use_cases"] = uc
            d = json.loads(get("https://api.elevenlabs.io/v1/shared-voices?" + urllib.parse.urlencode(q), k))
            for v in d.get("voices", []):
                if v["voice_id"] not in seen:
                    seen.add(v["voice_id"])
                    out.append(v)
            if not d.get("has_more"):
                break
            page += 1
    return out[:limit]


def preview_url(v):
    for vl in v.get("verified_languages") or []:
        if vl.get("language") == "hi" and vl.get("preview_url"):
            return vl["preview_url"]
    return v.get("preview_url")


def main():
    vdir = sys.argv[1]
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 400
    k = _key("ELEVENLABS_API_KEY")
    if not k:
        sys.exit("ELEVENLABS_API_KEY is not set")
    pdir = os.path.join(vdir, "library_previews")
    os.makedirs(pdir, exist_ok=True)
    voices = library(k, limit)
    print(f"{len(voices)} male Hindi library voices")
    enc = VoiceEncoder(verbose=False)
    refs = [enc.embed_utterance(preprocess_wav(r)) for r in sorted(glob.glob(os.path.join(vdir, "ref_*.wav")))]
    centroid = np.mean(refs, axis=0)
    centroid /= np.linalg.norm(centroid)
    rows = []
    for v in voices:
        url = preview_url(v)
        if not url:
            continue
        f = os.path.join(pdir, f"{v['voice_id']}.mp3")
        try:
            if not os.path.exists(f):
                urllib.request.urlretrieve(url, f)
            y, _ = librosa.load(f, sr=16000)
            sim = float(np.dot(enc.embed_utterance(preprocess_wav(y, source_sr=16000)), centroid))
        except Exception as e:
            print(f"  skip {v['name']}: {e}")
            continue
        rows.append((sim, v))
    rows.sort(key=lambda r: -r[0])
    json.dump([dict(similarity=s, voice_id=v["voice_id"], name=v["name"], use_case=v.get("use_case"),
                    free_users_allowed=v.get("free_users_allowed"), preview=preview_url(v),
                    uses_1y=v.get("usage_character_count_1y")) for s, v in rows],
              open(os.path.join(vdir, "library_ranking.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nclosest first (his own clips score ~0.97 with each other; best free Microsoft voice 0.73):")
    for s, v in rows[:15]:
        print(f"  {s:.3f}  {v['name'][:40]:40s} {v['voice_id']}  {v.get('use_case')}  "
              f"used {v.get('usage_character_count_1y') or 0:,} chars/yr")


main()
