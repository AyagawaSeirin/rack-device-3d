# Dell PowerEdge R7515 3.5 英寸网站用 3D 模型最终报告

> 当前验收以 `qa/rotation-review-20260827/final-report.md` 及其冻结哈希 `final-gate.json` 为准；本旧报告仅保留作谱系证据。

## 最终结论

**PASS_WITH_BOTTOM_FALLBACK**

九项最终门禁全部通过，失败项为 0。唯一受控降级是底面：在完成官方资料、产品页、经销商图库、多语种图片/视频及官方 3D/CAD/AR 路径检索后，仍未找到可用的精确 R7515 底面影像，因此按技能契约使用保守、无识别性、无虚构孔位/标签的 `GENERIC_BOTTOM_FALLBACK`。除此之外，身份、尺寸、前后配置、双 AC 电源、品牌、独立左右面、GLB 结构和双 WebGL 实载均通过。

## 锁定身份与外廓

- Dell Technologies / Dell EMC **PowerEdge R7515**，2U。
- 前面为 **12 × 3.5 英寸 LFF**，3 行 × 4 列，12 个托架全部安装，不装安全面板。
- 后面为 **无后置硬盘笼**版本：Riser 1B 槽位 2/3、PCIe 4/5、系统 I/O 与 OCP/LOM 区域。
- 电源统一为 **两只热插拔 EPP 750W AC PSU**，上下堆叠；未混入 DC/HVDC 或 1100W 标识。
- 保留可见的 DELL / DELL EMC、PowerEdge、R7515、EPP 750W 身份标识；没有添加后耳或中央面板 Logo。
- 精确最终外廓：**482 × 86.8 × 703.755 mm**；机身宽 434 mm，机身深 647.07 mm，无面板前伸 22 mm，后部超出机身 34.685 mm。

## 最终 GLB

| 版本 | 文件 | 字节数 | 约合 | SHA-256 |
|---|---|---:|---:|---|
| standard | `model/Dell-R7515-3.5inch.glb` | 18,850,044 | 17.977 MiB | `06b20f03ccc702fddb0dec854f37f60f4a4c14761488b3b58591bc7824b90f55` |
| web | `model/Dell-R7515-3.5inch-web.glb` | 10,604,860 | 10.114 MiB | `692020e5444f1f071f340a6f3b4908d8e4eef60ee570471bd1f3103496ec1f76` |

两份均为本项目自制外观模型，不是官方 CAD 的转换或替代品。每份含 163 个节点、163 个网格、163 个 primitive、13 个材质和 6 张内嵌底色纹理；法线与 UV 完整，材质为 OPAQUE，纹理引用为内嵌资源，无外部 buffer、无负尺度/镜像节点。技能 GLB 审计结果均为 `PASS`、0 error、0 warning，实际量得外廓与目标一致，三个轴单位比例误差为 0。

## 六面来源锁与图像生成

六面均由六次相互独立的 imagegen 调用生成，没有用左面镜像右面，也没有用顶面复制底面：

| 面 | 模式 | 主要锁定依据 |
|---|---|---|
| front | `SOURCE_LOCKED_GENERATION` | 精确 12-LFF 正面实拍 + 用户行锁 + Dell 官方正面 |
| rear | `SOURCE_LOCKED_GENERATION` | 精确无后盘、双 EPP 750W AC 后面实拍 + Dell 官方后面 |
| left | `SOURCE_LOCKED_GENERATION` | 直接左侧正投影实拍 + Dell 左侧结构图 |
| right | `MULTI_REFERENCE_RECONSTRUCTION` | 独立右侧/斜视实拍 + Dell 右侧结构图 |
| top | `MULTI_REFERENCE_RECONSTRUCTION` | 两个独立顶面斜视 + Dell 顶盖图与尺寸图 |
| bottom | `GENERIC_BOTTOM_FALLBACK` | 官方外廓尺寸 + 两侧可证实折边，仅作保守底面 |

原始品红底结果、抠图中间件、最终面、每一步 SHA-256、输入角色和逐面提示词分别保存在 `qa/work/imagegen-raw/`、`qa/work/imagegen-keyed/`、`views/`、`qa/imagegen-generation-manifest.csv` 与 `qa/imagegen-prompts/`。`source/face-source-lock.csv` 已绑定最终输出哈希。左右最终哈希不同，孔位、压筋与前后方向也经两查看器斜视确认独立。

## 可见几何与修复结果

