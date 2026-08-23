# Built-in imagegen generation record

All six faces used one or more dedicated built-in imagegen calls. The exact final prompts and binding input roles are in `qa/imagegen-prompts/<face>.md`. No CLI/API fallback was used.

| Face | Mode | Workspace generation lineage | Final canonical output |
|---|---|---|---|
| front | MULTI_REFERENCE_RECONSTRUCTION | `work/front-chroma.png` → alpha-clean lineage | `views/front.png` |
| rear | MULTI_REFERENCE_RECONSTRUCTION | `work/rear-chroma.png` → alpha-clean lineage | `views/rear.png` |
| left | MULTI_REFERENCE_RECONSTRUCTION | `work/left-chroma.png`; targeted aspect corrections `work/left-aspect-chroma.png` and `work/left-aspect-v2-chroma.png` | `views/left.png` |
| right | MULTI_REFERENCE_RECONSTRUCTION | `work/right-chroma.png` → `work/right-alpha.png` | `views/right.png` |
| top | MULTI_REFERENCE_RECONSTRUCTION | `work/top-chroma.png` → `work/top-alpha.png` | `views/top.png` |
| bottom | MULTI_REFERENCE_RECONSTRUCTION from official Dell AR assembly | `work/bottom-chroma.png` → `work/bottom-alpha.png` | `views/bottom.png` |

Every chroma source was converted with the installed imagegen skill's conservative border-connected removal helper, soft matte, despill, and one-pixel edge contraction. Selected pre-normalization RGBA outputs are retained under `qa/pre-dimension-normalization/`.

Primary identity/style sources remain the real exact-device photographs or user configuration lock recorded in `source/face-source-lock.csv`; AI derivatives never outrank those sources. The bottom is not a generic-family fallback: the preserved public Dell R7525 AR GLB is the exact-model geometry authority, with exact left/right photographs constraining material and edge silhouette.
