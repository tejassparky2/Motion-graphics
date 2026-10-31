"""WW2 map content for every package (SHOTLIST.md): named fronts with lon/lat keyframes, arrow sets, fortified and
rail lines, zones (pockets, hatched areas, occupied bands, closing rings), pin sets, camera presets and flood groups,
plus era presets (sides, owners, occupied land) per view. All lines are hand-traced at map scale from standard
campaign maps: close, not survey-exact. `python -m channels.ww2.kit.maps content` writes channels/ww2/data/fronts.json
from this file; animators call them by name:

    m = Map("europe", era="1941")
    m.view("east_front", 0)                  # a camera preset
    m.front("barbarossa", 1.0, 6.0)          # the front moves Jun -> Dec 1941 between t=1 and t=6
    m.arrows("barbarossa", 0.5, 3.0)         # its three arrows, staggered
    m.zone("stalingrad_ring", 2.0, 4.0)      # the ring closes
    m.line("maginot", 0.5, 2.5)              # the fort chain draws along the border
    m.pins("normandy_beaches", 1.0)          # five named beaches pop in turn
"""
from channels.ww2.kit.maps import SPLIT_1939

# ---------------------------------------------------------------- fronts (lon, lat), north to south / west to east
START_1941 = [(21.1, 55.75), (22.1, 55.3), (22.9, 54.4), (23.5, 54.05), (22.6, 53.75), (21.95, 53.3), (21.9, 52.95),
              (22.05, 52.7), (22.6, 52.45), (23.2, 52.25), (23.65, 52.08), (23.6, 51.55), (23.75, 51.1),
              (24.05, 50.75), (24.2, 50.45), (23.4, 50.25), (22.75, 50.05), (22.8, 49.8), (22.4, 49.55),
              (22.65, 49.08), (23.7, 48.75), (24.6, 48.0), (25.3, 47.85), (26.2, 47.95), (26.65, 48.2),
              (27.25, 47.6), (28.1, 46.65), (28.2, 45.5), (29.6, 45.25)]          # 22 June 1941, Baltic to Black Sea
DEC_1941 = [(30.8, 59.9), (31.6, 58.8), (33.0, 57.6), (35.9, 56.8), (37.2, 56.2), (36.4, 55.4), (37.3, 54.2),
            (36.3, 53.0), (36.6, 51.6), (37.4, 50.0), (38.4, 48.6), (39.4, 47.25)]     # at the gates of Moscow
JAN_1942 = [(30.8, 59.9), (31.6, 58.8), (32.4, 57.4), (33.8, 56.3), (34.8, 55.6), (34.9, 54.9), (35.6, 54.0),
            (36.1, 53.0), (36.6, 51.6), (37.4, 50.0), (38.4, 48.6), (39.0, 47.2)]       # pushed back from Moscow
NOV_1942 = [(30.8, 59.9), (31.6, 58.8), (32.4, 57.4), (33.8, 56.3), (34.8, 55.6), (34.9, 54.9), (35.6, 54.0),
            (36.1, 53.0), (37.5, 52.4), (39.2, 51.7), (40.3, 50.4), (41.5, 49.6), (43.2, 49.3), (44.5, 48.75),
            (44.6, 47.5), (44.0, 46.0), (44.2, 43.6), (41.0, 43.6), (38.0, 44.6)]       # the high-water mark
KURSK_JUL_1943 = [(35.2, 53.6), (36.4, 53.2), (36.6, 52.6), (35.9, 52.35), (35.2, 52.3), (34.6, 52.1), (34.4, 51.6),
                  (34.7, 51.1), (35.4, 50.9), (36.1, 50.75), (36.7, 50.6), (37.3, 50.2)]   # the salient
KURSK_AUG_1943 = [(33.8, 53.8), (34.4, 53.2), (34.8, 52.6), (34.9, 52.0), (34.9, 51.4), (35.3, 50.9), (35.9, 50.2),
                  (36.4, 49.7), (37.4, 49.2)]                                               # Orel, Kharkov retaken
BAGRATION_JUN = [(28.2, 59.4), (28.5, 58.0), (29.5, 56.4), (30.1, 55.6), (30.3, 54.9), (30.4, 54.3), (30.3, 53.8),
                 (29.9, 52.9), (29.2, 52.1), (27.0, 51.75), (25.0, 51.3), (24.9, 50.3), (25.3, 49.5), (25.6, 48.5),
                 (27.2, 47.6), (28.5, 47.1), (29.5, 46.5)]                                 # 22 June 1944
BAGRATION_AUG = [(28.2, 59.4), (27.2, 57.8), (25.4, 56.8), (23.8, 55.8), (22.9, 54.5), (22.0, 53.4), (21.1, 52.2),
                 (21.5, 51.6), (21.7, 50.6), (22.4, 49.9), (23.6, 49.2), (24.6, 48.5), (26.2, 47.7), (27.2, 47.3),
                 (28.8, 46.8), (29.6, 46.4)]                                               # on the Vistula
