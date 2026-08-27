# Dell PowerEdge R620 2.5-inch / 10SFF 最终报告

## 结论

**PASS_WITH_BOTTOM_FALLBACK**

两份必需的自制 GLB 已完成并通过身份、配置、尺寸、六面、结构、材质、双 WebGL 和视觉门禁。锁定对象为 Dell PowerEdge R620 1U 十盘位机箱：10 × 2.5 英寸 SFF，2 × 5 排列，十个托架均安装，无安全面板；十盘位专属三低矮 PCIe 槽后部；iDRAC7、DB9、VGA、2 × USB 2.0、4 × Base-T RJ45；两只相同 Dell 750W 热插拔 AC PSU。真实 DELL 与 PowerEdge R620 标识已保留。

唯一的限定项是底面。依照技能顺序穷尽 Dell 官方、手册、实机、视频、二手渠道及中英文检索后，未找到可验证的精确 R620 底面，因此使用不带虚构孔位、脚垫、标签、导轨或 Logo 的保守镀锌钢板 `GENERIC_BOTTOM_FALLBACK`。

## 交付文件

| 文件 | 大小 | SHA-256 | 结果 |
|---|---:|---|---|
| `model/Dell-R620-2.5inch.glb` | 16,096,672 bytes（15.35 MiB） | `ef61dfa7b5765bb565a81b26d464ca9f2bd7f2b5cf2224a20c3fabbf6b33bbfe` | PASS |
| `model/Dell-R620-2.5inch-web.glb` | 9,283,536 bytes（8.85 MiB） | `0fcb1b0adb4fe9199ba183eae01265c48c14d5a186e8e41e11e7d8ccfee71d96` | PASS |

两份文件均从零自制；没有复制、改包或用任何官方/第三方模型替代。

## 尺寸与结构

- 官方名义安装包络：482.4 × 42.8 × 752.1 mm（X/Y/Z）；主体 434.0 × 42.8 × 731.0 mm。
- GLB 审计实测：482.400 × 42.850 × 752.515 mm，比例误差 0.0595%，在技能容差内。
- 每份 GLB：297 nodes、297 meshes/primitives、18 materials、6 textures、6 unique base-color images。
- 两份 GLB 的结构、节点名和材质名一致；无镜像节点、无外部资源。
- 可见几何包括：封闭机箱核心、两只前把手/耳、十套独立 SFF 盘位/托架/把手/孔/释放环/状态灯、控制条、三块低矮 PCIe 挡板、独立后部端口、两套完整 750W AC PSU、左右独立挂钉/槽/接缝、顶盖锁扣和通风凹槽。
- GLB 两次技能审计与结构审计均为 0 错误；六面图审计为 0 错误、0 警告。

## 六面锁定

| 面 | 模式 | SHA-256 | 结果 |
|---|---|---|---|
| Front | `SOURCE_LOCKED_GENERATION` | `e379d0f6ed39807d65a52d77cc1ab2895ea90cdee3424a49120f57eb0ec55097` | PASS |
| Rear | `SOURCE_LOCKED_GENERATION` | `0a1c84203f230542846e91328b55c887d6fb0b4c2aaff84206ce989c0a481c0b` | PASS |
| Left | `MULTI_REFERENCE_RECONSTRUCTION` | `3df448319b241ef714948ea749d27138bbe4bc582513c02522cfb3748d833263` | PASS |
| Right | `MULTI_REFERENCE_RECONSTRUCTION` | `e724b21a096aa77d772b7366c3e42dd6cddac2e9fb89a9bdfbebc51f5172f0d3` | PASS |
| Top | `SOURCE_LOCKED_GENERATION` | `d69b58769482dbca2db772cb55f2d9e06ff499b58211c202b6e5f3c351c29f43` | PASS |
| Bottom | `GENERIC_BOTTOM_FALLBACK` | `b16065b8a83eee21aa8993411c8178a130011ca0a86d7a26067e4b1d40c91c67` | FALLBACK |

六个面来自六次独立生成链；左右分别锁定物理 -X/+X 实机证据并使用独立图像，没有镜像。最终图在去背景后只做官方物理比例归一化，原始生成、中间图、提示词与拒绝版本均留在 `qa/reference/`、`qa/imagegen-prompts/`。

## 双 WebGL 门禁

最终 GLB 重建后重新执行完整实载：

- Three.js：20 次。
- Babylon.js：20 次。
- Standard GLB：20 次。
- Web GLB：20 次。
- Front、rear、left、right、top、bottom、front-left、front-right、rear-left、rear-right：每个视角 4 次。

结果为 **40/40 真实页面状态与截图加载**，全部 `loaded=true`、`error=null`，包络一致，无恢复或推断事件。浏览器为 Chromium 151.0.7922.34。最终证据包含 40 个原子事件 JSON、40 张截图、40 张参考/渲染对照图和 4 张十视角拼图。

## 官方 3D 状态

未找到可公开下载、来源可验证且精确匹配 Dell PowerEdge R620 10SFF 安装配置的官方 GLB/glTF/OBJ/FBX/STEP/CAD。完整检索范围和阴性结果保存于 `source/optional-3d/README.md`；没有把第三方或 AI 重建文件标作官方，也没有用可选模型替代自制 standard/web GLB。

## 核心证据与门禁文件

- `qa/audit.json`：最终机器可读总门禁。
- `qa/glb-standard-audit.json`、`qa/glb-web-audit.json`：两份 GLB 结构/尺寸/材质审计。
- `qa/structure-audit.json`：身份、节点、可见配置与双版本结构一致性审计。
- `qa/views-audit.json`：六面分辨率、比例、透明度审计。
- `qa/feature-acceptance.md`：可见特征到几何/视觉证据验收矩阵。
- `qa/load-evidence/summary.json`、`final-load-events.ndjson`：40 次真实加载汇总与逐项证据。
- `qa/renders/final/`、`qa/comparisons/final/`、`qa/contact-sheets/`：最终实载截图、对照图和拼图。
- `source/identity-manifest.md`、`face-source-lock.csv`、`evidence.md`、`bottom-search-log.md`：身份、来源与 fallback 追溯。

## 剩余风险

1. 底面是证据约束下的保守 fallback，不是经实机确认的精确 R620 底面。
2. 左右侧与部分顶面细节由精确实机照片和官方图示重建，不是官方 CAD。
3. 生成的源锁定面在去背景后做了官方尺寸比例归一化；极小标签文字只用于外观表达，不应视作工程级可读数据。
4. 这是网站用外观副本，不是内部结构或工程 CAD。
5. 没有可用于网格对网格比较的精确官方安装配置模型。

本任务未执行 `git commit` 或 `git push`，且未修改其他型号目录。
