# A_yagis: Orographic precipitation, relief feedback, and simple climate-band modelling

Status: complete (first full pass). Labels: [B] full text read (PDF/HTML); [B-öz] abstract or metadata only; [Ö] search-snippet summary; BULUNAMADI = not found; ERİŞİLEMEDİ = could not access (network/bot protection/404).

Region of interest for the tool: 7°G–60°K (ITCZ to mid-latitude westerlies).

---

## 1. Orographic precipitation models

### 1.1 Smith & Barstad (2004), J. Atmos. Sci. 61(12), 1377–1391
- DOI: 10.1175/1520-0469(2004)061<1377:ALTOOP>2.0.CO;2. Citation confirmed from library record [Ö] (https://bvbvf1.bib-bvb.de/vufind/PrimoRecord/cdi_proquest_journals_236444084).
- Journal full text: ERİŞİLEMEDİ (journals.ametsoc.org did not resolve from this environment; DOI redirect not followed).
- Companion 6-page extended abstract by the same authors (10th Conf. Mesoscale Processes, paper 62756), https://ams.confex.com/ams/pdfpapers/62756.pdf: [B]. Equations below are from this abstract; the JAS paper itself was not read, so symbols and constants must be checked against it.
  - Steady-state, vertically integrated cloud water (q_c) and hydrometeor (q_h) budgets:
    - (1a) U·∇q_c = S_ref(x,y) − q_c/τ_c
    - (1b) U·∇q_h = q_c/τ_c − q_h/τ_f, with precipitation P = q_h/τ_f at ground level (the abstract writes the sink as the precipitation rate).
  - Source term: S = C_w U·∇h(x,y) (classical upslope form, Smith 1979) or from moist adiabatic lapse rate plus mountain-wave theory. C_w: lifting-to-condensation sensitivity.
  - Transfer function (Fourier domain, abstract eq. 2): P̂(k,l) = C_w · iσ ĥ(k,l) / { [1 − i m H_w] [1 + iσ τ_c] [1 + iσ τ_f] }.
    - m (vertical wavenumber, eq. 3): m = { [(N_m² − σ²)/σ²] (k² + l²) }^(1/2) (text extraction is garbled; verify).
    - σ = u·k + v·l (intrinsic frequency); k, l horizontal wavenumbers; H_w water-vapour scale height; N_m moist static stability frequency; τ_c conversion time; τ_f fallout time.
    - C_w (eq. 4): text extraction garbled; the abstract appears to give C_w = ρ_v0 (Γ_m/γ) with γ the ambient lapse rate and Γ_m the mean moist-adiabatic lapse rate. Verify before use.
  - Dynamics factor (1 − i m H_w) gives an upwind shift; cloud-time factors (1 + iστ) give a downwind shift. [B]
  - Efficiency numbers: PE_dyn = S_dyn/S_ref; PE_cloud = P/S_dyn. [B]
  - Negative precipitation is truncated: P_trun = max(P, 0). [B]
  - Example values in the abstract: N_m = 0.005 s⁻¹, wind 15 m/s, τ_c = τ_f = 1000 s, surface 280 K, 6.2 g/kg. [B]
- Field-tuned tau values (secondary, [Ö]): Oregon study gives roughly 500–5000 s from gauges and satellites (https://ams.confex.com/ams/pdfpapers/76934.pdf); a Stord campaign paper gives 350–500 s (https://ams.confex.com/ams/pdfpapers/114404.pdf); a non-linear comparison gives 100–300 s for both times.
- Roe (2005) describes the model as "a highly adaptable orographic precipitation model incorporating a linear atmospheric response and capable of efficient calculation over complex terrain", with microphysics as delay timescales. [B] (Roe 2005, see 1.3).

### 1.2 Python implementations
- PyPI `orographic-precipitation`, version 1.0, MIT licence, author listed as Raphael Lange; source repository per PyPI metadata: https://github.com/rlange2/orographic-precipitation [B-öz, PyPI JSON API: https://pypi.org/pypi/orographic-precipitation/json]. The HTML project page is JavaScript-only (ERİŞİLEMEDİ for HTML); the JSON API worked.
- The search also listed the same project under github.com/fastscape-lem/orographic-precipitation [Ö]. The GitHub URL returned HTTP 403 (ERİŞİLEMEDİ), so the repo owner could not be confirmed.
- API (PyPI 1.0 README) [B-öz]: `from orographic_precipitation import compute_orographic_precip`. Parameter dictionary keys:
  - `latitude` (40), `precip_base` (7, uniform precipitation rate), `wind_speed` (10), `wind_dir` (270, west), `conv_time` (1000 s), `fall_time` (1000 s), `nm` (0.005, moist stability frequency), `hw` (5000 m, water vapour scale height), `cw` (= ref_density × lapse_rate), `lapse_rate` (−5.8), `lapse_rate_m` (−6.5), `ref_density` (7.4e-3).
  - The README example uses a Gaussian hill: h_max = 500 m, σ = 15 km, centred at x0 = −25 km, in a 300 km × 250 km domain, to reproduce Fig. 4a–c of Smith & Barstad (2004).
- Version note [Ö]: 0.1 releases used different keys (`p0`, `windspeed`, `winddir`). Version 1.0 keys above are confirmed from the README, so use 1.0 names.
- R port (LTOP): https://rdrr.io/github/dschneiderch/LinearTheoryOrographicPrecip/src/R/LTmodel.R [Ö]. QGIS plugin "LinearTheoryOrographicPrecipitation" [Ö].
- Landlab `OrographicPrecipitator`: BULUNAMADI. The search returned no such component. The closest Landlab items are `SpatialPrecipitationDistribution` and `generate_spatial_precip` (with a Singer orographic rainfall function) at https://landlab.readthedocs.io/en/latest/reference/components/spatial_precip.html [Ö]. The Landlab components index URL returned 404 (ERİŞİLEMEDİ). Do not rely on this component name without checking the installed Landlab version.

### 1.3 Roe (2005), Annu. Rev. Earth Planet. Sci. 33, 645–671
- DOI 10.1146/annurev.earth.33.092203.122541. Full text read from the author's PDF: https://earthweb.ess.washington.edu/roe/Publications/Roe_OrogPrec_AnnRev05.pdf [B]. Publisher page returned 403 (ERİŞİLEMEDİ).
- Moisture scale height from linear T(z): saturated vapour density ρq_sat(z) = ρ_0 q0_sat exp(−z/H_m), H_m = −b/a (eq. 4); H_m ≈ 4 km in the tropics and ≈ 2 km at high latitudes; rule of thumb: a 10 °C fall halves the moisture. [B]
- Maximum precipitation tends to lie on windward slopes when peak elevations are comparable to H_m (2–4 km depending on latitude and season). [B]
- Precipitation efficiency = measured precipitation / S at the surface (Smith 1979). [B]
- Classes of orographic models: simple upslope models (Sawyer 1956; Smith 1979), linear models (Smith & Barstad 2004), seeder–feeder parameterisations, and full numerical models. [B]

### 1.4 Roe, Montgomery & Hallet (2003), J. Geophys. Res. 108(B6), 2315
- Correct title: "Orographic precipitation and the relief of mountain ranges" (the requested "relief-elevation relationship" title was not found). DOI 10.1029/2001JB001521. Full PDF read: https://earthweb.ess.washington.edu/roe/Web/GerardWeb/Publications_files/RoeEtal_Relief_JGR03.pdf [B].
- Bedrock river profile coupled to a physically based orographic precipitation model. [B]
- Feedback: dependence on slope gives a negative feedback on profile relief; dependence on elevation gives a positive feedback. The net effect depends on terrain geometry and orientation. [B]
- Relief responds to climate changes of realistic size; the response time matters. [B]
- Reference list item 10 gives a 1996 Nature citation for this title, which conflicts with the JGR 2003 record [Ö]. Treat as a metadata error.

### 1.5 Whipple & Meade (2004)
- Original paper: BULUNAMADI (not returned by search).
- Secondary [Ö] via Roe et al. (2008): analytical critical-wedge studies (Whipple & Meade 2004, 2006; Roe et al. 2006, 2008; Stolar et al. 2006, 2007; Tomkin & Roe 2007) give scaling relations that are insensitive to model details. The precipitation feedback sign can be negative or positive depending on whether precipitation rises or falls with orogen size.

---

## 2. Precipitation → erosion → tectonics feedback

### 2.1 Willett (1999), J. Geophys. Res. 104(B12), 28957–28981
- DOI 10.1029/1999JB900248 [Ö, EarthRef / BibBase]. Full text: ERİŞİLEMEDİ (agupubs returned 403). A Caltech journal-club PDF exists (http://www.tectonics.caltech.edu/meetings/journal_club/session4/Willett1999JGR.pdf) but was not read.
- Abstract-level [B-öz via search]: coupled tectonic deformation and fluvial erosion (stream-power law). A dimensionless erosion number (convergence rate, erodibility, precipitation) controls the time to steady state and belt shape. Asymmetric orographic rainfall is modelled; for the Southern Alps (New Zealand) and Cascadia, erosion was not efficient enough to reverse the topographic asymmetry. [Ö]
- Roe (2005) cites Willett (1999) for the link between erosion and mountain structure. [B]

### 2.2 Whipple (2009), Nature Geoscience, doi 10.1038/ngeo413 (published online 25 Jan 2009)
- Full text read from an Oregon State University PDF copy: https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2009_Whipple.pdf [B]. Nature page gives only the abstract and paywall [B-öz]: https://doi.org/10.1038/ngeo413. Issue and page numbers were not verified; cite by DOI.
- Erosion in critical-taper wedges is not simply passive; it strongly influences tectonic evolution. [B]
- Spatial correlations between intense precipitation or glaciation and fast rock uplift are common, but evidence that tectonics responds to climate (rather than merely coinciding with it) is rare. [B-öz, abstract]
- Expected coordinated response of a friction-dominated range to a climate-driven erosion increase: narrower range, temporary higher sediment yield, persistent higher uplift rate, reduced subsidence in adjacent basins. [B-öz, abstract]
- Best field cases: European Alps and St Elias range, Alaska. [B-öz, abstract]
- Erosion–uplift and rheology feedbacks can strengthen or alter coupling. [B]

---

## 3. Precipitation regimes, latitude and continentality

### 3.1 Köppen–Geiger maps: Beck et al. (2018), Sci. Data 5:180214
- DOI 10.1038/sdata.2018.214. Full text read from the open-access Nature page: https://www.nature.com/articles/sdata2018214 [B].
- 5 main classes, 30 sub-types, based on thresholds and seasonality of monthly temperature and precipitation (Peel et al. 2007 criteria) [B].
- 1-km resolution (0.0083°); present day 1980–2016; future 2071–2100 under RCP8.5 using 32 CMIP5 models with the anomaly method. [B]
- Present-day map ensemble: 3 temperature datasets (WorldClim V1 and V2, CHELSA V1.2) × 4 precipitation datasets (WorldClim V1 and V2, CHELSA V1.2, CHPclim V1), with topographic correction; each grid cell takes the most common class of 12 maps. [B]
- Accuracy against station data: 80.0% for the new map vs 66.1% (Kottek 2006), 70.9% (Peel 2007), and a third value for Kriticos et al. [B]. Mean confidence 92.6% for correctly classified stations (n = 17,667) and 77.4% for misclassified ones. [B]
- Data: GeoTIFF, unsigned 8-bit; maps at www.gloh2o.org/koppen and figshare. [B]
- Share of global land area in arid classes (BWh/BSh): BULUNAMADI. Not in the Beck 2018 text as fetched, and no other source returned it.
- Later Beck et al. (2023) [Ö]: about 5% of global land (excluding Antarctica) changed major Köppen class between 1901–1930 and 1991–2020; projected about 13% by 2071–2099 under SSP5-8.5.

### 3.2 Gridded climate datasets
- WorldClim 2: Fick & Hijmans (2017), Int. J. Climatol. 37(12), 4302–4315, DOI 10.1002/joc.5086 [Ö]. Cross-validation correlation for precipitation 0.86; for temperature 0.99 [Ö]. Source: https://fickse.github.io/files/Fick_International_Journal_of_Climatology_2017.pdf (PDF link from search; not read). Also worldclim.org.
- CHELSA: Karger et al. (2017), Sci. Data 4, 170122 [Ö, reference only]. Abstract not verified. Downloads: wsl.ch/lud/chelsa [Ö].
- Beck et al. (2018) use both as inputs (see 3.1) [B].

### 3.3 Continentality and rain shadows
- Continentality = reduced precipitation with distance from the ocean; strongest in winter for temperate and Mediterranean climates; rain shadows add to it on the lee side [Ö, ecology paper summary from search].
- Eurasian example (classic 1911 encyclopedia): inland rainfall decline is much faster where mountains lie close to the Pacific than in Europe [Ö]. The source is historical; treat as qualitative.
- Köppen-specific study on continentality thresholds: BULUNAMADI. The humid continental class description appears in textbooks only [Ö].

### 3.4 ITCZ and the Hadley/Ferrel structure
- ITCZ: rising branch of the Hadley cell near the equator; heavy rain; migrates seasonally, roughly 15°N–15°S, toward the summer hemisphere [Ö, course notes from search: https://courses.ems.psu.edu/meteo469/node/203].
- Subtropical highs near 30°: subsiding dry air, arid belts (Sahara, Namib, Kalahari) [Ö, same source and https://rmets.org/metmatters/global-atmospheric-circulation].
- Ferrel cell 30–60°: poleward flow from the subtropical high toward the subpolar low near 60°, deflected by Coriolis into mid-latitude westerlies; mid-latitude storms bring rain [Ö].
- Limit: why the Hadley cell ends near 30° is described as an open question in dynamical meteorology [Ö].

### 3.5 Held & Hou (1980)
- Held & Hou (1980), J. Atmos. Sci. 37, 515–533, DOI 10.1175/1520-0469(1980)037<0515:NASCIA>2.0.CO;2 [Ö]. Original not accessed (ERİŞİLEMEDİ for full text).
- Approximation: angular-momentum-conserving Hadley cell in a nearly inviscid atmosphere; annual-mean forcing; sin²φ depth-averaged RCE temperature profile [Ö, secondary, incl. Caballero et al. 2008]. Hadley width scaling for solstitial forcing: Caballero et al. (2008) [Ö].
- Caveat: real atmosphere violates angular-momentum conservation and energetic closure [Ö].

---

## 4. Simple global climate approaches

### 4.1 Energy-balance models
- North (1975) and Budyko–Sellers: zonal-mean energy-balance climate models with diffusive heat transport; Budyko and Sellers 1969 [Ö].
- Precipitation/hydrology parameterisation in North (1975): BULUNAMADI (search returned only temperature-model description).

### 4.2 Precipitation − evaporation (P − E)
- Zonal-mean pattern: P > E in the deep tropics; E > P in the subtropics (attributed to general subsidence); P > E again at mid to high latitudes [Ö, NCAR course text].
- Trenberth et al. (2007) on reanalysis water budgets: evaporation often exceeds precipitation over land in the tropics and subtropics, considered physically unrealistic in ERA-40 budgets [Ö].
- Uniform warming amplifies this pattern (more P − E in the tropics and high latitudes, less in the subtropics) [Ö, moist energy-balance study].
- Primary Trenberth subtropical-desert source: BULUNAMADI.

### 4.3 Practical implication for a simple model
- A zonal-band climate can be built from: (a) moisture-convergence bands (ITCZ at the equator, subtropical dry at about 30°, mid-latitude storm belt at 40–60°), (b) an exponential moisture scale height H_m ≈ 2–4 km for orographic lift (Roe 2005 [B]), (c) the Smith & Barstad (2004) transfer function on the terrain for the orographic part [B].
- For Köppen comparison, use the Beck et al. (2018) 1-km map or WorldClim/CHELSA as the reference [B].

---

## Source access summary
| Source | Status |
|---|---|
| Smith & Barstad 2004 (JAS) | ERİŞİLEMEDİ (full text); extended abstract read [B] |
| Roe 2005 (Annu. Rev.) | Full PDF [B] |
| Roe et al. 2003 (JGR) | Full PDF [B] |
| Whipple 2009 (Nat. Geosci.) | Full PDF via OSU copy [B]; Nature page abstract [B-öz] |
| Willett 1999 (JGR) | ERİŞİLEMEDİ (403); search summary [Ö] |
| Whipple & Meade 2004 | BULUNAMADI |
| Held & Hou 1980 | ERİŞİLEMEDİ; secondary [Ö] |
| Beck et al. 2018 | Full text [B] |
| PyPI orographic-precipitation | JSON metadata and README [B-öz]; HTML ERİŞİLEMEDİ (JS) |
| GitHub (rlange2 / fastscape-lem) | ERİŞİLEMEDİ (403, 404) |
| Landlab OrographicPrecipitator | BULUNAMADI |
| Trenberth primary (subtropical deserts) | BULUNAMADI |
| Köppen arid land share | BULUNAMADI |
