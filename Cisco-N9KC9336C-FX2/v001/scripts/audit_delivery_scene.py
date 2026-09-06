from pathlib import Path
import bpy,bmesh,json,math,hashlib
from mathutils import Vector
ROOT=Path(__file__).resolve().parents[1];s=bpy.context.scene;prefix='glb' if s.name.startswith('GLB_REIMPORT') else 'original'
objects=[o for o in s.objects if o.type=='MESH' and not any(c.name.startswith(('90_','98_')) for c in o.users_collection)]
fail=[];meshes=[];materials={};images={};checked=set();uvchecks=0
for o in objects:
 me=o.data
 if o.matrix_world.to_3x3().determinant()<=0:fail.append([o.name,'world negative determinant'])
 for m in me.materials:
  if not m or not m.use_nodes:continue
  for n in m.node_tree.nodes:
   if n.type in ['UVMAP','NORMAL_MAP'] and n.uv_map:
    uvchecks+=1
    if n.uv_map not in me.uv_layers:fail.append([o.name,'missing UV',n.uv_map])
   if n.type=='TEX_IMAGE' and n.image:
    im=n.image;images[im.name]={'size':list(im.size),'colorspace':im.colorspace_settings.name,'packed':bool(im.packed_file),'filepath':im.filepath}
    if not im.packed_file:fail.append([im.name,'not packed'])
  bs=next((n for n in m.node_tree.nodes if n.type=='BSDF_PRINCIPLED'),None)
  if bs:
   a=bs.inputs['Alpha'];tr=bs.inputs['Transmission Weight'];e=bs.inputs['Emission Color'];es=bs.inputs['Emission Strength'];r={'alpha':a.default_value,'alpha_linked':a.is_linked,'transmission':tr.default_value,'transmission_linked':tr.is_linked,'blend_method':m.blend_method,'backface_culling':m.use_backface_culling,'emission_strength':es.default_value,'emission_rgb':list(e.default_value[:3])};materials[m.name]=r
   if a.default_value!=1 or a.is_linked or tr.default_value!=0 or tr.is_linked or m.blend_method!='OPAQUE' or not m.use_backface_culling or (es.default_value>0 and max(e.default_value[:3])>0):fail.append([m.name,'material opaque/emission contract',r])
 if me.name in checked:continue
 checked.add(me.name);me.calc_normals_split()
 dots=[]
 for f in me.polygons:
  if f.area>2e-6 and 'silver_U_pull_handle' not in o.name:dots.extend(f.normal.dot(me.loops[i].normal) for i in f.loop_indices)
 if dots and min(dots)<.9999:fail.append([o.name,'large-plane split-normal deviation',min(dots)])
 for uv in me.uv_layers:
  if any(not math.isfinite(x) for d in uv.data for x in d.uv):fail.append([o.name,'nonfinite UV'])
 bm=bmesh.new();bm.from_mesh(me);raw_boundary=sum(not e.is_manifold for e in bm.edges);rawverts=len(bm.verts)
 if prefix=='glb':bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-7)
 boundary=sum(not e.is_manifold for e in bm.edges);zero=sum(f.calc_area()<1e-16 for f in bm.faces);volume=bm.calc_volume(signed=True);allowed=o.get('surface_role')=='intentional_print_surface'
 # Duplicate coordinate-identical faces are prohibited, including in open print surfaces.
 faces=[tuple(sorted(tuple(round(c,9) for c in v.co) for v in f.verts)) for f in bm.faces];duplicates=len(faces)-len(set(faces))
 if zero or duplicates or (not allowed and (boundary or volume<=0)):fail.append([o.name,'topology',boundary,zero,duplicates,volume,allowed])
 meshes.append({'mesh':me.name,'example':o.name,'raw_vertices':rawverts,'diagnostic_vertices':len(bm.verts),'raw_nonmanifold_edges':raw_boundary,'diagnostic_nonmanifold_edges':boundary,'zero_area_faces':zero,'duplicate_faces':duplicates,'volume_m3':volume,'intentional_print':allowed,'large_plane_min_normal_dot':min(dots) if dots else None});bm.free()
