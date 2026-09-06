import bpy,json
from pathlib import Path
p=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');sc=bpy.context.scene
used={n.image for o in sc.objects if o.type=='MESH' for m in o.data.materials if m and m.use_nodes for n in m.node_tree.nodes if n.type=='TEX_IMAGE' and n.image}
r={'filepath':bpy.data.filepath,'scene':sc.name,'scene_count':len(bpy.data.scenes),'mesh_objects':sum(o.type=='MESH' for o in sc.objects),'component_counts':{k:sum(o.get('component_type')==k for o in sc.objects) for k in ['2.5-inch hot-swap carrier','C6420 node','2400W PSU']},'used_texture_count':len(used),'all_used_textures_packed':all(i.packed_file for i in used),'denoise':sc.cycles.use_denoising,'preview_denoise':sc.cycles.use_preview_denoising,'frame':sc.frame_current,'text_blocks':len(bpy.data.texts),'delivery_notes':sc.get('delivery_notes'),'viewport_modes':[a.spaces.active.shading.type for a in bpy.context.screen.areas if a.type=='VIEW_3D']}
assert r['scene_count']==1 and r['mesh_objects']==2020 and r['all_used_textures_packed'] and not r['denoise'] and not r['preview_denoise']
(p/'qa/final-master-open-check.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))
