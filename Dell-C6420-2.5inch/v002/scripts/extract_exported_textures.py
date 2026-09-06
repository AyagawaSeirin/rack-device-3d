from pathlib import Path
import json,struct,hashlib,re
from PIL import Image
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002');dest=P/'textures/delivery';dest.mkdir(exist_ok=True);b=(P/'model/DELL-PowerEdge-C6420-4N-24SFF.glb').read_bytes();jlen,jtype=struct.unpack_from('<II',b,12);g=json.loads(b[20:20+jlen]);binstart=28+jlen;rows=[]
for i,img in enumerate(g['images']):
 bv=g['bufferViews'][img['bufferView']];raw=b[binstart+bv.get('byteOffset',0):binstart+bv.get('byteOffset',0)+bv['byteLength']];ext='.png' if img['mimeType']=='image/png' else '.jpg';name=re.sub('[^A-Za-z0-9._-]','_',img.get('name',f'image{i}'));path=dest/f'{i:02d}-{name}{ext}';path.write_bytes(raw)
 with Image.open(path) as im:size=im.size;im.verify()
 rows.append({'glb_image':i,'name':img.get('name'),'path':str(path.relative_to(P)),'pixels':list(size),'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})
(P/'textures/delivery/manifest.json').write_text(json.dumps(rows,indent=2));print('Extracted exact GLB embedded images',len(rows))
