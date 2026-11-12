# B: Map projection distortion and area measurement, research notes

Status: research complete for items 1 to 5. Open items are listed at the end.

Tags: [B] primary text read (official page/PDF fetched and extracted), [D] official documentation (EPSG, pyproj API), [Ö] summary or search snippet only, not verified in full text, [E] encyclopedia (Wikipedia), [H] my own calculation (script in the scratchpad, reproducible; values are not from a source).

Access notes:
- Direct WebFetch failed with DNS errors for pubs.usgs.gov, esri.com, epsg.org, pyproj4.github.io and geo.hunter.cuny.edu.
- curl (through the agent proxy) worked for pubs.usgs.gov, epsg.org, pyproj4.github.io, en.wikipedia.org and deck.gl. esri.com returned 403. The Wikipedia Mollweide page returned 429 (rate limit), so Mollweide is covered only by [H].
- Text was extracted with the scratchpad helper oku.py (read before use) and pdftotext.
- Scripts (outside the project): scratchpad/tissot_calc.py and scratchpad/dist_calc.py. pyproj 3.8.0 was installed into scratchpad/pylib.

## 1. Distortion measures and projection choice for a regional continent

### 1a. Definitions
- [B] Snyder, J. 1987, Map Projections: A Working Manual, USGS Professional Paper 1395, doi:10.3133/pp1395, 385 p. (catalog page at pubs.usgs.gov/publication/pp1395 read; PDF at pubs.usgs.gov/pp/1395/report.pdf, 22 MB, text extracted and read).
- [B] Snyder sec. 4, eq. 4-1: sin(w/2) = |a - b| / (a + b), where a and b are the semi-axes of the Tissot indicatrix and w is the maximum angular deformation. Snyder notes that some texts use 2w instead of w.
- [B] Snyder eq. 4-2 and 4-3 for cylindrical projections: h = (dy/dphi)/R, k = (dx/dlambda)/(R cos phi). h is the meridian scale factor, k the parallel scale factor.
- [B] Snyder: area scale factor = h x k; shape factor = h/k.
- [B] Snyder: "An infinitely small circle on the Earth projects as an infinitely small, but perfect, ellipse on any map projection. If the projection is conformal, the ellipse is a circle."
- [E] Wikipedia "Tissot's indicatrix": equal-area projections give indicatrices of equal area; conformal projections give circles (scale factor = radius).
- [D] EPSG Guidance Note 7-2, method 1024 (epsg.org, read): omega = 2 asin(|h - k| / (h + k)). This is the same as the Snyder relation when a and b are replaced by h and k.

Snyder example [B]: for an Albers projection on a sphere of radius 6,370,997 m, h = 1.00132 and k = 0.99868 at 45 N. Area scale factor = 0.99775 relative to the Clarke 1866 ellipsoid. Snyder also notes a sphere-vs-ellipsoid shape error of about 0.68% at the equator for a conformal projection.

### 1b. Numerical comparison [H]
Method: R = 6371 km sphere; Tissot Jacobian by finite differences using pyproj 3.8.0 (PROJ). Test band: 10 N to 77 N (67 deg span, about 7450 km north-south at R = 6371 km). Longitude offsets 0, 15 and 30 deg from the central meridian. Conic standard parallels: 21.17 and 65.83 deg (1/6 and 5/6 of the band); latitude of origin 43.5 deg. The band is an ASSUMPTION; the user's grid codes could not be converted to coordinates (see open items).

| Projection | Max abs(a*b - 1) over band | Area-weighted mean abs(a*b - 1) | Max omega (deg) |
|---|---|---|---|
| Equidistant cylindrical (std 0) | 3.445 | 0.463 | 78.5 |
| Mercator | 18.76 | 1.521 | 0 (conformal) |
| Lambert cylindrical equal-area | 0 | 0 | 129.3 |
| Mollweide | 0 | 0 | 54.8 |
| Robinson | 0.782 | 0.143 | 66.8 |
| Winkel Tripel | 1.912 | 0.280 | 59.0 |
| Albers equal-area conic (std 21.2/65.8, lat0 43.5) | 0 | 0 | 31.7 |
| Lambert conformal conic (same standards) | 0.357 | 0.102 | 0 (conformal) |

Point values [H] (longitude offset 0):
- Mercator: a = b = 1.414 at 45 deg (a*b = 2.000); a*b = 4.000 at 60 deg; 14.93 at 75 deg.
- Equidistant cylindrical: a*b = 1/cos(phi), i.e. 2.000 at 60 deg and 3.864 at 75 deg.
- Lambert cylindrical equal-area: a*b = 1 everywhere, but omega = 73.7 deg at 60 deg and 122 deg at 75 deg.
- Mollweide: omega = 3.0 deg at 45 deg; 43.2 deg at 75 deg.
- Winkel Tripel: a*b = 1.262 at 45 deg; 1.605 at 60 deg.
- Robinson: a*b = 0.815 at the equator; 0.944 at 45 deg; 1.238 at 60 deg.

