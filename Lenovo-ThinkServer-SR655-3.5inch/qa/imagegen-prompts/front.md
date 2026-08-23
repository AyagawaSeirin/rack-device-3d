# Front imagegen record

method: built-in `image_gen`, exactly one call for this face

production_mode: SOURCE_LOCKED_GENERATION

input_roles:

- Image 1: PRIMARY BINDING REAL PHOTOGRAPH — `source/third-party/ebay-206238343567-1.jpg`; exact original-generation SR655 12xLFF units; binding for real black plastic, grille, wear, color balance, highlight softness and photographic character. Ignore stacked neighboring units, plastic wrap and seller environment.
- Image 2: BINDING EXACT ORTHOGRAPHIC GEOMETRY — `qa/reference/official-viewer-front-crop.png`; official SR655 public viewer, 12 carriers, exact latch/I/O/logo placement.
- Image 3: REQUESTED CONFIGURATION LOCK — `qa/reference/user-screenshot-row4-upscaled.png`; fourth row front target.
- Image 4: TECHNICAL LAYOUT — `source/originals/lenovo-docs-front-12x3.5.png`; official bay numbering and component boundaries.

final_prompt:

Use case: product-mockup

Asset type: exact front orthographic rack-device texture for a website GLB

Primary request: generate one new perfectly straight-on front face of the original-generation Lenovo ThinkSystem SR655 (types 7Y00/7Z01), B5VK/AUR9 12x3.5-inch SAS/SATA chassis, matching the requested screenshot row.

Scene/backdrop: perfectly flat solid #ff00ff chroma-key background for local transparency extraction; absolutely uniform, no gradient, floor, shadow, reflection or texture; do not use #ff00ff in the device.

Style/medium: SOURCE-LOCKED real product photography. Image 1 is binding for genuine black molded plastic, honeycomb grille texture, slight real wear, color balance, contrast, highlight softness, recessed shadows and edge character. Do not turn it into clean CGI, game art, vector art or an illustrated product render.

Composition/framing: one complete 2U face only, no adjacent top or side, no perspective; both front rack latches fully visible; physical content ratio 482.0:86.5; generous chroma margin; at least 2400 px long-edge intent.

Verified invariants: exactly 12 LFF carrier fronts in 3 rows x 4 columns; identical carrier sizes and real vertical/red accents; left latch has VGA and vertical ThinkSystem factory logo; right latch has correct power/status controls, two stacked blue USB-A ports, pull-out information tab and SR655 model badge; no security bezel; preserve factory Lenovo/ThinkSystem/SR655 marks in correct location and readable orientation.

Opacity intent: all visible chassis pixels fully opaque, including black grilles and ports. Only true rack-latch through-holes may later become transparent; the external canvas is chroma key.

Avoid: changed bay count; 2.5-inch bays; V3 family substitution; fake screens or LEDs; invented ports; pseudo-text; mirrored logo; seller tape; plastic wrap; stacked servers; floor; cables; rails; detached fragments; watermark; relighting; beautification; smoothing; aggressive denoising; artificial symmetry; color restyling.

selected_output: `views/front.png`

chroma_source: `qa/imagegen-output/front-chroma.png`

output_record: one built-in imagegen call; magenta removed with the installed imagegen chroma helper; measured rectification to 2600x467; unverified serial/QR-like microprint below the authentic SR655 badge blurred while the SR655 badge remained.
