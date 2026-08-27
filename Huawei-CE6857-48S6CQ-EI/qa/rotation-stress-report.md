# Final rotation and authenticity review — Huawei-CE6857-48S6CQ-EI

Status: **PASS**

## Frozen identity

Huawei CE6857-48S6CQ-EI, PID 02352CHS, CE6857-EI-F-B0B with 4 FAN-031A-F and 2 x 600 W AC

Exact 48-SFP+/6-QSFP28 front, four blue fan modules, two blue-handled AC PSUs, U-brackets, non-mirrored sides and official stamped underside passed.

## Hashes

- Old standard: `0060e73351e81431a7afc11fb3525ad5e14f035fb9abe63cc370a617be386edf`
- Old web: `e8b4e5d40c743a854c03a4b2f04cec871af1103e331222c088b0270a76788803`
- Final standard: `a84042056c5a897f5f64e0b7c2da769ff444558c2254e5c173587fd9589ffd37`
- Final web: `87f20106ab0370c704cafc9c5eff1c01a953927d0be374b0336f33f471768b4a`

## Reproduction and root cause

No whole-shell alpha jump appeared in the correct v3/v4 visual baseline, but the old asset exported millimetre-valued positions into a metre-based web pipeline and reproducibly failed structural/material gates (670 web render-risk coplanar pairs; non-white BottomZinc baseColorFactor in standard).

Root cause: Millimetre coordinate export damaged cross-viewer depth precision; bottom stamp caps, rear module relief and side details were coplanar/near-coplanar with source-locked faces; the old bottom material violated the required main-face factor.

## Repair

- Exported all glTF positions in metres and recorded metre units while preserving the exact 442 x 43.6 x 457.9 mm installed envelope.
- Rebuilt bottom stamps as uncapped walls with separated photographic caps; separated rear module/handle/ground and side relief from canonical faces.
- Shrank the hidden core, normalized all main face materials to OPAQUE/[1,1,1,1]/single-sided, and retained the exact official PARM6039 GLB unchanged as source-only lineage.

## Final gates

- `audit_glb`: standard/web PASS, 0 errors, 0 warnings.
- `audit_views`: PASS, 0 errors; 6 alpha warnings manually resolved because every affected face has 0% core alpha below 250 and 0% transparent core.
- Standard/web geometry, UV and transform fingerprint parity: PASS.
- Static real-browser loads: 40/40 (Three.js + Babylon.js; standard + web; ten prescribed views), all WebGL2, ready, correct hash, zero recorded errors.
- Rotation stress: 96 frames per viewer/model combination (72 yaw at 5-degree increments + 24 pitch/checker frames), four final combinations, 384 final frames. Every automated gate and manual contact-sheet review passed.
- Matched orthographic source/render/overlay/difference rows: 6; authoritative three-quarter supporting overlays: 4; feature inventory rows checked: 32/32.

## Structural results

- standard: duplicate 0; opposite duplicate 0; source-surface coplanar hazards 0; degenerate 0; normal mismatches 0; negative transforms 0; material violations 0; partial-alpha images 0; closed core True; informational opaque solid contacts 704.
- web: duplicate 0; opposite duplicate 0; source-surface coplanar hazards 0; degenerate 0; normal mismatches 0; negative transforms 0; material violations 0; partial-alpha images 0; closed core True; informational opaque solid contacts 704.

## Warnings / residual risk

- Opaque solid/interior coplanar contact counts are retained as informational mechanical intersections; source-surface hazard count is zero in both final GLBs.

Machine-readable evidence: `qa/rotation-stress-report.json`; static loads: `qa/rotation-review/after/static-loads/static-40-loads.json`; matched-camera/feature review: `qa/rotation-review/after/matched-camera/matched-camera-manifest.json`.
