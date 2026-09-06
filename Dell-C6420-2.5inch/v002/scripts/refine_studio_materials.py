import bpy
from pathlib import Path
from mathutils import Vector
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');sc=bpy.context.scene
for name,strength in [('Zinc',.075),('Nickel',.06),('ABS',.32),('Nylon',.65)]:
 m=bpy.data.materials.get(name)
 if m:
  for n in m.node_tree.nodes:
   if n.type=='NORMAL_MAP':n.inputs['Strength'].default_value=strength
nt=sc.world.node_tree;bg=nt.nodes.get('Background')
for l in list(nt.links):
 if l.to_node==bg:nt.links.remove(l)
bg.inputs[0].default_value=(.78,.8,.82,1);bg.inputs[1].default_value=.7
for ob in bpy.data.collections['90_STUDIO'].objects:
 if ob.type=='LIGHT':ob.data.energy*=.65
ld=bpy.data.lights.new('Right_photographic_fill','AREA');ld.shape='RECTANGLE';ld.energy=32;ld.size=1.0;ld.size_y=.7
ob=bpy.data.objects.new('Right_photographic_fill',ld);bpy.data.collections['90_STUDIO'].objects.link(ob);ob.location=(.95,0,.45);ob.rotation_euler=(Vector((0,0,.04))-ob.location).to_track_quat('-Z','Y').to_euler()
sc.view_settings.look='None'
for n in sc.node_tree.nodes:
 if n.type=='ALPHAOVER':n.inputs[1].default_value=(16,16,16,1)
sc.cycles.samples=192
bpy.ops.wm.save_as_mainfile(filepath=str(P/'model/03b-front-material-corrected.blend'))
print('Reduced excessive surface amplitude; neutral environment; added side fill')
