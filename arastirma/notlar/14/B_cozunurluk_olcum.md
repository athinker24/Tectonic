# B: DEM resolution, scale dependence and river network (findings)

Status: research pass 1 done. Network access is heavily restricted in this session. Most primary-source hosts returned DNS errors (ENOTFOUND): www.gmba.unibe.ch, efi.eng.uci.edu, www.geomorphometry.org, hydrology.usu.edu, www.doi.org, esurf.copernicus.org. Everything below from search snippets is tagged [Ö] and must be verified against the original text before citing numbers.

Tags: [B] full text read; [B-öz] summary read; [Ö] search-snippet summary only; ERİŞİLEMEDİ = host not reachable; BULUNAMADI = not found.

Overall: no [B] or [B-öz] sources were obtained. No quantitative relief ratios for Δx = 5, 10, 20, 90 m or 1 km were found. Several exact citations need checking (see Section 6).

## 1. DEM resolution, relief, slope, valley density

- Zhang & Montgomery 1994, Water Resources Research 30:1019-1028, "Digital elevation model grid size, landscape representation, and hydrologic simulations". [Ö]
  - Grid sizes tested: 2, 4, 10, 30, 90 m, built from simulated landscapes on two small catchments (0.3 and 1.2 km²). [Ö]
  - Finding: a 10 m grid is a large improvement over 30 m and 90 m; 2 m and 4 m add only marginal gain on moderate-to-steep terrain. The authors suggest 10 m is often adequate. [Ö]
  - Caveat from a later comment: the 10 m conclusion depends on the input data, since the spot elevations came from stereo digitizing at about 10 m spacing. [Ö]
  - Exact equations and quantitative tables: ERİŞİLEMEDİ (AGU paywall, and the search result gave no full text).
- Grohmann 2013 (geomorphometry.org proceedings), on resolution and slope distribution. [Ö]
  - Coarser grids flatten slope values and distort the slope distribution. Resampling a fine DEM to coarser grids is the method. [Ö]
  - Full text: ERİŞİLEMEDİ (host blocked). The 2007 Grohmann paper itself: BULUNAMADI.
- Slope vs. grid size, fractal correction. [Ö] (esurf.copernicus.org preprint 2016-28 and a fractal-based coarse-slope paper)
  - Slope varies inversely with grid size; coarse-grid slopes underestimate true slope. A variogram/fractal correction is proposed. [Ö]
  - Slope length increases roughly linearly as resolution decreases (Guo et al. 2013). [Ö]
  - Exact coefficients for Δx = 5, 10, 20, 90 m: BULUNAMADI.
- Lin & Oguchi 2004, Geomorphology. [Ö]
  - Data: 1 m DEMs from digital photogrammetry, 88 subwatersheds; relations among drainage density, slope angle and relative height. Two drainage-density–slope types were found and linked to channelization stages.
  - No DEM-resolution or threshold-area statement found in the snippets. Full text: CSIS Discussion Paper #56 (University of Tokyo), not accessed.
- Relief ratios (local relief at 5, 10, 20, 90 m and 1 km cells): BULUNAMADI.

## 2. GMBA / Körner multi-window relief and ruggedness

- Körner, Paulsen & Spehn 2011, GMBA mountain definition: a ruggedness-based definition that does not use elevation. [Ö]
  - Method: 30 arc-second DEM; a 3×3 cell elevation range over a window of about 1.8 km × 1.8 km (one description), or a 3×3 grid in a 6 km-radius circle (another). [Ö]
  - Threshold conflict: sources give 300 m (Alpine Botany 2021), 200 m (GMBA 2021 raster notes), and 200 m with 1 km DEM for the older K2 characterization. [Ö]
  - Unresolved: which threshold applies to the 2011 definition. Check the original paper.
  - Coverage: 12.3% of Earth's land outside Antarctica, 511 million mountain people (GMBA); Kapos et al. alternative gives about 22% and 1.27 billion. [Ö]
- GMBA Definition v2.0 (2021): uses DEM-derived parameters rather than expert judgement; rasters at 30 arc-second. [Ö]
- Source page https://www.gmba.unibe.ch/tools/definitions/mountain_definition/index_eng.html: ERİŞİLEMEDİ (DNS failure).
- Hence the exact window, threshold and "multi-window" formula: not verified; [Ö] only.

