# Final report — Cisco N9KC9336

Status: **BLOCKED**

Report date: 2026-08-24 (Asia/Singapore)

## Resolved identity

- Supplied screenshot shorthand: `N9KC9336`
- Canonical chassis PID: `N9K-C9336C-FX2`
- Resolution method: the screenshot's 36-port front layout and rear `PSU + 3 fan trays + management cluster + PSU` layout match Cisco's official N9336C-FX2 figures and hardware guide feature-for-feature
- Official format: 1 RU, not 2 RU
- Front configuration: 36 fixed 40/100-Gigabit QSFP28 ports
- Screenshot rear configuration proven: 2 × AC PSU, 3 × fan trays, port-side-intake airflow (burgundy PI pull tabs)

The earlier 9336PQ identification was wrong and has been rejected. Its derived material was quarantined locally under `qa/rejected/wrong-identity-9336PQ/` and is excluded from the active source locks and committed delivery. The committed rejection record is `qa/rejected/wrong-identity-9336PQ/README.md`; none of the PQ material is eligible for the C9336C-FX2 build. A final filename scan found zero PQ assets in active `source/` or active `qa/` outside `qa/rejected/`.

## Blocking reason

The screenshot-to-official-figure comparison identifies the chassis, but neither the shorthand nor the thumbnail identifies its field-replaceable module BOM. Cisco officially supports three AC port-side-intake PSU PIDs (`NXA-PAC-750W-PI`, `NXA-PAC-1100W-PI2`, `NXA-PAC-1100W-PI3`) and two port-side-intake fan PIDs (`NXA-FAN-65CFM-PI`, `NXA-SFAN-65CFM-PI`).

The supplied rear image is only 210 × 55 pixels at source resolution. It proves AC and PI airflow but does not preserve the module labels needed to select exact PIDs. The 3D skill's assembly-identity gate forbids choosing a common bundle or visually plausible variant.

## Deliverable status

| Deliverable | Result | Size | SHA-256 |
|---|---|---:|---|
| Self-built standard GLB | Not produced — blocked before image generation/modeling | N/A | N/A |
| Self-built web GLB | Not produced — blocked before image generation/modeling | N/A | N/A |
| Exact official 3D backup | Not found after documented search | N/A | N/A |

The official 3D search is recorded in `source/optional-3d/SEARCH-LOG.md`. Cisco's public support/product/document/media surfaces and exact-PID 3D/CAD extension searches yielded no exact downloadable 3D file. A Visio stencil is 2D and was not treated as an official 3D asset.

## WebGL load evidence

- Required upon successful build: 2 GLBs × 2 independent viewers × 10 canonical/oblique views = at least 40 actual loads.
- Actual loads performed: **0**.
- Reason: the skill requires stopping before image generation and modeling when the installed assembly identity is ambiguous. There are no GLBs that could truthfully be loaded or audited.

This is not a failed viewer check and is not a partial `PASS`; it is a deliberate pre-build `BLOCKED` result.

## Evidence retained

- Exact official hardware guide PDF, exact front/rear figures, inspected page renders, user screenshot, and configuration crops are preserved under `source/`.
- Source lineage and uncertainty are recorded in `source/evidence.md`.
- The identity gate is recorded in `source/identity-manifest.md`.
- Face locks and the partial visible-feature inventory are recorded in `source/face-source-lock.csv` and `source/feature-inventory.csv`.
- Machine-readable gate results are in `qa/audit.json`.
- Browser runtime cache and vendored Python runtime dependencies were removed from the delivery tree; they are not evidence or deliverables.

## Required input to resume

Provide one of the following:

1. `show inventory` / BOM output that names the PSU and fan PIDs;
2. a readable rear close-up of the PSU and fan labels; or
3. an explicit choice of one exact PSU PID and one exact fan PID from the supported candidates.

After that identity is frozen, the six independent source-lock/imagegen passes, non-mirrored side construction, physical geometry build, standard/web exports, structural audits, and all 40 or more two-viewer loads can proceed.

## Residual risks

- PSU wattage/generation and fan family remain unknown.
- Left, right, top, and bottom evidence escalation was intentionally not completed after the earlier mandatory identity stop; bottom fallback has not been invoked.
- No exact official 3D file was found, so any resumed build must remain newly constructed from the locked evidence.
