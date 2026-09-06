import pathlib,json,csv,html,hashlib,struct
from PIL import Image
P=pathlib.Path('/root/Blender/DELL-C6420/v001')
a=json.loads((P/'qa/original-scene-audit.json').read_text());g=json.loads((P/'qa/glb-geometry-audit.json').read_text());o=json.loads((P/'qa/glb-orientation-audit.json').read_text());m=json.loads((P/'qa/measured-dimensions.json').read_text());alpha=json.loads((P/'qa/alpha-pixel-results.json').read_text());st=json.loads((P/'qa/glb-structure.json').read_text())
assert not a['geometry_flags'] and not g['geometric_flags_after_position_weld_copy'] and not st['alpha_failures'] and alpha['failures']==0
assert o['image_uv_failures']==o['text_axis_failures']==g['missed_shell_probes']==0
# Expand source index to individually identify every extracted PDF evidence page.
with (P/'sources.csv').open() as f:rows=[r for r in csv.DictReader(f) if r['source_type']!='Dell PDF page raster extraction'];fields=list(rows[0])
page_map={'technical-guide.pdf':'13 Fig1;14 Fig3/4;66 Fig11 Table31;67 PSU table','technical-specifications.pdf':'5 Fig1/Table1','c6420-technical-guide-older.pdf':'9/10 chassis views;34 dimensions','c6420-spec-sheet.pdf':'2 chassis options and 790 mm nominal depth','c6420-service-manual.pdf':'8/9 rear ports;14/15 service labels','c6400-service-manual.pdf':'7 Fig2/4 front/control;9 Fig5/6 rear/drive mapping;14-16 labels','c6420-technical-specifications.pdf':'4 Fig1/Table1 sled dimensions','hpc-design-whitepaper.pdf':'context only; not used as dimension authority'}
urls={pathlib.Path(r['local_path']).stem:r['asset_url'] for r in rows if r['source_type'].startswith('Dell official')}
for r in rows:
 if r['source_type'].startswith('Dell official'):r['pdf_page']=page_map.get(pathlib.Path(r['local_path']).name,r['pdf_page'])
for f in sorted((P/'sources/extracted').glob('*-p[0-9][0-9][0-9].png')):
 stem,page=f.stem.rsplit('-p',1)
 if stem not in urls:continue
 rows.append(dict(source_page=urls[stem],asset_url=urls[stem]+'#page='+str(int(page)),local_path=str(f.relative_to(P)),source_type='Dell PDF page raster extraction',view='Document diagram/table; page-specific content',actual_model='C6400 enclosure / C6420 subset; document may include other variants',node_count='4 target; single-node diagrams used only for components',drive_config='Only 24x2.5 subset adopted; 12x3.5 diagrams excluded',pdf_page=str(int(page)),confirmed_details='Original PDF page raster. See CONFIGURATION.md for which region is used.',confidence='high official; configuration must be filtered',status='verified PNG from verified PDF'))
with (P/'sources.csv').open('w',newline='') as f:w=csv.DictWriter(f,fields);w.writeheader();w.writerows(rows)
tex=[]
for f in (P/'textures').glob('*.png'):
 im=Image.open(f);tex.append({'file':str(f.relative_to(P)),'size':list(im.size),'bytes':f.stat().st_size})
