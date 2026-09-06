# Cisco Nexus N9K-C9336C-FX2 · v001

完整可编辑交换机资产。默认装配为36个空QSFP28业务口、额外的RJ45管理/Console、SFP管理与USB-A、3个双转子风扇模块、2个匹配AC电源、蓝色port-side exhaust及传统端口端挂耳。实体金属、孔壁、接口暗腔与导向结构均由几何构成。

- [离线图文审阅与真实桌面序列](REVIEW.html)
- [最终Blender主文件](model/CISCO-Nexus-N9K-C9336C-FX2.blend)
- [最终GLB](model/CISCO-Nexus-N9K-C9336C-FX2.glb)
- [尺寸及坐标](DIMENSIONS.md)、[配置](CONFIGURATION.md)、[证据覆盖](EVIDENCE.md)、[质量检查与限制](QA.md)
- [原始下载索引](sources/download-index.json)、[imagegen参考与退回记录](imagegen/REVIEW.html)
- [复现与编辑说明](REPRODUCE.md)、[SHA256清单](SHA256SUMS.txt)

Blender4.0.2制作，1单位=1米。端口面-Y、后部+Y、前视右侧+X，主壳底面Z=0。采用官方英寸规格换算439.42mm宽、622.30mm含拉手深、43.688mm主壳高；安装耳片外跨482.6mm与裸壳590mm深为估计。含0.025mm铭牌层的装配高度约43.713mm。

正式装配有966个网格对象、457个不同网格、484031个实例展开三角面。GLB有1040个节点、14种材质及7张内嵌PNG；不含摄影灯光、相机或测试夹具。金属全部OPAQUE、单面剔除、无透射。约33.75MB的GLB使用普通glTF2网格，无Draco依赖；可选KHR_materials_clearcoat用于未点亮指示灯表面。

主文件保留分组件层级、可重复脚本及隐藏的可编辑文字源集合98_EDITABLE_TEXT_SOURCES。重复部件共享网格，单独修改前先Make Single User。主壳/挂耳/端口/风扇/电源/管理/标识在独立集合中；90_STUDIO仅供预览。

正式预览为20张独立Cycles渲染，含六面、四斜视、俯仰斜视和8张特写。sources是原始实物/官方证据，imagegen是49次生成与修订记录中的23张选定参考，previews是三维渲染，desktop是真实桌面截图；四者分别保留来源。

实物证据主要来自NWR的3张4608×3456照片，Abacus/Serverlama同机型照片及官方指南交叉核对。未找到可信底面照片，底面明确标记INFERRED。未测量的孔位、厚度、隐藏接触件和转子布置为估计；不能作为制造或机柜干涉认证数据。铭牌小字保留原照信息上限，未虚构序列号或无法确认的PSU制造商修订。

`model/00…10…blend`为必要阶段文件，正式主文件仅以上不带阶段号的CISCO-Nexus-N9K-C9336C-FX2.blend。qa中的.blend均为独立测试夹具，不是另一版交付模型。

SHA256-MANIFEST.json区分原始下载、原始生成图/提示词、派生裁切/纹理、真实桌面截图和渲染。清单排除自身与运行环境缓存；最后执行的qa/archive-check.json作为清单校验结果单独保存，避免自引用循环。
