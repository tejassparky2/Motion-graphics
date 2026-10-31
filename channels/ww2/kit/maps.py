"""WW2 channel kit, maps: Natural Earth countries and 1938-1945 historical regions, three projections, and a Map you
draw every frame with a camera: side fills that flood from a point, coastlines and borders, coast ripples on the sea,
pulsing city dots, Kalam labels, growing attack arrows, moving front lines and the dashed "secret line".
Style rules: channels/ww2/STYLE.md ("Maps").

    from channels.ww2.kit.maps import Map
    m = Map("europe")                                   # or "pacific", "world"
    m.side("poland_w", 4.4, "germany", origin=(16.5, 52.3), dur=1.2)    # floods grey from that point
    m.arrow([(14.6, 53.2), (17.5, 52.9), (20.4, 52.3)], "germany", 3.2, 4.6)
    m.camera_key(0, (15, 52), 1.0); m.camera_key(3.5, (19.5, 52), 2.6)
    m.draw(cr, t)                                       # inside the scene's draw(cr, t), after paper(cr)

Data: Natural Earth admin-0 50m and lakes (public domain), downloaded once into build/ww2/ne/; build_data() projects,
cuts the historical regions and caches compact JSON in channels/ww2/data/<view>.json (committed), so a render needs
only json + cairo. The historical borders (Germany 1937 with East Prussia, the Sudetenland, Poland 1939 and its
September split, Bessarabia, Carpatho-Ukraine, Finnish Karelia, the 1940 demarcation line in France) are Natural Earth
land cut by hand-traced lon/lat lines: close at this scale, not survey-exact.

    /home/user/.venv-main/bin/python -m channels.ww2.kit.maps build       # (re)build the cached views
"""
import json
import math
import os
import random
import sys

from channels.ww2.kit.core import (H, HAND, ROOT, TITLE, W, back_out, cairo, clamp01, col, ease_in, ease_out, lerp,
                                   paper_surface, seg, smooth, text)

DATA = os.path.join(ROOT, "channels", "ww2", "data")
NE = os.path.join(ROOT, "build", "ww2", "ne")
NE_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/{}.geojson"
R_EARTH = 6371000.0                 # a sphere in the build and at runtime, so lon/lat placed live lines up exactly
Q = 4                               # stored coordinates are map pixels x Q, as ints

# map pixels: at zoom 1 the view's centre sits mid-frame and `width_km` spans the 1920 px width
VIEWS = {
    "europe": dict(proj="laea", lon0=15.0, lat0=52.0, center=(15.0, 52.0), width_km=5200,
                   clip=[(-32, 18, 72, 76)]),
    "pacific": dict(proj="eqearth", lon0=160.0, lat0=0.0, center=(145.0, 15.0), width_km=17000,
                    clip=[(25, -52, 180, 72), (-180, -52, -25, 72)]),
    "world": dict(proj="eqearth", lon0=0.0, lat0=0.0, center=(10.0, 8.0), width_km=38000,
                  clip=[(-179.9, -60, 179.9, 84)]),
}

# ---------------------------------------------------------------- historical lines (lon, lat), hand-traced
G37_EAST = [(13.5, 50.5), (15.0, 50.75), (16.3, 50.2), (16.9, 50.2), (17.6, 49.95), (18.55, 49.9), (18.6, 50.25),
            (18.25, 50.55), (17.85, 50.95), (17.45, 51.35), (16.85, 51.65), (16.3, 51.85), (16.05, 52.3),
            (15.85, 52.65), (16.3, 53.0), (16.85, 53.25), (17.25, 53.6), (17.35, 54.05), (17.55, 54.5),
            (17.75, 54.9), (13.5, 55.2)]                               # Pomerania and Silesia, west of the 1937 line
EAST_PRUSSIA_PL = [(19.2, 54.45), (19.45, 54.0), (19.7, 53.55), (20.4, 53.2), (21.2, 53.15), (21.9, 53.4),
                   (22.5, 53.95), (22.85, 54.4), (22.85, 55.0), (19.2, 55.0)]          # its part in today's Poland
KRESY = [(20.0, 49.3), (22.7, 49.05), (23.7, 48.75), (24.6, 48.0), (25.3, 48.25), (26.0, 48.45), (26.4, 48.55),
         (26.3, 49.3), (26.1, 49.75), (26.9, 50.4), (27.2, 50.9), (27.7, 51.6), (27.3, 52.5), (27.2, 53.1),
         (26.8, 53.5), (27.05, 53.95), (27.6, 54.4), (27.75, 55.0), (27.6, 55.7), (26.4, 55.7), (25.6, 55.25),
         (24.9, 54.95), (24.4, 54.5), (23.45, 54.2), (20.0, 54.2)]   # pre-war eastern Poland (Riga line), Vilnius
SPLIT_1939 = [(23.5, 54.05), (22.6, 53.75), (21.95, 53.3), (21.9, 52.95), (22.05, 52.7), (22.6, 52.45),
              (23.2, 52.25), (23.65, 52.08), (23.6, 51.55), (23.75, 51.1), (24.05, 50.75), (24.2, 50.45),
              (23.4, 50.25), (22.75, 50.05), (22.8, 49.8), (22.4, 49.55), (22.2, 49.5), (22.65, 49.08)]  # Bug-San
