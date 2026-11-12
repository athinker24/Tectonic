# D. Testing and correcting Airy isostasy (research notes)

Status: in progress (started 2026-11-11). Sections are filled as sources are read.

## Plan
1. Global elevation vs crustal thickness (CRUST1.0, CRUST2.0, Mooney 1998, Szwillus 2019, LITHO1.0, Lachenbruch and Morgan 1990, Hasterok and Chapman 2007, Levandowski 2014, Afonso 2022).
2. Lithosphere vs crust contribution to elevation (thermal isostasy, Pratt).
3. Reference densities and reference crustal thickness.
4. Orogenic root density (eclogitization), Moho depth vs seismic Moho.
5. Dynamic topography (Flament 2013, Hoggard 2016, Conrad).
6. Cases: Alps, Tibet, cratons.
7. Densities for the tool.
8. Oceanic lithosphere depth vs age (Parsons and Sclater 1977, GDH1, Crosby and McKenzie 2009).


## Findings so far

### Dynamic topography (D4)
- Flament, Gurnis and Muller 2013 (Lithosphere 5(2):189-210, doi 10.1130/L245.1). Abstract: dynamic topography "relatively small (<2 km) in amplitude"; "at long wavelengths (>5000 km), there is good agreement between published residual topography fields ... and present-day dynamic topography predicted from mantle flow models"; residual and predicted fields show "peak-to-peak amplitudes of roughly +/-2 km and a dominant degree two pattern". Source: https://earthbyte.org/?p=710 (abstract copy). Also: "The best constraint on the present-day dynamic topography ... is likely the residual bathymetry calculated by removing the isostatic effect of oceanic lithospheric structure." Same source.
- Hoggard, White and Al-Attar 2016 (Nature Geoscience 9:456-463). Abstract: predictive models have "peak amplitudes of about +/-2 km, dominated by wavelengths of 10^4 km"; observations from 2,120 spot measurements "have typical peak amplitudes of +/-1 km and wavelengths of approximately 10^3 km"; "At longer wavelengths (such as 10^4 km), observed dynamic topography has peak amplitudes of about +/-500 m." Source: https://researchportalplus.anu.edu.au/en/publications/global-dynamic-topography-observations-reveal-limited-influence-o/
- Implication: long-wavelength (>1000 km) dynamic topography is of order +/-0.5 to 1 km; models of mantle flow predict up to +/-2 km. A tool should treat it as an optional, small term (a few hundred m) and not part of the Airy core.

### Seafloor depth (D8), partial
- Wikipedia "Seafloor depth versus age" (secondary, formulas not rendered in the text I got): cooling mantle model (1974) fits seafloor younger than about 80 Ma; cooling plate model (Parsons and Sclater 1977) fits better beyond about 80 Ma and gives nearly constant depth of "~6400 m" for very old seafloor; ridge crest depth "typically 2500 m" for eastern Pacific. Source: https://en.wikipedia.org/wiki/Seafloor_depth_versus_age  (UNVERIFIED against primary paper; formulas missing in text).
- Stein and Stein 1992 (Nature 359:123-129, doi 10.1038/359123a0). Abstract only accessible: joint fit of heat flow and bathymetry "yields a model with a hotter, thinner lithosphere than in previous models". Source: https://www.nature.com/articles/359123a0.pdf . The GDH1 coefficients were NOT in the accessible text. Search-only (UNVERIFIED): ~350 m/Ma^0.5 subsidence for seafloor younger than ~70 Ma (review summary text: https://mantleplumes.awh.durham.ac.uk/DLABook/Stein_Accepted.pdf was not readable, see failed fetches).
- Korenaga reanalysis (search summary only, primary not read): subsidence rate ~320 m/Ma^0.5 for seafloor younger than ~70 Ma, about 10% lower than conventional values including Stein and Stein 1992. Source: search result pointing to Korenaga PDFs (not read).
- Crosby and McKenzie 2009 (GJI, "An analysis of young ocean depth, gravity and global residual topography"): primary text NOT accessed (no open PDF found). Search summary says it proposed a revised age-depth curve adding a damped sinusoid to flattening beyond 80 Ma. Source only: https://data.zhenzhi.com/details/1/904180179/1/9 (catalog page). Ridge depth of 2500 m claimed in the query: NOT confirmed from a primary source here.

