# Dell PowerEdge R720 2.5-inch / 16SFF 独立复核最终报告

复核日期：2026-08-27

最终状态：`PASS_WITH_BOTTOM_FALLBACK`

除底面没有可核验的精确 R720 16SFF 实机来源外，身份、配置、尺寸、六面、standard/web GLB、旋转稳定性、双引擎实载和逐项 inventory 均已通过。底面只保留 444 × 702 mm 的闭合不透明镀锌钢板轮廓，不虚构孔、脚、标签、通风、导轨或 Logo；不存在非底面缺口。

## 精确身份、代际与安装配置

- Dell PowerEdge R720，Dell 第 12 代，2U，16 × 2.5-inch SFF；16 个纵向托架为单排排列，全部安装，无安全面罩。
- 明确排除 R720xd、24SFF、8SFF、8LFF、R730/R730xd、后置 flex-bay、SFP+/10Gb-T NDC 和 DC PSU。
- 保留真实 DELL 与 PowerEdge R720 工厂标识以及原厂控制/媒体区。
- 后部为标准七槽：3 个低矮型 + 4 个全高 PCIe 挡板；iDRAC7、DB9、VGA、2 × USB、4 × Base-T RJ45 NDC、中央把手，无后置盘位。
- 电源锁定为 2 个匹配的 Dell 750 W 热插拔 AC PSU；两套 IEC、橙色释放件、把手、格栅和 PSU 风扇均保留。系统内部风扇不从闭合外壳外露，不虚构为外表面几何。
- 前耳为独立厚度结构并保留真实开孔；左右侧分别由独立来源锁定，没有镜像。
- 官方 Figure 18 的 `Za=18`、`Zb=684`、`Zc=723` 以机架法兰为基准；主体深度为 `Za+Zb=702 mm`，完整安装包络为 `Za+Zc=741 mm`。旧模型误把 684/723 直接当主体/总深度；最终 GLB 已修正为 482.4 × 87.3 × 741.0 mm，误差 0。

## 冻结交付物与哈希

| 对象 | 字节 | SHA-256 |
|---|---:|---|
| `model/Dell-R720-2.5inch.glb` | 11,368,272 | `20956b037d3f6ff179e6174f7d8c6081b2e739bdde2be13a5d738717d608469b` |
| `model/Dell-R720-2.5inch-web.glb` | 6,442,488 | `2fae80ebdef8f0cba6d2bb3cada080524294f77fcebdc4dd72b92f1304914c3a` |
| `model/build_model.mjs` | — | `1a497b60bd416ca3ac904b4e21a5958aa426823cb4af86657c40bacbb88a10e1` |
| Three.js 最终查看器 | — | `46aaa42db740588f0d7d5ce017e61e394047af69ea2f0c9d70ec229ace48eb2a` |
| Babylon.js 最终查看器 | — | `b755375b1bc11e68853591f3f3aee0cd6058c0801345f8ee936126d8b780d9a2` |

完整模型、构建器、六面和 viewer 冻结清单在 `qa/rotation-review-20260827/final/frozen-hashes.sha256`；最终证据完成后复核为全部 `OK`，不存在证据生成后模型/viewer 哈希变化。

## 问题复现、根因与因果修复

修复前的 GLB、构建器、六面、审计、加载证据与报告已完整归档到 `qa/superseded/pre-rotation-review-20260827/`，没有覆盖或删除旧成果。

修复前两引擎 × 两 GLB 已各完成 72 × 5° yaw、16 个多俯仰和 8 个稳定帧。当前 Chromium/WebGL2 环境的同角度 A/B 为逐像素一致，没有捕获到随机 alpha 跳变；但深层审计直接复现了模型缺陷：standard 和 web 均有 376 对精确共面、708 对近共面三角形并留下 2 个 unresolved 类别。主要来自照片面与 relief/端口/PSU、耳框与闭合片、侧面卡与挂钉/槽的重复或近共面层。这种深度竞争会随视角和引擎深度精度改变，不能被静态截图或同角度稳定帧排除。

模型侧修复包括：按正确 702/741 深度重建闭合核心；将六面卡内缩并建立明确的照片/relief 深度顺序；分离后部框、照片和突出 PSU；删除跨越 PCIe 的端口照片子卡和重叠覆盖层；让实体几何使用正常受光材料，仅 source-locked 照片面使用 unlit；所有主面强制 OPAQUE、neutral base factor 和单面渲染。standard/web 同步重建。

左侧 source-lock PNG 还复现了可见 `#FF00FF` 色键边缘。修复脚本仅清理色键/边缘污染并补齐轮廓，不缩放、不镜像、不重绘身份细节；最终 GLB 嵌入副本为 RGB/OPAQUE。旋转和 matched-camera 证据中未再出现洋红边、透明跳变或棋盘泄漏。