BULGE_0 = [(6.0, 51.4), (6.2, 50.9), (6.3, 50.55), (6.35, 50.3), (6.15, 50.05), (6.15, 49.85), (6.45, 49.5),
           (7.0, 49.25), (7.6, 49.1)]                                                      # 16 Dec 1944
BULGE_1 = [(6.0, 51.4), (6.2, 50.9), (6.1, 50.55), (5.6, 50.4), (5.1, 50.3), (4.95, 50.2), (5.3, 50.05), (5.6, 49.95),
           (5.75, 49.85), (6.15, 49.8), (6.45, 49.5), (7.0, 49.25), (7.6, 49.1)]          # 25 Dec, near the Meuse
ALAMEIN = [(28.9, 30.95), (28.85, 30.6), (28.9, 30.2), (28.95, 29.85)]                     # sea to the Qattara
CHINA_1938 = [(110.5, 41.0), (111.0, 37.5), (110.5, 35.0), (112.0, 34.0), (114.0, 32.3), (114.5, 30.6), (113.0, 29.6),
              (113.5, 28.0), (114.0, 25.5), (113.5, 23.6), (112.5, 21.6)]
CHINA_1944 = [(110.5, 41.0), (111.0, 37.5), (110.5, 35.0), (112.0, 34.0), (112.4, 32.0), (111.5, 30.7), (112.0, 29.2),
              (111.0, 27.0), (110.0, 25.3), (108.5, 24.0), (108.0, 22.0)]                 # after Ichi-Go
JAPAN_1942_PERIMETER = [(173.0, 53.0), (166.6, 19.3), (171.2, 7.1), (173.0, 1.4), (160.0, -9.4), (147.2, -9.4),
                        (125.5, -9.8), (110.0, -8.5), (95.3, 5.5), (92.5, 20.5), (94.6, 25.0)]

FRONTS = {
    "barbarossa": dict(view="europe", side="germany", keys=[(0, START_1941), (1, DEC_1941)]),
    "moscow_1941": dict(view="europe", side="germany", keys=[(0, DEC_1941), (1, JAN_1942)]),
    "case_blue_1942": dict(view="europe", side="germany", keys=[(0, JAN_1942), (1, NOV_1942)]),
    "kursk_1943": dict(view="europe", side="germany", keys=[(0, KURSK_JUL_1943), (1, KURSK_AUG_1943)]),
    "bagration": dict(view="europe", side="germany", keys=[(0, BAGRATION_JUN), (1, BAGRATION_AUG)]),
    "bulge": dict(view="europe", side="germany", keys=[(0, BULGE_0), (1, BULGE_1)]),
    "bulge_collapse": dict(view="europe", side="germany", keys=[(0, BULGE_1), (1, BULGE_0)]),
    "alamein": dict(view="europe", side="germany", keys=[(0, ALAMEIN), (1, ALAMEIN)]),
    "china": dict(view="pacific", side="japan", keys=[(0, CHINA_1938), (1, CHINA_1944)]),
    "japan_1942_perimeter": dict(view="pacific", side="japan", keys=[(0, JAPAN_1942_PERIMETER),
                                                                     (1, JAPAN_1942_PERIMETER)]),
}

# ---------------------------------------------------------------- arrow sets: (side, [paths][, width]); lon, lat
ARROW_WIDTH = {"normandy_1944": 40, "island_hop": 56, "atomic_1945": 50, "berlin_1945": 54, "stalingrad_uranus": 56,
               "kursk_1943": 56, "kursk_counter": 56, "bulge_1944": 56, "patton_bastogne": 50}
