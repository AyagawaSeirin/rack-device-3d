# Dell PowerEdge R7525 2.5-inch final report

## Result

**PASS**

This is a newly constructed exact-appearance website model for the verified Dell PowerEdge R7525 24 × 2.5-inch SFF assembly. It keeps the real `DELL EMC` / `PowerEdge R7525` branding, installed LCD security bezel, standard no-rear-drive rear, optional DB9 serial connector in Riser 3, and two matching 2400 W mixed-mode PSUs used as AC supplies.

No bottom fallback was used. The bottom is `MULTI_REFERENCE_RECONSTRUCTION` from the exact public Dell R7525 AR assembly plus exact left/right real photographs and Dell dimensions.

## Deliverables

| Deliverable | Bytes | SHA-256 | Audit |
|---|---:|---|---|
| `model/Dell-R7525-2.5inch.glb` | 10,789,788 | `75f798eff49cfe9f110068cd5c2a54d946ae7f78113c837a2012c433d883494d` | PASS |
| `model/Dell-R7525-2.5inch-web.glb` | 6,375,036 | `7f738897782ef91ef890cd91cf22844058902c5d950f7e9fb033077d765a4e21` | PASS |

Both GLBs are self-contained glTF 2.0 files. Each has 318 nodes, 23 meshes/primitives, 17 materials, seven embedded source-locked images/textures, no mirrored node, no external resource, and exact world bounds of 482.0 × 86.8 × 772.13 mm.

## Exact visible construction

- 24 independent portrait SFF carrier bodies, handles, orange releases, and status details.
- separate front control housings / rack-ear blocks, LCD bezel backing, bezel rails, 11 staggered factory-style honeycomb openings, lock, LCD strip, control details, and source-locked Dell EMC badge.
- four rear riser regions / eight PCIe positions, BOSS S2, DB9 serial in Riser 3, OCP/LOM/iDRAC/USB/VGA groups, retention pieces, and dense vent relief.
- two separately modeled 2400 W AC PSU modules with visible fan, fan hub/blades, IEC AC inlet, orange release, and maximum-depth handle geometry.
- closed outward-facing body, separate top latch, non-mirrored side relief, six internal hot-swap fan modules, and conservative official-AR-backed underside relief.

No official mesh was copied into either deliverable.

## Six-face lineage and image generation

- `source/identity-manifest.md`: VERIFIED.
- `source/face-source-lock.csv`: six independent face locks; left/right are distinct and never mirrored.
- `source/feature-inventory.csv`: exact count/order/relief/material build specification.
- `qa/imagegen-prompts/`: one dedicated prompt record per face.
- `qa/imagegen-generation-record.md`: built-in imagegen call/output lineage.
- `views/`: final transparent RGBA canonical faces.
- `qa/views-audit.json`: PASS, zero errors, maximum physical-ratio error below 0.15%.

The six selected imagegen outputs are preserved before dimension normalization. Final `views/` use Dell's verified physical ratios; see `qa/dimension-normalization.md`.

## Two-viewer actual-load gate

`qa/renders/load-evidence.json` contains **40 current-file actual loads**:

- Three.js: standard 10 + web 10.
- Babylon.js (right-handed glTF scene): standard 10 + web 10.
- Per file/viewer: six orthographic views plus front-left, front-right, rear-left, rear-right.

Every row records viewer, file variant, view, rendered PNG path, byte size, and SHA-256. The four contact sheets were inspected at original detail. Both engines agree on front/rear, physical left/right, opacity, branding, top/bottom, and PSU placement.

Comparisons:

- `qa/comparisons/standard-orthographic-contact.png`
- `qa/comparisons/web-orthographic-contact.png`
- `qa/comparisons/authoritative-oblique-sources-vs-renders.png`

## Official model status

Dell's public AR scene remains unchanged under `source/optional-3d/`:

- file: `dell-official-ar-r7525-mySceneClone.glb`
- size: 18,454,132 bytes
- SHA-256: `4d195480b7717b92687b20a9d0e96c1cd733e3cf4e4124fc92bb11fa89dbcbff`
- checksum revalidated: OK
- role: optional backup / exact geometry evidence only
- substitution for the new build: no
- official mesh copied: no

## Residual low risks

1. No direct real underside photograph was found after the documented search. Risk is limited by the exact public Dell R7525 AR assembly, official dimensions, and exact side-edge photographs; therefore this is PASS, not `PASS_WITH_BOTTOM_FALLBACK`.
2. The GLB audit reports one non-blocking warning because the separate Dell EMC badge crop is 900 px on its long edge, below the helper's generic 1024 px recommendation. It is source-locked, embedded uncompressed, and visually readable in both viewers at target distance.
3. Six view-audit warnings are expected antialiased silhouette / verified opening pixels. Main GLB materials are OPAQUE and both viewers show no chassis transparency.
4. Public AR asset redistribution/licensing terms were not independently adjudicated; the official file is retained only as the user-requested source backup and was not incorporated into the new deliverables.

No git commit or push was performed.
