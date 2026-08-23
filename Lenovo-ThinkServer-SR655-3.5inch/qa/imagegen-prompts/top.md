# Top imagegen record

method: built-in `image_gen`, exactly one call for this face

production_mode: SOURCE_LOCKED_GENERATION

input_roles:

- Image 1: PRIMARY BINDING REAL TOP PHOTOGRAPH — `source/third-party/ebay-206238343567-3.jpg`; exact closed top cover, factory service-label block, latch, vent, stamped panels, material/color/texture and photographic character.
- Image 2: BINDING EXACT ORTHOGRAPHIC GEOMETRY — `qa/reference/official-viewer-top-rectified.png`.
- Image 3: FRONT-EDGE/SILHOUETTE SUPPORT — `qa/reference/official-viewer-front-right-crop.png`.
- Image 4: REAR-EDGE/SILHOUETTE SUPPORT — `qa/reference/official-viewer-rear-right-crop.png`.

final_prompt:

Use case: product-mockup

Asset type: exact top orthographic rack-device texture for a website GLB

Primary request: generate one new perfectly top-down closed-cover view of the original-generation Lenovo ThinkSystem SR655 12x3.5 PCIe-rich appliance.

Scene/backdrop: perfectly flat solid #ff00ff chroma-key background, uniform and shadowless, no floor/reflection/gradient; do not use #ff00ff in the device.

Style/medium: SOURCE-LOCKED real product photography from Image 1. Preserve real galvanized-metal grain, subtle scuffs, gray/silver color balance, soft broad highlights and factory printing character. Do not clean, relight, beautify or smooth into CGI.

Composition/framing: complete top only, exactly perpendicular with no side/front/rear face visible; body width:depth ratio 444.6:764.7; portrait with front edge at image top and rear edge at image bottom; at least 1800 px long-edge intent.

Verified invariants: one closed top cover; large shallow central rectangular stamping; longitudinal/cross seams; black release latch with blue tab near the rear/right zone; one wide rear ventilation field; exact small screw/hole groups; preserve the large factory service-instruction label block from Image 1 at its real size and position, but do not invent serial numbers, QR content or new readable microtext. Authentic Lenovo/ThinkSystem marks may remain only where proven.

Opacity intent: metal and dark vent pixels fully opaque; external canvas only is chroma key.

Avoid: exposed internals; missing top cover; mirrored vent/latch; copied bottom; invented feet/rails; pseudo-words; fake serial/QR; seller background; fabric; plastic bag; shadow; floor; reflection; vector/toon/CGI restyle.

selected_output: `views/top.png`

chroma_source: `qa/imagegen-output/top-chroma.png`

output_record: one built-in imagegen call; magenta removed with the installed imagegen chroma helper; measured rectification to 1512x2600; factory service-label layout preserved while generated serial/QR-like microcontent was deliberately blurred/deidentified; latch, vent, stampings and real metal grain retained.
