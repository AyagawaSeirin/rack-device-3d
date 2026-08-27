# bottom.png generation record

- method: built-in `image_gen`
- use_case: product-mockup
- production_mode: GENERIC_BOTTOM_FALLBACK
- input_roles:
  - Image 1: INSPECTED GENERIC DELL UNDERSIDE REAL PHOTO — galvanized material character only; all geometry/non-R720 markings are forbidden.
  - Image 2: VERIFIED R720 LEFT-SIDE REAL PHOTO — lower-edge color and straight silhouette.
  - Image 3: VERIFIED R720 RIGHT-SIDE REAL PHOTO — opposite lower-edge color and straight silhouette.
  - Image 4: OFFICIAL DIMENSION DIAGRAM — exact 444 x 702 mm body ratio.

## Final prompt

Use case: product-mockup. Asset type: conservative bottom orthographic face asset for a Dell PowerEdge R720 website GLB. Production mode GENERIC_BOTTOM_FALLBACK after documented exact-model underside search exhaustion. Image 1 controls only generic Dell galvanized sheet-metal color, grain and photographic character; do not copy any of its holes, keyholes, feet, labels, access panels, seams, fasteners or rails because it is not an R720. Images 2-3 bind only the verified R720 straight lower side edges, silver material and absence of silhouette-changing feet/rails. Image 4 binds the 444:702 body ratio.

Generate one perfectly straight bottom-up face: a deliberately conservative, non-identifying, opaque galvanized rectangular sheet at physical ratio 444:702, front at the BOTTOM and rear at the TOP. No branding, model text, service label, QR code, vents, holes, keyholes, access panels, feet, rails, seams, screws, fasteners, protrusions or decorative detail. Do not mirror the top. Do not invent any mechanical feature.

Match real dull galvanized sheet grain, soft highlights and neutral color without CGI cleanup or illustration. Scene/backdrop: perfectly flat uniform #FF00FF chroma-key with no gradient, floor, shadow, reflection or texture; do not use #FF00FF on the sheet. One complete face only, no adjacent face or perspective.

## Final selection

- selected_generation: `qa/imagegen-staging/bottom-v2-chroma.png`
- alpha_master: `qa/imagegen-staging/bottom-v2-alpha.png`
- final_output: `views/bottom.png`
- selection_reason: deliberately conservative material-only fallback with no unsupported R720 underside geometry, labels, vents or holes.
- status_constraint: exact R720 underside was not found after the documented search; final delivery cannot be plain PASS.
