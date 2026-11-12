# A: Paleotopography (paleo-DEM) map production: research notes

Status: complete for the scope listed; open items at the end.
Labels: [B] full text read; [B-öz] abstract or summary read; [Ö] search-result summary only; BULUNAMADI = not found; ERİŞİLEMEDİ = not accessible.

## Corrections to the brief (checked against sources)
- Scotese & Wright 2018 is NOT an Earth system model. It is a manual, tectonic-model-based paleogeographic method (lithofacies + plate reconstruction + grayscale editing). [B]
- Poblete et al. 2021 (Earth-Science Reviews 214, 103508) covers the CENOZOIC (60, 40, 20 Ma), not the Phanerozoic. [B]
- A "Utrecht Paleogeography Calculator" that outputs paleotopography was NOT confirmed. The existing Utrecht product (Paleolatitude.org 3.0) is a rigid-polygon plate model with no elevation output. [B]

## 1. Scotese & Wright 2018, PALEOMAP PaleoDEM
- Source: https://www.earthbyte.org/webdav/ftp/Data_Collections/Scotese_Wright_2018_PaleoDEM/Scotese_Wright2018_PALEOMAP_PaleoDEMs.pdf [B]
- Scope: 117 paleoDEMs at 5 Myr intervals over the last 540 Myr; elevation/depth in m at 1°x1°. Zenodo https://doi.org/10.5281/zenodo.5460860 also holds a 0.1° (6 arc-min) netCDF set. [B; Zenodo page B-öz]
- Production: Phase I (2003–2008) 50 paleoDEMs at stage boundaries; Phase II (2010–2013) interpolated slices so every stage has a map. Extra slices for long stages and sequence-stratigraphic surfaces. [B]
- Method steps (paraphrased):
  1. Lithofacies maps give depositional environment (thick pure limestone = warm shallow sea; cross-bedded sandstone = dune field; andesite/granodiorite = arc or Andean range). Table 2 maps lithologies to environments. [B]
  2. Where the rock record is missing, environments are inferred from the tectonic history, using the PALEOMAP Global Plate Tectonic Model (Scotese 2016b). Rifting, subduction, collision and glacial rebound (Peltier 2004) are modelled as topographic changes. [B]
  3. Modern topography and bathymetry (Smith & Sandwell 1997; BEDMAP; IBCAO) are merged at 6-arc-min and rotated to paleo-positions. [B]
  4. Manual edits on a 256-level grayscale elevation map (white = +10,000 m, black = −10,000 m), using modern analogs (e.g. East African Rift cloned for a proto-South Atlantic rift). Rule of thumb: work backwards from present, map by map. [B]
  5. Grayscale converted back to elevation: the paleoDEM. [B]
  6. Colour classes applied to make paleogeographic maps (dark blue deep ocean ... white peaks). [B]
