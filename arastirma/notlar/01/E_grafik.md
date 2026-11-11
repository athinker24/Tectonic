# E: Computer-graphics research 2016-2026 on geologically grounded large-scale terrain

Research date: 2026-11-11. Sources were read as full text, from the author PDFs on HAL (fetched through the HAL file URL), the Purdue author page or GitLab/GitHub repositories, unless a source is marked otherwise.
The convention for every fact is URL first, then the claim. UNVERIFIED marks anything I could not confirm from a primary source.
PDF text was extracted with pdftotext. Some table numbers did not extract (they were images or the layout broke). Those cases are noted.

Relevance codes: (a) uplift derived from tectonics; (b) fixed land/sea mask or coastline (boundary conditions); (c) inverse modelling; (d) amplification/detail; (e) realism evaluation.

---

## 1. Cordonnier, Braun, Cani, Benes, Galin, Peytavie, Guérin 2016: "Large Scale Terrain Generation from Tectonic Uplift and Fluvial Erosion"
- Venue: Computer Graphics Forum 35(2) (Eurographics 2016), pp. 165-175, DOI 10.1111/cgf.12820. Sources: https://www.cs.purdue.edu/homes/bbenes/papers/Cordonier16CGF.pdf ; HAL file https://inria.hal.science/hal-01262376/file/2016_cordonnier.pdf ; record https://diglib.eg.org/handle/10.1111/cgf12820
- What it does: the user paints an uplift map. Uplift and stream-power fluvial erosion are then simulated on a random planar graph, and the resulting "stream graph" is converted into a DEM. The paper describes itself as the "first method in computer graphics that combines uplift and hydraulic erosion" (Purdue PDF, abstract).
- Inputs/outputs: input is a piecewise-uniform greyscale uplift map U over domain Ω. Output is a stream graph (node elevations, flow directions, drainage), which is rendered by interpolation or Phong tessellation, or by procedural landform primitives [GGP*15] plus amplification [GDPG16] (Purdue PDF §3.2, §6.2).
- Algorithm (Purdue PDF §3-5):
  - Equation: dh/dt = u − k A^m s^n, with n=1 and m=0.5. Nodes come from Poisson sampling over Ω and are joined by Delaunay triangulation. A Voronoi cell area gives each node its own "rain" area.
  - Each iteration has four steps. (1) Each node gets a receiver, its lowest neighbour, which forms stream trees. (2) Lakes (internal roots) are connected through passes, using a lake super-graph built in increasing pass-height order with a red-black tree. This costs O(N + M log M), whereas Braun & Willett's optional step costs O(N√N). (3) Drainage area is accumulated from leaves to roots in O(N). (4) An implicit solve runs from roots to leaves: h_i(t+δt) = [h_i(t) + δt(u_i + kA_i^m/|p_i−p_j| h_j(t+δt))] / (1 + kA_i^m δt/|p_i−p_j|).
  - A thermal correction then limits slopes to 30°. The talus angle can be modulated by Perlin noise (6°-54°) or by height to produce cliffs.
  - Boundary condition: "hk is set constant for nodes lying on the border of the domain Ω. These nodes are tagged as external nodes and serve as river mouths, i.e., points at the sea level". The border is the outlet (Purdue PDF §4.1).
- Parameters and scale: terrain 50×50 km², U_max = 5.0e-4 m/y, k = 5.61e-7 /y, δt = 2.5e5 y. The result converges in about 100-300 steps (mountains are formed by about 50). An empirical relation is h_max (km) = 2.244 u/k (Purdue PDF §6, §6.4).
- Runtime, Table 1 (CPU 3 GHz):
  - 10k samples: 0.031 s/step, 6.4 s total.
  - 40k samples: 0.177 s/step, 35.4 s.
  - 90k samples: 0.401 s/step, 78 s.
  - 160k samples: 1.273 s/step, 252 s.
  - Source: Purdue PDF §6.3.
- Realism: a visual side-by-side with the San Gabriel Mountains (USGS DEM), plus partial visual evaluation by a geologist co-author (Purdue PDF §6.1, §7).
- Code: none found.
- Relevance:
  - (a) Yes, but the uplift is painted, not derived from plates. Future work proposes using "plates-tectonics simulation to automatically compute uplift maps" (§7).
  - (b) The domain border is fixed at sea level. Arbitrary interior masks are not discussed, but the external-node mechanism generalises directly (my inference).
  - (c) No.
  - (d) Via primitives and amplification.
  - (e) Visual and expert only.
- Stated limitations (§7): realism was not evaluated with human subjects; the parameters are poorly understood even in geology; there is no sediment deposition; it models a single erosion process; the implementation is unoptimised. Also, "the actual shape of the uplift does not have a strong influence, except on the boundaries"; the uplift gradient matters most (§6.4).

## 2. Cordonnier, Galin, Gain, Benes, Guérin, Peytavie, Cani 2017: "Authoring Landscapes by Combining Ecosystem and Terrain Erosion Simulation"
- Venue: ACM TOG 36(4) (SIGGRAPH 2017), DOI 10.1145/3072959.3073667. Sources: https://hal.science/hal-01518967/file/authoring-landscapes-combining.pdf ; https://cs.purdue.edu/cgvlab/www/publications/cordonnier2017authoring
- What it does: a layered model (bedrock, broken rock, sand, humus, grass/shrub/tree layers) with event-based simulation of rain/hydraulic erosion, gravity slides, lightning, fire, vegetation growth and death, and two-way coupling between erosion and vegetation (HAL PDF abstract, §3).
- Scale: the time step is 1 year (HAL PDF §3.3). Grids are about 256×256, with cells "about 100 meters" (HAL PDF lines ~205, 384). The paper notes that its correlation-based approach is viable "up to 1 km²" before becoming costly (HAL PDF ~l.708).
- Relevance: low for tectonics. It is not stream-power, uplift or continental scale. It is useful only as a downstream "finishing" layer (d). It does not cover (a), (b) or (c).
- Code: none found.

