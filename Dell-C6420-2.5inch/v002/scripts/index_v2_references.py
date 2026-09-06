from pathlib import Path
import shutil,json,hashlib,csv
from PIL import Image
p=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');r=p/'references'
old=['02-rear-v1','03-left-v1','04-right-v2','05-top-v2','06-bottom-inferred-v1','09-rear-left-v1','10-rear-right-v1','12-low-rear-inferred-v3','19-rear-ports-detail-v1','21-psu-detail-v1']
for n in old:
 dest=n if n!='05-top-v2' else '05-top-reused-v001-v2'
 shutil.copy2(r/'v001-archive/imagegen'/(n+'.png'),r/'imagegen'/(dest+'.png'))
 src=r/'v001-archive/prompts'/(n+'.txt')
 if src.exists():shutil.copy2(src,r/'prompts'/(dest+'.txt'))
selected=['01-front-v2','02-rear-v1','03-left-v1','04-right-v2','05-top-reused-v001-v2','06-bottom-inferred-v1','07-front-left-v2','08-front-right-v2','09-rear-left-v1','10-rear-right-v1','11-high-oblique-v2','12-low-rear-inferred-v3','13-structural-sketch-v4','14-assembly-sketch-v4','15-sections-sketch-v2','16-brand-detail-v2','17-filler-detail-v3','18-control-area-detail-v2','19-rear-ports-detail-v1','20-node-latch-detail-v2','21-psu-detail-v1','22-vent-detail-v2']
(r/'SELECTED.txt').write_text(''.join('imagegen/'+s+'.png\n' for s in selected))
notes={
 '01':'Counted24 black fillers; front only; logo not used as texture.',
 '02':'Four nodes,2stackedcentralPSUs, inletleft/fanright rear-observer; no mirrored nodes.',
 '03':'Left side extrapolation; macro hardware locations from evidence/estimates, not AI.',
 '04':'Right side directioncorrect; details not measured from AI.',
 '05':'Reused true overhead portrait v001 reference. Top orthogonal direction suitable; sticker words and small stamp geometry are AI approximations and excluded from model. Actual stickers use original NSL photo UV.',
 '06':'Explicit AI inferred underside, no real bottom photos.',
 '07':'Frontleft;24blackfillers; left side details inferred.',
 '08':'Frontright;24blackfillers; no added NIC/frontcarrier options.',
 '09':'Rearleft;4nodes2PSUs; original photos remain authoritative.',
 '10':'Rearright;same rear handedness; side estimate.',
 '11':'Elevated front view;24blackfillers; structural surface photo reference auxiliary.',
 '12':'Low rearLEFT, despite original requested opposite. Correct view named inmanifest. Bottominferred.',
 '13':'Corrected schematic4banks x6bays, letteringcorrect; deliberately simple allocation sketch, no exact geometry implied.',
 '14':'Corrected assembly sidecutaway: plasticfillersfrontleft,4nodeswithdrawrear-right, correct6blockrear allocation. Projection overlap explicitlymarked.',
 '15':'0.8–1.0mm assumption clearlylabelled;solidplasticfiller nooldcarrier.',
 '16':'DELL EMC/C6400 and1/2/3/4 directioncorrect, poweroff. ONLY brand/control arrangement adopted; illustrated mountingflange not used. Brand textures areofficial realasset.',
 '17':'Singlemacro3fillers fullheight; upperinset,longraisedpad,lowerfoot. No newholes/silverlever.',
 '18':'Left controlandadjacentblackfillers;photoreal grain reference. NoAIprintedglyphtexture.',
 '19':'Same nodeport handedness; text and exactapertures readfromreal1800pxrear, not AI.',
 '20':'Plainbluepaddle/blacklonggrip selected. Neighborpowerlens looks screwlike; EXCLUDED from adoption, actual circularpowerlens used fromphoto. Microprint excluded.',
 '21':'Correct2400W fan/inlet side and wovenstrap. Label texture comesfromactualphoto.',
 '22':'Roundedpunches,foldthickness andcutedge only. Generator simplifiedloweraperturelayout; notusedasnodeportlayout. Exactrearplate tracesrealphoto.'}
reject={'05-top-v2':'FAIL front unfolded into top.','05-top-v3':'FAIL overall top aspectratio; preserved as rejected stamp discussion only.','13-structural-sketch-v2':'FAIL geometry/projection and bay count uncertain.','13-structural-sketch-v3':'FAIL28bays vs24.','14-assembly-sketch-v2':'FAIL rearIO facesfront.','14-assembly-sketch-v3':'FAIL PSUghosts misplaced ahead ofnodes.','17-filler-detail-v2':'FAIL montage notindependent fullheight detail.'}
manifest=[]
for f in sorted((r/'imagegen').glob('*.png')):
 n=f.stem;im=Image.open(f);manifest.append({'file':str(f.relative_to(p)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'pixels':im.size,'selected':n in selected,'role':'AI AUXILIARY REFERENCE; not photograph/CAD/texture','origin':'retained v001 imagegen' if n in old or 'reused' in n else 'built-in imagegen v002','prompt':str((r/'prompts'/(n+'.txt')).relative_to(p)),'review':notes.get(n[:2],'') if n in selected else reject.get(n,'Not selected')})
(r/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
(r/'REVIEW.md').write_text('# v002 参考审查\n\n全部是内置 imagegen 实际生成；22项选用清单已覆盖六视图、四斜视、俯仰、3张草图及7类细节。真实照片/官方尺寸始终为几何权威；局部使用范围逐项限定，AI文字不用作材质。v002新增19张，另保留原批次来源。\n\n'+''.join('- '+s+': '+notes[s[:2]]+'\n' for s in selected)+'\n## 退回图\n'+''.join('- '+k+': '+v+'\n' for k,v in reject.items()))
# Carry old authoritative source index with portable version paths and append actual new downloads.
f=p/'sources.csv';rows=list(csv.DictReader(f.open()));fields=list(rows[0])
for row in rows:
 for k,v in row.items():row[k]=v.replace('/v001/','/v002/')
(p/'sources-v001-reindexed.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with f.open('w',newline='') as out:
 w=csv.DictWriter(out,fieldnames=fields);w.writeheader();w.writerows(rows)
extra=json.loads((p/'sources/third_party/v2-supplement-downloads.json').read_text())
for e in extra:
 e['source_type']='third-party real photograph'
 e['adoption']='Auxiliary mechanical/photo detail only; locked rear remains NSL/ETB'
 if e['name'].startswith('techbuyer'):
  e['adoption']='Front/lid auxiliary only. Rearimage04 has different IO layout from locked C6420 source and is excluded; listing metadata not blindly trusted.'
 if e['name'].startswith('itc'):e['adoption']='Front filler/ear macro adopted; chrome captive screw variant excluded; selected black screw fromNSL.'
 if e['name'].startswith('bargain'):e['adoption']='Sled-extraction/steel construction secondary. PSU1600W or unpopulatedNIC options excluded.'
(p/'sources/v002-supplement-index.json').write_text(json.dumps(extra,ensure_ascii=False,indent=2))
print('Selected22, totalv002',len(manifest),'newdownloads',len(extra))
