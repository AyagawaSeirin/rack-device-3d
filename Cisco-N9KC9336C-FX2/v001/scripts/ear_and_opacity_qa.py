from pathlib import Path
import bpy,json,math
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1]
sc=bpy.context.scene;prefix='glb' if sc.name.startswith('GLB_REIMPORT') else 'original';ears=[o for o in sc.objects if o.get('component_type')=='rack_ear']
assert len(ears)==2
rows=[]
def cast(obj,origin,direction,distance=.1):
 inv=obj.matrix_world.inverted();org=inv@Vector(origin);d=(inv.to_3x3()@Vector(direction)).normalized()
 hit,loc,n,face=obj.ray_cast(org,d,distance=distance)
 return {'hit':bool(hit),'object':obj.name if hit else None,'normal':list((obj.matrix_world.inverted().transposed().to_3x3()@n).normalized()) if hit else None,'point':list(obj.matrix_world@loc) if hit else None}
for ear in ears:
 sign=1 if ear['side']=='RIGHT' else -1
 for z in [21.844-15.875,21.844,21.844+15.875]:
  for direction in [-1,1]:
   start=[sign*.2326,(-.301 if direction==1 else -.288),z/1000];r=cast(ear,start,[0,direction,0],.02);rows.append({'kind':'isolated_rack_slot','expected':'miss','pass':not r['hit'],'origin_m':start,'direction':[0,direction,0],**r})
 for y in [-284,-270,-256,-242,-228,-214]:
  for z in [10.8,32.8]:
   start=[sign*.228,y/1000,z/1000];r=cast(ear,start,[-sign,0,0],.02);rows.append({'kind':'isolated_side_arm_hole','expected':'miss','pass':not r['hit'],'origin_m':start,'direction':[-sign,0,0],**r})
 for direction in [-1,1]:
  start=[sign*.2248,(-.301 if direction==1 else -.288),.021844];r=cast(ear,start,[0,direction,0],.02);rows.append({'kind':'metal_land_front_back','expected':'ear hit, outward normal','pass':r['hit'] and Vector(r['normal']).dot(Vector((0,direction,0)))<-.98,'origin_m':start,'direction':[0,direction,0],**r})
 for z in [.018,.029]:
  start=[sign*.228,-.250,z];r=cast(ear,start,[-sign,0,0],.02);rows.append({'kind':'side_metal_land','expected':'ear hit','pass':r['hit'],'origin_m':start,'direction':[-sign,0,0],**r})
# Formal assembly ray casting; includes real screws, shell occlusion and empty aligned holes.
dg=bpy.context.evaluated_depsgraph_get();assembly=[]
def scene_cast(origin,direction,dist=.1):
 start=Vector(origin);dr=Vector(direction);remain=dist
 for attempt in range(5):
  hit,loc,n,fi,obj,matrix=sc.ray_cast(dg,start,dr,distance=remain)
  if hit and any(c.name.startswith('90_') for c in obj.users_collection):
   remain-=(loc-start).length+1e-5;start=loc+dr*1e-5
   continue
  break
 return {'hit':bool(hit),'object':obj.name if hit else None,'normal':list(n) if hit else None,'point':list(loc) if hit else None}
for ear in ears:
 sign=1 if ear['side']=='RIGHT' else -1
 for y in [-284,-270,-256,-242,-228,-214]:
  for z in [10.8,32.8]:
   start=[sign*.227,y/1000,z/1000];r=scene_cast(start,[-sign,0,0],.01)
   expected='ear fastener' if y in [-284,-256] else 'main sidewall' if y in [-270,-242,-214] else 'empty aligned chassis bore'
   ok=(r['hit'] and '_ear_M4_' in r['object']) if expected=='ear fastener' else (r['hit'] and 'sidewall' in r['object']) if expected=='main sidewall' else not r['hit']
   assembly.append({'kind':'assembled_side_arm','expected':expected,'pass':ok,'origin_m':start,**r})
 for z in [.005969,.021844,.037719]:
  r=scene_cast([sign*.2326,-.301,z],[0,1,0],.1);assembly.append({'kind':'assembled_empty_rack_slot','expected':'background/miss','pass':not r['hit'],**r})
