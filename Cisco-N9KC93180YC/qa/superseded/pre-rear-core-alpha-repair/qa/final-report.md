# Cisco N9K-C93180YC-FX 最终报告

审计日期：2026-08-24（Asia/Singapore）

## 最终结论

**PASS_WITH_BOTTOM_FALLBACK**

机箱、安装配置、六面素材、自建 standard/web GLB、两个独立 WebGL 引擎的 40 次逐次哈希实载、结构审计、左右非镜像审计和视觉比较均通过。唯一 fallback 是精确型号底面公开证据缺失；该限制只影响底面，并已使用技能允许的保守无标识底面。

## 精确交付身份

- 制造商：Cisco Systems, Inc.
- 机箱：Cisco Nexus 9000 C93180YC-FX Chassis
- PID：`N9K-C93180YC-FX`
- 前部：48 个空 SFP/SFP28 笼位，6 个空 QSFP/QSFP28 笼位；无光模块、无面罩
- 电源：2 × `NXA-PAC-500W-PI`，500W AC，酒红色 port-side intake
- 风扇：4 × `NXA-FAN-30CFM-PI`，酒红色 port-side intake
- 后部 I/O：FX L1/L2、BCN/STS、RS-232 console、USB、RJ-45 OOB
- 风道：port-side intake，所有 PSU/风扇方向一致
- 机架耳：仅前部；GLB 中后耳节点计数为 0

用户截图的四个酒红色拉手锁定 intake 物理配置。保存的旧版 FX 安装指南把酒红色 intake 风扇写作 `NXA-FAN-30CFM-B`；用户最终配置锁将订购 PID 统一为 `NXA-FAN-30CFM-PI`。二者在本任务的可见身份约束中均指向同一酒红色 intake 外观；最终 manifest、GLB 元数据、节点名和报告均使用用户锁定的 `-PI`。

## GLB 交付

| 文件 | 字节数 | SHA-256 | 结构 |
|---|---:|---|---|
| `models/Cisco-N9K-C93180YC-FX-standard.glb` | 9,896,600 | `4106f6617dd292abc33992edf33e6e6f5534e2448e17e449e3fb15753d8f0c62` | 418 nodes / 95 meshes / 15 materials / 6 embedded PNG |
| `models/Cisco-N9K-C93180YC-FX-web.glb` | 3,492,936 | `b6b6c52837561cd427c22a1c1026915c3e9d3d56507b00387fd97c9f6eb61037` | 418 nodes / 95 meshes / 15 materials / 6 embedded PNG |

两份 GLB 的几何签名完全相同：`c8d3be0fe17d6d290d73f55f15b0f1f464f13aa827d6a2640da863f330355b1b`。web 版只缩小内嵌纹理，未删减可见几何。

官方机身尺寸为 439 × 571 × 44 mm。前耳标称总宽按 19 英寸建模为 482.6 mm。查看器实测完整可见包围尺寸为 482.6 × 45.15 × 581.58 mm；高度/深度的额外量只来自表面 relief、前部端口面和后部真实把手/锁扣，不冒充官方机身尺寸。

## 六面 source-lock 与 imagegen

六面各使用一次独立内建 imagegen 调用，原始 chroma-key 输出保存在 `qa/intermediate/`，去背景并按物理比例处理的最终 PNG 在 `views/`：

- front：精确 FX 实拍 SOURCE_LOCKED_GENERATION，保留 Cisco 标识、`N9K-C93180YC-FX`、48+6 空笼位和三孔前耳；
- rear：用户截图锁定 2 PSU + 4 酒红色 PI 风扇，精确 FX 后部实拍/官方图锁定 L1/L2 和 500W 几何，PI 实拍锁定酒红色材质；蓝色 PE 只提供几何，禁止复制颜色；
- left/right：两次独立 MULTI_REFERENCE_RECONSTRUCTION，独立 prompt、独立输出、独立 UV；没有镜像；
- top：精确 FX 全顶面实拍 SOURCE_LOCKED_GENERATION；
- bottom：`GENERIC_BOTTOM_FALLBACK`，只继承通用 Cisco 1RU 银色板材和保守折边；无孔、无脚、无轨、无标签、无凸台、无服务开口。

标准 GLB 内嵌的六张 PNG 与 `views/*.png` 逐字节 SHA-256 全部一致。左右源文件 SHA 不同；将右面镜像后与左面比较，RGB 平均绝对差为 23.6656，远高于非镜像门槛 4.0。

## 真实可见几何审计

结构化计数全部吻合：

- 48 个独立 SFP28 凹槽；
- 6 个独立 QSFP28 凹槽；
- 2 个 `NXA-PAC-500W-PI` 模块与 2 个 IEC AC 入口；
- 4 个 `NXA-FAN-30CFM-PI` 风扇托盘与 4 个酒红色锁扣；
- 4 个 FX L1/L2/console/OOB 接口节点；
- 6 个前耳真实开孔；
- 0 个后耳节点；
- 左、右独立纹理节点各 1 个。

