# goSPL: Tectonic Forcing (Plate Motion and Uplift Input) Research Notes

Status: COMPLETE for the scope below. Open items are listed at the end.

Labels: [B] full text read, [B-öz] summary of full text, [D] official documentation, [Ö] search-result summary only.
Access notes:
- WebFetch returned ENOTFOUND for gospl.readthedocs.io. The same pages were downloaded with curl (HTTP 200) and converted with oku.py.
- github.com and api.github.com returned 403 to curl. raw.githubusercontent.com worked for the goSPL LICENSE and the goSPL-examples README.
- science.org returned 403 to curl (ERİŞİLEMEDİ, not accessible).
- pmc.ncbi.nlm.nih.gov returned a bot-check page (ERİŞİLEMEDİ). The check was not bypassed.
- pyGPlates / gospl-pygplates example: BULUNAMADI (not found).

## Source list

- S1 [D] goSPL, Tectonic forcing (dev docs): https://gospl.readthedocs.io/en/dev/tech_guide/tecto.html
- S2 [D] goSPL, Tectonic related parameters (user guide, optfile2): https://gospl.readthedocs.io/en/latest/user_guide/optfile2.html
- S3 [D] goSPL, Required input file parameters: https://gospl.readthedocs.io/en/latest/user_guide/inputfile.html
- S4 [D] goSPL, HPC scaling and performance: https://gospl.readthedocs.io/en/latest/user_guide/hpc_scaling.html
- S5 [D] goSPL, Installation via Conda: https://gospl.readthedocs.io/en/latest/getting_started/installConda.html
- S6 [D] goSPL docs root (version 2026.7.14, research examples list): https://gospl.readthedocs.io/en/latest/
- S7 [B] goSPL-examples README (raw): https://raw.githubusercontent.com/Geodels/goSPL-examples/main/README.md
- S8 [B] goSPL GPLv3 LICENSE (raw): https://raw.githubusercontent.com/Geodels/gospl/master/LICENSE
- S9 [B] PyPI metadata for gospl 2026.7.14: https://pypi.org/pypi/gospl/json
- S10 [B] Salles et al. 2023, Nature 624:115-121, "Landscape dynamics and the Phanerozoic diversification of the biosphere": https://www.nature.com/articles/s41586-023-06777-z
- S11 [B] Salles et al. 2024, Nature Communications 15:3430, "Physiography, foraging mobility, and the first peopling of Sahul": https://www.nature.com/articles/s41467-024-47662-1
- S12 [B-öz] Braun, Tectonophysics 2012 (PECUBE review): https://www.isterre.fr/IMG/pdf/Braun-Tectonophysics2012.pdf
- S13 [D] Badlands README (raw, master): https://raw.githubusercontent.com/badlands-model/badlands/master/README.md
- S14 [D] Badlands docs (build dated 2023-05-02; older than current): https://badlands.readthedocs.io/en/latest/ (xml.html, social.html, install.html)
- S15 [Ö] Salles et al. 2020, JOSS 5(56):2804 (goSPL software paper): https://joss.theoj.org/papers/10.21105/joss.02804.pdf (listed in S6; PDF reachable, not read in full)
- S16 [Ö] Search summary on Science 2023 paper (doi 10.1126/science.add2541): not read directly, see Section 3.
- S17 [Ö] Search summaries on pyGPlates and Pecube (no goSPL-specific content).

## 1. Tectonic forcing: vertical and horizontal input

