# FINAL REPORT — Dell-R7525-2.5inch

最终状态：**PASS**

## Final gate

- Exact identity：Dell PowerEdge R7525，15G/YX5X，2U。
- 盘型/面板：24 x 2.5-inch SFF; installed LCD security bezel; no rear drives。
- 后部配置：Risers 1-4; BOSS S2; optional DB9 in Riser 3; OCP 3.0; dual LOM; iDRAC; USB 2.0/3.0; VGA。
- 双 AC 电源：2 × 2400 W mixed-mode AC；无 PSU blank。
- Logo：DELL EMC factory mark retained。
- 官方 3D：保留 `source/optional-3d/dell-official-ar-r7525-mySceneClone.glb`，SHA-256 `4d195480b7717b92687b20a9d0e96c1cd733e3cf4e4124fc92bb11fa89dbcbff`；preserved unchanged as optional evidence; no vendor mesh copied into standard/web。

## 冻结与证据

- builder：`8ad6b5962465ae64e157ba7d30427f598810b28c969a6d809e57e4c60cd551e4`
- standard：`b12bdebef83edb474707ddb509893d8ae92c610422361c15a2c293966b567bdc`
- web：`3b1153912d8a0f6704003db0745e8aba8f85e1c4ac57e9baf79b6afd9ec209a5`
- 双 GLB 基础审计 0 errors/0 warnings；双深审计 0 unresolved。
- Three.js/Babylon.js × standard/web 四组合各 72 yaw、16 pitch、8 stability；合计 288/64/32。
- 40 次独立 cache-busted loads：40/40 PASS，每组合 10 次，page error 0，overlay 全隐藏，加载 hash 全匹配。
- Flicker：`PASS_NO_FLICKER`；16 对 stability 帧逐字节相同，8 张 matched-camera 四联图和联系人图已目检；无 z-fighting、透明跳变、泄漏、面消失、镜像、纹理切换、灰白跳变或遮罩混帧。
- Inventory：47/47 行通过，0 failure。
- 非底面缺口：0。残余风险：无。

机器可读门禁见 [FINAL-GATE.json](FINAL-GATE.json)，逐 inventory 见 [inventory-verification.csv](final/inventory-verification.csv)，完整根因、修复和复现记录见 [详细报告](final-report.md)。
