# Final QA — Huawei CloudEngine CE6857-48S6CQ-EI

## Result

**PASS** for the frozen complete appliance configuration:

- exact product: Huawei CloudEngine CE6857-48S6CQ-EI;
- ordering/configuration: `02352CHS / CE6857-EI-F-B0B`;
- airflow: blue `FAN-031A-F / AIR IN` on the power/fan side, port-side exhaust;
- installed rear: four fan modules and two 600 W AC modules, no blanks and no DC substitution;
- port side: 48 empty SFP+ cages and 6 empty QSFP28 cages;
- canonical orientation: port side is project front (`+Z`), `+X` is device right from the port side, `+Y` is up.

No generic-bottom fallback is used. The exact official PARM6039 underside is the binding bottom evidence.

## Final GLBs

| Asset | Bytes | SHA-256 | Structural audit |
|---|---:|---|---|
| `model/Huawei-CE6857-48S6CQ-EI.glb` | 11,287,912 | `0060e73351e81431a7afc11fb3525ad5e14f035fb9abe63cc370a617be386edf` | PASS, 0 errors, 0 warnings |
| `model/Huawei-CE6857-48S6CQ-EI-web.glb` | 1,958,128 | `e8b4e5d40c743a854c03a4b2f04cec871af1103e331222c088b0270a76788803` | PASS, 0 errors, 0 warnings |

Both are self-contained GLB 2.0 files with 399 named visible nodes/meshes, 16 materials, 6 embedded face textures, no mirrored node transforms, no external resources, OPAQUE main materials, explicit UVs on every textured primitive, and matching position/normal/UV/index payloads. Only texture packaging differs between standard and web.

Measured bounds are approximately `442.800 x 43.600 x 458.255 mm`, including the small external fastener/ear relief. Against the `442 x 43.6 x 457.9 mm` ledger envelope, normalized-axis nonuniformity is `0.0947%`; the audit has no dimension error or warning.

## Optional official evidence file

`source/optional-3d/CE6857-48S6CQ-EI-PARM6039-official.glb` remains byte-for-byte unchanged:

- SHA-256: `028500da34c65d5a2004b3b72d8ca2dde733778952c71d4afb028c431fa1992c`;
- status: `OPTIONAL-OFFICIAL` evidence/backup only;
- imported into authored mesh: **no**.

## Six canonical face audit

Aspect ratios use alpha>=8 content bounds. The side views correctly use the total 457.9 mm silhouette including the separate rear U bracket; top/bottom use the 420 mm chassis body depth.

| Face | Physical scope | Ratio error | Opaque-core alpha | Status |
|---|---|---:|---:|---|
| front | 442 / 43.6 | +2.3750% | 0% below alpha 250 | PASS |
| rear | 442 / 43.6 | -1.6137% | 0% below alpha 250 | PASS |
| left | 457.9 / 43.6 | -0.2006% | 0% below alpha 250 | PASS |
| right | 457.9 / 43.6 | +0.1738% | 0% below alpha 250 | PASS |
| top | 442 / 420 | -2.2570% | 0% below alpha 250 | PASS |
| bottom | 442 / 420 | -0.7111% | 0% below alpha 250 | PASS |

The earlier ratio-only imagegen edits for left/right were rejected because their powder coat drifted into an invented curly texture. Final left/right faces keep the prior source-locked photographic material and use a dimension-ledger-driven orthographic projection correction only. Rejected attempts and full input-role records are retained under `qa/imagegen-*`.

## Independent visible geometry

| Required group | Verified authored count |
|---|---:|
| canonical face assemblies | 6 |
| independent SFP+ cages | 48 |
| independent QSFP28 cages | 6 |
| FAN-031A-F module blocks | 4 |
| fan blue-handle nodes | 4 |
| 600 W AC PSU blocks | 2 |
| PSU blue-handle nodes | 2 |
| IEC AC inlet groups | 2 |
| rear U-bracket/ear parts | 8 (4 per physical side) |
| management port nodes | 3 (CONSOLE, ETH, USB) |
| bottom stamped groups | 8 |

The chassis core is closed. The rear U brackets are separate parts extending to the ledger overall depth; there are no invented lateral 482.6 mm front flanges and no copied rear ears. Dense front perforation relief, three SFP bank frames, 48+6 cages, fan/PSU seams, side-specific photographic surfaces, exact bottom stamping, and mounting relief remain externally represented.

## Dual-WebGL render matrix

Each matrix contains front, rear, left, right, top, bottom, front-left, front-right, rear-left, and rear-right at 1600x900:

| Viewer | Standard | Web | Orientation/opacity |
|---|---:|---:|---|
| Three.js | 10/10 | 10/10 | PASS |
| Babylon.js, explicit right-handed scene | 10/10 | 10/10 | PASS |

All 40 final captures reached `window.__READY` with no model-load error. Incidental browser console noise was limited to a favicon 404 and software-WebGL readback warnings. Dark-checker front/rear captures in both viewers show no transparent chassis, gray veil, or background rectangle.

Standard-to-web render mean absolute RGB difference is only `0.095–0.421` in Three.js and `0.061–0.406` in Babylon.js. Cross-viewer mean difference is `0.401–0.960`, attributable to the viewers' neutral lighting/rasterization; orientation, silhouette, opacity, port order, branding, fans, PSUs, and ears agree.

## Official comparison review

Matched 1600x900 reference/render/overlay/difference sheets exist for six official orthographic and four official three-quarter views. Diagnostic mean RGB differences are:

| View | MAE |
|---|---:|
| front | 9.607 |
| rear | 8.428 |
| left | 5.557 |
| right | 3.896 |
| top | 17.909 |
| bottom | 7.043 |
| front-left | 3.277 |
| front-right | 2.061 |
| rear-left | 2.434 |
| rear-right | 2.960 |

The pixel metric is diagnostic, not the pass criterion: the official CAD references and source-locked real-photo textures use different surface/lighting character. Feature review confirms the same 48+6 port arrangement, management group, four blue fans, two AC PSUs, side asymmetry, top red stripe/Huawei mark, bottom stamping, and rear U-bracket silhouette.

## Evidence index

- machine-readable final audit: `qa/audit.json`;
- audit comparison table: `qa/audit-comparison.csv`;
- deliverable hashes: `qa/deliverables-manifest.csv`;
- six-face physical audit: `qa/views-physical-audit.json`;
- GLB audits: `qa/glb-standard-audit.json`, `qa/glb-web-audit.json`;
- geometry inventory: `qa/geometry-manifest.csv`, `qa/build-summary.json`;
- final viewer renders: `qa/renders/`;
- official comparison sheets: `qa/comparisons/`;
- assembly/source locks: `source/identity-manifest.md`, `source/face-source-lock.csv`, `source/feature-inventory.csv`, `source/evidence.md`.
