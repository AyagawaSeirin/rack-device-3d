# Fortinet FortiGate FG-3700D AC 最终 QA

日期：2026-08-23  
最终状态：**PASS**

## 对象与装配冻结

- 制造商：Fortinet, Inc.
- 产品：FortiGate 3700D / MPN `FG-3700D`
- 精确实机标识：`FG-3700D-USG`
- 装配：AC，双热插拔冗余 PSU；三个后部风扇托盘、三个后视可见转子开口、六个 FAN 指示位
- 机身：437 × 133 × 579 mm
- 安装态审计包围盒：482.6 × 133 × 633 mm
- 坐标：`+X` 为从端口前面观察的设备右侧，`+Y` 向上，`+Z` 为端口前面
- 底面：精确监管实照，`SOURCE_LOCKED_GENERATION`，7 组双锁孔，稳定的 3-2-2 非镜像布局；未使用回退
- Logo：保留真实 Fortinet / FortiGate 标识
- 精确官方公开 3D：已完成公开搜索，未发现；`source/optional-3d/` 因此保持为空

## 交付资产

| 文件 | 大小 | SHA-256 | 状态 |
|---|---:|---|---|
| `model/Fortinet-FG3700D.glb` | 9,006,532 B | `0961f7873bd7fb4ae7b30c502fadfd739cdff04adc2bb499ea8a8aa03c0aa7d7` | PASS |
| `model/Fortinet-FG3700D-web.glb` | 6,167,632 B | `da509ed749d6025eec1573295b805c09d87f73896621f6d5920ffe189a57e694` | PASS |

两版均为自包含 GLB，外观节点完全一致；各含 1 scene、49 nodes、49 meshes、49 primitives、16 materials、6 张嵌入纹理，并使用 `KHR_materials_unlit` 保持六面源锁摄影纹理的颜色一致性。

## 可见几何门槛

- 闭合机身核心，无可见空内腔
- 前部两侧独立托架：真实网格开孔、侧板大开口、两组独立 U 形金属把手
- 4 个 QSFP+ 与 28 个 SFP/SFP+ 独立端口凹位和金属框，附管理/Console/USB 几何 relief
- 后部两只 AC PSU、两只 IEC C14、黑色拉环和绿色释放片
- 三个独立后风扇托盘、三组可见转子/叶片/轮毂、三组方孔格栅、六个 FAN 指示位
- 两个接地柱与独立接地板
- 左右侧凸点和紧固件按独立数组建模，未镜像复制
- 底面 7 组双锁孔为真实有孔平面，并有暗色内部背板；数量由 GLB extras 与命名节点双重审计

`qa/structure-audit.json` 对标准与网页 GLB 的全部上述命名节点、数量 extras 和节点一致性均判定为 `PASS`。

## 结构审计

| 审计 | 结果 | 错误 | 未解决警告 |
|---|---|---:|---:|
| 六面透明 PNG | PASS | 0 | 0 |
| 标准 GLB | PASS | 0 | 0 |
| 网页 GLB | PASS | 0 | 0 |
| 命名可见几何 | PASS | 0 | 0 |
| 统一交付审计 | PASS | 0 | 0 |

六面 PNG 的原始自动审计记录了 6 个透明边缘提示；逐面原始分辨率检查确认它们仅为产品外轮廓抗锯齿，六面的机身核心低于 alpha 250 的比例均为 0%，因此记录为已解决，不是未解决警告。

## 双独立 WebGL

- Three.js `0.179.1`
- Babylon.js `8.22.2`，显式启用右手坐标，确保物理左右与 glTF/Three.js 一致
- 标准/网页两版均各自在两个引擎中渲染：六正交 + 四斜视
- 共 40 张最终截图，全部为 1600 × 1200；截图视口显式固定为 4:3，未发生横向拉伸
- 两引擎标准版逐视图平均绝对 RGB 差最大值：4.378086 / 255
- 两引擎网页版逐视图平均绝对 RGB 差最大值：4.382834 / 255
- 标准/网页版在 Three.js 中逐视图平均绝对 RGB 差最大值：0.619793 / 255
- 浏览器控制台只有 SwiftShader `ReadPixels` 截图性能提示；无 GLB 加载、JavaScript、材质或 WebGL 错误

最终截图位于：

- `qa/viewer-threejs/standard/` 与 `qa/viewer-threejs/web/`
- `qa/viewer-babylonjs/standard/` 与 `qa/viewer-babylonjs/web/`
- 四张总览联系表位于 `qa/renders/`

## 比较材料

- `qa/comparisons/source-vs-threejs-standard/`：6 张源锁正交 + 4 张实机斜视对标准 GLB
- `qa/comparisons/threejs-vs-babylonjs-standard/`：10 个标准版双引擎对照
- `qa/comparisons/standard-vs-web-threejs/`：10 个标准/网页版对照
- `qa/comparison-table.csv`：10 个视图的来源、四个最终渲染路径、差异值和逐项 `PASS`
- `qa/manifest.csv`：核心交付文件大小与 SHA-256
- `qa/audit.json`：统一机器可读最终结论

像素差只作为诊断；最终接受以一对一特征计数、方向、非镜像机械特征、可见 relief、真实 Logo、材质与实机来源对照为准。

## 最终结论

精确身份、六面 source-lock、真实底面 7 组双锁孔、闭合可见几何、双 GLB、双独立 WebGL、六正交四斜视、结构审计、比较表、清单和最终 QA 已全部闭环。没有使用底面回退，没有用近邻型号或官方/第三方网格替代新建模型。

