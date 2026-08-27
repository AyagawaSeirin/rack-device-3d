# Juniper-MX204 final rotation and authenticity review

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Hashes

- Pre-rotation standard: `ebb52cb184647cf599e33fd3fdd7b441d15b85f367e4233a91ad9f494732d696`
- Pre-rotation web: `ceada7361c08e13c88ee6435ab75566c108c0539021f2d90845b9189f3c6c0a7`
- Final standard: `c927683dfb231b67684a2c7b903b5a1b94df259484b50b7092108960f87561e7`
- Final web: `7a4d94e867ea741dee197c26fc9e22bd28c3625ff832d4fbcbce99d4bf247506`

## Result

- The preserved pre-rotation checkpoint did not reproduce a visible full-surface flicker in 4 x 72 yaw frames; this report does not invent a before failure.
- Causal structural risk repaired: Flattened embedded face images to RGB, made all six baked photographic faces OPAQUE/unlit, and clamped face samplers.
- Skill `audit_views`: PASS with zero errors; alpha warnings were visually resolved as external antialiasing/true rack openings and do not enter the RGB GLBs.
- Skill `audit_glb`: standard/web PASS, zero errors and zero warnings.
- Supplemental duplicate/coplanar, material-alpha, sampler, negative-transform, and closed-core audits: standard/web PASS, zero unresolved errors.
- Standard/web world geometry is identical: `True` (10340 triangles across 168 scene nodes).
- Final browser gate: 40 independent cache-busted loads (2 engines x 2 GLBs x 10 views), all successful.
- Final rotation gate: 72 yaw frames plus 4 pitch frames per engine/GLB combination, 304 total final frames; no flicker, alpha jump, checker leak, disappearing face, mirror, texture switch, or gray transition.
- Feature inventory: 27 rows reviewed, zero unresolved.
- Exact PID/configuration and all five non-bottom faces remain verified against current official/local authoritative evidence. No public official exact-PID GLB/glTF/CAD was found.

## Residual warning

Only the documented `GENERIC_BOTTOM_FALLBACK` remains. It is conservative and non-identifying, so the status ceiling is `PASS_WITH_BOTTOM_FALLBACK` rather than ordinary PASS.
