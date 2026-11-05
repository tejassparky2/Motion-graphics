"""Background plates for the mythology videos: SDXL (DreamShaper XL Lightning, "selling images allowed") through the
local ComfyUI API, upscaled with Real-ESRGAN x4plus (BSD-3) and fitted to a vertical 1242x2208 plate (1.15x the
frame, so camera moves never show an edge). Empty stages only: no people and never a deity (the characters are drawn
in code). Owner, 6 Nov 2026: "Download everything is auto approved".

Usage: <ComfyUI venv python> is not needed here; run with the research venv:
  python -I -X utf8 channels/mythology/plates.py kakudmi [name ...] [--seeds 2]
Writes myth_assets/<video>/plates_raw/<name>_s<seed>.png and, for the first seed (or --pick name=seed), the fitted
plate myth_assets/<video>/<name>.png."""
import json, os, subprocess, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE]
from channel import ASSETS_ROOT, ROOT  # noqa: E402

COMFY = os.path.join(ROOT, "tools", "ComfyUI")
COMFY_PY = os.path.join(COMFY, ".venv", "Scripts", "python.exe")
ESRGAN = os.path.join(ROOT, "tools", "realesrgan", "realesrgan-ncnn-vulkan.exe")
URL = "http://127.0.0.1:8188"
CKPT = "DreamShaperXL_Lightning-SFW.safetensors"

STYLE = ("2D animated film background painting, painterly, soft shading, rich warm colours, highly detailed, "
         "vertical composition, empty open space in the lower middle for characters")
NEG = ("people, person, man, woman, child, face, figure, crowd, animal, text, letters, watermark, signature, logo, "
       "frame, border, onion dome, minaret, mosque, pagoda, chinese architecture, japanese, torii, european castle, "
       "gothic, church, modern, car, electric light, photo, photorealistic, 3d render, blurry, lowres, deformed")

PROMPTS = {
    "kakudmi": {
        "palace": "interior of an ancient Indian royal palace throne hall, carved sandstone pillars, scalloped "
                  "arches, hanging brass oil lamps, marigold garlands, red and gold silk drapes, polished stone floor, "
                  "warm golden evening light",
        "clouds": "rising through soft golden clouds into heaven, divine light rays from above, pastel pink and gold "
                  "sky, floating lotus petals, ethereal and serene",
        "brahmaloka": "celestial heavenly court high in the clouds, ornate golden Indian temple pavilion with carved "
                      "pillars and a curved shikhara tower, a vast glowing halo of light behind, pink lotus flowers on "
                      "golden clouds, sacred and serene, soft divine light",
        # the first prompt drew multi-tiered pagoda towers (6 Nov 2026), so heaven is a lotus lake with no buildings
        "brahmaloka2": "heaven high above the clouds, a vast calm lake covered with pink lotus flowers, golden divine "
                       "light rays falling from above, a soft glowing circle of light in the upper middle, distant "
                       "golden clouds, sacred and serene, no buildings, no tower",
        "dwaraka": "ancient Indian city of Dwaraka beside the sea at golden sunset, white and gold Hindu temples with "
                   "tall curved shikhara towers, palaces, a harbour with wooden sailing boats, gentle waves, warm sky",
        "street": "street of an ancient Indian town, small houses with clay tile roofs, market stalls with brass pots "
                  "and baskets, a huge banyan tree, soft morning light, dusty road in the foreground",
    },
}


