from pathlib import Path
import struct,json,hashlib,io,collections
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];p=ROOT/'model/CISCO-Nexus-N9K-C9336C-FX2.glb';b=p.read_bytes();magic,version,length=struct.unpack_from('<4sII',b);assert magic==b'glTF' and version==2 and length==len(b)
chunks=[];off=12
while off<len(b):
 n,t=struct.unpack_from('<II',b,off);off+=8;chunks.append((t,b[off:off+n]));off+=n;assert n%4==0
assert off==len(b) and chunks[0][0]==0x4e4f534a
d=json.loads(chunks[0][1]);binary=next(c for t,c in chunks if t==0x004e4942);assert d['buffers'][0]['byteLength']<=len(binary)
images=[]
for i,x in enumerate(d.get('images',[])):
 assert 'bufferView' in x and 'uri' not in x;v=d['bufferViews'][x['bufferView']];raw=binary[v.get('byteOffset',0):v.get('byteOffset',0)+v['byteLength']];im=Image.open(io.BytesIO(raw));im.load();images.append({'index':i,'name':x.get('name'),'size':list(im.size),'mode':im.mode,'format':im.format,'bytes':len(raw)})
materials=[]
for m in d.get('materials',[]):
 ext=m.get('extensions',{});r={'name':m.get('name'),'alphaMode':m.get('alphaMode','OPAQUE'),'doubleSided':m.get('doubleSided',False),'transmission':ext.get('KHR_materials_transmission',{}).get('transmissionFactor',0),'normal_scale':m.get('normalTexture',{}).get('scale',None)};assert r['alphaMode']=='OPAQUE' and not r['doubleSided'] and r['transmission']==0;materials.append(r)
counts=collections.Counter(n.get('extras',{}).get('component_type') for n in d.get('nodes',[]));assert counts['business_port']==36 and counts['fan_module']==3 and counts['psu_module']==2 and counts['rack_ear']==2
assert not d.get('cameras') and 'KHR_lights_punctual' not in d.get('extensions',{})
assert not any(n.get('name','').startswith(('Studio','SOURCE_TEXT_','QA_')) for n in d['nodes'])
triangles=sum(d['accessors'][pr['indices']]['count']//3 for m in d['meshes'] for pr in m['primitives'] if pr.get('mode',4)==4)
r={'pass':True,'file':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'version':version,'nodes':len(d['nodes']),'meshes':len(d['meshes']),'unique_mesh_triangles':triangles,'mesh_node_instances':sum('mesh' in n for n in d['nodes']),'component_counts':{str(k):v for k,v in counts.items()},'materials':materials,'embedded_images':images,'extensionsUsed':d.get('extensionsUsed',[]),'extensionsRequired':d.get('extensionsRequired',[])}
(ROOT/'qa/glb-container.json').write_text(json.dumps(r,indent=2));(ROOT/'qa/glb-scene.json').write_text(json.dumps(d,indent=2));print(json.dumps({k:r[k] for k in ['pass','bytes','nodes','meshes','mesh_node_instances','unique_mesh_triangles','sha256']}))
