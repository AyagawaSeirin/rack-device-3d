import bpy,json,math,sys
from pathlib import Path
from mathutils import Vector
P=Path('/root/Blender/DELL-C6420/v001');sc=bpy.context.scene;cam=sc.camera
sc.render.engine='CYCLES';sc.cycles.samples=96;sc.cycles.use_denoising=False;sc.render.threads_mode='FIXED';sc.render.threads=10
sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=False
sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.88,.90,.93,1);sc.world.node_tree.nodes['Background'].inputs[1].default_value=.30
sc.render.resolution_x=1400;sc.render.resolution_y=950
views={'front-right':((.9,-1.3,.66),(0,0,.04),1.10),'rear-left':((-.9,1.3,.66),(0,0,.04),1.10),'front':((0,-2,.0434),(0,0,.0434),.53),'rear':((0,2,.0434),(0,0,.0434),.53),'left':((-2,0,.0434),(0,0,.0434),.89),'right':((2,0,.0434),(0,0,.0434),.89),'top':((0,0,2),(0,0,0),.92),'bottom':((0,0,-2),(0,0,0),.92),'front-left':((-.9,-1.3,.66),(0,0,.04),1.10),'rear-right':((.9,1.3,.66),(0,0,.04),1.10),'brand-detail':((-.26,-.65,.09),(-.227,-.398,.050),.095),'rear-node-detail':((-.16,.72,.08),(-.133,.385,.064),.20),'psu-detail':((.02,.65,.065),(0,.385,.043),.13),'carrier-detail':((-.10,-.60,.09),(-.10,-.394,.043),.10),'low-rear':((-.65,1,-.43),(0,0,.04),1.04),'high-front':((.5,-.75,1.5),(0,0,.04),1.04)}
keys=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else list(views)
for key in keys:
 pos,target,scale=views[key];cam.location=pos;direction=Vector(target)-cam.location
 cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale
 if key in {'top','bottom'}:
  # Horizontal top/bottom orientation: +Y at screen top; bottom reverses X naturally.
  cam.rotation_euler=(0,0,0) if key=='top' else (math.pi,0,math.pi)
  sc.render.resolution_x=1100;sc.render.resolution_y=1550;cam.data.ortho_scale=.91
 else:sc.render.resolution_x=1400;sc.render.resolution_y=950
 sc.render.filepath=str(P/'previews'/(key+'.png'));bpy.ops.render.render(write_still=True)
 (P/'qa/render-progress.json').write_text(json.dumps({'last_completed':key,'requested':keys}))
 print('PREVIEW_DONE',key,flush=True)
