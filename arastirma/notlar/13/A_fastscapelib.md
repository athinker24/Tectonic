# Fastscapelib, fastscapelib-python and the fastscape / xsimlab-fastscape packages: research notes

Status: complete for the reachable sources. Items marked BULUNAMADI (not found) or ERİŞİLEMEDİ (not reachable) are listed explicitly.

Tags: [B] full source or full page read; [D] official documentation text (package metadata / docs in sdist); [Ö] search summary (none used).

## Access notes
- https://fastscapelib.readthedocs.io: ERİŞİLEMEDİ (DNS: getaddrinfo ENOTFOUND). Not retried.
- GitHub API (`gh api`) for fastscape-lem/* returned 403 (repo not enabled for session). add_repo was not called (per instructions).
- github.com repo pages for fastscapelib: readable via WebFetch. Repos fastscapelib-python and xsimlab-fastscape: 403 via curl; WebFetch of xsimlab-fastscape returned 404.
- Source headers fetched from raw.githubusercontent.com, branch `main`. Paths used: `include/fastscapelib/...`. Files not on main (404): README.md at repo root, trimesh_grid.hpp, xt_grid.hpp, diffusion.hpp (the actual file is eroders/diffusion_adi.hpp).

## 1. Current version, features, grid types, boundary conditions, node status
- Version [B, PyPI JSON]: fastscapelib 0.3.0, uploaded 2025-06-25. Earlier: 0.2.2 (2024-06-05), 0.2.0 (2023-10-09). https://pypi.org/project/fastscapelib/
- Description [B, GitHub README via PyPI description]: "A C++/Python library of efficient and reusable algorithms for landscape evolution modeling ... a (bare bones) toolkit for building your own Landscape Evolution Models (LEMs) or integrating it with other existing codes or models."
- Requirements [D, PyPI metadata]: Python >= 3.10; numpy >= 1.24; numba optional extra; pytest for tests.
- Grid headers present [B]: raster_grid.hpp, profile_grid.hpp, healpix_grid.hpp (plus base grid_base.hpp, base.hpp). Trimesh: BULUNAMADI (header not downloadable; the file name on main was 404; not otherwise confirmed).
- Node status enum [B, grid_base.hpp, `enum class node_status : std::uint8_t`]:
  - `core = 0` inner node
  - `fixed_value = 1` Dirichlet boundary
  - `fixed_gradient = 2` Neumann boundary
  - `looped = 3` periodic / reflective boundary
  - `ghost = 4` inactive node outside the domain (not in the original question list, but present in the source)
- Raster boundaries [B, raster_grid.hpp]: separate status for left, right, top, bottom borders (`raster_boundary_status`). Doc comment priority: fixed value > fixed gradient > looped > core. Looped borders must be symmetrical; otherwise `std::invalid_argument("looped boundaries are not symmetrical")`.
- HEALPix boundary [B, healpix_grid.hpp]: `node_status::looped` is rejected with `std::invalid_argument`; ghost nodes are skipped in neighbor lookup.
- Raster connectivity [B]: `raster_connect::queen` (8 neighbors, incl. diagonals) and `bishop` (4 diagonal neighbors). Neighbor struct stores flat index, row, col, distance, status.

## 2. Flow routing and depression handling
- Single flow [B, flow_router.hpp]: `single_flow_router(int n_threads)`. Uses thread pool when `threads_count() > 1`. Raster grids use queen (8-neighbor, D8-like) connectivity.
- Multiple flow [B, flow_router.hpp]: `multi_flow_router(double slope_exp)`, output `flow_direction::multi`. C++ default slope_exp = 1.0. The Python `fastscape` wrapper says the default slope exponent is 0 (equal split among receivers) [B, fastscape/processes/flow.py docstring]. These differ and should be checked against the fastscapelib-python binding.
- Sink resolvers [B, sink_resolver.hpp]:
  - `pflood_sink_resolver`: priority-flood fill (`detail::fill_sinks_sloped`).
  - `mst_sink_resolver(mst_method basin_method = mst_method::kruskal, mst_route_method route_method = mst_route_method::carve)`; route methods `basic` and `carve`.
- Name check: the names `fill_sinks` and `mst_sinks` from the question do not exist in the source. Correct names: `pflood_sink_resolver`, `mst_sink_resolver`.

## 3. SPL eroder and hillslope diffusion
- SPL [B, eroders/spl.hpp]: `spl_eroder(flow_graph, k_coef, area_exp, slope_exp, tolerance = 1e-3)`. Equation: dh/dt = -K A^m (grad h)^n. K = k_coef (scalar or array), m = area_exp, n = slope_exp. Step: `erode(drainage_area, elevation, dt)`.
- Numerics [B, spl.hpp doc]: implicit first-order finite difference in space and time after Braun & Willett (2013) with adaptations. n = 1: direct solution. n != 1: Newton-Raphson, convergence controlled by `tolerance`.
- Boundary [B]: erosion is zero at base-level nodes of the flow graph.
- Multiple flow [B]: only for n = 1 (exception raised otherwise).
- Lakes [B]: existing closed depressions are not eroded when a sink resolver is applied; no new closed depressions are created.
- Documentation inconsistency [B]: the doc comment calls the scheme "implicit", but also says it is "stable but not implicit with respect to upslope contributing area (A)", so large time steps may be unstable.
- Hillslope diffusion [B, eroders/diffusion_adi.hpp]: `diffusion_adi_eroder` solves linear diffusion with an Alternating Direction Implicit scheme, using Thomas (TDMA) tridiagonal solves per row/column. Step: `erode(elevation, dt)`.
- Python wrapper defaults [B, fastscape/processes/channel.py]: area_exp = 0.4, slope_exp = 1, tol_rel = tol_abs = 1e-4, Gauss-Seidel convergence.

## 4. Sediment deposition and the Fortran version
- Fastscapelib C++ [B]: no sediment deposition / transport model in the headers. "sediment flux" appears only in a comment in flow_graph.hpp. Confirmed absent.
- Sediment model is in the Python package `fastscape` 0.1.0 [B], which is a wrapper over `fastscapelib_fortran` (install docs: fastscapelib-fortran 2.8.2 or later [D]):
  - `sediment_model`: stream-power extension with channel transport and deposition; MultipleFlowRouter [D, models.rst].
  - `marine_model`: adds submarine transport, deposition and compaction [D].
  - `StreamPowerChannelTD`: `g_coef` = "detached bedrock transport/deposition coefficient". Mapped to Fortran context as `g1 = g_coef`, `g2 = -1.0` [B, channel.py]. Code comments mark a TODO to set a single `g` instead of `g1`/`g2` (linked to fastscapelib-fortran PR 25).
  - `DifferentialStreamPowerChannelTD`: separate g coefficients for bedrock and soil (`g1 = g_coef_bedrock`, `g2 = g_coef_soil`) [B].
- Davy & Lague (2009): BULUNAMADI in the fetched sources (no citation found in the fastscape sdist, which has no .bib / reference list for it). The mapping of `g` to Davy & Lague's formulation is therefore not verified here.
- "ErosionModel" class in the Fortran version: BULUNAMADI in the fetched sources.

## 5. Speed and memory (1 million nodes)
- Timing results: BULUNAMADI. The benchmark directory contains benchmark_spl.cpp, benchmark_single_flow_router.cpp, benchmark_multi_flow_router.cpp, benchmark_sink_resolver.cpp, benchmark_diffusion_adi.cpp, benchmark_basin_graph.cpp, benchmark_raster_grid.cpp, benchmark_profile_grid.cpp, benchmark_setup.hpp [B, tree listing + benchmark_setup.hpp read]. No committed results.
- Benchmark setup [B, benchmark_setup.hpp]: square raster of size n x n, n in {256, 512, 1024, 2048, 4096}, reported with Google Benchmark, time unit in milliseconds. n = 1024 gives 1,048,576 nodes (about 1 million). Random or cone initial elevation.
- Memory: BULUNAMADI.
- Multi-threading [B]: single_flow_router takes `n_threads` and uses a thread pool when more than 1 thread. Other routers and SPL: BULUNAMADI for threading in the fetched headers.

## 6. License, installation, Python binding, xsimlab
- fastscapelib license [B, PyPI and GitHub README]: GNU GPL v3.0. Third-party licenses kept in a `licenses` directory.
- fastscapelib install [D, PyPI]: `pip install fastscapelib` (0.3.0). Conda package for fastscapelib: BULUNAMADI.
- fastscapelib-python: separate GitHub repo name not confirmed (403). The `fastscapelib` PyPI package (0.3.0) is the Python distribution [D].
- xsimlab-fastscape: no PyPI project with that name (404). GitHub repo not readable (403/404). Not confirmed to exist.
- Closest match found: PyPI `fastscape` 0.1.0 [B], license BSD-3-Clause, summary "A fast, versatile and user-friendly landscape evolution model", depends on `xarray-simlab >= 0.5.0` and `numba`. Docs: https://fastscape.readthedocs.io, repo: https://github.com/fastscape-lem/fastscape. Conda: `conda install fastscape -c conda-forge` [D].
- xarray-simlab: PyPI version 0.5.0, license BSD-Clause-3, "generic framework and xarray extension for computer model simulations" [B, PyPI JSON].

## 7. HEALPix grid
- Constructor [B, healpix_grid.hpp]: `healpix_grid(T nside, Healpix_Ordering_Scheme::RING, double radius = numeric_constants<>::EARTH_RADIUS_METERS)`. Default radius is Earth radius in metres.
- Number of nodes [B]: `Npix()` from healpix_cxx for the given nside.
- Area weights [B]: uniform per node, `m_node_area = 4 * pi * R^2 / N`. `nodes_areas` broadcasts this value (equal-area pixelization).
- Coordinates [B]: `nodes_lonlat(idx)` via `pix2ang`, in radians (cell centroid). `nodes_xyz()` gives Cartesian coordinates.
- Boundaries [B]: looped nodes rejected; ghost nodes excluded from neighbors.
- Dependency [B]: healpix_cxx (Healpix_Base, Healpix_Tables, vec3).

## Sources
- [B] https://github.com/fastscape-lem/fastscapelib (WebFetch of GitHub page)
- [B] https://raw.githubusercontent.com/fastscape-lem/fastscapelib/main/include/fastscapelib/grid/grid_base.hpp
- [B] https://raw.githubusercontent.com/fastscape-lem/fastscapelib/main/include/fastscapelib/grid/raster_grid.hpp
- [B] https://raw.githubusercontent.com/fastscape-lem/fastscapelib/main/include/fastscapelib/grid/healpix_grid.hpp
- [B] https://raw.githubusercontent.com/fastscape-lem/fastscapelib/main/include/fastscapelib/flow/flow_router.hpp
- [B] https://raw.githubusercontent.com/fastscape-lem/fastscapelib/main/include/fastscapelib/flow/sink_resolver.hpp
- [B] https://raw.githubusercontent.com/fastscape-lem/fastscapelib/main/include/fastscapelib/flow/flow_graph.hpp
- [B] https://raw.githubusercontent.com/fastscape-lem/fastscapelib/main/include/fastscapelib/eroders/spl.hpp
- [B] https://raw.githubusercontent.com/fastscape-lem/fastscapelib/main/include/fastscapelib/eroders/diffusion_adi.hpp
- [B] https://raw.githubusercontent.com/fastscape-lem/fastscapelib/main/benchmark/benchmark_setup.hpp
- [B] https://pypi.org/pypi/fastscapelib/json
- [B] https://pypi.org/pypi/fastscape/json (sdist https://files.pythonhosted.org/packages/85/5b/83cdabca0d5ee2e82700180a442d2fdfdb9f5925091c89dd41d96baa3db2/fastscape-0.1.0.tar.gz, read only)
- [B] https://pypi.org/pypi/xarray-simlab/json
- [D] https://github.com/fastscape-lem/fastscape (sdist docs: models.rst, install.rst, processes.rst)
- ERİŞİLEMEDİ: https://fastscapelib.readthedocs.io
