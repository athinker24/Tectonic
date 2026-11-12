# B: Sea-level curves, plate/basin-driven sea-level rates, dynamic topography, shoreline computation, rotation interpolation, numerical stability

Status: DONE. Scope: 5 topics. Tam metinler: Miller 2020 (Europe PMC), Shoemake 1985 (PDF). Gerisi özet/arama özeti. Erişilemeyen kaynaklar aşağıda işaretli.

Legend: [B] full text read | [B-öz] summary read | [Ö] search snippet only | ERİŞİLEMEDİ = could not access | BULUNAMADI = not found

## 1. Long-term (Phanerozoic) sea-level curves and rates

- Haq, Hardenbol, Vail 1987 (Science 235:1156-1167, "Chronology of Fluctuating Sea Levels Since the Triassic"): [B-öz] Crossref abstract (https://api.crossref.org/works/10.1126/science.235.4793.1156). Covers past 250 Myr with cycle charts for Cenozoic, Cretaceous, Jurassic, Triassic. Full PDF at https://mantleplumes.awh.durham.ac.uk/WebDocuments/Haq1987.pdf: ERİŞİLEMEDİ (TLS: "unable to get local issuer certificate"; not bypassed). Amplitude numbers from the PDF: NOT VERIFIED. Miller 2020 (above) says EPR-derived amplitudes such as the 160 m middle Oligocene event are "too high by a factor of 2 to 3" [B, Miller 2020 intro].
- Miller et al. 2005 (Science 310:1293): PENDING
- Miller et al. 2020 (Science Advances 6:eaaz1346, "Cenozoic sea-level and cryospheric evolution from deep-sea geochemical and continental margin records"): [B] Europe PMC full text (PMC7228749, https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7228749/fullTextXML). Findings:
  - GMSL estimate for 66 Ma from Pacific benthic foraminiferal d18O and Mg/Ca; "statistically similar" to backstripped continental margin estimates (abstract).
  - Hothouse (Early Eocene, 56 to 47.8 Ma): ice-free; ice-free line drawn at +66 m above present (Fig. 1C caption).
  - Eocene GMSL 40 to 50 m above present, near or below modern levels in the Oligocene (text, "Amplitudes of sea-level change").
  - Long-term trend: sea level declined from average 28 +/- 6.8 m (42 to 40 Ma) to -0.5 +/- 2.7 m (12 to 10 Ma); shared linear trend = decrease of 1.0 +/- 0.5 m/Ma (text, backstripped comparison). Note: this is a Cenozoic icehouse-driven decline, not a plate-driven rate.
  - Ice-sheet changes: 10 to 30 m (Cool Greenhouse 48 to 34 Ma), >50 m (Icehouse from ~34 Ma) (abstract).
  - Authors state ocean basin volume effects operate "primarily on >1-Ma scale" (intro).
  - Also: Miller 2020 says EPR (Exxon) curves have "extremely high sea-level amplitudes (e.g., 160-m middle Oligocene event)" that are "too high by a factor of 2 to 3" (intro, citing Miller 2005 / refs 4,17).
- Miller et al. 2005 (Science 310:1293-1298, "The Phanerozoic Record of Global Sea-Level Change"): [B-öz] Crossref abstract (https://api.crossref.org/works/10.1126/science.1116412). Quote: "Long-term sea level peaked at 100 +/- 50 meters during the Cretaceous, implying that ocean-crust production rates were much lower than previously inferred." Also: sea level mirrors oxygen isotope (ice-volume) variations on 10^4 to 10^6 yr scale; 10^7-yr link attributed to temperature/CO2. Full text not fetched.
- Müller et al. 2008 (Science 319:1357, ocean basin dynamics): PENDING
- Kominz et al. 2008 (basin volume / sea-level estimate): PENDING
- Peak values (summary of the above): Late Cretaceous high estimates range roughly +40 to +250 m (Müller 2008 intro); Miller 2005 +100 +/- 50 m; Müller 2008 +170 (85 to 270) m; Kominz 2008 +75 to +110 m (Late Cretaceous), +150 m (Early Eocene). The +100 to +250 m range in the task is consistent with the Müller/Miller bounds; the "+250" is the upper end of the Müller estimate range, not a measured peak. Haq 2014 ("Cretaceous eustasy revisited", [Ö] search snippet): Turonian peak ~240 to 250 m above PDMSL; this is a later recalibration, NOT the 1987 Haq chart value (1987 chart amplitude: NOT VERIFIED, PDF unavailable).
- Rate (m/Myr) from basin volume / tectonics: NOT FOUND as an explicit peak rate. Found:
  - Miller 2020: long-term Cenozoic decrease 1.0 +/- 0.5 m/Ma [B].
  - Wright, Seton et al. 2020 (Earth-Science Reviews; EarthByte page https://www.earthbyte.org/?p=7658, abstract [B-öz]): "sea level driven by fluctuating ocean basin volume has changed by ~200 m since the Jurassic"; authors say revised estimates "will need to be combined with other processes ... including mantle convection-driven dynamic topography and glacio-eustasy". Exact ESR DOI not verified (a DOI guess returned an unrelated paper; do not cite a DOI from this note). Rate per Myr not stated in abstract.
  - Miller et al. 2011 long-term changes "below 10 m/Myr" [Ö, search snippet only, not verified in primary text].
  - Implied average: 200 m over ~200 Myr (Jurassic to present) = ~1 m/Myr [derived, my arithmetic, not a source value].

## 2. Dynamic topography and sea level (Gurnis, Moucha, Müller)

- "Gurnis 2012, Nature Geoscience" as named in the task: [Ö] NOT FOUND. Search returned no such paper. Closest: Spasojević & Gurnis 2012, AAPG Bulletin (hybrid inverse-forward convection model; dominant control on global sea level is ocean-lithosphere production; dynamic topography offsets the fall). Snippet URL: https://earthbyte.org/Newsletter/Issue2/2012_SpasojevicGurnis_AAPG_Bull.pdf. Fetch returned an HTML page (not a PDF): ERİŞİLEMEDİ as PDF.
- Moucha et al. 2008 (EPSL 271:101-108, DOI 10.1016/j.epsl.2008.03.056, "Dynamic topography and long-term sea-level variations: There is no such thing as a stable continental platform"): [Ö] search snippet/secondary. Claims: ~100 m dynamic topography change over last 30 Myr at New Jersey and conjugate West African margin (mantle flow from seismic tomography); subduction-related downwelling contributes a background trend of similar magnitude; long-term sea level from "stable" sites cannot be read as purely eustatic. Full text not fetched.
- Flament, Gurnis, Müller 2013 (Lithosphere review): [Ö] dynamic topography means long-term global sea-level change "cannot be estimated at a single passive margin."
- Müller, Hassan, Gurnis, Flament, Williams 2018 (Gondwana Research): [Ö] best-fit convection models give up to 500 (+/-150) m total dynamic subsidence in continental interiors.
- Nature Geoscience "Global dynamic topography observations reveal limited influence of large-scale mantle flow" [Ö]: at ~10^4 km wavelengths observed dynamic topography peaks ~+/-500 m. Authors/year not confirmed from search; do not cite without checking.
- Müller 2008 (above): NJ subsidence 105 to 180 m attributed partly to dynamic topography over subducted Farallon plate [B-öz].

## 3. Shoreline from paleotopography + sea level; hypsometry (Cogley 1984)

- Cogley 1984 (Reviews of Geophysics 22(2):101-122, DOI 10.1029/RG022i002p00101, "Continental margins and the extent and number of the continents"): [Ö] Crossref/search abstract summary: 14 continents, ~41% of Earth's surface (210.4 x 10^6 km^2); mean continental crust thickness ~36 km; crustal volume 7.2 x 10^9 km^3; height and thickness strongly linked. Source: https://scilit.com/publications/1941408b5ac0b6ddf3524191917e8705. Full text not fetched. Hypsometry formula (area vs elevation) NOT VERIFIED in this session.
- Shoreline formula (paleotopography + sea level = shoreline): NOT VERIFIED as an explicit equation. Method as described in search snippets [Ö]:
  - Paleogeographic maps give flooded area of today's exposed land; a modern hypsometric curve A(h) converts flooded area to sea-level change, i.e. invert A(h) at the flooded area. A 2022 study (https://duo.uio.no/handle/10852/94891, [Ö]) built a 520 Myr eustatic curve this way, ~280 m above present near 80 Ma.
  - Sensitivity: larger or steeper continents flood less area per metre of rise; Palaeozoic maxima come out ~+200 to +400 m (https://searchworks.jioinstitute.edu.in/articles/edo__ejs4778666, [Ö]).
  - Relative vs absolute: water depth at a paleoshoreline gives relative sea level only; subsidence must be estimated separately (https://csdms.colorado.edu/pub/users/huttone/docs/flexure.tex.pdf, [Ö]). Paleoshoreline maps separate non-tectonic vertical motion (https://www.earthbyte.org/Resources/Pdf/HeineYeoMuller_GlobalPaleoshorelines_AJES_inpress.pdf, [Ö]).
  - Cogley 1984 hypsometry gives the present-day continental elevation distribution used for the curve (abstract only).
  - "Continental freeboard" as a named term: BULUNAMADI.
- Practical algorithm (for the task's pipeline; my synthesis, not a source): cell is land if paleo-elevation > sea level SL(t); shoreline = contour where elevation = SL(t); flooded area = sum of cell areas below SL(t) on the continental mask; invert hypsometric curve if using area-based inference. Keep ocean-floor cells out of the continental mask.

## 4. Animation frames: SLERP / Euler pole interpolation, GPlates interpolation, C1 continuity, step sizes

- Shoemake 1985 (Animating rotation with quaternion curves, SIGGRAPH '85, Computer Graphics 19(3):245-254): [B] full text from https://www.fd.cvut.cz/personal/voracsar/GeometriePG/PGR020/shoemake.pdf (pdftotext). Note: the PDF's author line reads "Ken Shoemaker"; other indexes spell "Shoemake".
  - Slerp formula (Sec. 3.3 area): Slerp(q1,q2;u) = [sin((1-u)theta)/sin theta] q1 + [sin(u theta)/sin theta] q2, with cos theta = q1.q2 (OCR of the PDF; the extracted text gives the form "Slerp(ql,q2;u) = sin((1-u)...)/sin ... ql + ..."; cos(theta) = q1.q2 is stated in the paper's text as "q1*q2 ~ cos theta").
  - Motivation (Sec. 3.2): "Straight lines between quaternions ... If our interpolated points were evenly spaced along a line, the animated rotation would speed up in the middle." Solution: "great circle arc" on unit sphere, "we can rotate without speeding up by interpolating on the sphere" (Sec. 3.3).
  - Continuity: "the direction of rotation changes abruptly ... we want higher order continuity." Spline joints: "As the curve goes through its end points it is tangent to its end segments. Line up the segments across a join, match their lengths" (tangent/first-order continuity, i.e. C1 on the sphere; exact wording partly garbled by OCR).
  - Result: constant-speed rotation along great circle = constant angular velocity when u is linear in time (inference: standard reading of Sec. 3.3; the paper says speed is constant on the sphere).
  - Exact step sizes for animation: not stated in the paper (inference).
- GPlates pygplates API [B-öz] https://www.gplates.org/docs/pygplates/generated/pygplates.FiniteRotation.html: `FiniteRotation.interpolate(finite_rotation1, finite_rotation2, time1, time2, target_time)` is a static method, "Calculate the finite rotation which is the interpolation of two finite rotations." A finite rotation is an Euler pole + angle (pole lat, lon, angle in degrees). The algorithm (slerp vs. Euler-pole/angle blend) is NOT stated in the doc: NOT VERIFIED.
- GPlates user manual, Total Reconstruction Sequences [B-öz] https://www.gplates.org/docs/user-manual/TotalReconstructionSequences: rotation files give one entry per time; an identical Euler rotation across consecutive rows means no relative motion in that interval. No interpolation algorithm or default step size found in fetched page.
- Example step sizes (1 / 5 / 10 Myr): NOT VERIFIED from a GPlates tutorial. Only a GUI frame-interval setting (Reconstruction > Configure Animation) was found [Ö]. The 1/5/10 Myr values are the task's assumption, not confirmed.
- Shoemake SLERP (above) is the standard quaternion/rotation-curve reference for C1-like smooth interpolation; pygplates' method not confirmed as SLERP.

## 5. Numerical stability of uplift/erosion vs time step (Fastscape, CFL-like condition)

- Fastscape/Landlab: FastscapeEroder docs (landlab.readthedocs.io) = ENOTFOUND (DNS, not resolvable in this session): ERİŞİLEMEDİ. Search snippet only [Ö]: "should be stable against larger timesteps than an explicit stream power scheme", "nominally implicit ... check their implementation is behaving stably". A 2019 GSA conference abstract claims "unconditionally stable" (non-peer-reviewed, [Ö]).
- arXiv 1909.03176 snippet [Ö]: explicit solvers impose a strict time-step constraint, motivating implicit methods.
- Braun & Willett 2013 (Geomorphology 180-181:170-179, "very efficient O(n), implicit and parallel method to solve the stream power equation"): [Ö] bibliographic + secondary (Landlab docs). Primary full text NOT fetched (publisher access not tested; no DOI verified here).
  - Landlab docs (secondary, [Ö]): the approach is stable against larger timesteps than explicit stream power; steady-state answer is correct for any dt, but transient results depend on dt (see Appendix B of the 2013 paper, not read).
  - Braun & Deal (preprint, not peer-reviewed, [Ö]): FastScape and its variable-discharge+threshold generalization "does not need to satisfy the CFL condition" and is accurate for small and very long dt.
  - Numerical dt value / CFL-like criterion for FastscapeEroder: BULUNAMADI (no number). Practical implication: do not assume dt-independence of transient results; test convergence by halving dt.

## Status

Status: DONE (all five topics attempted; limits listed below).

## Sources consulted / errors

Fetched in full (primary text, [B]):
- Miller et al. 2020, Sci Adv, PMC7228749 via Europe PMC (https://www.ebi.ac.uk/europepmc/webservices/rest/PMC7228749/fullTextXML)
- Shoemake 1985, SIGGRAPH '85 (https://www.fd.cvut.cz/personal/voracsar/GeometriePG/PGR020/shoemake.pdf)

Abstracts via Crossref (API) [B-öz]:
- Haq et al. 1987; Miller et al. 2005; Müller et al. 2008; Kominz et al. 2008; Wright et al. 2020 (EarthByte page)
- pygplates FiniteRotation API page and GPlates TRS manual (www.gplates.org) [B-öz]

Search snippets only [Ö]: Moucha 2008, Flament 2013, Müller 2018, Cogley 1984, Braun & Willett 2013 (secondary), Haq 2014, Miller 2011, hypsometry method.

Errors and blocks:
- Haq 1987 PDF (mantleplumes.awh.durham.ac.uk): TLS "unable to get local issuer certificate". ERİŞİLEMEDİ. Not bypassed.
- Miller 2020 Science Advances HTML (science.org): Cloudflare bot challenge ("Just a moment..."). ERİŞİLEMEDİ (bot protection, not bypassed); full text obtained via Europe PMC instead.
- Müller 2008 ResearchGate PDF: "Temporarily Unavailable" page. ERİŞİLEMEDİ. Abstract obtained via Crossref.
- doi.org/10.1002/2017JB014930: Cloudflare challenge; not used.
- Spasojević & Gurnis 2012 PDF URL returned HTML: ERİŞİLEMEDİ as PDF.
- landlab.readthedocs.io: DNS ENOTFOUND (not in allowed domains): ERİŞİLEMEDİ. FastscapeEroder docs not read.
- gplates.org (bare host used by WebFetch): ENOTFOUND; www.gplates.org works via curl.
- Wrong DOI guess for Wright 2020 returned an unrelated paper; no DOI cited.
- Gurnis 2012 Nature Geoscience: not found (BULUNAMADI). Closest is Spasojević & Gurnis 2012 AAPG Bull.

Unresolved (BULUNAMADI or NOT VERIFIED):
- Explicit peak rate in m/Myr from basin volume (only Miller 2011 "<10 m/Myr" [Ö]).
- Haq 1987 Cretaceous amplitude (250 m figure is from Haq 2014).
- GPlates interpolation algorithm and 1/5/10 Myr step practice.
- Animation frame count guidance: BULUNAMADI.
- FastscapeEroder numerical dt limit: BULUNAMADI.
- Hypsometric/shoreline explicit equation: NOT VERIFIED.
