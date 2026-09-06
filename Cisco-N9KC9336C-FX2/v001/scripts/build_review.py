from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1];h=html.escape
views=['front','rear','left','right','top','bottom-INFERRED','front-left','front-right','rear-left','rear-right','high-oblique','low-oblique-INFERRED','detail-brand-controls','detail-qsfp28','detail-rear-management','detail-left-ear-front','detail-right-ear-back','detail-fan-module','detail-AC-power-supply','detail-top-ventilation']
src={
'front':('sources/third_party/abacus-1.webp','Abacus：同机型端口面；该照片挂耳方案未采用。'),
'rear':('sources/third_party/nwr-1.jpg','NWR：同一蓝色排风配置；3风扇、2AC电源及后管理接口。'),
'left':('sources/official/overview-501591.jpg','官方后左示意图：左侧仅局部证据，孔位为比例估计。'),
'right':('sources/third_party/serverlama-angledside.jpg','Serverlama：同机型右侧，无挂耳；不用于选定挂耳或电源。'),
 'top':('sources/third_party/nwr-2.jpg','NWR：顶面与前面；拆出的模块遮挡局部顶盖。'),
'front-left':('sources/third_party/nwr-3.jpg','NWR：仅前左品牌、空端口、左耳局部，不能证明整个左侧。'),
'front-right':('sources/third_party/nwr-2.jpg','NWR：前面、顶面、右侧局部。'),
'rear-left':('sources/third_party/abacus-3.webp','Abacus：后部/顶面轮廓复核；该图不同耳套件不采用。'),
'rear-right':('sources/third_party/nwr-1.jpg','NWR：后部/顶面轮廓复核；非相同相机角度，不作像素相似度证明。'),
'detail-brand-controls':('sources/third_party/nwr-3.jpg','Cisco桥形标识、PID、LS/BCN/STS/ENV及lane1–4来自实拍。'),
'detail-qsfp28':('sources/third_party/nwr-3.jpg','金属双笼外框、隔板两排孔可证；隐藏接触件和深度为估计。'),
'detail-left-ear-front':('sources/third_party/nwr-3.jpg','3个水平长圆通孔；厚度与孔壁细节为估计。'),
'detail-right-ear-back':('sources/official/install-501768.jpg','选定传统安装套件示意；4个安装螺钉，其余选择孔为估计。'),
'detail-rear-management':('sources/third_party/nwr-1.jpg','上RJ45 Console，下RJ45 management，旁边SFP和竖USB-A。'),
'detail-fan-module':('sources/third_party/nwr-1.jpg','3个65CFM-PE托盘，内部6个转子与3个模块分开计数。'),
'detail-AC-power-supply':('sources/third_party/nwr-1.jpg','匹配银色AC电源；尼龙线缆固定带收起。未知制造商修订不虚构。'),
'detail-top-ventilation':('sources/third_party/nwr-2.jpg','前端穿孔带；实际孔数、节距、板厚无制造图，按比例估计。')}
css='body{font:16px/1.6 system-ui,sans-serif;max-width:1500px;margin:32px auto;padding:0 24px;color:#20262b;background:#fafafa}a{color:#00677b}nav{display:flex;gap:20px;flex-wrap:wrap;margin:20px 0}h1{font-size:34px}h2{font-size:24px;margin-top:44px}figure{margin:0}img{max-width:100%;height:auto}section{padding:24px 0;border-top:1px solid #c6cbd0}.pair{display:grid;grid-template-columns:1fr 1fr;gap:20px}.pair img{width:100%;max-height:650px;object-fit:contain;background:#eee}figcaption{font-size:14px}button,input{font:inherit;margin:8px 8px 8px 0}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #ccc;text-align:left;padding:8px}.links{display:flex;gap:12px;flex-wrap:wrap}.frame{max-height:760px;display:block;margin:auto}small{color:#565e65}@media(max-width:800px){.pair{grid-template-columns:1fr}}'
a=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>N9K-C9336C-FX2 · v001</title><style>'+css+'</style><body>', '<h1>Cisco Nexus N9K-C9336C-FX2 · v001</h1><p>可编辑三维装配与原始证据对照。36个空QSFP28、3个双转子风扇模块、2个匹配AC电源、蓝色port-side exhaust、传统端口端挂耳。</p><p>底面为推测；未测量孔位、厚度及内部细节为估算。极小铭牌文字受真实源照片清晰度限制。生成参考不作为尺寸和文字证据。</p>', '<nav><a href="model/CISCO-Nexus-N9K-C9336C-FX2.blend">主Blender文件</a><a href="model/CISCO-Nexus-N9K-C9336C-FX2.glb">GLB</a><a href="QA.md">QA说明</a><a href="DIMENSIONS.md">尺寸</a><a href="EVIDENCE.md">证据范围</a><a href="imagegen/REVIEW.html">49次生成与23张选定参考</a><a href="#desktop">真实桌面记录</a><a href="#qa">测试图</a></nav>']
for name in views:
 p='previews/'+name+'.png';assert (ROOT/p).is_file(),p
 a+=['<section><h2>'+h(name)+'</h2><div class="pair"><figure><a href="'+p+'"><img loading="lazy" src="'+p+'"></a><figcaption>Blender Cycles渲染。中性浅灰背景；点击原图。</figcaption></figure>']
 if name in src:
  path,note=src[name];assert (ROOT/path).exists(),path;a+=['<figure><a href="'+path+'"><img loading="lazy" src="'+path+'"></a><figcaption>原始证据：'+h(note)+'</figcaption></figure>']
 else:a+=['<p>'+('无可信实拍底面，明确为推测钣金结构。' if 'INFERRED' in name else '组合俯视用于检查全机轮廓；实物证据见顶面与前面。')+'</p>']
 a+=['</div></section>']
