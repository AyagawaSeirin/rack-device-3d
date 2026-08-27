# Juniper MX304 final QA report

Final status: **PASS_WITH_BOTTOM_FALLBACK**

This report supersedes the pre-rotation report preserved at
`qa/superseded/pre-rotation-review-20260827/qa/qa-report.md`.

- Exact target: MX304-PREM-AC-FS physical configuration, 2U, two JNP304-RE above two MX304-LMIC16-BASE, dual JNP-PWR2200-AC, three JNP-FAN-2RU, no optional filter/cable manager.
- Pre-rotation standard/web SHA-256: `6bd23219b2467b756de4d6f8d990ef539a0719136a28b7d8e9ae2b2ec34c3332` / `7f240baeb6ce9e8751e49bae90b0a2b40478d75dd76c673f9e2691fe9e9fc9e5`.
- Final standard/web SHA-256: `4c6cdc6b165e43159291024f61282c9b34e22122bb50a99bafbde4adffc47d2f` / `ac58cde384950e27af7154d21f0d785b25982257e55cf2ee684d2cb539d49251`.
- Repair: the former open six-card shell now has a positive-volume closed core and inset front/rear backing; the unsupported coplanar top-seam box was removed; all face cards have stable separation and `CLAMP_TO_EDGE` sampling. The build no longer depends on a missing `/tmp` package tree.
- Structural gates: `audit_views` PASS with zero errors; both `audit_glb` files PASS with zero errors/warnings; both supplemental structural audits PASS with no alpha, duplicate/opposite triangle, visible coplanar, negative-transform, sampler, or closed-core error.
- Browser gate: 40 independent cache-busted loads and 304 final rotation/pitch frames across Three.js/Babylon.js and standard/web; no flicker, transparency jump, checker leak, disappearing face, mirror, texture switch, or gray transition.
- Feature inventory: 36/36 rows matched, zero unresolved; the independently reconstructed right face is not a horizontal flip.
- Residual warning: exact underside imagery remains unavailable; only the controlled generic-bottom fallback remains.

Full evidence: `qa/rotation-review-20260827/FINAL-ROTATION-REVIEW.md` and `rotation-stress-report.json`.
