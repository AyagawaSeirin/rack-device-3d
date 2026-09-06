import bpy,json,contextlib
from pathlib import Path
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');scene=bpy.context.scene
scene.name='DELL_C6420_4N_24SFF_V002_MASTER'
scene.eevee.taa_samples=128;scene.eevee.taa_render_samples=128
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':a.spaces.active.shading.type='SOLID'
bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
# Pack images and current source files into the editable project.
for img in bpy.data.images:
 if img.source=='FILE' and img.users:img.pack()
for name in [f.name for f in (P/'scripts').glob('*.py')]:
 tx=bpy.data.texts.get(name) or bpy.data.texts.new(name);tx.clear();tx.write((P/'scripts'/name).read_text())
bpy.ops.object.select_all(action='DESELECT')
selected=[]
for ob in scene.objects:
 if not any(c.name=='90_STUDIO' for c in ob.users_collection):ob.select_set(True);selected.append(ob)
bpy.context.view_layer.objects.active=next(o for o in selected if o.type=='MESH')
with (P/'qa/export-final.log').open('w') as log,contextlib.redirect_stdout(log):
 bpy.ops.export_scene.gltf(filepath=str(P/'model/DELL-PowerEdge-C6420-4N-24SFF.glb'),export_format='GLB',use_selection=True,export_apply=True,export_yup=True,export_texcoords=True,export_normals=True,export_materials='EXPORT',export_extras=True,export_cameras=False,export_lights=False,export_animations=False)
for ob in selected:ob.select_set(False)
scene.render.filepath=str(P/'previews/front-right.png')
bpy.ops.wm.save_as_mainfile(filepath=str(P/'model/DELL-PowerEdge-C6420-4N-24SFF.blend'))
print('GLB and packed editable master saved')
# Verify body and individual node bounding boxes from actual assembled components.
from mathutils import Vector

def bbox(obs):
 pts=[ob.matrix_world@v.co for ob in obs if ob.type=='MESH' for v in ob.data.vertices]
 lo=[min(v[i] for v in pts) for i in range(3)];hi=[max(v[i] for v in pts) for i in range(3)]
 return {'min_m':lo,'max_m':hi,'dimensions_mm':[(b-a)*1000 for a,b in zip(lo,hi)]}
result={'whole':bbox(selected),'nodes':{str(i):bbox(list(bpy.data.collections['04_NODE_'+str(i)].objects)) for i in range(1,5)}}
result['official_mm']={'whole_width_incl_ears':482.6,'whole_depth_incl_both_protrusions':824.1,'whole_height':86.8,'body_width':448,'body_depth_from_mount':763.2,'node_xyz':[174.4,574.5,40.5]}
(P/'qa/measured-dimensions.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
