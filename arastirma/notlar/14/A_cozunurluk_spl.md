# A: Grid-resolution (Δx) dependence of the stream power law E = K A^m S^n

Status: research complete for the sources reachable this session. Items marked ERİŞİLEMEDİ or BULUNAMADI are listed in the final section.

Labels:
- [B] full text read (HTML or PDF extraction)
- [B-öz] summary or abstract only, from the search tool
- [Ö] search snippet only
- [T] my own derivation from the cited results (not stated as such in the source)
- ERİŞİLEMEDİ: source could not be fetched (TLS or network); no bypass attempted
- BULUNAMADI: no supporting statement found in the sources read

Line numbers refer to the extracted text files in the scratchpad (dl2025, dl2020, dl367, dl741, dlpdf).

## 0. Attribution correction

- "Hergarten 2025, Earth Surface Dynamics, 'Resolution dependence of the stream power law' / 'K ve m ızgara çözünürlüğü ölçekleme'": BULUNAMADI under that title or author.
- The 2025 ESurf paper on grid resolution and the stream power law is ESurf 13, 403–415 (2025), "A fractal framework for channel–hillslope coupling", by Kargère, Constantine, Hales, Grieve and Johnson. URL: https://esurf.copernicus.org/articles/13/403/2025/ [B]. Hergarten is cited inside it, but is not an author.
- Hergarten's 2025 publications were not found in the search. Treat the user's title as unverified.

## 1. Hergarten (2020), transport-limited erosion

- Ref: Hergarten S. (2020), "Transport-limited fluvial erosion – simple formulation and efficient numerical treatment", Earth Surf. Dynam. 8, 841–854, DOI 10.5194/esurf-8-841-2020. URL: https://esurf.copernicus.org/articles/8/841/2020/ [B]
- Label: [B]
- Finding 1.1: Node area s_i is the pixel size on a regular mesh. Sediment flux Q_i (total, not per unit width) enters the balance. [B, lines 40–41]
- Finding 1.2: A transport-limited term with the detachment-limited K would give a scaling problem for rivers treated as linear objects. An extra rescaling factor that depends on pixel size must be added to the excavation term Γ to avoid artificial resolution dependence. The paper points to Howard (1994), Perron et al. (2008), Pelletier (2010) and Hergarten (2020a) for the factor, but does not give one universal formula. [B, line 133]
- Finding 1.3: Transport-limited erosion is a diffusion-type equation with a diffusivity that depends on catchment size and varies over orders of magnitude. [B, line 30]
- Finding 1.4: Linear model (n=1) is solved without iteration; time steps up to δt=1 give errors of "some percent", interpreted as a time lag. [B, line 91]
- Finding 1.5: Test domain 5000×5000 nodes, m=0.5, lengths in pixels. [B, line 78]

## 2. Hergarten (2020a), "Rivers as linear elements in landform evolution models"

- Ref: Earth Surf. Dynam. 8, 367–377, DOI 10.5194/esurf-8-367-2020. URL: https://esurf.copernicus.org/articles/8/367/2020/ [B]
- Finding 2.1 (the scaling problem): When rivers are one-pixel-wide linear objects and local transport is ignored, valleys narrow as the mesh width decreases ("canyon-like"). Examples use δ=0.01 (100×100) and δ=0.002 (500×500), m=0.5, θ=0.5. [B, lines 19–21]
- Finding 2.2 (local transport): With linear diffusion, the river steepness depends on δ and grows as δ decreases, because the river must remove sediment from hillslopes. [B, lines 22–26]
- Finding 2.3 (prior fixes): Howard (1994) used a sub-pixel river fraction (channel width w over δ). Perron et al. (2008) applied it to detachment-limited erosion with constant channel width. Pelletier (2010) rescaled the transport term instead. Hergarten argues that the first two still depend on w, and w is not consistent when it changes downstream. [B, lines 27–32]
- Finding 2.4 (threshold approach): Define a threshold catchment A_c (A ≥ A_c is river, otherwise hillslope). Mean hillslope area A_e draining into a river site with catchment A follows Eq. 14, A_e ≈ α A_c^β, which does not depend on A for large A. [B, lines 36–48]
- Finding 2.5 (fitted exponents): Lattice, θ=0.5: α = 1.360, β = 0.465. OCN reference (θ=0.5, L=4096): α = 1.508, β = 0.478. [B, lines 48, 53]
- Finding 2.6 (resulting δ dependence): If A_c is a physical area (A_c = δ² × pixel count), the fluvial incision term scales like δ^(−2β). For β = 0.5 this is δ^(−1), basically the same as Perron et al. (2008), but without the interpretation of w as a constant. [B, lines 53–54] Exact equation numbers (Eq. 11–16) are not recoverable from the text extraction.
- Finding 2.7 (residual dependence): Rescaled simulations still show a residual dependence on resolution. Mean k_s ranges from about 1.6 to 2.0 over N = 10^5 to 10^7 nodes. Unscaled simulations depend strongly on N. The cause is network reorganisation caused by diffusion; convergence as δ→0 is not clear. [B, lines 59, 62]