ARROWS = {
    # Europe 1935-40
    "italy_ethiopia_1935": ("italy", [[(13.0, 41.0), (22.0, 34.5), (32.4, 29.9), (37.5, 19.5), (38.75, 9.03)]]),
    "ethiopia_1935": ("italy", [[(39.0, 15.5), (39.4, 12.2), (38.75, 9.03)], [(45.3, 2.0), (42.6, 6.0), (39.4, 8.7)]]),
    "poland_1939": ("germany", [[(14.9, 53.3), (17.0, 53.0), (19.4, 52.6)], [(20.6, 54.0), (20.9, 53.3), (21.0, 52.5)],
                                [(17.6, 50.6), (19.0, 50.6), (20.6, 51.3)]]),
    "soviet_poland_1939": ("soviet", [[(31.0, 53.9), (28.3, 53.3), (25.0, 52.85)],
                                      [(31.0, 50.2), (28.0, 49.95), (24.9, 49.85)]]),
    "denmark_1940": ("germany", [[(9.4, 54.8), (9.6, 55.8), (10.0, 56.6)], [(11.0, 54.3), (11.9, 55.0), (12.55, 55.67)]]),
    "norway_1940": ("germany", [[(10.0, 55.5), (10.6, 57.6), (10.7, 59.6)], [(8.5, 56.0), (5.5, 58.8), (5.3, 60.4)],
                                [(9.0, 57.2), (12.0, 64.0), (17.4, 68.4)]]),
    "west_1940": ("germany", [[(7.2, 52.3), (6.2, 52.2), (5.0, 52.1)], [(6.4, 50.85), (5.6, 50.85), (4.4, 50.85)],
                              [(6.9, 49.8), (6.4, 49.7), (6.0, 49.6)], [(7.0, 50.1), (5.9, 49.9), (4.95, 49.7)]]),
    "sickle_1940": ("germany", [[(6.6, 50.3), (5.3, 49.85), (4.4, 49.75), (3.2, 49.95), (1.85, 50.15)]]),
    "sealion_1940": ("germany", [[(1.6, 50.7), (1.1, 50.9), (0.7, 51.0)]]),
    "blitz_1940": ("germany", [[(2.4, 49.9), (1.4, 50.7), (-0.1, 51.45)], [(3.2, 50.9), (1.6, 51.3), (0.1, 51.5)]]),
    # the East
    "barbarossa": ("germany", [[(21.6, 55.0), (25.5, 56.8), (28.5, 58.3), (30.0, 59.6)],
                               [(23.5, 52.6), (27.8, 53.9), (32.5, 54.8), (36.8, 55.7)],
                               [(24.0, 50.4), (27.5, 50.4), (30.5, 50.3), (35.5, 48.5)]]),
    "moscow_counter": ("soviet", [[(39.5, 56.6), (37.8, 56.3), (36.3, 56.1)], [(38.6, 55.6), (37.5, 55.5), (35.8, 55.3)],
                                  [(38.6, 54.2), (37.3, 54.3), (35.8, 54.1)]]),
    "case_blue_1942": ("germany", [[(37.0, 51.2), (38.8, 51.6), (39.3, 51.7)], [(37.2, 49.5), (40.8, 49.0), (44.3, 48.75)],
                                   [(38.5, 47.3), (40.5, 46.0), (43.5, 44.0)]]),
    "stalingrad_uranus": ("soviet", [[(42.0, 49.9), (42.7, 49.3), (43.5, 48.75)],
                                     [(45.3, 48.2), (44.6, 48.15), (43.6, 48.65)]]),
    "kursk_1943": ("germany", [[(36.1, 53.1), (36.2, 52.6), (36.2, 52.2)], [(36.6, 50.5), (36.5, 50.9), (36.4, 51.25)]]),
    "kursk_counter": ("soviet", [[(37.5, 52.8), (36.6, 52.95), (35.6, 53.1)], [(37.0, 50.6), (36.4, 50.25), (35.9, 49.9)]]),
    "reverse_1943": ("germany", [[(37.0, 52.0), (33.5, 52.5), (30.5, 52.6)], [(38.0, 49.5), (34.0, 49.0), (30.5, 48.3)]]),
    "bagration": ("soviet", [[(31.5, 54.6), (27.5, 54.4), (24.0, 54.0), (22.6, 53.6)],
                             [(30.4, 52.6), (27.0, 52.5), (23.8, 52.4), (21.7, 52.25)]]),
    # Africa and Italy
    "rommel_1942": ("germany", [[(20.1, 32.1), (23.9, 32.0), (28.6, 30.9)]]),
    "el_alamein": ("allies", [[(29.3, 30.85), (25.0, 31.6), (20.0, 31.0), (15.6, 31.25), (13.2, 32.85)]]),
    "torch_1942": ("allies", [[(-12.0, 35.5), (-9.5, 34.5), (-7.7, 33.6)], [(-4.5, 36.2), (-2.5, 35.9), (-0.7, 35.75)],
                              [(-2.0, 37.5), (1.2, 37.2), (3.0, 36.8)]]),
    "sicily_1943": ("allies", [[(10.3, 36.9), (12.5, 36.9), (13.9, 37.1)], [(14.5, 35.9), (14.9, 36.4), (15.1, 36.8)]]),
    "salerno_1943": ("allies", [[(14.3, 39.6), (14.6, 40.2), (14.9, 40.55)]]),
    "anzio_1944": ("allies", [[(12.0, 41.0), (12.4, 41.25), (12.62, 41.45)]]),
    # 1944-45 in the West and the end
    "normandy_1944": ("allies", [[(-1.4, 50.6), (-1.4, 49.9), (-1.17, 49.45)], [(-1.1, 50.6), (-0.95, 49.9), (-0.88, 49.4)],
                                 [(-0.8, 50.6), (-0.65, 49.9), (-0.57, 49.37)], [(-0.5, 50.6), (-0.45, 49.9), (-0.41, 49.36)],
                                 [(-0.25, 50.6), (-0.25, 49.9), (-0.28, 49.33)]]),
    "bulge_1944": ("germany", [[(6.5, 50.4), (5.8, 50.35), (5.0, 50.25)]]),
    "patton_bastogne": ("allies", [[(5.7, 49.3), (5.8, 49.7), (5.75, 49.95)]]),
    "west_1945": ("allies", [[(6.8, 51.3), (9.5, 51.8), (11.6, 52.3)], [(8.0, 49.5), (10.5, 50.5), (12.9, 51.5)]]),
    "berlin_1945": ("soviet", [[(14.6, 52.75), (13.9, 52.85), (13.15, 52.65)], [(14.6, 51.85), (13.8, 52.0), (13.0, 52.3)]]),
    # Pacific
    "manchuria_1931": ("japan", [[(121.6, 38.9), (122.8, 40.7), (123.4, 41.8), (125.3, 43.9), (126.6, 45.75)]]),
    "china_1937": ("japan", [[(116.4, 39.9), (115.5, 36.5), (114.3, 34.8)], [(121.5, 31.2), (119.5, 31.8), (118.8, 32.06)],
                             [(118.8, 32.06), (116.0, 31.3), (114.3, 30.6)]]),
    "pearl_harbor": ("japan", [[(147.5, 43.6), (165.0, 40.0), (-175.0, 32.0), (-158.0, 21.5)]]),
    "japan_1941_42": ("japan", [[(121.0, 25.0), (121.0, 18.5), (121.0, 14.6)], [(108.0, 18.0), (104.0, 8.0), (103.8, 1.4)],
                                [(115.0, 8.0), (110.0, 0.0), (106.8, -6.2)], [(147.0, 4.0), (150.0, -2.0), (152.2, -4.2)],
                                [(100.5, 13.75), (98.0, 16.0), (96.2, 16.8)]]),
    "midway_japan": ("japan", [[(141.0, 32.0), (160.0, 31.0), (-178.0, 28.5)]]),
    "midway_usa": ("allies", [[(-158.0, 21.5), (-168.0, 28.0), (-174.0, 31.0)]]),
    "island_hop": ("allies", [[(-158.0, 21.4), (-170.0, 12.0), (173.0, 1.6)], [(173.0, 1.6), (171.0, 6.5), (167.7, 9.2)],
                              [(167.7, 9.2), (157.0, 13.5), (145.8, 15.2)], [(145.8, 15.2), (142.0, 20.0), (141.3, 24.8)],
                              [(141.3, 24.8), (134.5, 26.5), (127.8, 26.3)]]),
    "macarthur": ("allies", [[(147.2, -9.4), (140.7, -2.5), (131.0, 5.0), (125.0, 10.9)]]),
    "burma_1944": ("allies", [[(93.94, 24.8), (95.5, 23.0), (96.1, 21.97)], [(96.1, 21.97), (96.2, 19.0), (96.16, 16.8)]]),
    "manchuria_1945": ("soviet", [[(112.5, 45.5), (118.0, 44.5), (123.4, 41.8)], [(127.5, 50.3), (127.0, 47.8), (126.6, 45.75)],
                                  [(132.0, 44.0), (130.0, 44.5), (126.6, 45.75)]]),
    "atomic_1945": ("allies", [[(145.6, 15.0), (138.5, 27.5), (132.46, 34.39)], [(145.6, 15.0), (136.0, 25.5), (129.87, 32.75)]]),
}

