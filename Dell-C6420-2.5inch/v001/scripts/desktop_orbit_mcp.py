"""Record an actual desktop-MCP keyboard orbit; no bpy view manipulation.
Cursor must already be in the inspected viewport. Screenshots are original MCP image bytes.
"""
import asyncio,base64,json,os,tomllib,sys,time
from pathlib import Path
from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
P=Path('/root/Blender/DELL-C6420/v001'); OUT=P/'desktop/turntable-material';OUT.mkdir(exist_ok=True)
async def main():
 conf=tomllib.loads(Path('/root/.codex/config.toml').read_text())['mcp_servers']['server_desktop'];env=dict(os.environ);env.update(conf.get('env',{}));log=[]
 params=StdioServerParameters(command=conf['command'],args=conf.get('args',[]),env=env)
 with (P/'qa/desktop-orbit-mcp-server.log').open('a') as err:
  async with stdio_client(params,errlog=err) as (read,write):
   async with ClientSession(read,write) as client:
    await client.initialize()
    for i in range(25):
     if i:
      key=await client.call_tool('desktop_key',{'key':'KP_6'});assert not key.isError
      await asyncio.sleep(1.4)
     result=await client.call_tool('desktop_screenshot',{})
     saved=False
     for block in result.content:
      if block.type=='image':
       path=OUT/f'frame-{i:03}.png';path.write_bytes(base64.b64decode(block.data));saved=True
     assert saved
     log.append({'frame':i,'cumulative_orbit_degrees':i*15,'input':None if i==0 else 'desktop_key KP_6','screenshot':str(path.relative_to(P)),'time':time.time()})
     (P/'qa/desktop-orbit-events.json').write_text(json.dumps(log,indent=2))
     print('CAPTURED',i,flush=True)
asyncio.run(main())
