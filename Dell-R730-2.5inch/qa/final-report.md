# Dell PowerEdge R730 16-SFF 3D asset — final report

> Superseded for current acceptance by `qa/rotation-review-20260827/final-report.md` and its frozen-hash `final-gate.json`. This older report is retained for lineage.

## Release decision

**PASS_WITH_BOTTOM_FALLBACK**

The self-authored standard and web GLBs pass all 18 consolidated release gates. The only exception is the documented, permitted generic-bottom fallback: an exact public underside photograph could not be found after the recorded official, third-party and local-language search.

## Locked identity and installed configuration

- Manufacturer/model: Dell PowerEdge R730, regulatory model/type E31S/E31S001.
- Chassis: complete 2U appliance, 16 x 2.5-inch SFF front backplane, slots 0–15 populated with Dell carriers, front bezel absent.
- Rear: seven vented blank PCIe positions (1–7), dedicated iDRAC, DB9 serial, DB15 VGA, two USB, four-port 1GbE NDC and upper-right grille.
- Power: two installed hot-plug Dell EPP 750W **AC** PSUs with IEC C14 inlets, fan faces and pull handles. No DC, single-PSU or 1100W substitution.
- Branding: visible factory DELL, PowerEdge R730, Intel and EPP 750W markings are retained as appearance evidence. No Dell EMC substitution was introduced.
- Excluded: R730xd, rear flex drives, 8-SFF, LFF/3.5-inch, front bezel, fitted rear add-in cards and rails.

## Final GLBs

| Variant | File | Size | SHA-256 |
|---|---|---:|---|
| Standard, PNG textures | `model/Dell-R730-2.5inch.glb` | 13,671,616 bytes (13.038 MiB) | `9c74ffddbb943bbfab7fe47955d2035c8869e4fa9e66eedf0304da6b30059e08` |
| Web, JPEG-optimized textures | `model/Dell-R730-2.5inch-web.glb` | 1,855,664 bytes (1.770 MiB) | `a86fe63f2e27d1f0cd251e5a69c94f71057ff5733f267e22cbed4bc49de8288e` |

Both files are self-authored from the locked evidence set. Neither is replaced by an official or third-party model.

## Structural and dimensional gates

- Both GLBs: `PASS`, 0 errors, 0 warnings.
- Each GLB: 1 scene, 362 nodes, 362 meshes, 362 primitives, 14 materials, 6 textures and 6 unique base-color images.
- No mirrored nodes; left and right use independent source-locked faces.
- Actual bounds: 482.4 x 87.54 x 741.15 mm.
- Official/derived target: 482.4 x 87.3 x 741.0 mm; the final model is within the evidence ledger tolerances.
- Visible geometry checks passed for the closed chassis, two rack-ear depth planes, 16 separate drive carriers, 32 drive LEDs, seven rear blank covers, four NDC RJ45 ports, two distinct EPP 750W AC PSUs and two PSU fan assemblies.

## Six-face lineage

- Six face-lock rows, six independent final imagegen prompts, six independent final generation outputs and six distinct final PNG hashes are present.
- Front, rear and left are source-locked photographic generations.
- Right and top are explicitly documented multi-reference reconstructions and are not mirrored from the opposite side.
- Bottom is explicitly tagged `GENERIC_BOTTOM_FALLBACK`; it is a conservative galvanized sheet with no invented logo, label, vent, foot, rail, hole, seam, port or fastener detail.
- `qa/views-audit.json` passes with 0 errors. Its six warnings are limited to expected antialiased edge pixels, not background contamination or core transparency.

## Actual WebGL load evidence

Required model-view count: **40**, all complete at 1280 x 720.

- Viewer A: Three.js 0.170.0 + GLTFLoader; standard and web GLBs each loaded in six orthogonal and four oblique cameras = 20 model screenshots.
- Viewer B: model-viewer 4.0.0 + Three.js 0.169.0; the same two GLBs and ten cameras = 20 model screenshots.
- Both release browser runs recorded 0 console errors.
- Four additional light/dark checkerboard screenshots validate silhouette/edge behavior in both viewers.
- Two additional perspective source-angle screenshots support the authoritative front-top and rear-top comparisons.
- Total actual-GLB screenshots: **46** (40 required model views + 4 checker views + 2 authoritative-angle views).

Comparison evidence includes six orthographic sheets, two authoritative source-angle sheets, ten standard-versus-web sheets and eight contact sheets, for 26 comparison PNGs. The 50-row feature inventory review passes in all four viewer/model combinations.

## Official 3D result

Dell exposes exact-model interactive R730 service 3D guides, including PSU, riser, cover, fan, control-panel and backplane procedures. No public exact raw GLB, glTF, STEP/STP, OBJ or FBX download was found. Browser and direct HTTP inspection of the official viewer were blocked by Dell/Akamai HTTP 403 in this environment.

The untouched response, headers and discovery conclusion are preserved under `source/optional-3d/`. They are evidence of the official interactive path, not a downloadable model. Consequently there is no official raw model to archive; the two required self-authored GLBs remain the deliverables.

## Remaining risks

1. The underside remains the controlled generic-bottom fallback because exact R730 underside photography was not found.
2. Right and top are evidence-constrained multi-reference reconstructions, not single exact orthographic factory photographs.
3. Very small regulatory/service-label glyphs are photographic texture detail and may not remain readable at extreme zoom.
4. The web GLB uses visually reviewed JPEG compression; the standard GLB retains PNG textures for higher fidelity.

## Gate artifacts

- Consolidated audit: `qa/audit.json`
- Feature-by-feature review: `qa/feature-review.csv`
- Standard structural audit: `qa/glb-standard-audit.json`
- Web structural audit: `qa/glb-web-audit.json`
- Six-face audit: `qa/views-audit.json`
- Viewer packages: `webgl/viewer-a/` and `webgl/viewer-b/`
- Final render evidence: `qa/renders/`
- Comparison evidence: `qa/comparisons/`

No git commit or push was performed.
