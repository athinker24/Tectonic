# B: Endorheic basins, closed-basin lakes, spillover, and lake modelling

Status: COMPLETE (first pass). Items marked BULUNAMADI were not found in accessible text.

Labels: [B] full text read; [B-öz] summary/article text read; [Ö] search snippet only.

Access notes:
- WebFetch failed with DNS errors for nature.com, arxiv.org and hydrosheds.org. curl through the proxy worked for these, and the text was extracted with oku.py. Full texts were read this way.
- Lehner & Döll (2004) PDF: connection reset on two attempts. ERİŞİLEMEDİ for full text; search snippet only [Ö].
- Fastscapelib flow guide (guide_flow.md.txt): fetch returned 0 characters. Source only [Ö].
- LakeMapperBarnes source file (landlab GitHub): not reached. Docs page read via search [Ö].
- Caspian–Manych paper (Cambridge Radiocarbon 2025, Limnol. Fish. Water Biol. 2026): search snippet only [Ö].

## Topic 1: Endorheic (closed) basins, area and examples

- Global endorheic share of land: about 18% (Wikipedia "Endorheic basin": "Approximately 18 per cent of the Earth's land drains to endorheic"). [B-öz] https://en.wikipedia.org/wiki/Endorheic_basin
- "All endorheic basins comprise about 20% of the global land area." Scientific Data, MERIT-Plus paper, 2023. [B] https://www.nature.com/articles/s41597-023-02875-9 (note: this paper cites a reference for the 20% figure that I could not confirm as Lehner & Döll 2004.)
- Regional shares: Australia 21%, North America 5% (Wikipedia Endorheic basin). [B-öz] same URL as above.
- Global endorheic area 32.67 million km², 2002–2016 (table in a 2024 study of endorheic water storage) [Ö]. Source: https://pmc.ncbi.nlm.nih.gov/articles/PMC6267997/table/T1 (not verified; BULUNAMADI for the exact table context).
- Watershed draining to shrinking endorheic and exorheic lakes: 18% of land area (Earth's Future, 2020) [Ö] https://doaj.org/article/325df9e3ace148e4b051121724a40201
- Tarim Basin: about 888,000 km²; endorheic; largest basin in NW China. [B-öz] https://en.wikipedia.org/wiki/Tarim_Basin
- Tarim sedimentary fill: "thick succession of Paleozoic, Mesozoic and Cenozoic sedimentary rocks ... locally exceeding thicknesses of 15 km." [B-öz] Wikipedia Tarim Basin. Note: the user's guess of 5–15 km is below the reported local maximum. This is an article-level summary, not a primary seismic study. A primary source for the average thickness is BULUNAMADI.
- Gobi Desert: area 1,295,000 km². [B-öz] https://en.wikipedia.org/wiki/Gobi_Desert
- Great Basin: 541,730 km² total; largest contiguous endorheic area in North America; lowest point Badwater Basin, −86 m (−282 ft). [B-öz] https://en.wikipedia.org/wiki/Great_Basin
- Caspian Sea: gross area 386,400 km²; surface about 27–28 m below sea level (−28 m stated in infobox); deepest south basin 1,023 m below sea level; endorheic; landlocked since Late Miocene ~5.5 Ma. [B-öz] https://en.wikipedia.org/wiki/Caspian_Sea
- Aral Sea: 68,000 km² (1960) → 17,160 km² (2004). Surface elevation 53.4 m (1960), 42 m (north, 2011), 29 m (south, 2007). [B-öz] https://en.wikipedia.org/wiki/Aral_Sea
- Lake Balkhash: 16,400 km² (2000); surface about 341 m a.s.l.; length ~600 km. [B-öz] https://en.wikipedia.org/wiki/Lake_Balkhash
- Altiplano: average elevation about 3,750 m; endorheic; parts of Chile, Bolivia, Peru, Argentina. [B-öz] https://en.wikipedia.org/wiki/Altiplano
- Lake Bonneville (Great Basin): maximum depth over 300 m (980 ft); area almost 51,000 km² at maximum; highest (Bonneville) shoreline reached ~17,500 years ago. [B-öz] https://en.wikipedia.org/wiki/Lake_Bonneville

## Topic 2: Origin of closed basins, sediment, spillover

Origin:
- Tarim closure: basin became a closed continental sedimentary basin in the Cenozoic due to uplift of the western Kunlun, Tian Shan and Altyn Tagh ranges; flexural model suggests uplift ~26–13 Ma and rapid uplift since ~5 Ma. [Ö] Basin-modelling study, 2020 (search results from aminer.org and research.ed.ac.uk; exact URL not recorded).
- Tian Shan barrier created a rain shadow in the NW Tarim; a Pamir–Tian Shan barrier established ~25 Ma in one framework. Estimates differ from Oligocene to late Miocene. [Ö]
- Caspian: endorheic since Late Miocene (~5.5 Ma) through tectonic uplift and sea-level fall. [B-öz] Wikipedia Caspian Sea.

Spillover and overflow examples:
- Caspian–Black Sea: early Khvalynian maximum at +48–50 m a.s.l. (traditional), "almost 80 m above the current Caspian Sea level", sea area 940,000 km² (2.5× current). [B] Hydrology paper, HESS 28, 241–2024 https://hess.copernicus.org/articles/28/241/2024/hess-28-241-2024.html
- Same HESS paper: "After the maximum level was reached, there was a breakthrough of the Caspian into the Manych Depression, which caused a westward flow into the Black Sea." [B] same URL.
- Spillway threshold disagreement: 2026 modelling gives max level ~40 m a.s.l. and spillway threshold at 31 m a.s.l.; Svitoch & Makshaev suggested threshold 45–50 m. [Ö] Limnological Fisheries and Water Biology 2026 and Cambridge Radiocarbon 2025 (search snippets only).
- Last Manych overflow ended ~14.5 ka cal BP (radiocarbon, Semikolennykh et al.); OSL dates suggest older. [Ö]
- Black Sea as former endorheic lake overflowing into Mediterranean. [B-öz] Wikipedia "Endorheic basin": "The Black Sea was likely such a lake ... before the Mediterranean Sea broke through."
- Lake Bonneville: overflowed Red Rock Pass into Snake River drainage; Bonneville flood lowered lake level by about 125 m (410 ft). The Provo shoreline formed during the overflowing phase. Lake later returned to closed status ~16.5 ka. [B-öz] Wikipedia Lake Bonneville and Endorheic basin.
- Malheur/Harney (Oregon): normally closed, has an outflow channel when high. [B-öz] Wikipedia Endorheic basin.
- Lake Tulare (California): endorheic in dry years, overflows in wet years. [B-öz] Wikipedia Endorheic basin.
- Lake Winnipeg: large non-contributing area in basin. [B-öz] same.

Spillover (general): "Overflow" follows when lake water level reaches the lowest point on the basin rim (Bonneville case). [B-öz] Wikipedia Lake Bonneville.

Sediment thickness:
- Tarim >15 km locally. See Topic 1.
- Endorheic basins as local base levels that limit erosion and deposition. [B-öz] Wikipedia Endorheic basin.
- Caspian Sea total sediment thickness: BULUNAMADI (not found in accessible text).

Lake area–volume relation:
- Explicit area–volume formula in a closed-basin lake: BULUNAMADI in accessible text. See Messager (Topic 4) for a depth model.

## Topic 3: Lake modelling (priority flood and sinks)

- Priority-Flood algorithm: floods DEMs inwards from edges using a priority queue; result has "no depressions or digital dams: every cell is guaranteed to drain." Time: O(n) for integer data, O(n lg n) for floating-point; O(m lg m) variant with plain queue, "the lowest time complexity of any known floating-point depression-filling algorithm." [B] arXiv 1511.04463 abstract https://arxiv.org/abs/1511.04463 (submitted 13 Nov 2015)
- Barnes, Lehman & Mulla, "Priority-Flood: An Optimal Depression-Filling and Watershed-Labeling Algorithm for Digital Elevation Models," Computers & Geosciences 62 (2014), pp. 117–127. [Ö] Citation from search snippet.
- Spillover definition: "lowest point where two watersheds meet"; spillover graph connects watersheds. [Ö] Secondary source; exact wording in the 2014 paper not read.
- Landlab LakeMapperBarnes (current name in docs: lake_fill component, class LakeMapperBarnes / lake_fill_barnes): "Fill sinks in a landscape to the brim, following the Barnes et al. (2014) algorithms." Outputs include lake_areas (area per lake), lake_outlets, and lake_dict. Warns that it overwrites fill_surface unless given a surface field. [Ö] https://landlab.readthedocs.io/en/latest/reference/components/lake_fill.html and https://landlab.readthedocs.io/en/latest/generated/api/landlab.components.lake_fill.lake_fill_barnes.html
- Landlab SinkFiller (sink_fill): permanently fills pits; not for repeated use during model run (use LakeMapperBarnes for that). [Ö] https://csdms.colorado.edu/wiki/Model:SinkFiller
- Fastscapelib PFloodSinkResolver (C++ name pflood_sink_resolver): priority-flood +epsilon variant [BLM14]. Epsilon avoids flat surfaces so flow can reach outlets. Modifies elevation but not the flow graph (graph_updated = false, elevation_updated = true). MST sink resolver updates both. [Ö] https://fastscapelib.readthedocs.io/en/latest/api_python/_api_generated/fastscapelib.PFloodSinkResolver.html
- Water balance (precipitation − evaporation) for closed lakes: Lake Bonneville level is set by water balance; closed-basin level changes follow climate. [B-öz] Wikipedia Lake Bonneville. Explicit P−E formula with numbers for a specific basin: BULUNAMADI.
- Caspian level and Volga discharge: levels track Volga discharge, which depends on rainfall in its catchment. [B-öz] Wikipedia Caspian Sea. Volga runoff 420 km³ "enough to keep the Caspian level at +35 m a.s.l." in a HESS 2024 model. [B] HESS 28, 241.

## Topic 4: Global lake databases and size statistics

HydroLAKES / Messager et al. 2016:
- Title: "Estimating the volume and age of water stored in global lakes using a geo-statistical approach," Nature Communications, 2016 (DOI 10.1038/NCOMMS13603). [Ö] search snippet.
- Abstract: 1.42 million natural lake polygons (≥10 ha); total surface area 2.67 × 10⁶ km² (1.8% of global land area); total shoreline 7.2 × 10⁶ km; total volume 181.9 × 10³ km³ (0.8% of global non-frozen terrestrial water stocks). Mean hydraulic residence time 1,834 days; median 456 days. [B] https://www.nature.com/articles/ncomms13603 (read via curl + oku.py)
- Model: lake depth predicted from surrounding terrain. Trained/validated on 12,150 depth records. [B] same URL. Depth best reflected by slope within 100 m of shoreline. [B] same URL.
- Validation: modelled volume underestimated observed by 16.5% (predicted 1,503 km³, observed 1,800 km³). Outside North America/Europe (190 lakes): underestimated by 28.3%. [B] same URL.
- Depth–area relation: explicit coefficients in Model 5 (Supplementary Table 4) were not read. Surface area is a predictor; exact equation BULUNAMADI.
- HydroLAKES (HydroSHEDS page): 1.4 million lakes/reservoirs, total area 2.67 million km², shoreline 7.2 million km, storage 181,900 km³; licensed CC-BY 4.0. [B] https://www.hydrosheds.org/hydrolakes (read via curl + oku.py)
- Pareto/power-law size distribution in HydroLAKES: BULUNAMADI.

Downing et al. 2006 (lake size distribution, Pareto model):
- Global model based on Pareto distribution: about 304 million lakes and ponds, covering 4.2 million km² (natural lakes and ponds ≥0.001 km²). "Global extent of natural lakes is twice as large as previously known." [B] Limnol. Oceanogr. 51(5), 2388–2397. PDF: https://www.caryinstitute.org/sites/default/files/public/reprints/Downing_et_al_2006_Limnol_Ocean.pdf (read via pdftotext)
- Pareto shape parameter c = 1.06 for the canonical data set (range 0.001 to 378,119 km²). [B] same PDF.
- Natural lakes and ponds ≥0.001 km² make up roughly 2.8% of non-oceanic land area, "not 1.3–1.8% as previously supposed." [B] same PDF.
- Power-law applicability caveat: Cael, Biggs & Seekell (2022) argue power-law fits hold only over finite size ranges; evidence "moderate and incomplete." [Ö] search snippet.

Lehner & Döll 2004 (GLWD):
- Global Lakes and Wetlands Database. Level 1: 3,067 largest lakes (area ≥50 km²) and 654 largest reservoirs (storage ≥0.5 km³). Level 2: water bodies ≥0.1 km². Level 3: 30-second raster of wetlands. [Ö] Search snippet; full PDF ERİŞİLEMEDİ (connection reset).
- Validated for lakes ≥1 km². [Ö] same source.

Depth vs area (general): mean depth correlated with terrain slope (Messager). Explicit depth–area power law: BULUNAMADI.

## Topic 5: Rain shadow and plateau edge, linked to closed basins

- Tian Shan and Pamir: high barrier blocks westerlies; rain shadow in NW Tarim. [Ö] search snippets on Tarim origin.
- Tarim closure from Kunlun, Tian Shan and Altyn Tagh uplift; aridification by rain shadow and mountain-front erosion. [Ö]
- Altiplano: endorheic in central Andes; average elevation ~3,750 m, "slightly less than that of the Tibetan Plateau"; unlike Tibet, it has salares (salt flats). [B-öz] Wikipedia Altiplano.
- Tibetan Plateau as edge of Tarim and Qaidam: Qaidam and Tarim endorheic with thick Cenozoic deposits and dramatic uplift. [Ö] Terra Nova 2015 (search snippet).
- Wikipedia "Rain shadow" lists Anatolian Plateau (Pontic and Taurus Mountains). [B-öz] https://en.wikipedia.org/wiki/Rain_shadow
- Quantitative precipitation numbers for Tibet rain shadow: BULUNAMADI.

## Summary of key numbers

| Item | Value | Label | Source |
|---|---|---|---|
| Endorheic share of global land | ~18% | [B-öz] | Wikipedia Endorheic basin |
| Endorheic share (Sci Data) | ~20% | [B] | Sci Data s41597-023-02875-9 |
| Australia / North America endorheic | 21% / 5% | [B-öz] | Wikipedia |
| Tarim Basin area | ~888,000 km² | [B-öz] | Wikipedia Tarim |
| Tarim sediment thickness | >15 km (local) | [B-öz] | Wikipedia Tarim |
| Gobi area | 1,295,000 km² | [B-öz] | Wikipedia Gobi |
| Great Basin | 541,730 km² | [B-öz] | Wikipedia Great Basin |
| Caspian: lowest surface | ~−28 m; deepest 1,023 m below sea level | [B-öz] | Wikipedia Caspian |
| Aral: area 1960 → 2004 | 68,000 → 17,160 km² | [B-öz] | Wikipedia Aral |
| Balkhash: area, elevation | 16,400 km²; ~341 m | [B-öz] | Wikipedia Balkhash |
| Altiplano average elevation | ~3,750 m | [B-öz] | Wikipedia Altiplano |
| Bonneville: max depth / area | >300 m / ~51,000 km² | [B-öz] | Wikipedia Lake Bonneville |
| Bonneville flood lake drop | ~125 m | [B-öz] | Wikipedia Lake Bonneville |
| Caspian early Khvalynian max | +48–50 m (traditional); ~80 m above current | [B] | HESS 2024 |
| Spillway threshold (2026 model) | 31 m a.s.l. (vs 45–50 m earlier) | [Ö] | search snippet |
| HydroLAKES: lakes / area / volume | 1.42 M / 2.67 M km² / 181.9 k km³ | [B] | Messager 2016; HydroSHEDS |
| Lake land share (Messager) | 1.8% of global land | [B] | Messager 2016 |
| Residence time mean / median | 1,834 / 456 days | [B] | Messager 2016 |
| Volume underestimate (validation) | 16.5% | [B] | Messager 2016 |
| Pareto shape c (Downing 2006) | 1.06 | [B] | Downing 2006 |
| Downing: lakes/ponds total | 304 M lakes; 4.2 M km² | [B] | Downing 2006 |
| Priority-Flood time complexity | O(n) integer; O(n lg n) float | [B] | arXiv 1511.04463 |
| Lehner & Döll: level 1 lakes | 3,067 (≥50 km²); 654 reservoirs | [Ö] | search snippet |

## Open items (BULUNAMADI or not verified)
- Depth–area or area–volume equation in closed-basin lakes (Messager Model 5 coefficients not read).
- Explicit Pareto/power-law exponent for HydroLAKES.
- Lehner & Döll 2004 full text (PDF connection reset).
- Fastscapelib flow guide full text (fetch returned 0 characters).
- Caspian sediment thickness.
- Tibet rain shadow precipitation numbers.
- Source for the "~20%" figure in the Sci Data paper (cites ref 1; not verified as Lehner & Döll).
