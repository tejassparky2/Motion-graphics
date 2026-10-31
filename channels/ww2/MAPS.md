# WW2 maps: what you can call by name

Engine: `channels/ww2/kit/maps.py`; content source: `channels/ww2/kit/map_content.py` (lon/lat, hand-traced at map scale); compiled to `channels/ww2/data/fronts.json` by `python -m channels.ww2.kit.maps content`.

```python
m = Map("europe", era="1941")            # eras below; muted=1.0 for the Holocaust chapter
m.view("stalingrad", 0)                      # camera preset (more keys: m.camera_key(t, (lon, lat), zoom))
m.front("case_blue_1942", 1.0, 5.0)          # a front moves between its keyframes from t=1 to t=5
m.arrows("stalingrad_uranus", 2.0, 3.5)      # an arrow set grows (staggered 0.25 s)
m.zone("stalingrad_ring", 3.0, 4.5)          # a ring closes / a pocket or area fades in
m.line("maginot", 0.5, 2.0)                  # a fort chain / rail / curtain draws along
m.pins("normandy_beaches", 1.0)              # named dots in turn
m.side("rhineland", 1, "germany", origin=(8.6, 50.0), dur=1.5, occupied=False)   # flood a region or group
```

**Eras:** `europe 1936`, `europe 1939`, `europe 1940`, `europe 1941`, `pacific 1937`, `pacific 1941`, `pacific 1942`

**Fronts:** `barbarossa`, `moscow_1941`, `case_blue_1942`, `kursk_1943`, `bagration`, `bulge`, `bulge_collapse`, `alamein`, `china`, `japan_1942_perimeter`

**Arrow sets:** `italy_ethiopia_1935`, `ethiopia_1935`, `poland_1939`, `soviet_poland_1939`, `denmark_1940`, `norway_1940`, `west_1940`, `sickle_1940`, `sealion_1940`, `blitz_1940`, `barbarossa`, `moscow_counter`, `case_blue_1942`, `stalingrad_uranus`, `kursk_1943`, `kursk_counter`, `reverse_1943`, `bagration`, `rommel_1942`, `el_alamein`, `torch_1942`, `sicily_1943`, `salerno_1943`, `anzio_1944`, `normandy_1944`, `bulge_1944`, `patton_bastogne`, `west_1945`, `berlin_1945`, `manchuria_1931`, `china_1937`, `pearl_harbor`, `japan_1941_42`, `midway_japan`, `midway_usa`, `island_hop`, `macarthur`, `burma_1944`, `manchuria_1945`, `atomic_1945`

**Lines:** `maginot`, `gustav`, `iron_curtain`, `secret_1939`, `rail_amsterdam`, `rail_paris`, `rail_berlin`, `rail_prague`, `rail_vienna`, `rail_budapest`, `rail_thessaloniki`, `rail_warsaw`, `rails_holocaust`

**Zones:** `dunkirk_pocket`, `battle_of_britain`, `ussr_occupied_1941`, `ussr_occupied_1942`, `stalingrad_ring`, `berlin_ring`, `leningrad_siege`, `bastogne_ring`, `japan_1942`

**Pin sets:** `normandy_beaches`, `normandy_airborne`, `camps`, `ghettos`, `island_hop`, `pacific_1941`, `midway`, `atomic`

**Camera presets:** `europe`, `poland`, `rhineland`, `central_europe`, `scandinavia`, `west_1940`, `maginot`, `ardennes`, `channel`, `dunkirk`, `britain`, `east_front`, `moscow`, `leningrad`, `stalingrad`, `caucasus`, `kursk`, `bagration`, `north_africa`, `alamein`, `ethiopia`, `italy`, `sicily`, `gustav`, `normandy`, `bulge`, `berlin`, `balkans`, `pacific`, `east_asia`, `manchuria`, `china`, `pearl_harbor`, `midway`, `island_hop`, `okinawa`, `japan`, `burma`, `south_east_asia`, `hiroshima`, `world`, `atlantic`, `world_europe`, `world_east_asia`

**Flood groups (Europe, in maps.py):** `germany_1936`, `germany_1937`, `greater_germany`, `czechoslovakia`, `poland`, `france`, `low_countries`, `baltics`, `romania_1939`, `finland_1939`, `italy_all`, `east_africa`

**Flood groups (Pacific / world):** `pacific:japan_1942_extent`, `pacific:empire_1937`, `world:ussr`, `world:axis_1942_home`, `world:axis_1942_occupied`, `world:axis_minors`, `world:allies_1942`, `world:commonwealth`, `world:nato_1949`, `world:warsaw_pact`

**Europe regions:** germany, rhineland, g37east, east_prussia, austria, sudeten, czech, slovakia, carpatho, poland_w, poland_e, lithuania, latvia, estonia, finland, fin_karelia, fin_petsamo, ussr, bessarabia, bukovina, romania, hungary, bulgaria, yugoslavia, albania, greece, turkey, italy, italy_south, sicily, france_occ, france_vichy, belgium, netherlands, luxembourg, denmark, norway, sweden, uk, ireland, iceland, spain, portugal, switzerland, morocco, algeria, tunisia, libya, egypt, ethiopia, eritrea, somalia, sudan, and the Middle East.

**Pacific regions:** japan, korea, taiwan, manchukuo, china_occ, china, mongolia, ussr, philippines, indochina, thailand, burma, malaya, dei, png, solomons, australia, nz, india, usa, canada, mexico. **World regions:** ISO-style codes (deu, gbr, usa, ...).

Notes: the world view's seam is at 180 deg, so the 'globe spins to the Pacific' move cuts to the pacific view. The coastline is Natural Earth 50m: fine to about zoom 8; Normandy at zoom 10 reads but is soft.
