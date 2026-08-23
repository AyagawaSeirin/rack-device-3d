# Dell PowerEdge R720 3.5 英寸最终交付报告

## 最终状态

`PASS_WITH_BOTTOM_FALLBACK`

除底面缺少可核验的精确 R720 实机来源外，既定门禁均已完成。底面仅使用通用 Dell 镀锌钢板的材质特征，主动删除所有不能由 R720 证据支持的孔位、标签、脚垫、通风、检修盖、导轨和紧固件，因此不能标为普通 `PASS`。

## 精确型号与配置锁

- Dell PowerEdge R720，2U；明确排除 R720xd、SFF 和 R730/R730xd。
- 前面板为 8 × 3.5 英寸 LFF，2 行 × 4 列，8 个托架全部安装；无安全面罩。
- 前部保留真实 DELL 与 PowerEdge R720 工厂标识、LCD/控制区、VGA、vFlash、双 USB 和光驱位。
- 后部为标准七槽 R720：3 个低矮型 + 4 个全高 PCIe 原厂挡板；iDRAC7、DB9、VGA、2 × USB 2.0、4 × RJ45 NDC。
- 电源统一为 2 个匹配的 Dell 750 W 热插拔 AC PSU；每个均有 IEC 交流输入、橙色释放件和可见风扇。无 DC 电源。
- 官方尺寸解释：机身 444 × 87.3 × 702 mm；含前锁耳和后部突出件的交付边界 482.4 × 87.3 × 741 mm。

## GLB 交付物

| 配置 | 文件 | 大小 | SHA-256 |
|---|---|---:|---|
| standard | `model/Dell-R720-3.5inch.glb` | 19,085,704 字节（18.20 MiB） | `ed797eeae6d3daf3fb553479fe1b4a8e92157e383bd69596b4d9c5adfc8b64cf` |
| web | `model/Dell-R720-3.5inch-web.glb` | 11,344,552 字节（10.82 MiB） | `3fb84bc99c2164863f1fdecf2fcb035be5e1010872efe8b6cd76e0e04947ce0b` |

两份均为本项目自制 GLB，不是官方模型的替代封装。两者都包含完整闭合机身、六面照片材质、8 个 LFF 托架的独立可见轮廓、七槽后部轮廓、后把手、双 PSU 突出结构、前锁耳闭合结构、非镜像左右侧细节与顶盖细节。模型使用右手坐标：从正面看 +X 向设备右、+Y 向上、+Z 向前。

## 六面源锁

六个最终透明 PNG 均有独立来源与生成记录；左右侧未镜像。完整来源路径、输入 SHA-256、锁定特征、最终输出路径和最终 SHA-256 在 `source/face-source-lock.csv`。

- 前：用户配置锁 + 官方手册 + 精确 8-LFF 实机照。
- 后：用户配置锁 + 官方标准 R720 七槽图 + 精确实机后照。
- 左：直接 R720 左侧实机照，前端在图像右侧。
- 右：独立的相反侧实机照，前端在图像左侧；不复制左侧标签和孔位。
- 顶：多张精确 8-LFF 三分之四照片与官方尺寸共同重建。
- 底：经完整检索仍无精确 R720 底面，采用受控 `GENERIC_BOTTOM_FALLBACK`。

透明素材审计为 `PASS`。前、后、右三张存在 3 条边缘提示，已逐张原尺寸检查：仅为轮廓/真实开孔抗锯齿像素；机身内核透明率为 0 或近似 0，不构成漏透明。

## 模型与 WebGL 门禁

- standard GLB 技能审计：`PASS`，0 error / 0 warning。
- web GLB 技能审计：`PASS`，0 error / 0 warning。
- 配置/结构审计：45/45 `PASS`；每份 121 个节点、121 个网格、8 张嵌入图片、0 个外链资源、0 个镜像节点。
- standard 与 web 的节点名、材料名和结构计数一致；差异仅为网站纹理优化。
- Three.js 实载：standard 10/10，web 10/10。
- Babylon.js 实载：standard 10/10，web 10/10。
- 合计 40 张真实 WebGL 加载渲染，全部为 1600 × 1200；每份 GLB 均覆盖前、后、左、右、顶、底六正交视角和前左、前右、后左、后右四斜视角。
- 两引擎与两配置的逐视角交叉检查全部 `PASS`。最大 standard/web 平均 RGB 差值小于 0.56/255；最大 Three.js/Babylon.js standard 平均差值为 3.23/255（底面光照/金属表现差异），外观与方向一致。

主要证据：

- `qa/views-audit.json`
- `qa/glb-standard-audit.json`
- `qa/glb-web-audit.json`
- `qa/structure-audit.json`
- `qa/webgl-render-audit.json`
- `qa/comparison-table.csv`
- `qa/comparisons/`
- `qa/renders/`
- `qa/manifest.csv`

## 官方公开精确 3D 情况

结果为 `NOT_FOUND_AFTER_EXHAUSTIVE_PUBLIC_SEARCH`。已检查 Dell 支持/文档及精确型号的 3D、CAD、AR、GLB、glTF、STEP、OBJ、FBX、BIM、Visio 等公开入口，没有找到官方可下载的精确 R720 8-LFF 三维文件或官方互动模型。因此 `source/optional-3d/` 仅保留完整检索记录，没有可原样备份的官方二进制文件；这不影响两份自制 GLB 的完成。

## 剩余风险

1. 精确 R720 底面实机照片/工程图仍未找到，底面是明确披露的保守 fallback。
2. 六面照片主材质是依据已检查的官方图、用户配置锁和实机照片进行的 source-locked AI 重建，不是 Dell 工厂 CAD 或同一台实机的六相机直接摄影。
3. 未发现官方精确 3D，因此模型几何是基于官方尺寸与可见外观证据的重建，而非 OEM 网格。

本任务未执行 Git commit 或 push。
