# HPE ProLiant DL360 Gen9 8SFF / 2.5-inch final QA report

- Final status: **PASS_WITH_BOTTOM_FALLBACK**
- Finalized: 2026-08-23 (Asia/Singapore)
- Scope: newly constructed website-ready standard/web GLBs; no official or third-party mesh substituted
- Git: no commit and no push

## Frozen delivery identity

- Manufacturer: Hewlett Packard Enterprise; chassis-era factory HP roundel and `ProLiant DL360 Gen9` marking retained
- Product/configuration: HPE ProLiant DL360 Gen9, CTO chassis 755258-B21, 1U, 8 SFF / 2.5-inch
- Front: no security bezel; eight populated Smart Carrier faces in the official 6+2 arrangement; Universal Media Bay with VGA, USB and slim optical drive; HPE Quick Release front ears
- Rear: three PCIe blanks; FlexibleLOM blank; two USB 3.0; DB9 serial; dedicated iLO 4; four embedded 331i RJ45; VGA
- Power: two matched HPE 500W Flex Slot hot-plug **AC** PSUs, each with radial fan, IEC C14 inlet, red release latch and pull handle; no DC PSU and no empty PSU bay
- Dimensions: published body 434.7 W × 43.2 H × 698.5 D mm; nominal front ear span 482.6 mm; modeled front/rear protrusions retained

Identity evidence and inclusion rules are frozen in `source/identity-manifest.md`, `source/dimension-ledger.csv`, `source/feature-inventory.csv` and `source/evidence.md`.

## Six-face source lock

| Face | Production mode | Primary source class | Final SHA-256 | Result |
|---|---|---|---|---|
| front | SOURCE_LOCKED_GENERATION | exact 755258-B21 real photograph | `3c6bdaf703ba1282dc9ba0b3b5353d5d46fd72ac135e29fabb3b36e13b84101a` | 8 SFF 6+2, media bay, control strip and brand marks verified; not mirrored |
| rear | SOURCE_LOCKED_GENERATION | exact dual-500W AC real photograph | `5a1a3d0b0f6c4aba795fd350993b40f88a5b2106e90383d10dd6c00d49bf951d` | blank PCIe/FlexibleLOM, serial/iLO/4×NIC/VGA and two AC PSUs verified; no rear ears |
| left | MULTI_REFERENCE_RECONSTRUCTION | exact-model rear-left/top real photograph | `d0248a8bad2c6c87c0580b30369d0e77d75e74056de9bf230c0fcfbb9f3bc1a7` | independent physical-left hole/slot/perforation order |
| right | MULTI_REFERENCE_RECONSTRUCTION | exact 8-bay front-right/top real photograph | `e3ea5602e1573fe5112218546723b0787ae69b5141f0db285929767509f423f6` | independent physical-right hole/long-slot/perforation order; not a left mirror |
| top | MULTI_REFERENCE_RECONSTRUCTION | exact-model rear/top real photograph | `02882edb2901d7cf6a0ae971396d334651e4e719a89f6f22dd0403e1e665e8ff` | cover, seams, latches, vent groups and rear-right hot-surface label verified |
| bottom | GENERIC_BOTTOM_FALLBACK | official chassis-base diagram plus exact-model material references | `b0fc036809e0f94cbf4a2f3b07cd98a9b7a8ab41f3c8fb169522a1897cee4e2a` | conservative closed galvanized sheet; no unsupported logo, label, vent, hole, foot, rail, seam or protrusion |

The exact underside remained unavailable after documented official, PDF, dynamic-gallery/browser, reseller, marketplace, used-equipment, video and multilingual searches. This is the sole fallback and fixes the final status at `PASS_WITH_BOTTOM_FALLBACK`. Full source paths, URLs, source hashes and locked traits are in `source/face-source-lock.csv`; recovered per-face built-in image-generation method, input roles, prompts, selected raw hashes and post-processing are in `qa/imagegen-prompts/`.

## Final GLBs

| Deliverable | Bytes | MiB | SHA-256 | Nodes / meshes / primitives | Embedded images |
|---|---:|---:|---|---:|---:|
| `model/HPE-DL360G9-2.5inch.glb` | 10,857,148 | 10.354 | `3360da73d2f1471d49960bcb8d260a82801b502129230c1190d582ae6f0c1271` | 416 / 416 / 416 | 8 |
| `model/HPE-DL360G9-2.5inch-web.glb` | 7,037,176 | 6.711 | `31ef838553e8d91759057fe32eb974a4324dc263b4d38bcd7a5375b180f67559` | 360 / 360 / 360 | 8 |

