# Dell PowerEdge R620 10×2.5 SFF visible-feature acceptance

Final review date: 2026-08-24 (Asia/Singapore).

| Gate | Locked requirement | GLB evidence | Visual evidence | Result |
|---|---|---|---|---|
| Exact identity | Dell PowerEdge R620 10-drive chassis; not 8SFF, R620xd, R720, or 2U | Asset metadata and `Closed_Chassis_Core`; exact variant field | User row-4 crops, official technical guide p11/p51 | PASS |
| Front drive layout | 10 installed 2.5-inch SFF carriers, 2 rows × 5 columns | Ten `Front_SFF_Drive_*_Handle_Top` assemblies, ten recesses, per-carrier relief | `views/front.png`; both viewer front renders | PASS |
| Front control and branding | Narrow device-left control strip; DELL and PowerEdge R620 marks; mini-USB and indicators | Separate control frame, power button, mini-USB recess, three lenses; photographic face retains marks | Exact IT Creations/Cloud Ninjas sources and user crop | PASS |
| Bezel/front exclusions | No bezel, optical drive, LCD strip, front VGA, dual full-size USB, or vFlash | No nodes for excluded 8-drive hardware | Front render and source lock | PASS |
| Rack latches | Two front-only latch/ear assemblies; no invented rear ears | Two `Front_Rack_Latch_*_Body` nodes; metadata `rear_rack_ears: 0` | Six orthographic and four oblique views | PASS |
| PCIe area | Three low-profile ventilated slot blanks | Three `Rear_LowProfile_PCIe_Blank_*_Top` assemblies | Official manual and exact rear source | PASS |
| Rear I/O | iDRAC7 RJ45, DB9, VGA, 2 USB 2.0, four Base-T RJ45 | Independent port frames and cavities; metadata exact counts | Rear reference/render comparison | PASS |
| Network exclusion | No SFP/SFP+ cage in target configuration | Metadata `network_adapter_SFP: 0`; no SFP nodes | Exact I350 rear source | PASS |
| Unified AC power | Two matching Dell 750W hot-plug AC PSUs with IEC C14, fan, orange latch, and handle | Two PSU frames, two IEC cavities, two fan assemblies, two release/handle groups | Exact PC Server & Parts rear and both viewer rear renders | PASS |
| Power exclusions | No DC terminal block; no single-PSU or PSU blank configuration | Metadata `DC_PSU: 0`, `AC_PSU_750W: 2` | Rear render | PASS |
| Physical left | Independent -X source; front at canonical image-right; asymmetric studs/slots/seam | Five left studs, four left slots, independent texture | `views/left.png` and four left loads | PASS |
| Physical right | Independent +X source; front at canonical image-left; not mirrored | Five right studs, four right slots, independent texture | `views/right.png` and four right loads | PASS |
| Top | Closed galvanized cover, latch, labels, front and rear vent relief | Top texture plus latch, seams, 3×40 front vents and asymmetric rear vents | Top comparisons and oblique renders | PASS |
| Bottom | Conservative unbranded galvanized underside only | Independent bottom face; no unsupported feet, rails, labels, logos, or holes | `views/bottom.png`; documented exhaustive search | FALLBACK |
| Installed envelope | 482.4 × 42.8 × 752.1 mm nominal | Audited actual 482.400 × 42.850 × 752.515 mm | Both skill GLB audits: 0 errors, 0 warnings | PASS |
| Six independent faces | Six embedded images and six face materials; left/right not mirrored | Six separate textured quads, no negative-scale nodes | View audit: 0 errors, 0 warnings | PASS_WITH_BOTTOM_FALLBACK |
| Standard/web parity | Same 297 nodes/meshes/primitives and 18 materials | Structure audit exact name/count equality | Four contact sheets | PASS |
| Dual WebGL | Three.js and Babylon.js each load both GLBs in ten required views | 40 atomic READY records with correct bounds | 40 screenshots and 40 comparison sheets | PASS |

The model is accepted as a website exterior replica. It is not represented as engineering/internal CAD.
