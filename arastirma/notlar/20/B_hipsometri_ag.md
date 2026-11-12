# B. Hypsometry, Hack's law, Horton ratios, drainage density, slope-area relation

Status: search complete; several primary sources were inaccessible (see Network status).

Labels: [B] full text read; [B-öz] abstract or catalogue record only; [Ö] search-result summary (primary text not read); BULUNAMADI = not found in this pass; ERİŞİLEMEDİ = source could not be accessed.

## Network status

- WebFetch: pubs.usgs.gov, pure.psu.edu, www.scribd.com and en.wikipedia.org returned DNS errors (ENOTFOUND).
- curl -sSL (through the proxy) returned 200 for pubs.usgs.gov, en.wikipedia.org, pure.psu.edu, esurf.copernicus.org, pdodds.w3.uvm.edu and cukerala.ac.in. Text was extracted with oku.py (trafilatura) or pdftotext.
- ERİŞİLEMEDİ (bot protection, 403 or "Just a moment" challenge): AGU/GSA DOI landing pages (Rigon 1996, doi:10.1029/96WR02397; Strahler 1952, doi:10.1130/0016-7606(1952)63[1117:HAAOET]2.0.CO;2; Pike & Wilson 1971, doi:10.1130/0016-7606(1971)82[1079:ERHIAG]2.0.CO;2); the core.ac.uk copy of Wobus's 2005 thesis (core.ac.uk/download/4399269.pdf); Columbia Academic Commons (Melton 1957).
- ERİŞİLEMEDİ (TLS): escholarship.org (full text of Harrison et al. 1983) failed with a self-signed certificate chain error. Not bypassed.
- ERİŞİLEMEDİ (access denied): repository.library.noaa.gov (ETOPO1 NGDC-24 PDF) returned an "Access Denied" HTML page.
- Horton 1932 DOI (doi:10.1029/TR013i001p00350) returned 403.
- Wobus 2006 full text: Scribd and the core.ac.uk thesis were both inaccessible; only search summaries were used.

## 1. Hypsometric integral (HI)

