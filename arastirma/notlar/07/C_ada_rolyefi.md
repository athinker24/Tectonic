# Relief and erosion on small mountainous islands: research notes

Status: complete for the reachable sources; open gaps listed in section 6.

Labels
- [B] primary source read (full text or abstract opened)
- [Ö] secondary: search-result summary or quoted second-hand, not opened
- [E] encyclopedia (Wikipedia, English)
- BULUNAMADI = not found in the sources reached

Access notes
- WebFetch returned DNS errors for nap.nationalacademies.org and www.doi.org. curl -sSL worked for both (nap.nationalacademies.org redirected to nationalacademies.org; doi.org redirected to nature.com). Text extracted with oku.py and pdftotext.
- ftp.ems.psu.edu (Fuller et al. 2003 PDF) failed TLS verification (certificate name mismatch). Not bypassed; the paper was not read.

---

## 1. Island area vs. highest elevation vs. relief

Values from English Wikipedia [E], fetched with curl and oku.py.

| Island | Area used here (km2) | Highest point (m) | Source note |
|---|---|---|---|
| Corsica | 8,680 (text) / 8,722 (infobox) | 2,706 (Monte Cinto) | "Monte Cinto as the highest peak at 2,706 m" [E]. Area conflict between text and infobox. |
| Sardinia | 24,100 | 1,834 (Punta La Marmora) | "area of 24,100 km2" and "highest peak is Punta La Marmora ... (1,834 m)" [E]. User value 24,090 is rounding. |
| Taiwan | 35,808 (main island) / 36,193 (168 islands) | 3,952 (Yu Shan) | "Yu Shan at 3,952 m" [E]. User value 36,000 is rounding of 35,808. |
| Crete | 8,450 (infobox and text) | 2,456 (Mount Ida / Psiloritis) | "Crete has an area of 8,450 km2" [E]. User value 8,336 NOT found in the page. |
| New Guinea | 785,753 | 4,884 (Puncak Jaya) | "area of 785,753 km2"; "Highest elevation 4,884 m" [E]. |
| South Island (NZ) | 150,437 | 3,724 (Aoraki / Mount Cook) | "Area 150,437 km2"; "Highest elevation 3,724 m" [E]. |

- Mean elevation or mean relief for these islands: BULUNAMADI in the sources read.
- Milliman & Syvitski 1992 [B] classify basins by maximum headwater elevation (high mountain >3000 m; mountain 1000-3000 m) and note that "a small island with elevations of 800-900 m probably should be considered mountainous."
- arXiv:2512.16659, "Self-Affine Scaling of Earth's Islands" [B, preprint, not peer reviewed], https://arxiv.org/html/2512.16659v1 (curl + oku.py): compiles elevation profiles of 131,063 islands spanning "8+ orders of magnitude" of area. Fits four scaling laws, including "maximum height-area relationship". Hurst exponent estimates differ by law ("The estimated Hurst exponents differ greatly"). The max-height exponent as a number: BULUNAMADI in the extracted text (only "a near-identical H was estimated" for that law). Paper notes the laws are "sorted in order of increasing expected influence of erosion at the shorelines."
- Relief-area scaling for small islands in the sense asked (ada alanı ile rölyef): only the arXiv preprint above; no peer-reviewed number found.

## 2. Coastal basins, river length, Hack's law

- Hack 1957 [B], USGS Professional Paper 294-B, https://pubs.usgs.gov/pp/0294b/report.pdf (curl, pdftotext). Abstract: stream length "(measured ... along the longest channel above the locality) increases directly as the 0.6 power of the drainage area. This rate of increase is not affected, except locally and for short distances, by the geology of the basin." Study basins: "between 0.12 and 375 square miles" (about 0.3 to 970 km2), Virginia and Maryland. So the original data include small basins, but not small islands.
- Wikipedia, "Hack's law" [E], https://en.wikipedia.org/wiki/Hack%27s_law (curl, oku.py): "the exponent h is slightly less than 0.6 in most basins"; "slightly decreases for larger basins (>8,000 mi2, or 20,720 km2)". Consistent with Hack 1957.
- Hack's law for small coastal or island basins: BULUNAMADI. Searches returned nothing on island or coastal-basin exponents.
- Basin area as a function of island width (geometric estimate): no source found; not quantified here.
- Small-basin yield example in the Milliman & Syvitski size range: Waiapu, East Cape, NZ. Catchment area 1,728 km2 and suspended sediment 35.07 Mt/yr in NIWA Hicks et al. 2011 table [B] (see section 3). Yield works out to about 20,300 t/km2/yr (my arithmetic: 35.07e6 / 1728).

