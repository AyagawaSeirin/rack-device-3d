from pathlib import Path
import bpy,json,hashlib,time
ROOT=Path(__file__).resolve().parents[1];s=bpy.context.scene
assert s.name=='CISCO_N9K_C9336C_FX2_V001'
bpy.ops.object.select_all(action='DESELECT');selected=[]
for o in s.objects:
 if any(c.name.startswith(('90_','98_')) for c in o.users_collection):continue
 if o.type in ['MESH','EMPTY']:o.select_set(True);selected.append(o)
assert sum(o.get('component_type')=='business_port' for o in selected)==36
assert sum(o.get('component_type')=='rack_ear' for o in selected)==2
assert not any(o.type in ['LIGHT','CAMERA'] for o in selected)
props={p.identifier for p in bpy.ops.export_scene.gltf.get_rna_type().properties}
kwargs={'filepath':str(ROOT/'model/CISCO-Nexus-N9K-C9336C-FX2.glb'),'export_format':'GLB','use_selection':True,'export_extras':True,'export_yup':True,'export_apply':False,'export_texcoords':True,'export_normals':True,'export_tangents':True,'export_materials':'EXPORT','export_cameras':False,'export_lights':False,'export_animations':False,'export_image_format':'AUTO'}
assert all(k in props for k in ['use_selection','export_format','export_extras','export_yup'])
kwargs={k:v for k,v in kwargs.items() if k in props};bpy.ops.export_scene.gltf(**kwargs)
bpy.ops.object.select_all(action='DESELECT');p=ROOT/'model/CISCO-Nexus-N9K-C9336C-FX2.glb'
(ROOT/'qa/export.json').write_text(json.dumps({'file':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size,'selected_nodes':len(selected),'excluded_collections':['90_STUDIO','98_EDITABLE_TEXT_SOURCES'],'options':kwargs},indent=2))
print('EXPORTED',p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest())
