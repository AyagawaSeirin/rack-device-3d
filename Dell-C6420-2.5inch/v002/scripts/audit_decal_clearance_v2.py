import bpy,json
from pathlib import Path
from mathutils import Vector
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');sc=bpy.context.scene;dg=bpy.context.evaluated_depsgraph_get();rows=[]
for o in sc.objects:
 if o.type!='MESH' or not (o.name.startswith(('Real_','DELL_EMC_official_badge','C6400_official_badge'))):continue
 verts=[o.matrix_world@v.co for v in o.data.vertices];center=sum(verts,Vector())/len(verts);n=Vector((0,0,1) if o.name.startswith('Real_') else (0,-1,0));hit,pos,no,idx,other,mat=sc.ray_cast(dg,center-n*.000002,-n,distance=.004)
 gap=(center-pos).dot(n) if hit else None
 rows.append({'label':o.name,'underlying_object':other.name if hit else None,'gap_mm':gap*1000 if gap is not None else None,'pass':hit and other!=o and gap>.00002})
r={'scene':sc.name,'independent_opaque_label_clearances':rows,'failed':sum(not a['pass'] for a in rows),'scope':'Ray tests from printed surface inward. Positive physical gap prevents coplanar flicker; not a global proof of all possible intersections.'};(P/'qa/decal-clearance-audit.json').write_text(json.dumps(r,indent=2));print(r)
