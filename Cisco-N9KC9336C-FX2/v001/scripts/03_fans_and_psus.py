from pathlib import Path
import sys,importlib,bpy,math,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import model_lib as L;importlib.reload(L)
from model_lib import *
assert not bpy.data.collections.get('04_FANS'), 'Stage already exists; inspect, do not duplicate'
root=bpy.data.objects['N9K-C9336C-FX2'];H=P['height']
def unite(a,b):
 bpy.context.view_layer.objects.active=a;m=a.modifiers.new('Joined molded solid','BOOLEAN');m.operation='UNION';m.solver='EXACT';m.object=b;bpy.ops.object.modifier_apply(modifier=m.name);bpy.data.objects.remove(b,do_unlink=True);return a
# Fan tray interiors are conservative; the three external tray designs follow NWR photos.
C='04_FANS'
for index,x in enumerate([115,25,-65],1):
 before=set(coll(C).objects);r=empty(f'FAN_MODULE_{index}_NXA-FAN-65CFM-PE',C,'fan_module');r.parent=root;r['fan_module_number']=index;r['rotor_count']=2;r['airflow']='port-side exhaust';r['hidden_rotor_layout']='INFERRED lateral placement; official source confirms two rotors, not manufacturing coordinates'
 for side in [-1,1]:
  xx=x+side*19.5
  frame(f'Fan{index}_rotor_housing_{side}',38,37,52,2,(xx,269,21.8),C,'Black polymer',radius=2.5)
  rt=empty(f'Fan{index}_ROTOR_{1 if side<0 else 2}_INFERRED',C,'fan_rotor');rt.parent=r;rt['inferred']=True
  hub=cyl(f'Fan{index}_hub_{side}',5.9,4,(xx,286,21.8),C,'Black polymer','Y',32);hub.parent=rt
  for b in range(7):
   a=b*2*math.pi/7;pts=[]
   for rad,theta in [(5.4,-.17),(15.8,-.05),(16.1,.31),(7.0,.50)]:
    t=a+theta*side;pts.append((rad*math.cos(t),rad*math.sin(t)))
   blade=prism(f'Fan{index}_blade_{side}_{b}',pts,1.1,(xx,285.5,21.8),C,'Black polymer');blade.parent=rt
  box(f'Fan{index}_top_retention_rail_{side}',(3.5,44,.6),(xx,267,40.5),C,'Cage stainless steel',.08)
  box(f'Fan{index}_rear_power_contact_block_{side}',(11,4,8),(xx,241,22),C,'Black polymer',.2)
 body=frame(f'Fan{index}_front_frame',88,39.4,2.5,4.0,(x,294.3,21.8),C,'Fan graphite polymer',radius=2)
 grille=perforated(f'Fan{index}_true_honeycomb_front_grille',19,7,4.1,3.9,1.32,.65,(x,295.75,23),C,'Dark grille metal',plane='XZ',shape='hex',stagger=.57)
 grille['source']='NWR rear photo; pitch estimated'
 # Open U-shaped pull handle, with a solid lower grip and side returns.
 outline=[(-36,32),(-22,8),(22,8),(36,32),(30,32),(17,15),(-17,15),(-30,32)]
 hand=prism(f'Fan{index}_molded_trapezoid_pull_handle',outline,15,(x,304.5,0),C,'Fan graphite polymer')
 grip=box('temporary_grip_union',(39,7,9),(x,313.5,12.5),C,'Fan graphite polymer');unite(hand,grip);bevel_obj(hand,.55,3)
 for sign in [-1,1]:
  tab=box(f'Fan{index}_BLUE_release_latch_{sign}',(7.7,14,25),(x+sign*39.5,303.5,20),C,'Blue airflow latch',.7)
  box(f'Fan{index}_latch_thumb_flare_{sign}',(10,3.8,19),(x+sign*39.3,311.3,20),C,'Blue airflow latch',.5)
  for zz in [14,17,20,23,26]:box(f'Fan{index}_latch_grip_rib_{sign}_{zz}',(5.8,.65,.42),(x+sign*39.3,313.35,zz),C,'Blue airflow latch',.1)
 # Recessed factory PID label bar. Plain known text, no generated microprint or serial.
 box(f'Fan{index}_PID_label_recess',(54,.25,3.9),(x,295.69,38.1),C,'Black polymer',.2)
 text_obj(f'Fan{index}_known_PID','NXA-FAN-65CFM-PE',1.22,(x,295.845,37.66),C,'Printed white','REAR','CENTER')
 for sx in [-39,39]:
  bolt=cyl(f'Fan{index}_flush_lock_pin_{sx}',1.35,.3,(x+sx,295.65,37.8),C,'Fastener steel','Y',24)
 # Parent all new objects except rotor children, maintaining physical hierarchy.
 for o in set(coll(C).objects)-before:
  if o!=r and o.parent is None:o.parent=r
