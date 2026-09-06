from pathlib import Path
import sys,importlib,bpy,json,math,numpy as np
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
import model_lib as L;importlib.reload(L)
from model_lib import *
assert not bpy.data.objects.get('Original_photo_top_chassis_label')
C='07_FACTORY_MARKINGS';H=P['height']
label=mesh('Original_photo_top_chassis_label',[(-201,-242,H+.025),(-96,-242,H+.025),(-96,-92,H+.025),(-201,-92,H+.025)],[(0,1,2,3)],C,solid=False);label.parent=bpy.data.objects['FRONT_BRAND_AND_PORT_LEGENDS']
label['source']='sources/third_party/nwr-2.jpg';label['source_pixel_quad']=[829,1930,1582,1930,1742,1360,1132,1360];label['source_resolution_limitation']='Photo projection does not restore unreadable small print';label['print_gap_mm']=.025
uv=label.data.uv_layers.new(name='SourcePhotoUV')
quad=[(829,1930),(1582,1930),(1742,1360),(1132,1360)]
for i,(x,y) in enumerate(quad):uv.data[i].uv=(x/4608,1-y/3456)
uvb=label.data.uv_layers.new(name='LabelBakeUV')
for i,co in enumerate([(0,0),(1,0),(1,1),(0,1)]):uvb.data[i].uv=co
uvb.active_render=True;label.data.uv_layers.active_index=1
m=bpy.data.materials.new('Source photographic label — explicit two UV bake');m.use_nodes=True;label.data.materials.append(m);nodes=m.node_tree.nodes;nodes.clear();links=m.node_tree.links
out=nodes.new('ShaderNodeOutputMaterial');em=nodes.new('ShaderNodeEmission');links.new(em.outputs[0],out.inputs['Surface'])
im=bpy.data.images.load(str(ROOT/'sources/third_party/nwr-2.jpg'),check_existing=True);im.colorspace_settings.name='sRGB'
tex=nodes.new('ShaderNodeTexImage');tex.image=im;uvn=nodes.new('ShaderNodeUVMap');uvn.uv_map='SourcePhotoUV';links.new(uvn.outputs[0],tex.inputs[0]);links.new(tex.outputs['Color'],em.inputs['Color'])
baked=bpy.data.images.new('NWR_original_chassis_label_baked',width=512,height=768,alpha=False);baked.colorspace_settings.name='sRGB'
target=nodes.new('ShaderNodeTexImage');target.image=baked;nodes.active=target
bpy.ops.object.select_all(action='DESELECT');label.select_set(True);bpy.context.view_layer.objects.active=label
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=1;sc.cycles.use_denoising=False;sc.cycles.use_preview_denoising=False
bpy.ops.object.bake(type='EMIT',margin=4,use_clear=True)
baked.filepath_raw=str(ROOT/'textures/original-chassis-label-512x768.png');baked.file_format='PNG';baked.save();baked.pack()
nodes.clear();out=nodes.new('ShaderNodeOutputMaterial');bs=nodes.new('ShaderNodeBsdfPrincipled');links.new(bs.outputs[0],out.inputs['Surface']);bs.inputs['Metallic'].default_value=.2;bs.inputs['Roughness'].default_value=.48;bs.inputs['Alpha'].default_value=1
tex=nodes.new('ShaderNodeTexImage');tex.image=baked;uvn=nodes.new('ShaderNodeUVMap');uvn.uv_map='LabelBakeUV';links.new(uvn.outputs[0],tex.inputs[0]);links.new(tex.outputs['Color'],bs.inputs['Base Color']);m.blend_method='OPAQUE';m.use_backface_culling=True
# Standard portable material maps. Periodic microtexture, never imagegen printing.
N=512;rng=np.random.default_rng(9336);a=rng.normal(0,1,(N,N));sm=(a+np.roll(a,1,0)+np.roll(a,-1,0)+np.roll(a,1,1)+np.roll(a,-1,1))/5;sm=sm/np.std(sm)
def save_map(name,rgb,noncolor=True):
 image=bpy.data.images.new(name,width=N,height=N,alpha=False,float_buffer=False);image.colorspace_settings.name='Non-Color' if noncolor else 'sRGB';rgba=np.ones((N,N,4),np.float32);rgba[:,:,:3]=rgb;image.pixels.foreach_set(rgba.ravel());image.filepath_raw=str(ROOT/'textures'/f'{name}.png');image.file_format='PNG';image.save();image.pack();return image
dx=(np.roll(sm,-1,1)-np.roll(sm,1,1))*.008;dy=(np.roll(sm,-1,0)-np.roll(sm,1,0))*.008
v=np.stack([-dx,-dy,np.ones_like(dx)],2);v/=np.linalg.norm(v,axis=2)[:,:,None];normal=save_map('metal-micro-normal',v*.5+.5)
for name,rough in [('Chassis satin nickel',.36),('Zinc plated brackets',.30),('Cage stainless steel',.29),('Fastener steel',.27),('Dark grille metal',.40)]:
 material=bpy.data.materials[name];nt=material.node_tree;bs=nt.nodes.get('Principled BSDF')
 rm=save_map(name.lower().replace(' ','-')+'-roughness',np.repeat(np.clip(rough+sm*.014,.08,.85)[:,:,None],3,2))
 un=nt.nodes.new('ShaderNodeUVMap');un.uv_map='Physical80mm';rt=nt.nodes.new('ShaderNodeTexImage');rt.image=rm;nt.links.new(un.outputs[0],rt.inputs[0]);nt.links.new(rt.outputs['Color'],bs.inputs['Roughness'])
 nm=nt.nodes.new('ShaderNodeTexImage');nm.image=normal;nn=nt.nodes.new('ShaderNodeNormalMap');nn.uv_map='Physical80mm';nn.inputs['Strength'].default_value=.18;nt.links.new(un.outputs[0],nm.inputs[0]);nt.links.new(nm.outputs['Color'],nn.inputs['Color']);nt.links.new(nn.outputs['Normal'],bs.inputs['Normal'])
 material['microtexture_tile_mm']=80;material['normal_scale']=.18;material['alpha_contract']='OPAQUE, alpha1, no transmission'
seen=set()
for o in sc.objects:
 if o.type!='MESH' or o.data in seen:continue
 seen.add(o.data)
 if not any(m and m.name in ['Chassis satin nickel','Zinc plated brackets','Cage stainless steel','Fastener steel','Dark grille metal'] for m in o.data.materials):continue
 uv=o.data.uv_layers.get('Physical80mm') or o.data.uv_layers.new(name='Physical80mm')
 for poly in o.data.polygons:
  axis=max(range(3),key=lambda i:abs(poly.normal[i]));ij=([1,2] if axis==0 else [0,2] if axis==1 else [0,1])
  for li in poly.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[ij[0]]/.08,co[ij[1]]/.08)
for image in bpy.data.images:
 if image.source=='FILE' and image.filepath:
  try:image.filepath=bpy.path.relpath(image.filepath,start=str(ROOT/'model'));image.pack()
  except Exception:pass
sc.cycles.samples=48;sc.cycles.use_denoising=False;sc.cycles.use_preview_denoising=False
(ROOT/'qa/label-bake.json').write_text(json.dumps({'source':label['source'],'quad_pixels':list(label['source_pixel_quad']),'input_uv':'SourcePhotoUV','output_uv':'LabelBakeUV','output':'textures/original-chassis-label-512x768.png','baked_via_gui_mcp':True,'source_resolution_not_recovered':True,'gap_mm':.025},indent=2))
stage_save('05-original-photo-label-and-standard-PBR.blend')
