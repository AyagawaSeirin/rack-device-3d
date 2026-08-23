# Physical-right ratio repair record

- production mode: `MULTI_REFERENCE_RECONSTRUCTION`
- built-in generation/edit path: `image_gen`, one dedicated call per attempt
- primary binding real photograph: `source/originals/official-gallery-rear_right.png`
- binding orthographic geometry: `qa/reference/official-orthographic/right.png`
- defect example only: the prior generated `views/right.png`
- physical target: `457.9 / 43.6 = 10.5023:1` for the complete silhouette, with a `420 / 43.6 = 9.6330:1` chassis body and a separate 37.9 mm rear U-bracket projection

## Attempt history

1. `qa/imagegen-raw/right-ratio-v3-key.png` / `qa/imagegen-alpha/right-ratio-v3.png`: source-guided regeneration retained the right-only label/equipotential identity but remained too thick at about 9.59:1; rejected.
2. `qa/imagegen-raw/right-ratio-v4-key.png` / `qa/imagegen-alpha/right-ratio-v4.png`: ratio reached about 10.62:1, but the powder coat drifted into an invented curly texture; rejected for source-style drift.

## Final selected result

The final `views/right.png` keeps the earlier source-locked photographic material, warranty label, two-stud equipotential terminal, exact hole layout, and right-side orientation, then applies only a dimension-ledger-driven orthographic projection correction to a 3072 x 293 px content box. Final alpha>=8 total-silhouette ratio error is `+0.1738%`; every audited alpha threshold remains within the 3% tolerance.

The rejected built-in attempts remain under `qa/imagegen-raw/` and `qa/imagegen-alpha/` and never outrank the binding real photograph.