- Bathymetry: ocean floor "unsubsided" with the Stein & Stein (1992) depth-age relation. Paleozoic deep ocean fixed at 4800 m (modern average 5400 m) to conserve water volume. [B]
- Resolution: high-res build ~10 km x 10 km horizontal, 40 m vertical. The 1° grid is a paleoclimate-model product. [B]
- Author-stated errors: "numerous errors in the paleotopography"; young features on old maps; features that appear, vanish and reappear; highest mountain heights likely overestimated; Paleozoic bathymetry is the weakest part. Report calls itself a "first draft". No quantitative error model. [B]
- Sea level: Haq et al. estimates judged too high; Haq & Schutter (2009) reduced by 30–40% for a better fit with flooding evidence. [B]
- Use: author says the 1°x1° paleoDEMs may be freely used for research; check the licence file on EarthByte before reuse. [B]
- Downloads: NetCDF 1° zip, CSV (lon/lat/elev), PALEOMAP atlases, GPlates rotation/geometry (Scotese_PaleoAtlas_v3.zip). https://www.earthbyte.org/paleodem-resource-scotese-and-wright-2018/ [B-öz]
- Later Phanerozoic update: AGU 2022 abstract (https://ui.adsabs.harvard.edu/abs/2022AGUFMGP45B0277S) uses Paleobiology Database inputs and cites Scotese (2021) for methods. [Ö]

## 2. Utrecht Paleogeography Model / Calculator (van Hinsbergen et al.)
- Paleolatitude.org 3.0: van Hinsbergen DJJ et al. 2026, PLoS One 21(4) e0346817, https://doi.org/10.1371/journal.pone.0346817 [B]
  - "Utrecht Paleogeography Model": global, GPlates-based, back to 320 Ma. Restores units thrust over each other in orogens. Rigid crustal polygons. [B]
  - Paleomagnetic frame gAPWP25; ages on the latest timescale. Outputs paleolatitude with uncertainty; batch upload and export. [B]
  - Downloads: GPlates rotation and polygon files, a paleogeography version (oceanic vs continental lithosphere). Figshare https://doi.org/10.6084/m9.figshare.31021144; Zenodo https://doi.org/10.5281/zenodo.18183857. [B]
  - Elevation: none. Zero hits for "topograph", "elevation" or "isostat" in the article. [B]
- Paleotopography calculator (planned): EGU 2020 abstract, van der Linden, Dupont-Nivet & van Hinsbergen, https://meetingorganizer.copernicus.org/EGU2020/EGU2020-2402.html. Planned free online calculator from kinematic inputs assuming isostasy, to be released as open source. [Ö]. BULUNAMADI: no launch or release found.
- Original paleolatitude calculator: van Hinsbergen et al. 2015, PLoS ONE, https://forthoofddijk.geo.uu.nl/assets/2015_vanHinsbergen_plos.pdf. Covers the last 200 Myr with error bars for climate modelling. [Ö]. Full PDF download failed (connection reset); not read in full.
- Boundary-condition method: Baatsen et al. 2015/2016 (Climate of the Past) cited by Scotese 2018 and Poblete 2021. Summary only, not read in full. [Ö]

## 3. Markwick & Valdes; Hay et al.
- Markwick PJ & Valdes PJ 2004, "Palaeo-digital elevation models for use as boundary conditions in coupled ocean-atmosphere GCM experiments: a Maastrichtian (Late Cretaceous) example," Palaeogeography, Palaeoclimatology, Palaeoecology 213 (1-2): 37–63. [Ö]
  - Purpose: palaeotopography and palaeobathymetry as GCM boundary conditions. Global GIS-based DEM from the Palaeogeographic Atlas Project (Ziegler et al. database). [Ö]
  - Secondary: Brown, Gaina & Müller (2006) describe the paper as a detailed account of building and using global palaeo-DEMs on land and at sea. [Ö]
  - A 2015 Climate of the Past preprint (https://cp.copernicus.org/preprints/11/4917/2015/cpd-11-4917-2015-AR1.pdf) says neither the Markwick & Valdes workflow nor the model was made public. [Ö]
  - Full text not read: BULUNAMADI in accessible sources.
- Hay: a specific "Hay 2006" paleotopography methods paper was BULUNAMADI.
  - Hay's 1999 Cretaceous work proposed revised continental blocks and shallow meridional seaways. [Ö]
  - Hay's later review (2016/2017) argues Cretaceous continental paleotopography was lower than assumed, affecting model comparisons. [Ö]

## 4. Poblete et al. 2021; Botsyun et al. 2016; paleoelevation indicators
- Poblete F, Dupont-Nivet G, Licht A, van Hinsbergen DJJ et al. 2021, "Towards interactive global paleogeographic maps, new reconstructions at 60, 40 and 20 Ma," Earth-Science Reviews 214:103508, https://doi.org/10.1016/j.earscirev.2021.103508. Full text read from https://www.geologist.nl/wp-content/uploads/2021/01/2021_Poblete_ESR.pdf. [B]
- Six-stage method: (1) GPlates kinematic model, with deforming plate boundaries reconstructed in six regions; (2) modified paleobathymetry where crust overlaps; (3) paleoshorelines from fossil and geologic databases; (4) isostatic compensation in polar regions plus eustatic correction (Müller et al. 2008 curve: +94.7 m at 60 Ma, +73.3 m at 40 Ma, +65.7 m at 20 Ma); (5) paleoelevation from thermochronology, stable isotopes, paleobotany, structure and geomorphology; (6) interactive online products. [B]
- Paleotopography procedure (Sec. 2.4) [B]:
  - Modern topography is cut into tectonic-block polygons in GPlates, rotated to paleo-position, and exported as netCDF.
  - (A) COB mask; (B) GMT blockmean + surface fills gaps from shortening; (C) land/sea mask from paleoshoreline; (D) linear rescaling per region, Z' = A + m·Z, with m = (Z'max − Z'min)/(Zmax − Zmin), to user-set target min/max altitudes.
  - Authors note the masked area is much larger than the data constraining it.
- Paleoelevation indicators [B]:
  - Stable oxygen isotopes in paleosols and meteoric water: "mature" paleoaltimetry (Rowley & Garzione 2007; Botsyun et al. 2016). Biased by temperature, moisture source, relative humidity, post-condensation effects, diagenesis.
  - Biotic paleoaltimetry: nearest living relatives; leaf physiognomy (Spicer 2018; Utescher et al. 2014). Accuracy depends on orogen.
  - Thermochronology: rock uplift and exhumation, not direct surface elevation; combined with planation surfaces and geomorphology (Carrapa & DeCelles 2015).
- Botsyun V et al. 2016, "Impacts of Tibetan Plateau uplift on atmospheric dynamics and associated precipitation δ18O," Climate of the Past 12:1401–1420, https://cp.copernicus.org/articles/12/1401/2016/. Abstract read [B-öz]: LMDZ-iso experiments with reduced Himalaya/Tibet height; only ~40% of sampled palaeoaltimetry sites capture the full topographic signal; uplift-driven changes in humidity and precipitation amount shift δ18O by up to 2.5‰, biasing palaeoelevation. Body not read.
- Wright et al.: BULUNAMADI in this session (not searched directly).
- Related 2021 ESR paper: Kocsis & Scotese 2021, "Mapping paleocoastlines and continental flooding during the Phanerozoic," https://doi.org/10.1016/j.earscirev.2020.103463. Tests Phanerozoic paleo-DEMs against Paleobiology Database occurrences. [Ö]

### Limitations stated by Poblete et al. 2021 (Sec. 5.2–5.3) [B]
- Rigid plates: continental margins deform (Patagonian bend, Bolivian Orocline, Basin and Range). Shortening uncertainty ~20% in well-constrained sections. Bolivian Orocline: 400 km shortening, ≥80 km uncertainty. South Asian margin: ~1000 km shortening, ≥200 km uncertainty.
- Paleomagnetic latitude resolution ~5°.
- Tibet-Himalaya predicted maximum elevation 1000–4500 m at 60 and 40 Ma.
- Nevadaplano ~4500 m at 60 Ma in western North America; southern extent poorly defined.
- Greater India basin depths −5000 to −2600 m assumed; deeper (>−6000 m) with other age-depth relations.
- Paleoshorelines: Golonka et al. 2006 shorelines have stage-level temporal resolution; prior South American sea reentrant until Eocene adjusted (likely only to mid-Maastrichtian).
- Linear DEM rescaling gives unrealistic relief and drainage. Authors say topography is the largest uncertainty, and quantifying uncertainty is "a future frontier". [B]

## 5. Uncertainty and resolution (km, m)
- Scotese & Wright 2018: public grid 1° (~110 km at the equator); high-res build 10 km / 40 m. Errors acknowledged in words only. [B]
- Poblete 2021: uncertainty expressed as km (shortening, shoreline) and elevation ranges (1000–4500 m, Tibet). No formal error bars on paleotopography; authors say quantification is impractical for the combined product. [B]
- Paleolatitude 3.0: bootstrap propagation of paleolatitude and age uncertainty (latitude, not elevation). [B-öz]
- Isotope paleoaltimetry: ~40% of sites faithful; up to 2.5‰ bias (Botsyun 2016). No single standard-error figure in m was found in the read text. BULUNAMADI for a standard m error value.

## 6. Software and formats
- GPlates: Scotese_PaleoAtlas_v3.zip (rotation + geometry, 2018 atlas). [B-öz]
- Scotese 2018: text (lon, lat, elev); CSV (PaleoDEMS_long_lat_elev_csv_v2.zip); netCDF 1° (read with NCL); 0.1° netCDF on Zenodo only. [B-öz]
- Poblete 2021: GPlates-based plate model; netCDF topography per block; interactive site https://map.paleoenvironment.eu/ with zoom, reprojection, and download as image or raster. [B]
- Paleolatitude 3.0: GPlates rotation + polygon files + paleogeography version on Zenodo/Figshare. [B]
- BULUNAMADI: a GPlates-branded "Paleo-Topography" dataset category. The observed sources above are the practical equivalents.

## Open items
- Full text of Markwick & Valdes 2004 (paywalled or not accessible in this session).
- Full text of Hay 2006 (not identified).
- Wright et al. (paleogeographic atlas / method) not searched directly.
- Botsyun et al. 2016 full text (for error figures in m).
- Baatsen et al. 2015/2016 full text (boundary-condition workflow).
- Licence file for the Scotese 2018 data on EarthByte.
- Van Hinsbergen et al. 2015 full PDF (download failed with a connection reset).