# ---------------------------------------------------------------- lines: (view, style, points)
MAGINOT = [(5.35, 49.5), (6.2, 49.45), (6.7, 49.25), (7.3, 49.15), (7.9, 49.05), (8.2, 48.95), (7.95, 48.6),
           (7.75, 48.3), (7.6, 47.95), (7.55, 47.6)]
GUSTAV = [(13.75, 41.22), (13.83, 41.5), (14.0, 41.7), (14.15, 41.95), (14.45, 42.15), (14.45, 42.35)]
IRON_CURTAIN = [(14.55, 53.43), (10.9, 54.0), (10.75, 53.4), (11.4, 52.9), (10.9, 52.4), (10.6, 51.6), (10.1, 51.0),
                (11.4, 50.5), (12.1, 50.3), (12.6, 49.8), (13.8, 48.75), (15.0, 48.95), (16.9, 48.6), (17.1, 48.0),
                (16.5, 47.5), (16.1, 46.85), (13.8, 45.6)]
AUSCHWITZ = (19.2, 50.03)
LINES = {
    "maginot": ("europe", "forts", MAGINOT),
    "gustav": ("europe", "forts", GUSTAV),
    "iron_curtain": ("europe", "curtain", IRON_CURTAIN),
    "secret_1939": ("europe", "dash", SPLIT_1939),
}
for _name, _city in (("amsterdam", (4.9, 52.37)), ("paris", (2.35, 48.86)), ("berlin", (13.4, 52.52)),
                     ("prague", (14.42, 50.09)), ("vienna", (16.37, 48.21)), ("budapest", (19.04, 47.5)),
                     ("thessaloniki", (22.94, 40.64))):
    LINES["rail_" + _name] = ("europe", "rail", [_city, ((_city[0] + AUSCHWITZ[0]) / 2 + 0.6, (_city[1] + AUSCHWITZ[1]) / 2
                                                         + 0.4), AUSCHWITZ])
