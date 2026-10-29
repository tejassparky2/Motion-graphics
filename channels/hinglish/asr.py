"""Whisper for the channel's clarity checks (retakes, liveliness retakes, render --check, pace measuring).

On the GPU when CUDA works, else on the CPU (owner, 29 Oct 2026: "If gpu is fast why won't you do all there").
The NVIDIA cuBLAS/cuDNN pip wheels (nvidia-cublas-cu12, nvidia-cudnn-cu12) put their DLLs in site-packages/nvidia/*/bin,
which Windows doesn't search on its own, so those folders are registered first.
"""
import glob
import os
import site
import sys

import numpy as np


def _add_cuda_dlls():
    if os.name != "nt":
        return
    for sp in site.getsitepackages():
        for d in glob.glob(os.path.join(sp, "nvidia", "*", "bin")):
            os.add_dll_directory(d)
            os.environ["PATH"] = d + os.pathsep + os.environ.get("PATH", "")


def whisper(size="medium"):
    from faster_whisper import WhisperModel
    _add_cuda_dlls()
    try:
        import ctranslate2
        if ctranslate2.get_cuda_device_count():
            model = WhisperModel(size, device="cuda", compute_type="int8_float16")
            list(model.transcribe(np.zeros(16000, np.float32), language="hi")[0])   # make sure the CUDA libs load
            print(f"whisper {size}: GPU", file=sys.stderr)
            return model
    except Exception as e:                                       # missing DLLs, out of GPU memory...
        print(f"whisper {size}: GPU unavailable ({type(e).__name__}: {e}), using CPU", file=sys.stderr)
    return WhisperModel(size, device="cpu", compute_type="int8")
