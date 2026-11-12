# A: Lithospheric flexure for foreland basins (working notes)

Status: COMPLETE for the search scope (2026-11-12 continuation). Failed fetches listed at end.

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

## Audet and Burgmann 2011 critique (Kalnins et al. 2015)
- Source read: https://geoweb.princeton.edu/people/simons/PDF/reprints/EPSL-2015b.pdf (Kalnins, Simons, Kirby, Wang, Olhede, EPSL 419:43-51)
- Abstract: North American continent "does not exhibit meaningful anisotropy in its mechanical strength"; global reanalysis finds "only scant evidence for lithospheric flexural anisotropy". Same URL.
- Implication for tool: do not model mechanical anisotropy of Te; use isotropic Te.
- Audet and Burgmann 2011 (Nat Geosci 4:184-187, DOI 10.1038/NGEO1080) full text: FAILED (ncedc PDF reset/SSL; not read). Only the search summary, which says Te is high on Archean cratons and low in Phanerozoic belts.

## Forebulge in the stratigraphic record (Horton 2022, J. Geol. Soc. 179, jgs2020-263, "Unconformity development in retroarc foreland basins")
Source read: https://par.nsf.gov/servlets/purl/10329923 (PDF; DOI https://doi.org/10.1144/jgs2020-263)
- Advancing wedge: cratonward migration of the flexural wave gives a diachronous unconformity (basal foreland unconformity). Same URL.
- Continuous steady forebulge advance "is considered unlikely"; jumps / punctuated migration more probable (preferential reactivation of structures). Same URL.
- "A stronger plate (higher flexural rigidity and Te) toward the craton fosters a greater flexural wavelength and broader forebulge through time" (cites Stockmal et al 1986; Waschbusch and Royden 1992; Fosdick et al 2014). Same URL.
- Forebulge: erosion in proximal/forebulge zone and bypass or reduced accommodation in medial-distal foreland. Same URL.
- Forebulge depozone unconformity and condensation: DeCelles and Giles 1996 (Basin Research) framework is cited here but the DeCelles and Giles 1996 PDF itself was not read (the PAR link resolved to Horton 2022).
- Foredeep-forebulge timing examples: Nepal Eocene-Oligocene unconformity ~15-20 Myr tied to forebulge migration (search summary; UNVERIFIED in body).

## Failed or unverified
- DeCelles 2012 (USGS PDF): returned HTML, FAILED.
- Audet and Burgmann 2011 (ncedc PDF): FAILED (connection reset / SSL). Not read.
- Burov and Watts 2006 (topex PDF): FAILED (SSL, proxy CA). Not read.
- Jordan 1981 full text and datapages abstract: datapages returned 41 chars, FAILED. Only search summary: flexural rigidity ~1e23 N m (search summary; UNVERIFIED). Jordan 1981 Te = 25 km from later citing paper (UNVERIFIED).
- Beaumont 1981 GJRAS 65:291-329: not retrieved; only citation and "viscoelastic plate model" from secondary (UNVERIFIED for numbers).
- Watts and Burov 2003 EPSL: not retrieved (the NSF link was Bellas 2022).
- Pérez-Gussinyé and Watts 2005 Nature Alps values: not retrieved. Malinverno and Haxby 1995 search summary: western Alps Te 30-39 km, eastern Alps 33-40 km (UNVERIFIED; the source was not read).
- Tesauro et al. 2012 G-cubed global Te map: NCEDC PDF FAILED (reset). Search summary only.

## IMPLEMENTATION FORMULAS (for the programmer)

Assumptions common to all: thin elastic plate (h << radius of curvature), 2D cylindrical bending (line load infinite along strike), plane stress, linear elasticity, small deflections, neutral surface at mid-plate, constant D unless noted, Winkler foundation (inviscid mantle, no viscous relaxation), no plate-wide compressive load P.

1. Flexural rigidity: D = E Te^3 / (12 (1 - nu^2)). Source: Stewart and Watts 1997 eq (2.2), https://ora.ox.ac.uk/objects/uuid:9f803b42-522e-442b-9849-bb8e6c2a5494/files/m88d0e5b84c28370abf6d7b84438cc52d ; Besson 2023 gives the same D form, https://se.copernicus.org/articles/14/197/2023/
   Values: E = 1e11 Pa, nu = 0.25 (both Stewart and Watts 1997 and Lin and Watts 2002 tables).
