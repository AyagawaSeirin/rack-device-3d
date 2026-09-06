from pathlib import Path
import bpy,json
ROOT=Path(__file__).resolve().parents[1]
o=bpy.data.objects['Original_photo_top_chassis_label'];m=o.data.materials[0];nt=m.node_tree;nodes=nt.nodes;links=nt.links
quad=[(820,1928),(1580,1933),(1747,1398),(1153,1398)]
for i,(x,y) in enumerate(quad):o.data.uv_layers['SourcePhotoUV'].data[i].uv=(x/4608,1-y/3456)
o['source_pixel_quad']=[v for co in quad for v in co]
baked=bpy.data.images['NWR_original_chassis_label_baked'];source=bpy.data.images.get('nwr-2.jpg') or bpy.data.images.load(str(ROOT/'sources/third_party/nwr-2.jpg'))
out=next(n for n in nodes if n.type=='OUTPUT_MATERIAL');bs=next(n for n in nodes if n.type=='BSDF_PRINCIPLED');em=nodes.new('ShaderNodeEmission');tx=nodes.new('ShaderNodeTexImage');tx.image=source;uv=nodes.new('ShaderNodeUVMap');uv.uv_map='SourcePhotoUV';links.new(uv.outputs[0],tx.inputs[0]);links.new(tx.outputs['Color'],em.inputs[0]);links.new(em.outputs[0],out.inputs[0]);target=nodes.new('ShaderNodeTexImage');target.image=baked;nodes.active=target
o.data.uv_layers.active_index=o.data.uv_layers.find('LabelBakeUV');o.data.uv_layers['LabelBakeUV'].active_render=True
bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o
bpy.context.scene.cycles.samples=1;bpy.ops.object.bake(type='EMIT',margin=4,use_clear=True)
baked.filepath_raw=str(ROOT/'textures/original-chassis-label-512x768.png');baked.save();baked.pack()
for n in [em,tx,uv,target]:nodes.remove(n)
links.new(bs.outputs[0],out.inputs[0]);bpy.context.scene.cycles.samples=48
r=json.loads((ROOT/'qa/label-bake.json').read_text());r['quad_pixels']=list(o['source_pixel_quad']);r['correction']='Corrected corners from wider original-photo inspection; removed extra top body strip and edge clipping';(ROOT/'qa/label-bake.json').write_text(json.dumps(r,indent=2))
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'model/07-label-projection-corrected.blend'),compress=True)
print('CORRECTED_PHOTO_LABEL_SAVED')
