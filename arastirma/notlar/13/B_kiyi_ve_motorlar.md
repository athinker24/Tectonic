# B. Coastline and sea-level handling in landscape evolution models; engine comparison; free CI limits

Status: IN PROGRESS (skeleton, sources being collected)

Labels: [B] full text read, [D] official documentation, [Ö] search summary, BULUNAMADI = not found, ERİŞİLEMEDİ = could not access.

## 1. Sea level and coastal boundary handling
- Landlab [B] (source code read from PyPI wheel landlab 2.11.0, not from docs site): boundary node status `BC_NODE_IS_FIXED_VALUE` (`grid.fixed_value_boundary_nodes`, `grid/base.py` l.285-286, 1011-1040). The SPACE docstring example (`components/space/space.py`) sets all edges closed and a single base-level outlet via `mg.set_watershed_boundary_condition_outlet_id(0, elev, -9999.0)`. `flow_director_d8.py` l.238 treats fixed-value nodes as flow sinks/outlets. Sea level is NOT a parameter of SPACE, StreamPowerEroder or FastscapeEroder; the only `sea_level__elevation` field is in `CarbonateProducer` (`components/carbonate/carbonate_producer.py` l.74-82, 245-250), which is a carbonate component, not a coastal erosion boundary. Docs site landlab.readthedocs.io: ERİŞİLEMEDİ (DNS fail); landlab.csdms.io not yet tried.
- Landlab GitHub master README: 200 (repo tree API and file-raw paths for components return 403/404 in this session; repo access not enabled for gh).
- Badlands: TBD
- goSPL: TBD
- CHILD (Tucker): TBD

## 2. Preventing artificial coastal steps with fixed-sea-level boundaries
- Slope limiting near coast: TBD
- Coastal plain / lagoon models (Pelletier 2013): TBD
- Cordonnier et al. 2017 (sculpting mountains): TBD

## 3. Comparison table (Landlab, goSPL, Fastscapelib, Badlands, Pecube, TTLEM)
TBD

## 4. Free CI limits ("Actions") and benchmarks
- GitHub Actions free runner limits: TBD
- Landlab 2.0 speed (Barnhart 2020): TBD
- Braun & Willett 2013: TBD
- Yuan et al. 2019 FastScape-SPL: TBD
- Campforts et al. 2017 TTLEC: TBD

## Sources
TBD
