# DELL PowerEdge C6420 四节点整机 · 24 × 2.5 英寸

完成版本：v001。机箱是该四合一系统配套的 C6400，内含四个 C6420 节点；交付对象为完整服务器。正面保留原厂 DELL EMC 和 C6400 铭牌，未将配套机箱铭牌改成其他型号。

## 打开成果

- 可编辑模型：[DELL-PowerEdge-C6420-4N-24SFF.blend](model/DELL-PowerEdge-C6420-4N-24SFF.blend)
- 通用模型：[DELL-PowerEdge-C6420-4N-24SFF.glb](model/DELL-PowerEdge-C6420-4N-24SFF.glb)
- [可浏览的对照与旋转证据](REVIEW.html) · [QA 报告](QA.md)
- [官方尺寸](DIMENSIONS.md) · [锁定配置与资料缺口](CONFIGURATION.md) · [来源索引](sources.csv)

Blender 4.0.2 内直接打开 .blend。所用 5 张图文贴图已打包；GLB 同样内嵌贴图，不需要外部下载。机箱、24 托架、四节点、双电源、接口、标识和紧固件按集合/组件分组；保留独立可编辑网格和组件父级。文字的内容保留在 readable_text 属性中，品牌使用官方图文资产的独立 UV。源码也保存在 Blender Text 数据中。

## 尺寸与坐标

1 Blender Unit = 1 米；官方毫米值 ÷1000。X 左右、Y 前后、Z 向上；正面 -Y、背面 +Y；站在正面看右侧 +X。主体底面中心为原点，最低 Z≈0（浮点误差量级）。

主体宽 448 mm、高 86.8 mm；挂耳总宽 482.6 mm。安装基准至后壳 Zb=763.2 mm，至后突出件 Zc=797.3 mm；前突出 Za=26.8 mm，故整机最外端总深为 **824.1 mm**。节点为 174.4×40.5×574.5 mm（宽×高×含把手深）。测量口径、790 mm 与 Zc 的区别、英寸换算笔误见 DIMENSIONS.md。

glTF 使用 Y-up，正面为 glTF +Z；导回 Blender 后恢复 Z-up/正面 -Y，未发生镜像或第二次毫米换算。

## 配置、精度和假设

采用同 24SFF 系统的官方热插拔载架形态填满 24 盘位。锁定经销商整机照片的后部选件：四节点、中央上下两只 EPP 2400W 电源、每节点双 SFP 插笼。网卡确切芯片/速率无法从照片确定，因此不编造型号或序列号。经销商前照装有塑料填充件，和本模型采用的正式载架状态已在 CONFIGURATION.md 明确区分。

这是按官方外包尺寸和公开外观证据建立的外观模型，不是生产用 CAD。**底面没有可信同配置实拍，四条浅筋底板为 AI 推测**；左右细孔、冲压和部分紧固件位置/板厚按比例估算。内部仅制作开口观察所需的外壳、托盘和遮挡。顶盖服务说明采用官方图文，版式及细节作了简化；模糊的警告微字未伪造。

远距细孔与窄金属高光在软件 OpenGL 中仍可能有像素级走样；近距和 Cycles 对照未发现由异常透明、反法线或共面贴花引起的大面闪烁。提供原始桌面旋转序列供复核。

## 文件内容

- sources/official：8 份原始官方 PDF，包括规格、技术指南、维护手册、规格单和 HPC 白皮书。
- sources/third_party：10 张验证格式/尺寸的第三方原图及访问记录；403 错误页不作为图片证据。
- sources/extracted：官方尺寸/结构页面及直接提取图文。
- references/imagegen：33 张实际内置 imagegen 输出（含纠错版本）；22 项最终采用清单在 references/SELECTED.txt。
- references/manifest.json：每张图的提示词、真实输入/生成输入、版本、原始工具输出路径、用途和 SHA256；prompts/ 保存完整提示词；references/imagegen/qa-log.md 逐图说明采用范围和拒用原因。
- model：阶段文件、最终 .blend / GLB 及参数表；textures：独立准确图文资产。
- previews：六面、四斜视、俯仰视和重要细节，共 16 张 Cycles 预览。
- desktop：实际 server_desktop MCP 操作截图、25 帧 360° 序列；qa：GLB 独立重导入项目、浅深背景图、几何/尺寸/UV/Alpha 检查及修复记录。
- backups：开始前未保存的原场景副本和修复前导出，未覆盖原来的 setup-check.blend。

## 复现

主要脚本是 scripts/build_c6420.py。它读取 model/parameters.json 的主体尺寸，以循环和可复用几何函数生成部件；进一步细节偏移在脚本中明确以米记录。脚本随后调用 repair_geometry.py、refine_finish.py、prepare_triangles.py。最终由 export_deliverables.py 保存和导出。重建会重新创建当前 Blender 文件中的对象，应在副本上执行。

实际执行使用的是已连接的 Blender MCP；本机协议调用入口也可复现：

```bash
/root/.local/share/uv/tools/blender-mcp/bin/python /root/.local/share/blender-mcp-setup/mcp_call.py blender execute_blender_code --code-file /root/Blender/DELL-C6420/v001/scripts/rebuild_via_mcp.py
/root/.local/share/uv/tools/blender-mcp/bin/python /root/.local/share/blender-mcp-setup/mcp_call.py blender execute_blender_code --code-file /root/Blender/DELL-C6420/v001/scripts/export_deliverables.py
```

渲染脚本为 render_previews.py；桌面真实旋转采集脚本为 desktop_orbit_mcp.py（执行前光标应位于已检查的 3D 视区）。该脚本实际经 server_desktop MCP 发送键盘输入并保存桌面截图，没有用 bpy 相机运动冒充 computer use。建模始终在原 XRDP Blender 实例中进行；后台 Blender 进程仅用于批量 CPU 渲染。Cycles 已关闭此环境不支持的降噪。

来源图片/官方图文与 DELL 商标的权利属于原权利人，来源及派生关系均保留。
