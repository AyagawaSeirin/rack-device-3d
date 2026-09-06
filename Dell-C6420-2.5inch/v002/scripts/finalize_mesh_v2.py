import bpy,bmesh,json,math,hashlib,struct
from mathutils import Vector,Matrix
from pathlib import Path
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');sc=bpy.context.scene
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':a.spaces.active.shading.type='SOLID'
new=[o for o in sc.objects if o.type in {'FONT','CURVE'}]
types={o.name:o.type for o in new}
bpy.ops.object.select_all(action='DESELECT')
for o in new:o.select_set(True)
if new:
 bpy.context.view_layer.objects.active=new[0];bpy.ops.object.convert(target='MESH')
for o in new:
 bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
 if types[o.name]=='CURVE':
  bd=[e for e in bm.edges if e.is_boundary]
  if bd:bmesh.ops.holes_fill(bm,edges=bd,sides=0)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 else:
  bm.normal_update()
  for f in bm.faces:
   if f.normal.z<0:f.normal_flip()
 bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='EAR_CLIP');bad=[f for f in bm.faces if f.calc_area()<1e-14]
 if bad:bmesh.ops.delete(bm,geom=bad,context='FACES')
 loose=[v for v in bm.verts if not v.link_faces]
 if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
 bm.to_mesh(o.data);bm.free();o.data.update();o['editable_source_type']=types[o.name]
# Physical envelope includes woven fibres; calibrate the actual cloth assembly as one unit.
for i in [1,2]:
 obs=[o for o in sc.objects if o.name in [f'PSU{i}_woven_extraction_loop',f'PSU{i}_woven_edge_fibres']]
 top=max((o.matrix_world@v.co).y for o in obs for v in o.data.vertices);dy=.4157-top
 for o in obs:o.location.y+=dy
# Smooth only manufactured radii; area-weighted normals preserve flat panel faces.
objs=[o for o in sc.objects if o.type=='MESH' and not any(c.name=='90_STUDIO' for c in o.users_collection)]
for o in objs:
 if o.get('intentional_open_surface') or o.get('readable_text') or 'ink' in o.name.lower() or 'print' in o.name.lower() or 'label' in o.name.lower():continue
 o.data.use_auto_smooth=True;o.data.auto_smooth_angle=math.radians(42)
 for f in o.data.polygons:f.use_smooth=True
 m=o.modifiers.new('Manufacturing_face_normals','WEIGHTED_NORMAL');m.keep_sharp=True;m.weight=50
bpy.ops.object.select_all(action='DESELECT')
for o in objs:o.select_set(True)
bpy.context.view_layer.objects.active=objs[0];bpy.ops.object.convert(target='MESH')
# Reuse byte-identical local meshes/UV/materials on repeated components.
shared={};dedup=0;canonical=[]
for o in objs:
 if o.data.users>1:o.data=o.data.copy()
 m=o.data
 if not m.vertices:continue
 center=Vector(tuple((min(v.co[j] for v in m.vertices)+max(v.co[j] for v in m.vertices))/2 for j in range(3)))
 for v in m.vertices:v.co-=center
 o.matrix_world=o.matrix_world@Matrix.Translation(center);m.update()
 h=hashlib.sha256();h.update('|'.join(x.name for x in m.materials).encode())
 for v in m.vertices:h.update(struct.pack('<3i',*(round(c*1e7) for c in v.co)))
 for f in m.polygons:
  h.update(struct.pack('<ii?',len(f.vertices),f.material_index,f.use_smooth));h.update(struct.pack('<'+'I'*len(f.vertices),*f.vertices))
 for layer in m.uv_layers:
  h.update(layer.name.encode())
  for loop in layer.data:h.update(struct.pack('<2i',*(round(c*1e6) for c in loop.uv)))
 # Split normals matter for physically shaded linked repeats.
 m.calc_normals_split()
 for loop in m.loops:h.update(struct.pack('<3i',*(round(c*1e5) for c in loop.normal)))
 key=h.digest()
 if key in shared:o.data=shared[key];dedup+=1
 else:shared[key]=m
 canonical.append(o.name)
sc['repeated_mesh_policy']='Repeated identical components share mesh data; Object>Relations>MakeSingleUser for independent changes'
(P/'qa/mesh-instancing.json').write_text(json.dumps({'mesh_objects':len(objs),'unique_meshes':len(shared),'shared_instances':dedup,'new_curves_and_fonts_converted':len(new),'policy':sc['repeated_mesh_policy']},indent=2))
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=str(P/'model/10-export-ready-meshes.blend'))
print('V002_MESH_FINAL',len(objs),len(shared),dedup,flush=True)
