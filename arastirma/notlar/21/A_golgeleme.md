# A: Realistic relief depiction in cartography (research notes)

Tags: [B] full text read, [B-öz] summary of a read page, [Ö] search-snippet only (not opened), BULUNAMADI = not found.
Scratch copies of the pages read: /tmp/claude-0/-home-user-Tectonic/1cb340b3-df7d-519b-96f4-5170b8cfb37a/scratchpad/a21/txt/

## 1. Single- and multidirectional hillshade

- Classic formula / defaults: Esri "How Hillshade Works" [B-öz]. Default azimuth 315 degrees (NW), default altitude 45 degrees. Azimuth is clockwise from north; altitude is measured above horizon; zenith = 90 - altitude; math azimuth = 360 - azimuth + 90 (mod 360). Slope and aspect come from a 3x3 window over the eight neighbours (the page does not name Horn). Shade formula text is an image/LaTeX on the page and was NOT extracted; the page cites Burrough & McDonell (1998) for the method. Horn (1981) is not verified in this session. Formula text: BULUNAMADI (verbatim).
  URL: https://doc.esri.com/en/arcgis-pro/latest/tool-reference/spatial-analyst/how-hillshade-works.html
- Mark (1992), multidirectional: USGS OFR 92-422, "Multidirectional, oblique-weighted, shaded-relief image of the Island of Hawaii", DOI 10.3133/ofr92422 [Ö, search snippet]. Snippet (Esri blog) says four azimuths 225, 270, 315, 360, each 30 degrees altitude, weighted by aspect (sin^2) [Ö]. Full text not retrieved (the pubs URL I tried returned a 703-char page). Azimuth/weight values: [Ö] only.
  URL: https://pubs.usgs.gov/of/1992/of92-422
- Current Esri multidirectional: "combines light from six different directions to represent an enhanced visualization of the terrain and to improve the appearance of regions with low relief. It improves the balance between the overexposed and shadow areas" [B-öz]. Six directions (not four) is the current Esri implementation.
  URL: https://doc.esri.com/en/arcgis-pro/latest/help/analysis/raster-functions/hillshade-function.html
- RVT manual, multidirectional: directions equally spaced 0-360, default 16, "16 is optimal"; 8, 16, 32, 36 are the most useful values; "not very useful to go much beyond 16 directions" [B-öz]. RGB composite of three directions separated by 60 degrees: red 315, green 15, blue 75 (Hobbs 1999 approach) [B-öz].
  URL: https://www.zrc-sazu.si/sites/default/files/rvt_2.2.1_0.pdf
- Jenny & Hurni (2006) on Hobbs (1995, 1999): three shadings from three illumination directions assigned to R, G, B channels to clarify landforms [B-öz].

## 2. Swiss-style relief shading

- Jenny & Hurni (2006), "Swiss-Style Colour Relief Shading Modulated by Elevation and by Exposure to Illumination" (ETH Zurich). Published in The Cartographic Journal (journal name taken from the PDF running header; volume not verified). Abstract [B-öz]: colour look-up table built from "all combinations of initial grey values and terrain elevations"; constructed from interactively placed colour reference points; uses a DEM. Imhof's Swiss schemes: sun-lit slopes yellow-green, shadowed slopes green-purple (shadow changes hue with exposure). Jenny & Hurni describe Imhof's Mount Rigi map with "unusual southern illumination" [B-öz].
  Local copy: .../scratchpad/a21/jenny2006.pdf
  URL: https://mail.colororacle.org/berniejenny/pdf/2006_JennyHurni_SwissStyleShading.pdf