## 3. Hergarten & Pietrek (2023), self-organisation of channels and hillslopes

- Ref: Earth Surf. Dynam. 11, 741–755, DOI 10.5194/esurf-11-741-2023. URL: https://esurf.copernicus.org/articles/11/741/2023/ [B]. PDF used for equations: https://esurf.copernicus.org/articles/11/741/2023/esurf-11-741-2023.pdf [B, PDF text extraction, some fraction order garbled]
- Finding 3.1 (K and U rescaling for pure fluvial model): Non-dimensional K is rescaled by α = δx^(n−2m) · L^(1−n) · T^(−1) (Eq. 16); U is rescaled by β = L·T^(−1). Transferring simulations between grid spacings at constant K and U requires α and β to stay constant. [B, PDF Eq. 16; text lines 68–69]
- Finding 3.2 (length and time scales): Eq. 17 gives T ∝ L ∝ δx^((n−2m)/n) (exponent read from garbled text; [T] for the reading). For m/n = 0.5 the exponent is 0, so L and T do not depend on δx. [B text lines 70; PDF Eq. 17, sign of exponent inferred]
- Finding 3.3 (diffusion breaks the scaling): With hillslope diffusion (K_d, K_t, shared stream-power model), the scaling is lost. A characteristic length appears. The parameter A_h (Eq. 14, A_h = (K̃_d/K_d)^(1/m) = (K̃_t/K_t)^(1/m), garbled in extraction) then scales with δx² in real-world units. To keep physical erodibilities fixed, the non-dimensional A_h must scale as A_h ∝ δx^(−2). [B, PDF lines ~483–488]
- Finding 3.4 (residual dependence): The authors cite Hergarten (2020a, Fig. 10) for a residual dependence even after rescaling. It is caused by the hillslope–fluvial transition, where parallel flow makes the catchment size depend on grid spacing. Transport capacity also depends on resolution, so the issue is not specific to the stream power model. [B, line 29]
- Finding 3.5 (diffusivity): In the same simulations, a 10-fold increase in D raises the channel-forming area by about 6.5, i.e. roughly D^0.8, not D. [B, line 42]
- Finding 3.6 (threshold): There is no universal A_c; it depends on the processes and their parameters, and A_c should increase with diffusivity. [B, line 32]
- Finding 3.7 (m = 0 for hillslopes): The hillslope model uses m = 0 because catchment size A depends on grid spacing for unchannelised flow. [B, line 51]

## 4. Kargère et al. (2025), fractal framework for channel–hillslope coupling

- Ref: Earth Surf. Dynam. 13, 403–415 (2025). URL: https://esurf.copernicus.org/articles/13/403/2025/ [B]
- Finding 4.1: On a two-dimensional grid, drainage area of hillslopes (parallel flow) depends on pixel width δ, while convergent channel flow areas are less affected. Hergarten (2020), Pelletier (2010) and Hergarten & Pietrek (2023) are cited for this. [B, line 29]
- Finding 4.2 (hypothesis 1, confirmed on Gabilan Mesa): Drainage area at the inflection point scales with one factor of δ. [B, lines 61, 63]
- Finding 4.3 (hypothesis 2): Channel-head drainage area is independent of δ and equals the square of the specific drainage area at the inflection point. [B, lines 61, 63]
- Finding 4.4: Specific drainage area a = A/δ, implicitly dependent on δ. Using D∞ flow routing on square pixels. [B, line 39]
- Finding 4.5 (channel width): The authors assume channel width can exceed pixel width, with the pixel width set to the channel-head width (following Litwin et al. 2022b). The channel-slope concavity then differs from Pelletier (2010). [B, line 67]
- Finding 4.6: No explicit rule for K(δ) or m(δ) was found in the extracted text. [B, grep of K / scaling terms]

