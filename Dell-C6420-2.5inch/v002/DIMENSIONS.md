# 官方尺寸、配置与方向

单位为毫米，建模换算为米（÷1000），Blender单位比例1.0。

|对象/符号|官方mm|测量口径|证据|
|---|---:|---|---|
|整机Xa|482.6|前部挂耳外侧总宽|Technical Guide p66 Fig11 Table31；Technical Specifications p5 Fig1|
|整机Xb|448.0|机身外壳宽，不含挂耳|同上|
|整机Y|86.8|外壳高|同上|
|Za|26.8|挂耳安装基准面前侧，至前部最外端，无独立装饰面罩|同上|
|Zb|763.2|安装基准面至后壳平面|同上|
|Zc|797.3|安装基准面至后端最外突出件|同上|
|C6420单节点X|174.4|单个节点宽|C6420 Technical Specifications p4 Fig1 Table1|
|C6420单节点Y|40.5|单个节点高|同上|
|C6420单节点Z|574.5|节点前端至含后部突出件的末端，图中包含抽拉件|同上|

出处链接：
- https://i.dell.com/sites/csdocuments/Product_Docs/en/poweredge-c6400-c6420-technical-guide.pdf
- https://dl.dell.com/topicspdf/poweredge-c6400_owners-manual2_en-us.pdf
- https://downloads.dell.com/topicspdf/poweredge-c6420_Owners-Manual2_en-us.pdf

图示优先的解释：Zb/Zc有相同的前部安装基准。因此前最外端至后壳长度=Za+Zb=790.0；包含后端突出件的总深=Za+Zc=824.1。不能把Zc直接当总外包长度。独立spec-sheet的790mm对应前最外端到后壳；未涵盖后突出抽拉件。技术规格同时把763.2mm写成30.28英寸，换算实际30.047英寸，属于单位不一致，采用技术指南及规格中一致的毫米值。

坐标：X左右，Y前后，Z向上；前面-Y，后面+Y；站在正面看右手方向+X。主体底面中心原点，底板最低Z=0；主体安装基准y=-0.3816，后壳y=+0.3816；前最外端y=-0.4084，后最外端y=+0.4157。总外包前后不对称，相对于主体底面中心有3.65mm偏移。

六面观察：前camera(0,-Y,+Zmid),画面右+X；后camera(0,+Y,+Zmid),画面右-X；左camera(-X,0,+Zmid),画面右+Y；右camera(+X,0,+Zmid),画面右-Y；顶camera(0,0,+Z),画面右+X/上+Y；底camera(0,0,-Z),画面右-X/上+Y。各视图独立生成，不水平翻图。

估算值：主要壳体板厚约0.85mm（估算）；盖板接缝、冲压凸筋、螺钉、风孔节距、接口外框按实拍比例；不是制造级公差。底面无可信实拍，采用通用金属底板与浅筋，明确AI推测，不称官方结构。
