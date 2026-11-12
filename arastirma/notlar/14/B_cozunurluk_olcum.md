# B: DEM resolution, scale dependence and river network (findings)

Status: pass 2 done. In pass 1 most hosts gave DNS errors. In pass 2, curl (no TLS bypass) reached www.gmba.unibe.ch, esurf.copernicus.org (articles and preprints), hydrology.usu.edu and orca.cardiff.ac.uk. Blocked: www.doi.org (HTTP 403, ERİŞİLEMEDİ), efi.eng.uci.edu (self-signed certificate chain, ERİŞİLEMEDİ; not bypassed), www.geomorphometry.org (DNS, ERİŞİLEMEDİ). Tags as below.

Tags: [B] full text read from the PDF or page; [B-öz] summary read; [Ö] search-snippet summary only; ERİŞİLEMEDİ = host not reachable or blocked; BULUNAMADI = not found.

## Corrections from pass 2
- The 2025 ESurf paper (ESurf 13, 403, 2025) is by B. Kargère et al., "A fractal framework for channel–hillslope coupling". Pass 1 wrongly attributed it to Hergarten and Pietrek. [B]
- Pass 1 said the GMBA window is about 1.8 km and the threshold is 200 or 300 m. The GMBA page (pass 2) gives the definition directly; see Section 2.

## 1. DEM resolution, relief, slope, valley density

- Grieve, Mudd, Milodowski, Clubb & Furbish 2016, "How does grid-resolution modulate the topographic expression of geomorphic processes?", ESurf Discussions, doi 10.5194/esurf-2016-28 (the file read is the discussion preprint; final publication status not checked). [B]
  - Sites: three US study sites, including Santa Cruz Island and Gabilan Mesa (California). 20 DEM resolutions per landscape, from 1 m upward.
  - Hillslope length and relief, using 1 m channel heads mapped to coarse grids (upper bound) and geometric channel heads at each resolution (lower bound). [B]
  - Santa Cruz Island: relief shows little resolution dependence up to about 10 m cells, then rises steadily beyond that. [B]
  - Gabilan Mesa: mean relief rises by about 20 m between the highest and lowest resolution datasets. [B]
  - Hillslope length: little change up to about 10 m; beyond that the geometric-channel method is affected by the loss of channel network accuracy. [B]
  - Curvature is largely insensitive to resolution on broad hilltops and valleys, but not on sharp ridges. [B]
  - Nyquist limit: the feature resolvable at grid spacing Res has a wavelength limit of 2·Res (quoted as "(2Res)^-1" in the text, i.e. the frequency). [B]
- Zhang & Montgomery 1994, Water Resources Research 30:1019-1028, DOI 10.1029/93WR03553. [Ö]
  - Grid sizes 2, 4, 10, 30, 90 m on two small western-US catchments. Finding: 10 m is a substantial gain over 30 and 90 m; 2 and 4 m add little for moderately to steep terrain. [Ö]
  - Increasing grid size raises the mean topographic index (larger contributing area, lower slopes). [Ö]
  - Numerical table: BULUNAMADI in pass 2. The DOI host is blocked (ERİŞİLEMEDİ) and the search returned no non-publisher full text.
- Grohmann 2013 (geomorphometry.org proceedings): coarser grids flatten slope values and distort the slope distribution. Full text ERİŞİLEMEDİ (host unreachable). Grohmann 2007: BULUNAMADI.
- Slope vs. grid size: slope varies inversely with grid size; a fractal/variogram correction is proposed for coarse-grid slopes. [Ö] Slope length increases roughly linearly as resolution decreases (Guo et al. 2013). [Ö]
- Lin & Oguchi 2004, Geomorphology. [Ö] 1 m DEMs from photogrammetry, 88 subwatersheds, two drainage-density–slope types tied to channelization stages. No threshold-area statement in the snippets. Full text: CSIS Discussion Paper #56 (not accessed).
- Local relief at Δx = 5, 10, 20, 90 m and 1 km cells: BULUNAMADI as a table. Qualitative values are in the Grieve et al. item above.

## 2. GMBA / Körner multi-window relief and ruggedness

- GMBA mountain definition page, https://www.gmba.unibe.ch/tools/definitions/mountain_definition/index_eng.html (reached with curl in pass 2). [B-öz]
  - Ruggedness = maximum elevation difference among 3 × 3 = 9 grid points of 30" data within 2.5' pixels, from the DEM used by WorldClim.
  - A 2.5' pixel is "rugged" (mountainous) if max minus min of the 9 points exceeds 200 m. [B-öz]
  - The 300 m value in the Alpine Botany 2021 snippet does not match this page. The 200 m threshold in the GMBA page is the one to use for the 2011 definition. Körner et al. (2011) was not reached (linked PDF on the same site, not fetched).
  - Coverage: mountains are 12.3% of Earth's surface outside Antarctica (GMBA) and home to 511 million people; Kapos et al. (combined elevation and ruggedness) give about 22% and 1.27 billion. [B-öz]
- Körner, Paulsen & Spehn 2011 (the source PDF, linked from the GMBA page): not fetched. Multi-window or 1.8 km window formula: BULUNAMADI in verified text. Pass-1 snippets (1.8 km window, 6 km radius) are unverified.
- GMBA Definition v2.0 (2021): DEM-derived parameters instead of expert judgement; 30 arc-second rasters. [Ö]

## 3. Coarse-graining (5 to 20 km), fractal and spectral approaches

