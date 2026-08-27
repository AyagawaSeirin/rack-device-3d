# Dell PowerEdge R7515 2.5 英寸网站用 3D 模型最终报告

## 最终结论

**最终状态：`PASS_WITH_BOTTOM_FALLBACK`**

两份自制 GLB、六个独立源锁定面、精确变体身份、统一双 AC 电源配置、品牌标识、两套独立 WebGL 查看器实载、六正交与四斜视目检、结构审计及最终证据清单均已完成。唯一降级项是：经过完整检索仍未获得可验证的 R7515 精确底面照片，因此底面按技能规定采用受控的 `GENERIC_BOTTOM_FALLBACK`，最终状态不得写成无条件 `PASS`。

最终关闭日期：2026-08-24（Asia/Singapore）。未执行 Git commit 或 push。

## 精确型号与安装配置

- 产品：Dell Technologies / Dell EMC PowerEdge R7515，2U，Regulatory Model E46S / Type E46S003。
- 前部：24 × 2.5 英寸 SFF，24 个载架/挡片面全部存在；安装原厂 Dell 2U 安全面板，13 个交错大六边形开口；保留居中的原厂 `DELL EMC` 标识。
- 后部：无后置硬盘笼；Riser 1B；两块水平槽挡片、两块竖直 PCIe 挡片；LOM、板载网口、iDRAC、USB、串口、VGA 的位置与证据锁一致。
- 电源：两只独立、上下堆叠的 Dell EPP 750 W 热插拔 **AC** PSU，均有 IEC AC 输入、风扇与绿色 `EPP 750W` 标识；没有 DC/HVDC 面、单 PSU 挡片或混合电源。
- 明确排除：R7525、所有 3.5 英寸/LFF 前部、后置硬盘配置、DC/HVDC PSU、单 PSU、去除安全面板的最终状态。

身份清单位于 `source/identity-manifest.md`，状态为 `VERIFIED`；证据链位于 `source/evidence.md`。

## 交付模型

| 构建 | 文件 | 大小 | SHA-256 |
|---|---|---:|---|
| standard | `model/Dell-R7515-2.5inch.glb` | 17,680,308 字节（约 16.86 MiB） | `1d6614f4f869c3daefd59f13655a85435deb935f19c1949aad43af5faea51c78` |
| web | `model/Dell-R7515-2.5inch-web.glb` | 8,114,260 字节（约 7.74 MiB） | `2c01f2405f0562b86ad2d78b3849e01723748e3816aa59f056697d797e62cb54` |

web 版本比 standard 版本小约 54.1%，但保留相同几何、节点、材质槽位、朝向、轮廓和可见配置；区别仅为纹理预算。

两份 GLB 的共同结构：

- 118 个节点、118 个网格、118 个 primitive、1,526 个顶点、2,614 个三角形；Three.js 运行时连场景根节点共报告 119 nodes。
- 13 个材质、9 个内嵌纹理/图像；所有材质为 `OPAQUE`。
- 无外部 buffer、纹理或其他运行时依赖；无镜像节点；GLB 可独立加载。
- 实测总包围盒：482.000 × 87.100 × 717.805 mm。
- 官方目标：482.000 × 86.800 × 717.595 mm；偏差分别为 0.000、+0.300、+0.210 mm，均通过最终尺寸门禁。

构建清单位于 `model/build-manifest.json`，可编辑构造源位于 `model/build_model.py`。

## 六面源锁与 imagegen 记录

六面均由相互独立的生产记录生成，左右面使用不同物理侧证据，不存在左右镜像。每一面的完整提示词保存在 `qa/imagegen-prompts/`，主来源、URL、SHA-256、约束和辅助来源保存在 `source/face-source-lock.csv`。

| 面 | 生产模式 | 最终 PNG SHA-256 | 判定 |
|---|---|---|---|
| front | `SOURCE_LOCKED_GENERATION` | `86e1640b918083087d256622c83de888d991d588dde74543e2e9433744fb7267` | 精确型号/配置锁定 |
| rear | `SOURCE_LOCKED_GENERATION` | `9ed00405e7a5187d6d887a8ec75d71ec58a6671dc7f3d9c20af7107ce14c1dc6` | 精确型号/配置锁定 |
| right | `MULTI_REFERENCE_RECONSTRUCTION` | `52809f6636e017f577f8c6d66f0912bbf557821e24046628fcb946697d3773b3` | 物理右侧独立重建，无合规标签 |
| left | `MULTI_REFERENCE_RECONSTRUCTION` | `c93244f3a9c136da2056954c72bf46a22787bca7da40cd2d17a9f7885363d818` | 物理左侧独立重建，保留三组标签 |
| top | `MULTI_REFERENCE_RECONSTRUCTION` | `87c337d809bb62664706007ae4c4c8420c0c4a5c9bb0dd2b44549712ca96fd40` | 多角度锁定；标签已校正为 `Dell PowerEdge R7515` |
| bottom | `GENERIC_BOTTOM_FALLBACK` | `4da2f3204986bdcb86b7e7a24c7270af60d3030e32b37740f39a658f07d32b38` | 受控底面降级，不复制顶面 |

前部的安全面板为真实可见几何：13 个六边形环、左右独立端块以及前部安装凸缘；其后保留来源锁定的 24-SFF 载架面。最终修复已移除曾经没有证据支持的通用机耳孔图案，保留无虚构孔位的两个前部安装凸缘。