- [D] S1: Tectonic forcing is user-defined. goSPL does not know whether it is lithospheric or mantle-driven and does not model crustal shortening or sediment compaction.
- [D] S2: The `tectonics:` block is a list of events. Each event has `start` and `end` (years) and either `upsub` (vertical only) or `hdisp` (3D displacement rates). Rates are in m/yr.
- [D] S2 example: `upsub: ['data/uplift20Ma','t']` (key `t`, one value per node, m/yr). `hdisp: ['data/hdisp18Ma','hxyz']` (key `hxyz`, 3D array with x, y, z components, m/yr; for 2D grids the z component is 0.0).
- [D] S3 and S2: Every input file must be a numpy zip archive (`.npz`). NetCDF or HDF5 is not an input format. Outputs are HDF5 with an XDMF descriptor (S4 / user guide outputs page).
- [D] S3: Model time keys are `start`, `end`, `dt` (implicit internal step), `tout` (output interval), `strat` (stratigraphic record interval), `rstep` (restart step). All times are in years.
- [D] S3: `advect` is set in the `domain:` block and takes `upwind`, `iioe1`, `iioe2` or `interp`.
- [D] S2: With `interp` (typically global plate motion), horizontal displacement is applied only at the event `end` time. Other schemes apply horizontal displacement at every `dt`. Vertical displacement is always applied every `dt`.
- [D] S1: `interp` events typically span "several thousands to millions of years".
- [D] S1: `upwind` and `iioe` were designed for 2D meshes. Surface advection on the global sphere is "has not been validated".
- [D] S1: With `interp`, the mesh is not remeshed. Advected points are interpolated back onto the fixed initial mesh with inverse-distance weighting from the three nearest advected points (SciPy cKDTree). A node that coincides with an advected point takes its value exactly. The docs call this efficient but "might not be the most accurate". Node density changes over time, and the docs note remeshing would be needed for strict accuracy.
- [D] S1: Stratigraphic layers are moved semi-Lagrangian after each surface step, not advected individually. Interpolation is not mass conservative; surface and layer totals can drift apart over long runs with strong motion. Layer moving costs about 3% of run time on a 1M-node mesh with a layer written every step.
- [D] S1: Cyclic 2D models run in serial (one MPI rank).
- [D] S1 and S2: Flexure is solved by `method: 'fem'` for 2D and `method: 'global'` (spherical harmonics, via pyshtools, run on the root rank) for global models.
- [D] S3: Planet `radius` (default 6378137.0 m) and `gravity` (default 9.81 m/s2) can be overridden.

## 2. Plate motion on the grid and the GPlates link

- [D] S1: For global meshes, horizontal advection "often corresponds to plate motions and can be obtained from plate-tectonic reconstruction software." The docs do not name GPlates or pyGPlates in the fetched pages.
- [B] S10 (Nature 2023): goSPL inputs are generated from palaeo-elevation maps "consistently tied to a plate tectonic model". The text uses 108 PALEOMAP maps spaced about 5 Myr apart, from the Holocene back to 541 Ma, on a 0.1 x 0.1 degree grid (about 10 km at the equator). The maps are resampled onto the icosahedral mesh. The Nature text does not describe a horizontal advection step in the sections read.
- [D] S7 (examples README): example `plate_mvt` is listed as "Global landscape evolution driven by horizontal plate motion (advection) together with vertical tectonics." The example files were not retrievable (raw paths returned 404 for guessed names).
- gospl-pygplates example: BULUNAMADI. Search (S17) found only general pyGPlates material. No goSPL-pyGPlates script was confirmed.
- Open point: whether plate_mvt uses pyGPlates or a precomputed velocity .npz.

## 3. Example uses: grid size, run time, cores, memory

Benchmarks (S4, HPC scaling, Gadi 48-core nodes; fixed number of steps, I/O off):

| Mesh | Nodes | Faces | Min ranks baseline | RSS per rank | Notes |
|---|---|---|---|---|---|
| 10 km | 5.9 M | 11.8 M | 16 | ~6.6 GB | 16 ranks: 521.3 s; 240 ranks: 46.9 s (speedup 11.1, efficiency 0.74); 288: 44.4 s |
| 8 km | 9.2 M | 18.5 M | 24 | ~9.9 GB | 24 ranks: 800.7 s; 96 ranks: 194.7 s |
| 5 km | 23.7 M | 47.3 M | 96 | ~24 GB on rank 0 (average ~3 GB) | 48 ranks on one 192 GB node is OOM-killed (S4) |

