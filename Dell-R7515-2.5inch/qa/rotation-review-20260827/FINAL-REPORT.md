# Dell PowerEdge R7515 24×2.5-inch 独立复核报告

最终状态：**PASS_WITH_BOTTOM_FALLBACK**

## 身份与配置结论

- 精确产品：Dell EMC PowerEdge R7515，15G/YX5X，2U，单路 AMD 机型。
- 锁定配置：24×2.5-inch SFF，24 个 carrier/blank 面完整；13 单元错列大六边形安全面板已安装；无后置盘笼。
- 后部：Riser 1B、slot 4/5、双 onboard 1GbE、双口 LOM、iDRAC、DB9、VGA、双 USB，未混入 R7525/R730 后板。
- 电源：两个相同 Dell EPP 750 W 热插拔 AC PSU，IEC 输入、圆形风扇、橙色释放件均保留；无 PSU blank。
- 厂牌：中央 DELL EMC 标识保留在 source-locked 正面与独立标识纹理中。
- 官方尺度：482 mm 耳片宽、434 mm 机身宽、86.8 mm 高、Za 35.84 mm、Zb 647.07 mm、Zc 681.755 mm；安装总深 717.595 mm。
- GLB 实测包围盒：481.99999 × 86.95000 × 717.79501 mm，处于来源账本容差内。

## 冻结基线

| 项目 | SHA-256 | 大小 |
|---|---|---:|
| builder `model/build_model.py` | `91514dc50735e3916aa9d840120fa664b117d36346c9e4a0025a1210c9039211` | — |
| standard `model/Dell-R7515-2.5inch.glb` | `9a25733362476989fd0947202932f7c38b5483d05df3c43be4e685987e71a47c` | 17,739,812 B |
| web `model/Dell-R7515-2.5inch-web.glb` | `aeba647e9f07f557f371fc8505313d06b8c1114f14c43dddbc7ead59f9f37996` | 8,173,788 B |
| 六面 PNG 集合 | `bf44f2e0c8e271af9a9449752045e8b7fd0822aee334ee364a48e4bb07cfe878` | — |

共享查看器冻结值：Three `28c5fb1c…318`；Babylon `c9ab50e3…125`；control `0df0b66c…4b1`；rotation runner `4c708ca4…13b3`；load runner `87941c93…b64`。完整值见 `final/manifests/frozen-hashes.json` 和 `final/manifests/evidence-integrity.json`。

## 根因与修复

模型侧根因：闭核与六面 source card 的间距过小；顶面 card/浮雕近共面；13 个独立蜂窝环与上下框在交点重复；后部相邻 riser 框、PSU volume/照片端面间距不足；Trimesh 导出的照片材质仍受 PBR/采样器差异影响。

模型侧修复：缩小闭核并为主卡片保留安全深度；下沉顶面照片并分离盖板/锁扣；将 13 单元格栅和上下框布尔合并后拆顶点、重算法线；错开后部框层；将 PSU volume 与 source-locked 端面分离 0.6 mm；统一照片材质为 `KHR_materials_unlit`、`OPAQUE`、`[1,1,1,1]`、`doubleSided=false`，并固定 `LINEAR_MIPMAP_LINEAR`/`CLAMP_TO_EDGE`。standard/web 由同一 builder 同步生成。

查看器侧根因：早期采集 runner 在 Node 上下文读取 `URL`，且 Babylon 连续 render loop 与截图 readback 叠加会造成采集不稳定；这不属于 GLB 缺陷。

查看器侧修复：查询参数改在页面上下文读取；Babylon 改为显式静态渲染；两引擎强制 WebGL2、固定 1200×800、右手语义、near/far 比 1200、固定中性光、无 tone mapping/后处理。主照片为 unlit，灯光不能掩盖纹理或法线问题；采集队列逐帧 `await`，不并发混帧。

## 审计结果

- `audit_views`: PASS，0 errors；6 条 warning 仅为透明画布轮廓抗锯齿，核心区域无透明孔洞。
- standard/web `audit_glb`: 均 PASS，0 errors，0 warnings；104 nodes、104 meshes、13 materials、9 embedded RGB images。
- standard/web 深审计均为 PASS，2,860 个世界空间三角形实例；duplicate 0、exact coplanar 0、near-coplanar 0、negative/singular transform 0、BLEND 0、doubleSided 0、primary-material error 0、closed-core failure 0、inward watertight mesh 0、normal/winding mismatch 0、unresolved 0。
- 无外部 buffer；主照片没有 alpha 通道，不使用全机 atlas，避免 mipmap/atlas 边缘串色。

## WebGL2 旋转与加载

- Three.js standard/web、Babylon.js standard/web 四组合各 72 个 yaw（0–355°，5°步进）、16 个多俯仰帧（-28/-8/+8/+28°，深/浅棋盘）、8 个稳定重复帧。
- 每型号合计 288 yaw + 64 pitch + 32 stability；16 对稳定帧逐字节相同。
- 40 次 cache-busted 独立新页面加载：每组合 10 次，40/40 PASS，page error 0，overlay 全部隐藏，实际 GLB hash 全部匹配；加载 1,205–3,513 ms，平均 2,193 ms。
- 四联图覆盖 yaw 000/045/090/135/180/225/270/315；逐帧目检未见闪烁、透明跳变、泄漏、面消失、镜像、纹理切换、灰白跳变或遮罩混帧。

## 真实性与 inventory

- `source/feature-inventory.csv` 的 40/40 行已逐行验证；standard/web 均无非底面缺口。
- 结果表：`final/inventory-verification.csv`；摘要：`final/manifests/inventory-summary.json`。
- 正面、后部、两侧、顶面均为 exact-model/source-locked；细字、标识和密集端口保持在不失真的 OPAQUE 照片面，耳片、面板、PSU、格栅、把手、风扇等关键轮廓保留独立深度。

## 残余风险

唯一缺口是没有找到该精确安装配置的可信底面照片或官方 public 3D；底面保持无品牌、无脚、无导轨、无虚构孔位的保守通用金属板。按约束仅此项允许 `PASS_WITH_BOTTOM_FALLBACK`，不存在需 BLOCKED 的非底面缺口。

## 复现

1. 按 `.agents/skills/rack-device-3d-model-assets/scripts/audit_views.py` 与 `audit_glb.py` 对 `views/` 和双 GLB 重跑基础审计。
2. `node Dell-R730-3.5inch/qa/rotation-review-20260827/deep_glb_audit.mjs <glb> <json>` 重跑专项审计。
3. 在仓库根启动 `python3 -m http.server 8897 --bind 127.0.0.1`，用 Playwright CLI 打开共享 `viewers/control.html`，snapshot 后分别执行 `run_capture.js` 与 `run_loads.js`。
4. `python3 Dell-R730-3.5inch/qa/rotation-review-20260827/generate_inventory_verification.py` 会重新验证 builder/GLB/viewer/manifest/重复帧哈希，再生成 inventory 结果；任一哈希不一致即停止。

