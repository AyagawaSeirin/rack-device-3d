# Cisco N9K-C93180YC-FX 最终报告

审计日期：2026-08-24（Asia/Singapore）

## 最终结论

**PASS_WITH_BOTTOM_FALLBACK**

本轮最终门禁修复已经完成。rear 仅做确定性 alpha 修复，RGB 完全不变；标准六面审计由 1 error 降为 0 errors。standard/web GLB 已重建，结构审计、精确身份/部件计数、标准与 web 几何一致性、两独立 WebGL 引擎的 40 次逐次哈希/字节/mtime 实载、截图哈希、比较表和人工视觉检查全部通过。

唯一 fallback 仍是精确型号底面公开证据缺失；该限制只影响底面，因此状态保持 `PASS_WITH_BOTTOM_FALLBACK`。

## 精确交付身份

- 制造商：Cisco Systems, Inc.
- 产品：Cisco Nexus 9000 C93180YC-FX Chassis
- PID：`N9K-C93180YC-FX`
- 前部：48 个空 SFP/SFP28 笼位 + 6 个空 QSFP/QSFP28 笼位；无光模块、无面罩
- 电源：2 × `NXA-PAC-500W-PI`，500W AC
- 风扇：4 × `NXA-FAN-30CFM-PI`
- 风道：port-side intake，PSU/风扇均为酒红色 PI 方向
- 机架耳：仅前部，6 个真实开孔；后耳节点为 0

## rear alpha 最小修复

标准审计核心为 rear 2200 × 221 图像的 `[176, 18, 2024, 203]` 区域。修复前核心中有 307 个 `alpha < 250` 像素和 29 个 `alpha 250–254` 像素，没有 `alpha < 8` 的真实透明孔。

修复操作只把这 336 个非 255 核心 alpha 提升为 255：

- RGB 改动像素：0
- alpha 改动像素：336
- 核心外 alpha 改动：0
- RGB SHA-256（前/后相同）：`ddd0723d2fad546fa81ee2ce11bdde30d5bb9480d4f7ee75b5c4b4269e56a059`
- 修复后 rear PNG SHA-256：`afb46b6eb7d85e4365fa2f3a47f641cfe04d7cfed9fb152909afa8d2491cbd53`
- 结构化证据：`qa/rear-alpha-repair.json`

## 最终 GLB

| 文件 | 字节数 | SHA-256 | GLB mtime UTC |
|---|---:|---|---|
| `models/Cisco-N9K-C93180YC-FX-standard.glb` | 9,883,884 | `0d6f8bbfd0993a33014b887ab6c4deabbb94b7a01c79abcecc9c57b04a3e740a` | `2026-08-24T08:14:51.131000+00:00` |
| `models/Cisco-N9K-C93180YC-FX-web.glb` | 3,492,720 | `e15f5488d4c5eadfeebb00e2056fc49194fe755ff20524aa344d3bc44ab5ff7e` | `2026-08-24T08:14:56.689000+00:00` |

两份 GLB 均为 418 nodes / 95 meshes / 15 materials / 6 embedded PNG。几何签名完全相同：`c8d3be0fe17d6d290d73f55f15b0f1f464f13aa827d6a2640da863f330355b1b`。全部材质为 `OPAQUE` 且单面，资源全部嵌入，无外部 buffer URI。

查看器实测完整包围尺寸为 482.6 × 45.15 × 581.58 mm。官方机身尺寸仍记录为 439 × 44 × 571 mm；额外高度/深度来自外部 relief、前端面及真实后部把手/锁扣。

## 审计结果