- Perron, Kirchner & Dietrich 2008, JGR 113, doi 10.1029/2007JF000866. [Ö] Terrain is not monofractal, so one Hurst exponent does not describe it. Abstract and results: ERİŞİLEMEDİ (efi.eng.uci.edu blocked by certificate; doi.org 403).
- Pelletier spectral analysis: BULUNAMADI.
- Fractal correction of coarse-grid slope: [Ö] (underestimate with coarse grids; variogram-based correction).
- Mean elevation, slope and local relief for 5 km to 20 km coarse-graining: BULUNAMADI as numbers. The qualitative trend (coarser grids flatten slope and lengthen hillslopes) comes from the items above. [Ö]

## 4. Keeping results consistent across resolutions

- Hergarten 2020, "Rivers as linear elements in landform evolution models", ESurf 8, 367-377, doi 10.5194/esurf-8-367-2020. [B]
  - Problem: detachment-limited stream-power erosion (E = K A^m S^n) coupled to hillslopes has a grid-spacing dependence; rivers on a grid are linear objects one pixel wide, so the pixel area covering the network decreases with mesh width.
  - Proposed fix: rescale the fluvial incision term by a power law in the threshold catchment size A_c and mesh width δ. The scaling factor is δ^d (Eq. 7), and rescaling replaces δ by channel width w, so a factor w^d remains (Eq. 8). Exact value of d: not quoted in the text read.
  - Example runs: δ = 0.01 (100 × 100 nodes) vs δ = 0.002 (500 × 500 nodes); canyon-like topography at fine resolution without local transport. [B]
  - Eroded area A_e vs catchment size A for different A_c. [B] (figure)
- Kargère et al. 2025, "A fractal framework for channel–hillslope coupling", ESurf 13, 403 (published 19 May 2025). [B-öz]
  - Characteristic landscape length from a 1D inflection point. In 2D, channel heads form at a characteristic area equal to the square of the characteristic length, independent of grid resolution. [B]
  - Box-counting fractal definition using grid resolution. Channels have drainage area with dimension 2; channel width scales as the square root of drainage area. [B]
- Guérin et al. 2017, "Interactive Example-Based Terrain Authoring with Conditional GANs", ACM TOG 36(4), article 228. [Ö] Learned synthesis from ridge/valley maps, not a physical model.
- Schott 2024: BULUNAMADI. Nearest match: Huftier, Schott, Galin, Argudo, Peytavie & Guérin, "Terrain Synthesis and Authoring based on Iso-Contours", Computer Graphics Forum 45 (2026). [Ö] Date mismatch; confirm the intended paper.
- Multigrid, downscaling, super-resolution, mesh refinement: not searched in this pass. Item 17 overlaps; kept short.

## 5. River network: resolution-dependent length, drainage density, A_c

- Tarboton, Bras & Rodriguez-Iturbe 1991, "On the Extraction of Channel Networks from Digital Elevation Data", Hydrological Processes 5:81-100. [B]
  - Criterion: the smallest support area S for which elevation scaling laws still hold (constant drop property; power-law slope–area scaling). Tested on 21 US DEM datasets. [B]
  - Example from the W15 basin: support area 50 pixels (30 m × 30 m) for the stream-drop analysis; the t-statistic analysis places the break in scaling near support areas of 20 to 50 pixels (sentence truncated in extraction; verify). [B]
  - The threshold where the constant drop property holds gives the basic horizontal length scale, expressed as support area or drainage density. Drainage density per basin is in Table III of the paper. [B]
- Tarboton 1992, "A physical basis for drainage density", Geomorphology 5: drainage density separates channel-forming (unstable) and diffusive (stable) process scales. [Ö]
- Helmlinger, Kumar & Foufoula-Georgiou 1993, WRR 29: morphometry strongly depends on A_th and DEM resolution. [Ö]
- Montgomery & Dietrich 1992, Science, "Channel initiation and the problem of landscape scale": channel-head threshold on A·|∇z|²; inverse area–slope relation at channel heads; thresholds depend on grid resolution. [Ö] Numerical A_c values: BULUNAMADI (1992 paper not reached; Nature 1988 DOI blocked).
- Coastline-type length dependence of drainage networks as a formula: BULUNAMADI. Qualitative support: Tarboton 1991 (scaling-based resolution choice) and Kargère et al. 2025 (resolution-independent channel-head area). [B]
- "Tarboton 1997", WRR 33(2):309-319: a D∞ flow-direction paper, not a drainage-density paper. [Ö] Check the user's citation.

## 6. Items to verify or still open
1. Körner et al. 2011 PDF: window size formula and whether 200 m is the same threshold (GMBA page says 200 m).
2. Zhang & Montgomery 1994 numerical table: not found outside the publisher.
3. Montgomery & Dietrich 1992 A_c numbers: not found.
4. Hergarten 2020 exponent d and fitted A_c scaling constants: check Eq. 7-11 in full text (text read only in part).
5. Schott 2024 citation: not found.
6. Tarboton 1997 citation: D∞ paper.
7. Grohmann 2013 slope-resolution numbers: full text blocked.
8. Perron 2008 abstract and spectral results: efi.eng.uci.edu blocked by certificate; not bypassed.

## 7. Hosts still blocked (ERİŞİLEMEDİ)
- www.doi.org (HTTP 403).
- efi.eng.uci.edu (TLS certificate chain not trusted; not bypassed).
- www.geomorphometry.org (DNS).
- Allowing these in session network settings would unlock items 2, 7, 8 above.