- [D] S4: A global mesh cannot start below these rank counts because of memory. Per-rank memory is replicated and stays roughly flat with rank count.
- [B] S10 (Nature 2023, Phanerozoic run): icosahedral mesh with more than 10 million nodes and 21 million cells, about 5 km average resolution. Each time slice used 168 CPUs. Simulation 1 covered 2 Myr with prescribed elevation and runoff. Simulation 2 added tectonic forcing and ran until erosion balanced uplift, reached within the first 1 Myr. Wall-clock time and memory are not reported in the text read.
- Consistency check: the 5 km benchmark needs at least 96 ranks (S4). The 168-CPU run in S10 is above that minimum. The S10 node count (>10 M nodes) does not match any S4 mesh row exactly, so the mesh definition is not identical.
- [B] S11 (Nature Comms 2024, Sahul): regional model at about 1 km resolution, forward from 75 to 35 ka, outputs every 1 kyr, run on 80 CPUs. Rock uplift is set to 0 (U = 0 m/yr); forcing is sea level and paleo-precipitation.
- Science 2023 (S16, doi 10.1126/science.add2541, "Hundred million years of landscape dynamics from catchment to global scale"): ERİŞİLEMEDİ (science.org returned 403). Search summary only [Ö]: resolution down to about 10 km; frames of 1 Myr; output maps every 5 Myr; "several hundred processors" and "several days" per simulation. These are unverified search-summary figures.
- Naming check against the request: the request refers to a "Salles 2023 Earth system landscape" and a "Salles 2024 paleo-erosion" study. The actual titles are "Landscape dynamics and the Phanerozoic diversification of the biosphere" (Nature 2023, S10) and "Physiography, foraging mobility, and the first peopling of Sahul" (Nature Comms 2024, S11). The 2023 Science paper is the "Hundred million years" study above. The request's "gospl ... Computers & Geosciences or Earth Surface Dynamics" 2023 software paper was not found: the software paper is Salles, Mallard, Zahirovic (2020), JOSS 5(56):2804 (S6, S15). BULUNAMADI for a separate 2023 software paper.
- [D] S6 research list also includes: Husson et al. 2022 (Sci. Rep.), Hadler Boggiani et al. 2025 (ESurf), Lorcery et al. 2025 (PLOS ONE), Salles et al. 2025 (PNAS), Hadler Boggiani et al. 2026 (JGR Earth Surface). Not read.
- The global "Cenozoic" simulation mentioned in the request was not identified. Mesh, time and core details for it: BULUNAMADI.

## 4. Comparison with Badlands and Pecube

Badlands:
- [D] S13 and S14: Python code, LGPL v3 licence (the README and the social.html page both say LGPL). Processes include diffusion, stream power, transport, marine deposition, reef growth, turbidity currents, and tectonic horizontal and vertical displacement, plus rainfall and sea-level forcing.
- [D] S14 (xml.html): Tectonics is set in an XML `<tectonic>` block. `<disp3d>` is 0 for vertical only or 1 for 3D. Vertical displacement uses an ASCII 1-column file in the same node order as the topography grid, with `<dstart>` and `<dend>` in years. For 3D, the displacement file has 3 columns (x, y, z), `<merge3d>` sets the node merge distance, and `<time3d>` splits long periods into shorter intervals. The docs cite Thieulot et al. (2014) for the 3D method.
- [D] S14: Input topography is a regular DEM CSV (e.g. `data/regularMR.csv`). The surface is a triangulated irregular network (TIN) that is remeshed when horizontal displacement is on.
- Difference from goSPL: Badlands is regional and works on a TIN with remeshing. goSPL is global and spherical, uses a fixed icosahedral mesh with interpolation, and takes .npz inputs. Badlands uses XML and CSV/ASCII inputs.
- Caveat: the Badlands docs build is dated 2023-05-02. Current behaviour may differ.