LINES["rail_warsaw"] = ("europe", "rail", [(21.01, 52.23), (21.6, 52.5), (22.05, 52.63)])           # to Treblinka
GROUP_LINES = {"rails_holocaust": ["rail_amsterdam", "rail_paris", "rail_berlin", "rail_prague", "rail_vienna",
                                   "rail_budapest", "rail_thessaloniki", "rail_warsaw"]}

# ---------------------------------------------------------------- zones: (view, kind, side, geometry)
#   pocket: polygon filled tinted + halftoned in its side, dashed edge     area: polygon hatched in alert red
#   occupied: polygon (clipped to land) tinted + halftoned                 ring: (centre, radius km) that closes
OCC_1941 = START_1941 + [(30.5, 45.0), (33.0, 44.3), (36.5, 45.3), (38.5, 46.9)] + DEC_1941[::-1] + \
    [(27.0, 59.6), (23.3, 59.3), (21.0, 57.5)]
OCC_1942 = START_1941 + [(30.5, 45.0), (33.0, 44.3), (36.6, 44.6)] + NOV_1942[::-1] + \
    [(27.0, 59.6), (23.3, 59.3), (21.0, 57.5)]
ZONES = {
    "dunkirk_pocket": ("europe", "pocket", "allies", [(1.9, 51.0), (2.55, 51.12), (3.05, 51.18), (3.15, 50.95),
                                                      (2.75, 50.72), (2.2, 50.82)]),
    "battle_of_britain": ("europe", "area", "alert", [(-1.8, 50.7), (1.5, 51.0), (1.6, 51.4), (0.9, 51.8),
                                                      (-0.6, 52.2), (-1.9, 51.6)]),
    "ussr_occupied_1941": ("europe", "occupied", "germany", OCC_1941),
    "ussr_occupied_1942": ("europe", "occupied", "germany", OCC_1942),
    "stalingrad_ring": ("europe", "ring", "soviet", ((43.75, 48.75), 55)),
    "berlin_ring": ("europe", "ring", "soviet", ((13.4, 52.5), 45)),
    "leningrad_siege": ("europe", "ring", "germany", ((30.3, 59.95), 38)),
    "bastogne_ring": ("europe", "ring", "germany", ((5.72, 50.0), 13)),
    "japan_1942": ("pacific", "area", "japan", JAPAN_1942_PERIMETER + [(100.0, 30.0), (130.0, 52.0), (150.0, 55.0)]),
}

# ---------------------------------------------------------------- pin sets: [label, lon, lat]
PINS = {
    "normandy_beaches": ("europe", [["UTAH", -1.17, 49.42, -34, -20], ["OMAHA", -0.88, 49.37, -42, 46],
                                    ["GOLD", -0.57, 49.34, -28, -20], ["JUNO", -0.41, 49.33, -26, 46],
                                    ["SWORD", -0.28, 49.30, -14, -20]]),      # [label, lon, lat, dx, dy]: up / down
    "normandy_airborne": ("europe", [["US AIRBORNE", -1.35, 49.38], ["BRITISH AIRBORNE", -0.22, 49.24]]),
    "camps": ("europe", [["AUSCHWITZ", 19.2, 50.03], ["TREBLINKA", 22.05, 52.63], ["SOBIBOR", 23.64, 51.45],
                         ["BELZEC", 23.46, 50.38], ["MAJDANEK", 22.6, 51.22], ["CHELMNO", 18.73, 52.15]]),
    "ghettos": ("europe", [["WARSAW", 21.01, 52.23], ["LODZ", 19.46, 51.76], ["KRAKOW", 19.94, 50.06],
                           ["LWOW", 24.03, 49.84], ["VILNA", 25.28, 54.69], ["MINSK", 27.56, 53.9]]),
    "island_hop": ("pacific", [["PEARL HARBOR", -157.95, 21.36], ["TARAWA", 172.97, 1.42], ["KWAJALEIN", 167.73, 9.18],
                               ["SAIPAN", 145.75, 15.18], ["IWO JIMA", 141.32, 24.78], ["OKINAWA", 127.8, 26.33]]),
    "pacific_1941": ("pacific", [["PEARL HARBOR", -157.95, 21.36], ["MANILA", 120.98, 14.6], ["HONG KONG", 114.17, 22.32],
                                 ["SINGAPORE", 103.82, 1.35], ["GUAM", 144.79, 13.44], ["WAKE", 166.6, 19.3]]),
    "midway": ("pacific", [["MIDWAY", -177.37, 28.21]]),
    "atomic": ("pacific", [["HIROSHIMA", 132.46, 34.39], ["NAGASAKI", 129.87, 32.75]]),
}

