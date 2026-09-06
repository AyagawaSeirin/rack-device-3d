from pathlib import Path
import subprocess,json,sys,datetime
ROOT=Path(__file__).resolve().parents[1]
PROMPT=(ROOT/'REQUEST.md').read_text().split('\n\n')[1]
p=Path(sys.argv[1]).resolve()
code='from pathlib import Path\n_task_script=Path('+repr(str(p))+')\nexec(compile(_task_script.read_text(),str(_task_script),"exec"),{"__file__":str(_task_script),"PROJECT_ROOT":_task_script.parents[1]})'
args={'user_prompt':PROMPT,'code':code}
cmd=['/root/.local/share/uv/tools/blender-mcp/bin/python','/root/.local/share/blender-mcp-setup/mcp_call.py','blender','execute_blender_code','--args',json.dumps(args,ensure_ascii=False)]
r=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
print(r.stdout);(ROOT/'qa'/('mcp-'+p.stem+'.log')).write_text(r.stdout)
sys.exit(r.returncode)
