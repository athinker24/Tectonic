# A: Grid options for global surface-process modelling (erosion, flow routing)

Status: COMPLETE for the sourced items; gaps listed in section 9.
Date: 2026-11-12
Labels: [B] primary source read (text/code/paper) | [D] official docs read | [O] search summary only | [E] encyclopedia | [C] my own calculation from the cited values (not in a source)
Access note: WebFetch returned DNS errors (getaddrinfo ENOTFOUND) for arxiv.org, landlab.readthedocs.io, joss.theoj.org and fastscapelib docs/GitHub (github 403). Sources marked "curl" were downloaded with curl through the proxy and converted to text locally. Downloads are in the session scratchpad, not in the repo.

## 1. Lat-long (equirectangular) grid
- Cell area on sphere (radius R, angles in radians): A = R^2 (sin phi1 - sin phi2)(theta1 - theta2). Source: johndcook.com/blog/2023/02/21/sphere-grid-area/ (curl) [B]. Sentence: "A = R ² (sin φ 1 − sin φ 2 ) (θ 1 − θ 2 )." Degrees version: "A = π R ² (sin φ 1 − sin φ 2 ) (θ 1 − θ 2 )/180." [B]
- Polar shrinkage, from the same formula with an equatorial row as reference [C]:
  - row centred 60 deg: area = 0.500 x equatorial row
  - row centred 80 deg: area = 0.174 x
  - row centred 89 deg: area = 0.0175 x
  - polar-most row (centre ~89.98 deg at 5 km): 0.00039 x; east-west width ratio cos(phi) is the same number, so aspect ratio of the polar cell (N-S over E-W) becomes very large. Cell aspect is therefore the practical problem, not only area.
- Cell counts [C] (equal-degree grid sized so the equatorial cell is ~h km, R = 6371 km):
  - 5 km: dlam = dphi = 0.0450 deg; 8006 x 4003 = 32,048,018 cells; one float64 field ~245 MiB.
  - 20 km: dlam = dphi = 0.1799 deg; 2002 x 1001 = 2,004,002 cells; one float64 field ~15 MiB.
- Earth radius used: fastscapelib HealpixGrid default radius 6.371e6 m [D] (see section 6). Cell sizes above use R = 6371 km.
- Landlab RasterModelGrid is planar (no spherical area) [D, from the Landlab grid reference list, section 6]; no Landlab source read here stating a lat-long mode. BULUNAMADI for Landlab lat-long support.

## 2. HEALPix (Gorski et al. 2005) [B]
- Source: arXiv astro-ph/0409513 (v1, 21 Sep 2004; the 2005 ApJ paper is the citation) https://arxiv.org/pdf/astro-ph/0409513 (curl; pdftotext).
- "A HEALPix map has Npix = 12Nside^2 pixels of the same area Omega_pix = pi/(3 Nside^2)." (Sec. 4.) [B]
- "Several such curvilinearly mapped coordinate patches (12 in the case of HEALPix, and 6 in the case of the COBE quad-sphere) are joined at the boundaries to cover the sphere." (Sec. 3 / Fig. 1 caption.) [B]
- "For a resolution parameter Nside, the pixels are layed out on 4Nside - 1 iso-latitude rings." (Sec. 4.) [B]
- "Pixel boundaries are non-geodesic and take a very simple form: cos theta = a + b x phi in the equatorial zone, and cos theta = a + b/phi^2 in the polar caps." (Sec. 5.3.) Equal area is verified analytically from this form. [B]
- Table 1 (sec. 3, p. 15): "The use of 32-bit signed integers for the pixel indexing currently restrict the resolution accessible to Nside <= 8192. The use of 64-bit signed integers will allow to reach Nside = 2^29." [B]
- Pixel-count table from the paper (Nside: Npix): 1024: 12,582,912; 2048: 50,331,648; 4096: 201,326,592. [B]
- Mean cell side from equal-area formula [C], Earth R = 6371 km:
  - Nside 256: 786,432 cells, ~25.5 km side
  - Nside 512: 3,145,728 cells, ~12.7 km
  - Nside 1024: 12,582,912 cells, ~6.4 km
  - Nside 2048: 50,331,648 cells, ~3.2 km
  - Nside 128: 196,608 cells, ~51 km
  - The table in the paper covers Nside = 2^k only (k = 0..29). Nside values between powers of two are not part of the paper's table. [B for the table, C for the sides]