### Lamb et al. 2020 Global Whole Lithosphere Isostasy (G-cubed, doi 10.1029/2020GC009150)
- Data description (Zenodo record, primary-author data release): "Global whole lithosphere isostasy: implications for surface elevations, structure, strength and densities of the continental lithosphere". Data sets include "average elevation and crustal thickness of continental interiors ... using a standard lithospheric thickness of 100 km" and "crustal density perturbation ... calculated to give zero elevation anomaly" and "conductive lithosphere mantle density perturbation". Source: https://zenodo.org/record/4031646
- Abstract summary (secondary, from search snippet via https://openpolar.no/Record/ftdoajarticles:oai:doaj.org%2Farticle:4e3703bf1dd04ceeade5327ec1440663 , not fully read): lithospheric thickness exerts first-order control on continental elevations; crust-versus-lithosphere density contrasts of 300-550 kg/m3 (crust) and 20-40 kg/m3 (asthenosphere) are quoted in a search summary (UNVERIFIED wording).
- A popular write-up by Lamb (search summary, not read) states continental average elevations are "surprisingly insensitive to their average crustal thicknesses, contrary to Airy's prediction."

### Airy arithmetic (course notes, secondary)
- Airy root: r = (rho_c / (rho_m - rho_c)) * h, with rho_c 2800, rho_m 3300 gives r = 5.6 h (root of 22.4 km for 4 km elevation). Source (course sheet, search only): https://www.geologyrocks.co.uk/people/pinter/pdf/IsostasyExercise.pdf (reference C0 = 35 km, not read in full).
- Slide deck (ICTP, Lamb lecture; search summary only): roughly 7.3 km of crust per 1 km elevation for dry crust, ~5.1 km with water. Source: https://indico.ictp.it/event/10509/session/94/contribution/339/material/slides/0.pdf (UNVERIFIED, slides).

### Sediment, Airy, Pratt
- Pratt vs Airy: qualitative comparison from course search summary (not a primary source).


### Zoback and Mooney 2003 (PRIMARY, read as PDF) - the key global test
- Citation: Zoback, M.D. and Mooney, W.D. 2003, "Lithospheric buoyancy and continental intraplate stresses", International Geology Review (file name 2003_IGR_LithoBuoyancy). Read from https://escweb.wr.usgs.gov/share/mooney/2003_IGR_LithoBuoyancy.pdf (USGS-hosted PDF, 10 pp.).
- Method: Lachenbruch and Morgan (1990) isostatic model. Elevation of a lithospheric column with crust (Lc, rho_c) and mantle lid (Lm, rho_m) floating on asthenosphere rho_a: Eq. (2b) eps = [(rho_a - rho_L)/(rho_a - rho_w)] L - H0, with H0 = 2.78 +/- 0.35 km (Eq. 3, the buoyant height of sea level, calibrated on mid-ocean ridges using a Table 1 of ridge-crest values).
- Crustal part, Eq. (4): Hc = (1/rho_a)(rho_a - rho_c) Lc - 2.78 km. Mantle part, Eq. (5): Hm = (1/rho_a)(rho_a - rho_m) Lm. Reference asthenosphere rho_a = 3300 kg/m3 used in predictions. (Source: the PDF above.)
- My derivation from Eq. (4) (not stated as such in the paper): with rho_a = 3300 and rho_c = 2800, a crust of 18.3 km gives zero crustal-buoyancy elevation (2.78 x 3300/500). This is the "sea level" crust for the crust-only term, not a physical reference thickness.
- Database: USGS global crustal database of more than 1700 seismic refraction models (Mooney et al. 1998, 2002), each with elevation from ETOPO5 averaged over 50 km radius.
- Results (quotes from the paper):
  - "a simple relationship between crustal thickness and surface elevation does not exist. ... major regions of the crust at or near sea level (0-200 m elevation) have crustal thicknesses that vary between 25 and 55 km."
  - Predicted crustal-buoyancy elevation exceeds observed in 97% of data; on average "1.73 +/- 0.95 km higher than the observed elevations." The difference is attributed to the mantle lid (dense lid pulls crust down).
  - Airy-type correlation (thicker crust = higher) only at extremes: crustal thickness > 55 km or < 20 km.
  - Mean crustal density increases with thickness: about 2764 kg/m3 for 25 km crust vs 2947 kg/m3 for 50 km crust (6.5% difference), except the thickest crust (> ~55 km), where density is lower. Mechanism suggested: thickening by lower crust flow or mafic underplating.
  - Density from velocity: rho = 1741 Vp^0.23 for sediments (Vp < 4.5 km/s; Gardner et al. 1974); crystalline rocks from Christensen and Mooney 1995 regressions rho = A + B Vp (Table 2 of paper); water 1050 kg/m3.
- Lithosphere thickness from buoyancy: good agreement with seismic lithosphere except cratons, where the model gives only 40-60% of seismic 200-350 km; reconciled by lowering cratonic mantle-lid density by about 1%.
- Consequence for a tool: a pure crust-thickness Airy predictor has no skill across the typical 25-55 km range. Mantle lid buoyancy must be part of the model, and the crust density should rise with thickness.

### Christensen and Mooney 1995 (search summary only, primary not read)
- Global weighted mean crustal thickness 41.1 km; mean crustal Vp 6.45 km/s; mean density 2830 kg/m3; mean SiO2 61.8%. Extended crust about 30.5 km, orogens about 46.3 km. Sources: https://rjes.wdcb.ru/v19/2019ES000692/refsdir-692/Chri95.html and https://usgs.gov/publications/seismic-velocity-structure-and-composition-continental-crust-a-global-view (search summary, UNVERIFIED wording). Note: the mean 41.1 km is inconsistent in the literature (Chulick and Mooney 2002 quoted as 39.2 km +/- 8.5 in a search summary, UNVERIFIED).


### Lachenbruch and Morgan 1990 (abstract, USGS record)
- Lithosphere modeled as floating on a uniform-density asthenosphere with no flexural strength; "simple graph relating elevation to lithosphere density and thickness" and mass-balance "rules of thumb". Great Basin mean elevation of about 1.75 km "probably requires substantial low-density magmatic contributions"; "Even models with a high initial elevation typically call for 10 km or so of accumulated magmatic material of near-crustal density." Source: https://pubs.usgs.gov/publication/70016328 (Tectonophysics 174:39-62, doi 10.1016/0040-1951(90)90383-J). Full text not read.
- Calibration (from Zoback and Mooney 2003, above): H0 = 2.78 km from mid-ocean ridge column.

### Korenaga et al. reference model (manuscript PDF, read) - oceanic depth formula
- Source: "A new reference model for the evolution of oceanic lithosphere in a cooling Earth", T. Korenaga, J. Korenaga, H. Kawakatsu, M. Yamano, manuscript submitted to JGR Solid Earth. Read from https://par.nsf.gov/servlets/purl/10317139 (PDF). Year not stated in the copy read.
- Their Eq. (10): seafloor depth d(t) = d0 + d1 sqrt(t) + d2 tanh(e2 t), with d0 = 2600 m, d1 = 409 m/Ma^0.5, d2 = 930 m, e2 = 0.018 /Ma; "valid up to t = 200 Ma, RMS error ~0.7%". The text says the second term is thermal contraction and the third is the spinel-to-garnet transition.
- Sign check (my computation): as printed (+d2), depth reaches 7.1 km at 80 Ma and 9.3 km at 200 Ma, which contradicts the observed plateau near 5.5-6 km. With -d2, depth is 5.4 km at 80 Ma and 5.8 km at 100 Ma. So the printed sign or the coefficient set is not reliable from this extraction. UNVERIFIED: do not hard-code these numbers without checking Eq. (10) in the typeset paper.
- Same paper: "Their reexamination ... yielded a subsidence rate of ~320 m Ma^-1/2 for seafloor younger than ~70 Ma ago, which is ~10% lower than conventional estimates (Parsons and Sclater 1977; Stein and Stein 1992; Carlson and Johnson 1994; Smith and Sandwell 1997)." Half-space cooling with realistic properties predicts 400-500 m/Ma^0.5 (their statement, citing Korenaga and Korenaga 2016).
- Global average ridge depth: "~2.85 +/- 0.5 km (Gale et al., 2014)" as quoted in Richards et al. 2018 (below).

### Richards et al. 2018 (JGR Solid Earth 10.1029/2018JB015998, PDF read)
- Source: https://freddrichards.github.io/documents/papers/richards_etal_2018_jgr.pdf
- Plate model fits of combined subsidence and heat flow give T = 1495 C, zp = 105 km, zero-age ridge depth zr = 2.22 km. Stated: "a predicted zero-age ridge depth of zr = 2.22 km is also markedly shallower than the global average of ~2.85 +/- 0.5 km (Gale et al., 2014)". So the 2500 m ridge depth in the tool brief is below the global average in this paper.
- Parsons and Sclater 1977 fit to subsidence alone: T = 1307 C, zp = 129 km; their original: T = 1350 +/- 275 C, zp = 125 +/- 10 km. Stein and Stein 1992 joint fit: T = 1450 C, zp = 90 km (as quoted by Richards et al.).
- Residual depth anomalies with half-space reference: "significantly offset away from zero"; with optimal plate model: symmetric, standard deviation +/-0.65 km (Richards et al. 2018, Fig. 11).
- Flattening of subsidence after ~60 Ma is "a general feature of old oceanic lithosphere (Korenaga, 2015)".
- Crosby et al. 2006 (GJI 166:553-573, doi 10.1111/j.1365-246X.2006.03015.x) cited as using near-zero gravity anomaly to identify normal seafloor. Not read.

### Christensen and Mooney / Mooney CRUST: search-only items (not read)
- CRUST1.0 poster (Laske, Masters, Ma, Pasyanos; EGU2013-2658), read from https://igppweb.ucsd.edu/~gabi/crust1/laske-egu13-crust1.pdf : model is 1 degree; each cell gives boundary depths and Vp, Vs, density for 8 layers: water, ice, 3 sediment layers, upper, middle and lower crystalline crust. Topography and bathymetry from ETOPO1. Moho depth from surface observations, with extrapolation where data are missing. Poster says CRUST2.0 tried to represent crustal thickness within +/-5 km; CRUST1.0 validated against Rayleigh wave group velocity maps. Poster is an abstract-level source, not peer reviewed.
- LITHO1.0: Pasyanos et al. 2014, JGR 119(3):2153-2173, doi 10.1002/2013JB010626 (search result, not read). CRUST1.0 is its starting crust.
- Mooney et al. 1998 (CRUST 5.1), Chulick and Mooney 2002 (world continental average 39.2 km, s.d. 8.5 km, UNVERIFIED search summary).

### Tibet (Murodov et al. 2022, Frontiers in Earth Science 10:821497, PDF read)
- Source: https://www.frontiersin.org/articles/10.3389/feart.2022.821497/pdf
- Moho depth increases from ~50 km beneath the Himalayas to ~90 km in the thickest crust in the western Qiangtang region (~36.2 N, 78 E) (paper's review, PDF line on Moho depth). Pamir maximum crust 78 +/- 3 km (same paper, review of earlier work).
- Search-only (UNVERIFIED wording): NE Tibet receiver-function study finds crust thinner than simple Airy predicts where elevation exceeds 3.0 km, attributed to upper-crustal shortening or lower-crustal extrusion (source: https://vufind.katalog.k.utb.cz/... search record; not read).
- My arithmetic (not from a source): for rho_c 2800, rho_m 3300, reference crust 35 km and 5 km elevation, Airy root = 5.6 x 5 = 28 km, total 63 km.

### Alps (search summary, Kissling et al. 2017 Tectonics: boris.unibe.ch PDF was blocked by a bot-check page, NOT read)
- Search summary: crustal root "almost 60-km thick," "far out of conventional Airy-isostatic equilibrium with a mean surface topography of only about 2 km"; compensation by a deep crustal root plus mantle slab (UNVERIFIED, from search snippet).
- Eastern Alps gravity study: crust-mantle density contrast of about 350 kg/m3 (search snippet, UNVERIFIED).

### Cratons (search summaries only)
- Southern African cratons stand 500-700 m higher than other cratons (except Tanzanian); excess elevation "cannot be explained by lithospheric structure within the petrologically permitted range of mantle densities" and needs sublithospheric support (search snippet, study not identified; UNVERIFIED).
- Stamps et al. (African superswell): anomaly ~500 m higher on average than global mean (search snippet, UNVERIFIED).
- Zoback and Mooney 2003 (read): cratonic mantle lid must be about 1% less dense than elsewhere to match 200-350 km lithosphere (see above).

### Failed or blocked (for the failed-fetch list)
- https://topex.ucsd.edu/geodynamics/parsons_sclater77.pdf: TLS "unable to get local issuer certificate" with default curl and with /root/.ccr/ca-bundle.crt. Not bypassed.
- https://mantleplumes.awh.durham.ac.uk/DLABook/Stein_Accepted.pdf: same TLS error; retried with the proxy bundle, connection reset.
- https://people.earth.yale.edu/sites/default/files/korenaga08b.pdf and korenaga21b.pdf: CONNECT 502 from proxy.
- https://boris.unibe.ch/113826/1/Kissling_et_al-2017-Tectonics.pdf: bot-check HTML page, not content.
- https://se.copernicus.org/articles/8/899/2017/se-8-899-2017.pdf: no text extracted.
- https://espace.curtin.edu.au/handle/20.500.11937/74829 (Kirby 2019): no text extracted.
- https://ds.iris.edu/ds/products/emc-crust1-0/ and emc-litho1-0: no model text extracted (106 chars).
- https://www.nature.com/articles/359123a0.pdf: only the abstract is free (6.5 KB text).
- Crosby and McKenzie 2009 GJI: no open PDF found in search.
- Levandowski 2014 global paper and Afonso 2022 global LitMod paper: not found by search.
- Coblentz et al. (Durham copy) : cannot be read (see TLS failure above).


### Steinberger, Conrad, Osei Tutu, Hoggard 2019 (Tectonophysics 760:221-228, PDF read)
- Source: https://gfzpublic.gfz-potsdam.de/pubman/item/item_4381899_3/component/file_4384888/4381899.pdf
- Combines Hoggard et al. 2016 oceanic residual topography with CRUST1.0 continental constraints; compares to mantle-flow predictions. Abstract: "relatively good overall agreement and amplitude spectra with similar slopes, except for degree two (> 10,000 km wavelengths) where predicted amplitude is more than two times as large."
- Intro: "most geodynamic models of global mantle flow produce patterns of dynamic topography with long-wavelength amplitudes of about 1-km or more (see Flament et al. (2013)...)"; "As far as we know, the present answer is no" regarding independent evidence for ~1 km degree-2 topography.
- Use for the tool: long-wavelength dynamic topography of about 0.5 to 1 km is the observationally supported range; models with 1 to 2 km are high.

### Szwillus et al. 2019 (JGR Solid Earth 124(2):1626-1652, doi 10.1029/2018JB016593) - search summaries only
- Geostatistical global Moho depth and average crustal Vp maps, about 0.72 degree resolution, with interpolation error (conference abstract; Africa Knowledge Platform, https://africa-knowledge-platform.ec.europa.eu/node/45857 ; EOS highlight https://eos.org/editor-highlights/new-global-crustal-model-built-as-foundation-for-future-studies).
- Agrees with CRUST1.0. Moho uncertainty below 4 km in North America and Europe, 10 km or more in most of Africa (UNVERIFIED wording, not read verbatim).
- Verbatim JGR abstract and average crustal velocity values NOT read.

### Afonso et al. 2019 (LithoRef18, GJI 217(3):1602-1628, doi 10.1093/gji/ggz094) - search summary only
- Joint inversion of gravity, geoid, seismic data with priors. Outputs: crustal thickness and density, lithospheric thickness, lithospheric mantle density vs depth, geotherms, sublithospheric density to 410 km. Data at https://www.earthbyte.org/webdav/ftp/earthbyte/gplates_portal/Afonso_etal_lithospheric_thickness_GJI2019/ (folder, not read).
- The 2022 LitMod global paper requested in the brief was NOT found; this 2019 paper is the closest match I could identify.

### Sediment density (search summaries, primary not read)
- Brief's range 2000-2500 kg/m3 NOT confirmed. A marine sediment density source (search summary) gives average estimates of 1.7 to 1.95 g/cm3 (1700-1950 kg/m3). Bulk density in backstripping models is computed from grain density and porosity, with porosity phi(z) = phi0 exp(-z/z0) (Sclater and Christie 1980, JGR 85:3711-3739; North Sea parameters; excerpt https://assets.cambridge.org/97811084/46969/excerpt/9781108446969_excerpt.pdf ). CONFLICT with the brief: treat 2000-2500 as a range that needs checking, and compute from porosity if the tool models sediments.

### Eclogite density (search summaries)
- Eclogite density at standard conditions about 3.45-3.75 g/cm3 vs peridotite 3.3-3.47 (secondary summary; source https://core.ac.uk/download/19158705.pdf or similar, UNVERIFIED which). Densification of up to about 10% (about 300-600 kg/m3) cited as an upper bound in a secondary summary. Gabbro-to-eclogite conversion incomplete in exposed lower crust and controlled by fluid abundance. Arc lower crust foundering when density exceeds mantle (about 3.33 g/cm3) (Scientific Reports, s41598-017-13221-6, search snippet).
- Jull and Kelemen 2001 (JGR; search snippet only): lower crustal lithologies can be denser than mantle by roughly 50-250 kg/m3, depending on composition, temperature, pressure. Not read.
- Ducea, Saleeby, Hacker 2015 review: NOT found.

### Dynamic topography extra (search snippets)
- Conrad and Husson 2009 type models: long-wavelength DT about 1-2 km, overpredicting degree 2 (search summary, not read). Conrad 2013 and "2019 Conrad" not found.

### Kirby 2019 "On the pitfalls of Airy isostasy" (search summary, record not readable)
- Argues Airy inability to represent actual compensation is well documented. https://espace.curtin.edu.au/handle/20.500.11937/74829 (no text extracted).

## Consolidated assessment for the tool (Topic D)

1. Global test. Crustal thickness alone does not predict elevation. Zoback and Mooney (2003) on 1700+ USGS crustal models: no relation for crust 25 to 55 km near sea level; Airy-type correlation only at extremes (<20 or >55 km). Crustal-only buoyancy overpredicts elevation in 97% of sites by 1.73 +/- 0.95 km. A pure Airy tool therefore misses most continental elevation variance and must include a mantle-lid term.
2. Lithospheric mantle term. Lachenbruch and Morgan (1990) model with H0 = 2.78 +/- 0.35 km, rho_a = 3300 kg/m3: Hm = (rho_a - rho_m)/rho_a x Lm (negative contribution). Lamb et al. 2020 (data release; abstract not read) report lithosphere thickness as first-order control and cite density contrasts of 300-550 kg/m3 (crust) and 20-40 kg/m3 (asthenosphere), UNVERIFIED.
3. Densities to adopt (defaults, with ranges). Mantle lid and asthenosphere 3300 kg/m3 (Zoback and Mooney Table 1 uses 3300; asthenosphere 3300). Crust 2800 kg/m3 (Christensen and Mooney 1995 mean 2830; ZM03 reports 2764 at 25 km and 2947 at 50 km, so make crust density increase with thickness). Water 1030 kg/m3 (Table 1 entries 1000-1030). Sediments: use porosity law, range 1700-2500 kg/m3, default 2200 is my suggestion, UNVERIFIED.
4. Reference thickness. Crust-only sea-level thickness depends on densities: 18.3 km (my derivation from ZM03 Eq. 4 with rho_c 2800). Continental mean thickness 39 to 41 km (Christensen and Mooney 1995 41.1 km; Chulick and Mooney 2002 39.2 km; search only). The "35 km reference" in the brief is a course-sheet value, not from a primary source here.
5. Orogenic roots. Airy root for 5 km elevation with 2800/3300: 28 km (5.6 ratio). Observed roots: Tibet ~70 km crust at ~5 km elevation (Murodov 2022 review: 50 km Himalaya, up to 90 km Qiangtang); Alps ~55-60 km at ~2 km (search). Both imply root-to-elevation ratios above Airy, consistent with mantle-lid or dynamic support and with eclogite densification (up to ~300-600 kg/m3 densification, UNVERIFIED primary). Tool should allow a crustal density increase in roots or a mantle-lid term, and must not fix the root from elevation alone.
6. Cratons. Excess elevation 500-700 m in southern African cratons not explained by depletion alone (search snippet); Zoback and Mooney reproduce 200-350 km cratonic lids with 1% lower density.
7. Dynamic topography. Long-wavelength (>5000 km) agreement with models; amplitude +/-2 km predicted vs +/-0.5 to 1 km observed (Hoggard 2016 abstract; Steinberger 2019). Tool default: optional term of +/-0.5 km at >1000 km wavelength, off by default.
8. Oceanic seafloor. Depth d(t) about 2500-2600 m at ridge (GDH1 family, search) but Richards et al. 2018 quote a global average of 2.85 +/- 0.5 km. Korenaga reference model: d0 = 2600 m, d1 = 409 m/Ma^0.5, d2 = 930 m, e2 = 0.018/Ma, sign of d2 ambiguous in extracted text (use only after checking). Old-seafloor plateau about 5.5 to 6.4 km (search, Wikipedia says ~6400 m under cooling plate; UNVERIFIED). Ocean basins 5.5 to 6 km deep plausible. Tool should use a verified formula, check Parsons and Sclater 1977 and Stein and Stein 1992 full text (not accessible here).

## Key takeaways for the tool (summary)
- Do not use a single Airy rule. Use Airy plus a lithospheric mantle lid term (Lachenbruch and Morgan 1990 form) with rho_a = 3300.
- Default densities: asthenosphere 3300; crust 2800 with optional increase with thickness (2764 at 25 km to 2947 at 50 km, ZM03); water 1030; sediments need porosity-based treatment, range 1700-2500 (conflict with brief's 2000-2500).
- Reference: crustal thickness at sea level depends on densities (18.3 km crust-only in the ZM03 form); mean continental crust 39-41 km.
- Expect residuals of about 1.7 +/- 1.0 km from crust-only Airy (ZM03). Plan for it.
- Orogenic roots: allow crust thicker than Airy for given elevation (Tibet, Alps). Use eclogite densification as an option (up to ~300-600 kg/m3, unverified primary), not a default.
- Dynamic topography: optional, +/-0.5 to 1 km at long wavelength.
- Oceans: ridge depth 2500-2600 m (GDH1 family; global average quoted 2.85 km), deep basins 5.5-6.4 km; formula must be verified from primary (Stein and Stein 1992 Eq. not readable).

## URLs read (full text or usable content)
- https://escweb.wr.usgs.gov/share/mooney/2003_IGR_LithoBuoyancy.pdf (Zoback and Mooney 2003, PDF)
- https://pubs.usgs.gov/publication/70016328 (Lachenbruch and Morgan 1990 abstract)
- https://www.usgs.gov/publications/continental-extension-magmatism-and-elevation-formal-relations-and-rules-thumb (same record)
- https://par.nsf.gov/servlets/purl/10317139 (Korenaga et al. reference model manuscript, PDF)
- https://freddrichards.github.io/documents/papers/richards_etal_2018_jgr.pdf (Richards et al. 2018, PDF)
- https://www.frontiersin.org/articles/10.3389/feart.2022.821497/pdf (Murodov et al. 2022, PDF)
- https://igppweb.ucsd.edu/~gabi/crust1/laske-egu13-crust1.pdf (CRUST1.0 poster, PDF)
- https://gfzpublic.gfz-potsdam.de/pubman/item/item_4381899_3/component/file_4384888/4381899.pdf (Steinberger et al. 2019, PDF)
- https://www.nature.com/articles/359123a0.pdf (Stein and Stein 1992, abstract only)
- https://earthbyte.org/?p=710 (Flament et al. 2013 abstract)
- https://researchportalplus.anu.edu.au/en/publications/global-dynamic-topography-observations-reveal-limited-influence-o/ (Hoggard et al. 2016 abstract)
- https://en.wikipedia.org/wiki/Seafloor_depth_versus_age (secondary)
- https://zenodo.org/record/4031646 (Lamb et al. 2020 data description)
- https://doaj.org/... and openpolar.no record for Lamb et al. 2020 (abstract snippet only)
- https://eos.org/editor-highlights/... and https://africa-knowledge-platform.ec.europa.eu/node/45857 (Szwillus summaries)
- https://www.earthbyte.org/... (Afonso 2019 folder listing, not read)

## Failed or blocked fetches
- https://topex.ucsd.edu/geodynamics/parsons_sclater77.pdf: TLS "unable to get local issuer certificate", also with /root/.ccr/ca-bundle.crt. Not bypassed.
- https://mantleplumes.awh.durham.ac.uk/DLABook/Stein_Accepted.pdf: TLS error, then connection reset.
- https://people.earth.yale.edu/sites/default/files/korenaga08b.pdf and korenaga21b.pdf and korenaga15a_0.pdf: proxy CONNECT 502.
- https://boris.unibe.ch/113826/1/Kissling_et_al-2017-Tectonics.pdf: bot-check page.
- https://se.copernicus.org/articles/8/899/2017/se-8-899-2017.pdf: no text extracted.
- https://espace.curtin.edu.au/handle/20.500.11937/74829 (Kirby 2019): no text.
- https://ds.iris.edu/ds/products/emc-crust1-0/ and emc-litho1-0: no model text (106 chars).
- https://pmc.ncbi.nlm.nih.gov/articles/PMC6941964: no text.
- https://core.ac.uk/download/228204057.pdf (Lamb 2020 full text): HTML, not PDF.
- https://core.ac.uk/download/288380902.pdf: no text.
- https://www.earthbyte.org/Resources/Pdf/Muller_Seton_...pdf: 404.
- https://uchicago.cottagelabs.com/... (Oceanic axial depth): no text.
- Not found by search: Crosby and McKenzie 2009 full text, Levandowski 2014 global paper, Afonso 2022 global LitMod paper, Conrad 2013, Ducea et al. 2015, Hasterok and Chapman 2007 full text (abstract only via Adelaide repository), Lachenbruch-Morgan full text, Jull and Kelemen 2001 full text, Christensen and Mooney 1995 full text, Mooney et al. 1998 full text (ifremer returned HTML).

## Dash check
