# N9K-C93180YC-FX 最终人工视觉检查

检查日期：2026-08-24（Asia/Singapore）  
检查对象：alpha 修复后重新构建的 standard/web GLB 及新一轮 40 次 WebGL 实载截图  
结论：**PASS；前、后、左、右及四个斜视均未退化**

## 检查范围

- 总览：`qa/webgl-loads/contact-sheets/all-40-hash-proven-loads.png`
- 正交：front、rear、left、right、top、bottom，覆盖 Three.js/Babylon.js 与 standard/web
- 斜视：front-left、front-right、rear-left、rear-right，覆盖 Three.js/Babylon.js 与 standard/web
- source-lock 对实际 GLB：`qa/comparisons/source-vs-render/`
- 双引擎同相机比较：`qa/comparisons/matched-engine/`
- 精确 FX 实拍斜视比较：`qa/comparisons/authoritative-oblique/`

## 结果

- front：48 个 SFP28 与 6 个 QSFP28 笼位、Cisco/PID 区域、前耳和真实开孔均保持完整；无镜像、裁切或丢件。
- rear：2 个 NXA-PAC-500W-PI、4 个酒红色 NXA-FAN-30CFM-PI、FX I/O 与拉手顺序保持不变；底盘核心不再出现非必要半透明像素；无后耳。
- left/right：两个独立侧面纹理与独立 relief 保持可见，左右未镜像或互换。
- front-left/front-right：端口面、前耳、顶盖和侧板的轮廓、层级、深度与视差无退化。
- rear-left/rear-right：双 PSU、四风扇、FX I/O、顶盖和侧板的顺序、颜色、深度与视差无退化。
- standard/web：轮廓、部件计数、方向和几何一致；两个引擎只存在原有的轻微抗锯齿/亮度差。

## 与归档前截图的退化比较

将新旧 40 张同视角截图裁去动态 run/status 标签后逐像素比较：

- 34/40 完全一致；
- standard 的 20/20 全部完全一致；
- 仅 web 的 rear、rear-left、rear-right 在两个引擎中各有极少量下采样像素变化，共 6 张；
- 单张最多变化 74 像素，比较区域 960,000 像素，约 0.0077%；
- 单张最大 RGB 平均绝对差为 0.000084（0–255 标度），肉眼不可见；
- 变化只来自修复后 rear alpha 参与 web 纹理下采样，不存在几何、身份、颜色布局或部件退化。

源 rear PNG 的 RGB 像素改动为 0，alpha 改动为 336，核心外 alpha 改动为 0。标准视图审计的 rear `core_alpha_below_250_percent` 与 `core_transparent_percent` 均为 0。

## 已说明的警告

六面 PNG 都保留透明外部背景与轮廓抗锯齿，因此标准审计保留 6 个透明/半透明轮廓检查 warning。人工在 checkerboard 上确认它们位于外轮廓/抗锯齿区域，不是底盘核心窗口、端口孔洞或透明雾。