## 5. Lague (2014), SPIM review

- Ref: Earth Surf. Process. Landforms 39, 38–61, DOI 10.1002/esp.3462. Full text: https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2014_Lague_ESPL.pdf [B]
- Finding 5.1: Equation 3 (the channel-steepness relation, slope–area with θ ≈ 0.5) applies only above a critical drainage area of about 0.1 to 5 km². Below that, colluvial processes dominate. [B, line 130 region]
- Finding 5.2: A_cr is the critical drainage area below which debris flow and landsliding dominate. [B, Fig. 3 caption]
- Finding 5.3: Grid spacing: the paper's own example uses dx = 5 m for a shear-stress model. A general grid-scaling rule for K is not given. Δx scaling: BULUNAMADI. [B, line 900]
- Finding 5.4: Lague argues that sub-grid width should be treated with an explicit partial-differential equation (trapezoidal cross-section), not a fixed Δx rule. [B, line 1236]

## 6. Armitage (2019), short communication "Flow as distributed lines within the landscape", ESurf 7, 67

- Ref: Earth Surf. Dynam. 7, 67 (2019). URL: https://esurf.copernicus.org/articles/7/67/2019/ [B]. Author name per search summary [Ö], not confirmed in the extracted header.
- Finding 6.1: Fixing flow width at sub-grid level makes response time depend on the chosen width, so a grid-independent LEM would need no predefined length scale. [B, line 12]
- Finding 6.2: Runoff per unit length is related to catchment area by Q_w ∝ A^0.8 (Syvitski & Milliman 2007). [B, line 21]
- Finding 6.3: Node-to-node flow routing is an alternative to cell-to-cell routing. In the tested setup, cell-to-cell SFD and node-to-node SFD both still show resolution dependence (wind-up time, valley spacing). [B, lines 26–30]
- Finding 6.4: Stream-power models typically route with SFD and still show resolution dependence (Braun & Sambridge 1997; Braun & Willett 2013). Pelletier (2010) with MFD still shows some dependence. [B, line 35]
- Finding 6.5: The Divide And Capture (DAC) model uses an adaptive mesh. Changing the re-meshing settings to 23 172 vs 93 734 cells gives very similar median wavelength. [B, line 37]

## 7. Pelletier (2010), flow routing

- Ref: Geomorphology 122, 91–98, DOI 10.1016/j.geomorph.2010.06.001 [B-öz, search summary]
- Finding 7.1: Refines flow-routing algorithms to give unit contributing areas (area per unit flow width) with reduced grid dependence. [Ö]
- Finding 7.2: Width set to pixel width for non-convergent flow, or to a power law of drainage area for convergent flow; compatible with D4, D8, Dinf and MFD. [Ö, GSA 2019 abstract]
- Finding 7.3: The full text was not accessible; the exponent is not verified. [Ö]

## 8. Perron, Dietrich & Kirchner (2008), valley spacing

- Ref: JGR 113, F04016, DOI 10.1029/2007JF000977 [B-öz, cited in Hergarten 2020 and 2020a]
- Finding 8.1: Cited as the source of the constant-channel-width sub-pixel scaling in the detachment-limited model (Hergarten 2020a, Section 2). [B, citing text]
- Finding 8.2: Full text: ERİŞİLEMEDİ (not fetched). Threshold-based conclusions are not verified.

## 9. Whipple & Tucker (1999)

- Ref: JGR 104(B8), 17661–17674, DOI 10.1029/1999JB900120 [B-öz, search summary]
- Finding 9.1: The stream-power model's dynamics depend on one non-dimensional group (uplift–erosion number). Response times depend on climate, rock strength and perturbation size. [Ö]
- Finding 9.2: PDF at https://planetarygeoscience.uchicago.edu/doc/Whipple_and_Tucker_1999.pdf: ERİŞİLEMEDİ. The certificate could not be verified by curl (TLS error with system CA and the proxy CA bundle). No bypass attempted. Hence no statement on grid dependence of K or m from this paper.

## 10. Stock & Montgomery (1999)

