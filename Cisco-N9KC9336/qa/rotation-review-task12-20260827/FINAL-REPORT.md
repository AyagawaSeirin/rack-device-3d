# Cisco-N9KC9336 Task-12 旋转与真实性复核

最终状态：**PASS_WITH_BOTTOM_FALLBACK**  
精确身份：**Cisco Nexus 9000 N9K-C9336C-FX2**  
复核日期：2026-08-27（Asia/Singapore）
视觉真实性返修完成：2026-08-28（Asia/Singapore）

## 结论

本型号按用户锁定的 FX2 身份与 AC 配置通过：2 × `NXA-PAC-1100W-PI2`、3 × `NXA-FAN-65CFM-PI`、port-side intake、36 × QSFP28、真实 Cisco/Nexus/PID/方向与模块布局均保留。standard/web 的结构、六面、真实 WebGL2 旋转、独立加载、matched-camera 外观和逐项 inventory 均为 0 unresolved。唯一降级项是没有找到精确底面来源，因此底面继续使用明确声明的保守闭合板 fallback。

第一轮修复前资料保存在 `qa/superseded/pre-rotation-review-20260827/`。视觉验收退回前的 GLB、构建器、六面、审计、40 loads、316 帧、正交、matched-camera、inventory、冻结清单和报告又完整追加到 `qa/superseded/pre-photographic-skin-repair-20260828/`；两处归档均未覆盖。

## 冻结哈希

| 产物 | 修复前 SHA-256 | 最终 SHA-256 | 最终字节数 |
|---|---|---|---:|
| standard GLB | `09f05222ad93c617fcba3e62a0afe493251f43e2813638616e815863ef62df49` | `c33f9ae3d36b7710e336e2aeecbad1bfd2416d20bb379e3beed84a133485868d` | 22,217,816 |
| web GLB | `debdc3ee39fab17a6482b590a373b02673e592acf92487cd032efb1677aa2841` | `cdb6e37999ed720aabe1f9da0641383f1d6320abd270a6c2696d493bea6584c6` | 1,307,548 |
| 构建器 | `1e4e6dde07b92e20c71412bbb5199778bbcfb260cf65785f7f3261c9e6148806` | `f1d523ba8762ac63ea99ee3dcce9d89f3b4f6fd45d625c2615382786fac882d9` | 以 `hash-freeze.json` 为准 |

最终模型尺寸为 439 × 44 × 623 mm（623 mm 包含真实后部突出件）。完整冻结清单及 Three.js、Babylon.js、正交查看器哈希见 `hash-freeze.json`。任何最终 GLB 哈希变化都使本目录的加载、旋转、正交和比较证据失效，必须全量重跑。

## 复现、根因与修复

### 模型根因：稳定性与照片真实性是两道独立门禁

第一轮补充结构审计确认：左右源锁平面与另建的侧面槽位/接地点 overpaint 几何结束在同一平面，形成确定性的共面深度竞争；标准版还把 RGBA 面纹理直接嵌入主面。第一轮已删除侧面重复 overpaint，并将 standard 主纹理改为 RGB-only；旋转稳定性门禁因此通过。

但视觉返查发现稳定并不等于真实：旧前照片层在机身表面后约 2.55 mm，前方的 18 组粗灰 cage frame、两块 port recess 和宽 center bar 大面积盖住照片中的双层端口、扣手与工厂标识；旧后面又在照片前叠加整块 dark honeycomb、PID 黑条、IEC/管理口方块、粗竖桥和块状把手。两个引擎一致显示这些遮挡，故根因是模型层级/过度 relief，而非查看器灯光。

最终修复将 front/rear source-photo skin 设为主外观层。粗 cage、port、vent、PSU/fan installed-volume、honeycomb、PID plate、IEC 和 management support 全部退到不透明照片 skin 后至少 0.25 mm；照片前只保留窄且与源图同位的 rim、微小 latch opening、LED、burgundy release 边缘及真实突出把手。把手横杆/支杆截面也缩细，不再把照片中的蜂窝、标签与扣手替换成平色矩形。standard 使用原子写入的 RGB PNG，web 同步重建；六个主面仍全部为 `OPAQUE`、`baseColorFactor=[1,1,1,1]`、`doubleSided=false`，机身不存在 `BLEND`。

### 查看器根因

共享 Three.js 正交查看器原先硬编码米制 QFX 所需的 camera distance/far，加载毫米制 Cisco 时会裁掉模型并产生“透明/空画面”假证据。这是查看器单位/near-far 根因，不是 GLB 透明。无效证据已保存在 `superseded-ortho-unit-clipping/`；查看器改为按实际 bounds 动态计算 distance/near/far 后，standard/web 六面全部重采。Babylon 的加载 UI 在证据查看器中关闭，采集只在 GLB 完成并稳定后入队，没有 overlay 混帧。

## 审计和真实浏览器门禁

- `audit_views`：PASS，0 errors，0 warnings。
- standard/web `audit_glb`：PASS，0 errors，0 warnings。
- standard/web 补充结构审计：PASS；material-alpha、embedded-image、sampler、negative-transform、degenerate、duplicate、opposite、未解决可见近共面、缺失 normal 均为 0；closed-core 与 winding-consistency 为 true。
- 独立加载：Three.js/Babylon.js × standard/web × 10 视角 = **40/40**；每次使用不同 cache-buster，40 个响应哈希/字节均命中冻结文件，均为 WebGL2，material violation 为 0。
- 旋转：4 组合各 72 × 5° yaw，共 **288 yaw 帧**；另有 16 个多俯仰帧和 12 个同角度稳定帧，共 **316 帧**。四组稳定帧各自逐字节相同。
- 人工 contact-sheet 目检：浅/深棋盘、顶/底俯仰和两引擎均未见闪烁、透明跳变、棋盘泄漏、面消失、镜像、纹理/灰白切换或加载遮罩混帧。

机器汇总见 `final-validation.json`；逐组合原始记录见 `final-loads/*/load-events.json` 与 `final-rotation/*/runtime.json`。

## 六面、matched-camera 与 inventory

standard/web 各生成 6 张 source / render / 50% overlay / absolute difference matched-camera 表。前面 36 个真实双层 QSFP28、Cisco/Nexus/PID 与中部扣手保持照片面貌；后面两只 PI2 PSU、三块真实蜂窝、`NXA-FAN-65CFM-PI` 标签、burgundy 扣手和管理区不再被粗块遮蔽。左右非镜像侧板与顶面通风带也继续一致。

视觉退回前→最终的 mean absolute RGB difference：standard front `6.277329 → 1.824464`，rear `4.385823 → 1.615475`；web front `6.278727 → 1.799814`，rear `4.390209 → 1.624491`。该数值只作诊断，最终 PASS 仍基于 100% feature-by-feature 人工检查。逐项 `feature-inventory.csv` 复核为 **23/23 matched、0 unresolved**，详见 `inventory-review.json`。

## 官方 3D 检索与风险

2026-08-27 重查 Cisco 官方支持、产品、安装指南与公共索引，未发现精确 `N9K-C9336C-FX2` 的公开官方 GLB/glTF/OBJ/FBX/STEP/STP/CAD 或交互 3D 包；没有可下载原样保留的官方 3D 字节。错误身份 `N9K-C9336PQ` 的历史官方查看器包仍只在 rejected 隔离区，不参与本型号。

剩余风险仅为精确底面公开证据缺失，以及该资产是外观级 web replica 而非制造 CAD。非底面没有未解决缺口。最终处置：**PASS_WITH_BOTTOM_FALLBACK**。
