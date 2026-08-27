# Final rotation and authenticity review — Huawei-RH1288V5-2.5inch

Status: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen identity

Huawei FusionServer Pro 1288H V5, 1U, exact 10 x 2.5-inch SFF configuration

Exact identity/configuration passed for front, rear, both non-mirrored sides and top. The underside remains the documented conservative GENERIC_BOTTOM_FALLBACK only.

## Hashes

- Old standard: `5aab50a1f7bf6874bf5ecd2a611fc2463f6f511ab935d84783d19c3b488c93e5`
- Old web: `b1f245d86e60e63b97ae332af6eb9f11fd1faedaffba6728e9c998c7e8b538bc`
- Final standard: `dec12900443e05b1abe79448c6f4f880be993fb235a7107832cca209fc2b8205`
- Final web: `10d74d846285762a9fbbc61a8213126b716bf97fe0aae7c54765600bd9fdc121`

## Reproduction and root cause

No whole-shell alpha jump appeared in the physically correct v3/v4 baseline, but the old GLBs reproducibly failed the structural rotation gate with 314 render-risk coplanar pairs. The superseded extreme-depth viewer also demonstrated how these layers can become angle-dependent.

Root cause: Near/coplanar source-locked face cards, relief/core caps and rear patches; redundant top vent cap boxes; insufficient separation at carrier handles, cover seams/latch and side details.

## Repair

- Reduced the hidden closed-core depth while preserving the installed envelope.
- Separated rear cover patches, carrier bodies/handles, cover seams/latch/steps and side relief from source surfaces by stable physical offsets.
- Removed 88 redundant coplanar top-vent cap boxes; the dense, flush perforation remains in the approved opaque high-resolution source texture.

## Final gates

- `audit_glb`: standard/web PASS, 0 errors, 0 warnings.
- `audit_views`: PASS, 0 errors; 5 alpha warnings manually resolved because every affected face has 0% core alpha below 250 and 0% transparent core.
- Standard/web geometry, UV and transform fingerprint parity: PASS.
- Static real-browser loads: 40/40 (Three.js + Babylon.js; standard + web; ten prescribed views), all WebGL2, ready, correct hash, zero recorded errors.
- Rotation stress: 96 frames per viewer/model combination (72 yaw at 5-degree increments + 24 pitch/checker frames), four final combinations, 384 final frames. Every automated gate and manual contact-sheet review passed.
- Matched orthographic source/render/overlay/difference rows: 6; authoritative three-quarter supporting overlays: 0; feature inventory rows checked: 32/32.

## Structural results

- standard: duplicate 0; opposite duplicate 0; source-surface coplanar hazards 0; degenerate 0; normal mismatches 0; negative transforms 0; material violations 0; partial-alpha images 0; closed core True; informational opaque solid contacts 32.
- web: duplicate 0; opposite duplicate 0; source-surface coplanar hazards 0; degenerate 0; normal mismatches 0; negative transforms 0; material violations 0; partial-alpha images 0; closed core True; informational opaque solid contacts 32.

## Warnings / residual risk

- Bottom-only evidence fallback; no non-bottom identity gap.
- Opaque solid/interior coplanar contact counts are retained as informational mechanical intersections; source-surface hazard count is zero in both final GLBs.

Machine-readable evidence: `qa/rotation-stress-report.json`; static loads: `qa/rotation-review/after/static-loads/static-40-loads.json`; matched-camera/feature review: `qa/rotation-review/after/matched-camera/matched-camera-manifest.json`.
