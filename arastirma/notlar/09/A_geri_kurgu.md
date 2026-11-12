# A: Plate tectonic backward reconstruction (geri kurgu) methods

Status: IN PROGRESS. Findings are appended as they are verified.

Tags: [B] primary source read, [D] official documentation, [O] summary, [E] encyclopedia.
Unfound items: BULUNAMADI.

## Findings

### F1 Müller et al. 2016 (Annual Review) [O]
- Citation: Müller, Seton, Zahirovic et al., "Ocean Basin Evolution and Global-Scale Plate Reorganization Events Since Pangea Breakup", Annu. Rev. Earth Planet. Sci. 44:107-138, doi:10.1146/annurev-earth-060115-012211.
- Scope: Triassic (230 Ma) to present. Plate polygons are continuously closing.
- Absolute reference frame: hybrid. Moving hotspot model for last 100 Ma; paleomagnetic model for 200-100 Ma.
- Source: https://www.earthbyte.org/ocean-basin-evolution-and-global-scale-plate-reorganization-events-since-pangea-breakup-2/
- Note: curl to annualreviews.org returned HTTP 403; this is a secondary EarthByte page, not the paper itself.

### F2 Matthews et al. 2016 (Global Planet. Change) [O]
- Citation: "Global plate boundary evolution and kinematics since the late Paleozoic", Global Planet. Change 146:226-250, doi:10.1016/j.gloplacha.2016.10.002.
- Scope: continuous model 410 Ma to present, evolving plate boundaries.
- Reference frame options: default mantle frame, hybrid moving-hotspot frame, TPW-corrected paleomagnetic frame.
- Reports peak plate speeds at 365 Ma; authors flag this as needing further study.
- Source: https://www.earthbyte.org/category/reconstructions/matthews-et-al-2016/

### F3 Merdith et al. 2021 (Earth-Sci. Rev.) [O]
- Citation: "Extending full-plate tectonic models into deep time: Linking the Neoproterozoic and the Phanerozoic", Earth-Sci. Rev. 214:103477, doi:10.1016/j.earscirev.2020.103477.
- Scope: 1000 Ma to present. Claimed as first continuous full-plate model 1 Ga to present.
- Reference frame: palaeomagnetic. New Gondwana APW path 540-320 Ma; global path 320-0 Ma.
- Source: https://www.earthbyte.org/extending-full-plate-tectonic-models-into-deep-time-linking-the-neoproterozoic-and-the-phanerozoic/
- Access: one repository lists the file under embargo; EarthByte offers model downloads.

### F4 Bullard, Everett & Smith 1965 [O]
- Published Phil. Trans. R. Soc. Lond. A, 28 Oct 1965. First computer-based fit of the circum-Atlantic continents.
- Criterion: least squares fit. Margins used at the 500-fathom depth contour, not shorelines. Euler's point theorem used for repositioning.
- Source: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4360082/ (commentary) ; https://earthguide.ucsd.edu/eoc/eoc_teachers_hs_earth/content_tectonics/pdf/Bullard_fit.pdf
- "Area-preserving" property: BULUNAMADI in these results.

