# Dell PowerEdge R720 2.5-inch — final report

## Result

**PASS_WITH_BOTTOM_FALLBACK**

The delivered subject is the Dell PowerEdge R720 2U, 16×2.5-inch SFF chassis with the front bezel removed. It retains the factory `DELL` and `PowerEdge R720` marks, one horizontal row of sixteen vertical SFF carriers, the R720 control/media zone, seven blank rear PCIe positions, four RJ45 NDC ports, dedicated management and legacy I/O, the central rear handle, and two matched Dell 750W AC hot-plug power supplies. R720xd, 8-SFF, 24-SFF, LFF, R730-family, DC-PSU and mixed-PSU traits are excluded.

The only qualification is the bottom face: exhaustive official, marketplace, multilingual and 3D/CAD searches did not yield a defensible exact R720 underside view. The fallback is deliberately plain, dimension-anchored galvanized sheet metal with no invented identifying holes, feet, labels or vents.

## Deliverables

| Variant | File | Bytes | SHA-256 |
| --- | --- | ---: | --- |
| Standard | `model/Dell-R720-2.5inch.glb` | 11,721,868 (11.18 MiB) | `9ddcb84c29ef9c30cf1537389b0a6d84136fc72f2639049c17f59d7fbe413650` |
| Web | `model/Dell-R720-2.5inch-web.glb` | 6,032,448 (5.75 MiB) | `e716ea7193259aedf361bdb15afa6a4c0143de181ca792989b38b874b3d35aaf` |

Both are newly constructed GLB 2.0 assets made by `model/build_model.mjs`. Each contains 331 nodes, 331 meshes/primitives, 15 materials and six embedded source-locked face textures. Both use opaque materials for cross-viewer stability, require no external buffers, contain no negative/mirrored node transforms and audit to an exact installed envelope of 482.4 × 87.3 × 723.0 mm.

Visible geometry includes sixteen independent carrier bodies, two front rack ears with four actual open mounting holes, seven individual PCIe blank plates, source-textured I/O recesses, four RJ45 recesses, a protruding central U-handle, two independently removable AC PSU bodies with IEC/fan/latch/handle geometry, and eight independently placed side-hook features.

## Six-face source lock

The canonical transparent PNGs are `views/front.png`, `rear.png`, `left.png`, `right.png`, `top.png` and `bottom.png`. The per-face sources, immutable source hashes, appearance decisions and final paths are recorded in `source/face-source-lock.csv`; every generated-face prompt and correction record is in `qa/imagegen-prompts/`.

Left and right are separately generated physical sides. Left has the front at screen right; right has the front at screen left. Neither was made by mirroring the other. The final left image preserves the selected imagegen pixels and uses only replicated top/bottom edge rows to meet the official complete-silhouette ratio without nonuniform scaling; its ratio error is 0.0715%. All six canonical PNGs pass `qa/views-audit.json` with zero errors.

## GLB and WebGL gates

- `qa/glb-standard-audit.json`: PASS, zero errors, one benign unlit-color warning.
- `qa/glb-web-audit.json`: PASS, zero errors, one benign unlit-color warning.
- Bounds in both independent viewers: `[0.4824, 0.0873, 0.7230]` m; mesh count 331; WebGL2.
- Required actual-load matrix: 40 renders — Three.js r185 and Babylon.js 9.22.1 × standard and web GLBs × six orthographic plus four oblique views.
- Additional comparison loads: six Three.js standard orthographic renders on a solid reference background.
- Total actual GLB render loads: **46**.
- Contact sheets: `qa/comparisons/contact-three-standard.png`, `contact-three-web.png`, `contact-babylon-standard.png`, and `contact-babylon-web.png`.
- Six reference/render/overlay/difference sheets: `qa/comparisons/orthographic-{front,rear,left,right,top,bottom}.png`.

The two viewers load the actual named GLB flavor rather than a proxy scene. Babylon.js is explicitly right-handed so physical left/right orientation matches Three.js and the source-lock landmarks. The complete load record is `qa/viewer-load-report.json`.

## Official 3D search

No exact public official Dell PowerEdge R720 exterior 3D/CAD/AR file was found as of the source-access date 2026-08-23. Therefore there is no official model file to preserve, and no community model was mislabeled or substituted. The search record is `source/optional-3d/README.md`. Both delivered GLBs remain self-made as required.

## Remaining risks

1. The hidden underside remains unverified and is intentionally classified `GENERIC_BOTTOM_FALLBACK`; this is why the result cannot be unconditional PASS.
2. Very small printed labels and connector legends may soften at distant website camera scales, particularly in the web variant, although the major identity and configuration features remain readable.
3. The transparent source PNG audit reports only expected anti-aliased edge/true-aperture warnings. The embedded GLB copies are flattened opaque RGB to avoid cross-viewer sorting artifacts.

No git commit or push was performed.
