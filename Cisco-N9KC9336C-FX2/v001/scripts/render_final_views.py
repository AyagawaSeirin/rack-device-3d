import bpy,sys,json,hashlib,datetime
from pathlib import Path
from mathutils import Vector,Matrix
ROOT=Path(__file__).resolve().parents[1];args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else [];worker=int(args[0]) if args else 0;workers=int(args[1]) if len(args)>1 else 1
s=bpy.context.scene
if len(args)>2 and args[2]=='handle-fix':assert all(o.get('sweep_fix') for o in s.objects if 'silver_U_pull_handle' in o.name), 'Saved handle repair absent'
c=s.camera;c.data.type='ORTHO';c.data.sensor_fit='HORIZONTAL';c.data.clip_start=.005;c.data.clip_end=20
s.render.engine='CYCLES';s.cycles.use_denoising=False;s.cycles.use_preview_denoising=False;s.cycles.adaptive_threshold=.025;s.cycles.use_adaptive_sampling=True
s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=True
floor=bpy.data.objects['Studio_shadow_floor'];floor.hide_set(False);floor.is_shadow_catcher=True
# White beauty background is composited in Blender. Raw-alpha QA is rendered separately.
s.use_nodes=True;nt=s.node_tree;nt.nodes.clear();rl=nt.nodes.new('CompositorNodeRLayers');over=nt.nodes.new('CompositorNodeAlphaOver');over.inputs[1].default_value=(1,1,1,1);nt.links.new(rl.outputs['Image'],over.inputs[2]);out=nt.nodes.new('CompositorNodeComposite');nt.links.new(over.outputs[0],out.inputs[0])
assembly=[o for o in s.objects if o.type=='MESH' and not any(x.name.startswith(('90_','98_')) for x in o.users_collection)]
points=[o.matrix_world@Vector(v) for o in assembly for v in o.bound_box]
centre=Vector((0,.01563,.02185))
# name, direction-from-target, image dimensions, target override, scale override, floor, samples
jobs=[
('front',(0,-1,0),(2600,410),None,None,False,128),('rear',(0,1,0),(2600,470),None,None,False,128),
('left',(-1,0,0),(2400,300),None,None,False,96),('right',(1,0,0),(2400,300),None,None,False,96),
('top',(0,0,1),(1600,2250),None,None,False,128),('bottom-INFERRED',(0,0,-1),(1600,2250),None,None,False,96),
('front-left',(-.85,-1.15,.58),(2000,1400),None,None,True,128),('front-right',(.85,-1.15,.58),(2000,1400),None,None,True,128),
('rear-left',(-.85,1.15,.58),(2000,1400),None,None,True,128),('rear-right',(.85,1.15,.58),(2000,1400),None,None,True,128),
('high-oblique',(.6,-.8,1.45),(1800,1800),None,None,True,128),('low-oblique-INFERRED',(-.9,-1.1,-.5),(2000,1200),None,None,False,128),
('detail-brand-controls',(0,-1,.07),(1800,1250),(-.203,-.294,.023),.083,False,192),
('detail-qsfp28',(.16,-1,.18),(1800,1250),(-.166,-.285,.0234),.079,False,192),
('detail-rear-management',(-.08,1,.07),(1800,1250),(-.135,.294,.022),.073,False,192),
('detail-left-ear-front',(-.5,-1,.15),(1600,1400),(-.227,-.280,.022),.073,False,128),
('detail-right-ear-back',(.8,1,.25),(1800,1200),(.227,-.253,.022),.130,False,128),
('detail-fan-module',(-.20,1,.15),(1800,1250),(.025,.301,.022),.118,False,192),
('detail-AC-power-supply',(-.45,1,.26),(1600,1400),(-.1885,.301,.022),.092,False,192),
('detail-top-ventilation',(.15,-.7,1),(1800,1150),(-.125,-.267,.0437),.155,False,128)]
def orient(pos,target,up):
 f=(target-pos).normalized();right=f.cross(up).normalized();u=right.cross(f).normalized();c.matrix_world=Matrix(((right.x,u.x,-f.x,pos.x),(right.y,u.y,-f.y,pos.y),(right.z,u.z,-f.z,pos.z),(0,0,0,1)))
results=[]
for i,(name,direction,res,target,scale,usefloor,samples) in enumerate(jobs):
 if i%workers!=worker:continue
 if len(args)>2 and args[2]=='handle-fix' and i not in list(range(12))+[18]:continue
 tgt=Vector(target) if target else centre;d=Vector(direction).normalized();up=Vector((0,1,0)) if abs(d.z)>.999 else Vector((0,0,1));orient(tgt+d*1.8,tgt,up)
 s.render.resolution_x,s.render.resolution_y=res;aspect=res[0]/res[1]
 if scale is None:
  inv=c.matrix_world.inverted();pp=[inv@p for p in points];xmin=min(p.x for p in pp);xmax=max(p.x for p in pp);ymin=min(p.y for p in pp);ymax=max(p.y for p in pp)
  offset=c.matrix_world.to_3x3()@Vector(((xmin+xmax)/2,(ymin+ymax)/2,0));c.location+=offset;c.data.ortho_scale=max(xmax-xmin,(ymax-ymin)*aspect)*1.10
 else:c.data.ortho_scale=scale
 floor.hide_render=not usefloor;s.cycles.samples=samples
 outpath=ROOT/'previews'/f'{name}.png';s.render.filepath=str(outpath);bpy.ops.render.render(write_still=True)
 r={'name':name,'path':str(outpath.relative_to(ROOT)),'resolution':res,'samples':samples,'sha256':hashlib.sha256(outpath.read_bytes()).hexdigest(),'view_direction':direction,'camera_matrix':[list(row) for row in c.matrix_world],'ortho_scale_m':c.data.ortho_scale,'beauty_background':'Blender AlphaOver white; separate raw-alpha tests validate opacity','inferred_bottom':'INFERRED' in name,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};results.append(r)
 (ROOT/'qa'/(f'final-renders-handle-fix-worker-{worker}.json' if len(args)>2 and args[2]=='handle-fix' else f'final-renders-worker-{worker}.json')).write_text(json.dumps(results,indent=2));print('VIEW_COMPLETE',name,flush=True)
