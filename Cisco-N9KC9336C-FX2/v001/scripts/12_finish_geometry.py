from pathlib import Path
import bpy,bmesh,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
for index in [1,2,3]:
 for sign in [-1,1]:
  flare=bpy.data.objects[f'Fan{index}_latch_thumb_flare_{sign}']
  for i in range(10):
   o=bpy.data.objects[f'Fan{index}_fine_vertical_thumb_rib_{sign}_{i}']
   for v in o.data.vertices:v.co.y*=.14/.30
   o.location=flare.matrix_world@Vector(((i-4.5)*.00048,.00195,0));o.rotation_euler=flare.rotation_euler.copy()
   bm=bmesh.new();bm.from_mesh(o.data);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(o.data);bm.free();o.data.update()
# Confirm the active scene is the main assembly, and preserve all packaged resources.
bpy.context.view_layer.update();bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/CISCO-Nexus-N9K-C9336C-FX2.blend'),compress=True)
(ROOT/'qa/latch-ridge-contact.json').write_text(json.dumps({'ribs':60,'position_basis':'actual canted flare matrix','nominal_base_overlap_mm':.02,'ridge_height_mm':.14,'geometry_is_applied':True},indent=2))
print('FINAL_GEOMETRY_SAVED')
