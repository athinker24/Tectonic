# B. Coastline and sea-level handling in landscape evolution models; engine comparison; free CI limits

Status: DONE (see Status section at end). Date of research: 2026-11-12.

Labels: [B] full text read, [D] official documentation, [Ö] search summary, BULUNAMADI = not found, ERİŞİLEMEDİ = could not access.

## 1. Sea level and coastal boundary handling
- Landlab [B] (source code read from PyPI wheel landlab 2.11.0, not from docs site): boundary node status `BC_NODE_IS_FIXED_VALUE` (`grid.fixed_value_boundary_nodes`, `grid/base.py` l.285-286, 1011-1040). The SPACE docstring example (`components/space/space.py`) sets all edges closed and a single base-level outlet via `mg.set_watershed_boundary_condition_outlet_id(0, elev, -9999.0)`. `flow_director_d8.py` l.238 treats fixed-value nodes as flow sinks/outlets. Sea level is NOT a parameter of SPACE, StreamPowerEroder or FastscapeEroder; the only `sea_level__elevation` field is in `CarbonateProducer` (`components/carbonate/carbonate_producer.py` l.74-82, 245-250), which is a carbonate component, not a coastal erosion boundary. Docs site landlab.readthedocs.io: ERİŞİLEMEDİ (DNS fail); landlab.csdms.io not yet tried.
- Landlab GitHub master README: 200 (repo tree API and file-raw paths for components return 403/404 in this session; repo access not enabled for gh).
- goSPL [B] (sdist gospl-2026.7.14 from PyPI, read as text, not executed): sea level is a time function, `self.sealevel = self.seafunction(self.tNow)` (`gospl/mesher/unstructuredmesh.py` l.565, 751-755). Marine deposition uses a sea-level comparison in `gospl/sed/seaplex.py` (`sinkIDs = lFill <= self.sealevel`, see REFACTOR_AUDIT.md l.170). Subaqueous diffusion `_diffuseOcean` (`∂h/∂t = ∇·(Cd∇h)`, docs/DESIGN_PROVENANCE.md l.250); base diffusivities `Cda`/`Cdm` (land/marine) in YAML (docs/DESIGN_DUAL_LITHOLOGY.md l.163). Pit filling restricted to "land and enclosed seas" (`pitfilling.py` l.690). Coastal boundary is open-sea handling via sea level, not a fixed-elevation edge. Docs gospl.readthedocs.io: ERİŞİLEMEDİ (DNS fail).
- Badlands [B] (sdist badlands-2.3.1): sea level forcing `self.sealevel = self.sea0 + self.seaFunc(time)` (or with z0 when `udw` flag set) in `src/badlands/forcing/forceSim.py` l.241-261. Carbonate module uses `depth = elevation - sealevel` (`model.py` l.579). Coastal wave/longshore transport module `simulation/waveSed.py` (l.31, 194, 362, 421). TIN-based, not raster.
- Fastscapelib [D] (sdist 0.3.0, doc/source/guide_grids.md): three grid types: profile, raster, triangular (irregular mesh, "this class doesn't implement any triangulation"). FlowGraph sets all `FIXED_VALUE` nodes as base levels by default. DiffusionADIEroder ignores node status and always uses fixed-value raster borders (l.134), a coastal-relevant limit. Licence GPL-3.0 (pyproject.toml).
- CHILD (Tucker): [Ö] CSDMS wiki (https://csdms.colorado.edu/wiki/Model:CHILD) lists source github.com/childmodel/child, GPL v2, maintenance only as of 2020; origin MIT 1997 (Gasparini, Lancaster, Tucker, Bras). One archived CZO page says C++; language not confirmed. Sea-level capability: BULUNAMADI in search results (not verified in source).
- Yuan et al. 2019 [B] (HAL hal-02136641 PDF, pdftotext): base-level nodes are open boundaries: "For the nodes at base level (open boundary, Figure 1b), we assume that the elevation is constant through time" (eq. 16) and "we also assume that sediment can leave the system from these base level nodes." This is the fixed-elevation outflow approach (no explicit sea-level term found in text: BULUNAMADI).
- Gasparini, Forte & Barnhart, "The trouble with time to steady state calculated from computational landscape evolution models", ESurf preprint esurf-2023-17 [B] (landlab 2.4.2.dev0, CHILD, TTLEM comparison, time-to-steady-state focus): "All of the nodes on the perimeter of grid were open boundaries where water can exit, but not enter, the grid. The elevation of the perimeter boundary nodes was fixed at zero meters." Good template for a fixed-elevation coast.
- Badlands: TBD
- goSPL: TBD
- CHILD (Tucker): TBD

## 2. Preventing artificial coastal steps with fixed-sea-level boundaries
- Slope limiting near coast: TBD
- Coastal plain / lagoon models (Pelletier 2013): TBD
- Cordonnier et al. 2017 (sculpting mountains): TBD

### Cross-cutting synthesis (sea level / coastal boundary)
- Fixed-elevation outflow edge (sediment leaves, elevation held): Landlab `BC_NODE_IS_FIXED_VALUE` with a single outlet [B]; Yuan et al. 2019 open base-level nodes, sediment leaves [B]; Gasparini et al. 2023 perimeter open boundaries at 0 m [B]; Fastscapelib FlowGraph base levels = FIXED_VALUE nodes [D].
- Pitfall, documented: Fastscapelib DiffusionADIEroder ignores node status and always assumes fixed-value raster borders [D]. A coastal diffusion step could therefore behave differently from the flow solver.
- Time-varying sea level: Badlands `sealevel = sea0 + seaFunc(time)` [B]; goSPL `sealevel = seafunction(tNow)` [B], with sediment sinks below sea level and subaqueous diffusion [B].
- Landlab: no sea-level parameter in SPACE, StreamPowerEroder or FastscapeEroder [B]. The only sea-level field is in CarbonateProducer [B].
- Section 2 approaches (coastal slope limiting, lagoon/coastal-plain model, Pelletier 2013, coastal-plain diffusion): none found in any consulted source. Pelletier 2013: BULUNAMADI. Cordonnier et al. 2018 full text: no sea-level or coastline handling; its "boundary" refers to fault/plate borders [B]. Any "artificial step" explanation below is my inference, not sourced.

## 3. Comparison table (Landlab, goSPL, Fastscapelib, Badlands, Pecube, TTLEM, CHILD)

Labels: [B] read in text; [D] official/package metadata; [Ö] search summary only.

| Model | Language | Grid | Parallel | Sediment | License | Latest release | Install |
|---|---|---|---|---|---|---|---|
| Landlab 2.11.0 | Python (C ext for flexure) [B] | Raster, hex, Voronoi/irregular dual graph [B/Ö] | BULUNAMADI | Yes (SPACE, carbonate, flux) [B] | MIT [Ö, GitHub page] | 2.11.0, uploaded 2026-04-06 [D PyPI] | `pip install landlab` [D] |
| goSPL 2026.7.14 | Python, Fortran dir [D/Ö] | Unstructured mesh (mesher/unstructuredmesh.py) [B]; spherical: pyshtools dependency, not verified | Yes: petsc4py + mpi4py in dependencies [B] | Yes (marine deposition, river sediment) [B] | GPL-3.0 [D] | 2026.7.14, uploaded 2026-07-10 [D PyPI] | `pip install gospl` [D] |
| Fastscapelib 0.3.0 | C++ with Python bindings [D] | Profile, raster, triangular (static) [D] | BULUNAMADI | Partial (sediment transport in eroders docs) [D] | GPL-3.0 [D] | 0.3.0, 2025-06-25 [D PyPI] | `pip install fastscapelib` [D] (wheels for py3.10–3.13, Linux/macOS/Windows) |
| Fastscapelib-fortran | Fortran + Python bindings [D] | BULUNAMADI | BULUNAMADI | BULUNAMADI | GPL-3.0 [D] | BULUNAMADI | BULUNAMADI |
| Badlands 2.3.1 | Python with Fortran utils (utils/*.f90) [B] | TIN (irregular triangulated) [D] | BULUNAMADI in model.py | Yes (waves, longshore transport, carbonate) [B] | Conflicting: PyPI GPL text; GitHub "LGPL-3.0 and 2 other licenses" [D]; check LICENSE | 2.3.1, uploaded 2026-05-01 [D PyPI] | PyPI package exists; install not tested |
| Pecube (Braun) | Fortran [Ö] | 3D finite element (advection-diffusion) [Ö] | BULUNAMADI | No (thermochronology, not sediment) [Ö, inferred] | GPL-3.0 [D] | BULUNAMADI (no dates on page) | BULUNAMADI |
| TTLEM (TopoToolbox) | MATLAB, requires MATLAB 2023b+ [D] | Raster (TopoToolbox 2) [Ö] | BULUNAMADI | Variant TTLEM_Sed exists [Ö] | LICENSE.md, name not confirmed [D] | V1.0b, 2025-03-18 [D GitHub] | TopoToolbox + MATLAB path |
| CHILD | C++ per one archived CZO page; not confirmed [Ö] | BULUNAMADI | BULUNAMADI | Yes (fluvial and hillslope sediment transport) [Ö] | GPL v2 [Ö CSDMS] | Maintenance only as of 2020 [Ö] | BULUNAMADI |

Notes:
- The user-supplied name "TTLEC" is TTLEM in the literature.
- Ranked by update activity from these metadata: goSPL and Landlab have 2026 releases; Badlands has a 2026 release; Fastscapelib 0.3.0 is from 2025; CHILD is maintenance-only per CSDMS; TTLEM last tagged 2025.
- docs sites landlab.readthedocs.io and gospl.readthedocs.io: ERİŞİLEMEDİ (DNS). landlab.csdms.io and badlands.readthedocs.io were not tested.

## 4. Free CI limits ("Actions") and benchmarks
- GitHub Actions, public repo, standard hosted runner: free and unlimited; 4 vCPU, 16 GB RAM, 14 GB SSD for Linux x64 (label ubuntu-latest) [Ö, search summary of docs.github.com runners page; direct fetch of docs.github.com ERİŞİLEMEDİ]. Private repo: 2 vCPU, 8 GB RAM [Ö].
- Limits: each job max 6 hours, then cancelled [Ö]; a workflow run max 35 days [Ö]; free plan concurrency 20 jobs (5 macOS) [Ö]. Each job runs on a new VM [Ö]. Artifact storage, minutes and cache quotas apply to private repos [Ö].
- Landlab single-core speed and time for 1 to 4 million nodes: BULUNAMADI. Barnhart et al. 2020 full text has no timing or node-count benchmark (only a note that performance improved for memory management and speed) [B].
- Braun & Willett 2013 (Geomorphology 180-181:170-179, DOI 10.1016/j.geomorph.2012.10.008): title and O(n) implicit claim [Ö]. Full text not accessed; benchmark numbers BULUNAMADI.
- Yuan et al. 2019 (JGR Earth Surface 124(6):1346-1365, DOI 10.1029/2018JF004867): method is O(N) and implicit, unconditionally stable [Ö]; PDF text [B] has no runtime or node-count figures (grep for CPU/second/runtime found none). Note the name is not "FastScape-SPL" in the title; the title is "A New Efficient Method to Solve the Stream Power Law Model Taking Into Account Sediment Deposition".
- Campforts, Schwanghart & Govers 2017, TTLEM 1.0 (ESurf 5, 47, 2017; DOI via https://www.earth-surf-dynam.net/5/47/2017/): focus is removing numerical diffusion [Ö]. Timing data: BULUNAMADI (paper not fully read).
- Barnhart et al. 2020 is in Earth Surface Dynamics 8, 379-397 (DOI 10.5194/esurf-8-379-2020), not GMD as the request stated [Ö + B].
- Honest bottom line: no published single-core or node-count timing for Landlab was found. Estimating whether 1 to 4 million nodes fit in 16 GB RAM or 6 hours would need a timing run on the target runner; not performed.

## Sources
- Landlab GitHub: https://github.com/landlab/landlab [D, fetched]; PyPI: https://pypi.org/pypi/landlab/json [D]; wheel landlab 2.11.0 (source read) [B]
- goSPL GitHub: https://github.com/geodels/gospl [D]; PyPI sdist gospl-2026.7.14 [B]; docs gospl.readthedocs.io ERİŞİLEMEDİ
- Badlands GitHub: https://github.com/badlands-model/badlands [D]; PyPI sdist badlands-2.3.1 [B]
- Fastscapelib: https://pypi.org/project/fastscapelib/ [D]; sdist 0.3.0 [D]; https://github.com/fastscape-lem/fastscapelib-fortran [D]
- Pecube: https://github.com/jeanbraun/Pecube [D, GPL-3.0]; Pecube-D Zenodo: https://zenodo.org/records/7785668 [Ö]
- TTLEM: https://github.com/topotoolbox/TTLEM [D]; paper https://www.earth-surf-dynam.net/5/47/2017/ [Ö]
- CHILD: https://csdms.colorado.edu/wiki/Model:CHILD [Ö]; https://github.com/childmodel/child [Ö]
- Barnhart et al. 2020: https://esurf.copernicus.org/articles/8/379/2020/ (PDF read) [B]; DOI 10.5194/esurf-8-379-2020
- Yuan et al. 2019: HAL https://hal-univ-tlse3.archives-ouvertes.fr/hal-02136641 (PDF read) [B]; DOI 10.1029/2018JF004867
- Gasparini, Forte & Barnhart (ESurf 2023 preprint): https://esurf.copernicus.org/preprints/esurf-2023-17/ (PDF read) [B]
- Cordonnier et al., IEEE TVCG 2018 (accepted 2017): https://www.cs.purdue.edu/homes/bbenes/papers/Cordonnier18TVCG.pdf (PDF read) [B]
- Braun & Willett 2013: DOI 10.1016/j.geomorph.2012.10.008 [Ö]
- GitHub Actions limits: https://docs.github.com/en/actions/reference/actions-limits [Ö]; runners: https://docs.github.com/en/actions/reference/runners/github-hosted-runners [Ö]; docs.github.com direct fetch ERİŞİLEMEDİ
- Pelletier 2013 (coastal plain): BULUNAMADI
- Landlab docs landlab.readthedocs.io: ERİŞİLEMEDİ (DNS fail)

## Status
Complete. Corrections to the request: Barnhart 2020 is ESurf, not GMD; Yuan 2019 title differs from "FastScape-SPL"; Cordonnier paper is TVCG 2018; TTLEC is TTLEM; Pelletier 2013 not found.
