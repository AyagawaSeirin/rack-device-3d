# Fortinet FortiGate FG-1500D final exact-appearance report

Final status: **PASS_WITH_BOTTOM_FALLBACK**

Completed on 2026-08-23 (Asia/Singapore). Scope is the user-locked Fortinet FortiGate FG-1500D 2U AC delivery appearance: D-generation front, no installed rack brackets, four upper rear fan trays, the requested blank/service-panel arrangement, and two vertical hot-swappable AC PSUs at the rear far right.

## Deliverables

| Artifact | Bytes | SHA-256 | Structural status |
|---|---:|---|---|
| `model/Fortinet-FG1500D.glb` | 12,648,812 | `23db204ad7fe973ddcd007b01e6a05d4d62d2c206ea9f4e3c524b310f51602ee` | PASS |
| `model/Fortinet-FG1500D-web.glb` | 2,132,016 | `2005bc62304731e6eb0c68dadb0ca4b799200a0d1afff0482afe84915d969d03` | PASS |

Both files are self-contained glTF 2.0 GLBs. Each contains 431 nodes, 362 meshes/primitives, 13 materials, six unique embedded face textures, no external buffers, no mirrored nodes, and OPAQUE externally visible materials. The standard and web files retain identical visible geometry and bounds; the web file changes only texture packaging/resolution.

## Identity, configuration, and visible geometry

- Identity manifest: VERIFIED for Fortinet FortiGate FG-1500D, D generation, 2U, complete appliance, dual AC power.
- Official body dimensions: 438 W x 89 H x 554 D mm.
- Actual audited GLB bounds: 438.38 x 89.16 x 555.87 mm, within the documented 2 mm installed-appearance tolerance; non-uniform ratio error is 0.1359%.
- Front identity: factory Fortinet/FortiGate 1500D marking, 16 GE SFP ports (1-16), 16 GE RJ45 ports (17-32), eight 10GE SFP+ ports (33-40), console/USB, two management RJ45 ports, and four status indicators.
- Rear identity: four separately framed fan trays with geometric grilles/handles, one upper blank/service group, four lower segmented panels, and two separately modeled AC PSU modules with IEC recesses and pull handles.
- Side identity: left and right are independent, not mirrored; only the physical-right side carries the regulatory-label block.
- Top identity: factory FORTINET wordmark is readable in the front-oriented direction.
- Rack hardware: no front or rear ears are modeled because the locked user row has no installed brackets and Fortinet documents the brackets as boxed accessories.
- Construction: closed outward shell plus source-aligned face planes, geometric port recess frames, fan rings/spokes/handles, PSU frames/recesses/handles, seams, panels, fasteners, and other parallax-producing relief; not a single decorative box.

## Six independent imagegen faces

Each face has its own built-in imagegen prompt and generated chroma artifact under `qa/imagegen-prompts/` and `qa/imagegen-staging/`. The complete method/output chain is recorded in `qa/imagegen-generation-record.json`.

| Face | Final production mode | Final pixels | Final SHA-256 | Gate |
|---|---|---:|---|---|
| front | MULTI_REFERENCE_RECONSTRUCTION | 2560 x 520 | `3ba334d7223da99588a2457a33c8ae7f11708ac9074d5ced4b077ae33bb80d80` | PASS |
| rear | MULTI_REFERENCE_RECONSTRUCTION | 2560 x 520 | `03f431757fae36dbf4b69e7e2d5be66068bdf098780d54fcd806068b0cbeb2ef` | PASS |
| left | MULTI_REFERENCE_RECONSTRUCTION | 2560 x 411 | `6f9aa424c3d277c65bbaed5ba806d7bd491cbf63e09b4b383a4318a75e49b612` | PASS |
| right | MULTI_REFERENCE_RECONSTRUCTION | 2560 x 411 | `ac2721bb582fc1c729f199f34f298dbe2558eef32a93f9a336d6d7186899ffab` | PASS |
| top | MULTI_REFERENCE_RECONSTRUCTION | 2048 x 2590 | `ad070c9590aa0eb1a10466233f87aa7818e945493a41c942e147fda716d0ed0b` | PASS |
| bottom | GENERIC_BOTTOM_FALLBACK | 2048 x 2590 | `b8d45757255a4f29bd5c049f3a4aaf3da417a1bc0223f022a8f39c18b6b383c0` | PASS_WITH_BOTTOM_FALLBACK |

