# B: Lithology and Relief (litoloji ve rölyef)

Status: COMPLETE for the requested topic list, with gaps marked. Each finding carries a value, URL, a supporting phrase (short), and a tag.

Tags: [B] full text read (local copy); [B-öz] summary of a primary-source abstract/excerpt; [Ö] search-result summary only; BULUNAMADI = not found; ERİŞİLEMEDİ = could not access.

Network notes:
- WebFetch returned DNS errors for doi.org, www.uvm.edu and landlab.csdms.io.
- curl via the proxy fetched www.uvm.edu (thesis PDF, HTTP 200) and landlab.csdms.io (HTTP 200) and Wikipedia pages (HTTP 200).
- doi.org/10.1029/2012GC004370 returned HTTP 403 via curl. This looks like publisher/bot protection. It was not bypassed; the paper is marked ERİŞİLEMEDİ.

---

## (1) K (erodibility) and lithology

### 1a. Stock & Montgomery 1999 (K ranges by lithology)
- Paper: Stock & Montgomery 1999, "Geologic constraints on bedrock river incision using the stream power law", JGR 104, 4983-4993, doi 10.1029/98JB02139. Full text: ERİŞİLEMEDİ (doi.org not resolvable).
- K ranges, m = 0.4, units m^0.2 / yr [Ö]:
  - granite and metamorphic rocks: 10^-7 to 10^-6
  - volcaniclastic rocks: 10^-5 to 10^-4
  - mudstone: 10^-4 to 10^-2
  - Source: https://earthref.org/ERR/42355 (EarthRef abstract; search summary)
