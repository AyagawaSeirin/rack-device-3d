# front.png generation record

- method: built-in `image_gen`
- use_case: product-mockup
- production_mode: SOURCE_LOCKED_GENERATION
- input_roles:
  - Image 1: PRIMARY BINDING USER CONFIGURATION-LOCK FACE PHOTO CROP — exact 8-LFF/no-bezel identity, count, layout, orientation and photographic character.
  - Image 2: BINDING OFFICIAL OWNER'S-MANUAL FIGURE — exact named controls and 2 x 4 geometry; diagram does not control color.
  - Image 3: SUPPORTING EXACT R720 8-LFF REAL PHOTO — carrier construction, metal/plastic texture and factory branding.
  - Image 4: SUPPORTING EXACT R720 8-LFF REAL PHOTO — top control band, side latches and material detail.

## Final prompt

Use case: product-mockup. Asset type: exact front orthographic face asset for a website GLB. Generate a new, perfectly straight-on front view of the exact Dell PowerEdge R720 2U 8 x 3.5-inch LFF configuration shown in Image 1, with no security bezel. Image 1 is the highest-authority binding configuration and face-layout reference; preserve its identity, 2 x 4 carrier count, spacing, left/right order, materials, real-product photographic character and orientation. Image 2 binds official geometry and control identities. Images 3-4 are exact R720 8-LFF real photographs that bind carrier, metal, plastic, color and fine material character without changing Image 1.

Required front inventory: two separate black front rack latch/ear assemblies; eight complete 3.5-inch LFF carriers in exactly two rows by four columns, each with its real silver horizontal handle and black four-aperture face; upper black control band with Dell mark, power/NMI/system-ID controls, one VGA, three LCD menu buttons, blue LCD with readable `PowerEdge R720`, one vFlash slot, exactly two USB 2.0 ports, factory information pull-tab area and one slim optical-drive tray at the upper right. Keep the factory Dell and PowerEdge R720 text in the same real location and normal reading orientation. Every carrier is present. No front bezel.

Output one complete front face only, centered, physical silhouette ratio 482.4:87.3, no top or side visible, no perspective, no floor, cable, rail, annotation, detached fragment, shadow or reflection. SOURCE-LOCKED real product photography: preserve the primary photograph's neutral black/silver color balance, genuine painted plastic and metal grain, small recess shadows, imperfect physical edge character and soft highlights; use the exact-LFF real photos only to recover detail. Do not beautify, relight, smooth, denoise into CGI, recolor, vectorize, toon-shade or create a generic product render.

Scene/backdrop: perfectly flat solid #FF00FF chroma-key background for local removal, one uniform color with no gradient, texture, floor, shadow or reflection. Do not use #FF00FF on the device. Crisp complete silhouette with padding. Avoid pseudo-text, fake service tags, fake QR codes, invented LEDs/displays/ports, changed counts, repetition, artificial symmetry, mirroring, R720xd, SFF, R730, bezel, seller labels and watermarks.

## Final selection

- selected_generation: `qa/imagegen-staging/front-v1-chroma.png`
- alpha_master: `qa/imagegen-staging/front-alpha.png`
- final_output: `views/front.png`
- selection_reason: preserves the user-locked 2 x 4 LFF layout, no-bezel state, genuine DELL/PowerEdge R720 marks and all eight carriers.
- rejected_revision: `qa/imagegen-staging/front-v2-rejected-chroma.png` — rejected for pseudo-label/detail drift.
