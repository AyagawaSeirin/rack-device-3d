# 提示词准备时的官方核验与访问状态

核验日期：2026-09-07。本文件只是独立建模任务的起点，尚未进行Cisco多角度商家实拍搜集、imagegen生成或Blender建模。

## 型号和数量

官方专用概览明确对应N9K-C9336C-FX2：1RU、36个40/100G QSFP28业务口、3个风扇模块、2个PSU；每个风扇模块有两个转子。管理RJ45、管理SFP、Console及USB是另外的管理/服务接口。风向颜色和PSU选件需在制作时选择一致的一套，尚未锁定具体实拍实体。[官方概览](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n9336cfx2_hig/guide/b_n9336cFX2_nxos_hardware_installation_guide/b_n9336cFX2_nxos_hardware_installation_guide_chapter_01.html)

FX2-E也是36口，但它是不同型号；系列表列出的FX2为3个双风扇托盘，而FX2-E为6个风扇。不能用端口总数相同来证明型号一致。[官方系列数据表](https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742282.html)

## 尺寸的初始依据

| 官方项 | 英制原值 | 官网厘米值 | 使用注意 |
|---|---:|---:|---|
| 宽 | 17.3in | 43.9cm | 不是已确认的挂耳最外总跨 |
| 含拉手深度 | 24.5in | 62.3cm | 不得重复加同一拉手突出量 |
| 高 | 1.72in | 4.4cm | 不能把1RU通用值替代具体尺寸 |

英寸精确换算与厘米舍入值略有差异，提示词要求保留两组值并在建模前选择有说明的基准，不声称制造级精度。[官方系统规格](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n9336cfx2_hig/guide/b_n9336cFX2_nxos_hardware_installation_guide/b_n9336cFX2_nxos_hardware_installation_guide_appendix_0111.html)

## 挂耳和安装方案

专用安装章节包含NXK-ACC-KIT-1RU与N3K-C3064-ACC-KIT等方案，涉及前后机身支架和机柜滑轨。制作时要选取与主实拍一致的一套；安装面可因机柜/冷热通道方案不同而改变，模型坐标仍以端口侧为-Y。当前未锁定耳板外形、孔位或安装距离，不能把文档文字清单当成已经完成的几何测量。[官方安装章节](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n9336cfx2_hig/guide/b_n9336cFX2_nxos_hardware_installation_guide/b_n9336cFX2_nxos_hardware_installation_guide_chapter_011.html)

## PDF与原始下载状态

在线检索/阅读工具能够读取专用硬件指南PDF（76页）和系列数据表PDF（19页）的内容；但本服务器用直接HTTP请求下载这两个原始PDF均返回403，使用浏览器User-Agent及普通download参数复试仍为403。因此**本目录没有伪造或占位的.pdf文件**，也没有声称原始PDF已下载。

- [硬件指南PDF](https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/hw/n9336cfx2_hig/guide/b_n9336cFX2_nxos_hardware_installation_guide.pdf)：在线解析所见概览从物理第7页/印刷第1页开始；尺寸在物理第55页/印刷第49页；挂耳安装从物理第28页/印刷第22页附近开始。执行时核对文件修订与真实页面，不盲用固定页号。
- [系列数据表PDF](https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/datasheet-c78-742282.pdf)：包含多个型号列，只有本型号列可用于本机约束。

新建模会话仍须实际搜索、查看并下载可获取的官方文件与第三方原始实拍，记录失败/替代来源，完成逐张资料审查后才能开展imagegen和建模。资料索引见[source-seed/index.json](source-seed/index.json)。
