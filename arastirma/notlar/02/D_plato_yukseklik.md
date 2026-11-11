# D: How kinematics turns into elevation (research notes, 2026-11-11)

(Work in progress; facts have source URL right after them. UNVERIFIED = not confirmed from a source read.)

## 1. Terrain-generation style uplift rules
- Cordonnier et al. 2018 (TVCG, Sculpting Mountains): crust deformation treated as isochoric, local crust thickness proportional to volume of crust material q in a cell; thickness change rate dq/dt = (q - q0)/dt; uplift u0 = 0 on the stable side of a procedurally defined fault (iso-level of q), and u0 = alpha * dq/dt elsewhere. alpha is a scaling coefficient chosen so average uplift is 5.0e-4 m/yr (0.5 mm/yr), "a geologically consistent value (uplift rate in mountain belts rarely exceed a few mm/yr)". They explicitly neglect isostasy (no crustal root depression) and fault dip. Total simulation time 5e6 yr; stream power erosion with n=1, m=0.5, k 2.5e-7 to 8e-7 /yr. https://www.cs.purdue.edu/homes/bbenes/papers/Cordonnier18TVCG.pdf

## 1b. Cordonnier 2016 and Willett 1999 (read as PDF text)
- Cordonnier et al. 2016 (CGF, "Large Scale Terrain Generation from Tectonic Uplift and Fluvial Erosion"): stream power h_t = u - k A^m s^n with n = 1, m = 0.5 ("the ratio m/n is ... thought to be m/n ~ 0.5 [WT99]"). Max tectonic uplift U = 5.0e-4 m/yr, "the average uplift among earth mountains" (author claim, not a measured value). Erosion constant k = 5.61e-7 /yr chosen "for mountains to culminate at about 2 000 m". Source: https://www.cs.purdue.edu/homes/bbenes/papers/Cordonier16CGF.pdf
- Willett 1999 (JGR 104(B12) 28957-28981, doi 10.1029/1999JB900248): 2-D finite element model, erosion = fluvial incision proportional to stream power. Dimensionless erosion number Ne (eq. 10, 2-D form, as printed in the text extraction: Ne ~ k h / V_p, with k erodibility, h layer thickness, V_p convergence velocity). Ne sets time to steady state and final size and shape. "Convergent tectonics creates topography with elevations over a kilometer but under 10 km" (author's statement about typical Ne range). Source: https://www.tectonics.caltech.edu/meetings/journal_club/session4/Willett1999JGR.pdf (course copy, check provenance; DOI above is the official record).
- Willett 1999 plateau mechanism: a maximum orogen elevation and a plateau in the interior "is a direct consequence of lateral flow in the lower crust preventing any additional increase in crustal thickness and elevation [Bird 1991; Royden 1996]"; plateau formation "depends on the Argand number"; with minimum viscosity Ar < 0.5 gives a strong crust. Same source as above.
- Willett 1999 steady state: at Ne = 2 max elevation 0.25 h; at Ne = 10 peak elevation 0.15 h; at Ne = 10 steady state is reached after nondimensional time < 2 (vs ~12 at Ne = 2). Same source.
- Willett 1999: at low Ne the profiles become "broad, more plateau-like form characteristic of the mechanical process"; high Ne gives concave-up river profiles. Same source.

## 2. Erosion rates (Portenga and Bierman 2011, GSA Today 21(8):4-10)
- Units: the paper reports m/Myr. 1 m/Myr = 0.001 mm/yr (conversion mine).
- Drainage basins: mean 218 m/Myr (~0.22 mm/yr), median 54 m/Myr (~0.054 mm/yr), n = 1149. Outcrops: mean 12 m/Myr (~0.012 mm/yr), median 5.4 m/Myr (~0.005 mm/yr), n = 450. Source: https://www.geosociety.org/gsatoday/archive/21/8/pdf/i1052-5173-21-8-4.pdf
- Seismically active basins 367 +/- 55 m/Myr (~0.37 mm/yr, n = 221); polar-climate basins 537 m/Myr (~0.54 mm/yr). Arid basins 100 m/Myr (~0.10 mm/yr). Same source.
- Note: these are 10Be averages over 1e3 to 1e6 yr, global, and mostly NOT in active orogens; use as a sanity check for a "background" rate only.

## 3. England and Molnar 1990 and Molnar and England 1990 (Nature review "chicken or egg")
- England and Molnar 1990 (Geology 18:1173-1177) separate surface uplift, rock uplift and exhumation: surface uplift = rock uplift - exhumation. Source: https://www.tectonics.caltech.edu/meetings/journal_club/session2/Molnar_and_England1990Nature.pdf (secondary PDF; the Geology article itself: UNVERIFIED full text). Summary read via https://blogs.egu.eu/divisions/ts/2021/09/20/ts-must-read-england-and-molnar-1990-surface-uplift-uplift-of-rocks-and-exhumation-of-rocks/
- Isostatic rebound from erosion: "for each 1 km of material removed from the range, the isostatic response is a lowering of the mean elevation by only ~0.17 km" (Molnar and England 1990 Nature review, Fig. 2; the 0.17 is a range mean-elevation quantity, not the local ratio). Source: same PDF, p. 1 text extraction.
- Molnar and England 1990 argue that the Alps' present mean elevation (~2000 m) makes the 4000 m Pliocene elevation inferred by de Sitter and Triimpy likely to be an isostatic artifact of valley incision (qualitative). Same source.

## 4. Airy isostasy: relations and densities (primary calc checked against MIT lecture)
- Airy balance (equal column mass): rho_c * h = (rho_m - rho_c) * r, so root r = h * rho_c / (rho_m - rho_c). With rho_c = 2800, rho_m = 3300 kg/m3 the root is 5.6 x the topographic height. Source: https://ocw.mit.edu/courses/12-002-physics-and-chemistry-of-the-terrestrial-planets-fall-2008/74fb28dc068682451773d2616e914ff2_MIT12_002f08_lec26.pdf (lecture, slides 4 "High Altitude Regions - Tibet": "dv = dt rho_c/(rho_m - rho_c) = 5000(2800)/500 = 28 km", and "Total Crustal Thickness beneath Tibet 61 km" for a 5 km high plateau on a 33 km normal crust). Pinter exercise confirms the same Airy formulation with compensation depth: https://www.geologyrocks.co.uk/people/pinter/pdf/IsostasyExercise.pdf
- Derived rule (ours, from the above): root = 5.6 x h for those densities; so 1000 m -> 5.6 km root, 2000 m -> 11.2 km, 4500 m -> 25.2 km, 5000 m -> 28 km. If rho_m = 3100 the factor is 2800/300 = 9.3 (MIT/handout example 5 km -> 47 km root). Density contrast is the big uncertainty.
- Sensitivity: ratio factor = rho_c/(rho_m - rho_c). Using rho_m 3300 vs 3100 changes the root by a factor of ~1.7 (computed).
- Typical crust (Royden et al. 2008): Tibet "5 km high over a region of approximately 3 million km2"; crust thickened "to ~80 km" is Argand's 1920s postulate, not a measurement. Source: https://hilst.mit.edu/wp-content/uploads/2017/05/2008_science_321-1054-1058.pdf (Royden, Burchfiel, van der Hilst, Science 321:1054-1058, doi 10.1126/science.1155371). Royden et al. 1997 (Science 276:788): plateau "uplifted by >4 km and its crust thickened to twice normal thickness (~70 km)". Source: https://geoscience-prey.sydney.edu.au/Teaching/Geos-3003/geos3003papers/RoydenScience98.pdf
- Tibet crust, secondary: >=65 km under most of Tibet, <80 km everywhere studied (surface waves; search summary, UNVERIFIED primary); 70 +/- 4 km in Lhasa terrane (2020-ish study cited in search, UNVERIFIED primary). Source for the 70 km claims: https://www.x-mol.com/paper/1308484164113371136 (not fetched; UNVERIFIED).
- Central Andes: Beck et al. (search summary) max 70-74 km under Western Cordillera; Altiplano 60-65 km at 20S; Airy predictions correlate with observed crust in high-elevation regions. Source: https://typeset.io/pdf/crustal-thickness-variations-in-the-central-andes-3utl2dce6o.pdf (not fetched; UNVERIFIED primary).
- Andean plateau crust 60-70 km (Hoke and Garzione 2008 summary of Oncken 2003, Beck et al. 1996). Source: https://www.sas.rochester.edu/ees/SIREAL/PDF_files/Hoke_and_Garzione_2008_EPSL.pdf
- Andes, Molnar and Garzione 2007: crust 70 km in Eastern Cordillera, 59-64 km central Altiplano (Beck and Zandt 2002); "average elevation of 4 km" for the Altiplano; "rise of the Altiplano of 3 +/- 1 km" between ~10 and 6.8 Ma. Source: https://www.sas.rochester.edu/ees/SIREAL/PDF_files/Molnar_and_Garzione_2007_Tectonics.pdf
- Zagros: Paul et al. 2006 receiver functions: crust rises abruptly to a maximum ~70 km beneath the Sanandaj-Sirjan zone; ~45 km near the front. Other values: 46 +/- 2 km (Hatzfeld 2003); 42 +/- 2 km (Fold-Thrust belt re-analysis); ~50 km UDMA (search summaries, not fetched). Source: https://core.ac.uk/download/47308989.pdf (not fetched; UNVERIFIED from snippet).
- Mongolia (Hangai dome): joint Rayleigh/RF inversion Moho 50-53 km, lithosphere 65-70 km; separate RF study 41-59 km with thickest crust under highest topography; 2026 GRL reports near-isostatic equilibrium with inherited crustal thickening as leading uplift factor, asthenosphere secondary. Source: https://www.citedrive.com/en/discovery/the-significance-of-inherited-crustal-thickening-in-surface-uplift-of-hangai-dome-in-central-mongolia/ (search snippet, UNVERIFIED primary). One abstract gives "elevations of 4 km" for the Hangay dome; this conflicts with the 1500 m guess in the brief. Source: https://agu.confex.com/agu/fm14/webprogram/Paper7993.html (search snippet).
- Alps: Spada et al. 2012 root ~60 km (cited in Braszus et al. 2025 search summary, UNVERIFIED primary). Moho depths 32 km (Cel09) and 48 km (ALP75) quoted in a secondary paper. No verified Swiss-Alps 50 km figure. Sources: https://se.copernicus.org/preprints/se-2020-179/se-2020-179-manuscript-version3.pdf (not read in full; UNVERIFIED).
- Molnar and England 1990 (Nature review): for 1 km of material removed from a range, the mean elevation drops only ~0.17 km by isostatic rebound (see section 3).

## 5. Lower crustal flow and plateau strength
- Clark and Royden 2000 (Geology 28:703-706, "Topographic ooze"): for a 15 km thick channel, lower-crust viscosity ~1e18 Pa s beneath low-gradient eastern margins, ~1e21 Pa s beneath steep margins, upper bound 1e16 Pa s beneath the plateau interior. Source: https://basin.earth.ncu.edu.tw/Course/SeminarII/abstract2014_1/2014.10.02_Sun,%20Yuan-Cheng/Topographic%20ooze%20building%20the%20eastern%20margin%20fo%20Tibet%20by%20low%20crustal%20flow.pdf (course copy).
- Royden et al. 2008: eastern Tibet crustal thickening "result[s] from rapid eastward flow of the deep crust" in crustal channels; onset ~15-20 Ma after slowdown of Pacific trench rollback. Source: https://hilst.mit.edu/wp-content/uploads/2017/05/2008_science_321-1054-1058.pdf
- Willett 1999 (see 1b): lateral lower-crust flow limits thickness and elevation; plateau depends on Argand number.
- Thermal condition (search summary, UNVERIFIED primary): Rey et al. argue a 5000 m Tibet needs a pre-thickening Moho ~500-600 C. Source: search snippet only.
- Upper crust differential stress >=150 MPa to maintain plateau relief ~10 Ma (EGU 2018 abstract, search snippet only). Source: https://meetingorganizer.copernicus.org/EGU2018/EGU2018-10124.pdf?EGUsphere (UNVERIFIED).
- Model result (search snippet): without lithosphere removal, weak rheology gives max topography < 4000 m. Source: https://www.nature.com/articles/s41467-018-07312-9 (snippet only, UNVERIFIED primary).

## 6. Steady state orogens and erosion limits
- Willett 1999 (see 1b): Ne sets steady state time and final size; Ne 2 gives peak ~0.25 h, Ne 10 gives ~0.15 h (h = model layer thickness, nondimensional). Typical natural Ne: "elevations over a kilometer but under 10 km" (Willett 1999 author statement). Source: https://www.tectonics.caltech.edu/meetings/journal_club/session4/Willett1999JGR.pdf
- Roe, Stolar and Willett 2006 (GSA Memoir, critical wedge response): steady state geometry from two relations: R/L = tan(alpha_c) (eq. 1, total relief R over half-width L equals critical taper), and U = F/L (eq. 2, uniform rock uplift U = accretionary flux F divided by width L). Consequence: uplift scales inversely with orogen width. Width is more sensitive to accretionary flux than to precipitation rate. Source: https://earthweb.ess.washington.edu/roe/Web/GerardWeb/Publications_files/RoeEtal_WedgeTheory_GSA06.pdf
- Critical wedge (Dahlen et al. 1984; Davis et al. 1983; Dahlen review): fixed taper set by decollement dip and wedge strength; stronger wedge gives lower critical taper; taper drops where wedge thicker than ~15 km (brittle-plastic transition). Source: search summary only (Dahlen review PDF failed, see failed fetches). UNVERIFIED primary.
- Taiwan steady state: Suppe 1981 inferred steady size and shape over Myr. Erosion 3-6 mm/yr across active mountains (Dadson et al. 2003 Nature 426:648-651, doi 10.1038/nature02150; search abstract, full text not read). Source: https://www.nature.com/articles/nature02150 (not fetched; abstract via https://ideas.repec.org/a/nat/nature/v426y2003i6967d10.1038_nature02150.html). Fission-track (Willett et al. 2003, Geology 31:945-948): best erosion 4-6 mm/yr in northern Taiwan. Derrieux et al. 2014 summary (search snippet): 2-8 mm/yr in Central Range, ~5 mm/yr whole belt. Source: https://scholar.lib.ntnu.edu.tw/en/publications/erosion-rates-and-orogenic-wedge-kinematics-in-taiwan-inferred-fr-2/ (UNVERIFIED primary).
- Taiwan convergence: Philippine Sea-Eurasia ~80-83 mm/yr, oblique ~20 deg, Taiwan share ~3 convergence : 1 transcurrent (80 vs 27 mm/yr, search summary). Source: https://www.tectonics.caltech.edu/publications/pdf/Hsu_Tectonophysics_2009.pdf (snippet; UNVERIFIED primary).
- Taiwan peak elevation (3.9 km) and orogen width (~100 km) from my memory are NOT confirmed by any source read: UNVERIFIED.
- Montgomery and Brandon 2002 (EPSL 201:481-489): global erosion-relief data; erosion rates in active ranges adjust to rock uplift mainly via landslide frequency. Source: https://repository.geologyscience.ru/bitstream/handle/123456789/28097/Mont_02.pdf?sequence=1. Ganges and Brahmaputra fit: E = 0.2 Rz (mm/yr, Rz in km, R^2 = 0.90), read from the text (Mont_02 p.1). Combined data Rz >= 100 m: power law E ~ 1.8 power of relief (prefactor garbled in extraction, UNVERIFIED). Note the Ganges fit: 1 km mean relief -> 0.2 mm/yr; 3 km relief -> 0.6 mm/yr.
- Erosion rate (10Be global): see section 2 (background rates are much lower than active-orogen rates).
- Central Alps: 10Be denudation 0.9 +/- 0.3 mm/yr (crystalline Central Alps) and 0.27 +/- 0.14 mm/yr for the Alpine foreland; geodetic rock uplift ~1 mm/yr in central Alps (leveling). Source: search summary of Wittmann et al. (UNVERIFIED primary): https://gfzpublic.gfz-potsdam.de/pubman/item/item_238796_1/component/file_238795/13194.pdf
- Himalaya/Nepal: exhumation ~1.5 to 2.6 km/Myr (Blythe et al. 2007 short term, Marsyandi); 1.5 to 12 km/Myr in other profiles (1.2 to 0.3 Ma). These are short-term rates (km/Myr = mm/yr numerically). Source: search summary only, Blythe et al. 2007 not read (UNVERIFIED).
- Himalaya basin erosion: Ganga-Brahmaputra exports 1 to 2 Gt/yr (search summary, not verified primary). Source: https://goldschmidtabstracts.info/2006/1084.pdf (UNVERIFIED). Galy and France-Lanord 2001 (Geology 29:23-26) not read.

## 7. Shortening and convergence budgets
- India-Eurasia convergence ~40 mm/yr (Banerjee 2008 GRL / Bangalore GPS, search summary); Himalaya takes ~18-21 mm/yr (Nepal GPS and MFT terrace shortening 21 +/- 1.5 mm/yr). Source: https://repository.ias.ac.in/21806/1/346.pdf and https://www.ncedc.org/ftp/outgoing/burgmann/REPRINTS/Banerjee_GRL2008.pdf (search summaries; UNVERIFIED primary).
- Long-term: at least 1400 km of N-S shortening across the Himalayan-Tibetan orogen since ~70 Ma (Yin and Harrison 2000, Annu. Rev. Earth Planet. Sci. 28:211-280, doi 10.1146/annurev.earth.28.1.211; search abstract, UNVERIFIED primary). Average 1400 km / 70 Myr = 20 mm/yr (derived, consistent with the Himalayan rates above).
- Central Andes: shortening rates 8-10 mm/yr pre-Miocene, 5-7 mm/yr post-Miocene (Hoke and Garzione 2008 summary of McQuarrie et al.). Source: https://www.sas.rochester.edu/ees/SIREAL/PDF_files/Hoke_and_Garzione_2008_EPSL.pdf (read in text; figures from their text, lines ~132).
- Eastern Tibet deep crust flow (Royden et al. 2008): flow started ~15-20 Ma after trench-rollback slowdown; "rapid eastward flow of the deep crust" in crustal channels. Source: https://hilst.mit.edu/wp-content/uploads/2017/05/2008_science_321-1054-1058.pdf
- Longmen Shan shortening rate 0.5-6.5 mm/yr? Royden 1997 GPS: "0 to 5 mm/yr" unreadable in extraction, UNVERIFIED. Source: https://geoscience-prey.sydney.edu.au/Teaching/Geos-3003/geos3003papers/RoydenScience98.pdf

## 8. Paleoaltimetry and surface uplift histories
- Tibet, central: Rowley and Currie 2006 (Nature 439:677-681, doi 10.1038/nature04506): Lunpola basin oxygen isotopes; plateau above ~4 km for >=35 Myr; estimates 4850, 4260, 4050 m (quoted by Molnar et al. 2006 comment). Source: https://ideas.repec.org/a/nat/nature/v439y2006i7077d10.1038_nature04506.html (abstract/record; full PDF https://www.nature.com/articles/nature05368.pdf not read). Molnar, Houseman and England 2006 reply: sample too small, mantle-thickening models not excluded. Source: https://www.nature.com/articles/nature05368.pdf (not read in full; UNVERIFIED).
- Tibet debate summary: Deng and Ding 2015 (NSR 2:417): camp A late Miocene (plateau reached modern height late), camp B early (Paleogene or middle Miocene, stable isotopes). Source: https://academic.oup.com/nsr/article/2/4/417/2936891 (search snippet; UNVERIFIED primary). Spicer et al. 2021 NSR: argue a single "uplift" is a misconception, true plateau late Neogene. Source: search summary only. Farnsworth et al. 2023 EPSL: isotope palaeoaltimetry works for mid-Eocene Tibet except low valleys. Source: search summary only.
- Eocene Tibet < 3000 m (Science Advances 2019 model-data, search summary). Source: search snippet only.
- Andes, Altiplano: Molnar and Garzione 2007 (Tectonics): rise of 3 +/- 1 km between ~10 and 6.8 Ma; rapid uplift of several km in 3 +/- 1 Myr; average Altiplano elevation 4 km. Source: https://www.sas.rochester.edu/ees/SIREAL/PDF_files/Molnar_and_Garzione_2007_Tectonics.pdf
  Derived: 3 km / 3.2 Myr = ~0.9 mm/yr average surface uplift.
- Andes, Hoke and Garzione 2008 (EPSL): "loss of a dense lithospheric root, and possibly changes in the tectonics of the central Andes" explains surface uplift 10-6 Ma (quote from the abstract, read in text). Source: https://www.sas.rochester.edu/ees/SIREAL/PDF_files/Hoke_and_Garzione_2008_EPSL.pdf
- Andes disputes: Sempere et al. comment: leaf-morphology paleoaltimetry underestimates high altitudes (search summary). Source: search snippet only.
- Iranian plateau: mean elevation ~1.8 km (search summary, several sources); uplift onset after ~17 Ma (Qom Formation); central basin 900-1000 m uplift in mid or late Miocene; Zagros shortening after early Miocene; accelerated Zagros shortening after ~12.4 Ma (Bakhtiari). Source: search summaries only (https://www.cambridge.org/core/product/19E9DEA9D3C59A77EFB14BFA4B36A1E2/core-reader; UNVERIFIED primary).
- Anatolia: central Anatolian plateau uplift >1 km since ~8 Ma with little shortening; interior 1 km uplifted c. 8-5 Ma (2021 Tectonophysics review). Delamination/dripping drives ~1-2 km; Govers and Bartol: delamination explains half of East Anatolian elevation. Gogus and Pysklywec 2008 (Geology) numerical model gives ~2 km uplift from delamination. Sources: https://www.geologist.nl/wp-content/uploads/2021/10/2021_McPhee_Tectonophysics.pdf and https://mantleplumes.awh.durham.ac.uk/WebDocuments/Gogus2008_Geology.pdf (Durham PDF failed to download). All search summaries; UNVERIFIED primary.
- Mongolia (Hangai): timing not established in sources read; no Cenozoic uplift history found. Gap.
- Anatolia and Mongolia both: dense lithospheric dripping/asthenosphere upwelling invoked; sources disagree.

## 9. Mechanisms, quantified where the sources give numbers
- Airy isostasy (primary, see section 4): root = h * rho_c/(rho_m - rho_c). Elevation per unit root thickening = (rho_m - rho_c)/rho_c = 0.18 for rho_c 2800 and rho_m 3300 (derived).
- Lower crustal flow: Clark and Royden 2000 viscosities (section 5). Royden et al. 2008 deep crust channel flow in eastern Tibet.
- Delamination/lithosphere removal: Molnar, England and Martinod 1993 (Rev. Geophys. 31:357-396): removal of lower lithosphere could raise mean elevation by 1000 m or more in a few Myr (search abstract summary; paper not read; UNVERIFIED primary). Source: search result listing https://earthref.org/ERR/62502 (not read).
- Delamination with Eclogite (Ye et al. 2022 Solid Earth 13:745): eclogite favours delamination (garnet, Fe content, eclogitization). Source: https://se.copernicus.org/articles/13/745/2022/se-13-745-2022.pdf (downloaded, not yet grepped; see TODO).
- Dynamic topography: Flament, Gurnis and Muller 2013 (Lithosphere 5:189-210, doi 10.1130/L245.1): amplitude under ~2 km; long-wavelength (>5000 km) agreement between models and residual topography. Source: https://www.earthbyte.org/Resources/Pdf/Flament_etal_2013_ObservationsAndModelsOfDynTopo.pdf (PDF link returned HTML, so only search abstract read: UNVERIFIED primary).
- Magmatic addition (Andes, Gangdese): Gangdese >4000 m at 55-45 Ma via thickening and slab breakoff (EGU/2017 search summary). Source: search snippet only; UNVERIFIED.
- Tibet residual topography: 70 km study reports residual topography about -2.4 +/- 1.5 km (search summary of a 2024-2025 study; UNVERIFIED primary).

## 10. Derived calculations for the tool (my arithmetic; check inputs before use)
- Pure area-balanced thickening: thickness scales as t = t0/(1 - e), e = horizontal shortening fraction. Doubling a 35 km crust needs e = 0.5 (50% shortening). Over a 1000 km wide belt that is ~500 km shortening.
- Thickening rate from convergence (uniform strain): dt/dt ~ t0 * v/W. Example: t0 = 35 km, W = 500 km, v = 20 mm/yr: dt/dt ~ 1.4 mm/yr thickening.
- Airy surface uplift rate = (rho_m - rho_c)/rho_c * dt/dt = 0.18 * 1.4 = ~0.25 mm/yr. This is the "alpha" for a physically-based rule (crust thickening rate to surface uplift rate).
- Average surface uplift needed: 4.5 km in 20 Myr = 0.23 mm/yr; 1.5 km in 30 Myr = 0.05 mm/yr; 5 km in 10 Myr = 0.5 mm/yr. Cordonnier 2016 uses U = 0.5 mm/yr (max uplift); without erosion, 2 km takes 4 Myr at that rate, so with erosion this is only an upper bound on time (derived).
- Molnar and Garzione Altiplano: 3 km in ~3.2 Myr = ~0.9 mm/yr.
- Mean elevation loss from erosion (Molnar and England 1990: 0.17 km per km for the range mean). Compare 1 - rho_c/rho_m = 0.15 (derived with rho 2800/3300). Local rebound of an eroded column in a broad Airy setting: rho_c/rho_m ~ 0.85 (derived, standard; UNVERIFIED primary).
- Roe et al. 2006 eq. 2 (U = F/L): F is an accretionary flux per unit along-strike length (units m^2/yr, so F/L gives m/yr). Example (derived): F = 0.02 m/yr x 35 km thick layer = 7e-4 km^2/yr; with L = 100 km, U = 7e-6 km/yr = 7 mm/yr. A narrower belt uplifts faster for the same flux. Units per Roe 2006 to be checked in the paper.

## TODO / open items (not yet done)
- Ye et al. 2022 (Solid Earth 13:745-759) read by grep: mineral-physics paper (eclogite density evolution during delamination in Tibet). It gives no uplift rates or heights; use only as qualitative support for eclogite-driven delamination.
- Gogus 2008 and Dahlen 1990 PDFs failed (TLS certificate), Flament 2013 PDF returned HTML.
- Cortial 2019 full text not found (the Eurographics bitstream was a 2026 paper). Its uplift rule remains UNVERIFIED.
- Procedural Riverscapes (Peytavie 2019) and Perche 2023 (Authoring Terrains with Spatialised Style) read by grep: not about uplift; irrelevant to the uplift rule.
- Rey 2001 Tectonophysics and Rey et al. Tibet heights: not read.


## 11. Key takeaways for the tool
1. Airy root rule: root r = h * rho_c/(rho_m - rho_c) = 5.6 h for rho_c 2800, rho_m 3300 (MIT lecture, Pinter exercise). Elevation per unit root = 0.18. Tibet-like 4.5 to 5 km implies a ~25 to 28 km root, i.e. total crust about 60 to 65 km on a 35 km base, matching observed 60 to 70 km (Hoke and Garzione 2008; Royden et al. 2008 "~70 km" for Tibet). Mongolia-like 1 to 2 km implies a 5.6 to 11 km root, i.e. ~40 to 46 km crust, roughly matching the Hangai 41 to 59 km range (sources in section 4).
2. Kinematic-to-uplift rule: u = alpha * (crustal thickening rate), alpha = (rho_m - rho_c)/rho_c ~ 0.18 if fully Airy. Cordonnier et al. 2018 use a tuned alpha with mean uplift 0.5 mm/yr and explicitly neglect isostasy, so their alpha is a style choice, not physics. Cordonnier 2016 max U = 0.5 mm/yr, k = 5.61e-7 /yr gives ~2 km culmination.
3. Time budget (derived): Tibet-like 4.5 km in 10 to 20 Myr needs 0.2 to 0.5 mm/yr average surface uplift; Mongolia-like 1.5 km in 30 Myr needs ~0.05 mm/yr; the Altiplano rise of 3 +/- 1 km in ~3 Myr (Molnar and Garzione 2007) is ~1 mm/yr and is a fast end-member. A 0.5 mm/yr global uplift cap (Cordonnier) reaches 5 km in 10 Myr only if no erosion is applied.
4. Thickening from convergence (derived): with uniform strain, dt/dt ~ t0 * v / W. A 35 km crust in a 500 km wide belt with 20 mm/yr convergence thickens ~1.4 mm/yr. Doubling the crust requires ~50% shortening. Himalaya takes ~18 to 21 of ~40 mm/yr India-Eurasia convergence (search summaries of GPS and geologic estimates); >= 1400 km N-S shortening since ~70 Ma implies ~20 mm/yr average (Yin and Harrison 2000 abstract).
5. Steady state (Roe et al. 2006): R/L = tan(alpha_c) and U = F/L. Uplift is inversely proportional to orogen width for a given accretionary flux. Erosion (Willett 1999): Ne = k h / V_p sets whether a plateau forms: low Ne (weak erodible crust or dry climate) gives a broad, plateau-like profile; high Ne gives low topography.
6. Erosion magnitudes: global 10Be medians 0.005 to 0.05 mm/yr (outcrops to basins); seismically active basins ~0.37 mm/yr mean (Portenga and Bierman 2011). Active orogens: Taiwan 3 to 6 mm/yr (Dadson et al. 2003 abstract; 2 to 8 mm/yr Central Range per Derrieux 2014 summary); Central Alps 0.9 mm/yr (Wittmann, summary). Montgomery and Brandon (2002) Ganges/Brahmaputra fit: E = 0.2 Rz mm/yr (Rz km): a 3 km relief gives ~0.6 mm/yr. Use mm/yr-level erosion in steep active belts, not 0.01 mm/yr.
7. Plateau mechanisms: (a) lower-crust flow (Clark and Royden 2000: 1e18 Pa s at low-gradient margins, 1e21 at steep margins for a 15 km channel; Royden et al. 2008 eastern Tibet flow); (b) mantle lithosphere removal or dripping (Molnar et al. 1993 claim of 1000 m in a few Myr; Hoke and Garzione 2008 Andes; Anatolia 1 to 2 km from delamination; sources disagree on share); (c) shortening and thickening (Argand 1920s, Airy, Isacks 1988 for Altiplano). Plateau interior elevation is constrained by strength; Willett (1999) cites lower-crust flow limiting thickness and elevation (Bird 1991; Royden 1996).
8. Uncertainty to surface, not hide: Tibet paleoaltimetry is disputed (Rowley and Currie 2006: > 4 km for >= 35 Myr; Deng and Ding 2015 summary of late vs early camps; Spicer et al. 2021 argue against a single uplift). Mongolia elevation conflicts (1500 m from brief vs ~4 km in one abstract; search summaries). Crustal thickness estimates vary by 10 to 20 km across methods; density contrast (rho_m 3100 vs 3300) changes Airy root by factor ~1.7.
9. Not verified (do not use as hard parameters yet): Cortial 2019 uplift formula; Taiwan peak height and width (3.9 km and ~100 km are from memory, UNVERIFIED); Alps Moho 50 to 60 km (Spada 2012/2013, not read); Zagros elevation 1.8 km (search summaries); Molnar et al. 1993 numbers (abstract only); Flament 2013 dynamic topography amplitude < 2 km (abstract only).
10. Shortening vs thickening share and elevation: a practical rule for a terrain generator is to set target elevation H, compute required root r = H * rho_c/(rho_m - rho_c), then set total thickening = r, and choose the convergence duration so that dt/dt * T = r; erosion then reduces H. The ratio of root to elevation is fixed by density, so the variable inputs are convergence rate, width and duration, plus an erosion number that caps H.

## URLs read (fetched and grepped, or abstracts read in search results and used)
Fetched and read as text:
- https://www.cs.purdue.edu/homes/bbenes/papers/Cordonnier16CGF.pdf (Cordonnier et al. 2016 CGF)
- https://www.tectonics.caltech.edu/meetings/journal_club/session4/Willett1999JGR.pdf (Willett 1999 JGR, course copy)
- https://www.geosociety.org/gsatoday/archive/21/8/pdf/i1052-5173-21-8-4.pdf (Portenga and Bierman 2011 GSA Today)
- https://www.tectonics.caltech.edu/meetings/journal_club/session2/Molnar_and_England1990Nature.pdf (Molnar and England 1990 Nature review)
- https://ocw.mit.edu/courses/12-002-physics-and-chemistry-of-the-terrestrial-planets-fall-2008/74fb28dc068682451773d2616e914ff2_MIT12_002f08_lec26.pdf (MIT lecture, Airy and Tibet example)
- https://www.geologyrocks.co.uk/people/pinter/pdf/IsostasyExercise.pdf (Pinter isostasy exercise)
- https://basin.earth.ncu.edu.tw/Course/SeminarII/abstract2014_1/2014.10.02_Sun,%20Yuan-Cheng/Topographic%20ooze%20building%20the%20eastern%20margin%20fo%20Tibet%20by%20low%20crustal%20flow.pdf (Clark and Royden 2000 Geology, course copy)
- https://geoscience-prey.sydney.edu.au/Teaching/Geos-3003/geos3003papers/RoydenScience98.pdf (Royden et al. 1997 Science)
- https://hilst.mit.edu/wp-content/uploads/2017/05/2008_science_321-1054-1058.pdf (Royden, Burchfiel, van der Hilst 2008 Science)
- https://www.sas.rochester.edu/ees/SIREAL/PDF_files/Hoke_and_Garzione_2008_EPSL.pdf (Hoke and Garzione 2008 EPSL)
- https://www.sas.rochester.edu/ees/SIREAL/PDF_files/Molnar_and_Garzione_2007_Tectonics.pdf (Molnar and Garzione 2007 Tectonics)
- https://earthweb.ess.washington.edu/roe/Web/GerardWeb/Publications_files/RoeEtal_WedgeTheory_GSA06.pdf (Roe, Stolar, Willett 2006)
- https://repository.geologyscience.ru/bitstream/handle/123456789/28097/Mont_02.pdf?sequence=1 (Montgomery and Brandon 2002 EPSL)
- https://se.copernicus.org/articles/13/745/2022/se-13-745-2022.pdf (Ye et al. 2022 Solid Earth, grepped)
- https://www.cs.purdue.edu/homes/bbenes/papers/Peytavie19CGF.pdf and Perche23CGF.pdf (downloaded, not relevant)
- https://diglib.eg.org/bitstreams/0b159ae6-4104-4325-be37-0ce97149537c/download (returned a different 2026 paper; not used)
Read from search results and abstracts (not full text; marked UNVERIFIED in the text):
- https://diglib.eg.org/handle/10.1111/cgf13614 (Cortial 2019 record)
- https://www.nature.com/articles/nature02150 and https://ideas.repec.org/a/nat/nature/v426y2003i6967d10.1038_nature02150.html (Dadson 2003)
- https://scholar.lib.ntnu.edu.tw/en/publications/erosion-rates-and-orogenic-wedge-kinematics-in-taiwan-inferred-fr-2/ (Willett et al. 2003 abstract)
- https://www.citedrive.com/en/discovery/the-significance-of-inherited-crustal-thickening-in-surface-uplift-of-hangai-dome-in-central-mongolia/ (Hangai 2026 GRL)
- https://agu.confex.com/agu/fm14/webprogram/Paper7993.html (Hangay dome 4 km abstract)
- https://www.nature.com/articles/nature05368.pdf (Rowley and Currie 2006 / Molnar et al. 2006, not read)
- https://ideas.repec.org/a/nat/nature/v439y2006i7077d10.1038_nature04506.html (Rowley and Currie 2006 record)
- https://academic.oup.com/nsr/article/2/4/417/2936891 (Deng and Ding 2015 NSR)
- https://www.geologist.nl/wp-content/uploads/2021/10/2021_McPhee_Tectonophysics.pdf (McPhee et al. 2021 Anatolia)
- https://www.cambridge.org/core/product/19E9DEA9D3C59A77EFB14BFA4B36A1E2/core-reader (Iran plateau review)
- https://core.ac.uk/download/47308989.pdf (Paul et al. 2006 Zagros)
- https://gfzpublic.gfz-potsdam.de/pubman/item/item_238796_1/component/file_238795/13194.pdf (Wittmann Alps)
- https://repository.ias.ac.in/21806/1/346.pdf and https://www.ncedc.org/ftp/outgoing/burgmann/REPRINTS/Banerjee_GRL2008.pdf (India-Eurasia GPS)
- https://www.earthbyte.org/Resources/Pdf/Flament_etal_2013_ObservationsAndModelsOfDynTopo.pdf (Flament 2013 search only)
- https://typeset.io/pdf/crustal-thickness-variations-in-the-central-andes-3utl2dce6o.pdf (Beck et al. Andes summary)
- https://www.x-mol.com/paper/1308484164113371136 (Tibet crust 70 km summary)
- https://meetingorganizer.copernicus.org/EGU2018/EGU2018-10124.pdf?EGUsphere (Tibet upper crust stress abstract)
- https://www.nature.com/articles/s41467-018-07312-9 (Tibet model abstract snippet)
- https://www.tectonics.caltech.edu/publications/pdf/Hsu_Tectonophysics_2009.pdf (Taiwan convergence snippet)
- https://repository.geologyscience.ru/handle/123456789/28097 (Montgomery and Brandon record)
- https://www.sas.rochester.edu/ees/SIREAL/PDF_files/Hoke_and_Garzione_2008_EPSL.pdf (also used for Andes shortening)
- https://goldschmidtabstracts.info/2006/1084.pdf (Himalaya sediment flux snippet)
- https://se.copernicus.org/preprints/se-2020-179/se-2020-179-manuscript-version3.pdf (Alps Moho search snippet only)
- https://www.nature.com/articles/s41467-018-07312-9 (listed above)
- https://earthref.org/ERR/62502 (Molnar, England, Martinod 1993 record listing)

## Failed fetches
- https://mantleplumes.awh.durham.ac.uk/WebDocuments/Gogus2008_Geology.pdf: TLS certificate verification failed (curl exit 60), also with the proxy CA bundle /root/.ccr/ca-bundle.crt. Not bypassed.
- https://planetarygeoscience.uchicago.edu/doc/Dahlen_Annual_Reviews.pdf: same TLS failure.
- https://www.earthbyte.org/Resources/Pdf/Flament_etal_2013_ObservationsAndModelsOfDynTopo.pdf: returned an HTML page, not a PDF.
- https://www.cs.purdue.edu/homes/bbenes/papers/Perche23CGF.pdf and Cordonnier16CGF.pdf via oku.py: returned empty text (used curl instead; worked).
- https://diglib.eg.org/items/d7b74043-dcb2-4b18-b128-5ec43b73548d/full via oku.py: empty output (Cortial 2019 full text still not read).
- https://diglib.eg.org/bitstreams/0b159ae6-4104-4325-be37-0ce97149537c/download: a different 2026 paper, not Cortial 2019.
- Not found in search (no full text located): Willett and Brandon 2002 (GSA Geology), Galy and France-Lanord 2001, Gilchrist and Stern 1994, Burbank et al. 1996 Nature (search returned a different NW Himalaya paper), Rey et al. 2001 Tectonophysics, Kay and Kay 2000, Bird 1991, Spada et al. 2013, Herman et al. 2013, Molnar et al. 1993 full text, Garzione et al. 2008 Science full text, Yin and Harrison 2000 full text, Dadson 2003 full text, Willett et al. 2003 full text.
