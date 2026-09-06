from pathlib import Path
import sys,importlib,math,json,bpy
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import model_lib as L;importlib.reload(L)
from model_lib import *
assert bpy.context.scene.name=='CISCO_N9K_C9336C_FX2_V001'
assert not bpy.data.collections.get('01_CHASSIS'), 'Stage already present: inspect before rerunning'
mat('Chassis satin nickel',(.50,.525,.55),.76,.36)
mat('Zinc plated brackets',(.57,.60,.635),.86,.30)
mat('Cage stainless steel',(.52,.54,.57),.91,.29)
mat('Fastener steel',(.40,.425,.45),.87,.27)
mat('Black polymer',(.022,.026,.031),0,.46)
mat('Fan graphite polymer',(.047,.054,.060),.05,.50)
mat('Blue airflow latch',(.008,.20,.42),0,.37)
mat('Interior shadow',(.008,.011,.014),.10,.59)
mat('Printed black',(.008,.009,.011),0,.60)
mat('Printed white',(.67,.69,.68),0,.67)
mat('Gold contacts',(.55,.33,.075),.8,.3)
mat('Dark grille metal',(.055,.061,.068),.58,.40)
mat('Indicator off',(.012,.023,.020),.15,.24)
W=P['width'];D=P['shell_depth_estimate'];H=P['height'];C='01_CHASSIS'
root=empty('N9K-C9336C-FX2', '00_ASSEMBLY','switch')
root['PID']=P['pid'];root['official_dimensions_mm']=[W,P['depth_with_handles'],H]
root['bottom_evidence']='INFERRED';root['airflow']='port-side-exhaust (blue)'
bottom=box('INFERRED_Bottom_folded_sheet',(W,D,1),(0,0,.5),C,'Chassis satin nickel',.1);bottom['inferred']=True;bottom['evidence']='No exact-model underside source found';bottom['component_type']='main_shell_bottom'
# Separate overlapping folded seams are real assembly interfaces; each piece is a closed solid.
for sign,label in [(-1,'LEFT'),(1,'RIGHT')]:
 side=box(label+'_sidewall_with_mounting_provisions',(1,D,H-1),(sign*(W/2-.5),0,(H+1)/2),C,'Chassis satin nickel',.12)
 for yy in [-284,-256,-228,228,256,284]:
  for zz in [10.8,32.8]:cut(side,cyl('tap_bore_tool',1.65,4,(sign*(W/2-.5),yy,zz),C,axis='X',n=20))
 for yy in [-187,-175,175,187]:cut(side,cyl('ground_bore_tool',1.5,4,(sign*(W/2-.5),yy,15),C,axis='X',n=20))
 side['hole_positions_estimated']=True
# Lid with true perforated front band, no photo wrap.
lid=box('Top_lid_main_sheet',(W-2,548,1),(0,21,H-.5),C,'Chassis satin nickel',.10)
for yy in [192,229]:
 for xx in [-135,0,135]:
  cut(lid,prism('stamping_tool',rounded_rect(111,1.0,.45,4),.26,(xx,yy,H-.045),C,plane='XY'))
lid['pressed_grooves_estimated']=True
box('Lid_port_edge_fold',(W-2,12,1),(0,-289,H-.5),C,'Chassis satin nickel',.10)
box('Lid_vent_transition',(W-2,1,1),(0,-252.5,H-.5),C,'Chassis satin nickel',.08)
vent=perforated('Lid_staggered_punched_vent_2028_through_holes',169,12,2.5,2.5,.77,1,(0,-268,H-.5),C,'Chassis satin nickel',stagger=.45)
for xx in [-1,1]:box('Lid_vent_side_border_'+str(xx),((W-2-422.5)/2,30,1),(xx*(422.5/2+(W-2-422.5)/4),-268,H-.5),C,'Chassis satin nickel')
# Interior baffles block implausible see-through paths but preserve visible hole depth.
box('Interior_under_port_vent_baffle',(W-12,42,1),(0,-267,H-8),C,'Interior shadow')
front=box('Port_face_solid_punched_panel',(W,1,H-6),(0,-D/2+.5,(H+6)/2),C,'Chassis satin nickel',.10)
for col in range(18):
 x=-189+22.5*col
 cut(front,prism('Cage_aperture_tool',rounded_rect(21.25,31.8,.45,4),4,(x,-295,23.4),C,plane='XZ'))
