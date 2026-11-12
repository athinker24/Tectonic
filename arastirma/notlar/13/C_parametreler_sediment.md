# Stream power law parameters (K, m, n, theta = m/n) and sediment transport: source notes

Status: IN PROGRESS. Tags: [B] full text read, [B-öz] summary/abstract-level, [Ö] search summary only, BULUNAMADI = not found, ERİŞİLEMEDİ = not accessible.

## Findings

### F1. Ruetenik et al. 2023, "Optimising global landscape evolution models with 10Be" (ESurf 11, 865-880)
- URL: https://esurf.copernicus.org/articles/11/865/2023/
- Tag: [B]
- Global Monte Carlo fit of LEMs to 10Be denudation rates (OCTOPUS catalogue).
- Advection-only optimum: n ~ 1.3 (no diffusion); advection-diffusion optimum: n ~ 2.3 (Q0.01 = 1.59-2.70); diffusion-only optimum exponent p ~ 2.0 (NSE 0.51).
- Optimised D/K ~ 1.79e6 m^(0.9n+1) (Q0.01 = 2.97e4 to 3.44e7), co-dependent with n.
- Quote (paraphrase of K): "broadly agrees with other studies that use K values in the range of ~1e-8 to 1e-5 m^(n-1) yr^-1 and D values ... 4.4e-4 to 3.6e-2 m^2 yr^-1" (Fernandes & Dietrich 1997 range for D).
- Whipple et al. 2017 optimal D/K = 5e2 (Himalaya, n fixed to 1), cited by Ruetenik as limited by fixed n.
- Sensitivity: n rises from ~1.1 to ~1.5 with drainage area in advection-only models; n range ~1.3 to ~3 for small catchments in advection-diffusion models.
- K vs precipitation: positive correlation for MAP > 1500 mm/yr and a local K maximum near ~300 mm/yr (semi-arid erodibility peak). Lithology: threefold K range within lithologic bins (much smaller than Sklar & Dietrich 2001 or Garcia-Castellanos & O'Connor 2018).
- Limitation stated by authors: m/n ratio not resolved by their approach.

### F2. Davy & Lague 2009 (JGR Earth Surface 114, F03007)
- DOI: https://doi.org/10.1029/2008JF001146 ; open PDF: https://hal.archives-ouvertes.fr/insu-00424874
- Tag: [Ö] (abstract-level via search; HAL PDF URL returned HTML, full text NOT retrieved yet)
- Mass balance of streamflow with erosion and deposition fluxes; the xi-q model reduces to transport-limited or detachment-limited depending on xi(q), but not always.
- Implemented in Landlab ErosionDeposition component.
- Full text: still to be retrieved (see open items).

### F3. Stock & Montgomery 1999 (JGR 104, 4983-4993)
- DOI: https://doi.org/10.1029/98JB02139
- Tag: [Ö]
- Numeric K range from this paper: BULUNAMADI (search summaries did not give it; full text not yet read).
- Concept: m, n, K constrained by matching evolved profile to modern profile over age of mapped paleoprofiles; K varies with lithology and this drives landscape change rate variability.
- Stock et al. 2005 (field incision after bedrock exposure): power law deviates at slopes > 0.03-0.10. Source: https://faculty.washington.edu/bcollins/publications_pdfs/Stock_et_al_2005_Field_measurements_of_incision_rates_following_bedrock_exposure.pdf [Ö]

### F4. Harel, Mudd & Attal 2016 (Geomorphology 268, 184-196)
- DOI: 10.1016/j.geomorph.2016.05.035 ; abstract: https://ui.adsabs.harvard.edu/abs/2016Geomo.268..184H
- Tag: [Ö]
- Global 10Be dataset; n and K normalised to theta = m/n = 0.5.
- Multiple regression: local K-precipitation correlation does NOT hold globally; questions regional climate/tectonic interpretations that assume uniform n.
- Sample count discrepancy between sources (EGU 2015 abstract: 1335 rates, 66 areas; preprint: 59 areas). Final published N not verified.
- Numeric K range: not yet retrieved from full text.

### F5. Lague 2014, "The stream power river incision model: evidence, theory and beyond" (ESPL 39, 38-61)
- DOI: https://doi.org/10.1002/esp.3638 (ESPL article ID; search gave DOI 10.1002/esp.3462 in one index, the preprint PDF prints 10.1002/esp.3638). Preprint: https://orbi.uliege.be/bitstream/2268/190050/1/preprint.pdf
- Tag: [B] (full text of preprint read via pdftotext; typeset page numbers in the PDF)
- m/n statements: "most calculated values of the m/n ratio fall in the range 0.4-0.7"; theory: m ~ 0.5 and n ~ 1 for unit stream power; m ~ 0.3 and n ~ 0.7 for shear stress.
- Worked examples in the same paper: Ourthe catchment fit gives m = 0.75, K = 4.63e-8 (units m^-0.5 yr^-1 as printed), and an improved m/n = 0.68 under n = 1 (paper discusses departure from 0.5).
- Second case in the text: m range 0.69-0.81 and K range 1.43e-8 to 1.61e-7 (printed units ~m^(1-2m)/yr, not further verified). The text compares these with a Roan Plateau fit: 0.50 < m < 0.62, 3.33e-8 < K < 2.87e-7.
- Concludes that the standard SPIM has inconsistencies (threshold/stochastic and width effects, sediment flux).
- Detachment- vs transport-limited discussion present in the paper (section on "Detachment- or transport-limited model?").

### F6. Harel et al. 2016 numeric K/n values
- Tag: [Ö] only. Full text was not accessed (core.ac.uk PDF returned HTTP 403). Numeric K range: not retrieved (BULUNAMADI in accessed sources).

### F7. Stock & Montgomery 1999 K range "1e-7 to 1e-2" (claim from task brief)
- Status: NOT VERIFIED. Full text was not accessed. The par.nsf.gov purl 10471890 that was offered as a source turned out to be Anderson, Gasparini & Johnson 2023 (ESurf 11, 995-1011, "Building a bimodal landscape..."), not Stock & Montgomery 1999. The K range remains BULUNAMADI in accessed sources. Do not cite the 1e-7 to 1e-2 range as sourced.

### F8. Whipple & Tucker 1999 (K as function of rock, geometry, hydrology, sediment)
- PDF URL https://planetarygeoscience.uchicago.edu/doc/Whipple_and_Tucker_1999.pdf: ERİŞİLEMEDİ (TLS certificate verification failed with curl; not bypassed).
- Via search summary [Ö]: Whipple & Tucker 1999 note K depends on bedrock properties, channel geometry, basin hydrology and sediment load (see Stock et al. 2005 and search results).

### F9. Davy & Lague 2009 full text
- HAL URLs (hal.archives-ouvertes.fr and hal.science) returned HTML landing pages, not PDF. Full text ERİŞİLEMEDİ; remains [Ö].

### F10. Shobe et al. 2017 SPACE (GMD 10, 4577-4604)
- DOI: 10.5194/gmd-10-4577-2017 ; https://gmd.copernicus.org/articles/10/4577/2017/
- Tag: [Ö]. Explicit sediment mass conservation on bed and in the water column; steady-state solutions for slope, alluvium thickness and sediment flux; reproduces detachment-limited, transport-limited and mixed behaviour.

### F11. Ruetenik 2023 vs Adams 2020
- Adams, Cook, ... "Climate controls on erosion in tectonically active landscapes", Science Advances 6(42), eaaz3166, DOI 10.1126/sciadv.aaz3166 (https://pmc.ncbi.nlm.nih.gov/articles/PMC7567587). Tag [Ö]. Erosion nonlinear in relief with proportionality set by mean annual rainfall; rainfall treated explicitly instead of inside K. (The brief's "Adams 2020 Climate-adjusted K" title is not the title found; citation to be corrected.)

### F12. Campforts 2017
- Found: Campforts, Schwanghart & Govers 2017, "Accurate simulation of transient landscape evolution by eliminating numerical diffusion: the TTLEM 1.0 model", ESurf 5, 47-66 (https://esurf.copernicus.org/articles/5/47/2017/). Tag [Ö]. It is NOT a landslide-threshold paper. Brief's "TTLEC 2017 landslide" is not found: BULUNAMADI for that claim.

### F13. Egholm 2013 (brief: "A mechanical model of landslide", Geology, critical slope 30-40 deg)
- Geology paper: BULUNAMADI. Closest match found: a 2013 Nature 498 paper (article 12218) on bedrock landsliding coupled with fluvial saltation-abrasion, with a stochastic landsliding model (PDF https://msandifo.github.io/pdfs/peer/2013_nature12218.pdf; authors not confirmed). Tag [Ö].
- Critical-angle values 30-40 deg: not confirmed from accessed sources.

### F14. Densmore et al. 1998 mechanical stability criterion
- Cited in search summaries as the mechanical stability criterion used in landscape evolution models for landslide triggering. Tag [Ö] (indirect via 2019 study summary).

### F15. Gailleton 2019 vs Hergarten (m/n / theta debate)
- Gailleton 2019 paper: BULUNAMADI in search. Related: Mudd, Clubb, Gailleton & Hurst 2018, "How concave are river channels?" (ESurf 6, 505-523; https://esurf.copernicus.org/articles/6/505/2018/), [Ö]: chi-based methods reproduce imposed m/n better than slope-area methods.
- Gailleton et al. EGU2020 presentation (https://presentations.copernicus.org/EGU2020/EGU2020-503_presentation.pdf) lists Hergarten et al. 2016 among methods that choose optimal theta. Conference slides, [Ö].
- A direct Gailleton-vs-Hergarten exchange: BULUNAMADI.

### F16. Ruetenik vs task brief: Ruetenik is on the global K/D topic; Anderson 2023 (ESurf 11, 995) is about lithology and Ksn, not used numerically.

## Open items
- Davy & Lague 2009 full text (HAL URL returned HTML landing page).
- Stock & Montgomery 1999 full text (K range).
- Harel 2016 full text (K, n values).
- Lague 2014 (ESPL), Gailleton 2019 vs Hergarten (m/n), Whipple & Tucker 1999, Roering 1999, Fernandes & Dietrich 1997, Densmore 1998, Campforts 2017, Egholm 2013, Shobe 2017 SPACE, Whipple 2009, Adams 2020.
