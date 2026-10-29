"""Search free-licence image (and video) libraries at once, download candidates, and build a numbered contact sheet.

Sources, each used only under a licence that allows use in monetized videos:
- Wikimedia Commons (no key): Public domain / CC0 / CC BY only (no BY-SA, NC, ND)
- NASA Image Library (no key): NASA media is generally public domain
- Smithsonian Open Access (api.data.gov DEMO_KEY, or SI_API_KEY): CC0 items only
- Openverse (no key, slow): CC0 / PDM / CC BY only
- Pexels (PEXELS_API_KEY), Pixabay (PIXABAY_API_KEY), Unsplash (UNSPLASH_ACCESS_KEY): their own free licences
Keys come from the environment or the git-ignored <shorts research>/.env (never printed).

Usage:
  python -I -X utf8 channels/hinglish/stock_search.py <out_dir> "query one" ["query two" ...] [--n 8] [--video]
Writes <out_dir>/<query>/<n>_<source>.jpg, candidates.json (licence, author, page) and sheet.png.
"""
import concurrent.futures as cf
import json, os, re, sys, urllib.error, urllib.parse, urllib.request
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _key(name):
    """A secret from the environment only (never printed)."""
    return os.environ.get(name)

UA = {"User-Agent": "DocAndTheOrgansAssets/0.1 (https://github.com/tejassparky2/motion-graphics; tejas@everything3dindia.com)"}
OK_COMMONS = re.compile(r"^(public domain|pd\b|cc0|cc by( \d(\.\d)?)?$)", re.I)


def get_json(url, headers=None, timeout=40, tries=8):
    """GET JSON; waits and retries when the server says "too many requests" (Wikimedia rate-limits shared cloud
    addresses) or is briefly unavailable."""
    import time
    for k in range(tries):
        req = urllib.request.Request(url, headers={**UA, **(headers or {})})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code not in (429, 502, 503, 504) or k == tries - 1:
                raise
            time.sleep(min(120, int(e.headers.get("Retry-After") or 30) + 5))
        except (urllib.error.URLError, TimeoutError):
            if k == tries - 1:
                raise
            time.sleep(20)


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def commons(q, n):
    p = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6, "gsrsearch": f"{q} filetype:bitmap",
         "gsrlimit": n * 4, "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1920}
    d = get_json("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p))
    out = []
    for pg in sorted((d.get("query") or {}).get("pages", {}).values(), key=lambda x: x.get("index", 0)):
        ii = (pg.get("imageinfo") or [{}])[0]
        md = ii.get("extmetadata", {})
        lic = strip_html(md.get("LicenseShortName", {}).get("value", ""))
        author = strip_html(md.get("Artist", {}).get("value", ""))
        if not OK_COMMONS.match(lic) or not author or min(ii.get("width", 0), ii.get("height", 0)) < 700:
            continue
        out.append(dict(source="commons", url=ii.get("thumburl") or ii.get("url"), page=ii.get("descriptionurl"),
                        title=pg["title"], author=author, license=lic,
                        license_url=md.get("LicenseUrl", {}).get("value", "")))
        if len(out) >= n:
            break
    return out


def nasa(q, n):
    d = get_json("https://images-api.nasa.gov/search?" + urllib.parse.urlencode({"q": q, "media_type": "image"}))
    out = []
    for it in d.get("collection", {}).get("items", [])[:n]:
        meta = it["data"][0]
        href = next((l["href"] for l in it.get("links", []) if l.get("rel") == "preview"), None)
        if href:
            out.append(dict(source="nasa", url=href.replace("~thumb", "~medium"), page=f"https://images.nasa.gov/details/{meta['nasa_id']}",
                            title=meta.get("title", ""), author=meta.get("center", "NASA"), license="NASA (public domain)",
                            license_url="https://www.nasa.gov/nasa-brand-center/images-and-media/"))
    return out


def smithsonian(q, n):
    k = _key("SI_API_KEY") or "DEMO_KEY"
    d = get_json("https://api.si.edu/openaccess/api/v1.0/search?" + urllib.parse.urlencode(
        {"q": f"{q} AND online_media_type:Images", "rows": n * 3, "api_key": k}))
    out = []
    for r in d.get("response", {}).get("rows", []):
        media = (((r.get("content") or {}).get("descriptiveNonRepeating") or {}).get("online_media") or {}).get("media", [])
        for m in media:
            if (m.get("usage") or {}).get("access") == "CC0" and m.get("content"):
                out.append(dict(source="smithsonian", url=m["content"], page=(r.get("content") or {}).get(
                    "descriptiveNonRepeating", {}).get("record_link", ""), title=r.get("title", ""), author="Smithsonian",
                                license="CC0", license_url="https://creativecommons.org/publicdomain/zero/1.0/"))
                break
        if len(out) >= n:
            break
    return out


def openverse(q, n):
    d = get_json("https://api.openverse.org/v1/images/?" + urllib.parse.urlencode(
        {"q": q, "license": "cc0,pdm,by", "page_size": n}), timeout=90)
    return [dict(source="openverse:" + r.get("source", ""), url=r["url"], page=r.get("foreign_landing_url"), title=r.get("title", ""),
                 author=r.get("creator") or "", license=f"{r.get('license', '').upper()} {r.get('license_version') or ''}".strip(),
                 license_url=r.get("license_url", "")) for r in d.get("results", [])]


def pexels(q, n, video=False):
    k = _key("PEXELS_API_KEY")
    if not k:
        return []
    if video:
        d = get_json("https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": q, "per_page": n, "orientation": "portrait"}),
                     {"Authorization": k})
        out = []
        for v in d.get("videos", []):
            f = max((f for f in v["video_files"] if f.get("width")), key=lambda f: f["width"] * f["height"])
            out.append(dict(source="pexels-video", url=f["link"], thumb=v.get("image"), page=v["url"], title=q,
                            author=v["user"]["name"], license="Pexels License", license_url="https://www.pexels.com/license/"))
        return out
    d = get_json("https://api.pexels.com/v1/search?" + urllib.parse.urlencode({"query": q, "per_page": n}), {"Authorization": k})
    return [dict(source="pexels", url=p["src"]["large2x"], page=p["url"], title=p.get("alt") or q, author=p["photographer"],
                 license="Pexels License", license_url="https://www.pexels.com/license/") for p in d.get("photos", [])]


