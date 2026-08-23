# Huawei CE6851-HI-B-B0A final QA

Date: 2026-08-23 (Asia/Singapore)

Final status: **PASS**

## Locked identity

- Manufacturer: Huawei Technologies Co., Ltd.
- Product: CE6851-48S6Q-HI
- Ordering part number: 02350JAS
- Part model: CE6851-HI-B-B0A
- Delivery subject: complete fixed 1U switch appliance
- Port side: 48 x 10GE SFP+ plus 6 x 40GE QSFP+
- Power side: 2 x PAC-600WA-B AC PSU, 2 x FAN-40EA-B fan module, central CONSOLE/ETH/USB/pull-tab area
- Airflow: port-side intake, power-side exhaust
- Published body dimensions: 442.0 W x 420.0 D x 43.6 H mm
- Canonical coordinates: +X physical device right from the port side, +Y up, +Z port side/front

The exact installation is verified by Huawei official imagery/documents and the exact-B REVO photo set. All six faces use `SOURCE_LOCKED_GENERATION`; an exact underside photo exists, so no generic-bottom fallback applies.

## Delivered GLBs

| File | Bytes | SHA-256 | Result |
|---|---:|---|---|
| `model/Huawei-CE6851.glb` | 16,579,548 | `8fb2e08ad9937d8d8bbdb524f6a83ca6c1d2882c19299289b9e28282e556531f` | PASS |
| `model/Huawei-CE6851-web.glb` | 10,129,052 | `f3ab68606febe15ed6be49147e58590f58f7537bfcb012629a261ec3e63519a8` | PASS |

Both are self-contained glTF 2.0 binaries. Each contains 49 nodes, 49 meshes/primitives, 12 materials, 6 textures, and 6 embedded images. The standard and web files have byte-identical exterior vertex/face geometry; the web variant reduces texture resolution only.

The audited overall bounds are 482.6 x 45.65 x 427.0 mm. Width includes the two separate 19-inch rack brackets. The 2.05 mm height and 7.0 mm depth additions over Huawei's body dimensions are the explicitly modeled exterior ribs, fasteners, handles, module and bracket projections; they remain within the recorded audit tolerance.

## Structural acceptance

| Gate | Actual | Result |
|---|---:|---|
| Closed chassis shell | watertight, positive volume | PASS |
| Source-locked exterior faces | 6 | PASS |
| SFP+ cages | 48 connected geometry components | PASS |
| QSFP+ cages | 6 connected geometry components | PASS |
| Business ports | 54 total | PASS |
| AC PSUs | 2 x PAC-600WA-B | PASS |
| Fan modules | 2 x FAN-40EA-B | PASS |
| Rack brackets | 2 separate watertight meshes | PASS |
| True bracket holes | 2 per bracket; Euler number -2 each | PASS |
| False rear rack brackets | 0 | PASS |
| Mirrored/negative transforms | 0 | PASS |
| External buffers/resources | 0 | PASS |

The physical right side retains the ground stud and yellow earth mark; the physical left side does not. The top retains the cover/vent/seam structure. The exact bottom retains photographed labels and stampings, with five modeled longitudinal ribs, one transverse rib and visible fastener relief. Flush fasteners that do not need parallax remain in the locked texture.

## Texture, material and alpha acceptance

- Six approved source-locked images are embedded independently; none is swapped, mirrored or rotated.
- Genuine HUAWEI/model and PAC-600WA-B/FAN-40EA-B markings remain visible.
- Standard embedded long edges are 3072 px for the four narrow faces and 2048 px for top/bottom.
- Web embedded long edges are 2048 px for the four narrow faces and 1536 px for top/bottom.
- Every main face material is `OPAQUE`, single-sided and `KHR_materials_unlit`; embedded face images are RGB with no accidental transparent chassis pixels.
- The separate chassis/mechanical materials are opaque PBR materials.
- View-asset audit status is PASS. Its six warnings are the expected anti-aliased transparent silhouette/true-hole pixels; every inset chassis core has 0.0% fully transparent pixels.

## Independent WebGL validation

Final GLBs were rendered in two independent WebGL2 paths:

- Three.js r180
- Babylon.js 9.22.0, explicitly using the right-handed glTF coordinate convention

For each engine and each GLB, six orthographic views and four oblique views were captured. The standard file also has left/right rack-ear, front logo, rear management and light/dark checkerboard captures. Total final screenshots: 52 at 1280 x 720.

Browser console error count is zero. GPU `ReadPixels` messages are screenshot-readback performance notices, not model or material failures.

Both viewers agree on orientation. As an automated asymmetric landmark check, yellow ground-mark pixels are `left=0, right=684` in Three.js and `left=0, right=688` in Babylon.js.

The maximum standard-versus-web normalized RMSE across ten views in either engine is 0.012141. This is consistent with texture downsampling; silhouette, orientation, component counts and visible relief are unchanged. Full figures are in `qa/render-comparison-table.csv`.

## Source/render comparison

Twelve matched-canvas comparison sheets were produced using the approved six views:

- six standard-GLB sheets from Three.js;
- six web-GLB sheets from Babylon.js;
- every sheet contains reference, actual render, 50% overlay and absolute difference panels.

Feature-by-feature review passes for the 48+6 port layout, dual-AC/dual-fan rear, management region, non-mirrored left/right landmarks, full top cover/vent, and exact photographic bottom with label/rib structure. Numeric image difference is retained as a diagnostic only; acceptance is based on identity-bearing feature correspondence.

## Repairs completed during final closure

1. Babylon.js was switched to a right-handed scene so physical left/right labels match the authored glTF convention.
2. Top/bottom orthographic cameras were widened so the full 420 mm depth and exterior projections remain inside the 1280 x 720 frame.
3. The bottom face winding/UV order was corrected from inward `+Y` to outward `-Y`, restoring the exact photographed bottom texture in single-sided rendering.
4. Babylon's default loading screen was disabled so no loader overlay contaminates QA captures.

The pre-bottom-normal-fix GLBs are retained under `model/archive/pre-bottom-normal-fix/`. They are historical repair inputs, not deliverables.

## Official 3D search

No exact public Huawei 3D asset was found. Huawei's exact preview metadata returned no 3D URL, and exact-PID searches for common CAD/3D formats found photographs/Visio material only. No official file was discarded or replaced; `source/official-3d-search.md` records the result.

## Acceptance conclusion

Both final GLBs pass structural audit, exact-feature review, source comparison, two-viewer orientation/opacity review, checkerboard alpha review and standard/web equivalence review. There is no unresolved error and no bottom fallback. Final classification: **PASS**.
