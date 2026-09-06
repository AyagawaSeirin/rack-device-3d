from pathlib import Path
import bpy,bmesh,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1]
report={'scene':bpy.context.scene.name,'filepath':bpy.data.filepath,'components':{},'meshes':[],'failures':[],'triangles':0}
objs=[o for o in bpy.context.scene.objects if not any(c.name.startswith('90_') for c in o.users_collection)]
for kind in ['business_port','double_cage','fan_module','fan_rotor','psu_module','rack_ear','management_rj45','console_rj45','management_sfp','usb_a']:
 report['components'][kind]=sum(o.get('component_type')==kind for o in objs)
seen={}
for o in objs:
 if o.type!='MESH':continue
 if any(s<0 for s in o.scale):report['failures'].append({'object':o.name,'failure':'negative_scale'})
 me=o.data;me.calc_loop_triangles();report['triangles']+=len(me.loop_triangles)
 if me.name in seen:continue
 bm=bmesh.new();bm.from_mesh(me)
 boundary=sum(e.is_boundary for e in bm.edges);nonmanifold=sum(not e.is_manifold for e in bm.edges);zero=sum(f.calc_area()<1e-16 for f in bm.faces)
 volume=bm.calc_volume(signed=True);open_allowed=o.get('surface_role')=='intentional_print_surface'
 d={'mesh':me.name,'example_object':o.name,'users':me.users,'vertices':len(me.vertices),'faces':len(me.polygons),'triangles':len(me.loop_triangles),'boundary_edges':boundary,'nonmanifold_edges':nonmanifold,'zero_area_faces':zero,'signed_volume_m3':volume,'open_allowed':open_allowed}
 if (nonmanifold and not open_allowed) or zero or (volume<=0 and not open_allowed):report['failures'].append(d)
 seen[me.name]=d;report['meshes'].append(d);bm.free()
from mathutils import Vector
points=[o.matrix_world@Vector(v) for o in objs if o.type=='MESH' for v in o.bound_box]
report['bounds_mm']={'min':[min(p[i] for p in points)*1000 for i in range(3)],'max':[max(p[i] for p in points)*1000 for i in range(3)]}
report['dimensions_mm']=[report['bounds_mm']['max'][i]-report['bounds_mm']['min'][i] for i in range(3)]
report['unique_meshes']=len(seen);report['mesh_instances']=sum(o.type=='MESH' for o in objs);report['pass']=not report['failures']
(ROOT/'qa/geometry-initial.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:report[k] for k in ['components','dimensions_mm','triangles','unique_meshes','mesh_instances','pass']}));print('FAILURES',len(report['failures']));print(json.dumps(report['failures'][:12],indent=2))