Source status of the projection rows:
- [B] Snyder: cylindrical equal-area is undistorted only along the equator, and the Albers projection is recommended for equal-area mapping of mid-latitude regions that are mainly east-west in extent. Snyder also says the cylindrical equal-area is well suited to regions that are mainly north-south in extent or that lie near the equator.
- [E] Wikipedia "Lambert cylindrical equal-area": undistorted along the equator (its standard parallel); distortion increases rapidly toward the poles.
- [E] Wikipedia "Albers projection": two standard parallels; distortion is minimal between them.
- [E] Wikipedia "Robinson projection": neither equal-area nor conformal; a 5-degree table of X and Y factors. Values used: 0 deg 1.0000 / 0.0000; 45 deg 0.8962 / 0.5571; 90 deg 0.5322 / 1.0000. The Robinson scale constants were not verified.
- [E] Wikipedia "Winkel tripel" was read but gave no usable formulas. Winkel values are [H].
- Mollweide: Wikipedia returned 429. Mollweide values are [H] only.

### 1c. Projection choice (for a mid-latitude continent with about 67 deg of north-south extent)
- [H] With the assumed band, Albers equal-area conic has zero area distortion and the smallest maximum angular distortion among the equal-area options (31.7 deg). Lambert conformal conic has zero angular distortion but up to about 36% area distortion.
- [H] Mercator and equidistant cylindrical are unsuitable for this band. Lambert cylindrical equal-area reaches 129 deg of angular distortion at 77 deg.
- Recommendation: Albers equal-area conic with standard parallels at 1/6 and 5/6 of the north-south span (or chosen to minimise distortion for the true extent). If the true east-west extent is small relative to north-south, re-run the script before choosing, since Snyder's advice on cylindrical forms depends on that shape.

## 2. Area-weighted measurement on the sphere

- [H] Area of a 1 deg by 1 deg cell (R = 6371 km): A = R^2 x dlambda x (sin phi2 - sin phi1).
  - 0 to 1 deg: 12,363.7 km^2; 30 to 31 deg: 10,653.3; 45 to 46 deg: 8,666.2; 60 to 61 deg: 6,088.4; 75 to 76 deg: 3,095.7.
  - The closed form R^2 (pi/180)^2 cos(mid-latitude) matches to about 0.1 km^2.
- [H] Sum of all 1 by 1 deg cells = 510,064,472 km^2 = 4 pi R^2 (exact match).
- [H] For the 10 to 77 deg band, the true share of the globe's area is 40.04%. Counting equal-height rows (naive, no cos weighting) gives 37.22%. On an equirectangular grid, each row must be weighted by cos(phi), or by sin differences.
- [D] pyproj Geod.polygon_area_perimeter(lons, lats): returns (area in m^2, perimeter in m) for a geodesic polygon (pyproj API page read). The sign convention (positive = counter-clockwise) comes from a search summary [Ö] and was not confirmed in the page.
- [Ö] pyproj issue #1399 reports geometry_area_perimeter returning 0 for a global polygon. Not verified; test before relying on it for a whole-globe mask.

## 3. Great-circle distance on R = 6371 km

- [H] Haversine (R = 6371 km) equals the exact sphere geodesic from pyproj (Geod with a = b = R) to all printed digits in every test pair. The haversine formula is therefore exact on this sphere.
- [H] Haversine vs WGS84 ellipsoidal geodesic (pyproj):
  - 1 deg meridian at equator: 111.195 vs 110.574 km (+0.56%)
  - 100 km at 45 deg: +0.05%
  - 1000 km east-west at 45 deg: -0.28%
  - 67 deg north-south (10 to 77 N): 7450.06 vs 7444.34 km (+0.08%)
  - 30 deg east-west at 60 deg: -0.36%
  - Near antipodal: +0.001%
- [H] North-south span 10 to 77 deg: 7450.1 km on R = 6371 km (67 deg times 111.195 km per deg). This matches the user's "approximately 7450 km".
- [E] Wikipedia "Vincenty's formulae": the inverse and direct methods are accurate to within 0.5 mm on the Earth ellipsoid, and more accurate than spherical great-circle methods.
- [Ö] Search summaries (Wikipedia haversine page not read in full): haversine is better conditioned than the spherical law of cosines for small distances.
- Not done: Vincenty itself was not implemented or run. The WGS84 reference here is pyproj's PROJ geodesic, whose algorithm was not checked.
- [B] Snyder: the radius of the Earth taken for a 1:5,000,000 map was 6,371,204 m, chosen to have approximately the same surface area as the International ellipsoid. This differs from 6,371,000 m by 0.003%.

