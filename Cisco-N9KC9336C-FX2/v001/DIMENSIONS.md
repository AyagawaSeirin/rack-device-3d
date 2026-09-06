# Dimensions and coordinate contract

Unit: 1 Blender unit = 1 metre. Parameters are millimetres until divided by 1000 exactly once.
Origin is the main chassis bottom centre excluding removable ears and handles. Chassis bottom Z=0, port face -Y, service face +Y, front-view right +X.

| Measure | Official imperial | Official metric rounded | Exact imperial conversion adopted | Coverage |
|---|---|---|---|---|
| Chassis width | 17.3 in | 43.9 cm | 439.42 mm | Body, excludes projecting rack flanges |
| Depth with handles | 24.5 in | 62.3 cm | 622.30 mm | Port-end body face through rear handle extreme; never add handles again |
| Height | 1.72 in | 4.4 cm | 43.688 mm | Main 1RU chassis |
| Clearance width with two brackets | 19.0 in | 48.3 cm | 482.60 mm | Installation clearance envelope; not a measured manufactured ear extremity |

Official guide: [system specifications](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n9336cfx2_hig/guide/b_n9336cFX2_nxos_hardware_installation_guide/b_n9336cFX2_nxos_hardware_installation_guide_appendix_0111.html), local `sources/official/hardware-guide.pdf`, physical page 55 / printed 49. Downloaded revision last modified 2026-07-16. Clearance width: physical page 19 / printed 13. The [series datasheet](https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742282.pdf), local `sources/official/datasheet.pdf`, physical/printed page 10, confirms the FX2 column separately from FX2-E.

The 0.42/0.70/0.312 mm differences between unit representations are publication rounding differences, not measured manufacturing error. Reference comparison tolerance: ±1.27 mm for the one-decimal-inch width/depth and ±0.5 mm for height. Geometric numeric tests will separately use 0.01 mm tolerance against the chosen parameters; that is not a physical accuracy claim.

Estimated working parameters from photographs, not official manufacturing dimensions:

| Parameter | Adopted mm | Uncertainty / basis |
|---|---:|---|
| Bare shell depth | 590.0 | ±8; allocation of the official total to body and photographed handle projection |
| Rear maximum handle projection | 32.3 | complementary to 622.3 total, not an independent official measure |
| Ear overall span | 482.6 | ±2; installation clearance and photographed flange proportion |
| Ear plate thickness | 1.8 | ±0.5; NWR close photograph shows folded solid metal |
| Shell sheet thickness | 1.0 | ±0.4; conservative sheet-metal working estimate |
| Port cage centre pitch | 22.5 | ±0.5; 18 equal columns across reference front face |
| Cage outer width | 20.8 | ±0.7; photographed proportion |
| Ear obround width / height | 9.8 / 6.5 | ±1; scaled to chassis height in NWR macro; 3 vertical slots |

View conventions: front screen-right +X; rear screen-right -X; top screen-right +X/up +Y; bottom screen-right -X/up +Y. Side views are independent observations, never horizontally flipped photographs. Ear installation plane is the port-end plane in the selected assembly. External slider rails and rack posts are excluded.

Final cage outside height estimate:26.52mm (H/W1.275), revised from31.2mm after NWR macro comparison. Generic connector literature is contextual and does not identify the Cisco OEM cage. Overall body height43.688mm; a0.025mm photographic label plane adds that amount to the assembly envelope.

Side projection convention verified with camera basis: viewing physical LEFT from-X with world+Z up puts port end-Y at image RIGHT; viewing RIGHT from+X puts ports at image LEFT. The two independent imagegen side candidates were correctly reclassified without mirroring; original prompts/names are retained as history.

Final geometric measurement (qa/original-delivery-scene.json): core shell439.420015×589.999974×43.687999mm; complete body with handles but without ears439.420015×622.299999×43.713000mm; with ears482.600003×622.299999×43.713000mm. The last height includes the measured0.025mm photographic ink/label plane. Depth starts at the LS control extremeY=-295.519978mm and ends at the PSU handleY=326.780021mm. Relative to the590mm shell,0.520mm is forward control projection and31.780mm rear handle projection; the preliminary32.3mm allocation is not added to those again.

glTF exports the standard Y-up convention (Blender XYZ→glTF X,Z,−Y). Importing through the glTF importer restores the documented Blender axes; the independent reimport test verified identical world bounds and text reading axes, without a second millimetre conversion.
