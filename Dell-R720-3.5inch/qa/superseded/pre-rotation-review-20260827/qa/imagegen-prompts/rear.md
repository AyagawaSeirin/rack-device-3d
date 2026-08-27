# rear.png generation record

- method: built-in `image_gen`
- use_case: product-mockup
- production_mode: SOURCE_LOCKED_GENERATION
- input_roles:
  - Image 1: PRIMARY BINDING USER CONFIGURATION-LOCK FACE PHOTO CROP — exact rear assembly, port order, blanking state and dual-AC configuration.
  - Image 2: BINDING OFFICIAL OWNER'S-MANUAL REAR FIGURE — exact R720 versus R720xd geometry.
  - Image 3: SUPPORTING OFFICIAL TECHNICAL-GUIDE R720 REAR COLOR FIGURE.
  - Image 4: SUPPORTING EXACT R720 8-LFF REAL REAR PHOTO — real relief/material, 750 W AC PSU construction.
  - Image 5: SUPPORTING EXACT R720 REAL REAR PHOTO — connector and fan detail.

## Final prompt

Use case: product-mockup. Asset type: exact rear orthographic face asset for a website GLB. Generate a new, perfectly straight-on rear view of the exact Dell PowerEdge R720 configuration shown in Image 1. Image 1 is the highest-authority binding assembly/layout/orientation reference. Images 2-3 bind the official R720 seven-slot rear and explicitly exclude the R720xd rear flex-bay. Images 4-5 bind real metal, connector, handle, fan and PSU photographic material character.

Required rear inventory, in the exact source order: three stacked low-profile perforated PCIe blanking plates labeled positions 1-3 at the upper left; four full-height perforated PCIe blanking plates in two rows/two columns labeled 4-7 across the upper middle/right; no installed add-in-card connectors; one black rear carrying handle; system-ID button and connector; exactly one dedicated iDRAC7 Enterprise RJ45; one teal/dark DB9 serial; one blue VGA; exactly two black USB 2.0 ports; one Select Network Adapter block with exactly four side-by-side RJ45 Ethernet ports; two complete hot-plug 750 W AC PSU modules with one IEC AC inlet, orange release latch, circular fan hub/blades and grille per PSU; upper-right perforated ventilation field. Preserve normal text orientation. Keep dark rear end strips within the 444 mm body width; do not create rear rack ears.

Output one complete rear face only, centered, physical silhouette ratio 444:87.3, no top or side visible, no perspective, no floor, cable, rail, annotation, shadow or reflection. SOURCE-LOCKED real product photography: same silver galvanized steel, black plastic, blue/teal port color, orange latches, real scratches, recess shadows, edge softness and restrained highlights as the references; not CGI cleanup or illustration.

Scene/backdrop: perfectly flat solid #FF00FF chroma-key background, completely uniform with no gradient, texture, floor, shadow or reflection. Do not use #FF00FF on the device. Avoid R720xd rear drives, SFF/R730 substitution, DC terminal blocks, missing or extra Ethernet/USB/PCIe/PSU parts, fake cards, pseudo-text, mirrored slot order, repeated AI patterns, seller stickers and watermarks.

## Final selection

- selected_generation: `qa/imagegen-staging/rear-v2-chroma.png`
- alpha_master: `qa/imagegen-staging/rear-v2-alpha.png`
- final_output: `views/rear.png`
- selection_reason: preserves the standard seven-slot R720 rear, required port order and two matching 750 W AC PSU faces without false rear ears.
- superseded_generation: `qa/imagegen-staging/rear-final-chroma.png` — retained as provenance, not shipped.
