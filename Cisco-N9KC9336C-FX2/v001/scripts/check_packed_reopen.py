from pathlib import Path
import bpy,json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];s=bpy.context.scene;assert s.name=='CISCO_N9K_C9336C_FX2_V001';v=next(a.spaces.active for a in bpy.context.screen.areas if a.type=='VIEW_3D');saved=json.loads((ROOT/'qa/final-saved-view.json').read_text());fail=[];images={};fonts=[];uvs=0
for o in s.objects:
 if o.type=='FONT' and o.data.font.filepath!='<builtin>':
  fonts.append({'object':o.name,'font':o.data.font.name,'packed':bool(o.data.font.packed_file)})
  if not o.data.font.packed_file:fail.append([o.name,'font not packed'])
 if o.type!='MESH' or any(c.name.startswith('90_') for c in o.users_collection):continue
 for m in o.data.materials:
  if not m or not m.use_nodes:continue
  for n in m.node_tree.nodes:
   if n.type in ['UVMAP','NORMAL_MAP'] and n.uv_map:
    uvs+=1
    if n.uv_map not in o.data.uv_layers:fail.append([o.name,'missing UV',n.uv_map])
   if n.type=='TEX_IMAGE' and n.image:
    im=n.image;images[im.name]={'packed':bool(im.packed_file),'relative_path':im.filepath,'size':list(im.size),'colorspace':im.colorspace_settings.name}
    if not im.packed_file or not all(im.size):fail.append([im.name,'unpacked or empty'])
q=list(v.region_3d.view_rotation);sq=saved['q'];norm=math.sqrt(sum(x*x for x in q)*sum(x*x for x in sq));angle=math.degrees(2*math.acos(min(1,abs(sum(a*b for a,b in zip(q,sq))/norm))))
if angle>.001 or abs(v.region_3d.view_distance-saved['distance'])>1e-6 or v.shading.type!='MATERIAL' or not v.shading.use_scene_world or not v.shading.use_scene_lights or bpy.context.screen.is_animation_playing:fail.append(['saved default viewport mismatch'])
rep={'pass':not fail,'master_file':'model/CISCO-Nexus-N9K-C9336C-FX2.blend','master_sha256':hashlib.sha256(Path(bpy.data.filepath).read_bytes()).hexdigest(),'scene':s.name,'scene_count':len(bpy.data.scenes),'images':images,'packed_font_objects':len(fonts),'font_resources':fonts,'uv_bindings_checked_after_reopen':uvs,'default_pose_delta_degrees':angle,'mode':v.shading.type,'scene_world':v.shading.use_scene_world,'scene_lights':v.shading.use_scene_lights,'clip_m':[v.clip_start,v.clip_end],'animation_playing':bpy.context.screen.is_animation_playing,'failures':fail};(ROOT/'qa/packed-reopen.json').write_text(json.dumps(rep,indent=2));print('PACKED_REOPEN',rep['pass'],len(images),len(fonts),uvs,fail)