## 3. Denudation rates (Taiwan, New Zealand, New Guinea)

Taiwan
- Dadson et al. 2003, Nature 426:648-651 [B], https://www.nature.com/articles/nature02150 (curl, oku.py). Abstract: "Estimated erosion rates within the actively deforming mountains are high (3-6 mm yr-1) on all timescales." Also: "The highest erosion rates are found where rapid deformation, high storm frequency and weak substrates coincide, despite low topographic relief."
- Fuller et al. 2003, J. Geol. 111:71-87 [Ö, search summary only; PDF not reached, see access note]: erosion rates "range from 2.2 to 8.3 mm/yr" for eastern Central Range basins.
- Hovius average surface lowering for Taiwan: 3.5 mm/yr [Ö, abstract quoted in search summary].
- Central Range, second-hand from Dadson et al. [Ö]: 2-8 mm/yr; about 5 mm/yr for the whole belt; local maxima above 30 mm/yr.
- In situ 10Be, area average 2.7 mm/yr; gauge-based estimates 3.7-6.7 mm/yr [Ö, search summaries, sources not identified]. Taroko-specific denudation rate: BULUNAMADI. One unattributed snippet gives uplift about 5.5 mm/yr and denudation roughly equal to uplift [Ö, no source; not verified].
- Milliman & Syvitski 1992 [B], https://nap.nationalacademies.org/read/1992/chapter/7 (curl, oku.py; reprint of J. Geol. 100:525-544): "Analysis of data from 280 rivers ... sediment loads/yields are log-linear function of basin area and maximum elevation." Small mountainous rivers "greatly underestimated in previous global sediment budgets, perhaps by as much as a factor of three." Oceania yields "probably >=3000 t/km2/yr." Mountainous rivers of about 10,000 km2 yield "between 140 and 1700 t/km2/yr." For basins below about 4,000 km2 the trend is "less pronounced"; "Some very small rivers in New Zealand and Taiwan ... have yields much lower than expected, while others have much higher yields."