def pixabay(q, n, video=False):
    k = _key("PIXABAY_API_KEY")
    if not k:
        return []
    if video:
        d = get_json("https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": k, "q": q, "per_page": max(3, n)}))
        return [dict(source="pixabay-video", url=h["videos"]["large"]["url"] or h["videos"]["medium"]["url"],
                     thumb=h["videos"]["medium"].get("thumbnail"), page=h["pageURL"], title=h.get("tags", q), author=h["user"],
                     license="Pixabay Content License", license_url="https://pixabay.com/service/license-summary/") for h in d.get("hits", [])]
    d = get_json("https://pixabay.com/api/?" + urllib.parse.urlencode({"key": k, "q": q, "per_page": max(3, n), "safesearch": "true"}))
    return [dict(source="pixabay", url=h["largeImageURL"], page=h["pageURL"], title=h.get("tags", q), author=h["user"],
                 license="Pixabay Content License", license_url="https://pixabay.com/service/license-summary/") for h in d.get("hits", [])]


def unsplash(q, n):
    k = _key("UNSPLASH_ACCESS_KEY")
    if not k:
        return []
    d = get_json("https://api.unsplash.com/search/photos?" + urllib.parse.urlencode({"query": q, "per_page": n, "client_id": k}))
    return [dict(source="unsplash", url=r["urls"]["regular"], page=r["links"]["html"], download_ping=r["links"]["download_location"],
                 title=r.get("alt_description") or q, author=r["user"]["name"], license="Unsplash License",
                 license_url="https://unsplash.com/license") for r in d.get("results", [])]


