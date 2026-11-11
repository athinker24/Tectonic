# D: How kinematics turns into elevation (research notes, 2026-11-11)

(Work in progress; facts have source URL right after them. UNVERIFIED = not confirmed from a source read.)

## 1. Terrain-generation style uplift rules
- Cordonnier et al. 2018 (TVCG, Sculpting Mountains): crust deformation treated as isochoric, local crust thickness proportional to volume of crust material q in a cell; thickness change rate dq/dt = (q - q0)/dt; uplift u0 = 0 on the stable side of a procedurally defined fault (iso-level of q), and u0 = alpha * dq/dt elsewhere. alpha is a scaling coefficient chosen so average uplift is 5.0e-4 m/yr (0.5 mm/yr), "a geologically consistent value (uplift rate in mountain belts rarely exceed a few mm/yr)". They explicitly neglect isostasy (no crustal root depression) and fault dip. Total simulation time 5e6 yr; stream power erosion with n=1, m=0.5, k 2.5e-7 to 8e-7 /yr. https://www.cs.purdue.edu/homes/bbenes/papers/Cordonnier18TVCG.pdf
