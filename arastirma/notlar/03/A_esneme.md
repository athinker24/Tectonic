# A: Lithospheric flexure for foreland basins (working notes)

Status: IN PROGRESS (2026-11-11). Sections filled as sources are read.

## Sources identified (search stage, not yet read in full)
- Burov and Watts 2006 (jelly sandwich vs creme brulee): https://topex.ucsd.edu/geodynamics/BurovWatts2006.pdf
- Audet and Burgmann 2011 Nat Geosci, DOI 10.1038/NGEO1080 (search gave this DOI; PDF mirror): https://ncedc.org/ftp/outgoing/burgmann/REPRINTS/Audet_NGEO2011.pdf
- Tesauro, Audet, Kaban, Burgmann, Cloetingh 2012 G-cubed: https://ncedc.org/ftp/outgoing/burgmann/REPRINTS/Tesauro_Gcubed_2012.pdf
- Tesauro, Kaban, Cloetingh 2012 Global Planetary Change 90-91:51-57, DOI 10.1016/j.gloplacha.2011.12.003 (not yet read)
- Tesauro, Kaban, Cloetingh 2013 Tectonophysics 602:78-86, DOI 10.1016/j.tecto.2013.01.006 (not yet read)
- Jordan 1981 AAPG Bull 65(12):2506-2520 "Thrust loads and foreland basin evolution, Cretaceous, western US" (abstract only so far): https://archives.datapages.com/data/bulletns/1980-81/data/pg/0065/0012/2500/2506.htm
- Kalnins et al. 2015 critique of Audet & Burgmann anisotropy (EPSL 2015b PDF): https://geoweb.princeton.edu/people/simons/PDF/reprints/EPSL-2015b.pdf
- Stewart and Watts 1997 (Appalachian Te 40-70 km), reported only via EGU blog, not read: https://blogs.egu.eu/divisions/gd/?p=1016
- Watts and Moore EGU 2017 global Te 34 +/- 4 km (abstract, EGU2017-4648): https://meetingorganizer.copernicus.org/EGU2017/EGU2017-4648.pdf?pdf

## Facts confirmed from reading sources
(to be filled)

## Facts from search snippets only (UNVERIFIED until read)
- Continental Te range 5-110 km, bimodal peaks near 10-30 km and 70-90 km (source: search summary of EGU/blog material; UNVERIFIED)
- Jordan 1981 model used Te = 25 km (from a later citing paper, UNVERIFIED)
- Burov and Watts 2006 framed jelly sandwich as more widely applicable (search summary; verify in text)

## Confirmed facts (read in text)