- Jenny (2001), "An Interactive Approach to Analytical Relief Shading", Cartographica 38(1-2) [Ö, search snippet]. Snippet: aspect-based shading on steep slopes, diffuse reflection on lowlands, bright grey on flat areas. Equations: BULUNAMADI (not opened).
- Kennelly (2008), "Terrain maps displaying hill-shading with curvature" (pp. 567-577) [Ö]. Snippet: curvature-combined hillshade enhances continuity of tonal edges, especially in strongly lit areas. Journal title not confirmed in the snippet (the query said Geomorphology; not verified).
- Kennelly & Stewart, "General sky models for illuminating terrains", IJGIS 28(2), 383-406 (2014) [Ö]. Snippet: a tool to select a general sky model and illuminate terrain with it. The query's "Kennelly 2014 Geomorphology" paper was NOT found: BULUNAMADI. Kennelly & Stewart 2006 "A uniform sky illumination model..." CaGIS 33(1) 21-36 [Ö].
- Leonowicz, Jenny & Hurni (2010), "Automated Reduction of Visual Complexity in Small-Scale Relief Shading", Cartographica 45(1):64-74, doi 10.3138/carto.45.1.64 [B-öz]. Key claim: at small scales SRTM-derived analytical shading shows too much detail; "mountain ridges are not sharp enough, large landform structures are not prominent" [B-öz]. Method: curvature-based DEM generalization; ridge-exaggerated and valley-deepened grids combined by terrain character. Example: Switzerland at 1:1,000,000 with diffuse-reflection shading, azimuth 300, inclination 45 (Yoeli 1959) [B-öz]. Conclusion (from abstract): automatic shading unsuitable for high-quality small-scale products without generalization [B-öz].
  Local copy: .../scratchpad/a21/txt/leon2010.txt
  URL: https://mail.colororacle.org/berniejenny/pdf/2010_Leonowicz_Small_Scale_Relief_Shading.pdf
- Veronesi & Hurni (2014): full paper NOT found: BULUNAMADI. Only an indirect mention in a 2015 ICA paper ("made relief shading easier to produce in GIS") [Ö].

## 3. Sky-view factor, openness, ambient occlusion; RVT

- Zakšek, Oštir & Kokalj (2011), "Sky-View Factor as a Relief Visualization Technique", Remote Sensing 3(2):398-415 [Ö, search snippet and RVT reference list]. Full text: not opened.
- RVT manual (Kokalj, Zakšek, Oštir, Pehani, Čotar, Somrak; v2.2.1) [B-öz]:
  - SVF = "a proxy for diffuse illumination and measures the proportion of the sky visible from a given point"; ridges and earthworks appear light, depressions dark.
  - SVF defaults: 8 search directions (16 "optimal for most applications"); search radius default 10 px; "Use small search radius (5-10 m; i.e. 5-20 pixels) if you are interested in small features".
  - Anisotropic SVF: weights from cosine of half-angle (Zakšek et al. 2012) [B-öz].
  - Openness (positive/negative): mean horizon elevation angle within a search radius; "Positive openness is similar to sky-view factor, with a more 'flattened feel', while negative openness gives additional information on convex features (Yokoyama et al. 2002)" [B-öz].
  - Table 1 (8-bit conversion): SVF linear stretch 0.6375-1; openness 60-95 degrees [B-öz].
  - Flat terrain: sun angle can be lowered to 15 degrees or less; SVF min/max cut-offs 0.9-1.0 [B-öz].
  - Kokalj & Somrak (2019), "Why not a single image?" is the recommended combination reference [B-öz].
  URL: https://www.zrc-sazu.si/sites/default/files/rvt_2.2.1_0.pdf ; project page https://iaps.zrc-sazu.si/en/svf
- Yokoyama, Shirasawa & Pike (2002), "Visualizing Topography by Openness", PE&RS 68(3):257-265 [Ö, GEOLIS record]. Note: the author list in the query (Shibasaki, Tachibana) is NOT correct per the record. Positive openness high for convex forms, negative for concave [Ö].
- Ambient occlusion: not separately searched: BULUNAMADI.

## 4. Hypsometric tint

- Patterson & Jenny (2011), "The Development and Rationale of Cross-blended Hypsometric Tints", Cartographic Perspectives 69, pp. 31-45, DOI 10.14714/CP69.20 [B-öz]. Full text read.
  - Concept: "Hypsometric tints (Imhof 1982)—cartographic jargon for elevation colors". Cross-blended tints use varying lowland colours per environment; four environmental regions only: "warm humid, cold humid, arid, and polar" [B].
  - Lowland environment colour only below 1,000 m; above that conventional and identical [B]: "With the exception of polar regions, the different environment colors occur only in areas that are below 1,000 meters in elevation."
  - Shaded relief: "a light application of shaded relief... does not contain gray value in flat areas, allowing readers to see the subtle..." [B-öz].
  - Scale: "best-suited for small- and medium-scale maps" [B].
  - Data: SRTM30Plus, 30-arcsecond base; dataset introduced 2009 on Natural Earth [B-öz].
  URL: https://cartographicperspectives.org/index.php/journal/article/download/cp69-patterson-jenny/html?inline=1
