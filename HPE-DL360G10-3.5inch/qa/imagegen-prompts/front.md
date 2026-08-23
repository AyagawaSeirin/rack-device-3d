# front.png

Production mode: `MULTI_REFERENCE_RECONSTRUCTION`

Input roles:

1. `source/originals/user-config-lock-screenshot.png`: PRIMARY BINDING USER CONFIGURATION LOCK, row 4 front; exact physical variant and straight orientation.
2. `source/pdf-pages/quickspecs-p04.png`: PRIMARY OFFICIAL 4LFF product-appearance and geometry reference; highest authority for four-carrier structure, top control band, ears, materials and HPE photographic character.
3. `source/third-party/etb-tech-4lff-angle.jpg`: BINDING EXACT 4LFF REAL PHOTOGRAPH for real galvanized metal/plastic texture, wear, right ear and carrier depth.
4. `source/originals/hpe-user-guide-front-4lff.png`: OFFICIAL TECHNICAL DIAGRAM for component count/order.
5. `source/third-party/mydraw-dl360-gen10-4lff-front.png`: SUPPORTING ORTHOGRAPHIC ORIENTATION ONLY; too small for materials or small details.

Final prompt:

Use case: product-mockup
Asset type: exact website GLB front-face source for a rack server
Primary request: Generate one new perfectly straight orthographic FRONT view of the exact Hewlett Packard Enterprise HPE ProLiant DL360 Gen10 1U 4LFF / 3.5-inch configuration frozen in the references. This is the early embedded-LOM generation and must not become Gen9, Gen10 Plus, Gen11, SFF or NVMe.
Scene/backdrop: perfectly flat, uniform solid #FFFF00 chroma-key canvas for later border-connected transparency removal; no gradient, texture, floor, contact shadow, cast shadow or reflection; keep the entire device separated from the canvas and do not use #FFFF00 on the device.
Style/medium: same real HPE product-photography character as Images 2 and 3, preserving brushed/galvanized metal grain, black molded plastic, small real wear, source color balance, modest contrast, highlight softness, recess shadows and imperfect real material. Do not convert it to clean CGI, game art, vector art, illustration or a beautified product render.
Composition/framing: one complete front only, centered, no visible top, bottom or side and no perspective; physical front-ear span to height ratio 482.6:42.9; very wide product across a larger canvas with safe padding, never squeezed.
Verified structure: two separate front ears/endcaps; left Drive Bay ID endcap; right black endcap with the genuine green HPE mark and readable factory text “ProLiant DL360 Gen10”; four independent 3.5-inch LFF Smart Carrier fronts in one row, numbered physically 1-4 left-to-right, each with its own recessed carrier body, pull handle, round green release/status detail and small magenta latch detail; continuous upper black ventilation/control band; ODD position blank; serial pull tab; display-port/USB2 option blank; standard Systems Insight Display/control group; front iLO Service and USB3 areas in their actual HPE positions; correct UID/power/health/NIC indicators. Keep four carriers present but do not invent readable capacity/serial/QR text where the source is unreadable.
Constraints: HPE/ProLiant factory marks must be integrated into the real ear material, correctly oriented and not mirrored. Each carrier/handle, ear, blank and port must remain mechanically distinct. Product pixels fully opaque. No bezel. No detached fragment, cable, rail, callout, arrow, number bubble, watermark or seller sticker.
Avoid: 8SFF/10SFF bays, Gen9/Gen10 Plus/Gen11 ears, extra drives, missing carriers, repeated AI patterns, fake screens, pseudo-text, invented LED colors, generic grille, artificial symmetry, smoothed materials, recoloring, relighting, denoising, mirrored logo or a beveled-box look.

Method: built-in `image_gen`; first yellow-chroma output was retained as `qa/staging/front-chroma-v1.png` but rejected because the background was nonuniform. One targeted background-only edit produced `qa/staging/front-chroma-v2.png` on cyan. Final alpha uses border-connected local flood removal at 20% color distance, one-pixel edge contraction, tight crop and ratio-preserving resize; no device feature was regenerated after the targeted edit.