Both are self-contained glTF 2.0 GLBs with no external buffer, no mirrored node, outward closed structural body, 18 materials, OPAQUE face materials, neutral base-color factors, UVs on all textured primitives and `KHR_materials_unlit` on the eight source-appearance materials. Standard and web retain the same visible assemblies and silhouette. The web version reduces repeated vent/relief tessellation and texture resolution only.

Final world bounds for both: **482.6 × 43.5 × 724.2 mm**. The 0.3 mm visual-height increment is the two 0.15 mm source-appearance sheets above the exact 43.2 mm closed structural body. The 0.7 mm depth delta against the 723.5 mm ledger target is within the audited protrusion tolerance. Non-uniform ratio error is 0.4296%; both GLB audits pass with zero errors and zero warnings.

## Visible geometry and viewer acceptance

- Eight independent SFF carriers retain rails, pull handles, release rings, green activity details, red latches and vent relief.
- Universal Media Bay, front status/SID/USB strip and front-only HPE Quick Release ears are separate geometry.
- Rear PCIe blanks, FlexibleLOM blank, USB/DB9/iLO/RJ45/VGA groups and both 500W AC PSU bodies/fans/C14 inlets/latches/handles are separate geometry.
- Top access cover, latches, grouped vent relief and independent non-mirrored side relief are present; bottom receives no unsupported feature geometry.
- A cross-viewer depth-fighting defect found in Babylon.js oblique views was repaired by moving the opaque source-appearance sheets to a 0.15 mm offset, below all modeled feature relief. Final Three.js and Babylon.js oblique renders no longer show white triangles or folded sheets.

Actual GLB live loads:

| Viewer | GLBs | Required views per GLB | Required loaded views | Extra dark-background loads | Result |
|---|---:|---:|---:|---:|---|
| Three.js 0.179.1 | standard + web | 6 orthographic + 4 oblique | 20 | 2 | PASS |
| Babylon.js 8.22.2 | standard + web | 6 orthographic + 4 oblique | 20 | 2 | PASS |

Total required live-loaded acceptance views: **40**. Total retained viewer screenshots including dark-background opacity checks: **44**. Two additional Babylon depth-repair smoke renders are retained but are not counted as required views.

Evidence:

- Four final 10-view sheets: `qa/contact-sheets/`
- 24 orthographic reference/render/overlay/difference sheets: `qa/comparisons/threejs/` and `qa/comparisons/babylonjs/`
- 8 authoritative oblique comparison sheets: `qa/comparisons/perspective-threejs/` and `qa/comparisons/perspective-babylonjs/`
- Actual viewer captures: `qa/viewer-threejs/` and `qa/viewer-babylonjs/`

Feature review confirms correct orientation, readable factory branding, eight-drive 6+2 order, dual-AC PSU state, no false rear ears, independent left/right faces, opaque main surfaces, closed bottom and no standard/web identifying-detail loss.

## Structural gates

- `qa/views-audit.json`: PASS, 0 errors. Six alpha warnings were manually resolved over light/dark checkerboards. Rear core has 0% fully transparent pixels and only anti-aliased edges; physical-right transparency is confined to source-proven real holes. Both GLBs composite all embedded face textures to RGB and use OPAQUE materials.
- `qa/glb-standard-audit.json`: PASS, 0 errors, 0 warnings.
- `qa/glb-web-audit.json`: PASS, 0 errors, 0 warnings.
- All six final PNGs are RGBA, tightly framed and above required long-edge resolution.
- No source download or official document was overwritten.

## Official 3D status and remaining risk

No public exact official HPE GLB, glTF, STEP, IGES, OBJ, FBX, CAD or AR asset for the DL360 Gen9 755258-B21 8SFF installed configuration was found. The negative search result is preserved in `source/optional-3d/README.md`; no Gen10, family-generic or third-party mesh was substituted. If an exact official asset later becomes public, it must be preserved unchanged in `source/optional-3d/` and remain optional rather than replacing these newly constructed GLBs.

Remaining disclosed risks:

1. Exact underside imagery is unavailable, hence the controlled bottom-only fallback.
2. Left/right/top orthographic assets are multi-reference reconstructions from inspected exact-model perspective photographs plus the official assembly diagram, not direct factory elevations.
3. The original conversational image-generation call envelopes were lost during the interrupted predecessor task; selected raw files, distinct hashes, recovered prompt contracts and input roles are preserved locally.
4. Tiny non-identity serial/microtext is intentionally not fabricated. Factory HP/ProLiant identity marks and the 500W PSU state remain visible.

No unresolved non-bottom identity, configuration, geometry, material, orientation, viewer or structural blocker remains.
