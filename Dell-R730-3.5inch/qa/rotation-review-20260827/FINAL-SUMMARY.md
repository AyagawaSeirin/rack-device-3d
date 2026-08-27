# FINAL SUMMARY — Dell R7515 / R730 / R7525

三个目标型号均已在冻结哈希未漂移的前提下完成最终门禁；现有正式浏览器证据已严格复用，没有重复采集。

| 型号 | Exact identity | 双 AC PSU | Browser gate | Flicker | Inventory | 最终状态 |
|---|---|---|---|---|---:|---|
| Dell-R7515-2.5inch | PowerEdge R7515，15G，2U，24SFF，安全面板，无后盘 | 2×750 W EPP AC | 四组合各 72 yaw；40/40 loads | PASS_NO_FLICKER | 40/40 | PASS_WITH_BOTTOM_FALLBACK |
| Dell-R730-3.5inch | PowerEdge R730，13G，2U，8LFF 2×4，无面板，标准后部 | 2×750 W AC | 四组合各 72 yaw；40/40 loads | PASS_NO_FLICKER | 31/31 | PASS_WITH_BOTTOM_FALLBACK |
| Dell-R7525-2.5inch | PowerEdge R7525，15G，2U，24SFF，LCD 面板，无后盘 | 2×2400 W mixed-mode AC | 四组合各 72 yaw；40/40 loads | PASS_NO_FLICKER | 47/47 | PASS |

三型号双 GLB 基础审计均 0 errors/0 warnings，双深审计均 0 unresolved，非底面缺口均为 0。R7515/R730 仅保留受控通用底面；R7525 底面由未修改的官方 AR GLB 支撑，官方文件 SHA-256 为 `4d195480b7717b92687b20a9d0e96c1cd733e3cf4e4124fc92bb11fa89dbcbff`。

机器门禁与报告：

- R7515：[FINAL-GATE.json](../../../Dell-R7515-2.5inch/qa/rotation-review-20260827/FINAL-GATE.json)；[FINAL-REPORT.md](../../../Dell-R7515-2.5inch/qa/rotation-review-20260827/FINAL-REPORT.md)
- R730：[FINAL-GATE.json](FINAL-GATE.json)；[FINAL-REPORT.md](FINAL-REPORT.md)
- R7525：[FINAL-GATE.json](../../../Dell-R7525-2.5inch/qa/rotation-review-20260827/FINAL-GATE.json)；[FINAL-REPORT.md](../../../Dell-R7525-2.5inch/qa/rotation-review-20260827/FINAL-REPORT.md)

未修改 `BATCH-STATUS.md`，未 stage、commit 或 push，未触碰其他型号。
