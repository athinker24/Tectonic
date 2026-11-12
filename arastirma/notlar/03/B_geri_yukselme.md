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

### Montgomery 1994 (JGR 99(B7), 13913-13921, DOI 10.1029/94JB00122): primary NOT read
- Two sources disagree and both are secondary:
  - Roe, Montgomery & Hallet 2003, JGR 108(B6) 2315: "Montgomery [1994] showed that the erosional deepening of valleys ... could account for at most a roughly 25% increase in the height of mountain peaks." Source: https://earthweb.ess.washington.edu/roe/Web/GerardWeb/Publications_files/RoeEtal_Relief_JGR03.pdf (full text read, intro p.1-2)
  - Search summary (EarthRef abstract, unverified): Sierra Nevada and Tibet 5-10%; Himalaya 20-30%. Source: https://earthref.org/ERR/40136 (metadata only)
- Brief said "American Journal of Science": the paper is JGR (not AJS).
- Use as a range: 5-25% of peak elevation from incision-driven compensation, depending on region and rigidity. Flagged as disagreement until the abstract is read.

### Montgomery & Brandon 2002 (EPSL 201, 481-489): abstract read in full
Source: https://repository.geologyscience.ru/bitstream/handle/123456789/28097/Mont_02.pdf (abstract and intro text)
- Olympic Mountains 10 m DEM transect: non-linear relation between long-term erosion rate and mean slope, similar to landsliding hillslope model. Mean slope vs mean local relief also related.
- Global 1 km analysis: erosion rate vs mean local relief gives different trends for low-erosion areas and tectonically active ranges; composite well described by non-linear models.
- Conclusion (abstract): erosion rates adjust to tectonic rock uplift mainly through landslide frequency rather than hillslope steepness; changes in local relief play a minor role in landscape-scale erosion. Break point near S ~ 25 degrees is in a garbled extraction: UNVERIFIED.
- Fitted equations not extracted. Use the qualitative non-linear form only.

### Roe et al. 2003 JGR (orographic precipitation and relief): intro read
- Gives the Montgomery 1994 range quoted above. Steady state: erosion rate must balance uplift rate everywhere (their eq. 1 context, p.1206 region). Stream-power exponent form not confirmed in the text read.

