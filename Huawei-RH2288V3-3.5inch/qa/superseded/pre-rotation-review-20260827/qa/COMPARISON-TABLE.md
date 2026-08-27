# Huawei RH2288 V3 12-LFF source-to-GLB comparison

Final classification: **PASS_WITH_BOTTOM_FALLBACK**

| Gate | Locked target | Actual standard/web GLB evidence | Result |
|---|---|---|---|
| Product identity | Huawei FusionServer RH2288 V3; nameplate H22M-03; 2U; 12 common 3.5-inch LFF | Asset metadata and source manifest retain FusionServer identity; front texture preserves Huawei logo and readable `RH2288 V3` badge | PASS |
| Body and rack span | 447 × 86.1 × 748 mm body; 482.6 mm front mounting span | Both GLBs audit at 482.600 × 86.420 × 756.520 mm overall, with published body held separately and the extra depth limited to front-carrier/rear-cord-loop protrusions | PASS |
| Front | 12 LFF carriers, 3 rows × 4 columns; no bezel; distinct control ears | Twelve independently named source-locked carrier reliefs (`00`–`11`) in the exact 3×4 layout; separate front-only control-ear geometry; no duplicated green strip after final repair | PASS |
| Rear configuration | No rear disks; SM211 2×GE; blank I/O module 2, onboard slots 4/5 and I/O module 1; two USB, Mgmt, VGA, DB9, UID | Seven exact-source rear relief regions plus backing geometry; exactly two SM211 RJ45 nodes; standard management/console nodes; zero rear-drive and zero rear-ear nodes | PASS |
| Power and cooling | Two identical 460 W AC PSUs stacked vertically on one rear side, with fan/cord-loop relief | PSU1/PSU2 nodes, fan rotors/hubs, ejectors and protruding cord-loop geometry are present and appear in both engines | PASS |
| Left/right | Different physical side shells, not mirrored | Independent texture nodes; byte-distinct left/right sources; separate side fastener and rail-lip geometry; no negative/mirrored transforms | PASS |
| Top | Approved top orientation, cover seam/vents/labels and service latch | Top UV orientation matches `views/top.png`; latch uses a source-locked relief region rather than a synthetic overlay | PASS |
| Bottom | Conservative plain galvanized underside only | Opaque 447:748 plate; no copied top, logo, label, vent, foot, rail or unsupported underside detail | PASS_WITH_BOTTOM_FALLBACK |
| Alpha/material | Opaque equipment surfaces; alpha only around elevation silhouettes | View audit has zero errors and no core transparency on five faces (left core transparent 0.00074% edge-level); GLBs embed six RGB textures, all face materials `OPAQUE` + `KHR_materials_unlit` | PASS |
| Standard versus web | Same exterior form; web texture reduction only | 220 nodes/meshes/primitives in each GLB; identical bounds and configuration; maximum 1200×800 screenshot RMSE 0.967004%, below the 1.5% acceptance threshold | PASS |
| Independent viewers | Six orthographic plus four perspective views in two engines for both GLBs | Three.js and Babylon.js each loaded standard and web GLBs for 10 cameras: 40 real-Chromium screenshots, all non-empty and 1200×800 | PASS |

Primary visual evidence:

- Orthographic source/render sheets: `qa/comparisons/<face>-source-vs-three-standard.png`
- Three.js standard/web contact sheets: `qa/comparisons/three-standard-ten-views.png`, `qa/comparisons/three-web-ten-views.png`
- Babylon.js standard/web contact sheets: `qa/comparisons/babylon-standard-ten-views.png`, `qa/comparisons/babylon-web-ten-views.png`
- Combined 40-view sheet: `qa/comparisons/two-engines-two-variants-forty-views.png`

