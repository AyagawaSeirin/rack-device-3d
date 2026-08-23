# Dell PowerEdge R7525 3.5-inch final report

Final status: **PASS_WITH_BOTTOM_FALLBACK**

## Frozen delivery identity

- Dell PowerEdge R7525, regulatory model E68S / type E68S001, complete 2U appliance.
- Front: 12 × 3.5-inch/LFF hot-swap layout, four columns × three rows, Dell EMC LCD/security bezel installed, factory `DELL EMC` marking retained.
- Rear: no rear-drive module; four riser groups/eight PCIe positions; BOSS S2 area; OCP 3.0, embedded NIC, iDRAC, USB and VGA groups; optional DB9 serial card absent.
- Power: two matching hot-plug 2400 W **AC** PSUs, redundant 1+1, with visible fans, `2400W` markings, IEC C20 inlets and orange release hardware. No DC geometry is present.
- Dimensions: 482.0 × 86.8 × 772.13 mm overall installed envelope; body width 434.0 mm.

The authoritative identity, dimension, evidence and feature records are `source/identity-manifest.md`, `source/dimension-ledger.csv`, `source/evidence.md`, `source/face-source-lock.csv` and `source/feature-inventory.csv`.

## Final GLBs

| Deliverable | Bytes | Approx. MiB | SHA-256 |
|---|---:|---:|---|
| `model/Dell-R7525-3.5inch.glb` | 11,067,812 | 10.55 | `90ec6e7a3601ae8166132f35ae3e9e8a62e646d349a548e419658b848a62ffc0` |
| `model/Dell-R7525-3.5inch-web.glb` | 5,523,780 | 5.27 | `e8655c521bfd599aa073756107ee5c1046c4efbe5631d8f16f3673832665aa05` |

Both are independently constructed deliverables, not Dell CAD. They share the same exterior geometry and configuration. The web GLB uses reduced face texture resolution while retaining the same identifying details. Each contains one scene, 77 nodes, 16 meshes/primitives, 18 materials and eight embedded images. There are no external buffers, negative/mirrored nodes or non-opaque visible materials.

The earlier GLBs were preserved unchanged under `qa/repairs/pre-fidelity-overlay-fix/`. The final repair removed coarse duplicated surface overlays that obscured the source-locked front/rear/top appearance, while retaining closed chassis geometry, front projection/backing, twelve separate carrier assemblies, separate PSU bodies and projections, asymmetric side relief and hidden internal fan assemblies. Exact rear PSU source crops are projected onto the two physical PSU bodies so their AC identity remains photographic while their depth is real geometry.

## Six-face lineage and image generation

- Front, rear, left, right and top are `MULTI_REFERENCE_RECONSTRUCTION` from exact-configuration real photos/video frames, official rendered manual pages and the user row-8 lock.
- Left and right are independent and non-mirrored. Their source hashes and asymmetric locked traits remain in `source/face-source-lock.csv`.
- Bottom is the sole `GENERIC_BOTTOM_FALLBACK`; the completed search is documented in `source/bottom-search-log.md`. It is a conservative closed galvanized sheet with no logo, label, vent, hole, foot, rail or invented mechanism, and it does not copy the top.
- The originating task became `notLoaded`, so its exact verbatim image-generation tool payload could not be retrieved. The preserved chroma → alpha → trim artifact chain remains in `qa/imagegen-selected/`; reconstructed acceptance prompts, inputs, modes and final hashes are explicitly labeled in `qa/imagegen-prompts/`. No face was regenerated during the final takeover.

## Automated gates

- `qa/views-audit.json`: PASS, zero errors. Five warnings are confined to anti-aliased exterior edges and verified side rail/keyhole openings in canonical transparent PNGs. Core chassis pixels are opaque; the embedded GLB face/PSU crops report zero transparent and zero semi-transparent pixels.
- `qa/glb-audit-standard.json`: PASS, zero errors, zero warnings.
- `qa/glb-audit-web.json`: PASS, zero errors, zero warnings.
- Both GLBs resolve to the exact 0.482 × 0.0868 × 0.77213 m bounds.

## Actual WebGL gates

`qa/webgl-evidence-final-v2/load-evidence.json` records **40/40** actual loads:

- Three.js 0.170.0 × standard: 10/10.
- Three.js 0.170.0 × web: 10/10.
- Babylon.js 7.44.0 × standard: 10/10.
- Babylon.js 7.44.0 × web: 10/10.

Each pair contains front, rear, left, right, top, bottom, front-left, front-right, rear-left and rear-right. The two viewers agree on file identity, physical orientation and bounds, with only normal JavaScript floating-point representation differences. Twenty-six screenshots were saved after `window.__VIEWER_READY__` during a batch whose pair-level return later timed out; those records are transparently marked as reconstructed from the already-saved ready-state screenshots. The remaining fourteen retain direct per-view navigation/load/screenshot logs. Every screenshot has a SHA-256 record.

Visual evidence:

- Four viewer/model contact sheets and combined sheet: `qa/webgl-evidence-final-v2/*/contact.png`, `qa/webgl-evidence-final-v2/all-viewers-contact.png`.
- Light/dark checkerboard alpha pass: `qa/webgl-evidence-final-v2/alpha-check/contact.png`.
- Six orthographic reference/render/overlay/difference sheets plus two authoritative front three-quarter comparisons: `qa/comparisons/`.
- Rack-ear, factory brand, dual AC PSU and rear-port close-ups: `qa/closeups/contact.png`.

Feature review confirms normal readable branding, 12 LFF carriers behind the bezel, non-mirrored sides, no false rear ears, eight PCIe positions, no rear-drive module, exact rear port order, two AC PSUs, one top latch, conservative non-identifying bottom, and no gray veil, transparent chassis, face swap or exposed interior.

## Optional official 3D

Dell publishes an exact-product interactive 3D service experience, recorded in `source/optional-3d/README.md`, but the public viewer returned Akamai HTTP 403 and exposed no public direct GLB, glTF, OBJ, FBX, STEP, IGES or USDZ download. No official binary was therefore available to preserve. The official viewer links and access outcome are retained; no access control was bypassed and no official model substituted for the two custom GLBs.

## Remaining risks

1. Exact underside imagery remains unavailable, so the disclosed bottom-only fallback prevents an ordinary PASS classification.
2. No exact public rear three-quarter photograph for the locked no-rear-drive configuration was found; rear slants are constrained by the official straight Figure 9, dimensions, side evidence and separately projected exact PSU surfaces.
3. Original verbatim image-generation prompts are unavailable because the source task became `notLoaded`; reconstructed prompt records are clearly identified rather than represented as recovered logs.

No Git commit or push was performed.
