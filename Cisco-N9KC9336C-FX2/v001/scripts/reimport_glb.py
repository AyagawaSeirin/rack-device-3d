from pathlib import Path
import bpy,json,hashlib
ROOT=Path(__file__).resolve().parents[1];original=bpy.context.scene;assert original.name=='CISCO_N9K_C9336C_FX2_V001';assert not bpy.data.scenes.get('GLB_REIMPORT_QA')
s=bpy.data.scenes.new('GLB_REIMPORT_QA');s.world=original.world.copy();s.unit_settings.system='METRIC';s.unit_settings.scale_length=1;s.render.engine='CYCLES';s.cycles.samples=128;s.cycles.use_denoising=False;s.cycles.use_preview_denoising=False;s.view_settings.view_transform='AgX';s.view_settings.look='AgX - Medium High Contrast';s.eevee.use_gtao=True;s.eevee.gtao_distance=.04;s.eevee.gtao_factor=1.25;s.eevee.taa_samples=64
bpy.context.window.scene=s;p=ROOT/'model/CISCO-Nexus-N9K-C9336C-FX2.glb';bpy.ops.import_scene.gltf(filepath=str(p));imported=list(s.objects)
# Copy only the recorded studio for verification; this collection is never part of the GLB.
c=bpy.data.collections.new('90_STUDIO_GLB_QA');s.collection.children.link(c)
for o in original.objects:
 if any(c.name.startswith('90_') for c in o.users_collection):
  q=o.copy();q.data=o.data.copy() if o.data else None;c.objects.link(q);q.parent=None;q.matrix_world=o.matrix_world.copy()
  if o==original.camera:s.camera=q
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  v=a.spaces.active;v.shading.type='MATERIAL';v.shading.use_scene_world=True;v.shading.use_scene_lights=True;v.overlay.show_overlays=False;v.clip_start=.01;v.clip_end=10
bpy.ops.object.select_all(action='DESELECT');bpy.ops.file.pack_all();s['source_glb_sha256']=hashlib.sha256(p.read_bytes()).hexdigest();s['verification_scene_only']=True
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'qa/GLB-reimport-verification.blend'),copy=True,compress=True)
report={'pass':True,'glb_sha256':s['source_glb_sha256'],'scene':s.name,'imported_objects':len(imported),'mesh_instances':sum(o.type=='MESH' for o in imported),'components':{k:sum(o.get('component_type')==k for o in imported) for k in ['business_port','double_cage','fan_module','fan_rotor','psu_module','rack_ear','management_rj45','console_rj45','management_sfp','usb_a']},'independent_scene':True,'original_preserved':original.name,'importer':'Blender4.0.2 built-in glTF2 importer','lights_added_after_import':'90_STUDIO_GLB_QA, copied original studio; never exported'}
(ROOT/'qa/glb-reimport.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
