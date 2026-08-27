# Forced review reopened record

Date: 2026-08-24  
Initial decision: **REOPENED / REWORK**

The prior PASS was revoked before relying on it. The forced reverse audit found three source-gate defects:

1. `source/face-source-lock.csv` used custom production-mode strings instead of the skill's exact allowed enumeration: `SOURCE_LOCKED_GENERATION`, `MULTI_REFERENCE_RECONSTRUCTION`, or `GENERIC_BOTTOM_FALLBACK`.
2. The physical-left feature row remained at `medium` confidence despite the main report claiming no unresolved non-bottom evidence gap.
3. The rear source-lock row listed `qgserver-rh2288v3-6.jpg` as supporting evidence even though visual inspection shows a horizontally arranged PSU illustration that conflicts with the official vertically stacked RH2288 V3 rear topology. The final rear texture itself follows the official Huawei diagram and exact ZOL photograph, but the lineage record was not acceptable.

The pre-review report, audit, source locks, feature inventory, identity manifest and evidence file are preserved under `before/`. Validation can return to `PASS_WITH_BOTTOM_FALLBACK` only after the source records are repaired, current GLBs independently pass structure/embedded-texture checks, and the current hashes complete forty real WebGL loads.
