"""Independent render-only QA; test opaque interior samples, not hole/AA boundaries."""
from pathlib import Path
import bpy,json,sys,hashlib,numpy as np
from mathutils import Vector,Matrix
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[1];prefix=sys.argv[sys.argv.index('--')+1];s=bpy.data.scenes['GLB_REIMPORT_QA' if prefix=='glb' else 'CISCO_N9K_C9336C_FX2_V001'];bpy.context.window.scene=s;c=s.camera;s.use_nodes=False;s.render.film_transparent=True;s.cycles.samples=40;s.cycles.adaptive_threshold=.05;s.cycles.use_denoising=False;s.cycles.use_preview_denoising=False;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.resolution_percentage=100
for o in s.objects:
 if o.name.startswith('Studio_shadow_floor'):o.hide_render=True
reports=[]
for view,dr,up in [('top',(0,0,1),(0,1,0)),('bottom-INFERRED',(0,0,-1),(0,1,0)),('left',(-1,0,0),(0,0,1)),('right',(1,0,0),(0,0,1))]:
 target=Vector((0,0,.021844));d=Vector(dr);p=target+d*.9;f=-d;r=f.cross(Vector(up)).normalized();u=r.cross(f);c.matrix_world=Matrix(((r.x,u.x,-f.x,p.x),(r.y,u.y,-f.y,p.y),(r.z,u.z,-f.z,p.z),(0,0,0,1)));c.data.type='ORTHO';c.data.sensor_fit='HORIZONTAL';c.data.ortho_scale=.7;c.data.clip_start=.001
 s.render.resolution_x=1000;s.render.resolution_y=1050 if 'top' in view or 'bottom' in view else 200
 out=ROOT/'qa'/f'{prefix}-shell-{view}-transparent.png';s.render.filepath=str(out);bpy.ops.render.render(write_still=True)
 im=bpy.data.images.load(str(out),check_existing=False);w,h=im.size;pix=np.array(im.pixels[:],dtype=np.float32).reshape(h,w,4)
 points=([[x,y,.043688 if view=='top' else 0] for x in [-.08,0,.1] for y in [-.15,0,.15]] if view in ['top','bottom-INFERRED'] else [[.21971 if view=='right' else -.21971,y,z] for y in [-.12,0,.12] for z in [.010,.021,.032]])
 samples=[]
 for pt in points:
  uv=world_to_camera_view(s,c,Vector(pt));x=int(uv.x*w);y=int(uv.y*h);a=float(pix[y-1:y+2,x-1:x+2,3].min());samples.append({'point_m':pt,'pixel':[x,y],'min_3x3_alpha':a,'pass':a>.985})
 bpy.data.images.remove(im);reports.append({'view':view,'transparent':str(out.relative_to(ROOT)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'samples':samples});(ROOT/'qa'/f'{prefix}-shell-render-tests.json').write_text(json.dumps({'pass':all(p['pass'] for r in reports for p in r['samples']),'renders':reports,'coverage':'36 dispersed closed-surface sample patches; actual ventilation and AA edges excluded'},indent=2));print('SHELL_ALPHA',prefix,view,flush=True)
