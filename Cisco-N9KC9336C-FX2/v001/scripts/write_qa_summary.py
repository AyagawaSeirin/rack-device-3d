from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
def read(n):return json.loads((ROOT/n).read_text())
g=read('qa/geometry-initial.json');o=read('qa/original-delivery-scene.json');b=read('qa/glb-delivery-scene.json');e=read('qa/glb-container.json');orig=read('qa/original-ear-render-tests.json');imp=read('qa/glb-ear-render-tests.json');orbit=read('desktop/glb-material/closure.json');reopen=read('qa/packed-reopen.json')
for d in [g,o,b,e,orig,imp,orbit,reopen]:assert d['pass']
assert len(orig['renders'])==len(imp['renders'])==11
text=f'''# QA — v001

本报告检查已交付文件，不把设定尺寸的小数精度当作实物制造精度。GLB回读与容器报告对应SHA256：`{e['sha256']}`。

| 检查 | 结果与覆盖 | 证据 |
|---|---|---|
| 型号/数量 | 36业务口=18列×2；独立1管理RJ45、1Console RJ45、1管理SFP、1USB-A；3风扇托盘/6内部转子；2匹配AC电源；2耳板 | geometry-initial.json、glb-reimport.json、front/rear及特写；人工图像复核见下文 |
| 尺寸/轴 | 原始与GLB回读包围盒一致；主壳439.420015×589.999974×43.687999mm；含拉手及耳片482.600003×622.299999×43.713000mm | original-delivery-scene.json、glb-delivery-scene.json、DIMENSIONS.md |
| 几何 | {g['triangles']}实例展开三角面、{g['mesh_instances']}网格对象、{g['unique_meshes']}不同网格；实体无不期望开放边/非流形边，体积正；无零面积/坐标重复面；世界变换无负行列式 | geometry-initial.json、两个delivery-scene.json |
| 平面法线 | 面积>2mm²平面，几何面与分裂顶点法线dot≥0.9999；U形圆管为有意弧面，单独按连续截面/特写审查 | delivery-scene.json、handle-sweep-fix.json |
| 原始挂耳 | 44隔离射线、30装配射线；11正反/侧面/斜视/掠射角渲染，42Alpha采样通过 | original-ray-tests.json、original-ear-render-tests.json及对应PNG |
| GLB挂耳 | 同样44+30射线、11渲染、42Alpha采样通过；渲染来自独立GLB场景复制的耳板 | glb-ray-tests.json、glb-ear-render-tests.json、glb-ear-fixture.blend |
| 机身封闭与端口深度 | 每版24处分散顶底侧射线；每版4透明渲染、36个3×3像素封闭区域Alpha采样；每版36端口射线在面板后20–40mm被内部结构挡住 | 两版ray-tests/shell-render-tests.json及light/dark/transparent PNG |
| 材质/纹理 | 原始与回读均Alpha1、Transmission0、OPAQUE、背面剔除；无颜色Alpha误连；14材质、7内嵌PNG，粗糙度/法线Non-Color、标签sRGB，法线强度0.18 | delivery-scene.json、glb-container.json |
| UV/文字 | 原始{o['uv_node_bindings_checked']}处UV节点绑定检查；读取轴与顶标签UV正向检验通过；保存重开后再次检查有效UV和packed依赖 | delivery-scene.json、packed-reopen.json、label-bake.json |
| 墨层间距 | 顶盖/标签真实世界边界实测{o['measured_label_gap_mm']:.9f}mm；视口near/far0.01/10m | delivery-scene.json、packed-reopen.json |
| 动态桌面 | 最终GLB材质模式25帧、24次实际15°旋转，首末姿态差{orbit['closure_angle_degrees']:.8f}°；最终主模型补充Solid/Material及拉手近看 | desktop/glb-material、desktop/final-master、desktop/final-master-solid |
| GLB容器 | glTF2长度/块边界有效；{e['nodes']}节点、{e['meshes']}网格、{e['unique_mesh_triangles']}不计实例复用的独立三角面；{e['bytes']:,}字节；7PNG解码；无摄影/测试节点 | export.json、glb-container.json、glb-scene.json |
| 主文件保存重开 | 主场景、材质视口、停止动画、纹理/字体资源打包及UV引用通过；最终桌面留下主模型 | packed-reopen.json、desktop/final-master-reopened.png |
| 归档 | 原始资料40项下载校验、图像/PDF/源码/离线链接/当前GLB哈希/交付清单检查 | source-integrity.json、archive-check.json、SHA256SUMS.txt |

表中JSON未写目录时均位于qa。几何零面积阈值1e-16m²，闭合实体signed-volume>0，数字尺寸测试容差0.01mm。glTF正常拆分同位置顶点；仅诊断BMesh副本以1e-7m焊接，正式导入网格保持原样。文字墨层与标签允许有意的开放边界，并有surface_role属性；不允许退化面。

## 真实图像对照

REVIEW.html将六面、四斜视和特写与对应原图/官方图并排。人工复核前面18个双笼，后面依次为PSU、3个风扇托盘、服务面板、PSU；管理SFP没有混入36业务口。NWR耳板每边3个水平长圆孔，正式装配保留4个侧面固定螺钉；孔后机身的正常遮挡没有为测试而删除。左右侧视依据世界坐标独立生成，没有水平翻转照片。

对照范围有限：左侧仅官方示意/实拍局部；右侧有无耳Serverlama库存照片；没有可信同型号底面。Abacus整体前后照片用于机身与模块布局，其不同耳片被排除。四斜视对照标明适用的面而不冒称每张存在同角度实拍。文字、非对称RJ45锁扣方向、USB竖向和标签灰/黄分区经单独查看。原始小字不做AI补全。

## 修复闭环与模式差异

1. 前面分块共面边造成黑线：重建连续厚面板，保留18个笼孔、260个下部通风孔和控制开口；微调相邻折边的装配关系。见front-refinement.json与before-refinement。后续渲染/桌面未见原共面条纹。
2. 初始灯光过曝：按中性world0.45和Key8W/Fill5.2W/Rim8W校准，曝光0、AgX Medium High Contrast。保留光照探针。没有提高金属Alpha或强行发光。
3. 笼体过高：依据NWR裸笼特写将外框高修为26.52mm/宽20.8mm；隐藏深度/触点仍为估计。低精度早期参考未成为结构权威。
4. 原照标签投影边界不准：显式SourcePhotoUV→LabelBakeUV烘焙，修正采样四边形，保留512×768源派生贴图；最终UV节点按名绑定。源照片无法提供的极小字没有恢复或虚构。
5. 曲线文字转换产生7个零面积三角形：删除这些无面积面及孤立边，不封堵真实字形孔洞；复查通过。见geometry-before-print-cleanup/print-degenerate-cleanup。
6. PSU管状拉手转弯出现扭折：原扫掠局部参考轴突变，改用连续固定横向截面与4mm弯曲半径；24周向分段、每90°16段。最终GLB在修正后导出，13张受影响全机/电源视图重渲染；旧图在before-handle-sweep-fix。见handle-sweep-fix、glb-detail-PSU-handle。
7. 平面法线首次检查错误地包含弯管，并漏计独立前面板的1mm壳深：修正测试覆盖范围，原失败报告保留。不是将失败实体改成双面。修正后的平面检查同时覆盖原版和回读版。
8. 原始Solid的25帧和原始Material的13帧是在最后拉手修正前取得，明确作为中间检查证据保留；最终GLB整圈和最终主文件补充截图证明修正后外观。q与−q按同一姿态计算，输入响应不代替视角查询。

Solid用于厚度/结构；Material Preview使用SceneWorld/SceneLights和Eevee局部AO（0.04m，factor1.25）。实时预览的笼腔可能比Cycles亮，反射与间接遮挡不同；最终Cycles可见正常暗腔。没有改变基础金属反射率来追逐不同渲染器的亮度。极细密孔网在远距桌面会有采样摩尔纹，放大后孔壁连续，Alpha/射线也证实真开孔；这与整片透明、错误背面剔除或共面闪烁不同。没有全局开启doubleSided。Cycles未提供OIDN，两个降噪开关均关闭，微量Monte Carlo噪点是已知渲染限制。

独立耳板孔中心Alpha要求<0.015、金属内部>0.985，避开抗锯齿边缘。孔边缘混合Alpha属于轮廓覆盖率。正式装配侧孔中的螺钉和机身都按命中对象检查；不会要求所有正式孔中心Alpha0。浅/深背景是对保留的RGBA图做显示空间Alpha合成，物体照明及Alpha不变。原始耳片未受拉手修复影响，其11张隔离图仍对应相同耳网格；测试夹具中的完整装配另已更新。

## 未被实物证实的部分

底面、裸壳深度分配、耳片外跨/厚度/孔距、壳厚、通风孔精细节距、隐藏笼内接触件与转子精细位置均为有标记估算。PSU选定PE2与蓝色排风，未知制造商子修订没有写入标签。铭牌极小字体、精密注塑筋/内部弹性机构及细小表面磨损未达到制造图复原级别。当前资产适用于设备外观与机柜三维展示，不是经实物测量的机械生产模型。
'''
text+='\nGit暂存范围检查通过：仅设备README与v001，18个LFS文件合计209914677字节，暂存指针、工作文件及本地LFS对象SHA256一致。见qa/staged-lfs-check.json；最终推送SHA由仓库历史和任务完成消息报告。\n'
(ROOT/'QA.md').write_text(text);print('QA summary written')
