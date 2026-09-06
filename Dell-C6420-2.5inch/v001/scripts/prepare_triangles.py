import bpy,bmesh,json
from pathlib import Path
from mathutils import Vector
P=Path('/root/Blender/DELL-C6420/v001');master=bpy.data.scenes.get('DELL_C6420_4N_24SFF_MASTER') or bpy.context.scene;bpy.context.window.scene=master
# Remove only our prior independent verification scene, already saved as evidence.
for s in list(bpy.data.scenes):
 if s.name.startswith('C6420_GLB_REIMPORT_QA'):
  for ob in list(s.objects):bpy.data.objects.remove(ob,do_unlink=True)
  bpy.data.scenes.remove(s)
cal=[]
for i in range(1,5):
 obs=[o for o in bpy.data.collections['04_NODE_'+str(i)].objects if o.type=='MESH']
 pts=[o.matrix_world@v.co for o in obs for v in o.data.vertices];lo=min(v.y for v in pts);hi=max(v.y for v in pts);delta=hi-lo-.5745
 for o in obs:
  if 'floor' in o.name or 'side_rail' in o.name:
   for v in o.data.vertices:
    w=o.matrix_world@v.co
    if w.y<lo+.001:v.co+=o.matrix_world.to_3x3().inverted()@Vector((0,delta,0))
 cal.append({'node':i,'front_edge_correction_mm':delta*1000})
changes=[]
for ob in master.objects:
 if ob.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(ob.data)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 # Eliminate collinear subdivisions before exporter triangulation.
 bmesh.ops.dissolve_limit(bm,angle_limit=1e-6,use_dissolve_boundaries=False,verts=list(bm.verts),edges=list(bm.edges),delimit={'UV','MATERIAL'})
 bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='EAR_CLIP')
 bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-7)
 bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='EAR_CLIP')
 bad=[f for f in bm.faces if f.calc_area()<1e-14]
 if bad:
  changes.append({'object':ob.name,'removed_zero_area_triangles':len(bad)})
  bmesh.ops.delete(bm,geom=bad,context='FACES')
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(ob.data);bm.free();ob.data.update()
(P/'qa/triangulation-repairs.json').write_text(json.dumps({'node_dimension_calibration':cal,'zero_triangle_cleanup':changes},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(P/'model/08-export-triangles-verified.blend'))
print('Calibrated nodes and prepared actual export triangles',cal,'removed',sum(x['removed_zero_area_triangles'] for x in changes))
