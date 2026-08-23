# HPE ProLiant DL360 Gen9 4LFF / 3.5-inch — Final QA report

Date: 2026-08-23  
Final status: **PASS_WITH_BOTTOM_FALLBACK**

The self-built standard and web GLBs pass identity, source-lineage, dimensions, structure, opacity, orientation, source-photo comparison, two-viewer WebGL loading, and standard-versus-web exterior-equivalence gates. Ordinary `PASS` is intentionally not claimed because no usable exact-model underside was found after the required search escalation; `bottom.png` uses the skill-defined conservative `GENERIC_BOTTOM_FALLBACK` exception.

## Frozen identity and installed configuration

- Hewlett Packard Enterprise HPE ProLiant DL360 Gen9, 1U, exact 4LFF / 3.5-inch chassis, base chassis SKU 755259-B21.
- Four installed 3.5-inch HPE Smart Carrier-style hot-plug carriers in one row; no security bezel.
- Rear configuration locked to three PCIe positions, installed 4x1GbE FlexibleLOM, two USB 3.0, installed DB9 serial, dedicated iLO 4, four embedded 1GbE RJ45, VGA, and exactly two HPE 500W Flex Slot hot-plug **AC** PSUs.
- Period-correct Intel/HP/HPE/ProLiant DL360 Gen9 factory identity remains visible. The model is not Gen10, not SFF, not the alternate two-port FlexibleLOM rear, and not a one-PSU or alternate-riser hybrid.
- User screenshot row 6 is the installed-configuration authority; official HPE documentation and cross-checked exact-device photographs establish identity, dimensions, component names, construction, and material.

## Final self-built GLBs

| Profile | File | Size | SHA-256 |
|---|---|---:|---|
| standard | `model/HPE-DL360G9-3.5inch.glb` | 17,376,584 bytes (16.57 MiB) | `cdc9a32363bf2cfcdfa3027533c9dbaca4fb897c62d325bdef7affa47bd39b04` |
| web | `model/HPE-DL360G9-3.5inch-web.glb` | 6,402,956 bytes (6.11 MiB) | `b2dbde391730bd77a86813a803f3e68201c532f6ea5664ba2f558e348426531e` |

Both files are self-contained glTF 2.0 GLBs built locally from the source-locked exterior workflow. No official or community mesh was copied or substituted. The two profiles contain the same 86 nodes, 85 meshes/primitives, 13 materials, six unique embedded face textures, orientation, silhouette, and externally visible construction. The web profile reduces texture/curve cost only.

## Dimensions, structure, and visible geometry

- Official 4LFF body ledger: 434.6 × 43.2 × 750.0 mm (W×H×D, bezel-free scope).
- Expected installed envelope: 482.6 × 43.2 × 770.0 mm, including front flange span, carrier relief, and PSU-handle relief.
- Audited actual GLB bounds: 482.600003 × 43.460000 × 770.060003 mm; nonuniform ratio error 0.3978%, inside the documented small-part tolerance.
- Closed outward-facing shell; no negative/mirrored node transforms, missing bounds, external buffers, empty visible interior, rear-ear duplication, or face swap.
- Main surfaces are `OPAQUE`, face materials use neutral factors and `KHR_materials_unlit`, all textured primitives have UVs, and all six embedded images are RGB/opaque.
- Separate visible geometry/relief includes front-only quick-release ears, four recessed/protruding LFF carrier assemblies, three rear PCIe assemblies, two complete PSU blocks and projecting handles, distinct left/right rail hardware, top cover seam/latch/vent relief, and seven separately represented hot-plug fan modules. Fine connector interiors retain exact source-photographic relief instead of synthetic generic port blocks.
- The final export repair removed transparent-RGB black bands and colored edge streaks, then rectified only the top/bottom body rectangles to the verified 434.6:750 ratio. Front ears and rear handles remain independent geometry rather than being baked into the top/bottom card.

## Six-face source lock and image generation

| Face | Production mode | Final PNG SHA-256 | Result |
|---|---|---|---|
| front | SOURCE_LOCKED_GENERATION | `ea30a174d3e9c6afa33502c430b53684d071c8a33205251b4bd6b908fc9563f4` | exact 4LFF four-carrier front, readable factory identity |
| rear | MULTI_REFERENCE_RECONSTRUCTION | `d84dc1687af37204e3af4197d9b17bc82ef66f6dcec656a2f5d40f4c33b22b47` | screenshot/official-layout rear with real-photo material lock |
| left | MULTI_REFERENCE_RECONSTRUCTION | `2a97c3e4383ea470e82251dae81d4187d414eaaa0b692a619add5ca5ccb634a4` | independently solved left, not mirrored |
| right | MULTI_REFERENCE_RECONSTRUCTION | `627fa1659991ee1a2ffe96d2ebfe8972a7d32abd4fcfc6bb4c058b504e257d71` | independently solved PSU-side right, not mirrored |
| top | SOURCE_LOCKED_GENERATION | `78acaffb01306b4965a9963d3a984bb0dfce33cc6d7ecf556b7e5106c447ec4d` | exact cover seam, vents, latch, material |
| bottom | GENERIC_BOTTOM_FALLBACK | `39eda05963c4ddd2ddaf813c7c6aef2ceac0833c00d6c5f91e62951503bcd765` | conservative plain galvanized pan only |

