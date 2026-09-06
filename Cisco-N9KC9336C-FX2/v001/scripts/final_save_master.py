from pathlib import Path
import bpy,json,hashlib
ROOT=Path(__file__).resolve().parents[1];s=bpy.context.scene;assert s.name=='CISCO_N9K_C9336C_FX2_V001';assert len(bpy.data.scenes)==1
if bpy.context.screen.is_animation_playing:bpy.ops.screen.animation_cancel(restore_frame=False)
s.frame_set(1);bpy.ops.object.select_all(action='DESELECT')
for im in bpy.data.images:
 if im.source=='FILE' and im.filepath:
  absolute=bpy.path.abspath(im.filepath)
  if Path(absolute).is_file():im.filepath=bpy.path.relpath(absolute,start=str(ROOT/'model'))
for fo in bpy.data.fonts:
 if fo.filepath and not fo.filepath.startswith('<'):
  # Font data is packed; keep original font source path as attribution only.
  pass
bpy.ops.file.pack_all();v=next(a.spaces.active for a in bpy.context.screen.areas if a.type=='VIEW_3D');v.shading.type='MATERIAL';v.shading.use_scene_world=True;v.shading.use_scene_lights=True;v.overlay.show_overlays=False;v.clip_start=.01;v.clip_end=10
s['lighting_recipe']='Neutral world0.45; AREA KEY8W size1.1m,FILL5.2W0.9m,RIM8W0.8m; AgX Medium High Contrast,exposure0; no emission.'
s['delivery_geometry_triangles']=484031;s['delivery_glb_sha256']=hashlib.sha256((ROOT/'model/CISCO-Nexus-N9K-C9336C-FX2.glb').read_bytes()).hexdigest();s['estimate_disclosure']='Bottom inferred; unmeasured hole pitches,thicknesses,hidden contacts and rotor positions estimated. See DIMENSIONS.md,EVIDENCE.md,QA.md.'
state={'q':list(v.region_3d.view_rotation),'distance':v.region_3d.view_distance,'location':list(v.region_3d.view_location),'mode':v.shading.type,'scene_world':v.shading.use_scene_world,'scene_lights':v.shading.use_scene_lights,'animation':bpy.context.screen.is_animation_playing,'frame':s.frame_current}
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/CISCO-Nexus-N9K-C9336C-FX2.blend'),compress=True);(ROOT/'qa/final-saved-view.json').write_text(json.dumps(state,indent=2));print('MASTER_SAVED',state)
