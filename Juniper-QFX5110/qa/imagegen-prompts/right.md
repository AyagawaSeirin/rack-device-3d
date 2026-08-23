# right.png generation record

- method: built-in `image_gen`, one dedicated call
- production_mode: `MULTI_REFERENCE_RECONSTRUCTION`
- raw_output: `qa/work/imagegen-raw/right.png`
- final_output: `views/right.png` (canonical body panel; front ear and rear handle silhouettes are retained as separate GLB geometry)
- input_roles:
  1. official exact-model right-labeled real photo — primary identity/material/style and slot placement
  2. official exact-model opposite-side real photo — proportion/finish cross-check, never mirrored
  3. exact-model EveryChina rack-ear close-up — front-ear profile only
  4. exact AFI dual-AC NW工房 rear/top photo — rear projection only

## Final prompt

Reconstruct one perfectly side-on orthographic physical RIGHT SIDE of Juniper QFX5110-48S-AFI. Preserve the exact dark-gray folded sheet-metal panel, top/bottom seams, every narrow stamped rail/mount slot at its real row and longitudinal position from the primary right-side photo, and the verified front-ear attachment/rear projections. It must not be a mirror of the left. Front at image-left, rear at image-right; no adjacent face or perspective. Same real metal grain, wear, color balance and soft highlights as the primary photo; no CGI cleanup, relighting, smoothing, denoising, vectorization or restyle. No side logo, label, vent grille, foot, full rail or invented screw. Flat uniform `#FF00FF`, all product pixels opaque, no shadow/cables/seller label/watermark/family substitution. Canonical panel normalized to 520.192:43.688; separable protrusions remain geometry.