# Lower face strip: rectangular punched holes, with PID print area at far left.
perforated('Front_lower_rectangular_vent_strip',130,2,3,2.8,(1.65,1.35),1,(9,-294.5,3.2),C,'Chassis satin nickel',plane='XZ',shape='rect')
box('Front_lower_control_label_land',(33.21,1,6),( -203.105,-294.5,3),C,'Chassis satin nickel')
box('Front_lower_right_land',(15.71,1,6),(211.855,-294.5,3),C,'Chassis satin nickel')
# Rear perimeter rim leaves module/service apertures truly open.
for z in [1.25,H-1.25]:box('Rear_horizontal_rim_'+str(z),(W,1,2.5),(0,294.5,z),C,'Chassis satin nickel')
for x in [-218.46,218.46]:box('Rear_side_rim_'+str(x),(2.5,1,H-5),(x,294.5,H/2),C,'Chassis satin nickel')
for x in [160,70,-20,-110,-160]:box('Rear_module_divider_'+str(x),(1.25,2,H-4),(x,294,H/2),C,'Chassis satin nickel',.1)
# Flush countersunk top screws: cut recess, then insert real recessed Phillips head.
first=None
for x,y in [(-207,-290),(-135,-290),(-67,-290),(0,-290),(67,-290),(135,-290),(207,-290),(-204,281),(204,281),(-132,190),(0,190),(132,190),(-132,229),(0,229),(132,229),(-198,50),(198,50)]:
 target=lid if y>-253 else None
 if target:cut(target,cyl('flush_fastener_seat',1.85,.7,(x,y,H),C,axis='Z',n=24))
 if first is None:first=screw('Lid_flush_Phillips_00',(x,y,H-.32),C,radius=1.65,depth=.55)
 else:instance(first,'Lid_flush_Phillips_'+str(x)+'_'+str(y),(x,y,H-.32),C)
for o in coll(C).objects:o.parent=root
# Traditional bracket arm with twelve selectable holes; four occupied by chassis screws.
EC='02_RACK_EARS';ear_root=empty('N3K-C3064-ACC-KIT_chassis_brackets',EC,'mounting_kit');ear_root.parent=root
hole_log=[]
for sign,label in [(-1,'LEFT'),(1,'RIGHT')]:
 inside=W/2+.25;outside=inside+1.8;end=P['ear_span_estimate']/2
 outline=[(inside,-205),(outside,-205),(outside,-293.2),(end,-293.2),(end,-295),(inside,-295)]
 outline=[(sign*x,y) for x,y in outline]
 ear=prism(label+'_EAR_bent_opaque_solid_with_true_bores',outline,H,(0,0,H/2),EC,'Zinc plated brackets',plane='XY')
 bevel_obj(ear,.23,3)
 for z in [H/2-15.875,H/2,H/2+15.875]:
  x=sign*232.6;cut(ear,prism('obround_bore_tool',rounded_rect(9.8,6.5,3.25,8),6,(x,-294.1,z),EC,plane='XZ'))
  hole_log.append({'ear':ear.name,'type':'rack_obround','centre_mm':[x,-294.1,z],'direction':[0,1,0],'expected_isolated':'miss','width_mm':9.8,'height_mm':6.5})
 for y in [-284,-270,-256,-242,-228,-214]:
  for z in [10.8,32.8]:cut(ear,cyl('ear_mount_bore_tool',2.15,6,(sign*(inside+.9),y,z),EC,axis='X',n=24))
 bevel_obj(ear,.065,2);ear.parent=ear_root;ear['component_type']='rack_ear';ear['side']=label;ear['plate_thickness_mm']=1.8;ear['rack_slots']=3;ear['side_arm_selectable_holes']=12;ear['source']='NWR nwr-3 + official traditional bracket 501768; hole pitch/arm length estimated'
 # Chassis mounting four M4 countersunk screws. Real object backs can obscure side holes in assembly.
 for y in [-284,-256]:
  for z in [10.8,32.8]:
   s=screw(label+'_ear_M4_'+str(y)+'_'+str(z),(sign*(outside-.35),y,z),EC,axis='X',radius=2.5,depth=.65)
   if sign<0:s.rotation_euler.z=math.pi
   s.parent=ear_root;s['fastener_role']='ear_to_chassis'
(ROOT/'qa/ear-test-points.json').write_text(json.dumps(hole_log,indent=2))
# Aim the solid viewport; desktop inputs will independently rotate this after construction.
from mathutils import Quaternion
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  s=a.spaces.active;s.shading.type='SOLID';s.shading.color_type='MATERIAL';s.region_3d.view_location=(0,0,.022);s.region_3d.view_distance=1.0;s.region_3d.view_rotation=Quaternion((.82,.48,.13,.28)).normalized();s.region_3d.view_perspective='ORTHO'
stage_save('01-shell-and-real-hole-brackets.blend')
