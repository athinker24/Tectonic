# A: Generating many distinct yet consistent solutions from a constrained inverse problem

Tags: [B] full text read (PDF/HTML/README), [B-öz] abstract/summary page only, [Ö] search-result summary only, ERİŞİLEMEDİ = not accessible (not bypassed).

## 1. Non-uniqueness of inverse problems

### 1a. Tarantola (2005) and Tarantola & Valette (1982) [Ö]
- Tarantola & Valette, "Inverse Problems = Quest for Information", J. Geophys. 50 (1982), 159-170. Search summary: the solution is the set of all possible models, each weighted by its posterior probability density. Equations NOT verified.
- Tarantola, *Inverse Problem Theory and Methods for Model Parameter Estimation*, SIAM 2005. Paid/institutional access only; ipgp.fr host returned DNS error / 403. Not read.
- Standard Bayesian form posterior ∝ prior × likelihood is background knowledge, not verified in a source here.

### 1b. Sambridge & Mosegaard (2002) [ERİŞİLEMEDİ / Ö]
- Rev. Geophys. 40(3), doi:10.1029/2000RG000089 (https://doi.org/10.1029/2000RG000089). Publisher page is behind a Cloudflare bot check; not bypassed.
- Search summary [Ö]: review of Monte Carlo methods for nonlinear geophysical inverse problems; literature review plus a summary of popular MC techniques.

### 1c. Schaaf et al. (2021), ABC with topology in GemPy 2.1 [B]
- Geosci. Model Dev. 14(6):3899-3918. https://gmd.copernicus.org/articles/14/3899/2021/gmd-14-3899-2021.html (fetched via curl + oku.py; WebFetch DNS failed).
- Quote [B]: "choosing a likelihood function ... does not seem to enhance the inference ... this work ... adopts an approximate Bayesian computation (ABC) approach to compute the posterior using a distance function instead of a likelihood function."
- ABC-REJ [B]: draw θ' from prior → simulate y(θ') → summary statistic S(y(θ')) (geomodel topology) → accept if distance(S(y(θ')), S(y_obs)) ≤ ε, else reject. Accepted samples approximate the posterior.
- Distance example [B]: Jaccard index on topology graphs, J(A,B) = |A∩B| / |A∪B| (edges = connected regions, citing Thiele et al. 2016b). Equals 1 only for identical graphs; tolerance ε used for acceptance.
- Ensemble construction [B]: input data treated as probability distributions; Monte Carlo realisations; synthetic fault model and Gullfaks (North Sea) case.

## 2. Quality-diversity algorithms

