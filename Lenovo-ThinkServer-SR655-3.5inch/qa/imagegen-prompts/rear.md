# Rear imagegen record

method: built-in `image_gen`, exactly one call for this face

production_mode: MULTI_REFERENCE_RECONSTRUCTION

input_roles:

- Image 1: PRIMARY EXACT-CONFIGURATION OFFICIAL COLOR SOURCE — `qa/reference/lp1161-p005-rear-8pcie-crop.png`; binding for 8-slot/no-rear-drive layout, two-port OCP, lower I/O order and two 750W AC PSUs.
- Image 2: BINDING EXACT ORTHOGRAPHIC GEOMETRY — `qa/reference/official-viewer-rear-8pcie-crop.png`; official public viewer switched to 12x3.5 PCIe-rich rear.
- Image 3: REQUESTED CONFIGURATION LOCK — `qa/reference/user-screenshot-row4-upscaled.png`; fourth row rear target.
- Image 4: REAL MATERIAL/PHOTOGRAPHIC STYLE SUPPORT — `source/third-party/ebay-206238343567-4.jpg`; exact-model real rear metal, vents, connectors and wear. It has only one 1100W PSU, so it must not control PSU count, wattage, blank bay or geometry.

final_prompt:

Use case: product-mockup

Asset type: exact rear orthographic rack-device texture for a website GLB

Primary request: reconstruct one new perfectly straight-on rear face of the original-generation Lenovo ThinkSystem SR655 12x3.5 PCIe-rich configuration shown in Images 1-3.

Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for local transparency extraction; absolutely uniform, no gradient, floor, shadow, reflection or texture; do not use #ff00ff in the device.

Style/medium: real product photography. Use Image 4 only for genuine galvanized metal, port, grille, screw, wear, color balance and recess-shadow character, while Images 1-3 are binding for exact factual configuration. No CGI cleanup or style redesign.

Composition/framing: one complete rear face only, perfectly orthographic, no top or side, no false rear ears, physical content ratio 482.0:86.5, at least 2400 px long-edge intent.

Verified invariants from rear left to right: three PCIe banks containing slots 1-3, 4-6 and 7-8 (8 total), all with factory perforated blanking covers; no rear drives; two-port OCP 3.0 adapter at lower left; error LED; BMC RJ45; locator LED; blue VGA; two stacked blue USB-A; DB9 serial; NMI; exactly two identical installed 750W AC hot-swap PSUs, each with readable “750W AC” circular face, C14 inlet, status LEDs and orange release handle. Preserve real slot dividers, latch handles, honeycomb perforations, screw pattern and depth.

Opacity intent: every visible rear surface fully opaque, including dark grilles/ports; external canvas is chroma key; no unsupported transparent holes.

Avoid: one-PSU seller configuration; 1100W label; DC connector; rear drive bays; 6-slot or 2-slot rear; copied front ears; invented OCP ports; fake adapters; pseudo-text; mirrored order; cables; seller labels; floor; watermark; vectorization; toon shading; smoothing; relighting; beautification.

selected_output: `views/rear.png`

chroma_source: `qa/imagegen-output/rear-chroma.png`

output_record: one built-in imagegen call; magenta removed with the installed imagegen chroma helper; measured rectification to 2400x467; exact 3+3+2 PCIe slots, two OCP ports and two 750W AC/C14 PSUs retained.