2. Governing ODE: D d^4w/dx^4 + (rho_m - rho_infill) g w = rho_load g q(x) (+ P term if used). Besson 2023 (structure confirmed), https://se.copernicus.org/articles/14/197/2023/
3. Flexural parameter: alpha = [4 D / ((rho_m - rho_infill) g)]^(1/4). MIT 12.520 notes (same as lambda = 1/alpha in NCU lecture). https://ocw.mit.edu/courses/12-520-geodynamics-fall-2006/353f42887f4ee449a0bd1602660dd0ae_lecture20.pdf ; https://basin.earth.ncu.edu.tw/download/courses/basin_analysis/4_flexure.pdf
4. Continuous plate, total line load V0 split half per side: w(x) = w0 exp(-x/alpha)[cos(x/alpha) + sin(x/alpha)], w0 = V0 alpha^3 / (8D). Zero crossing x0 = 3 pi alpha / 4; forebulge (uplift max) x_b = pi alpha; w_b = -exp(-pi) w0 = -0.0432 w0. MIT (same URL).
5. Broken plate (M = 0 at break), total load V0 split half to each side: w(x) = w0 exp(-x/alpha) cos(x/alpha), w0 = V0 alpha^3 / (4D). Zero crossing x0 = pi alpha / 2; forebulge x_b = 3 pi alpha / 4; w_b = -0.067 w0. MIT (same URL).
6. General prefactor (my derivation, consistent with MIT): continuous w0 = V_b alpha^3/(4D), broken w0 = V_b alpha^3/(2D), where V_b is the shear applied per side. Flagged: the NCU lecture broken-plate prefactor implies a ratio of 4 (not 2); unresolved, use MIT.
7. Sign: negative w under load (down). Forebulge is the negative-w minimum: w_b < 0 means uplift in the MIT convention, so the tool should flip sign when writing elevations.

## Worked numbers (my computation from formulas 1, 3, 4; E=1e11, nu=0.25, g=9.81; mantle 3300 kg/m3, infill 2500 kg/m3; not from a source)
Te (km) | D (N m) | alpha (km) | continuous x0 = 3pi alpha/4 (km) | continuous x_b = pi alpha (km)
5 | 1.1e21 | 27.4 | 64.6 | 86.2
10 | 8.9e21 | 46.1 | 108.7 | 144.9
20 | 7.1e22 | 77.6 | 182.8 | 243.8
30 | 2.4e23 | 105.2 | 247.8 | 330.4
40 | 5.7e23 | 130.5 | 307.5 | 410.0
60 | 1.9e24 | 176.9 | 416.7 | 555.6
80 | 4.6e24 | 219.5 | 517.1 | 689.5
Infill sensitivity at Te = 30 km (alpha, km; continuous bulge pi alpha): infill 2000: 93.1 (292.6); 2300: 99.5 (312.5); 2500: 105.2 (330.4); 2700: 113.0 (355.0); 3000: 134.4 (422.2). Lower infill density makes alpha smaller only weakly; alpha scales as (rho_m - rho_infill)^(-1/4).
Derived inverse check: a continuous-plate bulge at ~120 km (Swiss Molasse-type "original" wavelength, Hindle and Kley 2021) with infill 800 kg/m3 contrast implies alpha ~ 38 km and Te ~ 8 km (my calculation). Broken-plate or buried-load models give different Te; Lin and Watts 2002 state surface loads alone do not explain the depth and width of West Taiwan basin.