### F5 Hellinger (1981) [O, indirect]
- Original 1981 paper: BULUNAMADI (not retrieved directly).
- GPlates Hellinger tool doc says its fitting and uncertainty algorithms derive from Hellinger (1981) and Chang/Royer et al. (1988, 1991). Source: https://gplates.org/docs/user-manual/HellingerTool
- Hellinger 1979 MIT thesis "The Statistics of Finite Rotations in Plate Tectonics" exists (https://dspace.mit.edu/bitstream/handle/1721.1/54271/07243346-MIT.pdf?sequence=2) - thesis, not the 1981 paper; not yet read.
- Related: a 2012 Earth Planets Space paper reports multicollinearity between Euler vector components and a regularized estimator outperforming least squares in MSE. Source: https://earth-planets-space.springeropen.com/articles/10.5047/eps.2012.10.004

### F6 Müller et al. 2019 (Tectonics) [O]
- Citation: "A Global Plate Model Including Lithospheric Deformation Along Major Rifts and Orogens Since the Triassic", Tectonics 38:1884-1907, doi:10.1029/2018TC005462. Authors include Müller, Zahirovic, Gurnis.
- Scope: ~240 Ma to present. Includes deforming lithosphere (rifts, orogens) with stretching-factor grids. Relevant to item (6).
- Source: https://www.earthbyte.org/muller-et-al-2019-deforming-plate-reconstruction-and-seafloor-age-grids-tectonics/ (from search result; page not fetched)

### F7 Müller (R. D.) et al. 2022 (Solid Earth 13:1127) [B] (full text downloaded and grepped)
- Title: "A tectonic-rules-based mantle reference frame since 1 billion years ago - implications for supercontinent cycles and plate-mantle system evolution". Lead author R. Dietmar Müller.
- Method: absolute (mantle) frame optimised on top of the Merdith et al. (2021) relative model. Relative plate motions left unchanged. Four criteria:
  (1) net lithospheric rotation minimised but non-zero;
  (2) global trench migration minimised, favouring trench retreat;
  (3) misfit to present-day hotspot chains minimised;
  (4) global continental median plate speed < 60 mm/yr (bound from Zahirovic et al. 2015).
- Weights: for >80 Ma, NR=1, TM=0.5, PV=0.5, HS=0; for 0-80 Ma all = 1.
- Result claim: net rotation consistently < 0.25 deg/Myr.
- Source: https://se.copernicus.org/articles/13/1127/2022/ (full text fetched via curl)
- The user's "Annual Review 2022" label: NOT CONFIRMED. Only the 2016 Annual Review paper was found.

### F8 Buffan et al. 2023 (Methods Ecol. Evol.) [O]
- Used five open-access global plate models to reconstruct Phanerozoic palaeogeography (540-0 Ma) and quantify uncertainty. Found model differences grow with reconstruction age.
- Source: https://doaj.org/article/97f797fc7a114159a96fb790cd497431 (search hit)

### F9 Nature Reviews Earth & Environment Technical Review, 2022 [B] (abstract fetched)
- DOI 10.1038/s43017-022-00384-8. Title "Deconstructing plate tectonic reconstructions" was from a search snippet and is NOT verified against the page.
- Abstract: no "one-size-fits-all"; users must understand data and assumptions behind competing models; reconstructions simplify reality, so interpret them to avoid circular reasoning; calls for intercomparison and uncertainty quantification.
- Source: https://dx.doi.org/10.1038/s43017-022-00384-8

### F10 Müller et al. 2019 v2.0 update (EarthByte) [B-ish: page fetched via curl, text read]
- Absolute frame optimisation weights (TR=trench migration, NR=net rotation, HS=hotspot track fit):
  0-80 Ma: TR=1, NR=1, HS=1; 80-170 Ma: TR=1, NR=0.5; 170-250 Ma: TR=1, NR=0.2. Simplified at 5 Myr intervals.
- Also updates East Asia (Young et al. 2018 sync, 250-130 Ma) and Pacific APM fixes after Torsvik et al. 2019.
- Source: https://www.earthbyte.org/update-to-the-muller-et-al-2019-plate-reconstructions/
- Lesson for item (7): absolute frame weights change with age; the reference frame is a modelled choice, not a fact.

### Fetch failures (this session)
- gplates.org, www.ncbi.nlm.nih.gov, www.earthbyte.org: DNS ENOTFOUND in WebFetch. Hosts need to be allowed in session network settings. Results above are from search snippets only.
- annualreviews.org: curl HTTP 403.

### F11 Hotspot vs paleomagnetic frames and TPW [O] (search snippets, not fetched)
- Steinberger & Torsvik 2008 (Nature): absolute motion without hotspot tracks; continental average in paleomagnetic frame, 320 Myr; some rotations interpreted as TPW.
- Doubrovine, Steinberger & Torsvik 2012 (JGR 117:B09101, doi via ADS 2012JGRB..117.9101D): global moving-hotspot frame. A fixed-hotspot frame gave unacceptable misfits for 80-50 Ma. TPW rates vs paleomagnetic frame ~0.1 to 1 deg/Myr.
- Torsvik, Van der Voo & Redfield 2002 (EPSL): Early Cretaceous paleomagnetic and hotspot frames for Indo-Atlantic consistent with slow TPW; argues against global TPW.
- Explicit TPW-correction formula: BULUNAMADI in these results. Practical reading: hybrid frame = hotspot rotation for young times, paleomagnetic for old; the difference of the two rotations is the TPW estimate.
- Sources: https://ideas.repec.org/a/nat/nature/v452y2008i7187d10.1038_nature06824.html ; https://ui.adsabs.harvard.edu/abs/2012JGRB..117.9101D
- Torsvik et al. 2008 (hybrid frame) original: BULUNAMADI (not retrieved).

### F12 Finite rotation, Euler pole, anchoring [D] (GPlates/EarthBYTE tutorial text, search snippets)
- Euler's displacement theorem: any displacement on the sphere = rotation about an axis. Stored as pole lat, pole lon, angle (finite rotation). Relative rotation: moving plate ID, time (Ma), lat, lon, angle, conjugate (fixed) plate ID.
- Total reconstruction pole: rotation from present position to past position. Chains of relative rotations must be anchored to plate ID 000 (absolute reference frame: hotspot, paleomagnetic, or mantle).
- Sources: https://www.earthbyte.org/Resources/GPlates_tutorials/All_Tutorials/GPlates_Rotations1_Tutorial.html ; https://www.earthbyte.org/webdav/ftp/earthbyte/GPlates/TutorialData_GPlates2.1/Tutorial_2.2_Changing_Rotations_Equivalent_FiniteRotations_and_Cross-Overs.pdf
- Not verified: how closure of plate circuits is enforced; GPlates sign convention for the angle. BULUNAMADI.

### F13 Bullard, Everett & Smith 1965 method details [O] (Virtual Explorer article, text fetched)
- Each continent treated as rigid rotation (Euler's theorem). Best fit = rotation minimising sum of squared longitude differences between matched points on two contours. Matched points are at equal distance from rotation centre.
- Contours tested: 100, 500, 1000, 2000 fm isobaths. 500 fm gave best fit for South America-Africa.
- Source: https://virtualexplorer.com.au/article/2007/163/breakup-of-south-america-and-africa/headings.html
- Area-preserving claim: BULUNAMADI. The method is least-squares on contour matching, not an area-balance constraint.
- Criticism: isobath matching is arbitrary; COB geometry is often better fit visually (same source).

### F14 Euler pole uncertainty, Chang / Royer / Kirkwood (search snippets only)
- Chang 1988, "On reconstructing tectonic plate motion from ship track crossings", JASA 83:1178-1183.
- Royer & Chang 1991, JGR: Indian-Australian motion, last 20 Myr; method used in later studies.
- Kirkwood, Royer, Chang & Gordon 1999, GJI 137:408-428: estimating and combining finite rotations and uncertainties; rotation parameters from minimising quadratic objective. Source: https://perso-sdt.univ-brest.fr/~jroyer/GJI_99_abstract.html (fetch failed: 60 chars; snippet only).
- Chang, Ko, Royer & Lu 2000, Statistical Science: linearised error model for relative plate motion from marine magnetic anomalies. Source: https://projecteuclid.org/euclid.ss/1009213002
- Hanna & Chang 1990: graphical confidence region for unknown 3D rotation. Source: https://www.usgs.gov/publications/graphically-representing-confidence-region-unknown-rotation-three-dimensions
- Formula of the confidence region: BULUNAMADI.
- Note: a 2012 EPS paper reports multicollinearity between Euler vector components (see earlier entry).

## Open items (updated)
- Müller 2019 and 2022 models: not yet searched
- Hotspot / paleomag frame formulas: not yet searched
- Area-preserving reconstruction: not yet searched
- Plate-motion-model limits for deformed blocks: not yet searched

## Open items

- (1) Paleomagnetism and hotspot reference frames
- (2) Fixed Euler pole, finite rotation, Bullard fit, area-preserving reconstruction
- (3) Müller et al. 2016 / 2019 / 2022 global plate models
- (4) Matthews 2016 (Paleozoic), Merdith 2021 (Neoproterozoic)
- (5) Euler pole uncertainty: Hellinger 1981, Chang and others
- (6) Plate-motion-model limits for deformed / distributed-deformation blocks
- (7) Inverse-problem framing and analogues (jigsaw fit, paleogeographic reconstruction)