- "K ratio 10-100": the range is not stated as such in the paper. Arithmetic from the ranges above (my calculation, not the paper's wording): mudstone vs granite/metamorphic differs by about 10^2 to 10^5 (roughly 3-4 orders of magnitude). Treat the "10-100" phrasing as unverified.
- Two incision laws reported [B-öz]: K A^(0.3-0.5) S for Australian rivers with stable base level, and K_f A^(0.1-0.2) S_h for Kauai rivers with abrupt base-level change.

### 1b. Sklar & Dietrich 2001 (rock strength)
- Paper: "Sediment and rock strength controls on river incision into bedrock", Geology 29(12), 1087-1090, doi 10.1130/0091-7613(2001)029<1087. Full text: ERİŞİLEMEDİ.
- Finding [Ö]: erosion resistance scales with the square of tensile strength. Source: https://typeset.io/pdf/sediment-and-rock-strength-controls-on-river-incision-into-21g3zfozyk.pdf
- Finding [Ö]: erosion is nonlinear in sediment supply and grain size; fine sediment is a poor abrasive because it travels in suspension.
- Finding [Ö]: tensile strength is argued to be a better erodibility measure than Schmidt hammer rebound (Bursztyn, Grand Canyon summary: https://serc.carleton.edu/68937).

### 1c. Kirby & Whipple 2012
- Paper: "Expression of active tectonics in erosional landscapes", J. Structural Geology (2012). Full text: BULUNAMADI in this session.
- Finding [B-öz] from abstract: lithology, climate and uplift pattern complicate interpretation of channel profiles; topography alone allows multiple interpretations. Source: https://pure.psu.edu/en/publications/expression-of-active-tectonics-in-erosional-landscapes/
- "Lithologic knickpoint" definition in Kirby & Whipple 2012: BULUNAMADI (direct text not read).
- Indirect [Ö]: lithologic knickpoints are fixed to contacts between resistant and weak units (Whipple 2004, cited in a senior thesis: https://czo-archive.criticalzone.org/images/national/associated-files/Shale Hills/Neely_Al_SeniorThesis.pdf).

### 1d. Ratio support from another source
- Zondervan et al. (GSA 2022 abstract) [Ö]: intact-rock strength implies erodibility varies by about two orders of magnitude; K is normalized to the weakest lithology using uniaxial compressive strength. Source: https://gsa.confex.com/gsa/2022PR/webprogram/Handout/Paper376063/Zondervan_Jesse.pdf
- Harel et al. 2016 compilation [Ö, secondary mention]: K ∝ 1/q_u^2 (q_u = unconfined compressive strength); K is a bulk parameter that also absorbs climate, sediment and hydrology. Primary Harel et al. 2016 paper: NOT located and not read; source URL unconfirmed (BULUNAMADI as a verified link).
- Summary: a K ratio of about 10-100 is supported by the [Ö] Zondervan statement; the wider 10^2-10^5 spread comes from the Stock & Montgomery ranges (my arithmetic).

---

## (2) Layered rock: cuesta, hogback, mesa/butte; LEM implementation

### 2a. Landforms [B] (Wikipedia, local full text)
- Hogback: long narrow ridge from differential erosion of steeply dipping (>30-40 degrees) homoclinal sedimentary strata, alternating hard (sandstone, limestone) and weak (shale, mudstone, marl) beds. Source: https://en.wikipedia.org/wiki/Hogback_(geology)
- Example: Dinosaur Ridge, Colorado (Dakota Sandstone over Morrison Formation mudstone). Same source.
- Cuesta: asymmetric ridge with a gentle dip slope on the hard caprock and a steep scarp; gently dipping (lower dip than hogback). Source: https://en.wikipedia.org/wiki/Cuesta
- Continuum: hogback, homoclinal ridge and cuesta differ only by dip angle of the resistant beds. Both sources.
- Appalachian hogback: BULUNAMADI as a specific cited value. The Wikipedia page lists general examples only.

### 2b. Inverted topography and mesa caprock [Ö]
- Basalt flows fill valleys, then persist as high ground as soft surrounding rock erodes (NPS: https://www.nps.gov/articles/000/volcanic-inverted-topography.htm).
- Basalt is more erosion-resistant than surrounding red sandstone and shale; the cap controls the mesa's steep sides (Grand Mesa, Colorado, is an example). Source: https://ebsco.com/research-starters/geology/mesa-geology
- Exception: Herðubreið (Iceland) is a tuya, not an erosion remnant.

### 2c. Landlab LithoLayers (LEM implementation) [B] for the Landlab page; [Ö] for the component
- Landlab home page (https://landlab.csdms.io/, local full text) does not mention lithology; the component docs were not in the local copy (404 on guessed reference URLs).
- LithoLayers component [Ö]: rock types as IDs, each with property values such as K_sp (stream-power erodibility); layers are set by elevation (z0s) and per-layer IDs, so alternating IDs give flat or dipping layers; grid fields update as rock is exposed.
- Sources (search summaries): https://landlab.readthedocs.io/en/latest/reference/components/litholayers.html ; https://landlab.readthedocs.io/en/latest/tutorials/lithology/lithology_and_litholayers.html
- Caveat [Ö]: defaults may differ across versions; check the release used.

### 2d. Fastscapelib K map [Ö]
- SPLEroder takes k_coef as a scalar or a per-node array matching the grid size (implicit finite difference SPL solver). Source: https://fastscapelib.readthedocs.io/en/latest/api_python/_api_generated/fastscapelib.SPLEroder.html
- fastscape-litho maps an integer lithology label grid plus a per-rock-type parameter lookup to K (3D K supported; early-stage package, 2021). Source: https://pypi.org/project/fastscape-litho
- Workable recipe [Ö-derived]: build a 2D K array from a lithology label grid and pass it as k_coef. An official example for this workflow was not found: BULUNAMADI.

---

## (3) Hard-soft interbedding, granite batholith, volcanic terrain

### 3a. Granite tors and inselbergs [Ö]
- Strudley et al.: tors can arise from weathering-transport feedback, not only lithologic templates; tors may shrink with climate or base-level change, so they can be transient. Source: https://earthref.org/ERR/95873 (search summary; primary citation not confirmed).
- Zimbabwe morphometric study [Ö]: inselberg backwearing occurs on foliated, fractured, grusified granitoids. Source: search summary only; primary citation not confirmed.
- 10Be-based tor/scarp denudation (Sila Massif, EGU2019 abstract) [Ö]: slopes denude faster than planar surfaces. Source: https://meetingorganizer.copernicus.org/EGU2019/EGU2019-482.pdf
- Granite batholith relief contrast vs erosion rate: BULUNAMADI (no study quantifying batholith-scale relief contrast found).

### 3b. Interbedded hard/soft ratio
- Hogback and cuesta examples in 2a describe the mechanism; a quantitative relief-ratio value: BULUNAMADI.

---

## (4) Karst

- Karst is a topography from dissolution of soluble carbonates (limestone, dolomite); features include poljes, sinkholes (dolines), and underground drainage that can leave few or no surface rivers or lakes. [B] Source: https://en.wikipedia.org/wiki/Karst
- Karst is most developed in dense, thinly bedded, fractured limestone; chalk is typically poorly developed because it is porous. [B] Same source.
- Interstratal karst: insoluble sandstone cover over limestone can host doline fields (Wales examples). [B] Same source.
- Karst may occur in quartzite under the right conditions. [B] Same source.
- Quantitative "surface runoff deficit" value for karst vs non-karst: BULUNAMADI.

---

## (5) Global lithology maps

### 5a. GLiM (Hartmann & Moosdorf 2012)
- Paper: Geochemistry, Geochemical Geophysics, Geosystems 13, Q12004, doi 10.1029/2012GC004370. Full text: ERİŞİLEMEDİ (HTTP 403).
- 16 first-level lithology classes; second and third levels add 12 and 14 subclasses; about 1,235,400 polygons [Ö]. Sources: https://www.cen.uni-hamburg.de/facilities/visualization/interactive/lithological.html ; https://csdms.colorado.edu/wiki/Alldata:GLiM
- Broad area shares [Ö]: sediments about 64% (one-third of which are carbonates); metamorphics about 13%; plutonics about 7%; volcanics about 6%; water/ice about 10%. Shares for the 16 individual classes: BULUNAMADI.
- Version note [Ö]: CSDMS says v1.1; PANGAEA lists v1.0. Input map counts differ across sources (65 vs 92): unresolved.
- Data record: https://doi.pangaea.de/10.1594/PANGAEA.788537 (not downloaded in this session).

### 5b. GLHYMPS (Gleeson et al. 2014)
- Paper: Gleeson, Moosdorf, Hartmann & van Beek 2014, GRL 41, 3891-3898, doi 10.1002/2014GL059856. Full text: not read.
- Resolution: average polygon size about 100 km^2 (more than 100x finer than the previous map) [Ö]. Source: https://dspace.library.uvic.ca/items/13157b31-0236-41dd-8eb4-1c2aa0851dcf
- Mean permeability about 10^-15 m^2 (with permafrost) or 10^-14 m^2 (without) [Ö]; mean porosity 14% [Ö].
- Built on the high-resolution global lithology map and separates fine-grained from coarse sediments and sedimentary rocks [Ö].
- Dataset: https://openpolar.no/Record/ftborealisdata:doi:10.5683%2FSP2%2FDLGXYO/Details (DOI 10.5683/SP2/DLGXYO).

### 5c. Area per rock class: BULUNAMADI at class level for both GLiM and GLHYMPS.

---

## (6) Lithology effect on denudation rate (10Be)

Source: Portenga, E.W., "Using 10Be to constrain erosion rates of bedrock outcrops globally and in the central Appalachian Mountains", UVM MS thesis. Full text read locally [B]: https://www.uvm.edu/cosmolab/people/portenga/Portenga_Thesis_Final.pdf
Note: the thesis is the data source; the GSA Today article (Portenga, Bierman & Reusser, 2011) was not accessed.

- Global meta-analysis: outcrops n = 418, fluvial sediment (basins) n = 1110, 82 studies [B].
- Drainage-basin mean: 209 ± 33 m/My; median 53 m/My (n = 1110) [B].
- Outcrop mean: 12 ± 1.3 m/My; median 5.2 m/My (n = 418) [B].
- By outcrop lithology [B]: sedimentary 19 ± 1.9 m/My (n = 106); metamorphic 13 ± 1.7 m/My (n = 82); igneous 8.6 ± 0.9 m/My (n = 230). Sedimentary and metamorphic are statistically similar and faster than igneous.
- By climate [B]: temperate 26 ± 2.6 m/My (n = 75); polar 3.9 ± 0.39 m/My (n = 31).
- Unit note: 1 m/My = 1 mm/ka.
- The "218 mm/ka average" value supplied in the request: NOT in the thesis (BULUNAMADI). The thesis gives 209 m/My for drainage basins. The GSA Today value could not be checked.
- Climate and temperature show weak relation with global denudation rates [Ö, search summary].

---

## Implications for the tool (how an LEM could mimic litology)

Based on the findings above (not a tested implementation):
1. Assign K per cell from a lithology label grid (Landlab LithoLayers or Fastscapelib k_coef array). Use Stock & Montgomery class ranges as starting bounds, not fixed values.
2. Relative K contrast of 10-100 (strength-scaled, Zondervan) is a reasonable first-order range; 10^2-10^5 is the wider literature spread (my arithmetic, unverified against the paper).
3. Dipping sedimentary layers with alternating hard and weak beds produce hogbacks and cuestas; flat layers give mesas with resistant caps.
4. Basalt caprock and inverted topography need a resistant unit over a weak unit; this is a layer-stack setup.
5. Karst needs a separate process (dissolution, subsurface drainage), not just a K change; surface-runoff suppression is not in standard stream-power models.
6. Global targets for calibration: denudation medians 5-53 m/My (outcrop to basin). Lithology medians are not given in the thesis; only means.

---

## Open items

1. Full text blocked: Stock & Montgomery 1999; Sklar & Dietrich 2001; Kirby & Whipple 2012; Hartmann & Moosdorf 2012; Gleeson et al. 2014; Portenga et al. 2011 (GSA Today). Need doi.org access or a PDF mirror.
2. "218 mm/ka" value: verify in the GSA Today article.
3. Per-class GLiM area shares (16 classes): from the GLiM data or Hartmann & Moosdorf 2012 tables.
4. Appalachian hogback example with specific values: not found.
5. Granite batholith relief contrast vs erosion: no quantitative study found.
6. Karst surface runoff deficit quantified: not found.
7. Landlab LithoLayers default settings per version: check the release in use.