## Te value summary (with status)
- Continental Te range 5-110 km, bimodal peaks 10-30 and 70-90 km: Tesauro, Kaban, Cloetingh 2009 citing Burov and Diament 1995 (READ). https://research.vu.nl/ws/files/2522156/227389.pdf
- Global best fit (gravity and topography spectra) 34 +/- 4 km: Watts and Moore EGU 2017 abstract (search only, UNVERIFIED body).
- Himalaya foreland: 40 to over 90 km, > 70 km in foreland region (Stewart and Watts 1997, READ).
- Zagros: over 60 km in foreland to near zero beneath high Zagros (Stewart and Watts 1997, READ).
- Oman ophiolite load: 30 km (Stewart and Watts 1997, READ).
- West Taiwan basin (rifted margin): 13 km (Lin and Watts 2002, READ). https://basin.earth.ncu.edu.tw/publications/papers/Lin&Watts_2002.pdf
- Appalachians: 40-70 km (search snippet of Stewart and Watts, UNVERIFIED in body); Stewart and Watts 1997 body says rigidity stayed high ~300 Myr (READ).
- Andes: 5-85 km range, correlated with orogen width (Stewart and Watts 1997 abstract, READ for width correlation).
- Alps: western 30-39 km, eastern 33-40 km (Malinverno and Haxby 1995 summary, UNVERIFIED); Tesauro 2009: Alpine domain Te(strength) 20-34 km vs Te(age) 13-18 km (READ).
- Apennines and Pannonian: Te 20-35 km, lower Te (Tesauro 2009, READ).
- Subhercynian and Molasse broken or short-wavelength cases: Hindle and Kley 2021 (READ).
- Ocean Te vs thermal age (450 C isotherm, 10-40 km for 20-130 Ma, model-based): Bellas, Zhong, Watts 2022 (READ). https://par.nsf.gov/servlets/purl/10391238

## Te versus thermal age (continents): NO simple relation (Tesauro et al 2009, READ). Oceans: Te tracks a ~450 C isotherm in lab-rheology models (Bellas et al 2022, READ). Burov and Watts 2006 full text NOT READ.

## Disagreements and ranges (summary)
- Te definition: strength-based vs age/depth-based vs coherence-based give different numbers (Tesauro et al 2009, 2012; Burov and Diament 1995).
- Thin-plate vs viscoelastic: MIT/NCU use elastic plate; NCU shows viscoelastic example Te = 67 km, tau = 27.5 Myr. Beaumont 1981 (viscoelastic) was not read.
- Jelly sandwich vs creme brulee: unresolved in this session (Burov and Watts 2006 not read; Tesauro 2009 supports strength-based multilayer view for Europe).
- Anisotropy in Te: Audet and Burgmann 2011 vs Kalnins et al 2015 (no meaningful anisotropy in N. America).
- Broken vs continuous: Lin and Watts 2002, Hindle and Kley 2021 both argue for broken or buried-load models in foreland settings (basins too narrow with low Te, too shallow with high Te for a continuous plate).
- Forebulge location: "3 pi alpha/4" is the continuous-plate zero crossing (MIT) and the broken-plate forebulge (MIT), so the common shorthand is ambiguous; use the MIT formulas above.

## Gaps not filled
- Typical foredeep depth and width vs plate age: no sourced table found. Only Molasse (120 km, 5-7 km) and Subhercynian (25-40 km, ~2500 m) examples (Hindle and Kley 2021, READ).
- Watts 2001 book, Turcotte and Schubert 2002 text, Beaumont 1981, Jordan 1981 full text: not read (blocked or not retrieved).

## URLs read (full or relevant text)
- https://se.copernicus.org/articles/14/197/2023/ (Besson 2023)
- https://se.copernicus.org/articles/12/2425/2021/ (Hindle and Kley 2021)
- https://ocw.mit.edu/courses/12-520-geodynamics-fall-2006/353f42887f4ee449a0bd1602660dd0ae_lecture20.pdf (MIT OCW lecture 20)
- https://basin.earth.ncu.edu.tw/download/courses/basin_analysis/4_flexure.pdf (NCU Lin lecture, garbled formulas)
- https://basin.earth.ncu.edu.tw/publications/papers/Lin&Watts_2002.pdf (Lin and Watts 2002)
- https://ora.ox.ac.uk/objects/uuid:9f803b42-522e-442b-9849-bb8e6c2a5494/files/m88d0e5b84c28370abf6d7b84438cc52d (Stewart and Watts 1997)
- https://research.vu.nl/ws/files/2522156/227389.pdf (Tesauro, Kaban, Cloetingh 2009 GRL)
- https://par.nsf.gov/servlets/purl/10391238 (Bellas, Zhong, Watts 2022 GJI)
- https://par.nsf.gov/servlets/purl/10329923 (Horton 2022 JGS, forebulge unconformities)
- https://geoweb.princeton.edu/people/simons/PDF/reprints/EPSL-2015b.pdf (Kalnins et al 2015)
- https://www.earth.ox.ac.uk/node/3837911 (Oxford page, no content; search summary only)

