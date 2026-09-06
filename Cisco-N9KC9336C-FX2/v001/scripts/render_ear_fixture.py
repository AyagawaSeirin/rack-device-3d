import bpy,json,sys,hashlib
from pathlib import Path
from mathutils import Vector,Matrix
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];prefix=sys.argv[sys.argv.index('--')+1] if '--' in sys.argv else 'original';s=bpy.data.scenes['EAR_ISOLATION_QA'];bpy.context.window.scene=s;c=s.camera;s.use_nodes=False;s.render.film_transparent=True;s.cycles.use_denoising=False;s.cycles.use_preview_denoising=False;s.cycles.samples=40;s.render.image_settings.color_mode='RGBA';s.render.image_settings.file_format='PNG'
ears=[o for o in s.objects if o.get('component_type')=='rack_ear'];bg=bpy.data.objects['QA_CHECKER_BACKGROUND'];results=[]
def orient(pos,target):
 f=(target-pos).normalized();up=Vector((0,0,1));r=f.cross(up).normalized();u=r.cross(f);c.matrix_world=Matrix(((r.x,u.x,-f.x,pos.x),(r.y,u.y,-f.y,pos.y),(r.z,u.z,-f.z,pos.z),(0,0,0,1)))
 c.data.sensor_fit='HORIZONTAL';c.data.type='ORTHO';c.data.clip_start=.001
jobs=[('front',(0,-1,0),(0,-.294,.021844),.53,(2200,380),None),('back',(0,1,0),(0,-.294,.021844),.53,(2200,380),None),('right-side',(1,0,0),(.221,-.25,.021844),.12,(1500,800),'RIGHT'),('left-side',(-1,0,0),(-.221,-.25,.021844),.12,(1500,800),'LEFT'),('front-oblique',(.3,-1,.3),(0,-.268,.021844),.54,(1800,500),None),('back-oblique',(-.3,1,.3),(0,-.268,.021844),.54,(1800,500),None),('grazing',(.92,-.18,.12),(.224,-.255,.021844),.14,(1600,800),'RIGHT')]
for name,direction,target,scale,res,side in jobs:
 target=Vector(target);d=Vector(direction).normalized();orient(target+d*.8,target);c.data.ortho_scale=scale;s.render.resolution_x,s.render.resolution_y=res
 for o in ears:o.hide_render=side is not None and o['side']!=side
 # Checker stays behind the observed metal, in a plane normal to camera axis.
 bg.rotation_euler=c.rotation_euler;bg.rotation_euler.x-=1.57079632679;bg.location=target-d*.20
 for mode in (['checker','alpha'] if name in ['front','back','right-side','left-side'] else ['checker']):
  bg.hide_render=mode=='alpha';out=ROOT/'qa'/f'{prefix}-ear-{name}-{mode}.png';s.render.filepath=str(out);bpy.ops.render.render(write_still=True)
  record={'view':name,'mode':mode,'path':str(out.relative_to(ROOT)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'samples':[]}
  if mode=='alpha':
   im=bpy.data.images.load(str(out),check_existing=False);w,h=im.size
   import numpy as np
   pix=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4)
   tests=[]
   if name in ['front','back']:
    for sg in [-1,1]:
     for z in [.005969,.021844,.037719]:tests.append(('hole',[sg*.2326,-.2941,z],0))
     tests.append(('metal',[sg*.2248,-.2941,.021844],1))
   else:
    sg=1 if side=='RIGHT' else -1
    for y in [-.284,-.270,-.256,-.242,-.228,-.214]:
     for z in [.0108,.0328]:tests.append(('hole',[sg*.22086,y,z],0))
    tests.append(('metal',[sg*.22086,-.250,.022],1))
   for kind,point,expected in tests:
    uv=world_to_camera_view(s,c,Vector(point));x=int(uv.x*w);y=int(uv.y*h);a=float(pix[max(0,y-1):min(h,y+2),max(0,x-1):min(w,x+2),3].mean());ok=a<.015 if expected==0 else a>.985
    record['samples'].append({'kind':kind,'world_point':point,'pixel':[x,y],'expected_alpha':expected,'actual_mean_alpha':a,'pass':ok})
   bpy.data.images.remove(im)
  results.append(record);(ROOT/'qa'/f'{prefix}-ear-render-tests.json').write_text(json.dumps({'pass':all(x['pass'] for r in results for x in r['samples']),'renders':results,'note':'Only isolated unobstructed holes expected transparent; AA edge pixels not sampled.'},indent=2));print('EAR_QA_RENDER',prefix,name,mode,flush=True)
