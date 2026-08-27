# Juniper-QFX5110 final rotation and authenticity review

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Hashes

- Pre-rotation standard: `9443641983d78bfbdd0d5ee32d0b76697a62aefe8198219b96adc850456d6373`
- Pre-rotation web: `66646169651e414142aa224d7357b8e70fb84fd3ddf2df9ff64065e71165a113`
- Final standard: `079472babeefd92349789edeb28f33635c04fcb9086dfd900e7fcb0e4325ac59`
- Final web: `cdd30d96cfe04c2ba44cfe27176c89fcb5267b266ccb6543f3ddbac04a9ee53d`

## Result

- The preserved pre-rotation checkpoint did not reproduce a visible full-surface flicker in 4 x 72 yaw frames; this report does not invent a before failure.
- Causal structural risk repaired: Reduced front relief/texture depth precision risk by increasing the verified overlay clearance to 0.20 mm; clamped all face samplers to stop mip-edge wrap.
- Skill `audit_views`: PASS with zero errors; alpha warnings were visually resolved as external antialiasing/true rack openings and do not enter the RGB GLBs.
- Skill `audit_glb`: standard/web PASS, zero errors and zero warnings.
- Supplemental duplicate/coplanar, material-alpha, sampler, negative-transform, and closed-core audits: standard/web PASS, zero unresolved errors.
- Standard/web world geometry is identical: `True` (5018 triangles across 39 scene nodes).
- Final browser gate: 40 independent cache-busted loads (2 engines x 2 GLBs x 10 views), all successful.
- Final rotation gate: 72 yaw frames plus 4 pitch frames per engine/GLB combination, 304 total final frames; no flicker, alpha jump, checker leak, disappearing face, mirror, texture switch, or gray transition.
- Feature inventory: 30 rows reviewed, zero unresolved.
- Exact PID/configuration and all five non-bottom faces remain verified against current official/local authoritative evidence. No public official exact-PID GLB/glTF/CAD was found.

## Residual warning

Only the documented `GENERIC_BOTTOM_FALLBACK` remains. It is conservative and non-identifying, so the status ceiling is `PASS_WITH_BOTTOM_FALLBACK` rather than ordinary PASS.
