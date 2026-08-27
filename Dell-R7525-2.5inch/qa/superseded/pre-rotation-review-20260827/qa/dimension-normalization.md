# Official-dimension orthographic sampling normalization

The six selected built-in imagegen outputs are preserved unchanged under `qa/pre-dimension-normalization/` and in their `work/*-chroma.png` / `work/*-alpha*.png` lineage.

The final `views/*.png` files are the source-locked generated faces resampled onto the verified Dell physical projection grid used by the GLB:

| Face | Final pixels | Binding physical ratio |
|---|---:|---:|
| front | 4096 × 738 | 482.0 : 86.8 |
| rear | 4096 × 819 | 434.0 : 86.8 |
| left | 4096 × 461 | 772.13 : 86.8 |
| right | 4096 × 461 | 772.13 : 86.8 |
| top | 1727 × 3072 | 434.0 : 772.13 |
| bottom | 1727 × 3072 | 434.0 : 772.13 |

This normalization changes only the orthographic sampling grid. It does not change feature counts, labels, Dell branding, left/right identity, installed configuration, materials, source lineage, or the independently modeled geometry. The GLB already projected the same source-locked textures onto the exact world-space dimensions; the normalization makes the canonical PNGs match that final physical projection.

`qa/views-audit.json` reports `PASS`, zero errors, and maximum aspect-ratio error below 0.15%. Its six warnings are expected anti-aliased external edges / verified opening pixels; all main GLB materials remain `OPAQUE`.