# ---------------------------------------------------------------- camera presets: (view, (lon, lat), zoom)
VIEWS = {
    "normandy_detail": ("normandy", (-0.74, 49.36), 20.0), "omaha": ("normandy", (-0.88, 49.37), 30.0),
    "europe": ("europe", (15.0, 52.0), 1.0), "poland": ("europe", (20.6, 52.1), 2.55),
    "rhineland": ("europe", (7.5, 50.3), 4.0), "central_europe": ("europe", (15.5, 49.5), 2.6),
    "scandinavia": ("europe", (12.0, 61.5), 1.5), "west_1940": ("europe", (4.5, 50.0), 3.0),
    "maginot": ("europe", (6.6, 48.8), 5.5), "ardennes": ("europe", (5.0, 50.0), 4.5),
    "channel": ("europe", (1.0, 50.9), 4.0), "dunkirk": ("europe", (2.45, 51.0), 9.0),
    "britain": ("europe", (-1.5, 53.5), 2.4), "east_front": ("europe", (31.0, 52.5), 1.3),
    "moscow": ("europe", (36.5, 55.3), 3.5), "leningrad": ("europe", (30.3, 59.9), 5.0),
    "stalingrad": ("europe", (43.9, 48.75), 6.0), "caucasus": ("europe", (42.0, 46.0), 2.5),
    "kursk": ("europe", (36.0, 51.6), 4.5), "bagration": ("europe", (26.5, 53.5), 2.2),
    "north_africa": ("europe", (18.0, 31.5), 1.5), "alamein": ("europe", (28.9, 30.8), 7.0),
    "ethiopia": ("europe", (28.0, 26.0), 0.75), "italy": ("europe", (13.5, 41.5), 2.6),
    "sicily": ("europe", (14.0, 37.5), 4.5), "gustav": ("europe", (13.9, 41.6), 6.0),
    "normandy": ("europe", (-0.75, 49.55), 10.0), "bulge": ("europe", (5.6, 50.2), 6.0),
    "berlin": ("europe", (13.4, 52.5), 7.0), "balkans": ("europe", (21.0, 43.0), 2.2),
    "pacific": ("pacific", (165.0, 15.0), 1.0), "east_asia": ("pacific", (120.0, 35.0), 2.0),
    "manchuria": ("pacific", (125.0, 44.0), 3.0), "china": ("pacific", (113.0, 31.0), 2.4),
    "pearl_harbor": ("pacific", (-157.95, 21.4), 8.0), "midway": ("pacific", (-177.4, 28.2), 5.0),
    "island_hop": ("pacific", (155.0, 15.0), 1.4), "okinawa": ("pacific", (128.0, 26.5), 7.0),
    "japan": ("pacific", (136.0, 35.0), 4.0), "burma": ("pacific", (95.5, 21.0), 4.0),
    "south_east_asia": ("pacific", (112.0, 5.0), 2.2), "hiroshima": ("pacific", (131.0, 33.5), 9.0),
    "world": ("world", (10.0, 8.0), 1.0), "atlantic": ("world", (-35.0, 40.0), 2.2),
    "world_europe": ("world", (15.0, 50.0), 3.0), "world_east_asia": ("world", (120.0, 30.0), 2.5),
}

# ---------------------------------------------------------------- flood groups (region names of each view)
GROUPS = {
    "pacific": {"japan_1942_extent": ["china_occ", "indochina", "burma", "malaya", "dei", "philippines", "png",
                                      "solomons"],
                "empire_1937": ["japan", "korea", "taiwan", "manchukuo"]},
    "world": {
        "ussr": ["rus", "ukr", "blr", "est", "lva", "ltu", "mda", "geo", "arm", "aze", "kaz", "uzb", "tkm", "kgz", "tjk"],
        "axis_1942_home": ["deu", "aut", "ita", "jpn"],
        "axis_1942_occupied": ["cze", "pol", "fra", "bel", "nld", "lux", "dnk", "nor", "grc", "srb", "hrv", "bih",
                               "mne", "mkd", "svn", "kos", "alb", "ukr", "blr", "est", "lva", "ltu", "kor", "prk",
                               "twn", "phl", "idn", "mys", "mmr", "khm", "lao", "vnm", "tls", "brn", "sgp", "png"],
        "axis_minors": ["hun", "rou", "bgr", "svk", "tha"],
        "allies_1942": ["usa", "gbr", "can", "aus", "nzl", "zaf", "ind", "pak", "bgd", "lka"],
        "commonwealth": ["gbr", "can", "aus", "nzl", "zaf", "ind", "pak", "bgd", "lka", "nga", "gha", "ken", "uga",
                         "tza", "zmb", "zwe", "mwi", "sle", "egy", "mys", "sgp", "mmr", "jam"],
        "nato_1949": ["usa", "can", "gbr", "fra", "ita", "bel", "nld", "lux", "dnk", "nor", "isl", "prt"],
        "warsaw_pact": ["rus", "ukr", "blr", "est", "lva", "ltu", "mda", "geo", "arm", "aze", "kaz", "uzb", "tkm",
                        "kgz", "tjk", "pol", "cze", "svk", "hun", "rou", "bgr", "alb"],
    },
}

