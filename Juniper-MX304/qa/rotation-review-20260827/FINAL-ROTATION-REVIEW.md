# Juniper-MX304 final rotation and authenticity review

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Hashes

- Pre-rotation standard: `6bd23219b2467b756de4d6f8d990ef539a0719136a28b7d8e9ae2b2ec34c3332`
- Pre-rotation web: `7f240baeb6ce9e8751e49bae90b0a2b40478d75dd76c673f9e2691fe9e9fc9e5`
- Final standard: `4c6cdc6b165e43159291024f61282c9b34e22122bb50a99bafbde4adffc47d2f`
- Final web: `ac58cde384950e27af7154d21f0d785b25982257e55cf2ee684d2cb539d49251`

## Result

- The preserved pre-rotation checkpoint did not reproduce a visible full-surface flicker in 4 x 72 yaw frames; this report does not invent a before failure.
- Causal structural risk repaired: Replaced the open six-card shell with a positive-volume closed core plus inset front/rear backing; removed coplanar top-seam duplication; clamped face samplers.
- Skill `audit_views`: PASS with zero errors; alpha warnings were visually resolved as external antialiasing/true rack openings and do not enter the RGB GLBs.
- Skill `audit_glb`: standard/web PASS, zero errors and zero warnings.
- Supplemental duplicate/coplanar, material-alpha, sampler, negative-transform, and closed-core audits: standard/web PASS, zero unresolved errors.
- Standard/web world geometry is identical: `True` (50342 triangles across 121 scene nodes).
- Final browser gate: 40 independent cache-busted loads (2 engines x 2 GLBs x 10 views), all successful.
- Final rotation gate: 72 yaw frames plus 4 pitch frames per engine/GLB combination, 304 total final frames; no flicker, alpha jump, checker leak, disappearing face, mirror, texture switch, or gray transition.
- Feature inventory: 36 rows reviewed, zero unresolved.
- Exact PID/configuration and all five non-bottom faces remain verified against current official/local authoritative evidence. No public official exact-PID GLB/glTF/CAD was found.

## Residual warning

Only the documented `GENERIC_BOTTOM_FALLBACK` remains. It is conservative and non-identifying, so the status ceiling is `PASS_WITH_BOTTOM_FALLBACK` rather than ordinary PASS.
