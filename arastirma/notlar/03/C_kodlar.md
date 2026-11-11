# Topic C: implementations of flexural isostasy (research notes)

Date of research: 2026-11-11. Method: primary sources first (repositories cloned with git, PyPI and conda-forge JSON APIs, documentation read from the repo copies, Wickert 2016 GMD and Beuthe arXiv 0704.1627 PDFs read with pdftotext). WebFetch was not used. Search snippets are marked as such. Anything not confirmed from a source read is marked UNVERIFIED.

## Summary table

| Code | Language | Version (date) | License | Method | Te variable | Sphere | Status |
|---|---|---|---|---|---|---|---|
| gFlex (awickert) | Python (NumPy, SciPy) | 1.3.0 on PyPI (2026-05-27); 2.0.0b2 beta (2026-07-01); CHANGES lists 1.4.0 (2026-05-29) | GPL-3.0-only | FD (sparse LU), FFT, SAS, SAS_NG | FD only (plus padding helpers) | no (lat/lon input, great-circle distance in SAS_NG only) | active, 2026 commits |
| Landlab Flexure | Python + Cython | landlab 2.11.0 (PyPI) | MIT | Green's function (kei) direct sum, infinite plate | no (scalar eet) | no | active |
| Landlab gFlex wrapper | Python | same | MIT | calls gflex F2D | via gflex | no | active |
| goSPL | Python + PETSc + pyshtools | 2026.7.14 (2026-07-10 PyPI) | GPL-3.0 | flat: FV biharmonic direct solve (PETSc); global: spectral shell (pyshtools) | yes (both) | yes, bending-only shell operator | active |
| Fastscapelib-fortran (fsf) | Fortran | version 2.9.0dev, last commit 2024-11-07 | GPL-3.0 | spectral (FFT), optional example | uniform only | no | stale, optional |
| fastscapelib (Python, C++) | C++/Python | 0.3.0 (2025-06-25) | GPL-3.0 | none (no flexure code found) | - | - | not applicable |
| Badlands isoFlex | Python wrapper of gFlex | repo commit 2026-05-01 | GPL-3.0 | gFlex FD direct | yes via gFlex | no | uses gFlex 1.x API |
| TISC (danigeos) | C | repo commit 2026-11-02 | GPL-3.0 | 2D planform flexure, EET grid input; solver details UNVERIFIED | yes (EET file) | no | active |
| tAo (in TISC repo) | C | same repo | GPL-3.0 (assumed from TISC LICENSE; UNVERIFIED for tAo) | 1D finite difference, band solver | yes (1D) | no | 1D only |
| GMT grdflexure | C (GMT) | GMT 6.3 docs | LGPL (UNVERIFIED) | FFT, constant Te, Cartesian | no | no | mature |
| SHTOOLS / pyshtools | Python/Fortran | pyshtools 4.14.1 (2026-02-23) | BSD-3-Clause | spherical harmonic transform | n/a (tool) | yes | active |

## C1. gFlex (awickert/gFlex)