全部材质为 `OPAQUE` 且单面；资源全部嵌入 GLB，无外部 buffer URI。闭合机身核心、端口凹进、前耳真孔、PSU 把手/锁扣、风扇锁扣、侧面孔位/接地点和顶盖轮廓均有实际几何。首轮曾出现 relief 覆盖实拍纹理的问题，该轮模型和加载证据已废弃并保存在 `qa/superseded/`；最终 GLB 让 source-lock 实拍纹理保持可见，只以 relief 提供深度和视差。

## 双查看器 40 次实际加载

最终有效证据为 **40/40 PASS**：

| 查看器 | standard | web | 合计 |
|---|---:|---:|---:|
| Three.js r185 / WebGL2 | 10 | 10 | 20 |
| Babylon.js 9.22.1 / WebGL2 | 10 | 10 | 20 |
| 合计 | 20 | 20 | 40 |

每个组合均实际加载 6 个正交视角（front/rear/left/right/top/bottom）和 4 个斜视角（front-left/front-right/rear-left/rear-right）。每次使用唯一 URL，保存 1280 × 900 截图，记录传输字节、包围尺寸，并在浏览器内对实际响应字节计算 SHA-256：standard 哈希命中 20/20，web 哈希命中 20/20，合计 40/40；字节数命中 40/40；截图存在 40/40。

证据文件：

- `qa/webgl-loads/load-events.json`
- `qa/viewer-load-evidence.csv`
- `qa/webgl-loads/three/`
- `qa/webgl-loads/babylon/`
- `qa/webgl-loads/contact-sheets/all-40-hash-proven-loads.png`

早期哈希、relief 覆盖版、未带浏览器哈希字段的加载均移到 `qa/superseded/`，不计入最终 40。

## 比较与视觉抽检

- 20 张 Three.js/Babylon.js 同相机比较表：side-by-side、50% overlay、4× difference；
- 6 张正交 source-lock 对实际 standard GLB 比较；
- 3 张权威实拍与前/后斜视、顶视比较；
- 4 张 viewer/model 十视角 contact sheet，加 1 张全部 40 次总表。

抽检确认：标准/web 的 48+6 前部、2 PSU + 4 酒红色风扇、FX 后部 I/O、左右独立孔位、顶盖通风带/检修盖以及保守底面一致；两个引擎只存在轻微抗锯齿/亮度差，不存在方向翻转、左右镜像、后耳、丢件或变体漂移。

## 官方 3D 模型检索

结论：**NOT_FOUND**。

Cisco 支持页只提供 Nexus 9000 的 2D Visio stencil，不是 3D。官方/公共检索覆盖 `GLB`、`glTF`、`OBJ`、`FBX`、`STEP/STP`、`CAD`、`AR`。此外完整扫描了 Cisco 公共 Kaon WebGL 目录的 214 个 `app.xml` manifest；唯一 93180 3D 应用是不同产品 `Cisco Nexus 93180LC-EX`，没有 `N9K-C93180YC-FX` 几何。故 `source/optional-3d/` 只保留 NOT_FOUND 说明，没有官方文件可原样保存；两份自建 GLB 不受替代。

## 残余风险

1. **底面**：没有找到精确 FX 底面照片或官方图，因此最终状态必须是 `PASS_WITH_BOTTOM_FALLBACK`，不能升级为无条件 PASS。
2. **风扇命名代际**：保存的旧版 HIG 使用 `NXA-FAN-30CFM-B`，用户最终锁定订购 PID 为 `NXA-FAN-30CFM-PI`；物理外观和气流都由酒红色 intake 证据固定，最终交付使用 `-PI`。
3. **总深度**：Cisco 公开 571 mm 是机身尺寸；PSU 把手等突出部分没有独立官方总深度，因此报告同时给出 571 mm 机身深度与 581.58 mm 最终可见包围深度，不混淆两者。
4. **后部实拍**：高分辨率 exact-FX 后部来源是蓝色 PE，故只用于几何；最终酒红色 PI 颜色/安装数来自用户截图和精确 PI 模块实拍。该多源重建限制已明确记录。

## 流程与范围声明

- 会话缺少请求工作流中的 PDF 专用技能；官方 PDF 仍原样保存，并用 Ghostscript 完成文本提取、150 dpi 页面渲染与逐页视觉检查。
- 只修改了 `Cisco-N9KC93180YC/` 独立目录。
- 未修改其他型号目录，未触碰 `BATCH-STATUS.md`。
- 未 commit、未 push，未创建、分叉或委派其他 Codex 任务。

结构化最终审计见 `qa/audit.json` 与 `qa/delivery-validation.json`。
