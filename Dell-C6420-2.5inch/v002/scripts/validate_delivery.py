from pathlib import Path
from html.parser import HTMLParser
from PIL import Image
import json,hashlib,csv,struct
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002')
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,t,attrs):
  for a,v in attrs:
   if a in ['href','src'] and v and not v.startswith(('http','#','data:')):self.links.append(v)
h=Links();h.feed((P/'REVIEW.html').read_text());missing=sorted({x for x in h.links if not (P/x).is_file()});assert not missing,missing
manifest=[]
for sub in ['model','previews','textures/delivery','desktop/turntable-glb']:
 files=list((P/sub).glob('*'))
 for f in files:
  if not f.is_file() or sub=='model' and f.name not in ['DELL-PowerEdge-C6420-4N-24SFF.blend','DELL-PowerEdge-C6420-4N-24SFF.glb']:continue
  if f.suffix.lower() in ['.png','.jpg']:
   with Image.open(f) as im:im.verify()
  manifest.append({'file':str(f.relative_to(P)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
blend=P/'model/DELL-PowerEdge-C6420-4N-24SFF.blend';assert blend.read_bytes()[:7]==b'BLENDER'
b=(P/'model/DELL-PowerEdge-C6420-4N-24SFF.glb').read_bytes();assert b[:4]==b'glTF' and struct.unpack_from('<I',b,8)[0]==len(b)
assert hashlib.sha256(b).hexdigest()==json.loads((P/'qa/glb-container-audit.json').read_text())['sha256']
selected=(P/'references/SELECTED.txt').read_text().splitlines();assert len(selected)==22
for rel in selected:
 with Image.open(P/'references'/rel) as im:im.verify()
(P/'DELIVERY-MANIFEST.json').write_text(json.dumps({'main_version':'v002','artifacts':manifest,'html_local_links_checked':len(set(h.links)),'missing_links':missing,'selected_AI_references_checked':22,'exact_GLb_hash_matches_container_QA':True},indent=2));print('DELIVERY_VALID',len(manifest),'artifacts;',len(set(h.links)),'review links;22 selected references')