BUDJAK = [(28.2, 45.2), (29.8, 45.15), (30.8, 45.9), (30.2, 46.4), (29.0, 46.4), (28.2, 46.0)]
N_BUKOVINA = [(24.6, 47.6), (27.3, 47.7), (27.6, 48.5), (26.5, 48.9), (25.0, 48.6), (24.6, 48.3)]   # minus kresy
CARPATHO = [(22.1, 47.8), (22.1, 49.6), (23.0, 49.5), (24.8, 48.3), (24.6, 47.6)]      # minus kresy and bukovina
FIN_KARELIA = [(27.7, 60.55), (29.95, 60.15), (31.2, 60.6), (32.9, 61.4), (31.6, 62.9), (30.0, 61.9), (27.7, 60.9)]
FIN_PETSAMO = [(28.4, 69.0), (31.8, 69.9), (31.8, 70.3), (28.4, 70.3)]
VICHY = [(-1.25, 42.0), (-1.25, 43.0), (-0.6, 43.6), (-0.25, 44.55), (0.15, 45.65), (0.34, 46.58), (1.0, 47.15),
         (2.07, 47.22), (3.33, 46.57), (4.85, 46.78), (5.5, 47.1), (6.1, 46.45), (10.0, 46.0), (10.0, 41.0)]
MANCHUKUO = [(116.5, 40.5), (121.5, 39.0), (124.3, 39.8), (131.0, 42.5), (135.2, 48.5), (127.5, 53.6), (120.0, 53.3),
             (119.5, 50.0), (116.5, 46.5)]
CHINA_OCC = [(110.5, 41.0), (117.5, 41.0), (122.0, 37.5), (122.3, 31.0), (120.5, 28.0), (117.0, 23.5), (114.5, 22.2),
             (112.5, 21.5), (112.8, 24.5), (113.5, 29.0), (111.5, 31.0), (110.5, 35.0)]     # occupied by 1939-40

# region name -> recipe: ADM0_A3 codes to union, then optional ("&", poly, codes) cuts. Built in that order.
EUROPE = {
    "germany": ["DEU"], "austria": ["AUT"], "slovakia": ["SVK"],
    "g37east": [("&", G37_EAST, ["POL"])],
    "east_prussia": [("kaliningrad",), ("&", EAST_PRUSSIA_PL, ["POL"])],
    "kresy": [("&", KRESY, ["BLR", "UKR", "LTU"])],
    "bessarabia": ["MDA", ("&", BUDJAK, ["UKR"])], "bukovina": [("&", N_BUKOVINA, ["UKR"])],
    "carpatho": [("&", CARPATHO, ["UKR"])],
    "fin_karelia": [("&", FIN_KARELIA, ["RUS"])], "fin_petsamo": [("&", FIN_PETSAMO, ["RUS"])],
    "lithuania": ["LTU"], "latvia": ["LVA"], "estonia": ["EST"], "finland": ["FIN"], "romania": ["ROU"],
    "hungary": ["HUN"], "bulgaria": ["BGR"], "albania": ["ALB"], "greece": ["GRC"], "turkey": ["TUR"],
    "yugoslavia": ["SRB", "MNE", "BIH", "HRV", "SVN", "MKD", "KOS"], "italy": ["ITA", "SMR", "VAT"],
    "switzerland": ["CHE", "LIE"], "france": ["FRA", "MCO", "AND"], "belgium": ["BEL"], "netherlands": ["NLD"],
    "luxembourg": ["LUX"], "denmark": ["DNK"], "norway": ["NOR"], "sweden": ["SWE"], "uk": ["GBR"],
    "ireland": ["IRL"], "iceland": ["ISL"], "spain": ["ESP"], "portugal": ["PRT"], "cyprus": ["CYP", "CYN"],
    "malta": ["MLT"], "morocco": ["MAR", "SAH"], "algeria": ["DZA"], "tunisia": ["TUN"], "libya": ["LBY"],
    "egypt": ["EGY"], "syria": ["SYR"], "lebanon": ["LBN"], "palestine": ["ISR", "PSX"], "jordan": ["JOR"],
    "iraq": ["IRQ"], "saudi": ["SAU"], "iran": ["IRN"],
    "ussr": ["RUS", "BLR", "UKR", "GEO", "ARM", "AZE", "KAZ", "UZB", "TKM", "KGZ", "TJK"],
}
# carved out of their modern hosts (in this order), then split further below
CUT = [("east_prussia", "ussr"), ("kresy", "ussr"), ("kresy", "lithuania"), ("bessarabia", "ussr"),
       ("bukovina", "ussr"), ("carpatho", "ussr"), ("fin_karelia", "ussr"), ("fin_petsamo", "ussr")]
# Aug 1939 owners (borders show only between different owners) and sides; scenes change them with owner()/side()
OWNER_1939 = {"germany": "germany", "g37east": "germany", "east_prussia": "germany", "austria": "germany",
              "sudeten": "germany", "czech": "germany", "slovakia": "slovakia", "poland_w": "poland",
              "poland_e": "poland", "kresy": "poland", "bessarabia": "romania", "bukovina": "romania",
              "romania": "romania", "carpatho": "hungary", "fin_karelia": "finland", "fin_petsamo": "finland",
              "france_occ": "france", "france_vichy": "france"}
SIDE_1939 = {"germany": "germany", "g37east": "germany", "east_prussia": "germany", "austria": "germany",
             "sudeten": "germany", "czech": "germany", "slovakia": "italy", "italy": "italy", "albania": "italy",
             "libya": "italy", "poland_w": "allies", "poland_e": "allies", "uk": "allies", "france_occ": "allies",
             "france_vichy": "allies", "ussr": "soviet"}
GROUPS = {"germany_1937": ["germany", "g37east", "east_prussia"],
          "greater_germany": ["germany", "g37east", "east_prussia", "austria", "sudeten", "czech"],
          "czechoslovakia": ["sudeten", "czech", "slovakia", "carpatho"], "poland": ["poland_w", "poland_e"],
          "france": ["france_occ", "france_vichy"], "low_countries": ["belgium", "netherlands", "luxembourg"],
          "baltics": ["lithuania", "latvia", "estonia"], "romania_1939": ["romania", "bessarabia", "bukovina"],
          "finland_1939": ["finland", "fin_karelia", "fin_petsamo"]}