def post(path, body):
    req = urllib.request.Request(URL + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    return json.loads(urllib.request.urlopen(req, timeout=60).read())


def get(path):
    return urllib.request.urlopen(URL + path, timeout=60).read()


def server():
    try:
        get("/system_stats")
        return None
    except Exception:
        pass
    log = open(os.path.join(ROOT, "myth_out", "comfy_server.log"), "w")
    p = subprocess.Popen([COMFY_PY, "main.py", "--lowvram", "--listen", "127.0.0.1", "--port", "8188",
                          "--disable-auto-launch", "--preview-method", "none"], cwd=COMFY, stdout=log, stderr=log)
    for _ in range(240):
        time.sleep(2)
        try:
            get("/system_stats")
            return p
        except Exception:
            if p.poll() is not None:
                raise RuntimeError("ComfyUI exited; see myth_out/comfy_server.log")
    raise RuntimeError("ComfyUI did not start")


def workflow(prompt, seed, prefix, w=768, h=1344, steps=6):
    return {
        "1": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": CKPT}},
        "2": {"class_type": "CLIPTextEncode", "inputs": {"text": f"{prompt}, {STYLE}", "clip": ["1", 1]}},
        "3": {"class_type": "CLIPTextEncode", "inputs": {"text": NEG, "clip": ["1", 1]}},
        "4": {"class_type": "EmptyLatentImage", "inputs": {"width": w, "height": h, "batch_size": 1}},
        "5": {"class_type": "KSampler", "inputs": {"model": ["1", 0], "positive": ["2", 0], "negative": ["3", 0],
                                                   "latent_image": ["4", 0], "seed": seed, "steps": steps, "cfg": 2.0,
                                                   "sampler_name": "dpmpp_sde", "scheduler": "karras",
                                                   "denoise": 1.0}},
        "6": {"class_type": "VAEDecode", "inputs": {"samples": ["5", 0], "vae": ["1", 2]}},
        "7": {"class_type": "SaveImage", "inputs": {"images": ["6", 0], "filename_prefix": prefix}},
    }


def generate(prompt, seed, out_png):
    pid = post("/prompt", {"prompt": workflow(prompt, seed, "myth")})["prompt_id"]
    for _ in range(900):
        time.sleep(1)
        h = json.loads(get(f"/history/{pid}"))
        if pid in h:
            img = h[pid]["outputs"]["7"]["images"][0]
            data = get(f"/view?filename={img['filename']}&subfolder={img['subfolder']}&type={img['type']}")
            open(out_png, "wb").write(data)
            return
    raise RuntimeError("generation timed out")


def fit(raw_png, out_png, tw=1242, th=2208):
    from PIL import Image
    up = raw_png[:-4] + "_x4.png"
    subprocess.run([ESRGAN, "-i", raw_png, "-o", up, "-n", "realesrgan-x4plus", "-t", "128", "-g",
                    os.environ.get("ESRGAN_GPU", "1")], check=True,
                   capture_output=True)
    im = Image.open(up).convert("RGB")
    k = max(tw / im.width, th / im.height)
    im = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    x, y = (im.width - tw) // 2, (im.height - th) // 2
    im.crop((x, y, x + tw, y + th)).save(out_png)
    os.remove(up)


def main():
    video = sys.argv[1]
    args = [a for a in sys.argv[2:] if not a.startswith("--")]
    seeds = int(sys.argv[sys.argv.index("--seeds") + 1]) if "--seeds" in sys.argv else 2
    picks = dict(a.split("=") for a in args if "=" in a)
    names = [a for a in args if "=" not in a and not a.isdigit()] or list(PROMPTS[video])
    out_dir = os.path.join(ASSETS_ROOT, video)
    raw_dir = os.path.join(out_dir, "plates_raw")
    os.makedirs(raw_dir, exist_ok=True)
    if picks:                                  # only re-fit chosen seeds
        for name, seed in picks.items():
            fit(os.path.join(raw_dir, f"{name}_s{seed}.png"), os.path.join(out_dir, f"{name}.png"))
            print(f"{name}: picked seed {seed}", flush=True)
        return
    proc = server()
    try:
        for name in names:
            for k in range(seeds):
                seed = 1000 + 17 * k
                raw = os.path.join(raw_dir, f"{name}_s{seed}.png")
                if not os.path.exists(raw):
                    t = time.time()
                    generate(PROMPTS[video][name], seed, raw)
                    print(f"{name} seed {seed}: {time.time() - t:.0f} s", flush=True)
            fit(os.path.join(raw_dir, f"{name}_s1000.png"), os.path.join(out_dir, f"{name}.png"))
        json.dump([{"file": f"{n}.png", "title": f"{n} background", "author": "generated locally",
                    "license": "own work", "source": ""} for n in names],
                  open(os.path.join(out_dir, "credits.json"), "w"), indent=1)
    finally:
        if proc:
            proc.terminate()


if __name__ == "__main__":
    main()
