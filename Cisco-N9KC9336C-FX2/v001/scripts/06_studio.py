from pathlib import Path
import sys,importlib,bpy,math,json
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));import model_lib as L;importlib.reload(L)
from model_lib import *
sc=bpy.context.scene;C='90_STUDIO'
assert not bpy.data.collections.get(C)
for name,loc,energy,size in [('KEY',(.3,-.55,1.0),100,1.1),('FILL',(-.65,-.05,.55),65,.9),('RIM',(.1,.8,.8),100,.8)]:
 d=bpy.data.lights.new(name,'AREA');d.energy=energy;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);coll(C).objects.link(o);o.location=loc;o.rotation_euler=(Vector((0,0,.02))-o.location).to_track_quat('-Z','Y').to_euler()
mat('Studio backdrop',(.72,.72,.72),0,.85);floor=box('Studio_shadow_floor',(3000,3000,5),(0,0,-8),C,'Studio backdrop');floor['qa_or_studio']=True
camd=bpy.data.cameras.new('Review_camera');cam=bpy.data.objects.new('Review_camera',camd);coll(C).objects.link(cam);sc.camera=cam;camd.type='ORTHO';camd.clip_start=.001;camd.clip_end=50
cam.location=(.9,-1.2,.8);cam.rotation_euler=(Vector((0,0,.022))-cam.location).to_track_quat('-Z','Y').to_euler();camd.ortho_scale=.94
sc.render.engine='CYCLES';sc.cycles.device='CPU';sc.cycles.samples=48;sc.cycles.use_adaptive_sampling=True;sc.cycles.adaptive_threshold=.06;sc.cycles.use_denoising=False;sc.cycles.use_preview_denoising=False;sc.cycles.max_bounces=5
sc.render.resolution_x=1800;sc.render.resolution_y=1200;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=False
sc.view_settings.view_transform='AgX';sc.view_settings.look='AgX - Medium High Contrast';sc.view_settings.exposure=0
sc.world.node_tree.nodes['Background'].inputs[0].default_value=(.65,.65,.65,1);sc.world.node_tree.nodes['Background'].inputs[1].default_value=.45
sc['lighting_recipe']='Neutral world0.45 + key100W1.1m/fill65W0.9m/rim100W0.8m; AgX medium high contrast; no emission'
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':a.spaces.active.shading.type='SOLID';a.spaces.active.clip_start=.0005;a.spaces.active.clip_end=20
stage_save('06-first-complete-studio-review.blend')