(P/'qa/texture-inventory.json').write_text(json.dumps(tex,indent=2))
readme='''# DELL PowerEdge C6420 四节点整机 · 24 × 2.5 英寸

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
- references/manifest.json：每张图的提示词、真实输入/生成输入、版本、原始工具输出路径、用途和 SHA256；prompts/ 保存完整提示词；qa-log.md 逐图说明采用范围和拒用原因。
- model：阶段文件、最终 .blend / GLB 及参数表；textures：独立准确图文资产。
- previews：六面、四斜视、俯仰视和重要细节，共 16 张 Cycles 预览。
- desktop：实际 server_desktop MCP 操作截图、25 帧 360° 序列；qa：GLB 独立重导入项目、浅深背景图、几何/尺寸/UV/Alpha 检查及修复记录。
- backups：开始前未保存的原场景副本和修复前导出，未覆盖原来的 setup-check.blend。

## 复现

主要脚本是 scripts/build_c6420.py。它读取 model/parameters.json 的主体尺寸，以循环和可复用几何函数生成部件；进一步细节偏移在脚本中明确以米记录。脚本随后调用 repair_geometry.py、refine_finish.py、prepare_triangles.py。最终由 export_deliverables.py 保存和导出。重建会重新创建当前场景，应在副本上执行。

实际执行使用的是已连接的 Blender MCP；本机协议调用入口也可复现：

```bash
/root/.local/share/uv/tools/blender-mcp/bin/python /root/.local/share/blender-mcp-setup/mcp_call.py blender execute_blender_code --code-file /root/Blender/DELL-C6420/v001/scripts/build_c6420.py
/root/.local/share/uv/tools/blender-mcp/bin/python /root/.local/share/blender-mcp-setup/mcp_call.py blender execute_blender_code --code-file /root/Blender/DELL-C6420/v001/scripts/export_deliverables.py
```

渲染脚本为 render_previews.py；桌面真实旋转采集脚本为 desktop_orbit_mcp.py（执行前光标应位于已检查的 3D 视区）。该脚本实际经 server_desktop MCP 发送键盘输入并保存桌面截图，没有用 bpy 相机运动冒充 computer use。建模始终在原 XRDP Blender 实例中进行；后台 Blender 进程仅用于批量 CPU 渲染。Cycles 已关闭此环境不支持的降噪。

来源图片/官方图文与 DELL 商标的权利属于原权利人，来源及派生关系均保留。
'''
(P/'README.md').write_text(readme)
qa=f'''# QA · DELL C6420 4N / 24SFF

最终模型审计和 GLB 重新导入检查已完成。以下“通过”针对实际执行的检查范围，不等同于制造公差认证。

|检查|结论|证据与处理|
|---|---|---|
|目标/数量|通过|24 个载架、4 个 C6420 节点、2 个 PSU；original-scene-audit.json 与 glb-reimport-audit.json 一致|
|整机外包尺寸|通过|X {m['whole']['dimensions_mm'][0]:.6f}、Y {m['whole']['dimensions_mm'][1]:.6f}、Z {m['whole']['dimensions_mm'][2]:.6f} mm；数值误差均小于0.001mm；measured-dimensions.json|
|节点尺寸|通过|四节点宽174.4、高40.5、含把手深574.5mm；已校正0.325mm前缘偏差，triangulation-repairs.json|
|Blender 几何|通过|{a['object_count']}个网格、{a['triangle_count']:,}三角面；未说明的开放边界/负变换/退化面标记0；对象内部精确重复面0|
|导出后三角化|通过|首版GLB检出退化三角形；已预先清理共线细分并三角化，二次导入 geometric_flags=0；glb-geometry-before-fix.json、glb-geometry-audit.json|
|图片、文字、UV镜像|通过|5组图片UV、51处文字阅读轴均正确；glb-orientation-audit.json；brand-detail.png；没有水平翻转原图来补视角|
|透明/穿透|通过|18个材质均OPAQUE、Alpha=1、Transmission=0，无负缩放；30个外壳射线探针全命中；9组表面像素Alpha均255；glb-structure.json、alpha-pixel-results.json|
|孔洞/厚度|通过外观检查|真实方形/蜂窝穿孔，有板厚与后方遮挡；未使用机身透明或六面照片立方体；面板接缝有内部搭接|
|连续旋转|通过已记录检查|实际MCP键盘24次15°环绕，25张原始桌面PNG；0°与360°姿态四元数相差符号而代表同一朝向；另有拖拽俯仰、缩放和GLB掠射角截图|
|Solid / Material / Rendered|通过对照|desktop/03、06、07、09、10、11、13及最终Cycles；材质预览亮孔与窄高光在Cycles呈真实深腔，属于环境反射/采样差异|
|浅/深背景|通过|glb-front-right-light/dark、glb-rear-left-light/dark；实心表面不会随背景显露背后结构|
|独立GLB复开|通过|qa/GLB-reimport-verification.blend 的独立场景；1089个网格、24/4/2组件、5贴图、尺寸与原模型一致|
|六面与四斜视|完成检查，有证据限制|REVIEW.html并排展示来源/模型；前/后/右/顶有同配置照片或官方图，左/底及部分斜视缺独立实拍，未伪装成全部有实拍|

## 修复记录

1. 原始电源占位实体遮住风扇/插口内腔：替换为有厚度的侧/顶/底外壳，增加真实黑色插口框和后方风扇。
2. 顶盖接缝可能透视：增加内部搭接片；不应透视的表面采用连续不透明板材。
3. 曲线/文字转换的端盖分裂及退化细分：焊接实际端盖，文字改为有明确语义的表面油墨；印刷面保留合理开放边界，未全局双面掩盖反法线。
4. GLB三角化额外产生的退化三角形：在源几何中清理共线划分、显式三角化，然后重新导出、重新导入、重新审计。
5. 主体包围盒：将装饰凸起纳入86.8mm高范围，调整后抽拉环到824.1mm总深；节点深度修正至574.5mm。
6. imagegen中的盘位数量、错误展开顶视、虚构黑把手和结构草图拼写：错误版拒用，重生修正；全部版本和逐张结论保留。

## 限制与推测

- **底面为推测**，不是原厂测绘。侧板微孔、冲压、螺钉、网孔节距、板厚和接口内芯几何均含按比例估算；不能用来加工生产。
- 内部仅满足外观与开口遮挡；未做隐藏电路、散热器和制造级全零件碰撞验证。明显外露穿插已经通过多角度检查；螺钉、搭接和铰链存在有意装配接触。
- 顶盖官方服务图文的排版简化，未复刻模糊微字；已知品牌字形用原图，未使用AI字形作为真实贴图。
- 未确认SFP网卡芯片/速率，未编造型号、容量或序列号。
- 软件OpenGL远距细孔/金属窄高光仍可能出现像素级摩尔纹或跳动；已提高视口采样并用近距、Solid和Cycles核对。未发现大面Z-fighting、异常透明或反法线造成的可见缺面。
- 实拍参考存在盘位填充件与正式载架的状态差别，选择与依据见CONFIGURATION.md；没有混用3.5英寸机箱或其他代节点。

最终GLB：{st['file_bytes']:,}字节，SHA256 `{st['sha256']}`。未启用Draco压缩；本环境可选Draco库缺失不影响本次标准未压缩GLB。纹理尺寸见texture-inventory.json。所有JSON都保留实际数值和检查范围。
'''
(P/'QA.md').write_text(qa)
# Offline report with untouched original evidence. Images are referenced, not raster-edited.
head='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>C6420 外观与验证</title><style>body{font:16px/1.6 system-ui,sans-serif;margin:32px auto;max-width:1360px;padding:0 24px;background:#f7f7f5;color:#202426}h1{font-size:30px}h2{margin-top:44px}a{color:#176185}img{max-width:100%;height:auto;background:#ddd}figure{margin:0}figcaption{padding:7px 0;color:#555}section.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin:20px 0}.all{display:grid;grid-template-columns:repeat(3,1fr);gap:14px}button,input{font:inherit;margin:8px}#orbit{width:100%;max-height:700px;object-fit:contain}table{border-collapse:collapse}td,th{padding:9px;border:1px solid #ccc}@media(max-width:760px){section.grid,.all{grid-template-columns:1fr}}</style><h1>Dell PowerEdge C6420 · 四节点 · 24 × 2.5 英寸</h1><p><a href="README.md">交付说明</a> · <a href="QA.md">QA报告</a> · <a href="DIMENSIONS.md">尺寸</a> · <a href="sources.csv">来源索引</a></p><p>真实资料、AI辅助参考与模型渲染分别标注。缺失实拍的面不宣称已经实拍确认。</p>'''
parts=[head]
def fig(src,caption):return f'<figure><a href="{html.escape(src)}"><img loading="lazy" src="{html.escape(src)}"></a><figcaption>{html.escape(caption)}</figcaption></figure>'
comparisons=[('正面','sources/extracted/official-front-24sff.png','Dell官方24SFF载架正面（文档提取）','previews/front.png'),('后面','sources/third_party/nsl-_6400_back.png','锁定同配置整机实拍：4节点、中央2×2400W、每节点双SFP','previews/rear.png'),('右侧/前右斜视','sources/third_party/nsl-_6400_2.png','实拍右侧与顶部；照片前部为填充件状态','previews/front-right.png'),('左侧','references/imagegen/03-left-v1.png','AI辅助左视，侧板微孔估算；没有独立同配置左正面实拍','previews/left.png'),('右侧正视','sources/third_party/nsl-_6400_2.png','右側實拍可见区域，非严格正投影','previews/right.png'),('顶面','sources/third_party/nsl-C6400.png','实拍可见顶盖；模型服务图文版式简化','previews/top.png'),('底面','references/imagegen/06-bottom-inferred-v1.png','AI推测底面，非真实照片','previews/bottom.png'),('前左斜视','references/imagegen/07-front-left-v1.png','AI辅助独立前左斜视；外观/尺寸以官方及已得实拍为准','previews/front-left.png'),('后左斜视','sources/third_party/nsl-_6400_back.png','后部实拍依据；模型换成后左观察角','previews/rear-left.png'),('后右斜视','sources/third_party/nsl-_6400_back.png','后部实拍依据；模型换成后右观察角，节点不镜像','previews/rear-right.png')]
for title,src,caption,model in comparisons:parts.extend([f'<h2>{title}</h2><section class="grid">',fig(src,caption),fig(model,'Blender模型 · '+title),'</section>'])
parts.append('<h2>局部渲染</h2><div class="all">')
for name in ['brand-detail','carrier-detail','rear-node-detail','psu-detail','high-front','low-rear']:parts.append(fig('previews/'+name+'.png','模型渲染 · '+name))
parts.append('</div><h2>GLB重新导入后的浅/深背景</h2><section class="grid">')
for name in ['front-right-light','front-right-dark','rear-left-light','rear-left-dark']:parts.append(fig('qa/glb-'+name+'.png','GLB重新导入 · '+name))
parts.append('''</section><h2>真实桌面360°序列</h2><p>25张未经图像生成或修图的MCP桌面截图，24次键盘旋转；每次15°。点击图片可打开原始文件。该序列是在最终可见几何上采集，随后仅清理了不可见微小三角化和节点前缘误差，GLB另有重新导入检查。</p><button id="play">播放 / 暂停</button><input id="frame" type="range" min="0" max="24" value="0"><span id="angle">0°</span><a id="raw" href="desktop/turntable-material/frame-000.png"><img id="orbit" src="desktop/turntable-material/frame-000.png"></a><script>const slider=document.getElementById('frame'),pic=document.getElementById('orbit'),raw=document.getElementById('raw'),angle=document.getElementById('angle');function show(i){slider.value=i;pic.src='desktop/turntable-material/frame-'+String(i).padStart(3,'0')+'.png';raw.href=pic.src;angle.textContent=(i*15)+'°';}slider.oninput=()=>show(+slider.value);let timer=null;document.getElementById('play').onclick=()=>{if(timer){clearInterval(timer);timer=null;}else timer=setInterval(()=>show((+slider.value+1)%25),450);};</script><h2>全部 imagegen 最终采用参考</h2><p>22项独立资产；带有“推测”的图不作原厂结构证据。完整提示词与纠错记录在 references/ 中。</p><div class="all">''')
for line in (P/'references/SELECTED.txt').read_text().splitlines():parts.append(fig('references/'+line,'AI辅助参考 · '+pathlib.Path(line).stem))
parts.append('</div></html>');(P/'REVIEW.html').write_text('\n'.join(parts))
print('README, QA and offline REVIEW written; source index',len(rows),'records')
