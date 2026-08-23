# Left-side imagegen record

method: built-in `image_gen`, exactly one call for this face

production_mode: MULTI_REFERENCE_RECONSTRUCTION

input_roles:

- Image 1: PRIMARY REAL MATERIAL/STYLE SOURCE — `source/third-party/ebay-206238343567-3.jpg`; exact SR655 sheet-metal grain, cover color, factory wear and highlight softness.
- Image 2: BINDING EXACT LEFT-SIDE GEOMETRY — `qa/reference/official-viewer-left-crop.png`; official viewer, front edge at image right.
- Image 3: BINDING THREE-QUARTER GEOMETRY — `qa/reference/official-viewer-rear-right-crop.png`, used only to confirm the opposite-edge/rear relationship.
- Image 4: REAR/EDGE MATERIAL SUPPORT — `source/third-party/ebay-206238343567-4.jpg`.

final_prompt:

Use case: product-mockup

Asset type: exact left-side orthographic rack-device texture for a website GLB

Primary request: generate one new perfectly orthographic physical left side of the original-generation Lenovo ThinkSystem SR655 12x3.5 PCIe-rich appliance.

Scene/backdrop: perfectly flat solid #ff00ff chroma-key background, uniform and shadowless, no floor/reflection/gradient; do not use #ff00ff in the device.

Style/medium: same real galvanized sheet-metal photographic character as Image 1: fine grain, subtle handling marks, neutral gray/silver, soft highlights and real fastener recess shadows. No cleaner CGI style.

Composition/framing: complete side only, no top/front/rear face visible, rear edge at image left and black front latch/ear at image right, physical ratio 764.7:86.5, generous margin, at least 2000 px long-edge intent.

Verified invariants: longitudinal upper rail lip; two main sheet-metal regions and center seam; four raised circular bosses; asymmetric exact screw/hole pattern; two small rectangular slots near the rear/lower area; no yellow weight label on this face; no invented side vent, rail, feet or logo.

Opacity intent: entire side fully opaque; external canvas only is chroma key.

Avoid: copying or mirroring the right side; wrong front/rear order; yellow warning label; generic blank panel; rails; feet; vents; pseudo-text; floor; shadow; reflection; CGI cleanup; smoothing; exaggerated embossing.

selected_output: `views/left.png`

chroma_source: `qa/imagegen-output/left-chroma.png`

output_record: one built-in imagegen call; magenta removed with the installed imagegen chroma helper; measured rectification to 3000x339; left-side slots and asymmetric boss/hole pattern retained without a yellow label.