New Zealand
- NIWA, Hicks et al. 2011 [B], https://www.niwa.co.nz/sites/default/files/Hicks_etal_2011_sediment_yields_from_NZ_rivers.pdf (curl, pdftotext): East Cape area has "the highest SSYs (~ 20,000 t/km2/y)". Table row: Waiapu, catchment 1728 km2, suspended sediment 35.07 Mt/y.
- NIWA Water & Atmosphere 11(4), 2003 [B], https://niwa.co.nz/sites/default/files/import/attachments/estimates.pdf (curl, pdftotext): East Cape suspended yields "up to 20,000 t/km2/y"; the region "is 6% of the area of North Island" but "accounts for 58% of the sediment yield"; "lowering of the land surface in the region by ... approximately 7.5 mm each year." Note: this is suspended sediment converted to a lowering rate by NIWA. It is not a direct denudation measurement.
- Kniskern et al. 2009: Waiapu 17,800 t/km2/yr [Ö, search summary only].
- Southern Alps cosmogenic denudation (Zenodo table "Table2 new CRN data", https://zenodo.org/records/7950735/files/Table2_new_CRN_data.pdf, [Ö], not peer reviewed, not opened): Whataroa 5.20 +/- 1.22 mm/yr; Hokitika 5.87 +/- 1.32 mm/yr. Larsen et al. 2014 Whataroa 6.6 +/- 1.7 mm/yr and Herman et al. 2010 exhumation 8.7 +/- 1.3 mm/yr [Ö, from a summary].
- The user's claim "NZ 1-10 mm/yr": partly supported by a search summary giving "generally range between 0.6 and 9 mm/yr" for western Southern Alps 10Be catchments and a claim of "can exceed 10 mm/yr" [Ö]. Not confirmed from a primary source. Specific NZ-vs-Taiwan comparison: BULUNAMADI.

New Guinea / Papua New Guinea
- Ruxton & McDougall 1967, Am. J. Sci. 265:545-561, "Denudation rates in northeast Papua from potassium-argon dating of lavas": the paper exists (bibliography); the rate values were NOT retrieved. BULUNAMADI for Hydrographers Range rates.
- Suckling-Dayman complex (PNG), 10Be in quartz: 0.02-0.18 mm/yr [Ö, GRL Oct 2024 summary].

## 4. Orographic precipitation and rain shadow (Southern Alps)

West coast, 1981-2010 normals, NIWA West Coast Climatology [B], https://www.niwa.co.nz/sites/default/files/West_Coast_Climatology_NIWA_web.pdf (curl, pdftotext -layout). Summary: "Annual rainfall totals at relatively high elevations regularly exceed 10,000 mm, with low elevation coastal locations typically recording between 2,000 and 3,000 mm." Table 6 annual normals (mm/yr): Cropp River 11,400; Tuke River 10,558; Lake Paringa 5,588; Franz Josef 5,751; Lake Moeraki 4,301; Kopara 2,995; Seddonville 2,813; Hokitika 2,732; Greymouth 2,452; Inangahua 2,433; Westport 2,046; Reefton 1,943; Karamea 1,868. Station elevations are not given in the extracted table; they were not checked.

East side, 1981-2010 normals, NIWA Canterbury Climatology [B], https://niwa.co.nz/sites/default/files/Canterbury%20climate%20FINAL%20WEB_0.pdf (curl, pdftotext -layout), Table 6 (mm/yr): Arthur's Pass 4,642; Mt Cook Village 4,285; Methven 895; Akaroa 969; Castle Hill Village 967; Ashburton 681; Rangiora 688; Kaikoura 721; Darfield 756; Waipara 620; Christchurch 618; Culverden 576; Lake Tekapo 591; Timaru 550; Waimate 536; Tara Hills (Omarama) 506. Row-to-station mapping was checked against the layout (label follows its annual row); a manual check is advisable before quoting one station.
- NIWA Canterbury summary [B]: "rainfall is highest along the main divide which has both high elevation and western exposure. This is the result of orographic enhancement."
- Contrast: Franz Josef (5,751) and Hokitika (2,732) against Lake Tekapo (591), Christchurch (618), Omarama (506): roughly 8-10x between west coast and east basins. Mt Cook Village, on the eastern (Canterbury) side of the divide, is 4,285 mm, so the pattern is closer to divide proximity and elevation than to a simple west-east line.
- Rain-shadow description: Te Ara / NIWA map [E/Ö, search summary]: eastern areas "about 100 km away sit in a rain shadow." Milford Sound "almost 7 metres of rainfall a year" (NIWA lesson page [Ö, search summary]).
- Hokitika transect: maxima "7-11 km southeast of the New Zealand Alpine Fault" (rain-gauge transect study at Hokitika, Franz Josef and Haast) [Ö, search summary; paper not opened].
- West-east gradient in mm per km: BULUNAMADI. Station distances were not sourced, so no gradient value was computed.

## 5. Coastal plain to mountain ratio on islands

- Coastal plain fraction or hypsometry for small islands: BULUNAMADI.
- Nearest sources, both not about coastal plains: Klein et al. 2023, Frontiers in Marine Science, 47 volcanic islands, 24 geomorphometric parameters [Ö, search summary; abstract not opened]; arXiv:2512.16659 (section 1) [B, preprint].
- Suggested next queries: "hypsometric integral oceanic islands", "coastal lowland fraction island area".

## 6. Conflicts and open gaps

Conflicts (side by side)
- Taiwan denudation: Dadson 2003 "3-6 mm/yr" [B] vs Dadson as cited "2-8" (Central Range) and "about 5" (belt) [Ö] vs Fuller 2003 "2.2-8.3" [Ö] vs Hovius "3.5" [Ö] vs in situ 10Be 2.7 [Ö] vs gauge 3.7-6.7 [Ö]. Method and timescale differ: gauge (decadal), cosmogenic (centuries to millennia), thermochronometry (Myr).
- NZ Waiapu sediment yield: NIWA 2003/2011 about 20,000 t/km2/yr [B] vs Kniskern 2009 17,800 [Ö]. Different methods and years.
- NZ Southern Alps rates: cosmogenic Whataroa 5.2 (dataset, [Ö]) vs Larsen 2014 6.6 [Ö] vs Herman 2010 exhumation 8.7 [Ö]. Timescales differ.
- Oceania yield assumptions: Milliman & Meade 1983 used 1000 t/km2/yr [B text in MS1992]; MS1992 says Oceania "probably >=3000" [B].
- Island areas: Corsica 8,680 vs 8,722 [E]; Crete 8,336 (user) vs 8,450 [E]; Sardinia 24,090 (user) vs 24,100 [E]. Taiwan 36,000 (user) vs 35,808 main island / 36,193 with islands [E].
- Hack exponent: 0.6 [B] vs "slightly less than 0.6 in most basins" [E]. Consistent; the difference is rounding.
- West-east precipitation: simple west-east gradient vs Mt Cook Village 4,285 mm on the eastern side of the divide [B]. Elevation and divide proximity matter more than longitude.

Open gaps
- Mean or average relief for each island (BULUNAMADI).
- Hack's law exponent for small coastal basins or islands (BULUNAMADI).
- Basin area as a function of island width (no source).
- Taroko-specific denudation rate in a primary source (BULUNAMADI).
- Ruxton & McDougall 1967 rate values (BULUNAMADI).
- Southern Alps 1-10 mm/yr range from a primary source (not confirmed).
- Milliman & Syvitski 1992 Table 1 (individual river yields for NZ, Taiwan): not present in the NAP text extract; BULUNAMADI at the row level.
- Coastal plain fraction (BULUNAMADI).
- Fuller et al. 2003 full text: blocked by TLS name mismatch on ftp.ems.psu.edu (not bypassed).
- Station elevations for NIWA precipitation tables (not in extract).

## 7. Source list

Primary [B]
- Milliman & Syvitski 1992, J. Geol. 100:525-544, reprint: https://nap.nationalacademies.org/read/1992/chapter/7
- Dadson et al. 2003, Nature 426:648-651: https://www.nature.com/articles/nature02150
- Hack 1957, USGS PP 294-B: https://pubs.usgs.gov/pp/0294b/report.pdf
- NIWA Hicks et al. 2011 (NZ sediment yields): https://www.niwa.co.nz/sites/default/files/Hicks_etal_2011_sediment_yields_from_NZ_rivers.pdf
- NIWA 2003, Water & Atmosphere 11(4) estimates: https://niwa.co.nz/sites/default/files/import/attachments/estimates.pdf
- NIWA West Coast Climatology: https://www.niwa.co.nz/sites/default/files/West_Coast_Climatology_NIWA_web.pdf
- NIWA Canterbury Climatology: https://niwa.co.nz/sites/default/files/Canterbury%20climate%20FINAL%20WEB_0.pdf
- arXiv:2512.16659 (preprint): https://arxiv.org/html/2512.16659v1

Encyclopedia [E]
- https://en.wikipedia.org/wiki/Corsica
- https://en.wikipedia.org/wiki/Sardinia
- https://en.wikipedia.org/wiki/Taiwan
- https://en.wikipedia.org/wiki/Crete
- https://en.wikipedia.org/wiki/New_Guinea
- https://en.wikipedia.org/wiki/South_Island
- https://en.wikipedia.org/wiki/Hack%27s_law

Secondary [Ö] (search summaries, not opened)
- Fuller et al. 2003, J. Geol. 111:71-87
- Hovius et al. 2000, J. Geol.; Hovius 3.5 mm/yr figure
- Kniskern et al. 2009 (Waiapu 17,800 t/km2/yr)
- Zenodo CRN table: https://zenodo.org/records/7950735/files/Table2_new_CRN_data.pdf
- Larsen et al. 2014; Herman et al. 2010 (cited in a Whataroa study summary)
- Ruxton & McDougall 1967 (reference only)
- Suckling-Dayman 10Be study, GRL Oct 2024
- Klein et al. 2023, Frontiers in Marine Science, 10.3389/fmars.2023.1259262
- Te Ara mean annual rainfall map and NIWA lesson 7 (Milford Sound value)
