# top.png generation record

- method: built-in `image_gen`
- use_case: product-mockup
- production_mode: MULTI_REFERENCE_RECONSTRUCTION
- input_roles:
  - Image 1: PRIMARY EXACT R720 8-LFF REAL FRONT-THREE-QUARTER PHOTO — top cover, latch, transverse front details and right edge.
  - Image 2: BINDING EXACT R720 8-LFF REAL FRONT-THREE-QUARTER PHOTO — cover material, sparse screws and opposite edge.
  - Image 3: BINDING EXACT R720 8-LFF REAL REAR-ELEVATED PHOTO — rear boundary and latch position.
  - Image 4: SUPPORTING EXACT R720 8-LFF REAL PHOTO — top silhouette; security bezel is excluded.
  - Image 5: OFFICIAL DIMENSION DIAGRAM — 444 x 702 mm top body ratio.

## Final prompt

Use case: product-mockup. Asset type: exact top orthographic face asset for a website GLB. No direct orthographic top photo exists, so reconstruct only the jointly proven Dell PowerEdge R720 8 x 3.5-inch LFF top from Images 1-5. Preserve the exact LFF identity and no-bezel delivered state. Generate one perfectly straight top-down view of the closed 444 x 702 mm galvanized top body. Front is at the BOTTOM of the image and rear at the TOP.

Required proven top inventory: one large removable galvanized cover with real perimeter and transverse seams; one black rectangular latch in the rear half, offset left of center as jointly shown; sparse small round cover fasteners; a transverse front information-label band with white/orange/black factory graphics (do not invent readable serial or QR data); a narrow front perforated ventilation band; correct folded metal edges. Do not reveal the interior. Do not copy the top from another generation and do not add vents, handles, raised modules or labels not jointly visible in the exact-LFF sources.

Physical content ratio 444:702. Real product photography matching the exact-LFF photographs: neutral galvanized silver, real sheet grain and slight wear, soft broad highlights, shallow seam shadows and unpolished factory character. No CGI cleanup, symmetry correction, smoothing, relighting, vector art, illustration or game-asset look. Scene/backdrop: perfectly flat uniform #FF00FF chroma-key, no gradient, floor, cast shadow, reflection or texture; no #FF00FF on the device. One complete face, no adjacent sides, perspective, cables, rails, watermark or seller sticker.

## Final selection

- selected_generation: `qa/imagegen-staging/top-v1-chroma.png`
- alpha_master: `qa/imagegen-staging/top-alpha.png`
- final_output: `views/top.png`
- selection_reason: preserves the jointly evidenced front information band, vent strip, cover seam and single rear-biased latch.
- rejected_revision: `qa/imagegen-staging/top-v2-rejected-chroma.png` — rejected for altered factory graphics/detail drift.
