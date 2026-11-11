# A. Merak Map Maker and GPlates for worldbuilding (research notes, 2026-11-11)

Method note: merakmapmaker.com is a client-side single-page app (React/Vite). The HTML shell carries no content; the sitemap only lists `/`, `/pricing`, `/refunds`, `/privacy`, `/terms` (https://merakmapmaker.com/sitemap.xml). All Merak facts below therefore come from the **production JS bundle and worker bundles served by the site** (string literals such as the in-app "What's new" changelog, pricing table, UI labels and tooltips), fetched 2026-11-11:
- MAIN = https://merakmapmaker.com/assets/index-3D_Y8mU_.js
- CLW = https://merakmapmaker.com/assets/climateLab.worker-CGVWvzw9.js
Bundle filenames are hashed and will change on the next deploy. No Steam, itch.io, Patreon, Kickstarter, YouTube or press pages for "Merak Map Maker" turned up in web search (two searches, no relevant hits). The app links only to a Discord (https://discord.com/invite/7GyvZT6mJd) and a subreddit (https://www.reddit.com/r/MerakMapping/). reddit returns 403, so I did not read the subreddit.

---------------------------------------------------------------------
## PART 1: Merak Map Maker

### 1.0 What it is / platform / price
- Tagline (meta description): "Build the world you have been imagining. Sculpt real or invented terrain, paint fantasy maps by hand, grow cities street by street, and run the history of it all." (https://merakmapmaker.com)
- Platform: browser web app. Free tier: "The whole editor, on your own machine." (MAIN, pricing table `IG`)
- Pricing (MAIN, pricing table; the page is https://merakmapmaker.com/pricing):
  - **Free, $0 "forever"**: every map mode (Earth, blank world, fantasy, city); every tool (sculptor, Planet Advisor, city generator, 3D view); local save/open; **PNG export up to 2K**; timeline 10 years per scenario. Limits: watermark, no cloud save/autosave, no imported art/fonts/textures/flags, **no map projections** or cloud layers, personal use only.
  - **Premium, $6 per month**: no watermark, **export up to 16K** including 3D renders, unlimited timeline, cloud saving for 100 maps, autosave, local save folder, imports of art/fonts/textures/flags, map projections (Mercator, globe and others), cloud/weather layers, commercial licence.
  - **Founder's Lifetime, $49.99 once, "first 300 only"**: Premium for as long as Merak runs, cloud saving for 500 maps, founder badge.
  - Export px caps in code: `exportPx:[2048,16384,16384]` for free/premium/lifetime (MAIN).
  - Payments go through Polar (`/billing/polar/checkout`) (MAIN).
- Versions: no semantic version numbers. Releases are dated entries in the in-app changelog (MAIN, array `rA`, which also feeds the "What's new" popup, key `merak.whatsNewSeen`). **Latest entry: 8 November 2026, "Custom tectonics and projections".** Oldest entry in the list: 9 August 2026. Full list:
  - 2026-11-08 "Custom tectonics and projections": "**Tectonics: draw your own plates, run 200 million years, and save it as a GIF.**" Also Discworld and Custom projections, user-drawn travel routes, and "Biomes: lowered or sunk land changes to fit its new height."
  - 2026-11-01 "Geography Lab": "Geography Lab: change your planet and see its climate, land and life." Also: "**Tectonic history: 250 million years of moving plates. Saves as a GIF.**", "**Apply bathymetry: a tectonic sea floor, with ridges and trenches from your plates.**", "Import: Place on existing.", Water/Travel/Hazards/Resources tabs, solar-system skies.
  - 2026-10-26 "Solar system and sea styles": customisable solar system; "Realistic sea floor brushes, made from real ocean ridges, trenches and banks"; "**Grayscale export at your PNG size, up to 16K.**"
  - 2026-10-17 "Fine detail": "real terrain texture when you zoom in"; "Smooth coastlines up close, with no staircase edges"; "Real mountain brushes: pick a place in Sculpt > Shape, from the Alps to the Himalaya"; snow on peaks and ridges.
  - 2026-10-09 "Terrain upgrade": Render > Realistic; "Auto biomes: open Planet Advisor, press Analyze planet, scroll down, press Apply biomes."
  - 2026-10-06 "Hachured relief".
  - 2026-09-30 "Faster loading"; Advisor legend.
  - 2026-09-28 "Regions and provinces": "Coast lasso follows the coastline exactly."; "**Coastline lock added to the Sculpt toolbar.**"; "More accurate small rivers."
  - 2026-09-21 "Globe for blank worlds": "Globe projection for blank worlds, editable while sculpting."; river width slider.
  - 2026-09-14 "Auto biomes"; "Typed elevation for sculpt tools and import."
  - 2026-09-08 "Grayscale export added. Open it from Menu > Poster."
  - 2026-09-04 to 06 "Export improvements": "Better 16K and highest quality exports."
  - 2026-09-01 "Regional maps": "HD regional maps added. Open them from Planet Advisor in the tool rail."
  - 2026-08-23 "Tutorials": guided tour; "Advanced world generation options."; "Exact measurements on heightmap import."
  - 2026-08-09 "Fixes": "Heightmap import has a placement box."; "Better coastline detection in Trace Land."
  (all: MAIN, `rA`)

### 1.1 Tectonic plate simulation
Both modes sit in the "Geography Lab" panel. Its tabs are Climate, Water, Travel, Hazards, Resources, Items, **History**, **Tectonics** (MAIN).
- Restriction: "Tectonics works on a whole world you made, not on Earth or a region." (MAIN). The code gates it on terrain that is neither the Earth preset nor a region/HD region (`n4`).

**(a) History tab = reconstruction of the past from the present map (added 1 Nov 2026)**
- Changelog: "Tectonic history: 250 million years of moving plates. Saves as a GIF." (MAIN, 2026-11-01)
- The time slider runs from "250 Myr ago" to "50 ahead". Labels read "N Myr ago" / "N Myr ahead" / "Today". Constant `Zm=[-50,250]` (MAIN).
- Input: the existing relief and land of the user's world. Plates are **read from the land** (button "Plates from the land": "Drop the kept plates. Read new ones from the land."), with inferred Euler poles and a "motionFit". The worker `history` job takes `{terrain:{height}, rivers, edits, tecBase}` and returns boundaries flagged `inferred:true` (CLW; MAIN). Inferred labels read like "Plate N: drifting <dir> at X cm/yr" (MAIN).
- Options in History: "Today's coasts" ghost overlay, "Collisions", "Original plates, faint" ("The plates as read from the land, drawn faintly over yours"), "Geology map", "Save GIF" (file `tectonic-history`). The GIF frames are labelled "N million years ago" (MAIN).
- Fixed coastline? **Yes, implicitly.** The History tab is a view. The present (t = 0) is the user's unchanged map, and the past is a kinematic rewind of plates inferred from it. There is no "apply" button in History (only Play, Back to today and Save GIF found) (MAIN). How faithfully plates are inferred, and what happens at plate edges going back, I could not judge from the minified code (UNVERIFIED).

**(b) Tectonics tab = forward simulation from today (added 8 Nov 2026)**
- Changelog: "Tectonics: draw your own plates, run 200 million years, and save it as a GIF." (MAIN, 2026-11-08)
- Inputs (MAIN, Tectonics panel strings):
  - Starting terrain: the current world's height field. `tecRun` takes `{terrain:{height}, edits, seed, rifts, hotspots, erosion, tecBase}`.
  - Plates: by default read from the land ("Plates from the land"). They can be edited with "Draw a plate" ("Draw a closed shape. It becomes a plate."), "Match borders" ("On: a drawn plate stays inside the plate you draw it in. Off: it takes everything inside its outline."), "Adjust borders" ("Lasso ground into a plate, or cut it out.", Add/Cut), split ("Draw across a plate"), "Click to add a plate", "Merge into one plate", "Remove all plates", "Reset" ("Undo all plate edits"). The worker refuses more than 120 plates ("too many plates") (CLW).
  - Per-plate motion: heading in degrees and speed in cm/yr. Speed input is min 0, max 15, step 0.5, tooltip "**Speed, cm/yr. Earth: 1 to 10.**" (MAIN)
  - Per-boundary settings: "Boundary regime", which can be auto from plate motion or Subduction / Continental collision / Transform / spreading. Legend strings: "Neither sinks. Fold mountains." (collision), "Plates slide past. Fault, no relief." (transform), "Plates pull apart. New sea floor." (divergent). Also "Subducting plate" (choose which plate subducts), "Uplift rate" (slider 0 to 3 in steps of 0.25, "Uplift multiplier") and "Magmatism" ("Volcanoes along this boundary") (MAIN).
  - Run toggles: "Continental rifting" ("Continents split over time."), "Fluvial erosion" ("Rivers wear land down as it rises."), "Mantle plumes" ("Hotspots make volcanic island chains.") (MAIN).
  - Button: "Run 200 million years" / "Run again". Output is a time slider labelled "N million years on" with an event list such as "<t> Myr: P3 rifts apart" or "P1 and P2 lock together". Display options: "Boundaries" ("Red trench, orange collision, yellow new sea floor.") and "Original coasts" ("Show today's coasts"). "Save GIF" saves the run as a GIF (MAIN).
  - "**Apply this moment (N Myr on)**" replaces the map with that future state. Toast: "The world N million years on is your map now. Its rivers were removed: add them again for the new land. Ctrl+Z undoes it." (MAIN)
- Fixed coastline? **No.** The forward run moves the land, and Applying replaces the coastline; only the "Original coasts" ghost overlay remains. The time step appears to be 2 My (toast computes `s*2` million years; frame labels use `V*2`) (MAIN; inferred from code, treat as likely).
- Internal detail of possible interest: ocean-floor age is initialised from depth as `age = min(180, max(0, ((-z - 2500)/350)^2))` My for non-continental cells (CLW, function `dc`). This is a depth-to-age (half-space-cooling-like) relation.
- "Apply bathymetry" (1 Nov 2026) builds a tectonic sea floor. Worker progress strings: "Measuring the coasts", "Drawing mid-ocean ridges", "Cutting fracture zones", "Placing trenches", "Shaping the floor", "Laying real ridges, trenches and banks", "Writing the depths" (CLW). Boundary explanations: "Oceanic–continental subduction → offshore TRENCH + VOLCANIC MOUNTAIN ARC on the coast, Andes-style"; "Continental collision → FOLD MOUNTAINS, Himalaya-style"; "Sea-floor spreading → MID-OCEAN RIDGE"; "Continental rifting → RIFT VALLEY with lakes and volcanoes"; "Transform boundary → STRIKE-SLIP FAULT" (CLW). A geology map uses the classes Sedimentary platform, Foreland basin, Fold mountains, Volcanic arc, Worn-down mountains, Passive margin (CLW).
- Separately, there is a Sculpt "Coastline lock" (28 Sep 2026), presumably so sculpting does not alter the coast (exact semantics UNVERIFIED) (MAIN, `rA`).

### 1.2 Heightmap import/export
- Internal grid: `de=4096` wide, `Le=round(772/1600*4096)` = **1976 rows**. The canvas aspect is 1600x772 (about 2.07:1, not exactly 2:1). The base map projection list includes Natural Earth, Equirectangular, Mercator, Discworld and Globe. Natural Earth (`natural1`) is the default, since the History tab reprojects "to Natural Earth" (MAIN).
- **Export**: "Grayscale Export", tooltip "Export the raw elevation as a 16-bit greyscale PNG: full grid, no styling, opens in Unreal, Blender, Gaea or QGIS". The file is `<name>-heightmap-16bit.png`. The PNG has a `Description` text chunk: "16-bit greyscale heightmap. Black = <min> m, white = <max> m, sea level = sample <seaSample> of 65535." It also has a JSON `Merak` chunk `{v:1, kind:"heightmap", grid:[w,h], hscale, span:255, maxSample:65535, sea, seaSample, minMetres, maxMetres, projection}`. Above the base grid size the export uses "fine detail" upsampling ("Writing WxH 16-bit PNG"). The size is up to 16K per tier (16384 px) (MAIN; changelog 2026-10-26 "Grayscale export at your PNG size, up to 16K"). The export carries the doc's `projection` (terrainProj), so it is not necessarily equirectangular (MAIN).
- **Import**: "Import a heightmap or land-mask image as sculptable terrain"; "Import a file: GeoJSON, heightmap PNG or .warmap" (the .warmap is Merak's own document). The dialog "Import image → terrain" has two modes: "Heightmap / mask (auto)" and "Colour map (assign colours)", plus "Place on existing". Help text: "Grayscale = heightmap (black sea floor → white peaks, sea level ≈ 22% gray). Pure black & white = land mask (bright = land, dark = sea). Auto-detected." Also: "The image keeps its own proportions inside whatever box you draw: it is never stretched." (MAIN)
- Merak's own 16-bit PNGs round-trip exactly when depth = 16, kind = heightmap, width ≥ 4096 and the aspect matches (`wU`) (MAIN). "Exact measurements on heightmap import" arrived 23 Aug 2026 (MAIN, `rA`).
- "Trace land from an image": "Lift a landmass off any map picture, even a sketch with no heights in it." (MAIN)
- Earth data: bundled `earth_heights.bin` (Int16, 4096 x 1976). HD regions stream real topography of about 30 m ("HD relief: real ~30 m topography, fully sculptable") (MAIN).

### 1.3 Erosion, rivers, globe/3D, Planet Advisor
- Fluvial erosion is an option inside the tectonic run (above). The Lab reports an "Erosion" metric in mm/yr ("How fast the land wears down") (MAIN). I found no standalone hydraulic-erosion brush in the changelog (UNVERIFIED either way).
- Rivers: river width slider (21 Sep 2026); "More accurate small rivers" (28 Sep 2026); a Lab "Water" tab (1 Nov 2026). Applying a tectonic moment removes rivers (MAIN).
- Globe/3D: GlobeView, ThreeDView and SolarSystemView modules exist (asset list in MAIN). "Globe projection for blank worlds, editable while sculpting" (21 Sep 2026). 3D renders can be exported up to 16K on Premium (MAIN).
- Planet Advisor: "Analyze planet" leads to "Apply biomes" (auto biomes); HD regional maps open from Planet Advisor; there is an Advisor legend (MAIN, `rA`). The climate engine uses Köppen-style reasoning strings (CLW). The Geography Lab exposes planet parameters such as CO2, O2, temperature offset, day length and radius, with presets Earth, Ice age, Hothouse, Carboniferous, Slow spin and others (MAIN).

### 1.4 Scripting/CLI/automation
- No public API, CLI, plugin or scripting interface was found in the bundle or on the site. The only programmatic surface is a private cloud API (`/auth/*`, `/maps`, `/billing/*`) and a debug global `window.__geo` (projection helpers) (MAIN). Treat as **none (UNVERIFIED negative)**.

---------------------------------------------------------------------
## PART 2: GPlates for worldbuilding

Abbreviations for sources used repeatedly:
- SUPP = https://worldbuildingpasta.blogspot.com/2020/06/an-apple-pie-from-scratch-part-v.html ("An Apple Pie From Scratch, Part V Supplement: Tectonics: Using Gplates")
- VA = https://worldbuildingpasta.blogspot.com/2020/01/an-apple-pie-from-scratch-part-va.html ("Part Va: Tectonics: Construcing [sic] a Plate Tectonic History"). This is the main tectonics post; it lives on blogspot.
- VB = https://worldbuildingpasta.blogspot.com/2020/01/an-apple-pie-from-scratch-part-vb.html ("Part Vb: Tectonics: Alternatives to Plate Tectonics")
- VIIA = https://worldbuildingpasta.blogspot.com/2021/07/an-apple-pie-from-scratch-part-viia.html ("Part VIIa: Geology and Landforms: Tectonics and Volcanism"), the landform rules
- Discourse topics are cited by their full URL.

### 2.1 Step-by-step worldbuilder workflow in GPlates (Worldbuilding Pasta method) and file formats
1. **Set the timescale.** "on a scale of millions of years before the present (Ma); Gplates isn't built to handle timescales extending into the future. By default the scale only extends to 200 Ma"; the author used 1000 Ma and recommends "at least 2000 Ma" (SUPP). The preferences cap the max slider age at 9999 Ma, and the animation dialog allows 2 decimals (https://discourse.gplates.org/t/question-about-the-size-of-the-time-slider/3193). A developer (john.cannon) tested rotations at 3000 to 4000 Ma and they work, so there is no 2000 Ma limit (https://discourse.gplates.org/t/seeking-help-with-unmoving-plates-at-the-beginning-of-a-simulation/1264).
2. **Draw cratons** with Digitise New Polygon Geometry (G) at the start time. Feature type "Craton". Plate ID starts at 100 (never 0, which is reserved). Begin/End = Distant Past/Distant Future. Sizes "somewhere around 1-4000 km"; "around 8-12 cratons is probably ideal" for an Earthlike world (SUPP).
3. **Draw the supercontinent polygon** (ContinentalCrust) around the cratons, using one craton's plate ID. Check its area against 4πr² (510 million km² for Earth): 1/4 continental cover matches Earth about 1 Ga; "modern plate tectonics may be impossible once over 1/2 the planet's area is covered in continental crust" (SUPP). Polygons spanning more than half the globe confuse inside/outside tests (SUPP).
4. **Feature collections and the project.** Each feature collection is saved as a separate file. Use "Manage Feature Collections" > Save All, then "Save Project As" (SUPP). Use only Latin characters in names and paths (SUPP).
5. **Rotation file** (plain text `rotation.rot`, PLATES4 rotation format). Columns: `PlateID Time Lat Lon Angle ConjugatePlateID ! comment`, e.g. `100 2000.0 90.0 0.0 0.0 000 !`. "gplates will read this file from the present backwards, as opposed to our simulation process with proceeds from the past forwards". The 0.0 Ma row should be the identity (90, 0, 0). A conjugate of 000 means the plate moves independently; another plate ID means it follows that plate (SUPP). Load it via Manage Feature Collections > Open File (SUPP).
6. **Move the plates in timesteps.** The author uses 50 My steps, and 10 My steps for complex collisions. Use the Pole Manipulation toolset (5): Choose Feature (F), Move Pole (O), Modify Reconstruction Pole (P), then Apply. A pole near the plate centre gives rotation; a pole far away gives translation (SUPP).
7. **Check speeds** with Utilities > Kinematics Tool (Ctrl+Shift+K), Velocity magnitude in cm/yr (SUPP).
8. **"Drift correction".** Because the rotation file is read backwards, a plate drifts back toward its 0 Ma position after the last edited time. Copy the latest row to time 1.0 Ma for each moved plate (SUPP). A community Google Sheet automates this, generates the plate-ID lines and makes CPT colour maps (https://discourse.gplates.org/t/randomly-generate-n-plates-plus-a-helpful-google-sheet/937). The developer explains: "Your rotations at 1000Ma are zero... between 20Ma and 1000Ma the rotation will gradually shift... You need to duplicate the 20Ma rotations at 1000Ma" (https://discourse.gplates.org/t/coupling-continent/756).
9. **Rifts and splitting.** Draw a rift polyline, split features with copy geometry and new plate IDs, and edit the .rot file to change conjugates (SUPP).
10. **Flowlines** (feature type Flowline, multi-point, left/right plate IDs, times inserted every 10 My) show sea-floor spreading. "Adjacent flowlines generally shouldn't pass over each other... and they should never pass over existing sections of crust, except where subduction is occurring". Flowlines "drift" when rotations are overwritten, so you must recreate them often (SUPP). The forum shows many flowline bugs (https://discourse.gplates.org/t/ongoing-problem-with-flowlines-and-subducting-ocean-crusts/3286).
11. **Ocean crust** (OceanicCrust) polygons are traced from flowlines each timestep, named by formation age, e.g. "ocean 1950" (SUPP).
12. **Subduction zones and island arcs** go on the leading edges. A supercontinent can start ringed by subduction (SUPP).
13. **Rasters as land/water fills.** "Any map in an equirectangular projection-an even grid of latitude and longitude, which is twice as wide as it is tall-can be imported as a raster". The flat-colour raster is masked to continents via Layers > Inputs > "Reconstructed polygons" (SUPP).
14. **Collisions** are handled by hand. Create accreted terranes, redraw overlapping polygons "roughly halfway between the boundaries of the overlapping features" with new features beginning at the collision, end the old features, and tie the plate IDs with the parent as conjugate in .rot (SUPP). "we're not simulating the whole process of continuous deformation" (SUPP).
15. **Mark the results**: OrogenicBelt (Active → Former → Old collections), LargeIgneousProvince, HotSpot + MotionPath trails, MidOceanRidge (Half Stage Rotation), and ClosedPlateBoundary topologies (SUPP).
16. **Export.** Reconstruction > Export (Ctrl+Shift+E): "Export Single Snapshot Instant" or "Export Time Sequence of Snapshots". "Projected Geometries (and Rasters)" gives .svg and "Image (screenshot)" gives .png etc. Use the "Rectangular" projection to edit outside GPlates, centred via Set Projection > Central Meridian, camera at 0,0, zoom 100%; for video, 1 My steps with filename template "%n" (SUPP).

File formats (GPlates manual):
- Vector: GPML is the native format ("Click here to find out more about the GPlates Markup Language(GPML), the 'native' file format of GPlates", https://www.gplates.org/docs/). GPlates also loads and saves PLATES4 and Shapefiles: "you can load a Shapefile directly into GPlates" (https://www.gplates.org/docs/user-manual/Import/). The output format is chosen by file extension (https://www.gplates.org/docs/user-manual/LoadingAndSaving/). Shapefiles can be edited in QGIS (john.cannon, https://discourse.gplates.org/t/beginners-question/468).
- Raster import: RGB(A) formats "JPEG..., PNG, TIFF, GIF"; floating-point formats "NetCDF/GMT, GeoTIFF, ERMapper and Erdas Imagine" (.nc/.grd). A global raster is assumed to span -180..180 and -90..90 unless it is georeferenced. Time-dependent raster sets use filenames like `topography-0.jpg`, `topography-1.jpg` (time in Ma) (https://www.gplates.org/docs/user-manual/Import/).
- **Raster reconstruction**: "GPlates can also reconstruct rasters back in geological time with the assistance of a set of static polygons" (https://www.gplates.org/docs/user-manual/Import/). The Reconstructed Raster layer takes static polygons with plate IDs, an optional age grid and an optional "Surface Relief Raster... treated as a height-field" for shading (https://www.gplates.org/docs/user-manual/Layers/).
- Export (https://www.gplates.org/docs/user-manual/Export/): Reconstructed Geometries and Resolved Topologies as GMT, Shapefiles, OGR-GMT, GeoJSON; Projected Geometries as SVG; Image (screenshot) as bmp, jpg, png, ppm, tiff and others; Colour raster as 8-bit RGBA bmp, jpg, png, tiff, img; **Numerical raster as "nc, grd, tif, img: Export 32-bit floating-point numerical (non-coloured) raster data... (per time step)"**; Velocities as xy, gpml, CitcomS, Terra; Flowlines and Motion Paths as GMT, Shapefile, OGR-GMT, GeoJSON.
- Projections: only the central meridian can be changed, not the centre latitude; "Projections that have an arbitrary centre of projection like stereographic projections... aren't supported, and probably won't be" (john.cannon, https://discourse.gplates.org/t/beginners-question/468).

### 2.2 What GPlates does and does NOT do
Does:
- "desktop software for the interactive visualisation of plate tectonics... interactive plate tectonic reconstructions, geographic information system (GIS) functionality and raster data visualisation" (https://www.gplates.org/).
- "Plate tectonic reconstructions are the calculations of the probable positions, orientations and motions of tectonic plates through time, based upon the relative (plate-to-plate) positions of plates at various times in the past which may be inferred from other data" (https://www.gplates.org/docs/user-manual/Introduction_Gplates/). In other words it is kinematic: Euler rotations plus features, with no physics.
- Features page: topological plate polygons, deforming meshes, surface velocities, "Track crustal extension/contraction inside deforming regions", raster/vector reconstruction, cookie-cutting (https://www.gplates.org/features/). The deformation manual covers crustal thickness, stretching/thinning factors and tectonic subsidence (https://www.gplates.org/docs/user-manual/CrustalDeformation/; tectonic subsidence was added per https://www.gplates.org/news/).
Does NOT:
- No physics or forces. Moon/tides etc.: "Not directly, it'd be something you'd have to model yourself in the rotations." (john.cannon, https://discourse.gplates.org/t/non-earth-planets-and-accounting-for-satellites/930).
- No automatic collision handling, mountain building, erosion or topography generation. Every one of these is done by hand in the worldbuilding method: collisions are resolved by redrawing polygons, and orogenies, LIPs and hotspots are drawn as marker features afterwards (SUPP). "This is a problem with the method used in these worldbuilding scenarios because it treats the features like structurally rigid monoliths." (crackdtoothgrin, community user, https://discourse.gplates.org/t/how-do-divergent-boundaries-behave-when-theyre-almost-but-not-quite-transform/3272)
- Deformation exists but is limited for this use: "While GPlates does support deformation I suspect that it might not be fully useful for your scenario. It's more useful for calculating velocities and crustal thinning/thickening inside deforming regions... you can't really deform continent boundaries (polylines) unless they're tessellated into points." (john.cannon, https://discourse.gplates.org/t/beginners-question/468)
- Planet size: "the globe is represented internally as a unit radius sphere. Although there are probably places where the Earth's radius comes into play"; resizing the planet over time: "Not really" (john.cannon, same thread). SUPP notes the "Earth radius" setting affects the Measure tool.
- Future times are not supported in the UI (SUPP). A forum user says pyGPlates can use negative (future) times (https://discourse.gplates.org/t/adjusting-timescale-of-simulation-backwards/3278).
- Positioning: "GPlates prioritises the needs of the scientific community... we cannot always provide answers to those questions. So we have created this category for worldbuilding users to assist each other." (john.cannon, https://discourse.gplates.org/t/about-the-worldbuilding-category/764). On UI: "the U.I. is designed with a focus on presenting the data and not on creating it." (nickallanj, https://discourse.gplates.org/t/how-we-use-gplates/501)
- Known pain points: flowline drift, plates jumping when parent IDs change, ridges jumping when rotation angles pass 180° (https://discourse.gplates.org/t/mid-ocean-ridge-jumping/1265), and a cursor offset bug on Windows. A community fork, "GPlates 2.6.0-dev8-SR1: an unofficial fork for worldbuilding" (2026-08-07), adds Split Plate, Boolean Polygons, Retire Subducted Oceanic Crust, multi-vertex editing, a Rotation File Editor and drift-correction tools, built on Qt6. It is "not produced or endorsed by the GPlates team" and is a testing build (https://discourse.gplates.org/t/gplates-fork-multi-vertex-select-split-polygons-and-more/3275; download https://github.com/CaliTarheel/GPlates/releases/tag/2.6.0-dev8-SR1, not opened).

### 2.3 Forward vs backward from a fixed present-day map
- Worldbuilding Pasta's method is **forward** (past to present): start from a supercontinent and play the cycles (SUPP, VA). The author recommends running far back in time: VA's worked example spans 850 My (from "850 mya" to "0 mya") (VA).
- Asked about starting from an existing map and going backward, the author (comment by "Worldbuilding Pasta") replied: "**It's much harder**, the analogy I sometimes use is it's like looking at a pool table with balls randomly scattered around and then trying to reconstruct a game that would've resulted in that distribution. With reconstructing Earth's past, geologists have the benefit of knowing that it was the result of plate tectonic motion... whereas with a fictional world you have no such guarantee. I have seen a couple people do it, though, it's just tricky; the actual steps aren't going to be all that different, **rifting and collisions in gplates can sorta be treated as each other in reverse**, but you kinda have to be willing to **accept a wide margin of error**, and especially be **pretty abstract with your reconstruction of ocean plate motions**." (SUPP comments; the commenter name comes from the blog comment markup)
- Another reply: "You could maybe try to run the process backwards, but you'd have to take a pretty different approach which would probably take longer and kind of the main point of the process is to produce your continents and terrain so it'd be kind of redundant." (Worldbuilding Pasta, SUPP comments)
- GPlates' native model is itself **backward**. The rotation file is read from the present back, and the 0 Ma row is the identity, i.e. present-day geometry (SUPP). So drawing present-day continents at 0 Ma and adding rotations at older times is the "geologist" way, and it needs no drift correction. A forum user did exactly this ("i'm reconstructing plates from the modren day to past") (https://discourse.gplates.org/t/coupling-continent/756). Another user's "first draft was to start with the modern day landmass and work my way backwards through two super continent formations-resulting in 850my of simulation at 50my increments" (https://discourse.gplates.org/t/adjusting-timescale-of-simulation-backwards/3278). Another was "attempting to reverse-engineer the plate tectonics of a fictional continent" (https://discourse.gplates.org/t/cant-get-my-plates-to-move-correctly/902).
- Shifting a backward model so "today" lands at, say, 150 Ma has "no simple way". The advice is to back up the files and find-and-replace times in the text files, starting from the highest number (MrUks, community, https://discourse.gplates.org/t/adjusting-timescale-of-simulation-backwards/3278).
- Advice for working backwards, synthesised from the sources above:
  1. Put the fixed map at 0 Ma as features and as a raster (a land mask or heightmap in equirectangular projection). Cut it into plate polygons with plate IDs. The raster can then be reconstructed back in time via static polygons (https://www.gplates.org/docs/user-manual/Import/, https://www.gplates.org/docs/user-manual/Layers/).
  2. Read the present boundaries first. Mountain belts suggest past collisions or subduction; ages from VA's decay rule give the timing. Passive margins and parallel coastlines suggest rifts, so they should fit together when closed. Island chains suggest hotspot tracks, which give plate direction (VA, VIIA).
  3. Reverse the processes: a rift seen going back becomes a closing collision; a collision suture going back becomes a rift (WBP comment above).
  4. Keep ocean motion abstract and accept errors (WBP comment). Ocean crust is replaced on about 250 My scales (VA), so oceans older than about 200 My leave no record anyway (VA: "without much data on ocean plate motion older than around 200 million [years]").
  5. Rate-check with the Kinematics tool against the speed table (SUPP).

### 2.4 How Worldbuilding Pasta derives landforms from tectonic history: rules of thumb
Plate motion:
- Speed table in VA: subducting ocean **10-20** cm/yr; recent subduction collision **5-10**; active margin continent **2-5**; passive margin continent **<1** (VA). SUPP gives a slightly different table: 8-20 / 6 / 3 / <1 (SUPP). Note the discrepancy.
- Earth references: India up to 20 cm/yr in the late Cretaceous and about 6 now; Nazca 10; Pacific about 8; the Americas 3; North America 1 cm/yr for the first 25 My of rifting, then 3.5; Eurasia 1.5; Africa and Antarctica <1 (VA).
- "1 cm/yr is about 0.9° of rotation around the Earth every 10 million years"; an active-margin continent moving 100 My covers about 20-50° of longitude; for other planets, divide by the radius in Earth radii (VA).
- Author's own check of the worked example: "around 1-5 cm/year on average for major continents and 2-10 cm/year for ocean-only plates" (WBP reply, VA comments).
- Continental crust growth: 0.6-0.9 km³/yr, about 17-26 thousand km²/My, 9-15% per billion years, against about 200 million km² of continental crust today (VA).
- Cycles: ocean crust is completely replaced every ~250 My; the supercontinent cycle is ~750 My, possibly accelerated to 400-500 My (VA summary). Crust is 5 km thick at young ocean and 70 km at old continent, 35 km on average (VA).
Topography from history:
- **Mountain height decay**: "average mountain height tends to begin around **2500 meters and drop about 5 m every million years**, with peak height starting around **4000 m and dropping 8 m/myr**", and "an exponential decay might be a better model" (VA). These are average elevations; peaks and valleys are added later (VA).
- Orogeny marking: Andes-type polygons "100 km from the coasts and 100 km wide is a good standard". A collisional orogeny stays active for about 50 My after the collision ends and then becomes "former" and erodes. After 450 My it is "old": eroded flat, but its roots can be exhumed by later uplift. LIPs exist for 10 My, and LIPs older than 450 Ma matter little. Hotspots last "1-200 My" (SUPP).
- Four orogeny types: Andes-type (thin, subduction coast), Laramide-type (broad, fast subduction or ridge subduction), Ural-type (thin, simple collision), Himalayan-type (broad high plateaus, complex or energetic collision). Thicker orogenies go on leading edges of faster continents (SUPP; VIIA). VIIA gives the typical profiles of the four range types **as diagrams only**; the numbers are in images and were not extractable (UNVERIFIED).
- VIIA numeric dimensions from text:
  - Fold-and-thrust belts: ridges 5-50 km apart, hundreds of km long, 10-20 ridges across, ridges over 2000 m, standing 1000 m above valleys.
  - Basin and range: ridges shorter, under 100 km.
  - Trailing-edge island arcs: islands 100-200 km wide, hundreds to thousands of km long, highlands up to 3 km.
  - Young island arc (first ~50 My): islands 100-300 km from the trench, spaced 20-100 km, about 10-20 km across, volcanoes 0.5-1 km (up to 2+ km).
  - Intermediate arc (~100 My): islands up to 1,000 km long, peaks 2-3 km.
  - Mature arc (several hundred My): islands over 1,000 km long, a couple hundred km wide; Sumatra's ridge is about 50 km wide and over 3 km high.
  - Hotspot islands (Hawaii): peaks 1-4 km, islands 50-150 km across, about 100 km apart, prominent chain about 600 km, seamounts another 5,000 km.
  - Faults: up to 1,000+ km long, offsets up to hundreds of km, valleys under 10 km wide.
  - East African Rift: over 3,000 km.
  - Uplift: Laramide orogenies uplift the interior (Rockies to Mississippi gradient, about 1 km); plume uplift over 1 km (eastern/southern Africa); post-glacial rebound of several hundred m.
  (all VIIA)
- Crust boundaries are not coastlines: "the boundaries shown aren't actually coastlines, but boundaries between continental and oceanic crust (roughly)"; margins are submerged shelves (VA).
- Effort: the worked example took "a solid week of long afternoons" (VA).
- Alternatives to plate tectonics (stagnant lid, heat pipe, etc.) are covered in VB.

### 2.5 Versions, dates, licenses
- **GPlates desktop: latest stable is 2.5, released 15 April 2024** ("The current stable release of GPlates is GPlates 2.5, released in April 2024", https://www.gplates.org/download/; date from the news URL https://www.gplates.org/news/2024-04-15-GPlates-2-5-released/). 2.5 added subduction zone teeth (same news page). Previous: 2.4 on 2023-12-08 (https://www.gplates.org/news/ link list).
- **GPlates 3.0 is NOT released** as of 2026-11-11. There is no 3.0 on the download or news pages (https://www.gplates.org/download/, https://www.gplates.org/news/). A `gplates-3.0-dev` branch "includes the replacement of OpenGL with Vulkan (in progress)... will eventually be merged back into gplates and turned into the GPlates 3.0 release" (mirror README, https://www.gitlink.org.cn/NSCCN/GPlates). A development line "2.6.0-dev8" exists, since the community fork is based on it (https://discourse.gplates.org/t/gplates-fork-multi-vertex-select-split-polygons-and-more/3275). A search snippet claiming an EarthByte item targeted 3.0 for "late 2024" could not be fetched (UNVERIFIED).
- Platforms: Windows (.exe installer or .zip), macOS Intel (10.15+) and Apple Silicon (11+) .dmg, Ubuntu .deb, plus source (https://www.gplates.org/download/).
- **pyGPlates: latest 1.0.0**. The release candidate 1.0.0rc1 was announced 2024-12-13 and the official 1.0.0 was announced 2025-03-27 (https://discourse.gplates.org/t/pygplates-1-0-0-released/1020). PyPI upload date 2025-03-26; Python >=3.8; classifiers GPLv2, Windows/macOS/Linux (https://pypi.org/pypi/pygplates/json). Installed with conda or pip (https://www.gplates.org/download/). Docs: "PyGPlates 1.0 documentation" (https://www.gplates.org/docs/pygplates/).
- **GPlately: latest 2.0.0**: PyPI upload 2025-07-14 (https://pypi.org/pypi/gplately/json); forum announcement 2025-07-17 (https://discourse.gplates.org/c/announcements/8.json). It adds a CLI, the Plate Model Manager, a Docker image and early PyGMT (https://www.gplates.org/news/). License GPLv2, Python >=3.9 (PyPI JSON).
- License: "GPlates and pyGPlates are both free software... licensed for distribution under the GNU General Public License (GPL), version 2." (https://www.gplates.org/). Wikipedia says "GNU GPL version 2+" (https://en.wikipedia.org/wiki/GPlates). The official site says v2.
- Other: GPlates Web Service v1.0.0 (2024-12-23); the core source moved to GitHub in 2023 (https://discourse.gplates.org/c/announcements/8.json). GitHub pages could not be read from this environment (proxy 403).

---------------------------------------------------------------------
## Key takeaways for a tool that keeps a fixed coastline and invents a tectonic history
1. **Neither tool does exactly this today.** Merak's History tab (since 1 Nov 2026) comes closest. It keeps the user's present map as t = 0, infers plates and Euler motions from the land, and rewinds 250 My (plus 50 My ahead) as a viewable or GIF history, with no apply step. Its forward Tectonics mode (8 Nov 2026) changes the coastline. GPlates' rotation model is natively present-anchored (0 Ma = identity), which suits "fixed present map, invented past". But everything apart from the rigid rotations is manual there.
2. **Work in the backward direction the way GPlates stores it.** Fix the present geometry, assign plate IDs, and store finite rotations at older times. Then no drift correction is needed. Forward-authored histories need a "1.0 Ma copy" hack (SUPP).
3. **Use present-day landforms as constraints.** Pick the age of each mountain belt from its mean height with VA's decay rule: mean height h ≈ 2500 − 5·age (m, age in My) and peak ≈ 4000 − 8·age, so a 1500 m mean belt is about 200 My old. Then place a past collision or subduction at that age. Treat parallel passive margins as rift conjugates that must fit back together, and hotspot chains as plate-direction and speed indicators (island spacing about 100 km, chain length about 600 km active).
4. **Speed and plausibility checks**: active-margin continents 2-5 cm/yr, passive <1, oceanic plates 8-20; 1 cm/yr ≈ 0.9°/10 My on Earth, scaled by 1/R (VA, SUPP). Merak caps user speeds at 15 cm/yr ("Earth: 1 to 10").
5. **Accept non-uniqueness.** The WBP author: going backwards is "much harder... accept a wide margin of error... be pretty abstract with your reconstruction of ocean plate motions". Ocean floor older than about 200-250 My is gone anyway (VA). A tool can therefore invent ocean history fairly freely. The continental record (orogens, sutures, LIPs, cratons) carries the constraints.
6. **Interop formats worth supporting**: equirectangular 2:1 rasters (GPlates' assumption for global rasters), 16-bit grayscale PNG heightmaps (Merak export, with sea-level metadata in PNG text chunks), GeoTIFF/NetCDF 32-bit float (GPlates numerical raster import and export), GPML, Shapefile, GeoJSON features, and PLATES4 `.rot` rotation files. Writing a `.rot` plus plate polygons would let users inspect an invented history in GPlates or pyGPlates, and reconstruct their present heightmap back in time via static polygons.
7. **The gaps both tools leave**: physically coupled collisions with deformation, automatic orogeny placement from the history, and erosion-driven topography over time. GPlates leaves all three to the user. Merak has uplift, rifting, plume and fluvial-erosion toggles, but only in its forward mode.

---------------------------------------------------------------------
## URLs read
Merak:
- https://merakmapmaker.com (HTML shell)
- https://merakmapmaker.com/sitemap.xml
- https://merakmapmaker.com/robots.txt
- https://merakmapmaker.com/llms.txt (returns the SPA shell)
- https://merakmapmaker.com/assets/index-3D_Y8mU_.js (MAIN: changelog, pricing, UI strings)
- https://merakmapmaker.com/assets/climateLab.worker-CGVWvzw9.js (CLW)
- https://merakmapmaker.com/assets/heavy.worker-KMgXc4G2.js, https://merakmapmaker.com/assets/worldGen.worker-DWIm3jEB.js, https://merakmapmaker.com/assets/advisor.worker-CInabQC3.js (downloaded, only briefly grepped)
- Web searches "Merak Map Maker" and "merakmapmaker tectonic plates worldbuilding map maker": no relevant results
Worldbuilding Pasta:
- https://worldbuildingpasta.blogspot.com/2020/06/an-apple-pie-from-scratch-part-v.html (incl. comments)
- https://worldbuildingpasta.blogspot.com/2020/01/an-apple-pie-from-scratch-part-va.html (incl. comments)
- https://worldbuildingpasta.blogspot.com/2020/01/an-apple-pie-from-scratch-part-vb.html
- https://worldbuildingpasta.blogspot.com/2021/07/an-apple-pie-from-scratch-part-viia.html
GPlates discourse:
- https://discourse.gplates.org/categories.json
- https://discourse.gplates.org/c/worldbuilding/15.json (pages 0-1)
- https://discourse.gplates.org/c/announcements/8.json
- https://discourse.gplates.org/search.json (several queries)
- Topics: /t/126, /t/764, /t/3278, /t/977, /t/930, /t/3275, /t/3195, /t/1004, /t/937, /t/3193, /t/1264, /t/1265, /t/501, /t/902, /t/756, /t/468, /t/3286, /t/3272, /t/1020 (all under https://discourse.gplates.org/t/<id>)
GPlates official and other:
- https://www.gplates.org/
- https://www.gplates.org/download/
- https://www.gplates.org/news/
- https://www.gplates.org/news/2024-04-15-GPlates-2-5-released/
- https://www.gplates.org/features/
- https://www.gplates.org/docs/
- https://www.gplates.org/docs/pygplates/
- https://www.gplates.org/docs/user-manual/
- https://www.gplates.org/docs/user-manual/Introduction_Gplates/
- https://www.gplates.org/docs/user-manual/Import/
- https://www.gplates.org/docs/user-manual/LoadingAndSaving/
- https://www.gplates.org/docs/user-manual/Export/
- https://www.gplates.org/docs/user-manual/Layers/
- https://www.gplates.org/docs/user-manual/Reconstructions/ (fetched, not used)
- https://pypi.org/pypi/pygplates/json
- https://pypi.org/pypi/gplately/json
- https://en.wikipedia.org/wiki/GPlates
- https://www.gitlink.org.cn/NSCCN/GPlates
- Failed or blocked: github.com release pages (proxy 403), https://www.earthbyte.org/?p=8553 (little text), www.gplates.org/docs/pygplates/installation.html (404)
