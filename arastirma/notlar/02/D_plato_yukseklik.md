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
