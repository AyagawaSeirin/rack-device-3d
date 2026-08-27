# Dell PowerEdge R240 3.5-inch/LFF final report

Status: **PASS_WITH_BOTTOM_FALLBACK**

## Deliverables

| File | Bytes | SHA-256 |
|---|---:|---|
| `model/Dell-R240-3.5inch.glb` | 12,842,888 | `ec58f70b517cc465ae4f6ca5b344acfc008880bd35736928b8c325b0c40de5b4` |
| `model/Dell-R240-3.5inch-web.glb` | 4,656,604 | `820443089544918595ab062b7bca93d895084a000dc58c35bc282a251d9782a9` |

The model is the verified 4 × 3.5-inch hot-swap/LFF, bezel-absent R240 with standard rear, two PCIe blanking plates, four cabled fans and exactly one installed fixed/cabled AC PSU. Dell EMC / PowerEdge R240 product marking is retained. A second PSU is intentionally absent because the R240 is officially non-redundant; dual-PSU geometry belongs to another chassis family.

## Final gates

- Six independent face-source locks: PASS; physical left/right are not mirrored.
- Canonical PNG audit: PASS, 0 errors.
- Standard GLB audit: PASS, 0 errors, 0 warnings.
- Web GLB audit: PASS, 0 errors, 0 warnings.
- Feature-count audit: PASS.
- World bounds: exactly 482.0 × 42.8 × 573.596 mm.
- Independent final WebGL loads: 40 accepted post-repair loads — Three.js 20 and Babylon.js 20; each GLB received six orthographic and four three-quarter views in each engine; 40/40 parsed and rendered with HTTP 200 and zero browser errors.
- Comparison sheets: 32 across four viewer/model pairs, covering all six orthographic views plus two authoritative exact-unit three-quarter sources.
- Official exact public 3D: not found; reproducible log saved under `source/optional-3d/`; no official file was available to preserve.
- Bottom: conservative `GENERIC_BOTTOM_FALLBACK`, with unsupported underside details excluded.

Detailed evidence and residual-risk analysis are in `qa/qa-report.md`. No git commit or push was performed.
