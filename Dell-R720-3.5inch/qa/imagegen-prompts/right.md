# right.png generation record

- method: built-in `image_gen`
- use_case: product-mockup
- production_mode: SOURCE_LOCKED_GENERATION
- input_roles:
  - Image 1: PRIMARY BINDING DIRECT OPPOSITE-SIDE R720 REAL PHOTO — independent plain side, seam, fastener and hook pattern; front is at image left.
  - Image 2: SUPPORTING EXACT R720 8-LFF REAL PHOTO — requested LFF identity and matching side/front boundary.
  - Image 3: SUPPORTING EXACT R720 8-LFF REAL REAR PHOTO — matching opposite rear boundary, top and metal.
  - Image 4: OFFICIAL DIMENSION DIAGRAM — physical proportions only.

## Final prompt

Use case: product-mockup. Asset type: exact right-side orthographic face asset for a website GLB. Generate a new perfectly orthographic Dell PowerEdge R720 right side. Image 1 is the highest-authority direct real opposite-side reference: preserve its independent plain galvanized side shell, upper cover seam, non-mirrored hook-tab sequence, shallow stamped rail interface, exact sparse screw/fastener character and absence of the large black regulatory labels seen on the other side. The front of the server is at the LEFT edge of the resulting right-side image. Images 2-3 bind the exact R720 8 x 3.5-inch LFF/no-bezel assembly and rear/top boundaries. Image 4 binds proportions only.

Output one complete closed right side only, physical ratio 741:87.3 including verified front/rear silhouette, no top, bottom, front or rear face visible, no perspective. Preserve a straight lower edge and no installed rails. This is independent and must not be a mirrored left side. Do not add label blocks from the left face.

SOURCE-LOCKED real product photography: real galvanized sheet grain, minor wear, neutral silver color, soft highlights, stamped seam shadows and physical edge character as Image 1. No CGI cleanup, smoothing, relighting, illustration, vectorization or stylization. Scene/backdrop: perfectly flat uniform #FF00FF chroma-key with no gradient, floor, shadow, reflection or texture; no #FF00FF on the chassis. No cables, rails, hands, background, seller labels, watermark, fake vents, feet or invented hardware.

## Final selection

- selected_generation: `qa/imagegen-staging/right-alpha.png` (approved first-pass master)
- alpha_master: `qa/imagegen-staging/right-alpha.png`
- final_output: `views/right.png`
- selection_reason: preserves the independent plain side, front-at-left orientation and intentionally different fastener/hook pattern from the left face.
- rejected_revision: `qa/imagegen-staging/right-v2-rejected-chroma.png` — rejected for source-detail drift; no mirroring was used.
