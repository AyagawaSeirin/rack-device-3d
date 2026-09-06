from pathlib import Path
import bpy,bmesh,json,math,shutil
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];assert bpy.context.scene.name=='CISCO_N9K_C9336C_FX2_V001'
before=ROOT/'qa/before-handle-sweep-fix';before.mkdir(exist_ok=True)
changed=[]
for o in bpy.context.scene.objects:
 if 'silver_U_pull_handle' not in o.name:continue
 hx=(o.matrix_world@o.data.vertices[0].co).x*1000 # first ring may offset x; derive true centre from bounds instead
 hx=sum((o.matrix_world@Vector(v)).x for v in o.bound_box)/8*1000
 points=[(hx,296.2,6.2),(hx,321.18,6.2)]
 for i in range(1,17):
  a=-math.pi/2+i*math.pi/32;points.append((hx,321.18+4*math.cos(a),10.2+4*math.sin(a)))
 points.append((hx,325.18,32.8))
 for i in range(1,17):
  a=i*math.pi/32;points.append((hx,321.18+4*math.cos(a),32.8+4*math.sin(a)))
 points.append((hx,296.2,36.8));n=24;vs=[]
 # All centreline points lie in YZ: fixed +X first basis prevents former90degree flips.
 for i,p in enumerate(points):
  tangent=(Vector(points[min(i+1,len(points)-1)])-Vector(points[max(i-1,0)])).normalized();u=Vector((1,0,0));v=tangent.cross(u).normalized()
  for j in range(n):vs.append(tuple((Vector(p)+1.6*(math.cos(2*math.pi*j/n)*u+math.sin(2*math.pi*j/n)*v))/1000))
 fs=[tuple(reversed(range(n))),tuple((len(points)-1)*n+j for j in range(n))]
 for i in range(len(points)-1):
  for j in range(n):k=(j+1)%n;fs.append((i*n+j,i*n+k,(i+1)*n+k,(i+1)*n+j))
 old=o.data;me=bpy.data.meshes.new(o.name+'_parallel_section_sweep');me.from_pydata(vs,[],fs);me.update()
 for m in old.materials:me.materials.append(m)
 for p in me.polygons:p.use_smooth=len(p.vertices)==4
 bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bmesh.ops.triangulate(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
 uv=me.uv_layers.new(name='Physical80mm')
 for p in me.polygons:
  for li in p.loop_indices:
   co=me.vertices[me.loops[li].vertex_index].co;uv.data[li].uv=(co.y/.08,co.z/.08)
 o.data=me;o.location=(0,0,0);o.rotation_euler=(0,0,0);o.scale=(1,1,1);o['sweep_fix']='Fixed +X frame,16 subdivisions per90degree4mm bend,24 segments around1.6mm radius';changed.append(o.name)
for name in ['front','rear','left','right','top','bottom-INFERRED','front-left','front-right','rear-left','rear-right','high-oblique','low-oblique-INFERRED','detail-AC-power-supply']:
 p=ROOT/'previews'/f'{name}.png'
 if p.exists():shutil.copy2(p,before/p.name)
for f in ['geometry-initial.json','original-delivery-scene.json','final-renders.json']:
 p=ROOT/'qa'/f
 if p.exists():shutil.copy2(p,before/f)
bpy.ops.file.pack_all();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/CISCO-Nexus-N9K-C9336C-FX2.blend'),compress=True)
(ROOT/'qa/handle-sweep-fix.json').write_text(json.dumps({'changed':changed,'cause':'Original sweep changed reference axis as tangent turned; caused twisted quad strips at bends.','repair':'Continuous fixed transverse frame for planar centreline, circular filleted bends; no double-sided workaround','previous_views':'qa/before-handle-sweep-fix','affected_views_rerendered':False},indent=2));print('HANDLE_SWEEP_FIXED',changed)
