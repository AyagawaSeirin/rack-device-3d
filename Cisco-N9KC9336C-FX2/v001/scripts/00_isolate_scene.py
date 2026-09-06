import bpy,json,datetime
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
assert json.loads((ROOT/'imagegen/phase-complete.json').read_text())['reference_phase_complete']
assert json.loads((ROOT/'qa/pre-task-blender-state.json').read_text())['saved']
assert not bpy.data.is_dirty, 'Save new user edits before switching away'
previous=bpy.data.filepath
scene=bpy.data.scenes.new('CISCO_N9K_C9336C_FX2_V001')
bpy.context.window.scene=scene
for s in list(bpy.data.scenes):
 if s!=scene:bpy.data.scenes.remove(s)
for o in list(bpy.data.objects):
 if o.name not in scene.objects:bpy.data.objects.remove(o,do_unlink=True)
bpy.data.orphans_purge(do_local_ids=True,do_linked_ids=True,do_recursive=True)
scene.unit_settings.system='METRIC';scene.unit_settings.scale_length=1;scene.unit_settings.length_unit='MILLIMETERS'
scene.render.engine='CYCLES';scene.cycles.use_denoising=False;scene.cycles.use_preview_denoising=False
scene.cycles.samples=48;scene.render.threads_mode='FIXED';scene.render.threads=8
scene['PID']='N9K-C9336C-FX2';scene['coordinate_contract']='metres; bottom centre; front -Y; rear +Y; right +X'
scene['evidence']='See ../EVIDENCE.md and ../DIMENSIONS.md';scene['reference_stage_complete']=True
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  a.spaces.active.shading.type='SOLID';a.spaces.active.clip_start=0.0005;a.spaces.active.clip_end=20
scene.world=bpy.data.worlds.new('CISCO_NEUTRAL_WORLD');scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(0.65,0.65,0.65,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=0.45
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/00-isolated-scene.blend'),compress=True)
(ROOT/'qa/isolation.json').write_text(json.dumps({'previous_preserved_file':previous,'new_file':bpy.data.filepath,'objects':len(scene.objects),'time':datetime.datetime.now(datetime.timezone.utc).isoformat()},indent=2))
print('ISOLATION SAVED',bpy.data.filepath)
