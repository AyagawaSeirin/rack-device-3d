# 执行进度
目标锁定：完整 Dell PowerEdge C6420 四节点系统，C6400 配套机箱，24×2.5英寸前置盘位。
版本 v001；既有未保存场景已通过 Blender MCP 另存 backups/preexisting-setup-check.blend。
当前阶段：真实资料下载/核实完成主要结构，开始逐张 imagegen 参考生成；未正式建模。
工具：原生 Blender MCP、server_desktop 均可连接同一 XRDP 桌面；DISPLAY 动态检测为 :10.0。
7份官方 PDF，10张第三方原始产品照片已验证；sources/extracted 保存结构/尺寸页。
锁定后部参考：NewServerLife 同页全机，中央上下2400W EPP PSU，各节点双SFP插笼、双USB-A、微USB、miniDP、RJ45；不推定网卡芯片型号。
前部实拍是塑料空位填充件，建模采用同24SFF系统官方维护手册p7的24只热插拔载架，明确区分，不把空位填充件当载架。
尺寸：Xb448/H86.8/Zb763.2，耳宽Xa482.6，Za26.8，Zc797.3；Zc从挂耳安装基准量起，总外端深824.1。节点174.4×40.5×574.5，官方末项含抽拉突出部。
底面缺实拍、侧面细节不完整，允许推测并标注。不能水平翻转图像来补视角。
未完成：imagegen全清单、逐张检查与纠错、建模、真实桌面交互检查、GLB重新导入QA与所有交付。

参考阶段完成：8官方PDF、10第三方原图、25条sources.csv索引。imagegen已实际生成全部22项并保存多个纠错版本；SELECTED.txt列采用版本，manifest.json记录提示词/输入/版本/用途，qa-log逐张检查。官方品牌及服务标签已直接提取，未用AI文字当贴图。开始Blender MCP分阶段执行。

建模/修复完成：当前GUI文件model/07-finish-reviewed.blend，111?（以审计为准）对象；1089个mesh，233167三角面；24 carrier/4node/2PSU。官方整机总外包482.600003×824.099988×86.800014mm，原点主体底面中心。全部金属塑料不透明。原始阴影baffle/PSU占位实体已经修复为真正外壳，接缝加内搭片。Curve/Font转换独立可编辑mesh，曲线端盖焊接，文本为明确表面油墨。qa/original-scene-audit.json FLAGS0，内部精确重复面0。build_c6420.py + repair_geometry.py + refine_finish.py 已实际经过原生BlenderMCP执行。

渲染：previews/已有16张最终CPU Cycles96samples六视图、四斜视、高低视及detail；background批量渲染完毕，主GUI仍是同实例，仅batchrender额外后台进程。desktop/含阶段真实MCP截图。desktop/turntable-material已有25张MCP实际KP_6键盘旋转截图（0..360deg），原始1920×929；事件记录qa/desktop-orbit-events.json；起始四元数(0.7624284,0.4863007,0.2295498,0.3598910)，最终为其负数，代表同一姿态完成完整一圈。已查看0/3/6/9/12，尚需查看剩余视角并补多俯仰/近远/Solid/Rendered对比。

待完成：通过MCP执行scripts/export_deliverables.py（脚本已写但未执行）；GLB JSON材质/轴向/尺寸验证、重新导入独立场景并真实桌面检查；补充掠射角/顶底和浅深背景验证；QA报告/README/成果索引/对比页。小网孔/高光在MPreview远距会像素级变化，需区分采样/反射和真实透明；目前Ray渲染黑色腔体正确、材质OPAQUE。最终不得声称制造级精度，节点/侧孔/底面/微小标签的估算需明确。
