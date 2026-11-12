# Procedural terrain from tectonic uplift and erosion: research notes

Status: research pass complete. Labels: [B] = full text read; [B-öz] = abstract/metadata read; [Ö] = search snippet only; BULUNAMADI = not found; ERİŞİLEMEDİ = could not access.

## Source status

| # | Paper | Label | Note |
|---|---|---|---|
| 1 | Cordonnier et al. 2016, CGF 35(2) (Eurographics 2016) | [B] | PDF via curl, extracted with pdftotext |
| 2 | Cortial et al. 2019, "Procedural Tectonic Planets", CGF 38(2) | [B-öz] | Full PDF behind DSpace login: ERİŞİLEMEDİ |
| 3 | Schott et al. 2023, ACM TOG 42(5) | [B] | HAL preprint hal-04049125 via curl, 16 pages |
| 4 | Tzathas et al. 2024, "Physically-based Analytical Erosion for fast Terrain Generation", CGF 43(2) | [Ö] | Full PDF behind DSpace login: ERİŞİLEMEDİ. Requested titles "Orometry-based..." and "orogenic sketching" not found as such (see below) |
| 5a | Génevaux et al. 2013, "Terrain Generation Using Procedural Models Based on Hydrology", ACM TOG 32(4) | [B] | HAL PDF via curl |
| 5b | Guérin et al. 2022 STAR "Procedural terrain" | BULUNAMADI | Closest match is "Gradient Terrain Authoring" (EG 2022, CGF 41(2)), a regular paper, read as [B] (see 5c) |
| 5c | Guérin et al. 2022, "Gradient Terrain Authoring", CGF 41(2) | [B] | PDF via curl from UCT site |

Note on the request list: "Orometry-based terrain analysis and synthesis" is Argudo et al. 2019 (SIGGRAPH Asia), not Tzathas. "Orogenic sketching" returned nothing (BULUNAMADI). The closest 2019 STAR is Galin et al., "A Review of Digital Terrain Modeling" (CGF 38(2), 2019), seen only in search [Ö].

---

## 1. Cordonnier et al. 2016 [B]

Citation: G. Cordonnier, J. Braun, M.-P. Cani, B. Benes, É. Galin, A. Peytavie, É. Guérin. "Large Scale Terrain Generation from Tectonic Uplift and Fluvial Erosion." Computer Graphics Forum 35(2), Eurographics 2016. DOI 10.1111/cgf.12820.

