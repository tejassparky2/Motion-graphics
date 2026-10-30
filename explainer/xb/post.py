"""Finish frames: zoom transition between shots, burned-in captions.

python3 explainer/xb/post.py FRAMES CAPTIONS OUT --post scene_post.json --zoom START END
"""
import argparse
import json
import os

from PIL import Image, ImageEnhance

FPS = 24


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('frames')
    ap.add_argument('captions')
    ap.add_argument('out')
    ap.add_argument('--post', required=True)
    ap.add_argument('--zoom', nargs=2, type=float, help='seconds: punch-in into the knuckle before the cut')
    ap.add_argument('--flash', type=float, nargs='*', default=[], help='seconds of 2-frame white flashes')
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)
    meta = json.load(open(args.post))
    cx, cy = meta['zoom_center']
    names = sorted(f for f in os.listdir(args.frames) if f.startswith('f_') and f.endswith('.png'))
    for name in names:
        fi = int(name[2:6])
        t = (fi - 1) / FPS
        im = Image.open(os.path.join(args.frames, name)).convert('RGBA')
        W, H = im.size
        if args.zoom and args.zoom[0] <= t < args.zoom[1]:
            u = (t - args.zoom[0]) / (args.zoom[1] - args.zoom[0])
            z = 1.0 + 5.0 * u ** 2.2                    # accelerating punch-in
            w, h = W / z, H / z
            x0 = min(max(cx * W - w / 2, 0), W - w)
            y0 = min(max(cy * H - h / 2, 0), H - h)
            im = im.crop((int(x0), int(y0), int(x0 + w), int(y0 + h))).resize((W, H), Image.BICUBIC)
            im = ImageEnhance.Brightness(im).enhance(1.0 + 0.8 * u ** 3)
        for fl in args.flash:
            k = round((t - fl) * FPS)
            if 0 <= k < 3:
                im = ImageEnhance.Brightness(im).enhance((1.9, 1.4, 1.1)[k])
        cap = os.path.join(args.captions, f'c_{fi:04d}.png')
        if os.path.exists(cap):
            im.alpha_composite(Image.open(cap))
        im.convert('RGB').save(os.path.join(args.out, name))
    print('post:', len(names), 'frames')


if __name__ == '__main__':
    main()
