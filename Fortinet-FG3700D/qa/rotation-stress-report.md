# Final rotation and authenticity review — Fortinet-FG3700D

Status: **PASS**

## Frozen identity

Fortinet FortiGate FG-3700D / FG-3700D-USG AC, exact 3U installed configuration

Exact 4-QSFP+/28-SFP front, dual AC PSU rear, three rotor openings/six FAN indicators, rack handles, non-mirrored sides and exact underside passed.

## Hashes

- Old standard: `0961f7873bd7fb4ae7b30c502fadfd739cdff04adc2bb499ea8a8aa03c0aa7d7`
- Old web: `da509ed749d6025eec1573295b805c09d87f73896621f6d5920ffe189a57e694`
- Final standard: `b4969441ea1c6336d987f3075bc8057155705efd8c9d7b1fdfb57533e84753dc`
- Final web: `74a322aa002764528e45810322c59f8c5c034f1bda0ea9c93e9e350ea9c7191a`

## Reproduction and root cause

Yes. Severe angle-dependent depth striping was reproduced near yaw 85/90/95 in the preserved superseded v2 viewer. The old GLBs also failed the structural rotation gate with 306 standard / 264 web render-risk coplanar pairs. A correct-depth v3/v4 baseline did not produce a whole-shell alpha jump.

Root cause: Top seam/screw relief was too close to the source-locked top surface; the superseded viewer's approximately 1:2,000,000 near/far ratio amplified depth quantization. The old web export also reduced cylinder radial tessellation, violating exact standard/web visible-geometry parity.

## Repair

- Raised top seam bars and cover screws by a stable 0.25 mm physical offset without changing the device envelope.
- Replaced the pathological viewer depth range with radius-bounded near/far planes and corrected the Babylon bottom-view in-plane orientation.
- Made web radial tessellation identical to standard; web optimization is now texture/encoding-only and the geometry/UV/transform fingerprints match exactly.

## Final gates

- `audit_glb`: standard/web PASS, 0 errors, 0 warnings.
- `audit_views`: PASS, 0 errors; 6 alpha warnings manually resolved because every affected face has 0% core alpha below 250 and 0% transparent core.
- Standard/web geometry, UV and transform fingerprint parity: PASS.
- Static real-browser loads: 40/40 (Three.js + Babylon.js; standard + web; ten prescribed views), all WebGL2, ready, correct hash, zero recorded errors.
- Rotation stress: 96 frames per viewer/model combination (72 yaw at 5-degree increments + 24 pitch/checker frames), four final combinations, 384 final frames. Every automated gate and manual contact-sheet review passed.
- Matched orthographic source/render/overlay/difference rows: 6; authoritative three-quarter supporting overlays: 4; feature inventory rows checked: 33/33.

## Structural results

- standard: duplicate 0; opposite duplicate 0; source-surface coplanar hazards 0; degenerate 0; normal mismatches 0; negative transforms 0; material violations 0; partial-alpha images 0; closed core True; informational opaque solid contacts 132.
- web: duplicate 0; opposite duplicate 0; source-surface coplanar hazards 0; degenerate 0; normal mismatches 0; negative transforms 0; material violations 0; partial-alpha images 0; closed core True; informational opaque solid contacts 132.

## Warnings / residual risk

- Opaque solid/interior coplanar contact counts are retained as informational mechanical intersections; source-surface hazard count is zero in both final GLBs.

Machine-readable evidence: `qa/rotation-stress-report.json`; static loads: `qa/rotation-review/after/static-loads/static-40-loads.json`; matched-camera/feature review: `qa/rotation-review/after/matched-camera/matched-camera-manifest.json`.
