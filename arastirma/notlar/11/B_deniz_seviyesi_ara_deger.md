# B: Sea-level curves, plate/basin-driven sea-level rates, dynamic topography, shoreline computation, rotation interpolation, numerical stability

Status: IN PROGRESS (skeleton written first; findings appended as they are verified)

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
- Peak values (summary of the above): Late Cretaceous high estimates range roughly +40 to +250 m (Müller 2008 intro); Miller 2005 +100 +/- 50 m; Müller 2008 +170 (85 to 270) m; Kominz 2008 +75 to +110 m (Late Cretaceous), +150 m (Early Eocene). The +100 to +250 m range in the task is consistent with the Müller/Miller bounds; the "+250" is the upper end of the Müller estimate range, not a measured peak.
- Rate (m/Myr) from basin volume / tectonics: NOT FOUND in the fetched sources yet. Miller 2020 gives a long-term 1.0 +/- 0.5 m/Ma Cenozoic decrease (see above). Search for explicit peak-rate figures still needed (Wright et al. 2020, Earth-Science Reviews, is reported by search snippet [Ö] to show ~200 m change since Jurassic from basin volume).

## 2. Dynamic topography and sea level (Gurnis, Moucha, Müller)

- "Gurnis 2012, Nature Geoscience" as named in the task: [Ö] NOT FOUND. Search returned no such paper. Closest: Spasojević & Gurnis 2012, AAPG Bulletin (hybrid inverse-forward convection model; dominant control on global sea level is ocean-lithosphere production; dynamic topography offsets the fall). Snippet URL: https://earthbyte.org/Newsletter/Issue2/2012_SpasojevicGurnis_AAPG_Bull.pdf. Fetch returned an HTML page (not a PDF): ERİŞİLEMEDİ as PDF.
- Moucha et al. 2008 (EPSL): [Ö] title from a Nature Geoscience reference list: "Dynamic topography and long-term sea-level variations: there is no such thing as a stable continental platform." Full text not fetched.
- Flament, Gurnis, Müller 2013 (Lithosphere review): [Ö] dynamic topography means long-term global sea-level change "cannot be estimated at a single passive margin."
- Müller, Hassan, Gurnis, Flament, Williams 2018 (Gondwana Research): [Ö] best-fit convection models give up to 500 (+/-150) m total dynamic subsidence in continental interiors.
- Nature Geoscience "Global dynamic topography observations reveal limited influence of large-scale mantle flow" [Ö]: at ~10^4 km wavelengths observed dynamic topography peaks ~+/-500 m. Authors/year not confirmed from search; do not cite without checking.
- Müller 2008 (above): NJ subsidence 105 to 180 m attributed partly to dynamic topography over subducted Farallon plate [B-öz].

## 3. Shoreline from paleotopography + sea level; hypsometry (Cogley 1984)

- Cogley 1984 (Reviews of Geophysics 22(2):101-122, DOI 10.1029/RG022i002p00101, "Continental margins and the extent and number of the continents"): [Ö] Crossref/search abstract summary: 14 continents, ~41% of Earth's surface (210.4 x 10^6 km^2); mean continental crust thickness ~36 km; crustal volume 7.2 x 10^9 km^3; height and thickness strongly linked. Source: https://scilit.com/publications/1941408b5ac0b6ddf3524191917e8705. Full text not fetched. Hypsometry formula (area vs elevation) NOT VERIFIED in this session.
- Shoreline formula (paleotopography + sea level = shoreline; hypsometric integration of area above sea level): PENDING, to be taken from Cogley / Müller / Kominz texts; not yet fetched.

## 4. Animation frames: SLERP / Euler pole interpolation, GPlates interpolation, C1 continuity, step sizes

- Shoemake 1985 (Animating rotation with quaternion curves, SIGGRAPH '85, Computer Graphics 19(3):245-254): [B] full text from https://www.fd.cvut.cz/personal/voracsar/GeometriePG/PGR020/shoemake.pdf (pdftotext). Note: the PDF's author line reads "Ken Shoemaker"; other indexes spell "Shoemake".
  - Slerp formula (Sec. 3.3 area): Slerp(q1,q2;u) = [sin((1-u)theta)/sin theta] q1 + [sin(u theta)/sin theta] q2, with cos theta = q1.q2 (OCR of the PDF; the extracted text gives the form "Slerp(ql,q2;u) = sin((1-u)...)/sin ... ql + ..."; cos(theta) = q1.q2 is stated in the paper's text as "q1*q2 ~ cos theta").
  - Motivation (Sec. 3.2): "Straight lines between quaternions ... If our interpolated points were evenly spaced along a line, the animated rotation would speed up in the middle." Solution: "great circle arc" on unit sphere, "we can rotate without speeding up by interpolating on the sphere" (Sec. 3.3).
  - Continuity: "the direction of rotation changes abruptly ... we want higher order continuity." Spline joints: "As the curve goes through its end points it is tangent to its end segments. Line up the segments across a join, match their lengths" (tangent/first-order continuity, i.e. C1 on the sphere; exact wording partly garbled by OCR).
  - Result: constant-speed rotation along great circle = constant angular velocity when u is linear in time (inference: standard reading of Sec. 3.3; the paper says speed is constant on the sphere).
  - Exact step sizes for animation: not stated in the paper (inference).
- GPlates finite rotation interpolation: PENDING
- Example step sizes (1 / 5 / 10 Myr): PENDING

## 5. Numerical stability of uplift/erosion vs time step (Fastscape, CFL-like condition)

- PENDING

## Sources consulted / errors

- Network: PENDING