### 2a. MAP-Elites (Mouret & Clune 2015) [B]
- arXiv:1504.04909, https://arxiv.org/abs/1504.04909 (PDF https://arxiv.org/pdf/1504.04909), preprint 20 Apr 2015.
- Algorithm (Fig. 2) [B]: create an empty N-dimensional map; after G random initial solutions, repeat: pick a random elite x from the map, create x' by mutation/crossover, compute feature descriptor b(x') and performance p(x'); insert x' if cell b(x') is empty or p(x') exceeds the occupant's performance.
- Feature space [B]: user-chosen dimensions of variation, each discretised; granularity limited by compute. Hierarchical variant starts with coarse cells and subdivides them.
- Quote [B]: "MAP-Elites is an illumination algorithm." and "each member of the population is by definition diverse, at least according to the dimensions of the feature space."

### 2b. Novelty search (Lehman & Stanley 2011) [B]
- "Abandoning Objectives: Evolution through the Search for Novelty Alone", Evol. Comput. 19(2):189-223, doi:10.1162/EVCO_a_00025 (https://doi.org/10.1162/EVCO_a_00025). Full text read from a third-party course copy, https://www.cs.swarthmore.edu/~meeden/cs81/f17/papers/lehman_ecj11.pdf (not the publisher version). Publisher page not accessible.
- Eq. (1) [B]: ρ(x) = (1/k) Σ_{i=1..k} dist(x, μ_i), μ_i = k nearest neighbours in behaviour space. Sparse = novel.
- Quote [B]: "instead of rewarding performance based on an objective, novelty search rewards diverging from prior behaviors."
- Archive admission [B]: added if ρ exceeds a threshold ρ_min.

### 2c. Determinantal point processes (Kulesza & Taskar 2012) [B]
- arXiv:1207.6083, https://arxiv.org/abs/1207.6083 (PDF https://arxiv.org/pdf/1207.6083).
- Eq. (85) [B]: L_ij = q_i φ_i^T φ_j q_j, with q_i > 0 the item quality and ||φ_i|| = 1; S_ij = φ_i^T φ_j is a similarity.
- Eq. (87) [B]: P_L(Y) ∝ (Π_{i∈Y} q_i²) det(S_Y). The quality term and the diversity (determinant) term are separated.
- L-ensemble [B]: P_L(Y) ∝ det(L_Y) = Vol²({B_i : i∈Y}) with L = B^T B (Eq. 6, 26).
- Fixed-size sets: k-DPPs (Section 5) [B, section title only verified].

## 3. Constraint-based procedural generation

### 3a. WaveFunctionCollapse [B]
- Source README: https://github.com/mxgmn/WaveFunctionCollapse (raw: https://raw.githubusercontent.com/mxgmn/WaveFunctionCollapse/master/README.md). Local copy: /tmp/claude-0/-home-user-Tectonic/1cb340b3-df7d-519b-96f4-5170b8cfb37a/scratchpad/src/wfc/readme.md
- Constraints [B]: (C1) output contains only NxN patterns present in the input; (weak C2) pattern distribution resembles the input's.
- Algorithm [B]: each cell starts as a superposition; repeatedly collapse the cell with lowest Shannon entropy, then propagate constraints. A zero-coefficient cell is a contradiction and the run fails.
- Complexity [B]: "determining whether a certain bitmap allows other nontrivial bitmaps satisfying condition (C1) is NP-hard"; contradictions occur "surprisingly rarely" in practice.
- Diversity caveat [B]: "easy" tilesets (no contradictions possible) do not produce interesting global arrangements.
- Hybrid note [B]: ConvChain (MCMC, exact pattern statistics) can produce a well-sampled start, then WFC corrects local defects.

### 3b. ASP for diverse/similar solutions (Eiter et al.) [B]
- arXiv:1108.3260, https://arxiv.org/abs/1108.3260 (PDF https://arxiv.org/pdf/1108.3260), "Finding Similar/Diverse Solutions in Answer Set Programming".
- Problem [B]: given ASP program P, distance measure Δ over solution sets (non-negative integer), n and k: find a set S of size n with Δ(S) ≥ k (k-diverse) or Δ(S) ≤ k (k-similar); also a k-distant/k-close extension of a given set.
- Distance [B]: Hamming distance is used (e.g., action-based Hamming distance for planning).
- Methods [B]: offline enumeration + clustering; online reformulation in ASP; iterative online search; modified solver (CLASP-NK). The last online method was reported to outperform the others on the phylogeny case study.

### 3c. Other ASP/PCG sources [Ö]
- Smith & Mateas (ASP for PCG, declarative design spaces): https://course.ccs.neu.edu/cs5150f14/readings/smith_asp4pcg.pdf (not read in full).
- Togelius & Justinussen (generate-and-test in ASP can make diversity hard to guarantee): https://www.pcgworkshop.com/archive/togelius2012compositional.pdf (not read in full).
- Wang & Kreminski (ASP enumerates story outlines, then LLM writes stories): https://arxiv.org/html/2406.00554v2 (not read in full).

## 4. Distances between solutions

- Jaccard on topology graphs [B]: see 1c.
- Hamming distance on action/decision sequences [B]: see 3b.
- Wasserstein / Earth mover's distance [Ö]: Monge-Kantorovich optimal transport; EMD is the W1 case with ground metric d(x,y). Refs: Villani (2009), Peyre & Cuturi (2019). Search summary only: https://www.wikipedia.org/wiki/Earth_mover%27s_distance (not read as full text).
- Plate-model comparison [Ö]: Buffan et al. (2023, Methods in Ecology & Evolution) compare five open global plate models using palaeolatitudinal standard deviation and mean pairwise geodesic distance; differences increase with age. Source page https://doaj.org/article/97f797fc7a114159a96fb790cd497431 ERİŞİLEMEDİ (Cloudflare check); summary from search only.
- Plate uncertainty methods [Ö]: GPlates mailing-list discussion (2019): covariance propagation (linearised), bootstrap of misfit residuals, comparison of rotation files; total uncertainty needs a likelihood + MCMC (https://mailman.sydney.edu.au/pipermail/gplates-discuss/2019-October/000769.html).

## 5. Event-based / scenario-tree generators for paleogeography

- No source found that combines "event-based", paleogeographic, and Bayesian scenario ensembles. BULUNAMADI for that combination.
- Nearest matches [Ö]:
  - Skauvold & Eidsvik: process-based basin model with ensemble Kalman filter, prior ensemble driven by sea-level and sediment-supply parameters (https://arxiv.org/pdf/1711.07763).
  - 2025 GSA abstract: coastal stratigraphy under earthquake uncertainty; four scenarios from constrained/unconstrained slip and timing; Monte Carlo over multiple seismic events (search summary only).
  - EGU2020 particle filter for continental motion with paleomagnetic data; several thousand ensemble members (https://meetingorganizer.copernicus.org/EGU2020/EGU2020-20561.html).

## Access summary
- Read in full: MAP-Elites, DPP, novelty search (course copy), WFC README, Eiter ASP, Schaaf GMD 2021.
- ERİŞİLEMEDİ: Sambridge & Mosegaard (Cloudflare); Buffan 2023 (Cloudflare); Lehman & Stanley publisher page (Cloudflare).
- Not accessible / paid: Tarantola 2005 (ipgp.fr DNS/403; not downloaded from unofficial copies).
- WebFetch DNS failures: gmd.copernicus.org and doaj.org (fell back to curl + oku.py for GMD; DOAJ still blocked by bot check).
