# Dell PowerEdge R7525 24×2.5-inch 独立复核报告

最终状态：**PASS**

## 身份与配置结论

- 精确产品：Dell PowerEdge R7525，15G/YX5X，2U，双路 AMD 机型；未混入 R7515/R750/R730。
- 锁定配置：24×2.5-inch SFF，二十四个 portrait carrier；Dell EMC LCD security bezel 安装；无后置盘笼。
- 后部：Riser 1–4/BOSS S2、Riser 3 可选 DB9 serial、OCP 3.0、双 RJ45 LOM、iDRAC、USB 2.0/3.0、VGA，与锁定后视一致。
- 电源：两个相同 2400 W mixed-mode PSU 作为 AC 电源使用，双 IEC-C20 输入、双风扇/把手/橙色释放件；无 PSU blank。
- 厂牌：正面 source-locked DELL EMC 标识保留。
- 官方尺度：482 mm 耳片宽、434 mm 机身宽、86.8 mm 高、Za 35.84 mm、Zb 700.7 mm、Zc 736.29 mm；安装总深 772.13 mm。
- GLB 实测包围盒：482.00000 × 86.80000 × 772.13000 mm。

## 冻结基线

| 项目 | SHA-256 | 大小 |
|---|---|---:|
| builder `model/build-model.js` | `8ad6b5962465ae64e157ba7d30427f598810b28c969a6d809e57e4c60cd551e4` | — |
| standard `model/Dell-R7525-2.5inch.glb` | `b12bdebef83edb474707ddb509893d8ae92c610422361c15a2c293966b567bdc` | 10,863,692 B |
| web `model/Dell-R7525-2.5inch-web.glb` | `3b1153912d8a0f6704003db0745e8aba8f85e1c4ac57e9baf79b6afd9ec209a5` | 6,448,932 B |
| 六面 PNG 集合 | `db9bedc9da95b61981e7baf0744bef2522ddb30867a14caf6e36d1b26530370d` | — |

共享 viewer/runner 完整冻结值见 `final/manifests/frozen-hashes.json`；证据完整性见 `final/manifests/evidence-integrity.json`。

官方 public 3D 原件 `source/optional-3d/dell-official-ar-r7525-mySceneClone.glb` 保持未修改：18,454,132 B，SHA-256 `4d195480b7717b92687b20a9d0e96c1cd733e3cf4e4124fc92bb11fa89dbcbff`。它只作为全角度/底面证据，没有把厂商 mesh 复制进自建 standard/web。

## 根因与修复

模型侧根因：cylinder side/cap 绕序与法线不一致；hex ring 内外壁绕序/共享法线错误；闭核和顶/底 source card 近共面；bezel rail/hex/LCD/button、rear riser/port relief 和 PSU fan blade 存在重复或近共面；通用方块会遮盖 source-locked 后部细节；闭核一度被并发构建换成 8 顶点平滑法线核心。

模型侧修复：重写 cylinder cap ring 和 hex ring 面/硬法线；用外向、分面法线的几何闭核并留 card clearance；缩小/错开 bezel lattice、rail、LCD、button、carrier backing；后部改为不交叠 source frame；用独立 UV photo patch 保留双 PSU 细节，移除全直径重复 fan blades；serial/riser/port relief 逐层错开；standard/web 同因果重建。并发产生的平滑核心版本和失效帧都已保存在 superseded。

查看器侧根因与修复同前两型号；此外 Dell live AR 页本身曾出现 WebGL 资源警告/崩溃，属于厂商 viewer 场景问题，不影响已保存官方原件或自建 GLB。当前证据只使用冻结的独立 Three/Babylon harness。

## 审计结果

- `audit_views`: PASS，0 errors；6 条 warning 仅为轮廓抗锯齿，核心透明度在阈值内。
- standard/web `audit_glb`: 均 PASS，0 errors，0 warnings；250 nodes、25 shared meshes、17 materials、7 embedded RGB images。
- standard/web 深审计均 PASS，6,642 个世界空间三角形实例；duplicate/exact-coplanar/near-coplanar/negative/singular/BLEND/doubleSided/primary-material/closed-core/inward/normal-mismatch/unresolved 均为 0。
- 六个主面 OPAQUE、`[1,1,1,1]`、single-sided、unlit；每面独立纹理，mipmap+clamp，无全机 atlas 切换。
- 官方 AR GLB 的通用生产审计为 REWORK（厂商场景含 BLEND/MASK/double-sided，且场景轴向/总装 bounds 不符合当前交付尺度）；因此保持原件而不替换自建 production GLB。这不是 current standard/web 的 unresolved。

## WebGL2 旋转与加载

- 四组合各 72 yaw + 16 pitch + 8 stability；每型号合计 288 yaw、64 pitch、32 stability，16 对重复帧逐字节相同。
- 40 次 cache-busted 独立加载 40/40 PASS，每组合 10 次；page error 0、overlay 全隐藏、实际 hash 全匹配；986–3,147 ms，平均 1,852 ms。
- 八张同相机四联图和深/浅棋盘联系人图已目检；无闪烁、透明跳变、泄漏、消失面、镜像、纹理切换、灰白跳变或遮罩混帧。
- 21:42 的中途模型变更被 Babylon hash guard 当场拒绝；当时 194 个文件整体归档到 `superseded/pre-model-hash-change-20260827T214229/`，其后所有四组合从第 1 帧全量重跑。

## 真实性与 inventory

- inventory 含 47 条非空实际记录，47/47 已逐行验证；没有底面 fallback，也没有非底面缺口。
- 结果：`final/inventory-verification.csv`；摘要：`final/manifests/inventory-summary.json`。
- 底面为官方 AR GLB 支撑的 `MULTI_REFERENCE_RECONSTRUCTION`，仅保留官方可见的银色壳体、接缝和保守 relief，不复制顶面、不发明脚/导轨/标签。

## 残余风险

官方 public AR 是复杂 vendor scene，并非满足本项目材质/尺度契约的 production GLB；它只能作为证据。自建 standard/web 本身无已知残余缺口，最终状态为 `PASS`。

## 复现

执行基础 `audit_views.py`/`audit_glb.py`、共享 `deep_glb_audit.mjs`、Playwright `run_capture.js`/`run_loads.js`，最后运行 `generate_inventory_verification.py`。脚本会逐项校验 builder、双 GLB、viewer、四份 rotation manifest、16 对重复帧和 40 条 load hash，任何不一致即停止。