- Repository: https://github.com/awickert/gFlex (clone HEAD c147574, dated 2026-07-07). Docs: https://gflex.readthedocs.io
- License: GPL-3.0-only. Source: https://github.com/awickert/gFlex/blob/master/pyproject.toml (line 23).
- PyPI (https://pypi.org/pypi/gflex/json): release 1.3.0 uploaded 2026-05-27; 2.0.0b1 uploaded 2026-06-05; 2.0.0b2 uploaded 2026-07-01. Earlier: 1.2.0 (2024-01-08). The PyPI "version" field is 1.3.0, so `pip install gflex` gives 1.3.0, not the 2.0 beta.
- CHANGES.md (https://github.com/awickert/gFlex/blob/master/CHANGES.md) lists [2.0.0b2] dated 2026-07-02 and [1.4.0] dated 2026-05-29. The 1.4.0 date does not match a PyPI upload (1.3.0 is 2026-05-27). UNVERIFIED which of 1.3.0 or 1.4.0 is the current stable.
- Python: README says >= 3.11 (https://github.com/awickert/gFlex/blob/master/README.md). PyPI metadata for 1.3.0 says >= 3.10.
- Dependencies: numpy, scipy, matplotlib, pyyaml (README install section).
- conda-forge: gflex latest 1.1.0 (https://api.anaconda.org/package/conda-forge/gflex). conda-forge is far behind PyPI.
- Governing equation (https://github.com/awickert/gFlex/blob/master/docs/theory_and_numerics.rst, lines 25-60): nabla^2(D nabla^2 w) - Te sigma:nabla nabla w + Drho g w = q, with Drho = rho_m - rho_f. Sign: w < 0 is downward.
- Methods (README; CHANGES 1.4.0):
  - fd: finite difference, sparse direct LU (iterative FD removed in 2.0, CHANGES line 307).
  - sas: gridded superposition of analytical solutions, FFT convolution. Uniform Te.
  - sas_ng: ungridded SAS for arbitrary point loads. Uniform Te. Cost proportional to number of loaded cells (Wickert 2016, Fig. 6a; https://gmd.copernicus.org/articles/9/997/2016/gmd-9-997-2016.pdf).
  - fft: spectral solver, added in 1.4.0. Uniform Te. Exact for periodic BCs; other BCs use zero padding of 4 alpha (NoOutsideLoads approximation).
  - Spectral form: w(k) = q(k) / (D k^4 + Drho g) for the 1D case (theory doc lines 265-290). Wickert 2016 says the SAS/FFT approach is "efficient using fast Fourier transform" (GMD PDF, section 2.1).
- Boundary conditions (FD; README lines 86-101): zero_displacement_zero_slope (clamped), zero_displacement_zero_moment (pinned), zero_moment_zero_shear (free), zero_slope_zero_shear (mirror), no_outside_loads (infinite; pads one flexural wavelength), periodic. SAS, SAS_NG and FFT (non-periodic axes) assume no_outside_loads. Wickert 2016 states that periodic BCs could enable a global closed-sphere FD model if dx and dy could vary (GMD PDF, around line 368): this is not implemented.
- Spatially variable Te: FD only. Padding helpers for variable Te added in 1.4.0 (`pad_domain`, `smooth_pad_Te`, `recommended_pad_width`). README says a nearest-neighbour Te map gives spurious sharp gradients.
- In-plane stresses sigma_xx, sigma_yy, sigma_xy: FD and FFT (README; CHANGES 1.4.0).
- Spherical handling: `latlon: true` with `planetary_radius` (docs/configuration.rst lines 190-197). README: "latitude/longitude solutions are exact for SAS, approximate otherwise". SAS_NG uses great-circle distance (gflex/base.py lines 417-450). The solution is still the planar plate equation, not a spherical shell.
- Performance (docs/benchmarks.rst, https://github.com/awickert/gFlex/blob/master/docs/benchmarks.rst; hardware Ryzen 7840U, NumPy 1.26.4, SciPy 1.16.3, Python 3.12.7):
  - FD 2D: about 0.6 s at 200 x 200, about 5 s at 400 x 400. Docs describe roughly N^1.5 scaling.
  - FFT 2D: about 5 ms at 400 x 400, about 40 ms at 1000 x 1000.
  - SAS 2D: about 0.2 s at 300 x 300 (FD about 2 s there).
  - FD 1D: under 1 ms up to 2000 cells.
  - LU cache (cache_factorization=True): 7-12x speedup for 2D FD at 50x50 to 400x400.
  - No timing is given for 2000 x 1000 or larger grids. See the cost section below.
- Multithreaded FFT only helps at about 2000 x 2000 and above (CHANGES 2.0 beta, Performance section, line 389).
- 2.0 beta breaking changes relevant to a reimplementation or a wrapper (CHANGES.md lines 298-340): finalize() clears all state (w and qs cleared); INI config removed (YAML only); iterative FD removed; G2009 removed; PlateSolutionType removed; attribute `te` renamed `T_e`; "mirror" is an alias for zero_slope_zero_shear; PascalCase BC strings removed; prescribed-value BCs added. Default verbosity changed to quiet (line 121).
- Maintenance: active. Commits in July 2026, CI badge in README, 2.0 beta in July 2026.

## C2. Landlab Flexure component (landlab/landlab, MIT)

- Checked: landlab clone HEAD 5fa0cf1 (dated 2026-11-10). Files: src/landlab/components/flexure/flexure.py, flexure_1d.py, funcs.py, _ext/flexure2d.pyx; src/landlab/components/gflex/flexure.py. https://github.com/landlab/landlab
- License: MIT (LICENSE.md, "The MIT License (MIT)"). PyPI license field is empty but the file says MIT.
- PyPI landlab 2.11.0 (https://pypi.org/pypi/landlab/json). Repo pyproject.toml: requires-python >= 3.12 and build requires numpy>=2.0,<3 and Cython. PyPI metadata says >= 3.11. Use 3.12.
- Method: Green's function superposition on a Cartesian raster. Kernel `_create_kei_func_grid` (flexure.py lines 270-278) = kei(sqrt(dx^2+dy^2)/alpha). Loads are summed directly: Cython `subside_loads` (flexure2d.pyx lines 17-60) loops over rows (prange, nogil) and over all loads and columns, subtracting c * kei. Cost O(N_loads x N_grid). No FFT.
- Assumptions: infinite homogeneous plate, scalar `eet` (constant Te), no boundary conditions, Cartesian distances, steady state within one update (flex_lithosphere docstring in gFlex wrapper says "proceeds to steady state in a single timestep").
- Options: method 'airy' or 'flexure'; parameters eet, youngs, rho_mantle, gravity, n_procs (flexure.py lines 176-215).
- Fields: input lithosphere__overlying_pressure_increment (Pa); output lithosphere_surface__elevation_increment (m).
- gFlex wrapper: src/landlab/components/gflex/flexure.py instantiates gflex.F2D() (line 206), sets dx, dy, qs, then initialize/run/finalize (lines 270-300). It inherits gFlex's solver and BCs (defaults not checked here).
- Flexure1D: 1D version on rows (flexure_1d.py), same Green's function idea.

## C3. goSPL (Geodels/goSPL, GPL-3.0)

- Clone HEAD 17fc4c6, log date 2026-11-12. This is one day after the research date (2026-11-11); the date is anomalous and flagged. PyPI gospl 2026.7.14 uploaded 2026-07-10 (https://pypi.org/pypi/gospl/json). Version scheme is YYYY.M.D.
- License: GNU GPL v3 (LICENSE file; pyproject.toml line 22).
- Python >= 3.11. Dependencies (pyproject.toml): numpy, petsc4py, scipy, numpy-indexed, pandas, h5py, vtk, ruamel.yaml, mpi4py, pyshtools. PETSc and MPI make installation heavier than pure Python (conda or HPC setups in repo).
- Code: gospl/tools/addprocess.py, class GridProcess (line 22), applyFlexure (line 622).
- method 'fem' (default, flat models only): plate equation discretised with a finite-volume negative Laplacian Lm on the unstructured DMPlex mesh. Operator Lm diag(D) Lm + Drho g I, solved with a cached direct factorisation (serial PETSc LU; MUMPS in parallel; GMRES+GAMG optional via flexfem_ prefix). Varying Te in one linear solve. Docstring lines 423-460; build at line 530. Boundary conditions via bcN/S/E/W; the test file states 0Slope0Shear = mirror and clamped pins w=0 (addprocess.py lines 560-570).
- method 'global' (spherical models only): spectral thin-shell solve with pyshtools on a Driscoll-Healy DH2 grid. Operator: w_lm = q_lm / (Drho g + D P_l), P_l = (L^2 - 4L)/R^4, L = l(l+1); degrees 0 and 1 removed (addprocess.py lines 212-225 and 267-330). The code's own benchmark (benchmarks/test_flexure.py lines 50-80) says the operator is "bending-only" and that the full thin-shell response from Turcotte et al. 1981 / Wieczorek 2007 has bending D L^2 (L-4)/(R^4 (L-1+nu)) plus membrane term E Te (L-2)/(R^2 (L-1+nu)). goSPL's bending-only operator differs by factor L/(L-1+nu): 12% at l=2, 4% at l=4, under 1% for l >= 9 (per the benchmark comments). Membrane term is a few percent of Drho g for Earth-like Te (same comments). Therefore the spherical solver is approximate at the lowest degrees. These numbers are the repo's own claims and were not re-derived here.
- Varying Te in 'global': Picard iteration with Anderson acceleration; reference rigidity from max Te (addprocess.py lines 330-380). Controls maxIter (default 50), tol (5e-4), relax (1.0).
- 'global' is serial: load gathered to rank 0, solved, broadcast (applyFlexure lines 662-690). Docs (https://github.com/Geodels/goSPL/blob/master/docs/user_guide/hpc_scaling.rst lines 283-292 and 374-390): the flexure solve is a flat ~4 s floor at every rank count on the 10 km global mesh (5.9 M nodes); about 5 s at the 8 km mesh (9.2 M nodes); about 11 s at the 5 km mesh (23.7 M nodes). Hardware: NCI Gadi.
- YAML parameters (inputparser.py lines 1670-1734; docs/DUAL_LITHOLOGY_SUMMARY.md lines 170-180): method (fem|global), rhoa (3300 default), rhoc (2300, load density), thick (uniform Te, m; default 10000), young (65 GPa), nu (0.25), interval (default 1), maxIter, tol, relax, res_deg (DH grid).
- Load and output: dZ = h - h_old (elevation change since last solve); load = rhoc g dZ; ice converted to sediment-equivalent (910/rhoc) (addprocess.py lines 622-660). Deflection accumulated into localFlex and applied to hLocal.
- Coupling: flexure solved in the model step when flexCount % flex_interval == flex_interval - 1 (model.py lines 489-497). Load accumulates between solves.
- Maintenance: active (2026 commits and releases).

## C4. Fastscapelib (fsf = fastscapelib-fortran) and fastscapelib Python

- fsf: https://github.com/fastscape-lem/fastscapelib-fortran. Clone HEAD 45f9036, last commit 2024-11-07. Version in setup.py is 2.9.0dev (unreleased). CMake option USE_FLEXURE (default OFF) (CMakeLists.txt lines 93-102).
- Flexure: Fortran `flexure(h, hp, nx, ny, xl, yl, rhos, rhoa, eet, ibc)` (docs/api.adoc lines 650-690, https://github.com/fastscape-lem/fastscapelib-fortran/blob/master/docs/api.adoc). Spectral method for the biharmonic plate equation with uniform Te. Source files Flexure2D_v1.0/src/flexure2D.f90, four1.f, realft.f, sinft.f (Numerical Recipes style FFT and sine transforms; CMakeLists lines 26-32). Constants are fixed in the docs: E = 1e11 Pa, nu = 0.25, g = 9.81 (api.adoc). Density per cell (rhos array) is accepted. "Fixed boundary conditions in flexure #34" (release notes). The flexure is documented as "a simple example of a tectonic model", not part of the core library by default.
- fastscapelib (Python, https://pypi.org/pypi/fastscapelib/json): version 0.3.0, uploaded 2025-06-25, GPL-3.0. Grep of the clone (https://github.com/fastscape-lem/fastscapelib) found no flexure or isostasy code. So no flexure there.

## C5. Badlands (isoFlex wrapper around gFlex)

- Local clone HEAD 975f595 (2026-05-01). License GPL (COPYING, LICENSE). File: src/badlands/forcing/isoFlex.py.
- Uses gflex.F2D with Method "FD", Solver "direct", PlateSolutionType "vWC1994", Quiet True, E, nu, rho_m, rho_fill, g, Te (isoFlex.py lines 108-170). These are gFlex 1.x names.
- Under gFlex 2.0 these names change: te -> T_e, PlateSolutionType removed, PascalCase BC strings removed, default verbosity quiet (gFlex CHANGES.md lines 121 and 310-330). So the wrapper will need changes to work with gFlex 2.0. Mark as a compatibility risk, not tested.

## C6. TISC and tAo (danigeos/tisc, C, GPL-3)

- Clone HEAD 04ab59d (2026-11-02). https://github.com/danigeos/tisc . Author Daniel Garcia-Castellanos (CSIC). License GNU GPL v3 (tisc/doc/LICENSE.txt line 8). Copyright 1995-2019.
- TISC (README.md lines 13-15): 2D/3D planform model, C for Linux and macOS, couples tectonics, lithospheric flexure and surface processes. Elastic thickness can be a 2D grid (EET file, TISC_Documentation.md line 144 warns that abrupt EET changes can destabilise the calculation). Flexure options: -M plate model (0 none, 1 elastic, 2 viscoelastic), -T elastic thickness (0 = local isostasy, "faster calculation"), -s m to use "mathlib" for the flexural equations (TISC_Documentation.md lines 103-118). The numerical method of the planform flexure solver was NOT confirmed (UNVERIFIED: likely Fourier or finite difference; not read in source).
- tAo (pseudo 2D, 1D cross section): tao/doc/tAo_Documentation.md lines 207-215: 1D finite-difference flexure matrix with a band solver; isost_model 0-6 (elastic with constant or variable Te, visco-elastic, elastic-plastic). Used for foreland basins. 1D only, so not a 2000 x 1000 candidate.
- The 2002 Garcia-Castellanos reference and a finite element claim could not be confirmed (search only, see failed fetches).

## C7. GMT grdflexure (FFT, constant Te)

- Doc: https://docs.generic-mapping-tools.org/6.3/supplements/potential/grdflexure.html (read as text, 17.6k chars).
- Method: Fourier-domain solution on a rectangular Cartesian FFT grid (page lines 68 and 89). Constant Te; the doc says a variable infill density makes the Fourier solution invalid (page line 92). No spatially variable Te is described.
- Options: -E Te (values above 1e10 are read as flexural rigidity D), infill density, FFT size selection (-Na for the most accurate size, -Nf to force a size) (lines 22, 40).
- Cartesian only; the doc recommends projecting for regions near a pole (line 68).
- License not checked (UNVERIFIED; GMT is LGPL).

## C8. Spherical shell flexure and the size where curvature matters

- Brotchie and Silvester (1969) is the first thin shell application to Earth's lithosphere. Brotchie 1971 is a follow-up. Source (secondary): Beuthe arXiv 0704.1627 (https://arxiv.org/pdf/0704.1627, text read via pdftotext). Beuthe states that Brotchie and Silvester do not consider tangential loads and keep only dominant derivative terms, so their equation is a special case of Kraus (1967) and Vlasov (1964) shell equations (Beuthe section 1, lines 64-72). The original 1969 paper was not accessible (UNVERIFIED equation form).
- Beuthe also states the two standard approximations of flat plate theory: area small enough to treat the shell as a flat plate, and thin shell with thickness small relative to the load wavelength (Beuthe lines 52-58). No numeric curvature threshold is given there.
- Willemann and Turcotte (1981) shell admittance is cited by Wieczorek (Treatise 2007, Springer reference; 2015 revision). Source for formula details: goSPL benchmark comments (see C3).
- Size estimate (my computation, not from a source): with gFlex's 2D flexural parameter alpha = (D/Drho g)^(1/4) (gFlex docs/theory_and_numerics.rst lines 169-170), E = 65 GPa, nu = 0.25, Te = 30 km gives D = 1.6e23 N m. With Drho = 3300 (air infill), alpha ~ 47 km; with water infill (Drho = 2270), alpha ~ 51 km. The degree at which the flexural wavelength is comparable to the Earth radius is l ~ R/alpha ~ 120 to 135. For Te = 30 km, the flat approximation is adequate for wavelengths well below R (degrees above about 10), and the lowest degrees (wavelength of order thousands of km) are where the shell terms matter. The continent (60N to 7S, about 6,700 km N-S) spans a large fraction of a hemisphere, so curvature matters for the largest-scale part of the response. Also, longitudinal grid spacing shrinks by cos(lat): at 60N dx is half that at the equator, so a uniform planar grid in lat/lon is not uniform in km. This is a practical reason to project the domain before running planar solvers.
- Spherical harmonic flexure: goSPL uses pyshtools (Driscoll-Healy DH2 grid, spectral filter, bilinear back-interpolation; SHTOOLS transform docs in repo). SHTOOLS docs and examples were checked for flexure code: none found in the clone (grep of shtools for "flexur" returned no examples). Cost of an SH expansion on an N x 2N DH grid: not confirmed (UNVERIFIED).

## C9. Costs for a 2000 x 1000 grid (2e6 cells)

Measured numbers come from gFlex docs (same hardware class). Extrapolations are labelled.

| Method | Measured base | Extrapolated 2000 x 1000 | Notes |
|---|---|---|---|
| gFlex FFT, constant Te | 40 ms at 1000 x 1000 | about 0.1 s per solve (UNVERIFIED extrapolation, roughly N log N; padding adds cells) | fastest; uniform Te only; periodic or zero pad |
| gFlex SAS (gridded) | 0.2 s at 300 x 300 | roughly 5 s per solve (UNVERIFIED; N log N with N ratio 22) | uniform Te |
| gFlex FD, sparse LU | 5 s at 400 x 400 (about 0.6 s at 200 x 200) | roughly 4 min per factorisation and large fill memory (UNVERIFIED; cells x12.5, time x about 50 under the documented N^1.5 law) | variable Te; cached solve afterwards is a triangular solve only |
| gFlex FD with LU cache | 7-12x faster than uncached at 400 x 400 | solve-only cost, far less than factorisation (UNVERIFIED size) | `cache_factorization=True` |
| Landlab Flexure (direct sum) | none published | cost is N_loads x N_grid; all 2e6 cells loaded means 4e12 kernel evaluations (infeasible); 1e4 loaded cells means about 2e10 (UNVERIFIED, tens of seconds on several cores) | infinite plate, scalar Te |
| goSPL global spectral | about 4 s per solve on 5.9 M node mesh including interpolation (serial) | UNVERIFIED for a DH grid of 1000 x 2000 | spherical, serial solve |
| goSPL flat 'fem' | no timing for a 2e6 mesh in docs read | depends on PETSc LU or MUMPS; UNVERIFIED | variable Te, unstructured mesh |
| GMT grdflexure | not timed here | FFT-cost, comparable to gFlex FFT | constant Te |

Interpretation: for a grid of 2000 x 1000 with a variable Te field, the FD sparse direct solve is the bottleneck, and the cache is essential if the matrix is fixed. For constant Te, FFT or SAS is cheap. Real numbers need a local benchmark, which was not run here (instruction: read only).

## C10. Coupling flexure into landscape evolution time stepping

- Loads: erosion and deposition change since the last flexure solve (goSPL dZ = h - h_old, addprocess.py lines 622-660). Densities: rhoc for sediment or load (goSPL 2300; gFlex example in README uses rho_fill 0 for air and water 1030 for sea; Landlab uses rho_mantle). Ice as sediment-equivalent (910/rhoc) in goSPL.
- Update interval: goSPL `interval` solves every N steps and accumulates the load (model.py lines 489-497). Landlab: a steady-state solve per update call (flexure.py docstring). gFlex wrapper in Landlab: initialize, run, finalize per step (gflex/flexure.py lines 270-300).
- Feedback: goSPL applies the deflection to the elevation, then continues (addprocess.py lines 676-690). Landlab wrapper adds the difference to topographic__elevation (gflex/flexure.py lines 290-300).
- Badlands: flexure time step ftime passed to isoFlex (isoFlex.py docstring lines 90-95).
- Iteration to handle sea level: gFlex README (line ~226-228) says loads below sea level require an iterative fill approach, and the buoyancy of the fill changes the solution.

## C11. Assessment for a Python tool (2000 x 1000, 5-20 km cells, planar or spherical)

1. Easiest to reimplement: constant-Te FFT flexure (gFlex 1.4 FFT, GMT grdflexure). The Fourier operator w(k) = q(k) / (D k^4 + Drho g) is a few lines with numpy.fft.rfft2 and padding. Cost about 0.1 s per solve for 2e6 cells. Limitation: uniform Te, planar (Cartesian).
2. Easiest to call directly: gFlex 1.x (PyPI 1.3.0, GPL-3.0). Supports FD with variable Te, FFT, SAS. Install is pip-only and pure Python plus SciPy. Watch for the 2.0 API changes if you move to 2.0. GPL-3 license applies to the code you link or copy.
3. Variable Te with planar grid: reimplement the FD biharmonic (sparse matrix, 13-point stencil for D nabla^4, with variable D as in gFlex's FD and the goSPL FV form D inside Lm diag(D) Lm). Sparse direct factorisation of a 2e6 system is heavy. Alternative: iterative solver with the cached preconditioner, or the FFT-based variable-Te iteration (goSPL "global" uses Picard with Anderson, reusable idea). UNVERIFIED performance.
4. Spherical: goSPL's spectral thin-shell operator (pyshtools on DH grid, with the caveat about bending-only terms) is the only code found that does global flexure. It runs serially and needs pyshtools and a DH grid of about 1000 x 2000 for 5 km cells at Earth scale. For a continental window (60N to 7S), a rotated or projected planar domain is simpler, with the low-degree error documented.
5. Not recommended: Landlab Flexure direct sum for a 2e6 cell grid (cost scales with loads x grid).
6. Not applicable: fastscapelib Python (no flexure), pyGPlates (not checked in detail; the local clone contains only rotation data and gplately notebooks, no flexure code found by grep), Fastscapelib Fortran flexure (optional, uniform Te, stale since 2024).

## URLs read

- https://github.com/awickert/gFlex (clone, commit c147574)
- https://github.com/awickert/gFlex/blob/master/README.md
- https://github.com/awickert/gFlex/blob/master/CHANGES.md
- https://github.com/awickert/gFlex/blob/master/pyproject.toml
- https://github.com/awickert/gFlex/blob/master/docs/theory_and_numerics.rst
- https://github.com/awickert/gFlex/blob/master/docs/benchmarks.rst
- https://github.com/awickert/gFlex/blob/master/docs/configuration.rst
- https://github.com/awickert/gFlex/blob/master/gflex/base.py
- https://pypi.org/pypi/gflex/json
- https://pypi.org/pypi/landlab/json
- https://pypi.org/pypi/gospl/json
- https://pypi.org/pypi/fastscapelib/json
- https://pypi.org/pypi/pyshtools/json
- https://pypi.org/pypi/shtools/json (old unrelated package, checked only for existence)
- https://api.anaconda.org/package/conda-forge/gflex
- https://api.anaconda.org/package/conda-forge/landlab
- https://github.com/landlab/landlab (clone, commit 5fa0cf1): src/landlab/components/flexure/*, src/landlab/components/gflex/flexure.py, LICENSE.md, pyproject.toml
- https://github.com/Geodels/goSPL (clone, commit 17fc4c6): gospl/tools/addprocess.py, gospl/tools/inputparser.py, gospl/model.py, benchmarks/test_flexure.py, docs/DUAL_LITHOLOGY_SUMMARY.md, docs/user_guide/hpc_scaling.rst, LICENSE, pyproject.toml
- https://github.com/fastscape-lem/fastscapelib-fortran (clone, commit 45f9036): CMakeLists.txt, setup.py, docs/api.adoc, docs/release_notes.adoc, examples/flexure_test.f90 (not run)
- https://github.com/fastscape-lem/fastscapelib (clone, grep only)
- https://github.com/SHTOOLS/SHTOOLS (clone, grep only)
- Badlands: local clone (origin URL not recorded, so not cited as a URL), commit 975f595 (2026-05-01): src/badlands/forcing/isoFlex.py, COPYING
- https://github.com/danigeos/tisc (clone, commit 04ab59d): README.md, tisc/README.md, tisc/doc/TISC_Documentation.md, tisc/doc/LIMITATIONS.md, tisc/doc/LICENSE.txt, tao/doc/tAo_Documentation.md, tisc/src/tisc.c (grep)
- https://gmd.copernicus.org/articles/9/997/2016/gmd-9-997-2016.pdf (Wickert 2016, PDF via curl and pdftotext)
- https://arxiv.org/pdf/0704.1627 (Beuthe, thin elastic shells; PDF via curl and pdftotext)
- https://arxiv.org/abs/0704.1627 (abstract page via oku.py)
- https://gmd.copernicus.org/articles/9/997/2016/ (article page via oku.py; short text)
- https://docs.generic-mapping-tools.org/6.3/supplements/potential/grdflexure.html

## Failed fetches and gaps

- Brotchie and Silvester (1969) original paper: not found by search; only secondary description (Beuthe 2007) was read. Equation form UNVERIFIED.
- Wieczorek (2007) Treatise chapter text: not read. Only citation and a 2015 revision reference from search snippets. The 2015 PDF at planetarygeoscience.uchicago.edu was not fetched.
- Turcotte et al. (1981) and Willemann and Turcotte (1981): not read. Formulas only as quoted in goSPL's benchmark comments (UNVERIFIED here).
- gFlex 2.0 2D FD discretisation details (stencil) were not confirmed beyond docs.
- Pecube: search returned no flexure information. Source not checked. Status: UNVERIFIED whether Pecube has flexure.
- Cascade (Braun): CSDMS wiki page https://csdms.colorado.edu/wiki/Model:CASCADE appeared in search results only (snippet says flexural isostasy included). Code not inspected; language and license UNVERIFIED.
- "tAo" as a separate project: it lives inside the danigeos/tisc repository (checked). No separate tAo repository was searched.
- TISC 2002 Garcia-Castellanos reference and "finite element" claim: a search snippet could not confirm either. The C source flexure solver was not identified (only the -s m "mathlib" option is documented).
- Search for TISC returned a GitHub mirror (github-users.yhajoa.workers.dev), which was not used; the official clone was used instead.
- Search results for a planar vs spherical domain criterion gave no numeric threshold; the threshold in C8 is my own estimate.
- Shell-curvature Brotchie-Silvester equation and goSPL operator not re-derived here; the discrepancy is quoted from goSPL's own benchmark comments.
- The goSPL clone HEAD is dated 2026-11-12, one day after the research date (2026-11-11). Treated as anomalous; version info taken from PyPI.
- No benchmarks were run locally (instructions: read only, do not run untrusted code).

## Key takeaways for the tool

1. Constant Te: use an FFT (numpy rfft2) solution, w(k) = q(k) / (D k^4 + Drho g), with zero or periodic padding. Cost about 0.1 s for 2e6 cells (extrapolated from 40 ms at 1000 x 1000 in gFlex docs). Planar only.
2. Variable Te on a planar grid: a sparse FD biharmonic system with a cached factorisation (gFlex FD). Cost is dominated by the factorisation (extrapolated minutes for 2e6 cells; UNVERIFIED). Reuse the factorisation when Te does not change (gFlex cache_factorization gives 7-12x at 400 x 400). Use padding of Te (gFlex pad_domain helpers) to limit edge artefacts.
3. Do not use the Landlab direct-sum Flexure for a 2000 x 1000 grid with many loads. Its cost is N_loads x N_grid.
4. For a global or continental-scale domain, the planar approximation is adequate for flexural wavelengths of about 300 km (Te 30 km) except for the lowest spherical degrees (l < about 10). Project the domain (e.g., an equal-area or Lambert projection) before using planar solvers, and keep the lat/lon cell-size variation in mind (dx shrinks by cos(lat)).
5. gFlex (GPL-3.0) is the most complete documented option (FD, FFT, SAS, SAS_NG, BCs, variable Te, in-plane stress, latlon input), with PyPI 1.3.0 stable and 2.0.0b2 beta (2026-07). The 2.0 beta changes names and removes INI; Badlands shows the older API.
6. The only spherical flexure code found is goSPL (pyshtools, DH grid, serial). Its shell operator is bending-only; its own notes say it differs from the full thin-shell response at degrees below about 10 by 4 to 12 percent. Use it as a reference for the spherical approach, not as an exact spherical shell.
7. Density choices: rho_m 3300 kg/m3 (goSPL rhoa, gFlex rho_m); load density 2300 kg/m3 for sediment (goSPL rhoc); infill air (0) or water (1030) per setting (gFlex rho_fill). For sea-level loads, an iterative fill approach is needed (gFlex README).
8. Update interval: goSPL solves every `interval` steps and accumulates the load (default 1). Flexure is typically solved to steady state each update.
9. Code licenses: gFlex, goSPL, TISC, tAo, fsf are GPL-3.0; Landlab is MIT. Reimplementing the algorithm from papers avoids the GPL obligation for the new tool; copying code would bring it in.
10. Maintenance: gFlex (July 2026), Landlab (Nov 2026), goSPL (July to Nov 2026), TISC (Nov 2026), Fastscapelib Fortran (last commit Nov 2024, stale), fastscapelib Python (June 2025, no flexure), Badlands (May 2026, gFlex 1.x API).