PECUBE:
- [B-öz] S12 (Braun 2012 review): PECUBE is a three-dimensional thermal-kinematic finite-element code. It solves heat production, diffusion and advection under a time-varying surface. It predicts thermochronometric ages by tracking rock-particle time-temperature paths. Reported features include fault-controlled kinematics (fault geometry, slip rates), time-varying topography, subsurface (tunnel or borehole) prediction, detrital thermochronology, and inverse modelling with the Neighbourhood Algorithm.
- [B-öz] S12: "PECUBE explicitly decouples rock uplift from surface evolution." The rock-uplift rate is defined with respect to the base of the model.
- [Ö] S17: Pecube was originally developed by Jean Braun (2003). A modified version, Pecube-D, is maintained by Ehlers' group.
- Difference from goSPL: PECUBE is a regional thermochronology (age-prediction) tool. Its outputs are cooling ages and temperature histories, not sediment fluxes or stratigraphy. Its kinematic inputs are fault and velocity-field descriptions, not global plate-reconstruction grids. goSPL is a global landscape and sediment-routing model.
- Pecube licence and current repository: BULUNAMADI. github.com/Pecube returned 403 to curl.

## 5. Licence, installation, and GitHub Actions suitability

- [B] S8: goSPL is licensed under GNU GPL v3. S9 (PyPI) lists license "GNU GENERAL PUBLIC LICENSE Version 3".
- [D] S5: Conda install is `mamba create -n gospl -c geodels -c conda-forge gospl`. `-c conda-forge` is required so that petsc4py, mpi4py, pyshtools and vtk resolve. The docs list release tags from v2026.06.08 to v2026.7.14.
- [D] HPC install page (getting_started/installHPC, text in working copy): requires Intel MPI, HDF5, PETSc 3.21.3, netCDF, MKL, Python 3.11 modules. h5py and HDF5 must be MPI-linked for collective writes; a non-MPI h5py silently breaks this. A known issue exists with parallel HDF5 writes inside Singularity on Setonix.
- [D] S7 (examples README): recommends mamba or micromamba. Docker image `geodels/gospl-examples` is available. Example runs use `mpirun -np 4 gospl -i input-strati.yml`.
- [D] S7: The devcontainer requests a 4-core, 8 GB machine. The README warns that "some of the global examples are memory-hungry" and that free GitHub Codespaces accounts may be capped at 2 cores.
- Feasibility for a GitHub Actions runner (2 to 4 cores, 16 GB, as stated in the request; runner specs were not verified):
  - 10 km global mesh: needs at least 16 ranks; about 6.6 GB per rank at 16 ranks (about 105 GB total). Not feasible on 2 to 4 cores with 16 GB.
  - 8 km: needs 24 ranks minimum (about 9.9 GB per rank). Not feasible.
  - 5 km: needs 96 ranks minimum (about 24 GB on rank 0). Not feasible.
  - Global example `plate_mvt` memory and mesh size: BULUNAMADI. Likely infeasible on 16 GB if it uses a global mesh of comparable size (inference, not verified).
  - Local/2D examples (e.g. `generate_2Dmesh`, `flow_direction`, `implicit_timestepping` as listed in S7): not tested for memory or time. Likely feasible for small meshes, but unverified.
  - Cyclic 2D runs are serial only (S1).
- Other constraints: MPI-linked HDF5 is required for parallel output, so a plain pip install may not support full parallel I/O. The benchmark runs used 192 GB nodes; no CI-sized benchmark was found.

## Open items (not resolved in this pass)

1. gospl-pygplates example: BULUNAMADI. Need the goSPL-examples plate_mvt folder contents (raw paths 404 for guessed names; a directory listing would be needed).
2. Science 2023 full text: ERİŞİLEMEDİ (403). Needs a legitimate access route.
3. Memory and wall time for the Nature 2023 run: not in the text read; supplementary material not retrieved.
4. Badlands current docs (2023 build) and any newer version: not checked.
5. Pecube licence and current repository: not checked (github.com 403).
6. The 2020 JOSS software paper (S15) was not read in full.
