from pathlib import Path
import json,hashlib,csv
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002')
def read(n):return json.loads((P/'qa'/n).read_text())
a=read('original-scene-audit.json');g=read('glb-reimport-audit.json');c=read('glb-container-audit.json');d=read('measured-dimensions.json');geo=read('glb-geometry-audit.json');o=read('glb-orientation-audit.json');alpha=read('alpha-probe-results.json');clearance=read('decal-clearance-audit.json')
assert not a['geometry_flags'] and not geo['geometric_flags_after_position_weld_copy'] and not o['image_failures'] and not o['text_failures'] and not alpha['failures'] and not clearance['failed']
assert c['alpha_modes']==['OPAQUE'] and not c['double_sided_materials'] and c['all_images_embedded']
assert g['component_counts']=={'2.5-inch hot-swap carrier':24,'C6420 node':4,'2400W PSU':2}
selected=(P/'references/SELECTED.txt').read_text().splitlines();assert len(selected)==22 and all((P/'references'/x).is_file() for x in selected)
assert len(list((P/'desktop/turntable-material').glob('frame-*.png')))==25 and len(list((P/'desktop/turntable-glb').glob('frame-*.png')))==9
assets=['front','rear','left','right','top','bottom','front-left','front-right','rear-left','rear-right','high-front','low-rear','carrier-detail','brand-detail','node-detail','psu-detail','source-front-comparison','source-rear-comparison']
assert all((P/'previews'/f'{n}.png').is_file() for n in assets)
blend=P/'model/DELL-PowerEdge-C6420-4N-24SFF.blend';glb=P/'model/DELL-PowerEdge-C6420-4N-24SFF.glb';mb=lambda p:round(p.stat().st_size/1024/1024,2)
text=f'''# v002 质量检查记录

检查对象为四节点C6420完整服务器、24个正常2.5英寸热插拔托架、中央双2400W电源。前部塑料填充件已全部移除。写实外观重做包含连续折弯/冲压钢板、真实三维孔洞、接口暗腔、钢片拉手和细节PBR材质；保留原位DELL EMC及C6400品牌。

## 已执行检查

| 项目 | 结果 | 证据 |
|---|---|---|
| 官方尺寸 | 整机482.6×824.1×86.8mm（X/Y/Z，含挂耳/前后突出件）；4节点各174.4×574.5×40.5mm | DIMENSIONS.md；qa/measured-dimensions.json |
| 导出后尺寸/组件 | GLB重导入与原场景一致；24托架、4节点、2PSU | qa/glb-reimport-audit.json |
| 几何 | 2020网格对象，1,040,720三角面；无检测到的退化面、倒置封闭体或异常开放边界；对象内部重复面0 | qa/original-scene-audit.json；qa/glb-geometry-audit.json |
| 不该穿透的壳体 | 顶、底、左右30个射线探针均命中；原场景和GLB分别执行 | qa/original-shell-probes.json；qa/glb-geometry-audit.json |
| 镜像/文字/UV | 5个印刷图像UV及62组可读文字朝向通过；竖排iDRAC按真实竖向检查；负变换0，缺失UV引用0 | qa/original-orientation-audit.json；qa/glb-orientation-audit.json |
| 透明度 | GLB26材质全部OPAQUE，Alpha1、Transmission0，无全局双面；17张贴图完整内嵌 | qa/glb-container-audit.json |
| 深浅背景 | 前右/后左重导入渲染均检查；9个机身像素Alpha均255 | qa/glb-*-light.png、*-dark.png；qa/alpha-probe-results.json |
| 贴花深度 | 品牌与底材间隙约0.140mm，顶盖三标签约0.130mm，均非共面 | qa/decal-clearance-audit.json |
| 动态观察 | 原模型24次15°桌面输入、25帧；起终四元数绝对点积约1；GLB另24次桌面输入、9帧，覆盖360° | desktop/turntable-material；desktop/turntable-glb；qa/*orbit*.json |
| 视口模式 | 实际Solid、Material Preview、Cycles Rendered对照；近远、正面、俯仰与底面操作记录 | desktop/05*至09*；previews/ |
| 外观对照 | 6独立面、4斜视、俯仰视、4特写、2实拍对照视，共18张渲染 | REVIEW.html；previews/ |

外廓数值与官方设定的差异小于0.001mm，只代表浮点计算匹配，不代表所有细节都具有这种测量精度。GLB有788份独立网格，重复部件以实例复用。可编辑.blend约{mb(blend)}MiB；GLB约{mb(glb)}MiB。

## 实际发现并修复的问题

1. v001整体外观被退回；v002重建钣金、热插拔托架、节点、接口和电源。用户更正后废止塑料填充件，前部24个正常盘架与最终参考单明确一致。
2. 超亮照明、发灰塑料、过强金属颗粒和橡胶感电源拉带已重调：采用细微表面数据、黑色ABS、真实17.5mm宽织带形态及边缘纤维。微观表面为通用制造材质，不冒充扫描。
3. 曲线封口和文字转换产生的边界/退化面已清理，实体重新计算法线并显式三角化。重复小件共享网格，避免重复几何开销。
4. 低清顶盖标签投影出现拖影，改为清晰Abacus原始实拍。重开文件时发现UV层删除引起引用失效、渲染成黑块，已重建UV层并完成重开与GLB验证。
5. 前部金属孔板平面曾出现星状反光，查明平面顶点法线最大偏离约22.26°。最后只校正这两块共享孔板的平面法线，保留小倒角与开孔壁法线；复查品牌特写与相关前视、GLB。记录见qa/cheek-normal-correction.json。
6. 官方前后突出量按安装面正确累计，修正前拉手、后织带和控制外壳极值，避免把797.3mm错误当成整机总深。

未观察到大面Z-fighting、随机透明、翻面消失或明显外部穿模。极远距离下真实细孔/边缘仍可能有屏幕采样锯齿，不能把所有明暗变化都说成几何闪烁；模型使用实际孔洞和不透明材质，未用透明排序掩盖问题。射线、网格检查和选定视角属于具体覆盖范围，不是对任何相机位置的形式证明。

## 证据边界与保留限制

- 没找到完整真实底面，采用通用连续钢板与4条内凹加强筋；对象名INFERRED_bottom_formed_sheet及属性、EVIDENCE.md均标推测。
- 左侧局部孔位、隐蔽板厚/结构、风扇叶片及微观材质按可见效果估算。未建立不可见精密主板，也不声称制造级CAD或逐点扫描复刻。
- 顶盖极小字由真实照片保留，源分辨率不够的字不能完整读出；没有AI补字或虚构硬盘容量、序列号、网卡速率。
- 本模型为装配状态外观资产，有独立组件和拉手枢轴元数据，未制作开合动作或拆机动画。
- 原整圈桌面序列保留修复过程；最终孔板修正后以更新GLB整圈及前部特写复查。累计角度是桌面输入角，软件OpenGL重绘可短暂滞后。

原始素材、生成图与模型渲染分目录保存。来源索引97条（含文档、页面和辅助素材，不等于97张同配置实拍），具体采用/排除细节见sources.csv。最终参考22项，本轮内置imagegen新生成23张，错误生成保留并标记退回。
'''
(P/'QA.md').write_text(text)
(P/'README.md').write_text(f'''# Dell PowerEdge C6420 四节点整机 · v002

按实拍重做的写实外观模型。四个C6420节点装于C6400机箱，24个正常2.5英寸热插拔托架，双2400W电源。v001已退回，最终交付以本目录为准。

- [可编辑Blender模型](model/DELL-PowerEdge-C6420-4N-24SFF.blend)（约{mb(blend)}MiB，纹理打包）
- [GLB模型](model/DELL-PowerEdge-C6420-4N-24SFF.glb)（约{mb(glb)}MiB，贴图内嵌）
- [多角度预览与实拍对照](REVIEW.html)
- [QA记录](QA.md)、[官方尺寸](DIMENSIONS.md)、[锁定配置](CONFIGURATION.md)、[证据缺口](EVIDENCE.md)
- [来源索引](sources.csv)、[最终imagegen参考](references/SELECTED.txt)、[编辑与复现](REPRODUCE.md)

外廓482.6×824.1×86.8mm，含挂耳和前后突出件；主体宽448mm。1 Blender Unit=1m，前面-Y，后面+Y，正面看右侧+X，Z向上。原场景与GLB重导入尺寸一致。

在Blender4.0.2及以上打开.blend。主文件包含装配层级、可编辑网格、已打包纹理、摄影灯光和执行脚本；GLB导出排除摄影场景。独立导出纹理位于textures/delivery（17张）。重复部件共享网格，需要独立编辑时Make Single User。Cycles关闭不支持的降噪；Material Preview启用Scene World / Scene Lights。

底面与部分隐蔽细节明确为推测；极小铭牌字受实拍分辨率限制。这是公开资料支持的外观重建，不能声称所有未测量细节与实物逐点完全一致。

目录：sources为真实原图/PDF；references为imagegen及其提示词/版本/审查；model为主交付和阶段版本；textures为PBR/原始印刷及导出纹理；scripts为实际执行脚本；previews为18张模型渲染；desktop为真实桌面操作截图；qa为导出重开、几何/UV/透明度和修复记录。
''')
(P.parent/'README.md').write_text('''# Dell PowerEdge C6420 四节点整机

当前交付为[v002写实重做](v002/README.md)：24个正常2.5英寸热插拔硬盘托架、4个C6420节点、双2400W电源。\n\n[可编辑Blender模型](v002/model/DELL-PowerEdge-C6420-4N-24SFF.blend) · [GLB模型](v002/model/DELL-PowerEdge-C6420-4N-24SFF.glb) · [预览与实拍对照](v002/REVIEW.html) · [QA记录](v002/QA.md)\n\nv001已被用户退回并保留历史记录。底面和部分未证实细节的推测范围详见v002/QA.md。\n''')
print('Final README/QA written from verified evidence')