- Available cell sizes for the target range (5 to 20 km): Nside 256 (25.5 km) and 512 (12.7 km) are the nearest powers of two. 20 km is not reachable exactly; 5 km falls between 512 and 1024. [C]
- Gap: no source read yet for HEALPix used in landscape/flow models except Fastscapelib (section 6). BULUNAMADI for a published erosion study using HEALPix.

## 3. Cubed sphere
- Source read: Putman & Lin 2007, J. Comput. Phys. 227(1): 55–78 [O] (search summary only; PDF at weather.gov mirror not opened). Summary: the paper compares "the gnomonic, conformal, and two numerically generated grids" and "the more uniform version of the quasi-orthogonal cubed-sphere grids provided better overall accuracy than the most orthogonal (and therefore, much less uniform) conformal grid." [O]
- Corner singularities: grid non-orthogonality affects advection "near the cubed-sphere corner singularities." [O]
- Cell count per face with N x N cells: 6N^2 total [C]. Example: N = 1024 gives 6,291,456 cells (~ 6 x 1024^2), mean side ~ 9 km [C, R=6371 km].
- Gap: no primary text read; no value for uniformity ratio (max/min cell area) in this source. BULUNAMADI as a sourced number.

## 4. Icosahedral / geodesic (Voronoi/Delaunay) grids
- Landlab IcosphereGlobalGrid [D] (source code read via curl): https://landlab.readthedocs.io/en/latest/_modules/landlab/grid/icosphere.html
  - Class name is IcosphereGlobalGrid (not IcosphereGrid). Constructor: radius=1.0, mesh_densification_level=0. [B]
  - "The default configuration is a spherical grid of unit radius that forms the spherical version an icosahedron (20 triangular patches, 12 nodes), with the dual complement representing a dodecahedron (12 hexagonal cells, 20 corners)." [B]
  - "The mesh_densification_level parameter allows you to densify this initial shape by subdividing each triangular patch into four triangles, with corresponding addition of nodes." [B]
  - "If you specify mesh_densification_level=1, you get a soccer ball: a combination of pentagons and hexagons as cells. Further densification produces more hexagons." [B]
  - "Because there are no boundaries, there is a 1:1 relationship between nodes and cells." [B]
  - "Patch area is calculated as the spherical (not flat) triangle area." [B]
  - "the present version of the component does not include algorithms to calculate distances or areas on an ellipsoid" [B]
  - Node count V = 10*4^n + 2 for densification level n [C, from Euler formula with F = 20*4^n, E = 30*4^n; consistent with the 4-way subdivision in the docstring]. Not yet verified by running the code.
- Node/cell counts and mean cell side [C, R = 6371 km]:
  - level 8: 655,362 cells, ~27.9 km
  - level 9: 2,621,442 cells, ~14.0 km
  - level 10: 10,485,762 cells, ~7.0 km
  - level 11: 41,943,042 cells, ~3.5 km
  - One float64 field: level 9 ~20 MiB, level 10 ~80 MiB.
  - Note: refinement is by factors of 4 in count (factor 2 in size), so 5 km and 20 km are not hit exactly; nearest levels are 10 (7 km) and 9 (14 km) for the target range; level 8 is 28 km.
