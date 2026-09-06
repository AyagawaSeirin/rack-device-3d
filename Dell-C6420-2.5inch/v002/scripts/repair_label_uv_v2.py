import bpy,json
from pathlib import Path
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');report=[]
for name in ['Real_service_label_band','Real_yellow_warning_label','Real_regulatory_label']:
 o=bpy.data.objects[name];me=o.data
 # Do not hold RNA layer references while deleting other layers: collection indices move.
 while len(me.uv_layers):me.uv_layers.remove(me.uv_layers[0])
 uv=me.uv_layers.new(name='Clear_label_export_UV');uv.active_render=True;me.uv_layers.active=uv
 vs=[o.matrix_world@v.co for v in me.vertices];lo=[min(v[j] for v in vs) for j in range(2)];span=[max(v[j] for v in vs)-lo[j] for j in range(2)]
 for l in me.loops:
  p=vs[l.vertex_index];uv.data[l.index].uv=((p.x-lo[0])/span[0],(p.y-lo[1])/span[1])
 for m in me.materials:
  for n in m.node_tree.nodes:
   if n.type=='UVMAP':n.uv_map=uv.name
 report.append({'object':name,'layer':uv.name,'extent':'world X0to1,Y0to1','fix':'Recreate layer after removing shifted RNA indices; persistent shader UV name is now valid'})
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  sh=a.spaces.active.shading;sh.type='SOLID';sh.use_scene_world=True;sh.use_scene_lights=True
(P/'qa/label-uv-repair.json').write_text(json.dumps(report,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(P/'model/12-persistent-label-uv.blend'))
print('PERSISTENT_UV_FIXED',flush=True)