### Foreland basin fill numbers
- Lin and Watts 2002, JGR 107(B9) 2185, DOI 10.1029/2001JB000669: West Taiwan basin, elastic plate Te = 13 km; basin "infilled by a substantial thickness (up to 10 km)". Source: https://basin.earth.ncu.edu.tw/publications/papers/Lin&Watts_2002.pdf (full text read, abstract and intro).
- Flemings and Jordan 1990, Geology 18, 430-434, DOI 10.1130/0091-7613(1990)018<0430:SMOF: stratigraphic foreland model, lithosphere elastic thickness 25 km assumed (retro-arc model cited); model denudation vs relief relation is plotted in their Fig. 2 (proportionality not confirmed in text read); episodic thrusting with forebulge migration. Source: https://people.uncw.edu/lamaskint/GLY%20445-545%20FALL%202013/Flemings%20and%20Jordan%201990%20GEOLOGY%20Foreland%20Basin%20Modeling.pdf (text read, p.1-2). Viscoelastic relaxation is noted as controversial on basin timescales.
- Po Plain: Bruno et al. 2021 (Sedimentology; accepted version at https://cris.unibo.it/bitstream/11585/622978/2/sed.12374.pdf) says the Po Basin fill is a shallowing-upward Plio-Quaternary succession "up to 8 km thick (Ricci Lucchi, 1986)". Full text read; this is a Holocene palaeogeography paper, so the 8 km is a secondary citation. Stefani et al. 2019 (Tectonophysics 750, 262-279; https://ricerca.ogs.it/retrieve/bc4ed0ba-b3c4-4698-8874-6dafb4288513/1-s2.0-S0040195118303469-main.pdf) is a gravity/surface-wave study that maps Plio-Quaternary sediment thickness classes <1, 1-2, >2 km (figure legend). It does NOT give the 1.5 m/ka subsidence figure attributed to it by search: that claim is REJECTED as not found in that paper.
- Po infill rates (volume 10.6 km3/Ma Pliocene, 25.3 km3/Ma Pleistocene from Barrera et al. 2026 EGU abstract, preliminary): search-level only, UNVERIFIED.
- Mesopotamian / Zagros (search summaries only; Caltech PDF landing page was HTML, not fetched): flexural foreland depth 1-6 km along strike; equivalent Te of Arabian lithosphere ~50 km (2017 study); Te rising from ~20 km to ~55 km over last 20 Myr (NW Zagros); underfilled eastern sector, filled and deep western sector. Source landing: https://authors.library.caltech.edu/records/1bgnp-74m19 . All UNVERIFIED.
- Ganges/Bengal: Te 15-25 km for Garo-Rajmahal Gap (2019 Basin Research, search summary), subsidence 2-4 mm/yr in Bengal basin (citing Goodbred et al. 2003), Tista megafan accumulation <0.8 mm/yr. All search-level; primary text not read. The ~2006 India Plate study gives Lyon-Caen and Molnar Te ~90 km for the Indian plate (search summary; core.ac.uk PDF returned HTML, not read).
- Sinclair & Allen 1992, Basin Research 4, 215-232: fill-state ratio F = (thrust front advance rate) / (basin deflection rate at thrust front); F > 1 trends to overfilled, F < 1 to underfilled; underfilled deep-water then filled shallow-marine or overfilled continental phase (search summary of the paper's framework; primary not read). Source: https://www.earthdoc.org/content/journals/bre/4/3-4 (metadata).
- Catuneanu 2004 review (underfilled, filled, overfilled stages; base-level and supply control): https://www.eas.ualberta.ca/catuneanu/files/Papers_PDF%20files/2004_Catuneanu_Forelands_JAES.pdf (search summary; PDF not fetched yet).

### Burbank 1992 (Nature 357, 680-683): primary NOT read
- Nature PDF returned JavaScript. Search summary: Burbank inferred Himalayan uplift from sediment accumulation pattern in the Ganges basin; commentary favours erosional unloading as the better candidate (News and Views). Flexure details UNVERIFIED.

### Stephenson & Lambeck 1985: venue correction, primary NOT read (GJRAS 82, 31-56).

### Software components (documentation-level only)
- Landlab Flexure component (2D, uniform flexural rigidity, input lithosphere__overlying_pressure_increment in Pa, output lithosphere_surface__elevation_increment; default Airy; also Flexure1D and gFlex wrapper). Source: https://landlab.readthedocs.io/en/latest/reference/components/index.html (search summary; API docs at https://landlab.readthedocs.io/en/latest/generated/api/landlab.components.flexure.flexure.html not read). Erosion components: FastscapeEroder; ErosionDeposition (Davy and Lague style).
- goSPL (Salles et al. 2020, JOSS 5(54) 2804, DOI 10.21105/joss.02804): optional flexural isostasy driven by surface load changes; stream power erosion; priority-flood depression filling; marine diffusion. Source: https://gospl.readthedocs.io/en/stable/ (fetched via oku; the tech guide has only a one-line flexure mention, no equations). Source for feature list: https://gospl.readthedocs.io/en/stable/tech_guide/index.html
- Braun & Yamato 2010 and Gilchrist & Summerfield equations: not verified (see above).

### Catuneanu 2004, J. African Earth Sci. (foreland systems review), 16 pp (full text read)
Source: https://www.eas.ualberta.ca/catuneanu/files/Papers_PDF%20files/2004_Catuneanu_Forelands_JAES.pdf
- Underfilled, filled and overfilled stages defined by the interplay of base level change and sediment supply, which controls how much available accommodation is consumed (abstract). Underfilled = deep marine; filled = shallow marine; overfilled = fluvial (abstract).
- Early phase: flexural tectonics, underfilled foredeep, forebulge above base level. Middle phase: system-wide dynamic subsidence, forebulge drops below base level, foredeep goes from late underfilled to filled. Late phase: flexural tectonics, overfilled stage, fluvial sedimentation (abstract).
- Base level of deposition in a foreland system is the sea level of the interior seaway; it may be anywhere relative to the system (Sec. on base level, p.~10).
- Flexural and dynamic loading give contrasting base level changes across the flexural hinge line (text).

## Items NOT completed (to keep honest)
- Champagnac et al. 2007 Geology: only search metadata read. The Geology paper's own erosion-unloading numbers are not verified. The Champagnac 2009 Tectonophysics full text was read instead.
- Montgomery 1994 primary (JGR): not read. Range 5-25% comes from secondary sources that disagree.
- Burbank 1992 Nature, Gilchrist & Summerfield 1990 Nature: blocked (JavaScript). Not read.
- Stephenson & Lambeck 1985 (GJRAS): not read.
- Braun & Yamato 2010: not found in search.
- Wolf et al. EPSL 2022: not found; the Nature 2022 paper was read at intro/abstract level.
- Watts 2001 book: relaxation timescale range (0.1 to several Myr, or 1 to 100 Myr) is search-level and garbled; not verified. Viscoelastic tau = 2 eta / E is from Sternai 2019 text (read).
- Zagros/Mesopotamia, Ganges, Indus, Po infill numbers: search summaries and secondary citations; no primary full text beyond Lin & Watts 2002, Flemings & Jordan 1990 and Bruno 2021 (only the 8 km citation).
- Taiwan and Himalaya rebound observations: Whipple 2009 and Lin & Watts 2002 only; no GPS or leveling rate data read.
- Alps GPS/leveling rates: Sternai 2019 text read (uplift 1-2.5 mm/a), but not the GPS velocity papers themselves.
- Landlab and goSPL: docs-level only; no equations read.

## URLs read (full text or primary abstract)
- https://www.tectonics.caltech.edu/meetings/journal_club/session2/Molnar_and_England1990Nature.pdf (Molnar & England 1990 full text)
- https://gfzpublic.gfz-potsdam.de/pubman/item/item_238796_1/component/file_238795/13194.pdf (Champagnac et al. 2009 full text)
- https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2009_Whipple.pdf (Whipple 2009 full text)
- https://earthweb.ess.washington.edu/roe/Web/GerardWeb/Publications_files/RoeEtal_Relief_JGR03.pdf (Roe et al. 2003, intro)
- https://repository.geologyscience.ru/bitstream/handle/123456789/28097/Mont_02.pdf (Montgomery & Brandon 2002 abstract and intro)
- https://www.isterre.fr/IMG/pdf/Braun-and-Robert-ESPL2005.pdf (Braun & Robert 2005 full text, derivations)
- https://boa.unimib.it/bitstream/10281/229017/2/Sternai%20et%20al.%2c%202019.pdf (Sternai et al. 2019 full text)
- https://gfzpublic.gfz-potsdam.de/pubman/item/item_5011946_3/component/file_5012394/5011946.pdf (Wolf et al. 2022 Nature, intro)
- https://people.uncw.edu/lamaskint/GLY%20445-545%20FALL%202013/Flemings%20and%20Jordan%201990%20GEOLOGY%20Foreland%20Basin%20Modeling.pdf (Flemings & Jordan 1990)
- https://basin.earth.ncu.edu.tw/publications/papers/Lin&Watts_2002.pdf (Lin & Watts 2002 abstract and intro)
- https://cris.unibo.it/bitstream/11585/622978/2/sed.12374.pdf (Bruno et al. 2021, Po fill citation only)
- https://ricerca.ogs.it/retrieve/bc4ed0ba-b3c4-4698-8874-6dafb4288513/1-s2.0-S0040195118303469-main.pdf (Stefani et al. 2019, figure legend and metadata only)
- https://www.eas.ualberta.ca/catuneanu/files/Papers_PDF%20files/2004_Catuneanu_Forelands_JAES.pdf (Catuneanu 2004 full text)
- https://gospl.readthedocs.io/en/stable/ and https://gospl.readthedocs.io/en/stable/tech_guide/index.html (docs)
- https://landlab.readthedocs.io/en/latest/reference/components/index.html (search summary plus docs listing)
- Search-only metadata/abstract pages (read as search snippets, not as documents): https://www.nature.com/articles/346029a0 ; https://www.nature.com/articles/318527a0 ; https://data.zhenzhi.com/details/1/908083990 ; https://www.doi.org/10.1038/NGEO413 ; https://csdms.colorado.edu/wiki/Reference:Reference-000402 ; https://earthref.org/ERR/40136 ; https://www.earthdoc.org/content/journals/bre/4/3-4 ; https://authors.library.caltech.edu/records/1bgnp-74m19 ; https://meetingorganizer.copernicus.org/EGU22/EGU22-8815.html

## Failed fetches (not worked around)
- https://core.ac.uk/download/47307459.pdf (HTML landing, not PDF) and https://core.ac.uk/download/357532256.pdf (HTML). Montgomery 1994 and Champagnac 2007 PDFs not obtained.
- https://www.nature.com/articles/357680a0.pdf (Burbank 1992): JavaScript, not PDF (paywalled or script-only).
- https://www.nature.com/articles/346739a0.pdf (Gilchrist & Summerfield 1990): JavaScript, not PDF.
- https://core.ac.uk/download/11857861.pdf (Indian plate Te study): HTML, not PDF.
- https://authors.library.caltech.edu/records/1bgnp-74m19 (Zagros 2017): HTML landing; PDF not reached.
- https://repository.geologyscience.ru/handle/123456789/28097 : landing only.
- Braun & Yamato 2010 and Stephenson & Lambeck 1985 primaries: not found or not fetched.
- Wolf 2022 EPSL: no such paper found in search.

## Key takeaways for the tool
1. Local Airy compensation for eroded rock thickness dT (Molnar & England 1990, Champagnac 2009, Braun & Robert 2005): surface lowering = dT (1 - rho_c/rho_m); rock rise = dT rho_c/rho_m. With rho_c = 2.8, rho_m = 3.25 this gives rock rise ~0.86 dT and surface lowering ~0.14 dT (Champagnac 2009 rounds to 5/6). Molnar & England with 2.7/3.3 give 1/6 = 0.17. Braun & Robert with 2600/3200 give topography reduction factor 0.19 (erosion needed 5.3 km per km of relief). These differ only by density choice. The tool should expose rho_c, rho_m as parameters.
2. Flexural rigidity damps the response and widens it. Champagnac 2009 model: Te 10 km, E = 1e11 Pa, Poisson 0.25, 100 km boundary extension, instantaneous elastic response, reproduces 75% of geodetic rock uplift. Use flexure (not pure Airy) for continent-scale loads, and treat Airy as the Te -> 0 limit.
3. Fraction of erosion compensated (Airy limit): per km of rock removed, surface lowers by ~0.14-0.17 km (Champagnac 2009 densities; Molnar and England 1990) and rock rises by ~0.83-0.86 km. So rebound offsets ~83-86% of the removed thickness as rock uplift, and only ~14-17% shows as mean-surface lowering. Whipple 2009 gives c ~ 1/5 for Airy (different definition, UNVERIFIED equivalence). Steady state: erosion equals rock uplift (Whipple 2009, U = F_A/W).
4. Peak uplift from valley incision: range roughly 5-25% of peak height (Montgomery 1994 via Roe et al. 2003: at most ~25%; search summaries give 5-10% for Sierra and Tibet and 20-30% for Himalaya: disagreement, primary not read). Depends on Te, range width and boundary conditions. Use 5-25% as a bounded design range and flag.
5. Rock uplift vs surface uplift vs exhumation (England and Molnar 1990; Molnar and England 1990): exhumation = surface uplift + rock uplift relation: rock uplift relative to sea level = surface uplift + exhumation. Use separate fields in the tool and never equate exhumation with surface uplift.
6. Time response: viscoelastic relaxation tau = 2 eta / E (Sternai 2019 text). Lag magnitude for the Alps or other orogens is not verified here; the 10^4-10^5 yr figure is UNVERIFIED. Champagnac 2009 is an instantaneous elastic model with no time dependence. Watts' relaxation range (0.1 to several Myr) is search-level and garbled. For a tens-of-Myr simulation, instantaneous elastic response is a first-pass approximation; relaxation lag should be added as a separate option.
7. Erosion-relief scaling (Montgomery & Brandon 2002): erosion vs slope is non-linear in tectonically active ranges, and relief plays a minor role in landscape-scale erosion. Do not use a linear E = k S law without a threshold or non-linear term. The fitted exponent was not extracted; treat the non-linear form as a model choice.
8. Foreland fill state: classify basins as underfilled (deep marine), filled (shallow marine, base level reached), overfilled (fluvial, surface above base level) by comparing sediment supply with accommodation (Catuneanu 2004; Sinclair & Allen 1992 F ratio; search summary). A fixed coastline means base level = sea level, so an overfilled foredeep must be filled to base level before its surface can sit at sea level. Overfilled foredeeps can have fluvial surfaces above sea level.
9. Flexural foreland Te: Te 10-30 km typical in orogens (Braun & Robert: Dabie Shan 10-30 km; Flemings & Jordan 1990 used 25 km; Lin & Watts West Taiwan Te 13 km). Arabian lithosphere Te ~50 km (Zagros, search summary, UNVERIFIED). Stiffer lithosphere means wider, shallower foredeeps (Watts 1992 abstract, search summary) such as the Ganges and Mesopotamia.
10. Sediment infill and subsidence: Po Plio-Quaternary fill up to ~8 km (Bruno et al. 2021 citing Ricci Lucchi 1986). Infill rates (Po 10-25 km3/Ma) and Bengal subsidence 2-4 mm/yr are search-level, not verified.
11. Software: Landlab Flexure (uniform Te, Airy default; input Pa load; output elevation increment) and goSPL (optional flexure driven by surface load changes; stream power erosion) exist. Neither was verified at equation level. A custom 2D flexure solver (Fourier or finite difference) is straightforward to write and verify against Champagnac 2009 numbers.
12. Disagreements to keep open: Molnar & England (1990) 0.17 vs Braun & Robert 0.19 (density choice); Montgomery 1994 peak effect (5-25%); Alps rebound share of rock uplift (10-30% Central and Western in Sternai 2019 text vs ~50% in Champagnac 2009 and Valla et al. 2021); Te values (10 to 90 km depending on method, Lyon-Caen & Molnar 1983 ~90 km for India, search-level).
