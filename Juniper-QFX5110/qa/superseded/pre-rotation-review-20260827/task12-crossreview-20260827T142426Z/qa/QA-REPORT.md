# Juniper QFX5110 final QA report

Final status: **PASS_WITH_BOTTOM_FALLBACK**

This report supersedes the pre-rotation report preserved at
`qa/superseded/pre-rotation-review-20260827/qa/QA-REPORT.md`.

- Exact target: QFX5110-48S-AFI, 1U, 48 SFP+ + 4 QSFP28, five azure AFI fans, dual 650 W AC-AFI PSUs, verified front ears, no rear ears.
- Pre-rotation standard/web SHA-256: `9443641983d78bfbdd0d5ee32d0b76697a62aefe8198219b96adc850456d6373` / `66646169651e414142aa224d7357b8e70fb84fd3ddf2df9ff64065e71165a113`.
- Final standard/web SHA-256: `079472babeefd92349789edeb28f33635c04fcb9086dfd900e7fcb0e4325ac59` / `cdd30d96cfe04c2ba44cfe27176c89fcb5267b266ccb6543f3ddbac04a9ee53d`.
- Repair: front source-locked relief overlays now have 0.20 mm deterministic clearance; all texture samplers use `CLAMP_TO_EDGE`.
- Structural gates: `audit_views` PASS with zero errors; both `audit_glb` files PASS with zero errors/warnings; both supplemental structural audits PASS with no alpha, duplicate/opposite triangle, visible coplanar, negative-transform, sampler, or closed-core error.
- Browser gate: 40 independent cache-busted loads and 304 final rotation/pitch frames across Three.js/Babylon.js and standard/web; no flicker, transparency jump, checker leak, disappearing face, mirror, texture switch, or gray transition.
- Feature inventory: 30/30 rows matched, zero unresolved.
- Residual warning: exact underside imagery remains unavailable; only the controlled generic-bottom fallback remains.

Full evidence: `qa/rotation-review-20260827/FINAL-ROTATION-REVIEW.md` and `rotation-stress-report.json`.