### Plate equation and rigidity (Besson 2023, Solid Earth 14:197)
- Source read: https://se.copernicus.org/articles/14/197/2023/ (text read; the equation images did not survive extraction, so the explicit form below is confirmed in structure only, cross-checked against MIT below)
- Structure: fourth-order ODE, plate on a Winkler (inviscid fluid) foundation: D u'''' + (rho_m - rho_inf) g u = rho_L g q(x) (+ P u'' term for plate-wide stress). Confirmed statements: u(x) deflection; D = E h^3 / (12 (1 - nu^2)) with E elastic modulus, h effective elastic thickness, nu Poisson ratio (text: "D ... is given by ... where E is the elastic modulus ... h the elastic thickness ... nu Poisson's ratio"). Gunn 1943 origin. Foreland basins cited as application (Beaumont 1981).
- Note: Besson says the infill term can be treated either as load term (iterative) or moved to the left (direct). Infill density rho_F appears in the restoring term, which is the reason infill density changes wavelength.

### Continuous and broken plate line-load solutions (MIT OCW 12.520 Lecture 20, 2006)
Source read: https://ocw.mit.edu/courses/12-520-geodynamics-fall-2006/353f42887f4ee449a0bd1602660dd0ae_lecture20.pdf (PDF, text via pdftotext)
- Flexural parameter: alpha = [4D / ((rho_m - rho_w) g)]^(1/4). For foreland infill replace rho_w by rho_infill (in the notes, rho_w is the fill of water).
- Continuous plate, line load V0 (total, half taken by each side), x >= 0:
  w(x) = w0 exp(-x/alpha) [cos(x/alpha) + sin(x/alpha)],  w0 = V0 alpha^3 / (8 D)
  Zero crossing x0 = 3 pi alpha / 4.  Forebulge (max upward deflection) x_b = pi alpha.  Bulge amplitude w_b = -exp(-pi) w0 = -0.0432 w0.
- Broken plate (free end at the load, M=0 at x=0): w(x) = w0 exp(-x/alpha) cos(x/alpha),  w0 = V0 alpha^3 / (4 D)
  Zero crossing x0 = pi alpha / 2.  Forebulge x_b = 3 pi alpha / 4.  w_b = -0.067 w0.
- Notes state Te about 35 km (unbroken) vs 50 km (broken) as an example, and the "broken is about 1.5x thicker" rule.
- Independent check (my derivation, not from a source): w = w0 e^{-u}(cos u + sin u) = sqrt(2) w0 e^{-u} sin(u + pi/4); zero at u = 3pi/4; dw/du = -2 w0 e^{-u} sin u = 0 at u = pi (bulge). Broken: w = w0 e^{-u} cos u; zero at u = pi/2; dw/du = 0 at tan u = -1, u = 3pi/4. Consistent with MIT.
- Caveat for the tool: the literature term "forebulge at 3pi/4 alpha" applies to the BROKEN plate; for the continuous plate the bulge is at pi alpha and 3pi/4 alpha is the zero crossing.

### Numbers from Hindle and Kley 2021 (Solid Earth 12:2425)
Source read: https://se.copernicus.org/articles/12/2425/2021/ (text)
- Subhercynian Basin (broken plate, intraplate): wavelength ~25-40 km (short), amplitude ~2500 m; the Swiss Molasse Basin "original" wavelength ~120 km and 5-7 km amplitude (cites Burkhard and Sommaruga 1998; Homewood et al. 1986). Source: same URL, line 24.
- Broken plate segments of 15-20 km behave as rigid blocks (McQueen and Beaumont 1989 concept). Source: same URL.
- Te at fault positions near zero when broken; general Te definition cites Burov and Diament 1995. Source: same URL.

### Prefactor rule (my derivation, checked against MIT; NOT a quoted source formula)
- Decaying solutions: continuous w = C e^{-u}(cos u + sin u) with third derivative at 0 equal to 4C/alpha^3; broken w = C e^{-u} cos u with third derivative 2C/alpha^3 (u = x/alpha). Shear balance V_b = D |w'''(0)|.
- Continuous (symmetric, shear per side V_b): w0 = V_b alpha^3 / (4D). With V_b = V0/2 gives w0 = V0 alpha^3/(8D) (MIT).
- Broken (M=0 at break, shear V_b): w0 = V_b alpha^3 / (2D). With V_b = V0/2 (MIT Fig 20.3 splits the load) gives w0 = V0 alpha^3/(4D) (MIT).
- Tool rule: define the load as V0 total, split as above. Use sign convention: deflection negative under load (downward) in MIT.

### DISCREPANCY: NCU lecture (Lin, courtesy Watts) prefactors
Source: https://basin.earth.ncu.edu.tw/download/courses/basin_analysis/4_flexure.pdf (text extraction garbled)
- Continuous plate written as y = (P b lambda / [2 (rho_m - rho_inf) g]) e^{-lambda x}(cos + sin), with lambda = [(rho_m - rho_inf) g / (4D)]^{1/4} = 1/alpha. Consistent with MIT (P b lambda/(2 Delta rho g) = alpha^3/(8D) per unit load).
- Broken plate written as y = (2 P b lambda / [(rho_m - rho_inf) g]) e^{-lambda x} cos(lambda x). This implies a broken/continuous prefactor ratio of 4, whereas MIT and my derivation give 2 for the same total load. UNRESOLVED: may be an extraction error or a different load definition (P b vs V0). Tool should use the MIT/derived form and state the load convention.
- NCU lecture also states the Te = 67 km, tau = 27.5 Myr viscoelastic example and the Watts et al. 1995 idea that high Te gives thin-skinned and low Te gives thick-skinned deformation (same URL, text).

### DeCelles 2012 fetch FAILED
- https://rmgsc.cr.usgs.gov/outgoing/temp/sjohnstone/OllieLiterature/Stratigraphy/Decelles_2012_ForelandBasinSystemsRevisited.pdf returned an HTML page (1.2 KB), not the PDF. Failed fetch.

## Te numbers for forelands, from Stewart and Watts 1997 (JGR 102:5327)
Source read (text extraction of the Oxford ORA PDF): https://ora.ox.ac.uk/objects/uuid:9f803b42-522e-442b-9849-bb8e6c2a5494/files/m88d0e5b84c28370abf6d7b84438cc52d (abstract; also the body text)
- Oman (ophiolite load, profiles orthogonal to strike): Te = 30 km best fit.
- Himalayan foreland: recovered Te from 40 to over 90 km; profile- and grid-based both give Te > 70 km in the foreland region; beneath the Tibetan plateau Te generally < 10 km.
- Arabia-Eurasia (Zagros): Te over 60 km in the foreland region to close to zero beneath the high Zagros.
- Andes: correlation between orogen width and foreland Te; Andes Te range 5-85 km (cited in search; body text confirms width correlation).
- Appalachians (Karner and Watts 1983): rigidity high for ~300 Myr, supports elastic model; search summary gives Te 40-70 km (UNVERIFIED in body, the 40-70 km statement is from the search snippet).
- Global: grid-based Te from ~0 to over 90 km; low Te in active belts; high in cratons (abstract).
- Tectonic link: high-Te foreland correlates with overthrusting in Himalaya and Andes (abstract).

