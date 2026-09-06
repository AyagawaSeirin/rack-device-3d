from pathlib import Path
import sys,importlib,bpy,math,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));import model_lib as L;importlib.reload(L)
from model_lib import *
C='01_CHASSIS';root=bpy.data.objects['N9K-C9336C-FX2'];H=P['height'];W=P['width']
# Eliminate externally coplanar lid/side/bottom front faces behind the separate skin.
for name in ['LEFT_sidewall_with_mounting_provisions','RIGHT_sidewall_with_mounting_provisions','INFERRED_Bottom_folded_sheet']:
 o=bpy.data.objects[name]
 for v in o.data.vertices:
  if v.co.y<-.290:v.co.y+=.001
 o.data.update()
o=bpy.data.objects['Lid_port_edge_fold']
for v in o.data.vertices:
 if v.co.y<-.005:v.co.y+=.001
o.data.update()
for name in ['Port_face_solid_punched_panel','Front_lower_rectangular_vent_strip','Front_lower_control_label_land','Front_lower_right_land']:
 bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)
front=box('Port_face_solid_punched_panel',(W,1,H),(0,-294.5,H/2),C,'Chassis satin nickel');front.parent=root
for col in range(18):cut(front,prism('cage_cut_tool',rounded_rect(20.98,31.38,.44,4),4,(-189+22.5*col,-294.5,23.4),C))
vs=[];fs=[]
for col in range(130):
 for row in range(2):
  x=9+(col-64.5)*3;z=3.2+(row-.5)*2.8;outline=rounded_rect(1.65,1.35,.15,3);n=len(outline);k=len(vs)
  vs.extend((x+u,t,z+v) for t in [-2,2] for u,v in outline)
  fs.extend([tuple(k+i for i in reversed(range(n))),tuple(k+i for i in range(n,2*n))]);fs.extend((k+i,k+(i+1)%n,k+(i+1)%n+n,k+i+n) for i in range(n))
cut(front,mesh('260_front_vent_cutters',vs,fs,C,loc=(0,-294.5,0)))
for x,z in [(-211.1,23.7),(-211.1,18.6),(-211.1,13.5),(-203.65,35.4),(-203.65,29.9),(-203.65,24.4),(-203.65,18.9)]:cut(front,cyl('indicator_cut_tool',.95,4,(x,-294.5,z),C,axis='Y',n=32))
cut(front,cyl('LS_cut_tool',2.15,4,(-203.65,-294.5,11.25),C,axis='Y',n=48));bevel_obj(front,.055,2)
# Font sizes from the real macro, kept as true readable geometry.
for name,size in [('Cisco_brand_wordmark',3.9),('Cisco_product_family_line_1',3.2),('Cisco_product_family_line_2',3.2),('Correct_factory_PID',3.5)]:bpy.data.objects[name].data.size=size/1000
# Small opaque domed lenses, with a coated highlight; no emission/transmission.
material=bpy.data.materials['Indicator off'];bs=material.node_tree.nodes['Principled BSDF'];bs.inputs['Roughness'].default_value=.16;bs.inputs['Coat Weight'].default_value=.5;bs.inputs['Coat Roughness'].default_value=.12
for o in [o for o in bpy.context.scene.objects if o.get('component_type')=='front_indicator']:
 vs=[];fs=[];ns=32;nr=12
 # Parametric ellipsoid, closed at poles without degenerate duplicated pole rings.
 vs.append((0,-.30,0))
 for j in range(1,nr):
  a=math.pi*j/nr
  for i in range(ns):
   b=2*math.pi*i/ns;vs.append((.87*math.sin(a)*math.cos(b),-.30*math.cos(a),.87*math.sin(a)*math.sin(b)))
 vs.append((0,.30,0));end=len(vs)-1
 for i in range(ns):fs.append((0,1+(i+1)%ns,1+i));fs.append((end,end-1-i,end-1-(i+1)%ns))
 for j in range(nr-2):
  for i in range(ns):a=1+j*ns+i;b=1+j*ns+(i+1)%ns;fs.append((a,b,b+ns,a+ns))
 temp=mesh('lens_mesh_temp',vs,fs,'07_FACTORY_MARKINGS','Indicator off');o.data=temp.data;bpy.data.objects.remove(temp,do_unlink=True);o.location.y=-.29493
 for f in o.data.polygons:f.use_smooth=True
bevel_obj(bpy.data.objects['LS_selector_metal_button'],.065,3)
# Finer vertical thumb ridges and a slight canted flare replace heavy horizontal steps.
for o in list(bpy.context.scene.objects):
 if '_latch_grip_rib_' in o.name:bpy.data.objects.remove(o,do_unlink=True)
for index,x in enumerate([115,25,-65],1):
 pr=bpy.data.objects[f'FAN_MODULE_{index}_NXA-FAN-65CFM-PE']
 for sign in [-1,1]:
  flare=bpy.data.objects[f'Fan{index}_latch_thumb_flare_{sign}'];flare.rotation_euler.z=math.radians(sign*10)
  for i in range(10):
   rib=box(f'Fan{index}_fine_vertical_thumb_rib_{sign}_{i}',(.13,.30,13),(x+sign*39.3+(i-4.5)*.48,313.32,20),'04_FANS','Blue airflow latch',.04);rib.parent=pr
# Add the explicit physical UV map to new metallic geometry.
uv=front.data.uv_layers.new(name='Physical80mm')
for po in front.data.polygons:
 ax=max(range(3),key=lambda i:abs(po.normal[i]));ij=[1,2] if ax==0 else [0,2] if ax==1 else [0,1]
 for li in po.loop_indices:
  co=front.data.vertices[front.data.loops[li].vertex_index].co;uv.data[li].uv=(co[ij[0]]/.08,co[ij[1]]/.08)
(ROOT/'qa/front-refinement.json').write_text(json.dumps({'repaired':['coplanar external front seams','undersized family/PID printing','flat indicator lenses','oversized horizontal latch ribs'],'front_panel':'one continuous solid with18 cage bores260 vents and8 control bores','no_alpha_workaround':True},indent=2))
stage_save('09-continuous-front-and-photographic-controls.blend')
