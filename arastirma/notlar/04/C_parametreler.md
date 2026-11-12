# Topic C: parameters of landscape evolution models (stream power K, m, n, diffusion, h_max, lithology)

Date of research: 2026-11-12. Status: IN PROGRESS (sections added as sources are read).

Method note: primary PDFs were downloaded (curl) and converted with pdftotext. Quotes below were checked against the converted text unless marked UNVERIFIED.

## 1. Stream power law: basic form and units

- Stream power incision: I = K A^m S^n (Lague 2014 Eq. 1). K "is often called erodibility and is a measure of incision efficiency". A = upstream drainage area, S = topographic slope. Source: https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2014_Lague_ESPL.pdf (Lague 2014, ESPL 39, 38-61, DOI 10.1002/esp.3462, also https://doi.org/10.1002/esp.3462).
- Lague 2014 Eq. 2: dh/dt = U - K A^m (dh/dx)^n, with U the baselevel lowering / rock uplift rate. Same source.
- Hergarten 2020: "The parameter K is denoted erodibility. It is a lumped parameter subsuming all influences on erosion other than channel slope and catchment size, so it is not only a property of the rock but also depends on climate in a nontrivial way (e.g., Ferrier et al., 2013; Harel et al., 2016)." Source: https://esurf.copernicus.org/articles/8/367/2020/esurf-8-367-2020.pdf (Earth Surf. Dynam. 8, 367-377, 2020).
- Units (derived, dimensional check): with A in m^2 and E in m/yr, K A^m S^n requires K in yr^-1 m^(1-2m) when S is dimensionless. For m = 0.5 this reduces to K in yr^-1 (the Cordonnier value 5.61e-7 yr^-1 is consistent with this). For other m the unit of K changes with m, so K values reported with m = 0.4 or m = 0.5 are not directly comparable (Hergarten 2020 says the same: "the unit and meaning of the erodibility K would change").

## 2. Exponents m, n and concavity theta = m/n

- Lague 2014 explains that the SPIM can be derived "from simple energetic considerations (i.e., as the unit rate of energy expenditure on the channel bed and banks yielding m = 0.5 and n = 1)". Source: Lague 2014 (same PDF).
- Lague 2014: "the downstream decrease of channel slope with drainage area often observed in nature is well reproduced if m/n ~ 0.5 and U = I." Same source.
- Lague 2014 on concavity: "No systematic compilation of theta exists ... but a range of 0.4 to 0.6 is often reported (e.g. Kirby and Whipple, 2012; Whipple, 2004)." Also: "A reference concavity exponent of theta = 0.45 is now routinely used to compare channel profiles and individual reaches from different locations (Whipple, 2004; Whipple et al., 2013; Wobus et al., 2006a)." Source: Lague 2014.
- Lague 2014: theta "does not vary with uplift rate or lithology in a statistically significant way" in detailed single-factor studies (Duvall 2004; Kirby and Whipple 2001; Lague 2000; Ramsey 2006; Snyder 2000). Same source.
- Lague 2014 on threshold/stochastic effects: "typical values for m_s and n_s are 1.4 and 2.2 for high discharge variability ... and 2.8 and 4.7 for very low discharge variability" (effective exponents of the upscaled threshold-stochastic model, Eq. 23 context; assumptions c ~ 1, b ~ 0.3). Source: Lague 2014. Meaning: effective exponents of a SPIM can differ from the simple m = 0.5, n = 1 when thresholds and discharge variability matter.
- Lague 2014 notes the stream power exponent n can be > 1 in threshold-dominated regimes ("the river obey a non-linear SPIM (n>1)"). Source: Lague 2014 abstract.

## 3. Hergarten 2020: grid resolution and the threshold drainage area

- Central result: "This scaling problem causes a strong dependence of the resulting topographies on the spatial resolution of the grid." Source: Hergarten 2020 abstract (same PDF).
- Scaling approach: a threshold catchment size A_c separates channel sites (A >= A_c) from hillslopes. Fluvial erosion is rescaled by an area factor A_e = alpha * A_c^beta (Hergarten 2020 Eq. 14), with beta in [0.41, 0.46] from the simulated networks (Eq. 13: P(A) ~ A^-beta). Source: Hergarten 2020 (same PDF).
- Dimensional form (Eq. 15): E = (alpha/delta^2)... with A_c in physical area, the fluvial term scales as delta^(-2 beta); for beta = 0.5 it scales as 1/delta.
- Practical formula proposed (Eq. 16): E = (sqrt(2 A_c) / delta) K A^m S^n, with A_c in DEM pixels and delta the grid spacing, alpha = sqrt(2) "a reasonable estimate" for A_c of a few to 100 pixels at about 100 m resolution. Source: Hergarten 2020 (same PDF, Sect. "Numerical examples" / Eq. 16).
- Hergarten 2020 limitation: "In combination with such processes, e.g., diffusion, the dependence on the spatial resolution is not completely removed." Same PDF, Conclusions.
- Hergarten 2020 on breakdown of Flint's law: "A breakdown of Flint's law ... was reported at catchment sizes between about 0.1 and 5 km2 (Montgomery and Foufoula-Georgiou, 1993; Stock and Dietrich, 2003; Wobus et al., 2006)." Same PDF.
- Hergarten 2020: "Reasonable estimates of A_c are probably between ... a few to 100 DEM pixels" at 100 m resolution. Same PDF.
- Secondary (from search snippet, UNVERIFIED in full text): a 2025 paper in Earth Surf. Dynam. 13, 403-415 (https://orca.cardiff.ac.uk/id/eprint/179682/1/esurf-13-403-2025.pdf) reports that channel heads form at a resolution-independent drainage area. Not yet read.

## 4. Cordonnier et al. 2016 (computer graphics terrain paper): parameter values used

Source: https://www.cs.purdue.edu/homes/bbenes/papers/Cordonier16CGF.pdf (Eurographics 2016, Computer Graphics Forum 35(2)). Read from the converted PDF.

- Stream power Eq. (1): h_t = u(p) - k A(p)^m s(p)^n. Text: "The constants m and n depend on rock strength, climate, and the ... are poorly understood, the ratio m/n is constrained by the shape of the stream profiles and is thought of being m/n ~ 0.5 [WT99]. As in most geomorphological studies, we use n = 1 and m = 0.5." Same PDF.
- Erosion rate: "We set the erosion rate to k = 5.61 10^-7 y^-1 for mountains to culminate at about 2 000 m." Same PDF (Sect. 6). Units: yr^-1 (consistent with m = 0.5 as above).
- Maximum uplift: "U = 5.0 10^-4 m/y ... which is the average uplift among earth mountains." Domain 50 x 50 km^2. Same PDF.
- Time step: dt = 2.5e5 yr. Same PDF.
- Empirical relation: "We made a series of experiments ... It turned out this relation is linear and the height in kilometers follows the rule h_max = 2.244 u/k." Same PDF (Sect. 6.4). Consistency check: u/k = 5.0e-4 / 5.61e-7 = 891; 2.244 x 891 = 2000 m, matching the stated 2000 m. The relation is an empirical fit for this model and these units (u in m/yr, k in yr^-1), not a general law (the paper itself says the parameters "are not intuitive to set").
- Thermal limit: "if the result of the stream power equation leads to slopes higher than 30 degrees, we reduce the change of elevation so as to keep slopes in the prescribed range." Same PDF (Sect. 5). Also: "the usual talus angle for thermal erosion [MKM89]" (30 degrees). Same PDF.
- Cordonnier notes the paper's own relation is for a steady-state uniform regime: "the stream power equation ... reached an equilibrium state in a region where u and k are constant", giving s ~ A^(-m/n). Same PDF.

## 5. Lague 2014 review, additional quantitative points (read from PDF)

- Steepness vs incision: "channel steepness only increases linearly with incision rate in one dataset ... the range of ksn reported on earth covering a little more than one-order of magnitude (from ~20 to 500 m^0.9) for nearly three orders of magnitude change in incision rates (0.02 to 14 mm/yr)." Source: https://wpg.forestry.oregonstate.edu/sites/default/files/seminars/2014_Lague_ESPL.pdf (Lague 2014, Sect. on steepness/incision compilation, Fig. 1). This is the "nearly three orders of magnitude" in incision rate that is closest to the "four orders of magnitude" phrasing in the task (we did NOT find the phrase "four orders of magnitude" in Stock and Montgomery 1999 text; see Section 9).
- Erodibility ranges from instantaneous bed erodibility: "the instantaneous bedrock erodibility k_e are within one-order of magnitude between these three sites [Liwu, SGM, Rio Torto] ... despite an order of magnitude difference in incision rate and runoff (0.24 m/yr in the SGM versus 2.4 m/yr in Liwu)." Units of k_e: m^(5/2) s^2 kg^(-3/2) (for the threshold-stochastic formulation with a = 3/2). Values quoted: ~7e13 (Liwu), ~2.4e12 (SGM), ~2.4e13 (Rio Torto, Deff = 5 cm). Source: Lague 2014 (same PDF).
- Lague 2014 Eq. (3) (steepness) is ks = k_sn; theta used with reference 0.45; "an outcome of any incision model is that Equation 3 must be verified with theta of the order of 0.5 at SS."
- Lague 2014: "Note that Equation 3 only applies above a critical drainage area" (steepness index applies above a critical area; relevant when setting an area threshold).
- Lague 2014 on knickpoint celerity: the celerity depends on erodibility and drainage area "as in Anderson, 1994; Whipple and Tucker, 1999"; "Because m/n ... the celerity becomes dependent on slope and the KP geometry" (PDF lines around the knickpoint section). Exact celerity formula still to be read (see Section 7, TODO).
