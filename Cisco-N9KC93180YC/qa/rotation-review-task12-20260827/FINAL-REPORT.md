# Cisco-N9KC93180YC Task-12 旋转与真实性复核

最终任务状态：**PASS_WITH_BOTTOM_FALLBACK**  
锁定身份：**Cisco Nexus 9000 N9K-C93180YC-FX Chassis**  
模型/查看器质量状态：**PASS**  
复核日期：2026-08-27（Asia/Singapore）
验收口径修正：2026-08-28（Asia/Singapore）

## 结论与验收口径

standard/web 的几何、材质、六面、旋转、独立加载和真实性均已因果修复并通过全部技术门禁。总控在 2026-08-28 明确：所有设备的共通要求是 AC；`NXA-PAC-1100W-PI2` 与 `NXA-FAN-65CFM-PI` 是紧接 C9336C-FX2 未完成问题给出的精确 FRU 约束，只适用于 C9336C-FX2，不约束本型号。

最终 GLB 正确保留 `N9K-C93180YC-FX` 真实兼容的 2 × `NXA-PAC-500W-PI` AC PSU + 4 × `NXA-FAN-30CFM-PI` intake fan 配置。没有安装 1100W PI2/65CFM PI，是因为其模块尺寸、三风扇槽位和后部架构属于 C9336C-FX2，强装或重标会破坏 93180YC-FX 的精确性。该排除是正确的兼容性处理，不构成阻塞。唯一缺口仍是精确底面证据，因此最终状态为 **PASS_WITH_BOTTOM_FALLBACK**。

修复前模型、构建器、六面、审计、加载证据和旧报告已在修改前归档到 `qa/superseded/pre-rotation-review-20260827/`，未覆盖原文件。

## 冻结哈希

| 产物 | 修复前 SHA-256 | 最终 SHA-256 | 最终字节数 |
|---|---|---|---:|
| standard GLB | `0d6f8bbfd0993a33014b887ab6c4deabbb94b7a01c79abcecc9c57b04a3e740a` | `e12c36ec0b7c803edba7a1fa886a749b058f4d29b831ebcd6b40ce9d06ca172c` | 8,440,568 |
| web GLB | `e15f5488d4c5eadfeebb00e2056fc49194fe755ff20524aa344d3bc44ab5ff7e` | `7d3f9e81ae32da28b1c0c313cf2ecccf4dcc13ab5cc87bb997f9923041da242c` | 6,277,940 |
| 构建器 | `f094fe…b530` | `9043e117e01eae87fe9877b3b32d296f226117f74806a702df72b14fea701db7` | 以 `hash-freeze.json` 为准 |

最终可见 bounds 为 482.6 × 44.8 × 582.25 mm；官方机身本体仍单独记录为 439 × 44 × 571 mm，前耳和后把手突出量不与本体尺寸混淆。

## 复现、根因与修复

### 模型根因

修复前模型在前面同时存在连续照片条、分块照片卡、连续 QSFP 卡和几何 relief，部分层间只有约 0.01–0.02 mm，另有完全共面的相邻贴片；标准 GLB 还嵌入 RGBA 主面纹理。补充审计在两个层级均定位到可见近共面/alpha 风险。这是旋转时闪烁/透明错觉的模型深度根因，不是照明。

修复后仅保留一个源锁底面，端口贴片改为相互独立且有确定 clearance 的 patch，连续重叠卡被移除，latch relief 位于明确前层；standard/web 都嵌入 RGB-only 主纹理，web 面纹理提升至技能下限。六个主面全部为 `OPAQUE`、`[1,1,1,1]`、`doubleSided=false`，机身无 `BLEND`。

### 方向与六面根因

旧构建器元数据声明 `+X=device right`，但物理 left/right 纹理与 relief 实际放反，旧静态查看器又用反向相机把错误暂时遮住。本轮将纹理、侧槽、接地点和 fastener 全部交换到规范坐标，并同步纠正两个旧查看器。旧 top/bottom 还是含前耳的透视比例，错误地按 482.6:571 使用；已从已归档原图机械整流为 439:571 的正交机身投影，top 保留真实标签/盖板/通风，bottom 明确为无臆造细节的保守回退。

### 查看器根因

共享 Three.js 正交查看器的固定 distance/far 只适合米制 QFX，对毫米制 Cisco 会裁剪为空画面。无效证据已归档，动态 bounds 修复后 standard/web 六面全量重采。Babylon loading UI 被禁用，采集队列等待模型稳定，不存在 overlay 混帧。

## 审计与真实 WebGL2 门禁

- 六面：PASS，0 errors；6 个 alpha warning 均经 matched-camera/正交图复核为外轮廓 AA 或真实开孔，core alpha 为 0，最终 0 unresolved。
- standard/web `audit_glb`：PASS，0 errors，0 warnings。
- standard/web 补充结构审计：PASS；material-alpha、embedded-image、sampler、negative-transform、degenerate、duplicate、opposite、未解决可见近共面、缺失 normal 均为 0；closed-core 与 winding-consistency=true。
- 独立加载：2 引擎 × 2 层级 × 10 视角 = **40/40**，全部 cache-busted、WebGL2、冻结哈希/字节命中、主材质 OPAQUE。
- 旋转：4 组合各 72 × 5° yaw，共 **288 yaw 帧**；16 个俯仰帧；12 个同角度稳定帧；合计 **316 帧**。稳定帧逐字节相同。
- 人工目检未见闪烁、透明跳变、泄漏、面消失、镜像、纹理/灰白跳变或遮罩混帧。

技术证据总表见 `final-validation.json`。

## matched-camera、inventory 与真实性

standard/web 各 6 张 source/render/overlay/difference 表确认：48 SFP/SFP28 + 6 QSFP/QSFP28、前耳、四风扇/两 PSU、管理区顺序、左右不同侧板和整流 top 都与有效 FX 源锁一致。`feature-inventory.csv` 的 **15/15 行 matched、0 unresolved**；Task-12 配置冲突为 0。兼容性说明单独记录于 `inventory-review.json`。

真实 Cisco/Nexus/PID/模块颜色与方向均保留；没有把 C9336C-FX2 的不兼容 FRU 塞入或重标到本机箱。

## 官方 3D 检索与残余风险

2026-08-27 重查 Cisco 官方支持/指南和公共索引，未发现精确 `N9K-C93180YC-FX` 的公开官方 GLB/glTF/OBJ/FBX/STEP/STP/CAD 或交互 3D 包；没有官方 3D 字节可原样保留。搜索记录见 `source/official-3d-search-log.md`。

底面仍是唯一图像证据 fallback：使用不含臆造孔位、标签、脚垫或导轨的保守闭合板。非底面没有未解决缺口；冻结 GLB、40 次独立加载和 316 帧旋转证据均保持有效。最终处置：**PASS_WITH_BOTTOM_FALLBACK**。
