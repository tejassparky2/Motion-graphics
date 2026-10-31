"""WW2 channel kit, maps: Natural Earth countries and 1938-1945 historical regions, three projections, and a Map you
draw every frame with a camera, skinned as a printed 1940s war map (STYLE.md, "Maps"): aged-paper land, a grey-green
sea hatched along the coasts, ink coastlines, dashed borders, a light lat/long grid and a compass rose; sides in the
poster inks, occupied or annexed land halftoned; fills that flood from a point, fat poster arrows with a hard shadow
that grow along curves, moving front lines, the dashed "secret line", stamps, pulsing cities, Oswald/stencil labels.

    from channels.ww2.kit.maps import Map
    m = Map("europe")                                   # or "pacific", "world"
    m.side("poland_w", 4.4, "germany", origin=(16.5, 52.3), dur=1.2)    # floods grey (halftoned: occupied)
    m.arrow([(14.6, 53.2), (17.5, 52.9), (20.4, 52.3)], "germany", 3.2, 4.6)
    m.camera_key(0, (15, 52), 1.0); m.camera_key(3.5, (19.5, 52), 2.6)
    m.draw(cr, t)                                       # inside the scene's draw(cr, t), after paper(cr); then the
                                                        # date tag, and print_finish(cr, t) last

Data: Natural Earth admin-0 50m and lakes (public domain), downloaded once into build/ww2/ne/; build_data() projects,
cuts the historical regions and caches compact JSON in channels/ww2/data/<view>.json (committed), so a render needs
only json + cairo. The historical borders (Germany 1937 with East Prussia, the Sudetenland, Poland 1939 and its
September split, Bessarabia, Bukovina, Carpatho-Ukraine, Finnish Karelia, the 1940 demarcation line in France) are
Natural Earth land cut by hand-traced lon/lat lines (admin-1 at 50m doesn't cover Europe): close at this scale, not
survey-exact.

    /home/user/.venv-main/bin/python -m channels.ww2.kit.maps build       # (re)build the cached views
"""
import json
import math
import os
import random
import sys

from channels.ww2.kit.core import (H, LABEL, ROOT, STENCIL, W, _dot_tile, back_out, cairo, clamp01, col,
                                   ease_in, ease_out, lerp, seg, smooth, text)

DATA = os.path.join(ROOT, "channels", "ww2", "data")
NE = os.path.join(ROOT, "build", "ww2", "ne")
NE_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/{}.geojson"
R_EARTH = 6371000.0                 # a sphere in the build and at runtime, so lon/lat placed live lines up exactly
Q = 4                               # stored coordinates are map pixels x Q, as ints