## URLs from search summaries only (not read)
- https://topex.ucsd.edu/geodynamics/BurovWatts2006.pdf (Burov and Watts 2006; FAILED fetch)
- https://ncedc.org/ftp/outgoing/burgmann/REPRINTS/Audet_NGEO2011.pdf (FAILED)
- https://ncedc.org/ftp/outgoing/burgmann/REPRINTS/Tesauro_Gcubed_2012.pdf (FAILED)
- https://archives.datapages.com/data/bulletns/1980-81/data/pg/0065/0012/2500/2506.htm (Jordan 1981 abstract; FAILED)
- https://blogs.egu.eu/divisions/gd/?p=1016 (blog, Stewart and Watts summary)
- https://meetingorganizer.copernicus.org/EGU2017/EGU2017-4648.pdf?pdf (Watts and Moore 2017 abstract)

## Failed fetches
- topex BurovWatts2006.pdf: SSL certificate chain error through proxy CA (no full fix found in README beyond bundle, which also failed).
- ncedc Audet_NGEO2011.pdf and Tesauro_Gcubed_2012.pdf: connection reset by peer (proxy tunnel failure; recentRelayFailures in proxy status).
- DeCelles 2012 USGS PDF: returned HTML.
- Datapages Jordan 1981: 41 chars only.
- Oxford node 3837911: page not found content.
- Watts and Burov 2003 EPSL: not reachable via search-given links.

## Key takeaways for the tool
1. Use the continuous-plate formulas (MIT / Turcotte and Schubert form) as the default: alpha = (4D/((rho_m - rho_infill) g))^(1/4), D = E Te^3/(12(1-nu^2)), E = 1e11 Pa, nu = 0.25, rho_m ~ 3200-3330, rho_infill ~ 2500 kg/m3. The forebulge is at pi alpha, the zero crossing at 3 pi alpha/4, and the bulge depth is -0.043 w0.
2. Make the broken-plate option a separate switch: x_b = 3 pi alpha/4, x0 = pi alpha/2, w0 = V0 alpha^3/(4D), w_b = -0.067 w0. Broken plates better match narrow real foredeeps (Hindle and Kley 2021; Lin and Watts 2002).
3. Continuous Te = 30 km gives a bulge at ~330 km; real Molasse-type bulges are ~120 km, which implies Te ~ 8 km for a continuous plate (derived). Expect the tool to be too wide unless Te is low or the plate is broken. Keep Te in 5-40 km for most foreland belts and allow up to 60-80 km for cratonic forelands (Stewart and Watts 1997; Tesauro 2009).
4. Te is not a function of thermal age on continents (Tesauro 2009). If the tool wants a Te-age rule, use it only for oceans (Bellas et al 2022, ~450 C isotherm) and treat continents as a free parameter per belt.
5. Infill density matters: alpha scales as (rho_m - rho_infill)^(-1/4); going from 2500 to 2000 kg/m3 shrinks alpha by ~11% at Te 30 km (table above). Infill density is a weak lever on wavelength but a strong one on the depth via V0 alpha^3/D (w0 scales with alpha^3).
6. Depth scale: w0 = V0 alpha^3 / (8D) for continuous; the bulge height is a fixed fraction of w0 (0.043 for continuous, 0.067 for broken). Use load V0 as the total line load (N/m) with the half-per-side convention stated in code.
7. Anisotropy: do not model Te anisotropy (Kalnins et al 2015).
8. Jelly sandwich vs creme brulee: unresolved; use the strength-based Te as an upper-bound option and document it. Burov and Watts 2006 not read.
9. Forebulge migration: a stronger plate gives a wider, broader forebulge (Horton 2022), so Te can be tied to forebulge migration rate in the tool, but the migration is episodic and unsteady, not constant.
10. Single-load line model ignores buried loads and sediment decoupling (Lin and Watts 2002; Stewart and Watts 1997 Zagros salt decoupling). Add buried-load support as an option if fits are needed.
