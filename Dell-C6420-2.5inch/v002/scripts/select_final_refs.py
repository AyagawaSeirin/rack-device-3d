from pathlib import Path
import shutil,json,hashlib
from PIL import Image
p=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');r=p/'references'
shutil.copy2(r/'SELECTED.txt',r/'SELECTED-SUPERSEDED-BLANKS.txt')
reused=['01-front-v3','07-front-left-v1','08-front-right-v1','11-high-oblique-v2','14-assembly-sketch-v2','15-sections-sketch-v1','17-carrier-detail-v1']
for n in reused:
 dest=n+'-normal-reused'
 shutil.copy2(r/'v001-archive/imagegen'/(n+'.png'),r/'imagegen'/(dest+'.png'))
 if (r/'v001-archive/prompts'/(n+'.txt')).exists():shutil.copy2(r/'v001-archive/prompts'/(n+'.txt'),r/'prompts'/(dest+'.txt'))
selected=['01-front-v3-normal-reused','02-rear-v1','03-left-v1','04-right-v2','05-top-reused-v001-v2','06-bottom-inferred-v1','07-front-left-v1-normal-reused','08-front-right-v1-normal-reused','09-rear-left-v1','10-rear-right-v1','11-high-oblique-v2-normal-reused','12-low-rear-inferred-v3','13-structural-sketch-v4','14-assembly-sketch-v2-normal-reused','15-sections-sketch-v1-normal-reused','16-brand-detail-v2','17-carrier-detail-v1-normal-reused','18-left-control-only-v4','19-rear-ports-detail-v1','20-node-latch-detail-v2','21-psu-detail-v1','22-vent-detail-v2']
(r/'SELECTED.txt').write_text(''.join('imagegen/'+n+'.png\n' for n in selected))
old=json.loads((r/'manifest.json').read_text());prev={Path(e['file']).stem:e for e in old};records=[]
for f in sorted((r/'imagegen').glob('*.png')):
 name=f.stem;e=prev.get(name,{})
 e.update(file=str(f.relative_to(p)),selected=name in selected,pixels=Image.open(f).size,sha256=hashlib.sha256(f.read_bytes()).hexdigest(),role='AI辅助建模参考；不是实拍、尺寸依据或纹理源',prompt=str((r/'prompts'/(name+'.txt')).relative_to(p)))
 if name in selected:
  if 'normal-reused' in name:e['review']='用户明确要求正常盘架后重新采用已生成的24SFF正常托架参考；不采用已退回模型几何。盘数/形态对照官方与Bargain实拍，微小文字仍用真实资产。'
  if name=='18-left-control-only-v4':e['review']='单独左控制区：DELL EMC/1/2及4按钮方向正确；照片/官方原图决定最终字形。'
 else:
  if name in ['01-front-normal-carriers-v3','17-normal-carrier-detail-v3','18-control-normal-carrier-detail-v3']:e['review']='退回：分别出现22个盘架/4个拉手开窗/4开窗及错误按钮符号，未作为模型依据。'
  elif any(s in name for s in ['filler','front-v2','front-left-v2','front-right-v2','high-oblique-v2','sections-sketch-v2','assembly-sketch-v4']):e['review']='用户纠正后废止塑料填充件方案；不用于最终正常盘架模型。'
 records.append(e)
(r/'manifest.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))
(r/'REVIEW-FINAL.md').write_text('# 最终参考状态：正常热插拔托架\n\n用户要求正面使用正常盘架，不使用塑料填充件；此文优先于早期REVIEW.md。选用22项详见SELECTED.txt。保留所有退回/废止图，避免伪装成最终参考。\n\n正面/前斜视/托架与装配截面采用已有的正常托架imagegen参考，并用新下载的实拍校对。结构与材质全部由v002脚本重建。v002另实际新生成23张，涉及配置修正及参考重做；不以所有生成都成功来冒充质量通过。\n\nAI文字、细孔绝对位置、比例均不用于精确测量。顶部图只作观察方向参考，铭牌用原始NSL照片的投影UV；底面仍明确AI推测。19/20/22接口相邻区域的AI文字或示意差异不采用，最终节点依据1800pxETB实拍。\n')
(p/'CONFIGURATION.md').write_text('''# 最终锁定配置\n\nDell PowerEdge C6420 四合一整机：4个C6420计算节点装在C6400机箱内，24×2.5英寸前置盘位。用户明确要求24个正常热插拔硬盘托架，不使用塑料填充件。前部为Dell14G/DXD9H式三个拉手开窗、后置蜂窝网、银色金属杠杆、顶部橙圈释放按钮的正常托架外观。以Dell维护手册p7/p9及BargainHardware24SFF整机实拍确认；兼容托架的开合照片只用于理解钢片/铰链构造，未把其商家标志或无品牌身份当成原厂铭牌。未猜硬盘容量/序列号。\n\nNSL原始前照装有塑料填充件，仅用于机箱、侧面、顶盖、挂耳；这一前部状态已被用户明确替换。Bargain照片的连续0–23编号/1600W选件不照搬：最终为四节点直连映射1-0…4-5及已锁定2400W后部。\n\n后部始终以NSL/ETB同一拍摄实体为依据：4节点2×2排列，中央2只上下叠放2400W EPP电源；后视观察者看电源左侧AC入口/橙锁扣、右侧风扇。各节点相同方向：左侧2USB-A，旁边2SFP，蓝色抽拉件，微USB、miniDP、RJ45、圆形电源键，黑色长凹槽。NIC精确速率未知，不印猜测型号。\n\n品牌保留原位DELL EMC与C6400，外壳C6400不改成C6420。节点/整机名称在组件与文档中正确标识C6420。\n\n已知证据缺口：没有真实整机底面；采用通用连续钢板和4条内凹加强筋并标推测。左侧局部孔位、隐蔽厚度与微观表面是估算。顶盖标签使用真实照片原像素，微小字受原图分辨率限制，没有AI补字或虚构铭牌。\n''')
(p.parent/'README.md').write_text('# DELL PowerEdge C6420 四节点整机\n\nv001 已被用户退回，保留历史记录。v002 写实重做正在执行。\n\n最终要求：四个C6420节点，C6400的24×2.5英寸机箱，正面24个正常热插拔硬盘托架；不得交付塑料填充件。\n')
print('Final selected',len(selected),'all assets',len(records))
