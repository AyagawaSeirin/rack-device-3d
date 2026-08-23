# Physical-left ratio repair record

- production mode: `MULTI_REFERENCE_RECONSTRUCTION`
- built-in generation/edit path: `image_gen`, one dedicated call per attempt
- primary binding real photograph: `source/originals/official-gallery-rear_left.png`
- binding orthographic geometry: `qa/reference/official-orthographic/left.png`
- defect example only: the prior generated `views/left.png`
- physical target: `457.9 / 43.6 = 10.5023:1` for the complete silhouette, with a `420 / 43.6 = 9.6330:1` chassis body and a separate 37.9 mm rear U-bracket projection

## Attempt history

1. `qa/imagegen-raw/left-ratio-v3-key.png` / `qa/imagegen-alpha/left-ratio-v3.png`: source-guided regeneration retained identity but remained too thick at about 9.60:1; rejected.
2. `qa/imagegen-raw/left-ratio-v4-key.png` / `qa/imagegen-alpha/left-ratio-v4.png`: targeted vertical reduction overshot to about 11.82:1; rejected.
3. `qa/imagegen-raw/left-ratio-v5-key.png` / `qa/imagegen-alpha/left-ratio-v5.png`: ratio reached 10.29:1 but the powder coat drifted into an invented curly texture; rejected for source-style drift.
4. The final material-restoration edit also retained invented curly texture; rejected and not copied into `views/`.

## Final selected result

The final `views/left.png` keeps the earlier source-locked photographic material and verified feature layout, then applies only a dimension-ledger-driven orthographic projection correction to a 3072 x 293 px content box. No holes, fasteners, vent, U bracket, orientation, colors, or material pixels were invented or replaced. Final alpha>=8 total-silhouette ratio error is `-0.2006%`; the low-alpha and fully opaque threshold sweep remains within the 3% QA tolerance.

The rejected built-in attempts remain under `qa/imagegen-raw/` and `qa/imagegen-alpha/` and never outrank the binding real photograph.
