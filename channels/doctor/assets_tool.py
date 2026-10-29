#!/usr/bin/env python3
"""Photo assets for a doctor-channel reel, the way the Hinglish channel makes its Toxoplasma video: free-licence
photos, cut out with rembg (soft shadow added at draw time by poster.photo), or kept whole for framed plates.

  python channels/doctor/assets_tool.py fetch <candidates.jsonl> <work_dir>
      Download every candidate ({"q", "source", "url", "page", "author", "license", ...} per line) and write a
      numbered contact sheet per query (work_dir/sheet_q01.png ...) to pick from.
  python channels/doctor/assets_tool.py cut <work_dir> <candidate id> <video> <key> [--frame] [--crop x0,y0,x1,y1]
      Cut the candidate out with rembg (or keep it whole with --frame) into assets/doctor_photos/<video>/<key>.png
      (.jpg for --frame) and add its credit to that folder's credits.json.

Licences allowed: public domain, CC0, CC BY, Pixabay, Unsplash, Pexels (never BY-SA, NC or ND).
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

from PIL import Image, ImageDraw

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
UA = {"User-Agent": "DocAndTheOrgansAssets/0.1 (https://github.com/tejassparky2/motion-graphics)"}
OK = re.compile(r"^(public domain|pd|cc0|pdm|cc by( \d(\.\d)?)?|pixabay.*|unsplash.*|pexels.*)$", re.I)
SITES = {"pixabay": "Pixabay", "unsplash": "Unsplash", "pexels": "Pexels", "commons": "Wikimedia Commons"}


def fetch(jsonl, work):
    os.makedirs(work, exist_ok=True)
    rows = [json.loads(line) for line in open(jsonl, encoding="utf-8") if line.strip().startswith("{")]
    by_q = {}
    for r in rows:
        if not OK.match(r.get("license", "").strip()):
            print(f"skip (licence {r.get('license')!r}): {r.get('page')}")
            continue
        q = int(r["q"])
        k = len(by_q.setdefault(q, []))
        r["id"] = f"q{q:02d}_{k + 1}"
        r["file"] = os.path.join(work, r["id"] + ".jpg")
        if not os.path.exists(r["file"]):
            if "wikimedia" in r["url"]:
                time.sleep(6)                                     # Wikimedia throttles bursts from shared addresses
            ok = False
            for k in range(6):
                try:
                    req = urllib.request.Request(r["url"], headers=UA)
                    with urllib.request.urlopen(req, timeout=90) as f:
                        data = f.read()
                    open(r["file"], "wb").write(data)
                    Image.open(r["file"]).verify()
                    ok = True
                    break
                except urllib.error.HTTPError as e:
                    if e.code != 429:
                        break
                    time.sleep(min(60, int(e.headers.get("Retry-After") or 10) + 2))
                except Exception:                                 # noqa: BLE001
                    break
            if not ok:
                print(f"download failed {r['id']}", flush=True)
                continue
        by_q[q].append(r)
    json.dump([r for v in by_q.values() for r in v], open(os.path.join(work, "candidates.json"), "w"), indent=1)
    for q, rs in sorted(by_q.items()):
        sheet(rs, os.path.join(work, f"sheet_q{q:02d}.png"))
    print(f"{sum(len(v) for v in by_q.values())} candidates for {len(by_q)} queries in {work}")


def sheet(rows, path, tw=360, th=360):
    if not rows:
        return
    im = Image.new("RGB", (len(rows) * tw, th + 30), (235, 228, 212))
    dr = ImageDraw.Draw(im)
    for i, r in enumerate(rows):
        size = ""
        try:
            t = Image.open(r["file"]).convert("RGB")
            size = f"{t.width}x{t.height}"
            t.thumbnail((tw - 8, th - 8))
            im.paste(t, (i * tw + (tw - t.width) // 2, 4))
        except Exception:                                         # noqa: BLE001
            pass
        dr.text((i * tw + 6, th + 8), f"{r['id']} {r['source']} {size}", fill=(20, 10, 0))
    im.save(path)


def cut(work, cid, video, key, frame=False, crop=None):
    rows = {r["id"]: r for r in json.load(open(os.path.join(work, "candidates.json")))}
    r = rows[cid]
    out_dir = os.path.join(ROOT, "assets", "doctor_photos", video)
    os.makedirs(out_dir, exist_ok=True)
    im = Image.open(r["file"]).convert("RGB")
    if crop:
        im = im.crop(tuple(int(v) for v in crop.split(",")))
    im.thumbnail((1800, 1800), Image.LANCZOS)
    if frame:
        name = f"{key}.jpg"
        im.save(os.path.join(out_dir, name), quality=90, optimize=True)
    else:
        from rembg import new_session, remove
        cutout = remove(im, session=new_session("isnet-general-use"), post_process_mask=True)
        a = cutout.getchannel("A").point(lambda v: 0 if v < 12 else v)    # drop faint haze left round the subject
        cutout.putalpha(a)
        box = a.getbbox()
        cutout = cutout.crop((max(0, box[0] - 8), max(0, box[1] - 8), min(cutout.width, box[2] + 8),
                              min(cutout.height, box[3] + 8)))
        name = f"{key}.png"
        cutout.save(os.path.join(out_dir, name), optimize=True)
    cpath = os.path.join(out_dir, "credits.json")
    credits = json.load(open(cpath)) if os.path.exists(cpath) else []
    credits = [c for c in credits if c["file"] != name]
    credits.append(dict(file=name, author=r.get("author", ""), license=r.get("license", ""), page=r.get("page", ""),
                        title=r.get("note", "") or r.get("title", ""), site=SITES.get(r["source"], r["source"])))
    json.dump(credits, open(cpath, "w"), indent=1, ensure_ascii=False)
    print(f"wrote {os.path.join(out_dir, name)}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "fetch":
        fetch(a[1], a[2])
    elif a[0] == "cut":
        crop = a[a.index("--crop") + 1] if "--crop" in a else None
        cut(a[1], a[2], a[3], a[4], frame="--frame" in a, crop=crop)
