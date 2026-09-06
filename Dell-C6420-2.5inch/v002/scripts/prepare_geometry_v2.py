import bpy,bmesh,json,math,hashlib,struct
from pathlib import Path
from mathutils import Vector,Matrix
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');sc=bpy.context.scene
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':a.spaces.active.shading.type='SOLID'
# Retain raw modifier-level audit, and correct actual observed envelope excess.
raw=P/'qa/original-scene-audit.json'
if raw.exists() and not (P/'qa/before-cleanup-audit.json').exists():(P/'qa/before-cleanup-audit.json').write_bytes(raw.read_bytes())
for ob in sc.objects:
 if ob.name.startswith('Control_ear_shell_'):
  ob.dimensions.z=.05415;ob.location.z=.059725
bpy.context.view_layer.update()
bpy.ops.object.select_all(action='DESELECT')
objects=[o for o in sc.objects if o.type in {'MESH','CURVE','FONT'} and not any(c.name=='90_STUDIO' for c in o.users_collection)]
types={o.name:o.type for o in objects}
for ob in objects:ob['editable_source_type']=ob.type;ob.select_set(True)
bpy.context.view_layer.objects.active=objects[0];bpy.ops.object.convert(target='MESH')
fixes=[]
for ob in objects:
 bm=bmesh.new();bm.from_mesh(ob.data);bm.normal_update();before=(len(bm.verts),len(bm.faces),sum(e.is_boundary for e in bm.edges),sum(f.calc_area()<1e-14 for f in bm.faces))
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
 if types[ob.name]=='FONT':
  # True printed lettering stays planar and forward-facing; this is an intentional ink boundary.
  bad=[f for f in bm.faces if f.calc_area()<1e-14]
  if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
  bm.normal_update()
  for f in bm.faces:
   if f.normal.z<0:f.normal_flip()
 elif types[ob.name]=='CURVE':
  boundary=[e for e in bm.edges if e.is_boundary]
  if boundary:bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 else:bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 bmesh.ops.dissolve_limit(bm,angle_limit=1e-6,use_dissolve_boundaries=False,verts=list(bm.verts),edges=list(bm.edges),delimit={'UV','MATERIAL'})
 bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='EAR_CLIP')
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
 bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='EAR_CLIP')
 tiny=[f for f in bm.faces if f.calc_area()<1e-14]
 if tiny:bmesh.ops.delete(bm,geom=tiny,context='FACES')
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 loose=[v for v in bm.verts if not v.link_faces]
 if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
 if not ob.get('intentional_open_surface'):
  # Only numerical boundary loops left by zero-area removal; physical through holes already have wall/back rings.
  boundary=[e for e in bm.edges if e.is_boundary]
  if boundary:bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 bm.normal_update()
 if types[ob.name]=='FONT':
  for f in bm.faces:
   if f.normal.z<0:f.normal_flip()
 bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='EAR_CLIP')
 after=(len(bm.verts),len(bm.faces),sum(e.is_boundary for e in bm.edges),sum(f.calc_area()<1e-14 for f in bm.faces))
 if before!=after:fixes.append({'object':ob.name,'before_v_f_boundary_degenerate':before,'after_v_f_boundary_degenerate':after})
 bm.to_mesh(ob.data);bm.free();ob.data.update()
 # Correct handle/fabric outermost points on real geometry, not an invisible bounding box.
 if ob.name.startswith('Chrome_lifting_handle_'):
  front=min((ob.matrix_world@v.co).y for v in ob.data.vertices);ob.location.y+=(-.4084-front)
 if ob.name.startswith('PSU') and 'woven_extraction_loop' in ob.name:
  rear=max((ob.matrix_world@v.co).y for v in ob.data.vertices);ob.location.y+=(.4157-rear)
 if ob.name in ['INFERRED_bottom_formed_sheet','Right_side_wall','Left_side_wall_estimated']:
  inv=ob.matrix_world.inverted()
  for v in ob.data.vertices:
   q=ob.matrix_world@v.co
   if -.000001<q.z<0:q.z=0;v.co=inv@q
 bpy.context.view_layer.objects.active=ob
 if any(abs(v-1)>1e-7 for v in ob.scale):
  bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
# Calibrate individual sled length against official574.5mm including release handle.
cal=[]
for i in range(1,5):
 obs=[o for o in bpy.data.collections['04_NODE_'+str(i)].objects if o.type=='MESH'];ps=[o.matrix_world@v.co for o in obs for v in o.data.vertices];lo=min(p.y for p in ps);hi=max(p.y for p in ps);delta=hi-lo-.5745
 for ob in obs:
  if 'floor' in ob.name or 'tray_side' in ob.name:
   inv=ob.matrix_world.to_3x3().inverted()
   for v in ob.data.vertices:
    if (ob.matrix_world@v.co).y<lo+.001:v.co+=inv@Vector((0,delta,0))
 cal.append({'node':i,'front_correction_mm':delta*1000})
(P/'qa/geometry-cleanup.json').write_text(json.dumps({'repairs':fixes,'node_calibration':cal,'ink_policy':'Intentional planaropaque ink boundaries retained; no alpha','numeric_policy':'0.1micron weld; explicit triangulation; closed curve caps'},indent=2))
sc['geometry_stage']='Evaluated editable meshes, welded curve caps, explicit export triangles; no negative scaling'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=str(P/'model/08-clean-triangulated.blend'))
print('GEOMETRY_PREPARED',len(objects),'repaired',len(fixes),flush=True)
