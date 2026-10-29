#!/usr/bin/env python3
"""Keyless CC0 photo search in museum collections, for cut-outs (objects shot on plain backgrounds):
The Metropolitan Museum of Art (Open Access, public-domain objects only) and Smithsonian Open Access (CC0 media only,
api.data.gov DEMO_KEY or SI_API_KEY). Writes JSON lines that assets_tool.py fetch reads.

  python channels/doctor/museum_search.py <out.jsonl> "q=1:lay figure" "q=2:microscope" ... [--n 8]
A query can be "N:words" to number it like the shot list; otherwise queries are numbered in order.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

UA = {"User-Agent": "DocAndTheOrgansAssets/0.1 (https://github.com/tejassparky2/motion-graphics)"}


def get(url, tries=4):
    for k in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code not in (429, 502, 503, 504) or k == tries - 1:
                raise
            time.sleep(10 + 10 * k)


def met(q, n):
    ids = (get("https://collectionapi.metmuseum.org/public/collection/v1.1/search?" +
               urllib.parse.urlencode({"q": q, "hasImages": "true"})) or {}).get("objectIDs") or []
    out = []
    words = [w for w in q.lower().split() if len(w) > 2]
    for oid in ids[:60]:
        try:
            o = get(f"https://collectionapi.metmuseum.org/public/collection/v1/objects/{oid}")
        except Exception:                                         # noqa: BLE001
            continue
        title = f"{o.get('title', '')} ({o.get('objectName', '')})"
        if not o.get("isPublicDomain") or not o.get("primaryImage"):
            continue
        if words and not any(w in title.lower() for w in words):   # the search also matches descriptions
            continue
        out.append(dict(source="met", url=o["primaryImage"], page=o.get("objectURL", ""),
                        author="The Metropolitan Museum of Art", license="CC0", note=title[:100]))
        if len(out) >= n:
            break
    return out


def smithsonian(q, n):
    key = os.environ.get("SI_API_KEY") or "DEMO_KEY"
    d = get("https://api.si.edu/openaccess/api/v1.0/search?" + urllib.parse.urlencode(
        {"q": f"{q} AND online_media_type:Images", "rows": 40, "api_key": key}))
    out = []
    for r in (d.get("response") or {}).get("rows", []):
        c = r.get("content") or {}
        media = ((c.get("descriptiveNonRepeating") or {}).get("online_media") or {}).get("media", [])
        for m in media:
            if (m.get("usage") or {}).get("access") == "CC0" and m.get("content"):
                out.append(dict(source="smithsonian", url=m["content"], author="Smithsonian Institution",
                                page=(c.get("descriptiveNonRepeating") or {}).get("record_link", ""),
                                license="CC0", note=(r.get("title") or "")[:100]))
                break
        if len(out) >= n:
            break
    return out


if __name__ == "__main__":
    a = sys.argv[1:]
    n = int(a[a.index("--n") + 1]) if "--n" in a else 8
    qs = [x for i, x in enumerate(a[1:], 1) if not x.startswith("--") and a[i - 1] != "--n"]
    with open(a[0], "a", encoding="utf-8") as f:
        for i, q in enumerate(qs, 1):
            num, _, words = q.partition(":") if ":" in q and q.split(":")[0].isdigit() else (str(i), "", q)
            for fn in (met, smithsonian):
                try:
                    rows = fn(words, n)
                except Exception as e:                            # noqa: BLE001
                    print(f"q{num} {words!r} {fn.__name__}: failed ({type(e).__name__})", flush=True)
                    continue
                for r in rows:
                    f.write(json.dumps(dict(q=int(num), **r), ensure_ascii=False) + "\n")
                print(f"q{num} {words!r} {fn.__name__}: {len(rows)}", flush=True)