- [Ö] Strahler 1952, "Hypsometric (area-altitude) analysis of erosional topography", GSA Bull. 63(11), 1117-1142, doi:10.1130/0016-7606(1952)63[1117:HAAOET]2.0.CO;2. Primary text ERİŞİLEMEDİ. Search summary: the youth/mature/old framework is from this paper; mature and old curves are identical unless monadnocks are present, so Strahler proposed inequilibrium, equilibrium and monadnock stages instead. Label: [Ö].
- Strahler 1952 youth > 0.6, mature 0.35-0.6, old < 0.35 cutoffs: NOT CONFIRMED against a primary source. These values are widely repeated in secondary literature. Label: BULUNAMADI (primary).
- [B-öz] Wikipedia "Hypsometry" (https://en.wikipedia.org/wiki/Hypsometry, fetched with curl): cites Strahler 1952 for the three-parameter hypsometric curve and describes the HI as "a summary measure of the shape of the hypsometric curve". It gives no numeric HI ranges or stage cutoffs. Label: [B-öz].
- [Ö] Pike & Wilson 1971, Bull. GSA 82, 1079-1084: shows that the hypsometric integral and the elevation-relief ratio are mathematically identical (search summary). Stage cutoffs from this paper: BULUNAMADI. Label: [Ö].
- [Ö] Secondary citations (not primary): Chorley & Kennedy (1971) state that at HI <= 0.60 the integral stabilizes irrespective of absolute relief; Carson & Kirkby (1972) report maturity at about 0.50. Label: [Ö].
- [B] Application example (secondary): Meenachil basin, Kerala (J. Environ. Res. Eng. Manag. 73(4), 2017, pp. 41-57, https://cukerala.ac.in/cukpdfs/IQAC/3.4.5/3.4.5.GEO.027.pdf). Subwatersheds with Ea >= 0.30 are classed as "mature" and Ea < 0.30 as "old". This is one study's threshold, not Strahler's. Label: [B] (application, not primary).

## 2. Hypsometry of Earth's land surface

- [Ö] Historical mean land elevations (arXiv 1810.08658, "Estimating Atmospheric Mass Using Air Density", https://arxiv.org/pdf/1810.08658): 700 m (1895), 840 m (1921), 871 m (1931), 797 m (2012). The 840 m value is thus attributed to a 1921 estimate in this source, not to Cogley (1984). The same source lists land medians of 466 m (Kossinna 1931) and 420.5 m (2012 estimate). Label: [Ö].
- [Ö] A 30-arc-second elevation study (PMC, search summary) reports a land-area median of 408 m. Label: [Ö].
- "Median 377 m": not found in any source reviewed. Label: BULUNAMADI.
- Cogley 1984: no source found (journal, volume and pages not verified). Label: BULUNAMADI.
- [Ö] Harrison, Miskell, Brass, Saltzman, Sloan 1983, "Continental hypsography", Tectonics 2(4), 357-377 (search summary). The open-access eScholarship copy was ERİŞİLEMEDİ (TLS). The 840 m and 377 m values could not be checked against it. Label: [Ö] + ERİŞİLEMEDİ.
- [Ö] Amante & Eakins 2009, ETOPO1, NOAA Tech. Memo NESDIS NGDC-24 (DOI 10.7289/V5C8276M; search summary). PDF ERİŞİLEMEDİ (access denied). Whether it reports land-mean or median elevation could not be checked. Label: [Ö] + ERİŞİLEMEDİ.
- [Ö] Eakins et al. 2022, ETOPO 2022 15 arc-second model (DOI 10.25921/fd45-gt74; search summary). No land-mean statistic found in the record. Label: [Ö], BULUNAMADI (statistic).

## 3. Hack's law

- [B] Hack 1957, USGS Prof. Paper 294-B, "Studies of longitudinal stream profiles in Virginia and Maryland", pp. 45-97, doi:10.3133/pp294B. URL: https://pubs.usgs.gov/pp/0294b/report.pdf. Equation (3): L = 1.4 A^0.6, with L in miles and A in square miles. Quote: "The coefficient of the equation relating length and area averages around 1.4 but ranges between 1 and 2.5." For sandstone areas the coefficient is about 2.0. Measured drainage areas: 0.12-375 square miles. Label: [B].
- [B] Hack 1957 explains the 0.6 exponent by changing basin shape: if shape stayed constant the exponent would be 0.5 (derivation with mean width W_a = A/L). Label: [B].
- [B-öz] Wikipedia "Hack's law" (https://en.wikipedia.org/wiki/Hack%27s_law, fetched with curl): "the exponent h is slightly less than 0.6 in most basins", and slightly lower for basins above 8,000 mi². Wikipedia is a supporting source only. Label: [B-öz].
- [Ö] Rigon, Rodriguez-Iturbe, Maritan, Giacometti, Tarboton, Rinaldo 1996, "On Hack's law", Water Resour. Res. 32(11), 3367-3374, doi:10.1029/96WR02397 (ERİŞİLEMEDİ). Search summary: tests the relation with DEMs; links the exponent to elongation and fractal characters; gives a scaling-based explanation. Label: [Ö].
- Do not confuse with Willemin 2000, "Hack's law: sinuosity, convexity, elongation", WRR 36(11), 3365-3374, doi:10.1029/2000WR900229 (cited in the Wikipedia reference list). Label: [B-öz].

## 4. Horton ratios

- [B] Horton 1945, "Erosional development of streams and their drainage basins", GSA Bull. 56, 275-370. Copy read via pdftotext: https://pdodds.w3.uvm.edu/research/papers/others/1945/horton1945a.pdf (OCR is imperfect).
  - Bifurcation ratio R_B: "ranges from about 2 for flat or rolling drainage basins up to 3 or 4 for mountainous or highly dissected drainage basins." Label: [B].
  - Length ratio R_L: "range from about 2 to about 3; the average is 2.32." Label: [B].
  - Area ratio R_A: not found in the Horton text. Label: BULUNAMADI.
- Comparison with the brief: the brief's ranges (R_B 3-5, R_L 1.5-3.5, R_A 3-6) do not match Horton's own values (R_B upper limit 4 in Horton 1945). They may come from Strahler 1957 or Schumm 1956, which could not be verified here.
- [Ö] Strahler 1957 (Trans. AGU) and Schumm 1956 (GSA Bull. 67, 597-646, doi:10.1130/0016-7606(1956)67[597:EODSAS]2.0.CO;2). Schumm: bibliographic record confirmed; no free full text. Search summary: a fifth-order system in the Perth Amboy badlands; hypsometric analysis shows the point of maximum erosion migrating upchannel. R_B/R_L/R_A values: BULUNAMADI. Label: [Ö].

## 5. Drainage density and threshold area

- [Ö] Melton 1957, "An analysis of the relations among elements of climate, surface properties, and geomorphology", Columbia Univ., ONR Tech. Rep. 11, project NR 389-042. Full text ERİŞİLEMEDİ (Columbia bot challenge). Search summary: covers drainage density in relation to soil and climate. No numeric range obtained. Label: [Ö].
- [B] Horton 1945 defines drainage density in the text, but no numeric range was extracted in this pass. Label: BULUNAMADI (this pass).
- Horton 1932 (Trans. AGU 13): DOI returned 403; full text ERİŞİLEMEDİ. Label: ERİŞİLEMEDİ.
- Threshold (hillslope-channel transition) area: no numeric value found in the Wobus 2006 abstract or in search summaries. Label: BULUNAMADI.

## 6. Slope-area relation

- [B-öz] Kirby & Whipple 2012, "Expression of active tectonics in erosional landscapes", J. Struct. Geol. 44, 54-75, doi:10.1016/j.jsg.2012.07.009. Source: PSU record (https://pure.psu.edu/en/publications/expression-of-active-tectonics-in-erosional-landscapes/). Type: "Review article". Abstract: "existing data support theoretical expectations of positive, monotonic relationships between channel steepness index, a measure of channel gradient normalized for downstream increases in drainage area, and erosion rate at equilibrium". Label: [B-öz]. Full text not accessed.
- Kirby & Whipple 2012 giving theta_ref = 0.45 or "theta = 0.45 +/- 0.2": not in the abstract or record. A search summary attributes "0.4 < theta < 0.6" to this paper. Labels: [Ö] (secondary), BULUNAMADI (primary).
- [B] Mudd, Clubb, Gailleton, Hurst 2018, "How concave are river channels?", Earth Surf. Dynam. 6, 505-523, doi:10.5194/esurf-6-505-2018. Full text: https://esurf.copernicus.org/articles/6/505/2018/esurf-6-505-2018.pdf (read via pdftotext). Equation (1): S = k_s A^(-theta), with theta the concavity index and k_s the steepness index. A reference concavity theta_ref is used to normalise steepness (k_sn = A^theta_ref S, their eq. 6, citing Wobus et al. 2006a). Label: [B].
  - In this paper theta ~ 0.45 is the peak of the best-fit concavity distribution for one basin (disorder and bootstrap methods). For the Loess Plateau the authors recommend reference concavities of 0.4-0.5. This is not Kirby & Whipple's value. The string "+/- 0.2" does not appear. Label: [B].
  - The paper shows the choice of theta_ref changes relative k_sn values across a network. Label: [B].
- [Ö] Wobus, Whipple, Kirby, Snyder, Johnson, Spyropolou, Crosby, Sheehan 2006, "Tectonics from topography: procedures, promise, and pitfalls", GSA Spec. Pap. 398, pp. 55-74, doi:10.1130/2006.2398(04). Full text ERİŞİLEMEDİ. Search summary: channel-profile indices; slope-area power law; scaling breaks may map tectonic boundaries. No hillslope-channel threshold or theta_ref value found. Label: [Ö].

## Open items

- Primary HI stage cutoffs (Strahler 1952; Pike & Wilson 1971): need GSA access. Currently only secondary confirmation.
- Rigon et al. 1996 full text: needs AGU access.
- Kirby & Whipple 2012 full text: needed to check theta_ref and the "0.45 +/- 0.2" wording.
- Harrison et al. 1983 (840 m / 377 m): blocked by a TLS certificate error; cannot be checked without bypassing it.
- ETOPO1 NGDC-24: access denied; land-mean statistic not verified.
- Brief's R_B 3-5, R_L 1.5-3.5, R_A 3-6 and the "0.45 +/- 0.2" value were not confirmed in any primary text read in this pass.
- Cogley 1984: no source found.