## 4. Phone display (mobile web)

- [D] EPSG method 1024, "Popular Visualisation Pseudo Mercator" (read): uses spherical Mercator formulas on geodetic latitude with R = a = 6,378,137 m (WGS84 semi-major axis). "This method is not conformal: scale factor varies as a function of azimuth." The formula should not be used poleward of 88 deg.
- [D] EPSG 1024 scale factors: h = R / (rho cos phi) (meridian), k = R / (nu cos phi) (parallel), with rho and nu the WGS84 radii of curvature.
- [E] Wikipedia "Web Mercator projection": uses the WGS84 equatorial radius; projects ellipsoidal coordinates as if on a sphere.
- [H] Values from the EPSG formulas (relative to the ellipsoid, R = a):
  - lat 0: h = 1.0067, k = 1.0000, areal 1.0067, omega 0.39 deg
  - lat 30: h = 1.1596, k = 1.1537, areal 1.338, omega 0.29 deg
  - lat 45: h = 1.4166, k = 1.4118, areal 2.000, omega 0.19 deg
  - lat 60: h = 1.9983, k = 1.9950, areal 3.987, omega 0.10 deg
  - lat 75: h = 3.8534, k = 3.8516, areal 14.84, omega 0.03 deg
  - Latitude limit: 85.0511 deg (computed).
- The large areal distortion (about sec^2 phi) is inherent to Mercator. The angular distortion of EPSG:3857 is small (under 0.4 deg in these samples).
- Map libraries:
  - [B] MapLibre style specification "projection" property (maplibre.org/maplibre-style-spec/projection/, read): default "mercator"; the page's example uses "vertical-perspective" with a zoom interpolation. The full list of types was not visible in the extracted page.
  - [Ö] MapLibre GL JS 5.0.0 (January 2025) added a globe projection. Only from a search summary; not verified in a primary page.
  - [B] deck.gl GlobeView (deck.gl/docs/api-reference/core/globe-view, read): marked experimental; "No high-precision rendering at high zoom levels (> 12)"; "Known rendering issues when using multiple views mixing GlobeView and MapView".
  - [Ö] Development Seed (December 2024) reported deck.gl as the only library handling data near the poles acceptably in that evaluation, before MapLibre 5.0. Not read in full.
  - Leaflet: [B] reference page (leafletjs.com/reference.html) read partially. It defines CRS objects that combine a projection and a transformation (SimpleCRS, EPSG3857, EPSG4326) and says Leaflet CRS measure distance in meters by default. Custom projections are possible through the CRS interface, but no ready-made non-Mercator projection was found. BULUNAMADI for a list of built-in non-Mercator projections.
  - Canvas drawing with a custom projection: not researched. BULUNAMADI.

## 5. Converting an equirectangular PNG mask to real area

- [H] Equirectangular mask, one row per latitude band: area = sum over pixels of R^2 x dlambda x (sin phi2 - sin phi1), with dlambda = pixel width in radians. Using R = 6371 km for the sphere.
- [H] Alternative: reproject the mask to an equal-area CRS and count pixels times pixel area. Relies on GDAL's gdalwarp reprojection [B: gdalwarp docs read; reprojects to any supported projection, pixel size in SRS units, so a choice like an equal-area CRS is needed]. Not run: GDAL CLI and rasterio are not installed here.
- [D] pyproj Geod.polygon_area_perimeter for vector outlines: a polygon traced from the mask boundary gives geodesic area in m^2 directly. Check sign and closure per the API notes.
- Caveat: the 1 deg cell area and sum checks above confirm the spherical formula; a mask scanned from a Photoshop black-and-white drawing needs a georeference (pixel-to-lon/lat transform) before any of these formulas apply.

## Open items
1. The user's grid codes (60K-7G, 44B-43D) were not converted to latitude and longitude. The band used (10 to 77 N) is an assumption. Please confirm the coordinate system or extent; the scripts can be re-run with the real bounds.
2. Snyder's section on Albers standard-parallel selection was not read in full text. Standard-parallel choice above is my own rule of thumb.
3. Robinson scale constants, Winkel Tripel and Mollweide formulas were not checked in primary text.
4. Leaflet custom CRS API and MapLibre globe support were not verified in primary pages.
5. GDAL/rasterio area workflow was not run locally; Esri pages were blocked (403), and BULUNAMADI for a GDAL-specific area-of-raster recipe.
