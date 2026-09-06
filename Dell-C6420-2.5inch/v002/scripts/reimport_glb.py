import bpy,json,contextlib
from pathlib import Path
from mathutils import Vector
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');master=bpy.context.scene
qa=bpy.data.scenes.new('C6420_GLB_REIMPORT_QA');bpy.context.window.scene=qa
qa.unit_settings.system='METRIC';qa.unit_settings.scale_length=1
with (P/'qa/glb-import.log').open('w') as log,contextlib.redirect_stdout(log):
 bpy.ops.import_scene.gltf(filepath=str(P/'model/DELL-PowerEdge-C6420-4N-24SFF.glb'))
imported=list(qa.objects);pts=[o.matrix_world@v.co for o in imported if o.type=='MESH' for v in o.data.vertices]
lo=[min(p[i] for p in pts) for i in range(3)];hi=[max(p[i] for p in pts) for i in range(3)]
report={'scene':qa.name,'mesh_count':sum(o.type=='MESH' for o in imported),'bbox_min_m':lo,'bbox_max_m':hi,'bbox_mm':[(b-a)*1000 for a,b in zip(lo,hi)],'component_counts':{k:sum(o.get('component_type')==k for o in imported) for k in ['2.5-inch hot-swap carrier','C6420 node','2400W PSU']},'negative_transforms':[o.name for o in imported if o.matrix_world.determinant()<0], 'label_objects':[o.name for o in imported if o.get('source_asset')], 'packed_images':list({n.image.name for o in imported if o.type=='MESH' for m in o.data.materials if m and m.use_nodes for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image}), 'materials_transparency':[]}
for m in {m for o in imported if o.type=='MESH' for m in o.data.materials if m}:
 bs=m.node_tree.nodes.get('Principled BSDF')
 if bs:report['materials_transparency'].append({'name':m.name,'alpha':bs.inputs['Alpha'].default_value,'alpha_linked':bs.inputs['Alpha'].is_linked,'transmission':bs.inputs['Transmission Weight'].default_value,'blend_method':m.blend_method})
(P/'qa/glb-reimport-audit.json').write_text(json.dumps(report,indent=2))
# Copy studio only, so the imported model can be compared with identical lighting.
qa.world=master.world.copy();studio=bpy.data.collections.new('90_STUDIO');qa.collection.children.link(studio)
for ob in master.objects:
 if ob.type in {'CAMERA','LIGHT'}:
  copy=ob.copy();copy.data=ob.data.copy();studio.objects.link(copy)
  if ob.type=='CAMERA':qa.camera=copy
qa.render.engine='CYCLES';qa.cycles.device='CPU';qa.cycles.samples=96;qa.cycles.use_denoising=False;qa.cycles.use_preview_denoising=False
qa.render.resolution_x=1400;qa.render.resolution_y=950;qa.render.resolution_percentage=100
qa.view_settings.view_transform='AgX';qa.view_settings.look='AgX - Medium High Contrast';qa.render.image_settings.file_format='PNG';qa.render.film_transparent=False
qa.eevee.taa_samples=128;qa.eevee.taa_render_samples=128;qa.eevee.use_gtao=True;qa.eevee.gtao_distance=.025;qa.eevee.gtao_factor=1.25
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  s=a.spaces.active;s.clip_start=.001;s.clip_end=20;s.shading.type='SOLID';s.shading.use_scene_world=True;s.shading.use_scene_lights=True;s.overlay.show_overlays=False
  s.region_3d.view_location=Vector((0,0,.04));s.region_3d.view_distance=1.15;s.region_3d.view_rotation=Vector((1,-1.4,.8)).to_track_quat('Z','Y')
for o in qa.objects:o.select_set(False)
bpy.ops.wm.save_as_mainfile(filepath=str(P/'qa/GLB-reimport-verification.blend'),copy=True)
print(json.dumps({k:report[k] for k in ['scene','mesh_count','bbox_mm','component_counts','negative_transforms','label_objects']},indent=2))