查看器侧的旧证据链也有独立风险：没有同时强制 WebGL2、Babylon 右手坐标、模型哈希核验、透明棋盘、受控 near/far、串行捕获和 overlay 隔离。最终查看器显式使用 WebGL2，Babylon 采用右手坐标，关闭 tone mapping，near/far 比固定为 128，浅/深棋盘背景，ready+哈希确认后才隐藏 overlay，并等待 3 个稳定 RAF 后串行截图。模型审计归零后才生成最终证据，没有以灯光或查看器设置掩盖错误。

## 最终审计

- 两份技能 GLB 审计：均 `PASS`，0 error / 0 warning；各 253 nodes、253 meshes/primitives、15 materials、6 个嵌入图像、0 外链资源。
- 两份深层审计：duplicate triangle groups、exact coplanar、near-coplanar、negative/singular transform、BLEND、doubleSided、primary-face material error、closed-core failure、inward watertight mesh 和 normal mismatch 全部为 0；`unresolved=[]`。
- 主六面材质均为 `OPAQUE`、`baseColorFactor=[1,1,1,1]`、`doubleSided=false`；主机身没有 `BLEND`。
- `audit_views` 为 `PASS`、0 error。6 条 alpha 提示已逐张检查：只位于外轮廓抗锯齿/真实开孔，除左面极小色键清理边缘外 core transparent 为 0 或近 0；嵌入 GLB 的照片副本没有非透明 alpha，不构成模型透明。
- inventory 25/25 已逐项映射到最终 GLB 和 matched-camera 证据：24 `PASS`，1 个底面行 `PASS_WITH_BOTTOM_FALLBACK`。

## 最终真实 WebGL2 验收

- Three.js × standard/web、Babylon.js × standard/web 共 4 个组合。
- 每组合 72 个 5° yaw + 16 个多俯仰 + 8 个稳定帧；每型号合计 288 yaw、64 pitch、32 stability，即 384 帧。多俯仰覆盖浅/深棋盘；4 个基准角的 A/B 稳定帧在每组合均为 `AE=0`。
- 冻结后完成 40 次 cache-busted 独立真实页面加载：2 引擎 × 2 GLB × 10 规定视角。全部 HTTP 200、WebGL2、实际哈希=期望哈希、overlay 已隐藏、`page_errors=[]`、材质违规为 0。
- 已生成 12 张 matched-camera 捕获（6 面 × 浅/深）及 6 张 source/render/overlay/difference 四联图；接触表人工复核未见闪烁、透明跳变、棋盘泄漏、面消失、镜像、纹理切换、灰白跳变、洋红边或遮罩混帧。

核心证据：

- `qa/rotation-review-20260827/final/rotation/`
- `qa/rotation-review-20260827/final/loads/load-manifest.json`
- `qa/rotation-review-20260827/final/contact-sheets/rotation-all-combos.png`
- `qa/rotation-review-20260827/final/contact-sheets/loads-all-40.png`
- `qa/rotation-review-20260827/final/comparisons/`
- `qa/rotation-review-20260827/final/inventory-verification.csv`
- `qa/rotation-review-20260827/after/deep-standard.json` 与 `deep-web.json`

## 官方/公共精确 3D 检索与真实性

截至 2026-08-27，已复核 Dell 当前 R720 支持、手册、驱动、视频和公开资源，并按 exact PID 搜索 3D/CAD/STEP/IGES/GLB/glTF/OBJ/FBX/BIM/Visio/AR；也检查了 GrabCAD、3DContentCentral、Sketchfab 和公共索引。没有找到可验证且精确匹配 R720 16SFF、标准七槽、四 Base-T RJ45、双 750 W AC 安装配置的官方外观模型或权威公共模型，因此没有可下载并原样保留的官方二进制文件，也未把家族级或社区模型冒充官方。记录在 `source/optional-3d/recheck-20260827.md`。

最终两份 GLB 是依据官方尺寸、官方手册、用户配置锁和多角度精确实机证据重建的网站外观副本，不是 OEM CAD。六面来源、物理左右方向和不可镜像约束记录在 `source/face-source-lock.csv`；品牌 Logo 因真实性要求保留。

## 残余风险

1. 精确 R720 16SFF 底面仍无权威实机来源，只能采用明确披露的保守 fallback。
2. 模型是外观/DCIM 用重建，不包含内部工程结构；极小印刷文字不应视为工程级可读数据。
3. 没有官方精确 3D 可做网格对网格比较。

本任务未修改 `BATCH-STATUS.md`，未执行 git commit 或 push，也未处理其他型号。