# ---------------------------------------------------------------- era presets: {region: side}, {region: owner},
# occupied set. Europe 1936 (before the Rhineland), Aug 1939, Jul 1940, Jun 1941; Pacific 1937, Dec 1941, mid 1942.
GER = ["germany", "g37east", "east_prussia", "rhineland"]
_EU_BASE_SIDE = {"uk": "allies", "france_occ": "allies", "france_vichy": "allies", "ussr": "soviet", "italy": "italy",
                 "italy_south": "italy", "sicily": "italy", "libya": "italy", "eritrea": "italy", "somalia": "italy",
                 **{r: "germany" for r in GER}}
_EU_BASE_OWNER = {**{r: "germany" for r in GER}, "france_occ": "france", "france_vichy": "france",
                  "italy_south": "italy", "sicily": "italy", "fin_karelia": "finland", "fin_petsamo": "finland",
                  "bessarabia": "romania", "bukovina": "romania", "romania": "romania"}


def _era(side, owner, occupied):
    return dict(side=side, owner=owner, occupied=sorted(occupied))


_e36s = {**_EU_BASE_SIDE, "rhineland": "neutral"}
_e36o = {**_EU_BASE_OWNER, "sudeten": "czechoslovakia", "czech": "czechoslovakia", "slovakia": "czechoslovakia",
         "carpatho": "czechoslovakia", "poland_w": "poland", "poland_e": "poland"}
_e39s = {**_EU_BASE_SIDE, "austria": "germany", "sudeten": "germany", "czech": "germany", "slovakia": "italy",
         "albania": "italy", "ethiopia": "italy", "poland_w": "allies", "poland_e": "allies"}
_e39o = {**_EU_BASE_OWNER, "austria": "germany", "sudeten": "germany", "czech": "germany", "slovakia": "slovakia",
         "carpatho": "hungary", "poland_w": "poland", "poland_e": "poland", "albania": "italy", "ethiopia": "italy"}
_e39x = {"austria", "sudeten", "czech", "albania", "ethiopia"}
_e40s = {**_e39s, "channel_islands": "germany", "poland_w": "germany", "poland_e": "soviet", "lithuania": "soviet", "latvia": "soviet",
         "estonia": "soviet", "bessarabia": "soviet", "bukovina": "soviet", "fin_karelia": "soviet",
         "denmark": "germany", "norway": "germany", "netherlands": "germany", "belgium": "germany",
         "luxembourg": "germany", "france_occ": "germany", "france_vichy": "neutral"}
_e40o = {**_e39o, "poland_e": "ussr", "lithuania": "ussr", "latvia": "ussr", "estonia": "ussr", "bessarabia": "ussr",
         "bukovina": "ussr", "fin_karelia": "ussr", "luxembourg": "germany", "france_vichy": "vichy"}
_e40x = _e39x | {"channel_islands", "poland_w", "poland_e", "lithuania", "latvia", "estonia", "bessarabia", "bukovina", "fin_karelia",
                 "denmark", "norway", "netherlands", "belgium", "luxembourg", "france_occ"}
_e41s = {**_e40s, "yugoslavia": "germany", "greece": "germany", "hungary": "italy", "romania": "italy",
         "bulgaria": "italy", "carpatho": "italy", "ethiopia": "allies"}
_e41x = (_e40x | {"yugoslavia", "greece"}) - {"ethiopia"}
_P37s = {"japan": "japan", "korea": "japan", "taiwan": "japan", "manchukuo": "japan", "china": "china",
         "china_occ": "china", "ussr": "soviet", "usa": "allies", "australia": "allies", "nz": "allies",
         "india": "allies", "burma": "allies", "malaya": "allies", "philippines": "allies", "png": "allies"}
_P41s = {**_P37s, "china_occ": "japan", "indochina": "japan", "dei": "allies"}
_P42s = {**_P41s, "thailand": "japan", "burma": "japan", "malaya": "japan", "dei": "japan", "philippines": "japan",
         "png": "japan", "solomons": "japan"}
_e40ms = {**_e39s, "poland_w": "germany", "poland_e": "soviet", "fin_karelia": "soviet", "denmark": "germany",
          "norway": "germany"}                                     # 10 May 1940: France and the Low Countries free