- 正面：12 个独立托架/盘位/把手/锁扣/指示灯几何，两个独立控制翼；实拍纹理保留真实控制端口与 PowerEdge R7515 标识。
- 后面：以完整精确来源纹理绑定端口和板卡布局，只以薄框提供插槽/格栅起伏，避免通用几何遮挡真实端口；双 PSU 有独立壳体厚度、风扇环和橙色锁扣，真实 EPP 750W 风扇、C14 和把手保持可见。
- 顶面：独立顶盖、固定标签区、释放锁扣、后部通风条与接缝；修复了纹理面与顶盖几何共面引起的闪烁/白块。
- 左右面：独立纹理、孔位、压筋和轨道槽几何，无镜像节点。
- 六面纹理 V 方向已校正；正面电源按钮、后面串口/VGA 以及顶盖前后方向在两个引擎中一致。

掉线前的旧模型、旧结构审计和 48 次旧实载截图已保存在 `qa/repair-before/pre-final-visual-repair/`，没有覆盖或丢弃；最终报告只引用修复后重新执行的证据。

## 双 WebGL 最终实载

最终证据为 **48/48 PASS**，不是沿用修复前截图：

- 查看器：Three.js 24 次、Babylon.js 24 次。
- 模型：standard 24 次、web 24 次。
- 每个“查看器 × 模型”组合：前、后、左、右、顶、底六个正交视角，front-left、front-right、rear-left、rear-right 四个斜视，以及 front-logo、rear-psu 两个身份/电源特写，共 12 次。
- 40 次法定矩阵（六正交 + 四斜视）之外，另有 8 次 Logo/PSU 特写，合计 48 次。
- 48 个 QA ID 均唯一；全部通过真实 WebGL 加载并回报 PASS，边界均为 0.482 × 0.0868 × 0.703755 m。
- QA 服务器为每次加载重新计算磁盘 GLB 字节数与 SHA-256；48 条记录全部只出现上述两组最终哈希。
- 最终实载区间：2026-08-23 17:55:21 至 18:03:24 UTC。

48 张 1280 × 720 截图在 `qa/renders/`；四张完整接触表和总览在 `qa/contact-sheets/`。另有 **24 张**同相机“参考 / 实载 / 50% 叠加 / 差异”图（两查看器 × 两模型 × 六正交面）在 `qa/comparisons/`。逐面检查未发现模型缺失、纹理倒置、后端口重复、PSU 遮挡、顶盖白块、左右镜像或品牌丢失。

## 官方精确 3D 情况

未找到公开且精确匹配 R7515 12-LFF / 无后置盘 / 双 750W AC 配置的官方 GLB、glTF、CAD 或 AR 二进制。Dell 产品与 `resources/3dguides` 实际浏览器路径返回 Akamai HTTP 403；公开搜索索引也未暴露精确文件。没有尝试绕过访问控制，也没有拿 R7525、SFF 或其他后板模型冒充。由于不存在可合法取得的精确二进制，`source/optional-3d/` 中保存的是完整检索记录而不是替代模型。

## 最终门禁与剩余风险

`qa/final-audit.json` 的九项门禁全部 PASS：精确尺寸/构建清单、standard/web 结构、六面 PNG、六次独立来源锁、48 次双 WebGL 实载、截图与对比图、精确变体/统一 AC、官方 3D 检索、底面检索与受控 fallback。

剩余风险：

1. 精确底面资料仍不可得，底面仅为保守、无识别性 fallback；这也是最终状态不是普通 PASS 的唯一原因。
2. 表面纹理是来源锁定的生成式重建而非摄影测量；极小紧固件、金属纹理和微小标签可读性仍可能与个别实物批次有细微差异，但绑定的数量、布局、方向、配置和身份已核验。
3. 这是网站展示用外观副本，不是工程 CAD；内部结构、加工公差与维修级装配不在范围内。
4. 未发现公开官方精确 3D 不等同于证明 Dell 内部或受限渠道完全不存在该资产。

## 关键审计文件

- `qa/final-audit.json`：最终九门禁机器可读汇总。
- `qa/viewer-load-evidence.json`：48 次实载、模型哈希、字节数、WebGL 和边界证据。
- `qa/glb-audit-standard.json` / `qa/glb-audit-web.json`：两份 GLB 的结构与资源审计。
- `qa/views-audit.json`：六面尺寸、透明度和受控侧面边缘警告处理。
- `source/identity-manifest.md`、`source/evidence.md`、`source/feature-inventory.csv`、`source/dimension-ledger.csv`：身份、证据、特征和尺寸锁。
- `source/optional-3d/README.md`、`source/bottom-search-log.md`：官方 3D 与底面检索结论。

未执行 git commit 或 push。
