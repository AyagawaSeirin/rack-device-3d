import bpy,json
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path('/root/Blender/DELL-C6420/v001');s=bpy.context.scene;assert 'GLB_REIMPORT' in s.name
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=64;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=8
s.render.resolution_x=1400;s.render.resolution_y=950;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=True
s.world.node_tree.nodes['Background'].inputs[0].default_value=(.88,.9,.93,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.30
cam=s.camera;cam.data.type='ORTHO';cam.data.ortho_scale=1.10
for name,pos in [('front-right',(.9,-1.3,.66)),('rear-left',(-.9,1.3,.66))]:
 cam.location=pos;cam.rotation_euler=(Vector((0,0,.04))-cam.location).to_track_quat('-Z','Y').to_euler()
 s.use_nodes=False;s.render.filepath=str(P/'qa'/('glb-'+name+'-transparent.png'));bpy.ops.render.render(write_still=True)
 if name=='front-right':
  probes=[]
  for x,y in [(-.16,-.3),(0,-.3),(.16,-.3),(-.16,-.1),(0,-.1),(.16,-.1),(-.16,.18),(0,.18),(.16,.18)]:
   p=world_to_camera_view(s,cam,Vector((x,y,.0864)));probes.append({'world':[x,y,.0864],'pixel':[round(p.x*1399),round((1-p.y)*949)]})
  (P/'qa/alpha-probe-pixels.json').write_text(json.dumps(probes,indent=2))
 s.use_nodes=True;nt=s.node_tree;nt.nodes.clear();rl=nt.nodes.new('CompositorNodeRLayers');over=nt.nodes.new('CompositorNodeAlphaOver');out=nt.nodes.new('CompositorNodeComposite');over.inputs[0].default_value=1
 nt.links.new(rl.outputs['Image'],over.inputs[2]);nt.links.new(over.outputs['Image'],out.inputs[0])
 for bg,color in [('light',(.9,.9,.9,1)),('dark',(.008,.012,.018,1))]:
  over.inputs[1].default_value=color;s.render.filepath=str(P/'qa'/('glb-'+name+'-'+bg+'.png'));bpy.ops.render.render(write_still=True);print('GLB_BACKGROUND_CHECK',name,bg,flush=True)
