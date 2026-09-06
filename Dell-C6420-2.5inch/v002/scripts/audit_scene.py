import bpy,bmesh,json,math
from mathutils import Vector
from pathlib import Path
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');scene=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get()
objects=[o for o in scene.objects if o.type in {'MESH','CURVE','FONT'} and not any(c.name=='90_STUDIO' for c in o.users_collection)]
bad=[];stats=[];allpoints=[];duplicate_faces={};exact_duplicates=[]
for o in objects:
 e=o.evaluated_get(dg);m=e.to_mesh();bm=bmesh.new();bm.from_mesh(m)
 bounds=[o.matrix_world@v.co for v in m.vertices];allpoints.extend(bounds)
 boundary=sum(x.is_boundary for x in bm.edges);nonman=sum(not x.is_manifold for x in bm.edges);deg=sum(f.calc_area()<1e-14 for f in bm.faces)
 signed=bm.calc_volume(signed=True) if not boundary else None
 flag={'name':o.name,'boundary_edges':boundary,'nonmanifold_edges':nonman,'degenerate_faces':deg,'signed_volume_m3':signed,'negative_transform':o.matrix_world.determinant()<0,'intentional_open':o.get('intentional_open_surface','')}
 if deg or flag['negative_transform'] or (signed is not None and signed < -1e-14) or (nonman and not flag['intentional_open']):bad.append(flag)
 # Exact duplicated polygon vertex sets per-object; ignore point-touch and assembly contact.
 seen=set()
 for poly in m.polygons:
  key=tuple(sorted(tuple(round(c,8) for c in m.vertices[v].co) for v in poly.vertices))
  if key in seen:exact_duplicates.append(o.name)
  seen.add(key)
 m.calc_loop_triangles();stats.append({'name':o.name,'vertices':len(m.vertices),'polygons':len(m.polygons),'triangles':len(m.loop_triangles)})
 bm.free();e.to_mesh_clear()
mn=[min(p[i] for p in allpoints) for i in range(3)];mx=[max(p[i] for p in allpoints) for i in range(3)]
materials=[]
for m in bpy.data.materials:
 if not m.users:continue
 bs=m.node_tree.nodes.get('Principled BSDF') if m.use_nodes else None
 if bs:materials.append({'name':m.name,'alpha':bs.inputs['Alpha'].default_value,'alpha_linked':bs.inputs['Alpha'].is_linked,'transmission':bs.inputs['Transmission Weight'].default_value,'blend_method':m.blend_method,'backface_culling':m.use_backface_culling})
report={'scene':scene.name,'object_count':len(objects),'triangle_count':sum(s['triangles'] for s in stats),'polygon_count':sum(s['polygons'] for s in stats),'vertices':sum(s['vertices'] for s in stats),'bbox_min_m':mn,'bbox_max_m':mx,'bbox_mm':[(b-a)*1000 for a,b in zip(mn,mx)],'geometry_flags':bad,'exact_duplicate_faces_within_object':exact_duplicates,'materials':materials,'components':{k:sum(o.get('component_type')==k for o in scene.objects) for k in ['2.5-inch hot-swap carrier','C6420 node','2400W PSU']},'objects':stats}
(P/'qa/original-scene-audit.json').write_text(json.dumps(report,indent=2))
print(json.dumps({k:report[k] for k in ['object_count','triangle_count','bbox_mm','components']},indent=2));print('FLAGS',len(bad),[(x['name'],x['boundary_edges'],x['degenerate_faces']) for x in bad[:35]]);print('Duplicate faces',len(exact_duplicates))