## Caveat
- Lin and Watts 2002 (Taiwan) and Stewart and Watts 1997 use the 2D elastic beam with buried loads; Te recovered is sensitive to the infill, so Te depends on the density model.

## Parameter values (confirmed in two sources)
- E = 1e11 Pa, nu = 0.25: Stewart and Watts 1997 Table (text, ORA copy) https://ora.ox.ac.uk/objects/uuid:9f803b42-522e-442b-9849-bb8e6c2a5494/files/m88d0e5b84c28370abf6d7b84438cc52d ; and Lin and Watts 2002 Table (text): https://basin.earth.ncu.edu.tw/publications/papers/Lin&Watts_2002.pdf
- Stewart and Watts eq (2.2): D = E Te^3 / (12 (1 - nu^2)) (same ORA source). They note E and nu "may vary" but are fixed for comparability.
- Densities in Lin and Watts 2002 (Taiwan, Luzon-type orogen, Table): mantle 3200, crust 2800, infill 2500, topographic load 2600, water 1030 kg/m3. Stewart and Watts 1997 uses substrate (mantle) density 3330 kg/m3 in its Table.
- Lin and Watts 2002 finding (text): "Models with a low Te (e.g., 5 km) predict the ... basin is too narrow ... Models with a high Te (e.g., 20 km) predict the width, but the depth of the basin is too low. Therefore surface loading of a continuous elastic plate ... is unable to fully explain the shape of the foreland basin." Broken-plate models successfully explain Appalachian, central Andes, Himalaya basins (same URL). This is the depth-width tradeoff for the tool; cite as a published observation.
- Kinds of foreland infill: sediment density used in models 2500 kg/m3 (Lin and Watts).

## Te versus age and isotherm (Bellas, Zhong, Watts 2022, GJI 228:857-875)
Source read: https://par.nsf.gov/servlets/purl/10391238 (NOTE: the URL labelled as Watts and Burov 2003 actually resolved to this 2022 paper; the Watts and Burov 2003 EPSL paper was NOT read. FAILED for that paper.)
- Lab-derived (viscoelastic/yield) rheology: Te falls along the ~450 C isotherm depth, giving ~10-40 km for seafloor age 20-130 Ma (Suite 6; "lower bound for Te"). Same URL, p.864.
- Larger loads (A0 = 6 km, seamount scale): Te between 600 and 900 C isotherms, ~25-80 km depth. Same URL.
- Stress dependence / friction / creep temperature change Te by only 1-15 percent. Same URL.
- Observational catalogue used by them: 101 Te estimates from flexural systems across the oceans (31 from French Polynesia, Watts and Zhong 2000). Same URL.
- Load density 3330 kg/m3 and shear modulus 3.33e10 Pa in their model table. Same URL.
- Oceanic Te vs age: the thermal age relation (Te roughly the depth of a ~450 C isotherm) is a model result here, not an observed universal law. Good for the tool as a continental-agnostic oceanic rule only.

## Continental Te: jelly sandwich, bimodal range, Te versus age (Tesauro, Kaban, Cloetingh 2009 GRL "How rigid is Europe's lithosphere?")
Source read (PDF via VU Research Portal): https://research.vu.nl/ws/files/2522156/227389.pdf
- Continental Te "have a wide range of values (5-110 km), typically with a bimodal distribution around two peaks at 10-30 km and 70-90 km" (citing Burov and Diament 1995). Same URL.
- Two Te definitions (bottom of competent layer at 750 C for olivine vs 350 C for quartzite, Cloetingh and Burov 1996) give lower and upper bounds. Same URL.
- "No straightforward relationship between Te and thermal age is found in the continental part of the study." For provinces older than 85 Ma, Te is significantly smaller than the age-predicted value; younger provinces are the opposite. Same URL.
- Alpine domain, Northern Atlantic margin, Western Black Sea (younger than ~85 Ma): Te(strength) 20-34 km vs Te(age/h) 13-18 km. Same URL.
- Apennines and Pannonian basin: low Te (20-35 km range) with gradual strength transition; Te 80-100 km in some high-strength areas (Bohemian Massif/Adriatic); Te of 70 km in Fennoscandia. Same URL.
- Relevance to the jelly sandwich: the paper argues the mechanically strong layers (MSL) vs total strength determine Te; supports a multi-layer ("jelly sandwich" style coupling) reading for Europe, but the paper's own abstract is not fully read. Burov and Watts 2006 GSA Today is cited as the source of the debate.
- Burov and Watts 2006 (GSA Today 16(1):4-10) full text: NOT read (topex and earth.ox fetch failed or had no text). Status: abstract and summary via search only.
