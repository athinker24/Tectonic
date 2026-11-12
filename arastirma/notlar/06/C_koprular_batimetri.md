# C: Land bridges, straits and bathymetry generation (working notes)

Status: in progress. Labels: [B] primary source read, [O] search-summary only, [E] encyclopedia.
Conflicting numbers are listed side by side. Quotes are kept short.

## 1. Land bridges and straits

### 1.1 Panama Isthmus closure date (conflict)
- [O] Conventional view, about 3 Ma. O'Dea et al. (2016, Science Advances, Smithsonian STRI) defended the ~3 Ma age using multiple lines of evidence and refuted the 2015 early-closure papers. Source: https://www.earthmagazine.org/article/panamas-isthmus-stays-3-million-years-young-further-evidence-needed-support-older-age/ (secondary) and https://maritime-executive.com/corporate/new-study-reaffirms-timeline-on-formation-of-isthmus-of-panama
- [O] Older view, 13-15 Ma. Montes et al. (2015, Science) used detrital zircon: beds younger than ~13-15 Ma contain Panama-type zircon, older beds do not. Authors read this as the docking time, "nearly 10 million years before" the traditional closure. Source: https://www.sciencedaily.com/releases/2015/04/150409182955.htm
- [O] Middle claim, 15 Ma. Coates & Stallard (2013) proposed closure at 15 Ma: by then the block alignment leaves no space for trans-isthmian marine passages. Standard model places final closure at 4-3 Ma. Source: https://phys.org/news/2015-04-smithsonian-panama-debate-fueled-zircon.pdf (secondary)
- [O] Jaramillo (Smithsonian) suggests part of the disagreement is that closure was not a single event (first contact vs final closure). Source: https://www.sciencenews.org/?p=20601
- Note: the 15-20 Ma figure in the task is not clearly supported by the search results I saw. The 13-15 Ma figure is the older value found. Still to check: whether any source gives 15-20 Ma exactly.

## 2. Bathymetry formulas

### 2.1 Parsons & Sclater (1977) [O, OCR text from two extractions]
- d(t) = 2500 + 350 * sqrt(t) m, t in Ma. Source: J. Geophys. Res. 82, 803-827. PDF: https://topex.ucsd.edu/geodynamics/parsons_sclater77.pdf ; index: https://en.wikipedia.org/wiki/Seafloor_depth_versus_age
- Stated validity: 0-70 Ma (per paper, per search excerpt). Other sources give 70-90 Ma or 80 Ma. CONFLICT on cutoff.
- Older crust (>20 Ma): d(t) = 6400 - 3200 * exp(-t/62.8) m (same paper, per excerpt). Note: this is the exponential form, which Parsons & Sclater used for older seafloor.
- Heat flow: q(t) = 11.3 / sqrt(t) microcal cm^-2 s^-1 (same paper).
- Data basis: North Pacific and North Atlantic. Yale paper (Korenaga 2008) attributes ~350 m Ma^-1/2 to P&S 1977. Source: https://people.earth.yale.edu/sites/default/files/korenaga08b.pdf
- Not yet verified from the full paper text. Planned: WebFetch of the PDF.

## 3. GEBCO

### 3.1 GEBCO_2024 grid [O]
- 15 arc-second grid, released July 2024. 43200 rows x 86400 columns (3,732,480,000 points). Cell-centre referencing.
- Base: SRTM15+ v2.6 between 50 S and 60 N; GMTED2010 north of 60 N for land.
- Storage: NetCDF, 2-byte integers, metres. Citation DOI: 10.5285/1c44ce99-0a0d-5f4f-e063-7086abc0ea0f. Source: https://www.gebco.net/data-products-gridded-bathymetry-data/gebco2024-grid and https://www.gebco.net/sites/default/files/documents/GEBCO_grid_2024.pdf
- Conflict: atlas.co gives ~450 m at equator (15 arc-second is ~450 m N-S). Consistent. Its claim "about 25% seafloor mapped by multibeam" is NOT corroborated by GEBCO pages. Do not use it.

## 4. Messinian salinity crisis and Gibraltar

