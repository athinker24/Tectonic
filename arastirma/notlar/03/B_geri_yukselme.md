# B: Isostatic response to erosion and sedimentation (working notes)

Status: IN PROGRESS. Early search-level findings; primary text checks pending.

## Corrections to the brief (found while searching)
- Champagnac et al. 2007 is in GEOLOGY (vol 35, DOI 10.1130/G23053A.1), title "Quaternary erosion-induced isostatic rebound in the western Alps". Not Nature Geoscience. Source: https://data.zhenzhi.com/details/1/908083990 (search metadata, to be verified against the PDF)
- Whipple 2009 is "The influence of climate on the tectonic evolution of mountain belts", Nature Geoscience 2, 97-104, DOI 10.1038/ngeo413. Source: https://www.doi.org/10.1038/NGEO413 (search metadata)
- Garcia-Castellanos 2002 is "Interplay between lithospheric flexure and river transport in foreland basins", Basin Research 14, 89-104, DOI 10.1046/j.1365-2117.2002.00174.x. Source: https://csdms.colorado.edu/wiki/Reference:Reference-000402 (search metadata)
- Molnar and England 1990 is Nature 346, 29-34 (doi 10.1038/346029a0). The "0.17" figure was NOT confirmed by any search result. UNVERIFIED until the text is read.

## Findings so far (search-level; primary text pending)
- Molnar & England 1990 argue that inferred recent uplift signals (deep incision, late Cenozoic coarse sediment, palaeobotany) can come from climate cooling, with a feedback loop climate -> weathering -> erosion -> isostatic rebound. They distinguish rock uplift from surface uplift; many inferred uplift values are actually rock uplift or exhumation. Source: https://www.nature.com/articles/346029a0.pdf (abstract text via search snippet, to verify)
- Montgomery & Brandon 2002, EPSL 201, 481-489, DOI 10.1016/S0012-821X(02)00725-2. 10 m DEM transect across the Olympic Mountains: non-linear erosion vs mean slope; global 1 km comparison; relief plays a minor role in landscape-scale erosion in active ranges. Source: https://repository.geologyscience.ru/handle/123456789/28097 (abstract/metadata only).
- Champagnac et al. 2007 (Geology): erosion-induced isostatic response is a significant part of western Alps rock uplift, high since the Pliocene; uses flexure (finite elastic thickness widens affected area compared to erosion area). Later 2009 Tectonophysics work: up to ~50% of modern geodetic rock uplift is erosion-driven (secondary, via search summary of Elements 2021; UNVERIFIED primary).

## VERIFIED from full text (primary PDFs read)

### Molnar & England 1990, Nature 346, 29-34 (full text read)
Source: https://www.tectonics.caltech.edu/meetings/journal_club/session2/Molnar_and_England1990Nature.pdf (also https://www.nature.com/articles/346029a0.pdf)
- Local Airy isostasy (Archimedes applied to crust over mantle): removing a crustal layer of thickness dT and density rho_c, compensated by a root in mantle of density rho_m, lowers the surface by dT (rho_m - rho_c)/rho_m = dT/6 (paper writes this with rho_c/rho_m = 5/6 implied). So the 0.17 is confirmed as dT/6 = 0.17 dT, i.e. 0.17 km of mean-elevation lowering per km of rock removed.
- Rock (including the Moho) rises by 5/6 dT in that case. Their Fig. 2 caption: exhumation of dT gives rock uplift of 5/6 dT but mean elevation lowered by dT/6, unless tectonic thickening replaces the lost crust.
- Worked example in text: a region of mean elevation h eroded rapidly can become peaks at 2h with valleys near sea level, but mean elevation falls to 0.83h.
- Alps example: de Sitter's inferred 2000 m of Pliocene uplift could be partly isostatic response to valley incision; isostatic lowering of the present mean elevation is only ~0.17 km for the removed rock thickness they assume (Fig. 2).
- Definitions: uplift of rock relative to sea level = surface uplift + exhumation (their sum statement). Exhumation = thickness of rock removed from the surface. Many inferred recent uplifts are based on rock uplift or exhumation, not surface uplift.
- Assumptions: local (Airy) compensation, no flexural strength, simple density contrast. Feedback climate -> erosion -> rebound is proposed as a hypothesis.