a+=['<section id="desktop"><h2>真实桌面输入与原始截图</h2><p>实际server_desktop键盘输入；每帧由Blender查询视口四元数。GLB材质环绕为最终几何；original-solid/original-material是最后拉手修复前的中间记录。Solid与GLB整圈各24步，q与−q按相同姿态计算。下方播放的是已归档桌面截图，未用相机渲染替代。</p>'];sets={}
for d in sorted((ROOT/'desktop').iterdir()):
 if d.is_dir() and (d/'frames.json').exists():
  frames=json.loads((d/'frames.json').read_text());sets[d.name]=frames;a+=['<button onclick="choose('+h(json.dumps(d.name))+')">'+h(d.name)+'</button>']
a+=['<div><button onclick="step(-1)">上一帧</button><button onclick="toggle()" id="play">播放</button><button onclick="step(1)">下一帧</button><input id="slider" type="range" min="0" value="0" oninput="show(+this.value)"><span id="pose"></span></div><a id="raw"><img class="frame" id="frame"></a><p class="links">']
for k in sets:a+=['<a href="desktop/'+k+'/frames.json">'+h(k)+'姿态</a><a href="desktop/'+k+'/input-log.json">输入日志</a>']
a+=['</p></section><section id="qa"><h2>孔洞及不透明度测试</h2><p>隔离耳板移除的只是测试副本的螺钉；正式装配中的螺钉、机壳遮挡均保留。Alpha只在无遮挡孔中心和金属内部采样。</p>']
for prefix in ['original','glb']:
 a+=['<h3>'+prefix+'</h3><div class="links">']
 for f in sorted((ROOT/'qa').glob(prefix+'-ear-*.png')):a+=['<a href="qa/'+f.name+'">'+h(f.stem)+'</a>']
 for f in sorted((ROOT/'qa').glob(prefix+'-shell-*.png')):a+=['<a href="qa/'+f.name+'">'+h(f.stem)+'</a>']
 a+=['</div>']
a+=['<p><a href="qa/glb-detail-brand.png">GLB品牌回读特写</a> · <a href="qa/glb-detail-PSU-handle.png">GLB修正拉手特写</a> · <a href="qa/final-contact-sheet.png">20视图总览</a></p></section><script>const sets='+json.dumps(sets,ensure_ascii=False)+';let key=Object.keys(sets)[0],i=0,t=null;function show(n){let f=sets[key];i=(n+f.length)%f.length;let x=f[i];document.getElementById("frame").src=x.screenshot;document.getElementById("raw").href=x.screenshot;document.getElementById("slider").max=f.length-1;document.getElementById("slider").value=i;document.getElementById("pose").textContent=key+" · "+i+" · "+x.mode+" · "+(x.name||"");}function step(d){show(i+d)}function choose(k){key=k;show(0)}function toggle(){if(t){clearInterval(t);t=null}else{t=setInterval(()=>step(1),700)}document.getElementById("play").textContent=t?"暂停":"播放";}if(key)show(0);</script></body></html>']
(ROOT/'REVIEW.html').write_text('\n'.join(a));print('REVIEW built',len(views),'render views',len(sets),'desktop sets')