PACIFIC = {
    "japan": ["JPN"], "korea": ["KOR", "PRK"], "taiwan": ["TWN"],
    "manchukuo": [("&", MANCHUKUO, ["CHN"])], "china_occ": [("&", CHINA_OCC, ["CHN"])], "china": ["CHN"],
    "mongolia": ["MNG"], "ussr": ["RUS", "KAZ"], "philippines": ["PHL"], "indochina": ["VNM", "LAO", "KHM"],
    "thailand": ["THA"], "burma": ["MMR"], "malaya": ["MYS", "SGP", "BRN"], "dei": ["IDN", "TLS"], "png": ["PNG"],
    "australia": ["AUS"], "nz": ["NZL"], "india": ["IND", "PAK", "BGD", "LKA", "NPL", "BTN"], "usa": ["USA"],
    "canada": ["CAN"], "mexico": ["MEX"], "solomons": ["SLB"],
}
PACIFIC_CUT = [("manchukuo", "china"), ("china_occ", "china"), ("manchukuo", "china_occ")]
PACIFIC_SIDE = {"japan": "japan", "korea": "japan", "taiwan": "japan", "manchukuo": "japan", "china_occ": "japan",
                "china": "china", "ussr": "soviet", "usa": "allies", "australia": "allies", "nz": "allies",
                "india": "allies", "burma": "allies", "malaya": "allies", "philippines": "allies"}

CITIES = {   # (lon, lat)
    "Berlin": (13.40, 52.52), "Warsaw": (21.01, 52.23), "Danzig": (18.65, 54.35), "Krakow": (19.94, 50.06),
    "Lwow": (24.03, 49.84), "Brest": (23.69, 52.10), "Moscow": (37.62, 55.75), "Leningrad": (30.32, 59.94),
    "Stalingrad": (44.52, 48.71), "Kiev": (30.52, 50.45), "Minsk": (27.56, 53.90), "Kursk": (36.19, 51.73),
    "Sevastopol": (33.52, 44.62), "London": (-0.13, 51.51), "Paris": (2.35, 48.86), "Rome": (12.50, 41.90),
    "Vienna": (16.37, 48.21), "Prague": (14.42, 50.09), "Budapest": (19.04, 47.50), "Bucharest": (26.10, 44.43),
    "Belgrade": (20.46, 44.79), "Athens": (23.73, 37.98), "Oslo": (10.75, 59.91), "Narvik": (17.43, 68.44),
    "Copenhagen": (12.57, 55.68), "Stockholm": (18.07, 59.33), "Helsinki": (24.94, 60.17), "Amsterdam": (4.90, 52.37),
    "Brussels": (4.35, 50.85), "Dunkirk": (2.38, 51.03), "Caen": (-0.37, 49.18), "Madrid": (-3.70, 40.42),
    "Lisbon": (-9.14, 38.72), "Tobruk": (23.96, 32.08), "El Alamein": (28.95, 30.83), "Alexandria": (29.92, 31.20),
    "Cairo": (31.24, 30.04), "Tunis": (10.18, 36.81), "Sicily": (14.0, 37.6), "Anzio": (12.63, 41.45),
    "Tokyo": (139.69, 35.69), "Pearl Harbor": (-157.95, 21.36), "Midway": (-177.37, 28.21),
    "Manila": (120.98, 14.60), "Singapore": (103.82, 1.35), "Guadalcanal": (160.0, -9.6), "Iwo Jima": (141.32, 24.78),
    "Okinawa": (127.80, 26.33), "Hiroshima": (132.46, 34.39), "Nagasaki": (129.87, 32.75),
    "Shanghai": (121.47, 31.23), "Nanjing": (118.80, 32.06), "Beijing": (116.40, 39.90), "Hong Kong": (114.17, 22.32),
    "Rangoon": (96.16, 16.80), "Darwin": (130.84, -12.46), "Port Moresby": (147.18, -9.44), "Mukden": (123.43, 41.80),
}


# ---------------------------------------------------------------- projections (sphere; the build uses the same)
def project(view, lon, lat):
    """lon/lat -> map pixels for a view (zoom 1: the view centre mid-frame, `width_km` across)."""
    v = VIEWS[view] if isinstance(view, str) else view
    x, y = _proj_m(v, lon, lat)
    cx, cy = _proj_m(v, *v["center"])
    s = W / (v["width_km"] * 1000.0)
    return (x - cx) * s + W / 2, (cy - y) * s + H / 2


def _proj_m(v, lon, lat):
    lam = math.radians(((lon - v["lon0"] + 180.0) % 360.0) - 180.0)
    phi = math.radians(lat)
    if v["proj"] == "laea":
        p0 = math.radians(v["lat0"])
        k = math.sqrt(2.0 / max(1e-12, 1 + math.sin(p0) * math.sin(phi) + math.cos(p0) * math.cos(phi) * math.cos(lam)))
        return (R_EARTH * k * math.cos(phi) * math.sin(lam),
                R_EARTH * k * (math.cos(p0) * math.sin(phi) - math.sin(p0) * math.cos(phi) * math.cos(lam)))
    a1, a2, a3, a4 = 1.340264, -0.081106, 0.000893, 0.003796       # Equal Earth (Savric, Patterson, Jenny 2018)
    th = math.asin(math.sqrt(3) / 2 * math.sin(phi))
    t2 = th * th
    t6 = t2 * t2 * t2
    x = R_EARTH * 2 * math.sqrt(3) * lam * math.cos(th) / (3 * (9 * a4 * t6 * t2 + 7 * a3 * t6 + 3 * a2 * t2 + a1))
    y = R_EARTH * th * (a4 * t6 * t2 + a3 * t6 + a2 * t2 + a1)
    return x, y


# ---------------------------------------------------------------- build (shapely; run once, output committed)
def _fetch(name):
    os.makedirs(NE, exist_ok=True)
    p = os.path.join(NE, name + ".geojson")
    if not os.path.exists(p):
        import urllib.request
        urllib.request.urlretrieve(NE_URL.format(name), p)
    with open(p) as f:
        return json.load(f)


