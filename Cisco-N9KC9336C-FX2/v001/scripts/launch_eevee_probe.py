from pathlib import Path
import subprocess,json,os
ROOT=Path(__file__).resolve().parents[1]
cmd=['/root/.local/share/uv/tools/blender-mcp/bin/python','/root/.local/share/blender-mcp-setup/mcp_call.py','server_desktop','desktop_status']
r=subprocess.run(cmd,capture_output=True,text=True,check=True);status=json.loads(r.stdout);env=os.environ.copy();env['DISPLAY']=status['display'];env['LP_NUM_THREADS']='4'
with (ROOT/'qa/eevee-probe.log').open('w') as log:
 subprocess.run(['/usr/bin/blender','-b',str(ROOT/'model/08-neutral-studio-calibrated.blend'),'-t','4','--python',str(ROOT/'scripts/render_eevee_probe.py')],env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
