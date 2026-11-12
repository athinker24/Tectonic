# Terrain realism metrics: research notes (in progress)

Status: skeleton written. Findings will be appended per topic.
Tags: [B] full text read / [B-öz] summary read / [Ö] search snippet only / BULUNAMADI = not found / ERİŞİLEMEDİ = not reachable.

## 1. Hypsometry
- Strahler 1952, "Hypsometric (area-altitude) analysis of erosional topography", GSA Bulletin 63(11):1117-1142. [Ö] (search snippet, 2026-11 session). URL: https://researchclopedia.vercel.app/research/W2064972007 (secondary index; original not opened). Note: youth/maturity/old-age stages give distinct curves, but mature and old stages look identical unless monadnocks are present.
- Numeric HI thresholds (youth above 0.6, maturity 0.35-0.6, old below 0.35) are from a later Spanish-language basin study, not from Strahler 1952. Carson & Kirkby 1972 (integral settles near 0.5 at maturity) and Chorley & Kennedy 1971 (<=0.6) also cited second-hand. [Ö] Source: https://revistas.unlp.edu.ar/domus/article/download/2943/3846/11701 (listed, not read). Verify against the original before use.
- Land mean 840 m and median 377 m (Cogley / Harrison / Sinclair): NOT CONFIRMED. Search returned an arXiv paper (https://arxiv.org/pdf/1810.08658) listing mean land elevation 840 m for 1921 (a historical estimate, not Cogley), and medians of 466 m (Kossinna 1931) and 420.5 m (Amante & Eakins 2012). The 377 m median did not appear. Status: BULUNAMADI for the exact pair; treat the user's figure as unverified.
- ETOPO1 (Amante & Eakins 2009): not yet verified in this session.
- Other searches for topics 2-7 are pending: WebSearch hit the 5-hour usage limit (resets 06:00 UTC) after 3 queries.

## 2. Stream network scaling
- Hack's law: L = C A^h, h "slightly less than 0.6" in most basins; h decreases slightly for basins >8,000 mi2 (>20,720 km2). [B-öz] https://en.wikipedia.org/wiki/Hack%27s_law (read via curl). The user's L = 1.4 A^0.6 is consistent with h ~ 0.6 but the constant 1.4 is not in this source; C is basin/unit dependent. Verify the constant in Hack 1957 (not opened).
- Strahler stream order (top-down, outermost tributaries = 1): [B-öz] https://en.wikipedia.org/wiki/Stream_order. Horton ratio values (bifurcation 4-5, length 2-2.5, area 4.5-5): page fetched but no matching text found; BULUNAMADI in this session.
- Kirby & Whipple slope-area S = k_s A^-theta, theta ~0.45 +/- 0.2: BULUNAMADI (search quota exhausted; not verified).
- Channel-head threshold area: BULUNAMADI (not verified).

## 3. Fractal and spectral metrics
- Hypsometric curve / integral as summary metric: [B-öz] https://en.wikipedia.org/wiki/Hypsometric_curve. Strahler's three-parameter fit questioned by 2D landscape-evolution models; a one-extra-parameter modification proposed. Scale-dependence noted.
- Real landscapes behave differently at different scales; simple fractal functions often inappropriate; multi-fractal techniques suggested. [B-öz] https://en.wikipedia.org/wiki/Fractal_landscape
- Mark & Aronson 1984 (D ~2.2): BULUNAMADI (not verified). Perron 2008 spectral/Hurst: not verified. Power spectrum and Hurst exponent values: not verified.

## 4. Slope distribution
- Median slope 10-20 deg in mountainous terrain, threshold 30-40 deg: BULUNAMADI (not verified; search quota exhausted).

## 5. GEBCO and Copernicus DEM
- GEBCO: current grid is GEBCO_2026 (not 2024), 15 arc-second interval, global ocean and land terrain model, netCDF/GeoTIFF/ESRI ASCII, with a TID (type identifier) grid and under-ice variant. [B-öz] https://www.gebco.net/data_and_products/gridded_bathymetry_data/ (fetched via curl through proxy). Terms of use: linked on the page, not read.
- Copernicus DEM GLO-30 / GLO-90 accuracy and license: ERİŞİLEMEDİ. spacedata.copernicus.eu returned an empty extraction and WebFetch DNS failed. Verify: GLO-30 ~30 m, GLO-90 ~90 m are expected but NOT confirmed here.
- Wikipedia DEM article: FABDEM is a bare-earth 1 arc-second (~30 m) model derived from GLO-30, free for non-commercial use. [B-öz] https://en.wikipedia.org/wiki/Digital_elevation_model
- Coarse-graining and area-weighted comparison method: BULUNAMADI (not researched).

## 6. Perceptual realism evaluation
- BULUNAMADI (not researched in this session; search quota exhausted). Metrics to check next: user study, FID, orometry, elevation histograms, hydrological consistency.

## 7. Ridge connectivity and topology
- Argudo 2019 orometry (peak/pass graph): BULUNAMADI (not verified).

## Access log
- WebFetch DNS errors: www.gebco.net (first try failed, curl fallback worked), spacedata.copernicus.eu (failed both ways; empty).
- WebSearch: 3 queries succeeded, then 5-hour usage limit reached (resets 06:00 UTC).
- Unverified user claims: Cogley 840 m / 377 m pair (only a different 840 m figure from 1921 found); Strahler HI thresholds (second-hand only).