IMAGE_SOURCES = [commons, nasa, smithsonian, pexels, pixabay, unsplash, openverse]
if os.environ.get("STOCK_SOURCES"):      # e.g. STOCK_SOURCES=commons,nasa when Openverse is timing out
    IMAGE_SOURCES = [s for s in IMAGE_SOURCES if s.__name__ in os.environ["STOCK_SOURCES"].split(",")]
VIDEO_SOURCES = [lambda q, n: pexels(q, n, True), lambda q, n: pixabay(q, n, True)]


def fetch(url, path, tries=6):
    """Download a file, waiting and retrying when the server says "too many requests"."""
    import time
    for k in range(tries):
        req = urllib.request.Request(url, headers=UA)
        try:
            with urllib.request.urlopen(req, timeout=90) as r:
                data = r.read()
            break
        except urllib.error.HTTPError as e:
            if e.code not in (429, 502, 503, 504) or k == tries - 1:
                raise
            time.sleep(min(60, int(e.headers.get("Retry-After") or 10) + 2))
    with open(path, "wb") as f:
        f.write(data)


def search(q, out_dir, n=6, video=False):
    d = os.path.join(out_dir, re.sub(r"[^\w-]+", "_", q.lower()).strip("_"))
    os.makedirs(d, exist_ok=True)
    found, errors = [], []
    with cf.ThreadPoolExecutor(8) as ex:
        futs = {ex.submit(s, q, n): getattr(s, "__name__", "video") for s in (VIDEO_SOURCES if video else IMAGE_SOURCES)}
        for f in cf.as_completed(futs):
            try:
                found += f.result()
            except Exception as e:
                errors.append(f"{futs[f]}: {type(e).__name__}")
    rows = []
    for i, c in enumerate(found, 1):
        ext = ".mp4" if c["source"].endswith("video") else ".jpg"
        c["file"] = os.path.join(d, f"{i:02d}_{c['source'].split(':')[0]}{ext}")
        try:
            if not os.path.exists(c["file"]):
                fetch(c["url"], c["file"])
            if c.get("download_ping"):                         # Unsplash API guideline: register the download
                try:
                    get_json(c["download_ping"] + ("&" if "?" in c["download_ping"] else "?") + "client_id=" + _key("UNSPLASH_ACCESS_KEY"))
                except Exception:
                    pass
            if ext == ".mp4" and c.get("thumb"):
                c["thumb_file"] = c["file"][:-4] + "_thumb.jpg"
                fetch(c["thumb"], c["thumb_file"])
            rows.append(c)
        except Exception as e:
            errors.append(f"download {c['source']}: {type(e).__name__}")
    json.dump(rows, open(os.path.join(d, "candidates.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sheet(rows, os.path.join(d, "sheet.png"))
    by = {}
    for r in rows:
        by[r["source"].split(":")[0]] = by.get(r["source"].split(":")[0], 0) + 1
    print(f"{q!r}: {len(rows)} candidates {by}" + (f"  (skipped: {', '.join(errors)})" if errors else ""), flush=True)
    return rows


def sheet(rows, path, cols=5, tw=300, th=300):
    if not rows:
        return
    lines = (len(rows) + cols - 1) // cols
    im = Image.new("RGB", (cols * tw, lines * (th + 34)), (235, 228, 212))
    dr = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        font = ImageFont.load_default()
    for i, r in enumerate(rows):
        try:
            t = Image.open(r.get("thumb_file") or r["file"]).convert("RGB")
            t.thumbnail((tw - 8, th - 8))
            x, y = (i % cols) * tw, (i // cols) * (th + 34)
            im.paste(t, (x + (tw - t.width) // 2, y + 4))
            dr.text((x + 6, y + th + 4), f"{i + 1}. {r['source'].split(':')[0]} · {r['license'][:18]}", fill=(30, 20, 10), font=font)
        except Exception:
            continue
    im.save(path)


if __name__ == "__main__":
    args = sys.argv[1:]
    n = int(args[args.index("--n") + 1]) if "--n" in args else 6
    video = "--video" in args
    qs = [a for i, a in enumerate(args[1:], 1) if not a.startswith("--") and (i < 2 or args[i - 1] != "--n")]
    for q in qs:
        search(q, args[0], n, video)
