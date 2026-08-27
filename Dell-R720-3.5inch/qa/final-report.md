# Dell PowerEdge R720 3.5-inch 独立复核最终报告

复核日期：2026-08-27

最终状态：`PASS_WITH_BOTTOM_FALLBACK`

除底面没有可核验的精确实机来源外，身份、配置、尺寸、六面、standard/web GLB、旋转稳定性、双引擎实载和逐项 inventory 均已通过。底面只保留 444 × 702 mm 的闭合不透明镀锌钢板轮廓，不虚构孔、脚、标签、通风、导轨或 Logo；因此不能标为无条件 `PASS`，但不存在非底面缺口。

## 精确身份、代际与安装配置

- Dell PowerEdge R720，Dell 第 12 代，2U；明确排除 R720xd、SFF、R730/R730xd。
- 前部为 8 × 3.5-inch LFF，2 × 4 排列，8 个托架全部安装，无安全面罩。
- 保留真实 DELL 与 PowerEdge R720 工厂标识、LCD/控制区、VGA、vFlash、双 USB 和光驱位。
- 后部为标准 R720 七槽结构：3 个低矮型 + 4 个全高 PCIe 原厂挡板；iDRAC7、DB9、VGA、2 × USB、4 × Base-T RJ45 NDC。
- 电源锁定为 2 个匹配的 Dell 750 W 热插拔 AC PSU；两套 IEC 入口、橙色释放件、把手和 PSU 风扇均保留；无 DC 或混装 PSU。
- 前耳为独立厚度结构并保留真实开孔；系统内部风扇不从闭合外壳外露，外部可见的两个 PSU 风扇按来源照片保留。
- 官方 Figure 18 的 `Za=18`、`Zb=684`、`Zc=723` 均以机架法兰为基准；因此主体深度为 `Za+Zb=702 mm`，完整安装包络为 `Za+Zc=741 mm`。最终 GLB 为 482.4 × 87.3 × 741.0 mm，误差 0。

## 冻结交付物与哈希

| 对象 | 字节 | SHA-256 |
|---|---:|---|
| `model/Dell-R720-3.5inch.glb` | 19,031,468 | `6cb22b48cbf149098ca591cc24883e9be433557205d27944b84df3099d84480c` |
| `model/Dell-R720-3.5inch-web.glb` | 11,417,136 | `2260b8287221acd83c3dcafa2dbfde1c191e4db3fbead8ff10d868750c1ef597` |
| `model/build_model.py` | — | `75389ad6de4eb12af02b16f442b0d5e68e7559287dfba1e0ab9fda1313729d31` |
| Three.js 最终查看器 | — | `46aaa42db740588f0d7d5ce017e61e394047af69ea2f0c9d70ec229ace48eb2a` |
| Babylon.js 最终查看器 | — | `b755375b1bc11e68853591f3f3aee0cd6058c0801345f8ee936126d8b780d9a2` |

完整模型、构建器、六面和 viewer 冻结清单在 `qa/rotation-review-20260827/final/frozen-hashes.sha256`；最终证据完成后复核为全部 `OK`，不存在证据生成后模型/viewer 哈希变化。

## 问题复现、根因与因果修复

旧成果没有因为旧 `PASS` 被信任。修复前的 standard/web、构建器、六面、审计、加载证据与报告已完整归档到 `qa/superseded/pre-rotation-review-20260827/`。

修复前两引擎 × 两 GLB 已各完成 72 × 5° yaw、16 个多俯仰和 8 个同角度稳定帧。当前 Chromium/WebGL2 环境没有捕获到随机 alpha 跳变，同角度 A/B 为逐像素一致；但深层网格审计确实复现了可造成视角/深度相关闪烁的模型缺陷：standard 有 96 对精确共面和 104 对近共面三角形，web 有 96/84 对，均留下 2 个 unresolved 类别。问题集中在 PSU 照片面与风扇/紧固件、侧面照片卡与挂钉/槽、前耳框与闭合片等重复或近共面层。稳定截图不能排除这种深度竞争。

模型侧修复包括：裁剪前面 source-lock 照片至主体、用非重叠带状几何重建耳片与真实开孔、删除冗余闭合片和侧面长条、将面卡/浮雕分别内缩到有明确深度顺序的位置、让 PSU 精确照片只落在真实突出面并移除重叠风扇圆片。standard/web 同一构建路径同步重建。

