import bpy,math,json
from pathlib import Path
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');rows=[]
for name in ['Front_punched_cheek_-1','Front_punched_cheek_1']:
 o=bpy.data.objects[name];m=o.data;m.calc_normals_split();normals=[l.normal.copy() for l in m.loops];before=[];changed=0
 for f in m.polygons:
  if abs(f.normal.z)>.99999:
   for li in f.loop_indices:
    before.append(math.degrees(normals[li].angle(f.normal)));normals[li]=f.normal.copy();changed+=1
 m.normals_split_custom_set(normals);m.update();m.calc_normals_split();after=[math.degrees(m.loops[li].normal.angle(f.normal)) for f in m.polygons if abs(f.normal.z)>.99999 for li in f.loop_indices]
 o['normal_correction']='Punched flat sheet front/back normals match geometric plane; retain bevel wall normals'
 rows.append({'object':name,'corrected_flat_loops':changed,'max_before_degrees':max(before),'max_after_degrees':max(after),'geometry_and_uv_unchanged':True})
(P/'qa/cheek-normal-correction.json').write_text(json.dumps(rows,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(P/'model/13-flat-punched-sheet-normals.blend'));print(rows)