# map pixels: at zoom 1 the view's centre sits mid-frame and `width_km` spans the 1920 px width
VIEWS = {
    "europe": dict(proj="laea", lon0=15.0, lat0=52.0, center=(15.0, 52.0), width_km=5200,
                   clip=[(-32, 0, 72, 76)], grid=5, grid_lon=(-40, 80), grid_lat=(0, 80)),
    "pacific": dict(proj="eqearth", lon0=160.0, lat0=0.0, center=(145.0, 15.0), width_km=17000,
                    clip=[(25, -52, 180, 72), (-180, -52, -25, 72)], grid=15, grid_lon=(-335, -25),
                    grid_lat=(-60, 75)),
    "world": dict(proj="eqearth", lon0=0.0, lat0=0.0, center=(10.0, 8.0), width_km=38000,
                  clip=[(-179.9, -60, 179.9, 84)], grid=30, grid_lon=(-180, 180), grid_lat=(-60, 75)),
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
RHINELAND = [(5.8, 51.95), (7.2, 52.1), (7.6, 51.5), (8.2, 50.9), (8.7, 50.2), (8.6, 49.6), (8.4, 49.0),
             (8.0, 48.5), (7.9, 47.6), (5.8, 47.6)]                            # west of the Rhine plus its strip
ITALY_SOUTH = [(12.0, 41.25), (13.75, 41.22), (14.0, 41.7), (14.45, 42.35), (19.5, 42.35), (19.5, 35.5),
               (12.0, 35.5)]                                                   # south of the Gustav line
SICILY = [(12.2, 36.5), (15.8, 36.5), (15.8, 38.4), (12.2, 38.4)]
MANCHUKUO = [(116.5, 40.5), (121.5, 39.0), (124.3, 39.8), (131.0, 42.5), (135.2, 48.5), (127.5, 53.6), (120.0, 53.3),
             (119.5, 50.0), (116.5, 46.5)]
CHINA_OCC = [(110.5, 41.0), (117.5, 41.0), (122.0, 37.5), (122.3, 31.0), (120.5, 28.0), (117.0, 23.5), (114.5, 22.2),
             (112.5, 21.5), (112.8, 24.5), (113.5, 29.0), (111.5, 31.0), (110.5, 35.0)]     # occupied by 1939-40

# region name -> recipe: ADM0_A3 codes to union, then optional ("&", poly, codes) cuts. Built in that order.
EUROPE = {
    "germany": ["DEU"], "rhineland": [("&", RHINELAND, ["DEU"])], "austria": ["AUT"], "slovakia": ["SVK"],
    "sicily": [("&", SICILY, ["ITA"])], "italy_south": [("&", ITALY_SOUTH, ["ITA"])],
    "ethiopia": ["ETH"], "eritrea": ["ERI"], "somalia": ["SOM", "SOL"], "djibouti": ["DJI"], "sudan": ["SDN", "SSD"],
    "kenya": ["KEN"], "yemen": ["YEM"],
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
CUT = [("rhineland", "germany"), ("sicily", "italy_south"), ("italy_south", "italy"), ("sicily", "italy"),
       ("east_prussia", "ussr"), ("kresy", "ussr"), ("kresy", "lithuania"), ("bessarabia", "ussr"),
       ("bukovina", "ussr"), ("carpatho", "ussr"), ("fin_karelia", "ussr"), ("fin_petsamo", "ussr")]
GROUPS = {"germany_1937": ["germany", "g37east", "east_prussia"],
          "greater_germany": ["germany", "g37east", "east_prussia", "austria", "sudeten", "czech"],
          "czechoslovakia": ["sudeten", "czech", "slovakia", "carpatho"], "poland": ["poland_w", "poland_e"],
          "france": ["france_occ", "france_vichy"], "low_countries": ["belgium", "netherlands", "luxembourg"],
          "baltics": ["lithuania", "latvia", "estonia"], "romania_1939": ["romania", "bessarabia", "bukovina"],
          "finland_1939": ["finland", "fin_karelia", "fin_petsamo"],
          "germany_1936": ["germany", "g37east", "east_prussia", "rhineland"],
          "italy_all": ["italy", "italy_south", "sicily"], "east_africa": ["ethiopia", "eritrea", "somalia"]}
DEFAULT_ERA = {"europe": "1939", "pacific": "1941"}

PACIFIC = {
    "japan": ["JPN"], "korea": ["KOR", "PRK"], "taiwan": ["TWN"],
    "manchukuo": [("&", MANCHUKUO, ["CHN"])], "china_occ": [("&", CHINA_OCC, ["CHN"])], "china": ["CHN"],
    "mongolia": ["MNG"], "ussr": ["RUS", "KAZ"], "philippines": ["PHL"], "indochina": ["VNM", "LAO", "KHM"],
    "thailand": ["THA"], "burma": ["MMR"], "malaya": ["MYS", "SGP", "BRN"], "dei": ["IDN", "TLS"], "png": ["PNG"],
    "australia": ["AUS"], "nz": ["NZL"], "india": ["IND", "PAK", "BGD", "LKA", "NPL", "BTN"], "usa": ["USA"],
    "canada": ["CAN"], "mexico": ["MEX"], "solomons": ["SLB"],
}
PACIFIC_CUT = [("manchukuo", "china"), ("china_occ", "china"), ("manchukuo", "china_occ")]
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
    "Auschwitz": (19.20, 50.03), "Treblinka": (22.05, 52.63), "Addis Ababa": (38.75, 9.03), "Voronezh": (39.20, 51.67),
    "Bastogne": (5.72, 50.00), "Kharkov": (36.25, 49.99), "Rostov": (39.72, 47.24), "Benghazi": (20.07, 32.12),
    "Tripoli": (13.18, 32.89), "Salerno": (14.77, 40.68), "Monte Cassino": (13.81, 41.49), "Arnhem": (5.90, 51.98),
    "Torgau": (13.00, 51.56), "Wake": (166.60, 19.30), "Guam": (144.79, 13.44), "Saipan": (145.75, 15.18),
    "Tarawa": (172.97, 1.42), "Leyte": (125.00, 10.90), "Imphal": (93.94, 24.81), "Mandalay": (96.08, 21.96),
    "Harbin": (126.63, 45.75), "Rangoon": (96.16, 16.80), "Darwin": (130.84, -12.46), "Port Moresby": (147.18, -9.44), "Mukden": (123.43, 41.80),
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
    from shapely.geometry import LineString, Polygon, box, shape
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
        if view == "europe":                                           # 1939 Poland, its split; France 1940
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
                   bands=[], cities={k: [round(c, 1) for c in project(view, *ll)] for k, ll in CITIES.items()})
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
        for km in (11, 24):                                            # the coastal hatching bands (land + margin)
            out["bands"].append(_rings(land.buffer(km * 1000 * s, quad_segs=4).simplify(tol * 2), Q))
        with open(os.path.join(DATA, view + ".json"), "w") as f:
            json.dump(out, f, separators=(",", ":"))
        print(view, len(out["regions"]), "regions", len(out["edges"]), "edges",
              os.path.getsize(os.path.join(DATA, view + ".json")) // 1024, "KB")


def build_content():
    """Write channels/ww2/data/fronts.json from map_content.py (fronts, arrows, lines, zones, pins, views, eras)."""
    from channels.ww2.kit import map_content
    os.makedirs(DATA, exist_ok=True)
    p = os.path.join(DATA, "fronts.json")
    with open(p, "w") as f:
        json.dump(map_content.content(), f, separators=(",", ":"))
    print("fronts.json", os.path.getsize(p) // 1024, "KB")


_CONTENT = {}


def content():
    if not _CONTENT:
        with open(os.path.join(DATA, "fronts.json")) as f:
            _CONTENT.update(json.load(f))
    return _CONTENT


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


def _ctx():
    return cairo.Context(cairo.ImageSurface(cairo.FORMAT_A8, 1, 1))


def _path(rings, closed=True):
    """A cairo path (in map pixels) from flat int rings, built once."""
    c = _ctx()
    for r in rings:
        c.move_to(r[0] / Q, r[1] / Q)
        for i in range(2, len(r), 2):
            c.line_to(r[i] / Q, r[i + 1] / Q)
        if closed:
            c.close_path()
    return c.copy_path()


def _poly_path(polys):
    c = _ctx()
    for poly in polys:
        for i, p in enumerate(poly):
            (c.move_to if i == 0 else c.line_to)(*p)
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
    """The polyline's first `length` (in its own units)."""
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


def _tint(side, k=0.42):
    """An occupied land's base: the side ink mixed into the paper-land colour (the dots then carry the full ink)."""
    a, b = col(side), col("land")
    return tuple(lerp(b[i], a[i], k) for i in range(3)) + (1.0,)


class Map:
    """One map view. Set it up once (sides, owners, arrows, fronts, cities, labels, camera keys), then call
    draw(cr, t) every frame. All times are seconds in the scene; places are (lon, lat)."""

    def __init__(self, view="europe", era=None, sides=None, owners=None, occupied=None, compass=True, grid=True,
                 muted=0.0):
        """era: a preset from map_content.ERAS ("1936", "1939", "1940", "1941" in Europe; "1937", "1941", "1942" in
        the Pacific), overridden per region by sides / owners / occupied. muted (0-1): drain the colour (the Holocaust
        chapter's grey map)."""
        self.name = view
        d = _load(view)
        self.d = d
        self.paths = {k: _path(r) for k, r in d["regions"].items()}
        self.land = _path(d["land"])
        self.lakes = _path(d["lakes"])
        self.bands = [_path(b) for b in d["bands"]]
        self.edges = {k: _path(r, closed=False) for k, r in d["edges"].items()}
        self.bbox = {k: self._bbox(r) for k, r in d["regions"].items()}
        e = content().get("eras", {}).get(view, {}).get(era or DEFAULT_ERA.get(view, ""), {})
        sd, ow, oc = dict(e.get("side", {})), dict(e.get("owner", {})), set(e.get("occupied", []))
        sd.update(sides or {})
        ow.update(owners or {})
        if occupied is not None:
            oc = set(occupied)
        self._side = {k: [(-1e9, sd.get(k, "neutral"), None, 0.0, k in oc)] for k in self.paths}
        self._owner = {k: [(-1e9, ow.get(k, k))] for k in self.paths}
        self.arrows_, self.fronts, self.secrets, self.cities, self.labels, self.stamps = [], [], [], [], [], []
        self.lines, self.zones = [], []
        self.cam = []
        self.compass = compass
        self.muted = muted
        self.grid = self._graticule() if grid else None

    @staticmethod
    def _bbox(rings):
        xs = [r[i] / Q for r in rings for i in range(0, len(r), 2)]
        ys = [r[i] / Q for r in rings for i in range(1, len(r), 2)]
        return min(xs), min(ys), max(xs), max(ys)

    def _graticule(self):
        v = VIEWS[self.name]
        step, (lo0, lo1), (la0, la1) = v["grid"], v["grid_lon"], v["grid_lat"]
        lines = []
        for lon in range(lo0 - lo0 % step, lo1 + 1, step):
            lines.append([self.xy((lon, la0 + (la1 - la0) * i / 60)) for i in range(61)])
        for lat in range(la0 - la0 % step, la1 + 1, step):
            lines.append([self.xy((lo0 + (lo1 - lo0) * i / 120, lat)) for i in range(121)])
        return _poly_path(lines)

    def xy(self, lonlat):
        return project(self.name, *lonlat)

    def regions(self, name):
        return GROUPS.get(name) or content().get("groups", {}).get(self.name, {}).get(name) or [name]

    # ------------------------------------------------------------ setup
    def side(self, name, t, side, origin=None, dur=1.0, occupied=True):
        """From t, `name` (a region or a GROUPS name) turns `side`; with `origin` (lon, lat) the colour floods out
        from there over `dur` seconds instead of switching. occupied: halftone it (newly occupied or annexed land);
        False for land that changes side but stays its own (a country joining a side)."""
        for r in self.regions(name):
            if r in self._side:
                self._side[r].append((t, side, self.xy(origin) if origin else None, dur, occupied))
                self._side[r].sort(key=lambda e: e[0])

    def owner(self, name, t, owner):
        """From t, `name` belongs to `owner`: borders between regions of one owner disappear (an annexation)."""
        for r in self.regions(name):
            if r in self._owner:
                self._owner[r].append((t, owner))
                self._owner[r].sort(key=lambda e: e[0])

    def arrow(self, lonlats, side, t0, t1, width=70.0, hold=None):
        """A fat poster arrow along a smooth path through `lonlats`, growing from t0 to t1: side colour, ink outline,
        a hard drop shadow. width is in screen pixels across the head; `hold` ends it (fades) at that time."""
        self.arrows_.append(dict(pts=_catmull([self.xy(p) for p in lonlats]), side=side, t0=t0, t1=t1, w=width,
                                 hold=hold))

    def front(self, keys, t0=None, t1=None, width=7.0, side=None, t_in=None, t_out=None):
        """A front line moving between keyframed polylines. keys: a name from fronts.json ("barbarossa", "bulge",
        ...; its keyframes span t0 -> t1), or [(t, [(lon, lat), ...]), ...] in scene seconds."""
        if isinstance(keys, str):
            f = content()["fronts"][keys]
            side = side or None
            keys = [(t0 + (t1 - t0) * u, [tuple(p) for p in pts]) for u, pts in f["keys"]]
        self.fronts.append(dict(keys=[(t, _resample(_catmull([self.xy(p) for p in pts], 6), 64)) for t, pts in keys],
                                w=width, side=side, t_in=t_in if t_in is not None else keys[0][0], t_out=t_out))

    def arrows(self, name, t0, t1, stagger=0.25, hold=None, width=None, side=None):
        """A named arrow set from fronts.json ("barbarossa", "sickle_1940", "island_hop", ...), each growing over
        t1 - t0 seconds, started `stagger` apart."""
        a = content()["arrows"][name]
        for i, path in enumerate(a["paths"]):
            self.arrow([tuple(p) for p in path], side or a["side"], t0 + i * stagger, t1 + i * stagger,
                       width or a.get("width") or 70.0, hold)

    def line(self, name, t0, t1=None, t_out=None):
        """A named line from fronts.json, drawn along from t0 to t1 (or faded in at t0): "maginot"/"gustav" (a fort
        chain that glows as it lands), "iron_curtain", the rail lines ("rail_paris", ... or the group
        "rails_holocaust"), "secret_1939" (dashed)."""
        c = content()
        for n in c.get("line_groups", {}).get(name, [name]):
            ln = c["lines"][n]
            self.lines.append(dict(pts=_catmull([self.xy(tuple(p)) for p in ln["pts"]], 8), style=ln["style"], t0=t0,
                                   t1=t1 if t1 is not None else t0 + 0.4, t_out=t_out))

    def zone(self, name, t0, t1=None, t_out=None, side=None):
        """A named zone from fronts.json: pockets (Dunkirk), hatched areas (the Battle of Britain), occupied bands
        (ussr_occupied_1941/1942) and rings that close between t0 and t1 (Stalingrad, Berlin)."""
        zn = content()["zones"][name]
        if zn["kind"] == "ring":
            (lon, lat), km = zn["geom"]
            c = self.xy((lon, lat))
            s = W / (VIEWS[self.name]["width_km"] * 1000.0) * 1000.0 * km
            geom = (c, s)
        else:
            geom = [self.xy(tuple(p)) for p in zn["geom"]]
        self.zones.append(dict(kind=zn["kind"], side=side or zn["side"], geom=geom, t0=t0,
                               t1=t1 if t1 is not None else t0 + 0.6, t_out=t_out,
                               path=None if zn["kind"] == "ring" else _poly_path([geom + [geom[0]]])))

    def pins(self, name, t0, stagger=0.3, t_out=None, **kw):
        """A named pin set (the five Normandy beaches, the island hops, the camps): dots with labels, in turn."""
        for i, pin in enumerate(content()["pins"][name]["pins"]):
            lab, lon, lat = pin[:3]
            off = dict(dx=pin[3], dy=pin[4]) if len(pin) >= 5 else {}
            self.city(lab, t0 + i * stagger, t_out=t_out, lonlat=(lon, lat), **{**off, **kw})

    def view(self, name, t, zoom=None):
        """A camera key at a named preset ("stalingrad", "normandy", "midway", ...)."""
        v = content()["views"][name]
        self.camera_key(t, tuple(v["at"]), zoom or v["zoom"])

    def secret_line(self, lonlats, t0, t1, color="alert", width=6.0, t_out=None):
        """A dashed line drawn along `lonlats` from t0 to t1 (the secret protocol), gone at t_out."""
        self.secrets.append(dict(pts=_catmull([self.xy(p) for p in lonlats], 6), t0=t0, t1=t1, color=color, w=width,
                                 t_out=t_out))

    def stamp(self, word, lonlat, t0, t_out=None, size=78, color="alert", tilt=-0.12):
        """A rubber-stamp word ("SECRET", stencil) that slams down at lonlat at t0."""
        self.stamps.append(dict(word=word, at=self.xy(lonlat), t0=t0, t_out=t_out, size=size, color=color, tilt=tilt))

    def city(self, name, t0, t_out=None, lonlat=None, label=True, pulse=True, dx=16, dy=-14, size=34):
        """A city dot (with its name, Oswald) from t0; it pulses for a second when it appears."""
        self.cities.append(dict(name=name, at=self.xy(lonlat or CITIES[name]), t0=t0, t_out=t_out, label=label,
                                pulse=pulse, dx=dx, dy=dy, size=size))

    def label(self, s, t0, t_out=None, lonlat=None, region=None, size=48, color="ink", tilt=0.0, spacing=None,
              font=None):
        """A map label at lonlat (or a region's label point), fading in at t0: stencil for the big ones (size >= 40),
        Oswald below."""
        at = self.xy(lonlat) if lonlat else tuple(self.d["labels"][region])
        font = font or (STENCIL if size >= 40 else LABEL)
        sp = spacing if spacing is not None else (size * 0.12 if font == STENCIL else size * 0.06)
        self.labels.append(dict(s=s, at=at, t0=t0, t_out=t_out, size=size, color=color, tilt=tilt, sp=sp, font=font))

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
        """(state before, state now, flood origin, flood progress 0-1); a state is (side, occupied)."""
        hist = self._side[r]
        prev, cur = hist[0], hist[0]
        for e in hist[1:]:
            if t >= e[0]:
                prev, cur = cur, e
        if cur[2] is None or cur[3] <= 0:
            return (cur[1], cur[4]), (cur[1], cur[4]), None, 1.0
        return (prev[1], prev[4]), (cur[1], cur[4]), cur[2], clamp01((t - cur[0]) / cur[3])

    # ------------------------------------------------------------ draw
    def draw(self, cr, t):
        (cx, cy), z = self.camera_at(t)
        self._z, self._c, self._t = z, (cx, cy), t
        cr.save()
        cr.set_source_rgba(*col("sea", 0.94))                       # the printed sea (paper grain shows a little)
        cr.paint()
        cr.translate(W / 2, H / 2)
        cr.scale(z, z)
        cr.translate(-cx, -cy)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)
        self._hatch(cr)
        cr.new_path()
        cr.append_path(self.land)                                    # neutral land (aged paper) under everything
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.set_source_rgba(*col("land"))
        cr.fill()
        for r, p in self.paths.items():
            self._fill_region(cr, r, p, t, z)
        cr.new_path()                                                # lakes
        cr.append_path(self.lakes)
        cr.set_source_rgba(*col("sea"))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink", 0.8))
        cr.set_line_width(1.2 / z)
        cr.stroke()
        if self.grid is not None:                                    # the lat/long grid, printed faint over all
            cr.new_path()
            cr.append_path(self.grid)
            cr.set_source_rgba(*col("ink_soft", 0.22))
            cr.set_line_width(1.1 / z)
            cr.stroke()
        cr.set_line_width(1.8 / z)                                   # dashed borders, only between different owners
        cr.set_source_rgba(*col("ink", 0.8))
        cr.set_dash([9 / z, 5 / z])
        for k, p in self.edges.items():
            a, b = k.split("|")
            if self._owner_at(a, t) != self._owner_at(b, t):
                cr.new_path()
                cr.append_path(p)
                cr.stroke()
        cr.set_dash([])
        cr.new_path()                                                # coastline
        cr.append_path(self.land)
        cr.set_source_rgba(*col("ink"))
        cr.set_line_width(2.6 / z)
        cr.stroke()
        for zn in self.zones:                                        # zones under the fronts and arrows
            self._draw_zone(cr, zn, t, z)
        for f in self.fronts:
            self._draw_front(cr, f, t, z)
        for s in self.secrets:
            self._draw_secret(cr, s, t, z)
        for ln in self.lines:
            self._draw_line(cr, ln, t, z)
        for a in self.arrows_:
            self._draw_arrow(cr, a, t, z)
        cr.restore()
        for lb in self.labels:                                       # screen-space type: crisp at any zoom
            self._draw_label(cr, lb, t)
        for c in self.cities:
            self._draw_city(cr, c, t)
        for s in self.stamps:
            self._draw_stamp(cr, s, t)
        if self.compass:
            self._draw_compass(cr, t)
        if self.muted > 0:                                           # drain the colour (HOLO chapter)
            cr.save()
            cr.set_operator(cairo.OPERATOR_HSL_SATURATION)
            cr.set_source_rgba(0.5, 0.5, 0.5, self.muted)
            cr.paint()
            cr.restore()

    def screen(self, p):
        """Map pixels -> screen pixels with the camera of the last draw()."""
        (cx, cy), z = self._c, self._z
        return (p[0] - cx) * z + W / 2, (p[1] - cy) * z + H / 2

    def _hatch(self, cr):
        """Fine parallel hatching on the sea along the coasts: sparse out to the outer band, doubled near the shore.
        The lines are spaced in screen pixels (a print screen), so they stay fine at any zoom."""
        for i, band in enumerate(self.bands[::-1]):                  # outer band first
            cr.save()
            cr.new_path()
            cr.append_path(band)
            cr.append_path(self.land)
            cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)               # band XOR land = the sea margin
            cr.clip()
            cr.identity_matrix()
            gap, off = 12.0, 6.0 * i
            cr.set_source_rgba(*col("sea_dk", 0.9))
            cr.set_line_width(1.25)
            k = -H + off
            while k < W:
                cr.move_to(k, H)
                cr.line_to(k + H * 0.6, 0)
                k += gap
            cr.stroke()
            cr.restore()

    def _halftone_here(self, cr, side):
        """Halftone dots in the side ink over the current clip, at a fixed print-screen size on screen."""
        cr.save()
        cr.identity_matrix()
        cr.set_source_rgba(*col(side))
        cr.mask(_dot_tile(3, 11))
        cr.restore()

    def _paint_state(self, cr, state, z):
        """Fill the current path (preserved) in a region state: home land solid, occupied land tinted + halftoned."""
        side, occ = state
        if occ and side != "neutral":
            cr.set_source_rgba(*_tint(side))
            cr.fill_preserve()
            cr.save()
            cr.clip_preserve()
            self._halftone_here(cr, side)
            cr.restore()
        else:
            cr.set_source_rgba(*col(side))
            cr.fill_preserve()

    def _fill_region(self, cr, r, p, t, z):
        before, now, origin, u = self._side_at(r, t)
        cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.new_path()
        cr.append_path(p)
        state = before if u < 1 else now
        self._paint_state(cr, state, z)
        cr.set_source_rgba(*(_tint(state[0]) if state[1] and state[0] != "neutral" else col(state[0])))
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
        self._paint_state(cr, now, z)
        cr.set_source_rgba(*col("ink", 0.55))
        cr.set_line_width(2.6 / z)
        cr.stroke()
        cr.restore()

    def _arrow_poly(self, a, t, z):
        u = ease_out(seg(t, a["t0"], a["t1"]))
        if u <= 0:
            return None
        L = _length(a["pts"])
        body = _cut(a["pts"], L * u)
        if len(body) < 2:
            return None
        w = a["w"] / z
        head_len = min(0.95 * w, _length(body) * 0.6)
        shaft = _cut(body, max(0.0, _length(body) - head_len))
        tip, base = body[-1], shaft[-1]
        left, right = [], []
        n = len(shaft)
        for i, p in enumerate(shaft):                                # a fat shaft, a little wider toward the head
            q = shaft[min(i + 1, n - 1)] if i < n - 1 else tip
            o = shaft[max(i - 1, 0)] if i > 0 else p
            dx, dy = q[0] - o[0], q[1] - o[1]
            d = math.hypot(dx, dy) or 1.0
            hw = w * lerp(0.2, 0.27, i / max(1, n - 1))
            left.append((p[0] - dy / d * hw, p[1] + dx / d * hw))
            right.append((p[0] + dy / d * hw, p[1] - dx / d * hw))
        dx, dy = tip[0] - base[0], tip[1] - base[1]
        d = math.hypot(dx, dy) or 1.0
        nx, ny = -dy / d, dx / d
        hw = w * 0.5
        return left + [(base[0] + nx * hw, base[1] + ny * hw), tip, (base[0] - nx * hw, base[1] - ny * hw)] + right[::-1]

    def _draw_arrow(self, cr, a, t, z):
        poly = self._arrow_poly(a, t, z)
        if not poly:
            return
        fade = 1.0 - (ease_in(seg(t, a["hold"], a["hold"] + 0.4)) if a["hold"] is not None else 0.0)
        if fade <= 0:
            return

        def trace(dx=0.0, dy=0.0):
            cr.new_path()
            for i, p in enumerate(poly):
                (cr.move_to if i == 0 else cr.line_to)(p[0] + dx, p[1] + dy)
            cr.close_path()

        trace(7 / z, 8 / z)                                          # the hard poster shadow
        cr.set_source_rgba(*col("ink", 0.55 * fade))
        cr.fill()
        trace()
        cr.set_source_rgba(*col("cream", 0.9 * fade))                # a cream rim, so grey arrows read on grey land
        cr.set_line_width(10 / z)
        cr.stroke_preserve()
        cr.set_source_rgba(*col(a["side"], fade))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink", fade))
        cr.set_line_width(4.0 / z)
        cr.stroke()

    def _draw_line(self, cr, ln, t, z):
        u = smooth(seg(t, ln["t0"], ln["t1"]))
        if u <= 0 or (ln["t_out"] is not None and t > ln["t_out"] + 0.4):
            return
        a = 1 - (ease_in(seg(t, ln["t_out"], ln["t_out"] + 0.4)) if ln["t_out"] is not None else 0)
        pts = _cut(ln["pts"], _length(ln["pts"]) * u)
        if len(pts) < 2:
            return

        def trace():
            cr.new_path()
            for i, p in enumerate(pts):
                (cr.move_to if i == 0 else cr.line_to)(*p)

        st = ln["style"]
        if st == "forts":                                            # a fort chain: glow, cream rim, ink, blocks
            glow = 1 - seg(t, ln["t1"], ln["t1"] + 1.2)
            if glow > 0:
                trace()
                cr.set_source_rgba(*col("fire", 0.45 * glow * a))
                cr.set_line_width(30 / z)
                cr.stroke()
            trace()
            cr.set_source_rgba(*col("cream", 0.9 * a))
            cr.set_line_width(13 / z)
            cr.stroke()
            trace()
            cr.set_source_rgba(*col("ink", a))
            cr.set_line_width(6 / z)
            cr.stroke()
            L = _length(pts)
            step = 26 / z
            k = step / 2
            while k < L:                                             # square fort blocks along it
                p = _cut(pts, k)[-1]
                h = 6.5 / z
                cr.rectangle(p[0] - h, p[1] - h, 2 * h, 2 * h)
                cr.set_source_rgba(*col("ink", a))
                cr.fill_preserve()
                cr.set_source_rgba(*col("cream", a))
                cr.set_line_width(2 / z)
                cr.stroke()
                k += step
        elif st == "rail":                                           # rails: cross ties, then the line
            trace()
            cr.set_source_rgba(*col("ink", 0.85 * a))
            cr.set_line_width(10 / z)
            cr.set_dash([2.5 / z, 9 / z])
            cr.set_line_cap(cairo.LINE_CAP_BUTT)
            cr.stroke()
            cr.set_dash([])
            cr.set_line_cap(cairo.LINE_CAP_ROUND)
            trace()
            cr.set_line_width(2.6 / z)
            cr.stroke()
        elif st == "curtain":                                        # the Iron Curtain: a heavy black dash
            trace()
            cr.set_source_rgba(*col("cream", 0.9 * a))
            cr.set_line_width(14 / z)
            cr.stroke()
            trace()
            cr.set_source_rgba(*col("ink", a))
            cr.set_line_width(9 / z)
            cr.set_dash([22 / z, 8 / z])
            cr.stroke()
            cr.set_dash([])
        else:                                                        # dash (the secret line style)
            trace()
            cr.set_dash([18 / z, 11 / z])
            cr.set_source_rgba(*col("cream", 0.9 * a))
            cr.set_line_width(11 / z)
            cr.stroke_preserve()
            cr.set_source_rgba(*col("alert", a))
            cr.set_line_width(6 / z)
            cr.stroke()
            cr.set_dash([])

    def _draw_zone(self, cr, zn, t, z):
        if t < zn["t0"] or (zn["t_out"] is not None and t > zn["t_out"] + 0.4):
            return
        u = ease_out(seg(t, zn["t0"], zn["t1"]))
        a = 1 - (ease_in(seg(t, zn["t_out"], zn["t_out"] + 0.4)) if zn["t_out"] is not None else 0)
        kind = zn["kind"]
        if kind == "ring":                                           # two arcs close the ring from the east
            (cx, cy), r = zn["geom"]
            sweep = math.pi * u
            for lw, c in ((16 / z, "cream"), (10 / z, zn["side"])):
                cr.new_path()
                cr.arc(cx, cy, r, -sweep, sweep)
                cr.set_source_rgba(*col(c, a))
                cr.set_line_width(lw)
                cr.stroke()
            cr.new_path()
            cr.arc(cx, cy, r + 5 / z, -sweep, sweep)
            cr.arc_negative(cx, cy, r - 5 / z, sweep, -sweep)
            cr.close_path()
            cr.set_source_rgba(*col("ink", a))
            cr.set_line_width(2.5 / z)
            cr.stroke()
            return
        cr.save()
        cr.new_path()
        cr.append_path(zn["path"])
        if kind == "occupied":                                       # only on land
            cr.clip()
            cr.new_path()
            cr.append_path(self.land)
            cr.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        cr.clip()
        cr.paint_with_alpha(0)                                       # (keeps the clip; nothing drawn)
        cr.push_group()
        if kind in ("pocket", "occupied"):
            cr.set_source_rgba(*_tint(zn["side"]))
            cr.paint()
            self._halftone_here(cr, zn["side"])
        else:                                                        # area: hatched in its colour
            cr.identity_matrix()
            cr.set_source_rgba(*col(zn["side"], 0.75))
            cr.set_line_width(3.0)
            k = -H
            while k < W:
                cr.move_to(k, H)
                cr.line_to(k + H * 0.6, 0)
                k += 16
            cr.stroke()
        cr.pop_group_to_source()
        cr.paint_with_alpha(u * a * (0.9 if kind != "area" else 1.0))
        cr.restore()
        if kind != "occupied":                                       # a dashed edge
            cr.new_path()
            cr.append_path(zn["path"])
            cr.set_dash([10 / z, 6 / z])
            cr.set_source_rgba(*col("ink", u * a))
            cr.set_line_width(3 / z)
            cr.stroke()
            cr.set_dash([])

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
        for lw, c, alpha in ((f["w"] + 5, "cream", 0.85), (f["w"], f["side"] or "ink", 1.0)):
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
        cr.set_dash([18 / z, 11 / z])
        cr.set_source_rgba(*col("cream", 0.9 * a))
        cr.set_line_width((s["w"] + 5) / z)
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
        text(cr, lb["s"], 0, lb["size"] * 0.36, lb["size"], font=lb["font"], color=lb["color"], alpha=a,
             outline="cream", outline_w=lb["size"] * 0.17, spacing=lb["sp"])
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
                    cr.set_source_rgba(*col("alert", 0.85 * (1 - v) * a))
                    cr.set_line_width(3.5)
                    cr.stroke()
        cr.new_path()
        cr.arc(x, y, 9 * pop, 0, 2 * math.pi)
        cr.set_source_rgba(*col("cream", a))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink", a))
        cr.set_line_width(3.5)
        cr.stroke()
        cr.arc(x, y, 4 * pop, 0, 2 * math.pi)
        cr.fill()
        if c["label"]:
            la = a * ease_out(seg(t, c["t0"] + 0.1, c["t0"] + 0.45))
            text(cr, c["name"].upper(), x + c["dx"], y + c["dy"], c["size"], font=LABEL, color="ink", align="left",
                 alpha=la, outline="cream", outline_w=c["size"] * 0.2, spacing=c["size"] * 0.05)

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
        cr.select_font_face(STENCIL, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
        cr.set_font_size(size)
        sp = size * 0.1
        wd = cr.text_extents(s["word"]).x_advance + sp * (len(s["word"]) - 1)
        for inset, lw in ((0, 6.0), (11, 2.5)):                      # a double stamp border
            cr.rectangle(-wd / 2 - 26 + inset, -size * 0.78 + inset, wd + 52 - 2 * inset, size * 1.22 - 2 * inset)
            cr.set_source_rgba(*col(s["color"], 0.9 * a))
            cr.set_line_width(lw)
            cr.stroke()
        text(cr, s["word"], 0, size * 0.36, size, font=STENCIL, color=s["color"], alpha=0.9 * a, spacing=sp)
        cr.restore()

    def _draw_compass(self, cr, t, x=W - 112, y=H - 118, r=56):
        """A small printed compass rose: an eight-point star, ink and cream halves, a stencil N."""
        cr.save()
        cr.translate(x, y)
        cr.new_path()
        cr.arc(0, 0, r * 0.78, 0, 2 * math.pi)
        cr.set_source_rgba(*col("cream", 0.85))
        cr.fill_preserve()
        cr.set_source_rgba(*col("ink", 0.9))
        cr.set_line_width(2.0)
        cr.stroke()
        for k, ln, wd in ((1, r * 0.62, 0.16), (0, r, 0.2)):         # diagonals behind the cardinal points
            for q in range(4):
                a = q * math.pi / 2 + (math.pi / 4 if k else 0)
                ca, sa = math.cos(a), math.sin(a)
                for half in (0, 1):                                  # each point: a dark half and a light half
                    cr.new_path()
                    cr.move_to(0, 0)
                    cr.line_to(ca * ln, sa * ln)
                    s = 1 if half else -1
                    cr.line_to(-sa * s * ln * wd, ca * s * ln * wd)
                    cr.close_path()
                    cr.set_source_rgba(*col("ink" if half else "cream"))
                    cr.fill_preserve()
                    cr.set_source_rgba(*col("ink"))
                    cr.set_line_width(1.6)
                    cr.stroke()
        text(cr, "N", 0, -r - 8, 30, font=STENCIL, color="ink", outline="cream", outline_w=6)
        cr.restore()


if __name__ == "__main__" and sys.argv[1:2] == ["build"]:
    build_data(tuple(sys.argv[2:]) or ("europe", "pacific", "world"))
    build_content()
elif __name__ == "__main__" and sys.argv[1:2] == ["content"]:
    build_content()
