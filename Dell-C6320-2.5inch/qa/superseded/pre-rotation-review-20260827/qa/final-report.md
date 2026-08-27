# Dell PowerEdge C6300 + 4 × C6320 / 24 SFF final QA report

## Result

**PASS_WITH_BOTTOM_FALLBACK**

All identity-bearing and non-bottom exterior faces are source locked and pass. The bottom is the sole declared `GENERIC_BOTTOM_FALLBACK` because exhaustive official, reseller, auction, teardown, English, Chinese, and Japanese searching found no exact underside image. The fallback is a closed unbranded galvanized sheet with no unsupported holes, vents, feet, rails, labels, seams, fasteners, or protrusions.

## Frozen delivery identity

- Complete Dell PowerEdge C6300 2U host enclosure, regulatory model B08S.
- Four standard two-socket PowerEdge C6320 sleds in a fully populated rear 2 × 2 layout; no C6320p.
- One-row 24 × 2.5-inch SFF front, four groups of six carriers, with the documented non-usable narrow cover before the right control panel.
- Four identical rear node I/O sets: USB 3.0, two 10GbE SFP+, iDRAC RJ45, USB-to-serial, VGA, power/status, vented PCIe carrier/blank, and `POWEREDGE C6320` pull label.
- Two matching shared 1400 W AC hot-plug PSUs with IEC AC inlets, orange releases, and round fan/wire guards. No HVDC, 1600 W, or mixed pair.
- Dell front branding, front-only rack ears and true holes, asymmetric non-mirrored sides, closed top cover, and conservative bottom fallback.
- Binding scale: `482.3 W × 86.8 H × 795.9 D mm`; body width `448.0 mm`.

## Delivered GLBs

| Variant | Bytes | MiB | SHA-256 |
|---|---:|---:|---|
| `models/Dell-PowerEdge-C6300-4xC6320-24SFF-standard.glb` | 16,912,160 | 16.129 | `b95cc6fa82134e65b2608f64b7f56841394ad0e3068a917ce3e50f559a5fffb0` |
| `models/Dell-PowerEdge-C6300-4xC6320-24SFF-web.glb` | 5,985,340 | 5.708 | `5162625966d3de1b8cf3df656b86aab14071de97dd2e98a3d602cf2f1dbbf3d7` |

Both are self-contained GLB 2.0 files. Each has 294 nodes, 51 meshes/primitives, 17 materials, and 8 embedded base-color images. The standard and web geometry signature is identical: `d190433411df6eca37cc8715abee8a50b67e3888a26af82901c0e1364a71ed86`. Web optimization changes texture resolution only.

## Deterministic structural gates

- Six approved views: `PASS`, 0 errors, 0 warnings; all ratios differ from the official physical ratio by at most 0.0234%.
- Standard GLB: `PASS`, 0 errors, 0 warnings; actual bounds exactly `482.3 × 86.8 × 795.9` model units with `units_per_mm_xyz = [1,1,1]` and 0% nonuniform ratio error.
- Web GLB: `PASS`, 0 errors, **1 benign warning**; same exact bounds and 0% nonuniform ratio error. The sole warning is `TRUE_DELL_LOGO_Image` at `512 × 512 px`, below the auditor's recommended 1024px long edge.
- The 512px web logo remains clear at the target website camera distance. The standard GLB retains the same dedicated logo at `1024 × 1024 px`; Dell branding is also preserved in the source-locked front appearance. This optimization warning does not affect identity, geometry, opacity, texture embedding, or the 40 real-load results.
- All materials are opaque; no `BLEND`, no negative/mirrored transforms, no external buffers, no missing normals/UVs, and no other low-resolution texture warnings.
- The six standard GLB face images are exact byte matches for the approved `views/*.png` files.

Feature-count cross-check from the actual GLB:

- 24 SFF carrier bodies.
- 4 C6320 pull tabs and 4 true `POWEREDGE C6320` label planes.
- 8 SFP+ cages, 4 iDRAC RJ45 ports, and 4 VGA ports.
- 2 matching 1400 W AC PSU bodies, 2 IEC inlets, and 2 fan guards.
- 2 large front rack holes plus 8 small ear fasteners.
- 6 major side key slots total; right-only one vertical access slot and two upper recesses.

Machine-readable proof: `qa/delivery-validation.json`, `qa/audit-views.json`, `qa/audit-standard.json`, and `qa/audit-web.json`.

The validation policy explicitly permits only this named web-logo warning and fails if any additional structural warning appears.

## Two-viewer real-load gate

The final files were freshly transferred and parsed 40 times in real WebGL2 contexts:

- Three.js r185: 20 loads.
- Babylon.js 9.22.1: 20 loads.
- Standard GLB: 20 loads.
- Web GLB: 20 loads.
- Each viewer/model pair: six orthographic views plus four three-quarter views.
- 40 unique model URLs, 40 transfers above 1 MB, 40 `PASS` records, and 40 screenshots.

Evidence: `qa/webgl-loads/load-events.json` and `qa/webgl-loads/all-40-contact-sheet.png`.

## Visual comparisons

Six matched-camera reference/render/overlay/difference sheets were created from the actual standard GLB render:

| Face | Mean absolute RGB difference (0–255) |
|---|---:|
| front | 5.230104 |
| rear | 7.487336 |
| left | 2.719267 |
| right | 3.039303 |
| top | 2.391017 |
| bottom fallback | 3.477488 |

`qa/comparisons/authoritative-oblique-review.png` reviews all four actual three-quarter renders against exact-subject real photographs. Left/right were also reviewed together to confirm they are not mirrored. No unresolved non-bottom exterior mismatch remains.

## Official model search

No public exact official Dell model for the complete C6300 enclosure with four C6320 nodes was found. `source/optional-3d/README.md` records the official/CAD/AR/Visio/GLB/STEP search and the negative result. The directory is intentionally empty of 3D files; no seller reconstruction was mislabeled as official.

## Residual risks and disclosure

1. The exact underside is not publicly evidenced; status therefore cannot be plain `PASS` and remains `PASS_WITH_BOTTOM_FALLBACK`.
2. No straight photographic side elevations were found. Both sides are separate multi-reference reconstructions from official Dell service diagrams plus exact front/top/rear material and boundary photographs; the right-only slot/recess pattern is explicitly modeled and the sides are not mirrored.
3. Dell's dynamic manual page returned HTTP 403 in the real browser. The public static Dell PDF and image assets were retrieved and inspected instead; no access control was bypassed.
4. Factory serial/QR content is deliberately omitted rather than fabricated. Verified Dell/PowerEdge product marks are retained.
5. The web variant's dedicated `TRUE_DELL_LOGO_Image` is 512px rather than the audit recommendation of 1024px. It is a disclosed, non-blocking optimization warning: the logo remains clear at the target website distance, while the standard variant retains a 1024px copy.

No git commit or push was made.
