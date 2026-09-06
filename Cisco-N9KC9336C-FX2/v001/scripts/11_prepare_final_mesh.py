from pathlib import Path
import sys,importlib,bpy,bmesh,json,math
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));import model_lib as L;importlib.reload(L)
from model_lib import *
s=bpy.context.scene;source=coll('98_EDITABLE_TEXT_SOURCES');source.hide_render=True;source.hide_viewport=True
conversion=[]
for o in list(s.objects):
 if o.type!='FONT':continue
 backup=o.copy();backup.data=o.data.copy();backup.name='SOURCE_TEXT_'+o.name;backup.parent=None;source.objects.link(backup)
 bpy.ops.object.select_all(action='DESELECT');o.select_set(True);bpy.context.view_layer.objects.active=o;bpy.ops.object.convert(target='MESH');o=bpy.context.object;o['surface_role']='intentional_print_surface';conversion.append(o.name)
seen=set();clean=[]
for o in s.objects:
 if o.type!='MESH' or o.data in seen or any(c.name.startswith(('90_','98_')) for c in o.users_collection):continue
 seen.add(o.data);bm=bmesh.new();bm.from_mesh(o.data);v0=len(bm.verts);f0=len(bm.faces)
 bmesh.ops.remove_doubles(bm,verts=list(bm.verts),dist=1e-8);bmesh.ops.dissolve_degenerate(bm,edges=list(bm.edges),dist=1e-9);bmesh.ops.triangulate(bm,faces=list(bm.faces),quad_method='BEAUTY',ngon_method='BEAUTY')
 # Preserve text face direction; solids already have positive checked normals.
 if o.get('surface_role')!='intentional_print_surface':bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces))
 bm.to_mesh(o.data);bm.free();o.data.update();clean.append({'mesh':o.data.name,'vertices_before':v0,'faces_before':f0,'faces_after':len(o.data.polygons)})
for a in bpy.context.screen.areas:
 if a.type=='VIEW_3D':
  v=a.spaces.active;v.clip_start=.01;v.clip_end=10;v.overlay.show_extras=False;v.overlay.show_floor=False;v.shading.type='SOLID';v.region_3d.view_location=(0,0,.022);v.region_3d.view_distance=.80;v.region_3d.view_rotation=s.camera.rotation_euler.to_quaternion()
s.camera.data.clip_start=.005;s.camera.data.clip_end=10
s.eevee.use_gtao=True;s.eevee.gtao_distance=.04;s.eevee.gtao_factor=1.05;s.eevee.use_soft_shadows=True;s.eevee.taa_samples=32;s.eevee.taa_render_samples=128
floor=bpy.data.objects['Studio_shadow_floor'];floor.location.z=-.003;floor.hide_set(True)
s.cycles.samples=192;s.cycles.adaptive_threshold=.015;s['delivery_notes']='Exact PID/36 business ports/3 dual-rotor trays/2 matched AC PSUs. Bottom and unmeasured fine details inferred; see EVIDENCE.md. All metal opaque, real through-bores. Editable text backups in excluded collection98.'
for im in bpy.data.images:
 if im.filepath and im.type!='RENDER_RESULT':
  try:im.filepath=bpy.path.relpath(im.filepath,start=str(ROOT/'model'));im.pack()
  except Exception:pass
(ROOT/'qa/mesh-finalization.json').write_text(json.dumps({'text_meshes_converted':conversion,'editable_sources_collection':'98_EDITABLE_TEXT_SOURCES (not rendered/exported)','mesh_cleanup':clean,'viewport_clip_m':[.01,10]},indent=2))
bpy.ops.object.select_all(action='DESELECT')
stage_save('CISCO-Nexus-N9K-C9336C-FX2.blend')