后部的两个 PSU 是独立实体，并使用精确来源锁定的 AC PSU 端面；端口、Riser 1B、PCIe 挡片、通风与冲压接缝保持可见。左右侧面没有镜像：左侧标签仅出现在物理左侧，右侧保持无标签。

## 底面降级说明

检索范围包括 Dell 官方手册、技术指南、技术规格、动态 3D 资源、Dell AR/CAD、监管型号 E46S003、多个精确型号经销商/翻新商图库、市场/拍卖、拆机视频以及中英日等本地语言关键词。没有找到可验证的精确 R7515 底面图。

因此底面严格按 `source/bottom-search-log.md` 的控制规则生成：只保留由精确侧面和官方 434 × 647.07 mm 本体尺寸证明的折边与镀锌材料，不添加未证实的 Logo、标签、通风孔、孔位、脚、导轨、接缝、紧固件或凸起，也不复制或镜像顶面。该限制不改变任何已验证侧面或斜视轮廓。

## 官方公开 3D 模型情况

未发现公开且精确匹配 Dell PowerEdge R7515 的官方 GLB、glTF、STEP、OBJ、FBX、BIM 或 AR 文件。精确 R7515 `resources/3dguides` 端点已在真实浏览器检查，但本环境收到 Akamai 公共访问拒绝；独立索引检索也未找到对应资产标识。

`source/optional-3d/` 中仅保留原样检索记录 `README.md`。没有用 R7525 或其他近似机型冒充官方模型；即使未来获得精确官方文件，也只应原样补存于该目录，不能替代本次自制 standard/web GLB。

## 双 WebGL 实载

最终共完成 **40 次真实浏览器实载**，每次均保留非空 PNG、`LOADED` 覆盖层、运行时回执和截图 SHA-256：

| 查看器 | standard | web | 六正交 | 四斜视 | 结果 |
|---|---:|---:|---:|---:|---|
| `<model-viewer>` 4.3.1 | 10 | 10 | 每构建 6 | 每构建 4 | 20/20 `ready=true`、`modelIsVisible=true` |
| Three.js GLTFLoader 0.180.0 | 10 | 10 | 每构建 6 | 每构建 4 | 20/20 `ready=true`，WebGL 2.0 |

视角矩阵：front、rear、left、right、top、bottom、front-left、front-right、rear-left、rear-right。Three.js 每次实载均报告 118 meshes、9 textured meshes、118 draw calls、2,614 triangles，且 standard/web 的包围盒一致。

完整逐次证据：`qa/webgl-load-evidence.json`。逐视角 standard/web 像素诊断：`qa/standard-web-parity.csv`。后者仅用于纹理预算与目视一致性辅助；结构一致性的门禁依据是两份 GLB 相同的 topology 与包围盒。

最终截图目录：

- `qa/renders/model-viewer/standard/`：10 张
- `qa/renders/model-viewer/web/`：10 张
- `qa/renders/threejs/standard/`：10 张
- `qa/renders/threejs/web/`：10 张

四张最终联系表位于 `qa/comparisons/contact-model-viewer-standard.png`、`contact-model-viewer-web.png`、`contact-threejs-standard.png`、`contact-threejs-web.png`。六面源图/实际 GLB 渲染/50% 叠加/差异诊断位于 `qa/comparisons/{front,rear,left,right,top,bottom}.png`，总表为 `qa/comparisons/orthographic-comparison-contact.png`。

## 最终门禁

| 门禁 | 结果 | 说明 |
|---|---|---|
| 精确型号与安装变体 | PASS | R7515 24-SFF、安全面板、无后置硬盘、Riser 1B、双 750 W AC PSU |
| 六面独立源锁 | PASS | 6/6；左右独立，不镜像 |
| 六面 PNG 结构审计 | PASS | 0 errors；6 条仅为抗锯齿轮廓透明像素提示，已在棋盘背景逐面目检 |
| standard GLB 审计 | PASS | 0 errors、0 warnings |
| web GLB 审计 | PASS | 0 errors、0 warnings |
| 尺寸、轴向、包围盒 | PASS | 官方尺寸容差内，朝向一致 |
| 内嵌资源、材质、镜像 | PASS | 9 个内嵌图像、无外部资源、无镜像节点 |
| 品牌标识 | PASS | 保留 `DELL EMC` 与可见的 `Dell PowerEdge R7515` |
| 可见几何与端口/盘位 | PASS | 安全面板真实几何、24-SFF、端口、双 PSU 均可见 |
| 双 WebGL 实载 | PASS | 40/40；两查看器 × 两构建 × 十视角 |
| 六正交 + 四斜视目检 | PASS | 四张联系表与六面源图对照均通过 |
| 官方精确 3D 原样备份 | PASS（未发现） | 无精确公开资产；检索记录已保存，未用近似机型替代 |
| 精确底面 | `PASS_WITH_BOTTOM_FALLBACK` | 完整检索后采用受控通用底面 |

机器可读总门禁位于 `qa/audit.json`；原始结构审计为 `qa/views-audit.json`、`qa/glb-standard-audit.json`、`qa/glb-web-audit.json`。

## 剩余风险

1. 精确底面照片不可得，底面只保证保守材料、外形和已证实折边，不声称还原不可见的真实孔位或标签。
2. Dell 精确 3D 资源端点从本环境不可访问，且没有公开索引结果；若日后 Dell 公开精确资产，应原样补存并单独审计。
3. 极小合规文字、浅冲压与表面颗粒主要通过来源锁定纹理/多角度重建表达；本模型面向网站外观展示，不是内部结构或工程 CAD。

除上述已披露风险外，没有未关闭的最终门禁。
