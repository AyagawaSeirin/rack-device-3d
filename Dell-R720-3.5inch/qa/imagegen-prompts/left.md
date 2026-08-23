# left.png generation record

- method: built-in `image_gen`
- use_case: product-mockup
- production_mode: SOURCE_LOCKED_GENERATION
- input_roles:
  - Image 1: PRIMARY BINDING DIRECT R720 LEFT-SIDE REAL PHOTO — independent seam, label, screw and rail-hook layout; front is at image right.
  - Image 2: SUPPORTING REAL LEFT-SIDE/TOP CLOSE PHOTO — cover hooks and stamped relief.
  - Image 3: SUPPORTING EXACT R720 8-LFF REAL PHOTO — LFF assembly identity and matching shell/material.
  - Image 4: SUPPORTING EXACT R720 8-LFF REAL PHOTO — matching top/front edge and factory metal.

## Final prompt

Use case: product-mockup. Asset type: exact left-side orthographic face asset for a website GLB. Generate a new perfectly orthographic Dell PowerEdge R720 left side. Image 1 is the primary binding direct real side photograph: preserve its independent left-side upper cover seam, hook-tab sequence, shallow stamped rail interface, screw locations, two large black regulatory labels plus the smaller white label, galvanized texture, wear, brightness and real photographic character. The front of the server is at the RIGHT edge of the resulting left-side image, as in Image 1. Images 3-4 bind the requested exact R720 8 x 3.5-inch LFF/no-bezel assembly; they may not alter the side evidence.

Output one complete closed left side only, physical ratio 741:87.3 including the verified front/rear silhouette, no top, bottom, front or rear face visible, no perspective. Keep the top cover seam and hook tabs as shallow mechanical relief; keep factory labels as real flush labels but do not invent readable serial numbers or QR data. Preserve the straight lower edge and no installed rails. This is independently reconstructed; do not mirror the right side.

SOURCE-LOCKED real product photography: same galvanized metal grain, small scratches, imperfect label texture, neutral white balance, soft highlights and shallow seam shadows as Image 1. No CGI cleanup, smoothing, relighting, illustration, vectorization or stylization. Scene/backdrop: perfectly flat uniform #FF00FF chroma-key with no gradient, floor, shadow, reflection or texture; no #FF00FF on the chassis. No cable, rail, hand, background, seller label, watermark, fake vents, extra feet or invented hardware.

## Final selection

- selected_generation: `qa/imagegen-staging/left-v1-chroma.png`
- alpha_master: `qa/imagegen-staging/left-alpha.png`
- final_output: `views/left.png`
- selection_reason: preserves the independently evidenced label blocks, seam/hook sequence and front-at-right orientation.
- rejected_revision: `qa/imagegen-staging/left-v2-rejected-chroma.png` — rejected for source-detail and silhouette drift.
