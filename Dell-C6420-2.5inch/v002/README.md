# Dell PowerEdge C6420 四节点整机 · v002

按实拍重做的写实外观模型。四个C6420节点装于C6400机箱，24个正常2.5英寸热插拔托架，双2400W电源。v001已退回，最终交付以本目录为准。

- [可编辑Blender模型](model/DELL-PowerEdge-C6420-4N-24SFF.blend)（约89.3MiB，纹理打包）
- [GLB模型](model/DELL-PowerEdge-C6420-4N-24SFF.glb)（约56.0MiB，贴图内嵌）
- [多角度预览与实拍对照](REVIEW.html)
- [QA记录](QA.md)、[官方尺寸](DIMENSIONS.md)、[锁定配置](CONFIGURATION.md)、[证据缺口](EVIDENCE.md)
- [来源索引](sources.csv)、[最终imagegen参考](references/SELECTED.txt)、[编辑与复现](REPRODUCE.md)

外廓482.6×824.1×86.8mm，含挂耳和前后突出件；主体宽448mm。1 Blender Unit=1m，前面-Y，后面+Y，正面看右侧+X，Z向上。原场景与GLB重导入尺寸一致。

在Blender4.0.2及以上打开.blend。主文件包含装配层级、可编辑网格、已打包纹理、摄影灯光和执行脚本；GLB导出排除摄影场景。独立导出纹理位于textures/delivery（17张）。重复部件共享网格，需要独立编辑时Make Single User。Cycles关闭不支持的降噪；Material Preview启用Scene World / Scene Lights。

底面与部分隐蔽细节明确为推测；极小铭牌字受实拍分辨率限制。这是公开资料支持的外观重建，不能声称所有未测量细节与实物逐点完全一致。

目录：sources为真实原图/PDF；references为imagegen及其提示词/版本/审查；model为主交付和阶段版本；textures为PBR/原始印刷及导出纹理；scripts为实际执行脚本；previews为18张模型渲染；desktop为真实桌面操作截图；qa为导出重开、几何/UV/透明度和修复记录。