## 3. Cordonnier, Cani, Benes, Braun, Galin 2018: "Sculpting Mountains: Interactive Terrain Modeling Based on Subsurface Geology"
- Venue: IEEE TVCG 24(5), May 2018, pp. 1756-1769(?), DOI 10.1109/TVCG.2017.2689022. Sources: https://www.cs.purdue.edu/homes/bbenes/papers/Cordonnier18TVCG.pdf ; HAL https://hal.science/hal-01517343/file/paper.pdf
- What it does: the user moves tectonic plates with hand gestures on a multitouch table. A viscous, volume-preserving crust model under compression produces crustal thickening, which becomes an uplift map. Multi-scale folds of a layered stratigraphy refine the uplift, then stream-power erosion and landsliding build the terrain. Folded strata are rendered on cliffs (PDF abstract, §3).
- Algorithm (PDF §4-6):
  - Crust material q sits on a 1024×1024 2D grid and is transported by the rigid motions of the plates. The amount after motion is computed by inverse-mapping the cell corners: q(x_i) = q0·a_i/a_cell.
  - The thickness-change rate dq/dt = (q − q0)/Δt is converted to uplift: u0 = α dq/dt on the deforming side, and u0 = 0 on the stable side of a procedurally placed main fault (an iso-level of q). α is set so that mean uplift = 5.0e-4 m/y.
  - Folds come from fold skeletons. Wavelengths derive from layer thickness and viscosity, in a thin-sheet approximation. These yield a refined uplift u.
  - Erosion uses dz/dt = u − kA^m s^n on a TIN, with n=1, m=0.5 and k ≈ 5.5e-7 /y. A landslide/talus step follows. The implicit, linear-time solve evaluates heights in receiver order.
  - The surface rock type is looked up from the folded layers. Erodibility k and talus angle vary per layer, giving cliffs and cirques (Fig. 20).
- Isostasy: "we neglect isostasy by imposing that the compression-induced shortening results in surface uplift only" (PDF §4.3).
- Scale and runtime:
  - Interactive mode: a 100×100 km² terrain, a 10,000-vertex mesh, about 10 ms per iteration. A 5 My simulation takes 5 iterations. Average authoring rate is over 30 Hz on two CPU threads. The viscous compression takes about 10 ms on the GPU.
  - Offline: about 1,000,000 vertices, about 4 s per step, about 100 iterations (PDF §7).
- Parameters (Table 2): total simulated time 5e6 y; 2-10 layers of 0.1-5 km; fold wavelength 0.5-20 km; k 2.5e-7 to 8e-7; talus 30-50°.
- Evaluation: a user study (usability), plus validation of folds against geological simulations and real terrains. The fold-validation figure uses histograms of fold-normal angles versus compression direction and of wavelengths (PDF §7.3-7.4).
- Code: none found.
- Relevance:
  - (a) Strong. This is the most direct "uplift from plate kinematics" paper: thickening rate leads to uplift, with an asymmetric fault.
  - (b) Not addressed.
  - (c) No.
  - (d) Fold strata texture only.
  - (e) A user study plus geological comparison.
- Limitations (PDF §7.3): the fold model is valid only for early folding stages; there are no secondary faults (a volumetric simulation would be needed); "we do not allow for a plate setup that evolves over time"; it does not support precise editing.

