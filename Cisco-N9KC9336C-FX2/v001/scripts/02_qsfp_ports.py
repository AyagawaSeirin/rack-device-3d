from pathlib import Path
import sys,importlib,bpy,math,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import model_lib as L;importlib.reload(L)
from model_lib import *
assert not bpy.data.collections.get('03_QSFP28'), 'Inspect completed stage before rerun'
C='03_QSFP28';root=bpy.data.objects['N9K-C9336C-FX2'];allports=empty('36_BUSINESS_QSFP28_PORTS',C,'business_port_bank');allports.parent=root
# Fix two seam issues discovered in reviewing the shell construction parameters.
if bpy.data.objects.get('Lid_vent_transition'):bpy.data.objects.remove(bpy.data.objects['Lid_vent_transition'],do_unlink=True)
o=bpy.data.objects['Front_lower_control_label_land'];o.dimensions.x=.03371;o.location.x=-.202855
bpy.context.view_layer.objects.active=o;o.select_set(True);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.select_set(False)
protos=[];x=-189
cage=frame('Pair01_stainless_shell_29mm_deep',20.8,31.2,29,.32,(x,-280.5,23.4),C,'Cage stainless steel',radius=.42);protos.append(cage)
sep=box('Pair01_front_separator_true_perforations',(20.16,.45,7),(x,-294.62,23.4),C,'Cage stainless steel')
for xx in [-4.05,-1.35,1.35,4.05]:
 for zz in [-.90,.90]:cut(sep,prism('separator_slot_tool',rounded_rect(1.85,.85,.25,4),3,(x+xx,-294.6,23.4+zz),C,plane='XZ'))
for sign in [-1,1]:
 cut(sep,prism('separator_triangle_tool',[(-.82,-1.28),(.82,-1.28),(0,1.28)] if sign<0 else [(-.82,1.28),(.82,1.28),(0,-1.28)],3,(x+sign*8.1,-294.6,23.4),C,plane='XZ'))
bevel_obj(sep,.06,2);protos.append(sep)
protos.append(box('Pair01_internal_cooling_shelf',(19.8,22,.5),(x,-280,23.4),C,'Cage stainless steel'))
# Real longitudinal rails and recessed connector backing, without transceiver modules.
for row,z in enumerate([32.8,14.0]):
 pn=row+1;port=empty(f'BUSINESS_PORT_{pn:02d}_QSFP28_EMPTY',C,'business_port');port['port_number']=pn;port['empty_socket']=True;port.parent=allports
 parts=[]
 parts.append(box(f'Port{pn:02d}_recessed_connector_stop',(19.8,2.2,11.5),(x,-265.2,z),C,'Interior shadow',.10))
 parts.append(frame(f'Port{pn:02d}_connector_contact_surround',16.8,3.6,1.4,.45,(x,-267.0,z-2.6),C,'Black polymer',radius=.35))
 for side in [-1,1]:
  for zz in [-4.25,4.25]:parts.append(box(f'Port{pn:02d}_guide_{side}_{zz}',(.3,21,.55),(x+side*9.3,-282,z+zz),C,'Cage stainless steel',.05))
  # Shallow EMI spring lips near the mouth.
  for zz in [-2.8,0,2.8]:parts.append(box(f'Port{pn:02d}_spring_{side}_{zz}',(.20,2.1,1.1),(x+side*9.86,-292,z+zz),C,'Cage stainless steel',.03))
 vs=[];fs=[]
 for pin in range(19):
  px=(pin-9)*.77;w=.25;d=.45;h=.45;k=len(vs)
  vs.extend([(px-w/2,-d/2,-h/2),(px+w/2,-d/2,-h/2),(px+w/2,d/2,-h/2),(px-w/2,d/2,-h/2),(px-w/2,-d/2,h/2),(px+w/2,-d/2,h/2),(px+w/2,d/2,h/2),(px-w/2,d/2,h/2)])
  fs.extend(tuple(k+i for i in f) for f in [(3,2,1,0),(4,5,6,7),(0,1,5,4),(2,3,7,6),(3,0,4,7),(1,2,6,5)])
 parts.append(mesh(f'Port{pn:02d}_subtle_recessed_contact_row',vs,fs,C,'Gold contacts',(x,-267.75,z-2.6)))
 for part in parts:part.parent=port;part['port_row']=row;part['detail_evidence']='Cage interior depth/contact layout conservatively inferred; exterior from NWR macro'
 for col in range(1,18):
  xn=x+22.5*col;number=2*col+row+1;rp=empty(f'BUSINESS_PORT_{number:02d}_QSFP28_EMPTY',C,'business_port');rp.parent=allports;rp['port_number']=number;rp['empty_socket']=True
  for part in parts:instance(part,part.name.replace(f'Port{pn:02d}',f'Port{number:02d}'),(part.location.x*1000+22.5*col,part.location.y*1000,part.location.z*1000),C,rp)
for col in range(18):
 er=empty(f'DOUBLE_CAGE_{col+1:02d}',C,'double_cage');er.parent=allports;er['ports']=[2*col+1,2*col+2]
 for part in protos:
  if col==0:part.parent=er
  else:instance(part,part.name.replace('Pair01',f'Pair{col+1:02d}'),(part.location.x*1000+22.5*col,part.location.y*1000,part.location.z*1000),C,er)
assert sum(o.get('component_type')=='business_port' for o in coll(C).objects)==36
stage_save('02-thirty-six-empty-metal-cages.blend')
