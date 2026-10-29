#!/usr/bin/env python3
"""Wikimedia Commons photo search that works from the cloud server: the search goes through api.wikimedia.org (not
rate-limited here, unlike commons.wikimedia.org/w/api.php), the licences of all hits are then looked up in batches of
50 titles per call to the Commons API, and only public domain / CC0 / CC BY files are kept and downloaded from
upload.wikimedia.org. Writes a JSON-lines file that assets_tool.py fetch reads.

  python channels/doctor/commons_search.py <out.jsonl> "query 1" "query 2" ... [--n 8]
Each query is numbered in order (q = 1, 2, ...), like the shot list it serves.
"""
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = {"User-Agent": "DocAndTheOrgansAssets/0.1 (https://github.com/tejassparky2/motion-graphics; tejas@everything3dindia.com)"}
OK = re.compile(r"^(public domain|pd\b|cc0|cc by( \d(\.\d)?)?$)", re.I)


def get(url, tries=10):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code not in (429, 502, 503, 504) or k == tries - 1:
                raise
            wait = min(90, int(e.headers.get("Retry-After") or 10) + 3)
            print(f"  {e.code} from {url.split('/')[2]}, waiting {wait} s", file=sys.stderr, flush=True)
            time.sleep(wait)


def strip(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def search(q, n):
    d = get("https://api.wikimedia.org/core/v1/commons/search/page?" + urllib.parse.urlencode({"q": f"{q} filetype:bitmap", "limit": n * 5}))
    return [p["key"] for p in d.get("pages", []) if p["key"].lower().startswith("file:")]


def licences(titles):
    out = {}
    for i in range(0, len(titles), 50):
        chunk = titles[i:i + 50]
        d = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(
            {"action": "query", "format": "json", "titles": "|".join(t.replace("_", " ") for t in chunk),
             "prop": "imageinfo", "iiprop": "url|extmetadata|size", "iiurlwidth": 1800}))
        for pg in (d.get("query") or {}).get("pages", {}).values():
            ii = (pg.get("imageinfo") or [{}])[0]
            md = ii.get("extmetadata", {})
            out[pg["title"].replace(" ", "_")] = dict(
                url=ii.get("thumburl") or ii.get("url"), page=ii.get("descriptionurl"), w=ii.get("width", 0),
                h=ii.get("height", 0), license=strip(md.get("LicenseShortName", {}).get("value", "")),
                author=strip(md.get("Artist", {}).get("value", ""))[:120], title=pg["title"])
        print(f"  licences {min(i + 50, len(titles))}/{len(titles)}", file=sys.stderr, flush=True)
        time.sleep(2)
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    n = int(a[a.index("--n") + 1]) if "--n" in a else 8
    qs = [x for i, x in enumerate(a[1:], 1) if not x.startswith("--") and a[i - 1] != "--n"]
    hits = []
    for qi, q in enumerate(qs, 1):
        try:
            hits += [(qi, t) for t in search(q, n)]
        except Exception as e:                                    # noqa: BLE001
            print(f"q{qi} {q!r}: search failed ({type(e).__name__})", flush=True)
        time.sleep(0.5)
    print(f"{len(hits)} hits; looking up licences", file=sys.stderr, flush=True)
    info = licences(list(dict.fromkeys(t for _, t in hits)))
    kept = {}
    with open(a[0], "w", encoding="utf-8") as f:
        for qi, t in hits:
            m = info.get(t)
            if not m or not m["url"] or not OK.match(m["license"]) or not m["author"] or min(m["w"], m["h"]) < 600:
                continue
            if kept.get(qi, 0) >= n:
                continue
            kept[qi] = kept.get(qi, 0) + 1
            f.write(json.dumps(dict(q=qi, source="commons", url=m["url"], page=m["page"], author=m["author"],
                                    license=m["license"], w=m["w"], h=m["h"], note=m["title"]), ensure_ascii=False) + "\n")
    for qi, q in enumerate(qs, 1):
        print(f"q{qi} {q!r}: {kept.get(qi, 0)} usable", flush=True)
