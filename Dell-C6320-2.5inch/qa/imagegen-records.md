# Image generation lineage

All six faces were generated independently with the built-in image generation path, a per-face source lock, and a pure `#FF00FF` chroma background. The real exact-subject photograph or official diagram remained the binding identity/layout/material source; no earlier generated face or neighboring product was used as identity evidence. Full prompts are retained under `qa/imagegen-prompts/`.

| Face | Locked mode | Built-in generation result retained locally | SHA-256 | Correction and acceptance |
|---|---|---|---|---|
| front | `SOURCE_LOCKED_GENERATION` | `qa/intermediate/front-chroma.png` | `5771ff9bb95aaaaebfbf6b693666a25f91b3d00f45a24257fcf5d24d1777184b` | One targeted correction changed only the false second large ear hole. Accepted `front-chroma-corrected.png`, SHA `e21ea267c10413ff64bc29dd3da189d32c78acd1b1c9e1aafb428a524ec373bf`. |
| rear | `SOURCE_LOCKED_GENERATION` | `qa/intermediate/rear-chroma.png` | `bc61c900157bcec52e501bb5da464cf495b86ad3412b201236874e085510ba9a` | One targeted proportion reconstruction preserved two AC PSUs and four C6320 nodes. Accepted `rear-chroma-corrected.png`, SHA `9fbcbc53c78341203ae6e60210e77dabac609f840851b4673c1df2a1f8f98ad1`. |
| left | `MULTI_REFERENCE_RECONSTRUCTION` | `qa/intermediate/left-chroma.png` | `e092a7ad34508d08501223f3d8fca5b70ed961dcb2b5a9d713086336001977fe` | One proportion reconstruction retained the distinct left pattern and omitted right-only features. Accepted `left-chroma-corrected.png`, SHA `5be469d0ebaf7a4f5de7190b1d33e52e7c9bd62b3535c293bfa0f57f6025b73a`. |
| right | `MULTI_REFERENCE_RECONSTRUCTION` | `qa/intermediate/right-chroma.png` | `70f15094703e20f021e564b84684f9c91890eb30163f58d817f92bd90645c064` | One proportion reconstruction retained the right-only vertical slot and two upper recesses. Accepted `right-chroma-corrected.png`, SHA `b66534873fe8478286ca92cd9d8be4948105d9f9cb79181225d21cb937ee74ce`. |
| top | `MULTI_REFERENCE_RECONSTRUCTION` | `qa/intermediate/top-chroma-initial.png` | `6a457f4ec7803f4c56978b7a2a2a0666e6042c98d309a1c5ac522e56b0ab705a` | One targeted physical correction removed front/rear faces incorrectly rotated upward. Accepted `top-chroma.png`, SHA `856c18e43262383ad7d71efe5e8418c7b490d38dde664912ddc45aa7ad102cf6`; exact real-photo factory label blocks were subsequently composited without pseudo text. |
| bottom | `GENERIC_BOTTOM_FALLBACK` | `qa/intermediate/bottom-chroma.png` | `0dd430f52d3591f72890ccea71495a95bb4190951b801824b2d4dd94f5533ae8` | One conservative proportion reconstruction; no detail was added. Accepted `bottom-chroma-corrected.png`, SHA `7296441ba1c8da17a52307c84cd8d95296756c11d803b7d09a6d26f6d1526563`. |

## Background removal and physical-ratio projection

The imagegen chroma helper produced inspected alpha isolations. The accepted alpha files are:

- front `a487c2bd55a7090451c700930b6b28894acc5166ebf93c85d0e937e28e45af8a`
- rear `aba6865d91a5b483530b9fcdb82932616f98d27a58c84cdbcdbcfff19b2123b5`
- left `639dfba108b5ed5c8b7ffd90bf0fb677f4f7731cb8198d1e767f57724b696839`
- right `f6a569c209986dea461c73f0b317df1b0b46e1eb3d3282d1981e585fba065189`
- top `5a2502af81699df8963a84ec0598f4decb1b73c091ee064ca4d10b0b3f8ba07d`
- bottom `242b89a3ef1ef382f167009705e3bb6d7628c30abc417a1de7c7598f6091d3cf`

`qa/normalize_views.py` fits source pixels uniformly into official-dimension canvases and continues only non-identifying steel surface where necessary. It never anisotropically stretches ports, fans, holes, labels, or other identity-bearing pixels. The six final `views/*.png` files pass `audit_views.py` with zero errors and zero warnings.

## Built-in output provenance

The original built-in outputs remain under `/root/.codex/generated_images/01a02f37-c63b-7a33-973c-938731e6b33d/`. Their selected UUID filenames and byte hashes are recoverable one-to-one from the local copies above. No output was moved or deleted from that managed directory.
