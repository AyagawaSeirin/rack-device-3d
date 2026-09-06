"""Real server_desktop inputs/screenshots, independently queried Blender viewport poses."""
from pathlib import Path
import subprocess,json,time,datetime,math,hashlib,sys
ROOT=Path(__file__).resolve().parents[1];label=sys.argv[1] if len(sys.argv)>1 else 'original-solid';dest=ROOT/'desktop'/label;dest.mkdir(parents=True,exist_ok=True)
CLIENT=['/root/.local/share/uv/tools/blender-mcp/bin/python','/root/.local/share/blender-mcp-setup/mcp_call.py'];PROMPT=(ROOT/'REQUEST.md').read_text().split('\n\n')[1];events=[]
def call(server,tool,args=None,image=None):
 cmd=CLIENT+[server,tool]
 if args is not None:cmd+=['--args',json.dumps(args,ensure_ascii=False)]
 if image:cmd+=['--image-out',str(image)]
 r=subprocess.run(cmd,text=True,capture_output=True,check=True,timeout=205);return r.stdout

def key(k):
 answer=call('server_desktop','desktop_key',{'key':k});events.append({'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'key':k,'tool_result':answer.strip()})
def pose():
 code="import bpy,json\nfrom mathutils import Vector\nv=next(a.spaces.active for a in bpy.context.screen.areas if a.type=='VIEW_3D');r=v.region_3d\nprint(json.dumps({'q':list(r.view_rotation),'view_direction':list(r.view_rotation@Vector((0,0,-1))),'distance':r.view_distance,'location':list(r.view_location),'mode':v.shading.type,'file':bpy.data.filepath,'scene':bpy.context.scene.name}))"
 s=call('blender','execute_blender_code',{'code':code,'user_prompt':PROMPT});return json.JSONDecoder().raw_decode(s[s.index('{'):])[0]
def angle(a,b):
 dot=sum(x*y for x,y in zip(a,b));norm=math.sqrt(sum(x*x for x in a)*sum(x*x for x in b));return math.degrees(2*math.acos(min(1,abs(dot/norm))))
status=call('server_desktop','desktop_status');(dest/'desktop-status.json').write_text(status)
# Focus was established and one rotation verified from a fresh screenshot before launching.
key('KP_1');time.sleep(.8);key('KP_8');time.sleep(.6);key('KP_8');time.sleep(.8);key('KP_Add');time.sleep(.8)
frames=[]
for n in range(25):
 if n:
  key('KP_6');time.sleep(1.1)
 p=pose()
 if n:
  for retry in range(3):
   delta=angle(frames[-1]['q'],p['q'])
   if delta>1:break
   time.sleep(1);p=pose()
  assert 13.8<delta<16.2, f'No valid15 degree input rotation at frame{n}: {delta}'
 else:delta=0
 time.sleep(.5);out=dest/f'frame-{n:02d}.png';call('server_desktop','desktop_screenshot',image=out)
 frames.append({'index':n,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'screenshot':str(out.relative_to(ROOT)),'sha256':hashlib.sha256(out.read_bytes()).hexdigest(),'step_degrees_measured':delta,**p})
 (dest/'frames.json').write_text(json.dumps(frames,indent=2));(dest/'input-log.json').write_text(json.dumps(events,indent=2));print('DESKTOP_FRAME',label,n,'measured step',round(delta,4),flush=True)
closure=angle(frames[0]['q'],frames[-1]['q']);assert closure<.05
report={'pass':True,'frame_count':len(frames),'actual_key_events':len(events),'full_revolution_steps':24,'closure_angle_degrees':closure,'absolute_quaternion_dot_used':True,'all_intermediate_steps_verified':True,'mode':frames[0]['mode'],'native_screenshots':True,'first_last_pixel_files_distinct':frames[0]['sha256']!=frames[-1]['sha256'],'note':'Angles computed from queried viewport quaternion; key acknowledgements alone are not evidence.'}
(dest/'closure.json').write_text(json.dumps(report,indent=2));print('ORBIT_COMPLETE',json.dumps(report),flush=True)
