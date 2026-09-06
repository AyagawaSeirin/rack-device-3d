# Dell PowerEdge R730 8×3.5-inch 独立复核报告

最终状态：**PASS_WITH_BOTTOM_FALLBACK**

## 身份与配置结论

- 精确产品：Dell PowerEdge R730，13G，2U；不是 R730xd、R720 或 SFF 变体。
- 锁定配置：8×3.5-inch LFF，2×4 排列，八个 carrier 均在位；前安全面板未安装；光驱和前控制区保留。
- 后部：标准 R730、无 R730xd rear flex-bay；七个 PCIe 位为空白板；iDRAC8、DB9、VGA、双 USB 3.0、四个 NDC RJ45。
- 电源：两个相同 750 W 热插拔 AC PSU，IEC 输入、橙色释放件、整体风扇均保留；无 PSU blank。
- 厂牌：正面 Dell、PowerEdge R730 和 Intel 标识均保留。
- 官方尺度：482.4 mm 耳片宽、444 mm 机身宽、87.3 mm 高、Za（无面板）18 mm、Zb 684 mm、Zc 723 mm；前最外端到后最外端 741 mm。
- GLB 实测包围盒：482.40000 × 87.30000 × 741.00003 mm。

## 冻结基线

| 项目 | SHA-256 | 大小 |
|---|---|---:|
| builder `qa/build_model.mjs` | `4c8ff08e2397e8d4cf34a372f50a0e341e639ecf6aaa4304130b9c1169a3e03d` | — |
| standard `model/Dell-R730-3.5inch.glb` | `3cd64d33d2ae498a5f1a86ca0515b226f9e1ecd0c8a24eddcea7c6a4d6995c11` | 13,050,744 B |
| web `model/Dell-R730-3.5inch-web.glb` | `cb1bc616eef8b5fd24234540c24cf6c0d393dfead616593ba0e51b53c32f1c95` | 9,024,632 B |
| 六面 PNG 集合 | `032f3daf9397ff22fec25cb3dd0d442f016b748e11cbd4d3af748cf35aa7dc46` | — |

共享 viewer/runner 完整冻结值见 `final/manifests/frozen-hashes.json`；证据再校验结果见 `final/manifests/evidence-integrity.json`。

## 根因与修复

模型侧根因：box/cylinder 原始索引绕序向内；正面上排区域和 carrier handle/latch 几何互相覆盖；闭核贴近 source card；后部 source photo、PSU relief、风扇/护罩/把手存在重复或近共面层；顶面 card/浮雕和侧面 lip/stud 深度不足。

模型侧修复：统一 outward winding 并校正 cylinder cap/side；收缩闭核；按来源像素重新划分不重叠正面控制/通风/光驱区；缩短框条和 carrier relief；保留后部 source photo，改用不相交的浅框与 PSU relief；分离风扇 hub/guard/handle、顶面浮雕、侧 lip/stud。所有照片材质为 unlit、OPAQUE、中性因子、single-sided；采样器固定 mipmap 与 clamp。standard/web 由同一 builder 同步生成。

查看器侧根因与修复与 R7515 相同：runner 查询上下文和 Babylon 连续 readback 被隔离；当前强制真实 WebGL2、固定相机/viewport/near-far、右手语义、串行截图、固定中性照明且无后处理。

## 审计结果

- `audit_views`: PASS，0 errors；5 条 warning 只来自透明轮廓抗锯齿，核心区无透明缺口。
- standard/web `audit_glb`: 均 PASS，0 errors，0 warnings；147 nodes、147 meshes、16 materials、6 embedded RGB images。
- standard/web 深审计均 PASS，2,998 个世界空间三角形实例；duplicate/exact-coplanar/near-coplanar/negative/singular/BLEND/doubleSided/primary-material/closed-core/inward/normal-mismatch/unresolved 均为 0。
- 六个面各用独立纹理而非全机 atlas；无外部 buffer，主机身不使用 BLEND。

## WebGL2 旋转与加载

- 四组合各 72 yaw + 16 pitch + 8 stability；每型号合计 288 yaw、64 pitch、32 stability，16 对重复帧逐字节相同。
- 40 次 cache-busted 独立加载 40/40 PASS，每组合 10 次；page error 0、overlay 全隐藏、实际 hash 全匹配；1,156–3,487 ms，平均 1,969 ms。
- 八张同相机四联图已核对；未见 z-fighting、纹理/alpha 跳变、开放核心、消失面、镜像、灰白跳变或混帧。

## 真实性与 inventory

- inventory 含 31 条非空实际记录（源 CSV 的额外空行不计），31/31 已逐行验证；standard/web 无非底面缺口。
- 结果：`final/inventory-verification.csv`；摘要：`final/manifests/inventory-summary.json`。
- 8LFF 2×4、无面板、七槽空白后部、四 RJ45、双 750 W AC PSU 与用户锁定截图及官方资料一致。

## 残余风险

精确底面没有可信公开资料；底面为无品牌、无脚、无导轨、无虚构孔位的受控 fallback。其余五面和配置无缺口，因此结论为 `PASS_WITH_BOTTOM_FALLBACK`，不是 BLOCKED。

## 复现

执行基础 `audit_views.py`/`audit_glb.py`、共享 `deep_glb_audit.mjs`、Playwright `run_capture.js`/`run_loads.js`，最后运行 `generate_inventory_verification.py`。具体命令与 R7515 报告相同；脚本会拒绝任何与冻结 hash 不一致的 GLB/viewer/证据。