查看器侧是独立的证据与显示风险：旧流程没有同时强制 WebGL2、Babylon 右手坐标、模型哈希核验、透明棋盘、受控 near/far、串行捕获和 overlay 隔离。最终查看器显式使用 WebGL2，Babylon 采用右手坐标，关闭 tone mapping，near/far 比固定为 128，浅/深棋盘背景，ready+哈希确认后才隐藏 overlay，并在串行队列中等待 3 个稳定 RAF 再截图。查看器修复没有用于掩盖模型缺陷；深层几何审计先归零后才生成最终证据。

## 最终审计

- 两份技能 GLB 审计：均 `PASS`，0 error / 0 warning；各 259 nodes、259 meshes/primitives、13 materials、8 个嵌入图像、0 外链资源。
- 两份深层审计：duplicate triangle groups、exact coplanar、near-coplanar、negative/singular transform、BLEND、doubleSided、primary-face material error、closed-core failure、inward watertight mesh 和 normal mismatch 全部为 0；`unresolved=[]`。
- 主六面材质均为 `OPAQUE`、`baseColorFactor=[1,1,1,1]`、`doubleSided=false`；主机身没有 `BLEND`。
- `audit_views` 为 `PASS`、0 error。3 条 alpha 提示已逐张检查：只位于轮廓抗锯齿/真实开孔，core transparent 为 0 或近 0；嵌入 GLB 的照片副本为不带非透明 alpha 的 RGB/OPAQUE，不构成棋盘泄漏。
- inventory 43/43 已逐项映射到最终 GLB 和 matched-camera 证据：41 `PASS`，2 个底面约束行 `PASS_WITH_BOTTOM_FALLBACK`。

## 最终真实 WebGL2 验收

- Three.js × standard/web、Babylon.js × standard/web 共 4 个组合。
- 每组合 72 个 5° yaw + 16 个多俯仰 + 8 个稳定帧；每型号合计 288 yaw、64 pitch、32 stability，即 384 帧。多俯仰覆盖浅/深棋盘；4 个基准角的 A/B 稳定帧在每组合均为 `AE=0`。
- 冻结后完成 40 次 cache-busted 独立真实页面加载：2 引擎 × 2 GLB × 10 规定视角。全部 HTTP 200、WebGL2、实际哈希=期望哈希、overlay 已隐藏、`page_errors=[]`、材质违规为 0。
- 已生成 12 张 matched-camera 捕获（6 面 × 浅/深）及 6 张 source/render/overlay/difference 四联图；接触表人工复核未见闪烁、透明跳变、棋盘泄漏、面消失、镜像、纹理切换、灰白跳变或遮罩混帧。

核心证据：

- `qa/rotation-review-20260827/final/rotation/`
- `qa/rotation-review-20260827/final/loads/load-manifest.json`
- `qa/rotation-review-20260827/final/contact-sheets/rotation-all-combos.png`
- `qa/rotation-review-20260827/final/contact-sheets/loads-all-40.png`
- `qa/rotation-review-20260827/final/comparisons/`
- `qa/rotation-review-20260827/final/inventory-verification.csv`
- `qa/rotation-review-20260827/after/deep-standard.json` 与 `deep-web.json`

## 官方/公共精确 3D 检索与真实性

截至 2026-08-27，已复核 Dell 当前 R720 支持、手册、驱动、视频和公开资源，并按 exact PID 搜索 3D/CAD/STEP/IGES/GLB/glTF/OBJ/FBX/BIM/Visio/AR；也检查了 GrabCAD、3DContentCentral、Sketchfab 和公共索引。没有找到可验证且精确匹配 R720 8-LFF、标准七槽、双 750 W AC 安装配置的官方外观模型或权威公共模型，因此没有可下载并原样保留的官方二进制文件，也未把社区模型冒充官方。记录在 `source/optional-3d/recheck-20260827.md`。

最终两份 GLB 是依据官方尺寸、官方手册、用户配置锁和多角度精确实机证据重建的网站外观副本，不是 OEM CAD。六面来源与不可镜像方向记录在 `source/face-source-lock.csv`；品牌 Logo 因真实性要求保留。

## 残余风险

1. 精确底面仍无权威实机来源，只能采用明确披露的保守 fallback。
2. 模型是外观/DCIM 用重建，不包含内部工程结构；极小印刷文字不应视为工程级可读数据。
3. 没有官方精确 3D 可做网格对网格比较。

本任务未修改 `BATCH-STATUS.md`，未执行 git commit 或 push，也未处理其他型号。