_e40mo = {**_e39o, "poland_e": "ussr", "fin_karelia": "ussr"}
_e40mx = _e39x | {"poland_w", "poland_e", "fin_karelia", "denmark", "norway"}
ERAS = {
    "europe": {"1936": _era(_e36s, _e36o, set()), "1939": _era(_e39s, _e39o, _e39x),
               "1940_may": _era(_e40ms, _e40mo, _e40mx), "1940": _era(_e40s, _e40o, _e40x),
               "1941": _era(_e41s, _e40o, _e41x)},
    "pacific": {"1937": _era(_P37s, {}, {"korea", "taiwan", "manchukuo"}),
                "1941": _era(_P41s, {}, {"korea", "taiwan", "manchukuo", "china_occ", "indochina"}),
                "1942": _era(_P42s, {}, {"korea", "taiwan", "manchukuo", "china_occ", "indochina", "burma", "malaya",
                                         "dei", "philippines", "png", "solomons"})},
}


# ---------------------------------------------------------------- campaigns: keyed floods/annexations over 0 -> 1
# (u, region or group, side or None, flood origin (lon, lat) or None, flood duration (fraction), occupied, new owner)
CAMPAIGNS = {
    "poland_1939": [(0.0, "poland_w", "germany", (16.4, 52.0), 0.45, True, None),
                    (0.55, "poland_e", "soviet", (27.0, 51.6), 0.4, True, "ussr")],
    "scandinavia_1940": [(0.0, "denmark", "germany", (9.3, 54.9), 0.3, True, None),
                         (0.2, "norway", "germany", (10.7, 59.5), 0.7, True, None)],
    # 10 May -> 22 June 1940 (u = days / 43): the Low Countries, the sickle to the coast by 21 May (u 0.26), the
    # Dunkirk pocket 26 May - 4 June (u 0.37-0.58, a zone the scene adds), Fall Rot from 5 June, the armistice
    "fall_of_france": [(0.0, "netherlands", "germany", (6.9, 52.2), 0.12, True, None),
                       (0.0, "luxembourg", "germany", (6.3, 49.8), 0.03, True, "germany"),
                       (0.0, "belgium", "germany", (6.2, 50.6), 0.4, True, None),
                       (0.07, "france_north", "germany", (4.9, 49.7), 0.19, True, None),
                       (0.6, "france_occ", "germany", (2.5, 49.4), 0.35, True, None),
                       (0.98, "france_vichy", "neutral", None, 0.0, False, "vichy"),
                       (0.98, "channel_islands", "germany", None, 0.0, True, None)],
    "soviet_1940": [(0.0, "baltics", "soviet", (27.6, 56.5), 0.5, True, "ussr"),
                    (0.4, "bessarabia", "soviet", (29.5, 47.0), 0.4, True, "ussr"),
                    (0.4, "bukovina", "soviet", (26.5, 48.4), 0.4, True, "ussr")],
    "balkans_1941": [(0.0, "yugoslavia", "germany", (16.0, 46.2), 0.6, True, None),
                     (0.3, "greece", "germany", (22.5, 41.2), 0.6, True, None)],
    "italy_1943": [(0.0, "sicily", "allies", (14.0, 37.1), 0.35, True, None),
                   (0.5, "italy_south", "allies", (15.8, 39.0), 0.5, True, None)],
}


for _eras in ERAS.values():                                     # northern France follows the occupied zone
    for _e in _eras.values():
        for _k in ("side", "owner"):
            if "france_occ" in _e[_k]:
                _e[_k]["france_north"] = _e[_k]["france_occ"]
        if "france_occ" in _e["occupied"]:
            _e["occupied"] = sorted(set(_e["occupied"]) | {"france_north"})


def content():
    """Everything above as one JSON-ready dict (lon/lat lists)."""
    return dict(
        fronts={k: dict(view=v["view"], side=v["side"], keys=[[u, [list(p) for p in pts]] for u, pts in v["keys"]])
                for k, v in FRONTS.items()},
        arrows={k: dict(side=s, paths=[[list(p) for p in path] for path in paths], width=ARROW_WIDTH.get(k))
                for k, (s, paths) in ARROWS.items()},
        lines={k: dict(view=v, style=st, pts=[list(p) for p in pts]) for k, (v, st, pts) in LINES.items()},
        line_groups=GROUP_LINES,
        zones={k: dict(view=v, kind=kind, side=side,
                       geom=([list(geom[0]), geom[1]] if kind == "ring" else [list(p) for p in geom]))
               for k, (v, kind, side, geom) in ZONES.items()},
        pins={k: dict(view=v, pins=p) for k, (v, p) in PINS.items()},
        views={k: dict(view=v, at=list(at), zoom=z) for k, (v, at, z) in VIEWS.items()},
        groups=GROUPS, eras=ERAS,
        campaigns={k: [[u, r, sd, list(o) if o else None, d, oc, ow] for u, r, sd, o, d, oc, ow in evs]
                   for k, evs in CAMPAIGNS.items()})
