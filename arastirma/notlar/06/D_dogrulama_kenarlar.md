# D: Primary-text verification (margins, bridges, bathymetry)

Status: verification pass done. Labels: [B] primary text read (abstract or full text); [E] encyclopedia; [O] search summary only; BULUNAMADI = not found in any source read.

Scratch copies: /tmp/claude-0/-home-user-Tectonic/1cb340b3-df7d-519b-96f4-5170b8cfb37a/scratchpad/src/

## Access log
- WebFetch: DNS failure (ENOTFOUND) for www.grida.no and topex.ucsd.edu. WebFetch and curl are not the same path: curl through the proxy reached grida.no, nature.com, link.springer.com, en.wikipedia.org, earthref.org, www.nespmarine.edu.au, uchicago (cottagelabs mirror).
- curl failed: topex.ucsd.edu (no connection, rc 000); people.earth.yale.edu (proxy 502 CONNECT, twice); mantleplumes.awh.durham.ac.uk (TLS: issuer not in bundle, even with --cacert /root/.ccr/ca-bundle.crt; verification was not disabled); www.britannica.com (403); doi.wiley.com (DNS); AGU DOI pages (JS wall); sciencedirect DOI (redirect to paywall retrieve page, no text).
- Proxy status showed recent ws_closed_mid_exchange failures for ncedc.org and repository.geologyscience.ru.

## 1. Harris et al. 2014 and Harris & Whiteway 2011

### 1.1 Harris et al. 2014, Marine Geology 352, 4-24 (GSFM) [B abstract]
- Source: https://grida.no/publications/318 (curl, abstract text).
- Quote: "continental shelf width of passive margins (88 km) is nearly three times that of active margins (31 km)".
- Quote: "the average width of active slopes (36 km) is less than the average width of passive margin slopes (46 km)".
- Quote: "active margin slopes contain an area of 3.4 million km2 where the gradient exceeds 5 deg, compared with 1.3 million km2 on passive margin slopes".
- Quote: "the continental rise covers 27 million km2 adjacent to passive margins and less than 2.3 million km2 adjacent to active margins".
- Quote: "The GSFM includes 131,192 separate polygons in 29 geomorphic feature categories".
- CORRECTION to notes: the notes said "25 katmanli harita" [O]. The abstract says 29 categories. Use 29.
- CORRECTION to notes: the 84 km passive shelf figure (second secondary summary) is wrong. The primary says 88 km. Drop 84.
- Confirmed: passive slope 46 km, active slope 36 km. Passive rise 27 M km2, active rise <2.3 M km2 (notes said "<2,3 milyon"; correct). Active 3.4 M km2 vs passive 1.3 M km2 slopes >5 deg (matches).
- Not verified: basin areas, canyon totals in Harris 2014. The "9477 canyons" figure is attributed to Harris 2014 in the notes. BULUNAMADI in the primary abstract; the full text is paywalled. Treat as unverified.
- DOI: https://doi.org/10.1016/j.margeo.2014.01.011 resolves to an Elsevier paywall redirect. Volume/pages 352, 4-24 come from the search summary [O] and the grida record. Not independently confirmed.

