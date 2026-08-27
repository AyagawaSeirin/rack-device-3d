# FINAL REPORT — Dell-R730-3.5inch

最终状态：**PASS_WITH_BOTTOM_FALLBACK**

## Final gate

- Exact identity：Dell PowerEdge R730，13G，2U。
- 盘型/面板：8 x 3.5-inch LFF in 2 x 4; no front security bezel; no R730xd rear flex-bay。
- 后部配置：standard seven-slot R730 rear; iDRAC8; DB9; VGA; dual USB 3.0; four NDC RJ45。
- 双 AC 电源：2 × 750 W AC；无 PSU blank。
- Logo：Dell and PowerEdge R730 factory marks retained。
- 官方 3D：未发现可用的 exact-model public 3D；不以近似型号替代。

## 冻结与证据

- builder：`4c8ff08e2397e8d4cf34a372f50a0e341e639ecf6aaa4304130b9c1169a3e03d`
- standard：`3cd64d33d2ae498a5f1a86ca0515b226f9e1ecd0c8a24eddcea7c6a4d6995c11`
- web：`cb1bc616eef8b5fd24234540c24cf6c0d393dfead616593ba0e51b53c32f1c95`
- 双 GLB 基础审计 0 errors/0 warnings；双深审计 0 unresolved。
- Three.js/Babylon.js × standard/web 四组合各 72 yaw、16 pitch、8 stability；合计 288/64/32。
- 40 次独立 cache-busted loads：40/40 PASS，每组合 10 次，page error 0，overlay 全隐藏，加载 hash 全匹配。
- Flicker：`PASS_NO_FLICKER`；16 对 stability 帧逐字节相同，8 张 matched-camera 四联图和联系人图已目检；无 z-fighting、透明跳变、泄漏、面消失、镜像、纹理切换、灰白跳变或遮罩混帧。
- Inventory：31/31 行通过，0 failure。
- 非底面缺口：0。残余风险：仅保守通用底面。

机器可读门禁见 [FINAL-GATE.json](FINAL-GATE.json)，逐 inventory 见 [inventory-verification.csv](final/inventory-verification.csv)，完整根因、修复和复现记录见 [详细报告](final-report.md)。
