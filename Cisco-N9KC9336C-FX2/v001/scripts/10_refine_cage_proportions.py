from pathlib import Path
import sys,importlib,bpy,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));import model_lib as L;importlib.reload(L)
from model_lib import *
# The real NWR macro's paired cage H:W is about1.25, vs1.50 in first pass.
# Generic manufacturer stacked-cage literature is contextual, not claimed Cisco OEM identity.
seen=set()
for o in bpy.data.collections['03_QSFP28'].objects:
 if o.type!='MESH':continue
 if o.data not in seen:
  seen.add(o.data)
  for v in o.data.vertices:v.co.z*=.85
  o.data.update()
 o.location.z=.0234+(o.location.z-.0234)*.85
# Rebuild continuous face using the already executed, source-controlled block from stage09.
source=(ROOT/'scripts/09_refine_front_and_latches.py').read_text()
start=source.index("for name in ['Port_face_solid_punched_panel'")
end=source.index('# Font sizes')
block=source[start:end].replace("bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)","\n if bpy.data.objects.get(name):bpy.data.objects.remove(bpy.data.objects[name],do_unlink=True)").replace('20.98,31.38','20.98,26.70')
C='01_CHASSIS';root=bpy.data.objects['N9K-C9336C-FX2'];H=P['height'];W=P['width'];exec(block)
# Restore exact-scale UVs after changes, including the rebuilt face.
seen=set()
for o in [front]+list(bpy.data.collections['03_QSFP28'].objects):
 if o.type!='MESH' or o.data in seen:continue
 seen.add(o.data)
 if not any(m and any(n.type=='UVMAP' and n.uv_map=='Physical80mm' for n in m.node_tree.nodes) for m in o.data.materials):continue
 uv=o.data.uv_layers.get('Physical80mm') or o.data.uv_layers.new(name='Physical80mm')
 for po in o.data.polygons:
  ax=max(range(3),key=lambda i:abs(po.normal[i]));ij=[1,2] if ax==0 else [0,2] if ax==1 else [0,1]
  for li in po.loop_indices:
   co=o.data.vertices[o.data.loops[li].vertex_index].co;uv.data[li].uv=(co[ij[0]]/.08,co[ij[1]]/.08)
p=json.loads((ROOT/'parameters.json').read_text());p['cage_height_estimate']=26.52;p['cage_width_estimate']=20.8;p['cage_aspect_evidence']='NWR real macro ratio; generic stacked QSFP literature contextual only';(ROOT/'parameters.json').write_text(json.dumps(p,indent=2))
(ROOT/'qa/cage-proportion-correction.json').write_text(json.dumps({'first_pass_outer_mm':[20.8,31.2],'revised_outer_mm':[20.8,26.52],'ratio_before':1.5,'ratio_after':1.275,'all_36_port_geometry_scaled_consistently':True,'not_a_manufacturing_dimension':True},indent=2))
stage_save('10-photo-matched-cage-aspect.blend')