## 3. Coarse-graining (5 to 20 km), mean elevation, slope, local relief; fractal and spectral approaches

- Perron, Kirchner & Dietrich 2008, "Spectral signatures of characteristic spatial scales and nonfractal structure in landscapes", JGR 113, doi 10.1029/2007JF000866. [Ö]
  - Later work cites it as evidence that real terrain is not monofractal, so one Hurst exponent does not describe it. [Ö]
  - Abstract and main spectral results: not retrieved. The PDF at efi.eng.uci.edu was ERİŞİLEMEDİ.
- Clarke's scale-dependent / scale-independent split, calibrated by Fourier analysis and fractal dimension. [Ö]
- Pelletier spectral analysis: BULUNAMADI in this pass (no Pelletier paper found).
- Nyquist limit for grid resolution: f_N = 1/(2·Res) (a 2016 ESurf study). [Ö]
- Effect of coarse-graining from 5 to 20 km on mean elevation, slope and local relief: BULUNAMADI.

## 4. Keeping results consistent across resolutions: resampling, super-resolution, mesh refinement

- Guérin et al. 2017, "Interactive Example-Based Terrain Authoring with Conditional Generative Adversarial Networks", ACM TOG 36(4), article 228. [Ö]
  - Trained on paired real terrains and ridge/valley line maps. Learned synthesis, not a physical model. [Ö]
- Schott 2024: BULUNAMADI. The closest match is Huftier, Schott, Galin, Argudo, Peytavie & Guérin, "Terrain Synthesis and Authoring based on Iso-Contours", Computer Graphics Forum 45 (2026). [Ö]. This does not match the 2024 date in the request; confirm the intended paper with the requester.
- Multigrid, downscaling and mesh refinement references: not searched in this pass.
- Note: this topic overlaps with item 17. Kept short here.

## 5. River network: resolution-dependent length, drainage density, threshold area A_c

- Tarboton, Bras & Rodriguez-Iturbe 1991, "On the Extraction of Channel Networks from Digital Elevation Data", Hydrological Processes 5:81-100. [Ö]
  - Criterion: extract the highest-resolution (highest drainage density) network that still satisfies channel-network scaling laws. Tested on 21 US DEMs. [Ö]
- Tarboton, Bras & Rodriguez-Iturbe 1992, "A physical basis for drainage density", Geomorphology 5. [Ö]
  - Drainage density marks the transition between channel-forming (unstable) and diffusive (stable) processes.
- Helmlinger, Kumar & Foufoula-Georgiou 1993, WRR 29, "On the use of DEM data for Hortonian and fractal analyses of channel networks". [Ö]
  - Morphometry depends strongly on the support-area threshold A_th and on DEM resolution.
- Montgomery & Dietrich 1992, Science, "Channel initiation and the problem of landscape scale". [Ö]
  - Channel-head thresholds on A·|∇z|² (drainage area times slope squared). Inverse area–slope relation at channel heads, Tennessee valley data. Thresholds depend on grid resolution. [Ö]
  - Montgomery & Dietrich 1988 (Nature 336:232) is a separate paper: source area above channel head decreases with local gradient, 5-45°. [Ö]
  - Exact A_c values in km² or cells: BULUNAMADI.
- Coastline-paradox-type length dependence of river networks: BULUNAMADI as a formula in this pass. Qualitative support from Tarboton 1991 (scaling-based resolution choice). [Ö]
- Tarboton 1997, WRR 33(2):309-319 is the D∞ flow-direction paper, not a drainage-density paper. [Ö] The user's citation should be checked.

## 6. Items to verify before use

1. Körner et al. 2011 window size and threshold (300 m vs 200 m).
2. Zhang & Montgomery 1994 full numerical results.
3. Schott 2024 citation (no match found; 2026 CGF paper is the nearest).
4. Tarboton 1997 citation (D∞ paper; drainage-density claim not confirmed).
5. Montgomery & Dietrich 1992 A_c values.
6. Pelletier spectral paper: not found.

## 7. Hosts to allow for a second pass

www.gmba.unibe.ch, www.geomorphometry.org, hydrology.usu.edu, www.doi.org, efi.eng.uci.edu, esurf.copernicus.org. Access to these would allow [B] reading of most items above.
