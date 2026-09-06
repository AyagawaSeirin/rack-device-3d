from pathlib import Path
import json,hashlib
import pymupdf
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
idx=json.loads((ROOT/'sources/download-index.json').read_text());out=[]
for r in idx:
 if r['status']!='downloaded':continue
 p=ROOT/r['local_path'];b=p.read_bytes();item={'path':r['local_path'],'sha256':hashlib.sha256(b).hexdigest(),'source_bytes_unchanged':hashlib.sha256(b).hexdigest()==r['sha256']}
 if p.suffix=='.pdf':
  item.update(pdf_signature=b.startswith(b'%PDF-'),pages=len(pymupdf.open(p)))
 elif p.suffix in ['.jpg','.png','.webp','.jpeg']:
  im=Image.open(p);im.load();item.update(image_decode=True,size=im.size)
 out.append(item)
report={'pass':all(i['source_bytes_unchanged'] and i.get('pdf_signature',True) for i in out),'count':len(out),'files':out}
(ROOT/'qa/source-integrity.json').write_text(json.dumps(report,indent=2));print(report['pass'],report['count'])
