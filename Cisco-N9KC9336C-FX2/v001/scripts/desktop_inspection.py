from pathlib import Path
import subprocess,json,time,datetime,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];prefix=sys.argv[1];dest=ROOT/'desktop'/prefix;dest.mkdir(parents=True,exist_ok=True)
CLIENT=['/root/.local/share/uv/tools/blender-mcp/bin/python','/root/.local/share/blender-mcp-setup/mcp_call.py'];PROMPT=(ROOT/'REQUEST.md').read_text().split('\n\n')[1];events=[];frames=[]
def call(server,tool,args=None,image=None):
 cmd=CLIENT+[server,tool]
 if args is not None:cmd+=['--args',json.dumps(args,ensure_ascii=False)]
 if image:cmd+=['--image-out',str(image)]
 return subprocess.run(cmd,text=True,capture_output=True,check=True,timeout=205).stdout
def code(t):return call('blender','execute_blender_code',{'code':t,'user_prompt':PROMPT})
def key(k):
 r=call('server_desktop','desktop_key',{'key':k});events.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'key':k,'response':r.strip()});time.sleep(.8)
def pose():
 t="import bpy,json\nv=next(a.spaces.active for a in bpy.context.screen.areas if a.type=='VIEW_3D');r=v.region_3d\nprint(json.dumps({'q':list(r.view_rotation),'location':list(r.view_location),'distance':r.view_distance,'mode':v.shading.type,'scene_world':v.shading.use_scene_world,'scene_lights':v.shading.use_scene_lights,'scene':bpy.context.scene.name}))"
 s=code(t);return json.JSONDecoder().raw_decode(s[s.index('{'):])[0]
jobs=[('front',None,['KP_1']),('front-right',None,['KP_1','KP_6','KP_6','KP_8','KP_8']),('top',None,['KP_7']),('bottom-INFERRED',None,['ctrl+KP_7']),('left',None,['ctrl+KP_3']),('right',None,['KP_3']),('rear',None,['ctrl+KP_1']),('low-grazing',None,['KP_1','KP_2','KP_6']),('ear-front','LEFT_EAR_bent_opaque_solid_with_true_bores',['KP_1','KP_8','KP_6']),('ear-back','RIGHT_EAR_bent_opaque_solid_with_true_bores',['ctrl+KP_1','KP_8','KP_4','KP_4','KP_4']),('brand','Correct_factory_PID',['KP_1','KP_Subtract','KP_Subtract','KP_Subtract','KP_Subtract','KP_Subtract']),('rear-management','Rear_service_panel_true_apertures',['ctrl+KP_1','KP_6']),('return-overview',None,['KP_1','KP_6','KP_6','KP_8','KP_8'])]
if len(sys.argv)>2:
 profile=sys.argv[2]
 if profile=='final-solid':jobs=[j for j in jobs if j[0] in ['front-right','rear','low-grazing']]
 elif profile=='final-material':
  jobs=[j for j in jobs if j[0] in ['top','bottom-INFERRED','ear-front','ear-back','rear-management']]+[('PSU-handle','PSU2_silver_U_pull_handle',['ctrl+KP_1','KP_6','KP_6','KP_8']),('return-overview',None,['KP_1','KP_6','KP_6','KP_8','KP_8','KP_Add','KP_Add'])]
# Focus already confirmed by actual15degree desktop input and screenshot before invocation.
for name,selected,keys in jobs:
 selection="obs=[o for o in bpy.context.scene.objects if o.type=='MESH' and not any(c.name.startswith(('90_','98_')) for c in o.users_collection)]"
 if selected:selection=f"obs=[o for o in bpy.context.scene.objects if o.name.split('.')[0]=={selected!r}]"
 r=code("import bpy\nbpy.ops.object.select_all(action='DESELECT')\n"+selection+"\nassert obs, 'selection missing'\nfor o in obs:o.select_set(True)\nbpy.context.view_layer.objects.active=obs[0]")
 if 'Error' in r or 'selection missing' in r:raise RuntimeError(r)
 key('KP_Decimal')
 for k in keys:key(k)
 code("import bpy\nbpy.ops.object.select_all(action='DESELECT')")
 time.sleep(2);p=pose();out=dest/f'{len(frames):02d}-{name}.png';call('server_desktop','desktop_screenshot',image=out);frames.append({'name':name,'screenshot':str(out.relative_to(ROOT)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),**p});(dest/'frames.json').write_text(json.dumps(frames,indent=2));(dest/'input-log.json').write_text(json.dumps(events,indent=2));print('INSPECTED',name,flush=True)
print('INSPECTION_COMPLETE',len(frames),flush=True)
