# 2026-08-27 三型号独立复核总报告

| 型号 | 精确配置 | 最终状态 | 基础/深审计 | WebGL2 证据 | Inventory |
|---|---|---|---|---|---:|
| Dell-R7515-2.5inch | 15G、2U、24SFF、面板、无后盘、2×750 W AC | PASS_WITH_BOTTOM_FALLBACK | 双 GLB 0 errors；深审计 0 unresolved | 4×(72 yaw + 16 pitch + 8 stability)，40/40 loads | 40/40 |
| Dell-R730-3.5inch | 13G、2U、8LFF 2×4、无面板、标准后部、2×750 W AC | PASS_WITH_BOTTOM_FALLBACK | 双 GLB 0 errors；深审计 0 unresolved | 4×(72 yaw + 16 pitch + 8 stability)，40/40 loads | 31/31 非空记录 |
| Dell-R7525-2.5inch | 15G、2U、24SFF、LCD 面板、无后盘、2×2400 W AC | PASS | 双 GLB 0 errors；深审计 0 unresolved | 4×(72 yaw + 16 pitch + 8 stability)，40/40 loads | 47/47 非空记录 |

合计正式证据：864 个 5° yaw、192 个多俯仰棋盘帧、96 个稳定帧、120 个独立 cache-busted 加载截图；三型号 48 对重复帧逐字节一致。Three.js/Babylon.js、standard/web 全部使用真实 WebGL2；page error 0，overlay 全隐藏，near/far 比 1200，固定 1200×800 串行采集。

## 共享 viewer/runner 冻结哈希

| 文件 | SHA-256 |
|---|---|
| `viewers/three.html` | `28c5fb1c83975c9f484fad69e5a305e8c9f6596ca501efc5995a7696d778e318` |
| `viewers/babylon.html` | `c9ab50e3be29e713a212c86e3826f6cf5b4ca377643384196f60009eeffe2125` |
| `viewers/control.html` | `0df0b66c554d54fbafc3bd92843eb73aefda8c2a615a8be9464df07b5dec34b1` |
| `run_capture.js` | `4c708ca420936b97c30e16f2d0480a878a7782ce43f7856080d20278d19d13b3` |
| `run_loads.js` | `87941c9317dfcdbe4211b6b153240a1aa959ebefc966417e3e9ae54566dcdb64` |
| `deep_glb_audit.mjs` | `5f8974632c9916456eedfcb320a52d87be93831c6c7ab37b6ad92fe45fd8b0ee` |
| `generate_inventory_verification.py` | `5845d54223494a8d757dc6836a02968741126626e06957959c0939e3b80445f1` |

共同结构契约：主照片材质 OPAQUE、`[1,1,1,1]`、`doubleSided=false`、unlit；主机身不使用 BLEND；右手坐标；无负/奇异变换；无重复或 0.2 mm 内近共面三角形；闭核、外向绕序和法线均通过。每面独立纹理并使用 mipmap/clamp，不依赖全机 atlas。

失效证据均保留在各型号 `qa/rotation-review-20260827/superseded/`；修复前全量快照保留在 `qa/superseded/pre-rotation-review-20260827/`。R7525 官方 public AR GLB 原件保持未修改。未修改 `BATCH-STATUS.md`，未 stage/commit/push。

最终哈希与证据完整性分别见每型号 `final/manifests/frozen-hashes.json`、`evidence-integrity.json`；逐项真实性见 `final/inventory-verification.csv` 和八张 matched-camera 四联图。