### Champagnac, Schlunegger, Norton, von Blanckenburg, Abbuhl, Schwab 2009, Tectonophysics 474, 236-249, DOI 10.1016/j.tecto.2009.02.024 (full text read)
Source: https://gfzpublic.gfz-potsdam.de/pubman/item/item_238796_1/component/file_238795/13194.pdf
- Density values rho_c ~2.8, rho_m ~3.25 g/cm3 (Okaya 1996; Vigano and Martin 2007 cited). They state the isostatic response is ~5/6 (~80%) of erosional unloading. Correct form: rock uplift = dT * rho_c/rho_m; surface lowering = dT * (1 - rho_c/rho_m); the two sum to dT (exhumation). With their densities rho_c/rho_m = 0.86 and surface share 0.14; the 5/6 is rounded (ratio 0.83). Ratio erosion/rock uplift ~0.8 is expected for purely erosion-driven rock uplift with zero flexural rigidity.
- Central Alps regression rock uplift vs denudation slope 0.88 +/- 0.14 (paper Fig. 5). Intercept -0.03 +/- 0.09 mm/yr; rock uplift accounts roughly for 90% of denudation rate (section 3.5).
- Elastic thickness Te = 10-20 km (Steward and Watts 1997), or close to Airy (Lyon-Caen and Molnar 1989). Model: 2D elastic flexure with Te 10 km, E = 1e11 Pa, crustal density 2.8, Poisson 0.25, 100 km boundary extension, instantaneous, no time dependence, assumes isostatic equilibrium before loading. Result: max rock uplift ~ +0.8 mm/yr in core; fits 75% of observations; overpredicts foreland by ~0.2 mm/yr and underpredicts southern flank by ~0.2 mm/yr.
- Rock uplift defined per England and Molnar 1990 (paper's citation).

### Whipple 2009, Nature Geoscience 2, 97-104, DOI 10.1038/ngeo413 (full text read)
Source: https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2009_Whipple.pdf
- In a fixed-width block-uplift model, near-surface rock uplift U = c F_A / W, c = isostatic compensation factor, "c ~ 1/5 for Airy isostasy" (cites ref 39). Note this differs from the 1/6 of Molnar and England 1990 (different definition: fraction of added mass going to root per unit width, not dT/6); treat as UNVERIFIED equivalence.
- Steady state: erosion rate equals F_A/W; near-surface rock uplift balances erosion (U = F_A/W everywhere).
- Transient: erosional efficiency increase gives passive isostatic rebound; erosion exceeds F_A/W temporarily, excess rock from topography and crustal root goes to basins.
- Isostatic rebound to erosional unloading "operates even in inactive mountain ranges" (ref 51).
- Whipple argues steady erosion-uplift balance and isostatic rebound alone do not demonstrate a profound climate-tectonics link.

### Braun & Robert 2005, Earth Surf. Process. Landforms 30, 1203-1225, DOI 10.1002/esp.1271 (full text read)
Source: https://www.isterre.fr/IMG/pdf/Braun-and-Robert-ESPL2005.pdf
- Weight balance of a reference column (crust h, mantle L, compensation depth h+L+d) after erosion E0. Eq (2) as extracted: u = E0 * rho_c/rho_a with a denominator lost in extraction. Caption: "For typical density and crustal thickness values, u = 4 to 5 x E0". UNVERIFIED: the printed eq (2) and the caption disagree; rho_c/(rho_a - rho_c) gives ~4.3 with their densities, which fits the caption. Treat the exact form as needing the PDF figure check.
- Eq (3): E = dh / (1 - rho_c/rho_a) = dh * rho_a/(rho_a - rho_c). With rho_c = 2600, rho_a = 3200 kg/m3: factor 5.3, i.e. for each km of topography reduction ~5.3 km of crust must be eroded (checked arithmetic: 1/(1-0.8125)=5.33). Equivalent to surface lowering fraction 0.19 per km eroded, close to Molnar and England 0.17.
- Flexure: D w'''' + (rho_a - rho_s) g w = q(x) (eq 4 in text; standard Turcotte-type). Elastic thickness constrained to 10-30 km for the Dabie Shan (abstract). Mean exhumation 0.01-0.04 km/Myr in Dabie Shan; topography decays at constant rate since ~100 Ma. Trade-off between Te, exhumation and relief loss.
- Post-orogenic decay: erosion of topography can produce tens of km of exhumation per km of relief lost. (Text, p.1205.)

### Sternai et al. 2019, Earth-Science Reviews 190, 589-604, DOI 10.1016/j.earscirev.2019.01.005 (full text read)
Source: https://boa.unimib.it/bitstream/10281/229017/2/Sternai%20et%20al.%2c%202019.pdf
- Observed present uplift ~2-2.5 mm/a in NW and Central Alps, ~1 mm/a across Eastern to SW Alps (abstract/text).
- Mechanisms: deglaciation (since LGM), long-term erosion, slab detachment, mantle deflection.
- Viscoelastic relaxation timescale tau = 2 eta / E (eta mean asthenospheric viscosity, E elastic modulus), used as system response timescale (Sec 3.1.1; cites Turcotte and Schubert 2002, Watts 2009).
- Isostatic models from deglaciation account for ~10-30% of the geodetically observed uplift in the Western/Central Alps and up to ~50% in the Eastern Alps (text Sec 3.1). LGM ice melt accounts for ~90% of the deglaciation part in some models.
- Erosion-driven: Champagnac et al. 2007 constrained erosion unloading via elastic flexure; Mey et al. 2016 (viscoelastic, Te averaging 20 km) give maximum post-LGM erosion + sediment redistribution uplift up to ~0.5 mm/a in Central Alps (cited in review, text Sec 3.1).
- Conclusion (abstract): lithospheric adjustment to deglaciation and erosion may explain Eastern Alps uplift fully; in Western Alps roughly half; interacting processes best explain elevation change. Erosion-driven isostatic uplift explains up to ~50% of modern geodetic rock uplift (text, Valla, Sternai & Fox 2021 Elements summary, UNVERIFIED primary).
- Sediment storage in valleys reduces the isostatic response (noted in text).

### Wolf, Huismans, Braun, Yuan 2022, Nature 606, 516-521, DOI 10.1038/s41586-022-04700-6 (abstract/intro read)
Source: https://gfzpublic.gfz-potsdam.de/pubman/item/item_5011946_3/component/file_5012394/5011946.pdf
- Coupled FANTOM (thermo-mechanical) + FastScape (landscape). Non-dimensional Beaumont number Bm: Type 1 non-steady, strength controlled (Bm > 0.5); Type 2 flux steady state, strength controlled (Bm ~0.4-0.5); Type 3 flux steady state, erosion controlled (Bm < 0.4). Himalaya-Tibet and Central Andes: Type 1; Taiwan: Type 2; Southern Alps NZ: Type 3.
- Orogenic decay has two phases with different isostatic rebound characteristics and timescales (abstract). Full quantities not extracted yet.
- NOTE: this is the Nature paper, not the EPSL "Wolf 2022" the brief named. No EPSL 2022 Wolf paper confirmed.

### Gilchrist & Summerfield 1990, Nature 346, 739-742, DOI 10.1038/346739a0 (abstract only; PDF blocked)
- Differential denudation between coastal flank and interior -> flexural upwarps ~600 m, southern Africa west margin (search-level summary: https://www.nature.com/articles/346739a0). Nature PDF returned JavaScript, not a PDF; no full text. Equations UNVERIFIED.

### Stephenson & Lambeck 1985 (not confirmed in Nature)
- Search metadata: Geophys. J. R. astr. Soc. 82, 31-56 (1985), viscoelastic plate, erosion rate proportional to elevation, SE Australia application (search summary: https://www.nature.com/articles/318527a0 and related citations). The "Nature" venue in the brief is not confirmed. Full text not fetched.

### Braun & Yamato 2010: NOT FOUND in search. Not confirmed; do not cite until a DOI is found.