- Imhof: "Cartographic Relief Presentation" (Imhof 1982 is cited in CP69; the 1965 date in the query is not confirmed by any read source). Full text of either edition: BULUNAMADI (not opened). Imhof's tints (green, light yellow-green, light yellow, red, white): 1962 Swiss school atlas per CP69 [B-öz].
- Patterson & Jenny follow-up user study (CP 75, 2013/2014 date conflict): Patterson & Jenny, "Evaluating Cross-blended Hypsometric Tints", CP75 [Ö].

## 5. Bathymetric colouring

- Natural Earth 10m ocean bottom: blended depth colours and relief shading derived from CleanTOPO2 [Ö, search snippet]. Patterson's later Blue Earth Bathymetry (GEBCO-based) replaces it [Ö].
- Natural Earth 10m shaded relief: grayscale, land only; water filled with flat grey; derived from SRTM Plus [Ö]. A snippet gives conflicting coastline scales (10 vs 50 million) for the 10m vs 50m product; check the download notes [Ö].
  URLs: https://www.naturalearthdata.com/downloads/10m-raster-data ; https://www.naturalearthdata.com/downloads/50m-raster-data
- Patterson's Gray Earth design (CP 74) [Ö]: https://cartographicperspectives.org/index.php/journal/article/download/cp74-huffman-patterson/html?inline=1 (not read).

## 6. Vertical exaggeration and small-scale slope weighting

- Leonowicz et al. (2010) [B-öz]: small-scale shading must "accentuate the differences between mountainous and low-relief" areas; the method exaggerates ridgelines and deepens valleys; generalization is done before shading.
- Exact vertical exaggeration factor and slope weighting rules for small scales: BULUNAMADI (not found in the read sources).
- UCGIS GIS&T body of knowledge: vertical exaggeration defined as a z scale factor, used mainly in profiles [Ö].

## 7. Cell size (5-10 km) and scale

- Farmakis-Serebryakova, Heitzler & Hurni: resolution (m) = map scale denominator / 1000 / 2 [Ö, search snippet, not opened]. Computed from that rule: 1:10,000,000 gives 5 km; 1:20,000,000 gives 10 km. So 5-10 km cells fit maps of roughly 1:10M to 1:20M. Check against the original paper before relying on it.
- Cell count check (my arithmetic, not a source): global 510 million km2 / (5 km)^2 = about 20 million cells; at 10 km, about 5.1 million; land only (149 million km2): about 6 million at 5 km, about 1.5 million at 10 km. So a 1 to 3 million cell output corresponds to roughly 10 km cells over land, or a clipped area at 5 km.
- Leonowicz et al. (2010): SRTM 3 arcsec (about 60 m) is too detailed at 1:1,000,000 and must be generalized [B-öz]. Small-scale maps 1:500,000 and below: "few references" on shading for them [B-öz].
- Method per scale (summary, from the read sources):
  - 1:10M to 1:20M (5-10 km cells): hillshade alone is too busy; use generalized DEM or curvature-based generalization, low-contrast multidirectional hillshade, and hypsometric tints with shading overprint; cross-blended tints for regional environment [B-öz + computed].
  - Larger scales: SVF/openness with 5-10 m search radius for detail (RVT manual) [B-öz].

## Sources list (read)
- Jenny & Hurni 2006 (PDF, local copy) [B-öz]
- Patterson & Jenny 2011, CP69 html [B-öz]
- Leonowicz, Jenny & Hurni 2010 PDF [B-öz]
- RVT manual v2.2.1 PDF [B-öz]
- Esri How Hillshade Works [B-öz]
- Esri hillshade function (raster-functions page) [B-öz]

## Not found / not verified
- Mark 1992 full text (the Hawaii report): not retrieved.
- Horn (1981) original paper: not searched.
- Imhof 1965 / 1982 full text: not retrieved.
- Kennelly 2014 "Geomorphology" paper: not found.
- Veronesi & Hurni 2014: not found.
- Jenny 2001 equations: not retrieved.
- Ambient occlusion (Yokoyama 2002 in full), Zakšek 2011 full text: not opened.
