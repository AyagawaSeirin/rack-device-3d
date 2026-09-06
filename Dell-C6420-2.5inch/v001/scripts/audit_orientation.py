import bpy,json
from pathlib import Path
from mathutils import Vector
P=Path('/root/Blender/DELL-C6420/v001');s=bpy.context.scene;rows=[];texts=[]
for o in s.objects:
 if o.type!='MESH':continue
 if o.get('source_asset'):
  uv=o.data.uv_layers.active
  def corner(target):
   items=[((uv.data[l.index].uv-Vector(target)).length,o.matrix_world@o.data.vertices[l.vertex_index].co) for l in o.data.loops]
   return min(items,key=lambda q:q[0])[1]
  origin=corner((0,0));du=(corner((1,0))-origin).normalized();dv=(corner((0,1))-origin).normalized()
  top='Official_top' in o.name;u=Vector((1,0,0));v=Vector((0,1,0) if top else (0,0,1))
  rows.append({'object':o.name,'source':o['source_asset'],'u_dot_expected':du.dot(u),'v_dot_expected':dv.dot(v),'pass':du.dot(u)>.999 and dv.dot(v)>.999})
 if o.get('readable_text'):
  du=(o.matrix_world.to_3x3()@Vector((1,0,0))).normalized();rear=o.name.startswith(('Node','PSU'));expected=Vector((-1,0,0) if rear else (1,0,0))
  texts.append({'object':o.name,'text':o['readable_text'],'reading_axis_dot':du.dot(expected),'pass':du.dot(expected)>.999})
r={'scene':s.name,'image_UV':rows,'readable_text_direction':texts,'image_uv_failures':sum(not x['pass'] for x in rows),'text_axis_failures':sum(not x['pass'] for x in texts)}
(P/'qa/glb-orientation-audit.json').write_text(json.dumps(r,indent=2));print('UV checks',len(rows),'failures',r['image_uv_failures'],'text directions',len(texts),'failures',r['text_axis_failures'])