def build_data(views=("europe", "pacific", "world")):
    from shapely.geometry import LineString, MultiPolygon, Polygon, box, shape
    from shapely.ops import linemerge, transform, unary_union
    countries = {}
    for ft in _fetch("ne_50m_admin_0_countries")["features"]:
        g = shape(ft["geometry"]).buffer(0)
        a3 = ft["properties"]["ADM0_A3"]
        countries[a3] = countries[a3].union(g) if a3 in countries else g
    lakes = [shape(ft["geometry"]).buffer(0) for ft in _fetch("ne_50m_lakes")["features"]
             if (ft["properties"].get("scalerank") or 9) <= 4]

    def kaliningrad():
        return unary_union([p for p in getattr(countries["RUS"], "geoms", [countries["RUS"]])
                            if p.centroid.x < 23 and p.centroid.y < 56])

    def cook(recipe):
        parts = []
        for r in recipe:
            if isinstance(r, str):
                parts.append(countries.get(r, Polygon()))
            elif r[0] == "kaliningrad":
                parts.append(kaliningrad())
            else:
                host = unary_union([countries.get(c, Polygon()) for c in r[2]])
                parts.append(host.intersection(Polygon(r[1])))
        return unary_union(parts).buffer(0)

    os.makedirs(DATA, exist_ok=True)
    for view in views:
        v = VIEWS[view]
        clip = unary_union([box(*b) for b in v["clip"]])
        if view == "europe":
            recipes, cuts = EUROPE, CUT
        elif view == "pacific":
            recipes, cuts = PACIFIC, PACIFIC_CUT
        else:
            recipes = {a3.lower(): [a3] for a3 in countries}
            cuts = []
        geo = {k: cook(r) for k, r in recipes.items()}
        if view == "europe":                                           # generous outlines, trimmed to meet kresy
            geo["bukovina"] = geo["bukovina"].difference(geo["kresy"]).buffer(0)
            geo["carpatho"] = geo["carpatho"].difference(geo["kresy"]).difference(geo["bukovina"]).buffer(0)
        for small, big in cuts:
            geo[big] = geo[big].difference(geo[small]).buffer(0)
        if view == "europe":                                           # 1939 Poland, its split; Sudetenland; France
            pol = countries["POL"].difference(geo["g37east"]).difference(geo["east_prussia"])
            pol = pol.union(geo.pop("kresy")).buffer(0)
            west = Polygon(SPLIT_1939 + [(14.0, 48.5), (14.0, 55.5), (23.5, 55.5)])
            geo["poland_w"], geo["poland_e"] = pol.intersection(west).buffer(0), pol.difference(west).buffer(0)
            fr = geo.pop("france")
            geo["france_vichy"] = fr.intersection(Polygon(VICHY)).buffer(0)
            geo["france_occ"] = fr.difference(Polygon(VICHY)).buffer(0)
        land_all = unary_union(list(countries.values())).buffer(0)
        s = W / (v["width_km"] * 1000.0)
        cx, cy = _proj_m(v, *v["center"])

        def to_px(x, y, z=None):
            return (x - cx) * s + W / 2, (cy - y) * s + H / 2

        def prj(g):
            g = g.intersection(clip)
            if g.is_empty:
                return g
            g = transform(lambda lon, lat, z=None: _vec(v, lon, lat), g)
            return transform(to_px, g).buffer(0)

        pg = {k: prj(g) for k, g in geo.items()}
        pg = {k: g for k, g in pg.items() if not g.is_empty and g.area > 4}
        if view == "europe":                                           # the Sudetenland: the Czech border band
            cz = prj(countries["CZE"])
            band = pg["germany"].union(pg["austria"]).union(pg["g37east"]).buffer(40000 * s)
            pg["sudeten"] = cz.intersection(band).buffer(0)
            pg["czech"] = cz.difference(band).buffer(0)
        land = prj(land_all)
        tol = 0.22 if view == "europe" else 0.35
        out = dict(meta=dict(view=view, **{k: v[k] for k in ("proj", "lon0", "lat0", "center", "width_km")}, q=Q),
                   regions={}, labels={}, edges={}, land=_rings(land.simplify(tol), Q),
                   lakes=_rings(unary_union([prj(lk) for lk in lakes]).simplify(tol), Q),
                   ripples=[], cities={k: [round(c, 1) for c in project(view, *ll)] for k, ll in CITIES.items()})
        for k, g in sorted(pg.items()):
            out["regions"][k] = _rings(g.simplify(tol / 2), Q)
            big = max(getattr(g, "geoms", [g]), key=lambda p: p.area)
            lp = big.representative_point()
            out["labels"][k] = [round(lp.x, 1), round(lp.y, 1)]
        names = sorted(pg)                                             # shared edges, for owner-aware borders
        bounds = {k: pg[k].bounds for k in names}
        for i, a in enumerate(names):
            for b in names[i + 1:]:
                ba, bb = bounds[a], bounds[b]
                if ba[2] < bb[0] - 1 or bb[2] < ba[0] - 1 or ba[3] < bb[1] - 1 or bb[3] < ba[1] - 1:
                    continue
                e = pg[a].buffer(0.6).intersection(pg[b].boundary)
                if e.is_empty or e.length < 3:
                    continue
                lines = [ln for ln in getattr(e, "geoms", [e]) if isinstance(ln, LineString)]
                m = linemerge(lines) if lines else None
                if m is not None and not m.is_empty:
                    out["edges"][f"{a}|{b}"] = _lines(m.simplify(tol), Q)
        for km in (8, 17, 28):                                         # coast ripples on the sea
            r = land.buffer(km * 1000 * s, quad_segs=4).simplify(tol * 2)
            out["ripples"].append(_lines(r.boundary, Q))
        with open(os.path.join(DATA, view + ".json"), "w") as f:
            json.dump(out, f, separators=(",", ":"))
        print(view, len(out["regions"]), "regions", len(out["edges"]), "edges",
              os.path.getsize(os.path.join(DATA, view + ".json")) // 1024, "KB")


def _vec(v, lon, lat):
    import numpy as np
    lon, lat = np.asarray(lon, float), np.asarray(lat, float)
    xy = [_proj_m(v, a, b) for a, b in zip(lon.ravel(), lat.ravel())]
    return np.array([p[0] for p in xy]).reshape(lon.shape), np.array([p[1] for p in xy]).reshape(lat.shape)


def _rings(g, q):
    out = []
    for p in getattr(g, "geoms", [g]):
        if p.is_empty or p.geom_type != "Polygon":
            continue
        for ring in [p.exterior, *p.interiors]:
            pts = [c for xy in ring.coords for c in (int(round(xy[0] * q)), int(round(xy[1] * q)))]
            if len(pts) >= 6:
                out.append(pts)
    return out


def _lines(g, q):
    out = []
    for ln in getattr(g, "geoms", [g]):
        if ln.is_empty:
            continue
        if ln.geom_type in ("LinearRing", "LineString"):
            pts = [c for xy in ln.coords for c in (int(round(xy[0] * q)), int(round(xy[1] * q)))]
            if len(pts) >= 4:
                out.append(pts)
        elif hasattr(ln, "geoms"):
            out += _lines(ln, q)
    return out


# ---------------------------------------------------------------- runtime
_CACHE = {}


def _load(view):
    if view not in _CACHE:
        with open(os.path.join(DATA, view + ".json")) as f:
            _CACHE[view] = json.load(f)
    return _CACHE[view]


def _path(rings, closed=True):
    """A cairo path (in map pixels) from flat int rings, built once."""
    surf = cairo.ImageSurface(cairo.FORMAT_A8, 1, 1)
    c = cairo.Context(surf)
    for r in rings:
        c.move_to(r[0] / Q, r[1] / Q)
        for i in range(2, len(r), 2):
            c.line_to(r[i] / Q, r[i + 1] / Q)
        if closed:
            c.close_path()
    return c.copy_path()


def _catmull(pts, n=12):
    """A smooth curve through pts (Catmull-Rom), sampled n points per span."""
    if len(pts) < 3:
        return [(lerp(pts[0][0], pts[-1][0], i / (n * 2)), lerp(pts[0][1], pts[-1][1], i / (n * 2)))
                for i in range(n * 2 + 1)]
    P = [pts[0]] + list(pts) + [pts[-1]]
    out = []
    for i in range(1, len(P) - 2):
        p0, p1, p2, p3 = P[i - 1], P[i], P[i + 1], P[i + 2]
        for k in range(n):
            u = k / n
            u2, u3 = u * u, u * u * u
            out.append(tuple(0.5 * (2 * p1[j] + (-p0[j] + p2[j]) * u + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * u2
                                    + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * u3) for j in (0, 1)))
    out.append(tuple(pts[-1]))
    return out


def _cut(poly, length):
    """The polyline's first `length` (in its own units) and the arc length of the whole."""
    out, acc = [poly[0]], 0.0
    for a, b in zip(poly, poly[1:]):
        d = math.hypot(b[0] - a[0], b[1] - a[1])
        if acc + d >= length:
            u = (length - acc) / d if d else 0
            out.append((lerp(a[0], b[0], u), lerp(a[1], b[1], u)))
            return out
        out.append(b)
        acc += d
    return out


def _length(poly):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(poly, poly[1:]))


