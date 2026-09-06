import bpy,math
from mathutils import Vector
from pathlib import Path
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');sc=bpy.context.scene
co=bpy.data.collections.get('90_STUDIO')
if not co:co=bpy.data.collections.new('90_STUDIO');sc.collection.children.link(co)
for ob in list(co.objects):bpy.data.objects.remove(ob,do_unlink=True)
world=bpy.data.worlds.new('Neutral_photographic_studio_v002');world.use_nodes=True;sc.world=world
nt=world.node_tree;bg=nt.nodes.get('Background');bg.inputs['Strength'].default_value=.65
tex=nt.nodes.new('ShaderNodeTexEnvironment');tex.image=bpy.data.images.load('/usr/share/blender/datafiles/studiolights/world/studio.exr',check_existing=True);tex.image.pack()
nt.links.new(tex.outputs['Color'],bg.inputs['Color'])
for name,pos,power,sx,sy in [('Overhead_softbox',(-.25,-.3,1.15),40,1.1,.6),('Front_fill',(0,-1.05,.35),22,.85,.45),('Left_strip',(-.75,.06,.4),25,.17,.9),('Rear_rim',(.2,.95,.65),38,.85,.35)]:
 ld=bpy.data.lights.new(name,'AREA');ld.shape='RECTANGLE';ld.energy=power;ld.size=sx;ld.size_y=sy
 ob=bpy.data.objects.new(name,ld);co.objects.link(ob);ob.location=pos;ob.rotation_euler=(Vector((0,0,.04))-ob.location).to_track_quat('-Z','Y').to_euler()
cd=bpy.data.cameras.new('Photo_inspection_camera');cam=bpy.data.objects.new('Photo_inspection_camera',cd);co.objects.link(cam);sc.camera=cam;cd.type='ORTHO';cd.ortho_scale=.97;cd.lens=85;cd.clip_start=.001;cd.clip_end=20
cam.location=(.85,-1.55,.50);cam.rotation_euler=(Vector((0,0,.04))-cam.location).to_track_quat('-Z','Y').to_euler()
sc.render.resolution_x=1800;sc.render.resolution_y=1050;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True
sc.render.engine='CYCLES';sc.cycles.samples=128;sc.cycles.use_denoising=False;sc.cycles.use_preview_denoising=False;sc.render.threads_mode='FIXED';sc.render.threads=10
# Flat photographic background is composited only; real metal is lit/reflected by neutral HDR and area lights.
sc.use_nodes=True;nt=sc.node_tree;nt.nodes.clear();rl=nt.nodes.new('CompositorNodeRLayers');over=nt.nodes.new('CompositorNodeAlphaOver');over.inputs[1].default_value=(.92,.92,.92,1);nt.links.new(rl.outputs['Image'],over.inputs[2]);out=nt.nodes.new('CompositorNodeComposite');nt.links.new(over.outputs[0],out.inputs[0])
for screen in bpy.data.screens:
 for a in screen.areas:
  if a.type=='VIEW_3D':a.spaces.active.shading.studio_light='studio.exr';a.spaces.active.shading.studiolight_rotate_z=.35;a.spaces.active.shading.studiolight_intensity=.9
bpy.ops.wm.save_as_mainfile(filepath=str(P/'model/03-front-material-test.blend'))
print('Photographic studio and review checkpoint saved')