opaque=[]
for x in [-.08,0,.1]:
 for y in [-.15,0,.15]:
  for name,start,d in [('top',[x,y,.08],[0,0,-1]),('bottom',[x,y,-.04],[0,0,1])]:
   r=scene_cast(start,d,.1);opaque.append({'region':name,'origin_m':start,'pass':r['hit'] and ('Top_lid' in r['object'] if name=='top' else 'INFERRED_Bottom' in r['object']),**r})
for sign in [-1,1]:
 for y in [-.12,0,.12]:
  r=scene_cast([sign*.25,y,.021],[ -sign,0,0],.08);opaque.append({'region':'side','pass':r['hit'] and 'sidewall' in r['object'],**r})
ports=[]
for col in range(18):
 for row,z in enumerate([.0328,.014]):
  x=(-189+22.5*col)/1000;r=scene_cast([x,-.296,z],[0,1,0],.06);depth=(r['point'][1]+.295)*1000 if r['hit'] else None
  ports.append({'port':col*2+row+1,'first_hit_depth_from_face_mm':depth,'pass':r['hit'] and depth>20 and depth<40,**r})
report={'scene':sc.name,'source_glb_sha256':sc.get('source_glb_sha256'),'source_file':bpy.data.filepath,'isolated_ear_rays':rows,'assembled_ear_rays':assembly,'opaque_shell_rays':opaque,'business_port_depth_rays':ports,'pass':all(r['pass'] for r in rows+assembly+opaque+ports)}
(ROOT/'qa'/f'{prefix}-ray-tests.json').write_text(json.dumps(report,indent=2));print('RAY_QA',report['pass']);print(json.dumps([r for r in rows+assembly+opaque+ports if not r['pass']],indent=2))
# Independent saved fixture constructed through the GUI MCP.
qa=bpy.data.scenes.new('EAR_ISOLATION_QA');qa.render.engine='CYCLES';qa.cycles.samples=32;qa.cycles.use_denoising=False;qa.cycles.use_preview_denoising=False;qa.world=sc.world
for ear in ears:
 q=ear.copy();q.data=ear.data.copy();q.name='QA_'+ear.name;q.parent=None;q.matrix_world=ear.matrix_world.copy();qa.collection.objects.link(q)
for light in [o for o in sc.objects if o.type=='LIGHT']:
 q=light.copy();q.data=light.data.copy();qa.collection.objects.link(q)
cam=sc.camera.copy();cam.data=cam.data.copy();qa.collection.objects.link(cam);qa.camera=cam
# Checker plane behind the ears; actual high-contrast opaque background fixture.
me=bpy.data.meshes.new('QA_checker_mesh');me.from_pydata([(-1,0,-1),(1,0,-1),(1,0,1),(-1,0,1)],[],[(0,1,2,3)]);me.update();bg=bpy.data.objects.new('QA_CHECKER_BACKGROUND',me);qa.collection.objects.link(bg);bg.location=(0,-.27,.022)
m=bpy.data.materials.new('QA checker cyan magenta');m.use_nodes=True;n=m.node_tree.nodes;t=n.new('ShaderNodeTexChecker');t.inputs['Color1'].default_value=(.03,.75,.85,1);t.inputs['Color2'].default_value=(.85,.02,.23,1);t.inputs['Scale'].default_value=30;m.node_tree.links.new(t.outputs['Color'],n['Principled BSDF'].inputs['Base Color']);bg.data.materials.append(m)
qa.render.resolution_x=1600;qa.render.resolution_y=400;qa.render.image_settings.file_format='PNG';qa.render.image_settings.color_mode='RGBA';qa.render.film_transparent=True
bpy.context.window.scene=qa;bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'qa'/f'{prefix}-ear-fixture.blend'),copy=True,compress=True);bpy.context.window.scene=sc
for o in list(qa.objects):bpy.data.objects.remove(o,do_unlink=True)
bpy.data.scenes.remove(qa)
print(prefix.upper()+'_EAR_FIXTURE_SAVED; assembly restored')