def _resample(poly, n):
    L = _length(poly)
    return [_cut(poly, L * i / (n - 1))[-1] for i in range(n)]


class Map:
    """One map view. Set it up once (sides, owners, arrows, fronts, cities, labels, camera keys), then call
    draw(cr, t) every frame. All times are seconds in the scene; places are (lon, lat)."""

    def __init__(self, view="europe", sides=None, owners=None):
        self.view = view
        d = _load(view)
        self.d = d
        self.paths = {k: _path(r) for k, r in d["regions"].items()}
        self.land = _path(d["land"])
        self.lakes = _path(d["lakes"])
        self.ripples = [_path(r, closed=False) for r in d["ripples"]]
        self.edges = {k: _path(r, closed=False) for k, r in d["edges"].items()}
        self.bbox = {k: self._bbox(r) for k, r in d["regions"].items()}
        default = SIDE_1939 if view == "europe" else PACIFIC_SIDE if view == "pacific" else {}
        self._side = {k: [(-1e9, (sides or default).get(k, "neutral"), None, 0.0)] for k in self.paths}
        own = OWNER_1939 if view == "europe" else {}
        self._owner = {k: [(-1e9, (owners or own).get(k, k))] for k in self.paths}
        self.arrows, self.fronts, self.secrets, self.cities, self.labels, self.stamps = [], [], [], [], [], []
        self.cam = []

    @staticmethod
    def _bbox(rings):
        xs = [r[i] / Q for r in rings for i in range(0, len(r), 2)]
        ys = [r[i] / Q for r in rings for i in range(1, len(r), 2)]
        return min(xs), min(ys), max(xs), max(ys)

    def xy(self, lonlat):
        return project(self.view, *lonlat)

    def regions(self, name):
        return GROUPS.get(name, [name])

    # ------------------------------------------------------------ setup
    def side(self, name, t, side, origin=None, dur=1.0):
        """From t, `name` (a region or a GROUPS name) turns `side`; with `origin` (lon, lat) the colour floods out
        from there over `dur` seconds instead of switching."""
        for r in self.regions(name):
            if r in self._side:
                self._side[r].append((t, side, self.xy(origin) if origin else None, dur))
                self._side[r].sort(key=lambda e: e[0])

    def owner(self, name, t, owner):
        """From t, `name` belongs to `owner`: borders between regions of one owner disappear (an annexation)."""
        for r in self.regions(name):
            if r in self._owner:
                self._owner[r].append((t, owner))
                self._owner[r].sort(key=lambda e: e[0])

    def arrow(self, lonlats, side, t0, t1, width=46.0, hold=None):
        """An attack arrow along a smooth path through `lonlats`, growing from t0 to t1 (side colour, ink outline,
        white inner highlight, arrowhead). width is in screen pixels at the head; `hold` ends it (fades) at that time."""
        self.arrows.append(dict(pts=_catmull([self.xy(p) for p in lonlats]), side=side, t0=t0, t1=t1, w=width,
                                hold=hold))

    def front(self, keys, width=7.0, side=None, t_in=None, t_out=None):
        """A front line moving between keyframed polylines: keys = [(t, [(lon, lat), ...]), ...]."""
        self.fronts.append(dict(keys=[(t, _resample(_catmull([self.xy(p) for p in pts], 6), 64)) for t, pts in keys],
                                w=width, side=side, t_in=t_in if t_in is not None else keys[0][0], t_out=t_out))

    def secret_line(self, lonlats, t0, t1, color="alert", width=5.0, t_out=None):
        """A dashed line drawn along `lonlats` from t0 to t1 (the secret protocol), gone at t_out."""
        self.secrets.append(dict(pts=_catmull([self.xy(p) for p in lonlats], 6), t0=t0, t1=t1, color=color, w=width,
                                 t_out=t_out))

    def stamp(self, word, lonlat, t0, t_out=None, size=78, color="alert", tilt=-0.12):
        """A rubber-stamp word ("SECRET") that slams down at lonlat at t0."""
        self.stamps.append(dict(word=word, at=self.xy(lonlat), t0=t0, t_out=t_out, size=size, color=color, tilt=tilt))

    def city(self, name, t0, t_out=None, lonlat=None, label=True, pulse=True, dx=16, dy=-14, size=32):
        """A city dot (with its name) from t0; it pulses for a second when it appears."""
        self.cities.append(dict(name=name, at=self.xy(lonlat or CITIES[name]), t0=t0, t_out=t_out, label=label,
                                pulse=pulse, dx=dx, dy=dy, size=size))

    def label(self, s, t0, t_out=None, lonlat=None, region=None, size=44, color="ink", tilt=0.0, spacing=2.0):
        """A Kalam map label at lonlat (or at a region's label point), fading in at t0."""
        at = self.xy(lonlat) if lonlat else tuple(self.d["labels"][region])
        self.labels.append(dict(s=s, at=at, t0=t0, t_out=t_out, size=size, color=color, tilt=tilt, sp=spacing))

    def camera_key(self, t, lonlat, zoom):
        """The camera looks at lonlat with `zoom` at time t; between keys it eases (smooth in and out)."""
        self.cam.append((t, self.xy(lonlat), zoom))
        self.cam.sort(key=lambda k: k[0])

    # ------------------------------------------------------------ state at t
    def camera_at(self, t):
        if not self.cam:
            return (W / 2, H / 2), 1.0
        if t <= self.cam[0][0]:
            return self.cam[0][1], self.cam[0][2]
        for (ta, pa, za), (tb, pb, zb) in zip(self.cam, self.cam[1:]):
            if t <= tb:
                u = smooth(seg(t, ta, tb))
                lz = lerp(math.log(za), math.log(zb), u)                # zoom eases in log space (even speed)
                return (lerp(pa[0], pb[0], u), lerp(pa[1], pb[1], u)), math.exp(lz)
        return self.cam[-1][1], self.cam[-1][2]

    def _owner_at(self, r, t):
        o = self._owner[r][0][1]
        for tt, ow in self._owner[r]:
            if t >= tt:
                o = ow
        return o

    def _side_at(self, r, t):
        """(side before, side now, flood origin, flood progress 0-1)."""
        hist = self._side[r]
        prev, cur = hist[0], hist[0]
        for e in hist[1:]:
            if t >= e[0]:
                prev, cur = cur, e
        if cur[2] is None or cur[3] <= 0:
            return cur[1], cur[1], None, 1.0
        return prev[1], cur[1], cur[2], clamp01((t - cur[0]) / cur[3])

    # ------------------------------------------------------------ draw
    def draw(self, cr, t):
        (cx, cy), z = self.camera_at(t)
        self._z, self._c = z, (cx, cy)
        cr.save()
        cr.set_source_rgba(*col("sea", 0.86))                       # the sea over the paper (its grain shows through)
        cr.paint()
        cr.translate(W / 2, H / 2)
        cr.scale(z, z)
        cr.translate(-cx, -cy)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        for i, rp in enumerate(self.ripples):                       # coast ripples, fainter farther out
            cr.new_path()
            cr.append_path(rp)
            cr.set_source_rgba(*col("sea_dk", 0.75 - 0.2 * i))
            cr.set_line_width(1.6 / z)
            cr.stroke()
        cr.new_path()
        cr.append_path(self.land)                                    # neutral land under everything
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.set_source_rgba(*col("land"))
        cr.fill()
        for r, p in self.paths.items():
            self._fill_region(cr, r, p, t, z)
        cr.new_path()                                                # lakes
        cr.append_path(self.lakes)
        cr.set_source_rgba(*col("sea", 0.95))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink_soft", 0.8))
        cr.set_line_width(1.0 / z)
        cr.stroke()
        cr.set_line_width(1.5 / z)                                   # borders, only between different owners
        cr.set_source_rgba(*col("ink_soft", 0.9))
        for k, p in self.edges.items():
            a, b = k.split("|")
            if self._owner_at(a, t) != self._owner_at(b, t):
                cr.new_path()
                cr.append_path(p)
                cr.stroke()
        cr.new_path()                                                # coastline
        cr.append_path(self.land)
        cr.set_source_rgba(*col("ink", 0.92))
        cr.set_line_width(2.5 / z)
        cr.stroke()
        for f in self.fronts:
            self._draw_front(cr, f, t, z)
        for s in self.secrets:
            self._draw_secret(cr, s, t, z)
        for a in self.arrows:
            self._draw_arrow(cr, a, t, z)
        cr.restore()
        for lb in self.labels:                                       # screen-space type: crisp at any zoom
            self._draw_label(cr, lb, t)
        for c in self.cities:
            self._draw_city(cr, c, t)
        for s in self.stamps:
            self._draw_stamp(cr, s, t)
        cr.save()                                                    # the paper's grain back over the flat fills
        cr.set_operator(cairo.OPERATOR_MULTIPLY)
        cr.set_source_surface(paper_surface(), 0, 0)
        cr.paint_with_alpha(0.45)
        cr.restore()

    def screen(self, p):
        """Map pixels -> screen pixels with the camera of the last draw()."""
        (cx, cy), z = self._c, self._z
        return (p[0] - cx) * z + W / 2, (p[1] - cy) * z + H / 2

    def _fill_region(self, cr, r, p, t, z):
        before, now, origin, u = self._side_at(r, t)
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.new_path()
        cr.append_path(p)
        cr.set_source_rgba(*col(before if u < 1 else now))
        cr.fill_preserve()
        cr.set_line_width(1.2 / z)                                   # seal hairline seams between pieces
        cr.stroke()
        if u >= 1 or origin is None:
            return
        x0, y0, x1, y1 = self.bbox[r]
        far = max(math.hypot(x - origin[0], y - origin[1]) for x in (x0, x1) for y in (y0, y1))
        rad = far * ease_out(u) * 1.04
        if rad <= 0:
            return
        cr.save()
        cr.new_path()
        cr.append_path(p)
        cr.clip()
        rnd = random.Random(hash(r) & 0xffff)
        ph = [rnd.uniform(0, 6.28) for _ in range(3)]
        cr.new_path()
        n = 72
        for k in range(n + 1):                                       # a wobbly flood front
            a = k / n * 2 * math.pi
            rr = rad * (1 + 0.05 * math.sin(3 * a + ph[0]) + 0.035 * math.sin(7 * a + ph[1] + t * 3)
                        + 0.02 * math.sin(13 * a + ph[2]))
            (cr.move_to if k == 0 else cr.line_to)(origin[0] + rr * math.cos(a), origin[1] + rr * math.sin(a))
        cr.close_path()
        cr.set_source_rgba(*col(now))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink", 0.45))
        cr.set_line_width(2.4 / z)
        cr.stroke()
        cr.restore()

    def _draw_arrow(self, cr, a, t, z):
        u = ease_out(seg(t, a["t0"], a["t1"]))
        if u <= 0:
            return
        fade = 1.0 - (ease_in(seg(t, a["hold"], a["hold"] + 0.4)) if a["hold"] is not None else 0.0)
        if fade <= 0:
            return
        L = _length(a["pts"])
        body = _cut(a["pts"], L * u)
        if len(body) < 2:
            return
        w = a["w"] / z
        head_len = min(1.5 * w, _length(body) * 0.6)
        shaft = _cut(body, max(0.0, _length(body) - head_len))
        tip, base = body[-1], shaft[-1]
        left, right = [], []
        n = len(shaft)
        for i, p in enumerate(shaft):                                # tapered shaft: 45 % at the tail to 62 % at the neck
            q = shaft[min(i + 1, n - 1)] if i < n - 1 else tip
            o = shaft[max(i - 1, 0)] if i > 0 else p
            dx, dy = q[0] - o[0], q[1] - o[1]
            d = math.hypot(dx, dy) or 1.0
            hw = w * lerp(0.24, 0.34, i / max(1, n - 1))
            left.append((p[0] - dy / d * hw, p[1] + dx / d * hw))
            right.append((p[0] + dy / d * hw, p[1] - dx / d * hw))
        dx, dy = tip[0] - base[0], tip[1] - base[1]
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        hw = w * 0.62
        poly = left + [(base[0] + nx * hw, base[1] + ny * hw), tip, (base[0] - nx * hw, base[1] - ny * hw)] + right[::-1]
        cr.new_path()
        for i, p in enumerate(poly):
            (cr.move_to if i == 0 else cr.line_to)(*p)
        cr.close_path()
        cr.set_source_rgba(*col("paper", 0.9 * fade))                # a paper halo, so grey arrows read over grey land
        cr.set_line_width(9.0 / z)
        cr.stroke_preserve()
        cr.set_source_rgba(*col(a["side"], fade))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink", fade))
        cr.set_line_width(3.0 / z)
        cr.stroke()
        if len(shaft) > 2:                                           # the white inner highlight
            cr.new_path()
            hl = shaft[:max(2, int(len(shaft) * 0.92))]
            for i, p in enumerate(hl):
                (cr.move_to if i == 0 else cr.line_to)(p[0] - (right[i][0] - left[i][0]) * 0.18,
                                                       p[1] - (right[i][1] - left[i][1]) * 0.18)
            cr.set_source_rgba(*col("white", 0.55 * fade))
            cr.set_line_width(max(1.5, a["w"] * 0.09) / z)
            cr.stroke()

    def _draw_front(self, cr, f, t, z):
        if t < f["t_in"] or (f["t_out"] is not None and t > f["t_out"]):
            return
        keys = f["keys"]
        pts = keys[0][1]
        for (ta, pa), (tb, pb) in zip(keys, keys[1:]):
            if t >= tb:
                pts = pb
            elif t > ta:
                u = smooth(seg(t, ta, tb))
                pts = [(lerp(a[0], b[0], u), lerp(a[1], b[1], u)) for a, b in zip(pa, pb)]
                break
        a_in = ease_out(seg(t, f["t_in"], f["t_in"] + 0.4))
        a_out = 1 - (ease_in(seg(t, f["t_out"] - 0.4, f["t_out"])) if f["t_out"] is not None else 0)
        wob = []
        for i, p in enumerate(pts):                                  # a slow hand wobble
            q = pts[min(i + 1, len(pts) - 1)]
            o = pts[max(i - 1, 0)]
            dx, dy = q[0] - o[0], q[1] - o[1]
            d = math.hypot(dx, dy) or 1.0
            k = (2.2 * math.sin(i * 0.9 + t * 2.1) + 1.4 * math.sin(i * 2.3 - t * 1.3)) / z
            wob.append((p[0] - dy / d * k, p[1] + dx / d * k))
        for lw, c, alpha in ((f["w"] + 4, "paper", 0.8), (f["w"], f["side"] or "ink", 1.0)):
            cr.new_path()
            for i, p in enumerate(wob):
                (cr.move_to if i == 0 else cr.line_to)(*p)
            cr.set_source_rgba(*col(c, alpha * a_in * a_out))
            cr.set_line_width(lw / z)
            cr.stroke()

    def _draw_secret(self, cr, s, t, z):
        u = smooth(seg(t, s["t0"], s["t1"]))
        if u <= 0 or (s["t_out"] is not None and t > s["t_out"] + 0.4):
            return
        a = 1 - (ease_in(seg(t, s["t_out"], s["t_out"] + 0.4)) if s["t_out"] is not None else 0)
        pts = _cut(s["pts"], _length(s["pts"]) * u)
        cr.new_path()
        for i, p in enumerate(pts):
            (cr.move_to if i == 0 else cr.line_to)(*p)
        cr.set_dash([16 / z, 11 / z])
        cr.set_source_rgba(*col("paper", 0.85 * a))
        cr.set_line_width((s["w"] + 4) / z)
        cr.stroke_preserve()
        cr.set_source_rgba(*col(s["color"], a))
        cr.set_line_width(s["w"] / z)
        cr.stroke()
        cr.set_dash([])

    def _draw_label(self, cr, lb, t):
        a = ease_out(seg(t, lb["t0"], lb["t0"] + 0.45))
        if lb["t_out"] is not None:
            a *= 1 - ease_in(seg(t, lb["t_out"], lb["t_out"] + 0.4))
        if a <= 0:
            return
        x, y = self.screen(lb["at"])
        cr.save()
        cr.translate(x, y)
        cr.rotate(lb["tilt"])
        text(cr, lb["s"], 0, lb["size"] * 0.35, lb["size"], font=HAND, color=lb["color"], alpha=a, outline="paper",
             outline_w=lb["size"] * 0.16, spacing=lb["sp"])
        cr.restore()

    def _draw_city(self, cr, c, t):
        if t < c["t0"] or (c["t_out"] is not None and t > c["t_out"] + 0.4):
            return
        a = 1 - (ease_in(seg(t, c["t_out"], c["t_out"] + 0.4)) if c["t_out"] is not None else 0)
        x, y = self.screen(c["at"])
        pop = back_out(seg(t, c["t0"], c["t0"] + 0.3))
        if c["pulse"]:
            for k in range(2):                                       # two rings ripple out for a second
                v = seg(t, c["t0"] + k * 0.35, c["t0"] + k * 0.35 + 0.9)
                if 0 < v < 1:
                    cr.new_path()
                    cr.arc(x, y, 9 + 30 * ease_out(v), 0, 2 * math.pi)
                    cr.set_source_rgba(*col("alert", 0.8 * (1 - v) * a))
                    cr.set_line_width(3.0)
                    cr.stroke()
        cr.new_path()
        cr.arc(x, y, 8.5 * pop, 0, 2 * math.pi)
        cr.set_source_rgba(*col("paper", a))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink", a))
        cr.set_line_width(3.0)
        cr.stroke()
        cr.arc(x, y, 3.6 * pop, 0, 2 * math.pi)
        cr.fill()
        if c["label"]:
            la = a * ease_out(seg(t, c["t0"] + 0.1, c["t0"] + 0.45))
            text(cr, c["name"], x + c["dx"], y + c["dy"], c["size"], font=HAND, color="ink", align="left", alpha=la,
                 outline="paper", outline_w=c["size"] * 0.18)

    def _draw_stamp(self, cr, s, t):
        if t < s["t0"] or (s["t_out"] is not None and t > s["t_out"] + 0.35):
            return
        u = back_out(seg(t, s["t0"], s["t0"] + 0.25))
        a = min(1.0, u * 1.5) * (1 - (ease_in(seg(t, s["t_out"], s["t_out"] + 0.35)) if s["t_out"] is not None else 0))
        x, y = self.screen(s["at"])
        cr.save()
        cr.translate(x, y)
        cr.rotate(s["tilt"])
        k = 1.8 - 0.8 * u
        cr.scale(k, k)
        size = s["size"]
        cr.select_font_face(TITLE)
        cr.set_font_size(size)
        wd = cr.text_extents(s["word"]).x_advance + 4 * (len(s["word"]) - 1)
        for inset, lw in ((0, 6.0), (11, 2.5)):                      # a double stamp border
            cr.rectangle(-wd / 2 - 26 + inset, -size * 0.78 + inset, wd + 52 - 2 * inset, size * 1.22 - 2 * inset)
            cr.set_source_rgba(*col(s["color"], 0.88 * a))
            cr.set_line_width(lw)
            cr.stroke()
        text(cr, s["word"], 0, size * 0.36, size, font=TITLE, color=s["color"], bold=False, alpha=0.88 * a, spacing=4)
        cr.restore()


if __name__ == "__main__" and sys.argv[1:2] == ["build"]:
    build_data(tuple(sys.argv[2:]) or ("europe", "pacific", "world"))
