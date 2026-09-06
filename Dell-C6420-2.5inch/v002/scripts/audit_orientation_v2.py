import bpy,json,numpy as np
from pathlib import Path
from mathutils import Vector
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');sc=bpy.context.scene;rows=[];texts=[];uvrefs=[]
for o in sc.objects:
 if o.type!='MESH':continue
 if o.get('image_uv_verified') and 'woven_extraction_loop' not in o.name:
  top=o.name.startswith('Real_');expected_u=Vector((1,0,0));expected_v=Vector((0,1,0) if top else (0,0,1))
  uv=o.data.uv_layers.active
  points=[];coords=[]
  for l in o.data.loops:
   points.append(list(o.matrix_world@o.data.vertices[l.vertex_index].co));coords.append([*uv.data[l.index].uv,1])
  coeff=np.linalg.lstsq(np.array(coords),np.array(points),rcond=None)[0];du=Vector(coeff[0]).normalized();dv=Vector(coeff[1]).normalized();normal=du.cross(dv).normalized()
  rows.append({'object':o.name,'u_dot_expected':du.dot(expected_u),'v_dot_expected':dv.dot(expected_v),'front_handedness_dot':normal.dot(expected_u.cross(expected_v)),'pass':du.dot(expected_u)>.999 and dv.dot(expected_v)>.999})
 if o.get('readable_text'):
  du=(o.matrix_world.to_3x3()@Vector((1,0,0))).normalized();expected=Vector((0,0,1) if '_iDRAC_mark' in o.name else (-1,0,0) if o.name.startswith(('Node','PSU')) else (1,0,0));texts.append({'object':o.name,'text':o['readable_text'],'axis_dot':du.dot(expected),'pass':du.dot(expected)>.999})
 for m in o.data.materials:
  if m and m.use_nodes:
   for n in m.node_tree.nodes:
    if n.type=='UVMAP':uvrefs.append({'object':o.name,'material':m.name,'referenced_uv':n.uv_map,'exists':n.uv_map in o.data.uv_layers})
r={'scene':sc.name,'image_uv':rows,'readable_text_direction':texts,'image_failures':sum(not a['pass'] for a in rows),'text_failures':sum(not a['pass'] for a in texts),'uv_references':uvrefs,'missing_uv_references':sum(not a['exists'] for a in uvrefs),'negative_transforms':[o.name for o in sc.objects if o.matrix_world.determinant()<0]}
name='glb' if 'GLB_REIMPORT' in sc.name else 'original';(P/'qa'/f'{name}-orientation-audit.json').write_text(json.dumps(r,indent=2));print(name,'image UV',len(rows),'failed',r['image_failures'],'text',len(texts),'failed',r['text_failures'],'missingUV',r['missing_uv_references']);print([a for a in texts if not a['pass']][:15])
