# Juniper-QFX5110 Task-12 第二次独立交叉复核

最终状态：**PASS_WITH_BOTTOM_FALLBACK**  
精确身份：**Juniper QFX5110-48S-AFI，AC，Air In**  
复核日期：2026-08-27（Asia/Singapore）

## 结论

本轮在不信任旧 PASS 的前提下重新对当前 standard/web 哈希做第二次独立审计、真实 WebGL2 加载、四组合 5° 旋转、正交六面、matched-camera 与逐项 inventory 复核。48 × SFP+、4 × QSFP28、5 × AFI fan、2 × 650 W AC-AFI PSU、前耳、Juniper Logo/型号、管理区顺序与方向均一致。模型本轮无需再次修改；唯一降级项仍是精确底面照片不可得。

本轮开始前的当前模型、构建器、六面、审计、加载证据和报告已追加归档到 `qa/superseded/pre-rotation-review-20260827/task12-crossreview-20260827T142426Z/`，没有覆盖此前归档。

## 冻结哈希

| 产物 | Task-12 复核前 | Task-12 最终 | 字节数 |
|---|---|---|---:|
| standard GLB | `079472babeefd92349789edeb28f33635c04fcb9086dfd900e7fcb0e4325ac59` | 同左，未改模型 | 19,620,376 |
| web GLB | `cdd30d96cfe04c2ba44cfe27176c89fcb5267b266ccb6543f3ddbac04a9ee53d` | 同左，未改模型 | 7,272,784 |
| 构建器 | `0d151f7ea73130fb19ddf0bbfa5df010c3331603445d8db093cdfe0113819f13` | 同左 | 以 `hash-freeze.json` 为准 |

当前几何 bounds 为 482.6 × 43.848 × 551.992 mm，包含前耳与后模块把手；机身权威尺寸在 source ledger 中单独保留。

## 复现、模型根因与查看器根因

此前独立旋转复核保存的 pre checkpoint 在四组合 × 72 yaw 中没有出现可诚实宣称的整面可见闪烁；旧报告没有虚构 before failure。其结构风险是前面源锁纹理与 relief clearance 过小，以及 face sampler 的 mip 边缘 wrap；此前已把 clearance 固定到 0.20 mm，并将 sampler 设为 `CLAMP_TO_EDGE`。本次结构审计重新确认风险没有回归，因此模型哈希保持不变。

本轮实际发现的查看器根因是共享正交查看器固定 camera distance/far：它适合本型号的米制坐标，却会裁剪毫米制 Cisco，造成假透明证据。该查看器已按 bounds 动态计算 near/far；QFX 自身正交结果也用修复后的查看器重新采集。Babylon loading overlay 禁用，采集队列只在模型稳定后截图。

## 审计与真实浏览器门禁

- `audit_views`：PASS，0 errors；6 个 warning 经本轮图像复核为外轮廓 AA、连接器/通风或真实机架孔，0 unresolved。
- standard/web `audit_glb`：PASS，0 errors，0 warnings。
- standard/web 补充结构审计：PASS；material-alpha、embedded-image、sampler、negative-transform、degenerate、duplicate、opposite、未解决可见近共面、缺失 normal 均为 0；closed-core 与 winding-consistency=true；两层级几何均为 5,018 triangles。
- 独立加载：2 引擎 × 2 层级 × 10 视角 = **40/40**；全部使用唯一 cache-buster，响应 SHA-256/字节与冻结 GLB 一致，均为 WebGL2，material violation=0。
- 旋转：四组合各 72 × 5° yaw，共 **288 yaw 帧**；另有 16 个多俯仰帧和 12 个同角度稳定帧，共 **316 帧**。四组稳定帧分别逐字节一致。
- 浅/深棋盘和两引擎 contact sheet 人工检查未见闪烁、透明跳变、棋盘泄漏、面消失、镜像、纹理/灰白切换或加载遮罩混帧。

汇总见 `final-validation.json`，原始运行证据见 `final-loads/` 与 `final-rotation/`。

## matched-camera、inventory 与官方 3D

standard/web 各 6 张 source/render/overlay/difference 比较确认非底面五个方向的官方源锁一致。逐项 inventory 为 **30/30 matched、0 unresolved**，见 `inventory-review.json`。

2026-08-27 再次检索当前 Juniper 产品图库、硬件文档和公共索引，没有找到精确 `QFX5110-48S-AFI` 的公开官方 GLB/glTF/OBJ/FBX/STEP/STP/CAD 或交互 3D payload；没有官方模型字节可原样保留，检索更新写入 `source/optional-3d/README.md`。

底面继续使用不含臆造孔位、标签或脚垫的闭合灰色 sheet。非底面没有缺口。最终处置：**PASS_WITH_BOTTOM_FALLBACK**。
