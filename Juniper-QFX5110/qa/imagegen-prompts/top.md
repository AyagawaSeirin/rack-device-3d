# top.png generation record

- method: built-in `image_gen`, one dedicated call
- production_mode: `MULTI_REFERENCE_RECONSTRUCTION`
- raw_output: `qa/work/imagegen-raw/top.png`
- final_output: `views/top.png`
- input_roles:
  1. official exact-model front-top real photo — primary cover identity/material/style
  2. exact-model EveryChina top/front photo — front screw line and wear; cable/optics excluded
  3. exact-model EveryChina top/rear photo — rear cover edge/screws; label and pulled handles excluded
  4. exact AFI dual-AC NW工房 rear/top photo — complete proportions/rear edge

## Final prompt

Reconstruct a perfectly top-down orthographic TOP cover of the exact Juniper QFX5110-48S-AFI, front/port end at image-bottom and rear/FRU end at image-top, body ratio 440.944:520.192. Preserve one real gray painted sheet-metal cover, exact perimeter/folded seams, real screw locations, subtle wear and one very faint large embossed Juniper wordmark in its real position and normal orientation. Match the primary photo's grain, color, contrast and highlight softness; no CGI cleanup, relighting, beautification, smoothing, denoising, recoloring or vectorization. Body cover only; front ears and rear handles are separate geometry. No vents, holes, feet, rails, service/serial/QR label or decorative panel. Flat uniform `#FF00FF`, all cover pixels opaque, no adjacent face, shadow, cable, fan, PSU, ear, watermark or invented detail.
