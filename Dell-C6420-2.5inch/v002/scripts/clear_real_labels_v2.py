"""Project original, unmirrored Abacus rear-elevated C6400/C6420 photograph onto actual printed regions.
Only flat label pixels are baked; chassis geometry and NIC/PSU configuration remain the locked NSL/ETB set.
"""
import bpy,numpy as np,json
from pathlib import Path
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');sc=bpy.context.scene
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':a.spaces.active.shading.type='SOLID'
source=bpy.data.images.load(str(P/'sources/third_party/abacus-3.webp'),check_existing=True);source.pack()
regions=[('Real_service_label_band','service',[(1098,477),(514,467),(449,584),(1165,598)]),('Real_yellow_warning_label','warning',[(665,651),(491,647),(451,776),(638,780)]),('Real_regulatory_label','regulatory',[(1149,694),(988,691),(1003,765),(1179,768)])]
report=[]
for name,kind,quad in regions:
 ob=bpy.data.objects[name];ob.data=ob.data.copy();me=ob.data
 vs=[ob.matrix_world@v.co for v in me.vertices];xmin=min(v.x for v in vs);xmax=max(v.x for v in vs);ymin=min(v.y for v in vs);ymax=max(v.y for v in vs)
 A=[];b=[]
 for (x,y),(u,v) in zip([(0,0),(1,0),(1,1),(0,1)],quad):
  A.extend([[x,y,1,0,0,0,-u*x,-u*y],[0,0,0,x,y,1,-v*x,-v*y]]);b.extend([u,v])
 h=np.append(np.linalg.solve(np.array(A),np.array(b)),1).reshape(3,3)
 inp=me.uv_layers.new(name='Abacus_original_projective_UV');outuv=me.uv_layers.new(name='Clear_label_export_UV')
 for li,loop in enumerate(me.loops):
  p=vs[loop.vertex_index];xy=np.array([(p.x-xmin)/(xmax-xmin),(p.y-ymin)/(ymax-ymin),1]);q=h@xy;q/=q[2]
  inp.data[li].uv=(q[0]/1600,1-q[1]/1282);outuv.data[li].uv=xy[:2]
 me.uv_layers.active=outuv;outuv.active_render=True
 m=bpy.data.materials.new('Clear_original_'+kind);m.use_nodes=True;m.blend_method='OPAQUE';m.use_backface_culling=True;nt=m.node_tree;nt.nodes.clear()
 uv=nt.nodes.new('ShaderNodeUVMap');uv.uv_map=inp.name;tx=nt.nodes.new('ShaderNodeTexImage');tx.image=source;nt.links.new(uv.outputs[0],tx.inputs['Vector'])
 em=nt.nodes.new('ShaderNodeEmission');nt.links.new(tx.outputs['Color'],em.inputs[0]);out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(em.outputs[0],out.inputs['Surface']);me.materials.clear();me.materials.append(m)
 w,hsize=(2048,1024) if kind=='service' else (640,640);im=bpy.data.images.new('abacus-clear-'+kind,width=w,height=hsize,alpha=False)
 target=nt.nodes.new('ShaderNodeTexImage');target.image=im;nt.nodes.active=target
 bpy.ops.object.select_all(action='DESELECT');ob.select_set(True);bpy.context.view_layer.objects.active=ob;sc.cycles.samples=1;sc.render.bake.margin=4;sc.render.bake.use_clear=True
 bpy.ops.object.bake(type='EMIT');im.filepath_raw=str(P/'textures'/('abacus-clear-'+kind+'.png'));im.file_format='PNG';im.save();im.pack()
 nt.nodes.clear();uv=nt.nodes.new('ShaderNodeUVMap');uv.uv_map=outuv.name;tx=nt.nodes.new('ShaderNodeTexImage');tx.image=im;nt.links.new(uv.outputs[0],tx.inputs['Vector']);bs=nt.nodes.new('ShaderNodeBsdfPrincipled');bs.inputs['Roughness'].default_value=.73;bs.inputs['Specular IOR Level'].default_value=.2;bs.inputs['Alpha'].default_value=1;bs.inputs['Transmission Weight'].default_value=0;nt.links.new(tx.outputs['Color'],bs.inputs['Base Color']);out=nt.nodes.new('ShaderNodeOutputMaterial');nt.links.new(bs.outputs[0],out.inputs['Surface'])
 ob['source_asset']='sources/third_party/abacus-3.webp; unmodified original photo, projective label-only Blender EMIT bake';ob['source_page']='https://www.ebay.com/itm/126737099835';ob['legibility_limit']='Photographed small print retains original source resolution; no invented or AI lettering';ob['image_uv_verified']=True
 m['source_photo']=ob['source_asset'];m['orientation']='Rear photo projection reverses both world X and Y: 180-degree rotation, never a horizontal mirror'
 report.append({'object':name,'original_photo_quad_world_00_10_11_01':quad,'bounds_world_m':[xmin,xmax,ymin,ymax],'projective_matrix':h.tolist(),'baked_asset':im.filepath_raw,'photo_crop_px_height_approx':130 if kind=='service' else 130 if kind=='warning' else 74})
 # Export exactly one UV layer; original projective coordinates are recorded above.
 for layer in list(me.uv_layers):
  if layer!=outuv:me.uv_layers.remove(layer)
 sc.cycles.samples=128
bpy.ops.object.select_all(action='DESELECT');sc.cycles.use_denoising=False;sc.cycles.use_preview_denoising=False
(P/'qa/clear-label-projection.json').write_text(json.dumps({'source_page':'https://www.ebay.com/itm/126737099835','original_photo':'https://i.ebayimg.com/images/g/n~kAAOSw8-NnF9Yr/s-l1600.webp','note':'Supplemental clear label photo only. Different NIC option is excluded. Printed tiny text has finite photographic resolution.','regions':report},indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(P/'model/11-clear-original-labels.blend'))
print('CLEAR_REAL_LABELS_DONE',flush=True)
