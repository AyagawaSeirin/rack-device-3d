from pathlib import Path
import json,csv,hashlib,shutil
from PIL import Image
P=Path('/root/Project/rack-device-3d/Dell-C6420-2.5inch/v002')
with (P.parent/'v001/sources.csv').open() as f:rows=list(csv.DictReader(f));fields=list(rows[0])
seen={r['asset_url'] for r in rows}
for fn in ['sources/v002-supplement-index.json','sources/third_party/carrier-source-downloads.json','sources/third_party/carrier-ebay-sources.json','sources/third_party/top-search-downloads.json','sources/third_party/top-search-downloads-2.json']:
 for x in json.loads((P/fn).read_text()):
  url=x.get('url',x.get('image_url'));path=Path(x['path']);page=x.get('page','')
  if url in seen:continue
  seen.add(url);name=path.name
  notes=x.get('adoption',x.get('role',''));model='C6400 chassis, listed C6420 four-node system';nodes='4';config='24x2.5 target; configuration variations recorded';view='See original photograph';confidence='medium: real photo, fitted options checked separately'
  if name.startswith('dxd9h'):
   model='DXD9H-style compatible unbranded carrier';nodes='not applicable';config='2.5-inch carrier';view='Carrier front/hinge/open handle details';notes='Construction only: three handle windows, steel lever, honeycomb recessed behind, hinge and release. Not evidence of OEM branding or exact SKU.'
  if name.startswith('abacus'):
   view='Front elevated' if name!='abacus-3.webp' else 'Rear elevated and top labels';notes='Clear real C6400/C6420 top printed labels; 2400W EPP corroborated. Different NIC/expansion option excluded. Abacus3 is the final top-label pixel source.'
  if name.startswith('gfsi'):
   view='Elevated front or rear/top';notes='Supplementary top-label corroboration; 2000W PSU variant NOT adopted.'
  if name.startswith('itinstock'):
   view='Node internal tray';notes='Internal sheet construction and sled arrangement only; no precise PCB or alternate external NIC details copied.'
  if name.startswith('bargain'):
   notes+=' Final normal carrier shape uses front bargain02; 0-23 numbering/1600W options excluded, retain official four-node mapping and NSL/ETB rear.'
  with Image.open(path) as im:im.verify()
  rows.append(dict(zip(fields,[page,url,str(path.relative_to(P)),'third-party original photograph',view,model,nodes,config,'',notes,confidence,str(x.get('status','200 image verified'))])))
# Carry all original raw assets referenced in the archived source manifest into the self-contained version.
for r in rows:
 if not r['local_path']:continue
 dest=P/r['local_path']
 if not dest.exists():
  original=P.parent/'v001'/r['local_path']
  if original.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(original,dest)
 if 'nsl-' in r['local_path'] and 'C6420' not in Path(r['local_path']).name:r['confirmed_details']+=' v002: plastic blanks on source front are superseded by user-requested normal carriers; source remains for shell, ears, lid and locked rear.'
with (P/'sources.csv').open('w',newline='') as f:w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(rows)
checks=[]
for r in rows:
 p=P/r['local_path']
 if p.is_file():checks.append({'path':r['local_path'],'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'source_url':r['asset_url']})
(P/'sources/asset-integrity.json').write_text(json.dumps(checks,indent=2))
print('Sources',len(rows),'local verified hash records',len(checks))
