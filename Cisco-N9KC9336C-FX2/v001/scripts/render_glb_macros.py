from pathlib import Path
import bpy,json,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];s=bpy.data.scenes['GLB_REIMPORT_QA'];bpy.context.window.scene=s;c=s.camera;s.use_nodes=True;nt=s.node_tree;nt.nodes.clear();rl=nt.nodes.new('CompositorNodeRLayers');over=nt.nodes.new('CompositorNodeAlphaOver');over.inputs[1].default_value=(1,1,1,1);nt.links.new(rl.outputs['Image'],over.inputs[2]);out=nt.nodes.new('CompositorNodeComposite');nt.links.new(over.outputs[0],out.inputs[0]);s.render.film_transparent=True
for o in s.objects:
 if o.name.startswith('Studio_shadow_floor'):o.hide_render=True
s.render.engine='CYCLES';s.cycles.samples=96;s.cycles.adaptive_threshold=.025;s.cycles.use_denoising=False;s.cycles.use_preview_denoising=False;s.render.resolution_x=1200;s.render.resolution_y=1000;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';records=[]
for name,target,direction,scale in [('brand',(-.203,-.294,.023),(0,-1,.07),.083),('PSU-handle',(-.1885,.301,.022),(-.45,1,.26),.092)]:
 t=Vector(target);d=Vector(direction).normalized();c.location=t+d*1.8;c.rotation_euler=(t-c.location).to_track_quat('-Z','Y').to_euler();c.data.type='ORTHO';c.data.sensor_fit='HORIZONTAL';c.data.ortho_scale=scale;c.data.clip_start=.005;p=ROOT/'qa'/f'glb-detail-{name}.png';s.render.filepath=str(p);bpy.ops.render.render(write_still=True);records.append({'name':name,'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_glb_sha256':s['source_glb_sha256']});(ROOT/'qa/glb-macro-renders.json').write_text(json.dumps(records,indent=2));print('GLB_MACRO',name,flush=True)
