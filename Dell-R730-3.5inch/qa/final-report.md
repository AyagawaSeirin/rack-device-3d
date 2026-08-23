# Dell PowerEdge R730 3.5-inch final report

## Conclusion

**PASS_WITH_BOTTOM_FALLBACK**

The two required custom GLBs are complete and pass structural, dimensional, visible-feature, and dual-viewer WebGL gates. The locked assembly is Dell PowerEdge R730 (E31S/E31S001), 2U, 8 × 3.5-inch LFF in a 2 × 4 layout, all carriers installed, no security bezel, standard seven-slot R730 rear, four-RJ45 NDC, and two matching EPP 750W hot-swap AC PSUs. Real DELL and PowerEdge R730 markings are retained.

The qualified verdict is caused only by the bottom face. An exact underside could not be found after the documented official, marketplace, video, English, and Chinese search, so the bottom is a conservative, opaque galvanized `GENERIC_BOTTOM_FALLBACK` with no invented identifying details.

## Deliverables

| Artifact | Bytes | SHA-256 | Result |
|---|---:|---|---|
| `model/Dell-R730-3.5inch.glb` | 13,053,336 (12.45 MiB) | `09bf01fc36fe5406e04db43be32993a17b4f29fa233da155efa902b15d7cabda` | PASS |
| `model/Dell-R730-3.5inch-web.glb` | 9,027,224 (8.61 MiB) | `8f63924a3fab07f4b143e4a4735b9fe05bfc55cc0433f3110eaa083f66a787fa` | PASS |

Both files are newly built custom GLBs. Neither is an official mesh or a repackaged third-party model.

## Geometry and dimensions

- Final envelope: 482.4 × 87.3 × 741.0 mm (X/Y/Z).
- Body basis: 444 × 87.3 × 684 mm; bezel-absent front projection 18 mm; documented EIA reference to rear-most extent 723 mm.
- Each GLB contains 148 nodes, 148 meshes/primitives, 16 materials, 6 textures, and 6 unique base-color images.
- Both structural audits report zero errors and zero warnings; no mirrored nodes or external resources exist.
- Visible geometry includes separate front ears, eight LFF carrier recess/face/handle/latch assemblies, front control/iDRAC/vent/optical relief, internal fans where exposed, seven rear slot frames, independent I/O groups, rear handle, two complete PSU assemblies, top relief, side lips, and source-aligned right-side mounting studs.

## Six-face lock

| Face | Mode | Final SHA-256 | Result |
|---|---|---|---|
| Front | `SOURCE_LOCKED_GENERATION` | `b2e7383e4ed2c2d2be27a0bcb6fc63c1018c5ca295af73c6a501e252f641cf13` | PASS |
| Rear | `SOURCE_LOCKED_GENERATION` | `edb5ccfe53779711becd5c19bbd3c82be1e42df69733959b03f1eab8772b680c` | PASS |
| Left | `MULTI_REFERENCE_RECONSTRUCTION` | `41e8f6a4cb4f941fca9ff4339cc805fd22f65e93d6fed30aa92299680089f3d6` | PASS |
| Right | `MULTI_REFERENCE_RECONSTRUCTION` | `6f366e0e9ef56d6b36feb23b06d87a249d5023dde497ed7e380b33f00645f447` | PASS |
| Top | `SOURCE_LOCKED_GENERATION` | `2b0f8ead1ff64d6718d47df4b4171a8c6f5b1998e6478e7e772bd37b8627dba3` | PASS |
| Bottom | `GENERIC_BOTTOM_FALLBACK` | `8c513fabb899721f0ecb6b0c46601ed47a2a0b90b655d01dc1301ef510a1fce7` | FALLBACK |

Left and right were generated from independent physical-side evidence and are not mirrored. The view audit reports zero errors. Its five warnings are limited to antialiased exterior silhouette pixels on the non-bottom faces; every face has 0% transparent pixels in the inset chassis core and was visually accepted at original detail.

## Dual-viewer WebGL gate

The final evidence run started after the last GLB rebuild and loaded the models in two independent viewers:

- Three.js: 20 direct loads.
- Babylon.js: 20 direct loads.
- Standard GLB: 20 direct loads.
- Web GLB: 20 direct loads.
- Front, rear, left, right, top, bottom, front-left, front-right, rear-left, and rear-right: 4 loads per view.

Result: **40/40 direct page-state-and-screenshot loads**, all on attempt 1, with `loaded=true`, `error=null`, correct bounds, zero page errors, and zero recovered or inferred events. Browser: Chromium 151.0.7922.34. The final set contains 40 atomic event JSON files, 40 screenshots, 40 reference/render comparison sheets, and four ten-view contact sheets.

The run log also contains 44 `net::ERR_ABORTED` notices for `/qa-log` or superseded GLB requests. Runner order proves these occurred during page close/navigation after `window.__QA.loaded`, bounds capture, and screenshot write. They did not invalidate any event and are therefore non-gating lifecycle noise.

Final visual review covered all four contact sheets plus full-resolution rear/right details. Two viewers and both GLBs agree; the 2 × 4 front carriers, branding, seven rear slots, four RJ45 ports, dual AC inlets, orange PSU latches, EPP 750W fans, and independently reconstructed sides remain visible. The final right-side stud repair removed the prior texture/geometry double image.

## Official 3D status

No exact downloadable official Dell R730 8LFF installed-configuration GLB, glTF, STEP, OBJ, or FBX was found. Dell does publish R730 interactive service 3D Guide pages, but the public viewer route returned HTTP 403 and exposed no download. The unchanged response HTML, response headers, and discovery README are retained under `source/optional-3d/`. These artifacts document the official search; they are not represented as an official model and do not replace the two custom GLBs.

## Evidence and gate files

- `qa/audit.json`: machine-readable final gate record.
- `qa/glb-standard-audit.json`, `qa/glb-web-audit.json`: structural and dimensional audits.
- `qa/views-audit.json`: six-face resolution, ratio, and alpha audit.
- `qa/feature-acceptance.md`: visible-feature-to-geometry acceptance matrix.
- `qa/load-evidence/summary.json`: 40-load aggregate.
- `qa/load-evidence/final-load-events.ndjson`: 40 direct event records with screenshot hashes.
- `qa/renders/final/`: final live WebGL screenshots.
- `qa/comparisons/final/`: final matched reference/render sheets.
- `qa/contact-sheets/`: four final ten-view contact sheets.
- `source/identity-manifest.md`, `source/face-source-lock.csv`, `source/evidence.md`: exact identity, lineage, and source lock.
- `source/bottom-search-log.md`: bottom evidence exhaustion record.

## Remaining risks

1. The underside is a generic evidence-bounded fallback rather than a verified exact underside.
2. Left, right, and some top details are reconstructed from exact photographs and official diagrams, not official CAD.
3. Seller primary photographs contain watermarks; selected generated faces remove seller marks while preserving the server's real configuration and material evidence.
4. This is an exterior website replica, not engineering/internal CAD.
5. No exact official installed-configuration mesh was available for mesh-to-mesh comparison.

This task did not run `git commit` or `git push`.
