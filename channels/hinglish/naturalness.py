"""Predicted naturalness (MOS, 1-5) of speech files with UTMOS22 "strong" (SpeechMOS, MIT), a learned predictor of
how natural listeners rate synthetic speech. Used to rank voice candidates alongside clarity, not instead of ears.
Usage: python -I -X utf8 channels/hinglish/naturalness.py file1 [file2 ...]"""
import sys
import librosa, torch

_model = None


def mos(path):
    global _model
    if _model is None:
        _model = torch.hub.load("tarepan/SpeechMOS:v1.2.0", "utmos22_strong", trust_repo=True)
    y, _ = librosa.load(path, sr=16000)
    with torch.no_grad():
        return float(_model(torch.tensor(y).unsqueeze(0), 16000).item())


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(f"{mos(p):.2f}  {p}")