| 门禁 | 状态 | errors | warnings | 说明 |
|---|---|---:|---:|---|
| 标准六面 `audit_views.py` | PASS | 0 | 6 | 6 个 warning 均为已人工确认的外轮廓/AA 检查提示 |
| rear 核心 alpha | PASS | 0 | 1 | `core_alpha_below_250_percent=0.0`；`core_transparent_percent=0.0` |
| standard GLB 结构审计 | PASS | 0 | 1 | 内嵌 PNG 的轮廓 partial-alpha 检查提示 |
| web GLB 结构审计 | PASS | 0 | 2 | 轮廓 partial-alpha 与 web 底/顶纹理 946px 检查提示，已人工确认 |
| 综合 delivery validation | PASS_WITH_BOTTOM_FALLBACK | 0 | — | 所有布尔门禁为 true |

关键审计文件：

- `qa/views-audit.json`
- `qa/glb-structural-standard.json`
- `qa/glb-structural-web.json`
- `qa/audit.json`
- `qa/audit-standard.json`
- `qa/audit-web.json`
- `qa/delivery-validation.json`

## 双查看器 40 次实际加载

最终有效证据为 **40/40 PASS**：

| 查看器 | standard | web | 合计 |
|---|---:|---:|---:|
| Three.js r185 / WebGL2 | 10 | 10 | 20 |
| Babylon.js 9.22.1 / WebGL2 | 10 | 10 | 20 |
| 合计 | 20 | 20 | 40 |

每个 viewer/model 组合均实际加载 front、rear、left、right、top、bottom、front-left、front-right、rear-left、rear-right。40 次均使用唯一 URL，并全部满足：

- 浏览器内实际响应 SHA-256 命中：40/40
- 实际响应字节数命中：40/40
- HTTP `Last-Modified` 与最终 GLB mtime 秒级对应：40/40
- fresh-transfer 大于 1 MB：40/40
- 包围尺寸在门槛内：40/40
- 1280 × 900 截图存在且 CSV 中 SHA-256 可复算命中：40/40

证据路径：

- `qa/webgl-loads/load-events.json`
- `qa/viewer-load-evidence.csv`
- `qa/webgl-loads/three/`
- `qa/webgl-loads/babylon/`
- `qa/webgl-loads/contact-sheets/all-40-hash-proven-loads.png`

## 比较与人工检查

已重建：

- 4 张 viewer/model 十视角 contact sheet + 1 张全部 40 次总表；
- 20 张 Three.js/Babylon.js 同相机比较表；
- 6 张 source-lock 对实际 standard GLB 正交比较；
- 3 张精确 FX 实拍对前/后斜视和顶视比较。

人工检查确认 front、rear、left、right 和四个斜视均未退化。与归档前 40 张同视角截图去除动态标签后比较：standard 20/20 完全一致；仅 web 的 rear/rear-left/rear-right 出现肉眼不可见的下采样差异，单张最多变化 137/960,000 像素，最大 RGB 平均绝对差 0.000084（0–255 标度）。不存在几何、部件计数、方向、变体、品牌、颜色布局或 relief 退化。

人工记录：`qa/visual-inspection.md`。

## 历史归档与范围

修复前 rear、旧 standard/web GLB、旧审计、旧 40 次加载、旧 contact/comparisons、旧 delivery validation、旧人工检查和旧 final report 已归档到：

`qa/superseded/pre-rear-core-alpha-repair/`

本轮只修改 `Cisco-N9KC93180YC/`。未修改任何其他型号目录，未修改 `BATCH-STATUS.md`，未 commit、未 push，也未创建或分叉其他任务。

## 残余风险

1. 精确 FX 底面照片/官方图仍未找到，bottom 继续使用技能允许的保守 `GENERIC_BOTTOM_FALLBACK`，因此最终状态不能升级为无条件 PASS。
2. 保存的旧版 HIG 使用 `NXA-FAN-30CFM-B` 命名；用户最终配置锁为 `NXA-FAN-30CFM-PI`。物理外观和气流都由酒红色 intake 证据锁定，最终资产、元数据和报告统一使用 `-PI`。
3. Cisco 公开 571 mm 是机身深度，PSU 把手等突出件没有独立官方总深度；报告同时保留 571 mm 机身深度与 581.58 mm 可见包围深度，二者不混淆。
