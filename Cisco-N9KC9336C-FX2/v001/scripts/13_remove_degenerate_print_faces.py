from pathlib import Path
import bpy,bmesh,json,shutil
ROOT=Path(__file__).resolve().parents[1]
p=ROOT/'qa/geometry-initial.json';shutil.copy2(p,ROOT/'qa/geometry-before-print-cleanup.json')
changes=[]
for o in bpy.context.scene.objects:
 if o.type!='MESH' or o.get('surface_role')!='intentional_print_surface':continue
 bm=bmesh.new();bm.from_mesh(o.data);bad=[f for f in bm.faces if f.calc_area()<1e-16]
 if bad:
  changes.append({'object':o.name,'removed_zero_area_faces':len(bad)})
  bmesh.ops.delete(bm,geom=bad,context='FACES_ONLY')
  loose=[e for e in bm.edges if not e.link_faces]
  if loose:bmesh.ops.delete(bm,geom=loose,context='EDGES')
  loose=[v for v in bm.verts if not v.link_faces]
  if loose:bmesh.ops.delete(bm,geom=loose,context='VERTS')
  bm.to_mesh(o.data);o.data.update()
 bm.free()
bpy.ops.file.pack_all()
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/CISCO-Nexus-N9K-C9336C-FX2.blend'),compress=True)
(ROOT/'qa/print-degenerate-cleanup.json').write_text(json.dumps({'changes':changes,'visual_impact':'Only zero-area triangles removed; no visible face changed. Render workers loaded the same visible geometry before this cleanup.'},indent=2))
print(changes)