### 4.1 Timing [O]
- Crisis 5.97-5.33 Ma. Stage 1 (gypsum onset) 5.97-5.60 Ma. Sources: https://www.futura-sciences.com (secondary) ; Krijgsman et al. 2024 PDF: https://gis.geoecomar.ro/pnrr/wp-content/uploads/2025/07/Krijgsman_24_NREE.pdf (not yet read)

### 4.2 Gibraltar gateway (conflict)
- One view: Gibraltar closed, breached only at ~5.33 Ma.
- Krijgsman et al. (2018, Marine Geology, "The Gibraltar Corridor: Watergate of the Messinian Salinity Crisis"): Gibraltar was most likely open for most of the MSC. Rifian corridors also proposed. No sill depth found in search.
- Modern Camarinal sill: 284 m deep; Tarifa narrows 14.3 km wide. Source: search summary (no URL captured). Treat as [O].
- End-of-crisis level: Mediterranean ~1 km below Atlantic (one source, [O]).

## 5. Still open
- Suez, Bering, Bab el-Mandeb, Bosphorus sill depth/width data.
- Sea-level sensitivity: shelf area per 120 m drop; coastline shift.
- Stein & Stein (1992), GDH1 (Stein & Stein's depth-age).
- Ridge height, fracture zones, seamount counts.
- Smith & Sandwell grid resolution and seamount method.
- Synthetic bathymetry methods.

## Access note (added)
- WebFetch failed (DNS, host not in allowed network list): topex.ucsd.edu, www.nature.com, www.gebco.net. Per tool message, not retried. Primary PDFs (Parsons & Sclater 1977; Stein & Stein 1992 Nature; GEBCO docs) are therefore NOT read directly. All their figures below come from search excerpts and are labelled [O].

## 1. Additional land bridge / strait findings

### 1.2 Bering Strait / Bering land bridge
- [O] Present narrowest width ~85 km, between Cape Prince of Wales and Cape Dezhnev. Source: https://www.britannica.com/place/Bering-Strait ; https://worldatlas.com/straits/bering-strait.html
- [O] Present depth: Britannica 30-50 m average; WorldAtlas 50 m average, 90 m max. CONFLICT on maximum. These are today's strait, not the exposed land bridge.
- [O] Sea level fell "several hundred feet" in the Ice Age; migration dated ~20-35 ka (Britannica). No sill depth for the exposed land bridge found.

### 1.3 Bab el-Mandeb
- [O] Conflicting numbers: task figures 137 m depth and 29 km width NOT found in any source. Found: Hanish sill 163 m (one oceanographic paper) and ~160 m (another paper). Narrowest commonly ~26 km (encyclopedia). Source: https://en.wikipedia.org/wiki/Bab-el-Mandeb ; https://www2.whoi.edu/staff/lpratt/wp-content/uploads/sites/120/2019/07/JPO1999_2911_2769_2784_10134.pdf (Pratt 1999, J. Phys. Oceanogr. 29, 2769-2784; search excerpt only, not read).
- [O] Perim Island splits strait into two channels. Bab Iskender ~3.2 km wide, ~29 m deep (channel depth, not sill). Dact-el-Mayun ~26 km wide, ~310 m deep (per encyclopedia, fathom conversion; treat with caution).
- Reported: 137 m / 29 km unverified. Ask user for source if they have one.

### 1.4 Bosphorus
- [O] Minimum width ~700 m; strait length ~30 km; ~3.4 km wide at north outlet, 2.8 km at south inlet. CONFLICTING sill depths: 27 m (south entrance), ~35 m near Istanbul (deepest >110 m), ~40 m (Bosphorus) and ~70 m (Dardanelles). Source: search overview only (ancientportsantiques Lericolais 2019 PDF listed but not read).
- [O] Reconnection timing: IMI ~8.9-8.5 ka BP or 9.3-9.0 ka BP (one review); earlier exchange ~10.5-9 ka BP (another). 2003 hydraulic study dated salinification to 10.2-9.6 ka BP and found a deep-sill catastrophic flood unlikely. Later work argues slow, progressive reconnection.

### 1.5 Suez / Red Sea-Mediterranean link
- [O] Sill depth: NOT found.
- [O] Early Messinian: Red Sea isolated from Mediterranean; northern Gulf of Suez connection restricted before ~6.2 Ma (2022-era study, source: https://cp.copernicus.org/articles/11/233/2015/cp-11-233-2015.pdf is a 2015 Climate of the Past paper and was listed in search, but the 6.2 Ma statement came from a different result; treat as [O] with no URL verified).
- [O] Gargani et al. (2008, GRL) link Gulf of Suez evaporites to a threshold that disconnected Red Sea from E. Mediterranean at end of Miocene. No sill depth in abstract.
- [O] Red Sea reflooded from the south via a 320 km submarine canyon through the Hanish sill, ~1 Ma before Zanclean flood. Source: https://communities.springernature.com/posts/behind-the-paper-how-the-red-sea-dried-up-and-flooded-back
- Note: Suez "Panama-like" closure age is not given; no precise Suez closure date found.

### 1.6 Gibraltar (added to 4.2)
- Krijgsman et al. (2018) argue Gibraltar was "most likely open during most of the MSC"; Rifian corridors proposed. Sill depth NOT found in search. Check Krijgsman 2018 (Marine Geology) for strait-dynamics estimates.

## 2. Parsons & Sclater / Stein & Stein (additional)
- [O] Stein & Stein (1992) Nature 359, 123-129, "A model for the global variation in oceanic depth and heat flow with lithospheric age." Abstract claim: joint fit of heat flow and bathymetry gives hotter, thinner lithosphere than earlier models. GDH1 coefficients NOT verified in search.
- [O] Sqrt(age) law: a 1992 GRL test (search excerpt) reports sqrt(t) fails for crust older than ~90 Ma. Source excerpt; paper not identified precisely.
- Still to verify: GDH1 ridge depth (~2.6 km per the task; not confirmed) and cutoff ~90 Ma.

## 3. Smith & Sandwell (1997)
- [O] Citation: Science 277, 1956-1962. Merges ship soundings with altimetry-derived gravity (ERS-1, GEOSAT). Gravity RMS 3-5 mGal, resolution ~20-30 km wavelength. Coverage ice-free ocean within +/-72 deg.
- [O] "1 arc-minute" grid resolution NOT confirmed in search excerpts. Task claim stands unverified.
- [O] Seamount detection threshold ~2 km (Nature news 2014 summary). Wessel et al. (2010) give ~1.5 km.
- [O] Etnoyer (2005): model generally 192 m (+/-132) deeper than multibeam for 13 NE Pacific seamounts; small-feature height error up to 50%. Source: search excerpt.

## 4. Seamount counts (conflicting)
- [O] Wessel (2001) table: 11,882 unique seamounts (15,675 original entries with duplicates).
- [O] Hillier & Watts (2007): >200,000 seamounts >100 m high (track-line data). Cited in Wessel et al. 2010, Oceanography.
- [O] Kim & Wessel (2011, GJI) altimetry-gravity census: 40,000-55,000. A SOEST news item gives >24,000 for the same method. UNRESOLVED.
- [O] Yesson et al. (2011, DSR-I) 30-arc-sec bathymetry: 33,452 seamounts; 138,412 knolls. Notes overestimate along ridges.
- [O] Yesson & Letessier (UCL, date unconfirmed): SRTM30_PLUS v11, >4000 new predictions; flags 15 phantom features.
- 2014 Yesson total: NOT found.

## 5. Sea-level sensitivity (sourced + my calculation)
- [O] LGM fall ~120 m (Sunda shelf exposed) or ~116 m (other). Source: https://wikipedia.com/wiki/Sundaic ; https://pmc.ncbi.nlm.nih.gov/articles/PMC6291310
- [O] Sundaland ~1.8 million km^2 maximum extent. Modern land roughly half of max (implies ~doubling; inference by me).
- [O] Sahul (Australia excl. New Guinea): LGM 9.80 Mkm^2 vs early Holocene 7.68 Mkm^2 (drop 2.12 Mkm^2, ~21.6%). Source: https://ui.adsabs.harvard.edu/abs/2018QSRv..182..144W/abstract (Ward et al. 2018, QSR 182, 144). LGM is ~28% larger than the Holocene value (my calc).
- Sunda exact percentage: NOT found; Thai study table (Chulalongkorn 2006) listed but not read.

## 6. Sea-level sensitivity: parametric calculation (my calc, not sourced)
Model: shelf locally planar with constant slope s, drop D = 120 m. Horizontal shoreline shift = D / s. Area gained per unit coastline length = D / s (linear shelf, no curvature, no new islands, ignores crossing of basins).
Result (per 1000 km of coastline):

| slope s | shoreline shift | area gained per 1000 km coast |
|---|---|---|
| 1:2000 | 240 km | 240,000 km^2 |
| 1:1000 | 120 km | 120,000 km^2 |
| 1:500 | 60 km | 60,000 km^2 |
| 1:200 | 24 km | 24,000 km^2 |
| 1:100 | 12 km | 12,000 km^2 |

Check against the Sahul figure: [O] LGM Australia (excl. New Guinea) gained about 2.1 Mkm^2 relative to Holocene. The parametric model is only a sanity check; real shelves are not planar and their slopes vary by region. Use real bathymetry (ETOPO/GEBCO) to get exact numbers.

## 7. Ridge and synthetic bathymetry (additional)
- [O] Average crest depth: ~2,700 m (one source, search excerpt). Task said ~2.5 km: NOT exactly confirmed; sources differ slightly.
- [O] Slow spreading rift valleys ~1-3 km deep at 10-40 mm/yr. Fast spreading axial highs ~300-400 m tall. Source: Macdonald, "Mid-Ocean Ridge Tectonics" (PDF listed: https://macdonald.faculty.geol.ucsb.edu/papers/Macdonald Mid-Ocean Ridge Tectonics.pdf, not read).
- [O] Synthetic bathymetry, Goff & Jordan (1989): stationary zero-mean Gaussian random field; anisotropic model with 5 free parameters (amplitude, orientation, aspect ratio, characteristic length, fractal dimension); Fourier generation. Source: https://tos.org/oceanography/assets/docs/17-1_goff.pdf (listed, not read).
- [O] SYNBATH (Sandwell and colleagues, NOAA repository): uses seafloor age and fossil spreading rate/orientation to generate abyssal hill realizations; seamount masses from vertical gravity gradient plus a characteristic shape. Covers ~80% of seafloor that is gravity-predicted only. Source: https://repository.library.noaa.gov/view/noaa/49319
- [O] Fracture zones: NOT covered in search results. Needs dedicated search.

## 8. Panama: 15-20 Ma check
- No source gives exactly 15-20 Ma closure. Closest:
  - [O] Montes et al. 2015 (Science), zircon: 13-15 Ma docking. Source: https://www.sciencedaily.com/releases/2015/04/150409182955.htm
  - [O] Bacon et al. 2015 (PNAS), molecular divergence pulses 23-20 Ma and 8-6 Ma; broader closure window 23-7 Ma. Source: pmc link https://pmc.ncbi.nlm.nih.gov/articles/4434730 (listed, not read).
  - [O] O'Dea et al. 2016 and Texas A&M study: ~3 Ma (2.8 Ma). Source: https://news.galveston.tamu.edu/2016/08/19/new-study-reaffirms-timeline-on-formation-of-isthmus-of-panama/
  - [O] Lamont-Doherty overview: window 15 to 3 Ma. Source: https://lamont.columbia.edu/news/isthmus-panama-out-deep-earth
- So "15-20 Ma" is best described as the older camp's range, with Bacon et al. providing 20-23 Ma molecular signal as a separate line.

## Status summary
- Sections 1-8 contain findings. Unresolved: Suez sill depth; Gibraltar Messinian sill depth; Bab el-Mandeb 137 m / 29 km; GDH1 exact coefficients; Smith & Sandwell 1 arc-min; fracture zone methods; Sunda exact % gain; Yesson 2014 total.
- Primary sources not read directly due to network: Parsons & Sclater 1977 PDF, Stein & Stein 1992, GEBCO page.
