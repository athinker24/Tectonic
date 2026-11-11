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
