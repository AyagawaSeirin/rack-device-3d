# Dell PowerEdge R620 2.5-inch / 10SFF 独立复核最终报告

复核日期：2026-08-27

最终状态：`PASS_WITH_BOTTOM_FALLBACK`

除底面没有可核验的精确 R620 10SFF 实机来源外，身份、配置、尺寸、六面、standard/web GLB、旋转稳定性、双引擎实载和逐项 inventory 均已通过。底面只使用闭合不透明的保守镀锌钢板，不虚构孔、脚、标签、通风、导轨或 Logo；不存在非底面缺口。

## 精确身份、代际与安装配置

- Dell PowerEdge R620，Dell 第 12 代，1U，10 × 2.5-inch SFF；前部两行五列，10 个托架全部安装，无安全面罩。
- 明确排除 8SFF 短机身、R720/R720xd、2 × SFP+ 混合 NDC、两 PCIe 槽后部和 DC PSU。
- 10SFF 专属后部为 3 个低矮型 PCIe 挡板；iDRAC7、DB9、VGA、2 × USB、4 × Base-T RJ45 RNDC。
- 电源锁定为 2 个匹配的 Dell 750 W 热插拔 AC PSU；两套 IEC C14、橙色释放件、把手和可见 PSU 风扇均保留。七个内部系统风扇不从闭合外壳外露，因此不虚构为外表面几何。
- 保留真实 DELL 与 PowerEdge R620 工厂标识；前耳为独立突出结构并保留真实开孔。
- 官方 Figure 14 的 `Za=20.4`、`Zb=731`、`Zc=752.1` 以机架法兰为基准，而不是三个互相替代的总深度。10SFF 主体深度为 `Za+Zb=751.4 mm`，完整安装包络为 `Za+Zc=772.5 mm`。最终 GLB 为 482.4 × 42.8 × 772.5 mm，误差 0。

## 冻结交付物与哈希

| 对象 | 字节 | SHA-256 |
|---|---:|---|
| `model/Dell-R620-2.5inch.glb` | 17,090,656 | `ae3523f8ad0be17c38c7ac74ab3b2a340bcd66088ae8434a8731c00ff1591fb8` |
| `model/Dell-R620-2.5inch-web.glb` | 10,299,896 | `72958073d37626c79b7c83a2b4207429154b61dcbb92e08194f4ab83663dd2e6` |
| `model/build_model.py` | — | `e7bc9121b888f4e9c4558ca85c7afcbf97b8e7180241022a832a878baa283ddf` |
| Three.js 最终查看器 | — | `46aaa42db740588f0d7d5ce017e61e394047af69ea2f0c9d70ec229ace48eb2a` |
| Babylon.js 最终查看器 | — | `b755375b1bc11e68853591f3f3aee0cd6058c0801345f8ee936126d8b780d9a2` |

完整冻结清单在 `qa/rotation-review-20260827/final/frozen-hashes.sha256`；最终证据完成后复核全部 `OK`，不存在模型/viewer 哈希变化后继续沿用旧证据的情况。

## 问题复现、根因与因果修复

修复前的 GLB、构建器、六面、审计、加载证据与报告已完整归档到 `qa/superseded/pre-rotation-review-20260827/`，没有覆盖或删除旧成果。

修复前两引擎 × 两 GLB 已各完成 72 × 5° yaw、16 个多俯仰和 8 个稳定帧。当前 Chromium/WebGL2 环境的同角度 A/B 为逐像素一致，没有捕获到随机 alpha 跳变；但深层审计直接复现了模型缺陷：standard 有 1,172 对精确共面和 7,136 对近共面三角形，web 有 808/5,984 对，均留下 2 个 unresolved 类别。主要来自照片面与端口/PSU/风扇/紧固件、侧面卡与挂钉/槽、耳框与闭合片的重复或近共面层。这种深度竞争会随视角、深度精度和引擎实现改变，不能被同角度稳定帧洗白。

模型侧修复包括：按正确 751.4/772.5 深度重建闭合核心；以非重叠带状几何重建两只前耳与穿透开孔；把后部主体照片与突出 PSU 精确照片分置于不同真实深度；删除冗余覆盖层、共面风扇圆片和 flush 细节；让侧面/顶面照片与凹凸 relief 有明确深度顺序。standard/web 由同一构建器同步重建。

查看器侧的旧证据链也有独立风险：没有同时强制 WebGL2、Babylon 右手坐标、模型哈希核验、透明棋盘、受控 near/far、串行捕获和 overlay 隔离。最终查看器显式使用 WebGL2，Babylon 采用右手坐标，关闭 tone mapping，near/far 比固定为 128，浅/深棋盘背景，ready+哈希确认后才隐藏 overlay，并等待 3 个稳定 RAF 后串行截图。模型审计归零后才生成最终证据，没有以灯光或查看器设置掩盖错误。

## 最终审计

- 两份技能 GLB 审计：均 `PASS`，0 error / 0 warning；各 302 nodes、302 meshes/primitives、17 materials、8 个嵌入图像、0 外链资源。
- 两份深层审计：duplicate triangle groups、exact coplanar、near-coplanar、negative/singular transform、BLEND、doubleSided、primary-face material error、closed-core failure、inward watertight mesh 和 normal mismatch 全部为 0；`unresolved=[]`。
- 主六面材质均为 `OPAQUE`、`baseColorFactor=[1,1,1,1]`、`doubleSided=false`；主机身没有 `BLEND`。
- `audit_views` 为 `PASS`，0 error / 0 warning。
- inventory 44/44 已逐项映射到最终 GLB 和 matched-camera 证据：42 `PASS`，2 个底面约束行 `PASS_WITH_BOTTOM_FALLBACK`。

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

截至 2026-08-27，已复核 Dell 当前 R620 支持、手册、驱动、视频和公开资源，并按 exact PID 搜索 3D/CAD/STEP/IGES/GLB/glTF/OBJ/FBX/BIM/Visio/AR；也检查了 GrabCAD、3DContentCentral、Sketchfab 和公共索引。没有找到可验证且精确匹配 R620 10SFF、三低矮槽、四 Base-T RJ45、双 750 W AC 安装配置的官方外观模型或权威公共模型；搜索中的 Scania R620、家族级或无安装配置社区模型均被排除。没有可下载并原样保留的官方二进制文件。记录在 `source/optional-3d/recheck-20260827.md`。

最终两份 GLB 是依据官方尺寸、官方手册、用户配置锁和多角度精确实机证据重建的网站外观副本，不是 OEM CAD。六面来源、物理左右方向和不可镜像约束记录在 `source/face-source-lock.csv`；品牌 Logo 因真实性要求保留。

## 残余风险

1. 精确 R620 10SFF 底面仍无权威实机来源，只能采用明确披露的保守 fallback。
2. 模型是外观/DCIM 用重建，不包含内部工程结构；极小印刷文字不应视为工程级可读数据。
3. 没有官方精确 3D 可做网格对网格比较。

本任务未修改 `BATCH-STATUS.md`，未执行 git commit 或 push，也未处理其他型号。