### 1.2 Harris & Macmillan-Lawler 2016, Springer chapter (SRTM30_PLUS shelf) [B]
- Source: https://link.springer.com/10.1007/978-3-319-25121-9_7 (curl, full abstract).
- Quote: "For the analysis the global shelf was divided into 551 reporting blocks, each approximately 500 km in along-shelf length."
- Quote: "characterizes around 21 % of the global shelf" (glacial trough share; the notes' "~%21 buzul" is correct).
- Quote: "covers 427,000 km2 or about 1.3 % of all continental shelves" (coral reef; notes' "%1,3" correct).
- Quote: "There is a negative correlation between shelf width and active plate margins".
- Reference list confirms: Harris & Whiteway 2011, Mar Geol 285:69-86 [B].

### 1.3 Harris & Whiteway 2011, Marine Geology 285, 69-86 [B abstract]
- Source: https://www.nespmarine.edu.au/document/global-distribution-large-submarine-canyons-geomorphic-differences-between-active-and.html (curl, abstract text).
- Quote: "Based on an analysis of the ETOPO1 data set, this study has compiled the first inventory of 5849 separate large submarine canyons in the world ocean".
- Quote: "Active continental margins contain 15% more canyons (2586, equal to 44.2% of all canyons) than passive margins (2244, equal to 38.4%)".
- Quote: "river-associated, shelf-incising canyons are more numerous on active continental margins (n = 119) than on passive margins (n = 34)".
- Quote: "the canyons are steeper, shorter, more dendritic and more closely spaced on active than on passive continental margins".
- Confirmed: notes' 5849 / 2586 / 2244 / 44.2% / 38.4% / 119 / 34 are correct.
- Canyon spacing vs slope: confirmed qualitatively (steeper canyons, closer spacing). No numeric spacing or density in the abstract (notes' "yogunluk BULUNAMADI" stands).
- Conflict 5849 (HW2011) vs 9477 (Harris 2014 DB, per notes): still unresolved. Different dataset (ETOPO1 vs SRTM30_PLUS?) is plausible but not confirmed.

### 1.4 Not verified from primary (1.x)
- Shelf-break depth, slope/rise gradients beyond the >5 deg threshold, feature-area totals for canyons and basins: BULUNAMADI in accessible sources.
- Bührig et al. 2022 morphometry: not fetched this pass.

## 2. Parsons & Sclater 1977 / Stein & Stein 1992 / comparisons

### 2.1 Parsons & Sclater 1977, JGR 82, 803-827 [B for citation, coefficients BULUNAMADI]
- Primary PDF (topex.ucsd.edu): DNS/no connection. AGU DOI page: JS wall. Coefficients were NOT read from the primary.
- Citation: EarthRef record lists DOI 10.1029/JB082i005p00802 [E]; Wikipedia reference lists 10.1029/jb082i005p00803 [E]. The EarthRef DOI is likely a typo (p00802 vs p00803). Use 00803 but flag.
- EarthRef abstract [E, https://earthref.org/ERR/43966]: "The simple cooling model predicts a linear relation between depth and t1/2... For larger ages these relations break down, and depth and heat flow dec[rease]..." This confirms the sqrt(t) regime and breakdown at older ages. It does not give 2500, 350, 3200, 6400 or 62.8.
- Wikipedia "Seafloor depth versus age" [E, https://en.wikipedia.org/wiki/Seafloor_depth_versus_age]: formula text was stripped in extraction, so coefficients could not be read from it. Its prose states:
  - "The cooling mantle model explains the age-depth observations for seafloor younger than 80 million years."
  - "The depth predicted by the square root of seafloor age found by the 1974 cooling mantle derivation is too deep for seafloor older than 80 million years."
  - For the cooling plate model (PS77, North Pacific): "~125 km for lithosphere thickness"; older seafloor "can be assumed almost constant at ~6400 m depth"; heat flow "approximately constant at beyond 120 million years".
  - Notes said "6400 m" and "125 km" (notes had 6400, and 125 km is in Wikipedia only). Consistent.
- Rowley (Univ. of Chicago) PDF [B, http://uchicago.cottagelabs.com/... (mirror of the paper PDF; original journal not confirmed from header; manuscript revised 6 Sep 2018)], quoted sentences:
  - "Parsons and Sclater (1977) showed that square root of age also arises from a plate cooling model (McKenzie, 1967)."
  - "if the maximum age of the half-space solution is limited to <84 Ma, then zr = -2388 m, and B = 354 ... These latter results are close to those of Parsons and Sclater (1977). The best-fit plate model has zr = -2309 m, zp = 122 km, and dT = 1304 C."
  - Meaning: an independent fit gives B ~ 354 m/Ma^1/2 and zr ~ -2.4 km, close to PS77. This supports ~350 m/Ma^1/2 for B. It is NOT the PS77 coefficient set itself. The 2500 m intercept in notes is not confirmed by this.
  - Sign convention: Rowley uses negative depths; magnitudes ~2.3-2.4 km.
- Notes' "0-70 Ma validity" is UNRESOLVED. Sources read: Wikipedia says the cooling mantle model is good below 80 Ma, plate model good beyond 20 Ma; search summary says ~70 Ma. Primary text not read.
- Exponential form 6400 - 3200 exp(-t/62.8): BULUNAMADI in primary. Only "~6400 m" asymptote is corroborated (Wikipedia [E]). Treat 3200 and 62.8 as unverified.
- Heat flow q(t)=11.3/sqrt(t): BULUNAMADI in primary.

### 2.2 Stein & Stein 1992, Nature 359, 123-129 [B abstract]
- Source: https://www.nature.com/articles/359123a0 (curl; article landing page, PDF returned HTML).
- Quote: "Joint fitting of heat flow and bathymetry yields a model with a hotter, thinner lithosphere than in previous models. The new model provides a significantly better fit to the data, including those from older lithosphere previously treated as anomalous."
- Citation: "Stein, C., Stein, S. A model for the global variation in oceanic depth and heat flow with lithospheric age. Nature 359, 123-129 (1992). https://doi.org/10.1038/359123a0" (reference on the Nature page) [B].
- GDH1 coefficients (2600 + 365 sqrt(t) below ~90 Ma, plus exponential form above): BULUNAMADI in any source read. Full text is paywalled; the Durham accepted manuscript (Stein_Accepted.pdf) that would contain them failed TLS trust. Do not use the task's values as verified.
- Secondary: EarthRef ERR/13140 and search summary (not read in full) report a ~90 Ma breakpoint attributed to Johnson & Carlson 1992 [O]: sqrt(age) fails for crust older than ~90 Ma.
- Rowley PDF Figure 19 caption [B]: compares "Stein and Stein (1992; thin gray dashed)" curve with other models; no coefficients given there. Rowley also notes the best-fit half-space/plate solutions are close to PS77.

### 2.3 Hasterok 2013 / Korenaga 2016 comparison (GDH1 vs PSM vs HSCM)
- Not searched in this pass. Korenaga 2008 PDF (people.earth.yale.edu) returned proxy 502 twice. Result: BULUNAMADI (not attempted in depth; next pass).

## 3. Strait and sill depths (Bab el-Mandeb, Suez, Gibraltar)

### 3.1 Bab el-Mandeb [E, https://en.wikipedia.org/wiki/Bab-el-Mandeb, curl]
- Quote: "The distance across is about 26 kilometres (14 nmi) from Ras Menheli in Yemen to Ras Siyyan in Djibouti."
- Table: "Min. width 16 mi (26 km)".
- Quote: "The eastern, known as the Bab Iskender ... is 5.37 kilometres (2.90 nmi) wide and has a depth of 29 metres".
- Quote: "The western, or Dact-el-Mayun, has a width of 20.3 kilometres (11.0 nmi) and a depth of 310 metres".
- The task values "137 m depth, 29 km width": NOT found. 29 m is Bab Iskender channel depth; 26 km is the narrowest width. Use 26 km if a width is needed. The "29 km" value appears to be a mix of numbers, not a source.
- Hanish sill depth: BULUNAMADI. Search summary [O] gives a qualitative "volcanic Hanish sill" and a 2025 Communications Earth & Environment paper (DOI 10.1038/s43247-025-02642-1) that is NOT read. Earlier notes' "163 m" and "~160 m" are from search excerpts [O], unverified.
- Red Sea reflooding: ~6.2 Ma (flood via Hanish sill, 320 km submarine canyon) per Springer Nature "Behind the paper" [O]. Not read in full.

### 3.2 Suez: sill depth BULUNAMADI.
- Wikipedia "Gulf of Suez" was fetched (3.7 KB); no sill depth was found in that article.

### 3.3 Gibraltar, Camarinal sill [E, https://en.wikipedia.org/wiki/Strait_of_Gibraltar, curl]
- Quote: "the erosion ... 900 m (3,000 ft; 490 fathoms) at the narrows, 280 m (920 ft; 150 fathoms) at the Camarinal Sill".
- Quote: "The Strait's depth ranges between 300 and 900 metres".
- Quote: "7.7 nautical miles (14.3 km; 8.9 mi) at its narrowest point."
- CORRECTION to notes: notes said 284 m; Wikipedia says 280 m. Both [E]. Primary (Wesson & Gregg 1994, JGR 99 C5; cited) not read.
- Reflooding at ~5.33 Ma (Zanclean) [E], consistent with notes.

## 4. Sclater & Christie 1980
- Citation: Christie, P.A.F. and Sclater, J.G. (1980), "Continental stretching: An explanation of the post-mid-Cretaceous subsidence of the central North Sea Basin," JGR 85, doi 10.1029/JB085iB07p03711 [O, EarthRef search summary].
- AGU DOI page: JS wall, not read.
- Subsidence curve coefficients: BULUNAMADI.
- Note: the notes' title "sahanlik cokme egrisi" is not the title of this paper. It concerns the North Sea Basin (post-mid-Cretaceous), not a generic continental shelf curve. Correct the note's description.

## 5. Corrections to existing notes (A_kenarlar.md, C_koprular_batimetri.md)
| Item | Notes said | Verified value | Source |
|---|---|---|---|
| Passive shelf width | 88 km and 84 km (conflict) | 88 km (primary) | grida 318 [B] |
| Active shelf width | 31 km | 31 km | grida 318 [B] |
| Passive / active slope width | 46 / 36 km | 46 / 36 km | grida 318 [B] |
| Rise area | 27 M km2 passive | 27 M km2 passive; <2.3 M km2 active | grida 318 [B] |
| Map category count | 25 layers | 29 categories, 131,192 polygons | grida 318 [B] |
| Shelf blocks | 551 (~500 km) | 551 blocks, ~500 km | Springer 2016 [B] |
| Canyon total | 5849 (HW11) | 5849 | NESP abstract [B] |
| Active/passive canyons | 2586 / 2244 | 2586 (44.2%) / 2244 (38.4%) | NESP abstract [B] |
| Shelf-incising canyons | 119 / 34 | 119 / 34 | NESP abstract [B] |
| Camarinal sill depth | 284 m | 280 m | Wikipedia [E] |
| Bab el-Mandeb width | 29 km (task) | narrowest 26 km; 29 m is Bab Iskender depth | Wikipedia [E] |
| Bab el-Mandeb depth | 137 m (task) | BULUNAMADI | none |
| PS77 DOI | (notes: 803) | 10.1029/JB082i005p00803 (Wikipedia); EarthRef gives 00802 | [E] |

## 6. Remaining BULUNAMADI (not found in any source read)
- Parsons & Sclater 1977 full coefficients (2500, 350, 3200, 62.8, 11.3) and validity range (70 vs 80 Ma). Needs JGR PDF or a reachable copy (topex.ucsd.edu blocked).
- GDH1 coefficients (Stein & Stein 1992). Needs Nature full text or Durham accepted PDF (TLS trust failure).
- Sclater & Christie 1980 subsidence coefficients. Needs JGR article (AGU JS wall).
- Hanish sill depth; Suez sill depth.
- Harris 2014 basin and canyon area totals; 9477 canyon count source.
- Hasterok 2013 / Korenaga 2016 GDH1 vs PSM vs HSCM comparison (not searched this pass; Korenaga 2008 PDF proxy 502).

## 7. Suggested next steps
1. Allow topex.ucsd.edu and people.earth.yale.edu in session network settings (WebFetch DNS for grida.no also failed; curl works). Re-run Parsons & Sclater fetch.
2. Allow mantleplumes.awh.durham.ac.uk with a valid chain, or fetch the Stein & Stein 1993 Geophysical Monograph chapter for GDH1.
3. Check Harris et al. 2014 full text via bluehabitats.org / GRID-Arendal data release (the GSFM data are CC-BY 4.0 per search summary [O]).
