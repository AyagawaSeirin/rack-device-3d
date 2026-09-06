import bpy,bmesh,json
from pathlib import Path
from mathutils import Vector
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');s=bpy.context.scene;flags=[];triangles=0
for o in s.objects:
 if o.type!='MESH':continue
 bm=bmesh.new();bm.from_mesh(o.data)
 # glTF legitimately splits positions for normals/UV. Weld a diagnostic COPY to inspect physical closure.
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 boundary=sum(e.is_boundary for e in bm.edges);nm=sum(not e.is_manifold for e in bm.edges);deg=sum(f.calc_area()<1e-14 for f in bm.faces)
 if deg or (nm and not o.get('intentional_open_surface')):flags.append({'name':o.name,'boundary':boundary,'nonmanifold':nm,'degenerate':deg,'intentional_open':o.get('intentional_open_surface','')})
 bm.free();o.data.calc_loop_triangles();triangles+=len(o.data.loop_triangles)
# Opaque wall ray probes: top, bottom, left and right must always hit outer shell.
dg=bpy.context.evaluated_depsgraph_get();probes=[]
for x in [-.18,0,.18]:
 for y in [-.32,-.12,.10,.32]:
  for z,dz,face in [(1,-1,'top'),(-1,1,'bottom')]:
   hit,co,no,idx,ob,mat=s.ray_cast(dg,Vector((x,y,z)),Vector((0,0,dz)),distance=2)
   probes.append({'face':face,'origin':[x,y,z],'hit':hit,'object':ob.name if hit else None,'normal':list(no) if hit else None})
for y in [-.30,0,.30]:
 for sign in [-1,1]:
  hit,co,no,idx,ob,mat=s.ray_cast(dg,Vector((sign,y,.042)),Vector((-sign,0,0)),distance=2)
  probes.append({'face':'side','hit':hit,'object':ob.name if hit else None,'normal':list(no) if hit else None})
r={'scene':s.name,'triangle_count':triangles,'geometric_flags_after_position_weld_copy':flags,'opaque_wall_ray_probes':probes,'missed_shell_probes':sum(not x['hit'] for x in probes),'position_weld_is_diagnostic_only':True}
(P/('qa/glb-geometry-audit.json' if 'GLB_REIMPORT' in s.name else 'qa/original-shell-probes.json')).write_text(json.dumps(r,indent=2));print('GLB geometry flags',len(flags),flags[:8]);print('Opaque shell probes',len(probes),'misses',r['missed_shell_probes'])
