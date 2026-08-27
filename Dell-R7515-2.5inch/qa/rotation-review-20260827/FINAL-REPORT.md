# FINAL REPORT — Dell-R7515-2.5inch

最终状态：**PASS_WITH_BOTTOM_FALLBACK**

## Final gate

- Exact identity：Dell PowerEdge R7515，15G/YX5X，2U。
- 盘型/面板：24 x 2.5-inch SFF; installed security bezel; no rear drives。
- 后部配置：Riser 1B; slots 4/5; dual onboard 1GbE; dual-port LOM; iDRAC; DB9; VGA; dual USB。
- 双 AC 电源：2 × 750 W Dell EPP AC；无 PSU blank。
- Logo：DELL EMC factory mark retained。
- 官方 3D：未发现可用的 exact-model public 3D；不以近似型号替代。

## 冻结与证据

- builder：`91514dc50735e3916aa9d840120fa664b117d36346c9e4a0025a1210c9039211`
- standard：`9a25733362476989fd0947202932f7c38b5483d05df3c43be4e685987e71a47c`
- web：`aeba647e9f07f557f371fc8505313d06b8c1114f14c43dddbc7ead59f9f37996`
- 双 GLB 基础审计 0 errors/0 warnings；双深审计 0 unresolved。
- Three.js/Babylon.js × standard/web 四组合各 72 yaw、16 pitch、8 stability；合计 288/64/32。
- 40 次独立 cache-busted loads：40/40 PASS，每组合 10 次，page error 0，overlay 全隐藏，加载 hash 全匹配。
- Flicker：`PASS_NO_FLICKER`；16 对 stability 帧逐字节相同，8 张 matched-camera 四联图和联系人图已目检；无 z-fighting、透明跳变、泄漏、面消失、镜像、纹理切换、灰白跳变或遮罩混帧。
- Inventory：40/40 行通过，0 failure。
- 非底面缺口：0。残余风险：仅保守通用底面。

机器可读门禁见 [FINAL-GATE.json](FINAL-GATE.json)，逐 inventory 见 [inventory-verification.csv](final/inventory-verification.csv)，完整根因、修复和复现记录见 [详细报告](final-report.md)。
