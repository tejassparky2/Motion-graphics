"""Rank the described Kannada voices from kn_voice_design.py (or IndicF5 samples made from them).

Two passes, because the tools live in different environments; both add to <dir>/scores.json:
  <shorts research>/tools/.venv-f5/Scripts/python -I -X utf8 channels/mythology/kn_voice_design_score.py <dir> asr
      Whisper large-v3-turbo letter errors against the text (clarity), length, pitch, leading/trailing silence
  <shorts research>/.venv-research/Scripts/python -I -X utf8 channels/mythology/kn_voice_design_score.py <dir> sim
      Resemblyzer similarity to the Hindi narrator Aman (how close it sounds to the Hindi channel), then the table
Set CUDA_VISIBLE_DEVICES=-1 for the asr pass when another job holds the GPU."""
import glob, json, os, sys

import numpy as np
import soundfile as sf

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))           # <shorts research>
AMAN = os.path.join(ROOT, "mayank", "voice", "f5_refs", "named_aman_s3_ref.wav")
REF_TEXT = ("ಯೋಚಿಸಿ, ಸಾವಿರಾರು ವರ್ಷಗಳಿಂದ ಜನ ಹೇಳುತ್ತಾ ಬಂದಿರುವ ಒಂದು ಕಥೆ. "
            "ಆದರೆ ಅದರ ಒಂದು ಭಾಗ, ಹೆಚ್ಚಿನವರಿಗೆ ಗೊತ್ತೇ ಇಲ್ಲ.")


def kn(s):
    return [c for c in s if "ಀ" <= c <= "೿"]


def cer(ref, hyp):
    d = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        prev, d[0] = d[0], i
        for j, h in enumerate(hyp, 1):
            prev, d[j] = d[j], min(d[j] + 1, d[j - 1] + 1, prev + (r != h))
    return d[-1] / max(1, len(ref))


def mono(path, sr_out=None):
    a, sr = sf.read(path, dtype="float32")
    if a.ndim > 1:
        a = a.mean(1)
    if sr_out and sr != sr_out:
        import librosa
        a, sr = librosa.resample(a, orig_sr=sr, target_sr=sr_out), sr_out
    return a, sr


def asr_pass(d, scores):
    import librosa
    import torch
    from transformers import pipeline
    asr = pipeline("automatic-speech-recognition", model="openai/whisper-large-v3-turbo",
                   device="cuda" if torch.cuda.is_available() else "cpu",
                   torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32)
    texts = {}
    if os.path.exists(os.path.join(d, "texts.json")):                     # samples: their own text per clip
        texts = json.load(open(os.path.join(d, "texts.json"), encoding="utf-8"))
    for p in sorted(glob.glob(os.path.join(d, "*.wav"))):
        k = os.path.basename(p)[:-4]
        a, sr = mono(p)
        x = librosa.resample(a, orig_sr=sr, target_sr=16000) if sr != 16000 else a
        heard = asr({"raw": x, "sampling_rate": 16000},
                    generate_kwargs={"language": "kannada", "task": "transcribe"})["text"].strip()
        env = librosa.feature.rms(y=a, frame_length=2048, hop_length=512)[0]
        loud = np.where(env > env.max() * 0.05)[0]
        lead, trail = loud[0] * 512 / sr, (len(env) - loud[-1]) * 512 / sr
        f0, _, _ = librosa.pyin(a, fmin=60, fmax=400, sr=sr, frame_length=2048)
        f0 = f0[~np.isnan(f0)]
        scores.setdefault(k, {}).update(
            cer=round(cer(kn(texts.get(k, REF_TEXT)), kn(heard)), 3), heard=heard, seconds=round(len(a) / sr, 2),
            lead=round(lead, 2), trail=round(trail, 2),
            pitch=round(float(np.median(f0)), 0) if len(f0) else 0,
            pitch_range=round(float(np.percentile(f0, 90) - np.percentile(f0, 10)), 0) if len(f0) else 0)
        print(f"{k:24s} CER {scores[k]['cer']:4.0%}  {scores[k]['seconds']:4.1f}s  pitch {scores[k]['pitch']:.0f}  "
              f"{heard}", flush=True)


def sim_pass(d, scores):
    from resemblyzer import VoiceEncoder, preprocess_wav
    enc = VoiceEncoder(verbose=False)
    aman = enc.embed_utterance(preprocess_wav(AMAN))
    for p in sorted(glob.glob(os.path.join(d, "*.wav"))):
        k = os.path.basename(p)[:-4]
        scores.setdefault(k, {})["like_aman"] = round(float(np.dot(aman, enc.embed_utterance(preprocess_wav(p)))), 3)
    rows = sorted(scores.items(), key=lambda kv: (kv[1].get("cer", 1), -kv[1].get("like_aman", 0)))
    print(f"{'voice':24s} {'errors':>6s} {'like Aman':>9s} {'secs':>5s} {'pitch':>5s} {'range':>5s}")
    for k, s in rows:
        print(f"{k:24s} {s.get('cer', 1):6.0%} {s.get('like_aman', 0):9.2f} {s.get('seconds', 0):5.1f} "
              f"{s.get('pitch', 0):5.0f} {s.get('pitch_range', 0):5.0f}")


def main():
    d, mode = sys.argv[1], sys.argv[2]
    path = os.path.join(d, "scores.json")
    scores = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    (asr_pass if mode == "asr" else sim_pass)(d, scores)
    json.dump(scores, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