## 4. Cortial, Peytavie, Galin, Guérin 2019: "Procedural Tectonic Planets"
- Venue: Computer Graphics Forum 38(2) (Eurographics 2019), DOI 10.1111/cgf.13614 (confirmed by the EG digital library handle https://diglib.eg.org/handle/10.1111/cgf13614). Source: https://hal.science/hal-02136820/file/2019-Procedural-Tectonic-Planets.pdf (licence on PDF: CC BY-ND 4.0)
- What it does: procedural, non-physical plate tectonics on a sphere. User-controlled plate motions (geodetic rotation axes) cause subduction, continental collision (terrane accretion, slab break), seafloor generation at ridges, and plate rifting. The coarse crust is then amplified with procedural or real-DEM exemplars (HAL PDF abstract, §3-6).
- Data model: each plate is a spherical triangulation of point samples carrying crust type (oceanic/continental), thickness, elevation z, oceanic age and ridge direction, and continental orogeny age, type (Andean/Himalayan) and fold direction (Table 1).
- Uplift: the subduction uplift is ũ_j(p) = u0 · f(d(p)) · g(v(p)) · h(z̃_i(p)), where d is the distance to the subduction front, v is the relative plate speed (g(v) = v/v0), and z̃ is the normalised elevation of the subducting plate. f is a piecewise cubic profile that peaks at a control distance. Collision is a discrete event: terranes detach and suture, and uplift spreads over the collision region (HAL PDF §4.1-4.2).
- Erosion: deliberately simple at this scale (about 50 km samples, δt = 2 My). Continental erosion is z ← z − (z/z_c) ε_c δt. Oceanic dampening is z ← z − (1 − z/z_t) ε_o δt. Trench sediment fill is z ← z + ε_t δt. Low-frequency noise is added. Ocean crust generation and resampling run every 10-60 steps (HAL PDF §4.5).
- Scale: 500,000 samples for a 6,370 km-radius planet (about 35 km resolution). The crust model ranges from 50 to 500 km resolution. Amplified relief reaches about 100 m. Realistic planets appear after a few hundred iterations (about 250 My) (HAL PDF §1, §7).
- Evaluation:
  - A 2AFC user study with 24 participants and 6 pairs: the tectonic model got 97 votes against 47 for fractal planets.
  - The paper says it was "validated by a geological expert in tectonics" (HAL PDF §7.3-7.5).
  - Timing table values were not extractable. The text says most processes are interactive at about 100 km resolution, while ocean crust generation and rifting are the most expensive.
- States compatibility with river networks and stream-power erosion "at the expense of more computationally demanding iterations" (HAL PDF ~§7).
- Code: none found.
- Relevance:
  - (a) Yes, a procedural uplift from subduction/collision.
  - (b) No: continents emerge from the simulation rather than being imposed. The authors list only indirect control over continent shapes as a limitation.
  - (c) No.
  - (d) Yes, exemplar or procedural amplification.
  - (e) A user study plus an expert.
- Limitations: indirect control only; rifting tears progressively; too many forced subduction events; distortion of the planet is not modelled (§7.5).

## 5. Cortial, Guérin, Peytavie, Galin 2020: "Real-Time Hyper-Amplification of Planets"
- Venue: The Visual Computer (2020). Source: https://hal.science/hal-02967067/file/PlanetSubdiv-author.pdf
- What it does: starts from about 50 km control maps (crust elevation, orogeny age, humidity, plateau/hill presence). It builds a spherical Delaunay mesh over Poisson samples, regularises the coast triangles (estuaries), and grows a river network from the coasts inland, computing Horton-Strahler index, flow and water elevation. GPU rule-based dyadic subdivision then reaches about 50 cm precision, with typed vertices and edges (river, terrain, lake, gully, sea) (PDF abstract, §4-5).
- Runtime: preprocessing (230k vertices, 460k triangles, 52 km edges) takes 9.2 s on the CPU. A GPU subdivision update every about 10 frames averages about 80 ms (PDF §4, §7). Memory is over 2 GB of VRAM (limitations).
- Relevance:
  - (b) Yes, in effect: the coastline comes from the input maps, and rivers are grown from the coast inland. This is the river-growth-from-fixed-coast idea from Génevaux et al. 2013.
  - (d) Strong.
  - (a) Uses crust/orogeny-age maps from tectonic planets.
  - (c) No.
- Code: none found.

## 6. Argudo, Galin, Peytavie, Paris, Gain, Guérin 2019: "Orometry-based Terrain Analysis and Synthesis"
- Venue: ACM TOG 38(6), Article 199 (SIGGRAPH Asia 2019), DOI 10.1145/3355089.3356535. Source: https://hal.science/hal-02326472/file/2019-orometry.pdf
- What it does: analyses peaks and saddles (prominence, dominance, isolation, relevance) and the Divide Tree. It trains a Random Forest classifier over 50 mountain regions, with 75.3% mean accuracy at a 50 km radius and 86% once similar regions are merged. For synthesis, it generates a Divide Tree that matches the target statistics and a coarse elevation/density control map, builds the dual river network, rasterises via a TIN at 200 m meshing, then applies multi-fractal noise and constrained multi-scale erosion (HAL PDF §4-6).
- Erosion: hydraulic erosion [Cordonnier 2017] combined with a "compensating uplift" built from a distance field to the ridges, so erosion does not destroy the peaks. It runs at three scales starting at 100 m (HAL PDF §6.3).
- Runtime: a 90×90 km² terrain at 30 m (3000×3000) takes 60-190 s depending on peak density. Mostly Python, with C++ erosion (HAL PDF §7).
- Evaluation: a 2AFC perceptual study (65 subjects from a mountaineering forum, 15 pairs, Bayesian analysis). Among synthetic methods, only theirs overlapped with the real-Divide-Tree variant. Uplift plus erosion [Cordonnier 2016] was one of the treatments (HAL PDF §7.4, Fig. 22).
- Relevance:
  - (c) Strong. Divide Tree extraction from a DEM is the basis of Schott 2023's inverse modelling.
  - (e) Strong. The orometric statistics and classifier serve as a realism metric.
  - (a) No. (b) No.
- Limitations: the Divide Tree discards slope profiles and sub-threshold ridges; it assumes rivers follow medial axes; a gap in tree topology statistics remains (§7.5).
- Code: none found in the paper (UNVERIFIED whether released).

## 7. Galin, Guérin, Peytavie, Cordonnier, Cani, Benes, Gain 2019: "A Review of Digital Terrain Modeling"
- Venue: CGF 38(2) (Eurographics 2019 STAR), DOI 10.1111/cgf.13657. Source: https://hal.science/hal-02097510/file/A%20Review%20of%20Digital%20Terrain%20Modeling.pdf
- Content: a taxonomy of procedural, simulation and example-based methods. Section 4.2 covers tectonics and stream power erosion [CBC*16, CCB*18].
- Realism-evaluation methods listed (§6.2): static renderings, user studies, expert assessment, and automated physical-consistency tests ("usually limited to a test for consistent drainage").
- Open problems listed:
  - Variety of landforms "while maintaining overall consistency".
  - Planetary scale with control.
  - Efficiency: methods taking under a second on 1 km² at 1 m precision "typically take more than three hours" on 100×100 km² at the same precision.
  - Missing glacial and wind processes.
- Relevance: background and (e) methodology.

## 8. Schott, Paris, Fournier, Guérin, Galin 2023: "Large-scale terrain authoring through interactive erosion simulation"
- Venue: ACM TOG 42(5), Article 162 (presented at SIGGRAPH 2023), DOI 10.1145/3592787. Sources: https://h-schott.github.io/p/uplift ; HAL https://hal.science/hal-04049125/file/2022-uplift-author.pdf ; code https://github.com/H-Schott/StreamPowerErosion (MIT licence, read LICENSE in clone)
- What it does: authoring happens in the uplift domain, and the relief emerges from GPU stream-power erosion. Uplift is u = u0 + ũ. The static part u0 comes from a vector "Uplift Tree" (skeletal primitives plus operators). The dynamic part ũ is driven by PID controllers to satisfy point and curve elevation constraints (HAL PDF §3, §5-6).
- Equation: ∂h/∂t = u − s^n a^m + Δh (stream power plus Laplacian hillslope). It uses an explicit scheme on a regular grid: h_i(k+1) = h_i(k) + Δt (u_i − s_i^n a_i^m + ...) (HAL PDF §3-4).
- Drainage: L^p multiple-flow routing with p = 4 (Holmgren). It uses an iterative, parallel drainage approximation: at each step every cell gathers w_ji(k) ã_j(k) from its 8 neighbours plus its own unit rain. This converges to the exact value in n to 4n iterations, about 1.5n on average, where n is the grid width (HAL PDF §4.1-4.2).
  - The released GLSL shader confirms this. Border cells are hard-set to elevation 0 ("Border nodes are fixed to zero"). Each cell computes its new height, clamps it so it never goes below its steepest receiver (newH = max(newH, receiver)), then adds dt·uplift. Erodibility k is modulated by a noise buffer. Modes are SPL, SPL+Laplacian, and SPL+Laplacian+debris slope. Source: `data/shaders/spe_shader.glsl` in https://github.com/H-Schott/StreamPowerErosion
- Uplift Tree primitives:
  - Compact falloff u_S(1 − d²/r²)³.
  - Asymmetric "star-shaped" primitives using a pseudo-distance to a closed boundary curve Γ, for asymmetric ranges.
  - Segment mountain-range and valley primitives, with valley width w ∝ a^0.4.
  - Operators: warp (folds/faults; discontinuities are allowed in uplift), blend, min/max, copy-paste (HAL PDF §5).
- Procedural tectonic-fold uplift: the user designs a tensor field, which gives a vector field. Anisotropic off-lattice Eden growth of Poisson discs, constrained to align with the field (angle threshold α), produces dendritic ridge clusters. These are converted to segment primitives and modulated by density P and elevation E maps (HAL PDF §6.3).
- Inverse modelling (c):
  - The Divide Tree from a DEM [Argudo 2019] yields mountain-range primitives, combined with max. River trees yield valley primitives. Point constraints are added for prominent peaks.
  - Erosion then reproduces the major ridges and valleys "though not strictly identical", with a "lack of variety in the elevation of valleys" from missing sediment deposition (HAL PDF §6.1-6.2, §7.1; Figs. 14, 15, 27: Alps, Rockies, Himalaya).
  - A 1200×600 km terrain was authored from an inverse model of the Alps, including "sea editing" (Fig. 23).
- Runtime (GTX 1080 Ti, GLSL compute):
  - 512² needs about 5000 steps at 0.3 ms/step, 1.3 s total. The paper's comparison point is Cordonnier 2016 at 252 s for 160k nodes.
  - Interactive frame rates up to 4096², real-time editing at 1024².
  - Adaptive Δt grows 1% per step while the pit count decreases and is cut sharply when it increases (HAL PDF §7.2).
  - Table 1 values were not extractable as text.
- Scale: terrains from 100×100 km² to 1000×1000 km². Cell size 80-600 m. Grids 1024² (one example 2000×1200). A ×8 sparse amplification was used for Fig. 1 (HAL PDF §1, §7.5, Table 2).
- Realism (e): Hack's law L = c·a^h was fitted, giving e.g. L = 1.3 a^0.558 and L = 1.1 a^0.563, within the literature ranges c ∈ [1,6] and h ∈ [0.45,0.7] (watersheds under 10 km² excluded) (HAL PDF §7.3, Fig. 30).
- Relevance:
  - (a) Partial. Uplift is authored or procedural, with faults/folds as uplift warps, not plate kinematics.
  - (b) Only the domain border is an outlet at h=0 in the code. Arbitrary interior sea masks are not described; "sea editing" is shown but not specified, so its handling is UNVERIFIED.
  - (c) Yes. (d) Needs external amplification.
  - (e) Hack's law.
- Limitations (HAL PDF §7.5):
  - Conflicting constraints destabilise the controllers; ũ is computed on the CPU and updated about every 10 iterations.
  - Cell size is 80-600 m, so amplification is needed.
  - "water flows outside the terrain ... does not allow for the placement of lakes".
  - No mass conservation or sediment deposition.
  - Convergence is slow above 1024²; the authors suggest multigrid.

## 9. Schott, Galin, Guérin, Peytavie, Paris 2024: "Terrain Amplification using Multi-scale Erosion"
- Venue: ACM TOG 43(4), Article 145 (SIGGRAPH 2024), DOI 10.1145/3658200. Sources: https://h-schott.github.io/p/mserosion ; HAL https://hal.science/hal-04565030/file/2024-MultiScaleHydro-Author.pdf ; code https://github.com/H-Schott/MultiScaleErosion (MIT licence; OpenGL 4.3 compute shaders); Shadertoy https://www.shadertoy.com/view/XX2XWD . The URL given in the task (h-schott.github.io/publications/mserosion/publi_mserosion.html) returned "Not Found" on 2026-11-11.
- What it does: amplifies a low-resolution terrain T0 by repeated A_k = D_k ∘ T_k ∘ E_k ∘ U_k. U_k is bicubic upsampling. E_k is fluvial stream-power erosion without uplift. T_k is thermal stabilisation. D_k is sediment deposition. A diffusion-based elevation retargeting restores peaks and ridges, and a final multi-scale breaching step guarantees drainage (HAL PDF §3-5).
- Modified SPL: h_{i+1} = h_i − k ẽ_i, where ẽ = min(s^n, s_max^n) · min(a^m, a_max^m). The clamping avoids plunging incisions. Spatially varying erodibility is k(p) = k(1 − ρ(p)) from a user hardness map (HAL PDF §4.2).
- Multi-scale breaching: partial breaching operators [Barnes 2014] are applied with decreasing radii, avoiding one-cell-wide canyons (HAL PDF §5.2).
- Scale and runtime:
  - From 256² up to 8192² (×32).
  - One erosion step stays under 11 ms up to 4096² on the GPU.
  - Retargeting and breaching run on the CPU and take a few seconds at 4096² (HAL PDF §1, §7).
- Evaluation (e): the average breaching volume b (volume removed per area needed for free drainage) is compared against learning-based, procedural and sparse amplification. The paper's method has the lowest b even before breaching (HAL PDF §7, Table 3).
- Relevance:
  - (d) Strong.
  - (b) Not discussed beyond breaching to boundaries.
  - (a) No, uplift is explicitly ignored.
- Limitations: whole-map processing limits size to 8192² on one GPU; patch decomposition raises cross-patch drainage issues; style is limited to hydraulic landforms (HAL PDF §8).

## 10. Tzathas, Gailleton, Steer, Cordonnier 2024: "Physically-based analytical erosion for fast terrain generation"
- Venue: CGF 43(2) (Eurographics 2024), e15033, DOI 10.1111/cgf.15033. Sources: HAL https://hal.science/hal-04525371/file/Analytical_Terrains_EG.pdf ; code https://gitlab.inria.fr/landscapes/analytical-terrains (Python numpy plus numba; licence: Inria research-only, non-commercial, no sublicensing, from LICENSE.md in clone)
- What it does: given an initial terrain z0, an uplift map u (varying in space, constant in time), a boundary mask b and a time t, it outputs the terrain at time t with no time-stepping. It uses 1D analytical solutions of the SPL (n=1), evaluated by the method of characteristics along every upstream river path of a receiver tree (HAL PDF §3-4).
- Boundary mask: "each cell where b is True will force its altitude to remain constant: z = z0. At least one cell should be specified as a boundary". Uplift vanishes at the boundary for well-posedness (HAL PDF §3.2, §4.1). This is directly a fixed land/sea mask (b).
- Ordering problem: the river ordering depends on the result. A fixed-point iteration [Steer 2021] is stabilised with an exponential moving average. Convergence is accelerated by a multigrid coarse-to-fine scheme (2×2 averaging; bilinear upsampling with ±0.25 jitter). Alternatively, an optimisation works in the space of elevation differences d_c ≥ 0 to remove discontinuities (HAL PDF §5).
- Other processes: random receivers among the lower neighbours avoid axis-aligned rivers. Thermal erosion has critical slope atan(30°), and hillslope terms are integrated into a(s). Depression breaching is applied. A canyon or tributary boundary condition (constant small slope at the outlet) produces V-shaped canyons (HAL PDF §6-7).
- Runtime (Xeon E5-2650 v4, Python/numba), Table 2 (multigrid / fixed-point / simulation / optimisation):
  - 512²: 1.79 s / 7.85 s / 55.52 s / 0.94 s.
  - 1024²: 8.18 / 70.89 / 556.42 / 4.10 s.
  - 2048²: 33.65 / 538.71 / 4799.44 / 16.61 s.
  - The test case used δx = 50, 25 and 12 m over a constant extent. Steady state was reached at t = 4.6 My (HAL PDF §7.1).
- Validation (e): hypsometry compared against simulation [CBC*16] and fixed-point [Ste21]. The authors note one-to-one comparison is impossible because the river network is one of many valid networks (HAL PDF §7.1).
- The paper notes that GPU explicit SPL [Schott 2023] can be faster but has bounded Δt and no depression routing, so "all the water is trapped within the depressions" when eroding without uplift (HAL PDF §7.1).
- Relevance:
  - (b) Strong: an explicit boundary mask.
  - (a) Uplift is an input map; tectonic derivation is not addressed.
  - (c) No, though time acts as a forward slider.
  - (d) No.
  - (e) Hypsometry.
  - Python is very relevant for a GitHub Actions tool, but the licence is research-only.
- Limitations: no time-continuity (valleys can move when t changes); the analytical framework restricts other laws (sediment deposition, n≠1) (HAL PDF §8).

## 11. Paris, Guérin, Collon, Galin 2023: "Authoring and Simulating Meandering Rivers"
- Venue: ACM TOG 42(6) (SIGGRAPH Asia 2023), DOI 10.1145/3618350. Sources: https://hal.science/hal-04227965/file/2023-meanders.pdf ; code https://github.com/aparis69/Meandering-rivers (MIT, LICENSE read in clone)
- What it does: starts from a terrain plus a low-resolution river network encoded as a directed graph. Each channel's centreline migrates under a physically based, curvature-driven equation. Control terms account for the topography (migration is dampened by slope) and for user trajectory constraints. Cutoffs form oxbow lakes, and avulsions also occur. The recorded evolution yields erosion, sediment and vegetation maps. Results are compared with real river data on sinuosity and meander wavelength (HAL PDF abstract, §7, Table 3).
- Scale: example scenes up to about 35 km (HAL PDF Table 2).
- Relevance:
  - (d) Yes, as river-scale detail after the large-scale erosion.
  - (e) Sinuosity and wavelength statistics.
  - Not (a), (b) or (c).

## 12. Recent erosion and flow-routing building blocks (Inria/UCT/Purdue), 2023-2026
- Cordonnier et al. 2023 "Forming Terrains by Glacial Erosion", ACM TOG 42(4), DOI 10.1145/3592422. Source: https://inria.hal.science/hal-04090644/file/Sigg23_Glacial_Erosion__author.pdf ; code https://gitlab.inria.fr/landscapes/glacial-erosion (GitLab lists the licence as "Other"; text not read, so UNVERIFIED).
  - Uses a deep-learning ice-flow emulator plus multi-scale advection. Glacial, hillslope, debris-flow and fluvial erosion are combined.
  - Scale: 16×16 km² in under 5 minutes; 64×64 km² examples (HAL PDF §1, Fig. 6).
  - Relevance: low for a continental-scale tool. A possible later "glacial pass".
- Jain, Benes, Cordonnier 2024 "Efficient Debris-flow Simulation for Steep Terrain Erosion", ACM TOG 43(4), Article 58. Sources: https://www.cs.purdue.edu/homes/bbenes/papers/Arymaan24ToG.pdf ; HAL https://hal.science/hal-04574826 ; code https://gitlab.inria.fr/landscapes/debrisflow (Inria research-only licence, read raw LICENSE).
  - Adds a debris-flow law alongside uplift and SPL on the GPU, plus approximate GPU flow routing out of depressions.
  - Examples are about 8×8 km (PDF Fig. 6).
  - Relevance: ridge-near steep-slope realism.
- Jain, Kerbl, Gain, Finley, Cordonnier 2024 "FastFlow: GPU Acceleration of Flow and Depression Routing for Landscape Simulation", CGF 43(7) (Pacific Graphics 2024). Source: https://hal.science/hal-04684270/file/FastFlowPG2024_Author_Version.pdf ; code https://gitlab.inria.fr/landscapes/fastflow (Inria research-only licence, read raw LICENSE).
  - GPU flow routing in O(log n) iterations and depression routing in O(log² n). Speedups at 1024² are 5× (flow) and 34-52× (depressions). Implemented in PyTorch/TensorFlow with custom CUDA.
  - Input includes "a user-defined boolean mask b_c of outflow cells ... Typically, outflow cells would line the edges of the grid, but there are cases, such as ... estuaries, and sea shores where they would be placed within the domain" (HAL PDF §3). This is directly (b).
  - Limitation: single flow direction (SFD) only (HAL PDF limitations).
- Yang, Cordonnier, Cani, Perrenoud, Benes 2024 "Unerosion: Simulating Terrain Evolution Back in Time", CGF 43(8) (SCA 2024), DOI 10.1111/cgf.15182. Source: https://hal.science/hal-04714138/file/paper1015_CRC.pdf
  - Runs fluvial erosion (SPL with sedimentation), thermal erosion and deposition backwards in time. Using a negative Δt flips the upwind direction of the gradients.
  - It uses a space-time-varying uplift U. It was tested against real terrace heights in the Pyrenees.
  - Runtime: 100 iterations take about 60 s on 500×500 (HAL PDF §4-6).
  - Relevance: (c), an inverse in time rather than an uplift inversion.
  - Limitations: no multi-material crust; predicts smooth pasts; speculative by nature (HAL PDF §7).
- McDonald & Cordonnier 2026 "Stochastic geomorphological transport for terrain erosion simulation", ACM TOG 45(4), Article 78 (SIGGRAPH 2026), DOI 10.1145/3811336. Source: https://inria.hal.science/hal-05627837/file/2026_siggraph_geomorphological_transport.pdf ; code https://github.com/erosiv/geotransport (MIT; reference kernel only, the full erosion is in soillib, per README).
  - A GPU Monte-Carlo particle transport method that generalises SPL and debris flow through a momentum-conservation-based law. It produces braided rivers, meanders and deltas.
  - Equation: dz/dt = U − E_f + D_f − E_d − E_l + D_d, with Dirichlet boundaries.
  - Scale: 16-64 km² at 512²-4096². 1000-4000 steps; 51 ms/iteration at 1024²; 1-10 minutes total (HAL PDF §3, §6).
  - Relevance: detail and realism at valley scale, not continental.
- Jain, Gain, Cordonnier 2026 "Pixels2Peaks: Converting Terrain Images to Heightmaps", ACM TOG 45(4), DOI 10.1145/3811288. Source: https://inria.hal.science/hal-05617061/file/pixels2peaks.pdf
  - Recovers a heightmap from a single photo (pointmap, then a heightmap, then diffusion inpainting of occluded areas).
  - Relevance: (c), only in the image-to-DEM sense.
- Aryamaan Jain PhD thesis 2026 "Physically guided generation of digital terrains". HAL listing: https://theses.hal.science/tel-05783867/file/2026COAZ4025.pdf (not read, so contents UNVERIFIED).

## 13. Borg, Gain, Guérin, Peytavie, Cani, Galin 2026: "Authoring Terrestrial Planets with Diffusion Models"
- Venue: CGF (Eurographics 2026), DOI 10.1111/cgf.70390 (from the Wiley download stamp in the PDF). Licence on the paper: CC BY-NC 4.0. Source: https://hal.science/hal-05608820/file/Computer%20Graphics%20Forum%20-%202026%20-%20Borg%20-%20Authoring%20Terrestrial%20Planets%20with%20Diffusion%20Models.pdf
- What it does: the user paints coarse elevation (5 bands, including ocean at 0 m and coastal 0-183 m), landcover, temperature and precipitation on a globe at 78 km/pixel (512×256 for an Earth-size planet).
  - The elevation sketch is upsampled, contours are interpolated and noise is added. The PySheds library then computes upstream area. The resulting river network, at 2.4 km/pixel, conditions a tiled diffusion model on a quadsphere trained on Earth and Mars data.
  - Output: a 2.4 km/pixel heightmap plus satellite-like appearance (HAL PDF §3-5).
- Runtime: a full Earth-scale planet takes 1.5-5 h on a 20 GB H100 partition at 100 diffusion steps (HAL PDF §7).
- Relevance:
  - (b) The coastline comes from the user's ocean band. However, "our representation of the oceans is binary" and "blocky edges can occasionally appear in coastlines".
  - (a) No: "we do not explicitly enforce geological consistency ... lacks global information on tectonics or erosion". Future work proposes coupling with plate tectonics and erosion simulation.
  - The river derivation "does not guarantee hydrological termination in lakes or oceans" (HAL PDF §8).

## 14. Other 2025-2026 LIRIS work relevant to analysis and authoring
- Argudo, Guérin, Schott, Galin 2025 "Terrain descriptors for landscape synthesis, analysis and simulation", CGF 44(2), e70080 (Eurographics 2025 STAR). Sources: https://hal.science/hal-05246144/file/2024-metrics-author.pdf ; code https://github.com/oargudo/terrain-descriptors (MIT, C++/Qt).
  - Reviews and implements terrain metrics: slope, curvatures, TPI, ruggedness and roughness, visibility, geomorphons, drainage, Strahler basins, hypsometric integral, and a correlation matrix between metrics (HAL PDF §2-5).
  - Relevance: (e) Directly reusable as a realism checklist.
- Perche, Guérin, Galin, Peytavie 2025 "Vector-based Terrain Modelling", CGF e70160, DOI 10.1111/cgf.70160. Source: https://hal.science/hal-05104719/file/Vector_based_Terrain_Modelling.pdf
  - Converts a DEM into ellipsoid primitives at a user-defined accuracy and supports skeleton-based editing.
  - Relevance: (c)/(d), loosely.
- Huftier, Schott, Galin, Argudo, Peytavie, Guérin 2026 "Terrain Synthesis and Authoring based on Iso-Contours", CGF. Abstract read at https://h-schott.github.io/p/isos/ ; HAL listing hal-05608822 (the PDF fetch failed, so full text is UNVERIFIED).
  - Generates nested contours by inward "Open Eden Growth" and reconstructs a TIN with marching triangles. The result can feed erosion and amplification.
  - Relevance: in principle the outermost contour can be the given coastline (my inference, UNVERIFIED).
- Rajasekaran, Kang, Čadík, Galin, Guérin, Peytavie, Slavík, Benes 2022 "PTRM: Perceived Terrain Realism Metric", ACM TAP, DOI 10.1145/3514244. Source: https://hal.science/hal-03695473/file/article_5.pdf
  - Two perceptual studies found synthetic terrains less realistic than real ones. A metric predicts perceived realism from geomorphon distributions.
  - Relevance: (e).

## 15. Geoscience origins of the solver used in all the above
- Braun & Willett 2013, "A very efficient O(n), implicit and parallel method to solve the stream power equation governing fluvial incision and landscape evolution", Geomorphology 180-181, 170-179 (citation as given in https://meetingorganizer.copernicus.org/EGU2013/EGU2013-6718.pdf). The full text was not accessible (Elsevier), so details come from secondary descriptions:
  - Cordonnier 2016 extends "the original method from [BW13]" by "efficiently model[ling] water flowing from lakes". BW13's optional lake-connection step is O(N√N) (https://www.cs.purdue.edu/homes/bbenes/papers/Cordonier16CGF.pdf §1, §4.3).
  - Cordonnier, Bovy & Braun 2019 follow "the conventions of Braun and Willett (2013)": single steepest-descent receiver, donors, a stack ordering, and boundary nodes at fixed elevation (https://hal.science/hal-02136750/file/A_Versatile_Linear_Complexity_Algorithm_for_Flow_Routing_in_Topographies_with_Depressions.pdf §2).
  - Yuan et al. 2019 describe their extension as O(N) and implicit with sediment deposition. Base-level nodes keep constant elevation, and sediment leaves through them (https://hal.science/hal-02136641/file/ContinentalDeposition.pdf §2).
  - The core recursion (implicit in time, solved downstream to upstream along receivers, O(n) for n=1) is the one written out explicitly in Cordonnier 2016 Eq. 2, quoted in §1 above.
- Cordonnier, Bovy, Braun 2019, ESurf 7, 549-562, "A Versatile, Linear Complexity Algorithm for Flow Routing in Topographies with Depressions" (https://hal.science/hal-02136750/file/...pdf ; https://esurf.copernicus.org/articles/7/549/2019/). It builds an explicit graph of drainage basins, connected through passes by a minimum spanning tree. This gives linear-time depression routing as an alternative to Priority-Flood filling, and it is used in fastscapelib.
- Fastscapelib (C++/Python library implementing these algorithms): https://github.com/fastscape-lem/fastscapelib . Licence GPL-3.0 (LICENSE and README read in clone).
  - Every grid accepts a `nodes_status` array "allowing setting specific statuses for one or more nodes anywhere on the grid". FlowGraph uses all `FIXED_VALUE` nodes as base levels (doc/source/guide_grids.md, guide_flow.md in the clone).
  - In other words, an arbitrary sea mask can be the base level. Caveat in the same docs: "DiffusionADIEroder ignores the grid node status and always assumes fixed value boundaries on the raster grid borders".
- Hergarten 2020, ESurf 8, 841-854, "Transport-limited fluvial erosion – simple formulation and efficient numerical treatment" (https://esurf.copernicus.org/articles/8/841/2020/esurf-8-841-2020.pdf). It gives a direct, fully implicit solver for transport-limited erosion that "requires no iteration for the linear version ... allows for arbitrarily large time increments, and is almost as efficient as the established implicit solver for detachment-limited erosion" (abstract).
  - Hergarten's OpenLEM and the Hergarten/Robl glacial stream-power work were seen only in search snippets (https://gmd.copernicus.org/articles/16/1315/2023/gmd-16-1315-2023.html) and were not read, so they are UNVERIFIED.
  - No single "Hergarten & Robl" implicit-solver paper was found.

## Not read or not found (gaps)
- Galin's 2025 page reportedly mentions a SIGGRAPH-accepted "multi-scale erosion / implicit carving" item (search snippet only, https://perso.liris.cnrs.fr/eric.galin/2029-2025.html). LIRIS servers reset connections, so this is UNVERIFIED.
- Other items not read:
  - Grenier et al. 2024 (procedural erosion-like patterns, CGF).
  - Scott & Dodgson 2021 (breaching inside example-based synthesis).
  - Génevaux et al. 2013 (river-network-first terrains).
  - Arenite 2025 (sandstone).
  - Cortial's thesis (https://theses.hal.science/tel-03186765/file/these.pdf).
  - Cordonnier's thesis (https://theses.hal.science/tel-01971947/file/CORDONNIER_2018_archivage.pdf).
- DBLP, OpenAlex and Semantic Scholar search APIs were blocked or rate-limited. The 2025-2026 coverage therefore rests on HAL API author and title searches plus WebSearch. Non-French 2025-2026 groups may be under-covered.

---

## Summary table

| Paper | (a) tectonic uplift | (b) fixed coastline / BC | (c) inverse | (d) amplification | Code (licence) |
|---|---|---|---|---|---|
| Cordonnier+ 2016 CGF | Painted uplift map; SPL plus implicit BW13-style solve | Domain border = sea-level outlets (external nodes) | No | Via primitives/[GDPG16] | None found |
| Cordonnier+ 2017 TOG | No | No | No | Small-scale layers and ecosystem | None found |
| Cordonnier+ 2018 TVCG | **Yes**: crust thickening rate from plate motion, plus fault and folds, gives uplift | No | No | Strata texture | None found |
| Cortial+ 2019 CGF | **Yes** (procedural subduction/collision uplift on sphere) | No (continents emerge) | No | Exemplar/procedural | None found |
| Cortial+ 2020 TVC | Uses crust/orogeny maps | Coast taken from input; rivers grown from coast | No | **Yes** (50 km to 50 cm) | None found |
| Argudo+ 2019 TOG | No (compensating uplift only) | No | **Divide Tree from DEM** | Noise plus erosion | Not found |
| Galin+ 2019 STAR | Review | Review | Review | Review | n/a |
| Schott+ 2023 TOG | Authored/procedural uplift (tensor-field folds, warps for faults) | Border fixed at h=0 (shader) | **Yes** (DEM to Uplift Tree; PID elevation constraints) | Needs external | github H-Schott/StreamPowerErosion (MIT, C++/GLSL) |
| Schott+ 2024 TOG | No (uplift ignored) | Breaching to boundary | No | **Yes** (×32, to 8192²) | github H-Schott/MultiScaleErosion (MIT, C++/GLSL) |
| Tzathas+ 2024 CGF | Uplift map input (space-varying) | **Explicit boundary mask b** (z fixed) | No (time slider) | No | gitlab.inria.fr/landscapes/analytical-terrains (Python numpy/numba; Inria research-only, non-commercial) |
| Paris+ 2023 TOG | No | No | No | Rivers/meanders | github aparis69/Meandering-rivers (MIT) |
| FastFlow 2024 CGF | No | **Outflow mask anywhere (sea shores)** | No | No | gitlab landscapes/fastflow (Inria research-only) |
| Yang+ 2024 Unerosion | Space-time uplift U (input) | n/a | **Backward in time** | No | Not found |
| Borg+ 2026 CGF | No | Coast from ocean band (binary, blocky) | No | Diffusion to 2.4 km | Not found |
| McDonald & Cordonnier 2026 TOG | U term (input) | Dirichlet | No | Valley-scale detail | github erosiv/geotransport (MIT, reference only) |
| Argudo+ 2025 STAR | No | No | No | No; (e) metrics | github oargudo/terrain-descriptors (MIT) |
| fastscapelib (geo) | U input | **Per-node FIXED_VALUE anywhere** | No | No | github fastscape-lem/fastscapelib (GPL-3.0, C++/Python) |

## Key takeaways for a tool that keeps a fixed coastline, derives uplift from an invented block history, and erodes on GitHub Actions in Python

1. **The fixed coastline is a boundary condition, not a post-process.** Every SPL solver in this survey needs base-level nodes whose elevation is pinned.
   - Cordonnier 2016 used the domain border as "river mouths ... at the sea level".
   - Tzathas 2024 takes an arbitrary boolean mask b where z = z0.
   - FastFlow explicitly allows outflow cells "at sea shores ... within the domain".
   - fastscapelib accepts a per-node `FIXED_VALUE` status anywhere.
   - So: set all sea cells (or just the coastal ring) to FIXED_VALUE at h = 0. Land cells then cannot drain anywhere but to the given coast, which keeps the land/sea mask fixed by construction.
   - Also clamp land to ≥ 0+ε, or the explicit and implicit updates can push near-coast land below sea level. This is my inference; it is not stated in the papers.
2. **Uplift should be zero or small at the coast.** Tzathas 2024 requires uplift to vanish at the boundary for well-posedness. Cordonnier 2016 found that "the uplift gradient" and its shape near boundaries dominate the result. Derive U from the block history, then taper it toward the coast mask (for example with a distance-to-coast falloff).
3. **Converting a block history to uplift has a precedent.** Cordonnier 2018 computes uplift from the crustal thickening rate, u0 = α·dq/dt, with material advected by the block motions. It adds a procedural fault (u0 = 0 on the stable side) and fold-wavelength refinements, and rescales so the mean is about 5e-4 m/y. Cortial 2019 gives a cheaper per-collision-front recipe: u = u0·f(distance to front)·g(relative speed)·h(elevation).
   - Schott 2023 shows uplift may be discontinuous (faults) and can be warped or blended. Erosion then restores hydrological consistency.
   - Orogeny age (Cortial) can modulate erodibility k or a "old mountains" decay term.
   - Isostasy is neglected in all of these papers.
4. **Solver choice for Python on CI.**
   - The implicit O(n) BW13 scheme (receiver, stack, root-to-leaf solve; Cordonnier 2016 Eq. 2) is unconditionally stable for n=1 and allows large Δt, about 2.5e5 y. It needs about 100-300 steps (Cordonnier 2016). It is the natural fit for numpy/numba on a CPU runner.
   - The GPU explicit scheme (Schott 2023) needs thousands of steps (about 5000 at 512²) and has no depression routing (Tzathas 2024 critique). It does not suit CPU CI.
   - The analytical multigrid approach (Tzathas 2024) is Python/numba and fast (1024² in 8.2 s on a Xeon), and it has the boundary mask built in. Its code is research-only and non-commercial, so reimplement it from the paper rather than vendoring it.
   - fastscapelib is GPL-3.0. That is fine for a GPL project; otherwise write your own about 200-line numba BW13 plus Priority-Flood or Cordonnier-2019 basin-graph depression routing.
5. **Pits and lakes.** Run depression routing every step (Cordonnier 2016 lake graph, Cordonnier 2019 linear algorithm, or breaching). Without it, flow traps inside the land, especially when erosion runs without uplift (Tzathas 2024).
6. **Resolution and amplification.** SPL at continental scale lives at 80-600 m cells (Schott 2023). Add detail afterwards with Schott 2024-style clamped SPL (min(s, s_max)·min(a, a_max)) plus thermal and deposition passes on upsampled grids. Finish with multi-scale breaching so the coast-draining network survives the upsampling.
7. **Realism checks that are automatable in CI.**
   - Hack's law fit, with c in [1,6] and h in [0.45,0.7] (Schott 2023).
   - Breaching volume equal to 0 (Schott 2024).
   - Hypsometry against a reference (Tzathas 2024).
   - Orometry: prominence and isolation distributions, Divide Tree statistics (Argudo 2019).
   - Geomorphon histograms (PTRM 2022; Argudo 2025, MIT code).
   - Galin 2019 notes that automated validation is "usually limited to a test for consistent drainage". Adding these gives the tool a stronger story.
8. **Inverse option, if needed later.** Schott 2023 shows that DEM to Divide Tree/river tree to uplift primitives, plus PID-controlled ũ for peak heights, reproduces major ridges and valleys, but not exactly, and valleys come out too uniform without deposition.
9. **Known common gaps to state honestly.**
   - No sediment deposition in pure SPL, which gives flat-less valleys (Schott 2023, Cordonnier 2016).
   - Steady state depends on initial noise: one of many valid networks (Tzathas 2024).
   - The parameters k, m, n are poorly constrained. h_max ≈ 2.244 u/k (km) is a handy empirical calibration from Cordonnier 2016.

---

## URLs read (full text or page content)
- https://www.cs.purdue.edu/homes/bbenes/papers/Cordonier16CGF.pdf
- https://www.cs.purdue.edu/homes/bbenes/papers/Cordonnier18TVCG.pdf
- https://www.cs.purdue.edu/homes/bbenes/papers/Arymaan24ToG.pdf
- https://hal.science/hal-01518967/file/authoring-landscapes-combining.pdf
- https://hal.science/hal-02136820/file/2019-Procedural-Tectonic-Planets.pdf
- https://hal.science/hal-02967067/file/PlanetSubdiv-author.pdf
- https://hal.science/hal-02326472/file/2019-orometry.pdf
- https://hal.science/hal-02097510/file/A%20Review%20of%20Digital%20Terrain%20Modeling.pdf
- https://hal.science/hal-04049125/file/2022-uplift-author.pdf
- https://hal.science/hal-04565030/file/2024-MultiScaleHydro-Author.pdf
- https://hal.science/hal-04525371/file/Analytical_Terrains_EG.pdf
- https://hal.science/hal-04227965/file/2023-meanders.pdf
- https://inria.hal.science/hal-04090644/file/Sigg23_Glacial_Erosion__author.pdf
- https://hal.science/hal-04684270/file/FastFlowPG2024_Author_Version.pdf
- https://hal.science/hal-04714138/file/paper1015_CRC.pdf
- https://inria.hal.science/hal-05627837/file/2026_siggraph_geomorphological_transport.pdf
- https://inria.hal.science/hal-05617061/file/pixels2peaks.pdf (abstract and code link only)
- https://hal.science/hal-05608820/file/Computer%20Graphics%20Forum%20-%202026%20-%20Borg%20-%20Authoring%20Terrestrial%20Planets%20with%20Diffusion%20Models.pdf
- https://hal.science/hal-05246144/file/2024-metrics-author.pdf
- https://hal.science/hal-05104719/file/Vector_based_Terrain_Modelling.pdf (abstract only)
- https://hal.science/hal-03695473/file/article_5.pdf (abstract and introduction)
- https://hal.science/hal-02136750/file/A_Versatile_Linear_Complexity_Algorithm_for_Flow_Routing_in_Topographies_with_Depressions.pdf
- https://hal.science/hal-02136641/file/ContinentalDeposition.pdf
- https://esurf.copernicus.org/articles/8/841/2020/esurf-8-841-2020.pdf (abstract and introduction)
- https://meetingorganizer.copernicus.org/EGU2013/EGU2013-6718.pdf
- https://h-schott.github.io/p/uplift ; https://h-schott.github.io/p/mserosion ; https://h-schott.github.io/p/isos/ ; https://h-schott.github.io/p/desc/
- https://h-schott.github.io/publications/mserosion/publi_mserosion.html (returned Not Found)
- https://aparis69.github.io/public_html/projects/schott2023_Uplift.html ; https://aparis69.github.io/public_html/projects/schott2024_Erosion.html
- https://api.archives-ouvertes.fr/search/ (HAL API, for file URLs and listings)
- https://api.semanticscholar.org/graph/v1/paper/DOI:... (OA locations)
- Repositories cloned and read (README/LICENSE/source):
  - https://github.com/H-Schott/StreamPowerErosion (incl. data/shaders/spe_shader.glsl)
  - https://github.com/H-Schott/MultiScaleErosion
  - https://gitlab.inria.fr/landscapes/analytical-terrains
  - https://github.com/erosiv/geotransport
  - https://github.com/oargudo/terrain-descriptors
  - https://github.com/aparis69/Meandering-rivers
  - https://github.com/fastscape-lem/fastscapelib (README, LICENSE, doc/source/guide_grids.md, guide_flow.md)
  - https://gitlab.inria.fr/landscapes/fastflow/-/raw/main/LICENSE ; https://gitlab.inria.fr/landscapes/debrisflow/-/raw/main/LICENSE ; GitLab API project metadata for glacial-erosion
- Landing and metadata pages (not full text): https://diglib.eg.org/handle/10.1111/cgf12820 ; https://diglib.eg.org/handle/10.1111/cgf13614 ; https://cs.purdue.edu/cgvlab/www/publications/cordonnier2017authoring
- Blocked or failed: hal.science HTML pages behind the Anubis bot check (when sent a browser UA); perso.liris.cnrs.fr (connection reset); dl.acm.org PDFs; DBLP, OpenAlex and Semantic Scholar search (blocked or rate-limited).