# Two identical AC PSUs, each with genuine hollow body and structured empty IEC C14 inlet.
C='05_POWER_SUPPLIES'
for index,x in enumerate([188.5,-188.5],1):
 before=set(coll(C).objects);r=empty(f'PSU_{index}_NXA-PAC-1100W-PE2',C,'psu_module');r.parent=root;r['power_watts']=1100;r['power_type']='AC';r['airflow']='port-side exhaust';r['revision']='manufacturer subrevision unasserted'
 shell=frame(f'PSU{index}_formed_silver_shell',56.2,38.4,301,.8,(x,144.5,21.8),C,'Zinc plated brackets',radius=.55)
 box(f'PSU{index}_rear_internal_endcap',(54.5,1,36.5),(x,-6.5,21.8),C,'Zinc plated brackets',.1)
 box(f'PSU{index}_internal_mating_block',(39,5,13),(x,-9.2,13),C,'Black polymer',.3)
 box(f'PSU{index}_internal_opaque_baffle',(54,1,35),(x,277.5,21.8),C,'Interior shadow')
 # Front frame surrounds the AC inlet and cooling perforations.
 frame(f'PSU{index}_front_face_rim',56.4,39.2,1.7,2.1,(x,295.15,21.8),C,'Zinc plated brackets',radius=.7)
 box(f'PSU{index}_inlet_vent_divider',(1.7,1.7,35),(x-7.6,295.15,21.8),C,'Zinc plated brackets')
 perforated(f'PSU{index}_true_hex_cooling_vents',5,8,3.6,3.8,1.1,.75,(x-17.8,295.5,21.2),C,'Zinc plated brackets',plane='XZ',shape='hex',stagger=.48)
 sx=x+10.2;sz=20.8
 outer=[(-15,-12),(15,-12),(15,5),(9,12),(-9,12),(-15,5)]
 inner=[(-11.5,-8.8),(11.5,-8.8),(11.5,3.5),(7,8.8),(-7,8.8),(-11.5,3.5)]
 inlet=prism(f'PSU{index}_IEC_C14_black_inlet_housing',outer,8,(sx,292.9,sz),C,'Black polymer')
 cut(inlet,prism('inlet_through_cavity_tool',inner,20,(sx,293,sz),C));bevel_obj(inlet,.3,3)
 box(f'PSU{index}_IEC_recessed_black_floor',(23,1,18),(sx,286.4,sz),C,'Black polymer')
 for pin,(dx,dz) in enumerate([(-5,-3.3),(5,-3.3),(0,4.5)]):box(f'PSU{index}_IEC_pin_{pin}',(1.9,7.5 if pin<2 else 8.6,.85),(sx+dx,290.1,sz+dz),C,'Fastener steel',.12)
 # U-handle reaches the calibrated rear extreme, accounting for front LS-button protrusion.
 hx=x-17.8
 points=[(hx,296.2,6.2),(hx,321.7,6.2),(hx,324.8,7.0),(hx,325.18,10),(hx,325.18,33.6),(hx,323.5,36.8),(hx,296.2,36.8)]
 tube(f'PSU{index}_silver_U_pull_handle',points,1.6,C,'Fastener steel',14)
 box(f'PSU{index}_BLUE_release_latch',(4.6,12.5,10.5),(x-24,301.2,8.4),C,'Blue airflow latch',.6)
 # Stowed adjustable nylon cable retainer, no external power cable installed.
 box(f'PSU{index}_cord_retainer_anchor',(11,5,3.5),(sx,298.3,37.1),C,'Black polymer',.3)
 belt=frame(f'PSU{index}_stowed_nylon_retention_loop',20,12,3.1,1.0,(sx,307.8,32.4),C,'Black polymer',plane='YZ',radius=3)
 for yy in [300,302.2,304.4,306.6,308.8,311,313.2,315.4]:box(f'PSU{index}_retainer_rib_{yy}',(3.45,.4,.65),(sx,yy,38.3),C,'Black polymer',.07)
 for zz in [36.8,32.6]:cyl(f'PSU{index}_unpowered_LED_{zz}',.9,.3,(x-23,296.2,zz),C,'Indicator off','Y',20)
 text_obj(f'PSU{index}_FAIL_legend','FAIL',1.0,(x-25,296.27,37),C,'Printed black','REAR')
 text_obj(f'PSU{index}_OK_legend','OK',1.0,(x-25,296.27,32.8),C,'Printed black','REAR')
 for dx in [-24.5,24.5]:
  for zz in [4.1,39.3]:
   sc=screw(f'PSU{index}_face_screw_{dx}_{zz}',(x+dx,296.05,zz),C,axis='Y',radius=1.05,depth=.3);sc.rotation_euler.z=math.pi
 for o in set(coll(C).objects)-before:
  if o!=r and o.parent is None:o.parent=r
assert sum(o.get('component_type')=='fan_module' for o in bpy.context.scene.objects)==3
assert sum(o.get('component_type')=='fan_rotor' for o in bpy.context.scene.objects)==6
assert sum(o.get('component_type')=='psu_module' for o in bpy.context.scene.objects)==2
stage_save('03-three-fans-two-matched-AC-PSUs.blend')
