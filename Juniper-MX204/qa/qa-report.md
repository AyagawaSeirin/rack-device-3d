# Juniper MX204 final QA report

Final status: **PASS_WITH_BOTTOM_FALLBACK**

This report supersedes the pre-rotation report preserved at
`qa/superseded/pre-rotation-review-20260827/qa/qa-report.md`.

- Exact target: MX204-HW-BASE AC physical variant, 1U, fixed empty-port front, three JNP-FAN-1RU AFO modules, dual JPSU-650W-AC-AO, verified front/rear bracket state and side rails.
- Pre-rotation standard/web SHA-256: `ebb52cb184647cf599e33fd3fdd7b441d15b85f367e4233a91ad9f494732d696` / `ceada7361c08e13c88ee6435ab75566c108c0539021f2d90845b9189f3c6c0a7`.
- Final standard/web SHA-256: `c927683dfb231b67684a2c7b903b5a1b94df259484b50b7092108960f87561e7` / `7a4d94e867ea741dee197c26fc9e22bd28c3625ff832d4fbcbce99d4bf247506`.
- Repair: all embedded face textures are RGB, main six face materials are OPAQUE/unlit with neutral factors, and all texture samplers use `CLAMP_TO_EDGE`; the independently sourced right rail remains non-mirrored.
- Structural gates: `audit_views` PASS with zero errors; both `audit_glb` files PASS with zero errors/warnings; both supplemental structural audits PASS with no alpha, duplicate/opposite triangle, visible coplanar, negative-transform, sampler, or closed-core error.
- Browser gate: 40 independent cache-busted loads and 304 final rotation/pitch frames across Three.js/Babylon.js and standard/web; no flicker, transparency jump, checker leak, disappearing face, mirror, texture switch, or gray transition.
- Feature inventory: 27/27 rows matched, zero unresolved.
- Residual warning: exact underside imagery remains unavailable; only the controlled generic-bottom fallback remains.

Full evidence: `qa/rotation-review-20260827/FINAL-ROTATION-REVIEW.md` and `rotation-stress-report.json`.
