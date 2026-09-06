from pathlib import Path
import sys,importlib,bpy,math,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import model_lib as L;importlib.reload(L)
from model_lib import *
assert not bpy.data.collections.get('06_MANAGEMENT'), 'Already present; inspect before rerun'
root=bpy.data.objects['N9K-C9336C-FX2'];C='06_MANAGEMENT';r=empty('REAR_SERVICE_INTERFACES',C,'service_panel');r.parent=root
panel=box('Rear_service_panel_true_apertures',(49,1.4,40),(-135,295,21.8),C,'Chassis satin nickel',.2)
for name,z,orientation in [('CONSOLE',31.8,1),('MANAGEMENT',17.4,-1)]:
 x=-122.8;cut(panel,box('RJ45_panel_tool',(15.8,6,13.9),(x,295,z),C))
 rp=empty('REAR_'+name+'_RJ45',C,'console_rj45' if name=='CONSOLE' else 'management_rj45');rp.parent=r
 rp['connector']='8P8C RJ45';rp['interface']='RS232 console' if name=='CONSOLE' else 'out-of-band Ethernet'
 parts=[];parts.append(frame(name+'_RJ45_metal_shield',15.4,13.5,8,.35,(x,292.7,z),C,'Cage stainless steel',radius=.3))
 housing=box(name+'_RJ45_keyed_plastic_body',(14.6,8,12.7),(x,291.8,z),C,'Black polymer')
 outline=[(-5.8,-4.1),(5.8,-4.1),(5.8,3.0),(3.0,3.0),(3.0,5.2),(-3.0,5.2),(-3.0,3.0),(-5.8,3.0)]
 outline=[(u,v*orientation) for u,v in outline]
 cut(housing,prism('RJ45_key_cavity_tool',outline,15,(x,293.0,z),C));parts.append(housing)
 parts.append(box(name+'_RJ45_deep_connector_stop',(12,1,10.5),(x,286.6,z),C,'Interior shadow'))
 for n in range(8):parts.append(box(name+'_RJ45_contact_'+str(n),(.35,5,.22),(x+(n-3.5)*1.0,291.4,z-orientation*3.2),C,'Gold contacts',.035))
 for sx in [-5.6,5.6]:parts.append(box(name+'_RJ45_unpowered_corner_LED_'+str(sx),(2.0,.45,1.3),(x+sx,296.45,z+orientation*5.3),C,'Indicator off',.1))
 for o in parts:o.parent=rp
# Separate management SFP, excluded from the 36 business-port count.
x=-141;z=15.6;cut(panel,box('SFP_panel_tool',(15.1,6,10.5),(x,295,z),C))
rp=empty('REAR_MANAGEMENT_SFP_EMPTY',C,'management_sfp');rp.parent=r
parts=[frame('Mgmt_SFP_deep_metal_cage',14.7,10.1,18,.32,(x,288,z),C,'Cage stainless steel',radius=.35),box('Mgmt_SFP_recessed_connector_stop',(13.8,1.2,9.2),(x,279.1,z),C,'Interior shadow')]
for sx in [-5.8,5.8]:parts.append(box('Mgmt_SFP_guide_'+str(sx),(.22,12,.4),(x+sx,289,z-2.9),C,'Cage stainless steel',.03))
for n in range(10):parts.append(box('Mgmt_SFP_contact_'+str(n),(.28,.5,.3),(x+(n-4.5)*.8,279.85,z-2.0),C,'Gold contacts'))
for o in parts:o.parent=rp
# Vertical USB-A with visible keyed tongue and four contacts.
x=-153.5;z=19.25;cut(panel,box('USB_panel_tool',(5.6,6,13.7),(x,295,z),C))
rp=empty('REAR_USB_TYPE_A',C,'usb_a');rp.parent=r
parts=[frame('USB_A_metal_shell',5.25,13.3,8,.32,(x,293,z),C,'Cage stainless steel',radius=.45),box('USB_A_deep_stop',(4.5,1,12.5),(x,289,z),C,'Interior shadow'),box('USB_A_black_tongue',(1.15,5.7,10.3),(x+.65,292.7,z),C,'Black polymer',.15)]
for n in range(4):parts.append(box('USB_A_contact_'+str(n),(.1,3.0,.65),(x-.04,294,z+(n-1.5)*2.15),C,'Gold contacts',.02))
for o in parts:o.parent=rp
for x,name in [(-126,'BCN'),(-139,'STS')]:
 cut(panel,box('status_window_tool',(2.0,4,1.65),(x,295,5.8),C))
 o=box('REAR_'+name+'_unpowered_indicator',(1.9,.7,1.5),(x,295.7,5.8),C,'Indicator off',.15);o['component_type']='rear_status_indicator'
 text_obj('REAR_'+name+'_legend',name,1.25,(x,295.725,2.25),C,'Printed black','REAR','CENTER')
bolt=screw('Rear_service_retention_screw',(-132.5,295.72,5.8),C,axis='Y',radius=1.45,depth=.35);bolt.rotation_euler.z=math.pi
# Source-matched symbolic legends rather than fabricated port names.
def line(name,a,b,width=.14):
 dx=b[0]-a[0];dz=b[2]-a[2];length=math.hypot(dx,dz);ux=-dz/length*width/2;uz=dx/length*width/2
 pts=[(a[0]+ux,a[2]+uz),(a[0]-ux,a[2]-uz),(b[0]-ux,b[2]-uz),(b[0]+ux,b[2]+uz)]
 o=prism(name,pts,.015,(0,a[1],0),C,'Printed black');o['surface_role']='intentional_print_solid';return o
