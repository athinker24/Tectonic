# Topic C: parameters of landscape evolution models (stream power K, m, n, diffusion, critical slope, h_max, lithology, deposition)

Date of research: 2026-11-12. Status: complete for the reachable sources. Items not confirmed from a source I read are marked UNVERIFIED. Items I derived myself are marked DERIVED.

Method: primary PDFs were downloaded with curl and converted with pdftotext; numbers below were checked against the converted text unless stated otherwise. Where only a search-engine summary or an abstract page was available, that is said explicitly.

## 0. Quick reference (what to use, with citations)

| Quantity | Recommended starting value / range | Units | Main source (URL) | Confidence |
|---|---|---|---|---|
| m (area exponent) | 0.5 (energy/shear-stress argument); 0.35 to 0.65 tested by Mudd et al. 2018 | dimensionless | Lague 2014 (https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2014_Lague_ESPL.pdf); Mudd 2018 (https://esurf.copernicus.org/articles/6/505/2018/esurf-6-505-2018.pdf) | high for 0.5 as a default; large data-driven scatter |
| n (slope exponent) | 1 as default; Harel et al. 2016 global 10Be analysis finds n generally > 1 | dimensionless | Harel 2016 abstract (https://www.research.ed.ac.uk/en/publications/global-analysis-of-the-stream-power-law-parameters-based-on-world/) | contested |
| m/n (concavity theta) | 0.45 reference (range 0.4-0.6, Kirby and Whipple 2012 as cited by Lague 2014) | dimensionless | Lague 2014; Whipple 2004 (https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/Whipple_2004_AnnRevEPS.pdf) | high |
| K (Cordonier 2016 setting) | 5.61e-7 per yr (m = 0.5, n = 1) | yr^-1 (with A in m^2, E in m/yr) | Cordonnier 2016 (https://www.cs.purdue.edu/homes/bbenes/papers/Cordonier16CGF.pdf) | high for that model only |
| K (Fastscapelib river profile example) | 1e-4 (m = 0.5, n = 1) | time unit not stated on the page | https://fastscapelib.readthedocs.io/en/latest/examples/river_profile_py.html | medium |
| K (Landlab FastscapeEroder default) | 1e-3 (m = 0.5, n = 1) | units "vary with m_sp" per docs | https://landlab.readthedocs.io/en/latest/generated/api/landlab.components.stream_power.fastscape_stream_power.html | medium |
| K (Braun 2022 model setting) | 1e-5 m^(1-2m) yr^-1 with m = 0.4 | m^0.2 yr^-1 | Braun 2022 (https://esurf.copernicus.org/articles/10/301/2022/esurf-10-301-2022.pdf) | medium |
| K (Esurf 2025, normalised by sqrt(A)/delta) | 2.5e-5 to 5e-4 yr^-1 | yr^-1 (different normalisation, see Sect. 3) | Kargere et al. 2025 (https://esurf.copernicus.org/articles/13/403/2025/esurf-13-403-2025.pdf) | medium |
| Hillslope diffusivity D or K_c | 1e-3 to 1e-2 m^2/yr (scarps, semi-arid); about 5e-3 (humid N. California / Oregon); 1.7e-2 (frost, summit flats) | m^2/yr | Whipple 2004 lecture notes (https://ocw.mit.edu/courses/12-163-surface-processes-and-landscape-evolution-fall-2004/02cdc0e225e5d9015ff07c2bf4a2cc65_8_hillslope_evolution.pdf) | medium (secondary compilation) |
| D from Roering et al. 1999 calibration | K = 0.0032 +/- 0.0009 m^2/yr (one basin); five-basin mean 0.0036 m^2/yr | m^2/yr | Roering 1999 (https://typeset.io/pdf/evidence-for-nonlinear-diffusive-sediment-transport-on-532j2v7c1n.pdf) | high for Oregon Coast Range |
| Critical slope S_c (nonlinear diffusion) | 1.25 +/- 0.10 (tan of slope; five-basin mean 1.27); equivalent angle about 51 deg | dimensionless gradient | Roering 1999 (same) | high for that site |
| Thermal / talus limit | 30 deg (Cordonnier 2016); tan(30 deg) = 0.577 | degrees | Cordonnier 2016 | medium (a choice, not a measurement) |
| Response time / knickpoint celerity (n = 1) | V = K A^m (C = K, p = m) | m/yr | Lague 2014 (same PDF) | high |
| Rock strength effect on incision | erodibility scales inversely with tensile strength (abstract: resistance scales with square of tensile strength) | qualitative | Sklar and Dietrich 2001 (https://typeset.io/pdf/sediment-and-rock-strength-controls-on-river-incision-into-21g3zfozyk.pdf) | high (mill experiments) |
| Deposition coefficient G | 0 (pure detachment) in gOSPL default; 1 yr/m in Braun 2022 example | yr/m | gOSPL (https://gospl.readthedocs.io/en/dev/user_guide/surfproc.html); Braun 2022 | medium |

## 1. Stream power law: form, units and where K comes from

- Incision law: I = K A^m S^n (Lague 2014, Eq. 1). K "is often called erodibility and is a measure of incision efficiency", A is upstream drainage area, S the slope, m and n exponents. Source: https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2014_Lague_ESPL.pdf (ESPL 39, 38-61, 2014; DOI 10.1002/esp.3462).
- Landscape equation (Lague 2014, Eq. 2): dh/dt = U - K A^m (dh/dx)^n, with U the baselevel lowering or rock uplift rate. Same source.
- Hergarten 2020 on K: "It is a lumped parameter subsuming all influences on erosion other than channel slope and catchment size, so it is not only a property of the rock but also depends on climate in a nontrivial way (e.g., Ferrier et al., 2013; Harel et al., 2016)." Source: https://esurf.copernicus.org/articles/8/367/2020/esurf-8-367-2020.pdf (Earth Surf. Dynam. 8, 367-377).
- DERIVED units: if A is in m^2 and E in m/yr, then K has units yr^-1 m^(1-2m). For m = 0.5 this is yr^-1, which is why Cordonnier's K is in yr^-1. For other m the unit changes, so K values for different m are not directly comparable. Hergarten 2020 says the same: changing the exponent m changes "the unit and meaning of the erodibility K".
- Caveat on the "four orders of magnitude" claim in the brief: I did not find that phrase in a source I read. The Stock and Montgomery 1999 paper itself could not be fetched (Sect. 9). See Sect. 2 for what I could verify.

## 2. Stock and Montgomery 1999: lithology erodibility (secondary sources only)

- Full text NOT read. The DOI page (https://doi.org/10.1029/98JB02139) returned only "Enable JavaScript and cookies to continue". The par.nsf.gov link I first tried (https://par.nsf.gov/servlets/purl/10471890) is a different paper (Anderson et al. 2023), not Stock and Montgomery.
- EarthRef record summary (search result, https://earthref.org/ERR/42355), UNVERIFIED against the paper: for m = 0.4, K in m^0.2/yr is about 1e-7 to 1e-6 for granite and metamorphic rocks, 1e-5 to 1e-4 for volcaniclastic rocks, and 1e-4 to 1e-2 for mudstones. The same summary says this variation "could drive strong variability in the rate of long-term landscape change".
- DERIVED: these ranges together span about five decades (1e-7 to 1e-2), not four. The brief's "four orders of magnitude" therefore needs checking against the original paper before it is cited.
- Stock and Montgomery's framing of K (as quoted by a 2021-2023 paper, Anderson et al., https://esurf.copernicus.org/articles/11/995/2023/ and its preprint https://egusphere.copernicus.org/preprints/2022/egusphere-2022-1285/egusphere-2022-1285-manuscript-version3.pdf): "Erodibility is a model-dependent parameter ... m and n are exponents that can be calibrated to local conditions (e.g., Whipple and Tucker, 1999)." That paper also cites Stock and Montgomery 1999 for E = K A^m S^n with a power law between slope and drainage area.

## 3. Hergarten 2020 and the Esurf 2025 characteristic length: grid resolution and K

### 3a. Hergarten 2020 (Earth Surf. Dynam. 8, 367-377)
Source: https://esurf.copernicus.org/articles/8/367/2020/esurf-8-367-2020.pdf
- Problem: "This scaling problem causes a strong dependence of the resulting topographies on the spatial resolution of the grid." (abstract)
- Threshold catchment A_c: channel sites are those with A >= A_c. Rescaling uses an area A_e = alpha * A_c^beta (Eq. 14), with beta in [0.41, 0.46] from the simulated networks (Eq. 13: P(A) ~ A^-beta). Same PDF.
- Dimensional form (Eq. 15), DERIVED from the text: E = alpha * (A_c/delta^2)^beta * K * A^m * S^n. For beta = 0.5 this scales as 1/delta.
- Practical form (Eq. 16): E = (sqrt(2 A_c) / delta) * K * A^m * S^n, with A_c in DEM pixels and delta the grid spacing. The author takes alpha = sqrt(2) as "a reasonable estimate" for A_c of a few to 100 pixels at about 100 m resolution. Same PDF.
- Limitation: "In combination with such processes, e.g., diffusion, the dependence on the spatial resolution is not completely removed." Same PDF, Conclusions.
- Breakdown of Flint's law: "reported at catchment sizes between about 0.1 and 5 km2 (Montgomery and Foufoula-Georgiou, 1993; Stock and Dietrich, 2003; Wobus et al., 2006)". Same PDF.

### 3b. Kargere et al. 2025 (Earth Surf. Dynam. 13, 403-415): characteristic landscape length
Source: https://esurf.copernicus.org/articles/13/403/2025/esurf-13-403-2025.pdf (the Cardiff repository copy returned a Cloudflare challenge page, so I used the journal host).
- Abstract: "We derive the characteristic landscape length as the horizontal length in a one-dimensional landscape evolution framework required to form an inflection point. On a two-dimensional domain, channel heads form in steady state at the characteristic area, the square of the characteristic length, independent of grid resolution."
- Equation used: stream power term rescaled by sqrt(A)/delta: dz/dt = U - K (sqrt(A)/delta) |grad z|^n + D grad^2 z (their Eq. 7-8). The "specific drainage area" a = A/delta has length units, so K here has units yr^-1 and is NOT the same normalisation as K A^m with A in m^2 (their Eq. 8 in the text).
- Channel-head test: "nodes with A = (62 m)^2" for the Gabilan Mesa DEM; the characteristic length there is r = 62 m. Same PDF.
- Test parameter sets (figure captions, same PDF): (i) K = 2.5e-5 yr^-1, D = 7e-2 m^2/yr, U = 3.6e-3 m/yr, delta = 10 m; (ii) K = 5e-4 yr^-1, D = 5e-2 m^2/yr, U = 1e-3 m/yr; (iii) K = 2.5e-4 yr^-1, delta = 2 m, boundary length 100 m. The caption gives the channelization index as CI = l^2 K / D, with CI about 22, 89 and 357 in one set.
- Not captured: the closed-form expression for r in terms of K and D was not reliably extracted from the PDF text. UNVERIFIED beyond "r is defined from the 1D inflection point of the linear-diffusion plus stream power solution".
- Practical implication (DERIVED): the channel head area is A_head about r^2 with r set by K and D (not by the grid), so a model's threshold A_c should be tied to r, not chosen arbitrarily. The paper says that "computational models often implement a physically derived or arbitrarily chosen threshold for drainage area" (introduction).

### 3c. Other resolution-related statements
- Hergarten 2020 Sect. 2: relief depends on spatial resolution for the simple stream power model without local transport; river steepness is resolution-independent only in that case. Same PDF.

## 4. Area exponent m, slope exponent n, and concavity theta = m/n

- Energetic justification: Lague 2014 says the SPIM can be derived "from simple energetic considerations (i.e., as the unit rate of energy expenditure on the channel bed and banks yielding m = 0.5 and n = 1)". Source: Lague 2014 PDF (above).
- Lague 2014: "the downstream decrease of channel slope with drainage area often observed in nature is well reproduced if m/n ~ 0.5 and U = I." Same PDF.
- Steady-state concavity: "a range of 0.4 to 0.6 is often reported (e.g. Kirby and Whipple, 2012; Whipple, 2004)." "A reference concavity exponent of theta = 0.45 is now routinely used to compare channel profiles and individual reaches from different locations (Whipple, 2004; Whipple et al., 2013; Wobus et al., 2006a)." Same PDF.
- Lague 2014: theta "does not vary with uplift rate or lithology in a statistically significant way" in single-factor studies (Duvall et al. 2004; Kirby and Whipple 2001; Lague et al. 2000; Ramsey et al. 2006; Snyder et al. 2000). Same PDF.
- Whipple 2004 review: "Low concavities (<0.4) are associated either with short, steep drainages importantly influenced by debris flows ... or with downstream increases in either incision rate or rock strength ... Moderate concavities (0.4-0.7) are associated with actively uplifting bedrock channels in homogeneous substrates". Source: https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/Whipple_2004_AnnRevEPS.pdf
- Mudd et al. 2018 (ESurf 6, 505-523): "Patterns of the concavity index have been linked to the ratio of the area and slope exponents of the stream power incision model (m/n)". They warn that using a single reference concavity where it varies can give "spurious patterns in ksn" and that "selecting the correct concavity index is crucial". They also say chi-based theta values "are predicted to be relatively low, typically 0.1-0.6" in their landscapes. Source: https://esurf.copernicus.org/articles/6/505/2018/esurf-6-505-2018.pdf. Their simulations test m/n = 0.35, 0.5 and 0.65 with n = 1, and also n = 2, 1.5 and 0.66 at m/n = 0.5.
- Cordonnier 2016 uses m = 0.5, n = 1 (m/n = 0.5) "as in most geomorphological studies", citing Whipple and Tucker 1999 for m/n ~ 0.5. Source: https://www.cs.purdue.edu/homes/bbenes/papers/Cordonier16CGF.pdf
- Braun 2022 uses m = 0.4, n = 1 in its example (m/n = 0.4), and states that "the concavity of river channels implies that m/n ~ 0.5". Source: https://esurf.copernicus.org/articles/10/301/2022/esurf-10-301-2022.pdf
- Harel et al. 2016 (global 10Be analysis, Geomorphology 268, 184-196): N = 1457 basin erosion rates, 59 areas, using the integral method. Reported: "the slope exponent is generally > 1, meaning that the relationship between erosion rate and the channel gradient is nonlinear ... questions the validity of many regional interpretations ... where the unity of n is routinely assumed." Also normalised K and n to m/n = 0.5. Source (abstract read via the Edinburgh portal): https://www.research.ed.ac.uk/en/publications/global-analysis-of-the-stream-power-law-parameters-based-on-world/. Full text not read (Sect. 9). Sample counts differ between conference and paper versions in search summaries; I use the published abstract numbers.
- Threshold and discharge variability (Lague 2014): effective exponents in the threshold-stochastic model are "1.4 and 2.2 for high discharge variability (k = 0.5 ...) and 2.8 and 4.7 for very low discharge variability (k = 2 ...)" (assumptions c ~ 1, b ~ 0.3). Same PDF. Use this to justify n > 1 only if the tool is meant to represent threshold behaviour.
- Lague 2014 on n: "the river obey a non-linear SPIM (n>1)" in threshold-dominated knickzones (abstract). Same PDF.

## 5. Steady state, relief and h_max

### 5a. Steady-state channel slope (DERIVED from the stream power law)
- Lague 2014 Eq. 2 with dh/dt = 0 and U = I gives S^n = U / (K A^m), so S = (U/K)^(1/n) A^(-m/n). This matches Cordonnier's steady-state statement "s ~ A^(-m/n)" (Cordonnier 2016 PDF, Sect. 4).
- Worked check (DERIVED, arithmetic): with U = 5e-4 m/yr and K = 5.61e-7 yr^-1, n = 1, m = 0.5: at A = 1e8 m^2 (100 km^2), S = U/(K A^0.5) = 5e-4/(5.61e-7 * 1e4) = 0.089 (about 5 deg). At A = 1e6 m^2, S = 0.89 (about 42 deg), so small catchments with this K need the thermal limit or they will be unrealistically steep.

### 5b. Relief scaling and Cordonnier's empirical h_max
- Cordonnier 2016 (Sect. 6.4): "The erosion parameters ... are not intuitive to set ... The erosion coefficient k and the uplift u are both subject to a multiplication by dt, so only their ratio is relevant. ... It turned out this relation is linear and the height in kilometers follows the rule hmax = 2.244 u/k." Source: https://www.cs.purdue.edu/homes/bbenes/papers/Cordonier16CGF.pdf
- Check (DERIVED): u/k = (5.0e-4 m/yr) / (5.61e-7 yr^-1) = 891 m; 2.244 * 891 = 2000 m, matching the stated "about 2 000 m". The numbers are consistent if h and u/k are in the same length unit; the paper's "kilometers" label is consistent only if u is in km/Myr and k in Myr^-1 (equivalent). So the constant 2.244 is dimensionless and applies to that model's geometry, grid, time step and boundary conditions; it is not a general law.
- DERIVED general form: for the steady-state slope above, relief along a channel of length L scales as h ~ (U/K)^(1/n) * integral of A^(-m/n) dx. For n = 1 this is linear in U/K (as Cordonnier found), but for n = 2 it scales as (U/K)^(1/2). So the exponent n changes the dependence of relief on U/K strongly, and the Cordonnier linear fit cannot be carried over to n != 1.
- Whipple and Tucker 1999 (JGR 104, 17661-17674; DOI 10.1029/1999JB900120) is the source for the "height limits of mountain ranges" argument and the "uplift-erosion number". I could not read the full text (Sect. 9); the abstract as quoted in search summaries says the dynamic behaviour is controlled by "a single nondimensional group" and that n is a fundamental unknown. The exact form of the group is UNVERIFIED.

### 5c. Response time and knickpoint celerity
- Lague 2014 (n = 1): "the detachment-limited SPIM (Equation 2) is an advection equation predicting the parallel retreat of KPs at a celerity depending on erodibility and drainage area ... (with C = K and p = m, e.g. Rosenbloom and Anderson, 1994; Whipple and Tucker, 1999)." So V = K A^m (m/yr). Source: Lague 2014 PDF.
- Lague 2014: "Because m/n ~ 0.5, p and epsilon should be close to 0.5. This is roughly consistent with most field data but the data for hanging valleys in the Alps (epsilon = 0.8, Valla et al., 2010), the dataset on Scottish rivers by (epsilon = 1.26, Bishop et al., 2005) and the Waipaoa waterfalls (p = 1.12, Crosby and Whipple, 2006) ... would be more consistent with n ~ 2." Same PDF.
- DERIVED response timescale (n = 1): time to cross a reach of length L at celerity V is T = L/(K A^m). Example: L = 50 km, A = 1e8 m^2, K = 5.61e-7 yr^-1: K A^m = 5.6e-3 m/yr, so T = 5e4 m / 5.6e-3 m/yr = 9e6 yr. The result is sensitive to K and to A, so a scalar response time is only indicative. This is DERIVED arithmetic from the cited celerity; it is not a published Whipple and Tucker formula.
- Whipple 2004 review: "the rate at which these signals are conveyed sets, to first order, the timescale of landscape response to perturbation (Whipple & Tucker 1999, Whipple 2001)". Source: https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/Whipple_2004_AnnRevEPS.pdf
- Search-summary only (UNVERIFIED): Whipple 2001 gives response times of about 0.25 to 2.5 Ma depending on the nonlinearity and perturbation.

## 6. Hillslope diffusion: coefficient ranges and climate dependence

### 6a. Ranges (secondary compilation, read from MIT OCW lecture notes by K. Whipple, 12.163, Sept 2004)
Source: https://ocw.mit.edu/courses/12-163-surface-processes-and-landscape-evolution-fall-2004/02cdc0e225e5d9015ff07c2bf4a2cc65_8_hillslope_evolution.pdf
- "Scarp studies (southwestern US: semi-arid; granular soils; sparse vegetation) generally find: 10^-3 < Kc < 10^-2 m^2/yr."
- "Dietrich et al. in humid/temperate N. California and Oregon coastal mountains (moist winter conditions, dense vegetation) find: Kc ~ 5 x 10^-3 m^2/yr."
- "Small et al. (Geomorphology, 1999) on frost-dominated, unvegetated summit flats eroding at rates of ~15 um/yr estimate Kc ~ 1.7 x 10^-2 m^2/yr."
- Soil linear diffusivity used by a cosmogenic/soil production study: K = 50 cm^2/yr = 5e-3 m^2/yr (same notes; study not named in the text I read).
- Search summaries (UNVERIFIED, not read): Avouac (1993) gives 1-6 m^2/kyr (0.001-0.006 m^2/yr) for Holocene scarps in arid alluvium; Hanks et al. (1984) reports kappa = 1.1 to 11 m^2/ka for some coastal and shoreline scarps.
- Hanks (2000) (USGS record https://www.usgs.gov/publications/age-scarplike-landforms-diffusion-equation-analysis): the review of kappa values exists, but the full text was not reachable. Its tabulated values are UNVERIFIED.

### 6b. Calibrated values from one field study (Roering et al. 1999, WRR 35, 853-870)
Source: https://typeset.io/pdf/evidence-for-nonlinear-diffusive-sediment-transport-on-532j2v7c1n.pdf (third-party copy of the WRR paper; the AGU DOI page was not fetched).
- Calibration by divergence of sediment flux: K = 0.0032 +/- 0.0009 m^2/yr and S_c = 1.25 +/- 0.10 (one basin, MR1). Five-basin average: K = 0.0036 +/- 0.0016 m^2/yr and S_c = 1.27 +/- 0.16 (range S_c 1.2-1.35). Area-slope method: K between 0.0015 and 0.0045 m^2/yr and S_c between 1.0 and 1.4.
- Transport law: "sediment flux increases rapidly as gradient approaches a critical value." Their Sc is "generally equated with the angle of repose".
- Tectonic context in the same paper: rock uplift rates 0.03-0.23 mm/yr; erosion rate and soil production 0.1 +/- 0.03 mm/yr.
- Note: the paper's example run uses K = 0.003 m^2/yr, constant erosion rate C0 = 0.075 mm/yr, and S_c = 1.2 for the nonlinear hillslope.

### 6c. Fernandes and Dietrich 1997 and Hanks 2000
- Fernandes and Dietrich (1997) (WRR) and Hanks (2000) were not read in full. The Fernandes and Dietrich PDF link I tried returned a TLS certificate error (see Sect. 9). No coefficient values from them are used here.

### 6d. Model defaults (see Sect. 8)
- Landlab LinearDiffuser default linear_diffusivity = 0.01 (m^2 per time unit).
- gOSPL example config: hillslopeKa = 0.02 (aerial), hillslopeKm = 0.2 (marine) m^2/yr.

## 7. Critical slope, non-linear diffusion and thermal limits

- Roering et al. 1999: the transport law is linear at low gradient and flux diverges at S_c. Calibrated S_c = 1.25 (tan of angle). Source: Sect. 6b above.
- DERIVED: tan(angle) = S_c, so S_c = 1.25 corresponds to atan(1.25) = 51.3 deg; the 1.2-1.35 range gives 50.2-53.5 deg. Cordonnier's 30 deg (tan = 0.577) is a limit on the stream power result, not the same quantity.
- Cordonnier 2016 (Sect. 5): "if the result of the stream power equation leads to slopes higher than 30 deg, we reduce the change of elevation so as to keep slopes in the prescribed range." They cite Musgrave, Kelley and Malin (MKM89) for 30 deg as "the usual talus angle for thermal erosion". Source: https://www.cs.purdue.edu/homes/bbenes/papers/Cordonier16CGF.pdf. Cordonnier also notes that with a uniform 30 deg limit the valleys become "very regular geometric valleys", and that a varying limit (6 deg to 54 deg in their test) gives more random erosion patterns (Sect. 6, Fig. 17-18).
- Whipple 2004 lecture notes: scarp angle "usually the angle of repose, ca. 33 deg" for scarp diffusion analysis. Same OCW source.

## 8. Software defaults and example parameters (read from docs; versions not pinned)

- Fastscapelib, River Profile example (Python), https://fastscapelib.readthedocs.io/en/latest/examples/river_profile_py.html:
  - ProfileGrid 101 nodes, spacing 300 m; fixed-value base level on the left, core on the right.
  - SPLEroder: k_coef = 1e-4, area_exp = 0.5, slope_exp = 1, tolerance = 1e-5.
  - Uplift 1e-3 (per time unit; the page does not state the unit, most likely m/yr with time in years).
  - Hack's law area: A = 6.69 x^1.67. dt = 1e2, nsteps = 4000; at step 3000, k_coef is divided by 4 to simulate an erodibility change.
  - The page describes the erosion law as "uniform in space and time" parameters.
- Landlab FastscapeEroder, https://landlab.readthedocs.io/en/latest/generated/api/landlab.components.stream_power.fastscape_stream_power.html:
  - "This class uses the Braun-Willett Fastscape approach ... Braun-Willett (2013) implicit Fastscape algorithm."
  - Defaults: K_sp = 0.001, m_sp = 0.5, n_sp = 1.0, threshold_sp = 0.0, discharge_field = 'drainage_area'. Docs state "Erodibility (units depend on m_sp)".
- Landlab LinearDiffuser (diffusion component), https://landlab.readthedocs.io/en/latest/generated/api/landlab.components.diffusion.diffusion.html: __init__(grid, linear_diffusivity=0.01, method='simple', deposit=True); diffusivity in m^2 per time unit.
- gOSPL surface processes, https://gospl.readthedocs.io/en/dev/user_guide/surfproc.html:
  - SPL form E = K (P A)^m S^n; default m = 0.5, n = 1.0.
  - Optional rainfall-dependent erodibility (Murphy et al. 2016): E = (K_i P^d)(P A)^m S^n with d up to 0.42; default d = 0.0.
  - G = deposition coefficient (Yuan et al. 2019), default 0.0 (purely detachment-limited).
  - Diffusion example values: hillslopeKa 0.02, hillslopeKm 0.2, nonlinKm 500, clinSlp 5e-5 (example YAML block).
  - Lithology/fine-sediment contrast option: fine.k_factor (default 1.0, no contrast).
- Fastscapelib kernel eroder example (https://fastscapelib.readthedocs.io/en/latest/examples/kernel_eroder_py.html) was fetched but not read in full.

## 9. Deposition and sediment terms (Davy and Lague 2009; Yuan et al. 2019; Braun 2022)

- Davy and Lague 2009 (JGR Earth Surface 114, F03007; DOI 10.1029/2008JF001146): adds a streamflow mass-balance term; the central object is the sediment-transport length function xi(q) (unit-width discharge q and slope). The model reduces to transport-limited or detachment-limited erosion depending on xi. Source (abstract via search result, https://zendy.io/title/10.1029/2008jf001146). The full PDF (HAL) returned a bot challenge page and was not read.
- Yuan et al. 2019 (JGR Earth Surface 124, 1346-1365; DOI 10.1029/2018JF004867): an efficient implicit O(N) method for the Davy and Lague equation with deposition; search summary (UNVERIFIED) says it is unconditionally stable for large time steps; the sentence was truncated in the summary. Source: ADS record https://ui.adsabs.harvard.edu/abs/2019JGRF..124.1346Y (abstract only). The HAL copy returned HTML, not PDF.
- Braun 2022 (ESurf 10, 301-327) compares transport-limited and xi-q models. Example parameters from the caption: K_f = 1e-5 m^(1-2m) yr^-1 (m = 0.4); G = 1 yr/m; K_d = 1e-5 m^-1 yr^-1 (as printed "m^-2 m yr^-1"); w = 1e4 m; n = 1; L = 100 km; A_0 = 1e8 m^2; k = 0.6; p = 2; q_0 = 10 m/yr. Source: https://esurf.copernicus.org/articles/10/301/2022/esurf-10-301-2022.pdf
- Interpretation (DERIVED): G makes the deposition term dimensionless relative to erosion. G = 0 (gOSPL default) gives pure detachment-limited incision.

## 10. Rock strength and lithology

- Sklar and Dietrich 2001 (Geology, abstract): "rock resistance to fluvial erosion scales with the square of rock tensile strength." Also: "Maximum erosion rates occur at a critical level of coarse-grained sediment supply where the bedrock is only partially exposed. Fine-grained sediments provide poor abrasive tools." Source: https://typeset.io/pdf/sediment-and-rock-strength-controls-on-river-incision-into-21g3zfozyk.pdf (third-party copy; text matches the Geology letter per the search record).
- Anderson, Gasparini and Johnson (2023, ESurf 11, 995-1011; preprint at https://egusphere.copernicus.org/preprints/2022/egusphere-2022-1285/egusphere-2022-1285-manuscript-version3.pdf): "bedrock incision rate should scale inversely with rock tensile strength (Sklar and Dietrich, 2001; ...)". They used Schmidt hammer rebound values and discontinuity intensity as rock-strength proxies. Relevant as a recent example of field strength proxies.
- Moore, Sanders, Dietrich and Glaser (2009, ESPL 34, 1339-1352; DOI 10.1002/esp.1821), search-summary only (UNVERIFIED, full text not read): alpine rockwall recession rates 0.02-1.22 mm/yr (mean 0.28 mm/yr) for 40 cliffs in the Sierra Nevada, best described by an exponential decrease with the Slope Mass Rating (SMR); joint orientation is the most important SMR component.
- Lithology erodibility ratios: the only quantitative ratios I could verify are Lague 2014's instantaneous erodibility k_e within one order of magnitude across three sites with different runoff (see Sect. 11). The Stock and Montgomery ratios are UNVERIFIED (Sect. 2). gOSPL's fine.k_factor (default 1.0) is a user-set contrast with no published default.

## 11. Lague 2014 threshold and instantaneous erodibility (for the K calibration discussion)
- Instantaneous bed erodibility k_e in the threshold-stochastic model: about 7e13 (Liwu River), 2.4e12 (San Gabriel Mountains, SGM) and 2.4e13 (Rio Torto, Deff = 5 cm), in m^(5/2) s^2 kg^(-3/2) (a = 3/2). Lague 2014 says these values "are within one-order of magnitude between these three sites" despite an order-of-magnitude difference in incision rate (0.24 m/yr SGM vs 2.4 m/yr Liwu). Source: Lague 2014 PDF.
- Steepness vs incision (Lague 2014, Fig. 1 compilation): ksn ~20 to 500 m^0.9 for incision 0.02 to 14 mm/yr ("nearly three orders of magnitude change in incision rates"). Source: Lague 2014 PDF.

## 12. Disagreements and ranges (summary)

1. n: Harel et al. 2016 (global 10Be) find n generally > 1; Cordonnier, Fastscapelib and Landlab defaults use n = 1; Lague 2014 notes n ~ 2 for some datasets (Valla 2010; Bishop 2005) and threshold models give n > 1. Using n = 1 is a choice, not a finding.
2. m: default 0.5 is energetic/theoretical; Braun 2022 example uses m = 0.4; Mudd 2018 tests 0.35-0.65 at fixed m/n. The steepness and concavity results depend on the m/n ratio, and a single reference (0.45) is conventional.
3. theta: range 0.4-0.6 (Kirby and Whipple 2012, as cited by Lague 2014 and Mudd 2018); Mudd 2018 chi-based values 0.1-0.6 in their field catchments; Whipple 2004: <0.4 near knickpoints, 0.4-0.7 for uniform uplifting bedrock.
4. K: units and magnitude depend on m, normalisation (A in m^2 vs sqrt(A)/delta), and time unit. Values in the repo should not be compared without this conversion. Hergarten 2020 and Kargere 2025 show that K itself depends on grid spacing if the stream power term is not rescaled.
5. Diffusivity: field values range from about 1e-3 to 2e-2 m^2/yr (Whipple 2004 compilation); Roering 1999 gives 0.0015-0.0045 m^2/yr for one site; Landlab default 0.01; gOSPL example 0.02.
6. h_max: Cordonnier's linear rule (2.244 u/k) is calibrated to their n = 1, m = 0.5 model; for n != 1 the dependence changes (Sect. 5b).
7. Sediment deposition: Davy and Lague 2009 include deposition, while the simple SPL (Cordonnier, Fastscapelib, Landlab, gOSPL default G = 0) does not; Hergarten 2020 says the grid-scaling problem reappears when diffusion is added.

## 13. Notes on the brief's specific items

- Harel et al. 2016 "K vs precipitation": the published abstract says the expected local correlation between K and precipitation does NOT appear at global scale. So K cannot be set from climate alone without a regional calibration.
- Gailleton et al. 2019: the paper I found (ESurf 7, 211-230) is "A segmentation approach for the reproducible extraction and quantification of knickpoints from river long profiles" (knickpoint detection), NOT Bayesian erodibility estimation. The brief's description does not match. A Gailleton et al. 2024 Bayesian erodibility paper was not found.
- Esurf 2025 "characteristic length": the paper is Kargere, Constantine, Hales, Grieve and Johnson (2025). Its r is defined from the 1D inflection point and its channel-head area is r^2 (Sect. 3b).
- Kirby and Whipple 2012 full text was not reached; the 0.4-0.6 range is taken from Lague 2014 and Mudd 2018 quotations.
- Whipple et al. 2013 (cited for 0.45 by Lague) was not read; the reference details are from Lague's bibliography only.

## 14. Failed or blocked fetches (not bypassed)

1. https://doi.org/10.1029/98JB02139 (Stock and Montgomery 1999): JavaScript and cookie wall ("Enable JavaScript and cookies to continue").
2. https://planetarygeoscience.uchicago.edu/doc/Whipple_and_Tucker_1999.pdf (Whipple and Tucker 1999): TLS certificate verification failed ("unable to get local issuer certificate"). Not bypassed.
3. https://core.ac.uk/download/158138808.pdf (Harel et al. 2016 preprint): bot-check page ("Just a moment..."). Not bypassed. Abstract used from the Edinburgh portal instead.
4. https://hal-insu.archives-ouvertes.fr/insu-00424874/file/davy-JGR-2009.pdf and https://hal.science/insu-00424874/document (Davy and Lague 2009): bot-check page ("Making sure you're not a bot!"). Not bypassed.
5. https://orca.cardiff.ac.uk/id/eprint/179682/1/esurf-13-403-2025.pdf (Kargere et al. 2025 repository copy): Cloudflare challenge. The journal host (esurf.copernicus.org) was used instead.
6. https://efi.eng.uci.edu/papers/efg_092.pdf (listed as a diffusion paper in search results): TLS self-signed certificate chain error. Not bypassed.
7. https://par.nsf.gov/servlets/purl/10471890 (returned as "Stock and Montgomery"): wrong paper (Anderson et al. 2023). Not used.
8. https://hal-univ-tlse3.archives-ouvertes.fr/hal-02136641/document (Yuan et al. 2019): returned HTML, not a PDF. Not read.
9. Hanks (2000) chapter: no full text reachable (USGS record only).
10. Kirby and Whipple (2012) J. Struct. Geol.: not found in search; no full text.
11. Gailleton et al. 2024 (Bayesian erodibility): not found.

## 15. URLs read (full text or abstract)

Full text read (PDF or HTML converted):
- https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2014_Lague_ESPL.pdf (Lague 2014 review)
- https://esurf.copernicus.org/articles/8/367/2020/esurf-8-367-2020.pdf (Hergarten 2020)
- https://www.cs.purdue.edu/homes/bbenes/papers/Cordonier16CGF.pdf (Cordonnier et al. 2016)
- https://esurf.copernicus.org/articles/6/505/2018/esurf-6-505-2018.pdf (Mudd et al. 2018)
- https://esurf.copernicus.org/articles/13/403/2025/esurf-13-403-2025.pdf (Kargere et al. 2025)
- https://esurf.copernicus.org/articles/10/301/2022/esurf-10-301-2022.pdf (Braun 2022)
- https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/Whipple_2004_AnnRevEPS.pdf (Whipple 2004 review)
- https://ocw.mit.edu/courses/12-163-surface-processes-and-landscape-evolution-fall-2004/02cdc0e225e5d9015ff07c2bf4a2cc65_8_hillslope_evolution.pdf (Whipple 2004 lecture notes, hillslope diffusion)
- https://typeset.io/pdf/evidence-for-nonlinear-diffusive-sediment-transport-on-532j2v7c1n.pdf (Roering et al. 1999, third-party copy)
- https://typeset.io/pdf/sediment-and-rock-strength-controls-on-river-incision-into-21g3zfozyk.pdf (Sklar and Dietrich 2001, third-party copy)
- https://egusphere.copernicus.org/preprints/2022/egusphere-2022-1285/egusphere-2022-1285-manuscript-version3.pdf (Anderson et al., preprint; partly read)
- https://fastscapelib.readthedocs.io/en/latest/examples/river_profile_py.html (Fastscapelib example)
- https://landlab.readthedocs.io/en/latest/generated/api/landlab.components.stream_power.fastscape_stream_power.html (Landlab FastscapeEroder)
- https://landlab.readthedocs.io/en/latest/generated/api/landlab.components.diffusion.diffusion.html (Landlab LinearDiffuser)
- https://gospl.readthedocs.io/en/dev/user_guide/surfproc.html (gOSPL)

Abstract or summary read (not full text):
- https://www.research.ed.ac.uk/en/publications/global-analysis-of-the-stream-power-law-parameters-based-on-world/ (Harel et al. 2016 abstract)
- https://zendy.io/title/10.1029/2008jf001146 (Davy and Lague 2009 abstract, search result)
- https://ui.adsabs.harvard.edu/abs/2019JGRF..124.1346Y (Yuan et al. 2019 abstract, search result)
- https://earthref.org/ERR/42355 (Stock and Montgomery 1999 record, search result only; not opened)
- https://www.usgs.gov/publications/age-scarplike-landforms-diffusion-equation-analysis (Hanks 2000 record)

Fetched but not read in full: https://fastscapelib.readthedocs.io/en/latest/examples/kernel_eroder_py.html; https://esurf.copernicus.org/articles/14/247/2026/esurf-14-247-2026.pdf was seen in search results only.

## 16. Key takeaways for the tool

1. Default exponents: m = 0.5, n = 1 (the setting used by Cordonnier 2016, Landlab and Fastscapelib defaults, and Lague 2014's energy argument). Treat n = 1 as a choice that Harel et al. 2016 contest (n generally > 1 globally). Make n a parameter and test n = 1 and n = 1.5 to 2 for sensitivity.
2. Concavity: target m/n = 0.45 (range 0.4-0.6) for steepness normalisation. The steady-state profile depends only on the ratio m/n for uniform uplift and erodibility (Lague 2014; Cordonnier 2016 states "only the ratio between m and n has a meaning"), so fit or set the ratio, not m and n separately.
3. K units: state them. With A in m^2 and E in m/yr, K has units yr^-1 m^(1-2m). For m = 0.5, K in yr^-1. Cordonnier's K = 5.61e-7 yr^-1 gives a 2 km high belt at U = 0.5 mm/yr (DERIVED check: h = 2.244 U/K = 2000 m). Other K values in the literature are for different normalisations (Esurf 2025 uses sqrt(A)/delta; Fastscapelib and Landlab examples use 1e-4 and 1e-3 with unstated or different time units). Do not mix them.
4. Grid resolution: if the tool uses a fixed grid spacing and a stream power term without rescaling, the relief depends on delta (Hergarten 2020). Use the rescaling E = (sqrt(2 A_c)/delta) K A^m S^n (Hergarten 2020 Eq. 16) with A_c tied to the characteristic area r^2 (Kargere et al. 2025) rather than an arbitrary threshold; document A_c. With diffusion added the dependence is not fully removed (Hergarten 2020).
5. Hillslope diffusion: use D = 1e-3 to 1e-2 m^2/yr as the physical range (climate dependent: about 5e-3 in humid Oregon/N. California; scarp values in semi-arid SW US 1e-3 to 1e-2; frost-dominated summit flats 1.7e-2; Roering et al. 1999 calibrated 3.2e-3 m^2/yr in the Oregon Coast Range). Landlab's default 0.01 is inside the range.
6. Nonlinear diffusion: if slope limiting is wanted physically, use S_c = 1.25 (tan of angle, about 51 deg) from Roering et al. 1999. The 30 deg talus limit of Cordonnier 2016 is a cruder thermal cap for stream-power output and is a different quantity; state which one is used.
7. Steady state and h_max: the steady-state slope is S = (U/K)^(1/n) A^(-m/n). For n = 1, relief scales linearly with U/K (Cordonnier's h_max = 2.244 U/K, dimensionless constant tied to their model). For n != 1 the scaling is not linear, so do not use the Cordonnier constant for n != 1.
8. Response time: for n = 1 the knickpoint celerity is K A^m (Lague 2014). A reach-length time L/(K A^m) is a useful estimate (DERIVED); the published Whipple and Tucker (1999) formula could not be checked (Sect. 14), so label it as an estimate.
9. Mountain ages: different ages can be tested with time-dependent U(t) and by starting from a flat or low-relief initial surface. The fluvial response time (point 8, about 9e6 yr for a 50 km reach at K = 5.61e-7 yr^-1, A = 1e8 m^2) and the diffusive timescale h^2/D (DERIVED: for a 1 km hillslope with D = 5e-3 m^2/yr, about 2e8 yr; for the full 50 km belt, L^2/D = 5e11 yr, so hillslope diffusion alone does not equilibrate a belt at that scale) should both be computed and compared with the age range.
10. Sediment deposition: keep the deposition coefficient G = 0 (detachment-limited) unless the tool is meant to include Davy and Lague 2009 or Yuan et al. 2019 physics. If included, use the Braun 2022 example order of magnitude (G = 1 yr/m) only as a starting point, UNVERIFIED for mountain belts.
11. Rock strength: incision scales inversely with tensile strength (Sklar and Dietrich 2001); a lithology map can set K as K_rock = K_ref * (sigma_ref/sigma_t)^2 only as a qualitative rule (the proportionality constant is not calibrated here). Stock and Montgomery's lithology ranges (about 1e-7 to 1e-2 m^0.2/yr for m = 0.4) are UNVERIFIED and should be checked against the full paper before use.
12. Verify before publication: the Stock and Montgomery 1999 lithology table, the Whipple and Tucker 1999 response time and height-limit group, the Harel et al. 2016 K table, Davy and Lague 2009 equations, and Hanks 2000 values. These could not be read because of access blocks.
