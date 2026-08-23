# Right-side imagegen record

method: built-in `image_gen`, exactly one call for this face

production_mode: MULTI_REFERENCE_RECONSTRUCTION

input_roles:

- Image 1: PRIMARY REAL MATERIAL/STYLE SOURCE — `source/third-party/ebay-206238343567-3.jpg`; exact SR655 sheet-metal grain, cover color, factory wear and highlight softness.
- Image 2: BINDING EXACT RIGHT-SIDE GEOMETRY — `qa/reference/official-viewer-right-crop.png`; official viewer, front edge at image left.
- Image 3: BINDING THREE-QUARTER GEOMETRY — `qa/reference/official-viewer-front-right-crop.png`.
- Image 4: REAR/EDGE MATERIAL SUPPORT — `source/third-party/ebay-206238343567-4.jpg`.

final_prompt:

Use case: product-mockup

Asset type: exact right-side orthographic rack-device texture for a website GLB

Primary request: generate one new perfectly orthographic physical right side of the original-generation Lenovo ThinkSystem SR655 12x3.5 PCIe-rich appliance.

Scene/backdrop: perfectly flat solid #ff00ff chroma-key background, uniform and shadowless, no floor/reflection/gradient; do not use #ff00ff in the device.

Style/medium: same real galvanized sheet-metal photographic character as Image 1: visible fine grain, subtle handling marks, neutral gray/silver color, soft highlights and real fastener recess shadows. No cleaner CGI style.

Composition/framing: complete side only, no top/front/rear face visible, front edge at image left and rear edge at image right, physical ratio 764.7:86.5, generous margin, at least 2000 px long-edge intent.

Verified invariants: black front latch/ear silhouette only at left edge; longitudinal upper rail lip; two main sheet-metal panel regions and center seam; exact four raised circular bosses; exact screws/holes; small yellow/black weight warning label in front third; tiny rear lower flange projection; no invented side vent, rail, feet or logo.

Opacity intent: entire side fully opaque; external canvas only is chroma key.

Avoid: copying the left side; mirroring; wrong front/rear order; generic blank panel; extra labels; rails; feet; vents; handles; pseudo-text; floor; shadow; reflection; CGI cleanup; smoothing; exaggerated embossing.

selected_output: `views/right.png`

chroma_source: `qa/imagegen-output/right-chroma.png`

output_record: one built-in imagegen call; magenta removed with the installed imagegen chroma helper; measured rectification to 3000x339; right-only yellow warning label and exact boss/screw asymmetry retained.