def network_icon(x,z,name):
 for dx,dz in [(0,1.0),(-1.25,-1.0),(1.25,-1.0)]:
  o=frame(name+'_node_'+str(dx),1.05,.8,.018,.12,(x+dx,295.726,z+dz),C,'Printed black',radius=.12);o['surface_role']='intentional_print_surface'
 for a,b in [((x,z+.6),(x,z-.5)),((x-1.25,z-.5),(x+1.25,z-.5)),((x-1.25,z-.5),(x-1.25,z-.6)),((x+1.25,z-.5),(x+1.25,z-.6))]:line(name+'_line',(a[0],295.73,a[1]),(b[0],295.73,b[1]))
network_icon(-122.8,8.4,'RJ45_management_symbol');network_icon(-141,23.5,'SFP_management_symbol')
o=frame('Console_terminal_symbol',3.1,2.0,.018,.16,(-122.8,295.726,40.4),C,'Printed black',radius=.1);o['surface_role']='intentional_print_surface'
line('USB_symbol_stem',(-153.5,295.73,28),(-153.5,295.73,31.3),.18)
line('USB_symbol_branch_A',(-153.5,295.73,29.6),(-155.0,295.73,30.5),.18)
line('USB_symbol_branch_B',(-153.5,295.73,29.0),(-152.0,295.73,30.0),.18)
text_obj('Rear_P2_arrow_legend','P2',1.0,(-154.1,295.726,37),C,'Printed black','REAR')
for o in coll(C).objects:
 if o!=r and o.parent is None:o.parent=r
# Front known factory markings and mechanical controls.
C='07_FACTORY_MARKINGS';r=empty('FRONT_BRAND_AND_PORT_LEGENDS',C,'factory_markings');r.parent=root
front=bpy.data.objects['Port_face_solid_punched_panel']
for kind,x,z,label in [('chassis',-211.1,23.7,'BCN'),('chassis',-211.1,18.6,'STS'),('chassis',-211.1,13.5,'ENV'),('lane',-203.65,35.4,'1'),('lane',-203.65,29.9,'2'),('lane',-203.65,24.4,'3'),('lane',-203.65,18.9,'4')]:
 cut(front,cyl('front_indicator_aperture_tool',.95,3,(x,-294.5,z),C,axis='Y',n=24))
 o=cyl('FRONT_'+label+'_unpowered_lens',.87,.55,(x,-294.875,z),C,'Indicator off','Y',32);o['component_type']='front_indicator';o['indicator_group']=kind
 text_obj('FRONT_'+label+'_legend',label,1.65,((x+1.45 if kind=='lane' else -219.0),-295.026,z-.55),C,'Printed black','FRONT')
cut(front,cyl('LS_selector_aperture_tool',2.15,3,(-203.65,-294.5,11.25),C,axis='Y',n=40))
outer=cyl('LS_selector_black_surround',2.1,.45,(-203.65,-294.99,11.25),C,'Black polymer','Y',48)
button=cyl('LS_selector_metal_button',1.68,.64,(-203.65,-295.2,11.25),C,'Fastener steel','Y',48)
cut(button,cyl('LS_button_inset_tool',1.13,.11,(-203.65,-295.54,11.25),C,axis='Y',n=40))
text_obj('LS_selector_text','LS',1.7,(-203.65,-295.026,7.5),C,'Printed black','FRONT','CENTER')
# Bridge bars reconstructed from the sharp nwr-3 original: nine bars, two taller peaks.
for i,height in enumerate([.62,1.20,2.35,1.28,.70,1.28,2.35,1.20,.62]):
 o=prism('Cisco_bridge_bar_'+str(i+1),rounded_rect(.27,height,.13,5),.018,(-218.4+i*1.12,-295.036,40.5),C,'Printed black');o['surface_role']='intentional_print_solid';o['source']='NWR nwr-3 real brand macro'
text_obj('Cisco_brand_wordmark','CISCO',3.0,(-218.7,-295.026,35.9),C)
text_obj('Cisco_product_family_line_1','Cisco',2.2,(-218.7,-295.026,7.2),C)
text_obj('Cisco_product_family_line_2','Nexus',2.2,(-218.7,-295.026,4.8),C)
text_obj('Correct_factory_PID','N9K-C9336C-FX2',1.55,(-218.7,-295.026,1.5),C)
for col in range(18):
 x=-189+col*22.5
 for num,dx in [(2*col+1,-7.8),(2*col+2,6.8)]:text_obj(f'PORT_NUMBER_{num:02d}',str(num),1.7,(x+dx,-295.026,40.3),C,'Printed black','FRONT','CENTER')
 for sign in [-1,1]:
  pts=[(-.6,-.8),(.6,-.8),(0,.8)] if sign<0 else [(-.6,.8),(.6,.8),(0,-.8)]
  o=prism(f'Port_pair_{col+1}_direction_{sign}',pts,.015,(x+sign*3.6,-295.038,41.0),C,'Printed black');o['surface_role']='intentional_print_solid'
for o in coll(C).objects:
 if o!=r and o.parent is None:o.parent=r
stage_save('04-keyed-management-and-correct-brand.blend')