- Ref: JGR 104(B3), 4983–4993, DOI 10.1029/98JB02139 [Ö]
- Finding 10.1: Field calibration source for K. Content on channel heads or critical drainage area: BULUNAMADI in the search results.

## 11. Braun & Willett (2013)

- Ref: Geomorphology 180–181, 170–179, DOI 10.1016/j.geomorph.2012.10.008 [Ö]
- Finding 11.1: O(n) implicit stream-power solver. Landlab notes that transient accuracy is not time-step independent (see Appendix B of the paper). [Ö]
- Finding 11.2: Grid-spacing dependence of K or m: BULUNAMADI in search results. Full text not fetched.

## 12. Schwanghart & Scherler (2017)

- Ref: ESurf 5, 821–839, https://esurf.copernicus.org/articles/5/821/2017/ [Ö]
- Finding 12.1: Addresses DEM error and quantile-regression smoothing of river profiles. It is about data and profile uncertainty, not about how K or m scale with Δx. Relevance to Δx scaling: BULUNAMADI (tangential).

## 13. Campforts, Schwanghart & Govers (2017), TTLEM

- Ref: ESurf 5, 47–66, DOI 10.5194/esurf-5-47-2017. URL: https://esurf.copernicus.org/articles/5/47/2017/ [Ö]
- Finding 13.1: Higher-order flux-limited finite-volume scheme that reduces numerical diffusion for retreating knickpoints. [Ö]
- Finding 13.2: A threshold catchment size for fluvial vs. hillslope processes is used in TTLEM according to Hergarten (2020a) [B, line 34]. The threshold itself was not verified in the TTLEM text.

## 14. Cordonnier (2016), Gailleton (2019), adaptive meshes

- Cordonnier 2016 (K vs cell area): BULUNAMADI. The search did not return this paper. A Cordonnier & Braun paper on erodibility and cell area was also not found.
- Gailleton et al. (2019), ESurf 7, 549: the search returned the author list (Gailleton, Malatesta, Cordonnier, Braun), but the topic (90 m global topography and drainage basins) does not match "multiresolution / adaptive mesh". Multiresolution SPL result: BULUNAMADI.
- Adaptive mesh example: DAC (Goren et al. 2014) in Armitage (2019), Finding 6.5 [B].

## 15. Synthesis by question

### (1) Hergarten 2020 / 2025, and the stream power law K, m and Δx
- Hergarten (2020a): with A_c fixed as a physical area, the fluvial term scales as δ^(−2β), β ≈ 0.465–0.5 (exponent from fitted lattice data). [B]
- Hergarten & Pietrek (2023): for pure stream power, K scales as α = δx^(n−2m) L^(1−n) T^(−1) [B, Eq. 16]. With m/n = 0.5, this is independent of δx. [B, Eq. 17]
- Kargère et al. (2025): drainage area at inflection ∝ δ; channel-head area independent of δ. [B]
- m: no paper found that gives an explicit m(Δx) rule. m is held fixed (0.5) in all simulations above. Changing m with Δx: BULUNAMADI.
- n: constant (n = 1) in all sources. Δx dependence of n: BULUNAMADI.
- The relation A_e = α A_c^β fitted by Hergarten (2020a) gives an exponent β that depends on θ (0.45 to 0.75 tested, lower β for larger θ). [B, lines 49–50]

### (2) Braun & Willett, Schwanghart & Scherler, Perron, Cordonnier
- Braun & Willett (2013): grid-spacing rule BULUNAMADI.
- Schwanghart & Scherler (2017): data-side only; no K/m rule. [Ö]
- Perron et al. (2008): constant-width sub-pixel scaling, cited by Hergarten (2020a). Full text ERİŞİLEMEDİ.
- Cordonnier (2016): BULUNAMADI.

### (3) Whipple & Tucker (1999), Lague (2014), Δx and slope scale, critical area
- Whipple & Tucker (1999): uplift–erosion number; PDF ERİŞİLEMEDİ. [B-öz]
- Lague (2014): SPIM valid only above critical area 0.1–5 km² [B]; A_cr separates colluvial and fluvial domains [B]; no Δx rule for K [B].
- Stock & Montgomery (1999): channel-head / critical-area content BULUNAMADI in search results.
- Critical drainage area and hillslope/channel transition: Hergarten (2020a) (A_c threshold, Eq. 14), Hergarten & Pietrek (2023) (A_h, transition-zone argument) and Kargère et al. (2025) (inflection and channel-head areas) are the three sources with explicit scale-dependence [B].