- **Input:** A grayscale uplift map U, painted by the user. It sets the simulation domain and how fast mountains grow. Treated as a piecewise uniform distribution over the domain Ω.
- **Model (Eq. 1):** dh/dt = u(p) − k·A(p)^m · s(p)^n, where h = elevation, u = uplift, k = erosion coefficient, A = drainage area, s = slope (∇h).
- **Parameters:** n = 1 and m = 0.5 ("as in most geomorphological studies"). The paper says only the ratio m/n matters, and gives m/n ≈ 0.5 as a geological constraint.
- **Experimental values (Section 6):** Terrain 50 × 50 km². Maximum uplift U = 5.0·10⁻⁴ m/yr (average of Earth's mountains). Erosion coefficient k = 5.61·10⁻⁷ 1/yr, chosen so mountains peak near 2000 m. Geological time step δt = 2.5·10⁵ yr.
- **Height rule (Section 6.4):** Experiments gave a linear relation hmax = 2.244·u/k (height in km). The uplift-to-erosion ratio alone sets peak height.
- **Resolution / representation:** Vector representation. Poisson-distributed sample points, Delaunay triangulation, stream graph. Samples: 10k to 160k. Final heightfield built by blending Gaussian kernels.
- **Timing (Table 1; Intel i7 3 GHz, 16 GB RAM, C++/OpenGL):**
  - 10,000 samples: 0.031 s/step, 6.4 s to converge
  - 40,000 samples: 0.177 s/step, 35.4 s
  - 90,000 samples: 0.401 s/step, 78.0 s
  - 160,000 samples: 1.273 s/step, 252.0 s
  - Convergence takes roughly 100–300 steps.
- **Solver:** Implicit scheme with large time steps. Iterations are needed because stream-tree connectivity changes. Slopes capped at 30°.
- **Limitations (stated by authors):** Validation is visual only, with no human-subject study. Geological meaning of parameters is not well understood. Sediment deposition is neglected. Only fluvial erosion is modeled (no glacial, hillslope, or alluvial processes). Uplift maps are not generated automatically from plate tectonics (listed as future work). Implementation not optimized.
- **Code/data:** No code or data availability statement in the paper. A video is referenced. Open code: BULUNAMADI (from this text).
- **Real data:** Section 6.1 compares against a real dataset ("Real dataset"); the dataset name is cut off in the extracted text, so I did not record it.

## 2. Cortial et al. 2019, "Procedural Tectonic Planets" [B-öz]

Citation: Y. Cortial, A. Peytavie, É. Galin, É. Guérin. Computer Graphics Forum 38(2), 2019. DOI 10.1111/cgf.13614.

- **Abstract (from the Eurographics DL record):** Procedural authoring of synthetic tectonic planets. Avoids costly physical simulation by capturing the large-scale effects of plate movement and collision. Subduction and collision deform the lithosphere (continental and oceanic crust). The user steers plate motion, which evolves over time and produces continents, oceanic ridges, mountain ranges, and island arcs. The planet-scale model is then detailed with procedural or real elevation data. The user can trigger events such as catastrophic plate rifting.
- **Input type:** Plate motion parameters and interactive steering. Plate-based, not a painted uplift map.
- **Equations, parameter values, resolution, timing, limitations, code:** Not verified. The full PDF needs a login (ERİŞİLEMEDİ). Open PDF or code: BULUNAMADI.

## 3. Schott et al. 2023, "Large-scale Terrain Authoring through Interactive Erosion Simulation" [B]

Citation: H. Schott, A. Paris, L. Fournier, É. Guérin, É. Galin. ACM TOG 42(5), article 162, SIGGRAPH 2023. DOI 10.1145/3592787.

- **Input:** Uplift u = u₀ + ũ.
  - u₀ = static part, built from an "Uplift Tree": a hierarchical vector construction from brushes (skeletal primitives and operators).
  - ũ = dynamic correction that enforces elevation constraints (peaks, ridges, valley points and curves). Implemented as a PI-style controller with Kp = 0.01, Kd = 0.01, Ki = 0.001, updated every 10 iterations.
  - Alternatives: inverse procedural modeling, which reconstructs uplift from a DEM or from ridge and river networks.
- **Model (Eq. 1):** ∂h/∂t = u − s^n·a^m + Δh. a = drainage area, Δh = hillslope diffusion (Laplacian). K is not written explicitly (effectively 1). Only m/n matters; set to ≈ 1/2.
- **Drainage area approximation:** Incremental and parallel. Uses flow routing with a 5×5 local window and a p = ∞ steepest-slope distribution over 8 neighbors. Cells are not sorted by elevation, so it parallelizes on GPU.
- **Resolution:** Regular grid, explicit integration. Cell size 80–600 m. Test terrains 100 × 100 km² to 1000 × 1000 km². Higher detail via sparse amplification (×8), as in Figure 1.
- **Timing (Table 1; Intel i7 4 GHz, 16 GB RAM, NVIDIA GTX 1080 Ti, GLSL compute shaders):**

  | Grid | Steps | ms/step | Total (s) |
  |---|---|---|---|
  | 256² | 5k | 0.1 | 0.5 |
  | 512² | 5k | 0.3 | 1.3 |
  | 1024² | 11k | 0.8 | 9.1 |
  | 2048² | 39k | 3.3 | 128 |
  | 4096² | 81k | 12.5 | 1036 |

  - Authors compare with Cordonnier 2016: on a 160k-point graph (~400×400), that method takes ~252 s; this method takes ~1.3 s on 512×512. Caveat: hardware differs (CPU-only 3 GHz vs. 4 GHz CPU + GPU), so the comparison is not like-for-like.
- **Time-step heuristic:** Δt grows ×1.01 when the pit-cell count falls, and shrinks ×0.75 when it rises sharply.
- **Limitations (authors):** Conflicting elevation constraints placed close together can cause instability. The CPU-side correction term slows updates (authors suggest moving it to GPU). Convergence slows above 1024². Sediment deposition is absent, which the paper ties to low valley variety in inverse modeling (Section 6.1). The authors also say Cordonnier 2018's tectonic folding approach is indirect and not suited to authoring.
- **Code:** Erosion simulation code is publicly linked at github.com/HSchott/StreamPowerErosion (in the paper and the author page). The GitHub repository could not be accessed in this session, so its contents are not verified. Project page links also include a PDF, video, and code.

## 4. Tzathas et al. 2024, "Physically-based Analytical Erosion for fast Terrain Generation" [Ö]

Citation: P. Tzathas, B. Gailleton, P. Steer, G. Cordonnier. CGF 43(2), Eurographics 2024. DOI 10.1111/cgf.15033.

- **Summary (from search snippets only):** Analytical solutions of the stream power law, which describes uplift competing with fluvial erosion. Time becomes a parameter of a closed-form function, not a stopping criterion for an iterative simulation. Adds landslide and hillslope processes. Described as physically based and procedural, with fast large-scale generation.
- **Full text:** The PDF on the Eurographics DL requires login (ERİŞİLEMEDİ). No arXiv or HAL preprint found.
- **Equations, parameters, resolution, timing, limitations, code:** Not verified (full text required).
- **Related but different:** "Orometry-based terrain analysis and synthesis" is Argudo et al. 2019 (SIGGRAPH Asia), a peak-and-saddle graph method. "Orogenic sketching" BULUNAMADI.

## 5a. Génevaux et al. 2013, "Terrain Generation Using Procedural Models Based on Hydrology" [B]

Citation: J.-D. Génevaux, É. Galin, É. Guérin, A. Peytavie, B. Beneš. ACM TOG 32(4), article 143, SIGGRAPH 2013. DOI 10.1145/2461912.2461996.

- **Input:** Not uplift-based. The user provides the domain contour, river mouths, a few river sketches, and slope maps (terrain slope and river slope). Also a set of intuitive parameters.
- **Method:** Hydrology-inspired. A river graph grows from seeds on the contour and sketched rivers, using Horton–Strahler ordering. River types follow the Rosgen classification. Multi-scale hierarchical hybrid representation built from primitives (watersheds, cells).
- **Equations / constants:** No erosion PDE. Rules are in the form of expansion rules (Table 1). Minimum spacing between rivers σ = 3/4 · e = 1500 m. Parameter ζ ∈ [0, ∞) controls network length. Terrain noise: Perlin noise for roughness.
- **Resolution:** Vector/analytic, unlimited detail (multi-resolution). Evaluation at 1024 × 1024 samples for meshing.
- **Timing (Table 2; Intel i7 3 GHz, 16 GB RAM):**

  | Figure | Graph (1), s | Cells (2), s | Tree (3), s | Mesh (4), s |
  |---|---|---|---|---|
  | 17 A | 4.0 | 0.9 | 4.7 | 1.0 |
  | 17 B (3368 km² island) | 5.3 | 1.1 | 4.9 | 1.2 |
  | 18 | 0.1 | 0.1 | 1.8 | 1.0 |
  | 19 | 0.2 | 0.2 | 4.2 | 0.7 |
  | 20 | 0.6 | 0.4 | 4.6 | 1.0 |
  | 22 | 0.5 | 0.4 | 4.8 | 0.8 |

  - Authors: "several hundreds of square kilometers … in a few seconds." Island case: 81,853 primitives, ~8 MB (text reads "8, 180 kB").
- **Limitations (authors):** Only terrains that were once shaped by hydraulic erosion can be generated (dry terrain is possible by removing river beds). River networks subdivide only upstream, so deltas and oxbow lakes are not represented. Greedy construction can produce meandering crests and unnatural hills. Large mountains lack articulated valleys; flat rivers may cut through high mountains. Many parameters can produce unnatural terrain. Balance between user and system control left as future work.
- **Code:** The paper has no code availability statement. A third-party unofficial implementation exists on GitHub (wattzhikang/terrainHydrology), per search only [Ö]. Official code: BULUNAMADI.

## 5b. Guérin et al. 2022 STAR "Procedural terrain": BULUNAMADI

- Searches found no 2022 Eurographics STAR by Guérin on procedural terrain.
- Closest 2019 STAR (search only [Ö]): Galin, Guérin, Peytavie, Cordonnier et al., "A Review of Digital Terrain Modeling", CGF 38(2), 553–577, DOI 10.1111/cgf.13657.
- A 2025 STAR by Argudo, Guérin, Schott, Galin ("Terrain descriptors for landscape synthesis, analysis and simulation", CGF 44(2)) also surfaced [Ö]. It is about terrain metrics, not generation.

## 5c. Guérin et al. 2022, "Gradient Terrain Authoring" [B]

Citation: É. Guérin, A. Peytavie, S. Masnou, J. Digne, B. Sauvage, J. Gain, É. Galin. CGF 41(2), Eurographics 2022. DOI 10.1111/cgf.14460.

- **Approach:** Works in the gradient (slope) domain instead of elevation. Height-independent representation for blending procedural, simulated, and real terrain patches. Elevation is recovered by Poisson reconstruction with Dirichlet constraints (points and curves). Supports cut-and-paste with warping, painting brushes, and sketched elevation and gradient constraints.
- **Relation to uplift work:** Compares with geomorphological simulation (tectonic uplift and erosion). Argues that uplift and erosion tools are indirect for authoring. Provides a hydraulic-erosion brush implemented in the elevation domain as an example of combining tools.
- **Solver:** Half V-cycle multigrid, GPU compute shader. Iterations = 50 + 20·ℓ per level (ℓ counting up from 1 at a 9×9 grid). Grid size 2ⁿ + 1 recommended. Five buffers per level.
- **Timing (Table 1; Intel i7 4 GHz, 32 GB RAM, GTX 970 4 GB):**

  | Grid | Time (ms) | Memory (MB) |
  |---|---|---|
  | 513 × 513 | 27 | 7 |
  | 1025 × 1025 | 68 | 28 |
  | 2049 × 2049 | 275 | 112 |
  | 4097 × 4097 | 1180 | 448 |
  | 8193 × 8193 | 7670 | 1790 |

  - Real-time updates up to 1024 × 1024 are claimed for editing.
- **Super-resolution:** A cGAN was trained on 440 pairs (128² gradient → 512²); amplification up to ×4 (4 m → 1 m).
- **Limitations:** Intersecting or grazing constraints can conflict and produce near-vertical edges. Soft constraints conflicting with hard ones. Tool-control tradeoffs noted in user study.
- **Code:** Multigrid solver source at github.com/eric-guerin/gradient-terrains (paper statement). Not opened in this session.

---

## Cross-paper observations (from the read sources)

- Uplift-driven stream-power models (Cordonnier 2016, Schott 2023) share the same core equation; Schott drops explicit K and uses m/n ≈ 1/2.
- Schott 2023 claims a large speedup over Cordonnier 2016 (1.3 s vs. 252 s for comparable sizes), but the hardware differs.
- Génevaux 2013 is river-network-first and not based on uplift or erosion PDEs. Its timings are on the order of seconds for hundreds of km².
- Guérin 2022 is an authoring/representation paper, not a terrain-generation model. It is the basis for the "gradient domain" alternative to uplift.

## Access and tool notes

- www.cs.purdue.edu and h-schott.github.io: WebFetch returned DNS errors (getaddrinfo ENOTFOUND). curl succeeded for both.
- diglib.eg.org: one bitstream returned an MP4 video; the Cortial PDF bitstream returned a DSpace login page (ERİŞİLEMEDİ). The Tzathas PDF (diglib7) also returned a DSpace login page (ERİŞİLEMEDİ).
- github.com/H-Schott/StreamPowerErosion: session GitHub access not enabled. Not attached (no add_repo call made).
- A proxy-status check was denied by the auto-mode permission classifier; not retried or worked around.
- One curl download to diglib.eg.org failed with a connection reset; retried once and succeeded (for the HTML login page).
- PDFs extracted with pdftotext (layout mode for tables). oku.py was not used because it is for HTML pages.
- Local copies: /tmp/claude-0/-home-user-Tectonic/1cb340b3-df7d-519b-96f4-5170b8cfb37a/scratchpad/dl_cordonnier/, .../dl_schott/, .../dl_genevaux/, .../dl_guerin/.
