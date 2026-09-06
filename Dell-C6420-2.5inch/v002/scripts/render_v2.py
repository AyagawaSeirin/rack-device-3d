import bpy,sys,math,json
from mathutils import Vector
from pathlib import Path
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');sc=bpy.context.scene;cam=sc.camera
sc.render.engine='CYCLES';sc.cycles.samples=192;sc.cycles.use_denoising=False;sc.cycles.use_preview_denoising=False;sc.render.threads_mode='FIXED';sc.render.threads=10;sc.render.resolution_percentage=100
# Camera definitions separate evidence elevations from photograph-like low3/4 views.
views={
 'front-right':((.90,-1.75,.50),(0,0,.04),.98,1800,1050),
 'front-left':((-.90,-1.75,.50),(0,0,.04),.98,1800,1050),
 'rear-left':((-.90,1.75,.50),(0,0,.04),.98,1800,1050),
 'rear-right':((.90,1.75,.50),(0,0,.04),.98,1800,1050),
 'front':((0,-2,.0434),(0,0,.0434),.515,1800,620),
 'rear':((0,2,.0434),(0,0,.0434),.490,1800,620),
 'left':((-2,0,.0434),(0,0,.0434),.88,1800,620),
 'right':((2,0,.0434),(0,0,.0434),.88,1800,620),
 'top':((0,0,2),(0,0,0),.89,1100,1750),
 'bottom':((0,0,-2),(0,0,0),.89,1100,1750),
 'high-front':((.6,-.9,1.6),(0,0,.04),1.02,1600,1250),
 'low-rear':((-.8,1.5,-.50),(0,0,.04),1.02,1600,1050),
 'carrier-detail':((-.065,-.66,.075),(-.113,-.397,.0434),.094,1100,1500),
 'brand-detail':((-.26,-.71,.075),(-.224,-.397,.048),.091,1000,1500),
 'node-detail':((.140, .80,.090),(.1328,.383,.064),.195,1900,780),
 'psu-detail':((.005,.78,.074),(0,.383,.0434),.110,1400,1350),
 'source-front-comparison':((0,-2,.36),(0,0,.04),.540,1800,950),
 'source-rear-comparison':((0,2,.35),(0,0,.04),.515,1800,950)
}
keys=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else list(views)
for key in keys:
 pos,target,scale,w,h=views[key];cam.location=pos;cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale;cam.data.clip_start=.001;cam.data.clip_end=20
 if key=='top':cam.rotation_euler=(0,0,0)
 if key=='bottom':cam.rotation_euler=(math.pi,0,math.pi)
 sc.render.resolution_x=w;sc.render.resolution_y=h;sc.render.filepath=str(P/'previews'/(key+'.png'));bpy.ops.render.render(write_still=True)
 (P/'qa/render-progress.json').write_text(json.dumps({'last':key,'requested':keys}));print('V002_RENDER_DONE',key,flush=True)
