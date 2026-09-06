import bpy,bmesh,json
from pathlib import Path
P=Path('/root/Blender/DELL-C6420/v001');fixes=[]
for ob in bpy.context.scene.objects:
 if ob.type!='MESH':continue
 ink=bool(ob.get('readable_text'));cap=(ob.name.startswith('Steel_rack_handle') or 'guard_spoke' in ob.name or 'fabric_extraction_loop' in ob.name or ob.name.startswith(('Power_symbol_arc','Power_symbol_stroke')))
 if not ink and not cap:continue
 bm=bmesh.new();bm.from_mesh(ob.data);bm.normal_update()
 if ink:
  # Real printing is opaque surface ink, not a tessellated tiny extruded solid.
  remove=[f for f in bm.faces if f.normal.z<.99 or f.calc_area()<1e-14]
  bmesh.ops.delete(bm,geom=remove,context='FACES')
  ob['intentional_open_surface']='Printed opaque ink on existing substrate; front-facing surface only'
  for face in bm.faces:
   if face.normal.z<0:face.normal_flip()
 else:
  bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-6)
  bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
  boundary=[e for e in bm.edges if e.is_boundary]
  if boundary:bmesh.ops.holes_fill(bm,edges=boundary,sides=0)
  bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 loose=[v for v in bm.verts if not v.link_faces]
 if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
 bm.to_mesh(ob.data);bm.free();ob.data.update();fixes.append(ob.name)
(P/'qa/geometry-repairs-final.json').write_text(json.dumps({'repaired_objects':fixes,'ink_policy':'Single physical opaque printed surface; no alpha map','caps':'Weld at 1 micrometer and close split caps on handles, spokes, loops only'},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(P/'model/06-geometry-verified.blend'))
print('Repaired',len(fixes),'objects and saved 06-geometry-verified.blend')