### (4) K and D (diffusion) when Δx changes; 20 km preview vs 5 km run
- Pure fluvial (no diffusion): K scales as α(δx) from Eq. 16 [B]. For m/n = 0.5 the factor is δx-independent in the nondimensional setup, so K can be kept constant in physical units. [B + T]
- With diffusion (hillslope model): physical erodibilities K_d, K_t fix A_h. Real A_h ∝ δx², so the nondimensional A_h must scale as δx^(−2) to keep physical parameters constant [B, PDF text]. This is the paper's stated rule.
- Diffusivity effect on channel area: channel-forming area ∝ D^0.8 [B].
- Hergarten (2020a) rescaling of K with A_c: K_eff = K · (A_c-dependent factor) with δ^(−2β) [B, derived].
- Consistency between 20 km and 5 km runs: [T] Using Hergarten (2020a) at β ≈ 0.5, changing δ from 20 km to 5 km (factor 4) changes the fluvial term by about 4 in the rescaled K. Hergarten & Pietrek (2023) requires A_h ∝ δx^(−2), i.e. a factor of 16 between 20 km and 5 km. Both are only approximate; the residual dependence (k_s 1.6–2.0) means 20 km and 5 km results will not be identical without re-tuning. No paper tests this specific pair.
- Multiresolution / adaptive mesh: DAC (Goren et al. 2014, cited in Armitage 2019) uses adaptive meshing; resolution-consistency was shown only for wavelength (2 cell counts). [B]

## 16. Practical implications (for the user's model)

1. Do not assume K is resolution-independent. Use Hergarten & Pietrek (2023), Eq. 16, if the model is pure stream power (no hillslope diffusion); α depends on n, m, L, T, and δx.
2. If diffusion is present, define A_c or A_h in physical units and rescale K_d / K_t with δx^(−2) (Hergarten & Pietrek 2023), or use the threshold rescaling of Hergarten (2020a) with β from fitting.
3. Check convergence on the 20 km and 5 km grids with a residual tolerance around 15–20% (k_s spread 1.6–2.0 in Hergarten 2020a). [T]

## 17. Not found / not accessible

- ERİŞİLEMEDİ: Whipple & Tucker (1999) PDF (TLS certificate error, not bypassed).
- ERİŞİLEMEDİ: Perron, Dietrich & Kirchner (2008) full text (not fetched; citing text only).
- BULUNAMADI: Hergarten 2025 "Resolution dependence of the stream power law" (title/author not in ESurf index search).
- BULUNAMADI: Cordonnier (2016) K vs cell area.
- BULUNAMADI: Gailleton (2019) multiresolution / adaptive mesh stream-power paper.
- BULUNAMADI: explicit m(Δx) or n(Δx) rule in any fetched source.
- BULUNAMADI: Braun & Willett (2013) grid-spacing rule (full text not fetched; only Landlab note).
- BULUNAMADI: Stock & Montgomery (1999) channel-head content (search only).
- Note: Hergarten 2020 (transport-limited) text was fetched; equation numbers not recoverable from the extraction for Eq. 11–16 in 2020a.

## 18. Source URLs

- https://esurf.copernicus.org/articles/8/841/2020/ (Hergarten 2020) [B]
- https://esurf.copernicus.org/articles/8/367/2020/ (Hergarten 2020a) [B]
- https://esurf.copernicus.org/articles/11/741/2023/ (Hergarten & Pietrek 2023) [B]
- https://esurf.copernicus.org/articles/13/403/2025/ (Kargère et al. 2025) [B]
- https://esurf.copernicus.org/articles/7/67/2019/ (Armitage 2019 short communication) [B]
- https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2014_Lague_ESPL.pdf (Lague 2014) [B]
- https://esurf.copernicus.org/articles/5/821/2017/ (Schwanghart & Scherler 2017) [Ö]
- https://esurf.copernicus.org/articles/5/47/2017/ (Campforts et al. 2017) [Ö]
- https://planetarygeoscience.uchicago.edu/doc/Whipple_and_Tucker_1999.pdf (Whipple & Tucker 1999) ERİŞİLEMEDİ
