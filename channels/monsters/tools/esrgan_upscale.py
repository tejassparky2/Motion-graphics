"""Q4 upscale test (channels/monsters/DIORAMA_EP01_V3.md): Real-ESRGAN "realesr-animevideov3" (BSD-3, xinntao/Real-ESRGAN;
weights realesr-animevideov3.pth from the project's v0.2.5.0 release) against plain lanczos, 720x1280 -> 1080x1920.

The network is Real-ESRGAN's SRVGGNetCompact (archs/srvgg_arch.py), re-typed here so only torch is needed (the
realesrgan/basicsr packages break on current torchvision). It upscales 4x; the result is then resized down to the
target with lanczos, which is what Real-ESRGAN's own `--outscale 1.5` does.

    python channels/monsters/tools/esrgan_upscale.py WEIGHTS.pth IN.png OUT_DIR [--tile 0] [--threads 4]
        -> OUT_DIR/<name>_esrgan.png, OUT_DIR/<name>_lanczos.png, and the seconds per frame on stdout
"""
import argparse
import os
import time

import numpy as np
import torch
from PIL import Image
from torch import nn
from torch.nn import functional as F


class SRVGGNetCompact(nn.Module):
    """Real-ESRGAN's compact VGG-style network: conv + PReLU x (num_conv + 1), a conv to 3*s*s channels, a pixel
    shuffle, plus the nearest-upsampled input (it learns the residual)."""

    def __init__(self, num_in_ch=3, num_out_ch=3, num_feat=64, num_conv=16, upscale=4):
        super().__init__()
        self.upscale = upscale
        self.body = nn.ModuleList([nn.Conv2d(num_in_ch, num_feat, 3, 1, 1), nn.PReLU(num_parameters=num_feat)])
        for _ in range(num_conv):
            self.body.append(nn.Conv2d(num_feat, num_feat, 3, 1, 1))
            self.body.append(nn.PReLU(num_parameters=num_feat))
        self.body.append(nn.Conv2d(num_feat, num_out_ch * upscale * upscale, 3, 1, 1))
        self.upsampler = nn.PixelShuffle(upscale)

    def forward(self, x):
        out = x
        for layer in self.body:
            out = layer(out)
        out = self.upsampler(out)
        return out + F.interpolate(x, scale_factor=self.upscale, mode="nearest")


def load(weights):
    net = SRVGGNetCompact()
    sd = torch.load(weights, map_location="cpu", weights_only=True)
    net.load_state_dict(sd.get("params", sd), strict=True)
    return net.eval()


@torch.inference_mode()
def upscale(net, im, size, tile=0, pad=10):
    """im (PIL RGB) -> PIL RGB at `size`: the network's 4x, then lanczos down to `size`. With tile > 0 the frame is
    run in tiles (with `pad` px of overlap) to bound memory."""
    x = torch.from_numpy(np.asarray(im, dtype=np.float32) / 255.0).permute(2, 0, 1)[None]
    if not tile:
        y = net(x)
    else:
        _, _, h, w = x.shape
        y = torch.zeros(1, 3, h * 4, w * 4)
        for t in range(0, h, tile):
            for l in range(0, w, tile):
                t0, l0 = max(t - pad, 0), max(l - pad, 0)
                t1, l1 = min(t + tile + pad, h), min(l + tile + pad, w)
                o = net(x[:, :, t0:t1, l0:l1])
                bt, bl = (t - t0) * 4, (l - l0) * 4
                th, tw = min(tile, h - t) * 4, min(tile, w - l) * 4
                y[:, :, t * 4:t * 4 + th, l * 4:l * 4 + tw] = o[:, :, bt:bt + th, bl:bl + tw]
    a = (y[0].clamp(0, 1).permute(1, 2, 0).numpy() * 255.0).round().astype(np.uint8)
    return Image.fromarray(a).resize(size, Image.LANCZOS)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("weights")
    ap.add_argument("src", nargs="+")
    ap.add_argument("--out", required=True)
    ap.add_argument("--size", default="1080x1920")
    ap.add_argument("--tile", type=int, default=0)
    ap.add_argument("--threads", type=int, default=4)
    a = ap.parse_args()
    torch.set_num_threads(a.threads)
    size = tuple(int(v) for v in a.size.split("x"))
    os.makedirs(a.out, exist_ok=True)
    net = load(a.weights)
    for src in a.src:
        name = os.path.splitext(os.path.basename(src))[0]
        im = Image.open(src).convert("RGB")
        t = time.time()
        up = upscale(net, im, size, a.tile)
        dt = time.time() - t
        up.save(os.path.join(a.out, f"{name}_esrgan.png"))
        im.resize(size, Image.LANCZOS).save(os.path.join(a.out, f"{name}_lanczos.png"))
        print(f"{name}: {dt:.2f} s/frame", flush=True)


if __name__ == "__main__":
    main()