- goSPL [B] (JOSS 2020, DOI 10.21105/joss.02804; PDF read locally, https://joss.theoj.org/papers/10.21105/joss.02804 via curl):
  - "create an unstructured spherical mesh used as input for gospl." [B]
  - "gospl can also be used with different mesh resolutions enabling better representation of surface processes in regions of interest ... while using lower resolutions to save memory allocation in other parts (deep marine regions for example)." [B]
  - "Compared to eSCAPE ... it allows for (1) horizontal advection to be accounted for and (2) multiple lithologies and associated compaction to be represented." [B]
  - The JOSS text does not say Voronoi vs Delaunay; the word "voronoi" appears only in a figure caption on the flow page (below). [B]
  - Later goSPL preprint (EGUsphere 2026-4124) described as "meshes of up to 23.7 million nodes" [O, search summary]; not read.

## 5. Flow routing on these grids (D8, MFD, multi-directional)
- goSPL flow page (curl): https://gospl.readthedocs.io/en/latest/tech_guide/flow.html [D]
  - "This assumption makes the emergent flow network highly sensitive to the underlying mesh geometry and most dendritic shape of obtained stream networks is often an artefact of the surface triangulation." [B]
  - "To reduce this effect, authors have proposed to consider not only the steepest downhill direction but also to represent other directions appropriately weighted by slope (multiple flow direction - MFD)." [B]
  - "The number of flow direction paths is user-defined and can vary from 1 (i.e. SFD) up to 6 (i.e. MFD) depending of the grid neighbourhood complexity. The weights are calculated based on the number of downslope neighbours and are proportional to the slope." [B]
  - "The weights range between zero and one and sum to one for each node." [B]
  - Method: parallel implicit drainage area (IDA) method (Richardson et al. 2014) adapted to unstructured meshes, written as a sparse linear system solved with PETSc. [B]
  - Cells for the flow solve are Voronoi areas: "Cells (i.e. voronoi area defining the region of influence of each vertex)". [B]
- Landlab FlowDirectorMFD [D, from the Landlab docs page, curl and search summary]: "This method works for both raster and irregular grids." [B, docs page text]. For raster grids diagonals are optional (diagonals=False default). [O]
- Landlab depression finder: "the depression finder only works with FlowDirectorSteepest and FlowDirectorD8" [O, search summary]; so depression handling does not work with MFD in Landlab. [O]
- Landlab boundary nodes: "boundary nodes ... do not have area and do not contribute flow to nodes" [O].
- Seibert & McGlynn 2007 triangular MFD (grid-based, not mesh-based): "avoids unrealistic dispersion on planar or concave hillslopes" [O, search summary].
- D8 limitations on irregular grids: not sourced. The search did not return O'Callaghan & Mark 1984 or Freeman 1991; BULUNAMADI for their text. Qin 2007 mesh MFD: not found.
- Landlab Voronoi/Delaunay + FlowAccumulator combination: source module imports VoronoiDelaunayGrid; the explicit combination is not documented on the pages read. Treat as "likely, unverified" [C].

## 6. Software support
- Landlab grid types [D] (curl): https://landlab.readthedocs.io/en/latest/user_guide/reference/grid.html — "Landlab presently supports multiple grid types. The base class for all of these grid types is ModelGrid." Listed: FramedVoronoiGrid, HexModelGrid, IcosphereGlobalGrid, NetworkModelGrid, RadialModelGrid, RasterModelGrid, VoronoiDelaunayGrid. [B]
  - No HEALPix grid in Landlab. Lat-long grid: not listed. [B]
  - Landlab IcosphereGlobalGrid: see section 4. [B]
- Fastscapelib [O, search summary of fastscapelib.readthedocs.io]: four grid types: profile (1D), raster ("8-node connectivity (i.e., including diagonals)"), triangular mesh (2D, irregular), and HEALPix ("defined on the sphere. It is meant for planetary scale simulations."). [O]
  - Fastscapelib HealpixGrid [D, curl of api docs]: "A HEALPix (Hierarchical Equal Area isoLatitude Pixelation) grid defined on the sphere." Initializer: nside (int), nodes_status, radius (default Earth radius in meters, 6.371e6). "A higher value sets a grid with a finer resolution and a greater size N (i.e., total number of grid nodes)." [B]
  - Fastscapelib flow routers [D, curl of guide and API index]: SingleFlowRouter, MultiFlowRouter, and a TriMesh class are listed; the Catchment (TriMesh) example. [O, not inspected in detail]
- goSPL [B]: see sections 4 and 5. Unstructured spherical mesh; MFD routing with 1 to 6 flow directions. [B]
- Note: goSPL is in fact close to the user's target (global, deep time, Voronoi-type cells), but its own docs and paper do not state a fixed resolution in km. [B]

## 7. Numerical summary (target 5 to 20 km)
Values in [C] from the formulas above, R = 6371 km.

| Grid | Level / setting | Cells | Mean cell side | Notes |
|---|---|---|---|---|
| Lat-long | 5 km equator | 32,048,018 | 5 km (equator); polar rows 0.00039 x area at 89.98 deg | severe polar aspect ratio |
| Lat-long | 20 km equator | 2,004,002 | 20 km (equator); polar rows 0.00157 x | same pathology, fewer cells |
| HEALPix | Nside 256 | 786,432 | ~25.5 km | equal area, 12 base patches, non-geodesic edges [B] |
| HEALPix | Nside 512 | 3,145,728 | ~12.7 km | |
| HEALPix | Nside 1024 | 12,582,912 | ~6.4 km | ~96 MiB per float64 field |
| Icosahedral | level 9 | 2,621,442 | ~14.0 km | Landlab IcosphereGlobalGrid [B for construction] |
| Icosahedral | level 10 | 10,485,762 | ~7.0 km | ~80 MiB per float64 field |
| Cubed sphere | N = 1024 per face | 6,291,456 | ~9 km | [C] only; not sourced |

Uniformity (max/min cell area) for lat-long: 1 / 0.00039 ~ 2600 at 5 km (polar-most row vs equator) [C]. HEALPix and icosahedral: equal area by construction [B for HEALPix; B for the icosphere docstring "Patch area is calculated as the spherical triangle area", but per-cell equality is not stated in the code read; treat icosahedral uniformity as unverified].

## 8. Interpretation (for the user's model, not in any source)
- Lat-long is the cheapest to write but has the polar problem in section 1. Its aspect ratio alone rules it out for flow routing without a polar cap treatment.
- HEALPix gives equal area and a clear cell count formula (12 Nside^2), supported by the primary paper and by Fastscapelib's HealpixGrid. Its base-pixel edges are non-geodesic.
- Icosahedral/geodesic grids (Landlab IcosphereGlobalGrid, goSPL unstructured mesh) are the usual choice for flow routing on the sphere: MFD on Voronoi-type cells is documented in goSPL [B]. Their cell sizes come in factor-2 steps, so exact 5 km or 20 km is not reachable.
- Cubed sphere is only backed by secondary text here; numbers beyond 6N^2 cells need a primary source.

## 9. Gaps (BULUNAMADI or not yet checked)
- Cubed sphere: primary text (Putman & Lin 2007) not read; uniformity numbers not sourced.
- D8 limitations on irregular grids: O'Callaghan & Mark 1984 and Freeman 1991 not found in search.
- Qin 2007 mesh MFD: not found.
- Landlab FlowDirectorD8/Steepest on VoronoiDelaunayGrid: not verified.
- Landlab lat-long support: none found.
- Fastscapelib guide_grids.html: fetched via curl, but no explicit mention of HEALPix flow routing; not confirmed.
- goSPL 2026 preprint (EGUsphere-2026-4124): search summary only.
- Icosphere node-count formula 10*4^n+2: derived by me, not run.
- The user's note that the tool's continent is "60K to 7G" is not a sourced fact and is not used here.