The final views are tight rectangular equipment faces with alpha 255 over all product pixels. The pre-repair versions with transparent black ports/vents are preserved under `qa/repairs/2026-08-23-alpha-closure/before/`; no RGB feature, branding, count, orientation, or material appearance was changed by the alpha repair. `qa/views-audit.json` reports 0 errors, 0 warnings, PASS.

## Independent actual-GLB WebGL validation

- Three.js 0.185.1: standard and web GLBs, six orthographic plus four oblique views each, 20 successful actual loads.
- Babylon.js 9.22.1: standard and web GLBs, the same ten views each, 20 successful actual loads.
- Total: 40 fresh actual-GLB renders under `qa/renders-final/`; every checksum validates against `qa/final-render-checksums.sha256`.
- Browser-reported engine/model/view state was correct on every load, with 0 console errors. Chromium emitted only non-failing GPU readback performance warnings.
- Four final contact sheets under `qa/comparisons/final-contact-*.png` were inspected at original detail and confirm standard/web silhouette parity, viewer parity, correct left/right orientation, readable branding, four-fan/two-AC rear configuration, and no missing face.
- Existing matched-camera reference/render, source-angle, standard/web, and viewer-parity overlay/difference sheets remain under `qa/comparisons/` and were visually reviewed.

## Structural gates

| Gate | Result |
|---|---|
| `qa/views-audit.json` | PASS, 0 errors, 0 warnings |
| `qa/model-textures-audit.json` | PASS, 0 errors; six expected RGB rectangular-texture warnings only |
| `qa/glb-standard-audit.json` | PASS, 0 errors, 0 warnings |
| `qa/glb-web-audit.json` | PASS, 0 errors, 0 warnings |
| `qa/imagegen-generation-record.json` | PASS |
| `qa/webgl-validation.json` | PASS, 40/40 actual loads |
| Identity/configuration gate | VERIFIED |
| Source-lineage gate | PASS with controlled bottom fallback |
| Feature inventory gate | PASS, 27 rows checked |
| Dimension gate | PASS |
| GLB packaging/material/UV/orientation gate | PASS |

## Official model situation

No exact publicly downloadable Fortinet-official FG-1500D 3D/CAD/GLB/glTF was found in the initial evidence search or the final official-domain recheck. The only preserved optional file is `source/optional-3d/3D-Warehouse-Fortigate-1500D.usdz` (2,610,527 bytes; SHA-256 `e90da2985a23cbbe7e9c79d699a27534e6ad1c813b5232904a32713760d26c69`). It is a non-certified community upload, has incorrect dimensions and unrelated/generic texture content, and was not reused in either delivered GLB.

## Remaining disclosed risks

1. No full exact-model underside image was recoverable after official, PDF, browser-assisted, reseller, marketplace, used-equipment, video, regulatory, and local-language searches. The bottom is therefore the allowed conservative non-identifying fallback: verified 438:554 ratio and ivory sheet-metal edge character only, with no unsupported branding, labels, vents, holes, feet, rails, seams, fasteners, or protrusions.
2. The user-locked row-3 rear conflicts with Fortinet's catalog AC rear, which shows a different PSU/fan arrangement. The delivered model intentionally represents the user's requested row, not the catalog factory rear. This is recorded in the identity manifest, evidence log, model metadata, prompts, and feature inventory.

Because the first risk is the documented bottom-only exception and the second is an explicit user-owned delivery specification rather than an unresolved ambiguity, the final decision is **PASS_WITH_BOTTOM_FALLBACK**, not BLOCKED or REWORK.