def bounds(obs):
 pts=[o.matrix_world@Vector(v) for o in obs for v in o.bound_box];lo=[min(p[i] for p in pts)*1000 for i in range(3)];hi=[max(p[i] for p in pts)*1000 for i in range(3)];return {'min_mm':lo,'max_mm':hi,'size_mm':[hi[i]-lo[i] for i in range(3)]}
core=bounds([o for o in objects if o.name.split('.')[0] in ['Top_lid_main_sheet','INFERRED_Bottom_folded_sheet','LEFT_sidewall_with_mounting_provisions','RIGHT_sidewall_with_mounting_provisions','Port_face_solid_punched_panel']]);whole=bounds(objects);noears=bounds([o for o in objects if o.get('component_type')!='rack_ear' and '_ear_M4_' not in o.name]);
for actual,want in zip(core['size_mm'],[439.42,590,43.688]):
 if abs(actual-want)>.01:fail.append(['core dimension',actual,want])
for actual,want in zip(whole['size_mm'][:2],[482.6,622.3]):
 if abs(actual-want)>.01:fail.append(['assembly dimension',actual,want])
label=next(o for o in objects if o.name.startswith('Original_photo_top_chassis_label'));lid=next(o for o in objects if o.name.startswith('Top_lid_main_sheet'));gap=bounds([label])['min_mm'][2]-bounds([lid])['max_mm'][2]
if not .015<gap<.035:fail.append(['label measured gap',gap])
# Text front local +X maps world +X; rear local +X maps world -X. Label UV sign measured on world XY triangles.
orient=[]
for name,expected in [('Correct_factory_PID',Vector((1,0,0))),('PORT_NUMBER_01',Vector((1,0,0))),('REAR_STS_legend',Vector((-1,0,0)))]:
 o=next(o for o in objects if o.name.split('.')[0]==name);r=(o.matrix_world.to_3x3()@Vector((1,0,0))).normalized();ok=r.dot(expected)>.999;orient.append({'object':o.name,'world_reading_axis':list(r),'expected_axis':list(expected),'pass':ok})
 if not ok:fail.append([name,'text reading axis'])
uv=label.data.uv_layers.active;uv_orient=[]
for f in label.data.polygons:
 ls=list(f.loop_indices)[:3];ps=[label.matrix_world@label.data.vertices[label.data.loops[i].vertex_index].co for i in ls];us=[uv.data[i].uv for i in ls];area=(ps[1]-ps[0]).cross(ps[2]-ps[0]).z;ua=(us[1].x-us[0].x)*(us[2].y-us[0].y)-(us[1].y-us[0].y)*(us[2].x-us[0].x);uv_orient.append(area*ua>0)
if not all(uv_orient):fail.append(['label UV reflection'])
report={'pass':not fail,'scene':s.name,'source_blend':bpy.data.filepath,'glb_sha256':hashlib.sha256((ROOT/'model/CISCO-Nexus-N9K-C9336C-FX2.glb').read_bytes()).hexdigest() if prefix=='glb' else None,'diagnostic_weld_tolerance_m':1e-7 if prefix=='glb' else None,'meshes':meshes,'materials':materials,'images':images,'uv_node_bindings_checked':uvchecks,'bounds':{'core_shell':core,'with_handles_without_ears':noears,'complete_with_ears':whole},'measured_label_gap_mm':gap,'text_direction':orient,'label_uv_positive_orientation':uv_orient,'large_plane_area_threshold_m2':2e-6,'normal_test_exclusions':['PSU silver U pull handles are intentionally curved smooth tubes, not planar sheet'],'large_plane_normal_dot_threshold':.9999,'failures':fail}
(ROOT/'qa'/f'{prefix}-delivery-scene.json').write_text(json.dumps(report,indent=2));print('DELIVERY_SCENE',prefix,'PASS',not fail,'FAILURES',len(fail));print(json.dumps(fail[:30]));print(json.dumps(report['bounds']))