All six final face records identify built-in `image_gen`, a dedicated per-face call, prompt, labeled input roles, selected raw output, raw/final hashes, and post-processing chain. Every primary source hash in `face-source-lock.csv` and every raw/final imagegen hash was rechecked byte-for-byte. Left and right have different real sources, different prompts, different generated files, and different final hashes; neither is mirrored. The bottom does not copy the top and contains no unsupported branding, labels, vents, holes, feet, rails, or mechanical detail.

Automated view audit: `PASS`, zero errors. Its six generic alpha warnings were manually resolved by `qa/alpha-review.json`: every face has 0% alpha below 250 in the core and zero internal fully transparent components; all remaining alpha belongs only to external silhouette/antialias pixels.

## Two independent WebGL viewers

The actual final GLBs were loaded with both independent render paths under WebGL2:

| Viewer | standard | web | Required captures |
|---|---:|---:|---:|
| Three.js | 6 orthographic + 4 oblique | 6 orthographic + 4 oblique | 20 |
| Babylon.js | 6 orthographic + 4 oblique | 6 orthographic + 4 oblique | 20 |

Required actual-load total: **40**. The browser runs returned `qaReady=true`, no load error, WebGL2, and exact model-path binding; every capture is newer than its corresponding final GLB, and `qa/viewer-load-audit.json` reports `PASS`. Supplemental checks add four current dark-background front captures and six current source-camera renders (front-high, rear-high, front-low in both viewers), for **50 total final QA renders**.

Comparison evidence contains:

- 12 canonical source-vs-standard orthographic sheets (six per viewer);
- 20 standard-vs-web sheets (ten per viewer);
- eight real source-camera-vs-standard sheets (four per viewer);
- side-by-side, 50% overlay, and amplified-difference panels for every sheet.

Standard/web average absolute pixel difference is 0.111/255 in Three.js and 0.095/255 in Babylon.js across the ten matched cameras. Manual feature-count review confirms the same exterior configuration, readable front branding, four carriers, exact rear port order, dual 500W AC PSUs, independent side hardware, top construction, and conservative bottom in both viewers.

## Structural gate results

| Gate | Result |
|---|---|
| identity manifest | VERIFIED |
| dimension ledger | VERIFIED |
| visible-feature inventory | VERIFIED |
| face-source-lock hashes | PASS |
| imagegen records/prompts | PASS |
| six-view structural audit | PASS (0 errors; alpha warnings resolved) |
| standard GLB audit | PASS (0 errors, 0 warnings) |
| web GLB audit | PASS (0 errors, 0 warnings) |
| alpha/manual transparency review | PASS |
| two-viewer actual-load audit | PASS |
| source/camera comparisons | PASS_WITH_BOTTOM_FALLBACK |
| standard/web exterior equivalence | PASS |

## Optional official 3D result

No exact public HPE-authored GLB, glTF, STEP, OBJ, FBX, CAD download, AR model, or public viewer asset for the DL360 Gen9 4LFF / SKU 755259-B21 was found after the documented HPE support/PSNow/media, exact-SKU, format, AR, and public-index searches. Therefore `source/optional-3d/` correctly contains only `README.md`; there is no official exact 3D file to preserve. Official HPE 2D component diagrams, the service guide, rendered PDF pages, and API/page evidence are preserved unchanged under `source/` and are not represented as official 3D.

## Remaining risks and scope limits

1. Exact underside evidence is unavailable, so the final status must remain `PASS_WITH_BOTTOM_FALLBACK`. This is the only evidence exception.
2. Published dimensions do not separately enumerate every ear/handle projection; the 482.6 mm flange span and 8/12 mm front/rear relief use locked-source measurement with an explicit ±2 mm tolerance.
3. This is an exact exterior website asset, not manufacturing/internal CAD. Fine connector interiors and tiny flush text rely on high-resolution source-photographic relief; major silhouette/parallax/depth features are geometry.
4. The exact rear layout is locked by the user screenshot and HPE-origin render/diagrams; real exact-chassis photographs with a different FlexibleLOM are used only for material and adjacent construction, never to replace the requested four-port rear.

Two prior repair checkpoints (four GLBs total) remain preserved under `qa/repair-before-front-rear-relief/model/` and `qa/repair-before-opaque-edge-extension/model/`; only the two files in `model/` are deliverables. No Git commit or push was performed.
